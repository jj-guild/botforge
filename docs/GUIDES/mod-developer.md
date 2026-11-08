# Guide — Mod developer (human or AI)

Build a new mod (a game feature: register, ladder, clans, …) on the
BotForge core. If you are an AI session, read [vibe-coder.md](vibe-coder.md)
first for the session mechanics; this page is the technical map.

## What a mod is

A self-contained feature that declares its configuration in YAML and
implements its logic against the generic core — never against a
specific platform or game. See [MODS/README.md](../MODS/README.md) for
the mod system, lifecycle and composition rules.

## The non-negotiables

1. **Platform-agnostic core**: no discord.py imports in mod domain
   code. The mod core emits abstract actions and notification intents;
   the Discord surface (in `bot-discord`) renders them. No Discord IDs
   in the mod's MongoDB collections ([ADR-0011](../DECISIONS/011-protocol-interfaces.md)).
2. **Game-agnostic where the game is pluggable**: the mod core knows
   `game_key` and opaque strings only; everything game-specific comes
   from the provider seam.
3. **No cross-domain state**: the mod's durable state lives in its own
   collections ([ADR-0019](../DECISIONS/019-modular-monolith-extraction-contracts.md) rules).
4. **i18n-first**: every user-facing string resolves through the shared
   catalog from the first PR — no hardcoded text.
5. **Admin surface is Discord-first**: everything an admin manages
   (settings, game data, seasons) is manageable from Discord; requiring
   a dev action is a design bug.
6. **Tests land with the code** (acceptance properties in CI, mocked
   seams — see [testing strategy](../architecture/testing.md)).

## Anatomy (where things live)

| Piece | Location (botforge-services) |
|---|---|
| Domain core | `src/botforge/mods/<mod>/` (in svc-core, ADR-0020) |
| Discord surface (views, modals, intents) | `src/botforge/discord/…` surface in bot-discord |
| Config | `config/mods/<mod>.yaml` (channels, roles, settings template) |
| Rules & environment docs | `botforge` repo: `docs/MODS/<mod>/` (copy [TEMPLATE](../MODS/TEMPLATE/)) |
| Contracts (if the mod adds a cross-process seam) | `contracts/` + `make contracts` ([ADR-0020](../DECISIONS/020-process-split-bot-core-providers.md)) |

## Step-by-step

1. **Design**: write `docs/MODS/<mod>/` (README, RULES, ENVIRONMENT)
   from the template; get the game designer's agreement on rules.
2. **Declare**: `config/mods/<mod>.yaml` — channels and roles via
   `ModRegistry` logical keys, never raw IDs.
3. **Domain**: models + services against core seams
   (`WorkflowEngine`, `ChannelService`, `StateService`); typed errors
   from the exception taxonomy; idempotent provisioning.
4. **Surface**: views/modals through the UI SDK (never raw
   `discord.ui`); custom IDs `<mod>:<component>:<payload>`; runtime
   permission guards on every privileged item; 3-second rule
   (defer, then followup) on every interaction.
5. **Background tasks**: periodic work lives in the owning process with
   Redis locks; document cadence in ENVIRONMENT.md.
6. **Tests**: unit (no Discord), MockDiscord/SimCord for the surface,
   acceptance properties for the rules ([#139 mandate](https://github.com/jj-guild/botforge-services/issues/139)).
7. **Docs**: update `docs/MODS/<mod>/` and the botforge repo docs in
   the same PR — a mod without documentation is not done.

## Worked example

The ladder mod is the reference implementation:
[docs/MODS/ladder](../MODS/ladder/README.md) (seasons, pluggable rating,
queue+invites, Discord-first admin surface).

## Review gate

The developer reviews every PR ([VIBEWORKFLOW](../VIBEWORKFLOW.md)).
Expect: architecture rules above, tests, docs freshness, i18n, and a
demo of the admin surface in Discord on the test environment.
