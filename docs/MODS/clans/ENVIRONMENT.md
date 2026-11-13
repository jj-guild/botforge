# Clans mod — Environment

Configuration du mod clans — déclaration : `modules/mods/clans/mod.yaml`
(layout modulaire botforge#178).

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | mod actif |
| `seasonal` | bool | `false` — mod permanent |
| `private` | bool | `true` — visible/provisionné seulement pour ses owners et les bot-admins |
| `owner_discord_ids` | list | les owners du mod (ids Discord) |
| `settings.enrollment.min_elo` | int | ELO RM 1v1 requis (dégrade en revue manuelle sans seam ELO core) |
| `settings.enrollment.manual` | bool | toute candidature attend les admins du clan |

## Channels and roles

Channels (adressés `clans:<key>`):

- `clans:dashboard` — le salon « Clans » (dashboard épinglé)

Roles (résolus par RoleService):

- `clans:leader` — Chef de clan
- `clans:officer` — Officier de clan (valide les admissions)
- `clans:member` — Membre de clan

## Surfaces

- `/clan` — le dashboard éphémère : chaque clan, son nombre de membres
- forum par clan : liste des joueurs, bouton « Demander à rejoindre »
