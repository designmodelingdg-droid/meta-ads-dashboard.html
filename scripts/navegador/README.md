# Automatizar GoHighLevel con navegador

## Por qué existe

La API v2 de GHL es **de solo lectura** para lo que más falta. Verificado
contra la documentación oficial el 24-ago-2026:

| | |
|---|---|
| Workflows | solo `GET /workflows/` — ni crear, ni editar, ni publicar |
| Funnels y Sites | solo tres `GET` — ninguna escritura |
| Qué plantilla usa cada workflow | **no lo expone la API**, ni leyendo |

Lo que la API no escribe, un navegador sí. Esto es esa puerta.

---

## Cómo entra sin que nadie escriba una contraseña en un chat

**El camino recomendado es `GHL_STORAGE_STATE`**: una sesión ya iniciada,
exportada a JSON y guardada como secreto del repositorio.

Es mejor que usuario y contraseña por tres razones concretas:

1. **Caduca sola.** Una sesión muere en semanas. Una contraseña de GHL no, y es
   la llave maestra: quien la tenga puede borrar la cuenta entera.
2. **Sortea el 2FA.** GHL manda un código al correo. Un navegador sin nadie
   delante no puede resolverlo, así que con usuario y contraseña la corrida
   falla en cuanto se active la verificación.
3. **Se revoca cerrando sesión**, sin cambiar nada más.

### Generarla — cinco pasos, una sola vez

Esto se hace **en tu computadora**, no en el servidor: hace falta un navegador
con ventana para que puedas escribir tu clave y tu código de verificación.

**1 · Comprobar que tienes Node.** En la Terminal:

```bash
node --version
```

Si responde algo como `v22.x`, listo. Si dice *command not found*, instala la
versión **LTS** desde [nodejs.org](https://nodejs.org) y vuelve a abrir la
Terminal.

**2 · Instalar Playwright y su Chromium** (una vez en la vida):

```bash
npm install -g playwright
npx playwright install chromium
```

**3 · Capturar la sesión.** Desde la carpeta del repositorio:

```bash
node scripts/navegador/capturar-sesion.js
```

Se abre un Chromium limpio — **no usa tu Chrome ni tus perfiles**. Entra a GHL
como siempre: correo, clave y el código si te lo pide. En cuanto el script vea
que estás dentro de la subcuenta, guarda solo y te dice qué hacer. No tienes
que cerrar la ventana ni adivinar cuándo.

Si algo sale a medias **no guarda nada**, a propósito: un archivo incompleto
falla después, en mitad de una corrida, y ahí cuesta mucho más entender qué
pasó.

**4 · Pegarlo como secreto.** Abre `sesion.json`, copia todo (`Cmd/Ctrl + A`,
`Cmd/Ctrl + C`) y pégalo en:

> Settings → Secrets and variables → Actions → New repository secret
> Name: `GHL_STORAGE_STATE` · Value: (todo el contenido)

Después **borra el archivo del disco**: `rm sesion.json`. Ya está en el
repositorio como secreto y en el disco solo es un riesgo. Está en `.gitignore`,
así que no se puede commitear por accidente, pero eso no lo protege de que se
reenvíe por WhatsApp o quede en Descargas.

**5 · Comprobar que quedó bien**, sin tocar nada:

> Actions → Navegador GHL → Run workflow
> tarea = `sesion` · aplicar = `false`

Entra a Workflows y a Sites y dice si la sesión llega a las dos. Si te mandó al
login, caducó: se repite desde el paso 3.

### Qué es ese archivo, en claro

Una **sesión abierta de tu CRM**. Quien lo tenga entra sin clave y sin 2FA,
hasta que caduque o cierres sesión. No se manda por WhatsApp ni por correo.
Para revocarla en cualquier momento: cierra sesión en GHL y deja de servir.

### El camino alternativo

`GHL_USER` y `GHL_PASS` como secretos. Funciona **solo si la cuenta no pide
2FA**. Si lo pide, el script lo detecta, guarda captura y te manda a generar la
sesión. No se queda colgado ni finge que funcionó.

---

## Los tres frenos, y por qué están

**1 · Simulacro por defecto.** Ninguna tarea escribe nada sin `--aplicar`. El
modo normal recorre, dice lo que haría y sale.

**2 · Verificación después de escribir.** Cada acción vuelve a **leer** la
página para confirmar. Esto no es paranoia: en julio el bot de ZAPATA marcaba
los pasos en verde y el DM no llegaba. Se perdieron unos 35 leads antes de que
alguien abriera una conversación a comprobarlo. **Un clic dado no es un cambio
guardado.**

**3 · Fallo ruidoso.** Cuando algo no aparece donde se espera, se guarda
captura y HTML en `matriz-viral/fuentes/navegador/` antes de rendirse. Si GHL
cambia un botón de sitio, se ve en la imagen en vez de adivinar.

Y un tope: ninguna corrida toca más de 25 objetos. Volver a lanzarla continúa.

---

## Las tareas

> **Hay un segundo camino al navegador:** `browser-harness`, que se conecta al
> Chrome que ya tienes abierto y no necesita ningún secreto. No sustituye a
> esto — sirve para lo difícil y puntual, contigo delante, mientras que esto
> corre sin nadie. Está explicado en [BROWSER-HARNESS.md](BROWSER-HARNESS.md),
> con el aviso de alcance que hay que leer **antes** de conectarlo.

```bash
# LECTURA — comprobar que el secreto sigue sirviendo (empieza por aqui)
node scripts/navegador/tareas.js sesion

# LECTURA — inventario de páginas de Sites
node scripts/navegador/tareas.js paginas

# ESCRITURA — publicar un workflow en borrador
node scripts/navegador/tareas.js encender --flujo "NOMBRE" --aplicar

# ESCRITURA — restaurar una página de la papelera
node scripts/navegador/tareas.js restaurar-pagina --pagina "Test de Nivel BIM" --aplicar

# ESCRITURA — reemplazar el contenido de un elemento Custom Code
node scripts/navegador/tareas.js pegar-html \
  --pagina "Recursos" \
  --archivo recursos/ghl-recursos.html \
  --url https://funnel.dgdesignmodeling.com/recursos \
  --aplicar
```

### `mapa-flujos` no corre aquí — corre en el Mac

**Comprobado el 25-ago-2026, después de cinco corridas.** La última entró a un
solo workflow y esperó 90 segundos anotando cada vez que la página crecía:

```
+2s · 37 car · Loading fresh data... Initializing...
SIN CARGAR (37 car · 1 marcos)      ← ~88 s después, sin crecer una sola vez
```

El texto creció **una vez**, a los dos segundos, y ahí se quedó. Eso no es
lento: **está atascado.** Subir el tiempo de espera no lo arregla — el
constructor de workflows de GHL no termina de arrancar en un navegador sin
pantalla. (Por el camino diagnostiqué que el texto estaba en un iframe. No lo
estaba: `marcos: 1`. Queda anotado para que nadie vuelva por ahí.)

Así que este es el primer trabajo que cae del lado de **browser-harness**, con
el Chrome de siempre en el Mac, donde la página arranca porque es un navegador
normal con su sesión. El encargo ya está escrito y priorizado —ocho workflows, no los 148— en
[GUIA-MAPA-FLUJOS-MAC.md](GUIA-MAPA-FLUJOS-MAC.md). Ver también
[BROWSER-HARNESS.md](BROWSER-HARNESS.md).

El código sigue en `tareas.js` a propósito, y la tarea sigue en el menú de
Actions: el día que GHL cambie ese arranque vuelve a servir sin reescribir
nada. Lo que ya no se hace es lanzarla desde Actions esperando que salga bien —
si alguien lo intenta, la propia tarea lo avisa antes de empezar.

Lo demás de esta lista (`sesion`, `paginas`, `encender`, `restaurar-pagina`,
`pegar-html`) no está afectado: son pantallas que sí cargan.

---

`pegar-html` no verifica mirando la interfaz: **pide la página pública por HTTP**
y comprueba que traiga los enlaces nuevos y ya no los viejos. Por eso `--url` es
obligatorio. Si el editor guardó pero la página pública no cambió, la tarea
falla — que es justo lo que uno quiere saber.

Se lanzan desde **Actions → Navegador GHL → Run workflow**, que es donde viven
los secretos. En local no hay credenciales y no debe haberlas.

---

## Lo que sigue siendo mala idea, aunque ahora se pueda

Que exista el martillo no obliga a usarlo en todo.

- **No automatizar lo que se hace una vez.** Montar un workflow nuevo a mano
  toma diez minutos; escribir el script que lo monte toma horas y se rompe con
  el próximo rediseño de GHL.
- **No borrar nada por navegador.** Leer mal no rompe nada; borrar mal en un
  CRM con 1.200 oportunidades sí. Este paquete no tiene ninguna tarea de
  borrado y no debería tenerla.
- **Lo que la API sí sabe hacer, se hace por API.** Es más rápido, no se rompe
  cuando cambian un botón, y deja rastro limpio.
