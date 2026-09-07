import os
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings, UPLOAD_DIR
from app.services.document_loader import DocumentLoader
from app.services.chunker import Chunker
from app.services.vector_store import VectorStore

_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        _embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return _embeddings


def load_documents(data_dir: str):
    docs = []
    for path in Path(data_dir).glob("**/*"):
        if path.suffix.lower() in {".txt", ".md"}:
            docs.extend(TextLoader(str(path), encoding="utf-8").load())
        elif path.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(path)).load())
        elif path.suffix.lower() == ".docx":
            docs.extend(UnstructuredWordDocumentLoader(str(path)).load())
    return docs


def _prepare_chunks(documents, source_name: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["source"] = source_name
    return chunks


def index_uploaded_file(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    loader = DocumentLoader()
    documents = loader.load(str(path))
    if not documents:
        raise ValueError("Document is empty or could not be read.")

    chunks = _prepare_chunks(documents, path.name)
    if not chunks:
        raise ValueError("No text chunks could be created from this document.")

    store = VectorStore()
    # Re-uploading the same filename should replace its old chunks, not duplicate them.
    store.delete_source(path.name)
    count = store.add_documents(chunks)
    print(f"Indexed {count} chunks from {path.name}")
    return {"chunks": count, "source": path.name}


def index_all_uploads(force: bool = False):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    store = VectorStore()
    indexed = 0
    skipped = 0
    allowed = {".pdf", ".txt", ".md", ".docx"}

    for path in sorted(UPLOAD_DIR.iterdir()):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        if not force and store.source_chunk_count(path.name) > 0:
            skipped += 1
            continue
        index_uploaded_file(str(path))
        indexed += 1

    return {"indexed": indexed, "skipped": skipped, "total": indexed + skipped}


def rebuild_upload_index():
    store = VectorStore()
    # Clear collection safely by IDs, then rebuild from current uploads.
    try:
        data = store.db.get(include=[])
        ids = data.get("ids", [])
        if ids:
            store.db.delete(ids=ids)
    except Exception:
        pass
    return index_all_uploads(force=True)


def get_vectorstore():
    return VectorStore().db


def build_vectorstore(data_dir: str = None, persist_dir: str = None):
    """Compatibility helper for indexing the configured data directory."""
    data_dir = data_dir or settings.data_dir
    persist_dir = persist_dir or settings.chroma_dir
    raw_docs = load_documents(data_dir)
    if not raw_docs:
        raise ValueError(f"No supported documents found in {data_dir}")
    chunks = _prepare_chunks(raw_docs, "data")
    store = VectorStore()
    store.add_documents(chunks)
    return store.db


if __name__ == "__main__":
    print(rebuild_upload_index())
