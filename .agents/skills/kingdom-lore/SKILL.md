---
name: kingdom-lore
description: Load the Kingdoms mod lore in EVERY session that touches the kingdoms mod (territory-conquest AoE2 meta-game) — its docs, its code (modules/mods/kingdom in botforge-services), its Discord surfaces, its issues. Use whenever the human works on kingdoms or asks about kingdoms mechanics. The agent must know the lore better than the mod's designer and proactively propose/anticipate the next moves.
---

# Kingdoms lore — load it in every kingdom session

The Kingdoms mod is a **territory-conquest meta-game on AoE2**: player
Kingdoms (one Roi + Seigneurs) fight each other and Gaïa (the AI
kingdom) for maps, week after week, across seasons; the bot is the
world-state manager. The lore lives in this repo — **an agent working on
kingdoms without having read it is working blind**.

## Mandatory load (every kingdom session, before any work)

Right after the session-start protocol (AGENTS.md PRIORITY 0), when the
task touches the kingdoms mod in any way — code, docs, Discord surfaces,
issues, PRs — read **in full**:

- `docs/MODS/kingdoms/README.md` — purpose, concepts, core integration
- `docs/MODS/kingdoms/RULES.md` — the game rules
- `docs/MODS/kingdoms/DECISIONS.md` — the validated decisions (**win over everything**)
- `docs/MODS/kingdoms/PROMISES.md` — the marriage personalities
- `docs/MODS/kingdoms/CADASTRE.md` — map effects
- `docs/MODS/kingdoms/ENVIRONMENT.md` — season configuration
- `docs/MODS/kingdoms/CIVILIZATIONS.md` — civilization unlock conditions
- `docs/PLANS/reference/kingdoms-mod-saison2.md` — the Season II reference, the **functional source of truth**

**Precedence:** the Season II reference is the functional source of
truth; where it and `DECISIONS.md` disagree, the decisions win. Anything
marked **À DÉFINIR** must NEVER be invented by an implementation — ask
the human (UI select, [human-interaction](../human-interaction/SKILL.md)).

## The one-paragraph lore (so a session can reason before the full read)

Seasons (4 weeks/cycles by default, admin-launched, full data reset);
Kingdoms = Roi + 4 lords by default, Gaïa is the AI kingdom; a territory
is one AoE2 map, drawn from the allowed list, never duplicated within a
season; each lord has 1 attack + 1 defense per week (6h lead for player
kingdoms, 3h for Gaïa; Gaïa attacks are winner-takes-all FFA); weekly
events — Exploration (Sat 14:00, optional FFA), Lord's Day (Sun 23:30:
Gaïa maps, cadastre, alliances), era change (Wed midnight); technologies
are the currency (Embuscade, Traquenard, Patrouille, Contre-espionnage,
Sabotage, Explorateur, Jeu d'armes, Mariage arrangé, Corruption, Garde
Royale); diplomacy — civ-bound alliances, marriages, treaties, Royal
Order. Core integration: seasons register as `kingdoms-aoe2-<guild>-<index>`,
maps/pools come from the core game catalog, players from the core
identity service, territories post in the core `kingdoms-territories`
forum.

## Code map (botforge-services)

The mod lives in `modules/mods/kingdom/` — `conf/mod.yaml` (declaration:
salons, groups, roles), `conf/views.yaml` (declared surfaces),
`conf/locales/{fr,en}.yaml` (ALL user-facing strings, parity-tested),
`cogs/kingdom/` (the Discord layer — the only place `discord` may be
imported), `src/kingdom/` (game logic, never imports discord),
`grpc/kingdom/` (the service singleton: `mod_service("kingdom").stack()`).

The platform rules that apply to every mod change are pinned in
[discord-ui](../discord-ui/SKILL.md) and `docs/CONVENTIONS.md`:
view ids `panel:mod:<name>:…`/`menu:mod:<name>:…` (R9), the admin console
is SDK-owned (`panel:mod:<name>:admin:console` + the 🛠️ button), data
i18n only, English conventional commits only.

## Anticipation mandate (the designer must feel understood)

- **Propose, don't just execute.** At every milestone of a kingdom
  session, end with 2–4 concrete next moves drawn from the lore + the
  open issues/roadmap — each with a one-line rationale and the lore
  reference (file + section). Ask via a **UI select**
  ([human-interaction](../human-interaction/SKILL.md)), never a bare
  question. Example shape: « Next moves I see from RULES §Attaques:
  (a) defense-budget HUD on the attack panel, (b) … — which one? ».
- **Challenge before coding.** When the human brings an idea, check it
  against RULES.md / DECISIONS.md FIRST
  ([shape-game-designer-idea](../shape-game-designer-idea/SKILL.md)):
  say what conflicts, what the lore implies, and propose the variant
  that fits the design — then shape it into an issue.
- **Anticipate the seams.** The lore names flows the bot must serve
  (weekly events, cadastre, alliances, marriages, market, FFA,
  distributor, time machine). When a session touches one, sweep the
  neighboring lore surfaces for what's missing and propose them —
  that is how the mod reaches "works like the reference branch".
- **Discourse adapts to the roster profile** (AGENTS.md PRIORITY 0): the
  kingdoms designer is a vibe-coder/game-designer — plain language,
  outcomes, next clicks, in the human's chat language; GitHub output
  stays English.

## Working rules specific to this mod

- Never invent an **À DÉFINIR** item — escalate to the designer.
- The mod is game-bound to AoE2: hard-coded AoE2 options are intentional.
- Player-facing surfaces are pinned panels/menus; admin ops live in the
  mod console; no extra slash commands unless explicitly requested.
- Every user-facing string is i18n (fr/en yaml, parity test); timestamps
  render as `<t:…:R>`; modal inputs ride `discord.ui.Label`.
