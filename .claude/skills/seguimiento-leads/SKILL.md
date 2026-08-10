---
name: seguimiento-leads
description: |
  Revisa cómo van las secuencias automáticas de correo de los lead magnets
  (Zapatas→ACERO, Test→Máster, reactivación), cruza los resultados con el CRM
  y devuelve qué ajustar, anotándolo en RECOMENDACIONES.md.

  Usa este skill cuando Dayana diga: "seguimiento-leads", "cómo van los
  correos", "revisa las secuencias", "cómo va la nutrición de leads", "qué tal
  el seguimiento de los lead magnets", "cuántos respondieron los correos", o
  cuando pregunte si las secuencias de correo están funcionando.

  Se corre **una vez al mes**, o cuando se enciende una secuencia nueva.
---

# Skill: seguimiento-leads

Revisa las tres secuencias de correo que viven en `matriz-viral/seguimiento/`.

La regla de oro aquí: **la métrica que manda es cuántos respondieron**, no
cuántos abrieron. Una apertura no es una persona interesada; una respuesta sí.

---

## 0. Qué hay montado

| | Para quién | Destino | Archivo |
|---|---|---|---|
| **A** | Calculadora de Zapatas | Especialización en ACERO | `seguimiento/secuencia-A-zapatas-acero.md` |
| **B** | Test de Nivel BIM | Máster (por llamada) | `seguimiento/secuencia-B-test-master.md` |
| **C** | Lista dormida | Hub `/recursos` → re-segmentar | `seguimiento/secuencia-C-reactivacion.md` |

Las reglas y los umbrales están en `seguimiento/ESTRATEGIA.md`. El montaje, en
`seguimiento/MONTAJE-GHL.md`.

---

## 1. Sacar los datos

**De GHL, vía el conector de Windsor (solo lectura):**

- Contactos por tag: `seq-zapatas-acero`, `seq-test-master`,
  `seq-reactivacion`, `seq-completada`, `lead-caliente`, `email-frio`,
  `respondio-correo`
- **Oportunidades** por etapa y cuándo cambiaron: cuántas pasaron de
  "En nutrición" a "Interesado", y de ahí a "Llamada agendada"
- **Conversaciones**: cuántas respuestas de correo entraron en el periodo

**Lo que Windsor NO trae** y hay que pedirle a Dayana (captura de
Marketing → Emails → Statistics, por campaña):

- apertura y clic **correo por correo** (A1…A7, B1…B5, C1…C3)
- rebotes, spam y bajas

Sin eso no se puede decir dónde se cae la secuencia. **No estimarlo.**

---

## 2. Lo que hay que mirar

### 2.1 · Salud del envío — esto va primero

| Métrica | Umbral | Si falla |
|---|---|---|
| Rebotes | < 2 % | limpiar la lista antes de mandar nada más |
| **Spam** | **< 0,1 %** | 🚨 **parar todas las secuencias** |
| Bajas | < 0,5 % | normal en reactivación; vigilar en A y B |
| Apertura | ≥ 25 % | reescribir asuntos |
| Clic | ≥ 3 % | el correo se lee pero no convence |

Si la salud está mal, **no se sigue analizando nada más**: se para y se
arregla. Un dominio quemado tumba también los correos de facturación.

### 2.2 · Dónde se cae la secuencia

Poner apertura y clic de cada correo en una fila y buscar el escalón. El
patrón normal es que el correo 1 abra altísimo (llega cuando lo acaban de
pedir) y baje suave. **Una caída brusca en un correo concreto señala ese
correo**, no la secuencia entera.

Ojo con el correo de la oferta (A4, B3): si abre bien y no clica, el problema
es la oferta o el precio, no el asunto.

### 2.3 · Lo que de verdad importa

| Pregunta | Cómo se responde |
|---|---|
| ¿Cuántos **respondieron**? | tag `respondio-correo` + conversaciones |
| ¿Cuántas **llamadas** se agendaron? | oportunidades en "Llamada agendada" |
| ¿Cuántas **ventas** salieron? | oportunidades ganadas, **separando las reservas de $100** |
| ¿Cuántos quedaron **`email-frio`**? | si pasa del 40 % de la lista dormida, esa lista está muerta y hay que decirlo |

### 2.4 · Comparar con el mes anterior

Todo esto va contra la revisión anterior. Una secuencia que baja tres meses
seguidos se reescribe; no se le sube la frecuencia.

---

## 3. Cruzar con el resto

- **Contra la pauta** (`auditorias/`): un lead magnet que trae leads baratos
  pero cuya secuencia no convierte no es un lead magnet barato. Es un gasto.
- **Contra el contenido** (`matriz/`): si una pieza orgánica disparó registros,
  se anota — esa pieza vale más de lo que dicen sus views.
- **Contra `predijo-nivel-N`**: comparar lo que la gente creía con lo que
  responde. Esa distancia es material de contenido.

---

## 4. Lo que se entrega

**A Dayana**, en lenguaje llano:
1. ¿Vamos bien o mal? Una frase.
2. La salud del envío, primero. Si hay que parar algo, se dice arriba.
3. Cuántos respondieron y cuántas llamadas salieron. Esos dos números.
4. **Qué correo concreto hay que reescribir** y por qué.
5. Una decisión para el mes.

**Se anota en `matriz-viral/RECOMENDACIONES.md`:**
- una entrada nueva en «Historial» con la fecha y lo que se encontró
- las recomendaciones nuevas en la tabla de arriba, en 🔴
- mover a 🟢 o ⚫ lo que se resolvió, con motivo

---

## Reglas

- **Nunca inventar una métrica de correo.** Si Dayana no pasó las estadísticas,
  se dice qué falta y se analiza solo lo que sí llegó.
- **Responder pesa más que abrir.** Un mes con 40 respuestas y apertura del
  22 % es mejor que uno con apertura del 45 % y 3 respuestas.
- **Nunca subir la frecuencia de envío** para compensar malos resultados. Si no
  funciona, se reescribe.
- **Las reservas de $100 del Máster no son ventas.** Separarlas siempre.
- **El Máster no se cotiza por correo.** Si aparece un precio del Máster en una
  secuencia, es un error y hay que quitarlo.
- Si el spam pasa de 0,1 %, **se para todo** aunque el resto se vea bien.
