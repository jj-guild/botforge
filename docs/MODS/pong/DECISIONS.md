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
  à trancher en implémentation). Cas **impair** : résolu par la
  chaîne de parité (D-PONG-019).
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
     (format dédié `/add_result --forfait` ou équivalent, pas de
     manipulation du score) ;
  2. **Pas de rdv trouvé** — deux joueurs qui n'arrivent pas à
     planifier : **trancher est réservé à l'admin** de la compétition
     (admin win/arbitrage via console) ;
  3. **Match partiellement joué / abandon en cours de set** —
     autorisé : l'abandon donne les victoires restantes à
     l'adversaire (score complété, déclaration normale + validation).

## 2026-11-23 — Session 2 : flexibilité, seed humain, flux de joueurs

- **D-PONG-012 — Format v1 conservé + alternance + grâce ±3 jours.**
  La v1 reste le format hebdo (1 match par semaine, fenêtre
  mercredi → mardi), avec deux assouplissements :
  1. **`move_policy` alterne par saison** : S1 `classic`, S2
     `semi_blocked`, S3 `classic`… (paramètre de saison automatique,
     D-PONG-006 conserve sa définition) ;
  2. **Grâce ±3 jours** par ronde : le calcul de l'appariement
     suivant se fait sur les résultats **validés à l'échéance** de la
     ronde ; un match joué pendant la grâce compte immédiatement
     (récap), et son mouvement s'applique à la ronde suivante
     (**mouvement différé d'une ronde**).
- **D-PONG-013 — Seed humain à l'inscription.** En plus du seed
  ladder (formule D-PONG-007), le joueur **autodéclare son niveau**
  (« je joue au-dessus/en-dessous de mon Elo ladder ») ; l'admin peut
  **corriger le seed d'un joueur** avant le tirage et entre les
  rondes (console, constat → décision humaine). Les seeds ne sont
  jamais affichés aux joueurs.
- **D-PONG-014 — Pas de classement global ; récap personnel.**
  Objectif du tournoi : un cadre compétitif **sans pression**
  (pas de cash prize, focus progression et bienveillance). Aucun
  classement, leaderboard, podium ou score comparatif n'est publié.
  Chaque joueur accède à son **récap personnel par saison** (sets
  disputés, W/L, adversaires, parcours de tables) : **à la demande,
  via une réponse `ephemeral` de la commande `/recap`** (visible
  uniquement du demandeur), et **en DM privé à la clôture de la
  saison** (récap final). Un joueur qui quitte en cours de saison :
  récap clôturé sur ses sets disputés, aucune remise en ordre.
  L'ordre des tables existe uniquement comme **donnée interne**
  (`chain_position`) : noms de tables neutres, messages joueurs sans
  mention de montée/descente ou de position.
- **D-PONG-015 — Inscription tardive = file d'attente.** La fenêtre
  d'inscription se ferme à l'ouverture de la ronde 1. Après : le
  candidat passe en **`waitlist`** ( état mod). Le **binomage** des
  candidats en duos d'insertion est décidé **par l'admin** (pas de
  tolérance automatique de niveau).
- **D-PONG-016 — Tables « et-demi » théorisées (insertion locale).**
  Un duo validé entre comme **table pleine insérée dans la chaîne
  entre les deux tables qui encadrent son niveau** : le bot propose
  le point d'insertion, l'admin valide. L'insertion est possible **en
  cours de ronde** (le duo joue entre lui dès la ronde en cours,
  zéro impact sur les autres tables) et prend effet dans la chaîne de
  mouvement à la ronde suivante, avec **renumérotation
  automatique**. Effet strictement local : les voisins changent
  seulement de voisin de mouvement, aucun re-shuffle global.
- **D-PONG-017 — Départs.** Notification → le bot dresse le dossier
  (dates, matchs joués, match en attente — constat) → validation
  admin en console. Les **résultats déjà validés restent acquis**
  pour les adversaires. La place du partant est proposée **d'abord à
  la file d'attente**, au **créneau exact** dans la chaîne (pas de
  re-shuffle). Un départ pendant une ronde avec match en attente =
  **forfait (défaite)** pour le partant, l'adversaire valide et avance
  (D-PONG-011 cas 1).
- **D-PONG-018 — Match volontaire (absorption d'orphelin).** Sans
  remplaçant, le bot propose aux **joueurs voisins (par proximité)**
  un match d'appoint **volontaire** contre l'orphelin. Ce match est
  **récap-only : aucun mouvement** dans les deux sens (les
  mouvements ne se calculent que sur les matchs de table,
  RG-TAB-1).
- **D-PONG-019 — Chaîne de parité (résout Q-PONG-002).** L'effectif
  jouable n'est **jamais impair** ; chaque niveau absorbe le suivant :
  1. les arrivées sont **binômées** (un isolé attend un partenaire) ;
  2. un départ est **comblé au créneau exact** par la file ;
  3. sans remplaçant : **match volontaire récap-only** (D-PONG-018) ;
  4. dernier recours : le **fusible** — un volontaire de la file
     d'abord, l'admin ensuite.
  Les tables à 3 sont exclues. La question Q-PONG-002 est close.

## Ouvertes

- (aucune — les questions Q-PONG-001..007 sont résolues par
  D-PONG-005..011, Q-PONG-002 par D-PONG-019.)
