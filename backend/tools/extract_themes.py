import os
import json
from dotenv import load_dotenv
load_dotenv()
import google.genai as genai
from google.adk.tools import FunctionTool
import litellm

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY2"))


def extract_themes(review: str) -> dict:
    """Summarizes a customer review into a key point and assigns a category."""
    if not review:
        return {"key_point": "", "category": "other"}

    prompt = f"""
    Analyze this customer review and provide a one-sentence summary and a category.

    Review: {review}

    Respond in JSON only, no extra text:
    {{
        "key_point": "<one sentence summary of the review>",
        "category": "food" | "service" | "ambiance" | "price" | "other"
    }}
    """

    try:
        response = litellm.completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"key_point": "", "category": "other"}


extract_themes_tool = FunctionTool(func=extract_themes)
