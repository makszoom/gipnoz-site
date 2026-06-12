#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate sitemap.xml for gipnoz-site."""

import os
import glob
from datetime import datetime, timezone

# Корневая директория сайта (родитель директории scripts/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'https://makszoom.github.io/gipnoz-site'

def lastmod(path):
    mtime = os.path.getmtime(path)
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return dt.strftime('%Y-%m-%d')

def url_entry(rel_path, priority, changefreq='weekly'):
    # rel_path like 'index.html' or 'modules/module-0/lesson-0-1.html'
    full_path = os.path.join(BASE_DIR, rel_path)
    loc = f'{BASE_URL}/{rel_path.replace(os.sep, "/")}'
    # Strip .html for cleaner URLs where index.html
    if loc.endswith('/index.html'):
        loc = loc[:-10]  # remove 'index.html'
    lm = lastmod(full_path)
    return f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>'

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

# Priority map
entries = [
    # Main pages (highest priority)
    ('index.html', '1.0', 'weekly'),
    ('en/index.html', '1.0', 'weekly'),
    ('modules.html', '0.9', 'weekly'),
    ('en/modules.html', '0.9', 'weekly'),
    ('beginner.html', '0.9', 'weekly'),
    ('advanced.html', '0.9', 'weekly'),
    ('scripts.html', '0.8', 'weekly'),
    ('en/scripts.html', '0.8', 'weekly'),
    ('about.html', '0.7', 'monthly'),
    ('en/about.html', '0.7', 'monthly'),
    ('donate.html', '0.7', 'monthly'),
    ('en/donate.html', '0.7', 'monthly'),
]

for rel, pri, freq in entries:
    full = os.path.join(BASE_DIR, rel)
    if os.path.exists(full):
        lines.append(url_entry(rel, pri, freq))

# RU lessons
ru_lessons = sorted(glob.glob(os.path.join(BASE_DIR, 'modules', '*', 'lesson-*.html')))
for p in ru_lessons:
    rel = os.path.relpath(p, BASE_DIR)
    lines.append(url_entry(rel, '0.6', 'monthly'))

# EN lessons
en_lessons = sorted(glob.glob(os.path.join(BASE_DIR, 'en', '*', 'lesson-*.html')))
for p in en_lessons:
    rel = os.path.relpath(p, BASE_DIR)
    lines.append(url_entry(rel, '0.6', 'monthly'))

# Script pages
ru_scripts = sorted(glob.glob(os.path.join(BASE_DIR, 'scripts', 'script-*.html')))
for p in ru_scripts:
    rel = os.path.relpath(p, BASE_DIR)
    lines.append(url_entry(rel, '0.5', 'monthly'))

en_scripts = sorted(glob.glob(os.path.join(BASE_DIR, 'en', 'scripts', 'script-*.html')))
for p in en_scripts:
    rel = os.path.relpath(p, BASE_DIR)
    lines.append(url_entry(rel, '0.5', 'monthly'))

lines.append('</urlset>')

out_path = os.path.join(BASE_DIR, 'sitemap.xml')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f'Wrote {len(lines)-2} URLs to {out_path}')
