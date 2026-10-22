# Troubleshooting Log

Format: **Symptom → Cause → Fix → Lesson**

## App

### pytest: `ModuleNotFoundError: No module named 'app'` (collection error, 0 tests ran)
- **Cause:** `tests/unit/` has no `__init__.py`, so pytest puts `tests/unit/` (not the project root) on `sys.path`.
- **Fix:** `pythonpath = ["."]` under `[tool.pytest.ini_options]` in `pyproject.toml`. (`python -m pytest` also works but only if everyone remembers.)
- **Lesson:** never hack `sys.path` inside tests — fix it in config so IDE, CLI and CI behave the same.

### Tests pass alone but fail together (or depend on your shell)
- **Cause:** a test set `os.environ[...]` directly (leaks into later tests), or the code caches config (`@lru_cache get_settings`) so a changed env var is ignored; or a test asserts on a value from the developer's environment.
- **Fix:** `monkeypatch.setenv/delenv` (auto-restored); call the uncached `load_settings()` or `get_settings.cache_clear()`; assert allowed values, not "dev".

### Ubuntu: `error: externally-managed-environment` on `pip install`
- **Cause:** PEP 668 — system Python is managed by apt.
- **Fix:** `python3 -m venv .venv && source .venv/bin/activate`. Never `sudo pip`.

### Logs show `HTTP Request: ... huggingface.co ... 403 Forbidden` at startup
- **Cause:** Gradio sends usage telemetry by default; corporate network blocks it.
- **Fix:** `GRADIO_ANALYTICS_ENABLED=False` set in `app/__init__.py` before gradio is imported.
- **Lesson:** libraries can make outbound calls you didn't ask for — audit startup logs.

### `Activate.ps1 cannot be loaded because running scripts is disabled`
- **Cause:** PowerShell execution policy.
- **Fix:** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or skip activation and call `.\.venv\Scripts\python.exe -m ...` directly.

## Docker

### Docker Desktop: "Virtualization support not detected" (inside a VM)
- **Cause:** Docker Desktop on Windows/Mac runs a hidden Linux VM (WSL2/Hyper-V) because containers need a Linux kernel. Inside a VM that requires **nested virtualization**, which is disabled at the hypervisor (host) level.
- **Fix:** Host admin enables nested virtualization (Hyper-V: `Set-VMProcessor -ExposeVirtualizationExtensions $true`; VMware: "Expose hardware assisted virtualization"; Azure: supported VM size). Or use a Linux VM (Docker Engine runs natively), Codespaces, or rely on GitHub-hosted runners for builds.
- **Lesson:** Containers share the host kernel; VMs virtualize hardware. Admin *inside* a VM can't change host settings.
- Diagnose: `(Get-CimInstance Win32_ComputerSystem) | Select Manufacturer, Model` and `systeminfo | Select-String "Hyper-V|Virtualization|hypervisor"`.

## Git

### Push to personal GitHub blocked by Zscaler ("violates your organization's policy")
- **Cause:** Corporate laptop traffic goes through Zscaler (a cloud security proxy). Company policy allows GitHub for the work org but blocks personal accounts.
- **Fix:** Don't bypass it (hotspot, VPN, proxy tricks = policy violation). Push from a personal machine, or get an approved exception from IT.
- **Lesson:** Enterprise networks enforce egress policies. The same thing happens to CI runners and servers (firewalls, allow-lists), which is why self-hosted runners in corporate networks often need proxy config.

### TLS trust error vs policy block — don't confuse them
| | Certificate trust problem | Policy block |
|---|---|---|
| Symptom | `SSL: CERTIFICATE_VERIFY_FAILED` | "violates your organization's policy" |
| Cause | Client doesn't trust the proxy's re-signing CA (TLS inspection) | Proxy deliberately denies destination/action |
| Fix | Add corporate root CA to bundle: `REQUESTS_CA_BUNDLE`, `SSL_CERT_FILE`, `NODE_EXTRA_CA_CERTS`, `git config http.sslCAInfo` | Only the policy owner (IT/security) can change it |
- Diagnose: `git ls-remote <public-repo>` worked (exit 0) and `curl https://github.com` → 200, so TLS was fine; only personal-account sign-in was blocked.
- A CA bundle changes what **your client trusts**; it never changes what **the proxy allows**.

### Push rejected: "GH007: Your push would publish a private email address"
- **Cause:** GitHub setting *Block command line pushes that expose my email* is on.
- **Fix:** `git config --local user.email "<id>+<user>@users.noreply.github.com"` (find it in GitHub → Settings → Emails), then `git commit --amend --reset-author --no-edit`.

### Push fails with 403 / "Permission denied to <other-account>"
- **Cause:** Cached credentials for a different GitHub account (e.g. work account) are being used.
- **Fix:** Put the username in the remote URL (`https://Shankarr-18@github.com/...`) so GCM stores a separate credential, or remove the stale entry in Windows Credential Manager → Windows Credentials → `git:https://github.com`.

### SSH: "The authenticity of host 'github.com' can't be established ... Are you sure you want to continue connecting?"
- **Cause:** First SSH connection; GitHub's host key isn't in `~/.ssh/known_hosts` yet. (Non-interactive runs fail outright with `Host key verification failed.`)
- **Fix:** Compare the shown fingerprint with GitHub Docs → "GitHub's SSH key fingerprints" (ED25519: `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`), then type `yes`.
- **Lesson:** Never blindly type `yes`. If you later see `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`, stop — either GitHub rotated its key (check their blog/docs, then `ssh-keygen -R github.com`) or someone is intercepting.

### SSH: `Permission denied (publickey)`
- **Cause:** Git used a different key (or none). On a shared account, ssh may offer other people's keys.
- **Fix:** `git config --local core.sshCommand "ssh -i ~/.ssh/yapp_deploy_key -o IdentitiesOnly=yes"`; test with `ssh -i ~/.ssh/yapp_deploy_key -o IdentitiesOnly=yes -T git@github.com`. Check the public key is added under the repo's Deploy keys.

### Push: `ERROR: The key you are authenticating with has been marked as read only`
- **Cause:** Deploy key added without **Allow write access**.
- **Fix:** Repo Settings → Deploy keys → delete and re-add with write access ticked.

### Commits show the old author (Shank8r) after renaming the account
- **Cause:** Author is stamped into each commit when it's created; changing `user.name`/`user.email` only affects new commits.
- **Fix (unpushed only):** set the new local identity, then `git rebase --root --exec "git commit --amend --no-edit --reset-author"`. Verify with `git log --format='%an <%ae>'`.

## Ports / networking

### `[Errno 98] Address already in use` / port 8000 busy
- **Cause:** Another team's container publishes host port 8000 (`docker ps` PORTS shows `0.0.0.0:8000->8000/tcp`).
- **Fix:** Use **8500** for yapp (`--port 8500`, `-p 8500:8000`). Never stop someone else's container.
- Diagnose: `ss -tlnp | grep ':8000'`, `docker ps --format 'table {{.Names}}\t{{.Ports}}'`.

### App works with `curl` on the server but not from another machine
- **Cause:** uvicorn binds `127.0.0.1` by default = loopback only.
- **Fix:** For dev, keep `127.0.0.1` and use VS Code port forwarding / SSH tunnel. Use `--host 0.0.0.0` only when it must be reachable on the network (and inside containers — see Lesson 3).
