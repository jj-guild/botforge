# Pong — Mod Rules

Règles du jeu appliquées par le mod, extraites de
[REFERENCE.md](REFERENCE.md) (règlement AOE Pong). Chaque règle est écrite
pour être automatisable : testable ou vérifiable par le bot. Les zones à
discrétion admin sont classées **constat, décision humaine** : le bot
rapporte les faits (tags, timestamps, états), l'admin tranche.

## RG-REG — Enregistrement et inscription

### RG-REG-1 — Enregistrement joueur

`/register` (salon `pong:bot-commands`) enregistre le joueur : lien
`steam_id` ↔ `discord_id` plus les données AoE2 du core (pays, elo)
**lues via le profil game — jamais recopiées dans les collections du mod**.
La commande exige un consentement explicite (privacy gate) avant
persistance ; sans consentement, refus.

- **Cas limites** : discord_id déjà enregistré → proposition de liaison au
  profil existant ; steam_id déjà pris par un autre joueur → refus +
  notification admin.
- Manuel sinon : rien n'est déduit, l'admin arbitre.

### RG-REG-2 — Inscription à la saison

`/register_to_tournament` avec le nom de la saison active + validation
`rules: True` (acceptation du règlement tracée avec la version du
règlement acceptée). Le mod exige : RG-REG-1 réussi, présence
discord (= pas de vérification supplémentaire), et le déclaratif
« 2 disponibilités de 3h consécutives dans 17h-23h » capté à
l'inscription. Toute modification d'inscription doit être notifiée à un
admin : le mod fournit `/update_entry` qui tagge les admins.

- **Refus d'inscription** : décision humaine (le mod n'accepte ni ne
  refuse seul), il expose le bouton admin correspondant.

## RG-STRUC — Structure de saison

### RG-STRUC-1 — Rondes

Une saison compte `rounds_per_season` rondes (config, source S5
contradictoire : 4 ou 6 — voir DECISIONS), chacune d'une durée
`round_window` (défaut 7 jours, mercredi → mardi). Le BO est
`bo_format` (défaut BO5). À l'ouverture d'une ronde, le mod crée le
salon de chaque table, y annonce joueurs A/B, preset et ronde ;
à la clôture, il ferme les salons (config `close_tables`).

### RG-STRUC-2 — Attribution A/B et rôles de draft

Sur chaque table, le joueur A est le premier annoncé, le joueur B
l'autre. Le joueur A est host de la draft map **et** de la draft civ :

- automatiquement affiché en tête du salon de table (l'ordre A/B est
  calculé par le mod — **À DÉFINIR** : clé de tri (seed, elo, place
  de la ronde précédente) à trancher en DECISIONS) ;
- la convention « A host » est rappelée dans le panneau de table.

## RG-TAB — Tables et montée/descente

### RG-TAB-1 — Mouvements

Règle centrale (« comme au ping pong ») : **le gagnant d'une ronde monte
d'une table, le perdant descend**, sur `tables_count` tables. Les
mouvements sont calculés après validation du résultat (RG-RES-3), au
moment de l'ouverture de la ronde suivante. **À DÉFINIR** :
comportement exact aux bornes (le gagnant de la dernière table
monte-t-il ? le perdant de la première descend-il ?) et interaction
avec les tables bloquées (RG-TAB-2) — tranchés par `edge_policy`
(config, DECISIONS).

### RG-TAB-2 — Blocage de tables

L'admin peut **bloquer des tables à la montée ou à la descente** pour
éviter les (re)matchs : un joueur « bloque » à sa table plutôt que
d'en changer si la table cible est bloquée pour son sens de mouvement.
Opération console admin (`mod="pong"`), confirm card, log de cette
mutation, appliquée au calcul de la ronde suivante.

## RG-CDRAFT — Civilisations

### RG-CDRAFT-1 — Ban civs automatisé par table

Au début de chaque ronde, **pour chaque table**, le mod ban de façon
automatisée et aléatoire le nombre requis pour qu'il reste exactement
`civs_remaining` (défaut 15) civilisations disponibles, et communique
le preset draft-civ lié à la table.

- Aléatoire **re-traçable** (seed persistée par ronde+table pour audit et
  rejouabilité).
- Source des civilisations : `GameDataService` (core) — le mod ne
  duplique jamais le catalogue de civs.

### RG-CDRAFT-2 — Preset injouable

Si le preset draft-civ d'une table contient plus de deux civilisations
que le joueur ne possède pas, le joueur peut demander une nouvelle
draft (bouton signal sur la table → tag admin). Décision de relance :
humaine (admin) ; la nouvelle draft passe par RG-CDRAFT-1.

## RG-MDRAFT — Draft map et choix des maps

### RG-MDRAFT-1 — Draft normalisée (aeo2cm)

Draft map et draft civ se déroulent « comme dans tous les autres
tournois » sur le preset externe (aeo2cm, ex. S5 :
`https://aoe2cm.net/preset/pGWoJ`, preconfig `draft_map_preset`).
La **dernière map choisie** dans la draft est la **map neutre**, jouée
en premier : le mod l'affiche tel quel dans le panneau de table.

### RG-MDRAFT-2 — Les trois premiers bans = une catégorie

Dans la draft map, les **trois premiers bans de chaque joueur** doivent
concerner des maps de la **même catégorie** (ban de catégorie). Toute
draft ne respectant pas cette règle est **non valide et doit être
refaite à partir du début**.

- Vérifiable **dans le mod uniquement si la draft est menée dans ses
  surfaces** : le mod héberge alors la draft (boutons de draft par
  table, vue `panel:mod:pong:table:draft`) et invalide + relance
  automatiquement ; si la draft reste sur aoe2cm (externe), la vérif
  est déclarative : le poste de draft sur la table porte un bouton
  « draft non conforme » visible qui tagge un admin (constat,
  décision humaine).
- **À DÉFINIR** (DECISIONS) : draft interne au mod vs externe en phase 1.

### RG-MDRAFT-3 — Choix de la map suivante

Le **perdant** de la partie précédente choisit la map suivante parmi
**toutes les maps disponibles** (pas déjà jouées), y compris celles
draftées par son adversaire.

- Si le mod héberge la série (suivi des parties de la table), il
  affiche les maps restantes et le tour du perdant ; sinon, rappel
  déclaratif dans le panneau.

## RG-RES — Résultats

### RG-RES-1 — Déclaration

`/add_result` **sur le salon de la table** : joueur A, score `X-X`
(**score A à gauche, score B à droite**), joueur B. Validations :

- auteur ∈ {joueur A, joueur B} de la table, ronde ouverte ;
- format score `^[0-9]+-[0-9]+$`, compatibilité avec `bo_format`
  (BO5 : X+Y ≤ 5, max(X,Y) = 3 → **À DÉFINIR** : tolérance admin pour
  les scores hors format (forfaits), tranchée en config).

### RG-RES-2 — Validation ou contestation

Le **second joueur** (celui qui n'a pas déclaré) est invité à valider
via `/validate_score` ou contester via `/contest_score` **qui tagge un
admin**. Sans validation, le résultat reste `PENDING` jusqu'à un
traitement admin (constat, décision humaine). Après contestation :
l'admin tranche via la console (valider/invalider/redéclarer).

### RG-RES-3 — Enregistrement et mouvement

Un résultat **validé** (ou arbitré admin) est persisté et déclenche
RG-TAB-1 (montée/descente de la table), puis la mise à jour des vues
de ronde et du classement global. Idempotent : re-valider un résultat
déjà validé est sans effet (log seulement).

## RG-REC — Records et casting

### RG-REC-1 — Format de post des records

Pour faciliter casting et arbitrage, chaque match est accompagné d'un
message de résultat au format exact
`AOE Pong Ronde X Table X : Pseudo1 || Score || Pseudo2` et d'un zip
contenant le fichier « Drafts » (drafts maps + civs) et les parties
`AOEPong_Pseudo1_vs_Pseudo2_Game_X.aoe2rec`.

- Le mod génère le gabarit de message (bouton sur la table) et fournit
  un salon de records ; la collecte physique des fichiers reste
  humaine (**À DÉFINIR** : upload de zip par bouton vs lien externe,
  DECISIONS).

### RG-REC-2 — Open stream

Open stream par défaut (config `open_stream`, défaut vrai) : tout
caster peut caster ; le titre doit contenir « AOE Pong ». Le mod
propose l'annonce de cast sur la table (salon `pong:casting`, rôle
`pong_caster`) mais ne vérifie pas les titres de stream (hors
périmètre bot).

## RG-ADM — Commandes admin (constat, décision humaine)

Le mod fournit les documents et boutons, la décision reste humaine :

- **Admin Win / Admin Loose** : retard > 30 min (timestamp d'ouverture
  de table horodatée + rappel), replanification < 24h du créneau
  initialement prévu (planning gardé par la section de planification de
  la table), non-planification à la clôture de ronde → le mod liste
  les faits horodatés sur la table et la console ; l'admin applique le
  résultat admin via la console (confirm card + log).
- **Admin Restart** : rappel des critères (6 premières minutes
  in-game, liste des bugs de génération de la référence), annonce de
  table ; même civs/couleurs après restart (à rafraîchir dans le panneau).
- **Patch en cours de tournoi** : choix ancien/nouveau patch →
  paramètre de saison modifiable par la console (config
  `patch_policy`, défaut « admin decides »).
- **Litiges / sanctions / exclusions / refus d'inscription** : hors
  automation ; le mod fournit le fil de faits (logs, timestamps,
  états) sur demande console.
