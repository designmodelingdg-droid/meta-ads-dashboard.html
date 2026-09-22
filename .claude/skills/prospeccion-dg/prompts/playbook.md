# El playbook — ocho pasos, por teléfono y WhatsApp

De la guía de tododeia sobre Apify, **con el canal cambiado**: teléfono y
WhatsApp primero, y el correo como tercer canal **solo para direcciones de
confianza alta**. Los ajustes de DMA van marcados **así**.

Se pegan de a uno, esperando respuesta. Cada uno deja un archivo que el
siguiente necesita.

## Por qué por teléfono y no por correo

| De 1.000 negocios de Google Maps | |
|---|---|
| Con **teléfono** | ~950 — viene directo del mapa |
| Con **correo** | ~350 — hay que entrar a su web a buscarlo |

Triplica la base contactable y gasta menos crédito. Por eso el teléfono va
primero: no es prudencia, es que rinde más.

**El correo entra para cubrir el hueco** — los que no traen teléfono utilizable.
Pero con un filtro: solo `confianza: alta`, que es el correo que está en el sitio
oficial del negocio. Los genéricos tipo `info@` y `contacto@` **nunca**: muchos
están abandonados y algunos son trampas de spam, y un golpe a una trampa hace más
daño que cien correos bien mandados.

De 1.000 negocios salen ~350 con correo, y de esos los de confianza alta son una
fracción: se acaba escribiendo a unos **50-80 por cada mil**. El volumen bajo sale
del filtro, no de contenerse.

## Las reglas del canal nuevo

Un negocio publica su teléfono en Google Maps **para que lo llamen**. Escribirle
o llamarle es contacto comercial normal — no es lo mismo que escribirle en frío
a una persona que nunca publicó nada.

Dicho eso, tres cosas que sí queman el número:

1. **Número aparte, no el personal de nadie.** Un WhatsApp Business propio para
   esto. Si lo bloquean, no se lleva por delante el teléfono con el que hablas
   con alumnos y clientes.
2. **Volumen bajo y creciendo despacio.** Un número nuevo mandando decenas de
   mensajes el primer día es la forma conocida de que lo bloqueen. No te doy una
   cifra exacta porque no la tengo verificada; empieza en unos pocos al día y
   sube según vaya.
3. **Nada de herramientas de envío masivo ni APIs no oficiales.** Ese es el
   disparador de bloqueo más claro que hay. Se manda a mano o con WhatsApp
   Business oficial.

Y una que vale más que las tres: **a los de grado A se les llama, no se les
escribe.** Una llamada de treinta segundos vale más que veinte mensajes.

---

## 1 · La entrevista que evita la lista basura

> Vas a ayudarme a conseguir clientes para **Design Modeling DG, la consultoría**
> — no para la Academy. El canal es **teléfono y WhatsApp**, no correo. Antes de
> correr nada, entrevístame.
>
> Hazme las preguntas de a una, esperando mi respuesta, y no me des opciones de
> más de cinco. Necesitas saber:
> 1. Qué vende DG exactamente y en una línea qué problema resuelve.
> 2. Quién es el cliente ideal: tipo de empresa, tamaño, quién decide la compra.
> 3. Dónde están: ciudad, país. Si son varios, en qué orden.
> 4. Cuánto vale un cliente nuevo y cuántos hacen falta al mes.
> 5. Cómo se contacta hoy y qué ha funcionado o fallado.
> 6. Quién NO es cliente.
> 7. **Quién va a llamar y en qué horario puede.** Esto manda: de nada sirve una
>    lista de 50 si nadie tiene la tarde para llamar.
>
> Cuando tengas todo, escríbeme `perfil-cliente.md` con: el cliente ideal en un
> párrafo; mínimo cinco señales de que alguien SÍ califica, verificables desde
> fuera; mínimo cinco de descarte; y cinco búsquedas concretas para arrancar.
>
> Muéstramelo antes de guardarlo. **Todavía no corras ningún actor ni gastes
> crédito.**

---

## 2 · La prueba de fuego con 10

> Vamos a probar antes de gastar. Lee `perfil-cliente.md`.
>
> Elige el actor de Apify correcto — **el de Google Maps normal, no el de datos
> de contacto: no necesitamos correos y ese cuesta más** — y antes de correrlo:
> dime cuál elegiste y por qué; los parámetros exactos; el coste; **y cuánto
> crédito queda este mes, contando que la matriz gasta de la misma cuenta todos
> los lunes**. Espera mi OK.
>
> Con mi OK, saca SOLO 10. Después evalúa y dime sin adornos: cuántos cumplen mis
> señales, **cuántos traen teléfono utilizable**, y qué cambiarías para que la
> lista de 50 salga mejor.
>
> Si menos de 7 de 10 califican, no seguimos: propón la corrección. Guarda en
> `leads/muestra.csv`.

---

## 3 · Los 50, con tope de gasto

> Con la búsqueda corregida, sácame 50.
>
> Antes de correr, dime el coste y espera mi OK. **Pon `maxItems` y
> `maxTotalChargeUsd`** — es la regla 3 de `matriz-viral/CLAUDE.md`. Si a media
> corrida se va a pasar del doble, párate y avísame.
>
> Guarda en `leads/YYYY-MM-DD.csv` con estas columnas exactas:
> `negocio | contacto | puesto | telefono | tiene_whatsapp | correo | sitio_web |
> instagram | ciudad | rating | resenas | senal_de_calificacion | fuente | fecha`
>
> Reglas:
> - Si un dato no viene, «sin dato». No lo deduzcas, no lo completes con lo que
>   parece lógico.
> - **`tiene_whatsapp` se queda en «por verificar»**. No lo adivines por el
>   formato del número: se comprueba abriendo el chat, y eso lo hace una persona.
> - **`correo` solo si el actor lo trae de serie.** No actives add-ons para
>   buscarlo todavía — eso es el paso 4 y solo para los que hagan falta.
> - En `senal_de_calificacion`, la razón concreta por la que entra.
> - En `fuente`, el actor exacto.
> - Si ya está en algún CSV de `leads/`, no lo repitas.
>
> Al terminar: cuántos traen teléfono y **cuántos son fijos y cuántos móviles**,
> que es lo que decide si se llama o se escribe.

---

## 4 · Enriquecer, sin inventar

> Toma el CSV de hoy y compléta **solo lo que sirve para contactar**.
>
> **Primero el teléfono**, que es el canal principal. Para los que no lo traigan,
> mira si lo publican en su Instagram o en su sitio.
>
> **Después el correo, y SOLO para los que se quedaron sin teléfono utilizable.**
> No gastes crédito buscando el correo de alguien a quien ya podemos llamar.
>
> Agrega:
> - `origen_telefono`: «google maps», «sitio web», «red social» o «no encontrado».
> - `mejor_hora`: si el negocio publica horario, la franja para llamar. Si no lo
>   publica, «sin dato». **No la supongas por el tipo de negocio.**
> - `origen_correo`: «sitio web», «red social» o «no encontrado».
> - `confianza`: **alta** si está en el sitio oficial del negocio, mejor si es de
>   una persona con nombre · **media** si viene de un directorio o una red ·
>   **baja** si es genérico tipo `info@` o `contacto@`.
>
> Reglas que no se rompen:
> - Sin teléfono verificable, «sin dato». **No se deduce un número por el prefijo
>   de la zona.**
> - **Nunca generes un correo por patrón** (`nombre.apellido@dominio`). Eso es lo
>   que de verdad quema un dominio, y el nuestro manda los correos de los alumnos.
> - Un correo que no encontraste se queda «sin dato». No lo inventes, no lo
>   deduzcas del dominio de la web.
> - Si el negocio cerró o el sitio no existe, «descartado» con el motivo.
>
> Cierra con tres números: **con cuántos se puede hablar por teléfono, a cuántos
> se les puede escribir con confianza ALTA, y cuántos se quedaron sin ninguna vía.**

---

## 5 · Califica y ordena

> Califica con las señales de `perfil-cliente.md`. No inventes criterios.
>
> - `grado`: **A** = ≥4 señales y teléfono utilizable · **B** = 2-3 señales, o le
>   falta el teléfono bueno · **C** = apenas roza el perfil.
> - `canal`: **llamada** si es A · **whatsapp** si es B con móvil · **correo** si
>   es B sin teléfono utilizable pero con `confianza: alta` · **sin via** si no
>   tiene ninguna de las tres. **A nadie se le contacta por dos canales.**
> - `porque`: la evidencia en una línea. Nada de «parece buen prospecto»; quiero
>   «4,8 estrellas con 210 reseñas, sin sitio web, publica seguido en Instagram».
>
> Los que caigan en señal de descarte van a `descartados.csv` con el motivo.
>
> Después: cuántos A, B y C, **cuántos van por cada canal**, y los 10 a los que
> llamarías tú primero. Ordena el CSV con los A arriba.

---

## 6 · Los guiones — llamada, WhatsApp o correo según el canal

> ⚠️ **Antes de este paso: el número de envío es un WhatsApp Business aparte, no
> el personal de nadie.** Ver `montaje-local.md`.
>
> **Para los de grado A, escribe el guion de LLAMADA.** No un párrafo: el guion
> hablado.
> - Los primeros 10 segundos: quién eres, de dónde sacaste su número («los vi en
>   Google Maps») y **una razón concreta de por qué les llamas a ellos** — un
>   dato real del scraper. Sin dato real, no hay llamada: va a la lista de los
>   que hay que investigar antes.
> - La pregunta que abre: una que se conteste hablando, no con sí o no.
> - **Las dos objeciones más probables y qué contestar**, en una línea cada una.
> - El cierre: qué se pide exactamente. Una reunión de 15 minutos, no «le mando
>   información».
>
> **Para los de grado B, el mensaje de WhatsApp.**
> - Máximo 4 líneas. Se lee en la vista previa o no se lee.
> - Primera línea: el dato real de ese negocio. **Sin dato real, no hay mensaje**
>   — se marca «sin ángulo».
> - Di de dónde sacaste el número. Un desconocido que no explica cómo llegó da
>   desconfianza.
> - Cierra con una pregunta fácil.
> - **Sin archivos adjuntos, sin enlaces en el primer mensaje, sin audio.** Un
>   primer contacto con enlace parece estafa.
> - Español de Ecuador, de usted, tono de persona no de empresa. Sin emojis.
>
> **Para los de canal `correo` — y SOLO los de `confianza: alta`.**
> - **Asunto:** dos versiones, máximo 6 palabras, sin exclamaciones ni palabras de
>   promoción. Una directa y una en pregunta.
> - Primera línea: el dato real de ese negocio. **Sin dato real, no hay correo.**
> - Di de dónde salió su contacto, igual que en WhatsApp.
> - Máximo 90 palabras. Sin emojis, sin «espero que este correo te encuentre
>   bien», sin párrafos de tres líneas.
> - Cierre: una pregunta que se conteste con sí o no. **Nada de «agenda en mi
>   calendario» en el primero.**
> - **Ni un solo correo a una dirección de confianza media o baja.** Si el único
>   contacto es `info@`, ese negocio se queda para llamada.
>
> Guarda en `contactos/YYYY-MM-DD.csv`: `negocio | telefono | correo | grado |
> canal | confianza | angulo_usado | guion`.
>
> Antes de los 50, escríbeme 3 de cada tipo y espera mi visto bueno del tono.

---

## 7 · El seguimiento — menos que en correo

> **En WhatsApp se insiste menos que en correo.** El mensaje se ve aunque no
> contesten, así que repetir molesta más y se nota más.
>
> **Un solo seguimiento**, a los 4 o 5 días hábiles, máximo 3 líneas. Aporta algo
> nuevo: un ejemplo corto, una idea aplicada a ese negocio. **Nunca «le escribo
> para dar seguimiento»** como toda la razón.
>
> Si no contesta al segundo, se acabó. Nada de tres y cuatro mensajes.
>
> **Para los de grado A que no contestaron la llamada:** un segundo intento a
> otra hora del día, y si no, un WhatsApp corto diciendo que llamaste.
>
> **Para los de canal correo:** un solo seguimiento, máximo 50 palabras, a los 3
> días hábiles. En el mismo hilo, respondiendo al anterior, no como correo nuevo.
>
> Reglas:
> - Si alguien contesta, aunque sea que no, **sale** y entra en
>   `memoria/no-contactar.csv`.
> - **Si alguien pide que no le escriban, entra en esa lista para siempre.** Ese
>   archivo no se limpia ni se reordena nunca.
> - Nunca se vuelve a escribir a un número que ya está en `ya-contactados.csv`
>   sin que yo lo pida.
>
> Guarda en `contactos/seguimientos.csv`: `negocio | telefono | intento |
> dias_espera | canal | mensaje`.

---

## 8 · Qué funcionó, y afina la puntería

> Vamos a cerrar el ciclo. Pregúntame primero: a cuántos llamé, cuántos
> contestaron el teléfono, cuántos contestaron el WhatsApp, cuántas reuniones
> salieron, cuántos números estaban malos y cuántos pidieron que no les
> escribiera.
>
> Con eso:
> 1. Compara a los que contestaron contra los que no: ciudad, tamaño, rating, si
>    tenían sitio web, el ángulo, la hora a la que se llamó. **Dime el patrón
>    aunque sea incómodo.**
> 2. **Llamada, WhatsApp o correo: cuál trajo más reuniones**, con los números que
>    haya. Si los A por teléfono no rinden más que los B por mensaje, el grado
>    está mal puesto y hay que revisarlo.
> 3. Si hubo muchos números malos, qué falló al enriquecer.
> 4. **EL REBOTE DE LOS CORREOS.** Cuántos rebotaron sobre cuántos se mandaron.
>    **Si pasa del 2 %, lo dices como aviso y paramos el canal de correo** hasta
>    arreglar el enriquecimiento: por encima de ahí Google empieza a castigar la
>    reputación del dominio, y ese dominio manda los correos de los alumnos.
>    Dime también cuántos de los que rebotaron eran de `confianza` media, porque
>    si son casi todos, el filtro tiene que subir a solo alta.
> 4. Actualiza `perfil-cliente.md` con lo aprendido. Muéstrame los cambios
>    marcados antes de guardar.
>
> Cierra con las tres cosas concretas que cambiamos en la siguiente ronda:
> búsquedas, filtros, guiones u horarios. **Nada de consejos generales de
> ventas.**
