# Secuencia B — Test de Nivel BIM → Máster

**Para:** todo el que se registra en el Test de Nivel BIM (26 con correo hoy).
**Disparador:** tag `lead-test-nivel-bim` o entrada al pipeline.
**Duración:** 12 días · 5 correos.
**Destino:** **llamada de 30 minutos** — el Máster no se cotiza por correo.

**Sale de la secuencia** si: responde · agenda · compra · pide baja.

---

## ⚠️ El límite que hay que conocer antes de montarla

El test corre **en el navegador de la persona** y el resultado nunca vuelve a
GHL. Nosotros sabemos que se registró; **no sabemos qué nivel le salió.**

Por eso esta secuencia **no se personaliza por nivel obtenido**. Lo que sí
tenemos es el tag `predijo-nivel-1..4` cuando la persona pasó por el bot y
respondió qué nivel *creía* tener (mecánica de `TEXTOS-BOT.md`).

Y ahí está lo bueno: **la distancia entre lo que creía y lo que le salió es el
argumento**. El correo 1 se lo pregunta directamente, y la respuesta llega por
correo — que además nos saca a la persona del automático y la pone con un
humano, que es lo que queremos.

> **Si algún día el test devuelve el resultado a GHL** (haría falta que la app
> mande el nivel al formulario), esta secuencia se puede ramificar de verdad.
> Queda anotado como mejora, no como pendiente que bloquee.

---

## Correo 1 · Día 0 — La entrega + la pregunta

**Asunto:** Tu Test de Nivel BIM está aquí
**Preview:** 20 preguntas. Te ubica en uno de los 4 niveles.

```
Hola {{contact.first_name}},

Aquí tienes tu acceso. Guárdalo: puedes volver a entrar cuando quieras.

El test son 20 preguntas y te ubica en uno de los 4 niveles de la ruta
BIM: Modelador → Coordinador → BIM Manager 4D-5D → Especialista BIM+IA.

Dos cosas que lo hacen distinto de los tests que has visto:

1. Se cuenta por bloques y de forma CONSECUTIVA. Si dominas 4D-5D pero
   no sabes federar modelos, no te sube de nivel: te lo marca como
   conocimiento disperso. Duele un poco, pero es la verdad útil.

2. No te devuelve solo un número. Te dice qué competencias concretas te
   faltan para el siguiente peldaño.

Y para que quede claro: NO es una certificación ni un diploma. Es un
diagnóstico honesto para que sepas por dónde seguir.
```

**Botón:** `Hacer el test ahora` → `https://funnel.dgdesignmodeling.com/acceso-gratis-test-nivel-bim-form`

**PD:** `Cuando lo termines, respóndeme a este correo con el nivel que te salió. Me interesa de verdad — sobre todo si no fue el que esperabas.`

---

## Correo 2 · Día 2 — Los 4 niveles, explicados

> Único correo que se ramifica, y solo si existe el tag `predijo-nivel-N`.
> El cuerpo es el mismo; cambia el párrafo de apertura.

**Asunto:** Los 4 niveles BIM, sin humo
**Preview:** En qué se diferencia de verdad cada uno.

**Apertura si NO hay tag de predicción:**
```
Hola {{contact.first_name}},

Te explico los 4 niveles como los usamos nosotros, sin la palabrería
de siempre.
```

**Apertura si el tag es `predijo-nivel-1` o `predijo-nivel-2`:**
```
Hola {{contact.first_name}},

Cuando hablamos, me dijiste que te ubicabas en los primeros niveles. Casi
siempre esa gente se está subestimando: sabe más de lo que cree, pero le
falta el nombre técnico de lo que ya hace. Mira si te reconoces.
```

**Apertura si el tag es `predijo-nivel-3` o `predijo-nivel-4`:**
```
Hola {{contact.first_name}},

Me dijiste que te ubicabas alto. Aquí va la parte incómoda: el salto de
nivel 3 a 4 casi nunca es de software. Mira dónde te ves de verdad.
```

**Cuerpo (igual para todos):**
```
🔹 NIVEL 1 · Modelador BIM
   Modelas bien y rápido. El modelo es tuyo y funciona.
   El techo: dependes de que otro te diga qué modelar.

🔹 NIVEL 2 · Coordinador BIM
   Federas modelos de varias disciplinas, detectas interferencias y las
   resuelves con criterio (no solo las listas).
   El salto real: dejar de mirar TU modelo y empezar a mirar EL proyecto.

🔹 NIVEL 3 · BIM Manager 4D-5D
   Metes tiempo y costo en el modelo. El BIM deja de ser una entrega y
   pasa a ser la herramienta con la que se decide.
   El salto real: hablar con el que pone la plata, no con el que dibuja.

🔹 NIVEL 4 · Especialista BIM + IA
   Automatizas lo repetitivo y usas IA donde de verdad aporta. Construyes
   tus propias herramientas en vez de esperar a que salga el plugin.
   El salto real: dejar de usar software y empezar a hacerlo.

El salto que más cuesta —y de lejos— es del 1 al 2. No es técnico: es
dejar de ser el que ejecuta y pasar a ser el que decide.
```

**Botón:** `Ver mi nivel` → `https://funnel.dgdesignmodeling.com/acceso-gratis-test-nivel-bim-form`

**PD:** `¿En cuál te ubicaste? Respóndeme, me sirve muchísimo para saber qué contenido preparar.`

---

## Correo 3 · Día 5 — El salto que más cuesta

**Asunto:** De modelador a coordinador: por qué se atasca ahí
**Preview:** No es falta de software.

```
Hola {{contact.first_name}},

De toda la ruta, donde más gente se queda atascada es entre el nivel 1 y
el 2. Llevo años viéndolo y el motivo siempre es el mismo.

No es que no sepan el software. Es que nadie les enseñó a coordinar.

Modelar es un trabajo individual: tu modelo, tu disciplina, tu entrega.
Coordinar es otro oficio: decidir qué se cambia cuando dos disciplinas
chocan, y sostener esa decisión frente a gente que no quiere cambiarla.

Eso no se aprende con un tutorial de YouTube, porque no es una función
del programa. Se aprende con proyectos reales y con alguien que ya lo
hizo diciéndote por qué esa decisión y no la otra.

Es exactamente para lo que existe el Máster Internacional en BIM
Management e Inteligencia Artificial: no es un curso de software, es la
ruta completa de los 4 niveles con las microcredenciales de cada peldaño.
```

**Botón:** `Quiero que me cuenten cómo funciona` → `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe`

**PD:** `Son 30 minutos, sin compromiso. Me cuentas dónde estás y te digo si te sirve o no — a veces la respuesta es que todavía no.`

**→ Quien clique se etiqueta `lead-caliente` y la oportunidad pasa a "Interesado".**

---

## Correo 4 · Día 8 — El diferenciador real

> El Máster no compite por precio ni por horas. Compite por esto. Y esto es
> **verificable**, no promesa.

**Asunto:** Microcredenciales, no un PDF al final
**Preview:** La diferencia entre "hice un curso" y "puedo demostrarlo".

```
Hola {{contact.first_name}},

Un certificado al final de un curso dice que asististe. No dice qué sabes
hacer.

Por eso el Máster va por microcredenciales progresivas: una por cada
nivel de la ruta que te expliqué.

🎖️ Modelador BIM
🎖️ Coordinador BIM
🎖️ BIM Manager 4D-5D
🎖️ Especialista BIM + IA

Cada una avalada por el Silicon Valley Futures Institute, y cada una la
obtienes al demostrar ese nivel — no por asistir. Es lo único de todo
nuestro catálogo que tiene ese aval: ninguna Especialización lo lleva.

Y hay algo que casi nadie ofrece: la DMA Engineering Suite. Sacamos una
app de IA propia al mes y tú te la llevas. Te gradúas con tu propio kit
de herramientas funcionando, no con una carpeta de PDFs.

Además: 12 certificaciones Autodesk y títulos universitarios (Sabal
University EE.UU., aval SENESCYT en Ecuador, ISTE/DQ en Europa).
```

**Botón:** `Ver todas las acreditaciones` → `https://funnel.dgdesignmodeling.com/design-modeling-acreditaciones`

**PD:** `Si quieres saber en qué peldaño entrarías tú y cuánto te tomaría, eso se ve mejor hablando: https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe`

---

## Correo 5 · Día 12 — El cierre

**Asunto:** 30 minutos y te digo por dónde empezar
**Preview:** Último de esta serie.

```
Hola {{contact.first_name}},

Último correo de esta serie. De aquí en adelante solo te llega el
contenido de siempre.

Te dejo la única cosa que de verdad mueve la aguja: una llamada de 30
minutos.

No es una llamada de ventas disfrazada. Es esto:

→ Me cuentas en qué nivel estás y a dónde quieres llegar
→ Te digo qué te falta concretamente para el siguiente peldaño
→ Y si el camino es con nosotros, te explico cómo; si no, te digo qué
  harías tú por tu cuenta

He tenido esa conversación con gente a la que le dije que todavía no era
su momento. Prefiero eso a venderte algo que no te sirve.
```

**Botón:** `Agendar mis 30 minutos` → `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe`

**PD:** `Y si prefieres escribir antes de hablar, responde a este correo. Me llega a mí.`

---

## Recordatorio de regla

**El precio del Máster no va en ningún correo de esta secuencia.** Es regla
permanente del proyecto (`matriz-viral/CLAUDE.md`): el Máster nunca se cotiza
por contenido ni por chat, el objetivo de cada pieza es generar la
conversación. Aquí el precio se dice **en la llamada**.
