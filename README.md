# Salary Management Tool

A minimal salary management tool for HR Managers to manage employees and view salary insights across countries, departments, and job titles.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.14, Django 6, Django REST Framework |
| Frontend | Next.js 16, TypeScript, Tailwind CSS, shadcn/ui |
| Database | PostgreSQL 17 |
| Deployment | Railway (backend), Vercel (frontend) |

## Quick Start (Docker)

The fastest way to run everything locally:

```bash
docker-compose up -d
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api |

To stop:

```bash
docker-compose down
```

To wipe the database volume too:

```bash
docker-compose down -v
```

## Local Development (without Docker)

### Backend

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
cd backend
cp env.example .env        # fill in SECRET_KEY and DB_* values
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Seed 10,000 employees:

```bash
uv run python manage.py seed_employees
```

Run tests:

```bash
uv run pytest
```

Lint / format:

```bash
uv run ruff check .
uv run ruff format .
```

### Frontend

Requires Node.js 22+.

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:3000. It expects the backend at `http://localhost:8000/api` by default. Override with a `.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/employees/?page=n` | Paginated employee list |
| POST | `/api/employees/` | Create employee |
| GET | `/api/employees/{id}/` | Retrieve employee |
| PUT | `/api/employees/{id}/` | Full update |
| PATCH | `/api/employees/{id}/` | Partial update |
| DELETE | `/api/employees/{id}/` | Soft delete (marks Inactive) |
| GET | `/api/employees/insights/` | Salary stats by country, department, title |

## Features

- Employee CRUD — add, view, edit, deactivate (soft delete)
- Salary insights — min / max / avg / median by country, department, and job title
- Paginated employee table with skeleton loading and empty states
- Seed script — generates 10,000 realistic employees in ~135 ms
- Bruno API collection at `bruno/`

## Project Structure

```
salary_management/
├── backend/
│   ├── apps/employees/      # models, views, serializers, tests
│   │   └── management/commands/seed_employees.py
│   └── config/              # Django settings, URLs
├── frontend/
│   └── src/
│       ├── app/             # Next.js pages (employees, insights)
│       ├── components/      # UI components
│       ├── lib/api.ts       # Axios API client
│       └── types/           # TypeScript types
├── bruno/                   # Bruno API collection
└── docker-compose.yml
```
