# PHASE 4 — MOTION STANDARDS (AFTER EFFECTS GRADE) — MANDATORY

> **Read order when context is tight:** 4.1a (scene cycle) and 4.1b (transition variety)
> are the two rules QA will fail you on — never skip them. 4.1 (principles) and 4.5
> (recipes) can be skimmed if you already know animation principles; 4.3–4.4 (Remotion
> rules, helpers) are mandatory once you write code.

## 4.1 Technique library: pick what fits the plan, with a written reason in the motion plan

- **Easing:** spring, `Easing.out(cubic)`, or ease-in-out are available options. Fast entry
  then decelerating; exits accelerating.
- **Anticipation → overshoot → settle:** the element pulls back slightly before launching,
  passes the target, then settles (spring with low damping).
- **Squash & stretch** on falling, bouncing, or impacting objects (scaleX/scaleY moving
  oppositely for a few frames).
- **Overlapping action & follow-through:** parts of an element move with different delays
  (a label trailing the object, a shadow trailing the subject).
- **Stagger:** elements of a group enter in sequence, for example roughly 0.067–0.133 seconds
  apart, converted to the project FPS.
- **Kinetic typography:** text appears per letter/word (mask reveal rising from below,
  scale-bounce, small rotation).
- **Depth & camera:** layers (background, midground, foreground), parallax, and a slow camera
  move are available, for example a push-in of 1.00 to 1.06, a small pan, or a rotation of
  at most 1.5 degrees.
- **Secondary motion options:** floating particles/dots, swaying ambience, slow
  rotation, "breathing" (scale ±2%), waves.
- **Meaningful transitions:** layered color wipes, circle iris, an object growing to fill
  the screen, shape morph, match-cut. A transition SFX matched to the mechanism is available
  for every transition.
- **Brief screen shake** (around 0.2–0.4 seconds as an example range, decaying, converted
  to project FPS) at impact moments.
- **Number count-up**, **path drawing** (stroke-dashoffset), **filling bars/meters** for
  data.
- **Rhythm:** key movements follow the narration's meaning/timestamps; use the music beat
  when it doesn't conflict. Hook ≤ 2.5s; frame 0 already shows the hook word. An unplanned
  static frame longer than 0.5 seconds is a major bug. A planned hold noted in the plan is allowed.
- **Readability:** key text stays fully visible ≥ 0.35s + 0.15s per word; text size
  ≥ 40 px in portrait; high contrast; portrait safe zones: x 60–1020, y 180–1650
  (avoid platform UI overlays).

## 4.1a Motion cycle of EVERY scene — after the transition it keeps animating

**The transition is only a bridge between scenes, not the entire animation.** Once the
transition finishes, the main object must perform an action that explains the scene's content.

1. **Entrance:** elements enter with anticipation, easing/spring, stagger, and settle.
   Objects, text, and shadows don't arrive simultaneously. The first frame still has a
   readable hook.
2. **Main action after the transition:** the object performs an action relevant to the message
   (opening, folding, assembling, connecting, comparing, drawing a line, transforming,
   shifting focus). Stopping after the entrance is not enough.
3. **Development mid/late scene:** show continued action or compositional change as the
   narration progresses. For scenes ≥3 seconds, there must be at least **two distinct main
   action beats after the entrance completes** (e.g. a main action then a continued action).
   The entrance/transition does not count as either of those beats. Short scenes still need
   at least one action after the entrance; don't force dense motion that hurts readability.
4. **Sustained secondary motion:** follow-through, parallax, subtle camera, object breathing,
   or ambient changes that support the main action. Direction and depth must stay consistent.
   **Particles, camera zoom, photo sway, progress bars, and running subtitles alone do not
   satisfy the main action requirement.**
5. **Exit / handoff:** elements prepare to become the bridge to the next scene, not suddenly
   vanish behind a wipe. Use objects/direction/composition that preserve visual continuity.

- Avoid "static poster + subtitle" or "slightly zoomed photo + text" scenes. Photos must
  participate in the choreography: revealing the part being discussed, meaningful
  crop/focus changes, being split into cards, rearranged, or serving as the connecting
  object. Don't fabricate photo content or treat synthetic parallax as real footage.
- Vary actions between scenes. Don't repeat the "title enters → cards enter → everything
  sways until the end" recipe in every scene.
- Apply the easing, anticipation, overshoot/settle, overlap, follow-through, stagger, and
  squash/stretch principles **according to the object's nature**; not every object must
  bounce. Calm moments for reading are fine, but staging stays alive and the next action
  is planned. Source labels, disclaimers, and subtitles may be held steady for readability.
- All motion must clarify meaning and attention hierarchy. Replacing monotony with random
  motion, constant shaking, or everything moving hard at once is forbidden.

The actions themselves are the agent's content choice; this section does not prescribe
which actions.

## 4.1b Varied and meaningful transitions — required, no monotony

- Choose transitions based on the content/shape/motion relationship between two scenes; **don't
  use the same wipe at every boundary**. A different color or direction of wipe alone doesn't
  count as a different transition mechanism.
- Don't use the same transition mechanism on two consecutive boundaries. For videos with ≥5
  scenes, use at least **3 relevant transition mechanisms**, while keeping the visual language
  the agent chose for this production.
- Favor **object continuity/handoff**, **match-cut**, **shape morph**, **connected layout
  changes**, or **camera moves with parallax**. Iris, occlusion/reveal, and layered wipes may
  be used selectively when they support the message. Don't shuffle effect types just to hit
  a variety count.
- Example relationships: photo frame → bill sheet; an open budget card becomes an
  education/health card; a circular plate shape → the pivot point of a scale; an opinion card
  → a comment box. These are pattern examples, not mandatory templates for every video.
- Transitions must end with **new action inside the destination scene**, not an object that
  immediately freezes. Provide anticipation before and follow-through after the move.
- Each transition's SFX follows its mechanism (paper fold, slide, soft click, swoosh,
  impact as appropriate); don't automatically attach an identical whoosh/thud at every
  boundary.
- Implement `transition_plan` and per-scene action cues in the shared timing source
  `cues.json`. Helper kits are only building blocks; not a reason to keep copying the same
  transitions/motion.

## 4.2 Visual style

- Visual treatment follows the style paragraph for this production. Bold basic shapes and
  rounded corners are examples, not requirements. When using internet images per Phase 1a,
  integrate them with consistent layout and motion.
- **"AI slop" is forbidden:** tacky gradient meshes, excessive glow, blurred light rays,
  glassmorphism, generic stock photos, emoji as illustration, random decorations that don't
  support the message.
- Don't redraw brand logos/mascots from approximation. Use the user's original files, or
  don't show them.
- Don't use third-party characters/IPs/brands as decoration or copy them without permission.
  Referential assets relevant to the topic may be used when the context is right
  (verify subject identity in Phase 1a); don't imply endorsement or affiliation.

## 4.3 Mandatory Remotion rules

- All animation derives from `useCurrentFrame()`. **Forbidden:** CSS `transition`/`animation`,
  `setTimeout`, and `Math.random()` (breaks render determinism). For randomness use
  `random('seed')` from `remotion`.
- `spring` with negative frames can misbehave; always use `Math.max(0, frame - delay)`.
- Inside a `<Sequence>`, `useCurrentFrame()` is **local** to the sequence start.
- SVG vs HTML text: use an HTML `div` for long/wrapping text, SVG for illustration.

## 4.4 Configuration and helpers — one source of FPS, not a scene template

Use the configuration from `cues.json` for the **entire** project. The 30 fps default only
applies when the user hasn't specified an FPS. Don't hardcode FPS/dimensions again in Root,
components, audio, subtitles, or the fallback render. Ready-made helpers:
`templates/helpers.tsx` (same content as below).

```tsx
import {Easing, interpolate, spring} from 'remotion';
import cues from './cues.json';
export const FPS = cues.fps, W = cues.width, H = cues.height;
export const fr = (seconds: number) => Math.round(seconds * FPS);
export const totalFrames = Math.ceil(cues.dur * FPS);
export const ease = (frame: number, startSeconds: number, endSeconds: number, from=0, to=1) =>
  interpolate(frame, [fr(startSeconds), fr(endSeconds)], [from, to], {
    easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
export const spr = (frame: number, delaySeconds=0) => spring({
  frame: Math.max(0, frame-fr(delaySeconds)), fps: FPS,
  config: {damping: 13, stiffness: 170, mass: 0.8},
});
```

- Timing numbers passed to helpers come from cue events, not new timing invented in
  components. Design entrance, stagger, shake, squash, and transition durations in seconds,
  then convert with `fr()`. A "3 frame" recipe at 30 fps means 0.1 seconds; at 60 fps it
  becomes 6 frames, not still 3.
- `spring` uses the project FPS; sinusoidal/ambient motion is based on seconds (`frame/FPS`)
  and per-second speeds. Random seeds stay deterministic.
- Load local fonts and wait for them with `delayRender/continueRender` before
  still/render. Font failure is a QA bug, not a reason to silently swap the layout.
- Implement scenes from the motion plan, not repeated helpers. Subtitles, camera, and
  particles alone don't satisfy the main action requirement.
- Implement transitions **per boundary** from `transition_plan`. No global wipe component
  for all boundaries. If a handoff object crosses scenes, place it in a shared layer with
  controlled coordinates and z-order.
- When the FPS changes, validate that cue times in seconds stay the same and check the
  actual rendered output; 60 fps doesn't automatically guarantee smooth motion if the
  animation still jumps in large steps.

## 4.5 Motion recipes per element type (pick what fits, combine)

No row in this table is required (example only, not required). The agent may invent motions
that do not appear in this table; QA checks motion against the plan, not against this table.

| element | motion |
|---|---|
| Title | kinetic per word/letter + overshoot; at the climax scale-slam + shake |
| Main object | enters with spring, then "breathes" ±2% with constant slight rotation |
| Numbers/data | count-up with ease-in-out, tick SFX per step, stamp/ding on completion |
| Charts/meters | filling with ease, self-drawing lines (DrawPath) |
| Cards/lists | enter from the side with stagger around 0.1–0.133 seconds, overshoot |
| Falling/landing objects | acceleration, squash on landing, thud + dust particles |
| Transformation (before → after) | old object shrinks (reverse spring), new object grows ~0.1–0.133 seconds later at the same point |
| Background | 3-layer parallax, particles, swaying ambient elements |
| Transition | Chosen per boundary based on object/message relationships: handoff, match-cut, morph, layout change, camera move, iris, or selective wipe. Follow 4.1b, not a global wipe. |
| Scene content after the transition | Main action explaining the message → continued action as narration develops → handoff; camera/ambient/subtitles alone aren't enough. Follow 4.1a. |

## 4.6 Palette & typography

Palette and typography: the agent chooses both for each production and records the choice
and the reason in the style paragraph. Brand supplied by the user wins. Readability
thresholds still apply: contrast target 4.5:1 and the minimum text sizes in Section 4.1.
