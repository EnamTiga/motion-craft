# PHASE 6 — MUSIC & SOUND EFFECTS (MANDATORY, ALL SYNTHESIZED FROM CODE)

## 6.1 Rules

- Music must be **original**, synthesized from code, and newly designed to fit the context. Don't always
  fall back on kick/clap/hi-hat/bass/arpeggio/pad, 120 BPM, or the same build/drop structure.
  Instrumentation and structure follow the message, mood, duration, and space for narration.
- Create a **music plan** before synthesizing: emotional function, genre/character, tempo,
  timbre/instrumentation, motif, rhythm pattern, density, per-section changes, and the ending.
  Example choices: editorial = low pulse with thin textures; reflective = sparse notes;
  playful = light percussion. These are choices, not mandatory presets.
- If there is a previous video, compare music plans. Only changing the chords or the seed **does not
  count as new design**. Differentiate the musical dimensions that matter (e.g. timbre, groove,
  motif, structure, dynamics), not just the genre name. Don't claim it's "unique" simply because
  a new file was produced.
- The structure may be intro → development → space for narration → ending, or any other form that
  fits. Build/drop, risers, claps, and sidechain kicks are not obligations. Ducking against
  narration and dynamic headroom must still be designed if there is a voice-over.
- SFX are **cue-bound**: every important visual action gets a matching sound design (the 6.2 map is
  a menu of options, not a mandatory recipe). Not every letter/small motion needs an SFX; avoid
  constant sounds that cover the narration. Sound timings are read from `cues.json`, not retyped.
- No narration/human voice unless requested (voice-over mode in SKILL.md). Third-party
  samples only if CC0, with the source reported.
- Final loudness **−14 ±1 LUFS**, true peak **≤ −1.2 dBFS**.
- Match the music character to the Phase 1 answers (tempo `bpm`, progression `bars`,
  `breaks`). Examples: epic = minor, 120–128 BPM; cheerful = major, 110–120 BPM; chill = 85–95
  BPM without a hard build.
- No BPM range, chord example, or SFX map row in this file is required; the agent designs music and SFX for each production and records the character in the style paragraph.

## 6.2 Visual → sound map

| visual event | SFX (`type` in cues) |
|---|---|
| title/letters appear | `tick` per letter, `impact` at frame 0 |
| slam / text impact | `impact` + `clap` |
| scene transitions | Pick based on mechanism: scrape/slide, paper fold, soft click, selective whoosh, or impact; timing comes from the cue, not an automatic whoosh/thud on every boundary. |
| element pops / card enters | `pop` |
| droplets/water/liquid | `plink` |
| counting numbers | `ticks` (step 0.1) + `rise` (rising pitch) |
| number finishes / stamp | `thud` + `clap` + `bell` |
| object lands / building rises | `thud` (+ a slight `pop` just before for vanishing objects) |
| floating objects / drifting clouds | long `whoosh`, `pan` left/right |
| climax | `riser` before, then `impact` + `sparkle` |
| heat/sizzle/hiss | `shimmer` |
| closing call to action | `sparkle` + closing music chord |

## 6.3 Example audio generator — adaptation mandatory, not a stock soundtrack

The example generator lives in `templates/make_audio.py` in this skill (single source; do not copy
it into this document). It is a technical synthesis example, not an arrangement to copy: adapt its
instrument functions, motifs, rhythm patterns, structure, and SFX dispatch to match your new
music/transition plan. If a function does not support a cue you chose, implement it first; do not
replace all cues with whooshes just because that is all that is available. Keep the music, SFX, and
narration stems for QA. If there is narration, add the narration stem and ducking to the final mix;
this instrumental example does not do that automatically.

The source file is `templates/make_audio.py`. Copy it to the project root (or call it from the skill
folder) and run it from the project root: it reads `src/cues.json` and writes `raw_mix.wav`.

`make_audio.py` finalizes by default: after writing `raw_mix.wav` it runs the standard
two-stage chain (stage 1 measures loudnorm, stage 2 applies it linearly with the measured
values and ends with `alimiter=limit=0.72:level=false` as a hard ceiling) and writes
`public/mix.wav`. The limiter stage is not optional polish: without it, a WAV that measured
on target overshot to −0.7 dBFS true peak after AAC encoding in the final MP4, above the
Gate E limit of −1.2 dBTP. Pass `--no-finalize` to write only `raw_mix.wav` and normalize
manually with the same chain. Either way, **verify the numbers** on the result:

```bash
python3 make_audio.py
ffmpeg -nostats -i public/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
```

Target `I:` between −15 and −13 LUFS, `Peak:` ≤ −1.2 dBFS. If outside the target, repeat
loudnorm or adjust with `-af volume=XdB`.

If the production has narration, the mix must also pass the measured
voice-balance check defined in Gate E (`references/06-qa-gates.md`, section
7.6): narration at least +8 LU above the music/SFX bed in every narration
segment, measured on companion renders. Total loudness on target does not
prove the narration is audible over the bed; design the narration gain and
the ducking for that threshold, not just for the total.

Add new SFX types if the concept needs them (e.g. click, knock, water, typewriter): write
small functions with a swept sine + noise + exponential envelope, and add them to the SFX dispatch block in `templates/make_audio.py`.
Every scene must feel and sound different, while remaining one sound family.

---

## 6.4 Voice-over mode C — ElevenLabs API

- This mode runs only if the user selected it in Phase 1 and the configuration is complete.
  If the user chose no (mode A), don't create narration. If the user deferred the choice,
  the default remains no narration; don't use paid services without consent.
- If the user already supplied voice-over audio (mode B), use that audio per 6.5;
  don't request an API key or regenerate. Music and SFX remain mandatory and
  are produced separately per Phase 6; they are not replaced by the voice-over.
- **Mandatory configuration:** an API key securely available in the execution environment,
  the user's chosen `model_id`, and the selected voice's `voice_id`. The model ID selects the TTS
  model; the Voice ID selects the voice — they are different things. Don't guess the IDs or assume
  the API key alone is enough. If the user hasn't chosen yet, help with the list of models/voices
  actually available from the API or official documentation, then ask for a choice if needed.
- **API key security:** offer a secret/credential field or the `ELEVENLABS_API_KEY`
  environment variable as the safer path. If the user still chooses to paste the
  API key in chat, accept that choice after a brief warning that the key
  may persist in the conversation history. Ask for a project-specific key with minimum permissions
  and usage limits where available, and recommend revoking/replacing it once
  finished. Don't repeat or display the key in replies. Don't write it into
  code, recorded shell commands, logs, README, the MP4, or the project zip. Use it only
  through the available secret/runtime mechanism. Don't ask the user to upload a
  `.env` file. Include only a `.env.example` with empty values if needed.
- Before calling the API, check the current ElevenLabs documentation: language/model
  compatibility, audio formats, and alignment/timestamp support in the chosen model.
  Don't claim timestamp features apply to all models. Explain that calling the
  API may consume the user's quota/credits; don't make purchases, upgrades, or automatic top-ups.
- Use preset voices or voices the user is licensed to use. Don't clone or
  impersonate real people without appropriate permission. For factual videos, use
  a separate narrator and don't make it sound as if the subject speaks the synthetic narration.
- Compose the narration to the duration and beat plan, **show the script to the user and get
  approval BEFORE generating** (narration locks timing). Generate the voice-over before
  locking final timing. Store audio locally without credentials.
- **Timestamps:** if the chosen endpoint/model returns alignment/timestamps
  (character → start/end), use them — aggregate to word timings, no need for WhisperX.
  If the endpoint provides no alignment, use measured clip/per-sentence durations;
  don't fabricate per-word timestamps. Merge the timing into `cues.json` (the
  `voiceover.source: "elevenlabs"` block) as the single timing source for animation, narration,
  music, and SFX.
- While narration is playing, lower the music with ducking and keep SFX from covering key words.
  Normalize the final mix to the Phase 6 targets, not the individual tracks.
- If the API key/model/voice is unavailable, authentication fails, quota runs out, or the call
  fails, explain the problem without leaking secrets. Don't silently switch to Google
  TTS, Voicebox, or another provider. Ask the user to complete the configuration according to
  their chosen credential handling, with the security warnings above, or offer a version
  without narration.
- In the final report, state that the synthetic narration was made with ElevenLabs, the name/ID of the
  model and voice used (no API key), and any timing/pronunciation limitations found.

## 6.5 Voice-over mode B — user-supplied audio, timestamps via WhisperX

- **If the user supplies voice-over audio without timestamps, use WhisperX to produce
  timestamps.** Main repo: https://github.com/m-bain/whisperX. No need to ask the
  user to make timestamps themselves. The user's audio is the primary timing reference for the video; don't
  regenerate via ElevenLabs or any other service, and don't ask for a TTS API key.
- **If the user already included timestamps** (e.g. SRT/VTT/JSON karaoke file): validate
  their fit against the audio (order, ranges, duration coverage). Use them directly if
  valid; no need to reprocess with WhisperX. If timestamps are partially missing,
  wrong, or inconsistent, explain and fix them with WhisperX.
- If the audio is provided as a link, download it and verify the result is actually audio,
  not an HTML page. Keep the original audio unchanged. Create a working mono
  16 kHz copy if required by the pipeline, without altering the speed or content of the original audio.
- If a script is included, verify it matches the audio content, then run forced alignment
  with WhisperX. If there's only audio, transcribe first, then align
  with the appropriate language model. **Transcription alone is not the final per-word timestamp result:**
  run the `whisperx.align()` stage and take word start/end times from the alignment output.
- Detect/check the audio language and the availability of a matching alignment model; don't
  equate ASR language support with alignment support. Check the CPU/GPU/RAM environment
  and dependency compatibility before running. Tune the model, batch/chunk size,
  and compute type to the available resources; record the configuration actually used.
  Diarization is unnecessary for a single narrator.
- Save the raw WhisperX output and per-word results, at minimum `{word, start, end}` in
  seconds, plus SRT/VTT subtitles if needed. Import those results into `cues.json`
  (the `voiceover.source: "whisperx"` block) as the single timing source. For scene cues,
  group words into phrases/sentences; for word highlights, use per-word ranges.
  Music and SFX follow the visual/narration cues without covering the voice.
- **Mandatory timestamp QA:** check names, numbers, mis-transcribed words, empty/out-of-order/
  out-of-duration timestamps, implausible word durations, pauses, and start–middle–end
  synchronization. Don't split the audio duration evenly per word and call it alignment. If a
  word fails to align or its time is estimated, flag it clearly and report; fix the transcript and
  re-run alignment if needed. Don't claim you listened to the audio if you only inspected waveform/data.
- Don't cut, speed-change, or replace the user's audio content without permission. Fit the
  video duration to the audio; if that conflicts with the duration brief, ask which takes priority.
  If the audio is eventually edited with permission, recompute timestamps against the final audio version.
- If WhisperX fails due to language model, dependencies, download, or resources, report
  the actual cause. Don't claim timestamps were produced and don't silently switch to
  stable-ts or another method. Ask for approval for a fallback or provide steps to run WhisperX
  in a different environment.
- In the final report, state that the audio came from the user, timestamps were produced with WhisperX
  (or from validated user-supplied timestamps), the language/model used,
  and which parts still need checking. The audio content is narration material, **not automatically
  verified facts**; factual claims still follow Phase 2.

## 6.6 Voice-over mode D: Muse TTS (Muse only)

Mode D (Use Muse) is offered ONLY when both detection conditions hold:
(1) the skill is running in the Muse harness (skill installed in
`~/workspace/custom-skills/`, or the session states it runs in Muse), AND
(2) the Muse TTS path is detected: `/opt/hatch/bin/tts` exists and
`/opt/hatch/bin/tts --help` exits with code 0, or Muse spoken-audio capability
is available in the session. If either condition fails, Mode D does not appear
at all and the mode table stays A/B/C exactly as before.

Detection is an offer, not a promise of availability. Muse TTS is
rollout-gated and has no preflight, so the first segment is the real test: if
synthesizing the first segment fails because the capability is unavailable,
report it as it is, stop Mode D, and offer Mode A or Mode C. NEVER switch
providers silently.

This section does not change 6.4 (Mode C) or 6.5 (Mode B). Mode B stays
WhisperX. Mode D never runs WhisperX in any form, including to "fix" Mode D
timing.

Flow:

1. The user picks Mode D in Phase 1. The narration script is written, shown to
   the user, and approved BEFORE synthesis (the cross-mode approval rule in
   SKILL.md applies unchanged).
2. Split the script per segment = per scene, or per complete sentence/phrase,
   following the scene boundaries in the beat plan. One segment must never cut
   a phrase in the middle.
3. **Word limit per segment (mandatory): at most 15 words per segment.** Reason:
   Mode D subtitles are phrase level, one segment is one subtitle unit, so the
   segment length is the subtitle precision. Normal English speech runs at
   about 2.5 words per second, and the reference Mode D production (37.5
   seconds, 6 segments) averaged 6.25 seconds per segment: 6.25 x 2.5 is about
   15 words. Capping at 15 keeps a segment near 6 seconds, short enough for its
   phrase subtitle to stay in sync and readable; the longest reference segment
   (20 words, 7.97 seconds) already held one subtitle on screen for almost 8
   seconds. If a sentence runs over 15 words, split it at a clause boundary
   (comma, semicolon, conjunction) into two segments; never split mid-phrase
   and never speed up the audio to fit. Count words before synthesis, at script
   approval time, and record the per-segment counts in the script document.
   For Indonesian narration, apply the same 15-word cap as the default: the
   cap exists to bound subtitle duration, not to model one language's rate.
4. Synthesize per segment (Indonesian example):

   ```bash
   /opt/hatch/bin/tts speak --text "<segment text>" --language id --format mp3 --output public/vo-seg-01.mp3
   ```

   Limits that apply: output is MP3; the default timeout for `speak` is 120
   seconds; the default 1,200-character chunking applies to the
   `synthesize-script` path (not a reason to use script mode for Mode D,
   because Mode D needs one file per segment); voice quality varies per
   language; there is no API key and no third-party quota.
5. Measure each segment's duration, never guess it:

   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 public/vo-seg-01.mp3
   ```
6. Cumulative segment offsets become the timing boundaries in `cues.json`:
   segment 1 starts at 0.00, each next segment starts at the previous segment's
   end (plus a pause only when one is planned in the beat plan, and that pause
   is recorded). Total VO duration must not exceed `dur` in cues; if it does,
   revise the beat plan via `make_cues.py` — never cut or speed up the audio.
7. Mode D subtitles are phrase/segment level: each segment's text goes into
   the `captions` field in cues with start/end from step 6. `wordTimings` for
   Mode D is EMPTY or ABSENT. NEVER divide a segment's duration evenly per
   word, and NEVER invent per-word timestamps.
8. Segment files are named `public/vo-seg-NN.mp3` (NN two digits, in scene
   order). The trace file `qa/vo-muse-tts-segments.json` records, per segment:
   text, file, and the raw ffprobe duration. Concatenate the segments into
   `public/vo.mp3` with ffmpeg concat (or an equivalent filter) without
   changing speed and without cutting content; after concatenation, re-measure
   the combined duration with ffprobe — it must equal the sum of the segment
   durations +/- 0.1 seconds, otherwise investigate before cues are locked.
9. The voiceover block in cues for Mode D looks exactly like this:

   ```json
   "voiceover": {
     "audioFile": "public/vo.mp3",
     "source": "muse-tts",
     "segmentTimings": [
       {"text": "<segment text 1>", "file": "public/vo-seg-01.mp3", "start": 0.0, "end": 2.84},
       {"text": "<segment text 2>", "file": "public/vo-seg-02.mp3", "start": 2.84, "end": 5.31}
     ],
     "sourceTimestamps": "qa/vo-muse-tts-segments.json"
   }
   ```

   `audioFile` is the concatenation of the segments (no speed change),
   `segmentTimings` is the only narration timing source for Mode D, and
   `sourceTimestamps` points to the trace file holding the raw per-segment
   ffprobe durations.
10. Music and SFX stay mandatory, ducking against narration is still designed,
   and the final loudness target stays -14 +/-1 LUFS with true peak
   <= -1.2 dBFS (the existing Phase 6 rules, unchanged).
11. Gate D for Mode D: the per-word highlight deviation target is
    **NOT APPLICABLE**, because Mode D does not produce per-word timestamps
    ("Mode D does not produce per-word timestamps"). What is verified
    instead: segment-boundary synchronization (start, middle, and end of the
    video) against `segmentTimings`, and that phrase subtitles never appear
    before their segment starts.
