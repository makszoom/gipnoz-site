#!/usr/bin/env python3
"""Replace .lesson-video placeholders with Bunny Stream iframe in EN lessons."""
import os, re

LIBRARY_ID = "685123"
SITE_DIR = "C:/Users/valter/hermes-projects/gipnoz-site"

# Map lesson HTML file -> Bunny video GUID
lesson_map = {
    # Beginner
    "en/beginner/lesson-01.html": "c78ba04e-301d-4562-a4e6-93945109c4e4",
    "en/beginner/lesson-02.html": "3f14df54-9a90-44c0-ab53-1ac885da65f1",
    "en/beginner/lesson-03.html": "9b076f74-645a-4f2b-9552-1084b028aef1",
    "en/beginner/lesson-04.html": "a9f118bb-42bf-4bf9-908e-1857fdec4d5a",
    "en/beginner/lesson-05.html": "e3f7ad96-d482-4564-9d5c-abd7894da5a6",
    "en/beginner/lesson-06.html": "152095a6-13b9-46d7-aa68-13d002ef7bb8",
    "en/beginner/lesson-07.html": "a6086b1f-a229-47d0-9853-a44b5cb33718",
    "en/beginner/lesson-08.html": "ccb826f2-d5f7-4198-a845-aacbff1989eb",
    "en/beginner/lesson-09.html": "2a370403-c63e-4598-b40f-4875846bf1eb",
    "en/beginner/lesson-10.html": "8d49df7b-a3ce-4620-a063-ccaee1deeb8d",
    "en/beginner/lesson-11.html": "b81e7197-c38a-4ea8-ac99-ed019fec6e19",
    "en/beginner/lesson-12.html": "93840b94-1399-4abf-a540-a52546364146",
    # Advanced
    "en/advanced/lesson-adv1.html": "a4c66bef-9171-4e81-8a9f-e9bfed88b321",
    "en/advanced/lesson-adv2.html": "9137e82a-424e-48be-993f-5bc25c9d7a83",
    "en/advanced/lesson-adv3.html": "844ef428-6141-409b-93eb-bbf99873f13c",
    "en/advanced/lesson-adv4.html": "0be6aede-c7bd-4ab7-a834-936058df9739",
    "en/advanced/lesson-adv5.html": "f7a884c0-22ae-4ae6-9818-d388b340bbb3",
    "en/advanced/lesson-adv6.html": "c42de11b-da67-43ea-87a3-f44ce4290b6e",
}

# The .lesson-video placeholder block to replace
# It varies slightly between files, so we match the common pattern
placeholder_pattern = re.compile(
    r'<div class="lesson-video">\s*'
    r'<div class="lesson-video-icon"></div>\s*'
    r'<h3>Video available by subscription</h3>\s*'
    r'<p>.*?</p>\s*'
    r'<a href="\.\./donate\.html" class="btn">Get Access →</a>\s*'
    r'</div>',
    re.DOTALL
)

iframe_template = '''<div class="lesson-video-player">
    <iframe src="https://iframe.mediadelivery.net/embed/{library_id}/{guid}?autoplay=false"
      loading="lazy" allow="accelerometer;gyroscope;encrypted-media;picture-in-picture"
      allowfullscreen></iframe>
  </div>'''

updated = 0
not_found = 0

for relpath, guid in lesson_map.items():
    abspath = os.path.join(SITE_DIR, relpath)
    if not os.path.exists(abspath):
        print(f"  NOT FOUND: {relpath}")
        not_found += 1
        continue
    
    with open(abspath, "r", encoding="utf-8") as f:
        content = f.read()
    
    iframe_html = iframe_template.format(library_id=LIBRARY_ID, guid=guid)
    new_content, count = placeholder_pattern.subn(iframe_html, content)
    
    if count == 0:
        print(f"  NO MATCH: {relpath}")
        not_found += 1
        continue
    
    with open(abspath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"  OK: {relpath}")
    updated += 1

print(f"\nUpdated: {updated}, Not found/matched: {not_found}")
