# Mod init — starting a mod properly (`botforge mod init`)

This guide is **the reference** for starting a mod: the target layout, the
command that scaffolds everything, and two real example mods (ladder,
kingdoms). It serves humans **and** agents — a session creating a mod
starts here, improvises nothing, and saves its tokens for what matters
(the design, not the bootstrap).

Audience: game designers (via an agent session), developers, agents.

## 1. A mod = one self-contained directory

Since botforge#179, every mod lives in **one self-contained directory**
in `botforge-services` — the future extraction to an external repo
(botforge-services#211: a mod = one UV module + one Docker container +
its docs) will be a pure `git mv`:

```
modules/mods/<mod>/
  mod.yaml            declaration (ModRegistry schema, validated at boot)
  src/<mod>/         python package, imported as botforge.mods.<mod>
  locales/en.yaml    the mod's locale catalogs (merged at load time)
  locales/fr.yaml
  tests/             the mod's tests (run by make test)
  README.md          pointer to the canonical docs (botforge repo)
```

The mod's canonical documentation (rules, environment) stays in the
`botforge` repo: `docs/MODS/<mod>/` (README, RULES, ENVIRONMENT) —
never in `botforge-services`. **Two repos, two truths**: the code and
its declaration in `botforge-services`, the design in `botforge`.

The legacy layout (`src/botforge/mods/<mod>` +
`config/mods/<mod>.yaml`) remains supported and **wins on collision**
for the duration of the migration: a branch moving its mod keeps
precedence.

## 2. The command

```bash
uv run botforge mod init <name> [--seasonal | --permanent] [--private --owner <discord-id>]...
uv run botforge mod list
```

`init` generates the full directory above: a valid declaration, a
package with the three lifecycle hooks (`register`, `setup_hook`,
`close`), en/fr locales, an acceptance test, a pointer README. Nothing
is overwritten — an existing mod is refused.

`list` prints every declared mod and its layout (legacy or modular).

## 3. The mod contract (recap)

- `mod.yaml` follows the schema validated at boot — see
  [architecture/mods.md](../architecture/mods.md): `id`, `enabled`,
  `seasonal` **required** (the mod's type: seasonal → a lifecycle
  panel + per-season admin channels; permanent → a guild-level config
  panel), `settings`, `channel_groups`, `channels` (addressed
  `mod:key`), `roles`, `workflows`, `commands`, `dependencies`,
  `required_games`.
- **Channels are data, never code**:
  - `channel_groups` — the mod's Discord categories, declaration order
    = display order; `admin_only` (only the mod's admin roles +
    bot-admins see it) and `read_only` (nobody writes) apply to the
    group **and** to each channel (the default inheritance);
  - `channels` — `group` (reference validated at boot), `kind`
    (`text`/`forum`/`announce` — an announce channel is
    admin-written, readable by all, read-only by default);
  - `access.view`/`access.post` — the **role keys** declared by the mod
    (`view: [lord, king]`), resolved to names at load time; a role
    marked `admin: true` is the audience of `admin_only` channels. No
    auto-heal: the **Synchroniser** button of the section is the only
    re-creation path.
- **The lifecycle**: a suspended mod (`ModLifecycleService`, per
  guild) stays **manageable by admins** but **unusable by players** —
  `require_usable` is the gate of every player flow. Suspension is a
  flag, never a wipe.
- **Enrollment** (`settings.enrollment`): declarative criteria —
  `min_elo`/`max_elo` (scalar or `{value: …, leaderboard: rm_1v1}`),
  `min_matches` (`{count: 10, days: 30, leaderboard: …}`),
  `requires_profile`/`requires_profiles` (a linked account on every
  declared game), `manual` (admin validation; otherwise auto-accept
  when all criteria pass). The **window**: `opens_at`/`closes_at` (ISO
  timestamps) or `opens_before_start: 7d` (enrollments open before the
  season's start).
- **The map pool**: attached to a season (the season's `map_pool_id`,
  rotation = a new season with another pool) or to the mod via
  `settings.map_pool` — a `used` pool is frozen, never edited again.
- The mod's code talks **only to the core seams** (hooks, the UI SDK
  `botforge.discord.ui`, core services) — never to discord.py
  directly, never a hardcoded channel/role/guild id.
- The game-bound flag: a mod may be bound to a single game by design
  (kingdoms → AoE2) but **never owns** the game's data — the catalog
  belongs to the core `GameDataService`, the seasons to the core
  registry.

## 3b. Public and private mods

A mod is **public by default**. Declared `private: true` in the
`mod.yaml`, it becomes **private**:

- `owner_discord_ids` (the owners' Discord ids) is **required** — a
  private mod without an owner fails the boot (fail loudly);
- provisioning skips the guilds where **no** owner or bot-admin is a
  member;
- the surfaces (home menu, mod view dispatch) hide it from anyone who
  is not an owner or a bot-admin.

The scaffold does it in one command: `botforge mod init <name>
--private --owner <id> [--owner <id>...]`. Typical use: a mod under
construction that must not appear on production guilds before it is
ready.

## 4. The example mods

The two **move-in** pins (the target layout of real mods,
`enabled: false` while their code lives on the integration branches):

| | [ladder](../MODS/ladder/) | [kingdoms](../MODS/kingdoms/) |
|---|---|---|
| Type | seasonal, game-agnostic | seasonal, **game-bound (AoE2)** |
| Roles | 3 (mod staff + player/season_staff per season) | declared at move-in |
| Declaration | `modules/mods/ladder/mod.yaml` | `modules/mods/kingdoms/mod.yaml` (real, salons-first, from `vibe/drasah/main`) |
| Code | branch `vibe/merlin/main` (PR botforge-services#245) | branch `vibe/drasah/main` (PR botforge-services#244) |

The two `modules/mods/` directories pin **the target layout and the
real declaration**, with `enabled: false` while the code still lives
on the integration branch: the flag flips to `true` in the same PR as
the mechanical code move (one PR per mod, CI green at each step). That
is the pattern to follow for any existing mod.

## 5. The full path of a new mod

1. `uv run botforge mod init <name> --seasonal` (or `--permanent`)
2. Fill `mod.yaml` (channels, roles, workflows, commands)
3. Implement in `src/<name>/` against the core seams
4. Fill `locales/en.yaml` + `fr.yaml`
5. Document in the `botforge` repo: `docs/MODS/<name>/` from
   [TEMPLATE](../MODS/TEMPLATE/), a line in the
   [catalogue](../MODS/CATALOGUE.md) (maturity 1–2)
6. `make lint typecheck test`
7. Wire the design onto the vibe pipeline (issue, PR, deploy, tag) —
   see [VIBEWORKFLOW.md](../VIBEWORKFLOW.md)

## 6. The ready-to-wire generic systems

The core provides the full machinery — a declarative mod codes only
its specifics:

| System | Core service | What the mod declares |
|---|---|---|
| Enrollment journey | `EnrollmentService` | `settings.enrollment` (criteria from the library + `manual`) |
| Seasons (one active max, pool rotations, seasonal roles, enrollments) | `build_mod_season_stack` | `seasonal: true` + the `per_season` roles |
| Simple membership (register/unregister + role sync) | `MembershipService` | its business hooks |
| Admin dashboards (candidates/enrolled/accepted) | `AdminModSection` + `EnrollmentService.dashboard()` | its sections |
| Universe entities (forums, posts) | `EntityForumSpec` | its entities |

The enrollment journey: apply → automatic criteria → auto-accept /
motivated refusal / waiting queue → admin dashboard (pending ⏳ /
accepted ✅ / refused ❌) → admin accept/refuse with reasons →
`MembershipService.register` (season roles synced). The automatable
criteria: `min_elo`, `min_matches` (X matches / Y days / game Z),
`requires_profile`, plus `manual` to force human validation.

The full guided questionnaire (for novices and agents alike) lives in
the
[mod-intake](../../.agents/skills/mod-intake/SKILL.md) skill — a
session creating a mod starts there.

## See also

- [architecture/mods.md](../architecture/mods.md) — the system's
  design (registry, lifecycle, seams, contract)
- [MODS/README.md](../MODS/README.md) — the system on the docs side
- [MODS/CATALOGUE.md](../MODS/CATALOGUE.md) — every mod, maturity
- [GUIDES/mod-developer.md](mod-developer.md) — the developer guide
  (deeper: SDK, tests, core-evolution)
- [the mod-intake skill](../../.agents/skills/mod-intake/SKILL.md) —
  the guided questionnaire (a session's entry point)
