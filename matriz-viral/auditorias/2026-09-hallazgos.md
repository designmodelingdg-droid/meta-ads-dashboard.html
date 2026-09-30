# Auditoría de septiembre 2026 · lo que funcionó, lo que no y lo que está roto

> Datos al 30-sep-2026, 19:13 UTC:
> - publicaciones: Meta Graph API;
> - palabras, DM y clics: OpenReply;
> - leads y accesos: etiquetas de GHL;
> - historias: Graph API;
> - pauta: Meta Ads, del 31-ago al 29-sep;
> - dinero: Stripe y PayPal.
>
> Solo cuentas, ningún dato personal. Las tablas completas vienen debajo y en `2026-09-auditoria-mes.json`.

## Qué funcionó

1. **Dato de cálculo verificable** (post del 11-sep, cuantía mínima): 44.589 vistas, 146 comentarios, 715 guardados y **163 seguidores nuevos**. Es la mejor pieza del año.
   - Pedía **ACERO**, y esa palabra la contesta GHL. Hasta hoy **no se medía**. Ya se mide: el bot de ACERO suma 177 contactos en total (19 en los últimos 7 días).
2. **El tutorial «de un plano 2D a un modelo BIM»** (12-sep) no estaba en la matriz, y fue el segundo mejor:
   - 12.122 vistas, 99 comentarios, 402 guardados y 107 seguidores;
   - la palabra TUTORIAL mandó **47 DM** y trajo 10 clics reales (solo se cuentan clics limpios desde el 15-sep);
   - su parte 2 (22-sep) sacó 18 comentarios y 9 DM.
3. **Reels que piden un recurso con palabra:** la conversación sale 5 a 8 veces por encima de la mediana del mes, que son 2,66 comentarios por 1.000 vistas.
   - Guía Revit + ChatGPT (16-sep): 14,7 comentarios por cada 1.000 vistas.
   - Memoria de cálculo (25-sep): 13,6 por 1.000.
   - Memoria de cálculo (29-sep): 22,4 por 1.000, con 12 DM y 7 clics.
4. **Embudos que convierten, del bot al acceso:**
   - ZAPATA: 169 → 151 (89 %);
   - MEMORIA: 34 → 33;
   - la guía de Revit + ChatGPT funciona con la palabra **GUIA** en OpenReply (8 DM y 14 clics), no con CHATGPT.
5. **Cuenta:** de 80.347 a 80.875 seguidores (+528 en el mes). Cobrado neto del 31-ago al 29-sep: **$7.326,83** (Stripe $5.329,87 + PayPal $1.996,96).

## Qué no funcionó

1. **Los anuncios orgánicos del Tutor IA:**
   - post del 22-sep: 898 vistas y 0 comentarios;
   - reel del 23-sep: 0 comentarios;
   - reel del Diplomado del 24-sep: 2 comentarios y 1 DM.

   ⚠ **Alerta para octubre:** la semana 1 abre con el lanzamiento del Tutor IA del Diplomado (5 y 7-oct). Anunciar «ahora tiene tutor» no genera conversación. Hay que abrir con el problema (rebobinar la clase) y dejar el tutor como la solución, que es como están escritos el carrusel y el reel de octubre. Hay que medirlo el mismo lunes.
2. **Dynamo:**
   - el reel del 23-sep sacó 0 comentarios;
   - en OpenReply, 0 DM enviados y 4 fallidos;
   - en GHL, 6 al bot y 4 accesos.

   Es un recurso con poca tracción: queda fuera de los CTA de octubre.
3. **El carrusel de las 4 puertas** (23-sep, «la pieza del mes» en la matriz): 1.986 vistas, 2 comentarios y 1 DM de RUTA.
4. **Posts sin gancho ni palabra** (3, 7 y 29-sep): 0 a 2 comentarios.
5. **Las 3 campañas de pauta «LEAD MAGNETS»:** $77 gastados, 0 leads de formulario y 7 conversaciones. Se apagan o se rehacen con el anuncio del dato de cálculo.
6. **NIVEL** (Test de Nivel → Máster): solo 2 personas la pidieron en el mes. *Corregido el 30-sep:* el «0 accesos» era un error de medición, no de GHL (ver «Roto», punto 5). El problema real es de volumen: casi nadie la pidió.

## Qué está roto (arreglar antes de publicar en octubre)

1. **MEMORIA la escuchan tres automatizaciones:** dos campañas de OpenReply y el workflow de GHL.
   - 30 DM fallaron el 29 y 30-sep con «no eres el dueño de la conversación»: la primera que contesta se queda con el hilo y las otras fallan.
   - GHL registró 34 contactos, así que la mayoría probablemente sí recibió el recurso, pero no hay forma de saberlo persona por persona.
   - **Regla nueva: una palabra, una sola automatización.** Si la palabra tiene embudo en GHL (ZAPATA, ACERO, NIVEL, MEMORIA, DYNAMO, COTIZA), se pausa su campaña en OpenReply, o al revés, pero nunca las dos.
2. **DYNAMO**, el mismo choque: OpenReply falla 4 de 4 porque GHL contesta primero.
3. **BIM e IA como palabra de un recurso** (checklist de Navisworks): 3 fallidos de 5. BIM e IA son las palabras del bot de ventas del Máster, así que no se usan para recursos.
4. **ACERO: de 174 leads, solo 43 llegan al acceso (25 %)**, cuando ZAPATA llega al 89 %.
   - *Revisado en GHL el 30-sep:* el flujo funciona. El workflow «Comentario ACERO» manda al enlace correcto y el formulario pone `acceso-verificacion`.
   - La caída es de gente que recibe el DM y no llena el formulario. Además, el DM de Instagram solo se entrega dentro de las 24 h del comentario.
   - No está roto, **convierte poco**. La tarea es acortar el formulario y sumar un recordatorio. Octubre pide ACERO en 6 piezas.
5. ~~NIVEL no entrega acceso~~ **Error de medición, corregido el 30-sep.**
   - El flujo funciona: la rama TEST NIVEL pone `acceso-nivelbim`, y el embudo contaba `acceso-test-nivel`.
   - Ya se cuenta la etiqueta correcta en `embudo_leadmagnets.py`.
6. **En GHL siguen publicados dos workflows de accesos:** «✅ OLD Acceso y Descarga PDF Recursos Gratis» (61 inscritos) y el NEW. Pueden estar mandando el acceso dos veces. Hay que revisar y despublicar el OLD.
7. **BIM e IA ya las contesta GHL** con los workflows GENERICO (Instagram y Facebook/TikTok). Por eso chocaron las campañas de OpenReply que usaban BIM/IA para un recurso (el checklist de Navisworks).
8. **Las automatizaciones del repositorio estuvieron paradas del 27 al 30-sep**, por la suspensión de la cuenta de GitHub.
   - Las historias del 26 al 28-sep no se midieron y ya no se pueden recuperar: la API las borra a las 24 h.
   - Se relanzaron a mano el 30-sep. Hay que confirmar que las programadas vuelven solas: la de historias corre cada 4 h, a los :17.

## Qué cambia en la matriz de octubre por esta auditoría

**Ya está aplicado en `calendario-octubre.json`**, y lo muestran el artefacto, el Word y el JSON de la app:
- 4 reglas nuevas del mes;
- la decisión de pauta n.º 7;
- las notas de ZAPATA, ACERO, NIVEL y MEMORIA;
- DYNAMO retirada;
- 5 tareas nuevas del checklist;
- las notas de medición en las piezas del tutor;
- las destacadas;
- el bloque `auditoria_previa`.

`verificar_matriz_mes.py` comprueba además que cada palabra que pide el mes la contesta una sola automatización.


- Palabras de octubre: NIVEL, ACERO, ZAPATA, MEMORIA, COTIZA y DIPLOMADO, **cada una con una sola automatización**.
- **COTIZA** se monta en **una** herramienta. Hoy tiene la respuesta de Facebook en GHL; en Instagram va OpenReply o GHL, no las dos.
- NIVEL y ACERO ya están revisados (30-sep): funcionan. En ACERO hay que subir la conversión del DM al formulario.
- El formato ganador se repite: un dato verificable y un tutorial paso a paso con palabra (los dos mejores del mes).
- Los anuncios de producto («ahora tiene X») no van solos: siempre llevan detrás un problema.
