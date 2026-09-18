# Lo que hay que hacer en tu Mac — no se puede desde aquí

Esta sesión corre en un contenedor remoto que se recicla. Lo de abajo configura
**tu** ordenador, así que lo tienes que correr tú.

## 1 · Conectar el MCP de Apify

Cuenta gratis en apify.com (no pide tarjeta, da $5 de crédito al mes). Luego,
en la terminal:

```bash
mkdir prospeccion-dg && cd prospeccion-dg
claude mcp add --transport http apify https://mcp.apify.com
claude
```

Y dentro de Claude Code:

```
/mcp
```

Eso abre la autorización en el navegador. **Es un paso que necesita a una
persona**: no se puede hacer desde una sesión automática.

> Si prefieres no autorizar por navegador, el token va en el propio comando:
> `claude mcp add --transport http apify https://mcp.apify.com --header "Authorization: Bearer TU_TOKEN"`.
> Sale de Apify → Settings → API & Integrations.
> **Ese token no me lo pases por el chat.**

## 2 · Antes de la primera corrida, mira cuánto crédito queda

En apify.com, arriba a la derecha, el consumo del mes.

**No empieces con $5.** La matriz gasta de esa misma cuenta todos los lunes a
las 13:00 UTC (`refresh-matriz.yml`, el scraper de Instagram). Tu presupuesto
de prospección es lo que sobre de ahí.

## 3 · El dominio de correo, antes de escribir a nadie

Esto es lo que más caro sale si se hace mal, y lo explica el SKILL: **no uses
`dgdesignmodeling.com`**. Ese dominio manda los correos de los alumnos.

Hace falta un dominio aparte, con SPF, DKIM y DMARC, y calentarlo durante
semanas empezando por cinco o diez correos al día.

**Hasta que eso esté, el playbook se corre igual** — sacar la lista,
enriquecerla y calificarla no manda ningún correo. Lo que se para es el paso 6
en adelante.

## 4 · El agente con horario — solo cuando lo anterior funcione

La guía monta un agente en una carpeta que sale a buscar solo, con `launchd`.
Dos avisos antes de ir por ahí:

- **No corre con el ordenador apagado.** La tarea programada necesita tu Mac
  encendido.
- **Automatizar lo que todavía no dominas solo consigue basura más rápido.**
  Corre el playbook a mano un par de veces primero; lo que aprendas ahí es lo
  que hace que el agente no busque a ciegas.

Cuando llegue el momento, el prompt maestro de la guía lo construye. Pídemelo
y lo adapto a las reglas de DMA, igual que el playbook.
