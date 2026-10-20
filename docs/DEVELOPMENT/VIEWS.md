# VIEWS — the map of menus and panels

> **Source of truth.** This document describes **every view** of the
> bot: its id, its kind, where it lives, and its buttons. The code
> mirrors this list exactly (`views_declared.py` in kingdoms-services):
> reorganizing means changing this doc **and** that file in the same
> PR. Agents read this doc before adding, moving or removing a view.

## The two kinds of views

| Kind | Role | Content |
| ---- | ---- | ------- |
| **menu** | Navigate | Buttons only — every button opens another view. No data, no actions. |
| **panel** | Inform / act | Data (lists, stats), actions, live content. |

Shared rules:

- every view carries an **id** (`menu:games:aoe2`, `panel:profile`)
  rendered as its **footer** — the anchor every human feedback refers
  to;
- an **admin** button carries the 🔒 emoji and the most discreet style
  Discord allows;
- a **sync** button (channels & roles) carries the ⚙️ emoji;
- labels resolve through the i18n catalog (key
  `ui.views.<id without :>.title`);
- **caps**: 20 maps / map pool · 20 active map pools / guild ·
  20 games · 20 mods.

## The map (today: 1 game — aoe2, 0 mod)

```text
menu:home ──┬─> panel:profile
            ├─> menu:games:home ──┬─> menu:games:aoe2 ──┬─> panel:game:aoe2:live
            │                    │                     ├─> panel:game:aoe2:players
            │                    │                     └─> menu:game:aoe2:admin
            │                    └─> menu:games:admin ──> menu:game:aoe2:admin
            ├─> menu:mods:home ──┬─> (menu:mod:ladder      — disabled)
            │                   ├─> (menu:mod:tournament — disabled)
            │                   ├─> (menu:mod:kingdom     — disabled)
            │                   └─> menu:mods:admin
            └─> menu:admin ──┬─> panel:status
                             ├─> menu:games:admin
                             ├─> menu:mods:admin
                             └─ [⚙️ sync]
```

## The views, one by one

### `menu:home` — pinned in `root/general`
The starting point.
- → `panel:profile` (👤)
- → `menu:games:home` (🎮)
- → `menu:mods:home` (🧩)
- → `menu:admin` (🔒)

### `panel:profile`
The player's profile (linked accounts, rename). *Unchanged.*

### `menu:admin` — pinned in `bot/admin`
- → `panel:status` (📊)
- → `menu:games:admin` (🔒)
- → `menu:mods:admin` (🔒)
- ⚙️ sync channels & roles

### `panel:status` — boot DM
The deployment status (version, uptime, services). *Unchanged.*

### `menu:games:home` — pinned in `games/general`
The list of available games — **one button per game, long label**
(the game's name, not its game key), plus admin.
- → `menu:games:aoe2` (⚔️ Age of Empires II)
- → `menu:games:admin` (🔒)

### `menu:games:admin` — pinned in `games/admin`
- → `menu:game:aoe2:admin` (🔒 per game)
- ⚙️ sync channels & roles

### `menu:games:aoe2` — pinned in `games/aoe2/general`
The game's name as the title, then:
- text: **the channels** (content, restrictions, forums)
- text: **the roles** (usage)
- → `panel:game:aoe2:live` (📡)
- → `panel:game:aoe2:players` (👥)
- → `menu:game:aoe2:admin` (🔒)

### `menu:game:aoe2:admin` — pinned in `games/aoe2/admin`
The same channels/roles sections as the game's menu, then:
- ⭐ Add a map
- 🧱 Create a map pool
- ⚙️ sync channels & roles

### `panel:game:aoe2:live` — pinned in `games/aoe2/live`
The live dashboard. *Unchanged.*

### `panel:game:aoe2:players`
The registered players **of that game** — one line each, no guild
name. Generic: `panel:game:<key>:players`.

### `menu:mods:home` — pinned in `mods/general`
The list of mods (empty today) — **one button per mod, long label**,
plus admin. The declared placeholders are disabled:
- (menu:mod:ladder — disabled)
- (menu:mod:tournament — disabled)
- (menu:mod:kingdom — disabled)
- → `menu:mods:admin` (🔒)

### `menu:mods:admin` — pinned in `mods/admin`
- (menu:mod:ladder:admin — disabled, 🔒)
- (menu:mod:tournament:admin — disabled, 🔒)
- (menu:mod:kingdom:admin — disabled, 🔒)
- ⚙️ sync channels & roles

## Adding or moving a view (the how-to)

1. **Declare**: `views_declared.py` — one `ViewDecl` (id, kind, pin
   scope, buttons with their targets). A menu only declares buttons
   pointing at declared views (or the sync flag);
2. **Document**: add the view here, in the map and its own section;
3. **Wire**: if the view opens a handler, `wire_view("<id>", handler)`
   in `_wire_declared_views` (factory) — otherwise nothing;
4. **Translate**: `ui.views.<id>.title` / `.description` in `fr.yaml`
   **and** `en.yaml`;
5. **Test**: the registry validates itself (`validate_registry`) — an
   undeclared target, a menu button without target/sync/label are
   drifts the tests reject.

A new game follows the same path: `menu:games:<key>`,
`menu:game:<key>:admin`, its panels — the declarative menu builder
renders the menu automatically from the declaration.
