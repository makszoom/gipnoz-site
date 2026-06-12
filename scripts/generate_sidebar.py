#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate static lesson sidebars for all lesson HTML files.
Removes dependency on js/lesson-sidebar.js by embedding sidebar HTML directly.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── RU module map ──
RU_MODULES = {
    'module-0': {
        'title': 'Модуль 0 — Введение',
        'lang': 'ru',
        'lessons': [
            ['lesson-0-1.html', '0.1 — Что такое гипноз на самом деле'],
            ['lesson-0-2.html', '0.2 — Как работает сознание и подсознание'],
            ['lesson-0-3.html', '0.3 — Кому подходит гипноз. Тест на внушаемость'],
            ['lesson-0-4.html', '0.4 — Структура курса и чего ожидать'],
        ]
    },
    'module-1': {
        'title': 'Модуль 1 — Базовые техники',
        'lang': 'ru',
        'lessons': [
            ['lesson-1-1.html', '1.1 — Гипнотический договор и подготовка'],
            ['lesson-1-2.html', '1.2 — Каталепсия век и body scan'],
            ['lesson-1-3.html', '1.3 — Фракцинация и проверка руки'],
            ['lesson-1-4.html', '1.4 — Амнезия чисел и порог сомнамбулизма'],
            ['lesson-1-5.html', '1.5 — Проверки: каталепсия век и анальгезия'],
            ['lesson-1-6.html', '1.6 — Сокращённые версии и углубление'],
        ]
    },
    'module-2': {
        'title': 'Модуль 2 — Стабилизация',
        'lang': 'ru',
        'lessons': [
            ['lesson-2-1.html', '2.1 — Стабилизация сомнамбулизма'],
            ['lesson-2-2.html', '2.2 — Скрытый тест фракцинацией'],
            ['lesson-2-3.html', '2.3 — Работа с сопротивлением'],
            ['lesson-2-4.html', '2.4 — Прямые внушения: базовый протокол'],
            ['lesson-2-5.html', '2.5 — Пост-гипнотическое окно'],
        ]
    },
    'module-3': {
        'title': 'Модуль 3 — Мгновенный гипноз',
        'lang': 'ru',
        'lessons': [
            ['lesson-3-1.html', '3.1 — Четыре принципа мгновенного наведения'],
            ['lesson-3-2.html', '3.2 — Быстрое наведение через руку'],
            ['lesson-3-3.html', '3.3 — Наведение стоя и баланс'],
            ['lesson-3-4.html', '3.4 — Вербальный шок и шок от отсутствия шока'],
            ['lesson-3-5.html', '3.5 — Феномены в быстром гипнозе'],
            ['lesson-3-6.html', '3.6 — Когда использовать: контекст и безопасность'],
        ]
    },
    'module-4': {
        'title': 'Модуль 4 — Феномены',
        'lang': 'ru',
        'lessons': [
            ['lesson-4-1.html', '4.1 — Что такое феномены и зачем они нужны'],
            ['lesson-4-2.html', '4.2 — Каталепсия и анальгезия'],
            ['lesson-4-3.html', '4.3 — Амнезия: виды и техники'],
            ['lesson-4-4.html', '4.4 — Постгипнотические внушения и реиндукция'],
            ['lesson-4-5.html', '4.5 — Галлюцинации с открытыми и закрытыми глазами'],
            ['lesson-4-6.html', '4.6 — Введение в регрессию'],
        ]
    },
    'module-5': {
        'title': 'Модуль 5 — Терапия',
        'lang': 'ru',
        'lessons': [
            ['lesson-5-1.html', '5.1 — Три вопроса клиенту'],
            ['lesson-5-2.html', '5.2 — Четыре конструкции построения внушения'],
            ['lesson-5-3.html', '5.3 — Закон компаундинга и усиление'],
            ['lesson-5-4.html', '5.4 — Прямое внушение vs регрессия'],
            ['lesson-5-5.html', '5.5 — Структура сессии и контекст работы'],
        ]
    },
    'module-6': {
        'title': 'Модуль 6 — Продвинутый уровень',
        'lang': 'ru',
        'lessons': [
            ['lesson-6-1.html', '6.1 — Эстрадный гипноз'],
            ['lesson-6-2.html', '6.2 — «Цыганский гипноз»'],
            ['lesson-6-3.html', '6.3 — Трудные клиенты и ситуации'],
            ['lesson-6-4.html', '6.4 — Скорость vs глубина'],
            ['lesson-6-5.html', '6.5 — Этика и границы'],
        ]
    },
}

# ── EN module map ──
EN_MODULES = {
    'beginner': {
        'title': 'Beginner-Intermediate Course',
        'lang': 'en',
        'lessons': [
            ['lesson-01.html', 'B01 — Introduction &amp; History of Hypnosis'],
            ['lesson-02.html', 'B02 — Core Concepts: Rapport, Somnambulism &amp; Suggestibility'],
            ['lesson-03.html', 'B03 — Bypassing the Critical Factor &amp; Emergency Anesthesia'],
            ['lesson-04.html', 'B04 — Trance Levels &amp; Coma State Management'],
            ['lesson-05.html', 'B05 — Chevreul Pendulum &amp; Ideomotor Responses'],
            ['lesson-06.html', 'B06 — Waking Hypnosis &amp; Emotional Triggers'],
            ['lesson-07.html', 'B07 — Deepening: Counting, Hallucinations &amp; Post-Induction'],
            ['lesson-08.html', 'B08 — Elman Induction: Live Demo &amp; Step-by-Step'],
            ['lesson-09.html', 'B09 — Building a Practice: Referrals &amp; Marketing'],
            ['lesson-10.html', 'B10 — Self-Hypnosis'],
            ['lesson-11.html', 'B11 — Pain Control &amp; Anesthesia'],
            ['lesson-12.html', 'B12 — Working with Children &amp; The Coma State'],
        ]
    },
    'advanced': {
        'title': 'Advanced Course',
        'lang': 'en',
        'lessons': [
            ['lesson-adv1.html', 'Adv1 — Rapid &amp; Instant Inductions'],
            ['lesson-adv2.html', 'Adv2 — Universal Therapy Protocol'],
            ['lesson-adv3.html', 'Adv3 — Emotional Release &amp; Regression'],
            ['lesson-adv4.html', 'Adv4 — Marketing Your Practice &amp; Age Regression'],
            ['lesson-adv5.html', 'Adv5 — Forgiveness Therapy'],
            ['lesson-adv6.html', 'Adv6 — Past Life Regression'],
        ]
    },
}


def build_sidebar_html(module_title, lessons, current_file, lang):
    """Generate the sidebar inner HTML (progress bar + lesson list)."""
    total = len(lessons)
    current_index = next(
        (i for i, (f, _) in enumerate(lessons) if f == current_file), 0
    )
    pct = round((current_index + 1) / total * 100)

    if lang == 'ru':
        progress_text = f"Урок {current_index + 1} из {total} · {pct}%"
    else:
        progress_text = f"Lesson {current_index + 1} of {total} · {pct}%"

    lines = [
        '<div class="module-progress">',
        f'  <div class="module-progress-bar"><div class="module-progress-fill" style="width:{pct}%"></div></div>',
        f'  <div class="module-progress-text">{progress_text}</div>',
        '</div>',
        '<ul class="lesson-sidebar-list">',
    ]
    for j, (fname, title) in enumerate(lessons):
        cls = 'lesson-sidebar-item'
        if j == current_index:
            cls += ' current'
        elif j < current_index:
            cls += ' completed'
        lines.append(
            f'  <li class="{cls}"><a href="{fname}"><span class="lesson-sidebar-title">{title}</span></a></li>'
        )
    lines.append('</ul>')
    return '\n'.join(lines)


def build_toggle_text(module_title, lessons, current_file, lang):
    current_index = next(
        (i for i, (f, _) in enumerate(lessons) if f == current_file), 0
    )
    total = len(lessons)
    if lang == 'ru':
        return f"{module_title} · {current_index + 1} из {total}"
    else:
        return f"{module_title} · {current_index + 1} of {total}"


def remove_sidebar_js(content):
    """Remove any <script src="...lesson-sidebar.js"> references."""
    return re.sub(
        r'<script[^>]*src="[^"]*lesson-sidebar\.js"[^>]*>\s*</script>\s*',
        '',
        content,
        flags=re.IGNORECASE,
    )


def ensure_toggle_sidebar_func(content):
    """Add toggleSidebar() to inline script if missing."""
    if 'function toggleSidebar(' in content:
        return content
    func = (
        '\nfunction toggleSidebar(){'
        'var btn=document.querySelector(".sidebar-toggle");'
        'var panel=document.querySelector(".sidebar-mobile-panel");'
        'if(!btn||!panel)return;'
        'btn.classList.toggle("open");'
        'panel.classList.toggle("open");'
        '}'
    )
    # Try to insert after toggleMenu or toggleTheme
    match = re.search(r'(function toggle(?:Menu|Theme)\([^)]*\)[^{]*\{[^}]*\})', content)
    if match:
        insert_pos = match.end()
        return content[:insert_pos] + func + content[insert_pos:]
    # Fallback: insert before </script> near </body>
    match = re.search(r'(</script>\s*</body>)', content)
    if match:
        insert_pos = match.start()
        script_block = f'<script>{func}\n</script>'
        return content[:insert_pos] + script_block + '\n' + content[insert_pos:]
    return content


def wrap_with_layout(content, sidebar_html, toggle_text):
    """Wrap <main>...</main> with lesson-layout + sidebar."""
    main_open = re.search(r'(<main[^>]*>)', content)
    if not main_open:
        raise ValueError("No <main> tag found")
    main_start = main_open.start()

    main_close = content.find('</main>', main_start)
    if main_close == -1:
        raise ValueError("No closing </main> found")
    main_close_end = main_close + len('</main>')

    main_block = content[main_start:main_close_end]

    layout_block = (
        '<div class="lesson-layout">\n\n'
        '  <!-- Mobile sidebar toggle -->\n'
        f'  <button class="sidebar-toggle" onclick="toggleSidebar()">{toggle_text}</button>\n'
        '  <div class="sidebar-mobile-panel">\n'
        f'{sidebar_html}\n'
        '  </div>\n\n'
        '  <aside class="lesson-sidebar">\n'
        f'{sidebar_html}\n'
        '  </aside>\n\n'
        f'{main_block}\n'
        '</div>'
    )

    return content[:main_start] + layout_block + content[main_close_end:]


def update_existing_layout(content, sidebar_html, toggle_text):
    """Update sidebar contents in a file that already has lesson-layout."""
    # Update aside
    content = re.sub(
        r'(<aside class="lesson-sidebar">)\s*.*?(\s*</aside>)',
        lambda m: f'{m.group(1)}\n{sidebar_html}\n{m.group(2)}',
        content,
        count=1,
        flags=re.DOTALL,
    )
    # Update mobile panel
    content = re.sub(
        r'(<div class="sidebar-mobile-panel">)\s*.*?(\s*</div>)',
        lambda m: f'{m.group(1)}\n{sidebar_html}\n{m.group(2)}',
        content,
        count=1,
        flags=re.DOTALL,
    )
    # Update toggle button text
    content = re.sub(
        r'(<button class="sidebar-toggle"[^>]*>).*?(</button>)',
        lambda m: f'{m.group(1)}{toggle_text}{m.group(2)}',
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def process_file(filepath, module_key, module_data):
    """Process a single lesson HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    current_file = os.path.basename(filepath)
    lessons = module_data['lessons']
    lang = module_data['lang']

    sidebar_html = build_sidebar_html(
        module_data['title'], lessons, current_file, lang
    )
    toggle_text = build_toggle_text(
        module_data['title'], lessons, current_file, lang
    )

    # Remove old JS dependency
    content = remove_sidebar_js(content)

    if '<div class="lesson-layout">' in content:
        # Already has layout — update only
        content = update_existing_layout(content, sidebar_html, toggle_text)
    else:
        # Need to wrap main in layout
        content = wrap_with_layout(content, sidebar_html, toggle_text)

    # Ensure toggleSidebar function exists
    content = ensure_toggle_sidebar_func(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK {os.path.relpath(filepath, BASE_DIR)}")


def main():
    print("Generating static sidebars...\n")

    # RU modules
    for mod_key, mod_data in RU_MODULES.items():
        print(f"Module: {mod_data['title']}")
        mod_dir = os.path.join(BASE_DIR, 'modules', mod_key)
        for fname, _ in mod_data['lessons']:
            filepath = os.path.join(mod_dir, fname)
            if os.path.exists(filepath):
                process_file(filepath, mod_key, mod_data)
            else:
                print(f"  MISSING: {filepath}")

    # EN modules
    for mod_key, mod_data in EN_MODULES.items():
        print(f"Module: {mod_data['title']}")
        mod_dir = os.path.join(BASE_DIR, 'en', mod_key)
        for fname, _ in mod_data['lessons']:
            filepath = os.path.join(mod_dir, fname)
            if os.path.exists(filepath):
                process_file(filepath, mod_key, mod_data)
            else:
                print(f"  MISSING: {filepath}")

    print("\nDone.")


if __name__ == '__main__':
    main()
