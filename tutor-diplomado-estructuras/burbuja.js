/* Solo caracteres ASCII en el codigo: los acentos van como \u00e1 etc. Asi se
   ven bien aunque la pagina que lo carga no declare su codificacion.

   Burbuja del Tutor IA dentro de los cursos en GoHighLevel (24-sep): el del
   Diplomado BIM Estructuras y el de la Especializacion en Acero.

   Se pega UNA linea en GHL → Productos → el Diplomado → Configuracion →
   Avanzada → «Javascript personalizado» (ver MONTAJE-GHL.md). Esa linea carga
   este archivo, y este archivo pone una burbuja abajo a la derecha que abre
   el tutor en un panel, sin salir de la clase.

   Vive aqui, y no pegado entero en GHL, para poder corregirlo sin volver a
   tocar GoHighLevel: lo que se publica en Pages le llega a la burbuja solo.

   Si alguien pega la linea en el nivel del PORTAL (que se carga en todos los
   cursos), la burbuja solo aparece en las paginas del Diplomado: se reconoce
   por el ID del producto en la direccion. El portal de GHL cambia de pagina
   sin recargar, asi que eso se vuelve a mirar cada segundo.
*/
(function () {
  if (window.__dmaTutorBurbuja) return;          // pegado dos veces: una sola burbuja
  window.__dmaTutorBurbuja = true;

  // UN archivo para los dos tutores (24-sep). La linea de GHL dice cual con
  // «?programa=acero» en la direccion del script; sin eso es el Diplomado,
  // que fue el primero en pegarse. Cada curso abre SU tutor: un alumno del
  // Acero no puede recibir respuestas con clases del Diplomado, ni al reves.
  var BASE = 'https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/';
  var PROGRAMAS = {
    diplomado: { tutor: BASE + 'tutor-diplomado-estructuras/', nombre: 'Diplomado',
                 producto: 'b252f808-ce76-40b6-ba07-b9e13e29b4f4' },
    acero:     { tutor: BASE + 'tutor-acero/', nombre: 'Acero', producto: null }
  };
  var yo = (document.currentScript && document.currentScript.src) || '';
  var P = PROGRAMAS[/[?&]programa=acero\b/.test(yo) || window.DMA_TUTOR_PROGRAMA === 'acero'
                    ? 'acero' : 'diplomado'];
  var TUTOR = P.tutor;
  // Nivel producto: se muestra donde se cargue. Nivel portal (todos los
  // cursos): solo si la linea lo pide, y solo en paginas con el ID del producto.
  var soloDiplomado = P.producto && !!window.DMA_TUTOR_SOLO_DIPLOMADO;
  var PRODUCTO = P.producto;

  var css = [
    '#dma-tb-boton{position:fixed;right:20px;bottom:20px;z-index:2147483000;width:60px;height:60px;',
    'border-radius:50%;border:2px solid #e8a04a;background:#003e5c;color:#fff;cursor:pointer;',
    'box-shadow:0 6px 20px rgba(0,30,48,.35);display:flex;align-items:center;justify-content:center;',
    'font:800 15px/1 system-ui,sans-serif;letter-spacing:.02em;transition:transform .15s}',
    '#dma-tb-boton:hover{transform:scale(1.06)}',
    '#dma-tb-boton:focus-visible{outline:3px solid #e8a04a;outline-offset:3px}',
    '#dma-tb-etiqueta{position:fixed;right:90px;bottom:34px;z-index:2147483000;background:#003e5c;',
    'color:#fff;font:600 13px/1.2 system-ui,sans-serif;padding:7px 11px;border-radius:8px;',
    'box-shadow:0 4px 14px rgba(0,30,48,.25);pointer-events:none;white-space:nowrap}',
    '#dma-tb-panel{position:fixed;right:20px;bottom:92px;z-index:2147483001;width:420px;',
    'height:min(680px,calc(100vh - 120px));background:#fafaf7;border-radius:14px;overflow:hidden;',
    'box-shadow:0 12px 40px rgba(0,30,48,.35);display:none;flex-direction:column}',
    '#dma-tb-panel.abierto{display:flex}',
    '#dma-tb-cab{display:flex;align-items:center;gap:8px;padding:8px 10px;background:#001e30;color:#fff;',
    'font:700 13px/1.2 system-ui,sans-serif}',
    '#dma-tb-cab span{flex:1}',
    '#dma-tb-cab a,#dma-tb-cab button{color:#fff;background:none;border:0;cursor:pointer;',
    'font:600 12px system-ui,sans-serif;text-decoration:none;padding:4px 6px;border-radius:6px}',
    '#dma-tb-cab a:hover,#dma-tb-cab button:hover{background:rgba(255,255,255,.12)}',
    '#dma-tb-cab button{font-size:18px;line-height:1}',
    '#dma-tb-panel iframe{flex:1;border:0;width:100%;background:#fafaf7}',
    '@media (max-width:600px){#dma-tb-panel{right:0;bottom:0;width:100%;height:100%;border-radius:0}',
    '#dma-tb-etiqueta{display:none}}',
    '@media (prefers-reduced-motion:reduce){#dma-tb-boton{transition:none}}'
  ].join('');

  var boton, etiqueta, panel, marco;

  function montar() {
    var st = document.createElement('style');
    st.id = 'dma-tb-estilo';
    st.textContent = css;
    document.head.appendChild(st);

    boton = document.createElement('button');
    boton.id = 'dma-tb-boton';
    boton.type = 'button';
    boton.setAttribute('aria-label', 'Abrir el Tutor IA del ' + P.nombre);
    boton.setAttribute('aria-expanded', 'false');
    boton.textContent = 'IA';

    etiqueta = document.createElement('div');
    etiqueta.id = 'dma-tb-etiqueta';
    etiqueta.textContent = 'Preg\u00fantale a tus clases';
    setTimeout(function () { if (etiqueta) etiqueta.style.display = 'none'; }, 8000);

    panel = document.createElement('div');
    panel.id = 'dma-tb-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Tutor IA del ' + P.nombre);
    panel.innerHTML =
      '<div id="dma-tb-cab"><span>Tutor IA \u00b7 ' + P.nombre + '</span>' +
      '<a href="' + TUTOR + '" target="_blank" rel="noopener" title="Abrir en pantalla completa">Pantalla completa \u2197</a>' +
      '<button type="button" aria-label="Cerrar el tutor">\u00d7</button></div>';

    boton.addEventListener('click', alternar);
    panel.querySelector('button').addEventListener('click', cerrar);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('abierto')) cerrar();
    });
    // Con el cursor dentro del chat, las teclas las recibe el iframe: el tutor
    // avisa con un mensaje y aqui se cierra. Solo se acepta si viene del tutor.
    window.addEventListener('message', function (e) {
      if (e.data === 'dma-tb-cerrar' && TUTOR.indexOf(e.origin) === 0) cerrar();
    });

    document.body.appendChild(panel);
    document.body.appendChild(etiqueta);
    document.body.appendChild(boton);
  }

  function abrir() {
    // El tutor se carga la primera vez que se abre: si el alumno nunca lo usa,
    // la clase no paga ni un byte ni despierta el servidor.
    if (!marco) {
      marco = document.createElement('iframe');
      marco.src = TUTOR + '?burbuja=1';
      marco.title = 'Tutor IA del ' + P.nombre;
      panel.appendChild(marco);
    }
    panel.classList.add('abierto');
    boton.setAttribute('aria-expanded', 'true');
    boton.textContent = '\u00d7';
    if (etiqueta) etiqueta.style.display = 'none';
  }

  function cerrar() {
    panel.classList.remove('abierto');
    boton.setAttribute('aria-expanded', 'false');
    boton.textContent = 'IA';
    boton.focus();
  }

  function alternar() { panel.classList.contains('abierto') ? cerrar() : abrir(); }

  function visible(si) {
    boton.style.display = si ? 'flex' : 'none';
    if (!si) { panel.classList.remove('abierto'); if (etiqueta) etiqueta.style.display = 'none'; }
  }

  function revisar() {
    visible(!soloDiplomado || location.href.indexOf(PRODUCTO) !== -1);
  }

  function arrancar() {
    montar();
    revisar();
    if (soloDiplomado) setInterval(revisar, 1000);
  }

  if (document.body) arrancar();
  else document.addEventListener('DOMContentLoaded', arrancar);
})();
