# scroll-craft en DMA — cuándo sí y cuándo no

Este es el plugin **completo y sin tocar** de Luciano Mattica (fork de scroll-craft
de Nate Herk, MIT). Está aquí para que el equipo lo tenga versionado.

## Para el día a día, NO se usa este plugin

Nuestras landings se pegan dentro de **GHL → Sites → Custom Code container**, y
este plugin construye un sitio propio con su propio motor de scroll (58 KB de JS),
vídeo que se rebobina con la rueda y generación de imagen de pago.

Para las landings de DMA se usa **`landing-craft`**, que es la adaptación: se quedó
con el método y el oficio, y dejó fuera el motor. Está en
`.claude/skills/landing-craft/`.

## Cuándo SÍ tiene sentido este plugin

Cuando haya que hacer **un sitio propio fuera de GHL**: una web de consultoría, un
micrositio de lanzamiento, una página de marca que no cuelgue del CRM. Ahí el
motor de scroll cabe y merece la pena.

Requisitos: Node 18+, ffmpeg, Chrome, y una clave de **kie.ai** solo si se van a
generar imágenes o vídeo (si se construye con fotos propias, no hace falta clave
ni gasto).

## Cómo se instala

```bash
claude plugin marketplace add ./herramientas/scroll-craft
claude plugin install lucianomattica-design@lucianomattica
```

Después queda disponible `/lucianomattica-design:scroll-craft`.

## El flujo de los tres prompts

El documento original de Luciano describe tres prompts en orden:

1. **Preparar la carpeta y escribir el documento de diseño.** Deja el repositorio
   listo y produce `design.md` (todas las decisiones) y `assets/README.md` (la
   lista de imágenes que hay que conseguir). Solo cuando se aprueba ese documento
   se construye la página.
2. **Instalar el plugin.**
3. **Construir**, invocando la skill, que lee el `design.md`, pregunta solo lo que
   falta y construye tomando capturas del scroll para corregirse sola.

Las reglas que el propio autor destaca, y que ya están recogidas en
`landing-craft`: no inventar números ni precios, dar los colores en hexadecimal,
nombrar referencias de otros medios (una revista, una luz, un catálogo) en lugar de
sitios web, y pedir siempre verificación con capturas antes de mostrar el
resultado.

## Aviso

La clave `KIE_AI_API_KEY` va en un `.env` local, **nunca** en el repositorio ni en
un chat. El `.gitignore` del plugin ya excluye `.env`.
