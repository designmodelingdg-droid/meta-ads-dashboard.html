# Los ocho formularios mandaban al webinar de febrero de 2025

> **CERRADO el 25-ago-2026**, el mismo día. Comprobado de forma independiente
> con `scripts/formularios_destino.py`, que lee la página viva y no el estado
> del editor: **los ocho mandan a su propia página de gracias**, las ocho
> responden 200, y no queda ni una regla condicional.
>
> Se comprobó además que el arreglo **no se llevó nada por delante** — se hizo
> parcheando el cuerpo del guardado, que es un método que puede perder campos.
> Los ocho conservan nombre, correo, teléfono y **el campo de perfil con sus
> cuatro opciones**.
>
> Lo que queda es la única comprobación que no se puede hacer desde fuera:
> llenar un formulario de verdad y ver dónde cae.

**Encontrado el 25-ago-2026.** Lo encontró Dayana llenando el formulario, no
una revisión de configuración — y esa es la parte que hay que aprender.

---

## Qué pasa

Quien llena **cualquiera** de los ocho formularios de lead magnet no llega a su
recurso. Llega aquí:

```
https://funnel.dgdesignmodeling.com/webinar-certificados-confirmacion
```

> ¡REGISTRO COMPLETADO! Haz clic en el siguiente botón y podrás ingresar al
> evento. RECUERDA: 📅 **Fecha: 26 de febrero de 2025.**

Una confirmación de un webinar que ocurrió **hace un año y medio**, con un
botón «IR AL WEBINAR AHORA». Nada de la calculadora, del test, del ebook ni de
la guía de acero.

Los ocho. Sin excepción:

```
acceso-gratis-verificacion-acero-form      → webinar-certificados-confirmacion
acceso-gratis-calculadora-zapatas-form       → webinar-certificados-confirmacion
acceso-gratis-test-nivel-bim-form            → webinar-certificados-confirmacion
acceso-gratis-curso-introductorio-bim-form   → webinar-certificados-confirmacion
acceso-gratis-modulo-diplomado-bim-form      → webinar-certificados-confirmacion
descarga-gratis-ebook-bim-form               → webinar-certificados-confirmacion
descarga-gratis-guia-bim-form                → webinar-certificados-confirmacion
descarga-gratis-ai-pro-form                  → webinar-certificados-confirmacion
```

---

## Por qué no se veía

**El destino por defecto de los ocho estaba bien.** Se comprobó uno por uno y
cada formulario apuntaba a su propia página de gracias. Mirando esa pantalla,
todo estaba correcto.

Lo que manda es una **regla condicional**, que en GHL **gana sobre el destino
por defecto**:

```
si   full_name está lleno
 o   email     está lleno
 o   phone     está lleno
entonces → redirigir a /webinar-certificados-confirmacion
```

Con **«o»** y con **«está lleno»** sobre campos que son **obligatorios**, esa
condición se cumple **siempre**. No es una regla que se dispare a veces: se
dispara en el 100% de los envíos. El destino por defecto no se alcanza nunca.

Es una regla que quedó de la campaña del webinar de febrero de 2025 y se
heredó a cada formulario que se creó copiando otro.

---

## Qué hay que hacer

En **cada uno de los ocho** formularios: **Forms → editar → Settings → borrar
la regla condicional.** El destino por defecto ya está bien en siete de ocho y
con eso empieza a funcionar solo.

Y una corrección aparte, del destino por defecto:

```
acceso-gratis-test-nivel-bim-form  →  acceso-gratis-curso-introductorio-bim-gracias
                                      debería ser  acceso-gratis-test-nivel-bim-gracias
```

Después de borrar la regla, ese seguiría cayendo en el lugar equivocado.

**La comprobación no es mirar la configuración.** Es llenar el formulario y ver
dónde se cae. Que fue exactamente como apareció esto.

---

## Cuánto costó

No se puede saber con lo que hay en el repositorio, y no se va a estimar a ojo.
Lo que sí se sabe:

- La **Calculadora de Zapatas** y el **Test de Nivel** tienen pauta activa.
- Del 26-jul al 24-ago, `MASTER FORM V2` trajo **171 leads**.
- Cada uno de esos contactos **sí entró al CRM** —el formulario guarda antes de
  redirigir— pero **ninguno recibió lo que se le prometió** en la pantalla.

Los contactos están. Lo que no hubo fue entrega. Hay una lista de gente a la
que se le debe un recurso, y se puede reparar: se les manda el enlace por la
secuencia de correo.

---

## Cómo no vuelve a pasar

`scripts/formularios_destino.py` comprueba los ocho y **falla** si alguno no
manda a su propia página de gracias. Resuelve el payload del widget de GHL para
leer el destino real, no el que se ve al lado de `redirectUrl` —en ese payload
hay varias URLs y solo una es la activa.

Corre solo en las métricas semanales, junto a `enlaces.py`. Y se puede correr a
mano cuando se toque un formulario:

```bash
python3 scripts/formularios_destino.py
```

**La lección, que es la misma de julio con otro disfraz:** un formulario que
guarda el contacto parece que funciona. El contacto entra, el CRM crece, los
números de leads se ven bien. Lo que falla es lo que la persona recibe, y eso
solo se ve recorriéndolo como lo recorre ella.


---

## Lo que quedó del mismo clon, revisado el 25-ago después de arreglar el destino

Dayana llenó el formulario y vio el botón. Buscando eso aparecieron tres cosas
más, de la misma raíz: formularios creados copiando otro, y el texto viajó con
la copia.

### 1 · El botón de ACERO dice «Curso Introductorio» — solo ese

```
Verificaciones Acero   →  Quiero mi Curso Introductorio gratis     ← MAL
Calculadora Zapatas    →  Quiero mi Calculadora gratis
Nivelación BIM         →  Quiero mi Prueba de Nivel gratis
Curso BIM              →  Quiero mi Curso Introductorio gratis     ← bien, ese sí lo es
Módulo 1               →  Quiero mi Módulo 1 gratis
Ebook BIM              →  Quiero mi Ebook BIM gratis
AI PRO                 →  Quiero mi GPT IA PRO gratis
```

Los otros seis dicen lo suyo. **Solo hay que cambiar el de acero**, a algo como
«Quiero las 5 verificaciones gratis».

### 2 · El correo de confirmación dice «Reserva de cupo exitosa» — los ocho

Es el asunto que le llega a quien se registra en cualquier lead magnet. Quedó
de la campaña del webinar, igual que la regla condicional: **misma raíz, otra
cara.** A quien descargó un ebook se le dice que reservó un cupo.

### 3 · La pregunta de nivel BIM vive en un campo llamado «Descarga Gratis la Guia BIM»

Los ocho traen «¿Cuál es tu nivel actual en BIM?». Está bien que esté —es una
pregunta de calificación y es consistente— pero la respuesta se guarda en un
campo personalizado llamado `Descarga Gratis la Guia BIM`
(`contact.descarga_gratis_la_guia_bim`, creado el 12-mar-2025).

O sea: en la ficha de cada contacto, su nivel de BIM aparece bajo un título que
no tiene nada que ver. No rompe nada — el dato se guarda — pero cualquiera que
lea esa ficha dentro de seis meses va a entender otra cosa. Renombrar el campo
es de un minuto y no afecta a los datos ya guardados.

> Para acero hay algo más de fondo: preguntar el nivel de BIM a quien viene por
> un recurso de estructuras metálicas no segmenta nada útil. Pero eso es
> decisión de Dayana, no un defecto.


---

## 26-ago · Aylin encontró la copia, y la ruta cambió

**Lo encontró Aylin mirando los enlaces**, no una revisión automática. Otra vez
la persona antes que el script.

La página de registro de acero **era una copia de la calculadora y conservaba
su URL**: `acceso-gratis-calculadora-zapatas-form-2929`. Al abrirla salía la
calculadora. Es la misma raíz de todo lo de ayer —clonar y que el clon
arrastre lo del original— pero en la capa del funnel, no en la del formulario.

Ester lo corrigió y de paso arregló dos cosas que estaban en la tarea:

- El **botón**, que decía «calculadora». Ahora dice **«Quiero la Verificación
  gratis»**. Comprobado.
- El **redirect** en Configuración.

### La ruta buena es la SINGULAR

```
acceso-gratis-verificacion-acero-form      ← esta
acceso-gratis-verificacion-acero-gracias   ← y esta
```

No `verificaciones` en plural, que es la que habíamos puesto nosotros.

**Hoy responden las cuatro** —plural y singular— y sirven lo mismo, con 48
bytes de diferencia. Así que nada está roto ahora mismo. Pero **la plural es la
que sobra**, y el día que alguien la borre, todo lo que apunte ahí cae.

Actualizado en el repositorio: el hub, el script de comprobación y los cuatro
documentos que la mencionaban. Falta **volver a pegar `ghl-recursos.html`** en
la página `/recursos` de Sites — está en la tarea de ClickUp *«Actualizar
enlace de Recurso»*.

### Lo que esto enseña, y va al agente

**La ruta se acuerda ANTES de construir, no después.** Nosotros escribimos
`verificaciones` en veinte sitios, Ester publicó `verificacion`, y hubo que
tocar siete archivos para que coincidieran. No fue grave porque las dos
responden; con una sola habría sido un 404 en el hub.

Y la segunda: **un clon arrastra su URL.** Se revisa la URL del paso del
embudo, no solo el contenido de la página.
