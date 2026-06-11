import zipfile, re

docx_path = r"D:\гипноз\МК_Продвинутые_техники_гипноза_mp4_1.docx"
with zipfile.ZipFile(docx_path) as z:
    xml = z.read('word/document.xml').decode('utf-8')

text = re.sub(r'<[^>]+>', '', xml)
text = re.sub(r'\s+', ' ', text)

pattern = r'\[(\d+:\d+\.\d+ - \d+:\d+\.\d+)\]\s*\(SPEAKER_\d+\)\s*(.*?)(?=\[\d+:\d+\.\d+ - \d+:\d+\.\d+\]|$)'
matches = re.findall(pattern, text, re.DOTALL)

keywords = ['наведени', 'элман', 'переходим', 'фракцинаци', 'амнези', 'каталепси', 
            'мгновен', 'шок', 'феномен', 'галюцинац', 'регресси', 'прямое внушен',
            'стабилизаци', 'сопротивлени', 'пре-ток', 'преток', 'pre-talk',
            'спайк', 'спи"', 'углублен', 'терапи', 'уверенност', 'привычк',
            'стресс', 'эстрадн', 'цыган', 'этик', 'трудн', 'клиент', 'комплаен',
            'договор', 'запрещенн', 'соннамбул', 'тест', 'проверк']

for ts, snippet in matches:
    clean = snippet.strip()[:150].replace('\n', ' ')
    for kw in keywords:
        if kw.lower() in clean.lower():
            print(f"[{ts}] {clean}")
            break
