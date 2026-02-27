import os
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="Local Business Review Summarizer")

@app.get("/health")
def health_check():
    return {"status": "ok"}