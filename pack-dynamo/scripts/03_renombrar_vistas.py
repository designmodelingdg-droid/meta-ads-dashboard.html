# -*- coding: utf-8 -*-
"""
03 · RENOMBRAR VISTAS EN LOTE

Qué hace
    Busca y reemplaza texto en el nombre de muchas vistas de golpe, y
    opcionalmente añade un prefijo.

Entradas (Dynamo)
    IN[0]  lista de vistas
    IN[1]  texto a buscar   ("" para no buscar nada)
    IN[2]  texto a poner
    IN[3]  prefijo a añadir ("" para ninguno)
    IN[4]  SIMULACRO: True = solo enseña qué haría, NO toca nada
                      False = renombra de verdad

⚠️ ESTE SCRIPT SÍ MODIFICA EL MODELO cuando IN[4] es False.

    Corre SIEMPRE primero con IN[4] = True y lee la lista. Renombrar 200 vistas
    mal no se deshace cómodamente, y los nombres de vista salen impresos en los
    cajetines de los planos.

Salida
    En simulacro: la tabla de «antes -> después».
    En real: cuántas se renombraron, y cuáles fallaron y por qué.
"""
import clr

clr.AddReference('RevitAPI')

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

vistas    = IN[0] if isinstance(IN[0], list) else [IN[0]]
buscar    = IN[1] or ''
poner     = IN[2] or ''
prefijo   = IN[3] if len(IN) > 3 and IN[3] else ''
simulacro = IN[4] if len(IN) > 4 else True     # por defecto NO toca nada


def desenvolver(x):
    return x.InternalElement if hasattr(x, 'InternalElement') else x


def nombre_nuevo(actual):
    n = actual
    if buscar:
        n = n.replace(buscar, poner)
    if prefijo and not n.startswith(prefijo):
        n = prefijo + n
    return n


# Se calcula TODO primero y solo después se escribe. Así el simulacro y la
# ejecución real recorren exactamente el mismo camino: si el simulacro se ve
# bien, lo que se aplica es eso mismo y no una version parecida.
plan = []
for v in vistas:
    el = desenvolver(v)
    try:
        actual = el.Name
    except Exception:
        continue
    nuevo = nombre_nuevo(actual)
    if nuevo != actual:
        plan.append((el, actual, nuevo))

if simulacro:
    OUT = [
        u'SIMULACRO — no se tocó nada. %d vistas cambiarían:' % len(plan),
        [u'%s  ->  %s' % (a, n) for (_, a, n) in plan],
    ]
else:
    TransactionManager.Instance.EnsureInTransaction(doc)

    hechas, fallos = [], []
    for el, actual, nuevo in plan:
        try:
            el.Name = nuevo
            hechas.append(u'%s  ->  %s' % (actual, nuevo))
        except Exception as e:
            # El fallo más común: ya existe otra vista con ese nombre. Revit
            # exige nombres únicos. No se detiene el lote entero por uno.
            fallos.append(u'%s: %s' % (actual, e))

    TransactionManager.Instance.TransactionTaskDone()

    OUT = [u'%d renombradas, %d fallaron' % (len(hechas), len(fallos)),
           hechas, fallos]
