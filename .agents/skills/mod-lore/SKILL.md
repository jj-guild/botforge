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
   standard file set first (`README.md`, `RULES.md`, `ENVIRONMENT.md`),
   then `DECISIONS.md` and `REFERENCE.md` when present, then every
   mod-specific extra (e.g. kingdoms' `CADASTRE.md`, `PROMISES.md`,
   `CIVILIZATIONS.md`).
4. **Precedence**: `REFERENCE.md` (the designer's functional reference)
   is the functional source of truth; `DECISIONS.md` wins over both.
   Anything marked **À DÉFINIR** must NEVER be invented by an
   implementation — escalate to the designer.
5. **Load the code map**: the mod's code lives in
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
