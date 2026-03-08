tasks.md
========

專案名稱
----

**Personal Knowledge Platform（個人知識平台）**

* * *

1\. 文件目的
--------

本文件用於將 `requirements.md` 與 `design.md` 中定義的需求與設計，拆解為可執行的開發任務。  
任務拆解以 **MVP 優先** 為原則，先完成最小可用版本，再逐步擴充第二階段功能。

* * *

2\. 開發原則
--------

1.  優先完成從「貼上 URL → 自動解析 → AI 摘要 → 列表展示 → 搜尋」的核心閉環。
2.  先以單人私人使用場景為目標，不過早處理多使用者複雜度。
3.  優先採用模組化單體架構，避免過早微服務化。
4.  將高風險功能（如社群內容擷取、LLM 回傳穩定性）獨立處理與驗證。
5.  任務應盡量拆成小而可驗證的單位。

* * *

3\. 里程碑規劃
---------

* * *

### Milestone 1：專案初始化與基礎架構

目標：建立開發基礎，完成專案骨架、資料庫與基本部署環境。

### Milestone 2：URL 收錄與背景任務流程

目標：完成使用者送入連結、系統建立條目與背景任務排程。

### Milestone 3：內容解析與 AI 分析

目標：完成網頁解析、摘要、關鍵字、分類。

### Milestone 4：前端 MVP 介面

目標：完成新增頁、列表頁、詳細頁、Dashboard。

### Milestone 5：搜尋與驗收

目標：完成搜尋、篩選、錯誤處理與 MVP 驗收。

### Milestone 6：第二階段擴充（非 MVP）

目標：加入語意搜尋、個人註記、分享整合等進階功能。

* * *

4\. 任務總覽結構
----------

本文件將任務分為以下幾大類：

1.  專案初始化
2.  後端 API
3.  資料庫
4.  背景任務與佇列
5.  Parser 與內容擷取
6.  AI 分析模組
7.  搜尋模組
8.  前端 UI
9.  例外處理與觀測性
10.  部署與環境設定
11.  測試與驗收
12.  第二階段擴充

* * *

5\. 任務清單
========

* * *

A. 專案初始化任務
----------

### A-001 建立專案目錄結構

**說明**  
建立前端、後端、資料庫、部署設定等基本目錄結構。

**驗收標準**

*   目錄結構清楚
*   frontend / backend / infra 等資料夾已建立
*   README 初版存在

* * *

### A-002 建立 Git repository 與版本控制規範

**說明**  
初始化 Git 專案，建立基本 `.gitignore`、branch 策略與 commit 規範。

**驗收標準**

*   Git repository 已建立
*   `.gitignore` 已包含 Python、Node、env、build artifacts
*   有基本 commit message 規範說明

* * *

### A-003 建立開發環境設定文件

**說明**  
整理本地開發所需工具與啟動步驟。

**驗收標準**

*   README 中有安裝與啟動說明
*   包含前端、後端、DB、Redis 啟動方式

* * *

### A-004 建立 Docker Compose 開發環境

**說明**  
建立 docker-compose 設定，至少能啟動：

*   PostgreSQL
*   Redis
*   backend
*   frontend

**驗收標準**

*   `docker compose up` 可成功啟動主要服務
*   各服務間網路可互通

* * *

B. 後端 API 任務
------------

### B-001 初始化 FastAPI 專案

**說明**  
建立 FastAPI 專案骨架，包含 routers、schemas、services、models、config。

**驗收標準**

*   FastAPI 可成功啟動
*   有 `/health` endpoint
*   有基本專案模組結構

* * *

### B-002 建立設定管理模組

**說明**  
建立環境變數管理，例如：

*   DB URL
*   Redis URL
*   OpenAI API Key
*   App environment

**驗收標準**

*   可透過 `.env` 載入設定
*   有 config module
*   敏感資訊不寫死在程式碼中

* * *

### B-003 建立共用 API 回應格式

**說明**  
統一 API success / error response 格式，方便前後端整合。

**驗收標準**

*   成功與失敗回應格式一致
*   有錯誤碼或 message 欄位

* * *

### B-004 建立新增 URL API

**說明**  
實作 `POST /api/items`，接收網址並建立初始條目。

**驗收標準**

*   可接收 URL
*   會驗證 URL 格式
*   會建立初始 knowledge item
*   回傳 item id 與狀態

* * *

### B-005 建立條目列表 API

**說明**  
實作 `GET /api/items`，支援列表查詢與分頁。

**驗收標準**

*   可回傳 items 清單
*   支援 page / page\_size
*   支援基本排序

* * *

### B-006 建立單筆條目 API

**說明**  
實作 `GET /api/items/{id}`。

**驗收標準**

*   可依 id 取得單筆條目
*   回傳完整資料欄位
*   不存在時回傳 404

* * *

### B-007 建立 Dashboard API

**說明**  
實作 `GET /api/dashboard`。

**驗收標準**

*   回傳總收藏數
*   回傳最近新增數
*   回傳最新條目
*   回傳分類統計
*   回傳狀態統計

* * *

### B-008 建立重新處理條目 API

**說明**  
實作 `POST /api/items/{id}/reprocess`。

**驗收標準**

*   可對 failed 或指定條目重新排入處理流程
*   狀態正確更新

* * *

C. 資料庫任務
--------

### C-001 建立資料庫 migration 機制

**說明**  
導入 Alembic 或其他 migration 工具。

**驗收標準**

*   可以建立 migration
*   可以升級與回滾 schema

* * *

### C-002 建立 knowledge\_items 資料表

**說明**  
建立主資料表，包含條目核心欄位。

**驗收標準**

*   資料表欄位符合 design.md
*   能成功 CRUD

* * *

### C-003 建立 ingestion\_logs 資料表

**說明**  
建立處理歷程與錯誤紀錄表。

**驗收標準**

*   可記錄 parsing / analyzing / failed 等事件
*   與 knowledge\_items 關聯正確

* * *

### C-004 建立索引與唯一約束

**說明**  
為常用欄位建立索引，例如：

*   source\_url
*   captured\_at
*   processing\_status
*   category

**驗收標準**

*   URL 唯一性規則已定義
*   常用查詢欄位已加索引

* * *

### C-005 建立全文搜尋欄位設計

**說明**  
規劃 PostgreSQL Full Text Search 所需欄位，例如 tsvector。

**驗收標準**

*   有 searchable document 欄位或更新機制
*   可供後續搜尋使用

* * *

D. 背景任務與佇列任務
------------

### D-001 建立 Celery 或 RQ worker

**說明**  
建立背景任務執行機制。

**驗收標準**

*   worker 可啟動
*   能接收並執行測試任務

* * *

### D-002 建立任務狀態更新機制

**說明**  
背景任務開始、成功、失敗時，自動更新 knowledge item 狀態。

**驗收標準**

*   `received → queued → parsing → parsed → analyzing → ready` 可正常流轉
*   失敗時改為 `failed`

* * *

### D-003 建立 parse\_url\_job

**說明**  
建立解析 URL 的背景任務。

**驗收標準**

*   任務可接收 item id
*   能觸發對應 parser
*   能儲存解析結果

* * *

### D-004 建立 enrich\_content\_job

**說明**  
建立 AI 分析背景任務。

**驗收標準**

*   任務能讀取解析後內容
*   能呼叫 LLM
*   能儲存摘要、分類、關鍵字

* * *

### D-005 建立任務重試機制

**說明**  
對暫時性失敗（如 API timeout）加入 retry。

**驗收標準**

*   任務失敗可自動重試
*   重試上限可配置
*   最終失敗有清楚 log

* * *

E. Parser 與內容擷取任務
-----------------

### E-001 建立 BaseParser 介面

**說明**  
設計 parser 抽象層。

**驗收標準**

*   有統一 parser interface
*   可由 factory 或 registry 選擇對應 parser

* * *

### E-002 建立 GenericWebParser

**說明**  
解析一般文章頁面。

**驗收標準**

*   可抓 title、description
*   可抓主要正文
*   可輸出 cleaned\_content

* * *

### E-003 建立 YouTubeParser

**說明**  
處理 YouTube 連結，擷取：

*   title
*   description
*   thumbnail
*   transcript（若可取得）

**驗收標準**

*   可辨識 YouTube URL
*   可成功擷取基本資料
*   若 transcript 無法取得，需有 fallback 行為

* * *

### E-004 建立 FacebookParser 初版

**說明**  
先做可行範圍的 metadata 擷取。

**驗收標準**

*   可辨識 Facebook URL
*   至少可擷取 title / description / og metadata
*   明確記錄抓不到正文時的限制

* * *

### E-005 建立 ThreadsParser 初版

**說明**  
先做 Threads 的 metadata 與可行內容擷取。

**驗收標準**

*   可辨識 Threads URL
*   至少可擷取基本 metadata
*   失敗時有錯誤紀錄

* * *

### E-006 建立 parser factory / router

**說明**  
根據網址 domain 選擇 parser。

**驗收標準**

*   對不同來源會選到正確 parser
*   無對應來源時 fallback 到 GenericWebParser

* * *

### E-007 建立內容清洗與正規化流程

**說明**  
移除雜訊、過多空白、腳本殘留與無關段落。

**驗收標準**

*   cleaned\_content 可讀性明顯優於 raw content
*   不會留下大量 HTML 垃圾字串

* * *

F. AI 分析模組任務
------------

### F-001 建立 LLM client 封裝

**說明**  
將 OpenAI API 呼叫包成獨立 service。

**驗收標準**

*   API 呼叫不散落在業務邏輯中
*   可統一設定 model / timeout / retry

* * *

### F-002 設計 enrichment prompt

**說明**  
設計單一或多段 prompt，讓 LLM 產出：

*   short\_summary
*   full\_summary（可選）
*   keywords
*   category
*   content\_type

**驗收標準**

*   Prompt 輸出格式明確
*   有 category 候選集合或規則
*   支援中文輸出

* * *

### F-003 建立 LLM JSON 輸出 parser

**說明**  
驗證並解析 LLM 回傳 JSON。

**驗收標準**

*   可處理格式正確情況
*   對格式異常有 fallback / retry
*   可記錄錯誤訊息

* * *

### F-004 建立摘要生成流程

**說明**  
整合解析內容與 LLM，產生短摘要。

**驗收標準**

*   short\_summary 可成功寫入資料庫
*   中文內容摘要品質可接受

* * *

### F-005 建立關鍵字產生流程

**說明**  
從內容中產生關鍵字。

**驗收標準**

*   關鍵字數量合理
*   不全是空泛詞彙
*   可寫入資料庫

* * *

### F-006 建立分類流程

**說明**  
由 LLM 或規則分類內容。

**驗收標準**

*   category 能落在預設類別集
*   分類結果穩定

* * *

### F-007 建立超長內容處理策略

**說明**  
對過長文本做 truncate 或 chunking。

**驗收標準**

*   不因超長內容導致 API 失敗
*   有最大字數控制策略

* * *

G. 搜尋模組任務
---------

### G-001 建立全文搜尋資料更新機制

**說明**  
在條目 ready 後，更新搜尋欄位。

**驗收標準**

*   title、summary、keywords、content 會被納入搜尋內容

* * *

### G-002 建立關鍵字搜尋 API 支援

**說明**  
讓 `GET /api/items?q=...` 可搜尋。

**驗收標準**

*   輸入關鍵字可回傳對應條目
*   搜尋結果排序合理

* * *

### G-003 建立多條件篩選

**說明**  
支援 platform、category、status、date range 篩選。

**驗收標準**

*   可多條件同時使用
*   查詢結果正確

* * *

### G-004 建立搜尋結果排序

**說明**  
支援：

*   最新優先
*   最舊優先
*   相關性優先

**驗收標準**

*   API 可指定 sort 參數
*   前端可切換排序方式

* * *

H. 前端 UI 任務
-----------

### H-001 初始化前端專案

**說明**  
建立 Next.js 或 React 專案骨架。

**驗收標準**

*   前端可啟動
*   有基本 layout 與 routing

* * *

### H-002 建立全域版型與導航

**說明**  
建立頁首、側邊欄或主要導航。

**驗收標準**

*   至少可導向 Dashboard、Items、Add Item

* * *

### H-003 建立新增 URL 頁面

**說明**  
提供簡單表單讓使用者提交 URL。

**驗收標準**

*   可輸入 URL
*   可送出到 API
*   成功後顯示提示

* * *

### H-004 建立列表頁

**說明**  
顯示所有知識條目。

**驗收標準**

*   可顯示 title、summary、platform、category、status、captured\_at
*   支援分頁

* * *

### H-005 建立詳細頁

**說明**  
顯示單筆條目完整資訊。

**驗收標準**

*   顯示原始連結
*   顯示摘要
*   顯示關鍵字與分類
*   顯示 cleaned\_content
*   顯示狀態

* * *

### H-006 建立 Dashboard 頁面

**說明**  
顯示系統總覽資訊。

**驗收標準**

*   可顯示總收藏數
*   可顯示最近新增
*   可顯示最新條目
*   可顯示分類統計

* * *

### H-007 建立搜尋與篩選 UI

**說明**  
在列表頁加入搜尋框與篩選器。

**驗收標準**

*   可搜尋關鍵字
*   可依平台、分類、狀態篩選
*   可改變排序

* * *

### H-008 建立狀態顯示與錯誤提示

**說明**  
在前端清楚顯示 parsing / analyzing / ready / failed。

**驗收標準**

*   使用者可辨識條目目前狀態
*   failed 條目可顯示基本錯誤訊息

* * *

### H-009 建立空狀態與 loading 狀態

**說明**  
處理無資料、載入中、查無結果的畫面。

**驗收標準**

*   空狀態不會顯得壞掉
*   loading 有明確提示

* * *

I. 例外處理與觀測性任務
-------------

### I-001 建立後端 logging 機制

**說明**  
統一記錄 API、task、parser、AI 模組日誌。

**驗收標準**

*   有結構化 log 或至少模組化 log
*   可辨識錯誤來源

* * *

### I-002 建立 ingestion\_logs 寫入流程

**說明**  
每個關鍵節點寫入處理紀錄。

**驗收標準**

*   收錄、解析、分析、失敗都有 log
*   可追蹤處理歷程

* * *

### I-003 建立錯誤分類機制

**說明**  
將錯誤區分為：

*   invalid\_url
*   parse\_failed
*   llm\_failed
*   duplicate\_url
*   unknown\_error

**驗收標準**

*   error\_message 與 error type 有一致規則

* * *

### I-004 建立失敗條目重試流程

**說明**  
在前後端支援重新處理 failed item。

**驗收標準**

*   failed item 可重新執行
*   重試後狀態正確更新

* * *

J. 部署與環境設定任務
------------

### J-001 建立 backend Dockerfile

**說明**  
為 FastAPI 建立容器映像。

**驗收標準**

*   可成功 build
*   容器可啟動 API server

* * *

### J-002 建立 frontend Dockerfile

**說明**  
為前端建立容器映像。

**驗收標準**

*   可成功 build
*   容器可啟動前端應用

* * *

### J-003 建立生產環境 docker-compose 範本

**說明**  
整理部署所需 compose 檔案。

**驗收標準**

*   可用於 VPS / 本機私有部署
*   包含 env example

* * *

### J-004 建立環境變數範本

**說明**  
提供 `.env.example`。

**驗收標準**

*   所有必要環境變數皆列出
*   不含真實敏感資訊

* * *

K. 測試與驗收任務
----------

### K-001 建立後端單元測試基礎

**說明**  
為 service、parser、API 建立測試框架。

**驗收標準**

*   可執行 pytest 或等效工具
*   至少有基本 smoke tests

* * *

### K-002 建立 parser 測試案例

**說明**  
針對 GenericWebParser、YouTubeParser 做測試。

**驗收標準**

*   輸入測試網址可得到預期欄位
*   失敗情況可正確處理

* * *

### K-003 建立 API 測試

**說明**  
測試新增 URL、列表、詳細頁、dashboard。

**驗收標準**

*   核心 API 有自動化測試
*   回應格式符合預期

* * *

### K-004 建立前端基本互動測試

**說明**  
測試新增 URL、列表載入、詳細頁顯示。

**驗收標準**

*   主要頁面可通過 smoke test

* * *

### K-005 MVP 驗收測試

**說明**  
根據 requirements.md 驗收。

**驗收標準**

*   可成功新增 URL
*   可自動產出摘要與分類
*   可於列表頁看到條目
*   可搜尋到既有內容
*   可於 dashboard 看到統計資訊

* * *

6\. 第二階段擴充任務
============

* * *

L. 個人知識深化功能
-----------

### L-001 建立使用者註記欄位

**說明**  
讓使用者補上「為什麼收藏這篇」。

### L-002 建立星號 / 重點標記功能

**說明**  
可標記特別重要條目。

### L-003 建立已讀 / 已整理狀態

**說明**  
支援知識整理流程狀態管理。

* * *

M. 語意搜尋與向量功能
------------

### M-001 建立 embedding 生成流程

### M-002 建立 pgvector 或向量資料庫整合

### M-003 建立語意搜尋 API

### M-004 建立相似內容推薦功能

* * *

N. 分享整合功能
---------

### N-001 設計 iOS / 手機分享流程

### N-002 建立 LINE Bot 收錄入口

### N-003 建立瀏覽器 extension 初版

* * *

O. AI 知識助理功能
------------

### O-001 建立自然語言問答 API

### O-002 建立主題彙整功能

### O-003 建立每週回顧摘要功能

### O-004 建立「根據收藏生成筆記草稿」功能

* * *

7\. 建議 Issue 標籤分類
=================

之後如果你要丟進 GitHub Issues，我建議用這些 labels：

*   `backend`
*   `frontend`
*   `database`
*   `infra`
*   `ai`
*   `parser`
*   `search`
*   `bug`
*   `enhancement`
*   `mvp`
*   `phase-2`
*   `high-priority`
*   `low-priority`

* * *

8\. 建議開發優先順序
============

若要最務實地開始做，我建議順序是：

### 第一批先做

*   A-001 ~ A-004
*   B-001 ~ B-004
*   C-001 ~ C-003
*   D-001 ~ D-004
*   E-001, E-002, E-006, E-007
*   F-001 ~ F-004
*   H-001, H-003, H-004, H-005

這樣就能先跑出最核心的主流程。

### 第二批再做

*   B-005 ~ B-008
*   C-004 ~ C-005
*   E-003 ~ E-005
*   F-005 ~ F-007
*   G-001 ~ G-004
*   H-006 ~ H-009
*   I 系列
*   K 系列

* * *

9\. MVP 完成定義（Definition of Done）
================================

以下條件皆成立時，可視為 MVP 完成：

1.  使用者可手動貼上 URL。
2.  系統能建立條目並背景處理。
3.  系統能成功解析一般文章內容。
4.  系統能透過 AI 產生摘要、關鍵字與分類。
5.  系統能展示條目列表與單筆詳細頁。
6.  系統能提供基本 dashboard。
7.  系統能用關鍵字搜尋已收錄內容。
8.  失敗條目有清楚狀態與可重試機制。
9.  專案可透過 Docker Compose 啟動。

* * *

10\. 總結
=======

本 `tasks.md` 的目的，是把個人知識平台專案從概念、需求與設計，進一步拆成能夠逐步執行的實作任務。  
MVP 階段應聚焦在最核心的知識收錄閉環，不過早加入過多高階功能，確保你能先做出真正可用、可驗證、可持續演進的第一版系統。

* * *

如果你要，我下一步最適合接著做的是其中一個：

1.  幫你把這三份整合成 **完整 PRD 文件**
2.  幫你產出 **專案目錄結構範本**
3.  幫你直接寫 **GitHub Issues 版本的任務清單**
4.  幫你繼續寫 **資料表 schema 與 FastAPI/Next.js 專案骨架**



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)