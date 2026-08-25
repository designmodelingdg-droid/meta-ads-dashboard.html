# Las 5 verificaciones en acero que no puedes saltarte

**Lead magnet · palabra del bot: `ACERO`**
Cubre las promesas de tres piezas de la matriz de agosto:
`ago-acero-conexiones` (Mié 20) · `ago-blog-acero-verificaciones` (Sáb 23) ·
`ago-acero-sobredimensionado` (Mié 27).

> **Estado de fuentes — leer antes de publicar.**
> Verificado el 25-ago-2026 contra AISC 360 y NEC. Lo que está citado, está
> comprobado. Lo que lleva 🔶 necesita el temario de la Especialización o un
> Excel del equipo antes de salir. **Nada aquí sale de memoria sin marca.**

---

## Por qué existe esta guía

El perfil pasa por resistencia y aun así la estructura falla, se mueve o
cuesta el doble de lo que debía. Casi siempre es una de estas cinco.

Ninguna la resuelve el software solo. **El programa calcula; el criterio es
tuyo.** Un modelo devuelve un número aunque la hipótesis de partida sea
falsa — y esa es exactamente la trampa.

---

## 1 · Pandeo local

**Qué es.** Antes de que la sección desarrolle su capacidad, un ala o el alma
se abolla. La sección nunca llega al momento que tú le calculaste.

**Por qué se salta.** Porque la mayoría de perfiles laminados comerciales son
compactos, uno se acostumbra a que «siempre cumple», y el día que aparece un
armado, una sección soldada o un perfil de alma esbelta, nadie revisa.

**Qué revisar.** Clasifica **ala y alma por separado** y quédate con la peor
de las dos. Compara la relación ancho-espesor contra los dos límites:

| | |
|---|---|
| λ ≤ λp | **compacta** — desarrolla el momento plástico |
| λp < λ ≤ λr | **no compacta** — capacidad reducida |
| λ > λr | **esbelta** — gobierna el pandeo local |

Para el ala de un perfil I en flexión:

```
λp = 0.38 · √(E / Fy)
λr = 1.00 · √(E / Fy)
```

Con acero A36 (Fy = 250 MPa) y E = 200 000 MPa eso da **λp ≈ 10.7** y
**λr ≈ 28.3**. Con A572 Gr.50 (Fy = 345 MPa), **λp ≈ 9.1** y **λr ≈ 24.1**.

> **Fuente:** AISC 360, Tabla **B4.1a** (elementos en compresión axial) y
> Tabla **B4.1b** (elementos en flexión). La separación en dos tablas existe
> desde AISC 360-10; en 360-05 era una sola tabla B4.1.

**La regla que te llevas:** un perfil no es compacto porque sea laminado. Es
compacto porque su λ lo dice, y λ depende del acero — el mismo perfil puede
ser compacto en A36 y no compacto en A572.

---

## 2 · Pandeo lateral-torsional

**Qué es.** La viga no falla por flexión: se tuerce y se desplaza
lateralmente antes. La capacidad real depende de **cada cuánto está
arriostrada el ala en compresión**, no del perfil.

**Por qué se salta.** Porque en el modelo la viga es una línea. La línea no
tiene ala superior ni sabe si hay una vigueta encima cada 2 m o ninguna en
los 9 m del vano.

**Qué revisar.** La longitud no arriostrada `Lb` contra los dos umbrales del
capítulo F:

- `Lb ≤ Lp` → plastificación total, no gobierna el pandeo lateral
- `Lp < Lb ≤ Lr` → transición, capacidad reducida linealmente
- `Lb > Lr` → pandeo elástico, y la caída es fuerte

Y **`Cb`**: el factor que reconoce que un diagrama de momento no uniforme es
menos exigente. Tomar `Cb = 1.0` siempre es conservador y a veces caro; usar
el `Cb` real de tu diagrama puede devolverte un perfil menor.

> **Fuente:** AISC 360, **Capítulo F**, sección **F2** para perfiles I de
> alma compacta flectados en el eje fuerte.

**La regla que te llevas:** antes de aceptar el perfil, dibuja dónde está
arriostrada el ala superior **en obra**, no en el modelo. Si el arriostre que
supone tu cálculo no lo va a construir nadie, el cálculo no vale.

---

## 3 · Derivas y P-Δ

**Qué es.** Dos cosas que se confunden. La **deriva** es cuánto se desplaza
un piso respecto al de abajo. **P-Δ** es el momento adicional que aparece
porque la carga gravitacional actúa sobre una estructura ya desplazada.

**Por qué se salta.** Porque el diseño se cierra con resistencia y las
derivas se miran «después», cuando ya no hay margen para cambiar el sistema.
Y porque muchos modelos traen el análisis de segundo orden desactivado por
defecto.

**Qué revisar.**

**Deriva máxima inelástica.** En Ecuador el límite es explícito:

| Sistema estructural | ΔM máxima |
|---|---|
| Hormigón armado, **estructuras metálicas** y de madera | **0.02** |
| Mampostería | **0.01** |

Expresado como fracción de la altura de piso.

> **Fuente:** NEC-SE-DS, *Peligro sísmico · Diseño sismo resistente* —
> limitación de derivas de piso.

**Segundo orden.** No es opcional: si tu análisis es de primer orden, tienes
que amplificar. Y si tus derivas ya están cerca del límite, P-Δ te va a
sacar del límite.

**La regla que te llevas:** una estructura de acero rara vez la gobierna la
resistencia. La gobierna la rigidez. Si estás dimensionando por resistencia y
mirando derivas al final, vas a rehacer el proyecto.

---

## 4 · Coherencia entre el modelo y la conexión real

**Esta es la del error #1**, y es la que más caro sale.

**Qué es.** Modelas la conexión como empotrada — porque es el *default* del
programa — y en obra se construye con dos ángulos al alma. El modelo reparte
un momento que la conexión real no puede tomar.

**Qué pasa entonces.** El momento se va al centro del vano, las derivas salen
mayores que las calculadas, y la conexión se plastifica antes que la viga.

**Y al revés pasa igual, y es peor:** modelas articulado, en obra sueldan
alas completas, y el pórtico atrae más sismo del que calculaste.

**Por qué se salta.** Porque el modelo no se equivoca nunca: siempre devuelve
un resultado. La incoherencia no da error, da un número plausible.

**Qué revisar.** Que la hipótesis del modelo y el detalle de la conexión sean
**la misma cosa**, en las dos direcciones:

- ¿Modelaste empotrado? Entonces el detalle tiene que transmitir el momento
  **y** tener la rigidez para que el supuesto se sostenga.
- ¿Modelaste articulado? Entonces el detalle no puede desarrollar momento.
  Soldar alas «para que quede firme» cambia la estructura.
- ¿Semirrígida? Entonces el modelo necesita la rigidez rotacional real, y esa
  no es un *default*.

> **Fuente:** AISC 360, **Capítulo B** — clasificación de conexiones por su
> comportamiento momento-rotación (totalmente restringidas, parcialmente
> restringidas y simples), y **Capítulo J** para el diseño del detalle.

**La regla que te llevas:** la conexión no es un detalle que se resuelve al
final. Es una hipótesis de tu modelo, y si nadie la comprueba contra el
plano de taller, es una hipótesis que nadie verificó.

---

## 5 · Placa base y anclajes

**Qué es.** El punto donde el acero se encuentra con el hormigón. Transmite
carga axial, cortante y —si la base es empotrada— momento.

**Por qué se salta.** Porque queda entre dos especialidades. El de acero
asume que la cimentación lo resuelve; el de hormigón asume que viene definido
con el perfil. Y termina copiado de otro proyecto.

**Qué revisar.**

- **Coherencia con el modelo**, otra vez: si modelaste la base empotrada, la
  placa y los pernos tienen que tomar ese momento. Una base «empotrada» en el
  modelo y rotulada en obra cambia el periodo y las derivas de todo el
  edificio.
- **Aplastamiento del hormigón** bajo la placa.
- **Flexión de la placa** en los voladizos.
- **Anclajes**: tracción, cortante, e **interacción de las dos**.
- **Modo de falla del hormigón** — arrancamiento del cono, no solo la
  resistencia del perno.

> **Fuente:** AISC **Design Guide 1**, *Base Plate and Anchor Rod Design*,
> para el dimensionamiento; y el apéndice de anclajes al hormigón de ACI 318
> para los modos de falla del hormigón.
> 🔶 Los valores concretos de ejemplo hay que tomarlos del temario de la
> Especialización o de un cálculo del equipo — no van inventados.

**La regla que te llevas:** la placa base es la verificación que más veces se
copia de otro proyecto, y la que más veces está mal por eso.

---

## Cierre — lo que estas cinco tienen en común

Ninguna la detecta el software. Las cinco son la misma pregunta hecha de
cinco formas: **¿lo que supuse en el modelo es lo que se va a construir?**

- El perfil compacto lo supone la tabla, no el catálogo. *(1)*
- El arriostre lateral lo supone tu cálculo, lo construye el montador. *(2)*
- La rigidez la supone el análisis, la limita la norma. *(3)*
- La conexión la supone el *default* del programa, la decide el plano de
  taller. *(4)*
- La base la supone el modelo, la ejecuta otro gremio. *(5)*

El programa calcula. **El criterio es tuyo.**

---

## Descargo

Guía **educativa y de predimensionamiento**. No sustituye el criterio ni la
responsabilidad del profesional que firma. Toda verificación debe hacerse con
la norma vigente aplicable al proyecto y la revisa el ingeniero responsable.

No es una certificación ni un diploma.

---

## Pendientes antes de publicar

| | |
|---|---|
| 🔶 | Ejemplos numéricos de la §5 — hacen falta del temario o de un cálculo del equipo |
| 🔶 | Confirmar la edición de AISC 360 que usa la Especialización (360-16 o 360-22) para citar la tabla exacta |
| ✅ | λp y λr del ala en flexión — verificados |
| ✅ | Límites de deriva NEC-SE-DS — verificados (0.02 metálicas / 0.01 mampostería) |
