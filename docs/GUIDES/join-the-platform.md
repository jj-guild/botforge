# Guide — Join the platform (potential contributor)

You want to contribute to BotForge — as a game designer, a mod
developer, or any role. This page explains **how the platform works
for you** and what you need. No development experience is required to
run vibe-coding sessions; everything technical is done by your AI
agent.

## What you need

1. **A GitHub account** — your identity on the platform. Everything is
   public and open: [botforge](https://github.com/jj-guild/botforge)
   (docs), [botforge-services](https://github.com/jj-guild/botforge-services)
   (code), [botforge-infra](https://github.com/jj-guild/botforge-infra)
   (infrastructure).
2. **A Mistral account with the GitHub connector** — the AI agent
   (Mistral Vibe Code) acts **through your GitHub account**: the
   connector picks up your GitHub permissions, which come from your
   roles in the [CONTRIBUTORS.md](../../CONTRIBUTORS.md) matrix
   (roster teams → repo grants → what your agent may do). You never
   give the agent more rights than you have.
3. **A machine for your personal test environment (optional but
   recommended)** — a hosting, a Raspberry Pi, or a self-hosted GitHub
   Actions runner you own. It runs **your own test environment**
   (bot + MongoDB + Redis, one `docker compose up`) so you can test
   your mods on your own test Discord server before anyone else sees
   them. See [your-test-env.md](your-test-env.md).
4. **A signed CLA** — download [CLA.md](../../CLA.md) (or
   [CLA.pdf](../../CLA.pdf)), sign it, and **email it to a maintainer**
   (Merlin by default, address in the CLA). The maintainer's roster PR
   records your acceptance (`cla: accepted`) — that entry is what
   unlocks your PRs (the `cla` check reads the roster).

## How it works once you are in

- **The roster is the truth**: your entry in
  [CONTRIBUTORS.md](../../CONTRIBUTORS.md) declares your alias, teams,
  roles, what you own and what your agent may do on your behalf. A
  maintainer adds you through a reviewed PR — you never edit it
  yourself (it is maintainer-owned).
- **Your agent does the technical work**: issues, branches, PRs, CI,
  test deployments, releases. You review its asks (it asks through
  clear UI choices with context), you validate the game behavior on
  Discord, you decide the game design.
- **Reviews are automated by ownership**: GitHub CODEOWNERS requires
  a review exactly where you own code (your mod) or where the
  maintainers own it (core/platform). PRs automerge once the required
  reviews land; nobody clicks Merge.
- **Everything is documented**: the [INDEX](../INDEX.md) routes every
  question to its page. Your agent reads the same docs — the platform
  is designed so that a session with zero memory can pick up any work
  from the repo alone.

## First steps

1. Contact a maintainer (Merlin): who you are, what you want to do
   (game designer, mod developer, ops...).
2. Sign and email the CLA.
3. The maintainer's roster PR adds you (alias, teams, roles, agent
   scope) — GitHub follows the doc automatically.
4. Open your first Mistral Vibe session on the botforge repo; the
   agent reads the docs, greets you by your alias, and asks what you
   want to build.
5. Optionally, set up [your test environment](your-test-env.md) so
   your agent can deploy and validate your work on your own Discord
   server.

## See also

- [CONTRIBUTORS.md](../../CONTRIBUTORS.md) — the roster and authority
  matrix
- [VIBEWORKFLOW.md](../VIBEWORKFLOW.md) — the operating model
- [your-test-env.md](your-test-env.md) — your personal test
  environment checklist
