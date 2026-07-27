# DMA Chief of Staff — Blueprint

> Redactado con la metodología de **the-architect**
> (`designmodelingdg-droid/the-architect`, plantilla `templates/blueprint-template.md`).
>
> **Adaptación deliberada:** the-architect está pensado para productos web
> (sus 6 arquetipos son `saas-webapp`, `marketing-site`, `api-backend`,
> `mobile-app`, `content-platform`, `internal-tool`). Esto no es ninguno de los
> seis: es un **agente conversacional sobre un servicio ya desplegado**. El
> arquetipo más cercano es `internal-tool`, así que se conservan las secciones
> que aplican (stack, estructura, modelo de datos, build order, entorno,
> despliegue, pruebas, reglas no negociables) y se **omiten** las de frontend y
> design system —no hay interfaz gráfica, la interfaz es WhatsApp.

---

## 1. Visión

### El problema

Design Modeling Academy ya tiene un bot que atiende **clientes**
(`dma-sales-assistant`: vende el Máster, da soporte académico, cobra por Stripe).
Lo que no existe es lo contrario: algo que atienda **a Dayana**.

Hoy, para saber cómo va su empresa, tiene que abrir GoHighLevel, el
Administrador de Anuncios de Meta, Google Calendar y Stripe. Para agendar algo
mientras maneja, tiene que parar. Para no olvidar una idea, se la manda a sí
misma por WhatsApp y ahí se pierde.

### La solución

Un jefe de gabinete al que le manda una **nota de voz** y que, a partir de eso,
agenda, crea tareas, guarda notas y le devuelve el panorama real del negocio.

### Objetivos

1. Que dictar una orden y que quede hecha tome menos de 30 segundos.
2. Que "¿cómo vamos?" se responda en un solo mensaje, sin abrir ningún panel.
3. Que nada de lo que dicte se pierda.
4. Que **el bot de ventas no se vea afectado en absoluto**.

### Métricas de éxito

- Una nota de voz con 2 órdenes distintas ejecuta las 2 (hoy: 0).
- El brief de las 7:00 llega todos los días laborables.
- Cero incidentes de mensajes enviados a un cliente sin confirmación.
- Cero regresiones en los comandos `/dma` que ya usa el equipo.

---

## 2. Stack

| Capa | Elección | Por qué |
|---|---|---|
| Runtime | Python 3 / Flask | Ya es el del bot. Cambiar de stack sería reescribir. |
| Modelo | `claude-sonnet-5` con **tool use** | El razonamiento sobre transcripciones sucias y fechas relativas necesita más que Haiku; Sonnet 5 da la calidad de tool-calling sin el costo de Opus. Configurable con `ASISTENTE_MODEL`. |
| Transcripción | Whisper, vía `media_handler.py` | **Ya está construido y probado en producción.** |
| Canal | WhatsApp a través de GoHighLevel | Ya es el canal del bot. Cero infraestructura nueva. |
| Agenda / tareas / notas | Google Calendar + Tasks + Drive, REST directo | Es lo que pidió el encargo. REST en vez del SDK de Google para no engordar `requirements.txt`. |
| CRM | GoHighLevel vía `ghl_client.py` | 825 líneas ya escritas y en uso. |
| Anuncios | Meta Ads vía `meta_ads.py` | Ya existe. |
| Programación | APScheduler | Ya está en el proceso, `server.py:4466`. |
| Despliegue | Railway | Ya está vivo. |

### Lo que se decidió NO usar

- **Google Tasks SDK** — el REST con `requests` son 40 líneas y evita 6 dependencias.
- **Base de datos** — `railway.toml` fuerza `--workers 1`; un dict en memoria
  alcanza para el historial de conversación. Meter Postgres aquí sería
  infraestructura para un problema que no existe todavía.
- **Número de WhatsApp nuevo** — el webhook y la whitelist de admins ya existen.
- **Un servicio aparte** — desplegar un segundo servicio duplicaría credenciales,
  logs y costos para reutilizar los mismos módulos.

---

## 3. Estructura

Los tres módulos van a la **raíz** de `dma-sales-assistant`, junto a `server.py`:

```
dma-sales-assistant/
├── server.py               ← 1 parche en handle_admin_command (línea ~941)
├── asistente_agent.py      ← NUEVO · cerebro: system prompt + TOOLS + loop
├── google_client.py        ← NUEVO · Calendar + Tasks + Drive (OAuth propio)
├── panorama.py             ← NUEVO · agregador del estado de la empresa
├── media_handler.py        ← sin cambios (ya transcribe)
├── ghl_client.py           ← sin cambios (se consume)
├── meta_ads.py             ← sin cambios (se consume)
└── daily_report.py         ← sin cambios (se consume)
```

---

## 4. Modelo de datos

No hay base de datos. El estado vive donde ya vive el dato real:

| Dato | Dónde vive | Por qué ahí |
|---|---|---|
| Eventos | Google Calendar | Es el calendario que ella ya usa. |
| Tareas | Google Tasks | Sincroniza solo con su móvil. |
| Notas | Google Docs (Drive) | Buscables, compartibles, editables después. |
| Leads / oportunidades | GoHighLevel | Única fuente de verdad comercial. |
| Historial de conversación | `_ASISTENTE_HIST` en memoria, últimos 12 turnos | Solo sirve para resolver "sí, mándalo". Perderlo en un reinicio no cuesta nada. |

### Lista blanca de calendarios — la decisión menos obvia

La cuenta tiene **~90 calendarios**, casi todos de Google Classroom (uno por
curso: `DET4: Curso Especializado ETABS…`, `ARR2: Detallado de Refuerzo…`).

Si el agente lee todos, "¿qué tengo hoy?" devuelve 40 clases y entierra la única
reunión que importa. Por eso `google_client.CALENDARIOS_AGENDA` fija seis:
Personal, Familia, Plan de ventas, Máster BIM + IA, Design Modeling Academy y
Tareas Hubspot. Los de Classroom se consultan aparte, solo si se pregunta por
clases.

---

## 5. Herramientas del agente

Es el equivalente al "API design" de un producto web: el contrato entre el
modelo y el mundo.

| Herramienta | Reversible | Qué hace |
|---|---|---|
| `ver_agenda` | lectura | Eventos en un rango, solo calendarios de la lista blanca. |
| `crear_evento` | ✅ sí | Agenda. Duración por defecto 1 h. |
| `mover_evento` | ✅ sí | Cambia la hora. |
| `buscar_hueco` | lectura | Huecos libres respetando horario laboral y fines de semana. |
| `crear_tarea` | ✅ sí | Google Tasks, con fecha opcional. |
| `ver_tareas` | lectura | Pendientes, vencidas primero. |
| `completar_tarea` | ✅ sí | Marca hecha. |
| `crear_nota` | ✅ sí | Google Doc con el dictado ordenado. |
| `buscar_nota` | lectura | Búsqueda por texto en Drive. |
| `panorama_empresa` | lectura | Secciones a la carta: agenda, tareas, comercial, ads, académico. |
| `buscar_contacto` | lectura | Ficha de GHL: etiquetas, oportunidad, teléfono. |
| `enviar_mensaje_a_contacto` | ❌ **NO** | Manda WhatsApp a un contacto. **Exige `confirmado: true`.** |

### La regla de autonomía

Reversible → se ejecuta directo. Pedir permiso para agendar arruinaría el
producto: el punto es dictar y seguir manejando.

Irreversible o hacia afuera → se confirma antes. Una transcripción mal entendida
que agenda algo se arregla en 5 segundos; una que le escribe al cliente
equivocado, no.

La regla está **en dos capas**: escrita en el system prompt *y* verificada en el
dispatcher (`ejecutar_tool` devuelve "PENDIENTE DE CONFIRMACIÓN" si
`confirmado` no viene en `true`). Confiar solo en el prompt sería confiar en que
el modelo nunca se equivoque.

---

## 6. Orden de construcción

1. **`google_client.py`** — OAuth + Calendar. Probar con `credenciales_ok()`.
   Sin esto no hay nada más. *(hecho)*
2. **Tasks y Drive** en el mismo módulo. *(hecho)*
3. **`panorama.py`** componiendo `daily_report`, `meta_ads`, `academico_progreso`. *(hecho)*
4. **`asistente_agent.py`** — prompt, TOOLS, dispatcher, loop. *(hecho)*
5. **Parche en `server.py`** — fallback + historial + prefijo de voz. *(documentado en `INTEGRACION.md`)*
6. **Credenciales de Google en Railway** — requiere a Dayana. *(`GUIA-MONTAJE.md`)*
7. **Brief matutino** con APScheduler, y su plantilla de WhatsApp aprobada.
8. **Segunda tanda:** correo (Gmail), reuniones (Fathom/Zoom ya conectados),
   delegar tareas al equipo, mover oportunidades en GHL.

---

## 7. Entorno

### Variables nuevas

```
GOOGLE_CLIENT_ID              obligatoria
GOOGLE_CLIENT_SECRET          obligatoria
GOOGLE_REFRESH_TOKEN          obligatoria
GOOGLE_CALENDAR_PRINCIPAL     default designmodelingdg@gmail.com
GOOGLE_CARPETA_NOTAS          opcional, id de carpeta de Drive
ASISTENTE_MODEL               default claude-sonnet-5
ASISTENTE_ACTIVO              1 activo · 0 vuelve al fallback viejo, sin redeploy
```

### Dependencias nuevas

Ninguna. `requests`, `anthropic` y `pytz` ya están en `requirements.txt`.

---

## 8. Pruebas

Ver el checklist end-to-end de `INTEGRACION.md`. Los tres casos que de verdad
importan:

- **Dos órdenes en una sola nota de voz** → se ejecutan las dos. Es lo que la
  arquitectura vieja de `detect_*` no podía hacer.
- **Acción irreversible** → pide confirmación y no envía nada sin el "sí".
- **No-regresión:** `status` y `pausa X` siguen funcionando igual, y un lead
  cualquiera sigue recibiendo el bot de ventas sin cambios.

---

## 9. Reglas no negociables

1. **`--workers 1` se mantiene.** El anti-duplicación del bot de ventas vive en
   memoria de un proceso (`railway.toml` lo explica). Subir workers manda
   mensajes dobles a clientes reales.
2. **El asistente nunca responde a un no-admin.** Se activa solo tras
   `is_admin()`. Si falla, falla en silencio hacia el flujo de ventas normal.
3. **Nada de escribir hacia afuera sin `confirmado: true`.**
4. **La lista blanca de calendarios no se quita.** Existe por los ~90 calendarios
   de Classroom.
5. **`ASISTENTE_ACTIVO=0` siempre debe devolver el comportamiento anterior.** Es
   el freno de mano.
6. **El asistente no cotiza ni negocia el Máster.** Eso es del bot de ventas;
   mezclarlos rompe el guion comercial.
7. **Ningún secreto en el repo.** Todo por variables de entorno de Railway.
