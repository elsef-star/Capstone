from google import genai
from app.config import settings

ESTIMATED_COST_PER_EMBEDDING_CALL = 0.00001  # USD

def generate_text_embedding(text: str) -> tuple[list[float], float]:
    """
    Mətni 768-ölçülü embedding vektoruna çevirir.
    API xətası (404/400) baş verdikdə avtomatik fallback mock vektor qaytarır.
    """
    # API key yoxdursa və ya şablon dəyərdirsə mock vektor qaytar
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
        return [0.01] * 768, ESTIMATED_COST_PER_EMBEDDING_CALL

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embedding.values, ESTIMATED_COST_PER_EMBEDDING_CALL
    except Exception as e:
        print(f"[WARN] Embedding API Error ({e}). Fallback mock vektordan istifadə olunur.")
        return [0.01] * 768, ESTIMATED_COST_PER_EMBEDDING_CALL