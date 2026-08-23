# Technical Vocabulary

The control language. Each entry pairs the technical choice with what it does to the viewer, because a prompt that specifies a mechanism without knowing its effect is just noise with numbers in it.

**Contents**

1. Focal length
2. Aperture
3. Camera angle and height
4. Shot size and distance
5. Shutter, ISO, and motion character
6. Lighting — direction, quality, source
7. Studio modifiers and natural conditions
8. Color temperature and palette
9. Materials and surfaces
10. Composition
11. Film stock, era, and texture
12. Failure vocabulary — words that make output worse

---

## 1. Focal length

| Range | Character | Reach for it when |
|---|---|---|
| 8–16mm ultra-wide / fisheye | Extreme distortion, warped edges, immersive | Architectural interiors, skate and action POV, deliberate unease |
| 17–35mm wide | Environmental context, subject inside their world | Street, documentary, real estate, lifestyle where the room matters |
| 35–50mm standard | Natural human vision, honest, versatile | Documentary realism, UGC, anything that should feel unstyled |
| 50–85mm short telephoto | Gentle compression, flattering, isolating | Portraits, product hero shots, interviews |
| 85–135mm medium telephoto | Strong compression, creamy separation | Fashion, beauty, editorial portraiture |
| 135–300mm long telephoto | Backgrounds collapse into texture | Sports, wildlife, candid observation, layered city compression |
| 300mm+ super telephoto | Extreme flattening, near-abstraction | Distant subjects, graphic pattern, heat haze |

Focal length is the single most efficient word in a prompt. It sets perspective, depth relationships, and the emotional distance between viewer and subject in one number.

## 2. Aperture

| Setting | Depth of field | Use |
|---|---|---|
| f/0.95–f/1.4 | Razor-thin, dreamlike bokeh | Isolation, low light, romantic softness |
| f/1.8–f/2.8 | Portrait sweet spot | Subject separation with the eyes still fully sharp |
| f/4–f/5.6 | Moderate | Group shots, travel, context with a soft background |
| f/8–f/11 | Deep, peak lens sharpness | Landscape, architecture, product where every edge counts |
| f/16–f/22 | Everything sharp, starbursts on point lights | Sun stars, deep-focus tableaux, night cityscapes |

State where the focus plane sits, not only how shallow it is: "focus on the front lens element, ears already falling off" is a specification; "shallow depth of field" is a hope.

## 3. Camera angle and height

| Angle | Psychology |
|---|---|
| Worm's eye | Maximum drama, monumentality, the subject towers |
| Low angle | Dominance, heroism, architectural strength |
| Eye level | Equality, documentary honesty, neutrality |
| High angle | Vulnerability, observation, diminishment |
| Bird's eye / top-down | Pattern, abstraction, total overview, flat lay |
| Dutch tilt | Tension, instability, dynamic unease |

Camera *height* is separate from angle and often more useful. "Camera at chest height" and "camera at knee height, tilted slightly up" produce completely different power relationships even at the same nominal low angle.

## 4. Shot size and distance

Extreme wide (subject small in a large environment) · Wide / full body · Medium wide (knees up) · Medium (waist up) · Medium close-up (chest up) · Close-up (face fills frame) · Extreme close-up (single feature) · Macro (1:1 to 5:1, texture becomes the subject) · Over-the-shoulder · Two-shot · Insert (a detail cut into a sequence).

Say the crop explicitly. "Chest up, top of frame just above the head" removes an entire category of guesswork.

## 5. Shutter, ISO, and motion character

- **1/1000s+** — frozen, every droplet suspended, clinical sports
- **1/250s** — normal handheld, clean
- **1/60s** — slight organic softness in moving limbs
- **1/30s with panning** — subject holds, background smears laterally: speed you can feel
- **1/8s–1s** — light trails, ghosted figures, long-exposure abstraction
- **ISO 100–200** — clean, saturated, no grain
- **ISO 400–800** — visible fine grain, documentary honesty
- **ISO 1600–6400** — heavy grain, color noise, low-light authenticity

Shutter and ISO are how you buy imperfection on purpose. They are the most reliable antidote to output that looks too clean to be real.

## 6. Lighting — direction, quality, source

**Direction**

- Front-lit — flat, even, low drama, honest product
- 45° key (loop / Rembrandt) — classic portrait modeling, dimension without severity
- Side-lit (split) — maximum texture, sculptural, half the face in shadow
- Backlit — silhouette, halo, separation, romance, atmosphere made visible
- Rim / kicker — a bright edge peeling the subject off the background
- Top light — pooled eyes, ominous, theatrical
- Underlight — unnatural, unsettling, campfire or screen glow

**Quality**

- **Hard** (small source relative to subject): sharp shadow edges, high contrast, texture revealed, strength and severity
- **Soft** (large source, or diffused): gentle falloff, flattering, even, calm
- **Specular** vs **diffuse**: whether surfaces produce tight bright highlights or a broad even sheen

**Ratio** — the gap between key and fill is what people read as mood. 1:1 is commercial and open; 1:4 is dramatic; 1:8 and beyond is noir. Naming the ratio is more precise than naming the mood.

**Sources** — window light, open shade, direct sun, overcast, golden hour, blue hour, studio strobe, continuous LED, tungsten practicals, neon signage, firelight, screen glow, streetlight sodium vapor, headlights, moonlight.

**Practicals** — lamps, signs, and screens visible *inside* the frame. They are the fastest way to make artificial light look motivated rather than applied.

## 7. Studio modifiers and natural conditions

**Modifiers** — octabox (even, beautiful), stripbox (narrow, directional, great for edges), softbox (versatile), beauty dish (crisp portrait falloff), snoot (tight controlled pool), barn doors (selective blocking), gobo (projected pattern), scrim (cut intensity, keep quality), silver reflector (contrasty bounce), white reflector (neutral fill), gold reflector (warm fill), black flag (negative fill — deepens shadows, the most under-used tool in prompting).

**Natural conditions** — first light (cool-warm mix), golden hour (warm, low, directional), magic hour (blue-gold contrast), blue hour (cool, even, no shadow), overcast (a softbox the size of the sky), storm light (dark sky, bright subject), fog (depth layers made visible), rain (reflective everything), snow (natural fill from below), heat shimmer.

## 8. Color temperature and palette

| Kelvin | Reads as |
|---|---|
| 1800–2200K | Candle, match, embers — intimate, primal |
| 2700–3200K | Tungsten, warm interior — comfort, nostalgia, home |
| 4000–4500K | Neutral warm — natural, unremarkable, honest |
| 5600K | Daylight — balanced, professional, trustworthy |
| 6500–7500K | Overcast, shade, cool LED — clinical, modern, technological |
| 10000K+ | Deep blue shade — cold, isolating, night |

**Mixed temperature** is the most reliable way to make a frame look cinematic without saying "cinematic": a 3200K practical inside a 6500K blue-hour exterior tells a time-of-day story in one specification.

**Harmony systems** — monochromatic (sophisticated restraint), complementary (maximum tension), analogous (flow and calm), triadic (vibrant balance), split-complementary (contrast without harshness).

Always give at least three hex values. "Warm palette" averages; `#E8843A`, `#F5EDE0`, `#1A1A1A` does not.

## 9. Materials and surfaces

Materials are where believability lives. A perfectly lit object with no surface story still reads as CGI.

**Metals** — brushed aluminum (anisotropic streaked reflection), polished chrome (mirror, reflects the environment), anodized (colored, matte-satin), raw steel (grey, slightly mottled), oxidized copper (green patina), blued steel, powder-coated matte, galvanized (rough industrial spangle).

**Fabrics** — weave first (plain, twill, satin, canvas, ribbed knit), then fiber (cotton, linen, silk, wool, denim, technical synthetic), then treatment (mercerized, sandwashed, waxed, water-repellent). Fit and drape matter as much as material: "heavyweight cotton with a stiff drape holding its shape at the shoulder" is a different garment from "soft-washed cotton falling close to the body."

**Organic** — visible skin pores and fine hair, individual hair strand separation, wood grain with raised late-growth rings, stone with mineral variation, leather with crease patterns and worn edges, paper with tooth.

**Glass and liquid** — refraction, caustics, condensation beading, meniscus at the rim, surface tension, bubble scatter.

**Wear** — edge scratches, paint chip with primer showing, rust bloom, UV fade, fabric pilling, thumb-worn surfaces, dust settled in recesses. Wear is what separates a photograph from a render. Specify it deliberately.

**Environmental interaction** — dust motes in a light beam, atmospheric haze building with distance, moisture darkening a surface, heat distortion, breath in cold air, lens dust and faint scratches.

## 10. Composition

- **Framing** — rule of thirds, centered symmetry, negative space, tight crop, frame-within-frame
- **Layers** — name the foreground, midground, and background separately. Depth comes from having three things at three distances, not from an f-stop
- **Leading lines** — roads, architecture, shadows, arms, natural forms directing the eye
- **Balance** — symmetrical (formal, poster-like, stable) versus asymmetrical (dynamic, editorial)
- **Negative space** — where a headline goes, and how the frame breathes. Ad and thumbnail work lives or dies on this
- **Safe zones** — for social output, keep faces and critical elements inside the central 70% so platform crops and UI overlays do not destroy the composition

## 11. Film stock, era, and texture

Naming a stock or an era carries a whole grade in two words: Portra 400 (warm, forgiving skin), Ektar 100 (saturated, punchy), Tri-X 400 (contrasty black and white grain), Cinestill 800T (tungsten-balanced, red halation around highlights), Polaroid SX-70 (soft, milky, faded), Fuji Superia (green-leaning consumer), early-90s newspaper sports (grainy, flash-lit, high contrast), 2000s digicam flash (harsh direct flash, cool cast, blown highlights).

Digital character is equally specifiable: sensor cleanliness, halation, chromatic aberration at the edges, rolling-shutter skew, compression artifacts, scan dust and hairline scratches.

## 12. Failure vocabulary

Some words actively degrade output because they name an average rather than a mechanism.

- **"cinematic"** — the most over-trained word in every model. It pulls toward teal-and-orange, anamorphic flare, and shallow haze regardless of intent. Say what you actually mean: the lens, the ratio, the grade, the aspect.
- **"beautiful", "stunning", "amazing", "masterpiece", "8k", "highly detailed"** — pure quality-signaling with no content. They spend attention and specify nothing.
- **"professional lighting", "good lighting", "perfect composition"** — name the setup instead.
- **"realistic"** — realism is produced by materials, imperfection, and correct light, not by the word.
- **"epic", "dramatic", "moody"** — legitimate as Vision statements, useless as Structure. Pair each with its mechanism or delete it.

The four fatal mistakes, restated as a checklist:

1. Describing the subject instead of the shot
2. Vague lighting
3. Ignoring material properties
4. Generic style references ("make it cinematic" instead of a named tradition and what you are taking from it)
