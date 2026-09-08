from fastapi import FastAPI
from app.config import settings

app = FastAPI(title="AI Image Understanding & Content Matching Engine")

@app.get("/")
def root():
    return {"status": "ok", "message": "Matching Engine Service Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}