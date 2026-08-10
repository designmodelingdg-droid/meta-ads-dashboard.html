---
name: matriz-semanal
description: |
  Revisa las publicaciones de la semana y alimenta la matriz viral con sus métricas reales, sin depender de Apify.

  Usa este skill cuando Dayana diga: "matriz-semanal", "revisión semanal", "aquí están las estadísticas de la semana", "actualiza la matriz con estas métricas", "estas son las stats de los posts", "revisemos cómo fue la semana", o cuando pegue una tabla de métricas de Instagram/Facebook Insights (vistas, alcance, interacciones, comentarios, guardados). Úsalo también cuando pregunte qué funcionó o qué no funcionó esta semana.
---

# Skill: matriz-semanal

Cierra el ciclo semanal del sistema de contenido: **métricas reales → matriz actualizada → lecciones → ajuste del calendario**.

**Desde 2026-07-27 la recolección es AUTOMÁTICA** — la Action `metricas-semanales.yml`
corre cada lunes y actualiza la matriz sola. Dayana ya no tiene que pegar nada.

| Fuente | Para qué | Script |
|---|---|---|
| **Meta Graph API** | Nuestras métricas de IG y FB | `scripts/meta_organico.py` |
| **Meta `business_discovery`** | Competencia / sector (público) | `scripts/competencia.py` |
| **Apify** | Solo para estimar views/alcance de cuentas AJENAS | `scripts/refresh_matriz.py` |
| Tabla pegada a mano | Respaldo, o para las vistas de FB | `scripts/matriz_semanal.py` |

Tu trabajo ahora es **leer lo que llegó y sacar conclusiones**, no recolectar.

---

## Flujo automático (lo normal)

1. La Action ya actualizó `matriz.json` y `competencia.json` el lunes.
2. **Tú lees los cambios** (`git log`/`git diff` de `matriz-viral/matriz/`), completas
   `eje`/`tipo`/`nota` de las piezas nuevas, sacas las lecciones al brief y ajustas el
   calendario si un formato ganó claro.
3. Le resumes a Dayana en 4-5 líneas: ganador, peor, lección y qué cambiar.

Si la Action no corrió (o falta el secreto `META_TOKEN`), córrelo tú:
```bash
export META_TOKEN=...   # secreto del repo
python3 scripts/meta_organico.py --limit 30
python3 scripts/competencia.py
```

---

## Flujo manual (respaldo)

### 1. Recibe la tabla
Solo si hace falta (p. ej. vistas de Facebook). Dayana pega una tabla con las métricas de la semana. Columnas típicas (en cualquier orden, con o sin acentos):

`Publicación | Vistas | Alcance | Interacciones | Me gusta | Comentarios | Guardados | Compartidos | Cuentas con interacción | Visitas a perfil | Nuevos seguidores | Vistas en Facebook`

**Siempre pide las vistas de Facebook si no vienen** — está comprobado que FB puede ser más de la mitad del alcance real (el post ganador de julio sacó 9,103 de 11,193 vistas en FB).

### 2. Corre el script
Guarda la tabla en un archivo temporal y ejecuta:

```bash
# primero SIEMPRE en seco, para revisar el cruce
FECHA=2026-08-04 python3 scripts/matriz_semanal.py /tmp/semana.md --dry-run

# si el cruce es correcto, aplicar
FECHA=2026-08-04 python3 scripts/matriz_semanal.py /tmp/semana.md
```

El script cruza cada fila con las piezas ya registradas (por id, shortCode o parecido de título), actualiza las existentes, agrega las nuevas y muestra el ranking de la semana.

**Revisa el dry-run antes de aplicar:** si cruzó una pieza con la equivocada o creó una nueva que ya existía, corrígelo (puedes poner el `id` — ej. `DM128` — en la columna de título para forzar el cruce).

### 3. Completa lo que el script no puede saber
Las piezas nuevas quedan con `tipo`, `eje` y `nota` en blanco (marcadas `⟨pendiente⟩`). Complétalas a mano en `matriz-viral/matriz/matriz.json`:
- `tipo`: reel · carrusel · post · blog
- `eje`: NÚCLEO-IA · NÚCLEO-BIM · PROMO · OBRA · COMUNIDAD
- `nota`: **la lectura** — por qué funcionó o no (esto es lo más valioso de la matriz).

### 4. Saca las lecciones y actualiza el brief
Agrega una sección `## Actualización AAAA-MM-DD` en `matriz-viral/BRIEF-PATRICIO.md` con la tabla de la semana y **3-4 lecciones concretas**. Compara siempre contra lo que ya sabemos:

| Regla ya comprobada | Cómo verificarla esta semana |
|---|---|
| El lead magnet / herramienta gratuita es el formato ganador | ¿la pieza top fue un lead magnet? |
| Facebook puede ser la mitad del alcance | ¿cuánto vino de FB? |
| Sin pregunta directa → 0 comentarios | ¿las de 0 comentarios cerraron sin pregunta? |
| El humor va en reel, no en post plano | ¿hubo humor estático? ¿cómo rindió? |
| El hook debe tocar una duda real, no trivia | ¿el peor post tenía hook vago? |

Si algo **contradice** una regla, dilo explícitamente — la matriz se corrige con datos, no se defiende.

### 5. Ajusta el calendario y publica
- Si un formato/tema gana claramente, **súbele el peso** en `matriz/calendario-2026-XX.md` (y en la mezcla objetivo de `matriz/guia-formatos-y-redes.md`).
- Commit + push + PR + merge a la rama por defecto, para que la app y Patricio vean lo fresco.

### 6. Anota en el tablero
Siempre, al cerrar: escribe en **`matriz-viral/RECOMENDACIONES.md`**, que es
donde el equipo entero ve cómo vamos sin entrar a GitHub.
- una entrada nueva en «Historial» con la fecha y la lección de la semana
- lo que haya que hacer, en la tabla de arriba, en 🔴 y con responsable
- mueve a 🟢 lo que ya se hizo y a ⚫ lo descartado, con el motivo
- si una regla nueva se confirmó **tres semanas seguidas**, súbela a «Reglas
  permanentes» con su evidencia — deja de discutirse cada lunes

---

## Reglas
- **Nunca inventes métricas.** Lo que no venga en la tabla se queda vacío. Una matriz con huecos honestos vale más que una llena de suposiciones.
- **Registra siempre Facebook aparte** (`views_facebook`, `comentarios_facebook`) — es un canal propio, no un espejo.
- Marca las piezas sin shortcode con `reconciliar_shortcode: true`; cuando Apify vuelva (10 ago), se reconcilian solas corriendo `scripts/refresh_matriz.py`.
- El resumen para Dayana va **en 4-5 líneas máximo**: el ganador, el peor, la lección accionable y qué cambiar. Nada de reportes largos.

## ⭐ Vía preferida: Meta Graph API (ya no hace falta Apify)

Desde 2026-07-27 la recolección es **automática, oficial y gratis** con el token de
System User de Meta (el mismo de `dma-sales-assistant`, no expira):

```bash
export META_TOKEN=EAA...        # token de System User de "Design Modeling - Ads CLI"
python3 scripts/meta_organico.py --limit 30 --dry-run   # revisar
python3 scripts/meta_organico.py --limit 30             # aplicar
```

Trae de **Instagram** (@design_modeling_dg, id 17841404048578200): views, alcance,
likes, comentarios, guardados, compartidos, interacciones, visitas al perfil y
seguidores nuevos. De **Facebook** (página 101355061550758): comentarios, likes y
compartidos.

**Límite conocido:** Meta ELIMINÓ las vistas por publicación de Facebook de la API
(probado hasta v23) — solo se ven en la UI de Insights. Si necesitas ese dato,
pídeselo a Dayana y cárgalo a mano en `views_facebook`. Todo lo demás es automático.

## Si prefieres Apify (10 ago 2026)
Este skill sigue sirviendo para las lecturas y el ajuste, pero la recolección pasa a ser automática:
```bash
APIFY_TOKEN=xxx python3 scripts/refresh_matriz.py
```
y la Action `.github/workflows/refresh-matriz.yml` lo corre solo cada semana.
