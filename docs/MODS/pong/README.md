# Pong mod (jeu de raquettes)

> Scaffolded from `docs/MODS/TEMPLATE/README.md`. Ce README est la doc
> de lore du mod : l'agent la lit intégralement à chaque session sur le
> mod (voir le skill mod-lore). Tout ce qui est marqué **À DÉFINIR**
> ne doit pas être inventé par une implémentation.

## Purpose and concepts

**À DÉFINIR** — décrire le mod : son but (premier mod d'initiation de
la plateforme ? duel de pong ?), ses concepts clés (les noms du jeu :
match, raquette, balle, score...) et un paragraphe de lore dont un
agent peut raisonner avant la lecture complète.

Lien [REFERENCE.md](REFERENCE.md) si une référence du designer existe.

## Channel tree: salons, categories, roles

Organisation Discord du mod, déclarée dans son `conf/mod.yaml`
(botforge-services) :

- **categories / groupes de salons** — une ligne chacun : clé, nom
  d'affichage, admin_only ?, rôles d'accès ;
- **salons** — clé, nom d'affichage, groupe, type (text/forum),
  admin-only, accès ;
- **roles** — le trio standard (candidat/membre/admin, préfixé par la
  clé du mod) plus tout rôle spécifique : nom d'affichage, ce qu'il
  contrôle ;
- **la règle machine-room** — dossiers staff-only pendant l'installation
  du mod, et le comportement de la porte install/uninstall.

## External system integration

- Le mod est-il **game-bound** ? Clé de jeu, ce que le mod lit du
  catalogue du core sans jamais le posséder ;
- **providers externes** — API/gRPC, gate de config, mapping d'ids ;
- **seams du core** — pattern d'id seasons
  `pong-<game>-<guild>-<index>`, forums d'entités, route de profil, etc.

## Views, buttons and actions of the mod

Surfaces Discord du mod, déclarées dans `conf/views.yaml` :

- chaque id de vue (`panel:mod:pong:…` / `menu:mod:pong:…` — le
  contrat de nommage R9) avec son type et ce qu'elle affiche ;
- boutons/actions : clé de label, emoji, style, custom-id
  (`pong:<component>:<payload>`), templates des dynamic items (regex
  `.+`, jamais `[^:]+`), guards (check admin au clic), confirm
  cards, modals ;
- **la console admin** — `panel:mod:pong:admin:console` (SDK) et les
  ops que le mod y enregistre (`mod="pong"`).

## Pinned salons

Quels panels sont épinglés, où (clé de salon), id de vue du pin et
builder, cycle de vie du pin (créé si manquant, rafraîchi en place,
réparé si le salon est supprimé, balayé à la désinstallation).

## Player / admin / bot interactions

Qui fait quoi, par flux :

- **player** — boutons/entrées slash, fenêtres éphémères, guards (âge,
  slot, cooldown, budget, locks…) ;
- **admin** — ops de console et de debug, confirm cards, effets et
  logging de chaque mutation ;
- **bot** — listeners d'événements et passes de boot (self-heal,
  reconcile), boucles planifiées, règle never-raise (chaque passe
  rapporte à l'utilisateur, jamais seulement en log).

## Usage

```text
/pong [arguments]   # seulement si le mod a des commandes slash
```

## See also

- [RULES.md](RULES.md) — règles du jeu (automatisables/testables)
- [ENVIRONMENT.md](ENVIRONMENT.md) — la configuration + la config de saison
- [TESTS.md](TESTS.md) — les scénarios de validation
- [../CATALOGUE.md](../CATALOGUE.md) — l'entrée du mod dans le catalogue
- [../../WORKFLOWS.md](../../WORKFLOWS.md) — workflows de la plateforme liés
