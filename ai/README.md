# EduPath AI & Agent Architecture Layer

This directory contains the core agent definitions, provider abstractions, memory management, tool definitions, and structured prompt templates for **EduPath**.

## Directory Overview

- `agents/`: Implementation classes for the Orchestrator and 8 specialized sub-agents.
- `providers/`: Decoupled interface (`BaseAIProvider`) abstracting LLM backends (OpenAI, Anthropic, Gemini, local models).
- `tools/`: Reusable agent tools for database operations, web retrieval, and assessment.
- `memory/`: Stateful memory providers tracking session context and learning histories.
- `prompts/`: Versioned system prompt templates.
- `workflows/`: Multi-agent pipeline definitions.
- `schemas/`: Pydantic structured output validation models.
