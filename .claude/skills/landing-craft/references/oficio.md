# El suelo de oficio

Se lee antes de escribir markup, no después. No se anuncia la lista: se construye
cumpliéndola.

Todo lo de aquí se comprueba **sobre el resultado renderizado**, no sobre la
intención. «Usé una escala de espaciado» no es prueba; un valor calculado sí.

---

## Espaciado

El ritmo sale del contraste entre lo apretado y lo generoso, nunca de un valor
repetido hasta que todo pesa igual. Si no puedes señalar cuáles son los intervalos
apretados y cuáles las respiraciones, la página no tiene ritmo.

- **Más espacio encima de un título que debajo.** El hueco pertenece al límite
  entre secciones, no al par título-cuerpo. Al revés es el error de espaciado más
  común y hace que la página se lea como una lista.
- El padding de sección es fluido. Un teléfono no hereda el aire del escritorio:
  8 rem de padding en 375 px es un impuesto al scroll.
- Agrupa por proximidad antes de meter un contenedor. Si pusiste un borde para
  mostrar que dos cosas van juntas, el espaciado estaba mal primero.
- Los márgenes laterales escalan con la pantalla. La imagen a sangre llega al
  borde; el texto nunca.

**Óptico, no matemático.** Un padding igual alrededor de una forma con peso visual
desigual se ve mal. Se corrige contra el render, no contra el número.

---

## Tipografía

En DMA las dos familias ya están decididas y no se tocan: **Overpass** (titulares
y UI) y **Nunito** (cuerpo). Una tercera es un disfraz.

- **El tracking se cierra cuando el tamaño crece.** Overpass a 6 rem con tracking
  por defecto se lee suelto y amateur. Es corrección óptica, no decoración.
- **Medida de línea de 45 a 75 caracteres.** Un párrafo a todo el ancho en un
  monitor de 1600 px no se lee, por grande que sea la fuente.
- **Interlineado inverso a la medida.** Líneas más anchas piden más aire.
  Titulares 0,94-1,06; cuerpo 1,6.
- **Texto claro sobre fondo oscuro pide compensación en tres ejes**: un poco más
  de interlineado, un poco más de tracking y un paso más de peso. Nuestro navy
  `#001e30` con métricas de modo claro se ve fino y borroso.
- `text-wrap: balance` en titulares, `pretty` en cuerpo. Es gratis y quita la
  palabra huérfana que hace que un titular parezca accidental.
- **Baja el hero un escalón por debajo de 700 px.** Un titular que en escritorio
  ocupa dos líneas, a 390 px se parte en seis. Es el fallo que más se escapa.

---

## Color

La paleta DMA es fija: `--azul-principal: #003e5c`, `--naranja: #ca7520`,
`--azul-navy: #001e30`. Lo que hay que cuidar son los **roles**, no los valores.

- **Seis roles, un acento.** Lienzo, superficie, tinta, tinta suave, acento,
  tinta-sobre-acento. El acento manda en una zona o en un rol; acentos pequeños
  repartidos por todas partes son confeti.
- **El acento no cambia a mitad de página.** El naranja es el naranja en la
  sección 1 y en la 7.
- **El texto secundario va teñido, nunca gris plano.** Se deriva del azul o de la
  superficie. Un `#888` sobre nuestro azul se ve sucio.
- **Nada de negro puro.** `#000` no tiene aire. Como mínimo, el navy.
- Contraste medido sobre el render: cuerpo ≥ 4.5:1, texto grande ≥ 3:1, controles
  y foco ≥ 3:1.

**El naranja de DMA necesita DOS tonos, y esto ya está medido (12-sep-2026).**
`#ca7520` sobre blanco da **3,46:1**: pasa para texto grande, falla para todo lo
que sea cuerpo, botón pequeño, eyebrow o etiqueta. Y el ámbar `#e8a04a` sobre
blanco da **2,2:1**, que no pasa nada.

| Sobre fondo… | Tono | Medido |
|---|---|---|
| claro (texto pequeño, botones, eyebrows, ✓) | `#a7611b` | 4,81:1 |
| navy (el hero, el footer) | `#e8a04a` | 7,78:1 |
| claro, solo decoración y texto grande | `#ca7520` | 3,46:1 |

Es el mismo tono con dos luminosidades, que es lo que toca cuando una página
corta entre fondo claro y fondo oscuro: con un solo valor es **físicamente
imposible** pasar 4,5:1 en los dos. Un solo tono por fondo, un solo tono de
naranja en toda la página.

Cuidado con la clase compartida: si `.tick` se usa en el hero azul y también en
una sección blanca, necesita las dos reglas. Poner una sola arregla la mitad de
la página y rompe la otra, que es exactamente lo que pasó al arreglarlo la
primera vez.

**Redefinir una variable de color en una subsección no re-tiñe el texto que hay
debajo.** `color` se hereda como valor ya calculado, así que el texto cuyo `color`
se resolvió en `<body>` mantiene el del body por mucho que la sección redefina la
variable. Falla en silencio. Se arregla con una declaración en la misma subsección:

```css
.seccion--clara { --tinta: #001e30; --tinta-suave: #4a5f73; color: var(--tinta); }
```

Donde redefinas el token, vuelve a declarar `color`.

---

## Texto sobre imagen

«Nada de velo a pantalla completa» es la regla. Lo que se hace en su lugar, según
dónde esté el texto:

1. **Una esquina** de densidad, del tamaño del bloque de copy. Un degradado de
   borde tiene que oscurecer una franja entera para tapar una esquina; el de
   esquina pone la densidad donde está el texto y deja la foto en paz.
2. **Una banda**, transparente por encima del 58 %, cuando el copy ocupa todo el
   ancho. Es en lo que se convierten las dos esquinas por debajo de 860 px.
3. **Una columna** de densidad bajo una columna de texto, cuando el copy ocupa un
   lado de una imagen a sangre.

Y el caso positivo detrás de los tres: cuando hay una foto detrás de una columna
de texto, **enmascara la imagen lejos del texto** en vez de poner algo encima. Un
`mask-image` que termina donde empieza la columna le da al texto un fondo limpio y
le devuelve a la foto todo su contraste. Es mejor que cualquier velo.

**`width` y `height` en un `<img>` van en pareja.** Reservan la proporción y
evitan que la página salte al cargar. La trampa: sobrescribir solo uno en CSS deja
al otro resolviendo el valor del atributo, así que `width: 100%` en una imagen de
1920x1080 dentro de una columna estrecha la renderiza de 1080 px de alto y empuja
todo lo de abajo fuera de la pantalla. Parece un error de maquetación a tres
elementos de distancia de su causa. **Sobrescribe los dos o ninguno**, normalmente
`width: 100%; height: auto`.

Y después mídelo. Un velo ajustado a ojo suele quedar en 9:1 donde bastaba 4,5:1
—una foto tirada a la basura para nada— o en 2,8:1 justo en la zona clara.

---

## Profundidad

Es el eje que separa una página premium de un documento con estilos, y no es una
sola propiedad. Cinco herramientas, juntas:

1. **Sombra con desplazamiento y desenfoque.** Lo que está levantado proyecta
   hacia abajo. Un halo de color sin desplazamiento es decoración, no profundidad.
   Tiñe la sombra al tono del fondo: una sombra negra pura sobre color se ve sucia.
2. **Luz de canto.** Un resalte de 1 px arriba vende una superficie elevada mejor
   que cualquier desenfoque, porque los bordes reales atrapan luz.
3. **Escala y desenfoque como distancia.** Lo lejano es más pequeño, más suave y
   con menos contraste.
4. **Solape.** Un elemento cruzando el borde de otro da más profundidad que
   cualquier sombra. Es gratis y se usa poco.
5. **Grano.** Un fondo oscuro plano hace bandas en pantallas reales. Un 4-5 % de
   grano es la diferencia entre «una página oscura» y «una habitación con luz».

Tres niveles de elevación y no más. Si todo está elevado, nada lo está.

---

## Tarjetas

La tarjeta es el contenedor perezoso. Antes de usar una, pregunta qué está
haciendo que no hicieran la proximidad, una línea fina o el espacio.

- **Nunca una rejilla de tarjetas idénticas icono + título + texto como estructura
  de la página.** Es la señal más reconocible de página hecha con IA.
- **Nunca tarjetas anidadas.**
- **Nunca tres columnas iguales de tarjetas.** Rejilla asimétrica, zigzag de dos
  como mucho, un riel, o tipografía sobre espacio.
- Si una rejilla queda con una celda vacía al final, estaba mal planteada. Se
  reforma; no se pega un cuadro en blanco.
- Un solo radio de esquina en toda la página. Botones tipo píldora en una página
  de tarjetas cuadradas está roto, no es ecléctico.

---

## Movimiento

- `transform` y `opacity` para todo lo continuo. `clip-path` es el tercero
  permitido, para barridos. Nunca animar `width`, `height`, `margin`, `padding`,
  `top` o `left`, y nunca `transition: all`.
- **Nunca `ease-in` en la interfaz.** Retrasa el momento en el que el ojo ya está.
  Un `ease-out` de 200 ms se siente más rápido que un `ease-in` de 200 ms.
- **Transiciones de interfaz por debajo de 300 ms.** Hover 120-180 ms, botones
  100-160 ms.
- **Nunca `scale(0)`.** Entra desde `scale(0.95)` + `opacity: 0`. Nada en el mundo
  real aparece de la nada.
- Respuesta al pulsar en todo lo pulsable: `scale(0.97)` o `translateY(1px)`.
- Escalonar entradas de grupo entre 30 y 80 ms. Más se siente lento.
- El hover se limita a `(hover: hover) and (pointer: fine)`; el táctil dispara
  hovers falsos al tocar.
- Movimiento reducido significa **menos y más suave, no cero**. Se mantiene la
  opacidad que ayuda a entender y se quita todo cambio de posición.

---

## Estados y contenido

- Todo elemento interactivo tiene hover, focus-visible, active y disabled. Una
  página con solo el estado en reposo está a medio construir.
- **El foco tiene que verse.** Con el color de acento y con separación.
- **El texto del botón cabe en una línea en escritorio.** Un CTA partido está
  roto. Una a tres palabras.
- **Una etiqueta por intención.** «Quiero información» en el nav y «Hablar con un
  asesor» en el footer son el mismo botón con dos nombres. Se elige uno.
- Copy real, no lorem. Nombres reales, no «Juan Pérez».
- **Nada de estadísticas inventadas.** La precisión falsa (`4,1×`, `92 %`, `48k`)
  es un problema de credibilidad y, en una academia que vende formación técnica,
  también legal. Es la regla 1 de la casa y aquí se repite porque las plantillas
  de landing traen huecos de estadística que invitan a rellenarlos.

---

## Las superficies del navegador

Lo que no dibujaste también lleva el diseño, y es la señal más barata de que una
página se construyó en vez de ensamblarse. Es también el paso que más se salta:

color de selección, color del cursor de texto, anillo de foco, barra de scroll,
separación y grosor del subrayado, y números tabulares en lo que cuente o tabule.

---

## La lista de lo que no se hace

Son valores por defecto de categoría, no prohibiciones de principio. El brief
puede justificar cualquiera; echar mano de una cuando el eje está libre significa
que no estabas decidiendo.

**Estructura**
- Tarjetas idénticas como estructura. Tarjetas anidadas. Tres columnas iguales.
- La plantilla del número gigante: cifra enorme, etiqueta pequeña, estadísticas de
  apoyo, acento.
- Más de dos secciones seguidas de imagen-izquierda / texto-derecha.
- La misma familia de maquetación dos veces en una página.

**Etiquetas**
- Un eyebrow encima de cada título. Como mucho uno cada tres secciones.
- Números de sección (`01 / 06`) salvo que la secuencia sea información necesaria.
- Señales de scroll: «scroll», «↓», ratones animados. Están mirando el hero.
- Tiras de texto decorativo cruzando el hero.
- Píldoras y etiquetas encima de fotos.

**Superficie**
- Texto degradado. Neón y glows. Sombras duras sin desenfoque.
- Cristal y desenfoque como decoración en vez de como efecto concreto.
- `border-left` de color de más de 1 px en tarjetas o avisos.
- Monoespaciada como disfraz de «técnico» en vez de para código, datos o etiquetas.
  En DMA esto es especialmente fácil de hacer mal: somos técnicos de verdad, así
  que la monoespaciada tiene que ganarse su sitio.
- Emojis haciendo de sistema de iconos.
- Cursores personalizados.

**Contenido**
- Raya larga (—) visible. Punto, coma, dos puntos o paréntesis.
- Capturas falsas, paneles falsos, terminales falsas hechas con divs.
- Texto quemado dentro de una imagen generada.
- Verbos de relleno: potencia, revoluciona, impulsa, lleva al siguiente nivel.
- Un hero que desborda la pantalla. Titular de dos líneas como máximo, subtexto de
  20 palabras, CTA visible sin bajar.
- Más de cuatro elementos de texto en el hero.

---

## La prueba del entrecerrado

Difumina la página hasta perder el detalle. Todavía deberías poder nombrar el
elemento principal, el secundario y los grupos grandes, en ese orden.

Si todo se funde en un campo gris uniforme, el problema es de jerarquía, y no lo
arregla ninguna cantidad de sombra, degradado ni movimiento.
