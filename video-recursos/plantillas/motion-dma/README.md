# Motion DMA: rutas de producto, cromado con cámara e isométrico

Proyecto Remotion con los estilos 11, 12 y 14 del catálogo `estilos-reels-dma`, que se hicieron en octubre de 2026:

| Estilo | Composición (`<id>-vertical` / `<id>-landscape`) | Archivo |
|---|---|---|
| 11 · Ruta de producto | `RutaFusion` (Máster v3, la aprobada), `RutaColeccion`, `RutaEspecializaciones`, `RutaAcero`, `RutaDiplomado` | `src/compositions/RutaFusion.tsx`, `src/rutas/*.tsx` |
| 11 · versiones anteriores del Máster | `RutaMaster` (v1, look de marca), `RutaCine` (v2, animaciones) | `src/compositions/` |
| 12 · Cromado con cámara | `AdWorkshopCromo` (solo vertical) | `src/rutas/AdCromo.tsx` |
| 14 · Isométrico (Anatomy) | `AnatomyConexion` | `src/rutas/Conexion.tsx` + `src/anatomy/` |

El kit común de las rutas está en `src/rutas/kit.tsx`: `makeTiming`, `useStage`, `Whip`, `LightLine`, `Burst`, `Glass`, `AppTile`, `TextTile`, `Pop`, `Hero`, `StepCard`, `Caption`, `Carousel`, `Finale`, `Frame` y `HookRow`. Para un producto nuevo se copia `Acero.tsx` o `Diplomado.tsx`, se cambian los pasos y se registra en `src/compositions/index.ts`.

## Puesta en marcha

```bash
npm i
npx remotion studio src/index.ts
npx remotion render src/index.ts RutaAcero-vertical out/acero.mp4 --concurrency=2
./node_modules/.bin/tsc --noEmit   # typecheck
```

Pasada final (igual que en todos los videos DMA): `ffmpeg -i out/x.mp4 -vf "scale=in_range=full:out_range=tv,format=yuv420p" -af loudnorm=I=-14:TP=-1.5 -c:v libx264 -crf 18 -c:a aac -b:a 192k -movflags +faststart final.mp4`.

## Lo que NO viene en el repo (va en `public/`)

El repo es público, así que el material de marca y los certificados no se suben. Hay que ponerlos a mano:

- `public/rutas/logos/`:
  - logos de software: `revit.png` (solo el ícono), `navisworks.png`, `dynamo.png`, `python.png`, `robot.png`, `advance.png`, `autocad.png`, `openai.png`, `atc-white.png`;
  - credenciales: `micro.png` e `insignia.png` (DQ);
  - certificados de muestra: `cert-dm.jpg`, `cert-autodesk.jpg`, `cert-dq.jpg`, `cert-sabal.jpg`, `cert-udn.jpg`, con el **nombre del alumno y el número desenfocados** y rotulados «ejemplo».
  - Todo sale de la carpeta del Drive «Material de Diseño Gráfico / Logos de Marcas» y de la web.
- `public/rutas/tutor.mp4` (grabación real del Tutor IA), `whoosh.wav`, `musica_master.wav` (música original de `../../scripts/musica_original.py` o `musica_energica.py`) y `logo-dma.png`.
- `public/rutas/voz_<clave>.wav`: la voz de cada video, que sale de `voz/` (ver abajo).
- `public/adcromo/`: las tomas reales para el cromado con cámara.
- `public/sfx/`: los efectos de sonido del pack Kenney (CC0) que usa el kit.

## Voz de Gabriel con IA (`voz/`)

1. Escribir el guion en `voz/lines.json` (una clave por video, una frase por elemento). Escribe las palabras como se leen: «Páiton» para Python, «Bim más I A», y «Escríbenos y pide información» (así no sale «pilla»).
2. `VOZ_REF=/ruta/a/gabriel_ref.wav python tts.py` genera cada frase con Chatterbox Multilingual (CPU, gratis). Si una frase ya existe la salta; para rehacerla, se mueve a `old/`. **La muestra de voz de Gabriel nunca va al repo.**
3. `python3 armar.py <clave>` pega las frases sin silencios, normaliza a −14 LUFS y saca `voz_<clave>.wav` + `data_<clave>.json` (escenas y tiempos por palabra con Whisper). El json va a `src/data/<clave>.json` y el wav a `public/rutas/`.
4. No renderizar mientras corre `tts.py`: ocupa ~4 GB de RAM y el Chrome de Remotion se cae.

En `src/rutas/*.tsx`, los nodos se encienden con raíces de palabra que Whisper escribe igual («coordinas», cifras como dígitos «5», «120», «200»).

## Reglas

- El Máster nunca lleva precio. Los logos de software solo se usan si el programa los enseña.
- Las rutas se entregan en Reel y YouTube.
- Nada tapa la cara de Gabriel en el cromado: el texto va a y ≈ 1290 y los íconos a los lados.
- Tipografía: las rutas de octubre se aprobaron con la marca de `brand.json`. Las piezas nuevas usan la pareja de la Academia, Overpass 800/900 para títulos y Nunito para el resto, como ya hace `AdCromo.tsx`.
- `src/anatomy/` es de Anatomy (licencia MIT, ver `src/anatomy/LICENSE`). El esqueleto del estudio es Motion Architect (MIT, cabeceras en cada archivo).
