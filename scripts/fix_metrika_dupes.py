#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all HTML files:
1. Remove ALL Yandex.Metrika blocks (including duplicates)
2. Fix broken favicon links that got split by Metrika insertion
3. Insert clean favicon + single Metrika block before </head>
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

CLEAN_FAVICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>\U0001f9e0</text></svg>">'

YM_BLOCK = '''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=109680006', 'ym');
    ym(109680006, 'init', {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
    });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109680006" style="position:absolute;left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->'''

# Pattern for the ENTIRE Metrika block (from open comment to close comment)
YM_PATTERN = re.compile(
    r'<!--\s*Yandex\.Metrika\s*counter\s*-->.*?<!--\s*/Yandex\.Metrika\s*counter\s*-->\s*',
    re.DOTALL | re.IGNORECASE
)

# Pattern for broken favicon: starts with <link rel="icon"... and ends with </svg>">
# But may have been split across lines with content in between
BROKEN_FAVICON = re.compile(
    r'<link\s+rel="icon"\s+href="data:image/svg\+xml,<svg\s+xmlns=%22[^%]*%22\s+viewBox=%22[^%]*%22>.*?</svg>">\s*',
    re.DOTALL
)

# Pattern for the theme script that sometimes appears between broken favicon parts
THEME_SCRIPT = re.compile(
    r'<script>\(function\(\)\{var\s+t=localStorage\.getItem\("theme"\).*?</script>\s*',
    re.DOTALL
)


def fix_file(filepath):
    rel = filepath.relative_to(BASE)
    content = filepath.read_text(encoding='utf-8')
    original = content

    # 1. Remove ALL Yandex.Metrika blocks (including duplicates)
    content = YM_PATTERN.sub('', content)

    # 2. Remove broken favicon (the split one with content in between)
    content = BROKEN_FAVICON.sub('', content)

    # 3. Remove any orphaned theme scripts that were between favicon parts
    content = THEME_SCRIPT.sub('', content)

    # 4. Remove any orphaned <text y=...🧠</text></svg>"> fragments
    content = content.replace('<text y=%22.9em%22 font-size=%2290%22>\U0001f9e0</text></svg>">', '')

    # 5. Insert clean favicon before </head>
    # First check if there's already a clean favicon
    if CLEAN_FAVICON not in content:
        content = content.replace('</head>', CLEAN_FAVICON + '\n' + YM_BLOCK + '\n</head>', 1)
    else:
        # Favicon exists, just insert Metrika after it
        content = content.replace(CLEAN_FAVICON, CLEAN_FAVICON + '\n' + YM_BLOCK, 1)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    html_files = sorted(BASE.rglob('*.html'))
    fixed = 0
    skipped = 0
    errors = []

    for f in html_files:
        if 'node_modules' in str(f):
            continue
        try:
            if fix_file(f):
                print(f'  FIXED: {f.relative_to(BASE)}')
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append((f, str(e)))
            print(f'  ERROR: {f.relative_to(BASE)}: {e}')

    print(f'\nDone. Fixed: {fixed}, Skipped (no changes): {skipped}')
    if errors:
        print(f'Errors: {len(errors)}')
        for f, e in errors:
            print(f'  {f}: {e}')


if __name__ == '__main__':
    main()
