import zipfile, re

docx_path = r"D:\гипноз\МК_Продвинутые_техники_гипноза_mp4_1.docx"
with zipfile.ZipFile(docx_path) as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', '', xml).replace('\n', ' ').replace('\r', ' ')
text = re.sub(r'\s+', ' ', text)

# Segment 3 is [11:52.78 - 13:04.95]
# Segment end of 2 is at ~10:08, segment 3 starts at 11:52
# Let me extract the exact segment
pattern = r'\[(\d+:\d+\.\d+) - (\d+:\d+\.\d+)\]\s*\(SPEAKER_\d+\)\s*(.*?)(?=\[\d+:\d+\.\d+ - \d+:\d+\.\d+\]|$)'
segments = re.findall(pattern, text, re.DOTALL)

# Find segment 3 (index 3, which covers 11:52-13:04)
# Actually the start of "what is hypnosis" is at segment 10 [11:52.78 - 13:04.95]
for i, (s, e, content) in enumerate(segments):
    if s.startswith("11:52"):
        clean = content.strip()
        print(f"=== SEGMENT {i}: {s} - {e} ===")
        print(clean)
        print(f"\n--- Length: {len(clean)} chars ---")
        break
