import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

def get_db_connection():
    conn = psycopg2.connect(settings.DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # pgvector extension-ı aktivləşdiririk
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    
    # Images cədvəli
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            subject VARCHAR(255),
            category VARCHAR(100),
            attributes TEXT[],
            caption TEXT,
            confidence FLOAT,
            embedding vector(768),
            flagged BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Posts cədvəli
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            embedding vector(768),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Match review cədvəli
    cur.execute("""
        CREATE TABLE IF NOT EXISTS review_logs (
            id SERIAL PRIMARY KEY,
            post_id INT REFERENCES posts(id),
            image_id INT REFERENCES images(id),
            status VARCHAR(50),
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database tables initialized successfully!")