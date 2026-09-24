# ✧ EchoLog | Trading Journal API

EchoLog is a meticulously structured REST API designed to track, manage, and evaluate manual trading journal entries. Built with FastAPI and a strict Domain-Driven architecture, it isolates core business logic from routing, ensuring high performance, strict validation, and granular data ownership.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-Database-blue?style=for-the-badge)](https://sqlmodel.tiangolo.com/)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)]()

## Core Features

- **Resource-Based Architecture:** Domain-driven layout separating HTTP routers, business controllers, Pydantic schemas, and SQLModel databases into isolated modules.
- **Strict Data Hydration:** Enforces strict Pydantic validation for entity creation and `model_dump(exclude_unset=True)` for partial updates to ensure database parity.
- **Granular Authorization:** Implements stateless secure cookie authentication via PyJWT and pwdlib password hashing, natively enforcing row-level database ownership per user.
- **Monetization Ready:** Features an isolated webhook gateway to gate premium features behind active subscriptions.
- **Centralized Error Handling:** Employs a polymorphic base exception pattern (`APIException`) to catch service-layer violations and format them uniformly without polluting routing logic.

## Architecture

EchoLog utilizes a vertically sliced, resource-based directory structure to ensure horizontal scalability and maintainability.

```text
echolog/
├── pyproject.toml
└── src/
    └── echolog/
        ├── main.py              # Entry point & global exception handlers
        ├── core/
        │   ├── config.py        # Application configuration
        │   ├── exceptions.py    # Base exception classes
        │   ├── security.py      # pwdlib hashing
        │   ├── jwt.py           # PyJWT logic
        │   └── database.py      # Database session management
        │
        ├── users/               # User lifecycle & authentication
        ├── payments/            # Payment processing & subscription management
        ├── entries/             # Trading journal CRUD operations
        │   ├── routes.py        # Thin HTTP traffic controllers
        │   ├── controllers.py   # Explicit database orchestration
        │   ├── models.py        # SQLModel entities (table=True)
        │   ├── exceptions.py    # Domain specific errors
        │   └── schemas.py       # Pydantic DTOs for request validation