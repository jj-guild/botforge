---
name: discord-panels
description: Add a pinned menu, a scope folder (game/mod), or a channel to the Kingdoms menus through the Panels SDK. Use whenever a session adds or edits a guild surface — a home menu, an admin menu, a live panel, a channel, a category — or wires mod/game menus into the tree.
---

# Discord Panels (the Panels SDK rules)

Every pinned menu and every scope folder of the platform goes
through the **Panels SDK** — `src/kingdoms/discord/ui/panels.py`
(the declarative specs) and `panels_provisioning.py` (the tree
rules). Never hand-roll a channel creation, a pin, or a heal loop:
the SDK owns provisioning, translation, pinning and healing.

The channel tree — what goes where, the canonical order, the
naming — is **documented once** in
[docs/architecture/channel-tree.md](../../../docs/architecture/channel-tree.md)
(the kingdoms repo is the source of truth). This skill is the
how-to companion: read the tree doc first, apply it with the SDK.

## The three declarative bricks

```python
from kingdoms.discord.ui.panels import (
    ChannelDecl, PanelSpec, PinMode, ScopeSpec, register_scope,
)

# 1. The channels of one scope folder, tree-rule-declared.
channels = (
    ChannelDecl(key="general",    label_key="ui.channels.general",    access="readonly"),
    ChannelDecl(key="discussions", label_key="ui.channels.discussions"),
    ChannelDecl(key="classement", label_key="ui.channels.classement", access="readonly"),
    ChannelDecl(key="admin",      label_key="ui.channels.admin",      access="admin"),
    ChannelDecl(key="decisions",  label_key="ui.channels.decisions",  access="admin"),
)

# 2. The frozen menus pinned in those channels.
panels = (
    PanelSpec(
        name="ladder-home",
        channel="general",
        build=build_ladder_home,          # async (guild_id, locale) -> LayoutView
        pin_mode=PinMode.LATEST_ONLY,     # the pin contract
        description_key="ui.panels.ladder_home",
    ),
    PanelSpec(
        name="ladder-admin",
        channel="admin",
        build=build_ladder_admin,
        permissions=("bot-admins",),      # checked at click time too
    ),
)

# 3. The scope folder itself, registered at boot.
register_scope(ScopeSpec(
    scope="ladder",
    category_key="ui.categories.mods_ladder",   # slash-named by convention
    channels=channels,
    panels=panels,
))
```

That is **all** a mod author writes. The SDK does the rest:

- **Provisioning** — the category and channels are created in the
  **guild's locale** (the label keys render through the message
  catalog), in the canonical order (général → discussions → data →
  admin → décisions), read-only on menu channels, admin channels
  hidden from the default role. Idempotent: re-running is a no-op.
- **Pinning** — the panel's message is pinned per its PinMode, its
  id registered under `view:<guild-id>:<slug>` so it survives
  reboots.
- **Healing** — `autoheal=True` (default) recreates and re-pins a
  deleted panel message; the heal matches channels by their stable
  keys, never by the translated name (a rename never breaks it).

## The single ⚙️ Admin button rule

A **public surface never carries action buttons** — a forum post,
a home menu: nothing dangerous is ever exposed to someone who
cannot use it. One ⚙️ **Admin** button (`admin_button` from the
SDK) opens a permission-checked ephemeral management menu whose
buttons are **greyed by the entity's state** (a closed pool shows
Supprimer active and Publier greyed, etc.). The action buttons
themselves live in that ephemeral only.

```python
from kingdoms.discord.ui.panels import admin_button
view.add_item(admin_button(pool.id, "pool", game_key="aoe2"))
```

The admin callback pattern: guard the permission at click time,
open the ephemeral, render the state-greyed actions.

## Frozen menus, ephemeral navigation

A pinned menu is **frozen**: its page never changes, nobody edits
it. Every navigation is an **ephemeral view** opened by its
buttons (sub-menus, modals, back buttons). Never edit the pinned
message to "change page" — open an ephemeral instead. This is why
menu channels are read-only for everyone, admins included: the
discussions live in `discussions` (public) and `décisions`
(admin).

## Adding a scope: the checklist

1. Read the tree doc — place the folder (`games/<jeu>`,
   `mods/<mod>`), decide the data channels (readonly, sync-fed).
2. Declare the channels (ChannelDecl) — the general/discussions/
   admin/décisions four come from the pattern; add the data ones.
3. Declare the panels (PanelSpec) — `<scope>-home` public,
   `<scope>-admin` for the managers, live/data panels as needed.
4. Register the scope at boot (register_scope in the mod's
   registration) — the SDK provisions, pins and heals.
5. Add the label keys to the locale catalogs (FR + EN) — channels
   and panels both.
6. If the scope owns entities with public posts (maps, pools,
   civs, ...), their posts carry the ⚙️ Admin button and its
   ephemeral — never inline action buttons.

## What not to do

- Never `guild.create_text_channel` by hand — a raw creation
  bypasses the translation, the order and the heal.
- Never rename a channel by hand: the label key changes the
  displayed name, the stable key never changes.
- Never pin a menu by hand: the SDK owns the pin id (registry).
- Never put an action button on a public surface — the ⚙️ Admin
  button is the only allowed entry, permission-checked, greyed.
