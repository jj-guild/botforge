# BotForge Roadmap

> Current state and next steps of the plan, regenerated from the GitHub
> issues — the past (done issues, change history) lives on GitHub and in
> the git log of the `sync/generated-artifacts` branch. Single writer: the
> [Generated artifacts](../.agents/skills/generated-artifacts/SKILL.md) workflow.

Status values: `todo` / `in-progress` / `in-review` / `done` / `blocked` / `dropped`.

## Current lot

- [Lot 3 — Kingdoms mod integration (manual, with Drasah)](https://github.com/jj-guild/botforge-services/milestone/3) — **26 open**

### Open issues — what blocks closing the current lot, in work order

Order: dependency wave → priority label → slack → issue number. Details and full graph: [DEPENDENCIES.md](DEPENDENCIES.md).

- [#333 — feat(profile): Profile button in every game menu — generic, no game select](https://github.com/jj-guild/botforge-services/issues/333) — `todo` · P0 · size M
- [#337 — feat(provisioning): general and discussions channels into the bot category — nothing at the root](https://github.com/jj-guild/botforge-services/issues/337) — `todo` · P0 · size M
- [#362 — [Epic] Kingdoms mod on the new main — platform preparation and reimplementation (replaces the mechanical-move track)](https://github.com/jj-guild/botforge-services/issues/362) — `todo` · P1 · size XL
- [#339 — Platform finalization for the kingdoms mod: drasah seam mapping, console ops, the clock, home buttons, candidates dashboard](https://github.com/jj-guild/botforge-services/issues/339) — `todo` · P1 · size L
- [#365 — [core+mod] Absorb the duplicated implementations (core+kingdom) into the platform seams — dedup audit](https://github.com/jj-guild/botforge-services/issues/365) — `todo` · P1 · size L
- [#368 — [mod] Kingdoms reimplementation tranches — phased port from vibe/drasah/main, CI green per tranche](https://github.com/jj-guild/botforge-services/issues/368) — `todo` · P1 · size L
- [#412 — [kingdom] Restaurer l'environnement technique admin de Drasah (paramètres / machine à temps / distributeur / demandes / journal-admin) — epic de portage](https://github.com/jj-guild/botforge-services/issues/412) — `todo` · P1 · size L · PR [#403](https://github.com/jj-guild/botforge-services/pull/403)
- [#421 — feat(ops): discord-init — one action to reinitialize a server (reset-db + install + ensure-tree + restart), the ops-tasks stack's flagship chain](https://github.com/jj-guild/botforge-services/issues/421) — `todo` · P1 · size L
- [#422 — feat(console): one action registry, three surfaces — every console action (core and per-mod) auto-available as /console and /console-mod <mod-name> with --param=value](https://github.com/jj-guild/botforge-services/issues/422) — `todo` · P1 · size L
- [#433 — fix(ux): the ephemeral views that hold state in memory die silently at restart — the wizard engine's closure callbacks, the session id in the custom_id, the expiry answer never silent](https://github.com/jj-guild/botforge-services/issues/433) — `todo` · P1 · size L
- [#366 — [mod] Kingdoms reimplementation skeleton — botforge mod init scaffold, current mod.yaml, locales, assets](https://github.com/jj-guild/botforge-services/issues/366) — `todo` · P1 · size M
- [#367 — [mod] Kingdoms mechanism conformance — forum posts, DMs, ephemeral and static views, the single ephemeral-window registry](https://github.com/jj-guild/botforge-services/issues/367) — `todo` · P1 · size M
- [#381 — frame: the kingdoms mod dir is self-contained — commits everything but the mod, the mod declares itself, final rebase to vibe/mod-kingdom](https://github.com/jj-guild/botforge-services/issues/381) — `todo` · P1 · size M
- [#407 — core: seam DM — implémentation IPlatform.send_dm + support des vues (DMs interactifs)](https://github.com/jj-guild/botforge-services/issues/407) — `todo` · P1 · size M · PR [#403](https://github.com/jj-guild/botforge-services/pull/403)
- [#408 — core: seam provisioning éphémère — create_channel étendu (overwrites, kind, position) + delete](https://github.com/jj-guild/botforge-services/issues/408) — `todo` · P1 · size M · PR [#403](https://github.com/jj-guild/botforge-services/pull/403)
- [#411 — [kingdom] Reprise du scope « s'enregistrer / postuler » (salon-parcours-v2) : recette live + axe esthétique + polish — Merlin owner, Drasah hors du périmètre](https://github.com/jj-guild/botforge-services/issues/411) — `todo` · P1 · size M · PR [#403](https://github.com/jj-guild/botforge-services/pull/403)
- [#424 — feat(console-ops): the repaired headless runner — nuke, reset-data, install (--games/--mods), ensure-tree, idempotent](https://github.com/jj-guild/botforge-services/issues/424) — `todo` · P1 · size M · PR [#405](https://github.com/jj-guild/botforge-services/pull/405)
- [#413 — env test — surfaces du mod kingdom (pins + slash /kingdom) n'atterrissent pas sur la guilde Kingdoms (TEST) : config d'env à vérifier + accès /logs test requis](https://github.com/jj-guild/botforge-services/issues/413) — `todo` · P1 · size S
- [#423 — [Feature] game-aoe2: filter aggregator match events to known ids — only enrolled/tracked players and followed matches reach state, transitions and logs](https://github.com/jj-guild/botforge-services/issues/423) — `in-review` · P1 · size S · PR [#405](https://github.com/jj-guild/botforge-services/pull/405)
- [#369 — [mod] Kingdoms season-2 game-design backlog — taverne tranche 2 (mercenary contracts, auto-betting, drink effects), volière balancing, geopolitics notifications, map thumbnails](https://github.com/jj-guild/botforge-services/issues/369) — `todo` · P2 · size L
- [#348 — Map types: let users enter and edit the classification (open, semi-open, closed...)](https://github.com/jj-guild/botforge-services/issues/348) — `todo` · P2 · size M
- [#425 — [views/menus] Réévaluation : les changements d'arbre (scopes) et de menus éphémères évacués de #405](https://github.com/jj-guild/botforge-services/issues/425) — `todo` · P2 · size M · PR [#405](https://github.com/jj-guild/botforge-services/pull/405) · PR [#403](https://github.com/jj-guild/botforge-services/pull/403)
- [#343 — feat(pools): pool post member maps as a reusable Components V2 composition — nicer member list](https://github.com/jj-guild/botforge-services/issues/343) — `todo` · P2 · size S
- [#267 — mods-init platform — enrollment + criteria, per-mod seasons wire, admin dashboards, agent intake skill](https://github.com/jj-guild/botforge-services/issues/267) — `todo` · P3 · size XL
- [#326 — mods-init deliverable: test-env validation, companions, merge to main](https://github.com/jj-guild/botforge-services/issues/326) — `todo` · P3 · size M
- [#402 — fix(enroll): an insights URL whose insights ID differs from the relic ID fails the player lookup — resolve by either id](https://github.com/jj-guild/botforge-services/issues/402) — `in-review` · P3 · size M · PR [#405](https://github.com/jj-guild/botforge-services/pull/405)

## Upcoming lots

- [Lot 4 — Mod SDK & pro docs](https://github.com/jj-guild/botforge-services/milestone/4) — 35 open
  - The mod development experience goes pro: the SDK and its documentation.
- [Lot 4 — Mod SDK & pro docs (botforge)](https://github.com/jj-guild/botforge/milestone/1) — 1 open
  - The botforge-side slice of Lot 4: the skills and docs riding the Mod SDK & pro docs track (same lot as botforge-services' milestone 4).
- [Lot 5 — Packaging (PyPI + registries)](https://github.com/jj-guild/botforge-services/milestone/5) — 1 open
  - Deliverables published: one PyPI package per micro-service and per mod, Docker images on both registries.
- [Lot 6 — Multi-bot, multi-game, multi-mod](https://github.com/jj-guild/botforge-services/milestone/6) — 17 open
  - Several distinct bots from the same code, each with its own mod set — validated multi-game/multi-mod before 1.0.0.
- [Lot 7 — Externalized storage & disposable VPS](https://github.com/jj-guild/botforge-services/milestone/7) — 2 open
  - Durable data off the VPS, and a VPS you can throw away and rebuild in minutes.
- [Lot 8 — Pre-1.0.0 review gate (code, DB, architecture, quality)](https://github.com/jj-guild/botforge-services/milestone/8) — 16 open
  - The final gate before v1.0.0: the full review pass, absorbing the former v0.999.0 scope (kingdoms-services#320, P0).

## Pre-roadmap (arch-discussion)

Committee territory: the architecture discussion is in flight; the
outcome is shaped into lot-sized issues once decided. No session
picks these up, and they never enter the work order.

- [#221 — [Archi] The three-package SDK split — botforge-surfaces (the wire contract) / botforge-sdk (the mod developer's single tool) / botforge-discord-sdk (the Discord implementation, reusable outside the project)](https://github.com/jj-guild/botforge/issues/221) — `todo`
- [#133 — Fluxer POC — self-host, port one bot surface, and assess the Discord-migration feasibility and cost](https://github.com/jj-guild/botforge-infra/issues/133) — `todo` · P2 · size M
- [#141 — [Feature] IaC init — plan: (1) Ansible foundation + VPN + Forgejo + Nextcloud on a dedicated VM, (2) GitHub→Forgejo tags & releases mirror, Forgejo as prod trigger, (3) prod runs on our stack under IaC](https://github.com/jj-guild/botforge-infra/issues/141) — `todo`

- [#174 — [Epic] Pre-1.0 content bar — AoE2 full-featured, ladder iso-JeanJack (kingdoms if ready)](https://github.com/jj-guild/botforge/issues/174) — `todo` · P0 · size XL
- [#179 — [Epic v1.0.0] Modular repo layout — one self-contained directory per mod and per game (code, config, locales, tests)](https://github.com/jj-guild/botforge/issues/179) — `todo` · P0 · size XL
- [#120 — Implement the automated tournament mod (Epic B, zero-admin tournaments)](https://github.com/jj-guild/botforge-services/issues/120) — `todo` · P0 · size L
- [#134 — ci: CLA check does not re-run on /cla comment](https://github.com/jj-guild/botforge/issues/134) — `todo` · P1 · size S
- [#169 — [Epic] Mod SDK — factorized high-level platform behaviors, the single entry point for mod development](https://github.com/jj-guild/botforge/issues/169) — `todo` · P1 · size XL
- [#170 — [Epic] Public PyPI packages & service versioning — clean packaging, one image per service, /status or stack-version decision](https://github.com/jj-guild/botforge/issues/170) — `todo` · P1 · size L
- [#197 — [Docs] Pre-1.0 reconciliation: enforcement claims match reality + the mod target architecture (per-mod dirs, PyPI artifacts, multi-bot)](https://github.com/jj-guild/botforge/issues/197) — `todo` · P1 · size M
- [#89 — Deploy 4 processes (bot-discord, svc-core, ext-librematch, ext-aoe2lobby) + gRPC networking](https://github.com/jj-guild/botforge-infra/issues/89) — `todo` · P1 · size L
- [#127 — Externalize MongoDB & Redis to the managed clusters + backup/restore drills off the prod compose](https://github.com/jj-guild/botforge-infra/issues/127) — `todo` · P1 · size L
- [#156 — [Kingdoms T1] Mod foundations — module, season config, Kingdom/Lord/Gaïa models](https://github.com/jj-guild/botforge-services/issues/156) — `todo` · P1 · size XL
- [#157 — [Kingdoms T2] Season & enrollment — admin launch, reset, King/Lord registration, queue, swaps](https://github.com/jj-guild/botforge-services/issues/157) — `todo` · P1 · size XL
- [#158 — [Kingdoms T4] Attacks & defenses — state machine, delays, weekly points, combat technologies](https://github.com/jj-guild/botforge-services/issues/158) — `todo` · P1 · size XL
- [#159 — [Kingdoms T5] Weekly events — ages, Lord's Day (+Gaïa maps, cadastre), Saturday exploration](https://github.com/jj-guild/botforge-services/issues/159) — `todo` · P1 · size XL
- [#160 — [Kingdoms T6] Diplomacy & marriages — civilization conditions, alliances, marriages (standard & arranged)](https://github.com/jj-guild/botforge-services/issues/160) — `todo` · P1 · size XL
- [#161 — [Kingdoms T7] Economic technologies — tech currency, Explorateur, Corruption, Garde Royale](https://github.com/jj-guild/botforge-services/issues/161) — `todo` · P1 · size XL
- [#162 — [Kingdoms T8] Season end — Conquest victory, tie ShowMatch PA2, closing report](https://github.com/jj-guild/botforge-services/issues/162) — `todo` · P1 · size XL
- [#163 — [Kingdoms T3] Territories & maps — allowed map catalog, draw without duplicates, ejection/replacement](https://github.com/jj-guild/botforge-services/issues/163) — `todo` · P1 · size XL
- [#129 — Mod Kingdoms — méta-jeu de conquête AoE2 (Saison II) : documentation & suivi](https://github.com/jj-guild/botforge/issues/129) — `todo` · P2 · size M
- [#173 — [Epic] Contributor journeys — documented playbooks: bugfix, game connector, platform, mod, test-env ops, prod ops](https://github.com/jj-guild/botforge/issues/173) — `todo` · P2 · size M
- [#177 — [Epic v1.0.0] Generic platform systems — admin views, registration, seasons, logs, Discord config: centralized code, mod declinations](https://github.com/jj-guild/botforge/issues/177) — `todo` · P2 · size XL
- [#178 — [Epic v1.0.0] Mod contract — manifest: games, seasonal flag, roles/channels (regex-capable), admin parameters](https://github.com/jj-guild/botforge/issues/178) — `todo` · P2 · size L
- [#180 — [Epic v1.0.0] Mod development guide — SDK quickstart, component reference, core-evolution protocol, PR boundaries](https://github.com/jj-guild/botforge/issues/180) — `todo` · P2 · size M
- [#181 — [Epic v1.0.0] Game-connector development guide — plug a new game (CS2, Valorant, Fortnite, Roblox, …) step by step](https://github.com/jj-guild/botforge/issues/181) — `todo` · P2 · size M
- [#182 — [Epic v1.0.0] OAuth account linking — Steam first (auto AoE2 profile resolution), Twitch later](https://github.com/jj-guild/botforge/issues/182) — `todo` · P2 · size L
- [#183 — [Epic v1.0.0] Readable pydoc — generated API docs hosted, linked from PyPI packages and the source](https://github.com/jj-guild/botforge/issues/183) — `todo` · P2 · size M
- [#90 — Cross-process observability — correlation ids, dashboards, degradation alerts](https://github.com/jj-guild/botforge-infra/issues/90) — `todo` · P2 · size M
- [#19 — [Phase 3] Implement clans mod](https://github.com/jj-guild/botforge-services/issues/19) — `todo` · P2 · size M
- [#21 — [Phase 3] Implement admin mod](https://github.com/jj-guild/botforge-services/issues/21) — `todo` · P2 · size M
- [#334 — feat(ux): clickable images instead of menu links](https://github.com/jj-guild/botforge-services/issues/334) — `todo` · P2 · size M
- [#437 — [Feature] Core: retire the core's pinned salons once every view and button has a pin-free entry point](https://github.com/jj-guild/botforge-services/issues/437) — `todo` · P2 · size M · PR [#403](https://github.com/jj-guild/botforge-services/pull/403) · PR [#428](https://github.com/jj-guild/botforge-services/pull/428)
- [#457 — feat(game): notices légales déclarées par game — conf yaml (aoe2 : GCUR Microsoft) + rendu par le SDK sur les cards détaillées vendant des ressources](https://github.com/jj-guild/botforge-services/issues/457) — `todo` · P2 · size S
- [#459 — docs(monétisation): rouvrir les objectifs de monétisation + nouvel axe « hébergement de bots » — version industrialisée et simplifiée de ce que fait Drasah](https://github.com/jj-guild/botforge-services/issues/459) — `todo` · P2 · size M
- [#109 — [Docs] Product plan — living document (vision, phases 0-4, modules A-J, monetization, sovereignty)](https://github.com/jj-guild/botforge/issues/109) — `todo` · P3 · size M
- [#110 — Epic A: Core domain (players, seasons, matches, scoring, entitlements)](https://github.com/jj-guild/botforge/issues/110) — `todo` · P3 · size XL
- [#111 — Epic B: Tournament machine (sign-ups, seeding, brackets, disputes)](https://github.com/jj-guild/botforge/issues/111) — `todo` · P3 · size XL
- [#112 — Epic C: Game data & drafts (maps, mappools, civs, DraftProvider)](https://github.com/jj-guild/botforge/issues/112) — `todo` · P3 · size L
- [#113 — Epic D: Ratings & stars (Glicko-2, history, badges)](https://github.com/jj-guild/botforge/issues/113) — `todo` · P3 · size L
- [#114 — Epic E: Presence (real-time availability)](https://github.com/jj-guild/botforge/issues/114) — `todo` · P3 · size L
- [#115 — Epic F: Team maker (LFG tickets, balanced teams, captain drafts)](https://github.com/jj-guild/botforge/issues/115) — `todo` · P3 · size XL
- [#118 — Epic J: Social & moderation (friends, private feedback, sanctions)](https://github.com/jj-guild/botforge/issues/118) — `todo` · P3 · size XL
- [#136 — [Epic K] Vibe-coding mod platform — assisted, UI-based mod co-construction for designers and community](https://github.com/jj-guild/botforge/issues/136) — `todo` · P3 · size XL
- [#138 — Design: architecture Discord salons-first du mod Kingdoms (Saison 2) — /kingdom unique + panels par salon](https://github.com/jj-guild/botforge/issues/138) — `todo` · P3 · size M
- [#141 — [Epic L] Contributor spaces — personal branches, personal test environments, personal prod slots](https://github.com/jj-guild/botforge/issues/141) — `todo` · P3 · size XL
- [#143 — [Task] Factorize the shared check workflows (CLA, auto-triage, validate-issue) into one implementation](https://github.com/jj-guild/botforge/issues/143) — `todo` · P3 · size M
- [#151 — Assign owners for the orphan mods (ladder, register) — ownership check debt](https://github.com/jj-guild/botforge/issues/151) — `todo` · P3 · size S
- [#152 — Drifts de session Drasah : mod marriage hors process, branches feat/*, pile de PRs à restacker](https://github.com/jj-guild/botforge/issues/152) — `todo` · P3 · size S
- [#154 — Mod kingdoms : replier le travail marriage dans le mod kingdoms (décision : feature T6, pas un mod)](https://github.com/jj-guild/botforge/issues/154) — `todo` · P3 · size S
- [#155 — Hygiène branches/PRs Drasah : renommage vibe/*, restack, doublon salons-first](https://github.com/jj-guild/botforge/issues/155) — `todo` · P3 · size M
- [#156 — Rétrospective : pourquoi Drasah s'est bloqué (pile de PRs, conventions dérivées) — et ce qu'on change](https://github.com/jj-guild/botforge/issues/156) — `todo` · P3 · size S
- [#171 — [Epic] Per-service DB accounts — enforced core/games/mods perimeter isolation, trivial provisioning for new services](https://github.com/jj-guild/botforge/issues/171) — `todo` · P3 · size L
- [#172 — [Epic] Non-Discord data access — exportable guild configs, game stats, per-mod data (GitHub Actions first)](https://github.com/jj-guild/botforge/issues/172) — `todo` · P3 · size L
- [#187 — Visual engine library — generalize TCG card generation into a reusable JSON+template+art+text visual generator](https://github.com/jj-guild/botforge/issues/187) — `todo` · P3 · size XL
- [#202 — Branch naming rules — review vibe/<user>/main in favor of per-mod integration branches (vibe/mod-<name>)](https://github.com/jj-guild/botforge/issues/202) — `todo` · P3 · size S
- [#5 — [Phase 2] Configure monitoring](https://github.com/jj-guild/botforge-infra/issues/5) — `todo` · P3 · size M
- [#94 — TEST: KingdomsService non monté au démarrage du bot (« no service » sur les actions de saison)](https://github.com/jj-guild/botforge-infra/issues/94) — `todo` · P3 · size S
- [#95 — Multi-tenant GitOps — personal envs (test-<user>), prod slots (per user+mod), provisioning scripts](https://github.com/jj-guild/botforge-infra/issues/95) — `todo` · P3 · size XL
- [#96 — [Task] Silent rollback — re-pin without re-deploying when the re-pinned image already runs](https://github.com/jj-guild/botforge-infra/issues/96) — `todo` · P3 · size M
- [#107 — P1: SimCord journeys exit 128 when the pinned deploy_commit is not reachable from main](https://github.com/jj-guild/botforge-infra/issues/107) — `todo` · P3 · size M
- [#111 — [v0.5.0] Docker Hub rate limits break the builds — mirror the base images on ghcr.io](https://github.com/jj-guild/botforge-infra/issues/111) — `todo` · P3 · size M
- [#116 — Bot down après reset de token : crash-loop de restart sur LoginFailure + healthcheck aveugle (scaling bot = 1 confirmé)](https://github.com/jj-guild/botforge-infra/issues/116) — `todo` · P3 · size M
- [#122 — fix(envlogs): the --service filter rejects botforge-ext-aoe2lobby (unknown service although listed)](https://github.com/jj-guild/botforge-infra/issues/122) — `todo` · P3 · size S
- [#124 — chore(deploy): the deploy/logs/seed workflows must not notify the repo owner — attribute the runs to the deployer alias](https://github.com/jj-guild/botforge-infra/issues/124) — `todo` · P3 · size S
- [#128 — env-console.yml + per-env TEST_GUILD_IDS — the dev console's infra companion](https://github.com/jj-guild/botforge-infra/issues/128) — `todo` · P3 · size M
- [#20 — [Phase 1] Create deployment scripts](https://github.com/jj-guild/botforge-services/issues/20) — `todo` · P3 · size S
- [#121 — Full-auto tournament mode (auto rounds, auto seeding, scheduled seasons — after the 80% mode is proven)](https://github.com/jj-guild/botforge-services/issues/121) — `todo` · P3 · size L
- [#148 — Add /drasah medieval greeting command](https://github.com/jj-guild/botforge-services/issues/148) — `todo` · P3 · size S
- [#175 — [Task] Fix first designer-session drifts: core-owned provisioning, single source of truth, stack & PR conventions (PR #170 stack)](https://github.com/jj-guild/botforge-services/issues/175) — `todo` · P3 · size L
- [#199 — [Task] CLI mode awareness — sandbox / pro / cowboy guardrails for humans and agents](https://github.com/jj-guild/botforge-services/issues/199) — `todo` · P3 · size M
- [#200 — [Task] botforge branch — print-only helper for the user branch lifecycle (bootstrap, sync, promote)](https://github.com/jj-guild/botforge-services/issues/200) — `todo` · P3 · size S
- [#201 — [Task] kingdoms env — personal environment companion (show, deploy, validate)](https://github.com/jj-guild/botforge-services/issues/201) — `todo` · P3 · size M
- [#214 — [Epic] Gestion-saison — panel admin de gouvernance live (Season II, design validé session Drasah)](https://github.com/jj-guild/botforge-services/issues/214) — `todo` · P3 · size XL
- [#216 — Tranche ① — Structure Discord : 11 catégories + salons par royaume (D70)](https://github.com/jj-guild/botforge-services/issues/216) — `todo` · P3 · size L
- [#219 — Tranche ② — panels d'état des salons royaume (hors Salle du Conseil)](https://github.com/jj-guild/botforge-services/issues/219) — `todo` · P3 · size M
- [#232 — [Kingdoms] Phase 1.1 — salon gestion-saison + tableau de bord épinglé + salon Temps de saison](https://github.com/jj-guild/botforge-services/issues/232) — `todo` · P3 · size M
- [#286 — chambre-des-comptes: le bouton ne répond plus sur drasah (v4/fix-v1)](https://github.com/jj-guild/botforge-services/issues/286) — `todo` · P3 · size S
- [#392 — chore(deps): revisit pynacl when discord.py allows >= 1.6.2 (GHSA-mrfv-m5wm-5w6w, moderate)](https://github.com/jj-guild/botforge-services/issues/392) — `todo` · P3 · size S
- [#458 — docs(discord): audit des règles Discord à respecter — Developer Policy / ToS / vérification, et synthèse documentée](https://github.com/jj-guild/botforge-services/issues/458) — `todo` · P3 · size M
- [#150 — Provision the personal environment `aramatu` (roster user Ozymendias)](https://github.com/jj-guild/botforge-infra/issues/150) — `todo`
- [#439 — pong implementation — domain, surface, timers, tests, i18n, enable (guide steps 3-7)](https://github.com/jj-guild/botforge-services/issues/439) — `todo` · PR [#432](https://github.com/jj-guild/botforge-services/pull/432)
- [#441 — feat(cards): calibrer les clés blob « Mode Antiquité » et « Handicap » (paramètres de partie, lot 3)](https://github.com/jj-guild/botforge-services/issues/441) — `todo` · PR [#405](https://github.com/jj-guild/botforge-services/pull/405)
- [#442 — core: the ephemeral-window registry & per-scope window modes — promote the kingdom SINGLE mode to the platform (extraction from vibe/mod-kingdom-rework)](https://github.com/jj-guild/botforge-services/issues/442) — `todo` · size M
- [#443 — core: registration bind/unbind events + guild-scoped profile bindings — the salon-gate substrate (extraction from vibe/mod-kingdom-rework)](https://github.com/jj-guild/botforge-services/issues/443) — `todo` · size M
- [#444 — core: the machine-room rule — category-level gates as declaration data (extraction from vibe/mod-kingdom-rework)](https://github.com/jj-guild/botforge-services/issues/444) — `todo` · size M
- [#445 — core: the sidebar order is data — declared position/reorder, category-bottom enforcement, deny_view inverse audience (extraction from vibe/mod-kingdom-rework)](https://github.com/jj-guild/botforge-services/issues/445) — `todo` · size M
- [#446 — core: the `surface` view kind + the R9 mod view-id contract (registry, loader, router, arch test) — extraction from vibe/mod-kingdom-rework](https://github.com/jj-guild/botforge-services/issues/446) — `todo` · size S
- [#447 — core: the per-mod admin console surface — auto-declared panel:mod:<name>:admin:console + the 🛠️ button + mod-scoped action registry (extraction from vibe/mod-kingdom-rework)](https://github.com/jj-guild/botforge-services/issues/447) — `todo` · size S
- [#448 — core: live pins — the `live` pin flag refreshed on gesture and on cadence (extraction from vibe/mod-kingdom-rework)](https://github.com/jj-guild/botforge-services/issues/448) — `todo` · size S
- [#449 — feat(profile): la fiche user — comptes agrégés/splittés (toggle) + liste paginée de matchs one-line + view/détails par match (lot courant)](https://github.com/jj-guild/botforge-services/issues/449) — `todo`
- [#450 — feat(cards): les types de cards multi-format (one-line, standard, detailed) pour chaque ressource — sdk/core (lot courant)](https://github.com/jj-guild/botforge-services/issues/450) — `todo`
- [#451 — feat(cards): le mécanisme multi-format cardable universel — registry explicite, instructions, skill, enforcement d'architecture (lot courant)](https://github.com/jj-guild/botforge-services/issues/451) — `todo`
- [#452 — feat(cards): les composants sdk de listes de cardables — pagination, view + détails par item, documentation du pattern (lot courant)](https://github.com/jj-guild/botforge-services/issues/452) — `todo`
- [#453 — feat(cards): le contrat d'extensibilité des items sdk/core — le défaut est sacré, l'extension est additive (lot courant, transverse)](https://github.com/jj-guild/botforge-services/issues/453) — `todo`
- [#455 — feat(feeds): lot 4 - le pattern forum feeds partout : un post par entité, envois groupés, pokes de cycle de vie (skill discord-forum-feeds)](https://github.com/jj-guild/botforge-services/issues/455) — `todo` · PR [#405](https://github.com/jj-guild/botforge-services/pull/405)
- [#462 — Tranche 43 — Pavillon de guerre : jouer le ShowMatch pour de vrai (design acté, reporté)](https://github.com/jj-guild/botforge-services/issues/462) — `todo` · PR [#428](https://github.com/jj-guild/botforge-services/pull/428)

Dropped (closed as not planned):

- [#142 — $1](https://github.com/jj-guild/botforge-infra/issues/142)
- [#143 — $1](https://github.com/jj-guild/botforge-infra/issues/143)
- [#144 — $1](https://github.com/jj-guild/botforge-infra/issues/144)
- [#18 — [Phase 3] Implement report mod](https://github.com/jj-guild/botforge-services/issues/18)
- [#151 — [Feature] Coaching mod: coach/reviewer pool, booking flow, session workspace, ratings & reputation, commission ledger](https://github.com/jj-guild/botforge-services/issues/151)
- [#167 — Sub-task: coaching mod — domain core (models, booking state machine, reputation, ledger)](https://github.com/jj-guild/botforge-services/issues/167)
- [#168 — Sub-task: coaching mod — Discord surface (commands, dynamic views, session workspace)](https://github.com/jj-guild/botforge-services/issues/168)
- [#316 — Integrate Drasah's Kingdoms-mod stack (vibe/drasah/main, 634 commits) — sync, split into the T1-T8 tranches, restack PR #244](https://github.com/jj-guild/botforge-services/issues/316)
