# Correos de seguimiento de los lead magnets · qué está hecho y qué falta

> Datos al 2-oct-2026.
> - **Lo que recibe la gente:** `fuentes/ghl/seguimiento-correos-lm.json`, una muestra de los 20 contactos más recientes con la etiqueta de acceso de cada recurso, con los correos que GHL les mandó de verdad.
> - **Las plantillas que existen:** `fuentes/ghl/INVENTARIO-CORREOS.md`.
> - **Las secuencias escritas:** `seguimiento/correos-nutricion.json`.

## Hecho

| Lead magnet | Correo de acceso | Seguimiento | Lo que recibe la gente |
|---|---|---|---|
| ZAPATA | «Acceso Calculadora Zapatas» | **Activo** (carpeta ✅SEGUIMIENTO CALCULADORA) | 5 correos en unos 13 días, con puente a Acero: Error #1 al dimensionar una zapata · La zapata casi nunca es el problema · Lo que va arriba de la zapata · «Me interesa, pero no tengo tiempo» · Lo que dicen los que ya pasaron |
| NIVEL | «Acceso Test Nivel BIM» | **Activo** (carpeta ✅SEGUIMIENTO TEST BIM) | 4 correos en unos 11 días, con puente al Máster: Los 4 niveles BIM, sin humo · 30 minutos y te digo por dónde empezar · De modelador a coordinador · Microcredenciales, no un PDF al final |

## Falta (tareas para Ester)

1. **MEMORIA. Urgente:** entraron 77 contactos nuevos en 7 días, por el reel del 29-sep.
   - Las plantillas «Acceso Memoria de Cálculo_02», «_03a» («para quien ya entrega») y «_03b» («para quien empieza») existen desde el 11-sep, pero ningún workflow las manda.
   - Hay que crear el seguimiento después del acceso y definir cómo se reparte entre _03a y _03b.
2. **Guía Revit + ChatGPT:** conectar «Acceso Guía Revit + IA_02» y «_03». Están hechas desde el 11-sep.
3. **DYNAMO:**
   - conectar «Acceso Pack Dynamo_02» y «_03»;
   - revisar el botón de «Acceso Pack Dynamo_01», que a un cliente de TikTok le abrió una página 404.
4. **COTIZA (antes del 13-oct):** subir a GHL los 4 correos de la secuencia S5 (`correos-nutricion.json`) y crear el workflow con la etiqueta `lead-cotizador`:
   1. Tu cotizador de honorarios (y el primer número que cambiar)
   2. Lo que no está en tu propuesta te lo piden gratis
   3. Lo caro no es el curso
   4. ¿Cuánto te salió?
5. **ACERO (5 verificaciones):**
   - Hoy recibe solo el acceso y la reactivación genérica: «Hace tiempo que no te escribo», «¿En qué nivel BIM estás realmente?» y «¿Seguimos en contacto o te dejo tranquilo?».
   - No tiene secuencia propia. La escribe Claude y la monta Ester, con puente a la Especialización a $225 (el precio solo va en correo a la lista propia).
   - Ester tiene que explicar por qué «✅ Seguimientos 1,2,3 y 4 Especialización Acero» y «✅ (SMS) FACEBOOK FORM PRE FILTRO ACERO» pasaron a borrador el 28-sep, y si se vuelven a publicar.
6. **General:** despublicar «✅ OLD Acceso y Descarga PDF Recursos Gratis», que está publicado junto al NEW.

## Cómo se comprueba que quedó

Hay que volver a correr `scripts/seguimiento_correos_lm.py`: basta con hacer push a ese script o lanzar la Action «Seguimiento por correo». Cuando esté bien montado, cada recurso debe mostrar 2 o más correos por contacto en los que entraron después del montaje.
