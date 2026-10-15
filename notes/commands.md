# Commands Reference

## Git — setup
```powershell
git init -b main                                   # new repo, default branch "main"
git config --local user.name  "Shank8r"            # identity for THIS repo only
git config --local user.email "you@example.com"
git config --list --show-origin                    # see every setting + which file it came from
git remote add origin https://<user>@github.com/<user>/<repo>.git   # <user>@ makes GCM keep a per-account credential
git remote -v                                      # list remotes
```

## Git — daily
```powershell
git status                       # what changed?
git add <file>  /  git add .     # stage
git commit -m "message"          # snapshot
git log --oneline --graph        # history
git push -u origin main          # first push: -u sets upstream so later just `git push`
```

## Python / app
```powershell
python -m venv .venv                      # create isolated environment
.\.venv\Scripts\Activate.ps1               # activate it (prompt shows (.venv))
pip install -r requirements.txt           # install pinned deps
pip freeze                                # show every installed package + version
uvicorn app.main:app --reload --port 8000 # run app; --reload = restart on code change (dev only)
```

## Calling the API from PowerShell
```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/emi -Method Post -ContentType "application/json" `
  -Body '{"principal":500000,"annual_rate_pct":9,"years":5}'
```

## GitHub CLI
```powershell
gh auth status                   # which account(s) is gh logged into
```
