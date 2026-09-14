# Agent Reach — dónde se instala, y por qué NO aquí

[Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) · MIT · Python 3.10+

Un CLI que le da al agente ojos para leer Twitter, Reddit, YouTube, GitHub,
Instagram, Facebook y unas cuantas más, sin pagar APIs. Instala las
herramientas que leen cada red y escribe un fichero de skill que le dice al
agente qué ejecutar en cada caso. **Él no lee nada: enruta.**

## CUIDADO con el nombre

Hay al menos dos repositorios más llamados `agent-reach`, de otros autores.
El bueno es **`Panniantong/Agent-Reach`** — con esa mayúscula y ese autor.
Comprobado contra GitHub el 14-sep-2026: 80.850 estrellas. Los clones tenían
56 y 13. La propia guía avisa de que instalar el paquete equivocado es el
error más común, y aquí eso significa ejecutar código de un desconocido.

## Va en TU máquina, no en la sesión remota

Esto es lo importante y no lo dice la guía:

| Red | Qué necesita |
|---|---|
| Web, YouTube, RSS, V2EX | nada |
| GitHub, LinkedIn | credenciales solo para lo privado |
| Twitter/X, 小红书 | cookie o credenciales |
| **Instagram, Facebook, Reddit** | **sesión de Chrome de escritorio iniciada** |

Las tres que de verdad le sirven a DMA —Instagram, Facebook y Reddit— piden un
Chrome de escritorio con la sesión abierta. En el contenedor remoto donde corre
esta sesión **no hay navegador con tus sesiones**, y además el contenedor se
recicla: un `--system` aquí desaparece solo.

Lo que sí funcionaría en remoto —web, YouTube, GitHub, RSS— ya está cubierto
por WebFetch, WebSearch, el MCP de GitHub y Apify.

**Conclusión: se instala en el Claude Code de tu computadora.**

```bash
mkdir -p ~/.claude/skills          # el instalador solo escribe en carpetas que ya existen
pipx install "https://github.com/Panniantong/Agent-Reach/archive/main.zip"
agent-reach install --env=auto --system
agent-reach doctor --json          # dice qué funciona en TU equipo
```

Sin `--system` solo comprueba, no toca nada. Con `--system` instala
dependencias y registra el `SKILL.md`. Después, reiniciar la sesión del agente
para que cargue la skill nueva.

## El riesgo que sí hay que pensar

Para leer Instagram y Facebook usa **la sesión de tu navegador**, o sea la
cuenta con la que estés dentro. El propio README avisa del riesgo de bloqueo
por usar la cuenta principal.

La cuenta principal de DMA **es el negocio**. Un bloqueo de
@design_modeling_dg cuesta muchísimo más que lo que ahorra la herramienta. Si
se usa para Instagram o Facebook, que sea con una cuenta secundaria, nunca con
la que publica y paga la pauta.

Para leer métricas de nuestras propias piezas ya está Apify, que no toca la
sesión de nadie.
