# Référence — Mod Ladder 1v1 (rapport de l'existant JeanJack, V2.0)

> Rapport généré par le game designer à partir du code JeanJack, avec la
> stack cible (MongoDB + Redis) et les principes de séparation
> plateforme / mod / jeu. **Document autonome, archivé tel quel** — c'est
> la source de vérité fonctionnelle pour la migration "en mieux".
> L'adaptation aux contrats réels de BotForge (ADR-0011 seams, ADR-0020
> process split) se négocie dans [../v0.4.0-aoe2-ladder.md](../v0.4.0-aoe2-ladder.md),
> jamais en éditant cette référence.

---

## 0. Principes d'architecture (à lire en premier)

Trois domaines **strictement indépendants**, chacun développé et versionné séparément :

```
┌────────────────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
│  Plateforme (Discord…)  │     │      MOD LADDER      │     │   Jeu (AoE2…)           │
│  vues, boutons, modals, │◄────┤  rules, rating,      ├────►│  profils, lobbies,      │
│  embeds, DM, channels   │ P   │  matchmaking, maps,  │  G  │  résultats, temps réel  │
│  rôles, i18n            │ O   │  state machine,      │  A  │                         │
│                         │ R   │  persistance         │  M   │                         │
└────────────────────────┘ T   └──────────────────────┘  S └─────────────────────────┘
```

Règles de séparation non négociables :

1. **Le cœur du mod ne connaît ni Discord, ni AoE2.** Aucune collection Mongo du mod ne contient d'identifiants Discord (`discord_id`, `message_id`, `channel_id`, `role_id`) ni d'identifiants propres au jeu (`profile_id`, `match_id` in-game). Les collections ne contiennent que des identités **internes au mod** et des références abstraites.
2. **Des contrats d'interface (ports) existent déjà** entre ces domaines — ils ne sont **pas décrits dans ce document** et l'implémenteur (agent IA) devra les découvrir dans la stack cible et **faire les adaptations nécessaires**. Ce document définit ce que le mod **attend** de ces contrats (§1), pas leur signature exacte.
3. **AoE2 est le premier jeu supporté, pas le seul.** Toute règle, donnée ou workflow du cœur du mod doit rester valide pour un autre jeu (§6 : ce qui est spécifique à AoE2 vit exclusivement dans l'adaptateur jeu).
4. **Discord est la première plateforme, pas la seule.** Le mod doit pouvoir être exposé sur une autre plateforme de chat. Les IDs de messages/URLs par plateforme sont stockés via un **mécanisme existant de la stack** (registre de messages par plateforme), **jamais dans les collections du mod (§2.3)**.

Le mod expose et consomme :

**Ports consommés par le mod (fournis par la stack, à adapter) :**
- `PlatformGateway` : identité (user id mod ↔ user id plateforme), livraison de notifications, registre de messages par plateforme (persist/résoudre les IDs de messages par (plateforme, entité)), notion de "surface" (l'équivalent des canaux/catégories), notions de rôle/permission ("admin ladder", "joueur ladder").
- `GameGateway` : résolution d'identité ((game_key, profile_id) → user id mod), événements de cycle de vie de partie (lobby créé/fermé, partie commencée/terminée, participants), récupération de résultat de match, métadonnées de partie (map, durée, factions).
- Contrat de **profil utilisateur ↔ profil jeu** : la liaison "user mod ↔ profile_id du jeu" est gérée côté jeu/plateforme (workflow existant), le mod la consomme uniquement via `GameGateway`.

**Ports fournis par le mod (consommés par les adaptateurs) :**
- Services métier : inscription, file, matchmaking, matchs, rating, maps/pools, settings, audit (§3–§5).
- Catalogue d'**intents de notification** : événements métier à rendre (§7.2) — l'adaptateur plateforme décide du rendu (embed, DM, message éphémère, toast…), du texte (i18n) et du canal.

---

## 1. Contrats attendus (définition fonctionnelle, pas signature)

### 1.1 `PlatformGateway`

| Capacité | Attente fonctionnelle |
|---|---|
| Identité | Le mod ne manipule que des `user_id` internes. Le gateway traduit user mod ↔ plateforme (ex. Discord id). Un user mod peut exister sur plusieurs plateformes. |
| Registry de messages | Persister/résoudre des IDs de messages **par plateforme** pour les messages persistants (menu, file, leaderboard, fiche joueur, message de match). Le mod référence ces messages par `(surface_key, entity_type, entity_id)` et délègue le stockage concret au registry. **Interdit** de stocker un ID de message dans une collection du mod. |
| Surfaces | Notion abstraite de "surface nommée" (`play`, `leaderboard`, `matches`, `players`, `admins` — §7.1) : le gateway crée/gère l'équivalent local (canaux/catégories Discord, ou autre chose) et expose leur existence au mod par clé. Le mod ne stocke pas d'IDs de surfaces. |
| Permissions | Le mod demande "cet user est-il admin ladder ? / joueur ladder ?" — le gateway décide (rôle Discord, ou autre mécanisme sur une autre plateforme). |
| Livraison | `deliver(notification)` : le mod émet un intent (§7.2), le gateway choisit où et comment (message surface, DM, message éphémère d'interaction, mention, rien). |
| Composants interactifs | Le mod définit des **actions abstraites** (join_queue, leave_queue, ready, report, confirm, cancel, invite…) avec préconditions. L'adaptateur les matérialise (boutons, modals, selects, commandes slash). |

### 1.2 `GameGateway`

| Capacité | Attente fonctionnelle |
|---|---|
| Identité de jeu | Résoudre quels `user_id` du mod correspondent aux participants d'une partie du jeu (`resolve(profile_id) → user_id | null`). Un user peut avoir plusieurs profils jeu. |
| Événements de partie | Flux d'événements : `lobby_opened(match_ref, participants, metadata)`, `lobby_closed(match_ref)`, `game_started(match_ref, participants, metadata{map, start_time, factions})`, `game_ended(match_ref)`. `match_ref` = identifiant de partie **côté jeu** (string opaque pour le mod), `participants` = liste de `(profile_id, user_id résolu, metadata faction)`. Le mod n'interprète jamais la sémantique du `match_ref`. |
| Résultat | `get_result(match_ref, timeout, interval) → {winner_user_id, loser_user_id, map, duration, factions} | null`. Le gateway fait la traduction profil→user et la détermination du vainqueur — c'est une exigence forte : **le mod ne doit pas avoir à comprendre le format de résultat du jeu**. |
| Métadonnées d'affichage | Pour la fiche joueur : stats du profil (elo, V/D, rang, dernier match) exposées sous forme **générique** ; l'adaptateur jeu fournit des blocs nommés que l'adaptateur plateforme rend. |
| Liens de jeu | Le gateway fournit des "liens d'action" (rejoindre/spectate la partie, voir les insights) sous forme d'objets `{label, url, scheme_url?}` — le mod les transmet aux intents sans les construire. |
| Capacités déclarées | Le gateway déclare ce que le jeu supporte (temps réel oui/non, résultats fiables oui/non, check de map possible). Le mod **dégrade proprement** : sans temps réel → pas de statuts LOBBY/GAME_STARTED (la machine à états §5 tolère l'absence de ces événements) ; sans résultat fiable → confirmation manuelle systématique. |

**Convention de nommage interne** : le mod identifie le jeu par `game_key` (ex. `aoe2`) stocké sur le ladder ; tout le reste (factions, maps de jeu, leaderboards) est de la responsabilité du gateway. Les **maps du ladder** (§4) sont une donnée du mod — mais leur cohérence avec le jeu (filename) est validée par l'adaptateur jeu si possible (`check_map`), jamais supposée par le cœur.

---

## 2. Modèle de données (MongoDB)

Toutes les collections ci-dessous sont **du mod uniquement** : aucun ID Discord, aucun ID AoE2, aucune URL de message. Horodatages en epoch ms.

**`ladders`** — une config de ladder par serveur/communauté (le concept de "communauté" est résolu par le gateway plateforme en un `owner_ref` opaque) :
```js
{
  _id, owner_ref,            // opaque : résolu par PlatformGateway (ex. guild Discord)
  name: "Ladder 1v1", game_key: "aoe2",
  active_map_pool_id, started_at, ended_at,
  settings: {
    // matchmaking
    base_elo_threshold: 60, elo_threshold_increment: 20, increment_interval: 15,
    elo_threshold_max: 400, matchmaking_tick_interval: 5, instant_match_on_join: true,
    ready_timeout: 180, // durée de l'étape "prêt"
    // rating
    rating_system: "elo", elo_initial: 1000, elo_floor: 800,
    elo_k_provision_match_count: 10, elo_k_newbie: 60, elo_k_standard: 32,
    elo_max_gain: 40, elo_max_loss: 40,
    // maps
    player_fav_count: 3, player_ban_count: 2, random_ban_count: 2,
    // divers
    match_surface_cleanup_delay: 300,
    auto_confirm_system_report: true   // confirmer auto un résultat fiable du gateway
  }
}
```
Tous les settings sont paramétrables par les admins (§7.1) ; valeurs par défaut ci-dessus.

**`players`** :
```js
{ _id, ladder_id, user_id,          // unique (ladder_id, user_id) — user_id = identité mod
  display_name,                      // fourni par PlatformGateway à l'inscription
  rating: 1000, rating_max: 1000,    // caches dérivés de rating_history
  matches_count: 0, wins: 0, losses: 0, streak: 0,   // dérivés des matchs complétés
  rank: null, fav_map_ids: [], ban_map_ids: [],
  queued_at: null, registered_at }
```
Aucun `message_id` : le message persistant de la fiche joueur est référencé via le registry plateforme par `(platform, "player_message", player_id)`.

**`matches`** — 1v1 uniquement, machine à états §5 :
```js
{
  _id, ladder_id, status, created_at, ready_deadline_at,
  host: {user_id, ready_at, fav_map_ids: [], ban_map_ids: []},
  guest: {user_id, ready_at, fav_map_ids: [], ban_map_ids: []},
  origin: "matchmaking" | "invite",
  map_id, map_snapshot: {name, filename},   // figé au pick
  started_at, ready_completed_at,
  game: {                                 // rempli via GameGateway — opaque pour le cœur
    match_ref: <string|null>,              // ID de partie côté jeu (unique index si non-null)
    started_at, ended_at, duration, map_name,
    participants: [{user_id, faction_key}], // faction_key opaque (libellé fourni par le gateway)
  },
  winner_user_id, loser_user_id,
  reporter_user_id, reported_at, confirm_user_id, completed_at,
  rating_applied: {host: {before, after, delta, k}, guest: {...}},
  cancel: {reason, user_id, at},
  invalid_report_attempts: 0
}
```
Aucun `channel_id`/`message_id` : la "surface de match" est référencée par `(platform, "match_surface", match_id)` dans le registry.

**`rating_history`** : `{ _id, ladder_id, match_id, user_id, rating_before, rating_after, delta, k_used, reason: MATCH_RESULT|MANUAL_ADJUSTMENT|RESET, admin_user_id?, created_at }` — source de vérité du rating.

**`maps`** : `{ _id, game_key, name, filename, description, resource_url, archived_at }` — `filename` = référence de map pour le jeu (le sens exact, ex. fichier `.rms` AoE2, est défini par l'adaptateur jeu ; le cœur le stocke comme chaîne opaque obligatoire). Unique (game_key, name) hors archives. `resource_url` = lien de présentation, opaque.

**`map_pools`** : `{ _id, game_key, name, map_pack_url, map_ids: [], archived_at }`
**`map_pool_history`** : `{ _id, ladder_id, map_pool_id, activated_at, deactivated_at }`
**`admin_audit`** : `{ _id, ladder_id, admin_user_id, action, payload_diff, created_at }` — chaque mutation admin.

### 2.3 Mécanisme des IDs de messages par plateforme (règle)

Tout message/surface persistant du mod est enregistré via le mécanisme existant de la stack : le mod appelle le registry avec `(platform, message_key, entity_id)` et l'adaptateur plateforme stocke l'ID concret. Cas d'usage requis : menu play, message file, message leaderboard, fiche joueur, message de match. Le mod ne fait jamais de hypothèse sur le format de l'ID ni sur la plateforme.

### 2.4 Redis

| Clé | Type | Rôle |
|---|---|---|
| `ladder:{id}:queue` | ZSET (score = queued_at) | File d'attente (miroir rapide de `players.queued_at` ; écriture couplée) |
| `ladder:{id}:mm_lock` | SET NX EX | Verrou de passe de matchmaking (exclusion tick/event) |
| `ladder:{id}:settings` | HASH | Cache des settings, invalidé à chaque update |
| `ladder:{id}:rank` | ZSET (score = rating) | Leaderboard rapide |
| `game:{game_key}:rate` | compteurs | Throttle des appels jeu (dans l'adaptateur) |

---

## 3. Rating (Elo) — règles de gestion

inchangé par rapport à la V1, rappelé intégralement :

- **Application unique** au passage REPORTED → COMPLETED ; idempotence garantie par le champ `rating_applied` (rejeu interdit).
- `E = 1/(1+10^((R_adv−R)/400))`, `R' = R + K×(S−E)`, S ∈ {1,0}. 1v1 uniquement.
- **K évolutif** : < `elo_k_provision_match_count` matchs complétés (défaut 10) → K = `elo_k_newbie` (60) ; sinon K = `elo_k_standard` (32).
- **Bornes** : |delta| ≤ `elo_max_gain`/`elo_max_loss` (40) ; plancher `elo_floor` (800) ; initial `elo_initial` (1000).
- **Écriture** : 2 lignes `rating_history` + caches joueur (`rating`, `rating_max`) + compteurs W/L/streak (streak > 0 série de victoires, < 0 série de défaites, bascule → ±1).
- **Corrections** : rejet avant application → retour statut in-game précédent, rien à compenser. Incohérence après application → annulation admin **avec compensation** (écriture inverse `MANUAL_ADJUSTMENT`, recalcul des compteurs, `rating_applied` effacé). Ajustement manuel admin possible (±N, motif obligatoire). Reset possible (`RESET`).
- **Invariant testable** : somme des deltas d'histoire = rating courant.
- Match annulé avant confirmation → aucun impact rating.
- Le rating est **indépendant du jeu** : aucune donnée de jeu n'entre dans le calcul.

## 4. Maps et map pools — règles de gestion

- **Map** : créer (name unique par game_key, filename obligatoire — aucune déduction automatique, description et resource_url optionnelles) ; modifier (confirmation explicite si la map est présente dans des matchs — l'affichage historique change) ; supprimer → **archivage** seulement, interdit si dans un pool non archivé ou utilisée par des matchs (dans ce dernier cas l'archive reste possible : soft-delete sans casse d'historique, la map reste résolvable) ; import en masse avec rapport ligne à ligne.
- **Pool** : créer (nom unique, ≥1 map, warning non bloquant si `nb_maps < random_ban_count + 2×player_ban_count + 1`) ; composer (libre si inactif ; retrait du pool actif permis avec avertissement préférences orphelines) ; **activer** (transactionnel : set `active_map_pool_id` + ligne `map_pool_history` + nettoyage sélectif des fav/ban hors nouveau pool — reset total seulement sur demande explicite + intent de notification "pool switch" + audit) ; dupliquer ; archiver (jamais le pool actif).
- **Pick de map** (au moment où les deux joueurs sont prêts, pas avant) : bans admin aléatoires (`random_ban_count`) ∪ bans joueurs → candidats = pool − bans ; tirage pondéré (poids = 1 + nb de favs pointant la map) ; snapshot figé sur le match. Si l'adaptateur jeu expose `check_map`, une map de lobby non conforme génère un intent d'anomalie (pas un blocage).
- Toute mutation admin → `admin_audit`.

## 5. Matchmaking et machine à états

### 5.1 File et appariement

- **File** : préconditions join = joueur inscrit + **profil jeu résolvable via GameGateway** (au moins un profil lié) + aucun match actif. Leave interdit si match CREATED en attente de ready (annuler le match d'abord).
- **Compatibilité paire** : `|Δrating| ≤ min(seuil_A, seuil_B)`, `seuil = base_elo_threshold + elo_threshold_increment × floor(wait_s / increment_interval)`, cap `elo_threshold_max`. Réciprocité obligatoire.
- **Déclenchement** : événementiel au join/libération (si `instant_match_on_join`), + tick périodique `matchmaking_tick_interval` (filet de sécurité), le tout sous lock Redis.
- **Passe** : (1) annuler les matchs CREATED au ready-deadline dépassé (non-prêts sortis de la file, prêts re-éligibles) ; (2) calculer les paires valides ; (3) **maximum matching** maximisant le nombre de matchs (cas 2 joueurs : la seule paire valide est toujours créée — aucun joueur appariable ne reste seul si un matching complet existe), tri interne par `(min(pair_count), somme pair_count, |Δrating|)` ; (4) créer les matchs, retirer de file, émettre les intents de notification.
- **Transparence d'attente** : la vue file affiche temps d'attente, seuil courant, prochain élargissement ; information unique (anti-spam) si > 2 min sans candidat.

### 5.2 Cycle de vie d'un match

```
CREATED ──(2×prêts)──> READY ──(pick map)──> STARTED
   │ (deadline prêt)                                      │
   ▼                                                      ▼ (événements GameGateway si supportés)
CANCELED                                     LOBBY_OPEN → LOBBY_CLOSED → GAME_LIVE → GAME_ENDED
                                                              │ (2j absents)        │
                                                              ▼                     ▼
                                                          CANCELED/retour     RESULT_PENDING
                                                                                   │
                                                              REPORTED ◄── report (auto via gateway ou manuel)
                                                                  │
                                                                 COMPLETED (confirmation → rating appliqué une fois)
```

Détail des règles (toutes transitions **idempotentes** — les événements externes peuvent être reçus plusieurs fois) :
- **CREATED** : par matchmaking ou invitation (`origin`). `ready_deadline_at = now + ready_timeout`. Une "surface de match" est demandée à la plateforme. Chaque joueur confirme "prêt" ; deadline dépassée → annulation système (sortie de file des non-prêts).
- **READY → STARTED** : les deux prêts → pick map → sortie de file définitive.
- **Événements jeu** (si `realtime` déclaré) : `lobby_opened` → rattachement du `game.match_ref` (ou résolution par participants si le match ne l'avait pas), capture factions ; **piège connu** (AoE2) : le lobby ferme toujours quelques instants avant le début de partie — à `lobby_closed` en statut LOBBY, attendre un délai de grâce (15 s, configurable adapter-side) avant rétrogradation, un `game_started` peut survenir entre-temps. `game_started` avec un participant manquant → intent "joueur manquant" + retour en arrière. `game_ended` → RESULT_PENDING.
- **Sans temps réel** (jeu ne le supportant pas) : STARTED → directement RESULT_PENDING sur report manuel ; l'auto-report est désactivé, la machine à états saute les étapes LOBBY/GAME.
- **REPORTED** : auto (gateway `get_result` — poll par l'adaptateur, recommandé 5 s / timeout 30 s) ou manuel (les reports contradictoires des deux joueurs s'annulent). Mismatch report manuel vs résultat gateway → intent d'alerte admin (jamais de correction silencieuse). Report système fiable (`reliable_results` déclaré) + `auto_confirm_system_report` → COMPLETED direct.
- **COMPLETED** : application du rating (§3) une seule fois.
- **CANCELED** : par joueur (motif obligatoire, sort l'auteur de la file), par système (deadline, joueur manquant). Impossible après COMPLETED.

## 6. Séparation mod / jeu — checklist de rigueur

Le cœur du mod **ne doit contenir** : aucun `profile_id`, aucun ID/fichier propre au jeu dans ses collections (seuls `game_key` et des chaînes opaques `match_ref`/`filename`/`faction_key` y figurent, remplis par le gateway) ; aucune URL de jeu (les liens sont des objets fournis par le gateway et retransmis dans les intents) ; aucune logique de détermination de vainqueur (fournie par le gateway) ; aucune connaissance des leaderboards/civs du jeu.

**Ajouter un jeu = écrire un adaptateur `GameGateway`** qui déclare ses capacités (`realtime`, `reliable_results`, `check_map`, `player_stats`) + fournir maps/pools pour ce `game_key`. Le cœur ne change pas. Les tests d'acceptation du cœur doivent passer avec un gateway mocké sans aucune de ces capacités (parcours dégradé complet).

## 7. Couche plateforme (adaptateur Discord — inventaire de référence)

Tout ce qui suit est la spécification de l'**adaptateur Discord**, transposable à une autre plateforme. Le cœur n'expose que des **actions abstraites** et des **intents de notification**.

### 7.1 Structure Discord

- Catégorie "Ladder 1v1" + surfaces : #play (message persistant menu), #leaderboard (persistant), #matches (flux), #players (fiches), #admins.
- Rôles : "Ladder 1v1 admin", "Ladder 1v1 player".
- Entrée : commande `/ladder` (éphémère) + bouton "Ladder 1v1" dans le menu global du bot.
- IDs de tous les messages persistants → registry plateforme (§2.3), jamais en base mod.

### 7.2 Catalogue d'intents de notification (émis par le cœur, rendus par l'adaptateur)

Chaque intent porte : type, entités (match/joueurs/ladder), payloads ({map, reason, duration, deltas rating, game links[•], deadline, counts…}). Cibles conseillées : `match_surface` (surface du match), `players_surface`, `admins_surface`, `dm` (les deux joueurs). L'adaptateur décide du rendu ; la i18n est côté plateforme.

| Intent | Cible |
|---|---|
| `queue.joined` / `queue.left` | players |
| `match.created` | match + dm |
| `match.player_ready` | match + dm |
| `match.ready_timeout` | match + dm (joueur fautif) |
| `match.started` | match + dm |
| `match.lobby_opened` (+liens rejoindre) | match + dm |
| `match.lobby_closed` | match + dm |
| `match.game_started` (+liens spectate) | match + dm |
| `match.game_ended` (+lien post-partie) | match + dm |
| `match.missing_participant` | match + dm + admins |
| `match.map_mismatch` (si check_map) | match + admins |
| `match.result_reported` (par joueur / par système) | match + dm |
| `match.result_confirmed` (+deltas rating) | match + dm + matches |
| `match.result_rejected` | match + dm |
| `match.report_conflict` (reports contradictoires) | match + dm |
| `match.canceled` (par joueur / système + raison) | match + dm |
| `match.winner_mismatch` (report vs gateway) | admins |
| `match.invite.sent/accepted/refused/expired` | dm |
| `player.not_available` | dm |
| `registration.requested/accepted/refused` | admins / dm |
| `pool.switched` (ancien, nouveau) | players |
| `rating.adjusted` (admin) | admins + joueur |
| `queue.waiting_too_long` (info anti-spam) | dm |

### 7.3 Vues et actions abstraites (adaptateur Discord)

**Menu principal (PlayView)** : bannière, settings visibles ; actions : `play_open`, `leaderboard_open`, `preferences_open`, `admin_open` (si admin).
**PlayLadderView** : `queue_join`/`queue_leave` (exclusifs), `invite_player`, `queue_view`. Préconditions gérées par le cœur : non inscrit → registration ; profil jeu non résolvable → vue "profile manquant".
**QueueView (persistante, paginée)** : par joueur — nom, rating, temps d'attente, seuil courant, prochain élargissement, favs/bans ; actions join/leave/preferences/pagination.
**LeaderboardView (persistante, paginée)** : rang, joueur, `rating (max)`, `N matchs (XV/YD)`, streak.
**MatchView (surface de match, persistante)** : header "Ladder 1v1 {nom} — Match n°{id}", statut traduit, joueurs, map, durée ; timeline complète (créé, prêts, commencé, lobby + lien, partie + lien, terminé + lien, report/confirm/cancel avec auteurs) ; barre d'actions contextuelle : `ready` (CREATED), `report_result`, `confirm_result`, `reject_result`, `cancel_match`, `refresh`, et actions admin : `set_game_match_ref` (saisie manuelle), `fetch_result`, `matchmaking_settings`.
**PlayerView (persistante)** : stats ladder + blocs stats jeu (rendus depuis les métadonnées gateway) ; action `invite_player` si dispo.
**AdminView** : sections Maps (liste, ajouter/éditer/archiver/import masse), Map pools (créer/composer/dupliquer/activer avec diff + choix reset/archiver), Settings (tous les §2), Rating (ajuster, annuler-match avec compensation), Audit (10 dernières entrées).

### 7.4 Modals (adaptateur)

| Modal | Champs |
|---|---|
| Invite | select invité ; validité 3/5/15/30 min (défaut 5) ; map optionnelle (pool actif) |
| Report résultat | select vainqueur |
| Annulation | raison (obligatoire) |
| Préférences | multi-select favs (max `player_fav_count`), bans (max `player_ban_count`), disjoints |
| Settings admin | tous les settings §2 avec bornes de validation |
| Set game match ref | ID de partie (parsing tolérant, ex. `123`, `#123`, scheme URL) |
| Map edit / import | name, filename, description, resource_url / textarea `name:filename` par ligne |
| Rating adjust | joueur, ±N, motif |

### 7.5 Nettoyage

Tâche périodique (300 s) : demander à la plateforme la suppression des surfaces de match terminées/annulées plus vieilles que `match_surface_cleanup_delay` (avec message final d'annonce). Les données restent intégralement en base.

## 8. Tâches de fond

| Tâche | Cadence | Rôle |
|---|---|---|
| Matchmaking tick | `matchmaking_tick_interval` (5 s) / ladder | §5.1, lock Redis |
| Expiration deadlines | dans le tick | annulation des CREATED expirés |
| Cleanup surfaces | 300 s | §7.5 |
| Auto-report | on-demand après RESULT_PENDING (5 s × 30 s) | via gateway |
| Recalcul ranks | après confirmation (ZSET incrémental) + 60 s | leaderboard |

## 9. Critères d'acceptation

1. **Indépendance jeu** : tous les tests cœur passent avec un `GameGateway` mocké sans capacités (pas de temps réel, pas de résultat auto) — parcours complet : inscription → file → match → report manuel → confirmation → rating.
2. **Indépendance plateforme** : aucune collection du mod ne contient d'ID/URL de message ou de surface ; le registry plateforme est la seule localisation des IDs ; remplacer l'adaptateur par une plateforme mock ne casse aucune règle métier.
3. Deux joueurs à Δrating ≤ base → match < 2 s après l'arrivée du second ; à ±150 → ~1 min ; jamais appariés au-delà du cap (mais informés).
4. Aucun joueur appariable laissé seul si un matching complet existe ; cas 2 joueurs toujours appariés dès compatibilité.
5. Rating appliqué exactement une fois ; bornes K/delta/floor respectées ; invariant "somme des deltas = rating courant" vérifiable ; corrections admin tracées et compensées.
6. Admin gère maps + pools + settings intégralement depuis la plateforme, sans accès DB ; switch de pool transactionnel, notifié, préférences nettoyées, audité.
7. Toutes les transitions idempotentes (rejeu d'événements sans effet de bord) ; le délai de grâce "lobby fermé" géré côté adaptateur jeu.
8. Non-admin : aucune mutation admin possible ni visible.
