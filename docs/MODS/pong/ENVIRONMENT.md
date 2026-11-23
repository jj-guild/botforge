# Pong — Mod Environment

Environnement et configuration du mod.

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | Mod activé ou non |

**À DÉFINIR** — clés spécifiques au mod (limites, cooldowns, budgets…).

## Channels and roles

Canaux et rôles **déclarés** par le mod dans son YAML de config
(`config/mods/pong.yaml`, botforge-services). Les canaux sont adressés
par des clés de catégorie scoped-mod (`mod:key`, ex. `pong:arena`) ;
les rôles par des clés logiques (ex. `pong_player`). Le core les
provisionne automatiquement via `ModRegistry` +
`ChannelService`/`RoleService` (botforge-services#26) — ne jamais
lister de catégories de la plateforme ici, sauf si le mod en utilise
une (ex. `REPORTS`).

**À DÉFINIR** — arborescence de salons et rôles du mod.
