# Personal Knowledge Platform (個人知識管理平台)

Personal Knowledge Platform 是一個以 Linux-first 為前提設計的私人知識收納與檢索平台。經過架構精簡與重構，本專案現在專注於「結構化知識的儲存、檢索與展示」，成為一個輕量級、高效能的個人知識庫。

## 專案簡介與動機

在資訊爆炸的時代，我們每天在社群平台（如 Facebook、Threads、X）、YouTube 與各大網站上看到大量有價值的內容。然而，傳統的「書籤」或「丟進筆記軟體」的方式，往往讓這些資訊變成死水，難以在需要時被找回。

本專案的核心目標是：**建立一個結構化的知識沉澱系統，讓收藏的內容可搜尋、可分類、可回顧。**

不同於傳統的書籤工具，本平台採用了全新的工作流：
我們將「內容解析與 AI 處理」的重度運算移出平台，交由外部的 AI 助理（如 Manus 或 Telegram Bot）處理。平台本身則專注於提供高效的資料庫儲存、精美的視覺化展示與強大的檢索功能。

### 新版工作流程

1. **收集**：使用者在 Telegram 對話中將有價值的網頁連結傳送給 AI 助理。
2. **處理（外部）**：AI 助理自動擷取網頁內容，生成摘要、提取關鍵字並進行分類。
3. **收錄**：AI 助理透過本平台的 `/api/items/ingest` 端點，將結構化資料寫入系統。
4. **利用**：使用者登入平台，透過美觀的儀表板與列表頁，輕鬆搜尋與瀏覽知識條目。

## 系統架構

本專案採用精簡的微服務架構，透過 Cloudflare Tunnel 實現安全的公網存取，無需在路由器上開放任何連接埠：

```text
                    ┌─────────────────────────────┐
                    │        Internet              │
                    └──────────┬──────────────────-┘
                               │
                    ┌──────────▼──────────────────-┐
                    │    Cloudflare Tunnel          │
                    │    (cloudflared container)    │
                    │                               │
                    │  kno.domain.com → frontend    │
                    │  api-kno.domain.com → backend │
                    └──────────┬──────────────────-┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                     │
          ▼                    ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Next.js 前端   │  │  FastAPI 後端   │  │  PostgreSQL     │
│  (kno-frontend) │  │  (kno-backend)  │  │  (kno-postgres) │
│  :3000          │  │  :8000          │  │  :5432          │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                            │
                     ┌──────▼──────┐
                     │ 外部 AI 助理│
                     │ (API 寫入)  │
                     └─────────────┘
```

- **Cloudflare Tunnel**：透過 `cloudflared` 容器建立加密隧道，將公網請求安全地轉發到內部服務，無需暴露任何連接埠。
- **外部 AI 助理**：負責繁重的網頁爬取與 LLM 處理任務，透過 API Key 驗證將結構化資料寫入平台。
- **FastAPI 後端**：提供 API Key 驗證的寫入端點，以及供前端使用的查詢 API。
- **PostgreSQL 資料庫**：儲存所有結構化知識條目，並提供內建的全文搜尋能力。
- **Next.js 前端**：提供現代化、響應式的使用者介面，包含儀表板、列表頁與詳細頁。

## 功能特色

- **🚀 輕量級架構**：移除了 Celery 與 Redis，系統資源佔用極低，非常適合部署在 NAS 或低配置伺服器上。
- **🌐 Cloudflare Tunnel 整合**：內建 `cloudflared` 容器，一鍵啟動即可實現安全的公網存取，無需設定 port forwarding 或 DDNS。
- **🔒 安全寫入與存取**：
  - 寫入端點受 API Key 保護，防止未授權的資料寫入。
  - 前端採用 JWT 帳號密碼登入機制，確保私人知識庫不被公開存取。
- **✨ 現代化 UI 設計**：
  - 全面使用 Tailwind CSS 打造專業、簡潔的介面。
  - 內建深色模式 (Dark Mode) 支援。
  - 完美適配手機與電腦的響應式設計。
- **📊 數據儀表板**：首頁提供直觀的統計數據，包括收錄總數、平台來源分佈與內容類型分佈。
- **🔍 高效檢索**：基於 PostgreSQL 的搜尋功能，支援跨欄位（標題、摘要、關鍵字、作者、分類）的關鍵字查詢、平台過濾與分類篩選。

## 技術棧

- **後端**：Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic, Alembic
- **資料庫**：PostgreSQL 17 (搭配 psycopg 3)
- **前端**：Node.js 22, Next.js 15 (App Router), React 19, Tailwind CSS 3.4
- **網路**：Cloudflare Tunnel (cloudflared)
- **部署**：Docker, Docker Compose

## 部署指南

本專案專為容器化部署設計，特別針對 QNAP NAS 等環境進行了優化。

### 快速啟動

1. 複製環境變數範本：

   ```bash
   cp .env.example .env
   ```

2. 編輯 `.env` 檔案，設定你的密碼與 API Key：

   ```env
   # 設定寫入資料用的 API Key
   API_KEY=your_secure_api_key_here

   # 設定前端登入帳號密碼
   AUTH_USERNAME=admin
   AUTH_PASSWORD=your_secure_password

   # 設定 JWT 密鑰
   JWT_SECRET=generate_a_random_string_here

   # 設定前端呼叫後端 API 的公開 URL
   NEXT_PUBLIC_API_BASE_URL=https://api-knowledge.yourdomain.com

   # 設定 Cloudflare Tunnel Token
   CLOUDFLARE_TUNNEL_TOKEN=your-cloudflare-tunnel-token
   ```

3. 使用 Docker Compose 啟動：

   ```bash
   docker compose up -d --build
   ```

4. 訪問應用：
   - 前端介面：`https://knowledge.yourdomain.com`（或 `http://localhost:3000`）
   - 後端 API：`https://api-knowledge.yourdomain.com`（或 `http://localhost:8000`）

### 設定 Cloudflare Tunnel

本專案的 `docker-compose.yml` 已內建 `cloudflared` 服務，可透過 Cloudflare Tunnel 實現安全的公網存取，無需在路由器上設定 port forwarding。

**設定步驟：**

1. 登入 [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. 前往 **Networks** → **Tunnels** → **Create a tunnel**
3. 選擇 **Cloudflared** 作為連接器類型
4. 為 Tunnel 命名（例如 `nas-docker-tunnel`）
5. 複製 Tunnel Token，貼到 `.env` 檔案中的 `CLOUDFLARE_TUNNEL_TOKEN`
6. 在 Tunnel 的 **Public Hostname** 設定中，新增兩條路由：

   | Subdomain       | Domain           | Service                 |
   | --------------- | ---------------- | ----------------------- |
   | `knowledge`     | `yourdomain.com` | `http://localhost:3000` |
   | `api-knowledge` | `yourdomain.com` | `http://localhost:8000` |

   > **注意**：由於 `docker-compose.yml` 中 cloudflared 使用 `network_mode: "host"`，因此 Service 欄位需填寫 `localhost` 而非容器名稱。

7. **（選用）設定 Cloudflare WAF 規則**：若需要允許外部 API 呼叫（例如 AI 助理透過 API 寫入資料），請在 Cloudflare WAF 中新增規則，對帶有有效 `X-API-Key` 標頭的請求跳過驗證挑戰。

### QNAP NAS 部署注意事項

- 如果 NAS 上已有其他服務佔用 port 5432，可在 `.env` 中修改 `POSTGRES_PORT` 為其他值（例如 `5433`），僅影響對外 port，不影響容器內部連線。
- 如果遇到網路連線或防火牆問題，可以修改 `docker-compose.yml`，將 `backend` 與 `frontend` 服務設置為 `network_mode: "host"`。

> 更詳細的部署說明，請參考專案內的 `DEPLOY_GUIDE.md`。

## API 使用範例

### 寫入知識條目

外部系統（如 AI 助理）可以透過以下 API 將整理好的知識條目寫入平台：

```bash
curl -X POST https://api-knowledge.yourdomain.com/api/items/ingest \
  -H "X-API-Key: your_secure_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "source_url": "https://example.com/article",
    "source_platform": "facebook",
    "title": "文章標題",
    "author": "作者名稱",
    "short_summary": "一句話總結這篇文章",
    "full_summary": "詳細的重點摘要...",
    "keywords": ["AI", "Knowledge Management", "Productivity"],
    "category": "Technology",
    "content_type": "article"
  }'
```

### 搜尋知識條目

```bash
curl "https://api-knowledge.yourdomain.com/api/items?q=keyword&platform=facebook&sort=newest"
```

支援的查詢參數：

| 參數                 | 說明                                               |
| -------------------- | -------------------------------------------------- |
| `q`                  | 關鍵字搜尋（搜尋標題、摘要、全文摘要、作者、分類） |
| `platform`           | 依來源平台篩選（facebook, threads, youtube 等）    |
| `category`           | 依分類篩選                                         |
| `content_type`       | 依內容類型篩選                                     |
| `sort`               | 排序方式（newest, oldest, updated）                |
| `page` / `page_size` | 分頁控制                                           |

## 未來規劃

- 支援多位使用者與獨立的知識庫空間
- 增加知識圖譜（Knowledge Graph）視覺化功能
- 提供瀏覽器擴充功能，讓使用者可以在瀏覽網頁時直接觸發 AI 處理與收錄
- 支援更多內容來源平台的特定解析邏輯
- 前端新增編輯與刪除功能
- 圖片下載與儲存功能

---

## 授權條款

MIT License.

---

# Personal Knowledge Platform

The Personal Knowledge Platform is a Linux-first private knowledge storage and retrieval system. After architectural streamlining and refactoring, this project now focuses on "structured knowledge storage, retrieval, and display," serving as a lightweight, high-performance personal knowledge base.

## Project Introduction and Motivation

In an era of information overload, we encounter vast amounts of valuable content daily on social media platforms (e.g., Facebook, Threads, X), YouTube, and various websites. However, traditional methods like "bookmarking" or "dumping into note-taking apps" often render this information stagnant, making it difficult to retrieve when needed.

The core objective of this project is to: **establish a structured knowledge sedimentation system that makes collected content searchable, categorizable, and reviewable.**

Unlike conventional bookmarking tools, this platform adopts a new workflow:
We offload the computationally intensive tasks of "content parsing and AI processing" from the platform to external AI assistants (such as Manus or Telegram Bots). The platform itself then focuses on providing efficient database storage, elegant visual presentation, and powerful retrieval capabilities.

### New Workflow

1.  **Collect**: Users send valuable web links to an AI assistant via Telegram chat.
2.  **Process (External)**: The AI assistant automatically extracts web content, generates summaries, extracts keywords, and categorizes the information.
3.  **Ingest**: The AI assistant writes the structured data into the system via the platform's `/api/items/ingest` endpoint.
4.  **Utilize**: Users log into the platform and easily search and browse knowledge items through a beautiful dashboard and list pages.

## System Architecture

This project adopts a streamlined microservices architecture, comprising three core components:

```text
[ External AI Assistant ]
       │
       │ (Submits structured JSON with API Key authentication)
       ▼
[ FastAPI Backend ] ◄─── (REST API) ───► [ Next.js Frontend ]
       │                                     │
       │ (SQLAlchemy)                        │ (Users access via browser)
       ▼                                     ▼
[ PostgreSQL Database ]                   [ Users (requires login) ]
```

- **External AI Assistant**: Handles the heavy lifting of web scraping and LLM processing tasks.
- **FastAPI Backend**: Provides an API Key-authenticated ingestion endpoint and query APIs for the frontend.
- **PostgreSQL Database**: Stores all structured knowledge items and offers built-in full-text search capabilities.
- **Next.js Frontend**: Delivers a modern, responsive user interface, including a dashboard, list pages, and detail pages.

## Features

- **🚀 Lightweight Architecture**: Celery and Redis have been removed, resulting in minimal system resource consumption, ideal for deployment on NAS or low-spec servers.
- **🔒 Secure Ingestion and Access**:
  - Ingestion endpoint is protected by an API Key to prevent unauthorized data writes.
  - Frontend uses a JWT username/password login mechanism to ensure private knowledge bases are not publicly accessible.
- **✨ Modern UI Design**:
  - Built entirely with Tailwind CSS for a professional, clean interface.
  - Includes built-in Dark Mode support.
  - Responsive design perfectly adapts to mobile and desktop devices.
- **📊 Data Dashboard**: The homepage provides intuitive statistics, including total items collected, distribution by source platform, and content type distribution.
- **🔍 Efficient Retrieval**: PostgreSQL-based search functionality supports keyword queries, platform filtering, and category filtering.

## Technology Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic, Alembic
- **Database**: PostgreSQL 17 (with psycopg 3)
- **Frontend**: Node.js 22, Next.js 15 (App Router), React 19, Tailwind CSS 3.4
- **Deployment**: Docker, Docker Compose

## Deployment Guide

This project is designed for containerized deployment, with optimizations specifically for environments like NAS.

### Quick Start

1.  Copy the environment variable template:

    ```bash
    cp .env.example .env
    ```

2.  Edit the `.env` file to configure your passwords and API Key:

    ```env
    # API Key for data ingestion
    API_KEY=your_secure_api_key_here

    # Frontend login credentials
    AUTH_USERNAME=admin
    AUTH_PASSWORD=your_secure_password

    # JWT Secret Key
    JWT_SECRET=generate_a_random_string_here
    ```

3.  Start with Docker Compose:

    ```bash
    docker compose up -d
    ```

4.  Access the application:
    - Frontend UI: `http://localhost:3000` (or your NAS IP:3000)
    - Backend API: `http://localhost:8000`

### NAS Deployment Notes

If you encounter network connectivity or firewall issues on NAS, you can modify `docker-compose.yml` to set `network_mode: "host"` for the `backend` and `frontend` services.

> For more detailed deployment instructions, please refer to `DEPLOY_GUIDE.md` in the project.

## API Usage Example

External systems (e.g., AI assistants) can ingest structured knowledge items into the platform via the following API:

```bash
curl -X POST http://your-server:8000/api/items/ingest \
  -H "X-API-Key: your_secure_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "source_url": "https://example.com/article",
    "source_platform": "generic_web",
    "title": "Article Title",
    "author": "Author Name",
    "published_at": "2024-03-14T12:00:00Z",
    "raw_content": "Full article content...",
    "short_summary": "A one-sentence summary of the article",
    "full_summary": "Detailed key summary...",
    "keywords": ["AI", "Knowledge Management", "Productivity"],
    "category": "Technology",
    "content_type": "article"
  }'
```

## Future Plans

- Support multiple users with independent knowledge spaces.
- Add Knowledge Graph visualization features.
- Provide browser extensions to allow users to directly trigger AI processing and ingestion while browsing the web.
- Support specific parsing logic for more content source platforms.

---

## License

MIT License. See [LICENSE](/home/chihuah/projects/personal-knowledge-platform/LICENSE).
