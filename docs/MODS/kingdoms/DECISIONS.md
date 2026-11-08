# Kingdoms mod — Décisions validées

> Décisions prises par le game designer **après** la rédaction de la
> référence Season II
> ([../../PLANS/reference/kingdoms-mod-saison2.md](../../PLANS/reference/kingdoms-mod-saison2.md)).
> En cas de désaccord entre la référence et ce document, **ce document
> gagne**. Les points non tranchés restent **À DÉFINIR** (référence §30)
> et ne doivent jamais être inventés par une implémentation.

## D1 — Cycle

- **Un cycle = une semaine.**
- La bascule du cycle a lieu au **Jour du Seigneur (dimanche 23h30)**,
  dernier événement de la semaine ; les attaques/défenses se
  rechargent à la bascule.
- À chaque bascule, le bot publie **la Gazette** dans
  `📣-géopolitique` : le résumé hebdomadaire du cycle (territoires par
  royaume, alliances, technologies dépensées). Validé par le game
  designer.

## D2 — Technologies = monnaie

- Les bonus d'époque « +1/+2 technologies » sont des **points
  technologiques** — la même monnaie que celle utilisée pour acheter
  les actions spéciales (référence §20).

## D3 — Mariages d'époque

- « +1 mariage » = un **mariage supplémentaire utilisable** par le
  royaume à chaque passage d'époque.
- **À définir** : les usages non consommés se cumulent-ils d'une époque
  à l'autre ou expirent-ils ?

## D4 — Garnison en pause

- Le bonus « +1 garnison » de l'Âge sombre est **inactif** en Saison II
  (mécanique mise de côté pour équilibrage, référence §24). Il est
  conservé dans la configuration (désactivé), pas supprimé.

## D5 — Exploration = FFA réel, optionnel

- L'exploration du samedi est une **vraie partie AoE2 en FFA** entre
  les seigneurs envoyés.
- La participation est **optionnelle** : chaque royaume *peut* envoyer
  un seigneur (pas d'obligation).
- Le classement 1er/2e/3e correspond au **classement final de la
  partie FFA** ; récompenses inchangées (1er : la map + 1 tech ;
  2e : +3 tech ; 3e : +2 tech ; autres participants : +1 tech).

## D6 — Attaque Gaïa = FFA, chacun pour soi

- Les seign
eurs participants ne sont **pas alliés** contre Gaïa :
  chacun joue pour lui-même, contre les autres participants et contre
  l'IA.
- **Un seul gagnant** : le vainqueur de la partie remporte la victoire
  **et le territoire pour son royaume**. Pas de cas multi-gagnants.
- **Pas de limite de temps** pour les attaques contre Gaïa (la limite
  de temps paramétrable s'applique uniquement à l'exploration —
  décision D44).

## D7 — Défense : n'importe quel seigneur

- Face à une attaque contre son royaume, **n'importe quel seigneur du
  royaume défenseur** peut défendre (pas seulement le propriétaire du
  territoire).

## D8 — Absence de défenseur : paramètre admin

- Si aucun défenseur ne répond dans le délai, le comportement est un
  **paramètre d'administration** à deux valeurs :
  1. **victoire automatique** de l'attaquant (territoire capturé sans
     jouer) ;
  2. **partie contre l'IA** : la rencontre se joue en multijoueur sur
     la map indiquée contre l'IA, selon les paramètres IA du royaume.

## D9 — Technologies : coûts paramétrables

- **Tous les coûts des technologies sont paramétrables** ; les valeurs
  de la référence (Embuscade 2, Traquenard 1, Patrouille 2,
  Contre-espionnage 2, Sabotage 1, Explorateur 2, Jeu d'armes 1,
  Mariage arrangé 3, Corruption 4, Garde Royale 1) sont les
  **valeurs par défaut**.

## D10 — Embuscade

- Un royaume disposant de la technologie Embuscade obtient une
  **attaque supplémentaire** ; le royaume attaqué peut défendre **sans
  dépenser son point de défense** (c'est une attaque d'embuscade).

## D11 — Contre-espionnage

- Disponible si le royaume possède la technologie. Lors de la
  déclaration d'une attaque sur un territoire, une **option
  supplémentaire** permet d'indiquer le nom d'un autre seigneur —
  existant et jouant la partie — de n'importe quel royaume (la
  couverture). **X temps avant le lancement de la partie**
  (paramétrable par l'admin), l'identité du **vrai attaquant** est
  révélée.

## D12 — Sabotage


- Utilisable **en attaque ou en défense**, **avant le début de la
  partie**, uniquement dans les attaques **seigneur contre seigneur**
  (royaume contre royaume) — **indisponible contre Gaïa**.
- Phase de snipe : chaque camp **retire de la liste des civilisations**
  une civilisation que son adversaire ne pourra pas jouer (et
  réciproquement).
- **Maximum 2 sabotages par seigneur et par rencontre** ; le compteur
  repart à zéro à la rencontre suivante (un seigneur peut détenir
  plusieurs sabotages, sans limite de stock).

## D13 — Explorateur

- Le royaume **reçoit la map gratuitement et immédiatement** (territoire
  de Gaïa, sans déclaration d'attaque, sans partie).

## D14 — Garde Royale

- Protège un territoire **sur une durée** : rend l'attaque du
  territoire impossible.
- La protection est de **24h**, prolongeable : dépenser **1 point de
  technologie ajoute 24h** supplémentaires.

## D15 — Corruption

- Permet d'obtenir un territoire **de n'importe quel royaume ou de
  Gaïa** en dépensant **4 points technologiques** (défaut).
- Le territoire obtient un statut **inattaquable** — et les autres
  joueurs ne peuvent pas non plus le **corrompre** — **jusqu'au cycle
  prochain**.

## D16 — Victoire de saison : Conquête

- Le royaume vainqueur est celui disposant du **plus de territoires** à
  la fin de la saison — type de victoire nommé **« Conquête »**.
- La règle pourra évoluer par la suite (autres types de victoire
  envisageables plus tard).

## D17 — Partie non jouée contre un royaume joueur

- Si l'attaquant ne s'est pas présenté, **l'attaque est consommée**.
- **Exception admin** : selon son appréciation, l'admin peut
  **réattribuer le point d'attaque** si l'absence a une excuse valable.

## D18 — Échelle numérique de l'IA

- Échelle validée : **1=Facile, 2=Standard, 3=Intermédiaire,
  4=Difficile, 5=Extrême** ; les effets se combinent avec plancher 1
  et plafond 5.
- **La progression d'IA liée aux époques ne concerne que Gaïa**
  (Âge sombre=2, Féodal=
3, Châteaux=5, Impérial=5) — **pas** les
  royaumes joueurs.
- Pour qu'un royaume dispose d'une IA plus forte (défense contre les
  bots), il faut utiliser **Jeu d'armes** : effet **permanent** (+1
  niveau).
- **Traquenard** réduit le niveau de l'IA **d'un royaume joueur ou de
  Gaïa** — effet **temporaire (une seule fois par utilisation)**,
  contrairement à Jeu d'armes. Traquenard **peut se cumuler** si le
  joueur en dispose plusieurs, à sa guise.

## D19 — Traités : paramètres de vote

- Qui vote : **paramétrable** — uniquement les Rois, ou tous les
  seigneurs.
- Majorité : **paramétrable** — 50%+1, ou unanimité.
- Si le vote est positif, un message annonce que **les Dieux ont
  entendu leurs paroles** ; l'application est **soit au cycle
  prochain, soit à la saison suivante** (selon la demande).
- La **durée dépend de la demande**.
- **Un seul traité par saison**.

## D20 — Validation des résultats

- Les joueurs valident le résultat, qui est **retrouvé
  automatiquement** : AoE2 respecte le **game contract** — le cœur de
  la plateforme gère déjà la récupération des résultats
  (`games/aoe2` + providers ext-librematch / ext-aoe2lobby, ADR-0020).
- En cas de litige, **l'admin tranche**.

## D21 — Nom de royaume

- Validé par **l'admin** ; longueur et caractères autorisés
  **paramétrables** par l'admin. L'admin peut aussi **imposer les
  noms** des royaumes (mode royaumes imposés).
- Hors périmètre actuel (version ultérieure) : bonus particuliers
  attribués à chaque royaume.

## D22 — Effectif des royaumes

- Un royaume peut démarrer avec **un Roi seul** ; les limites du
  nombre de seigneurs requis sont **paramétrables** par l'admin.

## D23 — File d'attente, départ et remplacement

- Des joueurs peuvent s'inscrire **sans royaume** (en **attente**),
  pour des raisons d'équilibrage.
- Un joueur peut **quitter la saison en cours** (option avec motif
  indiqué) ; l'admin peut alors affecter un **joueur en attente**.
- Le remplaçant **reprend l'état d'attaque/
défense de la semaine** du
  joueur sortant : si celui-ci avait déjà attaqué, le remplaçant ne
  peut pas non plus attaquer (anti-abus).

## D24 — Échange de joueurs entre royaumes

- Uniquement **en fin de cycle → nouveau cycle** : des joueurs peuvent
  être **intervertis** entre royaumes. Les **liens de mariages suivent
  la position** : si A (marié à l'Éthiopie) échange sa place avec B,
  B devient marié à l'Éthiopie.

## D25 — Remplacement d'un seigneur parti

- Un remplaçant ne récupère **que le mariage lié à la personne** ;
  les **territoires et les points sont communs** aux seigneurs du
  même royaume (donc rien à transférer).

## D26 — Remplacement du Roi

- Le Roi peut être **remplacé par un seigneur du même royaume**.

## D27 — Qui déclare une attaque

- **N'importe quel seigneur** peut déclarer une attaque (pas besoin de
  l'accord du Roi).

## D28 — Sabotage & Contre-espionnage : saisie

- **Sabotage** : les joueurs indiquent **sur Discord dans la fenêtre
  d'attaque/défense** s'ils font usage d'un sabotage, **juste avant la
  rencontre**.
- **Contre-espionnage** : proposé **lors de la déclaration
  d'attaque** — le joueur peut déclarer l'attaque **au nom d'un autre
  joueur** (cf. D11).

## D29 — Égalité à l'exploration

- En cas d'égalité, **le gain est attribué aux deux joueurs**.

## D30 — Exploration : aucun ou un seul participant

- **Aucun participant** : la map est ajoutée au royaume de Gaïa.
- **Un seul participant** : il obtient **automatiquement la map avec
  le lot du 1er**, sans nécessité de la jouer.

## D31 — Jour du Seigneur : épuisement des maps

- Improbable en pratique ; règle de repli : **lorsque Gaïa ne peut
  plus disposer de 8 nouvelles maps, la partie (saison) s'arrête
  automatiquement**.

## D32 — Alliances & civilisations

- Correspondance **map → civilisations** fournie par l'admin (le
  game designer fournira la table) ; l'obtention de certaines
  civilisations répond à des **pré-requis fournis par l'admin**.
- En début de s
aison, chaque royaume reçoit **X civilisations**
  (paramétrable par l'admin). **À la fin de chaque cycle**, les
  alliances s'actualisent **en fonction des mariages et des
  territoires conquis** ; on peut obtenir des civilisations au début
  puis **les perdre ensuite**.

## D33 — Choix des civilisations en partie

- Le bot **actualise automatiquement** la liste des civilisations
  jouables par royaume ; chaque seigneur choisit sa civilisation à sa
  convenance, à condition d'y **avoir accès** et qu'elle ne soit pas
  **sabotée** (un seigneur ne peut pas empêcher l'autre d'obtenir sa
  civilisation).

## D34 — Mariages

- Chaque seigneur peut se marier **une fois** ; la promise est une
  reine, princesse ou autre personnalité **ayant réellement existé**
  par civilisation (liste fournie par le game designer) — rôle **RP
  uniquement**, sans importance mécanique.
- Si le seigneur **perd un combat**, il perd le mariage : **au cycle
  prochain** il perdra l'effet du mariage.

## D35 — Traquenard / Jeu d'armes : durée des effets

- **Traquenard** expire **à la fin du combat**.
- **Jeu d'armes** s'active **automatiquement** à l'obtention et reste
  **jusqu'à la fin de la saison**.

## D36 — Achat multiple de technologies

- Un royaume peut acheter **plusieurs fois la même technologie** si
  les conditions sont respectées ; chaque technologie a un
  **paramètre de limite d'obtention**.

## D37 — Corruption : fin de protection

- La protection tombe **lundi minuit** (après le dimanche du cycle).

## D38 — Fin de saison

- La saison se termine **le lundi qui suit le dimanche du 4e cycle**
  (après les 4 cycles), à minuit — précisé par D52.

## D39 — Litiges techniques en partie

- Le joueur utilise une **sauvegarde du jeu** pour continuer la
  partie ; **l'admin se réserve le droit de trancher**. La règle sera
  ajoutée au règlement.

## D40 — Fair-play & sanctions

- Gestion **humaine** (admin) ; des règles de comportement seront
  ajoutées au règlement (document à part).


## D41 — Garnison : confirmée en pause

- Renforts et garnisons sont **mis de côté** ; réintroduits plus
  tard. Le combat d'attaque contre un royaume joueur est donc
  **1 attaquant vs 1 défenseur**, sans renforts.

## D42 — Attaques simultanées

- Un territoire avec une déclaration d'attaque **en cours ne peut pas
  être ciblé** par une nouvelle attaque.
- Un royaume peut **subir plusieurs attaques simultanées** sur des
  territoires différents.

## D43 — Patrouille

- Permet à un royaume de **refuser un créneau horaire d'agression**
  (ex. minuit–2h) : impossible pour les autres royaumes d'attaquer
  dans cette tranche. Application **immédiate** ; une attaque déclarée
  **avant** l'application dans cette tranche **n'est pas annulée**,
  mais aucune nouvelle attaque n'y sera possible ensuite.
- Un royaume peut **modifier sa tranche**, applicable **au cycle
  prochain**.
- **Maximum 2 patrouilles par royaume et par saison**, donc 4h de
  tranquillité au total si les deux sont possédées.

## D44 — Limite de temps : uniquement l'exploration

- **Pas de limite de temps** pour les attaques contre Gaïa.
- La **limite de temps paramétrable** s'applique **uniquement au FFA
  du samedi (exploration)** : au bout de X, le vainqueur est le
  joueur au plus gros score.

## D45 — Mariage arrangé vs mariage standard

- Le mariage arrangé donne **l'exclusivité** d'une civilisation,
  **appliquée instantanément**.
- Le mariage standard s'obtient **gratuitement via les âges/époques** ;
  la règle **d'un mariage par seigneur ne peut pas être contournée**
  (même par le mariage arrangé).
- « Si le seigneur meurt » = **perd un combat**, même logique que D34.

## D46 — Cadastre et conditions de civilisations

- Fournis par le game designer (Saison II) : effet de chaque map au
  Jour du Seigneur ([CADASTRE.md](CADASTRE.md)) et conditions
  d'obtention de chaque civilisation
  ([CIVILIZATIONS.md](CIVILIZATIONS.md)).
- Types d'effets de cadastre observés : offrir une technologie
  ponct
uelle (par jour/semaine/dimanche), un point de technologie,
  une civilisation, un mariage, une embuscade, un sabotage, un
  contre-espionnage, une exploration, réduire/augmenter des délais
  d'agression, augmenter la capacité de patrouille, offrir une
  garnison (garnisons en pause — D41), ou une map désignée /
  points de technologie au choix.
- **À valider/traduire en grammaire** : certaines conditions de
  civilisations sont référentielles (Hongrois = « appartenir au
  Royaume des HeN », Shu/Wei/Wu = posséder « Chinois ») et plusieurs
  comportent des seuils paramétrables (nombre de maps, types
  d'environnement) ; les types de maps (eaux, ouverte, nomade,
  désert/sable, montagne/colline, marais, lacs, dorée/or, start
  wall) doivent être saisis dans le catalogue de maps de l'admin.

## D47 — Garde Royale : compléments

- **Pas de cumul** : impossible de poser plusieurs Gardes Royales sur
  le même territoire.
- Achat : **24h de protection** sans autre dépense ; **prolongation :
  1 point de technologie pour 3h** (et non 24h).

## D48 — Explorateur : correction

- Le royaume reçoit une **map aléatoire qui n'est pas encore sortie**
  (pas une map possédée par Gaïa) — tirée parmi la **liste des maps
  possibles** (autorisées), donc jamais protégée par Corruption ou
  Garde Royale.
- **Consommable** : après usage, l'effet ne peut plus être réactivé —
  il faut relancer une nouvelle acquisition (expédition).
- La map reçue devient un **territoire du royaume immédiatement**.

## D49 — Ordre Royal = traité (une seule mécanique)

- Avec l'âge requis (Âge féodal), le royaume ayant le plus
  d'**alliances** obtient l'**Ordre Royal**, qui lui donne le droit de
  **proposer le traité** de la saison (un seul traité par saison —
  D19). Ordre Royal et traité ne sont donc **qu'une seule et même
  mécanique** : le porteur de l'Ordre Royal propose, les participants
  votent (paramètres D19), et si voté, l'application suit la demande
  (cycle prochain ou saison suivante).
- Si 
le porteur ne propose rien dans son délai (D51), **l'opportunité
  est perdue** : il n'existe qu'un Ordre Royal par saison, sans
  réévaluation.

## D50 — ShowMatch PA2 (égalité finale)

- **PA2 = Play All 2** : les joueurs doivent jouer **les deux
  matchs obligatoirement** (contrairement au Best-Of) — le vainqueur
  d'une manche PA2 est désigné **au score sur l'ensemble des deux
  matchs**.
- **Format : 1v1 PA2 successifs**. Premier duel entre un joueur de
  chaque royaume : si **2-0**, son royaume remporte la manche ; si
  **1-1**, un **autre seigneur** de chaque royaume enchaîne un
  nouveau PA2, et ainsi de suite jusqu'à un **2-0**.
- **Choix des maps et civilisations** : chaque royaume choisit ses
  maps **parmi ses propres territoires** et ses civilisations
  disponibles ; **aucune map ni civilisation ne peut être
  réutilisée** au cours du ShowMatch.
- **Repli** : si un royaume n'a plus de civilisations ou de
  territoires disponibles, la suite se joue sur **Megarandom en
  civilisation aléatoire**.
- **Suite du ShowMatch** : on continue jusqu'à une victoire ; si tous
  les 1v1 ont eu lieu, le format passe en **2v2, puis 3v3**, et ainsi
  de suite.

## D51 — Ordre Royal : attribution et délai

- **Alliance = civilisation** (le royaume ayant le plus de
  civilisations).
- Attribué **au passage d'Âge féodal (mercredi minuit)** ; il n'en
  existe **qu'un seul** par saison, manifesté au féodal.
- Le Roi porteur de l'Ordre Royal dispose de **24h pour faire sa
  proposition de traité** (délai paramétrable par l'admin) ; passé ce
  délai, **l'opportunité est perdue**.
- Le vote suit les paramètres D19 (Rois ou tous les seigneurs ;
  50%+1 ou unanimité).

## D52 — Heure de fin de saison

- La saison se termine **lundi minuit**, après le Jour du Seigneur du
  4e cycle (en cohérence avec D37, fin de la protection Corruption).

## D53 — Mariages : durée et budget

- Un mariage est **permanent** jusqu'à ce que le seigneur marié
  **perde un combat** (il perd alors le ma
riage, effet retiré au
  cycle prochain — D34).
- **Chaque seigneur peut se marier une seule fois** ; les « +1
  mariage » d'époque augmentent la **capacité de mariages du
  royaume** (nombre de seigneurs pouvant être mariés au total).

## D54 — Liste des promises

- La liste des personnalités historiques (promises par civilisation)
  est déposée dans [PROMISES.md](PROMISES.md) — **RP uniquement**.
- Elle couvre plus de civilisations que les 50 conditions documentées
  (Danois, Magyars, Mapuche, Muisca, Saxons, Tupi, Varègues…) :
  promises disponibles dès qu'une civilisation est obtenue.

## D55 — Saison II : 3 cycles

- La Saison II est une saison d'**essai** de **3 semaines = 3 cycles** ;
  D1 reste le défaut générique de 4 cycles. Amende, pour la Saison II,
  la partie « 4e cycle » de D38/D52.

## D56 — Fenêtre de protection

- **Aucune agression ni Corruption du dimanche 23h30 au lundi 10h** ;
  les points rechargés à 23h30 sont utilisables **pour déclarer**
  dès 23h30.
- Le **sprint final** se joue **lundi 10h → minuit**.

## D57 — Crescendo IA des époques

- Châteaux passe d'IA 5 à **IA 4** : l'IA de Gaïa suit un crescendo
  **2→3→4→5**, un palier par cycle ; l'Âge sombre est la phase de
  **setup** du lancement. Amende D18 sur ce point.

## D58 — Corruption : vol total et protection 48h

- La Corruption **vole** le territoire choisi **sans combat** :
  transfert **total et instantané** (bonus cadastre **et**
  civilisations) ; l'ancien propriétaire perd tout sur le champ.
- Protection **48h en temps réel** — la fenêtre de protection (D56)
  peut absorber le reste du chrono : comportement **voulu**.
  Amende D15/D37.
- **Maximum 2 Corruptions par saison et par royaume**
  (paramétrable) ; l'ennemi reçoit toujours +1 tech.

## D59 — Mariages : stock, verrou, exclusivité

- Le royaume dispose d'un **stock de mariages** (base paramétrable,
  **+1 par époque franchie**) ; chaque mariage consomme une unité —
  **résout le « À définir » de D3 : les unités se cumulent**.
- Un mariage actif **par seigneur** ; **remariage autorisé** après
  une perte si le stock le permet.
- **Verrou de 24h** (temps réel) : ni attaquer ni défendre ; la
  fenêtre de protection ne met pas le chrono en pause.
- **Exclusivité** : une civilisation déjà mariée ne peut être ciblée
  par aucun mariage (ni classique, ni arrangé) ; elle redevient
  mariable au Jour du Seigneur suivant la rupture.
- Amende D34/D53 ; le remplaçant d'un seigneur parti n'hérite
  jamais du mariage (D25).

## D60 — Mariage arrangé

- 3 techs ; **exclusivité instantanée** **sans consommer le stock** ;
  **verrou réduit à 6h** (temps réel). Amende D45 sur la durée du
  verrou.

## D61 — Garde Royale

- **Une seule Garde Royale active par royaume** à la fois.
- 24h de base ; **la Garde protège aussi de la Corruption**.
- Prolongation : 1 tech = **+3h**, à **coût croissant** (chaque
  prolongation supplémentaire coûte 1 tech de plus : 1, 2, 3…).
  Amende D47 sur la prolongation.

## D62 — Épuisement des maps : alerte admin

- Si Gaïa ne peut pas recevoir ses 8 maps au Jour du Seigneur, elle
  reçoit **ce qui reste** et le bot **alerte l'admin** ; **l'arrêt
  automatique (D31) est abrogé**.

## D63 — Semaine de lancement

- La semaine de lancement n'est **pas un cycle complet** : le
  premier cycle entier commence au premier Jour du Seigneur.
- Les **hostilités sont ouvertes dès le lancement**, y compris
  pendant l'Âge sombre (setup).

## D64 — La Paroisse

- Chaque royaume possède une **Paroisse** à trois paliers :
  **Chapelle** (gratuit — verrou mariage 24h, +1 mariage au stock
  chaque Jour du Seigneur), **Église** (2 techs — verrou 12h, mêmes
  bonus, se marier rapporte +1 tech), **Cathédrale** (3 techs —
  verrou 6h, mêmes bonus, Chantier Sacrée).
- **Chantier Sacrée** : map désignée (annonce publique) **Sacrée
  72h** (temps réel) — immunisée contre toute action technologique
  (y compris Embuscade) et **insensible à la conquête** ; seule une
  **attaque classique** peut la disputer ; points consommés
  normalement quel que soit le résultat ; **gagnant du duel :
  +1 tech**, quel que soit son camp.
- **Validation** (défense victorieuse ou aucune attaque) : la map
  devient **inattaquable et incorruptible jusqu'à la fin de saison**.
  **Défaite du défenseur** : Cathédrale **détruite** (3 techs
  perdus), la **map reste au défenseur**, la Paroisse retombe à
  l'Église.
- Un seigneur ne défend **le même chantier qu'une fois** ; **une
  seule relance** possible en repayant 3 techs. Tous les coûts et
  durées sont **paramétrables**.

## D65 — Harmonisation avec le dossier marriage/ (data-only)

- Le dossier `marriage/` reste **data-only** : source de données des
  promises (`princesses.yaml`) ; **le gameplay du mariage vit dans
  RULES.md §28** (renvoi croisé avec PROMISES.md).
- Respect de D34 : seules les promises `documented` et
  `tradition` sont tirées ; les noms `legendary` sont **exclus**
  du tirage Kingdoms (`allow_legendary_names` à faux).

## D66 — Politique de modification des paramètres

- Chaque paramètre d'ENVIRONMENT.md porte une politique :
  **free** (modifiable à tout moment, effet sur les événements
  futurs), **next-cycle** (appliqué au cycle prochain),
  **next-season** (prochaine saison).
- Les chantiers Sacrée **en cours** et les Cathédrales **validées**
  ne sont **jamais rétro-touchés** : la promesse « ad vitam
  aeternam » est tenue.

## D67 — Seigneur de Guerre (compensation d'exclusion)

- Si l'admin **exclut un joueur** et qu'**aucun remplaçant** n'est
  disponible en file, l'admin peut attribuer la promotion
  **Seigneur de Guerre** à un seigneur du royaume concerné.
- **Effet mécanique : À DÉFINIR** avant implémentation (Saison II).
- Les rôles Discord du mod sont **extensibles** : Roi et Seigneur
  aujourd'hui, d'autres rôles ensuite (dont Seigneur de Guerre) —
  le code parcourt les rôles déclarés, aucun n'est codé en dur.

## D68 — Patrouille (redéfinition — amende D43)

- La Patrouille s'achète **au Marché par le Roi** (coût 2 🔬).
- Chaque achat protège **un créneau horaire quotidien de 2h** :
  pendant cette tranche, **tous les territoires** du royaume sont
  protégés contre les **attaques joueurs** et les actions
  technologiques (**Corruption, Explorateur**).
- **Gaïa n'attaque jamais** — la Patrouille n'a pas d'effet contre
  Gaïa (redéfini : plus de « match patrouille vs IA »).
- **Limite : 2 achats par royaume et par saison** par défaut,
  **paramétrable par l'admin** dans le panel avant lancement.
- La tranche est **modifiable uniquement pendant la fenêtre de
  protection** (dim. 23h30 → lun. 10h) ; sans changement,
  **maintien automatique**.
- Le Roi reçoit un rappel via le **Pigeon-Voyageur** (D69).

## D69 — Pigeon-Voyageur (amende — catalogue des messages)

- Salon **éphémère par royaume** : rappels adressés au Roi.
  Visible uniquement de son destinataire ; contenu éphémère par
  nature.
- **Format acté** : narration médiévale en ouverture (une ligne,
  adressée au Roi), données brutes en deuxième ligne (horaires,
  décomptes, coûts), redirection de salon en troisième ligne
  (`→`).
- **Catalogue validé (14 messages)** — déclencheur, puis contenu :

1. **Achat de patrouille** (Marché, Roi) : confirmation de la
   tranche (ex. 02h00 → 04h00 chaque jour) + achats restants.
   Sans rappel du coût (déjà payé).
2. **Ouverture de la fenêtre de modification de patrouille** :
   horaire actuel, échéance lundi 10h00, maintien automatique
   sans action.
3. **Mariage scellé** : seigneur + civilisation + promise tirée
   au sort (D71), verrou restant, +1 🔬 versé au trésor.
4. **Cathédrale prête / Chantier Sacrée disponible** :
   invitation à désigner la map (palier Cathédrale).
5. **Chantier Sacrée en cours** : map couverte + décompte +
   annonce publique passée en 📣-géopolitique.
6. **Chantier validé (réussite)** : terre inattaquable et
   incorruptible jusqu'à la fin de saison.
7. **Chantier perdu (défaite, D73)** : territoire conservé,
   attaquant +1 🔬, protection Sacrée reportée par la
   Cathédrale sur une autre terre.
8. **Ouverture de la fenêtre de protection + Jour du Seigneur**
   (fusion, D56) : trêve, points attaque/défense rechargés,
   trésor, stock mariages, déclaration d'attaque planifiée
   possible après lundi 10h00.
9. **Levée de la trêve** : fin de la fenêtre lundi 10h00,
   sprint final jusqu'à minuit.
10. **Changement d'époque** : nom de l'époque, IA royaume,
    bonus (+1 🔬, +1 mariage au stock), trésor.
11. **Attaque déclarée contre le royaume** : royaume attaquant,
    cible, délai, date du match ; redirection gestion vers
    ⚔️ Champs de Bataille — le résultat part en
    📣-géopolitique.
12. **Garde Royale expirante** : territoire couvert, temps
    restant, coût de prolongation (croissant).
13. **Corruption ennemie subie** : territoire perdu,
    compensation +1 🔬, transfert de salon du territoire.
14. **Vassal parti** : place libre, admin alerté pour le
    remplacement.

- **Exclusions actées** : rappel de fermeture de fenêtre, rappel
  de limite de patrouilles, résultat d'Exploration (passe en
  rappel général en 📣-géopolitique), point d'attaque non
  dépensé (système à repenser séparément).

## D70 — Architecture Discord « salons-first » (amende — réconciliée avec l'issue #138)

Le serveur est organisé en **11 catégories**. Sources : issue #138
(design validé), config `kingdoms.yaml` (code), arbitrages Drasah
(D67–D74). En cas de divergence, cette décision prime.

1. **Profils** — un salon profil par royaume (`profil-aquitaine`, …) ;
2. **Général** — Présentation, Annonce, Règles, Saison, Update,
   Taverne, Suggestion ;
3. **Conscription** — 📝 Postuler (ouvert à tous, panel éphémère :
   rôle souhaité, nom de royaume si Roi, lien AoE II Insight + ID,
   acceptation des règles) · 📋 Candidatures (admin only, boutons
   ✅ validé / ⏳ en attente / ❌ refusé) ;
4. **Kingdoms** — 🗺 Carte (v2, non prioritaire) · 📣 Géopolitique
   (TOUTES les annonces d'événements : combats, chantiers,
   corruptions, traités, époques, exploration) · 🛒 Marché
   (boutique technos, Roi uniquement — D68/D74) ;
5. **Époque** — salon au nom de l'âge courant (renommé à chaque
   bascule, mercredi minuit), affiche les bonus de l'époque ;
6. **Royaume Gaïa** — 🛡 Patrouille (contenu **à définir plus
   tard** — trou assumé) · 🗺 Territoire (maps de Gaïa,
   consultables) · 🔍 Exploration (comptes-rendus du samedi 14h).
   **Gaïa ne fait que défendre** : elle n'attaque jamais, ne
   déclare rien, ne consomme aucune techno. *(Abroge « Gaïa n'a
   pas de catégorie » — première rédaction de D70.)* ;
7. **Royaume [Nom]** (une par royaume joueur, créée à la
   validation du nom par l'admin, visible uniquement du Roi + des
   Seigneurs du royaume + admins) — **8 salons** :
   - 💬 **Salle du Conseil** — le seul salon de discussion du
     royaume, privé (stratégie, coordination) ;
   - 🛡️ **Patrouille** — vue d'état : tranche(s) 2h achetée(s),
     achats restants, modification dim. 23h30 → lun. 10h00 ;
   - 🎖️ **Seigneurs** — vue d'état : roster privé (1 ligne par
     seigneur, rôles extensibles, mariages, budgets ⚔️/🛡️,
     badges ❌ parti / 🆕 nouveau) ;
   - 🏰 **Le-Royaume** — vue d'état : fiche épinglée (effectif,
     trésorerie 🔬, compteur territoires, Alliances, Paroisse
     niveau X/3 + stock mariages, Patrouille, IA, technos, garde
     royale) ;
   - 🗺️ **Territoire** — vue d'état : cartes paginées 5/page,
     protections, détail au clic ; la Corruption transfère le
     territoire de salon ;
   - 📜 **Alliances** — vue d'état : civs jouables + blasons,
     🔍 En savoir plus éphémère ;
   - ⛪ **Église** — vue d'état + actions : palier, stock
     mariages, mariages actifs (💍/💍✨) ; boutons 💍 Se marier,
     ⛪ Améliorer, ✨ Chantier Sacrée, 🔍 règles ;
   - 🕊️ **Pigeon-Voyageur** — rappels éphémères au Roi (D69,
     catalogue validé : 14 messages).
   Les salons royaume sont des **vues d'état silencieuses** :
   toutes les annonces d'événements vont en 📣-géopolitique ;
8. **Champs de Bataille** — 🕐 Délais-attaque · ⚔️ Attaquer ·
   💬 Pourparlers. La **gestion** attaque/défense vit ici, le
   **résultat** est annoncé en 📣-géopolitique ;
9. **Scriptorium** — 👑 Seigneurs (leaderboard public : tous les
   seigneurs classés par royaume + ELO — distinct du 🎖️ Seigneurs
   privé du royaume) · 📖 Diplomatie (traités, relations) · 🗺
   Cadastre (territoires + effets + conditions de civilisations) ;
10. **Admin** (admin only) — ⚙️ Paramètres · 🚀 Saison · 🗺 Maps ·
    ✅ Validations · 🔧 Interventions · 📋 Demandes ;
11. **Support** — Question · Signaler un Bug.

Les anciens salons globaux Patrouille/Territoire/Diplomatie sont
**supprimés**, remplacés par les versions par royaume (le
Seigneurs global devient le leaderboard Scriptorium). Les images
(maps, blasons) viennent des banques admin `map_images`,
`blason_images` (D70/ENVIRONMENT), non bloquantes.

## D71 — Promise tirée au sort

- Pour **tout mariage** (standard ou arrangé), la promise est
  **tirée au sort** parmi les promises éligibles (D65 : seules
  `documented` et `tradition`, pas de `legendary`).
- Le joueur choisit la **civilisation**, jamais la promise.

## D72 — Exclusion admin

- L'exclusion admin d'un joueur emprunte le **même parcours que le
  départ volontaire** (`service.leave()`) : le seigneur quitte le
  royaume, ses données de saison suivent les règles de
  remplacement en vigueur.
- Si aucun remplaçant n'est disponible : compensation **Seigneur
  de Guerre** (D67). *(Trou d'implémentation repéré : le retrait
  actuel ne retire que les rôles Discord — à câbler.)*

## D73 — Chantier Sacrée : issue de la défaite (amende D64)

- **Réussite** (défense victorieuse ou 72h sans attaque) :
  inchangé — le territoire devient **inattaquable et
  incorruptible jusqu'à la fin de saison**, la Cathédrale reste
  liée à ce territoire.
- **Défaite** : le royaume défenseur **conserve son territoire** ;
  l'attaquant gagne **uniquement +1 🔬** (pas le territoire).
- La Cathédrale **n'est pas détruite** (abroge ce point de D64) :
  elle **se relie automatiquement à un autre territoire du
  royaume, choisi aléatoirement**, et la **protection Sacrée
  validée s'applique à ce nouveau territoire**.
- Le royaume perd uniquement **le choix de l'emplacement** de sa
  protection Sacrée ; la Paroisse **reste au palier Cathédrale**.
- L'upgrade de paroisse est un **achat direct, toujours réussi**
  (pas de probabilité d'échec).

## D74 — Mariages : périmètre standard vs arrangé (amende D45)

- **Mariage standard (stock)** : cible uniquement une
  civilisation **déjà possédée par le royaume** — il **renforce le
  lien** d'obtention. Le bonus « se marier rapporte +1 🔬 »
  (paliers Église/Cathédrale) s'applique **uniquement au mariage
  standard**.
- **Mariage arrangé (Marché, 3 🔬)** : cible **n'importe quelle
  civilisation du jeu** ; exclusivité instantanée **sans consommer
  le stock** ; verrou **6h** (D60 inchangé).
- **Exclusivité commune** : une civilisation déjà ciblée par un
  **mariage actif** (quel que soit le royaume) **ne peut plus être
  ciblée par aucun nouveau mariage**, ni standard, ni arrangé.
- Dans le salon Église, les mariages actifs portent des **badges
  distincts** : 💍 (stock) et 💍✨ (arrangé).

## D75 — Catégorie Admin : architecture de gouvernance (amende D70, item 10)

- La catégorie **Admin** est redécoupée en **6 salons** (amende
  l'item 10 de D70 ; la règle 35 de RULES.md et la section
  « Channels and roles » d'ENVIRONMENT.md sont mises à jour en
  conséquence) :
  1. 🏰 **Royaume** — roster et entités (opérations neutres) ;
  2. ⚖️ **Équilibrage** — royaumes ET marché (coûts 🔬, Paroisse
     D64, Patrouille D68, Corruption D58, politiques D66) ;
  3. ⏱️ **Gestion du temps** — Lancer / Pause / Décaler Jour J /
     Clôturer + dashboard épinglé + fenêtre de protection D56
     (absorbe le salon Gestion-saison de la phase 1.1 de l'épic
     botforge-services#214 ; le marker `botforge:season:dashboard`
     reste inchangé) ;
  4. 🎯 **Compensation/Sanction** — trois objets : 📥 En attente
     d'arbitrage · 📖 Journal (rollback intégré) · 🚫 Bannis ;
  5. 🧩 **Paramètres & Mods** — fusion des anciens Paramètres,
     Saison, Maps, Validations et Interventions, + infra
     (provisionnement, resets, activation des mods, banques
     d'images) ;
  6. 📋 **Demandes** — point d'entrée unique du flux joueur
     (candidatures, noms de royaume D21, signalements, appels).
- **Socle commun** : un service unique **Journal + Snapshot +
  Rollback** partagé par les six salons. Toute action admin exige
  un **motif obligatoire (sans exception)**, une **confirmation
  avant/après**, une **annonce en 📣-géopolitique**, une **entrée
  de journal horodatée** et un **MP au joueur** (fallback : salon
  du royaume).
- **Rollback** : par action, fenêtre **2h dégressive**, **1 max
  par action**, rétention **48h** puis **archivage compacté**
  (jamais de suppression silencieuse).
- **Royaume (opérations neutres, jamais punitives)** :
  - ajout manuel d'un joueur (modal Joueur / Rôle / Royaume ou
    attente / AoE II Insight requis / ID jeu 6–20 requis / smurfs
    optionnel — mêmes effets qu'une candidature validée, l'admin
    passe au-dessus des verrous) ;
  - affectation d'un joueur de la file vers un royaume ;
  - réassignation d'un rôle en attente (l'intervention D17 vit
    ici) ;
  - commutateur **recrutement par royaume** + commutateur
    **global des candidatures** (tous deux indépendants du
    lancement, affichés sur le dashboard) ;
  - quotas (`kingdoms_count` / `lords_per_kingdom`, politique
    **free**) : modifiables librement en cours de saison ;
    surcapacité = **gel**, jamais d'éjection automatique ; un
    seigneur n'appartient qu'à **un seul royaume** ; **1 Roi
    obligatoire par royaume** — un royaume sans Roi (créé
    manuellement ou après départ) reste visible en état « sans
    souverain » jusqu'à affectation ;
  - échange de trône : l'entrant hérite de tout (att/déf,
    mariages), le sortant perd tout → file, MP avec motif ;
  - éjecter → liste d'attente (le rôle est conservé) ;
  - dissoudre : territoires → Gaïa, joueurs → file (aucun
    attribut conservé), salon du royaume supprimé ;
  - création manuelle d'un royaume en cours de saison (distinct
    de `kingdoms_preset`, qui reste le mode pré-lancement) ;
  - renommage admin d'un royaume (avec motif, distinct du flux
    joueur D21) ;
  - vue Gaïa / orphelins (territoires sans propriétaire).
- **Droit de fondation** (config saison, D66) : coches Roi ☐ /
  Admin ☐, aucune coche cochée = sauvegarde refusée ; ne vaut que
  pour la fenêtre initiale — **saison lancée → fondation
  verrouillée**, seule reste ouverte la candidature Seigneur en
  attente ; le rôle Roi ≠ droit de fonder (un joueur peut être
  Roi en file attendant un royaume admin).
- **Compensation/Sanction** : les sanctions passent
  **uniquement** par un dossier guidé, avec snapshot AVANT
  l'action : trancher un litige (le résultat forcé ne transfère
  **pas** automatiquement le territoire — le transfert reste une
  action admin séparée, avec motif et snapshot) → compensations
  standard cochables (crédit libre joueur OU royaume) → sanctions
  royaume (confisquer, dissoudre, bloquer la Corruption, joueurs
  → file ou bannis).
- **Bannir** : sortie + marquage **persistant entre saisons**,
  verrou du flux Postuler avec motif, vue « Bannis » séparée
  (hors file), révocable manuellement. L'exclusion sans
  bannissement suit D72 (parcours du départ volontaire +
  compensation Seigneur de Guerre D67). La dissolution-sanction
  reste un cas séparé dans le dossier.
- Mise en œuvre : botforge-services, épic #214 — une étape = une
  PR = un déploiement = validation terrain ; le socle commun
  (Journal + Snapshot + Rollback) est construit avec la première
  PR du salon Royaume.
