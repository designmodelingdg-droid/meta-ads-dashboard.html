# Textos para los bots de palabra clave (IG / FB / WhatsApp)

Lo que el bot debe **saber** y lo que debe **responder** para cada herramienta
gratuita. Copiar tal cual en el workflow de GoHighLevel.

## Reglas que no se rompen

1. **Nunca precio.** Ni del Máster, ni de las especializaciones, ni "desde".
2. **Nunca "inscríbete"** ni cerrar la venta por chat. El objetivo del bot es
   entregar la herramienta y **abrir conversación**.
3. **Nunca llamarlo certificación** ni diploma. Son herramientas gratuitas.
4. **No prometer lo que no existe**: no hay envío por correo automático, no hay
   PDF de resultados. El resultado se ve en pantalla, al momento.
5. Si alguien pregunta precio o quiere inscribirse → **pasar a humano**, no
   improvisar cifras.

---

# 1 · TEST DE NIVEL BIM — palabra clave `NIVEL`

## Qué es (para que el bot lo entienda)

Test gratuito de 20 preguntas que ubica a la persona en uno de los 4 niveles de
la ruta BIM y le dice qué competencias concretas le faltan para el siguiente.

- **Los 4 niveles:** 1) Modelador BIM · 2) Coordinador BIM · 3) BIM Manager
  4D-5D · 4) Especialista BIM+IA.
- **Cómo califica:** 5 preguntas por nivel. Un nivel se domina con 70% o más, y
  se cuentan **en orden**: no se puede ser Coordinador sin dominar Modelador.
  Si alguien va fuerte en 4D-5D pero flojo en coordinación, el test se lo dice
  y lo marca como conocimiento disperso.
- **Qué recibe:** su nivel, un desglose con el porcentaje de cada bloque, la
  lista de competencias que le faltan y cuál es su siguiente paso.
- **Cuánto toma:** unos 5 minutos. Resultado inmediato en pantalla.
- **De dónde salen las preguntas:** del temario real del Máster Internacional
  BIM+IA (12 módulos), no de trivia.
- **Enlace:** https://funnel.dgdesignmodeling.com/test-nivel-bim
- **No es:** una certificación, un diploma, ni un quiz de redes. Es un
  diagnóstico.

## DM 1 — respuesta inmediata al comentario

> ¡Hola! 👋 Aquí está tu acceso al Test de Nivel BIM **GRATIS**
>
> 👉 https://funnel.dgdesignmodeling.com/test-nivel-bim
>
> Regístrate (20 segundos) y lo haces de inmediato desde el celular: 20
> preguntas, 5 minutos, y al terminar sabes en cuál de los 4 niveles estás y
> qué competencias concretas te faltan para el siguiente.
>
> Antes de que lo hagas, cuéntame ¿en qué nivel crees que vas a salir? 🙂
> 1️⃣ Modelador BIM
> 2️⃣ Coordinador BIM
> 3️⃣ BIM Manager 4D-5D
> 4️⃣ Especialista BIM+IA

**Por qué esta pregunta y no "¿a qué te dedicas?"** — en la calculadora esa
pregunta funciona porque no sabemos el perfil. En el test **ya lo sabemos**: el
formulario lo pide antes de entrar, así que volver a preguntarlo se siente a
interrogatorio.

Pedirle que **prediga su nivel antes de hacerlo** hace dos cosas: lo
compromete (y por eso lo hace), y deja servida la conversación de venta. La
distancia entre lo que creía y lo que le salió **es** el argumento.

## DM 2 — a las 24 h, aprovechando la predicción

Si respondió con un número, personalizar. Si no, la versión genérica.

> **Si dijo 3 o 4 y le salió 1 o 2:**
> {{contact.first_name}}, me dijiste que creías salir en {{nivel_predicho}} 👀
> ¿Qué te salió al final? Te lo pregunto porque cuando la diferencia es de dos
> niveles casi siempre es por lo mismo, y es más corto de cerrar de lo que
> parece.

> **Si acertó o no respondió:**
> {{contact.first_name}}, ¿alcanzaste a hacer el test? Cuéntame qué nivel te
> salió — sobre todo si fue más bajo de lo que esperabas, porque ahí es donde
> está lo interesante: ya sabes exactamente por dónde empezar.

**Etiquetar la predicción** (`predijo-nivel-1` … `predijo-nivel-4`): cruzada
contra el nivel real, es el mejor dato de calificación que vamos a tener. Quien
se sobreestima por dos niveles es el perfil que más necesita el Máster.

## Respuestas a lo que suelen preguntar

| Preguntan | El bot responde |
|---|---|
| "¿es gratis?" | Sí, totalmente gratis y sin límite de intentos. |
| "¿me dan certificado?" | No, no es una certificación — es un diagnóstico para saber en qué nivel estás y qué te falta. El certificado va por otro lado, si decides formarte. |
| "¿me llega por correo?" | No hace falta esperar nada: el resultado te sale en pantalla apenas terminas. |
| "¿cuánto dura?" | Unos 5 minutos. |
| "me salió nivel 1, ¿está mal?" | Para nada. La mayoría sale 1 o 2, y eso es normal: el test mide lo que sabes **hacer** en un proyecto, no lo que has estudiado. Lo valioso es que ya sabes cuál es tu siguiente paso. |
| "¿qué hago ahora?" | Depende de tu nivel — cuéntame cuál te salió y te digo qué conviene cerrar primero. *(→ pasar a humano)* |
| precio / quiero inscribirme | *(→ pasar a humano, no dar cifras)* |

**Etiquetas:** `lead-test-nivel` + `origen-bot-nivel`

---

# 2 · CALCULADORA DE ZAPATAS — palabra clave `ZAPATA`

## Qué es (para que el bot lo entienda)

Herramienta gratuita en el navegador que predimensiona **zapatas aisladas**:
se ingresan las cargas y los datos del suelo, y devuelve las dimensiones y las
verificaciones.

- **Qué calcula:** dimensiones de la zapata, presión sobre el terreno y las
  verificaciones que hay que revisar antes de dar por buena una cimentación.
- **Para quién:** ingenieros civiles y estructurales, y estudiantes que están
  aprendiendo a dimensionar.
- **Cuánto toma:** el resultado es inmediato, se actualiza mientras escribes.
- **Enlace:** https://funnel.dgdesignmodeling.com/calculadora-zapatas
- **Muy importante — el descargo:** es una herramienta de **apoyo y
  predimensionamiento**. No sustituye el criterio ni la responsabilidad del
  profesional que firma. Todo resultado debe verificarse con la norma que
  aplique en cada país y proyecto.
- **No es:** un software de diseño estructural certificado, ni un reemplazo de
  memoria de cálculo.

## DM 1 — el que ya está en producción

Este es el texto vivo, tal como lo tiene Dayana en el bot. Es el patrón que
siguen los demás: saludo → enlace → qué obtiene → **pregunta con opciones
numeradas**, que es lo que hace que respondan (contestar "2" no cuesta nada, y
esa respuesta abre la ventana de 24 h y segmenta al contacto).

> Hola! 👋 Aquí está tu acceso a la Calculadora de Zapatas GRATIS
>
> 👉 https://funnel.dgdesignmodeling.com/calculadora-zapatas
>
> Regístrate (20 segundos) y la usas de inmediato desde el celular:
> dimensiones, verificaciones y acero de tu zapata en 2 minutos.
>
> Mientras la pruebas, cuéntame ¿a qué te dedicas? 🙂
> 1️⃣ Estudiante de ingeniería/arquitectura
> 2️⃣ Ingeniero(a) o arquitecto(a) independiente
> 3️⃣ Trabajo en constructora/consultora
> 4️⃣ Docente

## DM 2 — a las 24 h, calificación

> {{contact.first_name}}, ¿pudiste probar la calculadora? 🙂
>
> Me da curiosidad en qué la estás usando — ¿es para un proyecto en obra, para
> la u, o para revisar algo que ya tenías hecho?

## Respuestas a lo que suelen preguntar

| Preguntan | El bot responde |
|---|---|
| "¿es gratis?" | Sí, gratis y sin instalar nada. Funciona en el navegador, también en el celular. |
| "¿sirve para zapatas combinadas / corridas / losas?" | Por ahora es para zapatas aisladas. Si necesitas otro tipo, dime cuál y lo tomo en cuenta para la próxima versión. |
| "¿con qué norma trabaja?" | Es un predimensionamiento general — la verificación contra la norma de tu país la tienes que hacer tú. Por eso siempre decimos que es una herramienta de apoyo. |
| "¿puedo usarla en un proyecto real?" | Para predimensionar, sí, y ahorra bastante tiempo. Pero la memoria de cálculo y la firma son tuyas: el resultado hay que verificarlo. |
| "¿me la puedo descargar?" | No hace falta descargarla, funciona desde el enlace. Guárdalo en favoritos y la tienes siempre a mano. |
| precio / quiero inscribirme | *(→ pasar a humano, no dar cifras)* |

**Etiquetas:** `lead-calculadora-zapatas` + `origen-bot-zapata`

---

## Nota de mantenimiento

Cuando exista el hub (`/recursos`, ver `recursos/PLAN-HUB.md`), los DM 1 de los
dos bots pasan a enlazar **al hub** en vez de a la herramienta suelta — así
quien pide una descubre la otra. Ese es el cambio principal que trae el hub y
hay que acordarse de hacerlo.
