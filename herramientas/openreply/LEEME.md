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

### 1 · Crear un usuario de Postgres que solo pueda leer

En la base de OpenReply, como administrador:

```sql
CREATE ROLE matriz_lectura LOGIN PASSWORD 'pon-aqui-una-larga-y-aleatoria';
GRANT CONNECT ON DATABASE openreply TO matriz_lectura;
GRANT USAGE  ON SCHEMA public       TO matriz_lectura;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO matriz_lectura;
-- y que las tablas futuras también queden legibles
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO matriz_lectura;
```

**Solo `SELECT`.** Este usuario no puede escribir, ni borrar, ni cambiar nada.
Si algún día el script tuviera un error, lo peor que puede pasar es que lea de
más — nunca que toque la base.

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

Una honestidad del dato: **los clics cuelgan de la campaña y del enlace, no de
la palabra.** `LinkClick` no guarda cuál palabra disparó, así que en una campaña
con varias palabras el CTR no se puede repartir entre ellas — y aquí no se
inventa.

## Cómo se probó

Sin tocar la base de producción. Se levantó un Postgres local, se creó el
esquema real de OpenReply (sacado de su `prisma/schema.prisma`) y se cargó un
escenario con los cuatro estados a la vez: ZAPATA viva, CHATGPT pausada, NIVEL
muda, MEMORIA y DYNAMO ausentes. El conector los distinguió los cuatro, y la
comprobación de fuga confirmó que ni el token ni un solo nombre salieron al
JSON.
