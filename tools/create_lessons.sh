#!/bin/bash
# Create lesson-by-lesson video files — fixed paths for Windows ffmpeg

FFMPEG=/tmp/ffmpeg.exe
SRC="D:/гипноз/видео для уроков/нарезка"
OUT="/d/гипноз/видео для уроков/нарезка2"

# Use native Windows paths for concat files
SRC_WIN="D:/гипноз/видео для уроков/нарезка"

function concat_to() {
  local lesson="$1"
  shift
  local list_file="C:/Users/valter/AppData/Local/Temp/concat_${lesson}.txt"
  rm -f "$list_file"
  for seg in "$@"; do
    echo "file '${SRC_WIN}/${seg}.mp4'" >> "$list_file"
  done
  echo "  [concat] $lesson"
  $FFMPEG -y -f concat -safe 0 -i "$list_file" -c copy "$OUT/${lesson}.mp4" 2>/dev/null
}

function copy_to() {
  local lesson="$1"
  local seg="$2"
  echo "  [copy]   $lesson"
  cp "$SRC/${seg}.mp4" "$OUT/${lesson}.mp4"
}

mkdir -p "$OUT"

echo "=== Module 0 ==="; concat_to "0.1-what-is-hypnosis" "03-what-is-hypnosis" "04-conscious-subconscious"
concat_to "0.2-conscious-subconscious" "04-conscious-subconscious" "05-critical-factor" "06-how-suggestion-works"
copy_to  "0.3-suggestibility-test" "08-phenomena-mention"
concat_to "0.4-course-structure" "09-trance-stages-somnambulism" "10-somnambulism-deep"
echo "=== Module 1 ==="; concat_to "1.1-pretalk-hypnotic-contract" "01-opening" "02-4-forbidden-words" "12-compliance" "13-session-control"
copy_to "1.2-eyelid-catalepsy-body-scan" "14-elman-start-body-scan"; copy_to "1.3-fractionation-arm-drop" "15-elman-amnesia-numbers"
copy_to "1.4-number-amnesia" "15-elman-amnesia-numbers"; copy_to "1.5-tests-catalepsy-analgesia" "16-elman-tests"
concat_to "1.6-shortened-versions" "17-shortened-versions" "18-demo-shortened"
echo "=== Module 2 ==="; copy_to "2.1-stabilizing-somnambulism" "19-hidden-tests"
copy_to "2.2-hidden-fractionation-test" "19-hidden-tests"; copy_to "2.3-working-with-resistance" "13-session-control"
copy_to "2.4-direct-suggestions" "22-direct-suggestion"; copy_to "2.5-post-hypnotic-window" "22-direct-suggestion"
echo "=== Module 3 ==="; copy_to "3.1-four-principles-spike" "20-instant-inductions"
copy_to "3.2-hand-induction" "20-instant-inductions"; copy_to "3.3-standing-induction" "20-instant-inductions"
copy_to "3.4-verbal-shock" "20-instant-inductions"
concat_to "3.5-phenomena-rapid-hypnosis" "20-instant-inductions" "21-phenomena-aphasia-amnesia"
copy_to "3.6-context-safety" "23-tests-phenomena-2"
echo "=== Module 4 ==="; copy_to "4.1-what-are-phenomena" "21-phenomena-aphasia-amnesia"
concat_to "4.2-catalepsy-analgesia" "08-phenomena-mention" "16-elman-tests"
copy_to "4.3-amnesia-types" "21-phenomena-aphasia-amnesia"; copy_to "4.4-post-hypnotic-suggestions" "22-direct-suggestion"
copy_to "4.5-hallucinations" "21-phenomena-aphasia-amnesia"
concat_to "4.6-introduction-to-regression" "21-phenomena-aphasia-amnesia" "23-tests-phenomena-2"
echo "=== Module 5 ==="; concat_to "5.1-three-questions" "22-direct-suggestion" "24-therapy"
copy_to "5.2-four-constructions" "22-direct-suggestion"; copy_to "5.3-law-of-compounding" "25-compounding"
concat_to "5.4-direct-suggestion-vs-regression" "24-therapy" "23-tests-phenomena-2"
copy_to "5.5-session-structure" "24-therapy"
echo "=== Module 6 ==="; concat_to "6.1-stage-hypnosis" "20-instant-inductions" "26-gypsy-hypnosis"
copy_to "6.2-gypsy-hypnosis" "26-gypsy-hypnosis"; copy_to "6.3-difficult-clients" "24-therapy"
copy_to "6.4-speed-vs-depth" "20-instant-inductions"
concat_to "6.5-ethics-boundaries" "24-therapy" "27-closing"

echo "=== Done ===" && ls -lh "$OUT"/ | wc -l && echo "---" && ls "$OUT"/ | sort
