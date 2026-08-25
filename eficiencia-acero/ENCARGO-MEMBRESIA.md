# Encargo · la membresía de ACERO

**Es lo único que le falta al recurso para entregar como entregan los demás.**

Esto no salió de la documentación de GHL: salió de mirar por HTTP cómo entregan
de verdad la Calculadora de Zapatas y el Test de Nivel, hoy, en producción.

---

## Lo que hacen los que ya funcionan

Los dos entregan **por un producto del portal**, y nada más:

```
Zapatas  → …/courses/products/7a9d1130-0681-44d8-b448-9904cb54af93/purchase-course
Test     → …/courses/products/3e9cf6a3-04cd-4a93-a7b8-2d5749206ebd/purchase-course
```

Tres cosas que se ven ahí y conviene copiar tal cual:

1. **El dominio es `designmodelingacademy.app.clientclub.net`.**
2. **La URL termina en `/purchase-course`** — no en el id a secas. Es la página
   de inscripción a la oferta.
3. **La gracias de Zapatas NO da ningún enlace directo.** Solo el botón del
   portal, uno, grande. Comprobado: cero referencias a `github.io` en esa
   página. Ese es el estándar de la casa.

La de ACERO hoy entrega el enlace directo con token, que fue lo correcto
mientras la membresía no existiera —nadie se quedó esperando— pero no es como
entregan los demás.

---

## Para pegar tal cual

```text
En GoHighLevel (subcuenta Design Modeling), Memberships.

PASO 1 — Crear el producto.
Memberships → Courses → Products → Create Product, plantilla en blanco.
Nombre: 5 Verificaciones en Acero · Herramienta DMA

PASO 2 — Dos lecciones, una por entregable.
En cada una, widget de Custom Code con un iframe:

  Lección 1 · La guía
  <iframe src="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/eficiencia-acero/guia.html?acceso=dm2026"
    style="width:100%;min-height:2400px;border:none;border-radius:12px"
    title="Las 5 verificaciones en acero"></iframe>

  Lección 2 · El verificador
  <iframe src="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/eficiencia-acero/app.html?acceso=dm2026"
    style="width:100%;min-height:1700px;border:none;border-radius:12px"
    title="Verificador de eficiencia en acero"></iframe>

El ?acceso=dm2026 las abre ya desbloqueadas: el candado no debe molestar a
quien ya es miembro, porque la membresía ya hizo el control de acceso.

Iframe y NO pegar el código: la fuente vive en GitHub Pages, así una
corrección se publica una vez y se refleja sola en la membresía, en el funnel
y en el enlace público.

PASO 3 — La oferta.
Memberships → Offers → New Offer → agregar el producto → precio Free →
guardar Y PUBLICAR.

PASO 4 — Publicar el PRODUCTO, no solo la lección y la oferta. Y confirmar
que la app de Cursos está habilitada en el Client Portal. Son las dos causas
típicas de «el portal se ve vacío».

PASO 5 — Conectar el workflow.
En el workflow que dispara el formulario de ACERO, añadir la acción
«Membership Grant Offer» → esa oferta. Con eso GHL crea el usuario del portal
y le manda sus credenciales.

PASO 6 — Pasarme la URL del producto.
Va a tener esta forma, igual que las otras dos:
https://designmodelingacademy.app.clientclub.net/courses/products/<ID>/purchase-course

Ojo con la terminación /purchase-course: las dos que ya funcionan la llevan.


VERIFICACIÓN, y no es mirar que los botones se pongan verdes:

  1. Pedir esa URL por HTTP y confirmar que responde 200.
  2. Llenar el formulario de ACERO de verdad, con un correo de prueba.
  3. Confirmar que llegó el correo con las credenciales del portal.
  4. Entrar al portal con esas credenciales y ver LAS DOS lecciones,
     con la guía y el verificador cargando dentro, sin candado.
  5. Buscar el contacto en el CRM y confirmar que el campo de perfil quedó
     guardado. Ese es el que falla en silencio.

REGLAS

- No borres ningún producto ni oferta existente. Solo crear.
- Si algo no sale, dilo con lo que viste. Un «no pude» con evidencia vale más
  que un «listo» que no es.
```

---

## Cuando llegue la URL

Se pega en `eficiencia-acero/gracias-agenda.html`:

```js
const URL_MEMBRESIA = '';   // ← aquí
```

Con eso los dos botones pasan a apuntar al portal y el aviso cambia solo a
«revisa tu correo». Mientras esté vacío sigue entregando el acceso directo, que
es la red de seguridad: **primero que funcione, después que funcione bonito.**

Y hay que volver a publicar la página en GHL, porque ese HTML vive pegado allá.
