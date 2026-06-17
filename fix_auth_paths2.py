#!/usr/bin/env python3
"""Fix auth-core.js paths on all pages — use absolute path /js/auth-core.js."""
import os

SITE_DIR = "C:/Users/valter/hermes-projects/gipnoz-site"

html_files = []
for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML files")

updated = 0
for filepath in html_files:
    relpath = os.path.relpath(filepath, SITE_DIR)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'auth-core.js' not in content:
        continue
    
    # Replace any relative path to auth-core.js with absolute path
    # Match: src="anything/auth-core.js" -> src="/js/auth-core.js"
    import re
    new_content = re.sub(
        r'src="[^"]*auth-core\.js"',
        'src="/js/auth-core.js"',
        content
    )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK: {relpath}")
        updated += 1
    else:
        print(f"  SKIP (no change): {relpath}")

print(f"\nUpdated: {updated}")
