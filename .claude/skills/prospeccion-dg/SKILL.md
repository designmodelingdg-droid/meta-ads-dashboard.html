---
name: prospeccion-dg
description: >
  Saca clientes B2B para Design Modeling DG (la consultoría) con los scrapers
  de Apify: define el cliente ideal, prueba con 10, saca la lista, la enriquece
  sin inventar, la califica y escribe los guiones de llamada y de WhatsApp.

  Usa este skill cuando Dayana diga: "prospeccion-dg", "busquemos clientes para
  la consultoría", "saca una lista de constructoras", "prospección con Apify",
  "clientes para DG", o cuando pida contactos B2B que no vengan de la pauta ni
  del contenido.

  NO es para la Academy. La Academy vende cursos a personas por anuncios y
  contenido; el contacto en frío no encaja ahí.
---

# Prospección B2B para Design Modeling DG

## Paso 0 · Antes de nada: esto no es el negocio de siempre

DMA capta hacia dentro — anuncio, formulario, closer; o contenido, comentario,
recurso gratuito. **Esto es lo contrario: salir a buscar a quien no te conoce.**
Es un motor aparte, no una mejora del que ya hay, y trae riesgos que el de
siempre no tiene.

**A quién sí:** constructoras, estudios de arquitectura y oficinas de
ingeniería que necesitan consultoría BIM. Eso es **Design Modeling DG**.

**A quién no:** particulares que quieren formarse. Esos ya llegan por la pauta
y por el contenido, y son de la **Academy**. Llamar en frío a un ingeniero para
ofrecerle un curso es otra cosa, y no es lo que hace esta cuenta.

## Paso 1 · Las tres reglas que no se rompen, y por qué son de DMA

### 1 · Se contacta por TELÉFONO, no por correo

`info@dgdesignmodeling.com` está en verde, y lo está **porque solo le escribe a
quien pidió algo**: quien descargó un recurso, quien llenó un formulario, los
alumnos. El correo en frío es el tráfico contrario, y es lo que genera quejas y
rebotes.

**Ese verde no protege: es lo que está en juego.** Si se cae, no se pierde la
prospección — se pierde que le lleguen los correos a quien ya pagó.

Y además el teléfono rinde más. De 1.000 negocios de Google Maps, **~950 traen
teléfono** (viene en el mapa) y **~350 traen correo** (hay que entrar a su web a
buscarlo). Triplica la base contactable y gasta menos crédito.

**El número de envío es un WhatsApp Business aparte**, nunca el personal de
nadie. Volumen bajo al principio, subiendo despacio. Y **nada de herramientas de
envío masivo ni APIs no oficiales**: ese es el disparador de bloqueo más claro.

A los de grado A se les **llama**. A los B se les escribe.

### 2 · Los leads en frío NO entran al GoHighLevel de siempre

La matriz mide el CRM: `ghl_datos.py` y `ghl_conversaciones.py` llenan
`fuentes/ghl/`, y de ahí salen el coste por lead, el cruce pauta→ventas y el
retorno real.

**Meter ahí trescientos contactos raspados de Google Maps destruye esas
métricas.** El CPL deja de significar nada porque el denominador se llena de
gente que nunca pidió nada. Y el cierre de mes, que ya costó arreglar una vez,
vuelve a mentir.

Si estos leads acaban en GHL, van con **etiqueta propia y en un pipeline
separado**, y quien lea las métricas tiene que poder excluirlos. Mientras eso
no esté montado, se quedan en su CSV.

### 3 · El crédito de Apify ya está comprometido

Apify da **$5 al mes gratis**, y la matriz ya se los está gastando sola:
`refresh-matriz.yml` corre **todos los lunes a las 13:00 UTC** y llama al
scraper de Instagram.

Así que el presupuesto de prospección **no es $5: es lo que sobre**. Antes de
cada corrida se mira lo gastado del mes.

Y la regla del repositorio (`matriz-viral/CLAUDE.md`, punto 3) exige que toda
corrida lleve `maxItems` **y** `maxTotalChargeUsd`. Aquí también.

> Ya se gastaron $2 una vez por saltarse esto, para traer 96 piezas sin una
> sola vista. El aviso estaba escrito dentro del propio script.

## Paso 2 · El playbook, en orden

Ocho pasos. Cada uno deja un archivo que el siguiente necesita. **Se espera la
respuesta antes del siguiente**, no se pegan todos de golpe.

| # | Paso | Qué deja |
|---|---|---|
| 1 | La entrevista | `perfil-cliente.md` |
| 2 | Prueba de 10 | `leads/muestra.csv` |
| 3 | Los 50, con tope | `leads/<fecha>.csv` |
| 4 | Enriquecer sin inventar | las columnas `origen_telefono` y `mejor_hora` |
| 5 | Calificar A/B/C | el CSV ordenado + `descartados.csv` |
| 6 | Guiones: llamada (A) y WhatsApp (B) | `contactos/<fecha>.csv` |
| 7 | El seguimiento (uno solo) | `contactos/seguimientos.csv` |
| 8 | Qué funcionó | `perfil-cliente.md` corregido |

Los prompts completos están en `prompts/playbook.md`.

### Lo que hace que sirvan, y que es lo mismo que ya rige en la matriz

- **Nunca inventar un dato.** Lo que no se encontró se queda en «sin dato». Es
  la regla 1 de `matriz-viral/CLAUDE.md` aplicada a otra cosa.
- **Nada de deducir un número por el prefijo de la zona.** Un teléfono que no
  se encontró se queda en «sin dato».
- **Probar con 10 antes de gastar en 50.** Si menos de 7 de 10 califican, se
  corrige la búsqueda, no se sigue.
- **Sin dato real de ese negocio, no hay contacto.** Se marca «sin ángulo» y
  se investiga antes de llamar.

## Paso 3 · Las cuentas honestas, antes de ilusionarse

De **1.000** negocios raspados salen ~950 con teléfono. No todos contestan, no
todos son el que decide, y muchos números son del mostrador y no del dueño.

**Nadie te puede dar la tasa de respuesta de tu nicho por teléfono sin haberlo
probado**, así que el paso 8 existe para medirla y el paso 2 para no gastar
antes de saber si la lista sirve.

Lo que sí está medido es el coste: **50 negocios de Google Maps salen por unos
30 centavos**. Sin pedir correos es aún más barato, porque no hay que rastrear
webs.

Y lo que la experiencia del correo sí enseña: **nueve conversaciones reales de
mil contactos es un buen mes, no un fracaso.** El error es esperar mil clientes.

## Lo que este skill NO monta, y no es un olvido

**El agente automático con horario no se monta desde aquí.** La guía original
lo construye con una tarea programada (`launchd`) en el Mac de Dayana. Esta
sesión corre en un contenedor remoto que se recicla: cualquier cosa que
programe aquí muere con la sesión.

**El MCP de Apify tampoco se conecta desde aquí.** `claude mcp add` configura
la instalación local, y la autorización es un paso de navegador. Los pasos
exactos, para hacerlos ella en su Mac, están en `prompts/montaje-local.md`.

**Y antes de automatizar, conviene correr el playbook a mano un par de veces.**
Automatizar algo que todavía no se domina solo consigue basura más rápido — lo
dice la propia guía y es cierto.

## De dónde sale esto

De la guía de la bóveda de **tododeia** sobre Apify (actualizada a julio 2026).
Los prompts se conservan y se les añaden las tres reglas de arriba, que son de
DMA y la guía no podía conocer: el canal —teléfono en vez del correo que
sostiene el CRM—, el GHL que la matriz mide, y el crédito de Apify que ya se
está gastando solo los lunes.
