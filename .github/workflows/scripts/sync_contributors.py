#!/usr/bin/env python3
"""Synchronize the org's teams and memberships with CONTRIBUTORS.md.

The roster (CONTRIBUTORS.md, botforge repo) is the single source of truth
for org teams, team memberships and team repo grants. This script makes
GitHub match the doc:

- declared contributor missing from a declared team  -> added
- GitHub membership absent from the doc               -> removed (revoked)
- declared team missing on GitHub                    -> created (+ grants)
- undeclared team / unrostered org member             -> flagged (never deleted)
- repo grants (role per repo)                         -> ensured

Every correction is printed; anything removed or flagged makes the run
exit non-zero (the workflow reports to the maintainers). Use --check to
only report (no mutation).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field

GITHUB_API = "https://api.github.com"
ORG = "jj-guild"


@dataclass
class Team:
    slug: str
    parent: str | None
    repos: dict[str, str] = field(default_factory=dict)
    purpose: str = ""


@dataclass
class Contributor:
    login: str
    teams: list[str] = field(default_factory=list)


class GitHub:
    """Thin GitHub REST client (stdlib only)."""

    def __init__(self, token: str) -> None:
        self.token = token

    def request(
        self,
        method: str,
        path: str,
        body: dict | None = None,
    ) -> tuple[int, object]:
        req = urllib.request.Request(
            f"{GITHUB_API}{path}",
            data=json.dumps(body).encode() if body else None,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "botforge-sync-contributors",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode() or "null"
                return resp.status, json.loads(raw) if raw else None
        except urllib.error.HTTPError as err:
            return err.code, None

    # -- reads ---------------------------------------------------------

    def list_teams(self) -> dict[str, dict]:
        status, data = self.request("GET", f"/orgs/{ORG}/teams?per_page=100")
        if status != 200 or not data:
            sys.exit(f"cannot list teams: HTTP {status}")
        return {t["slug"]: t for t in data}

    def team_members(self, slug: str) -> set[str]:
        status, data = self.request("GET", f"/orgs/{ORG}/teams/{slug}/members?per_page=100")
        if status != 200 or not data:
            return set()
        return {m["login"] for m in data}

    def team_repos(self, slug: str) -> dict[str, str]:
        status, data = self.request("GET", f"/orgs/{ORG}/teams/{slug}/repos?per_page=100")
        if status != 200 or not data:
            return {}
        roles: dict[str, str] = {}
        for r in data:
            role = r.get("role_name")
            if not role:
                role = "write" if r.get("permissions", {}).get("push") else "read"
            roles[r["name"]] = role
        return roles

    def org_members(self) -> set[str]:
        status, data = self.request("GET", f"/orgs/{ORG}/members?per_page=100")
        if status != 200 or not data:
            return set()
        return {m["login"] for m in data}

    # -- writes --------------------------------------------------------

    def add_member(self, slug: str, login: str) -> str:
        status, _ = self.request(
            "PUT",
            f"/orgs/{ORG}/teams/{slug}/memberships/{login}",
            body={"role": "member"},
        )
        note = "" if status in (200, 204) else f" (HTTP {status})"
        return f"ADD {login} -> {slug}{note}"

    def remove_member(self, slug: str, login: str) -> str:
        status, _ = self.request(
            "DELETE",
            f"/orgs/{ORG}/teams/{slug}/memberships/{login}",
        )
        note = "" if status == 204 else f" (HTTP {status})"
        return f"REMOVE {login} from {slug}{note}"

    def set_repo_grant(self, slug: str, repo: str, role: str) -> str:
        status, _ = self.request(
            "PUT",
            f"/orgs/{ORG}/teams/{slug}/repos/{ORG}/{repo}",
            body={"permission": role},
        )
        note = "" if status == 204 else f" (HTTP {status})"
        return f"GRANT {slug}: {repo} -> {role}{note}"

    def create_team(self, team: Team) -> str:
        status, _ = self.request(
            "POST",
            f"/orgs/{ORG}/teams",
            body={"name": team.slug, "privacy": "closed"},
        )
        note = "" if status == 201 else f" (HTTP {status})"
        return f"CREATE team {team.slug}{note}"


# -- roster parsing ------------------------------------------------------

TEAM_ROW = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|")
MEMBER_ROW = re.compile(r"^\|\s*@([A-Za-z0-9-]+)\s*\|")
GRANT = re.compile(r"([a-z-]+):\s*`(read|write|maintain|admin|triage)`")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def parse_roster(path: str) -> tuple[dict[str, Team], dict[str, Contributor]]:
    teams: dict[str, Team] = {}
    contributors: dict[str, Contributor] = {}
    section = ""
    with open(path) as fh:
        for line in fh:
            if line.startswith("## "):
                section = line[3:].strip()
                continue
            if section == "Teams" and TEAM_ROW.match(line):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 4 or cells[0].strip("`") == "Team slug":
                    continue
                if EMAIL.search(line):
                    sys.exit(
                        f"CONTRIBUTORS.md team row contains an email address "
                        f"({line.strip()!r}) — personal emails are forbidden "
                        f"in the roster (public repo; privacy incident "
                        f"prevention). Remove it."
                    )
                slug = cells[0].strip("`")
                parent = cells[1].strip("` ").strip("—-")
                parent = parent or None
                repos = {m.group(1): m.group(2) for m in GRANT.finditer(cells[2])}
                teams[slug] = Team(slug=slug, parent=parent, repos=repos, purpose=cells[3])
            elif section == "Contributors" and MEMBER_ROW.match(line):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 6 or cells[0].lstrip("@") == "Login":
                    continue
                if EMAIL.search(line):
                    sys.exit(
                        f"CONTRIBUTORS.md contributor row contains an email "
                        f"address ({line.strip()!r}) — personal emails are "
                        f"forbidden in the roster (public repo; privacy "
                        f"incident prevention). Remove it."
                    )
                login = cells[0].lstrip("@")
                # columns: login | alias | since | cla | github-teams | ...
                declared = [t.strip().strip("`") for t in cells[4].split(",")]
                contributors[login] = Contributor(login=login, teams=[t for t in declared if t])
    return teams, contributors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report only, no mutation")
    parser.add_argument("--roster", default="CONTRIBUTORS.md")
    args = parser.parse_args()

    token = os.environ.get("CONTRIBUTORS_SYNC_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("CONTRIBUTORS_SYNC_TOKEN (or GITHUB_TOKEN) is required")

    teams, contributors = parse_roster(args.roster)
    gh = GitHub(token)

    corrections: list[str] = []
    flags: list[str] = []

    live_teams = gh.list_teams()
    live_members = gh.org_members()

    for slug in live_teams:
        if slug not in teams:
            flags.append(f"undeclared team on GitHub: {slug}")

    for team in teams.values():
        if team.slug not in live_teams:
            if args.check:
                flags.append(f"declared team missing on GitHub: {team.slug}")
            else:
                corrections.append(gh.create_team(team))
            members: set[str] = set()
        else:
            members = gh.team_members(team.slug)
            if team.parent and team.parent not in live_teams:
                flags.append(f"declared parent team missing on GitHub: {team.parent}")
        declared = {c.login for c in contributors.values() if team.slug in c.teams}
        for login in sorted(declared - members):
            if args.check:
                flags.append(f"missing membership: {login} not in {team.slug}")
            else:
                corrections.append(gh.add_member(team.slug, login))
        for login in sorted(members - declared):
            if args.check:
                flags.append(f"over-granted membership: {login} in {team.slug} but not declared")
            else:
                corrections.append(gh.remove_member(team.slug, login))
        live_repos = gh.team_repos(team.slug)
        for repo, role in sorted(team.repos.items()):
            if live_repos.get(repo) != role:
                if args.check:
                    flags.append(
                        f"repo grant drift: {team.slug} on {repo}: "
                        f"{live_repos.get(repo)} != {role}"
                    )
                else:
                    corrections.append(gh.set_repo_grant(team.slug, repo, role))

    rostered = set(contributors)
    for login in sorted(live_members - rostered):
        flags.append(f"org member absent from the roster: {login}")

    print(f"Roster: {len(contributors)} contributors, {len(teams)} teams")
    for c in corrections:
        print(f"  corrected: {c}")
    for f in sorted(flags):
        print(f"  FLAG: {f}")
    if flags:
        print(f"\n{len(flags)} flag(s) — maintainers must resolve; see the tracking issue.")
        return 1
    print("Doc and GitHub are in sync." if not corrections else "\nCorrections applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
