<script>
/* Leitprogramm Dynamik — animierte Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort,
   Übungsrahmen, Minigrafen) wörtlich aus dem Leitprogramm Kinematik; neu sind die
   laufenden Animationen (Uhr, Start/Zurück, voriger Lauf als Vergleich), die Simulationen
   und die Übungstypen für 4.2. g = 9.81 m/s² wie Themenseite 4.2. Farben: v Grün,
   a Violett, Antrieb, Zug-, Faden- und Normalkraft Blau, Gewichtskraft Bernstein,
   Widerstand und Zentripetalkraft Rot (Themenseite 4.2, STYLEGUIDE §5.2). Zahlen mit
   Dezimalpunkt und echtem Minus; «·» nur als Malpunkt, Trenner ist der Strichpunkt. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var NB = '\u00A0';                                     // Zahl und Einheit nicht trennen
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
      X: X, Y: Y, ebene: ebene, clip: 'url(#' + id + ')',
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
      text: function(x, y, s, cls, anker){ return el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': cls }, s); }
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


  var G = 9.81;                                          // wie Themenseite 4.2
  // Wert mit Einheit zum Einsetzen: negative Werte in Klammern, echtes Minus
  function ew(x, u){ var t = zahl(x) + NB + u; return x < 0 ? '(' + t + ')' : t; }
  function marke(eltern, x, y, grund, index, cls, anker){
    var t = el(eltern, 'text', { x: x, y: y, 'text-anchor': anker || 'middle', 'class': cls }, grund);
    if (index){ el(t, 'tspan', { dy: 3, 'font-size': '8.5' }, index); }
    return t;
  }
  function pfeil(eltern, x1, y1, x2, y2, cls, spitze){
    var dx = x2 - x1, dy = y2 - y1, l = Math.hypot(dx, dy); if (l < 1) return;
    var s = Math.min(spitze || 8, l * 0.6), ux = dx / l, uy = dy / l;
    el(eltern, 'line', { x1: x1, y1: y1, x2: x2 - ux * s * 0.8, y2: y2 - uy * s * 0.8, 'class': 'pf-linie ' + cls });
    el(eltern, 'polygon', { points: x2 + ',' + y2 + ' ' + (x2 - ux * s - uy * s * 0.45) + ',' + (y2 - uy * s + ux * s * 0.45) + ' ' + (x2 - ux * s + uy * s * 0.45) + ',' + (y2 - uy * s - ux * s * 0.45), 'class': 'pf-kopf ' + cls });
  }
  function g_(eltern, attr){ return el(eltern, 'g', attr || {}); }
  function v_(s){ return '<i>' + s + '</i>'; }                     // Formelzeichen kursiv (v ist hier oft eine Zahl)

  /* ---------- Uhr für die laufenden Animationen ----------
     Eine Animation läuft nur auf Knopfdruck (Start, Kreisen, Fahrprogramm) — kein Punkt
     wandert ohne Anlass (STYLEGUIDE §5.10). Die Zeit kommt aus requestAnimationFrame;
     bei «weniger Bewegung» springt ein Lauf mit Ende sofort ans Ende. */
  var WENIGER = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function Uhr(schritt){
    var id = null, t0 = 0, t = 0;
    function tick(jetzt){
      if (!t0) t0 = jetzt - t * 1000;
      t = (jetzt - t0) / 1000;
      if (schritt(t) === false){ id = null; return; }
      id = requestAnimationFrame(tick);
    }
    return {
      start: function(ab){ this.stop(); t = ab || 0; t0 = 0; id = requestAnimationFrame(tick); },
      stop: function(){ if (id) cancelAnimationFrame(id); id = null; },
      laeuft: function(){ return id !== null; }
    };
  }
  function aktionen(fig, liste){
    var box = fig.querySelector('.sim-aktionen'), k = {};
    liste.forEach(function(a){ var b = document.createElement('button'); b.type = 'button'; b.className = 'aktion'; b.textContent = a[1]; b.addEventListener('click', a[2]); box.appendChild(b); k[a[0]] = b; });
    return k;
  }

  /* ---------- Kapitel 1: Kraft, Masse, Beschleunigung ----------
     Wie Animation 2 der Themenseite (Wagen auf reibungsfreier Bahn, a = F/m), aber mit dem
     v-t-Diagramm, das während der Fahrt entsteht, und der Geraden des vorigen Laufs als
     Vergleich: So wird «doppelte Kraft, doppelte Steigung» direkt sichtbar.
     Startwert = Clipbeispiel: F = 4 N, m = 2 kg, also a = 2 m/s². */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var BAHN = 16, X0 = 14, PX = 16.5;                         // 16 m Bahn, 16.5 px je m
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,118)' });
    var K = Achsen(dia, { w: 300, h: 190, x0: -0.5, x1: 4.6, y0: -2.4, y1: 21, sx: 0.5, sy: 2, xm: [1, 2, 3, 4], ym: [4, 8, 12, 16, 20], xname: 't [s]', yname: 'v [m/s]' });
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; spur = []; zeichnen(); });
    var t = 0, spur = [], vorher = null, letzter = null, lauf = null, laeufe = {}, ziel = null, pruefen = function(){};
    function werte(){ var F = B.wert('F'), m = B.wert('m'); return { F: F, m: m, a: F / m }; }
    function tEnde(a){ return a > 0 ? Math.min(4, Math.sqrt(2 * BAHN / a)) : 4; }
    var uhr = Uhr(function(tt){
      var w = werte(), te = tEnde(w.a);
      t = Math.min(tt, te); spur.push([t, w.a * t]); zeichnen();
      if (t >= te){ letzter = { a: w.a, te: te }; lauf = { F: w.F, m: w.m, a: w.a }; laeufe[w.F + '|' + w.m] = true; zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Start', function(){ spur = []; vorher = letzter; if (WENIGER){ var w = werte(); t = tEnde(w.a); spur = [[0, 0], [t, w.a * t]]; letzter = { a: w.a, te: t }; lauf = { F: w.F, m: w.m, a: w.a }; laeufe[w.F + '|' + w.m] = true; zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); t = 0; spur = []; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.t = t; w.lauf = lauf; w.laeufe = Object.keys(laeufe).length; w.bewegt = B.bewegt; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; spur = []; B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; lauf = null; laeufe = {}; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), v = w.a * t, s = 0.5 * w.a * t * t;
      B.anzeigen(); leeren(szene); K.leeren();
      // Bahn und Wagen
      el(szene, 'line', { x1: X0, y1: 86, x2: X0 + BAHN * PX, y2: 86, 'class': 'boden' });
      for (var k = 0; k <= BAHN; k += 4) el(szene, 'text', { x: X0 + k * PX, y: 100, 'text-anchor': 'middle', 'class': 'skala' }, k + ' m');
      var x = X0 + Math.min(s, BAHN) * PX;
      el(szene, 'rect', { x: x - 30, y: 62, width: 30, height: 18, rx: 3, 'class': 'wagen' });
      el(szene, 'circle', { cx: x - 23, cy: 82, r: 4, 'class': 'rad' }); el(szene, 'circle', { cx: x - 7, cy: 82, r: 4, 'class': 'rad' });
      el(szene, 'text', { x: x - 15, y: 75, 'text-anchor': 'middle', 'class': 'bt-klein' }, zahl(w.m) + NB + 'kg');
      // Pfeile: F 4 px je N, a 10 px je m/s² (bis 70 px); am Bahnende rücken sie ins Bild zurück
      if (w.F > 0){ var fa = Math.min(x, 292 - w.F * 4); pfeil(szene, fa, 71, fa + w.F * 4, 71, 'pf-f'); marke(szene, fa + w.F * 4 + 4, 68, 'F', '', 'pf-text pf-f', 'start'); }
      if (w.a > 0){ var la = Math.min(w.a * 10, 70), ax = Math.min(x - 30, 292 - la); pfeil(szene, ax, 50, ax + la, 50, 'pf-a', 6); marke(szene, ax + la + 4, 53, 'a', '', 'pf-text pf-a', 'start'); }
      // v-t-Diagramm: Ziel, voriger Lauf, aktuelle Spur
      if (ziel != null) K.kurve(function(x){ return ziel * x; }, 'zielkurve', 0, 4);
      if (vorher) K.kurve(function(x){ return vorher.a * x; }, 'vorher', 0, vorher.te);
      if (spur.length > 1) el(K.ebene, 'polyline', { points: spur.map(function(p){ return K.X(p[0]).toFixed(1) + ',' + K.Y(p[1]).toFixed(1); }).join(' '), 'class': 'kurve-v', 'clip-path': K.clip });
      var tr = +t.toFixed(2), vr = w.a * tr;                  // angezeigt: v aus der angezeigten Zeit, damit die Zeile nachrechenbar bleibt
      if (t > 0) K.punkt(t, v, 'p-v', 'v = ' + sig(vr) + NB + 'm/s', t > 2.8 ? -9 : 9, v > 17 ? 16 : -9, t > 2.8 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML =
        '<span>' + v_('a') + ' = ' + v_('F') + ' / ' + v_('m') + ' = ' + zahl(w.F) + NB + 'N / ' + zahl(w.m) + NB + 'kg ' + ist(w.a, sig(w.a)) + sig(w.a) + NB + 'm/s²</span>' +
        '<span>' + v_('v') + ' = ' + v_('a') + ' · ' + v_('t') + ' = ' + sig(w.a) + NB + 'm/s² · ' + zahl(tr) + NB + 's ' + ist(vr, sig(vr)) + sig(vr) + NB + 'm/s</span>' +
        (s >= BAHN - 1e-9 && t > 0 ? '<span class="sim-notiz">Der Wagen ist am Ende der Bahn.</span>' : '') +
        (vorher ? '<span class="sim-notiz">Gestrichelt grau: der vorige Lauf.</span>' : '');
      pruefen();
    }
    function hat(s, F, m){ return s.lauf && gl(s.lauf.F, F) && gl(s.lauf.m, m); }
    pruefen = Leiste(fig, [
      { text: 'Starte mehrmals mit verschiedenen Kräften und Massen. Wie hängt die Steigung der v-t-Geraden von \\(F\\) und \\(m\\) ab? Notiere deine Antwort.', ok: function(s){ return s.bewegt.F && s.bewegt.m && s.laeufe >= 3; },
        vergleich: 'Die Steigung ist die Beschleunigung \\(a = \\dfrac{F}{m}\\). Doppelte Kraft gibt die doppelte Steigung, doppelte Masse die halbe. Ohne Kraft bleibt der Wagen stehen; die Kraft bestimmt, wie schnell sich die Geschwindigkeit ändert.' },
      { text: 'Ein Wagen von \\(4\\;\\text{kg}\\) soll mit \\(1.5\\;\\text{m/s}^2\\) anfahren. Stelle die nötige Kraft ein und lass ihn fahren.', ok: function(s){ return hat(s, 6, 4); } },
      { text: 'Jetzt \\(8\\;\\text{kg}\\) mit derselben Beschleunigung: Welche Kraft braucht es? Stelle ein und lass fahren.', ok: function(s){ return hat(s, 12, 8); } },
      { text: 'Mit \\(10\\;\\text{N}\\): Welche Masse wird mit \\(2.5\\;\\text{m/s}^2\\) beschleunigt? Stelle ein und lass fahren.', ok: function(s){ return hat(s, 10, 4); } },
      { text: 'Ein Wagen von \\(3\\;\\text{kg}\\) soll nach \\(2\\;\\text{s}\\) genau \\(6\\;\\text{m/s}\\) schnell sein. Stelle die Kraft ein und lass fahren.', ok: function(s){ return hat(s, 9, 3); } },
      { text: 'Triff die gestrichelte Gerade: Stelle Kraft und Masse ein und lass fahren.', setup: function(S){ ziel = 5; S.setze({ F: 4, m: 2 }); }, ok: function(s){ return s.lauf && gl(s.lauf.a, 5); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Gesamtkraft und Trägheit ----------
     Nimmt das Grundgesetz der Themenseite mit zwei Kräften auf einer Geraden: Antrieb nach
     vorn, Fahrwiderstand gegen die Bewegung. Die Kamera fährt mit dem Velo mit (die Strasse
     zieht vorbei), das v-t-Diagramm entsteht während der Fahrt. Sind beide Kräfte gleich,
     fährt das Velo mit konstantem Tempo weiter — oder bleibt stehen, je nach Anfangstempo:
     das Trägheitsgesetz. Masse fest 80 kg (Velo mit Fahrerin). Startwert = Clipbeispiel:
     Antrieb 60 N, Widerstand 20 N, aus dem Stand. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), M = 80, TE = 8;
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,118)' });
    var K = Achsen(dia, { w: 300, h: 190, x0: -0.9, x1: 8.8, y0: -1.3, y1: 12.5, sx: 1, sy: 1, xm: [2, 4, 6, 8], ym: [2, 4, 6, 8, 10, 12], xname: 't [s]', yname: 'v [m/s]' });
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; spur = []; zeichnen(); });
    var t = 0, spur = [], vorher = null, letzter = null, lauf = null, laeufe = [], ziel = null, pruefen = function(){};
    function werte(){ var v0 = B.wert('v0'), FA = B.wert('FA'), FW = B.wert('FW'); return { v0: v0, FA: FA, FW: FW, Fg: FA - FW, a: (FA - FW) / M }; }
    // v(t) und s(t): Der Widerstand wirkt gegen die Bewegung; steht das Velo und reicht der
    // Antrieb nicht, bleibt es stehen (der Widerstand schiebt nicht rückwärts).
    function vt(w, tt){ if (w.v0 <= 0 && w.a <= 0) return 0; var v = w.v0 + w.a * tt; return Math.max(0, v); }
    function st(w, tt){ if (w.v0 <= 0 && w.a <= 0) return 0; if (w.a < 0){ var ts = w.v0 / -w.a; if (tt > ts) tt = ts; } return w.v0 * tt + 0.5 * w.a * tt * tt; }
    var uhr = Uhr(function(tt){
      var w = werte(); t = Math.min(tt, TE); spur.push([t, vt(w, t)]); zeichnen();
      if (t >= TE){ letzter = w; lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Fahren', function(){ spur = []; vorher = letzter; if (WENIGER){ var w = werte(); spur = []; for (var k = 0; k <= 40; k++) spur.push([TE * k / 40, vt(w, TE * k / 40)]); t = TE; letzter = w; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); t = 0; spur = []; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; w.bewegt = B.bewegt; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; spur = []; B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; lauf = null; laeufe = []; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), v = vt(w, t), s = st(w, t);
      B.anzeigen(); leeren(szene); K.leeren();
      // Strasse zieht vorbei: Markierungen alle 4 m, 12 px je m
      el(szene, 'line', { x1: 0, y1: 86, x2: 300, y2: 86, 'class': 'boden' });
      var off = (s * 12) % 48;
      for (var x = -off; x < 300; x += 48) el(szene, 'line', { x1: x, y1: 92, x2: x + 22, y2: 92, 'class': 'markierung' });
      // Velo mit Fahrerin; die Speichen drehen mit dem Weg (Rad 11 px, Strasse 12 px je m)
      var cx = 150, RR = 11, dreh = s * 12 / RR;
      [cx - 19, cx + 19].forEach(function(rx){
        el(szene, 'circle', { cx: rx, cy: 75, r: RR, 'class': 'velo-rad' });
        for (var k = 0; k < 3; k++){ var w2 = dreh + k * Math.PI / 3; el(szene, 'line', { x1: rx - RR * Math.cos(w2), y1: 75 - RR * Math.sin(w2), x2: rx + RR * Math.cos(w2), y2: 75 + RR * Math.sin(w2), 'class': 'speiche' }); }
      });
      el(szene, 'polyline', { points: (cx - 19) + ',75 ' + (cx - 2) + ',75 ' + (cx + 11) + ',55 ' + (cx - 8) + ',55 ' + (cx - 2) + ',75', 'class': 'rahmen' });
      el(szene, 'polyline', { points: (cx - 19) + ',75 ' + (cx - 8) + ',55', 'class': 'rahmen' });
      el(szene, 'polyline', { points: (cx + 19) + ',75 ' + (cx + 12) + ',50 ' + (cx + 15) + ',48', 'class': 'rahmen' });
      el(szene, 'circle', { cx: cx + 6, cy: 21, r: 5.5, 'class': 'mensch' });
      el(szene, 'polyline', { points: (cx - 9) + ',51 ' + (cx + 3) + ',28', 'class': 'mensch' });
      el(szene, 'polyline', { points: (cx + 3) + ',30 ' + (cx + 13) + ',48', 'class': 'mensch' });
      el(szene, 'polyline', { points: (cx - 9) + ',51 ' + (cx + 4) + ',60 ' + (cx - 2) + ',75', 'class': 'mensch' });
      el(szene, 'text', { x: cx - 30, y: 24, 'text-anchor': 'end', 'class': 'bt-klein' }, '80' + NB + 'kg');
      if (w.FA > 0){ pfeil(szene, cx + 32, 64, cx + 32 + w.FA * 0.9, 64, 'pf-f'); marke(szene, cx + 36 + w.FA * 0.9, 61, 'F', 'A', 'pf-text pf-f', 'start'); }
      if (w.FW > 0 && (v > 0 || w.FA > 0)){
        var fw = (v > 0 || w.FA >= w.FW) ? w.FW : w.FA;    // steht das Velo, hält der Widerstand nur so stark dagegen, wie der Antrieb zieht
        pfeil(szene, cx - 32, 64, cx - 32 - fw * 0.9, 64, 'pf-w'); marke(szene, cx - 36 - fw * 0.9, 61, 'F', 'W', 'pf-text pf-w', 'end');
      }
      if (v > 0){ pfeil(szene, cx + 20, 30, cx + 20 + v * 6, 30, 'pf-v', 6); marke(szene, cx + 24 + v * 6, 33, 'v', '', 'pf-text pf-v', 'start'); }
      // Diagramm
      if (ziel) K.kurve(function(x){ return ziel.v0 + ziel.a * x; }, 'zielkurve', 0, TE);
      if (vorher) el(K.ebene, 'polyline', { points: [0, 1, 2, 3, 4, 5, 6, 7, 8].map(function(k){ return K.X(k).toFixed(1) + ',' + K.Y(vt(vorher, k)).toFixed(1); }).join(' '), 'class': 'vorher', 'clip-path': K.clip });
      if (spur.length > 1) el(K.ebene, 'polyline', { points: spur.map(function(p){ return K.X(p[0]).toFixed(1) + ',' + K.Y(p[1]).toFixed(1); }).join(' '), 'class': 'kurve-v', 'clip-path': K.clip });
      if (t > 0) K.punkt(t, v, 'p-v', 'v = ' + sig(v) + NB + 'm/s', t > 5 ? -9 : 9, v > 10 ? 16 : -9, t > 5 ? 'end' : 'start');
      var steht = w.v0 <= 0 && w.a <= 0;
      rolle(fig, 'formel').innerHTML =
        '<span>' + v_('F') + '<sub>ges</sub> = ' + v_('F') + '<sub>A</sub> − ' + v_('F') + '<sub>W</sub> = ' + zahl(w.FA) + NB + 'N − ' + zahl(w.FW) + NB + 'N = ' + zahl(w.Fg) + NB + 'N</span>' +
        (steht ? '<span>Das Velo steht, und der Antrieb überwindet den Widerstand nicht: Es bleibt stehen.</span>'
               : '<span>' + v_('a') + ' = ' + v_('F') + '<sub>ges</sub> / ' + v_('m') + ' = ' + ew(w.Fg, 'N') + ' / 80' + NB + 'kg ' + ist(w.a, sig(w.a)) + minus(sig(w.a)) + NB + 'm/s²</span>') +
        (!steht && w.a === 0 ? '<span class="sim-notiz">Gesamtkraft null: Die Geschwindigkeit bleibt, wie sie ist.</span>' : '') +
        (vorher ? '<span class="sim-notiz">Gestrichelt grau: der vorige Lauf.</span>' : '');
      pruefen();
    }
    function lief(s, f){ return s.laeufe.some(f); }
    pruefen = Leiste(fig, [
      { text: 'Lass das Velo mit gleich grossem Antrieb und Widerstand fahren — einmal aus dem Stand, einmal mit Anfangstempo. Was geschieht? Notiere deine Antwort.', ok: function(s){ return lief(s, function(l){ return l.FA === l.FW && l.FA > 0 && l.v0 === 0; }) && lief(s, function(l){ return l.FA === l.FW && l.FA > 0 && l.v0 > 0; }); },
        vergleich: 'Aus dem Stand bleibt das Velo stehen, mit Anfangstempo fährt es mit genau diesem Tempo weiter. Beide Male ist die Gesamtkraft null, also auch die Beschleunigung: Der Bewegungszustand bleibt erhalten — das Trägheitsgesetz.' },
      { text: 'Antrieb \\(100\\;\\text{N}\\), Widerstand \\(30\\;\\text{N}\\), aus dem Stand: Stelle ein, lass fahren und lies die Beschleunigung ab.', ok: function(s){ return s.lauf && s.lauf.FA === 100 && s.lauf.FW === 30 && s.lauf.v0 === 0; } },
      { text: 'Das Velo soll mit \\(6\\;\\text{m/s}\\) gleichmässig weiterrollen, der Widerstand beträgt \\(25\\;\\text{N}\\). Stelle ein und lass fahren.', ok: function(s){ return s.lauf && s.lauf.v0 === 6 && s.lauf.FW === 25 && s.lauf.FA === 25; } },
      { text: 'Ohne Antrieb soll das Velo von \\(6\\;\\text{m/s}\\) mit \\(0.5\\;\\text{m/s}^2\\) langsamer werden. Welcher Widerstand ist das? Stelle ein und lass fahren.', ok: function(s){ return s.lauf && s.lauf.v0 === 6 && s.lauf.FA === 0 && s.lauf.FW === 40; } },
      { text: 'Der Widerstand beträgt \\(20\\;\\text{N}\\). Welcher Antrieb beschleunigt aus dem Stand mit \\(1\\;\\text{m/s}^2\\)? Stelle ein und lass fahren.', ok: function(s){ return s.lauf && s.lauf.FW === 20 && s.lauf.FA === 100 && s.lauf.v0 === 0; } },
      { text: 'Triff die gestrichelte Gerade: Stelle Anfangstempo und Kräfte ein und lass fahren.', setup: function(S){ ziel = { v0: 2, a: 0.5 }; S.setze({ v0: 0, FA: 60, FW: 20 }); }, ok: function(s){ return s.lauf && s.lauf.v0 === 2 && gl(s.lauf.a, 0.5); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Gewichtskraft und Aufzug ----------
     Nimmt Aufgabe A6 der Themenseite (scheinbares Gewicht im Aufzug) als laufende Szene: Die
     Kabine fährt, die Schachtwand zieht vorbei, die Waage zeigt live die Normalkraft — auch
     als «kg»-Anzeige, wie eine Personenwaage. Fahrprogramm per Knopf, Beschleunigung per
     Regler. Nach oben positiv. Startwert = Clipbeispiel: 60 kg, Anfahren nach oben mit 2 m/s². */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), pruefen = function(){}, pos = 0;
    var B = Bedienung(fig, function(){ pos = 0; neuStarten(); zeichnen(); });
    function werte(){
      var ph = B.wert('ph'), m = B.wert('m'), b = B.wert('a');
      var a = ph === 'auf' ? b : ph === 'brems' ? -b : ph === 'fall' ? -G : 0;
      var FG = m * G, FN = m * (G + a);
      return { ph: ph, m: m, b: b, a: a, FG: FG, FN: FN, anz: FN / G };
    }
    // Bewegung für das Bild, in Schleifen von 3 s (nur zur Anschauung): v nach oben positiv
    function vBild(w, tt){
      var z = tt % 3;
      if (w.ph === 'auf') return w.b * z * 0.5;
      if (w.ph === 'konst') return 2;
      if (w.ph === 'brems') return Math.max(0, 3 - w.b * z * 0.5);
      if (w.ph === 'fall') return -G * (tt % 1.2) * 0.5;
      return 0;
    }
    var letzt = 0;
    var uhr = Uhr(function(tt){ var w = werte(); pos += vBild(w, tt) * (tt - letzt) * 40; letzt = tt; zeichnen(); });
    function neuStarten(){ letzt = 0; uhr.stop(); if (B.wert('ph') !== 'ruhe' && !WENIGER) uhr.start(0); }
    var sim = {
      zustand: function(){ var w = werte(); w.bewegt = B.bewegt; w.phasen = B.gesehen('ph'); return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); pos = 0; neuStarten(); zeichnen(); },
      aufraeumen: function(){ B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte();
      B.anzeigen(); leeren(svg);
      // Schacht mit Wandmarken, die vorbeiziehen
      el(svg, 'rect', { x: 40, y: 0, width: 150, height: 260, 'class': 'schacht' });
      var off = ((pos % 40) + 40) % 40;
      for (var y = -40 + off; y < 260; y += 40){ el(svg, 'line', { x1: 40, y1: y, x2: 52, y2: y, 'class': 'wandmarke' }); el(svg, 'line', { x1: 178, y1: y, x2: 190, y2: y, 'class': 'wandmarke' }); }
      // Kabine mit Waage und Person
      el(svg, 'rect', { x: 60, y: 30, width: 110, height: 200, rx: 4, 'class': 'kabine' });
      if (w.ph !== 'fall') el(svg, 'line', { x1: 115, y1: 0, x2: 115, y2: 30, 'class': 'seil' });
      else { el(svg, 'line', { x1: 115, y1: 0, x2: 115, y2: 12, 'class': 'seil' }); el(svg, 'text', { x: 122, y: 14, 'class': 'bt-klein' }, 'gerissen'); }
      el(svg, 'rect', { x: 92, y: 210, width: 46, height: 10, rx: 2, 'class': 'waage' });
      var mx = 115;
      el(svg, 'circle', { cx: mx, cy: 120, r: 9, 'class': 'mensch' });
      el(svg, 'polyline', { points: mx + ',129 ' + mx + ',172 ' + (mx - 9) + ',209', 'class': 'mensch' });
      el(svg, 'polyline', { points: mx + ',172 ' + (mx + 9) + ',209', 'class': 'mensch' });
      el(svg, 'polyline', { points: (mx - 14) + ',150 ' + mx + ',140 ' + (mx + 14) + ',150', 'class': 'mensch' });
      // Kräfte an der Person (0.07 px je N), Beschleunigung neben der Kabine
      var k = 0.07;
      pfeil(svg, mx - 18, 160, mx - 18, 160 + w.FG * k, 'pf-g'); marke(svg, mx - 22, 160 + w.FG * k * 0.6, 'F', 'G', 'pf-text pf-g', 'end');
      if (w.FN > 0.5){ pfeil(svg, mx + 18, 208, mx + 18, 208 - w.FN * k, 'pf-f'); marke(svg, mx + 22, 208 - w.FN * k * 0.6, 'F', 'N', 'pf-text pf-f', 'start'); }
      if (Math.abs(w.a) > 0.01){ var la = Math.min(Math.abs(w.a) * 7, 70) * (w.a > 0 ? -1 : 1); pfeil(svg, 205, 130, 205, 130 + la, 'pf-a', 7); marke(svg, 212, 130 + la / 2, 'a', '', 'pf-text pf-a', 'start'); }
      // Anzeige der Waage
      el(svg, 'rect', { x: 214, y: 196, width: 80, height: 40, rx: 5, 'class': 'anzeige' });
      el(svg, 'text', { x: 254, y: 213, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Waage zeigt');
      el(svg, 'text', { x: 254, y: 230, 'text-anchor': 'middle', 'class': 'anzeige-zahl' }, fest(w.anz, 1) + NB + 'kg');
      var z = [];
      if (w.ph === 'ruhe' || w.ph === 'konst')
        z.push('<span>' + v_('a') + ' = 0: ' + v_('F') + '<sub>N</sub> = ' + v_('F') + '<sub>G</sub> = ' + v_('m') + ' · ' + v_('g') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² ' + ist(w.FG, sig(w.FG)) + sig(w.FG) + NB + 'N</span>');
      else {
        z.push('<span>Ansatz (nach oben positiv): ' + v_('F') + '<sub>N</sub> − ' + v_('F') + '<sub>G</sub> = ' + v_('m') + ' · ' + v_('a') + '</span>');
        z.push('<span>' + v_('F') + '<sub>N</sub> = ' + v_('m') + ' · (' + v_('g') + ' + ' + v_('a') + ') = ' + zahl(w.m) + NB + 'kg · (9.81' + NB + 'm/s² + ' + ew(+w.a.toFixed(2), 'm/s²') + ') ' + ist(w.FN, sig(w.FN)) + (Math.abs(w.FN) < 1e-9 ? '0' : sig(w.FN)) + NB + 'N</span>');
      }
      z.push('<span>Anzeige der Waage: ' + v_('F') + '<sub>N</sub> / ' + v_('g') + ' ' + ist(w.anz, fest(w.anz, 1)) + fest(w.anz, 1) + NB + 'kg</span>');
      rolle(fig, 'formel').innerHTML = z.join('');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Probiere alle fünf Fahrsituationen. Wann zeigt die Waage mehr, wann weniger als in Ruhe? Notiere deine Antwort.', ok: function(s){ return s.phasen >= 4; },
        vergleich: 'Mehr, wenn die Beschleunigung nach oben zeigt (Anfahren aufwärts); weniger, wenn sie nach unten zeigt (Bremsen der Aufwärtsfahrt); gleich viel bei Ruhe und gleichmässiger Fahrt. Die Waage zeigt die Normalkraft \\(F_N = m \\cdot (g + a)\\), nicht die Masse.' },
      { text: 'Eine Person von \\(80\\;\\text{kg}\\) steht im ruhenden Aufzug. Stelle ein und lies die Normalkraft ab.', ok: function(s){ return gl(s.m, 80) && s.ph === 'ruhe'; } },
      { text: 'Beim Anfahren nach oben zeigt die Waage bei einer Person von \\(75\\;\\text{kg}\\) rund \\(90\\;\\text{kg}\\) an. Stelle die Beschleunigung ein.', ok: function(s){ return gl(s.m, 75) && s.ph === 'auf' && Math.abs(s.anz - 90) < 0.6; } },
      { text: 'Die Aufwärtsfahrt wird mit \\(1.5\\;\\text{m/s}^2\\) gebremst, die Person hat \\(60\\;\\text{kg}\\). Stelle ein: Was zeigt die Waage?', ok: function(s){ return gl(s.m, 60) && s.ph === 'brems' && gl(s.b, 1.5); } },
      { text: 'Das Seil reisst: Wähle den freien Fall. Was zeigt die Waage — und warum? Notiere deine Antwort.', ok: function(s){ return s.ph === 'fall'; },
        vergleich: 'Null. Person und Waage fallen beide mit \\(g\\); die Waage muss die Person nicht mehr abstützen. Aus \\(F_N = m \\cdot (g + a)\\) mit \\(a = -g\\) folgt \\(F_N = 0\\): Die Person ist «schwerelos», obwohl ihre Gewichtskraft unverändert wirkt.' },
      { text: 'Stelle eine Fahrt ein, bei der die Waage die Hälfte der Ruheanzeige zeigt.', ok: function(s){ return s.ph !== 'fall' && Math.abs(s.FN / s.FG - 0.5) < 0.006; } }
    ], sim);
    neuStarten(); zeichnen();
  })();

  /* ---------- Kapitel 4: Zwei Körper, ein Faden ----------
     Nimmt die Atwood-Aufgabe A5 der Themenseite als Tischversion: Ein Wagen (m₁) auf dem
     reibungsfreien Tisch wird über eine Rolle von einem hängenden Körper (m₂) gezogen. Die
     Fahrt läuft ab, das v-t-Diagramm entsteht dabei, der vorige Lauf bleibt als Vergleich.
     Faden und Rolle masselos. Startwert = Clipbeispiel: m₁ = 3 kg, m₂ = 1 kg. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), TISCH = 1.2, PX = 80, TE = 2.5;     // 80 px je m, waagrecht wie senkrecht (der Faden ist undehnbar)
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,226)' });
    var K = Achsen(dia, { w: 300, h: 176, x0: -0.3, x1: 2.75, y0: -0.6, y1: 6.3, sx: 0.25, sy: 1, xm: [0.5, 1, 1.5, 2, 2.5], ym: [1, 2, 3, 4, 5, 6], xname: 't [s]', yname: 'v [m/s]' });
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; spur = []; zeichnen(); });
    var t = 0, spur = [], vorher = null, letzter = null, lauf = null, laeufe = {}, ziel = null, pruefen = function(){};
    function werte(){ var m1 = B.wert('m1'), m2 = B.wert('m2'), a = m2 * G / (m1 + m2); return { m1: m1, m2: m2, a: a, FS: m1 * a, FG2: m2 * G }; }
    function tEnde(a){ return Math.min(TE, Math.sqrt(2 * TISCH / a)); }
    var uhr = Uhr(function(tt){
      var w = werte(), te = tEnde(w.a); t = Math.min(tt, te); spur.push([t, w.a * t]); zeichnen();
      if (t >= te){ letzter = { a: w.a, te: te }; lauf = w; laeufe[w.m1 + '|' + w.m2] = true; zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Loslassen', function(){ spur = []; vorher = letzter; if (WENIGER){ var w = werte(); t = tEnde(w.a); spur = [[0, 0], [t, w.a * t]]; letzter = { a: w.a, te: t }; lauf = w; laeufe[w.m1 + '|' + w.m2] = true; zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); t = 0; spur = []; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = Object.keys(laeufe).length; w.bewegt = B.bewegt; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; spur = []; B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; lauf = null; laeufe = {}; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), v = w.a * t, s = Math.min(0.5 * w.a * t * t, TISCH);
      B.anzeigen(); leeren(szene); K.leeren();
      // Tisch, Rolle, Wagen, Faden, hängender Körper
      var tx0 = 8, ty = 44, bw = 44, rx = tx0 + 4 + bw + TISCH * PX + 12;
      el(szene, 'rect', { x: tx0, y: ty, width: rx - tx0 - 6, height: 6, 'class': 'tisch' });
      el(szene, 'circle', { cx: rx, cy: ty - 4, r: 7, 'class': 'rolle' });
      var wx = tx0 + 4 + s * PX;
      el(szene, 'rect', { x: wx, y: ty - 26, width: bw, height: 18, rx: 3, 'class': 'wagen' });
      el(szene, 'circle', { cx: wx + 9, cy: ty - 4, r: 4, 'class': 'rad' }); el(szene, 'circle', { cx: wx + bw - 9, cy: ty - 4, r: 4, 'class': 'rad' });
      el(szene, 'text', { x: wx + bw / 2, y: ty - 13, 'text-anchor': 'middle', 'class': 'bt-klein' }, zahl(w.m1) + NB + 'kg');
      el(szene, 'text', { x: wx + bw / 2, y: ty + 18, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'm₁');
      var hy = ty + 12 + s * PX, hs = 14 + Math.sqrt(w.m2) * 8, hx = rx + 7, hm = hy + hs / 2;
      el(szene, 'polyline', { points: (wx + bw) + ',' + (ty - 17) + ' ' + rx + ',' + (ty - 11) + ' ' + hx + ',' + (ty - 4) + ' ' + hx + ',' + hy, 'class': 'faden' });
      el(szene, 'rect', { x: hx - hs / 2, y: hy, width: hs, height: hs, rx: 2, 'class': 'gewicht' });
      el(szene, 'text', { x: hx - hs / 2 - 5, y: hm + 3, 'text-anchor': 'end', 'class': 'bt-klein' }, 'm₂ = ' + zahl(w.m2) + NB + 'kg');
      // Kräfte (1.6 px je N): Fadenkraft am Wagen; am hängenden Körper Gewichtskraft nach unten, Fadenkraft nach oben
      var k = 1.6, px1 = hx + hs / 2 + 7, px2 = px1 + 9;
      pfeil(szene, wx + bw + 2, ty - 32, wx + bw + 2 + w.FS * k, ty - 32, 'pf-f', 6); marke(szene, wx + bw + 6 + w.FS * k, ty - 29, 'F', 'S', 'pf-text pf-f', 'start');
      pfeil(szene, px1, hm, px1, hm + w.FG2 * k, 'pf-g', 6); marke(szene, px1 + 5, hm + w.FG2 * k, 'F', 'G2', 'pf-text pf-g', 'start');
      pfeil(szene, px2, hm, px2, hm - w.FS * k, 'pf-f', 6); marke(szene, px2 + 5, hm - w.FS * k + 8, 'F', 'S', 'pf-text pf-f', 'start');
      // Diagramm
      if (ziel != null) K.kurve(function(x){ return ziel * x; }, 'zielkurve', 0, TE);
      if (vorher) K.kurve(function(x){ return vorher.a * x; }, 'vorher', 0, vorher.te);
      if (spur.length > 1) el(K.ebene, 'polyline', { points: spur.map(function(p){ return K.X(p[0]).toFixed(1) + ',' + K.Y(p[1]).toFixed(1); }).join(' '), 'class': 'kurve-v', 'clip-path': K.clip });
      if (t > 0) K.punkt(t, v, 'p-v', 'v = ' + sig(v) + NB + 'm/s', t > 1.6 ? -9 : 9, v > 5 ? 16 : -9, t > 1.6 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML =
        '<span>' + v_('a') + ' = ' + v_('m') + '₂ · ' + v_('g') + ' / (' + v_('m') + '₁ + ' + v_('m') + '₂) = ' + zahl(w.m2) + NB + 'kg · 9.81' + NB + 'm/s² / ' + zahl(+(w.m1 + w.m2).toFixed(2)) + NB + 'kg ' + ist(w.a, sig(w.a)) + sig(w.a) + NB + 'm/s²</span>' +
        '<span>' + v_('F') + '<sub>S</sub> = ' + v_('m') + '₁ · ' + v_('a') + ' = ' + zahl(w.m1) + NB + 'kg · ' + sig(w.a) + NB + 'm/s² ' + ist(w.FS, sig(w.FS)) + sig(w.FS) + NB + 'N</span>' +
        '<span>' + v_('F') + '<sub>G2</sub> = ' + v_('m') + '₂ · ' + v_('g') + ' ' + ist(w.FG2, sig(w.FG2)) + sig(w.FG2) + NB + 'N</span>' +
        (vorher ? '<span class="sim-notiz">Gestrichelt grau: der vorige Lauf.</span>' : '');
      pruefen();
    }
    function hat(s, m1, m2){ return s.lauf && gl(s.lauf.m1, m1) && gl(s.lauf.m2, m2); }
    pruefen = Leiste(fig, [
      { text: 'Lass mehrmals mit verschiedenen Massen los. Ist die Fadenkraft so gross wie die Gewichtskraft des hängenden Körpers? Notiere deine Antwort.', ok: function(s){ return s.laeufe >= 2 && (s.bewegt.m1 || s.bewegt.m2); },
        vergleich: 'Nein, kleiner. Am hängenden Körper ziehen \\(F_{G2}\\) nach unten und \\(F_S\\) nach oben; weil er nach unten beschleunigt, muss \\(F_{G2}\\) grösser sein: \\(F_{G2} - F_S = m_2 \\cdot a\\). Nur wenn alles still steht, ist \\(F_S = F_{G2}\\).' },
      { text: '\\(m_1 = 2\\;\\text{kg}\\), \\(m_2 = 0.5\\;\\text{kg}\\): Stelle ein, lass los und lies die Beschleunigung ab.', ok: function(s){ return hat(s, 2, 0.5); } },
      { text: 'Gesamtmasse \\(3\\;\\text{kg}\\), aber \\(a \\approx 3.27\\;\\text{m/s}^2\\): Stelle ein und lass los.', ok: function(s){ return hat(s, 2, 1); } },
      { text: 'Bei \\(m_2 = 1.5\\;\\text{kg}\\) soll der Wagen mit der halben Erdbeschleunigung fahren. Wähle \\(m_1\\) und lass los.', ok: function(s){ return hat(s, 1.5, 1.5); } },
      { text: 'Die Fadenkraft soll bei \\(m_1 = 1\\;\\text{kg}\\) rund \\(4.9\\;\\text{N}\\) betragen. Wähle \\(m_2\\) und lass los.', ok: function(s){ return hat(s, 1, 1); } },
      { text: 'Triff die gestrichelte Gerade: Wähle die Massen und lass los.', setup: function(S){ ziel = G / 5; S.setze({ m1: 3, m2: 1 }); }, ok: function(s){ return s.lauf && gl(s.lauf.a, G / 5); } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Die Kraft zur Mitte ----------
     Nimmt Animation 6 der Themenseite (F_z = m·v²/r) als Kugel an der Schnur: Sie kreist auf
     Knopfdruck, und «Schnur kappen» lässt sie tangential geradeaus fliegen — das
     Trägheitsgesetz, sobald die Zentripetalkraft fehlt. v grün tangential, F_z rot zur Mitte
     (STYLEGUIDE §5.2; die Themenseite zeigt v dort blau). Startwert = Clipbeispiel:
     m = 2 kg, v = 3 m/s, r = 1 m: F_z = 18 N. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg'), CX = 150, CY = 140, PXM = 60;   // 60 px je m (r bis 2 m)
    var B = Bedienung(fig, function(){ los = null; zeichnen(); });
    var phi = Math.PI / 4, los = null, schnitte = 0, arten = {}, pruefen = function(){}, letzt = 0;
    function werte(){ var m = B.wert('m'), v = B.wert('v'), r = B.wert('r'); return { m: m, v: v, r: r, az: v * v / r, Fz: m * v * v / r }; }
    var uhr = Uhr(function(tt){
      var w = werte(), dt = tt - letzt; letzt = tt;
      if (los){ los.s += w.v * dt; zeichnen(); if (los.s * PXM > 260) return false; return; }
      phi += w.v / w.r * dt; zeichnen();
    });
    var knoepfe = aktionen(fig, [
      ['kreisen', '▶ Kreisen', function(){ los = null; letzt = 0; if (uhr.laeuft()){ uhr.stop(); knoepfe.kreisen.textContent = '▶ Kreisen'; } else if (!WENIGER){ uhr.start(0); knoepfe.kreisen.textContent = '⏸ Anhalten'; } }],
      ['kappen', '✂ Schnur kappen', function(){ if (los) return; los = { phi: phi, s: 0 }; schnitte++; letzt = 0; knoepfe.kreisen.textContent = '▶ Kreisen'; if (WENIGER){ los.s = 300 / PXM; zeichnen(); } else uhr.start(0); }],
      ['zurueck', '↺ Zurück', function(){ uhr.stop(); los = null; phi = Math.PI / 4; knoepfe.kreisen.textContent = '▶ Kreisen'; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.schnitte = schnitte; w.bewegt = B.bewegt; w.arten = Object.keys(arten).length; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); los = null; zeichnen(); },
      aufraeumen: function(){ schnitte = 0; arten = {}; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte();
      B.anzeigen(); leeren(svg);
      if (Math.abs(w.az - 8) < 1e-9) arten[w.v + '|' + w.r] = true;
      var R = w.r * PXM;
      el(svg, 'circle', { cx: CX, cy: CY, r: R, 'class': 'bahn-kreis' });
      el(svg, 'circle', { cx: CX, cy: CY, r: 3.5, 'class': 'knoten' });
      var p = los ? los.phi : phi, c = Math.cos(p), s = Math.sin(p), X = CX + R * c, Y = CY - R * s;
      var tx = -s, ty = -c;                                  // Tangente in Drehrichtung (gegen den Uhrzeiger), Bildschirmkoordinaten
      var lv = w.v * 8;
      if (los){
        var bx = X + tx * los.s * PXM, by = Y + ty * los.s * PXM;
        el(svg, 'line', { x1: X, y1: Y, x2: bx, y2: by, 'class': 'flugbahn' });
        el(svg, 'line', { x1: CX, y1: CY, x2: CX + (X - CX) * 0.35, y2: CY + (Y - CY) * 0.35, 'class': 'schnur' });
        pfeil(svg, bx, by, bx + tx * lv, by + ty * lv, 'pf-v');
        el(svg, 'circle', { cx: bx, cy: by, r: 6 + w.m * 1.5, 'class': 'kugel' });
        el(svg, 'text', { x: 8, y: 274, 'class': 'bt-klein' }, 'Ohne Schnur keine Kraft zur Mitte: Die Kugel fliegt geradeaus weiter.');
      } else {
        el(svg, 'line', { x1: CX, y1: CY, x2: X, y2: Y, 'class': 'schnur' });
        pfeil(svg, X, Y, X + tx * lv, Y + ty * lv, 'pf-v'); marke(svg, X + tx * (lv + 11), Y + ty * (lv + 11) + 4, 'v', '', 'pf-text pf-v');
        var lf = Math.min(w.Fz * 2.5, R - 10), gekuerzt = w.Fz * 2.5 > R - 10;   // 2.5 px je N
        if (lf > 3) pfeil(svg, X, Y, X - c * lf, Y + s * lf, 'pf-z', 7);
        marke(svg, X - c * lf * 0.55 + s * 12, Y + s * lf * 0.55 + c * 12 + 4, 'F', 'z', 'pf-text pf-z');
        el(svg, 'circle', { cx: X, cy: Y, r: 6 + w.m * 1.5, 'class': 'kugel' });
        if (gekuerzt) el(svg, 'text', { x: 8, y: 274, 'class': 'bt-klein' }, 'Kraftpfeil gekürzt (passt nicht in den Kreis).');
      }
      rolle(fig, 'formel').innerHTML =
        '<span>' + v_('a') + '<sub>z</sub> = ' + v_('v') + '² / ' + v_('r') + ' = (' + zahl(w.v) + NB + 'm/s)² / ' + zahl(w.r) + NB + 'm ' + ist(w.az, sig(w.az)) + sig(w.az) + NB + 'm/s²</span>' +
        '<span>' + v_('F') + '<sub>z</sub> = ' + v_('m') + ' · ' + v_('a') + '<sub>z</sub> = ' + zahl(w.m) + NB + 'kg · ' + sig(w.az) + NB + 'm/s² ' + ist(w.Fz, sig(w.Fz)) + sig(w.Fz) + NB + 'N</span>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Lass die Kugel kreisen und kappe die Schnur zweimal an verschiedenen Stellen. In welche Richtung fliegt sie weg? Notiere deine Antwort.', ok: function(s){ return s.schnitte >= 2; },
        vergleich: 'Immer geradeaus in Richtung ihrer Geschwindigkeit, also tangential — nicht nach aussen. Ohne die Kraft der Schnur zur Mitte gilt das Trägheitsgesetz: Die Kugel behält Tempo und Richtung.' },
      { text: '\\(m = 1\\;\\text{kg}\\), \\(r = 2\\;\\text{m}\\), \\(v = 4\\;\\text{m/s}\\): Stelle ein und lies die Zentripetalkraft ab.', ok: function(s){ return gl(s.m, 1) && gl(s.r, 2) && gl(s.v, 4); } },
      { text: 'Bei \\(1\\;\\text{kg}\\) und \\(2\\;\\text{m}\\): Verdopple das Tempo von \\(3\\;\\text{m/s}\\) auf \\(6\\;\\text{m/s}\\). Um welchen Faktor wächst \\(F_z\\)? Notiere.', setup: function(S){ S.setze({ m: 1, r: 2, v: 3 }); }, ok: function(s){ return gl(s.m, 1) && gl(s.r, 2) && gl(s.v, 6); },
        vergleich: 'Vierfach, von \\(4.5\\;\\text{N}\\) auf \\(18\\;\\text{N}\\): Die Geschwindigkeit steht in \\(F_z = \\dfrac{m \\cdot v^2}{r}\\) im Quadrat.' },
      { text: 'Die Schnur hält höchstens \\(20\\;\\text{N}\\). Kugel \\(2\\;\\text{kg}\\) auf \\(r = 1.6\\;\\text{m}\\): Stelle das höchste Tempo ein.', ok: function(s){ return gl(s.m, 2) && gl(s.r, 1.6) && gl(s.v, 4); } },
      { text: 'Mit \\(m = 2\\;\\text{kg}\\) und \\(r = 2\\;\\text{m}\\) soll \\(F_z = 25\\;\\text{N}\\) sein. Stelle das Tempo ein.', ok: function(s){ return gl(s.m, 2) && gl(s.r, 2) && gl(s.v, 5); } },
      { text: 'Stelle \\(a_z = 8\\;\\text{m/s}^2\\) ein — auf zwei verschiedene Arten.', ok: function(s){ return s.arten >= 2; } }
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


    var G = 9.81, PI2 = 2 * Math.PI;
    function umr(k){ return '\\(' + ein(k, 'km/h') + ' = \\dfrac{' + tz(k) + '}{3.6}\\;\\text{m/s} ' + erg(k / 3.6, 'm/s') + '\\)'; }
    function qs(x){ return erg(x, 'm/s^2').replace('\\text{m/s^2}', '\\text{m/s}^2'); }   // Ergebnis in m/s²
    function es(x){ return ein(x, 'm/s^2').replace('\\text{m/s^2}', '\\text{m/s}^2'); }
    function paar(l, a, b){ return l.some(function(p){ return p[0] === a && p[1] === b; }); }

    var TYPEN = {
      /* ----- Kapitel 1 ----- */
      'fma': { felder: ['x'], muster: function(A){ return A.art === 'a' ? '<i>a</i> = {x} m/s²' : A.art === 'F' ? '<i>F</i> = {x} N' : '<i>m</i> = {x} kg'; },
        neu: function(){
          var r = Math.random(), F, m, a, gr = false, mg;
          if (r < 0.4){
            do {
              gr = Math.random() < 0.3;
              if (gr){ mg = zufall([200, 250, 400, 500, 800]); m = mg / 1000; F = zufall([1, 2, 3, 4, 6]); }
              else { m = zufall([1.5, 2, 3, 4, 5, 8, 12, 25, 60]); F = zufall([6, 12, 15, 24, 30, 45, 60, 150, 300]); }
              a = F / m;
            } while (a < 0.2 || a > 25 || F === m || F === 1 || Math.abs(a - 1) < 0.02 || paar([[4, 2], [6, 4], [12, 8], [10, 4], [9, 3]], F, m));   // Clip, Simulation 1
            return { art: 'a', x: a, F: F, m: m, gr: gr, mg: mg,
              text: 'Eine Gesamtkraft von \\(' + ein(F, 'N') + '\\) wirkt auf einen Körper mit \\(m = ' + (gr ? ein(mg, 'g') : ein(m, 'kg')) + '\\). Wie gross ist seine Beschleunigung?' };
          }
          if (r < 0.7){
            do { m = zufall([0.5, 2, 3, 6, 15, 70, 1200]); a = zufall([0.5, 1.5, 2, 2.5, 3, 4, 6]); } while (Math.abs(m * a - m / a) < 1e-9 || Math.abs(m * a - a / m) < 1e-9);
            return { art: 'F', x: m * a, m: m, a: a,
              text: 'Ein Körper mit \\(m = ' + ein(m, 'kg') + '\\) soll mit \\(a = ' + es(a) + '\\) beschleunigt werden. Welche Gesamtkraft ist nötig?' };
          }
          do { F = zufall([6, 18, 30, 48, 90, 240, 600]); a = zufall([0.5, 1.5, 2, 3, 4, 6]); } while (Math.abs(F / a - F * a) < 1e-9 || Math.abs(F / a - a / F) < 1e-9);
          return { art: 'm', x: F / a, F: F, a: a,
            text: 'Eine Gesamtkraft von \\(' + ein(F, 'N') + '\\) beschleunigt einen Körper mit \\(' + es(a) + '\\). Welche Masse hat er?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'a'){
            if (A.gr && nah(e.x, A.F / A.mg)) return 'Gramm in Kilogramm umrechnen: \\(' + ein(A.mg, 'g') + ' = ' + ein(A.m, 'kg') + '\\). Das Newton ist \\(\\text{kg} \\cdot \\text{m/s}^2\\).';
            if (nah(e.x, A.m / A.F)) return 'Umgekehrt: \\(a = \\dfrac{F}{m}\\) — Kraft durch Masse.';
            if (nah(e.x, A.F * A.m)) return 'Aus \\(F = m \\cdot a\\) folgt \\(a = \\dfrac{F}{m}\\): durch die Masse teilen.';
            return '\\(a = \\dfrac{F}{m}\\), \\(m\\) in kg.';
          }
          if (A.art === 'F'){
            if (nah(e.x, A.m / A.a) || nah(e.x, A.a / A.m)) return 'Kraft ist Masse <em>mal</em> Beschleunigung: \\(F = m \\cdot a\\).';
            return '\\(F = m \\cdot a\\).';
          }
          if (nah(e.x, A.F * A.a)) return 'Aus \\(F = m \\cdot a\\) folgt \\(m = \\dfrac{F}{a}\\): durch die Beschleunigung teilen.';
          if (nah(e.x, A.a / A.F)) return 'Umgekehrt: \\(m = \\dfrac{F}{a}\\).';
          return '\\(m = \\dfrac{F}{a}\\).'; },
        fehler: function(A){
          if (A.art === 'a'){ var l = [[{ x: String(A.m / A.F) }, 'Umgekehrt'], [{ x: String(A.F * A.m) }, 'teilen']]; if (A.gr) l.push([{ x: String(A.F / A.mg) }, 'Gramm']); return l; }
          if (A.art === 'F') return [[{ x: String(A.m / A.a) }, 'mal'], [{ x: String(A.x * 1.1) }, null]];
          return [[{ x: String(A.F * A.a) }, 'teilen'], [{ x: String(A.a / A.F) }, 'Umgekehrt']]; },
        loesung: function(A){
          if (A.art === 'a') return (A.gr ? ein(A.mg, 'g') + ' = ' + ein(A.m, 'kg') + ',\\quad ' : '') + 'a = \\dfrac{F}{m} = \\dfrac{' + ein(A.F, 'N') + '}{' + ein(A.m, 'kg') + '} ' + qs(A.x);
          if (A.art === 'F') return 'F = m \\cdot a = ' + ein(A.m, 'kg') + ' \\cdot ' + es(A.a) + ' ' + erg(A.x, 'N');
          return 'm = \\dfrac{F}{a} = \\dfrac{' + ein(A.F, 'N') + '}{' + es(A.a) + '} ' + erg(A.x, 'kg'); } },
      'anfahren': { felder: ['v', 's'], muster: '<i>v</i> = {v} m/s; <i>s</i> = {s} m',
        neu: function(){
          var F, m, t;
          do { F = zufall([20, 30, 60, 120, 240]); m = zufall([10, 15, 20, 40, 60, 80]); t = zufall([2, 3, 4, 5]); } while (F / m > 8 || F / m < 0.25 || (F === 120 && m === 80 && t === 4));   // Aufgabe 1a
          var a = F / m;
          return { v: a * t, s: 0.5 * a * t * t, a: a, F: F, m: m, t: t,
            text: 'Eine konstante Gesamtkraft von \\(' + ein(F, 'N') + '\\) beschleunigt einen Wagen (\\(m = ' + ein(m, 'kg') + '\\)) aus dem Stand. Wie schnell ist er nach \\(' + ein(t, 's') + '\\), und welchen Weg hat er dann zurückgelegt?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v) && nah(e.s, A.s)) return null;
          var r = [];
          if (!nah(e.v, A.v)){
            if (nah(e.v, A.F * A.t)) r.push('Zuerst die Beschleunigung: \\(a = \\dfrac{F}{m}\\), dann \\(v = a \\cdot t\\).');
            else r.push('\\(a = \\dfrac{F}{m}\\), dann \\(v = a \\cdot t\\).');
          }
          if (!nah(e.s, A.s) && !(!nah(e.v, A.v) && nah(e.s, 0.5 * e.v * A.t))){
            if (nah(e.s, A.a * A.t * A.t) || nah(e.s, A.v * A.t)) r.push('Der Faktor \\(\\tfrac12\\) fehlt: \\(s = \\tfrac12 \\cdot a \\cdot t^2\\) — die Fläche unter der \\(v\\)-\\(t\\)-Geraden ist ein Dreieck.');
            else r.push('\\(s = \\tfrac12 \\cdot a \\cdot t^2\\).');
          }
          return r.join(' '); },
        fehler: function(A){ return [[{ v: String(A.F * A.t), s: String(0.5 * A.F * A.t * A.t) }, 'Beschleunigung'], [{ v: String(A.v), s: String(A.v * A.t) }, 'Faktor']]; },
        loesung: function(A){ return 'a = \\dfrac{F}{m} = \\dfrac{' + ein(A.F, 'N') + '}{' + ein(A.m, 'kg') + '} ' + qs(A.a) + ',\\quad v = a \\cdot t = ' + es(+A.a.toPrecision(4)) + ' \\cdot ' + ein(A.t, 's') + ' ' + erg(A.v, 'm/s') + ',\\quad s = \\tfrac12 \\cdot a \\cdot t^2 ' + erg(A.s, 'm'); } },
      'faktor': { felder: ['x'], muster: '<i>a</i> wird {x}-mal so gross',
        neu: function(){
          var k1, k2;
          do { k1 = zufall([2, 3, 4, 0.5]); k2 = zufall([2, 3, 4, 0.5]); } while (k1 === k2 || (k1 === 3 && k2 === 0.5) || Math.abs(k1 * k2 - k1 / k2) < 1e-9 || Math.abs(k2 / k1 - k1 / k2) < 1e-9);   // Gesamttest G1
          function wort(k){ return k === 0.5 ? 'halbiert' : k === 2 ? 'verdoppelt' : k === 3 ? 'verdreifacht' : 'vervierfacht'; }
          return { x: k1 / k2, k1: k1, k2: k2, text: 'Die Kraft auf einen Körper wird ' + wort(k1) + ', seine Masse ' + wort(k2) + '. Wie ändert sich die Beschleunigung? (Faktor, Brüche wie \\(1/2\\) gehen)' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.k1 * A.k2)) return 'Mehr Masse heisst <em>weniger</em> Beschleunigung: durch den Massenfaktor teilen, \\(a = \\dfrac{F}{m}\\).';
          if (nah(e.x, A.k2 / A.k1)) return 'Umgekehrt: Die Kraft steht im Zähler, die Masse im Nenner.';
          return '\\(a = \\dfrac{F}{m}\\): Kraftfaktor durch Massenfaktor.'; },
        fehler: function(A){ return [[{ x: String(A.k1 * A.k2) }, 'teilen'], [{ x: String(A.k2 / A.k1) }, 'Umgekehrt']]; },
        loesung: function(A){ return 'a_\\text{neu} = \\dfrac{' + tz(A.k1) + ' \\cdot F}{' + tz(A.k2) + ' \\cdot m} = ' + tz(+(A.k1 / A.k2).toPrecision(4)) + ' \\cdot \\dfrac{F}{m}'; } },

      /* ----- Kapitel 2 ----- */
      'gesamt': { felder: ['F', 'a'], muster: '<i>F</i><sub>ges</sub> = {F} N; <i>a</i> = {a} m/s²',
        neu: function(){
          var m, FA, FW;
          do { m = zufall([20, 40, 50, 80, 120]); FA = zufall([60, 90, 120, 150, 200]); FW = zufall([20, 30, 40, 50, 70, 100]); }
          while (FA === FW || (m === 30) || (m === 40 && FA === 150 && FW === 70) || Math.abs((FA - FW) / m) > 6);   // Gesamttest G3
          return { F: FA - FW, a: (FA - FW) / m, m: m, FA: FA, FW: FW,
            text: 'Ein Schlitten (\\(m = ' + ein(m, 'kg') + '\\)) gleitet schon. Er wird mit \\(' + ein(FA, 'N') + '\\) nach vorn gezogen, die Reibung bremst mit \\(' + ein(FW, 'N') + '\\). Wie gross sind Gesamtkraft und Beschleunigung? (nach vorn positiv)' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F) && nah(e.a, A.a)) return null;
          var r = [];
          if (!nah(e.F, A.F)){
            if (nah(e.F, A.FA + A.FW)) r.push('Die Reibung zeigt nach hinten: Kräfte in Gegenrichtung werden abgezogen, \\(F_\\text{ges} = F_A - F_W\\).');
            else if (nah(e.F, -A.F)) r.push('Vorzeichen: nach vorn positiv, \\(F_\\text{ges} = F_A - F_W\\).');
            else r.push('\\(F_\\text{ges} = F_A - F_W\\).');
          }
          if (!nah(e.a, A.a) && !(!nah(e.F, A.F) && nah(e.a, e.F / A.m))){
            if (nah(e.a, A.FA / A.m)) r.push('Die Beschleunigung kommt von der <em>Gesamt</em>kraft, nicht vom Zug allein: \\(a = \\dfrac{F_\\text{ges}}{m}\\).');
            else r.push('\\(a = \\dfrac{F_\\text{ges}}{m}\\).');
          }
          return r.join(' '); },
        fehler: function(A){ return [[{ F: String(A.FA + A.FW), a: String((A.FA + A.FW) / A.m) }, 'abgezogen'], [{ F: String(A.F), a: String(A.FA / A.m) }, 'Gesamt']]; },
        loesung: function(A){ return 'F_\\text{ges} = F_A - F_W = ' + ein(A.FA, 'N') + ' - ' + ein(A.FW, 'N') + ' = ' + ein(A.F, 'N') + ',\\quad a = \\dfrac{F_\\text{ges}}{m} = \\dfrac{' + ein(A.F, 'N') + '}{' + ein(A.m, 'kg') + '} ' + qs(A.a); } },
      'konstant': { felder: ['F'], muster: '<i>F</i><sub>A</sub> = {F} N',
        neu: function(){
          var FW = zufall([150, 300, 450, 800, 1200]), m = zufall([900, 1200, 1500]);
          if (Math.random() < 0.4){
            var v = zufall([15, 20, 25, 30]);
            return { art: 'k', F: FW, FW: FW, m: m, v: v, text: 'Ein Auto (\\(m = ' + ein(m, 'kg') + '\\)) fährt mit konstant \\(' + ein(v, 'm/s') + '\\) geradeaus; der Fahrwiderstand beträgt \\(' + ein(FW, 'N') + '\\). Wie gross ist die Antriebskraft?' };
          }
          var a = zufall([0.5, 1, 1.5, 2]);
          return { art: 'b', F: m * a + FW, FW: FW, m: m, a: a, text: 'Ein Auto (\\(m = ' + ein(m, 'kg') + '\\)) soll gegen einen Fahrwiderstand von \\(' + ein(FW, 'N') + '\\) mit \\(' + es(a) + '\\) beschleunigen. Welche Antriebskraft ist nötig?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (A.art === 'k'){
            if (Math.abs(e.F) < 1e-9) return 'Ohne Antrieb würde der Widerstand das Auto bremsen. Bei konstantem Tempo ist die <em>Gesamt</em>kraft null: \\(F_A = F_W\\).';
            if (nah(e.F, A.m * A.v) || nah(e.F, A.m * G)) return 'Bei konstantem Tempo ist \\(a = 0\\), also \\(F_\\text{ges} = 0\\): Der Antrieb gleicht genau den Widerstand aus.';
            return '\\(F_\\text{ges} = F_A - F_W = 0\\).';
          }
          if (nah(e.F, A.m * A.a)) return 'Das ist die Gesamtkraft. Der Antrieb muss zusätzlich den Widerstand überwinden: \\(F_A = m \\cdot a + F_W\\).';
          if (nah(e.F, A.m * A.a - A.FW)) return 'Der Widerstand wirkt gegen die Fahrt: \\(F_A - F_W = m \\cdot a\\), also \\(F_A = m \\cdot a + F_W\\).';
          return '\\(F_A - F_W = m \\cdot a\\).'; },
        fehler: function(A){
          if (A.art === 'k') return [[{ F: '0' }, 'Gesamt'], [{ F: String(A.m * A.v) }, 'konstantem']];
          return [[{ F: String(A.m * A.a) }, 'zusätzlich'], [{ F: String(A.m * A.a - A.FW) }, 'gegen die Fahrt']]; },
        loesung: function(A){ return A.art === 'k' ? 'a = 0:\\quad F_A - F_W = 0,\\quad F_A = F_W = ' + ein(A.FW, 'N')
                                                    : 'F_A - F_W = m \\cdot a,\\quad F_A = m \\cdot a + F_W = ' + ein(A.m, 'kg') + ' \\cdot ' + es(A.a) + ' + ' + ein(A.FW, 'N') + ' = ' + ein(A.F, 'N'); } },
      'bremsen': { felder: ['a', 't'], muster: '<i>a</i> = {a} m/s²; <i>t</i> = {t} s',
        neu: function(){
          var m, v0, FW;
          do { m = zufall([40, 60, 80, 100]); v0 = zufall([4, 6, 8, 10]); FW = zufall([20, 30, 40, 60, 80]); }
          while ((m === 40 && v0 === 8 && FW === 70) || (m === 80 && v0 === 6 && FW === 40) || FW === m || Math.abs(v0 * m / FW - FW / m) < 1e-6 || v0 * m / FW > 40);   // Gesamttest, Simulation 2
          var a = -FW / m;
          return { a: a, t: v0 / -a, m: m, v0: v0, FW: FW,
            text: 'Ein Schlitten (\\(m = ' + ein(m, 'kg') + '\\)) gleitet mit \\(' + ein(v0, 'm/s') + '\\) ohne Antrieb weiter; die Reibung beträgt \\(' + ein(FW, 'N') + '\\). Wie gross ist die Beschleunigung (nach vorn positiv), und wie lange dauert es bis zum Stillstand?' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a) && nah(e.t, A.t)) return null;
          var r = [];
          if (!nah(e.a, A.a)){
            if (nah(e.a, -A.a)) r.push('Vorzeichen: Die Reibung zeigt nach hinten, der Schlitten wird langsamer — \\(a\\) ist negativ.');
            else r.push('\\(a = \\dfrac{F_\\text{ges}}{m} = \\dfrac{-F_W}{m}\\).');
          }
          if (!nah(e.t, A.t) && !(!nah(e.a, A.a) && nah(e.t, A.v0 / Math.abs(e.a)))){
            if (nah(e.t, A.v0 * Math.abs(A.a))) r.push('Aus \\(0 = v_0 + a \\cdot t\\) folgt \\(t = \\dfrac{v_0}{|a|}\\): durch die Verzögerung teilen.');
            else r.push('\\(t = \\dfrac{v_0}{|a|}\\).');
          }
          return r.join(' '); },
        fehler: function(A){ return [[{ a: String(-A.a), t: String(A.t) }, 'Vorzeichen'], [{ a: String(A.a), t: String(A.v0 * Math.abs(A.a)) }, 'teilen']]; },
        loesung: function(A){ return 'a = \\dfrac{-F_W}{m} = \\dfrac{' + ein(-A.FW, 'N') + '}{' + ein(A.m, 'kg') + '} ' + qs(A.a) + ',\\quad t = \\dfrac{v_0}{|a|} = \\dfrac{' + ein(A.v0, 'm/s') + '}{' + es(+Math.abs(A.a).toPrecision(4)) + '} ' + erg(A.t, 's'); } },

      /* ----- Kapitel 3 ----- */
      'gewicht': { felder: ['F'], muster: '<i>F</i><sub>G</sub> = {F} N',
        neu: function(){
          var O = zufall([['auf der Erde', 9.81], ['auf dem Mond', 1.62], ['auf dem Mars', 3.71]]), m = zufall([0.25, 2, 5, 12, 50, 75]);
          return { F: m * O[1], m: m, g: O[1], ort: O[0], text: 'Ein Körper mit \\(m = ' + ein(m, 'kg') + '\\) liegt ' + O[0] + ' (\\(g = ' + es(O[1]) + '\\)). Wie gross ist seine Gewichtskraft?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.m)) return 'Das ist die Masse in kg. Gefragt ist die Kraft in Newton: \\(F_G = m \\cdot g\\).';
          if (nah(e.F, A.m / A.g) || nah(e.F, A.g / A.m)) return 'Masse <em>mal</em> Ortsfaktor: \\(F_G = m \\cdot g\\).';
          if (A.g !== 9.81 && nah(e.F, A.m * 9.81)) return 'Hier gilt nicht der Ortsfaktor der Erde, sondern \\(g = ' + es(A.g) + '\\).';
          return '\\(F_G = m \\cdot g\\).'; },
        fehler: function(A){ var l = [[{ F: String(A.m / A.g) }, 'mal']]; if (A.m !== A.F) l.push([{ F: String(A.m) }, 'Masse in kg']); if (A.g !== 9.81) l.push([{ F: String(A.m * 9.81) }, 'Ortsfaktor der Erde']); return l; },
        loesung: function(A){ return 'F_G = m \\cdot g = ' + ein(A.m, 'kg') + ' \\cdot ' + es(A.g) + ' ' + erg(A.F, 'N'); } },
      'aufzug': { felder: ['F'], muster: '<i>F</i><sub>N</sub> = {F} N',
        neu: function(){
          var S, m, b;
          do { S = zufall([['fährt nach oben an', 1], ['bremst die Fahrt nach oben', -1], ['fährt nach unten an', -1], ['bremst die Fahrt nach unten', 1]]); m = zufall([45, 55, 65, 80, 95]); b = zufall([0.8, 1.2, 1.6, 2.5]); }
          while (m === 70 && b === 1.8);   // Themenseite A6
          var a = S[1] * b;
          return { F: m * (G + a), m: m, a: a, b: b, sit: S[0],
            text: 'Eine Person (\\(m = ' + ein(m, 'kg') + '\\)) steht im Aufzug auf einer Waage. Der Aufzug ' + S[0] + ', der Betrag der Beschleunigung ist \\(' + es(b) + '\\). Welche Normalkraft misst die Waage?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.m * (G - A.a))) return 'Richtung prüfen: Zeigt die Beschleunigung nach oben oder nach unten? Anfahren nach oben und Bremsen nach unten heisst \\(a\\) nach oben.';
          if (nah(e.F, A.m * G)) return 'So viel zeigt die Waage nur ohne Beschleunigung. Ansatz: \\(F_N - F_G = m \\cdot a\\).';
          if (nah(e.F, A.m * Math.abs(A.a))) return 'Das ist nur \\(m \\cdot a\\). Die Waage trägt auch die Gewichtskraft: \\(F_N = m \\cdot (g + a)\\).';
          return 'Ansatz (nach oben positiv): \\(F_N - F_G = m \\cdot a\\).'; },
        fehler: function(A){ return [[{ F: String(A.m * (G - A.a)) }, 'Richtung'], [{ F: String(A.m * G) }, 'ohne Beschleunigung'], [{ F: String(A.m * A.b) }, 'nur']]; },
        loesung: function(A){ return 'F_N - F_G = m \\cdot a,\\quad F_N = m \\cdot (g + a) = ' + ein(A.m, 'kg') + ' \\cdot (9.81\\;\\text{m/s}^2 + (' + tz(A.a) + '\\;\\text{m/s}^2)) ' + erg(A.F, 'N'); } },
      'anzeige': { felder: ['a'], muster: '<i>a</i> = {a} m/s²',
        neu: function(){
          var m, k;
          do { m = zufall([50, 60, 75, 80]); k = zufall([-0.2, -0.15, -0.1, 0.1, 0.15, 0.2, 0.25]); } while (m === 60 && k === -52 / 60 + 1);
          var X0 = +(m * (1 + k)).toFixed(1);
          if (Math.abs((X0 - m) - G * X0 / m) < 0.02 * G * X0 / m) return TYPEN.anzeige.neu();
          var X = +(m * (1 + k)).toFixed(1);
          return { a: G * (X - m) / m, m: m, X: X,
            text: 'In Ruhe zeigt die Waage im Aufzug \\(' + ein(m, 'kg') + '\\) an, während der Fahrt \\(' + ein(X, 'kg') + '\\). Wie gross ist die Beschleunigung des Aufzugs? (nach oben positiv)' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a)) return null;
          if (nah(e.a, -A.a)) return 'Vorzeichen: Zeigt die Waage mehr als in Ruhe, ist die Beschleunigung nach oben gerichtet, also positiv.';
          if (nah(e.a, A.X - A.m)) return 'Die Anzeige ist \\(\\dfrac{F_N}{g}\\). Aus \\(F_N - m \\cdot g = m \\cdot a\\) folgt \\(a = g \\cdot \\dfrac{\\text{Anzeige} - m}{m}\\).';
          if (nah(e.a, G * A.X / A.m)) return 'Das ist \\(g + a\\). Die Beschleunigung ist nur der Unterschied zu \\(g\\).';
          return 'Ansatz: \\(F_N - F_G = m \\cdot a\\) mit \\(F_N = \\text{Anzeige} \\cdot g\\).'; },
        fehler: function(A){ return [[{ a: String(-A.a) }, 'Vorzeichen'], [{ a: String(A.X - A.m) }, 'Anzeige ist'], [{ a: String(G * A.X / A.m) }, 'Unterschied']]; },
        loesung: function(A){ return 'F_N - F_G = m \\cdot a,\\quad a = \\dfrac{F_N - F_G}{m} = \\dfrac{' + ein(A.X, 'kg') + ' \\cdot g - ' + ein(A.m, 'kg') + ' \\cdot g}{' + ein(A.m, 'kg') + '} ' + qs(A.a); } },

      /* ----- Kapitel 4 ----- */
      'faden': { felder: ['a', 'F'], muster: '<i>a</i> = {a} m/s²; <i>F</i><sub>S</sub> = {F} N',
        neu: function(){
          var m1, m2;
          do { m1 = zufall([0.5, 1, 2, 2.5, 4, 5]); m2 = zufall([0.2, 0.3, 0.5, 1, 1.5, 2]); }
          while (paar([[3, 1], [2, 0.5], [2, 1], [1.5, 1.5], [1, 1]], m1, m2) || (m1 === 2.5 && m2 === 1));   // Clip, Simulation 4, Gesamttest
          var a = m2 * G / (m1 + m2);
          return { a: a, F: m1 * a, m1: m1, m2: m2,
            text: 'Ein Wagen (\\(m_1 = ' + ein(m1, 'kg') + '\\)) steht auf einem reibungsfreien Tisch. Über eine Rolle zieht ihn ein hängender Körper (\\(m_2 = ' + ein(m2, 'kg') + '\\)). Beschleunigung und Fadenkraft? (Faden und Rolle masselos)' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a) && nah(e.F, A.F)) return null;
          var r = [];
          if (!nah(e.a, A.a)){
            if (nah(e.a, A.m2 * G / A.m1)) r.push('Die Gewichtskraft von \\(m_2\\) beschleunigt <em>beide</em> Körper: \\(a = \\dfrac{m_2 \\cdot g}{m_1 + m_2}\\).');
            else if (nah(e.a, G)) r.push('Frei fallen würde \\(m_2\\) mit \\(g\\). Hier muss es den Wagen mitziehen.');
            else r.push('\\(a = \\dfrac{m_2 \\cdot g}{m_1 + m_2}\\).');
          }
          if (!nah(e.F, A.F) && !(!nah(e.a, A.a) && nah(e.F, A.m1 * e.a))){
            if (nah(e.F, A.m2 * G)) r.push('Die Fadenkraft ist kleiner als die Gewichtskraft von \\(m_2\\) — sonst würde \\(m_2\\) nicht beschleunigen. Am Wagen allein: \\(F_S = m_1 \\cdot a\\).');
            else r.push('Am Wagen allein: \\(F_S = m_1 \\cdot a\\).');
          }
          return r.join(' '); },
        fehler: function(A){ var a2 = A.m2 * G / A.m1; return [[{ a: String(a2), F: String(A.m1 * a2) }, 'beide'], [{ a: String(A.a), F: String(A.m2 * G) }, 'kleiner']]; },
        loesung: function(A){ return 'a = \\dfrac{m_2 \\cdot g}{m_1 + m_2} = \\dfrac{' + ein(A.m2, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2}{' + ein(+(A.m1 + A.m2).toFixed(2), 'kg') + '} ' + qs(A.a) + ',\\quad F_S = m_1 \\cdot a ' + erg(A.F, 'N'); } },
      'zug': { felder: ['a', 'F'], muster: '<i>a</i> = {a} m/s²; <i>F</i><sub>K</sub> = {F} N',
        neu: function(){
          var m1 = zufall([800, 1000, 1200, 1500, 3000]), m2 = zufall([300, 500, 600, 800, 1500]), F = zufall([1500, 2000, 2400, 3000, 4500]);
          var a = F / (m1 + m2);
          return { a: a, F: m2 * a, m1: m1, m2: m2, FA: F,
            text: 'Ein Auto (\\(' + ein(m1, 'kg') + '\\)) zieht einen Anhänger (\\(' + ein(m2, 'kg') + '\\)) mit einer Antriebskraft von \\(' + ein(F, 'N') + '\\); Widerstände vernachlässigt. Beschleunigung und Kraft in der Kupplung?' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a) && nah(e.F, A.F)) return null;
          var r = [];
          if (!nah(e.a, A.a)){
            if (nah(e.a, A.FA / A.m1)) r.push('Die Antriebskraft beschleunigt Auto <em>und</em> Anhänger: \\(a = \\dfrac{F}{m_1 + m_2}\\).');
            else r.push('\\(a = \\dfrac{F}{m_1 + m_2}\\).');
          }
          if (!nah(e.F, A.F) && !(!nah(e.a, A.a) && nah(e.F, A.m2 * e.a))){
            if (nah(e.F, A.FA)) r.push('Die Kupplung muss nur den Anhänger beschleunigen: \\(F_K = m_2 \\cdot a\\).');
            else if (nah(e.F, A.m1 * A.a)) r.push('Das ist die Kraft für das Auto. Die Kupplung zieht den Anhänger: \\(F_K = m_2 \\cdot a\\).');
            else r.push('\\(F_K = m_2 \\cdot a\\).');
          }
          return r.join(' '); },
        fehler: function(A){ var a2 = A.FA / A.m1; return [[{ a: String(a2), F: String(A.m2 * a2) }, 'und'], [{ a: String(A.a), F: String(A.FA) }, 'nur den Anhänger']]; },
        loesung: function(A){ return 'a = \\dfrac{F}{m_1 + m_2} = \\dfrac{' + ein(A.FA, 'N') + '}{' + ein(A.m1 + A.m2, 'kg') + '} ' + qs(A.a) + ',\\quad F_K = m_2 \\cdot a ' + erg(A.F, 'N'); } },
      'faden_m2': { felder: ['m'], muster: '<i>m</i><sub>2</sub> = {m} kg',
        neu: function(){
          var m1, m2;
          do { m1 = zufall([1, 2, 3, 4]); m2 = zufall([0.4, 0.5, 0.8, 1, 1.2, 2]); } while (paar([[3, 1], [2, 0.5], [2, 1], [1, 1]], m1, m2));
          var a = +(m2 * G / (m1 + m2)).toPrecision(3);
          return { m: m1 * a / (G - a), m1: m1, a: a,
            text: 'Ein Wagen (\\(m_1 = ' + ein(m1, 'kg') + '\\)) wird auf dem reibungsfreien Tisch von einem hängenden Körper über eine Rolle gezogen. Gemessen wird \\(a = ' + es(a) + '\\). Welche Masse hat der hängende Körper?' }; },
        pruefen: function(A, e){
          if (nah(e.m, A.m, 0.012)) return null;
          if (nah(e.m, A.m1 * A.a / G, 0.012)) return 'Die Gewichtskraft von \\(m_2\\) beschleunigt beide Körper: \\(m_2 \\cdot g = (m_1 + m_2) \\cdot a\\). \\(m_2\\) steht auf beiden Seiten — zusammenfassen.';
          if (nah(e.m, A.m1 * A.a / (G + A.a), 0.012)) return 'Beim Umstellen von \\(m_2 \\cdot g = (m_1 + m_2) \\cdot a\\): \\(m_2 \\cdot (g - a) = m_1 \\cdot a\\).';
          return 'Ansatz: \\(m_2 \\cdot g = (m_1 + m_2) \\cdot a\\), nach \\(m_2\\) auflösen.'; },
        fehler: function(A){ return [[{ m: String(A.m1 * A.a / G) }, 'beide'], [{ m: String(A.m1 * A.a / (G + A.a)) }, 'Umstellen']]; },
        loesung: function(A){ return 'm_2 \\cdot g = (m_1 + m_2) \\cdot a,\\quad m_2 = \\dfrac{m_1 \\cdot a}{g - a} = \\dfrac{' + ein(A.m1, 'kg') + ' \\cdot ' + es(A.a) + '}{9.81\\;\\text{m/s}^2 - ' + es(A.a) + '} ' + erg(A.m, 'kg'); } },

      /* ----- Kapitel 5 ----- */
      'zentri': { felder: ['F'], muster: '<i>F</i><sub>z</sub> = {F} N',
        neu: function(){
          var kh = Math.random() < 0.4, m, v, vk, r;
          do {
            if (kh){ m = zufall([60, 80, 1000, 1200]); vk = zufall([18, 36, 54, 72]); v = vk / 3.6; r = zufall([20, 40, 60, 100]); }
            else { m = zufall([0.2, 0.5, 2, 3, 5]); v = zufall([2, 3, 5, 6, 8]); r = zufall([0.5, 0.8, 1.2, 2, 3]); }
          } while (v * v / r > 50 || (kh && v * v / r > 7) || (!kh && m === 2 && v === 3 && r === 1) || m === v || Math.abs(v - 1) < 1e-9 || Math.abs(r - 1) < 1e-9);   // Clip
          return { F: m * v * v / r, m: m, v: v, vk: vk, kh: kh, r: r,
            text: (kh ? 'Ein Fahrzeug (\\(m = ' + ein(m, 'kg') + '\\)) fährt mit \\(' + ein(vk, 'km/h') + '\\) durch eine Kurve mit \\(r = ' + ein(r, 'm') + '\\).' : 'Ein Körper (\\(m = ' + ein(m, 'kg') + '\\)) kreist an einer Schnur mit \\(' + ein(v, 'm/s') + '\\) auf \\(r = ' + ein(r, 'm') + '\\).') + ' Wie gross ist die Zentripetalkraft?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (A.kh && nah(e.F, A.m * A.vk * A.vk / A.r)) return 'Erst in m/s umrechnen: ' + umr(A.vk) + '.';
          if (nah(e.F, A.v * A.v / A.r)) return 'Das ist die Zentripetal<em>beschleunigung</em>. Die Kraft ist Masse mal Beschleunigung: \\(F_z = m \\cdot a_z\\).';
          if (nah(e.F, A.m * A.v / A.r)) return 'Die Geschwindigkeit steht im Quadrat: \\(F_z = \\dfrac{m \\cdot v^2}{r}\\).';
          if (nah(e.F, A.m * A.v * A.v * A.r)) return 'Durch den Radius teilen: \\(F_z = \\dfrac{m \\cdot v^2}{r}\\).';
          return '\\(F_z = \\dfrac{m \\cdot v^2}{r}\\) mit \\(v\\) in m/s.'; },
        fehler: function(A){ var l = [[{ F: String(A.m * A.v / A.r) }, 'Quadrat'], [{ F: String(A.m * A.v * A.v * A.r) }, 'teilen']]; if (A.m !== 1) l.push([{ F: String(A.v * A.v / A.r) }, 'beschleunigung']); if (A.kh) l.push([{ F: String(A.m * A.vk * A.vk / A.r) }, 'umrechnen']); return l; },
        loesung: function(A){ return (A.kh ? 'v = \\dfrac{' + tz(A.vk) + '}{3.6}\\;\\text{m/s} = ' + ein(A.v, 'm/s') + ',\\quad ' : '') + 'F_z = \\dfrac{m \\cdot v^2}{r} = \\dfrac{' + ein(A.m, 'kg') + ' \\cdot (' + ein(A.v, 'm/s') + ')^2}{' + ein(A.r, 'm') + '} ' + erg(A.F, 'N'); } },
      'vmax': { felder: ['v'], muster: '<i>v</i><sub>max</sub> = {v} m/s',
        neu: function(){
          var F, m, r, v;
          do { F = zufall([20, 50, 80, 120, 200]); m = zufall([0.5, 1, 2, 4]); r = zufall([0.5, 0.8, 1.2, 2]); v = Math.sqrt(F * r / m); } while (v > 20 || (F === 20 && m === 2 && r === 1.6) || Math.abs(F * r / m - 1) < 1e-9);   // Simulation 5
          return { v: v, F: F, m: m, r: r,
            text: 'Eine Schnur hält höchstens \\(' + ein(F, 'N') + '\\). Eine Kugel (\\(m = ' + ein(m, 'kg') + '\\)) soll daran auf \\(r = ' + ein(r, 'm') + '\\) kreisen. Wie schnell darf sie höchstens sein?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, A.F * A.r / A.m)) return 'Das ist \\(v^2\\). Noch die Wurzel ziehen: \\(v = \\sqrt{\\dfrac{F_z \\cdot r}{m}}\\).';
          if (nah(e.v, Math.sqrt(A.F / (A.m * A.r)))) return 'Beim Umstellen: \\(F_z = \\dfrac{m \\cdot v^2}{r}\\) mal \\(r\\), durch \\(m\\) — der Radius kommt in den Zähler.';
          return '\\(F_z = \\dfrac{m \\cdot v^2}{r}\\) nach \\(v\\) auflösen.'; },
        fehler: function(A){ return [[{ v: String(A.F * A.r / A.m) }, 'Wurzel'], [{ v: String(Math.sqrt(A.F / (A.m * A.r))) }, 'Zähler']]; },
        loesung: function(A){ return 'v = \\sqrt{\\dfrac{F_z \\cdot r}{m}} = \\sqrt{\\dfrac{' + ein(A.F, 'N') + ' \\cdot ' + ein(A.r, 'm') + '}{' + ein(A.m, 'kg') + '}} ' + erg(A.v, 'm/s'); } },
      'omega': { felder: ['F'], muster: '<i>F</i><sub>z</sub> = {F} N',
        neu: function(){
          var m = zufall([0.5, 1, 2, 60, 75]), T = zufall([0.5, 2, 4, 5, 8]), r = zufall([0.4, 1.5, 2.5, 4]);
          return { F: m * Math.pow(PI2 / T, 2) * r, m: m, T: T, r: r,
            text: 'Ein Körper (\\(m = ' + ein(m, 'kg') + '\\)) läuft gleichförmig auf einem Kreis mit \\(r = ' + ein(r, 'm') + '\\) um; ein Umlauf dauert \\(T = ' + ein(T, 's') + '\\). Wie gross ist die Zentripetalkraft?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.m * A.r / (A.T * A.T))) return '\\(\\omega = \\dfrac{2\\pi}{T}\\) — der Faktor \\(2\\pi\\) fehlt.';
          if (nah(e.F, A.m * PI2 / A.T * A.r)) return 'Die Winkelgeschwindigkeit steht im Quadrat: \\(F_z = m \\cdot \\omega^2 \\cdot r\\).';
          if (nah(e.F, A.m * Math.pow(PI2 * A.T, 2) * A.r)) return 'Umgekehrt: \\(\\omega = \\dfrac{2\\pi}{T}\\), nicht \\(2\\pi \\cdot T\\).';
          return '\\(\\omega = \\dfrac{2\\pi}{T}\\), dann \\(F_z = m \\cdot \\omega^2 \\cdot r\\).'; },
        fehler: function(A){ return [[{ F: String(A.m * A.r / (A.T * A.T)) }, '2\\pi'], [{ F: String(A.m * PI2 / A.T * A.r) }, 'Quadrat'], [{ F: String(A.m * Math.pow(PI2 * A.T, 2) * A.r) }, 'Umgekehrt']]; },
        loesung: function(A){ return '\\omega = \\dfrac{2\\pi}{T} = \\dfrac{2\\pi}{' + ein(A.T, 's') + '} ' + erg(PI2 / A.T, 'rad/s') + ',\\quad F_z = m \\cdot \\omega^2 \\cdot r = ' + ein(A.m, 'kg') + ' \\cdot (' + ein(+(PI2 / A.T).toPrecision(4), 'rad/s') + ')^2 \\cdot ' + ein(A.r, 'm') + ' ' + erg(A.F, 'N'); } }
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

  /* ---------- Minigrafen: Geraden zum Ablesen ----------
     <svg class="mini" data-geraden="m1;m2,q2" data-namen="A;B" data-farbe="kurve-s" data-fenster="x1,y1"
          data-teilung="sx,sy" data-xname data-yname data-punkte="x,y;…">
     Eine Gerade ist «m» (Ursprungsgerade) oder «m,q» (mit Achsenabschnitt).
     Punkte auf Gitterpunkten, damit sich Steigung und Achsenabschnitt ablesen lassen. */
  document.querySelectorAll('svg.mini[data-geraden]').forEach(function(svg){
    var fe = svg.dataset.fenster.split(',').map(Number), tl = (svg.dataset.teilung || '1,1').split(',').map(Number);
    var xm = [], ym = [], i;
    for (i = 2 * tl[0]; i <= fe[0] + 1e-9; i += 2 * tl[0]) xm.push(+i.toPrecision(6));
    for (i = 2 * tl[1]; i <= fe[1] + 1e-9; i += 2 * tl[1]) ym.push(+i.toPrecision(6));
    var w = 170, h = 150;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h); svg.setAttribute('role', 'img');
    var K = Achsen(svg, { w: w, h: h, x0: -fe[0] * 0.16, x1: fe[0] * 1.06, y0: -fe[1] * 0.14, y1: fe[1] * 1.08, sx: tl[0], sy: tl[1], xm: xm, ym: ym, r: 3, pfeil: 6, xname: svg.dataset.xname, yname: svg.dataset.yname });
    var namen = (svg.dataset.namen || '').split(';');
    var alle = svg.dataset.geraden.split(';').map(function(g){ return g.split(',').map(Number); });
    var flachste = Math.min.apply(null, alle.map(function(p){ return p[0]; }));
    svg.dataset.geraden.split(';').forEach(function(g, k){
      var p = g.split(',').map(Number), m = p[0], q = p[1] || 0;
      K.kurve(function(x){ return m * x + q; }, 'kurve-mini ' + (svg.dataset.farbe || ''), 0);
      // Name über dem Ende der Geraden, Versatz in Fensteranteilen (nicht in Dateneinheiten)
      if (namen[k]){ var xe = m > 0 ? Math.min(fe[0], (fe[1] - q) / m) * 0.97 : fe[0] * 0.97; K.text(xe - fe[0] * 0.03, m * xe + q + fe[1] * (alle.length > 1 && m === flachste ? -0.1 : 0.05), namen[k], 'mini-name', 'end'); }   // am rechten Ende, die flachste Gerade unten beschriftet: Namen treffen sich nicht
    });
    if (svg.dataset.punkte) svg.dataset.punkte.split(';').forEach(function(p){ var q = p.split(',').map(Number); K.punkt(q[0], q[1], 'p-mini'); });
  });
})();
</script>
