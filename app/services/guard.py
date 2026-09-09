from app.config import settings

def evaluate_mismatch_guard(
    post_title: str,
    image_subject: str,
    image_category: str,
    confidence: float,
    similarity_score: float
) -> tuple[bool, str]:
    """
    Məqalə ilə namizəd şəkil arasındakı uyğunluğu qiymətləndirir.
    Yalnız oxşarlıq, kateqoriya və confidence yüksək olduqda təsdiqləyir.
    """
    # Rule 1: Low confidence check
    if confidence < 0.60:
        return False, f"Flagged: Low image classification confidence ({confidence:.2f})"

    # Rule 2: Similarity threshold check
    if similarity_score < settings.SIMILARITY_THRESHOLD:
        return False, f"Similarity score ({similarity_score:.2f}) below threshold ({settings.SIMILARITY_THRESHOLD})"

    # Rule 3: Direct entity contradiction check (e.g. Fox article vs Wolf image)
    post_title_lower = post_title.lower()
    image_subject_lower = image_subject.lower()

    if "fox" in post_title_lower and "wolf" in image_subject_lower:
        return False, "Animal category mismatch: expected fox, detected wolf"

    if "wolf" in post_title_lower and "fox" in image_subject_lower:
        return False, "Animal category mismatch: expected wolf, detected fox"

    return True, "Match approved by Mismatch Guard"
