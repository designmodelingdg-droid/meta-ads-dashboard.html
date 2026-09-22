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

## 3 · El número de WhatsApp, antes de escribirle a nadie

**No uses tu WhatsApp personal ni el de Gabriel.** Si bloquean ese número, se
lleva por delante el teléfono con el que hablas con alumnos y clientes.

Hace falta un **WhatsApp Business aparte**, con su propio número. Y tres reglas:

- **Volumen bajo al principio**, subiendo despacio. Un número nuevo mandando
  decenas de mensajes el primer día es la forma conocida de que lo bloqueen.
- **Nada de herramientas de envío masivo** ni APIs no oficiales. Ese es el
  disparador de bloqueo más claro que hay. Se manda a mano, o con la app oficial
  de WhatsApp Business.
- **A los de grado A se les llama.** Una llamada de treinta segundos vale más
  que veinte mensajes, y no gasta número.

**Hasta que ese número exista, el playbook se corre igual** — definir el
cliente, sacar la lista, enriquecerla y calificarla no manda nada. Lo que se
para es el paso 6.

## 3 bis · El correo, desde el dominio de siempre

Decidido el 20-sep: **sí se usa `dgdesignmodeling.com`**, después de comprobar
que está en buen estado. Con dos condiciones que no son opcionales:

- **Solo a direcciones de `confianza: alta`** — las que están en el sitio oficial
  del negocio. Nunca a `info@` ni `contacto@`: muchas están abandonadas y algunas
  son trampas de spam.
- **Se miden los rebotes de la primera tanda.** Si pasan del **2 %**, se para el
  canal de correo hasta arreglar el enriquecimiento. Por encima de ahí Google
  castiga la reputación del dominio — y ese dominio manda los correos de los
  alumnos y las secuencias de los recursos.

El volumen sale bajo solo: de cada mil negocios raspados, los de confianza alta
son unos 50-80.

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
