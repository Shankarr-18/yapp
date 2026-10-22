# Commands Reference

> Dev machine is now **Linux (bash)**. PowerShell blocks below are from the Windows days.

## Git — setup
```powershell
git init -b main                                   # new repo, default branch "main"
git config --local user.name  "Shankarr-18"        # identity for THIS repo only
git config --local user.email "shankarhm1874@gmail.com"
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

## SSH deploy key (Linux)
```bash
ssh-keygen -t ed25519 -f ~/.ssh/yapp_deploy_key -C "yapp deploy key"   # make key pair; set a passphrase
cat ~/.ssh/yapp_deploy_key.pub        # PUBLIC half -> repo Settings -> Deploy keys (tick Allow write access)
ssh -i ~/.ssh/yapp_deploy_key -o IdentitiesOnly=yes -T git@github.com  # test: "Hi Shankarr-18/yapp! ..."
git config --local core.sshCommand "ssh -i ~/.ssh/yapp_deploy_key -o IdentitiesOnly=yes"  # use this key for THIS repo
git remote set-url origin git@github.com:Shankarr-18/yapp.git          # switch remote HTTPS -> SSH
ssh-keygen -lf ~/.ssh/known_hosts     # list fingerprints of hosts you've trusted
ssh-keygen -R github.com              # forget a host key (only if GitHub officially rotated it)
eval "$(ssh-agent -s)" && ssh-add -t 1h ~/.ssh/yapp_deploy_key  # optional: cache passphrase for 1 hour
```

## Git — rewrite unpushed history
```bash
git rebase --root --exec "git commit --amend --no-edit --reset-author"  # re-stamp EVERY commit with current local identity
git log --format='%h %an <%ae> %s'    # verify author on each commit
```
Only before pushing. After a push this needs `git push --force-with-lease` and breaks other clones.

## Copy files between machines
```bash
scp -r ./yapp jarvis@<linux-host>:/home/jarvis/shankar/   # copy folder over SSH (-r = recursive)
scp -P 2222 file user@host:/path/                         # non-default SSH port (capital -P)
rsync -av --exclude .venv ./yapp user@host:/path/         # alternative: incremental + excludes
```

## Ports & containers (shared server — read-only checks)
```bash
ss -tlnp                         # who is LISTENing on which TCP port (-t tcp, -l listen, -n numeric, -p process)
ss -tlnp | grep ':8500'          # is our port free?
docker ps                        # running containers; read the PORTS column
docker ps --format 'table {{.Names}}\t{{.Ports}}'   # just names + ports
```

## Testing (pytest)
```bash
pip install -r requirements-dev.txt     # runtime + pytest, pytest-cov, httpx
pytest                                  # all tests (config in pyproject.toml)
pytest -v / -q                          # verbose (one line per test) / quiet (dots)
pytest tests/unit                       # only the fast tests
pytest "tests/unit/test_emi.py::test_known_textbook_value"   # one test by node ID
pytest -k "invalid and Tenure"          # filter by name expression
pytest --durations=5                    # slowest phases
time pytest -q                          # real wall-clock (pytest's "in Xs" may miss conftests loaded before the session starts)
pytest --cov=app --cov-branch --cov-report=term-missing     # coverage + missing lines
```

## Python / app (Linux)
```bash
python3 -m venv .venv                     # create isolated environment
source .venv/bin/activate                 # activate (prompt shows (.venv)); `deactivate` to leave
pip install -r requirements.txt
pip index versions <pkg>                  # latest versions on PyPI (to pin)
uvicorn app.main:app --reload --port 8500 # 127.0.0.1 by default = only this machine (VS Code forwards the port)
curl -s http://127.0.0.1:8500/health
```
