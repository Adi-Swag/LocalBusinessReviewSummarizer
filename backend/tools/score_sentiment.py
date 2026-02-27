import os
import json
import google.generativeai as genai
from google.adk.tools import FunctionTool

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def score_sentiment(review: str) -> dict:
    """Scores a single customer review as positive, neutral, or negative with a confidence score between 0.0 and 1.0."""
    if not review:
        return {"sentiment": "neutral", "score": 0.0}
    
    prompt = f"""
    Classify this customer review sentiment.
    
    Review: {review}
    
    Respond in JSON only, no extra text:
    {{
        "sentiment": "positive" | "neutral" | "negative",
        "score": <float between 0.0 and 1.0>
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"sentiment": "neutral", "score": 0.0}

score_sentiment_tool = FunctionTool(func=score_sentiment)