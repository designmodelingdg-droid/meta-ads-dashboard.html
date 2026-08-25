# browser-harness — el otro camino al navegador

> Comprobado contra el repositorio oficial el **25-ago-2026**: versión 0.1.9,
> licencia MIT, `Development Status :: 3 - Alpha`.
> <https://github.com/browser-use/browser-harness>

## Qué es, y en qué se diferencia de lo que ya tenemos

Se conecta por CDP al **Chrome que ya tienes abierto**, en tu computadora. No
lanza un navegador nuevo ni necesita credenciales: usa las sesiones que ya
tienes iniciadas.

| | `scripts/navegador/` (Playwright) | browser-harness |
|---|---|---|
| Dónde corre | servidor de GitHub Actions | tu máquina, tu Chrome |
| Cómo entra | secreto `GHL_STORAGE_STATE` | ya estás dentro |
| Corre sin ti | **sí**, en horario | no |
| Rastro en el repo | sí, JSON commiteado | no |
| Interfaces difíciles | frágil | **es para lo que está hecho** |

**No compiten.** Playwright + Actions es para lo que tiene que pasar sin nadie
delante — el mapa de flujos, publicar un borrador, el chequeo de enlaces cada
semana, con su rastro en git. browser-harness es para lo difícil y puntual,
contigo mirando.

---

## El riesgo, dicho de frente

Un agente conectado a tu Chrome de diario ve **todas** tus pestañas con sesión
iniciada: el banco, el correo, el CRM, todo. No hay forma de darle solo GHL.

El archivo `GHL_STORAGE_STATE` que usa el otro camino abre GHL y nada más. Esa
diferencia es real y va en la dirección contraria a la que uno esperaría: la
herramienta más cómoda es la que más alcance concede.

**Por eso: un perfil de Chrome aparte.** Antes de conectar nada:

1. Chrome → menú de perfil → **Agregar** → llámalo `GHL-agente`.
2. En ese perfil inicia sesión **solo** en GoHighLevel. Nada más.
3. Conecta el agente a ese perfil, no al de siempre.

Cuesta dos minutos y es la diferencia entre darle una llave y darle el llavero.

---

## Instalación

El propio proyecto da un texto para pegar en Claude Code. Se pega **en el
Claude Code de tu computadora**, no en una sesión remota — la sesión remota
corre en un contenedor sin tu navegador:

```text
Install or upgrade browser-harness to the latest stable version with uv using
Python 3.12, register the skill from `browser-harness skill`, and connect it to
my browser. Ask whether I want local browser recordings enabled; default to no
and preserve my existing preference on upgrades. Follow
https://github.com/browser-use/browser-harness/blob/main/install.md if setup or
connection fails.
```

Lo que va a pasar, para que no te agarre por sorpresa:

- Instala con `uv` (no con pip). Si no tienes `uv`, lo pedirá.
- Te va a abrir `chrome://inspect/#remote-debugging` y pedirte que marques
  **«Allow remote debugging for this browser instance»**. Esa casilla es
  manual a propósito: es el permiso, y el agente no puede dárselo solo.
- En macOS puede aparecer una ventana de permiso por conexión; se resuelve con
  `browser-harness mac-approve`, que necesita permiso de Accesibilidad para la
  app desde la que lanzas la terminal.
- Va a preguntar por las **grabaciones locales** (capturas y trazas guardadas
  en tu disco). **Di que no.** Esas grabaciones pueden incluir contenido de
  pantalla del CRM, y no las necesitamos para nada de lo que hacemos.

Para Chrome local **no hace falta API key ni cuenta de Browser Use**. Lo de la
nube es opcional y es otro producto.

---

## Para qué lo usaríamos aquí

Lo que la API de GHL no deja hacer **y** Playwright a ciegas hace mal:

- **Pegar HTML en un elemento Custom Code.** El constructor de GHL mete el
  lienzo y el editor de código en marcos anidados. browser-harness trae guías
  propias para `iframes`, `cross-origin-iframes` y `shadow-dom` — es
  exactamente su caso de uso.
- **Editar los pasos de un workflow**, que la API ni siquiera deja leer.
- **Cambiar los enlaces dentro de los bots de DM.**

Ejemplo de encargo, con la verificación incluida — que es la parte que no se
debe omitir nunca:

```text
En GoHighLevel (subcuenta Design Modeling), abre Sites → la página /recursos →
el elemento Custom Code. Reemplaza TODO su contenido por el archivo
recursos/ghl-recursos.html de este repositorio. Guarda y publica.

Después NO me digas que quedó porque el botón se puso verde: pide
https://funnel.dgdesignmodeling.com/recursos por HTTP y confírmame que trae
acceso-gratis-test-nivel-bim-form y acceso-gratis-calculadora-zapatas-form, y
que ya no aparece ni /test-nivel-bim" ni /calculadora-zapatas".
```

Esa última frase no es un detalle de estilo. En julio el bot de ZAPATA marcaba
los pasos en verde y el DM no salía; se perdieron unos 35 leads antes de que
alguien abriera una conversación a comprobarlo. **Un clic dado no es un cambio
guardado, y un cambio guardado no es un cambio publicado.**

---

## Lo que sigue siendo mala idea

Lo mismo que en el otro camino, y por las mismas razones:

- **Nada de borrar.** Leer mal no rompe nada; borrar mal en un CRM con 1.200
  oportunidades sí.
- **Lo que la API sí sabe hacer, se hace por API.** Es más rápido y no se
  rompe cuando mueven un botón.
- **No automatizar lo que se hace una vez.** Que ahora exista el martillo no
  obliga a usarlo en todo.

Y uno propio de esta herramienta: **está en alfa.** Versión 0.1.9. Sirve para
trabajo puntual con alguien mirando, no para ponerlo en el camino crítico de
algo que tenga que funcionar solo.
