# Verificar mirándola

Una landing no tiene un solo estado. Tiene tantos como posiciones de scroll, y los
fallos viven entre las dos que miraste.

Esto no es «debería funcionar». Es abrirla, fotografiarla y **mirar las fotos**.

---

## El script

```bash
node .claude/skills/landing-craft/scripts/mirar.mjs <archivo.html | URL>
```

Hace cuatro cosas y deja las capturas en `lab/`:

1. Fotografía la página completa a **1200 px** y a **390 px**.
2. Recorre el scroll en seis posiciones en cada ancho.
3. Mide el **contraste real** de cada bloque de texto sobre lo que tiene detrás,
   ya compuesto — no el que dice el CSS.
4. Lista los enlaces y los botones, y avisa de los que se quedaron en `#` o vacíos.

Sale con código distinto de cero si encuentra contraste por debajo del mínimo o un
enlace muerto. Eso bloquea la entrega.

---

## Lo que el script NO puede decirte

Y es la mitad del trabajo:

- Si la jerarquía se entiende.
- Si la foto está cortada por un sitio feo.
- Si el titular respira o está apelmazado contra el borde.
- Si el pico es de verdad el momento más grande de la página.
- Si la página significa algo.

Por eso el paso siguiente es obligatorio: **abre las capturas y míralas.** Una por
una. La de 390 px con más atención que la de 1200, porque es por donde entra la
mayoría.

Y encima de eso, la prueba del entrecerrado (ver `oficio.md`): difumina hasta
perder el detalle y comprueba que todavía distingues el elemento principal, el
secundario y los grupos.

---

## Lo que hay que mirar en la de 390 px

Es donde se rompen las páginas de DMA, y siempre por lo mismo:

- **El titular del hero partido en cinco o seis líneas.** Un tamaño que en
  escritorio es correcto, a 390 px no lo es. Baja un escalón dentro de la media
  query.
- **Padding de escritorio heredado.** 8 rem arriba y abajo en un teléfono es scroll
  que el visitante paga sin recibir nada.
- **Tablas y rejillas que desbordan a lo ancho.** El cuerpo de la página no debe
  moverse en horizontal nunca. Si algo tiene que ser más ancho (una tabla, un
  diagrama), va dentro de su propio contenedor con scroll.
- **El botón del formulario partido en dos líneas.**
- **Las imágenes del marquee de avales**, que a ese ancho se amontonan.

---

## El caso GHL

Nuestras landings se pegan en **GHL → Sites → Custom Code container**, y eso añade
dos comprobaciones que no existen en un sitio propio:

1. **GHL pone `<html>`, `<head>` y `<body>`.** El HTML que entregamos no los lleva.
   Si los lleva, GHL los anida y el resultado es impredecible.
2. **Comprobar en la página publicada, no solo en el archivo local.** GHL inyecta
   sus propios estilos y su propio contenedor. Una página que se ve perfecta en
   local puede heredar un `max-width` o un `padding` de GHL. Se abre la URL real
   antes de dar nada por terminado.

Y una tercera que no es de maquetación: **el formulario embebido tiene que enviar
de verdad**. Se hace un envío de prueba, se comprueba que el contacto llega al CRM
con sus etiquetas, y después se borra el contacto de prueba.

---

## Qué se reporta

Siempre las dos listas, separadas:

- **Lo que verifiqué**, con el número concreto (contraste medido, anchos
  fotografiados, enlaces comprobados, envío de formulario probado).
- **Lo que no pude verificar**, y por qué.

Un reporte que solo trae la primera lista no es un reporte, es una promesa.
