# Brief · Matriz de diciembre 2026 · contenido sintomático

> Decisión de Dayana (17-nov-2026): en diciembre apuntamos a **contenido sintomático**
> («contenido problemático»): piezas que describen el problema que el comprador está
> viviendo hoy, con sus palabras, para que sienta que hablamos de él.
> Este brief es la entrada del skill `matriz-mensual` cuando se arme diciembre.

---

## 1. Por qué (datos, no opinión)

**Referencia que trajo Dayana** · @fedecaball, reel del 17-nov
(`matriz-viral/fuentes/referentes/post-Df3Lew8AQ7g.json`):
14.662 vistas · 169 comentarios = **11,5 comentarios por 1.000 vistas**, casi todos la
palabra clave. Tesis del reel: el contenido educativo trae vistas; el que **describe el
síntoma** del cliente trae conversaciones con gente que de verdad necesita ayuda.

**Lo que ya mostraba nuestra cuenta** (es la misma regla con otro nombre):

| Dato | Fuente |
|---|---|
| Gancho que acusa un hábito: **8,61 c/1k** contra 0,54 de la declaración genérica | RECOMENDACIONES.md, 4 revisiones seguidas |
| «¿Cobras 5 USD por m²?»: la única pieza con conversación de su semana (11 comentarios, 9 contactos a COTIZA) | BRIEF-PATRICIO.md |
| Listas sin error (chuleta de cerchas), objeciones sueltas y «la IA te reemplaza»: **0 comentarios** | BRIEF-PATRICIO.md, COMPRADORES-VS-NO.md |
| DM224 «la misma zapata no se comporta igual»: ganadora del 9–15 nov, 69 comentarios | matriz.json |

Diferencia fina con lo que hacíamos: «acusar un hábito» señala **lo que la persona hace
mal**; «sintomático» describe **lo que le pasa** (la frustración, la consecuencia). En
diciembre usamos las dos, pero el gancho abre siempre por el síntoma.

---

## 2. La regla de diciembre

1. **Intención del feed: 60 / 15 / 25** (problema-síntoma / solución / objeciones y
   testimonios). Antes era 50 / 20 / 30.
2. **Cada pieza nombra un síntoma de uno de los 5 perfiles que compran**
   (`matriz/COMPRADORES-VS-NO.md`). Si no le habla a ninguno, no entra.
3. **El educativo puro se queda solo en chuletas y carruseles de guardado** (alcance),
   nunca como pieza de venta.
4. **Prohibido:** «la IA te va a reemplazar», listas sin error ni decisión, objeción
   suelta en semana floja (máximo 1 objeción por cada 2 piezas de síntoma).
5. **Palabras vivas:** NIVEL (Máster), ACERO, ZAPATA, MEMORIA, COTIZA. Antes de usar
   una, mirar `fuentes/openreply/campanas.json`.

---

## 3. Estructura de la pieza sintomática

**Reel (45–75 s), Gabriel a cámara:**

| Tramo | Qué dice | Ejemplo |
|---|---|---|
| 1 · Golpe (0–3 s) | El síntoma en segunda persona, sin rodeo | «Llevas 5 años en BIM y sigues siendo *el que modela*.» |
| 2 · Espejo | «A mí también me pasó» — historia corta y real de Gabriel o de un alumno | «Yo modelaba perfecto y nadie me llamaba a las reuniones de coordinación.» |
| 3 · La causa | Por qué pasa (no es falta de esfuerzo, es lo que nadie enseña) | «No es Revit. Es que nadie te enseñó a gestionar información.» |
| 4 · Giro | Lo que cambia cuando se resuelve | «Cuando armas el BEP, te sientan en la mesa.» |
| 5 · CTA | Palabra clave + recurso concreto | «Comenta NIVEL y te mando el test para ver en qué bloque estás.» |

**Carrusel:** portada = el síntoma; láminas 2–4 = las señales («te pasa esto si…»);
lámina 5 = la causa; lámina 6 = qué hacer; última = palabra clave.

---

## 4. Banco de síntomas por perfil (punto de partida para escribir las piezas)

| Perfil (COMPRADORES-VS-NO) | Síntoma (gancho) | Producto | Palabra |
|---|---|---|---|
| Ingeniero empleado al que le exigen BIM | «Llevas años en BIM y sigues siendo el que modela» | Máster · B2 Coordinador | NIVEL |
| Ingeniero empleado | «Te pidieron coordinar y nadie te enseñó a dirigir una reunión de interferencias» | Máster · B2 | NIVEL |
| Ingeniero empleado | «Sabes Revit, pero no sabes BIM» | Máster · B1 | NIVEL |
| Contratista con AutoCAD + Excel | «Haces todo dos veces: el plano en AutoCAD y las cantidades en Excel» | Máster · B1 / B3 5D | NIVEL |
| Contratista | «Tu presupuesto no cuadra con lo que se construyó y no sabes de dónde sale la diferencia» | Máster · B3 5D | NIVEL |
| Consultor independiente | «Ganaste el proyecto y perdiste plata porque no pusiste las rondas de revisión» | Cotizador | COTIZA |
| Consultor independiente | «Rechazas proyectos de acero porque no sabes si tu cálculo aguanta la revisión» | Acero | ACERO |
| Calculista | «Tu modelo en Robot da ratios de 1,4 y no sabes si es la sección o los apoyos» (caso real de Mark) | Acero | ACERO |
| Calculista | «Te devolvieron la memoria y el cálculo estaba bien» | Memoria | MEMORIA |
| Calculista | «La zapata te dio y el estudio de suelos dice otra cosa» | Zapatas | ZAPATA |
| Arquitecto joven remoto | «Aplicas a trabajos afuera y te piden ISO 19650 y no sabes qué responder» | Máster · B1 | NIVEL |
| Cualquiera que usa IA | «Le preguntas a ChatGPT y te da un número… que lleva tu firma» | Máster · B4 BIM + IA | NIVEL |

---

## 5. Lo que hay que resolver ANTES de armar diciembre

| Pendiente | Por qué importa | Quién |
|---|---|---|
| **Enlace de compra directa del Máster completo** | El precio de lista es **US$ 2.699,99** (matriz-viral/CLAUDE.md: «$500 de entrada, o $499,99 de matrícula + $160/mes × 12»). Pero no existe enlace de pago único por ese monto: ni en Stripe ni en el bot ni en GHL; solo la entrada de $499,99 y la factura mensual de $160 | Dayana / closer |
| **Fecha de la próxima cohorte del Máster** | En GHL `fecha_de_inicio` = «Próxima cohorte: consulta con tu asesor». La última cohorte es «mar26». Sin fecha no hay urgencia real en las piezas de venta | Dayana / Gabriel |
| **Choque de precios workshop vs Black Friday** | La oferta del workshop da −10 % por bloque (hasta el 18-nov); el guion del closer da −25 % del 27 al 30-nov. Hay que decidir qué se le respeta a quien compró con el workshop | Dayana |
| **Precio del combo Máster + App (Círculo de Fundadores)** | La app sola: US$ 997 + 97/mes. El combo no tiene cifra | Dayana / Gabriel |

En público el Máster sigue **sin precio**; el Black Friday, **solo con porcentajes**.

---

## 6. Cómo se usa

Al correr `matriz-mensual` para diciembre:
1. Leer este brief y `COMPRADORES-VS-NO.md`.
2. Escribir las piezas nuevas desde la tabla de la sección 4 (una por perfil como mínimo),
   con la estructura de la sección 3, y sumarlas con `scripts/sumar_piezas.py`.
3. Verificar el reparto 60/15/25 y las palabras vivas con `scripts/verificar_matriz_mes.py`.
