# Pack starter de Dynamo — montaje en GoHighLevel

Para **Ester y Aylin**. Construido y probado; falta conectarlo al CRM.

```
Landing   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/pack-dynamo/
Gracias   …/pack-dynamo/gracias-agenda.html
La guía   …/pack-dynamo/guia.html?acceso=dm2026
El ZIP    …/pack-dynamo/Pack-Dynamo-Starter-DMA.zip
```

**Palabra clave: `DYNAMO`** · Etiquetas: `lead-dynamo` · `origen-bot-DYNAMO`

---

## ⚠️ ANTES DE PUBLICAR EL CTA — hay que correr los 5 scripts en Revit

La matriz ya lo decía: *«necesita más producción que los otros dos porque hay
que probar cada script»*. Sigue siendo cierto y no lo he podido cerrar.

**Lo que sí está comprobado desde aquí:**

- Los cinco tienen **sintaxis Python válida**.
- Ninguno usa `unicode()`, así que corren igual en IronPython 2 y en CPython 3
  (Revit 2023 en adelante). Este era un fallo real y estaba en el script 01.
- Las llamadas a la API existen y están documentadas: `Document.GetWarnings()`,
  `FailureMessage.GetDescriptionText()` / `GetFailingElements()` / `GetSeverity()`,
  `View.GetPlacementOnSheetStatus()`, `Parameter.StorageType`. Verificado contra
  la documentación oficial de Autodesk, no de memoria.
- La lógica que no depende de Revit está probada con casos:
  `python3 pack-dynamo/prueba/logica.py` (escapado de CSV y agrupamiento de
  duplicados, incluido el caso de 5 mm que NO debe agrupar).

**Lo que NO está comprobado, y hay que hacerlo abriendo Revit:**

| Script | Qué hay que ver |
|---|---|
| 01 · Advertencias | Que el CSV salga y que Excel abra los acentos bien. |
| 02 · Duplicados | Duplicar un elemento a propósito y ver si lo encuentra. |
| 03 · Renombrar | **El simulacro primero.** Que la lista «antes → después» sea correcta. |
| 04 · Vistas sin hoja | Que no liste plantillas ni tablas. |
| 05 · Parámetro | **El simulacro primero.** Que el conteo de «sin parámetro» cuadre. |

Los dos que escriben (03 y 05) traen el simulacro **encendido por defecto**, así
que la primera ejecución no puede romper nada aunque falle.

Hasta que alguien corra los cinco, **el CTA no sale**. Es semana 3, hay tiempo.
Si llega la fecha sin probarlos, la matriz ya tiene reemplazo previsto.

---

## PASO 1 — Formulario nativo

GHL → **Sites → Forms → New Form**. `Pack Dynamo`.

Campos: nombre, correo, WhatsApp, y el desplegable **«¿Has usado Dynamo antes?»**
con estas opciones: *Nunca lo he abierto · Lo abrí y me perdí · Uso scripts de
otros · Escribo los míos · Automatizo para todo el equipo*.

**Redirect URL:**

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/pack-dynamo/gracias-agenda.html?acceso=dm2026
```

Pega la URL del formulario en `index.html`, en `GHL_FORM_IFRAME_URL`.

## PASO 2 — Etiquetas

`lead-dynamo` y `origen-bot-DYNAMO`.

## PASO 3 — El bot, con DOS ramas separadas

Palabra `DYNAMO`. **Rama Instagram → DM de Instagram. Rama Facebook → DM de
Messenger. Nunca una acción compartida.** Y la respuesta pública lleva siempre
el enlace visible:

> Te dejo el pack aquí 👇 cinco scripts de Dynamo comentados por dentro, tres
> de ellos solo leen y no tocan tu modelo: [enlace]

## PASO 4 — La secuencia

| | Cuándo | Qué dice |
|---|---|---|
| Correo 1 | Inmediato | Los enlaces otra vez: guía y ZIP. |
| Correo 2 | 48 h | El script 02 y por qué los duplicados no se ven hasta que se presupuesta. |
| Correo 3 | Día 5 | Puente al módulo BIM + IA. Sin precio, con «agenda una cita». |

## PASO 5 — Notificación al setter

Con la respuesta de perfil. **«Nunca lo he abierto» y «automatizo para todo el
equipo» son dos conversaciones distintas**: al primero se le vende el módulo
completo, al segundo le sobra la mitad y hay que ir directo a lo de decidir qué
se automatiza en el flujo del equipo.

---

## Comprobar antes de publicar

1. Comentar `DYNAMO` **en Instagram** → llega el DM.
2. Comentar `DYNAMO` **en la copia de Facebook** → llega el DM por Messenger.
3. La respuesta pública incluye el enlace visible.
4. El enlace abre la landing **en teléfono**.
5. Enviar el formulario → redirige a gracias.
6. El botón de la guía abre **sin pedir registro**.
7. **El botón del ZIP descarga y el ZIP abre con los 5 .py dentro.**
8. **Los 5 scripts corren en Revit** (la tabla de arriba).
9. El contacto aparece en el CRM con sus dos etiquetas.
10. Borrar los contactos de prueba.

El punto 8 es el que bloquea el CTA. Los demás se pueden cerrar hoy.
