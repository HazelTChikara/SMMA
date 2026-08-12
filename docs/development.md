# Development guide

## Prerequisites

- Node.js 20+
- Python 3.13+
- Docker Desktop or Docker Engine

## Local setup

1. Start PostgreSQL and Redis:
   ```bash
   docker compose up -d postgres redis
   ```
2. Create a Python virtual environment and install API dependencies:
   ```bash
   cd apps/api
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Install frontend dependencies from the repository root:
   ```bash
   corepack enable pnpm
   pnpm install
   ```
4. Run the API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. Run the web app:
   ```bash
   pnpm --filter @smma/web dev
   ```

## Verification commands

- Backend tests: `pytest apps/api/tests`
- Frontend tests: `pnpm --filter @smma/web test`
- API health check: `curl http://localhost:8000/health`
