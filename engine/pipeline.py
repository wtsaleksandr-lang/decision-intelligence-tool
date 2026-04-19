"""
Decision Intelligence Engine — Main Pipeline.
Orchestrates: input → anonymize → blind judge (parallel) → aggregate → verdict.
"""

import asyncio
import os
import time
import uuid

from engine.types import DecisionInput, DecisionResult, RankedOption
from engine.verdict import compute_confidence, build_recommendation
from judges.rubric import build_dimensions
from judges.blind_judge import anonymize_options, run_judge, JUDGE_MODELS
from judges.aggregator import aggregate_decision_results
from tracking.cost_tracking import CostTracker, get_cost_profile
from tracking.history import save_decision


async def run_decision_pipeline(
    input_data: DecisionInput,
    on_step: callable = None,
) -> DecisionResult:
    """Run the full decision evaluation pipeline.

    Steps:
    1. Build dimensions from user criteria
    2. Anonymize and shuffle options
    3. Run 3 AI judges in parallel (blind)
    4. Aggregate scores
    5. Compute confidence
    6. Build result

    on_step: optional callback(step_name, detail) for SSE progress
    """
    run_id = str(uuid.uuid4())[:8]
    pipeline_start = time.time()
    cost_tracker = CostTracker()

    def emit(step: str, detail: str = ""):
        if on_step:
            on_step(step, detail)

    # Step 1: Build scoring dimensions
    emit("dimensions", "Building evaluation criteria...")
    dimensions = build_dimensions(input_data.criteria)

    # Step 2: Anonymize options
    emit("anonymize", "Shuffling options to prevent bias...")
    anonymized, key_map = anonymize_options(input_data.options)

    # Step 3: Run judges in parallel
    emit("judging", "Running independent AI judges...")
    cost_profile = get_cost_profile()

    judge_tasks = []
    judge_names = []
    for judge_name, config in JUDGE_MODELS.items():
        api_key = os.environ.get(config["env_key"])
        if not api_key:
            continue
        model_override = cost_profile.get(judge_name)
        judge_tasks.append(
            run_judge(
                judge_name=judge_name,
                api_key=api_key,
                question=input_data.question,
                anonymized_options=anonymized,
                dimensions=dimensions,
                timeout=300,
                model_override=model_override,
            )
        )
        judge_names.append(judge_name)

    if not judge_tasks:
        raise RuntimeError("No AI judges available. Check API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY).")

    emit("judging", f"Waiting for {len(judge_tasks)} judges...")
    judge_results = await asyncio.gather(*judge_tasks, return_exceptions=True)

    # Process results (convert exceptions to error dicts)
    processed_results = []
    for i, result in enumerate(judge_results):
        if isinstance(result, Exception):
            processed_results.append({"error": str(result)[:200], "judge": judge_names[i]})
        else:
            processed_results.append(result)
            # Track cost (estimate)
            model = cost_profile.get(judge_names[i], JUDGE_MODELS[judge_names[i]]["model"])
            cost_tracker.record(
                judge=judge_names[i],
                model=model,
                input_chars=len(str(anonymized)) + 2000,  # rough estimate
                output_chars=len(str(result)),
            )

    # Step 4: Aggregate
    emit("aggregating", "Aggregating judge scores...")
    aggregated = aggregate_decision_results(
        question=input_data.question,
        judge_results=processed_results,
        key_map=key_map,
        dimensions=dimensions,
    )

    # Step 5: Build ranked options
    ranked_options = []
    for option_text, data in aggregated["options"].items():
        ranked_options.append(RankedOption(
            option=option_text,
            rank=0,
            final_score=data["avg_scores"].get("overall", 0),
            dimension_scores=data["avg_scores"],
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            rank_points=data.get("rank_points", 0),
        ))

    # Sort by score, tiebreak by rank_points
    ranked_options.sort(key=lambda o: (o.final_score, o.rank_points), reverse=True)
    for i, opt in enumerate(ranked_options):
        opt.rank = i + 1

    # Step 6: Confidence
    emit("verdict", "Computing confidence and recommendation...")
    confidence_score, confidence_level = compute_confidence(
        judge_count=aggregated["judge_count"],
        judges_agree=aggregated["judges_agree"],
        ranked_options=ranked_options,
    )

    why_winner_won = build_recommendation(aggregated, ranked_options)
    latency_ms = int((time.time() - pipeline_start) * 1000)

    result = DecisionResult(
        question=input_data.question,
        ranked_options=ranked_options,
        winner=aggregated["winner"],
        why_winner_won=why_winner_won,
        judges_agree=aggregated["judges_agree"],
        judge_count=aggregated["judge_count"],
        confidence_level=confidence_level,
        confidence_score=confidence_score,
        total_cost_usd=cost_tracker.total(),
        latency_ms=latency_ms,
        run_id=run_id,
    )

    # Save to history
    emit("saving", "Saving results...")
    save_decision({
        "run_id": run_id,
        "question": input_data.question,
        "options": input_data.options,
        "criteria": input_data.criteria,
        "winner": result.winner,
        "confidence": confidence_level,
        "confidence_score": confidence_score,
        "judges_agree": result.judges_agree,
        "judge_count": result.judge_count,
        "latency_ms": latency_ms,
        "cost_usd": cost_tracker.total(),
        "ranked_options": [
            {
                "option": o.option,
                "rank": o.rank,
                "score": o.final_score,
                "strengths": o.strengths,
                "weaknesses": o.weaknesses,
            }
            for o in ranked_options
        ],
    })

    emit("done", "Analysis complete.")
    return result
