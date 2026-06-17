#!/usr/bin/env python3
"""Create video objects in Bunny Stream and upload EN video files."""
import json, subprocess, sys, time, os

LIBRARY_ID = "684480"
ACCESS_KEY = "d715ffb9-265a-4118-9164a48178c1-e91a-49c5"
BASE_URL = "https://video.bunnycdn.com/library"
VIDEO_DIR = "D:/гипноз/видео для уроков/Jerry Kein"

# Map: video title -> filename
videos = [
    ("B01 - Introduction & History of Hypnosis", "B01 - Introduction & History of Hypnosis.mp4"),
    ("B02 - Core Concepts - Rapport & Somnambulism", "B02 - Core Concepts - Rapport & Somnambulism.mp4"),
    ("B03 - Bypassing the Critical Factor", "B03 - Bypassing the Critical Factor.mp4"),
    ("B04 - Trance Levels & The Coma Story", "B04 - Trance Levels & The Coma Story.mp4"),
    ("B05 - Chevreul Pendulum & Ideomotor Responses", "B05 - Chevreul Pendulum & Ideomotor Responses.mp4"),
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

def run_curl(args, desc=""):
    """Run curl and return parsed JSON response."""
    cmd = ["curl", "-s", "--request"] + args + [
        "--header", f"AccessKey: {ACCESS_KEY}",
        "--header", "Accept: application/json",
        "--write-out", "\nHTTP_CODE:%{http_code}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    output = result.stdout.strip()
    parts = output.rsplit("\nHTTP_CODE:", 1)
    body = parts[0]
    http_code = parts[1] if len(parts) > 1 else "?"
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        data = {"raw": body}
    data["_http_code"] = http_code
    return data

# Step 1: Create all video objects
print("=== Step 1: Creating video objects ===")
created = []
for title, filename in videos:
    filepath = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filename}")
        continue
    
    print(f"  Creating: {title}...", end=" ", flush=True)
    data = run_curl([
        "POST", f"{BASE_URL}/{LIBRARY_ID}/videos",
        "--header", "Content-Type: application/json",
        "--data", json.dumps({"title": title})
    ], desc=title)
    
    if data.get("success") or data.get("guid"):
        guid = data.get("guid", "?")
        print(f"OK (guid: {guid[:8]}...)")
        created.append((title, filename, guid, filepath))
    else:
        print(f"FAIL: {data}")

print(f"\n=== Created {len(created)} video objects ===")

# Step 2: Upload files
print("\n=== Step 2: Uploading files ===")
for i, (title, filename, guid, filepath) in enumerate(created, 1):
    filesize = os.path.getsize(filepath)
    size_mb = filesize / (1024 * 1024)
    print(f"  [{i}/{len(created)}] Uploading: {title} ({size_mb:.0f} MB)...", end=" ", flush=True)
    
    upload_url = f"{BASE_URL}/{LIBRARY_ID}/videos/{guid}"
    cmd = [
        "curl", "-s", "--request", "PUT", upload_url,
        "--header", f"AccessKey: {ACCESS_KEY}",
        "--header", "Accept: application/json",
        "--header", "Content-Type: application/octet-stream",
        "--data-binary", f"@{filepath}",
        "--write-out", "\nHTTP_CODE:%{http_code}",
        "--max-time", "600"
    ]
    
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    elapsed = time.time() - start
    output = result.stdout.strip()
    
    parts = output.rsplit("\nHTTP_CODE:", 1)
    body = parts[0]
    http_code = parts[1] if len(parts) > 1 else "?"
    
    if http_code == "200":
        print(f"OK ({elapsed:.0f}s)")
    else:
        print(f"HTTP {http_code} ({elapsed:.0f}s)")
        try:
            j = json.loads(body)
            print(f"    Response: {j}")
        except:
            print(f"    Response: {body[:200]}")

print("\n=== Done ===")
