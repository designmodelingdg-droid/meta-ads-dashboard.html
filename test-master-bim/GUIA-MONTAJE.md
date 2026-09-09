# Diagnóstico BIM del Máster — montaje

Para **Ester y Aylin**. El test ya está construido y probado; lo que falta es
conectarlo a GoHighLevel para que el resultado llegue al asesor.

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-master-bim/
```

---

## Qué es esto, y en qué se diferencia del test que ya existe

Hay dos tests y **no son el mismo producto**:

| | Test de Nivel BIM (el que ya existe) | Diagnóstico BIM del Máster (este) |
|---|---|---|
| Para quién | Cualquiera, es un recurso gratuito | Solo quien **ya agendó** una cita |
| Cómo llega | Anuncio → landing → formulario | El closer lo manda por WhatsApp tras agendar |
| Qué mide | Nivel BIM | Nivel BIM **+ base técnica** (estructural o arquitectura) |
| A dónde va el resultado | A ninguna parte: se queda en el navegador | **Al CRM, al contacto que hizo el test** |
| Qué ve la persona al terminar | Su nivel y su ruta completa | **Nada de su perfil: se lo da el asesor en la cita** |
| Para qué sirve | Captar el dato | Que el asesor entre a la llamada sabiendo con quién habla |
| Qué enseña el asesor | Nada | Un **panel con las 20 respuestas**, que abre y comparte en la cita |

El test público no manda el resultado a ningún sitio. Ese es el agujero que
este cierra, y es la razón de que exista.

## Las 20 preguntas, en dos ejes

**Eje A · Nivel BIM (14 preguntas).** Cuatro bloques que corresponden a los
cuatro módulos: Modelador (4), Coordinador (4), BIM Manager 4D-5D (3),
Especialista BIM+IA (3). Un bloque se domina con el 70% de su puntaje.

**Eje B · Base técnica (6 preguntas).** Tres de cálculo y diseño estructural,
tres de arquitectura y edificación. Se considera base real con 6 de 9.

Esto último es lo nuevo, y es lo que más cambia la llamada: **al que
predimensiona una zapata no se le vende igual que al que resuelve un programa
arquitectónico**, aunque los dos sean Coordinadores BIM.

### Una regla que conviene entender antes de leer un resultado

El nivel es el **último bloque dominado sin saltos**. Si alguien domina
Modelador y BIM Manager pero no Coordinador, el test dice **Modelador**, no BIM
Manager, y añade que tiene conocimiento disperso por encima de su nivel.

Es a propósito: decirle al asesor que tiene delante a un BIM Manager cuando le
falta la coordinación entera hace que pierda la llamada en los primeros dos
minutos.

---

## PASO 1 — Crear los campos personalizados en el CRM

GHL → **Settings → Custom Fields → Add Field**. Siete campos, todos sobre el
objeto **Contact**:

| Nombre del campo | Clave (tiene que ser exacta) | Tipo |
|---|---|---|
| Nivel BIM | `nivel_bim` | Texto de una línea |
| Perfil técnico | `perfil_tecnico` | Texto de una línea |
| Módulo recomendado | `modulo_recomendado` | Texto de una línea |
| Código de diagnóstico | `codigo_diagnostico` | Texto de una línea |
| Enlace del resultado | `enlace_resultado` | **URL** (o texto de una línea) |
| Detalle del diagnóstico | `detalle_diagnostico` | **Texto largo** |
| Puntajes por bloque | `puntajes_bloques` | Texto de una línea |

La clave es lo que importa, no el nombre visible. Si GHL genera una clave
distinta al guardar (a veces le pone un prefijo), **hay que copiar la que
quedó** y pegarla en `app.html`, en el bloque `CFG.CAMPOS`.

## PASO 2 — Crear el formulario que recibe el resultado

GHL → **Sites → Forms → New Form**. Nómbralo `Diagnóstico BIM Máster`.

Añade los siete campos personalizados del paso 1. **Todos ocultos** (hidden):
la persona no ve nada de esto, el formulario solo transporta el dato al CRM.

> ⚠ **Y ADEMÁS el correo. Esto faltaba en esta guía y costó un montaje.**
> Un formulario de GHL con solo campos personalizados **no se pega a ningún
> contacto**: hace falta al menos **Email** o **Teléfono**, que son los que GHL
> usa para identificar o crear la ficha. Sin eso el diagnóstico no tiene dueño.
>
> Añade dos campos estándar más:
>
> | Campo | Visible | Por qué |
> |---|---|---|
> | **Email** | sí | Es la llave con la que GHL encuentra o crea el contacto |
> | **Nombre** (`Full Name`) | sí | Para que la ficha no quede sin nombre |
>
> Visibles a propósito: llegan prellenados desde el enlace que manda el closer
> y la persona los ve y puede corregirlos. Un correo mal escrito manda el
> diagnóstico a una ficha que no es.
>
> El test ya los envía — usa los nombres estándar de GHL, `email` y
> `full_name`, que son los que su prellenado reconoce. No hay que tocar código.
>
> **Ojo con el «+» también aquí:** GHL lo borra igual en los campos estándar,
> así que un correo con alias tipo `nombre+prueba@gmail.com` llega roto. Para
> probar, usa una dirección distinta de verdad.

Publica el formulario y copia su enlace, que se ve así:

```
https://api.leadconnectorhq.com/widget/form/AbC123XyZ
```

Pégalo en `app.html`, en `CFG.FORM_GHL`, reemplazando `PEGAR_ID_DEL_FORMULARIO`.

> Mientras no se pegue, el test funciona y calcula bien, pero muestra un aviso
> naranja diciendo que falta conectarlo. Es a propósito: es preferible un aviso
> visible a un resultado que se pierde en silencio.

**Por qué formulario nativo y no webhook:** el webhook de GHL es prémium y
cobra por ejecución. El formulario nativo es gratis y el dato entra igual.

### HECHO el 9-sep — y lo que salió al montarlo

Formulario montado: `c9q5RXwZp3kDRuwk1eCz`. Al conectarlo aparecieron tres
cosas que no se ven a simple vista. Quedan aquí porque las tres se repiten en
cualquier formulario de GHL que se monte igual.

**1. Las claves llevan tilde y no son las que uno supone.** GHL genera la clave
de cada campo a partir de su ETIQUETA. «Perfil técnico» produjo
`perfil_técnico`, con tilde; «Puntajes por bloque» produjo `puntajes_por_bloque`
y no `puntajes_bloques`. De las siete que enviaba el test, **solo una
coincidía**: las otras seis habrían llegado vacías sin que nada avisara.

Las claves reales, leídas del formulario publicado:

| Campo | Clave real (`data-q`) |
|---|---|
| Nivel BIM | `nivel_bim` |
| Perfil técnico | `perfil_técnico` |
| Código de diagnóstico | `código_de_diagnóstico` |
| Módulo recomendado | `módulo_recomendado` |
| Enlace del resultado | `enlace_del_resultado` |
| Detalle del diagnóstico | `detalle_del_diagnóstico` |
| Puntajes por bloque | `puntajes_por_bloque` |

**Cómo comprobarlas sin adivinar:** abre el enlace del formulario, mira el
código fuente de la página y busca `data-q=`. Eso es exactamente lo que GHL
cruza contra el querystring. Si alguien renombra una etiqueta, la clave cambia
y ese campo deja de llegar — por eso la prueba automática las compara.

**2. GHL borra el signo «+».** Su propio código hace `.replace(/\+/g,' ')` sobre
el valor, porque asume que un «+» es un espacio codificado. No hay forma de
colarle un «+» literal, ni escapándolo. Como el nivel más alto se llama
«Especialista BIM + IA», habría llegado al CRM como «Especialista BIM   IA».
El test ahora lo cambia por « y »: «Especialista BIM y IA».

**3. El formulario tiene que VERSE.** Iba en un iframe de altura 0 y, al
terminar de cargar, la pantalla decía «Listo. Tu asesor ya lo tiene». Era
falso: prellenar un formulario no lo envía. Nadie pulsaba «Continuar», así que
no se creaba el contacto y el diagnóstico no llegaba a ninguna parte — con la
pantalla diciendo que sí. Es el mismo patrón del incidente de julio.

Ahora el formulario se muestra y la pantalla pide el paso que falta: revisar
los datos, marcar la casilla de consentimiento y pulsar **Continuar**. La
casilla la marca la persona, no nosotros.

## PASO 3 — Cómo manda el link el closer (y cómo NO se duplica el contacto)

Casi todo el que recibe este enlace **ya tiene ficha en GHL**: viene de pauta y
está en «lead calificado» del pipeline de High Ticket. La pregunta que importa
es qué pasa cuando esa persona vuelve a dejar sus datos.

**Lo cruza el CORREO, no el `cid`.** Conviene decirlo claro porque el enlace
lleva las dos cosas y parece que manda el id:

| Parámetro | Qué hace de verdad |
|---|---|
| `email` | **Es la llave.** GHL busca ese correo; si ya existe, ACTUALIZA esa ficha |
| `nombre` | Rellena el nombre. No identifica a nadie |
| `cid` | **No hace nada en el formulario.** Se envía como `contact_id` y GHL lo ignora: no está en su lista de campos que prellena. Viaja en el payload y ya |

Así que la pieza que evita el duplicado es `{{contact.email}}` en la plantilla.
Si vuelve el mismo correo que ya está en la ficha, **no se crea un contacto
nuevo: se actualiza el que existe**, con sus etapas de pipeline, sus etiquetas
y su historial intactos.

### Las tres formas en que SÍ se duplicaría

1. **La persona escribe otro correo.** El de la pauta era el del trabajo y pone
   el personal. Por eso el correo va PRELLENADO y el test avisa en pantalla:
   «Tu correo ya viene puesto. Déjalo tal cual: es lo que hace que este
   diagnóstico se sume a tu ficha».
2. **El enlace llega sin `email`.** Si el closer lo copia a mano en vez de usar
   la plantilla con `{{contact.email}}`, o alguien lo reenvía a un amigo. En ese
   caso el test enseña el otro aviso: «Escribe el mismo correo con el que te
   registraste». Un enlace reenviado crea un contacto nuevo — y está bien, es
   una persona nueva de verdad.
3. **GHL tiene los duplicados permitidos.** Es un ajuste de la cuenta, no del
   formulario: `Settings → Business Profile → Allow Duplicate Contact`. Si está
   activado, GHL crea ficha nueva aunque el correo coincida. **Hay que
   comprobarlo antes de mandar el primer enlace** — es la única de las tres que
   no se ve venir.

### Y el «+» otra vez

GHL borra el signo «+» también en el correo. Un contacto cuyo correo sea
`nombre+algo@dominio.com` llegaría como `nombre algo@dominio.com`, no cruzaría
con nada y **crearía un duplicado**. Son pocos, pero si aparece un contacto
partido en dos, mira eso primero.

En la plantilla de WhatsApp de GHL:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-master-bim/?cid={{contact.id}}&nombre={{contact.first_name}}&email={{contact.email}}
```

Mensaje sugerido, después de agendar:

> Listo [nombre], ya quedó tu cita para el [día] a las [hora].
>
> Antes de la llamada, te paso un diagnóstico de 5 minutos: 20 preguntas sobre
> lo que sabes hacer en un proyecto. Lo reviso antes de hablar contigo, así no
> gastamos la cita en que me expliques desde cero por dónde vas.
>
> [link]

## PASO 4 — Lo que el asesor lee antes de llamar

En la ficha del contacto en GHL, en los campos personalizados. El que se lee
de un vistazo es **`detalle_diagnostico`**, que termina con una línea así:

```
PARA EL ASESOR: Domina hasta Coordinador, viene de cálculo estructural.
Entrar por BIM Management · GESTIONA.
```

Esa frase es el resumen operativo: nivel, de dónde viene y por dónde entrar.
Se lee en diez segundos, antes de marcar.

**Recomendado:** añadir esos campos a la vista de la oportunidad en el pipeline
de High Tickets, para que se vean sin abrir el contacto.

## PASO 5 — El panel que el asesor ENSEÑA en la llamada

Decir «eres Coordinador BIM» y **enseñarlo** no pesan lo mismo. Por eso, además
de los campos de texto, el contacto guarda un campo `enlace_resultado` con una
dirección como esta:

```
…/test-master-bim/resultado.html?r=33333322110000332110&n=Andrea
```

El asesor le da clic **durante la llamada** y comparte pantalla. El panel abre
con el nombre de la persona y muestra, en este orden:

1. **Su nivel**, con el perfil técnico y el código de diagnóstico.
2. **La escalera de los cuatro niveles**, con el porcentaje de cada uno y cuál
   es el siguiente escalón, marcado como «tu siguiente paso».
3. **Los dos ejes técnicos** —estructural y arquitectura— con su barra.
4. **El módulo por el que debería entrar**, con la microcredencial que da.
5. **Las 20 respuestas, una por una**, con lo que contestó en cada competencia.

Ese último bloque es el que sostiene la conversación. Cuando alguien dice «yo ya
sé coordinar», el asesor no discute: baja a la pregunta, le enseña que en «llevo
el flujo de información del proyecto» contestó *lo hago con ayuda*, y la
objeción se cae sola. Es la propia respuesta de la persona, no una opinión del
vendedor.

**Cómo funciona el enlace.** Las 20 respuestas van dentro de la dirección, en
esos 20 dígitos del `?r=`. No hay base de datos detrás: el enlace no caduca, no
se puede quedar huérfano, y si mañana cambiamos de CRM sigue abriendo igual.
Cada dígito es una pregunta y vale de 0 a 3.

**En el panel no hay nada interno.** Ni precios, ni notas del vendedor, ni
puntajes crudos. Está pensado para verlo con el cliente delante, así que el
asesor puede compartir pantalla sin revisar antes qué sale.

**Cuándo NO se manda.** El enlace no se envía por WhatsApp antes de la cita.
Es lo que se recoge *en* la llamada; mandarlo antes deshace la razón de haberlo
guardado (ver la última sección).

---

## Comprobar antes de darlo por hecho

No basta con que el test cargue. Hay que verificar que **el dato llega**:

1. Abre el link **con un `cid` real** de un contacto de prueba tuyo.
2. Responde las 20 preguntas de cualquier forma.
3. Al terminar debe decir «Listo. Tu asesor ya lo tiene.»
4. **Abre ese contacto en el CRM** y comprueba que los siete campos se llenaron.
5. **Haz clic en `enlace_resultado`.** Tiene que abrir el panel con el nombre de
   la persona y las 20 respuestas que acabas de dar.

Los pasos 4 y 5 son los que de verdad importan. Los pasos 1 a 3 pueden salir
bien y el dato no haber llegado a ninguna parte.

### Si los campos llegan vacíos

Quiere decir que el formulario de GHL no está tomando los valores de la
dirección. Dos cosas que revisar, en este orden:

1. **Que las claves coincidan** exactamente entre `CFG.CAMPOS` y las claves
   reales de los campos en el CRM. Es la causa más frecuente.
2. **Que el formulario acepte prellenado por URL.** Si tu versión de GHL no lo
   hace, la alternativa es el webhook prémium: se activa en el formulario y se
   pega su URL en `CFG.FORM_GHL`. Cuesta por ejecución, pero funciona igual.

Mientras tanto, el test siempre muestra al alumno un **código de diagnóstico**
—por ejemplo `B2-EST-57`— que el asesor puede pedirle y apuntar a mano. Se lee:
bloque dominado, base técnica, porcentaje global. No es la solución, es el
paracaídas.

---

## El resultado se entrega EN LA LLAMADA, no en la pantalla

Esta es la decisión que más define el test, y conviene que todo el equipo la
diga igual.

Al terminar, la persona **no ve su nivel ni su perfil**. Ve que el diagnóstico
está completo, que ya tenemos su perfil, y que su asesor se lo entrega en la
cita. El panel del paso 5 existe, está listo y es suyo —pero se abre en la
llamada.

**Por qué.** Si al terminar le decimos «eres Coordinador BIM», la cita pasa a
ser opcional: ya tiene lo que vino a buscar. Guardando el resultado, la llamada
deja de ser una presentación de ventas y pasa a ser el sitio donde recoge algo
que ya es suyo y todavía no ha visto. Sube la asistencia, que en agosto fue del
46,3% contra un objetivo del 80%.

**Cómo decirlo si preguntan por WhatsApp antes de la cita.** No se manda el
resultado por escrito, y no porque sea un secreto:

> Ya tengo tu perfil aquí delante. Te lo explico en la llamada porque tiene
> matices —hay cosas que dominas por encima de tu nivel y huecos que se cierran
> más rápido de lo que parece— y por escrito se malinterpreta. En cinco minutos
> de llamada lo tienes claro.

**Lo que sí es suyo desde el primer momento:** el código de diagnóstico que ve
en pantalla. No dice nada por sí solo, pero le demuestra que hay un resultado
real esperándolo, y que no es un texto genérico: es un código que sale de sus
respuestas.

## Lo que hay que saber cuando pregunten

**No sustituye a la llamada, la prepara.** El test calcula el nivel, el perfil
técnico y el módulo por el que debería entrar. Todo eso lo entrega el asesor,
enseñando el panel.

**Nunca dice precios.** Ni del Máster, ni de los módulos, ni de la ruta.

**Funciona sin el `cid`.** Si alguien abre el link suelto, el test corre
igual y muestra el código; simplemente el resultado no se pega a ningún
contacto.
