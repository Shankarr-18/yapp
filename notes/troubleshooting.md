# Troubleshooting Log

Format: **Symptom → Cause → Fix → Lesson**

## App

### Logs show `HTTP Request: ... huggingface.co ... 403 Forbidden` at startup
- **Cause:** Gradio sends usage telemetry by default; corporate network blocks it.
- **Fix:** `GRADIO_ANALYTICS_ENABLED=False` set in `app/__init__.py` before gradio is imported.
- **Lesson:** libraries can make outbound calls you didn't ask for — audit startup logs.

### `Activate.ps1 cannot be loaded because running scripts is disabled`
- **Cause:** PowerShell execution policy.
- **Fix:** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or skip activation and call `.\.venv\Scripts\python.exe -m ...` directly.

## Git

### Push rejected: "GH007: Your push would publish a private email address"
- **Cause:** GitHub setting *Block command line pushes that expose my email* is on.
- **Fix:** `git config --local user.email "<id>+<user>@users.noreply.github.com"` (find it in GitHub → Settings → Emails), then `git commit --amend --reset-author --no-edit`.

### Push fails with 403 / "Permission denied to <other-account>"
- **Cause:** Cached credentials for a different GitHub account (e.g. work account) are being used.
- **Fix:** Put the username in the remote URL (`https://Shank8r@github.com/...`) so GCM stores a separate credential, or remove the stale entry in Windows Credential Manager → Windows Credentials → `git:https://github.com`.
