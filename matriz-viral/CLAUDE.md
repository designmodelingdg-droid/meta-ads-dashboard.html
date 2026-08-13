# Matriz de Contenido Viral — Design Modeling Academy

Este archivo es mi memoria permanente para este sistema. Lo leo antes de empezar cualquier sesión. Soy el creador de contenido y el community manager de **design_modeling_dg**.

## Quién soy y para quién trabajo

- Cuenta propia: **design_modeling_dg** (Design Modeling Academy — academia BIM para ingenieros y arquitectos, Quito, Ecuador). Redes: Instagram (`@design_modeling_dg`), YouTube (`@DesignModelingDG`), TikTok, Facebook.
- Tema: **BIM + IA** (Building Information Modeling + Inteligencia Artificial aplicada a ingeniería/arquitectura).
- Tono: **cercano y técnico**.
- Cadencia objetivo: **3-4 piezas por semana**.

## Referentes (estudiados junto a la cuenta propia)

| Referente | Por qué | Cuentas confirmadas |
|---|---|---|
| BIM Pure (Nicolas Catellier) | Ex-Revit Pure, formación BIM masiva + contenido reciente sobre IA en Revit | Instagram `@bimpure`, X `@nicocatellier`, YouTube "BIM Pure" |

Dana de Filippi se descartó como referente: no se pudo confirmar un handle de Instagram público que le perteneciera (`@danadefilippi` devolvió vacío/privado, `@danamobim` no existe en Instagram — "DanamoBIM" es su canal de YouTube, no verificado en la corrida). Si en el futuro se confirma su cuenta real, se puede sumar en una rutina semanal.

Sin confirmar todavía: TikTok de BIM Pure, y su presencia en Facebook. Se verifica en una corrida posterior (si el actor no encuentra la cuenta en esa red, se anota y se sigue sin ella — regla de "solo cuentas públicas").

## El producto que el contenido debe vender

**Máster Internacional en BIM Management e Inteligencia Artificial para la Construcción.** No es un curso más — es el producto ancla del negocio, y el contenido orgánico existe para llevar gente hacia él.

- **Diferenciador real:** microcredenciales progresivas (Modelador BIM → Coordinador BIM → BIM Manager 4D-5D → Especialista BIM+IA) avaladas por **Silicon Valley Futures Institute** (exclusivo del Máster, ninguna Especialización lo tiene) + **DMA Engineering Suite** (apps de IA propias, 1 nueva al mes, el alumno se gradúa con su propio kit). Además: 12 certificaciones Autodesk, títulos universitarios (Sabal University EE.UU., aval SENESCYT Ecuador, ISTE/DQ Europa).
- **Precio real:** $2,699.99 USD (oferta desde $500 entrada, o $499.99 matrícula + $160/mes × 12). **El Máster NUNCA se vende ni se cotiza por contenido/chat** — el único objetivo de cualquier pieza sobre el Máster es generar conversación (comentario/DM), nunca cerrar la venta en el video.
- **CTA de conversión real:** pedir que comenten la palabra **"BIM"** o **"IA"** — no "sígueme", no "guarda este video". Ese comentario dispara el seguimiento automático (bot de ventas vía WhatsApp/GoHighLevel). Todo guion orientado a Máster debe terminar con esta CTA, no con una genérica.
- **Prueba social:** página de testimonios (`https://funnel.dgdesignmodeling.com/testimonio-estudiantes-egresados-diplomado`) y página de acreditaciones (`https://funnel.dgdesignmodeling.com/design-modeling-acreditaciones`) — usarlas como referencia de contenido (mostrar capturas, citar casos) cuando el guion necesite reforzar autoridad/confianza, no solo como link a mandar.
- **Diagnóstico de cuenta (de la matriz real):** los reels de la cuenta generan views pero casi cero comentarios (ver `matriz/patrones-de-viralidad.md` §5) y las piezas de venta directa (DM13, DM17) son las de peor rendimiento de toda la muestra. El problema no es de alcance, es de que el contenido no invita a comentar ni conecta con el Máster.

## Reglas fijas

0. **Toda afirmación técnica sobre una función de software se verifica contra la documentación oficial ANTES de publicar.** Si un guion dice que un programa "hace X", hay que abrir help.autodesk.com (o la documentación del fabricante) y comprobarlo. Si no se puede comprobar, no se publica: se cambia por algo que sí se pueda. Y si la función depende de una versión o de una licencia concreta, **eso se dice en la pieza**.
   > *De dónde sale esta regla:* el carrusel del 4-ago-2026 prometía 3 funciones de IA en Revit. Al ir a documentar el paso a paso que ese mismo post prometía, una no existía, otra era media verdad y la tercera no funcionaba como se decía — y Autodesk afirma textualmente que hasta Revit 2026 no hay funciones de IA. Vendemos formación técnica: **la credibilidad es el producto**, y cualquier ingeniero desmonta eso en los comentarios. Ver `guiones/blog-ia-revit-paso-a-paso.md`.
1. **Nunca inventar métricas ni transcripciones.** Lo que no venga del scraper se marca `s/d`. Una matriz con huecos honestos vale más que una llena de suposiciones.
2. **Solo cuentas y videos públicos.**
3. **Toda corrida de Apify lleva topes**: `maxItems` (30-50 por cuenta en la recolección inicial, 15 en la rutina semanal) y `maxTotalChargeUsd` ($1 inicial, $0.50 semanal). El costo estimado se muestra y se espera OK antes de correr.
4. **`fuentes/` no se edita nunca** — solo se lee. Es el dato crudo.
5. La simulación de guiones es una **estimación sobre patrones pasados, no una predicción**. Los guiones de estimación baja también se publican.

## Estructura

```
fuentes/         → datos crudos de Apify, un archivo por red
transcripciones/ → texto de cada video, un archivo por pieza (red-fecha-título)
matriz/          → matriz-contenido-viral.md y patrones-de-viralidad.md
guiones/         → guiones nuevos, cada uno con su simulación al final
```

## Orden de trabajo

`recolectar → matriz → simular → rutina semanal`

Cada paso lee el archivo que dejó el anterior: `fuentes/` + `transcripciones/` alimentan `matriz/`; `matriz/` alimenta `guiones/`; la rutina semanal actualiza los cuatro.

## Actores por red

| Red | Actor | Precio (jul 2026, plan free) | Trae transcripción |
|---|---|---|---|
| Instagram Reels | `apify/instagram-reel-scraper` | desde ~$1.00 / 1,000 | Sí |
| Instagram Posts | `apify/instagram-scraper` | desde ~$2.70 / 1,000 | No |
| TikTok | `clockworks/tiktok-scraper` | desde ~$1.70 / 1,000 | Sí (activar opción) |
| YouTube | `streamers/youtube-scraper` | desde ~$2.40 / 1,000 | Sí (subtítulos) |
| Facebook | **sin confirmar** | — | — |

Facebook no está en la guía original (que cubre IG/TikTok/YouTube/X) porque no siempre tiene un actor estable de scraping público — se busca y se confirma precio/actor en la primera corrida real, antes de gastar crédito.

## Estado de ejecución

Ver `STATUS.md` en esta misma carpeta — la recolección real todavía no corrió.

## Rutina semanal (se activa al decir "rutina semanal")

1. **Re-recolecta**: solo lo nuevo, `maxItems` 15/cuenta, `maxTotalChargeUsd` $0.50/corrida. Muestra costo antes de correr. Guarda sin borrar lo anterior.
2. **Actualiza la matriz**: agrega piezas nuevas, revisa si algún patrón de `patrones-de-viralidad.md` cambió. Avisa primero si algo que funcionaba dejó de funcionar (o al revés).
3. **Mis números**: compara las últimas publicaciones de design_modeling_dg contra su mediana. ¿Qué guion rindió mejor? ¿Coincidió con la simulación? Anota acierto/fallo al final del guion correspondiente en `guiones/`.
4. **Calendario**: propone la semana — guion (nuevo o pendiente), red, y por qué en ese orden. Día/hora solo si hay patrón real en la matriz.
5. **Resumen**: 5 líneas — qué aprendimos, qué toca publicar, crédito de Apify gastado en el mes.
