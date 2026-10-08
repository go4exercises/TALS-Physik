<script>
/* Leitprogramm Wärmeausdehnung und Gase — laufende Simulationen mit Aufgabenleiste, Übungen mit
   Rückmeldung, Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr,
   Übungsrahmen, Minigrafen) wörtlich aus dem Leitprogramm Hydrostatik; neu sind die Simulationen
   (Stab, Gefäss und Würfel, Meeresschicht, Gas im Zylinder, die drei Spezialfälle) und die
   Übungstypen für 5.3. α und γ wie Themenseite 5.3, T [K] = ϑ [°C] + 273.15 wie Themenseite 5.1.
   Farben (Farbe = eine Bedeutung): Ausdehnung (Δl, ΔV, Δh) und der laufende Zustand Bernstein,
   Ausgangszustand grau gestrichelt, Temperatur Orange, Druck Rot, Volumen Grün.
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
    /* Belegte Flächen [links, oben, rechts, unten] in px: Achsennamen, Teilung, Punkte und
       schon gesetzte Beschriftungen. etikett() sucht für die Beschriftung eines Punktes eine
       freie Stelle, die weder diese Flächen noch die übergebenen Kurven berührt. */
    var breite = function(s){ return String(s).replace(/_/g, '').length * 6.9; };
    var schutz = [[W - 3 - breite(o.xname || 'x'), Y(0) - pf - 14, W, Y(0) - pf + 1],
                  [X(0) + pf, 0, X(0) + pf + 4 + breite(o.yname || 'y'), pf + 8],
                  [0, Y(0) + 2, W, Y(0) + 16], [X(0) - 30, 0, X(0) + 2, H]];   // Teilung links der y-Achse (nicht der ganze Streifen)
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
        schutz.push([X(x) - 6, Y(y) - 6, X(x) + 6, Y(y) + 6]);
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      },
      /* Beschriftung «(x; y)» an einem Punkt: die erste freie von mehreren Stellen rund um
         den Punkt. kurven: [[f, von, bis], …] in Datenkoordinaten; belegt: weitere Flächen
         (Legende); wahl: eigene Reihenfolge der Stellen [dx, dy, Anker]. */
      etikett: function(x, y, s, cls, op){
        op = op || {};
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        var px = X(x), py = Y(y), bw = breite(s), bh = 11, alle = schutz.concat(op.belegt || []), ks = op.kurven || [];
        var wahl = op.wahl || [[8, -8, 'start'], [8, 17, 'start'], [-8, -8, 'end'], [-8, 17, 'end'],
                                [-8, -24, 'end'], [8, -24, 'start'], [-40, -8, 'end'], [-70, 2, 'end'],
                                [-8, 34, 'end'], [8, 34, 'start'], [-8, 52, 'end']];
        function frei(b){
          if (b[0] < 1 || b[2] > W - 1 || b[1] < 1 || b[3] > H - 1) return false;
          for (var i = 0; i < alle.length; i++){ var c = alle[i]; if (b[0] < c[2] && b[2] > c[0] && b[1] < c[3] && b[3] > c[1]) return false; }
          for (var j = 0; j < ks.length; j++){
            var vor = null;
            for (var k = 0; k <= 30; k++){
              var xx = x0 + (b[0] - 3 + (b[2] - b[0] + 6) * k / 30) / W * (x1 - x0);
              if (xx < ks[j][1] || xx > ks[j][2]){ vor = null; continue; }
              var yy = Y(ks[j][0](xx));
              if (yy > b[1] - 3 && yy < b[3] + 3) return false;
              if (vor != null && Math.min(vor, yy) < b[3] + 3 && Math.max(vor, yy) > b[1] - 3) return false;
              vor = yy;
            }
          }
          return true;
        }
        var gew = null, ks0 = ks;
        // erst frei von allem, dann frei von Beschriftungen und Rand, zuletzt nur im Bild (nie abgeschnitten)
        for (var stufe = 0; stufe < 3 && !gew; stufe++){
          if (stufe === 1) ks = [];
          if (stufe === 2) alle = [];
          for (var i = 0; i < wahl.length; i++){
            var c = wahl[i], tx = px + c[0], ty = py + c[1], l = c[2] === 'end' ? tx - bw : tx;
            if (frei([l, ty - bh + 1, l + bw, ty + 3])){ gew = c; break; }
          }
        }
        ks = ks0; if (!gew) gew = wahl[0];
        var gx = px + gew[0], gy = py + gew[1], gl_ = gew[2] === 'end' ? gx - bw : gx;
        schutz.push([gl_, gy - bh + 1, gl_ + bw, gy + 3]);
        el(ebene, 'text', { x: gx, y: gy, 'text-anchor': gew[2], 'class': 'p-text ' + cls }, s);
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

  var T0K = 273.15;                                      // T [K] = ϑ [°C] + 273.15 (Themenseite 5.1)
  var MAT = { st: { name: 'Stahl', a: 12e-6, z: '12' }, me: { name: 'Messing', a: 18.4e-6, z: '18.4' }, al: { name: 'Aluminium', a: 23.8e-6, z: '23.8' } };
  function zehn(m, k){ return m + '·10' + hoch(k); }     // «12·10⁻⁶»
  function p_(i){ return v_('p') + (i ? '<sub>' + i + '</sub>' : ''); }
  function V_(i){ return v_('V') + (i ? '<sub>' + i + '</sub>' : ''); }
  function T_(i){ return v_('T') + (i ? '<sub>' + i + '</sub>' : ''); }
  // Achsenteilung zum grössten Wert: höchstens vier beschriftete Striche
  function schritt(max){
    var st = [0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000], i = 0;
    while (i < st.length - 1 && max / st[i] > 4) i++;
    return st[i];
  }
  // Teilung nach oben und unten: oben bis max, unten bis −unten (beide positiv angegeben)
  function skalaPM(max, unten){
    var s = schritt(max), oben = Math.ceil(max * 1.04 / s) * s, tief = unten > 0 ? Math.ceil(unten * 1.04 / s) * s : 0.1 * oben, ym = [], v;
    for (v = s; v <= oben + 1e-9; v += s) ym.push(+v.toPrecision(6));
    for (v = -s; v >= -tief + s * 0.5 - 1e-9; v -= s) ym.push(+v.toPrecision(6));
    return { y0: -tief, y1: oben * 1.04, sy: s / 2, ym: ym };
  }
  // Thermometer: Säule von tmin bis tmax zwischen y oben und y unten, Kugel darunter
  function thermometer(eltern, x, yo, yu, t, tmin, tmax){
    el(eltern, 'rect', { x: x - 4, y: yo, width: 8, height: yu - yo, rx: 4, 'class': 'thermo-glas' });
    var h = (Math.max(tmin, Math.min(tmax, t)) - tmin) / (tmax - tmin) * (yu - yo - 4);
    el(eltern, 'rect', { x: x - 2, y: yu - 2 - h, width: 4, height: h + 6, 'class': 'thermo-saeule' });
    el(eltern, 'circle', { cx: x, cy: yu + 6, r: 7, 'class': 'thermo-kugel' });
  }

  /* ---------- Kapitel 1: Längenausdehnung ----------
     Ein Stab (Stahl, Messing oder Aluminium) hat bei ϑ₀ = 20 °C die Anfangslänge l₀ und ist links
     fest eingespannt. Auf Knopfdruck ändert sich seine Temperatur auf ϑ; das freie Ende wandert um
     Δl = α · l₀ · ΔT. Die Längenänderung ist im Bild stark vergrössert (Massstab je Länge: Aluminium
     bei +60 K braucht 70 px), die Länge l₀ nicht massstäblich. Darunter Δl über ϑ: die Gerade des
     gewählten Werkstoffs, die beiden anderen gestrichelt.
     Unterschied zur Themenseite (Animation 1): dort Δl ab ΔT = 0 nur beim Erwärmen; hier rechnet man
     ΔT aus zwei Temperaturen, kühlt auch ab und sieht das Vorzeichen. Werkstoffe und α wie Themenseite.
     Clipbeispiel: Stahl und Aluminium, 40 m, 20 → 60 °C; Startwerte Stahl, 60 m, 35 °C (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,186)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); tc = TA; zeichnen(); });
    var TA = 20, tc = TA, lauf = null, laeufe = [], pruefen = function(){};
    function werte(){ var mk = B.wert('mat'), m = MAT[mk], l0 = B.wert('l0'), t = B.wert('t'); return { mk: mk, m: m, l0: l0, t: t, dT: t - TA, dl: m.a * l0 * (t - TA) }; }
    function fertig(w){ lauf = { mat: w.mk, l0: w.l0, t: w.t, dl: w.dl }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(), u = Math.min(1, tt / 2); tc = TA + (w.t - TA) * u; zeichnen(); if (u >= 1){ tc = w.t; fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Temperatur ändern', function(){ if (WENIGER){ var w = werte(); tc = w.t; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück auf 20 °C', function(){ uhr.stop(); tc = TA; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); tc = TA; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      // Testhaken: momentane Temperatur in °C (Bildfolgen der Clips)
      zeige: function(x){ uhr.stop(); tc = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), t = Math.round(tc), dT = t - TA, dl = w.m.a * w.l0 * dT, mm = dl * 1000;
      B.anzeigen(); leeren(szene); leeren(dia);
      var k = 70 / (MAT.al.a * w.l0 * 60 * 1000);                   // px je mm
      var x0 = 30, xe = 186, y = 92, xn = xe + mm * k;
      // Kopfzeilen
      el(szene, 'text', { x: 4, y: 14, 'class': 'bt-wert' }, w.m.name + ': α = ' + zehn(w.m.z, '-6') + NB + '1/K');
      el(szene, 'text', { x: 4, y: 30, 'class': 'bt-klein' }, 'l₀ = ' + zahl(w.l0) + NB + 'm bei ϑ₀ = 20' + NB + '°C (nicht massstäblich)');
      // Fixpunkt und Stab
      el(szene, 'rect', { x: x0 - 12, y: y - 28, width: 12, height: 56, 'class': 'wand' });
      el(szene, 'rect', { x: x0, y: y - 8, width: Math.max(4, xn - x0), height: 16, 'class': 'stab' });
      el(szene, 'line', { x1: xe, y1: y - 24, x2: xe, y2: y + 26, 'class': 'vorher' });
      el(szene, 'text', { x: xe, y: y - 28, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Ende bei 20 °C');
      // Pfeil Δl zwischen altem und neuem Ende
      if (Math.abs(xn - xe) > 3){
        pfeil(szene, xe, y + 18, xn, y + 18, 'pf-dl', 6);
        el(szene, 'text', { x: (xe + xn) / 2, y: y + 36, 'text-anchor': 'middle', 'class': 'pf-text t-dl' }, 'Δl = ' + (mm < 0 ? '−' : '') + sig(Math.abs(mm)) + NB + 'mm');
      }
      el(szene, 'text', { x: 4, y: 156, 'class': 'bt-klein' }, 'Die Längenänderung ist im Bild stark vergrössert.');
      // Thermometer
      thermometer(szene, 284, 14, 64, t, -30, 80);
      el(szene, 'text', { x: 272, y: 34, 'text-anchor': 'end', 'class': 'bt-wert t-temp' }, 'ϑ = ' + minus(t) + NB + '°C');
      // Diagramm: Δl über ϑ
      var amax = MAT.al.a * w.l0 * 1000, sk = skalaPM(amax * 60, amax * 50);
      K = Achsen(dia, { w: 300, h: 128, x0: -38, x1: 88, y0: sk.y0, y1: sk.y1, sx: 10, sy: sk.sy, xm: [-20, 20, 40, 60, 80], ym: sk.ym, xname: 'ϑ [°C]', yname: 'Δl [mm]' });
      var kv = [];
      ['st', 'me', 'al'].forEach(function(q){
        var f = function(x){ return MAT[q].a * w.l0 * (x - TA) * 1000; };
        kv.push([f, -30, 80]);
        if (q !== w.mk) K.kurve(f, 'kurve-hilf hilfslinie', -30, 80);
      });
      K.kurve(function(x){ return w.m.a * w.l0 * (x - TA) * 1000; }, 'kurve-dl', -30, 80);
      stext(K.ebene, { x: 0, y: 154, 'class': 'legende l-dl' }, '— ' + w.m.name);
      stext(K.ebene, { x: 300, y: 154, 'text-anchor': 'end', 'class': 'legende hilfslinie' }, '- - die beiden anderen Werkstoffe');
      K.punkt(t, mm, 'p-dl');
      if (dT !== 0) K.etikett(t, mm, '(' + minus(t) + NB + '°C; ' + (mm < 0 ? '−' : '') + sig(Math.abs(mm)) + NB + 'mm)', 'p-dl', { kurven: kv, wahl: (dT < 0 ? [[K.X(28) - K.X(t), K.Y(sk.ym.filter(function(v){ return v < 0; }).slice(0, 2).reduce(function(a, b, i, r){ return a + b / r.length; }, 0)) + 4 - K.Y(mm), 'start']] : []).concat([[8, -8, 'start'], [-8, -8, 'end'], [8, -24, 'start'], [-8, -24, 'end'], [8, -40, 'start'], [-8, -40, 'end'], [8, 17, 'start'], [-8, 17, 'end'], [8, 34, 'start']]) });   // abgekühlt: unten rechts ist das Diagramm frei (alle Geraden steigen rechts von 20 °C)
      // Formelzeilen: eine Rechnung, eine Zeile
      var dlm = Math.abs(dl) < 1e-15 ? 0 : dl;
      var z = '<span>Δ' + v_('T') + ' = ' + v_('ϑ') + ' − ' + v_('ϑ') + '<sub>0</sub> = ' + ew(t, '°C') + ' − 20' + NB + '°C = ' + minus(dT) + NB + 'K</span>';
      z += '<span>Δ' + v_('l') + ' = ' + v_('α') + ' · ' + v_('l') + '<sub>0</sub> · Δ' + v_('T') + ' = ' + zehn(w.m.z, '-6') + NB + '1/K · ' + zahl(w.l0) + NB + 'm · ' + ew(dT, 'K') + ' ' + ist(dlm, sig(dlm)) + sig(dlm) + NB + 'm ' + ist(mm, sig(mm)) + sig(mm) + NB + 'mm</span>';
      z += '<span class="sim-notiz">Neue Länge: ' + v_('l') + ' = ' + v_('l') + '<sub>0</sub> + Δ' + v_('l') + ' ' + ist(w.l0 + dl, zahl(+(w.l0 + dl).toFixed(5))) + zahl(+(w.l0 + dl).toFixed(5)) + NB + 'm. Kühlt der Stab ab (ΔT < 0), wird er kürzer.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, mk, l0, t){ var l = s.lauf; return l && l.mat === mk && l.l0 === l0 && l.t === t; }
    pruefen = Leiste(fig, [
      { text: 'Ein Stahlträger ist bei \\(20\\;^\\circ\\text{C}\\) genau \\(30\\;\\text{m}\\) lang. Er erwärmt sich auf \\(50\\;^\\circ\\text{C}\\). Stelle ein und ändere die Temperatur. Wie gross ist \\(\\Delta l\\)? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 'st', 30, 50); },
        vergleich: '\\(\\Delta T = 50\\;^\\circ\\text{C} - 20\\;^\\circ\\text{C} = 30\\;\\text{K}\\), \\(\\Delta l = \\alpha \\cdot l_0 \\cdot \\Delta T = 12 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} \\cdot 30\\;\\text{m} \\cdot 30\\;\\text{K} = 0.0108\\;\\text{m} = 10.8\\;\\text{mm}\\).' },
      { text: 'Gleiche Länge, gleiche Temperatur, aber Aluminium: Wie viel mal so gross ist \\(\\Delta l\\) jetzt? Ändere die Temperatur und begründe mit der Formel.', ok: function(s){ return hat(s, 'al', 30, 50); },
        vergleich: '\\(\\Delta l = 23.8 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} \\cdot 30\\;\\text{m} \\cdot 30\\;\\text{K} \\approx 21.4\\;\\text{mm}\\), knapp doppelt so viel. \\(l_0\\) und \\(\\Delta T\\) sind gleich, es zählt nur \\(\\alpha\\): \\(\\dfrac{23.8}{12} \\approx 1.98\\).' },
      { text: 'Eine Messingstange (\\(8\\;\\text{m}\\)) kühlt von \\(20\\;^\\circ\\text{C}\\) auf \\(-15\\;^\\circ\\text{C}\\) ab. Notiere \\(\\Delta T\\) und \\(\\Delta l\\) mit Vorzeichen, dann stelle ein. Was bedeutet das Minus?', ok: function(s){ return hat(s, 'me', 8, -15); },
        vergleich: '\\(\\Delta T = -15\\;^\\circ\\text{C} - 20\\;^\\circ\\text{C} = -35\\;\\text{K}\\), \\(\\Delta l = 18.4 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} \\cdot 8\\;\\text{m} \\cdot (-35\\;\\text{K}) \\approx -5.15\\;\\text{mm}\\). Das Minus heisst: Die Stange wird kürzer.' },
      { text: 'Stahl bei \\(50\\;^\\circ\\text{C}\\): Welche Länge ergibt doppelt so viel \\(\\Delta l\\) wie in Aufgabe 1? Notiere und begründe, dann stelle ein und prüfe.', ok: function(s){ return hat(s, 'st', 60, 50); },
        vergleich: '\\(60\\;\\text{m}\\): \\(\\Delta l\\) ist proportional zu \\(l_0\\). Doppelte Länge, doppelte Längenänderung: \\(21.6\\;\\text{mm}\\) statt \\(10.8\\;\\text{mm}\\).' },
      { text: 'Ein Aluminiumprofil von \\(20\\;\\text{m}\\) darf höchstens \\(10\\;\\text{mm}\\) länger werden. Bis zu welcher Temperatur geht das (auf \\(1\\;^\\circ\\text{C}\\) genau)? Notiere deine Rechnung, dann stelle ein und prüfe.', ok: function(s){ return hat(s, 'al', 20, 41); },
        vergleich: '\\(\\Delta T = \\dfrac{\\Delta l}{\\alpha \\cdot l_0} = \\dfrac{0.010\\;\\text{m}}{23.8 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} \\cdot 20\\;\\text{m}} \\approx 21.0\\;\\text{K}\\), also bis \\(\\vartheta = 20\\;^\\circ\\text{C} + 21\\;\\text{K} = 41\\;^\\circ\\text{C}\\) (\\(\\Delta l \\approx 9.996\\;\\text{mm}\\)). Bei \\(42\\;^\\circ\\text{C}\\) sind es schon \\(10.5\\;\\text{mm}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Volumenausdehnung ----------
     Ein Liter-Gefäss mit Steigrohr (Ethanol, Quecksilber) oder ein Würfel (Aluminium, Stahl) mit dem
     Anfangsvolumen V₀ bei 20 °C. Auf Knopfdruck wird er auf ϑ erwärmt: die Flüssigkeit steigt im
     Steigrohr um ΔV (Skala in ml), der Würfel wächst in alle drei Richtungen (stark vergrössert,
     Kante × 84). Darunter ΔV über ΔT für die vier Stoffe beim eingestellten V₀ (gewählter Stoff
     durchgezogen, die anderen gestrichelt). Festkörper: γ ≈ 3 · α; Flüssigkeiten: γ aus der Tabelle.
     Gefäss und Steigrohr dehnen sich hier nicht aus (Modell; die scheinbare Ausdehnung steht im
     Festhalten und auf der Themenseite). Wasser fehlt bewusst: sein γ hängt stark von der Temperatur
     ab (Kapitel 3).
     Unterschied zur Themenseite (Animation 2): dort Füllstand und Würfel ohne Diagramm und ohne die
     Rechnung γ ≈ 3α in der Formelzeile; hier stehen alle vier Stoffe zum Vergleich im Diagramm.
     Clipbeispiel: 1 l Ethanol und 1 l Aluminium, 20 → 60 °C; Startwerte Ethanol, 1.5 l, 35 °C. */
  var STOFF = { et: { name: 'Ethanol', g: 1.10e-3, z: '1.10', k: '-3', fl: true }, hg: { name: 'Quecksilber', g: 0.18e-3, z: '0.18', k: '-3', fl: true },
                al: { name: 'Aluminium', a: 23.8e-6, z: '23.8', g: 3 * 23.8e-6, gz: '71.4' }, st: { name: 'Stahl', a: 12e-6, z: '12', g: 36e-6, gz: '36' } };
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,186)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); tc = TA; zeichnen(); });
    var TA = 20, tc = TA, lauf = null, laeufe = [], pruefen = function(){};
    function werte(){ var sk = B.wert('stoff'), s = STOFF[sk], V0 = B.wert('V0'), t = B.wert('t'); return { sk: sk, s: s, V0: V0, t: t, dT: t - TA, dV: s.g * V0 * (t - TA) }; }
    function fertig(w){ lauf = { stoff: w.sk, V0: w.V0, t: w.t, dV: w.dV }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(), u = Math.min(1, tt / 2); tc = TA + (w.t - TA) * u; zeichnen(); if (u >= 1){ tc = w.t; fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Erwärmen', function(){ if (WENIGER){ var w = werte(); tc = w.t; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück auf 20 °C', function(){ uhr.stop(); tc = TA; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); tc = TA; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); tc = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), t = Math.round(tc), dT = t - TA, dV = w.s.g * w.V0 * dT, ml = dV * 1000;
      B.anzeigen(); leeren(szene); leeren(dia);
      el(szene, 'text', { x: 4, y: 14, 'class': 'bt-wert' }, w.s.name + (w.s.fl ? ': γ = ' + zehn(w.s.z, w.s.k) + NB + '1/K' : ': α = ' + zehn(w.s.z, '-6') + NB + '1/K'));
      el(szene, 'text', { x: 4, y: 30, 'class': 'bt-klein' }, 'V₀ = ' + zahl(w.V0) + NB + 'l bei 20' + NB + '°C');
      if (w.s.fl){
        // Gefäss mit Steigrohr: 0-Marke bei 20 °C, Ethanol bei +60 K steigt 70 px
        var kt = 66 / (STOFF.et.g * w.V0 * 60 * 1000), xr = 120, y0r = 98, yn = y0r - ml * kt;   // Ethanol bei +60 K: 66 px über der 0-Marke
        el(szene, 'rect', { x: 70, y: 112, width: 100, height: 52, rx: 10, 'class': 'fluessig' });
        el(szene, 'rect', { x: xr - 5, y: yn, width: 10, height: 113 - yn, 'class': 'fluessig' });
        el(szene, 'path', { d: 'M' + (xr - 6) + ' 24 L' + (xr - 6) + ' 110 L80 110 Q68 110 68 122 L68 156 Q68 166 80 166 L160 166 Q172 166 172 156 L172 122 Q172 110 160 110 L' + (xr + 6) + ' 110 L' + (xr + 6) + ' 24', 'class': 'glas' });
        var st = schritt(STOFF.et.g * w.V0 * 60 * 1000), mk;
        for (mk = 0; mk * kt <= 70; mk += st){ var yy = y0r - mk * kt; el(szene, 'line', { x1: xr + 6, y1: yy, x2: xr + 12, y2: yy, 'class': 'tick' }); el(szene, 'text', { x: xr + 15, y: yy + 3, 'class': 'skala' }, zahl(+mk.toPrecision(6)) + (mk === 0 ? ' ml' : '')); }
        el(szene, 'line', { x1: xr - 16, y1: y0r, x2: xr - 6, y2: y0r, 'class': 'vorher' });
        if (ml * kt > 2){ pfeil(szene, xr - 12, y0r, xr - 12, yn, 'pf-dl', 5); el(szene, 'text', { x: xr - 16, y: (y0r + yn) / 2 + 4, 'text-anchor': 'end', 'class': 'pf-text t-dl' }, 'ΔV = ' + sig(ml) + NB + 'ml'); }
        el(szene, 'text', { x: 4, y: 176, 'class': 'bt-klein' }, 'Steigrohr: Skala in ml. Das Gefäss dehnt sich hier nicht mit.');
      } else {
        // Würfel, Kante im Bild × 84 vergrössert, links unten fest
        var a0 = 84, rel = dV / w.V0, a1 = a0 * (1 + 84 * rel / 3), xa = 60, ya = 164;
        el(szene, 'rect', { x: xa, y: ya - a1, width: a1, height: a1, 'class': 'wuerfel' });
        el(szene, 'rect', { x: xa, y: ya - a0, width: a0, height: a0, 'class': 'vorher' });
        if (a1 - a0 > 2){ el(szene, 'text', { x: xa + a1 + 6, y: ya - a1 / 2, 'class': 'pf-text t-dl' }, 'ΔV = ' + sig(ml) + NB + 'ml'); }
        el(szene, 'text', { x: 4, y: 176, 'class': 'bt-klein' }, 'Würfel: wächst in alle drei Richtungen (im Bild stark vergrössert).');
      }
      thermometer(szene, 284, 14, 64, t, 0, 90);
      el(szene, 'text', { x: 272, y: 34, 'text-anchor': 'end', 'class': 'bt-wert t-temp' }, 'ϑ = ' + minus(t) + NB + '°C');
      // Diagramm: ΔV über ΔT
      var emax = STOFF.et.g * w.V0 * 60 * 1000, sk = skalaPM(emax, 0);
      K = Achsen(dia, { w: 300, h: 128, x0: -5, x1: 66, y0: sk.y0, y1: sk.y1, sx: 5, sy: sk.sy, xm: [10, 20, 30, 40, 50, 60], ym: sk.ym, xname: 'ΔT [K]', yname: 'ΔV [ml]' });
      var kv = [];
      ['et', 'hg', 'al', 'st'].forEach(function(q){
        var f = function(x){ return STOFF[q].g * w.V0 * x * 1000; };
        kv.push([f, 0, 60]);
        if (q !== w.sk) K.kurve(f, 'kurve-hilf hilfslinie', 0, 60);
      });
      K.kurve(function(x){ return w.s.g * w.V0 * x * 1000; }, 'kurve-dl', 0, 60);
      stext(K.ebene, { x: 0, y: 154, 'class': 'legende l-dl' }, '— ' + w.s.name);
      stext(K.ebene, { x: 300, y: 154, 'text-anchor': 'end', 'class': 'legende hilfslinie' }, '- - die anderen Stoffe');
      K.punkt(dT, ml, 'p-dl');
      if (dT !== 0) K.etikett(dT, ml, '(' + dT + NB + 'K; ' + sig(ml) + NB + 'ml)', 'p-dl', { kurven: kv });
      var z = '<span>Δ' + v_('T') + ' = ' + v_('ϑ') + ' − ' + v_('ϑ') + '<sub>0</sub> = ' + ew(t, '°C') + ' − 20' + NB + '°C = ' + minus(dT) + NB + 'K</span>';
      if (!w.s.fl) z += '<span>' + v_('γ') + ' ≈ 3 · ' + v_('α') + ' = 3 · ' + zehn(w.s.z, '-6') + NB + '1/K = ' + zehn(w.s.gz, '-6') + NB + '1/K</span>';
      var gz = w.s.fl ? zehn(w.s.z, w.s.k) : zehn(w.s.gz, '-6'), dl_ = Math.abs(dV) < 1e-15 ? 0 : dV;
      z += '<span>Δ' + V_() + ' = ' + v_('γ') + ' · ' + V_('0') + ' · Δ' + v_('T') + ' = ' + gz + NB + '1/K · ' + zahl(w.V0) + NB + 'l · ' + ew(dT, 'K') + ' ' + ist(dl_, sig(dl_)) + sig(dl_) + NB + 'l ' + ist(ml, sig(ml)) + sig(ml) + NB + 'ml</span>';
      z += '<span class="sim-notiz">' + (w.s.fl ? 'Flüssigkeit: γ steht in der Tabelle.' : 'Festkörper: Jede Kante wächst um α · ΔT, das Volumen dreimal so stark.') + ' 1' + NB + 'l = 1000' + NB + 'ml.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, sk, V0, t){ var l = s.lauf; return l && l.stoff === sk && l.V0 === V0 && l.t === t; }
    pruefen = Leiste(fig, [
      { text: 'Erwärme \\(2.5\\;\\text{l}\\) Ethanol von \\(20\\;^\\circ\\text{C}\\) auf \\(60\\;^\\circ\\text{C}\\). Um wie viele Milliliter wächst das Volumen? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 'et', 2.5, 60); },
        vergleich: '\\(\\Delta V = \\gamma \\cdot V_0 \\cdot \\Delta T = 1.10 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 2.5\\;\\text{l} \\cdot 40\\;\\text{K} = 0.11\\;\\text{l} = 110\\;\\text{ml}\\).' },
      { text: 'Dasselbe mit Quecksilber. Wie viel mal kleiner ist \\(\\Delta V\\)? Erwärme und notiere. Warum steigt die Säule im Thermometer trotzdem gut sichtbar?', ok: function(s){ return hat(s, 'hg', 2.5, 60); },
        vergleich: '\\(\\Delta V = 0.18 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 2.5\\;\\text{l} \\cdot 40\\;\\text{K} = 18\\;\\text{ml}\\), rund sechsmal weniger (\\(\\tfrac{1.10}{0.18} \\approx 6.1\\)). Im Thermometer wird das kleine \\(\\Delta V\\) in ein sehr dünnes Rohr gedrückt — dort gibt es einen langen Weg.' },
      { text: 'Ein Stahlblock (\\(4\\;\\text{l}\\)) wird von \\(20\\;^\\circ\\text{C}\\) auf \\(70\\;^\\circ\\text{C}\\) erwärmt. Rechne zuerst \\(\\gamma\\) aus \\(\\alpha\\), dann \\(\\Delta V\\). Notiere, dann stelle ein und erwärme.', ok: function(s){ return hat(s, 'st', 4, 70); },
        vergleich: '\\(\\gamma \\approx 3 \\cdot \\alpha = 3 \\cdot 12 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} = 36 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}}\\), \\(\\Delta V = 36 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} \\cdot 4\\;\\text{l} \\cdot 50\\;\\text{K} = 0.0072\\;\\text{l} = 7.2\\;\\text{ml}\\).' },
      { text: 'Ein Aluminiumblock von \\(2\\;\\text{l}\\) soll um \\(5\\;\\text{ml}\\) wachsen. Bis zu welcher Temperatur musst du ihn erwärmen (auf \\(1\\;^\\circ\\text{C}\\) genau)? Notiere deine Rechnung, dann stelle ein und prüfe.', ok: function(s){ return hat(s, 'al', 2, 55); },
        vergleich: '\\(\\gamma = 3 \\cdot 23.8 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} = 71.4 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}}\\); \\(\\Delta T = \\dfrac{\\Delta V}{\\gamma \\cdot V_0} = \\dfrac{0.005\\;\\text{l}}{71.4 \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}} \\cdot 2\\;\\text{l}} \\approx 35.0\\;\\text{K}\\), also bis \\(55\\;^\\circ\\text{C}\\).' },
      { text: 'Bei \\(30\\;\\text{K}\\) Erwärmung wächst eine Menge Ethanol um \\(99\\;\\text{ml}\\). Wie viel Ethanol ist es? Notiere deine Rechnung, dann stelle ein und erwärme.', ok: function(s){ return hat(s, 'et', 3, 50); },
        vergleich: '\\(V_0 = \\dfrac{\\Delta V}{\\gamma \\cdot \\Delta T} = \\dfrac{0.099\\;\\text{l}}{1.10 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 30\\;\\text{K}} = 3.0\\;\\text{l}\\), erwärmt bis \\(50\\;^\\circ\\text{C}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Meeresspiegelanstieg ----------
     Ein Schnitt durch das Meer (3700 m tief, nicht massstäblich in der Breite). Die oberste Schicht der
     Dicke h₀ erwärmt sich auf Knopfdruck um ΔT; sie dehnt sich nach Δh = γ · h₀ · ΔT aus
     (γ = 0.21·10⁻³ 1/K wie Themenseite, Fläche fest, Tiefenwasser unverändert). Der Pegel links zeigt
     den Anstieg in cm. Darunter Δh über ΔT für die eingestellte Schicht, der vorige Lauf gestrichelt.
     Unterschied zur Themenseite (Animation 4): dort die ganze Säule h₀ als eine Wassersäule; hier die
     erwärmte Schicht über kaltem Tiefenwasser, damit die Wahl von h₀ eine Frage ist.
     Clipbeispiel: 500 m, 1.5 K; Startwerte 1200 m, 0.8 K (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,186)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); dc = 0; zeichnen(); });
    var GW = 0.21e-3, dc = 0, lauf = null, laeufe = [], vorher = null, letzter = null, pruefen = function(){};
    function werte(){ var h0 = B.wert('h0'), dT = B.wert('dT'); return { h0: h0, dT: dT, dh: GW * h0 * dT }; }
    function fertig(w){ lauf = { h0: w.h0, dT: w.dT, dh: w.dh }; letzter = lauf; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(), u = Math.min(1, tt / 2.5); dc = w.dT * u; zeichnen(); if (u >= 1){ dc = w.dT; fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Erwärmen', function(){ vorher = letzter; if (WENIGER){ var w = werte(); dc = w.dT; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); dc = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); dc = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },   // vorher bleibt: Aufgabe 2 vergleicht mit dem Lauf aus Aufgabe 1
      // Testhaken: momentane Erwärmung in K (Bildfolgen der Clips)
      zeige: function(x){ uhr.stop(); dc = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), d = Math.round(dc * 10) / 10, dh = GW * w.h0 * d, cm = dh * 100;
      B.anzeigen(); leeren(szene); leeren(dia);
      var xs = 110, xr = 262, ys = 44, PXM = 120 / 3700;                     // Meeresoberfläche, 120 px für 3700 m
      el(szene, 'rect', { x: xs, y: ys, width: xr - xs, height: 120, 'class': 'meer' });
      if (d > 0) el(szene, 'rect', { x: xs, y: ys, width: xr - xs, height: w.h0 * PXM, 'class': 'warm', 'fill-opacity': 0.15 + 0.45 * Math.min(1, d / 3) });
      el(szene, 'line', { x1: xs, y1: ys + w.h0 * PXM, x2: xr, y2: ys + w.h0 * PXM, 'class': 'vorher' });
      el(szene, 'path', { d: 'M' + xr + ' ' + (ys - 14) + ' L' + xr + ' ' + (ys + 120) + ' L296 ' + (ys + 120) + ' L296 ' + (ys - 14) + ' Z', 'class': 'land' });
      el(szene, 'path', { d: 'M' + xs + ' ' + (ys + 120) + ' L' + xr + ' ' + (ys + 120), 'class': 'gefaess' });
      for (var m = 0; m <= 3000; m += 1000){ var yy = ys + m * PXM; el(szene, 'line', { x1: xs - 4, y1: yy, x2: xs, y2: yy, 'class': 'tick' }); el(szene, 'text', { x: xs - 6, y: yy + 3, 'text-anchor': 'end', 'class': 'skala' }, m + ' m'); }
      if (w.h0 * PXM > 8){
        el(szene, 'line', { x1: xs + 8, y1: ys, x2: xs + 8, y2: ys + w.h0 * PXM, 'class': 'masslinie' });
        el(szene, 'text', { x: xs + 12, y: ys + Math.min(w.h0 * PXM, 60) / 2 + 4, 'class': 'pf-text' }, 'h₀ = ' + zahl(w.h0) + NB + 'm' + (d > 0 ? '; +' + zahl(d) + NB + 'K' : ''));   // dunkle Schrift: auf dem braunen Grund lesbar
      }
      el(szene, 'text', { x: 186, y: ys + 100, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'kaltes Tiefenwasser: unverändert');
      // Pegel (Lupe): 0 bis 140 cm
      var px = 18, py0 = 160, kc = 120 / 140, yp = py0 - cm * kc;
      el(szene, 'rect', { x: px - 8, y: py0 - 124, width: 16, height: 124, 'class': 'pegel' });
      for (var c = 0; c <= 140; c += 20){ var yc = py0 - c * kc; el(szene, 'line', { x1: px + 8, y1: yc, x2: px + 13, y2: yc, 'class': 'tick' }); el(szene, 'text', { x: px + 16, y: yc + 3, 'class': 'skala' }, c + (c === 0 ? ' cm' : '')); }
      el(szene, 'rect', { x: px - 6, y: yp, width: 12, height: py0 - yp, 'class': 'pegel-wasser' });
      el(szene, 'line', { x1: px - 10, y1: py0, x2: px + 10, y2: py0, 'class': 'vorher' });
      if (vorher && !uhr.laeuft()) el(szene, 'line', { x1: px - 10, y1: py0 - vorher.dh * 100 * kc, x2: px + 10, y2: py0 - vorher.dh * 100 * kc, 'class': 'vorher' });
      el(szene, 'text', { x: 4, y: 14, 'class': 'bt-wert' }, 'Pegel');
      el(szene, 'path', { d: 'M' + (px + 44) + ' ' + yp + ' L' + (px + 44) + ' ' + (ys - 10) + ' L' + xs + ' ' + (ys - 10) + ' L' + xs + ' ' + ys, 'class': 'lupe', fill: 'none' });   // über den Tiefenmarken geführt
      el(szene, 'text', { x: xr - 4, y: 14, 'text-anchor': 'end', 'class': 'bt-wert t-dl' }, 'Δh = ' + sig(cm) + NB + 'cm');
      el(szene, 'text', { x: xr - 4, y: 30, 'text-anchor': 'end', 'class': 'bt-klein' }, 'γ = 0.21·10⁻³' + NB + '1/K');
      // Diagramm: Δh über ΔT
      K = Achsen(dia, { w: 300, h: 128, x0: -0.3, x1: 3.3, y0: -14, y1: 145, sx: 0.5, sy: 10, xm: [0.5, 1, 1.5, 2, 2.5, 3], ym: [20, 40, 60, 80, 100, 120, 140], xname: 'ΔT [K]', yname: 'Δh [cm]' });
      var kv = [[function(x){ return GW * w.h0 * x * 100; }, 0, 3]];
      if (vorher && !uhr.laeuft()){ K.kurve(function(x){ return GW * vorher.h0 * x * 100; }, 'vorher', 0, 3); kv.push([function(x){ return GW * vorher.h0 * x * 100; }, 0, 3]); }
      K.kurve(kv[0][0], 'kurve-dl', 0, 3);
      stext(K.ebene, { x: 0, y: 154, 'class': 'legende l-dl' }, '— h₀ = ' + zahl(w.h0) + NB + 'm');
      if (vorher && !uhr.laeuft()) stext(K.ebene, { x: 300, y: 154, 'text-anchor': 'end', 'class': 'legende' }, '- - voriger Lauf: h₀ = ' + zahl(vorher.h0) + NB + 'm');
      K.punkt(d, cm, 'p-dl');
      if (d > 0) K.etikett(d, cm, '(' + zahl(d) + NB + 'K; ' + sig(cm) + NB + 'cm)', 'p-dl', { kurven: kv });
      var z = '<span>Δ' + v_('h') + ' = ' + v_('γ') + ' · ' + v_('h') + '<sub>0</sub> · Δ' + v_('T') + ' = 0.21·10' + hoch('-3') + NB + '1/K · ' + zahl(w.h0) + NB + 'm · ' + zahl(d) + NB + 'K ' + ist(dh, sig(dh)) + sig(dh) + NB + 'm ' + ist(cm, sig(cm)) + sig(cm) + NB + 'cm</span>';
      z += '<span class="sim-notiz">Modell: Nur die oberste Schicht ' + v_('h') + '<sub>0</sub> erwärmt sich, die Meeresfläche bleibt gleich, γ wie für Wasser bei 20' + NB + '°C. Schmelzwasser von Gletschern ist nicht berücksichtigt.' + (vorher ? ' Grau: voriger Lauf.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, h0, dT){ var l = s.lauf; return l && l.h0 === h0 && Math.abs(l.dT - dT) < 1e-9; }
    pruefen = Leiste(fig, [
      { text: 'Die obersten \\(300\\;\\text{m}\\) erwärmen sich um \\(2\\;\\text{K}\\). Um wie viele Zentimeter steigt der Meeresspiegel? Notiere, dann stelle ein und erwärme.', ok: function(s){ return hat(s, 300, 2); },
        vergleich: '\\(\\Delta h = \\gamma \\cdot h_0 \\cdot \\Delta T = 0.21 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 300\\;\\text{m} \\cdot 2\\;\\text{K} = 0.126\\;\\text{m} = 12.6\\;\\text{cm}\\).' },
      { text: 'Gleiche Erwärmung, aber doppelt so dicke Schicht (\\(600\\;\\text{m}\\)). Was geschieht mit \\(\\Delta h\\)? Vergleiche mit dem grauen vorigen Lauf und begründe.', ok: function(s){ return hat(s, 600, 2); },
        vergleich: 'Doppelt so viel, \\(25.2\\;\\text{cm}\\): \\(\\Delta h\\) ist proportional zu \\(h_0\\). Jeder Meter der Schicht dehnt sich gleich viel aus, doppelt so viele Meter geben den doppelten Anstieg.' },
      { text: 'Welche Erwärmung der obersten \\(800\\;\\text{m}\\) hebt den Meeresspiegel um \\(10\\;\\text{cm}\\) (auf \\(0.1\\;\\text{K}\\) genau)? Notiere deine Rechnung, dann stelle ein und prüfe.', ok: function(s){ return hat(s, 800, 0.6); },
        vergleich: '\\(\\Delta T = \\dfrac{\\Delta h}{\\gamma \\cdot h_0} = \\dfrac{0.10\\;\\text{m}}{0.21 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 800\\;\\text{m}} \\approx 0.60\\;\\text{K}\\) (\\(\\Delta h \\approx 10.1\\;\\text{cm}\\)).' },
      { text: 'Bei \\(1\\;\\text{K}\\) Erwärmung steigt der Meeresspiegel um \\(42\\;\\text{cm}\\). Wie dick ist die erwärmte Schicht? Notiere deine Rechnung, dann stelle ein und prüfe.', ok: function(s){ return hat(s, 2000, 1); },
        vergleich: '\\(h_0 = \\dfrac{\\Delta h}{\\gamma \\cdot \\Delta T} = \\dfrac{0.42\\;\\text{m}}{0.21 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 1\\;\\text{K}} = 2000\\;\\text{m}\\).' },
      { text: 'Stelle das Grösste ein: \\(2000\\;\\text{m}\\) und \\(3\\;\\text{K}\\). Notiere \\(\\Delta h\\). Nenne zwei Gründe, warum der wirkliche Anstieg durch Erwärmung anders ausfällt als im Modell.', ok: function(s){ return hat(s, 2000, 3); },
        vergleich: '\\(\\Delta h = 0.21 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}} \\cdot 2000\\;\\text{m} \\cdot 3\\;\\text{K} = 1.26\\;\\text{m}\\). Gründe: \\(\\gamma\\) hängt von Temperatur und Salzgehalt ab (kaltes Wasser dehnt sich viel weniger aus); die Erwärmung nimmt mit der Tiefe ab, statt in einer Schicht gleich zu sein. Dazu kommt Schmelzwasser von Gletschern, das hier fehlt.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Ideales Gas, allgemeine Gasgleichung ----------
     Gas in einem Zylinder mit Kolben, feste Gasmenge. Zustand 1: 1.00 bar; 2.0 l; 20 °C (293.15 K).
     Regler für V₂ und ϑ₂; auf Knopfdruck geht das Gas gleichmässig vom Zustand 1 in den Zustand 2,
     der Druck folgt aus p₁ · V₁ / T₁ = p · V / T. Manometer (absoluter Druck), Thermometer, Kolben.
     Darunter das p-V-Diagramm: Zustand 1, der Weg und die Isothermen zu T₁ und T₂ (gestrichelt).
     Unterschied zur Themenseite (Animation 5): dort springt der Druck mit dem Regler; hier wird der
     Übergang zwischen zwei benannten Zuständen gezeigt, wie in der Rechnung mit Index 1 und 2.
     Clipbeispiel: 2.0 l und 80 °C; 1.0 l und 20 °C; Startwerte 1.6 l, 50 °C (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,186)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); u = 0; zeichnen(); });
    var P1 = 1.00, V1 = 2.0, TH1 = 20, u = 0, lauf = null, laeufe = [], pruefen = function(){};
    var PUNKTE = [];                                                           // feste Lage der Teilchen (0..1), damit nichts flackert
    for (var i = 0; i < 40; i++) PUNKTE.push([(0.5 + i * 0.7548776662) % 1, (0.5 + i * 0.5698402910) % 1]);   // R2-Folge: gleichmässig, ohne Streifen
    function werte(){ var V = B.wert('V'), t = B.wert('t'), T = t + T0K; return { V: V, t: t, T: T, p: P1 * V1 * T / ((TH1 + T0K) * V) }; }
    function fertig(w){ lauf = { V: w.V, t: w.t, p: w.p }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ u = Math.min(1, tt / 2.5); zeichnen(); if (u >= 1){ fertig(werte()); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Zustand ändern', function(){ if (WENIGER){ u = 1; fertig(werte()); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zustand 1', function(){ uhr.stop(); u = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); u = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      // Testhaken: Anteil des Wegs von Zustand 1 zu Zustand 2, 0 bis 1
      zeige: function(x){ uhr.stop(); u = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), V = +(V1 + (w.V - V1) * u).toFixed(1), t = Math.round(TH1 + (w.t - TH1) * u), T = t + T0K, p = P1 * V1 * T / ((TH1 + T0K) * V);
      B.anzeigen(); leeren(szene); leeren(dia);
      // Zylinder: 30 px je Liter, Boden bei y 168
      var xa = 104, xb = 176, yb = 168, PXL = 30, yk = yb - V * PXL;
      el(szene, 'rect', { x: xa, y: yk, width: xb - xa, height: yb - yk, 'class': 'gas' });
      PUNKTE.forEach(function(q){ el(szene, 'circle', { cx: xa + 4 + q[0] * (xb - xa - 8), cy: yk + 4 + q[1] * (yb - yk - 8), r: 1.8, 'class': 'teilchen' }); });
      el(szene, 'path', { d: 'M' + (xa - 2) + ' 30 L' + (xa - 2) + ' ' + (yb + 2) + ' L' + (xb + 2) + ' ' + (yb + 2) + ' L' + (xb + 2) + ' 30', 'class': 'gefaess' });
      el(szene, 'rect', { x: xa, y: yk - 8, width: xb - xa, height: 8, 'class': 'kolben' });
      el(szene, 'line', { x1: (xa + xb) / 2, y1: yk - 8, x2: (xa + xb) / 2, y2: 20, 'class': 'stange' });
      el(szene, 'line', { x1: xa - 10, y1: yb - V1 * PXL, x2: xb + 10, y2: yb - V1 * PXL, 'class': 'vorher' });
      el(szene, 'text', { x: xa - 12, y: yb - V1 * PXL + 3, 'text-anchor': 'end', 'class': 'bt-klein' }, 'Zustand 1');
      thermometer(szene, 30, 40, 120, t, -50, 150);
      el(szene, 'text', { x: 42, y: 60, 'class': 'bt-wert t-temp' }, minus(t) + NB + '°C');
      el(szene, 'text', { x: 42, y: 74, 'class': 'bt-klein' }, '= ' + zahl(+T.toFixed(2)) + NB + 'K');
      // Manometer 0 bis 6 bar (absolut)
      var mx = 252, my = 70, R = 30, ww = Math.min(p, 6) / 6;
      el(szene, 'circle', { cx: mx, cy: my, r: R, 'class': 'manometer' });
      for (var b = 0; b <= 6; b++){ var aa = Math.PI * (1.25 - 1.5 * b / 6); el(szene, 'line', { x1: mx + (R - 5) * Math.cos(aa), y1: my - (R - 5) * Math.sin(aa), x2: mx + R * Math.cos(aa), y2: my - R * Math.sin(aa), 'class': 'tick' }); el(szene, 'text', { x: mx + (R - 12) * Math.cos(aa), y: my - (R - 12) * Math.sin(aa) + 3, 'text-anchor': 'middle', 'class': 'skala klein' }, b); }
      var az = Math.PI * (1.25 - 1.5 * ww); el(szene, 'line', { x1: mx, y1: my, x2: mx + (R - 8) * Math.cos(az), y2: my - (R - 8) * Math.sin(az), 'class': 'zeiger' });
      el(szene, 'text', { x: mx, y: my + R + 13, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'p in bar (absolut)');
      el(szene, 'text', { x: mx, y: my + R + 28, 'text-anchor': 'middle', 'class': 'bt-wert t-druck' }, p.toFixed(2) + NB + 'bar');
      el(szene, 'text', { x: mx, y: my + R + 46, 'text-anchor': 'middle', 'class': 'bt-wert t-vol' }, 'V = ' + V.toFixed(1) + NB + 'l');
      el(szene, 'path', { d: 'M' + (xb + 2) + ' ' + (yb - 6) + ' L' + (mx - R - 24) + ' ' + (yb - 6) + ' L' + (mx - R - 24) + ' ' + my + ' L' + (mx - R) + ' ' + my, 'class': 'schlauch', fill: 'none' });
      // Diagramm: p über V
      K = Achsen(dia, { w: 300, h: 128, x0: -0.3, x1: 4.9, y0: -0.6, y1: 6.4, sx: 0.5, sy: 1, xm: [1, 2, 3, 4], ym: [1, 2, 3, 4, 5, 6], xname: 'V [l]', yname: 'p [bar]' });
      var c1 = P1 * V1, c2 = P1 * V1 * T / (TH1 + T0K);   // Isotherme durch den Zustand im Bild
      K.kurve(function(x){ return c1 / x; }, 'vorher hilfslinie', 0.32, 4.3);
      if (Math.abs(t - TH1) > 0.5) K.kurve(function(x){ return c2 / x; }, 'kurve-iso hilfslinie', 0.32, 4.3);
      if (u > 0){ var d = 'M' + K.X(V1).toFixed(1) + ' ' + K.Y(P1).toFixed(1); for (var j = 1; j <= 30; j++){ var s = u * j / 30, Vs = V1 + (w.V - V1) * s, Ts = TH1 + T0K + (w.t - TH1) * s; d += ' L' + K.X(Vs).toFixed(1) + ' ' + K.Y(P1 * V1 * Ts / ((TH1 + T0K) * Vs)).toFixed(1); } el(K.ebene, 'path', { d: d, 'class': 'weg', 'clip-path': K.clip }); }
      K.punkt(V1, P1, 'p-eins', '1', -12, -6, 'middle');
      K.punkt(V, p, 'p-dl');
      if (u > 0.02) K.etikett(V, p, '(' + V.toFixed(1) + NB + 'l; ' + p.toFixed(2) + NB + 'bar)', 'p-dl', { kurven: [[function(x){ return c1 / x; }, 0.32, 4.3], [function(x){ return c2 / x; }, 0.32, 4.3]], });
      stext(K.ebene, { x: 0, y: 154, 'class': 'legende hilfslinie' }, '- - Isotherme bei T₁ = 293.15' + NB + 'K');
      if (Math.abs(t - TH1) > 0.5) stext(K.ebene, { x: 300, y: 154, 'text-anchor': 'end', 'class': 'legende t-temp hilfslinie' }, '- - bei T = ' + zahl(+T.toFixed(2)) + NB + 'K');
      // Formelzeilen: der Zustand im Bild (nach dem Lauf: Zustand 2)
      var z = '<span>' + T_('2') + ' [K] = ' + v_('ϑ') + '<sub>2</sub> [°C] + 273.15 = ' + minus(t) + ' + 273.15 = ' + zahl(+T.toFixed(2)) + '</span>';
      z += '<span>' + p_('2') + ' = ' + p_('1') + ' · ' + V_('1') + ' · ' + T_('2') + ' / (' + T_('1') + ' · ' + V_('2') + ') = 1.00' + NB + 'bar · 2.0' + NB + 'l · ' + zahl(+T.toFixed(2)) + NB + 'K / (293.15' + NB + 'K · ' + V.toFixed(1) + NB + 'l) ' + ist(p, p.toFixed(2)) + p.toFixed(2) + NB + 'bar</span>';
      z += '<span class="sim-notiz">Zustand 1: ' + p_('1') + ' = 1.00' + NB + 'bar; ' + V_('1') + ' = 2.0' + NB + 'l; ' + v_('ϑ') + '<sub>1</sub> = 20' + NB + '°C (' + T_('1') + ' = 293.15' + NB + 'K). Gasmenge fest, Druck absolut. Die Formelzeile zeigt den Zustand im Bild.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, V, t){ var l = s.lauf; return l && Math.abs(l.V - V) < 1e-9 && l.t === t; }
    pruefen = Leiste(fig, [
      { text: 'Erwärme das Gas auf \\(100\\;^\\circ\\text{C}\\), das Volumen bleibt \\(2.0\\;\\text{l}\\). Wie gross ist \\(p_2\\)? Notiere, dann vergleiche.', ok: function(s){ return hat(s, 2, 100); },
        vergleich: '\\(T_2 = 373.15\\;\\text{K}\\). \\(p_2 = \\dfrac{p_1 \\cdot V_1 \\cdot T_2}{T_1 \\cdot V_2} = \\dfrac{1.00\\;\\text{bar} \\cdot 2.0\\;\\text{l} \\cdot 373.15\\;\\text{K}}{293.15\\;\\text{K} \\cdot 2.0\\;\\text{l}} \\approx 1.27\\;\\text{bar}\\).' },
      { text: 'Stelle \\(40\\;^\\circ\\text{C}\\) ein (Volumen \\(2.0\\;\\text{l}\\)). Die Celsius-Zahl hat sich verdoppelt — der Druck auch? Notiere \\(p_2\\) und begründe.', ok: function(s){ return hat(s, 2, 40); },
        vergleich: 'Nein: \\(p_2 = 1.00\\;\\text{bar} \\cdot \\dfrac{313.15\\;\\text{K}}{293.15\\;\\text{K}} \\approx 1.07\\;\\text{bar}\\). Der Druck hängt an der absoluten Temperatur, und die steigt nur von \\(293\\;\\text{K}\\) auf \\(313\\;\\text{K}\\), um knapp \\(7\\;\\%\\).' },
      { text: 'Drücke das Gas bei \\(20\\;^\\circ\\text{C}\\) auf \\(0.5\\;\\text{l}\\) zusammen. Notiere \\(p_2\\). Warum steigt der Druck? Begründe mit den Teilchen.', ok: function(s){ return hat(s, 0.5, 20); },
        vergleich: '\\(p_2 = 1.00\\;\\text{bar} \\cdot \\dfrac{2.0\\;\\text{l}}{0.5\\;\\text{l}} = 4.0\\;\\text{bar}\\), viermal so viel. Gleich schnelle Teilchen haben weniger Platz und treffen öfter auf die Wand.' },
      { text: 'Beides zusammen: \\(V_2 = 1.2\\;\\text{l}\\) und \\(\\vartheta_2 = 80\\;^\\circ\\text{C}\\). Rechne \\(p_2\\) zuerst, dann stelle ein und prüfe.', ok: function(s){ return hat(s, 1.2, 80); },
        vergleich: '\\(p_2 = \\dfrac{1.00\\;\\text{bar} \\cdot 2.0\\;\\text{l} \\cdot 353.15\\;\\text{K}}{293.15\\;\\text{K} \\cdot 1.2\\;\\text{l}} \\approx 2.01\\;\\text{bar}\\).' },
      { text: 'Bei \\(V_2 = 1.5\\;\\text{l}\\) soll der Druck \\(1.50\\;\\text{bar}\\) sein. Welche Temperatur braucht es (auf \\(5\\;^\\circ\\text{C}\\) genau)? Notiere deine Rechnung, dann stelle ein und prüfe.', ok: function(s){ var l = s.lauf; return l && Math.abs(l.V - 1.5) < 1e-9 && Math.abs(l.p - 1.5) <= 0.01; },
        vergleich: '\\(T_2 = \\dfrac{p_2 \\cdot V_2 \\cdot T_1}{p_1 \\cdot V_1} = \\dfrac{1.50\\;\\text{bar} \\cdot 1.5\\;\\text{l} \\cdot 293.15\\;\\text{K}}{1.00\\;\\text{bar} \\cdot 2.0\\;\\text{l}} \\approx 329.8\\;\\text{K} \\approx 56.6\\;^\\circ\\text{C}\\). Auf dem Regler passt \\(55\\;^\\circ\\text{C}\\) (\\(1.49\\;\\text{bar}\\)).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Spezialfälle ----------
     Dieselbe feste Gasmenge, Zustand 1: 1.00 bar; 3.0 l; 20 °C. Ein Knopf wählt, was konstant bleibt:
     isotherm (Wasserbad, Regler V), isobar (frei beweglicher Kolben mit Gewicht, Regler ϑ) oder
     isochor (starre Flasche, Regler ϑ). Auf Knopfdruck läuft die Zustandsänderung; darunter das
     passende Diagramm: p-V (Hyperbel), V-T bzw. p-T in Kelvin (Ursprungsgerade, Verlängerung zum
     absoluten Nullpunkt gestrichelt).
     Unterschied zur Themenseite (Animation 6): dort Boyle-Mariotte und Amontons mit verschiebbarem
     Arbeitspunkt; hier alle drei Fälle mit dem Bild, das zeigt, warum die Grösse konstant bleibt.
     Clipbeispiel: Hyperbel 3 → 1.5 l, Geraden über 293 K; Startwerte isotherm, 2.4 l (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,186)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); u = 0; felder(); zeichnen(); });
    var P1 = 1.00, V1 = 3.0, TH1 = 20, T1 = TH1 + T0K, u = 0, lauf = null, laeufe = [], pruefen = function(){};
    var NAME = { T: 'isotherm', p: 'isobar', V: 'isochor' };
    function felder(){ var m = B.wert('fall'); fig.querySelectorAll('.reglerfeld[data-fall]').forEach(function(r){ r.hidden = r.dataset.fall.indexOf(m) < 0; }); }
    function werte(){
      var m = B.wert('fall'), V = m === 'T' ? B.wert('V') : V1, t = m === 'T' ? TH1 : B.wert('t'), T = t + T0K;
      var w = { fall: m, t: t, T: T, V: V, p: P1 };
      if (m === 'T') w.p = P1 * V1 / V; else if (m === 'p') w.V = V1 * T / T1; else w.p = P1 * T / T1;
      return w;
    }
    function fertig(w){ lauf = { fall: w.fall, V: +w.V.toFixed(6), t: w.t, p: +w.p.toFixed(6) }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ u = Math.min(1, tt / 2.5); zeichnen(); if (u >= 1){ fertig(werte()); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Zustand ändern', function(){ if (WENIGER){ u = 1; fertig(werte()); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zustand 1', function(){ uhr.stop(); u = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); u = 0; B.setze(o); felder(); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); u = x; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), m = w.fall;
      var t = Math.round((TH1 + (w.t - TH1) * u) / 5) * 5, T = t + T0K, V = m === 'T' ? +(V1 + (w.V - V1) * u).toFixed(1) : (m === 'p' ? V1 * T / T1 : V1), p = P1 * V1 * T / (T1 * V);
      B.anzeigen(); leeren(szene); leeren(dia);
      el(szene, 'text', { x: 4, y: 14, 'class': 'bt-wert' }, NAME[m] + ': ' + (m === 'T' ? 'T bleibt konstant' : (m === 'p' ? 'p bleibt konstant' : 'V bleibt konstant')));
      // Zylinder bzw. Flasche: 20 px je Liter, Boden bei y 172
      var xa = 110, xb = 170, yb = 172, PXL = 20, yk = yb - V * PXL;
      if (m === 'T') el(szene, 'rect', { x: xa - 18, y: yb - 64, width: xb - xa + 36, height: 70, rx: 4, 'class': 'bad' });
      el(szene, 'rect', { x: xa, y: yk, width: xb - xa, height: yb - yk, 'class': 'gas' });
      for (var i = 0; i < 30; i++){ var qx = (0.5 + i * 0.7548776662) % 1, qy = (0.5 + i * 0.5698402910) % 1; el(szene, 'circle', { cx: xa + 4 + qx * (xb - xa - 8), cy: yk + 4 + qy * (yb - yk - 8), r: 1.8, 'class': 'teilchen' }); }
      if (m === 'V'){
        el(szene, 'path', { d: 'M' + (xa - 3) + ' ' + (yb - V1 * PXL - 3) + ' L' + (xa - 3) + ' ' + (yb + 3) + ' L' + (xb + 3) + ' ' + (yb + 3) + ' L' + (xb + 3) + ' ' + (yb - V1 * PXL - 3) + ' Z', 'class': 'flasche-wand' });
        el(szene, 'text', { x: (xa + xb) / 2, y: yb - V1 * PXL - 10, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'starre Flasche');
      } else {
        el(szene, 'path', { d: 'M' + (xa - 2) + ' 34 L' + (xa - 2) + ' ' + (yb + 2) + ' L' + (xb + 2) + ' ' + (yb + 2) + ' L' + (xb + 2) + ' 34', 'class': 'gefaess' });
        el(szene, 'rect', { x: xa, y: yk - 7, width: xb - xa, height: 7, 'class': 'kolben' });
        el(szene, 'line', { x1: xa - 10, y1: yb - V1 * PXL, x2: xb + 10, y2: yb - V1 * PXL, 'class': 'vorher' });
        if (m === 'p'){ el(szene, 'rect', { x: xa + 14, y: yk - 25, width: xb - xa - 28, height: 18, 'class': 'gewicht' }); el(szene, 'text', { x: (xa + xb) / 2, y: yk - 12, 'text-anchor': 'middle', 'class': 'saeule-text' }, 'Gewicht'); }
        else { el(szene, 'line', { x1: (xa + xb) / 2, y1: yk - 7, x2: (xa + xb) / 2, y2: 26, 'class': 'stange' }); el(szene, 'text', { x: xb + 22, y: yb - 16, 'class': 'bt-klein' }, 'Wasserbad 20' + NB + '°C:'); el(szene, 'text', { x: xb + 22, y: yb - 4, 'class': 'bt-klein' }, 'langsam drücken'); }
      }
      el(szene, 'text', { x: 296, y: 80, 'text-anchor': 'end', 'class': 'bt-wert t-vol' }, 'V = ' + (m === 'p' ? sig(V) : V.toFixed(1)) + NB + 'l');
      thermometer(szene, 34, 40, 120, t, -150, 330);
      el(szene, 'text', { x: 46, y: 60, 'class': 'bt-wert t-temp' }, minus(t) + NB + '°C');
      el(szene, 'text', { x: 46, y: 74, 'class': 'bt-klein' }, '= ' + zahl(+T.toFixed(2)) + NB + 'K');
      el(szene, 'text', { x: 296, y: 60, 'text-anchor': 'end', 'class': 'bt-wert t-druck' }, 'p = ' + p.toFixed(2) + NB + 'bar');
      // Diagramm je Fall
      var o, f, x0, x1, xm, cur, ziel;
      if (m === 'T'){ o = { x0: -0.4, x1: 7.1, y0: -0.6, y1: 6.5, sx: 0.5, sy: 1, xm: [1, 2, 3, 4, 5, 6], ym: [1, 2, 3, 4, 5, 6], xname: 'V [l]', yname: 'p [bar]' }; f = function(x){ return P1 * V1 / x; }; x0 = 0.5; x1 = 5.8; cur = [V, p]; ziel = '(' + V.toFixed(1) + NB + 'l; ' + p.toFixed(2) + NB + 'bar)'; }
      else if (m === 'p'){ o = { x0: -40, x1: 660, y0: -0.6, y1: 7, sx: 50, sy: 1, xm: [100, 200, 300, 400, 500, 600], ym: [1, 2, 3, 4, 5, 6], xname: 'T [K]', yname: 'V [l]' }; f = function(x){ return V1 * x / T1; }; x0 = 123.15; x1 = 603.15; cur = [T, V]; ziel = '(' + zahl(+T.toFixed(2)) + NB + 'K; ' + sig(V) + NB + 'l)'; }
      else { o = { x0: -40, x1: 660, y0: -0.2, y1: 2.3, sx: 50, sy: 0.25, xm: [100, 200, 300, 400, 500, 600], ym: [0.5, 1, 1.5, 2], xname: 'T [K]', yname: 'p [bar]' }; f = function(x){ return P1 * x / T1; }; x0 = 123.15; x1 = 603.15; cur = [T, p]; ziel = '(' + zahl(+T.toFixed(2)) + NB + 'K; ' + p.toFixed(2) + NB + 'bar)'; }
      o.w = 300; o.h = 128;
      K = Achsen(dia, o);
      if (m !== 'T') K.kurve(f, 'kurve-hilf hilfslinie', 0, x0);                 // Verlängerung zum absoluten Nullpunkt
      K.kurve(f, 'kurve-dl', x0, x1);
      var e1 = m === 'T' ? [V1, P1] : (m === 'p' ? [T1, V1] : [T1, P1]);
      K.punkt(e1[0], e1[1], 'p-eins', '1', -10, -7, 'middle');
      K.punkt(cur[0], cur[1], 'p-dl');
      if (u > 0.02) K.etikett(cur[0], cur[1], ziel, 'p-dl', { kurven: [[f, 0, x1]] });
      stext(K.ebene, { x: 0, y: 154, 'class': 'legende l-dl' }, m === 'T' ? '— Hyperbel: p · V konstant' : (m === 'p' ? '— V / T konstant' : '— p / T konstant'));
      if (m !== 'T') stext(K.ebene, { x: 300, y: 154, 'text-anchor': 'end', 'class': 'legende hilfslinie' }, '- - Verlängerung bis 0 K');
      var z;   // der Zustand im Bild (nach dem Lauf: Zustand 2)
      if (m === 'T') z = '<span>' + p_('1') + ' · ' + V_('1') + ' = ' + p_('2') + ' · ' + V_('2') + ': ' + p_('2') + ' = ' + p_('1') + ' · ' + V_('1') + ' / ' + V_('2') + ' = 1.00' + NB + 'bar · 3.0' + NB + 'l / ' + V.toFixed(1) + NB + 'l ' + ist(p, p.toFixed(2)) + p.toFixed(2) + NB + 'bar</span>';
      else if (m === 'p') z = '<span>' + V_('1') + ' / ' + T_('1') + ' = ' + V_('2') + ' / ' + T_('2') + ': ' + V_('2') + ' = ' + V_('1') + ' · ' + T_('2') + ' / ' + T_('1') + ' = 3.0' + NB + 'l · ' + zahl(+T.toFixed(2)) + NB + 'K / 293.15' + NB + 'K ' + ist(V, sig(V)) + sig(V) + NB + 'l</span>';
      else z = '<span>' + p_('1') + ' / ' + T_('1') + ' = ' + p_('2') + ' / ' + T_('2') + ': ' + p_('2') + ' = ' + p_('1') + ' · ' + T_('2') + ' / ' + T_('1') + ' = 1.00' + NB + 'bar · ' + zahl(+T.toFixed(2)) + NB + 'K / 293.15' + NB + 'K ' + ist(p, p.toFixed(2)) + p.toFixed(2) + NB + 'bar</span>';
      z += '<span class="sim-notiz">Aus ' + p_('1') + ' · ' + V_('1') + ' / ' + T_('1') + ' = ' + p_('2') + ' · ' + V_('2') + ' / ' + T_('2') + ' fällt die konstante Grösse ' + (m === 'T' ? v_('T') : (m === 'p' ? v_('p') : v_('V'))) + ' heraus. Zustand 1: 1.00' + NB + 'bar; 3.0' + NB + 'l; 20' + NB + '°C (293.15' + NB + 'K).</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, f, V, t){ var l = s.lauf; return l && l.fall === f && (V == null || Math.abs(l.V - V) < 1e-9) && (t == null || l.t === t); }
    pruefen = Leiste(fig, [
      { text: 'Isotherm: Drücke das Gas auf \\(0.6\\;\\text{l}\\) zusammen. Notiere \\(p_2\\) und begründe mit \\(p \\cdot V\\).', ok: function(s){ return hat(s, 'T', 0.6, null); },
        vergleich: '\\(p_2 = \\dfrac{p_1 \\cdot V_1}{V_2} = \\dfrac{1.00\\;\\text{bar} \\cdot 3.0\\;\\text{l}}{0.6\\;\\text{l}} = 5.0\\;\\text{bar}\\). Das Produkt \\(p \\cdot V\\) bleibt \\(3\\;\\text{bar} \\cdot \\text{l}\\): \\(5.0\\;\\text{bar} \\cdot 0.6\\;\\text{l} = 3\\;\\text{bar} \\cdot \\text{l}\\). Das Volumen sinkt auf ein Fünftel, der Druck steigt auf das Fünffache.' },
      { text: 'Isobar: Kühle auf \\(-50\\;^\\circ\\text{C}\\) ab. Notiere \\(V_2\\). Unter \\(0\\;^\\circ\\text{C}\\) — warum wird das Volumen trotzdem nicht null? Begründe.', ok: function(s){ return hat(s, 'p', null, -50); },
        vergleich: '\\(V_2 = V_1 \\cdot \\dfrac{T_2}{T_1} = 3.0\\;\\text{l} \\cdot \\dfrac{223.15\\;\\text{K}}{293.15\\;\\text{K}} \\approx 2.28\\;\\text{l}\\). Proportional ist \\(V\\) zur absoluten Temperatur: \\(-50\\;^\\circ\\text{C}\\) sind noch \\(223\\;\\text{K}\\). Null wäre es erst bei \\(0\\;\\text{K}\\) — vorher wird das Gas flüssig.' },
      { text: 'Isochor: Bei welcher Temperatur ist der Druck \\(1.5\\)-mal so gross wie im Zustand 1 (auf \\(5\\;^\\circ\\text{C}\\) genau)? Notiere deine Rechnung, dann stelle ein und prüfe.', ok: function(s){ var l = s.lauf; return l && l.fall === 'V' && Math.abs(l.p - 1.5) <= 0.01; },
        vergleich: '\\(T_2 = T_1 \\cdot \\dfrac{p_2}{p_1} = 293.15\\;\\text{K} \\cdot 1.5 \\approx 439.7\\;\\text{K}\\), also \\(\\vartheta_2 \\approx 166.6\\;^\\circ\\text{C}\\). Auf dem Regler \\(165\\;^\\circ\\text{C}\\) (\\(1.49\\;\\text{bar}\\)). In Grad Celsius hätte man fälschlich \\(30\\;^\\circ\\text{C}\\) gerechnet.' },
      { text: 'Isobar: Erwärme auf \\(100\\;^\\circ\\text{C}\\) und notiere \\(V_2\\). Wohin zeigt die gestrichelte Verlängerung der Geraden? Was bedeutet das?', ok: function(s){ return hat(s, 'p', null, 100); },
        vergleich: '\\(V_2 = 3.0\\;\\text{l} \\cdot \\dfrac{373.15\\;\\text{K}}{293.15\\;\\text{K}} \\approx 3.82\\;\\text{l}\\). Die Gerade zeigt auf den Ursprung, \\(T = 0\\;\\text{K}\\): Volumen und absolute Temperatur sind proportional.' },
      { text: 'Eine zugehaltene Spritze wird langsam zusammengedrückt, bis der Druck \\(1.2\\;\\text{bar}\\) beträgt. Wähle den passenden Fall, stelle ein und ändere den Zustand. Welches Volumen bleibt?', ok: function(s){ return hat(s, 'T', 2.5, null); },
        vergleich: 'Isotherm (langsam, die Temperatur bleibt): \\(V_2 = \\dfrac{p_1 \\cdot V_1}{p_2} = \\dfrac{1.00\\;\\text{bar} \\cdot 3.0\\;\\text{l}}{1.2\\;\\text{bar}} = 2.5\\;\\text{l}\\).' }
    ], sim);
    felder();
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

    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/\u2212/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)(e[-+]?\d+)?$/i.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    function erg(x, u){ var r = +(+x).toPrecision(3); return (Math.abs(r - x) < 1e-9 * Math.max(1, Math.abs(x)) ? '= ' : '\\approx ') + (u === 'Ω' ? tz(r) + '\\;\\Omega' : ein(r, u)); }
    // Feste Beispiele (Clips, Kontrollfragen, Leisten, Festhalten, Kapitelaufgaben, Gesamttest, Themenseite):
    // Zufallsübungen dürfen sie nicht treffen. Die Wertelisten der Typen schliessen sie fast alle schon aus;
    // hier steht nur, was die Listen sonst treffen könnten (jede Bedingung kann eintreten).
    function fest_(a){ return a.join('|'); }
    var FEST = {};   // keine Kombination der Wertelisten trifft ein festes Beispiel (geprüft 07.10.2026)
    function istFest(typ, a){ return (FEST[typ] || []).indexOf(fest_(a)) >= 0; }
    // Fehlermuster müssen verschiedene Zahlen ergeben (HOWTO §15): alle Werte paarweise 2 % auseinander
    function verschieden(l){ for (var i = 0; i < l.length; i++) for (var j = i + 1; j < l.length; j++) if (Math.abs(l[i] - l[j]) <= 0.02 * Math.max(Math.abs(l[i]), Math.abs(l[j]))) return false; return true; }
    var TK = 273.15;
    var WERK = [['Stahl', 12e-6, '12'], ['Messing', 18.4e-6, '18.4'], ['Aluminium', 23.8e-6, '23.8']];
    function al(z){ return z + ' \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}}'; }               // α oder γ eines Festkörpers
    function gm(z){ return z + ' \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}}'; }               // γ einer Flüssigkeit
    function gr(t){ return tz(t) + '\\;^\\circ\\text{C}'; }
    function kel(x){ return tz(x) + '\\;\\text{K}'; }
    function kla(s, x){ return x < 0 ? '(' + s + ')' : s; }                                // negative Werte in Klammern
    function cm3(x){ return tz(x) + '\\;\\text{cm}^3'; }
    function r3(x){ return +(+x).toPrecision(3); }
    function ergT(t){ var r = Math.round(t * 10) / 10; return (Math.abs(r - t) < 1e-9 ? '= ' : '\\approx ') + tz(r) + '\\;^\\circ\\text{C}'; }
    function nahT(a, b){ return Math.abs(a - b) <= 0.25; }                                  // Temperaturen: auf 0.25 °C
    var GW = 0.21e-3;                                                                       // γ von Wasser bei 20 °C (Themenseite)

    var TYPEN = {
      /* ----- Kapitel 1: Längenausdehnung ----- */
      'laenge': { felder: ['d'], muster: 'Δ<i>l</i> = {d} mm',
        neu: function(){
          var o, m, l0, t1, t2, dT, d;
          do { o = zufall([['Eine Stahlschiene', 0, [18, 36, 54]], ['Ein Stahlträger', 0, [8, 14, 22]], ['Ein Messingrohr', 1, [1.5, 2.4, 3.6]], ['Ein Aluminiumprofil', 2, [2.5, 4.5, 6]]]);
               m = WERK[o[1]]; l0 = zufall(o[2]); t1 = zufall([-12, -4, 6, 15, 22]); t2 = zufall([-18, -7, 28, 37, 52]); dT = t2 - t1; d = m[1] * l0 * dT * 1000; }
          while (Math.abs(dT) < 10 || !verschieden([d, -d, d / 1000, m[1] * l0 * t2 * 1000, m[1] * l0 * (t2 + TK) * 1000].concat(t1 < 0 ? [m[1] * l0 * (t2 + t1) * 1000] : [])));
          return { d: d, a: m[1], z: m[2], l0: l0, t1: t1, t2: t2, dT: dT,
            text: o[0] + ' (' + m[0] + ', \\(\\alpha = ' + al(m[2]) + '\\)) ist bei \\(' + gr(t1) + '\\) genau \\(' + ein(l0, 'm') + '\\) lang. Um wie viel ändert sich seine Länge bis \\(' + gr(t2) + '\\)? Gib \\(\\Delta l\\) mit Vorzeichen an.' }; },
        pruefen: function(A, e){
          if (nah(e.d, A.d)) return null;
          if (nah(e.d, -A.d)) return 'Das Vorzeichen: ' + (A.dT < 0 ? 'Beim Abkühlen ist \\(\\Delta T\\) negativ, der Körper wird kürzer.' : 'Beim Erwärmen wird der Körper länger, \\(\\Delta l\\) ist positiv.');
          if (nah(e.d, A.d / 1000)) return 'Das ist \\(\\Delta l\\) in Meter. Gefragt sind Millimeter: \\(1\\;\\text{m} = 1000\\;\\text{mm}\\).';
          if (nah(e.d, A.a * A.l0 * A.t2 * 1000) || nah(e.d, A.a * A.l0 * (A.t2 + TK) * 1000)) return 'In die Formel gehört die Temperaturdifferenz \\(\\Delta T = \\vartheta_2 - \\vartheta_1\\), nicht eine Temperatur.';
          if (A.t1 < 0 && nah(e.d, A.a * A.l0 * (A.t2 + A.t1) * 1000)) return 'Achte auf das Minus der Anfangstemperatur: \\(\\Delta T = ' + gr(A.t2) + ' - (' + gr(A.t1) + ')\\).';
          return '\\(\\Delta l = \\alpha \\cdot l_0 \\cdot \\Delta T\\) mit \\(\\Delta T = \\vartheta_2 - \\vartheta_1\\), Ergebnis in mm.'; },
        fehler: function(A){ var l = [[{ d: String(-A.d) }, 'Das Vorzeichen:'], [{ d: String(A.d / 1000) }, 'Millimeter'], [{ d: String(A.a * A.l0 * A.t2 * 1000) }, 'Temperaturdifferenz']];
          if (A.t1 < 0) l.push([{ d: String(A.a * A.l0 * (A.t2 + A.t1) * 1000) }, 'Minus der Anfangstemperatur']); return l; },
        loesung: function(A){ return '\\Delta T = ' + gr(A.t2) + ' - ' + kla(gr(A.t1), A.t1) + ' = ' + kel(A.dT) + ',\\quad \\Delta l = \\alpha \\cdot l_0 \\cdot \\Delta T = ' + al(A.z) + ' \\cdot ' + ein(A.l0, 'm') + ' \\cdot ' + kla(kel(A.dT), A.dT) + ' ' + erg(A.d / 1000, 'm') + ' ' + erg(A.d, 'mm'); } },
      'temperatur': { felder: ['t'], muster: '<i>ϑ</i><sub>2</sub> = {t} °C',
        neu: function(){
          var o, m, l0, s, t1, dT;
          do { o = zufall([['einem Stahlträger', 0, [15, 24, 32]], ['einem Aluminiumgeländer', 2, [4, 6, 9]], ['einem Messingrohr', 1, [3, 5, 7]]]);
               m = WERK[o[1]]; l0 = zufall(o[2]); s = zufall([4, 6, 9]); t1 = zufall([-5, 5, 12, 18]); dT = s / 1000 / (m[1] * l0); }
          while (dT < 8 || t1 + dT > 75);
          return { t: t1 + dT, dT: dT, a: m[1], z: m[2], l0: l0, s: s, t1: t1,
            text: 'Zwischen ' + o[0] + ' (' + m[0] + ', \\(\\alpha = ' + al(m[2]) + '\\), \\(l_0 = ' + ein(l0, 'm') + '\\)) und der Mauer bleibt bei \\(' + gr(t1) + '\\) eine Fuge von \\(' + ein(s, 'mm') + '\\). Das andere Ende ist fest. Bei welcher Temperatur schliesst sich die Fuge?' }; },
        pruefen: function(A, e){
          if (nahT(e.t, A.t)) return null;
          if (nahT(e.t, A.dT)) return 'Das ist die Temperaturänderung \\(\\Delta T\\). Gesucht ist die Temperatur: \\(\\vartheta_2 = \\vartheta_1 + \\Delta T\\).';
          if (nahT(e.t, A.t + TK)) return 'Das ist die Temperatur in Kelvin. Gefragt ist sie in °C.';
          if (Math.abs(e.t - A.t1) > 100 && (nah(e.t, A.t1 + A.dT * 1000) || nah(e.t, A.dT * 1000))) return 'Die Fugenbreite in Meter einsetzen: \\(' + ein(A.s, 'mm') + ' = ' + ein(A.s / 1000, 'm') + '\\).';
          return 'Erst \\(\\Delta T = \\dfrac{\\Delta l}{\\alpha \\cdot l_0}\\), dann \\(\\vartheta_2 = \\vartheta_1 + \\Delta T\\).'; },
        fehler: function(A){ return [[{ t: String(A.dT) }, 'Temperaturänderung'], [{ t: String(A.t + TK) }, 'Kelvin'], [{ t: String(A.t1 + A.dT * 1000) }, 'Fugenbreite']]; },
        loesung: function(A){ return '\\Delta T = \\dfrac{\\Delta l}{\\alpha \\cdot l_0} = \\dfrac{' + ein(A.s / 1000, 'm') + '}{' + al(A.z) + ' \\cdot ' + ein(A.l0, 'm') + '} ' + erg(A.dT, 'K') + ',\\quad \\vartheta_2 = \\vartheta_1 + \\Delta T ' + ergT(A.t); } },
      'alpha': { felder: ['a', 'm'], muster: '<i>α</i> = {a} · 10⁻⁶ 1/K; Werkstoff: {m:Stahl|Messing|Aluminium}',
        neu: function(){
          var m = zufall(WERK), l0 = zufall([1.2, 2.0, 2.5, 3.2]), dT = zufall([35, 45, 60, 75]), dl = r3(m[1] * l0 * dT * 1000);
          return { a: dl / 1000 / (l0 * dT) * 1e6, m: m[0], l0: l0, dT: dT, dl: dl,
            text: 'Ein Stab ist \\(' + ein(l0, 'm') + '\\) lang. Er wird um \\(' + kel(dT) + '\\) erwärmt und dabei \\(' + ein(dl, 'mm') + '\\) länger. Bestimme \\(\\alpha\\) und den Werkstoff (Stahl \\(12\\), Messing \\(18.4\\), Aluminium \\(23.8\\), je \\(10^{-6}\\;\\tfrac{1}{\\text{K}}\\)).' }; },
        pruefen: function(A, e){
          if (nah(e.a, A.a)) return e.m === A.m ? null : '\\(\\alpha\\) stimmt. Vergleiche den Wert mit der Tabelle: Welcher Werkstoff hat ihn?';
          if (nah(e.a, A.a * 1e-6)) return 'Gib nur die Zahl vor \\(10^{-6}\\) ein.';
          if (nah(e.a, A.a * 1000)) return '\\(\\Delta l\\) in Meter einsetzen: \\(' + ein(A.dl, 'mm') + ' = ' + ein(A.dl / 1000, 'm') + '\\).';
          if (nah(e.a, A.a * A.dT)) return 'Auch durch \\(\\Delta T\\) teilen: \\(\\alpha = \\dfrac{\\Delta l}{l_0 \\cdot \\Delta T}\\).';
          if (nah(e.a * 1e-6, 1 / (A.a * 1e-6)) || nah(e.a, 1 / (A.a * 1e-6))) return 'Umgekehrt: \\(\\alpha = \\dfrac{\\Delta l}{l_0 \\cdot \\Delta T}\\), nicht der Kehrwert.';
          return '\\(\\alpha = \\dfrac{\\Delta l}{l_0 \\cdot \\Delta T}\\), \\(\\Delta l\\) in Meter.'; },
        fehler: function(A){ var b = A.m === 'Stahl' ? 'Messing' : 'Stahl'; return [[{ a: String(A.a), m: b }, 'Tabelle'], [{ a: String(A.a * 1000), m: A.m }, 'in Meter'], [{ a: String(A.a * A.dT), m: A.m }, 'teilen'], [{ a: String(1 / (A.a * 1e-6)), m: A.m }, 'Kehrwert']]; },
        loesung: function(A){ return '\\alpha = \\dfrac{\\Delta l}{l_0 \\cdot \\Delta T} = \\dfrac{' + ein(A.dl / 1000, 'm') + '}{' + ein(A.l0, 'm') + ' \\cdot ' + kel(A.dT) + '} \\approx ' + tz(r3(A.a)) + ' \\cdot 10^{-6}\\;\\tfrac{1}{\\text{K}}\\text{: ' + A.m + '}'; } },

      /* ----- Kapitel 2: Volumenausdehnung ----- */
      'volumen': { felder: ['v'], muster: 'Δ<i>V</i> = {v} ml',
        neu: function(){
          var o, V0, t1, t2, dT, d;
          do { o = zufall([['Ein Kanister enthält', 'Ethanol', 1.10e-3, '1.10', [5, 10, 20]], ['Eine Flasche enthält', 'Ethanol', 1.10e-3, '1.10', [0.5, 0.75, 1.5]], ['Ein Vorratsgefäss im Labor enthält', 'Quecksilber', 0.18e-3, '0.18', [0.25, 0.6, 1.2]]]);
               V0 = zufall(o[4]); t1 = zufall([5, 10, 15]); t2 = zufall([30, 38, 45]); dT = t2 - t1; d = o[2] * V0 * dT * 1000; }
          while (!verschieden([d, d / 1000, d * t2 / dT, 3 * d]));
          return { v: d, g: o[2], z: o[3], V0: V0, t1: t1, t2: t2, dT: dT,
            text: o[0] + ' \\(' + ein(V0, 'l') + '\\) ' + o[1] + ' (\\(\\gamma = ' + gm(o[3]) + '\\)). Es wird von \\(' + gr(t1) + '\\) auf \\(' + gr(t2) + '\\) erwärmt. Um wie viele Milliliter wächst das Volumen?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, A.v / 1000)) return 'Zehnerpotenzen prüfen: \\(\\gamma\\) einer Flüssigkeit steht in \\(10^{-3}\\;\\tfrac{1}{\\text{K}}\\), und \\(1\\;\\text{l} = 1000\\;\\text{ml}\\).';
          if (nah(e.v, A.v * A.t2 / A.dT)) return 'In die Formel gehört die Temperaturdifferenz \\(\\Delta T\\), nicht die Endtemperatur.';
          if (nah(e.v, 3 * A.v)) return 'Bei Flüssigkeiten steht \\(\\gamma\\) schon in der Tabelle — kein Faktor 3.';
          return '\\(\\Delta V = \\gamma \\cdot V_0 \\cdot \\Delta T\\), Ergebnis in ml.'; },
        fehler: function(A){ return [[{ v: String(A.v / 1000) }, 'Zehnerpotenzen'], [{ v: String(A.v * A.t2 / A.dT) }, 'Temperaturdifferenz'], [{ v: String(3 * A.v) }, 'Faktor 3']]; },
        loesung: function(A){ return '\\Delta V = \\gamma \\cdot V_0 \\cdot \\Delta T = ' + gm(A.z) + ' \\cdot ' + ein(A.V0, 'l') + ' \\cdot ' + kel(A.dT) + ' ' + erg(A.v / 1000, 'l') + ' ' + erg(A.v, 'ml'); } },
      'volumen-fest': { felder: ['v'], muster: 'Δ<i>V</i> = {v} cm³',
        neu: function(){
          var o = zufall([['Ein Stahlwürfel', 0, [125, 216, 343]], ['Ein Messingzylinder', 1, [80, 150, 240]], ['Ein Aluminiumblock', 2, [200, 450, 600]]]);
          var m = WERK[o[1]], V0 = zufall(o[2]), dT = zufall([40, 60, 90, 120]);
          return { v: 3 * m[1] * V0 * dT, a: m[1], z: m[2], V0: V0, dT: dT,
            text: o[0] + ' (' + m[0] + ', \\(\\alpha = ' + al(m[2]) + '\\)) hat bei \\(20\\;^\\circ\\text{C}\\) das Volumen \\(' + cm3(V0) + '\\). Er wird auf \\(' + gr(20 + dT) + '\\) erwärmt. Um wie viel wächst sein Volumen?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, A.v / 3)) return 'Das ist mit \\(\\alpha\\) gerechnet. Für das Volumen gilt \\(\\gamma \\approx 3 \\cdot \\alpha\\).';
          if (nah(e.v, A.v * 2 / 3)) return 'Ein Körper wächst in drei Richtungen, nicht in zwei: \\(\\gamma \\approx 3 \\cdot \\alpha\\).';
          if (nah(e.v, A.v * (20 + A.dT) / A.dT)) return 'In die Formel gehört die Temperaturdifferenz \\(\\Delta T\\), nicht die Endtemperatur.';
          return '\\(\\gamma \\approx 3 \\cdot \\alpha\\), dann \\(\\Delta V = \\gamma \\cdot V_0 \\cdot \\Delta T\\) in cm³.'; },
        fehler: function(A){ return [[{ v: String(A.v / 3) }, 'mit \\(\\alpha\\) gerechnet'], [{ v: String(A.v * 2 / 3) }, 'drei Richtungen'], [{ v: String(A.v * (20 + A.dT) / A.dT) }, 'Temperaturdifferenz']]; },
        loesung: function(A){ return '\\gamma \\approx 3 \\cdot \\alpha = ' + al(tz(r3(3 * A.a * 1e6))) + ',\\quad \\Delta V = \\gamma \\cdot V_0 \\cdot \\Delta T = ' + al(tz(r3(3 * A.a * 1e6))) + ' \\cdot ' + cm3(A.V0) + ' \\cdot ' + kel(A.dT) + ' \\approx ' + cm3(r3(A.v)); } },
      'fuellen': { felder: ['v'], muster: '<i>V</i><sub>0</sub> = {v} l',
        neu: function(){
          var o = zufall([['Ein Fass', [60, 200], 'Es'], ['Ein Tank', [1000, 2500], 'Er'], ['Ein Kanister', [20, 30], 'Er']]);
          var Vm = zufall(o[1]), t1 = zufall([6, 10, 14]), t2 = zufall([36, 42, 48]), dT = t2 - t1, g = 1.10e-3;
          return { v: Vm / (1 + g * dT), Vm: Vm, dT: dT, t1: t1, t2: t2, dV: g * Vm * dT,
            text: o[0] + ' fasst \\(' + ein(Vm, 'l') + '\\). ' + o[2] + ' wird bei \\(' + gr(t1) + '\\) mit Ethanol (\\(\\gamma = ' + gm('1.10') + '\\)) gefüllt; im Sommer kann der Inhalt \\(' + gr(t2) + '\\) warm werden. Wie viel Ethanol darf man höchstens einfüllen? (Das Gefäss gilt als starr.)' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, A.Vm + A.dV)) return 'Dann wäre mehr drin, als hineinpasst. Beim Erwärmen braucht das Ethanol zusätzlichen Platz.';
          if (nah(e.v, A.dV)) return 'Das ist der Platz, der frei bleiben muss. Gefragt ist die Füllmenge.';
          if (nah(e.v, A.Vm)) return 'Randvoll läuft es beim Erwärmen über: Lass Platz für \\(\\Delta V\\).';
          if (nah(e.v, A.Vm / (1 + 3 * 1.10e-3 * A.dT))) return 'Bei Flüssigkeiten steht \\(\\gamma\\) schon in der Tabelle — kein Faktor 3.';
          return 'Erwärmt soll das Ethanol genau das Gefäss füllen: \\(V_0 \\cdot (1 + \\gamma \\cdot \\Delta T) = V_\\text{max}\\).'; },
        fehler: function(A){ return [[{ v: String(A.Vm + A.dV) }, 'mehr drin'], [{ v: String(A.dV) }, 'frei bleiben'], [{ v: String(A.Vm) }, 'Randvoll'], [{ v: String(A.Vm / (1 + 3 * 1.10e-3 * A.dT)) }, 'Faktor 3']]; },
        loesung: function(A){ return 'V_0 = \\dfrac{V_\\text{max}}{1 + \\gamma \\cdot \\Delta T} = \\dfrac{' + ein(A.Vm, 'l') + '}{1 + ' + gm('1.10') + ' \\cdot ' + kel(A.dT) + '} ' + erg(A.v, 'l') + '\\quad\\text{(genähert: } V_\\text{max} - \\gamma \\cdot V_\\text{max} \\cdot \\Delta T \\approx ' + ein(r3(A.Vm - A.dV), 'l') + '\\text{)}'; } },

      /* ----- Kapitel 3: Wasser — Dichte und Meeresspiegel ----- */
      'dichte': { felder: ['r'], muster: '<i>ρ</i> = {r} kg/m³',
        neu: function(){
          var f = zufall([['Ethanol', 789, 1.10e-3, '1.10', [25, 40, 55]], ['Quecksilber', 13550, 0.18e-3, '0.18', [120, 160]]]), dT = zufall(f[4]);
          return { r: f[1] / (1 + f[2] * dT), r0: f[1], g: f[2], z: f[3], dT: dT,
            text: f[0] + ' hat bei \\(20\\;^\\circ\\text{C}\\) die Dichte \\(' + tz(f[1]) + '\\;\\text{kg/m}^3\\) (\\(\\gamma = ' + gm(f[3]) + '\\)). Wie gross ist die Dichte bei \\(' + gr(20 + dT) + '\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.r, A.r)) return null;
          if (nah(e.r, A.r0 * (1 + A.g * A.dT))) return 'Wärmer heisst grösseres Volumen bei gleicher Masse — die Dichte wird kleiner, nicht grösser.';
          if (nah(e.r, A.r0)) return 'Die Masse bleibt, aber das Volumen wächst: Die Dichte ändert sich.';
          return '\\(\\rho = \\dfrac{\\rho_0}{1 + \\gamma \\cdot \\Delta T}\\).'; },
        fehler: function(A){ return [[{ r: String(A.r0 * (1 + A.g * A.dT)) }, 'kleiner, nicht grösser'], [{ r: String(A.r0) }, 'Masse bleibt']]; },
        loesung: function(A){ return '\\rho = \\dfrac{\\rho_0}{1 + \\gamma \\cdot \\Delta T} = \\dfrac{' + tz(A.r0) + '\\;\\text{kg/m}^3}{1 + ' + gm(A.z) + ' \\cdot ' + kel(A.dT) + '} \\approx ' + tz(r3(A.r)) + '\\;\\text{kg/m}^3'; } },
      'meer': { felder: ['h'], muster: 'Δ<i>h</i> = {h} cm',
        neu: function(){
          var h0, dT, D, d;
          do { h0 = zufall([200, 350, 450, 900, 1200]); dT = zufall([0.3, 0.4, 0.7, 1.1, 2.5]); D = zufall([3200, 3800, 4500]); d = GW * h0 * dT * 100; }
          while (!verschieden([d, GW * D * dT * 100, d / 100, d / 1000]));
          return { h: d, h0: h0, dT: dT, D: D,
            text: 'Das Meer ist hier \\(' + ein(D, 'm') + '\\) tief. Die obersten \\(' + ein(h0, 'm') + '\\) erwärmen sich um \\(' + kel(dT) + '\\), das Tiefenwasser bleibt gleich. Um wie viele Zentimeter steigt der Meeresspiegel allein durch die Ausdehnung (\\(\\gamma = ' + gm('0.21') + '\\))?' }; },
        pruefen: function(A, e){
          if (nah(e.h, A.h)) return null;
          if (nah(e.h, GW * A.D * A.dT * 100)) return 'Nur die erwärmte Schicht dehnt sich aus: \\(h_0 = ' + ein(A.h0, 'm') + '\\), nicht die ganze Tiefe.';
          if (nah(e.h, A.h / 100)) return 'Das ist \\(\\Delta h\\) in Meter. Gefragt sind Zentimeter.';
          if (nah(e.h, A.h / 1000)) return 'Zehnerpotenz von \\(\\gamma\\) prüfen: \\(0.21 \\cdot 10^{-3}\\;\\tfrac{1}{\\text{K}}\\).';
          return '\\(\\Delta h = \\gamma \\cdot h_0 \\cdot \\Delta T\\) mit der Dicke \\(h_0\\) der erwärmten Schicht, Ergebnis in cm.'; },
        fehler: function(A){ return [[{ h: String(GW * A.D * A.dT * 100) }, 'erwärmte Schicht'], [{ h: String(A.h / 100) }, 'Zentimeter'], [{ h: String(A.h / 1000) }, 'Zehnerpotenz']]; },
        loesung: function(A){ return '\\Delta h = \\gamma \\cdot h_0 \\cdot \\Delta T = ' + gm('0.21') + ' \\cdot ' + ein(A.h0, 'm') + ' \\cdot ' + kel(A.dT) + ' ' + erg(A.h / 100, 'm') + ' ' + erg(A.h, 'cm'); } },
      'erwaermung': { felder: ['t'], muster: 'Δ<i>T</i> = {t} K',
        neu: function(){
          var h0, dh, t;
          do { h0 = zufall([250, 500, 750, 1500]); dh = zufall([3, 5, 8, 12, 20]); t = dh / 100 / (GW * h0); }
          while (t < 0.1 || t > 3 || !verschieden([t, t * 100, 1 / t]));
          return { t: t, h0: h0, dh: dh,
            text: 'Um wie viel muss sich die oberste Schicht des Meeres (\\(h_0 = ' + ein(h0, 'm') + '\\)) erwärmen, damit der Meeresspiegel allein durch die Ausdehnung um \\(' + ein(dh, 'cm') + '\\) steigt (\\(\\gamma = ' + gm('0.21') + '\\))?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t)) return null;
          if (nah(e.t, A.t * 100)) return '\\(\\Delta h\\) in Meter einsetzen: \\(' + ein(A.dh, 'cm') + ' = ' + ein(A.dh / 100, 'm') + '\\).';
          if (nah(e.t, 1 / A.t)) return 'Umgekehrt: \\(\\Delta T = \\dfrac{\\Delta h}{\\gamma \\cdot h_0}\\).';
          return '\\(\\Delta T = \\dfrac{\\Delta h}{\\gamma \\cdot h_0}\\), \\(\\Delta h\\) in Meter.'; },
        fehler: function(A){ return [[{ t: String(A.t * 100) }, 'in Meter'], [{ t: String(1 / A.t) }, 'Umgekehrt']]; },
        loesung: function(A){ return '\\Delta T = \\dfrac{\\Delta h}{\\gamma \\cdot h_0} = \\dfrac{' + ein(A.dh / 100, 'm') + '}{' + gm('0.21') + ' \\cdot ' + ein(A.h0, 'm') + '} ' + erg(A.t, 'K'); } },

      /* ----- Kapitel 4: allgemeine Gasgleichung ----- */
      'gas-p': { felder: ['p'], muster: '<i>p</i><sub>2</sub> = {p} bar',
        neu: function(){
          var p1, V1, f, t1, t2, T1, T2, p;
          do { p1 = zufall([1.0, 1.2, 1.5, 2.0]); V1 = zufall([1.5, 2.4, 3.0, 4.0]); f = zufall([0.5, 0.75, 0.8, 1.25]); t1 = zufall([10, 15, 25]); t2 = zufall([-20, 45, 70, 110]);
               T1 = t1 + TK; T2 = t2 + TK; p = p1 * T2 / (T1 * f); }
          while (p > 6 || !verschieden([p, p1 * f * T2 / T1, p1 * T1 / (T2 * f)].concat(t2 > 0 ? [p1 * t2 / (t1 * f)] : [])));
          var V2 = +(V1 * f).toPrecision(6);
          return { p: p, p1: p1, V1: V1, V2: V2, t1: t1, t2: t2, T1: T1, T2: T2,
            text: 'In einem Zylinder mit Kolben ist Gas eingeschlossen: \\(p_1 = ' + ein(p1, 'bar') + '\\), \\(V_1 = ' + ein(V1, 'l') + '\\), \\(\\vartheta_1 = ' + gr(t1) + '\\). Der Kolben wird auf \\(V_2 = ' + ein(V2, 'l') + '\\) verschoben, und das Gas hat danach \\(' + gr(t2) + '\\). Wie gross ist der Druck jetzt?' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (A.t2 > 0 && nah(e.p, A.p1 * A.V1 * A.t2 / (A.t1 * A.V2))) return 'Die Temperaturen gehören in Kelvin: \\(T\\;[\\text{K}] = \\vartheta\\;[^\\circ\\text{C}] + 273.15\\).';
          if (nah(e.p, A.p1 * A.V2 * A.T2 / (A.T1 * A.V1))) return 'Die Volumen stehen verkehrt: Kleineres Volumen gibt grösseren Druck.';
          if (nah(e.p, A.p1 * A.V1 * A.T1 / (A.T2 * A.V2))) return 'Die Temperaturen stehen verkehrt: Höhere Temperatur gibt grösseren Druck.';
          return '\\(p_2 = \\dfrac{p_1 \\cdot V_1 \\cdot T_2}{T_1 \\cdot V_2}\\), \\(T\\) in Kelvin.'; },
        fehler: function(A){ var l = [[{ p: String(A.p1 * A.V2 * A.T2 / (A.T1 * A.V1)) }, 'Volumen stehen verkehrt'], [{ p: String(A.p1 * A.V1 * A.T1 / (A.T2 * A.V2)) }, 'Temperaturen stehen verkehrt']];
          if (A.t2 > 0) l.push([{ p: String(A.p1 * A.V1 * A.t2 / (A.t1 * A.V2)) }, 'Kelvin']); return l; },
        loesung: function(A){ return 'p_2 = \\dfrac{p_1 \\cdot V_1 \\cdot T_2}{T_1 \\cdot V_2} = \\dfrac{' + ein(A.p1, 'bar') + ' \\cdot ' + ein(A.V1, 'l') + ' \\cdot ' + kel(+A.T2.toFixed(2)) + '}{' + kel(+A.T1.toFixed(2)) + ' \\cdot ' + ein(A.V2, 'l') + '} ' + erg(A.p, 'bar'); } },
      'gas-v': { felder: ['v'], muster: '<i>V</i><sub>2</sub> = {v} cm³',
        neu: function(){
          var p1 = zufall([2.2, 2.8, 3.5, 4.2]), V1 = zufall([4, 8, 15, 30]), t1 = zufall([6, 9, 12]), t2 = zufall([15, 18, 22]), T1 = t1 + TK, T2 = t2 + TK;
          return { v: p1 * V1 * T2 / T1, p1: p1, V1: V1, t1: t1, t2: t2, T1: T1, T2: T2,
            text: 'Eine Taucherin atmet aus. Eine Luftblase hat in der Tiefe \\(' + cm3(V1) + '\\) bei \\(p_1 = ' + ein(p1, 'bar') + '\\) (absolut) und \\(' + gr(t1) + '\\). Sie steigt auf; an der Oberfläche herrschen \\(' + ein(1, 'bar') + '\\) und \\(' + gr(t2) + '\\). Welches Volumen hat sie dort?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (nah(e.v, A.p1 * A.V1 * A.t2 / A.t1)) return 'Die Temperaturen gehören in Kelvin: \\(T\\;[\\text{K}] = \\vartheta\\;[^\\circ\\text{C}] + 273.15\\).';
          if (nah(e.v, A.V1 * A.T2 / (A.T1 * A.p1))) return 'Der Druck nimmt ab — wird die Blase grösser oder kleiner? Die Drücke stehen verkehrt.';
          return '\\(V_2 = \\dfrac{p_1 \\cdot V_1 \\cdot T_2}{T_1 \\cdot p_2}\\), \\(T\\) in Kelvin.'; },
        fehler: function(A){ return [[{ v: String(A.p1 * A.V1 * A.t2 / A.t1) }, 'Kelvin'], [{ v: String(A.V1 * A.T2 / (A.T1 * A.p1)) }, 'Drücke stehen verkehrt']]; },
        loesung: function(A){ return 'V_2 = \\dfrac{p_1 \\cdot V_1 \\cdot T_2}{T_1 \\cdot p_2} = \\dfrac{' + ein(A.p1, 'bar') + ' \\cdot ' + cm3(A.V1) + ' \\cdot ' + kel(+A.T2.toFixed(2)) + '}{' + kel(+A.T1.toFixed(2)) + ' \\cdot ' + ein(1, 'bar') + '} \\approx ' + cm3(r3(A.v)); } },
      'reifen': { felder: ['p'], muster: '<i>p</i><sub>ü,2</sub> = {p} bar',
        neu: function(){
          var o, pu, t1, t2, T1, T2, p;
          do { o = zufall(['Ein Autoreifen', 'Ein Velopneu', 'Ein Gummiboot']); pu = zufall(o === 'Ein Velopneu' ? [3.0, 4.5] : (o === 'Ein Autoreifen' ? [1.8, 2.4] : [0.25, 0.35])); t1 = zufall([2, 8, 12]); t2 = zufall([30, 38, 46]); T1 = t1 + TK; T2 = t2 + TK; p = (pu + 1) * T2 / T1 - 1; }
          while (!verschieden([p, pu * T2 / T1, (pu + 1) * T2 / T1, (pu + 1) * t2 / t1 - 1]));
          return { p: p, pu: pu, t1: t1, t2: t2, T1: T1, T2: T2,
            text: o + ' zeigt bei \\(' + gr(t1) + '\\) einen Überdruck von \\(' + ein(pu, 'bar') + '\\). In der Sonne wird die Luft darin \\(' + gr(t2) + '\\) warm; das Volumen bleibt fast gleich. Was zeigt das Manometer jetzt? (Luftdruck \\(1.0\\;\\text{bar}\\))' }; },
        pruefen: function(A, e){
          if (nah(e.p, A.p)) return null;
          if (nah(e.p, A.pu * A.T2 / A.T1)) return 'Mit dem Überdruck gerechnet. In die Gasgleichung gehört der absolute Druck: \\(p = p_\\text{ü} + 1.0\\;\\text{bar}\\).';
          if (nah(e.p, (A.pu + 1) * A.T2 / A.T1)) return 'Das ist der absolute Druck. Das Manometer zeigt den Überdruck: \\(1.0\\;\\text{bar}\\) abzählen.';
          if (nah(e.p, (A.pu + 1) * A.t2 / A.t1 - 1)) return 'Die Temperaturen gehören in Kelvin.';
          return 'Absolut rechnen: \\(p_1 = p_\\text{ü,1} + 1.0\\;\\text{bar}\\), \\(p_2 = p_1 \\cdot \\dfrac{T_2}{T_1}\\), dann wieder \\(1.0\\;\\text{bar}\\) abzählen.'; },
        fehler: function(A){ return [[{ p: String(A.pu * A.T2 / A.T1) }, 'Mit dem Überdruck'], [{ p: String((A.pu + 1) * A.T2 / A.T1) }, 'absolute Druck'], [{ p: String((A.pu + 1) * A.t2 / A.t1 - 1) }, 'Kelvin']]; },
        loesung: function(A){ return 'p_2 = \\dfrac{p_1 \\cdot V_1 \\cdot T_2}{T_1 \\cdot V_2} = p_1 \\cdot \\dfrac{T_2}{T_1} = ' + ein(A.pu + 1, 'bar') + ' \\cdot \\dfrac{' + kel(+A.T2.toFixed(2)) + '}{' + kel(+A.T1.toFixed(2)) + '} ' + erg(A.p + 1, 'bar') + ',\\quad p_\\text{ü,2} = p_2 - 1.0\\;\\text{bar} ' + erg(A.p, 'bar'); } },

      /* ----- Kapitel 5: Spezialfälle ----- */
      'isotherm': { felder: ['x'], muster: function(A){ return A.art === 'p' ? '<i>p</i><sub>2</sub> = {x} bar' : '<i>V</i><sub>2</sub> = {x} l'; },
        neu: function(){
          if (Math.random() < 0.5){
            var V1, V2;
            do { V1 = zufall([120, 180, 240, 300]); V2 = zufall([40, 60, 75, 90, 150]); } while (V2 >= V1 * 0.8 || !verschieden([V1 / V2, V2 / V1, V1 / V2 - 1]) || istFest('isotherm', ['p', V1, V2]));
            return { art: 'p', x: V1 / V2, a1: V1, a2: V2, p1: 1.0,
              text: 'Eine Velopumpe ist vorne zugehalten. Sie enthält \\(' + cm3(V1) + '\\) Luft bei \\(1.0\\;\\text{bar}\\). Du drückst den Kolben langsam auf \\(' + cm3(V2) + '\\). Wie gross ist der absolute Druck jetzt?' };
          }
          var p1 = zufall([1.0, 0.95]), V = zufall([1.5, 2.5, 4]), p2 = zufall([0.3, 0.45, 0.6]);
          return { art: 'V', x: p1 * V / p2, a1: p1, a2: p2, V1: V,
            text: 'Ein Ballon mit \\(' + ein(V, 'l') + '\\) Luft (\\(' + ein(p1, 'bar') + '\\)) liegt unter einer Glocke. Die Luft um ihn wird langsam abgepumpt, bis der Druck \\(' + ein(p2, 'bar') + '\\) beträgt; die Temperatur bleibt gleich. Welches Volumen hat er dann (Hülle ohne eigene Spannung)?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'p'){
            if (nah(e.x, A.a2 / A.a1)) return 'Kleineres Volumen, grösserer Druck: \\(p_1 \\cdot V_1 = p_2 \\cdot V_2\\) — umgekehrt proportional.';
            if (nah(e.x, A.x - 1)) return 'Das ist der Überdruck. Gefragt ist der absolute Druck.';
          } else if (nah(e.x, A.V1 * A.a2 / A.a1)) return 'Kleinerer Druck, grösseres Volumen: \\(p_1 \\cdot V_1 = p_2 \\cdot V_2\\) — umgekehrt proportional.';
          return 'Isotherm: \\(p_1 \\cdot V_1 = p_2 \\cdot V_2\\).'; },
        fehler: function(A){ return A.art === 'p' ? [[{ x: String(A.a2 / A.a1) }, 'umgekehrt proportional'], [{ x: String(A.x - 1) }, 'Überdruck']] : [[{ x: String(A.V1 * A.a2 / A.a1) }, 'umgekehrt proportional']]; },
        loesung: function(A){ return A.art === 'p' ? 'p_2 = \\dfrac{p_1 \\cdot V_1}{V_2} = \\dfrac{1.0\\;\\text{bar} \\cdot ' + cm3(A.a1) + '}{' + cm3(A.a2) + '} ' + erg(A.x, 'bar')
                                                 : 'V_2 = \\dfrac{p_1 \\cdot V_1}{p_2} = \\dfrac{' + ein(A.a1, 'bar') + ' \\cdot ' + ein(A.V1, 'l') + '}{' + ein(A.a2, 'bar') + '} ' + erg(A.x, 'l'); } },
      'isobar': { felder: ['v'], muster: '<i>V</i><sub>2</sub> = {v} l',
        neu: function(){
          var V1, t1, t2, T1, T2;
          do { V1 = zufall([1.2, 2.0, 3.5]); t1 = zufall([10, 18, 25]); t2 = zufall([-30, 60, 95, 150]); T1 = t1 + TK; T2 = t2 + TK; }
          while (!verschieden([V1 * T2 / T1, V1 * T1 / T2].concat(t2 > 0 ? [V1 * t2 / t1] : [])));
          return { v: V1 * T2 / T1, V1: V1, t1: t1, t2: t2, T1: T1, T2: T2,
            text: 'In einem Zylinder mit leicht beweglichem Kolben (der Druck bleibt gleich) sind \\(' + ein(V1, 'l') + '\\) Gas bei \\(' + gr(t1) + '\\). Das Gas wird auf \\(' + gr(t2) + '\\) gebracht. Welches Volumen hat es dann?' }; },
        pruefen: function(A, e){
          if (nah(e.v, A.v)) return null;
          if (A.t2 > 0 && nah(e.v, A.V1 * A.t2 / A.t1)) return 'Proportional ist das Volumen zur absoluten Temperatur: \\(T\\) in Kelvin.';
          if (nah(e.v, A.V1 * A.T1 / A.T2)) return 'Umgekehrt: Wärmer heisst grösseres Volumen, \\(\\dfrac{V_1}{T_1} = \\dfrac{V_2}{T_2}\\).';
          return 'Isobar: \\(\\dfrac{V_1}{T_1} = \\dfrac{V_2}{T_2}\\), \\(T\\) in Kelvin.'; },
        fehler: function(A){ var l = [[{ v: String(A.V1 * A.T1 / A.T2) }, 'Umgekehrt']]; if (A.t2 > 0) l.push([{ v: String(A.V1 * A.t2 / A.t1) }, 'Kelvin']); return l; },
        loesung: function(A){ return 'V_2 = V_1 \\cdot \\dfrac{T_2}{T_1} = ' + ein(A.V1, 'l') + ' \\cdot \\dfrac{' + kel(+A.T2.toFixed(2)) + '}{' + kel(+A.T1.toFixed(2)) + '} ' + erg(A.v, 'l'); } },
      'fall': { felder: ['f', 'x'], muster: function(A){ return 'Fall: {f:isotherm|isobar|isochor}; ' + A.gr + ' = {x} ' + A.u; },
        neu: function(){
          var art = zufall(['isochor', 'isobar', 'isotherm']), A;
          if (art === 'isochor'){
            var p1 = zufall([4, 6, 8, 12]), t1 = zufall([5, 12, 18]), t2 = zufall([35, 45, 60]);
            A = { x: p1 * (t2 + TK) / (t1 + TK), c: p1 * t2 / t1, inv: p1 * (t1 + TK) / (t2 + TK), gr: '<i>p</i><sub>2</sub>', u: 'bar', a: p1, t1: t1, t2: t2,
              text: 'Eine Druckluftflasche aus Stahl steht bei \\(' + gr(t1) + '\\) unter \\(' + ein(p1, 'bar') + '\\) (absolut). Sie liegt in der Sonne und wird \\(' + gr(t2) + '\\) warm. Welcher Fall liegt vor, und wie gross ist der Druck dann?' };
          } else if (art === 'isobar'){
            var V1 = zufall([0.8, 1.6, 2.4]), s1 = zufall([15, 22, 28]), s2 = zufall([-25, -10, 2]);
            A = { x: V1 * (s2 + TK) / (s1 + TK), c: s2 > 0 ? V1 * s2 / s1 : null, inv: V1 * (s1 + TK) / (s2 + TK), gr: '<i>V</i><sub>2</sub>', u: 'l', a: V1, t1: s1, t2: s2,
              text: 'Ein Zylinder mit einem Kolben, auf dem ein Gewicht liegt und der leicht gleitet, enthält \\(' + ein(V1, 'l') + '\\) Luft bei \\(' + gr(s1) + '\\). Er kommt ins Freie und kühlt auf \\(' + gr(s2) + '\\) ab. Welcher Fall liegt vor, und welches Volumen hat die Luft dann?' };
          } else {
            var WW = zufall([[30, 20], [30, 15], [30, 12], [20, 10], [20, 8], [50, 25], [50, 20]]), W1 = WW[0], W2 = WW[1];   // p₂ ≤ 2.5 bar: von Hand zu schaffen
            A = { x: W1 / W2, c: null, inv: W2 / W1, gr: '<i>p</i><sub>2</sub>', u: 'bar', a: W1, b: W2,
              text: 'Eine Spritze ist vorne zugehalten und enthält \\(' + ein(W1, 'ml') + '\\) Luft bei \\(1.0\\;\\text{bar}\\). Du drückst den Kolben langsam bei Zimmertemperatur auf \\(' + ein(W2, 'ml') + '\\). Welcher Fall liegt vor, und wie gross ist der absolute Druck dann?' };
          }
          A.f = art; return A; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return e.f === A.f ? null : 'Die Zahl stimmt. Welche Grösse bleibt hier konstant? Das bestimmt den Fall.';
          if (A.c != null && nah(e.x, A.c)) return 'Die Temperaturen gehören in Kelvin.';
          if (nah(e.x, A.inv)) return 'Verhältnis umgekehrt: ' + (A.f === 'isotherm' ? 'kleineres Volumen, grösserer Druck.' : 'wärmer heisst ' + (A.f === 'isobar' ? 'grösseres Volumen.' : 'grösserer Druck.'));
          return A.f === 'isotherm' ? '\\(p_1 \\cdot V_1 = p_2 \\cdot V_2\\).' : (A.f === 'isobar' ? '\\(\\dfrac{V_1}{T_1} = \\dfrac{V_2}{T_2}\\), \\(T\\) in Kelvin.' : '\\(\\dfrac{p_1}{T_1} = \\dfrac{p_2}{T_2}\\), \\(T\\) in Kelvin.'); },
        fehler: function(A){ var b = A.f === 'isochor' ? 'isobar' : 'isochor', l = [[{ f: b, x: String(A.x) }, 'konstant'], [{ f: A.f, x: String(A.inv) }, 'umgekehrt']]; if (A.c != null) l.push([{ f: A.f, x: String(A.c) }, 'Kelvin']); return l; },
        eingabe: function(A){ return { f: A.f, x: String(A.x) }; },
        loesung: function(A){
          if (A.f === 'isotherm') return '\\text{isotherm (langsam, Zimmertemperatur): } p_2 = \\dfrac{p_1 \\cdot V_1}{V_2} = \\dfrac{1.0\\;\\text{bar} \\cdot ' + ein(A.a, 'ml') + '}{' + ein(A.b, 'ml') + '} ' + erg(A.x, 'bar');
          if (A.f === 'isobar') return '\\text{isobar (Gewicht auf dem Kolben): } V_2 = V_1 \\cdot \\dfrac{T_2}{T_1} = ' + ein(A.a, 'l') + ' \\cdot \\dfrac{' + kel(+(A.t2 + TK).toFixed(2)) + '}{' + kel(+(A.t1 + TK).toFixed(2)) + '} ' + erg(A.x, 'l');
          return '\\text{isochor (starre Flasche): } p_2 = p_1 \\cdot \\dfrac{T_2}{T_1} = ' + ein(A.a, 'bar') + ' \\cdot \\dfrac{' + kel(+(A.t2 + TK).toFixed(2)) + '}{' + kel(+(A.t1 + TK).toFixed(2)) + '} ' + erg(A.x, 'bar'); } }
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
