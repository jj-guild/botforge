# KINGDOMS — DOCUMENT DE RÉFÉRENCE DU PROJET

> Verbatim reference provided by the game designer (Season II).
> This document is the **functional source of truth** for the Kingdoms mod.
> Validated decisions taken after this document was written are recorded in
> [DECISIONS.md](../../MODS/kingdoms/DECISIONS.md) — where the two disagree,
> the decisions win. Anything not defined here or in DECISIONS.md is
> **À DÉFINIR** and must not be invented by an implementation.

## 1. Présentation générale

**Kingdoms** est un événement communautaire externe autour d'**Age of Empires II: Definitive Edition**.

Le principe est de faire s'affronter plusieurs **Royaumes** qui cherchent à conquérir et conserver des **territoires**, chaque territoire correspondant à une map d'Age of Empires II.

Le jeu est organisé autour de :

* Royaumes joueurs ;
* Seigneurs ;
* Rois ;
* Gaïa, royaume contrôlé par l'IA ;
* territoires ;
* civilisations et alliances ;
* attaques et défenses ;
* technologies ;
* mariages ;
* exploration ;
* évolution des époques ;
* diplomatie ;
* événements hebdomadaires.

Le projet doit à terme pouvoir être géré par un **bot Discord**, avec éventuellement un site web dans une phase ultérieure.

---

# 2. Philosophie générale du système

Le système doit être conçu de manière **paramétrable**.

L'administrateur doit pouvoir modifier les principaux paramètres d'une saison sans devoir modifier le code du bot.

Exemples de paramètres :

* nombre de Royaumes ;
* nombre de Seigneurs par Royaume ;
* nombre de territoires de départ ;
* nombre de territoires de Gaïa ;
* liste des maps disponibles ;
* durée de la saison ;
* nombre de cycles ;
* horaires des événements ;
* règles et paramètres de certaines mécaniques.

La Saison II utilise des valeurs de base, mais ces valeurs ne doivent pas être codées en dur.

---

# 3. Saison

## 3.1 Durée

Une saison est normalement composée de :

* **4 semaines**
* **4 cycles**

Cependant, ces valeurs doivent être **modulables et configurables par l'administrateur**.

Une saison peut donc théoriquement avoir une autre durée si l'administrateur modifie les paramètres.

---

## 3.2 Début de saison

La date et l'heure exactes du début sont choisies par l'administrateur / organisateur.

Elles sont ensuite annoncées sur le serveur Discord **Kingdoms AOE**.

Le lancement d'une saison est une action administrative.

---

## 3.3 Passage d'une saison à l'autre

Le passage d'une saison à une autre n'est **pas automatique**.

L'administrateur doit lancer manuellement la nouvelle saison.

Lorsqu'une nouvelle saison est lancée :

**toutes les données de la saison précédente sont réinitialisées.**

Il n'y a pas de progression automatique conservée d'une saison à l'autre.

Après cette réinitialisation, les joueurs peuvent s'inscrire pour la nouvelle saison.

Les maps utilisées pendant une saison peuvent toutefois être réutilisées lors d'une saison suivante.

---

# 4. Royaumes joueurs

## 4.1 Nombre de Royaumes

Pour la Saison II :

**2 Royaumes joueurs**

Ce nombre est un **paramètre configurable par l'administrateur**.

---

## 4.2 Nombre de Seigneurs

Pour la Saison II :

**4 Seigneurs par Royaume**

Ce nombre est également **modifiable par l'administrateur**.

---

# 5. Inscription des joueurs et création des Royaumes

Lors du lancement d'une saison, l'administrateur peut choisir entre deux modes.

## 5.1 Royaumes imposés

L'administrateur peut imposer les Royaumes.

Dans ce cas, les Royaumes sont définis par l'administration.

---

## 5.2 Royaumes non imposés

Si les Royaumes ne sont pas imposés :

Les joueurs peuvent choisir de devenir :

* **Roi**
* **Seigneur**

Un joueur qui devient Roi peut **suggérer le nom de son Royaume**.

Les autres joueurs peuvent ensuite, au moment de leur inscription, choisir de rejoindre un **Royaume déjà existant**.

Le nombre maximal de Royaumes reste celui défini dans les paramètres de la saison.

### Point restant à définir

La validation du nom proposé par un Roi n'est pas encore définie.

---

# 6. Territoires

Un territoire correspond à une **map d'Age of Empires II**.

---

## 6.1 Territoires des Royaumes joueurs

Valeur de base Saison II :

**5 territoires par Royaume**

Cette valeur est configurable par l'administrateur.

Avec 2 Royaumes :

* Royaume A : 5 territoires
* Royaume B : 5 territoires

Soit **10 territoires joueurs** au départ.

---

## 6.2 Territoires de Gaïa

Valeur de base Saison II :

**8 territoires pour Gaïa**

Cette valeur est configurable par l'administrateur.

---

## 6.3 Attribution des territoires

Les territoires sont sélectionnés **aléatoirement**.

L'ordre d'attribution n'a aucune importance.

Le système doit simplement garantir :

> **Aucun doublon de map.**

Exemple avec la configuration actuelle :

* 5 maps pour Royaume A ;
* 5 maps pour Royaume B ;
* 8 maps pour Gaïa.

Total :

**18 maps différentes.**

---

# 7. Liste des maps disponibles

La liste des maps n'est pas automatiquement constituée de toutes les maps du jeu.

Les administrateurs définissent une **liste personnalisée de maps autorisées**.

Le bot ne doit sélectionner que des maps présentes dans cette liste.

La liste devrait normalement contenir largement plus de maps que nécessaire pour une saison.

Aucun nombre minimum strict de maps n'est imposé.

Si la liste devient insuffisante, le bot doit avertir l'administrateur.

---

# 8. Maps utilisées

Une map est considérée comme **utilisée dès qu'elle est sortie dans Kingdoms**.

Une map sortie peut appartenir :

1. à un Royaume joueur ;
2. à Gaïa au début de la saison ;
3. à Gaïa lors du Jour du Seigneur ;
4. à Gaïa lors d'une Exploration.

Une map déjà sortie ne peut pas être tirée à nouveau pendant la même saison.

---

## 8.1 Réutilisation entre saisons

L'interdiction de doublon concerne uniquement la saison en cours.

Une map utilisée pendant une saison peut donc être utilisée à nouveau lors d'une saison suivante.

---

# 9. Éjection et remplacement d'une map

L'administrateur peut **éjecter une map** en cas de problème.

Cela peut notamment arriver si une map présente un bug, un problème technique ou tout autre problème empêchant son utilisation.

Si une map déjà attribuée est éjectée :

* elle est retirée ;
* le bot sélectionne automatiquement une nouvelle map ;
* la nouvelle map est choisie **aléatoirement** ;
* elle doit provenir de la liste des maps autorisées ;
* elle doit être une map **qui n'est pas encore sortie dans Kingdoms** ;
* elle ne doit donc appartenir à aucun autre Royaume ou à Gaïa.

Le remplacement est automatique.

Si aucune map de remplacement n'est disponible, le bot doit prévenir l'administrateur.

---

# 10. Gaïa

Gaïa représente le royaume contrôlé par l'IA.

Valeur de base :

**8 territoires**

Cette valeur est configurable.

Gaïa peut perdre des territoires lorsqu'un Royaume joueur les conquiert.

Gaïa peut également recevoir régulièrement de nouveaux territoires.

---

# 11. Attaques et défenses

Chaque Seigneur possède normalement :

* **1 attaque par semaine**
* **1 défense par semaine**

Les règles précises de calendrier et de disponibilité des attaques doivent être appliquées selon les paramètres de la saison.

---

# 12. Attaque contre un Royaume joueur

Une attaque doit être déclarée dans :

`⚔️-attaquer`

Le territoire ciblé est une map appartenant au Royaume adverse.

## Délai

Délai par défaut :

**6 heures avant l'attaque contre un Royaume joueur.**

Ce délai peut être modifié selon les paramètres prévus.

---

## Défense

Le Royaume défenseur doit répondre à la déclaration.

L'attaquant fournit ensuite l'identifiant du lobby AoE2 :

`aoe2de://...`

---

## Résultat

Si l'attaquant gagne :

> le territoire est capturé.

Si l'attaquant perd :

> le territoire reste au défenseur.

Les détails concernant les cas particuliers doivent encore être définis.

---

# 13. Attaque contre Gaïa

Une attaque contre Gaïa possède un délai par défaut de :

**3 heures.**

Une attaque contre Gaïa cible un territoire appartenant à Gaïa.

---

## 13.1 Nombre d'attaquants

Maximum :

**1 joueur par Royaume**

Maximum global prévu :

**7 Seigneurs provenant de Royaumes différents.**

Les autres Royaumes peuvent rejoindre l'attaque selon les règles prévues.

---

## 13.2 Réservation du territoire

Il est impossible de déclarer une deuxième attaque indépendante sur un territoire Gaïa déjà réservé.

Le premier joueur à déclarer l'attaque :

* réserve le territoire ;
* réserve le créneau.

Les autres Seigneurs peuvent ensuite rejoindre cette attaque.

---

## 13.3 Format

Le format de la partie peut évoluer en fonction du nombre de participants.

Une attaque Gaïa à plusieurs peut donc prendre la forme d'une partie de type FFA / multijoueur avec les différents Royaumes participants et l'IA.

---

## 13.4 Victoire

Si les joueurs gagnent contre Gaïa :

> le territoire est capturé.

Si les joueurs perdent :

> le territoire reste à Gaïa.

---

## 13.5 Partie non jouée

Si l'attaque n'est pas jouée :

> l'attaque est consommée et Gaïa gagne.

Un abandon entraîne également une victoire de Gaïa selon les règles prévues.

Les détails concernant les problèmes techniques et déconnexions restent à préciser.

---

# 14. Niveau de l'IA

Le niveau de l'IA de Gaïa dépend :

* de l'époque ;
* des bonus éventuellement obtenus par le Royaume.

Les niveaux exacts et la correspondance précise avec les difficultés AoE2 restent à définir précisément.

---

# 15. Évolution des époques

Le changement d'époque a lieu :

**tous les mercredis à minuit.**

Les époques sont :

1. Âge sombre
2. Âge féodal
3. Âge des châteaux
4. Âge impérial

---

## 15.1 Âge sombre

Gaïa :

**IA standard**

Bonus :

* +1 mariage
* +1 garnison

---

## 15.2 Âge féodal

Gaïa :

**IA intermédiaire**

Bonus :

* +1 technologie
* +1 mariage

### Ordre Royal

L'Ordre Royal revient au Royaume possédant le plus d'alliances.

Il permet de proposer une règle supplémentaire.

---

## 15.3 Âge des châteaux

Gaïa :

**IA extrême**

Bonus :

* +2 technologies
* +1 mariage

---

## 15.4 Âge impérial

Gaïa :

**IA extrême**

Bonus :

* +2 technologies
* +1 mariage

---

# 16. Jour du Seigneur

Le Jour du Seigneur est exécuté :

**tous les dimanches à 23h30.**

À ce moment-là :

### 1. Ajout des maps

**8 nouvelles maps** sont ajoutées aléatoirement à Gaïa.

Le nombre de maps est configurable.

Les maps doivent être :

* présentes dans la liste autorisée ;
* pas encore sorties dans Kingdoms ;
* différentes de toutes les maps déjà utilisées.

### 2. Cadastre

Les effets définis dans :

`🧾-cadastre`

sont appliqués.

Les effets des maps sont définis en amont par les administrateurs.

### 3. Diplomatie

Les alliances sont actualisées selon les maps possédées.

Cela détermine notamment les civilisations disponibles et les éléments liés au draft civilisationnel.

---

# 17. Exploration du samedi

Une exploration est organisée :

**tous les samedis à 14h.**

Chaque Royaume peut envoyer un Seigneur.

Une map qui n'est **pas encore sortie dans Kingdoms** est sélectionnée aléatoirement.

Cette map devient alors une map sortie et donc utilisable dans Kingdoms.

---

## Récompenses

Classement :

### 1er

* remporte la map ;
* +1 point technologique.

### 2e

* +3 points technologiques.

### 3e

* +2 points technologiques.

### Autres participants

* +1 point technologique.

La map explorée devient donc un territoire du Royaume gagnant.

Les détails concernant les égalités, absences et problèmes techniques restent à définir.

---

# 18. Alliances

Les alliances sont liées aux civilisations.

Les alliances sont actualisées selon les territoires possédés.

Le système de diplomatie détermine notamment :

* les civilisations disponibles ;
* les civilisations déjà obtenues ;
* les conditions permettant d'obtenir certaines civilisations ;
* les éléments du draft civilisationnel.

Les règles détaillées du calcul des alliances doivent encore être complètement définies.

---

# 19. Mariages

Un mariage permet à un Seigneur de se lier au Roi ou à la Reine d'une civilisation.

Le mariage permet notamment :

* de sécuriser une civilisation pour son Royaume ;
* d'empêcher les adversaires de l'obtenir ;
* de supprimer certaines conditions normales d'obtention.

Si le Seigneur marié perd un combat :

> l'alliance tombe.

La civilisation redevient alors disponible selon les règles du système.

Les détails exacts du fonctionnement administratif des mariages restent à préciser.

---

# 20. Technologies

Les technologies sont une ressource permettant d'utiliser différentes actions spéciales.

Les technologies actuellement définies sont :

---

## Embuscade — coût 2

Permet une attaque supplémentaire.

Délai minimum :

**1 heure**

N'importe quel joueur peut défendre sans utiliser son point de défense.

Utilisation consommable / répétable selon les règles prévues.

---

## Traquenard — coût 1

Réduit le niveau de l'IA de Gaïa de :

**2 niveaux**

Utilisation consommable / répétable selon les règles prévues.

---

## Patrouille — coût 2

Permet de refuser un créneau d'agression de :

**2 heures**

Limite :

**2 utilisations permanentes**

---

## Contre-espionnage — coût 2

Permet d'effectuer une attaque en utilisant un autre membre du Royaume.

Le véritable attaquant peut ainsi rester caché.

Les détails précis restent à définir.

---

## Sabotage — coût 1

Permet une mécanique de snipe.

Maximum :

**2 par partie**

Les détails précis restent à définir.

---

## Explorateur — coût 2

Permet d'obtenir une map sans déclaration d'attaque dans la zone de Gaïa.

Les détails précis restent à définir.

---

## Jeu d'armes — coût 1

Augmente la difficulté de défense contre les bots :

**+1 niveau de difficulté IA**

---

## Mariage arrangé — coût 3

Permet d'obtenir l'exclusivité d'une civilisation via un mariage avec une promise.

L'exclusivité est perdue si le Seigneur concerné meurt.

---

## Corruption — coût 4

Permet d'acheter un territoire sans confrontation.

Le territoire ne peut alors pas être attaqué par l'ennemi selon la règle actuelle.

L'ennemi reçoit :

**+1 technologie**

Les détails de durée et de protection restent à préciser.

---

## Garde Royale — coût 1

Protège un territoire contre une attaque.

Bonus :

**1 technologie / 24h**

Les détails de fonctionnement restent à préciser.

---

# 21. Traités

Les traités deviennent disponibles à partir de :

**l'Âge féodal.**

Le Royaume possédant le plus de civilisations peut proposer un traité.

Un traité correspond à une **règle supplémentaire**.

La proposition est soumise au vote :

* POUR
* CONTRE

Tous les participants concernés votent.

Si la majorité est obtenue :

> le traité est appliqué.

La décision doit être annoncée dans :

`📣-géopolitique`

Les modalités exactes de majorité, durée et annulation restent à définir.

---

# 22. Ordre Royal

À l'Âge féodal, le Royaume ayant le plus d'alliances obtient l'Ordre Royal.

Le Roi de ce Royaume peut proposer une règle supplémentaire.

La requête est envoyée aux développeurs.

Tous les participants votent :

* POUR
* CONTRE

Si la majorité est obtenue :

> les développeurs tentent d'appliquer cette règle à l'Âge des châteaux.

Si la règle est trop complexe techniquement ou ne peut pas être implémentée à temps :

> elle pourra être reportée à une nouvelle saison.

---

# 23. Égalité finale

En cas d'égalité finale entre deux Royaumes :

**ShowMatch PA2**

est organisé.

Chaque Royaume choisit une map parmi **les territoires qu'il possède**.

Les joueurs des deux Royaumes s'affrontent.

Si l'égalité persiste :

* de nouveaux joueurs peuvent intervenir ;
* une nouvelle map appartenant au Royaume concerné est sélectionnée ;
* les confrontations continuent jusqu'à ce qu'un Royaume obtienne la victoire permettant de départager l'égalité.

Les détails précis du format du ShowMatch restent à définir.

---

# 24. Garnison

La mécanique de Garnison est actuellement :

> **mise de côté pour équilibrage.**

Elle ne constitue donc pas une priorité de développement actuellement.

Les règles envisagées précédemment comprennent notamment :

* transformation d'un point d'attaque/défense non utilisé ;
* renforts ;
* maximum de 3 garnisons par rencontre ;
* maximum de 3 renforts par Royaume.

Ces règles doivent être considérées comme **en travaux et non définitives**.

---

# 25. Salons Discord envisagés

Le système utilise notamment :

`⚔️-attaquer`

Pour les déclarations d'attaques.

`🕰️-délais-attaque`

Pour les informations relatives aux délais.

`🧾-cadastre`

Pour les territoires et leurs effets.

`📖-diplomatie`

Pour les alliances et civilisations.

`📣-géopolitique`

Pour les annonces et règles politiques / traités.

D'autres salons peuvent être ajoutés selon les besoins.

---

# 26. Gestion manuelle et automatisation

Le but du projet est de créer un système permettant au bot Discord de gérer automatiquement une grande partie de Kingdoms.

Cependant, l'administrateur doit conserver le contrôle du système.

L'admin doit pouvoir notamment :

* lancer une saison ;
* réinitialiser une saison ;
* modifier les paramètres ;
* définir la liste des maps ;
* éjecter une map ;
* gérer les Royaumes ;
* gérer les joueurs ;
* intervenir en cas de problème ;
* modifier certaines données si nécessaire.

---

# 27. Paramètres devant être configurables

Le système doit notamment permettre de configurer :

### Saison

* nombre de semaines ;
* nombre de cycles ;
* date/heure de début.

### Royaumes

* nombre de Royaumes ;
* nombre de Seigneurs par Royaume ;
* Royaumes imposés ou non.

### Territoires

* nombre de territoires par Royaume ;
* nombre de territoires de Gaïa.

### Maps

* liste des maps autorisées ;
* remplacement aléatoire ;
* possibilité d'éjecter une map.

### Attaques

* délais ;
* nombre d'attaques ;
* nombre de défenses ;
* paramètres Gaïa.

### Événements

* horaire du Jour du Seigneur ;
* nombre de maps ajoutées ;
* horaire de l'Exploration ;
* récompenses.

### Époques

* date/heure des changements ;
* niveau IA ;
* bonus.

---

# 28. Principe fondamental des données

Le bot doit distinguer :

### Données de configuration

Paramètres définis par l'administration.

Exemples :

* nombre de Royaumes ;
* nombre de joueurs ;
* nombre de territoires ;
* liste des maps ;
* horaires.

### Données de saison

Données générées pendant la saison.

Exemples :

* propriétaire d'une map ;
* alliances ;
* mariages ;
* technologies ;
* attaques ;
* défenses ;
* résultats.

Lorsqu'une nouvelle saison est lancée :

> les données de saison sont entièrement réinitialisées.

Les paramètres de configuration peuvent quant à eux être réutilisés ou modifiés par l'administrateur.

---

# 29. État actuel du projet

## Confirmé

* 2 Royaumes par défaut en Saison II.
* 4 Seigneurs par Royaume par défaut.
* 5 territoires par Royaume par défaut.
* 8 territoires Gaïa par défaut.
* Paramètres modulables par admin.
* Maps sélectionnées aléatoirement.
* Liste personnalisée de maps.
* Aucun doublon pendant une saison.
* Maps réutilisables entre saisons.
* Éjection d'une map possible.
* Remplacement automatique aléatoire par une map pas encore sortie.
* Saison lancée manuellement par l'admin.
* Réinitialisation complète entre les saisons.
* Inscription après réinitialisation.
* Royaumes imposables ou non.
* Choix Roi / Seigneur lorsque les Royaumes ne sont pas imposés.
* Un Roi peut suggérer le nom de son Royaume.
* Les joueurs peuvent rejoindre un Royaume existant.
* 4 semaines / 4 cycles par défaut.
* Territoires joueurs + Gaïa.
* Attaques et défenses.
* Progression par époques.
* Jour du Seigneur dimanche 23h30.
* Exploration samedi 14h.
* Alliances.
* Mariages.
* Technologies.
* Traités.
* Ordre Royal.
* ShowMatch en cas d'égalité.
* Garnison mise de côté pour le moment.

---

# 30. Points encore à définir

Les éléments suivants ne doivent PAS être inventés par le développeur ou l'IA.

Ils devront être décidés ultérieurement par l'administrateur/concepteur :

* validation du nom d'un Royaume ;
* nombre minimum de joueurs dans un Royaume ;
* départ d'un joueur ;
* changement de Royaume pendant une saison ;
* remplacement d'un joueur ;
* détails du draft des civilisations ;
* règles complètes des alliances ;
* choix précis des civilisations ;
* règles détaillées des attaques ;
* règles détaillées des défenses ;
* gestion des absences ;
* gestion des déconnexions ;
* gestion des problèmes techniques ;
* validation des résultats ;
* niveaux exacts de difficulté IA ;
* calcul précis des bonus IA ;
* détails des attaques Gaïa à plusieurs ;
* attribution d'un territoire Gaïa lorsqu'il y a plusieurs Royaumes participants ;
* règles précises des mariages ;
* fonctionnement détaillé des technologies ;
* majorité nécessaire pour les traités ;
* durée des traités ;
* règles détaillées de l'Ordre Royal ;
* format exact du ShowMatch final ;
* règles des égalités pendant l'Exploration ;
* règles de fair-play ;
* sanctions ;
* système complet de validation admin ;
* architecture technique définitive du bot ;
* éventuel site web.

---

# 31. Objectif technique

Le projet doit progressivement aboutir à un système dans lequel :

**Administrateur**
→ configure une saison

**Bot Discord**
→ initialise la saison

**Joueurs**
→ s'inscrivent / créent ou rejoignent des Royaumes

**Bot**
→ distribue les territoires

**Joueurs**
→ déclarent leurs actions

**Bot**
→ vérifie les contraintes et met à jour l'état du monde

**Événements automatiques**
→ font évoluer le monde chaque semaine

**Administrateur**
→ conserve la possibilité d'intervenir et de corriger les données.

Le bot doit donc être pensé comme le **gestionnaire de l'état du monde de Kingdoms**, et non simplement comme un bot de notifications Discord.

---

# 32. Règle importante pour le développement

Lorsqu'une règle n'est pas encore définie dans ce document :

> **le système ne doit pas inventer la règle.**

Elle doit être identifiée comme **À DÉFINIR** et pouvoir être ajoutée ultérieurement par l'administrateur.

Le projet doit privilégier une architecture permettant de modifier les règles et paramètres sans devoir reconstruire entièrement le système.
