# El playbook — los ocho prompts, en orden

De la guía de tododeia sobre Apify, con los ajustes de DMA marcados **así**.
Se pegan de a uno, esperando respuesta. Cada uno deja un archivo que el
siguiente necesita.

---

## 1 · La entrevista que evita la lista basura

> Vas a ayudarme a conseguir clientes para **Design Modeling DG, la parte de
> consultoría** — no para la Academy. Antes de correr nada, entrevístame.
>
> Hazme las preguntas de a una, esperando mi respuesta, y no me des opciones de
> más de cinco. Necesitas saber:
> 1. Qué vende DG exactamente y en una línea qué problema resuelve.
> 2. Quién es el cliente ideal: tipo de empresa, tamaño, quién decide la compra.
> 3. Dónde están: ciudad, país. Si son varios, en qué orden.
> 4. Cuánto vale un cliente nuevo y cuántos hacen falta al mes.
> 5. Cómo se contacta hoy y qué ha funcionado o fallado.
> 6. Quién NO es cliente: los que ya sabemos que hacen perder el tiempo.
>
> Cuando tengas todo, escríbeme `perfil-cliente.md` con: el cliente ideal en un
> párrafo; mínimo cinco señales de que alguien SÍ califica, concretas y
> verificables desde fuera; mínimo cinco señales de descarte; la red donde
> conviene buscarlos y por qué esa; y cinco búsquedas concretas para arrancar.
>
> Muéstramelo antes de guardarlo. **Todavía no corras ningún actor ni gastes
> crédito.**

---

## 2 · La prueba de fuego con 10

> Vamos a probar antes de gastar. Lee `perfil-cliente.md`.
>
> Elige el actor de Apify correcto y, antes de correrlo: dime cuál elegiste y
> por qué; enséñame los parámetros exactos; calcula el coste; **y dime cuánto
> crédito queda este mes, contando que la matriz gasta de la misma cuenta todos
> los lunes**. Espera mi OK.
>
> Con mi OK, saca SOLO 10 resultados. Después evalúa la muestra y dime sin
> adornos: cuántos de los 10 cumplen mis señales, qué campos vinieron vacíos, y
> qué cambiarías para que la lista de 50 salga mejor.
>
> Si menos de 7 de 10 califican, no seguimos: propón la corrección y volvemos a
> probar. Guarda la muestra en `leads/muestra.csv`.

---

## 3 · Los 50, con tope de gasto

> Con la búsqueda ya corregida, sácame 50 clientes potenciales.
>
> Antes de correr, dime el coste estimado y espera mi OK. **Pon `maxItems` y
> `maxTotalChargeUsd` en la llamada** — es la regla 3 de `matriz-viral/CLAUDE.md`
> y aquí también rige. Si a media corrida ves que se va a pasar del doble de lo
> estimado, párate y avísame.
>
> Guarda en `leads/YYYY-MM-DD.csv` con estas columnas exactas y en este orden:
> `negocio | contacto | puesto | telefono | correo | sitio_web | instagram |
> linkedin | ciudad | rating | resenas | senal_de_calificacion | fuente | fecha`
>
> Reglas de los datos:
> - Si un dato no viene, escribe «sin dato». No lo deduzcas, no lo completes con
>   lo que parece lógico, **no inventes correos tipo contacto@**.
> - En `senal_de_calificacion`, la razón concreta por la que entra.
> - En `fuente`, el actor exacto que lo trajo.
> - Si un negocio ya está en algún CSV de `leads/`, no lo repitas.
>
> Al terminar: cuántos traen teléfono, cuántos correo, cuántos los dos. Y dime
> con honestidad si esta cosecha sirve.

---

## 4 · Enriquecer sin inventar

> Toma el CSV de hoy y compléta los huecos con otros actores — el crawler del
> sitio del negocio, o el scraper de la red que ese negocio sí usa. En lotes de
> 10, con el coste estimado antes del primero.
>
> Agrega dos columnas:
> - `origen_correo`: «scraper original», «sitio web», «red social» o «no encontrado».
> - `confianza`: alta si el correo está en el sitio oficial; media si viene de un
>   directorio o una red; baja si es genérico tipo `info@`.
>
> Reglas que no se rompen:
> - Sin correo verificable se queda en «sin dato» y sigue en la lista con su
>   teléfono. **Prefiero llamar que mandar un correo que rebote.**
> - **Nada de generar correos por patrón** (`nombre.apellido@dominio`). Eso quema
>   dominios, y el nuestro manda los correos de los alumnos.
> - Si el negocio cerró o el sitio no existe, márcalo «descartado» con el motivo.
>
> Cierra diciendo cuántos quedaron con confianza alta, cuántos media y cuántos
> solo con teléfono.

---

## 5 · Califica y ordena

> Califica los leads con las señales de `perfil-cliente.md`. No inventes
> criterios nuevos.
>
> Agrega:
> - `grado`: **A** = cumple ≥4 señales y tiene contacto confiable · **B** = 2-3
>   señales, o le falta la vía buena · **C** = apenas roza el perfil.
> - `porque`: la evidencia concreta en una línea. Nada de «parece buen
>   prospecto»; quiero «4,8 estrellas con 210 reseñas, sin sitio web, publica
>   seguido en Instagram».
>
> Los que caigan en una señal de descarte van a `descartados.csv` con el motivo.
>
> Después: cuántos A, B y C, y los 10 por los que empezarías tú. Ordena el CSV
> con los A arriba.

---

## 6 · Los correos que sí se leen

> ⚠️ **Antes de este paso: comprobar que el dominio de envío NO es
> `dgdesignmodeling.com`.** Ver `montaje-local.md`. Si todavía no hay dominio
> aparte y calentado, este paso se queda escrito pero no se manda.
>
> Escribe el correo de primer contacto para los de grado A y B.
>
> - **Asunto:** dos versiones, máximo 6 palabras, sin exclamaciones ni palabras
>   de promoción. Una directa y una en pregunta.
> - **Primera línea:** un dato REAL de ese negocio sacado del scraper. **Si no
>   hay dato real, no escribas el correo:** márcalo «sin ángulo» y va a llamada.
> - **Cuerpo:** el puente entre ese dato y lo que vendemos, en una o dos líneas.
>   Sin prometer números que no podemos probar.
> - **Cierre:** una pregunta que se conteste con sí o no. Nada de «agenda en mi
>   calendario» en el primer correo.
>
> Máximo 90 palabras, español neutro, tono de persona que escribe rápido y bien,
> no de agencia. Sin emojis, sin «espero que este correo te encuentre bien».
>
> Guarda en `correos/YYYY-MM-DD.csv`: `negocio | correo | asunto_a | asunto_b |
> cuerpo | angulo_usado | grado`.
>
> Antes de los 50, escríbeme 3 y espera mi visto bueno del tono.

---

## 7 · Los dos seguimientos

> Escribe los dos seguimientos para cada contacto al que ya escribimos.
>
> **Seguimiento 1** — a los 3 días hábiles si no contestó. Máximo 50 palabras.
> Aporta algo nuevo: un ejemplo corto, una idea aplicada a su negocio, un dato
> de su industria. **Nunca «solo dando seguimiento» como toda la razón de
> escribir.**
>
> **Seguimiento 2** — 7 días después del primero si sigue en silencio. Máximo 35
> palabras. Cerrar la puerta con elegancia: dejas de escribir, si en algún
> momento le sirve ahí estás. Sin culpa, sin reclamo.
>
> Reglas:
> - Si alguien contesta, aunque sea que no, **sale de la secuencia** y entra en
>   `memoria/no-contactar.csv`.
> - Dos seguimientos y se acabó. Nada de tres, cuatro y cinco.
> - Cada uno va en el mismo hilo, respondiendo al anterior.
>
> Guarda en `correos/seguimientos.csv`: `negocio | correo | seguimiento |
> dias_espera | asunto | cuerpo`.

---

## 8 · Qué funcionó, y afina la puntería

> Vamos a cerrar el ciclo. Pregúntame primero: cuántos abrieron, cuántos
> contestaron, cuántos dijeron que sí a una llamada, cuántos rebotaron y cuántos
> pidieron que no les escribiera.
>
> Con eso:
> 1. Compara a los que contestaron contra los que no. Qué tienen en común los
>    que sí: ciudad, tamaño, rating, si tenían sitio web, el ángulo, el asunto.
>    **Dime el patrón aunque sea incómodo.**
> 2. Qué asunto y qué ángulo funcionaron mejor, con los números que haya.
> 3. Si el rebote pasó del 3 %, qué hicimos mal al enriquecer.
> 4. Actualiza `perfil-cliente.md` con lo aprendido. Muéstrame los cambios
>    marcados antes de guardar.
>
> Cierra con las tres cosas concretas que cambiamos en la siguiente ronda.
> Cambios a las búsquedas, a los filtros o a los correos — **nada de consejos
> generales de ventas.**
