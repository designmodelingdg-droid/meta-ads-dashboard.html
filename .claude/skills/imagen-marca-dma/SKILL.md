---
name: imagen-marca-dma
description: |
  Genera imágenes de marca de Design Modeling Academy con IA (Higgsfield): portadas de carrusel, imágenes de pauta, banco de imágenes de ingeniería para la web y las historias, y retratos del equipo en el mundo visual BIM+IA. Con la paleta, las reglas de encuadre y el manejo del logo de la casa.

  Usa este skill cuando Dayana diga: "imagen-marca-dma", "genérame una imagen", "hazme la portada del carrusel", "una imagen para el anuncio", "imágenes para la web", "necesito imágenes de ingeniería", "una foto mía en el mundo BIM", o cuando una pieza de la matriz necesite un visual que no existe.

  Probado: banco de 16 imágenes de ingeniería (ago-2026) y los keyframes del comercial con persona real (sep-2026).
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

## Reglas

- **Verificar cada imagen mirándola.** Verificar dos de cuarenta y ocho no es
  verificar cuarenta y ocho.
- **Material real cuando el tema es técnico**: las capturas de Revit son las de
  sus clases o las reales del proveedor, nunca infografías de terceros.
- Nunca instalar ni usar herramientas con credenciales ajenas para generar.
- Avisar cuántos créditos quedan después de cada tanda.
