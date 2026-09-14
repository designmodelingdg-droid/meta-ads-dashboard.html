# Stop AI Slop — qué se instaló y qué no

La guía traía diez repositorios. **Está instalado uno.** Esto no es pereza: lo
dice la propia guía, y aquí además hay una razón concreta.

## Lo que se instaló

**`humanizer`** — [blader/humanizer](https://github.com/blader/humanizer), MIT.

```bash
npx skills add blader/humanizer     # instalar o actualizar
```

Vive en `.agents/skills/humanizer/`, con un enlace desde `.claude/skills/`.
Se invoca con `/humanizer`.

Qué hace: coge un texto y le quita las marcas de escritura de IA sin cambiar lo
que dice. Va detrás de patrones de estructura, no de palabras sueltas: el
contraste «no es X, es Y», el cierre de una línea que repite lo ya dicho, las
listas de tres por costumbre, la raya por todas partes, la negrita de etiqueta,
el relleno, y los restos de conversación que nunca eran para el lector.

Por qué este y no otro: en la lista de skills de DMA no había **nada** que
tocara el texto. Era el único hueco de verdad.

## Lo que NO se instaló, y por qué

**Las skills de diseño de la guía.** DMA ya tiene `landing-craft`, y su
`references/oficio.md` es exactamente eso: una skill anti-slop de diseño, con
las reglas escritas para esta marca y los contrastes **medidos** sobre los
colores de la casa (`#ca7520` sobre blanco = 3,46:1; `#a7611b` = 4,81:1;
`#e8a04a` sobre azul marino = 7,78:1).

Poner encima una skill de diseño genérica no suma: las dos dan órdenes sobre
lo mismo y el resultado empeora. Es el aviso central de la propia guía —
**una por trabajo, no las diez.**

**Los repos sin instalador** (`awesome-design-md`, `stop-slop`). Son lecturas,
no herramientas. No hay nada que instalar.

## Un aviso para usarlo aquí

El `humanizer` está escrito en inglés y parte de los «Signs of AI writing» de
Wikipedia, que también lo están. Los patrones de **estructura** valen igual en
castellano — el cierre que repite, la tríada forzada, la negrita de etiqueta,
el bombo. Las listas de **palabras** concretas no: están en inglés.

Así que en un copy de DMA sirve para la estructura. Para el vocabulario, quien
manda sigue siendo la voz de la marca.

## Si se quiere otra

Antes de instalar la siguiente, la pregunta es cuál es el hueco. Si no se sabe
nombrar el hueco, la skill nueva no lo va a tapar: va a discutir con las que ya
están.
