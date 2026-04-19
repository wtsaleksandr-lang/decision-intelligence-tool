"""
Smoke test — runs 3 real decisions end-to-end through the pipeline.
"""

import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from config import settings
from engine.types import DecisionInput
from engine.pipeline import run_decision_pipeline

TEST_DECISIONS = [
    {
        "name": "Business: Best marketing strategy",
        "question": "Which marketing strategy should a small SaaS company pursue this quarter?",
        "options": [
            "Content marketing and SEO blog posts",
            "Paid ads on Google and Facebook",
            "Cold email outreach to prospects",
        ],
        "criteria": [
            {"name": "Cost", "weight": 8},
            {"name": "Speed to results", "weight": 7},
            {"name": "Long-term value", "weight": 6},
        ],
    },
    {
        "name": "Consumer: Best laptop choice",
        "question": "Which laptop should I buy for remote software development under $1500?",
        "options": [
            "MacBook Air M3 15-inch",
            "ThinkPad X1 Carbon Gen 12",
            "Framework Laptop 16",
            "Dell XPS 15",
        ],
        "criteria": [
            {"name": "Performance", "weight": 9},
            {"name": "Build quality", "weight": 7},
            {"name": "Value for money", "weight": 8},
        ],
    },
    {
        "name": "Personal: Best training plan",
        "question": "Which training plan is best for a beginner who wants to lose weight and build muscle?",
        "options": [
            "3-day full body lifting program",
            "5-day push/pull/legs split",
            "Daily 30-minute HIIT sessions",
        ],
        "criteria": [
            {"name": "Effectiveness", "weight": 9},
            {"name": "Time commitment", "weight": 7},
            {"name": "Sustainability", "weight": 8},
        ],
    },
]


async def run_smoke_tests():
    print("=" * 60)
    print("DECISION INTELLIGENCE TOOL — SMOKE TEST")
    print("=" * 60)

    # Check API keys
    judges = settings.available_judges()
    print(f"\nAvailable judges: {judges}")
    if not settings.has_any_api_key():
        print("ERROR: No API keys configured. Cannot run tests.")
        return False

    all_passed = True
    results = []

    for i, test in enumerate(TEST_DECISIONS, 1):
        print(f"\n{'-' * 60}")
        print(f"TEST {i}/3: {test['name']}")
        print(f"Question: {test['question']}")
        print(f"Options: {len(test['options'])}, Criteria: {len(test['criteria'])}")

        input_data = DecisionInput(
            question=test["question"],
            options=test["options"],
            criteria=test["criteria"],
        )

        steps = []

        def on_step(step, detail):
            steps.append(step)
            print(f"  [{step}] {detail}")

        start = time.time()
        try:
            result = await run_decision_pipeline(input_data, on_step=on_step)
            elapsed = time.time() - start

            print(f"\n  RESULT:")
            print(f"  Winner: {result.winner}")
            print(f"  Why: {result.why_winner_won[:120]}...")
            print(f"  Confidence: {result.confidence_level} ({result.confidence_score:.0f}/100)")
            print(f"  Judges agree: {result.judges_agree} ({result.judge_count} judges)")
            print(f"  Latency: {elapsed:.1f}s")
            print(f"  Est. cost: ${result.total_cost_usd:.4f}")

            print(f"\n  Ranked options:")
            for opt in result.ranked_options:
                print(f"    #{opt.rank} {opt.option} — {opt.final_score:.1f}/10")
                if opt.strengths:
                    print(f"       + {opt.strengths[0]}")
                if opt.weaknesses:
                    print(f"       - {opt.weaknesses[0]}")

            # Validate result
            checks = []
            checks.append(("has_winner", bool(result.winner)))
            checks.append(("has_ranked_options", len(result.ranked_options) >= 2))
            checks.append(("scores_reasonable", all(0 <= o.final_score <= 10 for o in result.ranked_options)))
            checks.append(("winner_is_rank_1", result.ranked_options[0].option == result.winner))
            checks.append(("confidence_valid", 10 <= result.confidence_score <= 95))
            checks.append(("judge_count_positive", result.judge_count >= 1))
            checks.append(("has_explanation", len(result.why_winner_won) > 10))
            checks.append(("pipeline_steps_ran", len(steps) >= 4))

            passed = all(v for _, v in checks)
            for name, ok in checks:
                status = "PASS" if ok else "FAIL"
                print(f"  [{status}] {name}")

            if not passed:
                all_passed = False

            results.append({"test": test["name"], "passed": passed, "winner": result.winner, "time": elapsed})

        except Exception as e:
            elapsed = time.time() - start
            print(f"  ERROR: {e}")
            all_passed = False
            results.append({"test": test["name"], "passed": False, "error": str(e), "time": elapsed})

    # Summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['test']} ({r.get('time', 0):.1f}s) — winner: {r.get('winner', 'N/A')}")

    total_passed = sum(1 for r in results if r["passed"])
    print(f"\n  {total_passed}/{len(results)} tests passed")

    # Check history file
    from pathlib import Path
    history_file = Path("history/decisions.jsonl")
    if history_file.exists():
        lines = history_file.read_text().strip().split("\n")
        print(f"  History: {len(lines)} decisions logged")
    else:
        print("  History: NOT created (potential bug)")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(run_smoke_tests())
    sys.exit(0 if success else 1)
