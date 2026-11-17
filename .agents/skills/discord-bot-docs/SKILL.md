---
name: discord-bot-docs
description: Read and keep botforge-services' docs/DEVELOPMENT/DISCORD-BOT.md up to date whenever a Discord surface changes — views, pinned panels, menus, components, ids, i18n, providers. The doc is hand-maintained: agents update it on every surface change.
---

# Discord bot documentation

`docs/DEVELOPMENT/DISCORD-BOT.md` **in the botforge-services repo** is
the reference for every Discord surface of the bot. It is
**hand-maintained**: no generator writes it, so it drifts silently
unless sessions update it.

## When a session MUST read it

Before touching any file under `src/botforge/discord/` in
botforge-services (views, panels, flows, pinned menus, forums, i18n)
— the doc states the current rules (pin immutability, view origin,
guild context, ids, i18n) and the file map; they constrain every
change.

## When a session MUST update it

After every change to a Discord surface (a new view, a renamed
panel, a moved pin, an id-grammar change, an i18n shift): update the
doc in the SAME PR — a surface change that drifts the doc is an
incomplete change.
