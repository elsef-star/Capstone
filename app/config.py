import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PORT: int = int(os.getenv("PORT", 8000))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/image_relevance_db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", 0.75))

settings = Settings()