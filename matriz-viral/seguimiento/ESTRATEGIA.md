# Estrategia de seguimiento de leads — Design Modeling Academy

**Escrita el 10-ago-2026.** Es el documento madre: las tres secuencias viven en
archivos aparte, el montaje también. Aquí está el porqué y las reglas.

---

## 1. El problema que resuelve

Tenemos ~2.300 contactos que llegaron por recursos gratuitos y **nadie les está
haciendo nada**. El flujo termina cuando la persona descarga: no hay correo de
bienvenida, no hay nutrición, y la oportunidad se queda parada en una etapa del
pipeline sin siguiente paso.

No es una impresión: `BRIEF-CALCULADORA-ZAPATAS.md` y el montaje del bot
mencionan una *"secuencia de nutrición normal"* que **nunca se escribió**. Lo
único que existía era la secuencia de 3 DMs del bot
(`guiones/2026-07-20_leadmagnet-calculadora-zapatas/campana-ghl.md`), que se
muere a las 24 horas por la ventana de mensajería de Meta.

WhatsApp masivo está descartado — bloquea la línea. **El correo es el puente.**

### Los números de partida (GHL vía Windsor, últimos 60 días)

| Segmento | Contactos | Con correo | Secuencia |
|---|---|---|---|
| Calculadora de Zapatas | 297 | **199** | A |
| Test de Nivel BIM | 31 | **26** | B |
| Lista dormida (ebook, guía, AI PRO, cursos) | 1.999 | **1.999** | C |

Estos números son del 10-ago-2026 y crecen solos. Las secuencias son por
disparador (entra al pipeline → arranca), así que no hay que volver a contarlos.

---

## 2. Las tres secuencias

| | Para quién | Hacia dónde | Duración |
|---|---|---|---|
| **A** | Calculadora de Zapatas | **Especialización en ACERO** | 14 días · 7 correos |
| **B** | Test de Nivel BIM | Máster (vía llamada) | 12 días · 5 correos |
| **C** | Lista dormida | Hub `/recursos` → re-segmentar | 8 días · 3 correos |

### Por qué Zapatas va a ACERO y no al Máster

Quien predimensiona una zapata es público **estructural**, no público de
gestión BIM. Y ACERO es el producto que más convierte de toda la cuenta:
**1.086 leads con CPL $0,45–$0,61** (ver `matriz/analisis-campanas.md`). Cierra
más rápido y más barato que el Máster. Mandarlos al Máster sería pedirles un
salto de tema *y* de precio al mismo tiempo.

### Por qué el test va al Máster

El test mide los 4 niveles de la ruta del Máster. La persona que lo hace ya
aceptó que hay una escalera y quiere saber en qué peldaño está. Ahí el Máster
es la respuesta natural — pero **por llamada, nunca cotizado en el correo**
(ver §5).

### Por qué la lista dormida va primero al hub y no a una oferta

Son ~2.000 personas que no saben de nosotros hace meses. Pedirles una compra
de entrada es la forma más rápida de ganarse un botón de spam. El hub
`/recursos` da valor sin pedir nada y **ya demostró que funciona**: un contacto
se llevó 5 recursos en 9 minutos el día del lanzamiento. El correo 2 usa el
test como segmentador — quien lo hace pasa a la secuencia B y deja de ser
"lista dormida".

---

## 3. Qué pasa con la oportunidad del pipeline

Esto contesta la pregunta directa: *"¿qué hago con estos clientes?"*.
**Nada a mano.** El workflow mueve la etapa solo:

```
Nuevo lead ──► En nutrición ──► Interesado ──────► Llamada agendada
 (entra)        (correo 0)      (clic en la        (reservó hora)
                                 oferta)                  │
                                                          ▼
                                                  aquí entra un humano
```

Tú solo miras la columna **"Llamada agendada"**. Todo lo anterior corre solo.

---

## 4. Salidas y etiquetas

**Sale de la secuencia** (deja de recibir correos automáticos) quien:

- **responde un correo** ← esto es lo que queremos, ahí entra un humano
- **agenda una llamada**
- **compra**
- **pide la baja**

**Etiquetas** (respetan la taxonomía que ya existe: `lead-<tema>`, `origen-bot-<palabra>`):

| Tag | Cuándo se pone |
|---|---|
| `seq-zapatas-acero` | entra a la secuencia A |
| `seq-test-master` | entra a la B |
| `seq-reactivacion` | entra a la C |
| `seq-completada` | terminó los correos sin convertir |
| `lead-caliente` | abrió y clicó 2 veces o más |
| `email-frio` | no abrió **ninguno** de los correos de la C |
| `respondio-correo` | contestó — sale de todo, lo atiende una persona |

`email-frio` es el freno de mano: esa gente deja de recibir envíos hasta nuevo
aviso. Seguir mandándole correo a quien nunca abre es lo que arruina la
reputación del dominio para todos los demás.

---

## 5. Reglas de contenido (no negociables)

1. **El Máster no se cotiza en correo.** Es regla permanente del proyecto
   (`matriz-viral/CLAUDE.md`). El precio de la **Especialización en ACERO** sí
   va, porque es lista propia con consentimiento y es un producto de decisión
   rápida. El Máster cierra siempre con **llamada**.
2. **Nunca prometer entrega por WhatsApp.** No existe ese workflow. Todo lo que
   se promete se entrega por enlace, en el mismo correo.
3. **Disclaimer educativo** donde toque: la calculadora es una herramienta de
   **predimensionamiento**; el diseño definitivo lo firma un ingeniero
   responsable. El test **no es una certificación ni un diploma**.
4. **Ningún correo sin `{{unsubscribe_url}}`.**
5. **Nada de cifras inventadas.** Si un dato no lo tenemos (precio, fecha de
   cohorte), va como marcador `[ASÍ]` y lo llena Dayana. Ver §8.

---

## 6. Entregabilidad — la única corrección al "todos a la vez"

Tú decides que la lista dormida entre completa, y así queda. Pero **GHL los
manda en lotes de 400 por día durante 5 días**, no los 2.000 de golpe.

El motivo es concreto: 2.000 correos de una sentada a una lista que no recibe
nada hace meses genera un pico de rebotes y de "marcar como spam" que los
filtros leen como envío masivo comprado. El dominio ya está calentado y
funcionando — eso es un activo que cuesta meses reconstruir.

Para ti no cambia nada: una sola acción, entran todos. Solo el envío se
reparte.

**Umbrales de salud.** Si se cruza cualquiera de estos, se pausa y se revisa
antes de seguir:

| Métrica | Mínimo/máximo | Qué significa si falla |
|---|---|---|
| Apertura | ≥ 25 % | el asunto no conecta, o estamos cayendo en promociones |
| Clics | ≥ 3 % | el correo se lee pero no convence |
| **Rebotes** | **< 2 %** | lista sucia — hay que limpiar antes de seguir |
| **Spam** | **< 0,1 %** | 🚨 parar todo. A 0,3 % Gmail empieza a filtrar el dominio |

**Orden de encendido:** primero A (199 contactos, riesgo bajo) → a las 48 h se
miran rebotes y spam → solo si están dentro de umbral se enciende C.

---

## 7. Qué se revisa y cuándo

Con el skill `seguimiento-leads`, una vez al mes:

- Cuántos entraron a cada secuencia y cuántos la terminaron
- Apertura y clic **por correo** — el correo que se cae señala dónde se pierde
- Cuántos respondieron (es la métrica que más importa)
- Cuántas oportunidades cambiaron de etapa y cuántas llamadas se agendaron
- Rebotes, spam y bajas
- **Salida:** una recomendación concreta, y se anota en `RECOMENDACIONES.md`

---

## 8. Lo que falta para encender (datos de Dayana)

No los inventé. Están como marcadores en los archivos de secuencia:

| Marcador | Qué es | Dónde aparece |
|---|---|---|
| `[ENLACE ACERO]` | URL de la página de venta de la Especialización en ACERO | Secuencia A, correos 4, 5, 6, 7 |
| `[PRECIO ACERO]` | precio y forma de pago | Secuencia A, correo 4 |
| `[FECHA INICIO ACERO]` | cuándo arranca la próxima cohorte | Secuencia A, correos 4 y 7 |
| `[TESTIMONIO 1/2]` | dos casos reales de alumnos de acero | Secuencia A, correo 6 |

Si no hay cohorte con fecha, el correo 7 se cambia por el cierre de llamada
(está escrito el reemplazo en el propio archivo). Sin fecha real **no se
inventa urgencia**.

---

## 9. Enlaces fijos

| Qué | URL |
|---|---|
| Hub de recursos | `https://funnel.dgdesignmodeling.com/recursos` |
| Calculadora de Zapatas | `https://funnel.dgdesignmodeling.com/calculadora-zapatas` |
| Test de Nivel BIM | `https://funnel.dgdesignmodeling.com/test-nivel-bim` |
| Agendar llamada (30 min) | `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe` |
| Testimonios | `https://funnel.dgdesignmodeling.com/testimonio-estudiantes-egresados-diplomado` |
| Acreditaciones | `https://funnel.dgdesignmodeling.com/design-modeling-acreditaciones` |
| Comunidad | `https://designmodelingacademy.app.clientclub.net/communities/groups/comunidad-design/home` |

---

## 10. Lo que esta estrategia NO hace

- No manda WhatsApp masivo.
- No borra ni fusiona contactos — eso lo decides tú.
- No toca el bot de Instagram/Facebook ni las landings publicadas.
- No cotiza el Máster.
- No inventa fechas de cohorte ni precios.
