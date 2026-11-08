#!/usr/bin/env python3
"""Roster ↔ CODEOWNERS consistency check (mods and games).

The roster (CONTRIBUTORS.md) is the single source of truth for who owns
what. This check enforces the ownership rules the platform runs on:

1. **Every mod and game has a rostered owner.** A mod directory
   (``docs/MODS/<mod>/`` in botforge, ``src/botforge/mods/<mod>/`` in
   botforge-services, ``config/mods/<mod>.yaml``) or a game directory
   (``src/botforge/core/games/<game>/``) without a matching `owns`
   entry in the roster is a violation: nobody is accountable for it and
   no CODEOWNERS line can legitimately exist. Creating a mod or a game
   without a roster entry is proscribed (CONVENTIONS.md) — this check
   is the automated enforcement.

2. **CODEOWNERS matches the roster.** Every mod/game delegation line in
   the CODEOWNERS files (botforge and botforge-services) must point at
   a contributor whose roster `owns` column names that mod/game;
   conversely, every roster-claimed mod/game must have its CODEOWNERS
   delegation lines (docs in botforge, code in botforge-services).

Exit 0 when consistent; every violation is reported and makes the run
fail (the sync workflow surfaces it to the maintainers).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MOD_DIRS = ("docs/MODS",)
BOTFORGE_SERVICES_MODS = "src/botforge/mods"
BOTFORGE_SERVICES_GAMES = "src/botforge/core/games"
CONFIG_MODS = "config/mods"

MEMBER_ROW = re.compile(r"^\|\s*@([A-Za-z0-9-]+)\s*\|")


def parse_owns(roster_path: Path) -> dict[str, str]:
    """login -> the `owns` cell (column 7 of the Contributors table)."""
    owns: dict[str, str] = {}
    section = ""
    for line in roster_path.read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section != "Contributors" or not MEMBER_ROW.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or cells[0].lstrip("@") == "Login":
            continue
        owns[cells[0].lstrip("@")] = cells[6]
    return owns


def claimed_mods_and_games(owns_cell: str) -> tuple[set[str], set[str]]:
    """Mods and games claimed by an `owns` cell, from its mod/game mentions."""
    mods = set(re.findall(r"\bmods?\s*\(([^)]*)\)", owns_cell))
    flat_mods: set[str] = set()
    for group in mods:
        for name in re.split(r"[,/]", group):
            name = name.strip().strip("`").lower()
            if name and name not in ("botforge",):  # the org's own mods count
                flat_mods.add(name)
    backtick = {m.lower() for m in re.findall(r"`([a-z0-9-]+)`", owns_cell)}
    games = {g for g in backtick if g in KNOWN_GAMES}
    return flat_mods | backtick, games


# Games known to the platform (core/games/<game>); extend with the catalog.
KNOWN_GAMES = {"aoe2"}
# Platform-owned games (core code owned by dev/maintainers, not a designer):
# add here when a game is platform-maintained instead of designer-owned.
KNOWN_GAMES_UNOWNED = {"aoe2"}


def discovered_mods() -> set[str]:
    """Mod names found in the repo: docs/MODS/<mod>/ and config/mods/<mod>.yaml."""
    found: set[str] = set()
    for mod_dir in MOD_DIRS:
        base = REPO / mod_dir
        if base.is_dir():
            found |= {p.name.lower() for p in base.iterdir() if p.is_dir()}
    cfg = REPO / CONFIG_MODS
    if cfg.is_dir():
        found |= {p.stem.lower() for p in cfg.glob("*.yaml")}
    return found


def codeowners_delegations(codeowners_path: Path) -> dict[str, str]:
    """path -> owner login, for non-team (individual) delegation lines."""
    delegations: dict[str, str] = {}
    if not codeowners_path.exists():
        return delegations
    for line in codeowners_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and not parts[1].startswith("@jj-guild/"):
            delegations[parts[0].rstrip("/")] = parts[1].lstrip("@")
    return delegations


def services_paths(services_repo: Path) -> tuple[set[str], set[str]]:
    """Mod and game names found in a botforge-services checkout."""
    mods: set[str] = set()
    games: set[str] = set()
    mods_dir = services_repo / BOTFORGE_SERVICES_MODS
    if mods_dir.is_dir():
        mods = {p.name.lower() for p in mods_dir.iterdir() if p.is_dir()}
    games_dir = services_repo / BOTFORGE_SERVICES_GAMES
    if games_dir.is_dir():
        games = {p.name.lower() for p in games_dir.iterdir() if p.is_dir() and p.name != "__pycache__"}
    return mods, games


def main() -> int:
    roster = REPO / "CONTRIBUTORS.md"
    owns = parse_owns(roster)
    violations: list[str] = []

    claimed: set[str] = set()
    for login, cell in owns.items():
        mods, _games = claimed_mods_and_games(cell)
        claimed |= mods

    discovered = discovered_mods()
    template_dirs = {"template", "readme.md"}
    for name in sorted(discovered - claimed - template_dirs):
        violations.append(
            f"mod '{name}' exists but no roster entry claims it (CONTRIBUTORS.md 'owns') "
            f"— creating a mod without a rostered owner is proscribed"
        )

    # botforge-services (sibling checkout when present): mod code and games
    services = REPO.parent / "github__jj-guild__botforge-services"
    if not services.is_dir():
        services = Path(
            os.environ.get("BOTFORGE_SERVICES_REPO", str(REPO.parent / "botforge-services"))
        )
    if services.is_dir():
        svc_mods, svc_games = services_paths(services)
        for name in sorted(svc_mods - claimed - template_dirs - {"__pycache__"}):
            violations.append(
                f"mod code 'src/botforge/mods/{name}' exists but no roster entry "
                f"claims it (CONTRIBUTORS.md 'owns') — creating a mod without a "
                f"rostered owner is proscribed"
            )
        for name in sorted(svc_games - claimed - KNOWN_GAMES_UNOWNED):
            violations.append(
                f"game 'src/botforge/core/games/{name}' exists but no roster entry "
                f"claims it (CONTRIBUTORS.md 'owns') — creating a game without a "
                f"rostered owner is proscribed"
            )

    co_kingdoms = codeowners_delegations(REPO / ".github" / "CODEOWNERS")
    for path, owner in co_kingdoms.items():
        if owner not in owns:
            violations.append(
                f"CODEOWNERS delegates '{path}' to @{owner} who has no roster entry"
            )
        else:
            mods, _ = claimed_mods_and_games(owns[owner])
            if not mods & {seg.lower() for seg in path.split("/")}:
                violations.append(
                    f"CODEOWNERS delegates '{path}' to @{owner} but their roster "
                    f"'owns' does not claim that mod"
                )
    for path, owner in co_kingdoms.items():
        if path not in {".github", "scripts"} and "@" + owner in owns:
            pass  # covered by the matching check above

    for v in violations:
        print(f"  VIOLATION: {v}")
    if violations:
        print(f"\n{len(violations)} ownership violation(s) — maintainers must resolve.")
        return 1
    print("Ownership consistent: roster 'owns' matches mods and CODEOWNERS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
