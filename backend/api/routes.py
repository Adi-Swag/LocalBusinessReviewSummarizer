from fastapi import APIRouter
from agents.orchestrator import orchestrator
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import uuid
import json

class ReviewsRequest(BaseModel):
    business_name: str
    reviews: list[str]

router = APIRouter()

session_service = InMemorySessionService()
runner = Runner(
    agent=orchestrator,
    app_name="local_business_summarizer",
    session_service=session_service
)

@router.post("/api/analyze")
async def analyze_reviews(request: ReviewsRequest):
    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name="local_business_summarizer",
        user_id="user",
        session_id=session_id
    )

    events = runner.run(
        user_id="user",
        session_id=session_id,
        new_message=Content(parts=[Part(text=str(request.reviews))])
    )
    
    final_response = ""
    for event in events:
        print(f"Event: {event}")  # temporary debug line
        if event.is_final_response():
            final_response = event.content.parts[0].text
            break
    try:
        final_response = json.loads(final_response)
    except json.JSONDecodeError:
        final_response = {"error": "Failed to parse agent response as JSON", "raw_response": final_response}    
    return final_response