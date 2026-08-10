# Montaje en GoHighLevel — secuencias de seguimiento

Guía clic a clic. La puede seguir Dayana o el Claude del navegador.
**Orden: 0 → 1 → 2 → 3 → 4.** El paso 5 (encender) va al final y por partes.

---

## Paso 0 · Antes de tocar nada

**0.1 · Comprobar el dominio de envío.**
Settings → Email Services → Dedicated Domain. Tiene que estar verificado con
**SPF, DKIM y DMARC en verde**. Ya lo está (Dayana confirma que las campañas
llegan bien), pero se mira igual: si alguno se cayó, se arregla antes que nada.

**0.2 · Limpiar la lista.**
Contacts → filtrar por `Email Status = Bounced` o `Unsubscribed` → marcarlos
para excluirlos de los envíos. Cada correo a una dirección muerta cuenta en
contra de la reputación del dominio.

**0.3 · Crear las etiquetas.**
Settings → Tags → New, una por una:

```
seq-zapatas-acero    seq-test-master    seq-reactivacion
seq-completada       lead-caliente      email-frio
respondio-correo
```

**0.4 · Confirmar las etapas del pipeline.**
Opportunities → Pipelines. Tienen que existir, en este orden:

```
Nuevo lead → En nutrición → Interesado → Llamada agendada
```

Si tienen otro nombre, **no se renombran** (rompería reportes viejos): se
anotan los nombres reales aquí abajo y se usan esos en los workflows.

> Nombres reales en la cuenta: _______________________________________

---

## Paso 1 · Guardar la plantilla de correo

1. Marketing → **Emails** → New → **Code / HTML Editor**
2. Pegar completo `matriz-viral/seguimiento/plantilla-email.html`
3. Guardar como plantilla con el nombre **`DMA · Base secuencias`**
4. **Comprobar el peso**: tiene que quedar por debajo de **102 KB**. Si GHL
   añade cosas y se pasa, quitar imágenes — nunca meter base64.
5. Mandarse una prueba a uno mismo y abrirla **en Gmail del celular**. Es donde
   Gmail recorta y donde se ve si el botón sobrevive.

Para cada correo de las secuencias: duplicar esta plantilla y reemplazar solo
`[[TITULO]]`, `[[CUERPO]]`, `[[TEXTO_BOTON]]`, `[[ENLACE_BOTON]]` y `[[PD]]`.

**Nombrar los correos así**, para no perderse después:
`A1-entrega` · `A2-error-zapata` · `A3-puente` · `A4-oferta-acero` ·
`A5-objecion` · `A6-testimonios` · `A7-cierre` · `B1…B5` · `C1…C3`.

---

## Paso 2 · Workflow A — Zapatas → ACERO

Automation → Workflows → **New** → Start from Scratch.
Nombre: **`SEQ-A · Zapatas → ACERO`**

**Disparador (Trigger):**
`Tag Added` → tag `lead-calculadora-zapatas`

**Acciones, en orden:**

| # | Acción | Configuración |
|---|---|---|
| 1 | Add Tag | `seq-zapatas-acero` |
| 2 | Update Opportunity | etapa → **En nutrición** |
| 3 | Send Email | `A1-entrega` |
| 4 | Wait | 2 días · **entre 9:00 y 11:00, hora del contacto** |
| 5 | Send Email | `A2-error-zapata` |
| 6 | Wait | 2 días · misma ventana |
| 7 | Send Email | `A3-puente` |
| 8 | Wait | 3 días |
| 9 | Send Email | `A4-oferta-acero` |
| 10 | Wait | 2 días |
| 11 | Send Email | `A5-objecion` |
| 12 | Wait | 3 días |
| 13 | Send Email | `A6-testimonios` |
| 14 | Wait | 2 días |
| 15 | Send Email | `A7-cierre` |
| 16 | Add Tag | `seq-completada` |
| 17 | Remove Tag | `seq-zapatas-acero` |

**Ventana horaria:** en cada Wait, activar *"Wait until a specific window"* →
9:00–11:00. Sin esto los correos salen de madrugada y la apertura se cae.

**Las 4 salidas (Goals / Events):**
Se configuran en Settings del workflow, no como pasos:

| Evento | Qué hace |
|---|---|
| **Email Replied** | Add tag `respondio-correo` → **Remove from workflow** → notificar a Dayana |
| **Appointment Booked** | Update Opportunity → **Llamada agendada** → Remove from workflow |
| **Unsubscribed** | Remove from workflow |
| **Opportunity ganada** | Remove from workflow |

**Regla de "Interesado":**
En el correo `A4-oferta-acero`, sobre el botón principal, poner la acción
condicional:
`If/Else → Email Link Clicked (A4)` → **Add tag `lead-caliente`** +
**Update Opportunity → Interesado**.

**Reglas del workflow (Settings):**
- ✅ *Allow re-entry*: **NO**. Que nadie reciba la secuencia dos veces.
- ✅ *Stop on response*: **SÍ**.

---

## Paso 3 · Workflow B — Test → Máster

Nombre: **`SEQ-B · Test de Nivel → Máster`**
**Disparador:** `Tag Added` → `lead-test-nivel-bim`

| # | Acción | Configuración |
|---|---|---|
| 1 | Add Tag | `seq-test-master` |
| 2 | Update Opportunity | **En nutrición** |
| 3 | Send Email | `B1-entrega` |
| 4 | Wait | 2 días · 9:00–11:00 |
| 5 | **If/Else** | ver abajo |
| 6 | Wait | 3 días |
| 7 | Send Email | `B3-salto` |
| 8 | Wait | 3 días |
| 9 | Send Email | `B4-microcredenciales` |
| 10 | Wait | 4 días |
| 11 | Send Email | `B5-cierre` |
| 12 | Add Tag | `seq-completada` |
| 13 | Remove Tag | `seq-test-master` |

**El If/Else del paso 5** — tres versiones del correo B2, mismo cuerpo,
distinta apertura (están escritas en `secuencia-B-test-master.md`):

```
¿Tiene tag predijo-nivel-1 o predijo-nivel-2?  → enviar B2-bajo
¿Tiene tag predijo-nivel-3 o predijo-nivel-4?  → enviar B2-alto
En cualquier otro caso                          → enviar B2-neutro
```

**Interesado:** clic en el botón de `B3-salto` → `lead-caliente` + etapa
**Interesado**.

**Salidas:** las mismas cuatro del workflow A.

---

## Paso 4 · Workflow C — Reactivación

Nombre: **`SEQ-C · Reactivación lista dormida`**
**Disparador:** `Tag Added` → `seq-reactivacion` (se pone a mano en la carga)

| # | Acción | Configuración |
|---|---|---|
| 1 | Send Email | `C1-hub` |
| 2 | Wait | 4 días · 9:00–11:00 |
| 3 | Send Email | `C2-test` |
| 4 | Wait | 4 días |
| 5 | Send Email | `C3-cierre` |
| 6 | Wait | 2 días |
| 7 | **If/Else** | ¿abrió alguno de los 3? |
| 7a | → **Sí** | Add tag `seq-completada` |
| 7b | → **No** | Add tag **`email-frio`** + quitar de envíos |
| 8 | Remove Tag | `seq-reactivacion` |

**Salida extra, solo en este workflow:**
`Tag Added: lead-test-nivel-bim` → **Remove from workflow**.
Quien hace el test pasa a la secuencia B y no debe recibir las dos.

### 4.1 · Cargar los contactos por lotes

**No se etiquetan los 1.999 de una vez.** Contacts → filtro
(ebook / guía / AI PRO / cursos, con correo válido) → ordenar por fecha →
seleccionar y añadir el tag `seq-reactivacion` así:

| Día | Cuántos |
|---|---|
| 1 | 400 |
| 2 | 400 |
| 3 | 400 |
| 4 | 400 |
| 5 | los ~399 que queden |

Si GHL ofrece **"Batch Actions"** con límite diario, se usa eso y se hace en un
solo movimiento. Es lo mismo.

**Entre lote y lote se mira el panel** (paso 5.3). Si los rebotes pasan de 2 %
o el spam de 0,1 %, **se para** y no se carga el lote siguiente.

---

## Paso 5 · Encender (y en qué orden)

### 5.1 · Prueba en seco — obligatoria

1. Duplicar el workflow A → `SEQ-A · PRUEBA`
2. Cambiar **todos los Wait a 2 minutos**
3. Meter el contacto `prueba+test@dgdesignmodeling.com`
4. Ver llegar los 7 correos. Comprobar en cada uno:
   - se ve bien **en Gmail del celular**
   - `{{contact.first_name}}` sale con el nombre, no vacío ni con las llaves
   - el botón lleva a donde debe
   - el enlace de baja funciona
5. Comprobar que la oportunidad se movió de etapa sola
6. Responder uno de los correos → confirmar que **sale del workflow**
7. **Borrar el workflow de prueba**

### 5.2 · Encendido escalonado

| Cuándo | Qué |
|---|---|
| Día 1 | Encender **solo A** (199 contactos) |
| Día 3 | Mirar el panel. Si está en verde → encender **B** (26) |
| Día 5 | Si sigue verde → primer lote de **C** (400) |
| Días 6-9 | Un lote diario, mirando el panel cada día |

### 5.3 · El panel

Marketing → Emails → Statistics, por campaña.

| Métrica | Meta | Si falla |
|---|---|---|
| Apertura | ≥ 25 % | reescribir asuntos |
| Clic | ≥ 3 % | el botón no convence |
| Rebote | **< 2 %** | 🚨 parar y limpiar la lista |
| Spam | **< 0,1 %** | 🚨 **parar todo** |
| Baja | < 0,5 % | normal en reactivación, vigilar |

---

## Lo que hay que llenar antes (no está inventado a propósito)

| Marcador | Dónde | Qué es |
|---|---|---|
| `[ENLACE ACERO]` | A4, A5, A6, A7 | URL de la página de venta de ACERO |
| `[PRECIO ACERO]` | A4 | precio y forma de pago |
| `[FECHA INICIO ACERO]` | A4, A7 | próxima cohorte (si no hay, usar el **A7 alternativo**) |
| `[HORAS/SEMANA]` | A5 | carga semanal real (si no se sabe, borrar la línea) |
| `[TESTIMONIO 1]` `[TESTIMONIO 2]` | A6 | dos casos **reales** de la página de testimonios |

---

## Errores que ya conocemos y hay que evitar

1. **Plantilla pesada.** La del skill `dma-email-campaign` pesa ~860 KB por el
   base64. Gmail recorta a 102 KB y se come el botón. Por eso existe
   `plantilla-email.html`.
2. **Waits sin ventana horaria.** Salen de madrugada; la apertura se desploma.
3. **Re-entry activado.** La misma persona recibe la secuencia dos veces y se
   da de baja.
4. **Cargar los 2.000 de golpe.** Pico de rebotes → el dominio calentado se
   quema en un día.
5. **Prometer entrega por WhatsApp.** Ese workflow no existe. Todo se entrega
   por enlace en el mismo correo.
6. **Mandar los 3 correos de C a quien ya hizo el test.** Por eso está la
   salida por tag del paso 4.
