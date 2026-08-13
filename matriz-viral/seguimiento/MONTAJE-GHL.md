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

## Paso 1b · 🚨 DÓNDE ESTÁN REALMENTE LOS LEADS

**Esto corrige el disparador de las secuencias. Léelo antes de montar nada.**

Los leads **ya están todos en un pipeline** que Dayana tiene funcionando. No hay
que crear nada nuevo — hay que engancharse a lo que ya existe.

| | |
|---|---|
| **Pipeline** | `qjXIsYXjqdWbge7bZCdT` — el de **INSTAGRAM – FACEBOOK** |
| **Etapa** | `eaa5097a-8317-4519-aae4-094471d8b26a` — **NUEVO LEAD MAGNET** |
| **Cuántos hay ahí** | **334 oportunidades**, todas en estado `open` |

### Qué hay exactamente en esa etapa

Comprobado contra el CRM el 11-ago-2026 (331 de los 334 caen en los últimos
120 días):

| Fuente | Cuántos | Nombre de la oportunidad | Va a |
|---|---|---|---|
| `Bot Zapatas IG/FB` | 106 | `Lead Zapatas - <usuario>` | **Secuencia A** |
| `Calculadora de Zapatas - Registro` | 78 | nombre de la persona | **Secuencia A** |
| `contacto-instagram` | 27 | `Lead Test BIM - <usuario>` | **Secuencia B** |
| `Test Nivel  IG/FB` | 10 | `Lead Test Nivel - <usuario>` | **Secuencia B** |
| *(sin fuente)* | 107 | nombre de la persona | **hay que mirarlos** |
| sueltos (ebook, módulo, Facebook) | 3 | varios | descartar |

**Total: ~184 de zapatas y ~37 del test.**

### ⚠️ Las cuatro trampas de este pipeline

Cualquiera de estas rompe el montaje en silencio:

1. **`Test Nivel  IG/FB` lleva DOS ESPACIOS** entre «Nivel» e «IG/FB». Un filtro
   con un solo espacio no encuentra a nadie y parece que no hay leads del test.
2. **El test entró con dos nombres distintos**: `Lead Test BIM` (27) y
   `Lead Test Nivel` (10). Filtrar solo por uno pierde a los otros.
3. **107 oportunidades no tienen fuente.** Si el filtro es solo por fuente, se
   quedan fuera un tercio de la etapa.
4. **Muchos vienen del bot de Instagram y NO TIENEN CORREO** — la oportunidad se
   llama con el usuario de IG (`Lead Zapatas - Mauricio_granados74`). De los 297
   contactos de zapatas, solo **199 tienen correo**. A los otros ~98 **no se les
   puede mandar esta secuencia**: hay que separarlos (ver paso 2c).

**Por eso el disparador NO es un tag, es la etapa del pipeline**, y el reparto a
la secuencia A o B se hace dentro del workflow con un If/Else.

---

## Paso 2 · Workflow A — Zapatas → ACERO

Automation → Workflows → **New** → Start from Scratch.
Nombre: **`SEQ-A · Zapatas → ACERO`**

**Disparador (Trigger):** `Opportunity Stage Changed`
- Pipeline: **INSTAGRAM – FACEBOOK** (`qjXIsYXjqdWbge7bZCdT`)
- Etapa: **NUEVO LEAD MAGNET** (`eaa5097a-8317-4519-aae4-094471d8b26a`)

**Y como primer paso, dos filtros en este orden** (antes de cualquier correo):

**Filtro 1 — ¿tiene correo?**
```
If/Else:  Email  is not empty
   → NO  →  Add tag `sin-correo-solo-dm`  →  END. No sigue.
   → SÍ  →  continúa
```

**Filtro 1b — ¿vino del bot o del formulario?**

Esto evita que la persona reciba el DM del bot y el correo diciendo lo mismo en
el mismo minuto. Es la diferencia entre un seguimiento y un acoso.

```
If/Else:  Opportunity Source  contains  "IG/FB"
   → SÍ (vino del bot)         →  WAIT 2 días  →  usar el correo A1-bot
   → NO (vino del formulario)  →  sin espera   →  usar el correo A1-web
```

**Por qué 2 días y no 10:** el bot ya hace su cadena de 3 DMs (inmediato, +3-4 h
y +1 día). A los 2 días esa cadena terminó y la ventana de 24 h de Meta está
cerrada — el correo entra justo cuando el bot se quedó sin poder hablar.

A los 10 días la persona ya no se acuerda de nosotros. Toda la ventaja de un
lead de lead magnet es que **acaba de levantar la mano**; esperar diez días es
tirar eso. Si aun así se prefieren los 10, se cambia el Wait y ya — pero queda
dicho que se va a notar en la apertura.

---

**Filtro 2 — ¿es de zapatas?** (con OR, para cubrir las tres formas de entrar)
```
If/Else, cualquiera de estas:
   Opportunity Name    contains  "Zapatas"
   Opportunity Source  contains  "Zapatas"
   Contact Tag         is        lead-calculadora-zapatas
   → SÍ  →  sigue la secuencia A
   → NO  →  END (lo recoge el workflow B)
```

> **Ojo:** «contains "Zapatas"» con Z mayúscula cubre tanto
> `Bot Zapatas IG/FB` como `Calculadora de Zapatas - Registro` y
> `Lead Zapatas - <usuario>`. Marca la opción **case-insensitive** si GHL la
> ofrece.

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

## Paso 2c · Los que NO tienen correo (~98 personas)

No es un caso raro: **es un tercio de la etapa.** Son los que entraron por el
bot de Instagram y solo dejaron su usuario.

A esos **no se les puede mandar la secuencia** — no hay a dónde. Lo que sí se
puede hacer, y hoy no se hace nada:

1. Quedan con tag **`sin-correo-solo-dm`** (lo pone el filtro 1).
2. Se les manda **un DM pidiendo el correo**, dentro de la ventana de 24 h de
   Meta si aún está abierta:

```
¡Hola! 👋 Te mandé la calculadora por aquí, pero se me queda corta la
conversación por DM.

¿Me pasas tu correo? Te mando el paso a paso completo de cómo usarla
sin que se te pierda entre los mensajes, y de paso te llegan las
herramientas nuevas cuando salen. Nada de spam. 🙌
```

3. Quien conteste con su correo → se le guarda en el contacto → **entra a la
   secuencia A automáticamente** (el filtro 1 ya deja de bloquearlo).

> **Esto es dinero que ya está pagado.** Son leads que costaron pauta y que hoy
> están muertos en el CRM porque nadie les pidió el correo. Recuperar aunque
> sea un tercio son ~30 personas más en la secuencia sin gastar un dólar.

---

## Paso 3 · Workflow B — Test → Máster

Nombre: **`SEQ-B · Test de Nivel → Máster`**

**Disparador:** el mismo que el A — `Opportunity Stage Changed`, pipeline
**INSTAGRAM – FACEBOOK**, etapa **NUEVO LEAD MAGNET**.

**Mismos dos filtros primero**, con la condición del test:

```
Filtro 1: Email is not empty  →  NO: tag `sin-correo-solo-dm` y END

Filtro 2, cualquiera de estas:
   Opportunity Name    contains  "Test"
   Opportunity Source  contains  "Test Nivel"
   Contact Tag         is        lead-test-nivel-bim
   → SÍ  →  sigue la secuencia B
   → NO  →  END
```

> **«contains "Test"» a secas, y es a propósito:** así entra tanto
> `Lead Test BIM` (27) como `Lead Test Nivel` (10). Y **no filtres por la
> fuente exacta `Test Nivel  IG/FB`** — lleva dos espacios y lo vas a escribir
> mal. Por eso la condición del nombre va primera.

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

## Paso 4c · 🔑 Meter a los 334 que YA están en la etapa

**Este es el punto de todo el montaje.** Los disparadores de arriba solo cogen a
los que entren **de ahora en adelante**. Las 334 personas que llevan meses
paradas en «NUEVO LEAD MAGNET» **no se enrolan solas** — hay que meterlas a
mano, una vez.

Se hace desde el módulo de Oportunidades, no desde Contactos:

1. **Opportunities** → seleccionar el pipeline **INSTAGRAM – FACEBOOK**
2. Filtrar por etapa **NUEVO LEAD MAGNET**
3. **Primero los de zapatas.** Filtro adicional:
   `Opportunity Name contains "Zapatas"` **o** `Source contains "Zapatas"`
   → seleccionar todos → **Add to Workflow** → `SEQ-A · Zapatas → ACERO`
4. **Después los del test.** Cambiar el filtro a
   `Opportunity Name contains "Test"`
   → seleccionar todos → **Add to Workflow** → `SEQ-B · Test de Nivel → Máster`
5. **Los ~107 sin fuente y sin nombre de lead**: son los que quedan cuando
   quitas los dos filtros anteriores. **No los metas a ciegas.** Ábrelos y mira
   de dónde vienen; lo más probable es que sean del formulario de la
   calculadora, en cuyo caso van a la A. Si no se puede saber, se dejan y se le
   pregunta a Dayana.

> ⚠️ **Los filtros de arriba se hacen con calma y se cuenta antes de enrolar.**
> Si un lead del test acaba en la secuencia de zapatas, recibe 7 correos sobre
> cimentaciones que no pidió. Eso no se puede deshacer.

### Y aquí sí hace falta el escalonado

Meter 334 personas de golpe a una secuencia es **exactamente** el pico de envío
que quema un dominio. Aunque sean menos que los 2.000 de la lista dormida,
llevan meses sin recibir nada nuestro — para los filtros son igual de fríos.

| Día | Qué enrolar |
|---|---|
| 1 | 50 de zapatas (los más recientes primero — se acuerdan de nosotros) |
| 2 | mirar el panel · si está verde, 100 más |
| 3 | los ~34 restantes de zapatas |
| 4 | los 37 del test, todos (son pocos) |

**Los más recientes primero** no es un detalle: quien descargó hace tres
semanas abre; quien descargó en mayo, no. Empezar por los que abren le enseña a
Gmail que nuestros correos se leen, y eso protege los envíos siguientes.

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

## Lo que hay que llenar antes

**Actualizado el 11-ago-2026: los datos de ACERO ya están puestos** (precio,
duración, modalidad, certificaciones y enlace de compra, del PDF oficial). Solo
quedan dos decisiones:

| Qué | Dónde | Decisión |
|---|---|---|
| **URL buena** | A4, A5, A7 | Se usó la de `clientclub`. En el PDF hay otras dos de `designmodelingacademy.com` — confirmar cuál es la canónica antes de encender |
| **Testimonios** | A6 | Los archivos son videos verticales; el correo no los reproduce. Por defecto enlaza a la página de testimonios. Ver las 3 opciones en el archivo de la secuencia |

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
