# Gabriel motion cromado (estilo 10)

Para **pauta con Gabriel a cámara**. Palabras clave en cromo 3D con los colores de DMA, algunas
**detrás de Gabriel** (lo recortamos cuadro a cuadro), palabras pequeñas que entran con desenfoque,
íconos 3D que rebotan y transiciones con golpe. Aprobado por Dayana el 22-oct-2026 («está genial
para los videos de pauta», con los colores de la empresa). Referencia externa: un reel de un
contador con texto cromado; se adaptó el lenguaje de edición, no los textos ni los logos.

| Archivo | Qué es |
|---|---|
| `Motion.tsx` | Motor. No se toca por reel. Cromo `cobre` / `navy` / `blanco`, palabras chicas en cobre claro, íconos (pregunta, foco, código, archivo, flecha, check, gráfica, dinero), contador circular, cámara con empujes, golpes, zoom hacia fuera y whips; cortina de puntos a un estudio navy y destello cobre. |
| `guion.ts` | **Lo único que se edita** por crudo: portada, tiempos, palabras, capa (detrás/delante), íconos y transiciones. El de ejemplo es «5 scripts de Dynamo». |
| `Root.tsx` | Registra la composición `Motion` (1080×1920, 30 fps). |
| `matte.py` | Recorte de Gabriel → `public/<base>_alfa.webm` (VP9 con alfa). MediaPipe *selfie multiclass* + filtro guiado + relleno de huecos (la camisa blanca a rayas se confundía con el fondo). |
| `sfx-ejemplo.json` | Eventos de sonido del ejemplo para `sfx_mix.py` (whoosh, pop, stamp, boom, ding…). |
| `../../scripts/musica_energica.py` | Música original sin copyright, 137 BPM; `python3 musica_energica.py <intro_s> <compases> <cola_s> out.wav`. |

## Pasos con un crudo nuevo

1. **Corte de voz** con `/editar` (Gabriel 1,2×, sin pausas) → `gabriel_editado.mp4` 1080×1920.
2. **Palabras con tiempos**: Whisper sobre el editado (`words.json`).
3. **Recorte**: `python3 matte.py gabriel_editado.mp4 public/gabriel_alfa.webm mascara.jpg`
   (modelo `models/selfie_multiclass.tflite` de MediaPipe, 16 MB, no va al repo). Revisar `mascara.jpg`.
4. **Guion** (`guion.ts`): una o dos palabras clave por frase en cromo; las que van detrás de la
   cabeza, a la altura de la frente (y ≈ 420–520) para que se lean a los lados; las de delante, al
   pecho (y ≈ 1250). Cobre = palabra principal, navy = apoyo. Palabras chicas arriba (y = 300) o
   encima de la palabra de delante. Un ícono por idea, nunca logos de terceros que no se enseñen.
5. **Render**: `npx remotion render src/index.ts Motion out/video.mp4 --crf=18`.
6. **Audio**: música (`musica_energica.py`) + SFX (`sfx_mix.py` con `MUSIC_GAIN=0.16 SFX_GAIN=0.45`)
   mezclados con la voz del video y `loudnorm` a −14 LUFS. Sin silencios.

## Reglas
- Portada en el fotograma 0 (título arriba detrás de la cabeza, subtítulo y chip abajo), todo dentro del recorte 3:4 (y 300–1580).
- Solo colores DMA: navy `#0D1E3A`, cobre `#D78631`, cobre claro `#F3B26B`. Letras Anton (cromo) y Overpass 800 (palabras chicas).
- El texto cinético hace de subtítulo: no se añaden subtítulos aparte.
- El crudo y el recorte de Gabriel no se suben al repo.
