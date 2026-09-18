---
name: prospeccion-dg
description: >
  Saca clientes B2B para Design Modeling DG (la consultoría) con los scrapers
  de Apify: define el cliente ideal, prueba con 10, saca la lista, la enriquece
  sin inventar, la califica y escribe los correos de primer contacto.

  Usa este skill cuando Dayana diga: "prospeccion-dg", "busquemos clientes para
  la consultoría", "saca una lista de constructoras", "prospección con Apify",
  "clientes para DG", o cuando pida contactos B2B que no vengan de la pauta ni
  del contenido.

  NO es para la Academy. La Academy vende cursos a personas por anuncios y
  contenido; el correo en frío no encaja ahí y quemaría el dominio que ya usa
  el CRM.
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
y por el contenido, y son de la **Academy**. Un correo en frío a un ingeniero
que no te conoce, ofreciéndole un curso, es spam.

## Paso 1 · Las tres reglas que no se rompen, y por qué son de DMA

### 1 · El dominio de los correos NUNCA es `dgdesignmodeling.com`

Ese dominio manda hoy los correos que de verdad importan: las secuencias de
los recursos gratuitos, los del CRM, los de los alumnos matriculados.

**Si se manda correo en frío desde ahí y Google lo castiga, no se cae la
prospección: se caen los correos a los alumnos que ya pagaron.** El daño no es
perder una campaña, es perder la comunicación con quien ya compró.

Dominio aparte, solo para esto. Con SPF, DKIM y DMARC. Empezando en cinco o
diez correos al día y subiendo durante semanas. El techo sano son 20-50 por
buzón al día, muy por debajo del límite técnico.

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
| 4 | Enriquecer sin inventar | las columnas `origen_correo` y `confianza` |
| 5 | Calificar A/B/C | el CSV ordenado + `descartados.csv` |
| 6 | Correos de primer contacto | `correos/<fecha>.csv` |
| 7 | Los dos seguimientos | `correos/seguimientos.csv` |
| 8 | Qué funcionó | `perfil-cliente.md` corregido |

Los prompts completos están en `prompts/playbook.md`.

### Lo que hace que sirvan, y que es lo mismo que ya rige en la matriz

- **Nunca inventar un dato.** Lo que no se encontró se queda en «sin dato». Es
  la regla 1 de `matriz-viral/CLAUDE.md` aplicada a otra cosa.
- **Nada de correos por patrón** (`nombre.apellido@dominio`). Eso quema
  dominios y es justo lo que el punto 1 intenta evitar.
- **Probar con 10 antes de gastar en 50.** Si menos de 7 de 10 califican, se
  corrige la búsqueda, no se sigue.
- **Sin dato real de ese negocio, no hay correo.** Se marca «sin ángulo» y se
  deja para llamada.

## Paso 3 · Las cuentas honestas, antes de ilusionarse

De **mil** negocios raspados salen unos 300-400 con correo — Google Maps no
guarda correos, los actores entran al sitio del negocio a buscarlos, así que
un negocio sin web se queda sin correo. Tras limpiar rebotes quedan ~300
enviables. Con una tasa de respuesta buena del 3 %, son **nueve
conversaciones**.

**Nueve conversaciones reales de mil negocios es un buen mes.** El error es
esperar mil clientes.

Y el coste: 50 negocios de Google Maps con contacto salen por unos **30
centavos**. LinkedIn e Instagram se comen el crédito bastante más rápido.

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
DMA y la guía no podía conocer: el dominio compartido con el CRM, el GHL que
la matriz mide, y el crédito de Apify que ya se está gastando solo los lunes.
