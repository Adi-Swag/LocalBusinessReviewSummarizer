import os
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
load_dotenv()
from tools.parse_reviews import parse_reviews_tool
from tools.score_sentiment import score_sentiment_tool



sentiment_agent = LlmAgent(
    name="sentiment_agent",
    model="openai/gpt-4o-mini",
    description=(
        "Cleans a list of raw customer reviews and scores each one as "
        "positive, neutral, or negative with a confidence score."
    ),
    instruction="""
You are a sentiment analysis agent for local business reviews.

When given a list of raw customer reviews, follow these steps strictly:

1. Call `parse_reviews` with the full list to clean and deduplicate the reviews.
2. For each review returned by `parse_reviews`, call `score_sentiment` on it individually.
3. Collect every result into a list.
4. Return a dict with:
- "cleaned_reviews": the list from parse_reviews
- "sentiment_results": the list of sentiment dicts

Do not skip any review. Do not summarize or paraphrase. Only call the provided tools.
""",
    tools=[parse_reviews_tool, score_sentiment_tool],
)
