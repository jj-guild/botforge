# Pong — Mod Environment

Environnement et configuration du mod. Valeurs par défaut issues du
règlement S5 ([REFERENCE.md](REFERENCE.md)) et des décisions
([DECISIONS.md](DECISIONS.md), D-PONG-001..011).

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | Mod activé ou non |
| `game_key` | str | Clé du juego → jeu lié — défaut `aoe2` (mod game-bound ; le mod lit le catalogue via le core, ne le possède pas) |
| `season_name` | str | Nom de la saison active (forme « AOE Pong S<N> ») |
| `rounds_per_season` | int | Nombre de rondes par saison — défaut **4** (D-PONG-005) |
| `round_window` | dict | Fenêtre de ronde — défaut mercredi → mardi (7 jours), timer de clôture auto |
| `bo_format` | int | Meilleur-of des matchs — défaut 5 (BO5) |
| `civs_remaining` | int | Civs restantes après le ban automatisé par table — défaut 15 |
| `tables_count` | derived | **Nombre d'inscrits / 2** (D-PONG-008) ; effectif impair bloquant jusqu'à Q-PONG-002 |
| `elo_seed_formula` | expr | Seed elo = `(2 × Elo actuel + Elo max) / 3`, calculé à l'inscription (D-PONG-007) |
| `move_policy` | enum | **`classic`** (gagnant monte, perdant descend) ou **`semi_blocked`** (groupes de 2 tables, 3 si impair — mouvements intra-groupe uniquement) — paramètre de saison (D-PONG-006) |
| `draft_map_preset` | url | Preset aoe2cm du map pool de la saison (S5 : https://aoe2cm.net/preset/pGWoJ) |
| `civ_draft_base_preset` | url | `base_preset` aoe2cm duquel le mod **dérive** le preset draft-civ de chaque table (D-PONG-009 ; générateur Python du mod owner, source aoe2cm : SiegeEngineers/aoe2cm2) |
| `map_pool` | ref | Référence au pool de maps de saison du core (`GameDataService`) — jamais une liste en dur dans le mod |
| `open_stream` | bool | Open stream autorisé — défaut vrai (titre « AOE Pong » exigé, non vérifié par le bot) |
| `patch_policy` | enum | Politique de patch en cours de tournoi — défaut « admin decides » (console) |
| `close_tables` | bool | Fermer les salons de tables à la clôture de ronde — défaut vrai |
| `planning_requirement` | str | Exigence déclarative d'inscription : « deux disponibilités de 3h consécutives dans 17h-23h » (fuseau FR), captée au moment de l'inscription |
| `records_provider` | ref | **Phase 2 (D-PONG-010)** : provider de génération du zip de records depuis les parties des joueurs (piste : https://replaypacker.zeta-two.com) |

## Channels and roles

Canaux et rôles **déclarés** par le mod dans son YAML de déclaration
(`modules/mods/pong/conf/mod.yaml`, botforge-services). Les canaux sont
adressés par des clés de catégorie scoped-mod (`pong:<key>`) ; les
rôles par des clés logiques. Le core les provisionne via
`ModRegistry` + `ChannelService`/`RoleService` (botforge-services#26)
— jamais de catégories de la plateforme ici.

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
map pool (référence core), presets (map + `base_preset` civs),
`bo_format`, `rounds_per_season` (4), `move_policy`
(classic/semi_blocked), politiques (`open_stream`, `patch_policy`).
