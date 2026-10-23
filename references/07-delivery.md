# Phase 8 — Delivery

## 1. Save and deliver the final file

- Save the MP4 with a clear name to an output directory that actually exists and
  persists in the current environment. In Muse, the standard path is: save the
  final MP4 in `~/workspace/` (the persistent directory) and hand it over as an
  attachment or file link in the chat, with the same filename and hash as in the
  QA report. In other harnesses, use that harness's file presentation tool;
  don't assume a specific path or tool always exists.
- Deliver the file whose **hash matches** the final QA report (`qa/report.md`).
- If the user asks for code, include a project zip without credentials/dependency caches.

## 2. Concise report — max 8 lines

End the message with:

- concept & scene flow
- specification (resolution, fps, duration, music BPM)
- voice-over mode and source, when narration is used (e.g. "voice-over: Mode D, muse-tts, subtitle level frasa, tanpa highlight per kata")
- data sources + labels used
- assumptions you made
- facts not found / demo numbers / things that **need verification**
- QA status (pass/partial/draft), the actual checking methods, and specific remaining
  limitations
- specific revision offers (e.g. "change the palette", "add scene X", "bump to 60 fps")

## 3. Revisions from the user

- Change **only what was requested** (edit the relevant files, re-render, re-QA that
  portion). Don't rebuild from scratch unless asked.
- After changing timing, re-run `make_cues.py` and `make_audio.py` so the sound
  stays in sync.
- Every replacement MP4 must be re-QA'd at minimum for the affected portions (see Phase 7.7) —
  evidence from an old version doesn't pass a new file.
