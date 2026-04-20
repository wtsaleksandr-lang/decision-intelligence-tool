#!/usr/bin/env python3
"""
Run the comprehensive product research through the AI Orchestrator pipeline.
Captures the full output (strategist synthesis + decision maker final) and saves it.
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Point to the orchestrator repo
ORCHESTRATOR_DIR = Path(r"C:\Users\Owner\.codex\ai-orchestrator")
sys.path.insert(0, str(ORCHESTRATOR_DIR))
os.chdir(str(ORCHESTRATOR_DIR))

from dotenv import load_dotenv
load_dotenv(ORCHESTRATOR_DIR / ".env")

from orchestrator.pipeline import run_pipeline
import uuid

PROMPT = """Conduct a comprehensive product research and strategic analysis for a Decision Intelligence Tool called "DecideIQ" that I am building and preparing to launch.

## WHAT WE BUILT

DecideIQ is an AI-powered decision comparison tool. Users describe a decision in natural language ("Should I buy Tesla Model 3 or Mach-E?"), and the system:

1. Extracts structured options and criteria from natural language input (GPT-4o-mini)
2. Validates the extraction quality before committing to expensive judge calls
3. Anonymizes and shuffles options to prevent position bias
4. Runs 3 independent AI analysts in parallel (GPT-4o/mini, Claude Sonnet/Haiku, Gemini Flash) — each with a different analytical perspective: General Analyst, Risk Skeptic, Pragmatist
5. Aggregates scores using rank-point consensus with judge agreement detection
6. Synthesizes a coherent recommendation from all judge outputs (separate AI call)
7. Computes confidence based on score spread, judge agreement, and judge count

Tech stack: Python + FastAPI backend, Jinja2 server-rendered frontend (dark theme, Fin.ai-inspired design), 6 LLM provider adapters.

Current benchmark: 7.3/10 overall quality across 20 test decisions. Strongest: Decisiveness (8.3), Winner Accuracy (7.7). Weakest: Confidence Calibration (6.5). Cost: $0.002/decision standard, $0.05 deep.

## WHO WILL USE THIS

Primary: Me (founder) for my SaaS and freight forwarding business decisions. Also: business professionals comparing vendors/strategies/tools, consumers comparing products, freelancers making client recommendations.

My specific use cases: freight forwarding carrier comparison, SaaS tool selection, pricing strategy, hiring decisions, daily operational decisions.

## RESEARCH NEEDED

### 1. Competition Analysis
Research ALL direct and indirect competitors in "AI decision-making" and "option comparison" space. What tools exist? How do they position? Pricing? Tech approach (single vs multi-model)? Strongest features to replicate? Weakest points to exploit? Revenue/traction estimates? User acquisition channels?

Include: Decidedly.ai, AHP tools, decision matrix tools, AI comparison assistants, any ProductHunt launches in this space, and general AI assistants used for decisions (ChatGPT, Claude, Perplexity).

### 2. Product Improvements
What features are we missing vs competitors? What unique features could differentiate us? How to get from 7.3 to 8.5+ quality? What admin dashboard features for a founder? Decision templates for specific industries? Follow-up chat? "What if" scenarios? Historical decision tracking with outcomes?

### 3. UI/UX and Launch
Is single-page tool-first the right approach? Best onboarding flow? Most effective trust signals? Minimum viable launch checklist? Domain recommendations? Where to launch first (ProductHunt, HN, Twitter, Reddit, niche communities)?

### 4. Monetization
Right pricing model? Free tier limits? Pro tier features? Viral sharing from results? SEO strategy for programmatic pages? Moat against ChatGPT doing this directly? Realistic revenue milestones ($1k, $10k, $100k/mo)?

### 5. Execution Roadmap
Prioritized actions: this week, this month, month 2-3, month 4-6. Be specific — tool names, exact features, pricing numbers, marketing channels, content strategies. No generic advice."""

CATEGORY = "deep_research"
MODE = "expert"


async def main():
    run_id = str(uuid.uuid4())[:8]
    queue = asyncio.Queue()
    model_tasks = {}

    # Use expert-tier models for research
    models = ["gpt-4o", "claude-sonnet-4-6", "gemini-2.5-flash", "deepseek-chat", "grok-3"]

    admin_overrides = {
        "force_tier": "expert",
        "force_web_search": True,
        "debug_mode": False,
        "max_output_length": 10000,
    }

    print("=" * 70)
    print("DECISION INTELLIGENCE TOOL — COMPREHENSIVE RESEARCH")
    print(f"Run ID: {run_id}")
    print(f"Mode: {MODE} | Category: {CATEGORY}")
    print(f"Models: {', '.join(models)}")
    print(f"Web search: ON")
    print("=" * 70)

    # Collect events
    strategist_outputs = []
    decision_output = None
    phase_count = 0

    start = time.time()

    # Run pipeline in background
    pipeline_task = asyncio.create_task(
        run_pipeline(
            run_id=run_id,
            category=CATEGORY,
            prompt=PROMPT,
            models=models,
            queue=queue,
            model_tasks=model_tasks,
            mode=MODE,
            quick_mode=False,
            admin_overrides=admin_overrides,
        )
    )

    # Consume events
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=600)
        except asyncio.TimeoutError:
            print("  [TIMEOUT] No events for 600s, stopping")
            break

        event = item.get("event", "")
        data = item.get("data", {})

        if event == "step":
            step = data.get("step", "")
            status = data.get("status", "")
            print(f"  [{step}] {status}")

        elif event == "phases_info":
            phase_count = data.get("total", 1)
            names = data.get("names", [])
            print(f"  [phases] {phase_count} phases: {names}")

        elif event == "model_result":
            model = data.get("model", "?")
            status = data.get("status", "?")
            phase = data.get("phase", "?")
            latency = data.get("latency_ms", 0)
            resp = data.get("response", "")
            chars = len(resp) if resp else 0
            print(f"  [research] phase={phase} model={model} status={status} {chars}chars {latency}ms")

        elif event == "strategist":
            result = data.get("result", "")
            phase = data.get("phase", "?")
            strategist_outputs.append({"phase": phase, "output": result})
            print(f"  [strategist] phase={phase} {len(result)}chars")

        elif event == "decision":
            decision_output = data.get("result", "")
            print(f"  [decision] {len(decision_output)}chars")

        elif event == "done":
            print(f"  [done] Pipeline complete")
            break

        elif event == "error":
            msg = data.get("message", str(data))
            print(f"  [ERROR] {msg[:200]}")
            break

    elapsed = time.time() - start
    await pipeline_task

    print(f"\nCompleted in {elapsed:.0f}s")
    print(f"Phases: {phase_count}")
    print(f"Strategist outputs: {len(strategist_outputs)}")
    print(f"Decision output: {len(decision_output) if decision_output else 0} chars")

    # Save results
    output_dir = Path(r"C:\Users\Owner\.codex\decision-intelligence-tool\research")
    output_dir.mkdir(exist_ok=True)

    # Save strategist outputs (per-phase synthesis)
    for i, s in enumerate(strategist_outputs):
        path = output_dir / f"strategist_phase_{s['phase']}.md"
        path.write_text(s["output"], encoding="utf-8")
        print(f"  Saved: {path}")

    # Save final decision output
    if decision_output:
        path = output_dir / "final_research_report.md"
        path.write_text(decision_output, encoding="utf-8")
        print(f"  Saved: {path}")

    # Save JSON for reference
    json_path = output_dir / "research_raw.json"
    json_path.write_text(json.dumps({
        "run_id": run_id,
        "elapsed_s": elapsed,
        "phases": phase_count,
        "strategist_outputs": strategist_outputs,
        "decision_output": decision_output,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved: {json_path}")


if __name__ == "__main__":
    asyncio.run(main())
