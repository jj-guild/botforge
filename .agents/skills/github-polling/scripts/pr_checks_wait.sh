#!/usr/bin/env bash
# Poll a GitHub PR's checks until every check is terminal — never a fixed sleep
# (the github-polling skill's rule). Prints one summary line per poll cycle.
#
# The checks are read on the PR's HEAD SHA via the check-runs API — the PR
# rollup briefly lists the PREVIOUS commit's checks after a push (the
# 2026-11-07 race: a green exit while every check on the new head was
# still pending; the ci-monitoring skill: "checks are verified on the head
# commit, completed").
#
# Usage:
#   pr_checks_wait.sh <owner/repo> <pr-number> [interval-s] [max-minutes]
#
# Exit codes: 0 = all checks terminal and green, 1 = failures or non-terminal
# past the cap, 2 = usage/CLI error.
set -euo pipefail

repo="${1:?usage: pr_checks_wait.sh <owner/repo> <pr-number> [interval-s] [max-minutes]}"
pr="${2:?usage: pr_checks_wait.sh <owner/repo> <pr-number> [interval-s] [max-minutes]}"
interval="${3:-15}"
cap_minutes="${4:-30}"

deadline=$(( $(date +%s) + cap_minutes * 60 ))
while :; do
    head="$(gh pr view "$pr" --repo "$repo" --json headRefOid --jq '.headRefOid' 2>/dev/null)" || { echo "gh error" >&2; exit 2; }
    summary="$(gh api "repos/${repo}/commits/${head}/check-runs" --jq 'reduce .check_runs[] as $c (
        {pass: 0, fail: 0, pending: 0, other: 0};
        if $c.status != "completed" then .pending += 1
        elif $c.conclusion == "success" then .pass += 1
        elif ($c.conclusion == "failure" or $c.conclusion == "cancelled" or $c.conclusion == "timed_out") then .fail += 1
        else .other += 1 end
    ) | "\(.pass)/\(.fail)/\(.pending)/\(.other)"' 2>/dev/null)" || { echo "gh error" >&2; exit 2; }
    IFS='/' read -r pass fail pending other <<<"$summary"
    total=$(( pass + fail + pending + other ))
    echo "head ${head:0:7} checks: pass=$pass fail=$fail pending=$pending neutral=$other"
    # a just-pushed head has NO check runs yet (0/0/0/0) — that is
    # pending, never green (the second 2026-11-07 race)
    if [ "$total" -eq 0 ]; then
        pending=1
    fi
    if [ "$pending" -eq 0 ]; then
        [ "$fail" -eq 0 ] && exit 0 || exit 1
    fi
    if [ "$(date +%s)" -ge "$deadline" ]; then
        echo "non-terminal after ${cap_minutes}min — diagnose (queued forever? waiting for a runner?)" >&2
        exit 1
    fi
    sleep "$interval"
done
