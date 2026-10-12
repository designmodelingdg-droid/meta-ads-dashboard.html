# Auditoría semanal del bot, el cierre y las ventas · 12-oct-2026

Compara la auditoría de GHL del **5-oct** con la del **12-oct** (`scripts/ghl_auditoria_bot.py`, las 400 conversaciones más recientes de cada fecha) y los cobros reales de Stripe y PayPal (`matriz-viral/fuentes/ingresos/`).

**Cómo leerla:**
- Las dos muestras se solapan: son las conversaciones más recientes de cada día, no solo las de la semana. Por eso se comparan **porcentajes**, no totales.
- La versión 2 del prompt (`PROMPT-AGENTE-VENTAS.md`) todavía **no está cargada**. Esta semana mide el efecto de la versión 1, que Patricio cargó después del 5-oct.

## El bot

| Indicador | 5-oct | 12-oct | Lectura |
|---|---|---|---|
| Conversaciones revisadas | 247 | 351 | |
| Terminan con un mensaje nuestro | 95,5 % | 94,3 % | Igual: la persona sigue dejando de contestar |
| **Nuestro último mensaje termina en pregunta** | 23 % | **47 %** | Mejoró al doble |
| Nuestro último mensaje sin pregunta ni paso | 63 % | 46 % | Mejoró, pero sigue siendo casi la mitad |
| «Revísalo y me cuentas» en el último mensaje | 19 | 9 | Mejoró |
| **Conversaciones que llegan al enlace de pago** | 8,9 % (22) | **11,7 % (41)** | Mejoró |
| Conversaciones con propuesta de llamada | 30 % | 25 % | Bajó |
| Respuesta a una objeción que termina en pregunta | 20 % | 20 % | **Sin cambio**: ante una objeción sigue informando y no pregunta |
| Largo mediano de nuestros mensajes | 154 caracteres | 145 | Algo más cortos |

Las objeciones que más aparecen siguen siendo las mismas: «lo pienso» (55), pedir descuento (51), clases grabadas (19), tiempo (17) y confianza (13).

**Fallas nuevas que vio Dayana** (primera medición, ver `PARA-PATRICIO.md`):
- 145 conversaciones con 3 o más saludos;
- 79 con dos mensajes nuestros casi iguales seguidos;
- 24 piden soporte y ninguna le llegó a Aylin;
- 21 con corchetes, «campo sin completar» o «marcador»;
- 20 donde el cliente escribió y nadie le contestó en más de 30 minutos.

## Los workflows de GHL siguen mandando las plantillas que había que apagar

Los mensajes nuestros que más se repiten en la muestra son plantillas de workflow, no del agente:

| Plantilla | Veces |
|---|---|
| «¡Solo por hoy…! …te llevas el curso de Cimentaciones BIM sin costo adicional… y el Tutor IA» | 127 |
| La misma, sin el Tutor IA | 108 |
| «Esperamos ser parte de su crecimiento profesional en un futuro…» (despedida) | 107 |
| «Últimos cupos… El día de hoy cerramos todos los cupos disponibles en promoción» | 100 |
| «…algo que muchos no saben 👇 la Especialización en Acero incluye un Tutor IA 24/7» | 98 |
| «¿Qué tal? Quería saber si lograste revisar la información…» | 87 |

Las urgencias falsas («solo por hoy», «hoy cerramos») estaban en la lista para apagar desde el 5-oct (`PLANTILLAS-GHL-A-CORREGIR.md`) y **siguen encendidas**. En las capturas de Dayana, a un mismo contacto le llegó «¡Solo por hoy!» dos veces con 40 minutos de diferencia, y otro recibió «Últimos cupos» sobre un curso que ya no se vende (Autodesk con IA). Es lo que se le pide a Ester en el mensaje del lunes.

## Las ventas (cobros reales)

Stripe y PayPal, del 9-sep al 8-oct (el archivo se actualiza solo el lunes a las 13:00 UTC):

| Semana | Cobros | Neto | Qué fue |
|---|---|---|---|
| 21–27 sep | 1 | USD 400 | Un cobro sin descripción |
| 28 sep–4 oct | 8 | USD 1.220 | 7 cuotas o matrículas del Máster (USD 160) y una reserva de USD 100 |
| 5–8 oct | 11 | USD 18.072 | Ver abajo |

La semana del 5 al 8 de octubre tiene:
- **un cobro único de USD 15.239,14 de una empresa constructora**: hay que confirmar si es de la Academy (formación para empresa) o de la consultoría DG antes de contarlo como venta de cursos;
- un cobro de USD 750 (el precio del módulo BIM Professional del Máster) y otro de USD 1.000;
- el resto, cuotas recurrentes del Máster (USD 160, 140, 113 y 30). Son ingreso recurrente, no captación nueva.

**En las tres semanas no hay ningún cobro de USD 225 ni de USD 199,99**: no aparece ninguna venta de la Especialización en Acero por Stripe ni por PayPal, aunque 41 conversaciones recibieron un enlace de pago. O los pagos de Acero entran por otra pasarela que no está en estos archivos, o los enlaces no se están pagando. Hay que confirmarlo con Ester.

## Qué hacer esta semana

1. **Patricio:** cargar la versión 2 del prompt y los enlaces de pago por país (Datafast, Stripe y PayPal).
2. **Ester:** apagar las plantillas de urgencia falsa y los mensajes repetidos, y cortar el flujo que deja pasar leads sin presupuesto.
3. **Confirmar por dónde entran los pagos de Acero.** Si existe otra pasarela (por ejemplo Datafast, o el checkout de la plataforma), sumarla a `fuentes/ingresos/` para que la auditoría vea las ventas.
4. **El lunes 19 se repite esta auditoría.** La meta para esa fecha:
   - más de 60 % de últimos mensajes con pregunta;
   - ninguna conversación con texto técnico filtrado;
   - menos de 20 con saludos repetidos;
   - todo pedido de soporte con la etiqueta `soporte-aylin`.
