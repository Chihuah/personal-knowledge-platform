design.md
=========

專案名稱
----

**Personal Knowledge Platform（個人知識平台）**

* * *

1\. 設計目標
--------

本文件的目的，是將 `requirements.md` 中定義的需求，轉化為具體的系統設計方案，作為後續實作、拆解任務與技術選型的依據。

本系統的核心設計目標如下：

1.  提供低摩擦的連結收錄流程。
2.  將網址自動轉換為具結構化資訊的知識條目。
3.  透過 AI/LLM 對內容進行摘要、分類、關鍵字提取與後續查詢支援。
4.  提供清楚的儀表板、列表瀏覽與搜尋介面。
5.  採模組化與可擴充設計，便於未來加入更多來源平台、語意搜尋與知識代理功能。

* * *

2\. 系統總覽架構
----------

本系統可拆分為以下幾個核心模組：

1.  **Ingestion Module（收錄模組）**  
    負責接收使用者送入的網址。
2.  **Parsing Module（內容解析模組）**  
    負責擷取網頁或影片的 metadata 與主要內容。
3.  **AI Enrichment Module（AI 分析模組）**  
    負責摘要、關鍵字、分類與內容類型判定。
4.  **Knowledge Store（知識儲存層）**  
    負責儲存知識條目、內容文本與分析結果。
5.  **Search & Query Module（搜尋與查詢模組）**  
    提供關鍵字搜尋與後續語意搜尋擴充能力。
6.  **Dashboard & UI Module（前端展示模組）**  
    提供首頁儀表板、列表頁、詳細頁與搜尋介面。
7.  **Background Job Module（背景工作模組）**  
    處理非同步內容解析與 AI 分析任務。

* * *

3\. 高階系統流程
----------

### 3.1 收錄流程

1.  使用者透過前端介面貼上網址，或由行動端分享連結至平台。
2.  API 接收網址請求。
3.  系統進行網址驗證與去重判斷。
4.  建立初始知識條目，狀態為 `received`。
5.  背景任務開始執行內容擷取。
6.  擷取完成後，更新狀態為 `parsing_completed`。
7.  系統呼叫 LLM 進行摘要、關鍵字、分類分析。
8.  分析完成後，更新狀態為 `ready`。
9.  條目出現在列表頁、搜尋頁與儀表板。

### 3.2 查詢流程

1.  使用者於搜尋頁輸入關鍵字或自然語言查詢。
2.  後端查詢資料庫與搜尋索引。
3.  回傳符合條件的知識條目。
4.  前端展示標題、摘要、來源與分類等資訊。
5.  使用者可點入詳細頁查看完整內容。

* * *

4\. 系統架構設計
----------

* * *

### 4.1 架構風格

建議採用：

*   **前後端分離架構**
*   **API 驅動**
*   **背景任務非同步處理**
*   **模組化服務設計**

MVP 階段不必拆成微服務，可先維持 **modular monolith（模組化單體架構）**，以降低開發與維運複雜度。

也就是說，部署上可以是一套系統，但程式結構上清楚區分模組。

* * *

### 4.2 建議技術組合

#### 前端

*   **Next.js**
    *   適合做 dashboard、列表頁、SEO 不是主要需求但開發體驗佳
    *   可同時處理前端 UI 與部分 server-side rendering

替代方案：

*   React + Vite

#### 後端

*   **FastAPI**
    *   適合快速開發 API
    *   易於與 Python 生態整合（爬取、文本處理、LLM API）
    *   適合任務導向與 AI 整合場景

替代方案：

*   NestJS
*   Django + DRF

#### 資料庫

*   **PostgreSQL**
    *   結構化資料穩定
    *   可支援 Full Text Search
    *   後續可擴充 pgvector

#### 背景任務

*   **Celery + Redis**
    *   適合解析任務、AI 任務、重試機制

較輕量替代方案：

*   RQ + Redis
*   FastAPI background tasks（僅適合 very small MVP，不建議長期使用）

#### AI/LLM

*   OpenAI API
    *   用於摘要、關鍵字、分類
    *   後續可加 embeddings

#### 搜尋

MVP：

*   PostgreSQL Full Text Search

第二階段：

*   `pgvector` 或外部向量資料庫

#### 內容擷取

*   BeautifulSoup / readability-lxml / trafilatura
*   YouTube 另做專用 parser
*   後續可考慮 headless browser 作為 fallback

* * *

5\. 模組設計
--------

* * *

### 5.1 Ingestion Module

#### 功能

*   接收使用者輸入的 URL
*   驗證格式
*   去重判斷
*   建立初始條目

#### 輸入

*   URL
*   可選的使用者備註（未來可擴充）

#### 輸出

*   建立一筆 knowledge item
*   任務丟入 queue

#### 設計重點

*   前端收到成功回應時，不需等待 AI 完成
*   API 僅負責接收、建立初始資料與排入背景任務

#### 狀態轉換

*   `received`
*   `queued`

* * *

### 5.2 Parsing Module

#### 功能

*   判斷來源平台
*   擷取 metadata
*   擷取主要文本
*   清洗文本內容

#### 支援來源

*   Facebook（先支援可公開取得之 metadata 與連結內容）
*   Threads
*   YouTube
*   一般文章頁面

#### 設計重點

不同來源應使用不同 parser strategy：

*   `FacebookParser`
*   `ThreadsParser`
*   `YouTubeParser`
*   `GenericWebParser`

建議使用 **Strategy Pattern**，依 URL domain 選擇對應 parser。

#### 輸出欄位

*   title
*   description
*   author
*   published\_at
*   thumbnail
*   raw\_content
*   cleaned\_content
*   source\_platform
*   content\_type

#### 例外處理

若解析失敗：

*   記錄 error message
*   更新條目狀態為 `failed`

* * *

### 5.3 AI Enrichment Module

#### 功能

*   對解析後內容做摘要
*   提取關鍵字
*   自動分類
*   判定內容類型
*   未來可加 embedding

#### 輸入

*   title
*   cleaned\_content
*   source\_platform
*   metadata

#### 輸出

*   short\_summary
*   full\_summary（可選）
*   keywords
*   category
*   content\_type
*   enrichment metadata

#### Prompt 設計原則

Prompt 應要求 LLM 回傳固定 JSON 結構，例如：

```
{
  "short_summary": "string",
  "keywords": ["string", "string"],
  "category": "string",
  "content_type": "string"
}
```

#### 設計重點

*   嚴格限制回傳格式
*   若 LLM 回傳格式錯誤，需有 retry 或 parser fallback
*   對過長內容先做 truncate 或 chunking

* * *

### 5.4 Knowledge Store

#### 功能

*   儲存知識條目
*   儲存擷取內容
*   儲存 AI 分析結果
*   提供查詢基礎

#### 設計原則

*   核心實體以 `knowledge_items` 為主
*   metadata、摘要、原文與 AI 結果可先存在單一表
*   未來若欄位複雜，再拆子表

* * *

### 5.5 Search & Query Module

#### MVP 階段功能

*   關鍵字搜尋
*   條件篩選
*   排序

#### 第二階段功能

*   語意搜尋
*   自然語言問答
*   相似條目推薦

#### 搜尋範圍

MVP 先搜尋：

*   title
*   short\_summary
*   keywords
*   cleaned\_content

#### 設計重點

MVP 先使用 PostgreSQL Full Text Search，原因：

*   部署簡單
*   不需額外服務
*   足夠支援第一版

* * *

### 5.6 Dashboard & UI Module

#### 頁面組成

1.  首頁 Dashboard
2.  知識條目列表頁
3.  單筆條目詳細頁
4.  搜尋頁
5.  收錄頁（手動新增 URL）

#### 首頁 Dashboard 顯示內容

*   總收藏數
*   最近新增數
*   最新收錄條目
*   分類統計
*   處理狀態統計

#### 列表頁功能

*   顯示卡片或表格
*   可依時間排序
*   可依分類、平台、狀態篩選

#### 詳細頁功能

*   顯示 title
*   顯示 source\_url
*   顯示 thumbnail
*   顯示 short\_summary
*   顯示完整擷取內容
*   顯示關鍵字、分類
*   顯示處理狀態

* * *

### 5.7 Background Job Module

#### 功能

*   執行解析任務
*   執行 AI 分析任務
*   重試失敗任務
*   更新任務狀態

#### 工作流程建議

1.  `parse_url_job`
2.  `enrich_content_job`
3.  `generate_embedding_job`（第二階段）

#### 設計重點

*   任務需可重試
*   任務失敗要記錄 log
*   條目狀態要可追蹤

* * *

6\. 資料表設計
---------

以下為 MVP 階段建議的主要資料表。

* * *

### 6.1 knowledge\_items

| 欄位名稱 | 型別 | 說明 |
| --- | --- | --- |
| id | UUID / BIGSERIAL | 主鍵 |
| source\_url | TEXT | 原始網址 |
| source\_platform | VARCHAR(50) | 來源平台 |
| title | TEXT | 標題 |
| author | TEXT | 作者或來源名稱 |
| published\_at | TIMESTAMP NULL | 發布時間 |
| captured\_at | TIMESTAMP | 收錄時間 |
| thumbnail\_url | TEXT NULL | 封面圖 |
| description | TEXT NULL | 原始 description |
| cleaned\_content | TEXT NULL | 清洗後內容 |
| short\_summary | TEXT NULL | 短摘要 |
| full\_summary | TEXT NULL | 長摘要，可選 |
| keywords | JSONB / TEXT\[\] | 關鍵字 |
| category | VARCHAR(100) NULL | 分類 |
| content\_type | VARCHAR(50) NULL | 內容類型 |
| processing\_status | VARCHAR(50) | 狀態 |
| error\_message | TEXT NULL | 錯誤資訊 |
| created\_at | TIMESTAMP | 建立時間 |
| updated\_at | TIMESTAMP | 更新時間 |

* * *

### 6.2 ingestion\_logs

| 欄位名稱 | 型別 | 說明 |
| --- | --- | --- |
| id | UUID / BIGSERIAL | 主鍵 |
| knowledge\_item\_id | FK | 對應條目 |
| action | VARCHAR(50) | 動作名稱 |
| status | VARCHAR(50) | 成功 / 失敗 |
| message | TEXT NULL | 記錄訊息 |
| created\_at | TIMESTAMP | 建立時間 |

用途：

*   追蹤解析與 AI 任務歷程
*   幫助 debug

* * *

### 6.3 tags（第二階段可拆）

MVP 可先不獨立建表，直接存在 `keywords` 欄位。  
若未來要支援使用者自訂標籤，再拆成：

*   `tags`
*   `knowledge_item_tags`

* * *

### 6.4 embeddings（第二階段）

若後續加入語意搜尋，可新增：

| 欄位名稱 | 型別 | 說明 |
| --- | --- | --- |
| id | UUID / BIGSERIAL | 主鍵 |
| knowledge\_item\_id | FK | 對應條目 |
| embedding | VECTOR | 向量資料 |
| model\_name | VARCHAR(100) | embedding model |
| created\_at | TIMESTAMP | 建立時間 |

* * *

7\. API 設計
----------

以下為 MVP 建議 API。

* * *

### 7.1 新增網址

**POST** `/api/items`

#### Request

```
{
  "url": "https://example.com/article"
}
```

#### Response

```
{
  "id": "uuid",
  "status": "received",
  "message": "Item created successfully"
}
```

* * *

### 7.2 查詢條目列表

**GET** `/api/items`

#### Query Parameters

*   `q`：關鍵字
*   `platform`
*   `category`
*   `status`
*   `page`
*   `page_size`
*   `sort`

#### Response

```
{
  "items": [
    {
      "id": "uuid",
      "title": "example",
      "source_platform": "youtube",
      "short_summary": "summary...",
      "category": "AI工具",
      "processing_status": "ready",
      "captured_at": "2026-03-07T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100
  }
}
```

* * *

### 7.3 取得單筆條目

**GET** `/api/items/{id}`

#### Response

```
{
  "id": "uuid",
  "source_url": "https://example.com",
  "title": "example title",
  "source_platform": "facebook",
  "author": "author name",
  "published_at": "2026-03-01T12:00:00",
  "captured_at": "2026-03-07T10:00:00",
  "thumbnail_url": "https://...",
  "description": "...",
  "cleaned_content": "...",
  "short_summary": "...",
  "full_summary": "...",
  "keywords": ["AI", "知識管理"],
  "category": "知識管理",
  "content_type": "貼文",
  "processing_status": "ready"
}
```

* * *

### 7.4 Dashboard 資料

**GET** `/api/dashboard`

#### Response

```
{
  "total_items": 150,
  "new_items_last_7_days": 12,
  "latest_items": [],
  "category_distribution": [
    { "category": "AI工具", "count": 30 },
    { "category": "教學", "count": 24 }
  ],
  "status_distribution": [
    { "status": "ready", "count": 120 },
    { "status": "parsing", "count": 5 }
  ]
}
```

* * *

### 7.5 重新處理條目

**POST** `/api/items/{id}/reprocess`

用途：

*   解析失敗時手動重跑
*   第二階段優化 AI 分析時重建資料

* * *

8\. 狀態機設計
---------

知識條目狀態建議如下：

*   `received`：已收到 URL
*   `queued`：已排入背景任務
*   `parsing`：內容解析中
*   `parsed`：解析完成
*   `analyzing`：AI 分析中
*   `ready`：完成，可正常展示
*   `failed`：任務失敗

### 狀態轉換範例

`received → queued → parsing → parsed → analyzing → ready`

若失敗：  
`parsing → failed`  
或  
`analyzing → failed`

* * *

9\. Parser 設計策略
---------------

為了提高可維護性，建議定義 parser 介面：

```
class BaseParser:
    def can_handle(self, url: str) -> bool:
        pass

    def parse(self, url: str) -> ParsedContent:
        pass
```

各平台實作：

*   `FacebookParser`
*   `ThreadsParser`
*   `YouTubeParser`
*   `GenericWebParser`

### ParsedContent 結構

```
class ParsedContent:
    title: str
    description: str | None
    author: str | None
    published_at: datetime | None
    thumbnail_url: str | None
    raw_content: str | None
    cleaned_content: str | None
    source_platform: str
    content_type: str | None
```

* * *

10\. AI Prompt 設計
-----------------

建議將 prompt 模組化，不要把 prompt 直接寫死在業務邏輯中。

可拆成：

*   `summary_prompt.py`
*   `classification_prompt.py`
*   `keyword_prompt.py`

或整合成單一 enrichment prompt。

### 範例輸入

*   title
*   platform
*   content\_text

### 範例輸出

```
{
  "short_summary": "這篇內容主要在說明……",
  "full_summary": "更完整摘要……",
  "keywords": ["知識管理", "AI整理", "社群收藏"],
  "category": "知識管理",
  "content_type": "文章"
}
```

### Prompt 設計原則

*   請模型只輸出 JSON
*   明確限制欄位
*   明確定義 category 候選集合
*   對超長內容做長度控制

* * *

11\. 搜尋設計
---------

* * *

### 11.1 MVP 搜尋

採用 PostgreSQL Full Text Search。

建立 searchable document，例如：

*   `title`
*   `short_summary`
*   `keywords`
*   `cleaned_content`

可合併為 `tsvector` 欄位，提升查詢效率。

### 11.2 第二階段搜尋

導入 embeddings 與 vector search，支援：

*   語意近似查詢
*   自然語言問答
*   相關條目推薦

* * *

12\. 前端頁面資訊架構
-------------

* * *

### 12.1 首頁 Dashboard

區塊建議：

*   Summary cards
    *   總收藏數
    *   最近 7 天新增
    *   ready 條目數
    *   failed 條目數
*   最新收錄條目
*   分類分布
*   最近處理失敗條目

* * *

### 12.2 列表頁

欄位建議：

*   標題
*   平台
*   分類
*   摘要
*   收錄時間
*   狀態

操作：

*   搜尋
*   篩選
*   排序
*   點擊進入詳細頁

* * *

### 12.3 詳細頁

區塊建議：

*   基本資訊區
*   原始連結區
*   摘要區
*   關鍵字 / 分類區
*   擷取內容區
*   處理歷程區（可選）

* * *

### 12.4 新增頁

一個簡單表單：

*   URL input
*   submit button

顯示：

*   成功提示
*   若已存在則顯示已有條目連結

* * *

13\. 安全與權限設計
------------

由於 MVP 預設為單人私人系統，可先採最簡化策略：

*   只有單一使用者登入
*   使用 session 或 token 驗證
*   所有資料皆屬私人

若先本機或私有部署，甚至可在 MVP 階段簡化登入，但正式版仍建議保留基本驗證。

### 後續可擴充

*   OAuth 登入
*   多使用者隔離
*   API key 保護
*   權限控管

* * *

14\. 錯誤處理設計
-----------

常見錯誤情境：

1.  URL 格式錯誤
2.  網頁內容無法擷取
3.  平台限制導致內容抓取失敗
4.  LLM API 失敗
5.  LLM 回傳格式異常
6.  重複網址提交

### 對應策略

*   API 回傳清楚錯誤訊息
*   ingestion\_logs 記錄每次失敗原因
*   失敗條目可重試
*   前端顯示目前狀態與錯誤摘要

* * *

15\. 可觀測性與紀錄
------------

建議加入：

*   application log
*   task log
*   ingestion log
*   API request log

至少需能觀察：

*   每日收錄量
*   解析成功率
*   AI 分析成功率
*   平均處理時間
*   失敗原因分布

* * *

16\. 部署建議
---------

### MVP 階段

可採單機 Docker Compose 部署：

*   frontend
*   backend
*   postgres
*   redis
*   worker

### 優點

*   架構清楚
*   方便本地開發
*   易於後續搬到 VPS 或 NAS

### 後續擴充

可再導入：

*   Nginx reverse proxy
*   object storage
*   monitoring
*   CI/CD pipeline

* * *

17\. MVP 開發優先順序
---------------

### Phase 1：核心資料流

1.  建立後端 API
2.  建立資料表
3.  完成新增 URL 流程
4.  完成基本 parser
5.  完成背景任務 queue
6.  完成 AI enrichment

### Phase 2：基本前端

1.  新增頁
2.  列表頁
3.  詳細頁
4.  Dashboard

### Phase 3：搜尋與優化

1.  關鍵字搜尋
2.  篩選功能
3.  錯誤重試
4.  狀態顯示

* * *

18\. 第二階段擴充設計方向
---------------

未來可擴充以下模組：

### 18.1 Share Integration

*   iOS share sheet
*   LINE Bot
*   Telegram Bot
*   瀏覽器 extension

### 18.2 Personal Notes

*   使用者自訂備註
*   為什麼收藏這篇
*   與哪個專案有關

### 18.3 Semantic Knowledge Layer

*   embedding
*   vector search
*   related items
*   topic clusters

### 18.4 AI Knowledge Assistant

*   自然語言問答
*   主題彙整
*   自動整理 weekly review
*   自動生成筆記草稿

* * *

19\. 設計總結
---------

本系統採用「收錄 → 解析 → AI 分析 → 儲存 → 查詢」的核心流程，並以模組化單體架構作為 MVP 階段的設計基礎。此設計兼顧快速落地與後續擴充能力，能先解決使用者最核心的問題：將零散收藏的連結轉換為可搜尋、可管理、可回顧的私人知識資產。

