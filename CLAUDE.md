# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A salary management tool for HR Managers. Backend: Django 6 + DRF + PostgreSQL. Frontend: ReactJS (not yet scaffolded). Planned deployment: Railway (backend), Vercel (frontend).

## Backend Setup

All backend commands run from `backend/`. Dependencies are managed with `uv`.

```bash
cd backend
uv sync                   # install dependencies
uv run python manage.py migrate
uv run python manage.py runserver
```

Copy `env.example` to `.env` and fill in: `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`. Requires Python 3.14+.

## Running Tests

```bash
cd backend
uv run pytest                              # all tests
uv run pytest apps/employees/tests/test_models.py   # single file
uv run pytest -k "test_employee_can_be_created"     # single test
```

Tests require a real PostgreSQL database (no mocking). `pytest.ini` sets `DJANGO_SETTINGS_MODULE = config.settings`.

## Linting & Formatting

```bash
cd backend
uv run ruff check .       # lint
uv run ruff format .      # format
```

Code style: **tabs** for indentation, **double quotes** for strings, 88-char line length. Migrations are excluded from ruff.

## Architecture

```
salary_management/
├── backend/
│   ├── apps/
│   │   └── employees/       # only app so far
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── migrations/
│   │       └── tests/
│   └── config/              # Django project config (settings, urls, wsgi)
└── frontend/                # ReactJS (not yet scaffolded)
```

`INSTALLED_APPS` ordering matters: `PROJECT_APPS` first, then `DJANGO_APPS`, then `THIRD_PARTY_APPS` (see `config/settings.py`).

## Employee Model

- Primary key: `UUIDField` using `uuid.uuid7` (time-ordered)
- Soft delete: set `employment_status = Inactive` instead of deleting rows
- Indexes on `(first_name, last_name)`, `job_title`, and `(country, job_title)` for salary insights queries
- `salary` is in USD as `DecimalField(max_digits=10, decimal_places=2)`

## Planned API Endpoints (from ARCHITECTURE.md)

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/api/employees/` | List / create |
| GET/PUT/PATCH/DELETE | `/api/employees/{id}/` | Retrieve / update / deactivate |
| GET | `/api/employees/insights/` | Salary stats (min, max, avg) by country/job title |
| POST | `/api/employees/import/` | Seed 10k employees |

## Test Fixtures

`backend/conftest.py` provides two shared pytest fixtures:
- `employee_data` — dict of valid employee fields
- `employee` — a saved `Employee` instance (uses `@pytest.mark.django_db`)

## Development Workflow

This project follows TDD (red → green cycle). Write a failing test first, then implement. New apps go under `backend/apps/` and must be added to `PROJECT_APPS` in `config/settings.py`.
