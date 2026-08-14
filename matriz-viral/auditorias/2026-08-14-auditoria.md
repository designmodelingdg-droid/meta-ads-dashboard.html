# Auditoría del reporte — 14-ago-2026

**Fuente:** `app.olympusagencia.com/panel/dg` · ventana: últimos 30 días.
**Novedad:** el reporte cambió de herramienta y de fondo. Ya no es el PDF de
`olympus-os.vercel.app`: es un panel conectado a Meta **y al CRM**.

---

## 1. Lo que SÍ aplicaron (de lo que pedimos el 3-ago)

| Pedido el 3-ago | Estado |
|---|---|
| Incluir métricas de retorno | ✅ **Hecho.** Revenue, ROAS y CPA en cabecera |
| Conciliar píxel contra CRM | ✅ **Hecho.** «Ventas = oportunidades ganadas en el CRM» |
| Abrir el geo-split por país | ✅ **Hecho.** Tabla por país con CPA y % de compra |
| Generar con el periodo cerrado | ✅ Ventana configurable de 7/30/90 días |

**Y algo que no habíamos pedido y está muy bien:** separan **«Acero (cuota)»**
de «Acero». Las 2 cuotas de $100 no se cuentan como venta completa. Es
exactamente la regla que veníamos aplicando a mano.

**Y son honestos donde no saben:** *«CPA por adset queda “—” porque las ventas
CRM hoy no traen una llave confiable para amarrarlas al adset exacto»*. Decir
que no se puede en vez de inventar un número es lo que hace útil un reporte.

---

## 2. Los números de la ventana

| | |
|---|---|
| Leads Meta | 273 |
| Compras CRM | 21 |
| Revenue CRM | **$5.503,92** |
| Gasto Meta | $984,16 |
| CPA global | $46,86 |
| **ROAS** | **5,59x** |

**Aritmética verificada:** CPA, ROAS y % de compra cuadran exactamente. Las
sumas por producto y por país dan **21 compras y $5.503,92** las dos, sin
descuadre de un centavo. El reporte es internamente coherente.

> ⚠️ **No se pudo verificar contra Meta.** En esta sesión no había token de la
> API. Todo lo de abajo es auditoría interna del reporte, no contraste con la
> fuente. **Pendiente para la próxima.**

### Por producto

| Producto | Compras | Revenue |
|---|---|---|
| Acero | 6 | $1.199,95 |
| Paquete Autodesk | 6 | $449,98 |
| Diplomado | 4 | $1.700,00 |
| Naves SAP2000 | 2 | $53,99 |
| Acero (cuota) | 2 | $200,00 |
| Máster BIM | 1 | $1.900,00 |

---

## 3. Los tres problemas que sí hay

### 🚨 «Paquete Autodesk · % compra 120 %»

**Un porcentaje de compra por encima de 100 % es imposible** si se define como
compras ÷ leads. Son 6 compras con 5 leads.

Significa que hay compras atribuidas a una campaña que no generó esos leads.
Es el equivalente de la «frecuencia 0,86» del reporte anterior: la señal de que
el dato no sale de donde se cree. Con $6,12 de gasto y CPA de $1,02, ese
producto se ve como el más rentable de todos — y probablemente no lo es.

### 🚨 Los leads de la cabecera no cuadran con los de los adsets

| | Leads |
|---|---|
| Cabecera del reporte | **273** |
| Suma de la tabla de adsets | **1.263** |

Una diferencia de **990**. Son dos universos distintos —probablemente leads
atribuidos vs leads totales de formulario— pero el reporte no dice cuál es cuál.
Y de ahí sale la segunda inconsistencia: «Acero · % compra 0,7 %» con 6 compras
implicaría ~857 leads, no 273.

### ⚠️ El 38 % de las ventas no tiene anuncio atribuido

«Sin anuncio (landing/orgánico)»: **8 de 21 compras**, $976,98. Es un 18 % del
revenue. No está mal que exista —hay ventas que entran por orgánico— pero
mientras sea casi 4 de cada 10, el CPA y el ROAS por anuncio están calculados
sobre una parte del total.

---

## 4. El dato que cambia una decisión

La tabla por país dice esto:

| País | Leads | Compras | Revenue | CPA |
|---|---|---|---|---|
| 🇪🇨 Ecuador | 137 | **9** | **$3.226,97** | $34,99 |
| 🇲🇽 México | 48 | 4 | $1.099,99 | $81,89 |
| 🇸🇻 El Salvador | 4 | 2 | $399,99 | $10,74 |
| 🇬🇹 Guatemala | 24 | 1 | $199,99 | $121,35 |
| 🇨🇱 Chile | 30 | 1 | $19,99 | $104,34 |

**Esto contradice el supuesto con el que veníamos trabajando.** La instrucción
del 8-ago fue *«bajarle a Guatemala y subirle a Ecuador, pero sin sacar
Guatemala, porque Ecuador no compra tanto como México o Guate»*.

Con este dato, **Ecuador es a la vez el que más compra ($3.227 de revenue, 9 de
21 ventas) y el del CPA más bajo de los grandes ($34,99)**. Guatemala es 1 venta
con el CPA más alto de la tabla ($121,35).

**No lo doy por bueno todavía**, por dos motivos: el reporte no está verificado
contra Meta, y el 38 % de ventas sin anuncio puede estar cargándose a un país
por el teléfono del lead. **Es la pregunta para el equipo**, no una decisión
tomada.

---

## 5. Cómo vamos, en una frase

**Bien, y por primera vez se puede afirmar con un número:** $984 de pauta
produjeron $5.504 registrados en el CRM. El reporte pasó de ser una lista de
métricas de vanidad a un panel de retorno, y aplicaron las cuatro correcciones
que se pidieron el 3-ago.

Lo que falta es que los denominadores cuadren.
