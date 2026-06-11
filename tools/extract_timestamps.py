import zipfile, re

docx_path = r"D:\гипноз\МК_Продвинутые_техники_гипноза_mp4_1.docx"
with zipfile.ZipFile(docx_path) as z:
    xml = z.read('word/document.xml').decode('utf-8')

text = re.sub(r'<[^>]+>', '', xml)
# Remove excessive whitespace
text = re.sub(r'\s+', ' ', text)

# Find timestamp blocks
pattern = r'\[(\d+:\d+\.\d+ - \d+:\d+\.\d+)\]\s*\(SPEAKER_\d+\)\s*(.*?)(?=\[\d+:\d+\.\d+ - \d+:\d+\.\d+\]|$)'
matches = re.findall(pattern, text, re.DOTALL)

for i, (ts, snippet) in enumerate(matches):
    clean = snippet.strip()[:120].replace('\n', ' ')
    print(f"[{ts}] {clean}")
