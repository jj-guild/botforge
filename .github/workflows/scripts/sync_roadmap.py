#!/usr/bin/env python3
"""Synchronize ROADMAP.md with GitHub issue states.

Queries the GitHub REST API for the three Kingdoms repositories, maps issue
states to roadmap statuses and rewrites ROADMAP.md in place: the "Next up"
section, the milestone table (live titles and counts), "Current Phase" and
"Out of Scope". The change log is dropped on purpose: the file shows the
current state and the next steps — the history lives in the git log of the
sync branch.

Status mapping (.agents/skills/update-roadmap/SKILL.md):
- closed as completed   -> done
- closed as not planned  -> dropped (row moved to "Out of Scope")
- open with a linked PR   -> in-review
- open, current status `in-progress` or `blocked` -> unchanged (manual judgment)
- open, otherwise        -> todo

The sibling repositories are public; when one is unreadable (rate limit,
missing token) the script warns and keeps its existing rows, like
scripts/validate_docs.py.

Exit codes: 0 success (or --check without drift), 1 drift detected in --check
mode, 2 fatal error.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

API_BASE = "https://api.github.com"
OWNER = "merlin-pinpin-org"
REPOS = ("kingdoms", "kingdoms-services", "kingdoms-infra")
PER_PAGE = 100
MANUAL_STATUSES = ("in-progress", "blocked", "backlog")
STATUSES = ("todo", "in-progress", "in-review", "done", "blocked", "dropped")

ISSUE_URL = f"https://github.com/{OWNER}/" + "{repo}/issues/{num}"
ROW_PLAIN_RE = re.compile(
    r"^\|\s*(?P<track>[^|]+?)\s*\|\s*(?P<repo>[\w.-]+)#(?P<num>\d+)\s*\|"
    r"\s*(?P<status>[a-z-]+)\s*\|$",
    re.MULTILINE,
)
BULLET_PLAIN_RE = re.compile(
    r"^(?P<prefix>\s*-\s+.*?dropped, see\s+)"
    r"(?P<repo>[\w.-]+)#(?P<num>\d+)"
    r"(?P<suffix>.*)$",
    re.MULTILINE,
)
LINKED_ISSUE_RE = re.compile(
    r"\[(?P<repo>[\w.-]+)#(?P<num>\d+)\]"
    r"\(https://github\.com/[\w.-]+/[\w.-]+/issues/\d+\)"
)
PLAIN_ISSUE_RE = re.compile(r"(?P<repo>[\w.-]+)#(?P<num>\d+)")
ROW_RE = re.compile(
    r"^\|\s*(?P<track>[^|]+?)\s*\|\s*"
    r"(?P<issue>\[[\w.-]+#\d+\]\(https://github\.com/[\w.-]+/[\w.-]+/issues/\d+\)"
    r"|[\w.-]+#\d+)"
    r"\s*\|\s*(?P<status>[a-z-]+)\s*\|$"
)


def issue_ref(repo: str, num: int) -> str:
    """Render an issue reference as a Markdown link."""
    return f"[{repo}#{num}]({ISSUE_URL.format(repo=repo, num=num)})"


def parse_issue_ref(reference: str) -> tuple[str, int]:
    """Extract (repo, num) from either a linked or a plain issue reference."""
    match = LINKED_ISSUE_RE.fullmatch(reference) or PLAIN_ISSUE_RE.fullmatch(reference)
    if not match:
        raise ValueError(f"unparseable issue reference: {reference!r}")
    return match["repo"], int(match["num"])
PHASE_HEADING_RE = re.compile(r"^### Phase (?P<num>\d+) —")
CURRENT_PHASE_RE = re.compile(r"^Phase (?P<num>\d+)\b")
MILESTONE_ROW_RE = re.compile(
    r"^\| \[(?P<label>[^\]]*)\]\((?P<url>https://github\.com/[\w.-]+/"
    r"(?P<repo>[\w.-]+)/milestone/(?P<num>\d+))\) \|(?P<rest>.*)$"
)
CHANGE_LOG_RE = re.compile(r"^## Change Log\s*$", re.IGNORECASE)
NEXT_UP_RE = re.compile(r"^## Next up\s*$")
MILESTONES_HEADING_RE = re.compile(r"^## Milestones\s*$")
PRIO_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
CLOSING_REF_RE = re.compile(
    r"\b(?:close[ds]?|closing|fix(?:e[ds]?)?|fixing|resolv(?:e[ds]?)?|resolving)"
    r"[\s:;,.'\"()\[\]]*(?:(?P<owner>[\w.-]+)/(?P<ref_repo>[\w.-]+))?"
    r"#(?P<num>\d+)",
    re.IGNORECASE,
)
BULLET_REF_RE = re.compile(
    r"\[(?P<repo>[\w.-]+)#(?P<num>\d+)\]\(https://github\.com/[\w.-]+/[\w.-]+/issues/\d+\)"
    r"|\b(?P<plain_repo>[\w.-]+)#(?P<plain_num>\d+)\b"
)


@dataclass
class Issue:
    state: str
    state_reason: str | None
    title: str
    milestone: int | None = None
    milestone_title: str | None = None
    priority: str | None = None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def api_get(path: str, token: str | None) -> list[dict]:
    """Return all pages of a GET request to the GitHub REST API.

    On an authentication failure (401/403) or a missing repo (404) the request
    is retried unauthenticated: all three Kingdoms repositories are public.
    Raises the last error when both attempts fail.
    """
    last_error: Exception | None = None
    for attempt_token in (token, None):
        items: list[dict] = []
        page = 1
        separator = "&" if "?" in path else "?"
        try:
            while True:
                url = f"{API_BASE}{path}{separator}per_page={PER_PAGE}&page={page}"
                request = urllib.request.Request(
                    url,
                    headers={
                        "Accept": "application/vnd.github+json",
                        "User-Agent": "kingdoms-roadmap-sync",
                    },
                )
                if attempt_token:
                    request.add_header("Authorization", f"Bearer {attempt_token}")
                with urllib.request.urlopen(request, timeout=30) as response:
                    data = json.load(response)
                items.extend(data)
                if not isinstance(data, list) or len(data) < PER_PAGE:
                    return items
                page += 1
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in (401, 403, 404) or attempt_token is None:
                raise
        except urllib.error.URLError as error:
            last_error = error
            raise
    raise last_error if last_error else RuntimeError("unreachable")


def fetch_repo_state(
    repo: str, token: str | None
) -> tuple[dict[int, Issue], set[int]] | None:
    """Return ({number: Issue}, {numbers with an open linked PR}) or None."""
    try:
        raw_issues = api_get(f"/repos/{OWNER}/{repo}/issues?state=all", token)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        warn(f"cannot read {OWNER}/{repo}: {error}; keeping its rows")
        return None

    issues = {
        item["number"]: Issue(
            state=item["state"],
            state_reason=item.get("state_reason"),
            title=item.get("title") or f"{repo}#{item['number']}",
            milestone=(item.get("milestone") or {}).get("number"),
            milestone_title=(item.get("milestone") or {}).get("title"),
            priority=next(
                (
                    m.group(1)
                    for label in item.get("labels") or []
                    if (m := re.match(r"^priority/(P[0-3])$", label.get("name", "")))
                ),
                None,
            ),
        )
        for item in raw_issues
        if "pull_request" not in item
    }
    if not issues:
        warn(
            f"{OWNER}/{repo} returned no issues; the GitHub API may have "
            f"rejected the token silently (check the issues:read permission)"
        )

    linked: set[int] = set()
    try:
        pulls = api_get(f"/repos/{OWNER}/{repo}/pulls?state=open", token)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        warn(f"cannot list open PRs of {OWNER}/{repo}: {error}; no PR detection")
        pulls = []
    for pull in pulls:
        for match in CLOSING_REF_RE.finditer(pull.get("body") or ""):
            ref_repo = match["ref_repo"]
            if ref_repo and ref_repo != repo:
                continue
            linked.add(int(match["num"]))
    return issues, linked


def fetch_milestones(token: str | None) -> dict[tuple[str, int], dict] | None:
    """Return {(repo, number): milestone} across the three repos, or None."""
    milestones: dict[tuple[str, int], dict] = {}
    for repo in REPOS:
        try:
            raw = api_get(f"/repos/{OWNER}/{repo}/milestones?state=all", token)
        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            warn(
                f"cannot read milestones of {OWNER}/{repo}: {error}; "
                "keeping the milestone titles already in the file"
            )
            return None
        for item in raw:
            milestones[(repo, item["number"])] = item
    return milestones


def compute_status(
    issue: Issue, has_pr: bool, current: str
) -> str:
    if issue.state == "closed":
        return "dropped" if issue.state_reason == "not_planned" else "done"
    if has_pr:
        return "in-review"
    if current in MANUAL_STATUSES:
        return current
    return "todo"


def migrate_links(text: str) -> tuple[str, int]:
    """Convert plain issue references to Markdown links; idempotent."""
    migrated = 0

    def link_row(match: re.Match) -> str:
        nonlocal migrated
        migrated += 1
        return f"| {match['track']} | {issue_ref(match['repo'], int(match['num']))} | {match['status']} |"

    text = ROW_PLAIN_RE.sub(link_row, text)

    def link_bullet(match: re.Match) -> str:
        nonlocal migrated
        migrated += 1
        return f"{match['prefix']}{issue_ref(match['repo'], int(match['num']))}{match['suffix']}"

    text = BULLET_PLAIN_RE.sub(link_bullet, text)

    header_old = (
        "> Single source of truth for project progress. Updated via the\n"
        "> [Update roadmap](.agents/skills/update-roadmap/SKILL.md) skill.\n"
    )
    header_new = (
        "> Current state and next steps of the plan, regenerated from the GitHub\n"
        "> issues — the history lives in the git log of the `sync/generated-artifacts`\n"
        "> branch. Single writer: the [Generated artifacts](../.agents/skills/generated-artifacts/SKILL.md) workflow.\n"
    )
    if header_old in text:
        text = text.replace(header_old, header_new)
        migrated += 1
    return text, migrated


def sync_roadmap(
    text: str,
    states: dict[str, tuple[dict[int, Issue], set[int]]],
    milestones: dict[tuple[str, int], dict] | None,
) -> tuple[str, list[str], list[str]]:
    """Return (new text, change summaries, warnings)."""
    lines = text.splitlines()
    warnings: list[str] = []
    changes: list[str] = []
    dropped: list[tuple[str, int, str]] = []
    missing: list[tuple[str, int, str]] = []
    phase_status: dict[int, list[str]] = defaultdict(list)
    referenced: dict[str, set[int]] = defaultdict(set)
    row_status: dict[int, str] = {}
    issue_status: dict[tuple[str, int], str] = {}
    subtasks_last_row = -1

    section: int | str | None = None
    for index, line in enumerate(lines):
        phase_match = PHASE_HEADING_RE.match(line)
        if phase_match:
            section = int(phase_match["num"])
            continue
        if line.startswith("### Sub-tasks"):
            section = "subtasks"
            continue
        if line.startswith("## "):
            section = None
            continue
        if section is None:
            continue
        row = ROW_RE.match(line)
        if not row:
            continue
        if section == "subtasks":
            subtasks_last_row = index
        repo, num = parse_issue_ref(row["issue"])
        current = row["status"]
        if repo not in REPOS:
            warnings.append(f"unknown repository reference '{repo}#{num}'")
            continue
        state = states.get(repo)
        if state is None:
            continue
        issues, linked = state
        issue = issues.get(num)
        if issue is None:
            warnings.append(f"issue {repo}#{num} not found on GitHub; keeping its row")
            continue
        status = compute_status(issue, num in linked, current)
        row_status[index] = status
        issue_status[(repo, num)] = status
        if status == "dropped":
            dropped.append((repo, num, issue.title))
            if current != "dropped":
                changes.append(f"{issue_ref(repo, num)} {current}->dropped (moved to Out of Scope)")
        elif status != current:
            changes.append(f"{issue_ref(repo, num)} {current}->{status}")
        if isinstance(section, int):
            phase_status[section].append(status)
        referenced[repo].add(num)

    for repo, state in states.items():
        issues, _linked = state
        for num, issue in issues.items():
            if issue.state == "open" and num not in referenced[repo]:
                missing.append((repo, num, issue.title))
                changes.append(
                    f"{issue_ref(repo, num)} added to Sub-tasks (was missing)"
                )

    if not changes:
        return text, changes, warnings

    out: list[str] = []
    in_out_of_scope = False
    out_of_scope_buffer: list[str] = []
    current_phase: int | None = None
    for phase, statuses in sorted(phase_status.items()):
        if any(status != "done" for status in statuses):
            current_phase = phase
            break
    replace_next_phase_line = current_phase is not None or any(row_status.values())

    if milestones:
        current_lots = ", ".join(
            f"[{m['title']}](https://github.com/{OWNER}/{repo}/milestone/{num})"
            f" ({m.get('open_issues', 0)} open)"
            for (repo, num), m in sorted(
                (
                    (key, value)
                    for key, value in milestones.items()
                    if value.get("state") == "open" and value.get("open_issues", 0) > 0
                ),
                key=lambda kv: (REPOS.index(kv[0][0]), kv[0][1]),
            )
        )
    else:
        current_lots = ""

    open_rows = []
    for repo, nums in referenced.items():
        state = states.get(repo)
        if state is None:
            continue
        issues, _linked = state
        for num in nums:
            status = issue_status.get((repo, num))
            if status not in ("todo", "in-progress", "in-review", "blocked"):
                continue
            issue = issues.get(num)
            open_rows.append(
                (
                    PRIO_RANK.get(issue.priority, 9) if issue else 9,
                    issue.milestone if issue and issue.milestone is not None else 10**9,
                    REPOS.index(repo),
                    num,
                    repo,
                    issue,
                    status,
                )
            )
    open_rows.sort(key=lambda r: r[:4])
    next_up_lines: list[str] = []
    if open_rows:
        next_up_lines = [
            "## Next up",
            "",
            "Open issues of the plan, ordered by priority label then lot. Statuses sync",
            "from GitHub; dependency order, sizes and slack: [DEPENDENCIES.md](DEPENDENCIES.md).",
            "",
            "| Issue | Lot | Priority | Status |",
            "| ----- | --- | -------- | ------ |",
        ]
        for _p, _m, _r, num, repo, issue, status in open_rows:
            lot = issue.milestone_title if issue and issue.milestone_title else "—"
            prio = issue.priority if issue and issue.priority else "—"
            next_up_lines.append(f"| {issue_ref(repo, num)} | {lot} | {prio} | {status} |")
        next_up_lines.append("")

    in_change_log = False
    next_up_done = False
    skip_next_up = False

    for index, line in enumerate(lines):
        if in_change_log:
            if line.startswith("## "):
                in_change_log = False
                out.append(line)
            continue
        if CHANGE_LOG_RE.match(line):
            in_change_log = True
            changes.append("change log dropped (history lives in the git log of the sync branch)")
            continue
        if NEXT_UP_RE.match(line):
            out.extend(next_up_lines)
            next_up_done = True
            skip_next_up = True
            continue
        if skip_next_up:
            if line.startswith("## "):
                skip_next_up = False
            else:
                continue
        if MILESTONES_HEADING_RE.match(line) and not next_up_done:
            out.extend(next_up_lines)
            next_up_done = True
        if line.startswith("## Out of Scope"):
            in_out_of_scope = True
            out.append(line)
            continue
        if index == subtasks_last_row and missing:
            if index in row_status:
                status = row_status[index]
                if status != "dropped":
                    row = ROW_RE.match(line)
                    repo, num = parse_issue_ref(row["issue"])
                    if row["status"] != status:
                        line = f"| {row['track']} | {issue_ref(repo, num)} | {status} |"
            out.append(line)
            for repo, num, _title in missing:
                out.append(f"| {_title} | {issue_ref(repo, num)} | todo |")
            continue
        if index in row_status:
            status = row_status[index]
            if status == "dropped":
                continue
            row = ROW_RE.match(line)
        if in_out_of_scope:
            if line.startswith("## "):
                while out_of_scope_buffer and out_of_scope_buffer[-1] == "":
                    out_of_scope_buffer.pop()
                for repo, num, title in dropped:
                    out_of_scope_buffer.append(
                        f"- {title} — dropped, see {issue_ref(repo, num)} (closed as not planned)"
                    )
                out.extend(out_of_scope_buffer)
                out.append("")
                out_of_scope_buffer = []
                in_out_of_scope = False
                out.append(line)
                continue
            out_of_scope_buffer.append(line)
            ref = BULLET_REF_RE.search(line)
            ref_repo = ref["repo"] if ref and ref["repo"] else (ref["plain_repo"] if ref else None)
            ref_num = ref["num"] if ref and ref["num"] else (ref["plain_num"] if ref else None)
            if ref_repo and ref_num and ref_repo in states:
                issue = states[ref_repo][0].get(int(ref_num))
                if issue is not None and issue.state == "open":
                    warnings.append(
                        f"{ref_repo}#{ref_num} is listed in Out of Scope "
                        f"but is open again; move it back manually"
                    )
            continue
        if index in row_status:
            status = row_status[index]
            if status == "dropped":
                continue
            row = ROW_RE.match(line)
            repo, num = parse_issue_ref(row["issue"])
            if row["status"] != status:
                line = f"| {row['track']} | {issue_ref(repo, num)} | {status} |"
        milestone_row = MILESTONE_ROW_RE.match(line)
        if milestone_row:
            key = (milestone_row["repo"], int(milestone_row["num"]))
            ms = milestones.get(key) if milestones else None
            if ms is not None:
                counts = f"{ms.get('open_issues', 0)} open / {ms.get('closed_issues', 0)} done"
                title = ms.get("title") or milestone_row["label"]
                line = f"| [{title}]({milestone_row['url']}) — {counts} |{milestone_row['rest']}"
            out.append(line)
            continue
        if replace_next_phase_line and CURRENT_PHASE_RE.match(line):
            if current_phase is None:
                out.append("All phases complete")
                changes.append("current phase -> all phases complete")
            else:
                old = int(CURRENT_PHASE_RE.match(line)["num"])
                if old != current_phase:
                    changes.append(f"current phase {old}->{current_phase}")
                if current_lots:
                    out.append(f"Phase {current_phase} — current lots: {current_lots}")
                else:
                    out.append(f"Phase {current_phase}")
            replace_next_phase_line = False
            continue
        out.append(line)

    if in_out_of_scope and dropped:
        while out_of_scope_buffer and out_of_scope_buffer[-1] == "":
            out_of_scope_buffer.pop()
        for repo, num, title in dropped:
            out_of_scope_buffer.append(
                f"- {title} — dropped, see {issue_ref(repo, num)} (closed as not planned)"
            )
        out.extend(out_of_scope_buffer)
        out.append("")

    return "\n".join(out) + "\n", changes, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without writing; exit 1 when the roadmap would change",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"),
        help="GitHub API token (default: the GH_TOKEN or GITHUB_TOKEN"
        " environment variable)",
    )
    parser.add_argument(
        "--roadmap",
        type=Path,
        default=repo_root() / "generated" / "ROADMAP.md",
        help="path to ROADMAP.md (default: the repository root)",
    )
    args = parser.parse_args()

    original = args.roadmap.read_text(encoding="utf-8")
    text, migrated = migrate_links(original)
    if migrated:
        print(f"migrated {migrated} plain issue reference(s) to Markdown links")
    states: dict[str, tuple[dict[int, Issue], set[int]] | None] = {}
    for repo in REPOS:
        states[repo] = fetch_repo_state(repo, args.token)
    known = {repo: state for repo, state in states.items() if state is not None}
    if not known:
        warn("no repository could be read; aborting")
        return 2

    milestones = fetch_milestones(args.token)
    new_text, changes, warnings = sync_roadmap(
        text, known, milestones  # type: ignore[arg-type]
    )
    for warning in warnings:
        warn(warning)

    if warnings:
        warn(
            "validation failed; fix the warnings above and re-run — "
            "ROADMAP.md was not written"
        )
        return 3

    if new_text == text:
        if text == original:
            print("ROADMAP.md is up to date")
            return 0
        if args.check:
            print(f"ROADMAP.md is up to date (link migration pending: {migrated} reference(s))")
            return 1
        args.roadmap.write_text(text, encoding="utf-8")
        print(f"ROADMAP.md updated (link migration: {migrated} reference(s))")
        return 0

    if args.check:
        diff = difflib.unified_diff(
            text.splitlines(), new_text.splitlines(),
            fromfile=str(args.roadmap), tofile=str(args.roadmap), lineterm="",
        )
        for line in diff:
            print(line)
        print(f"ROADMAP.md is out of date ({len(changes)} changes needed)")
        return 1

    args.roadmap.write_text(new_text, encoding="utf-8")
    for change in changes:
        print(change)
    print(f"ROADMAP.md updated ({len(changes)} changes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
