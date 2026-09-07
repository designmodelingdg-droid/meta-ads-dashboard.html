# -*- coding: utf-8 -*-
"""
05 · RELLENAR UN PARÁMETRO EN LOTE

Qué hace
    Escribe el mismo valor en un parámetro de muchos elementos a la vez.
    Sirve para rellenar Comentarios, Marca, Fase, códigos de clasificación,
    o cualquier parámetro de proyecto que hayas creado.

Entradas (Dynamo)
    IN[0]  lista de elementos
    IN[1]  nombre EXACTO del parámetro (respeta mayúsculas y acentos)
    IN[2]  valor a escribir
    IN[3]  SIMULACRO: True = solo dice qué haría, NO toca nada
                      False = escribe de verdad

⚠️ ESTE SCRIPT SÍ MODIFICA EL MODELO cuando IN[3] es False.

    El simulacro no es un adorno: te dice cuántos elementos NO tienen ese
    parámetro y cuántos lo tienen de solo lectura. Esos dos números son los que
    de verdad quieres ver antes de escribir en 800 elementos.

Salida
    Cuántos se escribieron, cuántos no tenían el parámetro, cuántos eran de
    solo lectura y cuántos fallaron.
"""
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import StorageType

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

elementos = IN[0] if isinstance(IN[0], list) else [IN[0]]
nombre    = IN[1]
valor     = IN[2]
simulacro = IN[3] if len(IN) > 3 else True     # por defecto NO toca nada


def desenvolver(x):
    return x.InternalElement if hasattr(x, 'InternalElement') else x


def escribir(p, v):
    """
    Set espera el tipo correcto según cómo guarde Revit ese parámetro.
    Pasarle una cadena a un parámetro numérico no da error: no hace nada.
    Por eso se mira StorageType antes y no después.
    """
    st = p.StorageType
    if st == StorageType.String:
        return p.Set(str(v))
    if st == StorageType.Integer:
        return p.Set(int(v))
    if st == StorageType.Double:
        return p.Set(float(v))
    if st == StorageType.ElementId:
        return False          # requiere un ElementId real: fuera del alcance
    return False


sin_parametro, solo_lectura, listos = [], [], []

for e in elementos:
    el = desenvolver(e)
    p = el.LookupParameter(nombre)
    if p is None:
        sin_parametro.append(el.Id.IntegerValue)
    elif p.IsReadOnly:
        solo_lectura.append(el.Id.IntegerValue)
    else:
        listos.append((el, p))

if simulacro:
    OUT = [
        u'SIMULACRO — no se tocó nada.',
        u'%d se escribirían' % len(listos),
        u'%d NO tienen el parámetro «%s»' % (len(sin_parametro), nombre),
        u'%d lo tienen de solo lectura' % len(solo_lectura),
        {'sin_parametro': sin_parametro, 'solo_lectura': solo_lectura},
    ]
else:
    TransactionManager.Instance.EnsureInTransaction(doc)

    hechos, fallos = 0, []
    for el, p in listos:
        try:
            if escribir(p, valor):
                hechos += 1
            else:
                fallos.append(u'%d: tipo de parámetro no soportado'
                              % el.Id.IntegerValue)
        except Exception as ex:
            fallos.append(u'%d: %s' % (el.Id.IntegerValue, ex))

    TransactionManager.Instance.TransactionTaskDone()

    OUT = [
        u'%d escritos, %d sin el parámetro, %d de solo lectura, %d fallaron'
        % (hechos, len(sin_parametro), len(solo_lectura), len(fallos)),
        fallos,
    ]
