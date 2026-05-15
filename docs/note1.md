This explanation is for the work before this commit. well explained for a reference
Let's take a step back and look under the hood of what we built in Sprints 1, 2, and 3.

---

### 1. The Folders and Files (What they do)

We are using a **Domain-Driven / Modular Architecture**. Instead of putting everything in one massive file,we separate concerns.

*   **`app/main.py`**: The entry point of your application. Think of it as the front desk of a building. It sets up the FastAPI app, configures CORS (so React is allowed in), and registers your routers (telling the app where the endpoints live).
*   **`app/core/`**: The brain for application-wide settings and utilities.
    *   `config.py`: Loads and validates your `.env` variables. If a database password is missing, it crashes the app safely before it even starts.
    *   `security.py`: Holds the cryptography logic (hashing passwords, generating JWTs). We keep this isolated so our API routes don't get cluttered with math and encryption code.
*   **`app/db/`**: The database engine room.
    *   `session.py`: Manages the connection pool to PostgreSQL. It provides the `get_db` function, which opens a database connection when a request comes in and safely closes it when the request is done.
    *   `base_class.py`: The foundation for our SQLAlchemy models.
*   **`app/models/` (SQLAlchemy)**: These files (`user.py`, `deck.py`, `flashcard.py`) represent your **Database Tables**. They dictate how data is stored on the hard drive in PostgreSQL.
*   **`app/schemas/` (Pydantic)**: These files represent your **JSON Data**. They dictate what data React is allowed to send to the API, and what data the API is allowed to send back to React. *(Note: Separating Models and Schemas is the most important concept in FastAPI).*
*   **`app/api/`**: The actual API endpoints (URLs).
    *   `auth.py`: The routes for `/register`, `/login`, and `/me`.
    *   `deps.py`: "Dependencies". Reusable blocks of code that run *before* your route logic. For example, `get_current_user` checks the JWT token before letting someone access the `/me` route.
*   **`alembic/` & `alembic.ini`**: The version control system for your database. When you change a model, Alembic writes the SQL commands to update PostgreSQL without deleting your existing data.

---

### 2. The System Flow (How they talk to each other)

Let's trace exactly what happens when your React app sends a request to `POST /api/v1/auth/register`:

1.  **The Request Arrives:** React sends a JSON payload `{"email": "test@test.com", "password": "123"}` to your server.
2.  **The Front Desk (`main.py`):** FastAPI receives it, checks CORS, and routes it to the `auth_router`.
3.  **Validation (`schemas/user.py`):** Before your code even runs, FastAPI passes the JSON to the `UserCreate` Pydantic schema. Pydantic checks: *Is the email a valid email format? Is the password a string?* If no, it instantly throws a 422 Error back to React. If yes, it proceeds.
4.  **Dependency Injection (`db/session.py`):** The route asks for `db: Session = Depends(get_db)`. FastAPI pauses, goes to `session.py`, grabs a live PostgreSQL connection, and hands it to your route.
5.  **Business Logic (`api/auth.py` & `core/security.py`):** Your route checks if the email exists. It then calls `get_password_hash()` from `security.py` to encrypt the password.
6.  **Database Save (`models/user.py`):** You create a `User` SQLAlchemy model and tell the `db` session to commit it. The data is saved to PostgreSQL.
7.  **The Response (`schemas/user.py`):** You return the database object. FastAPI intercepts it, passes it through the `UserResponse` Pydantic schema (which strips out the password so you don't accidentally send it to React!), and sends the final JSON back to the client.

---

### 3. The Libraries (The Tools we used)

Here is exactly what the tools in your `requirements.txt` are doing:

*   **`fastapi`**: The web framework itself. It handles the routing, the dependency injection, and automatically generates the Swagger UI docs.
*   **`uvicorn`**: The ASGI server. FastAPI is just code; Uvicorn is the actual web server that listens on port 8000 and feeds HTTP requests into FastAPI.
*   **`sqlalchemy`**: The ORM (Object Relational Mapper). It allows us to write Python classes (`class User`) instead of writing raw SQL strings (`SELECT * FROM users`).
*   **`psycopg2-binary`**: The adapter. SQLAlchemy doesn't know how to talk to PostgreSQL directly. Psycopg2 is the driver that translates SQLAlchemy's commands into the exact binary protocol PostgreSQL understands.
*   **`alembic`**: The database migration tool built by the creators of SQLAlchemy.
*   **`pydantic` & `pydantic-settings`**: The data validation library. It enforces type hints at runtime.
*   **`passlib[bcrypt]`**: The cryptography library we used to hash passwords so they aren't stored as plain text.
*   **`python-jose`**: The library we used to encode and decode the JSON Web Tokens (JWTs) for authentication.

---

Take your time to read through this. If you can visualize this flow, building the rest of the application will be incredibly easy because every single feature (Decks, Flashcards, AI generation) will follow this exact same pattern.
