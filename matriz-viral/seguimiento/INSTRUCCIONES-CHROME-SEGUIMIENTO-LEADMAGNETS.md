# Instrucciones para el Claude de Chrome · ¿está activo el seguimiento por correo de cada lead magnet?

> Solo lectura. **No cambies, no publiques, no despubliques y no edites nada.** Si algo hay que tocar, lo anotas y lo decide Dayana.
> Lección del 30-sep: si una acción de correo tiene «Sincronizar» activado con una plantilla compartida, no la abras en modo edición.

## Qué queremos saber

Para cada lead magnet:
1. ¿Hay un workflow que le mande **correos de nutrición** (seguimiento por correo, no WhatsApp ni SMS) **después** del correo de acceso?
2. ¿Ese workflow está **publicado**?
3. ¿Cuántos correos manda, con qué esperas y qué plantillas usa?
4. ¿Cuántos inscritos activos y terminados tiene?

## Lo que ya sabemos (listado del 30-sep, por la API)

| Lead magnet | Workflow de seguimiento que creemos que existe | Estado por API |
|---|---|---|
| ZAPATA | «✅ Seguimiento Zapatas → Especialización en ACERO» | publicado |
| NIVEL | «✅ Seguimiento Test de Nivel → Máster BIM+IA» | publicado |
| MEMORIA | ninguno con su nombre; hay plantillas «Acceso Memoria de Cálculo_02», «_03a», «_03b» | ¿? |
| DYNAMO | ninguno con su nombre; hay plantillas «Acceso Pack Dynamo_02» y «_03» | ¿? |
| Guía Revit + ChatGPT | ninguno con su nombre; hay plantillas «Acceso Guía Revit + IA_02» y «_03» | ¿? |
| ACERO (5 verificaciones) | ninguno propio | ¿? |
| COTIZA | ninguno (la secuencia S5 está escrita, sin montar) | no existe |

Además, **dos workflows de Acero pasaron a borrador el 28-sep**: «✅ Seguimientos 1,2,3 y 4 Especialización Acero» y «✅ (SMS) FACEBOOK FORM PRE FILTRO ACERO». Hay que confirmarlo.

## Pasos

1. **Automatización → Workflows.** Busca por nombre, uno por uno:
   - Seguimiento Zapatas
   - Seguimiento Test de Nivel
   - Seguimientos 1,2,3 y 4 Especialización Acero
   - FACEBOOK FORM PRE FILTRO ACERO
   - NEW Acceso y Descarga PDF Recursos Gratis
   - OLD Acceso y Descarga PDF Recursos Gratis
   - Seguimiento Correo + No Calificado (Cursos)
   - Seguimiento Correo + Oportunidad Futura (Cursos)
   - Seguimiento Reactivación de la lista dormida
   - Cualquier otro que diga «Seguimiento», «Nutrición» o «Memoria», «Dynamo», «Revit», «GPT» o «Guía».
2. **Para cada uno**, anota:
   - el estado (publicado o borrador) y la fecha de la última modificación;
   - el **disparador**: qué etiqueta o formulario lo activa (por ejemplo «se añade la etiqueta lead-calculadora-zapatas»);
   - los pasos de **correo**, en orden, con la espera entre cada uno y el nombre de la plantilla. Si hay pasos de WhatsApp o SMS, solo cuéntalos, no hace falta detallarlos;
   - los inscritos: activos, terminados y totales (pestaña «Inscritos» o el contador).
3. **En «NEW Acceso y Descarga PDF Recursos Gratis»**, abre las ramas MEMORIA, DYNAMO, REVIT+CHATGPT, VERIFICACIÓN (ACERO) y COTIZADOR. Dime si, después del correo de acceso, hay **esperas y más correos**: las plantillas `_02` y `_03`. Basta con que digas sí o no por rama.
4. **Busca dónde se usan las plantillas `_02` y `_03`.** En Marketing → Correos → Plantillas, abre «Acceso Memoria de Cálculo_02», «Acceso Pack Dynamo_02» y «Acceso Guía Revit + IA_02». Si GHL muestra en qué workflows se usa cada una, anótalo. Si no lo muestra, dilo.
5. **Para los dos workflows de Acero que están en borrador**, mira en el historial quién lo cambió y cuándo, si GHL lo muestra. No lo vuelvas a publicar.

## Cómo me lo devuelves

Una tabla así, y debajo lo raro que encontraste:

| Lead magnet | Workflow de correo | Estado | Disparador | Correos (espera → plantilla) | Inscritos |
|---|---|---|---|---|---|
| ZAPATA | … | publicado / borrador | etiqueta … | 1 · inmediato → … · 2 · +2 días → … | activos X / terminados Y |

Sin datos personales: no copies nombres ni correos de contactos.
