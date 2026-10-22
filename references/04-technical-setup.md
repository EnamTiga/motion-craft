# PHASE 5 — TECHNICAL SETUP

## 5.1 Environment check (run it, don't assume)

```bash
node -v && npm -v && ffmpeg -version | head -1
python3 -c "import numpy, scipy; print('numpy/scipy ok')"
nproc                                   # sandbox often has only 1 CPU
which chromium chromium-browser google-chrome 2>/dev/null
python3 -c "import camoufox; print('camoufox ok')" 2>/dev/null
```

If `numpy/scipy` isn't installed: `pip install numpy scipy --break-system-packages`.
If browser tools are missing and the network blocks downloads, report the cause and
use the honest fallback in 5.5.

## 5.2 Scaffold the project

```bash
mkdir -p proj && cd proj && mkdir -p src public out
cat > package.json <<'EOF'
{"name":"video","version":"1.0.0","private":true,"dependencies":{"@fontsource/poppins":"*","@remotion/bundler":"4.0.240","@remotion/cli":"4.0.240","@remotion/renderer":"4.0.240","react":"18","react-dom":"18","remotion":"4.0.240"}}
EOF
cat > tsconfig.json <<'EOF'
{"compilerOptions":{"target":"ES2020","module":"ESNext","moduleResolution":"node","jsx":"react-jsx","strict":false,"resolveJsonModule":true,"esModuleInterop":true,"skipLibCheck":true}}
EOF
cat > src/index.ts <<'EOF'
import {registerRoot} from 'remotion';
import {Root} from './Root';
registerRoot(Root);
EOF
cat > src/Root.tsx <<'EOF'
import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import cues from './cues.json';
export const Root: React.FC = () => (
  <Composition id="Main" component={Main} durationInFrames={Math.ceil(cues.dur * cues.fps)} fps={cues.fps} width={cues.width} height={cues.height} />
);
EOF
npm install 2>&1 | tail -2
cp node_modules/@fontsource/poppins/files/poppins-latin-900-normal.woff2 public/pop-900.woff2
cp node_modules/@fontsource/poppins/files/poppins-latin-600-normal.woff2 public/pop-600.woff2
```

Remotion version **4.0.240 has worked in previous testing**, but the current environment
must still be verified. If the version needs changing, pick the same compatible Remotion
package version set, pin it in the lockfile, then re-test; don't assume `latest` is
compatible. For other aspect ratios/FPS, change the configuration in `cues.json` via the
cue builder; Root and components read from it. Don't store duplicate configuration.

User images: put them in `public/` and use `<Img src={staticFile('name.png')} />`
(import `Img` from `remotion`).

## 5.3 Render commands (proven pattern)

```bash
CH="/actual/path/from-detection/chrome-headless-shell" # substitute from your check; don't run the placeholder
# If the CLI manages its own browser, the --browser-executable flag can be omitted.
# quick single-frame test:
npx remotion still src/index.ts Main out/t.png --frame=60 --browser-executable=$CH
# full render (foreground + timeout; don't run in background):
timeout 280 npx remotion render src/index.ts Main out/video.mp4 \
  --browser-executable=$CH --concurrency=1 --codec=h264 --crf=20 --overwrite
```

Pitfalls that have already occurred:
- **Background processes die** when the tool command finishes → always render in the
  foreground. Render time depends on FPS, duration, resolution, complexity, and resources;
  don't promise a fixed time.
- `--concurrency` must be ≤ CPU count (`nproc`). On 1 CPU, use `--concurrency=1`.
- Use `chromium_headless_shell` (not full chromium) via `--browser-executable`.
- Always test a few `still`s before the full render.

## 5.4 Workflow order

1. Settle the brief, assets, motion/transition/music plan; final audio/alignment if any →
   `make_cues.py` → `src/cues.json`
2. Write scene components in `src/Main.tsx` (using the 4.4 helpers, concepts from Phase 3)
3. If there is narration: get the final audio/alignment first per 6.4/6.5, lock the shared
   timing → `python3 make_audio.py` + loudnorm → `public/mix.wav` (Phase 6)
4. `still` at key points → contact sheet → **look** → fix
5. Full render → QA from the MP4 (Phase 7) → hand over (Phase 8)

## 5.5 Fallback if Remotion can't be installed/run

State the cause. Then: a time-controlled HTML page (`window.render(t)`), capture frames
with **Camoufox** (Python, Playwright API — see 1a; if not installed:
`pip install "camoufox[geoip]" && python -m camoufox fetch`), assemble with ffmpeg:

```python
# frame capture pattern (adapt): open the page via file://, call window.render(t) per frame,
# page.screenshot() → frames/f%04d.png, frame count = ceil(dur * FPS) from cues.json
```

```bash
ffmpeg -framerate "$FPS" -i frames/f%04d.png -i mix.wav -c:v libx264 -pix_fmt yuv420p -c:a aac out.mp4
```

Frame count and audio duration must already match; don't use `-shortest` to hide truncated
audio. Animation quality must still meet Phase 4.
Report that this is the fallback path.
