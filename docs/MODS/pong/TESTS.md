# Pong — Mod test scenarios

Liste des scénarios qui valident/sécurisent l'implémentation. **Chaque
scénario a exactement un test automatisé**, écrit par l'agent dans
`modules/mods/pong/tests/test_scenarios.py` (botforge-services), joué
par la CI (`pytest tests modules/mods/pong/tests/test_scenarios.py`),
et recoupé par la validation des docs (`validate_docs.py` échoue quand
un scénario documenté n'a pas de test).

## Format de scénario

- un id par scénario, `SC-PONG-NNN` ;
- scénario dans le même PR que la règle et le test qui l'implémentent ;
- le docstring du test porte l'id, pour que doc et code restent appariés.

## Scenarios

### SC-PONG-001 — enregistrement joueur avec consentement

- **Given** un utilisateur Discord non enregistré, un profil AoE2
  résolu par le core (steam_id, pays, elo)
- **When** il fait `/register` et accepte la privacy gate
- **Then** le joueur est enregistré (discord_id ↔ steam_id liés, données
  AoE2 lues via le core, non dupliquées) et le rôle `pong_candidate`
  lui est attribué

Implémenté par `test_SC_PONG_001_register_with_consent` dans
`test_scenarios.py`.

### SC-PONG-002 — enregistrement sans consentement refusé

- **Given** un utilisateur non enregistré
- **When** il fait `/register` et refuse la privacy gate
- **Then** rien n'est persisté (aucune collection Mongo/Redis touchée)

Implémenté par `test_SC_PONG_002_register_no_consent`.

### SC-PONG-003 — inscription à la saison : seed ladder + seed humain

- **Given** un joueur enregistré (`pong_candidate`), la saison active
- **When** il fait `/register_to_tournament` (« AOE Pong S<N> »)
  avec `rules: True`, le déclaratif de disponibilités **et son
  autodéclaration de niveau** (seed humain)
- **Then** il est inscrit (trace de la version du règlement acceptée),
  reçoit `pong_player`, son **seed elo** est calculé :
  `(2 × Elo actuel + Elo max) / 3` (D-PONG-007) et son seed humain
  enregistré (D-PONG-013) — aucun des deux n'est jamais affiché au
  joueur

Implémenté par `test_SC_PONG_003_register_to_tournament`.

### SC-PONG-004 — ouverture de ronde : salons neutres + ban civs

- **Given** une saison active avec N tables et des joueurs répartis
- **When** un admin lance l'op console d'ouverture de ronde
- **Then** chaque table a son salon provisionné (panneau : joueur A
  premier emplacement, B l'autre, rappel A host des deux drafts), le ban
  civs automatisé laisse exactement `civs_remaining` (15) civs
  disponibles **par table** (seed persistée ronde+table pour audit),
  le preset draft-civ par table est affiché, et l'annonce du mercredi
  est postée — **noms de tables neutres, aucune position ni
  montée/descente dans les messages joueurs, liste non ordonnée**
  (D-PONG-014, RG-TAB-5)

Implémenté par `test_SC_PONG_004_open_round`.

### SC-PONG-005 — mouvement classic après résultat validé

- **Given** des tables 1..N, `move_policy: classic`, un résultat
  validé sur la table T (2 < T < N-1)
- **When** la ronde suivante est calculée
- **Then** le gagnant monte d'une table, le perdant descend d'une
  table ; à la ronde suivante le montant occupe l'emplacement B et le
  descendant l'emplacement A (D-PONG-007)

Implémenté par `test_SC_PONG_005_climb_fall_classic`.

### SC-PONG-006 — mouvement semi_blocked : groupes de 2 tables

- **Given** `move_policy: semi_blocked`, 5 tables → groupes {T1,T2},
  {T3,T4}, {T5} (le dernier groupe prend l'impair), un résultat
  validé sur T3 et un sur T4
- **When** la ronde suivante est calculée
- **Then** les mouvements se font au sein de chaque groupe uniquement :
  gagnant de T3 reste en T3 (place B), perdant de T3 va en T4 (place
  A), gagnant de T4 va en T3, perdant de T4 reste en T4 ; aucun
  mouvement inter-groupe (D-PONG-006)

Implémenté par `test_SC_PONG_006_move_semi_blocked_groups`.

### SC-PONG-007 — déclaration de résultat valide

- **Given** une ronde ouverte, la table T avec joueurs A et B
- **When** le joueur A fait `/add_result` avec « 3-2 »
- **Then** le résultat est créé `PENDING` ; le joueur B est invité à
  valider ou contester

Implémenté par `test_SC_PONG_007_add_result`.

### SC-PONG-008 — score hors format refusé

- **Given** `bo_format` = 5 (BO5)
- **When** un joueur déclare « 4-2 » (X+Y > 5)
- **Then** la déclaration est refusée avec le motif (hors format BO5),
  rien n'est persisté

Implémenté par `test_SC_PONG_008_bad_score`.

### SC-PONG-009 — validation et contestation

- **Given** un résultat `PENDING`
- **When** le second joueur fait `/validate_score`
- **Then** le résultat passe `VALIDATED`, les vues de ronde se mettent
  à jour, le récap personnel du joueur est alimenté (D-PONG-014), et
  la re-validation est idempotente (log sans effet)
- **When** le second joueur fait `/contest_score`
- **Then** le résultat passe `CONTESTED` et les admins sont taggés

Implémenté par `test_SC_PONG_009_validate_contest`.

### SC-PONG-010 — étranger à la table refusé

- **Given** une table T et le joueur X, étranger (ni A ni B)
- **When** le joueur X tente `/add_result` sur T
- **Then** refus (garde : auteur ∈ {A, B} de la table, ronde ouverte)

Implémenté par `test_SC_PONG_010_outsider`.

### SC-PONG-011 — preset civ dérivé du base_preset

- **Given** le `civ_draft_base_preset` de la saison et une table ouverte
- **When** le mod génère le preset draft-civ de la table
  (D-PONG-009 : dérivation depuis le base_preset)
- **Then** le preset affiché ne contient que `civs_remaining` (15)
  civs, cohérentes avec le ban automatisé au seed persisté (la
  génération est re-traçable : même ronde+table ⇒ même preset)

Implémenté par `test_SC_PONG_011_civ_preset_derivation`.

### SC-PONG-012 — map neutre première jouée

- **Given** une draft map terminée sur la table T (aeo2cm, externe)
- **When** la série commence
- **Then** la dernière map choisie dans la draft est affichée comme
  map neutre, première jouée (RG-MDRAFT-1)

Implémenté par `test_SC_PONG_012_neutral_map`.

### SC-PONG-013 — contester un preset de civs

- **Given** le panneau de table avec bouton de signalement
- **When** un joueur signale « preset avec > 2 civs non possédées »
- **Then** les admins sont taggés avec la table et le preset (le mod
  constate, la relance est une décision admin)

Implémenté par `test_SC_PONG_013_report_preset`.

### SC-PONG-014 — clôture de ronde et fermeture des salons

- **Given** la fenêtre de ronde écoulée (mercredi → mardi)
- **When** la passe de clôture tourne
- **Then** les salons de tables sont fermés/archivés
  (`close_tables`), les résultats `PENDING` restants sont listés dans
  un fil de faits pour arbitrage admin, et le rapport de passe est
  posté (jamais en log seul)

Implémenté par `test_SC_PONG_014_close_round`.

### SC-PONG-015 — self-heal des salons et pins au boot

- **Given** un salon de table supprimé pendant une ronde ouverte
- **When** la passe de boot s'exécute
- **Then** le salon est recréé, le pin `menu:mod:pong:home` rétabli,
  sans exception non rendue (rapport posté dans `pong:announcements`)

Implémenté par `test_SC_PONG_015_selfheal`.

### SC-PONG-016 — forfait déclaré et validé

- **Given** une ronde ouverte, la table T ; le joueur A prévient qu'il
  est forfait sur la discussion de sa table
- **When** il saisit le résultat forfait (« perdu ») et que le joueur B
  valide (`/validate_score`)
- **Then** le résultat est **validé sans manipulation du score**
  (D-PONG-011 cas 1), le mouvement RG-TAB s'applique

Implémenté par `test_SC_PONG_016_forfeit`.

### SC-PONG-017 — abandon en cours de set

- **Given** un BO5 partiellement joué (ex. 1-1), le joueur A abandonne
  le set
- **When** le résultat est saisi avec les victoires restantes données
  à l'adversaire (ex. 1-3) et validé
- **Then** le résultat est accepté (D-PONG-011 cas 3 : les abandons en
  cours de set sont autorisés, les victoires restantes vont à
  l'adversaire)

Implémenté par `test_SC_PONG_017_mid_set_abandon`.

### SC-PONG-018 — pas de rdv trouvé : arbitrage admin

- **Given** une table sans planification possible à la clôture de
  ronde (aucun résultat, topic de planification vide)
- **When** la clôture liste les faits et l'admin applique un admin win
  via la console
- **Then** le résultat admin est persisté avec l'auteur de la décision
  (D-PONG-011 cas 2 : trancher est réservé à l'admin, jamais au bot)

Implémenté par `test_SC_PONG_018_admin_no_schedule`.

### SC-PONG-019 — inscription après clôture : file d'attente

- **Given** la ronde 1 ouverte (fenêtre d'inscription fermée), un
  joueur `pong_candidate` qui fait `/register_to_tournament`
- **When** la commande est traitée
- **Then** l'inscription à la saison est refusée avec un message
  explicite, le joueur passe en **`waitlist`** (rôle `pong_waitlist`,
  D-PONG-015) ; aucun joueur actif n'est modifié

Implémenté par `test_SC_PONG_019_waitlist`.

### SC-PONG-020 — insertion d'un duo (« table et-demi », D-PONG-016)

- **Given** deux candidats en `waitlist` binômés par l'admin, une
  ronde en cours, une chaîne de tables avec `chain_position`
- **When** le bot propose le point d'insertion et l'admin le valide
  (console, confirm card)
- **Then** le duo joue **entre lui** dès la ronde en cours (aucune
  autre table modifiée), la table prend sa place dans la chaîne à la
  ronde suivante avec **renumérotation automatique** ; seuls les
  voisins directs changent d'interlocuteur de mouvement ; l'opération
  est loggée

Implémenté par `test_SC_PONG_020_duo_insertion`.

### SC-PONG-021 — départ comblé au créneau exact (D-PONG-017)

- **Given** un joueur qui quitte entre deux rondes, un volontaire en
  `waitlist`, des résultats déjà validés impliquant le partant
- **When** l'admin valide le retrait en console (dossier de faits)
- **Then** le partant passe `departed` (récap clôturé), **ses
  résultats validés restent acquis** aux adversaires, et le
  volontaire prend **le créneau exact** dans la chaîne (`replacing`) :
  aucune autre table n'est re-shufflée

Implémenté par `test_SC_PONG_021_departure_slot_swap`.

### SC-PONG-022 — orphelin sans remplaçant : match volontaire recap-only (D-PONG-018/019)

- **Given** un départ validé sans volontaire en `waitlist`, les
  joueurs des tables voisines
- **When** le bot propose un match d'appoint et un voisin accepte
- **Then** le match est joué et validé **récap-only** : il compte
  dans les récaps des deux joueurs (DM privé), **aucun mouvement de
  table** ne s'applique (RG-TAB-1) ; l'orphelin reste à sa place ;
  dernier recours fusible : volontaire de la file, puis admin

Implémenté par `test_SC_PONG_022_orphan_volunteer_match`.

### SC-PONG-023 — grâce ±3 jours : mouvement différé (D-PONG-012)

- **Given** une ronde à l'échéance avec un résultat `PENDING`, et la
  ronde suivante appariée sur les résultats validés
- **When** le match est joué pendant la grâce et validé
- **Then** le récap des joueurs est mis à jour immédiatement, et le
  mouvement de table s'applique **à la ronde suivante** (différé
  d'une ronde : le montant/descendant bouge un cycle plus tard)

Implémenté par `test_SC_PONG_023_grace_deferred_move`.

### SC-PONG-024 — récap personnel en DM, aucun classement global (D-PONG-014)

- **Given** une saison avec des résultats validés, un joueur qui
  demande son récap (ou la fin de saison)
- **When** le récap est généré
- **Then** le joueur reçoit **en DM privé** ses sets disputés, W/L,
  adversaires et parcours de tables ; **aucun classement global,
  tableau comparatif ou podium n'est publié** sur le serveur ; les
  tables sont listées sans ordre de niveau (RG-TAB-5)

Implémenté par `test_SC_PONG_024_personal_recap_dm`.

> Les records auto (D-PONG-010, phase 2 — provider de zip sans spoiler)
> arrivent avec leur scénario dans le PR qui les implémente. Chaque
> nouvelle règle automatisable ajoutée à RULES.md arrive avec son
> scénario dans le même PR.
