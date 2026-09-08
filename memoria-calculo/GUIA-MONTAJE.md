# Guía + plantilla de memoria de cálculo — montaje en GoHighLevel

Para **Ester y Aylin**. Construido y probado; falta conectarlo al CRM.

```
Landing   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/memoria-calculo/
Gracias   …/memoria-calculo/gracias-agenda.html
La guía   …/memoria-calculo/guia.html?acceso=dm2026
Word      …/memoria-calculo/Plantilla-Memoria-de-Calculo-DMA.docx
Excel     …/memoria-calculo/Resumen-Verificaciones-DMA.xlsx
```

**Palabra clave: `MEMORIA`** · Etiquetas: `lead-memoria-calculo` · `origen-bot-MEMORIA`

---

## La estructura ya se cruzó contra una memoria real

**8 de septiembre.** Dayana pasó una memoria de proyecto tipo de Robot Structural
Analysis, de las que usa Gabriel, y la estructura de la guía se ajustó contra
ella. Lo que cambió:

| Cambio | Por qué |
|---|---|
| **De 13 a 12 secciones**, en otro orden | La memoria real pone la normativa después de describir el sistema, no antes |
| **Nueva: «Proceso de cálculo»** | La cadena ubicación → amenaza sísmica → uso → importancia → sistema. Es lo que más rápido orienta al revisor |
| **Nueva: «Cálculo del cortante basal»** | En Ecuador el revisor la busca por su nombre. Estaba escondida dentro de «resultados» |
| **Nueva: «Análisis modal»** | Períodos y participación de masas: es lo que justifica que el modelo dinámico valga |
| «Estados límite de servicio» → **«Limitación de daños»** | Es el nombre que usa la NEC y el que busca un revisor ecuatoriano |
| «Registro profesional» → **«Registro Senescyt»** | Es el dato que identifica al responsable en Ecuador |
| Portada con **área y n.º de niveles** | Lo primero que mira el revisor para ubicarse |
| **Nueva: convención de figuras y tablas** | La memoria real se apoya en 48 figuras. Sin sitio para ellas, la plantilla no servía |
| **Nueva devolución 6: el documento se contradice** | Ver abajo |

### La devolución nueva, y de dónde salió

Al leer la memoria real aparecieron cuatro incoherencias internas — restos de
haberla armado partiendo de otra anterior, que es lo normal:

- El objetivo y las conclusiones hablan de **«perfiles de acero»** en una
  estructura de **hormigón armado**.
- Un pie de tabla cita **un software distinto** del que se usó en todo el resto.
- El **tipo de suelo** es «D» en el texto y «E» en la tabla de coeficientes.
- La fila «tipo de estructura» de la tabla del cortante basal dice **«acero
  estructural»** en un edificio de hormigón: conviene comprobar que Ct y α
  correspondan al sistema real, porque de esa fila dependen.

Ninguna es un error de cálculo. Las cuatro se encuentran con tres búsquedas en
el documento. Por eso ahora la guía tiene una sexta devolución dedicada a esto,
y la plantilla abre su comprobación final con ellas.

**Estas incoherencias NO se publican con atribución.** La guía las cuenta en
abstracto, sin decir de qué documento salieron.

## Sigue pendiente: el visto bueno de Gabriel

La estructura ya no es teórica, pero **una cosa es cruzarla y otra que él la
apruebe.** Antes de que salga el CTA conviene que la mire y diga si:

1. Falta alguna sección para el tipo de memoria que entrega.
2. El orden es el que usa, o hay una razón práctica para otro.
3. La plantilla no induce a omitir nada.

Si llega la fecha sin ese visto bueno, la matriz ya tiene el reemplazo previsto:
el CTA cambia a las 5 Verificaciones de Acero, que ya existe.

## Lo que este recurso NO hace, y por qué

Está escrito así a propósito, y conviene que el equipo lo repita igual:

- **No calcula nada.** Es estructura documental: cómo se organiza y se justifica
  la memoria. Los valores y los criterios son del ingeniero.
- **No transcribe ninguna cifra normativa.** Se remite siempre a la norma vigente
  aplicable. Es la misma regla del tutor de IA.
- **La hoja de Excel calcula un ratio y marca CUMPLE / NO CUMPLE.** Nada más.
  No conoce ninguna norma: el límite admisible lo escribe el usuario. En el
  momento en que la hoja propusiera una sección o un valor, tendría que responder
  por ese número.

Esa contención es justamente lo que hace que podamos repartirlo. Un recurso que
propusiera valores de diseño no lo podríamos firmar.

---

## PASO 1 — El formulario nativo

GHL → **Sites → Forms → New Form**. Nómbralo `Memoria de cálculo`.

| Campo | Tipo | Obligatorio |
|---|---|---|
| Nombre y apellido | Texto | Sí |
| Correo | Email | Sí |
| WhatsApp | Teléfono | No |
| ¿Cada cuánto entregas memorias de cálculo? | Desplegable | Sí |

Opciones: *Varias al mes · Algunas al año · Voy a entregar la primera · Las
reviso, no las escribo · Todavía no, pero quiero aprender*.

**Redirect URL** al terminar:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/memoria-calculo/gracias-agenda.html?acceso=dm2026
```

Pega la URL del formulario en `index.html`, en `GHL_FORM_IFRAME_URL`.

## PASO 2 — Las dos etiquetas

`lead-memoria-calculo` (enciende la secuencia) y `origen-bot-MEMORIA`.

## PASO 3 — El bot, con DOS ramas separadas

Disparador de comentario filtrado por `MEMORIA`. **Rama Instagram → DM de
Instagram. Rama Facebook → DM de Messenger. Nunca una acción compartida** — es
lo que costó 35 leads en julio, y falla en silencio porque la respuesta pública
sí sale siempre.

La respuesta pública lleva **siempre el enlace visible**:

> Te la dejo aquí 👇 las 13 secciones de una memoria que se sostiene ante
> revisión, con la plantilla en Word y la hoja de verificaciones: [enlace]

## PASO 4 — La secuencia, con el puente que depende del perfil

| | Cuándo | Qué dice |
|---|---|---|
| Correo 1 | Inmediato | Los enlaces otra vez: guía, Word y Excel. |
| Correo 2 | 48 h | El error 3 (hipótesis listadas, no justificadas) y por qué es el que delata una memoria reciclada. |
| Correo 3 | Día 5 | **El puente cambia según lo que contestó.** |

**El correo 3, según el perfil:**

- *Varias al mes* / *Algunas al año* / *Las reviso* → **ACERO, $225, con el tutor
  de IA incluido.** Aquí el precio **sí** va: es alguien que ya trabaja y para
  quien $225 es una decisión pequeña.
- *Voy a entregar la primera* / *Todavía no* → **módulo BIM Professional**, sin
  precio, con «agenda una cita».

Esta bifurcación es la razón de que la pregunta de perfil esté en el formulario.
Si todos reciben el mismo correo 3, la pregunta sobra.

## PASO 5 — Notificación al setter

Con el nombre del recurso **y la respuesta de perfil**. Quien entrega varias
memorias al mes y quien va a entregar la primera no se trabajan igual, y esa
diferencia se pierde si todos caen en la misma bandeja.

---

## Comprobar antes de publicar

1. Comentar `MEMORIA` **en Instagram** → llega el DM.
2. Comentar `MEMORIA` **en la copia de Facebook** → llega el DM por Messenger.
3. La respuesta pública incluye el enlace visible.
4. El enlace abre la landing **en teléfono**.
5. Enviar el formulario → redirige a gracias.
6. El botón de la guía abre **sin pedir registro**.
7. **El botón de Word descarga un .docx que abre en Word.**
8. **El botón de Excel descarga un .xlsx y las fórmulas calculan el ratio.**
9. El contacto aparece en el CRM con sus dos etiquetas.
10. Borrar los contactos de prueba.

> **Los puntos 7 y 8 hay que hacerlos a mano.** Los dos ficheros se generan desde
> `scripts/build_memoria_plantilla.js` y `scripts/build_memoria_excel.py`, y
> están comprobados en cuanto a estructura y lógica — pero **en este entorno no
> hay forma de abrirlos en Word ni en Excel de verdad.** La primera vez que
> alguien los abra, que avise si algo se ve raro.
