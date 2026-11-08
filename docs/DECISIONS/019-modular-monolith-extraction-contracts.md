# ADR-0019: Modular monolith with extraction-ready contracts

**Status:** Accepted

**Accepted with:** game designer + developer (vibe-coding session decision)

**Date:** 2026-09-27

**Reference:** ADR-0012, botforge#109

## Context

The roadmap's end state includes many moving parts: a Discord bot, a
Twitch bot, a webapp, the AoE2 game with external data sources
(aoe2lobby, LibreMatch), and a growing set of mods. Early instinct
says "split into microservices now — the rework will be costly."

The costly rework, however, is not extracting a well-bounded module
into its own process (days of infra). The costly rework is
retrofitting boundaries into an entangled monolith: mods reading each
other's collections, ladder code importing a data provider, shared
DB schemas across domains. That is what ADR-0012 already prevents:

- narrow `typing.Protocol` seams everywhere (ADR-0011) — services
  know their dependencies by typed contract, never by implementation;
- a CI-enforced dependency matrix (import analysis) — a violation
  fails the build at commit time;
- four natures of building blocks with explicit composition rules.

Meanwhile, premature process separation has immediate, concrete costs
at the project's current scale: distributed state (an ELO update
crossing a network boundary needs retries and sagas instead of one
transaction), N× deployment versioning, cross-process debugging
without distributed tracing, and — specific to this project — a larger
surface the game designer must understand to create a mod.

## Decision

BotForge stays a **modular monolith** (one runtime, one container)
until an ADR-0012 extraction trigger fires. To make the future
separation a non-event, every seam that is a **network-extraction
candidate** must satisfy the following contract rules from day one:

1. **Serializable payloads only.** Seam inputs/outputs are JSON-safe
   primitives, pydantic/dataclass models, or `IChannel`-style
   lightweight views — never live `discord.py` objects. Platform
   objects stay inside the platform implementations.
2. **No shared state.** A block's durable state lives in its own
   collections, accessed only through its own database seam. No
   cross-domain collection reads.
3. **Explicit error taxonomy.** Seams raise the typed exception
   hierarchy (botforge-services#10), not library exceptions — a
   network boundary must be able to map errors without importing the
   library that raised them.
4. **Calls are async and idempotent-friendly.** Every seam method is
   async; provisioning/setup methods are idempotent (already the
   repo norm), so a retry across a future network hop is safe.

**Planned extraction order** (when triggers fire, each with its own
ADR and interface contract, per ADR-0012):

1. **Data providers** (`games/<game>/providers/`) — they talk to
   external APIs with their own rate limits, latency and downtime;
   isolating them protects the bot's event loop. First extraction
   candidate, expected around v0.4.0/v0.5.0.
2. **Webapp** (ADR-0015) — a request/response frontend is naturally
   its own process.
3. **Mods and games** — only on real triggers (independent release
   cadence, external contributors, isolated secrets, distinct
   scaling). No scheduled extraction.

## Alternatives Considered

- **Full microservices now** (`bot_discord`, `svc_core`, `svc_aoe2`,
  `mod_tournament`, `provider_aoe2lobby`, ...). Rejected: pays the
  distributed-state, deployment and observability costs immediately
  for scale the project does not have, and multiplies the surface the
  game designer must understand — simplicity is a product requirement
  of the vibe-coding platform.
- **Partial split now** (extract the data providers immediately).
  Rejected for now: no provider exists yet (#27 lands the first one);
  extracting a service before its contract has survived real usage
  freezes the wrong interface. The provider seam will be born
  extraction-ready (rules above), making the later move mechanical.

## Consequences

### Positive

- The expensive part of "microservices later" is already paid for:
  boundaries exist and are CI-enforced; extraction becomes a
  deployment change, not a redesign.
- One transaction for cross-domain updates; one deployment; one place
  to read logs while the project is small.
- The game designer composes features as packages + YAML, not as
  a fleet of services.

### Negative

- Extraction requires discipline on the contract rules above — a
  review checklist item for every new seam (added to the contribution
  guidance).
- A genuine scaling surprise (a mod exploding in CPU) must be
  mitigated within the monolith first (process-level isolation
  options), until its extraction ADR lands.

## References

- [ADR-0012](012-taxonomy-repo-strategy.md) — taxonomy, dependency
  matrix and extraction triggers
- [ADR-0011](011-protocol-interfaces.md) — Protocol seams
- [ADR-0015](015-webapp-api-boundary.md) — webapp boundary
- botforge-services#10 — typed exception hierarchy (rule 3)
- botforge#109 — product plan phases where extractions are expected
