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

**The code below is a technical synthesis example, not an arrangement to copy.**
Design/modify the instrument functions, motifs, rhythm patterns, structure, and SFX dispatch to match
your new music/transition plan. If a function doesn't support a cue you chose, implement it
first; don't replace all cues with whooshes just because that's all that's available. Keep
the music, SFX, and narration stems for QA. If there is narration, add the narration stem and ducking
to the final mix; this instrumental example does not do that automatically.

`make_audio.py` is run from the project root and reads `src/cues.json`.

```python
import numpy as np, json, wave
from scipy.signal import butter, sosfilt
np.random.seed(7)
SR = 44100
cues = json.load(open('src/cues.json'))
DUR = cues['dur']; M = cues['music']; BEAT = 60.0 / M['bpm']; BAR = BEAT * 4
N = int(DUR * SR) + SR
music = np.zeros((N, 2)); drums = np.zeros((N, 2)); sfx = np.zeros((N, 2))

def tt(d): return np.arange(int(d * SR)) / SR
def place(buf, sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i < 0 or i >= N: return
    n = min(len(sig), N - i)
    l = np.cos((pan + 1) * np.pi / 4) * 1.4142; r = np.sin((pan + 1) * np.pi / 4) * 1.4142
    buf[i:i+n, 0] += sig[:n] * gain * l; buf[i:i+n, 1] += sig[:n] * gain * r
def filt(x, kind, f, order=3): return sosfilt(butter(order, f, btype=kind, fs=SR, output='sos'), x)
def noise(d): return np.random.randn(int(d * SR))
def sweep_tone(d, f0, f1, curve=1.0):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** curve; return np.sin(2 * np.pi * np.cumsum(f) / SR)
def sweep_noise(d, f0, f1, q=1.6):
    x = noise(d); out = np.zeros_like(x); W = 2048; H = 1024; win = np.hanning(W); nch = max(1, len(x) // H - 1)
    for k in range(nch):
        s = k * H; fc = f0 * (f1 / f0) ** (k / max(1, nch - 1)); seg = x[s:s+W]
        if len(seg) < W: break
        out[s:s+W] += filt(seg, 'band', [max(60, fc / q), min(SR / 2 - 500, fc * q)], 2) * win
    return out / (np.max(np.abs(out)) + 1e-9)

# ---- basic sounds
def kick():
    t = tt(.5); s = np.sin(2 * np.pi * np.cumsum(48 + 130 * np.exp(-t * 30)) / SR) * np.exp(-t * 8)
    s[:150] += np.random.randn(150) * 0.4 * np.linspace(1, 0, 150); return s
def clap():
    t = tt(.25); n = filt(noise(.25), 'band', [900, 3500], 2); e = np.exp(-t * 20) * 0.5
    for o in (0, .011, .022): e += np.exp(-np.clip(t - o, 0, None) * 120) * (t >= o)
    return n * e * 0.7
def hat(o=False):
    d = .22 if o else .07; return filt(noise(d), 'high', 7000, 2) * np.exp(-tt(d) * (18 if o else 70)) * 0.5
def impact():
    t = tt(1.6); return np.sin(2*np.pi*np.cumsum(28 + 70*np.exp(-t*5))/SR) * np.exp(-t*2.6) + filt(noise(1.6), 'low', 500, 2) * np.exp(-t*3.2) * 0.7
def thud():
    t = tt(.35); return np.sin(2*np.pi*np.cumsum(50 + 70*np.exp(-t*25))/SR) * np.exp(-t*12) + filt(noise(.35), 'low', 700, 2) * np.exp(-t*45) * 0.6
def pop():
    t = tt(.16); return np.sin(2*np.pi*np.cumsum(350 + 800*np.exp(-t*30))/SR) * np.exp(-t*30)
def plink():
    t = tt(.3); f = 700 + 900*np.exp(-t*25); return (np.sin(2*np.pi*np.cumsum(f)/SR) + .3*np.sin(4*np.pi*np.cumsum(f)/SR)) * np.exp(-t*16)
def tick(): return filt(noise(.03), 'high', 3000, 2) * np.exp(-tt(.03) * 160)
def bell(f, d=1.4):
    t = tt(d); s = 0
    for m, a, k in [(1, 1, 3), (2.76, .5, 5), (5.4, .3, 8), (8.93, .15, 12)]: s = s + a*np.sin(2*np.pi*f*m*t)*np.exp(-t*k)
    return s * 0.6
def sparkle(t0, pan=0):
    for i, fq in enumerate([880, 1318, 1760, 2637, 3520]): place(sfx, bell(fq, .9) * 0.5, t0 + i*.055, pan + (i-2)*.2, 0.5)
def whoosh(t0, d, f0, f1, gain=.8, pan=0):
    x = sweep_noise(d, f0, f1); place(sfx, x * np.sin(np.pi * np.linspace(0, 1, len(x))) ** 2, t0, pan, gain)
def riser(t0, d, gain=.8):
    x = sweep_noise(d, 250, 7000, 1.8); e = np.linspace(0, 1, len(x)) ** 2.2
    place(sfx, (x + sweep_tone(d, 180, 1500, 2.0) * .25) * e, t0, 0, gain)

# ---- music
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def chord(name):
    r = NOTE[name[0]]; rest = name[1:]
    if rest[:1] == '#': r += 1; rest = rest[1:]
    elif rest[:1] == 'b': r -= 1; rest = rest[1:]
    minor = rest.startswith('m') and not rest.startswith('maj'); root = 36 + r
    while root < 41: root += 12
    return [440 * 2 ** ((m - 69) / 12) for m in (root, root + (3 if minor else 4), root + 7)]
def pluck(f, d=.3):
    t = tt(d); return sum((1 / n**1.4) * np.sin(2*np.pi*f*n*t) * np.exp(-t*(9 + 4*n)) for n in range(1, 7))
def bass(f, d=.24):
    t = tt(d); s = np.sin(2*np.pi*f*t) + .5*np.sin(4*np.pi*f*t)*np.exp(-t*10) + .3*np.sin(6*np.pi*f*t)*np.exp(-t*14)
    return s * np.minimum(1, t / .004) * np.exp(-t * 4)
def pad(freqs, d, det):
    t = tt(d); s = sum(np.sin(2*np.pi*f*det*n*t) / n**1.5 for f in freqs for n in range(1, 9))
    return s * np.minimum(1, t / .7) * np.minimum(1, (d - t) / .7) / len(freqs)

breaks = M.get('breaks', []); FINAL = M['final']
def on(t): return t < FINAL and not any(a <= t < b for a, b in breaks)

# drums
t = 0.0; kicks = []
while t < FINAL:
    if on(t): place(drums, kick(), t, 0, .95); kicks.append(t)
    t += BEAT
for a, b in breaks:
    for tb in (a, b - 2 * BEAT, b - BEAT): place(drums, kick(), tb, 0, .5)
t = 0.0
while t < FINAL:
    if on(t):
        beat_in_bar = round((t % BAR) / BEAT)
        if t >= M.get('clap_from', 2.0) and beat_in_bar in (1, 3): place(drums, clap(), t, 0, .8)
        if t >= M.get('hat_from', 2.0):
            place(drums, hat(), t + BEAT / 2, .3, .8); place(drums, hat(), t + BEAT / 4, -.3, .45)
    t += BEAT
if M.get('build'):
    x, gap, a = M['build'][0], .25, M['build'][0]
    while x < M['build'][1]:
        place(drums, clap(), x, 0, .5 + .5 * (x - a) / (M['build'][1] - a)); gap = max(.0625, gap * .8); x += gap
    riser(M['build'][0] - 1.0, M['build'][1] - M['build'][0] + 1.0, .7)
duck = np.ones(N)
for k in kicks:
    i = int(k * SR); n = int(.4 * SR); e = 1 - .6 * np.exp(-np.arange(n) / SR * 9); seg = duck[i:i+n]; duck[i:i+len(seg)] = np.minimum(seg, e[:len(seg)])
# bass, arp, pad per bar
nb = int(np.ceil(FINAL / BAR)) + 1
for bi in range(nb):
    t0 = bi * BAR; ch = chord(M['bars'][bi % len(M['bars'])]); inbreak = any(a <= t0 < b for a, b in breaks)
    if on(t0):
        for k in range(8): place(music, bass(ch[0]), t0 + k * BEAT / 2, 0, .9)
        place(music, np.sin(2*np.pi*(ch[0]/2)*tt(BAR*.95)) * np.minimum(1, tt(BAR*.95)/.05) * np.minimum(1, (BAR*.95 - tt(BAR*.95))/.2), t0, 0, .45)
    if t0 >= M.get('arp_from', 0) and t0 < FINAL:
        if inbreak:
            for k in range(8): place(music, pluck(ch[k % 3] * 4, .5), t0 + k * BEAT / 2, ((k % 3) - 1) * .4, .28)
        else:
            notes = [ch[0]*2, ch[1]*2, ch[2]*2, ch[1]*4, ch[2]*2, ch[1]*2, ch[0]*4, ch[2]*4]
            for k in range(16): place(music, pluck(notes[k % 8]), t0 + k * BEAT / 4, ((k % 4) - 1.5) * .3, .35)
    if t0 < FINAL:
        g = .5 if inbreak else .32; pf = [x * 2 for x in ch]
        place(music, pad(pf, BAR, 1.003), t0, -.5, g); place(music, pad(pf, BAR, .997), t0, .5, g)
fc = [x * 4 for x in chord(M.get('final_chord', M['bars'][-1]))] + [chord(M.get('final_chord', M['bars'][-1]))[0] * 8]
place(music, pad(fc, 1.5, 1.003), FINAL, -.5, .55); place(music, pad(fc, 1.5, .997), FINAL, .5, .55); place(drums, impact(), FINAL, 0, .7)

# ---- SFX from cues
for e in cues['sfx']:
    t, ty, g, p, d = e['t'], e['type'], e.get('gain', .8), e.get('pan', 0), e.get('d')
    if   ty == 'impact': place(sfx, impact(), t, p, g)
    elif ty == 'thud':   place(sfx, thud(), t, p, g)
    elif ty == 'clap':   place(sfx, clap(), t, p, g)
    elif ty == 'pop':    place(sfx, pop(), t, p, g)
    elif ty == 'plink':  place(sfx, plink(), t, p, g)
    elif ty == 'tick':   place(sfx, tick(), t, p, g)
    elif ty == 'ticks':
        x = t
        while x < t + d: place(sfx, tick(), x, p, g); x += e.get('step', .1)
    elif ty == 'bell':    place(sfx, bell(e.get('f', 1318)), t, p, g)
    elif ty == 'sparkle': sparkle(t, p)
    elif ty == 'whoosh':  whoosh(t, d or .5, e.get('f0', 300), e.get('f1', 5200), g, p)
    elif ty == 'riser':   riser(t, d or 1.2, g)
    elif ty == 'rise':    place(sfx, sweep_tone(d, e.get('f0', 250), e.get('f1', 1000), 1.3) * np.sin(np.pi * np.linspace(0, 1, int(d * SR))) * .2, t, p, g)
    elif ty == 'shimmer': place(sfx, filt(noise(d), 'high', 5000, 2) * np.sin(np.pi * np.linspace(0, 1, int(d * SR))) * .12, t, p, g)

# ---- mix
n = int(DUR * SR)
mix = np.tanh((music * duck[:, None] * .55 + drums * .8 + sfx * .95) * .9)[:n]
fo = int(.8 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix = mix / np.max(np.abs(mix)) * .9
with wave.open('raw_mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print('audio ok', n / SR, 'seconds')
```

Run it and normalize, then **verify the numbers**:

```bash
python3 make_audio.py
ffmpeg -y -loglevel error -i raw_mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 44100 public/mix.wav
ffmpeg -nostats -i public/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
```

Target `I:` between −15 and −13 LUFS, `Peak:` ≤ −1.2 dBFS. If outside the target, repeat
loudnorm or adjust with `-af volume=XdB`.

Add new SFX types if the concept needs them (e.g. click, knock, water, typewriter): write
small functions with a swept sine + noise + exponential envelope, and add them to the SFX block.
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
