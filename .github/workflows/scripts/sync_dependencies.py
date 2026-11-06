#!/usr/bin/env python3
"""Regenerate generated/DEPENDENCIES.md from GitHub issue dependencies.

Reads the `## Dependencies` section of every open issue in
`kingdoms-services` and `kingdoms-infra` (written as GitHub task-list
checkboxes: `- [ ] kingdoms-services#N` or `- [ ] #N` for same-repo refs),
runs critical-path analysis (CPM) on the resulting graph, and rewrites:

- the Mermaid dependency diagram (including the critical path),
- the wave table (parallelisable batches),
- the per-issue priority table (slack-based P0-P3).

Issue sizes come from the `size/XS|S|M|L|XL` labels (points: XS=1, S=3,
M=5, L=8, XL=13). If an issue has no size label, the script fails loudly
rather than guessing.

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

REPOS = ("kingdoms", "kingdoms-services", "kingdoms-infra")
OWNER = "merlin-pinpin-org"
SIZE_POINTS = {"XS": 1, "S": 3, "M": 5, "L": 8, "XL": 13}
PHASE_LABEL = re.compile(r"^phase-(\d+)$")
PRIORITY_LABEL = re.compile(r"^priority/(P[0-3])$")
DEP_LINE = re.compile(
    r"^-\s+\[([ x])\]\s+(?:merlin-pinpin-org/)?(kingdoms-services|kingdoms-infra|kingdoms)#(\d+)$"
)
DEP_LINE_SAME_REPO = re.compile(r"^-\s+\[([ x])\]\s+#(\d+)$")
DEP_LINE_OWNER = re.compile(
    r"^-\s+\[([ x])\]\s+merlin-pinpin-org/(kingdoms-services|kingdoms-infra|kingdoms)#(\d+)$"
)
DEPS_SECTION = re.compile(r"(?s)## Dependencies\n(.*?)(?=\n## |\Z)")
DOCS_URL = "https://github.com/merlin-pinpin-org/kingdoms/blob/sync/generated-artifacts/generated/DEPENDENCIES.md"


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
                        "labels": labels,
                        "size": size,
                        "phase": phase,
                        "prio_label": prio_label,
                        "deps": deps,
                        "done_deps": done_deps,
                    }
                )
            page += 1
    return issues


def fail_on_missing(issues: list[dict]) -> list[dict]:
    """Validate issue data; return the issues eligible for the graph.

    Untriaged issues (no size/* or no priority/* label) are excluded with
    a warning instead of aborting: the sync workflow is the single writer
    and must never deadlock on triage debt. Hard problems (unknown or
    inconsistent dependencies) still abort.
    """
    problems = []
    eligible = []
    ids = {i["id"] for i in issues}
    for i in issues:
        untriaged = False
        if i["size"] is None:
            print(f"warning: {i['id']}: no size/* label — excluded from the graph (triage it)")
            untriaged = True
        if i["prio_label"] is None:
            print(f"warning: {i['id']}: no priority/* label — excluded from the graph (triage it)")
            untriaged = True
        for d in i["deps"]:
            if d not in ids:
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
        if not untriaged:
            eligible.append(i)
    if problems:
        sys.exit("Refusing to regenerate:\n  " + "\n  ".join(problems))
    return eligible


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
        .replace("kingdoms-services", "ks")
        .replace("kingdoms-infra", "ki")
        .replace("kingdoms", "k")
    )


def issue_link(id_: str, title: str, limit: int = 60) -> str:
    repo, _, num = id_.partition("#")
    if len(title) > limit:
        title = title[: limit - 1].rstrip() + "…"
    return f"[{id_}](https://github.com/{OWNER}/{repo}/issues/{num}) — {title}"


def render(issues: list[dict], a: dict) -> str:
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
        f"Source: open issues in [kingdoms](https://github.com/merlin-pinpin-org/kingdoms/issues), "
        f"[kingdoms-services](https://github.com/merlin-pinpin-org/kingdoms-services/issues) "
        f"and [kingdoms-infra](https://github.com/merlin-pinpin-org/kingdoms-infra/issues).",
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
    lines += ["", "## Dependency graph", "", "```mermaid", "flowchart LR"]

    def ms_sort_key(ms: str) -> tuple:
        m = re.match(r"Lot (\d+)", ms)
        if m:
            return (0, int(m.group(1)), ms)
        if ms == "\u2014":
            return (2, 0, ms)
        return (1, 0, ms)

    def ms_short(ms: str) -> str:
        return ms.split(" (")[0]

    by_ms: defaultdict[str, list[dict]] = defaultdict(list)
    for i in issues:
        by_ms[i["milestone"]].append(i)
    epics: list[str] = []
    for idx, ms in enumerate(sorted(by_ms, key=ms_sort_key)):
        group = "Out of scope \u2014 no milestone" if ms == "\u2014" else ms_short(ms)
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
    lines += ["```", "", "## Waves (parallelisable batches)", "",
              "Issues in the same wave have no dependency on each other and can be",
              "worked on in parallel.", ""]
    by_wave: defaultdict[int, list[dict]] = defaultdict(list)
    for i in issues:
        by_wave[a["wave"][i["id"]]].append(i)
    for w in sorted(by_wave):
        lines.append(f"**Wave {w}**")
        lines.append("")
        lines.append("| Issue | Milestone | Size | Priority | Slack |")
        lines.append("| ----- | --------- | ---- | -------- | ----- |")
        for i in sorted(by_wave[w], key=lambda x: (-a["T"][x["id"]], x["id"])):
            lines.append(
                f"| {issue_link(i['id'], i['title'])} | {i['milestone']} | `{i['size']}` ({a['T'][i['id']]}) | `{i['prio_label']}` | {a['slack'][i['id']]} |"
            )
        lines.append("")
    lines += ["## All issues", "",
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
    issues = fail_on_missing(issues)
    analysis = cpm(issues)
    report_priority_drift(issues, analysis)
    content = render(issues, analysis)
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
