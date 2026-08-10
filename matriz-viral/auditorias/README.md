# Auditorías del reporte semanal de pauta

Una carpeta por semana con el reporte que manda la agencia y lo que salió al
verificarlo contra Meta y contra el CRM.

Formato: `AAAA-MM-DD-reporte.md` (lo que mandaron) y
`AAAA-MM-DD-auditoria.md` (lo que encontramos).

Sirve para dos cosas: ver si las correcciones pedidas se aplican, y comparar
semana contra semana sin fiarnos de la memoria.

Lo corre el skill `auditoria-pauta`, los viernes.

## Historial

| Fecha | Qué se encontró | Se pidió corregir |
|---|---|---|
| 2026-08-03 | El reporte se generó antes de cerrar el último día: marcaba $11 y cerró en $32,67. Gasto real $231,38 contra $210 reportado. Alcance real 90.115 contra ~23K. Una frecuencia de 0,86, que es imposible. Costo por conversación $0,50 y no $0,40. Sumaron conversaciones con leads. No abrieron el geo-split. Las métricas de retorno ya estaban en Meta (8 compras, ROAS 17,3x) y no las incluyeron. | 1) generar el reporte con el periodo cerrado · 2) corregir alcance y frecuencia · 3) incluir retorno y conciliar píxel contra CRM · 4) abrir el geo-split por país |
