# Git — Identity, Authentication, Config

## What & why
Git is a distributed version control system: every clone has the full history. GitHub is a *hosting service* for Git repos plus collaboration (PRs, Actions, Issues).

## Identity vs Authentication
| | Identity | Authentication |
|---|---|---|
| What | `user.name`/`user.email` stamped in each commit | Proof you're allowed to push |
| Verified? | No — anyone can type any email | Yes |
| Affects | Commit attribution, contribution graph | Whether push succeeds |

- GitHub links a commit to your account if the commit email is a **verified email** on that account.
- Commit **signing** (GPG/SSH) is how you prove identity → "Verified" badge.

## Config levels
`system` (all users) → `global` (your OS user, `~/.gitconfig`) → `local` (this repo, `.git/config`). Most specific wins.
In this repo: global = work email, local = personal email → work repos unaffected.

## Authentication options
| Method | How | Notes |
|---|---|---|
| GCM (HTTPS) | Browser OAuth login, stored in OS credential store | Easiest on Windows; default with Git for Windows |
| PAT (HTTPS) | Token used as password | Use fine-grained, least privilege, expiry. Never paste/commit it |
| SSH key | Public key on GitHub, private key local | Common on Linux/Mac; supports multiple accounts via `~/.ssh/config` |

## Common beginner mistakes
- Committing with the wrong (work) email → commits not linked to your profile.
- Pasting tokens into chats, code, or `.env` files that get committed.
- Forgetting `.gitignore` before the first commit → `.venv/`, `.env` pushed.

## Interview questions
1. Difference between `git fetch` and `git pull`? (pull = fetch + merge/rebase)
2. Can someone commit as you? How to prevent? (yes; commit signing + branch protection requiring signed commits)
3. What's the difference between global and local config?
4. What does `git push -u` do? (sets the upstream tracking branch)
