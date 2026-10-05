# Plantillas automáticas de GHL que hay que corregir

> **Para Patricio y Dayana.** Salen de la auditoría del 5-oct-2026 (`matriz-viral/fuentes/ghl/auditoria-bot-ventas.json`). Se revisaron las 239 conversaciones de WhatsApp más recientes, con todo su historial. El número es cuántas veces aparece cada mensaje en esas conversaciones.
>
> No son mensajes del agente de IA: son **workflows de GHL** que se disparan solos. Aunque el agente mejore, estas plantillas siguen saliendo y le quitan credibilidad.

## 1. Cadena de seguimiento de Acero: urgencia falsa y despedida

En muchas conversaciones, los cuatro últimos mensajes son siempre estos, en este orden, sin que la persona haya respondido nada:

| Veces | Mensaje |
|---|---|
| 65 | «¿Qué tal, [nombre]? Quería saber si lograste revisar la información que te envié… Cualquier duda… te la resuelvo por aquí mismo.» |
| 133 | «¡Solo por hoy, [nombre]! Al inscribirte hoy… te llevas el curso de Cimentaciones BIM sin costo adicional.» |
| 119 | «Últimos cupos ⏳ … aún estás a tiempo de aprovechar el 2x1… El día de hoy cerramos todos los cupos disponibles en promoción.» |
| 129 | «Esperamos ser parte de su crecimiento profesional en un futuro… te obsequiamos un curso introductorio BIM…» |

**Por qué hace perder ventas:**
- La misma persona recibe «solo por hoy» y «hoy cerramos los cupos» en días distintos. Al segundo mensaje se da cuenta de que la urgencia no es verdad, y eso le quita credibilidad a todo lo demás.
- La Especialización abre todos los meses: no hay un cierre de cupos «hoy».
- El «2x1» sigue vigente, pero como gancho para quien no le ve el valor al programa, no como urgencia de «hoy» mandada a todos.
- La despedida llega con 4 mensajes seguidos sin respuesta, y ninguno hace una pregunta sobre la persona.

**Qué poner en su lugar** (la cadencia del prompt del agente):

| Cuándo | Mensaje |
|---|---|
| 24 h | Algo útil ligado a lo que dijo, más una pregunta fácil. «Me quedé pensando en lo que me contaste de las naves: en esta clase se ve cómo se calcula la cercha [enlace]. ¿Es el tipo de proyecto que te piden?» |
| 48 h | «¿Sigues buscando aprender cálculo en acero o lo dejamos para más adelante?» |
| 5 días | «No quiero llenarte de mensajes. ¿Lo dejamos para otro momento o te reservo el cupo de este mes?» Si dijo que no le ve el valor, aquí va el 2x1 (sin «solo por hoy»). La promo de USD 100 ya no existe. |
| Después | La despedida con el curso de regalo está bien, pero **sola**, sin las dos urgencias antes. |

## 2. Fechas y ofertas vencidas que siguen saliendo

| Veces | Mensaje | Problema |
|---|---|---|
| 10+ | «Ya casi estamos listos para comenzar el Máster BIM+IA! Empezamos en Marzo 2026» y «Agenda tu inscripción hoy en PREVENTA» | Marzo de 2026 ya pasó, y el Máster ya no se vende como programa con fecha de inicio. |
| 1+ | «Empezamos este 05 de febrero de 2026» (Diplomado BIM) | Fecha vencida. |
| 16 | «Estamos con una preventa exclusiva de todos los cursos que lanzaremos para el año 2026» | Ya es octubre de 2026. |
| 22 | «Nuevo programa AUTODESK INTELIGENCIA ARTIFICIAL – 12 Cursos… por solo $299.99 USD (valor real $2399.99)» | **Ya no está a la venta: apagar esta plantilla.** |
| 23 | «Son únicamente 10 plazas disponibles» | Número de cupos que no está confirmado. |
| 1+ | «El día de hoy cerramos los cupos disponibles en la Especialización al 30 % off» | Otra urgencia de «hoy», con otro descuento distinto. |

## 3. Anuncios con un precio viejo: USD 199

Las personas llegan desde anuncios que todavía dicen **«💥 Precio especial: $199 USD por tiempo limitado»**, y Acero cuesta **USD 225** desde el 3-sep. Por eso aparecen mensajes como «¿Algún mejor precio de los $199?» o «Tipo $75 dos cuotas». La persona siente que le subieron el precio en el chat.

- **Pauta:** pausar o editar los anuncios que dicen $199 (Olympus).
- **Agente:** a quien llega por un anuncio de USD 199,99 se le respeta ese precio, **sin el Tutor IA**; con el tutor queda en USD 225 (decidido por Dayana el 5-oct).

## 4. Mensajes del agente que también salen como plantilla

| Veces | Mensaje | Qué cambiar |
|---|---|---|
| 12 (y 198 mensajes que cierran con «revísalo…» o «me cuentas») | «Revísalo con calma y me cuentas qué te parece 🙌» | Prohibido en el prompt nuevo (regla 1). |
| 21 + 12 + 13 | «Te dejo el PDF / el temario completo para que veas todo lo que incluye» | El temario va con una pregunta (regla 6). |
| 13 | «Buenas tardes colega, cuéntame ¿Lograste revisar la información que le envié?» | Seguimiento vacío. Cambiar por uno que aporte algo. |
| 100 | «¿Tienes 5 minutos ahora para contarte cómo funciona?» | Funciona como apertura, pero solo si después se pregunta por la persona, no si se manda el folleto. |
