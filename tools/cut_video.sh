#!/bin/bash
# Cut MK video into 12 lesson segments

FFMPEG=/tmp/ffmpeg.exe
INPUT="/d/гипноз/МК Продвинутые техники гипноза.mp4"
OUTDIR="/d/гипноз/видео для уроков"

echo "=== Starting cuts ==="

# Segment 1: 00:00 - 10:08 — Pre-talk intro, 4 forbidden words
$FFMPEG -y -ss 0 -to 00:10:08 -i "$INPUT" -c copy "$OUTDIR/01-pretalk-intro.mp4"

# Segment 2: 10:08 - 25:55 — What is hypnosis, conscious/subconscious
$FFMPEG -y -ss 00:10:08 -to 00:25:55 -i "$INPUT" -c copy "$OUTDIR/02-what-is-hypnosis.mp4"

# Segment 3: 25:55 - 38:00 — How suggestion works, critical factor
$FFMPEG -y -ss 00:25:55 -to 00:38:00 -i "$INPUT" -c copy "$OUTDIR/03-how-suggestion-works.mp4"

# Segment 4: 38:00 - 01:02:34 — Somnambulism, trance stages
$FFMPEG -y -ss 00:38:00 -to 01:02:34 -i "$INPUT" -c copy "$OUTDIR/04-somnambulism-trance-stages.mp4"

# Segment 5: 01:02:38 - 01:37:46 — Pre-talk details, compliance, contract
$FFMPEG -y -ss 01:02:38 -to 01:37:46 -i "$INPUT" -c copy "$OUTDIR/05-pretalk-contract.mp4"

# Segment 6: 01:37:48 - 02:35:00 — Elman induction demo (core)
$FFMPEG -y -ss 01:37:48 -to 02:35:00 -i "$INPUT" -c copy "$OUTDIR/06-elman-induction.mp4"

# Segment 7: 02:35:00 - 03:10:00 — Tests, shortened versions
$FFMPEG -y -ss 02:35:00 -to 03:10:00 -i "$INPUT" -c copy "$OUTDIR/07-tests-shortened.mp4"

# Segment 8: 03:10:00 - 04:00:00 — Deepening, hidden tests, fractionation, instant principles
$FFMPEG -y -ss 03:10:00 -to 04:00:00 -i "$INPUT" -c copy "$OUTDIR/08-deepening-tests.mp4"

# Segment 9: 04:00:00 - 04:30:00 — Instant inductions demo
$FFMPEG -y -ss 04:00:00 -to 04:30:00 -i "$INPUT" -c copy "$OUTDIR/09-instant-inductions.mp4"

# Segment 10: 04:30:00 - 05:02:00 — Phenomena, regression intro
$FFMPEG -y -ss 04:30:00 -to 05:02:00 -i "$INPUT" -c copy "$OUTDIR/10-phenomena-regression.mp4"

# Segment 11: 05:02:00 - 05:46:00 — Direct suggestion, therapy
$FFMPEG -y -ss 05:02:00 -to 05:46:00 -i "$INPUT" -c copy "$OUTDIR/11-direct-suggestion.mp4"

# Segment 12: 05:46:00 - 05:59:46 — Stage hypnosis, gypsy, ethics, closing
$FFMPEG -y -ss 05:46:00 -to 05:59:46 -i "$INPUT" -c copy "$OUTDIR/12-advanced-ethics.mp4"

echo "=== All cuts complete ==="
ls -lh "$OUTDIR"/
