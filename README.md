# Order API (FastAPI) — CI: Unit + Integration + Reports

This is a minimal project that demonstrates:
- FastAPI API (Swagger UI at `/docs`)
- PostgreSQL persistence via SQLAlchemy (sync)
- Unit tests (pure logic, repo mocked)
- Integration tests (API + real Postgres)
- GitHub Actions CI running unit + integration and uploading reports (JUnit + Coverage)

## 1) Requirements
- Python 3.11+ (3.12 recommended)
- Docker (for local Postgres)

## 2) Run locally

### 2.1 Start Postgres
```bash
docker compose up -d
```

### 2.2 Create venv & install deps
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2.3 Run API
```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/testdb"
uvicorn src.app.main:app --reload
```

Open Swagger UI:
- http://localhost:8000/docs

## 3) Run tests

### Unit tests (+coverage + junit)
```bash
mkdir -p reports/unit
pytest -m "not integration" \
  --junit-xml=reports/unit/junit.xml \
  --cov=src --cov-report=xml:reports/unit/coverage.xml --cov-report=html:reports/unit/coverage_html
```

### Integration tests (needs Postgres)
```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/testdb"
mkdir -p reports/integration
pytest -m integration --junit-xml=reports/integration/junit.xml
```

## 4) API Endpoints
- GET `/health`
- POST `/users`
- GET `/users/{id}`
- POST `/orders`
- GET `/orders/{id}`
- POST `/orders/{id}/pay`
