"""
Marketing — la matriz de contenido y el retorno real, por nota de voz.

## El problema que resuelve

El asistente ya sabía responder por dinero (`ventas.py`) y por agenda, pero no
por CONTENIDO. Dayana no podía preguntarle "¿qué toca publicar?" ni "¿cuál de
mis reels funcionó mejor?" — y esas dos preguntas son las que se hace mientras
maneja, que es justo cuando le habla.

Todo ese análisis ya existe: vive en la matriz viral, 148 reels reales con su
eje, su estructura y sus métricas, más 44 piezas ya guionadas. El problema era
de acceso, no de datos.

## Por qué lee de una URL pública y no del repo

El asistente corre en Render. No tiene el repositorio, ni debe tenerlo: darle
un token de GitHub para leer contenido que ya es público sería añadir una
credencial a cambio de nada.

La Action `publish-matriz.yml` publica la matriz a GitHub Pages cada vez que
cambia. Es la MISMA fuente que ve Patricio, así que el asistente y el equipo
de contenido nunca pueden estar mirando versiones distintas.

    https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/

## Lo que este módulo NO hace

No inventa el hueco. Si Pages no responde o el JSON cambió de forma, lo dice y
devuelve lo que sí pudo leer. Una matriz con un hueco honesto vale más que un
número redondeado a ojo — es la regla de la que sale todo el sistema.

## Zona horaria y frescura

La matriz se refresca semanalmente, así que se cachea 30 minutos en memoria:
sin eso, cada nota de voz se bajaría 100 KB tres veces. Cada respuesta dice de
cuándo es el dato, para que "esta semana" no se confunda con "hace tres".
"""
from __future__ import annotations

import datetime
import json
import logging
import statistics
import time
import urllib.request

log = logging.getLogger("dma-asistente")

BASE = "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html"
TTL_CACHE = 30 * 60          # 30 min: la matriz se refresca una vez por semana
TIMEOUT = 20                 # Render corta a los 30s; 20 deja margen para responder

# WhatsApp corta cerca de los 4.096 caracteres. Cuando un guion no cabe, se
# recorta y SE DICE — un recorte silencioso se lee como "esto es todo".
TOPE_WHATSAPP = 3500

_cache: dict[str, tuple[float, dict]] = {}


# ── Lectura ───────────────────────────────────────────────────────────────────

def _bajar(archivo: str) -> dict | None:
    """Trae un JSON publicado. Devuelve None si no se puede — nunca revienta."""
    guardado = _cache.get(archivo)
    if guardado and (time.time() - guardado[0]) < TTL_CACHE:
        return guardado[1]
    try:
        req = urllib.request.Request(f"{BASE}/{archivo}",
                                     headers={"User-Agent": "dma-asistente/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            datos = json.load(resp)
        _cache[archivo] = (time.time(), datos)
        return datos
    except Exception as e:                       # noqa: BLE001 — cualquier fallo degrada igual
        log.warning(f"⚠️ No se pudo leer {archivo}: {e}")
        # Si hay copia vieja en caché, vale más que nada: se usa y se avisa.
        return guardado[1] if guardado else None


def _frescura(datos: dict) -> str:
    gen = datos.get("generado")
    if not gen:
        return ""
    try:
        dias = (datetime.date.today() - datetime.date.fromisoformat(gen)).days
    except ValueError:
        return f" (datos del {gen})"
    if dias <= 1:
        return " (datos de hoy)"
    if dias <= 9:
        return f" (datos de hace {dias} días)"
    return f" (⚠️ datos del {gen}, hace {dias} días)"


def _recortar(texto: str) -> str:
    if len(texto) <= TOPE_WHATSAPP:
        return texto
    return (texto[:TOPE_WHATSAPP].rsplit("\n", 1)[0]
            + "\n\n… _cortado aquí porque no cabe en WhatsApp. "
              "Pídeme la parte que te falte._")


# ── Diagnóstico de la cuenta ─────────────────────────────────────────────────

def diagnostico() -> str:
    """Cómo va el contenido: qué eje se lleva el alcance y cuál se lleva la venta.

    Es la pregunta de fondo de toda la matriz. La cuenta se viraliza con OBRA,
    que trae público que mira pero no compra; el núcleo BIM+IA, que es lo que
    se vende, casi no tiene alcance. Este resumen lo pone en números cada vez,
    en vez de repetir de memoria una cifra que quizá ya cambió.
    """
    m = _bajar("matriz.json")
    if not m or not m.get("reels"):
        return ("📊 No pude leer la matriz ahora mismo. Está publicada en "
                "GitHub Pages; si acaba de correr la Action, prueba en un rato.")

    reels = m["reels"]
    total_piezas = len(reels)
    total_views = sum(r.get("views") or 0 for r in reels)

    por_eje: dict[str, dict] = {}
    for r in reels:
        eje = r.get("eje") or "sin eje"
        d = por_eje.setdefault(eje, {"piezas": 0, "views": 0})
        d["piezas"] += 1
        d["views"] += r.get("views") or 0

    vistas = [r.get("views") or 0 for r in reels if r.get("views")]
    mediana = statistics.median(vistas) if vistas else 0

    lineas = [f"📊 *Matriz de contenido*{_frescura(m)}",
              f"{total_piezas} piezas · {total_views:,.0f} vistas · mediana {mediana:,.0f}\n"]

    for eje, d in sorted(por_eje.items(), key=lambda x: -x[1]["views"]):
        pp = 100 * d["piezas"] / total_piezas
        pv = 100 * d["views"] / total_views if total_views else 0
        lineas.append(f"• *{eje}* — {pp:.0f}% de las piezas, *{pv:.1f}% del alcance*")

    lineas.append("\n_El alcance que se lleva OBRA no compra: quien compra el "
                  "Máster es quien modela desde la computadora. El formato viral "
                  "funciona, el tema es el que hay que mover._")
    return _recortar("\n".join(lineas))


def mejores_piezas(cuantas: int = 5, eje: str = "") -> str:
    """Las piezas que más rindieron, con su hook — para saber qué repetir."""
    m = _bajar("matriz.json")
    if not m or not m.get("reels"):
        return "📊 No pude leer la matriz ahora mismo."

    reels = [r for r in m["reels"] if r.get("views")]
    if eje:
        buscado = eje.strip().upper()
        filtrados = [r for r in reels if buscado in (r.get("eje") or "").upper()]
        if not filtrados:
            ejes = sorted({r.get("eje") or "?" for r in reels})
            return f"No hay piezas del eje «{eje}». Los ejes son: {', '.join(ejes)}."
        reels = filtrados

    cuantas = max(1, min(int(cuantas or 5), 15))
    top = sorted(reels, key=lambda r: -(r.get("views") or 0))[:cuantas]

    titulo = f"🏆 *Mejores piezas*{' · ' + eje.upper() if eje else ''}{_frescura(m)}"
    lineas = [titulo, ""]
    for r in top:
        hook = (r.get("hook") or r.get("tema") or "sin hook registrado").strip()
        lineas.append(f"• *{r.get('views') or 0:,.0f}* vistas · {r.get('comentarios') or 0} coment. "
                      f"· {r.get('eje') or '?'}")
        lineas.append(f"  _{hook[:150]}_")
    return _recortar("\n".join(lineas))


# ── Guiones listos ───────────────────────────────────────────────────────────

def guiones(formato: str = "", eje: str = "") -> str:
    """Qué hay ya escrito y esperando publicación, filtrable por formato o eje."""
    g = _bajar("guiones-completos.json")
    if not g or not g.get("piezas"):
        return "📝 No pude leer los guiones ahora mismo."

    piezas = g["piezas"]
    if formato:
        f = formato.strip().lower().rstrip("es").rstrip("s")   # carruseles → carrusel
        piezas = [p for p in piezas if f in (p.get("formato") or "").lower()]
    if eje:
        b = eje.strip().upper()
        piezas = [p for p in piezas if b in (p.get("eje") or "").upper()]

    if not piezas:
        formatos = sorted({p.get("formato") or "?" for p in g["piezas"]})
        return (f"No hay guiones con ese filtro. Los formatos disponibles son: "
                f"{', '.join(formatos)}.")

    lineas = [f"📝 *Guiones listos* — {len(piezas)} de {g.get('total', len(g['piezas']))}"
              f"{_frescura(g)}", ""]
    for p in piezas[:20]:
        lineas.append(f"• `{p.get('id')}` — {p.get('titulo')}")
        lineas.append(f"  _{p.get('formato')} · {p.get('eje') or 's/e'}_")
    if len(piezas) > 20:
        lineas.append(f"\n… y {len(piezas) - 20} más. Filtra por formato para verlos.")
    lineas.append("\n_Pídeme uno por su id y te lo paso completo._")
    return _recortar("\n".join(lineas))


def guion(identificador: str) -> str:
    """Un guion completo: hook, slides, caption y la CTA de cada red."""
    g = _bajar("guiones-completos.json")
    if not g or not g.get("piezas"):
        return "📝 No pude leer los guiones ahora mismo."

    clave = (identificador or "").strip().lower()
    if not clave:
        return "Dime el id del guion, o pídeme la lista con guiones_disponibles."

    pieza = next((p for p in g["piezas"] if (p.get("id") or "").lower() == clave), None)
    if not pieza:      # por id exacto no está: se busca por parecido en el título
        pieza = next((p for p in g["piezas"]
                      if clave in (p.get("titulo") or "").lower()
                      or clave in (p.get("id") or "").lower()), None)
    if not pieza:
        return (f"No encontré un guion que se llame «{identificador}». "
                "Pídeme la lista y te digo los ids.")

    lineas = [f"📝 *{pieza.get('titulo')}*",
              f"_{pieza.get('formato')} · {pieza.get('red_principal') or 'multi'} "
              f"· eje {pieza.get('eje') or 's/e'}_\n"]

    if pieza.get("hook"):
        lineas.append(f"*Hook:* {pieza['hook']}\n")

    for i, s in enumerate(pieza.get("slides") or [], 1):
        texto = s if isinstance(s, str) else (s.get("texto") or json.dumps(s, ensure_ascii=False))
        lineas.append(f"{i}. {texto}")

    if pieza.get("caption"):
        lineas.append(f"\n*Caption:*\n{pieza['caption']}")

    ctas = pieza.get("cta_por_red") or {}
    if isinstance(ctas, dict) and ctas:
        lineas.append("\n*CTA por red:*")
        for red, cta in ctas.items():
            lineas.append(f"• {red}: {cta}")

    if pieza.get("historias"):
        lineas.append(f"\n_Trae {len(pieza['historias'])} historia(s) de apoyo. "
                      "Pídemelas aparte si las quieres._")

    return _recortar("\n".join(lineas))


# ── Retorno real ─────────────────────────────────────────────────────────────

def _gasto_meta(dias: int) -> float | None:
    """Gasto de pauta, si el módulo de Meta Ads lo expone como número.

    Se prueban varios nombres porque `meta_ads` vive en el otro repositorio y
    puede cambiar. Si ninguno existe, se devuelve None y el informe lo dice:
    NO se saca el número del texto de `resumen_campanas`, porque parsear plata
    de una cadena es exactamente como se reportan cifras equivocadas.
    """
    try:
        import meta_ads
    except Exception as e:                       # noqa: BLE001
        log.warning(f"⚠️ meta_ads no disponible: {e}")
        return None
    for nombre in ("gasto_total", "spend_total", "total_gastado", "gasto"):
        fn = getattr(meta_ads, nombre, None)
        if callable(fn):
            try:
                valor = fn(dias)
                if isinstance(valor, (int, float)):
                    return float(valor)
            except Exception as e:               # noqa: BLE001
                log.warning(f"⚠️ meta_ads.{nombre} falló: {e}")
    return None


def retorno_real(dias: int = 30) -> str:
    """Lo cobrado contra lo gastado en pauta. El número que no opina.

    El CRM dice lo que alguien MARCÓ ganado; Stripe dice lo que ENTRÓ. Cuando
    no coinciden, gana Stripe. Y las reservas de $100 del Máster son anticipo,
    no venta cerrada: van aparte siempre.
    """
    import ventas                                # se importa aquí: evita ciclo al cargar

    dias = max(1, min(int(dias or 30), 90))
    hasta = datetime.date.today() - datetime.timedelta(days=1)   # la ventana cierra AYER
    desde = hasta - datetime.timedelta(days=dias - 1)

    try:
        cobros = ventas.cobros_stripe(desde, hasta)
    except Exception as e:                       # noqa: BLE001
        log.warning(f"⚠️ Stripe falló: {e}")
        return "💰 No pude leer Stripe ahora mismo, así que no te doy un retorno a medias."

    total = sum(c["monto"] for c in cobros)
    reservas = [c for c in cobros if 90 <= c["monto"] <= 110]
    cerrado = total - sum(c["monto"] for c in reservas)

    lineas = [f"💰 *Retorno real* — {desde.strftime('%d/%m')} al {hasta.strftime('%d/%m')}",
              f"_La ventana cierra ayer: un día sin cerrar da cifras cortas._\n",
              f"💳 Cobrado en Stripe: *${total:,.2f}* en {len(cobros)} cobro(s)"]

    if reservas:
        lineas.append(f"   de los cuales ${sum(c['monto'] for c in reservas):,.2f} son "
                      f"{len(reservas)} reserva(s) de ~$100 — anticipo, no venta cerrada")
        lineas.append(f"   venta cerrada: *${cerrado:,.2f}*")

    gasto = _gasto_meta(dias)
    if gasto is None:
        lineas.append("\n📊 No pude leer el gasto de Meta Ads, así que no te calculo "
                      "el retorno. Lo de arriba sí es exacto.")
    elif gasto > 0:
        lineas.append(f"\n📊 Gasto en pauta: *${gasto:,.2f}*")
        lineas.append(f"🎯 Por cada dólar de pauta volvieron *${total / gasto:,.2f}*")
    else:
        lineas.append("\n📊 Meta Ads reporta $0 de gasto en la ventana.")

    lineas.append("\n_Stripe no ve transferencias ni efectivo: lo cobrado real puede "
                  "ser mayor. No se suma con el CRM — sería la misma venta dos veces._")
    return _recortar("\n".join(lineas))
