#!/usr/bin/env python3
"""
Batch-fill all EN lesson pages with full text content.
Written content is based on analysis of original Kein .srt subtitles.
"""
import os, re

EN = r"C:\Users\valter\hermes-projects\gipnoz-site\en"

def lesson_template(title, duration, summary_paras, sections, takeaway, practice):
    """Build the <main> block HTML for a lesson page."""
    secs = []
    for h, ps in sections:
        secs.append(f'    <h3 style="font-size:1rem;margin:20px 0 10px;color:var(--accent);">{h}</h3>')
        for p in ps:
            secs.append(f'    <p style="margin-bottom:12px;">{p}</p>')
    
    intro_ps = '\n'.join(f'    <p style="margin-bottom:12px;">{p}</p>' for p in summary_paras)

    if practice:
        prac = practice
    else:
        prac = ''

    takeaway_block = f'''    <div class="mt-24" style="background:var(--accent-dim);padding:16px;border-radius:var(--radius-sm);">
      <p style="font-size:.9rem;color:var(--text-muted);"><strong>🧠 Key Takeaway:</strong> {takeaway}</p>
    </div>'''

    return f'''<main>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;font-size:.85rem;">
    <a href="../modules.html" style="color:var(--text-muted);">&larr; All lessons</a>
    <a href="../beginner.html" style="color:var(--text-muted);">&larr; Beginner-Intermediate Course</a>
  </div>

  <span class="tag tag-free">Free</span>
  <h1 style="font-size:1.6rem;margin:12px 0 8px;">{title}</h1>
  <p style="color:var(--text-muted);margin-bottom:24px;">~{duration} minutes</p>

  <div class="video-container">
    <div class="video-placeholder">
      <div style="font-size:3rem;margin-bottom:12px;">🎬</div>
      <p>Video coming soon</p>
      <p style="font-size:.85rem;color:var(--text-muted);">This lesson video is being prepared.</p>
    </div>
  </div>

  <!-- LESSON CONTENT -->
  <div class="card" style="margin-bottom:24px;">

    <h2 style="font-size:1.1rem;margin-bottom:12px;">About This Lesson</h2>
{intro_ps}

{chr(10).join(secs)}

{takeaway_block}
  </div>

{prac}

  <!-- LESSON NAVIGATION -->
  <div class="lesson-nav">
    <a href="lesson-04.html" class="lesson-nav-link">&larr; Trance Levels &amp; The Coma Story</a>
    <a href="lesson-06.html" class="lesson-nav-link">Waking Hypnosis &amp; Emotional Triggers &rarr;</a>
  </div>
</main>'''


# Actually, let me just use the simpler approach: patch the <main> block for each file.
# I already have the content written. Let me create a dict of patches.

# B05
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

  <!-- LESSON CONTENT -->
  <div class="card" style="margin-bottom:24px;">

    <h2 style="font-size:1.1rem;margin-bottom:12px;">About This Lesson</h2>
    <p style="margin-bottom:12px;">The Chevreul Pendulum is one of the simplest yet most convincing demonstrations that the subconscious mind exists and can be directly influenced. Kein uses it as both a teaching tool and an induction method. When the pendulum moves — seemingly on its own — the subject experiences undeniable proof that something beyond their conscious control is operating.</p>
    <p style="margin-bottom:12px;">This lesson is a hands-on workshop. Kein demonstrates the pendulum with volunteers, has the class practice in pairs, and then uses the pendulum state as a launchpad into deep formal trance. The core insight: when the pendulum swings, the critical factor has already been bypassed — the hypnosis has already begun.</p>

    <h3 style="font-size:1rem;margin:20px 0 10px;color:var(--accent);">The Pendulum Demonstration</h3>
    <p style="margin-bottom:12px;">Kein calls up a volunteer and hands her a weighted pendulum. He tells her to hold it steady and simply imagine it swinging forward and back. Within moments, the pendulum begins to swing. He asks her to mentally command it to stop — it stops. She mentally commands it to swing left and right — it obeys. Circles, figure-eights — the pendulum does whatever the subconscious decides. When asked if she's doing it consciously, she says, "No, I'm not doing anything!" The pendulum is moving purely through unconscious ideomotor responses.</p>
    <p style="margin-bottom:12px;">Kein then demonstrates a paradoxical effect: he tells the volunteer to mentally try to stop the pendulum — and the harder she tries, the faster it swings. This proves that conscious effort activates the wrong system. The subconscious responds best when the conscious mind steps aside.</p>

    <h3 style="font-size:1rem;margin:20px 0 10px;color:var(--accent);">From Pendulum to Trance</h3>
    <p style="margin-bottom:12px;">Once the pendulum is moving and the critical factor is bypassed, Kein transitions directly into formal hypnosis. He says: "Sleep — complete relaxation." The volunteer drops into deep trance on the spot. The pendulum has done the work of induction without the subject even realizing it.</p>
    <p style="margin-bottom:12px;">This is a powerful lesson: any technique that produces an observable subconscious response (pendulum, hand levitation) can serve as both a proof-of-concept and an induction. The subject experiences the reality of the subconscious, making them far more receptive to further suggestions.</p>

    <h3 style="font-size:1rem;margin:20px 0 10px;color:var(--accent);">Classroom Practice</h3>
    <p style="margin-bottom:12px;">Kein has the class work in pairs: one person acts as "operator" giving instructions (forward-back, stop, left-right, circle), while the other works the pendulum. Then they switch. This builds confidence in both roles — the subject learns to trust their subconscious, and the operator learns how to phrase suggestions clearly.</p>

    <div class="mt-24" style="background:var(--accent-dim);padding:16px;border-radius:var(--radius-sm);">
      <p style="font-size:.9rem;color:var(--text-muted);"><strong>🧠 Key Takeaway:</strong> The pendulum is not a toy — it's a direct line to the subconscious. When the pendulum moves, the critical factor is gone. Use it as an induction, as a proof, or any time you need to show someone that their own mind can do things they didn't think possible.</p>
    </div>
  </div>

  <!-- PRACTICE SECTION -->
  <div class="card" style="margin-bottom:24px;">
    <h2 style="font-size:1.1rem;margin-bottom:12px;">📝 Practice: The Pendulum</h2>
    <p style="margin-bottom:12px;">Make a simple pendulum using a string and a weighted object (a ring, a key, a paperclip). Practice on yourself first.</p>
    <div class="script-block">
      <h4>Self-Pendulum Script</h4>
      <p>"Hold the pendulum steady. Take a breath. Now just imagine the pendulum swinging forward and back. Don't make it move — just imagine it. Let your subconscious take over. Forward and back. Good. Now mentally say 'stop.' Notice how it stops. Now imagine it swinging in a circle. Let it go faster. Now mentally say 'stop' again. It stops. You've just communicated with your subconscious. It's real, it's listening, and it's ready to work with you."</p>
    </div>
  </div>

  <!-- LESSON NAVIGATION -->
  <div class="lesson-nav">
    <a href="lesson-04.html" class="lesson-nav-link">&larr; Trance Levels &amp; The Coma Story</a>
    <a href="lesson-06.html" class="lesson-nav-link">Waking Hypnosis &amp; Emotional Triggers &rarr;</a>
  </div>
</main>"""

print(b05_content[:100])
