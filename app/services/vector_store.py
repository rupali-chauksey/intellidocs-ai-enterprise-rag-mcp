from pathlib import Path
from typing import Iterable

from langchain_community.vectorstores import Chroma

from app.config import settings
from app.services.embedding import EmbeddingService

COLLECTION_NAME = "intellidocs"


class VectorStore:
    def __init__(self):
        Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
        self.db = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=settings.chroma_dir,
            embedding_function=EmbeddingService().get(),
        )

    def add_documents(self, documents):
        documents = list(documents)
        if not documents:
            return 0
        self.db.add_documents(documents)
        return len(documents)

    def delete_source(self, source: str):
        # Remove all chunks belonging to one document.
        self.db.delete(where={"source": source})

    def similarity_search(self, query: str, k: int = 5):
        try:
            return self.db.similarity_search_with_relevance_scores(query, k=k)
        except Exception:
            # Compatibility fallback for older Chroma/LangChain versions.
            return self.db.similarity_search_with_score(query, k=k)

    def source_chunk_count(self, source: str) -> int:
        try:
            data = self.db.get(where={"source": source}, include=[])
            return len(data.get("ids", []))
        except Exception:
            return 0

    def count(self) -> int:
        try:
            return self.db._collection.count()
        except Exception:
            return 0
