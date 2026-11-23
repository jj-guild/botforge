# Pong — User stories

Toutes les user stories que le bot doit couvrir. Chaque story :
**En tant que <rôle>, je veux <capacité> afin de <bénéfice>** —
tracée vers les règles (RULES.md), décisions (DECISIONS.md) et
scénarios de test (TESTS.md) qui la réalisent. Toute story sans trace
règle = point de design à trancher ; toute règle sans story = dead
doc signalé en revue.

Rôles : **C**andidat, **W**aitlist, **P**layer, **K** (caster),
**A**dmin, **S**pectateur.

## Parcours joueur

| ID | En tant que | je veux | afin de | Trace |
| --- | --- | --- | --- | --- |
| US-PONG-001 | C | m'enregistrer (steam ↔ discord) avec mon consentement explicite | lier mon profil AoE2 sans surprise de confidentialité | RG-REG-1, SC-001/002 |
| US-PONG-002 | C | m'inscrire à la saison en validant le règlement (version tracée) et déclarer mes disponibilités | jouer la saison en ayant accepté des règles connues | RG-REG-2 |
| US-PONG-003 | C | autodéclarer mon niveau (« je joue au-dessus/en-dessous de mon Elo ») | être placé à ma hauteur réelle dès la ronde 1 | D-PONG-013, RG-REG-2 |
| US-PONG-004 | P | recevoir chaque semaine mon match (« cette semaine, vs Y ») sans position ni montée/descente affichées | jouer sans pression de classement | RG-TAB-5, D-PONG-014, SC-004 |
| US-PONG-005 | P | avoir un salon de table dédié avec les deux drafts civs/map prêtes et le panneau complet (A host, map neutre, ban 3=1 catégorie) | tout savoir pour jouer sans relire le règlement | RG-CDRAFT-1, RG-MDRAFT-1/2, SC-004 |
| US-PONG-006 | P | planifier mon match dans un topic dédié (forum planification) | convenir d'un créneau sans DM chassé-croisé | ARCHITECTURE §5 |
| US-PONG-007 | P | déclarer mon résultat (`3-2`) sur ma table et faire valider par mon adversaire | clore le match sans intervention admin | RG-RES-1/2, SC-007/009 |
| US-PONG-008 | P | contester un résultat erroné (`/contest_score` → tag admin) | être protégé contre les fausses déclarations | RG-RES-2 |
| US-PONG-009 | P | déclarer un forfait (résultat « perdu », pas de manipulation de score) | abandonner proprement une semaine impossible | D-PONG-011-1, SC-016 |
| US-PONG-010 | P | abandonner en cours de set avec score complété (victoires restantes à l'adversaire) | arrêter un set perdu sans litige | D-PONG-011-3, SC-017 |
| US-PONG-011 | P | signaler « aucune date trouvée » et laisser l'admin trancher sur dossier de faits | ne pas porter le fardeau de l'arbitrage | D-PONG-011-2, SC-018 |
| US-PONG-012 | P | jouer dans la grâce ±3 jours et savoir que mon mouvement différera d'une ronde | absorber un imprévu sans bloquer la chaîne | D-PONG-012, SC-023 |
| US-PONG-013 | P | consulter mon récap à la demande (`/recap`, réponse ephemeral visible de moi seul) | suivre MA progression sans être jugé (ni me juger) | D-PONG-014, SC-024 |
| US-PONG-014 | P | recevoir mon récap final en DM à la clôture | garder une trace de ma saison | D-PONG-014, SC-024 |
| US-PONG-015 | P | signaler un preset de civs injouable (≥ 3 civs non possédées) ou une draft map non conforme (3 bans ≠ 1 catégorie) | jouer dans des conditions valides | RG-CDRAFT-2, RG-MDRAFT-2, SC-013 |
| US-PONG-016 | P | quitter le tournoi entre deux rondes et recevoir mon récap clôturé | partir sans pénaliser mes adversaires ni la structure | D-PONG-017, SC-021 |
| US-PONG-017 | P | me porter volontaire pour un match d'appoint contre un orphelin (sans mouvement de table, récap only) | aider la communauté à ne jamais laisser un joueur seul | D-PONG-018/019, SC-022 |
| US-PONG-018 | W | être repêché comme remplaçant au créneau exact d'un partant | jouer la saison sans bousculer les tables | D-PONG-017, SC-021 |
| US-PONG-019 | W | être inséré en duo (« table et-demi ») à notre niveau et jouer notre match dès la ronde en cours | entrer en cours de saison comme une table normale | D-PONG-016, SC-020 |
| US-PONG-020 | W | rejoindre la file d'attente quand l'inscription est close et être visible pour le binomage admin | ne pas rater la saison pour quelques jours de retard | D-PONG-015, SC-019 |
| US-PONG-021 | K | annoncer mon cast (open stream, titre « AOE Pong ») | caster librement | RG-REC-2 |
| US-PONG-022 | S/P | consulter les packs de records normalisés (`Ronde X Table X : P1 ‖ S ‖ P2` + zip) | revoir/arbitrer les matchs spoiler-free | RG-REC-1, D-PONG-010 |

## Parcours admin (constat, décision humaine)

| ID | En tant que | je veux | afin de | Trace |
| --- | --- | --- | --- | --- |
| US-PONG-023 | A | ouvrir une saison : tirage au seed (ladder + humain), appariement ronde 1, provision salons | lancer la compétition en confiance | RG-STRUC-1, SC-004 |
| US-PONG-024 | A | corriger le seed d'un joueur (avant tirage, entre rondes) en console | intégrer les retours terrain sans publier les seeds | D-PONG-013, RG-ADM |
| US-PONG-025 | A | binômer les candidats de la file en duos d'insertion, avec les côte-à-côte de seed humain | décider des entrées au feeling éclairé | D-PONG-015, RG-ADM |
| US-PONG-026 | A | valider le point d'insertion proposé par le bot pour un duo | insérer sans bousculer la chaîne | D-PONG-016, SC-020 |
| US-PONG-027 | A | valider un départ sur dossier de faits (matchs joués, en attente) et déclencher la chaîne de parité (file → match volontaire → fusible) | gérer les départs humainement en 2 clics | D-PONG-017/019, SC-021/022 |
| US-PONG-028 | A | appliquer un admin win/loose sur faits horodatés (retard 30 min, replanification <24 h, pas de rdv) | arbitrer vite et traçable | D-PONG-011-2, SC-018 |
| US-PONG-029 | A | bloquer des tables à la montée/descente (anti-rematch), le blocage verrouillant le groupe en semi_blocked | éviter les res-series indésirables | RG-TAB-2 |
| US-PONG-030 | A | relancer une draft civ non conforme via le bouton de signalement | garder les tables jouables | RG-CDRAFT-2 |
| US-PONG-031 | A | décider de la politique de patch en cours de tournoi | ne pas figer la compétition sur une MAJ | RG-ADM |
| US-PONG-032 | A | disposer du fil de faits d'une table sur demande console (timestamps, états) | arbitrer les litiges avec des preuves | RG-ADM, D-PONG-004 |
| US-PONG-033 | A | voir en console les seeds/positions (seul endroit où l'ordre existe) | administrer sans l'exposer aux joueurs | RG-TAB-5 |

## Parcours plateforme (mod lui-même)

| ID | En tant que | je veux | afin de | Trace |
| --- | --- | --- | --- | --- |
| US-PONG-034 | système | ouvrir/clôturer les rondes automatiquement (timer + grâce), self-heal des salons/pins au boot | tenir sans supervision manuelle (fini la gestion manuelle S5) | RG-STRUC-1, SC-004/014/015 |
| US-PONG-035 | système | calculer les mouvements selon `move_policy` de la saison (alternance S1 classic, S2 semi_blocked, …) | exécuter le pong sans erreur humaine | D-PONG-006/012, SC-005/006 |
| US-PONG-036 | système | garder tout le parcours auditable : logs d'admin, seeds persistés par ronde/table (drafts rejouables), rien de silencieux | garantir la confiance de la communauté | D-001..004, SC-014 |

> Les stories 34-36 façon « système » tracent l'automatisation ; le
> restes du flux manuel S5 (fusible, tables et-demi, deux matchs
> volontaires) se retrouve dans US-017/019/025/027 — c'est la
> désécralisation complète de la charge admin qui motivait ce mod.
