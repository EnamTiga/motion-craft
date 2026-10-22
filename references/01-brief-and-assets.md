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
- Don't ask about things already clear from the brief or references. Write those as
  **assumptions** in the summary.

## 1a-2. Image search & quality (if the user did not provide visual assets)

Searching for relevant images on the internet to **use directly in the video** is mandatory,
not just inspiration — once the topic/brief is clear, without asking the user to upload first.
Exception: the user forbids web search or explicitly requests illustrations only. If the
user provides images, prioritize their assets; search for supplements only when needed.

**Browser paths (in order):**
1. **Browser harness tool** (if available) — use it directly.
2. **None → install Camoufox** (automatic, NO need to ask — installing a technical
   dependency for an already-requested task is not a decision requiring approval):
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
   Playwright API, and reuse for the render fallback (Phase 5.5).
3. **Install fails** (network/permissions) → keyless APIs via curl: Openverse
   (`api.openverse.org/v1/images/`) or the Wikimedia Commons API → verify & download.
4. **All paths fail** → vector illustration for scenes that need it, REPORT in the final report.

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
Useful for QA Gate A and revisions.

**Integration into choreography:** download to `public/`, check quality, then integrate into
the animation (crop, mask reveal, parallax, pan/zoom with easing). Don't let it become a
static photo slideshow. Photos must participate in the choreography (see Phase 4.1a).

## 1b. Send this ONE question message (adapt, drop what's already answered)

Format: numbered, each question has short (lettered) options so the user can answer
quickly, e.g. answers: `1b 2a 3c`. Always offer an "up to you" option.

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
11. Voice-over? a) Yes, create with the ElevenLabs API (mode C)  b) No (mode A)  c) Use audio I send (mode B)  d) Up to you.
```

Question 11 is the **voice-over mode selection** (see SKILL.md). Mode C: ask for language,
voice character, `model_id`, and `voice_id` (or offer to help pick from the official
API/documentation). Mode B: ask for the audio (and timestamps if available). Don't ask for
API keys in this form; handle credential delivery in Phase 6.

## 1c. After the user answers

- If the user answers "up to you / anything / go ahead" for something, use the **defaults**: 9:16,
  1080×1920, 30 fps, 15–20s, mood matching the product, palette from Phase 4.6, music and SFX
  density chosen per context (not always 120 BPM), no new narration unless requested
  (mode A), language following the user. If the user already sent narration audio (mode B), use
  that audio and match the duration to it, not the 15–20 second default.
- Write a **5–8 line concept summary** (main visual metaphor, scene flow, climax moment,
  palette, music tempo) and **immediately proceed to building without waiting for approval**, unless
  something important is genuinely missing. Ask again only when stuck, and only one
  question.
