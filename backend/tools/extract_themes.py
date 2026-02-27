import os
import json
import google.generativeai as genai
from google.adk.tools import FunctionTool

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")


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
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"key_point": "", "category": "other"}


extract_themes_tool = FunctionTool(func=extract_themes)
