#!/usr/bin/env python3
"""Trae a la matriz lo que OpenReply sabe de las palabras clave.

Por que existe: la matriz lleva las seis palabras activas (ZAPATA, ACERO,
NIVEL, CHATGPT, MEMORIA, DYNAMO) como una CASILLA que alguien tiene que
acordarse de marcar — «montar el disparador CHATGPT en GHL» lleva semanas sin
marcar y nadie sabe si esta vivo. OpenReply es quien de verdad lo sabe: es el
que recibe el comentario, decide si casa con una palabra y manda el DM.

Con esto, «el disparador esta montado» deja de ser una casilla y pasa a ser un
hecho medido. Y de paso aparece lo que la casilla nunca iba a decir: cual de
las seis palabras convierte.

PRIVACIDAD — esto es deliberado y no se relaja:
  La tabla DmLog guarda `commenterName` y `commentText`, y InstagramAccount
  guarda `accessToken`. NADA de eso se lee aqui. Todas las consultas son
  agregados: cuentas, sumas y fechas. Ningun nombre, ningun texto de
  comentario, ningun token. Es el mismo criterio de `meta_pixel.py`, y la
  razon es la misma: un fichero de `fuentes/` acaba en un artefacto o en un
  PDF que se le pasa a alguien.

De donde sale el dato: la base de OpenReply (Postgres), en SOLO LECTURA.
La URL vive en el secreto del repositorio `OPENREPLY_DATABASE_URL` y no se
escribe nunca en el log ni en el JSON de salida.

Se consulta con `psql`, que ya viene en el runner de GitHub, para no meterle
una dependencia de pip a un repositorio donde todos los scripts son de
biblioteca estandar.

Uso:
    OPENREPLY_DATABASE_URL=postgresql://... python3 scripts/openreply.py
    OPENREPLY_DATABASE_URL=postgresql://... python3 scripts/openreply.py --dias 60
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

SALIDA = pathlib.Path("matriz-viral/fuentes/openreply")

# Las seis palabras que la matriz declara activas (regla del 11-sep). Se
# comparan contra lo que OpenReply tiene montado de verdad: esa diferencia es
# justo lo que este script existe para enseñar.
PALABRAS_MATRIZ = ["ZAPATA", "ACERO", "NIVEL", "CHATGPT", "MEMORIA", "DYNAMO"]

# EL CORTE DE LOS BOTS. Hasta el 14-sep inclusive los clics estan inflados por
# bots de vista previa; desde el 15 son personas. No es una deduccion de la
# forma de la serie: el filtro de rastreadores entro en produccion el 15-sep a
# las 00:10 UTC y Dayana lo verifico por via directa —una pagina de un commit
# POSTERIOR esta sirviendo, luego el filtro tambien—, con las pruebas del
# filtro en verde, incluida la que evita filtrar el navegador interno de
# Instagram, que es justo donde ocurre el clic bueno.
#
# Cualquier serie que cruce esta fecha mezcla dos cosas distintas, asi que se
# marca. Es la misma disciplina que `cotejo_fiable`.
CORTE_BOTS = "2026-09-15"

# Prisma no lleva @@map en este esquema, asi que las tablas se llaman igual
# que los modelos — con mayusculas, y en Postgres eso obliga a comillas.
CONSULTAS = {}

# OJO — el rol `matriz_ro` tiene permisos POR COLUMNA, no por tabla. Pedir una
# columna no concedida no devuelve nulo: tumba la consulta entera con
# «permission denied for table». Por eso aqui se nombra cada columna y no se
# usa `SELECT *` en ningun sitio.
#
# Falta a proposito la union con InstagramAccount: `Automation.instagramAccountId`
# no esta concedida, asi que no se puede decir a que cuenta pertenece cada
# campana. Se vive sin ello — hay una sola cuenta — y queda anotado en la salida.
# El rol `matriz_ro` tiene permisos POR COLUMNA. Pedir una no concedida no
# devuelve nulo: tumba la consulta entera. Por eso se nombra cada columna y no
# hay ningun `SELECT *`. La lista concedida vive en `prueba_openreply.py`, que
# comprueba estas consultas contra ella antes de que toquen produccion.
CONSULTAS["campanas"] = """
SELECT coalesce(json_agg(f ORDER BY f.enviados DESC), '[]'::json) FROM (
  SELECT
    a.id,
    a.name                              AS nombre,
    a.keywords                          AS palabras,
    a."matchAnyWord"                    AS casa_palabra_parcial,
    a."matchAnyPost"                    AS cualquier_post,
    a."dmTriggerEnabled"                AS dispara_con_dm,
    a."requireFollow"                   AS exige_seguir,
    a."isActive"                        AS activa,
    a."postId"                          AS post_id,
    a."postUrl"                         AS post_url,
    a."createdAt"                       AS creada,
    a."updatedAt"                       AS actualizada,
    ig.username                         AS cuenta,
    coalesce(d.enviados, 0)             AS enviados,
    coalesce(d.fallidos, 0)             AS fallidos,
    coalesce(d.entregados_sin_confirmar, 0) AS entregados_sin_confirmar,
    coalesce(d.saltados, 0)             AS saltados,
    coalesce(d.pendientes, 0)           AS pendientes,
    d.primer_envio,
    d.ultimo_envio,
    coalesce(c.clics, 0)                AS clics,
    coalesce(c.clics_limpios, 0)        AS clics_limpios,
    coalesce(c.clics_con_bots, 0)       AS clics_con_bots,
    coalesce(e.enlaces, 0)              AS enlaces_rastreados
  FROM "Automation" a
  JOIN "InstagramAccount" ig ON ig.id = a."instagramAccountId"
  LEFT JOIN (
    SELECT "automationId" AS aid,
      count(*) FILTER (WHERE status = 'SENT')                  AS enviados,
      -- Un FAILED con `dmDeliveryUnconfirmed` SI se entrego: Meta devolvio un
      -- error generico DESPUES de aceptar el envio. Contarlo como fallo es
      -- contar un DM que llego como si no hubiera llegado.
      count(*) FILTER (WHERE status = 'FAILED'
                       AND NOT "dmDeliveryUnconfirmed")        AS fallidos,
      count(*) FILTER (WHERE status = 'FAILED'
                       AND "dmDeliveryUnconfirmed")            AS entregados_sin_confirmar,
      count(*) FILTER (WHERE status::text LIKE 'SKIPPED%%')    AS saltados,
      count(*) FILTER (WHERE status = 'PENDING')               AS pendientes,
      min("dmSentAt")                                          AS primer_envio,
      max("dmSentAt")                                          AS ultimo_envio
    FROM "DmLog" GROUP BY "automationId"
  ) d ON d.aid = a.id
  LEFT JOIN (
    SELECT "automationId" AS aid,
      count(*)                                                   AS clics,
      count(*) FILTER (WHERE "createdAt" >= DATE '%(corte)s')     AS clics_limpios,
      count(*) FILTER (WHERE "createdAt" <  DATE '%(corte)s')     AS clics_con_bots
    FROM "LinkClick" GROUP BY "automationId"
  ) c ON c.aid = a.id
  LEFT JOIN (
    SELECT "automationId" AS aid, count(*) AS enlaces
    FROM "TrackedLink" GROUP BY "automationId"
  ) e ON e.aid = a.id
) f;
"""

CONSULTAS["por_palabra"] = """
SELECT coalesce(json_agg(f ORDER BY f.enviados DESC), '[]'::json) FROM (
  SELECT
    upper(l."matchedKeyword")                        AS palabra,
    a.name                                           AS campana,
    a."isActive"                                     AS campana_activa,
    count(*) FILTER (WHERE l.status = 'SENT')        AS enviados,
    count(*) FILTER (WHERE l.status = 'FAILED'
                     AND NOT l."dmDeliveryUnconfirmed")  AS fallidos,
    count(*) FILTER (WHERE l.status = 'FAILED'
                     AND l."dmDeliveryUnconfirmed")      AS entregados_sin_confirmar,
    count(*) FILTER (WHERE l.status::text LIKE 'SKIPPED%%') AS saltados,
    min(l."dmSentAt")                                AS primer_envio,
    max(l."dmSentAt")                                AS ultimo_envio
  FROM "DmLog" l
  JOIN "Automation" a ON a.id = l."automationId"
  WHERE l."matchedKeyword" IS NOT NULL
  GROUP BY upper(l."matchedKeyword"), a.name, a."isActive"
) f;
"""

# Los motivos de fallo, agrupados. Sin el texto del comentario: solo el mensaje
# de error que devolvio Meta, que es lo que dice si hay algo que arreglar.
CONSULTAS["motivos_de_fallo"] = """
SELECT coalesce(json_agg(f ORDER BY f.veces DESC), '[]'::json) FROM (
  SELECT
    l.status::text                    AS estado,
    l."dmDeliveryUnconfirmed"         AS pero_si_se_entrego,
    coalesce(l."errorMessage", '(sin mensaje)') AS motivo,
    count(*)                          AS veces,
    max(l."createdAt")                AS ultima_vez
  FROM "DmLog" l
  WHERE l.status <> 'SENT'
  GROUP BY l.status::text, l."dmDeliveryUnconfirmed",
           coalesce(l."errorMessage", '(sin mensaje)')
  LIMIT 50
) f;
"""

CONSULTAS["enlaces"] = """
SELECT coalesce(json_agg(f ORDER BY f.clics DESC), '[]'::json) FROM (
  SELECT
    t.slug,
    t.label                    AS etiqueta,
    t."destinationUrl"         AS destino,
    a.name                     AS campana,
    count(k.id)                AS clics,
    count(k.id) FILTER (WHERE k."createdAt" >= DATE '%(corte)s') AS clics_limpios,
    count(k.id) FILTER (WHERE k."createdAt" <  DATE '%(corte)s') AS clics_con_bots,
    min(k."createdAt")         AS primer_clic,
    max(k."createdAt")         AS ultimo_clic
  FROM "TrackedLink" t
  JOIN "Automation" a ON a.id = t."automationId"
  LEFT JOIN "LinkClick" k ON k."trackedLinkId" = t.id
  GROUP BY t.slug, t.label, t."destinationUrl", a.name
) f;
"""

CONSULTAS["clics_por_dia"] = """
SELECT coalesce(json_agg(f ORDER BY f.fecha), '[]'::json) FROM (
  SELECT date_trunc('day', k."createdAt")::date AS fecha, count(*) AS clics,
         (date_trunc('day', k."createdAt")::date >= DATE '%(corte)s') AS limpio
  FROM "LinkClick" k
  WHERE k."createdAt" >= now() - interval '%(dias)s days'
  GROUP BY 1
) f;
"""

CONSULTAS["envios_por_dia"] = """
SELECT coalesce(json_agg(f ORDER BY f.fecha), '[]'::json) FROM (
  SELECT date_trunc('day', l."dmSentAt")::date AS fecha, count(*) AS enviados
  FROM "DmLog" l
  WHERE l.status = 'SENT' AND l."dmSentAt" >= now() - interval '%(dias)s days'
  GROUP BY 1
) f;
"""

CONSULTAS["seguidores"] = """
SELECT coalesce(json_agg(f ORDER BY f.fecha), '[]'::json) FROM (
  SELECT ig.username AS cuenta, s.date AS fecha, s."followersCount" AS seguidores
  FROM "FollowerSnapshot" s
  JOIN "InstagramAccount" ig ON ig.id = s."instagramAccountId"
  WHERE s.date >= (current_date - interval '%(dias)s days')
) f;
"""


def consultar(url, sql, dias):
    """Una consulta por psql. Devuelve (datos, error_legible)."""
    entorno = dict(os.environ, PGCONNECT_TIMEOUT="20")
    try:
        r = subprocess.run(
            ["psql", url, "-X", "-q", "-t", "-A", "-v", "ON_ERROR_STOP=1",
             "-c", sql % {"dias": dias, "corte": CORTE_BOTS}],
            capture_output=True, text=True, timeout=120, env=entorno)
    except FileNotFoundError:
        return None, "No hay `psql` en este entorno."
    except subprocess.TimeoutExpired:
        return None, "La consulta pasó de 120 s."

    if r.returncode != 0:
        # La URL lleva la contraseña dentro: nunca se escribe el error crudo
        # sin limpiarlo antes.
        return None, limpiar(r.stderr.strip()[:400], url)
    salida = r.stdout.strip()
    if not salida:
        return [], None
    try:
        return json.loads(salida), None
    except json.JSONDecodeError as e:
        return None, f"Respuesta no era JSON: {e}"


def limpiar(texto, url):
    """Quita de un mensaje cualquier rastro de la cadena de conexión."""
    if url and url in texto:
        texto = texto.replace(url, "<URL OCULTA>")
    # Y por si psql la reescribe: cualquier cosa con esquema://usuario:clave@
    return re.sub(r"\w+://[^\s@]+@", "<URL OCULTA>@", texto)


def leer_los_clics(campanas):
    """Distingue «nadie hizo clic» de «esto no mide clics» — y no llama CTR a
    algo que no lo es.

    Dos trampas, las dos comprobadas contra el código de OpenReply:

    1. **El cero del medidor.** OpenReply solo crea un TrackedLink si la
       campaña se montó con un enlace rastreado — es opcional. Una campaña que
       manda el enlace crudo devuelve cero clics para siempre, y ese cero se
       lee igual que «el recurso no interesa a nadie». Es el mismo error que la
       CAPI del 14-sep: un cero del medidor leído como del mundo.

    2. **Clics no son personas.** `LinkClick` apunta cada apertura del
       redirector, no cada persona: la misma persona que abre el enlace tres
       veces cuenta tres, y los bots de vista previa de Instagram y WhatsApp
       también cuentan. Por eso los clics PUEDEN superar a los envíos, y
       `clics / enviados` no es un porcentaje de conversión.

       OpenReply resuelve eso capando el número al 100 %
       (`lib/tracking/analytics.ts`), y eso tira justo la señal: 1.200 clics
       sobre 60 envíos y 60 sobre 60 se muestran los dos como «100 %». Aquí no
       se capa. Cuando hay más clics que envíos se dice cuántos por envío y se
       dice por qué, y **no se llama CTR**.

    No se pueden contar clics ÚNICOS: haría falta `LinkClick.ipHash`, que está
    deliberadamente fuera del rol de solo lectura por ser un dato de persona.
    """
    for c in campanas:
        enlaces = int(c.get("enlaces_rastreados") or 0)
        enviados = int(c.get("enviados") or 0)
        clics = int(c.get("clics") or 0)

        if not enlaces:
            c["mide_clics"] = False
            c["ctr"] = None
            c["clics_por_dm"] = None
            c["lectura_clics"] = (
                "SIN ENLACE RASTREADO: esta campaña no mide clics. El cero es "
                "del medidor, no del público. Para medirla hay que montarle un "
                "enlace rastreado en OpenReply.")
            continue

        c["mide_clics"] = True
        limpios = int(c.get("clics_limpios") or 0)
        con_bots = int(c.get("clics_con_bots") or 0)

        if not enviados:
            c["ctr"] = None
            c["clics_por_dm"] = None
            c["lectura_clics"] = (
                f"{limpios} clics limpios, pero esta campaña no ha enviado "
                "ningún DM: esos clics vienen del enlace abierto por otra vía."
                if limpios else
                "Mide clics, pero todavía no ha enviado ningún DM.")
            continue

        # A partir de aqui SOLO se razona con los limpios. Los de antes del
        # corte se conservan en el JSON, pero no entran en ninguna tasa: son
        # bots de vista previa y meterlos en un CTR es inventarse el dato.
        por_dm = round(limpios / enviados, 2)
        c["clics_por_dm"] = por_dm

        aviso = (f" ({con_bots} clics más son anteriores al {CORTE_BOTS} y NO "
                 "se cuentan: eran bots de vista previa.)") if con_bots else ""

        if limpios > enviados:
            c["ctr"] = None
            c["lectura_clics"] = (
                f"{limpios} clics limpios sobre {enviados} DM enviados — "
                f"{por_dm} clics por DM. Al haber MÁS clics que envíos esto NO "
                "es un porcentaje de conversión: son aperturas repetidas de la "
                "misma persona o el enlace circulando fuera del DM." + aviso)
        else:
            c["ctr"] = round(limpios / enviados, 4)
            c["lectura_clics"] = (
                f"{limpios} clics limpios sobre {enviados} DM enviados "
                f"({limpios / enviados:.0%}). Son aperturas, no personas: la "
                "misma persona puede contar varias veces." + aviso)
    return campanas


def cotejar_con_la_matriz(por_palabra, campanas, hubo_fallo):
    """Compara lo que la matriz DECLARA contra lo que OpenReply tiene montado.

    `hubo_fallo` no es un adorno. Si la consulta de campañas murió, esta
    función no sabe nada — y decir «ZAPATA no existe» cuando en realidad no se
    pudo mirar es peor que no decir nada: se lee como un hecho comprobado. La
    primera prueba con permisos reales hizo exactamente eso, y por eso está
    aquí este parámetro.

    Devuelve además TODAS las palabras montadas con sus números, no solo las
    seis de la matriz. Lo que ya está funcionando importa más que lo que se
    buscaba: si en producción viven GUIA y TUTORIAL con miles de clics, mirar
    solo las seis declaradas es perderse lo único que está midiendo.
    """
    montadas = {}
    for c in campanas:
        for p in (c.get("palabras") or []):
            k = str(p).strip().upper()
            if not k:
                continue
            m = montadas.setdefault(k, {"campanas": [], "activa": False})
            m["campanas"].append(c.get("nombre"))
            if c.get("activa"):
                m["activa"] = True

    envios = {}
    for f in por_palabra:
        k = (f.get("palabra") or "").upper()
        envios[k] = envios.get(k, 0) + int(f.get("enviados") or 0)

    def lectura(palabra, m):
        if hubo_fallo:
            return ("NO SE PUDO COMPROBAR: la consulta de campañas falló. "
                    "Esto NO significa que la palabra no exista.")
        if not m:
            # OJO: esto NO significa que el comentario se quede sin respuesta.
            # Los disparadores de la matriz se montan en GoHighLevel, que es
            # otro sistema; OpenReply no sabe nada de el. Decir «no recibe
            # nada» seria afirmar sobre un sistema que no se esta mirando.
            return ("No existe en OpenReply. OJO: los disparadores de la matriz "
                    "se montan en GoHighLevel, que este conector NO ve — así "
                    "que esto no prueba que el comentario se quede sin "
                    "respuesta. Hay que comprobarlo en GHL.")
        if not m["activa"]:
            return "La campaña existe pero está PAUSADA: el comentario no dispara."
        if not envios.get(palabra):
            return "Montada y activa, pero todavía no ha disparado ni una vez."
        return f"Viva: {envios[palabra]} DM enviados."

    def fila(palabra, m, declarada):
        return {
            "palabra": palabra,
            "la_declara_la_matriz": declarada,
            "montada_en_openreply": None if hubo_fallo else bool(m),
            "campana_activa": None if hubo_fallo else bool(m and m["activa"]),
            "campanas": (m or {}).get("campanas", []),
            "dms_enviados": envios.get(palabra, 0),
            "lectura": lectura(palabra, m),
        }

    # las seis que la matriz declara
    filas = [fila(p, montadas.get(p), True) for p in PALABRAS_MATRIZ]

    # y TODAS las demás que estén montadas, con sus números
    # Las que viven en OpenReply y la matriz no declara. Importan mas que las
    # seis buscadas: son las que estan midiendo de verdad.
    otras = [fila(k, montadas[k], False)
             for k in sorted(set(montadas) - set(PALABRAS_MATRIZ))]

    return filas, otras


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=30,
                    help="ventana de las series por día (por defecto 30)")
    args = ap.parse_args()

    url = os.environ.get("OPENREPLY_DATABASE_URL", "").strip()
    if not url:
        print("::error::Falta OPENREPLY_DATABASE_URL. Este script corre dentro "
              "del Action, que es donde vive el secreto. Debe ser un usuario de "
              "Postgres con permiso SOLO DE LECTURA.", file=sys.stderr)
        return 1

    hoy = datetime.date.today()
    salida = {
        "generado": hoy.isoformat(),
        "ventana_series_dias": args.dias,
        "fuente": "OpenReply — base propia (Postgres), solo lectura",
        "nota_privacidad": (
            "Solo agregados. No se lee `commenterName`, ni `commentText`, ni "
            "`accessToken`. Ningún dato personal sale de la base."),
        "corte_de_bots": CORTE_BOTS,
        "nota_corte_de_bots": (
            f"Hasta el 14-sep inclusive los clics están INFLADOS por bots de "
            f"vista previa. Desde el {CORTE_BOTS} son personas: ese día entró "
            "en producción el filtro de rastreadores (verificado por vía "
            "directa, no por la forma de la serie). Todas las tasas de este "
            "fichero usan SOLO los clics limpios; los anteriores se conservan "
            "en `clics_con_bots` para no perderlos, pero no entran en ningún "
            "cálculo."),
        "nota_octubre_va_a_parecer_peor": (
            "AVISO PARA CUANDO SE COMPARE MES CONTRA MES. Desde el 15-sep, en "
            "las campañas con follow gate el DM ya no lleva el enlace del "
            "recurso: lleva el de una página de verificación que detecta al "
            "rastreador y no cuenta nada. Esos clics son doblemente limpios. "
            "Consecuencia: los números de octubre van a ser MUCHO más bajos "
            "que los de septiembre, y eso es CORRECTO. Comparar «1.825 en "
            "septiembre» contra «20 en octubre» y leer un desplome es el "
            "error: en septiembre se estaban contando bots."),
        "nota_fallos": (
            "Un `status = FAILED` con `dmDeliveryUnconfirmed` SÍ se entregó — "
            "Meta devolvió un error genérico después de aceptar el envío. Esos "
            "no se cuentan en `fallidos`, van aparte en "
            "`entregados_sin_confirmar`. Contarlos como fallo es contar como "
            "perdido un DM que llegó."),
        "nota_alcance": (
            "Esto solo ve OpenReply. Los disparadores de palabra de la matriz "
            "se montan en GoHighLevel, que es otro sistema y no se consulta "
            "aquí. Que una palabra no aparezca NO prueba que el comentario se "
            "quede sin respuesta."),
        "nota_cuenta": (
            "No se dice a qué cuenta de Instagram pertenece cada campaña: "
            "`Automation.instagramAccountId` no está concedida al rol de solo "
            "lectura. Con una sola cuenta no hace falta; si algún día hay "
            "varias, hay que conceder esa columna."),
        "nota_dms_por_palabra": (
            "Los DM SÍ se cuentan por palabra: `DmLog.matchedKeyword` guarda "
            "cuál disparó cada envío. Ver el bloque `por_palabra`."),
        "nota_clics": (
            "Los clics cuelgan de la CAMPAÑA y del ENLACE, no de la palabra: "
            "`LinkClick` no guarda cuál palabra disparó. En una campaña con "
            "varias palabras no se pueden repartir entre ellas, y aquí no se "
            "inventa. Además son APERTURAS, no personas: la misma persona "
            "cuenta varias veces y los bots de vista previa también, así que "
            "los clics pueden superar a los envíos. Cuando eso pasa, `ctr` "
            "queda en nulo y se usa `clics_por_dm`."),
        "fallos": [],
    }

    for nombre, sql in CONSULTAS.items():
        datos, err = consultar(url, sql, args.dias)
        if err:
            salida["fallos"].append({"consulta": nombre, "detalle": err})
            salida[nombre] = []
            print(f"  {nombre:18} FALLO — {err[:80]}", file=sys.stderr)
            continue
        salida[nombre] = datos
        print(f"  {nombre:18} ok ({len(datos)} filas)")

    # Un cero de clics puede ser del medidor. Se marca antes de nada.
    salida["campanas"] = leer_los_clics(salida.get("campanas") or [])

    # El cruce con la matriz, que es para lo que existe todo lo de arriba.
    # Si la consulta de campañas murió, el cruce no puede afirmar nada.
    fallo_campanas = any(f["consulta"] == "campanas" for f in salida["fallos"])
    filas, otras = cotejar_con_la_matriz(
        salida.get("por_palabra") or [], salida.get("campanas") or [],
        fallo_campanas)
    salida["cotejo_con_la_matriz"] = filas
    salida["otras_palabras_montadas"] = otras
    salida["cotejo_fiable"] = not fallo_campanas

    vivas = [f["palabra"] for f in filas if f["dms_enviados"] > 0]
    mudas = [f["palabra"] for f in filas if not f["montada_en_openreply"]]

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / "campanas.json"
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=1, default=str),
                       encoding="utf-8")

    print(f"\nEscrito {destino}")

    if fallo_campanas:
        print("  ⚠ LA CONSULTA DE CAMPAÑAS FALLÓ: el cruce de palabras no vale. "
              "No se puede decir qué está montado y qué no.")
    else:
        # Primero lo que esta VIVO, sea o no de las seis declaradas.
        vivas = sorted(
            [(f["palabra"], f["dms_enviados"]) for f in filas + otras
             if f["dms_enviados"] > 0], key=lambda x: -x[1])
        if vivas:
            print("  palabras que están disparando: "
                  + ", ".join(f"{p} ({n})" for p, n in vivas))
        else:
            print("  ninguna palabra ha disparado todavía.")

        mudas = [f["palabra"] for f in filas if not f["montada_en_openreply"]]
        if mudas:
            print(f"  de las 6 que declara la matriz, SIN CAMPAÑA: {', '.join(mudas)}")
        if otras:
            print("  montadas y fuera de la matriz: "
                  + ", ".join(f["palabra"] for f in otras))

    sin_medir = [c["nombre"] for c in salida.get("campanas") or []
                 if not c.get("mide_clics")]
    if sin_medir:
        print(f"  SIN ENLACE RASTREADO (su 0 de clics no significa nada): "
              f"{', '.join(sin_medir)}")
    if salida["fallos"]:
        print(f"  {len(salida['fallos'])} consulta(s) fallaron — quedan anotadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
