#!/usr/bin/env python3
"""make_cues.py — THE ONLY place timeline numbers are written.

Reads a structured brief + motion plan (JSON), validates them, and emits src/cues.json
consumed by the Remotion composition, audio synthesis, subtitles, and QA.

ADAPT THIS FILE: the argument schema below is a contract example, not a rigid format.
Keep the validation section intact — it is what guarantees visual/audio/QA agreement.

Usage:
    python3 make_cues.py plan.json           # writes src/cues.json
    python3 make_cues.py plan.json --out out/cues.json

plan.json minimal shape (fields omitted → defaults shown):
{
  "fps": 30, "width": 1080, "height": 1920,
  "dur": 18.5,                       # seconds; must cover the full audio
  "scenes": [
    {"id": "s1-hook", "start": 0.0, "end": 3.4,
     "entrance": {"t": 0.0, "action": "...", "duration": 0.6},
     "mainActions": [{"t": 1.2, "action": "...", "duration": 1.2}, ...],
     "continueAction": {"t": 3.1, "action": "..."},
     "exit": {"t": 3.3, "action": "..."},
     "handoff": "object that bridges to the next scene"}
  ],
  "transition_plan": [{"at": 3.4, "mechanism": "morph", "duration": 0.3,
                       "connector": "...", "direction": "...", "reason": "...", "sfx": "paper-fold"}],
  "voiceover": {"audioFile": "public/vo.mp3", "source": "whisperx",
                "wordTimings": [{"word": "Hi", "start": 0.4, "end": 0.7}]},   # optional
  # muse-tts example: {"audioFile": "public/vo.mp3", "source": "muse-tts", "segmentTimings": [{"text": "Halo", "file": "public/vo-seg-01.mp3", "start": 0.0, "end": 1.2}]}
  "sfx": [{"t": 0.0, "type": "impact", "gain": 0.9}],
  "music": {"bpm": 108, "bars": ["C","G","Am","F"], "final": 18.0}
}

See templates/cues.schema.json (the output contract) and templates/cues.example.json.
"""
import argparse
import json
import math
import os
import sys

FAIL = []


def err(msg):
    FAIL.append(msg)


def load(path):
    with open(path) as f:
        return json.load(f)


def validate(p):
    fps, dur = p.get("fps", 30), p["dur"]
    frames = math.ceil(dur * fps)
    p.setdefault("width", 1080)
    p.setdefault("height", 1920)
    p["frames"] = frames

    scenes = p.get("scenes") or err("scenes missing")
    if scenes:
        # bounds derived, not hand-written — one source only
        p["bounds"] = [scenes[0]["start"]] + [s["end"] for s in scenes]
        if abs(p["bounds"][-1] - dur) > 1 / fps:
            err(f"last scene end {p['bounds'][-1]} != dur {dur}")
        prev_end = None
        for s in scenes:
            if s["start"] >= s["end"]:
                err(f"scene {s.get('id')}: start >= end")
            if prev_end is not None and abs(s["start"] - prev_end) > 1 / fps:
                err(f"scene {s.get('id')}: gap/overlap at {s['start']} (prev end {prev_end})")
            prev_end = s["end"]
            for k in ("entrance", "exit"):
                if k not in s:
                    err(f"scene {s.get('id')}: missing {k}")
            mains = s.get("mainActions", [])
            dur_s = s["end"] - s["start"]
            need = 2 if dur_s >= 3.0 else 1
            if len(mains) < need:
                err(f"scene {s.get('id')}: {dur_s:.1f}s needs >= {need} mainActions, has {len(mains)}")
            for e in [s["entrance"], *mains, s.get("exit"), s.get("continueAction")]:
                if e and not (0 <= e["t"] <= dur):
                    err(f"scene {s.get('id')}: cue t={e['t']} outside [0,{dur}]")

    # transitions: one per boundary, no identical consecutive mechanisms
    tp = p.get("transition_plan") or []
    if not isinstance(tp, list):
        err("transition_plan must be a list")
        tp = []
    bounds = [s["end"] for s in scenes[:-1]] if scenes else []
    if len(tp) != len(bounds):
        err(f"transition_plan has {len(tp)} entries, boundaries = {len(bounds)}")
    for i, t in enumerate(tp):
        if bounds and abs(t["at"] - bounds[i]) > 1 / fps:
            err(f"transition {i}: at={t['at']} != boundary {bounds[i]}")
        if i > 0 and t.get("mechanism") == tp[i - 1].get("mechanism"):
            err(f"transition {i}: mechanism '{t.get('mechanism')}' repeats consecutively (violates 4.1b)")
        mech = t.get("mechanism", "")
        if len({x.get("mechanism") for x in tp}) < 3 and len(scenes) >= 5:
            err(">=5 scenes need >=3 distinct transition mechanisms (4.1b)")

    # sfx
    for e in p.get("sfx", []):
        if not (0 <= e["t"] <= dur):
            err(f"sfx {e.get('type')} t={e['t']} outside [0,{dur}]")
        if e.get("type") == "ticks" and not e.get("d"):
            err("sfx 'ticks' needs d (duration)")

    # voiceover word timings
    vo = p.get("voiceover")
    if vo:
        words = vo.get("wordTimings", [])
        last = -1.0
        for w in words:
            if w["start"] > w["end"]:
                err(f"vo word '{w['word']}': start > end")
            if w["end"] > dur:
                err(f"vo word '{w['word']}': end {w['end']} > dur {dur}")
            if w["start"] < last - 0.05:
                err(f"vo word '{w['word']}': out of order")
            last = w["end"]
        if vo.get("source") not in ("elevenlabs", "whisperx", "user-supplied", "muse-tts"):
            err(f"vo source '{vo.get('source')}' invalid")
        if vo.get("source") == "muse-tts" and vo.get("wordTimings"):
            err("vo muse-tts must not carry wordTimings; use segmentTimings/captions")
        segs = vo.get("segmentTimings")
        if segs:
            last_start = None
            for seg in segs:
                if seg["start"] >= seg["end"]:
                    err(f"vo segment '{seg.get('text', '')}': start >= end")
                if seg["end"] > dur:
                    err(f"vo segment '{seg.get('text', '')}': end {seg['end']} > dur {dur}")
                if last_start is not None and seg["start"] < last_start - 0.05:
                    err(f"vo segment '{seg.get('text', '')}': out of order")
                last_start = seg["start"]

    m = p.get("music") or err("music missing")
    if m and (not m.get("bpm") or not m.get("bars")):
        err("music needs bpm + bars")
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--out", default="src/cues.json")
    args = ap.parse_args()

    p = validate(load(args.plan))
    if FAIL:
        print("VALIDATION FAILED — fix the plan before rendering:")
        for f in FAIL:
            print("  -", f)
        sys.exit(1)

    out = args.out
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)
    print(f"cues ok: {p['width']}x{p['height']} @ {p['fps']}fps, {p['dur']}s ({p['frames']} frames) -> {args.out}")


if __name__ == "__main__":
    main()
