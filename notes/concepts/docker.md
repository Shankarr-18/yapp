# Docker \u2014 Dockerfile, image, container

## Why
Running the app by hand = install Python, venv, pip install exact versions, copy code, start uvicorn \u2014 on every machine, and something always differs ("works on my machine"). Docker does those steps **once** into a sealed **image**; the same image (same digest) is tested, pushed and deployed everywhere.

| Word | Analogy | yapp |
|---|---|---|
| Dockerfile | Recipe | [Dockerfile](../../Dockerfile) |
| Image | Cooked meal, sealed box (immutable) | `yapp:dev` locally, `shankar180/yapp:<tag>` on Docker Hub |
| Container | A plate served from the box (running process); many per image | `yapp-dev` (local test), `yapp-app` (deploy, Lesson 5) |

```mermaid
flowchart LR
    R[Dockerfile] -->|docker build| I[Image] -->|docker run| C[Container]
    I -->|docker push| H[(Docker Hub)] -->|docker pull| S[Server]
```

## Our Dockerfile in plain words
| Line | Meaning |
|---|---|
| `FROM python:3.12-slim-trixie AS builder` | Start from small Debian 13 + Python 3.12; stage named builder ("messy kitchen") |
| `RUN python -m venv /opt/venv` / `pip install -r requirements.txt` | Install deps into a venv |
| `FROM ... AS runtime` | Fresh clean stage ("lunchbox") |
| `COPY --from=builder /opt/venv /opt/venv` | Take only the finished venv |
| `COPY app/ ./app/` | Our code (root-owned \u2192 app can't modify itself) |
| `USER app` (uid 10001) | Not root |
| `EXPOSE 8000` | Documentation only |
| `HEALTHCHECK ... /health` | Docker marks the container healthy/unhealthy |
| `CMD ["uvicorn", ..., "--host", "0.0.0.0", "--port", "8000"]` | Exec form \u2192 PID 1 gets SIGTERM; 0.0.0.0 so port mapping works |

## Best practices applied
- `.dockerignore` (small context, no `.env`/`.git` leaks) \u00b7 deps layer before code layer (cache) \u00b7 slim base pinned to Python minor + OS \u00b7 multi-stage \u00b7 non-root \u00b7 healthcheck \u00b7 exec-form CMD \u00b7 stdout logging (`PYTHONUNBUFFERED=1`) \u00b7 **config at runtime** (`-e APP_ENV=prod`), not baked in.
- Later: pin base by digest + Dependabot/Renovate; OCI labels via CI; vulnerability scan (cron workflow).

## Base image choice
`python:3.12` full (~1 GB, compilers) \u00b7 **`-slim`** (glibc, wheels just work) \u2705 \u00b7 `-alpine` (musl \u2192 wheels often compile from source; avoid for pandas/numpy) \u00b7 distroless (no shell).

## What we measured (2026-10-23)
- 152 MB compressed (content size), 647 MB on disk. Venv layer 361 MB, our code 74 kB \u2192 code changes re-push only a tiny layer.
- 3 direct deps \u2192 ~50 installed packages (transitive).
- `docker ps`: `Up 12 seconds (healthy)`, `127.0.0.1:8500->8000/tcp`; `id` \u2192 `uid=10001(app)`; uvicorn = PID 1.

## Common mistakes
`COPY . .` without `.dockerignore` (ships `.env`, `.git`) \u00b7 copying code before installing deps (cache busted every build) \u00b7 app binds `127.0.0.1` in the container (port mapping fails) \u00b7 shell-form CMD (10 s kill on stop) \u00b7 running as root \u00b7 `:latest` base image (unreproducible) \u00b7 secrets in `ENV`/`ARG` (visible in `docker history`).

## Interview questions
1. Image vs container? Layer? Why does instruction order matter?
2. What does `EXPOSE` do vs `-p`?
3. Why multi-stage? Why non-root?
4. Why must the app listen on 0.0.0.0 inside a container?
5. Exec form vs shell form of `CMD` \u2014 what breaks?
6. Why avoid alpine for Python data stacks?
7. How would you keep secrets out of an image?
