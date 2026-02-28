import os
import json
from dotenv import load_dotenv
load_dotenv()
import google.genai as genai
from google.adk.tools import FunctionTool
import litellm

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY2"))


def synthesize_summary(sentiment_results: list[dict], theme_results: list[dict]) -> dict:
    """Generates an overall business summary from sentiment and theme analysis results.

    Args:
        sentiment_results: List of dicts with keys 'sentiment' and 'score'.
        theme_results: List of dicts with keys 'key_point' and 'category'.

    Returns:
        A dict with 'overall_summary', 'pros', 'cons', and 'who_is_this_for'.
    """
    if not sentiment_results and not theme_results:
        return {
            "overall_summary": "",
            "pros": [],
            "cons": [],
            "who_is_this_for": "",
        }

    all_themes = []
    for result in theme_results:
        all_themes.append({
            "key_point": result.get("key_point", ""),
            "category": result.get("category", "other")
        })

    prompt = f"""
You are analyzing customer reviews for a local business.

Sentiment results (each review rated positive/neutral/negative with a confidence score):
{json.dumps(sentiment_results, indent=2)}

Key points and categories extracted across all reviews:
{json.dumps(all_themes, indent=2)}

Based on this data, produce a concise business summary.

Respond in JSON only, no extra text:
{{
    "overall_summary": "<2-3 sentence summary of the business based on reviews>",
    "pros": ["<top pro 1>", "<top pro 2>", "<top pro 3>"],
    "cons": ["<top con 1>", "<top con 2>", "<top con 3>"],
    "who_is_this_for": "<short tag describing the ideal customer, e.g. 'families looking for casual dining'>"
}}
"""

    try:
        response = litellm.completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {
            "overall_summary": "",
            "pros": [],
            "cons": [],
            "who_is_this_for": "",
        }


synthesize_summary_tool = FunctionTool(func=synthesize_summary)