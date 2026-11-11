# Topology & C4 diagrams

This page holds the architecture committee's **C4-style diagrams**
(botforge-infra#132): the system context, the containers, and the two
deployment options for the hosting decision (VPS — with the Kapsule
trial — vs bare metal + hypervisor). The vision behind them is
[vision.md](vision.md); the load assumptions are
[capacity.md](capacity.md).

Diagrams are Mermaid, like the rest of the docs. They describe
**target placement**, not implementation detail — the deploy mechanics
live in `botforge-infra` (GITOPS.md, ENVIRONMENTS.md).

## Level 1 — System context

```mermaid
flowchart TB
    PLAYER["Player<br/>(Discord user)"]
    DESIGNER["Game designer<br/>(GitHub web UI + admin surfaces)"]
    STREAMER["Streamer"]
    WEBUSER["Web / desktop user"]

    subgraph BOTFORGE["BotForge platform"]
        DISCORD["Discord surface<br/>(today)"]
        FLUXER["Fluxer surface<br/>(POC, infra#133)"]
        WEBAPP["Webapp + website front"]
        PYQT["PyQt app (deferred)"]
        TWITCH["Twitch / Matrix / streamer bots (deferred)"]
    end

    GH["GitHub<br/>(repos, rulesets, runners)"]
    SCW["Scaleway<br/>(VPS hosting today; Kapsule option)"]

    PLAYER --> DISCORD
    PLAYER --> FLUXER
    STREAMER --> TWITCH
    WEBUSER --> WEBAPP
    WEBUSER --> PYQT
    DESIGNER --> GH
    GH --> BOTFORGE
    BOTFORGE --> SCW
```

## Level 2 — Containers

```mermaid
flowchart TD
    subgraph CORE["botforge-services containers (per env)"]
        BOTCORE["bot core process"]
        BOTPROVIDER["bot provider process"]
        BOTSUPPORT["support processes (4 total per env)"]
        MONGO[("MongoDB<br/>durable data")]
        REDIS[("Redis<br/>hot state")]
    end

    subgraph HOSTING["hosting (single VPS today)"]
        COMPOSE["docker-compose per env<br/>prod / test / merlin / drasah"]
        BIND[("bind mounts<br/>/opt/botforge/data/&lt;env&gt;")]
        RUNNER["self-hosted runner"]
    end

    subgraph DEVSTACK["self-hosted dev/ops stack (deferred)"]
        FORGEJO["Forgejo + Woodpecker"]
        NEXTCLOUD["Nextcloud"]
        OPENBAO["OpenBao"]
        ELK["ELK"]
    end

    CORE --> MONGO
    CORE --> REDIS
    COMPOSE --> BIND
    RUNNER --> COMPOSE
    GH2["GitHub deploy chain<br/>(state branches)"] --> RUNNER
    DEVSTACK -.-> HOSTING
```

## Level 3 — Deployment option A: VPS (incl. Kapsule trial)

The current topology: one VPS, four compose environments, GitOps
reconciliation by a self-hosted runner. Kapsule (managed Kubernetes,
free trial) is an **evaluation option** for the K8s appetite — no
manifest exists today.

```mermaid
flowchart TD
    subgraph VPS["VPS (Scaleway, Ubuntu)"]
        subgraph PROD["env: prod"]
            P1["compose project<br/>4 bot processes + mongo + redis"]
        end
        subgraph TEST["env: test"]
            T1["compose project"]
        end
        subgraph PERSO["env: merlin / drasah"]
            M1["compose project"]
        end
        RUNNERA["runner (labelized)"]
        OPT["/opt/botforge/data/&lt;env&gt; bind mounts"]
    end
    GH3["GitHub deploy chain"] -->|"state branch push"| RUNNERA
    RUNNERA --> PROD & TEST & PERSO
    PROD & TEST & PERSO --> OPT

    KAPSULE["Option: Scaleway Kapsule<br/>(managed K8s, free trial)<br/>— trial target if K8s is tested"]
```

## Level 3 — Deployment option B: bare metal + hypervisor

The alternative under evaluation (ADR-022): one physical host, one
hypervisor, environments as isolated VMs — stronger failure domains at
the cost of hardware ownership and ops burden.

```mermaid
flowchart TD
    subgraph BM["bare metal host"]
        HV["hypervisor (e.g. Proxmox)"]
        subgraph VM1["VM: prod"]
            V1["compose project + data"]
        end
        subgraph VM2["VM: test"]
            V2["compose project + data"]
        end
        subgraph VM3["VM: merlin / drasah"]
            V3["compose project + data"]
        end
        subgraph VM4["VM: dev/ops stack (optional isolation)"]
            V4["Forgejo, Nextcloud, OpenBao, ELK"]
        end
    end
    GH4["GitHub deploy chain"] -->|"state branch push"| HV
    HV --> VM1 & VM2 & VM3 & VM4
```

## Reading the two options

| Dimension | Option A (VPS + compose) | Option B (bare metal + HV) |
| --- | --- | --- |
| Isolation | compose projects only | VM-level failure domains |
| Ops burden | hoster-managed hardware | we own hardware, power, replacements |
| Cost model | monthly VPS tier(s) | hardware CAPEX + power |
| K8s path | Kapsule trial available | self-managed cluster (heavy) |
| Backup/restore | bind mounts + hoster restore (#338 input) | full VM snapshots + local storage |

The decision path, criteria and current status live in
[ADR-022](../DECISIONS/022-hosting-evaluation-path.md).
