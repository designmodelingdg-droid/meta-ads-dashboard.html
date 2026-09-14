# Cómo instalar la skill scroll-craft de Luciano Mattica

Sirve para Claude Code. Construye landing pages premium con scroll como línea de tiempo, capas de profundidad en el hero y verificación visual con screenshots.

## 1. Descomprimí el zip
Te queda una carpeta llamada `lucianomattica-design`. Dejala en algún lugar fijo (por ejemplo, Documentos).

## 2. Instalá el plugin
Abrí una terminal, entrá a la carpeta donde quedó descomprimido y corré:

```bash
claude plugin marketplace add ./lucianomattica-design
claude plugin install lucianomattica-design@lucianomattica
```

Si Claude Code te dice "Run /reload-plugins to activate", hacelo o abrí una sesión nueva.

## 3. Usala
Dentro de Claude Code, en la carpeta de tu proyecto:

```
/lucianomattica-design:scroll-craft
```

Contale qué querés construir. La skill te va a hacer unas preguntas (vibra, recorrido, energía, el momento que querés que se recuerde, qué imágenes tenés) y después construye.

## Requisitos
- Node 18 o superior.
- ffmpeg y Google Chrome instalados.
- Para que verifique con screenshots: `npm i playwright-core` dentro de tu proyecto.
- Opcional: una clave de kie.ai si querés que genere imágenes. Con tus propias fotos o recortes PNG no hace falta.

Diagnóstico rápido, desde la carpeta descomprimida:

```bash
node plugins/lucianomattica-design/skills/scroll-craft/scripts/doctor.mjs
```

## Tips para que salga bien
- Pasale un `brand.md` con colores, tipografía, tono y las 3 P: qué dolor resolvés, para quién, y qué promesa hacés.
- Dale imágenes por capas: un fondo sin el objeto, y cada elemento recortado con transparencia real, todos con la misma luz.
- Pedile siempre que se saque screenshots del scroll en desktop y en mobile y que corrija antes de mostrarte.

---
Basada en scroll-craft de Nate Herk (licencia MIT). Personalizada por Luciano Mattica.
