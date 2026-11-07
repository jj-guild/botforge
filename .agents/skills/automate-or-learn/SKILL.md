---
name: automate-or-learn
description: Decide where a recurring operation belongs (Makefile target, script, workflow, or skill) and when a session must persist a command it improvised. Use when a session runs a command twice, learns a new procedure or pitfall, or wonders how to memorize knowledge for future sessions.
---

# Automate or learn

Every recurring operation of the platform is a committed artifact — a
Makefile target, a script, or a GitHub Actions workflow. Nothing runs as a
one-off shell command, whether typed by a human (never — see
[docs/CONVENTIONS.md](../../../docs/CONVENTIONS.md), *Humans never code*)
or by an agent session. This skill decides **where each piece of automation
belongs** and **when a session must persist a command it improvised**.

## Where each automation belongs

**Check BEFORE typing, not after.** Before composing any multi-step shell
chain (a `gh`/`git`/`jq` pipeline, a poll loop, a log extraction), the
session first looks for the committed script that already does it and RUNS
it. Typing a command the platform already carries is a bug, whatever the
deadline. The known entry points:

- PR-checks waiting → `github-polling/scripts/pr_checks_wait.sh`
- Deploy status (pin + run + jobs) → `diagnose-deploy/scripts/deploy_status.sh`
- Deploy watching end-to-end → `kingdoms-services` `.github/workflows/scripts/watch_deploy.sh`


| Kind of operation | Artifact | Where |
| ----------------- | -------- | ----- |
| Anything a session runs more than once | Makefile target | `Makefile` of the repo it belongs to (`make lint`, `make session-check`, `make watch-deploy`, `make release`) |
| Reusable implementation, multi-step logic, fail-closed checks | Python or shell script | `scripts/` (or `.github/workflows/scripts/`) of the repo it belongs to (`botforge`: `.github/workflows/scripts/sync_roadmap.py`; `botforge-services`: `scripts/cut_release.sh`, `.github/workflows/scripts/watch_deploy.sh`) |
| Must run with no session open, or needs permissions the session lacks (releases, deploy pins, scheduled sync), or cannot run in the sandbox | GitHub Actions workflow | `.github/workflows/` of the repo it belongs to |
| How to use the above, plus pitfalls learned | Skill | `.agents/skills/<name>/SKILL.md` in the `botforge` repo (Agent Skills open standard) |

Rules of thumb:

- The Makefile is the **menu**: a new session discovers what exists by
  reading it. A script without its Makefile target (or workflow) is
  half-committed knowledge. A skill may also carry its own scripts
  (`.agents/skills/<name>/scripts/`) when the procedure is
  skill-specific — the `SKILL.md` documents their usage, and the
  scripts are committed, tested once, and never re-typed by hand.
- Scripts are **fail-closed**: explicit error, non-zero exit, no partial
  writes — same standard as the sync scripts (see
  [Generated artifacts sync](../../../docs/VIBEWORKFLOW.md)).
- Shell scripts pass `bash -n` (and shellcheck when available) before
  pushing; Python scripts run under the repo's checks.
- Anything the sandbox cannot run (compose boots, deploy runs, GitHub
  permissions) is exercised by a CI workflow — never left unverified
  (*Checks must pass everywhere* in
  [docs/CONVENTIONS.md](../../../docs/CONVENTIONS.md)).
- A required status check never uses a `paths:` filter (infra developer
  guide, workflow pitfalls).

## Learn it or drop it (the session rule)

Whenever a session types a shell command or writes a helper script for its
own convenience, it must ask: **will this be useful again?**

- **Yes, or plausibly yes → learn it.** Commit it to the repo it belongs
  to: wrap the command in a Makefile target or a script, bake in what the
  session learned (pre-flight checks, pitfalls, failure modes), and
  document it in a skill if usage is non-obvious. Sessions have no
  conversation memory: **an uncommitted command is knowledge lost**.
- **Genuinely no → keep it ephemeral**, and never present it to a human
  (humans never run commands at all).

## When you learn something new — propose, then persist

When a session learns to do something new (a procedure, a workaround, a
pitfall, a repeated command), it does not silently improvise: it
**proposes to the human** to memorize it for future sessions, stating the
destination:

- a **Makefile target or script** in the repo it belongs to, when the
  knowledge is executable;
- a **GitHub Actions workflow**, when it must run without a session or
  needs permissions the session lacks;
- a **skill page** (`.agents/skills/<name>/SKILL.md`), when the knowledge
  is procedural know-how, pitfalls, or usage rules;
- a **rule in `docs/CONVENTIONS.md` / `docs/VIBEWORKFLOW.md`**, when the
  knowledge is a binding convention for every future session.

On the human's approval (or by default at the end of a session, with the
change committed to a PR), the knowledge is committed to the matching
artifact and wired into the docs (AGENTS.md / DEVELOPER.md / skills index)
so future sessions discover it.

**Documentation enrichment is proactive (developer-mandated).** For
knowledge (rules, pitfalls, patterns — as opposed to executable
commands), the session does not wait to be asked: updating `AGENTS.md`,
the vibe-coding docs (`docs/CONVENTIONS.md`, `docs/VIBEWORKFLOW.md`,
`docs/DEVELOPER.md`…) and the skill pages is part of the change that
taught it. Pick one home for the rule (skill for know-how, convention
for binding rules, AGENTS.md one-liner + link for repo discovery) and
commit it with the change — see *Documentation is part of the
change* in [docs/CONVENTIONS.md](../../../docs/CONVENTIONS.md).

Examples of learned commands in this platform:
`make session-check` (the end-of-session checklist became a script),
`make release` and `make watch-deploy` (release cutting and deploy
monitoring became scripts with pre-flight checks).

## Procedure

1. Notice you are about to repeat a command, or that a helper script made
   your session easier.
2. Decide the artifact kind with the table above (Makefile target wrapping
   a script; workflow when no session can run it).
3. Commit it to the repo it belongs to, with the pitfalls you hit baked in
   as pre-flight checks or comments in the skill page.
4. Wire it: mention the new target/workflow in the repo's `AGENTS.md` or
   `docs/DEVELOPER.md` if future sessions must discover it, and keep the
   `botforge` docs in sync (a code change without its doc update is
   incomplete).
5. Do not ask a human to run it — ever.
