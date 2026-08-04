# Plan — Hub de recursos gratuitos de DMA

**Estado:** plan aprobado, sin construir · **Fecha:** 2026-08-04
**Bloquea a:** el anuncio del Test de Nivel BIM en redes (decisión de Dayana:
el test no sale a redes hasta que el hub exista).

---

## 1. El problema que resuelve

Hoy cada recurso gratuito es una isla con su propia landing:

| Recurso | Dónde vive | Cómo llega la gente |
|---|---|---|
| Calculadora de Zapatas | `/calculadora-zapatas` | bot ZAPATA, pauta |
| Test de Nivel BIM | `/test-nivel-bim` | bot NIVEL, pauta |
| Artículos | el blog de GHL | orgánico |
| Ebook BIM, GPTs, guías | sueltos | s/d |

Eso obliga a tener **un enlace distinto por pieza**, y el que llega por una
herramienta no se entera de que existen las demás. La calculadora se llevó el
70% del alcance de julio y **no empujó a nada más**, porque no había a dónde
empujar.

El hub convierte eso en **un solo destino** que crece solo: cada herramienta
nueva suma al mismo enlace en vez de competir con él.

## 2. Dónde vive

`https://funnel.dgdesignmodeling.com/recursos`

Mismo patrón que el test: se genera desde este repositorio, se pega en un
contenedor Custom Code de GHL, vive bajo el dominio propio. Las herramientas
se siguen sirviendo desde GitHub Pages, embebidas.

**No sustituye al blog.** El blog sigue siendo donde viven los artículos; el
hub es la portada de lo *gratis y accionable*, y enlaza al blog.

## 3. Los tres niveles de acceso

Es la decisión de fondo y define el resto:

| Nivel | Qué pide | Qué entrega | Para qué sirve |
|---|---|---|---|
| **Abierto** | nada | artículos del blog, GPTs públicos | que Google y las redes lo indexen; es la puerta |
| **Con registro** | nombre, correo, teléfono, perfil | las herramientas (calculadora, test) y las descargas | **es el que mete gente al CRM** |
| **Comunidad** | entrar a la comunidad gratuita | rutas completas, sesiones, lo que se sume | retención y conversación |

La regla: **cada nivel deja ver el siguiente**. Quien lee un artículo ve que
hay herramientas; quien usa una herramienta ve que hay comunidad. Sin eso el
hub es solo un listado.

## 4. Qué va dentro, en la primera versión

Solo lo que **existe y funciona hoy**. Nada de "próximamente":

1. **Test de Nivel BIM** — destacado arriba, es el estreno.
2. **Calculadora de Zapatas** — la que ya trae tráfico.
3. **Artículos del blog** — 4 a 6 seleccionados, enlazando al blog de GHL.
4. **La comunidad gratuita** — bloque de cierre, con qué se encuentra dentro.

Pendiente de inventario de Dayana: ebook BIM, GPTs y guías. Si están listos y
son gratuitos, entran en la primera versión; si no, en la segunda.

## 5. Cómo se construye

| Fase | Qué | Quién |
|---|---|---|
| **A** | Página `recursos/index.html` con el sistema visual de DMA (mismo que test y zapatas: nav blanco, navy + naranja, tarjeta por recurso) | Claude Code |
| **B** | `ghl-recursos.html` generado con `build_ghl_landing.py` y verificado en móvil | Claude Code |
| **C** | Pegar en GHL en la ruta `/recursos`, publicar | Claude del navegador |
| **D** | Enlazar desde: bio de Instagram, blog, comunidades, y los DM de los dos bots | Claude del navegador |

La fase A y B son de un tirón. Lo que marca el ritmo es C y D.

## 6. Decisiones tomadas (4-ago-2026)

- **Ruta confirmada:** `/recursos`.
- **Ebook BIM, GPTs y guías:** existen y son gratuitos. Dayana pasa los
  enlaces. No bloquean la primera versión.

### Corrección importante sobre los artículos

Las cuatro piezas que propuse **no son artículos del blog** — son
publicaciones de redes. Dayana lo aclaró: los artículos del blog todavía **hay
que crearlos**.

Eso no invalida la selección, la cambia de sitio: esas cuatro piezas son las
que **mejor rindieron por guardados**, y un guardado significa "esto me sirve,
vuelvo" — exactamente la intención de un hub. Así que son los **mejores
candidatos a convertirse en los primeros artículos**:

| Tema probado | Vistas | Guardados |
|---|---|---|
| Uniones en estructuras de acero (19-jun) | 11.447 | **71** |
| La IA ya hace 5 tareas de tu trabajo (16-jul) | 4.766 | **66** |
| Cómo se fija una estructura de acero (2-jul) | 4.624 | **45** |
| Le pedí a ChatGPT que diseñara una losa (15-jul) | 3.020 | **45** |

Se reparten entre **acero y BIM+IA**, que son justo los dos productos. No se
forzó: salió así. Confirma que la gente guarda lo que le resuelve trabajo.

### 🚫 Bloqueo: no puedo ver el blog

`funnel.dgdesignmodeling.com` está **bloqueado por la política de red** del
entorno donde corre Claude (`403` del proxy en el CONNECT). No es que el sitio
falle — es este entorno. No puedo inventariar el blog por mi cuenta.

**Lo que hace falta que traiga Dayana** (cualquiera de las tres sirve):

1. La lista pegada: título, URL y fecha de cada artículo publicado.
2. Capturas de la página del blog y de un artículo por dentro.
3. Un export desde GHL, si el blog lo permite.

Con eso puedo decidir qué se destaca, qué se reescribe y qué falta por crear.

## 7. La sesión del jueves — orden de trabajo

Pensado para hacerlo juntos, de lo que no depende de nadie a lo que sí.

| # | Qué | Depende de |
|---|---|---|
| 1 | Revisar el inventario del blog que traiga Dayana: qué hay, qué sirve, qué se reescribe | ella |
| 2 | Decidir los 4-6 destacados y cuáles hay que crear desde cero | los dos |
| 3 | Enlaces del ebook, los GPTs y las guías | ella |
| 4 | Construir `recursos/index.html` con el sistema visual de DMA | Claude |
| 5 | Generar `ghl-recursos.html` y verificarlo en móvil | Claude |
| 6 | Pegarlo en GHL en `/recursos` y publicar | Claude del navegador |
| 7 | Enlazarlo desde bio de IG, blog, comunidades y los DM de los dos bots | Claude del navegador |
| 8 | **Recién ahí**: lanzar el Test de Nivel BIM en redes | — |

**Lo que Claude puede adelantar antes del jueves**, si Dayana lo pide: montar
la página con lo que ya está confirmado —las dos herramientas y la comunidad—
para que el jueves sea rellenar y publicar en vez de empezar de cero.

## 8. Estructura de la página

Decidida, para no discutirla el jueves:

```
1. Cabecera        nav blanco + logo (el sistema de zapatas y del test)
2. Portada         "Todo lo que tenemos gratis, en un solo sitio"
                   + la promesa del nivel de acceso
3. HERRAMIENTAS    2 tarjetas grandes: Test de Nivel BIM · Calculadora
                   (las que piden registro → son las que llenan el CRM)
4. DESCARGAS       ebook, GPTs, guías (cuando lleguen los enlaces)
5. ARTÍCULOS       4-6 tarjetas que enlazan al blog
6. COMUNIDAD       bloque de cierre: qué encuentras dentro + entrar gratis
7. Pie             logo, aviso de que las herramientas son de apoyo
```

**La regla de oro del orden:** las herramientas van **arriba**, antes que los
artículos. Son las que piden registro y por tanto las que meten gente al CRM;
los artículos son abiertos y no capturan nada. Un hub que abre con artículos se
lee como un blog y no convierte.

## 7. Cómo sabremos si funciona

No por visitas. Por estas tres:

- **Registros nuevos al CRM desde el hub** (fuente `hub-recursos`).
- **Cuántos usan una segunda herramienta** — es lo que hoy no pasa y es la
  razón de existir del hub.
- **Entradas a la comunidad** desde el bloque de cierre.

## 8. Encaje con el calendario

El calendario de agosto tiene el **Mié 13** marcado como *"nuevo lead magnet,
por definir"*. **El hub es esa pieza**: en vez de anunciar una herramienta
suelta, se anuncia el sitio donde viven todas — y el Test de Nivel BIM se
estrena dentro de él. Un solo anuncio hace las dos cosas.
