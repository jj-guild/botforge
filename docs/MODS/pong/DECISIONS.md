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

## Ouvertes (questions du mod owner)

- **Q-PONG-001** — Nombre de rondes par saison : la source S5 est
  contradictoire (six rondes annoncées en présentation, quatre rondes
  datées). Valeur attendue pour `rounds_per_season` (config, défaut
  proposé : 6 en présentation standard, S5 avait 4).
- **Q-PONG-002** — Politique aux bornes (`edge_policy`) : le gagnant
  de la dernière table monte-t-il ? le perdant de la première
  descend-il ? (proposition : le gagnant de la dernière reste, le
  perdant de la première reste).
- **Q-PONG-003** — Clé d'attribution A/B (`table_order_key`) : le
  joueur A (hôte des deux drafts) est « le premier joueur annoncé » —
  premier annoncé selon quel tri ? (seed aléatoire ? elo ? place de la
  ronde précédente ?).
- **Q-PONG-004** — Nombre de tables (`tables_count`) par défaut.
- **Q-PONG-005** — Draft map/civ **interne au mod** (buttons du bot,
  vérif RG-MDRAFT-2 automatisée) vs **externe aoe2cm** (lien du
  preset seulement, constat déclaratif). Impacte
  `panel:mod:pong:table:draft` et SC-PONG-011.
- **Q-PONG-006** — Records : upload du zip des drafts/recs **par
  bouton** dans le salon records vs lien externe. Impacte RG-REC-1.
- **Q-PONG-007** — Tolérance des scores hors format BO (forfaits,
  scores admin) : refus strict + correction console, ou format
  « admin » dédié.
