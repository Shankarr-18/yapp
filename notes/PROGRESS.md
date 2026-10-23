# Progress Tracker

Legend: ✅ done · 🔄 in progress · ⬜ not started

**Current lesson: revision day, then 7 — build once, promote.** Dev machine: Linux (`/home/jarvis/shankar/yapp`), host port 8500. Repo: `Shankarr-18/yapp` (public). Docker Hub: `shankar180` → image `shankar180/yapp`.

**Assignment status: all required parts done ✅** (Dockerfile, automatic/manual/cron workflows, Docker Hub push, Secrets + Variables, step/job/workflow outputs, job summaries, ruff lint).

## Revision plan (read in this order, then explain each in your own words)
1. [docker.md](concepts/docker.md) — image vs container, Dockerfile line by line, ports
2. [networking.md](concepts/networking.md) — runners, gated-complex analogy, why self-hosted for deploy
3. [ci.md](concepts/ci.md) — workflow anatomy, jobs on fresh machines, secrets vs variables, tags vs digest
4. [release.md](concepts/release.md) — reusable workflow = function, SemVer, environments, script injection
5. [security.md](concepts/security.md) — cron, CVEs, Trivy, risk acceptance, pinning actions by SHA
6. Open each workflow file in `.github/workflows/` and read it top to bottom with the notes beside it.
7. Check the 07:00 IST scheduled run of **Nightly check** on GitHub (first automatic cron run).

## Assignment (from roommate)
Dockerfile · 3 workflows: **automatic** (push/PR), **manual** (deployment), **cron** · build + push to Docker Hub · GitHub Secrets + Variables · workflow **outputs** · **job summary** on the run page · lint checks.

## Phase 1 — Python, Testing, Docker, GitHub Actions

| # | Lesson | Status | Date | Notes |
|---|--------|--------|------|-------|
| 0 | Setup: git init, local identity, remote, .gitignore, notes | ✅ | 2026-10-15 | [git concepts](concepts/git.md) |
| 1 | App: FastAPI + Gradio, modules, env config, logging, errors, /health | ✅ | 2026-10-15 | [architecture](concepts/app-architecture.md) |
| 2 | Testing: pytest unit vs integration, fixtures, monkeypatch, coverage | ✅ | 2026-10-22 | [testing](concepts/testing.md) |
| 3 | Docker: multi-stage, .dockerignore, HEALTHCHECK, non-root, run on :8500 | ✅ | 2026-10-23 | [docker](concepts/docker.md) |
| 4 | `ci.yml` (automatic): ruff lint → pytest → build → push to Docker Hub on `main`; Secrets vs Variables; job outputs; job summary | ✅ | 2026-10-23 | [ci](concepts/ci.md) |
| 5 | Reusable `_build.yml` (workflow outputs) + manual `release.yml` (`workflow_dispatch`, SemVer, `production` Environment approval). First release `0.1.0` | ✅ | 2026-10-23 | [release](concepts/release.md) |
| 6 | `scheduled.yml` (cron 07:00 IST + manual): pull `:latest`, `/health`, Trivy scan, summary; pillow CVEs accepted in `.trivyignore` (expires 2026-11-23) | ✅ | 2026-10-23 | [security](concepts/security.md) |
| 7 | Upgrade: build once, promote (release re-tags the CI-tested image instead of rebuilding) | ⬜ | | |
| 8 | Bonus: self-hosted runner on this Linux server, deploy job → `yapp-app` on :8500 (public repo safeguards: fork-PR approval ✅, runner only for manual job, Environment reviewer ✅; no sudo — user-level systemd) | ⬜ | | |

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
| Moved repo to Linux (scp), first push with a repo-scoped deploy key, SSH host key verification, `core.sshCommand` | 2026-10-15 | [git concepts](concepts/git.md) |
| Rewriting unpushed commits: `git rebase --root --exec` (author rename to Shankarr-18) | 2026-10-15 | [git concepts](concepts/git.md) |
| Reading `docker ps` ports, bind address `0.0.0.0` vs `127.0.0.1`, picking port 8500 | 2026-10-15 | [networking](concepts/networking.md) |
| Big picture: runners (GitHub-hosted vs self-hosted), why private IP needs a self-hosted runner for deploy, fork-PR risk on public repos | 2026-10-23 | [networking](concepts/networking.md) |
