# -*- coding: utf-8 -*-
"""
02 · ELEMENTOS DUPLICADOS EN EL MISMO SITIO

Qué hace
    Encuentra elementos idénticos superpuestos exactamente: mismo tipo, misma
    posición. Devuelve los ID para que los selecciones en Revit.

Por qué importa
    Es el error que más caro sale de todos, porque no se ve. Los planos salen
    bien. El cuadro de cantidades cuenta el doble. Y nadie se entera hasta que
    alguien presupuesta con ese número.

Entradas (Dynamo)
    IN[0]  lista de elementos a revisar (de un Categories + All Elements of
           Category, por ejemplo), o None para revisar todo el modelo visible
    IN[1]  tolerancia en milímetros, por defecto 1. Dos elementos a menos de
           esa distancia se consideran en el mismo sitio.

Salida
    Lista de grupos duplicados, cada uno con sus ID.

NO MODIFICA EL MODELO. Solo lee y te dice dónde mirar. Borrar es tu decisión:
puede haber duplicados legítimos, y solo tú sabes cuál de los dos conservar.
"""
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, LocationPoint, LocationCurve

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

entrada   = IN[0]
tol_mm    = IN[1] if len(IN) > 1 and IN[1] else 1.0
# Revit trabaja internamente en pies decimales, siempre, sin importar las
# unidades del proyecto. 1 pie = 304.8 mm.
tol_pies  = tol_mm / 304.8


def desenvolver(x):
    """Dynamo entrega elementos envueltos. Saca el Element de Revit."""
    return x.InternalElement if hasattr(x, 'InternalElement') else x


def punto(el):
    """Posición representativa del elemento, o None si no tiene."""
    loc = el.Location
    if isinstance(loc, LocationPoint):
        return loc.Point
    if isinstance(loc, LocationCurve):
        # Para vigas y muros, el punto medio de su curva sirve de firma.
        c = loc.Curve
        return c.Evaluate(0.5, True)
    return None


def clave(el):
    """
    Firma del elemento: tipo + posición redondeada a la tolerancia.
    Redondear ANTES de comparar es lo que hace que dos elementos a 0,3 mm
    caigan en la misma casilla sin tener que compararlos todos contra todos.
    """
    p = punto(el)
    if p is None:
        return None
    r = lambda v: round(v / tol_pies)
    return (el.GetTypeId().IntegerValue, r(p.X), r(p.Y), r(p.Z))


# Si no le das nada, revisa todo lo que hay en el modelo.
if entrada:
    elementos = [desenvolver(e) for e in entrada]
else:
    elementos = list(FilteredElementCollector(doc)
                     .WhereElementIsNotElementType()
                     .ToElements())

cajas = {}
for el in elementos:
    try:
        k = clave(el)
    except Exception:
        k = None          # elementos sin geometría utilizable: se ignoran
    if k is None:
        continue
    cajas.setdefault(k, []).append(el)

# Solo interesan las casillas con más de uno dentro.
grupos = [g for g in cajas.values() if len(g) > 1]

resultado = []
for g in grupos:
    nombre = g[0].Name if hasattr(g[0], 'Name') else '(sin nombre)'
    resultado.append({
        'tipo': nombre,
        'cuantos': len(g),
        'ids': [e.Id.IntegerValue for e in g],
    })

total_sobrantes = sum(g['cuantos'] - 1 for g in resultado)

OUT = [
    u'%d grupos duplicados · %d elementos sobrantes' % (len(resultado), total_sobrantes),
    resultado,
]
