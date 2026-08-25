# Estado del lead magnet de ACERO

**Comprobado el 25-ago-2026 pidiendo las páginas por HTTP y la lista de
workflows por API.** Nada de esto sale de mirar el editor.

---

## Hecho y verificado

| | Evidencia |
|---|---|
| Las cuatro páginas publicadas en Pages | `index` · `guia` · `app` · `gracias-agenda` responden 200 |
| La landing y la gracias en GHL | las dos responden 200 |
| **La página de gracias renombrada** | `acceso-gratis-verificaciones-acero-gracias` da 200 y la vieja da **404** |
| **El redirect del formulario arreglado** | ahora apunta a la gracias de acero, no a la del Curso Introductorio |
| El campo de perfil sigue en el formulario | `cul_es_tu_perfil_actualmente` presente |
| **El hub pegado y publicado** | las tres marcas dentro de `/recursos`: la ruta, el título y la imagen |
| Los catorce enlaces del hub | los catorce responden 200 |
| El calendario en la gracias | `bIVuNHNojGEgH3gf6yXe` embebido |
| **Los workflows separados por canal** | dos workflows distintos, `IG ACERO` y `FB ACERO`, los dos publicados |

### Sobre el redirect: cambió el original en vez de duplicar

El encargo decía duplicar el formulario. Se le cambió el redirect al original
(`jgZBVSDHAgvfjsJHVFB8`). **Comprobado que no rompió nada:** ninguna de las
otras siete landings usa ese formulario — cada una tiene el suyo. Así que el
atajo salió bien. Queda anotado porque la próxima vez puede no salir.

### Sobre los workflows: quedó mejor que lo pedido

La guía pedía **dos ramas** dentro de un workflow, una por canal. Dayana montó
**dos workflows separados**, `IG ACERO` y `FB ACERO`. Es más robusto: con dos
workflows no existe la posibilidad de compartir la acción de envío por
descuido, que es justo lo que costó ~35 leads en julio. La plantilla se
reescribe con este método.

---

## 🔴 Lo que falta, en orden

### 1 · Hay un workflow duplicado en borrador

```
draft      IG ACERO · Comentario → DM + Membresía     ← sobra
published  ✅ IG ACERO · Comentario → DM + Membresía
published  ✅ FB ACERO · Comentario → DM + Membresía
```

El borrador no dispara nada, así que hoy no hace daño. **El riesgo es
mañana:** en la lista se ve igual de terminado que el publicado, y si alguien
lo publica por error salen **dos DM por cada comentario**. Se borra o se
renombra a `ZZ — borrar`.

### 2 · Los títulos siguen diciendo «Calculadora de Zapatas»

```
acceso-gratis-verificaciones-acero-form     → Calculadora de Zapatas Aisladas Gratis
acceso-gratis-verificaciones-acero-gracias  → Calculadora de Zapatas Aisladas Gratis
```

Es lo que se ve en la pestaña y **lo que aparece cuando alguien comparte el
enlace por WhatsApp**, que es como se comparte casi todo. Se corrige en los
ajustes de cada página del funnel (SEO / Page Title), no en el HTML pegado.

### 3 · La membresía no está montada

`URL_MEMBRESIA` sigue vacío en la página de gracias. Los workflows se llaman
«… → DM + Membresía», así que la intención está; falta confirmar si el producto
existe.

Mientras esté vacío **la entrega funciona igual**: la gracias da el acceso
directo con token. Nadie se queda esperando. Pero no entrega como los demás
recursos, que van por el portal.

### 4 · Nadie ha probado el recorrido completo

Es lo único que dice si esto funciona de verdad:

- [ ] Comentar `ACERO` **en Instagram** → llega el DM
- [ ] Comentar `ACERO` **en la copia de Facebook** → llega el DM
- [ ] La respuesta pública salió **con el enlace dentro**
- [ ] El enlace abre la landing → formulario → cae en la gracias de acero
- [ ] La guía y el verificador abren **sin candado**
- [ ] El contacto en el CRM tiene **el perfil guardado**

El segundo y el último son los que fallan en silencio. El segundo se llevó 35
leads en julio; el último es justo el dato que hace falta para mover la pauta.

---

## No bloquea, pero está pendiente

- **Comunidades** (Paso 5): vincular la guía en la pestaña Learning.
- **El logo de la tarjeta**: la imagen del hub trae el logo redibujado por
  ChatGPT. La versión corregida está en `tarjeta-hub.png`; si se sube al CDN,
  se cambia la URL de la tarjeta en una línea.
- **Los dos genéricos de comentario** se tocaron hoy. Falta confirmar si
  quedaron acotados a publicaciones concretas o siguen abiertos a cualquier
  post.
