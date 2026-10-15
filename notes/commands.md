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

## GitHub CLI
```powershell
gh auth status                   # which account(s) is gh logged into
```
