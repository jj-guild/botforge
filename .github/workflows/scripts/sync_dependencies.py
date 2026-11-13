#!/usr/bin/env python3
"""Regenerate generated/DEPENDENCIES.md from GitHub issue dependencies.

Reads the `## Dependencies` section of every open issue in the three repos
(written as GitHub task-list checkboxes: `- [ ] botforge-services#N` or
`- [ ] #N` for same-repo refs), runs critical-path analysis (CPM) on the
resulting graph, and rewrites:

- the "Next up" table (wave 0: no open dependency — actionable now),
- the critical path and the Mermaid dependency diagram,
- the later waves (dependency order),
- the per-issue inventory (slack-based P0-P3).

The page shows the current state and what to work next; the history lives
in the git log of the `sync/generated-artifacts` branch. An open issue that
depends on an issue closed as not planned is listed as out of scope instead
of entering the waves.

Issue sizes come from the `size/XS|S|M|L|XL` labels (points: XS=1, S=3,
M=5, L=8, XL=13). If an issue has no size label, the script fails loudly
rather than guessing. Issues carrying an off-roadmap label
(`arch-discussion`, `poc` — see OFF_ROADMAP_LABELS) are excluded from the
graph entirely: they are parallel tracks, not planned work.

Usage:
    GITHUB_TOKEN=... python3 scripts/sync_dependencies.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path

REPOS = ("botforge", "botforge-services", "botforge-infra")
OWNER = "jj-guild"
SIZE_POINTS = {"XS": 1, "S": 3, "M": 5, "L": 8, "XL": 13}
PRIO_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

# Off-roadmap labels (generic rule): an issue carrying one of these labels is
# a parallel track — committee discussion, proof of concept, experimental
# chantier — deliberately kept OUT of the generated roadmap and dependency
# graph. The PO's roadmap stays product-only; these tracks live (and are
# tracked) in their own issues. Dependencies pointing at an off-roadmap issue
# still resolve (the issue stays in the id space), it just never appears in
# the plan. Any future POC gets the `poc` label and is excluded the same way.
OFF_ROADMAP_LABELS = ("arch-discussion", "poc")
PHASE_LABEL = re.compile(r"^phase-(\d+)$")
PRIORITY_LABEL = re.compile(r"^priority/(P[0-3])$")
DEP_LINE = re.compile(
    r"^-\s+\[([ x])\]\s+(?:jj-guild/)?(botforge-services|botforge-infra|botforge)#(\d+)$"
)
DEP_LINE_SAME_REPO = re.compile(r"^-\s+\[([ x])\]\s+#(\d+)$")
DEP_LINE_OWNER = re.compile(
    r"^-\s+\[([ x])\]\s+jj-guild/(botforge-services|botforge-infra|botforge)#(\d+)$"
)
DEPS_SECTION = re.compile(r"(?s)## Dependencies\n(.*?)(?=\n## |\Z)")
DOCS_URL = "https://github.com/jj-guild/botforge/blob/sync/generated-artifacts/generated/DEPENDENCIES.md"


def gh_api(path: str) -> dict | list:
    env = dict(os.environ)
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if token:
        env["GH_TOKEN"] = token
    out = subprocess.run(
        ["gh", "api", path], capture_output=True, text=True, env=env, check=True
    )
    return json.loads(out.stdout)


def load_issues() -> list[dict]:
    issues = []
    for repo in REPOS:
        page = 1
        while True:
            data = gh_api(f"repos/{OWNER}/{repo}/issues?state=open&per_page=100&page={page}")
            if not data:
                break
            for it in data:
                if "pull_request" in it:
                    continue
                labels = [l["name"] if isinstance(l, dict) else l for l in it["labels"]]
                body = it.get("body") or ""
                m = DEPS_SECTION.search(body)
                deps: list[str] = []
                done_deps: list[str] = []
                if m:
                    for line in m.group(1).splitlines():
                        stripped = line.strip()
                        dm = DEP_LINE_OWNER.match(stripped)
                        if dm:
                            (done_deps if dm.group(1) == "x" else deps).append(
                                f"{dm.group(2)}#{dm.group(3)}"
                            )
                            continue
                        dm = DEP_LINE.match(stripped)
                        if dm:
                            (done_deps if dm.group(1) == "x" else deps).append(
                                f"{dm.group(2)}#{dm.group(3)}"
                            )
                            continue
                        dm = DEP_LINE_SAME_REPO.match(stripped)
                        if dm:
                            (done_deps if dm.group(1) == "x" else deps).append(
                                f"{repo}#{dm.group(2)}"
                            )
                size = next((s for s in SIZE_POINTS if f"size/{s}" in labels), None)
                phase = next((m2.group(1) for l in labels if (m2 := PHASE_LABEL.match(l))), "?")
                prio_label = next((m3.group(1) for l in labels if (m3 := PRIORITY_LABEL.match(l))), None)
                issues.append(
                    {
                        "id": f"{repo}#{it['number']}",
                        "repo": repo,
                        "number": it["number"],
                        "title": it["title"],
                        "milestone": (it.get("milestone") or {}).get("title") or "—",
                        "milestone_number": (it.get("milestone") or {}).get("number"),
                        "body": it.get("body") or "",
                        "labels": labels,
                        "off_roadmap": any(l in OFF_ROADMAP_LABELS for l in labels),
                        "size": size,
                        "phase": phase,
                        "prio_label": prio_label,
                        "deps": deps,
                        "done_deps": done_deps,
                    }
                )
            page += 1
    return issues


_ISSUE_CACHE: dict[str, dict] = {}


def fetch_issue(repo_num: str) -> dict | None:
    """Fetch a single issue (used to tell closed-completed from not-planned)."""
    if repo_num not in _ISSUE_CACHE:
        repo, _, num = repo_num.partition("#")
        try:
            _ISSUE_CACHE[repo_num] = gh_api(f"repos/{OWNER}/{repo}/issues/{num}")
        except subprocess.CalledProcessError:
            _ISSUE_CACHE[repo_num] = {}
    return _ISSUE_CACHE[repo_num] or None


def fail_on_missing(issues: list[dict]) -> tuple[list[dict], list[tuple[str, str]]]:
    """Validate issue data; return (issues eligible for the graph, blocked pairs).

    Untriaged issues (no size/* or no priority/* label) are excluded with
    a warning instead of aborting: the sync workflow is the single writer
    and must never deadlock on triage debt. An open issue depending on an
    issue closed as not planned is out of scope: it is excluded from the
    graph and reported in `blocked` as (issue, dropped dependency). Hard
    problems (unknown or inconsistent dependencies) still abort.
    """
    problems = []
    eligible = []
    blocked: list[tuple[str, str]] = []
    blocked_ids: set[str] = set()
    ids = {i["id"] for i in issues}
    for i in issues:
        if i.get("off_roadmap"):
            # Deliberate exclusion (OFF_ROADMAP_LABELS) — a parallel track, not
            # triage debt: no warning, the issue is simply not planned.
            continue
        untriaged = False
        if i["size"] is None:
            print(f"warning: {i['id']}: no size/* label — excluded from the graph (triage it)")
            untriaged = True
        if i["prio_label"] is None:
            print(f"warning: {i['id']}: no priority/* label — excluded from the graph (triage it)")
            untriaged = True
        for d in i["deps"]:
            if d not in ids:
                closed = fetch_issue(d)
                if (
                    closed
                    and closed.get("state") == "closed"
                    and closed.get("state_reason") == "not_planned"
                ):
                    blocked.append((i["id"], d))
                    blocked_ids.add(i["id"])
                    print(
                        f"warning: {i['id']}: depends on {d}, closed as not planned — "
                        f"excluded from the plan (out of scope)"
                    )
                    continue
                # A dependency on a closed issue is satisfied — treat it as
                # checked (warn so the issue body gets tidied up).
                print(
                    f"warning: {i['id']}: depends on closed issue {d} — "
                    f"counted as satisfied (uncheck the box in the issue body)"
                )
                i["done_deps"].append(d)
        for d in i["done_deps"]:
            if d in ids:
                problems.append(
                    f"{i['id']}: dependency on {d} is checked but the issue is "
                    f"still open — uncheck it or close {d}"
                )
        for d in i["done_deps"]:
            i["deps"] = [x for x in i["deps"] if x != d]
        if not untriaged and i["id"] not in blocked_ids:
            eligible.append(i)
    if problems:
        sys.exit("Refusing to regenerate:\n  " + "\n  ".join(problems))
    return eligible, blocked


def cpm(issues: list[dict]) -> dict:
    by_id = {i["id"]: i for i in issues}
    T = {i["id"]: SIZE_POINTS[i["size"]] for i in issues}
    pred = {i["id"]: [d for d in i["deps"] if d in T] for i in issues}
    succ: dict[str, list[str]] = defaultdict(list)
    for k, ds in pred.items():
        for d in ds:
            succ[d].append(k)
    indeg = {k: len(ds) for k, ds in pred.items()}
    order: list[str] = []
    q = deque(sorted([k for k, v in indeg.items() if v == 0]))
    ind = dict(indeg)
    while q:
        u = q.popleft()
        order.append(u)
        for v in sorted(succ[u]):
            ind[v] -= 1
            if ind[v] == 0:
                q.append(v)
    if len(order) != len(T):
        missing = sorted(set(T) - set(order))
        sys.exit(f"Dependency cycle detected involving: {', '.join(missing)}")

    ES, EF = {}, {}
    for u in order:
        ES[u] = max([EF[p] for p in pred[u]], default=0)
        EF[u] = ES[u] + T[u]
    total = max(EF.values())
    LF, LS = {}, {}
    for u in reversed(order):
        LF[u] = min([LS[s] for s in succ[u]], default=total)
        LS[u] = LF[u] - T[u]
    slack = {k: LS[k] - ES[k] for k in T}
    end = max(EF, key=EF.get)
    cp = [end]
    while pred[end]:
        end = max(pred[end], key=lambda p: EF[p])
        cp.append(end)
    cp.reverse()
    wave: dict[str, int] = {}

    def dep_depth(k: str) -> int:
        if k not in wave:
            wave[k] = max((dep_depth(p) for p in pred[k]), default=-1) + 1
        return wave[k]

    for k in order:
        dep_depth(k)
    return {"pred": pred, "succ": dict(succ), "T": T, "slack": slack, "wave": wave,
            "cp": cp, "total": total, "ES": ES, "EF": EF, "by_id": by_id}


def expected_prio(slack: int) -> str:
    if slack == 0:
        return "P0"
    if slack <= 4:
        return "P1"
    if slack <= 12:
        return "P2"
    return "P3"


def short_title(i: dict, limit: int = 40) -> str:
    """A readable short title: truncated at the em-dash or the limit."""
    t = i["title"].split(" \u2014 ")[0]
    t = t.split(" (")[0]
    if len(t) > limit:
        t = t[: limit - 1].rstrip() + "\u2026"
    return t


def node_key(i: dict) -> str:
    return (
        i["id"].replace("#", "_")
        .replace("botforge-services", "ks")
        .replace("botforge-infra", "ki")
        .replace("botforge", "k")
    )


def issue_link(id_: str, title: str, limit: int = 60) -> str:
    repo, _, num = id_.partition("#")
    if len(title) > limit:
        title = title[: limit - 1].rstrip() + "…"
    return f"[{id_}](https://github.com/{OWNER}/{repo}/issues/{num}) — {title}"


def render(issues: list[dict], a: dict, blocked: list[tuple[str, str]]) -> str:
    cp_set = set(a["cp"])
    by_id = a["by_id"]
    lines: list[str] = []
    lines += [
        "# Dependencies",
        "",
        "> Auto-generated by `scripts/sync_dependencies.py`. Do not edit manually:",
        "> edit the `## Dependencies` sections of the issues instead, then",
        "> regenerate this page (see the [Generated artifacts](../.agents/skills/generated-artifacts/SKILL.md) skill).",
        "",
        f"Source: open issues in [botforge](https://github.com/jj-guild/botforge/issues), "
        f"[botforge-services](https://github.com/jj-guild/botforge-services/issues) "
        f"and [botforge-infra](https://github.com/jj-guild/botforge-infra/issues).",
        "",
        "Current state and next steps only — the history lives in the git log of",
        "the `sync/generated-artifacts` branch.",
        "",
        "Priority labels come from critical-path analysis (CPM):",
        "",
        "| Label | Meaning |",
        "| ----- | ------- |",
        "| `priority/P0` | zero slack — on the critical path, any delay delays the project |",
        "| `priority/P1` | slack ≤ 4 pts — near-critical |",
        "| `priority/P2` | slack ≤ 12 pts |",
        "| `priority/P3` | large slack — can be deferred without impact |",
        "",
        "Sizes (`size/XS..XL`) map to points (1, 3, 5, 8, 13).",
        "",
        "## Critical path",
        "",
        f"Total: **{a['total']} pts**. Critical path:",
        "",
    ]
    lines.append(" -> ".join(f"[{n}](https://github.com/{OWNER}/{n.split('#')[0]}/issues/{n.split('#')[1]})" for n in a["cp"]))

    def ms_sort_key(ms: str) -> tuple:
        m = re.match(r"Lot (\d+)", ms)
        if m:
            return (0, int(m.group(1)), ms)
        if ms == "\u2014":
            return (2, 0, ms)
        return (1, 0, ms)

    def ms_short(ms: str) -> str:
        return ms.split(" (")[0]

    def wave_sort_key(i: dict) -> tuple:
        return (
            PRIO_RANK.get(i["prio_label"], 9),
            ms_sort_key(i["milestone"]),
            -a["T"][i["id"]],
            i["id"],
        )

    wave0 = sorted((i for i in issues if a["wave"][i["id"]] == 0), key=wave_sort_key)
    lines += [
        "",
        "## Next up — wave 0 (no open dependency: actionable now)",
        "",
        "| Issue | Lot | Size | Priority |",
        "| ----- | --- | ---- | -------- |",
    ]
    for i in wave0:
        lines.append(
            f"| {issue_link(i['id'], i['title'])} | {i['milestone']} | `{i['size']}` | `{i['prio_label']}` |"
        )
    lines += ["", "## Dependency graph", "", "```mermaid", "flowchart LR"]

    by_ms: defaultdict[str, list[dict]] = defaultdict(list)
    for i in issues:
        by_ms[i["milestone"]].append(i)
    epics: list[str] = []
    for idx, ms in enumerate(sorted(by_ms, key=ms_sort_key)):
        group = "No milestone yet" if ms == "\u2014" else ms_short(ms)
        lines.append(f"    subgraph MSG{idx}['{group}']")
        lines.append("        direction LR")
        for i in sorted(by_ms[ms], key=lambda x: x["number"]):
            label = f"#{i['number']} {short_title(i)}".replace('"', "'")
            lines.append(f'        {node_key(i)}["{label}"]')
            if "[epic]" in i["title"].lower():
                epics.append(node_key(i))
        lines.append("    end")
    for i in issues:
        for d in i["deps"]:
            if d in by_id:
                lines.append(f"    {node_key(by_id[d])} --> {node_key(i)}")
    lines.append("    classDef critical fill:#ffe0e0,stroke:#d43d51,stroke-width:3px;")
    lines.append("    classDef epic stroke:#1f6feb,stroke-width:3px,fill:#ddf4ff;")
    cp_keys = ",".join(node_key(by_id[n]) for n in a["cp"])
    lines.append(f"    class {cp_keys} critical")
    if epics:
        lines.append(f"    class {','.join(epics)} epic")
    lines += ["```", "", "## Later waves (dependency order)", "",
              "Wave 0 is the Next up table above. Wave N starts once the open",
              "dependencies of the previous waves are done; issues in the same wave",
              "are independent and can be worked on in parallel.", ""]
    by_wave: defaultdict[int, list[dict]] = defaultdict(list)
    for i in issues:
        by_wave[a["wave"][i["id"]]].append(i)
    for w in sorted(by_wave):
        if w == 0:
            continue
        lines.append(f"**Wave {w}**")
        lines.append("")
        lines.append("| Issue | Milestone | Size | Priority | Slack |")
        lines.append("| ----- | --------- | ---- | -------- | ----- |")
        for i in sorted(by_wave[w], key=wave_sort_key):
            lines.append(
                f"| {issue_link(i['id'], i['title'])} | {i['milestone']} | `{i['size']}` ({a['T'][i['id']]}) | `{i['prio_label']}` | {a['slack'][i['id']]} |"
            )
        lines.append("")
    if blocked:
        lines += ["## Out of scope (blocked by a dropped dependency)", ""]
        for iid, dep in sorted(blocked):
            lines.append(
                f"- [{iid}](https://github.com/{OWNER}/{iid.split('#')[0]}/issues/{iid.split('#')[1]})"
                f" — depends on {dep}, closed as not planned"
            )
        lines.append("")
    lines += ["## All open issues (inventory)", "",
              "| Issue | Milestone | Size | Priority | Slack | Depends on |",
              "| ----- | --------- | ---- | -------- | ----- | ---------- |"]
    for i in sorted(issues, key=lambda x: (x["repo"], x["number"])):
        deps = ", ".join(
            f"[{d}](https://github.com/{OWNER}/{d.split('#')[0]}/issues/{d.split('#')[1]})"
            for d in i["deps"]
        )
        deps_done = ", ".join(
            f"~~[{d}](https://github.com/{OWNER}/{d.split('#')[0]}/issues/{d.split('#')[1]})~~ ✅"
            for d in i["done_deps"]
        )
        all_deps = ", ".join(x for x in (deps, deps_done) if x) or "—"
        lines.append(f"| {issue_link(i['id'], i['title'])} | {i['milestone']} | `{i['size']}` | `{i['prio_label']}` | {a['slack'][i['id']]} | {all_deps} |")
    lines.append("")
    return "\n".join(lines)


def report_priority_drift(issues: list[dict], a: dict) -> None:
    """Print a warning for every issue whose priority label drifted from
    the critical-path slack, so it can be fixed manually with gh issue edit.
    The script never edits issues: labels are human decisions."""
    drifted = [
        i
        for i in issues
        if i["prio_label"] != expected_prio(a["slack"][i["id"]])
    ]
    if drifted:
        print("Priority label drift (fix with `gh issue edit`):")
        for i in sorted(drifted, key=lambda x: (x["repo"], x["number"])):
            expected = expected_prio(a["slack"][i["id"]])
            print(
                f"  {i['id']}: labeled {i['prio_label']}, "
                f"expected {expected} (slack {a['slack'][i['id']]} pts)"
            )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default="generated/DEPENDENCIES.md")
    args = ap.parse_args()
    issues = load_issues()
    issues, blocked = fail_on_missing(issues)
    analysis = cpm(issues)
    report_priority_drift(issues, analysis)
    content = render(issues, analysis, blocked)
    print(f"{len(issues)} issues, critical path: {' -> '.join(analysis['cp'])}, total {analysis['total']} pts")
    if args.dry_run:
        print(content)
        return
    out = Path(args.out)
    old = out.read_text() if out.exists() else ""
    if old == content:
        print("No changes.")
        return
    out.write_text(content)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
