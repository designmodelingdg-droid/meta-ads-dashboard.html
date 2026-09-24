# Montar el Tutor IA del Diplomado en GoHighLevel

Para **Ester y Aylin**. Es el mismo montaje que hicieron con el tutor del
Acero: un **Custom Block con botón**, sin pegar código. El tutor ya está en
línea y responde con las clases del Diplomado.

La dirección de este tutor es **otra**, no la del Acero:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-diplomado-estructuras/
```

---

## Dónde va, y dónde NO

Va **solo en el curso del Diplomado**:

- Diplomado Universitario Internacional BIM: Edificaciones de Acero Estructural
  y Hormigón Armado

**No va** en los cursos de la Especialización en Acero (esos llevan el botón
del tutor del Acero, que ya está puesto), ni en el Máster, ni en «Módulo 1 del
Diplomado Universitario Internacional BIM», que es un lead magnet. Este tutor
solo conoce las clases del Diplomado.

---

## Los pasos

1. Abrir el curso del Diplomado → **Editar** → en el selector **Páginas**
   elegir **Producto** (la portada del curso).
2. Añadir un **Custom Block** en el cuerpo, arriba del todo o justo debajo del
   video de presentación.
3. Rellenar los campos del bloque **exactamente así**:

| Campo del bloque | Qué poner |
|---|---|
| Imagen | `tarjeta-tutor.png` de **esta** carpeta (dice «de tu Diplomado»; no usar la del Acero) |
| Heading | `Tutor IA · pregúntale a tus clases` |
| Contenido | `Resuelve tus dudas con las clases de tu Diplomado. Te dice en qué lección y en qué minuto está la respuesta — y si algo no está en el material, te lo dice en vez de inventarlo.` |
| Button Text | `Abrir el Tutor IA` |
| Tipo de botón | Solid Button |
| Relleno del botón | `#0E2438` |
| Borde del botón | `#E8A04A` |
| Button Text (color) | `#FFFFFF` |
| Ir a la URL | la dirección de arriba, pegada completa |

4. **Guardar cambios.**

Opcional: el mismo bloque en **Páginas → Lección**, para tenerlo a mano
mientras se estudia.

---

## La burbuja dentro del curso (24-sep)

Además del botón, el tutor puede ir como una **burbuja abajo a la derecha** en
todas las páginas del Diplomado: el alumno la toca y el tutor se abre en un
panel encima de la clase, sin salir de ella (en el móvil ocupa la pantalla).

Se pega **una sola línea**, y solo en el Diplomado:

1. **Suscripciones → Cursos → Productos →** «Diplomado Universitario
   Internacional BIM: Edificaciones de Acero Estructural y Hormigón Armado»
   **→ Configuración** (menú de la izquierda).
2. Bajar hasta el final y abrir **«Avanzada»**.
3. En la pestaña **«Javascript personalizado»** pegar exactamente esto (sin
   etiquetas `<script>`):

```
(function(){var s=document.createElement('script');s.src='https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-diplomado-estructuras/burbuja.js';s.defer=true;document.head.appendChild(s);})();
```

4. **Guardar**, abrir el curso como alumno y comprobar que sale la burbuja
   «IA» abajo a la derecha.

**No pegarla en el Portal del cliente** (Configuración → Creación de marca →
Avanzado): eso la cargaría en todos los cursos. Si algún día hiciera falta
ponerla ahí, se pega esta otra versión, que solo la muestra en las páginas del
Diplomado:

```
window.DMA_TUTOR_SOLO_DIPLOMADO=true;(function(){var s=document.createElement('script');s.src='https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/tutor-diplomado-estructuras/burbuja.js';s.defer=true;document.head.appendChild(s);})();
```

El botón de la portada puede quedarse: son dos entradas al mismo tutor.

**Para la Especialización en Acero** es el mismo archivo con `?programa=acero`
al final de la dirección: ver `tutor-acero/MONTAJE-GHL.md`. Sin ese final,
abre el tutor del Diplomado.

Si la burbuja no aparece: el campo de «Javascript personalizado» del producto
no se pudo inspeccionar por dentro, así que cabe que no acepte JavaScript. En
ese caso, probar la misma línea envuelta en `<script>…</script>` en
**«Código de seguimiento del encabezado»** del mismo producto.

---

## Comprobar antes de darlo por hecho

Abrir el curso **como alumno** y pulsar el botón. Preguntar, por ejemplo:

> ¿Cómo diseño una zapata combinada?

Tiene que responder y terminar citando el módulo, la lección y el minuto:

> **FUENTES:** M6 Cimentaciones · Lección 22 · Prediseño de Zapatas Combinadas en RSA (Pt. 2) · min …

Si en vez de responder dice «todavía se está preparando», avisar a Dayana: la
página comprueba primero que el servidor tenga cargado el Diplomado y, si no,
no deja preguntar.

---

## Lo que hay que saber cuando pregunten

**Tiene cargados los módulos 2 a 9.** El Módulo 1 (iniciación en Revit) son
videos subidos directo a GHL, sin la transcripción que usa el tutor. Si un
alumno pregunta por algo de ese módulo, el tutor le dice que ese módulo aún no
lo tiene. Del Módulo 2 faltan 4 lecciones: las 3 de la Fase 7 (están en otra
cuenta de Vimeo) y una con subtítulos solo en inglés.

**No hay que activar a nadie.** Quien entra al área de miembros ya está
identificado por GoHighLevel.

**Nunca da cifras de norma ni precios.** Remite a la norma vigente en vez de
dictar el número.

**Topes al día.** 20 preguntas por navegador. El Diplomado tiene su propio tope
general, separado del Acero: un día con muchas preguntas en uno no deja sin
tutor al otro.
