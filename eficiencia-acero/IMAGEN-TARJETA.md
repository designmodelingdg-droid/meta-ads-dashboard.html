# La imagen de la tarjeta del hub

Es la pieza que va en `recursos/index.html`, en el `--img:url(...)` de la
tarjeta nueva. Sin ella la tarjeta hereda la imagen genérica de la sección y
el recurso se ve prestado.

---

## Especificación técnica, que no es negociable

| | |
|---|---|
| Tamaño | **1672 × 941 px** — el mismo de las siete tarjetas que ya existen |
| Proporción | 16:9 exacto |
| Formato | PNG |
| Fondo | **claro** (crema `#fafaf7` o blanco) |

El fondo claro no es gusto: la tarjeta pinta la imagen con `contain` y rellena
en **blanco**, para no recortar nunca el titular ni el logo. Una pieza con
fondo navy deja dos bandas blancas a los lados y parece un error de montaje.

**Nada importante en los bordes.** Ni texto ni logo a menos de 60 px del
borde: en móvil la tarjeta se estrecha y lo de las orillas es lo primero que
se pierde de vista.

---

## Qué tiene que decir

**Titular, grande y legible en miniatura:**

> ### Las 5 verificaciones en acero

**Bajada, más pequeña:**

> Antes de dar por buena la estructura

**Sello o etiqueta, en naranja `#ca7520`:**

> GRATIS

**Logo DMA** abajo a la derecha, en su versión de tinta oscura —esta pieza va
sobre fondo claro, así que **no** se blanquea.

---

## Cómo se ve

Un plano de estructura metálica, técnico y limpio: pórtico de acero en
perspectiva isométrica o un detalle de conexión viga-columna con su placa y
sus pernos. Trazo fino, azul marino `#003e5c` sobre el crema, con **acentos en
naranja** `#ca7520` marcando cinco puntos de verificación sobre la estructura
—como llamadas de un plano de taller, con su línea de guía.

Cinco acentos, ni cuatro ni seis. Son las cinco verificaciones y la imagen lo
dice sin explicarlo.

Estética de **plano de ingeniería, no de render**: nada de fotografía de obra,
nada de gente con casco, nada de destellos ni degradados 3D. La audiencia son
ingenieros estructurales y lo que les habla es un dibujo que parece salido de
su propio trabajo.

---

## Paleta

```
navy    #003e5c   el trazo y el titular
navy2   #001e30   texto secundario
naranja #ca7520   los cinco acentos y el sello GRATIS
crema   #fafaf7   el fondo
```

Tipografías de la marca: **Overpass** para el titular, **Nunito** para la
bajada. Si la herramienta no las tiene, cualquier sans geométrica de palo seco
con buen peso en negrita sirve — lo que no sirve es una serif ni una
manuscrita.

---

## Lo que no puede aparecer

- **Ningún precio.** Ni el del Máster, ni el de ACERO, ni ninguno.
- **Ni «certificado» ni «diploma».** Es un recurso gratuito, no una
  certificación, y llamarlo así nos mete en un problema que no es de diseño.
- **Ningún número de norma inventado.** Si se quiere citar, es AISC 360-16 o
  NEC-SE-DS, que son las que la guía cita de verdad. Si no, no se cita nada.

---

## Prompt corto, para pegar directo

```text
Technical engineering illustration, 16:9, 1672x941. Isometric line drawing of
a structural steel moment frame connection — beam-to-column with end plate and
bolts — thin precise linework in deep navy (#003e5c) on a warm cream
background (#fafaf7). Five orange (#ca7520) callout markers with thin leader
lines pointing to five distinct checkpoints on the structure, like shop-drawing
annotations. Bold geometric sans-serif headline "Las 5 verificaciones en
acero" in navy, upper left, with smaller subtitle "Antes de dar por buena la
estructura". Small orange pill badge reading "GRATIS". Clean, flat, editorial,
blueprint-adjacent. No photorealism, no 3D render, no gradients, no people, no
hard hats, no lens flare. Generous margins, nothing within 60px of the edges.
```

> Antes de generar: `get_cost`, borrador barato primero, y **no se genera sin
> que Dayana lo apruebe.** Esa es la regla de Higgsfield y aplica aquí igual.

---

## Dónde se sube

Al CDN de GHL (Media Storage), que es donde viven las otras siete. Queda una
URL `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/….png`, y esa
es la que va en el `--img:url(...)` de la tarjeta.


---

## Lo que salió, y la única corrección

La pieza se generó con ChatGPT y quedó **1672 × 941 exactos**, fondo crema,
cinco acentos naranjas, estética de plano. Da el ancho.

**Lo único que hubo que cambiar: el logo venía redibujado, no era el nuestro.**

| | El logo real | El que salió generado |
|---|---|---|
| La marca | una **grúa torre** — pluma horizontal, mástil y el cable con su punto | un triángulo tipo techo, con una línea debajo |
| El texto | Design Modeling DG | Design Modeling DG + una línea «ACADEMY» que el logo no lleva |

Los modelos de imagen **redibujan** los logos, no los pegan, y casi nunca dan
con la marca. Aquí perdió justo lo que identifica a DMA. Se corrigió pegando
encima el archivo real del CDN
(`6a04bbc1fa8afa3be0bb00d8.png`), recortado y escalado al mismo ancho.

**Para la próxima:** generar la pieza **con el espacio del logo vacío** y
pegarlo después. Sale más limpio que pedirlo en el prompt y tener que
arreglarlo.
