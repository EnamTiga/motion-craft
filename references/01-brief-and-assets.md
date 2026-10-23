# PHASE 1 — ASK FIRST (MANDATORY)

## 1a. First read what the user sent

- **txt/md/document files:** read the contents, extract facts, goals, names, numbers. That is the primary source of facts.
- **Product/logo images:** look at the image. Note the dominant colors (PIL is fine), shapes, and text on the packaging. Images from the user can be used directly in the video (`<Img src={staticFile('photo.png')} />`).
- **If the user did not provide reference images/visual assets** — see the **"Image search & quality"** section below.
- **Reference videos:** don't just say "I've seen it". Analyze it with tools:

  ```bash
  ffprobe -v error -show_entries stream=width,height,r_frame_rate,duration -of compact ref.mp4
  mkdir -p ref && ffmpeg -y -loglevel error -i ref.mp4 -vf "fps=2,scale=270:-1" ref/%03d.png
  # detect scene changes (number of cuts = rhythm):
  ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -c pts_time
  ```

  Build a contact sheet from the frames, look at it, then summarize **the style to emulate**:
  cut rhythm, transition types, typography style, palette, motion speed, camera usage.
  You cannot "hear" audio, so if tempo matters, try `pip install librosa` to estimate BPM,
  or ask the user.
  **Copy the style only. Do not copy content, characters, logos, or copyrighted assets
  belonging to others.**

### Measured reference blueprint (required when a reference video exists)

A style summary is not enough. When the user provides a reference video, or one is selected from a named source (section 1a-4), measure it and write the artifact `reference-blueprint.md` in the project folder before the concept is locked. Start from `templates/reference-blueprint.md`; do not invent a new layout for it.

Rules:

- One row per shot. Shot boundaries come from scene detection plus manual correction against the extracted frames. A boundary that was not checked against frames says so in its measurement source column.
- Every number carries its measurement source, one of: `ffprobe`, `ffmpeg-scene-detect`, `frame-inspection`, `manual-correction`, or `source-plate` for a number reported by the source site and not re-measured. Never present a `source-plate` number as an own measurement.
- The header records the format card: duration, resolution, frame rate, aspect ratio, shot count, median shot duration, cuts per minute, estimated BPM with its estimation method, and, when the audio was measured, integrated loudness and true peak.
- The blueprint feeds Phase 3: its rhythm numbers (median shot duration, cuts per minute, and the beat grid when measured) are copied into the beat plan, and the blueprint path is recorded in the concept summary. An impression that is not in the blueprint does not enter the plan.
- Copy the method, never the footage, the content, the characters, or the logos (see the reference rule above).

- Don't ask about things already clear from the brief or references. Write those as
  **assumptions** in the summary.

## 1a-2. Image search & quality (if the user did not provide visual assets)

Searching for relevant images on the internet to **use directly in the video** is mandatory,
not just inspiration — once the topic/brief is clear, without asking the user to upload first.
Exception: the user forbids web search or explicitly requests illustrations only. If the
user provides images, prioritize their assets; search for supplements only when needed.

**Browser paths (in order):**
1. **Muse `image-search` CLI (main path in Muse):**
   `image-search "<query per scene>" --max-results 5 --language <code>`.
   Take `media_url` (the full image) and record `page_url` as provenance.
   Download with curl to `public/`, then run the PIL quality check below as usual.
2. **Browser harness tool** (if available in another harness) — use it directly.
3. **Keyless APIs** via curl: Openverse (`api.openverse.org/v1/images/`) or the
   Wikimedia Commons API → verify & download.
4. **Camoufox (last resort, see the note below).**
5. **All paths fail** → vector illustration for scenes that need it, REPORT in the final report.

**Camoufox (last resort only):** Camoufox is installed only with the user's
approval, only when paths 1-3 are blocked by repeated CAPTCHAs for the same
image need, and its installation is reported. In Muse, Camoufox is not the
main image search path and not the main render fallback. The snippet below is kept only as a
reference for that last-resort path:

   ```bash
   pip install "camoufox[geoip]" && python -m camoufox fetch
   ```
   ```python
   from camoufox.sync_api import Camoufox
   with Camoufox(headless=True) as browser:
       page = browser.new_page()
       page.goto("https://www.bing.com/images/search?q=<query per scene needs>")
       # grab thumbnails → open the full-resolution page/media URL → download (requests/curl)
   ```
   Camoufox is chosen for: anti-fingerprinting (image search doesn't quickly hit CAPTCHA),
   Playwright API, and reuse for the render fallback (Phase 5.5, Plan C in Muse).

**Asset count & variety follow each scene's needs**, not one image for the whole video.
Build a per-scene visual requirements list from the motion plan before searching.
Crop/zoom/rotation/recoloring of the same image **does not count as a new asset**;
vary subject, angle, activity, or context meaningfully. Abstract scenes may use
purpose-designed illustrations/diagrams; not every scene needs photos. Photos may be
reused for continuity/handoff when relevant. If no suitable image exists for a scene,
report it; use vector illustration, not an irrelevant photo.

**Technical quality of each image (check with PIL after download):**
- Determine the **final display size** in the layout (from the motion plan), then source ≥ **2×
  the display size** (headroom for cropping, pan/zoom, Phase 4 camera push-in). Example: a
  400×300 card on a 1080p canvas → source ≥ 800×600; full-bleed 1080p → source ≥ 2160px on
  the long side ideally. Must be sharp when rendered at 720p & 1080p.
- Reject: blur, upscaling, heavy compression artifacts (small file with large dimensions =
  sign of bad compression), cropped subjects, watermarks.
- Camera zoom beyond source resolution = major bug at Gate B.
- Verify subject identity (real people/products/places) — don't use images of other
  people/events as substitutes. Don't remove watermarks or bypass paywalls.

**Record `assets.json`** (concise): `scene → source_url → changes made`.
For every asset, record its origin kind in assets.json: `image-search`, `openverse`, `wikimedia`, `browser`, `camoufox`, `muse-generated`, or `user-supplied`, next to the source_url.
Useful for QA Gate A and revisions.

**Integration into choreography:** download to `public/`, check quality, then integrate into
the animation (crop, mask reveal, parallax, pan/zoom with easing). Don't let it become a
static photo slideshow. Photos must participate in the choreography (see Phase 4.1a).

## 1a-3. Muse generated images (complement only)

- Muse generated images are a **complement**, not a replacement for searched
  photos of real subjects (real people, products, real places). For real
  subjects, generated images are FORBIDDEN as visual evidence.
- Legitimate uses: abstract backgrounds, textures, concept illustrations, and
  visual props that do not claim to depict a real subject.
- Limit: maximum **4** images per chat request. Needs beyond 4 are planned per
  batch and reported, never promised all at once.
- Record every generated asset in `assets.json` with `source_url` set to the
  marker `muse-generated` plus a brief prompt summary, so Gate A can tell it
  apart from searched photos.
- The technical quality rules of 1a-2 (sharpness, watermarks, cropped subjects)
  still apply to downloads; for generated images, anatomical defects or garbled
  text in the image are reject reasons.

## 1a-4. Named reference sources (prompts and measured examples)

When the brief has no reference yet, or a chosen direction needs a proven rhythm, look at these two sources before the concept is locked. They are the only prompt galleries named by this skill. Other galleries are not named on purpose: unverified mirrors and duplicates of the same pool add no evidence.

1. **motion-graphics.org**: a small curated gallery (85 videos, checked 2026-10-23) with dated per-entry statistics and an honest per-entry label stating whether a prompt was shared. Use it as the entry point when picking a reference.
2. **prompt-motion.com**: a large gallery of results with verbatim creator prompts. Use it as the raw pool once a direction is chosen.

**Hard filter for prompts.** Most gallery prompts are one sentence long and carry no buildable information. A prompt from any source may be used as build input only when all three hold:

- the full prompt text is at least 500 characters long,
- it contains at least one measured number (a duration, a BPM, a frame rate, a resolution, a loudness value, a pixel size),
- it contains a timing or structure breakdown (named sections, a beat list, or a second-by-second plan).

A prompt that fails any point is ignored as build input. It may still be recorded in the reference blueprint as visual inspiration, with its URL and nothing more. Duplicate copies of the same prompt across entries or sites count once. The 500 character threshold is deliberate: the one-sentence prompts that dominate the galleries (about 150 characters, of the "go all out" kind) fall under it, and the structured prompts that carry a beat grid and a build spec (several thousand characters) pass it.

**Trust labels.** Every prompt or recipe taken from a source is labeled, in the reference blueprint header and again in the concept summary:

- Prompt kind: `original-prompt` (the verbatim text published by the creator) or `reproduction-recipe` (a reconstruction written by someone else).
- Verification status: `verified` (you opened the source page during this project and saw the prompt next to its result video) or `unverified` (seen only in an index, a FAQ, or a second-hand quote).

An unverified reproduction recipe never overrides a measured blueprint or a rule in this skill. Extract patterns and structure only: prompts belong to their creators, so do not copy a prompt verbatim into a commercial production.

## 1b. Send this ONE question message (adapt, drop what's already answered)

Format: numbered, each question has short (lettered) options so the user can answer
quickly, e.g. answers: `1b 2a 3c`. Always offer an "up to you" option.
**At most 6 questions in one message** — pick the ones that most determine the design;
the rest become assumptions recorded in the concept summary (see 1c). The list below is
a question bank, not a mandatory full form:

```
Before I build, answer briefly (anything can be "up to you"):

1. Where will it be published? a) Reels/TikTok/Shorts  b) Ads/Instagram feed  c) YouTube  d) Presentation/website
2. Aspect ratio & duration? a) 9:16 · 15s  b) 9:16 · 30s  c) 1:1 · 15s  d) 16:9 · 30s
3. Main message viewers should remember? (one sentence)
4. Points/features/facts that MUST appear + which is the main focus?
5. Source of facts? a) from you/documents  b) I search the web  c) mix. Any claims/numbers that are off-limits?
6. Visual mood? a) epic cinematic  b) fun playful  c) elegant minimalist  d) futuristic tech  e) retro  f) up to you
7. Brand: colors/fonts/logo/mascot? (if none, I'll pick a palette myself: a) yes  b) no)
8. Visual assets (ask only if needed): a) your images  b) licensed internet images + illustrations  c) illustrations only  d) up to you. If there are no reference images from you, the default is that I search licensed internet images to use in the video.
9. Music: a) energetic/epic  b) cheerful  c) chill/lofi  d) dramatic. SFX: a) dense  b) moderate  c) minimal
10. On-screen text: language? Any CTA at the end (provide its text)? Anything that must not appear?
11. Voice-over? a) Yes, create with the ElevenLabs API (mode C)  b) No (mode A)  c) Use audio I send (mode B)  d) Use Muse narration (mode D, only if offered in Muse)  e) Up to you.
```

Question 11 is the **voice-over mode selection** (see SKILL.md). Mode C: ask for language,
voice character, `model_id`, and `voice_id` (or offer to help pick from the official
API/documentation). Mode B: ask for the audio (and timestamps if available). Don't ask for
API keys in this form; handle credential delivery in Phase 6.
Offer option d ONLY when Muse is detected per SKILL.md; never print option d in other harnesses. Mode D: ask language and voice character only; there is no model_id, voice_id, or API key to ask for.

## 1c. After the user answers

- If the user answers "up to you / anything / go ahead" for something, use the **defaults**: 9:16,
  1080×1920, 30 fps, 15–20s, mood matching the product, palette from Phase 4.6, music and SFX
  density chosen per context (not always 120 BPM), no new narration unless requested
  (mode A), language following the user. If the user already sent narration audio (mode B), use
  that audio and match the duration to it, not the 15–20 second default.
- Write a **5–8 line concept summary** (main visual metaphor, scene flow, climax moment,
  palette, music tempo) and **immediately proceed to building without waiting for approval**, unless
  something important is genuinely missing. Ask again only when stuck, and only one
  question. For a launch or product film brief, compare the duration and the ending against the corpus benchmarks in `references/08-format-archetypes.md` and show that comparison in the summary.
