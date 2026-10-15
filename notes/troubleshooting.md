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
- **Fix:** Put the username in the remote URL (`https://Shank8r@github.com/...`) so GCM stores a separate credential, or remove the stale entry in Windows Credential Manager → Windows Credentials → `git:https://github.com`.
