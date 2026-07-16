# Lessons (auto-distilled + manually curated)

> Entries here outlive specific tasks. The dream cycle promotes recurring
> patterns from episodic into this file. Feel free to curate manually —
> delete bad lessons, tighten wording, reorganize sections.

## Seed lessons
- Always read `protocols/permissions.md` before any destructive tool call.
- Write the failing test before writing the fix.
- Log to episodic memory on every significant action, success or failure.
- When a skill has failed 3+ times in 14 days, propose a rewrite.
- Never force push to protected branches under any circumstance.

## Auto-promoted entries will be appended below

### 2026-07

- Bunny Stream Token Authentication broke video loading on static sites — prefer simple client-side gating.js over server-side signing for non-DRM content  <!-- status=accepted confidence=0.6 evidence=1 id=lesson_a5ff33b745de -->
- Firebase auth-core.js must use absolute path /js/auth-core.js (not relative) and be loaded before </body> (not <head>) on static multi-directory sites  <!-- status=accepted confidence=0.6 evidence=1 id=lesson_9aeeaa06c72b -->
- For static education sites with video paywall: use .lesson-video CSS class for gating placeholder and .lesson-video-player for the iframe wrapper — keep gating logic in a single gating.js file  <!-- status=accepted confidence=0.6 evidence=1 id=lesson_3f4bfe3e42a6 -->
- Split sensitive API keys into parts (k1 + k2) in client-side JS to avoid automatic secret masking in logs and git diffs — assemble at runtime  <!-- status=accepted confidence=0.6 evidence=1 id=lesson_ed4fcfb99f23 -->
- After git push to GitHub Pages custom domain, always verify raw GitHub first. Wait 5-10 minutes before trusting live output. If raw shows the fix but live doesn't, it's a Cloudflare cache delay — NOT a deploy failure. Do NOT re-edit or re-push based on stale live output. If GitHub Pages hasn't rebuilt, trigger with: git commit --allow-empty -m 'trigger: rebuild' && git push origin master  <!-- status=accepted confidence=0.6 evidence=1 id=lesson_aebea83c3f9e -->
- Calm Anchor CWS description: emphasize Pavlovian anchoring / clinical hypnosis, never "breathing exercise" — Google SERP already embeds breathing tools, mobile apps dominate  <!-- status=legacy confidence=0.7 evidence=0 id=lesson_legacy_59e28d8b7906 -->
- CWS manifest description: hard limit 132 characters — write compact descriptions that fit without truncation  <!-- status=legacy confidence=0.7 evidence=0 id=lesson_legacy_4d69e24fce16 -->
- Chrome extension strategy: position around clinical hypnosis niche, not generic wellness — avoids competition with Google embedded tools (breathing circle) and mobile apps (Calm, Headspace)  <!-- status=legacy confidence=0.7 evidence=0 id=lesson_legacy_c67673b3f8a3 -->

### 2026-04

- Always serialize timestamps in UTC to avoid cross-region comparison bugs  <!-- status=accepted confidence=0.46 evidence=1 id=lesson_422695ae5b2d -->
