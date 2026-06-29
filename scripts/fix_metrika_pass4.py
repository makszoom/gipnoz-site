#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOURTH PASS: Fix regex that accidentally ate gtag.js.
The issue was `<script[^>]*>.*?mc\.yandex\.ru/metrika/tag\.js.*?</script>` with DOTALL
matched from a gtag <script> tag all the way to the first Metrika URL in a LATER script.

Fix: match Metrika script blocks by looking for mc.yandex.ru/metrika/tag.js
WITHIN the same <script>...</script> pair, not across tags.
"""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# Match a complete <script> block that contains mc.yandex.ru/metrika/tag.js
# Use a negative lookahead to ensure we don't cross </script> boundaries
METRIKA_SCRIPT = re.compile(
    r'<script[^>]*>\s*(?:(?!</script>)[\s\S])*?mc\.yandex\.ru/metrika/tag\.js(?:(?!</script>)[\s\S])*?</script>\s*',
    re.IGNORECASE
)

# Match <noscript> blocks with mc.yandex.ru/watch
METRIKA_NOSCRIPT = re.compile(
    r'<noscript>.*?mc\.yandex\.ru/watch/109680006.*?</noscript>\s*',
    re.DOTALL | re.IGNORECASE
)

# Match any remaining Yandex.Metrika HTML comments
YM_COMMENT = re.compile(
    r'<!--\s*/?Yandex\.Metrika\s*counter\s*-->\s*',
    re.IGNORECASE
)

# Match broken favicon fragments
BROKEN_FAVICON = re.compile(
    r'<link\s+rel="icon"\s+href="data:image/svg\+xml.*?</svg>">\s*',
    re.DOTALL
)

# Match orphaned SVG fragments
ORPHANED_SVG = re.compile(
    r'<text\s+y=%22.*?</text></svg>">\s*',
    re.DOTALL
)

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

    # 1. Remove ALL Metrika <script> blocks (with or without comments)
    content = METRIKA_SCRIPT.sub('', content)

    # 2. Remove ALL Metrika <noscript> blocks
    content = METRIKA_NOSCRIPT.sub('', content)

    # 3. Remove any orphaned Yandex.Metrika HTML comments
    content = YM_COMMENT.sub('', content)

    # 4. Remove broken favicon fragments
    content = BROKEN_FAVICON.sub('', content)

    # 5. Remove orphaned SVG fragments
    content = ORPHANED_SVG.sub('', content)

    # 6. Insert clean favicon + Metrika before </head>
    if CLEAN_FAVICON not in content:
        content = content.replace('</head>', CLEAN_FAVICON + '\n' + YM_BLOCK + '\n</head>', 1)
    else:
        favicon_pos = content.find(CLEAN_FAVICON)
        after = content[favicon_pos + len(CLEAN_FAVICON):]
        if 'mc.yandex.ru/metrika' not in after[:200]:
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
