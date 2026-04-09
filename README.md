# Salary Management Tool

A minimal yet usable salary management tool for an organization with 10,000 employees.  
Built for the **HR Manager** persona.

## Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Backend  | FastAPI + SQLAlchemy + SQLite |
| Frontend | React + TypeScript (Vite)   |
| Testing  | pytest (backend), Vitest (frontend) |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI application entry point
│   │   ├── models.py      # SQLAlchemy ORM models
│   │   ├── schemas.py     # Pydantic request/response schemas
│   │   └── database.py    # DB engine & session setup
│   ├── tests/             # pytest test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # Root component
│   │   └── App.test.tsx   # Component tests
│   └── package.json
└── README.md
```

## Getting Started

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v        # run tests
uvicorn app.main:app --reload     # start dev server on :8000
```

### Frontend

```bash
cd frontend
npm install
npm test          # run tests
npm run dev       # start dev server on :5173
```

## Development Approach

This project follows **Test-Driven Development (TDD)**: write a failing test first, implement just enough code to pass it, then refactor. Commit history reflects this red-green-refactor cycle.
