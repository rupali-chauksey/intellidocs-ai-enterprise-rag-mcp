from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    groq_api_key: str = ""
    llm_model: str = "openai/gpt-oss-120b"
    chroma_dir: str = str(BASE_DIR / "chroma_db")
    data_dir: str = str(BASE_DIR / "data")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5
    relevance_threshold: float = 0.30
    web_max_results: int = 4

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
UPLOAD_DIR = BASE_DIR / "app" / "uploads"
DB_PATH = BASE_DIR / "company.db"
