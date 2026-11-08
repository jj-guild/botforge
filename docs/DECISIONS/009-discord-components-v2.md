# ADR-0009: Dual Discord UI system — embeds for simple output, Components V2 for rich UI

- **Status**: Accepted
- **Date**: 2026-09-20
- **Deciders**: developer
- **Reference**: botforge-services#13

## Context

Discord shipped **Components V2**, a new message layout system, supported by
discord.py since **2.6** (we pin `discord.py>=2.7.1` in botforge-services#1).
It replaces the `content` + `embeds` + action-rows model with composable
blocks: `ui.LayoutView` as the root, then `ui.Container`, `ui.Section`,
`ui.TextDisplay`, `ui.MediaGallery`, `ui.File`, `ui.Separator`,
`ui.Thumbnail`, with `ui.ActionRow` still holding buttons and selects.

The legacy system (`ui.View`, `embeds`, `content`) continues to work and is
**not** deprecated; both systems can coexist in the same bot, but **not in
the same message**.

Embeds are **not** legacy: they remain the right tool for sober, lightweight
informational messages (a result, a confirmation, a log line) where a
Container card would be visually heavy. Components V2 is the right tool for
rich, structured, interactive UI (panels, multi-block layouts, galleries).
The two are complements, chosen per message.

Key incompatibilities to avoid (per Discord's component reference and the
discord.py 2.6 changelog):

1. A message sent with the `IS_COMPONENTS_V2` flag **cannot** use the
   `content`, `embeds`, `stickers`, or `poll` fields. Text goes in
   `TextDisplay`, rich cards in `Container`. Passing both raises an error.
2. The flag is **per-message and permanent**: once a message is sent with it,
   the flag cannot be removed from that message. Edits must keep using V2.
3. Character limit: **4000 characters shared across all `TextDisplay`**
   components in one message (`LayoutView.content_length()` checks it).
   Mentions inside `TextDisplay` **do ping** — templates must not inject
   mentionable text into layouts unintentionally.
4. **40 components max** per message; `Section` accepts only `TextDisplay`
   children (max 3) and only a `Thumbnail` or `Button` accessory;
   `Thumbnail` only exists as a Section accessory; `MediaGallery` holds up to
   10 items; separators offer `divider` and `small`/`large` spacing only.
5. Attachments are **not previewed** by default; they must be surfaced via
   `MediaGallery`, `File`, or `Thumbnail`. URL auto-embeds are disabled.
6. discord.py specifics: persistent views registered with `bot.add_view`
   and `DynamicItem` custom-id templating work with `LayoutView` too, but
   iteration uses `walk_children()` (components nest deeply), and disabling
   items must walk that tree.

The UI layer (botforge-services#13) has not been implemented yet, so we are
choosing the system before writing the first component — the cheapest time
to decide.

## Decision

BotForge uses **both** systems, chosen per message by a simple rule the
game designer can apply:

- **Embed** (`discord.Embed`, optionally with a `ui.View` for buttons):
  sober, lightweight, static or minimally interactive output — a match
  result, a confirmation, a status update. First choice for read-mostly
  messages.
- **Components V2** (`discord.ui.LayoutView` + `Container`/`Section`/
  `TextDisplay`/galleries): rich, structured, interactive UI — panels,
  multi-block layouts, side-by-side text + accessory, media galleries.
  Required whenever the message needs more than an embed's flat
  title/description/fields shape.

Concretely:

- botforge-services#13 ships **both** `ui/embeds.py` (EmbedBuilder for
  consistent sober styling) **and** `ui/layouts.py` (LayoutView
  subclasses for rich cards), with the same shared patterns:
  `interaction_check`, `on_timeout` + `walk_children()` disabling,
  `on_error`, persistent registration via `bot.add_view`, and
  `DynamicItem` custom-id templating (`<mod>:<component>:<payload>`).
- Every user-facing string goes through the i18n system (ADR-0008).
  V2 messages must keep `LayoutView.content_length()` ≤ 4000 — the
  UI layer **should** assert this before sending.
- A message is **either** embed-based or Components V2, never both
  (Discord rejects `content`/`embeds` on a V2 message). The flag is
  permanent per message: choose before sending.
- `IPlatform` stays layout-agnostic: it sends "a message" (embed or
  components); `MockDiscord` (botforge-services#2) **must** record both
  embeds and the V2 component tree so journey tests can assert on either.
- Mod issues state which system each of their messages uses; when in
  doubt, start with an embed and upgrade to V2 only when the layout
  demands it.

## Alternatives Considered

- **V2 only, drop embeds** (previous draft of this ADR): maximal layout
  freedom, but forces heavy Container cards for trivial messages and
  discards the sober, familiar embed rendering the game designer wants.
  Rejected.
- **Embeds only**: simpler and universally supported, but cannot express
  the rich panels BotForge needs (sections with accessories, galleries,
  multi-block layouts). Rejected.
- **Wait for discord.py V2 API surface to stabilize further**: discord.py
  2.6/2.7 already ship the full component set (`LayoutView`, `Container`,
  `Section`, `TextDisplay`, `MediaGallery`, `File`, `Thumbnail`,
  `Separator`), and 2.7.x has the `walk_children` fixes we need. Waiting
  buys nothing. Rejected.

## Consequences

**Positive**

- Sober, light embeds for most messages; rich V2 layouts where they add
  value — no heavy cards for trivial output.
- Both patterns share one set of rules (custom IDs, persistence, checks),
  so mods behave consistently across systems.
- `MockDiscord` records both surfaces, so journey tests assert on exactly
  what users see.

**Negative / risks**

- Two rendering paths to know and test (embeds vs V2 tree); mitigated by
  the per-message decision rule above.
- Layouts must be designed within the 40-component and 4000-char limits;
  long content (e.g., ladder rankings) needs pagination.
- Mentions in `TextDisplay` ping: template rendering must escape or gate
  mentionable content.
- The flag is irreversible per message: templates must be right on first
  send; edits must re-send a full V2 layout.
- Fewer community examples for V2 than embeds; we document our own
  patterns in [architecture/discord.md](../architecture/discord.md).

## References

- Discord components reference: <https://docs.discord.com/developers/components/reference>
- discord.py changelog (Components V2, GH-10166):
  <https://discordpy.readthedocs.io/en/latest/whats_new.html>
- [architecture/discord.md](../architecture/discord.md) — updated patterns
- botforge-services#13 (UI components), botforge-services#2 (MockDiscord)
