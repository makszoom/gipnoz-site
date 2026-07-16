# Major Decisions

> Record architectural or workflow choices that would be costly to re-debate.
> Use this template for each entry:

## YYYY-MM-DD: Decision title
**Decision:** _what was chosen_
**Rationale:** _why, in one or two sentences_
**Alternatives considered:** _what else was on the table and why rejected_
**Status:** active | revisited | superseded

## 2026-01-01: Four-layer memory separation
**Decision:** Split memory into working / episodic / semantic / personal rather than one flat folder.
**Rationale:** Each layer has different retention and retrieval needs. Flat memory breaks at ~6 weeks.
**Alternatives considered:** Flat directory (fails at scale), vector store (over-engineered for single user).
**Status:** active

## 2026-04-26: Add `design-md` seed skill (DESIGN.md / Google Stitch)
**Decision:** Ship a sixth seed skill, `design-md`, that points coding agents at a root `DESIGN.md` (Google Stitch format) as the visual-system source of truth. Loads only when `DESIGN.md` exists at the project root, default behavior is read-only on the contract file, and validation prefers `npx @google/design.md lint DESIGN.md` over hand-checks.
**Rationale:** `DESIGN.md` is becoming a de facto contract for AI-driven UI work; without an explicit skill, agents invent ad-hoc tokens that drift from the user's design system. Gating on `DESIGN.md`-existence keeps the skill silent on projects that don't use the format.
**Alternatives considered:** Bundle the rules into `git-proxy` or `skillforge` (wrong scope, wrong triggers); leave it to per-project `.agent/skills/` overrides (loses the cross-harness benefit); broader triggers like "UI"/"frontend"/"components"/"styling" (too generic, loads on every UI task even without DESIGN.md).
**Status:** active

## 2026-06-13: gipnozfree.com video hosting — Bunny Stream over Vimeo/YouTube
**Decision:** Use Bunny Stream (bunny.net) for video hosting instead of Vimeo ($20/mo) or YouTube Unlisted (no protection).
**Rationale:** Bunny Stream is $0.01/GB storage + $0.005/GB delivery, 20× cheaper than Vimeo. Domain-lock + simple token auth sufficient for paywall. Already uploaded 37 RU + 18 EN videos.
**Alternatives considered:** Vimeo ($20/mo flat, overkill for <500 views), YouTube Unlisted (zero protection, anyone with link watches), self-hosted (bandwidth costs).
**Status:** active

## 2026-06-13: Payments — NOWPayments (EN) + YooKassa (RU) over Stripe
**Decision:** Use NOWPayments for EN crypto (USDT) and YooKassa for RU ruble cards. Cloudflare Worker proxies webhooks to Firestore.
**Rationale:** Stripe / Lemon Squeezy unavailable for Russian residents. NOWPayments accepts crypto globally with 0.5–1% fee. YooKassa works with Russian cards (Sber, Mir). Avoids need for foreign LLC.
**Alternatives considered:** Stripe (requires US/UK entity), Lemon Squeezy (merchant of record, but blocked for RU residents), Gumroad (limited recurring, no RU payouts).
**Status:** active

## 2026-06-13: Video gating — simple CSS/JS over server-side token auth
**Decision:** Use client-side `gating.js` (CSS class toggle + Firebase Firestore check) instead of Bunny Stream Token Authentication.
**Rationale:** Token Auth broke video loading on static site (CORS, iframe issues) and added complexity without meaningful protection for non-DRM content. Simple gating is "good enough" for educational video.
**Alternatives considered:** Bunny Token Auth (server-side signed URLs, broke), Cloudflare Access (overkill), Vimeo domain lock ($20/mo).
**Status:** active

## 2026-07-01: Chrome extensions as traffic drivers, not products
**Decision:** Build free Chrome extensions (Calm Anchor, Sleep Now) that drive traffic to gipnozfree.com courses. Zero monetization inside extensions.
**Rationale:** Generic breathing/meditation extensions fail (Google embeds in SERP, mobile apps dominate). Position around clinical hypnosis / Pavlovian anchoring — niche with no Google competition. Extensions act as "warm leads" — user gets value, then sees "Learn more" → course upsell.
**Alternatives considered:** Monetized extensions (Freemium, ads — rejected by user), paid extensions (CWS ranking harder), generic wellness (competes with Google + Calm app).
**Status:** active

## 2026-07-03: CWS description — "Pavlovian anchoring" over "breathing exercise"
**Decision:** Rewrite Calm Anchor description to emphasize Pavlovian anchoring / clinical hypnosis, removing "breathing exercise" completely.
**Rationale:** Generic breathing tools are commoditized (Google SERP has built-in breathing circle, mobile apps dominate). Pavlovian anchoring is unique, defensible, and aligns with Gerald Kein hypnosis methodology.
**Alternatives considered:** Keep "breathing exercise" (easier to understand, but competes with Google), rebrand entirely (too late, brand established).
**Status:** active
