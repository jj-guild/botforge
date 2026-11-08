#!/usr/bin/env python3
"""Validate BotForge documentation completeness.

Checks:
- every mod declared in botforge-services config/mods/ has a doc directory
  in docs/MODS/ with README.md, RULES.md and ENVIRONMENT.md
- every Python module, public class and public function in
  botforge-services has a docstring (skipped when the source tree is absent)
- every Mermaid block in docs/ is syntactically plausible
  (declared diagram type, balanced subgraph/end, non-empty)

Exit code is non-zero when any check fails. Use --check for CI mode;
it behaves the same but prints a machine-friendly summary line.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

MERMAID_TYPES = (
    "flowchart",
    "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "journey",
    "gantt",
    "mindmap",
    "timeline",
    "gitGraph",
)

REQUIRED_MOD_FILES = ("README.md", "RULES.md", "ENVIRONMENT.md")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def check_mods_docs(docs_root: Path, config_root: Path | None) -> list[str]:
    """Verify every mod has complete documentation in docs/MODS/."""
    problems: list[str] = []
    mods_dir = docs_root / "MODS"
    if not mods_dir.is_dir():
        return [f"missing directory: {mods_dir}"]

    documented = {
        d.name
        for d in mods_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }

    declared: set[str] = set()
    if config_root and (config_root / "mods").is_dir():
        declared = {
            p.stem
            for p in (config_root / "mods").glob("*.y*ml")
            if not p.stem.startswith("_")
        }

    for mod in sorted(documented | declared):
        mod_dir = mods_dir / mod
        if not mod_dir.is_dir():
            problems.append(f"mod '{mod}' is declared but has no directory in docs/MODS/")
            continue
        for required in REQUIRED_MOD_FILES:
            if not (mod_dir / required).is_file():
                problems.append(
                    f"mod '{mod}' is missing {required} in docs/MODS/{mod}/"
                )

    return problems


def iter_python_files(source_root: Path):
    for path in sorted(source_root.rglob("*.py")):
        if any(part.startswith(".") for part in path.parts):
            continue
        if "rpc_generated" in path.parts:
            continue  # generated gRPC stubs (ADR-0020): never hand-documented
        yield path


def check_docstrings(source_root: Path | None) -> list[str]:
    """Verify public Python objects have docstrings."""
    if source_root is None:
        return []

    problems: list[str] = []
    for path in iter_python_files(source_root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            problems.append(f"{path}: syntax error: {exc}")
            continue

        if not ast.get_docstring(tree):
            problems.append(f"{path}: missing module docstring")

        for node in ast.walk(tree):
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_"):
                continue
            if not ast.get_docstring(node):
                problems.append(f"{path}: {node.name}() is missing a docstring")
    return problems


def check_mermaid(docs_root: Path) -> list[str]:
    """Run lightweight syntax checks on Mermaid blocks in Markdown files."""
    problems: list[str] = []
    block_re = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)

    for md in sorted(docs_root.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for index, match in enumerate(block_re.finditer(text), start=1):
            block = match.group(1)
            label = f"{md.relative_to(repo_root())} (block {index})"
            if not block.strip():
                problems.append(f"{label}: empty Mermaid block")
                continue
            first_line = block.strip().splitlines()[0].strip()
            if not any(first_line.startswith(t) for t in MERMAID_TYPES):
                problems.append(
                    f"{label}: missing diagram type "
                    f"(first line must start with one of {', '.join(MERMAID_TYPES)})"
                )
            if block.count("subgraph") != block.count("\nend") + block.count(
                "\n\tend"
            ):
                if not re.search(r"\bend\b", block):
                    problems.append(f"{label}: unbalanced subgraph/end")
                elif block.count("subgraph") != len(re.findall(r"^\s*end\s*$", block, re.MULTILINE)):
                    problems.append(f"{label}: unbalanced subgraph/end")
            for cls in re.findall(r"^\s*class\s+([^\n]+)$", block, re.MULTILINE):
                for key in cls.split(","):
                    if key.strip() != key or not key.strip():
                        problems.append(
                            f"{label}: invalid class statement "
                            f"(`class {cls.strip()}`): node ids must be "
                            f"comma-separated without spaces"
                        )
                        break
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="CI mode: print a summary line and exit non-zero on any failure",
    )
    parser.add_argument(
        "--docs",
        type=Path,
        default=repo_root() / "docs",
        help="Docs directory to validate (default: <repo>/docs)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=repo_root().parent / "botforge-services" / "src" / "botforge",
        help="Python source root for docstring checks "
        "(default: ../botforge-services/src/botforge)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=repo_root().parent / "botforge-services" / "config",
        help="botforge-services config root for mod declarations "
        "(default: ../botforge-services/config)",
    )
    args = parser.parse_args()

    docs_root = args.docs.resolve()
    if not docs_root.is_dir():
        print(f"error: docs directory not found: {docs_root}", file=sys.stderr)
        return 1

    source_root = args.source if args.source.is_dir() else None
    config_root = args.config if args.config.is_dir() else None

    if source_root is None:
        print(
            "error: botforge-services source not found — the docstring check "
            "is mandatory; refusing to validate partially",
            file=sys.stderr,
        )
        return 1
    if config_root is None:
        print(
            "error: botforge-services config not found — mod-declaration "
            "validation is mandatory; refusing to validate partially",
            file=sys.stderr,
        )
        return 1

    problems = (
        check_mods_docs(docs_root, config_root)
        + check_docstrings(source_root)
        + check_mermaid(docs_root)
    )

    for problem in problems:
        print(f"FAIL: {problem}")

    if args.check:
        status = "PASS" if not problems else f"FAIL ({len(problems)} problems)"
        print(f"validate_docs: {status}")
    else:
        print(f"{len(problems)} problem(s) found")

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
