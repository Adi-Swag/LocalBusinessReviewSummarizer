from google.adk.agents import LlmAgent
import os
from dotenv import load_dotenv
load_dotenv()
from tools.extract_themes import extract_themes_tool
from tools.trust_score import calculate_trust_score_tool
from tools.synthesize_summary import synthesize_summary_tool



summarization_agent = LlmAgent(
    name="summarization_agent",
    model="openai/gpt-4o-mini",
    description=(
        "Extracts themes from reviews, calculates a trust score, and synthesizes "
        "an overall business summary with pros, cons, and an audience tag."
    ),
    instruction="""
You are a summarization agent for local business reviews.

You will receive:
- `reviews`: a list of cleaned review strings
- `sentiment_results`: a list of sentiment dicts (output from the sentiment agent),
  each with keys "sentiment" and "score"

Follow these steps strictly in order:

1. For each review in `reviews`, call `extract_themes` on it individually.
   Collect all results into a list called theme_results.

2. Call `calculate_trust_score` with the full `sentiment_results` list.
   Keep the returned trust score result.

3. Call `synthesize_summary` with `sentiment_results` and `theme_results`.

4. Return a single combined dict:   
   {
     "trust_score_result": {
        "trust_score": ,
        "breakdown": {
            "sentiment_component": ,
            "consistency_component": ,
            "outlier_penalty":
        }
    },
     "summary": <result from step 3>
   }

Do not skip any review. Do not invent data. Only use the provided tools.
""",
    tools=[extract_themes_tool, calculate_trust_score_tool, synthesize_summary_tool],
)
