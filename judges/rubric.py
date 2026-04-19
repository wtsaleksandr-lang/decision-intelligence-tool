"""
Scoring rubric for decision evaluation.
Builds dynamic rubrics from user-defined criteria + built-in dimensions.
Ported from ai-orchestrator evaluation/rubric.py — adapted for option comparison.
"""

# Built-in dimensions always scored (the baseline)
BUILT_IN_DIMENSIONS = [
    {
        "name": "practicality",
        "label": "Practicality",
        "description": "How practical and feasible is this option to execute? Consider effort, resources, and complexity.",
        "scale": "1-10 (1=impractical, 10=easy to execute immediately)",
    },
    {
        "name": "risk_level",
        "label": "Risk Level",
        "description": "How risky is this option? Consider downsides, deal-breakers, and what could go wrong.",
        "scale": "1-10 (1=extremely risky, 10=very safe/low risk)",
    },
    {
        "name": "roi_potential",
        "label": "ROI / Upside Potential",
        "description": "How much value or return could this option generate? Consider long-term and short-term upside.",
        "scale": "1-10 (1=no real upside, 10=massive potential return)",
    },
    {
        "name": "overall_fit",
        "label": "Overall Fit",
        "description": "Considering everything, how well does this option fit the stated question and priorities?",
        "scale": "1-10 (1=poor fit, 10=perfect match)",
    },
]


def build_dimensions(user_criteria: list[dict]) -> list[dict]:
    """Build the full dimensions list from user criteria + built-in dimensions.

    user_criteria: [{"name": "Cost", "weight": 8}, {"name": "Speed", "weight": 6}, ...]
    """
    dims = []

    # User criteria become dimensions
    for c in user_criteria:
        dims.append({
            "name": c["name"].lower().replace(" ", "_"),
            "label": c["name"],
            "description": f"How well does this option perform on '{c['name']}'? Score based on the user's priorities.",
            "scale": "1-10 (1=very poor, 10=excellent)",
            "weight": c.get("weight", 5),
        })

    # Add built-in dimensions
    for dim in BUILT_IN_DIMENSIONS:
        dims.append({**dim, "weight": 5})  # built-in gets neutral weight

    return dims


JUDGE_SYSTEM_PROMPT = """You are a sharp decision analyst. Evaluate options blindly and decisively.

Options are labeled Option A, Option B, etc. They were randomly shuffled — do NOT assume ordering.

Score each option on these dimensions:

{dimensions}

SCORING RULES:
- Use the FULL 1-10 range. Most options should score 4-8. Reserve 9-10 for genuinely excellent. Use 1-3 for genuinely poor.
- Do NOT compress scores into 6-8 range. Differentiate clearly.
- Judge substance, not wording. Specific beats vague.
- High risk + high reward is NOT automatically better than moderate + safe.
- If two options are close, still pick a winner. Do not hedge.

OUTPUT RULES:
- Strength: ONE sentence, max 20 words. The single biggest advantage.
- Weakness: ONE sentence, max 20 words. The single biggest concern.
- Explanation: 2 sentences max. Be direct. Say why #1 wins and what #2 lacks.
- No filler, no caveats, no "it depends" hedging.

JSON format:
{{
  "evaluations": {{
    "Option A": {{
      {dim_keys}
      "strength": "<1 sentence, max 20 words>",
      "weakness": "<1 sentence, max 20 words>"
    }}
  }},
  "ranking": ["Option X", "Option Y", ...],
  "explanation": "<2 sentences. Direct. No hedging.>"
}}"""


def build_judge_system(dimensions: list[dict]) -> str:
    """Build the system prompt for judge models."""
    dim_text = "\n".join(
        f"- {d['label']}: {d['description']} ({d['scale']})"
        for d in dimensions
    )
    dim_keys = "\n      ".join(f'"{d["name"]}": "<int>",' for d in dimensions)
    return JUDGE_SYSTEM_PROMPT.format(dimensions=dim_text, dim_keys=dim_keys)


def build_judge_prompt(question: str, anonymized_options: dict[str, str]) -> str:
    """Build the user prompt for judge models.

    anonymized_options: {"Option A": "description...", "Option B": "description...", ...}
    """
    parts = [f"## Decision Question\n{question}\n"]
    for label, description in anonymized_options.items():
        parts.append(f"## {label}\n{description}\n")
    parts.append("\nEvaluate all options using the rubric. Respond in JSON only.")
    return "\n".join(parts)
