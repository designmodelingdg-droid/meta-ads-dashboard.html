# Ganadores de agosto 2026 — lo que se replica en septiembre

Esta carpeta existe por una sola razón: que las imágenes de los anuncios
ganadores tengan una **dirección estable**. Se publican a GitHub Pages, así que
el mazo de la reunión no depende de que una rama siga viva.

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cierre-agosto/img/…
```

## Los dos creativos

De los 6 anuncios con más leads del mes hay **solo 2 imágenes distintas**. Los
seis archivos que devolvió la API de Meta se reducen a dos md5: los rangos 1, 3,
4 y 6 son el mismo creativo corriendo en distintos conjuntos, y los rangos 2 y 5
son el otro. No es un error del volcado — es lo que de verdad pasó.

| Archivo | Leads | Gasto | CPL | Qué es |
|---|---|---|---|---|
| `anuncio-1-experto-bim-3x1.jpg` | 873 | $288,33 | $0,33 | Video. «Conviértete en un experto BIM», promo 3×1, CTA a WhatsApp |
| `anuncio-2-nave-industrial-30dias.jpg` | 512 | $164,15 | $0,32 | Estático. «Modela tu primera nave industrial en 30 días», CTA a WhatsApp |

Entre los dos: **1.385 de los 1.477 leads del mes**, el 94%.

El archivo del anuncio 1 es un fotograma del video, no el video. El volcado de
Meta trae además la portada en baja resolución y desenfocada
(`01-…-copia.jpg`, 28 KB): esa no sirve para mostrar nada, y es la razón de que
aquí esté el fotograma `-h` en su lugar.

## Lo que hay que arreglar antes de volver a usarlos

**Los dos llevan $199,99 impreso.** El precio de la Especialización es $225
desde el 3 de septiembre. Tal como están no pueden salir: ninguno de los dos se
puede reactivar sin rehacer la pieza.

Y los dos son de **julio**. Llevan dos meses corriendo sin reemplazo. Que sigan
ganando no significa que estén frescos: significa que no se ha probado nada
contra ellos.

## Lo orgánico

No hay archivos de imagen de las piezas orgánicas: la matriz guarda el enlace
permanente de Instagram, no el creativo. Los ganadores del mes van en el mazo
como enlace, que es lo que de verdad tenemos. Recuperar las imágenes requiere el
token de la Graph API de Meta (`META_TOKEN`), que no vive en el repositorio.
