# ⚒️ MetaForge - AI-Powered App Builder

> Transform natural language into working web applications using Google ADK multi-agent orchestration.

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10+-green) ![Status](https://img.shields.io/badge/status-active-success)

---

## 🎯 Features

- 🤖 **Multi-Agent AI** - Google ADK orchestrates Planner, Frontend, and Backend agents
- ⚡ **Fast Generation** - Complete apps in under 2 minutes
- 👁️ **Live Preview** - Real-time iframe preview with auto-reload
- 💬 **Chat Refinement** - Iteratively improve through conversation
- 🩹 **Self-Healing** - Automatic error detection and fixes (max 2 retries)
- 📁 **Code Browser** - View generated files with syntax highlighting
- 📊 **Progress Tracking** - Watch agents work in real-time

---

## 🏗️ Architecture

### System Overview

```mermaid
graph TB
    User([User])
    UI[NiceGUI Interface]
    Orch[Orchestrator]
    
    subgraph "Agents"
        Plan[Planner<br/>Analyze Requirements]
        FE[Frontend<br/>React + Canvas]
        BE[Backend<br/>FastAPI/Flask]
    end
    
    LLM[GPT-4o-mini]
    Files[(Generated<br/>Files)]
    Preview[Preview<br/>Server :8081]
    
    User --> UI
    UI --> Orch
    Orch --> Plan
    Orch --> FE
    Orch --> BE
    Plan --> LLM
    FE --> LLM
    BE --> LLM
    FE --> Files
    BE --> Files
    Files --> Preview
    Preview --> UI
    
    style User fill:#3b82f6,color:#fff
    style LLM fill:#f59e0b,color:#fff
    style Files fill:#10b981,color:#fff
    style Preview fill:#ef4444,color:#fff
```

### Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as NiceGUI
    participant Orch as Orchestrator
    participant Plan as PlannerAgent
    participant FE as FrontendAgent
    participant BE as BackendAgent
    
    User->>UI: "Build a Snake game"
    UI->>Orch: start_generation()
    
    Orch->>Plan: Analyze requirements
    Plan-->>Orch: RequirementSpec
    
    par Parallel Execution
        Orch->>FE: Generate React+Canvas
        Orch->>BE: Generate API (if needed)
    end
    
    FE-->>Orch: index.html
    BE-->>Orch: main.py
    
    Orch->>Orch: Validate & Self-Heal
    Orch->>UI: Update preview
    UI-->>User: Live preview + files
    
    User->>UI: "Make it dark mode"
    UI->>Orch: refine()
    Orch->>FE: Update code
    FE-->>Orch: Updated files
    Orch->>UI: Reload preview
```

### Component Architecture

```mermaid
graph LR
    subgraph "UI Layer - 3 Panels"
        A[Chat &<br/>Logs<br/>25%]
        B[Live<br/>Preview<br/>55%]
        C[Files &<br/>Code<br/>20%]
    end
    
    subgraph "Orchestration"
        D[Session<br/>Manager]
        E[ADK<br/>Runner]
    end
    
    subgraph "Validation"
        F[Code<br/>Validator]
        G[Self-Heal<br/>Logic]
    end
    
    A --> D
    B --> E
    C --> D
    D --> E
    E --> F
    F --> G
    G --> E
    
    style A fill:#1e293b,color:#fff
    style B fill:#1e293b,color:#fff
    style C fill:#1e293b,color:#fff
    style D fill:#8b5cf6,color:#fff
    style E fill:#8b5cf6,color:#fff
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/metaforge.git
cd metaforge

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY='your-key-here'  # Mac/Linux
set OPENAI_API_KEY=your-key-here       # Windows
```

### Run

```bash
python main.py
```

Open **http://localhost:9080**

---

## 📖 Usage

### Good Prompts ✅

```
"Build a Snake game with Canvas, score tracking, and dark mode"
"Create a todo app with categories, due dates, and localStorage"
"Make a calculator with memory functions and keyboard support"
```

### Poor Prompts ❌

```
"Make a game"           → Too vague
"Build an app"          → No specifics
"Create something cool" → No direction
```

### Refinement

```
User: "Build a Snake game"
Bot: ✅ Generated!

User: "Add pause button"
Bot: ✅ Updated!

User: "Increase snake speed"
Bot: ✅ Updated!
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | GPT-4o-mini (OpenAI) |
| **Orchestration** | Google ADK |
| **UI** | NiceGUI (Python) |
| **Generated Frontend** | React 18 + Tailwind/Canvas |
| **Generated Backend** | FastAPI / Flask |
| **Validation** | Python AST + Regex |
| **Preview** | HTTP Server (:8081) |

---

## 📂 Project Structure

```
metaforge/
├── main.py              # Entry point
├── config.py            # Prompts & settings
├── agents/
│   ├── orchestrator.py  # ADK orchestration
│   ├── components.py    # Planner/Frontend/Backend agents
│   └── base.py          # ADK base classes
├── ui/
│   ├── main.py          # NiceGUI app
│   └── components/      # UI panels
├── context/
│   ├── models.py        # Pydantic models
│   └── session_manager.py
├── utils/
│   ├── code_validator.py
│   └── file_manager.py
└── generated_projects/  # Output (gitignored)
```

---

## 🔧 Configuration

Edit `config.py`:

```python
# API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"

# Ports
NICEGUI_PORT = 9080
PREVIEW_PORT = 8081

# Prompts (see config.py for full text)
REQUIREMENTS_ANALYZER_PROMPT = "..."
FRONTEND_GENERATOR_PROMPT = "..."
BACKEND_GENERATOR_PROMPT = "..."
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **API key error** | `export OPENAI_API_KEY='your-key'` |
| **Preview not loading** | Check port 8081 availability |
| **Keyboard not working in game** | Click the focus overlay in preview |
| **Generation fails** | Check internet connection, verify API key |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- **Google ADK** - Multi-agent framework
- **OpenAI** - GPT-4o-mini model
- **NiceGUI** - Python web UI

---

<p align="center">
  <strong>Built with ❤️ using Google ADK and NiceGUI</strong><br>
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-troubleshooting">Troubleshooting</a>
</p>