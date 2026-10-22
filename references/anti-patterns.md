# Common Pitfalls (these have actually happened — don't repeat them)

Format: problem → fix, with ❌/✅ code examples where relevant.

## Environment & render

- Background process shell dies → always render in the foreground with `timeout`.
- Concurrency greater than the CPU count → errors. Use `--concurrency=1` on 1 CPU.
- Claiming "it's already epic/cool" without checking → always run Phase 7 before handoff.

```bash
# ❌ background, can die when the tool finishes
npx remotion render ... &
# ✅ foreground + time limit
timeout 280 npx remotion render src/index.ts Main out/video.mp4 --concurrency=1 --overwrite
```

## Animation code

```tsx
// ❌ Math.random() — multi-pass renders flicker/diverge
const x = Math.random();
// ✅ deterministic
import {random} from 'remotion';
const x = random(`seed-${frame}`);

// ❌ spring with a negative frame
const s = spring({frame, fps: FPS});
// ✅ clamp the delay
const s = spring({frame: Math.max(0, frame - fr(delay)), fps: FPS});

// ❌ CSS transition/animation or setTimeout — non-deterministic & not frame-driven
<div style={{transition: 'opacity 300ms'}} />
// ✅ everything derived from useCurrentFrame()
<div style={{opacity: ease(frame, 0.2, 0.6)}} />

// ❌ left/top/width — reflows every frame
<div style={{left: interpolate(frame, [0, 30], [0, 200])}} />
// ✅ transform
<div style={{transform: `translateX(${interpolate(frame, [0, 30], [0, 200])}px)`}} />
```

## Data & facts

- Writing ambiguous data labels (average vs. maximum) → misleading claims. Always
  label fully + cite the source.
- Inventing per-word timestamps (splitting the duration evenly) → not alignment; use WhisperX /
  API timestamps / validated user timestamps.
- Visuals (bar lengths, object sizes, arrows) implying unproven causality →
  diagrams must have units, periods, honest scales, and sources.

## Visuals & audio

- Illustration clashing with text (e.g. a sun overlapping a text pill) → keep separate zones for
  text and illustration; check at the final keyframe of the motion, not just the start.
- Light text on a light green/yellow background has weak contrast → put a dark pill/card behind
  the text.
- Empty frame 0 → the hook must be visible immediately (start at scale 0.6 or opacity 0.4,
  not 0).

```tsx
// ❌ hook starts from complete emptiness
const s = spring({frame, fps: FPS}); // frame 0: scale 0
// ✅ frame 0 is already readable
const s = spring({frame, fps: FPS});
const scale = 0.6 + 0.4 * s;
```

- Video feels "dead" because it's only fading → apply Phase 4 (easing, overshoot, stagger, camera,
  ambient); entrances/transitions alone don't satisfy the main-action requirement.
- spring delays: `spr(f, delay)` takes SECONDS, not frames — passing frames (e.g. `spr(f, 18)`)
  silently delays the element 18s so it never appears in a short scene. Always sub-second values
  (0.1–0.6) for stagger.
- Inside `<Sequence>`, `useCurrentFrame()` is LOCAL but cues.json times are ABSOLUTE — mixing
  them is the #1 timing bug (bars never fill, entrances never play; QA Gate B catches it as a
  "frozen scene"). Always use `useSceneClock(id)` + `easeAt()` from helpers.tsx, or subtract
  the Sequence's `from` before passing absolute seconds to helpers.
- External components used raw (library default timing, magic FPS) → run the adaptation
  checklist in `references/elements-ecosystem.md`.
- Identical transitions at every boundary (automatic whoosh/thud) → violates 4.1b; pick a
  mechanism per boundary from the `transition_plan`.
- **Never use `-map 0:a` when muxing the mix into a rendered MP4:** if the video already has an
  audio stream (even silence), `-map 0:a` keeps the OLD audio — the final MP4 stays silent
  (QA Gate E catches it as full-duration silence). Always use `-map 0:v -map 1:a` (video from
  the render, audio from the mix).
- Final audio measured only on the WAV before AAC → loudness can shift; measure the final MP4.
- `-shortest` used to hide truncated audio → fix the frame count/duration;
  don't paper over it with a flag.

## Process

- Handing off a replacement version without re-running QA → for every replacement MP4, re-run Gate C
  on at least the affected parts (Phase 7.7).
- Credentials/API keys ending up in code, logs, READMEs, or zips → blocker; use environment
  variables/secret fields only (see SKILL.md & Phase 6.4).
- Installing technical dependencies (Camoufox, WhisperX, numpy/scipy) treated as a
  ask-first decision → wrong; installing tools to run an already-requested task is automatic.
  What does require asking: paid services (TTS), special assets, and
  content decisions.
