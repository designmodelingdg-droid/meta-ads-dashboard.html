# Video Direction

**Contents**

1. The density inversion — why video prompts are shorter
2. The block format
3. Camera motion vocabulary
4. Subject motion and timing
5. Keyframes: start_image and end_image
6. Multi-shot sequences and continuity
7. Audio direction
8. Duration, aspect ratio, and platform
9. Video failure modes

---

## 1. The density inversion

Image prompting rewards density. Video prompting punishes it.

An image model resolves one moment, so every additional specification constrains that moment further. A video model has to resolve a *sequence* — and every extra instruction is another thing it must satisfy at every frame. Give it three competing actions and it will try to do all three at once. That is what morphing is: the model interpolating between instructions it cannot satisfy simultaneously.

So the rule is **one camera idea, one primary subject action, per generation.** If the concept needs more, it needs more shots, not more adjectives.

This does not mean vague. "Slow 20cm dolly-in, subject holds still and blinks once" is short *and* precise. Precision comes from naming exactly one thing well.

The Structure/Reference/Vision pillars still apply — but in video, Structure is inherited from the start frame rather than written out. Which is the strongest argument for the still-first workflow.

---

## 2. The block format

Labelled blocks stop the model from blending camera movement into subject movement, which is the most common source of chaotic output.

```
SHOT: [what the frame contains, one sentence — skip this when a start_image carries it]
CAMERA: [one movement, its speed, its distance]
SUBJECT: [one primary action, with its timing]
LIGHT & ATMOSPHERE: [what changes over the duration, or "holds constant"]
AUDIO: [ambience, foley, dialogue in quotes, or "none"]
NEGATIVE: [artifacts to suppress]
```

Worked example:

```
CAMERA: slow push-in, roughly 30cm over the full clip, locked height, no shake
SUBJECT: she lifts the cup, takes one sip, sets it down; eyes stay on the window throughout
LIGHT & ATMOSPHERE: morning window light holds constant; steam drifts upward and left
AUDIO: quiet room tone, a single ceramic-on-wood clink, distant traffic
NEGATIVE: no camera shake, no zoom, no extra people, no morphing hands, no text
```

Every model in the catalog handles this format. Some accept looser prose, but none are hurt by the structure, and it makes revision surgical — a bad take usually means one block was wrong, not the whole prompt.

---

## 3. Camera motion vocabulary

**Translation** (the camera body moves)

- **Dolly in / out** — toward or away from the subject. Change *feels* like approach or withdrawal
- **Truck left / right** — sideways, revealing parallax between depth layers
- **Pedestal up / down** — vertical rise or fall, framing held
- **Push-in** — a slow dolly in, the workhorse of emphasis
- **Arc / orbit** — circling the subject, showing dimension. Expensive in coherence; keep it slow and partial

**Rotation** (the camera pivots in place)

- **Pan left / right** — horizontal sweep
- **Tilt up / down** — vertical sweep, good for reveals of scale
- **Whip pan** — fast blur, usually a transition rather than a shot

**Optical**

- **Zoom in / out** — focal length changes, perspective does not. Reads as surveillance or as amateur; use deliberately
- **Rack focus** — the focus plane travels between two subjects. Powerful and often mangled; specify both planes and the direction
- **Dolly zoom** — dolly one way while zooming the other. Vertigo. Almost always more than a model can hold; use only as the single idea in the clip

**Handling**

- **Locked off / tripod** — no movement at all. Massively underused. Stillness makes any subject motion read stronger, and it is the safest choice for a first generation
- **Handheld** — organic drift and micro-corrections
- **Gimbal / Steadicam** — smooth floating motion
- **Shoulder-mounted** — weightier, slower drift than handheld
- **Drone** — aerial rise, flyover, orbit
- **Crane / jib** — sweeping vertical arcs

**Speed matters as much as direction.** "Slow", "steady", "gradual" hold together; "fast", "rapid", "aggressive" invite artifacts. Quantify the amount when you can — "a 20cm push", "a 15° pan" — because a distance is unambiguous where "slight" is not.

---

## 4. Subject motion and timing

Describe motion as a **single continuous action with a clear beginning and end state**, not as a list of things that happen.

- Good: "he turns his head from the window to camera and settles"
- Bad: "he turns to camera, smiles, picks up the mug, gestures at the product, and laughs"

For a 5-second clip, one action is the budget. For 10 seconds, two at most, and say what separates them: "she reads for the first three seconds, then looks up."

**Timing language the models understand:** "at the start", "holds for the first two seconds", "midway through", "at the end", "throughout", "settles into stillness". Explicit beat maps help longer clips:

```
SUBJECT: 0–2s holds still, eyes down · 2–4s lifts head to camera · 4–5s the beginning of a smile, no more
```

**The stillness anchor.** Opening with one to three seconds of near-stillness lets the model lock character design, wardrobe, and geometry before it has to move anything. It measurably improves identity retention across the clip. Cheap, and almost always worth it.

**Physical plausibility.** Models simulate physics loosely. Actions with clear real-world mechanics — walking, pouring, turning, sitting — hold together. Actions requiring articulated fingers, tool use, or object permanence through occlusion tend to break. When a shot needs hands doing something precise, frame it so hands are large and central, or cut around it.

---

## 5. Keyframes: start_image and end_image

**start_image is the highest-leverage control in video generation.** It fixes composition, lighting, palette, wardrobe, and identity before a single frame is generated. Everything the image prompt earned carries into the clip for free, and the video prompt reduces to "what moves?"

Default workflow:

1. Build and generate the still with the full three-pillar treatment
2. Pass its `job_id` (or a `media_id`) as `medias: [{ value: "…", role: "start_image" }]`
3. Write only CAMERA / SUBJECT / AUDIO — the frame is already described

**end_image** defines where the shot lands. Two frames plus a duration is close to shot-level control, and it is how loops are made (same image as start and end). Models supporting both: `seedance_2_5`, `seedance_2_0`, `seedance1_5`, `minimax_h3`, `flux_3_video`, `kling3_0`, `wan3_0`, `wan2_7`, `cinematic_studio_3_0`.

When start and end frames differ a lot, the model has to invent the path between them. Keep the delta modest — a change of pose, not a change of scene — or the interpolation shows.

**Other reference roles** — `image_references` (style or identity guidance without fixing the frame), `video_references` (motion transfer or continuation), `audio_references` (drive timing from a track). Check `medias[].roles` per model before assuming a role exists.

---

## 6. Multi-shot sequences and continuity

Two paths to more than one shot.

**Generate separately and edit.** Full control per shot. Continuity has to be enforced by you.

**Generate multi-shot in one call.** `kling3_0` handles multi-shot natively; `cinematic_studio_video_v2` exposes `multi_shots` with a `multi_prompt`. Cheaper and cuts are handled internally, but per-shot control drops.

Whichever path, continuity is a written checklist, not a hope. Carry these values *identically* across every shot in a sequence:

- Focal length family (do not mix a 24mm and an 85mm inside one scene without meaning to)
- Key direction and color temperature
- Palette hex values
- Wardrobe, down to the garment
- Time of day and weather
- Grain, sharpness, and grade character

Then vary deliberately: shot size, angle, and subject action are what create rhythm. A sequence that changes lighting between shots reads as a mistake; one that changes only shot size reads as editing.

**Shot rhythm for short-form:** hook (0–2s, the strongest image), development (2–8s, the substance), payoff or loop point (final 2s). Vertical short-form tolerates faster cutting than horizontal — a 2-second average shot length is normal on TikTok and unwatchable on YouTube.

---

## 7. Audio direction

Several models generate native audio — `seedance_2_x`, `kling3_0`, `kling2_6`, `cinematic_studio_3_0`, `flux_3_video`, `wan3_0`, `wan2_7`, `veo3`, `gemini_omni`, `grok_video_v15`, `marketing_studio_video`. Most default `generate_audio` or `sound` to **on**.

**Turn it off** when the clip is going under a voiceover, a music bed, or into an edit with its own sound design. Generated audio under a track is noise, and it costs credits.

**When you want it, direct it in layers:**

- **Ambience** — the room or place: "quiet room tone", "distant traffic", "wind across an open field"
- **Foley** — specific sounds tied to the action: "ceramic set down on wood", "fabric rustle as he turns", "single footstep on gravel"
- **Dialogue** — put spoken lines in quotes and keep them short. Roughly two to three words per second is a realistic delivery rate; more than that and lip-sync breaks down
- **Music** — describe instrumentation and tempo, not a named artist

Example: `AUDIO: quiet café ambience, low espresso machine hiss, she says "this is the one", no music`

For dialogue-heavy work, generating silent video and adding audio in post (or via `sync_so` lipsync) gives more control than native generation.

---

## 8. Duration, aspect ratio, and platform

**Duration.** Most models sit in a 4–15 second range; `seedance_2_5` and `wan3_0` reach 30 seconds; `flux_3_video` reaches 20. Longer is not better — coherence degrades with length, and most short-form shots are under 4 seconds anyway. Generate the length you will actually use.

**Aspect ratio.** Set it explicitly, every time. Several models default to 16:9 — `marketing_studio_video` notably — and a vertical campaign rendered horizontally is a wasted generation. 9:16 for TikTok, Reels, and Shorts; 16:9 for YouTube and web; 1:1 for feed; 21:9 for cinematic.

**Resolution.** Draft at 480p or 720p while the prompt is still moving. Re-run the settled version at 1080p or 4K, or upscale with `upscale_video`. Iterating at 4K is the fastest way to empty a credit balance.

---

## 9. Video failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Faces morph or identity drifts | Too much motion too early; no identity anchor | Add a stillness anchor at the start; use `start_image`; shorten the clip |
| Limbs warp, hands melt | Complex articulated motion | Simplify the action; keep hands out of frame or large and central |
| Background swims or changes | Camera move too fast or too wide | Slow it down, shorten the travel, or lock the camera off |
| Nothing moves | Motion under-specified or contradicted by "still" language | Name the movement concretely with a distance or an angle |
| Chaotic, everything moves at once | Camera and subject instructions blended | Split into labelled CAMERA and SUBJECT blocks; cut to one idea each |
| Wrong pacing | Duration mismatched to the action | Match duration to the beat map; regenerate shorter |
| Unwanted speech or music | `generate_audio` defaulted on | Set it off, or direct the audio explicitly |
| Colors shift mid-clip | No grade anchor | Restate palette hex values and Kelvin in the prompt; use `start_image` |
| Text or captions appear | Model default | Add "no text, no captions, no subtitles" to the negative |
