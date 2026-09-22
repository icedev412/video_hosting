# Video Hosting API

FastAPI + PostgreSQL backend: video upload, likes, subscriptions, feed.
Background transcoding via arq + Redis; storage via any S3-compatible bucket (MinIO locally).

## Structure

```
app/
  core/       settings, DB engine/session, JWT + password hashing
  models/     SQLAlchemy ORM models
  schemas/    Pydantic request/response models
  routers/    API endpoints (auth, videos, feed)
  services/   storage.py — talks to S3/MinIO
  workers/    arq background jobs (transcoding)
  deps.py     shared dependencies (get_db, get_current_user)
  main.py     app instance, router wiring
alembic/      migrations
tests/
```

## Getting started

1. `cp .env.example .env` and set a real `SECRET_KEY`
2. `docker compose up --build`
3. In another shell: `docker compose exec api alembic revision --autogenerate -m "init"`
   then `docker compose exec api alembic upgrade head`
4. Open http://localhost:8000/docs

The `worker` service runs the arq worker that transcodes uploaded videos in
the background — `app/workers/tasks.py` has a `TODO` where the ffmpeg
pipeline goes.

## Tests

```
pytest
```
