---
name: human-interaction
description: How an agent session communicates with its human — confirmations via UI selects (never bare questions), a always-visible live plan (todo list), context links before any ask, alias-based addressing. Applies to every human, every role, every repo. Use whenever the session is about to ask, report or plan.
---

# Human interaction

The human is non-technical by assumption (game designers) or an
experienced developer — either way they **review, decide and validate**;
the session does everything else. These rules make that review loop
cheap and predictable. They apply to **every human the session works
with, whatever their roster role** (vibe, mod, dev, ops, platform,
maintainer) — adapt the *content* to the role, never the *form*.

## 1. Ask through a UI select, never a bare question

When the session needs a decision or authorization only a human can
give (merge confirmation, direct-to-main push, force-push request,
scope extension, production approval, any maintainer confirmation
required by the authority matrix):

- **Always present the ask as a UI select** (2–4 concrete options plus
  free text), never a bare prose question and never an implied
  "continue?".
- No timeout: the select waits as long as the human needs.
- Ask as soon as the need is identified — do not batch asks at the end
  of a long run.
- One ask per select; a second independent decision gets its own
  select.

## 2. Before asking, give the context to decide

Never make the human hunt for the information that would let them
answer:

- **GitHub links, always** — every question, ask, validation request or
  select, without exception, carries descriptive Markdown links to the
  involved artifacts (issue, PR, commit, run, file). A select without
  its links is a malformed ask: redo it. This rule is non-negotiable
  and applies even to quick or mid-run asks;
- what the change **will impact** (files, repos, environments) and
  what it **will fix** (the concrete failure or gap), in one or two
  lines each;
- the risks or alternatives when they matter.

## 3. Keep a live, visible plan

- At the start of any multi-step work, publish the plan as a **todo
  list the human can see and fold/unfold**.
- **Update it as the work progresses** — mark items done the moment
  they are done, add items as they appear, never let it go stale
  mid-run. The human must be able to look at it at any time and know
  exactly where the session is.
- After completion or at each meaningful milestone, the plan doubles
  as the progress report.

## 4. Address and report by alias

- Address the human by their **roster alias** (CONTRIBUTORS.md),
  capitalized as a proper name (Merlin, Drasah) — never all-caps; the
  GitHub login is resolved only for API calls.
- Reports use the alias too, and name the exact artifacts (PR, issue,
  commit, run URL) the human may need to look at.

## 5. Honesty and cadence

- Report failures and blockers **immediately**, with the root cause
  found in the logs — never hide a mistake or a blocked state behind
  progress prose.
- Acknowledge the human's messages as they arrive, even mid-run; a
  long-running task gets a short "here is what I'm doing" note.
- When the session is certain and inside its scope, it acts; when a
  rule requires a human (the authority matrix, the git history
  rules), it asks — with a select, with context.

## 6. Speak the human's functional language

Adapt the discourse to the roster profile (AGENTS.md PRIORITY 0): plain,
clear language, in the human's chat language (French or English). For a
non-dev profile (game designer, mod owner): talk **game, lore and
Discord** — never infrastructure words (no "database", no "service
talking to another service", no "API"). When a technical topic comes up,
the session translates it into ONE simple sentence and handles it under
the hood — the human never debugs platform internals. GitHub output
(issues, PRs, comments, commits) stays English (CONVENTIONS.md,
*Working language*).

## 7. Temporary vs delegate — the human is never blocked

Always explain a problem in these simple terms:

- **A red check, a weird error message, a button that did not answer
  once** → temporary. The session reads the report, says in one sentence
  what it is, fixes it, retests. Nothing for the human to do.
- **A topic inside the platform's internals** (how the bot keeps its
  data, how the bot's pieces exchange, access security) → NOT the
  human's to fix. The session opens a clear issue to the platform
  maintainer (per the roster) with the symptom in functional language —
  **and proposes a workaround to keep moving anyway**: a mock, a
  temporary fixed value, a "coming soon" button, a clearly marked mock
  in code. Rule: **never blocked** — workaround in place, issue opened,
  work continues; the workaround is removed when the real mechanism
  lands.
- **A doubt on lore / game rules** → the human is the reference. Discuss,
  DECISIONS.md arbitrates, and a "À DÉFINIR" is never invented.

## 8. Anamnesis first when picking up legacy work

When a session picks up a migration or a port from legacy branches, its
FIRST move is a UI-select question: *"What worked on your old branches
that you miss today?"* Let the human answer freely, then offer 2–4
checkbox options built from what they cited plus what is already known.
The answers become the session's todo list. No coding before the answer.

## See also

- [CONTRIBUTORS.md](../../../CONTRIBUTORS.md) — roster, authority
  matrix, git history rules (what needs an explicit ask)
- [VIBEWORKFLOW.md](../../../docs/VIBEWORKFLOW.md) — the operating
  model (roles, approvals, session loop)
- [CONVENTIONS.md](../../../docs/CONVENTIONS.md) — repo-wide conventions
