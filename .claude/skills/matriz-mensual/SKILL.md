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
7. **No repetir pieza** que ya se usó otro mes: comparar contra los calendarios
   anteriores.

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
