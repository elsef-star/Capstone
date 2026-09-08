[ Image Library ] ---> ( Batch Processing ) ---> [ Vision AI Model ] ---> [ Structured Tags ]
|
[ Blog Post ] -----------------------------> ( Embedding Model ) -------> [ Vector Search ]
|
[ Mismatch Guard ]
|
( Match / Reject Decision )


## Setup & Running

1. **Install Dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
Environment Configuration:

Bash
cp .env.example .env
# Set your GEMINI_API_KEY inside .env
Database Setup & Seed:

Bash
docker compose up -d
python -m app.seed
Start Application:

Bash
uvicorn app.main:app --reload
Precision Metrics
Top-1 Precision: TBD% (Measured on evaluation dataset)

Limitations
Designed for small-to-medium image libraries (~50 images).