# Python Frontend Showcase

A comprehensive comparison of Python frontend frameworks by building the same barbershop management SaaS application using 6 different Python frontend frameworks, all sharing a common FastAPI backend.

## Project Overview

This project implements a barbershop management SaaS with the following features:
- User authentication and multi-tenancy
- Customer, barber, and service management
- Appointment scheduling and calendar
- Financial dashboard and analytics
- Notifications and reporting capabilities

## Frontend Frameworks Compared

1. **Reflex** - Full-stack Python web application
2. **Solara** - Reactive dashboard application
3. **FastUI** - API-driven administrative interface
4. **Streamlit** - Rapid MVP prototype
5. **Flet** - Cross-platform desktop/mobile/web application
6. **Kivy** - Mobile-first offline-capable application

## Backend Architecture

- **Framework**: FastAPI
- **Design**: Clean Architecture with Domain-Driven Design
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Caching**: Redis
- **Background Tasks**: Celery
- **Validation**: Pydantic v2

## Getting Started

### Prerequisites
- Python 3.13+
- Docker and Docker Compose
- Git

### Installation
1. Clone the repository
2. Copy `.env.example` to `.env` and configure environment variables
3. Run `docker-compose up -d` to start PostgreSQL and Redis
4. Install dependencies with `uv pip install -e .`
5. Run database migrations with `alembic upgrade head`
6. Start the development server with `uvicorn app.main:app --reload`

### Development
Each frontend framework has its own directory under `frontend/`:
- `frontend/reflex/`
- `frontend/solara/`
- `frontend/fastui/`
- `frontend/streamlit/`
- `frontend/flet/`
- `frontend/kivy/`

Refer to each framework's directory for specific setup and development instructions.

## Testing
Run tests with:
```bash
uv run pytest
```

## License
MIT
