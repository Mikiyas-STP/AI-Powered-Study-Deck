# AI-Powered Study Deck (PAPR Stack)

A professional-grade study tool that leverages AI to transform raw notes into structured flashcards using a Spaced Repetition System (SRS) foundation.

## 🌟 Key Features
- **AI Generation:** Asynchronously transforms raw text into JSON-structured flashcards.
- **Stateless Authentication:** Secure JWT-based auth flow with Bcrypt password hashing.
- **Relational Data Modeling:** Complex PostgreSQL schema with ownership-based authorization.
- **Spaced Repetition Ready:** Database schema includes `ease_factor`, `interval`, and `next_review_date` for future SRS implementation.
- **Modern UI:** Responsive Dashboard and Deck views built with React, Tailwind CSS, and Lucide icons.

## 🏗️ Technical Architecture (The "PAPR" Stack)
- **Python (FastAPI):** High-performance asynchronous backend with Pydantic for strict data validation.
- **PostgreSQL:** Relational storage with UUIDs for primary keys to prevent IDOR vulnerabilities.
- **SQLAlchemy 2.0:** Modern ORM using the latest Type-Hinted mapping style.
- **React:** Component-based UI with Axios interceptors for seamless JWT management.

## 🛠️ Setup & Installation

### Backend
1. `cd backend`
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Create a `.env` file (see `app/core/config.py` for required variables).
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## 🧪 Testing
The backend maintains a high standard of reliability with automated integration tests:
```bash
cd backend
pytest