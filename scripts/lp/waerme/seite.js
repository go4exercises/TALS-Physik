<script>
/* Leitprogramm Wärme — laufende Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr, Übungsrahmen,
   Minigrafen) wörtlich aus dem Leitprogramm Hydrostatik, Achsen mit der Höhe ya der x-Achse wie im
   Leitprogramm Energie; neu sind die sieben Simulationen (Wärme zuführen, Kalorimeter, Heizkurve,
   Heizkessel und Boiler, Energiesysteme, Wärmewege im Labor, Durchlässigkeit der Atmosphäre) und die
   Übungstypen für 5.2. Stoffwerte wie Themenseite 5.2 (c_W = 4182 J/(kg·K), c_Eis = 2100 J/(kg·K),
   L_f = 334 kJ/kg, L_v = 2256 kJ/kg). Farben (Farbe = eine Bedeutung): Temperatur eines Körpers
   Bernstein, Wasser Blau, Wärme (übertragen, abgestrahlt, Verlust) Rot, zugeführte Energie und Licht
   Orange, Nutzen (Strom, Nutzwärme) Grün, Körper, Gefässe und Achsen Grau.
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
    var sx = o.sx || 1, sy = o.sy || 1, i, ya = o.ya == null ? 0 : o.ya;   // ya: Höhe der x-Achse (Fenster ohne y = 0, wie Energie)
    for (i = Math.ceil(x0 / sx) * sx; i <= x1 + 1e-9; i += sx) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
    for (i = Math.ceil(y0 / sy) * sy; i <= y1 + 1e-9; i += sy) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    el(g, 'line', { x1: 0, y1: Y(ya), x2: W, y2: Y(ya), 'class': 'achse' });
    el(g, 'line', { x1: X(0), y1: 0, x2: X(0), y2: H, 'class': 'achse' });
    var pf = o.pfeil || 7;
    el(g, 'polygon', { points: W + ',' + Y(ya) + ' ' + (W - pf) + ',' + (Y(ya) - pf / 2) + ' ' + (W - pf) + ',' + (Y(ya) + pf / 2), 'class': 'pfeil' });
    el(g, 'polygon', { points: X(0) + ',0 ' + (X(0) - pf / 2) + ',' + pf + ' ' + (X(0) + pf / 2) + ',' + pf, 'class': 'pfeil' });
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(ya) + 13, 'text-anchor': 'middle', 'class': 'skala' }, minus(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(0) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, minus(t)); });
    var ebene = el(svg, 'g', {});
    var schilder = el(svg, 'g', {});
    stext(schilder, { x: W - 3, y: Y(ya) - pf - 2, 'text-anchor': 'end', 'class': 'achsname' }, o.xname || 'x');
    stext(schilder, { x: X(0) + pf + 2, y: pf + 5, 'text-anchor': 'start', 'class': 'achsname' }, o.yname || 'y');
    /* Belegte Flächen [links, oben, rechts, unten] in px: Achsennamen, Teilung, Punkte und
       schon gesetzte Beschriftungen. etikett() sucht für die Beschriftung eines Punktes eine
       freie Stelle, die weder diese Flächen noch die übergebenen Kurven berührt. */
    var breite = function(s){ return String(s).replace(/_/g, '').length * 6.3; };
    var schutz = [[W - 3 - breite(o.xname || 'x'), Y(ya) - pf - 14, W, Y(ya) - pf + 1],
                  [X(0) + pf, 0, X(0) + pf + 4 + breite(o.yname || 'y'), pf + 8],
                  [0, Y(ya) + 2, W, Y(ya) + 16], [0, 0, X(0) + 2, H]];
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
        var gew = wahl[0];
        for (var i = 0; i < wahl.length; i++){
          var c = wahl[i], tx = px + c[0], ty = py + c[1], l = c[2] === 'end' ? tx - bw : tx;
          if (frei([l, ty - bh + 1, l + bw, ty + 3])){ gew = c; break; }
        }
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


  // Stoffwerte wie Themenseite 5.2: c in J/(kg·K), latente Wärme in J/kg
  var CW = 4182, CEIS = 2100, LF = 334000, LV = 2256000, SIGMA = 5.67e-8;
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



  // Achsenteilung zum grössten Wert: höchstens fünf beschriftete Striche
  function skala(max){
    var st = [0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000], i = 0;
    while (i < st.length - 1 && max / st[i] > 5) i++;
    var s = st[i], oben = Math.ceil(max / s) * s, ym = [];
    for (var v = s; v <= oben + 1e-9; v += s) ym.push(+v.toPrecision(6));
    return { oben: oben, s: s, ym: ym };
  }
  function kj(x){ return sig(x / 1000) + NB + 'kJ'; }
  function grad(x, d){ return fest(x, d == null ? 1 : d) + NB + '°C'; }
  function th_(i){ return v_('ϑ') + (i ? '<sub>' + i + '</sub>' : ''); }
  function q_(i){ return v_('Q') + (i ? '<sub>' + i + '</sub>' : ''); }
  // Thermometer: Röhre von y0 (unten) bis y1 (oben), Füllung nach dem Anteil a (0 bis 1)
  function thermometer(eltern, x, y0, y1, a, text){
    el(eltern, 'rect', { x: x - 4, y: y1, width: 8, height: y0 - y1, rx: 4, 'class': 'thermo' });
    el(eltern, 'circle', { cx: x, cy: y0 + 5, r: 7, 'class': 'thermo-kugel' });
    var h = Math.max(0, Math.min(1, a)) * (y0 - y1 - 4);
    el(eltern, 'rect', { x: x - 2, y: y0 - h, width: 4, height: h + 4, 'class': 'thermo-saeule' });
    if (text) el(eltern, 'text', { x: x, y: y1 - 6, 'text-anchor': 'middle', 'class': 'bt-wert' }, text);
  }
  // Teilchen mit Pfeil: Länge wächst mit der Wurzel der absoluten Temperatur (mittlere Geschwindigkeit)
  var RICHT = [0.4, 2.1, 3.9, 5.3, 1.2, 2.9, 4.6, 0.1, 5.8, 3.3, 1.7, 4.2, 0.8, 2.5, 5.0, 3.6, 1.0, 4.9, 2.2, 5.6];
  function teilchen(eltern, x0, y0, b, h, T, n){
    var sp = 5, zs = Math.ceil(n / sp), L = 8 * Math.sqrt(Math.max(1, T) / 293.15);
    for (var k = 0; k < n; k++){
      var i = k % sp, j = Math.floor(k / sp), cx = x0 + (i + 0.5) * b / sp + (j % 2 ? 4 : -4), cy = y0 + (j + 0.5) * h / zs;
      var w = RICHT[k % RICHT.length];
      el(eltern, 'line', { x1: cx, y1: cy, x2: cx + L * Math.cos(w), y2: cy - L * Math.sin(w), 'class': 'tpfeil' });
      el(eltern, 'circle', { cx: cx, cy: cy, r: 2.6, 'class': 'teilchen' });
    }
  }

  /* ---------- Kapitel 1: Wärme zuführen ----------
     Ein Körper (Wasser, Speiseöl, Aluminium oder Eisen, Masse m) bekommt auf Knopfdruck die
     eingestellte Wärme Q von einer Heizplatte. Die Teilchenpfeile wachsen mit der mittleren
     Geschwindigkeit (∝ √T), im Diagramm wandert der Zustand auf der Geraden ϑ = 20 °C + Q / (m · c).
     Ohne Phasenwechsel: m ≥ 0.2 kg und Q ≤ 50 kJ halten Wasser unter 80 °C und die Metalle weit
     unter dem Schmelzpunkt. Unterschied zur Themenseite (Animation 1, sechs Stoffe als Balken
     nebeneinander): ein Körper, das Teilchenbild und der Weg im ϑ-Q-Diagramm; die Rechnung erst nach
     dem Lauf, damit die Vorhersage zählt. Clipbeispiel: 0.5 kg Wasser und 0.5 kg Öl mit je 20 kJ;
     Startwerte 1.0 kg Wasser, 10 kJ (kein Leistenziel). */
  var STOFF1 = { wasser: { n: 'Wasser', c: 4182, cls: 'wasser', y: 100 }, oel: { n: 'Speiseöl', c: 2000, cls: 'oel', y: 150 },
                 alu: { n: 'Aluminium', c: 896, cls: 'koerper alu', y: 300 }, eisen: { n: 'Eisen', c: 450, cls: 'koerper eisen', y: 600 } };
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,200)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); q = 0; ende = false; zeichnen(); });
    var q = 0, ende = false, lauf = null, laeufe = [], vorher = null, pruefen = function(){};
    function werte(){ var s = STOFF1[B.wert('stoff')], m = B.wert('m'), Q = B.wert('Q') * 1000; return { s: s, stoff: B.wert('stoff'), m: m, Q: Q, c: s.c, dT: Q / (m * s.c) }; }
    function fertig(w){ ende = true; lauf = { stoff: w.stoff, m: w.m, Q: w.Q / 1000, dT: w.dT, c: w.c }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); q = Math.min(w.Q, w.Q * tt / 2.4); zeichnen(); if (q >= w.Q){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Wärme zuführen', function(){ vorher = lauf; ende = false; q = 0; var w = werte(); if (WENIGER || w.Q === 0){ q = w.Q; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Neu', function(){ uhr.stop(); q = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); q = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; vorher = null; B.zuruecksetzen(); },
      // Testhaken: Zustand nach x kJ zugeführter Wärme (Bildfolgen der Clips); ohne Zahl der ganze Lauf
      zeige: function(x){ uhr.stop(); var w = werte(); if (x == null){ q = w.Q; fertig(w); } else { q = Math.min(w.Q, x * 1000); ende = false; } zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), th = 20 + q / (w.m * w.c); B.anzeigen(); leeren(szene); leeren(dia);
      var flues = w.stoff === 'wasser' || w.stoff === 'oel';
      // Körper auf der Heizplatte: Flüssigkeit im Becher oder Metallblock; Grösse wächst mit der Masse
      var hb = 46 + 50 * Math.sqrt(w.m / 2), x0 = 70, b = 120, y1 = 150 - hb;
      if (flues){
        el(szene, 'rect', { x: x0, y: y1, width: b, height: hb, 'class': w.s.cls });
        el(szene, 'path', { d: 'M' + (x0 - 2) + ' ' + (y1 - 14) + ' L' + (x0 - 2) + ' 151 L' + (x0 + b + 2) + ' 151 L' + (x0 + b + 2) + ' ' + (y1 - 14), 'class': 'gefaess' });
      } else el(szene, 'rect', { x: x0, y: y1, width: b, height: hb, rx: 3, 'class': w.s.cls });
      teilchen(szene, x0 + 6, y1 + 4, b - 12, hb - 8, th + 273.15, 15);
      var an = uhr.laeuft() || (q > 0 && !ende && q < w.Q);
      el(szene, 'rect', { x: 56, y: 152, width: 148, height: 9, rx: 2, 'class': 'platte' + (q > 0 ? ' an' : '') });
      el(szene, 'text', { x: 130, y: 174, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Heizplatte');
      if (q > 0){
        for (var k = 0; k < 3; k++) pfeil(szene, 95 + 35 * k, 151, 95 + 35 * k, 132, 'pf-q', 6);
        el(szene, 'text', { x: 212, y: 166, 'class': 'pf-text pf-q' }, (an ? 'Q fliesst: ' : 'Q = ') + sig(q / 1000) + NB + 'kJ');
      }
      el(szene, 'text', { x: x0, y: 14, 'class': 'bt-meldung' }, w.s.n + ', ' + zahl(w.m) + NB + 'kg; ' + 'c = ' + w.c + NB + 'J/(kg·K)');
      // Thermometer mit derselben Skala wie das Diagramm
      var ymax = Math.max(w.s.y, vorher ? STOFF1[vorher.stoff].y : 0);
      thermometer(szene, 246, 140, 40, th / ymax, grad(th));
      // Diagramm: Temperatur über der zugeführten Wärme, nur der gefahrene Weg
      var sk = skala(ymax);
      K = Achsen(dia, { w: 300, h: 118, x0: -4, x1: 54, y0: -0.08 * sk.oben, y1: sk.oben * 1.1, sx: 5, sy: sk.s / 2, xm: [10, 20, 30, 40, 50], ym: sk.ym, xname: 'Q [kJ]', yname: 'ϑ [°C]' });
      if (vorher && !uhr.laeuft()){ var v0 = vorher; K.kurve(function(x){ return 20 + x * 1000 / (v0.m * v0.c); }, 'vorher', 0, v0.Q); }
      if (q > 0) K.kurve(function(x){ return 20 + x * 1000 / (w.m * w.c); }, 't-kurve', 0, q / 1000);
      K.punkt(q / 1000, th, 'p-t');
      if (q > 0 && !uhr.laeuft()) K.etikett(q / 1000, th, '(' + sig(q / 1000) + NB + 'kJ; ' + grad(th) + ')', 'p-t',
                                           { kurven: [[function(x){ return 20 + x * 1000 / (w.m * w.c); }, 0, q / 1000]] });
      var z;
      if (ende && lauf){
        z = '<span>' + v_('Q') + ' = ' + v_('m') + ' · ' + v_('c') + ' · Δ' + v_('T') + ' → Δ' + v_('T') + ' = ' + v_('Q') + ' / (' + v_('m') + ' · ' + v_('c') + ') = ' + zahl(w.Q) + NB + 'J / (' + zahl(w.m) + NB + 'kg · ' + w.c + NB + 'J/(kg·K)) ' + ist(w.dT, fest(w.dT, 1)) + fest(w.dT, 1) + NB + 'K</span>';
        z += '<span>' + th_() + ' = 20' + NB + '°C + ' + fest(w.dT, 1) + NB + 'K ' + ist(20 + w.dT, grad(20 + w.dT)) + grad(20 + w.dT) + '</span>';
      } else z = '<span>' + v_('Q') + ' = ' + v_('m') + ' · ' + v_('c') + ' · Δ' + v_('T') + ' — Start bei 20' + NB + '°C. Die Rechnung steht hier nach dem Zuführen.</span>';
      z += '<span class="sim-notiz">Die Pfeile an den Teilchen zeigen ihre mittlere Geschwindigkeit. Ohne Phasenwechsel gerechnet.' + (vorher ? ' Grau gestrichelt: der vorige Lauf.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, stoff, m, Q){ return s.lauf && s.lauf.stoff === stoff && gl(s.lauf.m, m) && gl(s.lauf.Q, Q); }
    function war(s, stoff, m, Q){ return s.laeufe.some(function(l){ return l.stoff === stoff && gl(l.m, m) && gl(l.Q, Q); }); }
    pruefen = Leiste(fig, [
      { text: 'Führe einem Körper so viel Wärme zu, dass er um mindestens \\(50\\;\\text{K}\\) wärmer wird. Vergleiche die Pfeile an den Teilchen vorher und nachher: Was misst die Temperatur, was ist die Wärme? Notiere, dann vergleiche.', ok: function(s){ return s.lauf && s.lauf.dT >= 50; },
        vergleich: 'Die Teilchen bewegen sich nachher im Mittel schneller. Die Temperatur misst diese mittlere Bewegung der Teilchen — ein Zustand. Die Wärme \\(Q\\) ist die Energie, die von der Platte in den Körper übertragen wurde — ein Vorgang.' },
      { text: '\\(0.80\\;\\text{kg}\\) Wasser bekommen \\(25\\;\\text{kJ}\\). Um wie viel Kelvin steigt die Temperatur? Rechne zuerst, dann stelle ein und führe die Wärme zu.', ok: function(s){ return hat(s, 'wasser', 0.8, 25); },
        vergleich: '\\(\\Delta T = \\dfrac{Q}{m \\cdot c} = \\dfrac{25\\,000\\;\\text{J}}{0.80\\;\\text{kg} \\cdot 4182\\;\\text{J/(kg·K)}} \\approx 7.47\\;\\text{K}\\), von \\(20\\;^\\circ\\text{C}\\) auf rund \\(27.5\\;^\\circ\\text{C}\\).' },
      { text: 'Gib \\(0.40\\;\\text{kg}\\) Wasser und \\(1.60\\;\\text{kg}\\) Wasser je \\(30\\;\\text{kJ}\\). Welche Portion wird wärmer, welche hat mehr Wärme bekommen? Begründe.', ok: function(s){ return war(s, 'wasser', 0.4, 30) && war(s, 'wasser', 1.6, 30); },
        vergleich: 'Beide haben dieselbe Wärme bekommen, \\(30\\;\\text{kJ}\\). Die kleine Portion wird viermal so stark wärmer (\\(17.9\\;\\text{K}\\) gegen \\(4.5\\;\\text{K}\\)): Dieselbe Energie verteilt sich auf viermal weniger Teilchen. Gleiche Wärme heisst also nicht gleiche Temperatur.' },
      { text: 'Gib \\(1.00\\;\\text{kg}\\) Wasser und \\(1.00\\;\\text{kg}\\) Aluminium je \\(40\\;\\text{kJ}\\). Wievielmal so stark erwärmt sich das Aluminium? Begründe mit \\(c\\).', ok: function(s){ return war(s, 'wasser', 1, 40) && war(s, 'alu', 1, 40); },
        vergleich: 'Wasser: \\(9.6\\;\\text{K}\\), Aluminium: \\(44.6\\;\\text{K}\\) — rund \\(4.7\\)-mal so viel. Aluminium braucht je Kilogramm und Kelvin nur \\(896\\;\\text{J}\\), Wasser \\(4182\\;\\text{J}\\): \\(\\dfrac{4182}{896} \\approx 4.7\\).' },
      { text: '\\(0.80\\;\\text{kg}\\) Eisen sollen von \\(20\\;^\\circ\\text{C}\\) auf mindestens \\(100\\;^\\circ\\text{C}\\) kommen. Welche Wärme braucht es (auf \\(0.5\\;\\text{kJ}\\) genau, so wenig wie möglich)? Rechne, stelle ein und prüfe.', ok: function(s){ return hat(s, 'eisen', 0.8, 29); },
        vergleich: '\\(Q = m \\cdot c \\cdot \\Delta T = 0.80\\;\\text{kg} \\cdot 450\\;\\text{J/(kg·K)} \\cdot 80\\;\\text{K} = 28\\,800\\;\\text{J}\\). Auf dem Regler reichen \\(29.0\\;\\text{kJ}\\) (\\(100.6\\;^\\circ\\text{C}\\)); mit \\(28.5\\;\\text{kJ}\\) bleibt es bei \\(99.2\\;^\\circ\\text{C}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Wärmebilanz im Kalorimeter ----------
     Ein heisser Körper (Aluminium, Eisen oder heisses Wasser) kommt auf Knopfdruck in kaltes Wasser
     von 20 °C (Gefäss und Umgebung ohne Wärmeaufnahme). Beide Temperaturen nähern sich ϑ_m mit
     derselben Zeitkonstante (10 s, Modell), darum gibt der Körper in jedem Augenblick genau so viel ab,
     wie das Wasser aufnimmt: Die roten Balken Q_ab und Q_auf wachsen gleich. Unterschied zur
     Themenseite (Animation 2, zwei Wasserportionen sofort gemischt): verschiedene Stoffe, der
     Temperaturverlauf beider Körper bis zum Gleichgewicht und die Bilanz als Balken; ϑ_m steht erst
     nach dem Lauf da. Clipbeispiel: 0.25 kg Aluminium von 200 °C in 0.80 kg Wasser von 15 °C (ausserhalb
     des Wasser-Starts 20 °C); Startwerte Aluminium 0.30 kg, 150 °C, Wasser 0.40 kg (kein Leistenziel). */
  var STOFF2 = { alu: { n: 'Aluminium', c: 896, cls: 'koerper alu' }, eisen: { n: 'Eisen', c: 450, cls: 'koerper eisen' }, wasser: { n: 'heisses Wasser', c: 4182, cls: 'wasser' } };
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,184)' }), K = null;
    var tk = fig.querySelector('input[data-p="tk"]');
    var B = Bedienung(fig, function(){ grenzen(); uhr.stop(); t = 0; ende = false; zeichnen(); });
    var t = 0, ende = false, lauf = null, laeufe = [], vorher = null, pruefen = function(){};
    var TAU = 10, TEND = 60, TW = 20;
    // Heisses Wasser höchstens 95 °C: der Regler bekommt dann ein anderes Ende (HOWTO §16)
    function grenzen(){ var mx = B.wert('k') === 'wasser' ? 95 : 300; if (+tk.max !== mx){ tk.max = mx; if (+tk.value > mx) tk.value = mx; } }
    // Würde das Wasser über 100 °C kommen, siedet es: Das Modell (ohne Phasenwechsel) gilt dann nicht (HOWTO §15)
    function siedet(w){ return w.tm >= 100; }
    function werte(){
      var s = STOFF2[B.wert('k')], mk = B.wert('mk'), tk0 = B.wert('tk'), mw = B.wert('mw');
      var CK = mk * s.c, CWm = mw * CW, tm = (CK * tk0 + CWm * TW) / (CK + CWm);
      return { s: s, k: B.wert('k'), mk: mk, tk: tk0, mw: mw, CK: CK, CWm: CWm, tm: tm, Q: CK * (tk0 - tm) };
    }
    function bei(w, tt){ var e = tt >= TEND ? 0 : Math.exp(-tt / TAU); return { k: w.tm + (w.tk - w.tm) * e, w: w.tm - (w.tm - TW) * e, Q: w.Q * (1 - e) }; }
    function fertig(w){ ende = true; lauf = { k: w.k, mk: w.mk, tk: w.tk, mw: w.mw, tm: w.tm, Q: w.Q }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); t = Math.min(TEND, tt * 12); zeichnen(); if (t >= TEND){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Eintauchen', function(){ if (siedet(werte())){ zeichnen(); return; } vorher = lauf; ende = false; t = 0; if (WENIGER){ t = TEND; fertig(werte()); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Herausnehmen', function(){ uhr.stop(); t = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; ende = false; if (o.k) B.setze({ k: o.k }); grenzen(); B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; vorher = null; B.zuruecksetzen(); },
      // Testhaken: Zustand nach x Sekunden (Modellzeit); ohne Zahl der ganze Lauf
      zeige: function(x){ uhr.stop(); var w = werte(); if (siedet(w)) return; if (x == null || x >= TEND){ t = TEND; fertig(w); } else { t = x; ende = false; } zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), z = bei(w, t), drin = t > 0; B.anzeigen(); leeren(szene); leeren(dia);
      // Gefäss mit kaltem Wasser, der Körper hängt darüber oder liegt darin
      el(szene, 'rect', { x: 30, y: 70, width: 150, height: 86, 'class': 'wasser' });
      el(szene, 'path', { d: 'M28 50 L28 158 L182 158 L182 50', 'class': 'gefaess' });
      el(szene, 'line', { x1: 28, y1: 70, x2: 182, y2: 70, 'class': 'wasserlinie' });
      var kb = 26 + 30 * Math.sqrt(w.mk), ky = drin ? 150 - kb : 8;
      if (w.k === 'wasser'){
        // heisses Wasser: ein Becherinhalt, der ins Gefäss gegossen wird (im Gefäss als warme Schicht gezeichnet)
        if (!drin){ el(szene, 'rect', { x: 86, y: 14, width: 40, height: kb * 0.8, 'class': 'wasser heiss' }); el(szene, 'path', { d: 'M84 8 L84 ' + (16 + kb * 0.8) + ' L128 ' + (16 + kb * 0.8) + ' L128 8', 'class': 'gefaess' }); }
        else el(szene, 'rect', { x: 30, y: 70, width: 150, height: 86, 'class': 'wasser heiss', opacity: Math.max(0, Math.exp(-t / TAU)).toFixed(2) });
      } else {
        el(szene, 'line', { x1: 105, y1: 0, x2: 105, y2: ky, 'class': 'faden' });
        el(szene, 'rect', { x: 105 - kb / 2, y: ky, width: kb, height: kb, rx: 2, 'class': w.s.cls });
      }
      el(szene, 'text', { x: 40, y: 86, 'class': 'bt-wert w-text' }, 'Wasser ' + grad(z.w));
      el(szene, 'text', { x: w.k === 'wasser' ? 132 : 105 + kb / 2 + 4, y: drin ? (w.k === 'wasser' ? 104 : ky + 12) : 26, 'class': 'bt-wert t-text', 'text-anchor': 'start' }, (w.k === 'wasser' ? 'heiss ' : '') + grad(drin ? z.k : w.tk));
      // Bilanz: Q_ab (Körper gibt ab) und Q_auf (Wasser nimmt auf), gleich lang
      var bx = 214, by = 150, bh = 108, f = drin ? z.Q / Math.max(w.Q, 1) : 0;
      el(szene, 'line', { x1: bx - 6, y1: by, x2: bx + 82, y2: by, 'class': 'achse' });
      [[bx, 'ab', 'Körper gibt ab'], [bx + 46, 'auf', 'Wasser nimmt auf']].forEach(function(r){
        el(szene, 'rect', { x: r[0], y: by - bh * f, width: 30, height: bh * f, 'class': 'bal-q' });
        stext(szene, { x: r[0] + 15, y: by + 12, 'text-anchor': 'middle', 'class': 'pf-text pf-q' }, 'Q_' + r[1]);
      });
      if (drin) el(szene, 'text', { x: bx + 38, y: by - bh * f - 6, 'text-anchor': 'middle', 'class': 'bt-wert' }, 'je ' + kj(z.Q));
      // Diagramm: beide Temperaturen über der Zeit
      var top = Math.max(w.tk, vorher ? vorher.tk : 0), sk = skala(top);
      K = Achsen(dia, { w: 300, h: 128, x0: -8, x1: 78, y0: -0.08 * sk.oben, y1: sk.oben * 1.1, sx: 5, sy: sk.s / 2, xm: [10, 20, 30, 40, 50, 60], ym: sk.ym, xname: 't [s]', yname: 'ϑ [°C]' });
      if (vorher && !uhr.laeuft()) K.kurve(function(){ return vorher.tm; }, 'vorher', 0, 60);
      if (drin){
        K.kurve(function(x){ return bei(w, x).k; }, 't-kurve', 0, t);
        K.kurve(function(x){ return bei(w, x).w; }, 'w-kurve', 0, t);
      }
      if (ende){ K.kurve(function(){ return w.tm; }, 'gleich', 0, 60); K.etikett(60, w.tm, 'Mischtemperatur ≈ ' + grad(w.tm), 'p-t', { wahl: [[-4, -8, 'end'], [-4, 16, 'end']] }); }
      stext(K.ebene, { x: 296, y: 12, 'text-anchor': 'end', 'class': 'legende l-t' }, 'Körper');
      stext(K.ebene, { x: 296, y: 25, 'text-anchor': 'end', 'class': 'legende l-w' }, 'Wasser');
      var s = '';
      if (ende && lauf){
        var dk = w.tk - w.tm, dw = w.tm - TW;
        s = '<span>' + q_('ab') + ' = ' + q_('auf') + ': ' + zahl(w.mk) + NB + 'kg · ' + w.s.c + NB + 'J/(kg·K) · (' + zahl(w.tk) + NB + '°C − ' + th_('m') + ') = ' + zahl(w.mw) + NB + 'kg · 4182' + NB + 'J/(kg·K) · (' + th_('m') + ' − 20' + NB + '°C) → ' + th_('m') + ' ' + ist(w.tm, grad(w.tm)) + grad(w.tm) + '</span>';
        s += '<span>' + q_('ab') + ' = ' + v_('m') + '<sub>K</sub> · ' + v_('c') + '<sub>K</sub> · (' + th_('K') + ' − ' + th_('m') + ') = ' + zahl(w.mk) + NB + 'kg · ' + w.s.c + NB + 'J/(kg·K) · ' + fest(dk, 1) + NB + 'K ≈ ' + kj(w.mk * w.s.c * dk) + '</span>';
        s += '<span>' + q_('auf') + ' = ' + v_('m') + '<sub>W</sub> · ' + v_('c') + '<sub>W</sub> · (' + th_('m') + ' − ' + th_('W') + ') = ' + zahl(w.mw) + NB + 'kg · 4182' + NB + 'J/(kg·K) · ' + fest(dw, 1) + NB + 'K ≈ ' + kj(w.mw * CW * dw) + '</span>';
      } else if (siedet(w)) s = '<span class="warnzeile">Das Wasser würde sieden (Mischtemperatur über 100' + NB + '°C): Das Modell ohne Phasenwechsel gilt hier nicht. Wähle mehr Wasser, einen kleineren oder kühleren Körper.</span>';
      else s = '<span>' + q_('ab') + ' = ' + q_('auf') + ' — die Endtemperatur steht hier nach dem Eintauchen.</span>';
      s += '<span class="sim-notiz">Wasser im Gefäss: Start bei 20' + NB + '°C. Gefäss und Umgebung nehmen im Modell nichts auf; ein Körper über 100' + NB + '°C bringt das Wasser an der Berührfläche kurz zum Sieden, das rechnet das Modell nicht mit; die Zeitachse ist ein Modell.' + (vorher ? ' Grau gestrichelt: Endtemperatur des vorigen Laufs.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    function hat(s, k, mk, tk0, mw){ var l = s.lauf; return l && l.k === k && gl(l.mk, mk) && (tk0 == null || gl(l.tk, tk0)) && gl(l.mw, mw); }
    pruefen = Leiste(fig, [
      { text: 'Lass einen Körper eintauchen und vergleiche am Ende die beiden roten Balken. Warum sind sie gleich lang? Notiere, dann vergleiche.', ok: function(s){ return !!s.lauf; },
        vergleich: 'Gefäss und Umgebung nehmen nichts auf: Die Energie, die der Körper abgibt, nimmt das Wasser auf — \\(Q_\\text{ab} = Q_\\text{auf}\\). Das ist die Wärmebilanz. Der Austausch hört auf, wenn beide dieselbe Temperatur haben: thermisches Gleichgewicht.' },
      { text: 'Tauche \\(0.50\\;\\text{kg}\\) Eisen von \\(200\\;^\\circ\\text{C}\\) in \\(0.50\\;\\text{kg}\\) Wasser. Notiere die Endtemperatur. Warum liegt sie so nahe bei \\(20\\;^\\circ\\text{C}\\)?', ok: function(s){ return hat(s, 'eisen', 0.5, 200, 0.5); },
        vergleich: 'Rund \\(37.5\\;^\\circ\\text{C}\\). Bei gleicher Masse zählt \\(c\\): Wasser nimmt je Kilogramm und Kelvin \\(4182\\;\\text{J}\\) auf, Eisen gibt je Kilogramm und Kelvin nur \\(450\\;\\text{J}\\) ab. Das Eisen muss darum viel weiter abkühlen, als das Wasser wärmer wird.' },
      { text: 'Heisses Wasser von \\(80\\;^\\circ\\text{C}\\) soll \\(0.60\\;\\text{kg}\\) Wasser von \\(20\\;^\\circ\\text{C}\\) auf \\(40\\;^\\circ\\text{C}\\) bringen. Welche Masse brauchst du? Rechne mit \\(Q_\\text{ab} = Q_\\text{auf}\\), dann stelle ein und prüfe.', ok: function(s){ return hat(s, 'wasser', 0.3, 80, 0.6); },
        vergleich: '\\(m_1 \\cdot c \\cdot (80\\;^\\circ\\text{C} - 40\\;^\\circ\\text{C}) = 0.60\\;\\text{kg} \\cdot c \\cdot (40\\;^\\circ\\text{C} - 20\\;^\\circ\\text{C})\\); \\(c\\) kürzt sich: \\(m_1 = 0.60\\;\\text{kg} \\cdot \\dfrac{20\\;\\text{K}}{40\\;\\text{K}} = 0.30\\;\\text{kg}\\).' },
      { text: '\\(0.40\\;\\text{kg}\\) Aluminium sollen \\(0.60\\;\\text{kg}\\) Wasser genau auf \\(30\\;^\\circ\\text{C}\\) bringen. Welche Starttemperatur braucht das Aluminium? Rechne, stelle ein, prüfe.', ok: function(s){ return hat(s, 'alu', 0.4, null, 0.6) && Math.abs(s.lauf.tm - 30) <= 0.1; },
        vergleich: '\\(0.40\\;\\text{kg} \\cdot 896\\;\\text{J/(kg·K)} \\cdot (\\vartheta_K - 30\\;^\\circ\\text{C}) = 0.60\\;\\text{kg} \\cdot 4182\\;\\text{J/(kg·K)} \\cdot 10\\;\\text{K} = 25\\,092\\;\\text{J}\\), also \\(\\vartheta_K - 30\\;^\\circ\\text{C} \\approx 70.0\\;\\text{K}\\) und \\(\\vartheta_K \\approx 100\\;^\\circ\\text{C}\\).' },
      { text: 'Gleiche Masse, gleiche Starttemperatur: Tauche erst Aluminium, dann Eisen ein (je \\(0.40\\;\\text{kg}\\) von \\(150\\;^\\circ\\text{C}\\) in \\(0.40\\;\\text{kg}\\) Wasser). Welches wärmt das Wasser mehr? Begründe.', ok: function(s){ var a = false, e = false; s.laeufe.forEach(function(l){ if (gl(l.mk, 0.4) && gl(l.tk, 150) && gl(l.mw, 0.4)){ if (l.k === 'alu') a = true; if (l.k === 'eisen') e = true; } }); return a && e; },
        vergleich: 'Aluminium: rund \\(42.9\\;^\\circ\\text{C}\\), Eisen: rund \\(32.6\\;^\\circ\\text{C}\\). Aluminium gibt je Kilogramm und Kelvin Abkühlung doppelt so viel Wärme ab (\\(896\\) gegen \\(450\\;\\text{J/(kg·K)}\\)) — bei gleicher Masse und Temperatur trägt es mehr Energie ins Wasser.' }
    ], sim);
    grenzen(); zeichnen();
  })();

  /* ---------- Kapitel 3: Die Heizkurve auf der Herdplatte ----------
     Eis (Masse m, Starttemperatur ϑ_0) liegt in einem Topf auf einer Platte, die gleichmässig die
     Leistung P an den Inhalt abgibt. Auf Knopfdruck läuft die Heizkurve ϑ(t) im Zeitraffer bis alles
     verdampft ist: Eis erwärmen (c_Eis = 2100 J/(kg·K)), Schmelzen (L_f = 334 kJ/kg), Wasser erwärmen
     (4182 J/(kg·K)), Sieden (L_v = 2256 kJ/kg), Werte wie Themenseite 5.2. Unterschied zur Themenseite
     (Animation 3: feste 0.1 kg, Regler für die zugeführte Wärme): Zeitachse mit Leistung und Masse, so
     dass die Länge der Plateaus (t = m · L / P) sichtbar wird. Clipbeispiel: 0.5 kg Schnee von −10 °C
     mit 1.2 kW bis 80 °C (nicht einstellbar, endet vor dem Sieden); Startwerte 0.60 kg, 800 W,
     −10 °C (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,176)' }), K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); tz = 0; ende = false; zeichnen(); });
    var tz = 0, ende = false, lauf = null, laeufe = [], vorher = null, pruefen = function(){};
    function werte(){
      var m = B.wert('m'), P = B.wert('P'), t0 = B.wert('t0');
      var Q = [m * CEIS * (0 - t0), m * LF, m * CW * 100, m * LV], t = Q.map(function(q){ return q / P; });
      var T = t[0] + t[1] + t[2] + t[3];
      return { m: m, P: P, t0: t0, Q: Q, t: t, T: T };
    }
    // Temperatur, Abschnitt und Anteile nach der Zeit s (in s)
    function bei(w, s){
      var a = [0, w.t[0], w.t[0] + w.t[1], w.t[0] + w.t[1] + w.t[2], w.T];
      if (s <= a[1]) return { th: w.t0 + (s * w.P) / (w.m * CEIS), ab: 0, eis: 1, dampf: 0 };
      if (s <= a[2]) return { th: 0, ab: 1, eis: 1 - (s - a[1]) / w.t[1], dampf: 0 };
      if (s <= a[3]) return { th: (s - a[2]) * w.P / (w.m * CW), ab: 2, eis: 0, dampf: 0 };
      return { th: 100, ab: 3, eis: 0, dampf: Math.min(1, (s - a[3]) / w.t[3]) };
    }
    function kurve(w){ return function(x){ return bei(w, x * 60).th; }; }
    function fertig(w){ ende = true; lauf = { m: w.m, P: w.P, t0: w.t0, tS: w.t[1], tV: w.t[3], T: w.T }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); tz = Math.min(w.T, w.T * tt / 8); zeichnen(); if (tz >= w.T){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Heizen', function(){ vorher = lauf; ende = false; tz = 0; if (WENIGER){ var w = werte(); tz = w.T; fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Neues Eis', function(){ uhr.stop(); tz = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); tz = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; vorher = null; B.zuruecksetzen(); },
      // Testhaken: Zustand nach x Minuten; ohne Zahl der ganze Lauf
      zeige: function(x){ uhr.stop(); var w = werte(); if (x == null || x * 60 >= w.T){ tz = w.T; fertig(w); } else { tz = x * 60; ende = false; } zeichnen(); }
    };
    fig.__sim = sim;
    var NAME = ['Eis wird wärmer', 'Eis schmilzt', 'Wasser wird wärmer', 'Wasser siedet'];
    function zeichnen(){
      var w = werte(), z = bei(w, tz), heizt = tz > 0 && !(ende && tz >= w.T); B.anzeigen(); leeren(szene); leeren(dia);
      // Topf auf der Platte: Eiswürfel, Schmelzwasser, Dampf
      var x0 = 60, x1 = 180, yb = 140, hMax = 30 + 52 * Math.sqrt(w.m);
      var fl = (1 - z.eis) * (1 - z.dampf), hW = hMax * 0.75 * fl;
      if (hW > 0.5) el(szene, 'rect', { x: x0, y: yb - hW, width: x1 - x0, height: hW, 'class': 'wasser' });
      var n = Math.round(9 * z.eis * Math.min(1, w.m / 0.6 + 0.4));
      for (var k = 0; k < n; k++){ var r = Math.floor(k / 3), c = k % 3; el(szene, 'rect', { x: x0 + 14 + c * 34 + (r % 2) * 8, y: yb - 26 - r * 24 - (hW > 20 ? hW - 20 : 0) * 0.3, width: 22, height: 20, rx: 3, 'class': 'eis' }); }
      if (z.ab === 3 && heizt) for (var d = 0; d < 4; d++) el(szene, 'path', { d: 'M' + (x0 + 22 + d * 26) + ' ' + (yb - hW - 8) + ' q -6 -10 0 -20 q 6 -10 0 -20', 'class': 'dampf' });
      el(szene, 'path', { d: 'M' + (x0 - 3) + ' 40 L' + (x0 - 3) + ' ' + (yb + 2) + ' L' + (x1 + 3) + ' ' + (yb + 2) + ' L' + (x1 + 3) + ' 40', 'class': 'gefaess' });
      el(szene, 'rect', { x: 46, y: 144, width: 148, height: 9, rx: 2, 'class': 'platte' + (heizt ? ' an' : '') });
      el(szene, 'text', { x: 120, y: 166, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Platte: ' + zahl(w.P) + NB + 'W an den Inhalt');
      if (tz > 0) el(szene, 'text', { x: 4, y: 14, 'class': 'bt-meldung' }, (ende ? 'Alles verdampft' : NAME[z.ab]) + ' — nach ' + fest(tz / 60, 1) + NB + 'min');
      else el(szene, 'text', { x: 4, y: 14, 'class': 'bt-meldung' }, zahl(w.m) + NB + 'kg Eis von ' + grad(w.t0, 0));
      thermometer(szene, 236, 128, 36, (z.th + 30) / 140, grad(z.th));
      // Diagramm ϑ(t) in Minuten, x-Achse am unteren Rand (Fenster ab −35 °C)
      var top = Math.max(w.T, vorher ? vorher.T : 0) / 60, sk = skala(top);
      K = Achsen(dia, { w: 300, h: 140, x0: -0.1 * sk.oben, x1: sk.oben * 1.08, y0: -36, y1: 116, sx: sk.s / 2, sy: 10, xm: sk.ym, ym: [-20, 0, 20, 40, 60, 80, 100], xname: 't [min]', yname: 'ϑ [°C]', ya: -36 });
      if (vorher && !uhr.laeuft()){ var v0 = { m: vorher.m, P: vorher.P, t0: vorher.t0 }; v0 = werteVon(v0); K.kurve(kurve(v0), 'vorher', 0, v0.T / 60); }
      if (tz > 0) K.kurve(kurve(w), 't-kurve', 0, tz / 60);
      K.punkt(tz / 60, z.th, 'p-t');
      if (ende){
        var a1 = w.t[0] / 60, a2 = (w.t[0] + w.t[1]) / 60, a3 = (w.t[0] + w.t[1] + w.t[2]) / 60;
        K.text(Math.max((a1 + a2) / 2, 0.08 * sk.oben), -17, 'schmilzt', 'bt-klein');
        K.text((a3 + w.T / 60) / 2, 88, 'siedet', 'bt-klein');
      }
      var s;
      if (ende && lauf){
        var L = [['Eis erwärmen', v_('m') + ' · ' + v_('c') + '<sub>Eis</sub> · Δ' + v_('T'), zahl(w.m) + NB + 'kg · 2100' + NB + 'J/(kg·K) · ' + zahl(-w.t0) + NB + 'K'],
                 ['Schmelzen', v_('m') + ' · ' + v_('L') + '<sub>f</sub>', zahl(w.m) + NB + 'kg · 334' + NB + 'kJ/kg'],
                 ['Wasser erwärmen', v_('m') + ' · ' + v_('c') + '<sub>W</sub> · Δ' + v_('T'), zahl(w.m) + NB + 'kg · 4182' + NB + 'J/(kg·K) · 100' + NB + 'K'],
                 ['Sieden', v_('m') + ' · ' + v_('L') + '<sub>v</sub>', zahl(w.m) + NB + 'kg · 2256' + NB + 'kJ/kg']];
        s = '';
        L.forEach(function(r, i){ if (w.Q[i] > 0) s += '<span>' + r[0] + ': ' + v_('Q') + ' = ' + r[1] + ' = ' + r[2] + ' ' + ist(w.Q[i] / 1000, sig(w.Q[i] / 1000)) + kj(w.Q[i]) + '; ' + v_('t') + ' = ' + v_('Q') + ' / ' + v_('P') + ' ≈ ' + fest(w.t[i] / 60, 1) + NB + 'min</span>'; });
      } else s = '<span>Vier Abschnitte: erwärmen, schmelzen, erwärmen, sieden — die Rechnung steht hier nach dem Heizen.</span>';
      s += '<span class="sim-notiz">Die Platte gibt in jeder Sekunde gleich viel Energie an den Inhalt ab; Verluste an die Umgebung sind nicht eingerechnet. Zeitraffer.' + (vorher ? ' Grau gestrichelt: der vorige Lauf.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    function werteVon(o){
      var Q = [o.m * CEIS * (0 - o.t0), o.m * LF, o.m * CW * 100, o.m * LV], t = Q.map(function(q){ return q / o.P; });
      return { m: o.m, P: o.P, t0: o.t0, Q: Q, t: t, T: t[0] + t[1] + t[2] + t[3] };
    }
    pruefen = Leiste(fig, [
      { text: '\\(0.30\\;\\text{kg}\\) Eis von \\(0\\;^\\circ\\text{C}\\) auf einer Platte mit \\(1000\\;\\text{W}\\): Wie lange dauert das Schmelzen? Rechne zuerst, dann heize und lies ab.', ok: function(s){ var l = s.lauf; return l && gl(l.m, 0.3) && gl(l.P, 1000) && gl(l.t0, 0); },
        vergleich: '\\(Q = m \\cdot L_\\text{f} = 0.30\\;\\text{kg} \\cdot 334\\;\\text{kJ/kg} = 100.2\\;\\text{kJ}\\), \\(t = \\dfrac{Q}{P} = \\dfrac{100\\,200\\;\\text{J}}{1000\\;\\text{W}} \\approx 100\\;\\text{s} \\approx 1.7\\;\\text{min}\\). So lang bleibt die Kurve bei \\(0\\;^\\circ\\text{C}\\) waagrecht.' },
      { text: 'Heize zweimal mit derselben Leistung und Starttemperatur: einmal \\(0.40\\;\\text{kg}\\), einmal \\(0.80\\;\\text{kg}\\) Eis. Was geschieht mit den waagrechten Stücken? Begründe.', ok: function(s){ var l = s.laeufe; for (var i = 0; i < l.length; i++) for (var j = 0; j < l.length; j++) if (gl(l[i].m, 0.4) && gl(l[j].m, 0.8) && gl(l[i].P, l[j].P) && gl(l[i].t0, l[j].t0)) return true; return false; },
        vergleich: 'Sie werden doppelt so lang: \\(t = \\dfrac{m \\cdot L}{P}\\) wächst mit der Masse. Auch die schrägen Stücke dauern doppelt so lang, die Temperaturen der Plateaus bleiben bei \\(0\\;^\\circ\\text{C}\\) und \\(100\\;^\\circ\\text{C}\\).' },
      { text: 'Heize einmal bis zum Ende. Wievielmal so lange wie das Schmelzen dauert das Sieden? Lies ab und begründe mit den Werten von \\(L_\\text{f}\\) und \\(L_\\text{v}\\).', ok: function(s){ return !!s.lauf; },
        vergleich: 'Rund \\(6.75\\)-mal so lange: \\(\\dfrac{L_\\text{v}}{L_\\text{f}} = \\dfrac{2256\\;\\text{kJ/kg}}{334\\;\\text{kJ/kg}} \\approx 6.75\\). Masse und Leistung sind bei beiden Plateaus dieselben, es zählt nur die latente Wärme.' },
      { text: 'Starte bei \\(-30\\;^\\circ\\text{C}\\). Warum steigt die Kurve beim Eis steiler als beim Wasser? Vergleiche die Steigungen und begründe mit \\(c\\).', ok: function(s){ return s.lauf && gl(s.lauf.t0, -30); },
        vergleich: 'Gleiche Leistung, gleiche Masse: \\(\\Delta T = \\dfrac{P \\cdot t}{m \\cdot c}\\). Eis hat \\(c_\\text{Eis} = 2100\\;\\text{J/(kg·K)}\\), rund halb so viel wie Wasser (\\(4182\\;\\text{J/(kg·K)}\\)) — die Eiskurve steigt darum rund doppelt so steil.' },
      { text: 'Stelle die Leistung so ein, dass \\(0.50\\;\\text{kg}\\) Eis von \\(0\\;^\\circ\\text{C}\\) in höchstens \\(2\\;\\text{min}\\) geschmolzen sind, mit so wenig Leistung wie möglich (auf \\(50\\;\\text{W}\\) genau). Rechne, dann prüfe.', ok: function(s){ var l = s.lauf; return l && gl(l.m, 0.5) && gl(l.t0, 0) && gl(l.P, 1400); },
        vergleich: '\\(P = \\dfrac{m \\cdot L_\\text{f}}{t} = \\dfrac{0.50\\;\\text{kg} \\cdot 334\\,000\\;\\text{J/kg}}{120\\;\\text{s}} \\approx 1392\\;\\text{W}\\). Auf dem Regler reichen \\(1400\\;\\text{W}\\) (\\(119\\;\\text{s}\\)); mit \\(1350\\;\\text{W}\\) dauert es \\(124\\;\\text{s}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Heizkessel und Boiler ----------
     Ein Kessel verbrennt die eingestellte Masse Brennstoff (Heizwert H) und gibt die Nutzwärme
     η · m · H an einen Boiler mit 200 l Wasser von 10 °C ab; der Rest geht als Verlust durch den Kamin.
     Heizwerte wie im Leitprogramm Heizen (Heizöl 42.6, Erdgas 50.0, Holzpellets 17.0 MJ/kg). Der
     Massenregler hat je Brennstoff eigene Grenzen, damit das Wasser unter 100 °C bleibt (Erdgas
     1.5 kg bei η = 1: 99.7 °C). Unterschied zur Themenseite (keine Animation zum Heizwert; Animation 5
     zeigt den Wirkungsgrad eines Geräts in Prozent): vom Brennstoff über den Kessel bis zur
     Temperatur des Wassers, in MJ. Clipbeispiel: Pelletofen für 2800 kWh (kein Boiler); Bilder mit
     Erdgas 0.80 kg; Startwerte Heizöl 0.60 kg, η = 0.80 (kein Leistenziel). */
  var BRENN = { oel: { n: 'Heizöl', H: 42.6e6, mn: 0.1, mx: 1.5 }, gas: { n: 'Erdgas', H: 50.0e6, mn: 0.1, mx: 1.5 }, pel: { n: 'Holzpellets', H: 17.0e6, mn: 0.2, mx: 4.0 } };
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,214)' });
    var rm = fig.querySelector('input[data-p="m"]');
    var B = Bedienung(fig, function(){ grenzen(); uhr.stop(); f = 0; ende = false; zeichnen(); });
    var f = 0, ende = false, lauf = null, laeufe = [], vorher = null, pruefen = function(){};
    var MW = 200, TW = 10;
    // Der Massenregler bekommt je Brennstoff andere Grenzen (HOWTO §16: min, max, Wert mitsetzen)
    function grenzen(){ var b = BRENN[B.wert('f')]; if (+rm.max !== b.mx || +rm.min !== b.mn){ rm.min = b.mn; rm.max = b.mx; if (+rm.value > b.mx) rm.value = b.mx; if (+rm.value < b.mn) rm.value = b.mn; } }
    function werte(){
      var b = BRENN[B.wert('f')], m = B.wert('m'), eta = B.wert('eta'), Qz = m * b.H, Qn = eta * Qz;
      return { b: b, f: B.wert('f'), m: m, eta: eta, Qz: Qz, Qn: Qn, V: Qz - Qn, dT: Qn / (MW * CW) };
    }
    function fertig(w){ ende = true; lauf = { f: w.f, m: w.m, eta: w.eta, th: TW + w.dT, Qn: w.Qn }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ var w = werte(); f = Math.min(1, tt / 3); zeichnen(); if (f >= 1){ fertig(w); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Verbrennen', function(){ vorher = lauf; ende = false; f = 0; if (WENIGER){ f = 1; fertig(werte()); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Neu', function(){ uhr.stop(); f = 0; ende = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); f = 0; ende = false; if (o.f) B.setze({ f: o.f }); grenzen(); B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; vorher = null; B.zuruecksetzen(); },
      // Testhaken: Anteil x (0 bis 1) des Brennstoffs verbrannt; ohne Zahl der ganze Lauf
      zeige: function(x){ uhr.stop(); var w = werte(); if (x == null || x >= 1){ f = 1; fertig(w); } else { f = x; ende = false; } zeichnen(); }
    };
    fig.__sim = sim;
    var MJ = function(x){ return sig(x / 1e6) + NB + 'MJ'; };
    function zeichnen(){
      var w = werte(), qz = w.Qz * f, qn = w.Qn * f, qv = w.V * f, th = TW + w.dT * f; B.anzeigen(); leeren(szene); leeren(dia);
      var k = 0.42;                                                      // px je MJ für die Breite der Ströme
      // Brennstoff
      el(szene, 'rect', { x: 2, y: 86, width: 62, height: 44, rx: 4, 'class': 'brennstoff' });
      el(szene, 'text', { x: 33, y: 104, 'text-anchor': 'middle', 'class': 'bt-wert' }, w.b.n);
      el(szene, 'text', { x: 33, y: 119, 'text-anchor': 'middle', 'class': 'bt-wert' }, zahl(+(w.m * (1 - f)).toFixed(2)) + NB + 'kg');
      // Kessel und Kamin
      el(szene, 'rect', { x: 128, y: 30, width: 14, height: 56, 'class': 'kamin' });
      el(szene, 'rect', { x: 104, y: 84, width: 62, height: 50, rx: 5, 'class': 'kessel' });
      el(szene, 'text', { x: 135, y: 106, 'text-anchor': 'middle', 'class': 'bt-wert' }, 'Kessel');
      el(szene, 'text', { x: 135, y: 121, 'text-anchor': 'middle', 'class': 'bt-wert' }, 'η = ' + zahl(w.eta));
      if (f > 0){
        el(szene, 'line', { x1: 64, y1: 108, x2: 98, y2: 108, 'class': 'strom zu', 'stroke-width': Math.max(1.5, qz / 1e6 * k) });
        el(szene, 'line', { x1: 166, y1: 108, x2: 206, y2: 108, 'class': 'strom nutz', 'stroke-width': Math.max(1.5, qn / 1e6 * k) });
        el(szene, 'line', { x1: 135, y1: 80, x2: 135, y2: 22, 'class': 'strom verlust', 'stroke-width': Math.max(1.5, qv / 1e6 * k) });
        el(szene, 'text', { x: 81, y: 108 - qz / 1e6 * k / 2 - 5, 'text-anchor': 'middle', 'class': 'pf-text pf-zu' }, MJ(qz));
        el(szene, 'text', { x: 186, y: 108 + qn / 1e6 * k / 2 + 13, 'text-anchor': 'middle', 'class': 'pf-text pf-nutz' }, MJ(qn));
        el(szene, 'text', { x: 135 + qv / 1e6 * k / 2 + 5, y: 34, 'class': 'pf-text pf-q' }, 'Verlust ' + MJ(qv));
      }
      // Boiler mit 200 l Wasser
      el(szene, 'rect', { x: 208, y: 44, width: 64, height: 120, rx: 10, 'class': 'boiler' });
      el(szene, 'rect', { x: 212, y: 52, width: 56, height: 108, rx: 7, 'class': 'wasser' });
      el(szene, 'text', { x: 240, y: 180, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Boiler, 200 l Wasser');
      thermometer(szene, 288, 150, 50, th / 100, grad(th));
      // Energie in MJ als Balken (feste Achse bis 80 MJ: mehr gibt kein Brennstoff im Regelbereich)
      var X = function(x){ return 70 + x * 2.75; }, rows = [['zugeführt', qz, 'bal-zu'], ['Nutzwärme', qn, 'bal-nutz'], ['Verlust', qv, 'bal-verl']];
      el(dia, 'line', { x1: X(0), y1: 0, x2: X(0), y2: 84, 'class': 'achse' });
      el(dia, 'line', { x1: X(0), y1: 84, x2: X(80) + 6, y2: 84, 'class': 'achse' });
      [20, 40, 60, 80].forEach(function(v){ el(dia, 'line', { x1: X(v), y1: 0, x2: X(v), y2: 84, 'class': 'gitter' }); el(dia, 'text', { x: X(v), y: 97, 'text-anchor': 'middle', 'class': 'skala' }, v); });
      el(dia, 'text', { x: X(80) + 6, y: 110, 'text-anchor': 'end', 'class': 'achsname' }, 'Q [MJ]');
      rows.forEach(function(r, i){
        var y = 8 + i * 26;
        el(dia, 'text', { x: X(0) - 5, y: y + 13, 'text-anchor': 'end', 'class': 'skala' }, r[0]);
        if (r[1] > 0) el(dia, 'rect', { x: X(0), y: y, width: r[1] / 1e6 * 2.75, height: 18, 'class': r[2] });
        if (vorher && !uhr.laeuft()){ var vv = [vorher.m * BRENN[vorher.f].H, vorher.Qn, vorher.m * BRENN[vorher.f].H - vorher.Qn][i]; el(dia, 'line', { x1: X(vv / 1e6), y1: y - 2, x2: X(vv / 1e6), y2: y + 20, 'class': 'vorher' }); }
      });
      var s;
      if (ende && lauf){
        s = '<span>' + q_('zu') + ' = ' + v_('m') + ' · ' + v_('H') + ' = ' + zahl(w.m) + NB + 'kg · ' + fest(w.b.H / 1e6, 1) + NB + 'MJ/kg ' + ist(w.Qz / 1e6, sig(w.Qz / 1e6)) + MJ(w.Qz) + '</span>';
        s += '<span>' + q_('nutz') + ' = ' + v_('η') + ' · ' + v_('m') + ' · ' + v_('H') + ' = ' + zahl(w.eta) + ' · ' + zahl(w.m) + NB + 'kg · ' + fest(w.b.H / 1e6, 1) + NB + 'MJ/kg ' + ist(w.Qn / 1e6, sig(w.Qn / 1e6)) + MJ(w.Qn) + ' (' + sig(w.Qn / 3.6e6) + NB + 'kWh)</span>';
        s += '<span>Δ' + v_('T') + ' = ' + q_('nutz') + ' / (' + v_('m') + '<sub>W</sub> · ' + v_('c') + ') = ' + MJ(w.Qn) + ' / (200' + NB + 'kg · 4182' + NB + 'J/(kg·K)) ≈ ' + sig(w.dT) + NB + 'K → ' + th_() + ' ≈ ' + grad(TW + w.dT) + '</span>';
      } else s = '<span>' + q_('nutz') + ' = ' + v_('η') + ' · ' + v_('m') + ' · ' + v_('H') + ' — die Rechnung steht hier nach dem Verbrennen.</span>';
      s += '<span class="sim-notiz">Boiler: 200' + NB + 'l Wasser, Start bei 10' + NB + '°C. Breite der Ströme und Länge der Balken nach der Energie.' + (vorher ? ' Grau gestrichelt: der vorige Lauf.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    function hat(s, f_, m, eta){ var l = s.lauf; return l && l.f === f_ && gl(l.m, m) && gl(l.eta, eta); }
    pruefen = Leiste(fig, [
      { text: 'Verbrenne \\(1.00\\;\\text{kg}\\) Heizöl mit dem Wirkungsgrad \\(0.90\\). Wie warm wird das Wasser im Boiler? Rechne zuerst, dann verbrenne und vergleiche.', ok: function(s){ return hat(s, 'oel', 1, 0.9); },
        vergleich: '\\(Q_\\text{nutz} = \\eta \\cdot m \\cdot H = 0.90 \\cdot 1.00\\;\\text{kg} \\cdot 42.6\\;\\text{MJ/kg} \\approx 38.3\\;\\text{MJ}\\); \\(\\Delta T = \\dfrac{38.3\\;\\text{MJ}}{200\\;\\text{kg} \\cdot 4182\\;\\text{J/(kg·K)}} \\approx 45.8\\;\\text{K}\\), also rund \\(55.8\\;^\\circ\\text{C}\\).' },
      { text: 'Verbrenne dieselbe Menge desselben Brennstoffs zweimal: mit \\(\\eta = 0.95\\) und mit \\(\\eta = 0.70\\). Wohin geht der Unterschied? Begründe.', ok: function(s){ var l = s.laeufe; for (var i = 0; i < l.length; i++) for (var j = 0; j < l.length; j++) if (l[i].f === l[j].f && gl(l[i].m, l[j].m) && gl(l[i].eta, 0.95) && gl(l[j].eta, 0.7)) return true; return false; },
        vergleich: 'Die zugeführte Energie \\(m \\cdot H\\) ist gleich. Bei \\(\\eta = 0.70\\) gehen \\(30\\;\\%\\) statt \\(5\\;\\%\\) als heisses Abgas durch den Kamin — sie fehlen dem Wasser. Verschwunden ist die Energie nicht: Sie wärmt Kamin und Umgebung.' },
      { text: 'Wie viel Holzpellets ersetzen \\(1.00\\;\\text{kg}\\) Erdgas, bei gleichem Wirkungsgrad? Rechne, verbrenne beides und vergleiche die Temperaturen.', ok: function(s){ var g = null, p = null; s.laeufe.forEach(function(l){ if (l.f === 'gas' && gl(l.m, 1)) g = l; if (l.f === 'pel' && Math.abs(l.m - 50 / 17) <= 0.051) p = l; }); return g && p && gl(g.eta, p.eta); },
        vergleich: 'Gleiche Energie heisst \\(m_\\text{P} \\cdot 17.0\\;\\text{MJ/kg} = 1.00\\;\\text{kg} \\cdot 50.0\\;\\text{MJ/kg}\\), also \\(m_\\text{P} \\approx 2.94\\;\\text{kg}\\) — fast dreimal so viel Masse. Auf dem Regler passen \\(2.90\\;\\text{kg}\\) oder \\(2.95\\;\\text{kg}\\).' },
      { text: 'Mit Holzpellets und \\(\\eta = 0.85\\) soll das Wasser mindestens \\(60\\;^\\circ\\text{C}\\) warm werden. Welche Masse reicht gerade (auf \\(0.05\\;\\text{kg}\\) genau)? Rechne, dann prüfe.', ok: function(s){ return hat(s, 'pel', 2.9, 0.85); },
        vergleich: '\\(Q_\\text{nutz} = 200\\;\\text{kg} \\cdot 4182\\;\\text{J/(kg·K)} \\cdot 50\\;\\text{K} = 41.8\\;\\text{MJ}\\); \\(m = \\dfrac{Q_\\text{nutz}}{\\eta \\cdot H} = \\dfrac{41.8\\;\\text{MJ}}{0.85 \\cdot 17.0\\;\\text{MJ/kg}} \\approx 2.89\\;\\text{kg}\\). Mit \\(2.90\\;\\text{kg}\\) werden es \\(60.1\\;^\\circ\\text{C}\\), mit \\(2.85\\;\\text{kg}\\) nur \\(59.2\\;^\\circ\\text{C}\\).' },
      { text: 'Verbrenne \\(1.50\\;\\text{kg}\\) Heizöl mit \\(\\eta = 0.88\\). Wie viele Kilowattstunden Nutzwärme sind das? Rechne zuerst in MJ, dann in kWh.', ok: function(s){ return hat(s, 'oel', 1.5, 0.88); },
        vergleich: '\\(Q_\\text{nutz} = 0.88 \\cdot 1.50\\;\\text{kg} \\cdot 42.6\\;\\text{MJ/kg} \\approx 56.2\\;\\text{MJ}\\). Mit \\(1\\;\\text{kWh} = 3.6\\;\\text{MJ}\\): \\(\\dfrac{56.2\\;\\text{MJ}}{3.6\\;\\text{MJ/kWh}} \\approx 15.6\\;\\text{kWh}\\).' }
    ], sim);
    grenzen(); zeichnen();
  })();

  /* ---------- Kapitel 5: Energiesysteme vergleichen ----------
     Sechs Systeme mit demselben Raster: Energiefluss je 100 kWh, die hineinfliessen (bei der
     Wärmepumpe je 100 kWh Heizwärme), Lieferung im Sommer- und im Winterhalbjahr gegen den Bedarf
     eines Haushalts, dazu die Menge, die es für die eingestellte Jahresenergie braucht, und das
     Kohlendioxid über den Lebensweg (IPCC 2014, Medianwerte). Alle Wirkungsgrade und Anteile sind
     gerundete Modellannahmen und stehen in der Notiz; gerechnet wird mit Formeln aus 4.3 und 5.2
     (Lageenergie, Heizwert, Leistungszahl). Unterschied zur Themenseite (Animation 6 nur Wärmepumpe;
     die übrigen Systeme nur im Text): die sieben Systeme der Kompetenz an sechs Knöpfen (Biogas und WKK
     zusammen) nach denselben Gesichtspunkten nebeneinander. Der Clip rechnet Photovoltaik für eine Gemeinde
     (2 Mio. kWh); die Leiste fragt einen Haushalt (4500 kWh im Jahr) und macht die Winterlücke sichtbar
     (Startwerte: Biogas-WKK, 3000 kWh). */
  var SYS = {
    wasser: { n: 'Wasserkraft (Speichersee)', q: 'Quelle, erneuerbar', ein: [['Lageenergie', 100]], aus: [['Strom', 85, 'nutz'], ['Abwärme', 15, 'verl']],
              so: null, co2: 'rund 24 g', verf: 'speicherbar, liefert auf Abruf' },
    wind:   { n: 'Windkraft', q: 'Quelle, erneuerbar', ein: [['Wind', 100]], aus: [['Strom', 45, 'nutz'], ['bleibt im Wind', 55, 'rest']],
              so: [35, 65], co2: 'rund 11 g', verf: 'wetterabhängig, im Winter mehr' },
    pv:     { n: 'Photovoltaik', q: 'Quelle, erneuerbar', ein: [['Sonnenlicht', 100]], aus: [['Strom', 20, 'nutz'], ['Abwärme', 80, 'verl']],
              so: [70, 30], co2: 'rund 41 g', verf: 'nur bei Tag, im Sommer viel mehr' },
    wkk:    { n: 'Biogas-WKK', q: 'Biogas: Quelle, erneuerbar; WKK: Technik', ein: [['Biogas', 100]], aus: [['Strom', 35, 'nutz'], ['Nutzwärme', 55, 'waerme'], ['Abwärme', 10, 'verl']],
              so: [50, 50], co2: 'gering, wenn das Gas aus Gülle und Abfällen stammt', verf: 'speicherbar, gleichmässig' },
    kern:   { n: 'Kernkraftwerk', q: 'Quelle, nicht erneuerbar (Uranvorrat)', ein: [['Kernspaltung', 100]], aus: [['Strom', 33, 'nutz'], ['Abwärme', 67, 'verl']],
              so: [50, 50], co2: 'rund 12 g', verf: 'gleichmässig, Tag und Nacht' },
    wp:     { n: 'Wärmepumpe', q: 'keine Quelle: Technik, braucht Strom', ein: [['Strom', 25], ['Umgebung', 75]], aus: [['Heizwärme', 100, 'waerme']],
              so: [25, 75], co2: 'hängt davon ab, woher der Strom kommt', verf: 'braucht vor allem im Winter Strom' }
  };
  var BEDARF = [45, 55];                                                  // Strombedarf eines Haushalts, Modell
  var NOTIZ5 = {
    wasser: 'Modell: Turbine, Generator und Leitungen zusammen 85 %; Fallhöhe 500 m. Ein Speichersee liefert dann, wenn Strom gebraucht wird.',
    wind: 'Modell: Die Turbine nutzt rund 45 % der Bewegungsenergie der Luft, die durch die Rotorfläche strömt (möglich sind höchstens 59 %); Turbine mit 2 MW und rund 1800 Volllaststunden: 3.6 GWh im Jahr.',
    pv: 'Modell: Module mit 20 % Wirkungsgrad, 1100 kWh Sonnenlicht je m² und Jahr; 70 % des Ertrags im Sommerhalbjahr.',
    wkk: 'Modell: Biogas mit 6 kWh je m³ (Heizwert); die WKK macht daraus 35 % Strom und 55 % Nutzwärme.',
    kern: 'Modell: Das Kraftwerk macht 33 % der Wärme aus der Kernspaltung zu Strom; 1 g gespaltenes Uran-235 setzt rund 22 800 kWh Wärme frei.',
    wp: 'Modell: Leistungszahl im Jahresmittel 4.0; die Heizwärme wird zu drei Vierteln im Winterhalbjahr gebraucht, die Wärmepumpe braucht ihren Strom darum vor allem im Winter.'
  };
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,176)' });
    var lab = fig.querySelector('label[for="s5-E"]');
    var B = Bedienung(fig, function(){ zeichnen(); });
    var pruefen = function(){};
    function zehner(x){ var k = Math.floor(Math.log10(x)); return (+(x / Math.pow(10, k)).toPrecision(3)) + ' · 10<sup>' + k + '</sup>'; }
    function menge(sys, E){
      if (sys === 'wasser') return { v: E * 3.6e6 / (0.85 * 1000 * 9.81 * 500), z: v_('V') + ' = ' + v_('E') + ' / (' + v_('η') + ' · ' + v_('ρ') + ' · ' + v_('g') + ' · ' + v_('h') + ') = ' + zehner(E * 3.6e6) + NB + 'J / (0.85 · 1000' + NB + 'kg/m³ · 9.81' + NB + 'm/s² · 500' + NB + 'm)', u: 'm³ Wasser, die 500' + NB + 'm tief fallen' };
      if (sys === 'wind') return { v: E / 3.6e6 * 100, z: 'Anteil = ' + v_('E') + ' / 3.6' + NB + 'GWh = ' + zahl(E) + NB + 'kWh / 3' + NB + '600' + NB + '000' + NB + 'kWh', u: '% der Jahresproduktion einer Windturbine' };
      if (sys === 'pv') return { v: E / 220, z: v_('A') + ' = ' + v_('E') + ' / (' + v_('η') + ' · 1100' + NB + 'kWh/m²) = ' + zahl(E) + NB + 'kWh / (0.20 · 1100' + NB + 'kWh/m²)', u: 'm² Module' };
      if (sys === 'wkk') return { v: E / (0.35 * 6), z: v_('V') + ' = ' + v_('E') + ' / (' + v_('η') + '<sub>el</sub> · ' + v_('H') + ') = ' + zahl(E) + NB + 'kWh / (0.35 · 6' + NB + 'kWh/m³)', u: 'm³ Biogas' };
      if (sys === 'kern') return { v: E / (0.33 * 22778), z: v_('m') + ' = ' + v_('E') + ' / (' + v_('η') + ' · 22' + NB + '800' + NB + 'kWh/g) = ' + zahl(E) + NB + 'kWh / (0.33 · 22' + NB + '800' + NB + 'kWh/g)', u: 'g Uran-235, die gespalten werden' };
      return { v: E / 4, z: v_('E') + '<sub>el</sub> = ' + v_('Q') + '<sub>warm</sub> / COP = ' + zahl(E) + NB + 'kWh / 4.0', u: 'kWh Strom; der Rest kommt aus der Umgebung' };
    }
    var sim = {
      zustand: function(){ return { sys: B.wert('sys'), E: B.wert('E'), gesehen: function(w){ return B.gesehen('sys') && seen[w]; } }; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ B.zuruecksetzen(); seen = {}; seen[B.wert('sys')] = true; },
      zeige: function(){ zeichnen(); }
    };
    var seen = {};
    fig.__sim = sim;
    function zeichnen(){
      var sys = B.wert('sys'), S = SYS[sys], E = B.wert('E'); seen[sys] = true;
      B.anzeigen(); leeren(szene); leeren(dia);
      if (lab) lab.innerHTML = sys === 'wp' ? '<i>Q</i> Heizwärme' : '<i>E</i> Strom';
      // Energiefluss: links hinein (Orange), rechts heraus; Höhe 1.15 px je kWh von 100
      var k = 1.15, yo = 28, xl = 8, xb = 140, xr = 206;
      el(szene, 'text', { x: 150, y: 14, 'text-anchor': 'middle', 'class': 'bt-meldung' }, sys === 'wp' ? 'je 100 kWh Heizwärme' : 'je 100 kWh, die hineinfliessen');
      var y = yo;
      S.ein.forEach(function(e, i){
        var h = e[1] * k;
        el(szene, 'rect', { x: xl, y: y, width: 18, height: h, 'class': i ? 'fl-umg' : 'fl-zu' });
        el(szene, 'path', { d: 'M26 ' + y + ' L' + xb + ' ' + (yo + (y - yo) * 0.6) + ' L' + xb + ' ' + (yo + (y - yo + h) * 0.6) + ' L26 ' + (y + h) + ' Z', 'class': i ? 'fl-umg band' : 'fl-zu band' });
        el(szene, 'text', { x: 30, y: y + h / 2 + 4, 'class': 'bt-wert' }, sig(e[1]) + NB + 'kWh ' + e[0]);
        y += h;
      });
      el(szene, 'rect', { x: xb, y: yo - 4, width: 18, height: 100 * k * 0.6 + 8, rx: 3, 'class': 'kessel' });
      y = yo;
      S.aus.forEach(function(a){
        var h = a[1] * k, ya = yo + (y - yo) * 0.6, yb = yo + (y - yo + h) * 0.6;
        el(szene, 'path', { d: 'M' + (xb + 18) + ' ' + ya + ' L' + xr + ' ' + y + ' L' + xr + ' ' + (y + h) + ' L' + (xb + 18) + ' ' + yb + ' Z', 'class': 'fl-' + a[2] + ' band' });
        el(szene, 'rect', { x: xr, y: y, width: 14, height: h, 'class': 'fl-' + a[2] });
        var ty = y + Math.max(10, h / 2 - 2);
        el(szene, 'text', { x: xr + 18, y: ty, 'class': 'bt-wert' }, sig(a[1]) + NB + 'kWh');
        el(szene, 'text', { x: xr + 18, y: ty + 11, 'class': 'bt-klein' }, a[0]);
        y += h;
      });
      // Sommer- und Winterhalbjahr: Anteil der Jahreslieferung gegen den Bedarf (gestrichelt)
      var X0 = 46, Hh = 92, Y = function(p){ return 104 - p / 92 * Hh; };   // Platz über dem höchsten Balken (75 %) für die Legende
      el(dia, 'line', { x1: X0, y1: Y(0), x2: 296, y2: Y(0), 'class': 'achse' });
      el(dia, 'line', { x1: X0, y1: Y(0), x2: X0, y2: Y(90), 'class': 'achse' });
      [20, 40, 60, 80].forEach(function(p){ el(dia, 'line', { x1: X0, y1: Y(p), x2: 296, y2: Y(p), 'class': 'gitter' }); el(dia, 'text', { x: X0 - 4, y: Y(p) + 3.5, 'text-anchor': 'end', 'class': 'skala' }, p); });
      stext(dia, { x: X0 + 4, y: 6, 'class': 'achsname' }, 'Anteil [%]');
      ['Sommerhalbjahr', 'Winterhalbjahr'].forEach(function(t, i){
        var x = 80 + i * 112, so = S.so ? S.so[i] : BEDARF[i];
        el(dia, 'rect', { x: x, y: Y(so), width: 46, height: Y(0) - Y(so), 'class': sys === 'wp' ? 'fl-zu' : (S.so ? 'fl-nutz' : 'fl-nutz abruf') });
        if (sys !== 'wp') el(dia, 'rect', { x: x + 50, y: Y(BEDARF[i]), width: 30, height: Y(0) - Y(BEDARF[i]), 'class': 'bedarf' });
        el(dia, 'text', { x: x + 23, y: Y(so) - 4, 'text-anchor': 'middle', 'class': 'bt-wert' }, so + ' %');
        el(dia, 'text', { x: x + 40, y: Y(0) + 13, 'text-anchor': 'middle', 'class': 'skala' }, t);
      });
      el(dia, 'text', { x: 296, y: 6, 'text-anchor': 'end', 'class': 'legende' }, sys === 'wp' ? 'Strombedarf der Wärmepumpe' : (S.so ? 'grün: Lieferung; gestrichelt: Bedarf' : 'auf Abruf: so, wie es gebraucht wird'));
      var M = menge(sys, E), s = '';
      s += '<span>' + S.n + ' — ' + S.q + '</span>';
      s += '<span>Für ' + zahl(E) + NB + 'kWh ' + (sys === 'wp' ? 'Heizwärme' : 'Strom') + ' im Jahr: ' + M.z + ' ' + ist(M.v, sig(M.v)) + sig(M.v) + NB + M.u + '</span>';
      s += '<span>Verfügbarkeit: ' + S.verf + '; Kohlendioxid über den Lebensweg: ' + S.co2 + (sys === 'wkk' || sys === 'wp' ? '' : ' je kWh Strom') + ' (Erdgaskraftwerk: rund 490 g)</span>';
      s += '<span class="sim-notiz">' + NOTIZ5[sys] + (sys === 'wp' ? '' : ' Halbjahre gerundet; Bedarf eines Haushalts: 45 % im Sommer, 55 % im Winter.') + '</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Photovoltaik: Stelle \\(4500\\;\\text{kWh}\\) Strom im Jahr ein. Wie viel Modulfläche braucht es, und wie viel Strom liefert sie im Winterhalbjahr — gegen wie viel Bedarf? Notiere, dann vergleiche.', ok: function(s){ return s.sys === 'pv' && gl(s.E, 4500); },
        vergleich: '\\(A = \\dfrac{4500\\;\\text{kWh}}{0.20 \\cdot 1100\\;\\text{kWh/m}^2} \\approx 20.5\\;\\text{m}^2\\). Im Winterhalbjahr kommen nur \\(30\\;\\%\\), also \\(1350\\;\\text{kWh}\\) — gebraucht werden \\(55\\;\\%\\), also \\(2475\\;\\text{kWh}\\). Übers Jahr reicht es, im Winter nicht.' },
      { text: 'Finde das System, das im Winterhalbjahr deutlich mehr liefert als im Sommer (den Speichersee nicht mitgezählt). Warum ergänzt es die Photovoltaik gut?', ok: function(s){ return s.sys === 'wind'; },
        vergleich: 'Die Windkraft: rund \\(65\\;\\%\\) im Winterhalbjahr. Sie liefert dann, wenn die Photovoltaik wenig bringt — zusammen gleichen sie sich übers Jahr teilweise aus.' },
      { text: 'Vergleiche Wasserkraft und Biogas-WKK: Welches System macht den grössten Anteil Strom, welches nutzt insgesamt am meisten? Schau dir beide an und notiere.', ok: function(s){ return s.gesehen('wasser') && s.gesehen('wkk'); },
        vergleich: 'Am meisten Strom: die Wasserkraft (\\(85\\;\\%\\)). Insgesamt am meisten: die Biogas-WKK (\\(35\\;\\%\\) Strom und \\(55\\;\\%\\) Wärme, zusammen \\(90\\;\\%\\)) — sie nutzt die Abwärme, statt sie wegzukühlen.' },
      { text: 'Kernkraftwerk: Wie viel Abwärme fällt je Kilowattstunde Strom an? Wie liesse sie sich nutzen? Notiere, dann vergleiche.', ok: function(s){ return s.sys === 'kern'; },
        vergleich: 'Je \\(33\\;\\text{kWh}\\) Strom entstehen \\(67\\;\\text{kWh}\\) Abwärme, also rund \\(2\\;\\text{kWh}\\) je kWh Strom. Meist geht sie über Fluss oder Kühlturm in die Umgebung; als Fernwärme genutzt, wird das Werk zur Wärme-Kraft-Kopplung.' },
      { text: 'Wärmepumpe: Welcher Anteil der Heizwärme kommt aus der Umgebung? Ist die Wärmepumpe eine Energiequelle? Begründe.', ok: function(s){ return s.sys === 'wp'; },
        vergleich: 'Aus der Umgebung (Luft, Erdreich, Grundwasser): Bei COP 4.0 stammen \\(\\dfrac{3}{4} = 75\\;\\%\\) der Heizwärme von dort. Eine Quelle ist sie nicht — sie braucht Strom, um vorhandene Wärme auf Heiztemperatur zu heben.' }
    ], sim);
    seen[B.wert('sys')] = true;
    zeichnen();
  })();

  /* ---------- Kapitel 6: Wärmewege im Labor ----------
     Zwischen einer heissen (80 °C) und einer kalten Platte (20 °C), je 10 cm × 10 cm, liegt eine
     2 cm dicke Schicht: Kupfer, Holz, Wasser, Luft oder Vakuum. Auf Knopfdruck wird der Wärmestrom
     gemessen, getrennt nach Leitung (λ · A · ΔT / d), Konvektion (nur in Flüssigkeit und Gas und nur,
     wenn die heisse Platte unten ist; Nusselt-Zahl nach Hollands: Luft 3.1, Wasser 17.7) und Strahlung
     (nur durch Vakuum und Luft; Emissionsgrad 0.95 schwarz, 0.05 verspiegelt). Achse logarithmisch.
     Unterschied zur Themenseite (Animation 4 zeigt die drei Wege als Bild): die Wege messen und durch
     die Wahl von Stoff, Lage und Oberfläche einzeln ein- und ausschalten. Startwerte: Luft, heiss oben,
     schwarz (kein Leistenziel). */
  var FUELL = { kupfer: { n: 'Kupfer', l: 400, fl: false, durch: false }, holz: { n: 'Holz', l: 0.15, fl: false, durch: false },
                wasser: { n: 'Wasser', l: 0.60, fl: true, nu: 17.7, durch: false }, luft: { n: 'Luft', l: 0.026, fl: true, nu: 3.1, durch: true },
                vakuum: { n: 'Vakuum', l: 0, fl: false, durch: true } };
  (function(){
    var fig = document.getElementById('sim6'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,172)' });
    var B = Bedienung(fig, function(){ uhr.stop(); u = 0; ende = false; zeichnen(); });
    var u = 0, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var RAD = { schwarz: 4.632 / (2 / 0.95 - 1), spiegel: 4.632 / (2 / 0.05 - 1) };   // σ · A · (353.15⁴ − 293.15⁴) = 4.632 W
    function werte(){
      var F = FUELL[B.wert('fu')], lage = B.wert('lage'), ob = B.wert('ob');
      var L = 30 * F.l, Kv = F.fl && lage === 'unten' ? L * (F.nu - 1) : 0, S = F.durch ? RAD[ob] : 0;
      return { F: F, fu: B.wert('fu'), lage: lage, ob: ob, L: L, K: Kv, S: S, ges: L + Kv + S };
    }
    function fertig(w){ ende = true; lauf = { fu: w.fu, lage: w.lage, ob: w.ob, L: w.L, K: w.K, S: w.S, ges: w.ges }; laeufe.push(lauf); }
    var uhr = Uhr(function(tt){ u = Math.min(1, tt / 1.5); zeichnen(); if (u >= 1){ fertig(werte()); zeichnen(); return false; } });
    aktionen(fig, [['start', '▶ Messen', function(){ ende = false; u = 0; if (WENIGER){ u = 1; fertig(werte()); zeichnen(); } else uhr.start(0); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); u = 0; ende = false; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(){ uhr.stop(); u = 1; fertig(werte()); zeichnen(); }
    };
    fig.__sim = sim;
    function welle(x, y1, y2){ var d = 'M' + x + ' ' + y1, n = 6, h = (y2 - y1) / n; for (var i = 0; i < n; i++) d += ' q ' + (i % 2 ? -5 : 5) + ' ' + (h / 2) + ' 0 ' + h; return d; }
    function zeichnen(){
      var w = werte(); B.anzeigen(); leeren(szene); leeren(dia);
      var oben = w.lage === 'oben', yo = 40, yu = 120, xa = 40, xb = 220;
      // Platten: heiss (rot getönt) und kalt; die Schicht dazwischen
      el(szene, 'rect', { x: xa, y: yo + 8, width: xb - xa, height: yu - yo - 8, 'class': 'schicht ' + w.fu });
      if (w.fu === 'vakuum') el(szene, 'text', { x: xa + 40, y: (yo + yu) / 2 + 8, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Vakuum');
      el(szene, 'rect', { x: xa - 4, y: yo, width: xb - xa + 8, height: 8, 'class': 'platte-' + (oben ? 'heiss' : 'kalt') + (w.ob === 'spiegel' ? ' spiegel' : '') });
      el(szene, 'rect', { x: xa - 4, y: yu, width: xb - xa + 8, height: 8, 'class': 'platte-' + (oben ? 'kalt' : 'heiss') + (w.ob === 'spiegel' ? ' spiegel' : '') });
      el(szene, 'text', { x: xb + 10, y: yo + 8, 'class': 'bt-wert' }, oben ? '80 °C' : '20 °C');
      el(szene, 'text', { x: xb + 10, y: yu + 8, 'class': 'bt-wert' }, oben ? '20 °C' : '80 °C');
      el(szene, 'text', { x: xb + 10, y: (yo + yu) / 2 + 8, 'class': 'bt-klein' }, w.F.n + ', 2 cm');
      // Wege nach dem Messen (während des Messens einblendend)
      if (u > 0){
        var a = Math.min(1, u * 1.5), ys = oben ? yo + 10 : yu - 2, ye = oben ? yu - 2 : yo + 10;
        if (w.L > 0) [70, 100].forEach(function(x){ pfeil(szene, x, ys, x, ye, 'pf-q', 6); });
        if (w.K > 0) [150, 190].forEach(function(x, i){ el(szene, 'path', { d: 'M' + (x - 12) + ' ' + (yu - 12) + ' C ' + (x - 18) + ' ' + (yo + 14) + ', ' + (x + 18) + ' ' + (yo + 14) + ', ' + (x + 12) + ' ' + (yu - 12), 'class': 'konv', opacity: a }); });
        if (w.S > 0.5) [125, 135].forEach(function(x){ el(szene, 'path', { d: welle(x, ys, ye), 'class': 'welle', opacity: a }); });
        else if (w.S > 0) el(szene, 'path', { d: welle(130, ys, (ys + ye) / 2), 'class': 'welle duenn', opacity: a });
        if (!ende) el(szene, 'text', { x: 4, y: 160, 'class': 'bt-klein' }, 'misst …');
        else el(szene, 'text', { x: 130, y: 152, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'gerade Pfeile: Leitung; Schleifen: Konvektion; Wellen: Strahlung');
      }
      // Messwerte, logarithmische Achse von 0.01 W bis 100 000 W
      var X = function(p){ return 82 + (Math.log10(p) + 2) * 30; }, rows = [['Leitung', 'L'], ['Konvektion', 'K'], ['Strahlung', 'S']];
      el(dia, 'line', { x1: X(0.01), y1: 0, x2: X(0.01), y2: 84, 'class': 'achse' });
      el(dia, 'line', { x1: X(0.01), y1: 84, x2: X(1e5) + 4, y2: 84, 'class': 'achse' });
      [[0.01, '0.01'], [1, '1'], [100, '100'], [1e4, '10 000']].forEach(function(p){ el(dia, 'text', { x: X(p[0]), y: 97, 'text-anchor': 'middle', 'class': 'skala' }, p[1]); });
      [0.1, 1, 10, 100, 1000, 1e4, 1e5].forEach(function(p){ el(dia, 'line', { x1: X(p), y1: 0, x2: X(p), y2: 84, 'class': 'gitter' }); });
      el(dia, 'text', { x: 296, y: 110, 'text-anchor': 'end', 'class': 'achsname' }, 'Wärmestrom [W], logarithmisch');
      rows.forEach(function(r, i){
        var y = 6 + i * 26, p = w[r[1]];
        el(dia, 'text', { x: X(0.01) - 5, y: y + 13, 'text-anchor': 'end', 'class': 'skala' }, r[0]);
        if (!ende) return;
        if (p > 0){ el(dia, 'rect', { x: X(0.01), y: y, width: X(p) - X(0.01), height: 18, 'class': 'bal-q' });
          var innen = X(p) > 226; el(dia, 'text', { x: innen ? X(p) - 4 : X(p) + 4, y: y + 13, 'text-anchor': innen ? 'end' : 'start', 'class': 'bt-wert' }, 'P ≈ ' + sig(p, 2) + NB + 'W'); }
        else el(dia, 'text', { x: X(0.01) + 4, y: y + 13, 'class': 'bt-klein' }, 'wirkt nicht');
      });
      var s;
      if (ende && lauf){
        s = '<span>Wärmestrom gesamt: ' + v_('P') + ' ≈ ' + sig(w.ges, 2) + NB + 'W (Leitung ' + sig(w.L, 2) + NB + 'W; Konvektion ' + sig(w.K, 2) + NB + 'W; Strahlung ' + sig(w.S, 2) + NB + 'W)</span>';
        s += '<span>' + (w.L > 0 ? 'Leitung, weil Stoff zwischen den Platten liegt' : 'keine Leitung: kein Stoff') + '; ' + (w.K > 0 ? 'Konvektion, weil die warme ' + (w.fu === 'wasser' ? 'Flüssigkeit' : 'Luft') + ' unten aufsteigt' : (w.F.fl ? 'keine Konvektion: Die warme Schicht liegt oben' : 'keine Konvektion: nichts kann strömen')) + '; ' + (w.S > 0 ? 'Strahlung, weil die Schicht Infrarot durchlässt' : 'keine Strahlung durch die Schicht: ' + w.F.n + ' schluckt das Infrarot') + '</span>';
      } else s = '<span>Wähle Füllung, Lage und Oberfläche, dann miss den Wärmestrom.</span>';
      s += '<span class="sim-notiz">Platten 10 cm × 10 cm, 2 cm Abstand, 80 °C und 20 °C. Modellrechnung mit Tabellenwerten (Wärmeleitfähigkeit: Kupfer 400, Holz 0.15, Wasser 0.6, Luft 0.026 W/(m·K)). Achse logarithmisch: Jeder Teilstrich ist das Zehnfache des vorigen.</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    function war(s, f){ return s.laeufe.some(f); }
    pruefen = Leiste(fig, [
      { text: 'Finde eine Füllung, bei der nur die Strahlung Wärme überträgt, und miss. Warum fallen Leitung und Konvektion weg? Notiere, dann vergleiche.', ok: function(s){ return s.lauf && s.lauf.fu === 'vakuum'; },
        vergleich: 'Im Vakuum: Ohne Teilchen kann nichts Energie an Nachbarn weitergeben (keine Leitung) und nichts strömen (keine Konvektion). Strahlung braucht keinen Stoff — so kommt auch die Sonnenwärme durch den leeren Weltraum.' },
      { text: 'Luft zwischen den Platten: Miss einmal mit der heissen Platte unten und einmal oben. Warum ist der Wärmestrom verschieden?', ok: function(s){ return war(s, function(l){ return l.fu === 'luft' && l.lage === 'unten'; }) && war(s, function(l){ return l.fu === 'luft' && l.lage === 'oben'; }); },
        vergleich: 'Unten erwärmte Luft dehnt sich aus, wird leichter und steigt auf, kalte sinkt nach: Konvektion. Liegt die heisse Platte oben, bleibt die warme Luft oben liegen — es strömt nichts, es bleiben Leitung und Strahlung.' },
      { text: 'Miss mit Kupfer und mit Holz. Wievielmal so viel Wärme leitet Kupfer? Vergleiche mit den Werten der Wärmeleitfähigkeit.', ok: function(s){ return war(s, function(l){ return l.fu === 'kupfer'; }) && war(s, function(l){ return l.fu === 'holz'; }); },
        vergleich: '\\(12\\,000\\;\\text{W}\\) gegen \\(4.5\\;\\text{W}\\): rund \\(2700\\)-mal so viel, genau das Verhältnis \\(\\dfrac{400}{0.15} \\approx 2700\\) der Wärmeleitfähigkeiten. Darum haben Pfannen Holzgriffe.' },
      { text: 'Wasser ist durchsichtig. Miss mit Wasser: Welcher Weg fehlt trotzdem? Was folgt daraus für Wärmestrahlung und Licht?', ok: function(s){ return s.lauf && s.lauf.fu === 'wasser'; },
        vergleich: 'Die Strahlung: Wasser lässt sichtbares Licht durch, schluckt aber das Infrarot schon auf wenigen Millimetern. Durchsichtig für Licht heisst nicht durchlässig für Wärmestrahlung — derselbe Unterschied ist der Kern des Treibhauseffekts (Kapitel 7).' },
      { text: 'Bremse den Wärmestrom so stark wie möglich und miss. Wievielmal kleiner ist er als mit Luft (heisse Platte oben, schwarz)? Welcher Weg bleibt übrig?', ok: function(s){ return s.lauf && s.lauf.fu === 'vakuum' && s.lauf.ob === 'spiegel'; },
        vergleich: 'Vakuum und verspiegelte Flächen: rund \\(0.12\\;\\text{W}\\) statt rund \\(5\\;\\text{W}\\) — rund \\(40\\)-mal weniger. Das Vakuum unterbindet Leitung und Konvektion; übrig bleibt nur die Strahlung, und die werfen die Spiegel fast ganz zurück.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 7: Wie durchlässig ist die Atmosphäre? ----------
     Einschichtmodell: Die Erde nimmt im Mittel S = 240 W/m² Sonnenlicht auf (nach Abzug des reflektierten
     Teils, wie Leitprogramm Energie, Kapitel 6: (1 − a) · S/4 ≈ 238 W/m², hier gerundet). Die Atmosphäre
     lässt den Anteil D_L des Lichts und den Anteil D_W der Wärmestrahlung des Bodens durch; was sie
     aufnimmt, strahlt sie je zur Hälfte nach oben und nach unten ab. Bilanz von Boden und Atmosphäre:
     Bodenstrahlung U = S · (1 + D_L) / (1 + D_W), Gegenstrahlung A = U − D_L · S, T = (U / σ)^(1/4).
     Ohne Wind, Wolken und Verdunstung. Unterschied zur Themenseite (Animation 7: zwölf Strahlen nach der
     CO₂-Konzentration) und zum Leitprogramm Energie (Kapitel 6: Bilanz über die Zeit): die beiden
     Durchlässigkeiten getrennt einstellen — Erwärmung gibt es nur, wenn das Licht leichter durchkommt
     als die Wärmestrahlung. Pfeilbreiten im selben Massstab (0.075 px je W/m²). Eine Modelleinstellung
     für Seite, Clips, Aufgaben und Test: Licht 100 %, Wärmestrahlung 23 % → 14.9 °C (gemessen rund 15 °C),
     Boden 390 W/m², Gegenstrahlung 150 W/m² (wirklich rund 340 W/m²: die Atmosphäre nimmt auch Licht auf,
     und der Boden gibt Wärme durch Verdunstung und aufsteigende Luft ab). Vorindustriell 25 % → 13.7 °C:
     rund 1.2 K, wie gemessen. Startwerte 80 % und 60 % (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim7'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg);
    var B = Bedienung(fig, function(){ zeichnen(); });
    var pruefen = function(){};
    var S = 240, k = 0.075;
    function werte(){ var dl = B.wert('dl') / 100, dw = B.wert('dw') / 100, U = S * (1 + dl) / (1 + dw), A = U - dl * S, T = Math.pow(U / SIGMA, 0.25);
      return { dl: dl, dw: dw, U: U, A: A, T: T, th: T - 273.15 }; }
    var sim = { zustand: function(){ return werte(); }, zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); zeichnen(); }, aufraeumen: function(){ B.zuruecksetzen(); }, zeige: function(){ zeichnen(); } };
    fig.__sim = sim;
    function band(x, y1, y2, wert, cls){ var b = Math.max(1, wert * k); el(szene, 'rect', { x: x - b / 2, y: Math.min(y1, y2), width: b, height: Math.abs(y2 - y1), 'class': cls });
      var sp = y2 > y1 ? y2 : y1 - 0, dir = y2 > y1 ? 1 : -1, s = Math.max(5, b * 0.35);
      el(szene, 'polygon', { points: (x - b / 2 - 3) + ',' + (y2 - dir * s) + ' ' + (x + b / 2 + 3) + ',' + (y2 - dir * s) + ' ' + x + ',' + (y2 + dir * 2), 'class': cls }); }
    function zeichnen(){
      var w = werte(); B.anzeigen(); leeren(szene);
      var ya1 = 96, ya2 = 146, yb = 262;
      el(szene, 'rect', { x: 0, y: ya1, width: 300, height: ya2 - ya1, 'class': 'atmo', opacity: (0.18 + 0.5 * (1 - w.dw)).toFixed(2) });
      el(szene, 'text', { x: 296, y: ya1 + 13, 'text-anchor': 'end', 'class': 'bt-klein' }, 'Atmosphäre');
      el(szene, 'rect', { x: 0, y: yb, width: 300, height: 20, 'class': 'boden' });
      el(szene, 'circle', { cx: 18, cy: 16, r: 11, 'class': 'sonne' });
      // Licht: herein, zum Boden durch (Rest bleibt in der Atmosphäre)
      band(48, 18, ya1, S, 'licht');
      el(szene, 'text', { x: 62, y: 46, 'class': 'bt-wert l-licht' }, S + NB + 'W/m² Licht');
      if (w.dl > 0) band(48, ya2, yb - 2, w.dl * S, 'licht');
      el(szene, 'text', { x: 62, y: ya2 + 22, 'class': 'bt-wert l-licht' }, fest(w.dl * S, 0) + NB + 'W/m² durch');
      if (w.dl < 1) el(szene, 'text', { x: 62, y: ya1 + 30, 'class': 'bt-klein' }, fest((1 - w.dl) * S, 0) + NB + 'W/m² bleiben im Gas');
      // Wärmestrahlung des Bodens: nach oben, ein Teil direkt hinaus
      band(150, yb - 2, ya2, w.U, 'ir');
      el(szene, 'text', { x: 150 + w.U * k / 2 + 4, y: yb - 40, 'class': 'bt-wert l-ir' }, fest(w.U, 0) + NB + 'W/m²');
      if (w.dw > 0) band(150, ya1, 4, w.dw * w.U, 'ir');
      el(szene, 'text', { x: 150 + Math.max(4, w.dw * w.U * k / 2 + 4), y: 40, 'class': 'bt-wert l-ir' }, fest(w.dw * w.U, 0) + NB + 'W/m²');
      // Atmosphäre strahlt nach oben und nach unten (Gegenstrahlung)
      if (w.A > 1){ band(232, ya1, 4, w.A, 'ir atm'); band(262, ya2, yb - 2, w.A, 'ir atm'); }
      el(szene, 'text', { x: 232 - Math.max(6, w.A * k / 2 + 4), y: 70, 'text-anchor': 'end', 'class': 'bt-wert l-ir' }, fest(w.A, 0) + NB + 'W/m²');
      el(szene, 'text', { x: 262 - Math.max(6, w.A * k / 2 + 3), y: ya2 + 40, 'text-anchor': 'end', 'class': 'bt-wert l-ir' }, fest(w.A, 0) + NB + 'W/m²');
      el(szene, 'text', { x: 262 - Math.max(6, w.A * k / 2 + 3), y: ya2 + 52, 'text-anchor': 'end', 'class': 'bt-klein' }, 'Gegenstrahlung');
      el(szene, 'text', { x: 150, y: yb + 14, 'text-anchor': 'middle', 'class': 'bt-meldung boden-text' }, 'Boden: ' + fest(w.T, 1) + NB + 'K = ' + grad(w.th));
      var s = '<span>Boden: ' + v_('U') + ' = ' + v_('S') + ' · (1 + ' + v_('D') + '<sub>L</sub>) / (1 + ' + v_('D') + '<sub>W</sub>) = 240' + NB + 'W/m² · (1 + ' + fest(w.dl, 2) + ') / (1 + ' + fest(w.dw, 2) + ') ' + ist(w.U, sig(w.U)) + sig(w.U) + NB + 'W/m²</span>';
      s += '<span>' + v_('T') + ' = (' + v_('U') + ' / ' + v_('σ') + ')<sup>1/4</sup> = (' + sig(w.U) + NB + 'W/m² / 5.67·10⁻⁸' + NB + 'W/(m²·K⁴))<sup>1/4</sup> ≈ ' + fest(w.T, 1) + NB + 'K = ' + grad(w.th) + '</span>';
      s += '<span class="sim-notiz">' + v_('D') + '<sub>L</sub>: Anteil des Lichts, der bis zum Boden durchkommt; ' + v_('D') + '<sub>W</sub>: Anteil der Wärmestrahlung des Bodens, der direkt ins All gelangt. Einschichtmodell: Was die Atmosphäre aufnimmt, strahlt sie je zur Hälfte nach oben und nach unten ab; ohne Wolken, Wind und Verdunstung. Breite der Pfeile nach der Leistung je m².</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Stelle beide Durchlässigkeiten auf \\(100\\;\\%\\) — als gäbe es keine Atmosphäre. Welche Bodentemperatur stellt sich ein? Notiere, dann vergleiche.', ok: function(s){ return gl(s.dl, 1) && gl(s.dw, 1); },
        vergleich: 'Rund \\(255\\;\\text{K} \\approx -18\\;^\\circ\\text{C}\\): Der Boden muss die \\(240\\;\\text{W/m}^2\\) selbst abstrahlen, \\(\\sigma \\cdot T^4 = 240\\;\\text{W/m}^2\\). So kalt wäre die Erde ohne Treibhauseffekt.' },
      { text: 'Lass das Licht ganz durch. Wie viel Prozent der Wärmestrahlung darf die Modell-Atmosphäre durchlassen, damit der Boden \\(15\\;^\\circ\\text{C}\\) erreicht (auf \\(1\\;^\\circ\\text{C}\\) genau)? Notiere den Wert.', ok: function(s){ return gl(s.dl, 1) && Math.abs(s.th - 15) <= 0.8; },
        vergleich: 'Rund \\(23\\;\\%\\) (\\(22\\;\\%\\) bis \\(24\\;\\%\\) liegen innerhalb von \\(1\\;^\\circ\\text{C}\\)). Der Boden strahlt dann rund \\(390\\;\\text{W/m}^2\\) ab — \\(150\\;\\text{W/m}^2\\) mehr, als die Sonne liefert; im Einschichtmodell bekommt er den Rest als Gegenstrahlung zurück. Wirklich ist die Gegenstrahlung grösser, rund \\(340\\;\\text{W/m}^2\\): Die Atmosphäre nimmt auch Sonnenlicht auf, und der Boden verliert zusätzlich Wärme durch Verdunstung und aufsteigende Luft.' },
      { text: 'Stelle beide Durchlässigkeiten gleich ein, zum Beispiel je \\(60\\;\\%\\). Wie warm wird der Boden? Was folgt daraus für den Treibhauseffekt?', ok: function(s){ return gl(s.dl, s.dw) && s.dl < 1; },
        vergleich: 'Wieder rund \\(-18\\;^\\circ\\text{C}\\), wie ohne Atmosphäre. Wärmer wird es nur, wenn die Atmosphäre das Licht leichter durchlässt als die Wärmestrahlung — der Unterschied der Durchlässigkeiten macht den Treibhauseffekt.' },
      { text: 'Mehr Treibhausgas seit der Industrialisierung (Kohlendioxid von \\(280\\) auf \\(430\\;\\text{ppm}\\)): Im Einschichtmodell entspricht das etwa einer Abnahme der Wärmestrahlung, die direkt hinausgeht, von \\(25\\;\\%\\) auf \\(23\\;\\%\\) (Licht \\(100\\;\\%\\)). Stelle beides ein. Um wie viel wird es wärmer? Warum?', ok: function(s){ return gl(s.dl, 1) && gl(s.dw, 0.23); },
        setup: function(sim){ var z = sim.zustand(); if (gl(z.dl, 1) && gl(z.dw, 0.23)) sim.setze({ dw: 25 }); },
        vergleich: 'Von rund \\(13.7\\;^\\circ\\text{C}\\) auf rund \\(14.9\\;^\\circ\\text{C}\\), also rund \\(1.2\\;\\text{K}\\) — etwa so viel hat sich die Erde seit der Industrialisierung tatsächlich erwärmt. Die Atmosphäre hält mehr Wärmestrahlung zurück und strahlt mehr zum Boden zurück; der Boden erwärmt sich, bis er wieder so viel abgibt, wie hereinkommt.' },
      { text: 'Kehre es um: Licht \\(40\\;\\%\\), Wärmestrahlung \\(100\\;\\%\\). Was geschieht mit der Bodentemperatur? Wann könnte die Atmosphäre so wirken?', ok: function(s){ return gl(s.dl, 0.4) && gl(s.dw, 1); },
        vergleich: 'Der Boden kühlt auf rund \\(-40\\;^\\circ\\text{C}\\) ab: Die Atmosphäre hält das Licht oben fest und lässt die Wärmestrahlung des Bodens frei hinaus. So ähnlich wirkt eine dichte Russ- oder Rauchschicht, die Sonnenlicht schluckt, etwa über grossen Waldbränden.' }
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
    function tz(x){ var s = String(+(+x).toPrecision(6)); if (/e/.test(s)){ var p = s.split('e'); return p[0] + ' \\cdot 10^{' + (+p[1]) + '}'; } return s.replace(/^-/, '-'); }
    function ein(x, u){ return tz(x) + '\\;\\text{' + u + '}'; }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/−/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)(e[-+]?\d+)?$/i.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    // Ergebnis mit «=» oder «≈», drei signifikante Stellen
    function erg(x, u){ var r = +(+x).toPrecision(3); return (Math.abs(r - x) < 1e-9 * Math.max(1, Math.abs(x)) ? '= ' : '\\approx ') + ein(r, u); }
    function gr(x){ return tz(x) + '\\;^\\circ\\text{C}'; }
    function grE(x){ var r = +(+x).toPrecision(3); return (Math.abs(r - x) < 1e-9 * Math.max(1, Math.abs(x)) ? '= ' : '\\approx ') + gr(r); }
    var JKK = '\\;\\text{J/(kg·K)}';
    // Feste Beispiele (Clips, Kontrollfragen, Leisten, Festhalten, Kapitelaufgaben, Gesamttest, Themenseite)
    // treffen die Zufallsübungen nicht: Die Wertelisten der Generatoren enthalten keinen ihrer Werte
    // (geprüft mit scripts/lp/waerme/pruef_fest.py; «abstrahlung» hat nur eine Zahl und ist von Hand geprüft:
    // keine der festen Temperaturen 15, 18 und 30 °C im Pool). Darum hier keine Ausschlussliste.
    function ergR(x, u){ var r = +(+x).toPrecision(3); return (Math.abs(r - x) < 1e-9 * Math.max(1, Math.abs(x)) ? '= ' : '\\approx ') + tz(r) + '\\;' + u; }
    // Fehlermuster müssen verschiedene Zahlen ergeben (HOWTO §15): alle Werte paarweise 2 % auseinander
    function verschieden(l){ for (var i = 0; i < l.length; i++) for (var j = i + 1; j < l.length; j++) if (Math.abs(l[i] - l[j]) <= 0.02 * Math.max(Math.abs(l[i]), Math.abs(l[j]))) return false; return true; }
    var C = { 'Wasser': 4182, 'Ethanol': 2430, 'Speiseöl': 2000, 'Aluminium': 896, 'Sand': 835, 'Eisen': 450 };
    var STOFFE = ['Wasser', 'Ethanol', 'Speiseöl', 'Aluminium', 'Sand', 'Eisen'];

    function eisTol(t){ return Math.max(0.15, 0.012 * Math.abs(t)); }   // Übung «eiswuerfel»: Toleranz in K
    var TYPEN = {
      /* ----- Kapitel 1: Wärme und Temperatur ----- */
      'waermemenge': { felder: ['Q'], muster: '<i>Q</i> = {Q} kJ',
        neu: function(){
          var o, m, t1, t2, Q, l;
          do {
            o = zufall([['Wasser im Kochtopf', 'Wasser', [0.75, 1.2, 2.5, 3.5], [45, 60, 75, 90], 'es'], ['Ein Aluminiumtopf', 'Aluminium', [0.4, 0.65, 1.1], [80, 150, 220], 'er'],
                        ['Eine Eisenpfanne', 'Eisen', [0.9, 1.4, 2.2], [80, 150, 220], 'sie'], ['Ethanol in einer Flasche', 'Ethanol', [0.25, 0.4, 0.75], [35, 50, 65], 'es'],
                        ['Speiseöl in der Fritteuse', 'Speiseöl', [1.2, 2.5, 3.5], [120, 160, 175], 'es'], ['Sand im Sandkasten', 'Sand', [25, 40, 60], [35, 45, 55], 'er']]);
            m = zufall(o[2]); t1 = zufall([12, 15, 18, 22]); t2 = zufall(o[3]);
            Q = m * C[o[1]] * (t2 - t1);
            l = [Q, m * C[o[1]] * t2, Q * 1000];
            if (o[1] !== 'Wasser') l.push(m * 4182 * (t2 - t1));
          } while (!verschieden(l));
          return { Q: Q / 1000, m: m, s: o[1], c: C[o[1]], t1: t1, t2: t2,
            text: o[0] + ' (\\(' + ein(m, 'kg') + '\\), ' + o[1] + ', \\(c = ' + tz(C[o[1]]) + JKK + '\\)) wird von \\(' + gr(t1) + '\\) auf \\(' + gr(t2) + '\\) erwärmt. Wie viel Wärme nimmt ' + o[4] + ' auf?' }; },
        pruefen: function(A, e){
          if (nah(e.Q, A.Q)) return null;
          if (nah(e.Q, A.Q * 1000)) return 'Das ist die Wärme in Joule. Gefragt sind Kilojoule: \\(1\\;\\text{kJ} = 1000\\;\\text{J}\\).';
          if (nah(e.Q, A.m * A.c * A.t2 / 1000)) return 'In die Formel gehört die Temperaturänderung \\(\\Delta T = \\vartheta_2 - \\vartheta_1\\), nicht die Endtemperatur.';
          if (A.s !== 'Wasser' && nah(e.Q, A.m * 4182 * (A.t2 - A.t1) / 1000)) return 'Das ist der Wert von Wasser. Jeder Stoff hat seine eigene spezifische Wärmekapazität — nimm die von ' + A.s + '.';
          return '\\(Q = m \\cdot c \\cdot \\Delta T\\) mit \\(\\Delta T = \\vartheta_2 - \\vartheta_1\\), Ergebnis in kJ.'; },
        fehler: function(A){ var l = [[{ Q: String(A.Q * 1000) }, 'Joule'], [{ Q: String(A.m * A.c * A.t2 / 1000) }, 'Temperaturänderung']]; if (A.s !== 'Wasser') l.push([{ Q: String(A.m * 4182 * (A.t2 - A.t1) / 1000) }, 'Stoff']); return l; },
        loesung: function(A){ return 'Q = m \\cdot c \\cdot \\Delta T = ' + ein(A.m, 'kg') + ' \\cdot ' + tz(A.c) + JKK + ' \\cdot ' + ein(A.t2 - A.t1, 'K') + ' ' + erg(A.Q * 1000, 'J') + ' ' + erg(A.Q, 'kJ'); } },
      'erwaermung': { felder: ['t'], muster: '<i>ϑ</i><sub>2</sub> = {t} °C',
        neu: function(){
          var o, m, t1, dT, Q, l;
          do {
            o = zufall([['Das Wasser in einem Wasserkocher', 'Wasser', [0.6, 1.4, 1.7], [30, 45, 60], 'es'], ['Ein Aluminiumblock', 'Aluminium', [0.3, 0.7, 1.5], [40, 70, 110], 'er'],
                        ['Ein Eisengewicht', 'Eisen', [0.5, 1.2, 2.5], [40, 70, 110], 'es'], ['Eine Flasche Speiseöl', 'Speiseöl', [0.7, 0.9, 1.6], [25, 40, 60], 'das Öl']]);
            m = zufall(o[2]); t1 = zufall([8, 14, 19, 23]); dT = zufall(o[3]);
            Q = Math.round(m * C[o[1]] * dT / 500) / 2;                // auf 0.5 kJ gerundet
            var d = Q * 1000 / (m * C[o[1]]);
            l = [t1 + d, d, t1 + d * m, t1 + d / 1000];
          } while (!verschieden(l) || m === 1);
          return { t: t1 + Q * 1000 / (m * C[o[1]]), dT: Q * 1000 / (m * C[o[1]]), Q: Q, m: m, s: o[1], c: C[o[1]], t1: t1,
            text: o[0] + ' (\\(' + ein(m, 'kg') + '\\), ' + o[1] + ', \\(c = ' + tz(C[o[1]]) + JKK + '\\)) hat \\(' + gr(t1) + '\\) und nimmt \\(' + ein(Q, 'kJ') + '\\) Wärme auf. Welche Temperatur hat ' + o[4] + ' danach?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t)) return null;
          if (nah(e.t, A.dT)) return 'Das ist die Temperaturänderung \\(\\Delta T\\). Gefragt ist die Endtemperatur: \\(\\vartheta_2 = \\vartheta_1 + \\Delta T\\).';
          if (nah(e.t, A.t1 + A.dT * A.m)) return '\\(\\Delta T = \\dfrac{Q}{m \\cdot c}\\) — die Masse gehört in den Nenner.';
          if (nah(e.t, A.t1 + A.dT / 1000)) return 'Die Wärme in Joule einsetzen: \\(1\\;\\text{kJ} = 1000\\;\\text{J}\\).';
          return 'Zuerst \\(\\Delta T = \\dfrac{Q}{m \\cdot c}\\), dann \\(\\vartheta_2 = \\vartheta_1 + \\Delta T\\).'; },
        fehler: function(A){ return [[{ t: String(A.dT) }, 'Endtemperatur'], [{ t: String(A.t1 + A.dT * A.m) }, 'Masse'], [{ t: String(A.t1 + A.dT / 1000) }, 'Joule']]; },
        loesung: function(A){ return '\\Delta T = \\dfrac{Q}{m \\cdot c} = \\dfrac{' + ein(A.Q * 1000, 'J') + '}{' + ein(A.m, 'kg') + ' \\cdot ' + tz(A.c) + JKK + '} ' + erg(A.dT, 'K') + ',\\quad \\vartheta_2 = ' + gr(A.t1) + ' + ' + ein(+A.dT.toPrecision(3), 'K') + ' ' + grE(A.t); } },
      'c-messen': { felder: ['c', 's'], muster: '<i>c</i> = {c} J/(kg·K); Stoff: {s:Wasser|Ethanol|Speiseöl|Aluminium|Sand|Eisen}',
        neu: function(){
          var s, m, t1, dT, Q, l;
          do {
            s = zufall(STOFFE); m = zufall([0.2, 0.3, 0.6, 0.8]); t1 = zufall([16, 19, 21]); dT = zufall([15, 25, 35]);
            Q = +((m * C[s] * dT) / 1000).toPrecision(3);
            l = [Q * 1000 / (m * dT), Q / (m * dT), Q * 1000 / (m * (t1 + dT))];
          } while (!verschieden(l));
          return { c: Q * 1000 / (m * dT), s: s, Q: Q, m: m, t1: t1, t2: t1 + dT, dT: dT,
            text: 'Ein Heizstab gibt einer Probe von \\(' + ein(m, 'kg') + '\\) die Wärme \\(' + ein(Q, 'kJ') + '\\) ab. Die Probe wird von \\(' + gr(t1) + '\\) auf \\(' + gr(t1 + dT) + '\\) wärmer. Bestimme ihre spezifische Wärmekapazität und finde den Stoff in der Tabelle.' }; },
        eingabe: function(A){ return { c: String(A.c), s: A.s }; },
        pruefen: function(A, e){
          if (nah(e.c, A.c)) return e.s === A.s ? null : 'Der Wert stimmt. Vergleiche ihn mit der Tabelle im Festhalten: Welcher Stoff hat diesen Wert?';
          if (nah(e.c, A.c / 1000)) return 'Die Wärme in Joule einsetzen, dann kommt \\(c\\) in J/(kg·K).';
          if (nah(e.c, A.Q * 1000 / (A.m * A.t2))) return 'Durch die Temperaturänderung teilen, nicht durch die Endtemperatur.';
          return '\\(c = \\dfrac{Q}{m \\cdot \\Delta T}\\), \\(Q\\) in J.'; },
        fehler: function(A){ var a = A.s === 'Eisen' ? 'Sand' : 'Eisen'; return [[{ c: String(A.c / 1000), s: A.s }, 'Joule'], [{ c: String(A.Q * 1000 / (A.m * A.t2)), s: A.s }, 'Temperaturänderung'], [{ c: String(A.c), s: a }, 'Tabelle']]; },
        loesung: function(A){ return 'c = \\dfrac{Q}{m \\cdot \\Delta T} = \\dfrac{' + ein(A.Q * 1000, 'J') + '}{' + ein(A.m, 'kg') + ' \\cdot ' + ein(A.dT, 'K') + '} ' + erg(A.c, 'J/(kg·K)') + '\\;\\Rightarrow\\;\\text{' + A.s + '}'; } },

      /* ----- Kapitel 2: Wärmebilanz ----- */
      'mischen': { felder: ['t'], muster: '<i>ϑ</i><sub>m</sub> = {t} °C',
        neu: function(){
          var c, m1, t1, m2, t2, tm, l;
          do {
            // je Kontext eigene Massen und Temperaturen (kein «kochendes Wasser von 55 °C»)
            c = zufall([['heisser Tee', 'kaltes Wasser', [0.15, 0.25, 0.4], [70, 80, 90], [0.1, 0.2, 0.35]], ['heisses Wasser aus dem Boiler', 'kaltes Badewasser', [40, 60, 90], [55, 60, 65], [70, 110, 150]],
                        ['kochendes Wasser', 'Leitungswasser', [0.25, 0.5, 1.2], [100], [0.6, 1.5, 2]], ['warmes Wasser', 'kaltes Wasser', [2.5, 4, 7], [40, 45, 50], [3, 5, 9]]]);
            m1 = zufall(c[2]); m2 = zufall(c[4]);
            t1 = zufall(c[3]); t2 = zufall([8, 12, 16]);
            tm = (m1 * t1 + m2 * t2) / (m1 + m2);
            l = [tm, (t1 + t2) / 2, (m2 * t1 + m1 * t2) / (m1 + m2)];
          } while (gl(m1, m2) || !verschieden(l));
          return { t: tm, m1: m1, t1: t1, m2: m2, t2: t2,
            text: '\\(' + ein(m1, 'kg') + '\\) ' + c[0] + ' von \\(' + gr(t1) + '\\) werden mit \\(' + ein(m2, 'kg') + '\\) ' + c[1] + ' von \\(' + gr(t2) + '\\) gemischt (ohne Verluste). Welche Mischtemperatur stellt sich ein?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t)) return null;
          if (nah(e.t, (A.t1 + A.t2) / 2)) return 'Das ist der einfache Mittelwert. Er gilt nur für gleiche Massen — hier zieht die grössere Masse die Temperatur zu sich.';
          if (nah(e.t, (A.m2 * A.t1 + A.m1 * A.t2) / (A.m1 + A.m2))) return 'Die Massen sind vertauscht: Jede Temperatur wird mit der Masse ihrer eigenen Portion gewichtet.';
          return 'Bilanz \\(Q_\\text{ab} = Q_\\text{auf}\\); bei gleichem Stoff kürzt sich \\(c\\): \\(\\vartheta_\\text{m} = \\dfrac{m_1 \\cdot \\vartheta_1 + m_2 \\cdot \\vartheta_2}{m_1 + m_2}\\).'; },
        fehler: function(A){ return [[{ t: String((A.t1 + A.t2) / 2) }, 'Mittelwert'], [{ t: String((A.m2 * A.t1 + A.m1 * A.t2) / (A.m1 + A.m2)) }, 'vertauscht']]; },
        loesung: function(A){ return '\\vartheta_\\text{m} = \\dfrac{m_1 \\cdot \\vartheta_1 + m_2 \\cdot \\vartheta_2}{m_1 + m_2} = \\dfrac{' + ein(A.m1, 'kg') + ' \\cdot ' + gr(A.t1) + ' + ' + ein(A.m2, 'kg') + ' \\cdot ' + gr(A.t2) + '}{' + ein(A.m1 + A.m2, 'kg') + '} ' + grE(A.t); } },
      'abschrecken': { felder: ['t'], muster: '<i>ϑ</i><sub>m</sub> = {t} °C',
        neu: function(){
          var s, mk, tk, mw, tw, tm, l;
          do {
            s = zufall(['Aluminium', 'Eisen']); mk = zufall([0.15, 0.3, 0.6, 0.9, 1.2]); tk = zufall([120, 180, 250, 320]);
            mw = zufall([0.6, 1.0, 1.8, 2.5]); tw = zufall([12, 16, 21]);
            tm = (mk * C[s] * tk + mw * 4182 * tw) / (mk * C[s] + mw * 4182);
            l = [tm, (mk * tk + mw * tw) / (mk + mw), (tk + tw) / 2, (mk * 4182 * tk + mw * C[s] * tw) / (mk * 4182 + mw * C[s])];
          } while (!verschieden(l) || tm >= 90);                  // nichts verdampft: Mischung deutlich unter 100 °C
          return { t: tm, s: s, c: C[s], mk: mk, tk: tk, mw: mw, tw: tw,
            text: 'Ein Werkstück aus ' + s + ' (\\(' + ein(mk, 'kg') + '\\), \\(c = ' + tz(C[s]) + JKK + '\\)) von \\(' + gr(tk) + '\\) wird in \\(' + ein(mw, 'kg') + '\\) Wasser von \\(' + gr(tw) + '\\) abgeschreckt. Welche Temperatur stellt sich ein (Gefäss und Umgebung nehmen nichts auf, nichts verdampft)?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t)) return null;
          if (nah(e.t, (A.mk * A.tk + A.mw * A.tw) / (A.mk + A.mw))) return 'Verschiedene Stoffe: Die spezifische Wärmekapazität kürzt sich nicht. Gewichtet wird mit \\(m \\cdot c\\).';
          if (nah(e.t, (A.tk + A.tw) / 2)) return 'Das ist der einfache Mittelwert. Gewichtet wird mit \\(m \\cdot c\\) jeder Portion.';
          if (nah(e.t, (A.mk * 4182 * A.tk + A.mw * A.c * A.tw) / (A.mk * 4182 + A.mw * A.c))) return 'Die Werte von \\(c\\) sind vertauscht: Wasser hat \\(4182\\;\\text{J/(kg·K)}\\).';
          return 'Bilanz \\(m_K \\cdot c_K \\cdot (\\vartheta_K - \\vartheta_\\text{m}) = m_W \\cdot c_W \\cdot (\\vartheta_\\text{m} - \\vartheta_W)\\), nach \\(\\vartheta_\\text{m}\\) auflösen.'; },
        fehler: function(A){ return [[{ t: String((A.mk * A.tk + A.mw * A.tw) / (A.mk + A.mw)) }, 'Wärmekapazität'], [{ t: String((A.tk + A.tw) / 2) }, 'Mittelwert'], [{ t: String((A.mk * 4182 * A.tk + A.mw * A.c * A.tw) / (A.mk * 4182 + A.mw * A.c)) }, 'vertauscht']]; },
        loesung: function(A){ return '\\vartheta_\\text{m} = \\dfrac{m_K c_K \\vartheta_K + m_W c_W \\vartheta_W}{m_K c_K + m_W c_W} = \\dfrac{' + ein(A.mk, 'kg') + ' \\cdot ' + tz(A.c) + JKK + ' \\cdot ' + gr(A.tk) + ' + ' + ein(A.mw, 'kg') + ' \\cdot 4182' + JKK + ' \\cdot ' + gr(A.tw) + '}{' + ein(A.mk, 'kg') + ' \\cdot ' + tz(A.c) + JKK + ' + ' + ein(A.mw, 'kg') + ' \\cdot 4182' + JKK + '} ' + grE(A.t); } },
      'mischen-rueck': { felder: ['x'], muster: function(A){ return A.art === 'm' ? '<i>m</i><sub>heiss</sub> = {x} kg' : '<i>ϑ</i><sub>heiss</sub> = {x} °C'; },
        neu: function(){
          var art, mk, tk, tm, mh, th, x, falsch, l;
          do {
            art = zufall(['m', 't']); mk = zufall([0.4, 0.9, 1.5, 6, 25]); tk = zufall([10, 14, 18]); tm = zufall([32, 37, 42]);
            if (art === 'm'){ th = zufall([60, 75, 90]); x = mk * (tm - tk) / (th - tm); falsch = mk * (th - tm) / (tm - tk); }
            else { mh = zufall([0.3, 0.8, 2.5, 8]); x = tm + mk * (tm - tk) / mh; falsch = tm + mh * (tm - tk) / mk; th = x; }
            l = [x, falsch];
          } while (!verschieden(l) || (art === 't' && (x > 98 || x < 45)));
          var kalt = '\\(' + ein(mk, 'kg') + '\\) Wasser von \\(' + gr(tk) + '\\)';
          return { x: x, art: art, mk: mk, tk: tk, tm: tm, mh: mh, th: th, falsch: falsch,
            text: art === 'm' ? 'Wie viel Wasser von \\(' + gr(th) + '\\) musst du zu ' + kalt + ' giessen, damit die Mischung \\(' + gr(tm) + '\\) hat (ohne Verluste)?'
                              : 'Zu ' + kalt + ' kommen \\(' + ein(mh, 'kg') + '\\) heisses Wasser. Die Mischung soll \\(' + gr(tm) + '\\) haben. Wie heiss muss das heisse Wasser sein?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.falsch)) return A.art === 'm' ? 'Umgekehrt: Das heisse Wasser kühlt um \\(\\vartheta_\\text{heiss} - \\vartheta_\\text{m}\\) ab, das kalte wird um \\(\\vartheta_\\text{m} - \\vartheta_\\text{kalt}\\) wärmer — die Massen sind vertauscht.' : 'Die Massen sind vertauscht: Die kleine heisse Portion muss stark abkühlen, um die grosse zu erwärmen.';
          return 'Bilanz \\(m_\\text{heiss} \\cdot c \\cdot (\\vartheta_\\text{heiss} - \\vartheta_\\text{m}) = m_\\text{kalt} \\cdot c \\cdot (\\vartheta_\\text{m} - \\vartheta_\\text{kalt})\\); \\(c\\) kürzt sich, dann nach der gesuchten Grösse auflösen.'; },
        fehler: function(A){ return [[{ x: String(A.falsch) }, 'vertauscht']]; },
        loesung: function(A){
          if (A.art === 'm') return 'm_\\text{heiss} = m_\\text{kalt} \\cdot \\dfrac{\\vartheta_\\text{m} - \\vartheta_\\text{kalt}}{\\vartheta_\\text{heiss} - \\vartheta_\\text{m}} = ' + ein(A.mk, 'kg') + ' \\cdot \\dfrac{' + ein(A.tm - A.tk, 'K') + '}{' + ein(A.th - A.tm, 'K') + '} ' + erg(A.x, 'kg');
          return '\\vartheta_\\text{heiss} = \\vartheta_\\text{m} + \\dfrac{m_\\text{kalt} \\cdot (\\vartheta_\\text{m} - \\vartheta_\\text{kalt})}{m_\\text{heiss}} = ' + gr(A.tm) + ' + \\dfrac{' + ein(A.mk, 'kg') + ' \\cdot ' + ein(A.tm - A.tk, 'K') + '}{' + ein(A.mh, 'kg') + '} ' + grE(A.x); } },

      /* ----- Kapitel 3: Latente Wärme und Heizkurve ----- */
      'latent': { felder: ['Q', 'r'], muster: '<i>Q</i> = {Q} kJ; wird {r:aufgenommen|abgegeben}',
        neu: function(){
          var v = zufall([['schmelzen', 'Eis von \\(0\\;^\\circ\\text{C}\\) schmilzt vollständig', 334, 'aufgenommen'], ['erstarren', 'Wasser von \\(0\\;^\\circ\\text{C}\\) gefriert vollständig', 334, 'abgegeben'],
                            ['verdampfen', 'Wasser von \\(100\\;^\\circ\\text{C}\\) verdampft vollständig', 2256, 'aufgenommen'], ['kondensieren', 'Wasserdampf von \\(100\\;^\\circ\\text{C}\\) kondensiert vollständig', 2256, 'abgegeben']]),
              m = zufall([0.12, 0.25, 0.4, 0.75, 1.5]);
          return { Q: m * v[2], r: v[3], m: m, L: v[2], v: v[0], text: '\\(' + ein(m, 'kg') + '\\) ' + v[1] + '. Wie viel Wärme wird dabei umgesetzt, und wird sie aufgenommen oder abgegeben?' }; },
        eingabe: function(A){ return { Q: String(A.Q), r: A.r }; },
        pruefen: function(A, e){
          var anderes = A.L === 334 ? 2256 : 334;
          if (e.Q < 0) e = { Q: -e.Q, r: e.r };                  // Q < 0 heisst abgegeben: der Betrag zählt, die Richtung steht im Auswahlfeld
          if (nah(e.Q, A.Q)) return e.r === A.r ? null : 'Der Betrag stimmt. Zur Richtung: Beim Schmelzen und Verdampfen wird der Teilchenverband gelöst — das kostet Energie; beim Erstarren und Kondensieren wird dieselbe Energie wieder frei.';
          if (nah(e.Q, A.m * anderes)) return A.L === 334 ? 'Das ist die Verdampfungswärme. Hier geht es um den Übergang fest ↔ flüssig: Schmelzwärme \\(L_\\text{f} = 334\\;\\text{kJ/kg}\\).' : 'Das ist die Schmelzwärme. Hier geht es um den Übergang flüssig ↔ gasförmig: Verdampfungswärme \\(L_\\text{v} = 2256\\;\\text{kJ/kg}\\).';
          if (nah(e.Q, A.Q * 1000)) return 'Das ist Joule. Gefragt sind Kilojoule.';
          return '\\(Q = m \\cdot L\\) — ohne Temperaturänderung, mit dem passenden \\(L\\).'; },
        fehler: function(A){ var anderes = A.L === 334 ? 2256 : 334, gegen = A.r === 'aufgenommen' ? 'abgegeben' : 'aufgenommen';
          return [[{ Q: String(A.m * anderes), r: A.r }, A.L === 334 ? 'Schmelzwärme' : 'Verdampfungswärme'], [{ Q: String(A.Q), r: gegen }, 'Richtung'], [{ Q: String(A.Q * 1000), r: A.r }, 'Joule']]; },
        loesung: function(A){ return 'Q = m \\cdot L_\\text{' + (A.L === 334 ? 'f' : 'v') + '} = ' + ein(A.m, 'kg') + ' \\cdot ' + ein(A.L, 'kJ/kg') + ' ' + erg(A.Q, 'kJ') + '\\;(\\text{' + A.r + '})'; } },
      'eiswuerfel': { felder: ['t'], muster: '<i>ϑ</i><sub>m</sub> = {t} °C',
        neu: function(){
          // Getränk (Stoffwerte wie Wasser) und Eis von 0 °C. Reicht die Wärme des Getränks bis 0 °C nicht
          // fürs Schmelzen, bleibt Eis übrig, und die Mischung hat 0 °C.
          var g, mg, tg, me, qmax, qs, tm, l;
          do {
            g = zufall(['Eistee', 'Limonade', 'Mineralwasser', 'Orangensaft']);
            mg = zufall([0.2, 0.25, 0.35, 0.45, 0.5]); tg = zufall([18, 21, 26, 30]); me = zufall([0.02, 0.03, 0.045, 0.06, 0.08, 0.12, 0.15]);
            qmax = mg * 4182 * tg; qs = me * 334000;
            tm = qmax >= qs ? (qmax - qs) / ((mg + me) * 4182) : 0;
            l = [mg * tg / (mg + me), (qmax - qs) / (mg * 4182), (qmax - qs) / ((mg + me) * 4182)];
          } while (!verschieden(l) || (tm > 0 && tm < 1) || Math.abs(qmax - qs) < 0.08 * qs
                   || l.some(function(v){ return v !== tm && Math.abs(v - tm) <= 2.5 * eisTol(tm); }));   // Fehlerwerte ausserhalb der Rundungstoleranz
          return { t: tm, g: g, mg: mg, tg: tg, me: me, qmax: qmax, qs: qs, ganz: qmax >= qs,
            text: 'In \\(' + ein(mg, 'kg') + '\\) ' + g + ' von \\(' + gr(tg) + '\\) (Stoffwerte wie Wasser) kommen \\(' + ein(me, 'kg') + '\\) Eis von \\(0\\;^\\circ\\text{C}\\). Welche Temperatur hat das Getränk am Ende? Verluste vernachlässigt; \\(L_\\text{f} = 334\\;\\text{kJ/kg}\\), \\(c_\\text{W} = 4182' + JKK + '\\).' }; },
        pruefen: function(A, e){
          // Temperatur: auf 0.1 °C gerundet oder mit dreistelligen Zwischenwerten gerechnet zählt (eisTol)
          if (Math.abs(e.t - A.t) <= eisTol(A.t)) return null;
          var roh = (A.qmax - A.qs) / ((A.mg + A.me) * 4182);
          if (!A.ganz && (nah(e.t, roh) || nah(e.t, (A.qmax - A.qs) / (A.mg * 4182)))) return 'Unter \\(0\\;^\\circ\\text{C}\\) kann das Getränk nicht kommen. Prüfe zuerst, ob die Wärme des Getränks bis \\(0\\;^\\circ\\text{C}\\) überhaupt reicht, um alles Eis zu schmelzen.';
          if (nah(e.t, A.mg * A.tg / (A.mg + A.me))) return 'Das Schmelzen fehlt: Bevor das Schmelzwasser wärmer wird, braucht das Eis \\(m \\cdot L_\\text{f}\\) — ohne dass seine Temperatur steigt.';
          if (A.ganz && nah(e.t, (A.qmax - A.qs) / (A.mg * 4182))) return 'Das Schmelzwasser muss auch erwärmt werden: Auf der Seite der aufgenommenen Wärme steht zusätzlich \\(m_\\text{Eis} \\cdot c \\cdot (\\vartheta_\\text{m} - 0\\;^\\circ\\text{C})\\).';
          return 'Erst prüfen, ob alles Eis schmilzt. Dann \\(Q_\\text{ab} = Q_\\text{auf}\\): \\(m_\\text{G} \\cdot c \\cdot (\\vartheta_\\text{G} - \\vartheta_\\text{m}) = m_\\text{Eis} \\cdot L_\\text{f} + m_\\text{Eis} \\cdot c \\cdot \\vartheta_\\text{m}\\).'; },
        fehler: function(A){
          var l = [[{ t: String(A.mg * A.tg / (A.mg + A.me)) }, 'Schmelzen fehlt']];
          if (A.ganz) l.push([{ t: String((A.qmax - A.qs) / (A.mg * 4182)) }, 'Schmelzwasser']);
          else l.push([{ t: String((A.qmax - A.qs) / ((A.mg + A.me) * 4182)) }, 'alles Eis']);
          return l; },
        loesung: function(A){
          var kopf = 'Q_\\text{bis 0 °C} = ' + ein(A.mg, 'kg') + ' \\cdot 4182' + JKK + ' \\cdot ' + ein(A.tg, 'K') + ' ' + erg(A.qmax, 'J') + ',\\quad Q_\\text{schmelz} = ' + ein(A.me, 'kg') + ' \\cdot 334\\,000\\;\\text{J/kg} ' + erg(A.qs, 'J');
          if (!A.ganz) return kopf + '.\\;\\text{ Das reicht nicht: Es bleiben }' + ein(+((A.qs - A.qmax) / 334000).toPrecision(2), 'kg') + '\\text{ Eis, }\\vartheta_\\text{m} = 0\\;^\\circ\\text{C}';
          return kopf + '.\\;\\vartheta_\\text{m} = \\dfrac{Q_\\text{bis 0 °C} - Q_\\text{schmelz}}{(m_\\text{G} + m_\\text{Eis}) \\cdot c} = \\dfrac{' + ein(+(A.qmax - A.qs).toPrecision(4), 'J') + '}{' + ein(+(A.mg + A.me).toPrecision(4), 'kg') + ' \\cdot 4182' + JKK + '} ' + grE(A.t); } },
      'abschnitte': { felder: ['Q'], muster: '<i>Q</i> = {Q} kJ',
        neu: function(){
          var m, x, t, q1, q2, q3, l;
          do {
            m = zufall([0.15, 0.3, 0.45, 0.8, 1.2]); x = zufall([5, 8, 12, 18, 25]); t = zufall([10, 15, 25, 35, 50]);
            q1 = m * 2100 * x; q2 = m * 334000; q3 = m * 4182 * t;
            l = [q1 + q2 + q3, q1 + q3, m * 4182 * x + q2 + q3, q2 + q3, m * 4182 * (t + x)];
          } while (!verschieden(l));
          return { Q: (q1 + q2 + q3) / 1000, m: m, x: x, t: t, q1: q1, q2: q2, q3: q3,
            text: '\\(' + ein(m, 'kg') + '\\) Eis von \\(' + gr(-x).replace('-', '−') + '\\) sollen zu Wasser von \\(' + gr(t) + '\\) werden. Wie viel Wärme braucht es insgesamt? (\\(c_\\text{Eis} = 2100' + JKK + '\\), \\(c_\\text{W} = 4182' + JKK + '\\), \\(L_\\text{f} = 334\\;\\text{kJ/kg}\\))' }; },
        pruefen: function(A, e){
          if (nah(e.Q, A.Q)) return null;
          if (nah(e.Q, (A.q1 + A.q3) / 1000)) return 'Das Schmelzen fehlt: Bei \\(0\\;^\\circ\\text{C}\\) braucht es zusätzlich \\(m \\cdot L_\\text{f}\\), ohne dass die Temperatur steigt.';
          if (nah(e.Q, (A.m * 4182 * A.x + A.q2 + A.q3) / 1000)) return 'Für das Erwärmen des Eises gilt \\(c_\\text{Eis} = 2100' + JKK + '\\), nicht der Wert von flüssigem Wasser.';
          if (nah(e.Q, (A.q2 + A.q3) / 1000)) return 'Das Eis muss zuerst auf \\(0\\;^\\circ\\text{C}\\) erwärmt werden — dieser erste Abschnitt fehlt.';
          if (nah(e.Q, A.m * 4182 * (A.t + A.x) / 1000)) return 'Über eine Phasengrenze hinweg gilt keine einzige Formel: drei Abschnitte, einzeln rechnen, am Schluss addieren.';
          return 'Drei Abschnitte: Eis erwärmen (\\(m \\cdot c_\\text{Eis} \\cdot \\Delta T\\)), schmelzen (\\(m \\cdot L_\\text{f}\\)), Wasser erwärmen (\\(m \\cdot c_\\text{W} \\cdot \\Delta T\\)).'; },
        fehler: function(A){ return [[{ Q: String((A.q1 + A.q3) / 1000) }, 'Schmelzen'], [{ Q: String((A.m * 4182 * A.x + A.q2 + A.q3) / 1000) }, 'Eises'], [{ Q: String((A.q2 + A.q3) / 1000) }, 'Abschnitt'], [{ Q: String(A.m * 4182 * (A.t + A.x) / 1000) }, 'Abschnitte']]; },
        loesung: function(A){ return 'Q = m \\cdot c_\\text{Eis} \\cdot ' + ein(A.x, 'K') + ' + m \\cdot L_\\text{f} + m \\cdot c_\\text{W} \\cdot ' + ein(A.t, 'K') + ' = ' + ein(+(A.q1 / 1000).toPrecision(4), 'kJ') + ' + ' + ein(+(A.q2 / 1000).toPrecision(4), 'kJ') + ' + ' + ein(+(A.q3 / 1000).toPrecision(4), 'kJ') + ' ' + erg(A.Q, 'kJ'); } },
      'plateau': { felder: ['t'], muster: '<i>t</i> = {t} min',
        neu: function(){
          var v = zufall([['schmelzen', 'Eis von \\(0\\;^\\circ\\text{C}\\) liegt auf einer Platte', 'Wie lange dauert es, bis alles geschmolzen ist?', 334000], ['verdampfen', 'Wasser von \\(100\\;^\\circ\\text{C}\\) siedet auf einer Platte', 'Wie lange dauert es, bis alles verdampft ist?', 2256000]]),
              m = zufall([0.2, 0.35, 0.6, 0.9]), P = zufall([400, 650, 800, 1500, 2000]);
          return { t: m * v[3] / P / 60, m: m, P: P, L: v[3], v: v[0], text: '\\(' + ein(m, 'kg') + '\\) ' + v[1] + ', die dem Inhalt \\(' + ein(P, 'W') + '\\) zuführt. ' + v[2] }; },
        pruefen: function(A, e){
          var anderes = A.L === 334000 ? 2256000 : 334000;
          if (nah(e.t, A.t)) return null;
          if (nah(e.t, A.t * 60)) return 'Das sind Sekunden. Gefragt sind Minuten: durch 60 teilen.';
          if (nah(e.t, A.m * anderes / A.P / 60) || nah(e.t, A.m * anderes / A.P)) return A.L === 334000 ? 'Beim Schmelzen gilt die Schmelzwärme \\(L_\\text{f} = 334\\;\\text{kJ/kg}\\).' : 'Beim Verdampfen gilt die Verdampfungswärme \\(L_\\text{v} = 2256\\;\\text{kJ/kg}\\).';
          if (nah(e.t, A.t / 1000) || nah(e.t, A.t * 60 / 1000)) return 'Die latente Wärme in Joule je Kilogramm einsetzen: \\(1\\;\\text{kJ} = 1000\\;\\text{J}\\).';
          return 'Erst \\(Q = m \\cdot L\\), dann \\(t = \\dfrac{Q}{P}\\) in Sekunden, dann in Minuten.'; },
        fehler: function(A){ var anderes = A.L === 334000 ? 2256000 : 334000; return [[{ t: String(A.t * 60) }, 'Minuten'], [{ t: String(A.m * anderes / A.P / 60) }, A.L === 334000 ? 'Schmelzwärme' : 'Verdampfungswärme'], [{ t: String(A.t / 1000) }, 'Joule']]; },
        loesung: function(A){ return 't = \\dfrac{m \\cdot L}{P} = \\dfrac{' + ein(A.m, 'kg') + ' \\cdot ' + ein(A.L, 'J/kg') + '}{' + ein(A.P, 'W') + '} ' + erg(A.t * 60, 's') + ' ' + erg(A.t, 'min'); } },

      /* ----- Kapitel 4: Heizwert und Wirkungsgrad ----- */
      'heizwert': { felder: ['Q'], muster: function(A){ return '<i>Q</i><sub>nutz</sub> = {Q} ' + A.u; },
        neu: function(){
          var f, m, eta, u, Qn, l;
          do {
            f = zufall([['Heizöl', 42.6, 'ein Ölkessel', [0.7, 2.5, 6], [0.86, 0.9, 0.93]], ['Erdgas', 50.0, 'ein Gaskessel', [0.6, 1.8, 4], [0.88, 0.92, 0.95]], ['Propan', 46.4, 'ein Campingkocher', [0.25, 0.45], [0.4, 0.45, 0.5]],
                        ['Holzpellets', 17.0, 'ein Pelletofen', [3, 8, 15], [0.78, 0.85, 0.9]], ['Buchenholz', 15.0, 'ein Kachelofen', [4.5, 7, 12], [0.65, 0.72, 0.8]]]);
            m = zufall(f[3]); eta = zufall(f[4]);
            u = zufall(['MJ', 'kWh']);
            Qn = eta * m * f[1] / (u === 'kWh' ? 3.6 : 1);
            l = [Qn, Qn / eta, Qn / (eta * eta), u === 'MJ' ? Qn / 3.6 : Qn * 3.6];
          } while (!verschieden(l));
          return { Q: Qn, f: f[0], H: f[1], m: m, eta: eta, u: u,
            text: f[2].charAt(0).toUpperCase() + f[2].slice(1) + ' verbrennt \\(' + ein(m, 'kg') + '\\) ' + f[0] + ' (\\(H = ' + ein(f[1], 'MJ/kg') + '\\)) mit dem Wirkungsgrad \\(\\eta = ' + tz(eta) + '\\). Wie viel Nutzwärme gibt er ab, in ' + u + '?' }; },
        pruefen: function(A, e){
          if (nah(e.Q, A.Q)) return null;
          if (nah(e.Q, A.Q / A.eta)) return 'Das ist die zugeführte Energie \\(m \\cdot H\\). Nutzbar ist nur der Anteil \\(\\eta\\) davon: Mal den Wirkungsgrad.';
          if (nah(e.Q, A.Q / (A.eta * A.eta))) return 'Durch den Wirkungsgrad geteilt? Die Nutzwärme ist kleiner als die zugeführte Energie: \\(Q_\\text{nutz} = \\eta \\cdot m \\cdot H\\).';
          if (nah(e.Q, A.u === 'MJ' ? A.Q / 3.6 : A.Q * 3.6)) return 'Einheit prüfen: \\(1\\;\\text{kWh} = 3.6\\;\\text{MJ}\\). Gefragt ist ' + A.u + '.';
          return '\\(Q_\\text{nutz} = \\eta \\cdot m \\cdot H\\), dann allenfalls in kWh: durch 3.6.'; },
        fehler: function(A){ return [[{ Q: String(A.Q / A.eta) }, 'Wirkungsgrad'], [{ Q: String(A.Q / (A.eta * A.eta)) }, 'geteilt'], [{ Q: String(A.u === 'MJ' ? A.Q / 3.6 : A.Q * 3.6) }, 'kWh']]; },
        loesung: function(A){ var mj = A.eta * A.m * A.H; return 'Q_\\text{nutz} = \\eta \\cdot m \\cdot H = ' + tz(A.eta) + ' \\cdot ' + ein(A.m, 'kg') + ' \\cdot ' + ein(A.H, 'MJ/kg') + ' ' + erg(mj, 'MJ') + (A.u === 'kWh' ? ' = \\dfrac{' + ein(+mj.toPrecision(4), 'MJ') + '}{3.6\\;\\text{MJ/kWh}} ' + erg(A.Q, 'kWh') : ''); } },
      'brennstoff': { felder: ['m'], muster: '<i>m</i> = {m} kg',
        neu: function(){
          var f, Q, eta, mm, l;
          do {
            f = zufall([['Heizöl', 42.6], ['Erdgas', 50.0], ['Holzpellets', 17.0], ['Buchenholz', 15.0]]);
            Q = zufall([800, 1500, 3500, 6000, 9000]); eta = zufall([0.72, 0.8, 0.87, 0.94]);
            mm = Q * 3.6 / (eta * f[1]);
            l = [mm, Q * 3.6 * eta / f[1], Q / (eta * f[1]), Q * 3.6 / f[1]];
          } while (!verschieden(l));
          return { m: mm, f: f[0], H: f[1], Q: Q, eta: eta,
            text: 'Eine Heizung soll \\(' + ein(Q, 'kWh') + '\\) Nutzwärme liefern. Wie viel ' + f[0] + ' (\\(H = ' + ein(f[1], 'MJ/kg') + '\\)) braucht sie bei einem Wirkungsgrad von \\(' + tz(eta) + '\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.m, A.m)) return null;
          if (nah(e.m, A.Q * 3.6 * A.eta / A.H)) return 'Gesucht ist die Menge: Der Wirkungsgrad steht im Nenner. Es braucht mehr Brennstoff, als ohne Verluste nötig wäre.';
          if (nah(e.m, A.Q / (A.eta * A.H))) return 'Die Nutzwärme in MJ umrechnen: \\(1\\;\\text{kWh} = 3.6\\;\\text{MJ}\\).';
          if (nah(e.m, A.Q * 3.6 / A.H)) return 'Das wäre die Menge ohne Verluste. Mit dem Wirkungsgrad \\(\\eta \\lt 1\\) braucht es mehr.';
          return '\\(m = \\dfrac{Q_\\text{nutz}}{\\eta \\cdot H}\\) mit \\(Q_\\text{nutz}\\) in MJ.'; },
        fehler: function(A){ return [[{ m: String(A.Q * 3.6 * A.eta / A.H) }, 'Nenner'], [{ m: String(A.Q / (A.eta * A.H)) }, 'MJ'], [{ m: String(A.Q * 3.6 / A.H) }, 'Verluste']]; },
        loesung: function(A){ return 'm = \\dfrac{Q_\\text{nutz}}{\\eta \\cdot H} = \\dfrac{' + ein(A.Q * 3.6, 'MJ') + '}{' + tz(A.eta) + ' \\cdot ' + ein(A.H, 'MJ/kg') + '} ' + erg(A.m, 'kg'); } },
      'heizzeit': { felder: ['t'], muster: '<i>t</i> = {t} min',
        neu: function(){
          var g, m, t1, t2, P, eta, Q, t, l;
          do {
            g = zufall([['Ein Wasserkocher', [0.8, 1.2, 1.7], [1800, 2200, 2400], 100], ['Ein Tauchsieder', [0.3, 0.5], [800, 1000], 100], ['Ein Boiler mit Heizstab', [50, 80, 120], [2000, 3000], 60]]);
            m = zufall(g[1]); P = zufall(g[2]); t1 = zufall([10, 14, 18]); t2 = g[3]; eta = zufall([0.82, 0.88, 0.92, 0.96]);
            Q = m * 4182 * (t2 - t1); t = Q / (eta * P) / 60;
            l = [t, Q * eta / P / 60, Q / P / 60, t * 60];
          } while (!verschieden(l));
          return { t: t, m: m, t1: t1, t2: t2, P: P, eta: eta, Q: Q,
            text: g[0] + ' (\\(' + ein(P, 'W') + '\\), Wirkungsgrad \\(' + tz(eta) + '\\)) erwärmt \\(' + ein(m, 'kg') + '\\) Wasser von \\(' + gr(t1) + '\\) auf \\(' + gr(t2) + '\\). Wie lange dauert das?' }; },
        pruefen: function(A, e){
          if (nah(e.t, A.t)) return null;
          if (nah(e.t, A.t * 60)) return 'Das sind Sekunden. Gefragt sind Minuten.';
          if (nah(e.t, A.Q * A.eta / A.P / 60)) return 'Mit Verlusten dauert es länger: Der Wirkungsgrad steht im Nenner, \\(t = \\dfrac{Q}{\\eta \\cdot P}\\).';
          if (nah(e.t, A.Q / A.P / 60)) return 'Das wäre die Zeit ohne Verluste. Der Wirkungsgrad fehlt.';
          return 'Erst \\(Q = m \\cdot c \\cdot \\Delta T\\), dann \\(t = \\dfrac{Q}{\\eta \\cdot P}\\) in s, dann in min.'; },
        fehler: function(A){ return [[{ t: String(A.t * 60) }, 'Minuten'], [{ t: String(A.Q * A.eta / A.P / 60) }, 'Nenner'], [{ t: String(A.Q / A.P / 60) }, 'Wirkungsgrad']]; },
        loesung: function(A){ return 'Q = m \\cdot c \\cdot \\Delta T = ' + ein(A.m, 'kg') + ' \\cdot 4182' + JKK + ' \\cdot ' + ein(A.t2 - A.t1, 'K') + ' ' + erg(A.Q, 'J') + ',\\quad t = \\dfrac{Q}{\\eta \\cdot P} = \\dfrac{' + ein(+A.Q.toPrecision(4), 'J') + '}{' + tz(A.eta) + ' \\cdot ' + ein(A.P, 'W') + '} ' + erg(A.t * 60, 's') + ' ' + erg(A.t, 'min'); } },

      /* ----- Kapitel 5: Energiesysteme ----- */
      'pv': { felder: ['x'], muster: function(A){ return A.art === 'E' ? '<i>E</i> = {x} kWh' : '<i>A</i> = {x} m²'; },
        neu: function(){
          // Photovoltaik (Strom, η um 0.2) oder Sonnenkollektor (Wärme fürs Warmwasser, η 0.40 bis 0.50: höchstens rund 50 % wie in der Tabelle)
          var art, kol, A, eta, I, E, x, l;
          do {
            art = zufall(['E', 'A']); kol = zufall([false, false, true]); eta = kol ? zufall([0.4, 0.45, 0.5]) : zufall([0.18, 0.21, 0.22]); I = zufall([1000, 1150, 1250, 1400]);
            if (art === 'E'){ A = kol ? zufall([4, 7, 9]) : zufall([6, 12, 35, 60]); x = A * eta * I; l = [x, A * I, A * I / eta]; }
            else { E = kol ? zufall([1600, 2400, 3500]) : zufall([1800, 3200, 6500, 12000]); x = E / (eta * I); l = [x, E / I, E * eta / I]; }
          } while (!verschieden(l));
          var was = kol ? 'Wärme' : 'Strom', anl = kol ? 'Ein Sonnenkollektor fürs Warmwasser' : 'Eine Photovoltaikanlage', fl = kol ? 'Kollektorfläche' : 'Modulfläche';
          return { x: x, art: art, A: A, E: E, eta: eta, I: I, kol: kol, was: was,
            text: art === 'E' ? anl + ' hat \\(' + tz(A) + '\\;\\text{m}^2\\) ' + fl + ' mit dem Wirkungsgrad \\(' + tz(eta) + '\\). Am Ort fallen im Jahr \\(' + tz(I) + '\\;\\text{kWh}\\) Sonnenlicht auf jeden Quadratmeter. Wie viel ' + was + ' liefert ' + (kol ? 'er' : 'sie') + ' im Jahr?'
                              : anl + ' soll im Jahr \\(' + ein(E, 'kWh') + '\\) ' + was + ' liefern. Wirkungsgrad \\(' + tz(eta) + '\\), am Ort fallen im Jahr \\(' + tz(I) + '\\;\\text{kWh}\\) Sonnenlicht auf jeden Quadratmeter. Wie gross muss die ' + fl + ' sein?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'E'){
            if (nah(e.x, A.A * A.I)) return 'Das ist das ganze Sonnenlicht. ' + A.was + ' wird nur der Anteil \\(\\eta\\) davon: mal den Wirkungsgrad.';
            if (nah(e.x, A.A * A.I / A.eta)) return 'Durch den Wirkungsgrad geteilt? Genutzt wird weniger, als an Sonnenlicht ankommt: mal \\(\\eta\\).';
          } else {
            if (nah(e.x, A.E / A.I)) return 'So wäre es mit einem Wirkungsgrad von 1. Nur der Anteil \\(\\eta\\) wird genutzt — es braucht mehr Fläche.';
            if (nah(e.x, A.E * A.eta / A.I)) return 'Umstellen: \\(A = \\dfrac{E}{\\eta \\cdot I}\\) — der Wirkungsgrad gehört in den Nenner.';
          }
          return '\\(E = \\eta \\cdot A \\cdot I\\) mit \\(I\\) = Sonnenlicht je m² und Jahr.'; },
        fehler: function(A){ return A.art === 'E' ? [[{ x: String(A.A * A.I) }, 'Sonnenlicht'], [{ x: String(A.A * A.I / A.eta) }, 'geteilt']] : [[{ x: String(A.E / A.I) }, 'Fläche'], [{ x: String(A.E * A.eta / A.I) }, 'Nenner']]; },
        loesung: function(A){ return A.art === 'E' ? 'E = \\eta \\cdot A \\cdot I = ' + tz(A.eta) + ' \\cdot ' + tz(A.A) + '\\;\\text{m}^2 \\cdot ' + tz(A.I) + '\\;\\text{kWh/m}^2 ' + erg(A.x, 'kWh')
                                                     : 'A = \\dfrac{E}{\\eta \\cdot I} = \\dfrac{' + ein(A.E, 'kWh') + '}{' + tz(A.eta) + ' \\cdot ' + tz(A.I) + '\\;\\text{kWh/m}^2} \\approx ' + tz(+A.x.toPrecision(3)) + '\\;\\text{m}^2'; } },
      'wasserkraft': { felder: ['E'], muster: '<i>E</i> = {E} kWh',
        neu: function(){
          var V, h, eta, E, l;
          do { V = zufall([50, 120, 400, 2500]); h = zufall([80, 150, 350, 620, 1100]); eta = zufall([0.8, 0.85, 0.9]);
               E = eta * V * 1000 * 9.81 * h / 3.6e6; l = [E, E / 9.81, E * 3.6e6, E * 3600, E / eta]; } while (!verschieden(l));
          return { E: E, V: V, h: h, eta: eta,
            text: 'In einem Speicherkraftwerk fallen \\(' + tz(V) + '\\;\\text{m}^3\\) Wasser (\\(\\rho = 1000\\;\\text{kg/m}^3\\)) \\(' + ein(h, 'm') + '\\) tief durch die Turbine. Wirkungsgrad: \\(' + tz(eta) + '\\). Wie viel Strom entsteht, in kWh?' }; },
        pruefen: function(A, e){
          if (nah(e.E, A.E)) return null;
          if (nah(e.E, A.E / 9.81)) return 'Lageenergie ist \\(m \\cdot g \\cdot h\\) — die Erdbeschleunigung \\(g = 9.81\\;\\text{m/s}^2\\) fehlt.';
          if (nah(e.E, A.E * 3.6e6)) return 'Das ist Joule (Wattsekunden). In kWh: durch \\(3.6 \\cdot 10^6\\) teilen.';
          if (nah(e.E, A.E * 3600)) return 'Das ist Kilojoule. In kWh: durch \\(3600\\) teilen (\\(1\\;\\text{kWh} = 3600\\;\\text{kJ}\\)).';
          if (nah(e.E, A.E / A.eta)) return 'Das ist die ganze Lageenergie. Strom wird nur der Anteil \\(\\eta\\): mal den Wirkungsgrad.';
          return '\\(E = \\eta \\cdot m \\cdot g \\cdot h\\) mit \\(m = \\rho \\cdot V\\), dann in kWh: \\(1\\;\\text{kWh} = 3.6 \\cdot 10^6\\;\\text{J}\\).'; },
        fehler: function(A){ return [[{ E: String(A.E / 9.81) }, 'Erdbeschleunigung'], [{ E: String(A.E * 3.6e6) }, 'Joule'], [{ E: String(A.E * 3600) }, 'Kilojoule'], [{ E: String(A.E / A.eta) }, 'Wirkungsgrad']]; },
        loesung: function(A){ var J = A.eta * A.V * 1000 * 9.81 * A.h; return 'E = \\eta \\cdot \\rho \\cdot V \\cdot g \\cdot h = ' + tz(A.eta) + ' \\cdot 1000\\;\\text{kg/m}^3 \\cdot ' + tz(A.V) + '\\;\\text{m}^3 \\cdot 9.81\\;\\text{m/s}^2 \\cdot ' + ein(A.h, 'm') + ' ' + erg(J, 'J') + ' ' + erg(A.E, 'kWh'); } },
      'waermepumpe': { felder: ['E', 'U'], muster: '<i>E</i><sub>el</sub> = {E} kWh; aus der Umgebung: {U} kWh',
        neu: function(){
          var Q, cop, l;
          do { Q = zufall([6000, 9500, 12500, 16000, 22000]); cop = zufall([2.8, 3.2, 4.2, 4.5, 5]); l = [Q / cop, Q - Q / cop, Q * cop]; } while (!verschieden(l));
          return { E: Q / cop, U: Q - Q / cop, Q: Q, cop: cop,
            text: 'Eine Wärmepumpe liefert einem Haus im Jahr \\(' + ein(Q, 'kWh') + '\\) Heizwärme; ihre Leistungszahl beträgt im Mittel \\(\\text{COP} = ' + tz(cop) + '\\). Wie viel Strom braucht sie, und wie viel Wärme holt sie aus der Umgebung?' }; },
        eingabe: function(A){ return { E: String(A.E), U: String(A.U) }; },
        pruefen: function(A, e){
          if (nah(e.E, A.E) && nah(e.U, A.U)) return null;
          if (nah(e.E, A.Q * A.cop)) return 'Mal die Leistungszahl? \\(\\text{COP} = \\dfrac{Q_\\text{warm}}{E_\\text{el}}\\), also \\(E_\\text{el} = \\dfrac{Q_\\text{warm}}{\\text{COP}}\\) — der Strom ist kleiner als die Heizwärme.';
          if (nah(e.E, A.U) && nah(e.U, A.E)) return 'Strom und Umgebungswärme sind vertauscht: Der grössere Teil kommt aus der Umgebung.';
          if (nah(e.E, A.E)) return 'Der Strom stimmt. Umgebungswärme = Heizwärme − Strom.';
          return '\\(E_\\text{el} = \\dfrac{Q_\\text{warm}}{\\text{COP}}\\), Umgebungswärme \\(= Q_\\text{warm} - E_\\text{el}\\).'; },
        fehler: function(A){ return [[{ E: String(A.Q * A.cop), U: String(A.U) }, 'COP'], [{ E: String(A.U), U: String(A.E) }, 'vertauscht'], [{ E: String(A.E), U: String(A.Q) }, 'Umgebungswärme']]; },
        loesung: function(A){ return 'E_\\text{el} = \\dfrac{Q_\\text{warm}}{\\text{COP}} = \\dfrac{' + ein(A.Q, 'kWh') + '}{' + tz(A.cop) + '} ' + erg(A.E, 'kWh') + ',\\quad Q_\\text{U} = ' + ein(A.Q, 'kWh') + ' - ' + ein(+A.E.toPrecision(4), 'kWh') + ' ' + erg(A.U, 'kWh'); } },

      /* ----- Kapitel 6: Wärmetransport ----- */
      'weg': { felder: ['w'], muster: 'Weg: {w:Leitung|Konvektion|Strahlung}', klartext: true,
        neu: function(){
          var s = zufall([['Ein Bügeleisen glättet ein Hemd und macht es warm.', 'Leitung'], ['Ein Lötkolben erhitzt den Draht, den er berührt.', 'Leitung'],
                          ['Eine Wärmflasche wärmt den Bauch durch das Tuch hindurch.', 'Leitung'], ['Die Schuhsohle wird auf heissem Asphalt warm.', 'Leitung'],
                          ['Über einem Toaster steigt warme Luft auf.', 'Konvektion'], ['Im Kochtopf steigt das heisse Wasser in der Mitte auf und sinkt am Rand.', 'Konvektion'],
                          ['Der Golfstrom bringt warmes Meerwasser nach Europa.', 'Konvektion'], ['Ein Heizlüfter bläst warme Luft ins Zimmer.', 'Konvektion'],
                          ['Eine Wärmelampe wärmt Küken, ohne die Luft dazwischen stark zu erwärmen.', 'Strahlung'], ['Die Sonne erwärmt eine Raumsonde im Weltall.', 'Strahlung'],
                          ['Ein Grill mit Glut über dem Gargut bräunt den Käse von oben.', 'Strahlung'], ['Eine Wärmebildkamera sieht die warme Hauswand aus Distanz.', 'Strahlung']]);
          return { w: s[1], text: s[0] + ' Auf welchem Weg wird die Wärme vor allem übertragen?' }; },
        pruefen: function(A, e){
          if (e.w === A.w) return null;
          if (e.w === 'Leitung') return 'Leitung heisst: Teilchen geben Energie an ihre Nachbarn weiter, der Stoff bleibt am Ort. Berühren sich hier zwei Körper direkt?';
          if (e.w === 'Konvektion') return 'Konvektion heisst: Warmer Stoff (Luft, Wasser) strömt selbst und trägt die Energie mit. Strömt hier etwas?';
          return 'Strahlung braucht keinen Stoff dazwischen. Kommt die Energie hier ohne Berührung und ohne Strömung an?'; },
        fehler: function(A){ return ['Leitung', 'Konvektion', 'Strahlung'].filter(function(w){ return w !== A.w; }).map(function(w){ return [{ w: w }, w === 'Leitung' ? 'Nachbarn' : (w === 'Konvektion' ? 'strömt' : 'ohne Berührung')]; }); },
        loesung: function(A){ return A.w + ': ' + { Leitung: 'Die Energie wandert durch den Stoff von Teilchen zu Teilchen, dort wo sich die Körper berühren.', Konvektion: 'Der warme Stoff (Luft oder Wasser) strömt selbst und trägt die Energie mit.', Strahlung: 'Infrarotstrahlung trägt die Energie, ganz ohne Stoff dazwischen.' }[A.w]; } },
      'bremsen': { felder: ['w'], muster: 'bremst vor allem: {w:Leitung|Konvektion|Strahlung}', klartext: true,
        neu: function(){
          var s = zufall([['Ein Holzgriff an der Pfanne', 'Leitung'], ['Ein dicker Topflappen aus Stoff', 'Leitung'], ['Ein Korkuntersetzer unter dem heissen Topf', 'Leitung'],
                          ['Dichtungen an Fenstern und Türen', 'Konvektion'], ['Ein Windschutz um den Campingkocher', 'Konvektion'], ['Ein Deckel auf dem Kochtopf', 'Konvektion'],
                          ['Ein weisser Anstrich auf einem Flachdach in der Sonne', 'Strahlung'], ['Eine Sonnenschutzfolie am Autofenster', 'Strahlung'], ['Eine Alufolie an der Wand hinter dem Heizkörper', 'Strahlung']]);
          return { w: s[1], text: s[0] + ': Welchen Weg der Wärme bremst diese Massnahme vor allem?' }; },
        pruefen: function(A, e){
          if (e.w === A.w) return null;
          if (e.w === 'Leitung') return 'Leitung bremst man mit Stoffen, die schlecht leiten (Holz, Kork, eingeschlossene Luft). Liegt hier ein schlechter Leiter zwischen warm und kalt?';
          if (e.w === 'Konvektion') return 'Konvektion bremst man, indem man Strömung verhindert (dicht machen, abdecken). Wird hier eine Strömung aufgehalten?';
          return 'Strahlung bremst man mit spiegelnden Flächen, die sie zurückwerfen (eine helle Farbe wirft vor allem Sonnenlicht zurück). Wird hier etwas zurückgeworfen?'; },
        fehler: function(A){ return ['Leitung', 'Konvektion', 'Strahlung'].filter(function(w){ return w !== A.w; }).map(function(w){ return [{ w: w }, w === 'Leitung' ? 'schlechter Leiter' : (w === 'Konvektion' ? 'Strömung' : 'zurückgeworfen')]; }); },
        loesung: function(A){ return A.w + ': ' + { Leitung: 'Ein schlechter Wärmeleiter liegt zwischen warm und kalt.', Konvektion: 'Die Massnahme hält die warme Luft fest und verhindert so die Strömung.', Strahlung: 'Die spiegelnde Fläche wirft die Strahlung zurück; eine helle Farbe tut das vor allem beim Sonnenlicht.' }[A.w]; } },
      'leitfaehigkeit': { felder: ['x'], muster: '{x} -mal so viel',
        neu: function(){
          var L = [['Kupfer', 400], ['Eisen', 80], ['Glas', 0.8], ['Wasser', 0.6], ['Holz', 0.15], ['Mineralwolle', 0.04], ['ruhender Luft', 0.026]], a, b;
          do { a = zufall(L); b = zufall(L); } while (a[1] <= b[1] || (a[0] === 'Kupfer' && b[0] === 'Holz') || (a[0] === 'Eisen' && b[0] === 'Holz') || a[1] / b[1] < 1.5);
          return { x: a[1] / b[1], a: a, b: b,
            text: 'Zwei gleich grosse, gleich dicke Platten liegen zwischen denselben Temperaturen: eine aus ' + a[0] + ' (\\(\\lambda = ' + tz(a[1]) + '\\;\\text{W/(m·K)}\\)), eine aus ' + b[0] + ' (\\(\\lambda = ' + tz(b[1]) + '\\;\\text{W/(m·K)}\\)). Wievielmal so viel Wärme fliesst je Sekunde durch die Platte aus ' + a[0] + '?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, 1 / A.x)) return 'Umgekehrt: Der bessere Leiter lässt mehr Wärme durch — die Zahl muss grösser als 1 sein.';
          return 'Bei gleicher Fläche, Dicke und Temperatur wächst der Wärmestrom mit \\(\\lambda\\): Verhältnis der beiden Werte.'; },
        fehler: function(A){ return [[{ x: String(1 / A.x) }, 'Umgekehrt']]; },
        loesung: function(A){ return '\\dfrac{\\lambda_1}{\\lambda_2} = \\dfrac{' + tz(A.a[1]) + '}{' + tz(A.b[1]) + '} ' + (Math.abs(+A.x.toPrecision(3) - A.x) < 1e-9 ? '= ' : '\\approx ') + tz(+A.x.toPrecision(3)); } },

      /* ----- Kapitel 7: Treibhauseffekt ----- */
      'abstrahlung': { felder: ['x'], muster: function(A){ return A.art === 'r' ? '<i>ϑ</i> = {x} °C' : '<i>P</i>/<i>A</i> = {x} W/m²'; },
        neu: function(){
          // vorwärts: Temperatur gegeben, P/A gesucht; rückwärts: P/A gegeben, Temperatur in °C gesucht
          if (zufall(['v', 'r']) === 'r'){
            var q = zufall([['Ein Ziegeldach', 250], ['Eine Hauswand', 350], ['Ein Teich', 420], ['Eine Strassenoberfläche', 500], ['Ein Heizkörper', 600]]);
            var Tr = Math.pow(q[1] / SIGMA, 0.25);
            return { x: Tr - 273.15, art: 'r', PA: q[1], T: Tr, text: q[0] + ' strahlt als idealer Strahler \\(' + q[1] + '\\;\\text{W/m}^2\\) Wärmestrahlung ab. Welche Temperatur hat seine Oberfläche, in Grad Celsius? Rechne mit \\(\\sigma = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)\\).' };
          }
          var o = zufall([['Ein Wüstenboden', 45, 'er'], ['Eine Eisfläche', -10, 'sie'], ['Die Haut', 33, 'sie'], ['Ein Heizkörper', 55, 'er'], ['Asphalt in der Sonne', 50, 'er'], ['Eine Schneedecke', -20, 'sie'], ['Die Meeresoberfläche', 22, 'sie']]);
          var T = o[1] + 273.15;
          return { x: SIGMA * Math.pow(T, 4), art: 'v', t: o[1], T: T, text: o[0] + ' hat \\(' + gr(o[1]).replace(/^-/, '−') + '\\). Wie viel Wärmestrahlung gibt ' + o[2] + ' je Quadratmeter ab? Rechne mit \\(\\sigma = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)\\) und einem idealen Strahler.' }; },
        pruefen: function(A, e){
          if (A.art === 'r'){
            if (Math.abs(e.x - A.x) <= 0.6) return null;   // T auf ganze Kelvin gerundet zählt
            if (Math.abs(e.x - A.T) <= 0.5) return 'Das ist die Temperatur in Kelvin. Gefragt ist Grad Celsius: \\(\\vartheta = T - 273.15\\).';
            if (nah(e.x, Math.sqrt(A.PA / SIGMA) - 273.15, 0.01) || nah(e.x, Math.sqrt(A.PA / SIGMA), 0.01)) return 'Aus \\(T^4\\) holt man \\(T\\) mit der vierten Wurzel, nicht mit der Quadratwurzel.';
            return 'Nach \\(T\\) umstellen: \\(T = \\sqrt[4]{\\dfrac{P/A}{\\sigma}}\\), dann in Grad Celsius umrechnen.';
          }
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, SIGMA * Math.pow(A.t, 4))) return 'Die Temperatur in Kelvin einsetzen: \\(T = \\vartheta + 273.15\\).';
          if (nah(e.x, Math.pow(A.T, 4))) return 'Die Stefan-Boltzmann-Konstante \\(\\sigma\\) fehlt.';
          return '\\(\\dfrac{P}{A} = \\sigma \\cdot T^4\\) mit \\(T\\) in Kelvin.'; },
        fehler: function(A){
          if (A.art === 'r') return [[{ x: String(A.T) }, 'Kelvin'], [{ x: String(Math.sqrt(A.PA / SIGMA) - 273.15) }, 'Quadratwurzel']];
          return [[{ x: String(SIGMA * Math.pow(A.t, 4)) }, 'Kelvin'], [{ x: String(Math.pow(A.T, 4)) }, 'Konstante']]; },
        loesung: function(A){
          if (A.art === 'r') return 'T = \\sqrt[4]{\\dfrac{P/A}{\\sigma}} = \\sqrt[4]{\\dfrac{' + tz(A.PA) + '\\;\\text{W/m}^2' + '}{5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)}} \\approx ' + ein(+A.T.toFixed(1), 'K') + ',\\quad \\vartheta = T - 273.15 \\approx ' + gr(+A.x.toFixed(1));
          return '\\dfrac{P}{A} = \\sigma \\cdot T^4 = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4) \\cdot (' + tz(+A.T.toFixed(2)) + '\\;\\text{K})^4 ' + ergR(A.x, '\\text{W/m}^2'); } },
      'durchlaessig': { felder: ['x'], muster: function(A){ return A.art === 'p' ? '{x} %' : '{x} W/m²'; },
        neu: function(){
          // Einschichtmodell wie sim7 (Licht 240 W/m², ganz durchgelassen): Der Boden strahlt U = 480 W/m² / (1 + D) ab,
          // der Anteil D gelangt direkt ins All. U und D passen so im Modell zusammen.
          var art = zufall(['p', 'w']), D = zufall([0.15, 0.18, 0.27, 0.30, 0.33]), U = Math.round(480 / (1 + D));
          if (art === 'p') return { x: 100 * D, art: art, U: U, D: D, text: 'Im Einschichtmodell strahlt der Boden \\(' + tz(U) + '\\;\\text{W/m}^2\\) Wärmestrahlung ab; davon gelangen \\(' + tz(+(U * D).toPrecision(4)) + '\\;\\text{W/m}^2\\) direkt ins All. Wie viel Prozent der Wärmestrahlung lässt die Modell-Atmosphäre durch?' };
          return { x: U * D, art: art, U: U, D: D, text: 'Im Einschichtmodell lässt die Atmosphäre ' + tz(100 * D) + ' % der Wärmestrahlung des Bodens direkt ins All. Der Boden strahlt \\(' + tz(U) + '\\;\\text{W/m}^2\\) ab. Wie viel Wärmestrahlung gelangt direkt ins All?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'p'){ if (nah(e.x, 100 - A.x)) return 'Das ist der Anteil, den die Atmosphäre zurückhält. Gefragt ist der Anteil, der durchkommt.'; if (nah(e.x, A.D)) return 'Als Anteil stimmt es — in Prozent: mal 100.'; }
          else if (nah(e.x, A.U - A.x)) return 'Das ist der Teil, den die Atmosphäre zurückhält. Gefragt ist der Teil, der durchkommt.';
          return A.art === 'p' ? 'Durchgelassen geteilt durch abgestrahlt, mal 100 %.' : 'Durchgelassen = Anteil mal abgestrahlt.'; },
        fehler: function(A){ return A.art === 'p' ? [[{ x: String(100 - A.x) }, 'zurückhält'], [{ x: String(A.D) }, 'Prozent']] : [[{ x: String(A.U - A.x) }, 'zurückhält']]; },
        loesung: function(A){ return A.art === 'p' ? '\\dfrac{' + tz(+(A.U * A.D).toPrecision(4)) + '\\;\\text{W/m}^2}{' + tz(A.U) + '\\;\\text{W/m}^2} = ' + tz(A.D) + ' = ' + tz(A.x) + '\\;\\%' : tz(A.D) + ' \\cdot ' + tz(A.U) + '\\;\\text{W/m}^2 = ' + tz(+A.x.toPrecision(4)) + '\\;\\text{W/m}^2'; } },
      'aussage': { felder: ['r'], muster: 'Die Aussage ist {r:richtig|falsch}.', klartext: true,
        neu: function(){
          // [Aussage, richtig/falsch, Erklärung (Lösung), Hinweis (lenkt aufs Nachdenken, verrät nichts)]
          var s = zufall([['Stickstoff und Sauerstoff halten den grössten Teil der Wärmestrahlung zurück.', 'falsch', 'Stickstoff und Sauerstoff lassen Licht und Wärmestrahlung fast ungehindert durch. Zurückgehalten wird die Wärmestrahlung vor allem von Wasserdampf und Kohlendioxid.', 'Welche Gase nennt das Festhalten als Treibhausgase — und wie viel der Luft machen sie aus?'],
                          ['Ohne den natürlichen Treibhauseffekt läge die mittlere Bodentemperatur der Erde bei rund −18 °C.', 'richtig', 'Ohne Atmosphäre müsste der Boden die rund 240 W/m² selbst abstrahlen: σ · T⁴ = 240 W/m² ergibt rund 255 K.', 'Rechne nach: Bei welcher Temperatur strahlt ein Boden genau die 240 W/m² ab, die er von der Sonne bekommt?'],
                          ['Die Sonne strahlt vor allem sichtbares Licht ab, weil ihre Oberfläche rund 5500 °C heiss ist.', 'richtig', 'Je heisser ein Körper, desto kürzer die Wellenlänge, bei der er am meisten abstrahlt. Die kühle Erde strahlt darum im Infrarot.', 'Wovon hängt ab, ob ein Körper Licht oder Wärmestrahlung abgibt?'],
                          ['Die Atmosphäre ist für Wärmestrahlung durchlässiger als für sichtbares Licht.', 'falsch', 'Umgekehrt: Licht kommt weitgehend durch, die Wärmestrahlung des Bodens nur zum kleinen Teil. Genau dieser Unterschied macht den Treibhauseffekt.', 'Denk an die Simulation: Wann wurde der Boden wärmer als ohne Atmosphäre?'],
                          ['Mehr Kohlendioxid erwärmt die Erde, weil die Atmosphäre dann mehr Sonnenlicht durchlässt.', 'falsch', 'Kohlendioxid ändert fast nichts am Licht. Es hält mehr Wärmestrahlung zurück und strahlt mehr davon zum Boden zurück.', 'Welche der beiden Strahlungen nimmt Kohlendioxid auf — das Licht der Sonne oder die Wärmestrahlung des Bodens?'],
                          ['Die Atmosphäre strahlt auch nach unten zum Boden; diese Gegenstrahlung wärmt ihn zusätzlich zum Sonnenlicht.', 'richtig', 'Was die Treibhausgase an Wärmestrahlung aufnehmen, geben sie in alle Richtungen wieder ab — auch nach unten.', 'In welche Richtungen strahlen die Gase ab, was sie aufgenommen haben?'],
                          ['Ein warmer Boden strahlt umso mehr Wärmestrahlung ab, je höher seine Temperatur ist.', 'richtig', 'Die abgestrahlte Leistung je m² wächst mit der vierten Potenz der absoluten Temperatur: σ · T⁴.', 'Was sagt die Formel für die Abstrahlung je Quadratmeter über die Temperatur?'],
                          ['Treibhausgase lassen Wärmestrahlung nur in einer Richtung durch: hinein ja, hinaus nein.', 'falsch', 'Es gibt keine Richtung: Treibhausgase nehmen Wärmestrahlung auf und strahlen sie nach allen Seiten ab. Licht und Wärmestrahlung unterscheiden sich in der Wellenlänge, nicht in der Richtung.', 'Worin unterscheiden sich das hereinkommende Sonnenlicht und die Wärmestrahlung des Bodens wirklich?']]);
          return { r: s[1], text: '«' + s[0] + '» Stimmt das?', erkl: s[2], hinweis: s[3] }; },
        pruefen: function(A, e){ return e.r === A.r ? null : 'Noch nicht. ' + A.hinweis; },
        fehler: function(A){ return [[{ r: A.r === 'richtig' ? 'falsch' : 'richtig' }, 'Noch nicht']]; },
        loesung: function(A){ return (A.r === 'richtig' ? 'Richtig. ' : 'Falsch. ') + A.erkl; } }
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
          rueck.innerHTML = (f || 'Noch nicht.') + (versuche >= 2 ? ' <details class="ue-loes"><summary>Lösung</summary>' + (T.klartext ? T.loesung(A) : '\\(' + T.loesung(A) + '\\)') + '</details>' : '');
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
