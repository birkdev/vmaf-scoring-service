# VMAF Scoring Service

A web service for computing VMAF scores between a reference and distorted video file. Built with FastAPI and deployed on Google Cloud Run.

## Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Upload form for scoring two videos |
| `/files` | POST | Accepts `reference` and `distorted` MP4 files (max 32 MB each), returns a VMAF score |
| `/monitor` | GET | Dashboard showing the last 100 uptime checks |
| `/health` | GET | Returns `{"status": "ok"}` |

## Running locally

```
pip install -r requirements.txt
uvicorn main:app --reload
```

## Docker

```
docker compose up
```
