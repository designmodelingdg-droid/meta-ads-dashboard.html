# El workflow de palabra, para duplicar

**La idea:** dejar de montar un workflow desde cero cada vez. Se monta **uno**
bien hecho, y para cada recurso nuevo se **duplica y se cambian seis cosas**.

Cinco minutos en vez de media hora, y —lo que importa más— los defectos que ya
costaron leads no se vuelven a colar, porque no se vuelven a escribir.

> **Aviso de honestidad:** todavía no he visto por dentro los que montaste en
> la carpeta *leadmagnet*. Desde aquí no puedo: la API de GHL solo devuelve
> nombre, estado y fecha de un workflow, **no sus pasos**, y esa pantalla no
> carga en un navegador sin pantalla (comprobado el 25-ago, cinco corridas).
> Esta plantilla está escrita sobre el precedente documentado del bot ZAPATA.
> En cuanto me pases la lectura de los tuyos —el encargo está en
> `ENCARGO-LEER-FLUJOS.md`— la reescribo para que diga **tu** método y no el
> heredado.

---

## Las seis cosas que cambian entre un recurso y otro

Todo lo demás se queda igual. Esa es la gracia.

| # | Qué | Ejemplo (ACERO) |
|---|---|---|
| 1 | **El nombre del workflow** | `Bot ACERO — IG/FB` |
| 2 | **La palabra** del filtro | `acero` |
| 3 | **La publicación** a la que se acota | la pieza del Sáb 23 |
| 4 | **El enlace** de la respuesta pública y de los DM | `/acceso-gratis-verificaciones-acero-form` |
| 5 | **Las etiquetas** | `lead-acero-verificaciones` + `origen-bot-acero` |
| 6 | **El texto** del DM de entrega | «las 5 verificaciones en acero» |

Si al duplicar cambias esas seis y nada más, el workflow nuevo hereda las tres
protecciones de abajo sin que nadie tenga que acordarse de ellas.

---

## Las tres cosas que NO se tocan al duplicar

Son las que costaron caro. Van explicadas para que se entienda por qué, no
para que se obedezcan a ciegas.

### 1 · Dos ramas de envío, una por canal

**Nunca una sola acción de «Send DM» compartida entre los dos disparadores.**

Rama Instagram → DM por **Instagram**. Rama Facebook → DM por **Facebook
Messenger**.

Cuando un post nace en Instagram y aparece también en Facebook, quien comenta
en la copia de Facebook tiene un **ID de Facebook**. Si el envío está atado
solo al canal de Instagram, se intenta mandar al ID equivocado: **el workflow
marca el paso como ejecutado y el DM nunca sale.** En julio se perdieron unos
35 leads así, y nadie lo vio porque la respuesta pública sí salía siempre.

### 2 · La respuesta pública lleva el enlace, siempre

Nunca solo «te escribí al DM». El enlace directo en el comentario público es
**la red de seguridad real**: si el canal del DM falla, la persona igual entra.

### 3 · El disparador va acotado a la publicación

No a cualquier post. Abierto, se dispara con comentarios de piezas viejas que
prometían otra cosa — así fue como el post de conexiones terminó entregando el
temario de un curso de pago a gente que había pedido una guía gratis.

---

## Cómo se duplica

1. **Automation → Workflows**, carpeta *leadmagnet*.
2. En el workflow maestro, menú **⋮ → Duplicate**.
3. Renombrar (cambio 1).
4. Entrar a **cada** disparador y cambiar la palabra (2) y la publicación (3).
   Son dos disparadores: el de Instagram y el de Facebook. Los dos.
5. Recorrer los pasos cambiando enlaces (4), etiquetas (5) y textos (6).
6. **Publicar.** Un workflow en borrador no dispara nada, y se ve igual de
   terminado en la lista.

---

## La comprobación, que es media hora bien gastada

**No basta con que los pasos se pongan verdes.** El fallo de julio pasaba
justamente con todo en verde.

- [ ] Comentar la palabra **de verdad en Instagram** → llega el DM
- [ ] Comentar la palabra **de verdad en la copia de Facebook** → llega el DM
- [ ] La respuesta pública salió, **y trae el enlace dentro**
- [ ] El enlace del DM abre la landing correcta —no la de otro recurso—
      y responde 200
- [ ] El contacto quedó con **las dos etiquetas**
- [ ] El workflow quedó en **published**, no en draft

El segundo punto es el que falló en julio y el que casi nadie prueba, porque
hay que ir a buscar la copia en Facebook. Es justo el que hay que probar.

---

## Y el bot no es esto

Se mezclan seguido y mandan a montar lo que no es:

| | Qué hace | Quién |
|---|---|---|
| **El workflow** | alguien comenta la palabra en esa publicación → le llega el DM con los recursos, automático | esto que está aquí |
| **El bot** | cuando esa persona **responde** al DM, toma la conversación | Patricio. Se le pasa qué contestar |

El workflow entrega. El bot conversa después. Montar uno no monta el otro.
