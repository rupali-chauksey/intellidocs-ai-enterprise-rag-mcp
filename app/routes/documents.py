from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.config import UPLOAD_DIR
from app.services.vector_store import VectorStore

router = APIRouter(tags=["Documents"])


def format_file_size(size_bytes: int) -> str:
    """Return a human-readable file size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"

    return f"{size_bytes / (1024 * 1024):.2f} MB"


@router.get("/documents")
def list_documents():

    store = VectorStore()
    files = []

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    for file in sorted(
        UPLOAD_DIR.iterdir(),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    ):

        if not file.is_file():
            continue

        chunks = store.source_chunk_count(file.name)
        size_bytes = file.stat().st_size

        files.append({
            "filename": file.name,
            "size": format_file_size(size_bytes),
            "size_bytes": size_bytes,
            "uploaded_at": datetime.fromtimestamp(
                file.stat().st_mtime
            ).strftime("%d-%m-%Y %H:%M"),
            "extension": file.suffix.lower(),
            "status": "Indexed" if chunks else "Not Indexed",
            "chunks": chunks,
        })

    return files


@router.delete("/documents/{filename}")
def delete_document(filename: str):

    safe_name = Path(filename).name
    path = UPLOAD_DIR / safe_name

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    try:
        VectorStore().delete_source(safe_name)
        path.unlink()

        return {
            "success": True,
            "message": f"{safe_name} deleted successfully.",
            "vectors_deleted": True,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {exc}",
        )