import os
import json
from dotenv import load_dotenv
load_dotenv()
import google.genai as genai
from google.adk.tools import FunctionTool
import litellm

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY2"))

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
        response = litellm.completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"sentiment": "neutral", "score": 0.0}

score_sentiment_tool = FunctionTool(func=score_sentiment)