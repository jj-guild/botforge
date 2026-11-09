# Long-term vision

This page is the architecture committee's **long-term vision** for the
platform (botforge-infra#132): the target topology, where each surface
lands on it, and the build-vs-buy-vs-drop calls. The current-state
diagrams and the hosting options live in
[topology.md](topology.md); the load expectations live in
[capacity.md](capacity.md). The committee itself is described in
[committee.md](committee.md).

## Vision statement

BotForge is a **modular, multi-platform bot platform** whose surface
keeps expanding. The vision is a topology where:

1. **Every surface lands in a decided place** — the mapping below is
   the decision record; a new component cannot join the platform
   without a row in it.
2. **The chat provider is not the platform** — the core is
   platform-agnostic (ADR-0001); Discord is today's provider, and
   Fluxer (botforge-infra#133) is the live hedge under evaluation.
3. **Capacity is planned, not discovered** — peaks (tournaments,
   season launches, streams) are sized in [capacity.md](capacity.md)
   before they land.
4. **The self-hosted dev/ops stack is a product we operate** — each
   self-hosted component is sized, backed up and monitored like the
   platform itself, not as a hobby side-service.

## Surface map — build / buy / drop

The full owner list (botforge-infra#132), mapped by the committee
(kickoff minutes in [committee.md](committee.md)):

| Surface | Call | Vision |
| --- | --- | --- |
| Discord bot platform | **build** | the platform itself — core + mods |
| Webapp + website front | **build** | ADR-0015 API boundary; the webapp is the non-Discord surface |
| PyQt local app | **build, deferred** | desktop client on the same API boundary as the webapp; deep-dive before any work |
| Twitch bot | **build, deferred** | second `IPlatform` implementation (ADR-0001) |
| Matrix bot | **build, deferred** | third platform implementation; same contract |
| Streamer bot (streamer & bot flows) | **build, deferred** | sized after the Twitch deep-dive |
| Fluxer | **evaluate** | POC botforge-infra#133: port one surface, then decide porting target / second-class surface / no-go |
| MongoDB / Redis | **self-host** (today) | managed offer revisited at the hosting decision |
| Forgejo (+ Woodpecker) | **self-host** | dev stack anchor; Woodpecker placed with it |
| Nextcloud | **self-host, deferred** | ops burden sized first |
| ArgoCD | **self-host, conditional** | only if Kubernetes is chosen (Kapsule trial) |
| OpenBao | **self-host, deferred** | secrets story is a committee deep-dive |
| ELK (or equivalent) | **buy-vs-self-host, deferred** | sizing input of capacity.md; a lighter managed stack is allowed |
| VPN | **build** | access layer for the self-hosted stack |
| Ansible / IaC | **build** | standing rule: the second repetition of any manual op becomes IaC |
| Scaleway Kapsule | **evaluate** | free trial, a cheap way to test K8s — not the existing topology |
| Bare metal + hypervisor | **evaluate** | the hosting alternative — ADR-022 |

**Drop calls**: none at this stage. The committee's rule: a surface is
dropped only by an explicit ADR, never by silence.

## Build-vs-buy-vs-drop rules

- **Build** when the component *is* the product (platform, surfaces) or
  when no offer fits the data-isolation rules.
- **Buy/self-host managed** when the component is undifferentiated
  (storage, CI, monitoring) — prefer managed while the ops team is one
  person plus agents.
- **Drop** requires an ADR superseding the surface's row here.

## Open questions owned by this vision

1. **Hosting**: VPS (incl. Kapsule trial) vs bare metal + hypervisor —
   evaluation path in ADR-022, no fixed deadline
   (inputs: botforge-services#338, botforge-services#329,
   botforge-services#315, botforge-services#281).
2. **Discord vs Fluxer vs both** — POC botforge-infra#133.
3. **Secrets**: OpenBao vs the current state-branch secrets story.
4. **Where the self-hosted dev stack lives** — same hosting as prod, or
   isolated.
