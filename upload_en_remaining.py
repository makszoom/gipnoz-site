#!/usr/bin/env python3
"""Upload remaining EN videos to Bunny Stream (resume from B06)."""
import json, subprocess, sys, time, os

LIBRARY_ID = "684480"
ACCESS_KEY = "d715ffb9-265a-4118-9164a48178c1-e91a-49c5"
BASE_URL = "https://video.bunnycdn.com/library"
VIDEO_DIR = "D:/гипноз/видео для уроков/Jerry Kein"

# Already uploaded: B01-B05. Resume from B06.
videos = [
    ("B06 - Waking Hypnosis & Emotional Triggers", "B06 - Waking Hypnosis & Emotional Triggers.mp4"),
    ("B07 - Deepening Techniques", "B07 - Deepening Techniques.mp4"),
    ("B08 - Elman Induction Live Demo", "B08 - Elman Induction Live Demo.mp4"),
    ("B09 - Building a Practice", "B09 - Building a Practice.mp4"),
    ("B10 - Self-Hypnosis", "B10 - Self-Hypnosis.mp4"),
    ("B11 - Pain Control & Anesthesia", "B11 - Pain Control & Anesthesia.mp4"),
    ("B12 - The Coma State", "B12 - The Coma State.mp4"),
    ("Adv1 - Rapid & Instant Inductions", "Adv1 - Rapid & Instant Inductions.mp4"),
    ("Adv2 - Universal Therapy - Case Study Jane", "Adv2 - Universal Therapy - Case Study Jane.mp4"),
    ("Adv3 - Emotional Release & Regression", "Adv3 - Emotional Release & Regression.mp4"),
    ("Adv4 - Marketing & Age Regression", "Adv4 - Marketing & Age Regression.mp4"),
    ("Adv5 - Forgiveness Therapy", "Adv5 - Forgiveness Therapy.mp4"),
    ("Adv6 - Past Life Regression", "Adv6 - Past Life Regression.mp4"),
]

# First check which already exist in library
print("=== Checking existing videos in library ===")
result = subprocess.run([
    "curl", "-s", "--request", "GET",
    f"{BASE_URL}/{LIBRARY_ID}/videos?page=1&perPage=100",
    "--header", f"AccessKey: {ACCESS_KEY}",
    "--header", "Accept: application/json"
], capture_output=True, text=True, timeout=30)
existing = json.loads(result.stdout)
existing_titles = {v.get("title", "") for v in existing.get("videos", existing.get("items", []))}
print(f"Existing videos in library: {len(existing_titles)}")

for title, filename in videos:
    if title in existing_titles:
        print(f"  SKIP (already exists): {title}")
        continue
    
    filepath = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filename}")
        continue
    
    filesize = os.path.getsize(filepath)
    size_mb = filesize / (1024 * 1024)
    print(f"\n  Uploading: {title} ({size_mb:.0f} MB)...", end=" ", flush=True)
    
    # Create video object
    create = subprocess.run([
        "curl", "-s", "--request", "POST",
        f"{BASE_URL}/{LIBRARY_ID}/videos",
        "--header", f"AccessKey: {ACCESS_KEY}",
        "--header", "Accept: application/json",
        "--header", "Content-Type: application/json",
        "--data", json.dumps({"title": title})
    ], capture_output=True, text=True, timeout=30)
    created = json.loads(create.stdout)
    guid = created.get("guid", "")
    if not guid:
        print(f"FAIL create: {created}")
        continue
    print(f"created ({guid[:8]}...) ", end="", flush=True)
    
    # Upload file
    start = time.time()
    upload = subprocess.run([
        "curl", "-s", "--request", "PUT",
        f"{BASE_URL}/{LIBRARY_ID}/videos/{guid}",
        "--header", f"AccessKey: {ACCESS_KEY}",
        "--header", "Accept: application/json",
        "--header", "Content-Type: application/octet-stream",
        "--data-binary", f"@{filepath}",
        "--write-out", "\nHTTP_CODE:%{http_code}",
        "--max-time", "900"
    ], capture_output=True, text=True, timeout=900)
    elapsed = time.time() - start
    
    output = upload.stdout.strip()
    parts = output.rsplit("\nHTTP_CODE:", 1)
    http_code = parts[1] if len(parts) > 1 else "?"
    
    if http_code == "200":
        print(f"OK ({elapsed:.0f}s)")
    else:
        print(f"HTTP {http_code} ({elapsed:.0f}s)")
        try:
            j = json.loads(parts[0])
            print(f"    Response: {j}")
        except:
            print(f"    Response: {parts[0][:200]}")

print("\n=== Done ===")
