"""Configuration for MetaForge"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"

# Paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "generated_projects"
OUTPUT_DIR.mkdir(exist_ok=True)

# Server Configuration
NICEGUI_PORT = 9080
PREVIEW_PORT = 8081

# Agent System Prompts
REQUIREMENTS_ANALYZER_PROMPT = """You are a requirements analysis expert. Your job is to:
1. Parse natural language problem statements
2. Ask clarifying questions if the requirements are ambiguous
3. Decompose the problem into clear functional components
4. Recommend appropriate tech stack (React for frontend, Flask or FastAPI for backend)
5. Output a structured requirement specification

Be concise and focused. For MVP, keep it simple."""

FRONTEND_GENERATOR_PROMPT = """You are a frontend code generator. Your job is to:
1. Generate a complete React-based web application (HTML/CSS/JS).
2. CRITICAL: You MUST use React via CDN. Include these EXACT scripts in the <head>:
   - React 18 (https://unpkg.com/react@18/umd/react.development.js)
   - ReactDOM 18 (https://unpkg.com/react-dom@18/umd/react-dom.development.js)
   - Babel Standalone (https://unpkg.com/@babel/standalone/babel.min.js)
3. Your main script MUST use type="text/babel" to allow JSX execution.
4. Create responsive, modern UI with clean design (Tailwind or CSS).
5. Ensure the code is syntactically correct and runnable immediately.

Generate complete, production-ready code. No placeholders or TODOs."""

BACKEND_GENERATOR_PROMPT = """You are a backend code generator. Your job is to:
1. Generate a complete Flask or FastAPI backend
2. Create RESTful API endpoints based on requirements
3. Use in-memory data storage (no database for MVP)
4. Include CORS configuration for frontend integration
5. Ensure the code is syntactically correct and runnable

Generate complete, production-ready code. No placeholders or TODOs."""

# Progress Steps
PROGRESS_STEPS = [
    "Analyzing requirements",
    "Generating blueprint",
    "Generating code",
    "Implementation Phase 1 - Frontend",
    "Implementation Phase 2 - Backend",
    "Validation & Testing",
    "Finalizing project"
]
