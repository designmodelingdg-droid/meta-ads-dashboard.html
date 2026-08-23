# Model Routing — Higgsfield Catalog

Picking the right model does more for a result than another paragraph of prompt. This file is the map.

**Contents**

1. How to choose fast
2. Image models
3. Video models
4. Utility and editing tools
5. MCP call patterns
6. Credits and cost discipline

Model lineups change. When something here disagrees with `models_explore`, believe `models_explore` — call it with `action: "get"` and a `model_id` for live constraints, or `action: "recommend"` with a goal description when the job matches nothing below.

---

## 1. How to choose fast

Three questions resolve most cases.

**Does a specific person need to look the same across generations?**
→ `soul_2` with a trained `soul_id`. Nothing else in the catalog holds a likeness as reliably.

**Does legible text have to appear inside the frame?**
→ `nano_banana_pro`, `gpt_image_2`, or `openai_hazel`. Every other model will produce convincing-looking gibberish. If the text is brand copy that must be exact, generate the scene clean and set the type in Figma or Canva instead.

**Does a real product have to be reproduced exactly?**
→ Any model that accepts reference media, with the product photo attached and a fidelity clause. `marketing_studio_image` is purpose-built; `gpt_image_2` at high quality is the flexible alternative.

Everything else is a preference between houses: Google's Nano Banana line is fast and clean, Bytedance's Seedream line is precise and high-resolution, Higgsfield's Soul line is the most photographic with people, FLUX adheres tightly to literal instructions.

---

## 2. Image models

### People, character, editorial

| Model | Use for | Key parameters | Aspect ratios |
|---|---|---|---|
| `soul_2` | Realistic UGC, fashion editorial, portraits, character work. The default for anything with a person in it. | `quality`: 1.5k \| 2k · `soul_id` for trained identity · 1 reference image, role `image` | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 |
| `soul_cast` | Establishing a consistent cinematic character identity from text alone | `budget` 10–500 | 16:9 only |
| `soul_cinematic` | Cinema-grade stills, concept art, dramatic lighting | `quality`: 1.5k \| 2k · `soul_id` | adds 21:9 |
| `soul_location` | Environments, backgrounds, establishing plates with no subject | — | wide range incl. 21:9, 9:21 |

`soul_2` rewards long, dense, hyper-technical prompts — camera body feel, lighting ratios, fabric behavior. It is the one model where more precision reliably means more quality.

For a recurring character, training a Soul ID (5–20 photos, roughly 10 minutes) is worth it the moment the same face is needed more than twice. `show_characters(action='train')` — only when the user asks for it or supplies the photos.

### Typography, thumbnails, diagrams

| Model | Use for | Key parameters | Aspect ratios |
|---|---|---|---|
| `nano_banana_pro` | Highest-quality general work, text rendering, diagrams, 4K | `resolution`: 1k \| 2k \| 4k | 1:1, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 9:16, 16:9, 21:9 |
| `gpt_image_2` | Typography, editing, ad creatives, strong instruction-following | `resolution`: 1k \| 2k \| 4k · `quality`: low \| med \| high | 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3 |
| `openai_hazel` | Best-in-class text rendering, logos, infographics | `quality`: low \| med \| high | 1:1, 3:2, 2:3, auto |
| `nano_banana_2` | Fast, high-quality, versatile, 4K capable | `resolution`: 1k \| 2k \| 4k | same wide range as Pro |

`gpt_image_2` adds typography to anything that resembles an advertisement unless explicitly forbidden. Always carry "no text, no typography, no watermarks" in the negative when you want a clean plate from it.

### Product, commerce, brand

| Model | Use for | Notes |
|---|---|---|
| `marketing_studio_image` | One-click product ads for social campaigns | `resolution` up to 4k; widest aspect list including `auto` and 4:5 |
| `ms_image` (DTC Ads) | Brand-kit-aware DTC ads with avatars and curated formats | `style_id` is **required** — call `show_marketing_studio(type='image_style')` and let the user pick before generating. Optional `brand_kit_id`, `product_ids` (max 4), `batch_size` 1–20 |
| `recraft_v4_1` | Logos, icons, vector illustration, flat brand assets, mockups | `model_type`: standard \| vector \| utility \| utility_vector · `colors` (up to 10 hex) · `background_color` |

### Precision, resolution, transformation

| Model | Use for | Key parameters |
|---|---|---|
| `seedream_v5_pro` | Visual reasoning, instruction-based editing, up to 2K | `resolution`: 1k \| 1.5k \| 2k · `remove_bg` · `is_inpaint` |
| `seedream_v4_5` | 4K output, precise control, transformations | `quality`: basic (→4K) \| high (→~6K) |
| `flux_2` | Tight literal prompt adherence | `variant`: pro \| flex \| max · `resolution`: 1k \| 2k |
| `flux_kontext` | Context-aware editing and style transfer | — |
| `cinematic_studio_2_5` | Cinematic stills up to 4K | `resolution`: 1k \| 2k \| 4k |
| `kling_omni_image` | Versatile photorealism, very wide aspect support | `resolution`: 1k \| 2k |
| `grok_image` | Expressive, high-contrast, bold | `resolution` · `mode`: std \| quality |
| `z_image` | Fast, cheap, stylized drafts | — |
| `image_auto` | Let the router pick when the user has no preference | — |

---

## 3. Video models

### The reference-driven line (Bytedance Seedance)

| Model | Duration | Resolution | Reference roles |
|---|---|---|---|
| `seedance_2_5` | 4–30s | 480p, 720p | start_image, end_image, image_references, video_references, audio_references |
| `seedance_2_0` | 4–15s | up to 4k (`mode: std`) | same, plus multi-SKU product consistency |
| `seedance_2_0_mini` | 4–15s | 480p, 720p | same — the budget draft option |
| `seedance1_5` | 4, 8, 12s | up to 1080p | start_image, end_image |

`seedance_2_5` carries four modes: `t2v` (prompt only), `omni_reference` (any references), `video_edit` (edit one reference video, billed by its duration), `video_extension` (extend forward or backward — `extension_mode` required). Its 30-second ceiling is the longest single generation in the catalog.

Seedance responds well to explicitly separated camera and subject blocks and holds identity across shots better than most. `generate_audio` defaults true — turn it off when the clip is going under a music bed or a voiceover.

### The cinematic line

| Model | Duration | Notes |
|---|---|---|
| `cinematic_studio_3_0` | 4–15s | Most advanced cinema-grade. `resolution` to 4k, `genre` hint (action, horror, comedy, noir, drama, epic), `generate_audio` |
| `cinematic_studio_video_v2` | 3–12s | `genre`, `mode`: pro \| std, `speedramp` (slowmo, speedup, impact), `multi_shots` with `multi_prompt`, `cfg_scale` 0–1 for adherence strength |
| `veo3` | model default | Reliable cinematic, broad range. `variant`: veo-3-preview (quality) \| veo-3-fast. 16:9 and 9:16 only, start_image |

Raise `cfg_scale` toward 1 when a detailed prompt is being ignored; lower it toward 0 when output looks stiff and over-literal.

### The motion and multi-shot line (Kling)

| Model | Duration | Notes |
|---|---|---|
| `kling3_0` | 3–15s | Multi-shot, audio sync, motion transfer. `mode`: std \| pro \| 4k · `sound`: on \| off |
| `kling3_0_turbo` | 3–15s | Fast text-to-video and single start-frame animation, 720p/1080p |
| `kling2_6` | 5, 10s | Cinematic motion, strong physics, native audio |

`kling3_0` is the pick when one generation needs to contain more than one shot, or when motion must be transferred from a source video.

### Keyframe and multimodal

| Model | Duration | Notes |
|---|---|---|
| `minimax_h3` | 4–15s | 2K output, keyframes plus image/video/audio references, `batch_size` 1–4 |
| `minimax_hailuo` | 6, 10s | Natural physics and facial emotion. `variant` up to minimax-2.3 |
| `flux_3_video` | 5–20s | Text-to-video, multi-frame image-to-video, video continuation, synchronized audio, 1080p |
| `wan3_0` | 2–30s | First/last frame, multimodal references, `enable_thinking` for better adherence, `duration: -1` lets the model choose |
| `wan2_7` | 2–15s | Synchronized audio, character consistency |
| `grok_video_v15` | 2–15s | Start image plus image and audio references |
| `gemini_omni` | 4–10s | Reference-driven with native audio, 720p, 16:9 and 9:16 |

### Templated and utility video

| Model | Use for |
|---|---|
| `marketing_studio_video` | Product and UGC ads, TikTok/Reels ready, 12–15s. Supports `avatar_ids`, `product_ids`, `hook_id`, `setting_id`, `ad_reference_id`, and preset `mode` slugs. **Defaults to 16:9** — pass `aspect_ratio: "9:16"` explicitly for vertical |
| `higgsfield_preset` | Preset-routed image-to-video using viral templates. `preset_id` required — get it from `presets_show` |
| `clipify` | Turn one YouTube URL into subtitled short clips. `clips_num` 1–20, `clip_aspect`, subtitle font/case/position/highlight |

`hook_id` and `setting_id` work only with the UGC, Tutorial, Unboxing, Product Review, and UGC Virtual Try On presets, and are mutually exclusive with `ad_reference_id`. When using `ad_reference_id`, avatar and product are **not** inherited — pass them explicitly.

---

## 4. Utility and editing tools

Reach for these before regenerating. They are cheaper, faster, and preserve what already works.

| Need | Tool |
|---|---|
| More resolution | `upscale_image` (2K/4K), `upscale_video` |
| Expand the frame / uncrop | `outpaint_image`, `flux_2_pro_outpaint` (per-side pixel control; negative values crop) |
| Change aspect ratio | `reframe` |
| Cutout | `remove_background` |
| Recast, puppeteer, transfer motion | `motion_control` |
| Lip-sync to audio | `sync_so` |
| Image → 3D mesh (GLB) | `generate_3d` |
| Sprite sheet from a character | `autosprite` |
| Predict engagement before publishing | `virality_predictor` |

---

## 5. MCP call patterns

**Basic image call**

```
generate_image({ params: {
  model: "soul_2",
  prompt: "<master prompt as one dense paragraph>",
  aspect_ratio: "9:16",
  quality: "2k"
}})
```

Model-specific parameters go at the **top level** of `params`, not nested. `count` 2–4 produces variants of the *same* prompt; for several different prompts use `generate_image_batch` with `jobs_wait`, then one `show_generation_by_ids`.

**With reference media**

```
media_import_url("https://…/product.jpg")   → returns media_id
generate_image({ params: {
  model: "gpt_image_2",
  prompt: "Use the reference image as the exact product…",
  medias: [{ value: "<media_id>", role: "image" }],
  aspect_ratio: "1:1", quality: "high", resolution: "2k"
}})
```

Roles differ by model — check `medias[].roles` in `models_explore`. Common roles: `image`, `image_references`, `start_image`, `end_image`, `video_references`, `audio_references`. A prior generation's `job_id` can be passed as a `value` to chain generations. Never put an `https://` URL in `medias[].value`.

**Still → video**

```
generate_video({ params: {
  model: "seedance_2_5",
  prompt: "CAMERA: … SUBJECT: … AUDIO: …",
  medias: [{ value: "<image job_id or media_id>", role: "start_image" }],
  aspect_ratio: "9:16", duration: 5, resolution: "720p", generate_audio: false
}})
```

**Before any templated build** — narrated explainers, ads, UGC, unboxings, tutorials, character sheets, brand kits — call `get_workflow_instructions` with no argument to list the catalog, then again with the workflow name. Those bundles encode shot structure that is expensive to rediscover.

If a call returns a `recovery_tool`, call it immediately rather than explaining or asking first.

---

## 6. Credits and cost discipline

Generation spends the user's money. Three habits keep that honest:

- **Preflight.** `get_cost: true` returns the credit cost without submitting a job. Use it whenever the settings are unusual — 4K, long durations, large batches.
- **Draft cheap, finish expensive.** Compose at low resolution on a fast model (`z_image`, `nano_banana_2`, `seedance_2_0_mini`), then re-run the settled prompt at full quality. Iterating at 4K is the most common way to burn a balance.
- **Never opt into `use_unlim` unprompted.** It defaults to false. Passing true spends a limited free-trial allowance that the user may be saving. Omit it and let the server ask, or set it only when they explicitly say to use their unlimited generations.

`balance` and `show_plans_and_credits` report what is left when the user asks.
