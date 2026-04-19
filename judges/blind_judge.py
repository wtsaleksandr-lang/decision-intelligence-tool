"""
Blind judging pipeline for decision options.
Anonymizes and shuffles options, sends to multiple AI judges, collects scores.
Ported from ai-orchestrator evaluation/judges/blind_judge.py — adapted for user options.
"""

import json
import random
import re

import httpx

from judges.rubric import build_judge_system, build_judge_prompt
from providers.base import make_httpx_timeout


def anonymize_options(options: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    """Anonymize and shuffle user options to prevent position bias.

    Args:
        options: list of option descriptions

    Returns:
        (anonymized, key_map)
        anonymized: {"Option A": "description...", "Option B": "...", ...}
        key_map: {"Option A": "original option text", ...}
    """
    labels = [chr(65 + i) for i in range(len(options))]  # A, B, C, D...

    # Shuffle to prevent position bias
    indices = list(range(len(options)))
    random.shuffle(indices)

    anonymized = {}
    key_map = {}
    for label, idx in zip(labels, indices):
        opt_label = f"Option {label}"
        anonymized[opt_label] = options[idx]
        key_map[opt_label] = options[idx]

    return anonymized, key_map


# Judge model configs — same pattern as ai-orchestrator
JUDGE_MODELS = {
    "judge_openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o",
        "env_keys": ["OPENAI_API_KEY", "GPT_API_KEY"],
        "header_fn": lambda key: {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        "body_fn": lambda model, system, prompt: {
            "model": model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "max_tokens": 4096, "temperature": 0.3,
            "response_format": {"type": "json_object"},
        },
        "extract_fn": lambda data: data["choices"][0]["message"]["content"],
    },
    "judge_anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "model": "claude-sonnet-4-6",
        "env_keys": ["ANTHROPIC_API_KEY", "CLAUDE_API_KEY"],
        "header_fn": lambda key: {
            "x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json",
        },
        "body_fn": lambda model, system, prompt: {
            "model": model, "max_tokens": 4096,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        },
        "extract_fn": lambda data: data["content"][0]["text"],
    },
    "judge_google": {
        "url_fn": lambda model, key: (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent?key={key}"
        ),
        "model": "gemini-2.5-flash",
        "env_keys": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
        "header_fn": lambda key: {"Content-Type": "application/json"},
        "body_fn": lambda model, system, prompt: {
            "contents": [{"role": "user", "parts": [{"text": system + "\n\n" + prompt}]}],
            "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.3},
        },
        "extract_fn": lambda data: data["candidates"][0]["content"]["parts"][0]["text"],
    },
}


async def run_judge(
    judge_name: str,
    api_key: str,
    question: str,
    anonymized_options: dict[str, str],
    dimensions: list[dict],
    timeout: int = 300,
    model_override: str | None = None,
) -> dict:
    """Run a single judge evaluation on decision options.

    Returns parsed JSON scores or error dict.
    """
    config = JUDGE_MODELS.get(judge_name)
    if not config:
        return {"error": f"Unknown judge: {judge_name}"}

    system = build_judge_system(dimensions)
    user_prompt = build_judge_prompt(question, anonymized_options)
    model = model_override or config["model"]

    if "url_fn" in config:
        url = config["url_fn"](model, api_key)
    else:
        url = config["url"]

    headers = config["header_fn"](api_key)
    body = config["body_fn"](model, system, user_prompt)
    ht = make_httpx_timeout(timeout)

    try:
        async with httpx.AsyncClient(timeout=ht) as client:
            resp = await client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()
            raw_text = config["extract_fn"](data)

            # Parse JSON from response (may be wrapped in markdown)
            json_match = re.search(r'\{[\s\S]*\}', raw_text)
            if json_match:
                return json.loads(json_match.group())
            return {"error": "Judge returned no valid JSON", "raw": raw_text[:500]}

    except Exception as e:
        return {"error": str(e)[:200], "judge": judge_name}
