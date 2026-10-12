# Kingdoms mod (conquête de territoires AoE2)

> Rewritten from the game designer's Season II reference
> ([../../PLANS/reference/kingdoms-mod-saison2.md](../../PLANS/reference/kingdoms-mod-saison2.md))
> — the reference is the **functional source of truth**. This directory
> adapts it to the Kingdoms stack. Where the reference and
> [DECISIONS.md](DECISIONS.md) disagree, the decisions win. Anything
> marked **À DÉFINIR** must not be invented by an implementation.

## Purpose

A territory-conquest meta-game on top of Age of Empires II: player
Kingdoms (Roi + Seigneurs) fight each other and Gaïa (the AI kingdom)
to conquer maps, week after week, across seasons. The bot is the
**world-state manager**: it owns territories, schedules weekly events,
enforces attack/defense budgets, and applies diplomacy.

## Concepts

- **Saison** — 4 semaines / 4 cycles par défaut (configurable), lancée
  manuellement par l'admin ; réinitialisation complète des données de
  saison au lancement d'une nouvelle saison.
- **Royaume** — player kingdom (2 par défaut en Saison II) : un Roi,
  des Seigneurs (4 par défaut). Gaïa est le royaume IA.
- **Territoire** — une map AoE2 ; tirée depuis la liste autorisée,
  jamais en doublon pendant la saison.
- **Attaques / défenses** — 1 attaque et 1 défense par Seigneur et par
  semaine ; délai de 6h (royaume joueur) / 3h (Gaïa) ; les attaques
  Gaïa sont des FFA « chacun pour soi » (gagnant unique).
- **Événements hebdomadaires** — Exploration (samedi 14h, FFA
  optionnel), Jour du Seigneur (dimanche 23h30 : +maps Gaïa, cadastre,
  alliances), changement d'époque (mercredi minuit).
- **Technologies** — la monnaie du jeu ; achète des actions spéciales
  (Embuscade, Traquenard, Patrouille, Contre-espionnage, Sabotage,
  Explorateur, Jeu d'armes, Mariage arrangé, Corruption, Garde Royale).
- **Diplomatie** — alliances liées aux civilisations, actualisées selon
  les territoires ; mariages ; traités ; Ordre Royal.

## Core integration

The mod is **game-bound** (AoE2 only, see [../README.md](../README.md) — game-bound mods):
hard-coded AoE2 options are intentional. Everything shared is owned by the core:

- **Seasons** — registered in the core season registry with the visible id
  `kingdoms-aoe2-<guild id>-<index>` (index incremental from 1, per guild).
  The legacy internal `s-<timestamp>` ids are a fallback only.
- **Maps & map pools** — sourced from the core game catalog
  (`GameDataService`); the mod grafts onto the existing
  `aoe2-maps` and `aoe2-map-pools` forum topics (in the `games` category)
  and never creates or duplicates them.
- **Players** — Discord users come from the core identity/user service;
  the mod never manages accounts itself.
- **Territories** — distinct from maps: a territory is backed by one
  AoE2 map but carries the mod's own function (ownership, protection).
  Its visible id is `territory:<season id>:<map key>`; the
  `kingdoms-territories` forum (in the `games` category, built by the
  core entity-forum engine) carries one post per territory, linked to
  its map's `aoe2-maps` post, ids shown in a footer.
- **Map pool rotations** — the season's pool reference lives on the
  core season document (`map_pool_id`); the core's `map_pool_history`
  activations are the rotations, referenced from the season.
- **Factions** — the core's `aoe2-factions` forum (one post per
  faction) is the link target for the mod's future faction-overlay
  entities; the mod will reference these posts, never duplicate the
  factions themselves. "Faction" is the platform-generic term
  (AoE2 calls them civilizations, StarCraft races); each post carries
  the localized name and the game's own civ help text, sourced from
  the vendored aoe2techtree dataset (MIT licence, game data under
  Microsoft's Game Content Usage Rules,
  `https://github.com/SiegeEngineers/aoe2techtree`) with the source
  referenced at the top of every post. Content resolves per the
  guild's configured locale (FR/EN) through the core's cache-aside
  content service (Redis first, Mongo second).

## Seeding (deploy time)

The mod's season data seeds with its own CLI, by visible ids (the
panels' footers):

```
python -m kingdoms.mods.kingdoms.kingdoms_seed_cli <seed_yaml> <guild_id>
```

The YAML file (see the ladder/core seeds for the deploy-time pattern):

```yaml
season_id: kingdoms-aoe2-<guild id>-<index>   # required — the footer id
kingdoms: [Aquitaine]                        # imposed kingdom names
territories:                                 # optional initial draw
  - { map_key: arabia, owner: gaia }
  - { map_key: kawasan, owner: Aquitaine }
lords:                                       # enrolled players
  - { player_id: "<discord id>", kingdom: Aquitaine, role: lord, display_name: Rollon }
```

Idempotent (re-run skips existing ids). The maps and pools themselves
come from the core AoE2 seed — the mod seed only references map keys.
The territory ids are `territory:<season id>:<map key>`.

## Usage

```text
/kingdoms …      — jo
ueur : inscription, royaume, actions
/kingdoms-admin … — admin : saison, paramètres, maps, interventions
```

Les salons déclarés par le mod incluent `⚔️-attaquer`,
`🕰️-délais-attaque`, `🧾-cadastre`, `📖-diplomatie`,
`📣-géopolitique`.

## See also

- [RULES.md](RULES.md) — règles du mod
- [ENVIRONMENT.md](ENVIRONMENT.md) — configuration et surfaces
- [DECISIONS.md](DECISIONS.md) — décisions validées après la référence
- [../../PLANS/reference/kingdoms-mod-saison2.md](../../PLANS/reference/kingdoms-mod-saison2.md) — référence fonctionnelle

## Faction/map localized content seeding

The vendored aoe2techtree dataset (`data/core/aoe2techtree/` in
kingdoms-services) feeds the `faction_content` Mongo collection for
every platform locale:

```
python -m kingdoms.core.games.aoe2.faction_content_cli [dataset_dir]
```

Run once per environment (deploy-time seeding); the forums' posts
then read Redis first, Mongo second, per the guild's locale.

## Activation par guilde (games/mods)

Rien n'est actif par défaut. Chaque guilde enregistrée demande l'accès
aux games/mods depuis son panel `/admin` (bouton « Demander l'accès ») ;
les bot admins reçoivent la demande par DM et l'approuvent ou la
refusent depuis leur panneau DM (`/admin` en DM, réservé BOT_ADMINS —
aucune action n'est visible ou cliquable par quiconque d'autre). Les
accords vivent dans la collection `guild_access` ; le provisioning des
mods (channels/rôles) et la synchro des forums ne s'exécutent que pour
les guildes ayant reçu l'accès.

## Scope des entrées du catalogue

Les maps et factions portent un `owner_guild_id` : `None` = global
(config de jeu, bot admins — le bouton « + Map globale » du panel est
réservé aux bot admins), ou une guilde = enrichissement local créé par
les admins de la guilde. Les listes sont scoping (les entrées de la
guilde + les globales) ; les posts des forums suivent ce scope dans
toutes les guildes.

## Refresh du contenu (maj du jeu)

Le bouton « Rafraîchir le contenu civs/maps » (panneau DM bot admin)
ou `python -m kingdoms.core.games.aoe2.content_refresh_cli`
réconcilie le catalogue avec le dataset vendored : création des civs
manquantes (ex. The Viking Sagas), upsert du contenu localisé (unités
uniques, tech tree, textes d'aide — tout ce qui évolue à chaque maj).
Attribution : voir `data/core/aoe2techtree/ATTRIBUTION.md` (MIT +
notice Microsoft Game Content Usage Rules, affichée en tête de post).

## Enrichissement maps Liquipedia (#247)

Les pages map de Liquipedia (`https://liquipedia.net/ageofempires/`)
ont une infobox structurée (`{{Infobox map}}` : type de terrain
Land/Hybrid/Water, murs, nomade, nombre de TC, joueurs, créateur,
période, image). Le job de sync
`python -m kingdoms.core.games.aoe2.liquipedia_cli <season_yaml>`
la récupère via l'API MediaWiki officielle (pas de scraping HTML,
User-Agent identifiant + contact, 1 req/2 s et `action=parse`
1 req/30 s) et stocke, par map du catalogue : une ligne `summary`
calculée, l'`image_url` directe (pas de hotlink), et l'infobox
complète dans `liquipedia_infobox` (clés minuscules, brute —
exploitable par des filtres/panneaux futurs). Le sync est
idempotent et reprenable (empreinte `liquipedia_page_sha` par map,
commit par map). Le contact requis par les conditions d'usage de
l'API est la variable d'environnement GitHub **non-secrète**
`LIQUIPEDIA_CONTACT` (déclarée sur chaque GitHub environment, lue
par deploy-env.yml puis le compose de l'env). Attribution : voir
`data/core/liquipedia/ATTRIBUTION.md` (CC-BY-SA 3.0 texte ; images
© Microsoft, même régime que le dataset aoe2techtree).

La fiche de chaque map porte aussi `game_versions` (les onglets
`tabs static` de la page — les versions du jeu pour lesquelles la
map existe : AoE2, AoM, AoE3, AoE4..., avec leur page wiki) et des
**tags de requête** normalisés dans `tags` : `terrain:land|hybrid|water`,
`water`, `walled`, `nomad`, `tc:<n>`. Les tags sont indexés dans
Mongo (index multikey sur `tags`, index couvert `(entity_id, locale)` —
 créés par le sync via `ensure_indexes`) et requêtables via
`FactionContentService.query_by_tags` (ex. toutes les maps hybrides
nomades : `query_by_tags(["terrain:hybrid", "nomad"], entity_prefix="map:aoe2:")`).
Les listes de maps par guilde (scope guilde + globales, la majeure
partie étant des maps publiques partagées) passent par
`FactionContentService.list_map_content` : la liste résolue est
cachée en Redis par guilde+locale (TTL 1 h), invalidée par le
tracker d'entités à chaque `store` — les maps publiques ne sont
lues qu'une fois par guilde, pas une fois par map.

## Contrat des listes : 25 éléments et le two-pattern select/par-id

Discord limite un sélect à **25 options** — la plateforme le respecte
par conception, avec **deux patterns distincts, jamais de pagination**
(une pagination de sélect masque silencieusement les options au-delà
de la page et ses boutons de page concurrencent le sync) :

1. **Sélect natif** quand la liste tient dans la limite : les jeux et
   les mods actifs (<= 25 par convention plateforme), les map pools
   non supprimés d'une guilde (<= 25), les membres d'un map pool
   (<= 25, `MAX_POOL_MAPS`).
2. **Par-id** au-delà : un bouton ouvre une modale où l'on colle l'id
   (`map:public:arena`, `pool:<guild_id>:<slug>`) ; pour les maps,
   l'**import en masse** (une map par ligne : id, nom anglais avec
   underscores ou URL Liquipedia, refus si un échec) couvre l'init
   d'un pool complet.

Quand un sélect n'est pas disponible (catalogue de maps > 25), la
réponse **explique les alternatives** : bouton « Ajouter une map
(id) », ou le bouton « Ajouter à un map pool » **du post de chaque
map** (toujours visible, il opère par id).

Ids des entrées (convention scope-first, l'id porte la visibilité,
pas le jeu) : maps `map:public:<slug>` / `map:<guild_id>:<slug>`,
pools `pool:public:<slug>` / `pool:<guild_id>:<slug>`. Les templates
des composants persistants matchent ces ids avec `.+` — **jamais**
`[^:]+` (les ids contiennent des deux-points, le clic mourrait en
silence : c'est la cause racine historique des « boutons qui ne
répondent pas »).

## Mappings de providers (ids propres)

Chaque provider a ses ids propres (civ ids, map names) qui peuvent être
renumérotés à chaque maj du jeu ; les ids stables du catalogue ne
bougent jamais. Les tables de remappage (catalogue -> id provider)
vivent dans la collection `provider_mappings` (cache Redis 10 min) et
s'éditent depuis le panneau DM bot-admin (select « Editer un mapping
de provider » puis modal `catalog=provider`, une entrée par ligne).
Le refresh de contenu applique ces mappings ; la source de la data
est toujours référencée (ligne `Source :` en tête de post + panneau).

## Processus provider ext-aoe2techtree (API gRPC)

Le contenu de jeu est servi par un processus provider dédié
(`KINGDOMS_PROCESS: ext-aoe2techtree`, port 50063 sur le réseau docker
uniquement) via le contrat gRPC `kingdoms.v1.Content` : contenu
localisé de factions/maps, index de factions, capabilities. Le core le
consomme via `EXT_AOE2TECHTREE_URI` ; sans cette variable, le refresh
retombe sur la lecture du dataset vendored en-process (comportement
actuel inchangé).

La **source amont est abstraite** (`UpstreamContentSource`) : le dataset
vendored par défaut (`AOE2TECHTREE_SOURCE=dataset`), ou une autre API
HTTP (`AOE2TECHTREE_SOURCE=api` + `AOE2TECHTREE_API_URL`) sans toucher
au contrat ni au core — remplacer la source par une autre API est un
changement d'environnement, pas de code. Les mappings de provider
(catalogue -> id provider) s'appliquent avant l'appel à la source, quelle
qu'elle soit.
