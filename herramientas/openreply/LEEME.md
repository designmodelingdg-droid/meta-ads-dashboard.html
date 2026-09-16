# OpenReply → la matriz

OpenReply es la aplicación propia que recibe los comentarios de Instagram y
manda el DM cuando alguien escribe una palabra clave. Vive en su propio
repositorio (`designmodelingdg-droid/openreply`) y **no se copia aquí**: es una
aplicación Next.js con Postgres, Redis y un worker. Lo que se trae a la matriz
es su **dato**, igual que se trae el de Stripe, PayPal o Meta Ads.

## Por qué

La matriz lleva seis palabras activas —ZAPATA, ACERO, NIVEL, CHATGPT, MEMORIA,
DYNAMO— y el estado de cada una es **una casilla que alguien tiene que acordarse
de marcar**. «Montar el disparador CHATGPT en GHL» lleva semanas sin marcar y
nadie sabe si está puesto o no.

OpenReply sí lo sabe: es quien recibe el comentario y decide si casa. Conectado,
«el disparador está montado» deja de ser una casilla y pasa a ser un hecho
medido — y aparece además lo que la casilla nunca iba a decir: **cuál de las
seis palabras convierte**.

El cruce distingue cuatro estados, y los cuatro se leen distinto:

| Estado | Qué significa | Qué hacer |
|---|---|---|
| **Viva** | Montada, activa y con DM enviados | Nada |
| **Muda** | Montada y activa, pero nunca ha disparado | El CTA no se está publicando, o nadie comenta esa palabra |
| **Pausada** | La campaña existe pero está apagada | El comentario NO dispara. Encenderla |
| **Ausente** | No hay ninguna campaña con esa palabra | Si hay un CTA pidiéndola, **el comentario no recibe nada** |

Los dos del medio son los que hoy la matriz no distingue, y son justo los que
hacen que una pieza salga prometiendo un recurso que no llega.

## Qué hay que hacer UNA vez

### 1 · El usuario de solo lectura — HECHO (16-sep, Dayana)

`matriz_ro` existe en el Postgres de OpenReply (Railway), y se hizo **mejor de
lo que estaba escrito aquí**: los permisos son **por columna**, no por tabla.

La diferencia importa. Con `GRANT SELECT` por tabla, «no leemos datos
personales» es una promesa del script. Por columna, **la base misma rechaza**
leerlos, venga la consulta de donde venga.

Fuera del alcance del rol: `accessToken`, `commenterName`, `commentText`,
`commenterId`, `commentId`, `ipHash`, `userAgent`, `referrer`. La tabla
`FollowGate` no está concedida en absoluto — identifica a las personas una a
una.

Lo que el rol puede leer:

| Tabla | Columnas |
|---|---|
| `Automation` | id, name, keywords, matchAnyWord, isActive, postId, postUrl, createdAt, updatedAt |
| `DmLog` | id, automationId, matchedKeyword, status, attempts, dmSentAt, errorMessage, publicReplySentAt, createdAt |
| `TrackedLink` | id, automationId, slug, label, destinationUrl, createdAt |
| `LinkClick` | id, automationId, trackedLinkId, createdAt |
| `FollowerSnapshot` | id, instagramAccountId, date, followersCount, backfilled, createdAt |
| `InstagramAccount` | id, username |

**Consecuencia para el código, y no es menor:** con permisos por columna, pedir
una columna no concedida **no devuelve nulo — tumba la consulta entera** con
«permission denied for table». Nada de `SELECT *`, y cada columna nombrada.

`scripts/prueba_openreply.py` lleva esa tabla escrita y comprueba cada consulta
contra ella antes de que toque producción. La primera versión pedía cuatro
columnas de más y habría fallado en la primera corrida.

**Una columna que falta y se echa en falta:** `Automation.instagramAccountId`
no está concedida, así que no se puede decir a qué cuenta de Instagram
pertenece cada campaña. Con una sola cuenta da igual; si algún día hay varias,
hay que concederla.

### 2 · Guardar la URL en los secretos del repositorio

`Settings → Secrets and variables → Actions → New repository secret`

```
Name:  OPENREPLY_DATABASE_URL
Value: postgresql://matriz_lectura:LA-CLAVE@el-host:5432/openreply?sslmode=require
```

**La clave no se pega en el chat, ni en un archivo, ni en un mensaje.** Va
directa de tu navegador al secreto, igual que `META_TOKEN`.

Si la base solo acepta conexiones desde ciertas IP, hay que dejar entrar a los
runners de GitHub, o dar acceso por la vía que use tu proveedor.

## Cómo se usa

Corre solo dentro del Action `metricas-semanales.yml`, los lunes y los viernes,
junto al resto. A mano:

```
mcp__github__actions_run_trigger  metricas-semanales.yml
```

Deja `matriz-viral/fuentes/openreply/campanas.json`.

## Qué trae, y qué NO

Trae, todo agregado: campañas con sus palabras y si están activas, DM enviados
/ fallidos / saltados, **los motivos de fallo tal como los devolvió Meta**,
enlaces rastreados con sus clics, clics y envíos por día, y los seguidores
diarios.

**No trae, y es deliberado:** ni `commenterName`, ni `commentText`, ni
`commenterId`, ni `accessToken`, ni el hash de IP del clic. Son datos de
personas reales y llaves, y `fuentes/` acaba dentro de artefactos y PDF que se
comparten. `scripts/prueba_openreply.py` lo comprueba en cada corrida y **falla
la corrida** si una consulta nueva intenta leer una de esas columnas.

### Tres honestidades del dato

**1. Los DM SÍ se cuentan por palabra.** `DmLog.matchedKeyword` guarda cuál
palabra disparó cada envío, y el bloque `por_palabra` los cuenta.

**2. Los clics NO se pueden repartir por palabra.** `LinkClick` cuelga de la
campaña y del enlace, y no guarda la palabra. En una campaña con varias
palabras no se reparten, y aquí no se inventa.

**3. Los clics son APERTURAS, no personas — y pueden superar a los envíos.**
El redirector apunta cada apertura: la misma persona que abre el enlace tres
veces cuenta tres, y los bots de vista previa de Instagram y WhatsApp también
cuentan. Con 60 DM enviados puede haber 1.200 clics.

Por eso `clics / enviados` **no es un porcentaje de conversión**. OpenReply
resuelve eso capando el número al 100 % (`lib/tracking/analytics.ts`), y eso
tira la señal: 1.200 clics sobre 60 envíos y 60 sobre 60 se ven los dos como
«100 %». Aquí **no se capa**: cuando hay más clics que envíos, `ctr` queda en
nulo y se usa `clics_por_dm` con la explicación al lado.

No se pueden contar clics **únicos**: haría falta `LinkClick.ipHash`, que está
deliberadamente fuera del rol por ser un dato de persona. Es la decisión
correcta; solo hay que saber que el número son aperturas.

### Y el cero que no significa nada

Una campaña solo mide clics si se montó **con un enlace rastreado**. En
OpenReply eso es OPCIONAL: si el DM lleva el enlace crudo, no hay `TrackedLink`
y esa campaña marcará cero clics para siempre.

Ese cero se lee igual que «el recurso no le interesa a nadie». Por eso cada
campaña trae `mide_clics` y una `lectura_clics` explícita, y el CTR se deja en
**nulo, no en cero** — un cero se promedia y se grafica, un nulo no.

> Es el mismo error que la CAPI el 14-sep: `capi_detectada: False` en los cinco
> píxeles, incluido uno con 1.009 eventos de servidor. Un cero del medidor
> leído como del mundo.

### Y si una consulta falla, el cruce no afirma nada

`cotejo_fiable` dice si la consulta de campañas salió bien. Si falló, las
palabras NO se reportan como ausentes: se dice que no se pudo comprobar. La
primera prueba con permisos reales hizo justo eso —la consulta murió y el
script siguió afirmando que las seis palabras no existían— y es un fallo peor
que el que arregla, porque se lee como un hecho comprobado.

## Cómo se probó

Sin tocar la base de producción. Se levantó un Postgres local, se creó el
esquema real de OpenReply (sacado de su `prisma/schema.prisma`) y se cargó un
escenario con los cuatro estados a la vez: ZAPATA viva, CHATGPT pausada, NIVEL
muda, MEMORIA y DYNAMO ausentes. El conector los distinguió los cuatro, y la
comprobación de fuga confirmó que ni el token ni un solo nombre salieron al
JSON.
