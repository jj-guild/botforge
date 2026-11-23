# Pong — Mod Environment

Environnement et configuration du mod. Valeurs par défaut issues du
règlement S5 ([REFERENCE.md](REFERENCE.md)) et des décisions
([DECISIONS.md](DECISIONS.md), D-PONG-001..019).

## Configuration

| Key | Type | Description |
| --- | ---- | ----------- |
| `enabled` | bool | Mod activé ou non |
| `game_key` | str | Clé du jeu lié — défaut `aoe2` (mod game-bound ; le mod lit le catalogue via le core, ne le possède pas) |
| `season_name` | str | Nom de la saison active (forme « AOE Pong S<N> ») |
| `rounds_per_season` | int | Nombre de rondes par saison — défaut **4** (D-PONG-005) |
| `round_window` | dict | Fenêtre de ronde — défaut mercredi → mardi (7 jours), timer de clôture auto |
| `round_grace_days` | int | **Grâce en jours au-delà de la fenêtre — défaut 3** (D-PONG-012) : appariement suivant sur les résultats **validés à l'échéance** ; un match joué pendant la grâce compte au récap, **mouvement différé d'une ronde** |
| `bo_format` | int | Meilleur-of des matchs — défaut 5 (BO5) |
| `civs_remaining` | int | Civs restantes après le ban automatisé par table — défaut 15 |
| `tables_count` | derived | **Nombre d'inscrits / 2** (D-PONG-008) ; l'effectif jouable n'est jamais impair (chaîne de parité, D-PONG-019, RG-TAB-4) |
| `elo_seed_formula` | expr | Seed ladder = `(2 × Elo actuel + Elo max) / 3`, calculé à l'inscription (D-PONG-007) |
| `human_seed` | dict | **Seed humain (D-PONG-013)** : autodéclaration de niveau à l'inscription + `admin_override: true` (correction admin avant tirage et entre les rondes, console). Sert au placement uniquement, **jamais affiché** |
| `move_policy` | enum | **`classic`** (gagnant monte, perdant descend) ou **`semi_blocked`** (groupes de 2 tables, 3 si impair — mouvements intra-groupe uniquement) — définitions D-PONG-006 |
| `move_policy_schedule` | str | **Alternance par saison (D-PONG-012)** : `alternate` → S1 `classic`, S2 `semi_blocked`, S3 `classic`… (valeur par défaut) |
| `table_naming` | enum | **Noms neutres (D-PONG-014)** : les salons de tables ne portent ni numéro d'ordre ni niveau — défaut `neutral_random` ; `chain_position` interne, jamais affichée |
| `waitlist_admin_pairing` | bool | Le binomage de la file d'attente en duos d'insertion est décidé par l'admin, duo par duo (D-PONG-015) — défaut vrai (pas de tolérance automatique) |
| `orphan_match` | enum | Match d'appoint volontaire contre un orphelin sans remplaçant : `recap_only` (défaut, D-PONG-018) — aucun mouvement de table, proposé aux voisins par proximité ; fusible en dernier recours : volontaire de la file, puis admin (D-PONG-019) |
| `recap_delivery` | dict | Récap personnel par saison (sets, W/L, adversaires, parcours de tables) — **`on_request: ephemeral`** (réponse de `/recap` visible uniquement du demandeur, D-PONG-014) et **`season_close: dm`** (récap final en DM privé à la clôture). Aucune vue comparative publiée |
| `draft_map_preset` | url | Preset aoe2cm du map pool de la saison (S5 : https://aoe2cm.net/preset/pGWoJ) |
| `civ_draft_base_preset` | url | `base_preset` aoe2cm duquel le mod **dérive** le preset draft-civ de chaque table (D-PONG-009 ; générateur Python du mod owner, source aoe2cm : SiegeEngineers/aoe2cm2) |
| `map_pool` | ref | Référence au pool de maps de saison du core (`GameDataService`) — jamais une liste en dur dans le mod |
| `open_stream` | bool | Open stream autorisé — défaut vrai (titre « AOE Pong » exigé, non vérifié par le bot) |
| `patch_policy` | enum | Politique de patch en cours de tournoi — défaut « admin decides » (console) |
| `close_tables` | bool | Fermer les salons de tables à la clôture de ronde — défaut vrai |
| `planning_requirement` | str | Exigence déclarative d'inscription : « deux disponibilités de 3h consécutives dans 17h-23h » (fuseau FR), captée au moment de l'inscription |
| `records_provider` | ref | **Phase 2 (D-PONG-010)** : provider de génération du zip de records depuis les parties des joueurs (piste : https://replaypacker.zeta-two.com) |

## État joueur (cycle de vie)

`candidate` → `registered` → (`waitlist` — après clôture de la fenêtre
d'inscription, D-PONG-015) → `player` (saison active) → `replacing`
(entré au créneau exact d'un partant, D-PONG-017) → `departed`
(retrait validé admin, récap clôturé). Toute transition de retrait
est **constat par le bot → décision admin console** (RG-ADM).

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
| --- | --------------- | ------ | ---- | ----- |
| `pong:announcements` | annonces-pong | ladder | text | joueurs (lecture), admins (post) ; liste des tables **sans ordre de niveau** (D-PONG-014) |
| `pong:bot-commands` | bot-commands | ladder | text | players (commandes, dont `/recap` en réponse ephemeral) |
| `pong:planning` | planification | ladder | forum (1 topic par match) | players |
| `pong:records` | records | ladder | text | players, casters |
| `pong:casting` | casting | ladder | text | public read |
| `pong:table_<slug>` | table-<nom neutre> | tables | text | `pong_player` de la table + admins (channels **générés** par ronde, noms neutres sans numéro de niveau — D-PONG-014/RG-TAB-5, créés à l'ouverture, fermés/archivés à la clôture) |

### Roles

| Clé | Nom | Ce que ça gate |
| --- | --------------- | --------------- |
| `pong_candidate` | Pong Candidate | `/register` fait, pas encore inscrit à la saison |
| `pong_player` | Pong Player | joueur inscrit de la saison (salons ladder + tables) |
| `pong_waitlist` | Pong Waitlist | candidat après clôture de la fenêtre d'inscription (D-PONG-015) ; attend un binôme (RG-TAB-3/4) |
| `pong_admin` | Pong Admin | catégorie staff, console du mod, OPs admin |
| `pong_caster` | Pong Caster | annonce de cast (rôle descriptif, open stream) |

## Season configuration

Saisons enregistrées dans le registry de saisons du core avec l'id
visible game-scoped `pong-aoe2-<guild id>-<index>` (le mod ne fait
jamais son propre compteur). À l'activation d'une saison :
map pool (référence core), presets (map + `base_preset` civs),
`bo_format`, `rounds_per_season` (4), `round_grace_days` (3),
`move_policy` résolu par `move_policy_schedule: alternate`
(S1 classic, S2 semi_blocked, S3 classic…, D-PONG-012), politique
de parité (`waitlist_admin_pairing`, `orphan_match`), `recap_delivery`
(`on_request: ephemeral`, `season_close: dm`), politiques
(`open_stream`, `patch_policy`).
