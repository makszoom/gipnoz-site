#!/usr/bin/env python3
"""Generate full lesson content for all EN Kein lesson pages (B05-B12, Adv1-Adv6)."""
import os, re, json

EN = r"C:\Users\valter\hermes-projects\gipnoz-site\en"

def patch_file(filepath, old, new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old not in content:
        # Try fuzzy: find a unique substring
        lines = old.split('\n')
        first_line = lines[0].strip()
        idx = content.find(first_line)
        if idx >= 0:
            # Found anchor, replace from anchor to matching end
            end_marker = lines[-1].strip()
            end_idx = content.find(end_marker, idx)
            if end_idx >= 0:
                end_idx += len(end_marker)
                content = content[:idx] + new + content[end_idx:]
            else:
                print(f"  WARN: anchor '{first_line[:40]}' found but end '{end_marker[:40]}' not matched")
                return False
        else:
            print(f"  FAIL: could not find '{first_line[:50]}' in {filepath}")
            return False
    else:
        content = content.replace(old, new, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# B05 - Chevreul Pendulum
b05_content = """<main>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;font-size:.85rem;">
    <a href="../modules.html" style="color:var(--text-muted);">&larr; All lessons</a>
    <a href="../beginner.html" style="color:var(--text-muted);">&larr; Beginner-Intermediate Course</a>
  </div>

  <span class="tag tag-free">Free</span>
  <h1 style="font-size:1.6rem;margin:12px 0 8px;">B05 — Chevreul Pendulum &amp; Ideomotor Responses</h1>
  <p style="color:var(--text-muted);margin-bottom:24px;">~45 minutes</p>

  <div class="video-container">
    <div class="video-placeholder">
      <div style="font-size:3rem;margin-bottom:12px;">🎬</div>
      <p>Video coming soon</p>
      <p style="font-size:.85rem;color:var(--text-muted);">This lesson video is being prepared.</p>
    </div>
  </div>

  <div class="card" style="margin-bottom:24px;">
    <h2 style="font-size:1.1rem;margin-bottom:12px;">About This Lesson</h2>
    <p style="margin-bottom:12px;">The Chevreul Pendulum is one of the simplest yet most convincing demonstrations that the subconscious mind exists and can be directly influenced. Kein uses it as both a teaching tool and an induction method. When the pendulum moves — seemingly on its own — the subject experiences undeniable proof that something beyond their conscious control is operating.</p>
    <p style="margin-bottom:12px;">This lesson is a hands-on workshop. Kein demonstrates the pendulum with volunteers, has the class practice in pairs, and then uses the pendulum state as a launchpad into deep formal trance. The core insight: when the pendulum swings, the critical factor has already been bypassed.</p>

    <h3 style="font-size:1rem;margin:20px 0 10px;color:var(--accent);">The Pendulum Demonstration</h3>
    <p style="margin-bottom:12px;">Kein calls up a volunteer and hands her a weighted pendulum. He tells her to hold it steady and simply imagine it swinging forward and back. Within moments, the pendulum begins to swing. He asks her to mentally command it to stop — it stops. Circles, figure-eights — the pendulum does whatever the subconscious decides. When asked if she's doing it consciously, she says, "No, I'm not doing anything!"</p>
    <p style="margin-bottom:12px;">Kein then demonstrates a paradoxical effect: he tells the volunteer to mentally try to stop the pendulum — and the harder she tries, the faster it swings. This proves that conscious effort activates the wrong system. The subconscious responds best when the conscious mind steps aside.</p>

    <h3 style="font-size:1rem;margin:20px 0 10px;color:var(--accent);">From Pendulum to Trance</h3>
    <p style="margin-bottom:12px;">Once the pendulum is moving and the critical factor is bypassed, Kein transitions directly into formal hypnosis with a single command: "Sleep — complete relaxation." The volunteer drops into deep trance on the spot. The pendulum has done the work of induction without the subject even realizing it.</p>
    <p style="margin-bottom:12px;">Any technique that produces an observable subconscious response can serve as both a proof-of-concept and an induction. The subject experiences the reality of their own subconscious, making them far more receptive.</p>

    <div class="mt-24" style="background:var(--accent-dim);padding:16px;border-radius:var(--radius-sm);">
      <p style="font-size:.9rem;color:var(--text-muted);"><strong>🧠 Key Takeaway:</strong> The pendulum is not a toy — it's a direct line to the subconscious. When the pendulum moves, the critical factor is gone. Use it as an induction, a proof, or anytime you need to show someone their own mind can do things they didn't think possible.</p>
    </div>
  </div>

  <div class="card" style="margin-bottom:24px;">
    <h2 style="font-size:1.1rem;margin-bottom:12px;">📝 Practice: The Pendulum</h2>
    <p style="margin-bottom:12px;">Make a simple pendulum using a string and a weighted object (a ring, a key, a paperclip). Practice on yourself first.</p>
    <div class="script-block">
      <h4>Self-Pendulum Script</h4>
      <p>"Hold the pendulum steady. Take a breath. Now just imagine the pendulum swinging forward and back. Don't make it move — just imagine it. Let your subconscious take over. Forward and back. Good. Now mentally say 'stop.' Notice how it stops. Now imagine it swinging in a circle. It stops. You've just communicated with your subconscious."</p>
    </div>
  </div>

  <div class="lesson-nav">
    <a href="lesson-04.html" class="lesson-nav-link">&larr; Trance Levels &amp; The Coma Story</a>
    <a href="lesson-06.html" class="lesson-nav-link">Waking Hypnosis &amp; Emotional Triggers &rarr;</a>
  </div>
</main>"""

# Apply patches
files = {
    'beginner/lesson-05.html': b05_content,
}

for relpath, new_main in files.items():
    fpath = os.path.join(EN, relpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find the old <main> block
    start = html.find('<main>')
    end = html.find('</main>', start)
    if start >= 0 and end >= 0:
        end += len('</main>')
        html = html[:start] + new_main + html[end:]
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'✅ {relpath}')
    else:
        print(f'❌ {relpath}: <main> not found')

print('\nDone!')
