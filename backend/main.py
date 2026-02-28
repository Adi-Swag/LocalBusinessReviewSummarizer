import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Local Business Review Summarizer")


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(router)
