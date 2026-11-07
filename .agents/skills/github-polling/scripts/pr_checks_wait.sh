#!/usr/bin/env bash
# Poll a GitHub PR's checks until every check is terminal — never a fixed sleep
# (the github-polling skill's rule). Prints one summary line per poll cycle.
#
# Usage:
#   pr_checks_wait.sh <owner/repo> <pr-number> [interval-s] [max-minutes]
#
# Exit codes: 0 = all checks terminal (see the pass/fail counts in the last
# line), 1 = non-terminal past the cap, 2 = usage/CLI error.
set -euo pipefail

repo="${1:?usage: pr_checks_wait.sh <owner/repo> <pr-number> [interval-s] [max-minutes]}"
pr="${2:?usage: pr_checks_wait.sh <owner/repo> <pr-number> [interval-s] [max-minutes]}"
interval="${3:-15}"
cap_minutes="${4:-30}"

deadline=$(( $(date +%s) + cap_minutes * 60 ))
while :; do
    summary="$(gh pr view "$pr" --repo "$repo" --json statusCheckRollup \
        --jq 'reduce .statusCheckRollup[] as $c (
            {pass: 0, fail: 0, pending: 0, other: 0};
            if $c.status != "COMPLETED" then .pending += 1
            elif $c.conclusion == "SUCCESS" then .pass += 1
            elif ($c.conclusion == "FAILURE" or $c.conclusion == "CANCELLED" or $c.conclusion == "TIMED_OUT") then .fail += 1
            else .other += 1 end
        ) | "\(.pass)/\(.fail)/\(.pending)/\(.other)"' 2>/dev/null)" || { echo "gh error" >&2; exit 2; }
    IFS='/' read -r pass fail pending other <<<"$summary"
    echo "checks: pass=$pass fail=$fail pending=$pending skipped=$other"
    if [ "$pending" -eq 0 ]; then
        [ "$fail" -eq 0 ] && exit 0 || exit 1
    fi
    if [ "$(date +%s)" -ge "$deadline" ]; then
        echo "non-terminal after ${cap_minutes}min — diagnose (queued forever? waiting for a runner?)" >&2
        exit 1
    fi
    sleep "$interval"
done
