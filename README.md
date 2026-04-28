# Dwellio API

Minimal FastAPI scaffold for the Dwellio apartment search backend.

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

## Health Check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "Dwellio API",
  "environment": "development"
}
```
