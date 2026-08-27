# ✧ EchoLog | Smart AI Journal API

EchoLog is a meticulously structured REST API that transforms daily journaling into actionable insights. Built with FastAPI and a strict Domain-Driven architecture, it leverages the Google GenAI SDK to automatically analyze, summarize, and extract mood markers from manual diary entries while strictly isolating core business logic from AI integrations.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-Database-blue?style=for-the-badge)](https://sqlmodel.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google_GenAI-Sparkle-orange?style=for-the-badge)](https://ai.google.dev/)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)]()

## Core Features

- **Resource-Based Architecture:** Domain-driven layout separating HTTP routers, business services, Pydantic schemas, and SQLModel databases into isolated modules.
- **AI Generative Layer:** Utilizes `google-genai` (Gemini 2.5 Flash) for automated sentiment analysis, mood tagging, and single-sentence summarization of raw text entries.
- **Strict Data Hydration:** Enforces `model_validate()` for entity creation and `model_dump(exclude_unset=True)` for partial updates to ensure database parity.
- **Granular Authorization:** Implements stateless JWT authentication via PyJWT and bcrypt password hashing, natively enforcing row-level database ownership per user.
- **Monetization Ready:** Features an isolated webhook gateway with cryptographic signature validation to gate premium AI generation features behind active subscriptions.
- **Centralized Error Handling:** Employs a polymorphic base exception pattern (`DomainException`) to catch service-layer violations and format them uniformly without polluting routing logic.

## Architecture

EchoLog utilizes a vertically sliced, resource-based directory structure (inspired by NestJS) to ensure horizontal scalability.

```text
echolog/
├── pyproject.toml
└── src/
    └── echolog/
        ├── main.py              # Entry point & global exception handlers
        ├── database.py          # SQLite/PostgreSQL engine and session yielding
        ├── core/
        │   ├── security.py      # JWT encoding/decoding and Bcrypt hashing
        │   └── exceptions.py    # Base DomainException definitions
        └── modules/
            ├── users/           # User lifecycle & authentication
            ├── entries/         # Journal CRUD, manual transaction state
            │   ├── router.py    # Thin HTTP traffic controllers
            │   ├── service.py   # Explicit database & AI orchestration
            │   ├── models.py    # SQLModel entities (table=True)
            │   └── schemas.py   # Pydantic DTOs for request validation
            ├── analysis/        # Google GenAI prompt orchestration
            └── billing/         # Checkout sessions and webhook validation
```
