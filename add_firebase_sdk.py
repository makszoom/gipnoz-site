#!/usr/bin/env python3
"""Add Firebase SDK script tags to all HTML pages (before </head>)."""
import os, re

SITE_DIR = "C:/Users/valter/hermes-projects/gipnoz-site"

firebase_sdk = '''  <!-- Firebase SDKs -->
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js"></script>
  <script src="js/auth-core.js"></script>'''

firebase_sdk_en = '''  <!-- Firebase SDKs -->
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js"></script>
  <script src="../js/auth-core.js"></script>'''

html_files = []
for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML files")

# Pattern: find </head> and insert before it
pattern = re.compile(r'</head>')

updated = 0
for filepath in html_files:
    relpath = os.path.relpath(filepath, SITE_DIR)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has Firebase SDK
    if 'firebase-app-compat.js' in content:
        continue
    
    # Determine path to auth-core.js
    is_en = relpath.startswith('en')
    is_login = relpath.endswith('login.html')
    
    if is_en:
        sdk = firebase_sdk_en
    else:
        sdk = firebase_sdk
    
    # Insert before </head>
    new_content = pattern.sub(sdk + '\n</head>', content)
    
    if new_content == content:
        print(f"  SKIP (no </head>): {relpath}")
        continue
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  OK: {relpath}")
    updated += 1

print(f"\nUpdated: {updated}")
