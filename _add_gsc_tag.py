import re
from pathlib import Path

google_tag = '  <meta name="google-site-verification" content="2F4JYeb27ZKVf0utjU8QS4GLRsW8CoZ3MSiE-cfqtn0" />\n'

project = Path('.')
html_files = []
for f in project.rglob('*.html'):
    if '.git' not in str(f) and 'node_modules' not in str(f):
        html_files.append(f)

fixed = 0
skipped = 0
for f in sorted(html_files):
    content = f.read_text(encoding='utf-8')
    
    # Skip if already has Google verification
    if 'google-site-verification' in content:
        skipped += 1
        continue
    
    # Add after <head> tag
    new_content = re.sub(r'(<head>\s*\n)', r'\1' + google_tag, content, count=1)
    
    if new_content != content:
        f.write_text(new_content, encoding='utf-8')
        fixed += 1
    else:
        skipped += 1

print(f'Fixed: {fixed}, Skipped (already has tag or no <head>): {skipped}')
