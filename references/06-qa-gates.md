# PHASE 7 — EVIDENCED QA AND DELIVERY GATES (MANDATORY)

## 7.1 QA status: no rubber-stamping

Create `qa/report.md` and `qa/checks.json` with **the final file version/name and SHA-256**,
the target specification, tool configuration, and a table:

| ID | scene/timecode | check & criteria | method actually used | evidence/path or measured result | status | issue → fix → retest result |
| --- | --- | --- | --- | --- | --- | --- |

- Status: **PASS**, **FAIL**, **UNVERIFIED**, or **NOT APPLICABLE + reason**.
  Never turn "couldn't be checked" into a pass. Tool output numbers, stills, waveforms,
  and playback each prove different things.
- Distinguish **automated** evidence, **visual inspection of frames/sequences**, and
  **playback/listening**. Don't claim you watched/heard anything if you only read logs or
  looked at a contact sheet.
- **Blocker** bugs: corrupt/undecodable file, wrong specification, missing/truncated/
  altered narration without permission, wrong asset identity, misleading claims, leaked credentials. Must
  be fixed before delivering as final.
- **Major** bugs: every scene looks like a poster, monotonous transitions violating the plan, unreadable subtitles/key
  text, collisions/cropping, wrong cues, narration covered, audio clicks/clipping,
  blurry images/upscales beyond source resolution. Must be fixed; don't excuse them
  as "style preference".
- **Minor**: polish that doesn't block the message/context. Record specifically, including
  timecode. Don't use aggregate aesthetic scores to paper over blocker/major issues.
- A mandatory check that couldn't be run means **partial QA**. Don't say "final passed all
  QA"; you may deliver a **preview/draft** with explicit limitations and
  specific verification requests. If the user approves an exception, record
  the approval and the limitations — don't fake a passing status.
- Use `scripts/qa_check.sh` for the automated portion (metadata, full decode, loudness,
  silence/black/freeze scan) — its output goes into the table as automated evidence. Visual
  and listening inspection remain manual.

## 7.2 Gate A — audit of brief, data, assets, and plans before render

- Cross-check aspect ratio, resolution, FPS, duration, language, CTA, style paragraph, narration, constraints, and
  user priorities against the structured configuration. No default may silently
  override an explicit request.
- Validate all cues are finite and in range, scenes have no unplanned gaps/overlaps,
  event references are valid, and every consumer reads the same timing source.
- Audit `assets.json` (see 01): every scene has assets that fit its visual needs;
  variety is adequate; crop/zoom is not a new photo; a relevant photo is not automatic proof of a claim;
  check resolution, orientation, subject crop, and sharpness (≥2× display size, no
  blur/upscale) before use.
- Audit numbers/diagrams/opinion labels against sources and context. Don't display fabricated
  scales or causality. Unverified claims must be handled per Phase 2, not
  disguised as data through motion.
- The motion plan table must be complete: entrance, two action beats after the entrance for scenes
  ≥3 seconds, development, handoff, and the relationship to narration. Cues in the plan are not proof
  the actions are visible in the render.
- The plan contains the style paragraph from Phase 1c, and the rendered flow matches that
  paragraph. A flow that differs from the paragraph is a Gate A finding, whatever the flow looks like.
- Audit the transition plan: every boundary has a mechanism and a rationale, no two
  consecutive identical ones, at least 3 relevant mechanisms when there are ≥5 scenes. Different wipe colors/directions are not
  a new mechanism.
- Audit the music plan and stems: character fits the context, not an old recipe with different
  chords, SFX match their objects, and narration space and the ending are designed.
- **Scratch folder and free disk check (mandatory, before any render).** Rendering writes
  frames, temp files, and the output MP4 outside the project tree as well as inside it, and a
  full disk mid-render wastes the whole run (on the Muse VM, `/tmp` is a 512 MB tmpfs and a
  render there died with ENOSPC). Before Gate A passes:
  1. Pick the scratch folder for this render (the folder the render tool uses for temp files,
     e.g. via `TMPDIR`). If `/tmp` is a small tmpfs (check with `df -h /tmp`), set the scratch
     folder outside `/tmp`, on the large disk (e.g. `/var/tmp/<project>` or a folder under the
     workspace disk), and use it for the render commands.
  2. Measure free space on the scratch filesystem (`df -h <scratch folder>`) and on the output
     filesystem. Free space on each must be at least 2 GB and at least 5x the expected final
     MP4 size; if either is lower, free space, move the scratch folder, or stop and report.
     Do not start the render on a guess.
  3. Record the result in `qa/report.md` and in `qa/checks.json` under `gateA`:
     `scratchDir` (absolute path), `scratchFreeBytes` (number, from `df`), `outputFreeBytes`
     (number), and `diskCheck` (`PASS` or `FAIL`). A missing record means Gate A is not passed.

## 7.3 Gate B — stills & temporal testing before full render

- Render stills at frame 0, peak motion/overshoot, after the entrance, each major action,
  and just before the exit **for every scene**. Also check the moment all elements have reached
  their final positions, not just on entry.
- For **every transition**, capture a before–during–after sequence around the boundary: e.g.
  b−0.3 s to b+0.3 s at intervals ≤0.05 s; extend if the transition is longer. Convert
  via the project FPS and clamp to the valid range. Check handoff continuity, direction,
  occlusion, edges, z-order, scene bleed, and no unintended blank frames.
- Inspect in-scene motion with tight frame bursts at every action cue, plus
  samples along the scene (spacing ≤0.5 s). Show **which object changes and to explain what**.
  Subtitles/camera/particles/progress bars alone don't prove the main action.
- If pixel comparison/optical flow is used, separate the main object's ROI from
  subtitles/ambient. A whole-frame change score is not evidence of meaningful motion. Check
  easing, settle, follow-through, stagger, and action patterns across scenes; identify
  entrance patterns repeated without development.
- Check text/subtitles/sources/disclaimers at phone display size, not just desktop zoom: no collisions, cropping, leaving the safe area, being covered by hands/objects/stamps/wipes,
  or layout shifts from font fallback. For portrait 1080×1920: main text/subtitles ≥40 px, credits/sources ≥36 px; scale for other resolutions. The default safe area
  x 60–1020/y 180–1650 is adjusted per platform/ratio.
- Use readable text contrast (target 4.5:1 for body text/subtitles) and
  stable background fields on photos. Check full display range based on word count; don't
  count time while text is still masked/cropped as reading time.
- Check image quality in stills: photos are not blurry at their maximum display size
  (including during camera push-in). Zooming beyond source resolution = major bug.
- After fixes, re-run stills and bursts on the affected areas before the full render.

## 7.4 Gate C — technical QA on the FINAL MP4, not just the composition

- Measure the streams with `ffprobe` or an equivalent tool: video/audio codec, width/height,
  nominal and average FPS, frame count/duration, audio duration, sample rate, channels, and
  file size. Verify that **60 fps really was rendered at 60 fps** when requested; not a
  30 fps video duplicated or metadata-labeled as 60 fps.
- Match the frame count to the configuration. Visual duration rounding tolerance is at most
  one frame; container duration may have small audio codec padding (target difference
  ≤0.1 seconds). Padding is not a reason to accept a clipped last word.
- Decode the **entire file** to detect errors, e.g.
  `ffmpeg -v error -i FILE_FINAL -f null -`. Check the first/last frames and all
  scene boundaries from the final MP4. Don't conclude the file is healthy from metadata or
  pre-render stills alone.
- Scan the full duration with frame samples spaced ≤0.5 s, then take tight bursts at
  **all** action/transition cues from the final MP4. If available, play back the entire video to
  audit the rhythm; record the method actually used.
- Black/freeze/silence detectors are **diagnostics**, not sole judges. Review
  detected intervals against the design. Unintended black/blank frames >0.1 seconds,
  jumps, flicker, misrasterization, or dead objects after the entrance must be investigated.
  Subtitle motion can hide static scenes from the freeze detector.
- Test determinism on key frames if you use seeds/randomness or find inconsistent results. Check
  motion blur/judder/aliasing at the native FPS; raising the FPS doesn't
  fix a wrong animation step.

## 7.5 Gate D — narration, subtitles, and synchronization

Gate D applies only if `cues.json` has a `voiceover` block (modes B/C/D); without it, record
"not applicable + reason" and move on to Gate E.
For mode D (muse-tts), the per-word highlight target below is NOT APPLICABLE; verify segment-boundary sync against segmentTimings and phrase subtitle timing instead.

- Compare the final audio to the source audio: all content, order, and pace preserved
  unless changes were approved; no double playback, drift, missing pauses, or clipped first/last
  words. Compare waveform/duration/offset if levels were changed;
  MP3 checksums can't be used to match audio after encoding/mixing.
- Validate **all** word timestamps (from ElevenLabs alignment, WhisperX, or
  user-supplied): finite, start ≤ end, valid ranges, sensible ordering, overlapping/duplicate/
  empty words/zero or implausible durations flagged for review. Check the transcript for names, numbers,
  and domain terms; don't guess corrections. If the source transcript was changed, re-align
  the affected portions and keep a change trail.
- Check **start–middle–end** sync, every scene boundary, the first word after a long
  pause, critical words/names/numbers, and alignment outliers. For per-word
  highlights, target observed deviation ≤0.1 seconds when comparable against playback/human labels;
  deviations >0.2 seconds must be investigated. These are review targets, **not claims of tool accuracy**;
  without a reliable time reference, report uncertainty — don't produce an accuracy percentage.
- Ensure subtitles don't appear before their word, don't jump during transitions, don't linger through
  implausible pauses, and sentences/phrases aren't clipped by layout.
  Valid timestamps are not altered just to match music or motion.
- Important visual cues and SFX must match the events in `cues.json` (technical offset target
  ≤1 frame on the timeline, unless anticipation/tail is intentional). The same cue schedule doesn't
  prove the actual audio onsets match; inspect waveform/listening when available and note
  encoding delay if relevant.

## 7.6 Gate E — audio and sound design

- Measure the **final MP4**: integrated loudness −14 ±1 LUFS, true peak ≤−1.2 dBTP. Don't just
  measure the WAV before AAC; re-run normalization/encoding if the final result is off target.
- Check the music/SFX/narration stems to confirm they actually exist and aren't
  silence. Don't assume an AAC audio stream means music and SFX made it in.
- Check the ducking envelope during narration and the music's return in pauses; no excessive
  pumping, edit clicks, distortion, clipping, abrupt endings, or unplanned hum. Silence detection needs context: intentional narration pauses are not bugs.

**Voice balance check (measured, mandatory when the production has narration).**
Total loudness passing says nothing about balance: a mix can measure −14 LUFS
while the narration sits far below the music. (Measured incident, 2026-10-23:
a shipped demo measured −14.0 LUFS total while its VO stem sat 16–19 LU below
the music/SFX bed in every narration segment; the total was practically the
bed alone. The project owner heard it; no gate had measured it.)

- **Method — companion renders.** Render the narration stem and the bed stem
  (music + SFX) separately, each through the *same* mix chain and the *same*
  final gain/limiter as the final mix, with the other stem omitted. Measure
  integrated loudness (ebur128 or loudnorm) of each companion **per narration
  segment window**, using the segment boundaries from `cues.json`
  (`voiceover.segmentTimings` for Mode D, the equivalent narration timings for
  modes B/C). Per segment: `diffLU = LUFS(VO companion) − LUFS(bed companion)`.
  A gain applied identically to both companions cancels in the difference;
  never re-normalize the companions individually (a per-file dynamic
  normalization, e.g. a loudnorm pass that falls back to dynamic mode,
  destroys the evidence — if the finalize chain normalizes per file, measure
  the companions at the pre-finalize stage under the common gain and say so).
- **Cut windows inside the filtergraph** (`atrim=start=…:end=…` + `asetpts`),
  or extract each segment to its own file first and measure the extracted
  files. Do **not** measure a window by combining `-ss`/`-t` with a single
  ebur128 pass: on the ffmpeg build used for the 2026-10-23 repair that
  combination measured a different, louder window (same segment read
  −34.1 LUFS via atrim/decode-extraction but −28.2 LUFS via `-ss`/`-t`).
- **Threshold: every narration segment must measure diffLU ≥ +8.** The minimum
  per-segment difference is the headline number of this check. Below +8 in
  any segment is a Gate E FAIL (major: narration covered), fixed by raising
  the narration and/or lowering the bed under narration (static gain and/or
  stronger sidechain ducking), then re-measured on the new mix.
- **Record in `qa/checks.json`** under `gateE.voiceBalance`, exactly this shape:

  ```json
  "voiceBalance": {
    "status": "PASS",
    "method": "companion renders via identical chain, ebur128 per segmentTimings window, atrim-cut",
    "thresholdLU": 8,
    "minDiffLU": 10.6,
    "perSegment": [
      {"seg": 1, "start": 0.0, "end": 3.72, "voLUFS": -14.2, "bedLUFS": -24.8, "diffLU": 10.6}
    ]
  }
  ```

  One `perSegment` entry per narration segment. Keep the companion files
  (e.g. `qa/balance/vo_in_mix.wav` and `qa/balance/bed_in_mix.wav`) so the
  reviewer can re-measure independently; a reviewer re-measurement that does
  not reproduce the builder's numbers within ~0.5 LU invalidates the record.
- A production **with** narration but **no** `voiceBalance` record counts as
  Gate E not passed, whatever the total loudness says. With no narration
  (Mode A), record `"voiceBalance": {"status": "NOT APPLICABLE", "reason": "no narration"}`
  and move on. `templates/make_audio.py` carries a `voice_balance()` helper
  implementing this measurement.
- If listening/playback capability is available, listen to the final result at normal level:
  word clarity, music not covering narration, SFX not piercing, channel balance/mono,
  and mood changes matching scenes. LUFS measurement alone **does not prove**
  comfort or intelligibility. If you can't listen, mark the perceptual check UNVERIFIED
  and request a specific listening review.

**Perceptual listening step (defined, mandatory).** The listening above is not optional
color: it is a named sub-check with a named listener, named excerpts, and a written record.

- **Who listens:** the reviewer (the checker role, never the builder who rendered the file).
  If the reviewer has no audio playback path, a named human listener does it instead (the
  project owner or a person the owner appoints). "The agent" is not a listener name; record
  the role, e.g. `reviewer`, or the human's name/role.
- **Excerpts that must be heard** (full playback is better, but these are the minimum):
  1. The opening, 0:00 to 0:05, including the first narration entry if there is narration.
  2. The first 2 seconds of every narration segment (for Mode D: every `segmentTimings`
     start), checking word clarity and that music/SFX do not cover the entry.
  3. A 5 second excerpt around the midpoint of the video.
  4. The loudest section (climax, strongest SFX, or build/drop), checking for piercing
     SFX, pumping, distortion, and clipping.
  5. The final 5 seconds, including the ending chord and the fade out.
  6. Every interval the silence/clipping detectors flagged during Gate C/E scans.
- **Record in `qa/checks.json`** under `gateE.perceptualListening`, exactly this shape:

  ```json
  "perceptualListening": {
    "status": "PASS",
    "listenerRole": "reviewer",
    "listenedAt": "2026-10-23T10:00:00+07:00",
    "excerpts": [
      {"startS": 0.0, "endS": 5.0, "label": "opening", "result": "PASS", "notes": "first word clear, music under narration"}
    ],
    "findings": "none",
    "notListenedReason": null
  }
  ```

  `status` is `PASS`, `FAIL`, or `UNVERIFIED`. One `excerpts` entry per excerpt heard, with
  its own `result` and `notes`; a `FAIL` excerpt makes the sub-check `FAIL` and follows the
  retest flow in 7.7 like any other Gate E failure.
- **If listening is truly impossible** (no playback path for the reviewer and no human
  listener available): set `status` to `UNVERIFIED`, `excerpts` to `[]`, and
  `notListenedReason` to the specific cause (what path was tried and why it cannot play
  audio), plus the specific listening request sent to the user. An UNVERIFIED perceptual
  sub-check with no `perceptualListening` record, or with an empty `notListenedReason`,
  counts as Gate E not run, not as a passed gate with a footnote.

## 7.7 Retest and delivery gate

1. Log bugs with timecode, evidence, severity, root cause, fix, and retest result.
   Don't write "fixed" without checking a new render.
2. Visual-only revisions: keep valid audio/timestamps, re-render, and QA the changed areas
   + neighboring boundaries. Timing/audio revisions: regenerate cues/mix/alignment if
   needed, then audit the entire subtitle sequence and final sync.
3. For **every replacement MP4**, re-run metadata, full decode, loudness/peak,
   first/last frames, the full scan, and checks on the areas touched by the change. Evidence from an
   old version doesn't pass a new file.
4. Update the final hash and ensure the path that was measured, checked, and delivered
   is **the same**. Clean old previews out of the delivery so the user doesn't download the wrong file.
5. No remaining blocker/major issues for a passing final status. If a mandatory check
   is still unverified, report it as partial QA/draft per 7.1. The concise user report
   states status, methods, key evidence, and limitations; details live in
   `qa/report.md`.

---

Phase 8: see `references/07-delivery.md`. Delivery is owned and specified in full by that file;
it is not duplicated here.
