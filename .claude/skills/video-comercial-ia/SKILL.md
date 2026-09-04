---
name: video-comercial-ia
description: |
  Produce un comercial cinematográfico de Design Modeling Academy generado con IA (Higgsfield): escena por escena, con o sin una persona real de la casa como protagonista, tipografía DMA en post y placa final con el logo. Entrega vertical 9:16 y horizontal 16:9.

  Usa este skill cuando Dayana diga: "video-comercial-ia", "hazme un comercial", "un video para el máster", "genera un video con higgsfield", "un video con mi foto", "video con Gabriel de protagonista", "necesito un video para la pauta", o cuando traiga un MASTER PROMPT de comercial.

  Probado dos veces: comercial Revit 2027 (ago-2026, sin persona) y comercial con Gabriel de protagonista (2-sep-2026, 29 s desde una sola foto).
---

# Skill: video-comercial-ia

Un comercial de 30 s no se genera de una sola vez: **los modelos dan 5-15 s por
clip**. Son escenas encadenadas, y el problema real es que la identidad y el
estilo no cambien entre ellas.

---

## 1. Antes de gastar un crédito

```
balance                                  # cuántos créditos hay
generate_image / generate_video con get_cost:true    # preflight de cada paso
```

**`get_cost` responde aunque el plan no permita el modelo.** El permiso solo se
ve al enviar el trabajo. En el plan free (sep-2026):

| Paso | Modelo | Costo | Nota |
|---|---|---|---|
| Keyframes | `nano_banana_pro` 9:16 2k | 2 cr | funciona |
| Video | `minimax_h3_max` 9:16 5 s 768p | 12,5 cr | funciona |
| Video | `kling3_0` / `kling3_0_turbo` | 7,5 cr | **"Requires basic plan"** |

Otros límites del plan free: **429 rate_limit_reached** con más de 2 envíos a la
vez (se manda de dos en dos), y `mode:"pro"` exige plan de pago. Si el servidor
recomienda un preset en vez de generar, se declina con `declined_preset_id` y se
genera lo que se pidió.

Un comercial de 6 escenas sale por **~93 créditos**.

---

## 2. Con persona real: el método que funciona

1. **Preparar la foto.** Las fotos de teléfono traen EXIF orientation — si no se
   endereza, el modelo trabaja con la persona de lado:
   `ImageOps.exif_transpose(Image.open(foto))`, luego recorte 9:16.
2. **Un keyframe por escena** con `nano_banana_pro` y la foto como
   `image_references`.
3. **Animar cada keyframe** como `start_image`. La cara sale del keyframe, no de
   un texto: por eso se mantiene igual en todas las escenas.

### EL FALLO QUE HAY QUE EVITAR

La foto de Gabriel tenía un cuadro colgado detrás. En dos escenas el modelo
copió el cuadro al fondo **y duplicó su cara colgada en la pared**. Añadir
"no paintings, no wall art" al prompt NO bastó.

**Lo que funcionó:** generar primero un retrato limpio (escena 1, fondo neutro),
subirlo, y usar ESE como referencia para el resto. Regla: **la foto de
referencia debe tener fondo limpio; si no lo tiene, se fabrica uno antes de
seguir.**

Y verificar CADA keyframe mirándolo antes de animarlo: animar un keyframe malo
cuesta seis veces más que regenerar la imagen.

---

## 3. Escribir las escenas

Cada prompt de keyframe lleva:

- Identidad: "THIS EXACT MAN from the reference — identical real face, short
  beard, hairstyle, same tailored gray suit and white shirt".
- **Escala explícita**: sin ella el protagonista sale diminuto. "framed from the
  knees up, filling the lower two thirds of the frame".
- Mundo DMA: azul marino #0E2438, geometría blanca, acentos ámbar #E8A04A,
  blueprints cian, estética Autodesk Revit — **no ciencia ficción**.
- Prohibiciones: "exactly ONE person and ONE face, no framed pictures, no
  paintings, no text, no letters, no numbers, no watermark".

El prompt de video describe **solo el movimiento** (dolly-in, órbita, crane) y
repite que la cara no cambia.

---

## 4. Los rótulos NO los hace el modelo

Se piden explícitamente SIN texto y se añaden en post con un `.ass`: Montserrat
ExtraBold, blanco con la palabra clave en ámbar #E8A04A, `\fad(320,320)` y pop
de escala. Los modelos escriben texto con errores; así además queda con la
tipografía de la casa.

Los rótulos van **en español** salvo que se pida lo contrario: la audiencia lo es.

---

## 5. Montaje

- Clips a 1080×1920@30, recortados a 4,8 s.
- `xfade=fade:duration=0.4` entre escenas; `fadeblack` antes de la placa.
- **Placa final con el logo REAL**, nunca uno generado. Está en base64 dentro de
  `dma-sales-assistant/tutor/pagina/index.html`; se extrae y se recolorea a
  blanco conservando en ámbar los píxeles donde R−B > 15 (la grúa y los acentos).
- **Pista de audio silenciosa** (`anullsrc`): Instagram se queja de un MP4 sin
  pista de audio.
- Dos salidas: master CRF 18 y web CRF 22 (el chat corta en 30 MB).

Dos trampas de numpy al construir la placa: un degradado de shape `(H,1,3)` da
una imagen de **1 píxel de ancho** que ffmpeg estira sin avisar (hay que hacer
broadcast a `(H,W,3)`), y `alpha_composite` no pega el logo — `paste(logo, pos,
logo)` sí.

---

## 6. Entrega

- **Vertical 9:16** para reels, historias y pauta móvil.
- **Horizontal 16:9** para LinkedIn (solo acepta horizontal) y la web.
- Subir a Vimeo con la política de la casa: `view=disable` + `embed=public`.
  Los enlaces quedan en `videos/ENLACES-VIMEO.md`.

---

## Reglas

- **Solo material real de la casa.** Las capturas de Revit son las de sus clases
  o las reales del proveedor, nunca infografías generadas por terceros. El logo
  es el real.
- **Preflight de costo antes de cada tanda**, y avisar cuántos créditos quedan.
- **Verificar cada imagen y cada clip mirándolo.** Verificar dos de seis no es
  verificar seis.
- Nunca inventar funciones de software en el guion: lo que el video afirme que
  Revit hace, tiene que ser verdad (regla 0 de la matriz).

El método completo de la primera pieza con persona está en
`matriz-viral/comercial-revit-ia/METODO.md`.
