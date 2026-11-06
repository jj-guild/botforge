---
name: troubleshooting
description: The platform's failure memory — every incident already met and fixed (crashes, stuck deploys, flaky checks, architecture violations), per scope. Use when a session hits a problem: check here before diagnosing from scratch, and add the entry when the fix lands.
---

# Troubleshooting — the failure memory

Sessions have no memory; this skill is the platform's. Every incident
already met and fixed lives here, **per scope**, one dated entry per
incident, newest first. Before diagnosing a problem from scratch, check
whether the wall has already been met — and when a session fixes a
problem, the same PR adds the entry (PRIORITY 0 rule 7, kingdoms
CONVENTIONS.md *Troubleshooting is part of the fix*).

**Entry shape (all four, always):**

```
### <date> — <one-line symptom>
- Symptom: what it looked like (logs, behavior, error)
- Root cause: the real mechanism, found in the evidence
- Fix: what changed (commit/PR reference)
- Guard: the regression test that fails without the fix, by name
```

A fix without its test and its entry is incomplete; an entry without a
guard test is a story, not a memory.

## Scope: platform code (kingdoms-services)

No entry yet — the first fixed incident lands here.

## Scope: deploy & infra (kingdoms-infra, VPS, runners)

No entry yet — the first fixed incident lands here.
(The concurrency-zombie trap — a run waiting for an environment approval
holding the deploy group forever — is documented with its diagnosis
procedure in the
[diagnose-deploy](../diagnose-deploy/SKILL.md) skill.)

## Scope: docs & CI (kingdoms, workflows, checks)

No entry yet — the first fixed incident lands here.

## Rules

- **One home**: the entry lives in this skill; other docs link to it,
  never copy it (CONVENTIONS.md, *one home per rule*).
- **Root cause from evidence**: an entry states the mechanism found in
  the logs, not a guess (CONVENTIONS.md, *Diagnose before blaming the
  infrastructure*).
- **Scope first**: pick the section matching where the failure
  manifested; cross-scope incidents get one entry in the primary scope
  and links from the others.
- **Pruning is healthy**: an entry whose guard test was removed, or
  describing a mechanism that no longer exists, is deleted in the same
  PR that obsolete it — this is a memory, not a graveyard.
