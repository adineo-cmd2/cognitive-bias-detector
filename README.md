# Cognitive Bias Detector

> Detect cognitive biases in reasoning and text.

Paste an argument or decision and the engine flags the cognitive biases at work, maps them across the document, and tracks bias patterns over time on a timeline.

## Features

- Bias map across full documents
- Explorer with bias definitions and examples
- Timeline of detected biases over history
- Adjustable sensitivity settings

## Architecture

| Layer | Stack | Path |
|---|---|---|
| Frontend | Astro (file-based routing) | `frontend/` |
| Backend | FastAPI + SQLAlchemy + Pydantic | `backend/` |
| Tests | pytest | `backend/tests/` |

Frontend routes: `bias-map, explorer, timeline, settings`.

## Quick start

Backend (from `backend/`):

```bash
pip install -r requirements.txt
cp .env.example .env        # optional — works with no keys
python3 -m uvicorn app.main:app --port 8001
```

Frontend (from `frontend/`):

```bash
npm install
npm run dev
```

Tests: `python3 -m pytest backend/tests/ -v`

## Deployment

The frontend builds to a static bundle and deploys to GitHub Pages on every
push to `main` (`.github/workflows/deploy.yml`):

**https://adineo-cmd2.github.io/cognitive-bias-detector/**

## Project structure

```
backend/
  app/          FastAPI application
  tests/        pytest suite
frontend/
  src/pages/    Astro routes
```
