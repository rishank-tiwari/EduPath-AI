# EduPath

> **"Your AI-powered adaptive career learning companion."**

Developed for the **Agentic AI Hackathon 2026** organized by **Product Space**.

---

## 🚀 Overview

**EduPath** is an agentic AI learning and career-development platform designed to bridge the gap between a learner's current capabilities and their target career goals. Rather than providing static learning roadmaps or serving as a standard Q&A chatbot, EduPath operates as a stateful, goal-driven multi-agent system.

It dynamically analyzes resumes, projects, and skill profiles, identifies specific skill gaps, builds tailored learning paths, delivers practice exercises, evaluates submission performance, detects persistent weaknesses, and continuously adapts the learner's journey over time.

---

## 🔄 Core Product Loop

Unlike traditional linear course platforms, EduPath runs on a continuous closed-loop adaptive cycle:

```
[ UNDERSTAND ] ──> [ ANALYZE ] ──> [ PLAN ] ──> [ ACT ]
      ▲                                            │
      │                                            ▼
 [ REPEAT ] <── [ ADAPT ] <── [ MEASURE ] <────────┘
```

1. **UNDERSTAND**: Ingest user background, skills, resume, and target career role.
2. **ANALYZE**: Conduct precise skill-gap analysis against industry market requirements.
3. **PLAN**: Generate personalized, milestone-driven learning paths.
4. **ACT**: Deliver targeted resources, contextual practice tasks, and challenges.
5. **MEASURE**: Evaluate performance on practice tasks and assessments.
6. **ADAPT**: Detect persistent weaknesses and recalculate/refine the learning trajectory.
7. **REPEAT**: Continuously monitor and elevate learner competencies.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS (Modern, dark AI SaaS design system)
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios
- **Animations & Graphics**: Framer Motion
- **Data Visualization**: Recharts
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.10+ & FastAPI
- **Data Validation & Schemas**: Pydantic v2
- **Database**: MongoDB (Atlas compatible) via PyMongo & Motor
- **Authentication**: JWT Foundation (python-jose & passlib)
- **Environment Management**: python-dotenv & pydantic-settings

### AI Layer Architecture
- **Provider Abstraction**: Decoupled LLM interface (`BaseAIProvider`) supporting multiple backends (OpenAI, Anthropic, Ollama, etc.)
- **Agent Architecture**: Modular multi-agent engine (`BaseAgent`) supporting tool execution, memory state, and trace logging.

---

## 📂 Repository Structure

```
edupath/
│
├── frontend/             # React + Vite application shell & UI components
│   ├── public/
│   ├── src/
│   │   ├── assets/       # Static assets & graphics
│   │   ├── components/   # Reusable design system UI components
│   │   ├── constants/    # Global configuration & constants
│   │   ├── context/      # React context providers
│   │   ├── hooks/        # Custom React hooks
│   │   ├── layouts/      # Main & Dashboard layout containers
│   │   ├── pages/        # Application views (Landing, Dashboard)
│   │   ├── routes/       # App routing definition
│   │   ├── services/     # API services & HTTP handlers
│   │   ├── styles/       # Tailwind CSS & global design tokens
│   │   └── utils/        # Helper functions
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── backend/              # FastAPI backend server
│   ├── app/
│   │   ├── api/          # Route handlers & API version router (/api/v1)
│   │   ├── core/         # Config, security, database initialization
│   │   ├── middleware/   # CORS & exception handling middleware
│   │   ├── models/       # Database models
│   │   ├── repositories/ # Data access abstraction layer
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── services/     # Core domain business logic
│   │   ├── utils/        # Utility helpers & logging
│   │   └── main.py       # FastAPI application entrypoint
│   ├── tests/            # Pytest suite
│   ├── requirements.txt
│   └── README.md
│
├── ai/                   # AI & Agent Abstraction Layer
│   ├── agents/           # Specialized agent implementations
│   │   ├── orchestrator/
│   │   ├── profile/
│   │   ├── skill_gap/
│   │   ├── learning_planner/
│   │   ├── resource/
│   │   ├── practice/
│   │   ├── assessment/
│   │   ├── progress/
│   │   └── adaptation/
│   ├── providers/        # LLM Provider abstractions
│   ├── tools/            # Agent tool definitions
│   ├── memory/           # Agent state & memory handlers
│   ├── prompts/          # System prompt templates
│   ├── workflows/        # Multi-agent graph workflows
│   ├── schemas/          # Agent input/output schemas
│   └── README.md
│
├── docs/                 # Project & Architecture Documentation
│   ├── architecture/     # System architecture specifications
│   ├── agents/           # Agent system specifications
│   ├── api/              # OpenAPI specs & guidelines
│   ├── database/         # MongoDB schemas & index design
│   ├── product/          # Product specs & roadmap
│   └── development/      # Local setup & developer guides
│
├── .gitignore
├── .env.example
└── README.md
```

---

## ⚡ Quick Start & Local Setup

### Prerequisites
- Node.js v18+ and npm v9+
- Python 3.10+ and pip
- MongoDB (Local instance or MongoDB Atlas URI)

### 1. Environment Configuration
Copy `.env.example` to create your local `.env` file in the root directory:

```bash
cp .env.example .env
```

Ensure `.env` contains your backend and frontend configuration options.

### 2. Running the Backend Server

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI dev server with auto-reload
uvicorn app.main:app --reload --port 8000
```

The backend server will start at `http://localhost:8000`. You can inspect the health check at `http://localhost:8000/api/v1/health` and API docs at `http://localhost:8000/docs`.

### 3. Running the Frontend Server

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

The frontend application will be running at `http://localhost:5173`.

---

## 🔐 Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MONGODB_URI` | MongoDB connection URI | `mongodb://localhost:27017` |
| `MONGODB_DATABASE` | Target database name | `edupath` |
| `JWT_SECRET` | Secret key for JWT signing | `change_me` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `LLM_PROVIDER` | Active LLM provider driver | `openai` |
| `LLM_API_KEY` | Provider API Key | `""` |
| `FRONTEND_URL` | Allowed frontend origin for CORS | `http://localhost:5173` |
| `BACKEND_URL` | Backend server base URL | `http://localhost:8000` |

---

## 🤖 Future Agent Architecture

EduPath's agent layer is built around an **Orchestrator Agent** coordinating 8 specialized sub-agents:

1. **Profile Agent**: Analyzes resumes and target career roles to construct dynamic learner profiles.
2. **Skill Gap Agent**: Performs granular gap analysis against real-time market requirements.
3. **Learning Planner Agent**: Generates milestone-driven personalized roadmaps.
4. **Resource Agent**: Discovers and ranks high-quality learning resources.
5. **Practice Agent**: Crafts contextual coding tasks and project challenges.
6. **Assessment Agent**: Evaluates submitted work with detailed rubrics.
7. **Progress Agent**: Tracks mastery levels and retention across skills.
8. **Adaptation Agent**: Modifies upcoming learning milestones based on detected weaknesses.

---

## 📊 Project Status (Phase 0 — Foundation)

- [x] High-level multi-package repository setup
- [x] Modern AI SaaS frontend shell (React + Vite + Tailwind CSS)
- [x] FastAPI API-first server foundation with `/api/v1/health`
- [x] MongoDB resilience connection infrastructure
- [x] LLM Provider abstraction (`BaseAIProvider`)
- [x] Modular Agent framework (`BaseAgent`)
- [x] System, Agent, and Setup documentation

---

## 📄 License

Developed for the Agentic AI Hackathon 2026. All rights reserved.
