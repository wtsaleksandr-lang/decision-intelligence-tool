"""
Decision Intelligence Tool — FastAPI Backend.
Provides SSE-streaming decision evaluation endpoint.
"""

import asyncio
import json
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from config import settings
from engine.types import DecisionInput
from engine.pipeline import run_decision_pipeline
from tracking.history import get_recent_decisions

app = FastAPI(title="Decision Intelligence Tool", version="0.1.0")


# ─── Request/Response Models ───

class CriterionModel(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    weight: int = Field(ge=1, le=10, default=5)


class DecisionRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    options: list[str] = Field(min_length=2, max_length=10)
    criteria: list[CriterionModel] = Field(min_length=1, max_length=10)


# ─── Health Check ───

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "judges_available": settings.available_judges(),
        "has_api_keys": settings.has_any_api_key(),
    }


# ─── Decision Evaluation (SSE Stream) ───

@app.post("/api/decide")
async def decide(request: DecisionRequest, req: Request):
    """Evaluate a decision. Returns SSE stream with progress + final result."""

    if not settings.has_any_api_key():
        return JSONResponse(
            status_code=503,
            content={"error": "No AI judge API keys configured. Set at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY"},
        )

    input_data = DecisionInput(
        question=request.question,
        options=request.options,
        criteria=[{"name": c.name, "weight": c.weight} for c in request.criteria],
    )

    # Check Accept header for SSE
    accept = req.headers.get("accept", "")
    if "text/event-stream" in accept:
        return StreamingResponse(
            _stream_decision(input_data),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    # JSON fallback
    try:
        result = await run_decision_pipeline(input_data)
        return _result_to_json(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)[:300]})


async def _stream_decision(input_data: DecisionInput):
    """Generator that yields SSE events during pipeline execution."""
    queue = asyncio.Queue()

    def on_step(step: str, detail: str):
        queue.put_nowait({"step": step, "detail": detail})

    async def run():
        try:
            result = await run_decision_pipeline(input_data, on_step=on_step)
            queue.put_nowait({"result": _result_to_dict(result)})
        except Exception as e:
            queue.put_nowait({"error": str(e)[:300]})
        queue.put_nowait(None)  # sentinel

    task = asyncio.create_task(run())

    while True:
        item = await queue.get()
        if item is None:
            break
        if "step" in item:
            yield f"event: step\ndata: {json.dumps(item)}\n\n"
        elif "result" in item:
            yield f"event: result\ndata: {json.dumps(item['result'])}\n\n"
        elif "error" in item:
            yield f"event: error\ndata: {json.dumps(item)}\n\n"

    await task


# ─── History ───

@app.get("/api/history")
async def history():
    """Get recent decision evaluations."""
    return {"decisions": get_recent_decisions(limit=20)}


# ─── Helpers ───

def _result_to_dict(result) -> dict:
    return {
        "run_id": result.run_id,
        "question": result.question,
        "winner": result.winner,
        "why_winner_won": result.why_winner_won,
        "judges_agree": result.judges_agree,
        "judge_count": result.judge_count,
        "confidence_level": result.confidence_level,
        "confidence_score": result.confidence_score,
        "total_cost_usd": round(result.total_cost_usd, 4),
        "latency_ms": result.latency_ms,
        "ranked_options": [
            {
                "option": o.option,
                "rank": o.rank,
                "final_score": round(o.final_score, 2),
                "dimension_scores": {k: round(v, 2) for k, v in o.dimension_scores.items()},
                "strengths": o.strengths,
                "weaknesses": o.weaknesses,
                "rank_points": o.rank_points,
            }
            for o in result.ranked_options
        ],
    }


def _result_to_json(result) -> JSONResponse:
    return JSONResponse(content=_result_to_dict(result))


# ─── Static Files (for Streamlit or other frontend) ───

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
