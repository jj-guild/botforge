# Pong — Mod Rules

Règles du jeu appliquées par le mod, extraites de
[REFERENCE.md](REFERENCE.md) (règlement AOE Pong). Chaque règle est écrite
pour être automatisable : testable ou vérifiable par le bot. Les zones à
discrétion admin sont classées **constat, décision humaine** : le bot
rapporte les faits (tags, timestamps, états), l'admin tranche. Les
décisions priment ([DECISIONS.md](DECISIONS.md), D-PONG-001..019).

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
discord, et le déclaratif « 2 disponibilités de 3h consécutives dans
17h-23h » capté à l'inscription. Toute modification d'inscription doit
être notifiée à un admin : le mod fournit `/update_entry` qui tagge les
admins.

- **Seed ladder** : à l'inscription, le joueur reçoit son **seed elo** =
  `(2 × Elo actuel + Elo max) / 3` (D-PONG-007).
- **Seed humain (D-PONG-013)** : le joueur **autodéclare son niveau**
  (« au-dessus / en-dessous de mon Elo ladder », champ libre court) ;
  l'admin peut **corriger le seed** d'un joueur avant le tirage et
  entre les rondes (console, confirm card, log). Le seed sert
  uniquement au placement initial, **jamais affiché** aux joueurs.
- **Refus d'inscription** : décision humaine (le mod n'accepte ni ne
  refuse seul), il expose le bouton admin correspondant.

### RG-REG-3 — Inscription tardive : file d'attente

La fenêtre d'inscription se **ferme à l'ouverture de la ronde 1**
(D-PONG-015). Un `/register_to_tournament` après clôture est refusé
et propose l'ajout à la **file d'attente** (état joueur `waitlist`,
rôle `pong_waitlist`). Le **binomage** de deux candidats de la file
en duo d'insertion est une décision admin (aucune tolérance
automatique de niveau) ; le duo entre par RG-TAB-3.

## RG-STRUC — Structure de saison

### RG-STRUC-1 — Rondes et tables

Une saison compte `rounds_per_season` rondes (**4**, D-PONG-005),
chacune d'une fenêtre `round_window` (défaut 7 jours, mercredi →
mardi) **plus une grâce de `round_grace_days` (3) jours**
(D-PONG-012). Le BO est `bo_format` (défaut BO5). **Le nombre de
tables = nombre de joueurs / 2** ; l'effectif jouable n'est jamais
impair (chaîne de parité, RG-TAB-4). À l'ouverture d'une ronde, le
mod crée le salon de chaque table, y annonce joueurs A/B, preset et
ronde ; à la clôture, il ferme les salons (config `close_tables`).

- **Grâce ±3 jours (D-PONG-012)** : l'appariement de la ronde
  suivante se calcule sur les résultats **validés à l'échéance** de
  la ronde. Un match joué pendant la grâce compte immédiatement dans
  le récap du joueur (RG-RES-3) ; son **mouvement est différé d'une
  ronde** et s'applique au calcul suivant.

### RG-STRUC-2 — Attribution A/B et rôles de draft

Sur chaque table, **le joueur A est le joueur assis au premier
emplacement de la table**, le joueur B l'autre (D-PONG-007) :

- **ronde 1** : A = le mieux classé des deux au seed (ladder + humain,
  D-PONG-007/013) ;
- **rondes suivantes** : **le joueur qui monte prend l'emplacement B,
  le joueur qui descend prend l'emplacement A** (issu du calcul de
  mouvement RG-TAB) ;
- le joueur A est host de la draft map **et** de la draft civ — la
  convention est rappelée dans le panneau de table.

## RG-TAB — Tables et montée/descente

### RG-TAB-1 — Mouvements

Règle centrale (« comme au ping pong ») : **le gagnant monte, le
perdant descend**. Deux politiques de mouvement (D-PONG-006), qui
**alternent par saison** (D-PONG-012 : S1 `classic`, S2
`semi_blocked`, S3 `classic`…) :

1. **`classic`** — le gagnant monte d'une table, le perdant descend
   d'une table ;
2. **`semi_blocked`** — les tables sont regroupées 2 par 2 (3 pour le
   dernier groupe si le nombre de tables est impair) ; les
   montées/descentes se font **au sein de chaque groupe uniquement**
   (ex. groupe {T1, T2} : gagnant de T1 reste en T1, perdant de T1
   va en T2, gagnant de T2 va en T1, perdant de T2 reste en T2).
   Aucun mouvement inter-groupe.

Les mouvements se calculent **sur les matchs de table uniquement**
(un match d'appoint volontaire ne déplace personne, RG-TAB-4), au
moment de l'ouverture de la ronde suivante, sur les résultats
validés à l'échéance (grâce : mouvement différé d'une ronde,
D-PONG-012). Ils déterminent les emplacements A/B de la ronde
suivante (le montant prend B, le descendant prend A).

### RG-TAB-2 — Blocage de tables

L'admin peut **bloquer des tables à la montée ou à la descente** pour
éviter les (re)matchs : en `classic`, un joueur bloque à sa table si
la table cible est bloquée pour son sens de mouvement ; en
`semi_blocked`, le blocage d'une table verrouille son groupe.
Opération console admin (`mod="pong"`), confirm card, log de cette
mutation, appliquée au calcul de la ronde suivante.

### RG-TAB-3 — Tables « et-demi » : insertion d'un duo (D-PONG-016)

La chaîne des tables est une **liste ordonnée interne**
(`chain_position`, index numérique acceptant les intercalaires type
7.5). L'entrée d'un duo validé (RG-REG-3) procède ainsi :

1. le bot **propose le point d'insertion** : entre les deux tables
   qui encadrent le niveau du duo (seed humain de chaque entrant) ;
2. l'**admin valide** l'insertion en console (confirm card, log) ;
3. **en cours de ronde** : le duo joue son match entre lui dès la
   ronde en cours, **zéro impact sur les autres tables** ;
4. à la ronde suivante, la table prend sa place dans la chaîne de
   mouvement et la **renumérotation est automatique**. Seuls les
   voisins directs changent d'interlocuteur de mouvement ; aucun
   re-shuffle global.

### RG-TAB-4 — Chaîne de parité et matchs d'appoint (D-PONG-019)

L'effectif jouable n'est **jamais impair** ; chaque niveau absorbe le
suivant :

1. **Arrivées binômées** : un candidat seul de la file d'attente
   attend un partenaire (RG-REG-3) ;
2. **Départ comblé au créneau exact** : le premier volontaire de la
   file prend la place du partant dans la chaîne (pas de re-shuffle,
   résultats acquis conservés — D-PONG-017) ;
3. **Sans remplaçant — match volontaire** : le bot propose aux joueurs
   des **tables voisines (par proximité)** un match d'appoint contre
   l'orphelin, volontariat, **récap-only** : le résultat compte dans
   les récaps des deux joueurs mais **aucun mouvement** ne s'applique
   (RG-TAB-1) ;
4. **Dernier recours — fusible** : un volontaire de la file, puis
   l'admin.

Un départ pendant une ronde avec match en attente = **forfait
(défaite)** pour le partant (D-PONG-011 cas 1 / D-PONG-017).

### RG-TAB-5 — Ordre invisible des tables (D-PONG-014)

L'ordre des tables existe **dans les données, pas dans l'affichage** :

- `chain_position` est interne (consommée par le calcul de mouvement
  RG-TAB-1 et l'insertion RG-TAB-3, visible console admin uniquement) ;
- les salons de tables portent des **noms neutres** (pas de numéro
  d'ordre ni de niveau) ; le salon annonces liste les tables dans un
  ordre non significatif (alphabétique) ;
- les messages joueurs ne mentionnent **jamais** de position ni de
  montée/descente : « cette semaine, ton match : vs Y ».

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

### RG-MDRAFT-1 — Drafts externes (aeo2cm)

Draft map et draft civ restent **externes, sur aoe2cm** (D-PONG-009) :

- **draft map** : un simple preset à gérer, celui du map pool de la
  saison (ex. S5 : `https://aoe2cm.net/preset/pGWoJ`) ;
- **draft civ** : **dérivée d'un `base_preset`** — le mod génère le
  preset de la table à partir du `base_preset` (portage du générateur
  Python du mod owner ; source aoe2cm :
  https://github.com/SiegeEngineers/aoe2cm2), en appliquant d'abord
  RG-CDRAFT-1.

La **dernière map choisie** dans la draft est la **map neutre**, jouée
en premier : le mod l'affiche tel quel dans le panneau de table.

### RG-MDRAFT-2 — Les trois premiers bans = une catégorie

Dans la draft map, les **trois premiers bans de chaque joueur** doivent
concerner des maps de la **même catégorie** (ban de catégorie). Toute
draft ne respectant pas cette règle est **non valide et doit être
refaite à partir du début**.

- La draft étant externe (aeo2cm), la vérif est **déclarative** : le
  post de draft sur la table porte un bouton « draft non conforme »
  visible qui tagge un admin (constat, décision humaine).

### RG-MDRAFT-3 — Choix de la map suivante

Le **perdant** de la partie précédente choisit la map suivante parmi
**toutes les maps disponibles** (pas déjà jouées), y compris celles
draftées par son adversaire.

- Rappel déclaratif dans le panneau de table (le suivi de série par le
  mod n'est pas requis en phase 1 : la déclaration de résultat reste
  le point d'entrée).

## RG-RES — Résultats

### RG-RES-1 — Déclaration

`/add_result` **sur le salon de la table** : joueur A, score `X-X`
(**score A à gauche, score B à droite**), joueur B. Validations :

- auteur ∈ {joueur A, joueur B} de la table, ronde ouverte ;
- format score `^[0-9]+-[0-9]+$`, compatibilité avec `bo_format`
  (BO5 : X+Y ≤ 5, max(X,Y) = 3).

**Scores hors format — trois cas distincts (D-PONG-011)** :

1. **Forfait** — le joueur se déclare forfait sur sa table : il entre
   un résultat « perdu » (format forfait dédié, pas de manipulation du
   score), l'autre joueur valide, terminé ;
2. **Pas de rdv trouvé** — deux joueurs sans planification possible :
   **l'admin de la compétition tranche** (admin win via console,
   constat, décision humaine) ;
3. **Match partiellement joué / abandon en cours de set** — autorisé :
   l'abandon donne les victoires restantes à l'adversaire (score
   complété, déclaration normale + validation).

### RG-RES-2 — Validation ou contestation

Le **second joueur** (celui qui n'a pas déclaré) est invité à valider
via `/validate_score` ou contester via `/contest_score` **qui tagge un
admin**. Sans validation, le résultat reste `PENDING` jusqu'à un
traitement admin (constat, décision humaine). Après contestation :
l'admin tranche via la console (valider/invalider/redéclarer).

### RG-RES-3 — Enregistrement, récap personnel, mouvement

Un résultat **validé** (ou arbitré admin) est persisté, déclenche
RG-TAB-1 (mouvement de table — différé d'une ronde si joué pendant
la grâce, D-PONG-012) et alimente le **récap personnel** du joueur
(D-PONG-014) :

- **pas de classement global** : aucun tableau comparatif publié ;
- chaque joueur reçoit son récap (sets disputés, W/L, adversaires,
  parcours de tables) **en DM privé**, à la demande et en fin de
  saison ; un joueur qui quitte reçoit le récap clôturé de ses sets
  disputés (D-PONG-017) ;
- idempotent : re-valider un résultat déjà validé est sans effet (log
  seulement).

## RG-REC — Records et casting

### RG-REC-1 — Records

Pour faciliter casting et arbitrage, chaque match est accompagné d'un
message de résultat au format exact
`AOE Pong Ronde X Table X : Pseudo1 || Score || Pseudo2` affichant la
draft map et la draft civ, et d'un zip contenant le fichier
« Drafts » et les parties
`AOEPong_Pseudo1_vs_Pseudo2_Game_X.aoe2rec`.

- **Automatisation visée (D-PONG-010, phase 2)** : le mod génère le
  zip en allant chercher les parties des joueurs (piste :
  https://replaypacker.zeta-two.com) pour que les casters aient
  toujours les 5 records d'un BO5 **sans spoiler**. En phase 1, le
  mod génère le gabarit de message (bouton) ; la collecte physique
  des fichiers reste humaine.

### RG-REC-2 — Open stream

Open stream par défaut (config `open_stream`, défaut vrai) : tout
caster peut caster ; le titre doit contenir « AOE Pong ». Le mod
propose l'annonce de cast sur la table (salon `pong:casting`, rôle
`pong_caster`) mais ne vérifie pas les titres de stream (hors
périmètre bot).

## RG-ADM — Commandes admin (constat, décision humaine)

Le mod fournit les documents et boutons, la décision reste humaine :

- **Admin Win / Admin Loose** : retard > 30 min (timestamp d'ouverture
  de table + rappel), replanification < 24h du créneau prévu, ou
  **pas de rdv trouvé** (D-PONG-011 cas 2) → le mod liste les faits
  horodatés sur la table et la console ; l'admin applique le
  résultat admin via la console (confirm card + log).
- **Admin Restart** : rappel des critères (6 premières minutes
  in-game, liste des bugs de génération de la référence), annonce de
  table ; mêmes civs/couleurs après restart (à rafraîchir dans le
  panneau).
- **Correction de seed (D-PONG-013)** : l'admin ajuste le seed d'un
  joueur (avant le tirage, entre les rondes) ; confirm card + log ;
  le seed corrigé sert au placement suivant, jamais affiché.
- **Validation d'insertion (D-PONG-016)** : le bot propose le point
  d'insertion d'un duo, l'admin valide en console (confirm card) ;
  **binomage de la file (D-PONG-015)** : décision admin duo par duo.
- **Départ d'un joueur (D-PONG-017)** : le bot dresse le dossier
  (matchs joués/en attente, dates) ; l'admin valide le retrait en
  console ; place proposée à la file, sinon match volontaire
  (RG-TAB-4).
- **Patch en cours de tournoi** : choix ancien/nouveau patch →
  paramètre de saison modifiable par la console (config
  `patch_policy`, défaut « admin decides »).
- **Litiges / sanctions / exclusions / refus d'inscription** : hors
  automation ; le mod fournit le fil de faits (logs, timestamps,
  états) sur demande console.
