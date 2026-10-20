# VIEWS — the map of menus and panels

<!-- Generated from kingdoms-services config/views.yaml — edit the
     YAML, then regenerate (scripts/generate_views_doc.py). -->

Every view of the bot: its id, its kind (a **menu** only navigates; a **panel** informs or acts), where it pins, and its buttons — each a link to its target.

Shared rules:

- an admin button carries the 🔒 emoji, the most discreet style;
- a sync button (channels & roles) carries the ⚙️ emoji;
- every view renders its id as its footer;
- caps: 20 maps/pool · 20 active pools/guild · 20 games · 20 mods.

## The views

### `menu:home`

_menu_ — pinned in `root/general`.

Buttons:

- → [`panel:profile`](#panelprofile) — `ui.homes.btn_profile`
- → [`menu:games:home`](#menugameshome) — `ui.homes.btn_games`
- → [`menu:mods:home`](#menumodshome) — `ui.homes.btn_mods`
- → [`menu:admin`](#menuadmin) — `ui.homes.btn_admin` 🔒

### `panel:profile`

_panel_.

_(no buttons — content comes from its wired handler)_

### `menu:admin`

_menu_ — pinned in `bot/admin`.

Buttons:

- → [`panel:status`](#panelstatus) — `ui.homes.btn_status`
- → [`menu:games:admin`](#menugamesadmin) — `ui.homes.btn_games` 🔒
- → [`menu:mods:admin`](#menumodsadmin) — `ui.homes.btn_mods` 🔒
- `ui.homes.btn_sync` ⚙️ sync

### `panel:status`

_panel_.

_(no buttons — content comes from its wired handler)_

### `menu:games:home`

_menu_ — pinned in `games/general`.

Buttons:

- → [`menu:games:aoe2`](#menugamesaoe2) — `ui.games.homes.aoe2`
- → [`menu:games:admin`](#menugamesadmin) — `ui.homes.btn_games` 🔒

### `menu:games:admin`

_menu_ — pinned in `games/admin`.

Buttons:

- → [`menu:game:aoe2:admin`](#menugameaoe2admin) — `ui.games.homes.aoe2` 🔒
- `ui.homes.btn_sync` ⚙️ sync

### `menu:games:aoe2`

_menu_ — pinned in `games/aoe2/general`.

Buttons:

- → [`panel:game:aoe2:live`](#panelgameaoe2live) — `ui.homes.btn_live`
- → [`panel:game:aoe2:players`](#panelgameaoe2players) — `ui.homes.btn_users`
- → [`menu:game:aoe2:admin`](#menugameaoe2admin) — `ui.homes.btn_admin` 🔒

### `menu:game:aoe2:admin`

_menu_ — pinned in `games/aoe2/admin`.

Buttons:

- `ui.homes.btn_add_map` — action `add-map`
- `ui.homes.btn_create_pool` — action `create-pool`
- `ui.homes.btn_sync` ⚙️ sync

### `panel:game:aoe2:live`

_panel_.

_(no buttons — content comes from its wired handler)_

### `panel:game:aoe2:players`

_panel_.

_(no buttons — content comes from its wired handler)_

### `menu:mods:home`

_menu_ — pinned in `mods/general`.

Buttons:

- → [`menu:mod:ladder`](#menumodladder) — `ui.mods.homes.ladder` *(disabled)*
- → [`menu:mod:tournament`](#menumodtournament) — `ui.mods.homes.tournament` *(disabled)*
- → [`menu:mod:kingdom`](#menumodkingdom) — `ui.mods.homes.kingdom` *(disabled)*
- → [`menu:mods:admin`](#menumodsadmin) — `ui.homes.btn_mods` 🔒

### `menu:mods:admin`

_menu_ — pinned in `mods/admin`.

Buttons:

- → [`menu:mod:ladder:admin`](#menumodladderadmin) — `ui.mods.homes.ladder` 🔒 *(disabled)*
- → [`menu:mod:tournament:admin`](#menumodtournamentadmin) — `ui.mods.homes.tournament` 🔒 *(disabled)*
- → [`menu:mod:kingdom:admin`](#menumodkingdomadmin) — `ui.mods.homes.kingdom` 🔒 *(disabled)*
- `ui.homes.btn_sync` ⚙️ sync

### `menu:mod:ladder`

_menu_.

_(no buttons — content comes from its wired handler)_

### `menu:mod:tournament`

_menu_.

_(no buttons — content comes from its wired handler)_

### `menu:mod:kingdom`

_menu_.

_(no buttons — content comes from its wired handler)_

### `menu:mod:ladder:admin`

_menu_.

_(no buttons — content comes from its wired handler)_

### `menu:mod:tournament:admin`

_menu_.

_(no buttons — content comes from its wired handler)_

### `menu:mod:kingdom:admin`

_menu_.

_(no buttons — content comes from its wired handler)_

## The channel tree (the provisioned scopes)

The scopes the platform provisions — the channels and categories the
sync button recreates. A channel: `key` (stable id), `label` (i18n key),
`kind` (text|forum), `access` (public|readonly|admin).

### `root`

- `general` — ui.panels.channels.general · text · readonly
- `discussions` — ui.panels.channels.discussions · text · public

### `bot`

Category: `ui.panels.categories.bot`.

- `logs` — ui.panels.channels.logs · text · admin
- `admin` — ui.panels.channels.admin · text · admin
- `decisions` — ui.panels.channels.decisions · text · admin

### `games`

Category: `ui.panels.categories.games`.

- `general` — ui.panels.channels.general · text · readonly
- `admin` — ui.panels.channels.admin · text · admin

### `games/aoe2`

Category: `ui.panels.categories.games_aoe2`.

- `general` — ui.panels.channels.general · text · readonly
- `live` — ui.panels.channels.live · text · readonly
- `civs` — ui.panels.channels.civs · forum · readonly
- `maps` — ui.panels.channels.maps · forum · readonly
- `map-pools` — ui.panels.channels.map_pools · forum · readonly
- `admin` — ui.panels.channels.admin · text · admin

### `mods`

Category: `ui.panels.categories.mods`.

- `general` — ui.panels.channels.general · text · readonly
- `admin` — ui.panels.channels.admin · text · admin

## Adding or moving a view

Platform views live in `config/views.yaml`; a mod's own views live in
its own `config/mods/<mod>.views.yaml` (a mod's files never scatter —
kingdoms#179) and merge into the same registry.

1. **Declare** the view in the right YAML:
   id, kind, pin scope, buttons (target/label/admin/sync/action);
2. **Regenerate** this doc (`scripts/generate_views_doc.py`);
3. **Wire** the handler — `wire_view("<id>", handler)` for a panel,
   `wire_action("<view>", "<action>", handler)` for an action;
4. **Translate** the labels (`fr.yaml` and `en.yaml`, same change);
5. **Test**: the registry validates the YAML — an undeclared
   target, a button with no driver, an action without a label
   are drifts the tests reject.
