# Template — Mod README

Copy this directory (or `templates/mod-template/`) to
`docs/MODS/<mod-name>/` when creating a new mod, then fill in **every
section below** — this README is the mod's lore doc: the agent reads it
in full at every session on the mod (see the
[mod-lore](../../../.agents/skills/mod-lore/SKILL.md) skill).

## Purpose and concepts

Describe the mod: its purpose, its core concepts (the nouns of the
game), and one-paragraph lore an agent can reason from before the full
read. Link [REFERENCE.md](REFERENCE.md) when a designer reference exists.

## Channel tree: salons, categories, roles

The mod's Discord organization, as declared in the mod's
`conf/mod.yaml` (botforge-services):

- **categories / channel groups** — one line each: key, display name,
  admin_only?, access roles;
- **salons (channels)** — key, display name, group, kind (text/forum),
  admin-only, access;
- **roles** — the standard trio (candidate/member/admin, prefixed with
  the mod's key) plus any mod-specific role: display name, what it
  gates;
- **the machine-room rule** — which folders are staff-only while the
  mod is installed, and the install/uninstall gate behavior.

## External system integration

- Is the mod **game-bound**? Which game key (hard-coded options are
  intentional then), and what the mod reads from the core catalog
  (maps, pools, civs) without ever owning it;
- **external providers** — which ones (API/gRPC), the config gate, the
  id mapping to the mod's own ids, the provider process wiring;
- **core seams used** — seasons registry id pattern
  `<mod>-<game>-<guild>-<index>`, entity forums, profile route, etc.

## Views, buttons and actions of the mod

The mod's Discord surfaces, as declared in `conf/views.yaml`:

- every view id (`panel:mod:<name>:…` / `menu:mod:<name>:…` — the R9
  naming contract) with its kind (menu/panel/surface) and what it shows;
- the buttons/actions: label key, emoji, style, custom-id namespace
  (`<mod>:<component>:<payload>`), the dynamic-item template, the
  guard (click-time admin check), confirm cards and modals;
- the **admin console** — the SDK-owned `panel:mod:<name>:admin:console`
  and which ops the mod registers on it (`mod="<name>"`).

## Pinned salons

Which panels are pinned, where (salon key), the pin's view id and
builder, and the pin lifecycle (created when missing, refreshed in
place, healed on channel delete, swept when the mod uninstalls).

## Player / admin / bot interactions

Who does what, per flow:

- **player** — the buttons/slash entries a player can use, the
  ephemeral windows they open, the guards (age, slot, cooldown,
  budget, locks…);
- **admin** — the console ops and debug ops, the confirm cards, what
  each mutation does and how it is logged;
- **bot** — the event listeners and boot passes (self-heal, reconcile),
  the scheduled loops (phases, events), what they post where, and the
  never-raise rule (every pass reports to the user, never only logs).

## Usage

```text
/<command> [arguments]   # only if the mod has slash commands
```

## See also

- [RULES.md](RULES.md) — the game rules (automatable/testable)
- [ENVIRONMENT.md](ENVIRONMENT.md) — the environment + season configuration
- [DECISIONS.md](DECISIONS.md) — the validated decisions (they win)
- [REFERENCE.md](REFERENCE.md) — the designer's functional reference
- [../../WORKFLOWS.md](../../WORKFLOWS.md) — related platform workflows
