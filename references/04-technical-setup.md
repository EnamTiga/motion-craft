# PHASE 5 — TECHNICAL SETUP

## 5.1 Environment check (run it, don't assume)

```bash
node -v && npm -v && ffmpeg -version | head -1
python3 -c "import numpy, scipy; print('numpy/scipy ok')"
nproc                                   # sandbox often has only 1 CPU
free -m                                  # RAM: do not start a full render when available RAM is very low; report and wait or ask
npx remotion browser ensure              # official path: installs Remotion's own Chrome Headless Shell
which chromium chromium-browser google-chrome 2>/dev/null
python3 -c "import camoufox; print('camoufox ok')" 2>/dev/null   # Camoufox only matters for Plan C (5.5); not required on the main path
/opt/hatch/bin/tts --help >/dev/null && echo tts-cli-ok          # optional, Muse only, when Mode D is selected
```

If `numpy/scipy` isn't installed: `pip install numpy scipy --break-system-packages`.
If browser tools are missing and the network blocks downloads, report the cause and
use the honest fallback in 5.5.

## 5.2 Scaffold the project

```bash
mkdir -p proj && cd proj && mkdir -p src public out
cat > package.json <<'EOF'
{"name":"video","version":"1.0.0","private":true,"dependencies":{"@remotion/bundler":"4.0.538","@remotion/cli":"4.0.538","@remotion/renderer":"4.0.538","react":"18","react-dom":"18","remotion":"4.0.538"}}
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
# copy helpers into src/ — the relative import './cues.json' assumes this layout
cp <skill-folder>/templates/helpers.tsx src/helpers.tsx
# generate src/cues.json from your structured plan (see templates/make_cues.py):
python3 <skill-folder>/templates/make_cues.py plan.json --out src/cues.json
npm install 2>&1 | tail -2
# typeface: install the @fontsource package for the typeface the agent chose in the style
# paragraph, then copy its files into public/ using the same local font loading pattern:
cp node_modules/@fontsource/<chosen-typeface>/files/<chosen-typeface>-latin-<weight>-normal.woff2 public/<chosen-typeface>-<weight>.woff2
```

Remotion version **4.0.538** is pinned: it was verified as the latest stable npm
version on 2026-10-23 (verification command: `npm view remotion version`). If the
version needs changing, pick one compatible Remotion package version set, pin it
in the lockfile, then re-test fully (still + short render + cues validator) before
any production render; don't assume a future `latest` is automatically compatible
without a re-test. For other aspect ratios/FPS, change the configuration in `cues.json` via the
cue builder; Root and components read from it. Don't store duplicate configuration.

**Remotion license:** the Free License covers individuals and organizations of up
to 3 people, including unlimited commercial use. A Company License is required
once an organization grows to 4 or more people involved.

User images: put them in `public/` and use `<Img src={staticFile('name.png')} />`
(import `Img` from `remotion`).

## 5.3 Render commands (proven pattern)

Default path: let Remotion install and use its own Chrome Headless Shell — no
`--browser-executable` flag:

```bash
npx remotion browser ensure
# quick single-frame test:
npx remotion still src/index.ts Main out/t.png --frame=60
# full render (foreground + timeout; don't run in background):
timeout <set per project, see the VM-safe flow below> npx remotion render src/index.ts Main out/video.mp4 \
  --concurrency=1 --codec=h264 --crf=20 --overwrite
```

Alternative only: pointing `--browser-executable=$CH` at a foreign browser binary
is not the main path. Only if you deliberately use a foreign browser binary: it
MUST pass the still test first, and results may differ from Remotion's pinned shell.

Pitfalls that have already occurred:
- **Background processes die** when the tool command finishes → always render in the
  foreground. Render time depends on FPS, duration, resolution, complexity, and resources;
  don't promise a fixed time.
- `--concurrency` must be ≤ CPU count (`nproc`). On 1 CPU, use `--concurrency=1`.
- Only if you deliberately use a foreign browser binary: it MUST pass the still test first, and results may differ from Remotion's pinned shell.
- Always test a few `still`s before the full render.

**VM-safe render flow (mandatory on this VM)** — do not skip a step:

1. Check RAM with `free -m`. Start a full render only when available RAM is loose
   enough for Node + Chrome Headless Shell; when available RAM is very low (on
   this VM it has been seen in the hundreds of MB), postpone and report — do not force it.
2. Stills first, mandatory: at minimum a still at the start, middle, and end frame
   of key scenes. Look at the results. A failed still means the full render is forbidden.
3. Run a short test render (a short slice of the same composition) before the full
   render whenever the composition or the Remotion version is used for the first time.
4. Run the full render in the foreground with `--concurrency=1` on this 2-core VM
   (the concurrency ≤ `nproc` rule above still holds) — never in the background.
5. Set the render timeout to fit 1080x1920 reality on 2 cores: the old `timeout 280`
   fence is an example for a short test only, NOT a full-render fence. For a full
   render, state the timeout explicitly per project after the short test, and
   never promise a completion time.

## 5.4 Workflow order

1. Settle the brief, assets, motion/transition/music plan; final audio/alignment if any →
   `make_cues.py` → `src/cues.json`
2. Write scene components in `src/Main.tsx` (using the 4.4 helpers, concepts from Phase 3)
3. If there is narration: get the final audio/alignment first per 6.4/6.5, lock the shared
   timing → `python3 make_audio.py` + loudnorm → `public/mix.wav` (Phase 6)
4. `still` at key points → contact sheet → **look** → fix
5. Full render → QA from the MP4 (Phase 7) → hand over (Phase 8)

## 5.5 Fallback if Remotion can't be installed/run

In Muse this HTML + Camoufox + ffmpeg path is **Plan C** (Plan A = Remotion +
`npx remotion browser ensure`; Plan B = Remotion + an alternative browser binary
that passed the still test). It is Plan C because Camoufox is not installed by
default and per-frame capture is slower than Remotion on 2 cores.

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
