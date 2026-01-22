"""MetaForge - AI-Powered App Builder

Main entry point for the application.
"""
import os
import sys

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main import main

import config

if __name__ == "__main__":
    # Windows consoles can choke on emoji/Unicode; make stdout/stderr robust.
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable not set!", flush=True)
        print("Please set it with: export OPENAI_API_KEY='your-api-key'", flush=True)
        print("Or on Windows: set OPENAI_API_KEY=your-api-key", flush=True)
        print("Continuing without key (UI will load, generation will be blocked until key is set).", flush=True)
        print("", flush=True)
    
    print("Starting MetaForge...", flush=True)
    print(f"NiceGUI will be available at: http://localhost:{config.NICEGUI_PORT}", flush=True)
    print(f"Preview server will run on: http://localhost:{config.PREVIEW_PORT}", flush=True)
    print("", flush=True)
    
    main()
