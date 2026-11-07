---
name: discord-components
description: Build Discord components the right way (discord.py / Components V2) — each component (button, select, modal, Label, action row, emoji, timestamp), the wire traps that fail silently, and the patterns to follow. Generic and reusable in any bot project.
---

# Discord components — how to build, pitfalls, patterns

## How to build each component

- **Button** — `discord.ui.Button` with a stable `custom_id`; dispatch at click time. Register persistent views at bot setup so restarts keep the callbacks.
- **Select** — a select occupies a **whole action row**: never two selects in one row. Create the row **inside** the loop, one row per select — a row created before the loop and re-fed each iteration accumulates children and fails at render with `maximum number of children exceeded`.
- **Modal** — subclass `discord.ui.Modal` **and define `async def on_submit`**: a Modal without `on_submit` opens fine, then the submit dies with "interaction failed" and leaves zero logs. Cap: 5 top-level components per modal (a Label counts as one).
- **Label (type 18)** — wraps a select or a text input inside a modal: `discord.ui.Label(text=..., component=select)`. A **bare select in a modal is rejected** by the API (50035, `type must be one of (4,)`); the Label-wrapped one works. A TextInput label is capped at 45 characters. An optional select needs `required=False` + `min_values=0` (the API rejects `min_values=0` on a required component).
- **Emojis** — only API-validated symbols. Discord silently rejects unknown U+1F5xx symbols with 50035 (Invalid emoji) — one bad codepoint can kill buttons in production while the whole test suite stays green. Keep an allowlist and validate any new symbol live before adding it; a guard test should fail the build on unallowlisted 1F5xx codepoints.
- **Timestamps** — use the `<t:...>` mention format, never pre-formatted date strings.

## Wire traps (all fail silently)

- **The 3-second rule.** Discord invalidates an interaction ~3 s after it fires → `NotFound 10062 (Unknown interaction)`. Ack first (`defer()` or an in-place `edit_message`), do the slow work after, answer via followup.
- **One ack per interaction.** Never defer twice: the second raises `InteractionResponded` and the click dies silently. A dispatcher callback that delegates to sub-handlers must NOT defer if those handlers own their ack.
- **custom_id must match its own template.** A constant id against a template that expects a pattern raises `ValueError` at every rebuild — the control dies at first click, silently. Keep templates and emitted ids consistent; a test resolving the constants against the templates catches it at build time.
- **A silent failure with empty logs = the dispatch never happened.** The interaction never reached a callback: a modal nobody submits, an id nobody matches, a component nobody registered. Grep the dispatch path (modal `on_submit`, template vs custom_id, view registration) before suspecting backend services.
- **A modal submit refreshes the message it came from.** Capture `interaction.message` at the click, then `origin.edit(view=fresh)` at submit. Never send a second copy of the view; if the origin is gone, answer with plain text. Never edit a Components V2 message through `content` (50035) — edit through a View/container.
- **Never open a modal from a modal** — chain through an ephemeral message.

## Patterns to follow

- **Admin gating on public posts**: one visible ⚙️ button opens an ephemeral management view, checks the permission at click time, and greys out dangerous actions by state — dangerous buttons are never exposed on a public surface.
- **Pinned menus are static**: their buttons open ephemeral views for navigation; the pinned message is edited in place when content changes; clicking a pin answers with an ephemeral and never moves the pin.
- **Build-time guards**: a small architecture test suite fails the build on the trap shapes above (unallowlisted emoji codepoint, Modal subclass without `on_submit`, double-defer shape, more than one select per action row, custom_id/template mismatch).
