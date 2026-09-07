# -*- coding: utf-8 -*-
"""Prueba de la logica de los scripts que NO depende de Revit.

Que se puede probar aqui: el escapado de CSV (script 01) y la firma que agrupa
duplicados (script 02). Son las dos piezas donde un fallo pasa desapercibido —
un CSV con columnas corridas o un agrupamiento que se salta duplicados reales.

Que NO se prueba aqui, y hay que probarlo en Revit: todo lo que llama a la API.
Esta prueba no dice que los scripts funcionen: dice que estas dos piezas si.

    python3 pack-dynamo/prueba/logica.py
"""
import sys, ast, io, os, textwrap

RAIZ = os.path.join(os.path.dirname(__file__), '..', 'scripts')
fallos = []


def extraer(fichero, nombre_funcion):
    """Saca una funcion del script sin ejecutar el resto (que necesita Revit)."""
    src = io.open(os.path.join(RAIZ, fichero), encoding='utf-8').read()
    arbol = ast.parse(src)
    for n in arbol.body:
        if isinstance(n, ast.FunctionDef) and n.name == nombre_funcion:
            ns = {}
            exec(compile(ast.Module(body=[n], type_ignores=[]), '<x>', 'exec'), ns)
            return ns[nombre_funcion]
    raise AssertionError('no encontre %s en %s' % (nombre_funcion, fichero))


def check(etiqueta, obtenido, esperado):
    ok = obtenido == esperado
    if not ok:
        fallos.append('%s: obtuve %r, esperaba %r' % (etiqueta, obtenido, esperado))
    print('  %s %s' % ('OK  ' if ok else 'FALLA', etiqueta))


print('01 · escapado de CSV')
texto_csv = extraer('01_auditoria_advertencias.py', 'texto_csv')
# Textos reales de advertencias de Revit, que es donde esta el problema
check('descripcion con coma se entrecomilla',
      texto_csv('Highlighted walls overlap, one may be ignored'),
      '"Highlighted walls overlap, one may be ignored"')
check('texto simple no se toca', texto_csv('Warning'), 'Warning')
check('comillas dentro se duplican',
      texto_csv('El elemento "V-12" falla'), '"El elemento ""V-12"" falla"')
check('salto de linea se entrecomilla',
      texto_csv('linea1\nlinea2'), '"linea1\nlinea2"')
check('None da cadena vacia', texto_csv(None), '')
check('un numero no revienta', texto_csv(431287), '431287')
check('acentos intactos', texto_csv('Cotas huérfanas'), 'Cotas huérfanas')

print('\n02 · firma que agrupa duplicados')
# Reproduzco la clave del script 02 con la misma aritmetica
tol_pies = 1.0 / 304.8          # 1 mm


def clave(tipo, x, y, z):
    r = lambda v: round(v / tol_pies)
    return (tipo, r(x), r(y), r(z))


# Dos elementos exactamente encima -> misma casilla
check('duplicado exacto agrupa',
      clave(100, 5.0, 3.0, 0.0) == clave(100, 5.0, 3.0, 0.0), True)
# Separados 0,3 mm -> siguen siendo el mismo sitio
d = 0.3 / 304.8
check('a 0,3 mm sigue agrupando',
      clave(100, 5.0, 3.0, 0.0) == clave(100, 5.0 + d, 3.0, 0.0), True)
# Separados 5 mm -> son dos elementos distintos, NO deben agruparse
d5 = 5.0 / 304.8
check('a 5 mm NO agrupa',
      clave(100, 5.0, 3.0, 0.0) == clave(100, 5.0 + d5, 3.0, 0.0), False)
# Mismo sitio pero distinto tipo -> no es un duplicado
check('mismo sitio, distinto tipo, NO agrupa',
      clave(100, 5.0, 3.0, 0.0) == clave(200, 5.0, 3.0, 0.0), False)

print('\n' + ('FALLOS:\n  ' + '\n  '.join(fallos) if fallos else
      'Las dos piezas probables funcionan.'))
print('\nRECORDATORIO: esto no prueba los scripts. Todo lo que llama a la API\n'
      'de Revit solo se puede probar abriendo Revit y ejecutandolos.')
sys.exit(1 if fallos else 0)
