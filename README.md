# Healthcare Claims & Member Management API

A production-style backend API for managing healthcare members and insurance claims, with JWT authentication, role-based authorization, PostgreSQL persistence, Docker support, automated testing, and AI-assisted claim risk analysis.

## Features

- User registration and login
- JWT authentication
- Password hashing with bcrypt
- Role-based authorization
- Member profile management
- Healthcare claim management
- Claim pagination and filtering
- Claim approval/rejection workflow
- AI-assisted claim risk analysis
- Ollama + Qwen 2.5 integration
- AI analysis persistence in PostgreSQL
- AI output validation with Pydantic
- AI service error handling
- Request logging middleware
- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- Docker and Docker Compose
- Automated pytest test suite
- Swagger/OpenAPI documentation

## Architecture

```text
Client
   |
   v
FastAPI Routers
   |
   v
Authentication / Authorization
   |
   v
Service Layer
   |
   v
SQLAlchemy ORM
   |
   v
PostgreSQL

#AI Architecture

Healthcare Claim
       |
       v
AI Service
       |
       v
Ollama
       |
       v
Qwen 2.5
       |
       v
Risk Analysis
       |
       v
Pydantic Validation
       |
       v
PostgreSQL

#AI Architecture
Healthcare Claim
       |
       v
AI Service
       |
       v
Ollama
       |
       v
Qwen 2.5
       |
       v
Risk Analysis
       |
       v
Pydantic Validation
       |
       v
PostgreSQL

# Tech Stack
Python
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Pydantic
JWT
bcrypt
Ollama
Qwen 2.5
Docker
Docker Compose
pytest

Project Structure

app/
├── auth/
├── core/
├── exceptions/
├── middlewares/
├── models/
├── routers/
├── schemas/
├── services/
├── database.py
└── main.py

tests/
├── conftest.py
├── test_auth.py
├── test_members.py
├── test_claims.py
└── test_ai_claim.py