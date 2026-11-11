# Architecture Decision Records (ADR)

ADRs document the major technical decisions of the BotForge project: the
context, the decision, the alternatives considered, and the consequences.
They are **permanent documentation** — the rationale behind our choices must
survive the people who made them.

## What is an ADR?

An Architecture Decision Record captures a single, important architecture
decision: what was decided, why, what alternatives were rejected, and what
the consequences are (positive and negative).

## ADR format and structure

Every ADR follows the template ([decision-template.md](decision-template.md)):

1. **Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXX
2. **Date**: YYYY-MM-DD
3. **Context**: the problem and the forces at play
4. **Decision**: what was decided, in verifiable wording
5. **Alternatives Considered**: what else was on the table, and why it was
   rejected
6. **Consequences**: positive and negative outcomes
7. **Diagrams** (optional): Mermaid illustrations
8. **References**: related docs and issues

## How to create a new ADR

1. Copy `decision-template.md` to `NNN-short-title.md` where `NNN` is the next
   free number (zero-padded, e.g., `009`).
2. Fill every section — an ADR without alternatives and consequences is
   incomplete.
3. Start with status **Proposed** — unless the decision was shaped and
   challenged collaboratively with a human during the session, in which case
   it starts as **Accepted** with the co-construction recorded in the ADR
   body (see AGENTS.md).
4. Open a PR (per the vibe-coding workflow, see
   [../VIBEWORKFLOW.md](../VIBEWORKFLOW.md)).

## Numbering and versioning

- ADRs are numbered sequentially in decision order; numbers are never
   reused.
- ADRs are **immutable**: never edit an accepted ADR in place. If a decision
   changes, write a new ADR and mark the old one
   `Status: Superseded by ADR-NNN`.
- Superseded ADRs stay in the directory for the record.

## Relationship to CHANGELOG

ADRs record **why** a decision was made; the changelogs
(`docs/MODS/*/CHANGELOG.md`, releases) record **what** changed and when. A
change that reverses an ADR must produce both a new ADR and a changelog entry.

## Index

| ADR | Decision |
| --- | -------- |
| [001](001-multi-platform-architecture.md) | Multi-platform architecture (`IPlatform`) |
| [002](002-workflow-engine.md) | Workflow engine |
| [003](003-channel-categories.md) | Channel categories (`ChannelService`) |
| [004](004-mongodb-schema-design.md) | MongoDB schema design |
| [005](005-redis-state-management.md) | Redis state management |
| [006](006-docker-compose-infra.md) | Docker Compose infrastructure |
| [007](007-gitops-deployment.md) | GitOps deployment |
| [008](008-i18n-system.md) | YAML-based i18n |
| [009](009-discord-components-v2.md) | Dual Discord UI system (embeds + Components V2) |
| [010](010-redis-hosting.md) | Redis hosting (Redis Cloud free tier for prod) |
| [011](011-protocol-interfaces.md) | Structural typing (`typing.Protocol`) for core interfaces |
| [012](012-taxonomy-repo-strategy.md) | Taxonomy of building blocks, boundaries and repo strategy |
| [013](013-cross-platform-identity.md) | Cross-platform identity, OAuth providers and account merge |
| [014](014-rbac-permissions.md) | RBAC: application roles, grants and permission enforcement |
| [015](015-webapp-api-boundary.md) | Webapp frontend and API boundary |
| [016](016-discord-permissions-and-delivery.md) | Discord permissions & message delivery (DM vs channel, runtime role checks, channel access policies) |
| [017](017-packaging-distribution.md) | Packaging and distribution (workspace, private index, PyPI) |
| [018](018-environment-state-branches.md) | Per-environment state branches (GitOps deploy state) |
| [019](019-modular-monolith-extraction-contracts.md) | Modular monolith — extraction contracts |
| [020](020-process-split-bot-core-providers.md) | Process split: bot core / providers |
| [021](021-architecture-five-rules.md) | The five architecture rules — enforced, not remembered |
| [022](022-hosting-evaluation-path.md) | Hosting evaluation path — VPS (incl. Kapsule trial) vs bare metal + hypervisor |
