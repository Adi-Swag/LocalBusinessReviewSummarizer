from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from backend.agents.sentiment_agent import sentiment_agent
from backend.agents.summarization_agent import summarization_agent

orchestrator = LlmAgent(
    name="orchestrator",
    model="gemini-2.5-pro",
    description=(
        "Orchestrates the full local business review analysis pipeline: "
        "sentiment scoring followed by theme extraction, trust scoring, and summarization."
    ),
    instruction="""
You are the orchestrator for a local business review analysis system.

You will receive a list of raw customer reviews for a local business.

Follow these steps strictly in order:

1. Call `sentiment_agent` with the raw reviews list.
   It will clean the reviews and return:
   - `cleaned_reviews`: the deduplicated, cleaned review strings
   - `sentiment_results`: list of dicts with "sentiment" and "score" per review

2. Call `summarization_agent` with:
   - `reviews`: the cleaned_reviews from step 1
   - `sentiment_results`: the sentiment_results from step 1
   It will return:
   - `trust_score_result`: trust score and breakdown
   - `summary`: overall_summary, pros, cons, who_is_this_for

3. Return the final combined result as a single dict:
   {
     "sentiment_results": <from step 1>,
     "trust_score_result": <from step 2>,
     "summary": <from step 2>
   }

Do not skip any step. Do not invent or modify data between steps.
""",
    tools=[
        AgentTool(agent=sentiment_agent),
        AgentTool(agent=summarization_agent),
    ],
)
