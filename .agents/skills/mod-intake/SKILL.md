---
name: mod-intake
description: Guide a novice user (vibe-coder or game-designer) through creating a new mod — intake questionnaire (purpose, seasonal, enrollment criteria, universe/entities), reuse-first check against the core and existing mods, scaffold via `botforge mod init`, convention compliance. Use whenever a session starts creating a new mod, whatever the user's skill level.
---

# Mod intake — the guided parcours for a new mod

A session building a mod never improvises: it runs this questionnaire,
checks what already exists before writing anything, scaffolds with the
committed tool, and only then implements. The outcome is uniform — the
same structure, the same seams, the same conventions — whatever the
user's inputs. **The intake is a conversation in plain language; the
implementation is not.**

## 1. The intake questionnaire (ask, in this order)

Ask in the session's working language, one question at a time, in plain
words. Never ask anything technical (no "schema", no "Mongo").

1. **What does the mod do?** One sentence a player would understand.
   → if the idea is unshaped, run
   [shape-game-designer-idea](../shape-game-designer-idea/SKILL.md)
   first, then come back.
2. **Is it seasonal?** Does it run as a season (a period with a start
   and an end, everything reset per season) or is it always on?
   → `seasonal: true|false` — MANDATORY in the declaration.
3. **Who can join?** Free for everyone, or should candidates be checked?
   - nothing to check → no enrollment criteria;
   - checked by a human → `manual: true` (candidates queue, admins
     accept/refuse from the dashboard);
   - checkable automatically → the criteria library
     (see §2) — all-pass auto-accepts, a failure refuses with the reason,
     `manual` on top sends passing candidates to the queue anyway.
4. **What is the universe?** The entities (kingdoms, civs, maps, teams…),
   their names, and their interactions. One entity per row; keep the
   entity list stable (entities become forum posts and Mongo documents —
   renaming later is a migration).
5. **What does the player see?** The surfaces: channels (the mod's
   groups and channels), commands, pinned panels. Translate each into
   declaration data — a channel is a config line, never code:
   - `channel_groups:` — the Discord categories, declaration order =
     display order; `admin_only` (mod admin roles + bot admins only) and
     `read_only` (nobody writes) on the group AND its channels;
   - `channels:` — `group:` (validated at boot), `kind:`
     (text/forum/announce — announce is admin-written, read-only by
     default), `access.view`/`access.post` with the mod's **role keys**
     (`view: [lord, king]` — resolved from the declared roles); mark
     the mod's admin role with `admin: true` (the `admin_only`
     audience). No auto-heal: the Synchroniser button is the only
     re-creation path.
6. **When do inscriptions open?** A window gates `apply` itself:
   `opens_at`/`closes_at` (ISO timestamps) or `opens_before_start: 7d`
   (seasonal — inscriptions open before the season's start).

## 2. The enrollment criteria library (automatable checks)

Prefer an automatable criterion over a human gate — the dashboard
remains for the edge cases. Declared in `settings.enrollment`:

| Criterion | Declared as | Checks |
|---|---|---|
| `min_elo` | `min_elo: 1200` or `min_elo: {value: 1000, leaderboard: rm_1v1}` | the player's rating ≥ the value (optionally one leaderboard) |
| `max_elo` | `max_elo: 1500` (same mapping form) | the rating ≤ the value — the 1000-1500 range case |
| `min_matches` | `min_matches: {count: 5, days: 30}` (add `leaderboard:`) | X matches in the last Y days (optionally one leaderboard) |
| `requires_profile` | `requires_profile: true` | a bound, validated game profile (the mod's game) |
| `requires_profiles` | `requires_profiles: [aoe2, aoe4]` | a bound account on EVERY declared game |
| `manual` | `manual: true` | every candidate waits for an admin |

The window keys (`opens_at`, `closes_at`, `opens_before_start`) ride in
the same `settings.enrollment` mapping — they gate the apply, they are
not criteria.

Composition rule: all pass → auto-accept (unless `manual`); any failure →
refused with the failing reasons recorded; an unknown stat (unrated
player, missing history) degrades to a refusal reason "manual review" —
never a crash, never a silent accept.

## 3. Reuse-first check (before writing any code)

Run, in order, and tell the user what you found:

1. `uv run botforge mod list` — existing mods; an existing mod doing
   the job may answer without new code (depend on it via
   `dependencies:`).
2. The core inventory (see the guide): seasons (one active max,
   rotations), `SeasonRolesService` (per-season roles),
   `EnrollmentService` (apply/criteria/queue), `MembershipService`
   (register/unregister + role sync), `AdminModSection` (admin
   dashboards), `EntityForumSpec` (universe entity forums),
   `build_mod_season_stack` (the whole seasonal stack wired in one call).
3. The mod catalogue
   ([docs/MODS/CATALOGUE.md](../../../docs/MODS/CATALOGUE.md)) —
   something at maturity 2-3 may be extendable instead of rebuilt.

**The core/mods split rule**: duplicated machinery in a mod is a
factorization bug — if two mods need it, it belongs to the core (raise
it, do not copy it).

## 4. Scaffold, then implement

1. `uv run botforge mod init <name> --seasonal|--permanent
   [--private --owner <discord-id>]` — the self-contained directory
   (`modules/mods/<name>/`): declaration, package skeleton with the
   three lifecycle hooks, locales, tests.
2. Fill `mod.yaml` from the questionnaire answers (channels, roles,
   commands, `settings.enrollment`).
3. Implement against the core seams only — never import `discord.py`
   directly (the UI SDK builds every surface), never hardcode platform
   ids, never extend core enums.
4. Locale every user-facing string (`locales/en.yaml` + `fr.yaml`).
5. Tests: MockDiscord + in-memory stores, same seams as production.
6. `make lint typecheck test` — green before any push.

Reference: [docs/GUIDES/mod-init.md](../../../docs/GUIDES/mod-init.md)
(the canonical guide), the ladder and kingdoms examples
(`modules/mods/`).

## 5. Conventions — and deliberate deviations

Follow the project conventions by default:
[docs/CONVENTIONS.md](../../../docs/CONVENTIONS.md),
[architecture/mods.md](../../../docs/architecture/mods.md). The
enrollment UX follows the kingdoms precedent (Drasah's apply flow): one
ephemeral bubble per parcours (edited, never stacked), pending ⏳ /
accepted ✅ / refused ❌ states, restart-proof action buttons
(`<mod>:<component>:<payload>` custom ids).

A deviation is acceptable **only when deliberate**: state the reason in
the PR description ("deviates from X because Y"), and link it from the
mod's docs. An undocumented deviation is drift — the session drift
watchdog will find it.

## Deploying and validating a new mod — the learned pitfalls

After `make lint typecheck test` and the PR CI is green, the mod deploys
with `/deploy <env>` (a PR comment) and validates on the test Discord.
The lessons below come from real sessions — each one cost an hour:

- **Command visibility ≠ permission.** A slash command synced by an
  enabled mod is visible to EVERYONE on every guild the bot is on; the
  per-guild access gate only provisions channels/roles. Every mod
  command MUST validate the guild's granted access at click time
  (``build_guild_access_service().enabled_mods(guild_id)``) and deny
  ephemerally — *seeing a command never implies being allowed to use
  it* (AGENTS.md, runtime permission mandate). Add `@guild_only()`.
- **A mod that fails to load is invisible, not red.** Mod loading is
  best-effort by design; a broken import logs one line and the bot
  boots "green" without the mod. After deploying, ALWAYS check the env
  logs (`/logs <env>`) for `MOD <name> registered` — never trust the
  deploy pipeline alone.
- **The env state branch is last-writer-wins.** Deploying a PR pins
  `deploy/<env>`; another PR deployed minutes later replaces the pin —
  your validation silently tests someone else's code. Before validating,
  confirm the pin (`envs/<env>/state/botforge-bot.yml`) carries YOUR
  image; `/reset-env` wipes the access grants too — the guild must
  re-request access after a reset.
- **Approval ≠ provisioning.** Granting a mod from the admin DM used
  to only write the grant; the channels appeared at the next restart.
  The approve button now re-provisions immediately — but if a guild
  reports "approved, nothing happened", check the logs for the
  post-approval provisioning pass.
- **Slash-command sync latency is Discord-side.** A global sync can
  take up to ~1h to reach every client; a client refresh (Ctrl+R)
  usually reveals it sooner. Guild-scoped sync (`CICD_GUILD_ID` on the
  env) is instant — prefer it on test envs.
- **Mod loading happens once at boot.** A fix pushed after the deploy
  needs a re-deploy to take effect; `/restart <env>` is not enough if
  the image pin did not change.

## Anti-patterns

- Writing plumbing the core already owns (season numbering, role sync,
  admin panels, forums) — §3 first, always.
- "The bot decides who joins" → ask for the exact rule; every criterion
  is checkable or it is `manual`.
- A mod with no `seasonal` flag — startup fails loudly (by design).
- Starting the implementation before the questionnaire is complete —
  the intake is what makes mods uniform across users.
- A mod command without the click-time access guard — see *Deploying
  and validating* above; the sync surface is public by construction.
