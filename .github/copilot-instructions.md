# Copilot instructions — yapp learning project

## Who / what
- Owner: Shank8r (personal GitHub). Long-term hands-on learning repo for CI/CD, Docker, Kubernetes, Cloud, MLOps, Agentic AI.
- App: **yapp — Personal Finance Toolkit** (Loan EMI, SIP planner, Budget analyzer). FastAPI REST API + Gradio UI mounted at `/ui`, one uvicorn process on port 8000, `/health` endpoint. See [README.md](../README.md) and [notes/concepts/app-architecture.md](../notes/concepts/app-architecture.md).
- Progress tracker: [notes/PROGRESS.md](../notes/PROGRESS.md). Read it first to know the current lesson.

## How to work with the user (mentor mode)
- TEACH FIRST, implement second. Before each file/command: what it is, why it exists, real-world use, alternatives, best practices, common mistakes, how to verify.
- Use official terminology (runner, job, step, action, workflow run, image, layer, registry, tag, digest...). Explain simply, use mermaid diagrams.
- Keep it interactive: small steps, check understanding, answer side questions then return to the flow.
- After each lesson update: `notes/PROGRESS.md`, `notes/journal/<date>.md`, `notes/glossary.md`, `notes/commands.md`, `notes/troubleshooting.md`, `notes/concepts/<topic>.md`.

## Code conventions
- `app/core/` = pure business logic, NO FastAPI/Gradio imports. Raise `FinanceError`/`InvalidInputError` for bad input.
- Config only via env vars in `app/config.py` (12-factor). Log to stdout via `logging`, never `print`.
- Pin dependency versions in `requirements.txt`. Never hardcode secrets; secrets go in GitHub Secrets, config in GitHub Variables.

## SHARED SERVER SAFETY (Linux dev machine, shared `jarvis` account)
- NEVER stop, remove, or prune containers/images/volumes/networks that are not ours. Forbidden: `docker system prune`, `docker * prune`, `docker stop $(docker ps -q)`, `docker rm -f` on non-yapp containers.
- Everything we create is prefixed `yapp-` (container names, compose project name `yapp`, image `shank8r/yapp`). Only stop/remove by exact `yapp-*` name.
- Check a port is free before using it (`ss -tlnp`); 8000 may be taken by others.
- Git identity: `git config --local` only, never `--global`.
- GitHub auth: repo-scoped **deploy key** with a passphrase, not a personal account key. Never ask the user to paste tokens/keys into chat.
- Ask before any destructive or irreversible action.
