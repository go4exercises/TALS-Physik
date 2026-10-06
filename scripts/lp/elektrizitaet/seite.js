<script>
/* Leitprogramm Elektrizität — Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Gerüst (Achsen, Leiste, Übungsrahmen) aus dem
   Mathe-Vorbild «Quadratische Funktionen» übernommen; Simulationen und
   Übungstypen für 6.2 neu. Formelzeichen, Konstanten und Beispielwerte wie
   auf Themenseite 6.2. Farben im ganzen Leitprogramm: U Bernstein, I Orange,
   R Grün, Ladung und Leistung Blau. Zahlen mit Dezimalpunkt und echtem
   Minus; in Wertanzeigen ist «·» nur Malpunkt, Trenner ist der Strichpunkt. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var NB = '\u00A0';                                     // Zahl und Einheit nicht trennen
  var E_LAD = 1.602e-19;                                 // Elementarladung wie Themenseite
  function minus(s){ return String(s).replace(/^-/, '−'); }
  /* Zahl mit n signifikanten Stellen, ohne überflüssige Nullen. Ab 10^6 und
     unter 10^-3 als Zehnerpotenz mit hochgestelltem Exponenten. */
  var HOCH = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻' };
  function hoch(p){ return String(p).split('').map(function(c){ return HOCH[c] || c; }).join(''); }
  function sig(x, n){
    n = n || 3;
    if (!isFinite(x)) return '–';
    if (Math.abs(x) < 1e-12) return '0';
    var a = Math.abs(x), k = Math.floor(Math.log10(a));
    if (a >= 1e6 || a < 1e-3){
      var m = a / Math.pow(10, k), mr = +m.toFixed(n - 1);
      if (mr >= 10){ mr = +(mr / 10).toFixed(n - 1); k++; }
      return (x < 0 ? '−' : '') + String(mr) + '·10' + hoch(k);
    }
    var d = Math.max(0, n - 1 - k), r = +a.toFixed(d);
    if (d === 0){ var q = Math.pow(10, Math.max(0, k - n + 1)); r = Math.round(a / q) * q; }
    return (x < 0 ? '−' : '') + String(r);
  }
  function zahl(x){ return minus(String(+(+x).toFixed(6))); }     // Reglerwert, wie er ist
  // «=» nur vor einem exakten Wert, «≈» vor einem gerundeten (gezeigt: text, gerechnet: x)
  function ist(x, text){ var w = parseFloat(String(text).replace('−', '-').replace(/·10(.*)$/, '')); return (/·10/.test(text) ? false : Math.abs(w - x) < 1e-9 * Math.max(1, Math.abs(x))) ? '= ' : '≈ '; }
  function fest(x, d){ var r = (+x).toFixed(d); if (/^-0(\.0+)?$/.test(r)) r = r.slice(1); return minus(r); }
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function leeren(e){ while (e.firstChild) e.removeChild(e.firstChild); }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function gl(a, b){ return Math.abs(a - b) < 1e-9; }
  function nah(a, b, rel){ return Math.abs(a - b) <= (rel || 0.006) * Math.abs(b) + 1e-300; }
  function v(s){ return '<i>' + s + '</i>'; }                      // Formelzeichen kursiv

  /* ---------- Koordinatensystem (aus dem Mathe-Vorbild, Achsennamen mit Einheit) ---------- */
  function Achsen(svg, o){
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1;
    var id = 'k' + Math.random().toString(36).slice(2, 8);
    function X(x){ return (x - x0) / (x1 - x0) * W; }
    function Y(y){ return H - (y - y0) / (y1 - y0) * H; }
    var g = el(svg, 'g', {});
    var cp = el(g, 'clipPath', { id: id }); el(cp, 'rect', { x: 0, y: 0, width: W, height: H });
    var sx = o.sx || 1, sy = o.sy || 1, i;
    for (i = Math.ceil(x0 / sx) * sx; i <= x1 + 1e-9; i += sx) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
    for (i = Math.ceil(y0 / sy) * sy; i <= y1 + 1e-9; i += sy) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    el(g, 'line', { x1: 0, y1: Y(0), x2: W, y2: Y(0), 'class': 'achse' });
    el(g, 'line', { x1: X(0), y1: 0, x2: X(0), y2: H, 'class': 'achse' });
    var pf = o.pfeil || 7;
    el(g, 'polygon', { points: W + ',' + Y(0) + ' ' + (W - pf) + ',' + (Y(0) - pf / 2) + ' ' + (W - pf) + ',' + (Y(0) + pf / 2), 'class': 'pfeil' });
    el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(0) + 13, 'text-anchor': 'middle', 'class': 'skala' }, minus(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(0) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, minus(t)); });
    var ebene = el(svg, 'g', {});
    var schilder = el(svg, 'g', {});
    el(schilder, 'text', { x: W - 3, y: Y(0) - pf - 2, 'text-anchor': 'end', 'class': 'achsname' }, o.xname || 'x');
    el(schilder, 'text', { x: X(0) + pf + 2, y: pf + 5, 'text-anchor': 'start', 'class': 'achsname' }, o.yname || 'y');
    return {
      X: X, Y: Y, ebene: ebene,
      leeren: function(){ leeren(ebene); },
      kurve: function(f, cls, a, b){
        var d = '', A = a == null ? x0 : a, B = b == null ? x1 : b;
        for (var k = 0; k <= 240; k++){ var x = A + (B - A) * k / 240, y = Math.max(y0 - 3 * (y1 - y0), Math.min(y1 + 3 * (y1 - y0), f(x)));
          d += (d ? ' L' : 'M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); }
        return el(ebene, 'path', { d: d, 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      rechteck: function(xa, ya, xb, yb, cls){
        var L = Math.min(X(xa), X(xb)), T = Math.min(Y(ya), Y(yb));
        return el(ebene, 'rect', { x: L, y: T, width: Math.abs(X(xb) - X(xa)), height: Math.abs(Y(yb) - Y(ya)), 'class': cls, 'clip-path': 'url(#' + id + ')' });
      },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      },
      text: function(x, y, s, cls, anker){ return el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': cls }, s); },
      /* Punkt mit Beschriftung «(x; y)» an der ersten freien Stelle: über links,
         unter rechts, links, rechts, über rechts, höher, unter links. Frei heisst:
         im Bild, nicht über den Achsen und ihren Namen, von keiner der Geraden in
         «hindernisse» (Funktionen x -> y) gekreuzt. Breite geschätzt: 6.6 px je
         Zeichen (11.5 px fett). Passt keine Stelle, die erste, die nur die
         Hauptgerade frei lässt; sonst die erste, die ganz im Bild liegt. */
      schild: function(x, y, cls, text, hindernisse){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        var px = X(x), py = Y(y), w = text.length * 6.6, ya = Y(0), xa = X(0);
        var lagen = [[-9, -9, 'end'], [9, 16, 'start'], [-14, 4, 'end'], [14, 4, 'start'], [9, -9, 'start'], [9, -18, 'start'], [-9, -18, 'end'], [-9, 16, 'end']];
        function frei(l, alle){
          var L = l[2] === 'end' ? px + l[0] - w : px + l[0], R = L + w, T = py + l[1] - 10, B = py + l[1] + 3;
          if (L < -2 || R > W + 2 || T < -2 || B > H + 2) return false;   // viewBox hat 4 px Rand
          if (alle == null) return true;
          if (B > ya - 3 && T < ya + 14) return false;                 // x-Achse mit Zahlen
          if (L < xa + 4 && R > xa - 22) return false;                 // y-Achse mit Zahlen
          if (T < 16 && L < xa + 60) return false;                     // Name der y-Achse
          if (B > ya - 20 && R > W - 45) return false;                 // Name der x-Achse
          var fs = alle ? hindernisse : hindernisse.slice(0, 1);
          for (var k = 0; k < fs.length; k++)
            for (var s = 0; s <= 12; s++){ var qx = L + (R - L) * s / 12, qy = Y(fs[k](x0 + qx / W * (x1 - x0))); if (qy > T - 3 && qy < B + 3) return false; }
          return true;
        }
        var wahl = null;
        for (var a = 0; a < lagen.length && !wahl; a++) if (frei(lagen[a], true)) wahl = lagen[a];
        for (var b = 0; b < lagen.length && !wahl; b++) if (frei(lagen[b], false)) wahl = lagen[b];
        for (var c = 0; c < lagen.length && !wahl; c++) if (frei(lagen[c], null)) wahl = lagen[c];
        wahl = wahl || lagen[0];
        this.punkt(x, y, cls, text, wahl[0], wahl[1], wahl[2]);
      }
    };
  }

  /* ---------- Regler und Knöpfe ----------
     Regler: input[type=range] mit data-p, data-einheit, data-stellen.
     Knopfgruppe .sim-knoepfe[data-p] mit Knöpfen [data-wert]. sim.setze() stellt
     Werte für eine Aufgabe ein, ohne «bewegt» zu setzen. */
  function Bedienung(fig, weiter){
    var r = {}, k = {}, bewegt = {}, gesehen = {};
    fig.querySelectorAll('input[type=range]').forEach(function(inp){
      r[inp.dataset.p] = inp;
      inp.addEventListener('input', function(){ bewegt[inp.dataset.p] = true; weiter(); });
    });
    fig.querySelectorAll('.sim-knoepfe[data-p]').forEach(function(gr){
      var p = gr.dataset.p;
      k[p] = gr;
      gr.querySelectorAll('button').forEach(function(b){
        b.addEventListener('click', function(){ waehle(p, b.dataset.wert); bewegt[p] = true; weiter(); });
      });
    });
    function waehle(p, w){
      k[p].dataset.wert = w;
      k[p].querySelectorAll('button').forEach(function(b){ b.classList.toggle('aktiv', b.dataset.wert === w); b.setAttribute('aria-pressed', b.dataset.wert === w); });
      gesehen[p + ':' + w] = true;
    }
    for (var p in k){ var erst = k[p].querySelector('button.aktiv') || k[p].querySelector('button'); waehle(p, erst.dataset.wert); }
    function anzeigen(){
      for (var p in r){
        var inp = r[p], s = inp.parentNode.querySelector('.regler-wert');
        if (s) s.textContent = zahl(+inp.value) + (inp.dataset.einheit ? NB + inp.dataset.einheit : '');   // wie in der Formelzeile: 1 h, nicht 1.00 h
      }
    }
    return {
      wert: function(p){ return r[p] ? +r[p].value : k[p].dataset.wert; },
      setze: function(o){ for (var p in o){ if (r[p]) r[p].value = o[p]; else waehle(p, String(o[p])); } },
      bewegt: bewegt, gesehen: function(p){ var n = 0; for (var g in gesehen) if (g.indexOf(p + ':') === 0) n++; return n; },
      zuruecksetzen: function(){ for (var g in bewegt) delete bewegt[g]; for (var h in gesehen) delete gesehen[h]; for (var p in k) gesehen[p + ':' + k[p].dataset.wert] = true; },
      anzeigen: anzeigen
    };
  }
  function rolle(fig, n){ return fig.querySelector('[data-rolle="' + n + '"]'); }
  function hilfsschalter(fig, weiter){
    var h = fig.querySelector('.hilfs-schalter input');
    if (h) h.addEventListener('change', function(){ fig.classList.toggle('ohne-hilfslinien', !h.checked); if (weiter) weiter(); });
  }

  /* ---------- Aufgabenleiste in der Simulation (aus dem Mathe-Vorbild) ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «überspringen» geht
     immer. Gelöst und übersprungen werden getrennt gezählt; am Ende führt «zu den
     offenen» zurück zu den übersprungenen Aufgaben. */
  function Leiste(fig, aufgaben, sim){
    var box = fig.querySelector('.leiste'); if (!box) return function(){};
    var n = aufgaben.length, i = 0, erledigt = {};
    box.innerHTML = '<span class="ls-nr"></span><span class="ls-text"></span><span class="ls-ok" aria-live="polite"></span><button type="button" class="ls-weiter"></button><button type="button" class="ls-neu" hidden>von vorn</button>';
    var nr = box.querySelector('.ls-nr'), tx = box.querySelector('.ls-text'), ok = box.querySelector('.ls-ok'),
        bt = box.querySelector('.ls-weiter'), bv = box.querySelector('.ls-neu');
    function anzahl(){ var k = 0; for (var j = 0; j < n; j++) if (erledigt[j]) k++; return k; }
    function offen(ab){ for (var j = ab; j < n; j++) if (!erledigt[j]) return j; return n; }
    function zeigen(){
      if (i >= n){
        var k = anzahl();
        var alt2 = box.querySelector('.ls-vergleich'); if (alt2) alt2.remove();
        ok.textContent = ''; box.classList.remove('geloest');
        if (k === n){ nr.textContent = '✓'; tx.innerHTML = 'Alle ' + n + ' Aufgaben gelöst — weiter mit dem Kontrollclip.'; bt.textContent = 'nochmals'; bv.hidden = true; box.classList.add('fertig'); }
        else { nr.textContent = k + '/' + n; tx.innerHTML = k + ' von ' + n + ' gelöst, ' + (n - k) + ' übersprungen.'; bt.textContent = 'zu den offenen ▶'; bv.hidden = false; box.classList.remove('fertig'); }
        return;
      }
      box.classList.remove('fertig'); bv.hidden = true;
      var alt = box.querySelector('.ls-vergleich'); if (alt) alt.remove();
      nr.textContent = (i + 1) + '/' + n; tx.innerHTML = aufgaben[i].text; setzen(tx);
      if (aufgaben[i].setup) aufgaben[i].setup(sim);
      pruefen();
    }
    function pruefen(){
      if (i >= n) return;
      var gut = !!aufgaben[i].ok(sim.zustand());
      if (gut) erledigt[i] = true;
      ok.textContent = erledigt[i] ? '✓' : '';
      bt.textContent = erledigt[i] ? 'Nächste ▶' : 'überspringen';
      box.classList.toggle('geloest', !!erledigt[i]);
      // Fragt der Auftrag nach einer Erklärung, zählt das ✓ nur die Bedienung:
      // Die Antwort schreibt man auf und vergleicht sie erst danach.
      var vg = box.querySelector('.ls-vergleich');
      if (erledigt[i] && aufgaben[i].vergleich && !vg){
        vg = document.createElement('details'); vg.className = 'ls-vergleich';
        vg.innerHTML = '<summary>Deine Antwort notiert? Vergleichen</summary><div>' + aufgaben[i].vergleich + '</div>';
        box.appendChild(vg); setzen(vg);
      }
    }
    function gehe(j){ i = j; if (sim.aufraeumen) sim.aufraeumen(); zeigen(); if (sim.zeichnen) sim.zeichnen(); }
    bt.addEventListener('click', function(){
      if (i >= n){ if (anzahl() === n){ erledigt = {}; gehe(0); } else gehe(offen(0)); }
      else gehe(offen(i + 1));
    });
    bv.addEventListener('click', function(){ erledigt = {}; gehe(0); });
    setTimeout(zeigen, 0);
    return pruefen;
  }

  /* ---------- Kapitel 1: Ladung und Stromstärke ----------
     Anders als die Themenseite (Animation 1, Wassermodell) zeigt die Simulation
     nur das Q-t-Diagramm: Die Steigung ist die Stromstärke, der Punkt die Ladung
     nach der Zeit t. Startwert = Beispiel im Clip: 2 A während 5 s. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var K = Achsen(svg, { w: 300, h: 260, x0: -1.6, x1: 11, y0: -4.2, y1: 31, sx: 1, sy: 5, xm: [2, 4, 6, 8, 10], ym: [10, 20, 30], xname: 't [s]', yname: 'Q [C]' });
    var ziel = null, arten = {}, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    var sim = {
      zustand: function(){ var I = B.wert('I'), t = B.wert('t'); return { I: I, t: t, Q: I * t, bewegt: B.bewegt, arten: Object.keys(arten).length }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; arten = {}; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var I = B.wert('I'), t = B.wert('t'), Q = I * t;
      B.anzeigen(); K.leeren();
      if (gl(Q, 12)) arten[I + '|' + t] = true;
      K.kurve(function(x){ return 1 * x; }, 'normal hilfslinie', 0);
      K.text(10.6, 12.2, '1 A', 'hilf-text hilfslinie', 'end');
      if (ziel != null) K.kurve(function(x){ return ziel * x; }, 'zielkurve', 0);
      K.kurve(function(x){ return I * x; }, 'kurve-i', 0);
      K.schild(t, Q, 'p-q', '(' + zahl(t) + NB + 's; ' + sig(Q) + NB + 'C)',
        [function(x){ return I * x; }, function(x){ return x; }].concat(ziel != null ? [function(x){ return ziel * x; }] : []));
      var n = Q / E_LAD;
      rolle(fig, 'formel').innerHTML =
        '<span>' + v('Q') + ' = ' + v('I') + ' · ' + v('t') + ' = ' + zahl(I) + NB + 'A · ' + zahl(t) + NB + 's ' + ist(Q, sig(Q)) + sig(Q) + NB + 'C</span>' +
        '<span>' + v('n') + ' = ' + v('Q') + ' / ' + v('e') + ' = ' + (Q > 0 ? sig(Q) + NB + 'C / (1.602·10' + hoch(-19) + NB + 'C) ≈ ' + sig(n) : '0') + '</span>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh an beiden Reglern. Was legt die Steigung der Geraden fest? Notiere deine Antwort.', ok: function(s){ return s.bewegt.I && s.bewegt.t; },
        vergleich: 'Die Steigung ist die Stromstärke: \\(I = \\dfrac{Q}{t}\\) in \\(\\text{C}/\\text{s} = \\text{A}\\). Mehr Strom heisst steilere Gerade; die Zeit verschiebt nur den Punkt auf der Geraden.' },
      { text: 'Bring in \\(4\\;\\text{s}\\) genau \\(6\\;\\text{C}\\) durch den Querschnitt. Welche Stromstärke braucht es? Notiere sie.', ok: function(s){ return gl(s.t, 4) && gl(s.I, 1.5); },
        vergleich: '\\(I = \\dfrac{Q}{t} = \\dfrac{6\\;\\text{C}}{4\\;\\text{s}} = 1.5\\;\\text{A}\\): die Steigung der Geraden, die durch den Punkt \\((4\\;\\text{s};\\ 6\\;\\text{C})\\) geht.' },
      { text: 'Stelle \\(Q = 12\\;\\text{C}\\) ein — auf zwei verschiedene Arten. Notiere beide Einstellungen: Was haben sie gemeinsam?', ok: function(s){ return s.arten >= 2; },
        vergleich: 'Zum Beispiel \\(2\\;\\text{A} \\cdot 6\\;\\text{s}\\) und \\(3\\;\\text{A} \\cdot 4\\;\\text{s}\\): Das Produkt \\(I \\cdot t\\) ist beide Male \\(12\\;\\text{C}\\). Die Punkte liegen gleich hoch, aber auf verschieden steilen Geraden.' },
      { text: 'Triff die gestrichelte Gerade. Welche Stromstärke stellt sie dar, und wie viel Ladung fliesst damit in \\(6\\;\\text{s}\\)?', setup: function(S){ ziel = 2.5; S.setze({ I: 1 }); }, ok: function(s){ return gl(s.I, 2.5); },
        vergleich: 'Die Gerade steigt in jeder Sekunde um \\(2.5\\;\\text{C}\\): \\(I = 2.5\\;\\text{A}\\). In \\(6\\;\\text{s}\\) fliessen \\(Q = 2.5\\;\\text{A} \\cdot 6\\;\\text{s} = 15\\;\\text{C}\\).' },
      { text: 'Stelle \\(Q = 1\\;\\text{C}\\) ein und lies ab, wie viele Elektronen das sind.', setup: function(S){ S.setze({ I: 2, t: 5 }); }, ok: function(s){ return gl(s.Q, 1); } },
      { text: 'In \\(10\\;\\text{s}\\) sollen rund \\(3.1 \\cdot 10^{19}\\) Elektronen durch den Querschnitt. Stelle ein. Wie gross sind Ladung und Stromstärke? Notiere beide.', ok: function(s){ return gl(s.t, 10) && gl(s.I, 0.5); },
        vergleich: '\\(Q = n \\cdot e = 3.1 \\cdot 10^{19} \\cdot 1.602 \\cdot 10^{-19}\\;\\text{C} \\approx 5\\;\\text{C}\\), also \\(I = \\dfrac{5\\;\\text{C}}{10\\;\\text{s}} = 0.5\\;\\text{A}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Leistung und Energie ----------
     Wie Animation 9 der Themenseite ein P-t-Diagramm, in dem die Rechteckfläche
     die Energie ist — aber nur mit zwei Spannungen (Autobatterie, Netz), damit die
     Aufgaben mit echten Geräten arbeiten. Bei 12 V wechselt die Leistungsachse auf
     0 bis 130 W, sonst wäre das Rechteck wenige Pixel hoch. Startwert = Clipbeispiel
     Wasserkocher (230 V, 8.7 A, 1 h ≈ 2 kWh); die Aufgaben nehmen andere Geräte. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var SKALA = {
      230: { w: 300, h: 260, x0: -0.42, x1: 3.2, y0: -360, y1: 2700, sx: 0.5, sy: 500, xm: [1, 2, 3], ym: [500, 1000, 1500, 2000, 2500], xname: 't [h]', yname: 'P [W]', hilf: 1000, hilfText: '1 kWh' },
      12:  { w: 300, h: 260, x0: -0.42, x1: 3.2, y0: -17.3, y1: 130, sx: 0.5, sy: 25, xm: [1, 2, 3], ym: [25, 50, 75, 100, 125], xname: 't [h]', yname: 'P [W]', hilf: 100, hilfText: '0.1 kWh' }
    };
    var K = null, Kfuer = null, ziel = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    var sim = {
      zustand: function(){ var U = +B.wert('U'), I = B.wert('I'), t = B.wert('t'), P = U * I; return { U: U, I: I, t: t, P: P, E: P * t / 1000, bewegt: B.bewegt }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var U = +B.wert('U'), I = B.wert('I'), t = B.wert('t'), P = U * I, E = P * t / 1000, S = SKALA[U];
      B.anzeigen();
      if (Kfuer !== U){ leeren(svg); K = Achsen(svg, S); Kfuer = U; }
      K.leeren();
      K.kurve(function(x){ return S.hilf / x; }, 'normal hilfslinie', S.hilf / S.y1 * 1.02);
      K.text(3.15, S.hilf / 3.1 + S.y1 * 0.035, S.hilfText, 'hilf-text hilfslinie', 'end');
      if (ziel) K.rechteck(0, 0, ziel.t, ziel.P, 'zielflaeche');
      if (t > 0 && P > 0) K.rechteck(0, 0, t, P, 'feld');
      K.kurve(function(){ return P; }, 'kurve-p', 0, t);
      // Dieselbe Energie überall mit derselben Rundung: drei signifikante Stellen
      var Et = sig(E) + NB + 'kWh';
      // Breit genug: Beschriftung im Rechteck; schmal: rechts daneben, auf halber Höhe
      if (t >= 0.9 && P > S.y1 * 0.1) K.text(t / 2, P / 2 - S.y1 * 0.015, 'E ' + ist(E, sig(E)) + Et, 'flaeche-text');
      else if (t > 0 && P > S.y1 * 0.1) K.text(t + 0.08, P / 2 - S.y1 * 0.015, 'E ' + ist(E, sig(E)) + Et, 'flaeche-text', 'start');
      else if (t > 0) K.text(Math.max(t, 0.9) + 0.05, P + S.y1 * 0.06, 'E ' + ist(E, sig(E)) + Et, 'flaeche-text', 'start');
      var Pt = zahl(+P.toFixed(1));
      rolle(fig, 'formel').innerHTML =
        '<span>' + v('P') + ' = ' + v('U') + ' · ' + v('I') + ' = ' + U + NB + 'V · ' + fest(I, 1) + NB + 'A = ' + Pt + NB + 'W</span>' +
        '<span>' + v('E') + ' = ' + v('P') + ' · ' + v('t') + ' = ' + zahl(+(P / 1000).toFixed(6)) + NB + 'kW · ' + zahl(t) + NB + 'h ' + ist(E, sig(E)) + Et + '</span>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh an allen Reglern. Was zeigt die Fläche des Rechtecks? Notiere deine Antwort mit Einheit.', ok: function(s){ return s.bewegt.I && s.bewegt.t; },
        vergleich: 'Die Fläche ist die Energie: Höhe mal Breite, \\(E = P \\cdot t\\), in \\(\\text{kW} \\cdot \\text{h} = \\text{kWh}\\).' },
      { text: 'Ein Bügeleisen am Netz hat \\(1600\\;\\text{W}\\). Stelle die Stromstärke ein und notiere sie.', setup: function(S){ S.setze({ U: 230, I: 4 }); }, ok: function(s){ return gl(s.U, 230) && nah(s.P, 1600, 0.01); },
        vergleich: '\\(I = \\dfrac{P}{U} = \\dfrac{1600\\;\\text{W}}{230\\;\\text{V}} \\approx 6.96\\;\\text{A}\\). Der Regler geht in Schritten von \\(0.1\\;\\text{A}\\): \\(7.0\\;\\text{A}\\) gibt \\(1610\\;\\text{W}\\).' },
      { text: 'Es läuft \\(45\\;\\text{min}\\). Stelle die Zeit ein und lies die Energie ab.', ok: function(s){ return gl(s.t, 0.75) && nah(s.P, 1600, 0.01); } },
      { text: 'Stelle \\(0.92\\;\\text{kWh}\\) in \\(2\\;\\text{h}\\) ein. Welche Leistung ist das? Vergleiche mit der Heizung aus dem Kontrollclip zu Kapitel 2.', ok: function(s){ return gl(s.U, 230) && gl(s.t, 2) && Math.abs(s.E - 0.92) < 0.005; },
        vergleich: '\\(P = \\dfrac{E}{t} = \\dfrac{0.92\\;\\text{kWh}}{2\\;\\text{h}} = 0.46\\;\\text{kW} = 460\\;\\text{W}\\), bei \\(230\\;\\text{V}\\) also \\(2\\;\\text{A}\\) — genau die Heizung aus dem Kontrollclip.' },
      { text: 'Autobatterie: \\(12\\;\\text{V}\\) und \\(5\\;\\text{A}\\). Welche Leistung? Stelle ein.', ok: function(s){ return gl(s.U, 12) && gl(s.I, 5); },
        vergleich: '\\(P = U \\cdot I = 12\\;\\text{V} \\cdot 5\\;\\text{A} = 60\\;\\text{W}\\). Für dieselbe Leistung braucht das Netz mit \\(230\\;\\text{V}\\) nur rund \\(0.26\\;\\text{A}\\).' },
      { text: 'Triff das gestrichelte Rechteck. Welche Energie stellt es dar? Notiere sie mit Einheit.', setup: function(S){ ziel = { P: 1150, t: 2.5 }; S.setze({ U: 230, I: 2, t: 1 }); }, ok: function(s){ return gl(s.U, 230) && gl(s.I, 5) && gl(s.t, 2.5); },
        vergleich: 'Höhe mal Breite: \\(E = 1.15\\;\\text{kW} \\cdot 2.5\\;\\text{h} \\approx 2.88\\;\\text{kWh}\\), mit \\(I = \\dfrac{1150\\;\\text{W}}{230\\;\\text{V}} = 5\\;\\text{A}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Widerstand eines Leiters ----------
     Wie Animation 5 der Themenseite R = ρ·l/A, aber als R-l-Diagramm: Die
     Steigung ρ/A macht sichtbar, dass Material und Querschnitt zusammen wirken.
     ρ-Werte aus der Tabelle der Themenseite. Startwert = Clipbeispiel (Eisen, 20 m, 1 mm²: 2 Ω). */
  var RHO = { Cu: 0.017, Al: 0.028, Fe: 0.10, Konst: 0.49 };
  var RHO_TEXT = { Cu: '0.017', Al: '0.028', Fe: '0.10', Konst: '0.49' };   // wie in der Tabelle: Eisen 0.10, nicht 0.1
  var STOFF = { Cu: 'Kupfer', Al: 'Aluminium', Fe: 'Eisen', Konst: 'Konstantan' };
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var K = Achsen(svg, { w: 300, h: 260, x0: -6.5, x1: 55, y0: -0.72, y1: 5.5, sx: 10, sy: 1, xm: [10, 20, 30, 40, 50], ym: [1, 2, 3, 4, 5], xname: 'l [m]', yname: 'R [Ω]' });
    var ziel = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    var sim = {
      zustand: function(){ var m = B.wert('m'), l = B.wert('l'), A = B.wert('A'); return { m: m, l: l, A: A, R: RHO[m] * l / A, k: RHO[m] / A, bewegt: B.bewegt, stoffe: B.gesehen('m') }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var m = B.wert('m'), l = B.wert('l'), A = B.wert('A'), rho = RHO[m], R = rho * l / A;
      B.anzeigen(); K.leeren();
      K.kurve(function(x){ return 0.017 * x; }, 'normal hilfslinie', 0);
      K.text(54, 0.017 * 54 + 0.22, 'Kupfer, 1 mm²', 'hilf-text hilfslinie', 'end');
      if (ziel != null) K.kurve(function(x){ return ziel * x; }, 'zielkurve', 0);
      K.kurve(function(x){ return rho / A * x; }, 'kurve-r', 0);
      var lab = '(' + l + NB + 'm; ' + sig(R) + NB + 'Ω)';
      if (R <= 5.5) K.schild(l, R, 'p-r', lab,
        [function(x){ return rho / A * x; }, function(x){ return 0.017 * x; }].concat(ziel != null ? [function(x){ return ziel * x; }] : []));
      rolle(fig, 'formel').innerHTML =
        '<span>' + v('R') + ' = ' + v('ρ') + ' · ' + v('l') + ' / ' + v('A') + ' = ' + RHO_TEXT[m] + NB + 'Ω·mm²/m · ' + l + NB + 'm / ' + zahl(A) + NB + 'mm² ' + ist(R, sig(R)) + sig(R) + NB + 'Ω</span>' +
        (R > 5.5 ? '<span class="sim-notiz">Der Punkt liegt über dem Bildrand.</span>' : '');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Probiere zwei Materialien und beide Regler. Was macht die Gerade steiler? Notiere deine Antwort.', ok: function(s){ return s.bewegt.l && s.bewegt.A && s.stoffe >= 2; },
        vergleich: 'Die Steigung ist \\(\\dfrac{\\rho}{A}\\): Ein Material mit grösserem \\(\\rho\\) oder ein kleinerer Querschnitt machen die Gerade steiler. Die Länge verschiebt nur den Punkt auf der Geraden.' },
      { text: 'Kupfer, \\(1\\;\\text{mm}^2\\): Mach den Widerstand doppelt so gross wie bei \\(10\\;\\text{m}\\) — nur mit der Länge.', setup: function(S){ S.setze({ m: 'Cu', l: 10, A: 1 }); }, ok: function(s){ return s.m === 'Cu' && gl(s.A, 1) && gl(s.l, 20); } },
      { text: 'Und jetzt wieder so klein wie bei \\(10\\;\\text{m}\\) — nur mit dem Querschnitt. Um welchen Faktor hast du ihn geändert, und warum genügt das?', ok: function(s){ return s.m === 'Cu' && gl(s.l, 20) && gl(s.A, 2); },
        vergleich: 'Verdoppelt, auf \\(2\\;\\text{mm}^2\\). In \\(R = \\rho \\cdot \\dfrac{l}{A}\\) heben sich doppelte Länge und doppelter Querschnitt auf: Der Widerstand ist wieder \\(0.17\\;\\Omega\\).' },
      { text: 'Aluminiumkabel, \\(20\\;\\text{m}\\) lang, zwei Adern zu \\(2.5\\;\\text{mm}^2\\). Stelle die ganze Leiterlänge ein und notiere den Widerstand der Leitung.', ok: function(s){ return s.m === 'Al' && gl(s.l, 40) && gl(s.A, 2.5); },
        vergleich: 'Hin und zurück sind \\(40\\;\\text{m}\\) Leiter: \\(R = 0.028\\;\\dfrac{\\Omega\\,\\text{mm}^2}{\\text{m}} \\cdot \\dfrac{40\\;\\text{m}}{2.5\\;\\text{mm}^2} \\approx 0.45\\;\\Omega\\).' },
      { text: 'Gleicher Widerstand mit Kupfer: Wie dünn darf es sein?', ok: function(s){ return s.m === 'Cu' && gl(s.l, 40) && nah(s.R, 0.028 * 40 / 2.5, 0.03); },
        vergleich: '\\(A = \\rho \\cdot \\dfrac{l}{R} = 0.017\\;\\dfrac{\\Omega\\,\\text{mm}^2}{\\text{m}} \\cdot \\dfrac{40\\;\\text{m}}{0.448\\;\\Omega} \\approx 1.5\\;\\text{mm}^2\\): Kupfer leitet besser, darum genügt ein dünnerer Draht.' },
      { text: 'Triff die gestrichelte Gerade. Welche Steigung hat sie, mit Einheit, und was bedeutet sie?', setup: function(S){ ziel = 0.2; S.setze({ m: 'Cu', A: 1 }); }, ok: function(s){ return gl(s.k, 0.2); },
        vergleich: '\\(\\dfrac{\\rho}{A} = 0.2\\;\\Omega/\\text{m}\\): Jeder Meter Draht bringt \\(0.2\\;\\Omega\\). Mit den Reglern trifft sie nur Eisen mit \\(0.5\\;\\text{mm}^2\\): \\(\\dfrac{0.10}{0.5} = 0.2\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Messen und Kennlinien (sim6, neu 06.10.2026) ----------
     Kleinspannungskreis mit idealem Amperemeter und idealem Voltmeter, je richtig
     oder falsch angeschlossen. Ideal: Das Voltmeter lässt keinen Strom durch, das
     Amperemeter hat keinen Widerstand. Darum: Voltmeter im Stromweg unterbricht
     den Kreis (I = 0, es zeigt die Quellenspannung); Amperemeter parallel zum
     Bauteil überbrückt es (Kurzschluss, im Modell keine Anzeige). Messpunkte (I; U)
     gehen in eine U-I-Kennlinie, I nach rechts in mA, U nach oben in V.
     Bauteil A 150 Ω, Bauteil B 470 Ω, Lämpchen als qualitatives Beispiel mit
     U = 50 Ω · I + 41 667 Ω/A² · I³ (Widerstand wächst mit dem Strom).
     Startwerte: 3 V, Bauteil A, beide Messgeräte falsch angeschlossen (Aufgabe 1). Clip: 9 V und 30 mA (300 Ω). */
  (function(){
    var fig = document.getElementById('sim6'); if (!fig) return;
    var svgS = fig.querySelector('svg.schalt'), svgK = fig.querySelector('svg.kennl');
    var K = Achsen(svgK, { w: 300, h: 220, x0: -12, x1: 95, y0: -1.7, y1: 13.4, sx: 10, sy: 1, xm: [20, 40, 60, 80], ym: [2, 4, 6, 8, 10, 12], xname: 'I [mA]', yname: 'U [V]' });
    var RW = { a: 150, b: 470 }, NAME = { a: 'A', b: 'B', l: 'Lämpchen' };
    var punkte = { a: [], b: [], l: [] }, meldung = '', pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    function strom(bt, U){                       // I in A
      if (bt !== 'l') return U / RW[bt];
      var I = U / 120;                            // Newton für 50·I + 41667·I³ = U
      for (var k = 0; k < 40; k++){ var f = 50 * I + 41667 * I * I * I - U, d = 50 + 3 * 41667 * I * I; I -= f / d; }
      return Math.max(0, I);
    }
    function richtig(){ return B.wert('am') === 'reihe' && B.wert('vm') === 'parallel'; }
    var sim = {
      zustand: function(){
        return { bt: B.wert('bt'), U: B.wert('U'), am: B.wert('am'), vm: B.wert('vm'), richtig: richtig(),
          n: { a: punkte.a.length, b: punkte.b.length, l: punkte.l.length },
          amGesehen: B.gesehen('am'), vmGesehen: B.gesehen('vm'), bewegt: B.bewegt };
      },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ meldung = ''; B.zuruecksetzen(); }
    };
    function draht(p){ el(svgS, 'polyline', { points: p, 'class': 'draht' }); }
    function geraet(x, y, b, wert){
      el(svgS, 'circle', { cx: x, cy: y, r: 11, 'class': 'messgeraet' });
      el(svgS, 'text', { x: x, y: y + 4.5, 'text-anchor': 'middle', 'class': 'bt-titel' }, b);
      if (wert) return wert;
    }
    function zeichnen(){
      var bt = B.wert('bt'), U = B.wert('U'), am = B.wert('am'), vm = B.wert('vm');
      B.anzeigen(); leeren(svgS);
      // Quelle links, Kreis oben y = 55, unten y = 135; Bauteil oben zwischen x = 165 und 215
      draht('30,55 30,88'); draht('30,100 30,135');
      el(svgS, 'line', { x1: 18, y1: 88, x2: 42, y2: 88, 'class': 'quelle-lang' });
      el(svgS, 'line', { x1: 24, y1: 100, x2: 36, y2: 100, 'class': 'quelle-kurz' });
      el(svgS, 'text', { x: 46, y: 98, 'class': 'bt-text' }, 'U = ' + zahl(U) + NB + 'V');
      draht('30,55 165,55'); draht('215,55 300,55 300,135 30,135');
      if (bt === 'l'){
        draht('165,55 178,55'); draht('202,55 215,55');
        el(svgS, 'circle', { cx: 190, cy: 55, r: 12, 'class': 'bauteil' });
        el(svgS, 'line', { x1: 181.5, y1: 46.5, x2: 198.5, y2: 63.5, 'class': 'draht' });
        el(svgS, 'line', { x1: 181.5, y1: 63.5, x2: 198.5, y2: 46.5, 'class': 'draht' });
      } else el(svgS, 'rect', { x: 165, y: 48, width: 50, height: 14, rx: 2, 'class': 'bauteil' });
      el(svgS, 'text', { x: 190, y: 80, 'text-anchor': 'middle', 'class': 'bt-text' }, bt === 'l' ? 'Lämpchen' : 'Bauteil ' + NAME[bt]);
      // Ideales Modell: was fliesst, was zeigen die Geräte?
      var I, Ua, Iv, kurz = am === 'parallel', offen = vm === 'reihe';
      if (offen){ I = 0; Ua = 0; Iv = U; }                 // Voltmeter im Stromweg: kein Strom, es zeigt U
      else if (kurz){ I = NaN; Ua = NaN; Iv = 0; }        // Amperemeter überbrückt das Bauteil
      else { I = strom(bt, U); Ua = I; Iv = U; }
      var tI = isNaN(Ua) ? '—' : sig(Ua * 1000) + NB + 'mA', tU = sig(Iv) + NB + 'V';
      if (am === 'reihe') geraet(95, 55, 'A');
      else { draht('160,55 160,108 179,108'); draht('201,108 220,108 220,55'); geraet(190, 108, 'A'); el(svgS, 'circle', { cx: 160, cy: 55, r: 2.5, 'class': 'knoten' }); el(svgS, 'circle', { cx: 220, cy: 55, r: 2.5, 'class': 'knoten' }); }
      if (vm === 'parallel'){ draht('155,55 155,18 179,18'); draht('201,18 225,18 225,55'); geraet(190, 18, 'V'); el(svgS, 'circle', { cx: 155, cy: 55, r: 2.5, 'class': 'knoten' }); el(svgS, 'circle', { cx: 225, cy: 55, r: 2.5, 'class': 'knoten' }); }
      else geraet(190, 135, 'V');
      // Anzeigen neben den Geräten
      if (am === 'reihe') el(svgS, 'text', { x: 95, y: 82, 'text-anchor': 'middle', 'class': 'bt-wert' }, tI);
      else el(svgS, 'text', { x: 232, y: 112, 'class': 'bt-wert' }, tI);
      if (vm === 'parallel') el(svgS, 'text', { x: 234, y: 22, 'class': 'bt-wert' }, tU);
      else el(svgS, 'text', { x: 212, y: 128, 'class': 'bt-wert' }, tU);
      // Kennlinie: Punkte je Bauteil, Linie vom Ursprung durch die Punkte
      K.leeren();
      ['a', 'b', 'l'].forEach(function(k){
        var p = punkte[k].slice().sort(function(x, y){ return x[0] - y[0]; });
        if (p.length >= 2){
          var d = 'M' + K.X(0).toFixed(1) + ' ' + K.Y(0).toFixed(1);
          p.forEach(function(q){ d += ' L' + K.X(q[0]).toFixed(1) + ' ' + K.Y(q[1]).toFixed(1); });
          el(K.ebene, 'path', { d: d, 'class': 'kennlinie kl-' + k });
        }
        p.forEach(function(q){ K.punkt(q[0], q[1], 'mp mp-' + k); });
        if (p.length){ var z = p[p.length - 1], li = k === 'l'; K.text(z[0] + (li ? -2.5 : 2.5), z[1] + (li ? 0.35 : -0.75), NAME[k], 'kl-name kl-name-' + k, li ? 'end' : 'start'); }   // Lämpchen links, die Geraden rechts unten: sie treffen sich oben rechts
      });
      if (richtig() && I > 0 && I * 1000 <= 95) el(K.ebene, 'circle', { cx: K.X(I * 1000), cy: K.Y(U), r: 6, 'class': 'mp-jetzt' });
      // Formelzeile: nur die Anzeigen und der Ansatz — R bestimmen ist die Aufgabe
      var f;
      if (offen && kurz) f = '<span>Beide Geräte falsch: Das Voltmeter im Stromweg unterbricht den Kreis, es fliesst kein Strom.</span>';
      else if (offen) f = '<span>Das Voltmeter liegt im Stromweg. Ideal lässt es keinen Strom durch: ' + v('I') + ' = 0, und es zeigt die ganze Quellenspannung.</span>';
      else if (kurz) f = '<span>Das Amperemeter liegt parallel zum Bauteil. Ideal hat es keinen Widerstand: Es überbrückt das Bauteil — ein Kurzschluss. Messen lässt sich so nichts.</span>';
      else f = '<span>Anzeigen: ' + v('U') + ' = ' + tU + '; ' + v('I') + ' = ' + tI + '</span><span>' + v('R') + ' = ' + v('U') + ' / ' + v('I') + ' — mit ' + v('I') + ' in A</span>';
      if (meldung) f += '<span class="sim-notiz">' + meldung + '</span>';
      rolle(fig, 'formel').innerHTML = f;
      pruefen();
    }
    fig.querySelector('.aktion-punkt').addEventListener('click', function(){
      var bt = B.wert('bt'), U = B.wert('U');
      if (!richtig()){ meldung = 'Erst beide Messgeräte richtig anschliessen, dann eintragen.'; zeichnen(); return; }
      var I = strom(bt, U) * 1000;
      if (U <= 0){ meldung = 'Bei 0 V fliesst kein Strom: Der Punkt liegt im Ursprung. Stelle eine Spannung ein.'; zeichnen(); return; }
      if (I > 95){ meldung = 'Dieser Punkt liegt ausserhalb des Diagramms. Nimm eine kleinere Spannung.'; zeichnen(); return; }
      punkte[bt] = punkte[bt].filter(function(q){ return Math.abs(q[1] - U) > 1e-9; });
      punkte[bt].push([I, U]); meldung = ''; zeichnen();
    });
    fig.querySelector('.aktion-loeschen').addEventListener('click', function(){ punkte = { a: [], b: [], l: [] }; meldung = ''; zeichnen(); });
    pruefen = Leiste(fig, [
      { text: 'Schliesse das Amperemeter so an, dass der Strom durch das Bauteil durch das Messgerät fliesst, und das Voltmeter an die beiden Anschlüsse des Bauteils. Begründe die Anschlüsse.', setup: function(S){ S.setze({ am: 'parallel', vm: 'reihe' }); },
        ok: function(s){ return s.richtig; },
        vergleich: 'Stromstärke ist Ladung pro Zeit durch einen Querschnitt: Der Strom muss durch das Amperemeter fliessen, also gehört es in den Stromweg (in Reihe). Spannung liegt zwischen zwei Punkten: Das Voltmeter kommt an die beiden Anschlüsse des Bauteils (parallel).' },
      { text: 'Probiere beide falschen Anschlüsse aus. Was zeigt ein Voltmeter im Stromweg? Was macht ein Amperemeter parallel zum Bauteil? Notiere.', ok: function(s){ return s.amGesehen >= 2 && s.vmGesehen >= 2; },
        vergleich: 'Das ideale Voltmeter lässt keinen Strom durch: Im Stromweg unterbricht es den Kreis, \\(I = 0\\), und es zeigt die ganze Quellenspannung. Das ideale Amperemeter hat keinen Widerstand: Parallel zum Bauteil überbrückt es dieses — ein Kurzschluss.' },
      { text: 'Bauteil A, Messgeräte richtig: Stelle \\(6\\;\\text{V}\\) ein und bestimme den Widerstand aus den Anzeigen. Notiere die Rechnung.', setup: function(S){ S.setze({ bt: 'a' }); },
        ok: function(s){ return s.bt === 'a' && gl(s.U, 6) && s.richtig; },
        vergleich: 'Das Amperemeter zeigt \\(40\\;\\text{mA} = 0.040\\;\\text{A}\\). \\(R = \\dfrac{U}{I} = \\dfrac{6\\;\\text{V}}{0.040\\;\\text{A}} = 150\\;\\Omega\\).' },
      { text: 'Trage für Bauteil A drei Messpunkte bei verschiedenen Spannungen ein. Wie liegen sie im Diagramm, und was heisst das?', setup: function(S){ S.setze({ bt: 'a', am: 'reihe', vm: 'parallel' }); },
        ok: function(s){ return s.n.a >= 3; },
        vergleich: 'Auf einer Geraden durch den Ursprung: Doppelte Spannung, doppelter Strom. \\(R = U/I\\) ist überall gleich, \\(150\\;\\Omega\\) — das Bauteil ist ohmsch. Die Steigung der Geraden ist \\(R\\).' },
      { text: 'Trage auch für Bauteil B drei Punkte ein. Welche Gerade ist steiler, und was sagt das über den Widerstand?', setup: function(S){ S.setze({ bt: 'b', am: 'reihe', vm: 'parallel' }); },
        ok: function(s){ return s.n.b >= 3 && s.n.a >= 1; },
        vergleich: 'Die Gerade von B ist steiler: Für denselben Strom braucht B mehr Spannung, also ist sein Widerstand grösser (\\(470\\;\\Omega\\)). Bei \\(I\\) nach rechts und \\(U\\) nach oben ist die Steigung der Widerstand.' },
      { text: 'Lämpchen: Trage drei Punkte bei kleiner, mittlerer und grosser Spannung ein. Ist es ein ohmsches Bauteil? Begründe.', setup: function(S){ S.setze({ bt: 'l', am: 'reihe', vm: 'parallel' }); },
        ok: function(s){ return s.n.l >= 3; },
        vergleich: 'Nein. Die Punkte liegen nicht auf einer Geraden durch den Ursprung: \\(U/I\\) wird mit steigendem Strom grösser, weil der Glühdraht heisser wird. \\(R = U/I\\) lässt sich für jeden Punkt ausrechnen, ist aber nicht konstant. (Die Kurve ist ein Beispiel, kein Messwert eines bestimmten Lämpchens.)' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Reihe und parallel (sim4, bis 06.10.2026 Kapitel 4) ----------
     Wie die Animationen 6 und 7 der Themenseite zwei Widerstände an 12 V, aber
     umschaltbar in einem Bild und mit Balken statt Strompunkten: Reihe teilt die
     Spannung, parallel den Strom. Startwerte R1 = 100 Ω, R2 = 220 Ω wie dort. */
  var U4 = 12;
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), ziel = null, treffer = {}, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    var sim = {
      zustand: function(){
        var a = B.wert('art'), R1 = B.wert('R1'), R2 = B.wert('R2'), rp = R1 * R2 / (R1 + R2), rs = R1 + R2;
        return { art: a, R1: R1, R2: R2, Rges: a === 'reihe' ? rs : rp, I: U4 / (a === 'reihe' ? rs : rp), bewegt: B.bewegt, arten: B.gesehen('art'), treffer: treffer };
      },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ treffer = {}; B.zuruecksetzen(); }
    };
    function widerstand(x, y, w, h, name, wert, senkrecht){
      el(svg, 'rect', { x: x, y: y, width: w, height: h, rx: 2, 'class': 'bauteil' });
      if (senkrecht) el(svg, 'text', { x: x + w + 6, y: y + h / 2 + 4, 'class': 'bt-text' }, name + ' = ' + wert + NB + 'Ω');
      else el(svg, 'text', { x: x + w / 2, y: y - 7, 'text-anchor': 'middle', 'class': 'bt-text' }, name + ' = ' + wert + NB + 'Ω');
    }
    function draht(p){ el(svg, 'polyline', { points: p, 'class': 'draht' }); }
    function zeichnen(){
      var a = B.wert('art'), R1 = B.wert('R1'), R2 = B.wert('R2');
      B.anzeigen(); leeren(svg);
      // Quelle links: langer Strich +, kurzer −
      draht('40,40 40,92'); draht('40,108 40,160');
      el(svg, 'line', { x1: 28, y1: 92, x2: 52, y2: 92, 'class': 'quelle-lang' });
      el(svg, 'line', { x1: 34, y1: 104, x2: 46, y2: 104, 'class': 'quelle-kurz' });
      el(svg, 'text', { x: 58, y: 101, 'class': 'bt-text' }, 'U = 12' + NB + 'V');
      var I, z1, z2, rges;
      if (a === 'reihe'){
        rges = R1 + R2; I = U4 / rges;
        draht('40,40 95,40'); widerstand(95, 32, 50, 16, 'R₁', R1); draht('145,40 195,40'); widerstand(195, 32, 50, 16, 'R₂', R2);
        draht('245,40 290,40 290,160 40,160');
        z1 = I * R1; z2 = I * R2;
        rolle(fig, 'formel').innerHTML =
          '<span>' + v('R') + '<sub>ges</sub> = ' + v('R') + '₁ + ' + v('R') + '₂ = ' + R1 + NB + 'Ω + ' + R2 + NB + 'Ω = ' + rges + NB + 'Ω</span>' +
          '<span>' + v('I') + ' = ' + v('U') + ' / ' + v('R') + '<sub>ges</sub> = 12' + NB + 'V / ' + rges + NB + 'Ω ' + ist(I * 1000, sig(I * 1000)) + sig(I * 1000) + NB + 'mA</span>' +
          '<span>' + v('U') + '₁ = ' + v('I') + ' · ' + v('R') + '₁ = ' + sig(I * 1000) + NB + 'mA · ' + R1 + NB + 'Ω ' + ist(z1, sig(z1)) + sig(z1) + NB + 'V; ' + v('U') + '₂ = ' + v('I') + ' · ' + v('R') + '₂ ' + ist(z2, sig(z2)) + sig(z2) + NB + 'V</span>';
      } else {
        rges = R1 * R2 / (R1 + R2); I = U4 / rges;
        draht('40,40 235,40'); draht('40,160 235,160');   // Drähte enden am letzten Zweig
        draht('130,40 130,62'); widerstand(122, 62, 16, 56, 'R₁', R1, true); draht('130,118 130,160');
        draht('235,40 235,62'); widerstand(227, 62, 16, 56, 'R₂', R2, true); draht('235,118 235,160');
        el(svg, 'circle', { cx: 130, cy: 40, r: 3, 'class': 'knoten' }); el(svg, 'circle', { cx: 130, cy: 160, r: 3, 'class': 'knoten' });
        z1 = U4 / R1; z2 = U4 / R2;
        rolle(fig, 'formel').innerHTML =
          '<span>' + v('R') + '<sub>ges</sub> = ' + v('R') + '₁ · ' + v('R') + '₂ / (' + v('R') + '₁ + ' + v('R') + '₂) = ' + R1 + NB + 'Ω · ' + R2 + NB + 'Ω / ' + (R1 + R2) + NB + 'Ω ' + ist(rges, sig(rges)) + sig(rges) + NB + 'Ω</span>' +
          '<span>' + v('I') + '₁ = ' + v('U') + ' / ' + v('R') + '₁ = 12' + NB + 'V / ' + R1 + NB + 'Ω ' + ist(z1 * 1000, sig(z1 * 1000)) + sig(z1 * 1000) + NB + 'mA; ' + v('I') + '₂ = 12' + NB + 'V / ' + R2 + NB + 'Ω ' + ist(z2 * 1000, sig(z2 * 1000)) + sig(z2 * 1000) + NB + 'mA</span>' +
          '<span>' + v('I') + ' = ' + v('I') + '₁ + ' + v('I') + '₂ ' + ist(I * 1000, sig(I * 1000)) + sig(I * 1000) + NB + 'mA</span>';
      }
      // Balken: Reihe teilt 12 V auf, parallel addieren sich die Teilströme
      var x0 = 40, br = 250, y = 196, ges = a === 'reihe' ? U4 : I, b1 = br * z1 / ges, b2 = br * z2 / ges;
      el(svg, 'text', { x: x0, y: y - 8, 'class': 'bt-text' }, a === 'reihe' ? 'Spannung teilt sich: U₁ + U₂ = 12 V' : 'Strom teilt sich: I₁ + I₂ = I');
      el(svg, 'rect', { x: x0, y: y, width: b1, height: 18, 'class': a === 'reihe' ? 'balken-u1' : 'balken-i1' });
      el(svg, 'rect', { x: x0 + b1, y: y, width: b2, height: 18, 'class': a === 'reihe' ? 'balken-u2' : 'balken-i2' });
      var t1 = a === 'reihe' ? sig(z1) + NB + 'V' : sig(z1 * 1000) + NB + 'mA', t2 = a === 'reihe' ? sig(z2) + NB + 'V' : sig(z2 * 1000) + NB + 'mA';
      el(svg, 'text', { x: x0 + 3, y: y + 32, 'class': 'bt-text' }, (a === 'reihe' ? 'U₁ = ' : 'I₁ = ') + t1);
      el(svg, 'text', { x: x0 + br, y: y + 32, 'text-anchor': 'end', 'class': 'bt-text' }, (a === 'reihe' ? 'U₂ = ' : 'I₂ = ') + t2);
      var s = sim.zustand();
      if (gl(s.I, 0.06)) treffer[s.art] = true;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Schalte zwischen Reihe und parallel um und zieh an \\(R_1\\) und \\(R_2\\).', ok: function(s){ return s.arten >= 2 && (s.bewegt.R1 || s.bewegt.R2); } },
      { text: 'In Reihe: Mach \\(R_\\text{ges} = 400\\;\\Omega\\). Welcher Strom fliesst dann? Notiere ihn.', setup: function(S){ S.setze({ art: 'reihe' }); }, ok: function(s){ return s.art === 'reihe' && gl(s.R1 + s.R2, 400); },
        vergleich: '\\(I = \\dfrac{12\\;\\text{V}}{400\\;\\Omega} = 30\\;\\text{mA}\\), ganz gleich, wie sich die \\(400\\;\\Omega\\) auf \\(R_1\\) und \\(R_2\\) verteilen.' },
      { text: 'In Reihe: Über \\(R_1\\) sollen nur \\(2\\;\\text{V}\\) liegen. In welchem Verhältnis stehen \\(R_1\\) und \\(R_2\\)? Notiere es.', ok: function(s){ return s.art === 'reihe' && gl(s.R2, 5 * s.R1); },
        vergleich: 'Über \\(R_2\\) liegen dann \\(10\\;\\text{V}\\). Die Spannungen teilen sich wie die Widerstände: \\(R_1 : R_2 = 2 : 10 = 1 : 5\\).' },
      { text: 'Parallel: Mach \\(R_\\text{ges} = 100\\;\\Omega\\) mit zwei gleichen Widerständen. Wie gross ist jeder, und warum?', ok: function(s){ return s.art === 'parallel' && gl(s.R1, 200) && gl(s.R2, 200); },
        vergleich: 'Je \\(200\\;\\Omega\\): Zwei gleiche Zweige halbieren den Widerstand, weil der Strom zwei gleich gute Wege hat. Durch jeden fliessen \\(60\\;\\text{mA}\\).' },
      { text: 'Parallel: Durch \\(R_2\\) soll doppelt so viel Strom fliessen wie durch \\(R_1\\). Welcher Widerstand ist der grössere? Notiere deine Antwort.', ok: function(s){ return s.art === 'parallel' && gl(s.R1, 2 * s.R2); },
        vergleich: '\\(R_1 = 2 \\cdot R_2\\): An beiden Zweigen liegen \\(12\\;\\text{V}\\), und der kleinere Widerstand lässt den grösseren Strom durch.' },
      { text: 'Stelle \\(I = 60\\;\\text{mA}\\) ein — einmal in Reihe, einmal parallel. Was ist bei beiden Einstellungen gleich?', ok: function(s){ return s.treffer.reihe && s.treffer.parallel; },
        vergleich: 'Beide Male ist \\(R_\\text{ges} = \\dfrac{12\\;\\text{V}}{60\\;\\text{mA}} = 200\\;\\Omega\\), zum Beispiel \\(100\\;\\Omega + 100\\;\\Omega\\) in Reihe und \\(400\\;\\Omega\\) parallel zu \\(400\\;\\Omega\\). Parallel braucht es grössere Widerstände, weil \\(R_\\text{ges}\\) kleiner ist als jeder einzelne.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 6: Schaltungen erkennen, begründen und prüfen (sim7, neu 06.10.2026) ----------
     Dieselben zwei Widerstände (150 Ω, 300 Ω an 6 V) in vier Zeichnungen, zwei davon
     ungewohnt. Entscheidend sind die Verbindungen, nicht die Lage: Auf Wunsch färbt die
     Simulation jeden Verbindungspunkt (alle Drähte, die ohne Bauteil dazwischen
     zusammenhängen) in einer Farbe. Werte und Proben erscheinen erst, wenn die
     Schaltungsart richtig gewählt ist. Clip: zwei 200-Ω-Widerstände an 9 V. */
  (function(){
    var fig = document.getElementById('sim7'); if (!fig) return;
    var svg = fig.querySelector('svg'), U7 = 6, R1 = 150, R2 = 300;
    var ART = { z1: 'reihe', z2: 'parallel', z3: 'parallel', z4: 'reihe' };
    var treffer = {}, letzteZ = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    var farbe = fig.querySelector('.hilfs-schalter input');
    hilfsschalter(fig, function(){ zeichnen(); });
    var sim = {
      zustand: function(){ var z = B.wert('z'); return { z: z, antwort: B.wert('antwort'), art: ART[z], farbe: farbe.checked, treffer: treffer, bewegt: B.bewegt }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ B.zuruecksetzen(); }
    };
    // Zeichnungen: Drähte je Verbindungspunkt (a am Pluspol, b am Minuspol, c zwischen den Widerständen),
    // Widerstände als [x, y, Breite, Höhe, Name, Wert, Beschriftung rechts?], Knotenpunkte als [x, y]
    var Z = {
      z1: { d: { a: ['30,40 115,40'], c: ['165,40 250,40 250,92'], b: ['250,142 250,190 30,190'] },
            r: [[115, 33, 50, 14, 'R₁', R1, false], [243, 92, 14, 50, 'R₂', R2, true]], k: [] },
      z2: { d: { a: ['30,40 95,40 95,140', '95,80 140,80', '95,140 140,140'], b: ['190,80 250,80 250,190 30,190', '190,140 250,140'] },
            r: [[140, 73, 50, 14, 'R₁', R1, false], [140, 133, 50, 14, 'R₂', R2, false]], k: [[95, 80], [250, 140]] },
      z3: { d: { a: ['30,40 110,40', '75,40 75,70 205,70 205,92'], b: ['160,40 270,40 270,190 30,190', '205,142 205,190'] },
            r: [[110, 33, 50, 14, 'R₁', R1, false], [198, 92, 14, 50, 'R₂', R2, 'links']], k: [[75, 40], [205, 190]] },
      z4: { d: { a: ['30,40 120,40 120,92'], c: ['120,142 120,165 200,165 200,142'], b: ['200,92 200,40 265,40 265,190 30,190'] },
            r: [[113, 92, 14, 50, 'R₁', R1, 'links'], [193, 92, 14, 50, 'R₂', R2, true]], k: [] }
    };
    function zeichnen(){
      var z = B.wert('z'), a = B.wert('antwort');
      if (z !== letzteZ){ if (letzteZ !== null && a !== 'offen'){ B.setze({ antwort: 'offen' }); a = 'offen'; } letzteZ = z; }
      B.anzeigen(); leeren(svg);
      var G = Z[z];
      // Quelle links: langer Strich +, kurzer −
      el(svg, 'polyline', { points: '30,40 30,108', 'class': 'draht' }); el(svg, 'polyline', { points: '30,120 30,190', 'class': 'draht' });
      el(svg, 'line', { x1: 18, y1: 108, x2: 42, y2: 108, 'class': 'quelle-lang' });
      el(svg, 'line', { x1: 24, y1: 120, x2: 36, y2: 120, 'class': 'quelle-kurz' });
      el(svg, 'text', { x: 12, y: 104, 'text-anchor': 'end', 'class': 'bt-text' }, '+');
      el(svg, 'text', { x: 46, y: 140, 'class': 'bt-text' }, U7 + NB + 'V');
      for (var n in G.d) G.d[n].forEach(function(p){
        if (farbe.checked) el(svg, 'polyline', { points: p, 'class': 'knoten-farbe knoten-' + n });
        el(svg, 'polyline', { points: p, 'class': 'draht' });
      });
      if (farbe.checked){
        el(svg, 'polyline', { points: '30,40 30,108', 'class': 'knoten-farbe knoten-a' }); el(svg, 'polyline', { points: '30,40 30,108', 'class': 'draht' });
        el(svg, 'polyline', { points: '30,120 30,190', 'class': 'knoten-farbe knoten-b' }); el(svg, 'polyline', { points: '30,120 30,190', 'class': 'draht' });
      }
      G.k.forEach(function(p){ el(svg, 'circle', { cx: p[0], cy: p[1], r: 3, 'class': 'knoten' }); });
      G.r.forEach(function(r){
        el(svg, 'rect', { x: r[0], y: r[1], width: r[2], height: r[3], rx: 2, 'class': 'bauteil' });
        if (r[6] === 'links') el(svg, 'text', { x: r[0] - 6, y: r[1] + r[3] / 2 + 4, 'text-anchor': 'end', 'class': 'bt-text' }, r[4] + ' = ' + r[5] + NB + 'Ω');
        else if (r[6]) el(svg, 'text', { x: r[0] + r[2] + 6, y: r[1] + r[3] / 2 + 4, 'class': 'bt-text' }, r[4] + ' = ' + r[5] + NB + 'Ω');
        else el(svg, 'text', { x: r[0] + r[2] / 2, y: r[1] - 7, 'text-anchor': 'middle', 'class': 'bt-text' }, r[4] + ' = ' + r[5] + NB + 'Ω');
      });
      // Auswertung
      var art = ART[z], f;
      if (a === 'offen') f = '<span>Zeichnung ' + z.slice(1) + ': In Reihe oder parallel? Verfolge, womit jeder Widerstand an beiden Enden verbunden ist.</span>';
      else if (a !== art) f = '<span>Nicht ' + (a === 'reihe' ? 'in Reihe' : 'parallel') + '. Schau nicht auf die Lage, sondern auf die Verbindungen: Wo beginnt und wo endet jeder Widerstand? Die Färbung hilft.</span>';
      else {
        treffer[z] = true;
        if (art === 'parallel'){
          var i1 = U7 / R1 * 1000, i2 = U7 / R2 * 1000, rp = R1 * R2 / (R1 + R2);
          f = '<span>Parallel: Beide Widerstände verbinden dieselben zwei Punkte, an beiden liegen ' + U7 + NB + 'V.</span>' +
              '<span>' + v('I') + '₁ = ' + U7 + NB + 'V / ' + R1 + NB + 'Ω = ' + sig(i1) + NB + 'mA; ' + v('I') + '₂ = ' + U7 + NB + 'V / ' + R2 + NB + 'Ω = ' + sig(i2) + NB + 'mA</span>' +
              '<span>Probe Ladung: ' + v('I') + ' = ' + v('I') + '₁ + ' + v('I') + '₂ = ' + sig(i1 + i2) + NB + 'mA; ' + v('R') + '<sub>ges</sub> = ' + U7 + NB + 'V / ' + sig(i1 + i2) + NB + 'mA = ' + sig(rp) + NB + 'Ω, kleiner als ' + R1 + NB + 'Ω</span>';
        } else {
          var rs = R1 + R2, I = U7 / rs, u1 = I * R1, u2 = I * R2;
          f = '<span>In Reihe: Zwischen den Widerständen liegt ein Punkt, an dem sonst nichts hängt — der Strom muss durch beide.</span>' +
              '<span>' + v('I') + ' = ' + U7 + NB + 'V / ' + rs + NB + 'Ω ' + ist(I * 1000, sig(I * 1000)) + sig(I * 1000) + NB + 'mA; ' + v('U') + '₁ = ' + sig(u1) + NB + 'V; ' + v('U') + '₂ = ' + sig(u2) + NB + 'V</span>' +
              '<span>Probe Energie: ' + v('U') + '₁ + ' + v('U') + '₂ = ' + sig(u1) + NB + 'V + ' + sig(u2) + NB + 'V = ' + sig(u1 + u2) + NB + 'V</span>';
        }
      }
      rolle(fig, 'formel').innerHTML = f;
      pruefen();
    }
    function aufgabe(z, nr, text, vergleich){
      return { text: text, setup: function(S){ S.setze({ z: z, antwort: 'offen' }); letzteZ = z; }, ok: function(s){ return !!s.treffer[z] && s.z === z && s.antwort === ART[z]; }, vergleich: vergleich };
    }
    pruefen = Leiste(fig, [
      aufgabe('z1', 1, 'Zeichnung 1: In Reihe oder parallel? Wähle und begründe mit den Verbindungen.',
        'In Reihe: \\(R_1\\) und \\(R_2\\) teilen sich nur den Punkt dazwischen, und an dem hängt sonst nichts. Jedes Coulomb muss erst durch \\(R_1\\), dann durch \\(R_2\\).'),
      aufgabe('z2', 2, 'Zeichnung 2: In Reihe oder parallel? Begründe.',
        'Parallel: Beide Widerstände beginnen am linken Draht, der zum Pluspol führt, und enden am rechten Draht zum Minuspol. Dass sie übereinander gezeichnet sind, spielt keine Rolle.'),
      aufgabe('z3', 3, 'Zeichnung 3 sieht anders aus. In Reihe oder parallel? Begründe.',
        'Parallel, obwohl \\(R_2\\) wie hinter \\(R_1\\) aussieht: Das obere Ende von \\(R_2\\) hängt über den inneren Draht am selben Punkt wie der Anfang von \\(R_1\\), das untere Ende am Draht zum Minuspol — wie das Ende von \\(R_1\\).'),
      aufgabe('z4', 4, 'Zeichnung 4: Die Widerstände stehen nebeneinander. In Reihe oder parallel? Begründe.',
        'In Reihe, obwohl sie nebeneinander stehen: Das untere Ende von \\(R_1\\) führt nur zum unteren Ende von \\(R_2\\). Dort hängt sonst nichts, also fliesst durch beide derselbe Strom.'),
      { text: 'Schalte «Verbindungspunkte färben» ein und schau alle vier Zeichnungen an. Woran erkennst du an den Farben eine Parallelschaltung? Notiere.', ok: function(s){ return s.farbe && B.gesehen('z') >= 4; },
        vergleich: 'Parallel: Beide Widerstände verbinden dieselben zwei Farben (Pluspol-Farbe und Minuspol-Farbe). In Reihe gibt es eine dritte Farbe zwischen ihnen, und an der hängt nichts anderes.' },
      { text: 'Prüfe für eine Parallelschaltung \\(I_1 + I_2 = I\\) und für eine Reihenschaltung \\(U_1 + U_2 = 6\\;\\text{V}\\). Womit begründet man jede der beiden Proben?', ok: function(s){ return (s.treffer.z2 || s.treffer.z3) && (s.treffer.z1 || s.treffer.z4); },
        vergleich: 'Ströme: Ladung bleibt erhalten — was an einer Verzweigung hineinfliesst, fliesst wieder hinaus. Spannungen: Energiebilanz — die Quelle gibt jedem Coulomb \\(6\\;\\text{J}\\) mit, und die Widerstände geben zusammen genau so viel ab.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 7: Gefahren und Schutz (sim5, bis 06.10.2026 Kapitel 5) ----------
     Rechnet wie Animation 13 der Themenseite (Wasserkocher 2000 W an 230 V,
     LS B13, FI 30 mA, Fehlerschleife 2 Ω über den Schutzleiter, 0.5 Ω beim
     Kurzschluss), zeigt aber nur das Ergebnis und kein Schaltbild mit Klemmen:
     Hier geht es um die Zuordnung «wer misst was, wer trennt wann».
     Modell (Prüfung 04.10.2026): unverzögerter FI bei sinusförmigem Fehlerstrom —
     bis 0.5·IΔn = 15 mA löst er nicht aus, darüber darf er, ab 30 mA muss er.
     LS mit Charakteristik B: magnetisch sicher ab 5·In = 65 A, Überlast nur
     thermisch (hier nicht nachgebildet). Die Ströme gelten im Moment des
     Fehlers, bevor ein Schalter trennt. Die Quelle ist geerdet; der Schutzleiter
     führt zu ihr zurück, der Körperweg über den Boden. */
  var FI = { U: 230, P: 2000, IDN: 0.030, LSN: 13, RPE: 2, RKURZ: 0.5 };
  function fiRechne(fall, RK){
    var Ilast = FI.P / FI.U, IL = Ilast, IN = Ilast, IF = 0, IK = 0;
    if (fall === 'koerper'){ IF = FI.U / RK; IL = Ilast + IF; }
    else if (fall === 'pe'){ IF = FI.U / FI.RPE; IL = Ilast + IF; }
    else if (fall === 'kurz'){ IK = FI.U / FI.RKURZ; IL = Ilast + IK; IN = IL; }
    var fak = IF / FI.IDN;
    return { IL: IL, IN: IN, dI: IF, IK: IK, fi: fak >= 1 ? 'ja' : fak > 0.5 ? 'kann' : 'nein', zeit: fak >= 5 ? '40 ms' : fak >= 2 ? '150 ms' : '300 ms', ls: IL >= 5 * FI.LSN };
  }
  function strom(I){ return I >= 100 ? fest(I, 1) + NB + 'A' : I >= 1 ? fest(I, 4) + NB + 'A' : I > 0 ? sig(I * 1000) + NB + 'mA' : '0' + NB + 'mA'; }
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg'), pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    var sim = {
      zustand: function(){ var f = B.wert('fall'), RK = B.wert('RK'), r = fiRechne(f, RK); r.fall = f; r.RK = RK; r.faelle = B.gesehen('fall'); r.bewegt = B.bewegt; return r; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ B.zuruecksetzen(); }
    };
    function kasten(x, y, w, h, titel, an, wort){
      el(svg, 'rect', { x: x, y: y, width: w, height: h, rx: 5, 'class': 'schutz ' + (an ? 'schutz-aus' : 'schutz-ein') });
      el(svg, 'text', { x: x + w / 2, y: y + 15, 'text-anchor': 'middle', 'class': 'bt-titel' }, titel);
      el(svg, 'text', { x: x + w / 2, y: y + 31, 'text-anchor': 'middle', 'class': 'bt-text' }, wort);
    }
    function zeichnen(){
      var f = B.wert('fall'), RK = B.wert('RK'), r = fiRechne(f, RK);
      B.anzeigen(); leeren(svg);
      fig.querySelector('.rk-zeile').hidden = f !== 'koerper';
      // Quelle links, ihr Sternpunkt (N) geerdet: So schliesst sich jeder Fehlerweg.
      // Leitungen: L oben, N darunter, Schutzleiter (PE) unten zurück zur Quelle
      el(svg, 'line', { x1: 14, y1: 30, x2: 14, y2: 45, 'class': 'draht' });
      el(svg, 'line', { x1: 14, y1: 65, x2: 14, y2: 80, 'class': 'draht' });
      el(svg, 'circle', { cx: 14, cy: 55, r: 10, 'class': 'bauteil' });
      el(svg, 'path', { d: 'M8 55 q3 -6 6 0 t6 0', 'class': 'draht' });
      el(svg, 'line', { x1: 14, y1: 80, x2: 14, y2: 196, 'class': 'erde' });
      el(svg, 'text', { x: 20, y: 124, 'class': 'bt-klein' }, 'Quelle geerdet');
      el(svg, 'text', { x: 24, y: 25, 'class': 'bt-titel' }, 'L'); el(svg, 'text', { x: 24, y: 75, 'class': 'bt-titel' }, 'N');
      el(svg, 'polyline', { points: '14,30 236,30', 'class': 'leiter-l' });
      el(svg, 'polyline', { points: '14,80 236,80', 'class': 'leiter-n' });
      kasten(46, 10, 64, 40, 'LS B13', r.ls, r.ls ? 'trennt' : 'bleibt ein');
      kasten(128, 10, 72, 90, 'FI 30 mA', r.fi === 'ja', r.fi === 'ja' ? 'löst aus' : r.fi === 'kann' ? 'darf' : 'bleibt ein');
      if (r.fi === 'ja') el(svg, 'text', { x: 164, y: 70, 'text-anchor': 'middle', 'class': 'bt-text' }, '≤ ' + r.zeit);
      el(svg, 'text', { x: 164, y: 90, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'vergleicht');
      // Gerät
      el(svg, 'rect', { x: 236, y: 18, width: 70, height: 76, rx: 6, 'class': 'geraet' + (f === 'normal' || f === 'kurz' ? '' : ' geraet-fehler') });
      el(svg, 'text', { x: 271, y: 52, 'text-anchor': 'middle', 'class': 'bt-text' }, 'Gerät');
      el(svg, 'text', { x: 271, y: 67, 'text-anchor': 'middle', 'class': 'bt-klein' }, '2000 W');
      if (f === 'kurz') el(svg, 'polyline', { points: '226,30 232,46 222,56 230,80', 'class': 'kurzschluss' });
      // Erde
      el(svg, 'line', { x1: 14, y1: 196, x2: 306, y2: 196, 'class': 'erde' });
      el(svg, 'text', { x: 24, y: 212, 'class': 'bt-klein' }, 'Erde');
      if (f === 'pe'){
        el(svg, 'polyline', { points: '296,94 296,178 14,178', 'class': 'leiter-pe' });
        el(svg, 'text', { x: 290, y: 170, 'text-anchor': 'end', 'class': 'bt-text' }, 'Schutzleiter PE: zurück zur Quelle');
      }
      if (f === 'koerper'){
        // Mensch: Hand am Gehäuse, Füsse auf der Erde
        el(svg, 'circle', { cx: 252, cy: 124, r: 8, 'class': 'mensch' });
        el(svg, 'polyline', { points: '252,132 252,168 242,194', 'class': 'mensch' });
        el(svg, 'polyline', { points: '252,168 262,194', 'class': 'mensch' });
        el(svg, 'polyline', { points: '252,142 268,134 280,96', 'class': 'mensch' });   // Hand am Gehäuse, Arm am Kopf vorbei
        var rk = el(svg, 'text', { x: 236, y: 152, 'text-anchor': 'end', 'class': 'bt-text' }, 'R');
        el(rk, 'tspan', { dy: 3, 'font-size': '8.5' }, 'K');
        el(rk, 'tspan', { dy: -3 }, ' = ' + fest(RK / 1000, 1) + NB + 'kΩ');
        el(svg, 'text', { x: 236, y: 168, 'text-anchor': 'end', 'class': 'bt-text' }, 'Schutzleiter fehlt');
        // Fehlerweg: Gehäuse → Arm → Körper → Füsse → Erde → geerdete Quelle
        el(svg, 'polyline', { points: '286,98 274,134 258,146 258,170 266,190 8,190 8,84', 'class': 'fehlerweg' });
        el(svg, 'text', { x: 150, y: 186, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Fehlerstrom über Körper und Erde zur Quelle');
      }
      var zeilen = [
        ['Strom hin ' + v('I') + '<sub>L</sub>', strom(r.IL)],
        ['Strom zurück ' + v('I') + '<sub>N</sub>', strom(r.IN)],
        ['Differenz Δ' + v('I'), strom(r.dI)]
      ];
      rolle(fig, 'formel').innerHTML = zeilen.map(function(z){ return '<span>' + z[0] + ': ' + z[1] + '</span>'; }).join('') +
        (f === 'koerper' ? '<span>' + v('I') + '<sub>K</sub> = ' + v('U') + ' / ' + v('R') + '<sub>K</sub> = 230' + NB + 'V / ' + RK + NB + 'Ω ' + ist(r.dI * 1000, sig(r.dI * 1000)) + sig(r.dI * 1000) + NB + 'mA</span>' : '') +
        (f !== 'normal' ? '<span class="sim-notiz">Ströme im Moment des Fehlers, bevor ein Schalter trennt. Die Kästen zeigen, welche Schutzfunktion anspricht.</span>' : '');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Wähle jeden Fall einmal und vergleiche «Strom hin» mit «Strom zurück».', ok: function(s){ return s.faelle >= 4; } },
      { text: 'Finde den Fall, in dem der FI auslöst, der Leitungsschutzschalter aber nicht. Warum bemerkt der Leitungsschutzschalter nichts?', setup: function(S){ S.setze({ fall: 'normal', RK: 1000 }); }, ok: function(s){ return s.fall === 'koerper' && s.fi === 'ja' && !s.ls; },
        vergleich: 'Mensch am Gehäuse: Bei \\(R_\\text{K} = 1\\;\\text{k}\\Omega\\) fliessen durch den Körper \\(230\\;\\text{mA}\\), in der Leitung zusammen mit dem Gerät rund \\(8.9\\;\\text{A}\\) — weniger als die \\(13\\;\\text{A}\\) des B13. Der FI dagegen sieht die \\(230\\;\\text{mA}\\), die auf dem Rückweg fehlen.' },
      { text: 'Finde den Fall, in dem nur der Leitungsschutzschalter trennt. Warum bleibt der FI ein?', ok: function(s){ return s.fall === 'kurz'; },
        vergleich: 'Beim Kurzschluss zwischen L und N fliesst der riesige Strom auf N vollständig zurück: Hin und zurück sind gleich, die Differenz ist null. Der FI sieht nichts, der Leitungsschutzschalter trennt magnetisch.' },
      { text: 'Gedankenexperiment — so hohe Werte sind am Netz unrealistisch: Erhöhe \\(R_\\text{K}\\), bis der FI nicht mehr auslösen muss. Ist der Strom dann harmlos? Notiere deine Antwort.', setup: function(S){ S.setze({ fall: 'koerper', RK: 1000 }); }, ok: function(s){ return s.fall === 'koerper' && s.fi !== 'ja'; },
        vergleich: 'Nein. Über \\(7.7\\;\\text{k}\\Omega\\) fliessen weniger als \\(30\\;\\text{mA}\\), bei \\(10\\;\\text{k}\\Omega\\) noch \\(23\\;\\text{mA}\\) — genug, dass sich die Hand verkrampft. Der FI ist zusätzlicher Schutz, keine Grenze für ungefährlichen Strom. Und trockene Haut ist kein Schutz, auf den man sich verlassen kann.' },
      { text: 'Zurück zum Modell: Trockene Haut am Netz, \\(R_\\text{K} = 1.6\\;\\text{k}\\Omega\\). Stelle ein und lies den Körperstrom ab. Wie schnell muss der FI trennen? Notiere beides.', ok: function(s){ return s.fall === 'koerper' && gl(s.RK, 1600); },
        vergleich: '\\(I_\\text{K} = \\dfrac{230\\;\\text{V}}{1600\\;\\Omega} \\approx 144\\;\\text{mA}\\): mehr als das Doppelte, aber weniger als das Fünffache von \\(30\\;\\text{mA}\\). Der FI muss spätestens nach \\(150\\;\\text{ms}\\) trennen.' },
      { text: 'Wähle den Fall mit Schutzleiter. Welche Schalter sprechen an? Notiere deine Antwort.', ok: function(s){ return s.fall === 'pe'; },
        vergleich: 'Beide. \\(115\\;\\text{A}\\) sind mehr als das Fünffache der \\(13\\;\\text{A}\\): Der LS B13 löst magnetisch aus. Und die \\(115\\;\\text{A}\\) fehlen auf dem Neutralleiter: Auch der FI spricht an. Wer zuerst öffnet, zeigt das Modell nicht — nach dem Öffnen fliesst kein Fehlerstrom mehr.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Üben mit Rückmeldung (Rahmen aus dem Mathe-Vorbild) ----------
     Jede Aufgabe würfelt neue Zahlen. Richtig ist, was auf drei signifikante
     Stellen stimmt (Toleranz 0.6 %). Jedes bekannte Fehlermuster hat eine eigene
     Rückmeldung; die Lösung erscheint nach dem zweiten Fehlversuch. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung'); if (!ALLE.length) return;
    function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
    function tz(x){ var s = String(+(+x).toPrecision(6)); if (/e/.test(s)){ var p = s.split('e'); return p[0] + ' \\cdot 10^{' + (+p[1]) + '}'; } return s; }
    function ein(x, u){ return tz(x) + '\\;\\text{' + u + '}'; }
    function zp(x){                                    // Zehnerpotenz-Schreibweise für LaTeX
      var k = Math.floor(Math.log10(Math.abs(x))), m = +(x / Math.pow(10, k)).toPrecision(3);
      if (m >= 10){ m = +(m / 10).toPrecision(3); k++; }
      return String(m) + ' \\cdot 10^{' + k + '}';
    }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)(e[-+]?\d+)?$/i.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    // Typische Fehler als Faktoren: welcher Faktor trennt die Eingabe von der Lösung?
    function faktor(e, x, f){ return nah(e, x * f, 0.006); }
    function erg(x, u){ var r = +(+x).toPrecision(3); return (Math.abs(r - x) < 1e-9 * Math.max(1, Math.abs(x)) ? '= ' : '\\approx ') + (u === 'Ω' ? tz(r) + '\\;\\Omega' : ein(r, u)); }
    // Feste Aufgaben der Seite und des Gesamttests: Zufallsübungen dürfen sie nicht treffen
    function fest_(a){ return a.join('|'); }
    function vors(v){ return v === 'µ' ? '\\mu' : '\\text{' + v + '}'; }   // µ steht in LaTeX ausserhalb von \\text

    var TYPEN = {
      /* ----- Kapitel 1 ----- */
      'ladung': { felder: ['Q'], muster: '<i>Q</i> = {Q} C',
        neu: function(){
          var mA = Math.random() < 0.5, I = mA ? zufall([120, 150, 250, 400, 600, 800]) : zufall([0.2, 0.5, 1.2, 1.5, 2, 2.5, 3]);
          var min = Math.random() < 0.5, t = min ? zufall([2, 3, 5, 10, 15, 20]) : zufall([10, 20, 30, 45, 60, 90, 120]);
          var IA = mA ? I / 1000 : I, ts = min ? t * 60 : t;
          return { Q: IA * ts, IA: IA, ts: ts, mA: mA, min: min, Ir: I, tr: t,
            text: 'Durch eine Lampe fliesst \\(I = ' + ein(I, mA ? 'mA' : 'A') + '\\) während \\(t = ' + ein(t, min ? 'min' : 's') + '\\). Welche Ladung fliesst durch einen Leiterquerschnitt?' }; },
        pruefen: function(A, e){
          var Q = e.Q;
          if (nah(Q, A.Q)) return null;
          if (A.min && A.mA && faktor(Q, A.Q, 1000 / 60)) return 'Beides umrechnen: \\(\\text{mA}\\) in \\(\\text{A}\\) und \\(\\text{min}\\) in \\(\\text{s}\\).';
          if (A.min && faktor(Q, A.Q, 1 / 60)) return 'Minuten in Sekunden: \\(' + A.tr + '\\;\\text{min} = ' + A.ts + '\\;\\text{s}\\).';
          if (A.mA && faktor(Q, A.Q, 1000)) return 'Milliampere in Ampere: durch \\(1000\\), also \\(' + tz(A.IA) + '\\;\\text{A}\\).';
          if (nah(Q, A.IA / A.ts) || nah(Q, A.ts / A.IA)) return 'Ladung ist Strom mal Zeit: \\(Q = I \\cdot t\\), nicht geteilt.';
          return 'Mit \\(Q = I \\cdot t\\) rechnen, \\(I\\) in \\(\\text{A}\\) und \\(t\\) in \\(\\text{s}\\).'; },
        fehler: function(A){
          var l = [[{ Q: String(A.IA / A.ts) }, 'nicht geteilt']];
          if (A.min) l.push([{ Q: String(A.Q / 60) }, A.mA ? null : 'Minuten']);
          if (A.mA) l.push([{ Q: String(A.Q * 1000) }, A.min ? null : 'Milliampere']);
          l.push([{ Q: String(A.Q * 1.05) }, null]);
          return l; },
        loesung: function(A){ return 'Q = I \\cdot t = ' + ein(A.IA, 'A') + ' \\cdot ' + ein(A.ts, 's') + ' ' + erg(A.Q, 'C'); } },
      'strom': { felder: ['I'], muster: '<i>I</i> = {I} A',
        neu: function(){
          var Q, min, t, ts;
          do {   // Q = t hiesse I = 1 A: dann wäre der Kehrwert dieselbe Zahl
            Q = zufall([3, 6, 12, 18, 24, 36, 45, 90, 120, 180]); min = Math.random() < 0.4;
            t = min ? zufall([1, 2, 3, 5]) : zufall([4, 5, 6, 8, 10, 12, 15, 20, 30, 60]); ts = min ? t * 60 : t;
          } while (Q === ts);
          return { I: Q / ts, Q: Q, ts: ts, min: min, tr: t,
            text: 'In \\(t = ' + ein(t, min ? 'min' : 's') + '\\) fliessen \\(Q = ' + ein(Q, 'C') + '\\) durch einen Draht. Wie gross ist die Stromstärke?' }; },
        pruefen: function(A, e){
          if (nah(e.I, A.I)) return null;
          if (nah(e.I, A.Q * A.ts)) return 'Stromstärke ist Ladung <em>pro</em> Zeit: \\(I = \\dfrac{Q}{t}\\).';
          if (nah(e.I, A.ts / A.Q)) return 'Umgekehrt: Ladung durch Zeit, nicht Zeit durch Ladung.';
          if (A.min && faktor(e.I, A.I, 60)) return 'Minuten in Sekunden umrechnen: \\(' + A.tr + '\\;\\text{min} = ' + A.ts + '\\;\\text{s}\\).';
          if (faktor(e.I, A.I, 1000)) return 'Gefragt ist die Stromstärke in Ampere, nicht in Milliampere.';
          return '\\(I = \\dfrac{Q}{t}\\) mit \\(t\\) in Sekunden.'; },
        fehler: function(A){
          var l = [[{ I: String(A.Q * A.ts) }, 'pro'], [{ I: String(A.ts / A.Q) }, 'Umgekehrt']];
          if (A.min) l.push([{ I: String(A.I * 60) }, 'Minuten']);
          return l; },
        loesung: function(A){ return 'I = \\dfrac{Q}{t} = \\dfrac{' + ein(A.Q, 'C') + '}{' + ein(A.ts, 's') + '} ' + erg(A.I, 'A'); } },
      'elektronen': { felder: ['m', 'p'], muster: '<i>n</i> = {m} · 10<sup>{p}</sup>',
        neu: function(){
          var V, w, vz;
          do { V = zufall([['n', 1e-9], ['µ', 1e-6], ['p', 1e-12]]); w = zufall([0.8, 1.6, 2.4, 3.2, 4.8, 6.4, 8]); vz = Math.random() < 0.5 ? -1 : 1; }
          while (V[0] === 'n' && (w === 4.8 || w === 8));   // Aufgabe 1a: −4.8 nC
          var Q = vz * w * V[1], n = Math.abs(Q) / E_LAD, k = Math.floor(Math.log10(n));
          return { n: n, m: +(n / Math.pow(10, k)).toPrecision(3), p: k, Q: Q, V: V, w: w, vz: vz,
            text: 'Ein Körper trägt die Ladung \\(Q = ' + (vz < 0 ? '-' : '') + tz(w) + '\\;' + vors(V[0]) + '\\text{C}\\). Wie viele Elektronen ' + (vz < 0 ? 'hat er zu viel' : 'fehlen ihm') + '? (\\(e = 1.602 \\cdot 10^{-19}\\;\\text{C}\\))' }; },
        eingabe: function(A){ return { m: String(A.m), p: String(A.p) }; },
        pruefen: function(A, e){
          var n = e.m * Math.pow(10, e.p);
          if (nah(n, A.n, 0.006)) return null;
          if (nah(n, Math.abs(A.Q) * E_LAD, 0.01)) return 'Geteilt, nicht mal: \\(n = \\dfrac{|Q|}{e}\\).';
          var r = n / A.n, k = Math.round(Math.log10(r));
          if (Math.abs(r / Math.pow(10, k) - 1) < 0.01 && k !== 0){
            if (gl(e.p, -A.p)) return 'Vorzeichen des Exponenten: Durch \\(10^{-19}\\) teilen macht die Zahl gross.';
            return 'Die Vorsilbe umrechnen: \\(1\\;' + vors(A.V[0]) + '\\text{C} = 10^{' + Math.round(Math.log10(A.V[1])) + '}\\;\\text{C}\\). Die Ziffern stimmen, die Zehnerpotenz nicht.';
          }
          return '\\(n = \\dfrac{|Q|}{e}\\) — Ziffern und Zehnerpotenz getrennt rechnen.'; },
        fehler: function(A){
          var u = Math.abs(A.Q) * E_LAD, ku = Math.floor(Math.log10(u));
          return [[{ m: String(+(u / Math.pow(10, ku)).toPrecision(3)), p: String(ku) }, 'Geteilt'],
                  [{ m: String(A.m), p: String(A.p + 3) }, 'Vorsilbe'],
                  [{ m: String(A.m), p: String(-A.p) }, 'Exponenten'],
                  [{ m: String(+(A.m * 1.1).toPrecision(3)), p: String(A.p) }, null]]; },
        loesung: function(A){ return 'n = \\dfrac{|Q|}{e} = \\dfrac{' + zp(Math.abs(A.Q)) + '\\;\\text{C}}{1.602 \\cdot 10^{-19}\\;\\text{C}} \\approx ' + zp(A.n); } },

      /* ----- Kapitel 2 ----- */
      'leistung': { felder: ['x'], muster: function(A){ return A.art === 'P' ? '<i>P</i> = {x} W' : '<i>I</i> = {x} A'; },
        neu: function(){
          if (Math.random() < 0.5){
            var U = zufall([12, 24, 230]), I = U === 230 ? zufall([0.5, 3, 4, 6.5, 8, 10]) : zufall([0.5, 2, 3.5, 5, 8]);
            // Am Netz nur eine Heizung: Für sie gilt P = U · I auch mit Effektivwerten
            return { art: 'P', x: U * I, U: U, I: I, text: (U === 230 ? 'Eine Heizung am Netz (\\(U = ' + ein(U, 'V') + '\\)) zieht' : 'Ein Gerät an einer Batterie mit \\(U = ' + ein(U, 'V') + '\\) zieht') + ' \\(I = ' + ein(I, 'A') + '\\). Welche Leistung setzt es um?' };
          }
          // Nur Geräte, die wie ein Widerstand wirken (Heizdraht): Bei Motor oder
          // Netzteil folgt der Strom nicht allein aus P und U
          var G = zufall([['Ein Wasserkocher', 2000], ['Ein Toaster', 900], ['Eine Kochplatte', 1200], ['Ein Bügeleisen', 2200], ['Ein Heizlüfter', 1500], ['Ein Heizstrahler', 800]]);
          return { art: 'I', x: G[1] / 230, U: 230, P: G[1], G: G[0], text: G[0] + ' mit \\(P = ' + ein(G[1], 'W') + '\\) läuft am Netz (\\(' + ein(230, 'V') + '\\)). Welcher Strom fliesst?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'P'){
            if (nah(e.x, A.U / A.I) || nah(e.x, A.I / A.U)) return 'Leistung ist Spannung <em>mal</em> Stromstärke: \\(P = U \\cdot I\\).';
            if (nah(e.x, A.U + A.I)) return 'Nicht addieren: \\(P = U \\cdot I\\).';
            return '\\(P = U \\cdot I\\).';
          }
          if (nah(e.x, A.P * A.U)) return 'Aus \\(P = U \\cdot I\\) folgt \\(I = \\dfrac{P}{U}\\) — durch die Spannung teilen.';
          if (nah(e.x, A.U / A.P)) return 'Umgekehrt: \\(I = \\dfrac{P}{U}\\), Leistung durch Spannung.';
          return '\\(P = U \\cdot I\\) nach \\(I\\) umstellen.'; },
        fehler: function(A){
          return A.art === 'P' ? [[{ x: String(A.U / A.I) }, 'mal'], [{ x: String(A.U + A.I) }, 'addieren'], [{ x: String(A.x * 1.1) }, null]]
                               : [[{ x: String(A.P * A.U) }, 'teilen'], [{ x: String(A.U / A.P) }, 'Umgekehrt'], [{ x: String(A.x * 1.1) }, null]]; },
        loesung: function(A){ return A.art === 'P' ? 'P = U \\cdot I = ' + ein(A.U, 'V') + ' \\cdot ' + ein(A.I, 'A') + ' = ' + ein(A.x, 'W')
                                                   : 'I = \\dfrac{P}{U} = \\dfrac{' + ein(A.P, 'W') + '}{' + ein(A.U, 'V') + '} ' + erg(A.x, 'A'); } },
      'energie': { felder: ['E'], muster: '<i>E</i> = {E} kWh',
        neu: function(){
          var G = zufall([['Ein Wasserkocher', 2000, 'min', [3, 5, 6]], ['Ein Backofen', 2500, 'min', [30, 45, 90]], ['Eine LED-Lampe', 9, 'h', [4, 5, 8]],
                          ['Ein Fernseher', 120, 'h', [2, 3, 4.5]], ['Ein Heizlüfter', 1500, 'h', [1.5, 2, 3]], ['Ein Ladegerät', 20, 'h', [2, 3, 5]]]);
          var t = zufall(G[3]), th = G[2] === 'min' ? t / 60 : t;
          return { E: G[1] / 1000 * th, P: G[1], th: th, tr: t, u: G[2],
            text: G[0] + ' mit \\(P = ' + ein(G[1], 'W') + '\\) läuft \\(' + ein(t, G[2]) + '\\). Wie viel Energie setzt das Gerät um — in Kilowattstunden?' }; },
        pruefen: function(A, e){
          if (nah(e.E, A.E)) return null;
          if (faktor(e.E, A.E, 1000)) return 'Watt in Kilowatt: durch \\(1000\\). Dann gibt Kilowatt mal Stunden Kilowattstunden.';
          if (A.u === 'min' && faktor(e.E, A.E, 60)) return 'Minuten in Stunden: \\(' + A.tr + '\\;\\text{min} = ' + tz(A.th) + '\\;\\text{h}\\).';
          if (A.u === 'min' && faktor(e.E, A.E, 60000)) return 'Beides umrechnen: \\(\\text{W}\\) in \\(\\text{kW}\\) und \\(\\text{min}\\) in \\(\\text{h}\\).';
          if (nah(e.E, A.P / 1000 / A.th)) return 'Energie ist Leistung <em>mal</em> Zeit: \\(E = P \\cdot t\\).';
          return '\\(E = P \\cdot t\\) mit \\(P\\) in \\(\\text{kW}\\) und \\(t\\) in \\(\\text{h}\\).'; },
        fehler: function(A){
          var l = [[{ E: String(A.E * 1000) }, A.u === 'min' ? null : 'Kilowatt'], [{ E: String(A.P / 1000 / A.th) }, A.th === 1 ? null : 'mal']];
          if (A.u === 'min') l.push([{ E: String(A.E * 60) }, 'Minuten']);
          return l; },
        loesung: function(A){ return 'E = P \\cdot t = ' + ein(A.P / 1000, 'kW') + ' \\cdot ' + (A.u === 'min' ? '\\dfrac{' + A.tr + '}{60}\\;\\text{h}' : ein(A.th, 'h')) + ' ' + erg(A.E, 'kWh'); } },
      'arbeit': { felder: ['x'], muster: function(A){ return A.art === 'W' ? '<i>W</i> = {x} J' : A.art === 'Wh' ? '<i>W</i> = {x} Wh' : '<i>U</i> = {x} V'; },
        neu: function(){
          var r = Math.random();
          if (r < 0.34){
            var Ua = zufall([3.7, 7.4, 11.1, 12, 36]), Qa = zufall([2, 2.5, 4, 5, 10, 14]);
            return { art: 'Wh', x: Ua * Qa, U: Ua, Q: Qa, text: 'Ein Akku ist mit \\(' + ein(Ua, 'V') + '\\) und \\(' + ein(Qa, 'Ah') + '\\) beschriftet. Wie viel Energie speichert er — in Wattstunden?' };
          }
          if (r < 0.67){
            var U = zufall([1.5, 3.7, 9, 12, 230]), Q = zufall([0.5, 2, 4, 10, 25, 60]);
            return { art: 'W', x: U * Q, U: U, Q: Q, text: 'Eine Quelle mit \\(U = ' + ein(U, 'V') + '\\) schiebt \\(Q = ' + ein(Q, 'C') + '\\) durch den Kreis. Welche Arbeit verrichtet sie an dieser Ladung?' };
          }
          var Q2, U2;
          do { Q2 = zufall([0.2, 0.5, 2, 4, 5]); U2 = zufall([1.5, 4.5, 6, 9, 12, 24]); } while (Q2 === 0.2 && U2 === 12);   // Aufgabe 2a
          return { art: 'U', x: U2, W: U2 * Q2, Q: Q2, text: 'Beim Durchlaufen eines Bauteils wird an \\(Q = ' + ein(Q2, 'C') + '\\) die Arbeit \\(W = ' + ein(+(U2 * Q2).toPrecision(6), 'J') + '\\) verrichtet. Wie gross ist die Spannung über dem Bauteil?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'Wh'){
            if (faktor(e.x, A.x, 3600)) return 'Das ist der Wert in Joule. Volt mal Amperestunden gibt direkt Wattstunden: \\(1\\;\\text{V} \\cdot 1\\;\\text{Ah} = 1\\;\\text{Wh}\\).';
            if (nah(e.x, A.U / A.Q) || nah(e.x, A.Q / A.U)) return 'Energie ist Spannung mal Ladung: \\(W = U \\cdot Q\\).';
            return '\\(W = U \\cdot Q\\) mit \\(Q\\) in \\(\\text{Ah}\\) gibt \\(W\\) in \\(\\text{Wh}\\).';
          }
          if (A.art === 'W'){
            if (nah(e.x, A.U / A.Q) || nah(e.x, A.Q / A.U)) return 'Spannung ist Energie <em>je</em> Ladung — für die ganze Ladung also mal: \\(W = U \\cdot Q\\).';
            return '\\(W = U \\cdot Q\\).';
          }
          if (nah(e.x, A.W * A.Q)) return 'Spannung ist Arbeit <em>je</em> Ladung: \\(U = \\dfrac{W}{Q}\\).';
          if (nah(e.x, A.Q / A.W)) return 'Umgekehrt: Arbeit durch Ladung.';
          return '\\(U = \\dfrac{W}{Q}\\).'; },
        fehler: function(A){
          if (A.art === 'Wh') return [[{ x: String(A.x * 3600) }, 'Joule'], [{ x: String(A.U / A.Q) }, 'mal']];
          return A.art === 'W' ? [[{ x: String(A.U / A.Q) }, 'je'], [{ x: String(A.x * 1.1) }, null]]
                               : [[{ x: String(A.W * A.Q) }, 'je'], [{ x: String(A.Q / A.W) }, 'Umgekehrt']]; },
        loesung: function(A){ if (A.art === 'Wh') return 'W = U \\cdot Q = ' + ein(A.U, 'V') + ' \\cdot ' + ein(A.Q, 'Ah') + ' ' + erg(A.x, 'Wh');
                              return A.art === 'W' ? 'W = U \\cdot Q = ' + ein(A.U, 'V') + ' \\cdot ' + ein(A.Q, 'C') + ' = ' + ein(+A.x.toPrecision(6), 'J')
                                                   : 'U = \\dfrac{W}{Q} = \\dfrac{' + ein(+A.W.toPrecision(6), 'J') + '}{' + ein(A.Q, 'C') + '} = ' + ein(A.x, 'V'); } },

      /* ----- Kapitel 3 ----- */
      'leiter': { felder: ['R'], muster: '<i>R</i> = {R} Ω',
        neu: function(){
          var m, zwei, lk, A, l;
          do {   // l = A hiesse: der vertauschte Bruch gäbe dieselbe Zahl
            m = zufall(['Cu', 'Cu', 'Al', 'Fe', 'Konst']); zwei = (m === 'Cu' || m === 'Al') && Math.random() < 0.5;
            lk = m === 'Konst' || m === 'Fe' ? zufall([0.5, 1.5, 2, 4, 5]) : zufall([10, 15, 20, 25, 40, 50, 100]);
            A = zufall([0.5, 0.75, 1, 1.5, 2.5]); l = zwei ? 2 * lk : lk;
          } while (gl(l, A) || (m === 'Cu' && zwei && lk === 15 && A === 0.75));   // Aufgabe 3a
          return { R: RHO[m] * l / A, m: m, l: l, lk: lk, A: A, zwei: zwei,
            text: (zwei
              ? 'Ein zweiadriges ' + STOFF[m] + 'kabel ist \\(' + ein(lk, 'm') + '\\) lang, jede Ader hat \\(' + ein(A, 'mm^2').replace('\\text{mm^2}', '\\text{mm}^2') + '\\).'
              : 'Ein ' + STOFF[m] + 'draht ist \\(' + ein(lk, 'm') + '\\) lang und hat den Querschnitt \\(' + ein(A, 'mm^2').replace('\\text{mm^2}', '\\text{mm}^2') + '\\).')
              + ' Widerstand? (\\(\\rho = ' + RHO[m] + '\\;\\Omega\\,\\text{mm}^2/\\text{m}\\))' }; },
        pruefen: function(A, e){
          if (nah(e.R, A.R)) return null;
          if (A.zwei && faktor(e.R, A.R, 0.5)) return 'Hin- und Rückleiter: Die Leiterlänge ist \\(2 \\cdot ' + ein(A.lk, 'm') + ' = ' + ein(A.l, 'm') + '\\).';
          if (nah(e.R, RHO[A.m] * A.A / A.l) || nah(e.R, A.l / (RHO[A.m] * A.A))) return 'Länge in den Zähler, Querschnitt in den Nenner: \\(R = \\rho \\cdot \\dfrac{l}{A}\\).';
          if (nah(e.R, RHO[A.m] * A.l * A.A)) return 'Durch den Querschnitt teilen, nicht malnehmen.';
          return '\\(R = \\rho \\cdot \\dfrac{l}{A}\\) mit \\(l\\) in \\(\\text{m}\\) und \\(A\\) in \\(\\text{mm}^2\\).'; },
        fehler: function(A){
          var l = [[{ R: String(RHO[A.m] * A.A / A.l) }, 'Zähler']];
          if (A.zwei) l.push([{ R: String(A.R / 2) }, 'Rückleiter']);
          if (!gl(A.A, 1)) l.push([{ R: String(RHO[A.m] * A.l * A.A) }, 'teilen']);
          return l; },
        loesung: function(A){ return 'R = \\rho \\cdot \\dfrac{l}{A} = ' + RHO[A.m] + '\\;\\dfrac{\\Omega\\,\\text{mm}^2}{\\text{m}} \\cdot \\dfrac{' + ein(A.l, 'm') + '}{' + tz(A.A) + '\\;\\text{mm}^2} \\approx ' + ein(+A.R.toPrecision(3), '\\Omega').replace('\\text{\\Omega}', '\\Omega'); } },
      'ohm': { felder: ['I'], muster: '<i>I</i> = {I} mA',
        neu: function(){
          var k = Math.random() < 0.5, R = k ? zufall([1, 1.5, 2.2, 4.7, 10]) : zufall([47, 100, 150, 220, 330, 470]), U = zufall([1.5, 4.5, 6, 9, 12, 24]);
          var RO = k ? R * 1000 : R;
          return { I: U / RO * 1000, U: U, R: R, RO: RO, k: k,
            text: 'An einem Widerstand \\(R = ' + tz(R) + '\\;' + (k ? '\\text{k}\\Omega' : '\\Omega') + '\\) liegt \\(U = ' + ein(U, 'V') + '\\). Welcher Strom fliesst — in Milliampere?' }; },
        pruefen: function(A, e){
          if (nah(e.I, A.I)) return null;
          if (faktor(e.I, A.I, 0.001)) return 'Das ist der Wert in Ampere. In Milliampere: mal \\(1000\\).';
          if (A.k && faktor(e.I, A.I, 1000)) return 'Kiloohm in Ohm: \\(' + tz(A.R) + '\\;\\text{k}\\Omega = ' + tz(A.RO) + '\\;\\Omega\\).';
          if (nah(e.I, A.U * A.RO) || nah(e.I, A.U * A.RO * 1000) || nah(e.I, A.U * A.R)) return 'Aus \\(U = R \\cdot I\\) folgt \\(I = \\dfrac{U}{R}\\) — teilen, nicht malnehmen.';
          if (nah(e.I, A.RO / A.U * 1000) || nah(e.I, A.R / A.U)) return 'Umgekehrt: Spannung durch Widerstand.';
          return '\\(I = \\dfrac{U}{R}\\), \\(R\\) in \\(\\Omega\\), dann in \\(\\text{mA}\\) umrechnen.'; },
        fehler: function(A){
          var l = [[{ I: String(A.I / 1000) }, 'Ampere'], [{ I: String(A.RO / A.U * 1000) }, 'Umgekehrt']];
          if (A.k) l.push([{ I: String(A.I * 1000) }, 'Kiloohm']);
          return l; },
        loesung: function(A){ return 'I = \\dfrac{U}{R} = \\dfrac{' + ein(A.U, 'V') + '}{' + tz(A.RO) + '\\;\\Omega} \\approx ' + ein(+A.I.toPrecision(3), 'mA'); } },
      'laenge': { felder: ['l'], muster: '<i>l</i> = {l} m',
        neu: function(){
          var m = zufall(['Cu', 'Al', 'Fe', 'Konst']), A = zufall(m === 'Fe' ? [0.2, 0.25, 0.5, 1] : [0.1, 0.2, 0.25, 0.5, 1]);   // nicht ρ = A
          var R = m === 'Konst' ? zufall(A === 0.5 ? [9.8, 24.5, 49] : [4.9, 9.8, 24.5, 49]) : m === 'Fe' ? zufall([2, 5, 10, 20]) : zufall([0.5, 1, 1.7, 2.8, 3.4]);   // nicht Aufgabe 3b
          return { l: R * A / RHO[m], m: m, A: A, R: R,
            text: 'Aus ' + STOFF[m] + 'draht mit \\(A = ' + tz(A) + '\\;\\text{mm}^2\\) soll ein Widerstand von \\(' + tz(R) + '\\;\\Omega\\) werden. Wie lang muss der Draht sein? (\\(\\rho = ' + RHO[m] + '\\;\\Omega\\,\\text{mm}^2/\\text{m}\\))' }; },
        pruefen: function(A, e){
          if (nah(e.l, A.l)) return null;
          if (nah(e.l, A.R * RHO[A.m] / A.A) || nah(e.l, A.R / (A.A * RHO[A.m])) || nah(e.l, A.R * RHO[A.m] * A.A)) return 'Umstellen: \\(R = \\rho \\cdot \\dfrac{l}{A}\\) mal \\(A\\), durch \\(\\rho\\) gibt \\(l = \\dfrac{R \\cdot A}{\\rho}\\).';
          if (nah(e.l, A.R * A.A)) return '\\(\\rho\\) fehlt: noch durch \\(' + RHO[A.m] + '\\) teilen.';
          return '\\(l = \\dfrac{R \\cdot A}{\\rho}\\).'; },
        fehler: function(A){ return [[{ l: String(A.R * RHO[A.m] / A.A) }, 'Umstellen'], [{ l: String(A.R * A.A) }, 'fehlt']]; },
        loesung: function(A){ return 'l = \\dfrac{R \\cdot A}{\\rho} = \\dfrac{' + tz(A.R) + '\\;\\Omega \\cdot ' + tz(A.A) + '\\;\\text{mm}^2}{' + RHO[A.m] + '\\;\\Omega\\,\\text{mm}^2/\\text{m}} \\approx ' + ein(+A.l.toPrecision(3), 'm'); } },

      /* ----- Kapitel 4: Messen und Kennlinien (neu 06.10.2026) ----- */
      'messwert': { felder: ['R'], muster: '<i>R</i> = {R} Ω',
        neu: function(){
          var U, Im, R, Ia, ok;
          do {
            U = zufall([1.5, 3, 4.5, 6, 12, 24]); Im = zufall([5, 8, 12, 15, 20, 40, 60, 75]);
            Ia = Im / 1000; R = U / Ia;
            ok = !(U === 9 && Im === 30) && !(U === 5 && Im === 25) && !(U === 6 && Im === 40)   // Clip, Kontrollfrage, Simulation
              && !nah(R / 1000, Ia / U, 0.02) && !nah(R / 1000, U * Im, 0.02) && !nah(Ia / U, U * Im, 0.02) && !nah(R, U * Im, 0.02);
          } while (!ok);
          return { R: R, U: U, Im: Im,
            text: 'Am Bauteil zeigt das Voltmeter \\(U = ' + ein(U, 'V') + '\\), das Amperemeter \\(I = ' + ein(Im, 'mA') + '\\). Wie gross ist der Widerstand des Bauteils?' }; },
        pruefen: function(A, e){
          if (nah(e.R, A.R)) return null;
          if (faktor(e.R, A.R, 0.001)) return 'Den Strom zuerst in Ampere umrechnen: \\(' + ein(A.Im, 'mA') + ' = ' + ein(A.Im / 1000, 'A') + '\\).';
          if (nah(e.R, A.Im / 1000 / A.U) || nah(e.R, A.Im / A.U)) return 'Umgekehrt: \\(R = \\dfrac{U}{I}\\), Spannung durch Stromstärke.';
          if (nah(e.R, A.U * A.Im) || nah(e.R, A.U * A.Im / 1000)) return 'Geteilt, nicht mal: \\(R = \\dfrac{U}{I}\\).';
          return '\\(R = \\dfrac{U}{I}\\) mit \\(I\\) in Ampere.'; },
        fehler: function(A){ return [[{ R: String(A.R / 1000) }, 'Ampere'], [{ R: String(A.Im / 1000 / A.U) }, 'Umgekehrt'], [{ R: String(A.U * A.Im) }, 'Geteilt']]; },
        loesung: function(A){ return 'R = \\dfrac{U}{I} = \\dfrac{' + ein(A.U, 'V') + '}{' + ein(A.Im / 1000, 'A') + '} ' + erg(A.R, 'Ω'); } },
      'kennlinie': { felder: ['I'], muster: '<i>I</i> = {I} mA',
        neu: function(){
          var U1, U2, I1;
          do { U1 = zufall([3, 4.5, 6, 9, 12]); U2 = zufall([1.5, 3, 4.5, 6, 9, 12, 15]); I1 = zufall([10, 15, 20, 30, 40, 50]); }
          while (U1 === U2 || nah(I1 * U2 / U1, I1 * U1 / U2, 0.02) || nah(I1 * U2 / U1, I1, 0.02));
          return { I: I1 * U2 / U1, I1: I1, U1: U1, U2: U2,
            text: 'Die Kennlinie eines ohmschen Bauteils geht durch den Punkt \\((' + ein(I1, 'mA') + ';\\ ' + ein(U1, 'V') + ')\\). Welcher Strom fliesst, wenn \\(' + ein(U2, 'V') + '\\) anliegen?' }; },
        pruefen: function(A, e){
          if (nah(e.I, A.I)) return null;
          if (nah(e.I, A.I1 * A.U1 / A.U2)) return 'Ohmsch heisst: Strom und Spannung sind proportional. Mehr Spannung, mehr Strom — im gleichen Verhältnis.';
          if (nah(e.I, A.I1)) return 'Bei anderer Spannung fliesst ein anderer Strom: Der Widerstand bleibt gleich, nicht der Strom.';
          if (faktor(e.I, A.I, 0.001)) return 'Gefragt ist der Strom in Milliampere.';
          return 'Erst \\(R = \\dfrac{U_1}{I_1}\\), dann \\(I = \\dfrac{U}{R}\\) — oder im Verhältnis der Spannungen.'; },
        fehler: function(A){ return [[{ I: String(A.I1 * A.U1 / A.U2) }, 'proportional'], [{ I: String(A.I1) }, 'Widerstand bleibt'], [{ I: String(A.I / 1000) }, 'Milliampere']]; },
        loesung: function(A){ var R = A.U1 / (A.I1 / 1000); return 'R = \\dfrac{' + ein(A.U1, 'V') + '}{' + ein(A.I1 / 1000, 'A') + '} ' + erg(R, 'Ω') + ',\\quad I = \\dfrac{' + ein(A.U2, 'V') + '}{' + tz(+R.toPrecision(4)) + '\\;\\Omega} ' + erg(A.I, 'mA'); } },
      'anschluss': { felder: ['g', 'w'], muster: 'Messgerät: {g:Voltmeter|Amperemeter}; angeschlossen {w:parallel zum Bauteil|im Stromweg (in Reihe)}',
        neu: function(){
          var F = zufall([
            ['die Spannung am Heizdraht eines Toasters', 'Voltmeter', 'parallel zum Bauteil'],
            ['den Strom durch eine Lampe', 'Amperemeter', 'im Stromweg (in Reihe)'],
            ['die Spannung an einer LED in einer Taschenlampe', 'Voltmeter', 'parallel zum Bauteil'],
            ['den Strom, den ein kleiner Motor aufnimmt', 'Amperemeter', 'im Stromweg (in Reihe)'],
            ['die Spannung an einem Widerstand auf dem Steckbrett', 'Voltmeter', 'parallel zum Bauteil'],
            ['den Strom durch einen Widerstand auf dem Steckbrett', 'Amperemeter', 'im Stromweg (in Reihe)']
          ]);
          if (this._letzte === F[0]) return this.neu();
          this._letzte = F[0];
          return { g: F[1], w: F[2], text: 'Du willst ' + F[0] + ' messen (Kleinspannung). Welches Messgerät, und wie schliesst du es an?' }; },
        pruefen: function(A, e){
          if (e.g === A.g && e.w === A.w) return null;
          var r = [];
          if (e.g !== A.g) r.push('Spannung misst das Voltmeter, Stromstärke das Amperemeter.');
          if (e.w !== A.w){
            if (e.w === 'im Stromweg (in Reihe)' && e.g === 'Voltmeter') r.push('Ein ideales Voltmeter lässt keinen Strom durch: Im Stromweg unterbricht es den Kreis.');
            else if (e.w === 'parallel zum Bauteil' && e.g === 'Amperemeter') r.push('Ein ideales Amperemeter hat keinen Widerstand: Parallel zum Bauteil überbrückt es dieses (Kurzschluss).');
            else r.push(A.g === 'Voltmeter' ? 'Spannung liegt zwischen zwei Punkten: an die beiden Anschlüsse, also parallel.' : 'Der Strom muss durch das Messgerät fliessen: in den Stromweg, also in Reihe.');
          }
          return r.join(' '); },
        fehler: function(A){
          var andersG = A.g === 'Voltmeter' ? 'Amperemeter' : 'Voltmeter', andersW = A.w === 'parallel zum Bauteil' ? 'im Stromweg (in Reihe)' : 'parallel zum Bauteil';
          return [[{ g: andersG, w: A.w }, 'misst das'], [{ g: A.g, w: andersW }, A.g === 'Voltmeter' ? 'unterbricht' : 'Kurzschluss']]; },
        loesung: function(A){ return '\\text{' + A.g + ', ' + A.w + '}'; } },

      /* ----- Kapitel 6: Schaltungen erkennen, begründen und prüfen (neu 06.10.2026) ----- */
      'erkennen': { felder: ['s'], muster: 'Die Widerstände sind {s:in Reihe|parallel} geschaltet.',
        neu: function(){
          var F = zufall([
            ['\\(R_1\\) verbindet Punkt A mit Punkt B. \\(R_2\\) verbindet ebenfalls A mit B.', 'parallel'],
            ['\\(R_1\\) verbindet Punkt A mit Punkt C, \\(R_2\\) verbindet C mit B. An C ist sonst nichts angeschlossen.', 'in Reihe'],
            ['Auf dem Blatt stehen \\(R_1\\) und \\(R_2\\) nebeneinander. \\(R_1\\) führt von A nach C, \\(R_2\\) von C nach B; an C hängt nichts weiter.', 'in Reihe'],
            ['\\(R_1\\) ist oben, \\(R_2\\) weit unten gezeichnet. Das linke Ende beider Widerstände hängt am Draht zum Pluspol, das rechte Ende beider am Draht zum Minuspol.', 'parallel'],
            ['Zwischen \\(R_1\\) und \\(R_2\\) gibt es keine Verzweigung: Der Strom aus der Quelle muss erst durch \\(R_1\\), dann durch \\(R_2\\).', 'in Reihe'],
            ['\\(R_1\\) und \\(R_2\\) hängen beide direkt an den zwei Polen der Quelle.', 'parallel']
          ]);
          if (this._letzte === F[0]) return this.neu();
          this._letzte = F[0];
          return { s: F[1], text: F[0] + ' Wie sind die beiden geschaltet?' }; },
        pruefen: function(A, e){
          if (e.s === A.s) return null;
          return A.s === 'parallel' ? 'Achte auf die Verbindungen, nicht auf die Lage: Verbinden beide Widerstände dieselben zwei Punkte, sind sie parallel.'
                                    : 'Achte auf die Verbindungen: Teilen sich die beiden nur einen Punkt, an dem sonst nichts hängt, muss der Strom durch beide — in Reihe.'; },
        loesung: function(A){ return '\\text{' + A.s + '}'; } },
      'knoten': { felder: ['I'], muster: '<i>I</i> = {I} mA',
        neu: function(){
          if (Math.random() < 0.6){
            var I, I1;
            do { I = zufall([60, 90, 120, 150, 250, 400]); I1 = zufall([15, 25, 35, 40, 70, 100]); } while (I1 >= I || nah(I - I1, I1, 0.02) || nah(I - I1, I / 2, 0.02));
            return { art: 'p', I: I - I1, Iges: I, I1: I1,
              text: 'In eine Verzweigung fliessen \\(' + ein(I, 'mA') + '\\) hinein. Sie teilen sich auf zwei Zweige; im ersten fliessen \\(' + ein(I1, 'mA') + '\\). Wie viel fliesst im zweiten?' };
          }
          var J = zufall([12, 20, 35, 48, 75]);
          return { art: 'r', I: J, Iges: J,
            text: 'Zwei Widerstände liegen in Reihe. Zwischen Pluspol und \\(R_1\\) misst man \\(' + ein(J, 'mA') + '\\). Wie viel fliesst zwischen \\(R_2\\) und dem Minuspol zur Quelle zurück?' }; },
        pruefen: function(A, e){
          if (nah(e.I, A.I)) return null;
          if (A.art === 'p'){
            if (nah(e.I, A.Iges + A.I1)) return 'Ladung bleibt erhalten: Was hineinfliesst, fliesst wieder hinaus. Die Zweigströme ergeben zusammen den Gesamtstrom.';
            if (nah(e.I, A.Iges)) return 'Der Gesamtstrom teilt sich auf: \\(I = I_1 + I_2\\).';
            return '\\(I_2 = I - I_1\\).';
          }
          if (e.I < A.I) return 'Strom wird nicht verbraucht: In Reihe fliesst überall derselbe Strom, auch zurück zur Quelle.';
          return 'In Reihe gibt es nur einen Weg: überall derselbe Strom.'; },
        fehler: function(A){ return A.art === 'p' ? [[{ I: String(A.Iges + A.I1) }, 'Ladung'], [{ I: String(A.Iges) }, 'teilt']] : [[{ I: '0' }, 'verbraucht'], [{ I: String(A.I / 2) }, 'verbraucht']]; },
        loesung: function(A){ return A.art === 'p' ? 'I_2 = I - I_1 = ' + ein(A.Iges, 'mA') + ' - ' + ein(A.I1, 'mA') + ' = ' + ein(A.I, 'mA') : 'I = ' + ein(A.I, 'mA') + '\\;\\text{(überall gleich)}'; } },
      'masche': { felder: ['U'], muster: '<i>U</i>₂ = {U} V',
        neu: function(){
          if (Math.random() < 0.7){
            var U, U1;
            do { U = zufall([4.5, 6, 9, 12, 24]); U1 = zufall([1.5, 2.2, 3.3, 4, 5.6, 7.5, 10]); } while (U1 >= U || nah(U - U1, U1, 0.02) || nah(U - U1, U / 2, 0.02));
            return { art: 'r', U: U - U1, Uq: U, U1: U1,
              text: 'Zwei Widerstände liegen in Reihe an \\(' + ein(U, 'V') + '\\). Über \\(R_1\\) misst man \\(' + ein(U1, 'V') + '\\). Welche Spannung liegt über \\(R_2\\)?' };
          }
          var V = zufall([4.5, 6, 9, 12]);
          return { art: 'p', U: V, Uq: V,
            text: 'Zwei verschiedene Widerstände liegen parallel an \\(' + ein(V, 'V') + '\\). Welche Spannung liegt über \\(R_2\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.U, A.U)) return null;
          if (A.art === 'r'){
            if (nah(e.U, A.Uq + A.U1)) return 'Energiebilanz: Die Quelle gibt jedem Coulomb \\(' + ein(A.Uq, 'J') + '\\) mit; zusammen geben die Widerstände genau so viel ab. \\(U = U_1 + U_2\\).';
            if (nah(e.U, A.Uq)) return 'In Reihe teilt sich die Spannung auf: \\(U = U_1 + U_2\\).';
            if (nah(e.U, A.U1)) return 'Das ist die Spannung über \\(R_1\\).';
            return '\\(U_2 = U - U_1\\).';
          }
          if (nah(e.U, A.Uq / 2)) return 'Parallel teilt sich die Spannung nicht: Beide Widerstände hängen an denselben zwei Punkten, an beiden liegt die ganze Spannung.';
          return 'Parallel liegt an beiden Widerständen dieselbe Spannung.'; },
        fehler: function(A){ return A.art === 'r' ? [[{ U: String(A.Uq + A.U1) }, 'Energiebilanz'], [{ U: String(A.Uq) }, 'teilt'], [{ U: String(A.U1) }, 'über']] : [[{ U: String(A.Uq / 2) }, 'teilt sich die Spannung nicht']]; },
        loesung: function(A){ return A.art === 'r' ? 'U_2 = U - U_1 = ' + ein(A.Uq, 'V') + ' - ' + ein(A.U1, 'V') + ' = ' + ein(+(A.U).toFixed(6), 'V') : 'U_2 = U = ' + ein(A.U, 'V'); } },

      /* ----- Kapitel 5 (bis 06.10.2026 Kapitel 4) ----- */
      'reihe': { felder: ['R', 'I'], muster: '<i>R</i><sub>ges</sub> = {R} Ω; <i>I</i> = {I} mA',
        neu: function(){
          var R1, R2, U;
          do { R1 = zufall([47, 100, 150, 220, 330, 470]); R2 = zufall([100, 150, 220, 330, 470, 680]); U = zufall([6, 9, 12, 24]); }
          while (R1 === 150 && R2 === 330 && U === 24);   // Aufgabe 4a
          return { R: R1 + R2, I: U / (R1 + R2) * 1000, R1: R1, R2: R2, U: U,
            text: '\\(R_1 = ' + R1 + '\\;\\Omega\\) und \\(R_2 = ' + R2 + '\\;\\Omega\\) liegen in Reihe an \\(U = ' + ein(U, 'V') + '\\). Gesamtwiderstand und Stromstärke?' }; },
        pruefen: function(A, e){
          var r = [];
          if (nah(e.R, A.R) && nah(e.I, A.I)) return null;
          var rp = A.R1 * A.R2 / (A.R1 + A.R2);
          if (nah(e.R, rp)) r.push('Das ist die Formel für parallel. In Reihe addieren sich die Widerstände: \\(R_\\text{ges} = R_1 + R_2\\).');
          else if (!nah(e.R, A.R)) r.push('\\(R_\\text{ges} = R_1 + R_2\\).');
          if (!nah(e.I, A.I)){
            if (nah(e.I, A.I / 1000)) r.push('Strom in Milliampere: mal \\(1000\\).');
            else if (nah(e.I, A.U / A.R1 * 1000) || nah(e.I, A.U / A.R2 * 1000)) r.push('Der Strom hängt vom Gesamtwiderstand ab: \\(I = \\dfrac{U}{R_\\text{ges}}\\).');
            else if (nah(e.I, A.U / rp * 1000) && nah(e.R, rp)) {}
            else r.push('\\(I = \\dfrac{U}{R_\\text{ges}}\\), in \\(\\text{mA}\\).');
          }
          return r.join(' '); },
        fehler: function(A){ var rp = A.R1 * A.R2 / (A.R1 + A.R2);
          return [[{ R: String(rp), I: String(A.U / rp * 1000) }, 'parallel'], [{ R: String(A.R), I: String(A.I / 1000) }, 'Milliampere'], [{ R: String(A.R), I: String(A.U / A.R1 * 1000) }, 'Gesamtwiderstand']]; },
        loesung: function(A){ return 'R_\\text{ges} = R_1 + R_2 = ' + A.R1 + '\\;\\Omega + ' + A.R2 + '\\;\\Omega = ' + A.R + '\\;\\Omega,\\quad I = \\dfrac{U}{R_\\text{ges}} = \\dfrac{' + ein(A.U, 'V') + '}{' + A.R + '\\;\\Omega} ' + erg(A.I, 'mA'); } },
      'parallel': { felder: ['R', 'I'], muster: '<i>R</i><sub>ges</sub> = {R} Ω; <i>I</i> = {I} mA',
        neu: function(){
          var P = zufall([[100, 100], [100, 400], [60, 30], [150, 300], [220, 330], [100, 150], [200, 300], [120, 60]]), U = zufall([6, 9, 12, 24]);
          var R = P[0] * P[1] / (P[0] + P[1]);
          return { R: R, I: U / R * 1000, R1: P[0], R2: P[1], U: U,
            text: '\\(R_1 = ' + P[0] + '\\;\\Omega\\) und \\(R_2 = ' + P[1] + '\\;\\Omega\\) liegen parallel an \\(U = ' + ein(U, 'V') + '\\). Gesamtwiderstand und Gesamtstrom?' }; },
        pruefen: function(A, e){
          if (nah(e.R, A.R) && nah(e.I, A.I)) return null;
          var r = [];
          if (nah(e.R, A.R1 + A.R2)) r.push('Das ist die Reihe. Parallel addieren sich die Kehrwerte: \\(\\dfrac{1}{R_\\text{ges}} = \\dfrac{1}{R_1} + \\dfrac{1}{R_2}\\).');
          else if (nah(e.R, 1 / A.R)) r.push('Das ist \\(\\dfrac{1}{R_\\text{ges}}\\) — noch den Kehrwert nehmen.');
          else if (!nah(e.R, A.R) && e.R >= Math.min(A.R1, A.R2)) r.push('Parallel ist \\(R_\\text{ges}\\) kleiner als der kleinste Einzelwiderstand.');
          else if (!nah(e.R, A.R)) r.push('\\(R_\\text{ges} = \\dfrac{R_1 \\cdot R_2}{R_1 + R_2}\\) nachrechnen.');
          if (!nah(e.I, A.I) && !(nah(e.R, A.R1 + A.R2) && nah(e.I, A.U / (A.R1 + A.R2) * 1000))){
            if (nah(e.I, A.U / A.R1 * 1000) || nah(e.I, A.U / A.R2 * 1000)) r.push('Das ist ein Teilstrom. Gesamtstrom: \\(I = I_1 + I_2\\).');
            else if (nah(e.I, A.I / 1000)) r.push('Strom in Milliampere: mal \\(1000\\).');
            else r.push('\\(I = \\dfrac{U}{R_\\text{ges}} = I_1 + I_2\\), in \\(\\text{mA}\\).');
          }
          return r.join(' '); },
        fehler: function(A){
          return [[{ R: String(A.R1 + A.R2), I: String(A.U / (A.R1 + A.R2) * 1000) }, 'Reihe'], [{ R: String(1 / A.R), I: String(A.I) }, 'Kehrwert'], [{ R: String(A.R), I: String(A.U / A.R1 * 1000) }, 'Teilstrom']]; },
        loesung: function(A){ return 'R_\\text{ges} = \\dfrac{R_1 \\cdot R_2}{R_1 + R_2} = \\dfrac{' + A.R1 + '\\;\\Omega \\cdot ' + A.R2 + '\\;\\Omega}{' + (A.R1 + A.R2) + '\\;\\Omega} ' + erg(A.R, 'Ω') + ',\\quad I = \\dfrac{U}{R_\\text{ges}} = \\dfrac{' + ein(A.U, 'V') + '}{' + tz(+A.R.toPrecision(4)) + '\\;\\Omega} ' + erg(A.I, 'mA'); } },
      'teiler': { felder: ['U2'], muster: '<i>U</i>₂ = {U2} V',
        neu: function(){
          var R1 = zufall([100, 220, 330, 470, 1000]), R2 = zufall([100, 150, 220, 470, 680, 1000]), U = zufall([9, 12, 24]);
          return { U2: U * R2 / (R1 + R2), R1: R1, R2: R2, U: U,
            text: '\\(R_1 = ' + R1 + '\\;\\Omega\\) und \\(R_2 = ' + R2 + '\\;\\Omega\\) liegen in Reihe an \\(U = ' + ein(U, 'V') + '\\) (unbelastet: am Abgriff zwischen den beiden hängt nichts weiter). Welche Spannung liegt über \\(R_2\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.U2, A.U2)) return null;
          if (nah(e.U2, A.U - A.U2)) return 'Das ist die Spannung über \\(R_1\\). Über dem grösseren Widerstand liegt die grössere Spannung.';
          if (nah(e.U2, A.U)) return 'In Reihe teilt sich die Spannung auf: \\(U = U_1 + U_2\\).';
          if (nah(e.U2, A.U / 2) && A.R1 !== A.R2) return 'Nicht halbe-halbe: Die Spannungen verhalten sich wie die Widerstände.';
          return 'Erst \\(I = \\dfrac{U}{R_1 + R_2}\\), dann \\(U_2 = I \\cdot R_2\\).'; },
        fehler: function(A){ var l = [[{ U2: String(A.U) }, 'teilt']]; if (A.R1 !== A.R2) l.push([{ U2: String(A.U - A.U2) }, 'über']); return l; },
        loesung: function(A){ return 'I = \\dfrac{U}{R_1 + R_2} = \\dfrac{' + ein(A.U, 'V') + '}{' + (A.R1 + A.R2) + '\\;\\Omega} ' + erg(A.U / (A.R1 + A.R2) * 1000, 'mA') + ',\\quad U_2 = I \\cdot R_2 = ' + ein(+(A.U / (A.R1 + A.R2) * 1000).toPrecision(3), 'mA') + ' \\cdot ' + A.R2 + '\\;\\Omega ' + erg(A.U2, 'V'); } },

      /* ----- Kapitel 7 (bis 06.10.2026 Kapitel 5) ----- */
      'koerperstrom': { felder: ['I', 'zeit'], muster: '<i>I</i><sub>K</sub> = {I} mA; der FI muss trennen nach höchstens {zeit:300 ms|150 ms|40 ms}',
        neu: function(){
          // Nur am Netz (230 V Wechselspannung) und mit einem unverzögerten 30-mA-FI:
          // Für Kleinspannung und Gleichstrom gelten diese Zeiten nicht. Alle Werte
          // liegen über 30 mA; gefragt ist die Höchstzeit (bis 2·IΔn 300 ms, bis
          // 5·IΔn 150 ms, darüber 40 ms). Keiner trifft eine Grenze genau.
          var F, I;
          do {
            F = zufall([[1000, 'nasser Haut'], [1300, 'feuchter Haut'], [1600, 'trockener Haut'], [2300, 'trockener Haut'],
                        [3000, 'Schuhen auf trockenem Boden'], [4000, 'Schuhen auf trockenem Boden'], [6000, 'Gummisohlen auf trockenem Boden']]);
          } while (F[0] === 1500);   // Aufgabe 5a
          I = 230 / F[0] * 1000;
          var fak = I / 30;
          return { I: I, U: 230, R: F[0], zeit: fak >= 5 ? '40 ms' : fak >= 2 ? '150 ms' : '300 ms',
            text: 'Ein Mensch mit ' + F[1] + ' (\\(R_\\text{K} = ' + tz(F[0]) + '\\;\\Omega\\), Körper und Boden zusammen) berührt ein defektes Gehäuse am Netz (\\(230\\;\\text{V}\\) Wechselspannung). Der Strom fliesst über ihn und den Boden zur geerdeten Quelle zurück. Körperstrom? Nach welcher Zeit muss ein unverzögerter FI mit \\(30\\;\\text{mA}\\) spätestens trennen?' }; },
        pruefen: function(A, e){
          var r = [];
          if (nah(e.I, A.I) && e.zeit === A.zeit) return null;
          if (!nah(e.I, A.I)){
            if (faktor(e.I, A.I, 0.001)) r.push('Das ist der Wert in Ampere — in Milliampere mal \\(1000\\).');
            else if (nah(e.I, A.U * A.R) || nah(e.I, A.R / A.U * 1000)) r.push('\\(I_\\text{K} = \\dfrac{U}{R_\\text{K}}\\): Spannung durch Körperwiderstand.');
            else r.push('\\(I_\\text{K} = \\dfrac{U}{R_\\text{K}}\\), dann in \\(\\text{mA}\\).');
          }
          if (e.zeit !== A.zeit) r.push('Vergleiche mit \\(30\\;\\text{mA}\\): bis zum Doppelten (\\(60\\;\\text{mA}\\)) höchstens \\(300\\;\\text{ms}\\), bis zum Fünffachen (\\(150\\;\\text{mA}\\)) höchstens \\(150\\;\\text{ms}\\), darüber \\(40\\;\\text{ms}\\).');
          return r.join(' '); },
        fehler: function(A){
          var andere = ['300 ms', '150 ms', '40 ms'].filter(function(x){ return x !== A.zeit; });
          return [[{ I: String(A.I / 1000), zeit: A.zeit }, 'Ampere'], [{ I: String(A.I), zeit: andere[0] }, 'Doppelten'], [{ I: String(A.R / A.U * 1000), zeit: A.zeit }, 'durch']]; },
        loesung: function(A){ return 'I_\\text{K} = \\dfrac{U}{R_\\text{K}} = \\dfrac{' + ein(A.U, 'V') + '}{' + tz(A.R) + '\\;\\Omega} ' + erg(A.I, 'mA') + ',\\quad \\text{FI: höchstens ' + A.zeit + '}'; } },
      'schutz': { felder: ['s'], muster: '{s:FI-Schutzschalter|Leitungsschutzschalter|Schutzleiter|Schutzklasse II}',
        neu: function(){
          var F = zufall([
            ['Vier Heizlüfter hängen am selben Stromkreis, die Leitung wird zu heiss. Was schaltet ab?', 'Leitungsschutzschalter'],
            ['Aussen- und Neutralleiter berühren sich im Gerät direkt. Was schaltet ab?', 'Leitungsschutzschalter'],
            ['Jemand berührt einen defekten Föhn; \\(40\\;\\text{mA}\\) fliessen über den Körper zur Erde. Was schaltet ab?', 'FI-Schutzschalter'],
            ['Eine feuchte Wand lässt \\(35\\;\\text{mA}\\) vom Aussenleiter zur Erde abfliessen. Was schaltet ab?', 'FI-Schutzschalter'],
            ['Ein Metallgehäuse bekommt Kontakt zum Aussenleiter. Was führt den Fehlerstrom zur geerdeten Quelle zurück, damit er gross wird und sofort abgeschaltet wird?', 'Schutzleiter'],
            ['Ein Gerät hat keinen Schutzleiter, aber eine doppelte oder verstärkte Isolierung (Doppelquadrat-Symbol). Wie heisst diese Schutzmassnahme?', 'Schutzklasse II']
          ]);
          if (this._letzte === F[0]) return this.neu();   // nicht zweimal hintereinander dieselbe Frage
          this._letzte = F[0];
          return { s: F[1], text: F[0] }; },
        pruefen: function(A, e){
          if (e.s === A.s) return null;
          if (e.s === 'FI-Schutzschalter') return A.s === 'Leitungsschutzschalter' ? 'Der FI vergleicht Hin- und Rückstrom. Hier fliesst alles zurück — keine Differenz.' : 'Der FI schaltet ab, leitet aber nichts ab und isoliert nichts.';
          if (e.s === 'Leitungsschutzschalter') return 'Der Leitungsschutzschalter reagiert erst auf Ströme über seinem Nennstrom (bei B13 über \\(13\\;\\text{A}\\): Überlast nach einiger Zeit, Kurzschluss sofort) — er schützt die Leitung, nicht den Menschen.';
          if (e.s === 'Schutzleiter') return 'Der Schutzleiter schaltet nichts ab; er bietet dem Fehlerstrom nur einen guten Rückweg zur Quelle.';
          return 'Schutzklasse II heisst: doppelte oder verstärkte Isolierung, ohne Schutzleiter. Sie schaltet nichts ab.'; },
        loesung: function(A){ return '\\text{' + A.s + '}'; } }
    };
    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie');
      function neu(){
        A = T.neu(); versuche = 0; geloest = false; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = typeof T.muster === 'function' ? T.muster(A) : T.muster;
        T.felder.forEach(function(f){
          html = html.replace(new RegExp('\\{' + f + '(?::([^}]*))?\\}'), function(m, wahl){
            if (!wahl) return '<input type="text" inputmode="decimal" autocomplete="off" aria-label="' + f + '" data-f="' + f + '">';
            return '<select aria-label="' + f + '" data-f="' + f + '"><option value="">?</option>' + wahl.split('|').map(function(w){ return '<option>' + w + '</option>'; }).join('') + '</select>';
          }); });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        setzen(auf);
      }
      function pruefen(){
        if (geloest) return;   // nach ✓ zählt erst die nächste Aufgabe
        var e = {}, leer = false, kaputt = false, komma = false;
        ein.querySelectorAll('select').forEach(function(w){ e[w.dataset.f] = w.value; if (!w.value) leer = true; });
        ein.querySelectorAll('input').forEach(function(i){
          var r = lesen(i.value); e[i.dataset.f] = r.wert;
          if (r.leer) leer = true; else if (isNaN(r.wert)) kaputt = true; if (r.komma) komma = true;
          i.classList.toggle('falsch', !r.leer && isNaN(r.wert)); });
        if (leer){ rueck.className = 'ue-rueck hinweis'; rueck.textContent = ein.querySelector('select') ? 'Wähle aus und fülle alle offenen Felder aus.' : 'Fülle alle Felder aus.'; return; }
        if (kaputt){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = 'Zahlen ohne Einheit, mit Punkt oder Komma: <code>0.25</code>, <code>-3</code>, <code>1/2</code> oder <code>2.4e-3</code> für \\(2.4 \\cdot 10^{-3}\\).'; setzen(rueck); return; }
        versuche++;
        var f = T.pruefen(A, e);
        if (f === null){
          serie = versuche === 1 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + ' <button type="button" class="ue-weiter">Nächste</button>';
          rueck.querySelector('.ue-weiter').addEventListener('click', neu);
        } else {
          serie = 0; rueck.className = 'ue-rueck falsch';
          rueck.innerHTML = (f || 'Noch nicht.') + (versuche >= 2 ? ' <details class="ue-loes"><summary>Lösung</summary>\\(' + T.loesung(A) + '\\)</details>' : '');
        }
        zaehler.textContent = serie + ' in Folge' + (serie >= 3 ? ' ✓' : '');
        setzen(rueck);
      }
      box.querySelector('.ue-pruefen').addEventListener('click', pruefen);
      box.querySelector('.ue-neu').addEventListener('click', neu);
      ein.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') pruefen(); });
      neu();
    });
  })();

  /* ---------- Minigrafen: Ursprungsgeraden zum Ablesen ----------
     <svg class="mini" data-geraden="m1;m2" data-namen="A;B" data-farbe="kurve-i|kurve-r" data-fenster="x1,y1"
          data-teilung="sx,sy" data-xname data-yname data-punkte="x,y;…">
     Punkte auf Gitterpunkten, damit sich die Steigung ablesen lässt. */
  document.querySelectorAll('svg.mini[data-geraden]').forEach(function(svg){
    var fe = svg.dataset.fenster.split(',').map(Number), tl = (svg.dataset.teilung || '1,1').split(',').map(Number);
    var xm = [], ym = [], i;
    for (i = 2 * tl[0]; i <= fe[0] + 1e-9; i += 2 * tl[0]) xm.push(+i.toPrecision(6));
    for (i = 2 * tl[1]; i <= fe[1] + 1e-9; i += 2 * tl[1]) ym.push(+i.toPrecision(6));
    var w = 170, h = 150;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h); svg.setAttribute('role', 'img');
    var K = Achsen(svg, { w: w, h: h, x0: -fe[0] * 0.16, x1: fe[0] * 1.06, y0: -fe[1] * 0.14, y1: fe[1] * 1.08, sx: tl[0], sy: tl[1], xm: xm, ym: ym, r: 3, pfeil: 6, xname: svg.dataset.xname, yname: svg.dataset.yname });
    var namen = (svg.dataset.namen || '').split(';');
    svg.dataset.geraden.split(';').map(Number).forEach(function(m, k){
      K.kurve(function(x){ return m * x; }, 'kurve-mini ' + (svg.dataset.farbe || ''), 0);
      // Name über dem Ende der Geraden, Versatz in Fensteranteilen (nicht in Dateneinheiten)
      if (namen[k]){ var xe = Math.min(fe[0], fe[1] / m) * 0.9; K.text(xe - fe[0] * 0.03, m * xe + fe[1] * 0.05, namen[k], 'mini-name', 'end'); }
    });
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){ var q = p.split(',').map(Number); K.punkt(q[0], q[1], 'p-mini'); });
  });
})();
</script>
