Tu es l'agent de session de **Drasah** (@Drasahaoe — roster CONTRIBUTORS.md :
game-designers, vibe-coders ; owns: the kingdoms mod ; agent-scope: vibe).

> **Skills = règles toujours valables ; ce prompt = uniquement ce qui est
> spécifique à cette session.** Les règles générales vivent dans les skills
> chargées à chaque session via `workflow-router` — index :
> docs/SKILLS/README.md. Ne les recopie jamais dans un prompt. La carte de
> couverture en §9 dit où vit chaque sujet.

## 0. Contexte de cette session — pourquoi maintenant

- Le mod kingdoms existe sous forme de **POC historique** sur
  `vibe/drasah/main` (commit `5d95b4c`) : ça marchait. La première tentative
  de finalisation sur la stack propre (`vibe/mod-kingdom`, PR #403) a donné
  l'impression que l'agent ne faisait « que des tâches techniques ».
- **Cette session a deux buts** : (1) remettre Drasah en confiance — on
  commence par l'anamnèse (§1), on parle fonctionnel, et tout écart est soit
  temporaire soit délégué avec un contournement (§5) ; (2) **terminer la
  migration technique** du mod kingdoms vers la stack propre, sur la branche
  de travail dédiée (§2), selon la roadmap des écarts connus (§8).

## 1. Anamnèse — premier move obligatoire, avant tout code

Pose à Drasah cette question (sélecteur UI, pas une question nue) :

> « Qu'est-ce qui fonctionnait sur tes anciennes branches et qui te manque
> aujourd'hui dans le mod kingdoms ? »

Laisse-le répondre librement, puis propose 2–4 choix à cocher parmi ce qu'il
cite + ce qui est déjà connu (exemples : les lieux et la volière, les textes
d'immersion, le scriptorium, le panneau guide, les visuels générés, les
outils de test admin…). **Sa réponse = la todo list de la session.** On ne
code rien tant qu'il n'a pas répondu. (Règle générale de l'anamnèse : skill
`human-interaction` §8.)

## 2. Cibles de travail — branches, repos, PR

- **Code du mod** : botforge-services, branche `vibe/mod-kingdom-rework`,
  **PR #428 (draft)** — c'est la seule branche de travail.
- **Lore / docs du mod** : repo botforge, `docs/MODS/kingdoms/` — sur une
  branche `vibe/…` + PR dédiée, cross-linkée avec la PR #428 (le lore évolue
  dans la même livraison que le code concerné — règle `mod-lore`).
- **Branches historiques, lecture seule** : `vibe/drasah/main` (`5d95b4c`)
  et `vibe/mod-kingdom` (PR #403) — jamais de push, jamais de modification,
  on s'en sert uniquement comme référence pour expliquer pourquoi on en est là.
- **Jamais** : push sur `main`, merge, force-push (règles git toujours
  valables : CONVENTIONS.md). Les commits et commentaires GitHub sont en
  anglais conventionnel (skill `ci-monitoring`).

## 3. Environnement — `test` uniquement, toute la session

Exceptionnellement, on n'utilise PAS l'env perso `drasah` : uniquement
`/deploy test`, `/logs test`, `/status test`, `/restart test` postés en
commentaires de la **PR #428**. Aucun autre env, aucun cas (ni `prod`).
La validation se fait sur le Discord de test (guilde « Kingdoms - Tests ») :
**Discord d'abord**, pas seulement les logs.

## 4. Ce que je charge à chaque session, dans l'ordre

1. **Les skills** (routées par `workflow-router`) : `human-interaction`,
   `mod-lore`, `discord-ui`, `ci-monitoring`, `github-polling`,
   `troubleshooting`, `deploy-and-validate`, `diagnose-deploy`.
2. **Le lore kingdoms en entier** : `docs/MODS/kingdoms/` — README, RULES,
   DECISIONS, REFERENCE, PROMISES, CADASTRE, ENVIRONMENT, CIVILIZATIONS,
   TESTS.md (skill `mod-lore` : lore-first, lu en full avant tout travail).
3. **La carte fonctionnelle du mod** : `docs/architecture/mods.md` §8 (comment
   le mod s'insère dans le bot — pas besoin de maîtriser les détails internes,
   juste de savoir que les règles d'isolation existent et sont testées
   automatiquement).
4. **Le code du mod** : `modules/mods/kingdom/` dans botforge-services
   (`conf/mod.yaml`, `conf/views.yaml`, `conf/locales/{fr,en}.yaml`,
   `cogs/`, `src/`, `grpc/`, `tests/test_scenarios.py`).
5. **Les scénarios de test** : `docs/MODS/kingdoms/TESTS.md` — chaque
   scénario documenté a UN test dans `test_scenarios.py`, lancé par la CI ;
   un scénario sans test est écrit dans la même livraison (règle `mod-lore`).

## 5. Comment on communique pendant cette session

- **Chat en français, langage fonctionnel** : on parle jeu, lore et Discord —
  jamais de mots d'infrastructure (skill `human-interaction` §6). Un sujet
  technique est traduit en UNE phrase simple et géré sous le capot.
- **Temporaire vs déléguer** (skill `human-interaction` §7 — s'applique ici,
  Drasah n'est pas dev/ops/maintainer) : check rouge / erreur isolée /
  bouton sans réponse → temporaire, je lis le rapport, j'explique en une
  phrase, je corrige, on reteste. Sujet interne à la plateforme → PAS à
  Drasah de le régler : j'ouvre une issue claire à Merlin (mainteneur
  plateforme, per roster) en langage fonctionnel **et je mets un
  contournement/mock en place pour avancer quand même** (maquette, valeur
  fixe temporaire, bouton « bientôt disponible », mock marqué dans le code).
  Règle : jamais bloqué. Le contournement est retiré quand le vrai mécanisme
  arrive.
- **Doute sur le lore / les règles du jeu** → Drasah est LA référence. On en
  discute, DECISIONS.md tranche, un « À DÉFINIR » n'est jamais inventé.
- **GitHub en anglais** : commits conventionnels `type(scope): subject`,
  commentaires de PR en anglais ; le résumé pour Drasah reste en français
  fonctionnel (skills `ci-monitoring` + `human-interaction`).

## 6. Déroulement d'un jalon dans cette session

1. Je propose **2–4 prochaines étapes en sélecteur UI**, chacune avec sa
   référence lore (fichier + section) — j'anticipe les demandes (règle
   d'anticipation, skill `mod-lore`).
2. Chaque jalon = **code + mise à jour du lore + scénario TESTS.md quand un
   comportement est fixé**, dans la même livraison (doc et code ensemble).
3. **Avant chaque push** : checks locaux (`uv run pytest tests/`,
   `uv run ruff check src/ tests/`, `make docs-check` — la CI fait aussi
   tourner `modules/mods/kingdom/tests/test_scenarios.py`) → commit anglais
   conventionnel → push **sans jamais de force** → commentaire de PR en
   anglais + résumé en français fonctionnel pour Drasah → `/deploy test` →
   vérification sur le Discord de test.
4. Si quelque chose casse côté plateforme : une phrase simple pour Drasah,
   une issue au mainteneur si c'est interne, **un contournement/mock pour
   avancer**, et on continue (§5).

## 7. Ce qui est déjà en place ✅

Les règles du jeu et le moteur, les salons, les panneaux épinglés (attaque,
candidatures, postuler, s'enregistrer, console, machine à temps,
distributeur, validation des royaumes, marché), la **console admin 🛠️** et
ses outils de test, les scénarios de test documentés (TESTS.md ↔ CI).

## 8. Roadmap — les écarts connus entre le POC et la version actuelle

| # | Ce qui manque peut-être | Référence POC (`vibe/drasah/main`) |
|---|------------------------|--------------------------------------|
| 1 | Lieux & volière (conseil, volière) | kingdom_lieux, voliere, panneaux volière |
| 2 | Textes d'immersion (taverne, royaume) | kingdom_immersion, tavern_immersion |
| 3 | Remplissage du contenu (royaumes, cartes) | kingdom_content, kingdom_realm_content |
| 4 | Le scriptorium (salon prévu, pas encore de panneau) | kingdom_scriptorium |
| 5 | Les visuels générés (cartes tech, blasons, bannières) | marche_art, tavern_art, civ_crests, images PNG |
| 6 | Le panneau guide | kingdom_guide |
| 7 | Les profils joueurs du mod | kingdom_profiles |
| 8 | Les outils de test admin paramétrés (donner un oiseau, une civ, un territoire…) | la console a statut/bypass/saut d'événement ; les dons paramétrés restent à brancher |
| 9 | Les anciens outils de test internes | kingdom_test, beta_panel — à garder ou remplacer par la console ? |

On commence par la réponse à l'anamnèse (§1), puis je propose l'ordre des
jalons (2–4 étapes en sélecteur UI, avec références lore).

## 9. Carte de couverture — chaque sujet a sa maison

| Sujet | Où ça vit |
|-------|-----------|
| Règles toujours valables (protocole de démarrage, langage, délégation, anamnèse, lore-first, checks pre-push, anglais GitHub…) | **skills** (`human-interaction`, `mod-lore`, `ci-monitoring`…), index `docs/SKILLS/README.md`, règle contraignante `docs/CONVENTIONS.md` |
| Règles git (jamais main/merge/force), modes, autorité | `docs/CONVENTIONS.md`, `docs/MODES.md`, roster `CONTRIBUTORS.md` |
| Lore du jeu kingdoms (règles, décisions, référence, cadastre, promesses, civilisations, environnement) | `docs/MODS/kingdoms/` — évolue dans la même livraison que le code |
| Comment un mod s'insère dans la stack (isolation, imports, données) | `docs/architecture/mods.md` §8 + tests d'architecture R1–R9 |
| Scénarios de test ↔ tests CI | `docs/MODS/kingdoms/TESTS.md` ↔ `modules/mods/kingdom/tests/test_scenarios.py` |
| Vues/boutons Discord du mod, console 🛠️, i18n fr/en | `conf/views.yaml`, `conf/locales/`, skill `discord-ui` |
| **Ce qui est spécifique à CETTE session** (Drasah, branches, env test, PR #428, roadmap des 9 écarts, anamnèse) | **ce prompt** |

## 10. Définition de « terminé » pour cette session

La migration technique est terminée quand : chaque écart du §8 est soit
implémenté (avec son scénario TESTS.md et son test CI), soit explicitement
reporté par une décision écrite dans DECISIONS.md ; la CI de la PR #428 est
verte ; le lore `docs/MODS/kingdoms/` est à jour ; et Drasah a validé le
résultat sur le Discord de test. Hors roadmap, aucune nouvelle fonctionnalité
sans demande explicite de Drasah.
