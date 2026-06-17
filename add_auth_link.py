#!/usr/bin/env python3
"""Add auth-link to header nav on all HTML pages."""
import os, re

SITE_DIR = "C:/Users/valter/hermes-projects/gipnoz-site"

# Find all HTML files
html_files = []
for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML files")

# The auth link snippet to insert before theme-toggle button
ru_link = '<a href="login.html" id="auth-link" data-label="Войти" data-href="login.html" data-confirm="Выйти?">Войти</a>\n      '
en_link = '<a href="login.html" id="auth-link" data-label="Sign in" data-href="login.html" data-confirm="Sign out?">Sign in</a>\n      '

# Pattern: find theme-toggle button and insert auth-link before it
# We match the theme-toggle line and insert before it
pattern = re.compile(r'(      <button class="theme-toggle")')

updated = 0
for filepath in html_files:
    relpath = os.path.relpath(filepath, SITE_DIR)
    
    # Skip login pages (they already have auth-link)
    if relpath.endswith('login.html'):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if auth-link already exists
    if 'id="auth-link"' in content:
        continue
    
    # Determine language: files under en/ are English
    is_en = relpath.startswith('en')
    link = en_link if is_en else ru_link
    
    # Insert before theme-toggle
    new_content = pattern.sub(link + r'\1', content)
    
    if new_content == content:
        # Try alternative: maybe theme-toggle has different spacing
        # Some files might have different indentation
        alt_pattern = re.compile(r'(<button class="theme-toggle")')
        new_content = alt_pattern.sub(link.strip() + '\n    ' + r'\1', content)
        if new_content == content:
            print(f"  SKIP (no theme-toggle): {relpath}")
            continue
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  OK: {relpath}")
    updated += 1

print(f"\nUpdated: {updated}")
