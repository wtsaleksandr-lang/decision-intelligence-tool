"""
Verdict logic — computes confidence and generates recommendation summary.
"""

from engine.types import DecisionResult, RankedOption


def compute_confidence(
    judge_count: int,
    judges_agree: bool,
    ranked_options: list[RankedOption],
) -> tuple[float, str]:
    """Compute confidence score (0-100) and level (high/moderate/low).

    Based on:
    - Number of judges that responded
    - Whether judges agree on the winner
    - Score spread between #1 and #2
    """
    score = 50.0  # baseline

    # Judge count factor
    if judge_count >= 3:
        score += 15
    elif judge_count == 2:
        score += 5
    elif judge_count <= 1:
        score -= 15

    # Judge agreement
    if judges_agree:
        score += 20
    else:
        score -= 10

    # Score spread between #1 and #2
    if len(ranked_options) >= 2:
        spread = ranked_options[0].final_score - ranked_options[1].final_score
        if spread >= 1.5:
            score += 15  # clear winner
        elif spread >= 0.5:
            score += 5   # moderate gap
        else:
            score -= 10  # very tight race

    score = max(10, min(95, score))

    if score >= 70:
        level = "high"
    elif score >= 45:
        level = "moderate"
    else:
        level = "low"

    return score, level


def build_recommendation(result: dict, ranked_options: list[RankedOption]) -> str:
    """Build a human-readable recommendation from aggregated results."""
    explanations = result.get("explanations", [])

    if explanations:
        # Use the first judge's explanation as primary
        return explanations[0]

    # Fallback
    if ranked_options:
        winner = ranked_options[0]
        if len(ranked_options) >= 2:
            runner = ranked_options[1]
            return (
                f"{winner.option} is the recommended choice with a score of "
                f"{winner.final_score:.1f}/10, ahead of {runner.option} at "
                f"{runner.final_score:.1f}/10."
            )
        return f"{winner.option} is the recommended choice with a score of {winner.final_score:.1f}/10."

    return "Unable to determine a clear recommendation."
