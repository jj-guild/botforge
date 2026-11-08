# Contributing to BotForge (documentation repository)

New contributor? Read [docs/GUIDES/join-the-platform.md](docs/GUIDES/join-the-platform.md)
first — it explains what you need (GitHub + Mistral accounts, connector,
personal runner, signed CLA) before anything below.

This repository hosts no application code — only documentation, ADRs and
the Python scripts that validate docs and keep the generated artifacts in
sync. You do not need an AI agent to contribute: everything below runs
with a public clone and no credentials.

## Prerequisites

- Python 3.12+
- `git`
- A clone of [`botforge-services`](https://github.com/jj-guild/botforge-services)
  next to this repository (the doc validation reads its source and configs):

```bash
git clone https://github.com/jj-guild/botforge.git
git clone https://github.com/jj-guild/botforge-services.git
```

## Set up

```bash
cd botforge
```

No package installation is needed: the scripts use the Python standard
library only. If you plan to change the scripts themselves, keep them
stdlib-only and type-hinted.

## Your first contribution

1. **Pick or create an issue** (from a
   [template](https://github.com/jj-guild/botforge/issues/new/choose) —
   blank issues are disabled; non-compliant ones are flagged `invalid`).
2. **Create a branch** from `main`:

   ```bash
   git checkout -b docs/my-change main
   ```

3. **Edit the documentation.** Never edit `ROADMAP.md` or
   `docs/DEPENDENCIES.md` by hand — they are generated (see below).
4. **Validate before pushing** — this is the check CI runs on every PR:

   ```bash
   make session-check BOTFORGE_SERVICES=../botforge-services
   ```

   It runs docs validation (mod docs completeness, docstrings in the
   botforge-services source, Mermaid syntax) plus roadmap and
   dependency-graph drift. It fails closed with the exact artifact to
   fix. To run docs validation alone:

   ```bash
   make validate BOTFORGE_SERVICES=../botforge-services
   ```

5. **Sync the generated artifacts if you created or closed issues.**

   ```bash
   make sync-artifacts
   git add ROADMAP.md docs/DEPENDENCIES.md
   ```

   The scripts read the three repos through `gh api` (public, no
   credentials) and fail closed on unreadable repositories. New open
   issues must be registered in `ROADMAP.md` — the sync script warns
   until you add the row.
6. **Open a pull request.** Conventional Commit title (`docs:`, `fix:`),
   description linking the issue with a closing keyword (`Closes #N`).
7. Wait for review; the maintainer merges.

## Writing rules

- Everything in **English** (code, comments, docs, commits, PRs);
  game-related examples may be in French for i18n purposes.
- ADRs: any major architecture change gets an ADR in `docs/DECISIONS/`
  with a tracking issue first; check for numbers already reserved by
  open issues and in-flight PRs.
- Mermaid diagrams must use GitHub-compatible syntax (quote node labels
  containing `->` or `{}`; no colons inside unquoted labels).
- A change in `botforge-services` or `botforge-infra` without its doc
  update here is incomplete — docs and code change together.

## Code style (sync scripts)

- Python 3.12, type hints everywhere, stdlib only.
- Scripts are fail-closed: explicit error, non-zero exit, no partial
  writes.

## The vibe-coding model

This project is primarily built through an AI-agent workflow
([docs/VIBEWORKFLOW.md](docs/VIBEWORKFLOW.md)); agent sessions follow the
same checks you just ran. Human contributions are welcome and follow
exactly the path above — no agent required.

## CLA process

- First-time contributors must accept the CLA before their PR can be
  merged.
- **Send the CLA by email**: read [CLA.md](CLA.md), sign it and email it
  to a maintainer (see [CONTRIBUTORS.md](CONTRIBUTORS.md) for the
  maintainers).
- The maintainer adds your line to [CONTRIBUTORS.md](CONTRIBUTORS.md)
  (`cla: accepted`) in a maintainer-reviewed PR — that entry is the CLA
  record, and it triggers the contributor sync workflow (teams and
  memberships follow the roster).
- A CLA check runs on every PR from contributors whose `cla` is not
  `accepted` in the roster.

## License

By contributing, you agree that your contributions will be licensed under
the [AGPL-3.0](LICENSE) (see [CLA.md](CLA.md) for the full grant,
including the project's relicensing option).
