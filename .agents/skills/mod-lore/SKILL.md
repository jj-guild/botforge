---
name: mod-lore
description: Load the lore of the mod the human wants to work on — docs/MODS/<mod>/ (README, RULES, ENVIRONMENT, DECISIONS, REFERENCE + extras) — at the start of every session that touches a mod (its code in botforge-services, its docs, its Discord surfaces, its issues). If the mod has no docs yet, say so and help scaffold them from docs/MODS/TEMPLATE/. Use whenever the human says they want to work on a mod (any mod, e.g. kingdoms).
---

# Mod lore — where to find it, when to read it

Every mod's lore lives in **one standard place**: `docs/MODS/<mod-name>/`
in this repo (see the hierarchy table in
[docs/MODS/README.md](../../../docs/MODS/README.md)). An agent working
on a mod without having read its lore is working blind.

## When this skill loads

The human says they want to work on a mod — *"I want to work on the
kingdoms mod"*, *"let's continue the ladder"* — or the task touches a
mod's code (`modules/mods/<mod>/` in botforge-services), docs, Discord
surfaces, issues or PRs. Resolve the mod name from the request (ask via
UI select if ambiguous), then apply the procedure below.

## Procedure

1. **Resolve the mod's doc directory**: `docs/MODS/<mod-name>/`.
2. **If it does not exist (or the standard files are missing)** —
   **tell the human, do not invent lore**: say via a UI select
   ([human-interaction](../human-interaction/SKILL.md)) that the mod has
   no docs yet, and offer to **scaffold them**: copy
   `docs/MODS/TEMPLATE/` to `docs/MODS/<mod-name>/` (README, RULES,
   ENVIRONMENT) and fill them with the designer in the session, then
   open the issue/PR. Until the lore exists, the agent works from the
   code + issues only and says so.
3. **Check the mod's status first** (table in
   [docs/MODS/README.md](../../../docs/MODS/README.md)): a deleted or
   unlisted dir (the old ladder/ and register/ relics are gone) means
   **no lore** — go to step 2. A current dir is read ALL of it, in full,
   before any work: the
   standard file set first (`README.md` — which must cover the 5 lore
   blocks: channel tree/roles, external-system integration, views &
   buttons, pinned salons, player/admin/bot interactions — note any
   missing block and fill it with the designer — then `RULES.md`,
   `ENVIRONMENT.md`),
   then `DECISIONS.md` and `REFERENCE.md` when present, then every
   mod-specific extra (e.g. kingdoms' `CADASTRE.md`, `PROMISES.md`,
   `CIVILIZATIONS.md`).
4. **Precedence**: `REFERENCE.md` (the designer's functional reference)
   is the functional source of truth; `DECISIONS.md` wins over both.
   Anything marked **À DÉFINIR** must NEVER be invented by an
   implementation — escalate to the designer.
5. **Load the code map** — and the SDK map: read
   `docs/architecture/mods.md` §8 (how a mod plugs into the stack: import
   mapping, allowed/forbidden imports, Mongo/Redis/provider data
   ownership, isolation R1–R9). The mod's code lives in
   `modules/mods/<mod>/` in botforge-services — `conf/mod.yaml`
   (declaration: salons, groups, roles), `conf/views.yaml` (declared
   surfaces), `conf/locales/{fr,en}.yaml` (ALL user-facing strings,
   parity-tested), `cogs/<mod>/` (the Discord layer — the only place
   `discord` may be imported), `src/<mod>/` (game logic, never imports
   discord), `grpc/<mod>/` (the service singleton:
   `mod_service("<mod>").stack()`). The platform rules that apply to
   every mod change are pinned in [discord-ui](../discord-ui/SKILL.md)
   and `docs/CONVENTIONS.md` (view ids `panel:mod:<name>:…`/`menu:mod:<name>:…`
   R9, SDK-owned admin console, data i18n, English conventional commits).

## Anticipation mandate (the designer must feel understood)

- **Propose, don't just execute.** At every milestone, end with 2–4
  concrete next moves drawn from the mod's lore + its open issues —
  each with a one-line rationale and the lore reference (file + section).
  Ask via a **UI select**, never a bare question.
- **Challenge before coding.** Check any idea against the mod's
  `RULES.md` / `DECISIONS.md` FIRST
  ([shape-game-designer-idea](../shape-game-designer-idea/SKILL.md)):
  say what conflicts, what the lore implies, propose the fitting
  variant — then shape it into an issue.
- **Sweep the neighbors.** When a session touches one flow, sweep the
  mod's other lore surfaces for what's missing and propose them.
- **Discourse adapts to the roster profile** (AGENTS.md PRIORITY 0): a
  mod designer who is not dev/ops gets plain language, outcomes and next
  clicks in the human's chat language; GitHub output stays English.

## Technical guardrails — the agent owns them, the human never debugs them

A mod dev does not need to be an expert in the platform's technical
chantiers. When a check goes red, the agent reads the failing test,
explains it in ONE plain sentence, and fixes it. In plain language:

- **DB isolation (rule R5)** — every Mongo collection has ONE owner
  package; the mod only touches its own. Never add a raw collection
  read — move the access to the owning service.
- **Process isolation (rule R1)** — external providers (liquipedia,
  aoe2lobby…) run as their own processes; the mod reaches them only
  through the named provider seam, never by URL.
- **gRPC seams** — the mod's service is reached via
  `mod_service("<mod>").stack()` / `.service()` (the grpc package owns the
  singleton); a cog never builds the stack by hand.
- **Layering R1–R9** — `tests/architecture/` enforces the rules
  automatically (R6: no `import discord` outside the mod's cogs; R9: view
  ids `panel:mod:<name>:…`). A red architecture test is the agent's fix,
  not the human's.

## Anti-blocker kit (when the session runs alone)

- **CI red** → read the failing job logs; the reflexes are in
  [ci-monitoring](../ci-monitoring/SKILL.md) (pydoc stale → `make docs`;
  Check commits red → reword to English conventional; …).
- **Deploy / logs / status / restart** → PR comments `/deploy`,
  `/logs <env>`, `/status <env>`, `/restart <env>` (a vibe-coder uses its
  OWN env; `test` only via the authorized path); poll the answer, never a
  fixed sleep ([github-polling](../github-polling/SKILL.md)).
- **Platform failure memory** → [troubleshooting](../troubleshooting/SKILL.md)
  before diagnosing from scratch.
- **Blocked on a platform rule or a maintainer decision** → one plain
  sentence in the PR comment naming the platform owner (roster). Never
  force-push, never merge, never rewrite history alone.
- **GitHub output is English + conventional commits** — the
  `Check commits` gate enforces it; reword, don't bypass.
