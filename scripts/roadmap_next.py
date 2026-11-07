#!/usr/bin/env python3
"""Print the current lot's work order — the read-only, agent-facing half of
the roadmap tooling.

The generated artifacts (generated/ROADMAP.md, generated/DEPENDENCIES.md on
the sync/generated-artifacts branch) are written ONLY by the sync-generated
workflow; this script never writes them. It reuses the parsers and the CPM of
.github/workflows/scripts/sync_dependencies.py so the GitHub issues stay the
single source of truth.

Usage:
    python3 scripts/roadmap_next.py            # current lot's work table
    python3 scripts/roadmap_next.py --lot 4    # another lot
    python3 scripts/roadmap_next.py --lots     # per-lot summary
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import sync_dependencies as sd  # noqa: E402
import sync_roadmap as sr  # noqa: E402

PRIO_FR = {
    "P0": "P0 — critique (chemin critique)",
    "P1": "P1 — quasi-critique",
    "P2": "P2 — modérée",
    "P3": "P3 — peut attendre",
}


def lot_number(milestone_title: str) -> int | None:
    m = re.match(r"Lot (\d+)", milestone_title or "")
    return int(m.group(1)) if m else None


def issue_url(repo: str, num: int) -> str:
    return f"https://github.com/{sd.OWNER}/{repo}/issues/{num}"


def open_prs() -> tuple[dict[str, str], dict[str, dict[int, str]]]:
    """Return (issue id -> PR url via closing refs, repo -> {pr number: url})."""
    by_issue: dict[str, str] = {}
    by_repo: dict[str, dict[int, str]] = {}
    for repo in sd.REPOS:
        pulls = sd.gh_api(f"repos/{sd.OWNER}/{repo}/pulls?state=open&per_page=100")
        by_repo[repo] = {p["number"]: p["html_url"] for p in pulls}
        for pull in pulls:
            for m in sr.CLOSING_REF_RE.finditer(pull.get("body") or ""):
                if m["ref_repo"] and m["ref_repo"] != repo:
                    continue
                by_issue[f"{repo}#{m['num']}"] = pull["html_url"]
    return by_issue, by_repo


def pr_links_for(issue: dict, by_issue: dict[str, str], by_repo: dict[str, dict[int, str]]) -> list[str]:
    """PR URLs linked to an issue, both directions: closing refs in open PR
    bodies, and PR numbers referenced in the issue's own title/body."""
    links = []
    if issue["id"] in by_issue:
        links.append(by_issue[issue["id"]])
    seen = set(links)
    open_nums = by_repo.get(issue["repo"], {})
    text = f"{issue.get('title') or ''}\n{issue.get('body') or ''}"
    for m in re.finditer(r"#(\d+)", text):
        url = open_nums.get(int(m.group(1)))
        if url and url not in seen:
            seen.add(url)
            links.append(url)
    return links


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lot", type=int, default=None, help="lot number to list (default: current)")
    ap.add_argument("--lots", action="store_true", help="print the per-lot summary instead")
    args = ap.parse_args()

    issues = sd.load_issues()
    eligible, blocked = sd.fail_on_missing(issues)
    a = sd.cpm(eligible)
    pr_by_issue, pr_by_repo = open_prs()

    lots: dict[int, list[dict]] = {}
    titles: dict[int, str] = {}
    for i in eligible:
        n = lot_number(i["milestone"])
        if n is not None:
            lots.setdefault(n, []).append(i)
            titles.setdefault(n, i["milestone"])

    if args.lots or not lots:
        for n in sorted(lots):
            print(f"{titles[n].split(' (')[0]}: {len(lots[n])} open issues")
        if not lots:
            print("No open Lot milestone with triaged issues.")
        return 0

    current = args.lot if args.lot is not None else min(lots)
    if current not in lots:
        print(f"Lot {current} has no open triaged issues. Open lots: {sorted(lots)}")
        return 1
    lot_issues = sorted(
        lots[current],
        key=lambda i: (
            a["wave"][i["id"]],
            sd.PRIO_RANK.get(i["prio_label"], 9),
            a["slack"][i["id"]],
            i["number"],
        ),
    )

    print(f"# Current lot: {titles[current].split(' (')[0]} ({len(lot_issues)} open issues)")
    print()
    print("Work order: dependency wave first (an issue with open dependencies cannot start),")
    print("then priority label (P0 first), then slack (critical path first), then issue number.")
    print()
    print("| Issue / PR | Priority (fr) | Summary | Details | Lot |")
    print("|------------|---------------|---------|---------|-----|")
    for i in lot_issues:
        iid = i["id"]
        critical = "★ critical path, " if iid in a["cp"] else ""
        details = (
            f"{critical}wave {a['wave'][iid]}, {len(a['succ'].get(iid, []))} dependent(s), "
            f"size {i['size']} ({a['T'][iid]} pts), slack {a['slack'][iid]}"
        )
        prs = pr_links_for(i, pr_by_issue, pr_by_repo)
        pr_cell = "<br>".join(f"PR: [#{u.rsplit('/', 1)[-1]}]({u})" for u in prs) if prs else "PR: —"
        issue_cell = f"issue: [{iid}]({issue_url(i['repo'], i['number'])})<br>{pr_cell}"
        print(
            f"| {issue_cell} | {PRIO_FR.get(i['prio_label'], i['prio_label'])} "
            f"| {sd.short_title(i, 60)} | {details} | {i['milestone'].split(' (')[0]} |"
        )
    blocked_in_lot = [b for b in blocked if b[0] in {i["id"] for i in lots[current]}]
    if blocked_in_lot:
        print()
        for iid, dep in blocked_in_lot:
            print(f"- {iid} is out of scope: depends on {dep} (closed as not planned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
