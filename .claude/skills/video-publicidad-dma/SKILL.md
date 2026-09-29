---
name: video-publicidad-dma
description: Hace videos animados de publicidad para Design Modeling Academy (DMA) con el motor pizarrón de video-pizarra, ya adaptado a la marca — robot ámbar del Tutor IA como mascota, fondos de plano navy, colores y logo DMA, voz sintética en español verificada, capturas reales del producto legibles en vertical — y los entrega en MP4 listo para Meta. Receta probada con el video del Tutor IA (28-sep-2026). ACTIVA cuando Dayana diga "video-publicidad-dma", "hazme un video animado para el anuncio", "video explicativo del [producto]", "video con voz para pauta", "un video como el del tutor", o pida un anuncio en video sin grabar a nadie.
---

# Video de publicidad DMA (pizarrón + voz)

Para **publicidad** (anuncios de Meta, piezas de venta). El contenido orgánico de la matriz lo graba
Gabriel: no se sustituye por esto.

Usa el motor de `.claude/skills/video-pizarra/template/` (SVG + GSAP) y lee su `SKILL.md` y
`references/engine-api.md` antes de escribir escenas. Este skill añade lo que ese motor no sabe de DMA.
El ejemplo terminado está en `ejemplo/scenes.tutor-ia.js` (y en `matriz-viral/videos/tutor-ia-pizarra/`).

## Por qué pizarrón y no «minimal»

Dayana comparó los dos: el estilo minimal (tarjetas de texto) «no se ve tan didáctico» y le faltaba voz.
Lo que funciona es el pizarrón: la mascota **actúa** lo que dice la voz, el texto se escribe a mano, cada
escena tiene su fondo y su herramienta, y las transiciones nacen de algo de la escena.

## 1 · Guion de voz primero

Una frase por escena en `audio/guion.txt`, en el orden gancho → problema → giro → cómo se usa → prueba →
confianza → acceso → cierre. 45-60 s de voz en total. Reglas:

- **Datos solo de fuentes del repo** (p. ej. `matriz/lanzamiento-tutor-ia-octubre.json` para el tutor) y
  respetar su lista de lo que NO se dice. Nada de precios del Máster.
- **Números en letra** («ciento treinta y tres», «minuto cuatro con nueve segundos»): Piper los lee mejor.
- **«BIM» se escribe «bimm»** en el guion (con «BIM» dice «Benjamin»; con «bim», «viven»). En pantalla sigue
  siendo «BIM». Otras siglas: escribirlas como suenan o desarrollarlas («inteligencia artificial»).
- **CTA de pauta:** «Pide información». El botón del anuncio lleva al formulario o a WhatsApp. No pedir
  palabras clave en un anuncio.

## 2 · Voz sintética (decisión de Dayana, 28-sep)

```bash
./voz.sh audio/guion.txt        # Piper es_MX-claude-high + verificación con Whisper
```

Genera `audio/l1.wav…lN.wav`, imprime las duraciones y transcribe cada frase. **Leer
`audio/verificacion.txt` siempre**: es la única forma de saber si pronunció bien sin escucharlo. Si una
palabra sale mal, se reescribe como suena y se repite. Alternativa de voz: `VOZ=es_MX-ald-medium`.
Si algún día graba Gabriel, sus notas de voz sustituyen a `lN.wav` (una por escena) y el resto no cambia.

## 3 · Escenas (`scenes.js`)

Partir de `ejemplo/scenes.tutor-ia.js`. Lo que ya trae y no hay que rehacer:

- `speed: 1, mode: 'B'` → los segundos del guion son segundos reales y no hay ajuste al ritmo de la música.
- `VOD = [...]` con las duraciones de la voz. Cada escena dura `VOD[k] + 0.5` y llama `vo(a)` al empezar,
  que guarda el inicio en `window.__VO` para montar la voz.
- **Mascota = el robot del Tutor IA** (`mascotShape` con antena, en `hatches.brand` ámbar `#E8A04A`).
  Nunca la mascota por defecto del motor: es la de otra marca.
- **Fondos DMA:** `plano` (navy `#0E2438` con cuadrícula) y `azul` (`#003E5C`), además de los del motor
  (papel, pizarra, cuaderno, milimetrado, kraft, sol ámbar). Uno distinto por escena.
- **Colores:** naranja de texto `#CA7520` sobre fondos claros, ámbar `#E8A04A` sobre oscuros.
- **Final:** mosaico de escenas + robot + «Pide información» + logo DMA (`assets/logo.png`, copiar de
  `video-tutor-ia/marca/logo-dma-claro.png`).
- Sincronía: los textos clave se escriben cuando la voz los dice (estimar por la posición de la palabra
  dentro de la frase y comprobar en el QA).

## 4 · Capturas reales del producto

Siempre pantallazos reales, nunca interfaces inventadas. Una captura de 1920 px en vertical no se lee:

```bash
python3 recortar_captura.py fotograma.png assets/cap-x.png "64,676,401,708" "401,676,849,708" --etiqueta "66,262,200,285"
```

Recorta los renglones reales y los apila en una tarjeta de ≤ 520 px, que el video amplía casi al doble.
Para sacar fotogramas de una grabación: `ffmpeg -ss 70 -i grabacion.mp4 -frames:v 1 f70.png`.

## 5 · QA y render

```bash
export CHROME_PATH=/opt/pw-browsers/chromium     # en la nube; en local, omitir
node render.mjs --every 1.5 && python3 contact.py 8   # mirar contact.jpg: texto cortado, escenas vacías
./render_con_voz.sh nombre-del-video                  # video + efectos + voz, -14 LUFS, y copia -movil.mp4
```

Copiar antes al proyecto `scripts/vo_times.mjs` y `scripts/render_con_voz.sh`. El render tarda ~2 min
por minuto de video: correrlo en segundo plano. Entregar la versión `-movil.mp4`.

## Lo que ya se aprendió peleándose con esto

- **Tipografías en local.** El Chromium del contenedor no confía en el certificado del proxy y no carga
  Google Fonts: sin avisar, todo sale en letra del sistema. `template/fonts/` y `template-estilos/fonts/` ya
  traen Caveat, Kalam, JetBrains Mono, Overpass y Nunito, y los `index.html` apuntan ahí.
- **Chromium ya está instalado** en la nube: no correr `npx playwright install`, usar `CHROME_PATH`.
- **El push a GitHub puede fallar con 403** si la conexión de GitHub caducó: se reconecta en
  https://claude.ai/connect-github.
- Los MP4 no se suben al repositorio. Al repo va `scenes.js`, `audio/guion.txt`, las capturas recortadas
  y un `STORYBOARD.md` con la fuente de cada dato, en `matriz-viral/videos/<slug>/`.
