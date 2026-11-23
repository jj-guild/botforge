
# Pong — Mod Environment

Environnement et configuration du mod. Les valeurs par défaut viennent du
règlement S5 ([REFERENCE.md](REFERENCE.md)) ; tout ce qui est marqué
**À DÉFINIR** attend une décision (DECISIONS.md).

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | Mod activé ou non |
| `game_key` | str | Clé du jeu lié — défaut `aoe2` (mod game-bound ; le mod lit le catalogue via le core, ne le possède pas) |
| `season_name` | str | Nom de la saison active (forme « AOE Pong S<N> ») |
| `rounds_per_season` | int | Nombre de rondes par saison — **À DÉFINIR** (source S5 contradictoire : 4 vs 6, DECISIONS) |
| `round_window` | dict | Fenêtre de ronde — défaut mercredi → mardi (7 jours), timer de clôture auto |
| `bo_format` | int | Meilleur-of des matchs — défaut 5 (BO5) |
| `civs_remaining` | int | Civs restantes après le ban automatisé par table — défaut 15 |
| `tables_count` | int | Nombre de tables concurrentes par ronde — **À DÉFINIR** |
| `table_order_key` | enum | Clé de tri joueur A/B sur une table (seed, elo, place ronde précédente) — **À DÉFINIR** |
| `edge_policy` | enum | Mouvements aux bornes (le gagnant de la dernière table, le perdant de la première) — **À DÉFINIR** |
| `draft_map_preset` | url | Preset aoe2cm de draft map (S5 : https://aoe2cm.net/preset/pGWoJ) |
| `map_pool` | ref | Référence au pool de maps de saison du core (`GameDataService`) — jamais une liste en dur dans le mod |
| `open_stream` | bool | Open stream autorisé — défaut vrai (titre « AOE Pong » exigé, non vérifié par le bot) |
| `patch_policy` | enum | Politique de patch en cours de tournoi — défaut « admin decides » (console) |
| `close_tables` | bool | Fermer les salons de tables à la clôture de ronde — défaut vrai |
| `planning_requirement` | str | Exigence déclarative d'inscription : « deux disponibilités de 3h consécutives dans 17h-23h » (fuseau FR), captée au moment de l'inscription |

## Channels and roles

Canaux et rôles **déclarés** par le mod dans son YAML de config
(`config/mods/pong.yaml`, botforge-services). Les canaux sont adressés par
des clés de catégorie scoped-mod (`pong:<key>`) ; les rôles par des clés
logiques. Le core les provisionne via `ModRegistry` +
`ChannelService`/`RoleService` (botforge-services#26) — jamais de
catégories de la plateforme ici.

### Categories (mod-scoped)

| Clé | Nom d'affichage | Admin only | Rôles d'accès |
| --- | --------------- | ----------- | ------------- |
| `pong:ladder` | AOE Pong | non | `pong_player`, `pong_admin` |
| `pong:tables` | AOE Pong — Tables | non | `pong_player`, `pong_admin` |
| `pong:admin` | AOE Pong — Staff | oui | `pong_admin` |

### Salons (canaux)

| Clé | Nom | Groupe | Kind | Accès |
| --- | --- | ------ | ---- | ----- |
| `pong:announcements` | annonces-pong | ladder | text | joueurs (lecture), admins (post) |
| `pong:bot-commands` | bot-commands | ladder | text | players (commandes) |
| `pong:planning` | planification | ladder | forum (1 topic par match) | players |
| `pong:records` | records | ladder | text | players, casters |
| `pong:casting` | casting | ladder | text | public read |
| `pong:table_<n>` | table-<n> | tables | text | `pong_player` de la table + admins (channels **générés** par ronde, créés à l'ouverture, fermés/archivés à la clôture) |

### Roles

| Clé | Nom | Ce que ça gate |
| --- | --- | --------------- |
| `pong_candidate` | Pong Candidate | `/register` fait, pas encore inscrit à la saison |
| `pong_player` | Pong Player | joueur inscrit de la saison (salons ladder + tables) |
| `pong_admin` | Pong Admin | catégorie staff, console du mod, OPs admin |
| `pong_caster` | Pong Caster | annonce de cast (rôle descriptif, open stream) |

## Season configuration

Saisons enregistrées dans le registry de saisons du core avec l'id
visible game-scoped `pong-aoe2-<guild id>-<index>` (le mod ne fait
jamais son propre compteur). À l'activation d'une saison :
map pool (référence core), presets (map + civs), `bo_format`,
`rounds_per_season`, politiques (`open_stream`, `patch_policy`).
