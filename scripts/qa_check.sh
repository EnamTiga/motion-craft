#!/usr/bin/env bash
# qa_check.sh — automated QA for the final MP4 (Phase 7, automated parts of Gates C & E).
# Usage: ./qa_check.sh <file.mp4> [target_fps] [target_duration_seconds]
# Output: a text report; save it as automated evidence in qa/report.md.
set -u
FILE="${1:?Usage: qa_check.sh <file.mp4> [target_fps] [target_duration_seconds]}"
FPS_T="${2:-}"
DUR_T="${3:-}"

command -v ffprobe >/dev/null || { echo "ERROR: ffprobe not found"; exit 2; }

echo "=== qa_check.sh — $FILE ==="
echo "sha256: $(sha256sum "$FILE" | cut -d' ' -f1)"

echo "--- stream metadata"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,sample_rate,channels -of default=noprint_wrappers=1 "$FILE"

echo "--- full decode (errors must be empty)"
ffmpeg -v error -i "$FILE" -f null - 2>&1 && echo "decode: OK"

if [ -n "$DUR_T" ]; then
  DUR_A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FILE")
  echo "--- duration: target=$DUR_T actual=$DUR_A (target difference <= 0.1s)"
fi

echo "--- loudness (target I: -15..-13 LUFS, Peak: <= -1.2 dBFS)"
ffmpeg -nostats -i "$FILE" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2

echo "--- black/freeze/silence diagnostics (diagnostics, not judges)"
ffmpeg -v info -i "$FILE" -vf blackdetect=d=0.1 -an -f null - 2>&1 | grep blackdetect || echo "blackdetect: clean"
ffmpeg -v info -i "$FILE" -vf freezedetect=n=0.001:d=1 -an -f null - 2>&1 | grep freezedetect || echo "freezedetect: clean"
ffmpeg -v info -i "$FILE" -af silencedetect=n=-50dB:d=0.8 -f null - 2>&1 | grep silencedetect || echo "silencedetect: clean"

if [ -n "$FPS_T" ]; then
  FPS_A=$(ffprobe -v error -select_streams v -show_entries stream=avg_frame_rate -of csv=p=0 "$FILE")
  echo "--- FPS: target=$FPS_T actual=$FPS_A (fraction; 60/1 = true 60fps, 30/1 claimed as 60 = FAIL)"
fi

echo "=== done. Record the numbers above in qa/report.md as automated evidence. ==="
