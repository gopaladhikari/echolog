# EchoLog Development Roadmap

## Phase 1: The Architectural Foundation

_Goal: Establish the modular skeleton and database connection._

- **Initialize the Environment:** Use `uv` to set up the project and install `fastapi`, `sqlmodel`, and `uvicorn`.
- **Scaffold the Resource Structure:** Create the NestJS-style directory layout (`core`, `modules/users`, `modules/entries`, `modules/analysis`).
- **Configure SQLite:** In `database.py`, set up the synchronous SQLite engine (`create_engine`) and write the `get_session` dependency generator.

## Phase 2: Domain Entities & Validation

_Goal: Define the strict boundaries between database tables and API payloads._

- **Build the Base Model:** In `core/models.py`, create the `BaseModel` utilizing `sa_column_kwargs` for strict UTC `created_at` and `updated_at` database triggers.
- **Define SQLModel Entities:** In `entries/models.py` and `users/models.py`, create your `table=True` classes. Establish the explicit Foreign Key relationship between a User and their Journal Entries.
- **Construct Pydantic DTOs:** In `schemas.py` for both domains, build the strict data-transfer objects (`EntryCreate`, `EntryUpdate`, `EntryRead`).

## Phase 3: The Service Layer & Exception Handling

_Goal: Implement pure business logic without touching HTTP requests._

- **Centralize Exceptions:** Create the parent `DomainException` in `core/exceptions.py`, then build specific child errors (e.g., `EntryNotFoundError`) inside the `entries` module.
- **Build the CRUD Services:** In `entries/service.py`, write pure Python functions that accept Pydantic schemas, utilize `model_validate()` for creation and `model_dump(exclude_unset=True)` for updates, and execute manual `session.commit()` calls.
- **Wire the Global Handler:** In `main.py`, write the single `@app.exception_handler` to catch all `DomainException` triggers and translate them to HTTP responses.

## Phase 4: HTTP Routing & Pagination

_Goal: Expose the core application to the web securely._

- **Bind Routers:** Create `APIRouter` instances in `entries/router.py` and map them directly to your service functions.
- **Implement Advanced Queries:** Build the `GET /entries` endpoint. Accept optional `date` and `mood` query parameters, chaining the SQL `.where()` clauses before applying `.offset()` and `.limit()`.

## Phase 5: Identity & Row-Level Authorization

_Goal: Lock down the API so users only interact with their own data._

- **Password Cryptography:** Install `passlib` and build hashing/verification utilities in `core/security.py`. Update the `POST /users` flow to hash passwords before saving.
- **Stateless Sessions:** Install `PyJWT`. Build the login endpoint to return a signed JWT.
- **Dependency Injection Guard:** Create a `get_current_user` dependency that reads the JWT header, verifies it, and injects the active `User` object into your routes.
- **Enforce Data Ownership:** Update your `entries/service.py` to append `.where(JournalEntry.user_id == current_user.id)` to every single database query.

## Phase 6: Generative AI Orchestration

_Goal: Make the journal "smart" without blocking the core CRUD flow._

- **Initialize the SDK:** Add the `google-genai` SDK and configure the client in `analysis/service.py`.
- **Prompt Engineering:** Write the extraction function that commands the LLM to return a strict summary and mood tag.
- **Service Integration:** Update the `create_entry` service to intercept the raw text, pass it to the AI function, merge the generative response with the HTTP payload, and commit the final hybrid object to SQLite.
