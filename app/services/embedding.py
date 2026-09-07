from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings


class EmbeddingService:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    def get(self):
        return self.embedding
