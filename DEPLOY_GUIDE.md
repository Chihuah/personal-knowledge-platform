# 個人知識管理平台部署指南

## 專案簡介

此專案是一個基於 FastAPI (Python) 和 Next.js (React) 的個人知識管理平台。它提供了一個精簡的架構，專注於知識條目的儲存、顯示和搜尋功能。後端使用 PostgreSQL 進行資料儲存，並提供 API Key 驗證的寫入端點。前端則採用現代、簡潔的 UI 設計，支援帳號密碼登入，並具備響應式佈局和深色模式。

## 架構概覽

- **後端**: FastAPI (Python)
  - 資料庫: PostgreSQL
  - 驗證: API Key (寫入端點), 帳號密碼登入 (前端)
- **前端**: Next.js (React) with Tailwind CSS
  - 功能: 儀表板、知識條目列表（搜尋、篩選）、單筆條目詳細頁、登入頁
- **部署**: Docker Compose

## 部署步驟

本專案設計為可透過 Docker Compose 一鍵部署，特別適合在 Synoloy/QNAP NAS 等支援 Docker 的環境中運行。

### 1. 下載專案

請將改造後的專案壓縮包下載到您的部署環境中，例如 `/home/user/` 目錄下，然後解壓縮：

```bash
cd /home/user/
tar -xzvf personal-knowledge-platform.tar.gz
cd personal-knowledge-platform
```

### 2. 配置環境變數

專案根目錄下提供了一個 `.env.example` 檔案，您需要將其複製為 `.env` 並根據您的需求修改其中的變數。這些變數包含了資料庫連線、API Key、前端登入憑證等重要資訊。

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```ini
# ===== PostgreSQL =====
POSTGRES_DB=pkp
POSTGRES_USER=pkp
POSTGRES_PASSWORD=your-strong-db-password  # **請務必修改為強密碼**
POSTGRES_PORT=5432

# ===== Backend =====
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_APP_ENV=production
BACKEND_LOG_LEVEL=INFO
BACKEND_CORS_ORIGINS=http://localhost:3000,http://your-nas-ip:3000  # **請將 your-nas-ip 替換為您的 NAS IP 或前端域名**
DATABASE_URL=postgresql+psycopg://pkp:your-strong-db-password@postgres:5432/pkp # **請確保與 POSTGRES_PASSWORD 一致**

# API Key for external ingestion (used in X-API-Key header)
API_KEY=your-secret-api-key  # **請務必修改為您自己的 API Key**

# Frontend login credentials
AUTH_USERNAME=admin
AUTH_PASSWORD=your-strong-password  # **請務必修改為強密碼**

# JWT secret for session tokens
JWT_SECRET=your-random-jwt-secret-string  # **請務必修改為一個隨機且足夠長的字串**

# Pagination
ITEMS_PAGE_SIZE_DEFAULT=20
ITEMS_PAGE_SIZE_MAX=100

# ===== Frontend =====
FRONTEND_PORT=3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 # 如果前端與後端在同一主機，且透過 Docker Compose 內部網路通訊，此處可保持 localhost。若需外部訪問，請修改為後端服務的公開 URL。
```

**重要提示**：請確保 `POSTGRES_PASSWORD`、`API_KEY`、`AUTH_PASSWORD` 和 `JWT_SECRET` 都設置為安全且唯一的密碼/金鑰。

### 3. 啟動服務

在專案根目錄下執行以下命令啟動所有服務：

```bash
docker compose up -d
```

這將會啟動 PostgreSQL 資料庫、FastAPI 後端和 Next.js 前端服務。後端服務會自動執行 Alembic 資料庫遷移，建立所需的資料表。

### 4. 訪問平台

- **前端介面**: 部署成功後，您可以透過瀏覽器訪問 `http://localhost:3000` (如果您的 NAS IP 是 `192.168.1.100`，則可能是 `http://192.168.1.100:3000`)。使用您在 `.env` 中設定的 `AUTH_USERNAME` 和 `AUTH_PASSWORD` 進行登入。
- **後端 API 文件**: 您可以訪問 `http://localhost:8000/docs` 查看後端 API 的 Swagger UI 文件，其中包含了新的 `/api/items/ingest` 端點的詳細資訊。

### 5. 停止服務

若要停止所有服務，請在專案根目錄下執行：

```bash
docker compose down
```

若要停止並移除所有容器、網路和資料卷 (會刪除資料庫資料)，請執行：

```bash
docker compose down -v
```

## 外部知識條目提交 (API Ingestion)

您可以使用 `POST /api/items/ingest` 端點來提交結構化知識條目。請求需要包含 `X-API-Key` 標頭，其值應為您在 `.env` 中設定的 `API_KEY`。

**請求範例 (Python with `requests`)**:

```python
import requests
import json

API_KEY = "your-secret-api-key" # 替換為您的 API Key
BACKEND_URL = "http://localhost:8000" # 替換為您的後端 URL

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

data = {
    "source_url": "https://example.com/my-article",
    "source_platform": "blog",
    "author": "John Doe",
    "published_at": "2023-10-26T10:00:00Z",
    "title": "我的第一篇知識文章",
    "short_summary": "這是一篇關於個人知識管理系統的簡短摘要。",
    "full_summary": "這是一篇關於個人知識管理系統的完整摘要，詳細介紹了其設計理念和功能。",
    "keywords": ["知識管理", "個人", "生產力"],
    "category": "生產力工具",
    "content_type": "article",
    "raw_content": "這篇文章的完整內容..."
}

response = requests.post(f"{BACKEND_URL}/api/items/ingest", headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.json())
```

## 備註

- 本專案已移除 Celery 和 Redis 依賴，所有知識條目處理均為同步進行。
- 前端 UI 已全面美化，並支援深色模式，提供更好的使用者體驗。
- 響應式設計確保在不同設備上都能良好顯示。

