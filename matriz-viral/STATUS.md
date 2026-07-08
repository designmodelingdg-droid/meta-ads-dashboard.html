# Estado del sistema — 2026-07-08

## Lo que ya está listo

- [x] Interview completada: cuenta propia `design_modeling_dg`, redes IG/TikTok/YouTube/Facebook, tema BIM+IA, tono cercano y técnico, 3-4 piezas/semana.
- [x] Referentes investigados: BIM Pure (Nicolas Catellier) confirmado. Dana de Filippi descartada — no se confirmó su handle público.
- [x] Estructura de carpetas creada: `fuentes/`, `transcripciones/`, `matriz/`, `guiones/`.
- [x] `CLAUDE.md` con reglas, actores y rutina semanal.
- [x] **Recolección real (Apify) — corrida en local**, ver abajo. Este entorno remoto sigue bloqueado para `api.apify.com`; toda la recolección se hizo desde Claude Code local de Dayana.
- [x] Instagram de `@bimpure`: 19 reels con transcripción (~$0.96).
- [x] Instagram de `@design_modeling_dg`: 17 reels con transcripción (~$1.10).
- [ ] TikTok, YouTube, Facebook — pendientes para ambas cuentas.
- [ ] Matriz de Contenido Viral — en construcción con los 36 reels de Instagram ya recolectados.
- [ ] Guiones simulados — pendiente de la matriz.

## Por qué la recolección no corrió desde este entorno

Esta sesión corre en un entorno remoto (Claude Code on the web) cuya política de red **no permite salir a `api.apify.com`** (la puerta de enlace responde 403 — bloqueo de política, no un error de token), confirmado en más de un intento. Ni el MCP de Apify ni una llamada directa por API funcionan desde aquí mientras esa política siga así. El token que se compartió en el chat está guardado solo en esa sesión (no en este repo, no en git) — la recolección real se resolvió corriéndola en Claude Code local, con el token cargado ahí vía `claude mcp add --header`.

## Dos caminos para completar la recolección

### Opción A — Permitir el dominio en este entorno
En la configuración de red del entorno (Claude Code on the web → Settings del entorno) agrega a la lista permitida:
- `api.apify.com`
- `mcp.apify.com` (si prefieres MCP en vez de API directa)

Con eso permitido, retomo desde aquí mismo: corro los actores con los topes de costo definidos en `CLAUDE.md`, guardo todo en `fuentes/` y `transcripciones/`, y construyo la matriz.

### Opción B — Correr la recolección en tu máquina local
Usa los prompts de abajo tal cual, en una carpeta local con Claude Code:

```
mkdir matriz-viral && cd matriz-viral
claude mcp add --transport http apify https://mcp.apify.com
claude
/mcp
```

Copia el `CLAUDE.md` de esta carpeta a tu `matriz-viral/` local (ya tiene tus datos: cuentas, tema, tono, cadencia, referentes) y pega el prompt de "Recolecta" más abajo. Cuando termines, tráeme de vuelta `fuentes/` y `transcripciones/` (o el repo actualizado) y yo continúo con la matriz y los guiones.

## Prompt de recolección — ya personalizado

```
Vamos a recolectar el contenido. Lee CLAUDE.md para recordar qué cuentas
y redes estamos estudiando.

Cuentas:
- Propia: design_modeling_dg (Instagram, YouTube @DesignModelingDG, TikTok, Facebook)
- Referentes: Dana de Filippi (Instagram @danadefilippi, YouTube "DanamoBIM")
              BIM Pure / Nicolas Catellier (Instagram @bimpure, YouTube "BIM Pure")

Usando el MCP de Apify, para cada red acordada:

1. Corre el actor correcto:
   - Instagram reels → apify/instagram-reel-scraper (trae transcripción)
   - Instagram posts → apify/instagram-scraper (métricas y captions)
   - TikTok → clockworks/tiktok-scraper (activa la opción de transcribir
     todos los videos)
   - YouTube → streamers/youtube-scraper (trae los subtítulos)
   - Facebook → busca el actor adecuado en el store de Apify antes de
     correr nada; si no hay uno confiable, avísame y seguimos sin esa red.
2. Topes obligatorios en CADA corrida: maxItems entre 30 y 50 por
   cuenta, y maxTotalChargeUsd de 1 dólar. Antes de correr cada actor,
   muéstrame los parámetros y el costo estimado, y espera mi OK.
3. Si una corrida tarda más de 45 segundos, no te quedes esperando:
   guarda el ID de la corrida, sigue con la siguiente red y recupera el
   dataset cuando termine.
4. Guarda todo:
   - Los datos crudos en fuentes/, un archivo por red.
   - Cada transcripción en transcripciones/, nombrada red-fecha-título
     corto, con sus métricas arriba: vistas, likes, comentarios,
     compartidos y fecha de publicación.
5. Ordena cada red de más viral a menos viral con las vistas reales del
   scraper. Si un dato no viene, escribe "s/d" — nunca lo inventes ni lo
   estimes.
6. Al final: cuántas piezas bajamos por red, las 5 más virales de todas,
   y cuánto crédito de Apify gastamos.

Solo cuentas y videos públicos. Si una cuenta es privada o el actor no
puede leerla, dime cuál y seguimos sin ella.
```

Una vez exista contenido real en `fuentes/` y `transcripciones/`, uso los prompts de "matriz", "simula" y "rutina semanal" que ya están documentados en `CLAUDE.md` (tomados tal cual de la guía) para producir `matriz/matriz-contenido-viral.md`, `matriz/patrones-de-viralidad.md` y los guiones en `guiones/`.
