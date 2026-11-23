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
- **Then** rien n'est persisté (aucune collection Mongo/Redis n'est touchée)

Implémenté par `test_SC_PONG_002_register_no_consent`.

### SC-PONG-003 — inscription à la saison

- **Given** un joueur enregistré (`pong_candidate`), la saison active
- **When** il fait `/register_to_tournament` (« AOE Pong S<N> »)
  avec `rules: True` et le déclaratif de disponibilités
- **Then** il est inscrit (trace de la version du règlement acceptée)
  et reçoit `pong_player`

Implémenté par `test_SC_PONG_003_register_to_tournament`.

### SC-PONG-004 — ouverture de ronde : salons + ban civs

- **Given** une saison active avec N tables et des joueurs répartis
- **When** un admin lance l'op console d'ouverture de ronde
- **Then** chaque table a son salon provisionné (panneau : joueur A
  premier annoncé, B l'autre, rappel A host des deux drafts), le ban
  civs automatisé laisse exactement `civs_remaining` (15) civs
  disponibles **par table** (seed persistée ronde+table pour audit),
  le preset draft-civ par table est affiché, et l'annonce du mercredi
  est postée

Implémenté par `test_SC_PONG_004_open_round`.

### SC-PONG-005 — mouvement montée/descente après résultat validé

- **Given** des tables 1..N, un résultat validé sur la table T
- **When** la ronde suivante est calculée
- **Then** le gagnant monte d'une table, le perdant descend, selon la
  `edge_policy` configurée (cas aux bornes tranchés par la valeur de
  config, pas par le code)

Implémenté par `test_SC_PONG_005_climb_fall`.

### SC-PONG-006 — table bloquée à la montée/descente

- **Given** la table T+1 bloquée à la montée (RG-TAB-2) par un admin
- **When** le gagnant de la table T aurait dû y monter
- **Then** il reste à sa table (le blocage empêche le mouvement, loggé
  avec l'auteur de la mutation)

Implémenté par `test_SC_PONG_006_blocked_table`.

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
- **Then** le résultat passe `VALIDATED`, les vues ronde/classement se
  mettent à jour, et la re-validation est idempotente (log sans effet)
- **When** le second joueur fait `/contest_score`
- **Then** le résultat passe `CONTESTED` et les admins sont taggés

Implémenté par `test_SC_PONG_009_validate_contest`.

### SC-PONG-010 — étranger à la table refusé

- **Given** une table T et le joueur X, étranger (ni A ni B)
- **When** le joueur X tente `/add_result` sur T
- **Then** refus (garde : auteur ∈ {A, B} de la table, ronde ouverte)

Implémenté par `test_SC_PONG_010_outsider`.

### SC-PONG-011 — draft interne : trois bans de catégorie

- **Given** la draft menée dans les surfaces du mod
  (`panel:mod:pong:table:draft`, si retenue en DECISIONS)
- **When** un joueur ban ses 4 premières maps dans 2 catégories
  différentes (3 premiers bans pas tous de même catégorie)
- **Then** la draft est invalidée et doit être refaite à partir du
  début (RG-MDRAFT-2)

Implémenté par `test_SC_PONG_011_draft_category_bans`.

### SC-PONG-012 — map neutre première jouée

- **Given** une draft map terminée sur la table T
- **When** la série commence
- **Then** la dernière map choisie dans la draft est affichée comme
  map neutre, première jouée (RG-MDRAFT-1)

Implémenté par `test_SC_PONG_012_neutral_map`.

### SC-PONG-013 — signaler un preset de civs

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

> **À DÉFINIR** : les scénarios des surfaces de draft interne et du
> zip de records (RG-REC-1) attendent les décisions DECISIONS (mode
> draft, upload de records). Chaque nouvelle règle automatisable
> ajoutée à RULES.md arrive avec son scénario dans le même PR.
