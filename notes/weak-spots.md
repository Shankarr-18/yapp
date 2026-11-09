# Weak spots — re-quiz these (cover the answer, say it out loud, then check)

Review: 2026-11-11 · 2026-11-16 · 2026-11-30. Add every new miss here.

| # | Question | Correct one-liner | Missed on |
|---|---|---|---|
| 1 | Image vs container — does a container need a port? | Container = the image **running**. Ports (`-p`) are optional, only to reach it from outside. | 2026-10-26, 2026-11-09 |
| 2 | Authentication vs authorization? | **AuthN** = prove who you are (passport, deploy key). **AuthZ** = what you may do (boarding pass, write to yapp only). Identity = an unverified claim. | 2026-11-09 |
| 3 | What does "tags are mutable" mean? | The **same** tag can be moved to a **different** image (`latest`/`main` move on every release/push). Digest never moves. | 2026-11-09 |
| 4 | How do we deploy to a private server GitHub can't reach? | **Self-hosted runner** on that server polls GitHub **outbound** for jobs — no inbound needed. | 2026-11-09 |
| 5 | Nightly scan finds 1 fixable CRITICAL — steps? | Detect → investigate (package, transitive?, fix?) → assess (affects our app?) → decide (upgrade/rebuild/release or accept) → document (specific CVE ID + reason + expiry, never "ignore the package") → verify green + revisit. | 2026-11-09 |
| 6 | Why is rebuilding at release time risky? | The released box ≠ the tested box (new build, new digest; deps/base may have changed). **Build once, promote**: release only re-tags the CI-tested `sha-` image. | 2026-11-09 |
| 7 | The 8 stages? | Recipe → Save → Taste → Box → Shelf → **Label (release)** → Serve → Inspect. | 2026-11-09 (missed Label) |
| 8 | CI vs Continuous Delivery vs Deployment? | CI = merge changes into main often, each auto-checked. Delivery = always releasable, **human** decides. Deployment = goes live **automatically**. | 2026-11-09 |
