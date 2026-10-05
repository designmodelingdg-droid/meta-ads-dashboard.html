# Para Patricio: agente de ventas de WhatsApp

Patricio, estas son las instrucciones nuevas del agente de ventas, ya validadas por Dayana el 5 de octubre.

**Por qué cambiamos:** revisamos en GHL las 239 conversaciones de WhatsApp más recientes.
- El 95 % termina con un mensaje nuestro.
- En el 65 %, nuestro último mensaje no hace ninguna pregunta.
- Solo 23 personas llegaron a recibir el enlace de pago.

El agente informa bien, pero no lleva a la persona al siguiente paso.

## 1. Qué cargar en el agente

| Archivo | Dónde va |
|---|---|
| `PROMPT-AGENTE-VENTAS.md` | Instrucción de sistema. Reemplaza la actual. |
| `OBJECIONES-DMA.md` | Base de conocimiento |
| `ANTES-Y-DESPUES.md` | Base de conocimiento |
| `METODOS-DE-VENTA.md` | Base de conocimiento |

## 2. Lo que cambia en el comportamiento

- Cada mensaje termina en una pregunta o en un paso concreto. Se acaba el «revísalo con calma y me cuentas».
- Mensajes de 2 a 4 líneas. Primero pregunta qué necesita la persona y después presenta.
- Usa lo que la persona respondió en el formulario.
- Nunca niega que es un asistente. Cuando le piden una persona, o cuando desconfían, pasa la conversación a **Ester (a cualquier hora)**.
- **Cierre de Acero:** «¿Te paso el enlace para pagar con tarjeta o prefieres PayPal?»

## 3. Reglas de precio y promos (confirmadas por Dayana)

- **Acero:** USD 225 con el Tutor IA. El tutor tiene un límite de **20 preguntas al día**.
- **Asesoría en vivo con instructores:** el alumno la agenda mientras hace el curso, **sin costo**.
- **Cuotas:** solo si la persona dice que no puede pagar todo de una vez. Si acepta, pasa a Ester.
- **Anuncio de USD 199,99:** se respeta ese precio, pero **sin el Tutor IA**.
- **2x1:** es el gancho para quien no le ve el valor al programa. Nunca va de entrada ni con «solo por hoy».
- **No hay promo de USD 100.**
- **El programa AUTODESK IA de USD 299,99 ya no está a la venta.**
- El precio del Máster y de los Diplomados no se da por chat: se agenda una llamada con un asesor.

## 4. Plantillas de los workflows de GHL que hay que corregir

El detalle está en `PLANTILLAS-GHL-A-CORREGIR.md`. Lo urgente:
1. **Cadena de seguimiento de Acero.** Hoy salen seguidos «¿lograste revisar?», «¡Solo por hoy…!», «Últimos cupos… hoy cerramos» y la despedida. Hay que reemplazarla por la cadencia de 24 h, 48 h y 5 días del prompt. El 2x1 se queda, pero sin «hoy cerramos».
2. **Apagar las plantillas vencidas:**
   - «El Máster empieza en marzo 2026»;
   - «Preventa 2026»;
   - «Diplomado empieza el 05 de febrero de 2026»;
   - «únicamente 10 plazas»;
   - el programa de USD 299,99.
3. **Avisar a Ester en GHL** cada vez que el agente pase una conversación (con una etiqueta, una tarea o una notificación, como te quede mejor).

## 5. Cómo lo vamos a medir

Cada semana corre una auditoría automática en GHL. Lo que miramos:
- cuántas conversaciones terminan con nuestro mensaje (hoy, 95 %);
- cuántos últimos mensajes no hacen ninguna pregunta (hoy, 65 %);
- cuántas conversaciones llegan al enlace de pago (hoy, 23 de 239).
