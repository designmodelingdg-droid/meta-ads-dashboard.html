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

# Prisma no lleva @@map en este esquema, asi que las tablas se llaman igual
# que los modelos — con mayusculas, y en Postgres eso obliga a comillas.
CONSULTAS = {}

CONSULTAS["campanas"] = """
SELECT coalesce(json_agg(f ORDER BY f.enviados DESC), '[]'::json) FROM (
  SELECT
    a.id,
    a.name                              AS nombre,
    a.keywords                          AS palabras,
    a."isActive"                        AS activa,
    a."matchAnyPost"                    AS cualquier_post,
    a."dmTriggerEnabled"                AS dispara_con_dm,
    a."requireFollow"                   AS exige_seguir,
    a."postUrl"                         AS post_url,
    a."createdAt"                       AS creada,
    ig.username                         AS cuenta,
    coalesce(d.enviados, 0)             AS enviados,
    coalesce(d.fallidos, 0)             AS fallidos,
    coalesce(d.saltados, 0)             AS saltados,
    coalesce(d.pendientes, 0)           AS pendientes,
    d.primer_envio,
    d.ultimo_envio,
    coalesce(c.clics, 0)                AS clics
  FROM "Automation" a
  JOIN "InstagramAccount" ig ON ig.id = a."instagramAccountId"
  LEFT JOIN (
    SELECT "automationId" AS aid,
      count(*) FILTER (WHERE status = 'SENT')                  AS enviados,
      count(*) FILTER (WHERE status = 'FAILED')                AS fallidos,
      count(*) FILTER (WHERE status::text LIKE 'SKIPPED%%')    AS saltados,
      count(*) FILTER (WHERE status = 'PENDING')               AS pendientes,
      min("dmSentAt")                                          AS primer_envio,
      max("dmSentAt")                                          AS ultimo_envio
    FROM "DmLog" GROUP BY "automationId"
  ) d ON d.aid = a.id
  LEFT JOIN (
    SELECT "automationId" AS aid, count(*) AS clics
    FROM "LinkClick" GROUP BY "automationId"
  ) c ON c.aid = a.id
) f;
"""

# Por que importa: una campana puede llevar varias palabras. Esta es la unica
# consulta que dice cual de ellas disparo de verdad — `matchedKeyword` es lo
# que el worker apunto al casar el comentario.
CONSULTAS["por_palabra"] = """
SELECT coalesce(json_agg(f ORDER BY f.enviados DESC), '[]'::json) FROM (
  SELECT
    upper(l."matchedKeyword")                        AS palabra,
    a.name                                           AS campana,
    a."isActive"                                     AS campana_activa,
    count(*) FILTER (WHERE l.status = 'SENT')        AS enviados,
    count(*) FILTER (WHERE l.status = 'FAILED')      AS fallidos,
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
    coalesce(l."errorMessage", '(sin mensaje)') AS motivo,
    count(*)                          AS veces,
    max(l."createdAt")                AS ultima_vez
  FROM "DmLog" l
  WHERE l.status <> 'SENT'
  GROUP BY l.status::text, coalesce(l."errorMessage", '(sin mensaje)')
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
  SELECT date_trunc('day', k."createdAt")::date AS fecha, count(*) AS clics
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
             "-c", sql % {"dias": dias}],
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


def cotejar_con_la_matriz(por_palabra, campanas):
    """Compara las seis palabras que la matriz declara contra lo que hay montado.

    Es el corazón del asunto: la matriz DICE que seis palabras están activas;
    OpenReply SABE cuáles lo están. Donde no coinciden es donde hay un CTA
    publicándose contra un disparador que no existe.
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

    filas = []
    for palabra in PALABRAS_MATRIZ:
        m = montadas.get(palabra)
        filas.append({
            "palabra": palabra,
            "montada_en_openreply": bool(m),
            "campana_activa": bool(m and m["activa"]),
            "campanas": (m or {}).get("campanas", []),
            "dms_enviados": envios.get(palabra, 0),
            "lectura": (
                "No existe ninguna campaña con esta palabra. Si hay un CTA "
                "pidiéndola, el comentario no recibe nada."
                if not m else
                "La campaña existe pero está PAUSADA: el comentario no dispara."
                if not m["activa"] else
                "Montada y activa, pero todavía no ha disparado ni una vez."
                if not envios.get(palabra) else
                f"Viva: {envios[palabra]} DM enviados."
            ),
        })

    # Y al revés: palabras montadas en OpenReply que la matriz no declara.
    extra = sorted(set(montadas) - set(PALABRAS_MATRIZ))
    return filas, extra


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
        "nota_clics": (
            "Los clics cuelgan de la CAMPAÑA y del ENLACE, no de la palabra: "
            "`LinkClick` no guarda cuál palabra disparó. En una campaña con "
            "varias palabras, el CTR no se puede repartir entre ellas y aquí "
            "no se inventa."),
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

    # El cruce con la matriz, que es para lo que existe todo lo de arriba.
    filas, extra = cotejar_con_la_matriz(
        salida.get("por_palabra") or [], salida.get("campanas") or [])
    salida["cotejo_con_la_matriz"] = filas
    salida["palabras_en_openreply_que_la_matriz_no_declara"] = extra

    vivas = [f["palabra"] for f in filas if f["dms_enviados"] > 0]
    mudas = [f["palabra"] for f in filas if not f["montada_en_openreply"]]

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / "campanas.json"
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=1, default=str),
                       encoding="utf-8")

    print(f"\nEscrito {destino}")
    print(f"  palabras de la matriz que han disparado: {len(vivas)}/6"
          + (f" — {', '.join(vivas)}" if vivas else ""))
    if mudas:
        print(f"  SIN CAMPAÑA EN OPENREPLY: {', '.join(mudas)}")
    if extra:
        print(f"  montadas pero fuera de la matriz: {', '.join(extra)}")
    if salida["fallos"]:
        print(f"  {len(salida['fallos'])} consulta(s) fallaron — quedan anotadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
