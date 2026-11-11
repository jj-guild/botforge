# Testing strategy

This page defines how BotForge is tested: the in-memory test doubles, the
test pyramid, and the rules that keep tests fast and hermetic.
`MockDiscord` is tracked by botforge-services#2 and the behavioral layer by
botforge-services#22 / #24; this page is the strategy all test work must
follow. It will be enriched with concrete examples as the code lands in
`botforge-services`.

## 1. Principle: no test touches the real Discord API

Discord is an external, rate-limited, hard-to-reproduce dependency. Every
test runs against in-process test doubles, at two complementary depths:

- **`MockDiscord`** (botforge-services#2) — mock *objects*: subclasses of
  the real discord.py classes (`MockInteraction`, `MockGuild`,
  `MockMessage`…) built from plain Python data. Ideal for adapters, UI
  builders and fast surgical unit tests; permissive by design (no
  permissions, no dispatch), so it never validates the *glue*.
- **SimCord** ([github.com/SilentHacks/simcord](https://github.com/SilentHacks/simcord),
  dev-dependency `simcord[pytest]`) — a *simulator*: it swaps discord.py's
  two seams (`HTTPClient.request` and `ConnectionState.parsers`) for an
  in-memory backend, so the **real bot runs unmodified** through the real
  command dispatch, converters, permission checks, interaction lifecycle,
  view timeouts (virtual clock) and Components V2 layouts.
- **In-memory MongoDB substitute** — same interface as the persistence
  layer, no server needed
- **In-memory Redis substitute** — same interface as `StateService`, TTLs
  simulated with a controllable clock

Real-API verification (token present, intents correct) runs in CI against a
**dedicated CI/CD bot** whose token lives in the `botforge-services` secret
`CICD_DISCORD_TOKEN` (botforge-services#34): the `Discord smoke` job boots
the real bot container, asserts the gateway-ready signal, and soaks it. The
job is **fail-closed** on the secret: when the token is not configured the
job fails with an explicit error — a missing CI/CD bot token is a broken CI
setup, never a silent skip. The developer provisions the secret so CI can
pass.

### Why both MockDiscord and SimCord

Mock objects confirm what the test assumes: a mocked response always
succeeds, a clicked button calls its callback directly, permissions are
skipped. That is exactly right for testing *our* conversion and builder
code, and exactly wrong for testing the discord.py glue (dispatch, checks,
acknowledgment rules). The behavioral layer must cross the real
machinery — this is the lesson of
[discord.py#197](https://github.com/Rapptz/discord.py/issues/197): mocks
bypass dispatch, so the glue stayed untestable until simulators existed.
SimCord's own guide for coding agents states the failure mode plainly: *an
agent can produce a plausible mock that confirms its own assumptions.*

## 2. Test pyramid

| Level | Scope | Runs on | Tools |
| ----- | ----- | ------- | ----- |
| Unit | Core services, models, pure functions (`ChannelService` resolution, workflow transitions) — zero Discord | Every push/PR | pytest |
| Unit (Discord objects) | Adapters (`to_core_user`…), UI builders, embed/layout construction | Every push/PR | pytest + `MockDiscord` mocks |
| Integration | Multi-component flows: `WorkflowEngine` + `ChannelService` + `StateService` + stores | Every push/PR | pytest |
| Behavioral (journeys) | Complete user journeys driven as a user: slash commands, buttons, selects, modals, permissions, timeouts, Components V2 | Every push/PR | pytest + SimCord (`simcord_env`) |
| Smoke (preflight) | Real container entrypoint: environment, MongoDB, Redis, locale catalogs — no Discord gateway | Every push/PR | GitHub Actions (`Bot preflight` step) |
| Smoke (real Discord) | Real bot container, real gateway connection via the dedicated CI/CD bot | Every push/PR to `main`; **fails** if `CICD_DISCORD_TOKEN` is missing | GitHub Actions (`Discord smoke`, botforge-services#34) |

Behavioral tests are the template for mod journeys
(`tests/integration/test_simcord_journeys.py` in `botforge-services`):
arrange the world with builders, act as a user through actors, assert on
observable state (responses, channel messages, roles).

## 3. MockDiscord (mock objects — botforge-services#2)

`tests/mocks/discord_mock.py` in `botforge-services` provides mock
*objects*: `MockInteraction` (with `MockResponse`/`MockFollowup` recorders),
`MockUser`, `MockMember`, `MockRole`, `MockGuild`, `MockMessage`,
`MockTextChannel`/`MockVoiceChannel`/`MockCategoryChannel`/`MockDMChannel`,
`MockClient`, `MockView`, `MockModal` and UI helpers. Every mock subclasses
the real discord.py class so `isinstance` checks hold, records message
history, and — per [ADR-0009](../DECISIONS/009-discord-components-v2.md) —
records **both UI surfaces**: embed-based (`.embeds` + `.components`) and
Components V2 (`.layout` + flattened `walk_children()` tree).

### Capabilities (contract for botforge-services#2)

- Channel creation/lookup by category, mirroring guild structure
- Role assignment and membership tracking
- DM and message capture (content, embeds, components) in inspectable
  history
- Interaction response/followup recording (sent, deferred, ephemeral)
- A controllable clock for TTL and workflow-timeout tests

### What MockDiscord must NOT do

- Test the discord.py glue (dispatch, checks, permissions, acknowledgment
  lifecycle) — that is SimCord's job
- Reimplement game logic or workflow semantics — it is a platform, not an
  oracle
- Share state between tests — each test builds a fresh instance
- Paper over adapter bugs: the Discord adapter and `MockDiscord` implement
  the same `IPlatform` interface; divergences found in production are
  reproduced as tests at the `IPlatform` level first

## 4. SimCord (behavioral simulator)

`simcord[pytest]` is a dev-dependency of `botforge-services`. The pytest
plugin provides the `simcord_env` fixture; each test class overrides the
`simcord_bot` fixture with the bot it drives (calibration bots today, the
real bot factory once botforge-services#12 lands).

### Rules for behavioral tests

- Drive the bot as a **user**: `alice.slash(channel, "register")`,
  `alice.click(message, custom_id=…)`, `alice.submit_modal(shown, …)` —
  never call a command callback directly
- Assert observable results: `result.response.content`, channel messages,
  roles assigned, `InteractionResult` flags (`ephemeral`, `acknowledged`)
- **No token, no network, no sleeps** — actors settle the event loop, and
  `env.advance_time(seconds)` fires view timeouts and cooldowns instantly
- Keep `strict_sync=True` (default) for journeys that mirror production:
  an unsynced slash command must fail the test; use
  `@pytest.mark.simcord(strict_sync=False)` only for calibration tests
- A `RouteNotImplemented` failure is a SimCord parity gap: report it
  upstream or extend the test to another level — never replace it with a
  silent fake
- Components on a received `Message` are **wire-model** components
  (`discord.components.*`, `TextDisplay.content`), not UI items
  (`discord.ui.*`, `TextDisplay.text`); assert on the wire classes

### What each layer tests

- **Core services** — state transitions, persistence round-trips,
  channel-resolution order, lock behavior, restart recovery
- **Adapters/UI (MockDiscord)** — conversions between platform objects and
  core models (`IMessage`, `IChannel`, `IUser`), embed/layout builders,
  dual-surface recording per ADR-0009
- **Mods/workflows (SimCord)** — journey outcomes: responses, final state
  in MongoDB, roles assigned, messages sent, permissions enforced,
  i18n of every user-facing string (English default, French available —
  [ADR-0008](../DECISIONS/008-i18n-system.md))
- **Config** — every YAML file parses and validates against its schema

## 5. Rules

1. Tests never sleep on wall-clock time; timeouts are tested with the
   controllable clock (`MockDiscord` clock, `env.advance_time` on SimCord)
2. One assertion focus per test; journeys are split into ordered test
   cases that rebuild state explicitly rather than depending on execution
   order
3. User-facing strings are asserted through locale keys or localized
   content, never raw hardcoded text
4. CI (lint, test) runs on every PR in `botforge-services` and
   `botforge-infra`; docs validation runs on every PR in this repo
5. **Anything the dev sandbox cannot run is validated by GitHub Actions
   instead**: Docker builds, Compose boots, stack healthchecks,
   backup/restore round-trips and entrypoint runs are CI jobs, not manual
   checks. When a new check cannot run locally, add or extend the workflow
   that validates it — never leave it unverified.
   (`.github/workflows/check-docs.yml`)
6. **The right double for the right depth**: mock objects (MockDiscord)
   for our conversion/builder code; the simulator (SimCord) for anything
   that depends on discord.py dispatch, checks, permissions or the
   interaction lifecycle; no `MagicMock` as a substitute for Discord
   permissions or cache state; no `bot.run()` in tests.
7. **A flow tested with a fake service is not tested — the seam must have
   its own test** (botforge-services#322): a fake accepts any signature
   and never refuses, so a flow journey over a fake service proves the
   flow, not the wiring. Every caller-to-remote seam (the gRPC clients,
   the remotes and proxies) is held by two tests of its own: a
   **signature contract** (what the client issues matches what the
   servicer implements — see
   `tests/architecture/test_rpc_seam_contracts.py` in `botforge-services`)
   and one **end-to-end seam test** (the real client → the real servicer
   over loopback gRPC, only the backing callables faked — see
   `tests/integration/test_rpc_seam_journeys.py`).

## See also

- [core.md](core.md) — core services design
- [mods.md](mods.md) — mod system design
- [discord.md](discord.md) — Discord platform guide
- [ADR-0001](../DECISIONS/001-multi-platform-architecture.md) —
  `IPlatform` abstraction, the seam that makes this strategy possible
- [ADR-0009](../DECISIONS/009-discord-components-v2.md) — dual Discord UI
  system, respected by both test doubles
- [SimCord — AI coding agents guide](https://simcord.readthedocs.io/en/latest/guides/ai-coding-agents/)
  — the agent workflow this strategy adopts
