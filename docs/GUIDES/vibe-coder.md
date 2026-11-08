# Guide — Vibe coder (AI agent session)

You are an AI session with **no memory of previous conversations**.
This page is your boot checklist; the repo is the source of truth.

## Boot sequence (every session)

1. Read [CONVENTIONS.md](../CONVENTIONS.md) (language, checks, PR
   lifecycle) — non-negotiable.
2. Read [VIBEWORKFLOW.md](../VIBEWORKFLOW.md) (roles, approvals) and
   the target repo's `AGENTS.md` + `docs/DEVELOPER.md`.
3. `git status`, current branch, recent commits — never assume a clean
   state.
4. Find the work: the issue at hand (milestone
   [v0.4.0](https://github.com/jj-guild/botforge-services/milestone/3)),
   its dependencies, and the generated roadmap for context.

## Working rules (from the decisions taken with the developer)

- **First question of every session: what is this session for?** Ask
  the human before doing anything. Two kinds of work, two workflows:
  a **personal mod** (sandbox mode — the game designer's own game) or
  **platform work** (pro mode — core, platform, infra, shared
  features). When the human wants to create a mod, help and guide
  them: point to [mod-developer.md](mod-developer.md) and the mod
  bootstrap path (rules in `docs/MODS/<mod>/`, ownership in the
  roster) rather than starting from a blank slate.
- **`main` is right by default.** When a session's opinion conflicts
  with `main` (architecture, conventions, existing patterns), assume
  `main` is right; follow it. Disagreements are raised to the human
  (and, for core/platform, to the maintainer) — never worked around.
- **Personal mod (sandbox mode): stack commits on the integration
  branch, not PRs.** Push commits directly to the user's integration
  branch `vibe/<alias>/main`. Exactly one draft **mod PR**
  (`vibe/<alias>/main` → `main`) stays open for the whole life of the
  mod — opened on the first push, re-running the required checks on
  every push (that is its purpose: continuous validation of the
  stack). Never stack additional PRs on top of it. It goes ready and
  merges only when the owner judges the mod complete; until then it
  stays in draft, whatever the state of its checks.
- **Platform work (pro mode): collaborative feature branches → PRs to
  `main`.** One branch per subject (`vibe/<slug>`), PRs reviewed by
  CODEOWNERS, normal reviewable size — several PRs may be open in
  parallel (they are collaborative; sequential chaining is not
  required). Scope each PR like a review lot: one coherent unit a
  human can review in one sitting. Big issues are split into sub-PRs
  (e.g. ladder core
  [#134](https://github.com/jj-guild/botforge-services/issues/134):
  data model → matchmaking → state machine/rating → invites).
- **Tests land with every change** — the blanket mandate
  ([#139](https://github.com/jj-guild/botforge-services/issues/139))
  covers every v0.4.0 issue: acceptance properties in CI, coverage not
  lowered on touched paths.
- **Docs are part of the PR**: `make docs` freshness, mod docs in the
  botforge repo updated in the same PR when rules change.
- Before pushing: `make lint`, `make typecheck`, `make test` — all
  green, always. CI failures you caused get fixed before anything new.
- Never click Merge yourself. Ready = checks green + deployed to test +
  verified + nothing left for you to do; going ready enables automerge.
  CODEOWNERS name the owners (a mod's designer reviews their mod; the
  maintainers review the core/platform) — GitHub merges the ready PR
  once their approvals land. Never force-push without approval. Never
  touch protected branches.
- Architecture: ADRs are binding
  ([ADR-0020](../DECISIONS/020-process-split-bot-core-providers.md)
  process split; if you disagree, raise it, don't workaround it).
- gRPC contracts: edit `.proto` in `contracts/`, regenerate with
  `make contracts`, never hand-edit stubs.
- If a step needs a human (secrets, production approval, review), stop
  and ask — see [VIBEWORKFLOW](../VIBEWORKFLOW.md) for who does what.

## Session flow

```
read docs → issue → integration branch vibe/<alias>/main (personal
mod: stack commits; mod PR opened on first push) or vibe/<slug> (pro
mode) → implement + tests → lint/typecheck/test/docs → push (mod PR
checks re-run) → report + CI watch
```

Report the PR URL, what was verified, and what remains. If the
developer says "continue", keep working the open PR or open the next
one in the same session rules.

## Audience-specific pointers

- Building a mod → [mod-developer.md](mod-developer.md)
- Building a game/provider → [game-provider.md](game-provider.md)
