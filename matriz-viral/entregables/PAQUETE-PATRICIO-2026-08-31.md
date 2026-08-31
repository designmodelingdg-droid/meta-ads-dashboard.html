# Paquete para Patricio — reunión Olympus del 31-ago

Todo lo que pediste en la reunión y en el grupo, en un solo sitio.
Grabación: https://fathom.video/calls/803077550

---

## 1 · La plantilla HTML del blog

```
https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/claude/remote-control-setup-GUe3f/matriz-viral/guiones/blog-ia-revit-LISTO-PARA-PEGAR.html
```

Es el **ejemplo trabajado completo** (el artículo de IA en Revit ya publicado),
no una plantilla parametrizada — la estructura a replicar es:

- Cabecera en comentario HTML: `Título · Slug · Meta · Portada`
- Cuerpo en `<h2>` / `<p>` / `<blockquote>` limpios, sin estilos en línea —
  el blog de GHL pone los suyos
- **Las imágenes van alojadas en GitHub Pages del repo**, con URL permanente;
  nunca subidas al editor de GHL
- Portada 1200 × 675
- Cierra con el enlace a la landing del recurso **dentro del cuerpo**, no solo
  al final, y el descargo educativo

## 2 · La plantilla de correo — y el dato que explica por qué «no quedaron bien»

```
https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/claude/remote-control-setup-GUe3f/matriz-viral/seguimiento/plantilla-email.html
```

Esta es **la buena para secuencias y anuncios**: pesa **menos de 8 KB**, tabla
de 600 px, estilos en línea, imágenes por URL. Se rellena con 5 marcadores:

```
[[TITULO]]  [[CUERPO]]  [[TEXTO_BOTON]]  [[ENLACE_BOTON]]  [[PD]]
```

⚠️ **El dato importante:** existe otra plantilla (la del skill de campañas)
que pesa **~860 KB** porque lleva las imágenes en base64. **Gmail recorta todo
correo que pase de 102 KB** y muestra «[Mensaje recortado]» justo donde va el
botón. Si la app generó correos con esa, ahí está el porqué de que no quedaran
bien. Para la app: **siempre la de 8 KB**; la pesada solo sirve para un
broadcast único.

Y del acuerdo de la reunión: el botón «Enviar a GHL» debe dejar las plantillas
**en una carpeta propia**, no mezcladas con los correos viejos.

## 3 · El usuario de GitHub para invitar (tú deployas, ella edita)

```
designmodelingdg-droid
```

## 4 · El repo de la agenda (referencia de diseño)

```
https://github.com/designmodelingdg-droid/mi-agenda        (privado)
```

Es la app personal de agenda de Dayana — Next.js + Supabase — construida con
el método de The Architect (blueprint completo en `BLUEPRINT.md`: modelo de
datos, SQL, seguridad y orden de construcción). Comprobado antes de compartir:
**no tiene ninguna llave commiteada** — la `service_role` vive solo en Render.

Como es privado, Dayana te invita como colaborador de lectura:
**github.com/designmodelingdg-droid/mi-agenda → Settings → Collaborators →
Add people** → tu usuario de GitHub (pásaselo).

---

## Las tareas que quedaron, por si acaso

**Patricio (por fases, como dijiste):** reestructurar la navegación
(Contenido / Tareas del equipo / Ventas y Playbook, Aprobación dentro del
Calendario) · filtros de responsable y fecha en el Kanban · interfaz simple de
closer (asistió / compró) con webhook a GHL · atribución de reuniones por el
«asignado a» del lead · dashboard de KPIs automático desde GHL · generación de
blog y correo enganchada a la Matriz con estas plantillas · corregir «Enviar a
GHL» · adjuntos en tareas · compromisos de Fathom → botón «convertir en tarea».

**Ester:** doc de cómo se espera ver cada sección, con los cambios de botones
y agrupaciones (ya lo anunció en el grupo).

**Dayana:** este paquete ✓ · invitar a Patricio a `mi-agenda` · editar el
diseño en el repo de Olympus cuando llegue la invitación.
