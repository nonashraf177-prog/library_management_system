# Library Management System

A RESTful API for managing a library built with FastAPI, SQLAlchemy, and SQLite.

## Features
- JWT Authentication (register/login)
- Role-based access control (admin / member)
- Books CRUD with search and pagination
- Borrow/return books with limit enforcement (max 3 per user)
- Request logging middleware
- Monitoring health/metrics endpoint

## Setup
```bash
pip install -r requirements.txt
python run.py
```

## API Docs
Visit http://localhost:8000/docs after running.

## Project Structure
```
app/
  core/       - config, database, security, JWT, logging
  models/     - SQLAlchemy models
  schemas/    - Pydantic schemas
  routes/     - API endpoints
  services/   - Business logic
  dependencies/ - Auth & role guards
  middleware/ - Request logging
  utils/      - Helpers and constants
  monitoring/ - Health & metrics
tests/        - Pytest test suite
docker/       - Dockerfile & docker-compose
```
