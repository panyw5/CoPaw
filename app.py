#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CoPaw ModelScope Studio Entry Point
魔搭社区创空间入口文件

This file serves as the entry point for deploying CoPaw on ModelScope Studio.
"""
import os
import sys
import subprocess
from pathlib import Path

# Set working directory for CoPaw
WORKING_DIR = Path(os.getenv("COPAW_WORKING_DIR", "/app/working"))
SECRET_DIR = Path(os.getenv("COPAW_SECRET_DIR", "/app/working.secret"))

# Ensure directories exist
WORKING_DIR.mkdir(parents=True, exist_ok=True)
SECRET_DIR.mkdir(parents=True, exist_ok=True)

# Set environment variables
os.environ["COPAW_WORKING_DIR"] = str(WORKING_DIR)
os.environ["COPAW_SECRET_DIR"] = str(SECRET_DIR)
os.environ["COPAW_PORT"] = os.getenv("COPAW_PORT", "7860")  # ModelScope default port

# Disable features that may not work in ModelScope environment
os.environ["COPAW_DISABLE_DESKTOP"] = "1"
os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"

# Initialize CoPaw if not already initialized
config_file = WORKING_DIR / "config.json"
if not config_file.exists():
    print("Initializing CoPaw for the first time...")
    try:
        subprocess.run(
            ["copaw", "init", "--defaults", "--accept-security"],
            check=True,
            cwd=str(WORKING_DIR.parent),
        )
        print("CoPaw initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Warning: CoPaw initialization failed: {e}")
        print("Continuing anyway, you may need to configure manually.")

# Import CoPaw app
from copaw.app._app import app

# For ModelScope Studio compatibility
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("COPAW_PORT", "7860"))
    host = os.getenv("COPAW_HOST", "0.0.0.0")

    print("=" * 60)
    print(f"🐾 Starting CoPaw on {host}:{port}")
    print(f"📁 Working directory: {WORKING_DIR}")
    print(f"🔐 Secret directory: {SECRET_DIR}")
    print("=" * 60)
    print("\n💡 First time setup:")
    print("   1. Open the Console UI")
    print("   2. Go to Settings → Models")
    print("   3. Configure your LLM provider and API key")
    print("   4. Start chatting!\n")
    print("=" * 60)

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )
