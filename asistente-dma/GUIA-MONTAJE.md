# Guía de montaje — credenciales

Es la parte que no puedo hacer por ti: Google y ClickUp exigen que el dueño de
la cuenta autorice desde su navegador. Son ~20 minutos en total, una sola vez.

| Paso | Qué consigues | Cuánto tarda | ¿Obligatorio? |
|---|---|---|---|
| 1-5 | Credenciales de Google (agenda, tareas, notas) | ~15 min | **Sí** |
| 6 | Token de ClickUp (tareas al equipo) | 2 min | Sí, si quieres asignar tareas |
| 7 | Plantilla de WhatsApp (recordatorios fiables) | 5 min + espera de Meta | Recomendado |

Si te cansas, para después del paso 5: el asistente ya funciona con agenda,
tareas y notas. Los pasos 6 y 7 suman capacidades, no arreglan nada roto.

> **Por qué OAuth de usuario y no una cuenta de servicio:** Google Tasks y tu
> calendario personal viven en tu cuenta. Una cuenta de servicio es una identidad
> aparte — no ve tus tareas ni tu calendario a menos que uses delegación de
> dominio, que requiere Google Workspace de pago. Con OAuth de usuario, el
> asistente actúa **como tú**, que es justo lo que quieres.

---

## 1. Crear el proyecto y activar las APIs

1. Entra a [console.cloud.google.com](https://console.cloud.google.com) con
   **designmodelingdg@gmail.com**.
2. Arriba a la izquierda, selector de proyecto → **Proyecto nuevo** →
   nombre: `DMA Asistente` → **Crear**.
3. Asegúrate de estar dentro de ese proyecto (aparece arriba).
4. Ve a **APIs y servicios → Biblioteca** y activa **las tres**, una por una
   (buscar → **Habilitar**):
   - **Google Calendar API**
   - **Google Tasks API**
   - **Google Drive API**

## 2. Pantalla de consentimiento

1. **APIs y servicios → Pantalla de consentimiento de OAuth**.
2. Tipo de usuario: **Externo** → **Crear**.
3. Rellena solo lo obligatorio:
   - Nombre de la app: `DMA Asistente`
   - Correo de asistencia: `designmodelingdg@gmail.com`
   - Datos de contacto del desarrollador: `designmodelingdg@gmail.com`
4. **Guardar y continuar** en Permisos (no toques nada) y en Usuarios de prueba.
5. En **Usuarios de prueba** → **Añadir usuarios** → `designmodelingdg@gmail.com`.
   > Sin este paso Google te va a rechazar con "acceso bloqueado".
6. **Guardar**.

> La app queda en modo *Prueba*. Es correcto: el refresh token de un usuario de
> prueba caduca a los 7 días **solo si la app sigue en prueba y usa scopes
> sensibles**. Para que no caduque, en la pantalla de consentimiento pulsa
> **Publicar aplicación** (estado *En producción*). Google mostrará un aviso de
> "app no verificada" la primera vez — como eres la única usuaria, acepta con
> **Configuración avanzada → Ir a DMA Asistente**. No hace falta verificación de
> Google mientras no la use gente externa.

## 3. Crear las credenciales

1. **APIs y servicios → Credenciales → Crear credenciales → ID de cliente de OAuth**.
2. Tipo de aplicación: **Aplicación de escritorio**.
3. Nombre: `DMA Asistente CLI` → **Crear**.
4. Copia el **ID de cliente** y el **Secreto de cliente**. Son tus
   `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`.

## 4. Obtener el refresh token

En tu computadora (no en el servidor), guarda este archivo como `obtener_token.py`:

```python
"""Genera el GOOGLE_REFRESH_TOKEN. Se corre una sola vez, en local."""
import urllib.parse, webbrowser, requests

CLIENT_ID     = input("GOOGLE_CLIENT_ID: ").strip()
CLIENT_SECRET = input("GOOGLE_CLIENT_SECRET: ").strip()

SCOPES = " ".join([
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/drive.file",
])
REDIRECT = "http://localhost"

url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT,
    "response_type": "code",
    "scope": SCOPES,
    "access_type": "offline",     # imprescindible: sin esto no hay refresh token
    "prompt": "consent",          # fuerza que lo devuelva aunque ya hayas dado permiso
})

print("\nAbriendo el navegador. Autoriza con designmodelingdg@gmail.com.\n")
webbrowser.open(url)
print("Si no se abre solo, entra a:\n" + url + "\n")
print("Vas a caer en una página de error 'No se puede acceder a este sitio'.")
print("ES NORMAL. Copia de la barra de direcciones el valor de code=...\n")

code = input("Pega aquí el code: ").strip()

r = requests.post("https://oauth2.googleapis.com/token", data={
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT,
    "grant_type": "authorization_code",
}, timeout=30)

if not r.ok:
    print("❌ Falló:", r.status_code, r.text)
else:
    tok = r.json().get("refresh_token")
    print("\n✅ GOOGLE_REFRESH_TOKEN =", tok if tok else
          "(vacío — vuelve a correrlo, el permiso ya estaba dado)")
```

Córrelo:

```bash
pip install requests
python obtener_token.py
```

> **La URL de `code=` viene con `%2F` y demás.** Copia el valor tal cual aparece
> entre `code=` y el siguiente `&`. Si te da error "invalid_grant", el código ya
> se usó o expiró (duran minutos): vuelve a correr el script.

**Borra `obtener_token.py` cuando termines.** No lo subas a ningún repo.

## 5. Carpeta de notas (opcional pero recomendado)

1. En Google Drive crea una carpeta llamada **Notas Asistente DMA**.
2. Ábrela y copia el id de la URL:
   `https://drive.google.com/drive/folders/`**`1a2B3c...`**
3. Ese id va en `GOOGLE_CARPETA_NOTAS`.

Sin esto las notas caen sueltas en la raíz de tu Drive y se mezclan con todo.

## 6. Token de ClickUp (para crear tareas al equipo)

Esto es rápido — 2 minutos:

1. Entra a [app.clickup.com](https://app.clickup.com) con tu cuenta.
2. Abajo a la izquierda, click en tu **avatar** → **Settings**.
3. En el menú lateral: **Apps**.
4. En *API Token* → **Generate** (o **Regenerate** si ya había uno).
5. Copia el token. Empieza por `pk_`.

Ese valor va en `CLICKUP_TOKEN`.

> Tu equipo y tus 12 listas ya están escritos dentro de `clickup_client.py`
> (los leí de tu workspace real). Si más adelante entra alguien nuevo o creas
> una lista, hay que agregarlo ahí — está todo junto al principio del archivo,
> comentado y fácil de editar.

## 7. Plantilla de WhatsApp (para que los recordatorios siempre lleguen)

**Este paso es opcional pero importante, y conviene entender por qué.**

WhatsApp solo permite mandarte un mensaje libre si tú escribiste en las últimas
**24 horas**. Fuera de esa ventana, Meta lo bloquea. Como tú vas a usar el
asistente a diario, casi siempre estará abierta — pero "casi siempre" no sirve
para un recordatorio de reunión.

La solución es una plantilla pre-aprobada, que sí puede entrar siempre:

1. Entra a [business.facebook.com](https://business.facebook.com) → tu cuenta.
2. Menú **WhatsApp Manager** → **Plantillas de mensajes** → **Crear plantilla**.
3. Configúrala así:
   - Categoría: **Utilidad**
   - Nombre: `recordatorio_dma`
   - Idioma: **Español**
   - Cuerpo del mensaje: `⏰ Recordatorio: {{1}}`
   - En el ejemplo de `{{1}}` escribe: `En 30 min: reunión con Patricio`
4. **Enviar** y esperar la aprobación de Meta (suele tardar de minutos a
   un par de horas; es categoría Utilidad, se aprueba casi siempre).
5. Cuando aparezca como **Aprobada**, pon `WA_TEMPLATE_RECORDATORIO=recordatorio_dma`.

Si te saltas este paso, todo funciona igual, pero un recordatorio puede no
llegar si llevas más de un día sin hablarle al bot.

## 8. Pegar todo en Render

> **El bot vive en Render, no en Railway.** Si abriste Railway y te salió
> «0 Projects», estaba bien: ahí no hay nada y no hay que crear nada. El repo
> tiene un `railway.toml` que nunca se llegó a usar, y por eso lo dije mal antes.
> El servicio real es `dma-sales-assistant` en Render.

1. Entra a [dashboard.render.com](https://dashboard.render.com).
2. Abre el servicio **`dma-sales-assistant`**.
3. En el menú de la izquierda: **Environment**.
4. **Add Environment Variable** por cada línea (o **Add from .env** para pegarlas todas de una):

```
MODEL_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
GOOGLE_CLIENT_ID=...apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-...
GOOGLE_REFRESH_TOKEN=1//0...
GOOGLE_CALENDAR_PRINCIPAL=designmodelingdg@gmail.com
GOOGLE_CARPETA_NOTAS=1a2B3c...
CLICKUP_TOKEN=pk_...
WA_TEMPLATE_RECORDATORIO=recordatorio_dma
ASISTENTE_MODEL=claude-sonnet-5
ASISTENTE_ACTIVO=1
```

Pulsa **Save Changes**. Render redespliega solo — tarda un par de minutos.

## 9. Comprobar

```bash
python -c "import google_client, clickup_client as c; \
print('Google:', google_client.credenciales_ok(), '| ClickUp:', c.credenciales_ok())"
```

Los dos en `True` → listo. Si alguno sale `False`, el log dice cuál variable falla.

---

## Si algo se rompe

| Síntoma | Causa casi siempre |
|---|---|
| `invalid_grant` al refrescar | El refresh token se revocó, o la app sigue en *Prueba* y pasaron 7 días → publica la app (paso 2) y regenera el token. |
| `insufficient authentication scopes` | Faltó un scope al autorizar. Regenera el token con los tres del script. |
| `403 Google Tasks API has not been used` | Falta habilitar la API del paso 1. |
| Las notas no aparecen en la carpeta | `GOOGLE_CARPETA_NOTAS` vacío o con el id mal copiado. |
| El asistente ve clases de Classroom | Se editó `CALENDARIOS_AGENDA` en `google_client.py`. Esa lista blanca existe justo para eso. |
| `Falta CLICKUP_TOKEN` | No se pegó el token del paso 6 en Render. |
| "No reconocí a X en el equipo" | Esa persona no está en `EQUIPO` (`clickup_client.py`). Lisette, por ejemplo, no está en ClickUp. |
| Un recordatorio no llegó | Pasaron >24 h sin que le escribieras al bot y no hay plantilla aprobada (paso 7). |
| `credit balance is too low` | La cuenta de Anthropic no tiene saldo. Recarga, o pon `MODEL_PROVIDER=openrouter` con su `OPENROUTER_API_KEY`. |
| El asistente conversa pero no agenda | El modelo no hace tool calling. Ajusta `OPENROUTER_MODEL_TOOLS` a uno que sí (por defecto `google/gemini-2.5-flash`). |
| Llegan recordatorios repetidos | El archivo de estado se borró (vive en `/tmp`, se pierde al redesplegar). Molesto, no grave. |
