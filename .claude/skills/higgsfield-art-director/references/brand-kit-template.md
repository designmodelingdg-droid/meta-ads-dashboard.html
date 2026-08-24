# Brand Kit Template

Copy this file, fill it in, and keep it where your assistant can read it — a project doc, a repo file, or persistent memory. Point at it once per session ("use my brand kit") and every prompt inherits it: palette, defaults, banned vocabulary, the outfits your on-camera person actually wears.

Blank fields are fine. An unfilled field means "decide for me"; a filled one is a lock.

---

## Identity

**Brand / channel name:**

**What it makes:**

**Audience, in one line:**

**The one feeling every visual should transmit:**
> Write it as a feeling *plus* its mechanism, e.g. "approachable expertise — eye-level camera, warm practicals, never a studio backdrop"

---

## Palette

Hex values, most-used first. Three minimum; five is better.

| Role | Hex | Where it appears |
|---|---|---|
| Primary | `#` | |
| Background | `#` | |
| Text / darkest | `#` | |
| Accent | `#` | |
| Secondary accent | `#` | |

**Colors that must never appear:**
> e.g. neon, cyan, purple, cold blue — the ones that break the system on sight

---

## Look and feel

**Realism target:** raw and handheld · clean commercial · editorial · stylized/illustrated

**Default lighting character:**
> e.g. "natural available light, warm 3000–3500K, one soft key, never a hard rim"

**Default lens family:**
> e.g. "35mm for lifestyle, 85mm for portraits, never wider than 24mm"

**Grain and texture:** clean · fine grain · heavy grain · film stock: ______

**Traditions we belong to** (one or two, and what you take from each):
> e.g. "Everlane product photography — matte surfaces and one honest shadow"

**Traditions we are not:**
> e.g. "no MrBeast saturation, no stock-photo smiling, no 3D glossy render"

---

## On-camera person

**Identity source:** trained Soul ID `______` · reference photo · not applicable

**Identity rule:** when identity comes from a reference, never describe face, hair, build, skin tone, or age in a prompt — description competes with the reference and corrupts the likeness. Wardrobe, posture, gaze, and frame position only.

**Wardrobe system** — the outfits that recur, so prompts stay consistent:

| Look | Garments | Hex |
|---|---|---|
| A | | |
| B | | |
| C | | |

**Never wears:**

---

## Formats

| Surface | Ratio | Notes |
|---|---|---|
| | | |

**Safe zone rule:** keep faces and critical elements inside the central ___% so platform crops survive.

---

## Recurring props and elements

> Devices, packaging, mascot, signature objects. Include the substitution defaults you want, e.g. "generic laptop → space-black aluminum, no visible logo" · "phone → matte black, screen off or soft neutral glow"

---

## Banned vocabulary

Words that produce output off-system for this brand, beyond the universal ones:

> Universal starting set: "cinematic", "masterpiece", "8k", "highly detailed", "beautiful", "stunning" — all quality-signaling with no content.
> Add yours:

---

## Standing negative prompt

Appended to every generation for this brand:

```
no text, no letters, no captions, no watermark, no logos, no extra people, no distorted hands, no altered facial features, no skin smoothing, no plastic skin, no oversaturation,
```

---

## Post-production boundary

What never gets generated and always gets composited:

> e.g. all typography, logo lockups, CTA buttons, meaningful screen content, subtitles

**Tool used for compositing:**

---

## Default models

| Job | Model | Settings |
|---|---|---|
| Stills with people | | |
| Thumbnails / typography | | |
| Product | | |
| Video | | |
