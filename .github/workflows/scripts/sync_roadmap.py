#!/usr/bin/env python3
"""Regenerate generated/ROADMAP.md from GitHub issues and milestones.

The roadmap is the future, not the past: the generated page shows the
current lot, the open issues that block closing it (in work order), the
upcoming lots with their description, and the out-of-scope / no-lot
issues. Done issues and the change history live on GitHub and in the git
log of the `sync/generated-artifacts` branch — they are deliberately not
listed here.

The file is regenerated from scratch on every run; the only thing carried
over from the previous revision is the manual statuses (`in-progress` /
`blocked` / `backlog`), parsed from the old file's issue lines.

The three Kingdoms repositories are public; everything is read through
`gh api` (no custom secret). Usage:

    python3 .github/workflows/scripts/sync_roadmap.py [--check] [--roadmap PATH]

Exit codes: 0 success (or --check without drift), 1 drift in --check mode,
2 fatal error (unreadable repositories fail closed).
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sync_dependencies as sd  # noqa: E402

OWNER = "merlin-pinpin-org"
REPOS = ("kingdoms", "kingdoms-services", "kingdoms-infra")
MANUAL_STATUSES = ("in-progress", "blocked", "backlog")
STATUSES = ("todo", "in-progress", "in-review", "done", "blocked", "dropped")
PRIO_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
LOT_RE = re.compile(r"^Lot (\d+)")
CLOSING_REF_RE = re.compile(
    r"\b(?:close[ds]?|closing|fix(?:e[ds]?)?|fixing|resolv(?:e[ds]?)?|resolving)"
    r"[\s:;,.'\"()\[\]]*(?:(?P<owner>[\w.-]+)/(?P<ref_repo>[\w.-]+))?"
    r"#(?P<num>\d+)",
    re.IGNORECASE,
)
ISSUE_URL_RE = re.compile(
    r"https://github\.com/[\w.-]+/(?P<repo>[\w.-]+)/issues/(?P<num>\d+)"
)
STATUS_TOKEN_RE = re.compile(r"\b(todo|in-progress|in-review|done|blocked|dropped|backlog)\b")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def api_get(path: str, token: str | None) -> list[dict]:
    """Return all pages of a GET request, via `gh api --paginate --slurp`."""
    env = dict(os.environ)
    if token:
        env["GH_TOKEN"] = token
    result = subprocess.run(
        ["gh", "api", "--paginate", "--slurp", path],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh api {path}: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    if data and all(isinstance(page, list) for page in data):
        return [item for page in data for item in page]
    return data


def fetch_milestones(token: str | None) -> dict[tuple[str, int], dict] | None:
    """Return {(repo, number): milestone} across the three repos, or None."""
    milestones: dict[tuple[str, int], dict] = {}
    for repo in REPOS:
        try:
            raw = api_get(f"/repos/{OWNER}/{repo}/milestones?state=all", token)
        except RuntimeError as error:
            warn(f"cannot read milestones of {OWNER}/{repo}: {error}")
            return None
        for item in raw:
            milestones[(repo, item["number"])] = item
    return milestones


def fetch_closed_not_planned(token: str | None) -> list[tuple[str, int, str, str]]:
    """Return (repo, number, title, url) for issues closed as not planned."""
    out: list[tuple[str, int, str, str]] = []
    for repo in REPOS:
        try:
            items = api_get(f"/repos/{OWNER}/{repo}/issues?state=closed", token)
        except RuntimeError as error:
            warn(f"cannot read closed issues of {OWNER}/{repo}: {error}")
            continue
        for it in items:
            if "pull_request" in it:
                continue
            if it.get("state_reason") == "not_planned":
                num = it["number"]
                out.append(
                    (repo, num, it.get("title") or "", issue_url(repo, num))
                )
    out.sort(key=lambda x: (x[0], x[1]))
    return out


def fetch_open_pulls(token: str | None) -> tuple[dict[str, str], dict[str, dict[int, str]]]:
    """Return (issue id -> PR url via closing refs, repo -> {pr number: url})."""
    by_issue: dict[str, str] = {}
    by_repo: dict[str, dict[int, str]] = {}
    for repo in REPOS:
        try:
            pulls = api_get(f"/repos/{OWNER}/{repo}/pulls?state=open", token)
        except RuntimeError as error:
            warn(f"cannot list open PRs of {OWNER}/{repo}: {error}; no PR detection")
            pulls = []
        by_repo[repo] = {p["number"]: p["html_url"] for p in pulls}
        for pull in pulls:
            for m in CLOSING_REF_RE.finditer(pull.get("body") or ""):
                if m["ref_repo"] and m["ref_repo"] != repo:
                    continue
                by_issue[f"{repo}#{m['num']}"] = pull["html_url"]
    return by_issue, by_repo


def parse_manual_statuses(text: str) -> dict[tuple[str, int], str]:
    """Recover the statuses from the previous revision's issue lines.

    Only manual statuses matter downstream (in-progress / blocked /
    backlog); everything else is recomputed from GitHub state.
    """
    out: dict[tuple[str, int], str] = {}
    for line in text.splitlines():
        if not (line.startswith("|") or line.startswith("- ")):
            continue
        refs = ISSUE_URL_RE.findall(line)
        if not refs:
            continue
        tokens = STATUS_TOKEN_RE.findall(line)
        if not tokens:
            continue
        status = tokens[-1]
        for repo, num in refs:
            out[(repo, int(num))] = status
    return out


def issue_url(repo: str, num: int) -> str:
    return f"https://github.com/{OWNER}/{repo}/issues/{num}"


def milestone_url(repo: str, num: int) -> str:
    return f"https://github.com/{OWNER}/{repo}/milestone/{num}"


def pr_links_for(
    issue: dict, by_issue: dict[str, str], by_repo: dict[str, dict[int, str]]
) -> list[str]:
    """PR urls linked to an issue, both directions: closing refs in open PR
    bodies, and PR numbers referenced in the issue's own title/body."""
    links: list[str] = []
    if issue["id"] in by_issue:
        links.append(by_issue[issue["id"]])
    seen = set(links)
    text = f"{issue.get('title') or ''}\n{issue.get('body') or ''}"
    for m in re.finditer(r"#(\d+)", text):
        url = by_repo.get(issue["repo"], {}).get(int(m.group(1)))
        if url and url not in seen:
            seen.add(url)
            links.append(url)
    return links


def status_of(issue: dict, by_issue: dict[str, str], current_status: dict) -> str:
    if issue["id"] in by_issue:
        return "in-review"
    current = current_status.get((issue["repo"], issue["number"]))
    if current in MANUAL_STATUSES:
        return current
    return "todo"


def issue_line(
    issue: dict,
    status: str,
    pulls: tuple[dict[str, str], dict[str, dict[int, str]]],
) -> str:
    by_issue, by_repo = pulls
    line = (
        f"- [#{issue['number']} — {issue['title']}]({issue_url(issue['repo'], issue['number'])})"
        f" — `{status}`"
    )
    if issue.get("prio_label"):
        line += f" · {issue['prio_label']}"
    if issue.get("size"):
        line += f" · size {issue['size']}"
    for url in pr_links_for(issue, by_issue, by_repo):
        line += f" · PR [#{url.rsplit('/', 1)[-1]}]({url})"
    return line


def lot_sort_key(title: str, repo: str, num: int) -> tuple:
    m = LOT_RE.match(title or "")
    if m:
        return (0, int(m.group(1)), title, num)
    return (1, 0, title or "", num)


def build_roadmap(
    open_issues: list[dict],
    eligible: list[dict],
    analysis: dict,
    milestones: dict[tuple[str, int], dict] | None,
    closed_not_planned: list[tuple[str, int, str, str]],
    pulls: tuple[dict[str, str], dict[str, dict[int, str]]],
    current_status: dict[tuple[str, int], str],
) -> str:
    wave = analysis["wave"]
    slack = analysis["slack"]

    if not milestones:
        milestones = {}
        for i in open_issues:
            key = (i["repo"], i.get("milestone_number"))
            if i.get("milestone_number") is not None and key not in milestones:
                milestones[key] = {
                    "title": i["milestone"],
                    "state": "open",
                    "description": "",
                }

    open_count: dict[tuple[str, int], int] = defaultdict(int)
    by_ms: dict[tuple[str, int], list[dict]] = defaultdict(list)
    no_lot: list[dict] = []
    for i in open_issues:
        if i.get("milestone_number") is not None:
            key = (i["repo"], i["milestone_number"])
            open_count[key] += 1
            by_ms[key].append(i)
        else:
            no_lot.append(i)

    lots = []
    for (repo, num), ms in milestones.items():
        if ms.get("state") != "open":
            continue
        if open_count.get((repo, num), 0) == 0:
            continue
        lots.append((lot_sort_key(ms.get("title") or "", repo, num), repo, num, ms))
    lots.sort(key=lambda x: x[0])

    def work_order_key(i: dict) -> tuple:
        iid = i["id"]
        return (
            wave.get(iid, 10**9),
            PRIO_RANK.get(i.get("prio_label"), 9),
            slack.get(iid, 10**9),
            i["number"],
        )

    lines: list[str] = [
        "# Kingdoms Roadmap",
        "",
        "> Current state and next steps of the plan, regenerated from the GitHub",
        "> issues — the past (done issues, change history) lives on GitHub and in",
        "> the git log of the `sync/generated-artifacts` branch. Single writer: the",
        "> [Generated artifacts](../.agents/skills/generated-artifacts/SKILL.md) workflow.",
        "",
        "Status values: `todo` / `in-progress` / `in-review` / `done` / `blocked` / `dropped`.",
        "",
    ]

    lines += ["## Current lot", ""]
    if lots:
        _, repo, num, ms = lots[0]
        title = ms.get("title") or f"milestone {num}"
        lines.append(
            f"- [{title}]({milestone_url(repo, num)}) — **{open_count[(repo, num)]} open**"
        )
        lines.append("")
        lines += [
            "### Open issues — what blocks closing the current lot, in work order",
            "",
            "Order: dependency wave → priority label → slack → issue number."
            " Details and full graph: [DEPENDENCIES.md](DEPENDENCIES.md).",
            "",
        ]
        current_issues = sorted(by_ms.get((repo, num), []), key=work_order_key)
        if current_issues:
            for i in current_issues:
                lines.append(issue_line(i, status_of(i, pulls[0], current_status), pulls))
        else:
            lines.append("- (none — the lot can be closed)")
        lines.append("")
    else:
        lines.append("- none — every lot is closed")
        lines.append("")

    lines += ["## Upcoming lots", ""]
    if len(lots) > 1:
        for _, repo, num, ms in lots[1:]:
            title = ms.get("title") or f"milestone {num}"
            lines.append(
                f"- [{title}]({milestone_url(repo, num)}) — {open_count[(repo, num)]} open"
            )
            desc = re.sub(r"\s+", " ", (ms.get("description") or "").strip().split("\n\n")[0])
            if desc:
                if len(desc) > 240:
                    desc = desc[:239].rstrip() + "…"
                lines.append(f"  - {desc}")
    else:
        lines.append("- (none)")
    lines.append("")

    lines += ["## Out of scope / no lot", "", "Open issues without a lot:", ""]
    if no_lot:
        for i in sorted(
            no_lot, key=lambda x: (PRIO_RANK.get(x.get("prio_label"), 9), x["repo"], x["number"])
        ):
            lines.append(issue_line(i, status_of(i, pulls[0], current_status), pulls))
    else:
        lines.append("- (none)")
    lines.append("")
    lines += ["Dropped (closed as not planned):", ""]
    if closed_not_planned:
        for repo, num, title, url in closed_not_planned:
            lines.append(f"- [#{num} — {title}]({url})")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


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
        help="GitHub token for gh api (default: GH_TOKEN/GITHUB_TOKEN env)",
    )
    parser.add_argument(
        "--roadmap",
        type=Path,
        default=repo_root() / "generated" / "ROADMAP.md",
        help="path to ROADMAP.md (default: <repo>/generated/ROADMAP.md)",
    )
    args = parser.parse_args()

    try:
        open_issues = sd.load_issues()
    except subprocess.CalledProcessError as error:
        warn(f"cannot read the open issues: {error}")
        return 2
    if not open_issues:
        warn("no open issues read; the GitHub API may have failed silently")
        return 2
    eligible, _blocked = sd.fail_on_missing(open_issues)
    analysis = sd.cpm(eligible)
    milestones = fetch_milestones(args.token)
    closed_not_planned = fetch_closed_not_planned(args.token)
    pulls = fetch_open_pulls(args.token)

    original = args.roadmap.read_text(encoding="utf-8") if args.roadmap.exists() else ""
    current_status = parse_manual_statuses(original)
    new_text = build_roadmap(
        open_issues, eligible, analysis, milestones, closed_not_planned, pulls, current_status
    )

    if new_text == original:
        print("ROADMAP.md is up to date")
        return 0
    if args.check:
        diff = difflib.unified_diff(
            original.splitlines(),
            new_text.splitlines(),
            fromfile=str(args.roadmap),
            tofile=str(args.roadmap),
            lineterm="",
        )
        for line in diff:
            print(line)
        print("ROADMAP.md is out of date")
        return 1
    args.roadmap.write_text(new_text, encoding="utf-8")
    print(f"ROADMAP.md regenerated ({len(new_text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
