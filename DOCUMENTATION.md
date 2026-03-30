# InnerEdge Developer Documentation

## First 15 Minutes (Onboarding)
Use this quick path when joining the project for the first time.

1. Run setup once.
Windows:
- `setup.bat`

Bash:
- `bash setup.sh`

2. Start services.
- Backend: `.venv/Scripts/python.exe manage.py runserver`
- Frontend:

```bash
cd frontend
npm install
npm run dev
```

3. Confirm app is reachable.
- Backend docs: <http://127.0.0.1:8000/api/docs/>
- Frontend: <http://127.0.0.1:3000/>

4. Seed local baseline data (fresh DB only).
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py seed_assets`
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py seed_plans`
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py seed_tags`

5. Create local test account.
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py shell`
- Then run the test-user snippet in the
   "Create a test account for development" section.

6. Run quality checks before first commit.
- Bash: `bash scripts/verify.sh`
- Windows: `scripts\verify.bat`

## Purpose
This guide is for developers working on InnerEdge after first startup.
It focuses on how to run the system, verify changes, and safely
modify backend and frontend code.

## Stack Summary
- Backend: Django, Django REST Framework, Channels, Celery
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Database: SQLite (local default option) or PostgreSQL
- Async and Realtime: Redis (Celery broker/result backend + Channels layer)

## Core Directories
- Project config and root URL routing: [config](config)
- Domain apps: [accounts](accounts), [market](market), [journal](journal),
  [intel](intel), [paper](paper), [alerts](alerts), [billing](billing)
- Frontend app: [frontend](frontend)
- Verification scripts: [scripts](scripts)

## Local Development Runbook

### 1. Backend and frontend startup
Windows:
1. Run setup once: `setup.bat`
2. Start backend: `.venv\Scripts\python.exe manage.py runserver`
3. Start frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

Bash:
1. Run setup once: `bash setup.sh`
2. Start backend: `.venv/Scripts/python.exe manage.py runserver`
3. Start frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

### 2. If you do not have PostgreSQL locally
Run backend commands with `DB_ENGINE=sqlite`.

Examples:
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py migrate`
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py runserver`

### 3. URLs to verify after startup
- Root (redirects to docs): <http://127.0.0.1:8000/>
- Swagger docs: <http://127.0.0.1:8000/api/docs/>
- Admin: <http://127.0.0.1:8000/admin/>
- Frontend: <http://localhost:3000>

## What To Do After The App Is Running

### Seed baseline data
Use these once in a fresh local DB:
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py seed_assets`
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py seed_plans`
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py seed_tags`

### Create an admin user
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py createsuperuser`

### Create a test account for development
Use this if you need a predictable local login for API and UI testing.

Create or update a test user:

```bash
DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py shell
```

Then run:

```python
from django.contrib.auth import get_user_model

User = get_user_model()
u, _ = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
u.set_password("demo12345")
u.is_staff = True
u.is_superuser = True
u.save()
print("demo user ready")
```

Suggested local test credentials:
- Username: `demo`
- Password: `demo12345`

Test authenticated API access:
- `curl -u demo:demo12345 http://127.0.0.1:8000/api/market/assets/`

### Validate full repo health
- Bash: `bash scripts/verify.sh`
- Windows: `scripts\verify.bat`

These scripts run backend tests and frontend quality gates.

## Service Health Checklist

Use this section to confirm all required services are running.

### Required for core local development
1. Backend server
2. Frontend dev server

Checks:
- Backend docs should return 200:
  - `curl -I http://127.0.0.1:8000/api/docs/`
- Frontend root should return 200:
  - `curl -I http://127.0.0.1:3000/`

### Required for async tasks and realtime features
1. Redis
2. Celery worker

Checks:
- Redis availability:
  - `command -v redis-server`
- Start worker:
  - `DB_ENGINE=sqlite .venv/Scripts/python.exe -m celery -A config worker -l info`

If Redis is not installed, backend and frontend can still run,
but queue/realtime features are limited.

## Backend Developer Workflow

Use this checklist when you are changing backend behavior.

1. Activate venv and use SQLite mode if no local Postgres.
2. Make model or API changes in the relevant app.
3. Run migrations if models changed.
4. Run focused tests first, then full suite.
5. Validate endpoint behavior in Swagger.

Command set:
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py makemigrations`
- `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py migrate`
- `.venv/Scripts/python.exe -m pytest alerts/tests.py -q`
- `.venv/Scripts/python.exe -m pytest -q`

## Frontend Developer Workflow

Use this checklist when you are changing frontend behavior.

1. Keep backend running in another terminal.
2. Develop in `frontend/src` using Vite dev server.
3. Run lint and type checks before build.
4. Confirm API calls and auth flows in browser.

Command set:
- `cd frontend`
- `npm run dev`
- `npm run lint`
- `npm run type-check`
- `npm run build`
- `npm run verify`

## Change Workflow (Recommended)

### 1. Before coding
1. Pull latest changes.
2. Create a branch.
3. Run baseline verify script once.

### 2. While coding
1. Keep backend server and frontend dev server running.
2. Run targeted tests frequently.
3. Run frontend `npm run verify` before commit.

### 3. Before commit
1. Run `bash scripts/verify.sh` or `scripts\verify.bat`.
2. Check migrations are created if models changed.
3. Update docs if behavior or commands changed.

## Common Developer Tasks

### A. Add or change a backend model
1. Edit model in the relevant app under [accounts](accounts),
   [market](market), [journal](journal), [intel](intel),
   [paper](paper), [alerts](alerts), or [billing](billing).
2. Create migration:
   - `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py makemigrations`
3. Apply migration:
   - `DB_ENGINE=sqlite .venv/Scripts/python.exe manage.py migrate`
4. Update serializer, viewset, and tests for the changed model.

### B. Add or change an API endpoint
1. Update serializer in the app `serializers.py`.
2. Update view logic in `views.py`.
3. Register route in app `urls.py`.
4. If needed, include app URLs in [config/urls.py](config/urls.py).
5. Validate in Swagger at `/api/docs/`.

### C. Add or change frontend UI behavior
1. Update component/page in [frontend/src](frontend/src).
2. Run `cd frontend && npm run lint`.
3. Run `cd frontend && npm run type-check`.
4. Run `cd frontend && npm run build`.

### D. Add a Celery task
1. Add task function in app `tasks.py`.
2. Ensure task is imported through autodiscovery (already configured in Django project).
3. Start worker:
   - `DB_ENGINE=sqlite .venv/Scripts/python.exe -m celery -A config worker -l info`
4. Trigger task from shell/view and confirm worker logs.

### E. Realtime alerts and Channels
1. Ensure Redis is available.
2. Start Django server with ASGI config (already wired).
3. Validate websocket routing from [config/routing.py](config/routing.py) and [alerts/consumers.py](alerts/consumers.py).

## Environment Variables You Will Usually Edit
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DB_ENGINE`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `REDIS_URL`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

See template: [.env.example](.env.example)

## Authentication Notes For API Testing
Most endpoints are protected.

Options:
1. Use admin/session login from browser.
2. Use Basic Auth in curl/Postman with a local superuser.

Example:
- `curl -u username:password http://127.0.0.1:8000/api/market/assets/`

## Quality Gates

### Backend
- Full suite: `.venv/Scripts/python.exe -m pytest -q`
- Single file: `.venv/Scripts/python.exe -m pytest alerts/tests.py -q`

### Frontend
From [frontend](frontend):
- `npm run lint`
- `npm run type-check`
- `npm run build`
- `npm run verify` (runs all three)

## Known Local Constraints
- If Redis is missing, core backend and frontend still run,
  but Celery and some realtime behavior are limited.
- If Docker is missing, use SQLite local mode and local process startup commands.

## Troubleshooting

### 404 at root path
Root is intentionally redirected to docs in [config/urls.py](config/urls.py).

### 403 from API
You are not authenticated for that endpoint.

### Celery worker fails at startup
1. Check `REDIS_URL`.
2. Check Redis availability (`command -v redis-server`).
3. If no Redis/Docker, skip worker-dependent tests locally.

### Frontend cannot call backend
1. Confirm backend is running on port 8000.
2. Confirm frontend dev server is running on port 3000.
3. Confirm proxy and API base URL settings in frontend configuration.

## Related Documentation
- Setup quick guide: [PROJECT_SETUP.md](PROJECT_SETUP.md)
- Testing details: [TESTING.md](TESTING.md)
- Frontend reference: [frontend/README.md](frontend/README.md)
- Delivery summary: [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
