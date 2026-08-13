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
   style="--img:url('URL_DE_LA_IMAGEN')">
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

## C · La imagen de la tarjeta

- **Medidas: 1280 × 720 px** (16:9), PNG o JPG, **fondo claro**.
- Se muestra con `background-size: contain`, así que **no se recorta**: lo que
  exportes es lo que se ve entero.
- Idea: interfaz de Revit al fondo con velo azul marino `#001e30`, el panel del
  Autodesk Assistant destacado, y el título en dos líneas con «IA» en naranja
  `#ca7520`. Mismo estilo que la portada del carrusel del 4 de agosto, para que
  se lea como continuación de ese post.

## D · Cerrar el círculo con el post que ya está publicado

1. **Responder cada comentario** del post del 4-ago con el enlace del artículo.
2. **Fijar un comentario**: *"Ampliamos esto en el blog con el paso a paso real
   y una aclaración importante sobre en qué versión de Revit está cada función
   → [enlace]"*.
3. Quien haya comentado «BIM» o «IA» ya está en el bot: **mandarles el enlace
   por DM**, que es lo que se les prometió.
4. **Corregir el guion `jul-listicle-revit-ia`** en `guiones-completos.json`
   para que no se vuelva a publicar con las 3 funciones como están.
