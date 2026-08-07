# Auditoría del reporte — semana 1 al 7 de agosto 2026

## Veredicto: el reporte está bien. La cuenta no.

**Todas las cifras verificadas contra la API de Meta coinciden.** Es un cambio
grande respecto al del 3-ago, donde fallaban todas.

| Dato | Reporte | Meta | |
|---|---|---|---|
| Inversión total | $167 | $167,25 | ✓ |
| Gasto diario (6 días) | — | — | ✓ exacto los 6 |
| Alcance de cuenta | 74,7K | 74.691 | ✓ |
| Frecuencia de cuenta | 1,46 | 1,46 | ✓ |
| Impresiones | 108,9K | 108.851 | ✓ |
| Clics | 4.566 | 4.566 | ✓ |
| CTR | 4,19% | 4,19% | ✓ |
| Conversaciones | 168 | 168 | ✓ |
| Leads | 41 | 41 | ✓ |
| Compras / valor | 5 / $1.000 | 5 / $1.000 | ✓ |
| Alcance y frecuencia por campaña | — | — | ✓ los tres |

## Las cuatro correcciones pedidas el 3-ago

| Lo que se pidió | Estado |
|---|---|
| Generar el reporte con el periodo cerrado | ✅ los 6 días cuadran al centavo |
| Corregir alcance y frecuencia | ✅ ahora salen de Meta |
| Incluir métricas de retorno | ✅ 5 compras, $1.000, y avisan de la frecuencia 2,22 |
| Abrir el geo-split por país | ✅ con tabla por país |

Las cuatro aplicadas. Hay que reconocerlo.

## Lo que el reporte NO vio, y es lo que importa

**La cuenta publicitaria dejó de gastar.**

| Día | Gasto |
|---|---|
| 1–5 ago | ~$30/día |
| **6 ago** | **$9,10** (−70%) |
| **7 ago** | **$0** |

Causa, según la API de Meta:

- `account_status: 3` → **cuenta sin liquidar** (hay un pago pendiente)
- `balance: $104,96` sin pagar, sobre una cuenta de PayPal
- El tope de gasto **no** es el problema: quedan $653,80 de $2.500

Las campañas siguen en ACTIVE. No es que alguien las pausara: **Meta cortó la
entrega por el saldo pendiente.**

El reporte, en cambio, concluye que «hay potencial para invertir más
agresivamente» y recomienda subir a $600-800 al mes. Recomienda escalar una
cuenta que está parada.

## Lo demás que se ve en los datos

- **MASTER - FORM V2 va en frecuencia 2,22** con solo 6.641 personas de
  alcance. El reporte lo menciona, y tiene razón: ahí toca creativo nuevo.
- **Guatemala está cara**: $1,30 por conversación contra $0,46 de Ecuador.
  Casi el triple. Es la primera semana con el split abierto y ya se ve.
- **Ecuador es el más barato** y solo se lleva el 27% del presupuesto de ACERO.

