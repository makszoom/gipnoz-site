# AGENTS.md — gipnozfree.com

> **Гипноз с нуля / Hypnosis from Scratch** — образовательный сайт с курсом гипноза по методике Джерри Кайн (Gerald Kein).
> Двуязычный (RU + EN), статический HTML/CSS/JS, тёмная тема, mobile-first.

---

## Архитектура

```
gipnoz-site/
├── index.html              # RU главная (редирект по языку)
├── modules.html            # RU каталог модулей
├── scripts.html            # RU каталог скриптов
├── subscribe.html          # RU страница подписки
├── login.html              # RU страница входа
├── about.html              # RU о проекте
├── donate.html             # RU донаты
├── dashboard.html          # RU личный кабинет
├── 404.html                # Кастомная 404
│
├── ru/                     # RU hub-страницы (SEO-лендинги)
│   ├── kak-rabotaet-gipnoz.html
│   ├── obuchenie-gipnozu.html
│   └── samogipnoz.html
│
├── en/                     # EN версия (зеркальная структура)
│   ├── index.html
│   ├── modules.html
│   ├── scripts.html
│   ├── subscribe.html
│   ├── login.html
│   ├── about.html
│   ├── donate.html
│   ├── dashboard.html
│   ├── beginner.html       # Hub: Beginner-Intermediate (12 уроков)
│   ├── advanced.html        # Hub: Advanced (6 уроков)
│   ├── self-hypnosis.html   # Hub
│   ├── how-hypnosis-works.html
│   ├── is-hypnosis-real.html
│   ├── hypnosis-for-sleep.html
│   ├── hypnosis-for-weight-loss.html
│   ├── anxiety.html
│   ├── become-hypnotherapist.html
│   ├── beginner/            # 12 уроков (lesson-01..12.html)
│   ├── advanced/            # 6 уроков (lesson-adv1..6.html)
│   ├── scripts/             # 33 скрипта гипноза (EN)
│   └── img/                 # Изображения
│
├── modules/                # RU уроки (6 модулей × 5-6 уроков)
│   ├── module-0/           # Введение
│   ├── module-1/           # Базовые техники
│   ├── module-2/           # ...
│   ├── module-3/
│   ├── module-4/
│   ├── module-5/
│   └── module-6/
│
├── scripts/                # RU скрипты гипноза (33 шт)
│
├── css/
│   └── style.css            # Единый CSS (1419 строк, CSS-переменные, тёмная/светлая тема)
│
├── js/
│   ├── auth-core.js         # Firebase Auth (ключ split на k1+k2)
│   ├── gating.js            # Paywall: .lesson-video скрывается до логина/подписки
│   └── payments.js          # NOWPayments + YooKassa, Cloudflare Worker прокси
│
├── cloudflare-worker.js     # Webhook: NOWPayments IPN → Firestore
├── docs/                    # Статьи для Medium/Reddit
└── sitemap.xml              # 143 URL, отправлен в GSC
```

---

## Стек и внешние сервисы

| Сервис | Назначение | Ключевые данные |
|--------|-----------|----------------|
| **Beget** | Хостинг | gipnozfree.com |
| **Cloudflare** | DNS, SSL | NS: jocelyn+sullivan, SSL: Full, Account: Makszoom85@gmail.com |
| **Bunny Stream** | Видеохостинг | RU library: 684480 (37 видео), EN library: 685123 (18 видео), API: 951599e7... |
| **Firebase Auth** | Аутентификация | Project: gipnoz-site, API key split на k1+k2 в auth-core.js |
| **Firebase Firestore** | Подписки пользователей | Service Account: firebase-adminsdk-fbsvc@gipnoz-site |
| **NOWPayments** | Крипто-платежи | Monthly EN: 1209593029, Lifetime EN: 4436108535 |
| **YooKassa** | Рублёвые платежи (RU) | Через Cloudflare Worker |
| **Bybit** | Приём USDT | TBEymscYret4g8TJmniPKsoYJhD6b1A6gB |
| **GA4** | Аналитика | G-RMV8EW30RW |
| **Yandex.Metrika** | Аналитика (RU) | 109680006 |

---

## Ключевые решения и уроки

### Видео и paywall
- **Bunny Stream Token Authentication НЕ ИСПОЛЬЗОВАТЬ.** Сломало загрузку видео на статическом сайте. Вместо этого — простой клиентский `gating.js`.
- `.lesson-video` — CSS-класс для paywall-заглушки. `.lesson-video-player` — обёртка для iframe плеера.
- Gating: RU — видео открыто после логина (бесплатно). EN — требуется активная подписка.
- Видео вставляются через Bunny Stream iframe (не через API подписи).

### Firebase Auth
- `auth-core.js` должен подключаться с **абсолютным путём** `/js/auth-core.js` (не относительным). Относительные пути ломаются на страницах с разной глубиной директорий.
- API ключ **разделён на две части** (k1 + k2) чтобы избежать автоматического маскинга в логах.
- Скрипт должен быть перед `</body>`, **не в `<head>`**.
- Домен `gipnozfree.com` должен быть в Firebase Authorized domains.

### Платежи
- Cloudflare Worker (`gipnoz-payments.makszoom85.workers.dev`) проксирует создание NOWPayments инвойсов и верифицирует IPN webhook (HMAC-SHA512).
- Worker пишет статус подписки в Firestore через REST API.
- Секреты (IPN secret, API key, Firebase SA JSON) хранятся в `wrangler secret`.

### SEO
- **Каждая страница — уникальный контент.** Никаких шаблонных текстов.
- Meta description: ≤160 символов, реальные ключевые слова, CTA.
- Двуязычность: `<link rel="alternate" hreflang="ru/en">` на каждой странице.
- Sitemap: 143 URL, отправлен в Google Search Console.
- Open Graph теги на всех страницах.
- Yandex.Metrika + GA4 на всех 148 страницах.

### Дизайн
- Тёмная тема по умолчанию, светлая через `[data-theme="light"]`.
- CSS-переменные в `:root` (--bg, --accent, --text, --border и т.д.).
- Акцентный цвет: `#7c3aed` (фиолетовый).
- Шрифт: Inter, system-ui.
- Максимальная ширина контента: 800px.
- Mobile-first, адаптивная вёрстка.

### Языковая логика
- Определение языка: `navigator.language` + `localStorage('preferred_lang')`.
- RU — корень сайта, EN — `/en/`.
- Переключение языка: ссылки в header, сохраняется в localStorage.

---

## Соглашения разработки

- **Только статические файлы** — HTML, CSS, vanilla JS. Никаких фреймворков, никакого Node.js на проде.
- **Никаких секретов в репозитории.** API ключи, IPN секреты — только в `.env`, `wrangler secret`, или памяти Hermes.
- **Перед деплоем:** проверить что все `<script src="...">` используют абсолютные пути.
- **Новые страницы:** добавить GA4 + Metrika, Open Graph, hreflang alternates, meta description ≤160 chars.
- **Редактирование:** использовать `patch` (не перезаписывать весь файл), проверять что не сломались соседние элементы.
- **Безопасность:** предпочитать простые клиентские решения сложным серверным. Gating.js вместо Token Auth — пример правильного подхода.

---

## Полезные команды

```bash
# Репозиторий
cd /c/Users/valter/hermes-projects/gipnoz-site

# Деплой на Beget (через FTP или git)
# ...

# Проверка sitemap
# Открыть https://gipnozfree.com/sitemap.xml
```

---

## Agentic-stack brain

This project uses a portable brain in `.agent/`. Treat it as authoritative.

### Startup (read in order)
1. `.agent/AGENTS.md` — the map
2. `.agent/memory/personal/PREFERENCES.md` — user conventions
3. `.agent/memory/semantic/LESSONS.md` — distilled lessons
4. `.agent/protocols/permissions.md` — hard rules

### Skills
Skills under `.agent/skills/<name>/SKILL.md` follow the agentskills.io standard.
Use `/skills` in Hermes to browse them; load `SKILL.md` only when triggers match the current task.

### Recall before non-trivial tasks
For deploy / ship / migration / schema / timestamp / date / failing test /
debug / refactor, FIRST run:

```bash
python3 .agent/tools/recall.py "<description>"
```

Surface results in a `Consulted lessons before acting:` block and follow them.

### Memory discipline
- Update `.agent/memory/working/WORKSPACE.md` as you work.
- After significant actions, run `python3 .agent/tools/memory_reflect.py <skill> <action> <outcome>`.
- Never delete memory entries; archive only.
- Quick state: `python3 .agent/tools/show.py`.
- Teach a rule in one shot: `python3 .agent/tools/learn.py "<rule>" --rationale "<why>"`.

### Hard rules
- No force push to `main`, `production`, `staging`.
- No modification of `.agent/protocols/permissions.md`.
