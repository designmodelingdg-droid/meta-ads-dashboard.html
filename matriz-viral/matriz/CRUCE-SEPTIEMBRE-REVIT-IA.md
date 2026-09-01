# Septiembre: el cruce entre lo del nicho y lo nuestro

**26-ago-2026.** Dayana ve tracción en «Revit conectado a la IA» y quiere
apoyar septiembre ahí. Esto comprueba esa intuición contra datos.

**Veredicto: tiene razón, pero no por la razón que parece.**

> ⏸ **PROVISIONAL — decisión de Dayana, 26-ago.** Quedan reels por publicar.
> Se espera a que salgan y se rehace el cruce antes de cerrar septiembre.
>
> Lo que ya se sostiene y no va a cambiar con más datos: **las vistas son la
> métrica equivocada**, y la forma de los ganchos que funcionan.
> Lo que sí puede moverse: qué piezas concretas entran, y si el patrón de
> IA + Revit aguanta con más muestra.
>
> Cuando estén publicados: `refresh_matriz.py` las recoge en la corrida
> semanal, y con eso se rehace este cruce.
>
> **Primera confirmación (31-ago):** la semana 24-30 el patrón aguantó — y
> mejoró. «Sobredimensionar no es ir por el lado seguro» rompió el trade-off:
> 13.306 vistas CON 7,67 c/1k. La forma «afirmación que incomoda + palabra +
> recurso real detrás» supera incluso a las fronteras solas. La declaración
> genérica de IA volvió a quedarse en 1,75.

---

## Lo primero, porque cambia cómo se lee todo lo demás

Las vistas son la métrica equivocada para esta decisión.

| Eje | Mediana de vistas | Comentarios / 1.000 vistas |
|---|---|---|
| OBRA | **9.606** | **0,17** |
| NÚCLEO-BIM | 3.484 | 0,56 |
| NÚCLEO-IA | 2.087 | **1,58** |

Y en los extremos:

```
el reel de 4.720.794 vistas  →  0,10 comentarios por mil
los 6 mejores en conversación →  15,95 comentarios por mil
```

**Noventa y cinco veces más conversación por vista.** El encofrado hizo casi
cinco millones de vistas y prácticamente nadie comentó. Un comentario es lo
que dispara el workflow de palabra y se convierte en lead; una vista de obra
no es nada.

Si septiembre se juzga por vistas, va a parecer peor que agosto **y va a ser
mejor**. Conviene decidir ahora con qué se mide.

---

## Los seis que más conversación generaron, y qué tienen en común

```
30,54 c/1k   «Si todavía dimensionas zapatas a ojo, esto es para ti»
17,79 c/1k   «ChatGPT diseña una losa → la IA falla en el criterio, no en el cálculo»
12,50 c/1k   la variante del de zapatas
12,46 c/1k   «Tu Revit ya trae IA y poca gente la activó. Estas son 3…»
11,58 c/1k   «La IA ya hace 5 tareas de tu trabajo BIM. La 6ta, jamás.»
10,86 c/1k   «"Manejo Revit." 🫠»
```

**Cuatro de los seis son IA + Revit.** Los otros dos son el lead magnet de
zapatas, que comenta porque **pide** comentar — su CTA es la palabra.

La diferencia importa: los de IA generan conversación **sin pedirla**. Eso es
interés real, no un incentivo.

### La forma que se repite

No es «pregunta», ni «error», ni «tutorial» — probé esa clasificación sobre los
156 reels y no separa nada, las tres medianas quedan cerca de cero.

Lo que se repite en los que funcionan es **una frontera**:

| | La forma | Por qué mueve |
|---|---|---|
| **Ya lo tienes y no lo sabes** | «Tu Revit ya trae IA y poca gente la activó» | no vende nada, revela |
| **Hasta aquí llega, de aquí no pasa** | «La IA hace 5 tareas. La 6ta, jamás» | defiende su profesión |
| **Falla justo donde tú vales** | «ChatGPT falla en el criterio, no en el cálculo» | los reivindica |

Ninguna es un tutorial. Ninguna es «5 tips de Revit». Las tres le dicen al
ingeniero algo **sobre él**, no sobre el software.

---

## Lo que el nicho añade — poco, y hay que decirlo

Se bajaron **106 piezas** públicas de ocho etiquetas del nicho. **El resultado
es flojo y no da para conclusiones fuertes:**

- Volvieron **solo imágenes y carruseles, cero reels**. Las páginas de etiqueta
  no devuelven vídeo ni vistas.
- El engagement es diminuto: el mejor tiene 275 likes. Son etiquetas pequeñas.
- Solo 26 de 106 traen comentarios.

Con esa reserva, lo único que se sostiene es que **la señal apunta al mismo
sitio**. Ordenando por comentarios sobre likes:

```
0,846  «¿Te esfuerzas el doble y avanzas la mitad?»
0,556  «¿Te imaginas un asistente inteligente que planifique y ejecute?»
0,386  «La nueva Ley Europea de IA ya afecta a los estudios de arquitectura»
0,182  «Si usás Claude solamente para hacer preguntas, todavía te falta…»
```

Y los dos con más likes —«¿qué plugin de Revit usas más?» con 275, y un
proyecto bonito con 262— **casi no tienen comentarios**. Misma lección que en
casa: los likes no son conversación.

Ese último, el de Claude, es literalmente el ángulo de Dayana y es el único de
la muestra que lo toca.

**Para arreglar la investigación** hace falta apuntar a **cuentas** y no a
etiquetas — ahí sí vienen reels con vistas. `scripts/competencia.py` ya hace
eso y es por donde hay que ir la próxima vez.

---

## La propuesta para septiembre

Septiembre ya tiene **6 de 18 piezas** de Revit/IA: `ago-tip-revit-ia`,
`ago-chatgpt-revit`, `ago-dynamo-revit`, `ago-revit-ia-futuro`,
`ago-errores-modelar-revit`, `ago-plugins-revit`.

La columna vertebral está. Lo que falta es **el ángulo concreto de Dayana** —
Revit conectado a Claude— y **reescribir los ganchos con la forma que funciona**.

### Tres piezas nuevas, con la forma probada

| Formato | Gancho | De dónde sale |
|---|---|---|
| **Reel** | «Conectaste Claude a Revit y sigue sin servirte. Falta un paso.» | la forma de «ya lo tienes y no lo sabes» (12,46 c/1k) |
| **Carrusel** | «5 cosas que Claude sí hace en Revit. Y la que no va a hacer nunca.» | la forma de la frontera (11,58 c/1k) |
| **Reel** | «Le pedí a Claude que modelara una viga. Falló donde importa.» | la forma de «falla donde tú vales» (17,79 c/1k) |

Las tres con **CTA de palabra**, que es lo que convierte el comentario en lead.
Y la palabra necesita un recurso detrás **antes** de publicar — regla 1 del
agente, la del post de conexiones.

### Y lo que hay que decidir

**Con qué se mide el mes.** Si es vistas, OBRA gana siempre y septiembre va a
parecer un retroceso. La propuesta es medir **comentarios por mil vistas** y
**leads por pieza**, y dejar las vistas como dato de contexto.

No es maquillar el número: es que el objetivo del mes son citas, y las vistas
de obra no traen ninguna.
