# Personal Preferences

> **This file is yours.** It's the first thing your AI reads at the start of every session.
> Edit any time. Last updated: 2026-07-01.

## Who I am
- **Name:** Макс
- **Languages:** Russian (native), English (working proficiency)
- **Location:** Russia
- **Timezone:** MSK (UTC+3)
- **Platform:** Windows 10, git-bash terminal

## Code style
- **Stack:** Static HTML/CSS/vanilla JS. No frameworks, no Node.js on production.
- **CSS:** Single file, CSS custom properties, dark theme default, light via `[data-theme="light"]`.
- **JS:** Vanilla, no build step. IIFE pattern. Absolute paths for all `<script src>`.
- **Python:** 3.10 at `/c/Users/valter/AppData/Local/Programs/Python/Python310/python.exe`.
- **Simplicity:** Prefer simple client-side solutions over complex server-side ones. Gating.js over Token Auth — always choose the lighter approach.
- **Security:** Lightweight, testable. Don't introduce architectural complexity for marginal protection.

## Workflow
- **Research first** for non-obvious bugs. Find upstream patterns (Bootstrap, Material Design) before proposing fixes.
- **Ask before bulk destructive operations.** Don't delete or rewrite dozens of files without confirmation.
- **Use `patch` for edits**, not full file rewrites.
- **Test before claiming success.** Verify with real tool output, not assumptions.
- **Prefer compact files + short summaries** over walls of text.

## Communication
- **Be direct.** Skip pleasantries, surface tradeoffs.
- **Russian + English.** I often need RU translations alongside EN content.
- **Detail-oriented.** I catch inaccuracies — double-check facts before presenting them.
- **"Делай хорошо, не халтурь."** Quality matters. No templates, no filler.

## SEO & Content
- **Unique content only.** No templates, no duplicate text across pages.
- **Meta descriptions:** ≤160 characters, real keywords, CTA.
- **Bilingual:** RU + EN with proper `<link rel="alternate" hreflang="...">`.
- **Lesson titles:** Hypnosis techniques only — no stories, anecdotes, or narrative fluff. List multiple main topics covered.
- **Reddit:** Short, natural English, no fluff. Often need RU translation alongside.

## Project: gipnozfree.com
- **Repo:** `/c/Users/valter/hermes-projects/gipnoz-site` (canonical)
- **Domain:** gipnozfree.com (Beget)
- **Hosting:** Beget, Cloudflare DNS (NS: jocelyn+sullivan, SSL: Full)
- **Video:** Bunny Stream (RU lib: 684480 — 37 videos, EN lib: 685123 — 18 videos). Trial ended Jul 2026, reactivated with $10.
- **Auth:** Firebase Auth (project: gipnoz-site)
- **Payments:** NOWPayments (EN crypto) + YooKassa (RU cards), Cloudflare Worker proxy
- **Analytics:** GA4 (G-RMV8EW30RW) + Yandex.Metrika (109680006)
- **SEO:** 148 pages, sitemap submitted to GSC, targeting both Russian and English-speaking audiences
- **Domain history:** Blocked by registrar Jul 1 2026 due to unverified contact email; unblocked same day after verification.
- **INN:** 720319977466

## Chrome Extensions (traffic drivers)
- **Calm Anchor:** Instant anxiety relief via Pavlovian anchoring. On CWS review (updated description removed "breathing exercise").
- **Sleep Now:** Progressive relaxation for sleep. On CWS review. Includes ambient rain (Web Audio API + MP3 fallback).
- **Strategy:** Free extensions → traffic to gipnozfree.com via "Learn more" buttons. Zero permissions, zero monetization inside extensions.

## AI Tools
- **Hermes Agent** with Nous Portal subscription
- **Main model:** DeepSeek V4 Pro (coding), Kimi K2.6 (reading/docs)
- **Telegram gateway** in polling mode, cron health check every 1h
- **Mem0** for external memory
- **Interested in:** Cursor integration via agentic-stack for cross-agent knowledge sharing
- **Preferred execution:** Direct implementation (CSS, JS) over tool recommendations (Figma, Open Design rejected)
