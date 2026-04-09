# AI Tool Usage

This document describes how AI was used during the development of this project,
as required by the assessment.

## Tool

**Cursor IDE** with Claude as the AI pair-programming assistant.

## How AI Was Used

### 1. Test-Driven Development Workflow

AI accelerated the TDD cycle at every stage:

- **RED phase:** I described the feature requirements; AI generated comprehensive
  test cases — including edge cases I might have missed (negative salary, duplicate
  email, empty search, boundary pagination).
- **GREEN phase:** AI implemented the minimum code to pass the failing tests,
  respecting the existing project structure and conventions.
- **REFACTOR phase:** I directed the refactoring goals (e.g., "extract a services
  layer"); AI performed the mechanical extraction while I verified that all tests
  remained green.

### 2. Scaffolding & Boilerplate

- Initial project structure (FastAPI + React + Vite) was scaffolded with AI
  assistance, then reviewed and adjusted.
- Pydantic schemas, SQLAlchemy models, and TypeScript interfaces were generated
  from a description of the data model.
- The seed script's random-generation logic and bulk-insert batching were
  AI-assisted.

### 3. Code Review & Debugging

- When tests failed, I shared the error output with AI to diagnose the root cause
  (e.g., Python 3.9 not supporting `str | None` union syntax — fixed to
  `Optional[str]`).
- AI helped identify a miscount in `last_names.txt` (101 vs 100 entries) by
  cross-referencing test expectations.

### 4. Documentation

- `DESIGN.md` was drafted collaboratively: I outlined the decisions, AI structured
  them into a clear format with tables and diagrams.
- `README.md` was kept in sync with features as they were added.

## What I Controlled

- **Architecture decisions** — I chose the three-layer structure (routers →
  services → models), pagination strategy, and which extra metrics to build.
- **Feature scope** — I decided which insights to add beyond the minimum
  (department breakdown, headcount, top earners) based on what an HR Manager
  would find useful.
- **Quality gates** — I reviewed every generated test and implementation before
  committing, ensuring correctness and no unnecessary complexity.
- **Commit strategy** — I committed manually at each TDD boundary to show the
  evolution from failing tests → passing implementation → refactor.

## Outcome

Using AI as a pair programmer reduced boilerplate time significantly while
maintaining high test coverage (138 tests) and clean architecture. The key
benefit was rapid iteration through the Red-Green-Refactor cycle without
sacrificing code quality.
