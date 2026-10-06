<script>
/* Leitprogramm Kinematik — Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Gerüst (Achsen, Bedienung, Leiste, Übungsrahmen)
   wörtlich aus dem Leitprogramm Elektrizität (scripts/lp/elektrizitaet/seite.js);
   Simulationen und Übungstypen für 4.1 neu. Formelzeichen, g = 9.81 m/s² und
   Beispielwerte wie auf Themenseite 4.1. Farben wie dort (STYLEGUIDE §5.2):
   s Bernstein, v Grün, a und Komponenten Violett, a_z und Resultierende Rot.
   Zahlen mit Dezimalpunkt und echtem Minus; in Wertanzeigen ist «·» nur
   Malpunkt, Trenner ist der Strichpunkt. */
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


  var G = 9.81;                                          // wie Themenseite 4.1
  var GRAD = Math.PI / 180;
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

  /* ---------- Kapitel 1: Ort und Geschwindigkeit ----------
     Rechnet wie Animation 1 der Themenseite s(t) = s0 + v·t, zeigt aber nur das
     s-t-Diagramm — dafür mit einer zweiten, gestrichelten Geraden für Einholen und
     Zielspiel und einem Steigungsdreieck (Hilfslinie): Die Steigung ist v.
     Startwert = Clipbeispiel: Velofahrerin bei 20 m mit 5 m/s, nach 8 s bei 60 m. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var K = Achsen(svg, { w: 300, h: 260, x0: -1.5, x1: 12.6, y0: -16, y1: 124, sx: 1, sy: 10, xm: [2, 4, 6, 8, 10, 12], ym: [20, 40, 60, 80, 100, 120], xname: 't [s]', yname: 's [m]' });
    var ziel = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    var sim = {
      zustand: function(){ var v_ = B.wert('v'), s0 = B.wert('s0'), t = B.wert('t'); return { v: v_, s0: s0, t: t, s: s0 + v_ * t, bewegt: B.bewegt }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var v_ = B.wert('v'), s0 = B.wert('s0'), t = B.wert('t'), s = s0 + v_ * t;
      B.anzeigen(); K.leeren();
      if (ziel){
        K.kurve(function(x){ return ziel.s0 + ziel.v * x; }, 'zielkurve', 0);
        if (ziel.name){ var yb = ziel.s0 + ziel.v * 11.6; K.text(11.6, yb + (yb > 100 ? -12 : 6), ziel.name, 'ziel-text', 'end'); }
      }
      // Steigungsdreieck von t = 1 s bis 2 s: waagrecht 1 s, senkrecht v · 1 s
      var a1 = s0 + v_, a2 = s0 + 2 * v_;
      if (Math.abs(v_) > 0.01){
        K.kurve(function(){ return a1; }, 'dreieck hilfslinie', 1, 2);
        el(K.ebene, 'line', { x1: K.X(2), y1: K.Y(a1), x2: K.X(2), y2: K.Y(a2), 'class': 'dreieck hilfslinie' });
        K.text(1.5, a1 + (v_ > 0 ? -7 : 4), '1 s', 'hilf-text hilfslinie');
        K.text(2.25, (a1 + a2) / 2 - 1.5, 'Δs = ' + zahl(v_) + NB + 'm', 'hilf-text hilfslinie', 'start');
      }
      K.kurve(function(x){ return s0 + v_ * x; }, 'kurve-s', 0);
      K.punkt(t, s, 'p-s', '(' + zahl(t) + NB + 's; ' + sig(s) + NB + 'm)', t > 6 ? -9 : 9, s > 100 ? 18 : -9, t > 6 ? 'end' : 'start');
      rolle(fig, 'formel').innerHTML =
        '<span>' + v('s') + ' = ' + v('s') + '₀ + ' + v('v') + ' · ' + v('t') + ' = ' + zahl(s0) + NB + 'm + ' + ew(v_, 'm/s') + ' · ' + zahl(t) + NB + 's = ' + zahl(s) + NB + 'm</span>' +
        '<span>' + v('v') + ' = ' + zahl(v_) + NB + 'm/s = ' + zahl(v_) + ' · 3.6' + NB + 'km/h = ' + zahl(+(v_ * 3.6).toFixed(6)) + NB + 'km/h</span>' +
        (s > 124 || s < -16 ? '<span class="sim-notiz">Der Punkt liegt ausserhalb des Bildes.</span>' : '');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh an allen drei Reglern. Was bestimmt \\(v\\) an der Geraden, was \\(s_0\\)? Notiere deine Antwort.', ok: function(s){ return s.bewegt.v && s.bewegt.s0 && s.bewegt.t; },
        vergleich: 'Die Geschwindigkeit \\(v\\) ist die Steigung: Das Dreieck zeigt, wie viele Meter in einer Sekunde dazukommen. Der Startort \\(s_0\\) verschiebt die Gerade nur nach oben oder unten. Der Regler \\(t\\) bewegt bloss den Punkt auf der Geraden.' },
      { text: 'Ein Jogger startet bei \\(0\\;\\text{m}\\) und läuft mit \\(3\\;\\text{m/s}\\). Stelle ein: Wo ist er nach \\(10\\;\\text{s}\\)?', ok: function(s){ return gl(s.v, 3) && gl(s.s0, 0) && gl(s.t, 10); } },
      { text: 'Ein Tram fährt mit \\(36\\;\\text{km/h}\\). Stelle seine Geschwindigkeit in \\(\\text{m/s}\\) ein.', ok: function(s){ return gl(s.v, 10); } },
      { text: 'Ein Wagen startet bei \\(50\\;\\text{m}\\) und rollt mit \\(2.5\\;\\text{m/s}\\) zurück zum Nullpunkt. Stelle ein.', ok: function(s){ return gl(s.v, -2.5) && gl(s.s0, 50); } },
      { text: 'Einholen: B startet bei \\(20\\;\\text{m}\\) mit \\(3\\;\\text{m/s}\\) (gestrichelt). Du startest gleichzeitig bei \\(0\\;\\text{m}\\) mit \\(5\\;\\text{m/s}\\). Stelle Geschwindigkeit und Start ein und dann die Zeit, zu der du B einholst.', setup: function(S){ ziel = { s0: 20, v: 3, name: 'B' }; S.setze({ v: 2, s0: 0, t: 2 }); }, ok: function(s){ return gl(s.v, 5) && gl(s.s0, 0) && gl(s.t, 10); } },
      { text: 'Triff die gestrichelte Gerade. Welche Bewegung stellt sie dar? Notiere.', setup: function(S){ ziel = { s0: 40, v: -3 }; S.setze({ v: 2, s0: 10 }); }, ok: function(s){ return gl(s.v, -3) && gl(s.s0, 40); },
        vergleich: 'Eine gleichförmige Bewegung zurück zum Nullpunkt: Start bei \\(40\\;\\text{m}\\), jede Sekunde \\(3\\;\\text{m}\\) näher, also \\(v = -3\\;\\text{m/s}\\). Nach rund \\(13.3\\;\\text{s}\\) wäre der Körper dort.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Beschleunigung, Steigung und Fläche ----------
     Rechnet wie Animation 2 der Themenseite v = v0 + a·t und s = v0·t + ½·a·t², zeigt
     aber nur das v-t-Diagramm und färbt die Fläche darunter: Sie ist der Weg.
     Unter der t-Achse (Rückwärtsfahrt) zählt die Fläche negativ und ist anders
     gefärbt. Startwert = Clipbeispiel: aus dem Stand mit 2.5 m/s², nach 8 s 20 m/s und 80 m. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var K = Achsen(svg, { w: 300, h: 260, x0: -1.4, x1: 11, y0: -16, y1: 36, sx: 1, sy: 5, xm: [2, 4, 6, 8, 10], ym: [-10, 10, 20, 30], xname: 't [s]', yname: 'v [m/s]' });
    var ziel = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    var sim = {
      zustand: function(){ var v0 = B.wert('v0'), a = B.wert('a'), t = B.wert('t'); return { v0: v0, a: a, t: t, v: v0 + a * t, s: v0 * t + 0.5 * a * t * t, bewegt: B.bewegt }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; B.zuruecksetzen(); }
    };
    function flaeche(v0, a, ta, tb){
      if (tb - ta < 1e-9) return;
      var vm = v0 + a * (ta + tb) / 2;
      el(K.ebene, 'polygon', { points: [[ta, 0], [ta, v0 + a * ta], [tb, v0 + a * tb], [tb, 0]].map(function(p){ return K.X(p[0]).toFixed(1) + ',' + K.Y(p[1]).toFixed(1); }).join(' '),
        'class': vm >= 0 ? 'feld' : 'feld-neg', 'clip-path': K.clip });
    }
    function zeichnen(){
      var v0 = B.wert('v0'), a = B.wert('a'), t = B.wert('t'), vt = v0 + a * t, s = v0 * t + 0.5 * a * t * t;
      B.anzeigen(); K.leeren();
      var tz = Math.abs(a) > 1e-9 ? -v0 / a : -1, kreuzt = tz > 0 && tz < t;
      if (kreuzt){ flaeche(v0, a, 0, tz); flaeche(v0, a, tz, t); } else flaeche(v0, a, 0, t);
      if (ziel) K.kurve(function(x){ return ziel.v0 + ziel.a * x; }, 'zielkurve', 0);
      // Steigungsdreieck ab dem Punkt nach rechts (waagrecht 1 s, senkrecht a · 1 s): Die Schenkel
      // liegen neben dem Punkt, nicht unter seiner Beschriftung. Bei t > 9 s links davon.
      var rechts = t <= 9, ta = rechts ? t : t - 1, b1 = v0 + a * ta, b2 = v0 + a * (ta + 1);
      if (Math.abs(a) > 0.01){
        K.kurve(function(){ return b1; }, 'dreieck hilfslinie', ta, ta + 1);
        el(K.ebene, 'line', { x1: K.X(ta + 1), y1: K.Y(b1), x2: K.X(ta + 1), y2: K.Y(b2), 'class': 'dreieck hilfslinie' });
        K.text(ta + 0.5, b1 + (a > 0 ? -3.2 : 1.4), '1' + NB + 's', 'hilf-text hilfslinie');
        // steigend: rechts neben der Mitte des senkrechten Schenkels (die Gerade läuft darüber weiter);
        // fallend: auf Höhe der oberen Kante (die Gerade läuft unter dem Dreieck weiter)
        K.text(ta + 1.15, a > 0 ? (b1 + b2) / 2 - 0.6 : b1 + 0.4, 'Δv = ' + zahl(a) + NB + 'm/s', 'hilf-text hilfslinie', 'start');
      }
      // Bis zum eingestellten t kräftig, danach blass: Nach dem Stillstand fährt ein bremsendes
      // Auto nicht zurück — die Gerade zeigt dort nur, wie es mit derselben Beschleunigung weiterginge.
      K.kurve(function(x){ return v0 + a * x; }, 'kurve-v', 0, t);
      K.kurve(function(x){ return v0 + a * x; }, 'kurve-weiter', t);
      if (!kreuzt && t >= 4 && Math.abs(v0 + vt) / 2 >= 6) K.text(t * 0.36, (v0 + vt) / 2 * 0.3, 's ' + ist(s, sig(s)) + sig(s) + NB + 'm', 'flaeche-text');
      // Beschriftung (t; v) links vom Punkt: oberhalb, wenn die Gerade steigt, unterhalb, wenn sie fällt —
      // dort verläuft sie nicht. Steht der Körper beim Bremsen (|v| klein), nur der Punkt.
      var lab = '(' + zahl(t) + NB + 's; ' + sig(vt) + NB + 'm/s)';
      if (a >= 0) K.punkt(t, vt, 'p-v', lab, -9, vt > 28 ? 18 : -9, 'end');
      else K.punkt(t, vt, 'p-v', Math.abs(vt) < 4 ? '' : lab, -9, 18, 'end');
      rolle(fig, 'formel').innerHTML =
        '<span>' + v('v') + ' = ' + v('v') + '₀ + ' + v('a') + ' · ' + v('t') + ' = ' + zahl(v0) + NB + 'm/s + ' + ew(a, 'm/s²') + ' · ' + zahl(t) + NB + 's = ' + zahl(+vt.toFixed(6)) + NB + 'm/s</span>' +
        '<span>' + v('s') + ' = ' + v('v') + '₀ · ' + v('t') + ' + ½ · ' + v('a') + ' · ' + v('t') + '² = ' + zahl(v0) + NB + 'm/s · ' + zahl(t) + NB + 's + ½ · ' + ew(a, 'm/s²') + ' · (' + zahl(t) + NB + 's)² = ' + zahl(+s.toFixed(6)) + NB + 'm</span>' +
        (kreuzt ? '<span class="sim-notiz">Unter der t-Achse fährt der Körper rückwärts: Diese Fläche zählt negativ.</span>' : '') +
        (vt > 36 || vt < -16 ? '<span class="sim-notiz">Der Punkt liegt ausserhalb des Bildes.</span>' : '');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh an allen drei Reglern. Was zeigt die Steigung der Geraden, was die gefärbte Fläche? Notiere deine Antwort mit Einheiten.', ok: function(s){ return s.bewegt.v0 && s.bewegt.a && s.bewegt.t; },
        vergleich: 'Die Steigung ist die Beschleunigung \\(a\\) in \\(\\text{m/s}^2\\): So viel kommt je Sekunde zur Geschwindigkeit dazu. Die Fläche unter der Geraden ist der Weg \\(s\\): Höhe in \\(\\text{m/s}\\) mal Breite in \\(\\text{s}\\) gibt \\(\\text{m}\\).' },
      { text: 'Ein Velo fährt aus dem Stand los und beschleunigt mit \\(1.5\\;\\text{m/s}^2\\). Stelle ein: Wie schnell ist es nach \\(6\\;\\text{s}\\)?', ok: function(s){ return gl(s.v0, 0) && gl(s.a, 1.5) && gl(s.t, 6); } },
      { text: 'Ein Zug fährt mit \\(20\\;\\text{m/s}\\) und bremst mit \\(2\\;\\text{m/s}^2\\). Stelle den Zeitpunkt ein, an dem er steht, und lies den Bremsweg ab. Notiere ihn: In der nächsten Aufgabe vergleichst du.', ok: function(s){ return gl(s.v0, 20) && gl(s.a, -2) && gl(s.t, 10); },
        vergleich: 'Er steht nach \\(10\\;\\text{s}\\). Bremsweg = Dreiecksfläche unter der Geraden: \\(s = \\tfrac12 \\cdot 10\\;\\text{s} \\cdot 20\\;\\text{m/s} = 100\\;\\text{m}\\).' },
      { text: 'Gleiche Bremsung, aber nur \\(10\\;\\text{m/s}\\): Stelle wieder den Stillstand ein. Wie viel kürzer ist der Bremsweg? Notiere.', ok: function(s){ return gl(s.v0, 10) && gl(s.a, -2) && gl(s.t, 5); },
        vergleich: '\\(25\\;\\text{m}\\) statt \\(100\\;\\text{m}\\): ein Viertel. Halbe Geschwindigkeit, viertel Bremsweg — das Dreieck ist halb so hoch und halb so breit. Rechnerisch: \\(s = \\dfrac{v_0^2}{2 \\cdot |a|}\\).' },
      { text: 'Ein Körper soll in \\(4\\;\\text{s}\\) von \\(6\\;\\text{m/s}\\) auf \\(18\\;\\text{m/s}\\) kommen. Stelle \\(v_0\\), \\(t\\) und die nötige Beschleunigung \\(a\\) ein. Welchen Weg legt er dabei zurück? Notiere.', ok: function(s){ return gl(s.v0, 6) && gl(s.a, 3) && gl(s.t, 4); },
        vergleich: '\\(a = \\dfrac{\\Delta v}{\\Delta t} = \\dfrac{12\\;\\text{m/s}}{4\\;\\text{s}} = 3\\;\\text{m/s}^2\\). Der Weg ist das Trapez unter der Geraden: \\(s = 6\\;\\text{m/s} \\cdot 4\\;\\text{s} + \\tfrac12 \\cdot 3\\;\\text{m/s}^2 \\cdot (4\\;\\text{s})^2 = 48\\;\\text{m}\\).' },
      { text: 'Triff die gestrichelte Gerade. Welche Bewegungsart stellt der Graf dar? Notiere.', setup: function(S){ ziel = { v0: 24, a: -3 }; S.setze({ v0: 10, a: 1 }); }, ok: function(s){ return gl(s.v0, 24) && gl(s.a, -3); },
        vergleich: 'Eine gleichmässig verzögerte (gebremste) Bewegung: Start mit \\(24\\;\\text{m/s}\\), jede Sekunde \\(3\\;\\text{m/s}\\) langsamer, \\(a = -3\\;\\text{m/s}^2\\). Nach \\(8\\;\\text{s}\\) steht der Körper, nach \\(\\tfrac12 \\cdot 8\\;\\text{s} \\cdot 24\\;\\text{m/s} = 96\\;\\text{m}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Fall und Wurf (sim3) ----------
     Rechnet wie Animation 4 der Themenseite x = v0·cos α·t und y = v0·sin α·t − ½·g·t²,
     dazu eine Abwurfhöhe h0 (für Fall und waagrechten Wurf, wie im Mini-Check der
     Themenseite). Statt eines laufenden Balls zeigt sie den Ort alle 0.25 s als Punkte
     und deren Projektion auf die Achsen (Hilfslinien): waagrecht gleiche, senkrecht
     wachsende Abstände. x-y-Bahn im Massstab 1:1. Startwert = Clipbeispiel:
     waagrecht mit 8 m/s aus 20 m Höhe, Landung nach 2.02 s bei 16.2 m. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var K = Achsen(svg, { w: 300, h: 208, x0: -3, x1: 62, y0: -3, y1: 42, sx: 5, sy: 5, xm: [10, 20, 30, 40, 50, 60], ym: [10, 20, 30, 40], xname: 'x [m]', yname: 'y [m]' });
    var ziel = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    function wk(al){ return al < 0 ? '(−' + (-al) + '°)' : ' ' + al + '°'; }   // sin(−90°), nicht «sin -90°»
    function wurf(v0, al, h0){
      var vx = v0 * Math.cos(al * GRAD), vy = v0 * Math.sin(al * GRAD);
      var tF = (vy + Math.sqrt(vy * vy + 2 * G * h0)) / G;
      return { vx: vx, vy: vy, tF: tF, xF: vx * tF, hMax: h0 + (vy > 0 ? vy * vy / (2 * G) : 0) };
    }
    var sim = {
      zustand: function(){ var v0 = B.wert('v0'), al = B.wert('al'), h0 = B.wert('h0'), w = wurf(v0, al, h0);
        return { v0: v0, al: al, h0: h0, tF: w.tF, xF: w.xF, bewegt: B.bewegt }; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var v0 = B.wert('v0'), al = B.wert('al'), h0 = B.wert('h0'), w = wurf(v0, al, h0);
      B.anzeigen(); K.leeren();
      if (h0 > 0) el(K.ebene, 'line', { x1: K.X(0), y1: K.Y(0), x2: K.X(0), y2: K.Y(h0), 'class': 'turm' });
      if (ziel != null){
        el(K.ebene, 'rect', { x: K.X(ziel - 1.5), y: K.Y(1.6), width: K.X(ziel + 1.5) - K.X(ziel - 1.5), height: K.Y(0) - K.Y(1.6), 'class': 'zielmarke' });
        K.text(ziel, 3.2, 'Ziel', 'ziel-text');
      }
      var fertig = w.tF > 1e-9;
      if (fertig){
        var pkt = [], k;
        for (k = 0; k <= 160; k++){ var tt = w.tF * k / 160; pkt.push(K.X(w.vx * tt).toFixed(1) + ',' + K.Y(h0 + w.vy * tt - 0.5 * G * tt * tt).toFixed(1)); }
        el(K.ebene, 'polyline', { points: pkt.join(' '), 'class': 'bahn', 'clip-path': K.clip });
        // Ort alle 0.25 s, mit Projektion auf beide Achsen
        // Senkrechter Wurf: Aufweg links, Abweg rechts der Achse (wie im Lehrbuch nebeneinander),
        // sonst lägen alle Punkte auf der y-Achse und der Rückweg auf dem Hinweg.
        var senk = Math.abs(al) === 90;
        for (k = 0; k * 0.25 <= w.tF + 1e-9; k++){
          var t = k * 0.25, x = senk ? (w.vy - G * t > 0 ? -1.5 : 1.5) : w.vx * t, y = h0 + w.vy * t - 0.5 * G * t * t;
          if (x > 62 || y > 42) continue;
          el(K.ebene, 'line', { x1: K.X(x), y1: K.Y(0) - 3, x2: K.X(x), y2: K.Y(0) + 3, 'class': 'proj hilfslinie' });
          el(K.ebene, 'line', { x1: K.X(0) - 3, y1: K.Y(y), x2: K.X(0) + 3, y2: K.Y(y), 'class': 'proj hilfslinie' });
          el(K.ebene, 'circle', { cx: K.X(x), cy: K.Y(y), r: 3, 'class': 'p-s' });
        }
        if (w.xF <= 62 && Math.abs(al) < 90) K.punkt(w.xF, 0, 'p-land', 'x = ' + sig(w.xF) + NB + 'm', w.xF > 42 ? -6 : 6, -9, w.xF > 42 ? 'end' : 'start');
      }
      var zeilen = '';
      if (!fertig) zeilen = v0 > 0 ? '<span>Waagrecht oder nach unten vom Boden aus gibt es keinen Flug.</span>' : '<span>Ohne Abwurfhöhe und ohne Abwurfgeschwindigkeit bewegt sich nichts.</span>';
      else {
        if (Math.abs(w.vy) < 1e-9)
          zeilen += '<span>' + v('t') + '<sub>F</sub> = √(2 · ' + v('h') + '₀ / ' + v('g') + ') = √(2 · ' + zahl(h0) + NB + 'm / 9.81' + NB + 'm/s²) ' + ist(w.tF, sig(w.tF)) + sig(w.tF) + NB + 's</span>';
        else if (h0 === 0)
          zeilen += '<span>' + v('t') + '<sub>F</sub> = 2 · ' + v('v') + '₀ · sin ' + v('α') + ' / ' + v('g') + ' = 2 · ' + zahl(v0) + NB + 'm/s · sin' + wk(al) + ' / 9.81' + NB + 'm/s² ' + ist(w.tF, sig(w.tF)) + sig(w.tF) + NB + 's</span>';
        else
          zeilen += '<span>' + v('t') + '<sub>F</sub> aus ' + v('h') + '₀ + ' + v('v') + '₀ · sin ' + v('α') + ' · ' + v('t') + '<sub>F</sub> − ½ · ' + v('g') + ' · ' + v('t') + '<sub>F</sub>² = 0, also ' + zahl(h0) + NB + 'm + ' + zahl(v0) + NB + 'm/s · sin' + wk(al) + ' · ' + v('t') + '<sub>F</sub> − ½ · 9.81' + NB + 'm/s² · ' + v('t') + '<sub>F</sub>² = 0: ' + v('t') + '<sub>F</sub> ' + ist(w.tF, sig(w.tF)) + sig(w.tF) + NB + 's</span>';
        if (Math.abs(al) === 90 && w.vy > 0) zeilen += '<span>' + v('t') + '<sub>S</sub> = ' + v('v') + '₀ / ' + v('g') + ' = ' + zahl(v0) + NB + 'm/s / 9.81' + NB + 'm/s² ' + ist(w.vy / G, sig(w.vy / G)) + sig(w.vy / G) + NB + 's (Steigzeit)</span>';
        if (Math.abs(al) !== 90) zeilen += '<span>' + v('x') + '<sub>F</sub> = ' + v('v') + '₀ · cos ' + v('α') + ' · ' + v('t') + '<sub>F</sub> = ' + zahl(v0) + NB + 'm/s · cos' + wk(al) + ' · ' + sig(w.tF) + NB + 's ' + ist(w.xF, sig(w.xF)) + sig(w.xF) + NB + 'm</span>';
        if (w.vy > 1e-9) zeilen += '<span>' + v('h') + '<sub>max</sub> = ' + v('h') + '₀ + (' + v('v') + '₀ · sin ' + v('α') + ')² / (2 · ' + v('g') + ') = ' + zahl(h0) + NB + 'm + (' + zahl(v0) + NB + 'm/s · sin' + wk(al) + ')² / (2 · 9.81' + NB + 'm/s²) ' + ist(w.hMax, sig(w.hMax)) + sig(w.hMax) + NB + 'm</span>';
        if (w.xF > 62 || w.hMax > 42) zeilen += '<span class="sim-notiz">Ein Teil der Bahn liegt ausserhalb des Bildes.</span>';
      }
      if (fertig && Math.abs(al) === 90) zeilen += '<span class="sim-notiz">Senkrecht: Aufweg links, Abweg rechts der Achse gezeichnet, damit sich die Punkte nicht decken.</span>';
      rolle(fig, 'formel').innerHTML = zeilen;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh an allen drei Reglern. Die Punkte zeigen den Ball alle \\(0.25\\;\\text{s}\\). Was bleibt waagrecht gleich, was wächst senkrecht? Notiere deine Antwort.', ok: function(s){ return s.bewegt.v0 && s.bewegt.al && s.bewegt.h0; },
        vergleich: 'Waagrecht liegen die Punkte immer gleich weit auseinander: Die waagrechte Bewegung ist gleichförmig, \\(x = v_0 \\cdot \\cos\\alpha \\cdot t\\). Senkrecht werden die Abstände nach unten immer grösser: Die senkrechte Bewegung ist gleichmässig beschleunigt mit \\(g\\).' },
      { text: 'Freier Fall: Lass den Ball aus \\(30\\;\\text{m}\\) Höhe einfach fallen. Stelle ein und lies die Fallzeit ab.', ok: function(s){ return gl(s.v0, 0) && gl(s.h0, 30); } },
      { text: 'Gleiche Höhe, aber waagrecht mit \\(10\\;\\text{m/s}\\) geworfen: Stelle ein. Ändert sich die Fallzeit? Notiere.', ok: function(s){ return gl(s.v0, 10) && gl(s.al, 0) && gl(s.h0, 30); },
        vergleich: 'Nein: wieder rund \\(2.47\\;\\text{s}\\). Die senkrechte Bewegung hängt nur von der Höhe und von \\(g\\) ab; die waagrechte kommt dazu, ohne sie zu stören.' },
      { text: 'Senkrecht nach oben: Wirf den Ball vom Boden mit \\(15\\;\\text{m/s}\\) unter \\(\\alpha = 90^\\circ\\). Lies die Steighöhe ab. Wie lange steigt er, wie lange fällt er zurück? Notiere.', ok: function(s){ return gl(s.h0, 0) && gl(s.v0, 15) && gl(s.al, 90); },
        vergleich: 'Steighöhe \\(h_\\text{max} = \\dfrac{v_0^2}{2 \\cdot g} \\approx 11.5\\;\\text{m}\\). Er steigt \\(t_S = \\dfrac{v_0}{g} \\approx 1.53\\;\\text{s}\\) und fällt genau so lange zurück: Flugzeit \\(3.06\\;\\text{s}\\). Unten ist er wieder \\(15\\;\\text{m/s}\\) schnell, jetzt nach unten. Die Punkte oben liegen dichter: Dort ist er langsam.' },
      { text: 'Senkrecht nach unten: Wirf den Ball aus \\(20\\;\\text{m}\\) Höhe mit \\(5\\;\\text{m/s}\\) unter \\(\\alpha = -90^\\circ\\). Vergleiche die Flugzeit mit dem freien Fall aus \\(20\\;\\text{m}\\).', ok: function(s){ return gl(s.h0, 20) && gl(s.v0, 5) && gl(s.al, -90); },
        vergleich: 'Rund \\(1.57\\;\\text{s}\\) statt \\(2.02\\;\\text{s}\\): Er startet schon mit \\(5\\;\\text{m/s}\\) nach unten, und dazu kommt die Beschleunigung, \\(h = v_0 \\cdot t + \\tfrac12 \\cdot g \\cdot t^2\\).' },
      { text: 'Wurf vom Boden mit \\(12\\;\\text{m/s}\\): Finde den Winkel mit der grössten Wurfweite.', setup: function(S){ S.setze({ h0: 0, v0: 12, al: 20 }); }, ok: function(s){ return gl(s.h0, 0) && gl(s.v0, 12) && gl(s.al, 45); } },
      { text: 'Vom Boden mit \\(12\\;\\text{m/s}\\) unter \\(25^\\circ\\): Finde einen zweiten Winkel mit derselben Weite.', setup: function(S){ S.setze({ h0: 0, v0: 12, al: 25 }); }, ok: function(s){ return gl(s.h0, 0) && gl(s.v0, 12) && gl(s.al, 65); } },
      { text: 'Triff das Ziel bei \\(x = 30\\;\\text{m}\\) — Abwurf vom Boden.', setup: function(S){ ziel = 30; S.setze({ h0: 0, v0: 10, al: 30 }); }, ok: function(s){ return gl(s.h0, 0) && Math.abs(s.xF - 30) < 0.6; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Geschwindigkeit als Vektor (sim4) ----------
     Rechnet wie Animation 6 der Themenseite (Flussbreite 40 m, β = Schwimmrichtung
     gegen die Strömung gemessen, 90° = quer), zeigt aber keinen laufenden Schwimmer:
     die drei Pfeile am Start (v_S grün, v_F violett, v_Ufer rot, wie dort) und die
     Bahn bis zum Zielufer mit Landepunkt — Querzeit und Versatz stehen im Bild.
     Draufsicht 1:1, Pfeile 1 m/s ≙ 8 m. Startwert = Clipbeispiel: 2 m/s quer, 1 m/s Strömung. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var BR = 40, X0 = -35, X1 = 85, Y1 = 50, M = 2.5, KP = 8;     // Fenster in m, 2.5 px je m, Pfeile 8 m je m/s
    function px(x){ return (x - X0) * M; } function py(y){ return (Y1 - y) * M; }
    var ziel = null, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    function rechne(vS, be, vF){
      var vq = vS * Math.sin(be * GRAD), vl = vF + vS * Math.cos(be * GRAD), t = BR / vq;
      return { vq: vq, vl: vl, t: t, d: vl * t, vu: Math.hypot(vq, vl) };
    }
    var sim = {
      zustand: function(){ var vS = B.wert('vS'), be = B.wert('be'), vF = B.wert('vF'), r = rechne(vS, be, vF);
        r.vS = vS; r.be = be; r.vF = vF; r.bewegt = B.bewegt; return r; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ ziel = null; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var vS = B.wert('vS'), be = B.wert('be'), vF = B.wert('vF'), r = rechne(vS, be, vF);
      B.anzeigen(); leeren(svg);
      el(svg, 'rect', { x: 0, y: py(BR), width: px(X1), height: py(0) - py(BR), 'class': 'wasser' });
      el(svg, 'line', { x1: 0, y1: py(0), x2: px(X1), y2: py(0), 'class': 'uferlinie' });
      el(svg, 'line', { x1: 0, y1: py(BR), x2: px(X1), y2: py(BR), 'class': 'uferlinie' });
      el(svg, 'text', { x: 4, y: py(0) + 13, 'class': 'bt-klein' }, 'Startufer');
      el(svg, 'text', { x: 4, y: py(BR) - 5, 'class': 'bt-klein' }, 'Zielufer');
      el(svg, 'text', { x: px(X1) - 4, y: py(BR) - 5, 'text-anchor': 'end', 'class': 'bt-klein' }, 'b = 40 m');
      [-28, 28, 52].forEach(function(x){ pfeil(svg, px(x), py(6), px(x + 8), py(6), 'pf-stroem', 5); });
      el(svg, 'text', { x: px(70), y: py(6) + 4, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Strömung');
      if (ziel != null){
        el(svg, 'rect', { x: px(ziel) - 4, y: py(BR) - 9, width: 8, height: 9, 'class': 'zielmarke' });
        el(svg, 'text', { x: px(ziel), y: py(BR) - 12, 'text-anchor': 'middle', 'class': 'ziel-text' }, 'Ziel');
      }
      // Bahn bis zum Zielufer, am Fenster abgeschnitten
      var xe = r.d, ye = BR, tt = 1;
      if (xe > X1) tt = (X1 - 0) / xe; else if (xe < X0) tt = X0 / xe;
      el(svg, 'line', { x1: px(0), y1: py(0), x2: px(xe * tt), y2: py(ye * tt), 'class': 'bahn-weg' });
      if (tt === 1){
        el(svg, 'circle', { cx: px(xe), cy: py(BR), r: 4, 'class': 'p-land' });
        var lt = 'Versatz ' + minus(sig(r.d)) + NB + 'm' + (r.d < -0.05 ? ' (stromaufwärts)' : '');
        el(svg, 'text', { x: px(xe) + (xe > 50 ? -7 : 7), y: py(BR) + 13, 'text-anchor': xe > 50 ? 'end' : 'start', 'class': 'bt-text' }, lt);
      }
      // Pfeile am Start: v_S, daran v_F, Summe v_Ufer
      var sx = vS * Math.cos(be * GRAD) * KP, sy = vS * Math.sin(be * GRAD) * KP;
      pfeil(svg, px(0), py(0), px(sx), py(sy), 'pf-v');
      pfeil(svg, px(sx), py(sy), px(sx + vF * KP), py(sy), 'pf-f');
      pfeil(svg, px(0), py(0), px(sx + vF * KP), py(sy), 'pf-r');
      el(svg, 'circle', { cx: px(0), cy: py(0), r: 3.5, 'class': 'knoten' });
      marke(svg, px(sx / 2) - 6, py(sy / 2), 'v', 'S', 'pf-text pf-v', 'end');
      if (vF > 0.1) marke(svg, px(sx + vF * KP / 2), py(sy) - 6, 'v', 'F', 'pf-text pf-f');
      marke(svg, px((sx + vF * KP) / 2) + 8, py(sy / 2) + 12, 'v', 'Ufer', 'pf-text pf-r', 'start');
      rolle(fig, 'formel').innerHTML =
        '<span>Querzeit: ' + v('t') + ' = ' + v('b') + ' / (' + v('v') + '<sub>S</sub> · sin ' + v('β') + ') = 40' + NB + 'm / (' + zahl(vS) + NB + 'm/s · sin ' + be + '°) ' + ist(r.t, sig(r.t)) + sig(r.t) + NB + 's</span>' +
        '<span>Versatz: ' + v('d') + ' = (' + v('v') + '<sub>F</sub> + ' + v('v') + '<sub>S</sub> · cos ' + v('β') + ') · ' + v('t') + ' = (' + zahl(vF) + NB + 'm/s + ' + zahl(vS) + NB + 'm/s · cos ' + be + '°) · ' + sig(r.t) + NB + 's ' + ist(r.d, sig(r.d)) + minus(sig(r.d)) + NB + 'm</span>' +
        '<span>|' + v('v') + '<sub>Ufer</sub>| = √((' + v('v') + '<sub>F</sub> + ' + v('v') + '<sub>S</sub> · cos ' + v('β') + ')² + (' + v('v') + '<sub>S</sub> · sin ' + v('β') + ')²) ' + ist(r.vu, sig(r.vu)) + sig(r.vu) + NB + 'm/s</span>' +
        (tt < 1 ? '<span class="sim-notiz">Der Landepunkt liegt ausserhalb des Bildes.</span>' : '');
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh an allen drei Reglern. Wovon hängt die Querzeit ab, wovon der Versatz? Notiere deine Antwort.', ok: function(s){ return s.bewegt.vS && s.bewegt.be && s.bewegt.vF; },
        vergleich: 'Die Querzeit hängt nur von der Quergeschwindigkeit \\(v_S \\cdot \\sin\\beta\\) ab — die Strömung ändert sie nicht. Der Versatz entsteht aus der Längsgeschwindigkeit \\(v_F + v_S \\cdot \\cos\\beta\\) während dieser Querzeit.' },
      { text: 'Ein Boot fährt mit \\(2.5\\;\\text{m/s}\\) quer zum Ufer, die Strömung hat \\(1.5\\;\\text{m/s}\\). Stelle ein und lies den Versatz ab.', ok: function(s){ return gl(s.vS, 2.5) && gl(s.be, 90) && gl(s.vF, 1.5); } },
      { text: 'Gleiches Boot, gleiche Strömung: Komm genau gegenüber an.', ok: function(s){ return gl(s.vS, 2.5) && gl(s.vF, 1.5) && Math.abs(s.d) < 0.5; } },
      { text: 'Ein Schwimmer mit \\(2\\;\\text{m/s}\\) schwimmt quer. Stelle eine Strömung ein, bei der er unter \\(45^\\circ\\) abgetrieben wird.', ok: function(s){ return gl(s.vS, 2) && gl(s.be, 90) && gl(s.vF, 2); } },
      { text: 'Strömung \\(1\\;\\text{m/s}\\): Die Überquerung soll \\(16\\;\\text{s}\\) dauern. Stelle ein.', ok: function(s){ return gl(s.vF, 1) && Math.abs(s.t - 16) < 0.05; } },
      { text: 'Lande bei der Markierung, \\(30\\;\\text{m}\\) flussabwärts.', setup: function(S){ ziel = 30; S.setze({ vS: 2, be: 90, vF: 0.5 }); }, ok: function(s){ return Math.abs(s.d - 30) < 1; } }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Gleichförmige Kreisbewegung ----------
     Rechnet wie Animation 5 der Themenseite (v grün tangential, a_z rot zur Mitte),
     aber mit der Umlaufzeit T als Regler statt ω — f und ω werden daraus berechnet —
     und ohne laufenden Punkt: Der Ort auf der Bahn wird mit dem Winkel φ eingestellt.
     Pfeile streng proportional: v 8 px je m/s, a_z 4 px je m/s² — mit T ≥ 3 s reicht a_z
     nie über die Mitte, und Pfeil samt Beschriftung bleiben im Bild (vorab mit python3 geprüft).
     Startwert = Clipbeispiel: r = 4 m, T = 4 s (v ≈ 6.28 m/s, a_z ≈ 9.87 m/s²); die Aufgaben
     nehmen andere Werte. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var CX = 150, CY = 140, S = 20, arten = {}, pruefen = function(){};
    var B = Bedienung(fig, zeichnen);
    hilfsschalter(fig);
    function rechne(r, T){ var w = 2 * Math.PI / T, vv = w * r; return { f: 1 / T, w: w, v: vv, az: w * w * r }; }
    var sim = {
      zustand: function(){ var r = B.wert('r'), T = B.wert('T'), q = rechne(r, T); q.r = r; q.T = T; q.bewegt = B.bewegt; q.arten = Object.keys(arten).length; return q; },
      zeichnen: zeichnen, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ arten = {}; B.zuruecksetzen(); }
    };
    function zeichnen(){
      var r = B.wert('r'), T = B.wert('T'), ph = B.wert('ph'), q = rechne(r, T);
      B.anzeigen(); leeren(svg);
      if (Math.abs(q.v - Math.PI) < 0.01) arten[r + '|' + T] = true;
      var R = r * S, c = Math.cos(ph * GRAD), s = Math.sin(ph * GRAD);
      var X = CX + R * c, Y = CY - R * s;
      el(svg, 'circle', { cx: CX, cy: CY, r: R, 'class': 'bahn-kreis' });
      el(svg, 'line', { x1: CX, y1: CY, x2: X, y2: Y, 'class': 'radius hilfslinie' });
      el(svg, 'text', { x: CX + R * 0.5 * c + s * 9, y: CY - R * 0.5 * s + c * 9 + 4, 'text-anchor': 'middle', 'class': 'hilf-text hilfslinie' }, 'r');
      el(svg, 'circle', { cx: CX, cy: CY, r: 3, 'class': 'knoten' });
      // Drehsinn gegen den Uhrzeigersinn: Tangente (−sin φ, cos φ)
      var lv = q.v * 8, la = q.az * 4;
      pfeil(svg, X, Y, X - s * lv, Y - c * lv, 'pf-v');
      if (la > 1) pfeil(svg, X, Y, X - c * la, Y + s * la, 'pf-a', 7);
      el(svg, 'circle', { cx: X, cy: Y, r: 5.5, 'class': 'koerper' });
      marke(svg, X - s * (lv + 11), Y - c * (lv + 11) + 4, 'v', '', 'pf-text pf-v');
      if (la > 10) marke(svg, X - c * la * 0.55 + s * 12, Y + s * la * 0.55 + c * 12 + 4, 'a', 'z', 'pf-text pf-a');
      rolle(fig, 'formel').innerHTML =
        '<span>' + v('f') + ' = 1 / ' + v('T') + ' = 1 / ' + zahl(T) + NB + 's ' + ist(q.f, sig(q.f)) + sig(q.f) + NB + 'Hz</span>' +
        '<span>' + v('ω') + ' = 2π / ' + v('T') + ' = 2π / ' + zahl(T) + NB + 's ' + ist(q.w, sig(q.w)) + sig(q.w) + NB + 'rad/s</span>' +
        '<span>' + v('v') + ' = ' + v('ω') + ' · ' + v('r') + ' = ' + sig(q.w) + NB + 'rad/s · ' + zahl(r) + NB + 'm ' + ist(q.v, sig(q.v)) + sig(q.v) + NB + 'm/s</span>' +
        '<span>' + v('a') + '<sub>z</sub> = ' + v('ω') + '² · ' + v('r') + ' = (' + sig(q.w) + NB + 'rad/s)² · ' + zahl(r) + NB + 'm ' + ist(q.az, sig(q.az)) + sig(q.az) + NB + 'm/s²</span>';
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Zieh am Winkel \\(\\varphi\\). Was bleibt am grünen Pfeil gleich, was ändert sich — und warum ist das eine Beschleunigung? Notiere deine Antwort.', ok: function(s){ return s.bewegt.ph; },
        vergleich: 'Die Länge des Pfeils \\(\\vec v\\) — der Betrag der Geschwindigkeit — bleibt gleich, seine Richtung ändert sich ständig: Er liegt immer tangential an der Bahn. Eine Änderung der Richtung ist eine Änderung des Vektors \\(\\vec v\\), also eine Beschleunigung. Sie zeigt zur Mitte: \\(\\vec a_z\\).' },
      { text: 'Ein Kinderkarussell dreht sich einmal in \\(8\\;\\text{s}\\), das Kind sitzt \\(2\\;\\text{m}\\) vom Mittelpunkt. Stelle ein und lies \\(v\\) ab.', ok: function(s){ return gl(s.r, 2) && gl(s.T, 8); } },
      { text: 'Stelle eine Rotationsfrequenz von \\(0.2\\;\\text{Hz}\\) ein.', ok: function(s){ return gl(s.T, 5); } },
      { text: 'Bei \\(T = 6\\;\\text{s}\\): Verdopple den Radius von \\(2\\;\\text{m}\\) auf \\(4\\;\\text{m}\\). Was macht \\(a_z\\)? Notiere.', setup: function(S){ S.setze({ r: 2, T: 6 }); }, ok: function(s){ return gl(s.r, 4) && gl(s.T, 6); },
        vergleich: '\\(a_z\\) verdoppelt sich, von \\(2.19\\) auf \\(4.39\\;\\text{m/s}^2\\): Bei gleichem \\(\\omega\\) ist \\(a_z = \\omega^2 \\cdot r\\) proportional zu \\(r\\).' },
      { text: 'Jetzt bei \\(4\\;\\text{m}\\) die Umlaufzeit halbieren. Um welchen Faktor wächst \\(a_z\\)? Notiere.', ok: function(s){ return gl(s.r, 4) && gl(s.T, 3); },
        vergleich: 'Vierfach, auf \\(17.5\\;\\text{m/s}^2\\): Halbe Umlaufzeit heisst doppeltes \\(\\omega\\), und \\(\\omega\\) steht in \\(a_z = \\omega^2 \\cdot r\\) im Quadrat.' },
      { text: 'Stelle \\(v \\approx 3.14\\;\\text{m/s}\\) ein — auf zwei verschiedene Arten.', ok: function(s){ return s.arten >= 2; } }
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


    var G = 9.81, GRAD = Math.PI / 180, PI2 = 2 * Math.PI;
    function kmh(x){ return '\\(' + ein(x, 'km/h') + '\\)'; }
    function ms(x){ return '\\(' + ein(x, 'm/s') + '\\)'; }
    function umr(k){ return '\\(' + ein(k, 'km/h') + ' = \\dfrac{' + tz(k) + '}{3.6}\\;\\text{m/s} ' + erg(k / 3.6, 'm/s') + '\\)'; }

    var TYPEN = {
      /* ----- Kapitel 1 ----- */
      'ort': { felder: ['s'], muster: '<i>s</i> = {s} m',
        neu: function(){
          var s0, kh, vk, vv, t;
          do {
            s0 = zufall([0, 10, 25, 40, 120]); kh = Math.random() < 0.4;
            vk = kh ? zufall([18, 36, 54, 72, 90]) : zufall([2, 3.5, 4, 6, 8, 12]); vv = kh ? vk / 3.6 : vk; t = zufall([5, 8, 12, 15, 20, 30]);
          } while ((s0 === 20 && vv === 5 && t === 8) || (s0 === 20 && vv === 15 && t === 4)   // Clip, Themenseite
                   || (s0 === 10 && vv === 4 && t === 5)                            // Kontrollclip, Frage 3
                   || (s0 && nah(s0 + vv / t, vv * t, 0.02)));                     // zwei Fehlermuster, eine Zahl
          return { s: s0 + vv * t, s0: s0, kh: kh, vk: vk, v: vv, t: t,
            text: (kh ? 'Ein Auto' : 'Ein Velo') + ' startet bei \\(s_0 = ' + ein(s0, 'm') + '\\) und fährt gleichförmig mit \\(v = ' + ein(vk, kh ? 'km/h' : 'm/s') + '\\) weiter. Wo ist es nach \\(t = ' + ein(t, 's') + '\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.s, A.s)) return null;
          if (A.kh && nah(e.s, A.s0 + A.vk * A.t)) return 'Erst in m/s umrechnen: ' + umr(A.vk) + '.';
          if (A.kh && nah(e.s, A.s0 + A.vk * 3.6 * A.t)) return 'Von km/h in m/s teilt man durch 3.6, nicht mal.';
          if (A.s0 && nah(e.s, A.v * A.t)) return 'Der Startort fehlt: \\(s = s_0 + v \\cdot t\\).';
          if (nah(e.s, A.s0 + A.v / A.t) || nah(e.s, A.s0 + A.t / A.v)) return 'Geschwindigkeit <em>mal</em> Zeit gibt den Weg, nicht geteilt.';
          return '\\(s = s_0 + v \\cdot t\\) mit \\(v\\) in m/s.'; },
        fehler: function(A){
          var l = [[{ s: String(A.s0 + A.v / A.t) }, 'mal'], [{ s: String(A.s * 1.05) }, null]];
          if (A.kh) l.push([{ s: String(A.s0 + A.vk * A.t) }, 'umrechnen']);
          if (A.s0) l.push([{ s: String(A.v * A.t) }, 'Startort']);
          return l; },
        loesung: function(A){ return (A.kh ? 'v = \\dfrac{' + tz(A.vk) + '}{3.6}\\;\\text{m/s} = ' + ein(A.v, 'm/s') + ',\\quad ' : '') + 's = s_0 + v \\cdot t = ' + ein(A.s0, 'm') + ' + ' + ein(A.v, 'm/s') + ' \\cdot ' + ein(A.t, 's') + ' = ' + ein(A.s, 'm'); } },
      'mittel': { felder: ['v'], muster: function(A){ return 'mittlere <i>v</i> = {v} ' + (A.kh ? 'km/h' : 'm/s'); },
        neu: function(){
          if (Math.random() < 0.5){
            var s, tm;
            do { s = zufall([3, 6, 12, 18, 45, 150]); tm = zufall([10, 15, 20, 30, 40, 45, 90]); } while ((s === 12 && tm === 40) || s === tm || s / tm * 60 > 130 || s / tm * 60 < 15);   // Aufgabe 1b; s = t: Kehrwert gleich; Fahrt 15 bis 130 km/h
            return { kh: true, s: s, t: tm, v: s / (tm / 60),
              text: 'Eine Fahrt über \\(' + ein(s, 'km') + '\\) dauert mit allen Halten \\(' + ein(tm, 'min') + '\\). Wie gross ist die mittlere Geschwindigkeit, in km/h?' };
          }
          var sm = zufall([100, 200, 400, 800, 1500]), ts = zufall([12.5, 25, 50, 80, 125, 250]);
          if (sm / ts > 7.5 || sm / ts < 2.5) return this.neu();   // Läuferin: 2.5 bis 7.5 m/s
          return { kh: false, s: sm, t: ts, v: sm / ts,
            text: 'Eine Läuferin legt \\(' + ein(sm, 'm') + '\\) in \\(' + ein(ts, 's') + '\\) zurück. Wie gross ist ihre mittlere Geschwindigkeit, in m/s?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (A.kh && nah(e.v, A.s / A.t)) return 'Minuten in Stunden: \\(' + ein(A.t, 'min') + ' = \\tfrac{' + A.t + '}{60}\\;\\text{h}\\).';
          if (nah(e.v, A.t / A.s)) return 'Umgekehrt: Strecke durch Zeit, \\(\\bar v = \\dfrac{\\Delta s}{\\Delta t}\\).';
          if (nah(e.v, A.s * A.t)) return 'Geschwindigkeit ist Strecke <em>pro</em> Zeit, nicht mal.';
          if (A.kh && faktor(e.v, A.v, 1 / 3.6)) return 'Das ist der Wert in m/s. Gefragt ist km/h.';
          if (!A.kh && faktor(e.v, A.v, 3.6)) return 'Das ist der Wert in km/h. Gefragt ist m/s.';
          return '\\(\\bar v = \\dfrac{\\Delta s}{\\Delta t}\\) — ganze Strecke durch ganze Zeit.'; },
        fehler: function(A){
          var l = [[{ v: String(A.t / A.s) }, 'Umgekehrt'], [{ v: String(A.s * A.t) }, 'pro']];
          if (A.kh) l.push([{ v: String(A.s / A.t) }, 'Stunden'], [{ v: String(A.v / 3.6) }, 'm/s']);
          else l.push([{ v: String(A.v * 3.6) }, 'km/h']);
          return l; },
        loesung: function(A){ return A.kh ? '\\bar v = \\dfrac{\\Delta s}{\\Delta t} = \\dfrac{' + ein(A.s, 'km') + '}{\\tfrac{' + A.t + '}{60}\\;\\text{h}} ' + erg(A.v, 'km/h')
                                           : '\\bar v = \\dfrac{\\Delta s}{\\Delta t} = \\dfrac{' + ein(A.s, 'm') + '}{' + ein(A.t, 's') + '} ' + erg(A.v, 'm/s'); } },
      'einholen': { felder: ['t', 's'], muster: '<i>t</i> = {t} s; <i>s</i> = {s} m',
        neu: function(){
          var d, vB, vA;
          do { d = zufall([10, 15, 24, 30, 45, 60]); vB = zufall([2, 3, 4, 5, 8]); vA = vB + zufall([1, 1.5, 2, 3, 4]); }
          while ((d === 30 && vA === 6 && vB === 4) || (d === 20 && vA === 5 && vB === 3));   // Themenseite, Simulation 1
          var t = d / (vA - vB);
          return { t: t, s: vA * t, d: d, vA: vA, vB: vB,
            text: 'A startet bei \\(0\\;\\text{m}\\) mit \\(' + ein(vA, 'm/s') + '\\). B startet gleichzeitig \\(' + ein(d, 'm') + '\\) weiter vorn mit \\(' + ein(vB, 'm/s') + '\\) in dieselbe Richtung. Wann holt A den B ein, und wo (gemessen ab dem Start von A)?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t) && nah(e.s, A.s)) return null;
          var r = [];
          if (!nah(e.t, A.t)){
            if (nah(e.t, A.d / (A.vA + A.vB))) r.push('Beide fahren in dieselbe Richtung: A holt nur mit dem Unterschied der Geschwindigkeiten auf, \\(v_A - v_B\\).');
            else if (nah(e.t, A.d / A.vA)) r.push('B fährt weiter, während A aufholt. Ansatz: Beim Einholen sind beide am gleichen Ort, \\(v_A \\cdot t = d + v_B \\cdot t\\).');
            else r.push('Ansatz: \\(v_A \\cdot t = d + v_B \\cdot t\\), nach \\(t\\) auflösen.');
          }
          if (!nah(e.s, A.s) && !(!nah(e.t, A.t) && nah(e.s, A.vA * e.t))){
            if (nah(e.s, A.vB * A.t)) r.push('Das ist der Weg von B. Der Ort zählt ab dem Start von A: \\(s = v_A \\cdot t\\).');
            else r.push('Ort: \\(s = v_A \\cdot t\\) mit der Einholzeit.');
          }
          return r.join(' '); },
        fehler: function(A){ var t2 = A.d / (A.vA + A.vB);
          return [[{ t: String(t2), s: String(A.vA * t2) }, 'Unterschied'], [{ t: String(A.d / A.vA), s: String(A.d) }, 'gleichen Ort'], [{ t: String(A.t), s: String(A.vB * A.t) }, 'Weg von B']]; },
        loesung: function(A){ return 'v_A \\cdot t = d + v_B \\cdot t,\\quad t = \\dfrac{d}{v_A - v_B} = \\dfrac{' + ein(A.d, 'm') + '}{' + ein(A.vA, 'm/s') + ' - ' + ein(A.vB, 'm/s') + '} ' + erg(A.t, 's') + ',\\quad s = v_A \\cdot t = ' + ein(A.vA, 'm/s') + ' \\cdot ' + ein(+A.t.toPrecision(4), 's') + ' ' + erg(A.s, 'm'); } },

      /* ----- Kapitel 2 ----- */
      'beschl': { felder: ['a'], muster: '<i>a</i> = {a} m/s²',
        neu: function(){
          var kh, v0, v1, dt, br, tmp;
          do {
            kh = Math.random() < 0.5; br = Math.random() < 0.4;
            if (kh){ v0 = zufall([0, 18, 36]); v1 = zufall([54, 72, 90, 108]); } else { v0 = zufall([0, 2, 5, 10]); v1 = zufall([12, 15, 20, 25, 30]); }
            if (br){ tmp = v0; v0 = v1; v1 = tmp; }
            dt = zufall([3, 4, 5, 6, 8, 10, 12]);
          } while ((!kh && v0 === 10 && v1 === 30 && dt === 4) || (!kh && v0 === 0 && v1 === 20 && dt === 8) || (kh && v0 === 0 && v1 === 36 && dt === 12)
                   || Math.abs(Math.abs((v1 - v0) * (kh ? 1 / 3.6 : 1) / dt) - 1) < 0.02                       // |a| = 1: Kehrwert gleich
                   || (v0 && nah(v1 * (kh ? 1 / 3.6 : 1) / dt, dt / ((v1 - v0) * (kh ? 1 / 3.6 : 1)), 0.02)));
          var f = kh ? 1 / 3.6 : 1, a = (v1 - v0) * f / dt;
          return { a: a, kh: kh, br: br, v0: v0, v1: v1, dt: dt, f: f,
            text: 'Ein Fahrzeug wird in \\(' + ein(dt, 's') + '\\) gleichmässig von \\(' + ein(v0, kh ? 'km/h' : 'm/s') + '\\) auf \\(' + ein(v1, kh ? 'km/h' : 'm/s') + '\\) ' + (br ? 'langsamer' : 'schneller') + '. Wie gross ist die Beschleunigung (mit Vorzeichen)?' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a)) return null;
          if (A.kh && nah(e.a, (A.v1 - A.v0) / A.dt)) return 'km/h zuerst in m/s umrechnen: durch 3.6.';
          if (nah(e.a, -A.a)) return A.br ? 'Vorzeichen: \\(\\Delta v = v - v_0\\). Wird das Fahrzeug langsamer, ist \\(\\Delta v\\) negativ und damit auch \\(a\\).' : 'Vorzeichen: \\(\\Delta v = v - v_0\\). Wird das Fahrzeug schneller, ist \\(\\Delta v\\) positiv und damit auch \\(a\\).';
          if (A.v0 && nah(e.a, A.v1 * A.f / A.dt)) return 'Die Beschleunigung ist die <em>Änderung</em> der Geschwindigkeit: \\(\\Delta v = v - v_0\\), nicht die Endgeschwindigkeit.';
          if (nah(e.a, A.dt / ((A.v1 - A.v0) * A.f))) return 'Umgekehrt: \\(a = \\dfrac{\\Delta v}{\\Delta t}\\).';
          return '\\(a = \\dfrac{\\Delta v}{\\Delta t} = \\dfrac{v - v_0}{\\Delta t}\\) mit \\(v\\) in m/s.'; },
        fehler: function(A){
          var l = [[{ a: String(A.dt / ((A.v1 - A.v0) * A.f)) }, 'Umgekehrt']];
          if (A.kh) l.push([{ a: String((A.v1 - A.v0) / A.dt) }, 'km/h']);
          if (A.br) l.push([{ a: String(-A.a) }, 'Vorzeichen']);
          if (A.v0 && A.v1 && !nah(A.v1 * A.f / A.dt, -A.a)) l.push([{ a: String(A.v1 * A.f / A.dt) }, 'Änderung']);
          return l; },
        loesung: function(A){ var v0 = A.v0 * A.f, v1 = A.v1 * A.f;
          return (A.kh ? ein(A.v0, 'km/h') + ' ' + erg(v0, 'm/s') + ',\\; ' + ein(A.v1, 'km/h') + ' ' + erg(v1, 'm/s') + ',\\quad ' : '') + 'a = \\dfrac{v - v_0}{\\Delta t} = \\dfrac{' + ein(+v1.toPrecision(4), 'm/s') + ' - ' + ein(+v0.toPrecision(4), 'm/s') + '}{' + ein(A.dt, 's') + '} ' + erg(A.a, 'm/s^2').replace('\\text{m/s^2}', '\\text{m/s}^2'); } },
      'endwerte': { felder: ['v', 's'], muster: '<i>v</i> = {v} m/s; <i>s</i> = {s} m',
        neu: function(){
          var v0, a, t;
          do {
            v0 = zufall([0, 2, 4, 5, 8, 10, 16, 20]); t = zufall([2, 4, 5, 6, 8, 10]);
            a = v0 >= 10 && Math.random() < 0.4 ? -zufall([1, 1.5, 2]) : zufall([0.5, 1.5, 2, 2.5, 3, 4]);
          } while (v0 + a * t <= 0 || (v0 === 0 && a === 2 && t === 5) || (v0 === 4 && a === 2 && t === 6) || (v0 === 10 && a === 2 && t === 5) || (v0 === 0 && a === 2.5 && t === 8) || (v0 === 0 && a === 1.5 && t === 6)
                   || (v0 === 3 && a === 1.5 && t === 6) || (v0 === 2 && a === 2 && t === 6) || (v0 === 0 && a === 2 && t === 10));   // Kontrollclip, Aufgabe 2b, Fehlerkasten; v = 0 aus Leiste 3 und 4 durch «<= 0»
          return { v: v0 + a * t, s: v0 * t + 0.5 * a * t * t, v0: v0, a: a, t: t,
            text: 'Ein Körper hat \\(v_0 = ' + ein(v0, 'm/s') + '\\) und wird gleichmässig mit \\(a = ' + tz(a) + '\\;\\text{m/s}^2\\) ' + (a < 0 ? 'gebremst' : 'beschleunigt') + '. Geschwindigkeit und zurückgelegter Weg nach \\(t = ' + ein(t, 's') + '\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v) && nah(e.s, A.s)) return null;
          var r = [];
          if (!nah(e.v, A.v)){
            if (A.v0 && nah(e.v, A.a * A.t)) r.push('Die Anfangsgeschwindigkeit fehlt: \\(v = v_0 + a \\cdot t\\).');
            else r.push('\\(v = v_0 + a \\cdot t\\).');
          }
          if (!nah(e.s, A.s)){
            if (nah(e.s, A.v0 * A.t + A.a * A.t * A.t)) r.push('Der Faktor \\(\\tfrac12\\) fehlt (oder du hast mit der Endgeschwindigkeit \\(v \\cdot t\\) gerechnet): Die Fläche unter der \\(v\\)-\\(t\\)-Geraden ist ein Trapez, \\(s = v_0 \\cdot t + \\tfrac12 \\cdot a \\cdot t^2\\).');
            else if (A.v0 && nah(e.s, 0.5 * A.a * A.t * A.t)) r.push('Auch \\(v_0 \\cdot t\\) gehört dazu: \\(s = v_0 \\cdot t + \\tfrac12 \\cdot a \\cdot t^2\\).');
            else if (nah(e.s, A.v0 * A.t + 0.5 * A.a * A.t)) r.push('Die Zeit gehört im zweiten Glied ins Quadrat: \\(\\tfrac12 \\cdot a \\cdot t^2\\).');
            else r.push('\\(s = v_0 \\cdot t + \\tfrac12 \\cdot a \\cdot t^2\\).');
          }
          return r.join(' '); },
        fehler: function(A){
          var l = [[{ v: String(A.v), s: String(A.v0 * A.t + A.a * A.t * A.t) }, 'Faktor']];
          if (A.v0) l.push([{ v: String(A.a * A.t), s: String(A.s) }, 'Anfangsgeschwindigkeit'], [{ v: String(A.v), s: String(0.5 * A.a * A.t * A.t) }, 'Auch']);
          return l; },
        loesung: function(A){ return 'v = v_0 + a \\cdot t = ' + ein(A.v0, 'm/s') + ' + (' + tz(A.a) + '\\;\\text{m/s}^2) \\cdot ' + ein(A.t, 's') + ' = ' + ein(A.v, 'm/s') + ',\\quad s = v_0 \\cdot t + \\tfrac12 \\cdot a \\cdot t^2 = ' + ein(A.v0, 'm/s') + ' \\cdot ' + ein(A.t, 's') + ' + \\tfrac12 \\cdot (' + tz(A.a) + '\\;\\text{m/s}^2) \\cdot (' + ein(A.t, 's') + ')^2 ' + erg(A.s, 'm'); } },
      'bremsweg': { felder: ['s'], muster: '<i>s</i> = {s} m',
        neu: function(){
          var vk, a;
          do { vk = zufall([30, 50, 60, 80, 100, 120]); a = zufall([4, 5, 6, 7, 8]); } while ((vk === 50 && a === 5) || (vk === 90 && a === 6));   // Themenseite A3, Aufgabe 2c
          var v0 = vk / 3.6;
          return { s: v0 * v0 / (2 * a), vk: vk, v0: v0, a: a,
            text: 'Ein Auto fährt mit \\(' + ein(vk, 'km/h') + '\\) und bremst gleichmässig mit \\(' + tz(a) + '\\;\\text{m/s}^2\\) bis zum Stillstand. Wie lang ist der Bremsweg?' }; },
        pruefen: function(A, e){
          if (nah(e.s, A.s)) return null;
          if (nah(e.s, A.vk * A.vk / (2 * A.a))) return 'Erst in m/s umrechnen: ' + umr(A.vk) + '.';
          if (nah(e.s, A.v0 * A.v0 / A.a)) return 'Der Faktor 2 im Nenner fehlt: \\(s = \\dfrac{v_0^2}{2 \\cdot |a|}\\).';
          if (nah(e.s, A.v0 / (2 * A.a))) return 'Die Geschwindigkeit steht im Quadrat: \\(s = \\dfrac{v_0^2}{2 \\cdot |a|}\\).';
          if (nah(e.s, -A.s)) return 'Ein Bremsweg ist positiv. Mit \\(a\\) negativ: \\(s = -\\dfrac{v_0^2}{2a}\\).';
          return 'Aus \\(v^2 = v_0^2 + 2 \\cdot a \\cdot s\\) mit \\(v = 0\\): \\(s = \\dfrac{v_0^2}{2 \\cdot |a|}\\).'; },
        fehler: function(A){ return [[{ s: String(A.vk * A.vk / (2 * A.a)) }, 'umrechnen'], [{ s: String(A.v0 * A.v0 / A.a) }, 'Faktor 2'], [{ s: String(A.v0 / (2 * A.a)) }, 'Quadrat']]; },
        loesung: function(A){ return 'v_0 = \\dfrac{' + tz(A.vk) + '}{3.6}\\;\\text{m/s} ' + erg(A.v0, 'm/s') + ',\\quad s = \\dfrac{v_0^2}{2 \\cdot |a|} = \\dfrac{(' + ein(+A.v0.toPrecision(4), 'm/s') + ')^2}{2 \\cdot ' + tz(A.a) + '\\;\\text{m/s}^2} ' + erg(A.s, 'm'); } },

      /* ----- Kapitel 4: Fall und Wurf ----- */
      'fall': { felder: ['x', 'v'], muster: function(A){ return (A.art === 'h' ? '<i>t</i> = {x} s' : '<i>h</i> = {x} m') + '; <i>v</i> = {v} m/s'; },
        neu: function(){
          if (Math.random() < 0.5){
            var h = zufall([5, 10, 15, 25, 35, 60, 80]), t = Math.sqrt(2 * h / G);   // nicht 20 (Clip), 30 (Simulation)
            return { art: 'h', x: t, v: G * t, h: h, t: t, text: 'Ein Stein fällt aus \\(' + ein(h, 'm') + '\\) Höhe frei (ohne Luftwiderstand). Wie lange fällt er, und wie schnell ist er beim Aufprall?' };
          }
          var t2 = zufall([0.8, 1.5, 2.5, 3.5, 4]);   // nicht 1 s (t² = t) und nicht 0.5 s (g·t² = ½·g·t)
          return { art: 't', x: 0.5 * G * t2 * t2, v: G * t2, t: t2, h: 0.5 * G * t2 * t2, text: 'Ein Stein fällt \\(' + ein(t2, 's') + '\\) lang frei (ohne Luftwiderstand). Aus welcher Höhe fiel er, und wie schnell ist er dann?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x) && nah(e.v, A.v)) return null;
          var r = [];
          if (A.art === 'h'){
            if (!nah(e.x, A.t)){
              if (nah(e.x, 2 * A.h / G)) r.push('Die Wurzel fehlt: \\(t = \\sqrt{\\dfrac{2h}{g}}\\).');
              else if (nah(e.x, Math.sqrt(A.h / G))) r.push('Der Faktor 2 fehlt: Aus \\(h = \\tfrac12 \\cdot g \\cdot t^2\\) folgt \\(t^2 = \\dfrac{2h}{g}\\).');
              else if (nah(e.x, Math.sqrt(2 * A.h * G))) r.push('Durch \\(g\\) teilen, nicht malnehmen: \\(t = \\sqrt{\\dfrac{2h}{g}}\\).');
              else r.push('\\(t = \\sqrt{\\dfrac{2h}{g}}\\).');
            }
            if (!nah(e.v, A.v) && !(!nah(e.x, A.t) && nah(e.v, G * e.x))){
              if (nah(e.v, A.h / A.t)) r.push('Das ist die mittlere Geschwindigkeit. Beim Aufprall ist \\(v = g \\cdot t\\) — doppelt so viel.');
              else r.push('\\(v = g \\cdot t\\).');
            }
          } else {
            if (!nah(e.x, A.h)){
              if (nah(e.x, G * A.t * A.t)) r.push('Der Faktor \\(\\tfrac12\\) fehlt: \\(h = \\tfrac12 \\cdot g \\cdot t^2\\).');
              else if (nah(e.x, 0.5 * G * A.t)) r.push('Die Zeit steht im Quadrat: \\(h = \\tfrac12 \\cdot g \\cdot t^2\\).');
              else r.push('\\(h = \\tfrac12 \\cdot g \\cdot t^2\\).');
            }
            if (!nah(e.v, A.v)){
              if (nah(e.v, G * A.t * A.t)) r.push('Die Geschwindigkeit wächst linear: \\(v = g \\cdot t\\), ohne Quadrat.');
              else r.push('\\(v = g \\cdot t\\).');
            }
          }
          return r.join(' '); },
        fehler: function(A){
          if (A.art === 'h') return [[{ x: String(2 * A.h / G), v: String(2 * A.h) }, 'Wurzel'], [{ x: String(Math.sqrt(A.h / G)), v: String(G * Math.sqrt(A.h / G)) }, 'Faktor 2'], [{ x: String(A.t), v: String(A.h / A.t) }, 'mittlere']];
          return [[{ x: String(G * A.t * A.t), v: String(A.v) }, 'Faktor'], [{ x: String(0.5 * G * A.t), v: String(A.v) }, 'Quadrat'], [{ x: String(A.h), v: String(G * A.t * A.t) }, 'linear']]; },
        loesung: function(A){ return A.art === 'h'
          ? 't = \\sqrt{\\dfrac{2h}{g}} = \\sqrt{\\dfrac{2 \\cdot ' + ein(A.h, 'm') + '}{9.81\\;\\text{m/s}^2}} ' + erg(A.t, 's') + ',\\quad v = g \\cdot t = 9.81\\;\\text{m/s}^2 \\cdot ' + ein(+A.t.toPrecision(4), 's') + ' ' + erg(A.v, 'm/s')
          : 'h = \\tfrac12 \\cdot g \\cdot t^2 = \\tfrac12 \\cdot 9.81\\;\\text{m/s}^2 \\cdot (' + ein(A.t, 's') + ')^2 ' + erg(A.h, 'm') + ',\\quad v = g \\cdot t = 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.t, 's') + ' ' + erg(A.v, 'm/s'); } },
      'senkrecht': { felder: ['a', 'b'], muster: function(A){ return A.art === 'oben' ? '<i>t</i><sub>S</sub> = {a} s; <i>h</i><sub>max</sub> = {b} m' : '<i>v</i> = {a} m/s; <i>h</i> = {b} m'; },
        neu: function(){
          if (Math.random() < 0.5){
            var v0 = zufall([6, 8, 14, 20, 25]);   // nicht 10 (Kontrollfrage), 12 (Clip), 15 (Simulation), 18 (Aufgabe 4b)
            return { art: 'oben', a: v0 / G, b: v0 * v0 / (2 * G), v0: v0,
              text: 'Ein Ball wird mit \\(' + ein(v0, 'm/s') + '\\) senkrecht nach oben geworfen (ohne Luftwiderstand). Wie lange steigt er, und wie hoch kommt er über die Abwurfstelle?' };
          }
          var u0 = zufall([2, 3, 6, 8]), t = zufall([1.5, 2, 2.5, 3]);   // nicht t = 1 s: t² = t
          return { art: 'unten', a: u0 + G * t, b: u0 * t + 0.5 * G * t * t, v0: u0, t: t,
            text: 'Ein Stein wird von einer Brücke mit \\(' + ein(u0, 'm/s') + '\\) senkrecht nach unten geworfen (ohne Luftwiderstand). Wie schnell ist er nach \\(' + ein(t, 's') + '\\), und wie weit ist er gefallen?' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a) && nah(e.b, A.b)) return null;
          var r = [];
          if (A.art === 'oben'){
            if (!nah(e.a, A.a)){
              if (nah(e.a, A.v0 * G)) r.push('Durch \\(g\\) teilen: \\(t_S = \\dfrac{v_0}{g}\\).');
              else r.push('Oben ist \\(v = 0\\): Aus \\(v = v_0 - g \\cdot t\\) folgt \\(t_S = \\dfrac{v_0}{g}\\).');
            }
            if (!nah(e.b, A.b) && !(!nah(e.a, A.a) && nah(e.b, A.v0 * e.a - 0.5 * G * e.a * e.a))){
              if (nah(e.b, A.v0 * A.v0 / G)) r.push('Der Faktor 2 fehlt: \\(h_\\text{max} = \\dfrac{v_0^2}{2 \\cdot g}\\).');
              else if (nah(e.b, A.v0 / (2 * G))) r.push('Die Geschwindigkeit steht im Quadrat: \\(h_\\text{max} = \\dfrac{v_0^2}{2 \\cdot g}\\).');
              else r.push('\\(h_\\text{max} = \\dfrac{v_0^2}{2 \\cdot g}\\) oder \\(v_0 \\cdot t_S - \\tfrac12 \\cdot g \\cdot t_S^2\\).');
            }
          } else {
            if (!nah(e.a, A.a)){
              if (nah(e.a, G * A.t)) r.push('Die Anfangsgeschwindigkeit fehlt: \\(v = v_0 + g \\cdot t\\).');
              else r.push('\\(v = v_0 + g \\cdot t\\).');
            }
            if (!nah(e.b, A.b)){
              if (nah(e.b, 0.5 * G * A.t * A.t)) r.push('Der Weg aus der Anfangsgeschwindigkeit fehlt: \\(h = v_0 \\cdot t + \\tfrac12 \\cdot g \\cdot t^2\\).');
              else if (nah(e.b, A.v0 * A.t + G * A.t * A.t)) r.push('Der Faktor \\(\\tfrac12\\) fehlt: \\(h = v_0 \\cdot t + \\tfrac12 \\cdot g \\cdot t^2\\).');
              else r.push('\\(h = v_0 \\cdot t + \\tfrac12 \\cdot g \\cdot t^2\\).');
            }
          }
          return r.join(' '); },
        fehler: function(A){
          if (A.art === 'oben') return [[{ a: String(A.v0 * G), b: String(A.b) }, 'teilen'], [{ a: String(A.a), b: String(A.v0 * A.v0 / G) }, 'Faktor 2'], [{ a: String(A.a), b: String(A.v0 / (2 * G)) }, 'Quadrat']];
          return [[{ a: String(G * A.t), b: String(A.b) }, 'Anfangsgeschwindigkeit'], [{ a: String(A.a), b: String(0.5 * G * A.t * A.t) }, 'Anfangsgeschwindigkeit'], [{ a: String(A.a), b: String(A.v0 * A.t + G * A.t * A.t) }, 'Faktor']]; },
        loesung: function(A){ return A.art === 'oben'
          ? 't_S = \\dfrac{v_0}{g} = \\dfrac{' + ein(A.v0, 'm/s') + '}{9.81\\;\\text{m/s}^2} ' + erg(A.a, 's') + ',\\quad h_\\text{max} = \\dfrac{v_0^2}{2 \\cdot g} = \\dfrac{(' + ein(A.v0, 'm/s') + ')^2}{2 \\cdot 9.81\\;\\text{m/s}^2} ' + erg(A.b, 'm')
          : 'v = v_0 + g \\cdot t = ' + ein(A.v0, 'm/s') + ' + 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.t, 's') + ' ' + erg(A.a, 'm/s') + ',\\quad h = v_0 \\cdot t + \\tfrac12 \\cdot g \\cdot t^2 = ' + ein(A.v0, 'm/s') + ' \\cdot ' + ein(A.t, 's') + ' + \\tfrac12 \\cdot 9.81\\;\\text{m/s}^2 \\cdot (' + ein(A.t, 's') + ')^2 ' + erg(A.b, 'm'); } },
      'waagrecht': { felder: ['t', 'x'], muster: '<i>t</i> = {t} s; <i>x</i> = {x} m',
        neu: function(){
          var h, v0;
          do { h = zufall([1.2, 2, 3, 10, 20, 45]); v0 = zufall([2, 3, 5, 8, 12, 15]); } while ((h === 20 && v0 === 8) || (h === 45 && v0 === 12));   // Clip, Gesamttest
          var t = Math.sqrt(2 * h / G);
          return { t: t, x: v0 * t, h: h, v0: v0,
            text: 'Ein Ball wird aus \\(' + ein(h, 'm') + '\\) Höhe waagrecht mit \\(' + ein(v0, 'm/s') + '\\) abgeworfen. Wie lange fliegt er, und wie weit (waagrecht) landet er vom Abwurfpunkt?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t) && nah(e.x, A.x)) return null;
          var r = [];
          if (!nah(e.t, A.t)){
            if (nah(e.t, 2 * A.h / G)) r.push('Die Wurzel fehlt: \\(t = \\sqrt{\\dfrac{2h}{g}}\\).');
            else if (nah(e.t, A.h / A.v0)) r.push('Die Flugzeit hängt nur von der Höhe ab, nicht von \\(v_0\\): Senkrecht fällt der Ball wie im freien Fall, \\(t = \\sqrt{\\dfrac{2h}{g}}\\).');
            else r.push('Senkrecht wie im freien Fall: \\(t = \\sqrt{\\dfrac{2h}{g}}\\).');
          }
          if (!nah(e.x, A.x) && !(!nah(e.t, A.t) && nah(e.x, A.v0 * e.t))) r.push('Waagrecht gleichförmig: \\(x = v_0 \\cdot t\\).');
          return r.join(' '); },
        fehler: function(A){ var t2 = 2 * A.h / G;
          return [[{ t: String(t2), x: String(A.v0 * t2) }, 'Wurzel'], [{ t: String(A.h / A.v0), x: String(A.h) }, 'Höhe'], [{ t: String(A.t), x: String(A.x * 1.2) }, 'gleichförmig']]; },
        loesung: function(A){ return 't = \\sqrt{\\dfrac{2h}{g}} = \\sqrt{\\dfrac{2 \\cdot ' + ein(A.h, 'm') + '}{9.81\\;\\text{m/s}^2}} ' + erg(A.t, 's') + ',\\quad x = v_0 \\cdot t = ' + ein(A.v0, 'm/s') + ' \\cdot ' + ein(+A.t.toPrecision(4), 's') + ' ' + erg(A.x, 'm'); } },
      'schief': { felder: ['t', 'x'], muster: '<i>t</i><sub>F</sub> = {t} s; <i>s</i><sub>x</sub> = {x} m',
        neu: function(){
          var v0, al, ok;
          do {
            v0 = zufall([8, 10, 12, 15, 18, 20, 25]); al = zufall([15, 20, 30, 35, 40, 50, 55, 60, 70]);
            var t = 2 * v0 * Math.sin(al * GRAD) / G, tr = 2 * v0 * Math.sin(al) / G, tc = 2 * v0 * Math.cos(al * GRAD) / G;
            var x = v0 * v0 * Math.sin(2 * al * GRAD) / G, xr = v0 * v0 * Math.sin(2 * al) / G, xs = v0 * v0 * Math.sin(al * GRAD) / G;
            ok = !nah(tr, t, 0.02) && !nah(tc, t, 0.02) && !nah(tr, t / 2, 0.02) && !nah(tc, t / 2, 0.02) && !nah(xr, x, 0.02) && !nah(xs, x, 0.02) && !nah(xr, xs, 0.02);
          } while (!ok || (v0 === 15 && al === 45) || (v0 === 18 && al === 30) || (v0 === 14 && al === 50) || (v0 === 13 && al === 40));
          var tF = 2 * v0 * Math.sin(al * GRAD) / G;
          return { t: tF, x: v0 * v0 * Math.sin(2 * al * GRAD) / G, v0: v0, al: al,
            text: 'Ein Ball wird vom Boden mit \\(' + ein(v0, 'm/s') + '\\) unter \\(' + al + '^\\circ\\) abgeworfen und landet wieder auf dem Boden. Flugzeit und Wurfweite? (ohne Luftwiderstand)' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t) && nah(e.x, A.x)) return null;
          var r = [], s = Math.sin(A.al * GRAD), c = Math.cos(A.al * GRAD);
          if (nah(e.t, 2 * A.v0 * Math.sin(A.al) / G) || nah(e.x, A.v0 * A.v0 * Math.sin(2 * A.al) / G)) return 'Der Taschenrechner steht im Bogenmass (RAD). Stelle ihn auf Grad (DEG).';
          if (!nah(e.t, A.t)){
            if (nah(e.t, A.t / 2)) r.push('Das ist die Zeit bis zum höchsten Punkt. Hinauf und wieder hinunter dauert doppelt so lang: \\(t_F = \\dfrac{2 \\cdot v_0 \\cdot \\sin\\alpha}{g}\\).');
            else if (nah(e.t, 2 * A.v0 * c / G)) r.push('Für die Flugzeit zählt die senkrechte Komponente \\(v_0 \\cdot \\sin\\alpha\\), nicht \\(v_0 \\cdot \\cos\\alpha\\).');
            else r.push('\\(t_F = \\dfrac{2 \\cdot v_0 \\cdot \\sin\\alpha}{g}\\) — aus \\(y(t_F) = 0\\).');
          }
          if (!nah(e.x, A.x) && !(!nah(e.t, A.t) && nah(e.x, A.v0 * c * e.t))){
            if (nah(e.x, A.v0 * A.v0 * s / G)) r.push('Im Zähler steht \\(\\sin(2\\alpha)\\), nicht \\(\\sin\\alpha\\) — oder rechne \\(s_x = v_0 \\cdot \\cos\\alpha \\cdot t_F\\).');
            else r.push('Waagrecht gleichförmig: \\(s_x = v_0 \\cdot \\cos\\alpha \\cdot t_F\\).');
          }
          return r.join(' '); },
        fehler: function(A){ var c = Math.cos(A.al * GRAD), tc = 2 * A.v0 * c / G;
          return [[{ t: String(2 * A.v0 * Math.sin(A.al) / G), x: String(A.x) }, 'Bogenmass'], [{ t: String(A.t / 2), x: String(A.v0 * c * A.t / 2) }, 'höchsten'],
                  [{ t: String(tc), x: String(A.v0 * c * tc) }, 'senkrechte'], [{ t: String(A.t), x: String(A.v0 * A.v0 * Math.sin(A.al * GRAD) / G) }, 'Zähler']]; },
        loesung: function(A){ return 't_F = \\dfrac{2 \\cdot v_0 \\cdot \\sin\\alpha}{g} = \\dfrac{2 \\cdot ' + ein(A.v0, 'm/s') + ' \\cdot \\sin ' + A.al + '^\\circ}{9.81\\;\\text{m/s}^2} ' + erg(A.t, 's') + ',\\quad s_x = \\dfrac{v_0^2 \\cdot \\sin(2\\alpha)}{g} = \\dfrac{(' + ein(A.v0, 'm/s') + ')^2 \\cdot \\sin ' + (2 * A.al) + '^\\circ}{9.81\\;\\text{m/s}^2} ' + erg(A.x, 'm'); } },

      /* ----- Kapitel 3: Vektoren ----- */
      'eindim': { felder: ['v'], muster: '<i>v</i> = {v} m/s',
        neu: function(){
          var K, vT, vP, mit;
          do {
            K = zufall([['In einem Zug', 'des Zuges', [20, 25, 30, 40], [1, 1.5, 2]], ['Auf einem Schiff', 'des Schiffs', [5, 6, 8], [1, 2]], ['Auf einem Laufband', 'des Laufbands', [0.5, 0.8, 1, 1.2], [1, 1.5]]]);
            vT = zufall(K[2]); vP = zufall(K[3]); mit = Math.random() < 0.5;
          } while (vT === vP || (vT === 30 && vP === 1.5) || (vT === 8 && vP === 2 && !mit) || (vT === 1.2 && vP === 1.5));   // Clip, Kontrollclip, Aufgabe 4a
          return { v: mit ? vT + vP : vT - vP, vT: vT, vP: vP, mit: mit,
            text: K[0] + ' (\\(' + ein(vT, 'm/s') + '\\) gegenüber dem Boden) geht jemand mit \\(' + ein(vP, 'm/s') + '\\) ' + (mit ? 'in' : 'gegen die') + ' Fahrtrichtung. Wie schnell bewegt sich die Person gegenüber dem Boden? (Fahrtrichtung ' + K[1] + ' positiv)' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (A.mit && nah(e.v, A.vT - A.vP)) return 'In Fahrtrichtung zeigen beide Pfeile gleich: Die Geschwindigkeiten addieren sich.';
          if (!A.mit && nah(e.v, A.vT + A.vP)) return 'Gegen die Fahrtrichtung zeigt der Pfeil der Person nach hinten: \\(v = v_\\text{Träger} - v_\\text{Person}\\).';
          if (nah(e.v, -A.v)) return 'Vorzeichen: Die Fahrtrichtung zählt positiv.';
          if (nah(e.v, A.vP)) return 'Das ist die Geschwindigkeit gegenüber dem Fahrzeug. Gefragt ist die gegenüber dem Boden.';
          return 'Pfeile mit Vorzeichen addieren: Fahrtrichtung positiv, Gegenrichtung negativ.'; },
        fehler: function(A){ return [[{ v: String(A.mit ? A.vT - A.vP : A.vT + A.vP) }, A.mit ? 'addieren sich' : 'nach hinten'], [{ v: String(A.vP) }, 'Fahrzeug']]; },
        loesung: function(A){ return 'v = ' + ein(A.vT, 'm/s') + (A.mit ? ' + ' : ' - ') + ein(A.vP, 'm/s') + ' = ' + ein(A.v, 'm/s'); } },
      'quer': { felder: ['v', 'g'], muster: '|<i>v</i><sub>Ufer</sub>| = {v} m/s; <i>γ</i> = {g} °',
        neu: function(){
          var vS, vF;
          do { vS = zufall([1, 1.5, 2, 3, 4, 5]); vF = zufall([0.5, 1, 1.5, 2, 3]); }
          while (vS === vF || (vS === 2 && vF === 1) || (vS === 3 && vF === 4) || (vS === 3 && vF === 2) || (vS === 2.5 && vF === 1.5));
          return { v: Math.hypot(vS, vF), g: Math.atan(vF / vS) / GRAD, vS: vS, vF: vF,
            text: 'Eine Schwimmerin schwimmt mit \\(' + ein(vS, 'm/s') + '\\) quer zum Ufer, die Strömung hat \\(' + ein(vF, 'm/s') + '\\). Wie schnell ist sie gegenüber dem Ufer, und um welchen Winkel \\(\\gamma\\) wird sie gegenüber der Querrichtung abgetrieben?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v) && nah(e.g, A.g)) return null;
          var r = [];
          if (!nah(e.v, A.v)){
            if (nah(e.v, A.vS + A.vF) || nah(e.v, Math.abs(A.vS - A.vF))) r.push('Pfeile, die quer zueinander stehen, addiert man nicht als Zahlen: Pythagoras, \\(\\sqrt{v_S^2 + v_F^2}\\).');
            else if (nah(e.v, A.vS * A.vS + A.vF * A.vF)) r.push('Die Wurzel fehlt: \\(\\sqrt{v_S^2 + v_F^2}\\).');
            else r.push('\\(|\\vec v_\\text{Ufer}| = \\sqrt{v_S^2 + v_F^2}\\).');
          }
          if (!nah(e.g, A.g)){
            if (nah(e.g, 90 - A.g)) r.push('Das ist der Winkel zur Strömung. Gefragt ist die Abweichung von der Querrichtung: \\(\\tan\\gamma = \\dfrac{v_F}{v_S}\\).');
            else if (nah(e.g, A.g * GRAD)) r.push('Das ist der Winkel im Bogenmass. Gefragt sind Grad.');
            else r.push('\\(\\tan\\gamma = \\dfrac{v_F}{v_S}\\).');
          }
          return r.join(' '); },
        fehler: function(A){ return [[{ v: String(A.vS + A.vF), g: String(A.g) }, 'Pythagoras'], [{ v: String(A.v), g: String(90 - A.g) }, 'Strömung'], [{ v: String(A.v), g: String(A.g * GRAD) }, 'Bogenmass']]; },
        loesung: function(A){ return '|\\vec v_\\text{Ufer}| = \\sqrt{v_S^2 + v_F^2} = \\sqrt{(' + ein(A.vS, 'm/s') + ')^2 + (' + ein(A.vF, 'm/s') + ')^2} ' + erg(A.v, 'm/s') + ',\\quad \\tan\\gamma = \\dfrac{v_F}{v_S} = \\dfrac{' + tz(A.vF) + '}{' + tz(A.vS) + '},\\; \\gamma ' + (Math.abs(+A.g.toPrecision(3) - A.g) < 1e-9 ? '= ' : '\\approx ') + tz(+A.g.toPrecision(3)) + '^\\circ'; } },
      'fluss': { felder: ['t', 'd'], muster: '<i>t</i> = {t} s; <i>d</i> = {d} m',
        neu: function(){
          var b, vS, vF;
          do { b = zufall([20, 30, 40, 60, 80, 100]); vS = zufall([1, 1.5, 2, 2.5, 4]); vF = zufall([0.5, 1, 1.5, 2, 3]); }
          while (vS === vF || (b === 40 && vS === 2 && vF === 1) || (b === 60 && vS === 3 && vF === 2) || (b === 30 && vS === 2 && vF === 1) || (b === 50 && vS === 2.5 && vF === 1.5));
          var t = b / vS;
          return { t: t, d: vF * t, b: b, vS: vS, vF: vF,
            text: 'Ein Boot fährt mit \\(' + ein(vS, 'm/s') + '\\) quer über einen \\(' + ein(b, 'm') + '\\) breiten Fluss; die Strömung hat \\(' + ein(vF, 'm/s') + '\\). Wie lange dauert die Überquerung, und wie weit wird es flussabwärts versetzt?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t) && nah(e.d, A.d)) return null;
          var r = [];
          if (!nah(e.t, A.t)){
            if (nah(e.t, A.b / Math.hypot(A.vS, A.vF))) r.push('Die Querzeit hängt nur von der Quergeschwindigkeit ab: \\(t = \\dfrac{b}{v_S}\\). Die Strömung trägt nichts zum Überqueren bei.');
            else if (nah(e.t, A.b / A.vF)) r.push('Über den Fluss bringt das Boot seine eigene Geschwindigkeit, nicht die Strömung: \\(t = \\dfrac{b}{v_S}\\).');
            else r.push('\\(t = \\dfrac{b}{v_S}\\).');
          }
          if (!nah(e.d, A.d) && !(!nah(e.t, A.t) && nah(e.d, A.vF * e.t))){
            if (nah(e.d, A.vS * A.t)) r.push('Versetzt wird das Boot von der Strömung: \\(d = v_F \\cdot t\\).');
            else r.push('\\(d = v_F \\cdot t\\).');
          }
          return r.join(' '); },
        fehler: function(A){ var t2 = A.b / Math.hypot(A.vS, A.vF);
          return [[{ t: String(t2), d: String(A.vF * t2) }, 'Quergeschwindigkeit'], [{ t: String(A.b / A.vF), d: String(A.b) }, 'eigene'], [{ t: String(A.t), d: String(A.b) }, 'Strömung']]; },
        loesung: function(A){ return 't = \\dfrac{b}{v_S} = \\dfrac{' + ein(A.b, 'm') + '}{' + ein(A.vS, 'm/s') + '} ' + erg(A.t, 's') + ',\\quad d = v_F \\cdot t = ' + ein(A.vF, 'm/s') + ' \\cdot ' + ein(+A.t.toPrecision(4), 's') + ' ' + erg(A.d, 'm'); } },

      /* ----- Kapitel 5 ----- */
      'umlauf': { felder: ['f', 'w'], muster: '<i>f</i> = {f} Hz; <i>ω</i> = {w} rad/s',
        neu: function(){
          if (Math.random() < 0.5){
            var n = zufall([30, 45, 90, 240, 600, 900, 1500]);
            return { art: 'n', n: n, f: n / 60, w: PI2 * n / 60, text: 'Eine Welle macht \\(' + tz(n) + '\\) Umdrehungen pro Minute. Wie gross sind Rotationsfrequenz und Winkelgeschwindigkeit?' };
          }
          var T = zufall([0.2, 0.5, 2.5, 4, 5, 20]);
          return { art: 'T', T: T, f: 1 / T, w: PI2 / T, text: 'Ein Rad dreht sich gleichförmig, eine Umdrehung dauert \\(T = ' + ein(T, 's') + '\\). Wie gross sind Rotationsfrequenz und Winkelgeschwindigkeit?' }; },
        pruefen: function(A, e){
          if (nah(e.f, A.f) && nah(e.w, A.w)) return null;
          var r = [];
          if (!nah(e.f, A.f)){
            if (A.art === 'n' && nah(e.f, A.n)) r.push('Umdrehungen pro <em>Minute</em> in pro Sekunde: durch \\(60\\).');
            else if (nah(e.f, 1 / A.f)) r.push('Das ist die Umlaufzeit \\(T\\). Die Frequenz ist ihr Kehrwert: \\(f = \\dfrac{1}{T}\\).');
            else r.push(A.art === 'n' ? '\\(f\\) = Umdrehungen pro Sekunde.' : '\\(f = \\dfrac{1}{T}\\).');
          }
          if (!nah(e.w, A.w) && !(!nah(e.f, A.f) && nah(e.w, PI2 * e.f))){
            if (nah(e.w, A.f)) r.push('\\(2\\pi\\) fehlt: \\(\\omega = 2\\pi \\cdot f\\) — eine Umdrehung sind \\(2\\pi\\) rad.');
            else if (nah(e.w, PI2 / A.f)) r.push('Umgekehrt: \\(\\omega = 2\\pi \\cdot f = \\dfrac{2\\pi}{T}\\).');
            else if (nah(e.w, 360 * A.f)) r.push('Die Winkelgeschwindigkeit steht in rad/s: \\(2\\pi\\) statt \\(360^\\circ\\).');
            else r.push('\\(\\omega = 2\\pi \\cdot f\\).');
          }
          return r.join(' '); },
        fehler: function(A){
          var l = [[{ f: String(A.f), w: String(A.f) }, '2\\pi'], [{ f: String(A.f), w: String(PI2 / A.f) }, 'Umgekehrt'], [{ f: String(A.f), w: String(360 * A.f) }, 'rad/s'], [{ f: String(1 / A.f), w: String(PI2 / A.f) }, 'Kehrwert']];
          if (A.art === 'n') l.push([{ f: String(A.n), w: String(PI2 * A.n) }, 'Minute']);
          return l; },
        loesung: function(A){ return (A.art === 'n' ? 'f = \\dfrac{' + tz(A.n) + '}{60\\;\\text{s}} ' : 'f = \\dfrac{1}{T} = \\dfrac{1}{' + ein(A.T, 's') + '} ') + erg(A.f, 'Hz') + ',\\quad \\omega = 2\\pi \\cdot f = 2\\pi \\cdot ' + ein(+A.f.toPrecision(4), 'Hz') + ' ' + erg(A.w, 'rad/s'); } },
      'bahn': { felder: ['v', 'a'], muster: '<i>v</i> = {v} m/s; <i>a</i><sub>z</sub> = {a} m/s²',
        neu: function(){
          var r, T, vv;
          do { r = zufall([0.3, 0.5, 1.2, 2.5, 6, 8]); T = zufall([0.5, 1.5, 3, 5, 10, 12]); vv = PI2 * r / T; }
          while (Math.abs(vv - 1) < 0.05 || (r === 0.5 && T === 2) || vv * vv / r > 2000);
          return { v: vv, a: vv * vv / r, r: r, T: T,
            text: 'Ein Punkt läuft auf einem Kreis mit \\(r = ' + ein(r, 'm') + '\\) gleichförmig um; ein Umlauf dauert \\(T = ' + ein(T, 's') + '\\). Bahngeschwindigkeit und Zentripetalbeschleunigung?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v) && (nah(e.a, A.a) || nah(e.a, e.v * e.v / A.r))) return null;   // gerundetes v richtig weitergerechnet
          var r = [];
          if (!nah(e.v, A.v)){
            if (nah(e.v, A.r / A.T)) r.push('\\(2\\pi\\) fehlt: In einer Umlaufzeit legt der Punkt den Kreisumfang \\(2\\pi r\\) zurück, \\(v = \\dfrac{2\\pi r}{T} = \\omega \\cdot r\\).');
            else if (nah(e.v, Math.PI * A.r / A.T)) r.push('Der Umfang ist \\(2\\pi r\\), nicht \\(\\pi r\\).');
            else if (nah(e.v, PI2 * A.T / A.r)) r.push('Umgekehrt: \\(v = \\dfrac{2\\pi r}{T}\\).');
            else r.push('\\(v = \\omega \\cdot r = \\dfrac{2\\pi r}{T}\\).');
          }
          if (!nah(e.a, A.a) && !(!nah(e.v, A.v) && nah(e.a, e.v * e.v / A.r))){
            if (nah(e.a, A.v / A.r)) r.push('Das Quadrat fehlt: \\(a_z = \\dfrac{v^2}{r}\\).');
            else if (nah(e.a, A.v * A.v * A.r)) r.push('Durch \\(r\\) teilen: \\(a_z = \\dfrac{v^2}{r} = \\omega^2 \\cdot r\\).');
            else r.push('\\(a_z = \\dfrac{v^2}{r}\\).');
          }
          return r.join(' '); },
        fehler: function(A){ var v2 = A.r / A.T;
          return [[{ v: String(v2), a: String(v2 * v2 / A.r) }, '2\\pi'], [{ v: String(A.v), a: String(A.v / A.r) }, 'Quadrat'], [{ v: String(A.v), a: String(A.v * A.v * A.r) }, 'teilen']]; },
        loesung: function(A){ return 'v = \\dfrac{2\\pi \\cdot r}{T} = \\dfrac{2\\pi \\cdot ' + ein(A.r, 'm') + '}{' + ein(A.T, 's') + '} ' + erg(A.v, 'm/s') + ',\\quad a_z = \\dfrac{v^2}{r} = \\dfrac{(' + ein(+A.v.toPrecision(4), 'm/s') + ')^2}{' + ein(A.r, 'm') + '} ' + erg(A.a, 'm/s^2').replace('\\text{m/s^2}', '\\text{m/s}^2'); } },
      'zentripetal': { felder: ['a'], muster: '<i>a</i><sub>z</sub> = {a} m/s²',
        neu: function(){
          var vk, r;
          do { vk = zufall([36, 54, 72, 90, 108]); r = zufall([25, 40, 60, 100, 150, 250]); } while ((vk === 54 && r === 50) || (vk / 3.6) * (vk / 3.6) / r > 7);   // höchstens 7 m/s², sonst schafft es kein Auto
          var v0 = vk / 3.6;
          return { a: v0 * v0 / r, vk: vk, v: v0, r: r,
            text: 'Ein Auto fährt mit \\(' + ein(vk, 'km/h') + '\\) durch eine Kurve mit \\(r = ' + ein(r, 'm') + '\\). Wie gross ist die Zentripetalbeschleunigung?' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a)) return null;
          if (nah(e.a, A.vk * A.vk / A.r)) return 'Erst in m/s umrechnen: ' + umr(A.vk) + '.';
          if (nah(e.a, A.v / A.r)) return 'Das Quadrat fehlt: \\(a_z = \\dfrac{v^2}{r}\\).';
          if (nah(e.a, A.v * A.v * A.r)) return 'Durch \\(r\\) teilen: \\(a_z = \\dfrac{v^2}{r}\\).';
          return '\\(a_z = \\dfrac{v^2}{r}\\) mit \\(v\\) in m/s.'; },
        fehler: function(A){ return [[{ a: String(A.vk * A.vk / A.r) }, 'umrechnen'], [{ a: String(A.v / A.r) }, 'Quadrat'], [{ a: String(A.v * A.v * A.r) }, 'teilen']]; },
        loesung: function(A){ return 'v = \\dfrac{' + tz(A.vk) + '}{3.6}\\;\\text{m/s} ' + erg(A.v, 'm/s') + ',\\quad a_z = \\dfrac{v^2}{r} = \\dfrac{(' + ein(+A.v.toPrecision(4), 'm/s') + ')^2}{' + ein(A.r, 'm') + '} ' + erg(A.a, 'm/s^2').replace('\\text{m/s^2}', '\\text{m/s}^2'); } }
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
