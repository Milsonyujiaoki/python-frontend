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

Each framework implementation includes comprehensive documentation in the `docs/` folder:

1. **Reflex** - Full-stack Python web application
   - Reactive state management
   - Built-in database integration
   - Documentation: `docs/REFLEX_DEVELOPMENT_PATTERNS.md`

2. **Solara** - Reactive dashboard application
   - React-like components for Python
   - Memoization and caching
   - Documentation: `docs/SOLARA_DEVELOPMENT_PATTERNS.md`

3. **FastUI** - API-driven administrative interface
   - Schema-driven UI generation
   - Pydantic integration
   - Documentation: `docs/FASTUI_DEVELOPMENT_PATTERNS.md`

4. **Streamlit** - Rapid MVP prototype
   - Session state management
   - Data-centric widgets and visualizations
   - Documentation: `docs/STREAMLIT_DEVELOPMENT_PATTERNS.md`

5. **Flet** - Cross-platform desktop/mobile/web application
   - Flutter-based Python UI
   - Responsive layouts
   - Documentation: `docs/FLET_DEVELOPMENT_PATTERNS.md`

6. **Kivy** - Mobile-first offline-capable application
   - KV language for UI separation
   - Multi-touch support
   - Documentation: `docs/KIVY_DEVELOPMENT_PATTERNS.md`

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
- [mise](https://mxsh.dev/) (task runner) - optional but recommended

### Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and configure environment variables
3. Start the infrastructure services (PostgreSQL and Redis):
   ```bash
   docker-compose up -d
   ```
4. Install dependencies using mise (recommended) or manually:
   ```bash
   # Using mise (installs all dependencies)
   mise install

   # Or manually:
   # Backend
   pip install -r backend/requirements.txt
   # Each frontend (example for Solara)
   pip install -r frontend/solara/requirements.txt
   # Repeat for other frontends
   ```
5. Run database migrations:
   ```bash
   # Using mise
   mise run backend-migrate
   # Or manually
   alembic upgrade head
   ```

### Available Tasks (using mise)

The project uses [mise](https://mxsh.dev/) for task automation. Run `mise ls` to see all available tasks.

#### Common tasks:
- `mise install` - Install all dependencies (backend and frontends)
- `mise start` - Start all services (backend, frontends, and infrastructure)
- `mise test` - Run all tests
- `mise lint` - Lint all code
- `mise format` - Format all code

#### Backend tasks:
- `mise backend-install` - Install backend dependencies
- `mise backend-run` - Run the backend development server
- `mise backend-test` - Run backend tests
- `mise backend-lint` - Lint backend code
- `mise backend-format` - Format backend code
- `mise backend-migrate` - Run database migrations
- `mise backend-migrate-make` - Generate new migration script

#### Infrastructure tasks (Docker Compose):
- `mise db-up` - Start PostgreSQL and Redis containers
- `mie db-down` - Stop and remove containers
- `mise db-logs` - View logs for database and cache
- `mise db-restart` - Restart database and cache containers

#### Frontend tasks (replace `<framework>` with `reflex`, `solara`, `fastui`, `streamlit`, `flet`, or `kivy`):
- `mise frontend-<framework>-install` - Install frontend dependencies
- `mise frontend-<framework>-run` - Run the frontend development server
- `mise frontend-<framework>-test` - Run frontend tests
- `mise frontend-<framework>-lint` - Lint frontend code
- `mise frontend-<framework>-format` - Format frontend code

#### Example workflow:
```bash
# Start infrastructure
mise db-up

# Run migrations
mise backend-migrate

# Start backend
mise backend-run &

# Start a frontend (example: Solara)
mise frontend-solara-run &

# Run tests
mise test
```

### Development

Each frontend framework has its own directory under `frontend/`:
- `frontend/reflex/`
- `frontend/solara/`
- `frontend/fastui/`
- `frontend/streamlit/`
- `frontend/flet/`
- `frontend/kivy/`

Refer to each framework's directory for specific setup and development instructions.

The backend API is available at `http://localhost:8000` when running.

Frontends typically run on:
- Reflex: http://localhost:3000
- Solara: http://localhost:8080
- FastUI: http://localhost:8081
- Streamlit: http://localhost:8082
- Flet: http://localhost:5000 (or as configured)
- Kivy: Runs as a desktop/mobile application

## Testing

Run all tests with:
```bash
mise test
```

Or run tests for a specific component:
- Backend: `mise backend-test`
- Specific frontend: `mise frontend-<framework>-test`

## License

MIT