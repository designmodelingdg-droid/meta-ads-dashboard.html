# Los ocho formularios mandan al webinar de febrero de 2025

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
acceso-gratis-verificaciones-acero-form      → webinar-certificados-confirmacion
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
