# Guides — by audience

Who reads what. Each guide is the entry point for one audience; it
links to the authoritative documents instead of duplicating them.

| Audience | Guide | You want to… |
|---|---|---|
| Mod developer (human or AI) | [mod-developer.md](mod-developer.md) | Build a new mod on the BotForge core |
| Game provider developer | [game-provider.md](game-provider.md) | Integrate a new game and its external data providers |
| Vibe coder (AI agent session) | [vibe-coder.md](vibe-coder.md) | Run a work session: issues → branch → PR → CI |
| Game designer | [game-designer.md](game-designer.md) | Design a feature and get it built without coding |
| Platform developer (maintainer) | [DEVELOPER.md](../DEVELOPER.md) + [CONVENTIONS.md](../CONVENTIONS.md) | Review, challenge, approve |
| Org admin (one-time setup) | [rulesets.md](rulesets.md) | Create and maintain the GitHub rulesets |

## Reading order by goal

- **"I want a new game feature"** → game-designer.md, then the AI agent
  reads mod-developer.md.
- **"I want to add a game"** → game-provider.md (the developer reviews).
- **"I am an AI session starting work"** → vibe-coder.md first, then the
  issue at hand.

Authoritative references for everyone:
[ARCHITECTURE](../ARCHITECTURE.md) · [CONVENTIONS](../CONVENTIONS.md) ·
[VIBEWORKFLOW](../VIBEWORKFLOW.md) · [MODS](../MODS/README.md) ·
[DECISIONS](../DECISIONS/README.md) (ADRs) · [ROADMAP](https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/ROADMAP.md)
- [your-test-env.md](your-test-env.md) — what it takes to run your own
  test environment (Discord bot + server, GitHub secrets, agent does the
  rest) — for every vibe coder getting their personal env.
- [join-the-platform.md](join-the-platform.md) — what a new contributor needs (accounts, connector, runner, CLA)
