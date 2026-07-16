# Publicar la matriz fresca para la app (Patricio)

La app de contenido (`dg-contenido-ia.vercel.app`) debe leer **siempre** la última
versión de `matriz-viral/matriz/matriz.json` sin que el repo deje de ser privado.
La Action `publish-matriz.yml` lo resuelve publicando ese JSON a una URL pública
cada vez que cambia.

## Cómo funciona

1. Actualizamos la matriz en el repo (nuevo barrido de Apify, nuevos reels, etc.).
2. Al hacer push, si cambió `matriz.json`, la Action lo copia a GitHub Pages.
3. La app lo lee desde la URL pública → datos frescos, sin copiar nada a mano.

## Setup de una sola vez (2 minutos)

1. Haz **merge del PR #3** para que la Action y el `matriz.json` queden en la rama
   por defecto (`claude/remote-control-setup-GUe3f`).
2. En GitHub: **Settings → Pages → Build and deployment → Source: "GitHub Actions"**.
3. Corre la Action una vez a mano: pestaña **Actions → "Publicar matriz.json" → Run
   workflow** (o simplemente vuelve a pushear un cambio en `matriz.json`).

Listo. La URL pública queda en:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/matriz.json
```

> Refresco: Pages cachea ~10 min en CDN, así que un cambio tarda unos minutos en
> reflejarse. Para contenido de estrategia es más que suficiente.

## Cómo la app lee el JSON (Vercel)

GitHub Pages envía `Access-Control-Allow-Origin: *`, así que la app puede hacer
`fetch` directo desde el navegador o desde el server:

```js
const URL_MATRIZ =
  "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/matriz.json";

export async function getMatriz() {
  const res = await fetch(URL_MATRIZ, { next: { revalidate: 600 } }); // Next.js: revalida cada 10 min
  if (!res.ok) throw new Error("No se pudo leer la matriz");
  return res.json(); // { generado, total_reels, ejes, reels: [...] }
}
```

Cada reel trae: `id, shortCode, eje, fecha, duracion_s, views, likes, comentarios,
tema, estructura, hook, url`. El generador de contenido puede filtrar por `eje`
(`NÚCLEO-IA` / `NÚCLEO-BIM`) y ordenar por `views`/`comentarios` para alimentarse
solo de lo que funciona.

---

## Plan B — si GitHub Pages no está disponible (repo privado en plan Free)

Pages para repos privados requiere GitHub Pro/Team. Si tu repo es privado en el
plan Free, usa un **Gist público** en vez de Pages. Reemplaza la Action por esta:

```yaml
name: Publicar matriz.json (Gist)
on:
  push:
    branches: [claude/remote-control-setup-GUe3f, claude/matriz-viral-3t356o]
    paths: [matriz-viral/matriz/matriz.json]
  workflow_dispatch: {}
jobs:
  gist:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Actualizar Gist público
        env:
          GH_TOKEN: ${{ secrets.GIST_TOKEN }}   # PAT con scope "gist"
          GIST_ID: ${{ secrets.GIST_ID }}        # id del gist público
        run: |
          set -euo pipefail
          CONTENT=$(python3 -c "import json;print(json.dumps({'files':{'matriz.json':{'content':open('matriz-viral/matriz/matriz.json').read()}}}))")
          curl -sS -X PATCH \
            -H "Authorization: Bearer $GH_TOKEN" \
            -H "Accept: application/vnd.github+json" \
            "https://api.github.com/gists/$GIST_ID" \
            -d "$CONTENT" > /dev/null
          echo "Gist actualizado."
```

Setup del Plan B:
1. Crea un **Gist público** con un archivo `matriz.json` (cualquier contenido) y
   copia su **ID** (el hash en la URL del gist).
2. Crea un **Personal Access Token** con scope `gist` (Settings → Developer
   settings → Tokens).
3. En el repo: **Settings → Secrets and variables → Actions** → agrega
   `GIST_TOKEN` (el PAT) y `GIST_ID` (el id del gist).
4. La app lee: `https://gist.githubusercontent.com/<usuario>/<GIST_ID>/raw/matriz.json`

(La opción de Pages es más limpia; el Gist es el respaldo a prueba de planes.)
