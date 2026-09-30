---
name: matriz-mensual
description: |
  Genera la matriz de contenido de un mes completo: el calendario día por día y red por red, el análisis de contenido y el de pauta con datos reales, y el documento de Word listo para el equipo. Lo publica para Patricio y lo deja versionado.

  Usa este skill cuando Dayana diga: "matriz-mensual", "vamos a generar la matriz", "arma la matriz de septiembre", "la matriz del mes", "necesito el calendario del mes", "pásame el Word de la matriz", "qué publico este mes", o cuando pida el documento de contenido de un mes concreto.

  Se corre **una vez al mes**, en la última semana del mes anterior.
---

# Skill: matriz-mensual

Convierte los datos de la cuenta en **un plan de publicación del mes y un Word
que el equipo puede ejecutar sin preguntar nada**.

No inventa contenido nuevo: ordena el que ya está guionado, lo cruza con lo que
de verdad funcionó y lo reparte por día y por red.

---

## 0. Cómo funciona el sistema completo

Cinco piezas encadenadas. Entender esto es entender la matriz entera:

```
  matriz.json              151 piezas con métricas REALES de Meta
       ↓                   (lo que pasó)
  patrones-de-viralidad    qué formato y qué eje funcionan
       ↓                   (por qué pasó)
  guiones-completos.json   44 piezas escritas palabra por palabra
       ↓                   (qué vamos a publicar)
  calendario-<mes>.json    qué pieza, qué día, en qué red
       ↓                   (cuándo)
  build_matriz_docx.js     → el Word del mes
```

**Nada se escribe a mano en el Word.** Si un dato está mal, se corrige en su
archivo y se regenera. Editar el Word directamente se pierde en la siguiente
corrida.

### Quién refresca cada cosa

| Archivo | Quién lo actualiza | Cada cuánto |
|---|---|---|
| `matriz.json` | Action `metricas-semanales` (Graph API) | lunes y viernes |
| `fuentes/ads-insights/` | la misma Action | lunes y viernes |
| `fuentes/ingresos/` | la misma Action (Stripe + PayPal) | lunes y viernes |
| `guiones-completos.json` | a mano, cuando se escribe contenido nuevo | según haga falta |
| `calendario-<mes>.json` | **este skill** | una vez al mes |

---

## 0b. El método del mes (desde octubre de 2026) — leer SIEMPRE antes de empezar

Octubre fue el primer mes armado con este método, y es el que se repite. Los
meses anteriores (julio, agosto y septiembre) están cruzados con su resultado
real en `historico-2026.json`.

### De dónde sale cada dato (nunca de memoria)

| Qué | De dónde | Quién lo trae |
|---|---|---|
| Lo que funcionó en la cuenta propia | `matriz.json` (vistas, comentarios, guardados y seguidores por pieza) | **Meta Graph API**, Action «Métricas semanales» (lunes y viernes) |
| Referentes y competencia | `fuentes/` y `competencia.json` | **Apify** (con topes de costo, ver `matriz-viral/CLAUDE.md`) |
| Qué ya se publicó o planificó (jul–sep) | `historico-2026.json` + `HISTORICO-JUL-SEP.md` | `python3 scripts/historico_matriz.py` |
| Quién compra y quién no | `COMPRADORES-VS-NO.md` (GHL, Fathom, formulario de Acero, diagnóstico de pauta) | análisis sin datos personales |
| Si una palabra clave responde | `fuentes/openreply/campanas.json` | `scripts/openreply.py` |
| Pauta | `fuentes/ads-insights/` + el diagnóstico de Dayana del mes | Action + Dayana |

### Las reglas de contenido

- **Feed de ~18 piezas: 40/40/20 de formato** (reels / carruseles / posts) y
  **50/20/30 de intención** (problema / solución / objeciones y testimonios).
- **Cada pieza le habla a un perfil comprador** de `COMPRADORES-VS-NO.md`. Si no
  le habla a ninguno, no entra.
- **El patrón que funciona:** acusar un hábito concreto (8,61 comentarios por
  1.000 vistas contra 0,54) o dar un dato de cálculo verificable (DM168: 130
  comentarios y 611 guardados). No hacer «la IA te va a reemplazar» (0
  comentarios en julio).
- **Palabras vivas:** NIVEL (Máster), ACERO, ZAPATA, MEMORIA, COTIZA y, en los
  lanzamientos, DIPLOMADO. CHATGPT está retirada. Antes de usar una palabra, se
  mira `campanas.json`.
- **Lead magnets:** como máximo uno nuevo al mes. Los demás son de respaldo y
  ya existen. Si uno no genera DM en la semana 2, se cambia por otro de
  respaldo, no por uno nuevo.
- **Pauta:** primero se corrige lo que el diagnóstico del mes dice que hace
  perder leads, y después los anuncios nuevos entran **como reemplazo** de los
  cansados. Va un texto por ángulo y en una sola campaña. El Máster no lleva
  precio. ACERO lleva $225 solo en pauta y en correo a la lista propia.

### Los cinco grupos (calendario en modo `grupos`)

G1 Feed · G2 Comunidades · G3 Blog (sábados) · G4 LinkedIn (3 cuentas, sin
palabra clave) · G5 Historias (lunes a viernes, venta solo el jueves). Los
correos semanales van en `correos` y la pauta en `publicidad`.

**Destacadas:** el calendario lleva un bloque `destacadas` (responsable:
Daniela). Tiene las cinco destacadas, qué historias del mes se agregan a cada
una y qué se quita. Se quita lo que pide palabras muertas y lo que tiene
fechas, cupos o precios vencidos. Cada historia del G5 lleva su campo
`destacada`. En el checklist van dos tareas: limpiar antes del primer lunes y
guardar cada viernes.

### El flujo, con comandos

```bash
# 1. histórico al día (qué ya se usó y qué funcionó)
python3 scripts/historico_matriz.py
# 2. piezas nuevas escritas en JSON {"piezas":[...]} → a guiones-completos.json
python3 scripts/sumar_piezas.py archivo1.json archivo2.json --nota "qué se sumó"
# 3. el calendario del mes (ordena ids; el contenido vive en guiones-completos)
python3 matriz-viral/matriz/calendario-<mes>.py
# 4. las reglas: ids, listas, 40/40/20, 50/20/30, venta semanal, nada repetido,
#    palabras vivas, anuncios ≤125 caracteres en la primera línea, precios
python3 scripts/verificar_matriz_mes.py --mes AAAA-MM      # tiene que dar 0 fallas
# 5. entregables: artefacto por pestañas + JSON completo para la app + Word
python3 scripts/build_matriz_mes.py --mes AAAA-MM
node scripts/build_matriz_docx.js --mes AAAA-MM            # necesita `npm i docx`
# 6. creativos estáticos de pauta dibujados por código (copiar el de octubre)
node scripts/creativos_<mes>.mjs
```

Con eso salen `entregables/matriz-<mes>-artefacto.html` (se publica como
artefacto), `entregables/matriz-<mes>-AAAA-COMPLETA.json`, que es **el archivo
único que se sube a la app**, y el Word. `publish-matriz.yml` los publica en
GitHub Pages, y `calendario-actual.json` pasa solo al mes más reciente.

**La app de Daniela exige** que `slides`, `historias` y `guion_reel` sean
listas; `sumar_piezas.py` y `verificar_matriz_mes.py` lo comprueban.

---

## 1. Antes de generar: comprobar que el dato está fresco

```bash
python3 - <<'PY'
import json
m=json.load(open('matriz-viral/matriz/matriz.json'))
print('matriz actualizada:', m.get('actualizado'), '·', m['total_reels'], 'piezas')
print('sin eje:', sum(1 for r in m['reels'] if not r.get('eje')))
PY
```

- Si `actualizado` tiene más de una semana → correr la Action
  **Actions → Métricas semanales → Run workflow** y esperar.
- Si hay piezas **sin eje**, clasificarlas antes: una pieza sin eje no entra en
  el diagnóstico, y el porcentaje de núcleo saldría equivocado.

---

## 2. Armar el calendario del mes

Se crea `matriz-viral/matriz/calendario-<mes>.json`. Estructura:

| Campo | Qué lleva |
|---|---|
| `mes` | `"2026-09"` — es lo que resuelve el nombre y el título |
| `subtitulo` | una línea bajo el título del Word |
| `reglas_del_mes` | las reglas que van en la sección 1 |
| `piezas` | fecha · semana · `id` · tipo · formato · redes · nota |
| `pauta` | los `id` de las piezas de anuncio |
| `banco_reserva` | `id` de piezas listas por si se cae alguna |

**Cada `id` tiene que existir en `guiones-completos.json`.** Comprobarlo antes:

```bash
python3 - <<'PY'
import json
cal=json.load(open('matriz-viral/matriz/calendario-septiembre.json'))
ids={p['id'] for p in json.load(open('matriz-viral/matriz/guiones-completos.json'))['piezas']}
faltan=[e['id'] for e in cal['piezas']+[{'id':b} for b in cal['banco_reserva']] if e['id'] not in ids]
print('ids inexistentes:', faltan or 'ninguno')
PY
```

### Cómo se decide qué va cada día

1. **Ritmo:** 3-4 piezas por semana, 18 al mes. Más que eso no se sostiene.
2. **Mínimo 60% núcleo** (BIM · IA · modelado · acero). **Cero obra en el
   calendario:** da alcance, pero trae público que no compra.
3. **Los carruseles abren semana** — es el formato de mejor engagement.
4. **Los reels se agrupan** en dos días de grabación, no repartidos.
5. **Un slot de venta por semana, los jueves, en historias.** Nunca más de uno.
6. **Un blog por semana**, el sábado, anunciado con un post que lleva el enlace.
7. **No repetir pieza** que ya se usó otro mes: `verificar_matriz_mes.py` lo
   compara contra `historico-2026.json` (ids y ganchos casi iguales).

---

## 3. Generar el documento

```bash
npm i docx                                        # solo la primera vez
node scripts/build_matriz_docx.js --mes 2026-09
```

Sin `--mes` coge el calendario más reciente. Sale en
`matriz-viral/entregables/Matriz-Contenido-<Mes>-<Año>-DMA.docx`.

Las diez secciones: reglas · CTA · **pauta real** · **análisis de contenido** ·
calendario · desarrollo pieza por pieza · historias · venta y pauta · banco de
reserva · checklist.

**Las secciones de pauta y contenido salen de los datos, no del texto.** Si
falta una fuente, el documento lo dice en rojo en vez de rellenar el hueco.

---

## 4. Publicar y entregar

```bash
git add matriz-viral/matriz/calendario-*.json matriz-viral/entregables/
git commit -m "Matriz de contenido de <mes>"
git push -u origin <rama>
```

Al mergear, la Action `publish-matriz` deja el calendario y los guiones en la
URL pública, que es la que lee **Patricio** y la que lee el **asistente de
WhatsApp**. No hay que mandarle nada a nadie.

Y se le manda el Word a Dayana con `SendUserFile`.

---

## 5. Lo que se entrega en el chat

- **Una frase**: cuántas piezas, qué reparto por eje, qué cambia respecto al mes
  pasado.
- **El calendario en tabla**, para que lo lea sin abrir el Word.
- **Lo que salió del análisis de pauta**: qué campaña conviene y cuál no.
- **Qué hace falta** para poder ejecutarlo (piezas sin guion, bot sin montar).
- **El Word**, adjunto.

---

## Reglas

- **Nada se escribe a mano en el Word.** Se corrige el origen y se regenera.
- **Una pieza sin `id` en `guiones-completos.json` no entra al calendario.**
  Antes hay que escribirla.
- **El precio del Máster no aparece en ninguna pieza.** El de ACERO sí puede ir
  en correo a lista propia y en DM.
- **El número de cupos se actualiza cada vez.** Nunca se inventa.
- **Si falta un dato, el documento lo dice.** No se rellena de memoria: es como
  se publican cifras equivocadas.
- **Las historias de venta no se publican** hasta que el disparador de DM del
  bot esté montado para su palabra clave.

---

# ANEXO · Catálogo de datos — todo lo que se puede mirar

Esta parte existe para quien recibe el skill y no ha visto el sistema por
dentro. **Todo lo que la cuenta produce está aquí**: qué archivo, qué trae, y
el comando exacto para leerlo.

> **Por qué el catálogo y no los números.** Si aquí estuvieran pegadas las
> cifras de hoy, en dos semanas estarían mal y nadie se daría cuenta — que es
> justo como se publican datos equivocados. El catálogo dice **dónde mirar**,
> y lo que se mira siempre está al día.

Todo lo refresca sola la Action **`metricas-semanales`**, lunes y viernes.
Para forzarla: **Actions → Métricas semanales → Run workflow**.

---

## A · Contenido orgánico — Instagram y Facebook (Graph API)

### `matriz-viral/matriz/matriz.json`

El corazón del sistema: cada publicación con sus métricas reales.

| Campo | Qué es |
|---|---|
| `id` · `shortCode` · `url` | identificadores y enlace al post |
| `fecha` · `tipo` · `duracion_s` | cuándo, qué formato, cuánto dura |
| `eje` | **OBRA · NÚCLEO-BIM · NÚCLEO-IA · PROMO · COMUNIDAD** — se pone a mano |
| `views` · `alcance` | vistas y personas distintas |
| `likes` · `comentarios` · `guardados` · `shares` | interacción |
| `interacciones` · `visitas_perfil` · `nuevos_seguidores` | efecto sobre la cuenta |
| `views_facebook` · `comentarios_facebook` · `likes_facebook` | **el lado de Facebook** |
| `tema` · `hook` · `estructura` · `nota` | la lectura editorial, a mano |
| `generado` · `actualizado` | fecha del barrido / del último refresco |

```bash
python3 - <<'PY'
import json, collections
m = json.load(open('matriz-viral/matriz/matriz.json'))
print('actualizado:', m.get('actualizado'), '·', m['total_reels'], 'piezas')
c = collections.Counter(r.get('eje') or 'sin eje' for r in m['reels'])
print('por eje:', dict(c))
top = sorted([r for r in m['reels'] if r.get('comentarios')],
             key=lambda r: -r['comentarios'])[:5]
for r in top:
    print(f"  {r['comentarios']:>4} coment · {r.get('views',0):>9,} vistas · {r.get('eje')} · {(r.get('tema') or '')[:48]}")
PY
```

> **Facebook importa más de lo que parece.** En julio, más de la mitad del
> alcance real del post ganador vino de Facebook. Mirar solo Instagram da una
> foto a medias.

### `matriz-viral/matriz/competencia.json`

El sector, vía `business_discovery` de Meta: seguidores, caption, likes y
comentarios de cuentas business públicas. **No trae vistas ni alcance de
terceros** — Meta no los entrega. Eso se dice, no se estima.

---

## B · Pauta — Meta Ads

`matriz-viral/fuentes/ads-insights/` · cuatro cortes de la misma ventana:

| Archivo | Corte |
|---|---|
| `por-campana.json` | por campaña |
| `por-adset.json` | por conjunto de anuncios |
| `por-dia.json` | día a día |
| `por-pais.json` | por país |
| `resumen.json` | totales y ventana |

Campos por fila: `campaign_name` · `spend` · `impressions` · `reach` ·
`frequency` · `clicks` · `ctr` · `cpc` · `objective` · `actions` ·
`cost_per_action_type` · `date_start` · `date_stop`.

### Los leads llegan por DOS vías y Meta las cuenta distinto

Esto es lo que más se equivoca, así que va con ejemplo:

| Vía | `action_type` |
|---|---|
| Formulario | `lead` (o `onsite_conversion.lead_grouped`) |
| **WhatsApp** | `onsite_conversion.messaging_conversation_started_7d` |

Una campaña usa una u otra, nunca las dos: se suman sin duplicar. **Mirar solo
`lead` deja fuera las campañas de WhatsApp, que son las de mejor CPL y el
grueso del volumen.**

```bash
python3 - <<'PY'
import json
d = json.load(open('matriz-viral/fuentes/ads-insights/por-campana.json'))
def act(f, t):
    a = next((x for x in (f.get('actions') or []) if x['action_type'] == t), None)
    return float(a['value']) if a else 0.0
print('ventana', d['ventana']['desde'], '→', d['ventana']['hasta'])
for f in sorted(d['filas'], key=lambda x: -float(x.get('spend') or 0)):
    g = float(f.get('spend') or 0)
    if not g: continue
    form = act(f,'lead') or act(f,'onsite_conversion.lead_grouped')
    wsp  = act(f,'onsite_conversion.messaging_conversation_started_7d')
    tot  = form + wsp
    via  = 'WhatsApp' if wsp > tot/2 else ('Formulario' if tot else '—')
    cpl  = f'${g/tot:.2f}' if tot else 'SIN LEADS'
    print(f"  ${g:8.2f}  {int(tot):>5} leads  {via:<11} {cpl:>10}  {f['campaign_name'][:44]}")
PY
```

`matriz-viral/fuentes/ads-creativos/` guarda además **las imágenes de los
anuncios ganadores** con su `manifest.json` (campaña, gasto, leads, CPL, CTR).

---

## C · Dinero de verdad — Stripe y PayPal

`matriz-viral/fuentes/ingresos/` · `stripe.json`, `paypal.json`, `resumen.json`.

Cada cobro: `fecha` · `bruto` · `reembolsado` · `neto` · `moneda` · `correo` ·
`descripcion`. De Stripe solo lo `paid` + `succeeded`, con reembolsos ya
descontados.

**Esta es la única fuente que no opina.** El CRM dice lo que alguien *marcó*
ganado; esto dice lo que *entró*.

```bash
python3 -c "
import json
r=json.load(open('matriz-viral/fuentes/ingresos/resumen.json'))
print('ventana', r['ventana']['desde'],'→',r['ventana']['hasta'])
for k,v in r['fuentes'].items(): print(' ',k,v)
print('total cobrado:', r['total_neto'])"
```

> **Nunca se suma Stripe + PayPal + CRM**: es la misma venta contada dos veces.
> Y **las reservas de ~$100 del Máster no son ventas** — son anticipo, van
> aparte siempre.

---

## D · CRM — GoHighLevel

`matriz-viral/fuentes/ghl/` · lo baja `scripts/ghl_datos.py`:

| Archivo | Qué trae |
|---|---|
| `pipelines.json` | cada pipeline con sus etapas y sus ids |
| `oportunidades.json` | totales por pipeline, etapa, **fuente**, estado y mes |
| `etiquetas.json` | todas las etiquetas de la cuenta |
| `formularios.json` | los formularios y sus ids |
| `pagos.json` | transacciones registradas en GHL |
| `resumen.json` | los totales de cada bloque |

`oportunidades.json` → **`por_fuente`** es el campo que conecta contenido con
negocio: dice de dónde vienen los leads.

```bash
python3 -c "
import json
o=json.load(open('matriz-viral/fuentes/ghl/oportunidades.json'))
print(o['total'],'oportunidades · valor declarado',o.get('valor_declarado'))
print('por estado:', o['por_estado'])
print('por mes:', o['por_mes'])
print('top fuentes:')
for k,v in list(o['por_fuente'].items())[:10]: print('  ',v,'·',k)"
```

**Lo que NO hay, y no es un olvido:**

- **Datos personales.** No se bajan nombres, correos ni teléfonos: para decidir
  contenido hacen falta los agregados, no quién es cada persona.
- **Progreso de los alumnos.** Comprobado contra la documentación oficial de
  HighLevel: **ese endpoint no existe en la API pública.** Es una petición
  abierta de la comunidad. Se saca a mano desde Memberships.

`matriz-viral/fuentes/ghl-sonda.json` guarda qué endpoints abren y cuáles no,
con la traducción de cada código: `404` = la ruta no existe · `401`/`403` = el
token no entra · `422` = existe y entra, faltan parámetros.

> **Cuidado con los 403 de GoHighLevel.** Sin User-Agent de navegador,
> Cloudflare bloquea la IP con un Error 1010 que **parece** falta de permisos.
> El 15-ago los 19 endpoints dieron 403 por eso y se concluyó que el token no
> servía. Sí servía.

---

## E · El contenido escrito

`matriz-viral/matriz/guiones-completos.json` · cada pieza con `id` · `titulo` ·
`formato` · `red_principal` · `eje` · `pilar` · `hook` · `slides` · `caption` ·
`cta_por_red` · `prompt_imagenes` · `historias` · `notas_produccion`.

Las piezas de formato `historia` **no traen `slides` ni `caption`**: su guion
vive entero en `historias`, cuadro a cuadro (`n` · `visual` · `texto` ·
`sticker`).

**`slides`, `historias` y `guion_reel` son SIEMPRE listas.** La app de Daniela
las recorre lámina por lámina. Una nota de producción («los 7 slides del
carrusel rediagramados a PDF») va en `slides_nota` o en `notas_produccion`,
nunca como texto dentro de `slides`.
> *De dónde sale:* en octubre `oct-tutor-dip-li-academy` traía `slides` como
> texto y la app no la pudo mostrar. Patricio lo corrigió a mano en el archivo
> publicado el 28-sep. Antes de publicar, comprobar:
> `python3 -c "import json;g=json.load(open('matriz-viral/matriz/guiones-completos.json'));print([p['id'] for p in g['piezas'] for k in ('slides','historias','guion_reel') if k in p and not isinstance(p[k],list)])"`
> tiene que imprimir `[]`.

```bash
python3 -c "
import json, collections
g=json.load(open('matriz-viral/matriz/guiones-completos.json'))
print(g['total'],'piezas ·',dict(collections.Counter(p['formato'] for p in g['piezas'])))
for p in g['piezas'][:8]: print(f\"  {p['id']:34} {p.get('eje','?'):12} {p['titulo'][:46]}\")"
```

---

## F · Lo que hay que saber para no equivocarse

| Trampa | Qué pasa |
|---|---|
| Mirar solo `lead` en la pauta | se pierden las campañas de WhatsApp, las de mejor CPL |
| Mirar solo Instagram | Facebook aporta más de la mitad del alcance real |
| Leer un 403 de GHL como permisos | suele ser Cloudflare bloqueando la IP |
| Sumar CRM con Stripe | es la misma venta dos veces |
| Contar las reservas de $100 como venta | son anticipo del Máster |
| Fiarse de `generado` en la matriz | la fecha del refresco es `actualizado` |
| Ventana que llega hasta hoy | el día en curso va a medias y acorta las cifras |
| Pedir progreso de alumnos por API | no existe en GHL: se saca a mano |
