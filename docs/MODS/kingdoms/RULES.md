# Kingdoms mod — Règles

> Source fonctionnelle : la référence Season II
> ([REFERENCE.md](REFERENCE.md))
> corrigée par [DECISIONS.md](DECISIONS.md). Chaque règle ci-dessous est
> écrite pour être **automatisable** (testable par le bot). Tout point
> **À DÉFINIR** doit être tranché par le game designer avant
> l'implémentation correspondante — jamais inventé.

## Saison et cycle

1. Une saison dure par défaut **3 semaines = 3 cycles** en Saison II (essai — D55) ; défaut générique **4 semaines = 4 cycles** (un cycle =
   une semaine — D1) ; toutes les valeurs sont configurables (D9).
2. La saison est **lancée manuellement** par l'admin (date/heure
   annoncées) ; le passage de saison n'est jamais automatique.
3. Lancer une nouvelle saison **réinitialise toutes les données de
   saison** ; la configuration est conservée et modifiable. Les maps
   sont réutilisables entre saisons.
4. La bascule de cycle a lieu au **Jour du Seigneur (dimanche 23h30)** ;
   les points d'attaque/défense se rechargent à la bascule et sont **utilisables immédiatement pour déclarer** (règle 32) (1 attaque +
   1 défense par seigneur et par semaine). À chaque bascule, le bot
   publie **la Gazette** dans `📣-géopolitique` : résumé du cycle
   (territoires par royaume, alliances, technologies dépensées) — D1.
5. La saison se termine **le lundi minuit qui suit le Jour du Seigneur du dernier cycle** (3e en Saison II — D55) ; **dernier sprint de jeu lundi 10h → minuit** (D38/D52) ; le vainqueur est désigné à ce moment.

## Royaumes et inscription

6. Nombre de royaumes (2 par défaut) et de seigneurs par royaume (4 par
   défaut) : configurables. Gaïa est le royaume IA, ni jouable ni
   inscriptible.
7. Royaumes **imposés** (noms définis par l'admin) ou **non imposés** :
   les joueurs choisissent Roi ou Seigneur ; un Roi suggère le nom de
   son royaume, validé par l'admin (longueur et caractères
   paramétrables — D21) ; les suivants rejoignent un royaume existant.
   Un royaume peut démarrer avec **un Roi seul** (D22).
8. Des joueurs peuvent s'inscrire **en attente** (sans royaume) ;
   un joueur peut **quitter la saison** (option + 
motif) et l'admin
   affecte un joueur en attente en remplacement ; le remplaçant
   **reprend l'état attaque/défense de la semaine** du sortant
   (anti-abus — D23). Le Roi peut être remplacé par un seigneur du
   même royaume (D26).
9. Des joueurs peuvent être **intervertis entre royaumes uniquement en
   fin de cycle → nouveau cycle** ; les liens de mariages suivent la
   position (D24).

## Territoires et maps

10. Un territoire = une map AoE2, tirée aléatoirement depuis la
    **liste autorisée** définie par l'admin ; **aucun doublon** pendant
    la saison ; défaut : 5 par royaume joueur + 8 pour Gaïa (18 maps).
11. Une map est « utilisée » dès sa première sortie (attribution
    initiale, Jour du Seigneur, exploration, Explorateur) et ne peut
    plus être tirée avant la saison suivante.
12. Si la liste autorisée devient insuffisante, le bot **avertit
    l'admin**. Si Gaïa ne peut plus recevoir ses 8 nouvelles maps au Jour du Seigneur, **Gaïa reçoit les maps restantes et le bot alerte l'admin** (D62 — l'arrêt automatique est abrogé).
13. L'admin peut **éjecter une map** (bug, problème) : le bot la retire
    et tire automatiquement un remplacement non sorti dans la liste
    autorisée ; s'il n'en reste aucune, l'admin est prévenu.

## Attaques et défenses

14. Déclaration dans `⚔️-attaquer` : **n'importe quel seigneur** peut
    déclarer (D27). **Contre un royaume joueur** : délai 6h
    (configurable), l'attaquant fournit le lobby `aoe2de://…` ;
    victoire de l'attaquant = territoire capturé, défaite = le
    défenseur le garde.
15. Le combat est **1v1** : un attaquant contre un défenseur, sans
    renforts ni garnison (D41) ; **n'importe quel seigneur du royaume
    défenseur** peut défendre (D7).
16. Si aucun défenseur ne répond dans le délai : comportement
    **paramétrable admin** — victoire automatique de l'attaquant, ou
    partie contre l'IA sur la map (D8).
17. Attaquant absent : **l'attaque est consommée** ; l'admin peut réattribuer le point d'attaque **à son appréciation** (D17) ; le cadrage précis (limites, motifs, procédure) sera **défini ultérieurement par l'admin avant la saison**. Résultats
   
 récupérés **automatiquement via le game contract** ; litige =
    l'admin tranche (D20) ; problème technique = sauvegarde de la
    partie, l'admin tranche (D39).
18. Un territoire avec une attaque **en cours ne peut pas être ciblé**
    à nouveau ; un royaume peut subir plusieurs attaques simultanées
    sur des territoires différents (D42).
19. **Contre Gaïa** : délai 3h (configurable) ; max **1 seigneur par
    royaume**, **7 max** au total ; le premier déclarant réserve le
    territoire et le créneau ; les autres rejoignent la même attaque.
20. Attaque Gaïa = **FFA chacun pour soi** (D6) : un seul gagnant, qui
    remporte le territoire pour son royaume. **Pas de limite de
    temps** (D44). Partie non jouée ou abandon : **l'attaque est
    consommée et Gaïa gagne**.

## Époques (mercredi minuit, configurable)

21. Âge sombre → féodal → châteaux → impérial. L'IA de Gaïa évolue sur
    l'échelle numérique **1=Facile … 5=Extrême** (D18), en **crescendo 2→3→4→5** (D57) :
    - **Âge sombre** : IA 2 (Standard) ; +1 mariage
    - **Âge féodal** : IA 3 (Intermédiaire) ; +1 tech, +1 mariage ;
      Ordre Royal attribué (D51)
    - **Âge des châteaux** : IA 4 (Difficile) ; +2 tech, +1 mariage
    - **Âge impérial** : IA 5 (Extrême) ; +2 tech, +1 mariage
22. « +N technologies » = des **points technologiques** (monnaie — D2) ;
    « +1 mariage » = un mariage supplémentaire : la **capacité de
    mariages du royaume** (nombre de seigneurs pouvant être mariés)
    augmente d'une unité à chaque époque (D53).
23. La progression d'IA des époques ne concerne **que Gaïa** ; l'IA
    d'un royaume joueur ne change que par technologies : **Jeu
    d'armes** (+1 permanent jusqu'à la fin de saison) et **Traquenard**
    (−1 par utilisation, expire à la fin du combat, cumulable — D18,
    D35). Plancher 1, plafond 5.

## Événements hebdomadaires

24. **Exploration — samedi 14h** (configurable) : vraie partie AoE2
    **FFA** (D5), participation **optionnelle** (1 seigneur par
    royaume max) ; une map non sortie es
t tirée ; classement final de
    la partie : 1er remporte la map (territoire de son royaume) + 1
    tech ; 2e : +3 tech ; 3e : +2 tech ; autres participants : +1 tech.
    **Limite de temps paramétrable** : à l'échéance, le plus gros
    score gagne (D44). Égalité : **le gain est attribué aux deux
    joueurs** (D29). Aucun participant : la map va à Gaïa ; un seul
    participant : il obtient la map + le lot du 1er sans jouer (D30).
25. **Jour du Seigneur — dimanche 23h30** (configurable) :
    1) ajout de 8 maps (configurable) à Gaïa tirées parmi les non
    sorties ; 2) application du **cadastre**
    ([CADASTRE.md](CADASTRE.md)) ; 3) actualisation des **alliances**
    selon les territoires possédés et les mariages (D32).

## Diplomatie, mariages, traités

26. Alliances = civilisations (D51), recalculées **à la fin de chaque
    cycle** selon les mariages et les territoires conquis ; en début
    de saison chaque royaume reçoit X civilisations (paramétrable) ;
    on peut obtenir des civilisations puis les perdre (D32). Conditions
    d'obtention : [CIVILIZATIONS.md](CIVILIZATIONS.md).
27. Le bot **actualise automatiquement** la liste des civilisations
    jouables par royaume ; chaque seigneur choisit sa civilisation à
    sa convenance, à condition d'y avoir accès et qu'elle ne soit pas
    **sabotée** (D33).
28. Mariage : le royaume dispose d'un **stock de mariages** (valeur
    de base paramétrable, **+1 à chaque époque franchie** — D59) ; chaque
    mariage consomme **une unité du stock**. Un seigneur peut avoir **un
    mariage actif à la fois** ; le **remariage est possible** après une
    perte si le stock le permet. Une **civilisation déjà mariée ne peut
    être ciblée** par aucun mariage, ni classique ni arrangé (D59) ; elle
    redevient mariable au Jour du Seigneur suivant la rupture. Se marier
    applique un **verrou de 24h** (temps réel) : le seigneur ne peut
    **ni attaquer ni défendre** pendant cette durée (D59). La promise est
    une personnalité historique (RP uniquement — D54,
    [PROMISES.md](PROMISES.md)). Le mariage est **permanent jusqu'à ce
    que le seigneur perde un combat** (effet retiré au Jour du Seigneur
    suivant — D34/D53) ; la civilisation sécurisée reste jouable par le
    royaume jusqu'à ce Jour du Seigneur. Le remplaçant d'un seigneur
    parti **n'hérite jamais du mariage** (D25). Le **mariage arrangé**
    (3 techs) donne l'**exclusivité instantanée** d'une civilisation
    **sans consommer le stock**, avec un **verrou réduit de 6h** (D60).
29. **Ordre Royal = traité** (une seule mécanique — D49/D51) : à
    l'entrée à l'Âge féodal, le royaume ayant le **plus de
    civilisations** l'obtient ; son Roi 
dispose de **24h**
    (paramétrable) pour proposer le traité de la saison — un seul
    traité par saison (D19) ; vote POUR/CONTRE paramétrable (Rois ou
    tous les seigneurs ; 50%+1 ou unanimité — D19) ; si voté :
    annonce « les Dieux ont entendu leurs paroles » et application au
    cycle prochain ou à la saison suivante selon la demande ; sans
    proposition dans le délai, l'opportunité est perdue.

## Technologies (monnaie — D2/D9)

30. Points technologiques gagnés aux époques, à l'exploration, par le
    cadastre et par effet (Corruption : +1 tech à l'ennemi) ;
    dépensés en actions spéciales. **Coûts et limites paramétrables**
    (D9/D36) ; un royaume peut acheter plusieurs fois la même
    technologie dans la limite d'obtention de chacune. Les dix
    actions :
    - **Embuscade** (2) : attaque supplémentaire ; le défenseur
      volontaire ne dépense pas son point de défense (D10)
    - **Traquenard** (1) : −1 niveau IA (royaume joueur ou Gaïa) par
      utilisation, expire fin de combat, cumulable (D18/D35)
    - **Patrouille** (2) : crée une tranche quotidienne de 2h où
      **tous les territoires** du royaume sont protégés contre les
      **attaques joueurs et les actions technologiques** (Corruption,
      Explorateur) ; **Gaïa n'attaque jamais** ; achat au **Marché
      par le Roi** ; **2 achats max par royaume et par saison**
      (paramétrable admin) ; tranche modifiable **uniquement pendant
      la fenêtre de protection** (dim. 23h30 → lun. 10h), sinon
      maintien automatique ; rappel au Roi via le Pigeon-Voyageur
      (D68/D69)
    - **Contre-espionnage** (2) : déclarer l'attaque au nom d'un autre
      seigneur (la couverture) ; révélation du vrai attaquant X temps
      avant la partie, paramétrable (D11/D28)
        - **Sabotage** (1) : neutralise une civilisation adverse **pour
      la rencontre uniquement** (elle revient ensuite), utilisable même
      sur une civilisation mariée ; **2 max par seigneur et par
      rencontre**, compteur remis à zéro à la rencontre suivante (D12)
    - **Explorateur** (2) : map aléatoire **non sortie** reçue
      gratuitement et immédiatement, devient territoire du royaume ;
      consommable (D48)
    - **Jeu d'armes** (1) : +1 niveau IA permanent jusqu'à la fin de
      saison (D18/D35)
    - **Mariage arrangé** (3) : exclusivité instantanée d'une
      civilisation (D45)
        - **Corruption** (4) : **vole** un territoire de n'importe quel
      royaume ou de Gaïa **sans combat** — transfert **total et instantané**
      (bonus cadastre **et** civilisations) ; le territoire est
      **inattaquable et incorruptible 48h** (temps réel — la fenêtre de
      protection peut absorber le chrono, comportement voulu) ; l'ennemi
      reçoit +1 tech ; **max 2 par saison et par royaume** (D58)
    - **Garde Royale** (1) : **24h** de protection d'un territoire —
      ni attaque, **ni Corruption** ; **une seule Garde active par royaume**
      à la fois ; prolongation **1 tech = +3h**, à **coût croissant**
      (chaque prolongation supplémentaire coûte 1 tech de plus :
      1, 2, 3…) (D61)
## Garnison

31. **Mise de côté** pour équilibrage (Saison II — D4/D41) : aucune
    règle active ; les règles envisagées (transformation de points,
    renforts, max 3 garnisons / 3 renforts) sont **en travaux, non
    définitives**. Les effets « garnison » du cadastre sont conservés
    mais **inactifs**.


## Fenêtre de protection, lancement et Paroisse

32. **Fenêtre de protection** (D56) : **aucune agression ni Corruption du
    dimanche 23h30 au lundi 10h** ; les points rechargés à 23h30 peuvent
    être **dépensés pour déclarer** dès 23h30, mais aucun combat ni
    agression ne peut avoir lieu avant lundi 10h.

33. **Découpage de la saison** (D63) : la semaine de lancement n'est
    **pas un cycle complet** — le premier cycle entier commence au
    premier Jour du Seigneur ; les **hostilités sont ouvertes dès le
    lancement**, y compris pendant l'Âge sombre (setup).

34. **Paroisse** (D64) : chaque royaume possède une Paroisse à trois
    paliers :
    - **Chapelle** (gratuit, dès le lancement) : verrou du mariage
      classique **24h** ; **+1 mariage au stock à chaque Jour du
      Seigneur** ;
    - **Église** (2 techs) : verrou **12h** ; mêmes bonus ; **se marier
      rapporte +1 tech** ;
    - **Cathédrale** (3 techs) : verrou **6h** ; mêmes bonus ;
      **Chantier Sacrée** : le royaume désigne une map de son cadastre
      (annonce publique), qui devient **Sacrée pendant 72h** (temps
      réel) — immunisée contre **toute action technologique** (dans les
      deux sens, y compris Embuscade) et **insensible à la conquête**.
      Seule une **attaque classique** peut la disputer ; points
      consommés normalement quel que soit le résultat ; **le gagnant
      du duel reçoit +1 tech**, quel que soit son camp. **Défense
      victorieuse ou aucune attaque en 72h** : la Cathédrale est
      validée — la map devient **inattaquable et incorruptible
      jusqu'à la fin de saison**. **Défaite du défenseur** : la
      map **reste au royaume défenseur** ; l'attaquant gagne
      **uniquement +1 tech** (pas le territoire) ; la Cathédrale
      **n'est pas détruite** — elle **se relie automatiquement à un
      autre territoire du royaume, choisi aléatoirement**, et la
      protection Sacrée validée s'applique à ce nouveau territoire ;
      la Paroisse **reste au palier Cathédrale** ; le royaume perd
      uniquement **le choix de l'emplacement** (D73). Un seigneur
      ne peut défendre **le même chantier qu'une fois** ; **une seule
      relance** possible après échec en repayant 3 techs. L'upgrade
      de paroisse est un **achat direct, toujours réussi**. Tous les
    coûts et durées sont paramétrables.

## Salons Discord (architecture « salons-first » — D70)

35. Le serveur est organisé en **11 catégories** (D70) :
    **Profils** (profil par royaume) · **Général** (présentation,
    annonce, règles, saison, update, taverne, suggestions) ·
    **Conscription** (Postuler, Candidatures) · **Kingdoms**
    (Carte v2, Géopolitique — toutes les annonces d'événements,
    Marché) · **Époque** (salon au nom de l'âge courant) ·
    **Royaume Gaïa** (Patrouille à définir, Territoire,
    Exploration — Gaïa ne fait que défendre) · **Royaume [Nom]**
    (8 salons : Salle du Conseil, Patrouille, Seigneurs, Le-Royaume,
    Territoire, Alliances, Église, Pigeon-Voyageur) · **Champs de
    Bataille** (Délais-attaque, Attaquer, Pourparlers — la gestion
    attaque/défense vit ici, le résultat en Géopolitique) ·
    **Scriptorium** (Seigneurs leaderboard ELO public, Diplomatie,
    Cadastre) · **Admin** (Royaume, Équilibrage, Gestion du temps,
    Compensation/Sanction, Paramètres & Mods, Demandes —
    admin only — D75) · **Support** (Question,
    Signaler un Bug).
    La catégorie **Royaume [Nom]** est créée à la validation du
    nom par l'admin, visible uniquement du Roi + des Seigneurs du
    royaume + admins. Ses salons sont des **vues d'état
    silencieuses** (toutes les annonces vont en 📣-géopolitique),
    sauf la **Salle du Conseil**, seul salon de discussion privé
    du royaume. Les images (maps, blasons) viennent des banques
    admin `map_images`, `blason_images`, non bloquantes.
