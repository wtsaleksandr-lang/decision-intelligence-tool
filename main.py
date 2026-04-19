"""
Decision Intelligence Tool — FastAPI Backend + Frontend.
Single app, single port, single deploy.
"""

import asyncio
import json
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import settings
from engine.types import DecisionInput
from engine.pipeline import run_decision_pipeline
from tracking.history import get_recent_decisions, get_decision_by_run_id

app = FastAPI(title="Decision Intelligence Tool", version="0.2.0")
templates = Jinja2Templates(directory="templates")


# ─── Request/Response Models ───

class CriterionModel(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    weight: int = Field(ge=1, le=10, default=5)


class DecisionRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    options: list[str] = Field(min_length=2, max_length=10)
    criteria: list[CriterionModel] = Field(min_length=1, max_length=10)


# ─── Pages ───

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/decide")
async def decide_redirect():
    """Redirect /decide to homepage tool section."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/#tool", status_code=302)


@app.get("/result/{run_id}", response_class=HTMLResponse)
async def result_page(request: Request, run_id: str):
    decision = get_decision_by_run_id(run_id)
    if not decision:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("result.html", {"request": request, "result": decision})


# ─── API: Health ───

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "judges_available": settings.available_judges(),
        "has_api_keys": settings.has_any_api_key(),
    }


# ─── API: Decision Evaluation (SSE Stream) ───

@app.post("/api/decide")
async def decide(request: DecisionRequest, req: Request):
    """Evaluate a decision. Returns SSE stream with progress + final result."""

    if not settings.has_any_api_key():
        return JSONResponse(
            status_code=503,
            content={"error": "No AI judge API keys configured."},
        )

    input_data = DecisionInput(
        question=request.question,
        options=request.options,
        criteria=[{"name": c.name, "weight": c.weight} for c in request.criteria],
    )

    accept = req.headers.get("accept", "")
    if "text/event-stream" in accept:
        return StreamingResponse(
            _stream_decision(input_data),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    try:
        result = await run_decision_pipeline(input_data)
        return JSONResponse(content=_result_to_dict(result))
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
        queue.put_nowait(None)

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


# ─── API: History ───

@app.get("/api/history")
async def history():
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


# ─── Static Files ───

app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
