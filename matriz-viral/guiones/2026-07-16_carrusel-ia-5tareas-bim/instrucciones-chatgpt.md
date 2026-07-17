# Cómo generar el carrusel con ChatGPT (paso a paso)

Usa un chat de ChatGPT **con generación de imágenes activada**. Genera **un slide
por mensaje** (no los 8 de golpe): así el texto sale mucho más limpio.

> ⚠️ Realista: ChatGPT dibuja bien el estilo pero a veces se equivoca en textos
> largos o acentos. Por eso cada slide lleva **poco texto**. Si un slide sale con
> una palabra mal, responde: *"Regenera manteniendo el mismo estilo y corrige el
> texto EXACTO a: …"*.

---

## Paso 1 — Pega esto primero (fija el estilo de marca)

```
Vas a ayudarme a crear un carrusel de Instagram de 8 imágenes para mi academia
"Design Modeling Academy" (BIM + Inteligencia Artificial para ingenieros y
arquitectos). Todas las imágenes deben compartir EXACTAMENTE el mismo estilo:

- Formato vertical 4:5 (o 1024x1536 y lo recorto). 
- Fondo azul marino oscuro degradado (#0E2438 a #0A1B2B), con un sutil brillo azul
  arriba a la derecha.
- Acento naranja (#EE8A3C) para resaltar palabras clave y números.
- Tipografía sans serif geométrica, gruesa, moderna, muy legible. Texto en español
  con acentos correctos.
- Estilo minimalista, mucho espacio, una sola idea por slide. Nada de fotos de
  stock ni gente. Sin marcas de agua.
- Abajo a la izquierda, pequeño: "DG · @design_modeling_dg".
- Arriba a la derecha, pequeño: el número de slide (ej. "2/8").

Te iré pasando el texto de cada slide. Genera UNA imagen por mensaje, respetando
el texto al pie de la letra. ¿Listo? Empecemos con el slide 1.
```

---

## Paso 2 — Un prompt por slide (texto EXACTO entre comillas)

**Slide 1/8 — Portada (hook)**
```
Slide 1/8. Portada. Arriba, etiqueta pequeña naranja: "BIM + IA". Título grande,
en 3 líneas, con "5 tareas" y "jamás" en naranja:
"La IA ya hace 5 tareas de tu trabajo BIM. La 6ta, jamás."
Abajo, en naranja más chico: "Desliza y checa cuáles ya podrías delegar →".
```

**Slide 2/8**
```
Slide 2/8. Número grande "01" en contorno naranja arriba. Título:
"Detecta choques antes de que lleguen a obra".
Texto de apoyo: "Cruza estructura, instalaciones y arquitectura en tu modelo y
encuentra las interferencias antes de que aparezcan en campo (y cuesten miles)".
```

**Slide 3/8**
```
Slide 3/8. Número grande "02" en contorno naranja. Título:
"Crea familias y parámetros describiéndolos".
Texto de apoyo: "Le dices en palabras qué necesitas y te arma o ajusta familias y
parámetros en Revit. Menos clics, más modelo".
```

**Slide 4/8**
```
Slide 4/8. Número grande "03" en contorno naranja. Título:
"Saca tablas, cantidades y planos del modelo".
Texto de apoyo: "Genera cómputos, anotaciones y documentación directo del modelo
en minutos, no en tardes enteras".
```

**Slide 5/8**
```
Slide 5/8. Número grande "04" en contorno naranja. Título:
"Vincula el modelo con el tiempo (4D)".
Texto de apoyo: "Conecta el modelo con el cronograma y anticipa choques de
secuencia y retrasos antes de que pasen en campo".
```

**Slide 6/8**
```
Slide 6/8. Número grande "05" en contorno naranja. Título:
"Revisa estándares y normativa por ti".
Texto de apoyo: "Audita si tu modelo cumple el estándar BIM del proyecto y te
señala exactamente qué corregir".
```

**Slide 7/8 — El giro**
```
Slide 7/8. Arriba: "Y la 6ta, la que la IA NUNCA hará:". En el centro, enorme y en
naranja: "El CRITERIO." Abajo, texto: "Decidir qué está bien, qué es seguro y qué
cumple de verdad. La IA te da el punto de partida en segundos; la responsabilidad
técnica sigue siendo tuya".
```

**Slide 8/8 — CTA**
```
Slide 8/8. Centrado. Arriba: "¿Quieres usar la IA en tus proyectos BIM con criterio
profesional?". En el centro, grande y en blanco con las palabras entre comillas en
naranja: 'Comenta "BIM" o "IA"'. Abajo: "y te mando cómo lo aplicamos en el
Máster BIM + IA". Pie: "Design Modeling Academy".
```

---

## Paso 3 — Consejos para que salga perfecto
- Si el texto sale con errores: *"Corrige el texto a EXACTAMENTE: … (mismo estilo)"*.
- Pídele que use **los mismos colores y tipografía del slide anterior** para que el
  carrusel se vea uniforme.
- Descarga cada imagen y súbelas en orden 1 → 8.
- El **caption** ya lo tienes (está en el visor del carrusel y en `guion.md`).

## Alternativa (si el texto se complica en ChatGPT)
Usa ChatGPT solo para el **fondo y el estilo** (sin texto), y luego escribe los
textos encima en **Canva** con una plantilla 1080×1350. Es lo más confiable para
que las tildes y los párrafos queden perfectos. Los textos exactos están arriba.
