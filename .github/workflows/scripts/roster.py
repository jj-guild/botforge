#!/usr/bin/env python3
"""Canonical CONTRIBUTORS.md roster parser and authority checks.

One module, used everywhere a decision depends on who may do what:
- CLI (this file): `roster.py check <login> <capability> [--pr-author <login>]`
- Library: `from roster import Roster` (scripts and workflows).

The authority matrix lives in CONTRIBUTORS.md (the doc is the truth);
this module encodes the keyword->role rules from that matrix. Changing
the rules is a roster PR: edit the matrix, mirror the change here, and
the maintainers review both in the same PR.

Capabilities (from the authority matrix):
  env-reset    -> ops (any env) or the env's own owner (self reset only)
  deploy       -> requestor rostered (vibe or better); never prod-like
  env-control  -> ops (any env) or dev (test only)
  env-logs    -> ops (any env) or dev (test only)
  db-dump     -> ops
  release      -> dev or platform
  rollback     -> ops
  sync-teams   -> platform
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field

ROLE_LEVELS = {"none": 0, "vibe": 1, "mod": 2, "dev": 3, "platform": 3, "ops": 3}

CAPABILITY_RULES: dict[str, dict] = {
    "deploy": {"min": "vibe", "deny_envs_prod": True, "help": "deploy a PR to a non-prod env",
               "usage": "/deploy [env] — build the PR image and pin it on deploy/<env> (default test). Never prod-like envs."},
    "env-control": {"roles": ["ops", "dev", "mod", "vibe"], "own_env_roles": ["vibe", "mod", "dev", "ops"], "shared_env_roles": ["dev", "ops"], "help": "start/stop/restart/status an env",
                    "usage": "/restart [env] — restart the env stack in place. Also /start /stop /status via env-control."},
    "env-logs": {"roles": ["ops", "dev", "mod", "vibe"], "own_env_roles": ["vibe", "mod", "dev", "ops"], "shared_env_roles": ["dev", "ops"], "help": "read an env's logs",
                 "usage": "/logs [env] [--service S] [--since 30m] [--from iso] [--to iso] [--tail N] — collect logs and post them back (read-only)."},
    "db-dump": {"roles": ["ops"], "help": "dump an env's databases",
                "usage": "/dump-db [env] — mongodump + Redis snapshot, hosting archive + private artifact."},
    "release": {"roles": ["dev", "platform"], "help": "tag and release",
                "usage": "/release — cut a release from main (auto-bumped from Conventional Commits, never hand-picked)."},
    "rollback": {"roles": ["ops"], "help": "revert a pin",
                 "usage": "/rollback <env> — revert the last pinned image on deploy/<env> (previous known-good redeployed)."},
    "env-reset": {"own_env_only_roles": ["vibe", "mod", "dev", "platform"], "deny_envs_prod": True,
                  "help": "wipe an env's data and reseed",
                  "usage": "/reset-env [env] — wipe the env's data volumes and reseed from the workflow datasets. Self env only, unless ops. Never prod."},
    "sync-teams": {"roles": ["platform"], "help": "run the roster sync",
                   "usage": "/sync-teams — re-sync GitHub teams/permissions from CONTRIBUTORS.md (the doc is the source of truth)."},
    "console-ops": {"roles": ["ops", "dev", "mod", "vibe"], "own_env_roles": ["vibe", "mod", "dev", "ops"], "shared_env_roles": ["dev", "ops"], "deny_envs_prod": True,
                    "help": "run the console actions on an env's test guilds (GitHub-side /console)",
                    "usage": "/console <env> <clean-managed|nuke|reset-data|install> <guild_id|all> — same actions and gates as the Discord /console, headless. nuke needs --confirm NUKE. Never prod."},
}


@dataclass
class Person:
    login: str
    alias: str = ""
    cla: str = "none"
    teams: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)
    owns: str = ""
    agent_scope: str = ""


MEMBER_ROW = re.compile(r"^\|\s*@([A-Za-z0-9-]+)\s*\|")


def parse_roster(path: str) -> dict[str, Person]:
    people: dict[str, Person] = {}
    section = ""
    with open(path) as fh:
        for line in fh:
            if line.startswith("## "):
                section = line[3:].strip()
                continue
            if section != "Contributors" or not MEMBER_ROW.match(line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # columns: login | alias | since | cla | github-teams | roles | owns | agent-scope
            if len(cells) < 8 or cells[0].lstrip("@") == "Login":
                continue
            login = cells[0].lstrip("@")
            people[login] = Person(
                login=login,
                alias=cells[1],
                cla=cells[3],
                teams=[t.strip().strip("`") for t in cells[4].split(",") if t.strip()],
                roles=[r.strip() for r in re.split(r",(?![^(]*\))", cells[5]) if r.strip()],
                owns=cells[6],
                agent_scope=cells[7],
            )
    return people


def check(person: Person | None, capability: str, env: str = "", pr_author: Person | None = None) -> tuple[bool, str]:
    """Return (allowed, reason). Mirrors the authority matrix exactly."""
    rule = CAPABILITY_RULES.get(capability)
    if not rule:
        return False, f"unknown capability: {capability}"
    if person is None:
        return False, "requestor has no roster entry (CONTRIBUTORS.md) — ask a maintainer for onboarding"
    roles = {re.split(r"[(,]", r)[0].strip() for r in person.roles}
    roles = {r for r in roles if r and r != ")"}

    if "own_env_roles" in rule:
        # Ownership tiers (authority matrix): personal env (env == roster
        # alias) at vibe+, shared envs (test) at dev+, ops+ anywhere.
        if rule.get("deny_envs_prod") and env == "prod":
            return False, f"'{capability}' is never allowed on prod (per the authority matrix)"
        if env == "prod":
            if not roles & {"ops", "platform"}:
                return False, f"'{capability}' on prod requires ops (the authority matrix)"
        elif env and person.alias and env == person.alias.lower():
            if not any(ROLE_LEVELS.get(r, 0) >= ROLE_LEVELS["vibe"] for r in roles):
                return False, f"{person.alias or person.login} roles {sorted(roles) or ['none']} do not grant '{capability}' (needs vibe+ on a personal env, per the authority matrix)"
        elif env in ("test",) or not env:
            if not roles & set(rule["shared_env_roles"]) and not any(ROLE_LEVELS.get(r, 0) >= ROLE_LEVELS["ops"] for r in roles):
                return False, f"{person.alias or person.login} roles {sorted(roles) or ['none']} do not grant '{capability}' on shared envs (needs one of {rule['shared_env_roles']}+, per the authority matrix)"
        else:
            # someone else's personal env: ops+ only
            if not any(ROLE_LEVELS.get(r, 0) >= ROLE_LEVELS["ops"] for r in roles):
                return False, f"'{capability}' on another contributor's env ({env}) requires ops+ (the authority matrix)"
    elif "roles" in rule:
        if not roles & set(rule["roles"]):
            return False, f"{person.alias or person.login} roles {sorted(roles) or ['none']} do not grant '{capability}' (needs one of {rule['roles']}, per the authority matrix)"
        if env == "prod" and "test_only_roles" in rule:
            if roles & set(rule["test_only_roles"]) and not roles & (set(rule["roles"]) - set(rule["test_only_roles"])):
                return False, f"'{capability}' on prod requires ops (the authority matrix)"
    elif "own_env_only_roles" in rule:
        # Destructive: ops may reset any env; anyone else (vibe/mod/dev/platform)
        # may only reset their OWN environment (their roster alias).
        if rule.get("deny_envs_prod") and env == "prod":
            return False, f"'{capability}' is never allowed on prod (per the authority matrix)"
        if "ops" in roles:
            pass
        elif not roles & set(rule["own_env_only_roles"]):
            return False, f"{person.alias or person.login} roles {sorted(roles) or ['none']} do not grant '{capability}' (needs ops for any env, or one of {rule['own_env_only_roles']} on their own env, per the authority matrix)"
        elif env and person.alias and env != person.alias.lower():
            return False, f"'{capability}' on {env} is restricted to that environment's owner or ops ({person.alias or person.login} owns {person.alias.lower() or 'no env'}, per the authority matrix)"
    elif "min" in rule:
        granted = any(ROLE_LEVELS.get(r, 0) >= ROLE_LEVELS[rule["min"]] for r in roles)
        if not granted:
            return False, f"{person.alias or person.login} roles {sorted(roles) or ['none']} do not grant '{capability}' (needs {rule['min']}+, per the authority matrix)"

    # CLA is a precondition for any mutating action
    if not person.cla.lower().startswith("accepted"):
        return False, f"{person.alias or person.login} has no accepted CLA on record (roster says: {person.cla})"

    # Agent-mediated actions: the PR author's agent-scope must cover it too
    if pr_author is not None:
        scope = pr_author.agent_scope.lower()
        if capability in ("deploy", "rollback", "env-control", "release", "sync-teams"):
            if "fully on their behalf" not in scope and capability in ("deploy", "env-control", "env-reset") and "deploy" not in scope and "drive" not in scope:
                return False, f"PR author {pr_author.alias or pr_author.login}'s agent-scope does not cover '{capability}': \"{pr_author.agent_scope}\""
    return True, f"{person.alias or person.login} ({', '.join(sorted(roles)) or 'no roles'}) may '{capability}'{f' on {env}' if env else ''}"


def _normalized_roles(person: Person | None) -> set[str]:
    """Roles stripped of parenthetical qualifiers, as check() sees them."""
    roles = {re.split(r"[(,]", r)[0].strip() for r in (person.roles if person else [])}
    return {r for r in roles if r and r != ")"}


def _may_use(person: Person | None, capability: str) -> bool:
    """Role-only view of check() for /help listings (no env/CLA/scope context)."""
    rule = CAPABILITY_RULES.get(capability)
    if not rule or person is None:
        return False
    roles = _normalized_roles(person)
    if "roles" in rule:
        return bool(roles & set(rule["roles"]))
    if "own_env_only_roles" in rule:
        return "ops" in roles or bool(roles & set(rule["own_env_only_roles"]))
    return any(ROLE_LEVELS.get(r, 0) >= ROLE_LEVELS[rule["min"]] for r in roles)


def list_capabilities(person: Person | None) -> list[dict]:
    """The /help listing: one entry per capability the requestor may use."""
    return [
        {"capability": cap, "help": rule["help"], "usage": rule["usage"]}
        for cap, rule in CAPABILITY_RULES.items()
        if _may_use(person, cap)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", default="CONTRIBUTORS.md")
    parser.add_argument("login", nargs="?")
    parser.add_argument("capability", nargs="?", choices=list(CAPABILITY_RULES))
    parser.add_argument("--env", default="")
    parser.add_argument("--pr-author", default="")
    parser.add_argument("--list", action="store_true",
                        help="list the capabilities the login may use")
    parser.add_argument("--usage", default="",
                        help="print the detailed usage line of this capability")
    args = parser.parse_args()
    roster = parse_roster(args.roster)
    if args.list:
        if not args.login:
            print("::error::--list needs a login", file=sys.stderr)
            return 1
        print(json.dumps({"alias": roster[args.login].alias if args.login in roster else args.login,
                          "capabilities": list_capabilities(roster.get(args.login))}))
        return 0
    if args.usage:
        rule = CAPABILITY_RULES.get(args.usage)
        if not rule:
            print(f"unknown capability: {args.usage}", file=sys.stderr)
            return 1
        print(rule["usage"])
        return 0
    if not args.login or not args.capability:
        parser.error("login and capability are required (or use --list / --usage)")
    ok, reason = check(
        roster.get(args.login),
        args.capability,
        env=args.env,
        pr_author=roster.get(args.pr_author) if args.pr_author else None,
    )
    print(json.dumps({"allowed": ok, "reason": reason, "alias": roster[args.login].alias if args.login in roster else args.login}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
