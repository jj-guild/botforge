# Your own test environment — the checklist for vibe coders

This page explains **what it takes to run your own test environment** on
the platform — in plain words, for game designers and vibe coders who
never touch a terminal. Your agent does all of it; you only provide the
things only a human can provide (accounts, tokens, clicks).

## What an environment is

An environment ("env") is **your own copy of the whole bot**, running on
the platform's server, connected to **your own Discord test server**.
Deploying your work to your env lets you play with the bot in Discord
exactly like a player would, without touching anyone else's bot.

Each env is made of these pieces — the table is the whole story:

| Piece | What it is | Who provides it |
| --- | --- | --- |
| **A Discord bot application** | A bot account on the Discord developer portal (its token is the bot's password) | You: create it on the [Discord developer portal](https://discord.com/developers/applications), copy the token — never paste it anywhere except the secret your agent points you to |
| **A Discord test server** | A private Discord server where the bot runs; you invite the bot there and you are its admin | You: create it, invite your bot with the invite link your agent gives you |
| **An env directory on botforge-infra** | `envs/<name>/docker-compose.yml` — the recipe of your env (bot + database + cache), data, not code | Your agent: copies the test template, names the env after your alias (e.g. `envs/drasah/`) |
| **A GitHub environment** | The GitHub-side settings page named like your env (`Settings → Environments`) — holds the **secrets** (Discord token, admin IDs) and gates who may deploy to it | Your agent prepares it; **you** paste the secrets — the only human step |
| **A state branch `deploy/<name>`** | The Git branch that records *which version of the bot* your env runs | Your agent creates it, protected by a ruleset |
| **A ruleset on botforge-infra** | The GitHub rule that protects your state branch (the same one `deploy/test` uses — templated per env) | Your agent drafts the change; a maintainer approves it — branch protection is platform-owned |
| **A runner** | The small program on the server that executes your env's deployments. Test envs may share one server ("hosting") with separate runners — costs are mutualized, each env stays isolated (separate compose projects, separate networks) | Platform team: installs and labels it (`env-<name>`); nothing for you |

## What you actually do (the whole human part)

1. **Create a Discord application** for your bot on the developer portal,
   copy its token.
2. **Create a Discord test server**, and tell your agent its name.
3. **Paste the secrets** in the GitHub environment page your agent links
   you to (Discord token, your Discord user ID as bot admin).
4. **Invite your bot** to your test server with the link your agent
   gives you.
5. **Test**: say "déploie sur mon env" in your session — the agent
   deploys your current PR there, and you play in Discord.

Everything else — env directory, branches, rulesets, deployments,
rollbacks — is your agent's job, gated by the authority matrix
([CONTRIBUTORS.md](../../CONTRIBUTORS.md)).

## Rules that keep it safe

- Your env is **yours**: you deploy anything you want there (any of your
  open PRs), any time. It never affects `test`, `prod` or anyone else's
  env.
- **Prod is never a personal env** — production runs released versions
  only, deployed by ops.
- One env per contributor, named after your roster alias
  (lowercase, e.g. `drasah`), matching your branch prefix and your
  GitHub environment.
- If your bot misbehaves: `/restart drasah` from your session fixes most
  things; `/logs drasah` shows your agent why. No human ever needs a
  terminal.

## See also

- [ENVIRONMENTS.md](https://github.com/jj-guild/botforge-infra/blob/main/docs/ENVIRONMENTS.md) — the
  environment matrix and configuration variables (infra repo)
- [PROCESS.md](../PROCESS.md) — the deployment processes end to end
- [CONTRIBUTORS.md](../../CONTRIBUTORS.md) — the roster and authority matrix
