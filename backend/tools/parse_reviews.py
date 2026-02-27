from google.adk.tools import FunctionTool

def parse_reviews(reviews: list[str]) -> list[str]:
    cleaned_reviews = []
    seen = set()
    for review in reviews:
        cleaned_review = review.strip()
        if not cleaned_review:
            continue
        if len(cleaned_review) < 10:
            continue
        normalized = cleaned_review.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        cleaned_reviews.append(cleaned_review)
    return cleaned_reviews

parse_reviews_tool = FunctionTool(func=parse_reviews)