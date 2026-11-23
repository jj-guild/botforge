# Pong — Architecture Discord (salons, catégories, usage)

Architecture cible de l'espace Discord du mod : catégories, salons,
permissions, cycle de vie par ronde, et règles d'usage. Complète
[ENVIRONMENT.md](ENVIRONMENT.md) (clés de config) et
[RULES.md](RULES.md) (règles métier). Décisions D-PONG-006..019
([DECISIONS.md](DECISIONS.md)) s'appliquent.

## 1. Principe : catégories scoped-mod, provisionnées par le core

- Aucune catégorie/salon n'est créé en direct par le mod : tout passe
  par le `ModRegistry` + `ChannelService`/`RoleService` du core
  (botforge-services#26), depuis la **déclaration** YAML
  (`modules/mods/pong/conf/mod.yaml`).
- Les salons sont adressés par clés logiques `pong:<key>` — jamais par
  nom. Le mod ne dépend jamais du nommage physique : renommer un salon
  ne casse rien.
- Les salons de tables sont **générés par ronde** (opération
  `open_round`) et **archivés** à la clôture — jamais déclarés
  statiquement.

## 2. Cartographie

```
🏓 AOE PONG (groupe ladder — visible joueurs)      [pong:ladder]
├─ 📣 annonces-pong        pong:announcements   (texte)
├─ 🤖 bot-commands         pong:bot-commands    (texte)
├─ 📅 planification        pong:planning        (forum, 1 topic/match)
├─ 🎞️ records              pong:records         (texte)
└─ 🎙️ casting              pong:casting         (texte, lecture publique)

🏓 TABLES (groupe tables — généré par ronde)       [pong:tables]
└─ table-<slug>            pong:table_<slug>    (texte, 1 par table)
                                                     slugs neutres, uniques
                                                     par ronde, recyclés

⚙️ PONG-STAFF (groupe admin — admin_only)          [pong:admin]
├─ ⚙️ paramètres           pong:settings        (panneau lifecycle)
└─ 📜 journal-admin        pong:admin_log       (opérations horodatées)
```

## 3. Matrice de permissions

| Salon | Candidate | Waitlist | Player | Caster | Admin | hors-serveur |
| --- | --- | --- | --- | --- | --- | --- |
| `annonces-pong` | lecture | lecture | lecture | lecture | écriture | non |
| `bot-commands` | cmd `/register` | cmd inscription file | toutes cmd | — | toutes cmd | non |
| `planning` | non | non | lecture+post topic | lecture | écriture | non |
| `records` | non | non | lecture+post | lecture/post | écriture | non |
| `casting` | lecture | lecture | lecture | écriture | écriture | lecture (everyone) |
| `table_<slug>` | non | non si hors table | joueurs de la table | — | écriture | non |
| `paramètres` | non | non | non | non | écriture | non |
| `journal-admin` | non | non | non | non | lecture | non |

Roles gate : `pong_candidate`, `pong_waitlist`, `pong_player`,
`pong_caster`, `pong_admin` (voir ENVIRONMENT.md « Roles »). Le core
synchronise les permissions à chaque ronde (ouverture/clôture).

## 4. Cycle de vie d'une ronde (usage opérationnel)

### Ouverture (op console `open_round`)

1. Calcul de l'appariement sur les résultats **validés à l'échéance**
   (grâce ±3 j : D-PONG-012 — mouvement différé pour les retardataires).
2. Création des salons `table-<slug>` dans le groupe tables (slug tiré
   du pool `neutral_random`, sans ordre, D-PONG-014) + panneau pinned :
   joueurs A/B (A = premier emplacement, host des deux drafts), preset
   draft-civ, rappels (3 bans = 1 catégorie, map neutre = dernière
   choisie, perdant choisit la suivante), deadline = échéance + grâce.
3. Permissions sync : seuls les deux joueurs de la table + admins.
4. Topic de planification créé dans `pong:planning` :
   `Ronne <n> — <slug> : <PseudoA> vs <PseudoB>`.
5. Annonce dans `annonces-pong` : liste des tables **sans ordre de
   niveau**, deadlines, rappel d'usage. Aucune mention de
   montée/descente (RG-TAB-5).

### Pendant la ronde

- Les joueurs planifient dans leur topic, jouent, déclarent
  (`/add_result` sur le salon de table) et valident
  (`/validate_score`) ou contestent (`/contest_score` → tag admin).
- Boutons de constat sur la table : « draft non conforme »,
  « forfait », « signaler ». Tout signalement = tag admin + fil de
  faits horodaté (constat, décision humaine, RG-ADM).
- `/recap` : réponse **ephemeral** (visible du seul demandeur).

### Clôture (timer `round_window` + passe de clôture)

1. Résultats `PENDING` listés dans un fil d'arbitrage (jamais en log
   seul) ; admin win/loose si nécessaire (D-PONG-011).
2. Salons `table_<slug>` **archivés** (fermeture + déplacement dans
   une catégorie archive provisionnée par
   le core, pas un delete : l'historique fait partie du fil de faits).
3. Les matchs joués dans la grâce (±3 j) continuent d'être validés sur
   les topics archivés ; récap mis à jour immédiatement, mouvement
   appliqué au calcul suivant.

### Self-heal (boot + périodique)

- Salon manquant → recréé depuis l'état (panneau reconstruit), pins
  rétablis, permissions resynchronisées, rapport dans `annonces-pong`
  (jamais d'exception silencieuse, SC-PONG-015).

## 5. Règles d'usage (les « comment »)

- **`annonces-pong`** : seules les annonces automatisées + les admins
  y postent. Contenu contractuel : ronde ouverte/clôturée, tables
  (liste non ordonnée), civs par table, rappels génériques.
  Pas de résultats, pas de scores, pas de récap.
- **`bot-commands`** : toutes les commandes slash y sont censées
  fonctionner (résultat/valider/contester fonctionnent aussi sur le
  salon de table). Les réponses de commandes sensibles sont
  **ephemeral** : notice, récap, statut d'inscription.
- **`planning` (forum)** : 1 topic par match et par ronde ; les
  échanges de scheduling restent dedans (pas de DM obligatoire) ; le
  topic est verrouillé à la clôture.
- **`table_<slug>`** : espace de travail du match ; messages
  automatisés de table (panneau, broadcasts). Le nom du salon ne
  divulgue aucun niveau.
- **`casting`** : annonces de streams libres (open stream, D-PONG-002
  REFERENCE), à la main du joueur-caster ; le bot n'inspecte pas les
  titres.
- **`records`** : les packs (phase 1 : gabarit + bouton ; phase 2 :
  zip auto sans spoiler, D-PONG-010) par match, format de message
  normalisé `AOE Pong Ronde X Table X : P1 || S || P2`.
- **DM privés au joueur** : uniquement le récap final (clôture de
  saison ou départ, D-PONG-017). Si DM refusé : notice ephemeral dans
  `bot-commands` avec bouton « me le renvoyer » (repli à trancher).
  Aucun autre usage du DM (pas de relances privées).
- **`waitlist`** : les candidats inscrits après clôture gardent
  l'accès à `bot-commands` (inscription file) et lisent `annonces`;
  ils n'entrent dans `tables`/`planning` qu'une fois insérés en duo
  (RG-TAB-3) ou remplaçants (RG-TAB-4).

## 6. Insertions, remplacements, archives (flux joueurs, D-PONG-015..019)

- Duo validé (table et-demi) : salon `table_<slug>` créé **dès la
  ronde en cours** (les deux jouent entre eux), position dans la
  chaîne effective à la ronde suivante, renumérotation automatique.
- Remplaçant : reprise du créneau exact → permissions du salon de
  table mises à jour, topic réutilisé ou rouvert.
- Départ : salon de la table concernée passe en mode orphelin
  (panneau actualisé « match d'appoint volontaire proposé aux
  voisins ») jusqu'à absorption (remplaçant, match volontaire,
  fusible) ; à défaut, archivage anticipé du salon à la clôture.

## 7. Multi-tournois (note de périmètre)

Chaque type de tournoi vit dans **son propre périmètre scoped-mod**
(`pong:*`, futurs `swiss:*`, `bracket:*`…) avec ses catégories
provisionnées de la même manière : pas de collision de salons, le
core gère la coexistence (botforge-services#26). Le moteur
d'appariement de pong est implémenté derrière une seam `PairingPolicy`
(interface domaine pure) : les formats futurs (ronde suisse, brackets)
réutiliseront le socle commun (inscription, saisons, résultats, drafts,
récaps, console) en changeant la politique d'appariement. L'extraction
d'un `tournament-core` partagé se décidera **à la deuxième
implémentation**, pas avant (règle : abstraire après deux).
