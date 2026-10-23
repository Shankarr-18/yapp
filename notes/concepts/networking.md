# Networking — Private IPs, NAT, Outbound vs Inbound

## Core idea: who starts the connection?
| | Outbound | Inbound |
|---|---|---|
| Initiator | Your machine | Someone else |
| Examples | `git push`, `docker pull`, `pip install`, browsing | Webhook to your server, SSH into your server |
| From private IP | ✅ via NAT | ❌ not reachable from internet directly |

## Private IP & NAT
- Private ranges (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` — only meaningful inside a network.
- **NAT** rewrites private source IP → public IP on the way out and remembers the mapping.
- **Stateful firewall**: allows *replies* to connections you started; blocks unsolicited inbound.

```mermaid
flowchart LR
    L[Linux 10.0.0.5] -->|outbound| NAT[NAT / firewall] --> GH[GitHub]
    GH -.replies.-> NAT -.-> L
    I[Internet] -.x blocked inbound.-x NAT
```

## In our project
- Linux machine (private IP) → `git push` / `docker pull` → outbound → works.
- Windows VM browser → github.com → outbound → works.
- GitHub-hosted runners run in GitHub's cloud → never need to reach our machines.
- GitHub is the shared hub; the two machines never talk directly.

## When inbound matters
| Need | Solution |
|---|---|
| CI deploys to a private server | **Self-hosted runner** on that server — polls GitHub over outbound HTTPS, no inbound ports |
| Webhooks to a private app | Tunnels (ngrok, Cloudflare Tunnel) or public load balancer |
| See a remote app from laptop | **SSH port forwarding** (VS Code does it automatically) / `kubectl port-forward` later |

## Bind address: `127.0.0.1` vs `0.0.0.0`
| Bind | Reachable from | Use for |
|---|---|---|
| `127.0.0.1` (loopback) | Same machine only | Local dev on a shared server (uvicorn default) |
| `0.0.0.0` (all interfaces) | Anyone who can reach the machine (firewall permitting) | Servers meant to be reached; **inside containers** (Lesson 3) |

`0.0.0.0` is not an address you connect *to* — it means "listen on every interface".

## Reading `docker ps` PORTS
| PORTS shows | Meaning |
|---|---|
| `0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp` | Host port 8000 (all IPv4 + IPv6 interfaces) → container port 8000. **Host 8000 is taken.** |
| `127.0.0.1:8500->8000/tcp` | Host 8500, loopback only → container 8000 |
| `8000/tcp` (no arrow) | Container listens/exposes 8000 but it's **not published** to the host |

Format is `HOST_IP:HOST_PORT->CONTAINER_PORT/proto`. Only the **host** port must be unique per machine; many containers can use 8000 internally. That's why yapp keeps 8000 inside and uses `-p 8500:8000`.

## Runners and our network (the big picture)
Analogy: our server is a flat inside a **gated complex** (private IP `10.x` behind NAT/firewall). Going **out** is allowed; strangers **can't come in**.

| Step | Runs on | Needs to reach | Works? |
|---|---|---|---|
| lint, test, build, push to Docker Hub | GitHub-hosted runner (GitHub's cloud) | Docker Hub (internet) | ✅ cloud → cloud, our network not involved |
| deploy (run on our server) | must be **self-hosted** runner on our server | our server | ✅ only because the runner calls GitHub **outbound** and asks for work |
| deploy via GitHub-hosted runner SSHing in | GitHub's cloud | our server (inbound) | ❌ blocked by the gate |

**Public repo + self-hosted runner risk:** a stranger forks, edits a workflow (`runs-on: self-hosted`), opens a PR → PR workflows use **their** file → their code could run on our shared server. Locks: require approval for fork-PR workflows (main lock; read the diff before approving), only manual jobs target our runner, Environment approval. GitHub-hosted runs of fork PRs get no secrets and are throwaway — low risk.

## Container networking
```mermaid
flowchart LR
    CURL["curl on server"] -->|127.0.0.1:8500| MAP["Docker port mapping"] -->|from 172.17.0.1| APP["uvicorn :8000 in container"]
    HC["HEALTHCHECK inside"] -->|127.0.0.1:8000| APP
```
Containers sit on Docker's private bridge network (`docker0`, gateway `172.17.0.1`). Forwarded traffic arrives on the container's interface, not loopback → the app must bind `0.0.0.0` inside the container.

## Checks
```bash
curl -sI https://github.com | head -1
ssh -T git@github.com
docker pull hello-world
```

## Interview questions
1. How can a machine with a private IP reach the internet? (NAT)
2. How do self-hosted runners work behind a firewall? (outbound long-polling, no inbound ports)
3. What does "stateful firewall" mean?
4. How would you access a web app running on a private server from your laptop? (SSH tunnel / port-forward / bastion)
5. App works via `curl localhost` but not from another host — why? (bound to 127.0.0.1)
6. Two containers both listen on 8000 — conflict? (No, unless both publish the same **host** port)
