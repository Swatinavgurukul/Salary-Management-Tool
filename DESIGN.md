# Design Document — Salary Management Tool

## Architecture Overview

```
┌─────────────┐        /api proxy        ┌──────────────┐       ┌────────────┐
│   React UI  │  ───────────────────────► │  FastAPI     │ ────► │   SQLite   │
│  (Vite/TS)  │  :5173                    │  Backend     │       │     DB     │
│             │  ◄─────────────────────── │  :8000       │ ◄──── │            │
└─────────────┘       JSON responses      └──────────────┘       └────────────┘
```

**Frontend:** React 19 + TypeScript, bundled with Vite. Communicates with the backend through a `/api` reverse proxy in development.

**Backend:** FastAPI with SQLAlchemy ORM. Single `employees` table in SQLite. Three-layer architecture: routers (HTTP controllers) → services (business logic) → models (DB). Organized into routers (`employees`, `insights`) and services (`employee_service`, `insight_service`) for clean separation of concerns.

**Database:** SQLite — chosen for zero-infrastructure local development. The `salary > 0` CHECK constraint enforces data integrity at the DB level, in addition to Pydantic schema validation.

## Key Design Decisions

### 1. Two Layers of Validation
- **Pydantic schemas** catch invalid data at the API boundary (required fields, `salary > 0`, email format, string lengths).
- **SQLAlchemy model** enforces constraints at the DB level (`NOT NULL`, `UNIQUE email`, `CHECK salary > 0`).
- **Why:** Defense in depth. Schema validation gives friendly 422 errors; DB constraints prevent data corruption even if someone bypasses the API.

### 2. Server-Side Pagination + Search
- `GET /employees` returns `{items, total, page, page_size}` instead of a flat array.
- Server-side `ILIKE` search across name, title, country, department, email.
- **Why:** With 10,000 employees, sending all rows to the frontend is impractical. Server-side pagination keeps responses fast and memory-efficient.

### 3. Aggregate Queries for Insights
- Insights use SQL `MIN/MAX/AVG/COUNT` with `GROUP BY` — computed in the database, not in Python.
- **Why:** The database engine is optimized for aggregation over large datasets. For 10k rows, this is significantly faster than fetching all rows and computing in application code.

### 4. Case-Insensitive Filtering
- Country and job title filters use `func.lower()` for case-insensitive matching.
- **Why:** User experience — an HR manager shouldn't need to know the exact capitalization stored in the DB.

### 5. Idempotent Seed Script
- `seed.py` clears existing data before inserting, making it safe to run repeatedly.
- Uses bulk `INSERT` in batches of 1,000 rows for performance (~0.11s for 10k records).
- Names generated from `first_names.txt × last_names.txt` = 10,000 unique combinations.

## Test-Driven Development (TDD) Approach

Every feature followed the Red-Green-Refactor cycle:

1. **RED:** Write failing tests that define the expected behavior.
2. **GREEN:** Write the minimum code to make tests pass.
3. **REFACTOR:** Clean up while keeping tests green.

### Test Distribution

| Layer | Framework | Tests | What's Covered |
|-------|-----------|-------|---------------|
| Model | pytest | 13 | Employee fields, DB constraints, salary validation |
| CRUD API | pytest | 35 | POST/GET/PUT/DELETE, validation errors, 404/409/422 |
| Insights API | pytest | 26 | Country/job/department/headcount/top-earners aggregates |
| Pagination | pytest | 8 | Page/size params, search, empty pages |
| Edge Cases | pytest | 27 | Boundary values, special chars, field limits |
| Seed Script | pytest | 13 | Name loading, generation, uniqueness, field correctness |
| Frontend | Vitest | 29 | Page rendering, forms, loading/error states, nav, sections |

**Total: 151 tests**, all deterministic and fast (~3.7s total runtime).

### Test Design Principles
- **In-memory SQLite** for test DB — no file I/O, instant setup/teardown.
- **Isolated fixtures** — each test gets a fresh DB via `create_all`/`drop_all`.
- **API mocks** in frontend tests — no network calls, tests run in < 2s.

## Performance Considerations

| Operation | Approach | Time |
|-----------|----------|------|
| Seed 10k rows | Bulk INSERT, 1000-row batches | ~0.11s |
| List employees | Server-side pagination (20/page) | < 10ms |
| Insights queries | SQL aggregates, indexed columns | < 5ms |
| Frontend search | Server-side ILIKE, debounced | < 10ms |

### Database Indexes
All frequently queried columns are indexed: `full_name`, `job_title`, `country`, `department`. The `email` column has a unique index.

## Trade-offs

| Decision | Pros | Cons |
|----------|------|------|
| SQLite over PostgreSQL | Zero setup, single file, fast for 10k rows | No concurrent writes, limited to single-server deployment |
| Plain CSS over component library | No extra dependencies, fast build, full control | More manual work for complex UIs |
| Server-side search over client-side | Scales with data size, consistent with pagination | Extra round-trip per search query |
| Pydantic v2 over v1 | Better performance, `model_validate`, cleaner syntax | Requires Python 3.9+ compatibility adjustments |

## API Endpoints Summary

| Method | Path | Description |
|--------|------|-------------|
| POST | `/employees` | Create employee |
| GET | `/employees` | List with pagination + search |
| GET | `/employees/{id}` | Get single employee |
| PUT | `/employees/{id}` | Update employee (partial) |
| DELETE | `/employees/{id}` | Delete employee |
| GET | `/insights/country/{country}` | Salary stats for a country |
| GET | `/insights/job?job_title=&country=` | Salary stats for job title |
| GET | `/insights/department` | Breakdown by department |
| GET | `/insights/headcount` | Employee count by country |
| GET | `/insights/top-earners?limit=` | Highest paid employees |
| GET | `/health` | Health check |
