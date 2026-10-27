# The flow — one-page cheat sheet (be answerable)

## The 8 stages (never forget this line)
**Recipe → Save → Taste → Box → Shelf → Label → Serve → Inspect**

| # | Stage | Official name | Ours | One-line WHY |
|---|---|---|---|---|
| 1 | Recipe | Source code | FastAPI + Gradio, venv, pinned deps | Pipeline needs real cargo; pins = same versions everywhere |
| 2 | Save | Version control | git → GitHub, SSH deploy key | `git push` is the trigger; commit SHA traces every image back to code |
| 3 | Taste | Continuous Integration | ruff → pytest (unit, integration) | Same checks on every push; cheap/fast first (fail fast) |
| 4 | Box | Containerization (artifact) | Dockerfile → image, smoke test | Same box everywhere → no "works on my machine" |
| 5 | Shelf | Registry | Docker Hub `shankar180/yapp` | Runner is destroyed; servers need a permanent place to pull from |
| 6 | Label | Release (Continuous **Delivery**) | `release.yml`: SemVer + approval | A human decides what is official; versions never change |
| 7 | Serve | Deployment | `docker run -p 8500:8000` (Lesson 8: self-hosted runner) | Box becomes a running app |
| 8 | Inspect | Monitoring + security scanning | `scheduled.yml`: /health + Trivy | The world finds new CVEs daily; failure → email |

**The robot:** GitHub Actions. Workflow = instruction sheet · trigger = reason to start · job = task on one fresh machine · step = one command/action · runner = the machine.

## The 4 questions for anything
**WHAT** is it · **WHY** (what breaks without it) · **HOW** we did it · **WHAT ELSE** exists

## 4 triggers = 4 reasons to start
| Trigger | Reason | File |
|---|---|---|
| `push` / `pull_request` | code changed | `ci.yml` |
| `workflow_dispatch` | a person decided | `release.yml` (+ test button in `scheduled.yml`) |
| `schedule` | time passed (cron, UTC) | `scheduled.yml` |
| `workflow_call` | another workflow asked (function) | `_build.yml` |

## Must-remember sentences
1. Every job gets a **fresh empty machine** → checkout first; share data only via **outputs**.
2. **Identity** = claim (commit author) · **Authentication** = proof (deploy key) · **Authorization** = permission (write to yapp only).
3. **Deploy key** = least privilege on a shared server: one repo, revocable, passphrase.
4. **Lint** reads code; **tests** run code; **smoke test** runs the real box from outside.
5. Only a test **at the boundary** catches off-by-one. A test must fail once to be trusted. Coverage ≠ correctness.
6. **Image** = sealed box · **container** = box opened and running. Inside ports can repeat; **host ports must be unique**.
7. App listens on **0.0.0.0** inside the container (forwarded traffic arrives on the container's network card). **Healthy ≠ reachable.**
8. **Build time** (Dockerfile, cache) vs **run time** (`-e APP_ENV=prod`) → build once, configure anywhere (12-factor).
9. **Secret** = gives power if leaked (token) · **variable** = harmless config (username). Over-secret = `***` everywhere.
10. **Tag** = sticky note (moves) · **digest** = fingerprint (never changes) → deploy by digest.
11. GitHub runner → Docker Hub works (cloud ↔ cloud). Runner → our server fails (private IP, inbound blocked) → **self-hosted runner** polls **outbound**.
12. Release validate: SemVer · main only · == `__version__` · tag not existing → fail before asking a human.
13. Never put `${{ inputs.x }}` in `run:` → pass via `env:` (data, not code).
14. **Pin everything that moves:** `==` deps, base image, `ubuntu-24.04`, third-party actions by commit SHA.
15. **Triage:** detect → investigate → assess → decide → document → revisit. Accept **specific CVE IDs with expiry**, never a whole package. Always-red checks cause **alert fatigue**.

## Interview one-liners
| Question | Answer |
|---|---|
| CI vs CD? | CI = integrate + check every change. Delivery = releasable artifact ready; Deployment = automatically live |
| Container vs VM? | Container shares host kernel (MBs, seconds); VM has its own OS (GBs, minutes) |
| Why multi-stage? | Build in a "kitchen" stage, ship only the clean result |
| Why non-root? | A compromised app isn't root |
| Reusable workflow? | Workflow with `on: workflow_call`; inputs = parameters, outputs = return value |
| Environment? | Named target with protection rules (reviewers, branches) → approval gate + audit trail |
| Why cron in UTC late? | GitHub queues scheduled runs; not guaranteed on time |
| Tell me about a security issue | pillow story: nightly scan red → transitive via gradio → fix blocked by gradio<13 → no image processing → accepted per-CVE with 30-day expiry → new CVE 2 days later caught because we accepted IDs, not the package |

## Same flow in other tools
GitHub Actions workflow/runner/job/secret/environment ≈ GitLab CI `.gitlab-ci.yml`/runner/job/masked variable/environment ≈ Jenkins `Jenkinsfile`/agent/stage/credentials/`input` ≈ Azure DevOps pipeline/agent/job/variable group/approvals.
