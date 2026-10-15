# Progress Tracker

Legend: ✅ done · 🔄 in progress · ⬜ not started

## Phase 1 — Python, Streamlit, Testing, Docker, GitHub Actions

| # | Lesson | Status | Date | Notes |
|---|--------|--------|------|-------|
| 0 | Setup: git init, local identity, remote, .gitignore, notes | ✅ | 2026-10-15 | [git concepts](concepts/git.md) |
| 1 | App: FastAPI + Gradio, modules, env config, logging, errors, /health | ✅ | 2026-10-15 | [architecture](concepts/app-architecture.md) |
| 2 | Testing: pytest unit vs integration | ⬜ | | |
| 3 | Docker: multi-stage, .dockerignore, HEALTHCHECK, non-root | ⬜ | | |
| 4 | GitHub Actions basics + `ci.yml` (push/PR) | ⬜ | | |
| 5 | Secrets vs Variables, Docker Hub push, tagging/SemVer | ⬜ | | |
| 6 | `deploy.yml` — manual `workflow_dispatch` + environments | ⬜ | | |
| 7 | `scheduled.yml` — cron checks | ⬜ | | |
| 8 | Job summaries (`$GITHUB_STEP_SUMMARY`) + job outputs | ⬜ | | |

## Phase 2 — Docker Compose, multiple services, databases
⬜ Branching strategy: introduce `dev` branch + PR flow

## Phase 3 — Kubernetes (Deployments, Services, Ingress, ConfigMaps, Secrets)
## Phase 4 — Cloud (AWS/Azure) + Terraform (IaC)
## Phase 5 — Observability (Prometheus, Grafana, OpenTelemetry)
## Phase 6 — MLOps (model deployment, model monitoring)
## Phase 7 — Agentic AI (LLM apps, RAG, tool calling, multi-agent)

## Extra topics learned outside the plan
| Topic | Date | Notes |
|-------|------|-------|
| Private IP, NAT, outbound vs inbound, self-hosted runners behind firewalls | 2026-10-15 | [networking](concepts/networking.md) |
| TLS inspection (Zscaler): cert trust error vs policy block | 2026-10-15 | [troubleshooting](troubleshooting.md) |
| Containers vs VMs, nested virtualization | 2026-10-15 | [troubleshooting](troubleshooting.md) |
