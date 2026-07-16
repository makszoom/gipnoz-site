---
name: static-education-site
description: Build and deploy a mobile-first, dark-theme static education site with video courses, membership, payments, and bilingual SEO — based on the gipnozfree.com blueprint.
version: 2.0.0
triggers:
  - "education site"
  - "video course site"
  - "membership site"
  - "static site with paywall"
  - "online course platform"
  - "hypnosis course"
  - "training site"
  - "bilingual site"
  - "gipnoz"
---

# Static Education Site Blueprint

Build a production-grade static education site with video courses, membership, payments, and bilingual SEO.

---

## Architecture Decisions

### Stack (non-negotiable)
- **Static HTML/CSS/vanilla JS only.** No frameworks, no Node.js on production.
- **Single CSS file** with CSS custom properties for theming (dark default, light via `[data-theme="light"]`).
- **No build step.** Every HTML file is self-contained with shared CSS/JS via `<link>` and `<script>`.

### Hosting & DNS
- **GitHub Pages** for static hosting (free, fast, automatic deploy on push).
- **Cloudflare** for DNS + SSL (Full mode) + custom domain.
- **Bunny Stream** for video hosting (not self-hosted — too heavy).

### Auth & Membership
- **Firebase Auth** (email/password or social). One project, one Firestore for subscriptions.
- API key split into `k1 + k2` in client JS to avoid log masking.
- `auth-core.js` loaded with **absolute path** `/js/auth-core.js` before `</body>`.
- **SEO hub pages** (landing pages, about, etc.) — NO auth. Only lesson/video pages need auth.

### Payments
- **NOWPayments** for crypto (USDT, etc.).
- **YooKassa** for local currency card payments.
- **Cloudflare Worker** as payment webhook proxy (HMAC-SHA512 verification → Firestore).
- Worker secrets via `wrangler secret put`.

### Video Paywall
- **Client-side gating only.** No server-side token signing — it breaks on static sites.
- CSS classes: `.lesson-video` (paywall placeholder), `.lesson-video-player` (iframe wrapper).
- Single `gating.js` file with language detection.
- RU: free after login. EN: requires active subscription.

### Bilingual Structure
- Root = primary language (RU), `/en/` = secondary.
- `<link rel="alternate" hreflang="...">` on every page.
- Language detection: `navigator.language` + `localStorage('preferred_lang')`.
- **Language switcher ONLY on homepages** (`index.html`, `en/index.html`). Internal pages have no switcher — avoids 404 on asymmetric structures.

---

## Deploy

**Hosting**: GitHub Pages + Cloudflare custom domain.
- Branch: `master` (or `main`)
- **Deploy**: `git push origin master` — GitHub Pages builds automatically

```bash
git add -A && git commit -m "fix: ..."
git push origin master
```

**Verify live** — after push, wait **5-10 minutes** before trusting `curl` output:

```bash
# Step 1: check raw GitHub (source of truth)
curl -s "https://raw.githubusercontent.com/USER/REPO/master/about.html" | grep '<nav>'

# Step 2: check live domain (may lag behind raw)
curl -s "https://yourdomain.com/about.html" | grep '<nav>'

# If raw shows the fix but live doesn't → cache delay, not deploy failure
```

**Cloudflare cache delay** — even after Purge Everything + Development Mode, edge nodes may serve stale HTML for **3-5 minutes** (sometimes up to 10). Query params and cache-bypass headers do NOT help.

**When live is stale but raw is clean** — possible causes:
1. GitHub Pages hasn't rebuilt yet → trigger with empty commit: `git commit --allow-empty -m "trigger: rebuild" && git push origin master`
2. Cloudflare cache → Purge Everything + wait 3-5 min, or enable Development Mode

**Critical rule**: Do NOT re-edit files, re-push commits, or patch code based on stale live output. If raw GitHub shows the fix → the fix IS deployed.

---

## Critical Pitfalls

- **Bunny Stream Token Authentication — DO NOT IMPLEMENT.** Attempted and rolled back after breaking video playback. Client-side gating with static iframes is the working approach.
- **Firebase Firestore frontend SDK hangs from some regions** — NEVER use for gating checks on client. Move ALL subscription verification to Cloudflare Worker.
- **Batch HTML editing — sed fails with HTML entities** — write Python script via `write_file`, then run via `terminal` with full Python path. See references for template.
- **Structural asymmetry between languages** — RU and EN often have different page structures (e.g., `modules/` vs `en/beginner/`). Language switch links on internal pages must point to the OTHER LANGUAGE HOMEPAGE, not a mirrored internal page.
- **Making mass changes without understanding project structure** — Before any batch edit across 10+ files, FIRST audit the project: list all HTML files, verify structural relationships, check git history. When user says "study the project thoroughly" — they mean exactly this.
- **Cloudflare cache delay** — Purge Everything + Development Mode ≠ instant. Edge nodes process asynchronously. Wait 3-10 minutes.

---

## Site Structure Template

```
site/
├── index.html              # Homepage with language redirect
├── modules.html            # Course catalog
├── scripts.html            # Scripts catalog
├── subscribe.html          # Pricing/payment page
├── login.html              # Auth page
├── about.html              # About page
├── donate.html             # Donations
├── dashboard.html          # User dashboard (post-login)
├── 404.html                # Custom 404
│
├── ru/                     # Hub pages (SEO landing pages)
│   └── topic-1.html
│
├── en/                     # English mirror
│   ├── index.html
│   ├── modules.html
│   ├── scripts.html
│   ├── subscribe.html
│   ├── login.html
│   ├── about.html
│   ├── donate.html
│   ├── dashboard.html
│   ├── hub-page-1.html     # SEO hub pages — NO auth
│   ├── hub-page-2.html
│   ├── lessons/            # Individual lesson pages
│   ├── scripts/            # Individual script pages
│   └── img/                # Images
│
├── modules/                # RU lesson pages
│   ├── module-1/
│   │   ├── lesson-1-1.html
│   │   └── ...
│   └── module-N/
│
├── scripts/                # RU script pages
│
├── css/
│   └── style.css            # Single shared CSS
├── js/
│   ├── auth-core.js         # Firebase Auth (absolute path /js/auth-core.js)
│   ├── gating.js            # Paywall check
│   └── payments.js          # Payment UI
│
├── sitemap.xml              # Auto-generated
└── robots.txt
```

---

## Verification Commands

```bash
# After deploy: verify raw GitHub vs live
curl -s "https://raw.githubusercontent.com/USER/REPO/master/about.html" | grep '<nav>'
curl -s "https://yourdomain.com/about.html" | grep '<nav>'

# Verify auth removed from hub pages
for f in en/hub-page-*.html ru/topic-*.html; do
  grep -c "auth-core" "$f"  # should be 0
done

# Verify analytics present
for f in index.html en/index.html; do
  grep -c "gtag\|G-" "$f"     # GA4
done
```
