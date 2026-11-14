# BotForge Roadmap

> Current state and next steps of the plan, regenerated from the GitHub
> issues — the past (done issues, change history) lives on GitHub and in
> the git log of the `sync/generated-artifacts` branch. Single writer: the
> [Generated artifacts](../.agents/skills/generated-artifacts/SKILL.md) workflow.

Status values: `todo` / `in-progress` / `in-review` / `done` / `blocked` / `dropped`.

## Current lot

- [Lot 3 — Kingdoms mod integration (manual, with Drasah)](https://github.com/jj-guild/botforge-services/milestone/3) — **15 open**

### Open issues — what blocks closing the current lot, in work order

Order: dependency wave → priority label → slack → issue number. Details and full graph: [DEPENDENCIES.md](DEPENDENCIES.md).

- [#321 — UX: one uniform pseudo-embed layout (discord-ui skill) — the id in the same place on every card](https://github.com/jj-guild/botforge-services/issues/321) — `todo` · P0 · size M
- [#334 — feat(ux): clickable images instead of menu links](https://github.com/jj-guild/botforge-services/issues/334) — `todo` · P0 · size M
- [#362 — [Epic] Kingdoms mod on the new main — platform preparation and reimplementation (replaces the mechanical-move track)](https://github.com/jj-guild/botforge-services/issues/362) — `todo` · P1 · size XL
- [#339 — Platform finalization for the kingdoms mod: drasah seam mapping, console ops, the clock, home buttons, candidates dashboard](https://github.com/jj-guild/botforge-services/issues/339) — `todo` · P1 · size L
- [#365 — [core+mod] Absorb the duplicated implementations (core+kingdom) into the platform seams — dedup audit](https://github.com/jj-guild/botforge-services/issues/365) — `todo` · P1 · size L
- [#368 — [mod] Kingdoms reimplementation tranches — phased port from vibe/drasah/main, CI green per tranche](https://github.com/jj-guild/botforge-services/issues/368) — `todo` · P1 · size L
- [#363 — [core] Home & admin navigation for mods — wire the menu:mod:* placeholders, kingdoms menu entries, the generic Profile button, clickable images](https://github.com/jj-guild/botforge-services/issues/363) — `in-review` · P1 · size M · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#366 — [mod] Kingdoms reimplementation skeleton — botforge mod init scaffold, current mod.yaml, locales, assets](https://github.com/jj-guild/botforge-services/issues/366) — `todo` · P1 · size M
- [#367 — [mod] Kingdoms mechanism conformance — forum posts, DMs, ephemeral and static views, the single ephemeral-window registry](https://github.com/jj-guild/botforge-services/issues/367) — `todo` · P1 · size M
- [#369 — [mod] Kingdoms season-2 game-design backlog — taverne tranche 2 (mercenary contracts, auto-betting, drink effects), volière balancing, geopolitics notifications, map thumbnails](https://github.com/jj-guild/botforge-services/issues/369) — `todo` · P2 · size L
- [#348 — Map types: let users enter and edit the classification (open, semi-open, closed...)](https://github.com/jj-guild/botforge-services/issues/348) — `todo` · P2 · size M
- [#343 — feat(pools): pool post member maps as a reusable Components V2 composition — nicer member list](https://github.com/jj-guild/botforge-services/issues/343) — `todo` · P2 · size S
- [#360 — Static views (pins) must refresh when the deployed version changes — a stored view id to detect staleness](https://github.com/jj-guild/botforge-services/issues/360) — `todo` · P2 · size S
- [#267 — mods-init platform — enrollment + criteria, per-mod seasons wire, admin dashboards, agent intake skill](https://github.com/jj-guild/botforge-services/issues/267) — `todo` · P3 · size XL
- [#326 — mods-init deliverable: test-env validation, companions, merge to main](https://github.com/jj-guild/botforge-services/issues/326) — `todo` · P3 · size M

## Upcoming lots

- [Lot 4 — Mod SDK & pro docs](https://github.com/jj-guild/botforge-services/milestone/4) — 14 open
  - The mod development experience goes pro: the SDK and its documentation.
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
- [#145 — fix(deploy): prod deploys are dead — the self-hosted runner was never reinstalled after the org rename](https://github.com/jj-guild/botforge-infra/issues/145) — `todo` · P0 · size M
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
- [#380 — core: the menu/panel template set — the types kingdoms uses, as reusable SDK archetypes](https://github.com/jj-guild/botforge-services/issues/380) — `in-review` · P1 · size M · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#381 — frame: the kingdoms mod dir is self-contained — commits everything but the mod, the mod declares itself, final rebase to vibe/mod-kingdom](https://github.com/jj-guild/botforge-services/issues/381) — `todo` · P1 · size M
- [#393 — feat(sdk): the operator's tools are ALWAYS LAST — the admin flip closes a home, the repair closes an admin surface](https://github.com/jj-guild/botforge-services/issues/393) — `in-review` · P1 · size S · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
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
- [#350 — [Post-rename] The resource-post SDK: one abstraction for every forum post, menu and sync surface — map/pool/faction first, mod resources next](https://github.com/jj-guild/botforge-services/issues/350) — `todo` · P2 · size XL
- [#395 — [Feature] Generalize the Jinja card templating: every view is a template (name + params), a modal-driven post tool, and custom map creation](https://github.com/jj-guild/botforge-services/issues/395) — `todo` · P2 · size L
- [#397 — External battery flaky: Liquipedia 429 on the maps-query-shape check](https://github.com/jj-guild/botforge-services/issues/397) — `todo` · P2 · size S
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
- [#396 — [Feature] Announcements through the templating mechanism once the visual generator lands (template + form + visual + params)](https://github.com/jj-guild/botforge-services/issues/396) — `todo` · P3 · size M
- [#374 — core: mod & game install/uninstall — the mods forum, one post per mod, autoload of present mods](https://github.com/jj-guild/botforge-services/issues/374) — `in-review` · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#375 — core: the mod SDK — no discord imports in a service, DB/cache through the seams only](https://github.com/jj-guild/botforge-services/issues/375) — `in-review` · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#376 — core: no external access from a mod — external data goes through a provider](https://github.com/jj-guild/botforge-services/issues/376) — `in-review` · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#377 — core: the installed games/mods ride the home menu — one button each, greyed when unavailable](https://github.com/jj-guild/botforge-services/issues/377) — `in-review` · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#378 — core: the per-mod home standard — enroll/leave, the enrolled list, the mod's own panels](https://github.com/jj-guild/botforge-services/issues/378) — `in-review` · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#379 — core: the per-mod admin standard — the season panel and the candidates management](https://github.com/jj-guild/botforge-services/issues/379) — `in-review` · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#384 — feat(ux): rename the user-facing "Synchroniser" action to "Réparer salons & rôles"](https://github.com/jj-guild/botforge-services/issues/384) — `in-review` · size S · PR [#386](https://github.com/jj-guild/botforge-services/pull/386)
- [#385 — chore(copy): remove over-descriptions and obsolete strings from logs and user-facing surfaces](https://github.com/jj-guild/botforge-services/issues/385) — `todo` · size S

Dropped (closed as not planned):

- [#142 — $1](https://github.com/jj-guild/botforge-infra/issues/142)
- [#143 — $1](https://github.com/jj-guild/botforge-infra/issues/143)
- [#144 — $1](https://github.com/jj-guild/botforge-infra/issues/144)
- [#18 — [Phase 3] Implement report mod](https://github.com/jj-guild/botforge-services/issues/18)
- [#151 — [Feature] Coaching mod: coach/reviewer pool, booking flow, session workspace, ratings & reputation, commission ledger](https://github.com/jj-guild/botforge-services/issues/151)
- [#167 — Sub-task: coaching mod — domain core (models, booking state machine, reputation, ledger)](https://github.com/jj-guild/botforge-services/issues/167)
- [#168 — Sub-task: coaching mod — Discord surface (commands, dynamic views, session workspace)](https://github.com/jj-guild/botforge-services/issues/168)
- [#316 — Integrate Drasah's Kingdoms-mod stack (vibe/drasah/main, 634 commits) — sync, split into the T1-T8 tranches, restack PR #244](https://github.com/jj-guild/botforge-services/issues/316)
