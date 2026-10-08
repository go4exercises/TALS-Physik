<script>
/* Leitprogramm Temperatur — laufende Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung.
   Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr, Übungsrahmen) wörtlich aus dem
   Leitprogramm Hydrostatik; Achsen() mit ya (Höhe der x-Achse) wie im Leitprogramm Energie.
   Neu sind die Simulationen (Luftteilchen in der Box, drei Stoffe bei derselben Temperatur,
   Gasthermometer, Temperaturverlauf mit Celsius- und Kelvin-Achse) und die Übungstypen für 5.1.
   T = ϑ + 273.15 wie Themenseite 5.1. Farben (Farbe = eine Bedeutung): Celsius-Temperatur
   Bernstein, Kelvin-Temperatur und absoluter Nullpunkt Grün, Temperaturdifferenz Orange, Druck Rot,
   Teilchen und Messkurven Tinte. Zahlen mit Dezimalpunkt und echtem Minus; «·» nur als Malpunkt,
   Trenner ist der Strichpunkt. */
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
    var sx = o.sx || 1, sy = o.sy || 1, i, ya = o.ya == null ? 0 : o.ya;   // ya: Höhe der x-Achse (Fenster ohne y = 0)
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
    var breite = function(s){ return String(s).replace(/_/g, '').length * 6.6; };
    // Teilungszahlen einzeln schützen (die y-Achse steht hier oft mitten im Bild, bei ϑ = 0)
    var schutz = [[W - 3 - breite(o.xname || 'x'), Y(ya) - pf - 14, W, Y(ya) - pf + 1],
                  [X(0) + pf, 0, X(0) + pf + 4 + breite(o.yname || 'y'), pf + 8]];
    (o.xm || []).forEach(function(t){ var b = breite(minus(t)) / 2 + 2; schutz.push([X(t) - b, Y(ya) + 2, X(t) + b, Y(ya) + 16]); });
    (o.ym || []).forEach(function(t){ schutz.push([X(0) - 7 - breite(minus(t)), Y(t) - 7, X(0) - 2, Y(t) + 6]); });
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
        // Zahl der Konflikte einer Lage (ausserhalb des Bildes: unbrauchbar); gewählt wird die erste
        // freie Lage, sonst die mit den wenigsten Konflikten
        function konflikte(b){
          if (b[0] < 1 || b[2] > W - 1 || b[1] < 1 || b[3] > H - 1) return 1000;
          var n = 0;
          for (var i = 0; i < alle.length; i++){ var c = alle[i]; if (b[0] < c[2] && b[2] > c[0] && b[1] < c[3] && b[3] > c[1]) n += 40; }   // Text auf Text wiegt schwerer als Text auf der Kurve
          for (var j = 0; j < ks.length; j++){
            var vor = null;
            for (var k = 0; k <= 30; k++){
              var xx = x0 + (b[0] - 3 + (b[2] - b[0] + 6) * k / 30) / W * (x1 - x0);
              if (xx < ks[j][1] || xx > ks[j][2]){ vor = null; continue; }
              var yy = Y(ks[j][0](xx));
              if (yy > b[1] - 3 && yy < b[3] + 3) n++;
              else if (vor != null && Math.min(vor, yy) < b[3] + 3 && Math.max(vor, yy) > b[1] - 3) n++;
              vor = yy;
            }
          }
          return n;
        }
        var gew = wahl[0], best = Infinity;
        for (var i = 0; i < wahl.length; i++){
          var c = wahl[i], tx = px + c[0], ty = py + c[1], l = c[2] === 'end' ? tx - bw : tx;
          var n = konflikte([l, ty - bh + 1, l + bw, ty + 3]);
          if (n < best){ best = n; gew = c; }
          if (n === 0) break;
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


  /* ---------- Gemeinsames für die Teilchenbilder ----------
     Teilchenbewegung allein aus der Zeit gerechnet (für die Testhaken der Clipbilder):
     Gasteilchen fliegen geradeaus und prallen an den Wänden ab (Spiegelung, refl), ohne Stösse
     untereinander. Die Tempi sind Quantile der Maxwell-Verteilung, normiert auf den Mittelwert 1
     (mit python3 berechnet), mal dem mittleren Tempo. */
  var T0 = 273.15;                                        // wie Themenseite 5.1: T = ϑ + 273.15
  var Q30 = [0.253, 0.372, 0.448, 0.509, 0.561, 0.607, 0.65, 0.691, 0.73, 0.767, 0.804, 0.84, 0.876, 0.912, 0.947,
             0.984, 1.02, 1.058, 1.097, 1.137, 1.179, 1.224, 1.272, 1.324, 1.382, 1.447, 1.524, 1.62, 1.754, 2.008];
  var Q16 = [0.316, 0.469, 0.57, 0.654, 0.728, 0.798, 0.866, 0.933, 1.001, 1.071, 1.146, 1.229, 1.322, 1.436, 1.59, 1.87];
  function folge(seed){                                   // feste Zufallsfolge (mulberry32): jedes Bild gleich
    var a = seed >>> 0;
    return function(){ a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function refl(u, a, b){ var L = b - a, m = ((u - a) % (2 * L) + 2 * L) % (2 * L); return a + (m < L ? m : 2 * L - m); }
  // Mittleres Tempo von Stickstoff (Hauptteil der Luft): v = √(8 R T / (π M)), M = 0.028 kg/mol
  function vMittel(c){ return Math.sqrt(8 * 8.314 * (c + T0) / (Math.PI * 0.028)); }
  function grad(c){ return minus(String(c)) + NB + '°C'; }

  /* ---------- Kapitel 1: Luftteilchen in der Box ----------
     30 Stickstoffteilchen fliegen in einer Box; das Tempo jedes Teilchens wächst mit der
     Temperatur. Darunter das mittlere Tempo über der Temperatur. Unterschied zur Themenseite
     (Animation 1): Regler in °C (Kelvin kommt erst in Kapitel 3), Tempi in m/s statt in Prozent,
     die Kurve zum Ablesen, Aufträge in der Leiste. Ein markiertes Teilchen ◎ ist schneller als
     das Mittel. Stickstoff wird bei −196 °C flüssig: Regler −150 °C bis 300 °C.
     Clipbeispiel (Problem): 20 °C → 80 °C. Startwert 150 °C (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var box = g_(svg), dia = g_(svg, { transform: 'translate(0,178)' }), K = null;
    var BW = 300, BH = 150, R = 4.2, KPX = 0.13;                             // 0.13 px je (m/s · s): 471 m/s → 61 px/s
    var rnd = folge(11), MARK = 25, teil = [];
    for (var i = 0; i < Q30.length; i++){
      var w = rnd() * 2 * Math.PI;
      teil.push({ x0: R + rnd() * (BW - 2 * R), y0: R + rnd() * (BH - 2 * R), cx: Math.cos(w), cy: Math.sin(w), q: Q30[i], s: 0 });
    }
    var lief = false, besucht = {}, pruefen = function(){}, tAlt = 0;
    var B = Bedienung(fig, function(){ besucht[B.wert('c')] = true; zeichnen(); });
    var uhr = Uhr(function(t){ var dt = Math.min(0.1, t - tAlt); tAlt = t; var v = vMittel(B.wert('c'));
      teil.forEach(function(p){ p.s += p.q * v * KPX * dt; }); teilchen(); });
    var knopf = aktionen(fig, [['start', '▶ Teilchen bewegen', function(){
      if (uhr.laeuft()){ uhr.stop(); knopf.start.textContent = '▶ Teilchen bewegen'; return; }
      lief = true; zeichnen();
      if (WENIGER){ teil.forEach(function(p){ p.s += p.q * vMittel(B.wert('c')) * KPX * 0.8; }); teilchen(); return; }
      tAlt = 0; uhr.start(0); knopf.start.textContent = '❚❚ Anhalten'; }]]);
    var sim = {
      zustand: function(){ return { c: B.wert('c'), v: vMittel(B.wert('c')), lief: lief, besucht: besucht }; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ besucht = {}; B.zuruecksetzen(); },
      // Testhaken für Clipbilder: Temperatur c in °C, Zeit t in s (Lage der Teilchen allein aus der Zeit)
      zeige: function(c, t){ uhr.stop(); if (c != null) B.setze({ c: c }); var v = vMittel(B.wert('c'));
        teil.forEach(function(p){ p.s = p.q * v * KPX * (t || 0); }); zeichnen(); }
    };
    fig.__sim = sim;
    function lage(p){ return [refl(p.x0 + p.cx * p.s, R, BW - R), refl(p.y0 + p.cy * p.s, R, BH - R)]; }
    function teilchen(){
      leeren(box);
      el(box, 'rect', { x: 0, y: 0, width: BW, height: BH, 'class': 'box-grund' });
      teil.forEach(function(p, k){ if (k === MARK) return; var l = lage(p); el(box, 'circle', { cx: l[0], cy: l[1], r: R, 'class': 'teilchen' }); });
      var m = lage(teil[MARK]);
      el(box, 'circle', { cx: m[0], cy: m[1], r: R + 2.2, 'class': 'teilchen-mark' });
      el(box, 'circle', { cx: m[0], cy: m[1], r: 2, 'class': 'teilchen-kern' });
      el(box, 'rect', { x: 0, y: 0, width: BW, height: BH, 'class': 'box-rand' });
    }
    function zeichnen(){
      var c = B.wert('c'), v = vMittel(c);
      B.anzeigen(); teilchen(); leeren(dia);
      K = Achsen(dia, { w: 300, h: 140, x0: -215, x1: 335, y0: -95, y1: 900, sx: 50, sy: 100, xm: [-200, -100, 100, 200, 300], ym: [200, 400, 600, 800], xname: 'ϑ [°C]', yname: 'Tempo [m/s]' });
      K.kurve(vMittel, 'kurve-v', -150, 300);
      K.punkt(c, v, 'p-c');
      // Beschriftung auch unter der Kurve (rechts sind die Beschriftungen sonst zu breit für das Bild)
      K.etikett(c, v, '(' + grad(c) + '; ' + sig(v) + NB + 'm/s)', 'p-c', { kurven: [[vMittel, -150, 300]],
        wahl: [[8, -8, 'start'], [-8, -8, 'end'], [8, 17, 'start'], [-8, 17, 'end'], [50, 30, 'end'], [70, 44, 'end'], [-8, -24, 'end'], [-40, -8, 'end'], [-8, 34, 'end'], [8, 34, 'start']] });
      var z = '<span>Bei ' + v_('ϑ') + ' = ' + grad(c) + ' fliegen die Teilchen im Mittel mit ' + sig(v) + NB + 'm/s.</span>';
      z += '<span>Einzelne Teilchen: ◎ ' + sig(Q30[MARK] * v) + NB + 'm/s; das langsamste ' + sig(Q30[0] * v) + NB + 'm/s; das schnellste ' + sig(Q30[29] * v) + NB + 'm/s.</span>';
      z += '<span class="sim-notiz">Modell: Stickstoff, der Hauptteil der Luft. Die Stösse der Teilchen untereinander sind nicht gezeichnet.' + (WENIGER ? ' Weniger Bewegung: Jeder Klick auf «Teilchen bewegen» zeigt einen späteren Augenblick.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function bei(s, c){ return s.c === c; }
    pruefen = Leiste(fig, [
      { text: 'Lass die Teilchen laufen und stelle \\(40\\,^\\circ\\text{C}\\) ein. Sind alle Teilchen gleich schnell? Vergleiche das markierte Teilchen ◎ mit dem Mittel. Notiere, dann vergleiche.',
        ok: function(s){ return s.lief && bei(s, 40); },
        vergleich: 'Nein. Die Tempi reichen von rund \\(123\\;\\text{m/s}\\) bis \\(977\\;\\text{m/s}\\); ◎ fliegt mit \\(704\\;\\text{m/s}\\), schneller als das Mittel von \\(487\\;\\text{m/s}\\). Zur Temperatur gehört der Mittelwert über alle Teilchen, nicht das Tempo eines einzelnen.' },
      { text: 'Stelle \\(0\\,^\\circ\\text{C}\\) ein — bei dieser Temperatur gefriert Wasser. Stehen die Luftteilchen still? Notiere, was du abliest, und begründe.',
        ok: function(s){ return bei(s, 0); },
        vergleich: 'Nein: Bei \\(0\\,^\\circ\\text{C}\\) fliegen sie im Mittel mit \\(454\\;\\text{m/s}\\), kaum langsamer als bei \\(20\\,^\\circ\\text{C}\\). \\(0\\,^\\circ\\text{C}\\) ist nur der Nullpunkt der Celsius-Skala (der Schmelzpunkt des Wassers), kein Stillstand.' },
      { text: 'Bei welcher Temperatur fliegen die Teilchen im Mittel mit \\(500\\;\\text{m/s}\\)? Lies an der Kurve ab, dann stelle ein (auf \\(5\\,^\\circ\\text{C}\\) genau).',
        ok: function(s){ return s.c === 55 || s.c === 60; },
        vergleich: 'Bei rund \\(57\\,^\\circ\\text{C}\\): Der Regler zeigt bei \\(55\\,^\\circ\\text{C}\\) \\(498\\;\\text{m/s}\\) und bei \\(60\\,^\\circ\\text{C}\\) \\(502\\;\\text{m/s}\\).' },
      { text: 'Lies das mittlere Tempo bei \\(300\\,^\\circ\\text{C}\\) ab. Bei welcher Temperatur ist es nur halb so gross? Notiere deine Schätzung aus der Kurve, dann stelle ein.',
        ok: function(s){ return s.besucht[300] && Math.abs(s.v - vMittel(300) / 2) <= 0.02 * vMittel(300) / 2; },
        vergleich: 'Bei \\(300\\,^\\circ\\text{C}\\) rund \\(658\\;\\text{m/s}\\), die Hälfte sind \\(329\\;\\text{m/s}\\): Die Kurve erreicht sie bei rund \\(-130\\,^\\circ\\text{C}\\). Halbes Tempo heisst nicht halbe Celsius-Zahl (\\(150\\,^\\circ\\text{C}\\)) — die Kurve geht nicht durch den Nullpunkt der Celsius-Skala. Auch in Kelvin halbiert sich nicht einfach die Zahl: Halbes Tempo gehört zu einem Viertel der Kelvin-Temperatur (\\(573\\;\\text{K}\\) → \\(143\\;\\text{K}\\)), denn die mittlere Bewegungsenergie ist proportional zur Kelvin-Temperatur, das Tempo wächst langsamer.' },
      { text: 'Kühle so weit ab, wie die Simulation erlaubt. Was geschieht mit der Bewegung, wenn man noch weiter abkühlen könnte? Begründe mit der Kurve.',
        ok: function(s){ return bei(s, -150); },
        vergleich: 'Bei \\(-150\\,^\\circ\\text{C}\\) noch \\(305\\;\\text{m/s}\\). Je kälter, desto langsamer, und die Kurve fällt immer steiler. Es gibt eine tiefste Temperatur, bei der die Teilchenbewegung minimal ist: den absoluten Nullpunkt, \\(-273.15\\,^\\circ\\text{C}\\) (Kapitel 3). Die Simulation endet bei \\(-150\\,^\\circ\\text{C}\\), weil Stickstoff bei \\(-196\\,^\\circ\\text{C}\\) flüssig wird.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Drei Stoffe bei derselben Temperatur ----------
     Wasser, Brom und Essigsäure (Schmelz- und Siedepunkte wie Themenseite 5.1, Animation 2) in
     drei Boxen nebeneinander; darunter je Stoff eine Schiene mit den Bereichen fest, flüssig,
     gasförmig. Unterschied zur Themenseite: alle drei Stoffe zugleich bei derselben Temperatur,
     Aufträge zum Vergleichen in der Leiste. Genau am Schmelz- bzw. Siedepunkt zeigt die Box beide
     Zustände nebeneinander. Fest: Schwingen um feste Plätze; flüssig: dicht, verschiebbar;
     gasförmig: freier Flug, Tempo mit der Temperatur. Startwert 70 °C (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var boxen = g_(svg), schiene = g_(svg, { transform: 'translate(0,160)' });
    var STOFFE = [['Wasser', 0, 100], ['Brom', -7, 59], ['Essigsäure', 17, 118]];
    var BW = 92, BH = 112, GAP = 12, R = 4.6, C0 = -20, C1 = 130;
    var rnd = folge(23), part = [];
    // Grundlagen: Gitterplatz (fest, 4 × 4 unten in der Mitte); flüssig füllt den Boden der Box in drei
    // Reihen (6, 5, 5 Teilchen), beim Sieden zwei Reihen, beim Schmelzen eine Reihe über dem Gitter.
    function reihen(n, yUnten){ var l = [], r = 0; n.forEach(function(m){ for (var j = 0; j < m; j++)
      l.push([9 + (BW - 18) / (m - 1) * j + (rnd() - 0.5) * 5, yUnten - 15 * r + (rnd() - 0.5) * 5]); r++; }); return l; }
    for (var k = 0; k < 3; k++){
      var l = [], FL = reihen([6, 5, 5], BH - 8), SD = reihen([5, 5], BH - 8), SM = reihen([8], BH - 36);
      for (var i = 0; i < 16; i++){
        var w = rnd() * 2 * Math.PI;
        l.push({ gx: 25 + 14 * (i % 4), gy: BH - 8 - 14 * Math.floor(i / 4), fl: FL[i], sd: SD[i % 10], sm: SM[i % 8],
                 a1: rnd() * 6.3, a2: rnd() * 6.3, a3: rnd() * 6.3, w1: 0.8 + rnd() * 0.8, w2: 0.8 + rnd() * 0.8,
                 x0: R + rnd() * (BW - 2 * R), y0: R + rnd() * (BH - 2 * R), cx: Math.cos(w), cy: Math.sin(w), q: Q16[i], s: 0 });
      }
      part.push(l);
    }
    var lief = false, besucht = {}, pruefen = function(){}, zeit = 0, tAlt = 0;
    var B = Bedienung(fig, function(){ besucht[B.wert('c')] = true; zeichnen(); });
    var uhr = Uhr(function(t){ var dt = Math.min(0.1, t - tAlt); tAlt = t; vor(dt); boxenZeichnen(); });
    var knopf = aktionen(fig, [['start', '▶ Teilchen bewegen', function(){
      if (uhr.laeuft()){ uhr.stop(); knopf.start.textContent = '▶ Teilchen bewegen'; return; }
      lief = true; zeichnen();
      if (WENIGER){ vor(0.7); boxenZeichnen(); return; }
      tAlt = 0; uhr.start(0); knopf.start.textContent = '❚❚ Anhalten'; }],
      // Feinschritte: Der Regler hat 150 Stufen, auf dem Handy trifft der Finger keinen einzelnen Grad
      ['ab', '− 1 °C', function(){ schritt(-1); }], ['auf', '+ 1 °C', function(){ schritt(1); }]]);
    function schritt(d){ var inp = fig.querySelector('input[data-p="c"]'); inp.value = Math.max(C0, Math.min(C1, +inp.value + d)); inp.dispatchEvent(new Event('input', { bubbles: true })); }
    function zustand(k, c){ var s = STOFFE[k]; return c < s[1] ? 'fest' : c === s[1] ? 'schmilzt' : c < s[2] ? 'flüssig' : c === s[2] ? 'siedet' : 'gasförmig'; }
    function vor(dt){ var c = B.wert('c'); zeit += dt * vMittel(c) / vMittel(20);      // Schwingen und Gleiten lebhafter, je wärmer
      part.forEach(function(l){ l.forEach(function(p){ p.s += p.q * vMittel(c) * 0.12 * dt; }); }); }
    var sim = {
      zustand: function(){ var c = B.wert('c'); return { c: c, z: [0, 1, 2].map(function(k){ return zustand(k, c); }), lief: lief, besucht: besucht }; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ besucht = {}; B.zuruecksetzen(); },
      zeige: function(c, t){ uhr.stop(); if (c != null) B.setze({ c: c }); var v = vMittel(B.wert('c')); zeit = (t || 0) * v / vMittel(20);
        part.forEach(function(l){ l.forEach(function(p){ p.s = p.q * v * 0.12 * (t || 0); }); }); zeichnen(); }
    };
    fig.__sim = sim;
    // Lage eines Teilchens je nach Rolle; Amplituden wachsen mit der Temperatur
    // am Schmelzpunkt (gross) klein gehalten, damit das Gitter neben der Flüssigkeit erkennbar bleibt
    function fest(p, c, s, klein){ var a = klein ? 0.7 : 0.6 + 1.8 * Math.max(0, Math.min(1, (c - C0) / (s[1] - C0 + 1)));
      return [p.gx + a * Math.sin(11 * zeit + p.a1), p.gy + a * Math.sin(13 * zeit + p.a2)]; }
    function fluessig(b, p, ymin, ymax){ var x = b[0] + 6 * Math.sin(p.w1 * 2 * zeit + p.a1) + 3 * Math.sin(p.w2 * 9 * zeit + p.a3);
      var y = b[1] + 3 * Math.sin(p.w2 * 2.6 * zeit + p.a2) + 1.5 * Math.sin(p.w1 * 10 * zeit + p.a1);
      return [Math.max(R, Math.min(BW - R, x)), Math.max(ymin, Math.min(ymax, y))]; }
    function gas(p, ymax){ return [refl(p.x0 + p.cx * p.s, R, BW - R), refl(p.y0 + p.cy * p.s, R, ymax - R)]; }
    function boxenZeichnen(){
      var c = B.wert('c'); leeren(boxen);
      STOFFE.forEach(function(s, k){
        var gx = k * (BW + GAP), g = g_(boxen, { transform: 'translate(' + gx + ',14)', 'class': 'stoffbox stoff-' + k }), z = zustand(k, c);
        el(boxen, 'text', { x: gx + BW / 2, y: 9, 'text-anchor': 'middle', 'class': 'box-titel' }, s[0]);
        el(g, 'rect', { x: 0, y: 0, width: BW, height: BH, 'class': 'box-grund' });
        part[k].forEach(function(p, i){
          var l;
          if (z === 'fest') l = fest(p, c, s);
          else if (z === 'schmilzt') l = i < 8 ? fest(p, c, s, true) : fluessig(p.sm, p, BH - 44, BH - 32);       // unten zwei Gitterreihen, darüber Flüssigkeit
          else if (z === 'flüssig') l = fluessig(p.fl, p, BH - 42, BH - R);
          else if (z === 'siedet') l = i < 10 ? fluessig(p.sd, p, BH - 26, BH - R) : gas(p, BH - 34);           // unten Flüssigkeit, oben Dampf
          else l = gas(p, BH);
          el(g, 'circle', { cx: l[0], cy: l[1], r: R, 'class': 'teilchen' });
        });
        el(g, 'rect', { x: 0, y: 0, width: BW, height: BH, 'class': 'box-rand' });
        el(boxen, 'text', { x: gx + BW / 2, y: BH + 28, 'text-anchor': 'middle', 'class': 'box-zustand' }, z);
      });
    }
    function zeichnen(){
      var c = B.wert('c'); B.anzeigen(); boxenZeichnen(); leeren(schiene);
      var X = function(t){ return (t - C0) / (C1 - C0) * 300; };
      for (var t = C0; t <= C1; t += 10) el(schiene, 'line', { x1: X(t), y1: 0, x2: X(t), y2: 66, 'class': 'gitter' });
      STOFFE.forEach(function(s, k){
        var y = 4 + 21 * k;
        el(schiene, 'rect', { x: 0, y: y, width: X(s[1]), height: 13, 'class': 'zust-fest' });
        el(schiene, 'rect', { x: X(s[1]), y: y, width: X(s[2]) - X(s[1]), height: 13, 'class': 'zust-fl' });
        el(schiene, 'rect', { x: X(s[2]), y: y, width: 300 - X(s[2]), height: 13, 'class': 'zust-gas' });
        el(schiene, 'text', { x: 3, y: y + 10, 'class': 'zust-name' }, s[0]);
        el(schiene, 'text', { x: X(s[1]) + 2, y: y + 10, 'class': 'zust-zahl' }, minus(String(s[1])));
        el(schiene, 'text', { x: X(s[2]) + 2, y: y + 10, 'class': 'zust-zahl' }, minus(String(s[2])));
      });
      el(schiene, 'line', { x1: 0, y1: 66, x2: 300, y2: 66, 'class': 'achse' });
      for (t = C0; t <= C1; t += 30) el(schiene, 'text', { x: X(t), y: 79, 'text-anchor': t === C0 ? 'start' : t + 30 > C1 ? 'end' : 'middle', 'class': 'skala' }, minus(String(t)));
      el(schiene, 'text', { x: 300, y: 92, 'text-anchor': 'end', 'class': 'achsname' }, 'ϑ [°C]');
      el(schiene, 'text', { x: 0, y: 92, 'class': 'legende' }, 'dunkel: fest; mittel: flüssig; hell: gasförmig');
      el(schiene, 'line', { x1: X(c), y1: -2, x2: X(c), y2: 68, 'class': 'linie-c' });
      el(schiene, 'polygon', { points: X(c) + ',66 ' + (X(c) - 4) + ',72 ' + (X(c) + 4) + ',72', 'class': 'kopf-c' });
      var z = '<span>Bei ' + v_('ϑ') + ' = ' + grad(c) + ': ' + STOFFE.map(function(s, k){ return s[0] + ' ' + zustand(k, c); }).join('; ') + '.</span>';
      z += '<span class="sim-notiz">Schmelz- und Siedepunkte bei Normaldruck (1013' + NB + 'hPa).' + (WENIGER ? ' Weniger Bewegung: Jeder Klick auf «Teilchen bewegen» zeigt einen späteren Augenblick.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Lass die Teilchen laufen. Stelle eine Temperatur ein, bei der Wasser flüssig ist, Essigsäure aber noch fest. In welchem Bereich geht das? Notiere, dann vergleiche.',
        ok: function(s){ return s.lief && s.z[0] === 'flüssig' && s.z[2] === 'fest'; },
        vergleich: 'Zwischen \\(0\\,^\\circ\\text{C}\\) und \\(17\\,^\\circ\\text{C}\\): Wasser ist dort schon geschmolzen, Essigsäure noch nicht. Bei gleicher Temperatur sind verschiedene Stoffe in verschiedenen Zuständen.' },
      { text: 'Bei welchen Temperaturen sind alle drei Stoffe flüssig? Stelle eine solche Temperatur ein und notiere den ganzen Bereich.',
        ok: function(s){ return s.z.every(function(z){ return z === 'flüssig'; }); },
        vergleich: 'Über dem höchsten Schmelzpunkt (Essigsäure, \\(17\\,^\\circ\\text{C}\\)) und unter dem tiefsten Siedepunkt (Brom, \\(59\\,^\\circ\\text{C}\\)): also zwischen \\(17\\,^\\circ\\text{C}\\) und \\(59\\,^\\circ\\text{C}\\).' },
      { text: 'Stelle genau den Siedepunkt von Brom ein. Was zeigt die Brom-Box? Wie heisst der Übergang, wenn du weiter erwärmst, und wie heisst er umgekehrt?',
        ok: function(s){ return s.c === 59; },
        vergleich: 'Flüssigkeit unten und Dampf darüber, nebeneinander: Brom siedet. Erwärmt man weiter, verdampft alles (flüssig → gasförmig: verdampfen); umgekehrt heisst es kondensieren.' },
      { text: 'Erwärme so weit, dass zwei Stoffe gasförmig sind und einer noch flüssig. Welcher bleibt flüssig, und warum?',
        ok: function(s){ var g = s.z.filter(function(z){ return z === 'gasförmig'; }).length, f = s.z.filter(function(z){ return z === 'flüssig'; }).length; return g === 2 && f === 1; },
        vergleich: 'Zwischen \\(100\\,^\\circ\\text{C}\\) und \\(118\\,^\\circ\\text{C}\\): Wasser und Brom sind verdampft, Essigsäure siedet erst bei \\(118\\,^\\circ\\text{C}\\). Schmelz- und Siedepunkte gehören zum Stoff.' },
      { text: 'Kühle von \\(30\\,^\\circ\\text{C}\\) auf \\(-15\\,^\\circ\\text{C}\\) ab. Welche Übergänge siehst du, in welcher Reihenfolge, und was tun die Teilchen dabei?',
        ok: function(s){ return s.besucht[30] && s.c === -15; },
        vergleich: 'Zuerst erstarrt Essigsäure (bei \\(17\\,^\\circ\\text{C}\\)), dann Wasser (bei \\(0\\,^\\circ\\text{C}\\)), zuletzt Brom (bei \\(-7\\,^\\circ\\text{C}\\)). Beim Erstarren finden die Teilchen feste Plätze und schwingen nur noch um sie.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Gasthermometer ----------
     Ein Glaskolben mit Gas (Volumen fest) steht in einem Bad; ein Manometer zeigt den Druck.
     «Messen» trägt den Punkt (ϑ; p) ins Diagramm ein, «Gerade verlängern» zieht die Gerade durch
     die Messpunkte bis zum Druck null. Gas A: 1000 hPa bei 0 °C, Gas B: 600 hPa bei 0 °C;
     p = p(0 °C) · (ϑ + 273.15) / 273.15 (ideales Gas). Die Bäder bei 0 °C und 100 °C sind die
     Fixpunkte der Celsius-Skala (Eiswasser, siedendes Wasser bei Normaldruck). Unterschied zur
     Themenseite (Animation 5): Messpunkte selbst aufnehmen, Bäder als Fixpunkte, Druck in hPa,
     Zielaufgaben. Clipbilder: 20 °C und 70 °C mit Gas A. Startwert 50 °C (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,176)' }), K = null;
    var P0 = { A: 1000, B: 600 }, punkte = { A: [], B: [] }, neu = [], verl = false, pruefen = function(){};
    var B = Bedienung(fig, function(){ zeichnen(); });
    function druck(c, g){ return P0[g] * (c + T0) / T0; }
    var knopf = aktionen(fig, [
      ['messen', '● Messen', function(){ var c = B.wert('c'), g = B.wert('gas'), p = druck(c, g);
        if (!punkte[g].some(function(q){ return q[0] === c; })) punkte[g].push([c, p]);
        neu.push([g, c, p]); zeichnen(); }],
      ['gerade', '📏 Gerade verlängern', function(){ verl = !verl; zeichnen(); }],
      ['loeschen', '↺ Messreihe löschen', function(){ punkte = { A: [], B: [] }; neu = []; verl = false; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var c = B.wert('c'), g = B.wert('gas'); return { c: c, gas: g, p: druck(c, g), punkte: punkte, neu: neu, verl: verl }; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ B.setze(o); zeichnen(); },
      aufraeumen: function(){ neu = []; verl = false; B.zuruecksetzen(); },
      // Testhaken für Clipbilder: Messpunkte [[ϑ, Gas], …], Bad ϑ, Gerade ja/nein
      zeige: function(liste, c, g, gerade){ punkte = { A: [], B: [] };
        (liste || []).forEach(function(m){ punkte[m[1]].push([m[0], druck(m[0], m[1])]); });
        B.setze({ c: c, gas: g || 'A' }); verl = !!gerade; zeichnen(); }
    };
    fig.__sim = sim;
    // Gerade durch die Messpunkte eines Gases (Ausgleichsgerade; im Modell liegen alle Punkte genau darauf)
    function gerade(l){
      if (l.length < 2) return null;
      var n = l.length, sx = 0, sy = 0, sxx = 0, sxy = 0;
      l.forEach(function(q){ sx += q[0]; sy += q[1]; sxx += q[0] * q[0]; sxy += q[0] * q[1]; });
      var d = n * sxx - sx * sx; if (Math.abs(d) < 1e-9) return null;
      var m = (n * sxy - sx * sy) / d, b = (sy - m * sx) / n;
      return { m: m, b: b, null: -b / m, von: Math.min.apply(null, l.map(function(q){ return q[0]; })), bis: Math.max.apply(null, l.map(function(q){ return q[0]; })) };
    }
    function bad(c){ return c === 0 ? 'Eiswasser' : c === 100 ? 'siedendes Wasser' : c < 0 ? 'Kältebad' : c < 100 ? 'Wasserbad' : 'Ölbad'; }
    function zeichnen(){
      var c = B.wert('c'), g = B.wert('gas'), p = druck(c, g);
      B.anzeigen(); leeren(szene); leeren(dia);
      knopf.gerade.classList.toggle('an', verl); knopf.gerade.setAttribute('aria-pressed', verl);
      // Bad mit Kolben
      el(szene, 'rect', { x: 6, y: 66, width: 130, height: 80, rx: 4, 'class': 'bad' + (c < 0 ? ' kalt' : c > 100 ? ' oel' : '') });
      el(szene, 'line', { x1: 6, y1: 72, x2: 136, y2: 72, 'class': 'badlinie' });
      el(szene, 'path', { d: 'M6 60 V146 H136 V60', 'class': 'gefaess' });
      if (c === 0){ [[18, 74], [104, 77], [60, 76]].forEach(function(e){ el(szene, 'rect', { x: e[0], y: e[1], width: 14, height: 12, rx: 2, 'class': 'eis' }); }); }
      if (c === 100){ [[20, 130], [30, 100], [112, 120], [120, 92], [100, 84], [24, 82]].forEach(function(e){ el(szene, 'circle', { cx: e[0], cy: e[1], r: 3.2, 'class': 'blase' }); }); }
      el(szene, 'rect', { x: 67, y: 26, width: 8, height: 64, 'class': 'glas' });
      el(szene, 'circle', { cx: 71, cy: 112, r: 26, 'class': 'glas' });
      var rr = folge(5), nGas = g === 'A' ? 10 : 6;
      for (var i = 0; i < nGas; i++){ var w = rr() * 6.283, d = 4 + rr() * 17; el(szene, 'circle', { cx: 71 + d * Math.cos(w), cy: 112 + d * Math.sin(w), r: 2.6, 'class': 'teilchen' }); }
      el(szene, 'path', { d: 'M71 26 V16 H196 V36', 'class': 'rohr-linie' });
      el(szene, 'rect', { x: 160, y: 36, width: 132, height: 52, rx: 6, 'class': 'messgeraet' });
      el(szene, 'text', { x: 226, y: 52, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Druck im Kolben');
      el(szene, 'text', { x: 226, y: 76, 'text-anchor': 'middle', 'class': 'bt-druck' }, Math.round(p) + NB + 'hPa');
      el(szene, 'text', { x: 71, y: 162, 'text-anchor': 'middle', 'class': 'bt-meldung' }, bad(c) + ': ' + grad(c));
      el(szene, 'text', { x: 226, y: 104, 'text-anchor': 'middle', 'class': 'bt-klein' }, g === 'A' ? 'Gas A (mehr Gas)' : 'Gas B (weniger Gas)');
      // Diagramm p über ϑ
      K = Achsen(dia, { w: 300, h: 160, x0: -315, x1: 225, y0: -180, y1: 2000, sx: 50, sy: 250, xm: [-300, -200, -100, 100, 200], ym: [500, 1000, 1500], xname: 'ϑ [°C]', yname: 'p [hPa]' });
      var z = '<span>' + bad(c) + ' mit ' + v_('ϑ') + ' = ' + grad(c) + ': Druck im Kolben ' + v_('p') + ' = ' + Math.round(p) + NB + 'hPa (' + (g === 'A' ? 'Gas A' : 'Gas B') + ').</span>';
      var nulls = [];
      ['A', 'B'].forEach(function(gg){
        var ge = gerade(punkte[gg]);
        if (ge && verl){
          K.kurve(function(x){ return ge.m * x + ge.b; }, 'kurve-druck ext', ge.null, ge.von);
          K.kurve(function(x){ return ge.m * x + ge.b; }, 'kurve-druck', ge.von, Math.max(ge.bis, ge.von + 1));
          nulls.push([gg, ge.null]);
        }
      });
      ['A', 'B'].forEach(function(gg){ punkte[gg].forEach(function(q){
        if (gg === 'A') el(K.ebene, 'circle', { cx: K.X(q[0]), cy: K.Y(q[1]), r: 3.6, 'class': 'p-druck' });
        else el(K.ebene, 'rect', { x: K.X(q[0]) - 3.4, y: K.Y(q[1]) - 3.4, width: 6.8, height: 6.8, 'class': 'p-druck' }); }); });
      el(K.ebene, 'circle', { cx: K.X(c), cy: K.Y(p), r: 5.5, 'class': 'p-offen' });
      if (nulls.length){
        el(K.ebene, 'circle', { cx: K.X(nulls[0][1]), cy: K.Y(0), r: 4.2, 'class': 'p-k' });
        el(K.ebene, 'text', { x: K.X(nulls[0][1]) - 2, y: K.Y(0) - 9, 'text-anchor': 'start', 'class': 'p-text p-k' }, 'p = 0 bei ≈ ' + grad(Math.round(nulls[0][1])));
        nulls.forEach(function(n){ z += '<span>Die Gerade durch die Messpunkte von Gas ' + n[0] + ' trifft ' + v_('p') + ' = 0 bei ' + v_('ϑ') + ' ≈ ' + grad(Math.round(n[1])) + '.</span>'; });
      } else if (verl) z += '<span>Für eine Gerade braucht es mindestens zwei Messpunkte desselben Gases.</span>';
      el(K.ebene, 'text', { x: 300, y: 152 + 26, 'text-anchor': 'end', 'class': 'legende' }, '● Gas A   ■ Gas B   ○ jetzt im Bad');
      z += '<span class="sim-notiz">Das Volumen des Kolbens bleibt gleich. Messpunkte: Gas A ' + punkte.A.length + ', Gas B ' + punkte.B.length + '.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function gemessen(s, g, c){ return s.neu.some(function(m){ return (!g || m[0] === g) && m[1] === c; }); }
    pruefen = Leiste(fig, [
      { text: 'Miss den Druck in den beiden Bädern, die Anders Celsius als Fixpunkte seiner Skala wählte (gleiches Gas). Welche Bäder sind es, und warum gerade sie?',
        ok: function(s){ return ['A', 'B'].some(function(g){ return gemessen(s, g, 0) && gemessen(s, g, 100); }); },
        vergleich: 'Eiswasser (\\(0\\,^\\circ\\text{C}\\)) und siedendes Wasser (\\(100\\,^\\circ\\text{C}\\), bei Normaldruck). Beide lassen sich überall mit Wasser herstellen, und ihre Temperatur bleibt fest, solange Eis schmilzt bzw. Wasser siedet: gut wiederholbar.' },
      { text: 'Lass die Gerade durch deine Messpunkte bis zum Druck null verlängern. Bei welcher Temperatur trifft sie die Achse? Notiere.',
        ok: function(s){ return s.verl && ['A', 'B'].some(function(g){ return gerade(s.punkte[g]); }); },
        vergleich: 'Bei rund \\(-273\\,^\\circ\\text{C}\\), genau bei \\(-273.15\\,^\\circ\\text{C}\\). Kälter kann das Gas nicht werden: Sein Druck wäre sonst negativ.' },
      { text: 'Wechsle zur kleineren Gasmenge B, miss bei zwei Temperaturen und verlängere die Gerade. Bei welcher Temperatur zeigt Gas B \\(700\\;\\text{hPa}\\)? Lies ab, dann miss dort (auf \\(5\\,^\\circ\\text{C}\\) genau).',
        ok: function(s){ return s.verl && s.punkte.B.length >= 2 && (gemessen(s, 'B', 45) || gemessen(s, 'B', 50)); },
        vergleich: 'Bei rund \\(46\\,^\\circ\\text{C}\\): gemessen \\(699\\;\\text{hPa}\\) bei \\(45\\,^\\circ\\text{C}\\) und \\(710\\;\\text{hPa}\\) bei \\(50\\,^\\circ\\text{C}\\). Die Gerade von Gas B ist flacher als die von Gas A, trifft die Achse aber an derselben Stelle, bei rund \\(-273\\,^\\circ\\text{C}\\): Der Nullpunkt hängt nicht von der Gasmenge ab.' },
      { text: 'Bei welcher Temperatur hat Gas A nur noch halb so viel Druck wie bei \\(0\\,^\\circ\\text{C}\\)? Lies an der verlängerten Geraden ab, dann miss dort (auf \\(5\\,^\\circ\\text{C}\\) genau).',
        ok: function(s){ return gemessen(s, 'A', -135) || gemessen(s, 'A', -140); },
        vergleich: 'Halber Druck liegt auf halbem Weg zwischen \\(-273.15\\,^\\circ\\text{C}\\) und \\(0\\,^\\circ\\text{C}\\): bei rund \\(-137\\,^\\circ\\text{C}\\) (\\(500\\;\\text{hPa}\\)). Gemessen ergeben \\(-135\\,^\\circ\\text{C}\\) \\(506\\;\\text{hPa}\\) und \\(-140\\,^\\circ\\text{C}\\) \\(487\\;\\text{hPa}\\). Vom absoluten Nullpunkt aus gezählt ist der Abstand halbiert: Der Druck ist proportional zur Temperatur, wenn man sie dort beginnen lässt.' },
      { text: 'Miss bei der tiefsten Temperatur der Simulation. Warum kann es keine Temperatur unter \\(-273.15\\,^\\circ\\text{C}\\) geben? Begründe mit dem Druck und mit den Teilchen.',
        ok: function(s){ return gemessen(s, null, -200); },
        vergleich: 'Bei \\(-200\\,^\\circ\\text{C}\\) hat Gas A noch \\(268\\;\\text{hPa}\\). Unter \\(-273.15\\,^\\circ\\text{C}\\) müsste der Druck negativ werden — das gibt es nicht. Die Teilchen bewegen sich dort so wenig wie überhaupt möglich: Das ist der absolute Nullpunkt, der Nullpunkt der Kelvin-Skala.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Temperaturverlauf mit zwei Skalen ----------
     Ein Datenlogger zeichnet eine Temperatur über der Zeit: links die Celsius-, rechts die
     Kelvin-Skala (gleiche Schritte, Nullpunkt um 273.15 verschoben). Zwei Zeitpunkte t₁ und t₂
     mit Δϑ (links) und ΔT (rechts) als gleich lange Klammern. Tee: ϑ = 22 °C + 68 °C · e^(−t/12 min);
     Wintertag: ϑ = −2 °C + 6 °C · sin(2π (t − 8 h)/24 h), Minimum −8 °C um 2 h, Maximum 4 °C um 14 h
     (Modellkurven, nur zum Ablesen). Werte: ϑ auf 0.1 °C, T = ϑ + 273.15 aus dem gerundeten ϑ.
     Unterschied zur Themenseite (Animationen 3 und 4): Messkurve mit zwei Achsen, Zeitpunkte
     statt Temperaturen als Regler, Aufträge in der Leiste. Startwerte Tee 5 min und 20 min. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var dia = g_(svg, { transform: 'translate(34,4)' }), K = null, pruefen = function(){}, sz = null;
    var SZ = {
      tee: { f: function(t){ return 22 + 68 * Math.exp(-t / 12); }, max: 40, step: 1, u: 'min', t1: 5, t2: 20, y0: 15, y1: 95, sy: 5, ym: [20, 30, 40, 50, 60, 70, 80, 90], kt: [300, 320, 340, 360], sx: 5, xm: [10, 20, 30, 40], name: 'Tee in der Tasse' },
      winter: { f: function(t){ return -2 + 6 * Math.sin(2 * Math.PI * (t - 8) / 24); }, max: 24, step: 0.5, u: 'h', t1: 6, t2: 18, y0: -10, y1: 6, sy: 1, ym: [-10, -8, -6, -4, -2, 0, 2, 4, 6], kt: [264, 266, 268, 270, 272, 274, 276, 278], sx: 2, xm: [6, 12, 18, 24], name: 'Wintertag' }
    };
    var B = Bedienung(fig, function(){ if (B.wert('sz') !== sz) wechsle(B.wert('sz')); zeichnen(); });
    // Ein Umschalter wechselt die Bedeutung der Regler: Bereich, Schritt, Wert und Einheit mitsetzen (HOWTO §16)
    function wechsle(w){
      sz = w; var S = SZ[w];
      ['t1', 't2'].forEach(function(p){ var inp = fig.querySelector('input[data-p="' + p + '"]');
        inp.min = 0; inp.max = S.max; inp.step = S.step; inp.value = S[p]; inp.dataset.einheit = S.u; inp.dataset.stellen = S.step < 1 ? 1 : 0; });
    }
    function r1(x){ return Math.round(x * 10) / 10; }
    function werte(){ var S = SZ[B.wert('sz')], t1 = B.wert('t1'), t2 = B.wert('t2'), c1 = r1(S.f(t1)), c2 = r1(S.f(t2));
      return { sz: B.wert('sz'), t1: t1, t2: t2, c1: c1, c2: c2, T1: c1 + T0, T2: c2 + T0, d: r1(c2 - c1) }; }
    var sim = {
      zustand: function(){ return werte(); },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ if (o.sz && o.sz !== sz){ B.setze({ sz: o.sz }); wechsle(o.sz); } B.setze(o); zeichnen(); },
      aufraeumen: function(){ B.zuruecksetzen(); },
      zeige: function(w, t1, t2){ sim.setze({ sz: w, t1: t1, t2: t2 }); }
    };
    fig.__sim = sim;
    function f1(x){ return fest(x, 1); }
    function f2(x){ return fest(x, 2); }
    function zeichnen(){
      var w = werte(), S = SZ[w.sz], W = 236, H = 190;
      B.anzeigen(); leeren(dia);
      K = Achsen(dia, { w: W, h: H, x0: 0, x1: S.max * 1.06, y0: S.y0, y1: S.y1 + (S.y1 - S.y0) * 0.06, ya: S.y0, sx: S.sx, sy: S.sy, xm: S.xm, ym: S.ym, xname: 't [' + S.u + ']', yname: 'ϑ [°C]' });
      // rechte Achse in Kelvin: dieselben Schritte, um 273.15 verschoben
      var xr = W - 2;
      el(dia, 'line', { x1: xr, y1: K.Y(S.y0), x2: xr, y2: 0, 'class': 'achse-k' });
      S.kt.forEach(function(T){ var y = K.Y(T - T0); el(dia, 'line', { x1: xr - 4, y1: y, x2: xr + 4, y2: y, 'class': 'achse-k' });
        el(dia, 'text', { x: xr + 6, y: y + 3.5, 'class': 'skala skala-k' }, T); });
      el(dia, 'text', { x: xr + 4, y: -2 + 9, 'text-anchor': 'end', 'class': 'achsname achsname-k' }, 'T [K]');
      K.kurve(S.f, 'kurve-v', 0, S.max);
      // Hilfslinien von den Punkten zu beiden Achsen
      [[w.t1, w.c1], [w.t2, w.c2]].forEach(function(q){
        el(K.ebene, 'line', { x1: 0, y1: K.Y(q[1]), x2: xr, y2: K.Y(q[1]), 'class': 'hilfslinie fuehrung' }); });
      // Klammern Δϑ (links) und ΔT (rechts), gleich lang
      var ya = K.Y(w.c1), yb = K.Y(w.c2), ym = Math.abs(yb - ya) > 26 ? (ya + yb) / 2 : Math.max(ya, yb) + 22;   // kurze Klammer: Text darunter
      if (Math.abs(yb - ya) > 3){
        pfeil(K.ebene, 10, ya, 10, yb, 'pf-delta', 6); pfeil(K.ebene, xr - 10, ya, xr - 10, yb, 'pf-delta', 6);
        el(K.ebene, 'text', { x: 15, y: ym + 4, 'class': 'p-text p-delta' }, 'Δϑ = ' + f1(w.d) + NB + '°C');
        el(K.ebene, 'text', { x: xr - 15, y: ym + 4, 'text-anchor': 'end', 'class': 'p-text p-delta' }, 'ΔT = ' + f1(w.d) + NB + 'K');
      }
      // Punktbeschriftungen weichen den Klammertexten und der steilen Kurve aus (auch weit rechts vom Punkt)
      var kv = [[S.f, 0, S.max]], bt = function(s){ return s.length * 6.3; }, bel = [];
      if (Math.abs(yb - ya) > 3){ var s1 = 'Δϑ = ' + f1(w.d) + ' °C', s2 = 'ΔT = ' + f1(w.d) + ' K';
        bel = [[13, ym - 8, 17 + bt(s1), ym + 7], [xr - 17 - bt(s2), ym - 8, xr - 13, ym + 7]]; }
      var wahl = [[8, -8, 'start'], [8, 17, 'start'], [-8, -8, 'end'], [-8, 17, 'end'], [30, 10, 'start'], [40, 24, 'start'],
                  [-8, -24, 'end'], [8, -24, 'start'], [8, 34, 'start'], [-8, 34, 'end'], [-8, -40, 'end'], [-8, -56, 'end'], [-8, 52, 'end'], [-40, 17, 'end'], [-40, 32, 'end']];
      K.punkt(w.t1, w.c1, 'p-c'); K.punkt(w.t2, w.c2, 'p-c');
      // der frühere Punkt beschriftet lieber links, der spätere rechts: Nahe Punkte bekommen getrennte Beschriftungen
      var links = [[-10, 4, 'end']].concat(wahl.filter(function(c){ return c[2] === 'end'; }), wahl.filter(function(c){ return c[2] !== 'end'; })),
          rechts = [[10, 4, 'start']].concat(wahl.filter(function(c){ return c[2] !== 'end'; }), wahl.filter(function(c){ return c[2] === 'end'; }));
      var nah_ = Math.abs(K.X(w.t2) - K.X(w.t1)) < 120 && Math.abs(yb - ya) < 40, frueh = w.t1 <= w.t2;
      K.etikett(w.t1, w.c1, '(' + zahl(w.t1) + NB + S.u + '; ' + f1(w.c1) + NB + '°C)', 'p-c', { kurven: kv, belegt: bel, wahl: nah_ ? (frueh ? links : rechts) : wahl });
      K.etikett(w.t2, w.c2, '(' + zahl(w.t2) + NB + S.u + '; ' + f1(w.c2) + NB + '°C)', 'p-c', { kurven: kv, belegt: bel, wahl: nah_ ? (frueh ? rechts : links) : wahl });
      var z = '<span>' + v_('T') + '₁ [K] = ' + v_('ϑ') + '₁ [°C] + 273.15 = ' + f1(w.c1) + ' + 273.15 = ' + f2(w.T1) + '</span>';
      z += '<span>' + v_('T') + '₂ [K] = ' + v_('ϑ') + '₂ [°C] + 273.15 = ' + f1(w.c2) + ' + 273.15 = ' + f2(w.T2) + '</span>';
      function ec(x){ var t = f1(x) + NB + '°C'; return x < 0 ? '(' + t + ')' : t; }
      z += '<span>Δ' + v_('ϑ') + ' = ' + v_('ϑ') + '₂ − ' + v_('ϑ') + '₁ = ' + f1(w.c2) + NB + '°C − ' + ec(w.c1) + ' = ' + f1(w.d) + NB + '°C</span>';
      z += '<span>Δ' + v_('T') + ' = ' + v_('T') + '₂ − ' + v_('T') + '₁ = ' + f2(w.T2) + NB + 'K − ' + f2(w.T1) + NB + 'K = ' + f1(w.d) + NB + 'K</span>';
      z += '<span class="sim-notiz">' + S.name + ' (Modellkurve). Links Celsius, rechts Kelvin.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    wechsle(B.wert('sz'));
    pruefen = Leiste(fig, [
      { text: 'Wintertag: Stelle \\(t_1\\) auf den kältesten Zeitpunkt. Lies die Temperatur in °C ab und rechne sie in Kelvin um. Stimmt die rechte Achse?',
        setup: function(s){ s.setze({ sz: 'winter' }); },
        ok: function(s){ return s.sz === 'winter' && s.t1 === 2; },
        vergleich: 'Um 2 Uhr: \\(-8.0\\,^\\circ\\text{C}\\). \\(T\\,[\\text{K}] = \\vartheta\\,[^\\circ\\text{C}] + 273.15 = -8.0 + 273.15 = 265.15\\). Vorsicht mit dem Minus: nicht \\(273.15 + 8\\). Auf der rechten Achse liegt der Punkt knapp über \\(265\\;\\text{K}\\).' },
      { text: 'Ab welcher Uhrzeit ist es wärmer als \\(273.15\\;\\text{K}\\)? Wie viel °C sind das? Stelle \\(t_2\\) auf die erste halbe Stunde darüber.',
        ok: function(s){ return s.sz === 'winter' && s.t2 === 9.5; },
        vergleich: '\\(273.15\\;\\text{K}\\) sind \\(0\\,^\\circ\\text{C}\\): \\(\\vartheta\\,[^\\circ\\text{C}] = T\\,[\\text{K}] - 273.15 = 0\\). Um 9 Uhr zeigt die Kurve noch \\(-0.4\\,^\\circ\\text{C}\\), um 9:30 Uhr \\(0.3\\,^\\circ\\text{C}\\).' },
      { text: 'Stelle \\(t_1 = 2\\;\\text{h}\\) und \\(t_2 = 14\\;\\text{h}\\). Wie gross ist die Temperaturänderung in °C und in K? Begründe, warum beide Zahlen gleich sind.',
        ok: function(s){ return s.sz === 'winter' && s.t1 === 2 && s.t2 === 14; },
        vergleich: '\\(\\Delta\\vartheta = 4.0\\,^\\circ\\text{C} - (-8.0\\,^\\circ\\text{C}) = 12.0\\,^\\circ\\text{C}\\), \\(\\Delta T = 277.15\\;\\text{K} - 265.15\\;\\text{K} = 12.0\\;\\text{K}\\). Beide Skalen haben gleich grosse Schritte; die \\(273.15\\) stecken in beiden Werten und fallen beim Subtrahieren weg. Die beiden Klammern sind gleich lang.' },
      { text: 'Tee: Stelle \\(t_1 = 0\\). Nach wie vielen Minuten ist der Tee \\(30\\;\\text{K}\\) kühler als zu Beginn? Stelle \\(t_2\\) ein (auf \\(1\\;\\text{min}\\) genau) und notiere \\(\\vartheta_2\\) und \\(T_2\\).',
        setup: function(s){ s.setze({ sz: 'tee' }); },
        ok: function(s){ return s.sz === 'tee' && s.t1 === 0 && s.t2 === 7; },
        vergleich: '\\(30\\;\\text{K}\\) kühler heisst \\(30\\,^\\circ\\text{C}\\) kühler: von \\(90\\,^\\circ\\text{C}\\) auf \\(60\\,^\\circ\\text{C}\\). Nach \\(7\\;\\text{min}\\) zeigt die Kurve \\(59.9\\,^\\circ\\text{C}\\), also \\(333.05\\;\\text{K}\\) (\\(\\Delta T = -30.1\\;\\text{K}\\)).' },
      { text: 'Ein Rezept verlangt: «auf unter \\(323\\;\\text{K}\\) abkühlen lassen». Ab welcher Minute ist das erreicht? Rechne zuerst in °C um, dann stelle \\(t_2\\) ein.',
        ok: function(s){ return s.sz === 'tee' && s.t2 === 11; },
        vergleich: '\\(\\vartheta\\,[^\\circ\\text{C}] = T\\,[\\text{K}] - 273.15 = 323 - 273.15 = 49.85\\), also knapp \\(50\\,^\\circ\\text{C}\\). Nach \\(10\\;\\text{min}\\) sind es noch \\(51.6\\,^\\circ\\text{C}\\) (\\(324.75\\;\\text{K}\\)), nach \\(11\\;\\text{min}\\) \\(49.2\\,^\\circ\\text{C}\\) (\\(322.35\\;\\text{K}\\)).' }
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
    // Feste Beispiele (Clips, Kontrollfragen, Leisten, Festhalten, Kapitelaufgaben, Gesamttest, Themenseite):
    // Zufallsübungen dürfen sie nicht treffen. Schlüssel je Typ aus den Werten, mit fest_() gebildet.
    function fest_(a){ return a.join('|'); }
    // Nur die festen Beispiele, die ein Generator überhaupt treffen kann (beim Bau mit allen Wertelisten
    // nachgerechnet): Die Wertelisten der übrigen Typen enthalten keine Werte aus Clips, Kontrollfragen,
    // Leisten, Festhalten, Aufgaben, Gesamttest oder Themenseite.
    var FEST = {
      'zustand': [fest_(['Sauerstoff', -200])]                                                                                                             // Kontrollfrage 1, Kapitel 2
    };
    function istFest(typ, a){ return (FEST[typ] || []).indexOf(fest_(a)) >= 0; }
    // Fehlermuster müssen verschiedene Zahlen ergeben (HOWTO §15): alle Werte paarweise 2 % auseinander
    function verschieden(l){ for (var i = 0; i < l.length; i++) for (var j = i + 1; j < l.length; j++) if (Math.abs(l[i] - l[j]) <= 0.02 * Math.max(Math.abs(l[i]), Math.abs(l[j]))) return false; return true; }
    var T0 = 273.15;
    function gr(x){ return tz(x) + '\\,^\\circ\\text{C}'; }                 // Celsius in LaTeX, wie Themenseite 5.1
    function kv(x){ return tz(x) + '\\;\\text{K}'; }
    function r2(x){ return Math.round(x * 100) / 100; }
    // Temperaturen: absolut auf 0.2 K genau (wer mit 273 statt 273.15 rechnet oder auf ganze Kelvin rundet, hat recht)
    function nahT(e, x){ return Math.abs(e - x) <= 0.2; }
    // Auswahl mit eigener Rückmeldung je falscher Antwort: optionen [[Text, richtig?, Rückmeldung, Stichwort]]
    function mischen(l){ var a = l.slice(); for (var i = a.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    var BUCHST = ['A', 'B', 'C'];

    // Kapitel 1: Aussagen zur Temperatur im Teilchenbild [Aussage, richtig?, Rückmeldung bei falscher Wahl, Stichwort]
    var AUSSAGEN = [
      ['Bei \\(0\\,^\\circ\\text{C}\\) stehen die Teilchen von Wasser still.', false, 'Bei \\(0\\,^\\circ\\text{C}\\) liegt nur der Nullpunkt der Celsius-Skala. Die Teilchen bewegen sich weiter; minimal wird die Bewegung erst am absoluten Nullpunkt, \\(-273.15\\,^\\circ\\text{C}\\).', 'Nullpunkt der Celsius'],
      ['Ein einzelnes Teilchen, das schneller ist als die anderen, hat eine höhere Temperatur.', false, 'Die Temperatur ist ein Mittelwert über sehr viele Teilchen. Ein einzelnes Teilchen hat keine Temperatur.', 'Mittelwert'],
      ['Erwärmt man ein Gas, bewegen sich seine Teilchen im Mittel schneller.', true, 'Höhere Temperatur heisst grössere mittlere Bewegungsenergie: Die Teilchen werden im Mittel schneller.', 'grössere mittlere'],
      ['In einem Eiswürfel bewegen sich die Teilchen nicht.', false, 'Auch in einem Festkörper bewegen sich die Teilchen: Sie schwingen um ihre festen Plätze.', 'schwingen'],
      ['Bei gleicher Temperatur sind alle Teilchen eines Gases gleich schnell.', false, 'Die Tempi sind verschieden: einige Teilchen sind viel schneller, andere langsamer. Gleich ist nur der Mittelwert.', 'verschieden'],
      ['Die Temperatur ist ein Mass für die mittlere Bewegungsenergie der Teilchen.', true, 'Genau so ist sie definiert: Je heftiger sich die Teilchen im Mittel bewegen, desto höher die Temperatur.', 'definiert'],
      ['Die Brown\'sche Bewegung zeigt, dass sich die Teilchen einer Flüssigkeit ständig bewegen.', true, 'Ein sichtbares Tröpfchen zittert, weil unsichtbare Teilchen es von allen Seiten anstossen — ohne Pause.', 'anstossen'],
      ['Kühlt man immer weiter ab, kann man die Temperatur beliebig weit senken.', false, 'Es gibt eine tiefste Temperatur: den absoluten Nullpunkt, \\(-273.15\\,^\\circ\\text{C}\\). Dort ist die Teilchenbewegung minimal.', 'tiefste'],
      ['Bei \\(60\\,^\\circ\\text{C}\\) bewegen sich die Luftteilchen im Mittel doppelt so schnell wie bei \\(30\\,^\\circ\\text{C}\\).', false, 'Wärmer heisst schneller, aber nicht im Verhältnis der Celsius-Zahlen: im Mittel \\(502\\;\\text{m/s}\\) gegen \\(479\\;\\text{m/s}\\).', 'Verhältnis'],
      ['Ein Zimmer kühlt über Nacht ab. Seine Luftteilchen bewegen sich danach im Mittel langsamer.', true, 'Tiefere Temperatur heisst kleinere mittlere Bewegungsenergie: Die Teilchen werden im Mittel langsamer.', 'kleinere mittlere'],
      ['Wenn man Wasser erwärmt, nimmt die Bewegung jedes einzelnen Teilchens zu.', false, 'Im Mittel nimmt sie zu. Einzelne Teilchen werden durch Stösse auch einmal langsamer — es zählt der Durchschnitt.', 'Durchschnitt'],
      ['Auch in einem Gletscher bei \\(-10\\,^\\circ\\text{C}\\) bewegen sich die Teilchen.', true, 'Erst am absoluten Nullpunkt, \\(-273.15\\,^\\circ\\text{C}\\), ist die Bewegung minimal; \\(-10\\,^\\circ\\text{C}\\) liegt weit darüber. Die Teilchen schwingen um ihre Plätze.', 'weit darüber']
    ];
    // Kapitel 1: Beobachtung → Erklärung im Teilchenbild [Beobachtung, [[Erklärung, richtig?, Rückmeldung, Stichwort] × 3]]
    var BEOBACHTUNGEN = [
      ['Ein Tropfen Lebensmittelfarbe verteilt sich in einem ruhigen Glas Wasser im Lauf einiger Stunden im ganzen Glas, ohne dass jemand rührt.',
       [['Die Wasserteilchen bewegen sich ständig und stossen die Farbteilchen in alle Richtungen.', true],
        ['Die Farbe ist leichter als Wasser und steigt nach oben.', false, 'Dann sammelte sie sich oben. Sie verteilt sich aber in alle Richtungen — was treibt sie überallhin?', 'alle Richtungen'],
        ['Das Wasser im Glas strömt im Kreis.', false, 'Niemand rührt — was bewegt sich trotzdem, und zwar in alle Richtungen?', 'Niemand rührt']]],
      ['Ein zugebundener Ballon liegt in der Sonne und wird praller.',
       [['Die Luftteilchen im Ballon bewegen sich heftiger und prallen stärker gegen die Hülle.', true],
        ['Die Luftteilchen werden in der Wärme grösser.', false, 'Die Teilchen selbst bleiben gleich gross. Was ändert sich an ihnen, wenn es wärmer wird?', 'gleich gross'],
        ['Durch die Hülle kommt Luft von aussen hinein.', false, 'Der Ballon ist zu; die Zahl der Teilchen bleibt gleich. Was tun dieselben Teilchen anders?', 'zu']]],
      ['Ein nasses Tuch trocknet an der warmen Heizung schneller als in einem kalten Keller.',
       [['An der Heizung sind mehr Wasserteilchen schnell genug, um das Tuch zu verlassen.', true],
        ['Die Heizung zieht die Wasserteilchen an.', false, 'Eine Heizung zieht nichts an. Wodurch können die Wasserteilchen das Tuch verlassen?', 'zieht nichts'],
        ['Im kalten Keller sind die Wasserteilchen schwerer.', false, 'Die Masse der Teilchen hängt nicht von der Temperatur ab. Was ändert sich mit der Temperatur?', 'Masse']]],
      ['Unter dem Mikroskop zittern in einem Wassertropfen winzige Tuschekörnchen ununterbrochen hin und her.',
       [['Unsichtbare Wasserteilchen stossen sie zufällig von allen Seiten an.', true],
        ['Das Licht des Mikroskops schiebt die Körnchen.', false, 'Auch bei schwachem Licht zittern sie gleich. Wer stösst sie an?', 'schwachem Licht'],
        ['Die Körnchen bewegen sich von selbst, wie Lebewesen.', false, 'Auch Tusche, Staub und Russ zittern — sie leben nicht. Was ist um sie herum?', 'leben nicht']]],
      ['Eine Pfütze trocknet auch bei \\(15\\,^\\circ\\text{C}\\), obwohl Wasser erst bei \\(100\\,^\\circ\\text{C}\\) siedet.',
       [['Einzelne Wasserteilchen sind viel schneller als der Durchschnitt und können entweichen.', true],
        ['Die Sonne erwärmt die Pfütze auf \\(100\\,^\\circ\\text{C}\\).', false, 'Auch im Schatten trocknet sie, ohne zu sieden. Sind alle Teilchen gleich schnell?', 'Schatten'],
        ['Der Boden saugt das ganze Wasser auf.', false, 'Auch eine Pfütze auf Asphalt verschwindet. Wohin gehen die Teilchen?', 'Asphalt']]],
      ['In einem geschlossenen Glaskasten ohne Luftzug steht ein offenes Fläschchen Parfüm. Nach einiger Zeit riecht man den Duft auch in der gegenüberliegenden Ecke.',
       [['Die bewegten Luftteilchen stossen die Duftteilchen zufällig in alle Richtungen weiter.', true],
        ['Die Glaswand zieht die Duftteilchen an.', false, 'Dann sammelte sich der Duft an der Wand. Er verteilt sich aber im ganzen Kasten — was treibt ihn?', 'Wand'],
        ['Die Nase zieht die Duftteilchen an.', false, 'Der Duft ist auch dort, wo niemand riecht. Was trägt ihn durch den Kasten?', 'niemand']]]
    ];

    // Kapitel 2: Stoffe mit Schmelz- und Siedepunkt bei Normaldruck (°C, gerundet)
    var STOFFE = [['Wasser', 0, 100], ['Ethanol', -114, 78], ['Quecksilber', -39, 357], ['Eisen', 1538, 2862], ['Blei', 327, 1749],
                  ['Stickstoff', -210, -196], ['Sauerstoff', -219, -183], ['Brom', -7, 59], ['Essigsäure', 17, 118], ['Zinn', 232, 2602]];
    function zst(s, c){ return c < s[1] ? 'fest' : c < s[2] ? 'flüssig' : 'gasförmig'; }
    function rund(c){ var a = Math.abs(c); return Math.round(c / (a >= 200 ? 10 : a >= 40 ? 5 : 1)) * (a >= 200 ? 10 : a >= 40 ? 5 : 1); }

    var TYPEN = {
      /* ----- Kapitel 1: Temperatur und Teilchenbewegung ----- */
      'aussage': { felder: ['w'], muster: 'Die Aussage ist {w:richtig|falsch}.',
        neu: function(){ var a = zufall(AUSSAGEN); return { w: a[1] ? 'richtig' : 'falsch', a: a, text: '«' + a[0] + '» Richtig oder falsch?' }; },
        pruefen: function(A, e){ return e.w === A.w ? null : A.a[2]; },
        fehler: function(A){ return [[{ w: A.w === 'richtig' ? 'falsch' : 'richtig' }, A.a[3]]]; },
        loesung: function(A){ return '\\text{' + A.w + '}'; },   // für pruef-formelsatz; angezeigt wird loesung_html
        loesung_html: function(A){ return '<b>' + A.w + '</b>: ' + A.a[2]; } },
      'beobachtung': { felder: ['w'], muster: 'Erklärung: {w:A|B|C}',
        neu: function(){
          var b = zufall(BEOBACHTUNGEN), o = mischen(b[1]), k = 0;
          o.forEach(function(x, i){ if (x[1]) k = i; });
          return { w: BUCHST[k], o: o, text: b[0] + ' Welche Erklärung im Teilchenbild passt?<br>' + o.map(function(x, i){ return '<b>' + BUCHST[i] + '</b> ' + x[0]; }).join('<br>') }; },
        pruefen: function(A, e){ if (e.w === A.w) return null; return A.o[BUCHST.indexOf(e.w)][2]; },
        fehler: function(A){ var l = []; A.o.forEach(function(x, i){ if (!x[1]) l.push([{ w: BUCHST[i] }, x[3]]); }); return l; },
        loesung: function(A){ return '\\text{' + A.w + '}'; },   // für pruef-formelsatz; angezeigt wird loesung_html
        loesung_html: function(A){ return '<b>' + A.w + '</b>: ' + A.o[BUCHST.indexOf(A.w)][0]; } },

      /* ----- Kapitel 2: Aggregatzustände ----- */
      'zustand': { felder: ['w'], muster: 'Zustand: {w:fest|flüssig|gasförmig}',
        neu: function(){
          var s, c, zone;
          do { s = zufall(STOFFE); zone = zufall([0, 1, 2]);
               c = zone === 0 ? s[1] - zufall([5, 15, 40, 80]) : zone === 1 ? s[1] + (s[2] - s[1]) * zufall([0.15, 0.4, 0.7, 0.9]) : s[2] + zufall([10, 30, 60, 150]);
               c = rund(c); } while (c <= -273 || c === s[1] || c === s[2] || zst(s, c) !== ['fest', 'flüssig', 'gasförmig'][zone] || istFest('zustand', [s[0], c]));
          return { w: zst(s, c), s: s, c: c,
            text: s[0] + ' schmilzt bei \\(' + gr(s[1]) + '\\) und siedet bei \\(' + gr(s[2]) + '\\) (Normaldruck). In welchem Zustand ist ' + s[0] + ' bei \\(' + gr(c) + '\\)?' }; },
        pruefen: function(A, e){
          if (e.w === A.w) return null;
          var minus_ = (A.c < 0 || A.s[1] < 0) ? ' Vorsicht mit dem Minus: Von zwei negativen Temperaturen ist die mit dem kleineren Betrag die wärmere.' : '';
          if (A.w === 'flüssig' && e.w === 'fest') return 'Fest ist der Stoff nur unter seinem Schmelzpunkt. Liegt \\(' + gr(A.c) + '\\) darunter?' + minus_;
          if (A.w === 'fest' && e.w === 'flüssig') return 'Flüssig wird der Stoff erst über seinem Schmelzpunkt. Liegt \\(' + gr(A.c) + '\\) darüber?' + minus_;
          if (A.w === 'fest' && e.w === 'gasförmig') return 'Schmelzpunkt und Siedepunkt verwechselt? Unter dem Schmelzpunkt ist der Stoff fest.' + minus_;
          if (A.w === 'gasförmig' && e.w === 'fest') return 'Schmelzpunkt und Siedepunkt verwechselt? Über dem Siedepunkt ist der Stoff gasförmig.';
          if (A.w === 'gasförmig') return 'Vergleiche mit dem Siedepunkt: Liegt \\(' + gr(A.c) + '\\) darüber, ist der Stoff gasförmig.' + ((A.c < 0 || A.s[2] < 0) ? ' Vorsicht mit dem Minus.' : '');
          return 'Gasförmig wird der Stoff erst über seinem Siedepunkt. Liegt \\(' + gr(A.c) + '\\) darüber?' + ((A.c < 0 || A.s[2] < 0) ? ' Vorsicht mit dem Minus.' : ''); },
        fehler: function(A){ return ['fest', 'flüssig', 'gasförmig'].filter(function(z){ return z !== A.w; }).map(function(z){
          var st = A.w === 'flüssig' ? (z === 'fest' ? 'unter seinem Schmelzpunkt' : 'über seinem Siedepunkt') : A.w === 'fest' ? (z === 'flüssig' ? 'erst über seinem Schmelzpunkt' : 'verwechselt') : (z === 'fest' ? 'verwechselt' : 'Siedepunkt');
          return [{ w: z }, st]; }); },
        loesung: function(A){ return '\\text{' + A.w + '}'; },   // für pruef-formelsatz; angezeigt wird loesung_html
        loesung_html: function(A){ return '\\(' + gr(A.c) + '\\) liegt ' + (A.w === 'fest' ? 'unter dem Schmelzpunkt \\(' + gr(A.s[1]) + '\\)' : A.w === 'flüssig' ? 'zwischen \\(' + gr(A.s[1]) + '\\) und \\(' + gr(A.s[2]) + '\\)' : 'über dem Siedepunkt \\(' + gr(A.s[2]) + '\\)') + ': <b>' + A.w + '</b>.'; } },
      'uebergang': { felder: ['w'], muster: 'Übergang: {w:schmelzen|erstarren|verdampfen|kondensieren}',
        neu: function(){
          var s, c1, c2, w;
          do { s = zufall(STOFFE); var welcher = zufall([1, 2]), auf = Math.random() < 0.5, p = s[welcher];
               var unten = rund(p - zufall([5, 12, 25])), oben = rund(p + zufall([5, 12, 25]));
               c1 = auf ? unten : oben; c2 = auf ? oben : unten;
               w = welcher === 1 ? (auf ? 'schmelzen' : 'erstarren') : (auf ? 'verdampfen' : 'kondensieren');
          } while (c1 <= -273 || c2 <= -273 || Math.min(c1, c2) < s[1] && Math.max(c1, c2) > s[2] || c1 === s[1] || c1 === s[2] || c2 === s[1] || c2 === s[2]
                   || (w === 'schmelzen' || w === 'erstarren') && Math.max(c1, c2) >= s[2] || (w === 'verdampfen' || w === 'kondensieren') && Math.min(c1, c2) <= s[1]
                   || istFest('uebergang', [s[0], c1, c2]));
          return { w: w, s: s, c1: c1, c2: c2,
            text: s[0] + ' (Schmelzpunkt \\(' + gr(s[1]) + '\\), Siedepunkt \\(' + gr(s[2]) + '\\)) wird von \\(' + gr(c1) + '\\) auf \\(' + gr(c2) + '\\) ' + (c2 > c1 ? 'erwärmt' : 'abgekühlt') + '. Welcher Übergang findet statt?' }; },
        pruefen: function(A, e){
          if (e.w === A.w) return null;
          var paar = { schmelzen: 'erstarren', erstarren: 'schmelzen', verdampfen: 'kondensieren', kondensieren: 'verdampfen' };
          if (paar[A.w] === e.w) return 'Richtung prüfen: Wird ' + (A.c2 > A.c1 ? 'erwärmt' : 'abgekühlt') + ', geht es ' + (A.c2 > A.c1 ? 'zum Zustand mit mehr Bewegung' : 'zum Zustand mit weniger Bewegung') + '. Fest → flüssig heisst schmelzen, flüssig → gasförmig verdampfen; umgekehrt erstarren und kondensieren.';
          return 'Welcher Punkt liegt zwischen \\(' + gr(A.c1) + '\\) und \\(' + gr(A.c2) + '\\): der Schmelzpunkt oder der Siedepunkt?'; },
        fehler: function(A){ var paar = { schmelzen: 'erstarren', erstarren: 'schmelzen', verdampfen: 'kondensieren', kondensieren: 'verdampfen' }, l = [[{ w: paar[A.w] }, 'Richtung']];
          ['schmelzen', 'erstarren', 'verdampfen', 'kondensieren'].forEach(function(z){ if (z !== A.w && z !== paar[A.w]) l.push([{ w: z }, 'Welcher Punkt']); }); return l; },
        loesung: function(A){ return '\\text{' + A.w + '}'; },   // für pruef-formelsatz; angezeigt wird loesung_html
        loesung_html: function(A){ var schm = A.w === 'schmelzen' || A.w === 'erstarren';
          return 'Zwischen \\(' + gr(A.c1) + '\\) und \\(' + gr(A.c2) + '\\) liegt der ' + (schm ? 'Schmelzpunkt' : 'Siedepunkt') + ' \\(' + gr(schm ? A.s[1] : A.s[2]) + '\\): <b>' + A.w + '</b> (' + { schmelzen: 'fest → flüssig', erstarren: 'flüssig → fest', verdampfen: 'flüssig → gasförmig', kondensieren: 'gasförmig → flüssig' }[A.w] + ').'; } },

      /* ----- Kapitel 3: Celsius und Kelvin ----- */
      'eichen': { felder: ['c'], muster: '<i>ϑ</i> = {c} °C',
        neu: function(){
          var x0, sp, c, x;
          do { x0 = zufall([1.5, 2, 2.4, 3.2, 4]); sp = zufall([15, 16, 18, 20, 24]); c = zufall([-15, -10, 12, 18, 25, 32, 45, 64, 75, 85]);
               x = Math.round((x0 + sp * c / 100) * 10) / 10; c = (x - x0) / sp * 100;
          } while (!verschieden([c, x / (x0 + sp) * 100, x / sp * 100, (x - x0) / (x0 + sp) * 100]) || Math.abs(c) < 5 || x < 0.5);   // Faden nie unter dem Rohranfang
          return { c: c, x0: x0, x100: +(x0 + sp).toFixed(1), x: x, sp: sp,
            text: 'Ein selbst gebautes Thermometer: In Eiswasser steht der Faden bei \\(' + tz(x0) + '\\;\\text{cm}\\), in siedendem Wasser (Normaldruck) bei \\(' + tz(+(x0 + sp).toFixed(1)) + '\\;\\text{cm}\\). Heute steht er bei \\(' + tz(x) + '\\;\\text{cm}\\). Welche Temperatur zeigt er an?' }; },
        pruefen: function(A, e){
          if (Math.abs(e.c - A.c) <= 0.2) return null;
          if (nah(e.c, A.x / A.x100 * 100, 0.01)) return 'Der Nullpunkt liegt nicht bei \\(0\\;\\text{cm}\\), sondern beim Eiswasser-Strich. Miss vom Eiswasser-Strich aus, und der Abstand zwischen den beiden Fixpunkten sind die \\(100\\) Schritte.';
          if (nah(e.c, A.x / A.sp * 100, 0.01)) return 'Miss vom Eiswasser-Strich aus: Zuerst \\(' + tz(A.x0) + '\\;\\text{cm}\\) abziehen.';
          if (nah(e.c, (A.x - A.x0) / A.x100 * 100, 0.01)) return 'Die \\(100\\) Schritte liegen zwischen den beiden Fixpunkten: \\(' + tz(A.x100) + '\\;\\text{cm} - ' + tz(A.x0) + '\\;\\text{cm}\\).';
          if (nah(e.c, -A.c, 0.01)) return 'Vorzeichen prüfen: Unter dem Eiswasser-Strich ist die Temperatur negativ, darüber positiv.';
          return 'Der Abstand vom Eiswasser-Strich, geteilt durch den Abstand der beiden Fixpunkte, mal \\(100\\,^\\circ\\text{C}\\).'; },
        fehler: function(A){ return [[{ c: String(A.x / A.x100 * 100) }, 'Eiswasser-Strich aus, und'], [{ c: String(A.x / A.sp * 100) }, 'abziehen'], [{ c: String((A.x - A.x0) / A.x100 * 100) }, 'zwischen den beiden Fixpunkten']]; },
        loesung: function(A){ return '\\vartheta = \\dfrac{' + tz(A.x) + '\\;\\text{cm} - ' + tz(A.x0) + '\\;\\text{cm}}{' + tz(A.x100) + '\\;\\text{cm} - ' + tz(A.x0) + '\\;\\text{cm}} \\cdot 100\\,^\\circ\\text{C} ' + (Math.abs(A.c - Math.round(A.c * 10) / 10) < 1e-9 ? '= ' : '\\approx ') + tz(Math.round(A.c * 10) / 10) + '\\,^\\circ\\text{C}'; } },
      'nullpunkt': { felder: ['c'], muster: '<i>ϑ</i><sub>0</sub> = {c} °C',
        neu: function(){
          var c1, c2, p0, p1, p2, n;
          // Messfehler höchstens ±0.1 % bei mindestens 60 K Spanne: das Ergebnis bleibt nahe −273 °C (rund ±2 K)
          do { c1 = zufall([5, 10, 15, 20]); c2 = zufall([80, 90, 100]); p0 = zufall([800, 950, 1013, 1200]);
               p1 = Math.round(p0 * (c1 + T0) / T0); p2 = Math.round(p0 * (c2 + T0) / T0 * (1 + zufall([-0.001, -0.0005, 0.0005, 0.001])));
               n = c1 - p1 * (c2 - c1) / (p2 - p1);
          } while (!verschieden([n, -n, c1 - p2 * (c2 - c1) / (p2 - p1), -p1 * (c2 - c1) / (p2 - p1), c1 - p1 * (p2 - p1) / (c2 - c1)]) || istFest('nullpunkt', [c1, c2]));
          return { c: n, c1: c1, c2: c2, p1: p1, p2: p2,
            text: 'Eine Gruppe misst mit einem Gasthermometer (Volumen fest): bei \\(' + gr(c1) + '\\) einen Druck von \\(' + tz(p1) + '\\;\\text{hPa}\\), bei \\(' + gr(c2) + '\\) \\(' + tz(p2) + '\\;\\text{hPa}\\). Wo trifft die verlängerte Gerade den Druck null?' }; },
        pruefen: function(A, e){
          // Der Literaturwert (−273.15 °C, auch −273 °C) gilt immer, mit Hinweis auf den eigenen Messwert;
          // sonst Toleranz 2 °C um den Wert aus den Messwerten
          if (Math.abs(e.c + T0) <= 0.2 || Math.abs(e.c + 273) <= 0.2) return Math.abs(A.c + T0) > 0.3
            ? { ok: true, text: 'Das ist der Literaturwert. Aus diesen Messwerten ergibt sich \\(' + gr(Math.round(A.c * 10) / 10) + '\\); die kleine Abweichung kommt vom Messfehler.' } : null;
          if (Math.abs(e.c - A.c) <= 2) return null;
          var m = (A.p2 - A.p1) / (A.c2 - A.c1);
          if (nah(e.c, -A.c)) return 'Vorzeichen: Die Gerade sinkt zum kälteren Ende hin; der Druck null liegt weit unter \\(0\\,^\\circ\\text{C}\\).';
          if (A.c1 !== 0 && nah(e.c, -A.p1 / m)) return 'So weit liegt der Schnittpunkt unter \\(' + gr(A.c1) + '\\) — nicht unter \\(0\\,^\\circ\\text{C}\\). Zieh die Strecke von \\(' + gr(A.c1) + '\\) ab.';
          if (nah(e.c, A.c1 - A.p2 / m)) return 'Von welchem Messpunkt aus rechnest du? Druck und Temperatur müssen zum selben Punkt gehören.';
          if (nah(e.c, A.c1 - A.p1 * m)) return 'Steigung umgekehrt: Die Gerade steigt um \\(\\dfrac{\\Delta p}{\\Delta\\vartheta}\\) hPa je °C; die Strecke bis zum Druck null ist \\(p_1\\) geteilt durch die Steigung.';
          return 'Steigung \\(\\dfrac{p_2 - p_1}{\\vartheta_2 - \\vartheta_1}\\), dann von \\(\\vartheta_1\\) aus so weit hinunter, bis der Druck null ist.'; },
        fehler: function(A){ var m = (A.p2 - A.p1) / (A.c2 - A.c1), l = [[{ c: String(-A.c) }, 'Vorzeichen'], [{ c: String(A.c1 - A.p2 / m) }, 'Messpunkt'], [{ c: String(A.c1 - A.p1 * m) }, 'umgekehrt']];
          if (A.c1 !== 0) l.push([{ c: String(-A.p1 / m) }, 'Zieh die Strecke']); return l; },
        loesung: function(A){ var m = (A.p2 - A.p1) / (A.c2 - A.c1);
          return '\\dfrac{\\Delta p}{\\Delta\\vartheta} = \\dfrac{' + tz(A.p2) + '\\;\\text{hPa} - ' + tz(A.p1) + '\\;\\text{hPa}}{' + gr(A.c2) + ' - ' + gr(A.c1) + '} \\approx ' + tz(+m.toPrecision(4)) + '\\;\\tfrac{\\text{hPa}}{^\\circ\\text{C}},\\quad \\vartheta_0 = \\vartheta_1 - \\dfrac{p_1}{\\Delta p/\\Delta\\vartheta} = ' + gr(A.c1) + ' - \\dfrac{' + tz(A.p1) + '\\;\\text{hPa}}{' + tz(+m.toPrecision(4)) + '\\;\\text{hPa}/^\\circ\\text{C}} \\approx ' + gr(Math.round(A.c)); } },
      'skala': { felder: ['w'], muster: 'Skala: {w:Celsius|Kelvin|gleich gut}',
        neu: function(){
          var s = zufall([
            ['Ein Wetterbericht nennt die Höchsttemperatur von morgen.', 'Celsius', { Kelvin: 'Möglich wäre es, aber im Alltag ist Celsius üblich: handliche Zahlen, \\(0\\,^\\circ\\text{C}\\) beim Gefrieren des Wassers.', 'gleich gut': 'Die Zahlen sind nicht gleich: \\(25\\,^\\circ\\text{C}\\) sind \\(298.15\\;\\text{K}\\). Welche Skala ist im Alltag üblich?' }],
            ['Ein Arzt misst Fieber.', 'Celsius', { Kelvin: 'Möglich wäre es, aber in der Medizin und im Alltag ist Celsius üblich.', 'gleich gut': 'Eine einzelne Temperatur hat in den beiden Skalen verschiedene Zahlen. Welche ist im Alltag üblich?' }],
            ['Um welchen Faktor wächst die mittlere Bewegungsenergie der Teilchen, wenn ein Gas wärmer wird?', 'Kelvin', { Celsius: 'Ein Verhältnis braucht einen echten Nullpunkt. Der Nullpunkt der Celsius-Skala ist willkürlich gewählt.', 'gleich gut': 'Verhältnisse sind in den beiden Skalen nicht gleich: \\(\\tfrac{30\\,^\\circ\\text{C}}{15\\,^\\circ\\text{C}} = 2\\), aber \\(\\tfrac{303.15\\;\\text{K}}{288.15\\;\\text{K}} \\approx 1.05\\).' }],
            ['Der Druck eines Gases in einem festen Behälter ist proportional zu seiner Temperatur.', 'Kelvin', { Celsius: 'Proportional heisst: bei null Temperatur null Druck. Der Druck wird null bei \\(-273.15\\,^\\circ\\text{C}\\), nicht bei \\(0\\,^\\circ\\text{C}\\).', 'gleich gut': 'Bei \\(0\\,^\\circ\\text{C}\\) hat das Gas noch Druck. Proportional ist er nur zur Temperatur ab dem absoluten Nullpunkt.' }],
            ['Flüssiges Helium siedet bei sehr tiefer Temperatur (Physiklabor).', 'Kelvin', { Celsius: 'Nahe am absoluten Nullpunkt sind Celsius-Werte unhandlich (\\(-268.95\\,^\\circ\\text{C}\\)); die Tieftemperaturforschung rechnet in Kelvin (\\(4.2\\;\\text{K}\\)).', 'gleich gut': 'Die Zahlen sind verschieden: \\(4.2\\;\\text{K}\\) sind \\(-268.95\\,^\\circ\\text{C}\\). Welche Skala zeigt den Abstand zum absoluten Nullpunkt direkt?' }],
            ['Die SI-Basiseinheit der Temperatur.', 'Kelvin', { Celsius: 'Das Grad Celsius ist eine abgeleitete Einheit. Die Basiseinheit im SI ist das Kelvin.', 'gleich gut': 'Nur eine der beiden ist die Basiseinheit des SI.' }],
            ['Eine Suppe wird um einen bestimmten Betrag erwärmt: Wie gross ist die Temperaturänderung?', 'gleich gut', { Celsius: 'Celsius geht — Kelvin aber genauso: Eine Differenz hat in beiden Skalen dieselbe Zahl.', Kelvin: 'Kelvin geht — nötig ist es aber nicht: Eine Differenz hat in beiden Skalen dieselbe Zahl.' }],
            ['Der Unterschied zwischen der Temperatur im Kühlteil und im Tiefkühlteil eines Kühlschranks.', 'gleich gut', { Celsius: 'Celsius geht — Kelvin aber genauso: Eine Differenz hat in beiden Skalen dieselbe Zahl.', Kelvin: 'Kelvin geht — nötig ist es aber nicht: Eine Differenz hat in beiden Skalen dieselbe Zahl.' }]
          ]);
          return { w: s[1], s: s, text: s[0] + ' Welche Skala nimmt man hier — Celsius, Kelvin, oder sind beide gleich gut?' }; },
        pruefen: function(A, e){ return e.w === A.w ? null : A.s[2][e.w]; },
        fehler: function(A){ return Object.keys(A.s[2]).map(function(k){ return [{ w: k }, A.s[2][k].split(' ').slice(0, 2).join(' ')]; }); },
        loesung: function(A){ return '\\text{' + A.w + '}'; },   // für pruef-formelsatz; angezeigt wird loesung_html
        loesung_html: function(A){ return '<b>' + A.w + '</b>' + (A.w === 'Celsius' ? ': im Alltag üblich.' : A.w === 'Kelvin' ? ': Hier zählt der Abstand vom absoluten Nullpunkt.' : ': Eine Temperaturdifferenz hat in beiden Skalen dieselbe Zahl.'); } },

      /* ----- Kapitel 4: Umrechnen und Temperaturdifferenz ----- */
      'umrechnen': { felder: ['x'], muster: function(A){ return A.nachK ? '<i>T</i> = {x} K' : '<i>ϑ</i> = {x} °C'; },
        neu: function(){
          var nachK = Math.random() < 0.5, c, w;
          if (nachK){
            do { c = zufall([['Im Kühlschrank sind es', [3, 5, 6, 7]], ['In der Sauna sind es', [80, 85, 90, 95]], ['In einer Winternacht in Samedan sind es', [-28, -22, -31]],
                             ['Im Pizzaofen sind es', [380, 420, 450]], ['Im Tiefkühler sind es', [-24, -22, -20]], ['An einer Lötspitze sind es', [330, 350, 380]],
                             ['Flüssiger Sauerstoff siedet bei', [-183]], ['Ethanol schmilzt bei', [-114]]]);
                 w = zufall(c[1]); } while (istFest('umrechnen', ['C', w]));
            return { nachK: true, x: w + T0, w: w, text: c[0] + ' \\(' + gr(w) + '\\). Wie viel Kelvin sind das?' };
          }
          do { c = zufall([['Der Glühdraht einer Lampe hat', [2700, 2800, 3000]], ['Die Oberfläche des Neptunmonds Triton hat rund', [38]], ['Die Luft an einem heissen Sommertag hat', [303, 306, 308]],
                           ['Ein Kühlschrank kühlt auf', [277, 278, 280]], ['Die Oberfläche der Venus hat rund', [737]], ['Der Mars hat im Mittel rund', [210]]]);
               w = zufall(c[1]); } while (istFest('umrechnen', ['K', w]));
          return { nachK: false, x: w - T0, w: w, text: c[0] + ' \\(' + kv(w) + '\\). Wie viel Grad Celsius sind das?' }; },
        pruefen: function(A, e){
          if (nahT(e.x, A.x)) return null;
          if (A.nachK){
            if (nahT(e.x, A.w - T0)) return 'Kelvin-Zahlen sind um \\(273.15\\) grösser als Celsius-Zahlen: \\(T\\,[\\text{K}] = \\vartheta\\,[^\\circ\\text{C}] + 273.15\\).';
            if (A.w < 0 && nahT(e.x, -A.w + T0)) return 'Vorsicht mit dem Minus: \\(' + tz(A.w) + ' + 273.15\\), nicht \\(273.15 + ' + tz(-A.w) + '\\).';
            if (e.x < 0) return 'Eine Temperatur in Kelvin ist nie negativ.';
            return '\\(T\\,[\\text{K}] = \\vartheta\\,[^\\circ\\text{C}] + 273.15\\).';
          }
          if (nahT(e.x, A.w + T0)) return 'Celsius-Zahlen sind um \\(273.15\\) kleiner als Kelvin-Zahlen: \\(\\vartheta\\,[^\\circ\\text{C}] = T\\,[\\text{K}] - 273.15\\).';
          if (A.w < T0 && nahT(e.x, T0 - A.w)) return 'Vorzeichen prüfen: Unter \\(273.15\\;\\text{K}\\) ist die Celsius-Temperatur negativ, \\(' + tz(A.w) + ' - 273.15\\).';
          return '\\(\\vartheta\\,[^\\circ\\text{C}] = T\\,[\\text{K}] - 273.15\\).'; },
        fehler: function(A){ if (A.nachK){ var l = [[{ x: String(A.w - T0) }, 'grösser als Celsius']]; if (A.w < 0) l.push([{ x: String(-A.w + T0) }, 'Minus']); return l; }
          var m = [[{ x: String(A.w + T0) }, 'kleiner als Kelvin']]; if (A.w < T0) m.push([{ x: String(T0 - A.w) }, 'Vorzeichen']); return m; },
        loesung: function(A){ return A.nachK ? 'T\\,[\\text{K}] = \\vartheta\\,[^\\circ\\text{C}] + 273.15 = ' + tz(A.w) + ' + 273.15 = ' + tz(r2(A.x))
                                             : '\\vartheta\\,[^\\circ\\text{C}] = T\\,[\\text{K}] - 273.15 = ' + tz(A.w) + ' - 273.15 = ' + tz(r2(A.x)); } },
      'differenz': { felder: ['x'], muster: 'Δ<i>T</i> = {x} K',
        neu: function(){
          var k, a, b, d;
          do { k = zufall([
                 ['Ein Werkstück aus Stahl wird im Ofen von %1 auf %2 erwärmt.', 'CC', [18, 20, 22], [180, 250, 420, 600]],
                 ['Ein Getränk kühlt im Kühlschrank von %1 auf %2 ab.', 'CC', [21, 24, 28], [5, 6, 7]],
                 ['Eine Probe wird im Labor von %1 auf %2 abgekühlt.', 'KK', [295, 300], [77.4, 120, 200]],
                 ['Ein Kühlakku aus dem Tiefkühler (%1) erwärmt sich in einer Tasche; ein Datenlogger zeigt danach %2.', 'CK', [-22, -20, -16], [268.15, 275.15, 281.15]],
                 ['Ein Krug Tee kühlt von %1 auf %2 ab.', 'KC', [358.15, 363.15], [35, 40, 45]]]);
               a = zufall(k[2]); b = zufall(k[3]);
               var Ta = k[1].charAt(0) === 'C' ? a + T0 : a, Tb = k[1].charAt(1) === 'C' ? b + T0 : b; d = Tb - Ta;
          } while (!verschieden([d, -d, d + T0, d - T0]) || Math.abs(d) < 3 || istFest('differenz', [a, b]));
          function zeig(v, art){ return art === 'C' ? '\\(' + gr(v) + '\\)' : '\\(' + kv(v) + '\\)'; }
          return { x: d, a: a, b: b, art: k[1], text: k[0].replace('%1', zeig(a, k[1].charAt(0))).replace('%2', zeig(b, k[1].charAt(1))) + ' Wie gross ist die Temperaturänderung \\(\\Delta T = T_2 - T_1\\) in Kelvin? (Abkühlen gibt ein negatives \\(\\Delta T\\).)' }; },
        pruefen: function(A, e){
          if (nahT(e.x, A.x)) return null;
          if (nahT(e.x, -A.x)) return 'Ende minus Anfang: \\(\\Delta T = T_2 - T_1\\). ' + (A.x < 0 ? 'Beim Abkühlen ist \\(\\Delta T\\) negativ.' : 'Beim Erwärmen ist \\(\\Delta T\\) positiv.');
          if (nahT(e.x, A.x + T0) || nahT(e.x, A.x - T0)) return A.art === 'CC' || A.art === 'KK' ? 'Bei einer Differenz fällt die \\(273.15\\) weg: \\(\\Delta T = \\Delta\\vartheta\\). Nichts dazuzählen.'
                                                                                              : 'Zuerst beide Temperaturen in dieselbe Skala bringen: Kelvin minus Celsius ergibt keine Differenz.';
          return '\\(\\Delta T = T_2 - T_1\\); beide Werte in derselben Skala.'; },
        fehler: function(A){ var st = A.art === 'CC' || A.art === 'KK' ? 'fällt die' : 'dieselbe Skala';
          return [[{ x: String(-A.x) }, 'Ende minus Anfang'], [{ x: String(A.x + T0) }, st], [{ x: String(A.x - T0) }, st]]; },
        loesung: function(A){
          var Ta = A.art.charAt(0) === 'C' ? A.a + T0 : A.a, Tb = A.art.charAt(1) === 'C' ? A.b + T0 : A.b;
          if (A.art === 'CC') return '\\Delta T = \\Delta\\vartheta = \\vartheta_2 - \\vartheta_1 = ' + gr(A.b) + ' - ' + (A.a < 0 ? '(' + gr(A.a) + ')' : gr(A.a)) + ' = ' + tz(r2(A.x)) + '\\;\\text{K}';
          return '\\Delta T = T_2 - T_1 = ' + kv(r2(Tb)) + ' - ' + kv(r2(Ta)) + ' = ' + tz(r2(A.x)) + '\\;\\text{K}'; } },
      'faktor': { felder: ['x'], muster: 'Faktor {x}',
        neu: function(){
          var a, b, Ta, Tb, f;
          do { a = zufall([-50, -20, 10, 25, 50, 80]); b = zufall([-80, 0, 40, 120, 200, 350, 500]);
               Ta = a + T0; Tb = b + T0; f = Tb / Ta;
          } while (a === b || Math.abs(f - 1) < 0.05 || !verschieden([f, b / a, Tb - Ta, Ta / Tb]) || istFest('faktor', [a, b]));
          return { x: f, a: a, b: b, text: 'Ein Gas in einem verschlossenen Behälter wird von \\(' + gr(a) + '\\) auf \\(' + gr(b) + '\\) ' + (b > a ? 'erwärmt' : 'abgekühlt') + '. Um welchen Faktor ändert sich die mittlere Bewegungsenergie seiner Teilchen?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.b / A.a)) return 'Ein Verhältnis braucht die Temperaturen in Kelvin: Der Nullpunkt der Celsius-Skala ist willkürlich.';
          if (nah(e.x, A.a / A.b) && A.b !== 0) return 'Ein Verhältnis braucht die Temperaturen in Kelvin — und neu durch alt.';
          if (nah(e.x, (A.a + T0) / (A.b + T0))) return 'Umgekehrt: Faktor = neu durch alt, \\(\\dfrac{T_2}{T_1}\\).';
          if (nah(e.x, A.b - A.a)) return 'Das ist die Temperaturänderung. Gefragt ist ein Faktor: \\(\\dfrac{T_2}{T_1}\\).';
          return 'Die mittlere Bewegungsenergie ist proportional zur Temperatur in Kelvin: Faktor \\(\\dfrac{T_2}{T_1}\\).'; },
        fehler: function(A){ return [[{ x: String(A.b / A.a) }, 'braucht die Temperaturen in Kelvin'], [{ x: String((A.a + T0) / (A.b + T0)) }, 'Umgekehrt'], [{ x: String(A.b - A.a) }, 'Temperaturänderung']]; },
        loesung: function(A){ return '\\dfrac{T_2}{T_1} = \\dfrac{' + kv(r2(A.b + T0)) + '}{' + kv(r2(A.a + T0)) + '} ' + erg(A.x, '').replace('\\;\\text{}', ''); } }
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
        var f = T.pruefen(A, e), extra = '';
        if (f && f.ok){ extra = ' ' + f.text; f = null; }
        if (f === null){
          serie = versuche === 1 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + extra + ' <button type="button" class="ue-weiter">Nächste</button>';
          rueck.querySelector('.ue-weiter').addEventListener('click', neu);
        } else {
          serie = 0; rueck.className = 'ue-rueck falsch';
          // Auswahlaufgaben geben ihre Lösung als Text (loesung_html), Rechenaufgaben als Formel
          rueck.innerHTML = (f || 'Noch nicht.') + (versuche >= 2 ? ' <details class="ue-loes"><summary>Lösung</summary>' + (T.loesung_html ? T.loesung_html(A) : '\\(' + T.loesung(A) + '\\)') + '</details>' : '');
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

})();
</script>
