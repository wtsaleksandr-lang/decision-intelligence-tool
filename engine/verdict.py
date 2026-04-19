"""
Verdict logic — computes confidence and generates recommendation summary.
Polished for realistic confidence and concise output.
"""

from engine.types import DecisionResult, RankedOption


def compute_confidence(
    judge_count: int,
    judges_agree: bool,
    ranked_options: list[RankedOption],
) -> tuple[float, str]:
    """Compute confidence score (0-100) and level.

    Factors weighted by reliability signal strength:
    - Judge count (most critical — more judges = more robust)
    - Judge agreement (strong signal — unanimous vs split)
    - Score spread (moderate signal — clear gap vs tight race)
    - Number of options (minor — more options = harder to be sure)
    """
    score = 40.0  # conservative baseline

    # Judge count (0-25 points)
    if judge_count >= 3:
        score += 25
    elif judge_count == 2:
        score += 12
    elif judge_count == 1:
        score += 0  # single judge = minimal confidence

    # Agreement (0-20 points)
    if judges_agree and judge_count >= 2:
        score += 20
    elif judges_agree and judge_count == 1:
        score += 5  # single judge "agreeing with itself" means nothing
    else:
        score -= 5

    # Score spread between #1 and #2 (0-15 points)
    if len(ranked_options) >= 2:
        spread = ranked_options[0].final_score - ranked_options[1].final_score
        if spread >= 2.0:
            score += 15   # dominant winner
        elif spread >= 1.0:
            score += 10   # clear gap
        elif spread >= 0.3:
            score += 3    # slight edge
        else:
            score -= 5    # essentially a tie

    # Option count penalty (more options = more uncertainty)
    n_options = len(ranked_options)
    if n_options >= 6:
        score -= 5
    elif n_options >= 4:
        score -= 2

    score = max(15, min(92, score))

    if score >= 70:
        level = "high"
    elif score >= 45:
        level = "moderate"
    else:
        level = "low"

    return round(score), level


def build_recommendation(result: dict, ranked_options: list[RankedOption]) -> str:
    """Build a concise, decisive recommendation.

    Prefers judge explanations but cleans them up.
    Falls back to a structured summary.
    """
    explanations = result.get("explanations", [])

    if explanations and ranked_options:
        winner_name = ranked_options[0].option.lower()
        # Find an explanation that actually mentions the winner
        matching = [e for e in explanations if winner_name in e.lower() or ranked_options[0].option in e]
        best = matching[0] if matching else explanations[0]
        # Trim to 2-3 sentences max
        sentences = [s.strip() for s in best.replace('\n', ' ').split('.') if s.strip()]
        if len(sentences) > 3:
            sentences = sentences[:3]
        return '. '.join(sentences) + '.'

    # Structured fallback
    if not ranked_options:
        return "Unable to determine a clear recommendation."

    winner = ranked_options[0]
    parts = [f"{winner.option} is the strongest choice"]

    if winner.strengths:
        parts.append(f"primarily for its {winner.strengths[0].lower().rstrip('.')}")

    if len(ranked_options) >= 2:
        runner = ranked_options[1]
        spread = winner.final_score - runner.final_score
        if spread < 0.5:
            parts.append(f"though {runner.option} is a close alternative")
        else:
            parts.append(f"scoring {spread:.1f} points above {runner.option}")

    return '. '.join(parts) + '.'
