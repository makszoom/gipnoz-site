import zipfile, re

docx_path = r"D:\гипноз\МК_Продвинутые_техники_гипноза_mp4_1.docx"
with zipfile.ZipFile(docx_path) as z:
    xml = z.read('word/document.xml').decode('utf-8')

text = re.sub(r'<[^>]+>', '', xml)
text = re.sub(r'\s+', ' ', text)

# Get all timestamp blocks with content
pattern = r'\[(\d+:\d+\.\d+ - \d+:\d+\.\d+)\]\s*\(SPEAKER_\d+\)\s*(.*?)(?=\[\d+:\d+\.\d+ - \d+:\d+\.\d+\]|$)'
matches = re.findall(pattern, text, re.DOTALL)

# Key transitions to look for
transitions = {
    'элман': 'Elman induction starts',
    'наведение элман': 'Start of Elman',
    'пре-ток': 'Pre-talk section',
    'переходим к наведению': 'Moving to induction',
    'теперь мы переходим': 'Transition point',
    'фракцинац': 'Fractionation',
    'амнези': 'Amnesia',
    'каталепси': 'Catalepsy',
    'анальгези': 'Analgesia',
    'мгновен': 'Instant/rapid',
    'четыре принцип': '4 principles',
    'феномен': 'Phenomena',
    'регресси': 'Regression',
    'прямое внушен': 'Direct suggestion',
    'спайк': 'Spike theory',
    'углублен': 'Deepening',
    'терапи': 'Therapy',
    'уверенност': 'Confidence',
    'привычк': 'Habits',
    'стресс': 'Stress',
    'эстрадн': 'Stage hypnosis',
    'цыган': 'Gypsy hypnosis',
    'этик': 'Ethics',
    'трудн клиент': 'Difficult clients',
    'сопротивлен': 'Resistance',
    'соннамбул': 'Somnambulism',
    'тест': 'Test',
    'проверк': 'Check/test',
    'сокращен': 'Shortened version',
    'комплаен': 'Compliance',
    'договор': 'Contract',
    'запрещенн': 'Forbidden words',
    'спи"': 'Sleep command',
    'рук': 'Hand (induction)',
    'баланс': 'Balance',
    'стоя': 'Standing induction',
    'шок': 'Shock induction',
    'галлюцинац': 'Hallucination',
    'афази': 'Aphasia',
    'постгипноти': 'Post-hypnotic',
    'реиндукц': 'Reinduction',
    'заверш': 'Closing/summary',
    'вопрос': 'Q&A',
    'кофе': 'Coffee break',
    'перерыв': 'Break',
}

# Also look for natural transition phrases
transition_phrases = [
    'теперь мы', 'сейчас я', 'давайте', 'переходим к',
    'следующий', 'начинаем', 'вторая часть', 'продолжаем',
    'я покажу', 'я продемонстрирую', 'я хочу показать',
    'мы с вами', 'обратите внимание', 'важно понимать',
    'в конце', 'резюме', 'подведем итог'
]

print("=== ALL TIMESTAMP SEGMENTS ===")
for i, (ts, snippet) in enumerate(matches):
    clean = snippet.strip()[:200].replace('\n', ' ')
    
    # Mark if contains any key transition
    markers = []
    for kw, label in transitions.items():
        if kw.lower() in clean.lower():
            markers.append(label)
    
    # Mark if starts with transition phrase
    first_words = clean.lower()[:30]
    for phrase in transition_phrases:
        if phrase in first_words:
            if 'q&a' not in [m.lower() for m in markers]:
                markers.append(f'→ {phrase}')
    
    marker_str = f'  **{", ".join(markers)}**' if markers else ''
    
    # Show every segment with its number for reference
    print(f'{i:3d}. [{ts}]{marker_str}')
    print(f'     {clean[:150]}')
    print()
