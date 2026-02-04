# 🦞 OpenClaw 智慧老師（礁島學習系統）

> **Soul System 子專案** - 教導學習 | 提供資訊 | MCP 直接實現

---

## 📋 專案定位

| 項目 | 說明 |
|------|------|
| **所屬系統** | Soul System（思維熔爐） |
| **核心功能** | 1️⃣ 教導學習 2️⃣ 提供資訊 3️⃣ MCP 直接實現 |
| **向量檢索** | ✅ 支援（chunk-friendly 格式） |
| **語言** | 中文文檔，英文代碼 |

---

## 🎯 三大功能

### 1️⃣ 教導學習
透過結構化文檔教導用戶：
- OpenClaw 安裝與配置
- 部署方式選擇
- 安全最佳實踐
- 多模型整合
- 技能系統開發

### 2️⃣ 提供資訊
向量檢索友好的知識庫：
- 所有文檔帶有檢索標籤
- chunk 大小優化
- 支援 Soul API 查詢

### 3️⃣ MCP 直接實現
需要時可直接執行操作：
- `openclaw_install` - 安裝 OpenClaw
- `openclaw_health` - 健康檢查
- `openclaw_config` - 配置管理
- `openclaw_deploy` - 一鍵部署

---

## 📁 目錄結構

```
openclaw-deployment/
├── docs/                           # 📚 教學文檔
│   ├── 01-快速入門.md              # 5 分鐘上手
│   ├── 02-部署方式.md              # Docker/npm/Nix 對比
│   ├── 03-安全配置.md              # 生產環境安全
│   ├── 04-多模型整合.md            # Claude/GPT/Gemini
│   ├── 05-技能系統.md              # 自定義技能
│   └── 06-記憶系統.md              # SOUL.md + MEMORY.md
├── mcp/                            # 🔧 MCP 工具實現
│   ├── openclaw_mcp.py             # MCP Server 主程式
│   └── tools.py                    # 工具函數
├── configs/                        # ⚙️ 配置範本
│   ├── docker-compose.yml
│   ├── openclaw.json
│   ├── SOUL.md
│   └── MEMORY.md
├── scripts/                        # 🔧 自動化腳本
│   └── install.sh
└── skill.md                        # 技能定義（含中文備註）
```

---

## 🔧 MCP 工具使用方式

### 在 Claude Code / OpenClaw 中使用

```bash
# 載入技能
/skill openclaw-deployment

# 直接呼叫 MCP 工具
openclaw_install          # 安裝 OpenClaw
openclaw_health           # 健康檢查
openclaw_config --show    # 顯示配置
openclaw_deploy --docker  # Docker 部署
```

### MCP 配置（settings.json）

```json
{
  "mcpServers": {
    "openclaw-teacher": {
      "command": "python3",
      "args": ["~/Documents/思維熔爐/openclaw-deployment/mcp/openclaw_mcp.py"]
    }
  }
}
```

---

## 🧠 向量檢索標籤

```yaml
tags:
  - openclaw
  - deployment
  - docker
  - npm
  - multi-model
  - skills
  - memory
  - soul-system
  - mcp
  - 部署
  - 教學
  - 礁島學習
```

---

## 📖 相關技能

| 技能名稱 | 中文備註 | 使用方式 |
|----------|----------|----------|
| `openclaw-deployment` | 🦞 部署教學 + MCP 實現 | `/skill openclaw-deployment` |
| `openclaw-master` | 🦞 智慧老師主技能 | `/skill openclaw-master` |
| `openclaw-official-guide` | 📋 官方配置指南 | `/skill openclaw-official-guide` |
| `openclaw-advanced` | 🚀 進階玩法 | `/skill openclaw-advanced` |

---

*最後更新：2026-02-04*
*所屬：Soul System > 礁島學習*
