# lucianomattica-design · scroll-craft

Skill de Claude Code para construir landing pages premium donde el scroll es la línea de tiempo: capas de profundidad en el hero, secciones que se comportan distinto entre sí, un movimiento firma por sitio, y verificación visual con screenshots antes de entregar.

Fork personalizado de [scroll-craft](https://github.com/nateherkai/scroll-craft) de Nate Herk (MIT).

## Instalar

```bash
claude plugin marketplace add prompteafacil-hub/scroll-craft
claude plugin install lucianomattica-design@lucianomattica
```

O desde el zip: descomprimilo y corré

```bash
claude plugin marketplace add ./lucianomattica-design
claude plugin install lucianomattica-design@lucianomattica
```

## Usar

```
/lucianomattica-design:scroll-craft
```

La skill entrevista antes de construir (vibra, recorrido, energía, momento a recordar, movimiento único, rango estético, escenas o mundo continuo, assets). Después planifica el hero por capas, escribe el HTML sobre un sistema de tokens y se saca screenshots del scroll en desktop y mobile para corregirse sola.

## Requisitos
- Node 18+, ffmpeg, Chrome.
- `npm i playwright-core` en la carpeta del proyecto para la verificación con screenshots.
- Clave de kie.ai solo si querés que genere imágenes. Con tus propias fotos y recortes PNG no hace falta.

Diagnóstico: `node plugins/lucianomattica-design/skills/scroll-craft/scripts/doctor.mjs`
