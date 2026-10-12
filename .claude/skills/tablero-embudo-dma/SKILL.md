---
name: tablero-embudo-dma
description: Crea el tablero semanal (dashboard HTML + resumen de 5 líneas) del embudo completo de Design Modeling Academy - gasto de Meta Ads → leads → CPL → contactos en GHL → citas agendadas → ventas, con cuadre OBLIGATORIO entre Meta y GHL, y conexión con la matriz de contenido orgánico. ACTIVA cuando Dayana o su equipo digan - "tablero", "tablero semanal", "reporte de la semana", "reporte de leads", "reporte meta ghl", "cómo va el embudo", "dashboard de campañas", "cuántos leads llegaron", "actualiza el tablero", "reporte de clientes", "cruza meta con ghl", o pidan cualquier reporte que combine Meta Ads con GoHighLevel. Para la parte de matriz de contenido orgánico, delega en matriz-viral/CLAUDE.md del repo meta-ads-dashboard.html.
---

# TABLERO-EMBUDO-DMA — Reporte semanal del embudo Meta → GHL

Este manual enseña a hacer el reporte como lo hace Dayana (Design Modeling
Academy, Quito). El tablero existe para responder **una sola pregunta**:
¿el gasto de Meta se está convirtiendo en citas y ventas, y en qué etapa
se cae el embudo?

## Contexto del negocio (por qué estos números)

- El embudo real: anuncio de Meta o contenido orgánico → landing / lead
  magnet (ej. `calculadora-zapatas/`) → contacto en **GHL (Sharp CRM)** →
  bot/seguimiento por WhatsApp → **cita agendada** → **venta**.
- El producto ancla es el **Máster Internacional en BIM Management e IA**
  ($2,699.99). **Nunca se vende ni se cotiza por chat/contenido** — el
  contenido y los anuncios generan conversación (CTA: comenta "BIM" o
  "IA") y el cierre pasa por cita. El tablero debe reflejar esa lógica.

## Fuentes de datos (en este orden)

1. **ads-cli** — la app de Meta que Dayana creó (Marketing API). Corre en
   su máquina local, NO vive en este repo. Desde una sesión remota:
   pedirle que corra el pull y pegue/suba el JSON o CSV. Por campaña:
   gasto, impresiones, clics, leads, rango de fechas.
2. **API de GHL** — contactos nuevos del periodo (con fuente/tag/campaña),
   citas agendadas en los calendarios, y oportunidades con su etapa
   (**ganada = venta**, con su valor).
3. **Fallback de solo lectura:** si la sesión tiene el MCP de Windsor.ai
   conectado, se pueden jalar las métricas de Meta en vivo (conector
   `facebook`). Sirve para no bloquear el tablero, pero el cuadre contra
   GHL sigue siendo obligatorio.
4. **Nunca inventar ni estimar métricas.** Dato que no llegó = `s/d`.
   Regla de la casa: *"una matriz con huecos honestos vale más que una
   llena de suposiciones"* — aplica igual al tablero.

## Pasos, en orden

1. **Periodo.** Semana cerrada lunes–domingo anterior (o la que pidan).
   Traer SIEMPRE también la semana previa, para los deltas.
2. **Recolectar Meta** (por campaña): gasto, leads, CPL = gasto ÷ leads.
3. **Recolectar GHL**: contactos nuevos por fuente, citas agendadas,
   ventas (oportunidades ganadas) y su valor.
4. **CUADRE Meta ↔ GHL — el paso que no se salta.** Por cada
   campaña/fuente, comparar los leads que reporta Meta contra los
   contactos que realmente llegaron a GHL. Si difieren: mostrar ambas
   cifras + la diferencia + causa probable (sincronización pendiente,
   duplicados, lead de formulario nativo sin mapear, UTM perdido).
   **Prohibido** forzar los números para que cuadren o mostrar una sola
   fuente como si fuera la verdad. Este es el error histórico a evitar:
   *"números que no cuadran entre Meta y GHL"* presentados como si
   cuadraran.
5. **Tablero HTML** con la spec de abajo.
6. **Resumen** de máximo 5 líneas: qué aprendimos, qué escalar / apagar /
   ajustar, y qué toca la próxima semana. Cada línea respaldada por un
   número del tablero.
7. **Matriz de contenido.** Si estás en el repo `meta-ads-dashboard.html`
   y toca la parte orgánica, seguir `matriz-viral/CLAUDE.md` (sección
   "rutina semanal") y traer al tablero solo los highlights: la mejor
   pieza de la semana vs la mediana de la cuenta, y si el CTA "comenta
   BIM o IA" generó conversación (referencia: DM18 logró tasa de
   comentarios ~100× la mediana con ese CTA).
8. **Guardar y versionar.** En el repo: `reportes/AAAA-Wss/` con
   `tablero.html`, `resumen.md` y los datos crudos en `fuentes/` (los
   crudos **no se editan nunca**, solo se leen). Commit + push.

## Reglas de decisión

- **CPL se juzga contra la mediana de las últimas 4 semanas**, no contra
  un número mágico. Sin histórico → se reporta, no se juzga.
- **Campaña con menos de 7 días corriendo:** se reporta, pero NO se
  recomienda apagarla todavía.
- **Etiquetas estrictas:** "ventas" = oportunidades GANADAS en GHL en el
  periodo. Citas ≠ ventas; leads de Meta ≠ contactos de GHL. Nunca
  mezclar nombres entre etapas.
- **Muchos leads y 0 ventas** → la recomendación apunta al seguimiento
  (bot, citas, llamadas), nunca a "poner el precio en el anuncio" — el
  Máster no se cotiza por chat.
- **Falta una fuente completa** (ej. no llegó el pull de GHL): el tablero
  sale igual, con `s/d` en esas columnas y una nota visible de qué falta.
  No se retrasa ni se rellena.

## Spec del tablero HTML

- **Un solo archivo, sin dependencias externas** (mismo criterio que las
  apps DMA: debe abrir local y poder pegarse en GHL como Custom Code).
- **Brandkit DMA fijo:** fuentes Overpass (títulos) + Nunito (cuerpo) con
  fallback de sistema; paleta `--azul-principal:#003e5c` ·
  `--azul-medio:#0a5a80` · `--azul-navy:#001e30` · `--naranja:#ca7520` ·
  `--naranja-claro:#e8a04a` · `--naranja-palido:#f7e8cc` ·
  `--crema:#fafaf7`. Logo:
  `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04bbc1fa8afa3be0bb00d8.png`.
- **Secciones en este orden:**
  1. Header con periodo y fecha/hora de corte de los datos.
  2. Fila de KPIs: Gasto · Leads Meta · CPL · Contactos GHL · Citas ·
     Ventas — cada uno con su delta vs semana anterior.
  3. Embudo visual con el % de paso entre etapas.
  4. Tabla por campaña (gasto, leads, CPL, contactos GHL, citas, ventas).
  5. **Tabla de cuadre Meta vs GHL** con diferencia y causa probable.
  6. Highlights de contenido orgánico (si la matriz está al día).
  7. El resumen de 5 líneas.
- Deltas en color según dirección **del negocio**, no del número: CPL que
  baja es verde; gasto que sube con CPL estable no es alarma.

## Cómo se ve un buen resultado (checklist antes de entregar)

- [ ] Cada número es rastreable a un archivo o respuesta de API con
      fecha — cero números "de memoria".
- [ ] La tabla de cuadre Meta vs GHL existe y muestra ambas fuentes lado
      a lado, **aunque cuadren**.
- [ ] Las sumas por campaña dan el total (verificar la aritmética antes
      de entregar, no después).
- [ ] Todos los KPIs tienen delta vs semana anterior, o `s/d`.
- [ ] El HTML abre standalone sin internet y usa el brandkit DMA.
- [ ] El resumen cabe en 5 líneas y al menos una es una acción concreta
      para la próxima semana.
- [ ] Los datos crudos quedaron en `reportes/AAAA-Wss/fuentes/` sin
      editar.
