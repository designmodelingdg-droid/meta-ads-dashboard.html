# -*- coding: utf-8 -*-
"""
01 · AUDITORÍA DE ADVERTENCIAS  ->  CSV

Qué hace
    Saca TODAS las advertencias del modelo a un archivo CSV, con el texto de
    cada una, su gravedad y los ID de los elementos que la causan.

Por qué es el primero del pack
    Un modelo con 400 avisos sin leer no es un modelo grande: es un presupuesto
    con 400 sorpresas dentro. El cuadro de advertencias de Revit no se puede
    ordenar, ni filtrar, ni pasar a nadie. En CSV sí.

Entradas (Dynamo)
    IN[0]  ruta de salida, p. ej. "C:\\temp\\advertencias.csv"
    IN[1]  True para ejecutar. Se pide a propósito: así el script no escribe
           un archivo cada vez que Dynamo refresca el grafo solo.

Salida
    La ruta del CSV escrito, y el número de advertencias encontradas.

NO MODIFICA EL MODELO. Solo lee. Se puede correr sin miedo en un archivo vivo.
"""
import clr
import codecs

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import ElementId

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

ruta     = IN[0]
ejecutar = IN[1]


def texto_csv(v):
    """
    Escapa un valor para CSV. Las descripciones de Revit traen comas casi
    siempre, y comillas a veces: sin esto el CSV sale con las columnas corridas
    y nadie entiende por que.

    Se usa '%s' en vez de unicode() o str() porque este script tiene que correr
    igual en el motor viejo de Dynamo (IronPython 2) y en el actual (CPython 3),
    donde unicode() ya no existe.
    """
    if v is None:
        return u''
    s = u'%s' % (v,)
    if any(c in s for c in [u',', u'"', u'\n', u'\r']):
        s = u'"' + s.replace(u'"', u'""') + u'"'
    return s


if not ejecutar:
    OUT = 'Pon IN[1] en True para escribir el archivo.'
else:
    # GetWarnings devuelve los FailureMessage que Revit acumula en el modelo.
    # Es lo mismo que ves en Manage > Warnings, pero manipulable.
    avisos = doc.GetWarnings()

    filas = [u'gravedad,descripcion,n_elementos,ids_elementos']
    for a in avisos:
        # GetSeverity() -> Warning / Error. GetDescriptionText() -> el texto
        # exacto que ves en el cuadro, en el idioma de tu Revit.
        gravedad = a.GetSeverity().ToString()
        desc     = a.GetDescriptionText()

        # GetFailingElements() devuelve los ID de los elementos culpables.
        # Estos ID son los que pegas en Manage > Select by ID para ir a verlos.
        ids = [str(i.IntegerValue) for i in a.GetFailingElements()]

        filas.append(u'%s,%s,%d,%s' % (
            texto_csv(gravedad), texto_csv(desc), len(ids),
            texto_csv(u' '.join(ids))))

    # utf-8 con BOM: sin el BOM, Excel en Windows abre los acentos rotos.
    with codecs.open(ruta, 'w', 'utf-8-sig') as f:
        f.write(u'\n'.join(filas))

    OUT = [ruta, u'%d advertencias exportadas' % len(avisos)]
