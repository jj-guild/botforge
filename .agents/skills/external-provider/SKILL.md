---
name: external-provider
description: Integrate any external API/provider into a bot platform — config gating that matches the wire, real-wire integration tests, id mapping between URL ids and API ids, and reading logs before guessing. Generic and reusable for any third-party service (stats APIs, lobby websockets, game data, wikis).
---

# External provider integration

## Config gates must match the wire

- Before gating on a config value (API key, endpoint URI, base URL), verify the value can actually be absent **and** that the service genuinely requires it. A gate that rejects every valid input while the real service answers anyone is the worst failure mode — it is silent.
- An env var that **exists but is empty** defeats `${VAR:-default}` shell/compose defaults — the default never applies. Code must fall back itself (`value or DEFAULT`), always.
- Declared capabilities are the contract: keep them static and honest. Degrade the *response* (return None) when a key is missing — never lie in the capability declaration.

## Test the real wire shape

- A test suite that mocks the seam passes while prod fails. The integration test must run the real server/client, the real adapter, the real reply payloads — and assert on the **endpoint actually called** (e.g. the personal-stat call, never the raw leaderboard HTTP route).

## Id mapping

- The id visible in a pasted URL is not necessarily the id the API wants: an external service may key on a different identifier (a second id resolved through the service's own endpoint). Resolve any pasted id/URL through the provider's resolution path, **store the id the API wants**, and build links with the path that matches that id (the plain profile path expects the URL id, not the API id).

## Logs before hypotheses

- Log access (`/logs`-style, per environment) answers in one grep what an afternoon of hypotheses cannot. Read the logs first, always.
