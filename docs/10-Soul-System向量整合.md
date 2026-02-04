# 🧠 Soul System 向量整合指南

> **向量檢索標籤**：`soul-system`, `vector`, `memory`, `search`, `向量`, `記憶`
> **資料來源**：第 1 輪多代理搜尋精煉

---

## 📋 Soul System 概述

Soul System 是思維熔爐的核心記憶系統，提供：
- 長期記憶儲存
- 向量檢索能力
- 多代理記憶共享
- 人格設定管理

---

## 🗂️ 目錄結構

```
~/Documents/思維熔爐/
├── soul_core/
│   └── app/
│       ├── db.py           # 資料庫連接
│       ├── config.py       # 配置管理
│       ├── models.py       # 資料模型
│       ├── schema.sql      # 資料庫結構
│       └── clawbot/        # 機器人整合
│           ├── app.py
│           ├── telegram_handler.py
│           └── line_handler.py
├── credentials/            # 憑證管理
│   ├── credential_manager.py
│   ├── api_key_router.py
│   └── sa_router.py
├── core/                   # 核心文檔
│   ├── THOUGHT_FORGE.md    # 思維熔爐
│   └── XIAODI_SOUL.md      # 小滴靈魂
└── data/
    └── soul_api.db         # Soul API 資料庫
```

---

## 🔌 Soul API 端點

### 基本資訊

| 項目 | 值 |
|------|-----|
| **位址** | `localhost:8531` |
| **協議** | HTTP REST |
| **格式** | JSON |

### 端點列表

| 端點 | 方法 | 用途 |
|------|------|------|
| `/soul/query` | POST | 查詢記憶 |
| `/soul/store` | POST | 儲存記憶 |
| `/soul/search` | POST | 向量搜尋 |
| `/soul/tags` | GET | 取得所有標籤 |
| `/health` | GET | 健康檢查 |

---

## 📝 API 使用範例

### 查詢記憶

```bash
curl -X POST http://localhost:8531/soul/query \
  -H "Content-Type: application/json" \
  -d '{"query": "OpenClaw 部署方式"}'
```

**回應格式**：
```json
{
  "success": true,
  "results": [
    {
      "id": "mem_123",
      "content": "OpenClaw 支援 npm 和 Docker 兩種部署方式...",
      "tags": ["openclaw", "deployment"],
      "score": 0.92,
      "created_at": "2026-02-04T12:00:00Z"
    }
  ]
}
```

### 儲存記憶

```bash
curl -X POST http://localhost:8531/soul/store \
  -H "Content-Type: application/json" \
  -d '{
    "content": "OpenClaw 部署專案已完成",
    "tags": ["openclaw", "deployment", "completed"],
    "metadata": {"project": "openclaw-deployment"}
  }'
```

### 向量搜尋

```bash
curl -X POST http://localhost:8531/soul/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "如何配置多模型",
    "top_k": 5,
    "threshold": 0.7
  }'
```

---

## 🔗 與 OpenClaw 部署專案整合

### 向量標籤設計

本專案使用以下向量標籤供 Soul System 檢索：

```yaml
vector_tags:
  # 主題標籤
  - openclaw
  - deployment
  - mcp
  
  # 功能標籤
  - installation
  - docker
  - npm
  - multi-model
  - skills
  - memory
  - security
  
  # 中文標籤
  - 部署
  - 安裝
  - 教學
  - 礁島學習
```

### 文檔格式優化

為支援向量檢索，文檔採用以下格式：

1. **標題層級明確**：使用 H1-H3 層級
2. **段落適中**：每段 100-300 字
3. **標籤明確**：每份文檔開頭標註向量標籤
4. **語意完整**：每段可獨立理解

---

## 🗃️ 資料庫結構

### Soul API 資料庫（SQLite）

```sql
-- 記憶表
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    embedding BLOB,
    tags TEXT,  -- JSON array
    metadata TEXT,  -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- 標籤索引
CREATE INDEX idx_memories_tags ON memories(tags);

-- 向量索引（使用 sqlite-vec 擴展）
CREATE VIRTUAL TABLE vec_memories USING vec0(
    id TEXT PRIMARY KEY,
    embedding FLOAT[1536]
);
```

### 連接配置

```python
# db.py 配置模式
conn = sqlite3.connect(settings.db_path, check_same_thread=False)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA synchronous=NORMAL;")
conn.execute("PRAGMA busy_timeout=5000;")
conn.execute("PRAGMA foreign_keys=ON;")
```

---

## 🔧 整合步驟

### 步驟 1：確認 Soul API 運行

```bash
curl http://localhost:8531/health
```

### 步驟 2：索引文檔

```python
import requests
from pathlib import Path

def index_document(doc_path: str):
    """將文檔索引到 Soul System"""
    content = Path(doc_path).read_text()
    
    # 提取標籤
    tags = extract_tags(content)
    
    # 儲存到 Soul System
    response = requests.post(
        "http://localhost:8531/soul/store",
        json={
            "content": content,
            "tags": tags,
            "metadata": {
                "source": doc_path,
                "project": "openclaw-deployment"
            }
        }
    )
    return response.json()

# 索引所有文檔
docs_path = Path("~/Documents/思維熔爐/openclaw-deployment/docs")
for doc in docs_path.glob("*.md"):
    index_document(str(doc))
```

### 步驟 3：查詢測試

```python
def test_search():
    """測試向量搜尋"""
    response = requests.post(
        "http://localhost:8531/soul/search",
        json={
            "query": "OpenClaw Docker 部署",
            "top_k": 3
        }
    )
    results = response.json()
    
    for r in results["results"]:
        print(f"Score: {r['score']:.2f}")
        print(f"Content: {r['content'][:100]}...")
        print("---")
```

---

## 📊 統一憑證中心整合

Soul System 使用統一憑證中心管理 API Keys：

### 憑證配置

| 服務 | 數量 | 用途 |
|------|------|------|
| Gemini API Keys | 25 個 | 向量嵌入 |
| OpenAI API Keys | 2 個 | 備用嵌入 |
| Service Accounts | 13 個 | GCP 服務 |

### 金鑰輪替

```python
from credential_manager import get_api_key

# 自動輪替取得可用金鑰
api_key = get_api_key("gemini", strategy="round-robin")
```

---

## ⚠️ 注意事項

### 向量維度

- **Gemini Embedding**: 768 維
- **OpenAI Embedding**: 1536 維
- 確保使用相同模型進行索引和查詢

### 效能優化

1. **批量索引**：一次索引多份文檔
2. **快取結果**：高頻查詢使用快取
3. **分片存儲**：大量資料分片處理

### 資料同步

- Soul API 資料庫位於：`~/Documents/思維熔爐/data/soul_api.db`
- 定期備份重要記憶
- 使用 WAL 模式確保一致性

---

*文檔版本：1.0*
*資料來源：Soul System 程式碼分析*
