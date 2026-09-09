from app.db import get_db_connection, init_db
from app.services.embeddings import generate_text_embedding

def seed_database():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()

    # Bazanı təmizləyirik
    cur.execute("TRUNCATE review_logs, posts, images RESTART IDENTITY CASCADE;")

    # 1. Nümunə Şəkillər (Corpus)
    sample_images = [
        {
            "filename": "red_fox_forest.jpg",
            "subject": "red fox",
            "category": "animal",
            "attributes": ["orange fur", "forest", "wild"],
            "caption": "A vibrant red fox standing among pine trees in autumn forest",
            "confidence": 0.95,
            "flagged": False
        },
        {
            "filename": "gray_wolf_snow.jpg",
            "subject": "gray wolf",
            "category": "animal",
            "attributes": ["gray fur", "pack", "snow"],
            "caption": "A gray wolf staring directly ahead in snowy woodland environment",
            "confidence": 0.92,
            "flagged": False
        },
        {
            "filename": "golden_retriever_park.jpg",
            "subject": "dog",
            "category": "animal",
            "attributes": ["golden fur", "pet", "domestic"],
            "caption": "A friendly golden retriever dog sitting on green grass",
            "confidence": 0.88,
            "flagged": False
        },
        {
            "filename": "blurred_unknown.jpg",
            "subject": "unknown mammal",
            "category": "animal",
            "attributes": ["blurry", "shadow"],
            "caption": "An unidentifiable blurry creature in dark shadows",
            "confidence": 0.45,  # Low confidence -> Flagged[cite: 1]
            "flagged": True
        }
    ]

    for img in sample_images:
        emb, _ = generate_text_embedding(f"{img['subject']} {img['caption']}")
        cur.execute("""
            INSERT INTO images (filename, subject, category, attributes, caption, confidence, embedding, flagged)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            img['filename'], img['subject'], img['category'],
            img['attributes'], img['caption'], img['confidence'],
            emb, img['flagged']
        ))

    # 2. Nümunə Blog Postları[cite: 1]
    sample_posts = [
        {
            "title": "The Habitat and Behavior of Red Foxes",
            "content": "Red foxes are small wild mammals known for their rusty orange fur and intelligence in forested regions."
        },
        {
            "title": "Understanding Gray Wolf Pack Dynamics",
            "content": "Gray wolves live in structured packs and hunt in cold, snowy environments across North America."
        },
        {
            "title": "Quantum Computing Innovations in 2026",
            "content": "Superconducting qubits and quantum encryption are redefining modern cryptography and cloud technology."
        }
    ]

    for post in sample_posts:
        emb, _ = generate_text_embedding(f"{post['title']} {post['content']}")
        cur.execute("""
            INSERT INTO posts (title, content, embedding)
            VALUES (%s, %s, %s);
        """, (post['title'], post['content'], emb))

    conn.commit()
    cur.close()
    conn.close()
    print("Database seeded successfully with test images and posts!")

if __name__ == "__main__":
    seed_database()