#!/usr/bin/env python3
"""Prueba de `openreply.py` SIN base de datos y SIN red.

Dos cosas que hay que poder comprobar en cada corrida, antes de tocar la base
de producción:

1. QUE NINGUNA CONSULTA LEA DATOS PERSONALES NI TOKENS.
   Es una comprobación estática sobre el texto de las consultas. Existe porque
   el riesgo no es el script de hoy: es el `SELECT` que alguien añada dentro de
   seis meses para «ver quién comentó». La tabla DmLog tiene el nombre y el
   texto del comentario a un JOIN de distancia, y `fuentes/` acaba dentro de un
   artefacto que se comparte.

2. QUE EL CRUCE CON LA MATRIZ DIGA LA VERDAD EN LOS CASOS RAROS.
   Una palabra puede estar sin montar, montada y pausada, montada y activa pero
   sin disparar nunca, o viva. Los cuatro casos se leen distinto y los cuatro
   importan: el segundo y el tercero son los que hoy la matriz no distingue.

Se corre como primer paso del Action, antes que `openreply.py`.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import openreply as orep  # noqa: E402  (se importa por el módulo, no se ejecuta)

# Columnas que NUNCA deben aparecer en una consulta. La lista sale del propio
# esquema de OpenReply: son las que llevan datos de una persona o una llave.
PROHIBIDAS = [
    '"commenterName"', '"commentText"', '"commenterId"', '"commentId"',
    '"accessToken"', '"ipHash"', '"userAgent"', '"referrer"',
    '"zernioAccountId"',
]

fallos = []


def comprobar(nombre, condicion, detalle=""):
    print(f"  {'ok  ' if condicion else 'FALLA'} {nombre}"
          + (f" — {detalle}" if detalle and not condicion else ""))
    if not condicion:
        fallos.append(nombre)


# Lo que el rol `matriz_ro` puede leer de verdad, columna por columna, tal como
# lo concedió Dayana el 16-sep. Los permisos son POR COLUMNA: pedir una que no
# esté aquí no devuelve nulo, TUMBA la consulta entera con «permission denied
# for table». La primera prueba con permisos reales se llevó por delante la
# consulta de campañas por tres columnas de más y un JOIN.
CONCEDIDO = {
    "Automation": "id name keywords matchAnyWord isActive postId postUrl "
                  "createdAt updatedAt",
    "DmLog": "id automationId matchedKeyword status attempts dmSentAt "
             "errorMessage publicReplySentAt createdAt",
    "TrackedLink": "id automationId slug label destinationUrl createdAt",
    "LinkClick": "id automationId trackedLinkId createdAt",
    "FollowerSnapshot": "id instagramAccountId date followersCount backfilled "
                        "createdAt",
    "InstagramAccount": "id username",
}
CONCEDIDO = {tabla: set(cols.split()) for tabla, cols in CONCEDIDO.items()}

# Con qué alias se nombra cada tabla dentro de las consultas.
ALIAS = {"a": "Automation", "l": "DmLog", "t": "TrackedLink",
         "k": "LinkClick", "s": "FollowerSnapshot", "ig": "InstagramAccount"}

# Tablas que el rol no puede tocar EN ABSOLUTO.
VETADAS = ["FollowGate", "Workspace", "User", "Account", "Session",
           "ZernioConnection", "WebhookEvent", "ProcessedComment"]


print("0 · Las consultas solo piden columnas concedidas")
import re
for nombre, sql in orep.CONSULTAS.items():
    pedidas = [(ALIAS[al], col) for al, col in re.findall(r'\b(\w+)\."(\w+)"', sql)
               if al in ALIAS]
    malas = [f"{tb}.{c}" for tb, c in pedidas if c not in CONCEDIDO[tb]]
    comprobar(f"consulta «{nombre}» — columnas", not malas,
              f"pide {', '.join(sorted(set(malas)))}")

for nombre, sql in orep.CONSULTAS.items():
    tocadas = [tb for tb in VETADAS if f'"{tb}"' in sql]
    comprobar(f"consulta «{nombre}» — tablas vetadas", not tocadas,
              f"toca {', '.join(tocadas)}")

comprobar("ninguna consulta usa SELECT *",
          not any(re.search(r"SELECT\s+\*", sql, re.I) for sql in orep.CONSULTAS.values()),
          "con permisos por columna, SELECT * siempre falla")

print("\n1 · Ninguna consulta lee datos personales ni llaves")

for nombre, sql in orep.CONSULTAS.items():
    malas = [c for c in PROHIBIDAS if c in sql]
    comprobar(f"consulta «{nombre}»", not malas, f"lee {', '.join(malas)}")

print("\n2 · El cruce con la matriz distingue los cuatro casos")

campanas = [
    {"nombre": "Zapatas", "palabras": ["ZAPATA"], "activa": True},
    {"nombre": "Revit + ChatGPT", "palabras": ["CHATGPT"], "activa": False},
    {"nombre": "Test de Nivel", "palabras": ["NIVEL"], "activa": True},
    {"nombre": "Bot Master", "palabras": ["BIM", "IA"], "activa": True},
]
por_palabra = [{"palabra": "ZAPATA", "enviados": 40}]

filas, otras = orep.cotejar_con_la_matriz(por_palabra, campanas, False)
por = {f["palabra"]: f for f in filas}

comprobar("viva: ZAPATA tiene envíos",
          por["ZAPATA"]["dms_enviados"] == 40 and por["ZAPATA"]["campana_activa"])
comprobar("pausada: CHATGPT está montada pero su campaña no está activa",
          por["CHATGPT"]["montada_en_openreply"]
          and not por["CHATGPT"]["campana_activa"]
          and "PAUSADA" in por["CHATGPT"]["lectura"])
comprobar("muda: NIVEL está activa pero nunca disparó",
          por["NIVEL"]["campana_activa"] and por["NIVEL"]["dms_enviados"] == 0
          and "todavía no ha disparado" in por["NIVEL"]["lectura"])
comprobar("ausente: MEMORIA no existe en ninguna campaña",
          not por["MEMORIA"]["montada_en_openreply"]
          and "no recibe nada" in por["MEMORIA"]["lectura"])
comprobar("se listan las seis palabras de la matriz", len(filas) == 6)
comprobar("las de OpenReply que la matriz no declara salen aparte CON sus números",
          [f["palabra"] for f in otras] == ["BIM", "IA"]
          and all("dms_enviados" in f for f in otras),
          f"salió {[f['palabra'] for f in otras]}")

# El fallo que casi se va a produccion: la consulta muere y el cruce sigue
# afirmando que las palabras no existen.
rotas, _ = orep.cotejar_con_la_matriz([], [], True)
comprobar("si la consulta de campañas falla, el cruce NO afirma nada",
          all(f["montada_en_openreply"] is None for f in rotas)
          and all("NO SE PUDO COMPROBAR" in f["lectura"] for f in rotas),
          "un fallo de permisos se leía como «la palabra no existe»")

print("\n3 · Un cero de clics no siempre significa lo mismo")

camps = orep.leer_los_clics([
    {"nombre": "Con enlace", "enlaces_rastreados": 1, "enviados": 40, "clics": 17},
    {"nombre": "Sin enlace", "enlaces_rastreados": 0, "enviados": 30, "clics": 0},
    {"nombre": "Mide pero no ha enviado", "enlaces_rastreados": 1,
     "enviados": 0, "clics": 0},
])
con, sin, mudo = camps

comprobar("la que mide da CTR", con["mide_clics"] and con["ctr"] == 0.425)
comprobar("la que NO mide deja el CTR en nulo, no en cero",
          sin["mide_clics"] is False and sin["ctr"] is None,
          "un 0.0 se promedia y se grafica; un nulo no")
comprobar("y lo dice con todas las letras",
          "SIN ENLACE RASTREADO" in sin["lectura_clics"]
          and "del medidor" in sin["lectura_clics"])
comprobar("30 enviados con 0 clics sin enlace NO se lee como fracaso",
          "no mide clics" in sin["lectura_clics"])
comprobar("la que mide pero no ha enviado no divide por cero",
          mudo["ctr"] is None and "no ha enviado" in mudo["lectura_clics"])

# La forma que tienen los datos REALES de produccion: decenas de envios y
# miles de clics. OpenReply capa eso al 100 %; aqui se dice lo que es.
mas = orep.leer_los_clics([{"nombre": "GUIA", "enlaces_rastreados": 1,
                           "enviados": 60, "clics": 1200}])[0]
comprobar("más clics que envíos NO se presenta como un 2000 % ni como 100 %",
          mas["ctr"] is None and mas["clics_por_dm"] == 20.0,
          f"ctr={mas['ctr']} clics_por_dm={mas['clics_por_dm']}")
comprobar("y explica por qué no es una tasa",
          "NO es un porcentaje de conversión" in mas["lectura_clics"]
          and "bots" in mas["lectura_clics"])
comprobar("con clics pero cero envíos tampoco revienta",
          orep.leer_los_clics([{"nombre": "x", "enlaces_rastreados": 1,
                                "enviados": 0, "clics": 9}])[0]["ctr"] is None)

print("\n4 · Detalles que ya han mordido")
comprobar("las palabras se comparan en mayúsculas",
          orep.cotejar_con_la_matriz(
              [{"palabra": "ZAPATA", "enviados": 3}],
              [{"nombre": "x", "palabras": ["zapata"], "activa": True}], False
          )[0][0]["montada_en_openreply"],
          "una campaña con la palabra en minúsculas debe contar igual")

comprobar("una URL con contraseña nunca se escribe en un error",
          "<URL OCULTA>" in orep.limpiar(
              "error en postgresql://usuario:clave@host:5432/db al conectar",
              "postgresql://usuario:clave@host:5432/db")
          and "clave" not in orep.limpiar(
              "error en postgresql://usuario:clave@host:5432/db al conectar",
              "postgresql://usuario:clave@host:5432/db"))

comprobar("también se oculta una URL que el script no conocía",
          "clave" not in orep.limpiar("falló postgres://otro:clave@h/d", ""))

print()
if fallos:
    print(f"::error::{len(fallos)} comprobación(es) fallaron: {', '.join(fallos)}")
    raise SystemExit(1)
print("Todo en orden.")
