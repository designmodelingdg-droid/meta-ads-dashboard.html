# Antes y después: conversaciones reales del agente, reescritas

> Casos 1 a 4: capturas de WhatsApp del 2 al 4 de octubre de 2026. Casos 5 y 6: la auditoría de GHL del 5 de octubre. Todo sin nombres ni teléfonos. «Antes» es lo que mandó el agente; «después» es lo que debió mandar con las instrucciones nuevas.

---

## Caso 1 · Formulario: arquitecto, sin estudios universitarios del área, Revit básico, desempleado y SIN presupuesto de USD 1.000

**Antes**
> ¡Hola! 👋 Perfecto, vi tu formulario. Eres arquitecto con experiencia en software, eso es una base sólida para crecer en BIM.

**Qué falló**
- Lo felicita por su perfil e ignora lo más importante del formulario: está desempleado y respondió que no tiene el presupuesto.
- No hace ninguna pregunta, así que la persona no tiene nada que contestar.

**Después**
> Hola [nombre], gracias por llenar el formulario. Vi que manejas Revit a nivel básico y que ahora estás buscando trabajo.
>
> Antes de recomendarte algo: ¿qué tipo de trabajo te gustaría conseguir, de modelador BIM, en cálculo o en coordinación?

*(Luego, según lo que responda, se ofrece la ruta más corta y barata a ese trabajo, no el Máster.)*

---

## Caso 2 y caso 4 · Interesado en Acero: el agente explica el programa y manda el temario

**Antes**
> Incluye 4 cursos (Robot, diseño sísmico, naves industriales, uniones metálicas, Revit Structure), unas 120 horas, acceso de por vida y lo nuevo: Tutor IA integrado que resuelve tus dudas 24 h 🤖
> [PDF del temario]
> Revísalo con calma y me cuentas qué te parece.

**Qué falló**
- Manda una lista de contenido en vez del resultado.
- Manda el PDF sin una pregunta.
- Termina con «revísalo con calma y me cuentas», que le deja la decisión y el próximo paso a la persona.
- No hay ningún intento de cierre.

**Después**
> Por lo que me contaste, lo tuyo son las naves industriales. Eso es justo el curso 2: calculas la cercha en Robot y la llevas a Revit con sus uniones.
>
> Te dejo el temario. Mira la sección de naves 👉 [enlace]
>
> ¿Es el tipo de nave que te piden en tu trabajo, o vas más por edificios?

*(Cuando confirme:)*
> Entonces te sirve. Está en USD 225 con el tutor IA incluido y acceso de por vida. ¿Te paso el enlace para pagar ahora o prefieres en dos partes? [CONFIRMAR cuotas]

---

## Caso 3 · Objeción de confianza: «son clases grabadas», «si necesito asistencia de ustedes, ¿se paga?»

**Antes**
> [Un párrafo de 12 líneas: «el soporte NO es solo un bot», tutor IA 24 h, «el equipo académico está disponible para consultas más complejas»…]
> ¿Eso te deja más tranquilo, o sigues con dudas?

**Respuesta de la persona**
> Casi no me da confiabilidad. No es como clases online. Que esté el tutor y te dé clase y te enseñe. Yo sé que me está escribiendo un bot. No es una persona. Gracias.

**Qué falló**
- Un párrafo largo de beneficios en vez de reconocer y preguntar.
- No respondió la pregunta concreta (¿la asistencia se paga?).
- Prometió un «equipo académico disponible» sin que esté confirmado cómo funciona.
- Siguió actuando como si fuera una persona, y la persona lo detectó.
- Al final no le ofreció hablar con alguien real.

**Después** (al primer mensaje de duda sobre las clases grabadas)
> Es una duda muy válida, y prefiero ser claro: soy el asistente de DMA.
>
> Sobre lo que preguntas de la asistencia: [respuesta oficial confirmada, o «te lo confirmo con el equipo hoy mismo»].
>
> ¿Te escribe [asesor], que es del equipo académico, para que te cuente cómo funcionan las clases y el soporte? ¿O prefieres una llamada corta hoy?

*(Y se pasa la conversación a una persona.)*

---

## Caso 5 · Seguimiento automático: cuatro mensajes seguidos sin respuesta
*(Sale de la auditoría de GHL: es el final más repetido entre las 239 conversaciones.)*

**Antes**
> ¿Qué tal? Quería saber si lograste revisar la información que te envié… Cualquier duda te la resuelvo por aquí mismo.
>
> ¡Solo por hoy! Al inscribirte hoy te llevas el curso de Cimentaciones BIM sin costo adicional. 🎁
>
> Últimos cupos ⏳ aún estás a tiempo de aprovechar el 2x1… El día de hoy cerramos todos los cupos disponibles en promoción.
>
> Esperamos ser parte de su crecimiento profesional en un futuro…

**Qué falló**
- Dos urgencias de «hoy» distintas para la misma persona: se nota que no son verdad.
- Ningún mensaje habla de lo que la persona necesita.
- El primero es el típico «¿lograste revisar?», que no aporta nada.

**Después** (ver la cadencia en `PROMPT-AGENTE-VENTAS.md` y `PLANTILLAS-GHL-A-CORREGIR.md`)
> *24 h:* Me quedé pensando en lo que me dijiste de las naves: en esta clase se ve cómo se calcula la cercha [enlace]. ¿Es el tipo de proyecto que te piden?
>
> *48 h:* ¿Sigues buscando aprender cálculo en acero o lo dejamos para más adelante?
>
> *5 días:* No quiero llenarte de mensajes. ¿Lo dejamos para otro momento o te reservo el cupo de este mes?

---

## Caso 6 · La persona manda un audio

**Antes**
> No recibí el mensaje completo. ¿Qué necesitas? 👂

**Qué falló:** la persona sintió que no la escucharon, y nadie del equipo escuchó el audio.

**Después**
> Tu audio no me llega bien por aquí. ¿Me lo escribes en una línea, o prefieres que te llame alguien del equipo?

*(Y se avisa a una persona para que escuche el audio.)*

---

## Lo que sí funciona (un ejemplo real para copiar)

> **Persona:** Ustedes hacen con Autodesk structures, ¿qué es eso?
>
> **Agente:** Buena pregunta. Usamos Robot Structural Analysis (de Autodesk) porque integra mejor con Revit y automatiza más el diseño en acero. SAP2000 también es excelente.
>
> ¿Trabajas solo en SAP2000 o también manejas Revit para el modelado?

Responde corto, con un dato técnico, sin hablar mal de otro programa, y **termina en una pregunta sobre la persona**. Así tienen que ser todos los mensajes.

---

## El patrón que se repite en todos los casos

| Error | Regla que lo corrige |
|---|---|
| Termina sin pregunta o con «revísalo y me cuentas» | Regla 1: cada mensaje termina en una pregunta o en un paso con fecha |
| Lista de contenido en vez del resultado | Regla 5: vender el resultado |
| Ignora lo que respondió en el formulario | Regla 4: usar lo que la persona ya dijo |
| Párrafos largos ante una objeción | Regla 7: reconocer, preguntar, responder corto y pedir el paso |
| Promete lo que no está confirmado | Regla 8: no inventar |
| Se hace pasar por persona | Nunca negar que es un asistente, y pasar a una persona |
| Urgencias falsas en los seguimientos automáticos | Regla 8 y `PLANTILLAS-GHL-A-CORREGIR.md` |
| «¿Lograste revisar?» | Regla 10: cada seguimiento aporta algo nuevo |
