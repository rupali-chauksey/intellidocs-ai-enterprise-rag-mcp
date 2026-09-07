from pathlib import Path
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List

from app.config import settings, UPLOAD_DIR, DB_PATH
from app.graph import get_graph
from app.ingestion import index_all_uploads
from app.routes.upload import router as upload_router
from app.routes.documents import router as document_router

app = FastAPI(
    title="IntelliDocs AI",
    description="Enterprise AI Assistant — RAG + MCP + Database + Web Search + Conversation Memory",
    version="3.0.0",
)
app.include_router(document_router)
app.include_router(upload_router)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    conversation_history: Optional[List[ChatMessage]] = None


@app.on_event("startup")
def startup():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    result = index_all_uploads(force=False)
    print(f"[STARTUP] Upload index: {result}")
    if not settings.groq_api_key:
        print("[WARNING] GROQ_API_KEY is empty. Add it to .env before asking questions.")


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/healthz")
@app.get("/health")
def health():
    try:
        from app.services.vector_store import VectorStore
        vector_count = VectorStore().count()
    except Exception:
        vector_count = 0
    return {
        "status": "ok",
        "version": app.version,
        "llm_model": settings.llm_model,
        "vector_chunks": vector_count,
        "database_available": DB_PATH.exists(),
    }


@app.post("/ingest")
def ingest():
    from app.ingestion import rebuild_upload_index
    try:
        return {"status": "ingested", **rebuild_upload_index()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/chat")
def chat(request: ChatRequest):
    if not settings.groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured. Add it to .env and restart the server.")
    history = [m.model_dump() for m in (request.conversation_history or [])][-8:]
    start = time.time()
    try:
        result = get_graph().invoke({
            "query": request.query.strip(),
            "history": history,
            "kb_results": [],
            "web_results": [],
            "citations": [],
            "used_web_search": False,
        })
        elapsed = round(time.time() - start, 2)
        return {
            "answer": result.get("answer", ""),
            "route": result.get("route", "rag"),
            "used_web_search": result.get("used_web_search", False),
            "citations": result.get("citations", []),
            "tool_used": result.get("tool_used", ""),
            "time_taken": elapsed,
            "debug": result.get("debug", {}),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
