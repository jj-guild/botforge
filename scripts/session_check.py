#!/usr/bin/env python3
"""Session checklist, run mechanically (docs/CONVENTIONS.md).

Fail-closed check of everything a session must leave consistent across the
three BotForge repositories:

- docs validation: scripts/validate_docs.py --check (mods docs, docstrings,
  Mermaid syntax) against the botforge-services clone;
- roadmap drift: scripts/sync_roadmap.py --check (issue states vs the
  generated ROADMAP.md — the sync-generated workflow publishes it on the
  sync/generated-artifacts branch; a local mismatch only means the
  workflow has not run since the issue change, it is NOT a session error);
- dependency-graph drift: scripts/sync_dependencies.py --dry-run against the
  committed generated/DEPENDENCIES.md (open issues, size/priority labels).

Exit code is non-zero when any check fails; each failure line names the exact
artefact to fix. The script never commits anything; it may export the
generated artifacts from the sync/generated-artifacts branch into the
untracked local generated/ directory so the drift checks can run on a
fresh clone (main carries no generated files).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPOS = ("botforge", "botforge-infra", "botforge-services")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def run_check(name: str, cmd: list[str]) -> list[str]:
    """Run one check; return its failure lines (empty when it passes)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"PASS  {name}")
        return []
    print(f"FAIL  {name}")
    lines = (result.stdout + result.stderr).strip().splitlines()
    return [f"{name}: {line}" for line in lines if line]


def ensure_generated_artifacts(root: Path) -> list[str]:
    """Materialize generated/ROADMAP.md from the sync branch when absent.

    Main carries no generated files; sync_roadmap.py --check reads the
    local generated/ROADMAP.md, so a fresh clone must export it from the
    sync/generated-artifacts branch first (untracked, never committed).
    """
    roadmap = root / "generated" / "ROADMAP.md"
    if roadmap.exists():
        return []
    result = subprocess.run(
        ["git", "show", "origin/sync/generated-artifacts:generated/ROADMAP.md"],
        cwd=root, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return [
            "roadmap drift: generated/ROADMAP.md is absent and the "
            "sync/generated-artifacts branch is not fetched - run: "
            "git fetch origin sync/generated-artifacts"
        ]
    roadmap.parent.mkdir(exist_ok=True)
    roadmap.write_text(result.stdout)
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--source",
        required=True,
        help="botforge-services source root (src/botforge)",
    )
    parser.add_argument(
        "--config",
        required=True,
        help="botforge-services config root (config)",
    )
    parser.add_argument(
        "--scripts-dir",
        default="scripts",
        help="directory holding validate_docs.py and sync_roadmap.py",
    )
    args = parser.parse_args()

    root = repo_root()
    scripts_dir = root / args.scripts_dir
    checks: list[list[str]] = [ensure_generated_artifacts(root)]
    checks.append(
        run_check(
            "docs validation",
            [
                "python3",
                str(scripts_dir / "validate_docs.py"),
                "--check",
                "--source",
                args.source,
                "--config",
                args.config,
            ],
        )
    )
    checks.append(
        run_check(
            "roadmap drift",
            ["python3", str(scripts_dir / "sync_roadmap.py"), "--check"],
        )
    )

    deps_out = Path("/tmp") / "botforge-dependencies-check.md"
    deps_result = subprocess.run(
        [
            "python3",
            str(scripts_dir / "sync_dependencies.py"),
            "--out",
            str(deps_out),
        ],
        capture_output=True,
        text=True,
    )
    dep_path = root / "generated" / "DEPENDENCIES.md"
    if dep_path.exists():
        committed = dep_path.read_text()
    else:
        # The generated dependency graph lives on the sync/generated-artifacts
        # branch (main carries no generated files); read it from there.
        committed = subprocess.run(
            ["git", "show", "origin/sync/generated-artifacts:generated/DEPENDENCIES.md"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout
    generated = deps_out.read_text() if deps_out.exists() else ""
    deps_out.unlink(missing_ok=True)
    if deps_result.returncode == 0 and generated == committed:
        print("PASS  dependency-graph drift")
    else:
        print("FAIL  dependency-graph drift")
        checks.append(
            ["dependency-graph: generated/DEPENDENCIES.md is out of date"
             " — trigger the sync-generated workflow (single writer)"]
        )

    failures = [line for group in checks for line in group]
    if failures:
        print("\nThe following need fixing before ending the session:")
        for line in failures:
            print(f"- {line}")
        return 1
    print("\nAll session checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
