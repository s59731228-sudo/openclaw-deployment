# 🔌 MCP 整合深度指南

> **向量檢索標籤**：`mcp`, `integration`, `protocol`, `servers`, `tools`, `整合`
> **資料來源**：第 1 輪多代理搜尋精煉

---

## 📋 MCP 協議概述

**MCP (Model Context Protocol)** 是讓 AI 工具與外部服務整合的標準協議。

### 核心能力

| 能力 | 說明 |
|------|------|
| **外部服務連接** | 連接資料庫、API、檔案系統 |
| **工具暴露** | 單一服務可提供 10+ 個工具 |
| **認證處理** | 支援 OAuth 和複雜認證流程 |
| **自動設置** | 與插件綁定自動配置 |

---

## 🔧 MCP Server 配置方式

### 方式一：獨立 .mcp.json（推薦）

在插件根目錄創建 `.mcp.json`：

```json
{
  "my-mcp-server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "API_KEY": "${MY_API_KEY}"
    }
  }
}
```

**優點**：
- 職責分離清晰
- 易於維護
- 適合多 Server 場景

### 方式二：內嵌於 settings.json

```json
{
  "mcpServers": {
    "openclaw-teacher": {
      "command": "python3",
      "args": ["~/Documents/思維熔爐/openclaw-deployment/mcp/openclaw_mcp.py"],
      "env": {
        "PYTHONPATH": "~/Documents/思維熔爐/openclaw-deployment"
      }
    }
  }
}
```

**優點**：
- 單一配置檔
- 適合簡單場景

---

## 📡 MCP Server 類型

### 類型一：stdio（本地進程）

透過 stdin/stdout 通訊的本地 MCP Server。

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
    "env": {
      "LOG_LEVEL": "debug"
    }
  }
}
```

**適用場景**：
- 檔案系統存取
- 本地資料庫連接
- 自定義 MCP Server
- NPM 打包的 MCP Server

**生命週期**：
- Claude Code 啟動並管理進程
- 透過 stdin/stdout 通訊
- Claude Code 結束時終止

### 類型二：SSE（Server-Sent Events）

連接遠端託管的 MCP Server，支援 OAuth。

```json
{
  "cloud-service": {
    "type": "sse",
    "url": "https://mcp.example.com/events",
    "oauth": {
      "client_id": "${CLIENT_ID}",
      "auth_url": "https://example.com/oauth/authorize"
    }
  }
}
```

**適用場景**：
- 雲端服務整合
- 需要 OAuth 認證
- 即時事件推送

### 類型三：HTTP/WebSocket

傳統 HTTP API 或 WebSocket 連接。

```json
{
  "api-service": {
    "type": "http",
    "baseUrl": "https://api.example.com",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

---

## 🛠️ 自定義 MCP Server 開發

### Python 實現範例

```python
#!/usr/bin/env python3
"""自定義 MCP Server 範例"""

import json
import sys
from typing import Any

def handle_request(request: dict) -> dict:
    """處理 MCP 請求"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "my_tool",
                    "description": "我的工具說明",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "param1": {"type": "string"}
                        }
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "my_tool":
            result = execute_my_tool(arguments)
            return {"content": [{"type": "text", "text": json.dumps(result)}]}
    
    return {"error": "Unknown method"}

def execute_my_tool(args: dict) -> dict:
    """執行工具邏輯"""
    return {"success": True, "result": "..."}

def main():
    """MCP Server 主循環"""
    for line in sys.stdin:
        request = json.loads(line)
        response = handle_request(request)
        print(json.dumps(response), flush=True)

if __name__ == "__main__":
    main()
```

### 工具定義格式

```json
{
  "name": "tool_name",
  "description": "工具說明（中文）",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "參數說明"
      },
      "param2": {
        "type": "integer",
        "default": 10
      }
    },
    "required": ["param1"]
  }
}
```

---

## 🔗 與 Soul System 整合

### Soul API 端點

| 端點 | 用途 |
|------|------|
| `/soul/query` | 查詢記憶 |
| `/soul/store` | 儲存記憶 |
| `/soul/search` | 向量搜尋 |

### MCP 整合 Soul API

```python
import requests

def soul_query(query: str) -> dict:
    """查詢 Soul System 記憶"""
    response = requests.post(
        "http://localhost:8531/soul/query",
        json={"query": query}
    )
    return response.json()

def soul_store(content: str, tags: list) -> dict:
    """儲存到 Soul System"""
    response = requests.post(
        "http://localhost:8531/soul/store",
        json={"content": content, "tags": tags}
    )
    return response.json()
```

---

## 📂 現有 MCP 資源（本地）

### 已安裝的 MCP Server

| Server | 位置 | 用途 |
|--------|------|------|
| brave-search | npx @anthropic/mcp-server-brave-search | 網路搜尋 |
| pal | uvx pal-mcp-server | Gemini/OpenAI 整合 |
| playwright | @anthropic/mcp-server-playwright | 瀏覽器自動化 |

### 技能中的 MCP 整合

本專案的 MCP 實現位於：
```
~/Documents/思維熔爐/openclaw-deployment/mcp/openclaw_mcp.py
```

提供 5 個工具：
- `openclaw_install`
- `openclaw_health`
- `openclaw_config`
- `openclaw_deploy`
- `openclaw_docs`

---

## ⚠️ MCP 開發注意事項

### 必須遵守

1. **JSON 格式**：請求和回應必須是有效 JSON
2. **錯誤處理**：總是返回結構化錯誤
3. **超時處理**：設置合理的超時時間
4. **資源清理**：進程結束時清理資源

### 最佳實踐

1. **工具命名**：使用 snake_case，語意清晰
2. **參數驗證**：驗證所有輸入參數
3. **文檔完整**：每個工具都要有說明
4. **返回格式統一**：`{"success": bool, ...}`

---

*文檔版本：1.0*
*資料來源：多代理搜尋精煉*
