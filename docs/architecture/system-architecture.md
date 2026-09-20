# EduPath System Architecture

## Overview

EduPath is engineered following an **API-first, decoupled agentic architecture**. The application separates UI presentation, HTTP REST routing, business domain logic, database persistence, and AI agent execution into clear, single-responsibility layers.

```
┌─────────────────────────────────────────────────────────┐
│                     React + Vite UI                     │
│    (Landing Page, Dashboard, Practice UI, Recharts)     │
└────────────────────────────┬────────────────────────────┘
                             │ REST API (JSON over HTTP)
┌────────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                      │
│   (/api/v1 Routes, Security, Services, Repositories)    │
└──────────────┬────────────────────────────┬─────────────┘
               │                            │
               ▼                            ▼
┌────────────────────────────┐┌───────────────────────────┐
│       PyMongo Client       ││     AI Layer & Agents     │
│  (MongoDB Atlas Compatible)││ (Provider Abstraction,    │
└────────────────────────────┘│  Agent Orchestration)     │
                              └───────────────────────────┘
```

---

## Key Architecture Principles

1. **Separation of Concerns**: The Frontend does not invoke LLM APIs directly, nor does the AI layer touch MongoDB driver objects. Communication flows cleanly via defined schemas and interfaces.
2. **API-First REST Architecture**: All client actions execute via clean `/api/v1` routes backed by Pydantic models.
3. **AI Provider Decoupling**: AI capabilities interact with a `BaseAIProvider` abstraction. Switching providers (e.g., OpenAI, Anthropic, local models) requires changing configuration rather than modifying business code.
4. **Stateful Agent Memory**: Learner profiles, skill models, evaluation logs, and adaptation histories are stored persistently in MongoDB, allowing agents to operate contextually across sessions.
5. **Observability & Traceability**: Agent executions emit structured telemetry events capturing inputs, reasoning steps, tool usage, decisions, outputs, and execution timing.

---

## Core Domain Layering

- **Frontend (`frontend/`)**: React 18, Vite, Tailwind CSS, Framer Motion, Recharts. Communicates exclusively with the backend REST endpoints.
- **API Routes (`backend/app/api/`)**: Enforces authentication, request validation using Pydantic, error response formatting, and status code management.
- **Service Layer (`backend/app/services/`)**: Implements application workflows, coordinates database repositories, and triggers agent pipelines.
- **Repository Layer (`backend/app/repositories/`)**: Encapsulates raw database queries and MongoDB persistence operations.
- **AI Agent System (`ai/`)**: Defines agent interfaces, provider drivers, prompt templates, and autonomous agent state machines.
