# Glossary — use the official words

## Git
| Term | Meaning |
|------|---------|
| Repository (repo) | Project folder + its full history (the `.git/` directory) |
| Commit | A snapshot of tracked files + metadata (author, message, parent) |
| Branch | A movable pointer to a commit (`main`, `dev`) |
| Remote | A named URL of another copy of the repo (`origin` → GitHub) |
| Working tree / Staging area (index) | Your files on disk / what goes into the next commit (`git add`) |
| Author identity | `user.name` + `user.email` in commit metadata — **not verified** |
| Authentication | Proof you may push (GCM login, PAT, SSH key) — **verified** |
| Config levels | `system` → `global` → `local`; most specific wins |
| GCM | Git Credential Manager — stores credentials in Windows Credential Manager |
| Rebase | Replay commits on a new base, creating **new** commits (new hashes) |
| `rebase --root --exec` | Replay every commit from the first one, running a command after each |
| Force push | Overwrite remote history; prefer `--force-with-lease` (refuses if remote moved) |
| `core.sshCommand` | Per-repo override of the `ssh` command Git uses (e.g. which key) |

## SSH
| Term | Meaning |
|------|---------|
| Key pair | Private key (stays on your machine) + public key (given to the server) |
| ed25519 | Modern, short, fast key type — default choice today |
| Passphrase | Password that encrypts the private key file on disk |
| ssh-agent | Background process that holds decrypted keys so you type the passphrase once |
| Deploy key | SSH public key attached to **one repository**, read-only or read/write; not tied to a user |
| Host key | Server's own key pair; proves the server is the real one |
| Fingerprint | Short hash of a key (`SHA256:...`) for human comparison |
| `known_hosts` | `~/.ssh/known_hosts` — host keys you've already trusted |
| MITM | Man-in-the-middle: attacker pretending to be the server |
| `IdentitiesOnly=yes` | Offer only the key given with `-i`, not every key in the agent/`~/.ssh` |
| scp | Secure copy — copy files over SSH |

## Web / API
| Term | Meaning |
|------|---------|
| ASGI | Contract between async Python web apps and servers |
| uvicorn | ASGI **server** — listens on a port, speaks HTTP |
| FastAPI | Web **framework** — routing, validation, auto docs |
| Endpoint / route | URL path + HTTP method handled by a function (`POST /api/v1/emi`) |
| OpenAPI | Machine-readable API description; powers `/docs` |
| Pydantic | Data validation via type hints |
| Status codes | 200 OK · 400 bad input (business rule) · 422 schema invalid · 500 server bug |
| Liveness / readiness | "Process alive?" / "Ready to take traffic?" |
| Virtual environment (venv) | Isolated Python packages per project |
| Pinning | Exact versions in requirements (`==`) for reproducible builds |
| Telemetry | Usage data a library sends to its vendor |

## Networking
| Term | Meaning |
|------|---------|
| Private IP | Address valid only inside a network (`10.x`, `172.16-31.x`, `192.168.x`) |
| NAT | Router rewrites private → public IP for outbound traffic |
| Outbound / egress | Connection started by your machine |
| Inbound / ingress | Connection started by someone else to your machine |
| Stateful firewall | Allows replies to connections you started, blocks unsolicited inbound |
| Port forwarding / SSH tunnel | Carry traffic for a remote port through an existing SSH connection |
| Headless | Machine with no GUI/desktop, terminal-only (typical server) |
| TLS inspection | Proxy decrypts/re-encrypts HTTPS with its own CA (e.g. Zscaler) |
| Bind address | Which local interface a server listens on |
| Loopback (`127.0.0.1`, `::1`) | Same-machine-only interface |
| `0.0.0.0` / `::` | "All interfaces" — reachable from the network |
| Listening socket | A process waiting for connections on IP:port (`ss -tlnp`) |

## GitHub Actions
| Term | Meaning |
|------|---------|
| Workflow | YAML file in `.github/workflows/` that automates something |
| Event / trigger | What starts a workflow: `push`, `pull_request`, `workflow_dispatch`, `schedule` |
| Workflow run | One execution of a workflow |
| Job | Group of steps executed on one runner; jobs run in parallel unless `needs:` |
| Step | One `run:` command or one `uses:` action inside a job |
| Action | Reusable packaged step, e.g. `actions/checkout@v4` |
| Runner | Machine that executes a job. GitHub-hosted (fresh VM, discarded) or self-hosted |
| GitHub-hosted runner | Temporary VM in GitHub's cloud; reaches the internet (Docker Hub) but not our private network |
| Self-hosted runner | GitHub's agent installed on our machine; polls GitHub **outbound** for jobs — needed to deploy inside a private network |
| Fork / pull request | A stranger's copy of the repo / a request to merge their changes; PR workflows run **their** workflow file |
| Secret | Encrypted value, masked in logs: `${{ secrets.X }}` |
| Variable | Plain-text config value: `${{ vars.X }}` |
| Environment | Named deploy target (dev/prod) with own secrets + protection rules (required reviewers) |
| Artifact | Files persisted from a run for download |
| Job summary | Markdown written to `$GITHUB_STEP_SUMMARY`, shown on the run page |
| `needs:` | Job dependency: order + skip if the needed job failed |
| Step / job output | Value a step exposes (`steps.<id>.outputs.x`) / a job exposes to later jobs (`needs.<job>.outputs.x`) |
| `GITHUB_TOKEN` / `permissions:` | Auto token per run / limits what it may do (least privilege) |
| `concurrency` | Limit to one run per group; optionally cancel older runs |
| `paths-ignore` | Don't trigger when only these paths changed |
| Smoke test | Quick "does it start and answer?" check on the built artifact |
| Reusable workflow | Workflow with `on: workflow_call`; called via `jobs.<id>.uses:`, takes `inputs`/`secrets`, returns workflow `outputs` (like a function) |
| `workflow_dispatch` | Manual trigger: "Run workflow" button with `inputs` form fields |
| Environment protection rules | Required reviewers, branch restrictions, wait timer — a job with `environment:` pauses until satisfied |
| Deployment (GitHub) | Record created when a job with `environment:` runs; shown under repo → Deployments |
| Script injection | `${{ }}` is pasted into the script before bash runs → untrusted text can become commands; pass via `env:` |
| SemVer | `MAJOR.MINOR.PATCH`: breaking / feature / fix |
| Immutable release tag | A version tag is never re-pushed; a new build gets a new version |
| Build once, promote | Re-tag the already-tested image for release instead of rebuilding (same digest test → prod) |
| Runner image label | `ubuntu-latest` (moving) vs `ubuntu-24.04` (pinned) |
| Linter / formatter | Finds code problems without running it / rewrites layout consistently (ruff does both) |
| Annotation | Error/warning shown on a file line in GitHub UI (`::error::`, `--output-format=github`) |
| Personal access token (Docker Hub) | Scoped, revocable password substitute for automation; works with 2FA |

## Testing
| Term | Meaning |
|------|---------|
| Unit test | Tests one function in isolation (our `app/core/*`) — fast, precise |
| Integration test | Tests parts working together (HTTP → FastAPI → core → JSON) |
| E2E test | Drives the real UI/system like a user (browser) — slow, brittle |
| Test pyramid | Many unit, fewer integration, very few E2E |
| Test discovery | pytest finds `test_*.py` files and `test_*` functions |
| Collection error | Test file couldn't be imported — nothing ran (exit code 2) |
| Failure vs error | `F` = assertion/exception in the test · `E` = setup/fixture problem |
| Node ID | `file::function[params]` — address of one test case |
| Fixture | Reusable setup injected by parameter name; `yield` = setup/teardown |
| Fixture scope | `function` (default, fresh each test) · `module` · `session` (once per run) |
| `conftest.py` | Auto-loaded file sharing fixtures with tests in its folder |
| Parametrize | One test function → many cases (`@pytest.mark.parametrize`) |
| `monkeypatch` | Built-in fixture to temporarily change env vars/attributes; auto-restored |
| `pytest.approx` | Float comparison with tolerance |
| Oracle | Independent source of the expected answer (textbook value, closed-form formula) |
| Boundary value | Test exactly at the limit (0, 100, 50) — catches off-by-one |
| Coverage (line / branch) | Which lines / which `if` sides ran during tests — not proof of correctness |
| `TestClient` | Calls the ASGI app in-process over httpx — no server, no port |

## Docker
| Term | Meaning |
|------|---------|
| Image | Read-only blueprint (filesystem + metadata) |
| Container | A running instance of an image |
| Layer | Cached filesystem change produced by one Dockerfile instruction |
| Registry | Server that stores images (Docker Hub, GHCR, ECR, ACR) |
| Repository | Named collection of image versions in a registry (`shankar180/yapp`) |
| Port publishing | `-p HOST:CONTAINER` — map a host port to a container port (`-p 8500:8000`) |
| Tag | Human-friendly, **mutable** label (`:1.0.0`, `:latest`) — a sticky note that can move |
| Digest | Immutable content hash (`sha256:...`) — the exact image, its fingerprint |
| Dockerfile | Text recipe of build steps (`FROM`, `RUN`, `COPY`, `USER`, `CMD`) |
| Build context | Folder sent to the builder (`.`); `COPY` can only see files in it |
| `.dockerignore` | Excludes files from the build context (`.git`, `.venv`, `.env`, tests) |
| Base image | Starting filesystem (`python:3.12-slim-trixie`) |
| Multi-stage build | Several `FROM`s; build in one stage, copy only results into the final one |
| Layer cache | Unchanged steps are reused; a changed step rebuilds everything after it |
| BuildKit | Docker's modern build engine (parallel stages, cache, attestations) |
| `EXPOSE` | Documents the container port — does **not** publish it |
| `HEALTHCHECK` | Command Docker runs periodically → `(healthy)` / `(unhealthy)` |
| Exec form vs shell form | `CMD ["uvicorn", ...]` (PID 1, gets signals) vs `CMD uvicorn ...` (wrapped in `/bin/sh`) |
| PID 1 | First process in the container; must handle `SIGTERM` for graceful stop |
| Detached (`-d`) | Container runs in the background |
| Bridge network (`docker0`) | Containers' private network; host reaches them via gateway `172.17.0.1` |
| Image index | One tag covering multiple CPU architectures (amd64, arm64) |
| Content size vs disk usage | Compressed (transferred to/from registry) vs unpacked on disk |
| Transitive dependency | A dependency of your dependency (Gradio → pandas, numpy) |
