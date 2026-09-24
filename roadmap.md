# EchoLog Development Roadmap

## Phase 1: The Architectural Foundation
*Goal: Establish the modular skeleton and database connection.*

* **Initialize the Environment:** Use `uv` to set up the project and install `fastapi`, `sqlmodel`, and `uvicorn`.
* **Scaffold the Resource Structure:** Create the domain-driven directory layout (`core`, `users`, `entries`, `payments`).
* **Configure SQLite:** In `database.py`, set up the synchronous SQLite engine (`create_engine`) and write the `get_session` dependency generator.

## Phase 2: Domain Entities & Validation
*Goal: Define the strict boundaries between database tables and API payloads.*

* **Define SQLModel Entities:** In `entries/models.py` and `users/models.py`, create your `table=True` classes. Establish the explicit Foreign Key relationship between a User and their Journal Entries.
* **Construct Pydantic DTOs:** In `schemas.py` for both domains, build the strict data-transfer objects (`CreateEntry`, `UpdateEntry`, `ReadEntry`, etc.).

## Phase 3: The Controller Layer & Exception Handling
*Goal: Implement pure business logic without touching HTTP requests.*

* **Centralize Exceptions:** Create the parent `APIException` in `core/exceptions.py`, then build specific child errors (e.g., `EntryNotFoundException`) inside the domain modules.
* **Build the CRUD Controllers:** In `entries/controllers.py`, write pure Python functions that accept Pydantic schemas, execute manual `session.commit()` calls, and manage entity state.
* **Wire the Global Handler:** In `main.py`, write the single `@app.exception_handler` to catch all `APIException` triggers and translate them into standardized JSON HTTP responses.

## Phase 4: HTTP Routing
*Goal: Expose the core application to the web securely.*

* **Bind Routers:** Create `APIRouter` instances in `entries/routes.py` and map them directly to your controller functions.
* **Implement REST Endpoints:** Build out the full lifecycle (`GET`, `POST`, `PATCH`, `DELETE`) for journaling trades.

## Phase 5: Identity & Row-Level Authorization
*Goal: Lock down the API so users only interact with their own data.*

* **Password Cryptography:** Install `pwdlib` and build hashing/verification utilities in `core/security.py`. Update the user registration flow to hash passwords.
* **Stateless Sessions:** Install `PyJWT`. Build the login endpoint to generate tokens and store them securely in HTTP-only cookies.
* **Dependency Injection Guard:** Create a `get_current_user` dependency that validates the JWT cookie and injects the active `User` object into protected routes.
* **Enforce Data Ownership:** Update `entries/controllers.py` to append `.where(Entries.user_id == user_id)` to database queries, guaranteeing strict data isolation between accounts.

## Phase 6: Generative AI Orchestration (Deferred)
*Goal: Make the journal "smart" by extracting insights from trade notes.*

* **Initialize the SDK:** Add the `google-genai` SDK and configure the client.
* **Prompt Engineering:** Write extraction functions that command the LLM to return strict summaries and psychological mood tags based on the user's manual notes.
* **Service Integration:** Create background tasks or dedicated analysis endpoints to process journal history asynchronously using Gemini.