# Pong mod (ladder montante/descendante « comme au ping pong »)

> Scaffolded from `docs/MODS/TEMPLATE/README.md`. Ce README est la doc
> de lore du mod : l'agent la lit intégralement à chaque session sur le
> mod (skill mod-lore). La source fonctionnelle est le règlement du
> tournoi AOE Pong, archivé dans [REFERENCE.md](REFERENCE.md) — les
> zones marquées **À DÉFINIR** ne doivent jamais être inventées par une
> implémentation.

## Purpose and concepts

L'AOE Pong est un **tournoi compétitif régulier** : donner aux joueurs
un cadre de tournoi hebdomadaire pour progresser, contre l'adversaire
le plus proche de leur niveau. Le concept central vient de l'origine du
tournoi (\[TabA\] Zyxuwyz) : des **montées/descentes comme au ping
pong** — le gagnant d'une ronde **monte** d'une table, le perdant
**descend**.

Concepts (les noms du jeu) :

- **Table** : le duel 1v1 de la semaine ; sur Discord, un salon de
  table ouvert à l'ouverture de la ronde et fermé à sa clôture ;
- **Ronde** : une semaine de jeu (défaut mercredi → mardi), match en
  BO (`bo_format`, défaut BO5) ;
- **Saison** : `rounds_per_season` rondes (nom de la forme
  « AOE Pong S<N> »), map pool et presets par saison ;
- **Draft civs** : ban automatisé aléatoire par table jusqu'à
  `civs_remaining` (défaut 15) civilisations restantes, preset
  draft-civ par table ;
- **Draft map** : déroulée « comme dans tous les autres tournois »,
  les trois premiers bans de chaque joueur = une même catégorie ;
- **Map neutre** : la dernière map choisie dans la draft, première
  map jouée ; le perdant choisit chaque map suivante ;
- **Casting / records** : open stream, résultats postés dans un
  format normalisé avec zip des drafts et enregistrements.

Lore en une phrase : une Antre où l'on monte et descend de table à
chaque semaine de tournoi, à la façon des paliers d'un ping-pong, pour
toujours jouer l'adversaire le plus proche de son niveau.

## Channel tree: salons, categories, roles

Organisation Discord du mod (déclarée dans `conf/mod.yaml`) :

Categories / groupes :

- `pong:admin` — « AOE Pong — Staff » (admin_only) : console du mod,
  fils de faits admin ;
- `pong:ladder` — « AOE Pong » : salons visibles des inscrits ;
- `pong:tables` — « AOE Pong — Tables » : les salons de tables
  générés par ronde.

Salons :

- `pong:announcements` — « annonces-pong » (texte, accès joueurs)
  dans `pong:ladder` : annonces d'ouverture/clôture de ronde, liste
  des tables et presets du mercredi ;
- `pong:bot-commands` — « bot-commands » (texte) : commandes slash
  du mod (`/register`, `/register_to_tournament`…) ;
- `pong:planning` — « planification » (forum) : un topic par match
  pour fixes de date/heure et prévention admin ;
- `pong:records` — « records » (texte) : post des résultats
  normalisés + zip des drafts/recs, nourrit casters et admins ;
- `pong:casting` — « casting » (texte) : annonces de cast ;
- `pong:table_<n>` — salons de tables **générés** (un salon par table
  active, clé `pong:table_<index>`, créé à l'ouverture de la ronde,
  archivé/fermé à la clôture) dans `pong:tables`.

Rôles (trio standard + spécifiques) :

- `pong_player` — « Pong Player » : joueur inscrit de la saison ;
  rôle attribué par l'inscription (RG-REG-2), retiré à la
  clôture de saison ;
- `pong_admin` — « Pong Admin » : accès `pong:admin`, console,
  validations admin ;
- `pong_caster` — « Pong Caster » : accès à l'annonce de cast
  (open stream, rôle descriptif) ;
- `pong_candidate` — « Pong Candidate » : registration faite
  (RG-REG-1), pas encore inscrit à la saison.

Règle machine-room : `pong:admin` est staff-only pendant que le mod
est installé (dossiers de fils de faits admin) ; l'installation
demande la confirmation admin (gate) et la désinstallation ferme les
salons de tables actives et retire `pong_player`.

## External system integration

- **Game-bound** : oui — mod lié à AoE2 (`game_key: aoe2`, comme le
  mod kingdoms) : presets de draft civs/map et formats BO de la
  saison ; le vieil Ours (S5) était exclusivement AoE2.
- **Ce que le mod lit du core** (jamais possédé/dupliqué) : catalogue
  de civilisations, maps et pools de maps de saison via
  `GameDataService` ; profils (elo, pays, steam_id, discord_id) via la
  route de profil du core. Le mod ne stocke ni civs ni maps de
  données de jeu.
- **External providers** : aoe2cm (presets draft map/civ,
  `draft_map_preset` config ; le mod **génère le lien du preset**, il
  ne gère pas la plateforme externe) ; aoe2lobby/LibreMatch plus tard
  pour les résultats automatiques (hors périmètre v1).
- **Core seams** : registry de saisons avec id visible game-scoped
  `pong-aoe2-<guild id>-<index>` ; forums d'entités (topic
  planification par match) ; forum sync `[game key]-maps` du core
  pour les topics maps (lecture seule par le mod).

## Views, buttons and actions of the mod

Views (R9 naming contract, `conf/views.yaml`) :

- `menu:mod:pong:home` (menu) — l'accueil du mod : saison active,
  rôle, sa propre table ; épingle via `pong:announcements` ;
- `panel:mod:pong:table` (panel, dynamic by table) — le panneau de
  table : joueurs A/B (A host des deux drafts), preset civs de la
  table, map neutre, maps restantes si tracking, rappel des règles
  A/host, état du résultat (`PENDING`/`VALIDATED`/`CONTESTED`),
  boutons d'action de table ;
- `panel:mod:pong:round` (panel) — la ronde en cours : toutes les
  tables, scores en attente, deadline de ronde ;
- `panel:mod:pong:standings` (panel) — vue globale des résultats :
  palmarès par table, montées/descentes de la ronde précédente ;
- `panel:mod:pong:table:draft` (panel, **À DÉFINIR**) — la surface de
  draft interne (si retenue en DECISIONS) : bans/picks avec la règle
  des 3 bans = 1 catégorie appliquée par le mod ;
- `panel:mod:pong:admin:console` (SDK-owned console) — les ops du
  mod (voir plus bas).

Boutons/actions (custom-id `<mod>:<component>:<payload>`,
template `.+`) :

- `pong:register:<discord_id>` — lancement de l'enregistrement
  (privacy gate avant persistance, RG-REG-1) ;
- `pong:register_season:<season_id>` — inscription à la saison avec
  `rules: True` et le déclaratif de disponibilités (RG-REG-2) ;
- `pong:add_result:<table_id>` — déclaration de résultat (modal
  joueur A/score/joueur B, RG-RES-1) ;
- `pong:validate:<result_id>` / `pong:contest:<result_id>` —
  validation/contestation par le second joueur (RG-RES-2, la
  contestation tagge les admins) ;
- `pong:report_preset:<table_id>` — signalement « preset avec > 2
  civs non possédées » → tag admin (RG-CDRAFT-2) ;
- `pong:report_draft:<table_id>` — signalement « draft non conforme »
  → tag admin (RG-MDRAFT-2, si draft externe) ;
- `pong:record_template:<table_id>` — génère le gabarit du message de
  records + gestion du zip (RG-REC-1) ;
- `pong:announce_cast:<table_id>` — annonce de cast sur
  `pong:casting` (RG-REC-2) ;
- `pong:update_entry:<discord_id>` — modification d'inscription →
  tag admin (RG-REG-2).

Guards : check admin au clic (jamais à l'affichage) pour toutes les
ops console ; confirm cards pour les mutations admin (bloquer une
table, appliquer un admin win/loose, invalider un résultat) ; modals
pour `/add_result` et l'inscription.

Admin console (`mod="pong"`) : `open_season`, `open_round` (crée les
tables/salons + ban civs + presets), `close_round` (ferme les salons
de tables), `block_table` (montée/descente, RG-TAB-2),
`admin_result` (admin win/loose, RG-ADM), `arbitrate_result`
(valider/invalider/redéclarer, RG-RES-2), `redraft_preset`
(RG-CDRAFT-2), `patch_policy` (RG-ADM), `reset_table`,
`reload_season_config` (preset map pool par saison) ; chaque op loggée
(confirm card + log de mutation).

## Pinned salons

- `menu:mod:pong:home` épinglé dans `pong:announcements` ;
- `panel:mod:pong:round` épinglé dans `pong:ladder` (salon
  d'accueil de saison) ;
- cycle de vie : pin créé si manquant, rafraîchi en place à chaque
  changement, rétabli si salon supprimé (self-heal au boot), balayé à
  la désinstallation du mod.

## Player / admin / bot interactions

- **player** — `/register` puis `/register_to_tournament`
  (RG-REG-1/2, modal de consentement et de disponibilités) ;
  consulte son panneau de table (A/B, host, preset, map neutre) ;
  déclare le résultat sur sa table (`/add_result`, guard : auteur =
  joueur A ou B de la table, ronde ouverte, format de score
  X-X) ; valide ou conteste le résultat du co-équipier de table ;
  signale un preset (> 2 civs non possédées) ou une draft non
  conforme ; génère son gabarit de records ; annonce son cast ; met
  à jour son inscription (tag admin).
- **admin** — console : ouverture de saison, ouverture de ronde
  (tables + ban civs + presets), clôture de ronde, blocage de tables,
  admin win/loose (sur les faits horodatés fournis par le mod :
  retard 30 min, replanif < 24h, non-planification), arbitrage de
  contestation, relance de preset, politique patch ; chaque mutation
  a une confirm card et un log ; PAS d'automation des litiges
  (constat, décision humaine) ;
- **bot** — passes de boot : self-heal des salons/ pins manquants,
  reconcile des tables (salon existe pour chaque ronde ouverte),
  heal des rôles ; boucles planifiées : ouverture/clôture de ronde
  (mercredi → mardi), annonce du mercredi (tables + presets),
  rappels d'échéance aux joueurs ; jamais d'exception non rendue :
  chaque passe poste son rapport (dans `pong:announcements` ou un fil
  de faits, jamais en log seul) ; passe d'archivage des salons de
  tables clôturés.

## Usage

```text
/register                     # enregistrement joueur (consentement requis)
/register_to_tournament       # inscription à la saison active (rules: True)
/add_result                    # déclaration de résultat sur la table (X-X)
/validate_score                # validation du résultat déclaré
/contest_score                 # contestation → tagge un admin
```

## See also

- [REFERENCE.md](REFERENCE.md) — le règlement officiel AOE Pong (source)
- [RULES.md](RULES.md) — les règles du jeu (automatisables/testables)
- [ENVIRONMENT.md](ENVIRONMENT.md) — la configuration + la config de saison
- [DECISIONS.md](DECISIONS.md) — les décisions validées (elles priment)
- [TESTS.md](TESTS.md) — les scénarios de validation
- [../CATALOGUE.md](../CATALOGUE.md) — l'entrée du mod dans le catalogue
- [../../WORKFLOWS.md](../../WORKFLOWS.md) — les workflows de la plateforme liés
