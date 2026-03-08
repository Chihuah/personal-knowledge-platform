# Personal Knowledge Platform

Personal Knowledge Platform is a Linux-first private knowledge capture and retrieval system built around FastAPI, Next.js, PostgreSQL, Redis, and Celery.

## Current scope

This repository now includes the MVP foundation and first end-to-end backend flow:

- FastAPI APIs for capture, list, detail, dashboard, and reprocess
- SQLAlchemy models plus Alembic migrations
- Celery worker and parser / enrichment pipeline boundaries
- Next.js frontend MVP surface
- Docker Compose services for PostgreSQL, Redis, backend, worker, and frontend
- backend tests for API, pipeline, and task execution

## Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Node.js 22+

## Local development

1. Copy the environment template.

```bash
cp .env.example .env
```

2. Start the stack.

```bash
docker compose up --build
```

3. Open the apps.

- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/health`
- Dashboard API: `http://localhost:8000/api/dashboard`

## Backend setup without Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Run the worker in another shell:

```bash
cd backend
source .venv/bin/activate
TASKS_MODE=celery celery -A app.tasks.celery_app.celery_app worker --loglevel=INFO
```

## Frontend setup without Docker

```bash
cd frontend
npm install
npm run dev
```

## Tests

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Migration smoke check:

```bash
cd backend
source .venv/bin/activate
DATABASE_URL=sqlite+pysqlite:////tmp/pkp_migration.db alembic upgrade head
```

Frontend:

```bash
cd frontend
npm install
npm run build
```

## Version control conventions

- Use short-lived branches per task.
- Prefer small, reviewable commits.
- Keep generated files and secrets out of version control.

## Security notes

- Store the real `OPENAI_API_KEY` only in a local `.env` or deployment secret manager.
- Do not commit `.env`, exported credentials, or deployment-specific secret files.
- The repository only includes `.env.example` placeholders and local development defaults.

## License

MIT. See [LICENSE](/home/chihuah/projects/personal-knowledge-platform/LICENSE).
