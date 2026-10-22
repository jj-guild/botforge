# Channels, pinned views and admin surfaces

This page documents the **runtime conventions** learned while building
the first mods: how salons are resolved, how pinned views behave, and
what admin surface each mod type gets. These are enforced by review —
treat them as law.

## 1. Channels are resolved by stored id, never by name

- Every salon/category the bot provisions is recorded in the **channels
  Mongo registry** under a logical key (e.g. `ladder:home:<season>`,
  `mod:<mod>:admin`), together with its Discord **id**.
- Resolution at runtime uses the **stored id** only. Names are labels
  used on first creation; a human renaming a salon in Discord must
  never break the bot.
- The registry heals **on demand**: the boot pass provisions a virgin
  guild, and the sync button ("Synchroniser") re-provisions anything
  missing afterwards (salon deleted, message unpinned, post deleted).
  While an entity exists in the database and is not disabled, its
  salon/pinned message comes back at the next sync — nothing watches
  Discord in real time, nothing runs in a loop.
- Forum posts work the same way: the message id of each map post (or
  pool post) is stored so the flow can link back to the exact post.

## 2. Pinned views contract

- **Pins never move.** Clicking a pinned menu answers with an
  **ephemeral view**; the pinned message itself is edited in place when
  its content changes.
- **Auto-refresh.** When an input changes (a parameter, the guild
  locale, a season state), the surface calls the pin-refresher registry
  (`pinned_views.refresh_registered_pins`) so every registered pin is
  rebuilt with fresh data.
- **Read-only by default.** Pinned salons are locked (`send_messages`
  denied for @everyone, the bot keeps writing through its own
  overwrite). The bot-admin panel exposes a per-category read-only
  toggle; mods expose theirs through the same seam.

## 3. Mod types are mandatory

Every mod declaration (`kingdoms-services/config/mods/<mod>.yaml`)
must state its type:

```yaml
seasonal: true   # or false — mandatory, registry fails startup without it
```

Two mod types, two admin surfaces (single `ModAdminChannelSpec`
registration in core):

| Type | Admin surface | Where |
| ---- | ------------- | ----- |
| `seasonal: true` | Root lifecycle panel (create/activate/end seasons, enrollments) + a pinned **season admin salon** per season | Root admin channel at the guild root; per-season salon inside the season category |
| `seasonal: false` | Config panel carrying the mod's guild-level settings | Admin channel **inside the mod's guild category** |

Admin salons are **admins-only by default**; all other salons are
public. Visibility is recomputed on sync, so a perm drift is repaired on
the next pass.

## 4. Core/mods split rule

**Mod code stays minimal.** Anything a second mod could reuse lives in
core:

- shared wiring seams (game-data service builder, admin guard,
  guild-category resolution) — `kingdoms.discord.wiring`
- maps / map pools / per-game maps forum / per-pool pool forums
- seasons provisioning (roles + salons created at season creation)
- the mod admin channel mechanism, pinned menus, read-only policy,
  roles panel
- categories, channels registry, i18n catalog

A mod file should read like a **spec declaration** plus thin builders
wired into the generic machinery (see `ladder_admin_channel.py` for the
reference pattern). When reviewing mod code: any duplicated UI
component or workflow filler is a factorization bug.

## See also

- [mods.md](mods.md) — mod system design and the mod contract
- [discord.md](discord.md) — the Discord implementation layer
- [ADR-0008](../DECISIONS/008-i18n-system.md) — i18n (every user-facing
  string, per guild, with pin resync on locale change)

## 5. Ephemeral views contract

- **An ephemeral view never sends a copy of itself — even after a modal
  submit.** The only valid shapes: (1) a component click answers
  `interaction.response.edit_message(...)`; (2) a modal submit edits the
  message its opening button CAPTURED (`origin = interaction.message` at
  the click, `origin.edit(view=fresh)` at the submit — the
  `_profile_followup` pattern); the first-ever render sends the one
  message. When the captured origin is gone, the fallback is a PLAIN
  TEXT answer — never a new copy of the view.
- **A modal's submit REFRESHES the view it came from** (the submit
  changes what the view displays — re-render it with the fresh data,
  the `_profile_followup` shape). And a components-v2 message is
  edited through a VIEW, never through `content` (the API rejects
  `content` on a v2 edit — 50035); the answer text rides a container
  (`_text_answer`).
- **An ephemeral view is never replaced by another view.** The update
  re-renders the same logical view with fresh data; navigating to a
  genuinely different view opens it in its own message, and the previous
  one is never duplicated to do so.
- The ack always lands before any slow work (forum syncs, provider
  fetches): `defer()` or the in-place edit first, the slow cascade
  after — a modal's 3-second window is a hard failure otherwise.
- A select rides a modal **wrapped in a Label**
  (`discord.ui.Label(text=..., component=select)`) — never bare: the
  API rejects a bare select in a modal (50035 `type must be one of
  (4,)`), the Label-wrapped one works (the same shape as the profile's
  add-account form). A `TextInput` label is capped at **45 characters**.
