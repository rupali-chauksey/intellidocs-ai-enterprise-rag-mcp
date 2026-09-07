from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.uploader import save_upload_file
from app.ingestion import index_uploaded_file

router = APIRouter(tags=["Upload"])
ALLOWED = {".pdf", ".txt", ".md", ".docx"}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, MD, and DOCX files are supported.")
    try:
        path = await save_upload_file(file)
        result = index_uploaded_file(str(path))
        return {"success": True, "filename": filename, "chunks": result["chunks"], "status": "Indexed", "message": "Document uploaded and indexed successfully."}
    except Exception as exc:
        try:
            if 'path' in locals() and path.exists(): path.unlink()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Upload/indexing failed: {exc}")
