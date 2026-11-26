# Plantilla de artes de diciembre 2026

Con esto se generaron los carruseles, posts, historias y anuncios de diciembre
(sistema visual de noviembre + toque navideño + logo Autodesk ATC).

- `gen.py pieza.json salida/` → láminas 1080×1350 (HTML) · `node render.js salida/` las pasa a PNG.
- `ads.py anuncio.json salida/` → anuncios en 1:1, 3:4, 9:16 y 16:9 · `node render-ads.js salida/`.
- `historias.py` → cuadros 1080×1920 desde el calendario · `node render-h.js out/hist`.
- `fmt.sh arte.png prefijo` → adapta una foto a los 4 formatos de pauta con el sello DG | ATC.
- `piezas/` y `ads/`: el texto y la composición de cada pieza. Para cambiar un texto se edita su JSON y se regenera.

Las rutas de las capturas reales apuntan al banco de la sesión (`banco-real/`, sacado de las clases de Vimeo);
si no está, hay que volver a sacarlas. Los fondos se guardaron en JPG (los scripts esperan `fondo-*.png`).
Las artes finales están en la página de aprobación (artefacto «Matriz Diciembre DMA»).
