---
name: discord-ui
description: Build any Discord message, view, embed or Components V2 layout through the kingdoms-services UI SDK, never discord.ui directly. Use whenever a session builds, reviews or refactors a bot message, button, select menu, ranking, config panel or any user-facing Discord UI.
---

# Discord UI (the SDK rules)

Every user-facing Discord message of the platform is built through the
UI SDK in `kingdoms-services` — `src/kingdoms/discord/ui/`
(`factory.py` for the bricks and builders, `screens.py` for the
archetypes). No feature instantiates `discord.ui` / `discord.Embed`
classes directly: the SDK is the single place where the Discord layout
rules are enforced, at build time, with a clear `UILayoutError` —
before anything is sent.

## The bricks

Two builders cover the ADR-0009 dual system:

- `UIEmbed` — light informational output (`.field()`, `.footer()`,
  `.build()`), where markdown links and line breaks **do** render
  (classic embed fields).
- `UILayout` — rich Components V2 output, composed of `Container`,
  `Section`, `Text`, `Row`, `Button`, `Separator`, `Thumbnail`,
  `Action` (interactive button), `SelectMenu` (interactive select).

```python
from kingdoms.discord.ui import UILayout, Container, Section, Text, Row, Button, Separator

view = (
    UILayout()
    .add(
        Container(accent=BLURPLE)
        .add(Text("# 🚀 Title\n-# `badge`"))
        .add(Section(Text("**Services**"), button=Button("PR", url)))
        .add(Separator())
        .add(Row(Button("Pipeline", run_url), Button("Image", pkg_url)))
    )
    .build()
)
```

## Navigation is buttons, not links (the V2 text rule)

In Components V2 text blocks — and **worst in sub-texts / footers
(`-# …`) — links and line breaks do not render reliably**. The rule:

- text blocks carry **plain labels, code spans and timestamps only**
  (`<t:…:R>`);
- **every link is a link button in an action row**
  (`Row(Button(label, url), …)`);
- a section layout follows the announcement pattern:

  ```
  **Services**
  [Branch] [Pull-request]        ← action row
  PR title                       ← plain text
  `sha7`                         ← plain text
  [Commit] [Files]               ← action row
  <t:…:R>                        ← timestamp
  [🚦 Pipeline] [📦 Image]       ← action row
  ```

- embeds (`UIEmbed`) are the exception: markdown links render there
  (e.g. the `/status` embed keeps its `[label](url)` lines).

## Times are Discord timestamps, never formatted strings

Never render a user-facing time as a formatted string with an explicit
or implicit timezone — always send a Unix epoch and let Discord format
it with `<t:…:F>` (full date-time), `<t:…:R>` (relative) or the other
`<t:…>` styles. Discord localizes the display **per viewer**, so:

- a per-guild or per-mod "timezone setting" is **not needed** for
  displaying times — a panel that offers one for display purposes is a
  bug;
- a stored reference timezone is justified only when the platform
  computes on wall-clock boundaries ("Sunday 23:30", "24h shield") —
  and then it is a **core guild setting** (see CONVENTIONS.md, *Guild-
  level settings and the admin surface*), never a mod setting;
- compute the epoch from the stored instant and format nothing: the
  viewer's Discord client does the rest.

## Interactive items

- `Action(label, custom_id, on_click, style=…, disabled=False)` — button
  with an async callback. The custom_id **must** follow
  `<mod>:<component>:<payload>` (e.g. `admin:ping:`, `ranking:page:next`);
  the convention is enforced at build time.
- `SelectMenu(custom_id, options, on_choose, …)` — the callback
  receives `(interaction, chosen_values)`; no digging through
  `interaction.data` in feature code.
- `Row` holds 1–5 items; a `SelectMenu` sits alone in its row.
- `disabled=True` renders the button greyed out — for the steps that
  exist in the design but not yet in the code; a disabled button never
  wires its callback.

## Modals (the Label rule and the interaction contract)

**A select inside a modal MUST be wrapped in a Label component; a TextInput
must NOT be.** Two rules, both learned the hard way:

1. **Selects ride a Label** (type 18): `modal.add_item(discord.ui.Label(
   text="…", component=select))`. A bare `modal.add_item(select)` is
   **silently rejected** by the API — the opening button seems dead.
2. **TextInputs stay naked** (the repo's proven ActionRow pattern):
   `modal.add_item(TextInput(label="…"))`. Wrapping a TextInput in a
   Label is NOT supported by discord.py 2.7's serializer (the deprecated
   inner `label` leaks into the payload and Discord rejects the modal —
   the 2026-10-15 regression: the add modal stopped opening). The Label's
   text is capped at 45 chars, its description at 100.

Both are guarded by `tests/architecture/test_modal_constraints.py`
(runtime scan of every modal, payload shape + limits check, source scan)
— never bypass it.

Other modal rules, learned the hard way:

- **`send_modal` needs the interaction's response token** — it cannot ride a
  deferred interaction. Any read before `send_modal` (options, prefill) must
  be fast (wrap it in `asyncio.wait_for(..., timeout=2.5)` with a fallback)
  or the click exceeds the 3-second window and dies silently.
- **`on_submit` defers first** — a modal's submit is a fresh interaction: the
  provider/database writes happen after `defer(ephemeral=True, thinking=True)`,
  the answer rides the followup.
- **Select values are read at submit time** — `Modal._refresh` populates
  `select.values` from the payload; the select is found by `custom_id` through
  `walk_children()` (Label wrappers are descended into). Set a stable
  `custom_id` on every modal select.
- **A modal never opens another modal** — the chain passes through an
  ephemeral message.
- **Modals are capped at 5 top-level components** (Label counts as one).

## Session lessons (2026-10-17, the Discord wire traps)

Everything below cost a deploy cycle to find — never reintroduce:

- **Component emojis come from an API-validated allowlist.** Discord
  rejects U+1F5xx symbols outside its set with a silent 50035 (Invalid
  emoji) — U+1F5F2 killed two admin buttons in production while the whole
  test suite stayed green. The guard
  `tests/architecture/test_component_guards.py` fails the build on any
  unallowlisted 1F5xx codepoint: validate a new symbol live before
  adding it.
- **One ack per interaction.** A DynamicItem callback that dispatches to
  a `_handle_*` (admin_persistent) must NOT defer first — those
  handlers own their acknowledgment; deferring twice raises
  InteractionResponded and the click dies silently (the Roles bug). The
  same guard fails the build on the double-defer shape.
- **A modal is nothing without `on_submit`** (2026-10-17 language bug).
  A `discord.ui.Modal` subclass without `async def on_submit` opens
  fine, then the submit dies with "interaction failed" and **leaves
  zero logs** — the whole suite stays green and even `/logs` shows
  nothing. Every Modal must define `on_submit`; the guard
  (`test_component_guards.py::test_modals_define_on_submit`) fails the
  build on a Modal subclass without it.
- **One select per action row — and a fresh row per loop iteration.**
  A Discord Select occupies a whole action row; two in one row raise
  `maximum number of children exceeded` at render time. The sneaky
  shape: the row created **before** a loop while the loop `add_item`s a
  select into it — every iteration re-feeds the same row object. Create
  the row inside the loop, one row per select. The guard
  (`test_action_rows_hold_one_select`) fails the build on both shapes.
- **A silent failure with empty logs is a dispatch that never happened.**
  When a click "does nothing" and `/logs` shows nothing, the
  interaction never reached a callback: a modal nobody submits, an id
  nobody matches, a component nobody registered. Grep the dispatch path
  (modal `on_submit`, DynamicItem template vs custom_id,
  `add_dynamic_items` registration) before suspecting the services.

## The 3-second rule (defer, then followup)

**Discord invalidates an interaction ~3 seconds after it fires.** A
command or a component callback that answers later than that gets
`NotFound 10062 (Unknown interaction)` — the user sees "This interaction
failed" and the crash reporter gets noise. Reading a database, calling an
external service or building a heavy layout routinely exceeds 3s.

Rules:

- the first await on a command path is **always**
  `interaction.response.defer(ephemeral=...)` (or an immediate
  `send_message` when nothing precedes the answer); the real answer then
  rides `interaction.followup.send(...)`;
- a deferred interaction stays answerable for **15 minutes** — the
  followup owns the slow reads;
- component callbacks re-rendering after a service read follow the same
  pattern: defer, read, `followup.edit_message(...)` / `edit_message`;
- **no slow call before the defer** — the defer is the very first
  statement, before any `await` on a service or database;
- an expired interaction (NotFound / HTTP 403-404 on the answer) is
  classified benign (`is_benign_interaction_error`): a warning log line,
  never a full crash report;
- every command test asserts `result.deferred` (simcord) or
  `interaction.response.deferred` (discord_mock) so a regression fails
  CI, not the users.

## Long-running actions: announce, then report at the same place

**A task that runs past a few seconds (an external API paced by its
terms, a bulk operation, a heavy aggregation) never leaves the user
staring at a dead button.** The moment the work starts, the user gets a
message saying WHAT is running, that it is in progress, and that the
result will be posted **in that very message**. When the work ends,
that same message is edited into the result — never a second,
unrelated message.

The canonical shape (three steps, in order):

```python
await interaction.response.defer(ephemeral=True, thinking=True)
progress = await interaction.followup.send("... running, the result will be posted here", ephemeral=True)
result = await the_slow_thing(...)                       # minutes are fine
await interaction.followup.edit_message(progress.id, content=the_result_or_failure)
```

Rules:

- the progress message names **what runs** and the **pacing reason**
  ("Liquipedia is queried at its own pace — this can take minutes"),
  so the wait is understood, not resented;
- **every exit path edits the progress message** — success, failure,
  and the "nothing to do" cases; the promise "the result lands here"
  is never broken;
- a click that can double-run the same slow work carries a
  **process-wide cooldown** (e.g. 5 minutes): the second click answers
  ephemerally with when it may retry, and never queues a duplicate run;
- live per-item progress (a bulk import editing its message per line)
  is the same pattern applied repeatedly — `edit_message` on the same
  id, one message end to end.

Reference implementations: `MapsSyncButton.callback` and
`GamesBulkImportModal.on_submit` (`kingdoms-services`,
`src/kingdoms/discord/admin_dm_panel.py` / `admin_panel_games.py`).

## Runtime permission checks (the click-time mandate)

**Never assume that seeing a button means being allowed to click it.**
Discord components are visible to whoever can read the channel —
permissions drift, role removals and channel moves happen between
render and click. Rules:

- every interactive item behind a privilege validates the interaction
  **at click time**, through the shared guards
  (`kingdoms.discord.guards`: `require_admin` / `is_admin`);
- the admin identity is: `BOT_ADMINS` (env-sourced operators), guild
  administrators (live Discord permissions), or the `bot-admins` guild
  role (resolved live through the RolesService, cache-aside Redis);
- `@app_commands.default_permissions(administrator=True)` only **hides**
  the command entry in the client UI — it never replaces the runtime
  check;
- a denial is answered ephemerally with the reason, and the callback
  returns immediately;
- the guard is the one place the check lives: a feature never
  re-implements it, never caches its result across clicks.

## The admin surface (transparency rule)

Admin messages with actions live in the guild's `🛡-bot-admins`
channel — never scattered in gameplay channels, never ephemeral-only:

- the channel is provisioned by the AdminChannelService (cache-aside:
  Redis → Mongo → adoption → creation), visible to the `bot-admins`
  role, guild administrators and the bot only;
- the BOT_ADMINS are synced **into** the role — the operator roster is
  public knowledge, and the role is its visible form;
- privileges never depend on the role: the guards check `BOT_ADMINS`
  first (environment-sourced, impossible to strip from Discord);
  removing the role costs the visibility, not the rights;
- the sync is one-way (add, never remove) and re-applied at every
  channel resolution — a manual un-sync never survives.

**One admin surface, extended at runtime.** The pinned bot-admins panel
is the platform's single admin surface. A mod never builds its own
admin panel, settings channel or guild-level pickers (locale, timezone):

- generic, mod-independent settings (locale, reference timezone, managed
  channels) are **core guild settings** — a mod that re-declares one
  duplicates the value by definition (one guild, one value);
- a mod's admin needs enter the **pinned panel through the core's
  runtime extension seam**: each enabled mod registers its admin section
  (label, entry point) and the panel renders them dynamically. If the
  seam is missing, **fix the core seam** — never fork the panel
  (CONVENTIONS.md, *Guild-level settings and the admin surface*);
- mod-specific tunables (gameplay constants) stay in the mod YAML
  `settings:` — data admin-overridable through the core surface, not a
  new UI.

## Screen archetypes (`screens.py`)

Prefer a ready-made shape over raw composition:

- `render_ranking(Ranking(title, entries))` — paged leader board
  (podium on page 1); the Prev/Next actions **edit the message in
  place** (UPDATE_MESSAGE), never repost.
- `build_config_panel(title, settings, mod=…, on_apply=…, on_reset=…)` —
  one `SelectMenu` per setting + Apply/Reset actions.
- `build_match_report(title, summary, details, mod=…)` — structured
  report with optional links and thumbnail.
- `PaginatedScreen(pages, mod=…, title=…)` — generic pagination when
  an archetype does not fit.

## Build-time guarantees (why the SDK exists)

The SDK rejects, with a clear `UILayoutError` before anything is sent:

- the 4000-character shared TextDisplay budget (V2) and the embed
  character budget;
- the 40-component cap;
- a `Section` without exactly one accessory (`button=` or
  `thumbnail=`), or with more than 3 text blocks;
- a `Row` with more than 5 items, or a misplaced `SelectMenu`;
- a `custom_id` that breaks the `<mod>:<component>:<payload>`
  convention.

## The V2 wire rule (no `content` on a LayoutView message)

A Components V2 message **cannot carry `content`, `embeds`, `stickers`
or `poll`** — Discord rejects the request outright (SimCord mirrors
this with `ComponentValidationError`). The rule:

- **every visible text lives in a `Text` block of the layout**, never
  in the `send_message(content=...)` argument — sending
  `content="Clan recruitment"` + `view=LayoutView` raises a 400 at send
  time, not at build time, so the SDK cannot catch it;
- the panel title is therefore a `Text("# …")` block, and a journey
  that needs body text adds it as the first block of the container;
- the only acceptable `send_message` shape for V2 is
  `send_message(view=layout_view)` — no `content`, no `embeds`;
- embeds (`UIEmbed`) are the reverse: they ride `embeds=`, never a
  `LayoutView`.

## Testing

- Unit: assert on the serialized wire (`view.to_components()`), with
  `simcord.components.validate_components` for full validation.
- Behavioral: SimCord journeys drive the real dispatch — click the
  buttons (`alice.click(message, custom_id=…)`), read the message back
  (`channel.last_message`) and assert on observable state; pagination
  must edit the message in place (same message id).

## Procedure

1. Reach for an archetype first (`screens.py`); compose factory bricks
   only when no archetype fits — and if the composition recurs,
   propose a new archetype.
2. Build through `UILayout` / `UIEmbed` only; never touch
   `discord.ui` classes in feature code.
3. Keep text blocks navigation-free (labels, code spans, timestamps);
   links ride in action rows.
4. Localize labels through the i18n catalogs (`config/locales/`),
   never hardcoded.
5. Assert the wire structure in tests (`to_components()`), and the
   click journey in SimCord for anything interactive.
6. Guard every privileged callback at click time
   (`require_admin(interaction, bot_admins, roles_service)`) —
   visibility is never authorization.

## Localization (one catalog, every surface)

Every user-facing string renders through the shared `MessageCatalog`
(`config/locales/<locale>.yaml`, one top-level section per surface).
Slash command names/description go through `locale_str` markers plus
the `CatalogTranslator` (`kingdoms.discord.commands_i18n`) — the yaml
`commands.<name>_name` / `commands.<name>_description` keys are the
only source; never a hardcoded localization dict.

The locale resolution rules (native Discord, nothing stored):

- **ephemeral / interaction surfaces** — the **clicker's client
  language first** (`interaction.locale`), then the server's language
  when the client speaks one the catalog does not carry — resolved
  through `kingdoms.discord.locales.interaction_locale`. A French
  client sees French even on an English server, exactly like Discord
  localizes slash commands;
- **pinned / public messages** (panels, announcements, lifecycle
  events) — the server's own language, `guild.preferred_locale`
  (Server Settings → Language), resolved through `guild_locale` /
  `guild_locale_by_id`: one public message, one language;
- **DMs** — the user's client language, `interaction.locale` (again
  through the seam); DMs follow the user, not a guild;
- **command entries** — the Discord client locale, through the
  translator, not the guild's.

The platform stores the language (the admin picker for the guild,
the DM picker for the user) and **the stored choice wins** over every
Discord signal — Discord's own surfaces have hard limits:

- a **Community server** carries a real language setting
  (`preferred_locale`, Server Settings → Language) — the guild
  surfaces follow it;
- a **non-Community server** has NO language setting: Discord
  hard-codes `en-US`. The guild surfaces fall back to the **majority
  of the members' observed client languages** (every interaction
  records the clicker's client language per guild —
  `observe_guild_member_locale` / `observed_guild_locale`);
- a **user's** language exists only inside interactions: the bot
  observes it per user (DMs render in the last-seen language) and
  per guild (the majority fallback above).

A guild that never picked falls back to Discord's signal, then the
members' observed majority; a user who never picked falls back to
their last observed client language. The pickers live in menu:admin
(set-language action) and the DM panel's language opener.

Adding a screen or message, the checklist (never skip the sweep):

1. every visible string — labels, hints, placeholders, button labels,
   select options, section titles — resolves through the catalog:
   add the keys to **both** `en.yaml` and `fr.yaml` in the same change;
2. sweep the touched module for hardcoded strings that escaped
   previous passes (`grep` the literals) — a "Visibility" left in
   English in a French panel is the classic regression;
3. render through `MessageCatalog.render`/`section` with the resolved
   locale — never parse a yaml file from a feature module (one loader);
4. the parity test: `section()` fills missing locale keys with
   English, and a new key in one locale only is a bug — keep the
   key sets identical.

## Menus, panels and the views registry

Every view is **declared once** in `config/views.yaml`
(kingdoms-services) — the single source of truth the runtime menu
builder, the pins and the button router consume, and from which
docs/DEVELOPMENT/VIEWS.md is generated
(`scripts/generate_views_doc.py` — regenerate it in the same change).
YAML anchors and aliases keep the repetition out. Navigation buttons
declare their target; complex behaviors declare an action id the code
wires at boot (`wire_action`) — an unwired action renders disabled.

**A mod declares its own views in its own config**
(`config/mods/<mod>.views.yaml`); the registry merges them with the
platform's. A mod's files never scatter across the repo — its
declaration, views, code and locales live together (kingdoms#179,
the modular-layout rule): never add a mod's i18n keys to the shared
`config/locales/`, never add its views to the platform's YAML. Two kinds:

- a **menu** navigates — buttons only, each opening another view;
- a **panel** informs or acts — data, actions, live content.

The rules the registry enforces (the tests reject the drifts):

- a menu button opens a **declared** view (`view:open:<view id>` on
  the wire — the ViewOpenButton router), or carries the sync flag;
- an admin button renders with 🔒, as discreet as Discord allows;
- a sync button renders with 🔄 (the TreeEnsureButton: re-provision
  the scope's channels and roles);
- **the universal home rule** (registry-enforced): a menu pinned in
  a scope's `general` explains its scope (the channel notice renders
  from the declared tree — links, access bands), navigates, and
  reaches the admin surface. The same contract for every game and
  mod to come;
- every view carries its id as its `-#` footer;
- the platform caps: 20 maps/pool, 20 active pools/guild, 20 games,
  20 mods.

Adding or reorganizing views: read docs/DEVELOPMENT/VIEWS.md first,
then declare, wire (`wire_view`), translate both locales, and keep
the doc and `views_declared.py` in the same PR — the doc is the
source of truth, the code is its executable mirror.

## Views organization (adding a screen)

- one module per surface in `kingdoms/discord/` (admin.py, status.py…):
  the builders, the callbacks and the command registration together;
- the layout composition lives in `ui/screens.py` when the shape is
  reusable (an archetype), in the surface module when it is not;
- custom IDs keep the `<mod>:<component>:<payload>` convention (the
  mod is the surface: `admin:`, `status:`, …);
- labels and urls: prefer an emoji + a short generic label on buttons
  (🔍 Files, 📦 Image, 🌿 Branch); the full values (sha, tags, ids) ride
  the text blocks next to the buttons, timestamps render as Discord
  relative times (`<t:…:R>`);
- **every view carries its view id as its footer** — a small `-#`
  line with the id in backticks (`view:aoe2:admin`), built through
  `kingdoms.core.ids.footer` (or `MenuSpec.view_id` on the menu
  template). The id is the anchor every human feedback refers to:
  "the Create button on `view:games:pools:manage` is broken" — no
  view ships without one.

## Proactivity mandate (know the whole discord.py surface)

The game designer and the developer are **not always aware of what
Discord offers**. The session is the expert of the platform surface:
it must know everything available in discord.py (verified against the
installed version), **propose** features that use it when relevant,
and document what exists before documenting how to use it. When a
game-design idea maps to a native Discord capability, propose it
first — a native feature costs less and behaves better than a
hand-rolled one.

Rule: at the start of any UI/feature design discussion, sweep this
inventory for what fits; mention the candidates to the designer even
when unasked. New capabilities discovered mid-session are added here
(announce the memorization to the user — they can veto it).

## Untapped capabilities inventory (discord.py 2.7.1, verified)

Capabilities available but not yet used by the platform. Each becomes
a "How to use" section the day a feature needs it:

- **Polls** — `discord.Poll(question, duration=timedelta, multiple=…)`
  with `.add_answer(text=…, emoji=…)`, sent via `Message.poll` /
  `send(poll=…)`; `Message.end_poll()` closes it; results via
  `PollAnswer.voters` fetch. Native multi-choice votes (map pools,
  rule votes, MVP elections) — no hand-rolled reaction counting.
- **Threads** — public/private/archived, `TextChannel.create_thread`,
  `Message.create_thread(name, auto_archive_duration=…)`,
  `Thread.add_member`/`remove_member`, slowmode per thread.
  Per-match or per-tournament discussion spaces without channel
  sprawl; `per_instance` mod channels can be threads.
- **Forum channels** — `ForumChannel.create_thread` with tags
  (`ForumTag`), required tags, layout. Clan recruitment boards,
  tournament announcements, report queues with categories.
- **Scheduled events** — `Guild.create_scheduled_event`
  (stage/voice/external, start/end times, image, recurrence via
  the API), subscribers listing. Tournament sessions, match
  schedules, season openings with native RSVP + reminders.
- **Voice / stage** — `Guild.create_voice_channel`, `create_stage_channel`,
  `Member.move_to`, mute/deafen, `VoiceChannel.connect` (the bot can
  speak). Tournament casting stages, team voice pickups.
- **Webhooks** — `Webhook`/`PartialWebhook` follow (channels can
  relay), `TextChannel.create_webhook(name, avatar)` posting with a
  custom identity per message. Match feeds posting as "AOE2 Bot",
  clan channels posting as the clan.
- **AutoMod** — `AutoModRule` (block/flag/timeout on keyword/mention/
  spam patterns, per-channel/rule exemptions). Tournament channel
  anti-spam without custom message scanning.
- **Reactions** — `Message.add_reaction`, `Reaction.users`, reaction
  removal; cheap RSVP/interest markers where a poll is overkill.
- **Guild membership screening / onboarding** — `Guild.onboarding`
  (prompts, default channels/roles), `membership_screening` fields.
  Newcomer routing to the registration flow.
- **Message attributes** — pinning (`pin()`), crossposting
  (`Message.publish` in announcement channels), `Message.edit`
  (component refresh in place), bulk delete (`purge`).

Anything missing from this list that a session uses must be added
here in the same change (the sweep is a loop, not a one-shot).
