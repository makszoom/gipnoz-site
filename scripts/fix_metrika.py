#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Yandex.Metrika across all HTML files.
- EN files: remove Metrika completely
- RU files: update to clean parameters

Uses line-based approach to handle all formatting variants.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# New clean Metrika block for RU files
RU_METRIKA = '''<!-- Yandex.Metrika counter -->
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


def is_en_file(filepath):
    rel = os.path.relpath(filepath, BASE_DIR)
    return rel.startswith('en' + os.sep)


def find_metrika_block(lines):
    """Find start and end line indices of Metrika block.
    Returns (start_idx, end_idx) or None.
    """
    n = len(lines)
    start = None
    end = None

    for i, line in enumerate(lines):
        # Look for metrika tag.js or counter comment
        if start is None and ('mc.yandex.ru/metrika/tag.js' in line or 'Yandex.Metrika counter' in line):
            start = i
            # Check if previous line is the comment
            if i > 0 and 'Yandex.Metrika counter' in lines[i-1]:
                start = i - 1

        if start is not None and '</noscript>' in line:
            end = i
            # Check if this line also has <script>...theme right after
            # Actually just return end here, theme script is separate
            break

    if start is not None and end is not None:
        return (start, end)
    return None


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    block = find_metrika_block(lines)
    if not block:
        return False

    start_idx, end_idx = block

    # For EN: remove the block
    # For RU: replace with clean block
    is_en = is_en_file(filepath)

    if is_en:
        new_lines = lines[:start_idx] + lines[end_idx + 1:]
        action = 'removed'
    else:
        # Replace block with clean RU version
        new_lines = lines[:start_idx] + [RU_METRIKA + '\n'] + lines[end_idx + 1:]
        action = 'updated'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f'  {action}: {os.path.relpath(filepath, BASE_DIR)}')
    return True


def main():
    print('Fixing Yandex.Metrika (line-based)...\n')

    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in {'.git', 'scripts', 'assets'}]
        for fname in files:
            if fname.endswith('.html'):
                html_files.append(os.path.join(root, fname))

    count = 0
    for filepath in sorted(html_files):
        if process_file(filepath):
            count += 1

    print(f'\nDone. {count} files processed.')


if __name__ == '__main__':
    main()
