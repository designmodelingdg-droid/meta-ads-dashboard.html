# Recursos y plantillas de video DMA

Todo lo que hace falta para editar los reels y anuncios de DMA en cualquier conversación, sin volver a buscarlo. El catálogo de estilos (qué estilo usar y cómo se edita) vive en la skill `estilos-reels-dma`; aquí están el material y el código.

## 1. Recursos de Drive (logos, B-roll, fotos de Gabriel)

921 archivos (~7,4 GB) en **PLANIFICACIONES INTERNAS / Contenido Adicional**. El manifiesto con el id de cada archivo **no se sube a este repo, que es público** (los archivos están compartidos por enlace y quedarían expuestos): vive en esa misma carpeta del Drive, partido en 18 archivos `manifest-recursos-video-parte-1.tsv` … `-parte-18.tsv` (y las carpetas en `folders-recursos-video-parte-1..3.tsv`). Se bajan con el conector de Google Drive, se pegan en orden (`cat manifest-recursos-video-parte-{1..18}.tsv > manifest.tsv`) y luego:

```bash
python3 video-recursos/scripts/bajar_recursos.py "Logos de Marcas" --manifiesto manifest.tsv             # solo logos (~76 MB)
python3 video-recursos/scripts/bajar_recursos.py "MATERIAL PARA VIDEOS 2026" --manifiesto manifest.tsv   # B-roll (~1,6 GB)
python3 video-recursos/scripts/bajar_recursos.py --manifiesto manifest.tsv                               # todo
```

Lo más usado:

| Ruta | Qué hay |
|---|---|
| `Material de Diseño Gráfico/Logos de Marcas/Autodesk/` | Revit, Robot, Advance Steel, AutoCAD, Navisworks, Inventor (lockups blanco y negro, iconos), logos ATC y Learning Partner |
| `Material de Diseño Gráfico/Logos de Marcas/` (resto) | CSI (Etabs, Safe, SAP2000), Cype, Dynamo, Python, OpenAI, Idea Statica, convenios y sellos (DQ, Sabal, Uninaciones, ISTE, UAIII, EQS), logo DG 2026 |
| `MATERIAL PARA VIDEOS 2026/` | B-roll vertical: acero y naves industriales, cimentaciones, BIM para Máster/Diplomado, videos de validez, títulos y software |
| `Material de Diseño Gráfico/Instructores/`, `Gabriel Pantoja/` | Fotos de Gabriel en alta |
| `Material de Diseño Gráfico/Imagenes de Autodesk/` | Material oficial de producto |
| `Material de Diseño Gráfico/Cierre de Video Reels/` | Cierres de marca para Reels, Shorts y YouTube |
| `2025-Historias Recurrentes/Testimonios/` | Testimonios de alumnos (solo con permiso de publicación) |

Si se suben archivos nuevos a esa carpeta, hay que regenerar el manifiesto del Drive con el conector de Google Drive (`parentId = '<id>'`, recursivo y paginando).

Regla: el logo de un software solo aparece si el programa lo enseña. Acero = Revit, Robot y Advance Steel.

## 2. Plantillas (Remotion)

Cada archivo es el `src/Composition.tsx` de un video ya aprobado; se copian a un proyecto Remotion nuevo y se cambian tiempos, textos y material.

| Archivo | Estilo | Video de origen |
|---|---|---|
| `explicativo-pizarra-acero.tsx` | 1 · Explicativo (pizarra + Gabriel) | Acero «sobredimensionar», ganchos A/B/C |
| `publicitario-acero.tsx` | 6 · Publicitario (cortes con zoom e insertos) | Acero «sobredimensionar» |
| `demo-recurso-tres-bandas.tsx` | 3 · Demo de recurso «Tres bandas» | Pack de Dynamo (lead magnet) |
| `gabriel-motion-graphics.tsx` | 8a · Gabriel + motion graphics (gráficas detrás de él) | Acero «sobredimensionar» |
| `brag-web-en-celular.tsx` + `brag-plan-ejemplo.md` | 8b · 100 % animado (Brag), web real dentro de un celular | Pack de Dynamo |
| `pizarra-dibujada/` (motor + escenas + voz + SFX) | 9 · Pizarra dibujada a mano con voz de Gabriel (IA) | «5 tipos de cimentación» |

## 3. Scripts

- `scripts/editar.py` (**/editar**, el primer paso de todo reel): del crudo a `gabriel_editado.mp4` + `words.json`.
  ```bash
  python3 video-recursos/scripts/editar.py preparar trabajo/ hook.mov d1.mov d2.mov cierre.mov   # escribe trabajo/receta.json
  python3 video-recursos/scripts/editar.py render trabajo/                                         # corta, acelera, normaliza, transcribe
  ```
  - **Silero** (el VAD que ya trae faster-whisper) decide dónde hay voz; **Whisper** solo corrige los bordes para no comerse el final de una palabra. Probado con el crudo del Pack de Dynamo: salieron los mismos cortes que se habían hecho a mano.
  - **Encuadre a la cara**: si el clip es horizontal, YuNet (OpenCV) busca la cara y recorta el 9:16 centrado en ella (mediana, para que no baile).
  - **Receta** (`receta.json`): tramos por clip, velocidad (1.2× Gabriel, 1.1× clases) y LUFS. Se edita a mano y `render` rehace solo los clips cuya parte cambió.
  - **Volumen** a −14 LUFS en dos pasadas con pico máximo −1 dBTP (en voz suele quedar en −14,5 a −15 por el límite de pico).
- `scripts/bajar_recursos.py`: baja del manifiesto lo que se le pida.
- `scripts/recortar_gabriel.sh`: recorta a Gabriel (rembg `u2net_human_seg`) y deja un WebM con transparencia para el estilo 8a.

Los videos editados se guardan en la rama `vimeo-clips` (carpeta `vimeo-clips/editados/`), nunca en esta rama, para no hacer pesado el repo.
