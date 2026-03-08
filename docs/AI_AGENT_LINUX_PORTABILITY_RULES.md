# 個人知識平台開發

AI\_AGENT\_LINUX\_PORTABILITY\_RULES.md
=======================================

文件目的
----

本文件定義 AI Agent（如 Codex）在本專案開發時，必須遵守的 Linux 可移植性規範。  
目標是確保本專案雖然目前在 Windows 10 + WSL 2 環境中開發，但未來可順利部署與遷移到真正的 Linux 主機，而不需大幅修改程式碼、腳本或部署流程。

本文件適用於：

*   後端程式碼
*   前端程式碼
*   Docker 與部署設定
*   腳本與工具鏈
*   路徑與檔案操作
*   開發環境相關設定

* * *

核心原則
----

### 規則 1：一律以 Linux 為第一目標環境

所有實作、腳本、路徑、依賴與執行方式，必須優先假設目標環境是原生 Linux，而不是 Windows。

**要求：**

*   不可把 Windows 當成預設執行平台
*   不可撰寫只適用於 Windows 的核心流程
*   所有重要工作流都必須可在 Linux shell 中執行

* * *

### 規則 2：禁止依賴 Windows 專屬路徑

不得在程式碼、設定檔、腳本或文件中硬編碼 Windows 路徑，例如：

*   `C:\\Users\\...`
*   `D:\\project\\...`
*   `/mnt/c/...`

**要求：**

*   使用相對路徑
*   使用環境變數
*   使用 Linux 可攜式路徑處理方式

* * *

### 規則 3：所有腳本優先使用 Bash，不使用 `.bat` 或 PowerShell

部署、啟動、測試、資料初始化等腳本，應優先提供 Bash 版本。

**要求：**

*   使用 `.sh`
*   使用 POSIX / Bash 相容語法
*   不以 PowerShell 作為主要腳本格式
*   若提供 PowerShell，必須是附加選項，不得是唯一版本

* * *

### 規則 4：專案內的服務優先容器化

凡是可容器化的服務，應優先透過 Docker 執行，以降低環境差異。

**適用對象：**

*   PostgreSQL
*   Redis
*   Celery worker
*   backend
*   frontend

**要求：**

*   優先提供 `Dockerfile`
*   優先提供 `docker compose` 啟動方式
*   不假設使用者已在本機手動安裝資料庫或 Redis

* * *

### 規則 5：不要依賴 WSL 特有行為

不得使用只在 WSL 中可行、但在真正 Linux 主機上不成立的行為作為正式方案。

**例如：**

*   依賴 `/mnt/c/...`
*   依賴可直接呼叫 Windows 可執行檔
*   依賴 WSL 自動掛載 Windows 磁碟
*   依賴 Windows GUI 程式參與核心流程

* * *

### 規則 6：所有環境設定必須外部化

所有可變設定都必須放入環境變數，不得寫死在程式碼中。

**至少包含：**

*   資料庫連線字串
*   Redis 位置
*   API key
*   secret key
*   host / port
*   log level
*   app environment

**要求：**

*   提供 `.env.example`
*   程式讀取 `.env`
*   不得提交真實敏感資訊

* * *

### 規則 7：依賴清單必須完整且可重建

所有執行環境依賴必須能透過檔案重建，不得依賴開發者「手動記憶安裝過什麼」。

**要求：**

*   Python 使用 `requirements.txt` 或 `pyproject.toml`
*   Node 使用 `package.json`
*   Docker 映像使用 `Dockerfile`
*   DB schema 使用 migration
*   不允許「口頭依賴」

* * *

### 規則 8：資料庫結構變更必須使用 migration

任何資料表、欄位或索引變更，都必須透過 migration 管理。

**要求：**

*   不直接手動改 production schema
*   不依賴本機資料庫的偶然狀態
*   migration 必須可在 Linux 主機執行

* * *

### 規則 9：避免使用大小寫不敏感的檔名假設

Windows 檔案系統常對大小寫較寬鬆，但 Linux 對大小寫敏感。

**要求：**

*   匯入模組時，檔名大小寫必須完全一致
*   不得同時存在容易混淆的檔名
*   不可依賴 Windows 對大小寫的寬容行為

* * *

### 規則 10：避免 CRLF / LF 問題

所有程式碼與腳本預設應使用 Linux 友善的換行格式。

**要求：**

*   優先使用 LF
*   shell script 不得以 CRLF 儲存
*   不得讓 Bash 腳本因行尾格式錯誤而失效

* * *

### 規則 11：所有檔案權限需求必須明確

如果某腳本需要可執行權限，必須在 repo 中明確管理，而不是依靠手動修正。

**要求：**

*   shell script 應正確設置執行權限
*   Docker / entrypoint 腳本需可在 Linux 上直接執行
*   不得假設 Windows 不看權限就代表 Linux 也沒問題

* * *

### 規則 12：不得把本機絕對路徑當成應用設定

不得在應用程式中假設固定目錄存在，例如：

*   `/home/user/...`
*   `/root/...`
*   `/mnt/c/...`

**要求：**

*   用環境變數指定資料目錄
*   用相對路徑處理 repo 內檔案
*   可配置 upload / cache / logs 路徑

* * *

### 規則 13：服務啟動方式必須可在 Linux 上無互動執行

所有服務都必須能以非互動方式啟動，不能依賴 GUI 點擊或人工操作。

**要求：**

*   可透過 `docker compose up`
*   或可透過明確 CLI 指令啟動
*   不依賴 Windows 視窗操作
*   不依賴手動開某個桌面程式才能運作

* * *

### 規則 14：避免使用僅 Windows 可用的工具作為必要前置

若某工具只有 Windows 版，則不能成為專案開發或部署的必要條件。

**要求：**

*   優先使用跨平台工具
*   優先使用 CLI 工具
*   若某工具僅為 Windows 輔助工具，需標明為 optional

* * *

### 規則 15：測試必須在 Linux 風格環境可執行

所有測試流程都應能在 WSL / Linux shell 中執行。

**要求：**

*   backend test 可用 Linux CLI 執行
*   frontend build/test 可用 Linux CLI 執行
*   不得只提供 Windows IDE 專用測試方式

* * *

### 規則 16：日誌、暫存與資料輸出目錄需可配置

程式不得把 log、cache、temp、export 檔案寫死到特定本機目錄。

**要求：**

*   使用環境變數或設定檔指定
*   預設路徑需為 Linux 合理位置
*   若寫入 repo 外部目錄，必須可配置

* * *

### 規則 17：網路設定與主機名稱不得綁死本機環境

不得把 `localhost`、固定 IP、固定網卡名稱寫死成無法移植的部署假設。

**要求：**

*   host / port 使用環境變數控制
*   service name 優先以 Docker Compose service 名稱為準
*   不假設特定 Windows 網路設定存在

* * *

### 規則 18：背景工作、排程與服務角色要分離

應用程式中的 web、worker、scheduler 等角色，必須可在 Linux 主機上各自獨立啟動。

**要求：**

*   backend API 可單獨啟動
*   Celery worker 可單獨啟動
*   scheduler 若存在也應可單獨啟動
*   不要把所有角色硬塞進單一互動式啟動流程

* * *

### 規則 19：文件中的指令以 Linux / WSL 指令為主

所有 README、設置文件、部署文件中的主要命令應以 Linux shell 為主。

**要求：**

*   優先提供 Bash 指令
*   若提供 Windows 指令，應作為補充
*   對部署相關指令，一律先寫 Linux 版

* * *

### 規則 20：每次新增功能時，都要檢查 Linux 可移植性

AI Agent 在實作任何新功能前後，都必須主動檢查是否違反本文件規則。

**實作要求：**  
在每次完成變更後，Agent 必須自我檢查以下問題：

1.  是否引入 Windows 專屬路徑？
2.  是否新增只能在 Windows 執行的腳本？
3.  是否依賴 WSL 特有行為？
4.  是否漏了 `.env.example`、migration、Docker 或依賴檔更新？
5.  是否可在真正 Linux 主機重建與執行？

若答案有任何一項為「是」或「不確定」，不得直接視為完成，必須先修正。

* * *

### 規則 21：後端基礎服務預設必須容器化
在本專案中，PostgreSQL 與 Redis 屬於後端基礎服務。AI Agent 在設計、實作、文件撰寫與啟動流程規劃時，必須預設這些服務由 Docker Compose 提供，而不是依賴開發者手動在 WSL、本機 Linux 或 Windows 上安裝服務。

**要求：**
- PostgreSQL 與 Redis 應優先定義在 `docker-compose.yml` 中
- backend、worker 與其他相依服務應透過 Docker network service name 連線
- 不得把「先手動安裝 PostgreSQL / Redis」當成主要 setup 流程
- `.env.example` 應反映容器化的預設連線方式
- 文件中的主要啟動指令應以 Docker Compose 為準

**例外情況：**
若因特殊整合、效能測試、外部託管資料庫或明確需求而不使用容器，Agent 必須在文件與回報中清楚說明原因，且不得將該例外方案寫成預設架構。

* * *

### 規則 22：容器間連線不得預設使用 localhost
若 backend、worker、PostgreSQL、Redis 皆透過 Docker Compose 執行，服務之間的預設連線應使用 Compose service name，而不是 `localhost`。

**要求：**
- PostgreSQL 連線主機應預設為例如 `postgres`
- Redis 連線主機應預設為例如 `redis`
- 不得將 `localhost` 寫死為容器間通訊的預設值
- 若需支援本機直連模式，必須透過環境變數切換

* * *

Agent 執行指令
----------

當 Agent 在本專案中進行實作時，必須遵守以下流程：

### 開始實作前

1.  先讀取 `AGENTS.md`
2.  再讀取：
    *   `docs/PRD.md`
    *   `docs/requirements.md`
    *   `docs/design.md`
    *   `docs/tasks.md`
    *   `docs/AI_AGENT_LINUX_PORTABILITY_RULES.md`

### 實作中

1.  以 Linux-first 方式做設計
2.  優先使用 Docker / Compose / Bash / `.env`
3.  不得引入 Windows-only 依賴作為核心方案

### 完成後回報時

每次都必須附上一段 Linux 可移植性檢查摘要，至少回答：

*   本次是否新增任何 Windows 專屬依賴？
*   本次是否新增任何不可移植路徑？
*   本次是否需要更新 Docker、env、migration 或腳本？
*   本次變更是否可直接在 Linux 主機執行？

* * *
