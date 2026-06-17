#!/usr/bin/env python3
"""Move auth-core.js from <head> to just before </body> (before inline scripts)."""
import os, re

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
    
    # Determine correct path to auth-core.js from this file
    is_en = relpath.startswith('en')
    depth = relpath.count('/')
    
    if is_en:
        if depth == 1:
            auth_path = '../js/auth-core.js'
        else:
            auth_path = '../../js/auth-core.js'
    else:
        if depth == 0:
            auth_path = 'js/auth-core.js'
        else:
            auth_path = '../js/auth-core.js'
    
    # Remove auth-core.js from wherever it is
    lines = content.split('\n')
    new_lines = [l for l in lines if 'auth-core.js' not in l]
    new_content = '\n'.join(new_lines)
    
    # Insert auth-core.js before the first <script> block before </body>
    # Find the last <script> block before </body>
    body_end = new_content.find('</body>')
    if body_end == -1:
        print(f"  SKIP (no </body>): {relpath}")
        continue
    
    # Find the last <script> before </body>
    last_script_start = new_content.rfind('<script', 0, body_end)
    
    if last_script_start == -1:
        # No scripts at bottom, just insert before </body>
        insert = f'<script src="{auth_path}"></script>\n'
        new_content = new_content.replace('</body>', insert + '</body>')
    else:
        # Insert auth-core.js right before the last script block
        insert = f'<script src="{auth_path}"></script>\n'
        new_content = new_content[:last_script_start] + insert + new_content[last_script_start:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  OK: {relpath}")
    updated += 1

print(f"\nUpdated: {updated}")
