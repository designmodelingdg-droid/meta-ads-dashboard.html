# Pizarra dibujada (estilo 9)

Video explicativo **sin presentador**: dibujos técnicos que se trazan solos sobre papel, con un
marcador DMA que sigue la línea, y la **voz de Gabriel hecha con IA** explicando. Aprobado por
Dayana el 19-oct-2026 con «5 tipos de cimentación» (referencias externas: reels de pizarra a mano
de cimentaciones; se adaptó el lenguaje, no los textos).

| Archivo | Qué es |
|---|---|
| `draw.ts` | Motor: trazos con temblor de mano, rellenos que aparecen al cerrar el contorno, textos que se escriben, isométrico (`iso`, `box`), flechas, rayado de terreno. Paleta DMA. |
| `escenas-niveles.ts` | **Ejemplo vigente** (letras de marca): portada + N±0.00 + 5 niveles con un corte de capas que crece página a página + CTA NIVEL. |
| `escenas-cimentaciones.ts` | Primer ejemplo (5 tipos de cimentación). Usaba Kalam; con el `draw.ts` actual el texto sale en Anton/Overpass. |
| `Composition.tsx` | Páginas que se deslizan, marcador, subtítulos de 1–2 palabras con resaltador cobre, logo al pie, audio `mezcla.wav`. |
| `voz_clonada.py` | Voz de Gabriel con Chatterbox (MIT, CPU, gratis). La muestra de su voz no va en el repo. |
| `sfx_desde_escenas.py` | Sonido de marcador por tramo dibujado + papel en cada cambio de página + «ding» en el CTA. |

**Letras (Dayana, 19-oct-2026):** Anton para títulos, códigos y subtítulos; Overpass 800 para etiquetas. Nada de Kalam salvo que lo pida. Papel con cuadrícula de 60 px.

Proyecto Remotion: `src/draw.ts`, `src/scenes.ts` (= escenas), `src/Composition.tsx`,
`src/timing.json`, `src/words.json`; en `public/` las fuentes Anton y Overpass 800 (latin + latin-ext), `logo-dma-dark.png` y `mezcla.wav`.

Para sacar la línea de tiempo y generar los SFX:
```bash
npx esbuild dump.ts --bundle --platform=node --loader:.json=json --outfile=dump.js
# dump.ts: import { ELS, PAGE_START, TOTAL } from "./src/scenes"; console.log(JSON.stringify({els: ELS, pages: PAGE_START, total: TOTAL}))
```
