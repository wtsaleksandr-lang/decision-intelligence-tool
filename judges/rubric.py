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


JUDGE_SYSTEM_PROMPT = """You are an expert decision analyst performing a blind comparison of options.

You will be given a decision question and multiple options labeled Option A, Option B, Option C, etc.
The options have been randomly shuffled. Do NOT assume any ordering.

Your job is to evaluate each option on these dimensions:

{dimensions}

For each option, provide:
1. A score (1-10) for each dimension
2. A brief strength (1 sentence)
3. A brief weakness (1 sentence)

Then provide:
4. Your overall ranking from best to worst
5. A brief explanation of why #1 is the best choice (2-3 sentences)

IMPORTANT RULES:
- Be honest and critical. Not everything deserves a high score.
- Judge the SUBSTANCE of each option, not how it's worded.
- If an option is vague or lacks specifics, score it low on practicality and overall_fit.
- A shorter, specific option can beat a longer, vague one.
- Consider trade-offs: high reward with high risk is not automatically better than moderate reward with low risk.

Respond in this exact JSON format:
{{
  "evaluations": {{
    "Option A": {{
      {dim_keys}
      "strength": "<1 sentence>",
      "weakness": "<1 sentence>"
    }},
    ...for each option
  }},
  "ranking": ["Option X", "Option Y", ...],
  "explanation": "<2-3 sentences explaining why #1 is best>"
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
