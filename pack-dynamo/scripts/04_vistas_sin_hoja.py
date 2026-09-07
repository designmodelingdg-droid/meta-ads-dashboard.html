# -*- coding: utf-8 -*-
"""
04 · VISTAS QUE NO ESTÁN EN NINGUNA HOJA

Qué hace
    Lista las vistas del proyecto que no se han colocado en ninguna hoja.

Para qué sirve
    Dos cosas. Limpiar el archivo —cada vista cuesta peso y tiempo de apertura—
    y, sobre todo, DETECTAR LO QUE FALTA POR ENTREGAR: una vista trabajada que
    no está en ninguna hoja suele ser una vista que alguien olvidó colocar.

Entradas (Dynamo)
    IN[0]  True para incluir también las plantillas de vista (por defecto False:
           las plantillas nunca van en hojas y solo ensucian la lista)

Salida
    La lista de vistas sin hoja, con su tipo, y el conteo.

NO MODIFICA EL MODELO. Borrar vistas es irreversible y la decisión es tuya:
esta lista es para mirarla, no para borrarla en bloque.
"""
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import (FilteredElementCollector, View, ViewType,
                               ViewPlacementOnSheetStatus)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

incluir_plantillas = IN[0] if len(IN) > 0 and IN[0] else False

# Estos tipos de vista NO van en hojas por definición. Si no se excluyen,
# la lista sale llena de ruido y nadie la lee — que es peor que no tenerla.
NUNCA_EN_HOJA = set([
    ViewType.ProjectBrowser,
    ViewType.SystemBrowser,
    ViewType.Internal,
    ViewType.DrawingSheet,     # la hoja no va dentro de otra hoja
    ViewType.Schedule,         # las tablas se colocan aparte
])

vistas = (FilteredElementCollector(doc)
          .OfClass(View)
          .WhereElementIsNotElementType()
          .ToElements())

sin_hoja = []
for v in vistas:
    if v.IsTemplate and not incluir_plantillas:
        continue
    if v.ViewType in NUNCA_EN_HOJA:
        continue

    # GetPlacementOnSheetStatus es la forma correcta de preguntarlo. La
    # alternativa —recorrer todos los Viewport— se deja fuera vistas que se
    # colocan por otros medios, como las tablas segmentadas.
    try:
        estado = v.GetPlacementOnSheetStatus()
    except Exception:
        continue

    if estado == ViewPlacementOnSheetStatus.NotPlaced:
        sin_hoja.append(v)

detalle = sorted(
    [u'%s  ·  %s' % (v.ViewType.ToString(), v.Name) for v in sin_hoja])

OUT = [
    u'%d vistas sin colocar en ninguna hoja (de %d revisadas)'
    % (len(sin_hoja), len(vistas)),
    detalle,
    [v.Id.IntegerValue for v in sin_hoja],
]
