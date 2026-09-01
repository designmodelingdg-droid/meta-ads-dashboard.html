# Secuencia C — Reactivación de la lista dormida

**Para:** los ~1.999 contactos que llegaron por ebook, guía BIM, AI PRO o los
cursos gratuitos y llevan meses sin recibir nada.
**Disparador:** carga manual una sola vez (después esta secuencia se apaga).
**Duración:** 8 días · 3 correos.
**Destino:** el hub `/recursos` primero, re-segmentar después.

**Sale de la secuencia** si: responde · agenda · compra · pide baja · hace el test.

---

## ⚠️ Lo primero: cómo se envía

Aunque los 1.999 entren de una sola vez, **GHL los manda en lotes de 400 por
día durante 5 días**. En el montaje esto es una casilla ("Batch"), no un
trabajo extra.

El motivo, en corto: 2.000 correos de golpe a una lista que no recibe nada hace
meses produce un pico de rebotes y de "marcar como spam" que los filtros leen
como lista comprada. El dominio ya está calentado y funcionando — eso costó
meses y se pierde en un día.

**Antes de encender**, en GHL: quitar los contactos ya marcados como rebote
duro o dados de baja. Si la plataforma ofrece validación de lista, pasarla.
Cada correo a una dirección muerta cuenta en contra.

**Freno de mano:** quien no abra **ninguno** de los 3 correos queda con tag
`email-frio` y deja de recibir envíos. No se insiste.

---

## Correo 1 · Día 0 — Devolver valor, no pedir nada

> Cero venta. Cero producto. Un solo enlace, y que sea el mejor que tenemos.
> El hub ya demostró que funciona: un contacto se llevó **5 recursos en 9
> minutos** el día que se lanzó.

**Asunto:** Hace tiempo que no te escribo (y te debo algo)
**Preview:** 10 recursos gratis en una sola página. Sin registrarte otra vez.

```
Hola {{contact.first_name}},

Hace un tiempo descargaste uno de nuestros recursos y, con honestidad,
después no te escribimos casi nada. Estuvimos con la cabeza metida en
construir cosas.

Esas cosas ya están listas, y quiero que las tengas.

Armamos una sola página donde vive TODO lo que hemos hecho gratis:

🛠️ La Calculadora de Zapatas — predimensiona en 2 minutos desde el celular
🎯 El Test de Nivel BIM — 20 preguntas, te dice en qué peldaño estás de verdad
📚 5 descargas: ebook BIM, guía BIM, AI PRO, curso introductorio y un
   módulo completo del diplomado
📝 Artículos del blog
👥 Y la comunidad, por si quieres preguntar cosas

Todo abierto. No hay que registrarse otra vez ni pagar nada.
```

**Botón:** `Ver los 10 recursos` → `https://funnel.dgdesignmodeling.com/recursos`

**PD:** `Cuéntame en qué estás trabajando ahora — responde a este correo y te digo cuál de los recursos te sirve más. Leo todas las respuestas.`

---

## Correo 2 · Día 4 — El segmentador

> Este correo es el que más trabaja de los tres. Quien hace el test **entra a
> la secuencia B** y deja de ser lista dormida: pasa a ser un lead con tema y
> con destino.

**Asunto:** ¿En qué nivel BIM estás realmente?
**Preview:** 20 preguntas. La respuesta suele sorprender.

```
Hola {{contact.first_name}},

Te hago una pregunta incómoda: si mañana te ofrecen liderar la
coordinación BIM de un proyecto grande, ¿lo tomas?

La mayoría duda. Y casi siempre duda por la razón equivocada — no por lo
que le falta, sino por lo que cree que le falta.

Hicimos un test de 20 preguntas que te ubica en uno de los 4 niveles
reales de la ruta BIM y —esto es lo importante— te dice qué competencias
concretas te faltan para el siguiente.

Es honesto a propósito: cuenta por bloques y de forma consecutiva. Si
dominas 4D-5D pero no sabes federar modelos, no te sube de nivel. Te lo
marca como conocimiento disperso, que es lo que es.

Es gratis, son 20 preguntas y NO es una certificación. Es un diagnóstico.
```

**Botón:** `Hacer el test` → `https://funnel.dgdesignmodeling.com/acceso-gratis-test-nivel-bim-form`

**PD:** `Responde con el nivel que te salió. Sobre todo si no fue el que esperabas — esa distancia es la información más útil que vas a sacar del test.`

**→ Quien lo haga, entra a la secuencia B y sale de esta.**

---

## Correo 3 · Día 8 — Cierre honesto y limpieza

> Aquí se cierra y **se ofrece la baja de forma visible**. Suena a perder
> contactos; es al revés: quien se da de baja aquí es quien iba a marcarte
> como spam en el próximo envío. Una baja no hace daño; un reporte de spam
> se lo hace a todos los correos que mandes después.

**Asunto:** ¿Seguimos en contacto o te dejo tranquilo?
**Preview:** Sin rodeos: decides tú.

```
Hola {{contact.first_name}},

Te escribí dos veces esta semana después de mucho silencio, así que te
lo pregunto de frente en lugar de seguir insistiendo.

Si esto te sirve, quédate. Te va a llegar:
→ Las herramientas gratuitas nuevas (sale una cada pocas semanas)
→ Lo que vamos aprendiendo de BIM + IA aplicado a proyectos reales
→ Nada de spam ni de promociones todos los días

Si ya no te sirve, dale a "Darme de baja" ahí abajo. En serio, sin
resentimientos: prefiero una lista de gente a la que de verdad le
interesa que un número grande que no le sirve a nadie.

Y si estás en un momento de decidir qué estudiar o hacia dónde llevar tu
carrera, te ofrezco algo mejor que un correo: 30 minutos conmigo. Me
cuentas dónde estás, te digo qué haría yo en tu lugar. Aunque la
respuesta sea "por ahora nada".
```

**Botón:** `Agendar 30 minutos` → `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe`

**PD:** `Y si prefieres solo responder este correo contándome en qué andas, también vale. Me llega a mí.`

---

## Después de la secuencia

| Situación | Qué se hace |
|---|---|
| Hizo el test | Ya está en la secuencia B. Se le quita `seq-reactivacion` |
| Abrió y clicó, no convirtió | `seq-completada` → pasa a la lista de contenido normal |
| Abrió pero no clicó nunca | `seq-completada` → lista de contenido normal |
| **No abrió ninguno** | **`email-frio`** → deja de recibir envíos hasta nuevo aviso |
| Respondió | `respondio-correo` → lo atiende una persona |

Los `email-frio` no se borran. Se dejan quietos. Si algún día hay algo que de
verdad valga la pena (un lanzamiento grande), se puede hacer un último intento
con ellos aparte — pero nunca mezclados con la lista sana.
