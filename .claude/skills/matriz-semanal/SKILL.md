---
name: matriz-semanal
description: |
  Revisa las publicaciones de la semana y alimenta la matriz viral con sus métricas reales, sin depender de Apify.

  Usa este skill cuando Dayana diga: "matriz-semanal", "revisión semanal", "aquí están las estadísticas de la semana", "actualiza la matriz con estas métricas", "estas son las stats de los posts", "revisemos cómo fue la semana", o cuando pegue una tabla de métricas de Instagram/Facebook Insights (vistas, alcance, interacciones, comentarios, guardados). Úsalo también cuando pregunte qué funcionó o qué no funcionó esta semana.
---

# Skill: matriz-semanal

Cierra el ciclo semanal del sistema de contenido: **métricas reales → matriz actualizada → lecciones → ajuste del calendario**.

Pensado para el periodo **sin Apify** (el crédito se reinicia el 10 de agosto de 2026). Los datos los pega Dayana desde Instagram/Facebook Insights.

---

## Flujo (5 pasos)

### 1. Recibe la tabla
Dayana pega una tabla con las métricas de la semana. Columnas típicas (en cualquier orden, con o sin acentos):

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

---

## Reglas
- **Nunca inventes métricas.** Lo que no venga en la tabla se queda vacío. Una matriz con huecos honestos vale más que una llena de suposiciones.
- **Registra siempre Facebook aparte** (`views_facebook`, `comentarios_facebook`) — es un canal propio, no un espejo.
- Marca las piezas sin shortcode con `reconciliar_shortcode: true`; cuando Apify vuelva (10 ago), se reconcilian solas corriendo `scripts/refresh_matriz.py`.
- El resumen para Dayana va **en 4-5 líneas máximo**: el ganador, el peor, la lección accionable y qué cambiar. Nada de reportes largos.

## Cuando Apify vuelva (10 ago 2026)
Este skill sigue sirviendo para las lecturas y el ajuste, pero la recolección pasa a ser automática:
```bash
APIFY_TOKEN=xxx python3 scripts/refresh_matriz.py
```
y la Action `.github/workflows/refresh-matriz.yml` lo corre solo cada semana.
