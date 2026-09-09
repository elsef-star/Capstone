from app.db import get_db_connection
from app.services.guard import evaluate_mismatch_guard

def run_evaluation():
    conn = get_db_connection()
    cur = conn.cursor()

    # Etiketlənmiş test seti (Post ID -> Gözlənilən Şəkil Subyekti)
    ground_truth = {
        1: "red fox",    # Post 1 (Red Fox) -> red_fox_forest.jpg
        2: "gray wolf",  # Post 2 (Gray Wolf) -> gray_wolf_snow.jpg
        3: None          # Post 3 (Quantum) -> REJECTED / NO_MATCH olmalıdır
    }

    total_tests = len(ground_truth)
    correct_predictions = 0

    print("\n=== TOP-1 PRECISION EVALUATION RUN ===")

    for post_id, expected_subject in ground_truth.items():
        cur.execute("SELECT id, title, embedding FROM posts WHERE id = %s;", (post_id,))
        post = cur.fetchone()
        if not post:
            continue

        _, title, post_embedding = post

        cur.execute("""
            SELECT id, filename, subject, category, caption, confidence,
                   1 - (embedding <=> %s::vector) as similarity
            FROM images
            WHERE flagged = FALSE
            ORDER BY similarity DESC
            LIMIT 1;
        """, (post_embedding,))

        candidate = cur.fetchone()
        if not candidate:
            prediction = None
        else:
            img_id, filename, subject, category, caption, confidence, similarity = candidate
            is_safe, _ = evaluate_mismatch_guard(
                post_title=title,
                image_subject=subject,
                image_category=category,
                confidence=confidence,
                similarity_score=float(similarity)
            )
            prediction = subject if is_safe else None

        if prediction == expected_subject:
            correct_predictions += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(f"Post {post_id} ('{title[:30]}...'): Expected='{expected_subject}', Got='{prediction}' -> [{status}]")

    precision = (correct_predictions / total_tests) * 100
    print("------------------------------------------")
    print(f"Top-1 Precision: {precision:.2f}% ({correct_predictions}/{total_tests})")
    print("==========================================\n")

    cur.close()
    conn.close()
    return precision

if __name__ == "__main__":
    run_evaluation()