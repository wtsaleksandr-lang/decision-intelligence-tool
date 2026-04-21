#!/usr/bin/env python3
"""
Run a business decision through the Decision Intelligence Tool.
Uses DEEP mode = 3 flagship models (GPT-4o, Claude Sonnet, Gemini Flash).
"""

import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from engine.types import DecisionInput, AnalysisSettings
from engine.pipeline import run_decision_pipeline


QUESTION = """What is the BEST product/business structure for my two AI products (AI Orchestrator Tool — superior research/synthesis; and Decision Intelligence Tool — options comparison/ranking)? Context: solo founder, need paid conversions, differentiation from ChatGPT/Claude, SEO growth, 3-year scalability, and defensibility against big AI companies."""

OPTIONS = [
    "Two fully separate websites + two separate brands/products (maximum brand clarity)",
    "One single website + one unified tool combining both systems (simplest funnel)",
    "One single website + two separate tools inside same ecosystem (shared brand, separate funnels/modes)",
    "One master tool with smart intent detection (auto-routes prompts to Research / Decision / Hybrid mode)",
    "Freemium entry tool + upsell ecosystem (one simple public tool feeds users to premium specialized tools)",
]

CRITERIA = [
    {"name": "Paid conversion potential", "weight": 10},
    {"name": "User clarity / simplicity", "weight": 9},
    {"name": "Impress users quickly", "weight": 8},
    {"name": "Differentiation vs ChatGPT / Claude / Gemini", "weight": 10},
    {"name": "SEO growth potential", "weight": 9},
    {"name": "AI-generated content / SEO automation compatibility", "weight": 7},
    {"name": "Retention / repeat usage", "weight": 9},
    {"name": "Virality / word of mouth", "weight": 7},
    {"name": "3-year scalability", "weight": 9},
    {"name": "Brand authority / premium perception", "weight": 8},
    {"name": "Ease of execution for solo founder", "weight": 10},
    {"name": "Long-term defensibility vs big AI companies", "weight": 10},
]


async def main():
    # Use DEEP mode: 3 flagship models (gpt-4o, claude-sonnet-4-6, gemini-2.5-flash)
    # Risk-focused: brutally honest, finds weaknesses
    # Detailed: thorough strength/weakness analysis
    input_data = DecisionInput(
        question=QUESTION,
        options=OPTIONS,
        criteria=CRITERIA,
        settings=AnalysisSettings(
            depth="deep",
            focus="risks",
            length="detailed",
            web_search=False,
        ),
    )

    print("=" * 70)
    print("DECISION INTELLIGENCE TOOL — BUSINESS STRUCTURE ANALYSIS")
    print("Mode: DEEP (3 flagship models: GPT-4o + Claude Sonnet + Gemini)")
    print("Focus: Risk-focused")
    print("Length: Detailed")
    print("=" * 70)
    print()

    def on_step(step, detail):
        print(f"  [{step}] {detail}")

    result = await run_decision_pipeline(input_data, on_step=on_step)

    print()
    print("=" * 70)
    print("RESULT")
    print("=" * 70)
    print(f"\nWINNER: {result.winner}")
    print(f"\nCONFIDENCE: {result.confidence_level} ({result.confidence_score}/100)")
    print(f"JUDGES: {result.judge_count}, AGREEMENT: {'Unanimous' if result.judges_agree else 'Split'}")
    print(f"\nRECOMMENDATION:")
    print(result.why_winner_won)
    print()
    print("RANKED OPTIONS:")
    for o in result.ranked_options:
        print(f"\n  #{o.rank} — {o.option}")
        print(f"      Final score: {o.final_score:.1f}/10")
        # Show per-criterion scores
        for dim, score in o.dimension_scores.items():
            if dim != "overall":
                label = dim.replace("_", " ").title()
                print(f"      {label}: {score:.1f}")
        if o.strengths:
            print(f"      Strengths:")
            for s in o.strengths:
                print(f"        + {s}")
        if o.weaknesses:
            print(f"      Weaknesses:")
            for w in o.weaknesses:
                print(f"        - {w}")

    print()
    print(f"Latency: {result.latency_ms / 1000:.1f}s")
    print(f"Cost: ${result.total_cost_usd:.4f}")
    print(f"Run ID: {result.run_id}")

    # Save to file
    output_path = Path("research/business_decision_result.md")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Business Structure Decision — Analysis\n\n")
        f.write(f"**Mode:** Deep (3 flagship models) | **Focus:** Risk | **Length:** Detailed\n\n")
        f.write(f"**Judges:** {result.judge_count} | **Agreement:** {'Unanimous' if result.judges_agree else 'Split'}\n\n")
        f.write(f"## Question\n{QUESTION}\n\n")
        f.write(f"## WINNER: {result.winner}\n\n")
        f.write(f"**Confidence:** {result.confidence_level} ({result.confidence_score}/100)\n\n")
        f.write(f"**Recommendation:**\n{result.why_winner_won}\n\n")
        f.write(f"## Ranked Options\n\n")
        for o in result.ranked_options:
            f.write(f"### #{o.rank} — {o.option}\n\n")
            f.write(f"**Final score:** {o.final_score:.1f}/10\n\n")
            f.write(f"**Dimension scores:**\n\n")
            for dim, score in o.dimension_scores.items():
                if dim != "overall":
                    label = dim.replace("_", " ").title()
                    f.write(f"- {label}: {score:.1f}\n")
            if o.strengths:
                f.write(f"\n**Strengths:**\n")
                for s in o.strengths:
                    f.write(f"- {s}\n")
            if o.weaknesses:
                f.write(f"\n**Weaknesses:**\n")
                for w in o.weaknesses:
                    f.write(f"- {w}\n")
            f.write("\n")
        f.write(f"\n---\n")
        f.write(f"Latency: {result.latency_ms / 1000:.1f}s | Cost: ${result.total_cost_usd:.4f} | Run: {result.run_id}\n")

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
