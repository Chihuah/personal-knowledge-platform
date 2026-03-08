# Personal Knowledge Platform

## 中文說明

Personal Knowledge Platform 是一個以 Linux-first 為前提設計的私人知識收納與檢索平台，核心目標是把平常在 Facebook、Threads、YouTube 與一般網頁上看到的有價值內容，從「先丟連結存起來」這種鬆散收藏習慣，轉化成可整理、可搜尋、可回顧、可再利用的個人知識資產。

### 專案發想與源由

這個專案的起點很直接：日常在社群平台與網路上會持續遇到值得保存的文章、貼文、影片與工具介紹，但實際上大多數收藏行為只停留在把網址貼到 LINE 私人對話、筆記工具或書籤裡。久而久之，累積下來的是大量「曾經覺得重要，但之後很難找回」的資訊。

真正的問題不是缺少收藏工具，而是缺少一個能把這些連結進一步整理成知識條目的系統。因此這個專案的目的，不是單純再做一個 bookmark app，而是建立一條更完整的流程：

看到內容 -> 快速收錄 -> 自動解析 -> AI 摘要與分類 -> 日後搜尋與重新利用

### 專案目的

本專案希望解決以下幾個核心問題：

- 降低收錄資訊的摩擦，延續原本「看到就先存」的習慣
- 自動擷取網頁或影片的 metadata 與主要內容
- 透過 AI 協助產生摘要、關鍵字、分類與內容型態
- 讓過去收錄的內容不再只是網址堆積，而是具結構的 knowledge items
- 提供 dashboard、列表、詳細頁與搜尋，提升找回率與再利用率

### 目前的系統做法

目前的處理邏輯是先由後端 parser 抓取網頁資料與 metadata，再把整理後的文字內容交給 LLM 做摘要、關鍵字與分類分析，而不是讓 LLM 自主打開網頁與選工具瀏覽。這樣的設計在 MVP 階段更容易控制成本、提高可測試性，並讓資料流與錯誤邊界更清楚。

### AI 協作開發說明

本專案的規格整理、系統設計、任務拆解、文件撰寫與主要程式碼實作，皆在 OpenAI Codex / GPT-5.4 的協作下完成。這包含：

- PRD、requirements、design、tasks 等規格文件的建立與整理
- 後端 FastAPI、資料模型、背景任務與 parsing / enrichment pipeline 的撰寫
- 前端 Next.js MVP 頁面與 API 串接
- Docker Compose、README、測試與專案結構整理

換句話說，這個 repository 不只是「使用 AI 輔助寫幾段程式」，而是整個專案從需求定義到 MVP 實作，都有 AI 參與協作開發。

### 目前範圍

這個 repository 目前已包含 MVP 基礎與第一條可執行閉環：

- 使用者可貼上 URL 建立知識條目
- 後端可排入背景任務進行 parsing 與 AI enrichment
- 系統可儲存、列出、查詢、重新處理與顯示 dashboard
- 前端已有可操作的 MVP 頁面
- 本地開發以 Docker Compose 為主，並以 Linux 可移植性為優先

---

## English

Personal Knowledge Platform is a Linux-first private knowledge capture and retrieval system built around FastAPI, Next.js, PostgreSQL, Redis, and Celery.

### Project origin

This project started from a common problem: valuable links are easy to save, but hard to turn into reusable knowledge. Articles, social posts, videos, and tool references often end up scattered across chat threads, bookmarks, and temporary notes. Over time, that creates a pile of URLs instead of a searchable, structured personal knowledge base.

The purpose of this project is to close that gap by building a workflow that turns raw links into knowledge items:

See content -> Capture quickly -> Parse automatically -> Enrich with AI -> Find and reuse later

### AI-assisted development

This repository has been developed with substantial assistance from OpenAI GPT-5.4, including specification drafting, architecture planning, documentation writing, and code implementation for the MVP.

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
