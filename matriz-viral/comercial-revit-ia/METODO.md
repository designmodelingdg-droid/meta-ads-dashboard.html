# Comercial "Revit 2027 + IA" con persona real — método probado

Primera pieza: 2026-09-02. 29 s, 1080x1920, con Gabriel como protagonista a
partir de UNA foto suya. Sirve de plantilla para cualquier comercial con una
persona real de la casa.

## El problema que resuelve, y el que casi lo arruina

Un modelo de video genera 5-15 s como máximo, así que un comercial de 30 s son
varios clips encadenados. El riesgo es que la cara cambie entre clips. La
solución que funcionó:

1. **Un keyframe por escena**, todos generados con `nano_banana_pro` usando la
   misma foto como `image_references`.
2. **Cada keyframe se anima** como `start_image` con un modelo de imagen-a-video.
   La cara del clip sale del keyframe, no de un texto: por eso se mantiene.

**EL FALLO A EVITAR:** la foto original tenía un cuadro colgado detrás. En dos
escenas el modelo copió ese cuadro al fondo **y duplicó la cara del sujeto**
colgada en la pared. Añadir "no paintings, no wall art" al prompt no bastó.
Lo que sí funcionó: generar primero un retrato limpio (escena 1, fondo neutro),
subirlo, y usar ESE como referencia para el resto de escenas. Regla: **la foto
de referencia debe tener fondo limpio, o se fabrica uno antes de seguir.**

Corolario: verificar CADA keyframe mirándolo antes de animarlo. Animar un
keyframe malo cuesta el triple que regenerar la imagen.

## Preparación de la foto

Las fotos de teléfono llegan con EXIF orientation (la nuestra venía con 6, o
sea 90°). Si no se endereza, el modelo trabaja con la persona de lado:

    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(foto))   # <- imprescindible
    # recorte 9:16 centrado en la persona -> 1080x1920

## Modelos y costos reales (plan free, sep-2026)

| Paso | Modelo | Costo |
|---|---|---|
| Keyframes | `nano_banana_pro`, 9:16, 2k | 2 cr / imagen |
| Video | `minimax_h3_max`, 9:16, 5 s, 768p | 12,5 cr / clip |

`kling3_0` y `kling3_0_turbo` devuelven **"Requires basic plan or higher"** con
el plan free, aunque aparezcan en el catálogo y `get_cost` responda. El costo se
preflighta con `get_cost:true`, pero el permiso de plan solo se ve al enviar.

Otras dos cosas del plan free: el backend responde **429 rate_limit_reached**
con más de 2 envíos simultáneos (se manda de dos en dos), y `mode:"pro"` de
Kling también exige plan de pago. Si aparece una recomendación de preset, se
declina con `declined_preset_id` y se genera lo pedido.

Total de la pieza: 9 imágenes + 6 clips = **93 créditos**.

## Los rótulos NO los hace el modelo

Se piden explícitamente sin texto ("NO text, NO letters, NO numbers") y se
añaden en post con un `.ass` (`titulos.ass` en esta carpeta): Montserrat
ExtraBold, blanco con la palabra clave en ámbar DMA #E8A04A, fade de 320 ms y
pop de escala. Los modelos escriben texto con errores; así además queda con la
tipografía de la casa.

## Montaje

- Cada clip a 1080x1920@30 y recortado a 4,8 s.
- Encadenado con `xfade=fade:duration=0.4`, y `fadeblack` antes de la placa.
- Placa final: degradado azul DMA + el logo REAL (extraído en base64 de
  `tutor/pagina/index.html`), recoloreado a blanco conservando en ámbar los
  píxeles donde R-B > 15 (la grúa y los acentos). Nunca un logo generado.
- Pista de audio silenciosa (`anullsrc`): Instagram se queja de un MP4 sin
  pista de audio.
- Dos salidas: master CRF 18 (~31 MB) y web CRF 22 (~16 MB, por el tope de
  30 MB al enviarlo por chat).

Dos trampas de numpy en la placa: un degradado `(H,1,3)` produce una imagen de
**1 píxel de ancho** que ffmpeg estira sin avisar (hay que hacer broadcast a
`(H,W,3)`), y `alpha_composite` no pegó el logo — `paste(logo, pos, logo)` sí.

## Idioma

Los rótulos van en español porque la audiencia lo es, aunque el brief original
los pidiera en inglés. La versión en inglés es solo regenerar el `.ass`.
