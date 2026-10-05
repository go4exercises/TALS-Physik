<script>
/* Leitprogramm Hydrostatik — laufende Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr, Übungsrahmen,
   Minigrafen) wörtlich aus dem Leitprogramm Statik; neu sind die Simulationen (Person im Schnee,
   Taucherin mit Manometer, Saugrohr unter Luftdruck, hydraulische Hebebühne, Körper an der
   Federwaage, Würfel, der sich im Wasser einpendelt) und die Übungstypen für 4.5. g = 9.81 m/s²
   und p_0 = 1013 hPa wie Themenseite 4.5. Farben: Gewichtskraft Bernstein (wie Statik und
   Dynamik), Auftrieb Grün, Kräfte an Kolben Blau, Luftdruck Grau, Tiefe und Höhe Violett.
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
  // SVG-Text mit Indizes: «F_y [N]», «μ_H · F_N» — der Teil nach «_» steht tiefer und kleiner
  function stext(eltern, attr, s){
    var t = el(eltern, 'text', attr), tief = false;
    String(s).split(/(_[A-Za-zα-ω0-9,]+)/).forEach(function(p){
      if (!p) return;
      if (p.charAt(0) === '_'){ el(t, 'tspan', { dy: tief ? 0 : 3, 'font-size': '0.78em' }, p.slice(1)); tief = true; }
      else { el(t, 'tspan', tief ? { dy: -3 } : {}, p); tief = false; }
    });
    return t;
  }
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
    stext(schilder, { x: W - 3, y: Y(0) - pf - 2, 'text-anchor': 'end', 'class': 'achsname' }, o.xname || 'x');
    stext(schilder, { x: X(0) + pf + 2, y: pf + 5, 'text-anchor': 'start', 'class': 'achsname' }, o.yname || 'y');
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


  var G = 9.81;                                          // wie Themenseite 4.5
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


  function kn(x){ return sig(x) + NB + 'N'; }
  function F_(i){ return v_('F') + '<sub>' + i + '</sub>'; }
  function p_(i){ return v_('p') + (i ? '<sub>' + i + '</sub>' : ''); }
  // Achsenteilung zum grössten Wert: höchstens vier beschriftete Striche
  function skala(max){
    var st = [0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000], i = 0;
    while (i < st.length - 1 && max / st[i] > 4) i++;
    var s = st[i], oben = Math.ceil(max * 1.08 / s) * s, ym = [];
    for (var v = s; v <= oben + 1e-9; v += s) ym.push(+v.toPrecision(6));
    return { y0: -0.1 * oben, y1: oben * 1.04, sy: s / 2, ym: ym };
  }
  // Druck in Pa auf drei Stellen, dazu in den gefragten Einheiten
  function pa(x){ return sig(x) + NB + 'Pa'; }
  function wasser(eltern, x, y, w, h, cls){ return el(eltern, 'rect', { x: x, y: y, width: w, height: h, 'class': cls || 'wasser' }); }

  /* ---------- Kapitel 1: Druck zwischen Festkörpern ----------
     Eine Person steht auf einer Auflagefläche A im Schnee. Auf Knopfdruck stellt sie sich hin
     und sinkt ein; die Eindrucktiefe wächst mit dem Druck p = F / A (vereinfachtes Schneemodell
     d = 40 cm · p / (p + 10 kPa)). Darunter der Druck über der Fläche (Hyperbel) für die
     eingestellte Masse. Gewichtskraft Bernstein. Clipbeispiel: 60 kg auf 300 cm² und 1800 cm²;
     Startwerte 50 kg, 600 cm². */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,196)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); u = 0; ende = false; zeichnen(); });
    var u = 0, ende = false, lauf = null, laeufe = [], vorher = null, pruefen = function(){};
    var SY = 120, PXCM = 2;                                                     // Schneeoberfläche, 2 px je cm
    function werte(){ var m = B.wert('m'), A = B.wert('A'), F = m * G, p = F / (A / 1e4); return { m: m, A: A, F: F, p: p, d: 40 * p / (p + 10000) }; }
    function fertig(w){ ende = true; lauf = { m: w.m, A: w.A, p: w.p, d: w.d }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); u = Math.min(1, tt / 2.2); zeichnen(); if (u >= 1){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Hinstehen', function(){ vorher = lauf; ende = false; if (WENIGER){ u = 1; fertig(werte()); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); u = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); u = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; vorher = null; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); u = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(); B.anzeigen(); leeren(szene); leeren(dia);
      // erst absetzen (u bis 0.4), dann einsinken
      var senk = u < 0.4 ? 0 : (u - 0.4) / 0.6, ss = senk * senk * (3 - 2 * senk), dz = w.d * ss * PXCM, hoch = u < 0.4 ? (1 - u / 0.4) * 30 : 0;
      el(szene, 'rect', { x: 0, y: SY, width: 300, height: 76, 'class': 'schnee' });
      el(szene, 'line', { x1: 0, y1: SY, x2: 300, y2: SY, 'class': 'schnee-rand' });
      for (var cm = 10; cm <= 30; cm += 10) el(szene, 'text', { x: 296, y: SY + cm * PXCM + 3, 'text-anchor': 'end', 'class': 'skala' }, cm + ' cm');
      // Auflage: Breite nach Fläche (quadratische Platte, Seitenansicht)
      var bw = Math.max(10, Math.sqrt(w.A) * 2.0), cx = 140, fy = SY - hoch + dz;
      if (dz > 0.5) el(szene, 'rect', { x: cx - bw / 2, y: SY, width: bw, height: dz, 'class': 'mulde' });
      el(szene, 'rect', { x: cx - bw / 2, y: fy - 5, width: bw, height: 5, rx: 1.5, 'class': 'sohle' });
      // Person (Strichfigur), Grösse nach Masse
      var s = 0.8 + w.m / 250, ky = fy - 5;
      el(szene, 'line', { x1: cx - 7 * s, y1: ky, x2: cx, y2: ky - 30 * s, 'class': 'mensch' });
      el(szene, 'line', { x1: cx + 7 * s, y1: ky, x2: cx, y2: ky - 30 * s, 'class': 'mensch' });
      el(szene, 'line', { x1: cx, y1: ky - 30 * s, x2: cx, y2: ky - 58 * s, 'class': 'mensch' });
      el(szene, 'line', { x1: cx - 13 * s, y1: ky - 44 * s, x2: cx + 13 * s, y2: ky - 44 * s, 'class': 'mensch' });
      el(szene, 'circle', { cx: cx, cy: ky - 66 * s, r: 7 * s, 'class': 'kopf' });
      var lF = 18 + w.F / 25;
      pfeil(szene, cx + 30, ky - 50, cx + 30, ky - 50 + lF, 'pf-g', 8); marke(szene, cx + 36, ky - 46 + lF / 2, 'F', 'G', 'pf-text pf-g', 'start');
      if (vorher && !uhr.laeuft()) el(szene, 'line', { x1: 12, y1: SY + vorher.d * PXCM, x2: 70, y2: SY + vorher.d * PXCM, 'class': 'vorher' });
      if (dz > 2) el(szene, 'text', { x: cx - bw / 2 - 6, y: SY + dz / 2 + 4, 'text-anchor': 'end', 'class': 'bt-klein' }, sig(w.d * ss, 2) + ' cm');
      // Diagramm: Druck über der Fläche für diese Masse
      var pmax = w.m * G / 0.01 / 1000;                                      // kPa bei 100 cm²
      var sk = skala(Math.min(pmax, 120));
      K = Achsen(dia, { w: 300, h: 120, x0: -250, x1: 4300, y0: sk.y0, y1: sk.y1, sx: 500, sy: sk.sy, xm: [1000, 2000, 3000, 4000], ym: sk.ym, xname: 'A [cm²]', yname: 'p [kPa]' });
      K.kurve(function(a){ return w.m * G / (a / 1e4) / 1000; }, 'kurve-p', 100, 4000);
      K.punkt(w.A, w.p / 1000, 'p-p');
      var z = '<span>' + p_() + ' = ' + v_('F') + ' / ' + v_('A') + ' = ' + v_('m') + ' · ' + v_('g') + ' / ' + v_('A') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² / ' + zahl(w.A / 1e4) + NB + 'm² ' + ist(w.p, sig(w.p)) + sig(w.p) + NB + 'Pa</span>';
      z += '<span>' + p_() + ' ' + ist(w.p, sig(w.p)) + sig(w.p / 1000) + NB + 'kPa ' + ist(w.p / 100, sig(w.p / 100)) + sig(w.p / 100) + NB + 'hPa ' + ist(w.p / 1e5, sig(w.p / 1e5)) + sig(w.p / 1e5) + NB + 'bar</span>';
      z += '<span class="sim-notiz">' + zahl(w.A) + NB + 'cm² = ' + zahl(w.A / 1e4) + NB + 'm². Vereinfachtes Schneemodell: Je grösser der Druck, desto tiefer sinkt man ein.' + (vorher ? ' Grau: Tiefe beim vorigen Hinstehen.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, m, A){ return s.lauf && s.lauf.m === m && s.lauf.A === A; }
    pruefen = Leiste(fig, [
      { text: 'Eine Person mit \\(70\\;\\text{kg}\\) steht auf Schuhen mit zusammen \\(400\\;\\text{cm}^2\\). Stell dich hin. Wie gross ist der Druck in kPa und in bar? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 70, 400); },
        vergleich: '\\(F = m \\cdot g = 70\\;\\text{kg} \\cdot 9.81\\;\\text{m/s}^2 \\approx 687\\;\\text{N}\\), \\(A = 400\\;\\text{cm}^2 = 0.04\\;\\text{m}^2\\). \\(p = \\dfrac{F}{A} \\approx 17\\,200\\;\\text{Pa} = 17.2\\;\\text{kPa} = 0.172\\;\\text{bar}\\).' },
      { text: 'Bleib bei derselben Masse und verdopple die Fläche. Stell dich zweimal hin. Was geschieht mit dem Druck? Begründe.', ok: function(s){ var l = s.laeufe; for (var i = 0; i < l.length; i++) for (var j = 0; j < l.length; j++) if (l[i].m === l[j].m && l[j].A === 2 * l[i].A) return true; return false; },
        vergleich: 'Der Druck halbiert sich: Dieselbe Kraft verteilt sich auf die doppelte Fläche, \\(p = \\dfrac{F}{A}\\). Darum sinkt man mit Schneeschuhen weniger ein.' },
      { text: 'Eine Person mit \\(60\\;\\text{kg}\\) soll höchstens \\(4\\;\\text{kPa}\\) erzeugen. Welche Fläche braucht sie mindestens (auf \\(50\\;\\text{cm}^2\\) genau)? Stelle ein und stell dich hin.', ok: function(s){ return hat(s, 60, 1500); },
        vergleich: '\\(A = \\dfrac{F}{p} = \\dfrac{60\\;\\text{kg} \\cdot 9.81\\;\\text{m/s}^2}{4000\\;\\text{Pa}} \\approx 0.147\\;\\text{m}^2 = 1470\\;\\text{cm}^2\\). Auf dem Regler reichen \\(1500\\;\\text{cm}^2\\); bei \\(1450\\;\\text{cm}^2\\) wären es schon rund \\(4.06\\;\\text{kPa}\\).' },
      { text: 'Eine Person mit \\(100\\;\\text{kg}\\) soll gleich tief einsinken wie eine mit \\(50\\;\\text{kg}\\) auf \\(600\\;\\text{cm}^2\\). Welche Fläche braucht sie? Stelle ein und stell dich hin.', ok: function(s){ return hat(s, 100, 1200); },
        vergleich: 'Gleich tief heisst gleicher Druck. Doppelte Kraft braucht dafür die doppelte Fläche: \\(1200\\;\\text{cm}^2\\).' },
      { text: 'Bei \\(2500\\;\\text{cm}^2\\) soll der Druck \\(2.0\\;\\text{kPa}\\) betragen (auf \\(0.05\\;\\text{kPa}\\) genau). Welche Masse? Stelle ein und stell dich hin.', ok: function(s){ return s.lauf && s.lauf.A === 2500 && Math.abs(s.lauf.p - 2000) <= 50; },
        vergleich: '\\(F = p \\cdot A = 2000\\;\\text{Pa} \\cdot 0.25\\;\\text{m}^2 = 500\\;\\text{N}\\), \\(m = \\dfrac{F}{g} \\approx 51\\;\\text{kg}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Schweredruck beim Tauchen ----------
     Eine Taucherin taucht auf Knopfdruck bis zur eingestellten Tiefe. Ein Manometer zeigt den
     Schweredruck p_S = ρ · g · h und den Gesamtdruck p = p_0 + p_S; im Diagramm wächst der
     Gesamtdruck als Gerade über h (gestrichelt: Schweredruck allein). p_0 = 1013 hPa.
     Clipbeispiel: 6 m im Schwimmbecken; Startwerte 8 m, See. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,208)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); h = 0; ende = false; zeichnen(); });
    var h = 0, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var P0 = 101300, WY = 22, PXM = 4.4;                                      // Wasseroberfläche, 4.4 px je m (40 m)
    function werte(){ var hz = B.wert('h'), rho = +B.wert('rho'); return { hz: hz, rho: rho }; }
    function fertig(w){ ende = true; lauf = { h: w.hz, rho: w.rho, pS: w.rho * G * w.hz, p: P0 + w.rho * G * w.hz }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); h = Math.min(w.hz, tt * 6); zeichnen(); if (h >= w.hz){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Abtauchen', function(){ ende = false; if (WENIGER){ var w = werte(); h = w.hz; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Auftauchen', function(){ uhr.stop(); h = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); h = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); h = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), pS = w.rho * G * h, p = P0 + pS;
      B.anzeigen(); leeren(szene); leeren(dia);
      wasser(szene, 0, WY, 200, 40 * PXM + 4, w.rho > 1100 ? 'wasser salzig' : 'wasser');
      el(szene, 'line', { x1: 0, y1: WY, x2: 200, y2: WY, 'class': 'wasserlinie' });
      for (var t = 10; t <= 40; t += 10) el(szene, 'text', { x: 4, y: WY + t * PXM + 4, 'class': 'skala' }, t + ' m');
      // Taucherin (Kopf unten nicht nötig: aufrecht, Flossen unten)
      var dx = 110, dy = WY + h * PXM;
      el(szene, 'circle', { cx: dx, cy: dy - 4, r: 5, 'class': 'kopf' });
      el(szene, 'rect', { x: dx - 4, y: dy + 1, width: 8, height: 16, rx: 3, 'class': 'taucher' });
      el(szene, 'rect', { x: dx + 4, y: dy + 2, width: 4, height: 10, rx: 1.5, 'class': 'flasche' });
      el(szene, 'line', { x1: dx - 2, y1: dy + 17, x2: dx - 5, y2: dy + 26, 'class': 'mensch' }); el(szene, 'line', { x1: dx + 2, y1: dy + 17, x2: dx + 5, y2: dy + 26, 'class': 'mensch' });
      if (h > 0.2){ el(szene, 'line', { x1: 60, y1: WY, x2: 60, y2: dy, 'class': 'hebelarm' }); el(szene, 'text', { x: 64, y: (WY + dy) / 2 + 4, 'class': 'pf-text pf-a' }, 'h = ' + zahl(+h.toFixed(1)) + ' m'); }
      // Manometer rechts
      var mx = 252, my = 70, R = 34, wmax = 6e5, ww = Math.min(p, wmax) / wmax;
      el(szene, 'circle', { cx: mx, cy: my, r: R, 'class': 'manometer' });
      for (var b = 0; b <= 6; b++){ var aa = Math.PI * (1.25 - 1.5 * b / 6); el(szene, 'line', { x1: mx + (R - 6) * Math.cos(aa), y1: my - (R - 6) * Math.sin(aa), x2: mx + R * Math.cos(aa), y2: my - R * Math.sin(aa), 'class': 'tick' }); el(szene, 'text', { x: mx + (R - 13) * Math.cos(aa), y: my - (R - 13) * Math.sin(aa) + 3, 'text-anchor': 'middle', 'class': 'skala klein' }, b); }
      var az = Math.PI * (1.25 - 1.5 * ww); el(szene, 'line', { x1: mx, y1: my, x2: mx + (R - 9) * Math.cos(az), y2: my - (R - 9) * Math.sin(az), 'class': 'zeiger' });
      el(szene, 'text', { x: mx, y: my + R + 13, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'p in bar (absolut)');
      el(szene, 'text', { x: mx, y: my + R + 30, 'text-anchor': 'middle', 'class': 'bt-wert' }, sig(p / 1e5) + NB + 'bar');
      // Diagramm: Druck über der Tiefe bis zur aktuellen Tiefe
      K = Achsen(dia, { w: 300, h: 120, x0: -2.5, x1: 43, y0: -0.6, y1: 6.6, sx: 5, sy: 0.5, xm: [10, 20, 30, 40], ym: [1, 2, 3, 4, 5, 6], xname: 'h [m]', yname: 'p [bar]' });
      if (h > 0){ K.kurve(function(x){ return (P0 + w.rho * G * x) / 1e5; }, 'kurve-p', 0, h); K.kurve(function(x){ return w.rho * G * x / 1e5; }, 'kurve-ps', 0, h); }
      K.punkt(h, p / 1e5, 'p-p'); K.punkt(h, pS / 1e5, 'p-ps');
      stext(K.ebene, { x: 296, y: 12, 'text-anchor': 'end', 'class': 'legende l-p' }, '— p = p_0 + p_S');
      stext(K.ebene, { x: 296, y: 24, 'text-anchor': 'end', 'class': 'legende l-ps' }, '- - p_S');
      var H = +h.toFixed(1);
      var z = '<span>' + p_('S') + ' = ' + v_('ρ') + ' · ' + v_('g') + ' · ' + v_('h') + ' = ' + zahl(w.rho) + NB + 'kg/m³ · 9.81' + NB + 'm/s² · ' + zahl(H) + NB + 'm ' + ist(w.rho * G * H, sig(w.rho * G * H)) + sig(w.rho * G * H) + NB + 'Pa</span>';
      var pSh = w.rho * G * H / 100;
      z += '<span>' + p_() + ' = ' + p_('0') + ' + ' + p_('S') + ' = 1013' + NB + 'hPa + ' + zahl(+pSh.toFixed(1)) + NB + 'hPa ' + ist(1013 + pSh, sig(1013 + pSh, 4)) + sig(1013 + pSh, 4) + NB + 'hPa</span>';
      z += '<span class="sim-notiz">' + p_('0') + ': Luftdruck an der Oberfläche (Meereshöhe). Das Manometer zeigt den absoluten Druck.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, hh, r){ return s.lauf && s.lauf.h === hh && s.lauf.rho === r; }
    pruefen = Leiste(fig, [
      { text: 'Tauche im See auf \\(15\\;\\text{m}\\). Wie gross sind Schweredruck und Gesamtdruck in bar? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 15, 1000); },
        vergleich: '\\(p_S = \\rho \\cdot g \\cdot h = 1000\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\cdot 15\\;\\text{m} \\approx 147\\,000\\;\\text{Pa} \\approx 1.47\\;\\text{bar}\\). Mit dem Luftdruck: \\(p = 1.013\\;\\text{bar} + 1.47\\;\\text{bar} \\approx 2.48\\;\\text{bar}\\).' },
      { text: 'In welcher Tiefe ist der Gesamtdruck im See zum ersten Mal mindestens doppelt so gross wie an der Oberfläche? Tauche hin (auf \\(0.5\\;\\text{m}\\) genau).', ok: function(s){ return hat(s, 10.5, 1000); },
        vergleich: 'Doppelt heisst \\(p_S = p_0\\): \\(h = \\dfrac{p_0}{\\rho \\cdot g} = \\dfrac{101\\,300\\;\\text{Pa}}{1000\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2} \\approx 10.3\\;\\text{m}\\). Auf dem Regler ist \\(10.5\\;\\text{m}\\) die erste Tiefe, die reicht.' },
      { text: 'Tauche auf \\(20\\;\\text{m}\\), einmal im See und einmal im Meer. Wo ist der Druck grösser, und warum? Begründe.', ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (l.h === 20) n[l.rho] = true; }); return n[1000] && n[1025]; },
        vergleich: 'Im Meer: Meerwasser hat die grössere Dichte (\\(1025\\;\\text{kg/m}^3\\)), die Wassersäule darüber ist schwerer. \\(p_S\\) wächst mit \\(\\rho\\): rund \\(2.01\\;\\text{bar}\\) statt \\(1.96\\;\\text{bar}\\).' },
      { text: 'Tauche im See bis \\(30\\;\\text{m}\\). Lies im Diagramm ab, um wie viel der Druck je \\(10\\;\\text{m}\\) zunimmt. Warum beginnt die durchgezogene Gerade nicht bei null? Begründe.', ok: function(s){ return hat(s, 30, 1000); },
        vergleich: 'Je \\(10\\;\\text{m}\\) rund \\(1\\;\\text{bar}\\) (genauer \\(0.98\\;\\text{bar}\\)). Die Gerade beginnt beim Luftdruck \\(p_0 \\approx 1\\;\\text{bar}\\): Auf die Oberfläche drückt schon die Luft. Nur der Schweredruck (gestrichelt) beginnt bei null.' },
      { text: 'Im Toten Meer (\\(1240\\;\\text{kg/m}^3\\)): In welcher Tiefe herrscht derselbe Schweredruck wie in \\(31\\;\\text{m}\\) Tiefe im See? Rechne, dann tauche hin.', ok: function(s){ return hat(s, 25, 1240); },
        vergleich: '\\(\\rho_1 \\cdot h_1 = \\rho_2 \\cdot h_2\\): \\(h = \\dfrac{1000\\;\\text{kg/m}^3 \\cdot 31\\;\\text{m}}{1240\\;\\text{kg/m}^3} = 25\\;\\text{m}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Luftdruck und Saugrohr ----------
     Ein oben geschlossenes Rohr steht in einem Becken. Auf Knopfdruck saugt eine Pumpe die Luft
     aus dem Rohr, der Innendruck sinkt auf p_i; der Luftdruck p_0 auf das Becken drückt die
     Flüssigkeit hoch, bis ρ · g · h = p_0 − p_i. Ort (Luftdruck) und Flüssigkeit wählbar.
     Clipbeispiel: Trinkhalm, Torricelli 760 mm; Startwerte 800 hPa, Meereshöhe, Wasser. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg);
    var B = Bedienung(fig, function(){ uhr.stop(); pi = null; ende = false; zeichnen(); });
    var pi = null, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var BY = 300, ORTE = { '1013': 'Meereshöhe', '965': 'Zürich (408 m)', '841': 'Davos (1560 m)', '671': 'Jungfraujoch (3454 m)' };
    function werte(){ var p0 = +B.wert('ort'), piz = B.wert('pi'), rho = +B.wert('fl'); return { p0: p0, piz: piz, rho: rho }; }
    function hoehe(w, p){ return Math.max(0, (w.p0 - p) * 100 / (w.rho * G)); }
    function fertig(w){ ende = true; lauf = { p0: w.p0, pi: w.piz, rho: w.rho, h: hoehe(w, w.piz) }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(), u = Math.min(1, tt / 2.5); pi = w.p0 + (Math.min(w.piz, w.p0) - w.p0) * u; zeichnen(); if (u >= 1){ pi = Math.min(w.piz, w.p0); fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Absaugen', function(){ ende = false; if (WENIGER){ var w = werte(); pi = Math.min(w.piz, w.p0); fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Belüften', function(){ uhr.stop(); pi = null; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); pi = null; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); pi = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), p = pi == null ? w.p0 : pi, h = hoehe(w, p), hg = w.rho > 5000;
      var HM = hg ? 1 : 12, PXM = 250 / HM;                                     // Rohr 12 m (Wasser) oder 1 m (Quecksilber)
      B.anzeigen(); leeren(szene);
      // Becken
      el(szene, 'rect', { x: 20, y: BY - 22, width: 200, height: 22, 'class': hg ? 'quecksilber' : 'wasser' });
      el(szene, 'path', { d: 'M18 ' + (BY - 30) + ' L18 ' + BY + ' L222 ' + BY + ' L222 ' + (BY - 30), 'class': 'gefaess' });
      // Rohr
      var rx = 110, top = BY - 12 - HM * PXM;
      el(szene, 'rect', { x: rx - 8, y: top, width: 16, height: BY - 8 - top, 'class': 'rohr' });
      el(szene, 'rect', { x: rx - 6, y: BY - 12 - h * PXM, width: 12, height: h * PXM + 4, 'class': hg ? 'quecksilber' : 'wasser' });
      el(szene, 'rect', { x: rx - 14, y: top - 14, width: 28, height: 14, rx: 2, 'class': 'pumpe' });
      el(szene, 'text', { x: rx, y: top - 4, 'text-anchor': 'middle', 'class': 'saeule-text' }, 'Pumpe');
      // Skala am Rohr
      var st = hg ? 0.2 : 2;
      for (var m = 0; m <= HM + 1e-9; m += st){ var yy = BY - 12 - m * PXM; el(szene, 'line', { x1: rx + 8, y1: yy, x2: rx + 13, y2: yy, 'class': 'tick' }); el(szene, 'text', { x: rx + 16, y: yy + 3, 'class': 'skala' }, zahl(+m.toFixed(1)) + ' m'); }
      // Luftdruck-Pfeile auf das Becken
      for (var ax = 40; ax <= 200; ax += 40) if (Math.abs(ax - rx) > 20) pfeil(szene, ax, BY - 52, ax, BY - 25, 'pf-luft', 6);
      el(szene, 'text', { x: 296, y: BY - 58, 'text-anchor': 'end', 'class': 'bt-klein' }, 'Luftdruck ' + zahl(w.p0) + ' hPa');
      if (h * PXM > 14){ el(szene, 'line', { x1: rx - 22, y1: BY - 12, x2: rx - 22, y2: BY - 12 - h * PXM, 'class': 'hebelarm' }); el(szene, 'text', { x: rx - 26, y: BY - 12 - h * PXM / 2, 'text-anchor': 'end', 'class': 'pf-text pf-a' }, 'h = ' + sig(h) + ' m'); }
      el(szene, 'text', { x: 296, y: 30, 'text-anchor': 'end', 'class': 'bt-klein' }, ORTE[String(w.p0)]);
      el(szene, 'text', { x: 296, y: 46, 'text-anchor': 'end', 'class': 'bt-wert' }, 'innen ' + zahl(+p.toFixed(1)) + ' hPa');
      if (w.piz >= w.p0) el(szene, 'text', { x: 296, y: 62, 'text-anchor': 'end', 'class': 'bt-meldung' }, 'kein Unterdruck');
      var P = +p.toFixed(1), hh = hoehe(w, P);
      var z = '<span>' + v_('ρ') + ' · ' + v_('g') + ' · ' + v_('h') + ' = ' + p_('0') + ' − ' + p_('i') + ' = ' + zahl(w.p0) + NB + 'hPa − ' + zahl(P) + NB + 'hPa = ' + zahl(+(w.p0 - P).toFixed(1)) + NB + 'hPa</span>';
      z += '<span>' + v_('h') + ' = (' + p_('0') + ' − ' + p_('i') + ') / (' + v_('ρ') + ' · ' + v_('g') + ') = ' + zahl(+((w.p0 - P) * 100).toFixed(0)) + NB + 'Pa / (' + zahl(w.rho) + NB + 'kg/m³ · 9.81' + NB + 'm/s²) ' + ist(hh, sig(hh)) + sig(hh) + NB + 'm</span>';
      z += '<span class="sim-notiz">' + p_('i') + ': Druck der Restluft im Rohr. Der Luftdruck draussen drückt die Flüssigkeit hoch; ' + v_('p') + '<sub>i</sub> = 0 ist ein Vakuum. Luftdruck des Orts: Mittelwert.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, p0, piz, rho){ var l = s.lauf; return l && l.p0 === p0 && l.pi === piz && l.rho === rho; }
    pruefen = Leiste(fig, [
      { text: 'In Zürich: Sauge alle Luft aus dem Rohr (\\(p_i = 0\\)). Wie hoch steigt das Wasser höchstens? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 965, 0, 1000); },
        vergleich: '\\(h = \\dfrac{p_0}{\\rho \\cdot g} = \\dfrac{96\\,500\\;\\text{Pa}}{1000\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2} \\approx 9.84\\;\\text{m}\\). Höher geht es nicht: Mehr als den ganzen Luftdruck kann die Luft draussen nicht aufbringen.' },
      { text: 'Dasselbe auf dem Jungfraujoch. Wie hoch steigt das Wasser jetzt höchstens?', ok: function(s){ return hat(s, 671, 0, 1000); } },
      { text: 'Fülle das Becken mit Quecksilber (\\(13\\,600\\;\\text{kg/m}^3\\)) und sauge auf Meereshöhe alles leer. Wie hoch steht die Säule? So funktioniert das Quecksilberbarometer.', ok: function(s){ return hat(s, 1013, 0, 13600); },
        vergleich: '\\(h = \\dfrac{101\\,300\\;\\text{Pa}}{13\\,600\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2} \\approx 0.759\\;\\text{m} \\approx 760\\;\\text{mm}\\). Steigt der Luftdruck, steigt die Säule — das Barometer zeigt den Luftdruck an.' },
      { text: 'Auf Meereshöhe soll das Wasser genau \\(5\\;\\text{m}\\) hoch stehen. Welcher Innendruck? Stelle ein und sauge ab.', ok: function(s){ return hat(s, 1013, 522.5, 1000); },
        vergleich: '\\(p_0 - p_i = \\rho \\cdot g \\cdot h = 1000\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\cdot 5\\;\\text{m} = 49\\,050\\;\\text{Pa} = 490.5\\;\\text{hPa}\\), also \\(p_i = 1013\\;\\text{hPa} - 490.5\\;\\text{hPa} = 522.5\\;\\text{hPa}\\).' },
      { text: 'Ein Bauer will Grundwasser mit einer Saugpumpe aus \\(12\\;\\text{m}\\) Tiefe holen. Probiere an verschiedenen Orten, ob das geht. Begründe.', ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (l.pi === 0 && l.rho === 1000) n[l.p0] = true; }); return Object.keys(n).length >= 2; },
        vergleich: 'Es geht nirgends. Eine Saugpumpe kann nur den Druck im Rohr senken; hochgedrückt wird das Wasser vom Luftdruck. Der reicht auch im besten Fall (Vakuum, Meereshöhe) nur für rund \\(10.3\\;\\text{m}\\), in den Bergen für weniger. Für tiefere Brunnen braucht es eine Pumpe unten im Wasser, die drückt.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Hydraulische Hebebühne ----------
     Auf Knopfdruck pumpt der kleine Kolben fünfmal je 20 cm. Der Druck p = F₁ / A₁ wirkt überall
     in der Flüssigkeit; am grossen Kolben entsteht F₂ = p · A₂. Reicht F₂ für die Gewichtskraft
     des Autos, hebt es sich je Pumpstoss um s₂ = s₁ · A₁ / A₂. Kräfte an den Kolben Blau,
     Gewichtskraft Bernstein. Clipbeispiel: 200 N, 10 cm², 500 cm²; Startwerte 150 N, 10 cm², 300 cm², 1000 kg. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg);
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; ende = false; zeichnen(); });
    var t = 0, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var HUB = 5, S1 = 20;                                                     // fünf Pumpstösse zu 20 cm
    function werte(){ var F1 = B.wert('F1'), A1 = B.wert('A1'), A2 = B.wert('A2'), m = B.wert('m'), p = F1 / (A1 / 1e4), F2 = p * A2 / 1e4; return { F1: F1, A1: A1, A2: A2, m: m, p: p, F2: F2, FG: m * G, hebt: F2 >= m * G - 1e-9, s2: S1 * A1 / A2 }; }
    function fertig(w){ ende = true; lauf = { F1: w.F1, A1: w.A1, A2: w.A2, m: w.m, hebt: w.hebt, F2: w.F2, h: w.hebt ? HUB * w.s2 : 0 }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); t = Math.min(HUB, tt / 0.7); zeichnen(); if (t >= HUB){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Pumpen', function(){ ende = false; if (WENIGER){ t = HUB; fertig(werte()); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Ablassen', function(){ uhr.stop(); t = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); t = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(); B.anzeigen(); leeren(szene);
      var k = Math.floor(t), f = t - k, takt = f < 0.5 ? f / 0.5 : (1 - f) / 0.5;   // Kolben runter, dann zurück
      if (t >= HUB) takt = 0;
      var zug = w.hebt ? (k + Math.min(1, f / 0.5)) * w.s2 : 0; if (t >= HUB) zug = w.hebt ? HUB * w.s2 : 0;
      // Gefäss: links schmaler Zylinder, rechts breiter, unten verbunden
      var bl = 6 + Math.sqrt(w.A1) * 3, br = 30 + Math.sqrt(w.A2) * 3.2, xl = 60, xr = 200, by = 260, ky = 160;
      el(szene, 'path', { d: 'M' + (xl - bl / 2) + ' ' + (ky - 50) + ' L' + (xl - bl / 2) + ' ' + by + ' L' + (xr + br / 2) + ' ' + by + ' L' + (xr + br / 2) + ' ' + (ky - 50), 'class': 'gefaess' });
      var yl = ky + takt * S1 * 1.6, yr = ky - zug * 1.6;                       // 1.6 px je cm Kolbenweg
      el(szene, 'rect', { x: xl - bl / 2 + 1, y: yl, width: bl - 2, height: by - yl - 1, 'class': 'oel' });
      el(szene, 'rect', { x: xr - br / 2 + 1, y: yr, width: br - 2, height: by - yr - 1, 'class': 'oel' });
      el(szene, 'rect', { x: xl + bl / 2 - 1, y: by - 26, width: xr - br / 2 - xl - bl / 2 + 2, height: 25, 'class': 'oel' });
      el(szene, 'rect', { x: xl - bl / 2 + 1, y: yl - 6, width: bl - 2, height: 6, 'class': 'kolben' });
      el(szene, 'rect', { x: xr - br / 2 + 1, y: yr - 6, width: br - 2, height: 6, 'class': 'kolben' });
      el(szene, 'line', { x1: xl, y1: yl - 6, x2: xl, y2: yl - 40, 'class': 'stange' });
      // Auto auf dem grossen Kolben
      var ay = yr - 6;
      el(szene, 'path', { d: 'M' + (xr - 42) + ' ' + (ay - 6) + ' L' + (xr - 42) + ' ' + (ay - 18) + ' L' + (xr - 22) + ' ' + (ay - 20) + ' L' + (xr - 12) + ' ' + (ay - 32) + ' L' + (xr + 18) + ' ' + (ay - 32) + ' L' + (xr + 30) + ' ' + (ay - 20) + ' L' + (xr + 42) + ' ' + (ay - 18) + ' L' + (xr + 42) + ' ' + (ay - 6) + ' Z', 'class': 'auto' });
      el(szene, 'circle', { cx: xr - 26, cy: ay - 6, r: 6, 'class': 'rad' }); el(szene, 'circle', { cx: xr + 26, cy: ay - 6, r: 6, 'class': 'rad' });
      // Kräfte
      pfeil(szene, xl, yl - 78, xl, yl - 44, 'pf-f', 8); marke(szene, xl + 6, yl - 62, 'F', '1', 'pf-text pf-f', 'start');
      pfeil(szene, xr + 52, ay - 40, xr + 52, ay - 8, 'pf-g', 8); marke(szene, xr + 56, ay - 22, 'F', 'G', 'pf-text pf-g', 'start');
      pfeil(szene, xr - br / 2 - 10, yr + 40, xr - br / 2 - 10, yr + 4, 'pf-f', 8); marke(szene, xr - br / 2 - 14, yr + 26, 'F', '2', 'pf-text pf-f', 'end');
      el(szene, 'text', { x: 150, y: by + 16, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'p = ' + sig(w.p / 1e5) + ' bar überall in der Flüssigkeit');
      if (ende || t > 0) el(szene, 'text', { x: 296, y: 18, 'text-anchor': 'end', 'class': 'bt-meldung' }, w.hebt ? 'gehoben: ' + sig(zug) + ' cm' : (t > 0 ? 'F₂ zu klein: Das Auto bleibt stehen.' : ''));
      var z = '<span>' + v_('p') + ' = ' + F_('1') + ' / ' + v_('A') + '<sub>1</sub> = ' + zahl(w.F1) + NB + 'N / ' + zahl(w.A1 / 1e4) + NB + 'm² ' + ist(w.p, sig(w.p)) + sig(w.p) + NB + 'Pa ' + ist(w.p / 1e5, sig(w.p / 1e5)) + sig(w.p / 1e5) + NB + 'bar</span>';
      z += '<span>' + F_('2') + ' = ' + F_('1') + ' · ' + v_('A') + '<sub>2</sub> / ' + v_('A') + '<sub>1</sub> = ' + zahl(w.F1) + NB + 'N · ' + zahl(w.A2) + NB + 'cm² / ' + zahl(w.A1) + NB + 'cm² ' + ist(w.F2, sig(w.F2)) + sig(w.F2) + NB + 'N; ' + F_('G') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² ' + ist(w.FG, sig(w.FG)) + sig(w.FG) + NB + 'N</span>';
      z += '<span>' + v_('s') + '<sub>2</sub> = ' + v_('s') + '<sub>1</sub> · ' + v_('A') + '<sub>1</sub> / ' + v_('A') + '<sub>2</sub> = 20' + NB + 'cm · ' + zahl(w.A1) + NB + 'cm² / ' + zahl(w.A2) + NB + 'cm² ' + ist(w.s2, sig(w.s2)) + sig(w.s2) + NB + 'cm je Pumpstoss</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, F1, A1, A2, m){ var l = s.lauf; return l && l.F1 === F1 && l.A1 === A1 && l.A2 === A2 && l.m === m; }
    pruefen = Leiste(fig, [
      { text: 'Ein Auto mit \\(1200\\;\\text{kg}\\) soll mit \\(F_1 = 300\\;\\text{N}\\) am kleinen Kolben (\\(A_1 = 5\\;\\text{cm}^2\\)) gehoben werden. Welche Fläche \\(A_2\\) braucht es mindestens (auf \\(10\\;\\text{cm}^2\\) genau)? Stelle ein und pumpe.', ok: function(s){ return hat(s, 300, 5, 200, 1200) && s.lauf.hebt; },
        vergleich: '\\(F_2 = m \\cdot g \\approx 11\\,770\\;\\text{N}\\). Aus \\(\\dfrac{F_1}{A_1} = \\dfrac{F_2}{A_2}\\): \\(A_2 = A_1 \\cdot \\dfrac{F_2}{F_1} = 5\\;\\text{cm}^2 \\cdot \\dfrac{11\\,770\\;\\text{N}}{300\\;\\text{N}} \\approx 196\\;\\text{cm}^2\\) — auf dem Regler \\(200\\;\\text{cm}^2\\).' },
      { text: 'Gleiche Einstellung: Wie gross ist der Druck in bar, und wie hoch hebt sich das Auto nach den fünf Pumpstössen? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 300, 5, 200, 1200) && s.lauf.hebt; },
        vergleich: '\\(p = \\dfrac{300\\;\\text{N}}{0.0005\\;\\text{m}^2} = 600\\,000\\;\\text{Pa} = 6\\;\\text{bar}\\). Je Pumpstoss \\(s_2 = 20\\;\\text{cm} \\cdot \\dfrac{5\\;\\text{cm}^2}{200\\;\\text{cm}^2} = 0.5\\;\\text{cm}\\), nach fünf Stössen \\(2.5\\;\\text{cm}\\).' },
      { text: 'Mit \\(A_1 = 4\\;\\text{cm}^2\\) und \\(A_2 = 800\\;\\text{cm}^2\\): Welche kleinste Kraft \\(F_1\\) hebt einen Lieferwagen mit \\(1500\\;\\text{kg}\\) (auf \\(10\\;\\text{N}\\) genau)?', ok: function(s){ return hat(s, 80, 4, 800, 1500) && s.lauf.hebt; },
        vergleich: '\\(F_1 = F_2 \\cdot \\dfrac{A_1}{A_2} = 1500\\;\\text{kg} \\cdot 9.81\\;\\text{m/s}^2 \\cdot \\dfrac{4}{800} \\approx 73.6\\;\\text{N}\\) — auf dem Regler \\(80\\;\\text{N}\\); \\(70\\;\\text{N}\\) reichen nicht.' },
      { text: 'Hebe irgendein Auto. Vergleiche die Arbeit am kleinen Kolben mit der Hubarbeit am Auto. Was bezahlt man für die grosse Kraft? Begründe.', ok: function(s){ return s.lauf && s.lauf.hebt; },
        vergleich: 'Den Weg: Der kleine Kolben geht \\(\\dfrac{A_2}{A_1}\\)-mal so weit wie der grosse. Die Arbeit \\(F_1 \\cdot s_1 = F_2 \\cdot s_2\\) ist auf beiden Seiten gleich (ohne Reibung) — Kraft wird gewonnen, Energie nicht.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Auftrieb an der Federwaage ----------
     Ein Zylinder (V = 200 cm³, Höhe 10 cm) hängt an einer Federwaage und wird auf Knopfdruck
     bis zur eingestellten Tiefe eingetaucht. Die Waage zeigt F_G − F_A mit F_A = ρ_Fl · V_e · g.
     Im Diagramm die Anzeige über der Eintauchtiefe. Gewichtskraft Bernstein, Auftrieb Grün. Clipbeispiel: Messing in Wasser; Startwerte Aluminium, Wasser, 4 cm. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,252)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); he = 0; ende = false; zeichnen(); });
    var he = 0, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var V = 200e-6, HK = 10, WY = 150, PXCM = 6;                              // Körper 10 cm hoch, Wasser bei y = 150
    function werte(){ var hz = B.wert('he'), rk = +B.wert('stoff'), rf = +B.wert('fl'); return { hz: hz, rk: rk, rf: rf, FG: rk * V * G }; }
    function FA(w, x){ return w.rf * V * Math.min(x, HK) / HK * G; }
    function fertig(w){ ende = true; lauf = { he: w.hz, rk: w.rk, rf: w.rf, FA: FA(w, w.hz), FW: w.FG - FA(w, w.hz) }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); he = Math.min(w.hz, tt * 4); zeichnen(); if (he >= w.hz){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Eintauchen', function(){ ende = false; if (WENIGER){ var w = werte(); he = w.hz; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Herausziehen', function(){ uhr.stop(); he = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); he = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); he = x; zeichnen(); }
    };
    fig.__sim = sim;
    var NAMEN = { '2700': 'Aluminium', '8500': 'Messing', '7870': 'Eisen', '7290': 'Stoff X' };
    function zeichnen(){
      var w = werte(), fa = FA(w, he), fw = w.FG - fa;
      B.anzeigen(); leeren(szene); leeren(dia);
      // Gefäss mit Flüssigkeit (Pegelanstieg vernachlässigt)
      el(szene, 'rect', { x: 60, y: WY, width: 160, height: 90, 'class': w.rf < 900 ? 'wasser spiritus' : 'wasser' });
      el(szene, 'path', { d: 'M58 ' + (WY - 10) + ' L58 ' + (WY + 92) + ' L222 ' + (WY + 92) + ' L222 ' + (WY - 10), 'class': 'gefaess' });
      // Federwaage: Gehäuse oben, Feder bis zum Körper
      var kx = 140, unten = WY + he * PXCM, oben = unten - HK * PXCM;          // Körper
      // Die Waage wird mit dem Körper abgesenkt; die Feder dehnt sich mit der Anzeige (2 px je N)
      var dehn = 8 + fw * 2.0, fo = oben - 6 - dehn;
      el(szene, 'rect', { x: kx - 9, y: fo - 34, width: 18, height: 34, rx: 3, 'class': 'waage-gehaeuse' });
      var zz = 'M' + kx + ' ' + fo; for (var i = 1; i <= 8; i++) zz += ' L' + (kx + (i % 2 ? 6 : -6)) + ' ' + (fo + dehn * i / 8.5); zz += ' L' + kx + ' ' + (fo + dehn);
      el(szene, 'path', { d: zz, 'class': 'feder' });
      el(szene, 'line', { x1: kx, y1: fo + dehn, x2: kx, y2: oben, 'class': 'faden' });
      el(szene, 'text', { x: kx + 14, y: fo - 14, 'class': 'bt-wert' }, 'Waage: ' + sig(fw) + NB + 'N');
      el(szene, 'rect', { x: kx - 16, y: oben, width: 32, height: HK * PXCM, rx: 2, 'class': 'koerper' });
      el(szene, 'text', { x: kx, y: oben + HK * PXCM / 2 + 4, 'text-anchor': 'middle', 'class': 'klotz-zahl' }, NAMEN[String(w.rk)]);
      // Kräfte am Körper: F_G nach unten (rechts), F_A nach oben (links), Massstab 6 px je N
      var k = 45 / w.FG;                                                     // Gewichtskraft immer 45 px, Auftrieb im selben Massstab
      pfeil(szene, kx + 24, oben + 10, kx + 24, oben + 10 + w.FG * k, 'pf-g', 7); marke(szene, kx + 29, oben + 14 + w.FG * k / 2, 'F', 'G', 'pf-text pf-g', 'start');
      if (fa * k > 3){ pfeil(szene, kx - 24, unten, kx - 24, unten - fa * k, 'pf-n', 7); marke(szene, kx - 29, unten - fa * k / 2, 'F', 'A', 'pf-text pf-n', 'end'); }
      if (he > 0.2) el(szene, 'text', { x: 228, y: WY + Math.min(he, 14) * PXCM / 2 + 4, 'class': 'bt-klein' }, 'eingetaucht ' + zahl(+he.toFixed(1)) + ' cm');
      // Diagramm: Anzeige über der Eintauchtiefe
      var sk = skala(w.FG * 1.15);
      K = Achsen(dia, { w: 300, h: 110, x0: -0.8, x1: 15.5, y0: sk.y0, y1: sk.y1, sx: 1, sy: sk.sy, xm: [2, 4, 6, 8, 10, 12, 14], ym: sk.ym, xname: 'h_e [cm]', yname: 'F [N]' });
      if (he > 0){ K.kurve(function(x){ return w.FG - FA(w, x); }, 'kurve-waage', 0, he); K.kurve(function(x){ return FA(w, x); }, 'kurve-fa', 0, he); }
      K.punkt(he, fw, 'p-waage'); K.punkt(he, fa, 'p-fa');
      stext(K.ebene, { x: 296, y: 12, 'text-anchor': 'end', 'class': 'legende l-waage' }, '— Anzeige der Waage');
      stext(K.ebene, { x: 296, y: 24, 'text-anchor': 'end', 'class': 'legende l-fa' }, '- - F_A');
      var Ve = V * 1e6 * Math.min(+he.toFixed(1), HK) / HK, fA = w.rf * Ve * 1e-6 * G;
      var z = '<span>' + F_('A') + ' = ' + v_('ρ') + '<sub>Fl</sub> · ' + v_('V') + '<sub>e</sub> · ' + v_('g') + ' = ' + zahl(w.rf) + NB + 'kg/m³ · ' + zahl(+Ve.toFixed(1)) + NB + 'cm³ · 9.81' + NB + 'm/s² ' + ist(fA, sig(fA)) + sig(fA) + NB + 'N</span>';
      z += '<span>Anzeige = ' + F_('G') + ' − ' + F_('A') + ' = ' + sig(w.FG) + NB + 'N − ' + sig(fA) + NB + 'N ' + ist(w.FG - fA, sig(w.FG - fA)) + sig(w.FG - fA) + NB + 'N</span>';
      z += '<span class="sim-notiz">' + v_('V') + '<sub>e</sub>: eingetauchtes Volumen (Körper: 200' + NB + 'cm³, 10' + NB + 'cm hoch; 1' + NB + 'cm³ = 10⁻⁶' + NB + 'm³). Pfeile im Massstab der Gewichtskraft. ' + F_('G') + ' = ' + v_('ρ') + '<sub>K</sub> · ' + v_('V') + ' · ' + v_('g') + ' ' + ist(w.FG, sig(w.FG)) + sig(w.FG) + NB + 'N.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, h, rk, rf){ var l = s.lauf; return l && l.he === h && l.rk === rk && l.rf === rf; }
    pruefen = Leiste(fig, [
      { text: 'Aluminium in Wasser: Tauche den Körper ganz ein (\\(10\\;\\text{cm}\\)). Wie gross ist der Auftrieb? Notiere, dann vergleiche mit der Anzeige.', ok: function(s){ return hat(s, 10, 2700, 1000); },
        vergleich: '\\(F_A = \\rho_{Fl} \\cdot V_e \\cdot g = 1000\\;\\text{kg/m}^3 \\cdot 0.0002\\;\\text{m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\approx 1.96\\;\\text{N}\\) — genau das Gewicht von \\(200\\;\\text{cm}^3\\) Wasser. Die Waage zeigt \\(5.30\\;\\text{N} - 1.96\\;\\text{N} \\approx 3.34\\;\\text{N}\\).' },
      { text: 'Tauche denselben Körper nur halb ein (\\(5\\;\\text{cm}\\)). Wie gross ist der Auftrieb jetzt? Begründe.', ok: function(s){ return hat(s, 5, 2700, 1000); },
        vergleich: 'Halb so gross, rund \\(0.98\\;\\text{N}\\): Der Auftrieb hängt am eingetauchten Volumen, und davon ist nur die Hälfte im Wasser.' },
      { text: 'Tauche den Körper \\(14\\;\\text{cm}\\) tief. Ab welcher Tiefe bleibt die Anzeige im Diagramm gleich? Warum wird der Auftrieb nicht noch grösser? Begründe.', ok: function(s){ return s.lauf && s.lauf.he === 14; },
        vergleich: 'Ab \\(10\\;\\text{cm}\\), wenn der Körper ganz unter Wasser ist. Danach ändert sich das verdrängte Volumen nicht mehr — die Tiefe spielt für den Auftrieb keine Rolle.' },
      { text: 'Tauche den Aluminiumkörper ganz in Wasser und ganz in Spiritus. Wo ist der Auftrieb kleiner, und warum? Begründe.', ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (l.rk === 2700 && l.he >= 10) n[l.rf] = true; }); return n[1000] && n[790]; },
        vergleich: 'In Spiritus (\\(790\\;\\text{kg/m}^3\\)): Das verdrängte Volumen ist gleich, aber die verdrängte Flüssigkeit ist leichter. \\(F_A = \\rho_{Fl} \\cdot V_e \\cdot g\\) wird mit \\(\\rho_{Fl}\\) kleiner: \\(1.55\\;\\text{N}\\) statt \\(1.96\\;\\text{N}\\).' },
      { text: 'Stoff X: Miss die Anzeige an der Luft und ganz in Wasser. Bestimme daraus die Dichte von Stoff X. Notiere, dann vergleiche.', ok: function(s){ var a = false, b = false; s.laeufe.forEach(function(l){ if (l.rk === 7290 && l.he === 0) a = true; if (l.rk === 7290 && l.he >= 10 && l.rf === 1000) b = true; }); return a && b; },
        vergleich: 'An der Luft \\(F_G \\approx 14.3\\;\\text{N}\\), in Wasser \\(\\approx 12.3\\;\\text{N}\\): \\(F_A \\approx 1.96\\;\\text{N}\\), also \\(V = \\dfrac{F_A}{\\rho_W \\cdot g} = 200\\;\\text{cm}^3\\). \\(\\rho = \\dfrac{F_G}{V \\cdot g} = \\dfrac{F_G}{F_A} \\cdot \\rho_W \\approx 7290\\;\\text{kg/m}^3\\) — das ist Zinn.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 6: Schwimmen, Schweben, Sinken ----------
     Ein Würfel (10 cm) wird auf Knopfdruck an der Oberfläche losgelassen. Gewichtskraft,
     Auftrieb (nach eingetauchtem Volumen) und eine Dämpfung bestimmen die Bewegung; er pendelt
     sich ein (schwimmt), bleibt stehen, wo er ist (schwebt), oder sinkt auf den Boden. Im
     Diagramm die Eintauchtiefe über der Zeit. Clipbeispiel: Eis 917 in Wasser, Eisberg;
     Startwerte 400 kg/m³, Süsswasser. */
  (function(){
    var fig = document.getElementById('sim6'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,206)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); los(); zeichnen(); });
    var y = 0, vy = 0, spur = [], tz = 0, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var A = 10, WY = 50, PXCM = 4, TIEF = 30, TMAX = 6;                     // Würfel 10 cm, Wasser 30 cm tief
    function werte(){ var rk = B.wert('rk'), rf = +B.wert('fl'); return { rk: rk, rf: rf, anteil: rk / rf }; }
    function los(){ y = 0; vy = 0; spur = []; tz = 0; ende = false; }
    function zustandEnde(w){ return w.rk < w.rf - 1e-9 ? 'schwimmt' : (Math.abs(w.rk - w.rf) < 1e-9 ? 'schwebt' : 'sinkt'); }
    function fertig(w){ ende = true; lauf = { rk: w.rk, rf: w.rf, art: zustandEnde(w), he: Math.min(y, A) }; laeufe.push(lauf); }
    // y: Eintauchtiefe der Unterseite in cm (0 = Unterseite an der Oberfläche)
    function schritt(w, dt){
      var Ve = Math.max(0, Math.min(y, A)) / A, a = 981 * (1 - (w.rf / w.rk) * Ve) - 6 * vy;   // cm/s², gedämpft
      vy += a * dt; y += vy * dt;
      if (y >= TIEF){ y = TIEF; vy = 0; }
    }
    var tl = 0;
    var uhr = Uhr(function(tt){
      var w = werte(), dt = Math.min(0.03, tt - tl); tl = tt;
      for (var i = 0; i < 6; i++) schritt(w, dt / 6);
      tz = tt; spur.push([tt, Math.min(y, A + 0.001) === y ? y : y]);
      zeichnen();
      if (tt >= TMAX){ fertig(w); zeichnen(); return false; }
    });
    function sofort(w){ los(); for (var t = 0; t < TMAX; t += 0.005){ for (var i = 0; i < 1; i++) schritt(w, 0.005); if (Math.round(t / 0.005) % 6 === 0) spur.push([t, y]); } tz = TMAX; }
    aktionen(fig, [['start', '▶ Loslassen', function(){ uhr.stop(); los(); tl = 0; if (WENIGER){ var w = werte(); sofort(w); fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Herausnehmen', function(){ uhr.stop(); los(); zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); los(); B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; ende = false; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); var w = werte(); sofort(w); fertig(w); zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(); B.anzeigen(); leeren(szene); leeren(dia);
      wasser(szene, 40, WY, 200, TIEF * PXCM, w.rf > 1100 ? 'wasser salzig' : (w.rf < 900 ? 'wasser spiritus' : 'wasser'));
      el(szene, 'path', { d: 'M38 ' + (WY - 30) + ' L38 ' + (WY + TIEF * PXCM + 2) + ' L242 ' + (WY + TIEF * PXCM + 2) + ' L242 ' + (WY - 30), 'class': 'gefaess' });
      var cx = 140, unter = WY + y * PXCM, ob = unter - A * PXCM;
      el(szene, 'rect', { x: cx - A * PXCM / 2, y: ob, width: A * PXCM, height: A * PXCM, 'class': 'koerper holz' });
      el(szene, 'line', { x1: 38, y1: WY, x2: 242, y2: WY, 'class': 'wasserlinie' });
      var Ve = Math.max(0, Math.min(y, A)) / A, FG = w.rk * 0.001 * G, FA = w.rf * 0.001 * Ve * G, k = 30 / FG;   // Würfel 1 l; F_G immer 30 px
      pfeil(szene, cx + 10, ob + 20, cx + 10, ob + 20 + FG * k, 'pf-g', 7); marke(szene, cx + 15, ob + 24 + FG * k / 2, 'F', 'G', 'pf-text pf-g', 'start');
      if (FA * k > 3){ pfeil(szene, cx - 10, unter - 2, cx - 10, unter - 2 - FA * k, 'pf-n', 7); marke(szene, cx - 15, unter - FA * k / 2, 'F', 'A', 'pf-text pf-n', 'end'); }
      if (ende && lauf) el(szene, 'text', { x: 296, y: 16, 'text-anchor': 'end', 'class': 'bt-meldung' }, lauf.art === 'schwimmt' ? 'Er schwimmt: ' + sig(100 * w.anteil) + ' % unter Wasser.' : (lauf.art === 'schwebt' ? 'Er schwebt.' : 'Er sinkt auf den Boden.'));
      // Diagramm: Eintauchtiefe der Unterseite über der Zeit
      K = Achsen(dia, { w: 300, h: 110, x0: -0.3, x1: 6.4, y0: -3, y1: 32, sx: 1, sy: 5, xm: [1, 2, 3, 4, 5, 6], ym: [10, 20, 30], xname: 't [s]', yname: 'Tiefe [cm]' });
      K.kurve(function(){ return A; }, 'vorher', 0, 6.2);
      if (spur.length > 1){ var d = ''; spur.forEach(function(q, i){ d += (i ? ' L' : 'M') + K.X(q[0]).toFixed(1) + ' ' + K.Y(Math.min(q[1], 31)).toFixed(1); }); el(K.ebene, 'path', { d: d, 'class': 'kurve-tiefe', 'clip-path': K.clip }); }
      stext(K.ebene, { x: 296, y: 12, 'text-anchor': 'end', 'class': 'legende' }, '- - Würfel ganz eingetaucht (10 cm)');
      var z = '<span>Schwimmt: ' + v_('V') + '<sub>e</sub> / ' + v_('V') + ' = ' + v_('ρ') + '<sub>K</sub> / ' + v_('ρ') + '<sub>Fl</sub> = ' + zahl(w.rk) + NB + 'kg/m³ / ' + zahl(w.rf) + NB + 'kg/m³ ' + ist(w.anteil, sig(w.anteil)) + sig(w.anteil) + '</span>';
      z += '<span>' + F_('G') + ' = ' + v_('ρ') + '<sub>K</sub> · ' + v_('V') + ' · ' + v_('g') + ' ' + ist(FG, sig(FG)) + sig(FG) + NB + 'N; ' + F_('A') + ' = ' + v_('ρ') + '<sub>Fl</sub> · ' + v_('V') + '<sub>e</sub> · ' + v_('g') + ' ' + ist(FA, sig(FA)) + sig(FA) + NB + 'N</span>';
      z += '<span class="sim-notiz">Würfel: 10' + NB + 'cm Kante, 1' + NB + 'l. Die Gleichung oben gilt nur, wenn er schwimmt (' + v_('ρ') + '<sub>K</sub> < ' + v_('ρ') + '<sub>Fl</sub>). Das Wasser bremst die Bewegung. Pfeile im Massstab der Gewichtskraft.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, rk, rf){ var l = s.lauf; return l && l.rk === rk && l.rf === rf; }
    pruefen = Leiste(fig, [
      { text: 'Ein Würfel aus Kiefernholz (\\(520\\;\\text{kg/m}^3\\)) in Süsswasser: Lass ihn los. Welcher Anteil taucht ein, und wie tief (Kante \\(10\\;\\text{cm}\\))? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 520, 1000); },
        vergleich: 'Er schwimmt, \\(F_A = F_G\\): \\(\\dfrac{V_e}{V} = \\dfrac{\\rho_K}{\\rho_{Fl}} = \\dfrac{520}{1000} = 0.52\\). Er taucht \\(5.2\\;\\text{cm}\\) tief ein.' },
      { text: 'Finde die Dichte, bei der der Würfel im Meerwasser schwebt, und lass ihn los.', ok: function(s){ return hat(s, 1025, 1025); },
        vergleich: 'Bei \\(\\rho_K = \\rho_{Fl} = 1025\\;\\text{kg/m}^3\\): Ganz eingetaucht ist der Auftrieb genau so gross wie die Gewichtskraft — er bleibt in jeder Tiefe stehen.' },
      { text: 'Ein Eiswürfel (\\(920\\;\\text{kg/m}^3\\)): Lass ihn in Süsswasser und in Spiritus los. Was geschieht? Begründe.', ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (l.rk === 920) n[l.rf] = true; }); return n[1000] && n[790]; },
        vergleich: 'In Wasser schwimmt er (\\(920 < 1000\\)), in Spiritus sinkt er (\\(920 > 790\\)). Ob ein Körper schwimmt, entscheidet der Vergleich seiner Dichte mit der Dichte der Flüssigkeit — nicht seine Masse.' },
      { text: 'Ein Würfel taucht in Süsswasser genau \\(8.5\\;\\text{cm}\\) tief ein. Welche Dichte hat er? Stelle ein und prüfe.', ok: function(s){ return hat(s, 850, 1000); },
        vergleich: '\\(\\rho_K = \\rho_{Fl} \\cdot \\dfrac{V_e}{V} = 1000\\;\\text{kg/m}^3 \\cdot \\dfrac{8.5\\;\\text{cm}}{10\\;\\text{cm}} = 850\\;\\text{kg/m}^3\\).' }
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


    var G = 9.81;
    function paar(l, a, b){ return l.some(function(p){ return p[0] === a && p[1] === b; }); }

    function grad(a){ return a * Math.PI / 180; }
    // Fehlermuster müssen verschiedene Zahlen ergeben (HOWTO §15): alle Werte paarweise 2 % auseinander
    function verschieden(l){ for (var i = 0; i < l.length; i++) for (var j = i + 1; j < l.length; j++) if (Math.abs(l[i] - l[j]) <= 0.02 * Math.max(Math.abs(l[i]), Math.abs(l[j]))) return false; return true; }

    var FL = [['Wasser', 1000], ['Meerwasser', 1025], ['Speiseöl', 920], ['Spiritus', 790]];
    var TYPEN = {
      /* ----- Kapitel 1: Druck ----- */
      'druck': { felder: ['p'], muster: '<i>p</i> = {p} kPa',
        neu: function(){
          var c, m, A;
          do { c = zufall([['Ein Koffer', [12, 18, 25]], ['Eine Person', [55, 68, 85]], ['Ein Kühlschrank', [65, 90]], ['Ein Klavier', [250, 320]]]);
               m = zufall(c[1]); A = zufall([15, 40, 120, 300, 800, 2500]); } while (m * G / (A / 1e4) > 2e6 || m * G / (A / 1e4) < 1000);   // 1 kPa bis 2 MPa
          return { p: m * G / (A / 1e4) / 1000, m: m, A: A,
            text: c[0] + ' mit \\(' + ein(m, 'kg') + '\\) steht auf einer Auflagefläche von zusammen \\(' + tz(A) + '\\;\\text{cm}^2\\). Wie gross ist der Druck auf den Boden?' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (nah(e.p, A.p / 1e4) || nah(e.p, A.p * 1e4)) return 'Die Fläche in Quadratmeter umrechnen: \\(1\\;\\text{cm}^2 = 10^{-4}\\;\\text{m}^2\\).';
          if (nah(e.p, A.p / G)) return 'Druck ist Kraft je Fläche — zuerst die Gewichtskraft \\(F = m \\cdot g\\).';
          if (nah(e.p, A.p * 1000)) return 'Das ist der Druck in Pascal. Gefragt sind Kilopascal.';
          return '\\(p = \\dfrac{F}{A} = \\dfrac{m \\cdot g}{A}\\), \\(A\\) in m², Ergebnis in kPa.'; },
        fehler: function(A){ return [[{ p: String(A.p / 1e4) }, 'Quadratmeter'], [{ p: String(A.p / G) }, 'Gewichtskraft'], [{ p: String(A.p * 1000) }, 'Pascal']]; },
        loesung: function(A){ return 'p = \\dfrac{m \\cdot g}{A} = \\dfrac{' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2}{' + tz(A.A / 1e4) + '\\;\\text{m}^2} ' + erg(A.p * 1000, 'Pa') + ' ' + erg(A.p, 'kPa'); } },
      'flaeche': { felder: ['A'], muster: '<i>A</i> = {A} cm²',
        neu: function(){
          var F, p;
          do { F = zufall([150, 400, 650, 900, 2400]); p = zufall([2, 5, 8, 15, 40, 120]); } while (!verschieden([F / p * 10, F / p / 1e3, F * p, F / p * 1e4]));
          var c = zufall(['Ein Schneeschuh soll', 'Die Füsse eines Gestells sollen', 'Ein Brett auf dem Eis soll']);
          return { A: F / (p * 1000) * 1e4, F: F, p: p,
            text: c + ' eine Kraft von \\(' + ein(F, 'N') + '\\) so verteilen, dass der Druck höchstens \\(' + ein(p, 'kPa') + '\\) beträgt. Wie gross muss die Fläche mindestens sein?' }; },
        pruefen: function(A, e){
          if (nah(e.A, A.A)) return null;
          if (nah(e.A, A.A / 1e4)) return 'Das ist die Fläche in Quadratmeter. Gefragt sind cm²: \\(1\\;\\text{m}^2 = 10\\,000\\;\\text{cm}^2\\).';
          if (nah(e.A, A.A * 1000) || nah(e.A, A.A / 1000)) return 'Den Druck in Pascal einsetzen: \\(1\\;\\text{kPa} = 1000\\;\\text{Pa}\\).';
          if (nah(e.A, A.F * A.p)) return 'Umstellen: \\(A = \\dfrac{F}{p}\\), nicht mal.';
          return '\\(A = \\dfrac{F}{p}\\) mit \\(p\\) in Pa, Ergebnis in m², dann in cm².'; },
        fehler: function(A){ return [[{ A: String(A.A / 1e4) }, 'Quadratmeter'], [{ A: String(A.A * 1000) }, 'Pascal'], [{ A: String(A.F * A.p) }, 'Umstellen']]; },
        loesung: function(A){ return 'A = \\dfrac{F}{p} = \\dfrac{' + ein(A.F, 'N') + '}{' + tz(A.p * 1000) + '\\;\\text{Pa}} ' + erg(A.A / 1e4, 'm^2').replace('\\text{m^2}', '\\text{m}^2') + ' ' + erg(A.A, 'cm^2').replace('\\text{cm^2}', '\\text{cm}^2'); } },
      'einheiten': { felder: ['x'], muster: function(A){ return '{x} ' + A.nach; },
        neu: function(){
          var E = { 'Pa': 1, 'hPa': 100, 'kPa': 1000, 'bar': 1e5, 'mbar': 100 }, von, nach, w;
          var paare = [['bar', 'Pa'], ['Pa', 'bar'], ['hPa', 'bar'], ['bar', 'hPa'], ['kPa', 'hPa'], ['mbar', 'Pa'], ['kPa', 'bar'], ['Pa', 'hPa']];
          var q = zufall(paare); von = q[0]; nach = q[1];
          w = zufall(von === 'Pa' ? [850, 2400, 56000, 310000] : von === 'bar' ? [0.35, 2.4, 6, 0.012] : [3.5, 45, 260, 1013]);
          return { x: w * E[von] / E[nach], w: w, von: von, nach: nach, text: 'Rechne um: \\(' + tz(w) + '\\;\\text{' + von + '}\\) in \\(\\text{' + nach + '}\\).' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          for (var k = -6; k <= 6; k++) if (k && nah(e.x, A.x * Math.pow(10, k))) return 'Umrechnung prüfen: \\(1\\;\\text{bar} = 1000\\;\\text{hPa} = 100\\,000\\;\\text{Pa}\\), \\(1\\;\\text{hPa} = 1\\;\\text{mbar} = 100\\;\\text{Pa}\\), \\(1\\;\\text{kPa} = 1000\\;\\text{Pa}\\).';
          return 'Zuerst in Pascal, dann in die Zieleinheit.'; },
        fehler: function(A){ return [[{ x: String(A.x * 10) }, 'Umrechnung'], [{ x: String(A.x / 100) }, 'Umrechnung']]; },
        loesung: function(A){ return tz(A.w) + '\\;\\text{' + A.von + '} = ' + tz(+A.x.toPrecision(6)) + '\\;\\text{' + A.nach + '}'; } },

      /* ----- Kapitel 2: Schweredruck ----- */
      'schweredruck': { felder: ['p'], muster: '<i>p</i><sub>S</sub> = {p} kPa',
        neu: function(){
          var f, h, cm;
          do { f = zufall(FL); cm = Math.random() < 0.4; h = cm ? zufall([35, 60, 85, 140]) : zufall([2.5, 4, 7, 12, 18, 35]); } while (!cm && f[1] === 1000 && h === 10);
          var hm = cm ? h / 100 : h;
          return { p: f[1] * G * hm / 1000, rho: f[1], h: h, cm: cm, hm: hm,
            text: 'Wie gross ist der Schweredruck in \\(' + ein(h, cm ? 'cm' : 'm') + '\\) Tiefe in ' + f[0] + ' (\\(\\rho = ' + ein(f[1], 'kg/m^3').replace('\\text{kg/m^3}', '\\text{kg/m}^3') + '\\))?' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (A.cm && nah(e.p, A.p * 100)) return 'Die Tiefe in Meter umrechnen: \\(' + ein(A.h, 'cm') + ' = ' + ein(A.hm, 'm') + '\\).';
          if (nah(e.p, A.p / G)) return '\\(g\\) fehlt: \\(p_S = \\rho \\cdot g \\cdot h\\).';
          if (nah(e.p, A.p * 1000)) return 'Das ist Pascal. Gefragt sind Kilopascal.';
          if (nah(e.p, A.p + 101.3)) return 'Gefragt ist nur der Schweredruck, ohne Luftdruck.';
          return '\\(p_S = \\rho \\cdot g \\cdot h\\), \\(h\\) in m, Ergebnis in kPa.'; },
        fehler: function(A){ var l = [[{ p: String(A.p / G) }, 'fehlt'], [{ p: String(A.p * 1000) }, 'Pascal'], [{ p: String(A.p + 101.3) }, 'Luftdruck']]; if (A.cm) l.push([{ p: String(A.p * 100) }, 'Meter']); return l; },
        loesung: function(A){ return 'p_S = \\rho \\cdot g \\cdot h = ' + tz(A.rho) + '\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.hm, 'm') + ' ' + erg(A.p, 'kPa'); } },
      'tiefe': { felder: ['h'], muster: '<i>h</i> = {h} m',
        neu: function(){
          var f, p;
          do { f = zufall(FL); p = zufall([25, 60, 150, 240, 500]); } while (f[1] === 1000 && p === 200);
          return { h: p * 1000 / (f[1] * G), p: p, rho: f[1],
            text: 'In ' + f[0] + ' (\\(\\rho = ' + tz(f[1]) + '\\;\\text{kg/m}^3\\)) misst ein Sensor einen Schweredruck von \\(' + ein(p, 'kPa') + '\\). Wie tief ist er?' }; },
        pruefen: function(A, e){
          if (nah(e.h, A.h)) return null;
          if (nah(e.h, A.h / 1000)) return 'Den Druck in Pascal einsetzen: \\(1\\;\\text{kPa} = 1000\\;\\text{Pa}\\).';
          if (nah(e.h, A.h * G)) return '\\(g\\) fehlt im Nenner: \\(h = \\dfrac{p_S}{\\rho \\cdot g}\\).';
          return '\\(h = \\dfrac{p_S}{\\rho \\cdot g}\\), \\(p_S\\) in Pa.'; },
        fehler: function(A){ return [[{ h: String(A.h / 1000) }, 'Pascal'], [{ h: String(A.h * G) }, 'fehlt']]; },
        loesung: function(A){ return 'h = \\dfrac{p_S}{\\rho \\cdot g} = \\dfrac{' + tz(A.p * 1000) + '\\;\\text{Pa}}{' + tz(A.rho) + '\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2} ' + erg(A.h, 'm'); } },
      'gesamtdruck': { felder: ['p'], muster: '<i>p</i> = {p} bar',
        neu: function(){
          var f = zufall([['einem Bergsee', 1000, 841, 'Luftdruck dort \\(841\\;\\text{hPa}\\)'], ['einem See im Mittelland', 1000, 965, 'Luftdruck dort \\(965\\;\\text{hPa}\\)'], ['dem Meer', 1025, 1013, 'Luftdruck \\(1013\\;\\text{hPa}\\)']]);
          var h; do { h = zufall([4, 8, 12, 22, 28, 42]); } while ((f[1] === 1000 && (h === 15 || h === 10)) || (f[1] === 1025 && h === 20));
          return { p: (f[2] * 100 + f[1] * G * h) / 1e5, p0: f[2], rho: f[1], h: h,
            text: 'Eine Taucherin ist in \\(' + ein(h, 'm') + '\\) Tiefe in ' + f[0] + ' (' + f[3] + ', \\(\\rho = ' + tz(f[1]) + '\\;\\text{kg/m}^3\\)). Wie gross ist der Gesamtdruck auf sie?' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (nah(e.p, A.rho * G * A.h / 1e5)) return 'Das ist nur der Schweredruck. Der Luftdruck an der Oberfläche kommt dazu: \\(p = p_0 + p_S\\).';
          if (nah(e.p, (101300 + A.rho * G * A.h) / 1e5) && A.p0 !== 1013) return 'Der Luftdruck an diesem Ort ist nicht \\(1013\\;\\text{hPa}\\).';
          if (nah(e.p, A.p * 1e5) || nah(e.p, A.p * 1000)) return 'Gefragt ist bar: \\(1\\;\\text{bar} = 100\\,000\\;\\text{Pa} = 1000\\;\\text{hPa}\\).';
          return '\\(p = p_0 + \\rho \\cdot g \\cdot h\\), alles in Pa, dann in bar.'; },
        fehler: function(A){ var l = [[{ p: String(A.rho * G * A.h / 1e5) }, 'Luftdruck'], [{ p: String(A.p * 1e5) }, 'bar']]; if (A.p0 !== 1013) l.push([{ p: String((101300 + A.rho * G * A.h) / 1e5) }, 'diesem Ort']); return l; },
        loesung: function(A){ return 'p = p_0 + \\rho \\cdot g \\cdot h = ' + tz(A.p0 * 100) + '\\;\\text{Pa} + ' + tz(A.rho) + '\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + ' ' + erg(A.p, 'bar'); } },

      /* ----- Kapitel 3: Luftdruck ----- */
      'saughoehe': { felder: ['h'], muster: '<i>h</i> = {h} m',
        neu: function(){
          var o = zufall([['in Basel', 975], ['in St. Moritz', 820], ['auf dem Säntis', 750], ['in Lugano', 980]]), f = zufall([['Wasser', 1000], ['Speiseöl', 920], ['Spiritus', 790]]);
          return { h: o[1] * 100 / (f[1] * G), p0: o[1], rho: f[1],
            text: 'Wie hoch kann eine Saugpumpe ' + f[0] + ' (\\(' + tz(f[1]) + '\\;\\text{kg/m}^3\\)) ' + o[0] + ' höchstens ansaugen? Luftdruck dort: \\(' + ein(o[1], 'hPa') + '\\).' }; },
        pruefen: function(A, e){
          if (nah(e.h, A.h)) return null;
          if (nah(e.h, A.h / 100)) return 'Den Luftdruck in Pascal einsetzen: \\(1\\;\\text{hPa} = 100\\;\\text{Pa}\\).';
          if (nah(e.h, A.h * G)) return '\\(g\\) fehlt: \\(h = \\dfrac{p_0}{\\rho \\cdot g}\\).';
          return 'Höchstens bis der ganze Luftdruck die Säule trägt: \\(\\rho \\cdot g \\cdot h = p_0\\).'; },
        fehler: function(A){ return [[{ h: String(A.h / 100) }, 'Pascal'], [{ h: String(A.h * G) }, 'fehlt']]; },
        loesung: function(A){ return '\\rho \\cdot g \\cdot h = p_0,\\quad h = \\dfrac{' + tz(A.p0 * 100) + '\\;\\text{Pa}}{' + tz(A.rho) + '\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2} ' + erg(A.h, 'm'); } },
      'unterdruck': { felder: ['h'], muster: '<i>h</i> = {h} cm',
        neu: function(){
          var p0 = zufall([1013, 965, 990]), d = zufall([8, 15, 25, 40]), pi = p0 - d;
          return { h: d * 100 / (1000 * G) * 100, p0: p0, pi: pi, d: d,
            text: 'Beim Trinken mit einem Strohhalm senkst du den Druck im Mund auf \\(' + ein(pi, 'hPa') + '\\); draussen herrschen \\(' + ein(p0, 'hPa') + '\\). Wie hoch kann das Getränk (Dichte wie Wasser) im Halm höchstens steigen?' }; },
        pruefen: function(A, e){
          if (nah(e.h, A.h)) return null;
          if (nah(e.h, A.pi * 100 / (1000 * G) * 100) || nah(e.h, A.p0 * 100 / (1000 * G) * 100)) return 'Es zählt der Unterschied zwischen aussen und innen: \\(p_0 - p_i\\).';
          if (nah(e.h, A.h / 100)) return 'Das ist in Meter. Gefragt sind Zentimeter.';
          if (nah(e.h, A.h / 100 / 100)) return 'Den Druckunterschied in Pascal einsetzen, das Ergebnis in cm.';
          return '\\(\\rho \\cdot g \\cdot h = p_0 - p_i\\).'; },
        fehler: function(A){ return [[{ h: String(A.pi * 100 / (1000 * G) * 100) }, 'Unterschied'], [{ h: String(A.h / 100) }, 'Meter']]; },
        loesung: function(A){ return 'h = \\dfrac{p_0 - p_i}{\\rho \\cdot g} = \\dfrac{' + tz(A.d * 100) + '\\;\\text{Pa}}{1000\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2} ' + erg(A.h / 100, 'm') + ' ' + erg(A.h, 'cm'); } },
      'barometer': { felder: ['p'], muster: '<i>p</i><sub>0</sub> = {p} hPa',
        neu: function(){
          var mm = zufall([720, 735, 748, 771, 690, 642]);
          return { p: 13600 * G * mm / 1000 / 100, mm: mm,
            text: 'In einem Quecksilberbarometer (\\(\\rho = 13\\,600\\;\\text{kg/m}^3\\)) steht die Säule \\(' + ein(mm, 'mm') + '\\) hoch. Wie gross ist der Luftdruck?' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (nah(e.p, A.p * 1000) || nah(e.p, A.p * 100000)) return 'Die Höhe in Meter einsetzen: \\(' + ein(A.mm, 'mm') + ' = ' + ein(A.mm / 1000, 'm') + '\\), Ergebnis in hPa.';
          if (nah(e.p, A.p * 100)) return 'Das ist Pascal. Gefragt sind Hektopascal: durch 100.';
          if (nah(e.p, A.p / G)) return '\\(g\\) fehlt: \\(p_0 = \\rho \\cdot g \\cdot h\\).';
          return 'Die Säule hält dem Luftdruck das Gleichgewicht: \\(p_0 = \\rho \\cdot g \\cdot h\\).'; },
        fehler: function(A){ return [[{ p: String(A.p * 1000) }, 'Meter'], [{ p: String(A.p * 100) }, 'Hektopascal'], [{ p: String(A.p / G) }, 'fehlt']]; },
        loesung: function(A){ return 'p_0 = \\rho \\cdot g \\cdot h = 13\\,600\\;\\text{kg/m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.mm / 1000, 'm') + ' ' + erg(A.p * 100, 'Pa') + ' ' + erg(A.p, 'hPa'); } },

      /* ----- Kapitel 4: Pascal ----- */
      'presse': { felder: ['F'], muster: '<i>F</i><sub>2</sub> = {F} N',
        neu: function(){
          var F1, A1, A2;
          do { F1 = zufall([40, 120, 250, 380]); A1 = zufall([2, 3, 6, 12]); A2 = zufall([60, 150, 450, 900]); } while (F1 * A2 / A1 > 60000 || !verschieden([F1 * A2 / A1, F1 * A1 / A2, F1 * A2, F1]));
          return { F: F1 * A2 / A1, F1: F1, A1: A1, A2: A2,
            text: 'Eine hydraulische Presse: Am kleinen Kolben (\\(A_1 = ' + tz(A1) + '\\;\\text{cm}^2\\)) drückt eine Kraft von \\(' + ein(F1, 'N') + '\\). Welche Kraft entsteht am grossen Kolben (\\(A_2 = ' + tz(A2) + '\\;\\text{cm}^2\\))?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.F1 * A.A1 / A.A2)) return 'Umgekehrt: Am grossen Kolben entsteht die grosse Kraft. \\(\\dfrac{F_1}{A_1} = \\dfrac{F_2}{A_2}\\).';
          if (nah(e.F, A.F1)) return 'Gleich ist der Druck, nicht die Kraft.';
          return 'Der Druck ist überall gleich: \\(F_2 = F_1 \\cdot \\dfrac{A_2}{A_1}\\).'; },
        fehler: function(A){ return [[{ F: String(A.F1 * A.A1 / A.A2) }, 'Umgekehrt'], [{ F: String(A.F1) }, 'Druck']]; },
        loesung: function(A){ return 'F_2 = F_1 \\cdot \\dfrac{A_2}{A_1} = ' + ein(A.F1, 'N') + ' \\cdot \\dfrac{' + tz(A.A2) + '\\;\\text{cm}^2}{' + tz(A.A1) + '\\;\\text{cm}^2} ' + erg(A.F, 'N'); } },
      'kolbenweg': { felder: ['s'], muster: function(A){ return A.art === 2 ? '<i>s</i><sub>2</sub> = {s} cm' : '<i>s</i><sub>1</sub> = {s} cm'; },
        neu: function(){
          var A1 = zufall([2, 4, 5, 8]), A2 = zufall([80, 120, 300, 500]);
          if (Math.random() < 0.5){ var s1 = zufall([12, 15, 25, 30]); return { art: 2, s: s1 * A1 / A2, s1: s1, A1: A1, A2: A2,
            text: 'Der kleine Kolben einer Presse (\\(A_1 = ' + tz(A1) + '\\;\\text{cm}^2\\)) wird \\(' + ein(s1, 'cm') + '\\) hineingedrückt. Um wie viel hebt sich der grosse Kolben (\\(A_2 = ' + tz(A2) + '\\;\\text{cm}^2\\))?' }; }
          var s2 = zufall([1.5, 3, 6, 10]); return { art: 1, s: s2 * A2 / A1, s2: s2, A1: A1, A2: A2,
            text: 'Ein Wagenheber soll ein Auto um \\(' + ein(s2, 'cm') + '\\) heben (\\(A_2 = ' + tz(A2) + '\\;\\text{cm}^2\\)). Welchen Gesamtweg muss der kleine Kolben (\\(A_1 = ' + tz(A1) + '\\;\\text{cm}^2\\)) zurücklegen?' }; },
        pruefen: function(A, e){
          if (nah(e.s, A.s)) return null;
          var um = A.art === 2 ? A.s1 * A.A2 / A.A1 : A.s2 * A.A1 / A.A2;
          if (nah(e.s, um)) return 'Umgekehrt: Das verdrängte Volumen ist gleich, \\(A_1 \\cdot s_1 = A_2 \\cdot s_2\\). Der grosse Kolben bewegt sich wenig.';
          return 'Gleiches Volumen auf beiden Seiten: \\(A_1 \\cdot s_1 = A_2 \\cdot s_2\\).'; },
        fehler: function(A){ return [[{ s: String(A.art === 2 ? A.s1 * A.A2 / A.A1 : A.s2 * A.A1 / A.A2) }, 'Umgekehrt']]; },
        loesung: function(A){ return A.art === 2 ? 's_2 = s_1 \\cdot \\dfrac{A_1}{A_2} = ' + ein(A.s1, 'cm') + ' \\cdot \\dfrac{' + tz(A.A1) + '}{' + tz(A.A2) + '} ' + erg(A.s, 'cm')
                                                 : 's_1 = s_2 \\cdot \\dfrac{A_2}{A_1} = ' + ein(A.s2, 'cm') + ' \\cdot \\dfrac{' + tz(A.A2) + '}{' + tz(A.A1) + '} ' + erg(A.s, 'cm'); } },
      'druck-presse': { felder: ['p'], muster: '<i>p</i> = {p} bar',
        neu: function(){
          var F1 = zufall([60, 150, 240, 450]), A1 = zufall([1.5, 2.5, 4, 8]);
          return { p: F1 / (A1 / 1e4) / 1e5, F1: F1, A1: A1,
            text: 'Am kleinen Kolben einer Hebebühne (\\(A_1 = ' + tz(A1) + '\\;\\text{cm}^2\\)) drückt eine Kraft von \\(' + ein(F1, 'N') + '\\). Welcher Druck herrscht in der Hydraulikflüssigkeit?' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (nah(e.p, A.p / 1e4) || nah(e.p, A.p * 1e5) || nah(e.p, A.p * 10)) return 'Fläche in m² (\\(1\\;\\text{cm}^2 = 10^{-4}\\;\\text{m}^2\\)), Ergebnis in bar (\\(1\\;\\text{bar} = 10^5\\;\\text{Pa}\\)).';
          return '\\(p = \\dfrac{F_1}{A_1}\\).'; },
        fehler: function(A){ return [[{ p: String(A.p / 1e4) }, 'Fläche'], [{ p: String(A.p * 1e5) }, 'Fläche']]; },
        loesung: function(A){ return 'p = \\dfrac{F_1}{A_1} = \\dfrac{' + ein(A.F1, 'N') + '}{' + tz(A.A1 / 1e4) + '\\;\\text{m}^2} ' + erg(A.p * 1e5, 'Pa') + ' ' + erg(A.p, 'bar'); } },

      /* ----- Kapitel 5: Auftrieb ----- */
      'auftrieb': { felder: ['F'], muster: '<i>F</i><sub>A</sub> = {F} N',
        neu: function(){
          var f = zufall(FL), K = zufall([['Ein Stein', 2600], ['Ein Eisenteil', 7870], ['Ein Aluminiumteil', 2700]]), V, l;
          do { l = Math.random() < 0.5; V = l ? zufall([0.5, 1.5, 3, 4.5]) : zufall([80, 250, 600, 1200]); } while (l && V === 2 && f[1] === 1000);
          var Vm = l ? V / 1000 : V / 1e6;
          return { F: f[1] * Vm * G, rf: f[1], rk: K[1], V: V, l: l, Vm: Vm,
            text: K[0] + ' (\\(\\rho_K = ' + tz(K[1]) + '\\;\\text{kg/m}^3\\)) mit dem Volumen \\(' + (l ? ein(V, 'l') : tz(V) + '\\;\\text{cm}^3') + '\\) liegt ganz in ' + f[0] + ' (\\(\\rho_{Fl} = ' + tz(f[1]) + '\\;\\text{kg/m}^3\\)). Wie gross ist die Auftriebskraft?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.rk * A.Vm * G)) return 'Das ist die Gewichtskraft des Körpers. Der Auftrieb ist das Gewicht der <em>verdrängten Flüssigkeit</em>: \\(\\rho_{Fl}\\).';
          if (nah(e.F, A.F * 1000) || nah(e.F, A.F * 1e6) || nah(e.F, A.F / 1000)) return 'Das Volumen in m³ umrechnen: \\(1\\;\\text{l} = 10^{-3}\\;\\text{m}^3\\), \\(1\\;\\text{cm}^3 = 10^{-6}\\;\\text{m}^3\\).';
          if (nah(e.F, A.F / G)) return 'Das ist die verdrängte Masse in kg. Die Kraft: mal \\(g\\).';
          return '\\(F_A = \\rho_{Fl} \\cdot V_e \\cdot g\\).'; },
        fehler: function(A){ return [[{ F: String(A.rk * A.Vm * G) }, 'verdrängten'], [{ F: String(A.F * 1000) }, 'm³'], [{ F: String(A.F / G) }, 'Masse']]; },
        loesung: function(A){ return 'F_A = \\rho_{Fl} \\cdot V_e \\cdot g = ' + tz(A.rf) + '\\;\\text{kg/m}^3 \\cdot ' + tz(A.Vm) + '\\;\\text{m}^3 \\cdot 9.81\\;\\text{m/s}^2 ' + erg(A.F, 'N'); } },
      'waage': { felder: ['F'], muster: 'Anzeige = {F} N',
        neu: function(){
          var f = zufall(FL), K = zufall([['Messing', 8500], ['Granit', 2750], ['Kupfer', 8960]]), V = zufall([50, 120, 300, 750]);
          var FG = K[1] * V * 1e-6 * G, FA = f[1] * V * 1e-6 * G;
          return { F: FG - FA, FG: FG, FA: FA, V: V, rf: f[1], text: 'Ein Körper aus ' + K[0] + ' (\\(V = ' + tz(V) + '\\;\\text{cm}^3\\)) hängt an einer Federwaage; an der Luft zeigt sie \\(' + ein(+FG.toPrecision(3), 'N') + '\\). Was zeigt sie, wenn der Körper ganz in ' + f[0] + ' (\\(' + tz(f[1]) + '\\;\\text{kg/m}^3\\)) taucht?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F, 0.012)) return null;   // F_G ist auf drei Stellen angegeben
          if (nah(e.F, A.FG + A.FA, 0.012)) return 'Der Auftrieb zeigt nach oben und entlastet die Waage: abziehen.';
          if (nah(e.F, A.FA, 0.012)) return 'Das ist nur der Auftrieb. Die Waage zeigt \\(F_G - F_A\\).';
          return 'Anzeige \\(= F_G - F_A\\) mit \\(F_A = \\rho_{Fl} \\cdot V \\cdot g\\).'; },
        fehler: function(A){ return [[{ F: String(A.FG + A.FA) }, 'entlastet'], [{ F: String(A.FA) }, 'nur']]; },
        loesung: function(A){ return 'F_A = ' + tz(A.rf) + '\\;\\text{kg/m}^3 \\cdot ' + tz(A.V / 1e6) + '\\;\\text{m}^3 \\cdot 9.81\\;\\text{m/s}^2 ' + erg(A.FA, 'N') + ',\\quad F_G - F_A ' + erg(A.F, 'N'); } },
      'dichte-waage': { felder: ['r'], muster: '<i>ρ</i><sub>K</sub> = {r} kg/m³',
        neu: function(){
          var L, W;
          do { L = zufall([2.4, 3.6, 5.2, 7.8]); W = +(L * zufall([0.55, 0.63, 0.7, 0.88])).toFixed(2); } while (!verschieden([L / (L - W) * 1000, L / W * 1000, (L - W) / L * 1000]));
          return { r: L / (L - W) * 1000, L: L, W: W, text: 'Eine Federwaage zeigt für einen Körper an der Luft \\(' + ein(L, 'N') + '\\), ganz in Wasser getaucht \\(' + ein(W, 'N') + '\\). Welche Dichte hat der Körper?' }; },
        pruefen: function(A, e){
          if (nah(e.r, A.r)) return null;
          if (nah(e.r, A.L / A.W * 1000)) return 'Der Auftrieb ist der Unterschied der Anzeigen: \\(F_A = ' + tz(A.L) + '\\;\\text{N} - ' + tz(A.W) + '\\;\\text{N}\\).';
          if (nah(e.r, (A.L - A.W) / A.L * 1000)) return 'Umgekehrt: \\(\\dfrac{\\rho_K}{\\rho_W} = \\dfrac{F_G}{F_A}\\).';
          return 'Aus dem Auftrieb das Volumen, dann \\(\\rho_K = \\dfrac{F_G}{F_A} \\cdot \\rho_W\\).'; },
        fehler: function(A){ return [[{ r: String(A.L / A.W * 1000) }, 'Unterschied'], [{ r: String((A.L - A.W) / A.L * 1000) }, 'Umgekehrt']]; },
        loesung: function(A){ return 'F_A = ' + ein(A.L, 'N') + ' - ' + ein(A.W, 'N') + ',\\quad \\rho_K = \\dfrac{F_G}{F_A} \\cdot \\rho_W = \\dfrac{' + ein(A.L, 'N') + '}{' + ein(+(A.L - A.W).toFixed(2), 'N') + '} \\cdot 1000\\;\\text{kg/m}^3 ' + erg(A.r, 'kg/m^3').replace('\\text{kg/m^3}', '\\text{kg/m}^3'); } },

      /* ----- Kapitel 6: Schwimmen, Schweben, Sinken ----- */
      'anteil': { felder: ['x'], muster: '{x} %',
        neu: function(){
          var K, f;
          K = zufall([['Ein Holzbalken', 640], ['Ein Paraffinblock', 900], ['Ein Kunststoffschwimmer', 360], ['Eine Boje', 250]]); f = zufall([['Süsswasser', 1000], ['Meerwasser', 1025], ['Salzsole', 1200]]);
          return { x: 100 * K[1] / f[1], rk: K[1], rf: f[1], text: K[0] + ' (\\(\\rho_K = ' + tz(K[1]) + '\\;\\text{kg/m}^3\\)) schwimmt in ' + f[0] + ' (\\(' + tz(f[1]) + '\\;\\text{kg/m}^3\\)). Wie viel Prozent seines Volumens liegen unter der Oberfläche?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, 100 - A.x)) return 'Das ist der Anteil über Wasser. Gefragt ist der Teil unter der Oberfläche.';
          if (nah(e.x, 100 * A.rf / A.rk)) return 'Umgekehrt: \\(\\dfrac{V_e}{V} = \\dfrac{\\rho_K}{\\rho_{Fl}}\\), immer kleiner als 1.';
          if (nah(e.x, A.x / 100)) return 'In Prozent angeben: mal 100.';
          return 'Schwimmend gilt \\(F_A = F_G\\), daraus \\(\\dfrac{V_e}{V} = \\dfrac{\\rho_K}{\\rho_{Fl}}\\).'; },
        fehler: function(A){ return [[{ x: String(100 - A.x) }, 'über Wasser'], [{ x: String(100 * A.rf / A.rk) }, 'Umgekehrt'], [{ x: String(A.x / 100) }, 'Prozent']]; },
        loesung: function(A){ return '\\dfrac{V_e}{V} = \\dfrac{\\rho_K}{\\rho_{Fl}} = \\dfrac{' + tz(A.rk) + '}{' + tz(A.rf) + '} ' + erg(A.x / 100, '').replace('\\;\\text{}', '') + ' = ' + tz(+A.x.toPrecision(3)) + '\\,\\%'; } },
      'eintauchtiefe': { felder: ['h'], muster: '<i>h</i><sub>e</sub> = {h} cm',
        neu: function(){
          var H, rk, f;
          do { H = zufall([6, 12, 20, 30]); rk = zufall([450, 600, 750, 880]); f = zufall([['Süsswasser', 1000], ['Meerwasser', 1025]]); } while (!verschieden([H * rk / f[1], H * f[1] / rk, H - H * rk / f[1]]));
          return { h: H * rk / f[1], H: H, rk: rk, rf: f[1], text: 'Ein Holzquader (\\(\\rho_K = ' + tz(rk) + '\\;\\text{kg/m}^3\\)), \\(' + ein(H, 'cm') + '\\) hoch, schwimmt flach in ' + f[0] + ' (\\(' + tz(f[1]) + '\\;\\text{kg/m}^3\\)). Wie tief taucht er ein?' }; },
        pruefen: function(A, e){
          if (nah(e.h, A.h)) return null;
          if (nah(e.h, A.H - A.h)) return 'Das ist der Teil über Wasser.';
          if (nah(e.h, A.H * A.rf / A.rk)) return 'Umgekehrt: \\(\\dfrac{h_e}{H} = \\dfrac{\\rho_K}{\\rho_{Fl}}\\).';
          return 'Bei gleichem Querschnitt verhalten sich die Höhen wie die Volumen: \\(h_e = H \\cdot \\dfrac{\\rho_K}{\\rho_{Fl}}\\).'; },
        fehler: function(A){ return [[{ h: String(A.H - A.h) }, 'über Wasser'], [{ h: String(A.H * A.rf / A.rk) }, 'Umgekehrt']]; },
        loesung: function(A){ return 'h_e = H \\cdot \\dfrac{\\rho_K}{\\rho_{Fl}} = ' + ein(A.H, 'cm') + ' \\cdot \\dfrac{' + tz(A.rk) + '}{' + tz(A.rf) + '} ' + erg(A.h, 'cm'); } },
      'mittlere-dichte': { felder: ['r'], muster: '<i>ρ</i> = {r} kg/m³',
        neu: function(){
          var c = zufall([['Ein verschlossener Kanister', [0.8, 1.6, 3.4], [5, 10, 20]], ['Ein Schwimmring', [0.4, 0.9], [12, 18]], ['Eine gefüllte Flasche', [1.1, 1.6], [1, 1.5]], ['Ein Tauchgewicht mit Luftkammer', [2.4, 3.2], [2, 2.5]]]);
          var m = zufall(c[1]), V = zufall(c[2]);
          return { r: m / (V / 1000), m: m, V: V, text: c[0] + ' hat die Masse \\(' + ein(m, 'kg') + '\\) und das Volumen \\(' + ein(V, 'l') + '\\). Wie gross ist seine mittlere Dichte? Schwimmt er in Wasser?' }; },
        pruefen: function(A, e){
          if (nah(e.r, A.r)) return null;
          if (nah(e.r, A.r / 1000)) return 'Das ist kg je Liter. In kg/m³: \\(1\\;\\text{l} = 10^{-3}\\;\\text{m}^3\\).';
          if (nah(e.r, 1 / (A.r / 1000)) || nah(e.r, A.V / A.m * 1000)) return 'Umgekehrt: Dichte ist Masse durch Volumen.';
          return '\\(\\rho = \\dfrac{m}{V}\\), \\(V\\) in m³.'; },
        fehler: function(A){ return [[{ r: String(A.r / 1000) }, 'Liter'], [{ r: String(A.V / A.m * 1000) }, 'Umgekehrt']]; },
        loesung: function(A){ return '\\rho = \\dfrac{m}{V} = \\dfrac{' + ein(A.m, 'kg') + '}{' + tz(A.V / 1000) + '\\;\\text{m}^3} ' + erg(A.r, 'kg/m^3').replace('\\text{kg/m^3}', '\\text{kg/m}^3') + (A.r < 1000 ? '\\;\\text{— schwimmt}' : (A.r > 1000 ? '\\;\\text{— sinkt}' : '\\;\\text{— schwebt}')); } }
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
