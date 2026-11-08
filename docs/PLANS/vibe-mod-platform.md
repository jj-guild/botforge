# Vibe-coding mod platform — long-term platform plan

**Status: PLANNING (Phase 4+).** This is a new **platform element**, not a mod:
a productized surface that lets game designers — and eventually community
members — specify, review and validate mods co-constructed with AI agent
sessions, without ever touching GitHub or a terminal.

- Tracked by [botforge#136](https://github.com/jj-guild/botforge/issues/136) (Epic K).
- Builds on the existing internal workflow
  ([VIBEWORKFLOW.md](../VIBEWORKFLOW.md)) — it **productizes** it; it does not
  replace the underlying pipeline (issues → PRs → CI → deploy → validate →
  tag/release).
- Nothing here is decided: each section records the candidate options, the
  constraints and what is missing to start development. An **ADR per decision
  axis** is required before any implementation (see *Decision plan*).

## 1. Vision

Today, one game designer works with agent sessions through GitHub issues and
PRs. The developer merges. This works but does not scale: every new idea
requires GitHub literacy, and every step requires the developer as
gatekeeper.

The platform's target state: a **single assisted entry point** where a mod
idea travels the whole pipeline —

```
idea → shaped design → tracked issue → branch + PRs (CI green)
     → deploy to a chosen environment → designer validation
     → tag + release
```

— where the *only* human actions are creative (designing, challenging,
validating) and governance (approving), performed from a non-technical
surface.

Two maturity stages:
1. **Internal** (game designers of the org): removes GitHub from their path.
2. **Community** (external designers propose mods for their own servers):
   adds identity, quota, trust and moderation concerns.

## 2. Interaction channel (open — ADR required)

The first decision: through which surface do humans talk to the platform?

| Option | Strengths | Weaknesses | Verdict candidate |
| ------ | --------- | ---------- | ----------------- |
| **Discord text** (threads, forms, buttons) | Zero onboarding — the community already lives there; threads map naturally to "one mod = one workspace"; existing bot surface patterns (Discord Components v2, ADR-0009) | Structured editing of long design docs is clunky; message-length and history limits; harder audit trail than GitHub | Strong candidate for stage 1 (internal) |
| **Discord voice** | Designers think out loud; the richest idea capture | Transcription cost and error rate; no reviewable artifact without a transcription + structuring step; privacy consent needed | Candidate as an *input mode* within a Discord flow, not the backbone |
| **Web UI (webapp per ADR-0015)** | Best structured editing, review and status views; the natural long-term home for a "mod workshop" | A whole new frontend surface to build, secure and host; splits the community's attention away from Discord | Strong candidate for stage 2 (community) |
| **Hybrid** — Discord for conversation and notifications, web UI for structured design editing and review | Each surface does what it is best at | Two surfaces to build and keep coherent | The likely long-term shape; stage 1 can be Discord-only |

**Recommendation to challenge with the game designers:** stage 1 Discord-only
(text threads + forms), stage 2 adds the web UI. Voice enters later as an
input mode if demand appears.

## 3. Human roles and constraints

| Role | Who | Actions on the platform | Constraints |
| ---- | ---- | ----------------------- | ----------- |
| Game designer | Org member, non-developer | Submits ideas, answers the agent's shaping questions, validates deployed behavior | Never sees GitHub; approval weight: design only |
| Community designer (stage 2) | External, non-developer | Same as above for their own server's mods | Quota-limited; requires trust level / moderation screening |
| Developer | Org maintainer | Reviews and merges platform-relevant PRs; approves architecture | Cannot be in the loop for every community mod — must be needed only for platform and high-risk changes (this is the main scaling constraint to design around) |
| Ops | Org maintainer | Environment, secrets, prod approvals, resource quotas | One-time + incident path |
| AI agent (Vibe Code) | Mistral-powered | All technical work: shaping, issues, code, PRs, CI, deploys, tags/releases | Never merges; identity and audit per session; cost per session is a real budget line |

**Key constraint to resolve:** today's model puts the developer's Merge click
on every PR. A platform serving many designers requires a **graduated trust
model** — e.g. automatic merge for agent PRs that touch only mod-scoped
content (YAML, docs, mod code) with all CI checks green + agent review pass,
and developer review reserved for core/platform/infra changes. This is a
ruleset + risk-scoping design task, and a cultural decision: it must be an
explicit ADR validated by the developer.

## 4. Quality of service

- **Concurrency:** how many agent sessions can run simultaneously? (Cost,
  hosting load, CI queue length.) Needs a session-scheduler design and a hard
  cap per environment.
- **Cost control:** each session consumes model tokens + CI minutes + deploy
  time. Needs per-designer quota and budget alerts before community stage.
- **Latency/UX:** a designer must get a visible progress signal at each
  pipeline step (shaping → issue → PR → CI → deploy → validation), not
  silence. The status view is a first-class deliverable.
- **Isolation:** community mods must not be able to break the core or other
  mods — mod sandboxing/scoping rules already exist via `ModRegistry`; the
  platform must enforce them automatically (automated scope checks in CI, not
  human review).
- **Fairness:** community stage needs anti-abuse rules (request rate, idea
  size, rejections) — define with the community, not imposed.
- **Durability:** platform state (sessions, statuses, quotas) must be durable
  in MongoDB like the rest; no in-memory-only workflow state.

## 5. Communication / UX

- **Language:** non-technical French/English per the game designer's
  preference (i18n system already exists, ADR-0008); no jargon — the platform
  translates ("your mod is being tested on the test server", not "PR #123 CI
  green").
- **Transparency:** every automated action must be explainable after the
  fact — a visible, human-readable trace of what the agent did and why
  (links to the underlying GitHub artifacts for those who want depth).
- **Feedback loop:** validation happens in Discord on the deployed
  environment (the designers' existing habit) — the platform's job is to
  route feedback to the right session/issue automatically.
- **Announcement & community framing:** before community stage, an RFC-style
  post (per the monetization doc's consultation principle) presenting the
  platform, its limits and its cost model.

## 6. Pricing direction (parked)

Stage 1 (internal) has no pricing. Community stage has a real cost per
designer (model tokens, CI, hosting) and therefore a pricing question —
**parked under glass** exactly like the monetization axes: see
[monetization.md](monetization.md). Candidate directions (free tier with
quota, pay-per-deploy, community sponsorship) are captured there in Axis A's
spirit but are **not decisions**. Community consultation first.

## 7. What is missing to develop this feature (gap list)

Capabilities that do **not** exist today and must be built or decided first:

1. **Agent-facing API surface** — a programmatic bridge between the
   interaction channel and GitHub/CI/deploy: today the agent operates GitHub
   directly in a session; the platform needs a durable orchestration layer
   (session state machine: idea → shaping → issue → PR → deploy → validate →
   release) that survives across sessions. Largest single gap.
2. **Channel decision** (section 2) + the corresponding surface work
   (Discord Components v2 flows, or webapp screens per ADR-0015).
3. **Graduated trust model** (section 3): automated merge rules, risk-scope
   classification of PRs, ruleset changes — requires a developer-validated
   ADR.
4. **Session scheduling, quotas and budget monitoring** (section 4).
5. **Human-readable status/trace view** (section 5).
6. **Community identity & moderation** (stage 2 only): external accounts,
   trust levels, abuse handling.
7. **Pricing/community consultation** — parked (section 6).

## 8. Decision plan (ADRs required before implementation)

| # | Decision | Depends on |
| - | -------- | ---------- |
| 1 | Interaction channel (stage 1 and stage 2 shapes) | Community habits, ADR-0015 |
| 2 | Graduated trust model (what merges without a human) | Risk appetite, ruleset mechanics |
| 3 | Orchestration layer architecture (where the session state machine lives) | Decision 1, process split (ADR-0020) |
| 4 | QoS limits and quota model | Cost data from real usage |
| 5 | Community opening (identity, moderation, pricing) | Monetization consultation, legal |

## 9. History

- 2026-09-30: epic created as [botforge#136](https://github.com/jj-guild/botforge/issues/136)
  (Epic K) after the co-construction platform discussion; plan document
  added, pricing direction explicitly parked.
