# Decision Intelligence Tool

A web application that helps users make better decisions by evaluating multiple options against weighted criteria using multiple AI models as "blind judges."

## Architecture

- **Backend:** FastAPI (Python) served via Uvicorn/Gunicorn
- **Frontend:** Jinja2 HTML templates + static files served by FastAPI
- **Single app, single port** — frontend and backend run together on port 5000

## Key Features

- **Blind Judging:** Options are anonymized and shuffled to prevent position bias
- **Multi-Model Evaluation:** Uses OpenAI (GPT-4o), Anthropic (Claude), and Google (Gemini) in parallel
- **Weighted Criteria:** Users define criteria with different weights
- **Confidence Scoring:** Based on judge agreement and statistical margin
- **Real-time Progress:** Server-Sent Events (SSE) stream pipeline progress
- **Cost Tracking:** Estimates USD cost per decision run

## Project Layout

```
main.py           - FastAPI app entry point, routes, SSE logic
config.py         - Settings (host, port, API key detection)
engine/           - Core decision pipeline logic
  pipeline.py     - Orchestrates the full decision flow
  types.py        - Pydantic models for data structures
  verdict.py      - Confidence scoring and recommendation text
judges/           - AI judging logic
  blind_judge.py  - Option anonymization and AI call retry logic
  aggregator.py   - Merges results from multiple judges
  rubric.py       - Generates system prompts/scoring rubrics
providers/        - LLM API adapters (OpenAI, Anthropic, Google, etc.)
tracking/         - Cost tracking and decision history
templates/        - Jinja2 HTML templates
static/           - Static assets (CSS, JS)
tests/            - Smoke tests
```

## Running Locally

```bash
python main.py
```

Server runs on `http://0.0.0.0:5000`

## Required Environment Variables

At least ONE of the following API keys is required:

- `OPENAI_API_KEY` — OpenAI GPT-4o
- `ANTHROPIC_API_KEY` — Anthropic Claude
- `GOOGLE_API_KEY` — Google Gemini

Optional:
- `COST_PROFILE` — `cheap` | `balanced` | `full` (default: `cheap`)
- `PORT` — server port (default: `5000`)
- `DEBUG` — `true` | `false` (default: `false`)

## Dependencies

- fastapi, uvicorn, gunicorn — web server
- httpx — async HTTP for AI API calls
- python-dotenv — environment variable management
- jinja2 — HTML templating
- pydantic — data validation

## Notes

- Starlette 1.0.0 changed the `TemplateResponse` API — `request` is now the first positional argument, not part of the context dict
- Default port changed from 8000 to 5000 for Replit compatibility
