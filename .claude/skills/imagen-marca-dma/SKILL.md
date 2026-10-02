---
name: imagen-marca-dma
description: |
  Genera imágenes de marca de Design Modeling Academy con IA (Higgsfield): portadas de carrusel, imágenes de pauta, banco de imágenes de ingeniería para la web y las historias, y retratos del equipo en el mundo visual BIM+IA. Con la paleta, las reglas de encuadre y el manejo del logo de la casa.

  Usa este skill cuando Dayana diga: "imagen-marca-dma", "genérame una imagen", "hazme la portada del carrusel", "una imagen para el anuncio", "imágenes para la web", "necesito imágenes de ingeniería", "una foto mía en el mundo BIM", "hazme una historia", "una portada con el estilo del perfil", o cuando una pieza de la matriz necesite un visual que no existe.

  Probado: banco de 16 imágenes de ingeniería (ago-2026), los keyframes del comercial con persona real (sep-2026) y las plantillas con el estilo del perfil para historias y portadas de apoyo (oct-2026, sección 8). Las artes que se publican se hacen en la app.
---

# Skill: imagen-marca-dma

---

## 1. La paleta y el mundo visual

| Uso | Color |
|---|---|
| Fondo / azul marino DMA | `#0E2438` |
| Acento ámbar (SIEMPRE la palabra clave) | `#E8A04A` |
| Naranja de carruseles | `#EE8A3C` |
| Geometría BIM | blanco y hormigón |
| Blueprints y datos | cian claro |

Estética: **técnica, limpia, premium, tipo Autodesk Revit**. Nunca ciencia
ficción, nunca fantasía arquitectónica, nunca geometría imposible: el público
son ingenieros y detectan un edificio que no se sostiene.

---

## 2. Modelos y costos (plan free, sep-2026)

| Para qué | Modelo | Costo |
|---|---|---|
| Calidad máxima, referencias de identidad | `nano_banana_pro` 2k | 2 cr |
| Volumen (banco de imágenes) | `nano_banana_2_lite` | 1 cr |

Siempre `get_cost:true` antes de una tanda. **Máximo 2 envíos simultáneos**: con
más da 429 rate_limit_reached. `get_cost` responde aunque el plan no permita el
modelo — el permiso solo se ve al enviar.

---

## 3. Formatos

| Destino | Ratio | Px |
|---|---|---|
| Carrusel Instagram | 4:5 | 1080×1350 |
| Post plano | 4:5 | 1080×1350 |
| Historias / reels / keyframes | 9:16 | 1080×1920 |
| Web y LinkedIn | 16:9 | 1920×1080 |

Las imágenes generadas en vertical **no sirven recortadas** para tarjetas
horizontales: se pide la variante 16:9 desde el principio.

---

## 4. El texto NO lo escribe el modelo

Los modelos de imagen escriben con errores de ortografía. En todo prompt va
"NO text, NO letters, NO numbers, NO watermark", y el texto se monta después
(en el carrusel lo pone diseño; en video, un `.ass`).

Excepción: `nano_banana_pro` sí renderiza texto corto en inglés de forma
aceptable, pero **igual hay que leerlo carácter por carácter antes de publicar**.

---

## 5. El logo es el real, nunca generado

El logo de Design Modeling DG (la grúa) está en base64 dentro de
`dma-sales-assistant/tutor/pagina/index.html` y en el CDN de la cuenta. Se monta
en post. Para fondo oscuro se recolorea a blanco conservando en ámbar los
píxeles donde R−B > 15.

**Un logo generado por IA sale mal siempre y es la marca.**

---

## 6. Retratos del equipo en el mundo BIM

Ver el skill `video-comercial-ia`, sección 2: mismo método (foto de referencia
con fondo limpio, escala explícita, una sola persona) y la misma advertencia —
si la foto tiene un cuadro detrás, el modelo lo copia y duplica la cara.

---

## 7. Dónde viven las imágenes

Las que van a la web o a las historias pasan al repo público bajo
`recursos/img/` para tener URL propia de DMA en Pages: **una web no puede colgar
de los enlaces del CDN de Higgsfield**, que no controlamos. La lista tema por
tema está en `recursos/img/historias/LISTA-IMAGENES.md`.

---

## 8. Plantillas con el estilo del perfil (aprobadas el 2-oct-2026)

> **Las artes que se publican las hace el equipo desde la app.** Estas plantillas
> son de apoyo: historias, portadas de reels, piezas internas y cualquier visual
> que haga falta rápido. No reemplazan el arte de la app.

Las primeras portadas hechas por código, con fondo azul, cuadrícula y Anton, se
rechazaron: «se ven feas, genéricas y planas». Se rehicieron copiando el grid
real de @design_modeling_dg, midiendo los píxeles de una captura, y quedaron
aprobadas. Todo vive en `plantilla-perfil/`, con los ejemplos renderizados en
`plantilla-perfil/ejemplos/`.

**Lo que hace que se vea como el perfil:**

| Elemento | Valor |
|---|---|
| Fondo | navy muy oscuro, degradado radial de `#0C2442` (arriba) a `#071A2F` y `#05142A`. Es más oscuro que el `#0E2438` de la tabla 1. |
| Naranja del perfil | `#E8893A`, medido en las portadas («5 ERRORES», «¿EN QUÉ ETAPA BIM?»). El `#E8A04A` sale pálido al lado. |
| Titular A, condensado (el preferido) | Bebas Neue, blanco con un degradado leve a `#D3D8DF`, palabras clave en naranja, 150-170 px. Como «CINCO TAREAS DE REVIT». |
| Titular B, geométrico | Montserrat 900, mayúsculas, interletrado −2,5 px, 96 px, y la cifra o frase clave a 158 px en naranja. Como «5 ERRORES AL MODELAR». |
| Subtítulo | Montserrat 700-800 en caja normal, con el final en naranja. Debajo, una raya naranja de 120×7 px. |
| Fondo técnico | trazos de plano tenues con medidas y ejes (`bp.svg`, opacidad 0,10-0,16) y una imagen técnica real o del banco de marca, oscurecida y con los bordes fundidos. |
| Cabecera | logo real (`logo-claro.png`) arriba a la izquierda, y en carrusel el contador `01/07` con la barra en naranja. |
| Pie | «MEDIR A DIARIO \| DECIDIR MEJOR» (Montserrat 800, 19 px, interletrado 6 px) y a la derecha «DESLIZA →» o «COMENTA PALABRA →», con la palabra en naranja. |

**Plantillas:**

| Archivo | Para qué | Tamaño |
|---|---|---|
| `portada-carrusel.html` | Portada de carrusel, titular condensado | 1080×1350 |
| `portada-geometrica.html` | La misma con el titular geométrico | 1080×1350 |
| `post-plano.html` | Post de una imagen con CTA de palabra | 1080×1350 |
| `historia.html` | Historia vertical, con 250 px libres arriba y abajo | 1080×1920 |

**Cómo se usa:** se copia la plantilla, se cambia el texto y la imagen de fondo
(las del banco están en `recursos/img/historias/`) y se renderiza:

```
npm i --prefix /tmp/pw playwright-core@1.56.0      # una vez por sesión
NODE_PATH=/tmp/pw/node_modules node render.cjs mi-pieza.html
```

`render.cjs` usa el Chromium de `/opt/pw-browsers`, espera a que carguen las
fuentes (vienen en `fonts/`, no dependen de internet) y muestra cuáles cargó.
Si no aparece «Bebas Neue» o «Montserrat», el render no sirve.

**Reglas de estas piezas:**
- Una idea por pieza, y el titular se lee en un segundo a tamaño de celular. Hay que revisarlo reducido a 360 px de ancho.
- Nada se tapa ni se corta: ni el titular con la imagen, ni el pie con la CTA. Se revisa mirando el PNG, siempre.
- Las capturas de software son siempre reales. Si el guion pide un pantallazo de Revit o Robot y no lo hay, se usa una imagen del banco **y se avisa** de que falta la captura.
- Nada de personas generadas con IA. Si va Gabriel, es una foto real recortada, sin subtítulos encima.
- Nada de precios en el diseño salvo que el guion lo confirme. El Máster nunca lleva precio.

## Reglas

- **Verificar cada imagen mirándola.** Verificar dos de cuarenta y ocho no es
  verificar cuarenta y ocho.
- **Material real cuando el tema es técnico**: las capturas de Revit son las de
  sus clases o las reales del proveedor, nunca infografías de terceros.
- Nunca instalar ni usar herramientas con credenciales ajenas para generar.
- Avisar cuántos créditos quedan después de cada tanda.
