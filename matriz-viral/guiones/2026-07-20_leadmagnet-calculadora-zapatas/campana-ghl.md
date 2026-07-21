# Campaña GHL — Lead magnet Calculadora de Zapatas

**Enlaces:**
- Landing (calculadora): `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/`
  *(cuando esté el funnel: `funnel.dgdesignmodeling.com/...` — reemplazar)*
- Booking (llamada): `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe`
- Merge field de GHL para el nombre: `{{contact.first_name}}`

---

## A) EMAIL (broadcast a tu lista)

**Asuntos (elige 1 — A/B si quieres):**
1. 🎁 Te regalo mi calculadora de zapatas (gratis, desde el celular)
2. Diseña una zapata aislada en 2 minutos (te la regalo)
3. Deja de dimensionar zapatas "a ojo" — toma esta herramienta

**Preview text:** Cargas, acero, verificaciones y esquema. Gratis, desde tu celular.

**Cuerpo:**
```
Hola {{contact.first_name}},

¿Cuánto te toma predimensionar una zapata aislada? ¿Media hora entre el Excel,
las verificaciones de cortante y punzonamiento, y el acero?

Te hicimos un regalo: una calculadora web GRATIS que hace todo ese proceso en
2 minutos, desde tu celular:

✅ Cargas y esfuerzo del suelo
✅ Sugerencia de dimensiones (T × S y altura h)
✅ Verificaciones de cortante y punzonamiento en vivo
✅ Acero: varillas, diámetro y espaciamiento
✅ Esquema de planta y corte, dibujado solo

👉 Ábrela gratis aquí: [ENLACE LANDING]

Es la misma metodología de nuestro curso de Diseño de Cimentaciones. Ojo: es una
herramienta de predimensionamiento — el diseño definitivo lo firma un ingeniero
responsable.

Un abrazo,
Dayana · Design Modeling Academy

PS: Esta calculadora es una probadita de algo más grande — automatizar TODO tu
flujo de proyecto con BIM + IA, no solo la zapata. Al abrirla puedes agendar una
llamada gratis con nosotros si quieres ver cómo aplicarlo a tu caso.
```
> Poner el botón/enlace grande apuntando a la landing. El PS enlaza al booking.

---

## B) WHATSAPP / SMS (broadcast corto)

```
Hola {{contact.first_name}}! 👷 En Design Modeling te regalamos nuestra
calculadora de zapatas aisladas: cargas, acero y verificaciones en 2 minutos,
desde el celular y gratis 👉 [ENLACE LANDING]
```
> WhatsApp permite un poco más largo; SMS mantenlo bajo 160 caracteres (quita la palabra "aisladas" si hace falta).

---

## C) BOT de Instagram/Facebook — palabra clave "ZAPATA"

**Disparador (Workflow GHL):** comentario en la publicación que contenga **ZAPATA**
(Trigger: *Instagram/Facebook Comment* → contains "zapata", case-insensitive).

**1. Respuesta pública al comentario (auto):**
```
¡Te acabo de escribir por DM! 📩🙌
```

**2. DM inmediato (entrega):**
```
¡Hola {{contact.first_name}}! Aquí está tu calculadora de zapatas GRATIS 👉
[ENLACE LANDING]

Es la misma metodología de nuestro curso de cimentaciones. Cualquier duda,
escríbeme por aquí. 🙌
```

**3. DM de seguimiento (+3-4 horas — re-encuadre):**
```
¿Ya la probaste? 😄 Fíjate que hace en 2 minutos lo que a mano toma media hora.

Eso mismo enseñamos a hacer con TODO tu proyecto: BIM + IA + criterio. La
tecnología te da la velocidad; el criterio profesional sigue siendo tuyo.
¿Te muestro cómo? 👇
```

**4. DM (+1 día — invitación a agendar):**
```
Muchos de nuestros alumnos pasaron de calcular a mano → a liderar proyectos como
BIM Managers.

Si quieres, agenda una llamada gratis de 30 min y te contamos cómo aplicarlo a
tu caso 👉 [ENLACE BOOKING]
```

---

## Cómo enviarla en GHL (rápido)

1. **Email/SMS broadcast:** Marketing → Emails (o Conversations → nuevo broadcast) → elige la audiencia (segmento de ingenieros/leads) → pega asunto + cuerpo → programa o "Enviar ahora".
2. **Bot de comentarios:** Automation → Workflows → New → Trigger "Instagram/Facebook Comment" (keyword: zapata) → acciones: responder comentario + enviar DM 1 + Wait 3h + DM 2 + Wait 1 día + DM 3.
3. **Etiqueta:** a todo el que entre por aquí ponle el tag `lead-calculadora-zapatas` (para medir y para la secuencia del Máster).
4. Reemplaza `[ENLACE LANDING]` y `[ENLACE BOOKING]` por los de arriba.

**Regla:** manda el email/SMS solo a contactos que dieron consentimiento. El objetivo es captar y conversar, no cerrar la venta del Máster en el mensaje.
