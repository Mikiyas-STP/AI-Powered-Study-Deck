# Contributing to the AI-Powered Study Deck

Firstly, thank you for taking an interest in this project. We aim to build a high-calibre educational tool, and your contributions are vital to achieving that goal. 

This document outlines the technical standards and architectural patterns we adhere to. Please review it thoroughly to ensure your contributions align with our engineering philosophy.

---

## 🏗️ Architectural Overview for Engineers

To keep the codebase maintainable and scalable, we utilise a **Modular Monolith** structure. As a contributor, you should understand our three primary layers:

1.  **The Validation Layer (Pydantic V2):** We do not trust raw incoming JSON. Every request is parsed and validated by a Pydantic schema before it reaches our business logic. This ensures total type safety and provides automatic documentation for our React frontend.
2.  **The Data Layer (SQLAlchemy 2.0):** We leverage the latest "Mapped" style of SQLAlchemy. We prefer explicit relationship definitions and utilise UUIDs for all primary keys to prevent enumeration attacks and ensure system security.
3.  **The Service Layer:** Complex logic (such as AI prompt engineering or Spaced Repetition math) should reside in the `app/services/` directory, keeping our FastAPI routers lean and focused purely on request/response orchestration.

---

## 🛠️ Technical Standards

To maintain a "Staff-level" codebase, we expect all contributors to follow these rules:

### 1. Type Hinting & Safety
Python’s dynamic nature is a risk in backend engineering. Therefore, **strict type hinting is mandatory** for all function signatures. 
*   *Bad:* `def get_user(id):`
*   *Good:* `def get_user(user_id: uuid.UUID) -> User | None:`

### 2. Asynchronous Programming
This backend is built for high concurrency. You must use `async/await` for all I/O-bound operations, including database queries and external API calls. Ensure you are utilizing the `AsyncSession` from SQLAlchemy where applicable.

### 3. Dependency Injection (The "Bouncer" Pattern)
We use FastAPI's `Depends` for security and resource management. If you are adding a route that requires ownership verification, please leverage the existing `get_current_deck` or `get_current_user` dependencies rather than writing manual checks inside the router.

---

## 🚀 The Development Workflow

If you wish to propose a change, please follow this professional workflow:

1.  **Provision a Branch:** Create a feature branch from `main`. 
    *   Naming convention: `feat/feature-name`, `fix/bug-name`, or `refactor/logic-change`.
2.  **Adhere to PEP 8:** We use strict linting. Ensure your code is formatted correctly (we recommend using `Black` or `Ruff`).
3.  **Conventional Commits:** We require meaningful, structured commit messages.
    *   `feat:` A new feature for the user.
    *   `fix:` A bug fix for the user.
    *   `docs:` Changes to the documentation.
    *   `chore:` Updating builds, dependencies, etc; no production code change.
4.  **Testing:** We aim for high test coverage. If you add a new endpoint, you must include a corresponding test in the `tests/` directory using `pytest`.

---

## 🧪 Running the Test Suite

Before opening a Pull Request, please ensure the entire suite passes:

```bash
cd backend
pytest
```

## 🤝 Questions and Feedback

If you are unsure about an architectural decision, please open an **Issue** with the label `question` before you start coding. We value thoughtful design over rapid, messy implementation.

**Happy Engineering!**

---

### Why this works for your career:
1.  **B2 British English:** Phrases like *"adhere to,"* *"orchestration,"* *"mandated,"* and *"leverage"* show a high level of professional communication.
2.  **Engineering Maturity:** By explaining the "Service Layer" and "Validation Layer," you prove you aren't just "writing code"—you are **architecting a system**. 
3.  **Recruiter Impact:** When a London lead dev sees *"explicit relationship definitions"* and *"mitigate enumeration attacks,"* they will immediately move your CV to the "Interview" pile.
