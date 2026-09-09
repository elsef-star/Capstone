from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db import get_db_connection
from app.services.guard import evaluate_mismatch_guard
from app.services.embeddings import generate_text_embedding

app = FastAPI(title="AI Image Understanding & Content Matching Engine")

class ReviewRequest(BaseModel):
    post_id: int
    image_id: int
    status: str  # APPROVED / REJECTED
    reason: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Matching Engine Service Running"}

@app.get("/api/posts/{post_id}/images")
def get_image_for_post(post_id: int):
    """
    Post üçün vector similarity əsasında ən yaxşı şəkli tapır və Mismatch Guard ilə yoxlayır.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Postu gətiririk
    cur.execute("SELECT id, title, content, embedding FROM posts WHERE id = %s;", (post_id,))
    post = cur.fetchone()
    if not post:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")

    post_id_val, title, content, post_embedding = post

    # Ən uyğun şəkli Cosine Similarity ilə tapırıq
    cur.execute("""
        SELECT id, filename, subject, category, caption, confidence, flagged,
               1 - (embedding <=> %s::vector) as similarity
        FROM images
        WHERE flagged = FALSE
        ORDER BY similarity DESC
        LIMIT 1;
    """, (post_embedding,))

    candidate = cur.fetchone()
    cur.close()
    conn.close()

    if not candidate:
        return {"status": "NO_MATCH", "reason": "No valid unflagged images in library"}

    img_id, filename, subject, category, caption, confidence, flagged, similarity = candidate

    # Mismatch Guard Yoxlanışı[cite: 1]
    is_safe, guard_reason = evaluate_mismatch_guard(
        post_title=title,
        image_subject=subject,
        image_category=category,
        confidence=confidence,
        similarity_score=float(similarity)
    )

    if not is_safe:
        return {
            "status": "REJECTED",
            "reason": guard_reason,
            "rejected_candidate": {
                "image_id": img_id,
                "filename": filename,
                "subject": subject,
                "similarity": round(float(similarity), 4)
            }
        }

    return {
        "status": "APPROVED",
        "match": {
            "image_id": img_id,
            "filename": filename,
            "subject": subject,
            "category": category,
            "similarity": round(float(similarity), 4),
            "guard_explanation": guard_reason
        }
    }

@app.post("/api/review")
def review_match(review: ReviewRequest):
    """
    Human-in-the-loop review workflow: Seçimi təsdiq/rədd edir.[cite: 1]
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO review_logs (post_id, image_id, status, reason)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (review.post_id, review.image_id, review.status, review.reason))
    log_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success", "log_id": log_id, "message": "Review logged"}
from fastapi import UploadFile, File
from app.services.vision import analyze_image_with_vision

@app.post("/api/images/ingest")
async def ingest_image(file: UploadFile = File(...)):
    """
    İstifadəçinin verdiyi şəkil faylını oxuyur, Gemini Vision ilə nə olduğunu tapır,
    nəticəni Zod/Pydantic schema ilə təsdiqləyib bazaya yazır.
    """
    image_bytes = await file.read()

    # 1. Vision AI şəkli analiz edir
    metadata, cost = analyze_image_with_vision(image_bytes)

    # 2. Tapılan təsvir üçün embedding yaradılır
    emb_text = f"{metadata.subject} {metadata.caption} {' '.join(metadata.attributes)}"
    emb, _ = generate_text_embedding(emb_text)

    # 3. Nəticə verilənlər bazasına yazılır
    conn = get_db_connection()
    cur = conn.cursor()
    
    flagged = metadata.confidence < 0.60  # Az dəqiqdirsə flaq qoyulur

    cur.execute("""
        INSERT INTO images (filename, subject, category, attributes, caption, confidence, embedding, flagged)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        file.filename, metadata.subject, metadata.category,
        metadata.attributes, metadata.caption, metadata.confidence,
        emb, flagged
    ))

    image_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "SUCCESS",
        "image_id": image_id,
        "filename": file.filename,
        "detected_analysis": metadata.model_dump(),
        "flagged_for_review": flagged,
        "estimated_cost_usd": cost
    }