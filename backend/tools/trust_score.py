import statistics
from google.adk.tools import FunctionTool


def calculate_trust_score(sentiment_results: list[dict]) -> dict:
    """Calculates a trust score (0-100) from a list of sentiment analysis results.

    Scoring breakdown:
        - 70 pts  : sentiment ratio (proportion of positive reviews)
        - 20 pts  : consistency    (low score variance = trustworthy)
        - -10 pts : outlier penalty (reviews flagged as statistical outliers)
    """
    if not sentiment_results:
        return {
            "trust_score": 0,
            "breakdown": {
                "sentiment_component": 0.0,
                "consistency_component": 0.0,
                "outlier_penalty": 0.0,
            },
        }

    scores = [r.get("score", 0.0) for r in sentiment_results]
    sentiments = [r.get("sentiment", "neutral") for r in sentiment_results]
    total = len(sentiment_results)

    # --- 70 pts: sentiment ratio ---
    positive_count = sum(1 for s in sentiments if s == "positive")
    sentiment_component = (positive_count / total) * 70.0

    # --- 20 pts: consistency (low variance = high score) ---
    # Scores are in [0, 1]; max possible variance for that range is 0.25 
    if total > 1:
        variance = statistics.variance(scores)
        consistency_normalized = max(0.0, 1.0 - (variance / 0.25))
    else:
        consistency_normalized = 1.0
    consistency_component = consistency_normalized * 20.0

    # --- up to -10 pts: outlier penalty ---
    # Outliers defined as reviews whose score is >2 std deviations from the mean
    if total > 2:
        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores)
        if stdev > 0:
            outlier_count = sum(1 for s in scores if abs((s - mean) / stdev) > 2)
        else:
            outlier_count = 0
        outlier_ratio = outlier_count / total
    else:
        outlier_ratio = 0.0
    outlier_penalty = outlier_ratio * 10.0

    trust_score = sentiment_component + consistency_component - outlier_penalty
    trust_score = round(max(0.0, min(100.0, trust_score)), 2)

    return {
        "trust_score": trust_score,
        "breakdown": {
            "sentiment_component": round(sentiment_component, 2),
            "consistency_component": round(consistency_component, 2),
            "outlier_penalty": round(outlier_penalty, 2),
        },
    }


calculate_trust_score_tool = FunctionTool(func=calculate_trust_score)
