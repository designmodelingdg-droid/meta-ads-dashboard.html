# Automatizar GoHighLevel con navegador

## Por qué existe

La API v2 de GHL es **de solo lectura** para lo que más falta. Verificado
contra la documentación oficial el 24-ago-2026:

| | |
|---|---|
| Workflows | solo `GET /workflows/` — ni crear, ni editar, ni publicar |
| Funnels y Sites | solo tres `GET` — ninguna escritura |
| Qué plantilla usa cada workflow | **no lo expone la API**, ni leyendo |

Lo que la API no escribe, un navegador sí. Esto es esa puerta.

---

## Cómo entra sin que nadie escriba una contraseña en un chat

**El camino recomendado es `GHL_STORAGE_STATE`**: una sesión ya iniciada,
exportada a JSON y guardada como secreto del repositorio.

Es mejor que usuario y contraseña por tres razones concretas:

1. **Caduca sola.** Una sesión muere en semanas. Una contraseña de GHL no, y es
   la llave maestra: quien la tenga puede borrar la cuenta entera.
2. **Sortea el 2FA.** GHL manda un código al correo. Un navegador sin nadie
   delante no puede resolverlo, así que con usuario y contraseña la corrida
   falla en cuanto se active la verificación.
3. **Se revoca cerrando sesión**, sin cambiar nada más.

### Generarla (cinco minutos, una vez)

En tu computadora, con Node instalado:

```bash
npm install -g playwright
npx playwright open --save-storage=sesion.json https://app.gohighlevel.com/
```

Se abre un Chromium. **Entra normal**, con tu clave y tu 2FA. Cuando estés
dentro y veas la subcuenta, cierra la ventana. Queda un `sesion.json`.

Ese archivo **no va al repositorio**. Se pega tal cual en:

> Settings → Secrets and variables → Actions → New repository secret
> Name: `GHL_STORAGE_STATE` · Value: (todo el contenido de sesion.json)

Cuando caduque, la corrida lo dirá con todas las letras y se repite el proceso.

### El camino alternativo

`GHL_USER` y `GHL_PASS` como secretos. Funciona **solo si la cuenta no pide
2FA**. Si lo pide, el script lo detecta, guarda captura y te manda a generar la
sesión. No se queda colgado ni finge que funcionó.

---

## Los tres frenos, y por qué están

**1 · Simulacro por defecto.** Ninguna tarea escribe nada sin `--aplicar`. El
modo normal recorre, dice lo que haría y sale.

**2 · Verificación después de escribir.** Cada acción vuelve a **leer** la
página para confirmar. Esto no es paranoia: en julio el bot de ZAPATA marcaba
los pasos en verde y el DM no llegaba. Se perdieron unos 35 leads antes de que
alguien abriera una conversación a comprobarlo. **Un clic dado no es un cambio
guardado.**

**3 · Fallo ruidoso.** Cuando algo no aparece donde se espera, se guarda
captura y HTML en `matriz-viral/fuentes/navegador/` antes de rendirse. Si GHL
cambia un botón de sitio, se ve en la imagen en vez de adivinar.

Y un tope: ninguna corrida toca más de 25 objetos. Volver a lanzarla continúa.

---

## Las tareas

```bash
# LECTURA — el mapa que la API no da
node scripts/navegador/tareas.js mapa-flujos --limite 25

# LECTURA — inventario de páginas de Sites
node scripts/navegador/tareas.js paginas

# ESCRITURA — publicar un workflow en borrador
node scripts/navegador/tareas.js encender --flujo "NOMBRE" --aplicar

# ESCRITURA — restaurar una página de la papelera
node scripts/navegador/tareas.js restaurar-pagina --pagina "Test de Nivel BIM" --aplicar
```

Se lanzan desde **Actions → Navegador GHL → Run workflow**, que es donde viven
los secretos. En local no hay credenciales y no debe haberlas.

---

## Lo que sigue siendo mala idea, aunque ahora se pueda

Que exista el martillo no obliga a usarlo en todo.

- **No automatizar lo que se hace una vez.** Montar un workflow nuevo a mano
  toma diez minutos; escribir el script que lo monte toma horas y se rompe con
  el próximo rediseño de GHL.
- **No borrar nada por navegador.** Leer mal no rompe nada; borrar mal en un
  CRM con 1.200 oportunidades sí. Este paquete no tiene ninguna tarea de
  borrado y no debería tenerla.
- **Lo que la API sí sabe hacer, se hace por API.** Es más rápido, no se rompe
  cuando cambian un botón, y deja rastro limpio.
