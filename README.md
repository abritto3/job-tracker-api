# Job Tracker API

A backend API for tracking job applications, built to reflect how a real production service is designed, tested, and deployed.

This project was built as part of my job search to demonstrate practical backend engineering skills beyond coursework: authentication, data modelling, API design, testing, CI, and deployment.

Live demo: (add Render URL here)

---

## Why this project exists

Most portfolio projects stop at “CRUD works locally”.

This project goes further and focuses on **how a backend service is actually built and run**:

- authenticated, multi-user system
- data isolation per user
- migrations instead of manual schema changes
- automated tests
- CI pipeline
- Dockerised deployment
- cloud hosting with a managed database

The goal is not novelty — it’s **realism**.

---

## What the API does

The API allows users to:

- register and log in securely
- manage their own job applications
- track application status (applied, interview, offer, rejected)
- update notes and links
- soft-delete applications without losing history

All data is scoped to the authenticated user.

---

## High-level architecture

Client (Swagger UI or frontend)
→ FastAPI application
→ PostgreSQL database

Authentication is handled using JWTs (OAuth2 password flow).  
Each request is authenticated and authorised before accessing data.

Database schema changes are handled via Alembic migrations.  
The service runs inside Docker for consistency across environments.

---

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest
- Docker & Docker Compose
- GitHub Actions
- Render (deployment)

---

## Project structure

job-tracker-api/
- app/
  - main.py            Application entry point
  - auth.py            JWT creation and validation
  - database.py        Database engine and session
  - deps.py            Dependency injection
  - models.py          SQLAlchemy models
  - schemas.py         Pydantic request/response models
  - routes/
    - auth.py          Registration and login
    - applications.py  Job application CRUD
- alembic/             Database migrations
- tests/               Integration tests
- Dockerfile
- docker-compose.yml
- requirements.txt
- README.md

---

## Authentication

Authentication uses JWTs with OAuth2 password flow.

Typical flow:

1. Register a user  
   POST /auth/register

2. Log in  
   POST /auth/login

3. Use the returned token to access protected endpoints

Swagger UI supports this flow directly via the “Authorize” button.

---

## Job application endpoints

- POST /applications  
  Create a new job application

- GET /applications  
  List applications for the current user  
  Supports filtering by status

- PATCH /applications/{id}  
  Update status or details

- DELETE /applications/{id}  
  Soft delete (keeps data but hides it by default)

---

## Running locally (Docker)

Start the service and database:

docker compose up -d --build

Run migrations:

docker exec -it job-tracker-api alembic upgrade head

Open Swagger UI:

http://127.0.0.1:8000/docs

---

## Testing

The test suite covers:

- health check
- user registration and login
- JWT-protected endpoints
- full job application CRUD lifecycle

Tests run against a real PostgreSQL database.

Run tests locally:

pytest -q

---

## Continuous Integration

GitHub Actions runs on every push and pull request to main.

The pipeline:
- starts PostgreSQL
- installs dependencies
- runs the full test suite

This ensures changes do not break core functionality.

---

## Deployment

The API is deployed on Render as a Docker web service.

- PostgreSQL is provided as a managed Render database
- migrations run automatically on startup
- secrets are configured via environment variables
- the same Docker image is used locally and in production

---

## Environment variables

DATABASE_URL  
PostgreSQL connection string

JWT_SECRET  
Secret used to sign JWTs

JWT_ALGORITHM  
HS256

ACCESS_TOKEN_EXPIRE_MINUTES  
Token lifetime

---

## What this project demonstrates

- Designing a secure, multi-user backend API
- Implementing authentication and authorisation
- Modelling relational data correctly
- Managing schema changes with migrations
- Writing meaningful integration tests
- Using Docker for reproducible environments
- Setting up CI pipelines
- Deploying and running a backend service in the cloud

This project reflects how backend systems are built in practice, not just how endpoints are written.

---

## License

MIT
