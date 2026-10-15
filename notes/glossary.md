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
| Secret | Encrypted value, masked in logs: `${{ secrets.X }}` |
| Variable | Plain-text config value: `${{ vars.X }}` |
| Environment | Named deploy target (dev/prod) with own secrets + protection rules (required reviewers) |
| Artifact | Files persisted from a run for download |
| Job summary | Markdown written to `$GITHUB_STEP_SUMMARY`, shown on the run page |

## Docker
| Term | Meaning |
|------|---------|
| Image | Read-only blueprint (filesystem + metadata) |
| Container | A running instance of an image |
| Layer | Cached filesystem change produced by one Dockerfile instruction |
| Registry | Server that stores images (Docker Hub, GHCR, ECR, ACR) |
| Repository | Named collection of image versions in a registry (`shank8r/yapp`) |
| Tag | Human-friendly, **mutable** label (`:1.0.0`, `:latest`) |
| Digest | Immutable content hash (`sha256:...`) — the exact image |
