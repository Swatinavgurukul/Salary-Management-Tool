# Salary Management Tool

A minimal yet usable salary management tool for an organization with 10,000 employees.
Built for the **HR Manager** persona.

## Tech Stack

| Layer    | Technology                      |
|----------|---------------------------------|
| Backend  | FastAPI + SQLAlchemy + SQLite   |
| Frontend | React 19 + TypeScript (Vite)    |
| Testing  | pytest (backend), Vitest (frontend) |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models.py            # SQLAlchemy Employee model
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── database.py          # DB engine & session
│   │   └── routers/
│   │       ├── employees.py     # CRUD endpoints (paginated)
│   │       └── insights.py      # Salary analytics endpoints
│   ├── tests/                   # 98 pytest tests
│   ├── data/
│   │   ├── first_names.txt      # 100 first names for seeding
│   │   └── last_names.txt       # 100 last names for seeding
│   ├── seed.py                  # Bulk-insert 10k employees
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # EmployeeList, EmployeeForm, Insights
│   │   ├── api/client.ts        # Axios API client
│   │   └── types/employee.ts    # TypeScript interfaces
│   └── package.json
├── DESIGN.md                    # Architecture, trade-offs, TDD approach
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Seed 10,000 employees
python seed.py

# Start dev server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

# Run tests
npm test

# Start dev server (proxies /api to backend on :8000)
npm run dev
```

Then open http://localhost:5173.

### Run Both Together

Open two terminals:

```bash
# Terminal 1 — Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd frontend && npm run dev
```

## Features

### Employee Management
- View paginated employee list with server-side search
- Add, edit, and delete employees
- Validated fields: name, job title, country, salary (> 0), department, email (unique)

### Salary Insights
- **Country insights:** min/max/avg salary and headcount for any country
- **Job title insights:** average salary by role, optionally filtered by country
- **Department breakdown:** aggregate stats per department
- **Headcount by country:** employee distribution across countries
- **Top 10 earners:** highest paid employees in the organization

## Testing

111+ tests covering model validation, all API endpoints, pagination, seed script, and frontend components.

```bash
# Backend (98 tests, ~1s)
cd backend && python -m pytest tests/ -v

# Frontend (16 tests, ~1.5s)
cd frontend && npm test
```

## Development Approach

This project was built using **Test-Driven Development (TDD)** with incremental commits. See [DESIGN.md](DESIGN.md) for architecture decisions, trade-offs, and performance considerations.
