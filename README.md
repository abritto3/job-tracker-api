# Job Tracker API

I've created a production-ready FastAPI backend for tracking job applications.  
The project demonstrates authentication, secure multi-user data access, CRUD operations, database migrations, automated testing, CI, Docker, and cloud deployment.


Tech stack: FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, GitHub Actions, JWT

----------------------------------------------------------------

FEATURES

- JWT authentication using OAuth2 password flow
- Secure, per-user job application tracking
- Full CRUD API for job applications
- Soft delete support
- Database migrations with Alembic
- Automated integration tests with pytest
- Dockerised local and production setup
- CI pipeline using GitHub Actions
- Cloud deployment ready (Render + managed PostgreSQL)

----------------------------------------------------------------

HIGH-LEVEL ARCHITECTURE

Client (Swagger UI or frontend)
  |
  v
FastAPI application
  - Authentication (JWT)
  - Business logic (CRUD)
  - Request validation
  |
  v
PostgreSQL database
  - Users
  - Job applications

Each request is authenticated via JWT and scoped to the current user.
Database schema changes are managed via Alembic migrations.
The API runs in Docker for consistency across environments.

----------------------------------------------------------------

PROJECT STRUCTURE

job-tracker-api/
- app/
  - auth.py            JWT creation and verification
  - database.py        Database engine and session
  - deps.py            Dependency injection
  - models.py          SQLAlchemy models
  - schemas.py         Pydantic schemas
  - routes/
    - auth.py          Register and login endpoints
    - applications.py  Job application CRUD
  - main.py            Application entrypoint
- alembic/             Database migrations
- tests/               Pytest integration tests
- Dockerfile
- docker-compose.yml
- requirements.txt
- README.md

----------------------------------------------------------------

RUN LOCALLY (DOCKER)

1. Start the services

docker compose up -d --build

2. Run database migrations

docker exec -it job-tracker-api alembic upgrade head

3. Open Swagger UI

http://127.0.0.1:8000/docs

----------------------------------------------------------------

AUTHENTICATION FLOW

1. Register a user
   POST /auth/register

2. Login
   POST /auth/login

3. Authorize in Swagger UI
   Use the "Authorize" button (OAuth2 password flow)

4. Access protected endpoints
   GET /me
   CRUD operations on /applications

----------------------------------------------------------------

JOB APPLICATION CRUD

Create application
POST /applications

List applications
GET /applications
Optional query params:
- status
- include_inactive

Update application
PATCH /applications/{id}

Soft delete application
DELETE /applications/{id}

All job applications are scoped to the authenticated user.

----------------------------------------------------------------

TESTING

The test suite covers:
- Health endpoint
- User registration and login
- JWT-protected endpoints
- Full job application CRUD lifecycle

Run tests locally:

pytest -q

----------------------------------------------------------------


