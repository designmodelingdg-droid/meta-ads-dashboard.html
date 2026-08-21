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

## 2. Lo que el reporte no ve: el dinero

Aquí está el hallazgo de la semana.

| | |
|---|---|
| Revenue que reporta el CRM | **$1.099,98** en 5 compras |
| **Cobrado de verdad** (Stripe + PayPal) | **$2.249,98** en 9 cobros |
| **Diferencia** | **+$1.150,00** |

Entró **el doble** de lo que el CRM registró. No es error del reporte: el
reporte lee bien el CRM. Es que **al CRM no le está llegando todo**.

Desglose de los 9 cobros reales:

| Fecha | Monto | Qué es |
|---|---|---|
| 13-ago | **$1.120,00** | ⚠️ **No aparece en el CRM.** Es la partida grande |
| 13-ago | $100,00 | reserva |
| 13-ago | $50,00 | — |
| 14-ago | $100,00 | reserva |
| 16-ago | $160,00 ×2 | recurrencia del Máster |
| 17-ago | $199,99 | ACERO |
| 18-ago | $160,00 | recurrencia del Máster |
| 19-ago | $199,99 | ACERO (factura 000212) |

**El cobro de $1.120 del 13 de agosto es lo que hay que rastrear.** Solo eso
explica casi toda la diferencia.

### El retorno honesto

El reporte dice **2,49x**. Contra lo cobrado de verdad:

| Cálculo | Retorno |
|---|---|
| Todo lo cobrado ÷ gasto | **5,11x** |
| Sin las recurrencias del Máster ($480) | **4,02x** |
| Sin recurrencias ni reservas ($200) | **3,57x** |

**El más honesto es 3,57x**, y aun así es 43% mejor que el 2,49x reportado.
Las recurrencias son de ventas viejas y las reservas de $100 son anticipo, no
venta cerrada — las tres cifras se dan juntas para que no haya trampa.

---

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

1. **Rastrear el cobro de $1.120 del 13-ago** y por qué no está en el CRM.
2. **Pedir que impriman las fechas exactas del periodo** en la cabecera.
3. **Vigilar México dos semanas** antes de tocar su presupuesto.
4. **Decidir sobre «Tráfico al perfil»**: tres auditorías sin generar negocio.
5. El reporte no trae **frecuencia**. Sin ella no se ve el desgaste, que es lo
   que anticipa la caída del CPL. Se pide para la próxima.
