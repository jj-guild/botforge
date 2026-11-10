# The game designer's guide — describing an idea, following its delivery

> **Français :[le guide du game designer est ici](GAME-DESIGN.fr.md).**
> The bot speaks English and French (`config/locales/`); this guide is
> available in both too. This page is the English version.

This page is the **game designer's** entry point: it explains how to turn
an idea into a feature visible in Discord, without ever touching a
technical tool. All the technical work is done by the agent (agent
sessions) or by CI — see [VIBEWORKFLOW.md](VIBEWORKFLOW.md) for the full
operating model and [PROCESS.md](PROCESS.md) for the per-role detail.

## What you actually do

1. **You describe the idea in an agent session** (Discord or session).
   No format needed to start — the agent asks questions and turns the
   discussion into a structured **GitHub issue** (objective, context,
   acceptance criteria) that you re-read and validate.
2. **The agent implements and opens a PR.** You don't follow the PR
   itself: when the agent announces the test deployment is ready, **you
   test in Discord** on the test server.
3. **You validate the behavior** by playing. This is your only
   functional quality criterion: does the bot do what you had in mind?
4. **The developer (or ops) reviews and merges the PR.** You don't need
   merge rights — that is deliberate.
5. For the feature to reach real players, it must be part of a
   **published version** (`vX.Y.Z`) — just ask the agent "shall we
   publish a version?" and follow along.

## How to describe an idea well

A well-described idea saves a round-trip. The elements that help the
agent (in any order, in plain language):

- **The expected outcome as a player sees it**: "when a player types
  `/kingdom`, they see their castle and resources".
- **The game rules**: numbers, durations, limits, what is allowed or
  forbidden. If a rule feels fuzzy to you, say so — the agent will help
  make it precise and automatable.
- **An example scenario**: "player A attacks, player B defends, here is
  what should happen".
- **What must not change**: the existing interactions to preserve.

The agent systematically **challenges** the design: it may propose a
simpler variant to automate, raise a contradiction between two rules,
or split a big idea into steps deliverable one by one. That is normal
and intended — just answer in plain language.

## Where to test: the test server

- Features under development run on the **test** Discord server;
  production (real players) only receives published versions.
- When a test deployment is in progress, the PR carries a **tracking
  comment** showing its progress: 🟡 building → 🔵 deploying →
  🟢 deployed (or ❌ failed, ⛔ denied). If you see ❌, just report it to the
  agent — diagnosing is its job, not yours.

## Reading the bot's /status

The `/status` command is your dashboard in Discord. In plain language:

- **Version** — the running build: a link to the test PR, the commit or
  the release that produced the bot you are looking at.
- **Infra** — the pipeline that deployed this build (link to the run):
  proof that what you test is the latest delivery.
- **Admins** — the bot operators and server admins: who to turn to when
  something does not work.
- **Games / Mods** — the configured games and active modules.

## When something is stuck

- **A command does not respond**: check `/status` (is the bot
  up to date?), then report to an admin listed in the report.
- **A deployment fails** (❌ on the PR): the agent diagnoses with the
  dedicated runbook — report it, nothing to do on your side.
- **An idea comes back to you**: just ask the agent to open an issue so
  it is not lost; issues are the project's logbook.

## What you will never do

- Write or merge code, run commands, open a terminal.
- Handle secrets, environments or GitHub permissions.
- Approve a production deployment (that is ops' role).

If an agent session offers you a command to paste in a terminal, refuse:
it is a bug in the session — report it.
