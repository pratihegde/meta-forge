# ⚒️ MetaForge - AI-Powered App Builder

**Forge apps from ideas** using Google ADK and NiceGUI.

MetaForge transforms natural language problem statements into working applications with live preview, real-time progress tracking, and instant deployment.

## Features

- 🤖 **Google ADK Orchestration** - Multi-agent system with LLM-powered code generation
- ⚡ **Lightning Fast** - Generate apps in under 2 minutes
- 👁️ **Live Preview** - See your app come to life in real-time
- 📁 **File Tree** - Browse and view generated code with syntax highlighting
- 📊 **Progress Tracking** - Watch intermediate steps as agents work
- 📦 **Ready to Deploy** - Download complete projects as ZIP

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    GOOGLE ADK ORCHESTRATOR                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │
│  │  Planning   │───▶│  Execution  │───▶│  Validation │               │
│  │   Phase     │    │   Phase     │    │   Phase     │               │
│  └─────────────┘    └─────────────┘    └─────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Requirements   │  │    Code Gen     │  │   Validator     │
│    Analyzer     │  │    Agents       │  │     Agent       │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│  - Parse input  │  │  - Frontend     │  │  - Syntax check │
│  - Clarify      │  │  - Backend      │  │  - Preview test │
│  - Decompose    │  │  (Parallel)     │  │  - Security     │
│  - Tech stack   │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Google Gemini API key

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd c:/AIAgents/Lyzr-antigrav
   ```

2. **Create virtual environment with uv:**
   ```bash
   uv venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -e .
   ```

4. **Set your Google API key:**
   ```bash
   # Windows
   set GOOGLE_API_KEY=your-api-key-here
   
   # Linux/Mac
   export GOOGLE_API_KEY=your-api-key-here
   ```

### Run MetaForge

```bash
python main.py
```

Then open your browser to `http://localhost:8080`

## Usage

1. **Enter your app idea** in the problem statement textarea
2. **Click "Generate App"** to start the orchestration
3. **Watch the progress** in the left panel as agents work
4. **See live preview** in the center panel
5. **Browse generated files** in the right panel
6. **Download your app** as a ZIP file

### Example Prompts

- "Create a calculator with basic operations"
- "Build a todo list app with categories and due dates"
- "Make a weather app that shows current conditions"
- "Design a simple blog with posts and comments"

## Project Structure

```
c:/AIAgents/Lyzr-antigrav/
├── main.py                 # Entry point
├── config.py               # Configuration
├── pyproject.toml          # uv dependencies
├── agents/
│   ├── orchestrator.py     # Google ADK orchestrator
│   └── __init__.py
├── context/
│   ├── models.py           # Pydantic models
│   ├── session_manager.py  # Session state management
│   └── __init__.py
├── ui/
│   ├── main.py             # NiceGUI application
│   └── components/
│       ├── landing_page.py # Hero page
│       ├── progress_panel.py
│       ├── live_preview.py
│       ├── file_tree.py
│       └── __init__.py
├── preview/
│   ├── preview_server.py   # HTTP server for preview
│   └── __init__.py
├── utils/
│   ├── code_validator.py   # Syntax validation
│   ├── file_manager.py     # File operations
│   └── __init__.py
└── generated_projects/     # Output directory
```

## Tech Stack

- **Orchestration**: Google ADK (Gemini 2.0 Flash)
- **Frontend**: NiceGUI
- **Generated Apps**: React (HTML/CSS/JS) + Flask/FastAPI
- **Dependency Management**: uv
- **Validation**: AST parsing, regex patterns

## User Iterations

MetaForge supports iterative improvements! After generating an app:

1. Provide feedback or request changes
2. Click "Regenerate"
3. The same agent loop processes your iteration
4. Preview updates automatically

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black .

# Lint
pylint agents/ ui/ context/ utils/
```

## Troubleshooting

**Issue**: "GOOGLE_API_KEY not set"
- **Solution**: Set the environment variable with your Gemini API key

**Issue**: Preview not loading
- **Solution**: Check that port 8081 is not in use

**Issue**: Generation fails
- **Solution**: Check your API key and internet connection

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR.

---

Built with ❤️ using Google ADK and NiceGUI
