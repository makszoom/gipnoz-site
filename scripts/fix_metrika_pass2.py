#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECOND PASS: Remove orphaned Metrika comments and remaining broken favicon fragments.
After pass 1, some files still have orphaned <!-- Yandex.Metrika counter --> 
comments that weren't part of a complete block.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# Remove ANY remaining Yandex.Metrika comment (open or close) — standalone
ORPHANED_OPEN = re.compile(r'<!--\s*Yandex\.Metrika\s*counter\s*-->\s*', re.IGNORECASE)
ORPHANED_CLOSE = re.compile(r'<!--\s*/Yandex\.Metrika\s*counter\s*-->\s*', re.IGNORECASE)

# Remove any remaining broken favicon fragments
BROKEN_FAVICON_FRAG = re.compile(
    r'<link\s+rel="icon"\s+href="data:image/svg\+xml.*?</svg>">\s*',
    re.DOTALL
)

# Remove orphaned <text y=...🧠</text></svg>"> fragments
ORPHANED_SVG = re.compile(r'<text\s+y=%22.*?</text></svg>">\s*', re.DOTALL)

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


def fix_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content

    # 1. Remove any remaining broken favicon (the split one)
    content = BROKEN_FAVICON_FRAG.sub('', content)

    # 2. Remove orphaned SVG fragments
    content = ORPHANED_SVG.sub('', content)

    # 3. Remove ALL orphaned Metrika comments (open and close)
    content = ORPHANED_OPEN.sub('', content)
    content = ORPHANED_CLOSE.sub('', content)

    # 4. Ensure clean favicon exists before </head>
    if CLEAN_FAVICON not in content:
        content = content.replace('</head>', CLEAN_FAVICON + '\n' + YM_BLOCK + '\n</head>', 1)
    else:
        # Favicon exists, ensure Metrika block follows it
        # Check if Metrika block already follows favicon
        favicon_pos = content.find(CLEAN_FAVICON)
        after_favicon = content[favicon_pos + len(CLEAN_FAVICON):]
        if 'mc.yandex.ru/metrika' not in after_favicon[:200]:
            # Metrika missing after favicon — insert it
            content = content.replace(CLEAN_FAVICON, CLEAN_FAVICON + '\n' + YM_BLOCK, 1)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    html_files = sorted(BASE.rglob('*.html'))
    fixed = 0
    skipped = 0

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
            print(f'  ERROR: {f.relative_to(BASE)}: {e}')

    print(f'\nDone. Fixed: {fixed}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
