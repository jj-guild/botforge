# Monetization — parked axes and long-term building blocks

**Status: PARKED — under glass.** Monetization is explicitly *out of scope* for
current phases. This document exists to preserve the research and design work
already done, so the subject can be reopened later **in consultation with the
community** without losing anything and without pressuring the roadmap.

- **No implementation, no issue, no commitment** is attached to anything below.
- Nothing here is a decision. Each axis is a *candidate*, with its open
  questions and preconditions. Pricing itself is handled separately by the
  project owner.
- This page is updated only when new ideas are deliberately parked here; it
  is never cited as a justification to start work.

## Why this document exists

Two epics (Monetization, Review & coaching marketplace) and one research task
(Discord App Monetization / SKUs) were removed from the tracker at the
developer's request. The content was worth keeping: it captured concrete
designs, provider research and legal constraints. Parking it here keeps the
tracker focused on the game, while giving the community a structured base to
build on when the time comes.

## Guiding principles (agreed so far)

1. **Community first** — any monetization decision is made *with* the
   community, never imposed. A proposal is shared and discussed before
   anything ships.
2. **The game stays free to play** — every candidate below is an *optional*
   service around the game (organization, convenience, marketplace), never a
   paywall on core gameplay.
3. **Sovereignty-first payments** — preference for European payment service
   providers and self-hosted escrow-capable wallets over US-only lock-in.
4. **Legal review is a hard gate** — anything touching real money (fees,
   commissions, cashprizes, escrow) requires a legal framing *before* any
   implementation.
5. **Concierge before code** — validate demand manually (a human does the
   job, the platform takes notes) before automating anything.

## Parked axes

### Axis A — Entitlements engine (organizer-side revenue)

A generic entitlements engine covering three primitives: **subscriptions**,
**per-event one-shot payments**, and **lifetime flags** (e.g. founder status).
The engine itself is game-agnostic and would live in the core, behind a
`PaymentProvider` abstraction.

Candidate applications:
- **Season Pass** per organizer-server: optional premium features for
  organizers running leagues/seasons.
- **Per-event hosting fee**: organizers pay a small fee when the platform
  hosts their tournament end-to-end.
- **Player entry fees**: opt-in paid entry for specific events.

Open questions:
- Which features are free vs. premium (must never split core gameplay)?
- Refund, chargeback and dispute handling — who owns it?
- Tax handling per country for entry fees.

Preconditions: community consultation, legal review, at least one proven
revenue-free season of organizer usage to know what is actually valuable.

### Axis B — Cashprize escrow (trust-based prize money)

Mode B cashprizes: players' entry fees fund a prize pool held in **escrow**
until the event completes, released to winners by the platform.

Design captured:
- Escrow via wallet-based PSPs (**Mangopay** or **Lemonway**), platform take
  rate of **5–10%**, behind legal review.
- Fallback providers: **Stripe**, and **Payplug** for French acquiring.

Open questions:
- Gambling/lottery regulation per country (this is the biggest legal risk of
  the whole page — potentially disqualifying).
- Minimum event size to be worth the operational cost.
- Dispute resolution when a result is contested.

Preconditions: legal review first (non-negotiable), insurance consideration,
community consultation on take rate.

### Axis C — Review & coaching marketplace (player-side revenue)

Players pay qualified reviewers for **structured game reports** or long-term
**coaching arcs** (tournament preparation).

Design captured:
- Reviewer pricing **tiered by level**, with levels verified by the platform
  through the rating system (Glicko-2 history) — no self-declared experts.
- Platform **take rate 15–20%**, **escrow until delivery**.
- The moat: the platform owns the player's match history, so the reviewer
  receives a **dossier**, not a cold DM — better coaching, less fraud.

Open questions:
- Quality assurance and post-session dispute handling.
- Revenue share for the reviewer's community vs. the platform.
- Whether Discord-native payments (Axis D) or external checkout fits better.

Preconditions: concierge validation (manually match a few reviewers and
players first), legal framing, community consultation.

### Axis D — Discord App Monetization (SKUs)

Using Discord's native App Monetization (**Premium Apps / SKUs**) as an
alternative collection channel for coaching payments.

Research captured (official Discord docs, July 2026):

- Native SKUs would require **Discord App Verification** (public privacy
  policy, public terms of service, complete app identity) — useful anyway to
  scale past 100 servers. Readiness work is tracked in
  jj-guild/botforge-services#154.
- **Economics**: Discord keeps a **15% platform fee** on the first $1M
  cumulative gross sales (10% after), on top of payment-processing and
  transaction fees; the first payout only happens after **$100** collective
  earnings; purchases through the iOS/Android apps add a **15–30% store
  fee**; Developer Policy requires the Discord price to be **no higher**
  than the same offering sold elsewhere.
- Payouts go to the **developer team's** Stripe account, never to individual
  coaches/reviewers — redistributing to them would recreate internal payment
  management (and its tax/legal burden), which is exactly what v1 avoids.
- Raw SKUs have **fixed prices set in the Developer Portal**: they cannot
  represent a per-coach freely-set price. Two candidate designs fit:
  - *Design A — consumable credit SKUs* (fixed price points, e.g. 10/25/50
    credits; players spend credits, coaches price in credits; the platform
    pays coaches out of team payouts — manual, ledgered).
  - *Design B — coach listing subscription* (one monthly user-subscription
    SKU: paying coaches appear in the coach pool and its filters; session
    money stays player↔coach direct). Design B is the simplest and most
    compliant: one SKU, one entitlement check, nothing to redistribute.
    Drawbacks: the fee share on small recurring revenue, the $100 payout
    threshold, and the risk that good unsubscribed coaches impoverish the
    pool (hidden vs. visible-not-bookable vs. bookable-out-of-filters —
    undecided).
- Payouts and refunds follow Discord's rules, not the platform's.

Open questions:
- Revenue share comparison: Discord SKUs vs. own PSP (Mangopay/Stripe).
- Whether verification requirements are compatible with the sovereignty-first
  principle.

Preconditions: none blocking — the *verification readiness* itself (privacy
policy, ToS, app identity) is worth doing independently and is tracked
elsewhere. The SKU decision is parked.

## What is NOT parked (stays out of this page)

- **Pricing** — amounts, tiers, take rates beyond the captured candidate
  ranges: decided separately by the project owner.
- **Any implementation work** — nothing on this page justifies a line of code.

## Reactivation process

1. The project owner opens the subject with the community (Discord, RFC-style
   post referencing this page).
2. One axis is picked; the discussion outcome is recorded as an **ADR** in
   `docs/DECISIONS/` (a decision to monetize is an architecture decision too).
3. Only then are tracker issues created, referencing the ADR.
4. This page is updated to mark the axis as *activated* and link the ADR.

## History

- 2026 (pre-pivot product plan): Epic H (Monetization) and Epic I (Review &
  coaching marketplace) designed with the game designers; Phase 4 target.
- Research task on Discord App Monetization (SKUs) recorded for the coaching
  mod.
- Decision with the game designers: the coaching mod itself ships **v1
  subscription-free, no payment handling** (indicative commission ledger
  only); monetization stays out of scope until the coach market justifies
  the verification programme.
- Epics and research issue deleted from the tracker; content preserved here,
  subject parked until community consultation.
