# Channel tree — channels and menus organization

> Source of truth: how each mod/game organizes its channels, where the
> pinned menus live, and how to evolve the tree. Provisioning applies
> these rules automatically (SDK panels).

## Reference tree

```
GUILD
│
├── # 🗺️ general ………… [menu: view:home]
├── # 💬 discussions … (open, public)
│
├── 📂 bot
│   ├── # 📜 logs
│   ├── # 🛠️ admin ……… [menu: view:bot:admin]
│   └── # ⚖️ decisions … (open, admin)
│
├── 📂 games
│   ├── # 🗺️ general … [menu: view:games:home]
│   └── # 🛠️ admin ……… [menu: view:games:admin]
│
├── 📂 ⚔️ games/aoe2
│   ├── # 🗺️ general … [menu: view:aoe2:home]
│   ├── # 📡 live ……… [dashboard: view:aoe2:live]
│   ├── # 🏛️ civilizations (forum, sync)
│   ├── # 🌍 maps ………… (forum, sync)
│   ├── # 🧩 map pools … (forum, sync)
│   └── # 🛠️ admin ……… [menu: view:aoe2:admin]
│
├── 📂 🧩 mods
│   ├── # 🗺️ general … [menu: view:mods:home]
│   └── # 🛠️ admin ……… [menu: view:mods:admin]
│
├── 📂 🧩 mods/<mod>   (one folder per mod, upcoming)
│   ├── # 🗺️ general … [menu: view:<mod>:home]
│   ├── # 💬 discussions (open, public)
│   ├── # <data-*> ……… (readonly, sync)
│   ├── # 🛠️ admin ……… [menu: view:<mod>:admin]
│   └── # ⚖️ decisions … (open, admin)
│
└── 📂 🎮 games/<game>   (one folder per game, upcoming)
    ├── # 🗺️ general … [menu: view:<game>:home]
    ├── # 💬 discussions (open, public)
    ├── # <forums> ……… (forums, sync)
    ├── # 🛠️ admin ……… [menu: view:<game>:admin]
    └── # ⚖️ decisions … (open, admin)

Grouping folders (games, mods, games/<game>) carry only `general` and
`admin`: exchanges and decisions live in the **perimeter** folders
(mods/<mod>, games/<game>), never in the grouping folders.
```

## Structural rules

1. **One perimeter = one folder** (category with a slash:
   `games/aoe2`, `mods/ladder`). The folder's channels do not repeat the
   scope (`# civs`, not `# aoe2-civs`). The root scope (`root`) carries
   `general` and `discussions` **without a category**.

2. **The bot always allows itself**: every provisioned channel carries
   an explicit overwrite for the bot itself (view, send, manage, embed,
   attach) — otherwise a `view_channel=False` for @everyone locks the
   bot out of its own channel and every surface (pins, syncs,
   dashboards) degrades to 403. Rule enforced by provisioning, never
   bypassed by hand.

3. **Best-effort per channel, never per scope**: a Discord operation
   that fails on one channel (403 on a move, rate limit, …) skips that
   channel and continues the scope — the other channels' resolutions
   still persist. A channel failure must never empty a whole folder
   (lesson of 2026-10-13: a single 403 on `channel.edit(category=...)`
   left a whole scope unresolved, hence empty).

4. **Resolution by stored id, never by name**: each provisioned channel
   is persisted under `tree:<scope>:<key>` (collection `channels`);
   syncs, pins and dashboards resolve by that id. The display name is
   only a translated label — no code resolves by name. Provisioning is
   the **only** owner of creation: a resolution that finds no stored id
   creates nothing (no-op).

5. **Canonical order** in each folder: `general` → `discussions` (public,
   unique — never a chat/discussions duplicate) → data channels
   (readonly, sync) → `admin` → `decisions`. `admin` and `decisions`
   always close the folder.

6. **The `bot` category is private** (bot-admins). Public exchanges live
   in `# discussions` at the root; there is no `bot/chat` nor
   `admin-chat` at the root.

7. **Translation at creation**: each channel is named in the guild's
   language at provisioning time (`general`, `discussions`,
   `decisions`, `civs`…). The internal key (locale key) is stable; only
   the display name is translated; the heal recognizes channels by their
   key, never by their display name.

8. **Menu channels are readonly** (nobody writes in them, admins
   included). Exchanges go to `discussions` (public) or `decisions`
   (perimeter admin).

9. **View ids are flat**: a view id's scope is the **last segment** of
   the folder scope — `games/aoe2` gives `view:aoe2:home`,
   `view:aoe2:admin`, `view:aoe2:live`; `mods/ladder` will give
   `view:ladder:news`. Never a slash in a view id: they must stay
   quotable.

10. **Every menu is a `PanelSpec`** (SDK `botforge.discord.ui`):
    `name` (registry `view:<guild-id>:<slug>`), `pinned_on`
    (channel + PinMode LATEST_ONLY|ALL|None), `autoheal`,
    `navigable` (False everywhere: pinned, ephemerals), `permissions`
    (required roles), `build`. The SDK provisions, pins, translates;
    healing is **on demand** (the perimeter's Sync button), never in
    real time.

## Menus: pinned + ephemeral navigation

A pinned menu is **static**: its page never changes. Its buttons open
**ephemeral views** in which you navigate (back, sub-views, modals).
Public surfaces **never** expose an action button directly.

### The single Admin button

On a public post (map forum post, pool, civ), a single visible button:
**⚙️ Admin**. It opens a management ephemeral, checks the permission at
click time, and offers buttons **greyed out by context**:

| Post | Admin ephemeral |
|---|---|
| Map | [Add to a pool] [Delete] — delete greyed if the map is in an active pool; add greyed if no editable pool |
| Map pool | [Edit] [Publish] [Close] [Delete] — greyed by lifecycle (editing → Publish active; published → Close active; closed → Delete active, confirmed by name) |

**Rule to remember**: dangerous buttons are never exposed on a public
surface; they live behind the Admin button, in an ephemeral, checked at
click time, greyed by context.

## How to add a perimeter (game or mod)

1. **Declare the folder's channels** (stable key + i18n label + kind:
   text/forum/category + access: public/admin/readonly).
2. **Declare the PanelSpecs**: `<scope>-home` (public, readonly,
   autoheal), `<scope>-admin` (perimeter bot-admins), optionally
   `<scope>-live` or data panels.
3. **Register at boot**: the SDK provisions the folder in the guild's
   language, pins the menus, heals.
4. **Data** (forum posts) stays managed by periodic syncs — one post
   per entity, with its Admin button.

### Example — ladder mod (upcoming)

```
📁 mods/ladder
   ├── # general        ……… [menu: ladder-home]
   ├── # discussions    ……… (open, public)
   ├── # leaderboard    ……… (readonly, sync — top N)
   ├── # news           ……… (readonly, sync — results)
   ├── # matches        ……… (readonly, sync — played matches)
   ├── # admin          ……… [menu: ladder-admin]
   └── # decisions      ……… (open, admin)
```

### Example — kingdoms mod (upcoming)

```
📁 mods/kingdoms
   ├── # general        ……… [menu: botforge-home]
   ├── # discussions    ……… (open, public)
   ├── # map            ……… (readonly, sync)
   ├── # admin          ……… [menu: botforge-admin]
   └── # decisions      ……… (open, admin)
```

## Evolving the tree

- **Add a data channel**: key + label + provisioning — the heal
  recreates it; no menu code to touch if it has no menu.
- **Add a menu**: one more PanelSpec; the SDK pins it on the next pass.
- **Rename**: the key never moves; only the translated label changes —
  the heal follows by key.
- **Remove**: remove the declaration; the channel becomes orphan
  (archive it manually — the SDK never deletes).
