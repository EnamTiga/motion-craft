# motion-craft

An **After Effects-grade motion graphics video production** skill for coding agents &
harnesses — an 8-phase pipeline, evidenced 5-gate QA, music & SFX synthesized from code, a single
source of timing (`cues.json`), optional voice-over (no-narration / user-audio /
ElevenLabs modes).

> Install: `npx skills add <repo>/motion-craft` *(or copy this skill folder into your
> harness's skills directory)*

## Quick install (copy & paste)

Give your AI agent one message — it reads the repo and follows the skill:

```bash
npx -y skills add EnamTiga/motion-craft -g -y
```

Then tell your agent:

```
Read the motion-craft skill (SKILL.md) and follow it to make my video.
```

That's it — the skill is self-describing: the agent loads `SKILL.md`, which routes it
through the 8 phases and the reference files on demand. No extra configuration needed.

## Contents

```
SKILL.md                    entry: role, absolute rules, phase router, voice-over A/B/C
references/
  01-brief-and-assets.md    Phase 1 — ask first, visual assets (browser/Camoufox), image quality
  02-facts-and-concept.md   Phases 2–3 — labeled fact research, concept, motion plan, cues.json
  03-motion-standards.md    Phase 4 — AE-grade motion standards, anti-slop, Remotion rules (read-order note at top)
  04-technical-setup.md     Phase 5 — Remotion scaffold, render, fallback
  05-audio-design.md        Phase 6 — code-synthesized music/SFX, voice-over modes B & C
  06-qa-gates.md            Phase 7 — evidenced 5-gate QA (A–E) + Phase 8 handoff
  07-delivery.md            Phase 8 — delivery & report
  elements-ecosystem.md     external component curation + mandatory adaptation checklist
  anti-patterns.md          pitfalls that have actually happened, ❌/✅ format
templates/
  helpers.tsx               FPS/ease/spring/fr/scene helpers — utilities, not scene templates
  make_cues.py              plan → validated src/cues.json generator (enforces scene & transition rules)
  cues.schema.json          the cues.json contract schema
  cues.example.json         a complete cues.json example
scripts/qa_check.sh         automated QA: metadata, decode, loudness, black/freeze/silence
.github/workflows/validate.yml  CI: schema validation, make_cues positive/negative tests, language check, qa_check smoke test
```

## Where this skill sits

This skill is a **craft & QA layer**, not a Remotion tutorial. For Remotion technical
rules (API, render, captions), pair it with the official skill: `npx skills add
remotion-dev/skills`. Component libraries (remocn, snapcn, Remotion Elements) are used as
**building blocks** with an adaptation checklist — not as a replacement for choreography
(see `references/elements-ecosystem.md`).

## Prompt template for users

Send SKILL.md (or install the skill) to your AI session, then write briefly:

```
Make a video about <product/topic>. The target audience is <audience>. Here are my references:
<attach files/images/video if any>
```

The agent will ask once (platform, duration, mood, voice-over), then produce a complete video
with animation, music, and SFX — plus a QA report.

## License

MIT — see `LICENSE`.
