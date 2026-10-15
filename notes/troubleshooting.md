# Troubleshooting Log

Format: **Symptom → Cause → Fix → Lesson**

## Git

### Push rejected: "GH007: Your push would publish a private email address"
- **Cause:** GitHub setting *Block command line pushes that expose my email* is on.
- **Fix:** `git config --local user.email "<id>+<user>@users.noreply.github.com"` (find it in GitHub → Settings → Emails), then `git commit --amend --reset-author --no-edit`.

### Push fails with 403 / "Permission denied to <other-account>"
- **Cause:** Cached credentials for a different GitHub account (e.g. work account) are being used.
- **Fix:** Put the username in the remote URL (`https://Shank8r@github.com/...`) so GCM stores a separate credential, or remove the stale entry in Windows Credential Manager → Windows Credentials → `git:https://github.com`.
