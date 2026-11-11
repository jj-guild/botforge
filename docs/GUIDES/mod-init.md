# Mod init — créer un mod proprement (`botforge mod init`)

Ce guide est **la référence** pour initier un mod : le layout cible, la
commande qui scaffold tout, et deux mods d'exemple réels (ladder,
kingdoms). Il sert aux humains **et** aux agents — une session qui crée
un mod commence ici, n'improvise rien, et économise ses tokens sur ce
qui compte (le design, pas le bootstrap).

Audience : game designers (via une session agent), développeurs, agents.

## 1. Un mod = un répertoire autonome

Depuis botforge#179, chaque mod vit dans **un seul répertoire
self-contained** dans `botforge-services` — l'extraction future vers un
repo externe (botforge-services#211 : un mod = un module UV + un
conteneur Docker + sa doc) sera un pur `git mv` :

```
modules/mods/<mod>/
  mod.yaml            déclaration (schéma ModRegistry, validée au boot)
  src/<mod>/          package python, importé comme botforge.mods.<mod>
  locales/en.yaml     catalogues de locale du mod (fusionnés au chargement)
  locales/fr.yaml
  tests/              tests du mod (lancés par make test)
  README.md           pointeur vers la doc canonique (repo botforge)
```

La documentation canonique du mod (règles, environnement) reste dans le
repo `botforge` : `docs/MODS/<mod>/` (README, RULES, ENVIRONMENT) —
jamais dans `botforge-services`. **Deux repos, deux vérités** : le code
et sa déclaration dans `botforge-services`, le design dans `botforge`.

L'ancien layout (`src/botforge/mods/<mod>` + `config/mods/<mod>.yaml`) —
reste supporté et **prioritaire en cas de collision** le temps de la
migration : une branche qui déménage son mod garde la main.

## 2. La commande

```bash
uv run botforge mod init <name> [--seasonal | --permanent] [--private --owner <discord-id>]...
uv run botforge mod list
```

`init` génère le répertoire complet ci-dessus : déclaration valide,
package avec les trois hooks de cycle de vie (`register`, `setup_hook`,
`close`), locales en/fr, test d'acceptation, README pointeur. Rien
n'est écrasé — un mod existant est refusé.

`list` affiche chaque mod déclaré et son layout (legacy ou modulaire).

## 3. Le contrat du mod (rappel)

- `mod.yaml` respecte le schéma validé au boot — voir
  [architecture/mods.md](../architecture/mods.md) : `id`, `enabled`,
  `seasonal` **obligatoire** (type du mod : saisonnier → panneau de
  cycle de vie + salons admin par saison ; permanent → panneau de
  config au niveau guilde), `settings`, `channel_groups`, `channels`
  (adressés `mod:key`), `roles`, `workflows`, `commands`,
  `dependencies`, `required_games`.
- **Les salons sont des données, jamais du code** :
  - `channel_groups` — les catégories Discord du mod, l'ordre de
    déclaration = l'ordre d'affichage ; `admin_only` (seuls les rôles
    admin du mod + les bot-admins le voient) et `read_only` (personne
    n'écrit) s'appliquent au groupe **et** à chaque salon
    (l'héritage par défaut) ;
  - `channels` — `group` (référence validée au boot), `kind`
    (`text`/`forum`/`announce` — une announce est admin-écrite,
    lisible par tous, read-only par défaut) ;
  - `access.view`/`access.post` — les **clés de rôles** déclarés par
    le mod (`view: [lord, king]`), résolues en noms au chargement ;
    un rôle marqué `admin: true` est l'audience des salons
    `admin_only`. Pas d'auto-heal : le bouton **Synchroniser** de la
    section est le seul chemin de re-création.
- **Le cycle de vie** : un mod suspendu (`ModLifecycleService`, par
  guilde) reste **gérable par les admins** mais **inutilisable par les
  joueurs** — `require_usable` est le point de contrôle de chaque flux
  joueur. La suspension est un flag, jamais un wipe.
- **Les inscriptions** (`settings.enrollment`) : critères déclaratifs —
  `min_elo`/`max_elo` (scalaire ou `{value: …, leaderboard: rm_1v1}`),
  `min_matches` (`{count: 10, days: 30, leaderboard: …}`),
  `requires_profile`/`requires_profiles` (un compte lié sur chaque jeu
  déclaré), `manual` (validation admin ; sinon auto-accept quand tous
  les critères passent). La **fenêtre** : `opens_at`/`closes_at`
  (timestamps ISO) ou `opens_before_start: 7d` (les inscriptions
  ouvrent avant le début de la saison).
- **Le map pool** : attaché à une saison (`map_pool_id` de la saison,
  rotation = une nouvelle saison avec un autre pool) ou au mod via
  `settings.map_pool` — un pool `used` est gelé, jamais réédité.
- Le code du mod ne parle **qu'aux seams du core** (hooks, UI SDK
  `botforge.discord.ui`, services core) — jamais à discord.py
  directement, jamais d'IDs de salon/rôle/guilde en dur.
- Le flag game-bound : un mod peut être lié à un seul jeu par design
  (kingdoms → AoE2) mais ne possède **jamais** les données du jeu — le
  catalogue appartient au core `GameDataService`, les saisons au
  registre core.

## 3b. Mods publics et privés

Un mod est **public par défaut**. Déclaré `private: true` dans le
`mod.yaml`, il devient **privé** :

- `owner_discord_ids` (ids Discord des propriétaires) est
  **obligatoire** — un mod privé sans propriétaire fait échouer le boot
  (fail loudly) ;
- le provisioning saute les guildes où **aucun** propriétaire ni
  bot-admin n'est membre ;
- les surfaces (menu home, dispatch des vues de mod) le cachent à
  quiconque n'est pas propriétaire ou bot-admin.

Le scaffold le fait en une commande : `botforge mod init <name>
--private --owner <id> [--owner <id>...]`. Usage typique : un mod en
cours de construction qui ne doit pas apparaître sur les guildes de
production avant d'être prêt.

## 4. Les mods d'exemple

Les deux pins de **déménagement** (le layout cible des mods réels,
`enabled: false` tant que leur code vit sur les branches
d'intégration) :

| | [ladder](../MODS/ladder/) | [kingdoms](../MODS/kingdoms/) |
|---|---|---|
| Type | saisonnier, game-agnostic | saisonnier, **game-bound (AoE2)** |
| Rôles | 3 (staff mod + player/season_staff par saison) | déclarés au déménagement |
| Déclaration | `modules/mods/ladder/mod.yaml` | `modules/mods/kingdoms/mod.yaml` (réelle, salons-first, depuis `vibe/drasah/main`) |
| Code | branche `vibe/merlin/main` (PR botforge-services#245) | branche `vibe/drasah/main` (PR botforge-services#244) |

Les deux répertoires `modules/mods/` pin **le layout cible et la
déclaration réelle**, avec `enabled: false` tant que le code vit encore
sur la branche d'intégration : le flag passe à `true` dans la même PR
que le déménagement mécanique du code (un PR par mod, CI verte à chaque
étape). C'est le pattern à suivre pour tout mod existant.

## 5. Le chemin complet d'un nouveau mod

1. `uv run botforge mod init <name> --seasonal` (ou `--permanent`)
2. Remplir `mod.yaml` (channels, roles, workflows, commands)
3. Implémenter dans `src/<name>/` contre les seams du core
4. Remplir `locales/en.yaml` + `fr.yaml`
5. Documenter dans le repo `botforge` : `docs/MODS/<name>/` depuis
   [TEMPLATE](../MODS/TEMPLATE/), ligne dans le
   [catalogue](../MODS/CATALOGUE.md) (maturité 1–2)
6. `make lint typecheck test`
7. Brancher le design sur la pipeline vibe (issue, PR, deploy, tag) —
   voir [VIBEWORKFLOW.md](../VIBEWORKFLOW.md)

## 6. Les systèmes génériques prêts à brancher

Le core fournit la machinerie complète — un mod déclaratif ne code que
ses spécificités :

| Système | Service core | Ce que le mod déclare |
|---|---|---|
| Parcours d'inscription | `EnrollmentService` | `settings.enrollment` (critères de la bibliothèque + `manual`) |
| Saisons (une active max, rotations de pools, rôles saisonniers, inscriptions) | `build_mod_season_stack` | `seasonal: true` + les rôles `per_season` |
| Inscription simple (register/unregister + sync rôles) | `MembershipService` | ses hooks métier |
| Dashboards admin (candidats/inscrits/acceptés) | `AdminModSection` + `EnrollmentService.dashboard()` | ses sections |
| Entités de l'univers (forums, posts) | `EntityForumSpec` | ses entités |

Le parcours d'inscription : apply → critères automatiques →
auto-accept / refus motivé / file d'attente → dashboard admin
(pending ⏳ / accepted ✅ / refused ❌) → accept/refus admin avec raisons
→ `MembershipService.register` (rôles de saison syncés). Les critères
automatisables : `min_elo`, `min_matches` (X parties / Y jours / jeu Z),
`requires_profile`, plus `manual` pour forcer la validation humaine.

Le questionnaire guidé complet (pour les novices comme pour les agents)
vit dans la skill
[mod-intake](../../.agents/skills/mod-intake/SKILL.md) — une session qui
crée un mod commence par elle.

## Voir aussi

- [architecture/mods.md](../architecture/mods.md) — le design du
  système (registry, cycle de vie, seams, contrat)
- [MODS/README.md](../MODS/README.md) — le système côté documentation
- [MODS/CATALOGUE.md](../MODS/CATALOGUE.md) — tous les mods, maturité
- [GUIDES/mod-developer.md](mod-developer.md) — le guide développeur
  (plus profond : SDK, tests, core-evolution)
- [la skill mod-intake](../../.agents/skills/mod-intake/SKILL.md) — le
  questionnaire guidé (le point d'entrée d'une session)
