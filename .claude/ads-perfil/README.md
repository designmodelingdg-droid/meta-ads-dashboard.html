# Perfil de claude-ads

`claude-ads` guarda su perfil en `~/.claude-ads/profile.json`. **Este contenedor
es efímero**: esa carpeta se pierde en cuanto termina la sesión, y entonces
cualquier `/ads` volvería a pedir industria, gasto y objetivo desde cero.

Por eso la copia buena vive aquí, versionada. Para restaurarla al empezar
una sesión nueva:

```
mkdir -p ~/.claude-ads && cp .claude/ads-perfil/profile.json ~/.claude-ads/
```

## Qué hay dentro, y de dónde salió

Nada se inventó ni se preguntó: todo se leyó de `matriz-viral/fuentes/`.

| Campo | Valor | De dónde |
|---|---|---|
| `industry` | `other` | El esquema solo admite ecommerce, local-service, real-estate, healthcare, finance, agency u other. **Formación no está en la lista**, así que va como `other`: forzarla a otra categoría traería benchmarks de un negocio que no es el nuestro. |
| `monthly_spend_usd` | 1098.54 | `fuentes/ads-insights/resumen.json`, ventana 22-jul → 20-ago-2026. Es gasto real de la Graph API, no una estimación. |
| `primary_goal` | `leads` | Tres de las cinco campañas activas persiguen lead o venta por formulario. |
| `active_platforms` | `["meta"]` | DMA solo tiene pauta en Meta. Google y TikTok quedan sin conectar a propósito. |
| `connections.meta.tier` | `export` | No hay token de Meta en la sesión — y no debe haberlo, los tokens viven como secretos del repo. La auditoría corre contra los datos ya bajados en `fuentes/ads-insights/`. |
| `preferences.language` | `es` | |

## Lo que hay que actualizar y cuándo

`monthly_spend_usd` se queda viejo solo. El workflow semanal refresca
`resumen.json` los lunes y viernes, así que conviene releerlo antes de una
auditoría:

```
python3 .claude/skills/ads/scripts/profile.py set context.monthly_spend_usd <gasto>
```

## Ojo: se solapa con `auditoria-pauta`

Ya existe el skill `auditoria-pauta`, que audita el reporte semanal de Olympus
contra la API de Meta y contra el CRM. **No hacen lo mismo y conviene no
mezclarlos:**

- `auditoria-pauta` comprueba si **el reporte de la agencia dice la verdad**.
  Es una auditoría de proveedor.
- `/ads meta` comprueba si **la cuenta está bien montada** — píxel, CAPI,
  diversidad creativa, fatiga, estructura. Es una auditoría técnica.

Lo segundo nunca se había hecho.
