---
name: fable-plan
description: Planifica cualquier función, mejora o pieza nueva de ESTE repo (meta-ads-dashboard.html de DMA) antes de escribir una línea de código. ACTIVA SIEMPRE que el usuario pida "planea", "plan para", "cómo harías", "diseña la implementación de", "quiero agregar X", "nueva función", "mejora a la calculadora/landing/matriz/script/workflow", o antes de empezar cualquier cambio no trivial (más de un archivo, o que toque publicación/GHL/datos). También cuando otra skill (leadmagnet-app, landing-*) vaya a arrancar un trabajo grande: primero el plan con esta skill, después la ejecución.
---

# FABLE-PLAN — Cómo se planifica en este repo

Este repo NO es un proyecto de software clásico: es el sistema de marketing de
Design Modeling Academy. No hay `package.json`, ni suite de tests, ni build.
Hay piezas HTML autocontenidas, datos curados a mano, un script Python y dos
GitHub Actions. Un plan genérico de "correr los tests" aquí no significa nada;
la verificación es **por pieza** y está definida abajo.

## Regla cero: nunca proponer sin explorar

Antes de escribir el plan, lee los archivos de la zona que vas a tocar.
Mapa de zonas → lectura obligatoria:

| Zona a tocar | Leer PRIMERO |
|---|---|
| Lead magnets / apps (`calculadora-zapatas/`, futuras `calculadora-*/`) | `.claude/skills/leadmagnet-app/SKILL.md` (la receta completa), luego `calculadora-zapatas/app.html` (patrón de referencia: candado, CALC-START/END, chips CUMPLE/VERIFICAR), `GUIA-MONTAJE.md` |
| Landings / páginas de funnel | `.claude/skills/landing-producto/SKILL.md` o `landing-evento`/`landing-agenda` según el tipo, + `calculadora-zapatas/index.html` y `gracias-agenda.html` como implementación real |
| Matriz de contenido (`matriz-viral/`) | `matriz-viral/CLAUDE.md` (reglas fijas del sistema) y `matriz-viral/STATUS.md` (qué corrió de verdad y qué está pendiente) — SIEMPRE los dos |
| Script de refresco (`scripts/refresh_matriz.py`) | El docstring del script (contrato defensivo: si Apify falla, NO escribe y sale 0) y `.github/workflows/refresh-matriz.yml` que lo invoca |
| Publicación / GitHub Pages | `.github/workflows/publish-matriz.yml` — fíjate en `paths:` y en el paso "Armar carpeta pública": **lo que no esté listado ahí NO se publica**, aunque hagas merge |
| Skills (`.claude/skills/`) | Otra skill existente del mismo tipo, para copiar formato (frontmatter con `name` = carpeta y `description` con disparadores, en español) |

Si el pedido cruza zonas (casi siempre: una app nueva toca app + landing +
workflow + brief), lee las de TODAS las zonas involucradas.

## Las preguntas obligatorias del plan

Todo plan responde estas seis, en este orden, por escrito:

1. **¿Cuál es el problema real detrás del pedido?** Aquí casi todo existe para
   una sola cosa: llevar gente al Máster BIM+IA vía comentario/DM/lead. Si el
   pedido no conecta con eso, pregunta para qué es antes de asumir.
2. **¿Qué es lo más pequeño que lo resuelve?** Este repo premia piezas chicas
   que se publican rápido (un botón, una sección, un campo en el JSON) sobre
   sistemas. Propón el mínimo y anota el "después, si funciona".
3. **¿Qué se rompe con este cambio AQUÍ?** Checklist específico del repo:
   - ¿Tocas `matriz.json`? → lo lee la app de Patricio en Vercel
     (`dg-contenido-ia.vercel.app`) por la URL pública de Pages; no cambies
     claves del esquema (`generado, total_reels, ejes, reels[]`) sin avisar.
   - ¿Tocas HTML que se pega en GHL? → `ghl-landing.html` se GENERA desde
     `index.html` (no se edita a mano) y todo debe seguir autocontenido con
     URLs absolutas.
   - ¿Creas carpeta nueva en la raíz? → hay que añadirla a
     `publish-matriz.yml` (paso "Armar carpeta pública" + `paths:`) o no
     existirá en Pages.
   - ¿Tocas el candado/token de una app? → la membresía GHL embebe la app
     con `?acceso=TOKEN`; romper el token rompe el portal de alumnos.
   - ¿Tocas `fuentes/`? → NO. Es dato crudo, solo lectura (regla fija 4 del
     CLAUDE.md de la matriz).
4. **¿Qué casos límite aplican?** Los recurrentes de este repo: usuario sin
   registro (candado), webhook GHL caído (`mode:'no-cors'`, nunca bloquear el
   acceso), Apify sin crédito (plan free → el script debe salir limpio),
   métricas ausentes (se marca `s/d`, jamás se inventa), caché CDN de Pages
   (~10 min; saltarla con `?v=N` o `raw.githubusercontent.com/.../gh-pages/...`).
5. **¿Cómo verificamos que quedó?** Con los comandos reales (sección
   siguiente). Cada paso del plan nombra SU verificación; "se ve bien" no es
   una verificación salvo que diga quién lo mira y dónde.
6. **¿Qué NO vamos a hacer y por qué?** Lista explícita. Motivos típicos
   aquí: cuesta crédito de Apify, requiere plan de pago (Inbound Webhook de
   GHL cobra por ejecución), promete algo que no existe (envío por
   correo/WhatsApp), o es "después, si funciona" del punto 2.

## Cómo se verifica en este repo (los comandos de verdad)

- **Lógica de cálculo de una app**: extraer la función pura y compararla
  contra el Excel fuente, magnitud por magnitud, tolerancia 1e-6 relativa:
  ```bash
  sed -n '/CALC-START/,/CALC-END/p' calculadora-zapatas/app.html > /tmp/calc.js
  node /tmp/test-calc.js   # test ad-hoc que importa calc.js y compara vs Excel
  ```
  Cero diferencias o no se publica. Sin Excel fuente no hay app.
- **HTML en navegador real**: smoke test Playwright con el Chromium
  preinstalado (`executablePath: '/opt/pw-browsers/chromium'`), bloqueando
  `**fonts.g**` y los widgets de GHL (el sandbox no llega a esos dominios).
  Ruta mínima: candado sin registro → formulario → redirección con token →
  resultados renderizados → caso que falla marca VERIFICAR → cero errores JS.
- **Lint HTML**: `htmlhint <archivo>.html` (el hook de sesión lo instala).
  Atrapa etiquetas rotas, no diseño.
- **Script Python**: `python3 -m py_compile scripts/refresh_matriz.py` +
  correrlo SIN `APIFY_TOKEN` y confirmar que sale 0 sin tocar la matriz
  (ese es su contrato). Con token solo si el usuario aprueba el gasto
  (topes: ver reglas fijas del CLAUDE.md de la matriz).
- **JSON de la matriz**: `python3 -m json.tool matriz-viral/matriz/matriz.json > /dev/null`
  y verificar que el esquema (`generado, total_reels, ejes, reels[]`) no cambió.
- **Ojo humano (Dayana)**: obligatorio para todo lo visual (brandkit, copy) y
  todo lo que se monta en GHL — el montaje en GHL siempre lo ejecuta ella o su
  Claude local, con guía copy-paste estilo `GUIA-MONTAJE.md`. El plan marca
  esos pasos como "lo ejecuta Dayana" y entrega la guía, no asume acceso.
- **Publicación**: tras el merge, la Action `publish-matriz.yml` publica a
  `gh-pages`; verificar la URL pública real
  (`https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/...`)
  recordando la caché de ~10 min.

## Git y ramas (no hay main)

- La rama por defecto es **`claude/remote-control-setup-GUe3f`**. No existe
  `main` ni `master`.
- Se desarrolla en la rama designada de la sesión, PR (draft) contra la rama
  por defecto, merge tras revisión.
- **Nunca** mergear ramas de otras sesiones sin `git diff --stat` primero —
  una rama vieja puede pisar trabajo. Rescatar archivos puntuales con
  `git checkout <rama> -- <archivo>`.
- Commits en español, descriptivos, una pieza lógica por commit (mira
  `git log --oneline` para el estilo).

## Formato del plan

Pasos **pequeños y reversibles**, cada uno con su verificación pegada:

```
## Plan: <título>

**Problema real:** …
**Lo mínimo que lo resuelve:** …
**Qué NO haremos:** … (y por qué)
**Riesgos aquí:** … (del checklist del punto 3)

### Pasos
1. <cambio chico y reversible>
   ✓ Verifica: <comando o revisión concreta de la lista de arriba>
2. …
   ✓ Verifica: …
N. PR draft a claude/remote-control-setup-GUe3f + qué mirar en la revisión
   ✓ Verifica: Action verde + URL pública si aplica + ojo de Dayana si es visual
```

Un paso que no se puede deshacer con un `git revert` limpio (gastar crédito
de Apify, publicar a Pages, montar en GHL, mandar algo a la app de Patricio)
va al FINAL del plan y marcado como **irreversible — confirmar antes**.

## La regla de las preguntas

**Si la respuesta a una pregunta puede cambiar el plan, se pregunta ANTES de
escribirlo.** (Ej.: "¿hay Excel fuente para esta calculadora?" — sin eso no
hay plan posible; "¿esto va a GHL o solo a Pages?" — cambia la arquitectura
del HTML.)

**Si no lo cambia, se decide con el criterio del repo y se ANOTA la decisión
en el plan** con una línea "Decidido: X porque Y", para que Dayana pueda
vetarla en la revisión sin que el trabajo se bloquee esperándola.
