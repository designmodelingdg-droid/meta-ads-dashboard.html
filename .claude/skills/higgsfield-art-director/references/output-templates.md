# Output Templates — Worked Examples

Three complete deliveries. Read one that matches the job at hand rather than all three.

**Contents**

1. Concept mode → image (product ad)
2. Reference mode → image (reverse-engineered portrait)
3. Still → video (animating a generated frame)
4. The intake round, in practice

---

## 1. Concept mode → image

**User said:** "I need a hero shot of our new ceramic pour-over kettle for the product page. Something premium."

**Intake asked** (one round, four questions): format → 1:1 for the page grid · surface → warm neutral, not white · mood → quiet craftsmanship · palette → open. Everything else decided and logged.

---

**A. MASTER PROMPT**

```json
{
  "style": "premium e-commerce product photography, editorial rather than catalog",
  "subject_action": "a matte ceramic pour-over kettle standing centered and upright, gooseneck spout angled slightly toward camera-right, lid seated, nothing else in frame",
  "wardrobe_or_product": "matte glazed stoneware body in warm bone white with a faintly visible glaze pool at the base, thin unglazed clay rim at the foot showing raw grain, brushed stainless gooseneck spout with soft anisotropic highlight, walnut handle with visible open grain and a slight sheen where a hand would rest",
  "environment": "seamless warm neutral sweep, no horizon line, no props, no surface texture beyond a faint paper tooth",
  "camera": "105mm macro-telephoto, f/8, eye-level with the vessel's midpoint, straight-on with a 10° rotation so both the spout profile and the handle read, tight product crop with even margin",
  "lighting": "large gridded softbox key from camera-left at 45° and slightly above, white bounce card camera-right at quarter power holding shadow detail, narrow stripbox behind camera-right raking a rim highlight along the spout edge, black flag opposite to keep the shadow side from filling, 5000K neutral daylight, 1:3 key-to-fill ratio",
  "materials": "matte glaze scattering light diffusely with no specular hotspot on the body, brushed steel producing a directional streaked highlight rather than a mirror, walnut grain catching light along the raised figure, a single soft contact shadow anchoring the kettle to the surface",
  "color_palette": ["#E8E2D6", "#F2EDE4", "#8A6A47", "#B8B2A6", "#2C2823"],
  "composition": "centered, generous even negative space on all four sides, kettle occupying roughly 62% of frame height, contact shadow falling down and slightly camera-right",
  "atmosphere": "clean still air, no haze, no particulate",
  "mood": "quiet craftsmanship — restraint and material honesty, produced by neutral 5000K light, matte surfaces refusing to glare, and one believable shadow instead of a reflection",
  "format": "1:1 square, 2048×2048",
  "negative_prompt": "no text, no typography, no logos, no watermark, no price tags, no people, no hands, no extra props, no steam, no water, no glossy plastic sheen, no mirror reflection, no reflective floor, no gradient background, no vignette, no lens flare, no oversaturation"
}
```

**B. CONDENSED PROMPT**

> Premium e-commerce product photograph of a matte ceramic pour-over kettle, square 1:1. Centered and upright on a seamless warm neutral sweep, gooseneck spout angled slightly toward camera-right, rotated about 10° so both spout profile and walnut handle read. Warm bone-white matte stoneware with a faint glaze pool at the base and a raw unglazed clay foot, brushed stainless gooseneck catching a soft streaked highlight, walnut handle with open grain. 105mm at f/8, eye level with the vessel's midpoint, tight crop with even margin. Large gridded softbox key from camera-left at 45° and slightly above, white bounce card camera-right at quarter power, narrow stripbox raking a rim highlight along the spout edge, black flag opposite to hold the shadow side, neutral 5000K, 1:3 key-to-fill. Matte glaze scatters light with no specular hotspot; one soft believable contact shadow falls down and slightly camera-right. Palette #E8E2D6, #F2EDE4, #8A6A47, #B8B2A6, #2C2823. Generous even negative space, kettle at about 62% of frame height. Quiet craftsmanship — restraint and material honesty. No text, no typography, no logos, no watermark, no price tags, no people, no hands, no extra props, no steam, no glossy plastic sheen, no mirror reflection, no reflective floor, no gradient background, no vignette, no lens flare.

**C. NEGATIVE PROMPT**

```
no text, no typography, no logos, no watermark, no price tags, no people, no hands, no extra props, no steam, no water, no glossy plastic sheen, no mirror reflection, no reflective floor, no gradient background, no vignette, no lens flare, no oversaturation
```

**D. SETTINGS**

| | |
|---|---|
| Model | `marketing_studio_image` (alt: `gpt_image_2`, quality `high`) |
| Aspect ratio | `1:1` |
| Resolution | `2k` |
| Reference | attach the real product photo as `medias[{role: "image"}]` and prepend *"Use the reference image as the exact product — same proportions, same materials, same parts. Do not redesign, do not add or remove parts."* |

**E. POST-PRODUCTION**

Product name, price, and any badge set in Figma over the right-hand negative space. Nothing baked into the render.

**F. ASSUMPTIONS**

1:1 at 2048px for crop headroom · warm neutral sweep rather than pure white so the bone glaze separates · one contact shadow instead of a reflection, since reflections are the tell that reads as stock render.

---

## 2. Reference mode → image

**User said:** "Recreate this look for my client, but make it a man in his forties in a workshop." *(reference attached: high-contrast environmental portrait)*

No intake round. The reference answered format, lighting, palette, and mood; only the subject and setting changed. Deconstruction ran silently.

---

**A. MASTER PROMPT**

```json
{
  "style": "environmental documentary portrait, editorial magazine tradition, mid-format film character",
  "subject_action": "a man in his forties standing at a workbench, body angled about 30° away from camera, head turned back to meet the lens, weight settled on the back foot, one hand resting flat on the bench, the other hanging relaxed",
  "wardrobe_or_product": "heavyweight canvas work apron over a faded chambray shirt with the sleeves rolled to mid-forearm, visible wear at the apron pocket edges, fabric holding a stiff drape",
  "environment": "a working woodshop, midground bench with tools laid out in use rather than arranged, background racking and timber stock falling into soft shadow, sawdust settled on surfaces",
  "camera": "85mm, f/2.0, camera at chest height, slight upward tilt, medium shot from waist up, subject placed on the left third",
  "lighting": "single large north-facing window as key from camera-right at roughly 60°, unmodified, hard-ish quality with a defined shadow edge, no fill on the camera-left side letting it fall to near-black, 5600K daylight against one warm 2900K practical bulb visible deep in the background, 1:6 key-to-fill",
  "materials": "skin with visible pores, forearm hair and a day of stubble, canvas with a coarse open weave and a worn sheen at stress points, raw timber end-grain, fine airborne sawdust catching the window light",
  "color_palette": ["#C9B79A", "#6B5641", "#2A2521", "#8FA3A8", "#E4DCCB"],
  "composition": "subject on the left third, bench leading diagonally from lower-left into the frame, background falling three stops darker, focus plane on the near eye with the far shoulder already softening",
  "atmosphere": "visible dust suspended in the window beam, air with weight to it",
  "mood": "earned competence — the sense of someone interrupted mid-task, produced by the unfilled shadow side, the working-not-styled bench, and eye contact without a smile",
  "format": "4:5 vertical, 2048×2560",
  "negative_prompt": "no text, no watermark, no logos, no extra people, no distorted hands, no skin smoothing, no plastic skin, no beautification, no studio backdrop, no arranged tools, no teal-and-orange grade, no lens flare, no HDR halos"
}
```

**B. CONDENSED PROMPT**

> Environmental documentary portrait in an editorial magazine tradition, 4:5 vertical, mid-format film character. A man in his forties stands at a workbench in a working woodshop, body angled about 30° away, head turned back to camera, weight on the back foot, one hand flat on the bench. Heavyweight canvas work apron over a faded chambray shirt rolled to mid-forearm, wear visible at the pocket edges. 85mm at f/2.0, camera at chest height with a slight upward tilt, medium shot, subject on the left third. Single large north window as key from camera-right at 60°, unmodified, defined shadow edge, no fill on the camera-left side falling to near-black, 5600K daylight against one warm 2900K practical deep in the background, 1:6 ratio. Skin with visible pores and stubble, coarse open canvas weave with a worn sheen at stress points, raw timber end-grain, fine sawdust suspended in the window beam. Tools laid out in use, not arranged; background racking three stops darker. Focus on the near eye, far shoulder already softening. Palette #C9B79A, #6B5641, #2A2521, #8FA3A8, #E4DCCB. Earned competence — someone interrupted mid-task, eye contact without a smile. No text, no watermark, no logos, no extra people, no distorted hands, no skin smoothing, no plastic skin, no beautification, no studio backdrop, no arranged tools, no teal-and-orange grade, no lens flare.

**D. SETTINGS**

| | |
|---|---|
| Model | `soul_2`, quality `2k` |
| Aspect ratio | `4:5` — *not offered by `soul_2`; use `3:4` or generate 3:4 and `reframe` to 4:5* |
| Reference | attach the reference as `medias[{role: "image"}]` for style and palette guidance only |

**E. POST-PRODUCTION** — nothing.

**F. ASSUMPTIONS**

Mirrored the reference's contrast ratio and unfilled shadow side, which is what gives it its character · palette pulled from the reference and shifted toward wood and canvas for the new setting · `soul_2` has no 4:5, so delivering 3:4 with a reframe step.

---

## 3. Still → video

**User said:** "Can you make that kettle shot move? Something for the top of the product page."

---

**A. MASTER PROMPT**

```
CAMERA: slow push-in, roughly 15cm over the full clip, locked height, no shake, no zoom
SUBJECT: the kettle stays completely still; a thin ribbon of steam begins at the spout around one second in and drifts upward and slightly camera-right, thinning as it rises
LIGHT & ATMOSPHERE: lighting holds exactly constant; the contact shadow does not move; a few dust motes drift slowly through the key light
AUDIO: none
NEGATIVE: no camera shake, no handheld drift, no zoom, no rotation, no hands, no pouring, no water, no liquid, no text, no captions, no extra objects entering frame, no lighting change, no color shift
```

**D. SETTINGS**

| | |
|---|---|
| Model | `seedance_2_5` |
| Start frame | the approved still's `job_id` as `medias[{role: "start_image"}]` |
| Aspect ratio | `1:1` |
| Duration | `5` |
| Resolution | `720p` for approval, re-run at higher or `upscale_video` for final |
| `generate_audio` | `false` |

**E. POST-PRODUCTION**

Loop the clip in the page player. If a seamless loop is wanted, pass the same still as `end_image` so the frame returns to its starting state.

**F. ASSUMPTIONS**

Steam is the only motion, because a product hero that moves too much reads as a commercial rather than a page header · audio off since it will sit muted on the page · 5 seconds because the loop point matters more than the length.

---

## 4. The intake round, in practice

What a good intake looks like — concrete options, an open path, and a stated default so silence still produces a result.

> **1. Where does this run?**
> (a) Instagram feed 4:5 · (b) Reels/TikTok 9:16 · (c) YouTube 16:9 · (d) product page 1:1 · (e) something else
>
> **2. How polished?**
> (a) raw and handheld, feels like a phone · (b) clean commercial, obviously produced · (c) editorial — produced but not slick
>
> **3. The one feeling it should land?**
> (a) aspirational calm · (b) urgency and energy · (c) quiet craftsmanship · (d) playful · (e) your words
>
> **4. Palette?**
> (a) faithful to the reference · (b) your brand colors — paste them · (c) your call
>
> Answer what you know and I'll decide the rest — I'll list every assumption at the end.

Two rounds maximum. Then write once, completely, and stop asking.
