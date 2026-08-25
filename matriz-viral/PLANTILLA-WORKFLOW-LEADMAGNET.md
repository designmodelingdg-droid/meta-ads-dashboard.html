# El workflow de palabra, para duplicar

**La idea:** dejar de montar un workflow desde cero cada vez. Se monta **uno**
bien hecho, y para cada recurso nuevo se **duplica y se cambian seis cosas**.

Cinco minutos en vez de media hora, y —lo que importa más— los defectos que ya
costaron leads no se vuelven a colar, porque no se vuelven a escribir.

> **Lo que sí se sabe de los de Dayana, y lo que no.** Por API se ve el nombre
> y el estado; los pasos no, porque esa ruta devuelve 404 (comprobado, no
> leído). Lo que se ve basta para lo importante:
>
> ```
> published  ✅ IG ACERO · Comentario → DM + Membresía
> published  ✅ FB ACERO · Comentario → DM + Membresía
> ```
>
> **Montó dos workflows separados, uno por canal** — no dos ramas dentro de
> uno, que era lo que pedía la guía vieja. Es más robusto, y por eso esta
> plantilla ya está escrita con su método. El detalle de los pasos sigue
> pendiente de la lectura por navegador (`ENCARGO-LEER-FLUJOS.md`).

---

## Las seis cosas que cambian entre un recurso y otro

Todo lo demás se queda igual. Esa es la gracia.

| # | Qué | Ejemplo (ACERO) |
|---|---|---|
| 1 | **El nombre del workflow** | `IG ACERO · …` y `FB ACERO · …`, uno por canal |
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

### 1 · Un workflow por canal — el método de Dayana

**Un workflow para Instagram y otro para Facebook, separados.** No dos ramas
dentro del mismo, y muchísimo menos una sola acción de «Send DM» compartida.

```
✅ IG ACERO · Comentario → DM + Membresía
✅ FB ACERO · Comentario → DM + Membresía
```

Dos workflows es más seguro que dos ramas, y esa es la mejora: con archivos
separados **no existe la posibilidad** de compartir la acción de envío por
descuido. La estructura impide el error en vez de pedir que nadie lo cometa.

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
4. Cambiar la palabra (2) y la publicación (3) en el disparador.
   **Y repetir todo con el del otro canal** — son dos workflows, no uno.
   Duplicar solo el de Instagram y olvidar el de Facebook es el descuido fácil.
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


---

## Y limpiar los borradores que sobran

Al duplicar quedan copias a medias. El 25-ago quedó una:

```
draft      IG ACERO · Comentario → DM + Membresía     ← sobra
published  ✅ IG ACERO · Comentario → DM + Membresía
```

Un borrador no dispara nada, así que no hace daño hoy. **El problema es
mañana:** en la lista se ve igual de terminado que el bueno, y si alguien lo
publica por error salen **dos DM por cada comentario**.

Por eso el `✅` delante del nombre en los publicados: se distingue de un
vistazo cuál es el que corre. Y lo que sobra se borra o se renombra a
`ZZ — borrar`, no se deja «por si acaso».
