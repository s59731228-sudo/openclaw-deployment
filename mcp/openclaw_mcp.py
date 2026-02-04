#!/usr/bin/env python3
"""
OpenClaw 智慧老師 MCP Server
功能：教導學習 | 提供資訊 | 直接執行操作

使用方式：
1. 在 settings.json 中配置此 MCP
2. 透過 AI 助手呼叫工具
"""

import subprocess
import json
import os
import sys
from pathlib import Path
from typing import Optional

DOCS_PATH = Path(__file__).parent.parent / "docs"
CONFIGS_PATH = Path(__file__).parent.parent / "configs"


def run_command(cmd: list[str], timeout: int = 60) -> dict:
    """執行系統指令並返回結果"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"指令超時（{timeout}秒）"}
    except FileNotFoundError:
        return {"success": False, "error": f"找不到指令: {cmd[0]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def openclaw_install(method: str = "npm") -> dict:
    """
    安裝 OpenClaw

    參數:
        method: 安裝方式 - "npm" (預設) 或 "docker"

    使用範例:
        openclaw_install()           # npm 安裝
        openclaw_install("docker")   # Docker 安裝
    """
    if method == "npm":
        result = run_command(["npm", "install", "-g", "openclaw@latest"])
        if result["success"]:
            onboard = run_command(["openclaw", "onboard", "--install-daemon"])
            return {
                "success": True,
                "message": "OpenClaw 安裝完成",
                "install_output": result["stdout"],
                "onboard_output": onboard.get("stdout", ""),
            }
        return result

    elif method == "docker":
        compose_file = CONFIGS_PATH / "docker-compose.yml"
        if not compose_file.exists():
            return {"success": False, "error": "找不到 docker-compose.yml"}

        result = run_command(
            ["docker", "compose", "-f", str(compose_file), "up", "-d"], timeout=120
        )
        return {
            "success": result["success"],
            "message": "Docker 容器已啟動" if result["success"] else "啟動失敗",
            "output": result.get("stdout", "") + result.get("stderr", ""),
        }

    return {"success": False, "error": f"不支援的安裝方式: {method}"}


def openclaw_health() -> dict:
    """
    健康檢查

    檢查項目:
        - OpenClaw 安裝狀態
        - Node.js 版本
        - 網關狀態
        - API 金鑰配置

    使用範例:
        openclaw_health()
    """
    checks = {}

    node_result = run_command(["node", "-v"])
    checks["node"] = {
        "status": "✅" if node_result["success"] else "❌",
        "version": node_result.get("stdout", "").strip()
        if node_result["success"]
        else "未安裝",
    }

    openclaw_result = run_command(["openclaw", "--version"])
    checks["openclaw"] = {
        "status": "✅" if openclaw_result["success"] else "❌",
        "version": openclaw_result.get("stdout", "").strip()
        if openclaw_result["success"]
        else "未安裝",
    }

    api_keys = {
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY", ""),
    }
    checks["api_keys"] = {
        k: "✅ 已配置" if v else "❌ 未配置" for k, v in api_keys.items()
    }

    doctor_result = run_command(["openclaw", "doctor"])
    checks["doctor"] = {
        "status": "✅" if doctor_result["success"] else "⚠️",
        "output": doctor_result.get("stdout", "")[:500],
    }

    return {"success": True, "checks": checks, "summary": "健康檢查完成"}


def openclaw_config(
    action: str = "show", key: Optional[str] = None, value: Optional[str] = None
) -> dict:
    """
    配置管理

    參數:
        action: "show" (顯示) | "get" (取得) | "set" (設定)
        key: 配置鍵（用於 get/set）
        value: 配置值（用於 set）

    使用範例:
        openclaw_config("show")                    # 顯示所有配置
        openclaw_config("get", "models.default")   # 取得預設模型
        openclaw_config("set", "gateway.port", "18790")  # 設定端口
    """
    config_file = Path.home() / ".openclaw" / "openclaw.json"

    if action == "show":
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
            return {"success": True, "config": config}
        return {"success": False, "error": "配置檔不存在，請先執行 openclaw onboard"}

    elif action == "get":
        if not key:
            return {"success": False, "error": "請指定 key"}
        result = run_command(["openclaw", "config", "get", key])
        return {
            "success": result["success"],
            "key": key,
            "value": result.get("stdout", "").strip(),
        }

    elif action == "set":
        if not key or not value:
            return {"success": False, "error": "請指定 key 和 value"}
        result = run_command(["openclaw", "config", "set", key, value])
        return {
            "success": result["success"],
            "message": f"已設定 {key} = {value}" if result["success"] else "設定失敗",
        }

    return {"success": False, "error": f"不支援的操作: {action}"}


def openclaw_deploy(method: str = "docker", port: int = 18789) -> dict:
    """
    一鍵部署

    參數:
        method: "docker" (預設) | "npm" | "daemon"
        port: 網關端口（預設 18789）

    使用範例:
        openclaw_deploy()                    # Docker 部署
        openclaw_deploy("npm", 18790)        # npm 部署到 18790 端口
        openclaw_deploy("daemon")            # 背景守護程序
    """
    if method == "docker":
        compose_file = CONFIGS_PATH / "docker-compose.yml"
        if not compose_file.exists():
            return {"success": False, "error": "找不到 docker-compose.yml"}

        env = os.environ.copy()
        env["GATEWAY_PORT"] = str(port)

        result = run_command(
            ["docker", "compose", "-f", str(compose_file), "up", "-d"], timeout=120
        )
        return {
            "success": result["success"],
            "message": f"Docker 部署完成，端口 {port}"
            if result["success"]
            else "部署失敗",
            "output": result.get("stdout", "") + result.get("stderr", ""),
        }

    elif method == "npm":
        result = run_command(["openclaw", "gateway", "--port", str(port)])
        return {
            "success": True,
            "message": f"網關已啟動，端口 {port}",
            "note": "此為前台執行，關閉終端會停止",
        }

    elif method == "daemon":
        result = run_command(["openclaw", "gateway", "--daemon", "--port", str(port)])
        return {
            "success": result["success"],
            "message": f"守護程序已啟動，端口 {port}"
            if result["success"]
            else "啟動失敗",
        }

    return {"success": False, "error": f"不支援的部署方式: {method}"}


def openclaw_docs(topic: Optional[str] = None) -> dict:
    """
    查詢教學文檔

    參數:
        topic: 主題名稱（可選）
               - "快速入門" / "quick-start"
               - "部署方式" / "deployment"
               - "安全配置" / "security"
               - "多模型" / "multi-model"
               - "技能系統" / "skills"
               - "記憶系統" / "memory"

    使用範例:
        openclaw_docs()              # 列出所有文檔
        openclaw_docs("部署方式")    # 查詢部署文檔
    """
    topic_map = {
        "快速入門": "01-快速入門.md",
        "quick-start": "01-快速入門.md",
        "部署方式": "02-部署方式.md",
        "deployment": "02-部署方式.md",
        "安全配置": "03-安全配置.md",
        "security": "03-安全配置.md",
        "多模型": "04-多模型整合.md",
        "multi-model": "04-多模型整合.md",
        "技能系統": "05-技能系統.md",
        "skills": "05-技能系統.md",
        "記憶系統": "06-記憶系統.md",
        "memory": "06-記憶系統.md",
    }

    if topic is None:
        docs = list(DOCS_PATH.glob("*.md"))
        return {
            "success": True,
            "available_docs": [d.name for d in docs],
            "usage": "使用 openclaw_docs('主題名稱') 查詢特定文檔",
        }

    filename = topic_map.get(topic, topic)
    doc_path = DOCS_PATH / filename

    if not doc_path.exists():
        if not filename.endswith(".md"):
            doc_path = DOCS_PATH / f"{filename}.md"

    if doc_path.exists():
        with open(doc_path, encoding="utf-8") as f:
            content = f.read()
        return {"success": True, "topic": topic, "content": content}

    return {
        "success": False,
        "error": f"找不到文檔: {topic}",
        "available": list(topic_map.keys()),
    }


TOOLS = {
    "openclaw_install": openclaw_install,
    "openclaw_health": openclaw_health,
    "openclaw_config": openclaw_config,
    "openclaw_deploy": openclaw_deploy,
    "openclaw_docs": openclaw_docs,
}


def main():
    """MCP Server 主程式"""
    print("OpenClaw 智慧老師 MCP Server 啟動", file=sys.stderr)
    print(f"可用工具: {list(TOOLS.keys())}", file=sys.stderr)


if __name__ == "__main__":
    main()
