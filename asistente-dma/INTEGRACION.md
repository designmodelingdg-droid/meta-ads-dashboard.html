# Integración con `dma-sales-assistant`

Los tres módulos de esta carpeta (`asistente_agent.py`, `google_client.py`,
`panorama.py`) están escritos para vivir **en la raíz** del repo
`designmodelingdg-droid/dma-sales-assistant`, junto a `server.py`.

Lo mejor del montaje: el bot ya tiene todo lo difícil resuelto y el enganche real
es **de una línea**.

---

## Por qué el enganche es tan pequeño

Recorrido de una nota de voz tuya, hoy, sin tocar nada:

| Paso | Dónde | Estado |
|---|---|---|
| Llega el audio a GHL | `server.py:3405` `/webhook/ghl` | ✅ ya existe |
| Se transcribe con Whisper | `media_handler.transcribe_audio`, llamado en `server.py:2624` | ✅ **ya existe** |
| Se reconoce que eres tú | `is_admin()` con `ADMIN_DMA_PHONES` (`server.py:432`) | ✅ ya existe |
| Se enruta como comando admin | `is_admin_message()` → `handle_admin_command()` (`server.py:2700`, `2742`) | ✅ ya existe |
| El texto libre cae al fallback | `server.py:943` → `claude.interpret_admin_command()` | ⬅️ **aquí entra el asistente** |

Ese fallback hoy es una llamada a Haiku **sin herramientas**: solo conversa, no
puede hacer nada. Es literalmente el hueco donde faltaba el agente.

---

## Paso 1 — Copiar los tres módulos

```bash
cp asistente-dma/asistente_agent.py  <repo dma-sales-assistant>/
cp asistente-dma/google_client.py    <repo dma-sales-assistant>/
cp asistente-dma/panorama.py         <repo dma-sales-assistant>/
```

## Paso 2 — El parche de una línea

En `server.py`, dentro de `handle_admin_command`, la rama del final
(**línea 941-950**, "comando libre → Claude lo interpreta"):

```python
    # ── comando libre → Claude lo interpreta (fallback) ──
    else:
        try:
            resp = claude.interpret_admin_command(command)        # ← ANTES
```

queda así:

```python
    # ── comando libre → Jefe de Gabinete (agente con herramientas) ──
    else:
        try:
            if os.getenv("ASISTENTE_ACTIVO", "1") == "1":
                import asistente_agent
                resp, _hist = asistente_agent.responder(
                    command,
                    historial=_ASISTENTE_HIST.get(contact_id),
                )
                # Se guardan solo los últimos turnos: sin esto, "sí, mándalo"
                # no sabe a qué se refiere; con todo, el contexto crece sin fin.
                _ASISTENTE_HIST[contact_id] = _hist[-12:]
            else:
                resp = claude.interpret_admin_command(command)
        except Exception as _ai_err:
            log.error(f"❌ Asistente falló: {_ai_err}")
            resp = (
                f"❓ No pude procesar: \"{command[:50]}\"\n\n"
                f"Escribe *ayuda* para ver los comandos exactos."
            )
```

Y arriba, junto a `ADMIN_STATE` (`server.py:319`):

```python
# Historial del asistente ejecutivo, por contacto admin.
# En memoria: railway.toml fuerza --workers 1, así que hay un solo proceso.
# Si algún día se sube a varios workers, esto debe pasar a Redis o a GHL.
_ASISTENTE_HIST: dict[str, list] = {}
```

### Por qué así y no reemplazando todo `handle_admin_command`

Los comandos literales (`status`, `pausa X`, `link 70`, `escanear`) los usan
**6 personas** de la whitelist, no solo tú. Si el agente se los come, cambias el
flujo de trabajo del equipo entero sin avisar. Con este parche:

- Los comandos exactos siguen funcionando igual de rápido y sin costo de tokens.
- Solo lo que **hoy ya no funciona** (hablar normal) pasa por el agente.
- `ASISTENTE_ACTIVO=0` lo apaga sin redeploy si algo sale mal.

## Paso 3 — El prefijo `/dma` y las notas de voz

Hay un detalle real: `is_admin_message()` exige que el mensaje empiece con `/dma`.
En una **nota de voz** eso es un problema — tendrías que decir "barra dma" en voz
alta y confiar en que Whisper lo transcriba bien.

Dos salidas, elige una:

**A — Decir "asistente" al empezar la nota** (cero cambios de código): agrega el
disparador a la lista de prefijos aceptados en `server.py:449`:

```python
PREFIJOS_ADMIN = (ADMIN_PREFIX, "asistente", "oye asistente")

def is_admin_message(phone: str, message: str) -> bool:
    msg = (message or "").strip().lower()
    if not any(msg.startswith(p) for p in PREFIJOS_ADMIN):
        return False
    return is_admin(phone)
```

**B — Sin prefijo, solo para tu número personal** (más cómodo, más delicado):
`593983241210` es tuyo y no es un lead, así que todo lo que llegue de ahí puede ir
directo al asistente:

```python
ASISTENTE_SIN_PREFIJO = {"593983241210"}   # solo Dayana personal

def is_admin_message(phone: str, message: str) -> bool:
    clean = _clean_phone(phone)
    if any(clean.endswith(p[-9:]) for p in ASISTENTE_SIN_PREFIJO):
        return True
    ...
```

Recomiendo **A para arrancar**: es reversible y no cambia el comportamiento de
ningún otro número de la whitelist. Cuando confíes en el asistente, pasas a B.

## Paso 4 — Brief matutino

Al final de `server.py`, junto a los otros `_scheduler.add_job` (`:4466`):

```python
def _job_brief_matutino():
    import panorama, whatsapp_cloud
    from config import ADMIN_PHONE
    try:
        whatsapp_cloud.send_text(ADMIN_PHONE, panorama.brief_matutino())
    except Exception as e:
        log.error(f"❌ Brief matutino falló: {e}")

_scheduler.add_job(_job_brief_matutino, "cron", hour=7, minute=0,
                   timezone=TZ_EC, id="brief_matutino", replace_existing=True)
```

> ⚠️ **Ventana de 24 h de WhatsApp.** Si llevas más de 24 h sin escribirle al bot,
> Meta bloquea el mensaje libre y el brief no llega. Para que sea confiable hay
> que mandarlo como **plantilla aprobada** con `whatsapp_cloud.send_template()`.
> Hay que crear esa plantilla en el Business Manager antes de confiar en esto.

## Paso 5 — Dependencias y variables

`requirements.txt` no necesita nada nuevo: `requests`, `anthropic` y `pytz` ya
están. `google_client.py` usa REST directo justamente para no meter el SDK de
Google.

Variables nuevas en Railway (ver `GUIA-MONTAJE.md` para conseguirlas):

```
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REFRESH_TOKEN
GOOGLE_CALENDAR_PRINCIPAL=designmodelingdg@gmail.com
GOOGLE_CARPETA_NOTAS          (opcional: id de la carpeta de Drive para notas)
ASISTENTE_MODEL=claude-sonnet-5
ASISTENTE_ACTIVO=1
```

---

## Qué quedó probado y qué no

Probado en el entorno de construcción, sin red hacia Google ni GHL:

- ✅ Los tres módulos compilan e importan en Python 3.11.
- ✅ Los 12 schemas de herramientas están bien formados.
- ✅ **La guardia de confirmación funciona:** `enviar_mensaje_a_contacto` con
  `confirmado=false` devuelve "PENDIENTE DE CONFIRMACIÓN" sin siquiera importar
  `ghl_client` — no hay forma de que envíe algo por accidente.
- ✅ Los fallos de herramienta se devuelven como texto, nunca como excepción:
  una caída de GHL no tumba la conversación.
- ✅ `panorama()` degrada bloque por bloque: si Meta Ads falla, el resto sale.
- ✅ Las fechas se resuelven con offset de Ecuador (`-05:00`), y una fecha basura
  cae a hoy en vez de reventar.

**No probado aquí** (no había API key de Anthropic en el entorno de construcción):

- ⚠️ El round-trip real con el modelo: que Claude elija bien las herramientas
  ante una transcripción sucia. **Esto hay que probarlo en Railway**, con los
  casos 3-6 de abajo. Es lo primero que debes verificar tras el despliegue.
- ⚠️ Las llamadas reales a Google (hacen falta las credenciales del paso 5).

## Prueba end-to-end

1. `python -c "import asistente_agent, google_client, panorama"` — importa limpio.
2. `python -c "import google_client; print(google_client.credenciales_ok())"` → `True`.
3. Desde tu WhatsApp, **texto**: `asistente ¿qué tengo hoy?` → devuelve la agenda.
4. **Nota de voz**: *"asistente, agéndame mañana a las 4 de la tarde reunión con
   Patricio"* → aparece el evento y responde confirmando.
5. **Nota de voz con dos órdenes**: *"agéndame el jueves a las 10 con Ester y
   recuérdame llamar al proveedor el viernes"* → un evento **y** una tarea.
6. **Irreversible**: *"escríbele a Carlos que la oferta vence hoy"* → **pide
   confirmación** y no envía nada hasta que respondas "sí".
7. `asistente ¿cómo vamos?` → panorama comercial.
8. `status` (comando de siempre) → sigue respondiendo igual que antes. **Esta es
   la prueba de no-regresión.**
9. Desde un número que NO sea admin, escribir cualquier cosa → responde el bot de
   ventas de siempre, sin rastro del asistente.
