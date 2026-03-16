#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CoPaw ModelScope Studio Entry Point (Gradio Compatible)
魔搭社区创空间入口文件 - Gradio 兼容版本
"""
import os
import sys
import subprocess
import threading
import time
from pathlib import Path

# Set working directory for CoPaw
WORKING_DIR = Path(os.getenv("COPAW_WORKING_DIR", "/tmp/copaw_working"))
SECRET_DIR = Path(os.getenv("COPAW_SECRET_DIR", "/tmp/copaw_secret"))

# Ensure directories exist
WORKING_DIR.mkdir(parents=True, exist_ok=True)
SECRET_DIR.mkdir(parents=True, exist_ok=True)

# Set environment variables
os.environ["COPAW_WORKING_DIR"] = str(WORKING_DIR)
os.environ["COPAW_SECRET_DIR"] = str(SECRET_DIR)
os.environ["COPAW_PORT"] = "8088"  # CoPaw internal port

# Disable features that may not work in ModelScope environment
os.environ["COPAW_DISABLE_DESKTOP"] = "1"
os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"

# Initialize CoPaw if not already initialized
config_file = WORKING_DIR / "config.json"
if not config_file.exists():
    print("🐾 Initializing CoPaw for the first time...")
    try:
        subprocess.run(
            ["copaw", "init", "--defaults", "--accept-security"],
            check=True,
            env=os.environ,
        )
        print("✅ CoPaw initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: CoPaw initialization failed: {e}")
        print("Continuing anyway, you may need to configure manually.")

def start_copaw_server():
    """Start CoPaw FastAPI server in background"""
    print("=" * 60)
    print("🐾 Starting CoPaw server...")
    print(f"📁 Working directory: {WORKING_DIR}")
    print(f"🔐 Secret directory: {SECRET_DIR}")
    print("=" * 60)

    # Import and run CoPaw app
    from copaw.app._app import app
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8088,
        log_level="info",
    )

# Start CoPaw server in background thread
server_thread = threading.Thread(target=start_copaw_server, daemon=True)
server_thread.start()

# Wait for server to start
print("⏳ Waiting for CoPaw server to start...")
time.sleep(5)

# Create Gradio interface as a proxy
import gradio as gr

def create_interface():
    """Create Gradio interface that redirects to CoPaw Console"""

    with gr.Blocks(title="CoPaw - Personal AI Assistant") as demo:
        gr.Markdown("""
        # 🐾 CoPaw - Personal AI Assistant

        CoPaw 正在后台运行! 请点击下面的链接访问 Console 界面。

        ## 🚀 快速开始

        1. **访问 Console**: 点击下方的 "Open CoPaw Console" 按钮
        2. **配置 API Key**: 进入 Settings → Models,配置你的 LLM 提供商
        3. **开始对话**: 在 Console 中与 CoPaw 交流

        ## 📝 注意事项

        - 首次使用需要配置 API Key (DashScope、OpenAI 等)
        - 可以在 Settings → Channels 配置钉钉、飞书等渠道
        - 所有数据存储在工作目录,重启后保留

        ## 🔗 相关链接

        - [官方文档](https://copaw.agentscope.io/)
        - [GitHub](https://github.com/agentscope-ai/CoPaw)
        """)

        gr.Markdown("""
        ### 访问 CoPaw Console

        由于魔搭创空间的限制,请使用以下方式访问 CoPaw:

        1. **方式一**: 在浏览器地址栏中,将当前 URL 的端口改为 `:8088`
           - 例如: `https://xxx.modelscope.cn:8088/`

        2. **方式二**: 如果上述方式不可用,请查看创空间的日志获取访问地址

        3. **方式三**: 使用 Docker 部署方式 (见下方说明)
        """)

        with gr.Accordion("💡 为什么需要这样访问?", open=False):
            gr.Markdown("""
            CoPaw 是一个 FastAPI 应用,运行在 8088 端口。
            魔搭创空间主要支持 Gradio/Streamlit,所以我们创建了这个 Gradio 包装器。

            **更好的部署方式**: 使用 Docker 部署 (见下方)
            """)

        with gr.Accordion("🐳 推荐: 使用 Docker 部署", open=False):
            gr.Markdown("""
            如果当前方式无法正常访问,建议使用 Docker 部署:

            1. 在魔搭创空间配置中选择 **Docker** (beta)
            2. 使用项目中的 `deploy/Dockerfile`
            3. 这样可以完整运行 CoPaw,无需 Gradio 包装

            或者使用官方的一键部署:
            - [ModelScope Studio 一键部署](https://modelscope.cn/studios/fork?target=AgentScope/CoPaw)
            """)

        gr.Markdown("""
        ---

        **CoPaw 服务状态**: 🟢 运行中 (端口 8088)

        如有问题,请查看创空间日志或访问 [GitHub Issues](https://github.com/agentscope-ai/CoPaw/issues)
        """)

    return demo

# Create and launch Gradio interface
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎉 CoPaw is ready!")
    print("=" * 60)
    print("\n💡 提示:")
    print("   - CoPaw 服务运行在端口 8088")
    print("   - Gradio 界面运行在端口 7860")
    print("   - 请按照界面提示访问 CoPaw Console\n")

    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
