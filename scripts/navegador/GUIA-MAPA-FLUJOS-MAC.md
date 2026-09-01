# El mapa de flujos — se saca desde el Mac

**Para la sesión de Claude Code del Mac, con browser-harness.**
Esto no se puede correr desde GitHub Actions y no es un capricho: está
comprobado.

---

## Por qué no corre en Actions

Cinco corridas el 25-ago-2026. La última entró a **un solo** workflow y esperó
90 segundos anotando cada vez que la página crecía:

```
+2s · 37 car · Loading fresh data... Initializing...
SIN CARGAR (37 car · 1 marcos)      ← ~88 s después, sin crecer una sola vez
```

El texto creció **una vez**, a los dos segundos, y ahí se quedó. Eso no es
lento: **está atascado.** El constructor de workflows de GHL no termina de
arrancar en un navegador sin pantalla, y subir el tiempo de espera no lo
arregla. (Por el camino se diagnosticó que el texto estaba en un iframe. No lo
estaba: `marcos: 1`. Queda anotado para que nadie vuelva por ahí.)

En tu Chrome sí arranca, porque es un navegador normal con su sesión.

---

## Antes de empezar

Chrome cerrado del todo con `Cmd + Q` —no basta cerrar la ventana— y después:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

El detalle completo, y por qué esa puerta abierta alcanza todas tus pestañas,
está en [BROWSER-HARNESS.md](BROWSER-HARNESS.md).

---

## No son 148 — son 8

La cuenta tiene 148 workflows: 76 publicados y 72 en borrador. Recorrerlos
todos a mano es media tarde y casi todo lo que saldría no le sirve a nadie.

Los borradores no mandan nada, así que no se miran. Y de los publicados, estos
ocho son los que contestan preguntas que hoy están abiertas. Ese es el encargo.

---

**1 · Calculadora Zapatas - Acceso Membresía**  
**El molde.** Cómo se concede de verdad la membresía — es lo que hay que copiar para ACERO.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/c2321459-7d3e-4e69-99ed-247374a14761
```
<sub>`published` · última edición 2026-08-04</sub>

**2 · Test de Nivel BIM - Otorgar acceso**  
El segundo ejemplo de entrega, para contrastar que el molde es el molde y no una casualidad.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/b8099ad3-c452-47db-b5db-a04725a4c955
```
<sub>`published` · última edición 2026-08-04</sub>

**3 · Bot ZAPATA — IG/FB**  
El workflow de palabra. **La pregunta:** ¿tiene una acción de envío por Instagram y otra por Facebook, separadas? Ahí estuvo el fallo de julio.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/70a70198-d1f0-4f26-b4f9-81c8ca13f5b3
```
<sub>`published` · última edición 2026-08-17</sub>

**4 · Bot Nivel- Test  — IG/FB**  
Lo mismo, en el otro recurso. Si los dos tienen el mismo defecto, es el patrón y no un descuido.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/373de22a-b53b-4e3b-b696-8b5ef6a2552d
```
<sub>`published` · última edición 2026-08-10</sub>

**5 · ✅ Comentario IG-GENERICO (rutea por palabra BIM/IA)**  
**El de más riesgo.** Si se dispara con comentarios de *cualquier* publicación, es lo que mandó el temario de un curso de pago a quien pidió una guía gratis.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/8e0eeb83-95bd-4cdc-87eb-dca27c45952e
```
<sub>`published` · última edición 2026-08-14</sub>

**6 · ✅ Comentario Facebook/TikTok - GENERICO (rutea por palabra BIM/IA)**  
Su gemelo del otro lado.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/381695fd-5427-47fa-961c-4845459ad48b
```
<sub>`published` · última edición 2026-08-14</sub>

**7 · ✅ Acceso y Descarga PDF Recursos Gratis**  
Qué correo sale con los recursos gratis, y si el enlace que lleva sigue vivo después del renombrado.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/cf3e5cfd-4d3a-46af-87ad-4d80ebd1ba8c
```
<sub>`published` · última edición 2026-08-20</sub>

**8 · ✅ Seguimientos 1,2,3 y 4 Especialización Acero**  
Los cuatro correos de ACERO que ya existen — para no escribir de nuevo lo que ya está escrito.

```
https://app.gohighlevel.com/v2/location/nkKbOarn5IwHeMv48uY9/automation/workflows/87fe06b9-861b-4226-8b97-f79aa95c7109
```
<sub>`published` · última edición 2026-08-24</sub>

---

## El encargo, para pegar tal cual

```text
Tengo Chrome abierto con --remote-debugging-port=9222 y la sesión de
GoHighLevel iniciada (subcuenta Design Modeling).

Abre una por una las ocho direcciones de la lista de
scripts/navegador/GUIA-MAPA-FLUJOS-MAC.md. En cada workflow, espera a que el
lienzo termine de dibujar los pasos —no leas la pantalla mientras diga
«Initializing…»— y anótame, en orden:

  1. El DISPARADOR completo. Si es un comentario, dime la palabra Y si está
     acotado a una publicación concreta o si aplica a cualquiera.
  2. Cada PASO, en orden, con su tipo (correo, DM, SMS, espera, condición,
     etiqueta, membresía…).
  3. En los pasos de correo: el asunto y qué plantilla usa.
  4. En los pasos de DM: por qué canal sale exactamente, y si hay una acción
     por canal o una sola compartida entre ramas.
  5. Los enlaces que aparezcan dentro de cualquier mensaje, tal cual.

Escríbelo en matriz-viral/fuentes/navegador/mapa-flujos-mac.md, un bloque por
workflow, con la fecha y la dirección de cada uno.

Reglas:
- No toques nada. Esto es solo lectura: no guardes, no publiques, no edites un
  paso «para ver qué pasa». Si algo se abre en modo edición, ciérralo sin
  guardar.
- No copies nombres, teléfonos ni correos de contactos reales al archivo. Los
  asuntos y las plantillas sí; los datos de personas no.
- Si un workflow no carga ni en tu Chrome, dilo y sigue con el siguiente. Un
  «no cargó» anotado vale más que un resumen inventado.
```

---

## Qué se hace con lo que salga

Tres cosas, en este orden:

**1 · El molde de la membresía (workflows 1 y 2).**
El `GUIA-MONTAJE.md` de ACERO dice *«añadir Membership Grant Offer»*, y eso
salió de comparar páginas vivas, no de haber visto el workflow por dentro. Con
esto se confirma o se corrige antes de montarlo, en vez de después.

**2 · Las ramas de DM (workflows 3 y 4).**
La pregunta es una sola: **¿una acción de envío por canal, o una compartida?**
Si están compartidas, ese es el fallo de julio todavía vivo — el que se llevó
unos 35 leads sin que nadie lo viera, porque la respuesta pública sí salía. Se
arregla en esos dos antes de montar el de ACERO con el mismo defecto.

**3 · El alcance de los genéricos (workflows 5 y 6).**
Si se disparan con comentarios de cualquier publicación, ya sabemos cómo el
post de conexiones terminó mandando el temario de un curso de pago a gente que
pidió una guía gratis. Eso se acota a publicaciones concretas.

Los workflows 7 y 8 son material: los correos de ACERO que ya están escritos y
el correo de recursos gratis, para no volver a redactar lo que existe.

---

## Lo que no hay que hacer

**No lanzar `mapa-flujos` desde Actions «por si acaso».** La tarea sigue en el
menú a propósito —el día que GHL cambie ese arranque vuelve a servir— pero hoy
avisa y no termina. Gastar una corrida en comprobarlo otra vez es gastar una
corrida.

**No dar por leído un workflow por haber abierto su pestaña.** El lienzo tarda
en dibujar los pasos incluso en un navegador normal. Si el resumen sale
sospechosamente corto, lo más probable es que se leyera a medio dibujar.
