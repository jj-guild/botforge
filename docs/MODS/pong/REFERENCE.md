# Pong — REFERENCE (règlement AOE Pong, source fonctionnelle)

> **Document source, archivé tel quel** : le règlement officiel du tournoi
> AOE Pong (saison 5, « Antre de l'Ours »), fourni par Aramatu (mod owner).
> C'est la **source de vérité fonctionnelle** pour la migration « en mieux »
> vers BotForge. L'adaptation aux contrats réels de BotForge (seams ADR-0011,
> split ADR-0020, core GameDataService, DraftProvider) se spécifie dans
> [RULES.md](RULES.md) et [DECISIONS.md](DECISIONS.md), jamais en éditant
> cette référence. Les écarts/conflits et les zones non automatisables y
> sont tracés au lieu d'être résolus ici.

## AOE Pong (règlement original — S5)

**Présentation du tournoi :**

L'AOE Pong est un tournoi qui a pour but de vous donner un cadre compétitif dans lequel vous pourrez progresser sur différents aspects du jeu et plus généralement dans la préparation de tournois.
L'objectif est donc de vous permettre de jouer des matchs régulièrement, en condition de tournoi, contre l'adversaire le plus proche de votre niveau possible.

L'idée et l'origine du tournoi vient de \[TabA\] Zyxuwyz qui a proposé de faire des sortes de montées/descentes comme au ping pong. Le gagnant d'une ronde va monter, et le perdant va descendre.
Il se peut que nous décidions de bloquer des tables pour la montée ou la descente afin d'éviter les (re)matchs.

**Déroulement du tournoi :**

Le tournoi va se jouer sur une durée de six rondes étalées sur six semaines.
Vous aurez donc une semaine pour faire votre match en BO5.

> ⚠️ Conflit interne à la source : la présentation annonce six rondes sur
> six semaines, la section « Dates et durée » (S5) en annonce quatre
> (rondes du mercredi au mardi). Exploité comme **paramètre de config**
> (`rounds_per_season`), valeur tranchée par le mod owner — voir
> [DECISIONS.md](DECISIONS.md).

Au début de chaque round, pour chaque table, nous allons ban de façon automatisée et aléatoire le nombre de civilisation requis afin qu'il n'en reste que 15 à votre disposition. Nous vous communiquerons à ce moment-là le preset de draft-civ lié à votre table. Ensuite, nous resterons plus classique puisque la draft map et la draft civ se dérouleront comme dans tous les autres tournois.

Le joueur A sera le premier joueur annoncé sur la table, le joueur B l'autre. Le joueur A sera l'host de la draft map. Le joueur A sera l'host de la draft civ.

La dernière map choisie dans la draft sera la map neutre, c'est-à-dire la première map jouée.

Lien de la draft map : https://aoe2cm.net/preset/pGWoJ

**Précision sur la draft map :**

Les **trois premiers bans** de chaque joueur équivalent à un ban d'une catégorie. Ils doivent donc concerner les maps de la **même** catégorie. Toute draft ne respectant pas cette règle sera considérée comme non valide et devra être refaite à partir du début.

**Précision sur le choix des maps :**

Le perdant choisit la map suivante parmi toutes celles disponibles (i.e qui n'ont pas déjà été jouées), même parmi celles draftées par son adversaire.

**Inscriptions (extrait automatisable) :**

- `/register` sur le channel #bot-commands : enregistre le joueur, lie
  steamID ↔ discordID + données AoE2 (pays, elo). Consentement explicite
  requis (mise en base de données).
- Pseudo Discord = pseudo in-game exigé (renommage demandé sinon).
- Deux disponibilités de 3h consécutives par semaine dans la plage 17h-23h
  (fuseau FR) demandées aux participants.
- `/register_to_tournament` avec le nom « AOE Pong S5 » + validation
  `rules: True` (les règles lues sont acceptées). Toute modification
  d'inscription notifiée à un admin. Les admins peuvent refuser une
  inscription.
- Présence sur le Discord exigée au démarrage (exclusion sinon).

**Dates et durée (S5) :** rondes du mercredi au mardi ; Ronde 1 : mer 3 juin → mar 9 juin 2026, puis une ronde par semaine (mercredi → mardi), quatre rondes en S5.

**Déroulement d'une ronde :**

- **Planification** : le mercredi, l'admin publie la liste des tables et le
  preset de civ draft. Si le preset contient plus de deux civilisations que
  le joueur ne possède pas, taguer un admin pour une nouvelle draft. Les
  joueurs fixent eux-mêmes date/heure et préviennent les admins dans la
  section du tournoi prévue à cet effet. Absence annoncée : proposer une
  nouvelle date ; demande à moins de 24h du match initial → l'adversaire
  peut demander l'Admin Win. Match non planifiable dans les délais : délai
  supplémentaire ou Admin Win à la discrétion des admins.
- **Retard** : > 30 minutes de retard → Admin Loose possible. Retard
  annoncé : l'adversaire peut l'accepter ou non, et peut réclamer l'Admin
  Win à tout moment ; les admins restent arbitres au-delà des 30 minutes.
- **Résultats** : `/add_result` sur la table (joueur A, score « X-X »,
  joueur B). Le second joueur valide via `/validate_score` ou conteste via
  `/contest_score` (tag un admin).
- **Records** (casting/admins) : poster le résultat au format
  `AOE Pong Ronde X Table X : Pseudo1 || Score || Pseudo 2` avec un zip
  contenant un fichier texte « Drafts » (drafts maps et civs) + les parties
  renommées `AOEPong_Pseudo1_vs_Pseudo2_Game_X.aoe2rec`.

**Règles générales (extraits liés au mod) :**

- Pas de bug use volontaire ; patch : choix ancien/nouveau à la discrétion
  des admins pendant l'événement.
- Tricherie : disqualification immédiate + bannissement des événements
  futurs ; interdiction de communication tierce pendant une partie ; accord
  écrit obligatoire pour streamer sa POV (streamer « en sourdine ») ;
  partage de compte interdit.
- Comportement : respect exigé de tous les acteurs (joueurs, admins,
  casters) ; arbitrage et sanctions (blâme → exclusion) réservés aux admins.
- Règlement modifiable par les admins en cours de tournoi.

**Règles en partie (extraits liés au mod) :**

- Pas de restart sauf **Admin Restart** : demandable dans les 6 premières
  minutes in-game pour génération de map buguée (villageois/animaux
  manquants, > 50 % de côtés de minerai/baies inaccessibles, reliques
  manquantes, unité piégée, génération non conforme). Après restart : mêmes
  civilisations et couleurs.
- **Laming** (maps sans forum, 3 villageois, jusqu'à 3 min in-game ou fin
  du traité) : interdit d'attaquer villageois/bâtiments/animaux, murer
  ennemis/ressources/reliques/animaux, TC à portée l'un de l'autre (admin-re
  si TC aveugle), tuer un animal sans y prendre 35 de nourriture ; vol de
  moutons/vaches/poules autorisé. Ailleurs : toutes formes de laming
  autorisées.
- **Pause** : pause autorisée uniquement pour un problème affectant la
  capacité à jouer ; interruption obligatoire sur demande admin ; le
  joueur qui pause relance (après accord adverse) ; pauses raisonnables.
- **Settings** : settings normaux de ladder (référence : capture du
  règlement original). **Map pool S5** : mod
  https://www.ageofempires.com/mods/details/503568/ (22 maps listées dans
  la source : African Reed Beds, African River, Arena, Bypass, Cliffbound,
  CoastToMountain, Dzimbabwe, Dzong, Fernando de Noronha, Fortified
  Clearing, Frigid Lake, Ishtmus, Land Madness, Morass, Nomad, Northern
  Crossrings, Quebrada de Cafayate, Ring of Reeds, Slopes, Stranded,
  Te Fiti…). **À DÉFINIR** : le map pool par saison est lu depuis le core
  (`GameDataService`), jamais codé dans le mod.
- **Streaming** : open stream ; n'importe quel streamer peut caster ;
  « AOE Pong » dans le titre du stream exigé.

**Contacts (S5)** : Aramatu, Elhyar, Phare_Macie, Scramble (admins Discord).
