# Encargo para browser-harness — lo que queda en GHL

**Cuatro cosas, en este orden.** El orden importa: la primera es la única que
bloquea mandar tráfico, y la última es la que se vuelve cara si se deja para
después.

Va después de que termine el workflow de Instagram. No hace falta parar nada.

---

## No hace falta tener el repositorio en el Mac

El `git pull` falló porque la sesión del Mac no está parada dentro del
repositorio — y resulta que **no lo necesita**. El archivo del hub está
publicado y se puede pedir directo:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/recursos/ghl-recursos.html
```

Comprobado: 24.206 bytes, con la tarjeta nueva dentro, idéntico byte a byte al
del repositorio. Hay una segunda copia igual de fresca por si esa fallara:

```
https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/claude/remote-control-setup-GUe3f/recursos/ghl-recursos.html
```

> Si algún día se quiere el repositorio en el Mac de todas formas, primero hay
> que ver si ya está en alguna parte:
> ```bash
> find ~ -maxdepth 4 -type d -name "meta-ads-dashboard.html" 2>/dev/null
> ```
> Y si no aparece, se clona. Pero para este encargo no hace falta.

---

## Para pegar tal cual

```text
Tengo Chrome abierto con --remote-debugging-port=9222 y la sesión de
GoHighLevel iniciada (subcuenta Design Modeling). Cuatro tareas, en este
orden. Después de cada una, verifica como te digo y dime el resultado antes de
pasar a la siguiente.


TAREA 1 — El formulario de ACERO manda a la página de gracias equivocada.

El formulario nativo embebido en la landing de ACERO es jgZBVSDHAgvfjsJHVFB8.
Su configuración tiene actionType "redirigir" y redirectUrl apuntando a
https://funnel.dgdesignmodeling.com/acceso-gratis-curso-introductorio-bim-gracias

Quien llena el formulario de ACERO aterriza en la gracias del Curso
Introductorio BIM y nunca recibe la guía ni el verificador.

DUPLICA ese formulario. No le cambies el redirect al original: puede estar en
uso en algo que no se ve desde fuera, y duplicar nunca rompe nada. Al
duplicado ponle de nombre «Lead Magnet ACERO — 5 verificaciones» y su redirect
a la página de gracias de acero:
https://funnel.dgdesignmodeling.com/acceso-gratis-verificacion-acero-gracias

Después cambia la landing de ACERO para que use el duplicado en vez del
original.

VERIFICA: llena el formulario de verdad, una vez, con un correo de prueba.
Dime a qué página caes. Si no caes en la de gracias de acero, no sigas: eso es
lo que había que arreglar.


TAREA 2 — Pegar el hub de recursos actualizado.

Abre Sites → la página /recursos → el elemento Custom Code. Reemplaza TODO su
contenido por lo que devuelve esta dirección:

https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/recursos/ghl-recursos.html

Son 24.206 bytes. Descárgala y pega el contenido completo, tal cual, sin
recortar ni reindentar. Guarda y publica.

VERIFICA: no me digas que quedó porque el botón se puso verde. Pide
https://funnel.dgdesignmodeling.com/recursos por HTTP y confírmame que trae
estas tres cosas dentro:
  acceso-gratis-verificacion-acero-form
  Las 5 verificaciones en acero
  6a8decb8e25296bd1b4a357d


TAREA 3 — Los títulos dicen «Calculadora de Zapatas».

Las tres páginas conservan el título del clon:
  <title>Calculadora de Zapatas Aisladas Gratis | Design Modeling Academy

Eso es lo que se ve en la pestaña del navegador y lo que aparece cuando
alguien comparte el enlace por WhatsApp. Se corrige en los ajustes de cada
página del funnel (SEO / Page Title), no en el HTML pegado.

Pon:
  landing de ACERO → Las 5 verificaciones en acero | Design Modeling Academy
  gracias de ACERO → Tu acceso está listo | Design Modeling Academy

La de zapatas déjala como está: esa sí es la calculadora de zapatas.

VERIFICA: pide las dos páginas por HTTP y léeme el <title> de cada una.


TAREA 4 — Renombrar la página de gracias.

Hoy se llama acceso-gratis-verificacion-acero-gracias pero sirve
contenido de acero. Renómbrala a:
  acceso-gratis-verificacion-acero-gracias

Hazla AL FINAL y solo si las tres anteriores quedaron. Renombrar rompe todo lo
que apunte a la ruta vieja, y GHL no deja redirección del path anterior.
Ahora es barato porque todavía no hay nadie usándolo; en una semana ya no.

Después de renombrar hay que actualizar el redirect del formulario duplicado
de la TAREA 1, que apunta a la ruta vieja. Ese es el orden y no al revés.

VERIFICA: la ruta nueva responde 200, y llena el formulario otra vez para
confirmar que cae ahí.


REGLAS PARA LAS CUATRO

- No borres nada. Ni formularios, ni páginas, ni contactos. Si algo parece que
  sobra, dilo y no lo toques.
- Un clic dado no es un cambio guardado, y un cambio guardado no es un cambio
  publicado. La verificación es pedir la página por HTTP, no mirar el editor.
- Si algo no sale, dilo con lo que viste. Un «no pude» con evidencia vale más
  que un «listo» que no es.
- Avísame el nombre exacto que quede en cada página. Un renombrado sin aviso
  dejó dos lead magnets en 404 durante días.
```

---

## Lo que sigue después, y no es de navegador

Cuando la TAREA 4 esté hecha, avísame la ruta final de la página de gracias.
Hay que actualizarla en `eficiencia-acero/gracias-agenda.html` y volver a
publicar, o el enlace del repositorio queda apuntando al nombre viejo.

Y queda el **Paso 3, la membresía**, que es lo que hace que este recurso
entregue igual que los demás. Antes de montarla conviene leer por dentro el
workflow «Calculadora Zapatas - Acceso Membresía» — está en
`scripts/navegador/GUIA-MAPA-FLUJOS-MAC.md`, es el primero de la lista.
