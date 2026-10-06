<script>
/* Leitprogramm Energie — laufende Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr, Übungsrahmen,
   Minigrafen) wörtlich aus dem Leitprogramm Dynamik; neu sind die Simulationen (Arbeit als
   Fläche, Bremsen und Energie-Parabel, Achterbahn, Rampe mit Reibung und Motor, Kran mit
   Wirkungsgrad, Energiebilanz der Erde) und die Übungstypen für 4.3. g = 9.81 m/s² wie
   Themenseite 4.3. Farben wie dort: Lageenergie Bernstein, Bewegungsenergie Grün, Wärme Rot,
   zugeführte Energie und Kräfte Blau, Kraftanteil in Wegrichtung Violett (STYLEGUIDE §5.2).
   Zahlen mit Dezimalpunkt und echtem Minus; «·» nur als Malpunkt, Trenner ist der Strichpunkt. */
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


  var G = 9.81;                                          // wie Themenseite 4.3
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

  /* ---------- Energiebalken: stehende Säulen mit Wert darunter ----------
     liste: [{ name, wert (J), cls }]; skala in px je J; Säulen nebeneinander ab x. */
  function saeulen(eltern, x, basis, breite, abstand, liste, skala, einheit){
    liste.forEach(function(s, k){
      var h = Math.max(0, s.wert * skala), xx = x + k * (breite + abstand);
      el(eltern, 'rect', { x: xx, y: basis - h, width: breite, height: h, 'class': 'saeule ' + s.cls });
      el(eltern, 'line', { x1: xx - 3, y1: basis, x2: xx + breite + 3, y2: basis, 'class': 'achse' });
      var t = el(eltern, 'text', { x: xx + breite / 2, y: basis + 13, 'text-anchor': 'middle', 'class': 'bt-klein' });
      t.textContent = s.name;
      el(eltern, 'text', { x: xx + breite / 2, y: basis + 25, 'text-anchor': 'middle', 'class': 'bt-wert' }, (s.wert < 1 ? '0' : sig(s.wert / (einheit || 1))) + NB + (einheit === 1000 ? 'kJ' : 'J'));
    });
  }
  function wurzel(x){ return Math.sqrt(Math.max(0, x)); }

  /* ---------- Kapitel 1: Arbeit ----------
     Nimmt Animation 1 der Themenseite (Arbeit als Fläche im Kraft-Weg-Diagramm) als laufende
     Szene: Eine Kiste wird mit der Kraft F unter dem Winkel α gezogen; nur der Anteil
     F_s = F · cos α in Wegrichtung verrichtet Arbeit. Während der Fahrt füllt sich die Fläche
     unter F_s im Diagramm. Kraft Blau, Anteil in Wegrichtung Violett (Komponente, STYLEGUIDE
     §5.2). Startwert = Clipbeispiel: F = 200 N, α = 0°, s = 5 m: W = 1000 J. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), X0 = 20, PX = 30;              // 30 px je m, Bahn 8 m
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,126)' });
    var K = Achsen(dia, { w: 300, h: 180, x0: -0.6, x1: 8.8, y0: -45, y1: 440, sx: 1, sy: 50, xm: [2, 4, 6, 8], ym: [100, 200, 300, 400], xname: 's [m]', yname: 'Fₛ [N]' });
    var B = Bedienung(fig, function(){ uhr.stop(); x = 0; zeichnen(); });
    var x = 0, vorher = null, letzter = null, lauf = null, laeufe = [], ziel = null, pruefen = function(){};
    function werte(){ var F = B.wert('F'), a = B.wert('al'), s = B.wert('s'), Fs = F * Math.cos(a * Math.PI / 180); return { F: F, a: a, s: s, Fs: Fs, W: Fs * s }; }
    var uhr = Uhr(function(tt){
      var w = werte(); x = Math.min(tt * 2, w.s); zeichnen();                 // 2 m/s zur Anschauung
      if (x >= w.s){ letzter = w; lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Ziehen', function(){ vorher = letzter; if (WENIGER){ var w = werte(); x = w.s; letzter = w; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); x = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); x = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; lauf = null; laeufe = []; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), r = w.a * Math.PI / 180, c = Math.cos(r), sn = Math.sin(r);
      B.anzeigen(); leeren(szene); K.leeren();
      el(szene, 'line', { x1: 8, y1: 96, x2: 292, y2: 96, 'class': 'boden' });
      for (var k = 0; k <= 8; k += 2) el(szene, 'text', { x: X0 + 14 + k * PX, y: 110, 'text-anchor': 'middle', 'class': 'skala' }, k + ' m');
      var bx = X0 + x * PX;
      el(szene, 'rect', { x: bx, y: 72, width: 28, height: 24, rx: 2, 'class': 'kiste' });
      var ax = bx + 28, ay = 80;
      var ls = Math.min(62, (296 - ax) / Math.max(c, 0.2));                // Seil bleibt im Bild
      el(szene, 'line', { x1: ax, y1: ay, x2: ax + ls * c, y2: ay - ls * sn, 'class': 'seil' });
      // Kraft (0.12 px je N) längs des Seils, ihr Anteil in Wegrichtung waagrecht darunter
      var lf = Math.min(w.F * 0.12, ls);
      if (lf > 2){ pfeil(szene, ax, ay, ax + lf * c, ay - lf * sn, 'pf-f'); marke(szene, ax + lf * c + 7, ay - lf * sn - 3, 'F', '', 'pf-text pf-f', 'start'); }
      if (w.Fs * 0.12 > 2 && w.a > 0){ pfeil(szene, ax, 90, ax + w.Fs * 0.12, 90, 'pf-a', 6); el(szene, 'line', { x1: ax + lf * c, y1: ay - lf * sn, x2: ax + lf * c, y2: 90, 'class': 'hilfslinie' }); marke(szene, ax + w.Fs * 0.12 + 5, 93, 'F', 's', 'pf-text pf-a', 'start'); }
      el(szene, 'text', { x: ax + 16, y: ay - 4, 'class': 'bt-klein' }, w.a > 0 ? 'α = ' + zahl(w.a) + '°' : '');
      // Diagramm: Fläche unter F_s bis zur aktuellen Stelle
      if (ziel) K.rechteck(0, 0, ziel.s, ziel.Fs, 'zielflaeche');
      if (vorher) K.rechteck(0, 0, vorher.s, vorher.Fs, 'vorher-flaeche');
      if (x > 0) K.rechteck(0, 0, x, w.Fs, 'flaeche-w');
      K.kurve(function(){ return w.Fs; }, 'kurve-fs', 0, w.s);
      if (x > 0) K.text(x / 2, w.Fs / 2, 'W', 'flaeche-name');
      var z = '<span>' + v_('W') + ' = ' + v_('F') + ' · ' + v_('s') + ' · cos ' + v_('α') + ' = ' + zahl(w.F) + NB + 'N · ' + zahl(w.s) + NB + 'm · cos ' + zahl(w.a) + '° ' + ist(w.W, sig(w.W)) + sig(w.W) + NB + 'J</span>';
      z += '<span class="sim-notiz">' + (w.a > 0 ? 'Nur der Anteil in Wegrichtung, ' + v_('F') + '<sub>s</sub> = ' + v_('F') + ' · cos ' + v_('α') + ', verrichtet Arbeit. ' : '') + 'Die Arbeit ist die Fläche unter ' + v_('F') + '<sub>s</sub> im Diagramm.</span>';
      if (vorher) z += '<span class="sim-notiz">Gestrichelt grau: der vorige Zug.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, F, a, w){ return s.lauf && s.lauf.F === F && s.lauf.a === a && s.lauf.s === w; }
    pruefen = Leiste(fig, [
      { text: 'Zieh die Kiste dreimal mit derselben Kraft und demselben Weg, aber unter drei verschiedenen Winkeln. Wie hängt die Arbeit vom Winkel ab? Notiere deine Antwort.', ok: function(s){ var l = s.laeufe, n = {}; l.forEach(function(a){ if (a.F === l[l.length - 1].F && a.s === l[l.length - 1].s) n[a.a] = true; }); return l.length && Object.keys(n).length >= 3; },
        vergleich: 'Je grösser der Winkel, desto kleiner die Arbeit: Nur der Anteil \\(F_s = F \\cdot \\cos\\alpha\\) in Wegrichtung zählt, und \\(\\cos\\alpha\\) wird mit dem Winkel kleiner. Bei \\(90^\\circ\\) wäre er null — eine Kraft senkrecht zum Weg verrichtet keine Arbeit.' },
      { text: 'Zieh die Kiste waagrecht mit \\(250\\;\\text{N}\\) über \\(6\\;\\text{m}\\). Wie gross ist die Arbeit?', ok: function(s){ return hat(s, 250, 0, 6); } },
      { text: 'Jetzt dieselbe Kraft, derselbe Weg, aber das Seil steigt unter \\(60^\\circ\\) an. Zieh und vergleiche mit Aufgabe 2: Welcher Teil der Arbeit bleibt? Notiere deine Antwort.', ok: function(s){ return hat(s, 250, 60, 6); },
        vergleich: 'Die Hälfte: \\(W = 250\\;\\text{N} \\cdot 6\\;\\text{m} \\cdot \\cos 60^\\circ = 750\\;\\text{J}\\) statt \\(1500\\;\\text{J}\\), weil \\(\\cos 60^\\circ = 0.5\\). Nur der Anteil in Wegrichtung, \\(F_s = 125\\;\\text{N}\\), verrichtet Arbeit.' },
      { text: 'Waagrecht gezogen sollen auf \\(4\\;\\text{m}\\) genau \\(600\\;\\text{J}\\) Arbeit verrichtet werden. Welche Kraft braucht es? Stelle ein und zieh.', ok: function(s){ return hat(s, 150, 0, 4); } },
      { text: 'Mit \\(300\\;\\text{N}\\) über \\(8\\;\\text{m}\\) sollen nur \\(1200\\;\\text{J}\\) Arbeit herauskommen. Unter welchem Winkel? Stelle ein und zieh.', ok: function(s){ return hat(s, 300, 60, 8); } },
      { text: 'Triff die gestrichelte Fläche genau: Stelle Kraft, Winkel und Weg ein und zieh. Wie viel Arbeit stellt die Fläche dar? Notiere deine Antwort.', setup: function(S){ ziel = { s: 6, Fs: 160 }; S.setze({ F: 100, al: 20, s: 3 }); }, ok: function(s){ return s.lauf && s.lauf.s === 6 && Math.abs(s.lauf.Fs - 160) < 1e-6; },
        vergleich: 'Die Fläche ist \\(W = F_s \\cdot s = 160\\;\\text{N} \\cdot 6\\;\\text{m} = 960\\;\\text{J}\\). Getroffen hat jede Einstellung mit \\(F \\cdot \\cos\\alpha = 160\\;\\text{N}\\), etwa \\(160\\;\\text{N}\\) waagrecht oder \\(320\\;\\text{N}\\) unter \\(60^\\circ\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Bewegungsenergie und Bremsweg ----------
     Nimmt Animation 2 der Themenseite (Energie-Parabel E_kin(v)) als Bremsung: Ein Auto
     bremst mit konstanter Kraft F_B; die Bremsarbeit F_B · s nimmt ihm die ganze
     Bewegungsenergie. Während der Bremsung gleitet der Punkt die Parabel hinunter. Doppeltes
     Tempo: vierfache Energie, vierfacher Bremsweg. Startwert = Clipbeispiel: 1000 kg, 10 m/s,
     F_B = 5000 N: E_kin = 50 kJ, s = 10 m. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), X0 = 18, PX = 1.65;              // 1.65 px je m, Strasse 160 m
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,122)' });
    var K = Achsen(dia, { w: 300, h: 190, x0: -1.5, x1: 27.5, y0: -45, y1: 680, sx: 5, sy: 100, xm: [5, 10, 15, 20, 25], ym: [200, 400, 600], xname: 'v [m/s]', yname: 'E [kJ]' });
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; zeichnen(); });
    var t = 0, vorher = null, letzter = null, lauf = null, laeufe = [], ziel = null, pruefen = function(){};
    function werte(){ var m = B.wert('m'), v = B.wert('v'), F = B.wert('F'), E = 0.5 * m * v * v; return { m: m, v: v, F: F, E: E, s: E / F, a: F / m, te: v / (F / m) }; }
    var uhr = Uhr(function(tt){
      var w = werte(), k = Math.max(1, w.te / 4);                          // höchstens 4 s Animation
      t = Math.min(tt * k, w.te); zeichnen();
      if (t >= w.te){ letzter = w; lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Bremsen', function(){ vorher = letzter; if (WENIGER){ var w = werte(); t = w.te; letzter = w; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); t = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; lauf = null; laeufe = []; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), vn = Math.max(0, w.v - w.a * t), sn = w.v * t - 0.5 * w.a * t * t, En = 0.5 * w.m * vn * vn;
      B.anzeigen(); leeren(szene); K.leeren();
      el(szene, 'line', { x1: 8, y1: 86, x2: 292, y2: 86, 'class': 'boden' });
      for (var k = 0; k <= 160; k += 40) el(szene, 'text', { x: X0 + k * PX, y: 100, 'text-anchor': 'middle', 'class': 'skala' }, k + ' m');
      if (ziel) el(szene, 'line', { x1: X0 + ziel * PX, y1: 60, x2: X0 + ziel * PX, y2: 86, 'class': 'zielstrich' });
      var cx = X0 + sn * PX;
      if (sn > 0){ el(szene, 'line', { x1: X0, y1: 85, x2: cx, y2: 85, 'class': 'bremsspur' }); el(szene, 'text', { x: X0, y: 46, 'class': 'bt-wert' }, (t >= w.te ? 'Bremsweg: ' : 'Bremsweg bisher: ') + sig(sn) + NB + 'm'); }
      // Auto: Spitze an der gefahrenen Strecke
      el(szene, 'path', { d: 'M' + (cx - 30) + ',80 L' + (cx - 30) + ',68 L' + (cx - 22) + ',68 L' + (cx - 17) + ',60 L' + (cx - 6) + ',60 L' + (cx - 1) + ',68 L' + cx + ',70 L' + cx + ',80 Z', 'class': 'auto' });
      el(szene, 'circle', { cx: cx - 24, cy: 81, r: 4.5, 'class': 'rad' }); el(szene, 'circle', { cx: cx - 7, cy: 81, r: 4.5, 'class': 'rad' });
      if (t > 0 && vn > 0){ pfeil(szene, cx - 32, 70, cx - 32 - w.F * 0.004, 70, 'pf-w'); marke(szene, cx - 36 - w.F * 0.004, 67, 'F', 'B', 'pf-text pf-w', 'end'); }
      if (vn > 0){ pfeil(szene, cx + 4, 56, cx + 4 + vn * 1.6, 56, 'pf-v', 6); marke(szene, cx + 8 + vn * 1.6, 59, 'v', '', 'pf-text pf-v', 'start'); }
      // Diagramm: Parabel E_kin(v) in kJ, Punkt gleitet beim Bremsen hinunter
      if (vorher) K.kurve(function(u){ return 0.5 * vorher.m * u * u / 1000; }, 'vorher', 0, 26);
      K.kurve(function(u){ return 0.5 * w.m * u * u / 1000; }, 'kurve-ekin', 0, 26);
      // Punkt mit beiden Koordinaten. Die Parabel steigt nach rechts: Beschriftung rechts unter
      // dem Punkt, wenn darunter Platz ist; sonst darüber, so weit links wie möglich (bis an die
      // E-Achse) und gerade so hoch, dass sie die Kurve über ihrer ganzen Breite meidet.
      var lab = '(' + sig(vn) + NB + 'm/s; ' + sig(En / 1000, 4) + NB + 'kJ)', lw = lab.length * 6.4,
          px0 = K.X(vn), py0 = K.Y(En / 1000), ppu = K.X(1) - K.X(0), dx = 9, dy = 17;
      if (py0 + dy > K.Y(0) - 5 || px0 + 9 + lw > 300 || (py0 + dy > K.Y(0) - 22 && px0 + 9 + lw > 245)){   // nicht auf Achse oder Achsnamen
        dx = Math.max(K.X(0) + 6 - px0, -9 - lw);
        var hoch = 0; for (var xp = px0 + dx; xp <= px0 + dx + lw; xp += 3){ var u = vn + (xp - px0) / ppu; hoch = Math.max(hoch, py0 - K.Y(0.5 * w.m * u * u / 1000)); }
        dy = -9 - hoch;
      }
      K.punkt(vn, En / 1000, 'p-v', lab, dx, dy, 'start');
      var z = '<span>' + v_('E') + '<sub>kin</sub> = ½ · ' + v_('m') + ' · ' + v_('v') + '² = ½ · ' + zahl(w.m) + NB + 'kg · (' + zahl(w.v) + NB + 'm/s)² ' + ist(w.E, sig(w.E, 4)) + sig(w.E, 4) + NB + 'J</span>' +
              '<span>Bremsweg: ' + v_('F') + '<sub>B</sub> · ' + v_('s') + ' = ' + v_('E') + '<sub>kin</sub> → ' + v_('s') + ' = ' + v_('E') + '<sub>kin</sub> / ' + v_('F') + '<sub>B</sub> = ' + sig(w.E, 4) + NB + 'J / ' + zahl(w.F) + NB + 'N ' + ist(w.s, sig(w.s)) + sig(w.s) + NB + 'm</span>';
      if (vorher) z += '<span class="sim-notiz">Gestrichelt grau: die Parabel der vorigen Bremsung.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, m, v, F){ return s.lauf && s.lauf.m === m && s.lauf.v === v && s.lauf.F === F; }
    pruefen = Leiste(fig, [
      { text: 'Bremse dasselbe Auto mit derselben Bremskraft einmal aus \\(10\\;\\text{m/s}\\) und einmal aus \\(20\\;\\text{m/s}\\). Wie verändert sich der Bremsweg? Notiere deine Antwort.', ok: function(s){ return s.laeufe.some(function(a){ return a.v === 10 && s.laeufe.some(function(b){ return b.v === 20 && b.m === a.m && b.F === a.F; }); }); },
        vergleich: 'Er wird viermal so lang. Doppeltes Tempo heisst vierfache Bewegungsenergie, \\(E_\\text{kin} = \\tfrac12 \\cdot m \\cdot v^2\\), und die Bremse muss sie mit derselben Kraft abbauen: \\(F_B \\cdot s = E_\\text{kin}\\).' },
      { text: 'Ein Auto mit \\(1500\\;\\text{kg}\\) fährt \\(12\\;\\text{m/s}\\) und bremst mit \\(6000\\;\\text{N}\\). Stelle ein, brems und lies Energie und Bremsweg ab.', ok: function(s){ return hat(s, 1500, 12, 6000); } },
      { text: 'Ein Kleinwagen mit \\(800\\;\\text{kg}\\) bremst aus \\(15\\;\\text{m/s}\\) mit \\(6000\\;\\text{N}\\). Wie lang wird der Bremsweg bei doppelter Masse, sonst gleich? Stelle ein und brems.', ok: function(s){ return hat(s, 1600, 15, 6000); } },
      { text: 'Welche Bremskraft hält ein Auto mit \\(1200\\;\\text{kg}\\) aus \\(20\\;\\text{m/s}\\) auf \\(40\\;\\text{m}\\) an? Stelle ein und brems.', ok: function(s){ return hat(s, 1200, 20, 6000); } },
      { text: 'Ein Auto mit \\(2000\\;\\text{kg}\\) hat \\(400\\;\\text{kJ}\\) Bewegungsenergie. Wie schnell fährt es? Stelle ein und brems.', ok: function(s){ return s.lauf && s.lauf.m === 2000 && s.lauf.v === 20; } },
      { text: 'Bremse so, dass das Auto genau an der gestrichelten Linie steht. Warum gibt es mehrere Einstellungen, die das schaffen? Notiere deine Antwort.', setup: function(S){ ziel = 25; S.setze({ m: 1200, v: 8, F: 7000 }); }, ok: function(s){ return s.lauf && Math.abs(s.lauf.s - 25) < 1e-6; },
        vergleich: 'Der Bremsweg ist \\(s = \\dfrac{E_\\text{kin}}{F_B}\\). Jede Einstellung, bei der die Bewegungsenergie genau \\(25\\;\\text{m}\\) mal die Bremskraft ist, trifft die Linie: etwa \\(1000\\;\\text{kg}\\), \\(20\\;\\text{m/s}\\) und \\(8000\\;\\text{N}\\) (\\(200\\;\\text{kJ}\\)) oder \\(2000\\;\\text{kg}\\), \\(10\\;\\text{m/s}\\) und \\(4000\\;\\text{N}\\) (\\(100\\;\\text{kJ}\\)).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Energieerhaltung auf der Achterbahn ----------
     Nimmt Animation 3 der Themenseite (Pendel mit Energiebalken) als Achterbahn ohne Reibung:
     Der Wagen startet auf der Höhe h₀, fährt durchs Tal und über einen zweiten Hügel h₂.
     Lage- und Bewegungsenergie wechseln, ihre Summe bleibt (Säulen). Reicht die Energie
     nicht, kehrt der Wagen um. Massstab 4.6 px je m in beiden Richtungen. Startwert =
     Clipbeispiel: h₀ = 20 m, h₂ = 12 m, v₀ = 0, m = 300 kg. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), S = 4.6, XL = 10, YB = 162;
    var szene = g_(svg), unten = g_(svg);
    var B = Bedienung(fig, function(){ uhr.stop(); bahn = null; pos = 0; dir = 1; zeichnen(); });
    var pos = 0, dir = 1, bahn = null, vorher = null, letzter = null, lauf = null, laeufe = [], pruefen = function(){}, notiz = '';
    function werte(){ var h0 = B.wert('h0'), h2 = B.wert('h2'), v0 = B.wert('v0'), m = B.wert('m'); return { h0: h0, h2: h2, v0: v0, m: m, E: m * G * h0 + 0.5 * m * v0 * v0 }; }
    function profil(x, w){
      if (x <= 14) return w.h0 * (1 - Math.sin(Math.PI * x / 28));     // oben schon geneigt: Der Wagen rollt sofort an
      if (x <= 20) return 0;
      if (x <= 32) return w.h2 * (1 - Math.cos(Math.PI * (x - 20) / 12)) / 2;
      if (x <= 44) return w.h2 * (1 + Math.cos(Math.PI * (x - 32) / 12)) / 2;
      return 0;
    }
    function bauen(w){                                    // Bogenlänge entlang der Bahn
      var p = [], L = 0, xa = 0, ha = profil(0, w);
      for (var x = 0; x <= 60.0001; x += 0.05){ var h = profil(x, w); L += Math.hypot(x - xa, h - ha); p.push([x, h, L]); xa = x; ha = h; }
      return p;
    }
    function ort(b, s){ var i = 0, j = b.length - 1; while (j - i > 1){ var k = (i + j) >> 1; if (b[k][2] <= s) i = k; else j = k; } var a = b[i], c = b[j], f = (s - a[2]) / Math.max(1e-9, c[2] - a[2]); return [a[0] + (c[0] - a[0]) * f, a[1] + (c[1] - a[1]) * f]; }
    var letzt = 0, rek = null;
    var uhr = Uhr(function(tt){
      var w = werte(), dt = Math.min(0.05, tt - letzt); letzt = tt;
      if (!bahn) bahn = bauen(w);
      for (var n = 0; n < 5; n++){                       // kleine Schritte: Umkehrpunkt sauber treffen
        var h = ort(bahn, pos)[1], v2 = w.v0 * w.v0 + 2 * G * (w.h0 - h), v = wurzel(v2);
        var neu = pos + dir * Math.max(v, 0.3) * dt / 5, hn = ort(bahn, neu)[1];
        if (w.v0 * w.v0 + 2 * G * (w.h0 - hn) < 0){ dir = -dir; rek.umkehr = true; rek.hmax = h; }
        else pos = neu;
        var x = ort(bahn, pos)[0];
        if (Math.abs(x - 32) < 0.3 && dir > 0 && w.v0 * w.v0 + 2 * G * (w.h0 - w.h2) >= 0) rek.oben = true;
        if (dir < 0 && x < 14 && w.v0 * w.v0 + 2 * G * (w.h0 - ort(bahn, pos)[1]) < 0.05){ pos = Math.max(pos, 0.001); rek.ende = 'start'; letzter = rek; lauf = rek; laeufe.push(rek); zeichnen(); return false; }   // zurück auf der Starthöhe: Halt
      }
      zeichnen();
      var xe = ort(bahn, pos)[0];
      if (xe >= 59.9 || pos <= 0 || tt > 14){ rek.ende = xe >= 59.9 ? 'ziel' : 'start'; letzter = rek; lauf = rek; laeufe.push(rek); zeichnen(); return false; }
    });
    function start(){
      var w = werte(); vorher = letzter; bahn = bauen(w); pos = 0.001; dir = 1; letzt = 0;
      rek = { m: w.m, h0: w.h0, h2: w.h2, v0: w.v0, oben: false, umkehr: false, vTal: wurzel(w.v0 * w.v0 + 2 * G * w.h0), vTop: wurzel(w.v0 * w.v0 + 2 * G * (w.h0 - w.h2)) };
      if (WENIGER){ var reicht = w.v0 * w.v0 + 2 * G * (w.h0 - w.h2) > 0; rek.oben = reicht; rek.umkehr = !reicht; pos = reicht ? bahn[bahn.length - 1][2] : 0.001; rek.ende = reicht ? 'ziel' : 'start'; letzter = rek; lauf = rek; laeufe.push(rek); zeichnen(); }
      else uhr.start(0);
    }
    aktionen(fig, [['start', '▶ Loslassen', start], ['zurueck', '↺ Zurück', function(){ uhr.stop(); pos = 0; dir = 1; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); B.setze(o); bahn = null; pos = 0; zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      // Testhaken für Clipbilder (.claude/tools/aufnahme-anim.mjs): Wagen an die Stelle x [m] setzen
      zeige: function(xz){ uhr.stop(); var w = werte(); bahn = bauen(w); var i = 0; while (i < bahn.length - 2 && bahn[i + 1][0] <= xz) i++; var A = bahn[i], C = bahn[i + 1]; pos = A[2] + (C[2] - A[2]) * Math.max(0, Math.min(1, (xz - A[0]) / (C[0] - A[0]))); zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), b = bahn || bauen(w), p = ort(b, pos), h = p[1], v = wurzel(w.v0 * w.v0 + 2 * G * (w.h0 - h));
      B.anzeigen(); leeren(szene); leeren(unten);
      // Höhenlinien alle 10 m, Bahn, Wagen
      for (var k = 10; k <= 30; k += 10){ el(szene, 'line', { x1: XL, y1: YB - k * S, x2: XL + 60 * S, y2: YB - k * S, 'class': 'gitter' }); el(szene, 'text', { x: XL + 60 * S - 2, y: YB - k * S - 3, 'text-anchor': 'end', 'class': 'skala' }, k + ' m'); }
      el(szene, 'path', { d: b.filter(function(q, i){ return i % 4 === 0; }).map(function(q, i){ return (i ? 'L' : 'M') + (XL + q[0] * S).toFixed(1) + ',' + (YB - q[1] * S).toFixed(1); }).join(' '), 'class': 'schiene' });
      el(szene, 'line', { x1: XL, y1: YB, x2: XL + 60 * S, y2: YB, 'class': 'boden' });
      el(szene, 'text', { x: XL + 14, y: YB - w.h0 * S - 14, 'class': 'bt-klein' }, 'h₀ = ' + zahl(w.h0) + NB + 'm');
      el(szene, 'text', { x: XL + 32 * S + 16, y: YB - w.h2 * S - 2, 'text-anchor': 'start', 'class': 'bt-klein' }, 'h₂ = ' + zahl(w.h2) + NB + 'm');
      var wx = XL + p[0] * S, wy = YB - h * S;
      el(szene, 'circle', { cx: wx, cy: wy - 6, r: 6, 'class': 'kugel' });
      if (pos > 2 && v > 0.3) el(szene, 'text', { x: wx, y: wy - 16, 'text-anchor': 'middle', 'class': 'bt-wert' }, 'v = ' + sig(v) + NB + 'm/s');
      // Säulen: Lage, Bewegung, Summe — gleicher Massstab, die Summe bleibt
      var Ep = w.m * G * h, Ek = 0.5 * w.m * v * v, sk = 110 / Math.max(1, w.E);
      saeulen(unten, 50, 300, 46, 34, [{ name: 'Eₚₒₜ', wert: Ep, cls: 'e-pot' }, { name: 'Eₖᵢₙ', wert: Ek, cls: 'e-kin' }, { name: 'Summe', wert: Ep + Ek, cls: 'e-ges' }], sk, 1000);
      var z = '<span>Ohne Reibung bleibt die Summe: ' + v_('m') + ' · ' + v_('g') + ' · ' + v_('h') + '₀ + ½ · ' + v_('m') + ' · ' + v_('v') + '₀² = ' + v_('m') + ' · ' + v_('g') + ' · ' + v_('h') + ' + ½ · ' + v_('m') + ' · ' + v_('v') + '²</span>' +
              '<span>Im Tal: ' + v_('v') + ' = √(' + v_('v') + '₀² + 2 · ' + v_('g') + ' · ' + v_('h') + '₀) = √((' + zahl(w.v0) + NB + 'm/s)² + 2 · 9.81' + NB + 'm/s² · ' + zahl(w.h0) + NB + 'm) ' + ist(wurzel(w.v0 * w.v0 + 2 * G * w.h0), sig(wurzel(w.v0 * w.v0 + 2 * G * w.h0))) + sig(wurzel(w.v0 * w.v0 + 2 * G * w.h0)) + NB + 'm/s</span>';
      var v2t = w.v0 * w.v0 + 2 * G * (w.h0 - w.h2);
      z += v2t >= 0 ? '<span>Auf Hügel 2: ' + v_('v') + ' = √(' + v_('v') + '₀² + 2 · ' + v_('g') + ' · (' + v_('h') + '₀ − ' + v_('h') + '₂)) = √((' + zahl(w.v0) + NB + 'm/s)² + 2 · 9.81' + NB + 'm/s² · ' + ew(+(w.h0 - w.h2).toFixed(2), 'm') + ') ' + ist(wurzel(v2t), sig(wurzel(v2t))) + sig(wurzel(v2t)) + NB + 'm/s</span>'
                      : '<span>Hügel 2 ist zu hoch: Die Energie reicht nur bis ' + v_('h') + ' = ' + v_('h') + '₀ + ' + v_('v') + '₀² / (2 · ' + v_('g') + ') ' + ist(w.h0 + w.v0 * w.v0 / (2 * G), sig(w.h0 + w.v0 * w.v0 / (2 * G))) + sig(w.h0 + w.v0 * w.v0 / (2 * G)) + NB + 'm, dann kehrt der Wagen um.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Lass den Wagen mit zwei verschiedenen Massen fahren, sonst gleich. Ist er im Tal verschieden schnell? Notiere deine Antwort.', ok: function(s){ return s.laeufe.some(function(a){ return s.laeufe.some(function(b){ return b.m !== a.m && b.h0 === a.h0 && b.v0 === a.v0; }); }); },
        vergleich: 'Nein. In \\(m \\cdot g \\cdot h_0 = \\tfrac12 \\cdot m \\cdot v^2\\) steht die Masse auf beiden Seiten und kürzt sich: \\(v = \\sqrt{2 \\cdot g \\cdot h_0}\\). Der schwerere Wagen hat mehr Energie, braucht aber auch mehr für dasselbe Tempo.' },
      { text: 'Start aus der Ruhe auf \\(25\\;\\text{m}\\) Höhe: Wie schnell ist der Wagen im Tal? Stelle ein und lass los.', ok: function(s){ return s.lauf && s.lauf.h0 === 25 && s.lauf.v0 === 0; } },
      { text: 'Gleicher Start, der zweite Hügel ist \\(15\\;\\text{m}\\) hoch. Wie schnell ist der Wagen oben auf diesem Hügel?', ok: function(s){ return s.lauf && s.lauf.h0 === 25 && s.lauf.v0 === 0 && s.lauf.h2 === 15 && s.lauf.oben; } },
      { text: 'Hügel 2 ist \\(18\\;\\text{m}\\) hoch, der Start \\(15\\;\\text{m}\\). Mit welchem Anfangstempo schafft der Wagen den Hügel gerade noch? Stelle auf \\(0.1\\;\\text{m/s}\\) genau ein und lass los.', ok: function(s){ return s.lauf && s.lauf.h0 === 15 && s.lauf.h2 === 18 && s.lauf.oben && s.lauf.v0 <= 7.75; },
        vergleich: 'Gerechnet: \\(v_0 = \\sqrt{2 \\cdot g \\cdot (h_2 - h_0)} = \\sqrt{2 \\cdot 9.81\\;\\text{m/s}^2 \\cdot 3\\;\\text{m}} \\approx 7.67\\;\\text{m/s}\\). Auf dem Regler reicht \\(7.6\\;\\text{m/s}\\) knapp nicht, \\(7.7\\;\\text{m/s}\\) gerade.' },
      { text: 'Start aus der Ruhe auf \\(25\\;\\text{m}\\): Wie hoch darf Hügel 2 sein, damit der Wagen oben noch \\(10\\;\\text{m/s}\\) hat? Stelle ein und lass los.', ok: function(s){ return s.lauf && s.lauf.h0 === 25 && s.lauf.v0 === 0 && s.lauf.oben && Math.abs(s.lauf.vTop - 10) < 0.05; } },
      { text: 'Stelle eine Fahrt ein, bei der der Wagen an Hügel 2 umkehrt. Wie hoch kommt er? Notiere deine Antwort.', ok: function(s){ return s.lauf && s.lauf.umkehr; },
        vergleich: 'Ohne Reibung genau bis zur Höhe, bei der seine ganze Energie wieder Lageenergie ist: \\(h = h_0 + \\dfrac{v_0^2}{2 \\cdot g}\\), aus der Ruhe also genau auf die Starthöhe. Dann rollt er zurück.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Reibung und Motor ----------
     Nimmt Animation 6 der Themenseite (Energiefluss mit Verlusten) als Wagen auf einer Rampe
     von 40 m: zugeführt werden die abgegebene Lageenergie und die Motorarbeit F_M · s, daraus
     werden Bewegungsenergie, Wärme durch Reibung F_R · s und — bergauf — Lageenergie. Die
     beiden Säulen sind in jedem Moment gleich hoch: der Energieerhaltungssatz mit Motor und
     Reibung. Startwert = Clipbeispiel: 80 kg, 10 m hinunter, ohne Reibung und Motor. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), L = 40, S = 5.5;                 // Rampe 40 m, 5.5 px je m
    var szene = g_(svg), unten = g_(svg);
    var B = Bedienung(fig, function(){ uhr.stop(); x = 0; zeichnen(); });
    var x = 0, vorher = null, letzter = null, lauf = null, laeufe = [], pruefen = function(){};
    function werte(){
      var m = B.wert('m'), h = B.wert('h'), FR = B.wert('FR'), FM = B.wert('FM');
      var a = (m * G * h / L + FM - FR) / m, Ek = m * G * h + FM * L - FR * L;
      return { m: m, h: h, FR: FR, FM: FM, a: a, Ek: Ek, faehrt: a > 1e-9, zu: m * G * Math.max(h, 0) + FM * L, W: FR * L, te: a > 1e-9 ? Math.sqrt(2 * L / a) : 0 };
    }
    var uhr = Uhr(function(tt){
      var w = werte(), k = Math.max(1, w.te / 4); x = Math.min(L, 0.5 * w.a * Math.pow(tt * k, 2)); zeichnen();
      if (x >= L){ letzter = w; lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Losfahren', function(){ var w = werte(); vorher = letzter; x = 0; if (!w.faehrt){ lauf = null; zeichnen(); return; } if (WENIGER){ x = L; letzter = w; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); x = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); x = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), d = Math.sqrt(L * L - w.h * w.h), yA = 140 - Math.max(w.h, 0) * S, yB = 140 + Math.min(w.h, 0) * S;
      var Ax = 30, Bx = 30 + d * S, f = x / L, px = Ax + (Bx - Ax) * f, py = yA + (yB - yA) * f, ang = Math.atan2(yB - yA, Bx - Ax);
      B.anzeigen(); leeren(szene); leeren(unten);
      el(szene, 'polygon', { points: Ax + ',' + yA + ' ' + Bx + ',' + yB + ' ' + Math.max(Ax, Bx) + ',' + 146 + ' ' + Ax + ',146', 'class': 'rampe' });
      el(szene, 'line', { x1: Ax, y1: yA, x2: Bx, y2: yB, 'class': 'boden' });
      if (w.h !== 0){ var hx = w.h > 0 ? Ax - 8 : Bx + 8; el(szene, 'line', { x1: hx, y1: Math.min(yA, yB), x2: hx, y2: Math.max(yA, yB), 'class': 'masslinie' }); el(szene, 'text', { x: hx + (w.h > 0 ? -4 : 4), y: (yA + yB) / 2 + 4, 'text-anchor': w.h > 0 ? 'end' : 'start', 'class': 'bt-klein' }, Math.abs(w.h) + NB + 'm'); }
      el(szene, 'text', { x: (Ax + Bx) / 2, y: 160, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Weg auf der Rampe: 40' + NB + 'm');
      var gw = g_(szene, { transform: 'translate(' + px.toFixed(1) + ',' + py.toFixed(1) + ') rotate(' + (ang * 180 / Math.PI).toFixed(2) + ')' });
      el(gw, 'rect', { x: -14, y: -16, width: 28, height: 13, rx: 2, 'class': 'wagen' });
      el(gw, 'circle', { cx: -8, cy: -2.5, r: 3, 'class': 'rad' }); el(gw, 'circle', { cx: 8, cy: -2.5, r: 3, 'class': 'rad' });
      if (w.FM > 0){ pfeil(gw, 15, -10, 15 + w.FM * 0.1, -10, 'pf-f', 6); marke(gw, 19 + w.FM * 0.1, -13, 'F', 'M', 'pf-text pf-f', 'start'); }
      if (w.FR > 0 && w.faehrt){ pfeil(gw, -15, -10, -15 - w.FR * 0.1, -10, 'pf-w', 6); marke(gw, -19 - w.FR * 0.1, -13, 'F', 'R', 'pf-text pf-w', 'end'); }
      // Säulen bis zur aktuellen Stelle: links zugeführt, rechts wohin es gegangen ist
      var ep = w.m * G * w.h * f, mot = w.FM * L * f, wae = w.FR * L * f, ek = w.faehrt ? 0.5 * w.m * Math.pow(Math.sqrt(2 * w.a * x), 2) : 0;
      var links = [{ wert: Math.max(ep, 0), cls: 'e-pot', name: 'Lage' }, { wert: mot, cls: 'e-motor', name: 'Motor' }];
      var rechts = [{ wert: ek, cls: 'e-kin', name: 'Bewegung' }, { wert: wae, cls: 'e-waerme', name: 'Wärme' }, { wert: Math.max(-ep, 0), cls: 'e-pot', name: 'Lage' }];
      var gesamt = Math.max(1, w.m * G * Math.max(w.h, 0) + w.FM * L), sk = 108 / gesamt;
      [[links, 70, 'zugeführt'], [rechts, 180, 'danach']].forEach(function(sp){
        var y = 300;
        sp[0].forEach(function(t){ var hh = t.wert * sk; if (hh > 0.3){ el(unten, 'rect', { x: sp[1], y: y - hh, width: 50, height: hh, 'class': 'saeule ' + t.cls }); if (hh > 11) el(unten, 'text', { x: sp[1] + 25, y: y - hh / 2 + 4, 'text-anchor': 'middle', 'class': 'saeule-text' }, t.name); } y -= hh; });
        el(unten, 'line', { x1: sp[1] - 4, y1: 300, x2: sp[1] + 54, y2: 300, 'class': 'achse' });
        el(unten, 'text', { x: sp[1] + 25, y: 314, 'text-anchor': 'middle', 'class': 'bt-klein' }, sp[2]);
      });
      var z = '<span>Bilanz (Lage hinunter positiv): ' + v_('m') + ' · ' + v_('g') + ' · ' + v_('h') + ' + ' + v_('F') + '<sub>M</sub> · ' + v_('s') + ' = ' + v_('E') + '<sub>kin</sub> + ' + v_('F') + '<sub>R</sub> · ' + v_('s') + '</span>';
      if (!w.faehrt) z += '<span>Der Wagen fährt nicht los: ' + (w.h < 0 ? 'Der Motor überwindet ' + (w.FR > 0 ? 'Hangabtrieb und Reibung' : 'den Hangabtrieb') + ' nicht.' : w.h === 0 && w.FM === 0 ? 'Auf ebener Strecke ohne Motor wirkt keine antreibende Kraft.' : (w.FM > 0 ? 'Hangabtrieb und Motor' : 'Der Hangabtrieb') + ' ' + (w.FM > 0 ? 'überwinden' : 'überwindet') + ' die Reibung nicht.') + '</span>';
      else z += '<span>' + v_('E') + '<sub>kin</sub> = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² · ' + ew(w.h, 'm') + ' + ' + zahl(w.FM) + NB + 'N · 40' + NB + 'm − ' + zahl(w.FR) + NB + 'N · 40' + NB + 'm ' + ist(w.Ek, sig(w.Ek, 4)) + sig(w.Ek, 4) + NB + 'J</span>' +
                '<span>' + v_('v') + ' = √(2 · ' + v_('E') + '<sub>kin</sub> / ' + v_('m') + ') = √(2 · ' + sig(w.Ek, 4) + NB + 'J / ' + zahl(w.m) + NB + 'kg) ' + ist(wurzel(2 * w.Ek / w.m), sig(wurzel(2 * w.Ek / w.m))) + sig(wurzel(2 * w.Ek / w.m)) + NB + 'm/s</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, m, h, FR, FM){ return s.lauf && s.lauf.m === m && s.lauf.h === h && s.lauf.FR === FR && s.lauf.FM === FM; }
    pruefen = Leiste(fig, [
      { text: 'Fahr zuerst ohne Reibung und ohne Motor hinunter, dann mit Reibung. Wohin geht die Energie, die unten als Bewegungsenergie fehlt? Notiere deine Antwort.', ok: function(s){ return s.laeufe.some(function(a){ return a.FR === 0 && a.FM === 0 && a.h > 0; }) && s.laeufe.some(function(a){ return a.FR > 0 && a.FM === 0 && a.h > 0; }); },
        vergleich: 'In Wärme: Die Reibung verrichtet die Arbeit \\(F_R \\cdot s\\), Räder, Lager und Boden werden etwas wärmer. Die Summe bleibt — die rechte Säule ist gleich hoch wie die linke, nur ein Teil ist jetzt Wärme statt Bewegungsenergie.' },
      { text: 'Wagen \\(60\\;\\text{kg}\\), \\(15\\;\\text{m}\\) hinunter, ohne Reibung und Motor: Wie schnell ist er unten?', ok: function(s){ return hat(s, 60, 15, 0, 0); } },
      { text: 'Dieselbe Fahrt mit \\(80\\;\\text{N}\\) Reibung: Wie viel Energie wird zu Wärme, und wie schnell ist der Wagen unten?', ok: function(s){ return hat(s, 60, 15, 80, 0); } },
      { text: 'Bergauf: Das Ende liegt \\(5\\;\\text{m}\\) höher (\\(h = -5\\;\\text{m}\\)), Reibung \\(50\\;\\text{N}\\), Wagen \\(80\\;\\text{kg}\\). Mit welcher Motorkraft kommt er gerade noch oben an? Stelle ein und fahr.', ok: function(s){ return hat(s, 80, -5, 50, 150); } },
      { text: 'Stelle eine Fahrt ein, bei der genau ein Viertel der zugeführten Energie zu Wärme wird. Wohin gehen die übrigen drei Viertel? Notiere deine Antwort.', ok: function(s){ return s.lauf && s.lauf.zu > 0 && Math.abs(s.lauf.W / s.lauf.zu - 0.25) < 0.01; },
        vergleich: 'In die Bewegungsenergie am Ende — fährt der Wagen bergauf, zum Teil auch in Lageenergie. Zugeführt werden die Lageenergie beim Hinunterfahren und die Motorarbeit \\(F_M \\cdot s\\); ein Viertel davon macht die Reibung \\(F_R \\cdot s\\) zu Wärme. Die beiden Säulen bleiben gleich hoch.' },
      { text: 'Fahr mit Motor \\(10\\;\\text{m}\\) bergauf (\\(h = -10\\;\\text{m}\\)), ohne Reibung. Wohin ist die Motorarbeit gegangen? Notiere deine Antwort.', ok: function(s){ return s.lauf && s.lauf.h === -10 && s.lauf.FR === 0 && s.lauf.FM > 0; },
        vergleich: 'Zum grössten Teil in Lageenergie \\(m \\cdot g \\cdot h\\), der Rest in Bewegungsenergie: \\(F_M \\cdot s = m \\cdot g \\cdot h + E_\\text{kin}\\). Mit Reibung käme noch Wärme dazu.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Leistung und Wirkungsgrad ----------
     Nimmt Animation 5 der Themenseite (Hubleistung beim Heben) als Kran: Die Last steigt in
     der Hubzeit t gleichmässig auf die Höhe h. Die Säulen wachsen mit: zugeführt (Blau) teilt
     sich in Nutzen (Lageenergie, Bernstein) und Verlust (Wärme, Rot) — Verhältnis η.
     Startwert = Clipbeispiel: 200 kg, 10 m, 20 s, η = 0.8: P = 981 W, P_zu ≈ 1226 W. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg'), S = 11, YB = 280;               // 11 px je m
    var szene = g_(svg);
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; zeichnen(); });
    var t = 0, vorher = null, letzter = null, lauf = null, laeufe = [], ziel = null, pruefen = function(){};
    function werte(){ var m = B.wert('m'), h = B.wert('h'), T = B.wert('t'), e = B.wert('eta'), W = m * G * h; return { m: m, h: h, t: T, eta: e, W: W, Pn: W / T, Pz: W / (e * T), Ez: W / e }; }
    var uhr = Uhr(function(tt){
      var w = werte(), k = Math.max(1, w.t / 5); t = Math.min(w.t, tt * k); zeichnen();
      if (t >= w.t){ letzter = w; lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Heben', function(){ vorher = letzter; if (WENIGER){ var w = werte(); t = w.t; letzter = w; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); t = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; lauf = null; laeufe = []; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var w = werte(), hn = w.h * t / w.t, f = t / w.t;
      B.anzeigen(); leeren(szene);
      el(szene, 'line', { x1: 8, y1: YB, x2: 200, y2: YB, 'class': 'boden' });
      el(szene, 'rect', { x: 46, y: 36, width: 10, height: YB - 36, 'class': 'mast' });
      el(szene, 'rect', { x: 40, y: 30, width: 150, height: 8, 'class': 'mast' });
      for (var k = 0; k <= 20; k += 5){ el(szene, 'line', { x1: 36, y1: YB - k * S, x2: 46, y2: YB - k * S, 'class': 'achse' }); el(szene, 'text', { x: 32, y: YB - k * S + (k ? 4 : -3), 'text-anchor': 'end', 'class': 'skala' }, k + ' m'); }
      el(szene, 'rect', { x: 58, y: YB - 26, width: 34, height: 22, rx: 3, 'class': 'motor' });
      el(szene, 'text', { x: 75, y: YB - 11, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Motor');
      var ly = YB - hn * S - 24;
      el(szene, 'line', { x1: 170, y1: 38, x2: 170, y2: ly, 'class': 'seil' });
      el(szene, 'rect', { x: 154, y: ly, width: 32, height: 24, rx: 2, 'class': 'kiste' });
      el(szene, 'text', { x: 170, y: ly + 16, 'text-anchor': 'middle', 'class': 'bt-klein' }, zahl(w.m) + NB + 'kg');
      el(szene, 'line', { x1: 190, y1: YB - w.h * S, x2: 200, y2: YB - w.h * S, 'class': 'zielstrich' }); el(szene, 'text', { x: 195, y: YB - w.h * S - 4, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'h');
      el(szene, 'text', { x: 100, y: 58, 'class': 'bt-wert' }, 't = ' + fest(t, 1) + NB + 's');
      // Energiefluss: zugeführt teilt sich in Nutzen und Verlust (Säulen wachsen mit der Zeit)
      var sk = 150 / Math.max(1, w.Ez);
      var cols = [['zu', w.Ez * f, 'e-motor'], ['nutz', w.W * f, 'e-pot'], ['verl', (w.Ez - w.W) * f, 'e-waerme']];
      cols.forEach(function(c, i){ var xx = 212 + i * 29, hh = c[1] * sk; el(szene, 'rect', { x: xx, y: YB - hh, width: 22, height: hh, 'class': 'saeule ' + c[2] }); el(szene, 'text', { x: xx + 11, y: YB + 12, 'text-anchor': 'middle', 'class': 'bt-klein' }, c[0]); });
      el(szene, 'line', { x1: 208, y1: YB, x2: 296, y2: YB, 'class': 'achse' });
      var z = '<span>' + v_('P') + '<sub>nutz</sub> = ' + v_('m') + ' · ' + v_('g') + ' · ' + v_('h') + ' / ' + v_('t') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² · ' + zahl(w.h) + NB + 'm / ' + zahl(w.t) + NB + 's ' + ist(w.Pn, sig(w.Pn, 4)) + sig(w.Pn, 4) + NB + 'W</span>' +
              '<span>' + v_('P') + '<sub>zu</sub> = ' + v_('P') + '<sub>nutz</sub> / ' + v_('η') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² · ' + zahl(w.h) + NB + 'm / (' + zahl(w.eta) + ' · ' + zahl(w.t) + NB + 's) ' + ist(w.Pz, sig(w.Pz, 4)) + sig(w.Pz, 4) + NB + 'W</span>';
      if (vorher) z += '<span class="sim-notiz">Voriger Hub: ' + v_('P') + '<sub>nutz</sub> ≈ ' + sig(vorher.Pn, 4) + NB + 'W.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, m, h, T, e){ return s.lauf && s.lauf.m === m && s.lauf.h === h && s.lauf.t === T && (e == null || gl(s.lauf.eta, e)); }
    pruefen = Leiste(fig, [
      { text: 'Heb dieselbe Last gleich hoch, einmal in der doppelten Zeit. Was ändert sich: die Arbeit oder die Leistung? Notiere deine Antwort.', ok: function(s){ return s.laeufe.some(function(a){ return s.laeufe.some(function(b){ return b.m === a.m && b.h === a.h && b.t === 2 * a.t; }); }); },
        vergleich: 'Die Arbeit \\(m \\cdot g \\cdot h\\) bleibt gleich, die Leistung halbiert sich: \\(P = \\dfrac{W}{t}\\). Leistung sagt, wie schnell Energie umgesetzt wird.' },
      { text: 'Der Kran hebt \\(300\\;\\text{kg}\\) in \\(30\\;\\text{s}\\) auf \\(15\\;\\text{m}\\). Wie gross ist die Nutzleistung?', ok: function(s){ return hat(s, 300, 15, 30); } },
      { text: 'Dieselbe Last in der halben Zeit: Wie gross ist die Nutzleistung jetzt?', ok: function(s){ return hat(s, 300, 15, 15); } },
      { text: 'Wieder \\(300\\;\\text{kg}\\), \\(15\\;\\text{m}\\), \\(30\\;\\text{s}\\), aber der Antrieb hat den Wirkungsgrad \\(0.75\\). Welche Leistung muss zugeführt werden?', ok: function(s){ return hat(s, 300, 15, 30, 0.75); } },
      { text: 'Der Motor nimmt höchstens \\(1500\\;\\text{W}\\) auf, \\(\\eta = 0.75\\). Last \\(300\\;\\text{kg}\\), Höhe \\(12\\;\\text{m}\\): Stelle die kürzeste mögliche Hubzeit in ganzen Sekunden ein und heb.', ok: function(s){ return hat(s, 300, 12, 32, 0.75); } },
      { text: 'Stelle einen Hub ein, für den genau \\(2\\;\\text{kW}\\) zugeführt werden müssen, und heb. Wie viel davon hebt die Last, und wohin geht der Rest? Notiere deine Antwort.', ok: function(s){ return s.lauf && Math.abs(s.lauf.Pz - 2000) < 10; },
        vergleich: 'Die Nutzleistung ist \\(P_\\text{nutz} = \\eta \\cdot 2\\;\\text{kW}\\), bei \\(\\eta = 0.75\\) also \\(1500\\;\\text{W}\\). Der Rest, \\((1 - \\eta) \\cdot 2\\;\\text{kW}\\), wird im Antrieb zu Wärme.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 6: Energiebilanz der Erde ----------
     Nimmt den Abschnitt «Energiebilanz der Erde» der Themenseite als laufende Bilanz:
     aufgenommen (1 − a) · S/4, abgestrahlt ins Weltall f · σ · T⁴, wobei f der Anteil der
     Wärmestrahlung der Oberfläche ist, der ins All gelangt (mehr Treibhausgas, kleineres f).
     Ist die Bilanz nicht ausgeglichen, ändert sich die Temperatur: C · dT/dt = Ein − Aus mit
     C = 4.2 · 10⁸ J/(m²·K) (rund 100 m Ozean). 30 Jahre laufen in 6 s. Startwert:
     a = 0.30, f = 0.61, T = 288 K (Themenseite: 238 W/m² hinein und hinaus). */
  (function(){
    var fig = document.getElementById('sim6'); if (!fig) return;
    var svg = fig.querySelector('svg'), SOL = 1361, SIG = 5.67e-8, C = 4.2e8, JAHR = 3.156e7;
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,176)' });
    var K = Achsen(dia, { w: 300, h: 140, x0: -2.5, x1: 31, y0: 240, y1: 314, sx: 5, sy: 10, xm: [5, 10, 15, 20, 25, 30], ym: [250, 260, 270, 280, 290, 300, 310], xname: 't [Jahre]', yname: 'T [K]' });
    var B = Bedienung(fig, function(){ uhr.stop(); spur = [[0, T]]; zeichnen(); });
    var T0 = Math.pow(0.7 * SOL / 4 / (0.61 * SIG), 0.25), T = T0, spur = [[0, T0]],   // Start im Gleichgewicht von heute (a = 0.30, f = 0.61)
         lauf = null, laeufe = [], pruefen = function(){}, letzt = 0;
    function werte(){ var a = B.wert('al'), f = B.wert('f'), ein = (1 - a) * SOL / 4; return { a: a, f: f, ein: ein, aus: f * SIG * Math.pow(T, 4), Teq: Math.pow(ein / (f * SIG), 0.25) }; }
    function schritt(jahre){ var w = werte(), n = Math.ceil(jahre / 0.05), dt = jahre / n * JAHR; for (var i = 0; i < n; i++){ T += ((1 - w.a) * SOL / 4 - w.f * SIG * Math.pow(T, 4)) / C * dt; } }
    var uhr = Uhr(function(tt){
      var j = Math.min(30, tt * 5), w;
      schritt(j - letzt); letzt = j; spur.push([j, T]); zeichnen();
      if (j >= 30){ w = werte(); lauf = { a: w.a, f: w.f, T: T, Teq: w.Teq }; laeufe.push(lauf); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ 30 Jahre laufen lassen', function(){ spur = [[0, T]]; letzt = 0; if (WENIGER){ for (var j = 1; j <= 30; j++){ schritt(1); spur.push([j, T]); } var w = werte(); lauf = { a: w.a, f: w.f, T: T, Teq: w.Teq }; laeufe.push(lauf); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ auf heute', function(){ uhr.stop(); T = T0; spur = [[0, T]]; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.T = T; w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); B.setze(o); spur = [[0, T]]; zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); }
    };
    function band(x1, y1, x2, y2, breite, cls){ el(szene, 'line', { x1: x1, y1: y1, x2: x2, y2: y2, 'class': 'strahl ' + cls, 'stroke-width': breite.toFixed(1) }); var dx = x2 - x1, dy = y2 - y1, l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l, s = breite / 2 + 6; el(szene, 'polygon', { points: (x2 + ux * 9) + ',' + (y2 + uy * 9) + ' ' + (x2 - uy * s) + ',' + (y2 + ux * s) + ' ' + (x2 + uy * s) + ',' + (y2 - ux * s), 'class': 'strahl-kopf ' + cls }); }
    function zeichnen(){
      var w = werte(), aus = w.f * SIG * Math.pow(T, 4), k = 0.07;               // 0.07 px Breite je W/m²
      B.anzeigen(); leeren(szene); K.leeren();
      el(szene, 'circle', { cx: -14, cy: 82, r: 40, 'class': 'sonne' });
      el(szene, 'circle', { cx: 170, cy: 82, r: 56, 'class': 'atmosphaere', 'fill-opacity': (0.08 + 0.9 * (1 - w.f)).toFixed(2) });
      el(szene, 'circle', { cx: 170, cy: 82, r: 40, 'class': 'erde' });
      band(30, 70, 124, 70, SOL / 4 * k, 'ein');
      el(szene, 'text', { x: 34, y: 56, 'class': 'bt-klein' }, 'Sonne: ' + sig(SOL / 4) + NB + 'W/m²');
      band(124, 92, 34, 112, w.a * SOL / 4 * k, 'zurueck');
      el(szene, 'text', { x: 34, y: 130, 'class': 'bt-klein' }, 'zurückgeworfen: ' + sig(w.a * SOL / 4) + NB + 'W/m²');
      band(214, 64, 284, 22, aus * k, 'aus');
      el(szene, 'text', { x: 262, y: 14, 'text-anchor': 'end', 'class': 'bt-klein' }, 'ins All: ' + sig(aus) + NB + 'W/m²');
      el(szene, 'text', { x: 170, y: 86, 'text-anchor': 'middle', 'class': 'erde-text' }, fest(T, 1) + NB + 'K');
      el(szene, 'text', { x: 170, y: 152, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Treibhausgase (Hülle): Anteil ins All f = ' + zahl(w.f));
      K.kurve(function(){ return w.Teq; }, 'gleichgewicht', 0, 30);
      K.text(30, w.Teq + (w.Teq > 306 ? -5 : 2), 'Gleichgewicht ' + fest(w.Teq, 1) + NB + 'K', 'gleichgewicht-text', 'end');
      if (spur.length > 1) el(K.ebene, 'polyline', { points: spur.map(function(p){ return K.X(p[0]).toFixed(1) + ',' + K.Y(p[1]).toFixed(1); }).join(' '), 'class': 'kurve-t', 'clip-path': K.clip });
      var diff = w.ein - aus;
      rolle(fig, 'formel').innerHTML =
        '<span>Aufgenommen: (1 − ' + v_('a') + ') · ' + v_('S') + ' / 4 = (1 − ' + zahl(w.a) + ') · 1361' + NB + 'W/m² / 4 ' + ist(w.ein, sig(w.ein)) + sig(w.ein) + NB + 'W/m²</span>' +
        '<span>Ins All: ' + v_('f') + ' · ' + v_('σ') + ' · ' + v_('T') + '⁴ = ' + zahl(w.f) + ' · 5.67·10⁻⁸' + NB + 'W/(m²·K⁴) · (' + fest(T, 1) + NB + 'K)⁴ ≈ ' + sig(aus) + NB + 'W/m²</span>' +
        '<span>' + (Math.abs(diff) < 0.05 ? 'Bilanz ausgeglichen: Die Temperatur bleibt.' : (diff > 0 ? 'Es kommt ' + sig(diff) + NB + 'W/m² mehr herein als hinaus: Die Erde erwärmt sich.' : 'Es geht ' + sig(-diff) + NB + 'W/m² mehr hinaus als herein: Die Erde kühlt ab.')) + '</span>';
      pruefen();
    }
    function fertig(s, a, f){ return s.lauf && gl(s.lauf.a, a) && gl(s.lauf.f, f) && Math.abs(s.lauf.T - s.lauf.Teq) < 0.5; }
    pruefen = Leiste(fig, [
      { text: 'Ohne Treibhausgase gelangt alle Wärmestrahlung ins All (\\(f = 1\\)); dazu weniger Wolken, Albedo \\(0.25\\). Stelle ein und lass laufen. Welche Temperatur stellt sich ein?', ok: function(s){ return fertig(s, 0.25, 1); } },
      { text: 'Stelle den heutigen Zustand ein (\\(a = 0.30\\), \\(f = 0.61\\)) und lass laufen. Bleibt die Temperatur gleich, obwohl die Erde ständig abstrahlt? Notiere deine Antwort.', ok: function(s){ return fertig(s, 0.3, 0.61); },
        vergleich: 'Rund \\(238\\;\\text{W/m}^2\\) hinein und \\(238\\;\\text{W/m}^2\\) hinaus. Die Erde strahlt dauernd ab, aber genauso viel Sonnenstrahlung fliesst nach. Kühlt sie ab, strahlt sie nach \\(\\sigma \\cdot T^4\\) sofort weniger ab — die Bilanz stellt sich von selbst wieder ein.' },
      { text: 'Mehr Treibhausgas: \\(f\\) sinkt von \\(0.61\\) auf \\(0.60\\). Lass vom heutigen Zustand aus laufen. Um wie viel steigt die Temperatur, und warum hört sie wieder auf zu steigen? Notiere deine Antwort.', ok: function(s){ return fertig(s, 0.3, 0.6); },
        vergleich: 'Um rund \\(1.2\\;\\text{K}\\) auf etwa \\(289\\;\\text{K}\\). Zuerst geht weniger hinaus als herein, die Erde erwärmt sich. Mit der Temperatur steigt die Abstrahlung, bis sie wieder gleich der Aufnahme ist — der Energieerhaltungssatz gilt, nur bei höherer Temperatur.' },
      { text: 'Meereis schmilzt, die Albedo sinkt auf \\(0.28\\) (\\(f = 0.61\\)). Lass laufen: Was geschieht? Notiere deine Antwort.', ok: function(s){ return fertig(s, 0.28, 0.61); },
        vergleich: 'Die Erde nimmt mehr auf, \\((1 - a) \\cdot S/4\\) wird grösser, und sie erwärmt sich auf rund \\(290\\;\\text{K}\\). In Wirklichkeit schmilzt dadurch noch mehr Eis — eine Rückkopplung, die die Erwärmung verstärkt.' },
      { text: 'Bei \\(f = 0.58\\): Welche Albedo bräuchte es, damit die Erde wieder rund \\(288\\;\\text{K}\\) hat? Stelle ein und lass laufen.', ok: function(s){ return s.lauf && gl(s.lauf.f, 0.58) && Math.abs(s.lauf.T - s.lauf.Teq) < 0.5 && Math.abs(s.lauf.Teq - 288) < 1; } }
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

    var SIG = 5.67e-8;
    function grad(a){ return a * Math.PI / 180; }

    var TYPEN = {
      /* ----- Kapitel 1: Energie und Arbeit ----- */
      'arbeit': { felder: ['W'], muster: '<i>W</i> = {W} J',
        neu: function(){
          var F, s, a;
          do { F = zufall([40, 60, 80, 120, 150, 250, 400]); s = zufall([3, 4, 5, 8, 12, 20, 50]); a = zufall([0, 20, 30, 45, 60]); }
          while ((F === 250 && s === 6) || (F === 80 && s === 50 && a === 30) || F === s);   // Simulation 1, Aufgabe 1b
          return { W: F * s * Math.cos(grad(a)), F: F, s: s, a: a,
            text: 'Eine Kraft von \\(' + ein(F, 'N') + '\\) zieht einen Körper \\(' + ein(s, 'm') + '\\) weit' + (a ? '; sie wirkt unter \\(' + a + '^\\circ\\) zur Bewegungsrichtung' : ', genau in Bewegungsrichtung') + '. Wie gross ist die Arbeit?' }; },
        pruefen: function(A, e){
          if (nah(e.W, A.W)) return null;
          if (A.a && nah(e.W, A.F * A.s)) return 'Nur der Anteil der Kraft in Wegrichtung zählt: \\(W = F \\cdot s \\cdot \\cos\\alpha\\).';
          if (A.a && A.a !== 45 && nah(e.W, A.F * A.s * Math.sin(grad(A.a)))) return 'Der Anteil in Wegrichtung ist \\(F \\cdot \\cos\\alpha\\), nicht \\(F \\cdot \\sin\\alpha\\): \\(\\alpha\\) ist der Winkel zum Weg.';
          if (nah(e.W, A.F / A.s) || nah(e.W, A.s / A.F)) return 'Arbeit ist Kraft <em>mal</em> Weg.';
          return '\\(W = F \\cdot s \\cdot \\cos\\alpha\\), Winkel in Grad.'; },
        fehler: function(A){ var l = [[{ W: String(A.F / A.s) }, 'mal']]; if (A.a) l.push([{ W: String(A.F * A.s) }, 'Anteil']); if (A.a && A.a !== 45) l.push([{ W: String(A.F * A.s * Math.sin(grad(A.a))) }, 'sin']); return l; },
        loesung: function(A){ return 'W = F \\cdot s \\cdot \\cos\\alpha = ' + ein(A.F, 'N') + ' \\cdot ' + ein(A.s, 'm') + ' \\cdot \\cos ' + A.a + '^\\circ ' + erg(A.W, 'J'); } },
      'hub': { felder: ['x'], muster: function(A){ return A.art === 'W' ? '<i>W</i> = {x} J' : '<i>h</i> = {x} m'; },
        neu: function(){
          var m, h;
          do { m = zufall([2, 5, 12, 25, 60, 75]); h = zufall([1.5, 3, 4, 8, 12, 25]); } while (m === h);
          if (Math.random() < 0.6) return { art: 'W', x: m * G * h, m: m, h: h, text: 'Ein Körper mit \\(m = ' + ein(m, 'kg') + '\\) wird \\(' + ein(h, 'm') + '\\) hoch gehoben. Wie gross ist die Hubarbeit?' };
          return { art: 'h', x: h, m: m, W: m * G * h, text: 'Für das Heben eines Körpers mit \\(m = ' + ein(m, 'kg') + '\\) werden \\(' + ein(+(m * G * h).toPrecision(4), 'J') + '\\) Hubarbeit verrichtet. Wie hoch wurde er gehoben?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'W'){
            if (nah(e.x, A.m * A.h)) return 'Die Kraft zum Heben ist die Gewichtskraft \\(m \\cdot g\\): \\(W = m \\cdot g \\cdot h\\).';
            if (nah(e.x, A.m * G)) return 'Das ist nur die Gewichtskraft. Arbeit ist Kraft mal Weg: \\(W = m \\cdot g \\cdot h\\).';
            return '\\(W = m \\cdot g \\cdot h\\).';
          }
          if (nah(e.x, A.W / A.m)) return 'Durch die Gewichtskraft teilen, nicht nur durch die Masse: \\(h = \\dfrac{W}{m \\cdot g}\\).';
          return '\\(h = \\dfrac{W}{m \\cdot g}\\).'; },
        fehler: function(A){ return A.art === 'W' ? [[{ x: String(A.m * A.h) }, 'Gewichtskraft'], [{ x: String(A.m * G) }, 'nur']] : [[{ x: String(A.W / A.m) }, 'Gewichtskraft']]; },
        loesung: function(A){ return A.art === 'W' ? 'W = m \\cdot g \\cdot h = ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + ' ' + erg(A.x, 'J')
                                                   : 'h = \\dfrac{W}{m \\cdot g} = \\dfrac{' + ein(+A.W.toPrecision(4), 'J') + '}{' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2} ' + erg(A.x, 'm'); } },
      'kwh': { felder: ['x'], muster: function(A){ return A.art === 'MJ' ? '<i>E</i> = {x} MJ' : '<i>E</i> = {x} kWh'; },
        neu: function(){
          if (Math.random() < 0.5){ var k = zufall([0.5, 2, 3.5, 12, 40, 75]); return { art: 'MJ', x: k * 3.6, k: k, text: 'Ein Gerät setzt \\(' + ein(k, 'kWh') + '\\) Energie um. Wie viele Megajoule sind das?' }; }
          var P, t; do { P = zufall([60, 800, 1500, 2000, 9]); t = zufall([0.5, 2, 3, 8, 24]); } while (P * t === 1000 || P === t);
          return { art: 'kWh', x: P * t / 1000, P: P, t: t, text: 'Ein Gerät mit \\(' + ein(P, 'W') + '\\) läuft \\(' + ein(t, 'h') + '\\). Wie viel Energie setzt es um, in Kilowattstunden?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'MJ'){
            if (nah(e.x, A.k / 3.6)) return 'Umgekehrt: \\(1\\;\\text{kWh} = 1000\\;\\text{W} \\cdot 3600\\;\\text{s} = 3.6\\;\\text{MJ}\\) — mal \\(3.6\\).';
            if (nah(e.x, A.k * 3600) || nah(e.x, A.k * 3.6e6) || nah(e.x, A.k * 3600 * 1000)) return 'Gefragt sind Megajoule: \\(1\\;\\text{kWh} = 3.6\\;\\text{MJ}\\).';
            return '\\(1\\;\\text{kWh} = 3.6\\;\\text{MJ}\\).';
          }
          if (nah(e.x, A.P * A.t)) return 'Das sind Wattstunden. In Kilowattstunden: durch \\(1000\\).';
          if (nah(e.x, A.P * A.t * 3600)) return 'Das sind Joule. Gefragt sind Kilowattstunden: \\(E = P \\cdot t\\) mit \\(P\\) in kW und \\(t\\) in h.';
          return '\\(E = P \\cdot t\\) mit \\(P\\) in kW und \\(t\\) in h.'; },
        fehler: function(A){ return A.art === 'MJ' ? [[{ x: String(A.k / 3.6) }, 'Umgekehrt'], [{ x: String(A.k * 3600) }, 'Megajoule']] : [[{ x: String(A.P * A.t) }, 'Wattstunden'], [{ x: String(A.P * A.t * 3600) }, 'Joule']]; },
        loesung: function(A){ return A.art === 'MJ' ? 'E = ' + ein(A.k, 'kWh') + ' = ' + tz(A.k) + ' \\cdot 3.6\\;\\text{MJ} ' + erg(A.x, 'MJ')
                                                    : 'E = P \\cdot t = ' + ein(A.P / 1000, 'kW') + ' \\cdot ' + ein(A.t, 'h') + ' ' + erg(A.x, 'kWh'); } },

      /* ----- Kapitel 2: Bewegungs- und Lageenergie ----- */
      'ekin': { felder: ['E'], muster: '<i>E</i><sub>kin</sub> = {E} J',
        neu: function(){
          var O, v, kmh = Math.random() < 0.35;
          do { O = zufall([['Ein Tennisball', 0.06], ['Ein Fussball', 0.4], ['Eine Läuferin', 60], ['Ein Velo mit Fahrer', 90], ['Ein Auto', 1200], ['Ein Auto', 1500]]);
               v = kmh ? zufall([36, 54, 72, 90, 108]) / 3.6 : zufall([3, 4, 5, 8, 12, 25, 40]); }
          while ((O[1] < 1 && (v < 8)) || (O[1] > 1000 && v < 8) || (O[1] === 60 && v > 9) || (O[1] === 90 && v > 15) || (O[1] === 1500 && (Math.abs(v - 20) < 1e-9 || Math.abs(v - 10) < 1e-9)) || (O[1] === 90 && v === 5) || (O[1] === 0.4 && (Math.abs(v - 10) < 1e-9 || Math.abs(v - 15) < 1e-9)));   // plausibel; Aufgabe 2a, Kontrollfrage, Festhalten
          return { E: 0.5 * O[1] * v * v, m: O[1], v: v, kmh: kmh, vk: v * 3.6,
            text: O[0] + ' (\\(m = ' + ein(O[1], 'kg') + '\\)) bewegt sich mit \\(' + (kmh ? ein(+(v * 3.6).toFixed(6), 'km/h') : ein(v, 'm/s')) + '\\). Wie gross ist die Bewegungsenergie?' }; },
        pruefen: function(A, e){
          if (nah(e.E, A.E)) return null;
          if (A.kmh && nah(e.E, 0.5 * A.m * A.vk * A.vk)) return 'Erst in m/s umrechnen: ' + umr(A.vk) + '.';
          if (nah(e.E, A.m * A.v * A.v)) return 'Der Faktor \\(\\tfrac12\\) fehlt: \\(E_\\text{kin} = \\tfrac12 \\cdot m \\cdot v^2\\).';
          if (nah(e.E, 0.5 * A.m * A.v)) return 'Die Geschwindigkeit steht im Quadrat.';
          return '\\(E_\\text{kin} = \\tfrac12 \\cdot m \\cdot v^2\\) mit \\(v\\) in m/s.'; },
        fehler: function(A){ var l = [[{ E: String(A.m * A.v * A.v) }, 'Faktor'], [{ E: String(0.5 * A.m * A.v) }, 'Quadrat']]; if (A.kmh) l.push([{ E: String(0.5 * A.m * A.vk * A.vk) }, 'umrechnen']); return l; },
        loesung: function(A){ return (A.kmh ? 'v = \\dfrac{' + tz(+A.vk.toFixed(6)) + '}{3.6}\\;\\text{m/s} ' + erg(A.v, 'm/s') + ',\\quad ' : '') + 'E_\\text{kin} = \\tfrac12 \\cdot m \\cdot v^2 = \\tfrac12 \\cdot ' + ein(A.m, 'kg') + ' \\cdot (' + ein(+A.v.toPrecision(4), 'm/s') + ')^2 ' + erg(A.E, 'J'); } },
      'vaus': { felder: ['v'], muster: '<i>v</i> = {v} m/s',
        neu: function(){
          var m, v;
          do { m = zufall([2, 50, 80, 1200]); v = zufall([4, 6, 12, 15, 25]); } while ((m === 2 && v > 15) || (m === 80 && v > 12) || (m === 50 && v > 12) || (m === 1200 && v < 12) || false);   // plausibel
          return { v: v, m: m, E: 0.5 * m * v * v, text: 'Ein Körper mit \\(m = ' + ein(m, 'kg') + '\\) hat \\(' + ein(0.5 * m * v * v, 'J') + '\\) Bewegungsenergie. Wie schnell ist er?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, Math.sqrt(A.E / A.m))) return 'Der Faktor \\(2\\) fehlt: \\(v = \\sqrt{\\dfrac{2 \\cdot E_\\text{kin}}{m}}\\).';
          if (nah(e.v, 2 * A.E / A.m)) return 'Das ist \\(v^2\\). Noch die Wurzel ziehen.';
          return '\\(E_\\text{kin} = \\tfrac12 \\cdot m \\cdot v^2\\) nach \\(v\\) auflösen: \\(v = \\sqrt{\\dfrac{2 \\cdot E_\\text{kin}}{m}}\\).'; },
        fehler: function(A){ return [[{ v: String(Math.sqrt(A.E / A.m)) }, 'Faktor'], [{ v: String(2 * A.E / A.m) }, 'Wurzel']]; },
        loesung: function(A){ return 'v = \\sqrt{\\dfrac{2 \\cdot E_\\text{kin}}{m}} = \\sqrt{\\dfrac{2 \\cdot ' + ein(A.E, 'J') + '}{' + ein(A.m, 'kg') + '}} ' + erg(A.v, 'm/s'); } },
      'bremsweg': { felder: ['s'], muster: '<i>s</i> = {s} m',
        neu: function(){
          var m, v, F;
          do { m = zufall([900, 1200, 1500, 1800]); v = zufall([12, 15, 20, 25, 30]); F = zufall([4500, 6000, 7500, 9000]); } while (F / m > 8 || F / m < 3 || (m === 1200 && v === 20 && F === 6000));   // plausibel; Simulation 2
          return { s: 0.5 * m * v * v / F, m: m, v: v, F: F, text: 'Ein Auto (\\(m = ' + ein(m, 'kg') + '\\)) fährt mit \\(' + ein(v, 'm/s') + '\\) und bremst mit der konstanten Kraft \\(' + ein(F, 'N') + '\\). Wie lang ist der Bremsweg?' }; },
        pruefen: function(A, e){
          if (nah(e.s, A.s)) return null;
          if (nah(e.s, A.m * A.v * A.v / A.F)) return 'Der Faktor \\(\\tfrac12\\) in \\(E_\\text{kin}\\) fehlt.';
          if (nah(e.s, 0.5 * A.m * A.v / A.F)) return 'Die Geschwindigkeit steht im Quadrat: \\(E_\\text{kin} = \\tfrac12 \\cdot m \\cdot v^2\\).';
          return 'Die Bremsarbeit nimmt die Bewegungsenergie: \\(F_B \\cdot s = \\tfrac12 \\cdot m \\cdot v^2\\).'; },
        fehler: function(A){ return [[{ s: String(A.m * A.v * A.v / A.F) }, 'Faktor'], [{ s: String(0.5 * A.m * A.v / A.F) }, 'Quadrat']]; },
        loesung: function(A){ return 'F_B \\cdot s = \\tfrac12 \\cdot m \\cdot v^2,\\quad s = \\dfrac{m \\cdot v^2}{2 \\cdot F_B} = \\dfrac{' + ein(A.m, 'kg') + ' \\cdot (' + ein(A.v, 'm/s') + ')^2}{2 \\cdot ' + ein(A.F, 'N') + '} ' + erg(A.s, 'm'); } },

      /* ----- Kapitel 3: Energieerhaltung ----- */
      'fall': { felder: ['v'], muster: '<i>v</i> = {v} m/s',
        neu: function(){
          var h, m;
          h = zufall([1.25, 3, 7, 10, 20, 80]); m = zufall([0.2, 0.5, 3, 70]);   // nicht 45 m (Mini-Check der Themenseite), nicht 5 m (Kontrollfrage)
          return { v: Math.sqrt(2 * G * h), h: h, m: m, text: 'Ein Körper (\\(m = ' + ein(m, 'kg') + '\\)) fällt aus \\(' + ein(h, 'm') + '\\) Höhe aus der Ruhe, ohne Luftwiderstand. Wie schnell ist er unten?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, Math.sqrt(G * A.h))) return 'Aus \\(m \\cdot g \\cdot h = \\tfrac12 \\cdot m \\cdot v^2\\) folgt \\(v = \\sqrt{2 \\cdot g \\cdot h}\\) — der Faktor \\(2\\) fehlt.';
          if (nah(e.v, 2 * G * A.h)) return 'Das ist \\(v^2\\). Noch die Wurzel ziehen.';
          if (nah(e.v, Math.sqrt(2 * A.m * G * A.h))) return 'Die Masse kürzt sich: Sie steht auf beiden Seiten von \\(m \\cdot g \\cdot h = \\tfrac12 \\cdot m \\cdot v^2\\).';
          return 'Energieerhaltung: \\(m \\cdot g \\cdot h = \\tfrac12 \\cdot m \\cdot v^2\\), also \\(v = \\sqrt{2 \\cdot g \\cdot h}\\).'; },
        fehler: function(A){ var l = [[{ v: String(Math.sqrt(G * A.h)) }, 'Faktor'], [{ v: String(2 * G * A.h) }, 'Wurzel']]; if (A.m !== 0.5) l.push([{ v: String(Math.sqrt(2 * A.m * G * A.h)) }, 'kürzt']); return l; },
        loesung: function(A){ return 'm \\cdot g \\cdot h = \\tfrac12 \\cdot m \\cdot v^2,\\quad v = \\sqrt{2 \\cdot g \\cdot h} = \\sqrt{2 \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + '} ' + erg(A.v, 'm/s'); } },
      'hoehe': { felder: ['h'], muster: '<i>h</i> = {h} m',
        neu: function(){ var v = zufall([3, 5, 8, 15, 2.5, 7]);   // nicht 10 m/s (Mini-Check der Themenseite), nicht 12 m/s (Aufgabe 3b), nicht 6 m/s (Kontrollfrage)
          return { h: v * v / (2 * G), v: v, text: 'Ein Ball wird mit \\(' + ein(v, 'm/s') + '\\) senkrecht nach oben geworfen. Wie hoch steigt er, ohne Luftwiderstand?' }; },
        pruefen: function(A, e){
          if (nah(e.h, A.h)) return null;
          if (nah(e.h, A.v * A.v / G)) return 'Der Faktor \\(2\\) fehlt: \\(h = \\dfrac{v^2}{2 \\cdot g}\\).';
          if (nah(e.h, A.v / (2 * G))) return 'Die Geschwindigkeit steht im Quadrat.';
          return 'Oben ist alles Lageenergie: \\(\\tfrac12 \\cdot m \\cdot v^2 = m \\cdot g \\cdot h\\).'; },
        fehler: function(A){ return [[{ h: String(A.v * A.v / G) }, 'Faktor'], [{ h: String(A.v / (2 * G)) }, 'Quadrat']]; },
        loesung: function(A){ return '\\tfrac12 \\cdot m \\cdot v^2 = m \\cdot g \\cdot h,\\quad h = \\dfrac{v^2}{2 \\cdot g} = \\dfrac{(' + ein(A.v, 'm/s') + ')^2}{2 \\cdot 9.81\\;\\text{m/s}^2} ' + erg(A.h, 'm'); } },
      'huegel': { felder: ['v'], muster: '<i>v</i> = {v} m/s',
        neu: function(){
          var h0, h2, v0;
          do { h0 = zufall([15, 18, 30, 40]); h2 = zufall([5, 8, 14, 25]); v0 = zufall([0, 3, 4, 6]); }
          while (h2 >= h0 || (h0 - h2 === 5 && v0 === 3) || Math.abs(v0 + Math.sqrt(2 * G * (h0 - h2)) - Math.sqrt(v0 * v0 + 2 * G * h0)) < 0.02 * Math.sqrt(v0 * v0 + 2 * G * h0));   // Clip, Simulation 3; Fehlermuster unterscheidbar
          return { v: Math.sqrt(v0 * v0 + 2 * G * (h0 - h2)), h0: h0, h2: h2, v0: v0,
            text: 'Ein Wagen fährt reibungsfrei mit \\(' + ein(v0, 'm/s') + '\\) auf \\(' + ein(h0, 'm') + '\\) Höhe los. Wie schnell ist er oben auf einem Hügel von \\(' + ein(h2, 'm') + '\\) Höhe?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (A.v0 && nah(e.v, Math.sqrt(2 * G * (A.h0 - A.h2)))) return 'Die Anfangsgeschwindigkeit bringt Bewegungsenergie mit: \\(\\tfrac12 \\cdot m \\cdot v_0^2\\) zählt zur Summe.';
          if (nah(e.v, Math.sqrt(A.v0 * A.v0 + 2 * G * A.h0))) return 'Das wäre das Tempo im Tal. Auf dem Hügel ist ein Teil wieder Lageenergie: \\(h_0 - h_2\\).';
          if (nah(e.v, A.v0 + Math.sqrt(2 * G * (A.h0 - A.h2)))) return 'Geschwindigkeiten addieren sich hier nicht — die Energien: \\(v^2 = v_0^2 + 2 \\cdot g \\cdot (h_0 - h_2)\\).';
          return 'Energieerhaltung: \\(m \\cdot g \\cdot h_0 + \\tfrac12 \\cdot m \\cdot v_0^2 = m \\cdot g \\cdot h_2 + \\tfrac12 \\cdot m \\cdot v^2\\).'; },
        fehler: function(A){ var l = [[{ v: String(Math.sqrt(A.v0 * A.v0 + 2 * G * A.h0)) }, 'Tal']]; if (A.v0){ l.push([{ v: String(Math.sqrt(2 * G * (A.h0 - A.h2))) }, 'Anfangsgeschwindigkeit']); l.push([{ v: String(A.v0 + Math.sqrt(2 * G * (A.h0 - A.h2))) }, 'Energien']); } return l; },
        loesung: function(A){ return 'v = \\sqrt{v_0^2 + 2 \\cdot g \\cdot (h_0 - h_2)} = \\sqrt{(' + ein(A.v0, 'm/s') + ')^2 + 2 \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h0 - A.h2, 'm') + '} ' + erg(A.v, 'm/s'); } },

      /* ----- Kapitel 4: Reibung und Motor ----- */
      'reibung': { felder: ['v'], muster: '<i>v</i> = {v} m/s',
        neu: function(){
          var m, h, s, F, E;
          do { m = zufall([40, 60, 80]); h = zufall([5, 8, 12, 20]); s = zufall([20, 40, 60, 100]); F = zufall([20, 30, 50, 80]); E = m * G * h - F * s; }
          while (E < 0.25 * m * G * h || s / h < 2.5);   // Simulation 4
          return { v: Math.sqrt(2 * E / m), m: m, h: h, s: s, F: F, E: E,
            text: 'Ein Schlitten mit Kind (\\(m = ' + ein(m, 'kg') + '\\)) fährt aus der Ruhe einen \\(' + ein(s, 'm') + '\\) langen Hang hinunter, \\(' + ein(h, 'm') + '\\) Höhenunterschied. Die Reibung beträgt \\(' + ein(F, 'N') + '\\). Wie schnell ist er unten?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, Math.sqrt(2 * G * A.h))) return 'Ohne Reibung wäre das richtig. Die Reibung macht aus \\(F_R \\cdot s\\) Wärme: \\(\\tfrac12 \\cdot m \\cdot v^2 = m \\cdot g \\cdot h - F_R \\cdot s\\).';
          if (nah(e.v, Math.sqrt(2 * (A.m * G * A.h + A.F * A.s) / A.m))) return 'Die Reibung liefert keine Energie, sie nimmt welche weg: abziehen.';
          if (nah(e.v, 2 * A.E / A.m)) return 'Das ist \\(v^2\\). Noch die Wurzel ziehen.';
          return 'Bilanz: \\(m \\cdot g \\cdot h = \\tfrac12 \\cdot m \\cdot v^2 + F_R \\cdot s\\).'; },
        fehler: function(A){ return [[{ v: String(Math.sqrt(2 * G * A.h)) }, 'Ohne Reibung'], [{ v: String(Math.sqrt(2 * (A.m * G * A.h + A.F * A.s) / A.m)) }, 'abziehen']]; },
        loesung: function(A){ return 'E_\\text{kin} = m \\cdot g \\cdot h - F_R \\cdot s = ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + ' - ' + ein(A.F, 'N') + ' \\cdot ' + ein(A.s, 'm') + ' ' + erg(A.E, 'J') + ',\\quad v = \\sqrt{\\dfrac{2 \\cdot E_\\text{kin}}{m}} ' + erg(A.v, 'm/s'); } },
      'waerme': { felder: ['W'], muster: '<i>E</i><sub>Wärme</sub> = {W} J',
        neu: function(){
          var m, h, v;
          do { m = zufall([50, 70, 90]); h = zufall([6, 10, 15, 30]); v = zufall([5, 8, 10, 12, 15]); } while (0.5 * v * v > 0.85 * G * h || 0.5 * v * v < 0.3 * G * h);
          return { W: m * G * h - 0.5 * m * v * v, m: m, h: h, v: v,
            text: 'Eine Skifahrerin (\\(m = ' + ein(m, 'kg') + '\\)) fährt aus der Ruhe \\(' + ein(h, 'm') + '\\) hinunter und ist unten \\(' + ein(v, 'm/s') + '\\) schnell. Wie viel Energie wurde durch Reibung und Luftwiderstand zu Wärme?' }; },
        pruefen: function(A, e){
          if (nah(e.W, A.W)) return null;
          if (nah(e.W, 0.5 * A.m * A.v * A.v)) return 'Das ist die Bewegungsenergie unten. Zu Wärme wurde, was davon an der Lageenergie fehlt.';
          if (nah(e.W, A.m * G * A.h)) return 'Das ist die ganze Lageenergie. Ein Teil davon steckt unten in der Bewegung.';
          if (nah(e.W, A.m * G * A.h - A.m * A.v * A.v)) return 'Der Faktor \\(\\tfrac12\\) in \\(E_\\text{kin}\\) fehlt.';
          return 'Bilanz: \\(m \\cdot g \\cdot h = \\tfrac12 \\cdot m \\cdot v^2 + E_\\text{Wärme}\\).'; },
        fehler: function(A){ return [[{ W: String(0.5 * A.m * A.v * A.v) }, 'Bewegungsenergie'], [{ W: String(A.m * G * A.h) }, 'ganze'], [{ W: String(A.m * G * A.h - A.m * A.v * A.v) }, 'Faktor']]; },
        loesung: function(A){ return 'E_\\text{Wärme} = m \\cdot g \\cdot h - \\tfrac12 \\cdot m \\cdot v^2 = ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + ' - \\tfrac12 \\cdot ' + ein(A.m, 'kg') + ' \\cdot (' + ein(A.v, 'm/s') + ')^2 ' + erg(A.W, 'J'); } },
      'motor': { felder: ['W'], muster: '<i>W</i><sub>M</sub> = {W} J',
        neu: function(){
          var O, h, s, F;
          do { O = zufall([['Ein E-Bike mit Fahrer', 100], ['Ein Kleinwagen', 900], ['Eine Standseilbahn-Kabine', 3000]]); h = zufall([20, 50, 80, 120]); s = zufall([400, 600, 1000, 1500]); F = zufall([20, 60, 300, 900]); }
          while (s / h < 6 || F > 0.05 * O[1] * G || F < 0.01 * O[1] * G);
          return { W: O[1] * G * h + F * s, m: O[1], h: h, s: s, F: F,
            text: O[0] + ' (\\(m = ' + ein(O[1], 'kg') + '\\)) fährt mit konstantem Tempo eine \\(' + ein(s, 'm') + '\\) lange Strecke hinauf, \\(' + ein(h, 'm') + '\\) Höhenunterschied. Die Reibung beträgt \\(' + ein(F, 'N') + '\\). Wie viel Arbeit muss der Motor verrichten?' }; },
        pruefen: function(A, e){
          if (nah(e.W, A.W)) return null;
          if (nah(e.W, A.m * G * A.h)) return 'Das ist nur die Lageenergie. Die Reibung kostet zusätzlich \\(F_R \\cdot s\\).';
          if (nah(e.W, A.m * G * A.h - A.F * A.s)) return 'Die Reibung arbeitet gegen den Motor: Ihre Arbeit kommt dazu, nicht weg.';
          if (nah(e.W, A.m * G * A.s + A.F * A.s)) return 'Hubarbeit mit dem Höhenunterschied \\(h\\), nicht mit der Streckenlänge.';
          return 'Konstantes Tempo: \\(W_M = m \\cdot g \\cdot h + F_R \\cdot s\\).'; },
        fehler: function(A){ return [[{ W: String(A.m * G * A.h) }, 'Lageenergie'], [{ W: String(A.m * G * A.h - A.F * A.s) }, 'gegen'], [{ W: String(A.m * G * A.s + A.F * A.s) }, 'Höhenunterschied']]; },
        loesung: function(A){ return 'W_M = m \\cdot g \\cdot h + F_R \\cdot s = ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + ' + ' + ein(A.F, 'N') + ' \\cdot ' + ein(A.s, 'm') + ' ' + erg(A.W, 'J'); } },

      /* ----- Kapitel 5: Leistung und Wirkungsgrad ----- */
      'leistung': { felder: ['P'], muster: '<i>P</i> = {P} W',
        neu: function(){
          var O, h, t;
          do { O = zufall([['Eine Person', 65], ['Ein Kran hebt eine Last', 400], ['Ein Lift mit Personen', 800]]); h = zufall([3, 6, 10, 15, 24]); t = zufall([4, 8, 12, 20, 30]); }
          while (O[1] * G * h / t > (O[1] < 100 ? 600 : 12000) || O[1] * G * h / t < 40 || (O[1] === 400 && h === 10 && t === 20));
          return { P: O[1] * G * h / t, m: O[1], h: h, t: t,
            text: O[0] + ' (\\(m = ' + ein(O[1], 'kg') + '\\)) ' + (O[1] === 65 ? 'steigt' : 'fährt') + ' in \\(' + ein(t, 's') + '\\) gleichmässig \\(' + ein(h, 'm') + '\\) hoch. Wie gross ist die Hubleistung?' }; },
        pruefen: function(A, e){
          if (nah(e.P, A.P)) return null;
          if (nah(e.P, A.m * G * A.h * A.t)) return 'Leistung ist Arbeit <em>pro</em> Zeit: \\(P = \\dfrac{W}{t}\\).';
          if (nah(e.P, A.m * A.h / A.t)) return 'Die Hubarbeit ist \\(m \\cdot g \\cdot h\\) — \\(g\\) fehlt.';
          if (nah(e.P, A.m * G * A.h)) return 'Das ist die Arbeit. Noch durch die Zeit teilen.';
          return '\\(P = \\dfrac{W}{t} = \\dfrac{m \\cdot g \\cdot h}{t}\\).'; },
        fehler: function(A){ return [[{ P: String(A.m * G * A.h * A.t) }, 'pro'], [{ P: String(A.m * A.h / A.t) }, 'fehlt'], [{ P: String(A.m * G * A.h) }, 'Arbeit']]; },
        loesung: function(A){ return 'P = \\dfrac{m \\cdot g \\cdot h}{t} = \\dfrac{' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + '}{' + ein(A.t, 's') + '} ' + erg(A.P, 'W'); } },
      'pfv': { felder: ['F'], muster: '<i>F</i> = {F} N',
        neu: function(){
          var P, v;
          do { P = zufall([15, 30, 45, 60, 90]); v = zufall([36, 54, 72, 90, 108]); } while (P === v || (P === 15 && v === 72) || P * 1000 / (v / 3.6) > 2500 || P * 1000 / (v / 3.6) < 300);   // plausibel: Fahrwiderstand 300 bis 2500 N   // Aufgabe 5b
          return { F: P * 1000 / (v / 3.6), P: P, v: v,
            text: 'Ein Auto fährt mit konstant \\(' + ein(v, 'km/h') + '\\); der Motor gibt dabei \\(' + ein(P, 'kW') + '\\) an die Räder ab. Wie gross ist die Antriebskraft? (\\(P = F \\cdot v\\))' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.P * 1000 / A.v)) return 'Erst in m/s umrechnen: ' + umr(A.v) + '.';
          if (nah(e.F, A.P / (A.v / 3.6))) return 'Die Leistung in Watt einsetzen: \\(' + ein(A.P, 'kW') + ' = ' + ein(A.P * 1000, 'W') + '\\).';
          if (nah(e.F, A.P * 1000 * A.v / 3.6)) return 'Aus \\(P = F \\cdot v\\) folgt \\(F = \\dfrac{P}{v}\\): durch die Geschwindigkeit teilen.';
          return '\\(F = \\dfrac{P}{v}\\) mit \\(P\\) in W und \\(v\\) in m/s.'; },
        fehler: function(A){ return [[{ F: String(A.P * 1000 / A.v) }, 'umrechnen'], [{ F: String(A.P / (A.v / 3.6)) }, 'Watt']]; },
        loesung: function(A){ return 'v = \\dfrac{' + tz(A.v) + '}{3.6}\\;\\text{m/s} ' + erg(A.v / 3.6, 'm/s') + ',\\quad F = \\dfrac{P}{v} = \\dfrac{' + ein(A.P * 1000, 'W') + '}{' + ein(+(A.v / 3.6).toPrecision(4), 'm/s') + '} ' + erg(A.F, 'N'); } },
      'eta': { felder: ['x'], muster: function(A){ return A.art === 'eta' ? '<i>η</i> = {x}' : '<i>P</i><sub>verl</sub> = {x} W'; },
        neu: function(){
          var G2 = zufall([['Ein Akkuschrauber', 300, 0.7], ['Eine Kaffeemaschine', 1000, 0.85], ['Ein Elektromotor', 1200, 0.9], ['Ein Netzteil', 40, 0.85], ['Ein Benzinmotor', 50000, 0.3]]);   // nicht LED und Glühlampe (Aufgabe 5d)
          if (Math.random() < 0.5) return { art: 'eta', x: G2[2], Pz: G2[1], Pn: G2[1] * G2[2], name: G2[0], text: G2[0] + ' nimmt \\(' + ein(G2[1], 'W') + '\\) auf und gibt \\(' + ein(+(G2[1] * G2[2]).toPrecision(4), 'W') + '\\) nutzbar ab. Wie gross ist der Wirkungsgrad? (als Dezimalzahl)' };
          return { art: 'verl', x: G2[1] * (1 - G2[2]), Pz: G2[1], e: G2[2], text: G2[0] + ' nimmt \\(' + ein(G2[1], 'W') + '\\) auf, der Wirkungsgrad ist \\(' + tz(G2[2]) + '\\). Wie gross ist die Verlustleistung?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'eta'){
            if (nah(e.x, A.Pz / A.Pn)) return 'Umgekehrt: Nutzen durch Aufwand, \\(\\eta = \\dfrac{P_\\text{nutz}}{P_\\text{zu}}\\) — er ist nie grösser als 1.';
            if (nah(e.x, A.x * 100)) return 'Gefragt ist die Dezimalzahl, nicht Prozent.';
            return '\\(\\eta = \\dfrac{P_\\text{nutz}}{P_\\text{zu}}\\).';
          }
          if (nah(e.x, A.Pz * A.e)) return 'Das ist die Nutzleistung. Verloren geht der Rest: \\(P_\\text{verl} = P_\\text{zu} - P_\\text{nutz}\\).';
          return '\\(P_\\text{verl} = P_\\text{zu} - \\eta \\cdot P_\\text{zu} = (1 - \\eta) \\cdot P_\\text{zu}\\).'; },
        fehler: function(A){ return A.art === 'eta' ? [[{ x: String(A.Pz / A.Pn) }, 'Umgekehrt'], [{ x: String(A.x * 100) }, 'Prozent']] : [[{ x: String(A.Pz * A.e) }, 'Nutzleistung']]; },
        loesung: function(A){ return A.art === 'eta' ? '\\eta = \\dfrac{P_\\text{nutz}}{P_\\text{zu}} = \\dfrac{' + ein(+A.Pn.toPrecision(4), 'W') + '}{' + ein(A.Pz, 'W') + '} = ' + tz(A.x)
                                                     : 'P_\\text{verl} = (1 - \\eta) \\cdot P_\\text{zu} = (1 - ' + tz(A.e) + ') \\cdot ' + ein(A.Pz, 'W') + ' ' + erg(A.x, 'W'); } },

      /* ----- Kapitel 6: Energiebilanz der Erde ----- */
      'albedo': { felder: ['P'], muster: '<i>P</i>/<i>A</i> = {P} W/m²',
        neu: function(){
          var O = zufall([['die Erde', 1361, [0.25, 0.32, 0.35], true], ['den Merkur', 9116, [0.07], false], ['den Jupiter', 50.5, [0.34], true], ['den Mond', 1361, [0.12], false]]), a = zufall(O[2]);   // nicht 0.28 (Simulation 6)
          return { P: (1 - a) * O[1] / 4, S: O[1], a: a, name: O[0], text: 'Auf ' + O[0] + ' treffen' + (O[3] ? ' ausserhalb der Atmosphäre' : '') + ' \\(S = ' + ein(O[1], 'W/m^2').replace('\\text{W/m^2}', '\\text{W/m}^2') + '\\), die Albedo ist \\(' + tz(a) + '\\). Wie viel Leistung je Quadratmeter nimmt der Himmelskörper im Mittel auf?' }; },
        pruefen: function(A, e){
          if (nah(e.P, A.P)) return null;
          if (nah(e.P, A.a * A.S / 4)) return 'Das ist der zurückgeworfene Anteil. Aufgenommen wird \\(1 - a\\).';
          if (nah(e.P, (1 - A.a) * A.S)) return 'Die Kugel fängt mit \\(\\pi R^2\\) auf, verteilt aber auf \\(4\\pi R^2\\): durch 4 teilen.';
          if (nah(e.P, A.S / 4)) return 'Die Albedo fehlt: Der Anteil \\(a\\) wird zurückgeworfen.';
          return '\\(\\dfrac{P}{A} = (1 - a) \\cdot \\dfrac{S}{4}\\).'; },
        fehler: function(A){ return [[{ P: String(A.a * A.S / 4) }, 'zurückgeworfene'], [{ P: String((1 - A.a) * A.S) }, '4'], [{ P: String(A.S / 4) }, 'Albedo']]; },
        loesung: function(A){ return '\\dfrac{P}{A} = (1 - a) \\cdot \\dfrac{S}{4} = (1 - ' + tz(A.a) + ') \\cdot \\dfrac{' + tz(A.S) + '\\;\\text{W/m}^2}{4} ' + erg(A.P, 'W/m^2').replace('\\text{W/m^2}', '\\text{W/m}^2'); } },
      'strahlung': { felder: ['P'], muster: '<i>P</i>/<i>A</i> = {P} W/m²',
        neu: function(){
          var c = Math.random() < 0.5, T = c ? zufall([-18, 0, 27, 40, 10]) : zufall([200, 255, 300, 320, 330]);   // nicht 15 °C (Mini-Check der Themenseite)
          var K = c ? T + 273.15 : T;
          return { P: SIG * Math.pow(K, 4), T: T, K: K, c: c, text: 'Eine Fläche hat die Temperatur \\(' + (c ? tz(T) + '\\;^\\circ\\text{C}' : ein(T, 'K')) + '\\). Wie viel Leistung je Quadratmeter strahlt sie ab? (\\(\\sigma = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)\\))' }; },
        pruefen: function(A, e){
          if (nah(e.P, A.P)) return null;
          if (A.c && nah(e.P, SIG * Math.pow(A.T, 4))) return 'Die Temperatur in Kelvin einsetzen: \\(T = ' + tz(A.T) + ' + 273.15\\;\\text{K}\\).';
          if (nah(e.P, SIG * A.K)) return 'Die Temperatur steht in der vierten Potenz: \\(\\dfrac{P}{A} = \\sigma \\cdot T^4\\).';
          if (nah(e.P, SIG * Math.pow(A.K, 2))) return 'Vierte Potenz, nicht Quadrat.';
          return '\\(\\dfrac{P}{A} = \\sigma \\cdot T^4\\) mit \\(T\\) in Kelvin.'; },
        fehler: function(A){ var l = [[{ P: String(SIG * Math.pow(A.K, 2)) }, 'Quadrat']]; if (A.c && A.T !== 0) l.push([{ P: String(SIG * Math.pow(A.T, 4)) }, 'Kelvin']); return l; },
        loesung: function(A){ return (A.c ? 'T = ' + tz(A.T) + ' + 273.15\\;\\text{K} = ' + ein(+A.K.toFixed(2), 'K') + ',\\quad ' : '') + '\\dfrac{P}{A} = \\sigma \\cdot T^4 = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4) \\cdot (' + ein(+A.K.toFixed(2), 'K') + ')^4 ' + erg(A.P, 'W/m^2').replace('\\text{W/m^2}', '\\text{W/m}^2'); } },
      'gleichgewicht': { felder: ['T'], muster: '<i>T</i> = {T} K',
        neu: function(){ var P = zufall([200, 300, 400, 125, 180, 260]);   // nicht 238 W/m² (Themenseite), nicht rund 150 W/m² (Gesamttest G6)
          return { T: Math.pow(P / SIG, 0.25), P: P, text: 'Ein Planet ohne Atmosphäre nimmt im Mittel \\(' + ein(P, 'W/m^2').replace('\\text{W/m^2}', '\\text{W/m}^2') + '\\) auf. Bei welcher Temperatur strahlt er gleich viel ab? (\\(\\sigma = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)\\))' }; },
        pruefen: function(A, e){
          if (nah(e.T, A.T)) return null;
          if (nah(e.T, Math.sqrt(A.P / SIG))) return 'Vierte Wurzel, nicht Quadratwurzel: \\(T = \\sqrt[4]{\\dfrac{P/A}{\\sigma}}\\).';
          if (nah(e.T, A.T - 273.15)) return 'Das ist in Grad Celsius. Gefragt ist Kelvin.';
          return 'Gleichgewicht: \\(\\sigma \\cdot T^4 = \\dfrac{P}{A}\\), also \\(T = \\sqrt[4]{\\dfrac{P/A}{\\sigma}}\\).'; },
        fehler: function(A){ return [[{ T: String(Math.sqrt(A.P / SIG)) }, 'Vierte'], [{ T: String(A.T - 273.15) }, 'Celsius']]; },
        loesung: function(A){ return '\\sigma \\cdot T^4 = \\dfrac{P}{A},\\quad T = \\sqrt[4]{\\dfrac{' + tz(A.P) + '\\;\\text{W/m}^2}{5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)}} ' + erg(A.T, 'K'); } }
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
