# Calculadora de Zapatas — guía de montaje del lead magnet

Lead magnet de Design Modeling Academy: landing de captura + calculadora de
zapata aislada, replicando el paso a paso de la hoja Excel del curso de
Diseño de Cimentaciones (hoja `Z-1`).

## Qué contiene esta carpeta

| Archivo | Qué es |
|---|---|
| `index.html` | **Landing de captura**: explica cómo se calcula la zapata y cómo se usa la app, y pide nombre, correo, WhatsApp y pregunta de calificación ("¿A qué te dedicas?"). Al enviar, redirige a la calculadora. **El Inbound Webhook de GHL ya está conectado.** |
| `app.html` | **La calculadora** (autocontenida, sin servidores). Incluye un "candado": si alguien llega sin registrarse, le muestra un aviso y lo manda a la landing. |
| `ghl-landing.html` | **La misma landing lista para GoHighLevel**: pega el archivo completo en un elemento *Custom Code* de tu funnel (sección de ancho completo). Se genera desde `index.html` con URLs absolutas. |
| `img/vista-calculadora.png` | Captura de la calculadora usada en la sección "Así se usa". |
| `GUIA-MONTAJE.md` | Esta guía. |

## URLs públicas (GitHub Pages)

El repositorio ya publica en GitHub Pages. Cuando este cambio se mergee a la
rama por defecto (o se ejecute la Action a mano), quedará disponible en:

- Landing: `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/`
- Calculadora: `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/app.html`

Ese es el enlace que compartes en anuncios, bio de Instagram o WhatsApp.
(Si prefieres un dominio propio, puedes montarla también dentro de GHL — ver
la opción C más abajo.)

## Conectar los leads a GoHighLevel

En `index.html`, al inicio del `<script>` final, hay dos constantes. Elige
**una** de estas vías:

### Opción A — Inbound Webhook (YA CONECTADA)

El webhook del workflow "Webhook Entrante" ya está pegado en
`GHL_WEBHOOK_URL` de `index.html` (y por tanto en `ghl-landing.html`).
Pasos que quedan en GHL, una sola vez:

1. Con el disparador abierto, pulsa **"Recuperar solicitudes de muestra"** —
   ya se envió un registro de prueba con el JSON
   (`nombre`, `email`, `telefono`, `perfil`, `fuente`, `pagina`).
2. Mapea los campos en la acción **Create/Update Contact**
   (nombre → Full Name, email → Email, telefono → Phone, perfil → campo
   personalizado), agrega una etiqueta tipo `lead-calculadora-zapatas`,
   **guarda el trigger y publica el workflow**.
3. Encadena tu secuencia de seguimiento (WhatsApp/email del bot de ventas).

### Opción B — Formulario nativo de GHL

1. En GHL: **Sites → Forms → Builder**, crea el formulario con los mismos campos.
2. En las opciones del formulario, configura **On Submit → Redirect** a la URL
   de la calculadora **incluyendo el token**:
   `…/calculadora-zapatas/app.html?acceso=dm2026`
3. Copia la URL del embed (`https://api.leadconnectorhq.com/widget/form/XXXX`)
   y pégala en `GHL_FORM_IFRAME_URL` de `index.html`. El formulario nativo
   reemplaza automáticamente al formulario propio de la página.

### Opción C — Todo dentro del funnel de GHL

Si prefieres que todo viva en `funnel.dgdesignmodeling.com`:

1. Crea un funnel de 2 pasos en GHL.
2. **Paso 1**: landing con formulario nativo de GHL (puedes copiar los textos
   de `index.html`).
3. **Paso 2**: página con un elemento **Custom Code / HTML**, y pega dentro el
   contenido completo de `app.html` (es autocontenido). En `app.html` cambia
   `REQUIERE_REGISTRO = false`, porque el funnel ya obliga a pasar por el
   formulario del paso 1.

## El candado de acceso

- Token actual: `dm2026` (constante `TOKEN_ACCESO`, igual en `index.html` y `app.html`).
- Quien completa el formulario entra con `app.html?acceso=dm2026` y queda
  recordado en su navegador (localStorage).
- Para invalidar enlaces compartidos, cambia el token en ambos archivos.
- Para desactivar el candado por completo: `REQUIERE_REGISTRO = false` en `app.html`.

## Qué calcula la app (hoja Z-1 del Excel del curso)

1. Cargas PD/PV (directas o por metrados: `P = M·N·pisos·carga/1000`).
2. Esfuerzo neto del suelo: `σn = σt·10 − γm·hf − S/C/1000`.
3. Área requerida `Az = (PD+PV)/σn` y sugerencia de T×S (hoja CÁLCULO AUXILIAR).
4. Reacción última `Pu = 1.4·PD + 1.7·PV`, `Wnu = Pu/(T·S)`.
5. Peralte `d = h − 0.075` con botón que sugiere la h mínima que cumple.
6. Cortante en cada dirección: `φVc = 0.85·0.53·√f'c·ancho·d·10` vs `Vu = Wnu·ancho·(Lv−d)`.
7. Punzonamiento: tres límites `φVc1/φVc2/φVc3` (β, límite general y αs según
   posición de columna) vs `Vu = Pu − Wnu·m·n`.
8. Flexión en ambas direcciones con `w = 0.8475 − √(0.7182 − 1.695·Mu·10⁵/(0.9·f'c·b·d²))`,
   cuantía mínima 0.0018, y distribución de varillas (cantidad y espaciamiento).

Notas respecto al Excel:

- El cortante se verifica como `Vu ≤ φVc` en **ambas** direcciones (la hoja
  tenía esa celda incompleta y solo revisaba una dirección); en punzonamiento
  se compara `Vu ≤ mín(φVc)` directamente, el criterio estándar.
- Las verificaciones se recalculan en vivo y muestran `CUMPLE` / `VERIFICAR`
  igual que la hoja.

Los valores fueron verificados uno a uno contra la hoja `Z-1`
(Az = 9.1769 m², Wnu = 8.4632 t/m², φVc = 90.173 t, φVc punz. = 194.219 t,
Mu = 26.955 t·m, As = 24.8625 cm², etc.).
