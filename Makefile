# BotForge (documentation repo) — session automation.
#
# The targets mirror the session checklist of docs/CONVENTIONS.md; the agent
# runs `make session-check` before opening any PR and at the end of a session.

BOTFORGE_SERVICES ?= ../botforge-services

.PHONY: help session-check sync-artifacts validate contributors-check contributors-sync roadmap-next

# List the available targets (human entry point).
help:
	@echo "BotForge docs repo — available targets:"
	@echo "  make help                        — show this help"
	@echo "  make session-check               — full validation (docs + roadmap + dependencies)"
	@echo "  make roadmap-next                — print the current lot's ordered work table (read-only)"
	@echo "  make validate                    — docs validation only"
	@echo "  make sync-artifacts              — regenerate generated/ROADMAP.md and generated/DEPENDENCIES.md"
	@echo "  make contributors-check          — roster dry-run (report org drift, no mutation)"
	@echo "  make contributors-sync           — reconcile the org with CONTRIBUTORS.md (mutates)"
	@echo "  BOTFORGE_SERVICES=<path>          — where the botforge-services clone lives (default: ../botforge-services)"

# Mechanical session checklist: docs validation, roadmap drift,
# dependency-graph drift. Fails closed with the exact artefacts to fix.
session-check:
	python3 scripts/session_check.py --source $(BOTFORGE_SERVICES)/src/botforge --config $(BOTFORGE_SERVICES)/config --scripts-dir .github/workflows/scripts

# Current lot's work order, straight from the issues (read-only; reuses the
# workflow scripts' parsers). This is what the roadmap-unroll skill runs.
roadmap-next:
	python3 scripts/roadmap_next.py

# Regenerate the synced artefacts (generated/ROADMAP.md, generated/DEPENDENCIES.md) —
# local dry-run only: the sync-generated workflow owns the real
# regeneration (post-merge, daily 06:00 UTC, on demand). Never commit
# the output to a PR branch.
sync-artifacts:
	python3 .github/workflows/scripts/sync_roadmap.py
	python3 .github/workflows/scripts/sync_dependencies.py

# Roster sync: the org follows CONTRIBUTORS.md (source of truth).
# `contributors-check` reports without mutating (what the CI runs on roster PRs);
# `contributors-sync` adds/removes memberships, teams and repo grants to match the doc.
contributors-check:
	python3 .github/workflows/scripts/sync_contributors.py --check

contributors-sync:
	python3 .github/workflows/scripts/sync_contributors.py

# Restack the open PRs of a repository on top of each other (stacking

validate:
	python3 .github/workflows/scripts/validate_docs.py --check --source $(BOTFORGE_SERVICES)/src/botforge --config $(BOTFORGE_SERVICES)/config
