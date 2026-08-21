# Auditoría del reporte semanal — 20-ago-2026

**Reporte:** `app.olympusagencia.com/panel/dg` · ventana de 7 días
**Verificado contra:** `fuentes/ads-insights/` (Graph API) y `fuentes/ingresos/`
(Stripe + PayPal), datos del repo al 19-ago.

---

## 0. Lo primero: aplicaron los cuatro cambios

Los cuatro que se pidieron el 3-ago están hechos. Conviene decirlo:

| Se pidió el 3-ago | Estado |
|---|---|
| Abrir el geo-split por país | 🟢 **Hecho.** 12 adsets con su CPL |
| Incluir métricas de retorno | 🟢 **Hecho.** Revenue, CPA y ROAS |
| Conciliar píxel contra CRM | 🟢 **Hecho.** Tabla «Ventas reales (CRM)» |
| Generar con el periodo cerrado | 🟡 **Casi.** Ver §2 |

Y definen los leads igual que nosotros: *«conversaciones de WhatsApp iniciadas +
leads de formulario»*. Es la definición correcta, y es la que hace que las
tablas cuadren entre sí.

---

## 1. El gasto cuadra

| | Reporte | Nuestro dato (13→19 ago) | Diferencia |
|---|---|---|---|
| Gasto | $442,32 | $440,17 | **+$2,15 (0,5%)** |
| Leads | 612 | 568 | +44 (7,7%) |

**El gasto está bien.** Medio punto de diferencia es ruido de ventana.

Los leads bailan un 7,7%. La causa más probable es que su ventana está corrida
un día respecto a la nuestra —la nuestra cierra el 19— y no que el dato esté
mal. **Se les pide que impriman las fechas exactas del periodo en la cabecera**,
que es lo único que falta para poder cuadrar sin adivinar.

---

## 2. El dinero, ya con la corrección de Dayana

> **Corrección del 20-ago.** La primera versión de esta auditoría decía que el
> cobro de $1.120 del 13-ago era una venta sin registrar, y calculaba un retorno
> de 3,57x. **Estaba mal.** Dayana confirmó que son **dos alumnos del Máster que
> venían pagando $160 al mes y liquidaron el saldo de una vez.** Es recurrencia
> de una venta vieja, no venta nueva. Recalculado abajo.

Entraron **$2.249,98** por pasarela. Pero casi todo es de ventas ya hechas:

| Concepto | Monto | ¿Venta nueva? |
|---|---|---|
| 2 alumnos liquidan el Máster (13-ago) | $1.120,00 | ❌ recurrencia |
| 3 cuotas de $160 del Máster | $480,00 | ❌ recurrencia |
| 2 reservas de $100 | $200,00 | ❌ anticipo |
| 2 × ACERO ($199,99) | $399,98 | ✅ |
| 1 cobro de $50 | $50,00 | ✅ sin identificar |
| **Venta nueva por pasarela** | **$449,98** | |

### Y el CRM tiene ventas que la pasarela no ve

Al revés de lo que parecía. El CRM registra **Diplomado $500** y **Paquete
Autodesk $299,99** que **no aparecen en Stripe ni en PayPal** — o sea que
entraron por transferencia o efectivo, que la pasarela no puede ver.

| | |
|---|---|
| Venta nueva por pasarela | $449,98 |
| Venta nueva solo en el CRM (transferencia) | $799,99 |
| **VENTA NUEVA TOTAL** | **$1.249,97** |
| Gasto de pauta | $440,17 |
| **RETORNO REAL** | **2,84x** |

**El reporte dice 2,49x. El real es 2,84x.** La agencia estaba mucho más cerca
de lo que parecía: la diferencia son las dos ventas por transferencia y el
segundo ACERO.

### Lo único que sigue sin cuadrar

**La pasarela muestra DOS cobros de ACERO ($199,99 el 17-ago por PayPal y
$199,99 el 19-ago por Stripe, factura 000212) y el CRM registra UNO.** Es una
venta real que no está en el pipeline. Vale la pena revisar cuál de las dos
falta y por qué.

> **La lección de método:** ninguna de las dos fuentes lo ve todo. La pasarela
> no ve transferencias ni efectivo; el CRM no ve lo que nadie registra. Y las
> recurrencias inflan la pasarela si no se separan. **El retorno honesto solo
> sale cruzando las dos y quitando lo que no es venta nueva.**

## 3. La decisión de la semana: México

El geo-split que ahora sí abren deja ver esto:

| País | Gasto | Leads | Compras | Revenue |
|---|---|---|---|---|
| 🇪🇨 Ecuador | $143,30 | 202 | **2** | $600,00 |
| 🇲🇽 México | $136,78 | **237** | **0** | — |

**Casi el mismo gasto. México trae MÁS leads y CERO compras.**

Y los adsets mexicanos son los de CPL más bajo de toda la cuenta: MX Acero FORM
a **$0,32** y el resto de LATAM a $0,30. Ese CPL barato es justo lo que engaña:
son los leads que menos cuestan y los que no compran.

No es para apagar México de golpe —una semana no es una tendencia— pero sí para
mirarlo dos semanas seguidas antes de seguir subiendo su presupuesto.

### Y otra vez «Tráfico al perfil»

| Adset | Gasto | Leads | CPL |
|---|---|---|---|
| ADVTG+ · 🟢[12MAYO] TRÁFICO AL PERFIL - IG | $25,50 | **1** | **$25,50** |

En la ventana de 30 días esta campaña llevaba $81,52 con **cero** leads. Ahora
suma $25,50 más por un solo lead. Es la única de la cuenta que no genera
negocio y lleva tres auditorías apareciendo.

---

## 4. Lo que sí está funcionando

**Los dos anuncios que vendieron**, con su retorno real por anuncio:

| Anuncio | Gasto | Leads | Compras | Revenue | ROAS |
|---|---|---|---|---|---|
| 🟡[18MAYO] MASTER - FORM V2 | $23,00 | 20 | 1 | $500,00 | **21,74x** |
| 🟡 [JUL] ESPE.1 ACERO - WSP SMS | $24,79 | 18 | 1 | $199,99 | **8,07x** |

Con $47,79 entre los dos trajeron $699,99. **Ahí es donde está el dinero**, no
en los adsets de CPL barato.

---

## 5. Lo que queda abierto

1. **Cuadrar el segundo ACERO**: la pasarela muestra dos cobros de $199,99 y el CRM registra uno.
2. **Pedir que impriman las fechas exactas del periodo** en la cabecera.
3. **Vigilar México dos semanas** antes de tocar su presupuesto.
4. **Decidir sobre «Tráfico al perfil»**: tres auditorías sin generar negocio.
5. El reporte no trae **frecuencia**. Sin ella no se ve el desgaste, que es lo
   que anticipa la caída del CPL. Se pide para la próxima.
