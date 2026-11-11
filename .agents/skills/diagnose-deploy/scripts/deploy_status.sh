#!/usr/bin/env bash
# One-shot deploy status for a kingdoms environment — the committed
# replacement for the ad-hoc `gh api`/`gh run list`/`gh run view` sequence
# (the automate-or-learn rule: a session never re-types it).
#
# Prints, for <env>:
#   1. the latest pin commit on the deploy/<env> state branch;
#   2. the latest "Deploy environment" run: id, status, conclusion, title;
#   3. the run's per-job verdicts.
#
# Usage: deploy_status.sh <env> [--json]
# Exit 0 = the run completed successfully; 1 = failed/still running; 2 = CLI error.
set -euo pipefail

env_name="${1:?usage: deploy_status.sh <env> [--json]}"
fmt="${2:-}"
infra_repo="jj-guild/botforge-infra"

pin="$(gh api "repos/${infra_repo}/commits?sha=deploy/${env_name}&per_page=1" \
    --jq '.[0] | .sha[0:7] + " — " + (.commit.message | split("\n")[0])' 2>/dev/null)" || { echo "gh error (pin)" >&2; exit 2; }
echo "pin (deploy/${env_name}): ${pin}"

# the deploy runs live on the deploy/<env> state branch (deploy.yml) —
# filtering without the branch picks up stale broken runs from PR heads
run_json="$(gh run list --repo "${infra_repo}" --branch "deploy/${env_name}" --workflow deploy.yml --limit 1 \
    --json databaseId,status,conclusion,displayTitle \
    --jq '.[0] | (.databaseId|tostring) + " " + .status + " " + (.conclusion // "-") + " " + .displayTitle' 2>/dev/null)" || { echo "gh error (run)" >&2; exit 2; }
read -r run_id run_status run_conclusion _ <<<"$run_json"
echo "deploy run: id=${run_id} status=${run_status} conclusion=${run_conclusion}"

if [ "$fmt" = "--json" ]; then
    gh run view "$run_id" --repo "${infra_repo}" --json jobs --jq '.jobs'
else
    gh run view "$run_id" --repo "${infra_repo}" --json jobs \
        --jq '.jobs[] | "  " + .name + ": " + (.conclusion // .status)'
fi

[ "$run_status" = "completed" ] && [ "$run_conclusion" = "success" ] && exit 0 || exit 1
