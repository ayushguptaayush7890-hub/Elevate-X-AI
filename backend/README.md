# Elevate X AI – Backend Infrastructure

This directory contains the Python FastAPI backend for **Elevate X AI**, an AI-powered career and vocational skills-matching platform.

---

## 1. Tech Stack

- **Runtime:** Python 3.12+ (Tested on Python 3.13)
- **API Framework:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **Validation & Settings:** [Pydantic v2](https://docs.pydantic.dev/latest/) + [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Database & ORM:** PostgreSQL 16 + [SQLAlchemy 2.0](https://www.sqlalchemy.org/) + [psycopg 3 binary](https://www.psycopg.org/psycopg3/)
- **Database Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Testing:** [Pytest](https://docs.pytest.org/) + [HTTPX](https://www.python-httpx.org/)

---

## 2. Directory Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint & lifespan
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic v2 settings & environment loader
│   │   ├── database.py          # SQLAlchemy 2.0 engine, SessionLocal, get_db
│   │   ├── logging.py           # Structured logging configuration
│   │   └── exceptions.py        # Centralized exception handlers
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py            # Master API router
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py        # /health and /health/database checks
│   ├── models/
│   │   ├── __init__.py          # Model exports & Base metadata
│   │   └── base.py              # TimestampMixin and DeclarativeBase
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── health.py            # Pydantic v2 response schemas
│   ├── services/
│   │   └── __init__.py          # Business logic layer (reserved for future phases)
│   └── repositories/
│       └── __init__.py          # Database access layer (reserved for future phases)
├── migrations/
│   ├── env.py                   # Alembic environment linked to Base.metadata
│   ├── script.py.mako           # Migration script template
│   └── versions/                # Database revision scripts
│       └── 0001_initial_baseline.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Isolated in-memory SQLite fixtures for Pytest
│   └── test_health.py           # Health, DB failure, CORS, & error handling tests
├── .env.example                 # Template for environment variables
├── .env                         # Local environment configuration
├── alembic.ini                  # Alembic configuration
├── docker-compose.yml           # PostgreSQL 16 container definition
├── requirements.txt             # Pinned backend dependencies
└── README.md                    # Backend documentation
```

---

## 3. Getting Started

### Prerequisites

- Python 3.12 or higher (`python3 --version`)
- Docker & Docker Compose (optional for local PostgreSQL)

### 3.1 Virtual Environment Setup

From the `backend/` directory:

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate virtual environment
# macOS / Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.2 Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Review and adjust variables in `.env` as needed:

| Variable | Default Value | Description |
|---|---|---|
| `APP_NAME` | `Elevate X AI API` | Application title |
| `APP_ENV` | `development` | Environment mode (`development` / `production`) |
| `DEBUG` | `true` | Debug flag |
| `API_V1_PREFIX` | `/api/v1` | URL prefix for version 1 API |
| `PORT` | `8000` | Local server port |
| `CORS_ORIGINS` | `["http://localhost:3000","http://localhost:3002"]` | Allowed CORS origins for Next.js |
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres_password@localhost:5432/elevate_x_ai` | Primary PostgreSQL connection string |

---

## 4. PostgreSQL Setup

### Option A: Using Docker Compose (Recommended)

Start the local PostgreSQL 16 container:

```bash
# Start PostgreSQL container in background
docker compose up -d

# View database container logs
docker compose logs -f postgres

# Stop PostgreSQL container
docker compose down
```

### Option B: Local PostgreSQL (Homebrew on macOS)

If Docker is unavailable:

```bash
# Install PostgreSQL 16 via Homebrew
brew install postgresql@16

# Start the PostgreSQL service
brew services start postgresql@16

# Create database and user
psql postgres -c "CREATE USER postgres WITH PASSWORD 'postgres_password';"
psql postgres -c "CREATE DATABASE elevate_x_ai OWNER postgres;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE elevate_x_ai TO postgres;"
```

---

## 5. Database Migrations (Alembic)

Alembic is configured to read the database URL dynamically from the Pydantic settings.

```bash
# Verify current migration status
alembic current

# Check latest head revision
alembic heads

# Apply all pending migrations to the database
alembic upgrade head

# Rollback one migration step
alembic downgrade -1

# Generate a new auto-detected migration (when models change in later phases)
alembic revision --autogenerate -m "describe_migration"
```

---

## 6. Running the API Server

Start the Uvicorn development server:

```bash
# From the backend directory with virtual environment activated:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server starts at `http://localhost:8000`.

### Interactive API Documentation

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON:** [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## 7. Health & Phase 2 API Endpoints

### 7.1 Health & Diagnostics

| Endpoint | Method | Status | Description |
|---|---|---|---|
| `/api/v1/health` | GET | `200 OK` | Verifies API runtime status, version, and timestamp. |
| `/api/v1/health/database` | GET | `200 OK` / `503 Service Unavailable` | Live query (`SELECT 1`) against PostgreSQL. **Never reports healthy if connection fails.** |
| `/api/health` | GET | `200 OK` | Convenience alias for frontend compatibility. |

### 7.2 Authentication & User Accounts

| Endpoint | Method | Auth Required | Description |
|---|---|---|---|
| `/api/v1/auth/register` | POST | No | Registers new user with bcrypt password and auto-initializes profile. |
| `/api/v1/auth/login` | POST | No | Authenticates user credentials, returns JWT access & refresh tokens. |
| `/api/v1/auth/logout` | POST | Yes | Blacklists the active JWT token identifier in `revoked_tokens`. |
| `/api/v1/auth/me` | GET | Yes | Retrieves authenticated user account metadata. |
| `/api/v1/auth/refresh` | POST | No | Issues a fresh access token using a valid refresh token. |
| `/api/v1/auth/forgot-password` | POST | No | Generates cryptographically secure password recovery token. |
| `/api/v1/auth/reset-password` | POST | No | Resets account password using issued token. |
| `/api/v1/auth/change-password` | POST | Yes | Authenticated password update verifying current password. |

### 7.3 Vocational Profiles, Education & Work Experience

| Endpoint | Method | Auth Required | Description |
|---|---|---|---|
| `/api/v1/profiles/me` | GET | Yes | Fetches user's own vocational profile. |
| `/api/v1/profiles/me` | PUT | Yes | Updates headline, bio, location, trade category, or experience. |
| `/api/v1/profiles/education` | GET | Yes | Lists user's vocational/academic education credentials. |
| `/api/v1/profiles/education` | POST | Yes | Adds a new education record. |
| `/api/v1/profiles/education/{id}` | DELETE | Yes | Deletes an education record (strict user isolation). |
| `/api/v1/profiles/experience` | GET | Yes | Lists workplace and informal trade experiences. |
| `/api/v1/profiles/experience` | POST | Yes | Logs a new formal or informal work experience. |
| `/api/v1/profiles/experience/{id}` | PUT | Yes | Updates an experience record owned by the user. |
| `/api/v1/profiles/experience/{id}` | DELETE | Yes | Deletes an experience record owned by the user. |
| `/api/v1/profiles/preferences` | GET / PUT | Yes | Retrieves or updates career target roles and salary range. |

### 7.4 Vocational Skills Catalog & User Profile Skills

| Endpoint | Method | Auth Required | Description |
|---|---|---|---|
| `/api/v1/skills` | GET | No | Searchable catalog of NSQF-aligned trade competencies. |
| `/api/v1/skills` | POST | No | Adds new standardized competency to global catalog. |
| `/api/v1/skills/{id}` | GET | No | Retrieves detailed metadata for a catalog skill. |
| `/api/v1/profiles/me/skills` | GET | Yes | Lists all competencies on user profile with verification status. |
| `/api/v1/profiles/me/skills` | POST | Yes | Adds skill (self-reported by default) to profile. |
| `/api/v1/profiles/me/skills/{id}` | PUT | Yes | Updates proficiency level, confidence, or verification status. |
| `/api/v1/profiles/me/skills/{id}` | DELETE | Yes | Removes skill from user profile. |
| `/api/v1/profiles/me/skills/{id}/evidence` | POST | Yes | Attaches practical assessment score; >= 80% upgrades to `assessed`. |

#### Example Responses

**`GET /api/v1/health`:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-11-14T12:51:45.201440Z",
  "environment": "development"
}
```

**`GET /api/v1/health/database` (Connected):**
```json
{
  "status": "healthy",
  "database": "connected",
  "dialect": "postgresql",
  "timestamp": "2026-11-14T12:51:45.214205Z",
  "error": null
}
```

**`GET /api/v1/health/database` (Disconnected):**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "dialect": null,
  "timestamp": "2026-11-14T12:51:45.214205Z",
  "error": "connection to server at '127.0.0.1', port 5432 failed: Connection refused"
}
```

---

## 8. Running Automated Tests

The Pytest suite runs against an in-memory SQLite database via `conftest.py`, ensuring tests execute independently of external database availability.

```bash
# Run test suite
pytest -v

# Run with coverage report
pytest --cov=app tests/
```

Test coverage includes:
- API health response structure
- Database connectivity check (both connected & 503 disconnected paths)
- CORS header verification for Next.js frontend origin (`http://localhost:3002`)
- OpenAPI specification schema availability
- Root documentation redirect
- Centralized 404 and validation error handling

