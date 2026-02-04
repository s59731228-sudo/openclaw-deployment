---
name: openclaw-deployment
description: "🦞 OpenClaw 部署教學 - 教導學習 | 提供資訊 | MCP 直接實現（礁島學習系統）"
metadata:
  {
    "soul_system": true,
    "vector_search": true,
    "mcp_enabled": true,
    "language": "zh-TW",
    "version": "1.2"
  }
---

# 🦞 OpenClaw 部署教學（礁島學習系統）

> **中文備註**：此技能用於教導 OpenClaw 部署，支援向量檢索，可透過 MCP 直接執行操作
> **使用方式**：`/skill openclaw-deployment` 或在對話中提及 OpenClaw 部署相關問題
> **所屬系統**：Soul System > 礁島學習

---

## 🎯 技能三大功能

| 功能 | 說明 | 觸發方式 |
|------|------|----------|
| 1️⃣ 教導學習 | 回答 OpenClaw 相關問題 | 提問即可 |
| 2️⃣ 提供資訊 | 從知識庫檢索文檔 | `openclaw_docs("主題")` |
| 3️⃣ MCP 實現 | 直接執行操作 | 呼叫 MCP 工具 |

---

## 🔧 MCP 工具完整參數說明

### 工具一：`openclaw_install` - 安裝 OpenClaw

```python
openclaw_install(method: str = "npm") -> dict
```

| 參數 | 類型 | 必填 | 預設值 | 選項 | 說明 |
|------|------|------|--------|------|------|
| `method` | str | 否 | `"npm"` | `"npm"`, `"docker"` | 安裝方式 |

**調用範例**：
```python
openclaw_install()           # npm 安裝（預設）
openclaw_install("npm")      # npm 安裝
openclaw_install("docker")   # Docker 安裝
```

---

### 工具二：`openclaw_health` - 健康檢查

```python
openclaw_health() -> dict
```

| 參數 | 說明 |
|------|------|
| （無參數） | 自動檢查所有項目 |

**調用範例**：
```python
openclaw_health()  # 執行全面健康檢查
```

**檢查項目**：Node.js 版本、OpenClaw 安裝、API 金鑰、系統診斷

---

### 工具三：`openclaw_config` - 配置管理

```python
openclaw_config(action: str = "show", key: str = None, value: str = None) -> dict
```

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `action` | str | 否 | `"show"` | `"show"` / `"get"` / `"set"` |
| `key` | str | 條件 | `None` | 配置鍵（get/set 必填） |
| `value` | str | 條件 | `None` | 配置值（set 必填） |

**調用範例**：
```python
openclaw_config("show")                              # 顯示所有配置
openclaw_config("get", "models.default")             # 取得預設模型
openclaw_config("set", "gateway.port", "18790")      # 設定端口
```

**常用配置路徑**：
- `gateway.port` - 網關端口
- `models.default` - 預設模型
- `models.routing.strategy` - 路由策略
- `memory.enabled` - 記憶功能

---

### 工具四：`openclaw_deploy` - 一鍵部署

```python
openclaw_deploy(method: str = "docker", port: int = 18789) -> dict
```

| 參數 | 類型 | 必填 | 預設值 | 選項 | 說明 |
|------|------|------|--------|------|------|
| `method` | str | 否 | `"docker"` | `"docker"`, `"npm"`, `"daemon"` | 部署方式 |
| `port` | int | 否 | `18789` | 1024-65535 | 網關端口 |

**調用範例**：
```python
openclaw_deploy()                    # Docker 部署（預設）
openclaw_deploy("docker", 18789)     # Docker 部署到 18789
openclaw_deploy("npm", 18790)        # npm 前台執行
openclaw_deploy("daemon", 18789)     # 背景守護程序
```

---

### 工具五：`openclaw_docs` - 查詢文檔

```python
openclaw_docs(topic: str = None) -> dict
```

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `topic` | str | 否 | `None` | 主題名稱（中文或英文） |

**調用範例**：
```python
openclaw_docs()              # 列出所有文檔
openclaw_docs("快速入門")    # 查詢快速入門
openclaw_docs("deployment")  # 查詢部署方式
```

**主題對照**：
| 中文 | 英文 | 文檔 |
|------|------|------|
| 快速入門 | quick-start | 01-快速入門.md |
| 部署方式 | deployment | 02-部署方式.md |
| 安全配置 | security | 03-安全配置.md |
| 多模型 | multi-model | 04-多模型整合.md |
| 技能系統 | skills | 05-技能系統.md |
| 記憶系統 | memory | 06-記憶系統.md |

---

## 🎮 12 種玩法速查

| # | 玩法 | 難度 | MCP 調用 |
|---|------|------|----------|
| 1 | 一鍵安裝 | ⭐ | `openclaw_install()` |
| 2 | 多模型切換 | ⭐⭐ | `openclaw_config("set", "models.routing.strategy", "task-route")` |
| 3 | 自定義技能 | ⭐⭐⭐ | `openclaw_docs("技能系統")` |
| 4 | 記憶客製化 | ⭐⭐ | `openclaw_docs("記憶系統")` |
| 5 | Docker 部署 | ⭐⭐ | `openclaw_deploy("docker")` |
| 6 | API 金鑰輪替 | ⭐⭐⭐ | 配置多金鑰 round-robin |
| 7 | 向量記憶 | ⭐⭐⭐ | 整合 Qdrant |
| 8 | Telegram Bot | ⭐⭐⭐ | `openclaw channels add telegram` |
| 9 | 批量處理 | ⭐⭐⭐ | `openclaw batch process` |
| 10 | 安全沙箱 | ⭐⭐⭐⭐ | Docker 安全配置 |
| 11 | 多租戶 | ⭐⭐⭐⭐ | 架構設計 |
| 12 | 監控告警 | ⭐⭐⭐ | Prometheus + Grafana |

**詳細玩法說明**：見 `docs/08-十種以上玩法.md`

---

## 📊 框架架構

```
┌─────────────────────────────────────────┐
│       OpenClaw 智慧老師 MCP              │
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Install │ │ Health  │ │ Config  │   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
│       │           │           │         │
│  ┌────┴────┐ ┌────┴────┐               │
│  │ Deploy  │ │  Docs   │               │
│  └─────────┘ └─────────┘               │
├─────────────────────────────────────────┤
│  底層：run_command | File I/O | JSON    │
└─────────────────────────────────────────┘
```

---

## 📚 知識庫索引（14 份文檔）

| 文檔 | 標籤 | 內容摘要 |
|------|------|----------|
| 01-快速入門.md | `installation`, `quick-start` | 5 分鐘上手 |
| 02-部署方式.md | `deployment`, `docker`, `npm` | 4 種部署比較 |
| 03-安全配置.md | `security`, `api-key` | 金鑰管理、隔離 |
| 04-多模型整合.md | `multi-model`, `routing` | 模型切換策略 |
| 05-技能系統.md | `skills`, `mcp` | 技能開發指南 |
| 06-記憶系統.md | `memory`, `soul` | SOUL.md 格式 |
| 07-MCP工具完整手冊.md | `tools`, `parameters` | 參數詳解 |
| 08-十種以上玩法.md | `playbook`, `use-cases` | 12 種玩法 |
| 09-MCP整合深度指南.md | `mcp`, `protocol` | MCP 協議深度 |
| 10-Soul-System向量整合.md | `vector`, `embedding` | 向量檢索整合 |
| 11-完整規範框架.md | `framework`, `specification` | 3x3 搜尋整理 |
| 12-輪詢策略最佳實踐.md | `polling`, `rotation`, `fallback` | 輪詢策略工作流 |
| 13-部署參數與相依性.md | `parameters`, `dependencies` | 環境變數、Docker |
| 14-向量資料庫整合.md | `vector`, `embedding`, `chromadb` | 向量 DB 整合 |

---

## 🚀 快速開始

### 安裝並啟動

```python
# 1. 安裝
openclaw_install("npm")

# 2. 檢查
openclaw_health()

# 3. 部署
openclaw_deploy("daemon", 18789)
```

### 查詢文檔

```python
# 列出所有文檔
openclaw_docs()

# 查詢特定主題
openclaw_docs("部署方式")
```

---

## 🧠 向量檢索標籤

```yaml
vector_tags:
  - openclaw
  - deployment
  - installation
  - docker
  - npm
  - kubernetes
  - multi-model
  - claude
  - gpt
  - gemini
  - skills
  - mcp
  - memory
  - soul
  - security
  - api-key
  - 部署
  - 安裝
  - 教學
  - 礁島學習
  - 玩法
  - 參數
```

---

## 🔗 相關技能

| 技能 | 說明 | 載入 |
|------|------|------|
| `openclaw-master` | 🦞 智慧老師主技能 | `/skill openclaw-master` |
| `openclaw-official-guide` | 📋 官方配置指南 | `/skill openclaw-official-guide` |
| `openclaw-advanced` | 🚀 進階玩法 | `/skill openclaw-advanced` |
| `openclaw-super-skills` | ⚡ 超級技能框架 | `/skill openclaw-super-skills` |

---

*技能版本：1.1*
*所屬系統：Soul System > 礁島學習*
*最後更新：2026-02-04*
*文檔數量：8 份 | 玩法數量：12 種 | MCP 工具：5 個*
