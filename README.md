# yapp — Personal Finance Toolkit

A personal finance web app (Loan EMI, SIP planner, Budget analyzer) used as a hands-on playground for **CI/CD, Docker, Kubernetes, Cloud, MLOps and Agentic AI**. The project grows phase by phase — see [notes/PROGRESS.md](notes/PROGRESS.md).

## Architecture

```mermaid
flowchart LR
    Browser -->|/ui| G[Gradio UI]
    Client[API client] -->|/api/v1/*| R[FastAPI routes]
    Probe[Health probe] -->|/health| R
    G --> C[core business logic]
    R --> C
```

One uvicorn process serves the REST API (FastAPI) and the web UI (Gradio, mounted at `/ui`).

| Path | Purpose |
|------|---------|
| `/ui` | Web UI |
| `/docs` | Interactive API docs (Swagger) |
| `/health` | Liveness check |
| `POST /api/v1/emi` | Loan EMI |
| `POST /api/v1/sip` | SIP projection |
| `POST /api/v1/budget/analyze` | Budget breakdown |

## Configuration

| Env var | Default | Allowed |
|---------|---------|---------|
| `APP_ENV` | `dev` | `dev`, `staging`, `prod` |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `CURRENCY` | `INR` | any label |

## Local development (Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt     # runtime + test tools
uvicorn app.main:app --reload --port 8500
```
Open http://127.0.0.1:8500/ui — try the Budget tab with [samples/expenses_sample.csv](samples/expenses_sample.csv).

## Tests

```bash
pytest                                  # everything (unit + integration)
pytest tests/unit                       # fast: pure business logic, no FastAPI/Gradio
pytest tests/integration                # HTTP API via FastAPI TestClient (in-process, no port)
pytest --cov=app --cov-branch --cov-report=term-missing   # coverage
```

## Roadmap
Docker → CI/CD (GitHub Actions + Docker Hub) → Compose & DB → Kubernetes → Cloud & Terraform → Observability → MLOps → Agentic AI.
