---
name: higgsfield-art-director
description: Turns a vague visual idea into a production-ready image or video prompt using a three-pillar method (Structure, Reference, Vision), routes it to the right Higgsfield model, and generates it through the Higgsfield MCP when connected. Use this whenever someone wants an AI image or video that should look intentional rather than random — product and e-commerce ads, YouTube thumbnails, UGC clips, B-roll, character and avatar scenes, editorial stills, posters, brand visuals. Trigger it when a user shares a reference and says "recreate this" or "make it like this"; when they say "write me a prompt", "make this look professional", "why does my generation look fake / plastic / AI", "prompt for Soul 2 / Nano Banana / Seedance / Kling / Veo / GPT Image", or ask which Higgsfield model to use; when they want a still animated into video; and also when they just describe an image or video they want without ever saying "prompt". Prefer this over improvising a prompt — every unstructured attempt burns real generation credits.
license: MIT
---

# Higgsfield Art Director

## Why this works

Two people ask the same model for the same shot. One gets AI slop; the other gets something that looks like it was shot on assignment. The difference is not a magic word. It is that the second person specified the **photograph** instead of describing the **subject**.

The model is not feeling your adjectives. When you write "dramatic," it pattern-matches thousands of images tagged dramatic and returns their average. Average is exactly what you get back. When you write "single hard key from camera-left at 45°, deep unfilled shadow side, 3200K," you have named the thing that *causes* drama — and there is nothing left to average.

So the entire job is translation: take what the person feels, convert it into what a camera and a light actually do, and hand the model a specification instead of a wish.

Work through six moves. Skip any that the situation has already answered.

---

## 1. Read the situation

Two questions decide everything downstream.

**Which mode?**

- **Reference mode** — an image or video was attached, or a link to one. The reference already answers most variables. Extract them instead of asking. Jump to move 3.
- **Concept mode** — an idea in words only. The variables live in the person's head and must be drawn out before writing anything. Go to move 2.
- **Repair mode** — a generation came back wrong. Do not rewrite blindly; diagnose which pillar failed (see "When a result comes back wrong" near the end).

**Which job?** Name it in one phrase — *product ad on white*, *YouTube thumbnail*, *UGC talking head*, *B-roll insert*, *editorial portrait*, *character turnaround*, *brand poster*. The job sets the aspect ratio, the model, and the acceptable level of polish. A UGC clip that looks like a commercial has failed; a commercial that looks like UGC has also failed.

If a brand kit is configured — a file the user points to, something in project docs, or a spec they paste — read it now and apply its palette, banned words, and defaults throughout. `references/brand-kit-template.md` is the template to hand someone who does not have one yet.

---

## 2. Lock the variables before writing (concept mode only)

Guessing produces revision cycles, and every cycle spends real credits. Questions are cheaper than regenerations, so ask — but ask like a director running a pre-pro meeting, not like a form.

Ask only what is genuinely unresolved, as multiple choice with concrete options plus an open path, **2–4 questions per round, two rounds maximum**. Then write once, completely.

The variables worth locking:

1. **Format** — aspect ratio and where it will be seen (9:16 Reel, 4:5 feed, 16:9 YouTube, 1:1 catalog, 21:9 cinematic)
2. **Environment** — location, time of day, interior or exterior
3. **Subject specifics** — wardrobe, product, props, and whether identity comes from a reference
4. **Mood** — the one feeling the frame should transmit, in plain words
5. **Realism target** — raw and handheld, clean commercial, or stylized/illustrated
6. **Palette** — faithful to a reference, brand-locked, or open

Anything they leave open, decide yourself and log the decision in the ASSUMPTIONS line. A delivered prompt with three stated assumptions beats a third round of questions.

---

## 3. Build with the three pillars

Every prompt — reverse-engineered or built from nothing — is assembled from three layers. Structure and Reference are craft. Vision is what makes the craft cohere.

### Pillar 1 — STRUCTURE (the technical foundation)

The engineering that makes everything else possible. Most people skip it entirely, which is exactly why their images lack intention.

- **Camera** — focal length in mm, aperture, shutter and ISO when motion or grain matter, angle, camera height, shot type, distance
- **Lighting** — source, direction, quality (hard/soft), color temperature in Kelvin, contrast ratio, shadow behavior, practicals in frame
- **Materials** — surface properties, wear and texture, how each surface answers the light, environmental interaction (dust, moisture, haze)
- **Composition** — framing, negative space, foreground/midground/background layers, leading lines, where the depth of field falls

### Pillar 2 — REFERENCE (the style anchor)

Where the image sits in visual history. This is extraction and synthesis, not copying: take the lighting philosophy from one tradition, the mood from another, the texture from a third.

- Photographic or artistic tradition and era
- Analog versus digital character — grain, halation, sharpness profile, chromatic behavior
- One or two named anchors, and only when they genuinely fit. A forced reference muddies the output more than no reference at all.

### Pillar 3 — VISION (the emotional intent)

The question everything else answers: **what should someone feel looking at this?** Then, and this is the part that matters — name the technical mechanism that produces the feeling. Vision without mechanism is a mood board; vision with mechanism is a shot.

> intimate authority = low camera height + warm 3200K practicals + tight 85mm compression
> unfiltered immediacy = handheld 35mm + 1/30s drag + flat overcast key + visible grain

When the three pillars agree with each other, the frame reads as one intentional decision. When they fight — glossy commercial lighting on a raw documentary concept — the output looks like AI, because incoherence is the actual signature of AI slop.

### The priority hierarchy

Prompt elements do not carry equal weight. When space is limited or the model is drifting, spend the words in this order:

1. **Camera and lens** — establishes perspective and depth relationships
2. **Lighting architecture** — creates mood, defines form, controls contrast
3. **Subject and composition** — defines content and visual organization
4. **Material reality** — the layer that buys believability
5. **Environmental context** — narrative support and authenticity
6. **Style references** — places the work in a tradition

A prompt that nails 1 and 2 and skips 6 still looks professional. The reverse never does.

### Reverse-engineering a reference

In reference mode, run the deconstruction silently — do not narrate it beat by beat — and read it back as a built prompt. What to look for:

- **Technical**: focal length signature (compression or distortion), depth of field, camera height and angle, key direction and quality, contrast ratio, color temperature and whether sources are mixed
- **Material**: which surfaces carry the image, how wear and texture are rendered, atmospheric interaction
- **Color and mood**: palette relationships as hex values, harmony system, and the emotional read those choices produce

Then deliver the full package immediately. The reference already answered the questions; re-asking them wastes the user's time. Only interrupt when something is genuinely blocking: which figure is the subject in a group shot, or whether an illustration should be converted to photoreal or style-matched.

---

## 4. Defend the prompt

A prompt is not only what you ask for. It is also what you prevent. Every model has default behaviors that will quietly overwrite your intent, and naming them is the difference between one generation and six.

**The identity rule.** When a person's identity comes from a reference — a trained Soul ID, a character reference, an uploaded photo — do not describe their face, hair, build, skin tone, or age. Written description competes with the reference and corrupts the likeness. Describe wardrobe, posture, gaze, action, and exact position in frame; leave the person themselves to the reference. When a reference shows someone whose identity should *not* carry over, extract their pose, wardrobe, and placement only.

**Fidelity anchoring.** When a real product or object must be reproduced exactly, say so explicitly — *"use the reference as the exact product, keep proportions, materials and every part identical, do not redesign, do not add or remove parts."* Without that clause, models redesign the object into something generic and plausible, which is worse than useless for commerce.

**Anti-interpretation clauses.** Models have stubborn defaults: adding a "+" between two logos, adding typography to anything that looks like an ad, making flat icons glossy 3D, adding a reflective floor, smoothing skin into plastic, warming everything to teal-and-orange. When a default threatens your concept, state the prohibition in its own clause *and* repeat it in the negative prompt. Anything that survives both is worth a second look at the concept.

**The negative prompt.** A short, targeted block beats a long generic one — every term you list also spends a little attention. Start here and extend per image:

> no text, no letters, no captions, no watermark, no logos, no extra people, no distorted hands, no altered facial features, no skin smoothing, no plastic skin, no oversaturation

**The post-production boundary.** Text, CTAs, logo lockups, and meaningful screen content are unreliable in generation and trivial in Figma or Canva. Render the physical scene — the phone at that angle with a soft neutral glow, the clean band of negative space where the headline goes — and list the overlays under POST-PRODUCTION. Exceptions exist: `gpt_image_2`, `openai_hazel`, and `nano_banana_pro` render short typography reliably enough for thumbnails and posters. Even then, spell the text exactly and forbid extra text elsewhere in the frame.

**The precision floor.** Before delivering, every prompt carries at minimum: focal length in mm, an aperture, a color temperature in Kelvin, three or more hex values anchoring the palette, and a negative block. These are not decoration — they are the specific things whose absence lets the model average.

---

## 5. Route to a model

The right model does more for the result than another paragraph of prompt. Match the job:

| Job | Start with |
|---|---|
| Realistic people, UGC, fashion, editorial portraits | `soul_2` (add `soul_id` for a consistent recurring character) |
| Legible typography, thumbnails, posters, diagrams | `nano_banana_pro`, `gpt_image_2`, `openai_hazel` |
| Product and e-commerce ads | `marketing_studio_image`, or `gpt_image_2` with the product photo as reference |
| Maximum resolution and precise control | `seedream_v5_pro`, `nano_banana_pro` at 4k |
| Cinematic stills and concept art | `soul_cinematic`, `cinematic_studio_2_5` |
| Logos, icons, vector, flat brand assets | `recraft_v4_1` |
| Video from a still (the default path) | `seedance_2_5`, `kling3_0`, `minimax_h3` |
| Multi-shot sequences, audio sync, motion transfer | `kling3_0` |
| Product and UGC video ads | `marketing_studio_video` |
| Cinema-grade video | `cinematic_studio_3_0` |

`references/model-routing.md` carries the full catalog with parameters, durations, aspect ratios, and reference-input roles. Read it before generating for a model whose constraints are not fresh in context, and call `models_explore` with `action: "recommend"` when the job does not match anything above.

**The still-to-motion bridge.** Text-to-video gives away control of every framing decision at once. Generating the still first and animating it as `start_image` keeps camera, light, wardrobe, and palette locked, and reduces video to a single question: what moves? Default to this path unless the person explicitly wants text-to-video.

Video prompts follow a different discipline than image prompts — density helps images and hurts video. `references/video-direction.md` covers motion vocabulary, the CAMERA/SUBJECT/AUDIO block format, shot chaining, and keyframe workflows. Read it before writing any video prompt.

---

## 6. Deliver the package

Lead with the thing they can paste. Keep the explanation short — they came for a prompt, not an essay.

**A. MASTER PROMPT** — structured, in English regardless of conversation language, because models adhere measurably better to English. JSON by default; XML when the platform or the user prefers it. Fields:

`style` · `subject_action` · `wardrobe_or_product` · `environment` · `camera` · `lighting` · `materials` · `color_palette` (hex array) · `composition` · `atmosphere` · `mood` · `format` · `negative_prompt`

**B. CONDENSED PROMPT** — the same specification as one dense English paragraph, for character-limited fields. Skip only if asked.

**C. NEGATIVE PROMPT** — as a standalone line, ready to paste into its own field.

**D. SETTINGS** — model, aspect ratio, resolution or quality tier, and any model-specific parameters, named exactly as the platform expects them.

**E. POST-PRODUCTION** — every element to be composited outside the generator. Write "nothing" when there is nothing.

**F. ASSUMPTIONS** — one line naming what you decided on their behalf.

Match the user's language for everything conversational — questions, POST-PRODUCTION, ASSUMPTIONS. Prompt content stays English.

`references/output-templates.md` has complete worked examples for image, reference, and video modes. Read it the first time you deliver in a session.

---

## 7. Generate, if a Higgsfield MCP is connected

When the Higgsfield tools are available, the prompt does not have to stay theoretical.

**Offer before spending.** Generation costs the user real credits, so ask first and let them approve the model and settings. `get_cost: true` preflights the price without submitting anything. Never pass `use_unlim: true` on your own initiative — that quietly spends a limited free-trial allowance.

**Reference media.** Web URLs go through `media_import_url`; local files through `media_upload_widget`. Both return a `media_id` that goes into `params.medias[]` with the right `role` — never paste a URL into `medias[].value`. Omitting the reference is the single most common reason a "faithful" product render comes back as an invented product.

**Templated jobs.** Before building any multi-step made-to-brief video — narrated explainers, ads, UGC, unboxings, tutorials, character sheets, brand kits — call `get_workflow_instructions` with no argument to see the catalog, then load the matching workflow. These bundled workflows already encode the shot structure; reinventing it produces worse results.

**Edits beat regenerations.** For an existing asset, reach for the dedicated tool rather than rolling the dice again: `upscale_image` / `upscale_video`, `outpaint_image`, `reframe`, `remove_background`, `motion_control`.

When no Higgsfield MCP is present, deliver the package and note that the SETTINGS block maps directly onto the fields in the Higgsfield web app.

---

## When a result comes back wrong

Rewriting the whole prompt is the slow fix. Identify which pillar failed and repair only that.

| Symptom | Failed layer | Move |
|---|---|---|
| Looks generic, "stock", could be anyone's | Structure absent | Add lens, aperture, key direction, Kelvin |
| Flat, no dimension, no drama | Lighting under-specified | Name direction, quality, ratio, shadow behavior |
| Reads as fake / plastic / CGI | Materials missing | Add wear, texture, imperfection, surface response |
| Right elements, wrong feeling | Vision unstated | Name the feeling *and* its technical mechanism |
| Composition scattered, no focal point | Composition missing | Specify framing, layers, negative space, DoF placement |
| Model ignored a specific instruction | Buried too deep | Move it up the hierarchy, isolate it in its own clause, echo it in the negative |
| Wrong face on a referenced person | Identity described in text | Delete every physical descriptor; let the reference carry it |
| Product redesigned | No fidelity anchor | Add the exact-reproduction clause and attach the reference media |
| Unwanted text or logos appeared | Predictable default | Explicit prohibition plus negative prompt, or move it to post |
| Video morphs, warps, or drifts | Video prompt overloaded | Cut to one camera idea and one subject action |

---

## Self-check before delivering

1. Focal length, aperture, Kelvin, and three hex values are all present
2. A negative prompt block exists and is targeted, not boilerplate
3. Vision is stated as a feeling *with* the mechanism that produces it
4. No physical description of anyone whose identity comes from a reference
5. Text, logos, and CTAs are either handled by a text-capable model or moved to POST-PRODUCTION
6. Model, aspect ratio, and parameters are real and named as the platform names them
7. Video prompts carry exactly one camera idea and one primary subject action
8. Someone else could rebuild this shot from the Structure block alone

Fix quietly, then deliver.

---

## Reference files

- `references/model-routing.md` — full Higgsfield image, video, and utility catalog: parameters, aspect ratios, durations, reference roles, and MCP call patterns. Read before generating for an unfamiliar model.
- `references/technical-vocabulary.md` — camera, lighting, material, composition, and color libraries, plus the psychology of each choice. Read when building Structure for a setup outside your fluency.
- `references/video-direction.md` — motion vocabulary, block format, shot chaining, keyframes, audio direction. Read before writing any video prompt.
- `references/output-templates.md` — complete worked packages for image, reference, and video modes. Read the first time you deliver in a session.
- `references/brand-kit-template.md` — fillable template so a user's palette, voice, and defaults persist across sessions. Offer it when someone repeats the same style preferences.
