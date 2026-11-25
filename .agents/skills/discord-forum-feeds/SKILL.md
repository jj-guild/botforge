---
name: discord-forum-feeds
description: A feed salon is a FORUM, one post per KNOWN entity (player, mod, pool...), cards batched 10 per message, lifecycle pokes (join/leave, bind/unbind) reconcile the posts instantly. Apply to every salon that surfaces per-entity activity.
---

# Discord forum feeds - one post per entity, batched, reconciled

**The rule (owner 2026-11-25)**: a feed salon that surfaces an
ENTITY's activity (a player's matches, a mod's builds...) is a
**forum channel**, not a text channel:

- **one post (thread) per KNOWN entity** - the member reads HIS
  entity's history in one place; an event shared by several entities
  lands in EACH one's post (the duplicate is assumed, never deduped
  ACROSS posts);
- **the registry is per-post** (`{guild}:livefeed:<feed>:posts` in the
  `channels` collection): `{entity_id: {thread_id, name, refs[], messages{ref: mid}}}` - the refs
  prevent a double post within a post, the message ids drive the
  reconcile;
- **grouped sends**: cards fold into ONE `LayoutView` per message,
  up to **10 cards per message**; a batch Discord refuses (the
  40-component cap) HALVES until it fits - one card per message is the
  floor, never a failure;
- **the lifecycle pokes the reconcile**: member join/leave and
  bind/unbind events run `instant_sweep(bot, guild_id)` NOW - the
  5-minute sweep is the SAFETY NET, never the fast path (the events
  queue through the service's `events` seam: emit on mutation, the
  discord side binds late);
- **the channel resolves cache-first, fetch-second** - a channel
  created after the boot never rides the client's cache, `fetch_channel`
  is the fallback (a fresh salon silently starving is the classic
  bug);
- **observability**: every reconcile decision logs its verb (`post
  created/deleted`, `repaired`, `reconcile: N dead dropped`) - a
  silent skip is a bug.

## Procedure

1. **Declare the channel** `kind: forum` in `config/views.yaml`.
2. **Own a posts registry** doc per feed: `{guild}:livefeed:<feed>:posts`.
3. **Reconcile posts on every sweep**: `_ensure_player_posts`
   creates the missing threads, deletes the orphans (entity left or
   unbound), NEVER blindly resets - reconcile against the live
   channel (list the messages, drop the dead refs, repost the
   missing).
4. **Group the sends through** `_send_cards_grouped` (10 per
   message, halving fallback).
5. **Bind the pokes**: gateway listeners (`on_member_join/remove`,
   `on_guild_channel_delete/create`) + the service's
   bind/unbind emits → `instant_sweep`.
6. **Version the seed** (`_SEED_VERSION`) - a build change re-seeds
   once, the repair reconciles forever.

Reference implementation: `botforge/discord/live_activity.py`
(matches forum, aoe2). Lot 4 applies it everywhere.
