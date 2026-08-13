# Artículo de blog — «La IA de Revit, paso a paso»

**Por qué existe:** el post del **lunes 4 de agosto** (`jul-listicle-revit-ia`)
cierra prometiendo *"Comenta BIM o IA y te mando cómo activarlas **paso a
paso**"*. Ese paso a paso no existe. Este archivo lo resuelve.

**Verificado el 11-ago-2026** contra la documentación oficial de Autodesk
(help.autodesk.com + base de conocimiento de soporte).

---

## 🚨 PRIMERO: lo que hay que saber antes de escribir nada

Al ir a documentar el paso a paso, las 3 funciones que promete el post **no
resisten la verificación**. Esto es lo que dice Autodesk, textual:

> **«What are Revit AI-driven features in Revit?»** →
> *"As of Revit 2026 version, there are no AI driven features."*
> ([artículo de soporte de Autodesk](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-are-Revit-AI-driven-features-in-Revit.html))

### Las 3 promesas, una por una

| Lo que dice el post | Qué encontré | Veredicto |
|---|---|---|
| **01 · «Genera detalles constructivos — con Autodesk AI Assist le describes el detalle y te arma la primera versión»** | No existe ningún «Autodesk AI Assist» que genere detalles constructivos en Revit. Los detalles se dibujan en vistas de dibujo (*drafting views*), a mano. Lo más parecido —*Automated Drawings*— está en **Fusion**, no en Revit | ❌ **No existe** |
| **02 · «Detecta y RESUELVE choques — te sugiere la solución más común según miles de proyectos»** | Revit tiene **Interference Check** y ACC tiene **Model Coordination**. Los dos **detectan**. Ninguno sugiere solución, y no hay IA documentada en ninguno | ❌ **La mitad es falsa** (detecta sí, resuelve no) |
| **03 · «Propone distribución en planta — le das los m² y te da 3 layouts en segundos»** | Esto **sí existe**: se llama **Generative Design in Revit**. Pero no es conversacional, requiere un *study type* preparado en Dynamo, y solo lo tienen los suscriptores de la **AEC Collection** | 🟡 **Existe, pero no funciona así** |

### Lo que sí es verdad y el post no menciona

**Autodesk Assistant** — es IA de verdad, conversacional, y **sí automatiza
tareas dentro de Revit**. Pero:

> *"Autodesk Assistant is currently available only in **Revit 2027**"* — y está
> en **Tech Preview**.

O sea: la premisa «tu Revit ya tiene IA adentro» **solo es cierta si tienes
Revit 2027**. Quien esté en 2026 o antes no tiene nada de esto.

### Qué hacer con el post que ya está publicado

**Mi recomendación: no borrarlo.** Tiene alcance y comentarios, y borrarlo se
nota más que corregirlo. Tres cosas, en este orden:

1. **Publicar este artículo** y responder a cada comentario con el enlace. El
   artículo es más honesto que el post y eso **juega a favor** — es
   exactamente el posicionamiento de la academia.
2. **Comentario fijado** en el post: *"Ampliamos esto en el blog con el paso a
   paso real y una aclaración importante sobre qué versión de Revit lo trae →
   [enlace]"*.
3. **Corregir el guion en la matriz** para que no se vuelva a publicar igual.
   La pieza `jul-listicle-revit-ia` está en `guiones-completos.json`.

Y una regla nueva para `RECOMENDACIONES.md`:

> **Toda afirmación técnica sobre una función de software se verifica contra la
> documentación oficial antes de publicarse.** Vendemos formación técnica: la
> credibilidad *es* el producto. Un carrusel que promete funciones que no
> existen se lo desmonta cualquier ingeniero en los comentarios.

---

# 📄 EL ARTÍCULO (listo para pegar)

**Título:** La IA de Revit, paso a paso: qué trae de verdad y cómo activarlo

**Slug sugerido:** `ia-en-revit-paso-a-paso-como-activarla`

**Meta descripción (155 car.):** Qué funciones de IA trae Revit realmente, en
qué versión, y el paso a paso para activarlas. Sin humo: también lo que no hace.

**Categoría:** BIM + IA · **Tiempo de lectura:** 6 min

---

## Antes de empezar: la verdad incómoda

Si buscas «IA en Revit» vas a encontrar mil publicaciones prometiendo cosas
espectaculares. Vamos a empezar por donde nadie empieza: **por lo que Autodesk
dice oficialmente.**

En su propia base de conocimiento, respondiendo a la pregunta «¿qué funciones
de IA tiene Revit?», Autodesk contesta:

> *"A partir de la versión Revit 2026, no hay funciones impulsadas por IA."*

Léelo otra vez. **Hasta Revit 2026 inclusive, no hay IA integrada en Revit.**

Entonces, ¿de qué habla todo el mundo? De dos cosas que sí existen, cada una con
su letra pequeña. Vamos con las dos, paso a paso.

---

## 1 · Autodesk Assistant — la IA de verdad (solo en Revit 2027)

Esta es la que sí es inteligencia artificial en el sentido que te imaginas:
le escribes en lenguaje normal y hace cosas.

**Requisitos, sin rodeos:**
- **Revit 2027.** En versiones anteriores no está y no se puede instalar.
- Cuenta de Autodesk con sesión iniciada.
- Está en **Tech Preview**: Autodesk lo da por funcional pero en evolución.

### Paso a paso para activarlo

1. **Abre Revit 2027 e inicia sesión** con tu cuenta de Autodesk. Sin sesión
   iniciada no aparece.
2. **Busca el icono de Autodesk Assistant** en la barra de título, junto al
   InfoCenter (arriba a la derecha). Haz clic.
   - ¿No lo ves? Ve a **View → User Interface → Autodesk Assistant**.
   - ¿Sigue sin aparecer? Cierra Revit y vuelve a abrirlo. Normalmente está
     abierto por defecto cuando has iniciado sesión.
3. **Activa el Tech Preview.** Esto es lo importante y donde casi todos se
   quedan a medias. Dentro del panel del Assistant, entra en **Settings** y
   enciende el Tech Preview.
   - **Sin Tech Preview**, el Assistant solo responde preguntas de ayuda.
   - **Con Tech Preview**, puede consultar tu modelo y ejecutar tareas.
4. **Acomoda el panel.** Se comporta como cualquier paleta de Revit: lo puedes
   arrastrar, apilarlo con Propiedades y el Navegador de proyectos, o mandarlo
   a un segundo monitor. También le puedes asignar un atajo de teclado.

### Qué le puedes pedir (esto sí funciona)

**Ayuda contextual** — «¿Cómo creo una vista de sección?»

**Consultar el modelo** — sin contar a mano:
- «¿Cuántas columnas hay en la planta baja?»
- «Encuentra todas las puertas del Nivel 1»

**Automatizar tareas** — aquí está el ahorro real:
- «Crea una tabla de planificación de puertas»
- «Crea una planta para el Nivel 2»

Autodesk documenta seis grupos de herramientas que el Assistant maneja:
consulta del modelo, exportación, gestión de láminas y documentación, gestión
de recintos, tablas y datos, y operaciones sobre elementos.

### Un ejemplo real, encadenado

Este es el flujo que la propia Autodesk demuestra. Fíjate que son órdenes
seguidas, en lenguaje normal:

```
Crea una nueva planta para el Nivel 1 llamada "L1-AI"
Aplica una plantilla de vista apropiada
Etiqueta todos los recintos de la vista
Repite el mismo proceso para los Niveles 2 y 3
Crea láminas nuevas y coloca cada planta en su propia lámina
Añade "Demo" al inicio del nombre de cada lámina
Imprime las láminas nuevas a un archivo PDF
```

Eso es una tarde de trabajo repetitivo resuelta escribiendo siete frases.
**Ahí está el valor real**, no en los renders mágicos.

### Lo que tienes que saber antes de confiarte

- **Tú apruebas los cambios.** El Assistant no toca el modelo sin que se lo
  pidas o confirmes.
- **Puede equivocarse.** Autodesk lo dice explícitamente: las respuestas
  generadas por IA pueden ser incompletas o incorrectas. **Verifica siempre.**
- **No se puede desinstalar** ni desactivar del todo. Si no lo quieres usar,
  cierras el panel.
- **Tu conversación y tu historial** se guardan en la nube asociados a tu
  cuenta. Autodesk afirma que no se usan para entrenar modelos.

---

## 2 · Generative Design — lo de los layouts (y su letra pequeña)

Esta es la función detrás de «le doy los metros y me da opciones de
distribución». Existe, funciona, y lleva años en Revit. Pero **no es IA
conversacional**: es optimización. Le das metas, restricciones y variables, y
el computador genera y evalúa cientos de alternativas.

**Requisitos:**
- Suscripción a la **AEC Collection** (u otro acceso específico). Sin eso, el
  panel no aparece en la cinta.
- **No está en Revit LT.** Nunca.
- Hace falta un **study type**: un archivo `.DYN` de Dynamo con su carpeta
  `Dependencies`. Revit trae ejemplos en la carpeta *Autodesk Samples*.

### Paso a paso

1. **Abre el modelo** y prepáralo. Ten abierta una vista donde se vean los
   elementos que el estudio necesita seleccionar.
2. **Manage → panel Generative Design → Create Study.**
   - ¿No ves el panel Generative Design en la pestaña Manage? No tienes acceso.
     Puedes hacer algo equivalente con **Dynamo for Revit**.
3. **En «Choose Folder»**, elige la carpeta con el study type. Los ejemplos de
   Autodesk están en *Autodesk Samples*. Para añadir la tuya, *Add Folder*.
4. **Selecciona el study type y define el estudio**: el método (optimizar,
   aleatorizar…), las variables de entrada y las metas.
5. **Espera.** Puedes seguir trabajando mientras genera; las opciones van
   apareciendo. Cuánto tarda depende de cuántas generaciones pidas.
6. **Explora los resultados** en *Explore Outcomes*. Cada opción es un modelo 3D
   con sus valores de entrada y de salida, y vienen ordenadas según tus metas.
7. **Integra la ganadora**: con la opción seleccionada, pulsa **Create Revit
   Elements**. El modelo se actualiza con esa solución.

Si el resultado no te convence, cambias metas o variables y vuelves a lanzar.
Ese ciclo es el trabajo real.

---

## 3 · Lo que Revit NO hace (aunque lo hayas leído por ahí)

Con la misma honestidad:

**❌ No genera detalles constructivos con IA.** No existe esa función. Los
detalles se dibujan en vistas de dibujo con las herramientas de detallado, o se
toman de una biblioteca de detalles. Punto.

**❌ No resuelve los choques.** Revit tiene **Interference Check** y ACC tiene
**Model Coordination**: te dicen *dónde* está el choque. **Decidir qué se mueve
sigue siendo trabajo de un coordinador.** Ningún software documenta hoy
sugerirte la solución.

**❌ El Assistant no navega por internet** por defecto, así que no busca normas
ni catálogos por su cuenta.

---

## Y esto es lo importante

Ninguna de estas herramientas te da el proyecto. Te dan **el primer borrador,
más rápido**.

El Assistant te ahorra la tarde de crear láminas y tablas. Generative Design te
ahorra dibujar veinte alternativas para descubrir que la buena era la tercera.
Pero **quién decide si la solución sirve, si cumple la norma y si se puede
construir, sigues siendo tú.**

Esa es exactamente la diferencia entre saber usar el software y ser el
profesional que decide. Lo primero se está automatizando. Lo segundo, no.

---

## ¿Y ahora qué?

Si quieres aprender a integrar esto en un flujo de trabajo completo —no como
truco suelto, sino como método— echa un vistazo a nuestros recursos gratuitos:

👉 **[Todos los recursos gratis](https://funnel.dgdesignmodeling.com/recursos)**

Y si quieres saber en qué nivel BIM estás realmente antes de decidir qué
estudiar, tenemos un test de 20 preguntas que te lo dice sin adornos:

👉 **[Test de Nivel BIM](https://funnel.dgdesignmodeling.com/test-nivel-bim)**

💬 **¿Ya probaste alguna de estas funciones? ¿En qué versión de Revit estás?**
Cuéntamelo en los comentarios — tengo curiosidad de saber cuántos ya están
en 2027.

---

### Fuentes

Toda la información técnica sale de la documentación oficial de Autodesk:

- [What AI features are available in Revit?](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-AI-features-are-available-in-Revit.html)
- [What are Revit AI-driven features in Revit](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-are-Revit-AI-driven-features-in-Revit.html)
- [Autodesk Assistant in Revit (Tech Preview)](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-Assistant/files/GUID-620ECD98-53F7-47F1-B700-EEE84F15EBF7.html)
- [How to enable Autodesk Assistant in Revit](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-enable-Autodesk-Assistant-in-Revit.html)
- [Create a Study Using Generative Design in Revit](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-GDiR/files/GUID-2519E7FD-8992-49F6-9F4F-CBA17E1AB991.htm)
- [Workflow: Generative Design](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-GDiR/files/GUID-8ACC2154-54C4-4929-951C-376CF3411A95.htm)
- [What can Autodesk Assistant do?](https://help.autodesk.com/cloudhelp/ENU/Assistant-User-Guide/files/assistant-topics/AA_Capabilities.html)

*Última verificación: 11 de agosto de 2026. Autodesk cambia estas funciones con
frecuencia; si encuentras algo distinto en tu versión, escríbenos.*

---
---

# 🔧 MONTAJE — cómo subirlo

## A · Publicarlo en el blog de GHL

1. **Sites → Blogs → New Post**
2. **Título:** `La IA de Revit, paso a paso: qué trae de verdad y cómo activarlo`
3. **URL slug:** `ia-en-revit-paso-a-paso-como-activarla`
   → queda en `https://funnel.dgdesignmodeling.com/post/ia-en-revit-paso-a-paso-como-activarla`
4. **Meta descripción:** la de arriba (155 caracteres, ya medida)
5. **Categoría:** BIM + IA · **Autor:** Design Modeling Academy
6. Pega el cuerpo desde «Antes de empezar» hasta «Fuentes».
7. **Imagen destacada:** ver punto C.
8. **Publicar** y copiar la URL final.

> **Ojo con los enlaces a Autodesk:** ponlos con `target="_blank"` para que no
> se lleven al lector fuera del sitio. Y **déjalos**: son la prueba de que el
> artículo está verificado, que es todo su valor.

## B · Añadirlo al hub de recursos

En `recursos/index.html`, sección **ARTÍCULOS** (ahora tiene 3 tarjetas). Se
copia una tarjeta existente y se cambian tres cosas:

```html
<a class="card" href="https://funnel.dgdesignmodeling.com/post/ia-en-revit-paso-a-paso-como-activarla"
   style="--img:url('https://d8j0ntlcm91z4.cloudfront.net/user_3DHYHNPN9mWRQrSP8pMrjtnrcPd/hf_20260813_163210_2936e922-71bc-4a1f-b4cf-502f7ed4fa74.png')">
  <span class="foto"></span>
  <span class="txt">
    <strong>La IA de Revit, paso a paso</strong>
    <em>Qué trae de verdad, en qué versión, y cómo activarlo. Con lo que no hace.</em>
  </span>
</a>
```

Tres avisos, de los errores que ya cometimos con este hub:

- El `href` va **escrito en el HTML**, no inyectado por JavaScript. Si no,
  Google y la vista previa de WhatsApp no lo ven.
- La imagen va como variable `--img` en el `style`, **sin barras invertidas**
  antes de las comillas.
- El script oculta las tarjetas que sigan en `href="#"`. Si se te queda así,
  la tarjeta desaparece y parece que no se subió.

## C · Las imágenes — ✅ YA GENERADAS (13-ago-2026)

**Las 4 que se podían generar están hechas y revisadas una por una.** Se
descargan de estos enlaces y se suben a GHL tal cual — **no hay que retocarlas
ni pasarlas por Canva**, el texto ya va dentro y está bien escrito.

| # | Qué es | Enlace | Medidas |
|---|---|---|---|
| **C1** | **Portada** — «La IA de Revit / paso a paso» | [descargar](https://d8j0ntlcm91z4.cloudfront.net/user_3DHYHNPN9mWRQrSP8pMrjtnrcPd/hf_20260813_163210_2936e922-71bc-4a1f-b4cf-502f7ed4fa74.png) | 1376 × 768 |
| **C2** | Línea de tiempo con los rótulos y la fuente | [descargar](https://d8j0ntlcm91z4.cloudfront.net/user_3DHYHNPN9mWRQrSP8pMrjtnrcPd/hf_20260813_163403_29606539-c764-4ff3-a820-eb55f56f166a.png) | 1376 × 768 |
| **C4** | Generative Design — 9 plantas, 1 elegida | [descargar](https://d8j0ntlcm91z4.cloudfront.net/user_3DHYHNPN9mWRQrSP8pMrjtnrcPd/hf_20260813_163210_68fbabe1-a0f7-48d9-93fa-6b2a0b353d7d.png) | 1376 × 768 |
| **C5** | «Lo que NO hace» — el choque sin resolver | [descargar](https://d8j0ntlcm91z4.cloudfront.net/user_3DHYHNPN9mWRQrSP8pMrjtnrcPd/hf_20260813_163210_6e1a7e32-2d70-46aa-9785-b6829c8711b9.png) | 1376 × 768 |

> ⚠️ **Los enlaces de Higgsfield caducan.** Descargarlas y subirlas a GHL cuanto
> antes; una vez en `assets.cdn.filesafe.space` ya son permanentes.

**C3 (el panel del Autodesk Assistant) NO está generada, y es a propósito** —
tiene que ser captura real de pantalla. Ver más abajo.

Todas salieron con la paleta de marca: azul `#001e30`, naranja `#ca7520`, crema
`#fafaf7`. Se revisaron una por una antes de darlas por buenas.

---

### Si hubiera que regenerar alguna, estos son los prompts

**Paleta obligatoria** (la de la marca, ya usada en el hub y las landings):

| | |
|---|---|
| Azul marino | `#001e30` |
| Naranja | `#ca7520` |
| Crema de fondo | `#fafaf7` |
| Texto sobre azul | `#c5d6e2` |
| Tipografías | **Overpass** (títulos, 800-900) · **Nunita/Nunito** (texto) |

**Reglas para las 5:** fondo claro o azul marino sólido (nunca degradados
raros) · nada de texto en inglés · nada de manos con seis dedos: si sale gente,
que sea de espaldas o en plano de pantalla · **ninguna imagen debe inventar una
interfaz de Revit que no existe** — si no hay captura real, usar ilustración
abstracta, nunca una UI falsa que parezca real.

---

### C1 · PORTADA (la que va en el blog y en la tarjeta del hub)

**Medidas: 1280 × 720 px** (16:9). PNG. **Fondo claro.**

> ⚠️ En el hub se muestra con `background-size: contain`, así que **no se
> recorta**: lo que exportes es exactamente lo que se ve. Nada pegado al borde.

**Prompt:**
```
Ilustración editorial horizontal 1280x720 para artículo técnico de arquitectura
e ingeniería. Fondo azul marino profundo #001e30. A la izquierda, un panel de
chat estilizado y minimalista (rectángulo redondeado color crema #fafaf7) con
tres líneas de texto simuladas y un cursor naranja #ca7520 parpadeando. A la
derecha, la silueta en wireframe naranja de un edificio en planta, con líneas
finas técnicas. Entre los dos, una flecha delgada naranja. Estilo plano,
geométrico, sin degradados, sin fotografías, sin texto legible. Mucho aire
alrededor. Estética de revista técnica seria, no de banner promocional.
```

**Encima, en Canva o el editor:** el título en Overpass 900,
`La IA de Revit` en crema + `paso a paso` en naranja, dos líneas, alineado a la
izquierda, con margen generoso.

---

### C2 · «Hasta 2026 no hay IA» (va después del primer párrafo)

**Medidas: 1200 × 675 px.** Es la imagen que da credibilidad al artículo — la
que la gente captura y comparte.

**Prompt:**
```
Gráfico informativo minimalista 1200x675, fondo azul marino #001e30. Una línea
de tiempo horizontal con cuatro nodos etiquetados 2024, 2025, 2026, 2027. Los
tres primeros nodos son círculos vacíos grises apagados; el cuarto, el de 2027,
es un círculo relleno naranja #ca7520 y más grande, con un halo suave. Bajo la
línea, mucho espacio vacío para texto. Estilo plano, geométrico, líneas finas,
sin degradados, sin fotografías, sin texto.
```

**Encima:** sobre los 3 primeros → `Sin funciones de IA`. Sobre el de 2027 →
`Autodesk Assistant`. Abajo pequeño: `Fuente: help.autodesk.com`.

---

### C3 · El panel del Autodesk Assistant (sección 1)

**Aquí NO se genera imagen. Se toma una captura real.**

Es lo único del artículo que la gente va a intentar reproducir en su pantalla:
una interfaz inventada por IA sería exactamente el error que este artículo viene
a corregir.

- **Si hay Revit 2027 a mano:** captura de la barra de título con el icono del
  Assistant señalado, y otra del panel abierto con Settings y el Tech Preview
  encendido. 1200 px de ancho mínimo.
- **Si no hay Revit 2027:** usar el diagrama de C2 y **decirlo en el pie**:
  *"Captura pendiente — el Assistant solo está en Revit 2027"*. Honesto y
  coherente con el artículo.

---

### C4 · Generative Design (sección 2)

**Medidas: 1200 × 675 px.**

**Prompt:**
```
Ilustración técnica plana 1200x675, fondo crema #fafaf7. Una cuadrícula de
nueve plantas arquitectónicas esquemáticas en miniatura, dibujadas en línea
fina azul marino #001e30, todas ligeramente distintas entre sí. Una de las
nueve está resaltada con un borde naranja #ca7520 grueso y un fondo naranja muy
tenue. Estilo diagrama de arquitecto, líneas técnicas limpias, sin sombras, sin
degradados, sin texto, sin fotografías. Mucho espacio en blanco entre las
miniaturas.
```

Idea: cientos de alternativas generadas, **una elegida por un humano**. Es la
tesis del artículo en una imagen.

---

### C5 · «Lo que NO hace» (sección 3)

**Medidas: 1200 × 675 px.**

**Prompt:**
```
Ilustración conceptual plana 1200x675, fondo azul marino #001e30. Dos elementos
estructurales lineales que se cruzan formando una intersección, dibujados en
línea fina crema #fafaf7. El punto exacto donde se cruzan está marcado con un
círculo naranja #ca7520 brillante. Sobre el punto de cruce, un signo de
interrogación grande y limpio, tipografía geométrica sans-serif, en naranja.
Estilo diagrama técnico minimalista, sin degradados, sin fotografías, sin más
texto.
```

Idea exacta: el software marca el choque; **la pregunta de qué se mueve sigue
sin respuesta automática**.

---

### Dónde va cada una dentro del artículo

| Imagen | Posición |
|---|---|
| **C1 Portada** | imagen destacada del post + tarjeta del hub |
| **C2 Línea de tiempo** | después de la cita de Autodesk, antes de «¿de qué habla todo el mundo?» |
| **C3 Captura del Assistant** | dentro de «Paso a paso para activarlo», después del punto 3 |
| **C4 Generative Design** | al inicio de la sección 2, antes de los requisitos |
| **C5 Interrogación** | al inicio de la sección 3 |

**Texto alternativo (`alt`) de cada una** — hace falta para SEO y accesibilidad:

- C1: `La IA de Revit paso a paso: qué funciones trae y en qué versión`
- C2: `Línea de tiempo: las funciones de IA en Revit llegan en la versión 2027`
- C3: `Panel de Autodesk Assistant abierto en Revit 2027`
- C4: `Nueve alternativas de planta generadas con Generative Design, una seleccionada`
- C5: `Interferencia entre dos elementos: el software la detecta pero no la resuelve`

---

## D · Que quede PRIMERO en el hub de recursos

Este es el punto crítico: **la persona llega desde el DM y este artículo tiene
que ser el primero que ve.**

En `recursos/index.html`, sección `id="articulos"`, pegar esta tarjeta
**justo después de `<div class="grid g3">`**, antes de la de SAP2000:

```html
      <a class="card" style="--img:url('https://d8j0ntlcm91z4.cloudfront.net/user_3DHYHNPN9mWRQrSP8pMrjtnrcPd/hf_20260813_163210_2936e922-71bc-4a1f-b4cf-502f7ed4fa74.png')" data-url="art0" href="https://funnel.dgdesignmodeling.com/post/ia-en-revit-paso-a-paso-como-activarla">
        <span class="foto"></span>
        <span class="cuerpo">
        <span class="tag">BIM + IA</span>
        <h3>La IA de Revit, paso a paso: qué trae de verdad</h3>
        <p>Qué funciones existen, en qué versión están y cómo activarlas. Con lo que Revit todavía no hace.</p>
        <span class="go">Leer el artículo →</span>
      </span>
      </a>
```

**Tres avisos, de errores que ya cometimos en este mismo hub:**

- El `href` va **escrito en el HTML**, no inyectado por JavaScript. Si no,
  Google y la vista previa de WhatsApp no lo ven.
- La imagen va como `--img` en el `style`, **sin barras invertidas** antes de
  las comillas (`url('...')`, nunca `url(\'...\')`).
- El script oculta las tarjetas que sigan en `href="#"`. Si se te queda así, la
  tarjeta desaparece y parece que no se subió.

**Y una decisión:** con esta pasan a ser **4 tarjetas en una rejilla de 3**, así
que la cuarta baja sola a una segunda fila. Dos salidas:

- **La que recomiendo:** dejarlas en 4. Se ve bien y no se pierde nada.
- Si molesta visualmente, quitar «BIM para todos: más allá de las grandes
  empresas», que es la más genérica de las tres.

**Comprobar después de subirlo:** abrir `/recursos` en el celular y confirmar
que el artículo nuevo es **el primero** de la sección «Del blog» y que el enlace
abre el post.

---

## E · Cerrar el círculo con el post que ya está publicado

1. **Responder cada comentario** del post del 4-ago con el enlace del artículo.
2. **Fijar un comentario**: *"Ampliamos esto en el blog con el paso a paso real
   y una aclaración importante sobre en qué versión de Revit está cada función
   → [enlace]"*.
3. Quien haya comentado «BIM» o «IA» ya está en el bot: **mandarles el DM** con
   el enlace, que es lo que se les prometió. El texto está en la sección F.
4. ✅ **El guion `jul-listicle-revit-ia` ya está corregido** en
   `guiones-completos.json` (11-ago-2026): 8 slides, hook con la versión, un
   slide nuevo de «lo que NO hace», y las notas de producción explican por qué.
   No republicar la versión vieja.

---

## F · El DM que se manda a quien comentó

> Va en el workflow del bot, disparado por el comentario «BIM» o «IA» en **esa
> publicación en concreto**. Dos mensajes: la entrega y, un rato después, la
> pregunta.

**DM 1 — inmediato:**

```
¡Hola! 👋 Aquí está lo que te prometí: el paso a paso completo de las
funciones de IA de Revit 👇

📄 https://funnel.dgdesignmodeling.com/post/ia-en-revit-paso-a-paso-como-activarla

Te aviso de algo antes de que lo abras, porque en el post no cabía:
Autodesk dice en su propia documentación que HASTA REVIT 2026 no hay
funciones de IA. Lo que existe llegó con la 2027.

En el artículo está el paso a paso real de lo que sí funciona (con las
fuentes de Autodesk enlazadas) y también lo que Revit todavía NO hace,
aunque se diga por ahí.

Y si te sirve, aquí están todas nuestras herramientas gratis en un solo
sitio — calculadora de zapatas, test de nivel BIM, ebooks y más:
🎁 https://funnel.dgdesignmodeling.com/recursos
```

**DM 2 — a las 3-4 horas:**

```
¿Alcanzaste a leerlo? 😄

Te hago la pregunta que me interesa de verdad: ¿en qué versión de Revit
estás trabajando?

Te lo pregunto porque es lo que decide qué puedes usar hoy y qué no. Y
según lo que me digas, te apunto por dónde empezar. 👇
```

**Reglas del DM** (las de siempre, para que no se rompa nada):

- **Nunca prometer envío por WhatsApp.** Todo va por enlace, en el mismo DM.
- **No cotizar el Máster.** Si preguntan precio → pasa a una persona.
- Etiquetar a quien entre por aquí con `lead-blog-ia-revit`, para poder medirlo.
- La ventana de mensajería de Meta es de **24 horas**: el DM 2 tiene que salir
  dentro de ese plazo o no llega. Por eso va a las 3-4 h y no al día siguiente.
