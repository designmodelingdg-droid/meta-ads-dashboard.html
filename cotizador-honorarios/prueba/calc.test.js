/* Prueba del núcleo de cálculo del cotizador.
 * Extrae la función entre CALC-START y CALC-END de app.html y la compara con
 * casos resueltos a mano, operación por operación (tolerancia 1e-6 relativa).
 *   node cotizador-honorarios/prueba/calc.test.js
 */
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'app.html'), 'utf8');
const calc = src.slice(src.indexOf('/* CALC-START */'), src.indexOf('/* CALC-END */'));
const calcularCotizacion = new Function(calc + '; return calcularCotizacion;')();
let fallos = 0;
const igual = (a, b, t) => { const ok = Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(b)); console.log(`  ${ok ? 'sí' : 'NO'} · ${t}: ${a} (esperado ${b})`); if (!ok) fallos++; };
const es = (c, t) => { console.log(`  ${c ? 'sí' : 'NO'} · ${t}`); if (!c) fallos++; };

const ENT = [
  {n:'Modelo', on:true, fijas:8, por100:6}, {n:'Diseño', on:true, fijas:6, por100:5},
  {n:'Planos', on:true, fijas:8, por100:6}, {n:'Memoria', on:true, fijas:4, por100:2},
  {n:'Planilla', on:false, fijas:2, por100:2}, {n:'Coord', on:true, fijas:4, por100:0},
];
const base = {ingresoMensual:1500, costosFijos:300, horasSemana:40, pctFacturable:60,
  niveles:[120,120,120], sotanosN:0, sotanosArea:0, entregables:ENT,
  revisionesN:2, revisionesH:4, visitasN:0, visitasH:4, contingencia:15,
  modo:'m2', precioM2:5, precioFijo:0, cobraIva:true, ivaTasa:15, retenciones:[], hitos:[40,40,20]};

console.log('A · ejemplo cargado en la app (Ecuador, 3 niveles de 120 m², 5 USD/m²)');
let r = calcularCotizacion(base);
// a mano
const hFact = 40 * 52 / 12 * 0.60;                 // 104
const tarifa = (1500 + 300) / hFact;               // 17.307692...
const area = 360;
const hAlc = (8+6*3.6) + (6+5*3.6) + (8+6*3.6) + (4+2*3.6) + 4;   // 98.4
const hTot = (hAlc + 2*4) * 1.15;                  // 122.36
igual(r.horasFactMes, 104, 'horas facturables al mes');
igual(r.tarifaMin, tarifa, 'tarifa mínima por hora');
igual(r.area, area, 'área total');
igual(r.horasAlcance, hAlc, 'horas del alcance');
igual(r.horasTotal, hTot, 'horas con imprevistos');
igual(r.precioMin, hTot * tarifa, 'precio mínimo');
igual(r.precioMinM2, hTot * tarifa / area, 'precio mínimo por m²');
igual(r.precio, 1800, 'precio por m² × área');
igual(r.tarifaReal, 1800 / hTot, 'tarifa real por hora');
es(!r.cubre, 'marca NO CUBRE');
igual(r.iva, 270, 'IVA 15 %');
igual(r.total, 2070, 'total a facturar');
igual(r.hitos[0].monto, 828, 'primer hito 40 % del total');
igual(r.reparto.reduce((s,x)=>s+x.monto,0), 1800, 'el reparto por entregable suma el precio');

console.log('B · México con retenciones de persona moral, monto único, con sótano y visitas');
r = calcularCotizacion({...base, niveles:[200,180], sotanosN:1, sotanosArea:150, visitasN:3, visitasH:5,
  modo:'fijo', precioFijo:90000, ivaTasa:16,
  retenciones:[{n:'ISR', pct:10, base:'sub', on:true}, {n:'IVA', pct:200/3, base:'iva', on:true}, {n:'apagada', pct:50, base:'sub', on:false}]});
igual(r.area, 530, 'área con sótano');
igual(r.horasVisitas, 15, 'horas de visitas');
igual(r.iva, 14400, 'IVA 16 %');
igual(r.retenido, 9000 + 9600, 'ISR 10 % + 2/3 del IVA (la apagada no cuenta)');
igual(r.recibes, 104400 - 18600, 'lo que llega a la cuenta');
es(r.cubre, 'con un monto alto, CUBRE');

console.log('C · modo desde mis horas: el precio es el mínimo y cubre');
r = calcularCotizacion({...base, modo:'horas'});
igual(r.precio, r.precioMin, 'precio = mínimo');
igual(r.tarifaReal, r.tarifaMin, 'tarifa real = mínima');
es(r.cubre, 'cubre (sin error de redondeo)');

console.log('D · República Dominicana: ISR 15 % y 100 % del ITBIS, sin cobrar IVA no retiene ITBIS');
r = calcularCotizacion({...base, ivaTasa:18, retenciones:[{n:'ISR', pct:15, base:'sub', on:true}, {n:'ITBIS', pct:100, base:'iva', on:true}]});
igual(r.retenido, 1800*0.15 + 1800*0.18, 'ISR 15 % + todo el ITBIS');
r = calcularCotizacion({...base, cobraIva:false, ivaTasa:18, retenciones:[{n:'ITBIS', pct:100, base:'iva', on:true}]});
igual(r.retenido, 0, 'sin ITBIS cobrado no hay ITBIS que retener');

console.log('E · bordes');
r = calcularCotizacion({...base, niveles:[0], sotanosN:0});
es(!(r.area > 0), 'área cero no rompe');
r = calcularCotizacion({...base, pctFacturable:0});
es(!isFinite(r.tarifaMin), 'sin horas facturables la tarifa no es un número (la UI lo avisa)');
r = calcularCotizacion({...base, niveles:[-50, 100]});
igual(r.area, 100, 'un área negativa no resta');

console.log(fallos ? `\n${fallos} FALLOS` : '\nprueba OK');
process.exit(fallos ? 1 : 0);
