# Template — Mod test scenarios

Copy this file with the mod's doc set (`docs/MODS/<mod-name>/`) and list
the scenarios that validate/secure the implementation. **Every scenario
has exactly one automated test**, implemented by the agent in
`modules/mods/<mod>/tests/test_scenarios.py` (botforge-services), run by
CI (`pytest tests modules/mods/*/tests/test_scenarios.py`), and
cross-checked by the botforge docs validation (`validate_docs.py` fails
when a documented scenario has no test).

## Scenario format

```markdown
### SC-<MOD>-001 — short title

- **Given** …
- **When** …
- **Then** … (the acceptance criterion the test asserts)

Implemented by `test_SC_<MOD>_001_*` in `test_scenarios.py`.
```

Rules:

- one id per scenario, `SC-<MOD>-NNN` (MOD = the mod id, uppercase);
- scenarios may be complex (multi-step flows, several actors) — the test
  drives the same steps against fakes/mocks;
- the test's docstring carries the id, so doc and code stay paired;
- the agent writes the missing tests **in the same PR** as the doc
  change — a scenario without its test is a drift the CI check rejects.

## Scenarios

### SC-MOD-001 — example

- **Given** …
- **When** …
- **Then** …
