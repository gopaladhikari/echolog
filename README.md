# ✧ EchoLog | Pro Trading Journal API

EchoLog is a meticulously structured REST API designed to track, manage, and evaluate manual trading journal entries. Built with FastAPI and a strict Domain-Driven architecture, it perfectly isolates core business logic from HTTP routing, ensuring high performance, strict data validation, and granular row-level data ownership.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-Database-blue?style=for-the-badge)](https://sqlmodel.tiangolo.com/)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)]()
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)]()

## Core Features

- **Resource-Based Architecture:** A highly scalable, domain-driven layout separating HTTP routers, business controllers, Pydantic schemas, and SQLModel databases into isolated modules (`users`, `entries`, `payments`).
- **Secure Identity Management:** Implements stateless, HTTP-only secure cookie authentication via PyJWT and modern password hashing using `pwdlib`. Natively enforces row-level database ownership so users can only access their own trades.
- **Automated SaaS Monetization:** Features a robust, webhook-driven payment gateway using the PayPal Server SDK. Automatically handles monthly/yearly subscription lifecycles, signature verification, and database syncing without requiring manual CRON jobs.
- **Freemium Business Logic:** Enforces usage caps directly at the controller level (e.g., Free users are limited to 20 trades per month), seamlessly upgrading them to unlimited access upon active PayPal subscription status.
- **Strict Data Hydration:** Enforces strict Pydantic validation for entity creation and `model_dump(exclude_unset=True)` for partial updates to ensure database parity.
- **Centralized Error Handling:** Employs a polymorphic base exception pattern (`APIException`) to catch service-layer violations (like `SubscriptionLimitExceededException`) and format them uniformly without polluting routing logic.

## Architecture & Directory Structure

EchoLog utilizes a vertically sliced, NestJS-inspired directory structure to ensure the codebase remains maintainable as it scales.

```text
echolog/
├── pyproject.toml
└── src/
    └── echolog/
        ├── main.py              # Entry point & global exception handlers
        ├── core/
        │   ├── config.py        # Environment variables & application config
        │   ├── exceptions.py    # Polymorphic base exception classes
        │   ├── security.py      # pwdlib cryptographic hashing
        │   ├── jwt.py           # PyJWT token generation & verification
        │   ├── resend.py        # Transactional email dispatcher
        │   └── database.py      # SQLite engine & session management
        │
        ├── users/               # Identity, Auth, and Account Management
        │
        ├── payments/            # Monetization & PayPal Integration
        │   ├── setup_paypal.py  # One-time script to generate PayPal Plan IDs
        │   ├── routes.py        # Webhook listener and checkout redirect endpoints
        │   └── controllers.py   # Cryptographic webhook signature validation
        │
        └── entries/             # Trading Journal CRUD & Business Logic
            ├── routes.py        # Thin HTTP traffic controllers
            ├── controllers.py   # Subscription limit enforcement & DB orchestration
            ├── models.py        # SQLModel entities (table=True)
            ├── exceptions.py    # Domain-specific errors (e.g., EntryNotFound)
            └── schemas.py       # Pydantic DTOs for strict request validation
```

## Local Setup & Development

**1. Environment Variables**
Create a `.env` file in the root directory and populate it with your specific keys:
```env
BASE_URL=https://your-ngrok-url.app
DATABASE_URL=sqlite:///echolog.db
ACCESS_TOKEN_SECRET_KEY=your_super_secret_key
RESEND_API_KEY=re_123456789
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_secret
PAYPAL_WEBHOOK_ID=your_paypal_webhook_id
PAYPAL_MONTHLY_PLAN_ID=P-12345... # Generated via setup_paypal.py
PAYPAL_YEARLY_PLAN_ID=P-67890...  # Generated via setup_paypal.py
```

**2. Generate PayPal Plans (One-Time Setup)**
Before running the server, generate your subscription plans in PayPal:
```bash
uv run python src/echolog/payments/setup_paypal.py
```
*Copy the outputted Plan IDs into your `.env` file.*

**3. Run the Server**
Start the FastAPI development server:
```bash
uv run fastapi dev src/echolog/main.py
```

## Test Credentials

To quickly test the authentication flow, you can register or use the following placeholder credentials:
* **Full Name:** Test User
* **Email:** user@echolog.com
* **Password:** Echolog123