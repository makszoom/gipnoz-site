#!/usr/bin/env python3
"""Fix auth-link href to use absolute paths (/login.html) instead of relative."""
import os, re

SITE_DIR = "C:/Users/valter/hermes-projects/gipnoz-site"

html_files = []
for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML files")

# Fix RU pages: data-href="login.html" -> data-href="/login.html"
# Fix EN pages: data-href="login.html" -> data-href="/en/login.html"
# Also fix the href attribute itself if it's just login.html

ru_fixed = 0
en_fixed = 0

for filepath in html_files:
    relpath = os.path.relpath(filepath, SITE_DIR)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'id="auth-link"' not in content:
        continue
    
    is_en = relpath.startswith('en')
    new_content = content
    
    if is_en:
        # EN: data-href="login.html" -> data-href="/en/login.html"
        new_content = new_content.replace('data-href="login.html"', 'data-href="/en/login.html"')
        # Also fix the href attribute if it's a bare relative link
        new_content = re.sub(r'href="login\.html"', 'href="/en/login.html"', new_content)
    else:
        # RU: data-href="login.html" -> data-href="/login.html"
        new_content = new_content.replace('data-href="login.html"', 'data-href="/login.html"')
        new_content = re.sub(r'href="login\.html"', 'href="/login.html"', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        if is_en:
            en_fixed += 1
        else:
            ru_fixed += 1
        print(f"  OK: {relpath}")

print(f"\nRU fixed: {ru_fixed}, EN fixed: {en_fixed}")
