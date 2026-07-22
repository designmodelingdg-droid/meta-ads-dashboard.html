---
name: arranque
description: Manual de arranque para CUALQUIER proyecto nuevo de Dayana / Design Modeling. ACTIVA SIEMPRE que el usuario diga "proyecto nuevo", "nuevo proyecto", "arrancar proyecto", "empezar proyecto", "crear un repo", "kickoff", "vamos a construir [algo] desde cero", "día 1 de", o pida crear una app/herramienta/sistema que todavía no tiene repositorio. Úsalo ANTES de escribir la primera línea de código - define las preguntas previas, el stack por defecto, el día 1 no negociable y el checklist de salida del arranque. NO aplica a trabajo dentro de un proyecto ya arrancado.
---

# ARRANQUE — Cómo empezar un proyecto nuevo (manual destilado de cicatrices reales)

Este manual sale de la autopsia del repo `meta-ads-dashboard.html`: un repo
que se llama como un dashboard que nunca existió, sin rama `main`, sin
CLAUDE.md en la raíz, con el deploy arreglado a las patadas en dos commits, y
con un bloqueo de red descubierto a mitad del trabajo. También sale de lo que
SÍ funcionó ahí: reglas escritas el día 1, stack aburrido, y skills extraídas
de patrones probados. No repitas las cicatrices; repite los aciertos.

## FASE 0 — Antes de escribir código (30 minutos, obligatoria)

Responde estas tres preguntas POR ESCRITO (irán al CLAUDE.md). Si el usuario
no las respondió en su mensaje, pregúntaselas antes de crear nada:

1. **¿Qué problema resuelve?** Una frase. Si necesitas dos, el alcance ya
   está creciendo antes de empezar.
2. **¿Quién lo usa?** Persona concreta: "un ingeniero que llega desde un reel
   de Instagram", no "los usuarios".
3. **¿Cuál es la primera cosa VISIBLE que demuestra que funciona?** Una URL
   que se abre, un cálculo que da el número correcto, un formulario que
   guarda un lead. Eso — y solo eso — es la meta de la semana 1.

Además, en la Fase 0 (cicatrices directas de este repo):

- **Nombra el repo por el proyecto, no por un archivo ni por la idea del
  día.** `meta-ads-dashboard.html` quedó pegado para siempre en cada URL
  pública (`...github.io/meta-ads-dashboard.html/calculadora-zapatas/`)
  porque renombrar rompía links ya compartidos con leads. El nombre del repo
  es una decisión PÚBLICA y casi irreversible: minúsculas, guiones, sin
  extensión, sin nombre de herramienta. Ej: `dma-leadmagnets`,
  `matriz-viral`.
- **Verifica los bloqueos del entorno ANTES de prometer nada.** En este repo
  se descubrió a mitad del trabajo que `api.apify.com` estaba bloqueado por
  la política de red del entorno remoto, y toda la recolección tuvo que
  migrar a la máquina local. Día 1: haz un `curl -sI https://dominio-clave`
  a cada API externa que el proyecto necesite. Si algo da 403 de política,
  decide en ese momento (pedir que lo permitan en Settings del entorno, o
  plan B local) — no cuando ya hay trabajo apilado.

## FASE 1 — Stack: mínimo y aburrido

Regla: **una decisión reversible hoy vale más que la "perfecta" la próxima
semana.** Elige lo que ya conoces, anota el porqué, y sigue.

Stack por defecto de Dayana (el probado en este repo — úsalo salvo que el
proyecto exija otra cosa, y si la exige, pregunta antes de asumir):

| Pieza | Elección | Por qué |
|---|---|---|
| App / herramienta | **HTML autocontenido** (un archivo, CSS y JS inline, cero build, cero dependencias) | Se pega como Custom Code en GHL/Sharp CRM, se publica en Pages tal cual, y no hay `node_modules` que mantener |
| Hosting público | **GitHub Pages vía rama `gh-pages`** (action `peaceiris/actions-gh-pages@v4`) | La vía "Source: GitHub Actions" FALLÓ en este repo porque el token del workflow no puede habilitar Pages solo; la rama `gh-pages` se activa sola, sin pasos manuales en Settings |
| Funnel / captura | **GoHighLevel (Sharp CRM)**: formulario nativo embebido, membresía con iframe, bot por palabra clave | Es el CRM real del negocio; el patrón completo está en el skill `leadmagnet-app` |
| Automatización | **Python + GitHub Actions** solo cuando algo deba correr sin humanos | Un script en `scripts/` + un workflow; nada de frameworks de pipelines |
| Datos externos | **Apify con topes SIEMPRE** (`maxItems`, `maxTotalChargeUsd`, mostrar costo y esperar OK) | Regla que evitó sorpresas de facturación durante semanas de corridas |

**Registro de decisiones:** cada elección de stack va al CLAUDE.md con una
línea de porqué (como la tabla de arriba). Cuando un modelo futuro pregunte
"¿por qué esto es un solo HTML?", la respuesta debe estar escrita, no en la
memoria de nadie.

## FASE 2 — El día 1 no negociable

Nada de esto se pospone. En este orden, el mismo día:

1. **Git bien parido:**
   ```bash
   git init -b main          # main como default, NO una rama de sesión
   printf '__pycache__/\n*.pyc\n.DS_Store\nnode_modules/\n' > .gitignore
   git add -A && git commit -m "Arranque: estructura, CLAUDE.md y hola público"
   git push -u origin main
   ```
   Cicatriz: este repo tiene como rama default `claude/remote-control-setup-GUe3f`
   (una rama de sesión de Claude) y `__pycache__/*.pyc` commiteados porque
   nunca hubo `.gitignore`. El workflow de deploy tuvo que enumerar tres
   ramas `claude/*` a mano para saber cuándo publicar.

2. **CLAUDE.md EN LA RAÍZ** (no enterrado en una subcarpeta). Contenido
   mínimo, calcado del que sí funcionó en `matriz-viral/CLAUDE.md`:
   - Qué es el proyecto, quién lo usa, qué vende/logra (las 3 respuestas de Fase 0).
   - **Reglas fijas** numeradas (las de este repo que valen oro: "nunca
     inventar datos — lo que falta se marca `s/d`", "la carpeta de datos
     crudos no se edita nunca", "toda corrida pagada lleva tope de costo").
   - **Estructura** de carpetas con una línea de propósito por carpeta.
   - **Comandos** reales: cómo se prueba, cómo se publica, cómo se corre la rutina.
   - Registro de decisiones de stack (tabla de Fase 1).

3. **Estructura explicada, no solo creada.** Carpetas con `.gitkeep` si están
   vacías, y cada una nombrada en el CLAUDE.md. En este repo funcionó
   perfecto (`fuentes/ → solo lectura`, `matriz/`, `guiones/`); lo que faltó
   fue el mapa a nivel raíz cuando aparecieron `calculadora-zapatas/`,
   `scripts/` y `.github/`.

4. **Deploy del "hola" HOY, no cuando haya algo que mostrar.** Un
   `index.html` mínimo publicado en Pages el día 1. Cicatriz: aquí el deploy
   se intentó recién con el lead magnet listo y costó dos commits de arreglo
   (`4aaa8c6` y `72b1ea5`) y corridas fallidas, con el trabajo ya esperando.
   Con el "hola" publicado el día 1, la tubería está probada cuando de verdad
   la necesitas — y ya tienes la URL pública real para planear el funnel.

5. **STATUS.md en la raíz** con checkboxes: qué está listo, qué está
   pendiente, qué está bloqueado y por qué. En este repo fue lo que permitió
   retomar el trabajo entre sesiones y dejar documentado el bloqueo de Apify
   con sus dos salidas. Se actualiza al final de cada sesión de trabajo.

## FASE 3 — Cero sobre-ingeniería

- **Nada de capas para problemas que no existen.** Ni framework, ni build,
  ni base de datos, ni tests exhaustivos de arranque. Este repo entero — app,
  landing, funnel, automatización — vive en HTML plano + un script Python, y
  eso es una virtud, no una deuda.
- **La verificación sí, la arquitectura no.** Lo que este repo verificó desde
  el inicio (fórmulas contra el Excel fuente con tolerancia 1e-6, smoke test
  de Playwright del flujo completo, métricas reales vs simulación) valió cada
  minuto. La regla: verifica LO QUE EL USUARIO VE; no construyas
  infraestructura para lo que nadie pidió.
- **Extrae skills DESPUÉS de la segunda repetición, no antes.** Aquí
  `landing-producto` → `landing-evento` → `landing-agenda` → `leadmagnet-app`
  se destilaron de patrones ya probados en producción. Nunca escribas una
  skill especulativa de algo que aún no funcionó una vez.
- **Alcance:** cuando aparezca la idea nueva a mitad del arranque (aquí:
  dashboard → matriz viral → calculadora → bot → campañas), la pregunta
  obligatoria es "¿esto es ESTE proyecto u OTRO repo?". Este repo acumuló
  tres proyectos bajo un nombre que no describe a ninguno. Un pivote es
  legítimo; que se herede el repo del proyecto muerto, no.

## CHECKLIST DE SALIDA DEL ARRANQUE

El arranque está terminado solo cuando TODO esto es verdad:

- [ ] Las 3 respuestas de Fase 0 escritas en el CLAUDE.md de la raíz.
- [ ] Repo nombrado por el proyecto (sin extensiones, sin nombre heredado de otra idea).
- [ ] Rama default `main`; ninguna rama de sesión `claude/*` es la default.
- [ ] `.gitignore` antes del primer commit (nunca `__pycache__` en el historial).
- [ ] CLAUDE.md en la raíz: reglas fijas, estructura, comandos, decisiones de stack con porqué.
- [ ] STATUS.md con el estado real (listo / pendiente / bloqueado).
- [ ] "Hola" publicado y URL pública verificada con el navegador (no asumida).
- [ ] APIs externas probadas desde ESTE entorno (`curl -sI`); bloqueos anotados en STATUS.md con plan B.
- [ ] Topes de costo escritos como regla para todo servicio pagado.
- [ ] Regla de datos honestos escrita: lo que no se midió se marca `s/d`, jamás se inventa.
- [ ] Cero capas especulativas: si una pieza no sirve a la "primera cosa visible", no existe todavía.

Si un punto no se cumple, el arranque NO terminó — no importa cuánto código haya.
