# Pong — Decisions

Les décisions validées priment sur tout le reste du doc set (règle de la
plateforme : voir docs/MODS/README.md — si c'était discuté, c'est écrit
ici, daté). Les décisions marquées **ouverte** sont les questions de
design en attente du mod owner.

## 2026-11-23 — Bootstrap du mod

- **D-PONG-001** — `pong` est un **mod distinct** de `ladder` : la
  ladder (queue Elo, matchmaking blossom, botforge-services#15) et le
  pong (tournoi à tables montée/descendante, saison à rondes
  hebdomadaires) coexistent ; aucun des deux n'est dérivé de l'autre.
  Validé par Aramatu (mod owner), session du 2026-11-23.
- **D-PONG-002** — La **source fonctionnelle** du mod est le règlement
  officiel du tournoi AOE Pong (S5, « Antre de l'Ours »), fourni par
  Aramatu et archivé tel quel dans [REFERENCE.md](REFERENCE.md) —
  même pattern que la référence JeanJack V2.0 du mod ladder.
- **D-PONG-003** — Le mod est **game-bound AoE2** (`game_key: aoe2`,
  comme kingdoms) : presets de draft et formats BO sont liés à AoE2 ;
  catalogue de civs/maps/pools lu via `GameDataService` (jamais
  dupliqué).
- **D-PONG-004** — Les décisions à discrétion humaine du règlement
  (admin win/loose, arbitrage de litiges, refus d'inscription,
  politique de patch, sanctions) restent **constat par le bot,
  décision humaine** : le mod fournit les documents et fils de faits
  horodatés, les admins arbitrent via la console.

## 2026-11-23 — Réponses du mod owner (questions de design)

- **D-PONG-005 (ex Q-PONG-001)** — `rounds_per_season` = **4** (la
  contradiction de la source S5 est tranchée : 4 rondes).
- **D-PONG-006 (ex Q-PONG-002)** — **Deux politiques de mouvement**
  (`move_policy`, paramètre de saison) :
  1. **`classic`** — le gagnant monte, le perdant descend (une table) ;
  2. **`semi_blocked`** — les tables sont regroupées 2 par 2 (3 pour le
     dernier groupe si le nombre de tables est impair) ; les
     montées/descentes se gèrent **au sein de chaque groupe**
     uniquement (ex. groupe {T1, T2} : gagnant de T1 reste en T1,
     perdant de T1 va en T2, gagnant de T2 va en T1, perdant de T2
     reste en T2). Aucun mouvement inter-groupe.
- **D-PONG-007 (ex Q-PONG-003)** — **Attribution A/B** : le joueur A
  est le joueur assis au **premier emplacement** de la table. Chaque
  joueur est classé par son **seed elo** =
  `(2 × Elo actuel + Elo max) / 3`, calculé **à l'inscription**. Ronde 1 :
  A = le mieux classé des deux. Rondes suivantes : **le joueur qui
  monte prend l'emplacement B, le joueur qui descend prend
  l'emplacement A** (le gagnant monte en B, le perdant descend en A).
- **D-PONG-008 (ex Q-PONG-004)** — **Nombre de tables = nombre de
  joueurs / 2**, provisionné à l'ouverture de saison (ou de ronde,
  à trancher en implémentation). Cas **impair** : deux pistes posées
  par le mod owner — un joueur **remplaçant** qui entre/sort du
  tournoi selon l'effectif, ou une gestion des tables **à 3+** ; la
  question reste ouverte (Q-PONG-002 ci-dessous).
- **D-PONG-009 (ex Q-PONG-005)** — **Drafts externes via aoe2cm** :
  la draft map utilise un simple preset (le map pool) ; la draft civ
  est **dérivée d'un `base_preset`** (génération automatisée — le mod
  owner fournit son code Python actuel de génération ; source aoe2cm :
  https://github.com/SiegeEngineers/aoe2cm2). La règle des 3 bans =
  1 catégorie reste **constat déclaratif** (bouton de signalement →
  tag admin), la plateforme externe n'étant pas pilotable par le bot.
- **D-PONG-010 (ex Q-PONG-006)** — **Records automatiques** : le mod
  génère le zip des records en allant chercher les parties des joueurs
  (piste : https://replaypacker.zeta-two.com) pour que les casters
  aient toujours les 5 records d'un BO5 **sans spoiler**, avec un
  message affichant la draft map et la draft civ. Feature visée phase
  2 (dépend du provider de records).
- **D-PONG-011 (ex Q-PONG-007)** — **Scores hors format**, trois cas
  distincts :
  1. **Forfait** — un joueur se déclare forfait sur sa table : il
     entre un résultat « perdu », l'autre joueur valide, terminé
     (format dédié `/add_result --forfeit` ou équivalent, pas de
     manipulation du score) ;
  2. **Pas de rdv trouvé** — deux joueurs qui n'arrivent pas à
     planifier : **trancher est réservé à l'admin** de la compétition
     (admin win/arbitrage via console) ;
  3. **Match partiellement joué / abandon en cours de set** —
     autorisé : l'abandon donne les victoires restantes à
     l'adversaire (score complété, déclaration normale + validation).

## Ouvertes

- **Q-PONG-002 (issue de l'impair, ex Q-PONG-004)** — effectif joueur
  impair : joueur remplaçant qui entre/sort du tournoi selon
  l'effectif, ou tables à 3 (ou plus) avec une politique de
  mouvement adaptée ? À trancher avant l'ouverture de la première
  saison (l'ouverture de saison avec effectif impair reste bloquée
  jusqu'à décision).
