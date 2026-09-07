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
| Para qué sirve | Captar el dato | Que el asesor entre a la llamada sabiendo con quién habla |

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

GHL → **Settings → Custom Fields → Add Field**. Seis campos, todos sobre el
objeto **Contact**:

| Nombre del campo | Clave (tiene que ser exacta) | Tipo |
|---|---|---|
| Nivel BIM | `nivel_bim` | Texto de una línea |
| Perfil técnico | `perfil_tecnico` | Texto de una línea |
| Módulo recomendado | `modulo_recomendado` | Texto de una línea |
| Código de diagnóstico | `codigo_diagnostico` | Texto de una línea |
| Detalle del diagnóstico | `detalle_diagnostico` | **Texto largo** |
| Puntajes por bloque | `puntajes_bloques` | Texto de una línea |

La clave es lo que importa, no el nombre visible. Si GHL genera una clave
distinta al guardar (a veces le pone un prefijo), **hay que copiar la que
quedó** y pegarla en `app.html`, en el bloque `CFG.CAMPOS`.

## PASO 2 — Crear el formulario que recibe el resultado

GHL → **Sites → Forms → New Form**. Nómbralo `Diagnóstico BIM Máster`.

Añade los seis campos personalizados del paso 1. **Todos ocultos** (hidden):
el alumno ya vio su resultado en el test, este formulario solo transporta el
dato al CRM.

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

## PASO 3 — Cómo manda el link el closer

El link tiene que llevar identificado al contacto, o el resultado no se puede
pegar a nadie. En la plantilla de WhatsApp de GHL:

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

## PASO 4 — Dónde lo lee el asesor

En la ficha del contacto en GHL, en los campos personalizados. El que se lee
de un vistazo es **`detalle_diagnostico`**, que termina con una línea así:

```
PARA EL ASESOR: Domina hasta Coordinador, viene de cálculo estructural.
Entrar por BIM Management · GESTIONA.
```

Esa frase es el resumen operativo: nivel, de dónde viene y por dónde entrar.
Todo lo demás es el respaldo por si la conversación lo pide.

**Recomendado:** añadir esos campos a la vista de la oportunidad en el pipeline
de High Tickets, para que se vean sin abrir el contacto.

---

## Comprobar antes de darlo por hecho

No basta con que el test cargue. Hay que verificar que **el dato llega**:

1. Abre el link **con un `cid` real** de un contacto de prueba tuyo.
2. Responde las 20 preguntas de cualquier forma.
3. Al terminar debe decir «Listo. Tu asesor ya lo tiene.»
4. **Abre ese contacto en el CRM** y comprueba que los seis campos se llenaron.

El paso 4 es el que de verdad importa. Los pasos 1 a 3 pueden salir bien y el
dato no haber llegado.

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

## Lo que hay que saber cuando pregunten

**No sustituye a la llamada, la prepara.** El test le dice al alumno su nivel y
su perfil; la ruta, los módulos y el precio son de la conversación con el
asesor. Está escrito así a propósito.

**El alumno ve su nivel al terminar.** No se le oculta: ver «eres Coordinador
BIM» es lo que hace que llegue a la cita con ganas. Lo que no ve es la ruta
completa ni qué módulo comprar.

**Nunca dice precios.** Ni del Máster, ni de los módulos, ni de la ruta.

**Funciona sin el `cid`.** Si alguien abre el link suelto, el test corre
igual y muestra el código; simplemente el resultado no se pega a ningún
contacto.
