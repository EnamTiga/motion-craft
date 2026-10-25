# Elements Ecosystem — building blocks, not the finished product

External Remotion component libraries are used as **pattern references and building blocks**.
They do NOT replace the motion plan, scene choreography, or transition plan — those are
always designed from Phase 3, not assembled from lined-up components.

## Source catalog (priority order)

| Priority | Source | How to get it | When to use |
|---|---|---|---|
| 1 | **remocn** (github.com/Remocn/remocn) | `npx shadcn@latest add @remocn/<name>` — code lands in your project, you own it | Common primitives: text reveal, transitions, kinetic titles |
| 2 | **snapcn** (github.com/shadcn-labs/snapcn) | `npx shadcn@latest add @snapcn/<name>` | Software product demos: terminal simulators, device frames, AI chat streams, karaoke captions, cursor tracking |
| 3 | **Remotion Elements** (remotion.dev/docs/elements) | copy from the docs | Backgrounds, data cards (bar chart, number counter), lower thirds, title cards |
| 4 | remotion-bits / Onda | npm / jsrepo | Special needs not covered by 1–3 |

## MANDATORY adaptation checklist (5 points) — before an external component is used

1. **Timing from `cues.json`** — all component time numbers are replaced with cue events; the
   library's built-in `durationInFrames` prop is removed. No second timing source in the component.
2. **FPS/dimensions from the `fr()`/`FPS` helpers** (Phase 4.4) — convert the library's magic
   frame numbers (written for 30 fps) into seconds → `fr()`.
3. **Choreography stays yours** — entrance → main action → follow-up action → handoff still
   comes from the motion plan. Elements fill in the pieces; a scene must not be just
   lined-up drop-in components.
4. **Transitions still come from `transition_plan`** — don't use the library's default transitions.
   External components usually lack context about your scene-to-scene handoff.
5. **Determinism and the 4.3 rules still apply** — audit incoming code: `Math.random()`,
   `setTimeout`, CSS animations, and out-of-context `useCurrentFrame()` must
   be fixed; springs without `Math.max(0, frame - delay)` cleaned up.

## Example: before vs after adaptation

```tsx
// ❌ Raw drop-in: library's own timing, not bound to cues
<TextReveal text="Save 40%" />
// (the component has internal timing of 90 frames @ 30fps — wrong in a 60fps project,
//  and it has no idea when to appear according to cues.json)

// ✅ Adapted: timing from cues, FPS from the helper, choreography from the motion plan
const cue = cues.scenes[2].mainAction; // {t: 6.4}
<Sequence from={fr(cue.t)} durationInFrames={fr(1.5)}>
  <TextReveal text="Save 40%" /> {/* component already refactored: fr(), no internal timing */}
</Sequence>
```

## Hard boundaries

- **Forbidden** to build the video by just sticking elements side by side → that's exactly
  the "cheap template" that Phase 4.2 calls AI slop; it violates 4.1a (a main action per scene)
  and 4.1b (monotonous transitions).
- This catalog is a **reference map** — component names and install methods can change;
  check the source repo when you're about to use one. If the install fails or the name doesn't exist, don't
  invent component names; write it yourself from the motion plan (that's always possible).
- Priority stays the same: the base treatment is the treatment the agent chose in the style
  paragraph for this production; elements are used when they speed things up without homogenizing the result.
