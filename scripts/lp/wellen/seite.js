<script>
/* Leitprogramm Wellen — laufende Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr, Übungsrahmen,
   Minigrafen) wörtlich aus dem Leitprogramm Wärme (dort aus Hydrostatik); neu sind die sechs Simulationen
   (Teilchenkette, Momentbild und Zeitdiagramm, zwei Seile, Sender im Spektrum, Atom und Laser,
   Durchlässigkeit der Atmosphäre) und die Übungstypen für 6.1. Werte wie Themenseite 6.1: Schall in Luft
   (15 °C) 340 m/s, Helium 980, Wasser 1500, Eisen 5170 m/s; c = 3.00·10⁸ m/s im Vakuum; sichtbares Licht
   380 bis 780 nm. Farben (Farbe = eine Bedeutung): Welle und Auslenkung (Kurven, Teilchen der Welle, E-Feld)
   Bernstein, Ausbreitung und Front Grün, Licht der Sonne Orange, Wärmestrahlung und Infrarot Rot,
   Teilchen, markierte Punkte, Masslinien, Achsen und B-Feld Tinte bzw. Grau; Photonen in ihrer Spektralfarbe.
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
        if (s) s.textContent = (inp.dataset.stellen != null ? fest(+inp.value, +inp.dataset.stellen) : zahl(+inp.value)) + (inp.dataset.einheit ? NB + inp.dataset.einheit : '');   // gleich gerundet wie in Formelzeile und Bild   // wie in der Formelzeile: 1 h, nicht 1.00 h
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



  // Werte wie Themenseite 6.1
  var CL = 3.00e8;                                         // Lichtgeschwindigkeit im Vakuum, m/s
  var SCHALL = { 'Luft': 340, 'Helium': 980, 'Wasser': 1500, 'Eisen': 5170 };   // Luft bei 15 °C
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
  // Masslinie mit Spitzen an beiden Enden (λ, T, Abstände)
  function mass(eltern, x1, y, x2, text, cls){
    var m = (x1 + x2) / 2;
    pfeil(eltern, m, y, x1, y, 'mass', 5); pfeil(eltern, m, y, x2, y, 'mass', 5);
    if (text) el(eltern, 'text', { x: m, y: y - 4, 'text-anchor': 'middle', 'class': 'bt-wert ' + (cls || '') }, text);
  }
  function g_(eltern, attr){ return el(eltern, 'g', attr || {}); }
  function v_(s){ return '<i>' + s + '</i>'; }                     // Formelzeichen kursiv
  // Wellenlinie (Photon, Strahlung) von (x1, y1) nach (x2, y2) mit Spitze
  function wellig(eltern, x1, y1, x2, y2, cls, n, amp){
    var dx = x2 - x1, dy = y2 - y1, l = Math.hypot(dx, dy); if (l < 4) return;
    var ux = dx / l, uy = dy / l, d = '', k, N = Math.max(8, Math.round(l / 2)), w = n || Math.max(2, Math.round(l / 12));
    for (k = 0; k <= N; k++){ var q = k / N, s = (l - 7) * q, a = (amp == null ? 3.5 : amp) * Math.sin(2 * Math.PI * w * q);
      d += (k ? ' L' : 'M') + (x1 + ux * s - uy * a).toFixed(1) + ' ' + (y1 + uy * s + ux * a).toFixed(1); }
    el(eltern, 'path', { d: d, 'class': 'photon ' + cls });
    el(eltern, 'polygon', { points: x2 + ',' + y2 + ' ' + (x2 - ux * 8 - uy * 4) + ',' + (y2 - uy * 8 + ux * 4) + ' ' + (x2 - ux * 8 + uy * 4) + ',' + (y2 - uy * 8 - ux * 4), 'class': 'photon-kopf ' + cls });
  }
  // Spektralfarbe einer Wellenlänge in nm (380 bis 780 nm; ausserhalb grau bzw. dunkelrot für Infrarot)
  function spektralfarbe(nm){
    if (nm > 780) return '#8e2a20';
    if (nm < 380) return '#6b4fa0';
    var r, g, b;
    if (nm < 440){ r = (440 - nm) / 60; g = 0; b = 1; }
    else if (nm < 490){ r = 0; g = (nm - 440) / 50; b = 1; }
    else if (nm < 510){ r = 0; g = 1; b = (510 - nm) / 20; }
    else if (nm < 580){ r = (nm - 510) / 70; g = 1; b = 0; }
    else if (nm < 645){ r = 1; g = (645 - nm) / 65; b = 0; }
    else { r = 1; g = 0; b = 0; }
    return 'rgb(' + Math.round(r * 215) + ',' + Math.round(g * 190) + ',' + Math.round(b * 215) + ')';
  }
  // n signifikante Stellen mit Nullen am Ende (0.060, 6.0, 3.00·10⁸): für gegebene Messwerte und was aus ihnen folgt
  function sz(x, n){
    var a = Math.abs(x); if (a === 0) return '0';
    if (a >= 1e4 || a < 1e-2){ var k = Math.floor(Math.log10(a)), m = a / Math.pow(10, k);
      if (+m.toFixed(n - 1) >= 10){ m /= 10; k++; } return (x < 0 ? '−' : '') + m.toFixed(n - 1) + '·10' + hoch(k); }
    return (x < 0 ? '−' : '') + a.toPrecision(n);
  }
  // Länge mit passender Vorsilbe (3.16 m, 6.0 cm, 532 nm …), n signifikante Stellen
  function laenge(m, n){
    // [Faktor, Vorsilbe, ab]: nm schon ab 0.1 nm (0.10 nm statt 100 pm, wie die Themenseite)
    var a = Math.abs(m), t = [[1e3, 'km', 1e3], [1, 'm', 1], [1e-2, 'cm', 1e-2], [1e-3, 'mm', 1e-3], [1e-6, 'µm', 1e-6], [1e-9, 'nm', 1e-10], [1e-12, 'pm', 0]];
    for (var i = 0; i < t.length; i++) if (a >= t[i][2] * 0.9999 || i === t.length - 1) return sz(m / t[i][0], n || 3) + NB + t[i][1];
  }

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

  /* ---------- Kapitel 1: Von der Schwingung zur Welle ----------
     Eine Kette aus 21 gekoppelten Teilchen (Abstand 0.15 m, Länge 3.0 m). Das erste Teilchen ist der
     Erreger; er schwingt mit der Frequenz f. Jedes Teilchen übernimmt die Bewegung seines linken Nachbarn
     verzögert: Die Störung läuft mit c = 1.2 m/s (Eigenschaft der Kette). Teilchen bei s:
     y(s, t) = A · sin(2π · f · (t − s/c)) für t ≥ s/c, sonst in Ruhe; «ein Stoss»: nur eine halbe
     Schwingung (ein Berg). Querwelle A = 0.25 m nach oben, Längswelle A = 0.10 m in Ausbreitungsrichtung
     (bei kurzen Wellen kleiner, höchstens 0.75 · λ/(2π), damit sich die Teilchen nicht überholen). Bild 1:1,
     90 px je m; Echtzeit. Unterschied zur Themenseite (Einstieg und Animation 3: Wellen, die schon laufen,
     ohne Erreger): Die Welle entsteht hier aus der Ruhe — die Front und der verzögerte Start des markierten
     Teilchens P (s = 1.8 m, Start nach 1.5 s) zeigen die Kopplung. Clipbeispiel: Seil, Hand 5-mal in 4.0 s,
     Band 3.6 m nach 2.4 s; Startwerte Querwelle, dauernd, 1.0 Hz (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg);
    var C = 1.2, N = 21, DS = 0.15, SP = 1.8, IP = 12, LEN = 3.0, X0 = 24, K = 90, Y0 = 76, TDAUER = 30;
    var t = 0, lauf = null, laeufe = [], pause = false, pruefen = function(){};
    var B = Bedienung(fig, function(){ neu(); });
    function werte(){
      var f = B.wert('f'), art = B.wert('art'), lam = C / f;
      return { f: f, T: 1 / f, lam: lam, art: art, erreger: B.wert('erreger'), A: art === 'quer' ? 0.25 : Math.min(0.10, 0.75 * lam / (2 * Math.PI)) };
    }
    function aus(s, tt, w){
      var tau = tt - s / C; if (tau <= 0) return 0;
      if (w.erreger === 'stoss' && tau > 0.5 / w.f) return 0;
      return w.A * Math.sin(2 * Math.PI * w.f * tau);
    }
    function ende(w){ return w.erreger === 'stoss' ? LEN / C + 0.5 / w.f + 0.6 : TDAUER; }
    function merken(){ if (lauf){ lauf.tmax = Math.max(lauf.tmax, t); if (t >= SP / C - 1e-9 && lauf.tP == null) lauf.tP = SP / C; } }
    var uhr = Uhr(function(tt){ var w = werte(); t = Math.min(tt, ende(w)); merken(); zeichnen(); if (t >= ende(w)){ setTimeout(knoepfe, 0); return false; } });
    function neu(){ uhr.stop(); t = 0; lauf = null; pause = false; zeichnen(); knoepfe(); }
    var A = aktionen(fig, [
      ['start', '▶ Start', function(){
        var w = werte(); pause = false;
        lauf = { art: w.art, erreger: w.erreger, f: w.f, tP: null, tmax: 0 }; laeufe.push(lauf);
        if (WENIGER){ t = w.erreger === 'stoss' ? ende(w) : 6; merken(); zeichnen(); knoepfe(); }
        else { t = 0; uhr.start(0); knoepfe(); } }],
      ['pause', '⏸ Pause', function(){ if (uhr.laeuft()){ uhr.stop(); pause = true; } else if (pause && lauf){ pause = false; uhr.start(t); } knoepfe(); zeichnen(); }],
      ['neu', '↺ Neu', function(){ neu(); }]]);
    function knoepfe(){ A.pause.textContent = uhr.laeuft() ? '⏸ Pause' : '▶ weiter'; A.pause.disabled = !(uhr.laeuft() || (pause && lauf)); }
    var sim = {
      zustand: function(){ var w = werte(); w.t = t; w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); },
      setze: function(o){ uhr.stop(); t = 0; lauf = null; pause = false; B.setze(o); zeichnen(); knoepfe(); },
      aufraeumen: function(){ uhr.stop(); t = 0; lauf = null; laeufe = []; pause = false; B.zuruecksetzen(); knoepfe(); },
      // Testhaken: Zustand x Sekunden nach dem Start (Bildfolgen der Clips)
      zeige: function(x){ uhr.stop(); var w = werte(); lauf = { art: w.art, erreger: w.erreger, f: w.f, tP: null, tmax: 0 }; t = x; merken(); pause = true; zeichnen(); knoepfe(); }
    };
    fig.__sim = sim;
    function X(s){ return X0 + K * s; }
    function zeichnen(){
      var w = werte(); B.anzeigen(); leeren(szene);
      var aktiv = !!lauf, i, s, a, x, y, pts = [];
      el(szene, 'line', { x1: X(0), y1: Y0, x2: X(LEN), y2: Y0, 'class': 'ruhe' });
      for (i = 0; i < N; i++){
        s = i * DS; a = aktiv ? aus(s, t, w) : 0; x = X(s); y = Y0;
        if (w.art === 'quer') y = Y0 - K * a; else x = X(s) + K * a;
        pts.push([x, y]);
      }
      // Ruhelage von P als Hilfslinie: P kehrt immer dorthin zurück
      if (w.art === 'quer') el(szene, 'line', { x1: X(SP), y1: Y0 - 34, x2: X(SP), y2: Y0 + 34, 'class': 'hilfslinie fuehrung' });
      else el(szene, 'line', { x1: X(SP) - 14, y1: Y0 + 22, x2: X(SP) + 14, y2: Y0 + 22, 'class': 'hilfslinie fuehrung' });
      if (w.art === 'quer'){
        el(szene, 'polyline', { points: pts.map(function(p){ return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' '), 'class': 'kette' });
        for (i = 1; i < N; i++) if (i !== IP) el(szene, 'circle', { cx: pts[i][0], cy: pts[i][1], r: 3.2, 'class': 'teilchen-w' });
      } else {
        el(szene, 'line', { x1: X(0), y1: Y0, x2: X(LEN), y2: Y0, 'class': 'kette' });
        for (i = 1; i < N; i++) if (i !== IP) el(szene, 'line', { x1: pts[i][0], y1: Y0 - 13, x2: pts[i][0], y2: Y0 + 13, 'class': 'windung' });
      }
      // Erreger (erstes Teilchen) und markiertes Teilchen P
      el(szene, 'rect', { x: pts[0][0] - 6, y: pts[0][1] - 6, width: 12, height: 12, rx: 2, 'class': 'erreger' });
      el(szene, 'text', { x: X(0) - 6, y: Y0 + 46, 'class': 'bt-klein' }, 'Erreger');
      if (w.art === 'quer'){ el(szene, 'circle', { cx: pts[IP][0], cy: pts[IP][1], r: 5, 'class': 'p-mark' });
        el(szene, 'text', { x: pts[IP][0] + 8, y: pts[IP][1] - 8, 'class': 'p-text p-tinte' }, 'P'); }
      else { el(szene, 'line', { x1: pts[IP][0], y1: Y0 - 16, x2: pts[IP][0], y2: Y0 + 16, 'class': 'windung p-bar' });
        el(szene, 'text', { x: pts[IP][0], y: Y0 - 21, 'text-anchor': 'middle', 'class': 'p-text p-tinte' }, 'P'); }
      // Front der Welle (grün): so weit ist die Störung gekommen
      var sf = C * t;
      if (aktiv && t > 0 && sf <= LEN + 1e-9){
        var xf = X(sf);
        pfeil(szene, Math.max(X(0), xf - 26), 26, xf, 26, 'pf-c', 6);
        el(szene, 'line', { x1: xf, y1: 30, x2: xf, y2: Y0 + 30, 'class': 'front-linie' });
        if (sf < 0.6) el(szene, 'text', { x: xf + 4, y: 22, 'class': 'bt-wert c-text' }, 'Front');
        else el(szene, 'text', { x: xf - 30, y: 22, 'text-anchor': 'end', 'class': 'bt-wert c-text' }, 'Front');
      }
      // s-Achse
      var ya = 128;
      el(szene, 'line', { x1: X(0), y1: ya, x2: X(LEN) + 6, y2: ya, 'class': 'achse' });
      for (i = 0; i <= 6; i++){ x = X(i * 0.5); el(szene, 'line', { x1: x, y1: ya, x2: x, y2: ya + 4, 'class': 'achse' });
        el(szene, 'text', { x: x, y: ya + 15, 'text-anchor': 'middle', 'class': 'skala' }, zahl(i * 0.5)); }
      el(szene, 'text', { x: X(LEN) + 6, y: ya - 5, 'text-anchor': 'end', 'class': 'achsname' }, 's [m]');
      // Uhr
      el(szene, 'text', { x: 0, y: 8, 'class': 'bt-meldung' }, 't = ' + fest(t, 1) + NB + 's');
      el(szene, 'text', { x: 300, y: 8, 'text-anchor': 'end', 'class': 'bt-klein' },
         w.erreger === 'stoss' ? 'Erreger: ein Stoss' : 'Erreger: ' + fest(aktiv ? w.f * t : 0, 1) + ' Schwingungen');
      var z = '<span>' + v_('T') + ' = 1 / ' + v_('f') + ' = 1 / ' + fest(w.f, 2) + NB + 'Hz ' + ist(1 / w.f, sz(1 / w.f, 3)) + sz(1 / w.f, 3) + NB + 's: so lange dauert eine Schwingung des Erregers.</span>';
      if (lauf && lauf.tP != null && t >= lauf.tP) z += '<span>P (bei ' + v_('s') + ' = 1.8' + NB + 'm) beginnt bei ' + v_('t') + ' = 1.5' + NB + 's zu schwingen.</span>';
      z += '<span class="sim-notiz">' + (w.art === 'quer' ? 'Querwelle: Die Teilchen schwingen quer zur Ausbreitung.' : 'Längswelle: Die Teilchen schwingen in Ausbreitungsrichtung; es entstehen Verdichtungen und Verdünnungen.')
         + ' Gestrichelt: die Ruhelage von P. Die Welle läuft in Echtzeit; Start, Pause und Neu mit den Knöpfen.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, bed){ return s.laeufe.some(bed); }
    function gleich(a, b){ return Math.abs(a - b) < 1e-6; }
    pruefen = Leiste(fig, [
      { text: 'Starte eine Querwelle (dauernd) und beobachte nur das markierte Teilchen P. Wie bewegt sich P, wie bewegt sich die Welle? Notiere, dann vergleiche.',
        ok: function(s){ return hat(s, function(l){ return l.art === 'quer' && l.erreger === 'dauernd' && l.tP != null && l.tmax >= l.tP + 1 / l.f; }); },
        vergleich: 'P schwingt nur auf und ab um seine Ruhelage und kommt immer wieder an seinen Platz zurück. Die Welle dagegen läuft nach rechts. Weitergegeben wird die Bewegung von Teilchen zu Teilchen — transportiert wird Energie, keine Materie.' },
      { text: 'Wähle «ein Stoss» und starte. Lies ab, wann P zu schwingen beginnt. Wie schnell läuft die Störung durch die Kette? Rechne, dann vergleiche.',
        ok: function(s){ return hat(s, function(l){ return l.erreger === 'stoss' && l.tP != null; }); },
        vergleich: 'P liegt \\(1.8\\;\\text{m}\\) vom Erreger entfernt und beginnt nach \\(1.5\\;\\text{s}\\) zu schwingen: \\(c = \\dfrac{s}{t} = \\dfrac{1.8\\;\\text{m}}{1.5\\;\\text{s}} = 1.2\\;\\text{m/s}\\). Jedes Teilchen startet etwas später als sein linker Nachbar — diese Verzögerung macht aus der Schwingung eine laufende Welle.' },
      { text: 'Wechsle zur Längswelle (dauernd) und starte. In welche Richtung schwingt P jetzt? Wo liegen die Teilchen dicht, wo weit auseinander?',
        ok: function(s){ return hat(s, function(l){ return l.art === 'laengs' && l.erreger === 'dauernd' && l.tP != null && l.tmax >= l.tP + 1 / l.f; }); },
        vergleich: 'P schwingt hin und her, in Ausbreitungsrichtung. Wo die Teilchen zusammenrücken, entsteht eine Verdichtung, wo sie auseinanderrücken, eine Verdünnung; beide wandern nach rechts. So läuft Schall durch die Luft: als Längswelle aus Druckschwankungen.' },
      { text: 'Der Erreger soll für eine Schwingung genau \\(0.625\\;\\text{s}\\) brauchen. Welche Frequenz musst du einstellen? Rechne, stelle ein und starte.',
        ok: function(s){ return hat(s, function(l){ return gleich(l.f, 1.6) && l.tmax >= 1 / l.f; }); },
        vergleich: '\\(f = \\dfrac{1}{T} = \\dfrac{1}{0.625\\;\\text{s}} = 1.6\\;\\text{Hz}\\): Der Erreger schwingt \\(1.6\\)-mal pro Sekunde.' },
      { text: 'Stelle \\(f = 2.0\\;\\text{Hz}\\) und starte eine Querwelle (dauernd). Zähle die Wellenberge auf der Kette, sobald die Front am Ende ist. Wie oft hat der Erreger bis dahin geschwungen?',
        ok: function(s){ return hat(s, function(l){ return l.art === 'quer' && l.erreger === 'dauernd' && gleich(l.f, 2) && l.tmax >= 2.5; }); },
        vergleich: 'Die Front braucht \\(\\dfrac{3.0\\;\\text{m}}{1.2\\;\\text{m/s}} = 2.5\\;\\text{s}\\) bis ans Ende. In dieser Zeit schwingt der Erreger \\(2.5\\;\\text{s} \\cdot 2.0\\;\\text{Hz} = 5\\)-mal — und \\(5\\) Wellenberge liegen auf der Kette: Jede Schwingung des Erregers schickt eine Welle los.' }
    ], sim);
    zeichnen(); knoepfe();
  })();

  /* ---------- Kapitel 2: Momentbild und Zeitdiagramm ----------
     Dieselbe Seilwelle in zwei Diagrammen: oben das Momentbild y(s) zum Zeitpunkt t (Regler), unten das
     Zeitdiagramm y(t) des Punkts P an der Stelle s_P (Regler). y(s, t) = A · sin(2π · (t/T − s/λ)),
     A = 4 cm, die Welle läuft nach rechts. Welle A: λ = 2.0 m, T = 1.6 s (c = 1.25 m/s); Welle B: λ = 3.0 m,
     T = 1.2 s (c = 2.5 m/s). Gitter 0.5 m bzw. 0.2 s: Bei Welle A liegen Berge und Maxima auf Gitterlinien (Abstand 2.0 m, 1.6 s); bei Welle B
     liegen die Abstände (3.0 m, 1.2 s) auf Gitterlinien, die Lage der Berge im Allgemeinen nicht. Ein Dreieck
     markiert einen bestimmten Wellenberg (k = 0: s = λ · (t/T − 1/4)); er wandert nur, wenn man t verschiebt
     (kein Punkt läuft von selbst, STYLEGUIDE §5.10). λ und T stehen nirgends: Sie werden abgelesen.
     Unterschied zur Themenseite 6.1a (Animation 3, laufende Welle mit Mitschrieb): beide Diagramme hängen an
     zwei Reglern (Zeitpunkt, Ort). Clipbeispiel: Wellenbad λ = 5.0 m, T = 2.0 s; Startwerte Welle A,
     t = 0.5 s, P bei 1.0 m (kein Leistenziel). */
  var WELLEN2 = { A: { lam: 2.0, T: 1.6 }, B: { lam: 3.0, T: 1.2 } };
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var kopf = g_(svg), g1 = g_(svg, { transform: 'translate(0,18)' }), mitte = g_(svg), g2 = g_(svg, { transform: 'translate(0,186)' });
    var AMP = 4, pruefen = function(){};
    var B = Bedienung(fig, function(){ zeichnen(); });
    hilfsschalter(fig, function(){ zeichnen(); });
    function werte(){ var w = WELLEN2[B.wert('welle')], t = B.wert('t'), sp = B.wert('sp');
      return { welle: B.wert('welle'), lam: w.lam, T: w.T, t: t, sp: sp, yP: yv(w, sp, t), bewegt: B.bewegt }; }
    function yv(w, s, t){ return AMP * Math.sin(2 * Math.PI * (t / w.T - s / w.lam)); }
    var sim = {
      zustand: function(){ return werte(); }, zeichnen: function(){ zeichnen(); },
      setze: function(o){ B.setze(o); zeichnen(); }, aufraeumen: function(){ B.zuruecksetzen(); },
      // Testhaken: {welle, t, sp} einstellen (Bilder der Clips)
      zeige: function(o){ if (o) B.setze(o); zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var z = werte(), w = WELLEN2[z.welle]; B.anzeigen(); leeren(kopf); leeren(g1); leeren(mitte); leeren(g2);
      var mit = !fig.classList.contains('ohne-hilfslinien');
      el(kopf, 'text', { x: 0, y: 8, 'class': 'bt-meldung' }, 'Momentbild: das ganze Seil bei t = ' + fest(z.t, 1) + NB + 's');
      var K1 = Achsen(g1, { w: 300, h: 130, x0: -0.45, x1: 6.75, y0: -6.5, y1: 6.5, sx: 0.5, sy: 2, xm: [1, 2, 3, 4, 5, 6], ym: [-4, 4], xname: 's [m]', yname: 'y [cm]' });
      K1.kurve(function(s){ return yv(w, s, z.t); }, 'w-kurve', 0, 6.0);
      // markierter Wellenberg (Dreieck darüber)
      var sc = w.lam * (z.t / w.T - 0.25);
      if (sc >= 0.3 && sc <= 6.0){ var xc = K1.X(sc), yc = K1.Y(AMP) - 5;
        el(K1.ebene, 'polygon', { points: (xc - 5) + ',' + (yc - 8) + ' ' + (xc + 5) + ',' + (yc - 8) + ' ' + xc + ',' + yc, 'class': 'berg-mark' }); }
      if (mit) el(K1.ebene, 'line', { x1: K1.X(z.sp), y1: 0, x2: K1.X(z.sp), y2: 130, 'class': 'hilfslinie' });
      K1.punkt(z.sp, z.yP, 'p-mark', 'P', 7, -7);
      el(mitte, 'text', { x: 0, y: 176, 'class': 'bt-meldung' }, 'Zeitdiagramm: der Punkt P bei s = ' + fest(z.sp, 1) + NB + 'm');
      var K2 = Achsen(g2, { w: 300, h: 130, x0: -0.45, x1: 6.75, y0: -6.5, y1: 6.5, sx: 0.2, sy: 2, xm: [1, 2, 3, 4, 5, 6], ym: [-4, 4], xname: 't [s]', yname: 'y [cm]' });
      K2.kurve(function(t){ return yv(w, z.sp, t); }, 'w-kurve', 0, 6.0);
      if (mit) el(K2.ebene, 'line', { x1: K2.X(z.t), y1: 0, x2: K2.X(z.t), y2: 130, 'class': 'hilfslinie' });
      K2.punkt(z.t, z.yP, 'p-mark', 'P', 7, -7);
      var s = '<span>Oben steht die Zeit still: Man sieht das ganze Seil. Unten steht der Ort fest: Man sieht, wie sich P im Lauf der Zeit bewegt.</span>';
      s += '<span>P: ' + v_('y') + ' ' + ist(z.yP, fest(z.yP, 1)) + fest(z.yP, 1) + NB + 'cm bei ' + v_('t') + ' = ' + fest(z.t, 1) + NB + 's</span>';
      s += '<span class="sim-notiz">Das Dreieck markiert einen bestimmten Wellenberg. Die Welle läuft nach rechts; sie bewegt sich, wenn du t verschiebst. ' + (mit ? 'Gestrichelt: die Stelle von P oben, der Zeitpunkt t unten.' : '') + '</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    function nahe(a, b){ return Math.abs(a - b) < 0.05; }
    pruefen = Leiste(fig, [
      { text: 'Ziehe am Regler \\(t\\), bis P gerade auf einem Wellenberg sitzt. Lies im Momentbild ab, wie weit der nächste Berg entfernt ist. Notiere diese Wellenlänge \\(\\lambda\\).',
        ok: function(s){ return s.welle === 'A' && s.yP >= 0.98 * AMP && s.bewegt.t; },
        vergleich: '\\(\\lambda = 2.0\\;\\text{m}\\): von Berg zu Berg auf der \\(s\\)-Achse, in Metern. Ebenso gut von Tal zu Tal oder zwischen zwei anderen Stellen gleicher Phase.' },
      { text: 'Jetzt das Zeitdiagramm: P sitzt bei \\(t = 1.2\\;\\text{s}\\) auf einem Berg. Ziehe \\(t\\) bis zum nächsten Maximum von P. Wie lange hat das gedauert? Notiere diese Periode \\(T\\).',
        setup: function(sim){ sim.setze({ welle: 'A', sp: 1, t: 1.2 }); },
        ok: function(s){ return s.welle === 'A' && nahe(s.sp, 1) && nahe(s.t, 2.8); },
        vergleich: '\\(T = 2.8\\;\\text{s} - 1.2\\;\\text{s} = 1.6\\;\\text{s}\\): von Maximum zu Maximum auf der \\(t\\)-Achse, in Sekunden. Nach einer Periode ist P wieder im selben Zustand.' },
      { text: 'Das Dreieck markiert einen Wellenberg. Ziehe \\(t\\) um eine Periode weiter, von \\(2.8\\;\\text{s}\\) auf \\(4.4\\;\\text{s}\\). Wie weit ist dieser Berg gewandert? Berechne daraus die Phasengeschwindigkeit.',
        setup: function(sim){ sim.setze({ welle: 'A', sp: 1, t: 2.8 }); },
        ok: function(s){ return s.welle === 'A' && nahe(s.t, 4.4); },
        vergleich: 'Der Berg rückt in einer Periode genau um eine Wellenlänge weiter, von \\(3.0\\;\\text{m}\\) auf \\(5.0\\;\\text{m}\\): \\(c = \\dfrac{\\lambda}{T} = \\dfrac{2.0\\;\\text{m}}{1.6\\;\\text{s}} = 1.25\\;\\text{m/s}\\). Das ist die Phasengeschwindigkeit: So schnell wandert eine Stelle gleicher Phase, etwa ein Berg.' },
      { text: 'Wähle Welle B. Bestimme \\(\\lambda\\) im Momentbild und \\(T\\) im Zeitdiagramm, dann die Frequenz \\(f\\) und die Phasengeschwindigkeit \\(c\\).',
        ok: function(s){ return s.welle === 'B' && (s.bewegt.t || s.bewegt.sp); },
        vergleich: '\\(\\lambda = 3.0\\;\\text{m}\\) (Berg zu Berg im Momentbild), \\(T = 1.2\\;\\text{s}\\) (Maximum zu Maximum im Zeitdiagramm). \\(f = \\dfrac{1}{T} = \\dfrac{1}{1.2\\;\\text{s}} \\approx 0.83\\;\\text{Hz}\\) und \\(c = \\dfrac{\\lambda}{T} = \\dfrac{3.0\\;\\text{m}}{1.2\\;\\text{s}} = 2.5\\;\\text{m/s}\\).' },
      { text: 'Bleib bei Welle B und schiebe P an eine andere Stelle. Was ändert sich im Zeitdiagramm, was nicht? Ändert sich \\(\\lambda\\)?',
        ok: function(s){ return s.welle === 'B' && s.bewegt.sp && !nahe(s.sp, 1); },
        vergleich: 'Die Kurve im Zeitdiagramm verschiebt sich nur: P erreicht seine Maxima zu anderen Zeiten. Ihr Abstand bleibt \\(T = 1.2\\;\\text{s}\\) — jeder Punkt schwingt im Takt des Erregers. Auch \\(\\lambda\\) bleibt: Es ist eine Strecke im Momentbild, keine Zeit.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Sender und Medium — zwei Seile ----------
     Ein Sender (Hand) schwingt links mit der Frequenz f. Das linke Seil (0 bis 3 m) trägt die Welle mit
     c₁ = 1.0 m/s; an der Knotenstelle (3 m) geht sie in ein zweites Seil über: dünner (c₂ = 2.0 m/s), gleich
     (1.0 m/s) oder dicker (0.5 m/s). Auslenkung y = A · sin(2π · f · τ), τ = Zeit seit der Ankunft der Front
     (links τ = t − s/c₁, rechts τ = t − 3 m/c₁ − (s − 3 m)/c₂); A = 0.40 m, im Bild 47 px je m. Die Front
     läuft unabhängig von f. Eine Reflexion an der Knotenstelle zeichnet das Modell nicht (Vertiefung auf
     der Themenseite 6.1a). Echtzeit. Unterschied zur Themenseite (Animation 2: ein Medium mit Reglern für
     c und f; Animation 4: Balken je Medium): der Übergang selbst — links und rechts dieselbe Frequenz,
     verschiedene Wellenlängen. Clipbeispiel: 850 Hz von Luft in Wasser; Startwerte 0.75 Hz, rechts das
     gleiche Seil (kein Leistenziel). */
  var SEIL2 = { duenn: { c: 2.0, n: 'dünneres Seil', d: 1.4 }, gleich: { c: 1.0, n: 'gleiches Seil', d: 2.6 }, dick: { c: 0.5, n: 'dickeres Seil', d: 4.6 } };
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg);
    var C1 = 1.0, SJ = 3.0, LEN = 6.0, S1 = 2.0, S2 = 4.5, X0 = 12, K = 47, Y0 = 72, AMP = 0.40;
    var t = 0, lauf = null, laeufe = [], pause = false, pruefen = function(){};
    var B = Bedienung(fig, function(){ neu(); });
    function werte(){ var r = B.wert('rechts'), f = B.wert('f'), c2 = SEIL2[r].c;
      return { f: f, rechts: r, c2: c2, lam1: C1 / f, lam2: c2 / f, tJ: SJ / C1, t1: S1 / C1, t2: SJ / C1 + (S2 - SJ) / c2, tEnde: SJ / C1 + (LEN - SJ) / c2 }; }
    function tau(s, tt, w){ return s <= SJ ? tt - s / C1 : tt - SJ / C1 - (s - SJ) / w.c2; }
    function aus(s, tt, w){ var q = tau(s, tt, w); return q <= 0 ? 0 : AMP * Math.sin(2 * Math.PI * w.f * q); }
    function ende(w){ return w.tEnde + 4; }
    function merken(){ if (!lauf) return; var w = werte(); lauf.tmax = Math.max(lauf.tmax, t); }
    var uhr = Uhr(function(tt){ var w = werte(); t = Math.min(tt, ende(w)); merken(); zeichnen(); if (t >= ende(w)){ setTimeout(knoepfe, 0); return false; } });
    function neu(){ uhr.stop(); t = 0; lauf = null; pause = false; zeichnen(); knoepfe(); }
    var A = aktionen(fig, [
      ['start', '▶ Start', function(){ var w = werte(); pause = false;
        lauf = { f: w.f, rechts: w.rechts, tmax: 0, tJ: w.tJ, t1: w.t1, t2: w.t2 }; laeufe.push(lauf);
        if (WENIGER){ t = ende(w); merken(); zeichnen(); knoepfe(); } else { t = 0; uhr.start(0); knoepfe(); } }],
      ['pause', '⏸ Pause', function(){ if (uhr.laeuft()){ uhr.stop(); pause = true; } else if (pause && lauf){ pause = false; uhr.start(t); } knoepfe(); zeichnen(); }],
      ['neu', '↺ Neu', function(){ neu(); }]]);
    function knoepfe(){ A.pause.textContent = uhr.laeuft() ? '⏸ Pause' : '▶ weiter'; A.pause.disabled = !(uhr.laeuft() || (pause && lauf)); }
    var sim = {
      zustand: function(){ var w = werte(); w.t = t; w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); },
      setze: function(o){ uhr.stop(); t = 0; lauf = null; pause = false; B.setze(o); zeichnen(); knoepfe(); },
      aufraeumen: function(){ uhr.stop(); t = 0; lauf = null; laeufe = []; pause = false; B.zuruecksetzen(); knoepfe(); },
      // Testhaken: Zustand x Sekunden nach dem Start (Bildfolgen der Clips)
      zeige: function(x){ uhr.stop(); var w = werte(); lauf = { f: w.f, rechts: w.rechts, tmax: 0, tJ: w.tJ, t1: w.t1, t2: w.t2 }; t = x; merken(); pause = true; zeichnen(); knoepfe(); }
    };
    fig.__sim = sim;
    function X(s){ return X0 + K * s; }
    function zeichnen(){
      var w = werte(), aktiv = !!lauf, i, s; B.anzeigen(); leeren(szene);
      el(szene, 'line', { x1: X(0), y1: Y0, x2: X(LEN), y2: Y0, 'class': 'ruhe' });
      // Seile: links normal, rechts nach Wahl dünner oder dicker
      var l = [], r = [];
      for (i = 0; i <= 240; i++){ s = LEN * i / 240; var p = X(s).toFixed(1) + ',' + (Y0 - K * (aktiv ? aus(s, t, w) : 0)).toFixed(1); if (s <= SJ) l.push(p); if (s >= SJ) r.push(p); }
      el(szene, 'polyline', { points: l.join(' '), 'class': 'seil', 'stroke-width': SEIL2.gleich.d });
      el(szene, 'polyline', { points: r.join(' '), 'class': 'seil', 'stroke-width': SEIL2[w.rechts].d });
      var yJ = Y0 - K * (aktiv ? aus(SJ, t, w) : 0);
      el(szene, 'circle', { cx: X(SJ), cy: yJ, r: 3.6, 'class': 'knoten' });
      el(szene, 'rect', { x: X(0) - 6, y: Y0 - K * (aktiv ? aus(0, t, w) : 0) - 6, width: 12, height: 12, rx: 2, 'class': 'erreger' });
      [[S1, 'P₁'], [S2, 'P₂']].forEach(function(m){ var y = Y0 - K * (aktiv ? aus(m[0], t, w) : 0);
        el(szene, 'circle', { cx: X(m[0]), cy: y, r: 4.5, 'class': 'p-mark' });
        el(szene, 'text', { x: X(m[0]) + 7, y: y - 7, 'class': 'p-text p-tinte' }, m[1]); });
      // Front (grün)
      var sf = t <= w.tJ ? C1 * t : SJ + w.c2 * (t - w.tJ);
      if (aktiv && t > 0 && sf <= LEN + 1e-9){ var xf = X(sf);
        pfeil(szene, Math.max(X(0), xf - 26), 18, xf, 18, 'pf-c', 6);
        el(szene, 'line', { x1: xf, y1: 22, x2: xf, y2: Y0 + 26, 'class': 'front-linie' });
        el(szene, 'text', { x: sf < 0.7 ? xf + 4 : xf - 30, y: 14, 'text-anchor': sf < 0.7 ? 'start' : 'end', 'class': 'bt-wert c-text' }, 'Front'); }
      // Beschriftung der Seile
      el(szene, 'text', { x: X(0.1), y: Y0 + 34, 'class': 'bt-klein' }, 'Seil 1: c₁ = 1.0' + NB + 'm/s');
      el(szene, 'text', { x: X(SJ + 0.15), y: Y0 + 34, 'class': 'bt-klein' }, 'Seil 2 (' + SEIL2[w.rechts].n + '): c₂ = ' + sz(w.c2, 2) + NB + 'm/s');
      // Wellenlängen als Masslinien (Lineal), sobald die Welle dort angekommen ist
      var ym = Y0 + 58;
      if (aktiv && t >= w.t1){ if (w.lam1 <= SJ - 0.1) mass(szene, X(0.05), ym, X(0.05 + w.lam1), 'λ₁ = ' + fest(w.lam1, 2) + NB + 'm', 'mass-text');
        else el(szene, 'text', { x: X(0.1), y: ym, 'class': 'bt-wert mass-text' }, 'λ₁ = ' + fest(w.lam1, 2) + NB + 'm' + ' (länger als Seil 1)'); }
      if (aktiv && t >= w.t2){ if (w.lam2 <= LEN - SJ - 0.1) mass(szene, X(SJ + 0.05), ym, X(SJ + 0.05 + w.lam2), 'λ₂ = ' + fest(w.lam2, 2) + NB + 'm', 'mass-text');
        else el(szene, 'text', { x: X(SJ + 0.1), y: ym, 'class': 'bt-wert mass-text' }, 'λ₂ = ' + fest(w.lam2, 2) + NB + 'm' + ' (länger als Seil 2)'); }
      // s-Achse
      var ya = 146;
      el(szene, 'line', { x1: X(0), y1: ya, x2: X(LEN) + 4, y2: ya, 'class': 'achse' });
      for (i = 0; i <= 6; i++){ var x = X(i); el(szene, 'line', { x1: x, y1: ya, x2: x, y2: ya + 4, 'class': 'achse' });
        el(szene, 'text', { x: x, y: ya + 15, 'text-anchor': 'middle', 'class': 'skala' }, String(i)); }
      el(szene, 'text', { x: X(LEN) + 4, y: ya - 5, 'text-anchor': 'end', 'class': 'achsname' }, 's [m]');
      el(szene, 'text', { x: 0, y: 4, 'class': 'bt-meldung' }, 't = ' + fest(t, 1) + NB + 's');
      el(szene, 'text', { x: 300, y: 4, 'text-anchor': 'end', 'class': 'bt-klein' }, 'Sender: f = ' + fest(w.f, 2) + NB + 'Hz');
      var z = '';
      if (aktiv && t >= w.t1) z += '<span>Seil 1: ' + v_('λ') + '<sub>1</sub> = ' + v_('c') + '<sub>1</sub> / ' + v_('f') + ' = 1.0' + NB + 'm/s / ' + fest(w.f, 2) + NB + 'Hz ' + ist(w.lam1, fest(w.lam1, 2)) + fest(w.lam1, 2) + NB + 'm' + '</span>';
      if (aktiv && t >= w.tJ) z += '<span>Die Front erreicht die Knotenstelle nach ' + v_('t') + ' = 3.0' + NB + 's — bei jeder Frequenz.</span>';
      if (aktiv && t >= w.t2) z += '<span>Seil 2: ' + v_('λ') + '<sub>2</sub> = ' + v_('c') + '<sub>2</sub> / ' + v_('f') + ' = ' + sz(w.c2, 2) + NB + 'm/s / ' + fest(w.f, 2) + NB + 'Hz ' + ist(w.lam2, fest(w.lam2, 2)) + fest(w.lam2, 2) + NB + 'm' + '</span>';
      if (!z) z = '<span>' + v_('c') + ' = ' + v_('λ') + ' · ' + v_('f') + ' — die Wellenlängen stehen hier, sobald die Welle P₁ bzw. P₂ erreicht.</span>';
      z += '<span class="sim-notiz">P₁ und P₂ zeigen, wie die Seile an diesen Stellen schwingen. Die Reflexion an der Knotenstelle ist weggelassen. Echtzeit.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function gleich(a, b){ return Math.abs(a - b) < 1e-6; }
    function hat(s, bed){ return s.laeufe.some(bed); }
    pruefen = Leiste(fig, [
      { text: 'Lass rechts das gleiche Seil. Starte mit \\(f = 0.50\\;\\text{Hz}\\), danach mit \\(f = 1.0\\;\\text{Hz}\\), je bis die Front an der Knotenstelle ist. Was geschieht mit \\(\\lambda\\)? Kommt die Front früher an?',
        ok: function(s){ return hat(s, function(l){ return l.rechts === 'gleich' && gleich(l.f, 0.5) && l.tmax >= l.tJ; }) && hat(s, function(l){ return l.rechts === 'gleich' && gleich(l.f, 1) && l.tmax >= l.tJ; }); },
        vergleich: 'Mit der doppelten Frequenz wird die Welle halb so lang: \\(\\lambda = \\dfrac{c}{f}\\) gibt \\(2.0\\;\\text{m}\\) bzw. \\(1.0\\;\\text{m}\\). Die Front kommt in beiden Läufen nach \\(3.0\\;\\text{s}\\) an der Knotenstelle an: Die Geschwindigkeit gehört zum Seil, nicht zum Sender. Ein schnellerer Sender macht die Welle kürzer, nicht schneller.' },
      { text: 'Hänge rechts das dickere Seil an und starte. Wie oft schwingen P₁ und P₂ pro Sekunde? Wie lang sind die Wellen links und rechts?',
        ok: function(s){ return hat(s, function(l){ return l.rechts === 'dick' && l.tmax >= l.t2 + 1 / l.f; }); },
        vergleich: 'P₁ und P₂ schwingen im selben Takt: Die Frequenz bleibt beim Übergang, sie kommt vom Sender. Im dickeren Seil läuft die Welle halb so schnell und ist darum halb so lang: \\(\\lambda_2 = \\dfrac{c_2}{f}\\).' },
      { text: 'Rechts das dickere Seil (\\(c_2 = 0.50\\;\\text{m/s}\\)): Welche Frequenz braucht der Sender, damit die Welle dort \\(0.40\\;\\text{m}\\) lang ist? Rechne, stelle ein und starte.',
        ok: function(s){ return hat(s, function(l){ return l.rechts === 'dick' && gleich(l.f, 1.25) && l.tmax >= l.t2; }); },
        vergleich: '\\(f = \\dfrac{c_2}{\\lambda_2} = \\dfrac{0.50\\;\\text{m/s}}{0.40\\;\\text{m}} = 1.25\\;\\text{Hz}\\). Im linken Seil ist dieselbe Welle \\(\\lambda_1 = \\dfrac{1.0\\;\\text{m/s}}{1.25\\;\\text{Hz}} = 0.80\\;\\text{m}\\) lang.' },
      { text: 'Bei \\(f = 0.80\\;\\text{Hz}\\) ist die Welle rechts \\(2.5\\;\\text{m}\\) lang. Welches Seil hängt dort? Rechne zuerst, dann prüfe mit einem Lauf.',
        ok: function(s){ return hat(s, function(l){ return l.rechts === 'duenn' && gleich(l.f, 0.8) && l.tmax >= l.t2; }); },
        vergleich: '\\(c_2 = \\lambda_2 \\cdot f = 2.5\\;\\text{m} \\cdot 0.80\\;\\text{Hz} = 2.0\\;\\text{m/s}\\): das dünnere Seil.' },
      { text: 'Ein Ton geht von der Luft (\\(340\\;\\text{m/s}\\)) ins Wasser (\\(1500\\;\\text{m/s}\\)). Welches Seil spielt hier die Rolle des Wassers? Stelle es ein und starte mit \\(f = 1.0\\;\\text{Hz}\\). Um welchen Faktor wird die Welle im Wasser länger?',
        setup: function(sim){ sim.setze({ rechts: 'gleich' }); },
        ok: function(s){ return hat(s, function(l){ return l.rechts === 'duenn' && gleich(l.f, 1) && l.tmax >= l.t2; }); },
        vergleich: 'Wasser ist schneller als Luft — wie das dünnere Seil. Die Frequenz bleibt, die Wellenlänge wächst im selben Verhältnis wie die Geschwindigkeit: \\(\\dfrac{\\lambda_\\text{Wasser}}{\\lambda_\\text{Luft}} = \\dfrac{1500\\;\\text{m/s}}{340\\;\\text{m/s}} \\approx 4.4\\); bei den Seilen \\(\\dfrac{2.0\\;\\text{m/s}}{1.0\\;\\text{m/s}} = 2\\).' }
    ], sim);
    zeichnen(); knoepfe();
  })();

  /* ---------- Kapitel 4: Geräte im elektromagnetischen Spektrum ----------
     Sechs Geräte arbeiten mit elektromagnetischen Wellen: UKW-Radio 95.0 MHz, WLAN 5.0 GHz, Wärmebildkamera
     10 µm, Laserpointer (grün) 532 nm, UV-Lampe 365 nm, Röntgenröhre 0.10 nm. Oben das Spektrum über
     log₁₀(λ/m) von −12 bis 3 mit den Bereichen und Grenzen der Themenseite (Animation 5); kein Gerät liegt nahe
     an einer Grenze. Unten das Feldbild: das elektrische Feld E (senkrecht) und das magnetische Feld B (schräg
     gezeichnet: es steht senkrecht auf E und auf der Ausbreitung), in Phase; in Zeitlupe auf Knopfdruck. Das
     Feldbild ist für jedes Gerät dasselbe, nur die angeschriebene Wellenlänge ändert sich. Unterschied zur
     Themenseite (Animation 5: ein Schieber durchs ganze Spektrum mit Photonenergie): Geräte aus dem Alltag,
     das Feld der Welle und die Rechnung c = λ · f je Gerät. Clipbeispiel: UKW-Sender 88.0 MHz und 45 km;
     Startwert UKW-Radio (kein Leistenziel). */
  var BAENDER = [[-12, -11, 'Gammastrahlung', 'Gamma', 'b-gamma'], [-11, -8, 'Röntgenstrahlung', 'Röntgen', 'b-roe'],
                 [-8, -6.42, 'Ultraviolett', 'UV', 'b-uv'], [-6.42, -6.11, 'sichtbares Licht', 'sichtbar', 'b-vis'],
                 [-6.11, -3, 'Infrarot', 'Infrarot', 'b-ir'], [-3, 0, 'Mikrowellen', 'Mikrowellen', 'b-mw'], [0, 3, 'Radiowellen', 'Radio', 'b-radio']];   // Grenze bei 1 m wie Themenseite (Entscheid 08.10.2026)
  // «=» vor einem exakten, «≈» vor einem gerundeten Ergebnis (n signifikante Stellen)
  function gl_n(x, n){ var r = +(+x).toPrecision(n); return Math.abs(r - x) <= 1e-9 * Math.abs(x) ? '= ' : '≈ '; }
  function bandVon(lam){ var L = Math.log10(lam); for (var i = 0; i < BAENDER.length; i++) if (L >= BAENDER[i][0] && L < BAENDER[i][1]) return BAENDER[i]; return BAENDER[BAENDER.length - 1]; }
  var GERAETE = { radio: { n: 'UKW-Radio', f: 95.0e6, gegeben: 'f', text: '95.0' + NB + 'MHz', st: 3 }, wlan: { n: 'WLAN', f: 5.0e9, gegeben: 'f', text: '5.0' + NB + 'GHz', st: 2 },
                  ir: { n: 'Wärmebildkamera', lam: 10e-6, gegeben: 'lam', text: '10' + NB + 'µm', st: 2 }, gruen: { n: 'Laserpointer (grün)', lam: 532e-9, gegeben: 'lam', text: '532' + NB + 'nm', st: 3 },
                  uv: { n: 'UV-Lampe', lam: 365e-9, gegeben: 'lam', text: '365' + NB + 'nm', st: 3 }, roentgen: { n: 'Röntgenröhre', lam: 0.10e-9, gegeben: 'lam', text: '0.10' + NB + 'nm', st: 2 } };
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var spek = g_(svg), feld = g_(svg);
    var phase = 0, laeuft = false, lief = false, gesehen = {}, pruefen = function(){};
    var B = Bedienung(fig, function(){ gesehen[B.wert('geraet')] = true; zeichnen(); });
    gesehen[B.wert('geraet')] = true;
    function werte(){ var g = GERAETE[B.wert('geraet')], lam = g.lam || CL / g.f, f = g.f || CL / g.lam;
      return { geraet: B.wert('geraet'), g: g, lam: lam, f: f, band: bandVon(lam), gesehen: gesehen, lief: lief }; }
    var uhr = Uhr(function(tt){ phase = tt * 0.5; zeichnenFeld(werte()); });
    var A = aktionen(fig, [['zeitlupe', '▶ Zeitlupe', function(){
        if (uhr.laeuft()){ uhr.stop(); laeuft = false; } else { lief = true; laeuft = true; if (WENIGER){ phase += 0.25; zeichnen(); laeuft = false; } else uhr.start(phase / 0.5); }
        A.zeitlupe.textContent = laeuft ? '⏸ Pause' : '▶ Zeitlupe'; zeichnen(); }]]);
    var sim = {
      zustand: function(){ return werte(); }, zeichnen: function(){ zeichnen(); },
      setze: function(o){ B.setze(o); gesehen[B.wert('geraet')] = true; zeichnen(); },
      aufraeumen: function(){ uhr.stop(); laeuft = false; lief = false; A.zeitlupe.textContent = '▶ Zeitlupe'; gesehen = {}; gesehen[B.wert('geraet')] = true; B.zuruecksetzen(); },
      // Testhaken: Phase des Feldbilds (Bruchteil einer Periode)
      zeige: function(x){ uhr.stop(); laeuft = false; phase = x || 0; zeichnen(); }
    };
    fig.__sim = sim;
    var LX0 = 6, LX1 = 296;
    function lx(L){ return LX0 + (L + 12) / 15 * (LX1 - LX0); }
    function zeichnenSpektrum(w){
      leeren(spek);
      var y0 = 30, y1 = 50, i;
      el(spek, 'text', { x: 0, y: 4, 'class': 'bt-klein' }, 'Wellenlänge λ [m]  →  wächst nach rechts');
      BAENDER.forEach(function(b){ el(spek, 'rect', { x: lx(b[0]), y: y0, width: lx(b[1]) - lx(b[0]), height: y1 - y0, 'class': 'spek-band ' + b[4] }); });
      // sichtbares Licht in seinen Farben
      for (i = 0; i < 12; i++){ var nm = 780 - 400 * (i + 0.5) / 12, L = Math.log10(nm * 1e-9);
        el(spek, 'rect', { x: lx(L) - 0.4, y: y0, width: (lx(-6.11) - lx(-6.42)) / 12 + 0.8, height: y1 - y0, fill: spektralfarbe(nm) }); }
      el(spek, 'rect', { x: LX0, y: y0, width: LX1 - LX0, height: y1 - y0, 'class': 'band-rahmen' });
      for (i = -12; i <= 3; i += 3){ el(spek, 'line', { x1: lx(i), y1: y0 - 3, x2: lx(i), y2: y0, 'class': 'achse' });
        el(spek, 'text', { x: lx(i), y: 19, 'text-anchor': 'middle', 'class': 'skala' }, i === 0 ? '1' : '10' + hoch(i)); }
      // Namen in zwei Reihen (sichtbar und UV liegen dicht beieinander)
      BAENDER.forEach(function(b, k){ var reihe = [0, 1, 0, 1, 0, 1, 0][k];
        el(spek, 'text', { x: Math.max(14, (lx(b[0]) + lx(b[1])) / 2), y: y1 + 12 + 11 * reihe, 'text-anchor': 'middle', 'class': 'bt-klein' }, b[3]); });
      // Frequenzachse: wo f eine Zehnerpotenz ist (log λ = log c − n)
      var yf = 92;
      for (var n = 6; n <= 18; n += 3){ var L2 = Math.log10(CL) - n; el(spek, 'text', { x: lx(L2), y: yf, 'text-anchor': 'middle', 'class': 'skala f-skala' }, '10' + hoch(n)); }
      el(spek, 'text', { x: 300, y: yf + 12, 'text-anchor': 'end', 'class': 'bt-klein f-skala' }, 'Frequenz f [Hz]  ←  wächst nach links');
      // Marke des Geräts: Strich durchs Band, Dreieck darüber (zwischen Teilung und Band)
      var xm = lx(Math.log10(w.lam));
      el(spek, 'line', { x1: xm, y1: y0 - 1, x2: xm, y2: y1 + 1, 'class': 'marke-linie' });
      el(spek, 'polygon', { points: (xm - 4.5) + ',' + (y0 - 7) + ' ' + (xm + 4.5) + ',' + (y0 - 7) + ' ' + xm + ',' + (y0 - 1), 'class': 'marke-dreieck' });
    }
    function zeichnenFeld(w){
      leeren(feld);
      var ya = 202, xa = 24, xb = 270, lamPx = 112, ae = 40, ab = 30, i;
      el(feld, 'text', { x: 0, y: 126, 'class': 'bt-meldung' }, w.g.n + ': ' + w.band[2]);
      el(feld, 'line', { x1: xa, y1: ya, x2: xb, y2: ya, 'class': 'achse' });
      // E (Bernstein, senkrecht) und B (Grau, schräg gezeichnet), in Phase; die Welle läuft nach rechts
      var dE = '', dB = '';
      for (i = 0; i <= 120; i++){ var x = xa + (xb - xa) * i / 120, ph = 2 * Math.PI * ((x - xa) / lamPx - phase), e = Math.sin(-ph);
        dE += (i ? ' L' : 'M') + x.toFixed(1) + ' ' + (ya - ae * e).toFixed(1);
        dB += (i ? ' L' : 'M') + (x - 0.55 * ab * e).toFixed(1) + ' ' + (ya + 0.55 * ab * e).toFixed(1);
        if (i % 6 === 3){ el(feld, 'line', { x1: x, y1: ya, x2: x, y2: ya - ae * e, 'class': 'e-pfeil' });
          el(feld, 'line', { x1: x, y1: ya, x2: x - 0.55 * ab * e, y2: ya + 0.55 * ab * e, 'class': 'b-pfeil' }); }
      }
      el(feld, 'path', { d: dB, 'class': 'b-kurve' });
      el(feld, 'path', { d: dE, 'class': 'e-kurve' });
      // Ausbreitung: Pfeil auf der Achse
      pfeil(feld, xb, ya, xb + 26, ya, 'pf-c', 7);
      el(feld, 'text', { x: xb + 13, y: ya - 6, 'text-anchor': 'middle', 'class': 'bt-wert c-text' }, 'c');
      // eine Wellenlänge zwischen zwei Bergen von E
      var x1 = xa + lamPx * (((phase + 0.75) % 1 + 1) % 1);   // ein Berg von E: (x − xa)/λ − Phase = −1/4 + k
      mass(feld, x1, 146, x1 + lamPx, 'λ = ' + laenge(w.lam, w.g.st), 'mass-text');
      // Legende unter dem Bild
      el(feld, 'line', { x1: 2, y1: 266, x2: 16, y2: 266, 'class': 'e-kurve' });
      el(feld, 'text', { x: 20, y: 269.5, 'class': 'bt-wert e-text' }, 'E: elektrisches Feld');
      el(feld, 'line', { x1: 120, y1: 266, x2: 134, y2: 266, 'class': 'b-kurve' });
      el(feld, 'text', { x: 138, y: 269.5, 'class': 'bt-wert b-text' }, 'B: magnetisches Feld');
      el(feld, 'text', { x: 2, y: 284, 'class': 'bt-wert c-text' }, 'c = 3.00·10⁸' + NB + 'm/s: Ausbreitung, im Vakuum für alle Geräte gleich');
    }
    function zeichnen(){
      var w = werte(); B.anzeigen(); zeichnenSpektrum(w); zeichnenFeld(w);
      var s = w.g.gegeben === 'f'
        ? '<span>' + w.g.n + ': ' + v_('f') + ' = ' + w.g.text + ' → ' + v_('λ') + ' = ' + v_('c') + ' / ' + v_('f') + ' = 3.00·10⁸' + NB + 'm/s / ' + sz(w.f, w.g.st) + NB + 'Hz ' + gl_n(w.lam, w.g.st) + laenge(w.lam, w.g.st) + '</span>'
        : '<span>' + w.g.n + ': ' + v_('λ') + ' = ' + w.g.text + ' → ' + v_('f') + ' = ' + v_('c') + ' / ' + v_('λ') + ' = 3.00·10⁸' + NB + 'm/s / ' + sz(w.lam, w.g.st) + NB + 'm ' + gl_n(w.f, w.g.st) + sz(w.f, w.g.st) + NB + 'Hz</span>';
      s += '<span>Bereich: ' + w.band[2] + '</span>';
      s += '<span class="sim-notiz">Unten das Feld der Welle: Elektrisches und magnetisches Feld schwingen senkrecht zueinander und quer zur Ausbreitung. Im Vakuum laufen alle diese Wellen gleich schnell. Das Feldbild ist nicht massstäblich und läuft in Zeitlupe.</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Wähle zuerst das UKW-Radio, dann die Röntgenröhre. Wievielmal kürzer ist die Röntgenwelle? Wie schnell laufen die beiden Wellen im Vakuum?',
        ok: function(s){ return s.gesehen.radio && s.gesehen.roentgen; },
        vergleich: '\\(\\dfrac{3.16\\;\\text{m}}{1.0 \\cdot 10^{-10}\\;\\text{m}} \\approx 3 \\cdot 10^{10}\\): rund dreissig Milliarden Mal kürzer. Trotzdem laufen beide im Vakuum gleich schnell, mit \\(c = 3.00 \\cdot 10^{8}\\;\\text{m/s}\\).' },
      { text: 'Ein Gerät arbeitet mit \\(5.0\\;\\text{GHz}\\). Berechne seine Wellenlänge und den Bereich im Spektrum. Dann suche das Gerät.',
        ok: function(s){ return s.geraet === 'wlan'; },
        vergleich: '\\(\\lambda = \\dfrac{c}{f} = \\dfrac{3.00 \\cdot 10^{8}\\;\\text{m/s}}{5.0 \\cdot 10^{9}\\;\\text{Hz}} = 0.060\\;\\text{m} = 6.0\\;\\text{cm}\\): Mikrowellen. Es ist das WLAN.' },
      { text: 'Die Wärmebildkamera nimmt Strahlung um \\(10\\;\\mu\\text{m}\\) auf. Berechne die Frequenz, dann wähle die Kamera und vergleiche. In welchem Bereich liegt sie?',
        ok: function(s){ return s.geraet === 'ir'; },
        vergleich: '\\(f = \\dfrac{c}{\\lambda} = \\dfrac{3.00 \\cdot 10^{8}\\;\\text{m/s}}{1.0 \\cdot 10^{-5}\\;\\text{m}} = 3.0 \\cdot 10^{13}\\;\\text{Hz}\\): Infrarot — die Wärmestrahlung von Körpern um Raumtemperatur.' },
      { text: 'Starte die Zeitlupe. Was schwingt hier, und in welche Richtungen? Ist die Welle eine Quer- oder eine Längswelle?',
        ok: function(s){ return s.lief; },
        vergleich: 'Es schwingen ein elektrisches Feld \\(E\\) und ein magnetisches Feld \\(B\\) — keine Teilchen. Beide stehen senkrecht aufeinander und senkrecht zur Ausbreitung: eine Querwelle (Transversalwelle). Darum braucht sie kein Medium.' },
      { text: 'Laserpointer oder UV-Lampe: Welche Welle hat die höhere Frequenz, und um welchen Faktor? Wähle beide nacheinander und vergleiche.',
        ok: function(s){ return s.gesehen.gruen && s.gesehen.uv; },
        vergleich: 'UV: \\(365\\;\\text{nm}\\), \\(f \\approx 8.22 \\cdot 10^{14}\\;\\text{Hz}\\); grüner Laser: \\(532\\;\\text{nm}\\), \\(f \\approx 5.64 \\cdot 10^{14}\\;\\text{Hz}\\). Die UV-Frequenz ist rund \\(1.46\\)-mal so gross (\\(\\tfrac{532}{365}\\)): Je kürzer die Wellenlänge, desto höher die Frequenz, bei gleichem \\(c\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Emission, Absorption und Laser ----------
     Ein Modellatom mit drei Energiestufen E₁ < E₂ < E₃; die Stufen E₂ − E₁ und E₃ − E₁ stehen im Verhältnis
     2 : 3. Ein Photon trägt genau die Energie des Sprungs; E = h · f, also f im selben Verhältnis und
     λ = c/f umgekehrt: E₂ → E₁ gibt 600 nm (orange), E₃ → E₁ 400 nm (violett), E₃ → E₂ (Stufe 1) 1200 nm
     (Infrarot, unsichtbar). Modus Emission: anregen (auf E₂ oder E₃), dann zurückspringen; von E₃ abwechselnd
     direkt (400 nm) und über E₂ (1200 nm, dann 600 nm); Richtung des Photons jedes Mal eine andere.
     Modus Absorption: weisses Licht durch das Gas; Atome im Grundzustand nehmen nur 400 nm und 600 nm auf
     (Sprünge nach oben), dahinter fehlen diese Linien. Modus Laser: sieben Atome zwischen zwei Spiegeln
     (rechts teildurchlässig); Pumpen regt alle auf E₂ an und hält sie angeregt. Ein erstes Photon (600 nm)
     läuft der Achse entlang; trifft es auf ein angeregtes Atom, löst es ein gleiches zweites aus (stimulierte
     Emission); am rechten Spiegel tritt rund ein Drittel aus. Ohne Pumpen kein Licht. Unterschied zur
     Themenseite (Animation 6: Elektron auf zwei Bahnen, Resonator): drei Stufen mit Zahlen für die
     Wellenlängen, dazu die Absorption als Umkehrung. Clipbeispiel: Neon 640 nm und Stufe 1.25-mal so gross;
     Startwert Emission, Elektron auf E₁ (kein Leistenziel). */
  var STUFE = { 1: 0, 2: 2, 3: 3 }, LAM5 = { '21': 600, '31': 400, '32': 1200 };
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var stufen = g_(svg), rechts = g_(svg);
    var YE = { 1: 236, 2: 146, 3: 101 }, pruefen = function(){};
    // Zustand der drei Modi
    var niveau = 1, fotonen = [], e3zahl = 0, sprung = null, tSprung = 0, warteschlange = [];
    var absorb = 0, absorbFertig = false;
    var pumpe = false, atome = [], paket = null, hinaus = 0, laserLief = false, laserT = 0, meldung = '';
    var B = Bedienung(fig, function(){ zuruecksetzen(); zeichnen(); });
    var WINKEL = [-0.75, 2.4, 4.3, 5.6, 3.9, 3.5, 0.6, 2.9];   // keiner steil nach unten (Beschriftung über der Photonenliste); Etikett seitlich begrenzt
    function modus(){ return B.wert('modus'); }
    function zuruecksetzen(){ uhr.stop(); niveau = 1; sprung = null; warteschlange = []; absorb = 0; absorbFertig = false;
      pumpe = false; atome = [0, 0, 0, 0, 0, 0, 0].map(function(){ return { an: false, t: 0 }; }); paket = null; hinaus = 0; laserT = 0; meldung = ''; knoepfeSetzen(); }
    var uhr = Uhr(function(tt){
      var dt = tt - (uhr.letzt || 0); uhr.letzt = tt; if (dt > 0.1) dt = 0.1;
      if (modus() === 'emission'){
        tSprung += dt;
        if (sprung && tSprung >= 1.3){ fotonen.push(LAM5[sprung.von + '' + sprung.nach]); niveau = sprung.nach; sprung = warteschlange.shift() || null; tSprung = 0; }
        zeichnen(); if (!sprung){ setTimeout(knoepfeSetzen, 0); return false; }
      } else if (modus() === 'absorption'){
        absorb = Math.min(1, absorb + dt / 2.0); zeichnen(); if (absorb >= 1){ absorbFertig = true; zeichnen(); setTimeout(knoepfeSetzen, 0); return false; }
      } else {
        laserT += dt; schrittLaser(dt); zeichnen(); if (laserT >= 10){ setTimeout(knoepfeSetzen, 0); return false; }
      }
    });
    function starte(){ uhr.letzt = 0; uhr.start(0); }
    // Laser: Atome bei x = 124 + 22 i, Spiegel bei 108 (ganz) und 270 (teildurchlässig)
    var AX = function(i){ return 124 + 22 * i; }, SPL = 108, SPR = 270, VPX = 150;
    function schrittLaser(dt){
      atome.forEach(function(a){ if (!a.an && pumpe){ a.t += dt; if (a.t >= 0.6){ a.an = true; a.t = 0; } } });
      if (!paket) return;
      var alt = paket.x; paket.x += paket.r * VPX * dt;
      atome.forEach(function(a, i){ var x = AX(i); if (a.an && ((alt < x && paket.x >= x) || (alt > x && paket.x <= x))){ a.an = false; a.t = 0; paket.n += 1; } });
      if (paket.x >= SPR){ var raus = Math.max(1, Math.round(paket.n / 3)); hinaus += raus; paket.n = Math.max(1, paket.n - raus); paket.x = 2 * SPR - paket.x; paket.r = -1; }
      if (paket.x <= SPL){ paket.x = 2 * SPL - paket.x; paket.r = 1; }
    }
    var A = aktionen(fig, [
      ['e2', '⚡ auf E₂ anregen', function(){ if (sprung) return; niveau = 2; meldung = 'Energie zugeführt (etwa durch einen Stoss): Das Elektron ist auf E₂.'; zeichnen(); }],
      ['e3', '⚡ auf E₃ anregen', function(){ if (sprung) return; niveau = 3; meldung = 'Energie zugeführt: Das Elektron ist auf E₃.'; zeichnen(); }],
      ['zurueck', '▶ zurückspringen', function(){
        if (sprung) return;
        if (niveau === 1){ meldung = 'Das Elektron ist schon auf E₁, der tiefsten Stufe: Es kann nicht zurückspringen. Rege es zuerst an.'; zeichnen(); return; }
        if (niveau === 2) warteschlange = [{ von: 2, nach: 1 }];
        else { warteschlange = e3zahl % 2 === 0 ? [{ von: 3, nach: 1 }] : [{ von: 3, nach: 2 }, { von: 2, nach: 1 }]; e3zahl++; }
        sprung = warteschlange.shift(); tSprung = 0; meldung = '';
        if (WENIGER){ while (sprung){ fotonen.push(LAM5[sprung.von + '' + sprung.nach]); sprung = warteschlange.shift() || null; } niveau = 1; zeichnen(); }
        else { starte(); knoepfeSetzen(); } }],
      ['licht', '▶ Licht durchschicken', function(){ absorb = 0; absorbFertig = false; if (WENIGER){ absorb = 1; absorbFertig = true; zeichnen(); } else { starte(); knoepfeSetzen(); } }],
      ['pumpen', '⚡ Pumpen an', function(){ pumpe = !pumpe; if (pumpe) atome.forEach(function(a){ a.an = true; a.t = 0; }); knoepfeSetzen(); zeichnen(); }],
      ['laser', '▶ Start', function(){
        hinaus = 0; laserT = 0;
        var erstes = -1; atome.forEach(function(a, i){ if (erstes < 0 && a.an) erstes = i; });
        if (erstes < 0){ paket = null; meldung = 'Kein Atom ist angeregt: Es entsteht kein Photon. Ein Laser braucht Energie von aussen — erst pumpen.'; zeichnen(); return; }
        meldung = ''; atome[erstes].an = false; paket = { x: AX(erstes), r: 1, n: 1 }; laserLief = true;
        if (WENIGER){ for (var k = 0; k < 400; k++) schrittLaser(0.025); laserT = 10; zeichnen(); } else { starte(); knoepfeSetzen(); } }]]);
    function knoepfeSetzen(){
      var m = modus();
      ['e2', 'e3', 'zurueck'].forEach(function(k){ A[k].hidden = m !== 'emission'; A[k].disabled = !!sprung; });
      A.licht.hidden = m !== 'absorption'; A.licht.disabled = uhr.laeuft();
      A.pumpen.hidden = A.laser.hidden = m !== 'laser'; A.pumpen.textContent = pumpe ? '⚡ Pumpen aus' : '⚡ Pumpen an'; A.laser.disabled = uhr.laeuft();
    }
    var sim = {
      zustand: function(){ return { modus: modus(), niveau: niveau, fotonen: fotonen.slice(), absorbFertig: absorbFertig, hinaus: hinaus, laserLief: laserLief, pumpe: pumpe }; },
      zeichnen: function(){ zeichnen(); },
      setze: function(o){ B.setze(o); zuruecksetzen(); zeichnen(); },
      aufraeumen: function(){ zuruecksetzen(); fotonen = []; e3zahl = 0; laserLief = false; B.zuruecksetzen(); },
      // Testhaken (Bilder der Clips): {niveau, fotonen, sprung: [von, nach, Zeit], absorb, pumpe, paket: [x, n], hinaus}
      zeige: function(o){ uhr.stop(); o = o || {}; if (o.modus) B.setze({ modus: o.modus });
        if (o.niveau) niveau = o.niveau; if (o.fotonen) fotonen = o.fotonen.slice();
        sprung = o.sprung ? { von: o.sprung[0], nach: o.sprung[1] } : null; tSprung = o.sprung ? o.sprung[2] : 0;
        if (o.absorb != null){ absorb = o.absorb; absorbFertig = absorb >= 1; }
        if (o.pumpe != null){ pumpe = o.pumpe; atome.forEach(function(a, i){ a.an = o.atome ? !!o.atome[i] : pumpe; }); }
        if (o.paket) paket = { x: o.paket[0], r: 1, n: o.paket[1] }; if (o.hinaus != null) hinaus = o.hinaus;
        meldung = o.meldung || ''; knoepfeSetzen(); zeichnen(); }
    };
    fig.__sim = sim;
    function zeichneStufen(m){
      leeren(stufen);
      el(stufen, 'text', { x: 4, y: 80, 'class': 'bt-klein' }, 'Energie');
      pfeil(stufen, 4, 240, 4, 88, 'achse-pf', 5);
      [1, 2, 3].forEach(function(k){ el(stufen, 'line', { x1: 14, y1: YE[k], x2: 80, y2: YE[k], 'class': 'niveau' });
        stext(stufen, { x: 84, y: YE[k] + 4, 'class': 'bt-wert' }, 'E_' + k); });
      if (m === 'absorption'){
        [[2, 600, 24], [3, 400, 62]].forEach(function(a){ if (absorb > 0){
          pfeil(stufen, a[2], YE[1] - 2, a[2], YE[a[0]] + 3, 'sprung-auf', 6);
          el(stufen, 'text', { x: a[2] + 4, y: (YE[1] + YE[a[0]]) / 2 + 12, 'class': 'bt-klein' }, a[1] + NB + 'nm'); } });
        el(stufen, 'circle', { cx: 46, cy: YE[1], r: 5, 'class': 'elektron' });
        return;
      }
      if (m === 'laser'){ el(stufen, 'text', { x: 14, y: YE[2] - 8, 'class': 'bt-klein' }, 'Laser: E₂ → E₁'); return; }
      var y = YE[niveau];
      if (sprung){ var q = Math.min(1, tSprung / 0.3); y = YE[sprung.von] + (YE[sprung.nach] - YE[sprung.von]) * q;
        pfeil(stufen, 46, YE[sprung.von] + 6, 46, YE[sprung.nach] - 2, 'sprung', 6); }
      el(stufen, 'circle', { cx: 46, cy: y, r: 5, 'class': 'elektron' });
    }
    function streifen(eltern, y, h, fehlen, bis){
      // Spektrum 380 bis 780 nm zwischen x 116 und 296; «fehlen»: Wellenlängen, die dunkel bleiben
      var X = function(nm){ return 116 + (nm - 380) / 400 * 180; };
      for (var nm = 380; nm < 780; nm += 5){ if (X(nm) > 116 + 180 * bis) break;
        var weg = fehlen.some(function(l){ return Math.abs(nm + 2.5 - l) < 6; });
        el(eltern, 'rect', { x: X(nm), y: y, width: 180 / 80 + 0.4, height: h, fill: weg ? '#1c1a17' : spektralfarbe(nm + 2.5) }); }
      el(eltern, 'rect', { x: 116, y: y, width: 180, height: h, 'class': 'band-rahmen' });
      [400, 500, 600, 700].forEach(function(l){ el(eltern, 'text', { x: X(l), y: y + h + 10, 'text-anchor': 'middle', 'class': 'skala' }, String(l)); });
      el(eltern, 'text', { x: 296, y: y + h + 20, 'text-anchor': 'end', 'class': 'achsname' }, 'λ [nm]');
    }
    function zeichneRechts(m){
      leeren(rechts);
      if (m === 'emission'){
        var cx = 200, cy = 150;
        el(rechts, 'circle', { cx: cx, cy: cy, r: 20, 'class': 'atom' });
        el(rechts, 'circle', { cx: cx, cy: cy, r: 4, 'class': 'kern' });
        el(rechts, 'text', { x: cx, y: cy + 36, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Atom');
        if (sprung && tSprung > 0.3){
          var lam = LAM5[sprung.von + '' + sprung.nach], w = WINKEL[fotonen.length % WINKEL.length], q = Math.min(1, (tSprung - 0.3) / 0.8), L = 22 + 64 * q;
          wellig(rechts, cx + 22 * Math.cos(w), cy + 22 * Math.sin(w), cx + L * Math.cos(w), cy + L * Math.sin(w), lam > 780 ? 'ir-photon' : '', null, 3.5);
          rechts.lastChild.previousSibling.setAttribute('stroke', spektralfarbe(lam)); rechts.lastChild.setAttribute('fill', spektralfarbe(lam));
          if (q >= 1) el(rechts, 'text', { x: Math.max(24, Math.min(276, cx + (L + 10) * Math.cos(w))), y: cy + (L + 10) * Math.sin(w) + 4, 'text-anchor': 'middle', 'class': 'bt-wert' }, lam + NB + 'nm');
        }
        el(rechts, 'text', { x: 108, y: 238, 'class': 'bt-klein' }, 'Photonen bisher:');
        fotonen.slice(-4).forEach(function(l, k){ var x = 108 + 46 * k;
          el(rechts, 'rect', { x: x + 4, y: 244, width: 30, height: 8, rx: 2, fill: spektralfarbe(l), 'class': l > 780 ? 'ir-kaestchen' : '' });
          el(rechts, 'text', { x: x + 19, y: 263, 'text-anchor': 'middle', 'class': 'skala' }, l + NB + 'nm'); });
      } else if (m === 'absorption'){
        el(rechts, 'text', { x: 116, y: 60, 'class': 'bt-klein' }, 'Licht der Lampe (vor dem Gas):');
        streifen(rechts, 64, 14, [], 1);
        el(rechts, 'rect', { x: 150, y: 118, width: 112, height: 50, rx: 6, 'class': 'gaszelle' });
        for (var i = 0; i < 6; i++) el(rechts, 'circle', { cx: 164 + 17 * i, cy: 143 + (i % 2 ? 7 : -7), r: 3.5, 'class': 'kern' });
        el(rechts, 'text', { x: 206, y: 182, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Gas aus diesen Atomen (alle auf E₁)');
        pfeil(rechts, 112, 143, 148, 143, 'pf-licht', 7);
        el(rechts, 'text', { x: 108, y: 134, 'class': 'bt-klein' }, 'weiss');
        if (absorb > 0){ pfeil(rechts, 264, 143, 290, 143, 'pf-licht', 7);
          el(rechts, 'text', { x: 116, y: 206, 'class': 'bt-klein' }, 'hinter dem Gas:'); streifen(rechts, 210, 14, [400, 600], absorb); }
      } else {
        el(rechts, 'rect', { x: SPL, y: 110, width: SPR - SPL, height: 78, rx: 4, 'class': 'gaszelle' });
        el(rechts, 'line', { x1: SPL, y1: 104, x2: SPL, y2: 194, 'class': 'spiegel' });
        el(rechts, 'line', { x1: SPR, y1: 104, x2: SPR, y2: 194, 'class': 'spiegel teil' });
        el(rechts, 'text', { x: SPL - 3, y: 98, 'class': 'bt-klein' }, 'Spiegel');
        el(rechts, 'text', { x: SPR, y: 98, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'teildurchlässig');
        atome.forEach(function(a, i){ var x = AX(i);
          el(rechts, 'circle', { cx: x, cy: 168, r: 7, 'class': 'atom' + (a.an ? ' angeregt' : '') });
          el(rechts, 'circle', { cx: x, cy: a.an ? 162 : 174, r: 2.4, 'class': 'elektron' }); });
        el(rechts, 'text', { x: 189, y: 204, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Atome: hell = angeregt (E₂), Elektron oben');
        if (paket){ var rows = Math.min(5, paket.n), x0 = paket.x - 12 * paket.r;
          for (var k = 0; k < rows; k++){ wellig(rechts, x0, 132 + 5 * k, x0 + 24 * paket.r, 132 + 5 * k, '', 3, 2);
            rechts.lastChild.previousSibling.setAttribute('stroke', spektralfarbe(600)); rechts.lastChild.setAttribute('fill', spektralfarbe(600)); }
          el(rechts, 'text', { x: paket.x, y: 124, 'text-anchor': 'middle', 'class': 'bt-wert' }, paket.n + ' Photonen'); }
        if (hinaus > 0){ var h = Math.min(22, 3 + 1.2 * Math.sqrt(hinaus));
          el(rechts, 'rect', { x: SPR + 2, y: 155 - h / 2, width: 30, height: h, fill: spektralfarbe(600), opacity: 0.85 });
          el(rechts, 'text', { x: 300, y: 228, 'text-anchor': 'end', 'class': 'bt-wert' }, 'Laserstrahl: ' + hinaus + ' Photonen'); }
        el(rechts, 'text', { x: 108, y: 246, 'class': 'bt-klein' }, pumpe ? 'Pumpen an: Energie von aussen' : 'Pumpen aus');
      }
    }
    function zeichnen(){
      var m = modus(); B.anzeigen(); zeichneStufen(m); zeichneRechts(m);
      var s;
      if (m === 'emission') s = '<span>Photon: ' + v_('E') + '<sub>Photon</sub> = ' + v_('E') + '<sub>oben</sub> − ' + v_('E') + '<sub>unten</sub> = ' + v_('h') + ' · ' + v_('f') + '; grössere Stufe → höhere Frequenz → kürzere Wellenlänge.</span>'
                             + '<span>Die Stufen E₂ − E₁ und E₃ − E₁ stehen im Verhältnis 2 : 3; die kleine Stufe E₃ − E₂ ist halb so gross wie E₂ − E₁. Die Wellenlänge jedes Photons steht unten, sobald es ausgesandt ist.</span>';
      else if (m === 'absorption') s = '<span>Ein Atom auf E₁ nimmt nur Photonen auf, deren Energie genau zu einem Sprung nach oben passt' + (absorbFertig ? ': E₁ → E₂ (600' + NB + 'nm) und E₁ → E₃ (400' + NB + 'nm).' : '.') + '</span>';
      else s = '<span>Stimulierte Emission: Ein Photon trifft ein angeregtes Atom und löst ein zweites aus — gleiche Wellenlänge (600' + NB + 'nm), gleiche Richtung, gleicher Takt.</span>';
      if (meldung) s += '<span class="warnzeile">' + meldung + '</span>';
      s += '<span class="sim-notiz">Modellatom mit drei Stufen; Photonen in ihrer Farbe, Infrarot dunkelrot gestrichelt (unsichtbar).</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    zuruecksetzen();
    pruefen = Leiste(fig, [
      { text: 'Rege das Elektron auf E₂ an und lass es zurückspringen. Welche Wellenlänge hat das Photon, welche Farbe? Notiere.',
        setup: function(sim){ if (sim.zustand().modus !== 'emission') sim.setze({ modus: 'emission' }); },
        ok: function(s){ return s.modus === 'emission' && s.fotonen.indexOf(600) >= 0; },
        vergleich: '\\(600\\;\\text{nm}\\), orange. Das Photon trägt genau die Energie der Stufe von E₂ nach E₁.' },
      { text: 'Rege jetzt auf E₃ an und lass das Elektron mehrmals zurückspringen, bis du drei verschiedene Photonen gesehen hast. Wie hängen ihre Wellenlängen mit den Stufen zusammen?',
        ok: function(s){ return s.modus === 'emission' && [400, 1200, 600].every(function(l){ return s.fotonen.indexOf(l) >= 0; }); },
        vergleich: 'Direkt von E₃ nach E₁: \\(400\\;\\text{nm}\\), violett. Die Stufe ist \\(1.5\\)-mal so gross wie von E₂ nach E₁, die Frequenz \\(1.5\\)-mal so hoch, die Wellenlänge \\(\\dfrac{600\\;\\text{nm}}{1.5} = 400\\;\\text{nm}\\). Über E₂: zuerst die kleine Stufe, \\(1200\\;\\text{nm}\\) (Infrarot, unsichtbar), dann \\(600\\;\\text{nm}\\).' },
      { text: 'Wähle «Absorption» und schicke weisses Licht durch das Gas. Welche Wellenlängen fehlen dahinter — und warum genau diese?',
        ok: function(s){ return s.modus === 'absorption' && s.absorbFertig; },
        vergleich: '\\(400\\;\\text{nm}\\) und \\(600\\;\\text{nm}\\) fehlen. Ein Atom auf E₁ nimmt nur ein Photon auf, dessen Energie genau zu einem Sprung nach oben passt (E₁ → E₂, E₁ → E₃). Alle anderen Wellenlängen gehen durch. Absorption ist die Umkehrung der Emission — aber nur für Sprünge, die von der besetzten Stufe ausgehen: Die \\(1200\\;\\text{nm}\\) (E₂ → E₃) fehlen nicht, weil kein Elektron auf E₂ sitzt.' },
      { text: 'Wähle «Laser», schalte das Pumpen ein und starte. Vergleiche die Photonen im Laserstrahl mit der einzelnen Emission: Wellenlänge, Richtung, Takt.',
        ok: function(s){ return s.modus === 'laser' && s.hinaus >= 10; },
        vergleich: 'Alle Photonen haben \\(600\\;\\text{nm}\\), laufen in dieselbe Richtung und schwingen im gleichen Takt (gleiche Phase): Ein Photon löst an einem angeregten Atom ein gleiches zweites aus — stimulierte Emission. Zwischen den Spiegeln werden es immer mehr; durch den teildurchlässigen Spiegel tritt der Laserstrahl aus. Bei der einzelnen Emission war die Richtung jedes Mal eine andere.' }
    ], sim);
    knoepfeSetzen(); zeichnen();
  })();

  /* ---------- Kapitel 6: Durchlässigkeit der Atmosphäre nach Wellenlänge ----------
     Oben die Strahlung der Sonne (5800 K) und des Bodens (288 K, rund 15 °C) über der Wellenlänge
     (logarithmisch, 0.1 µm bis 100 µm), je auf gleiche Höhe gebracht (Planck-Kurven, Maxima bei 0.50 µm und
     10.1 µm). Grau: die Bereiche, in denen die gewählten Gase stark aufnehmen — vereinfacht ganz dunkel oder
     ganz durchlässig, wie im Leitprogramm Wärme (Aufgabe 7c): Wasserdampf 5.5 bis 7.5 µm und ab 20 µm,
     Kohlendioxid um 15.25 µm mit der halben Breite 1.75 µm · (1 + 0.25 · log₂(C/430 ppm)) (bei 430 ppm 13.5 bis
     17.0 µm; mehr Gas nimmt auch an den Rändern des Bands auf), Methan 7.4 bis 8.0 µm und Ozon 9.3 bis 10.1 µm (mitten im Fenster).
     Gezeichnet ist λ · B_λ (flächentreu über log λ): Gipfel bei 0.63 µm und 12.7 µm; je Mikrometer liegen die Maxima bei
     0.50 µm und 10.1 µm. Die Anteile sind
     Integrale der Planck-Kurven über log λ (0.05 µm bis 1000 µm, 2000 Stützstellen). Unten ein Schema: Licht
     kommt durch, die aufgenommene Bodenstrahlung strahlen die Gase nach allen Seiten wieder ab; Pfeilbreiten
     nach den Anteilen, keine Watt — die Energiebilanz rechnet das Leitprogramm Wärme (Kapitel 7). Nicht im Modell:
     Aufnahme von Sonnenlicht (Ultraviolett durch Ozon, Wasserdampf im nahen Infrarot), Wolken, Streuung. Unterschied zur Themenseite
     (Animation 7: Regler für die Treibhausgase und ein Pfeilschema in Watt) und zum Leitprogramm Wärme (sim7:
     Einschichtmodell mit Temperaturen): welche Gase bei welchen Wellenlängen aufnehmen. Startwerte: Wasserdampf und
     Kohlendioxid, 430 ppm (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim6'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var dia = g_(svg, { transform: 'translate(0,14)' }), schema = g_(svg), kopf = g_(svg), pruefen = function(){};
    var gesehen = {};
    var B = Bedienung(fig, function(){ merke(); zeichnen(); });
    var C2 = 14388, NS = 2000, LO = Math.log10(0.05), HI = Math.log10(1000), GS = [], GE = [], LAM = [];
    function planck(l, T){ var e = C2 / (l * T); return e > 700 ? 0 : Math.pow(l, -5) / (Math.exp(e) - 1); }
    (function(){ for (var i = 0; i < NS; i++){ var l = Math.pow(10, LO + (HI - LO) * (i + 0.5) / NS); LAM.push(l); GS.push(planck(l, 5800) * l); GE.push(planck(l, 288) * l); } })();
    var SUMS = GS.reduce(function(a, b){ return a + b; }, 0), SUME = GE.reduce(function(a, b){ return a + b; }, 0);
    function co2(C){ if (C <= 0) return null; var w = 1.75 * (1 + 0.25 * Math.log2(C / 430)); return w > 0 ? [15.25 - w, 15.25 + w] : null; }
    function baender(stufe, C){
      var b = [];
      if (stufe >= 1){ b.push([5.5, 7.5, 'H₂O']); b.push([20, 1000, 'H₂O']); }
      if (stufe >= 2){ var c = co2(C); if (c) b.push([c[0], c[1], 'CO₂']); }
      if (stufe >= 3){ b.push([7.4, 8.0, 'CH₄']); b.push([9.3, 10.1, 'O₃']); }
      return b;
    }
    function anteil(G, S, b){ var s = 0; for (var i = 0; i < NS; i++){ var l = LAM[i]; for (var k = 0; k < b.length; k++) if (l >= b[k][0] && l <= b[k][1]){ s += G[i]; break; } } return s / S; }
    function werte(){ var st = +B.wert('gase'), C = B.wert('ppm'), b = baender(st, C);
      return { stufe: st, ppm: C, b: b, sonne: anteil(GS, SUMS, b), boden: anteil(GE, SUME, b), gesehen: gesehen }; }
    function merke(){ var w = werte(); if (w.stufe >= 2) gesehen[w.ppm] = true; }
    var sim = {
      zustand: function(){ return werte(); }, zeichnen: function(){ zeichnen(); },
      setze: function(o){ B.setze(o); merke(); zeichnen(); },
      aufraeumen: function(){ gesehen = {}; merke(); B.zuruecksetzen(); },
      zeige: function(o){ if (o) B.setze(o); zeichnen(); }
    };
    fig.__sim = sim;
    function U(l){ return Math.log10(l) + 1.2; }                  // x-Koordinate: log₁₀(λ/µm) + 1.2
    function zeichnen(){
      var w = werte(), i; B.anzeigen(); leeren(dia); leeren(schema); leeren(kopf);
      el(kopf, 'text', { x: 0, y: 6, 'class': 'bt-klein' }, 'Strahlung je Stück der log-Achse (flächentreu), auf gleiche Höhe gebracht');
      var K = Achsen(dia, { w: 300, h: 150, x0: -0.05, x1: 3.4, y0: -0.12, y1: 1.18, sx: 100, sy: 100, xm: [], ym: [], xname: ' ', yname: 'relativ' });
      // Gitter und Teilung je Zehnerpotenz; Achsenname unter der Teilung (die Kurve des Bodens reicht bis an den rechten Rand)
      [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100].forEach(function(l){ el(K.ebene, 'line', { x1: K.X(U(l)), y1: K.Y(1.18), x2: K.X(U(l)), y2: K.Y(0), 'class': 'gitter' });
        if ([0.1, 0.5, 1, 10, 100].indexOf(l) >= 0) el(K.ebene, 'text', { x: K.X(U(l)), y: K.Y(0) + 12, 'text-anchor': 'middle', 'class': 'skala' }, String(l)); });
      el(K.ebene, 'text', { x: 300, y: K.Y(0) + 25, 'text-anchor': 'end', 'class': 'achsname' }, 'λ [µm], logarithmisch');
      // sichtbares Licht als schmaler Streifen
      el(K.ebene, 'rect', { x: K.X(U(0.38)), y: K.Y(1.18), width: K.X(U(0.78)) - K.X(U(0.38)), height: K.Y(0) - K.Y(1.18), 'class': 'fl-vis' });
      el(K.ebene, 'text', { x: K.X(U(0.55)), y: K.Y(1.1), 'text-anchor': 'middle', 'class': 'bt-klein' }, 'sichtbar');
      // Aufnahmebereiche der Gase
      w.b.forEach(function(b){ var a = Math.max(U(b[0]), -0.05), e = Math.min(U(b[1]), 3.4);
        el(K.ebene, 'rect', { x: K.X(a), y: K.Y(1.18), width: K.X(e) - K.X(a), height: K.Y(0) - K.Y(1.18), 'class': 'fl-rest' }); });
      var namen = {};
      w.b.forEach(function(b){ var m = b[1] > 100 ? U(40) : (U(b[0]) + U(b[1])) / 2; if (namen[b[2] + Math.round(m)]) return; namen[b[2] + Math.round(m)] = true;
        el(K.ebene, 'text', { x: K.X(m) - (b[2] === 'CH₄' ? 8 : 0), y: K.Y(b[2] === 'CH₄' ? 0.8 : b[2] === 'O₃' ? 0.1 : 1.1), 'text-anchor': b[2] === 'CH₄' ? 'end' : 'middle', 'class': 'bt-wert gas-name' }, b[2]); });   // CH₄ links neben, O₃ unten in seinem Band   // CH₄ tiefer: sein Band grenzt an das des Wasserdampfs
      // Kurven: Sonne (Orange) und Boden (Rot)
      // λ · B_λ: je Stück der log-Achse; die Fläche unter der Kurve ist die Strahlung (Maxima bei 0.63 µm und 12.7 µm)
      var ms = planck(0.6327, 5800) * 0.6327, me = planck(12.74, 288) * 12.74;
      K.kurve(function(u){ var l = Math.pow(10, u - 1.2); return planck(l, 5800) * l / ms; }, 'k-sonne', 0, 3.4);
      K.kurve(function(u){ var l = Math.pow(10, u - 1.2); return planck(l, 288) * l / me; }, 'k-boden', 0, 3.4);
      el(K.ebene, 'text', { x: K.X(U(1.1)), y: K.Y(0.8), 'class': 'bt-wert l-licht' }, 'Sonne');
      el(K.ebene, 'text', { x: K.X(U(4.6)), y: K.Y(0.5), 'text-anchor': 'end', 'class': 'bt-wert l-ir' }, 'Boden');
      // Schema: Sonne, Atmosphäre, Boden (Pfeilbreiten nach den Anteilen, Zahlen in der Formelzeile)
      var ya1 = 236, ya2 = 258, yb = 292, k = 16;
      el(schema, 'rect', { x: 0, y: ya1, width: 300, height: ya2 - ya1, 'class': 'atmo', opacity: (0.12 + 0.55 * w.boden).toFixed(2) });
      el(schema, 'text', { x: 188, y: ya1 + 14, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Gase der Atmosphäre');
      el(schema, 'rect', { x: 0, y: yb, width: 300, height: 8, 'class': 'boden' });
      el(schema, 'circle', { cx: 12, cy: 208, r: 8, 'class': 'sonne' });
      band(30, 214, yb - 2, 1 - w.sonne, 'licht', k);
      el(schema, 'text', { x: 42, y: 280, 'class': 'bt-wert l-licht' }, 'Licht');
      band(120, yb - 2, ya2, 1, 'ir', k);
      el(schema, 'text', { x: 132, y: 280, 'class': 'bt-wert l-ir' }, 'Bodenstrahlung');
      if (w.boden < 0.999){ band(120, ya1, 204, 1 - w.boden, 'ir', k); el(schema, 'text', { x: 132, y: 214, 'class': 'bt-wert l-ir' }, 'ins All'); }
      if (w.boden > 0.005){ band(252, ya1, 204, w.boden / 2, 'ir atm', k); band(278, ya2, yb - 2, w.boden / 2, 'ir atm', k);
        el(schema, 'text', { x: 244, y: 214, 'text-anchor': 'end', 'class': 'bt-wert l-ir' }, 'ins All');
        el(schema, 'text', { x: 270, y: 280, 'text-anchor': 'end', 'class': 'bt-wert l-ir' }, 'zurück'); }
      var s = '<span>Im Bandmodell in den grauen Bereichen: Sonnenlicht ' + fest(100 * w.sonne, 1) + NB + '%; Wärmestrahlung des Bodens ' + fest(100 * w.boden, 0) + NB + '%</span>';
      s += '<span>' + (w.stufe === 0 ? 'Stickstoff und Sauerstoff allein nehmen weder Licht noch Wärmestrahlung nennenswert auf.' : 'Was die Gase aufnehmen, strahlen sie in alle Richtungen wieder ab — auch zurück zum Boden.') + '</span>';
      s += '<span class="sim-notiz">Die Kurven zeigen die Strahlung je Stück der log-Achse (flächentreu); ihre Gipfel liegen darum bei rund 0.6 µm und 13 µm, je Mikrometer liegen die Maxima bei 0.5 µm und 10 µm. Bandmodell: In den grauen Bereichen nimmt das Gas alles auf, sonst nichts; Wolken, schwächere Banden, Streuung und die Aufnahme von Sonnenlicht sind weggelassen. Die Prozente sind darum nicht mit dem Einschichtmodell des Leitprogramms Wärme vergleichbar; die echte Atmosphäre nimmt mehr Bodenstrahlung auf. Pfeilbreiten nach den Anteilen; die Energiebilanz in Watt rechnet das Leitprogramm Wärme.</span>';
      rolle(fig, 'formel').innerHTML = s;
      pruefen();
    }
    function band(x, y1, y2, anteil, cls, k){
      var b = Math.max(1, anteil * k), dir = y2 > y1 ? 1 : -1, s = Math.max(5, b * 0.35);
      el(schema, 'rect', { x: x - b / 2, y: Math.min(y1, y2), width: b, height: Math.abs(y2 - y1), 'class': cls });
      el(schema, 'polygon', { points: (x - b / 2 - 3) + ',' + (y2 - dir * s) + ' ' + (x + b / 2 + 3) + ',' + (y2 - dir * s) + ' ' + x + ',' + (y2 + dir * 2), 'class': cls });
    }
    merke();
    pruefen = Leiste(fig, [
      { text: 'Stelle «keine Treibhausgase» ein: nur Stickstoff und Sauerstoff. Wie viel der Wärmestrahlung des Bodens nimmt die Luft auf? Notiere, dann vergleiche.',
        ok: function(s){ return s.stufe === 0; },
        vergleich: '\\(0\\;\\%\\): Stickstoff und Sauerstoff, rund \\(99\\;\\%\\) der Luft, nehmen weder Licht noch Wärmestrahlung nennenswert auf. Ohne Treibhausgase ginge die ganze Bodenstrahlung ins All; die Erde wäre im Mittel rund \\(-18\\;^\\circ\\text{C}\\) kalt statt rund \\(+15\\;^\\circ\\text{C}\\).' },
      { text: 'Nimm den Wasserdampf dazu. Welche der beiden Strahlungen trifft das vor allem? Notiere beide Anteile.',
        ok: function(s){ return s.stufe === 1; },
        vergleich: 'Im Bandmodell: Sonnenlicht \\(0.2\\;\\%\\), Bodenstrahlung \\(36\\;\\%\\). Die Bereiche des Wasserdampfs liegen im Infrarot, weit weg vom Licht der Sonne (je Mikrometer am stärksten um \\(0.5\\;\\mu\\text{m}\\)), aber mitten in der Strahlung des Bodens um \\(10\\;\\mu\\text{m}\\).' },
      { text: 'Nimm das Kohlendioxid dazu: zuerst \\(280\\;\\text{ppm}\\) wie vor der Industrialisierung, dann \\(430\\;\\text{ppm}\\) wie heute. Wie verändert sich sein Bereich, wie der Anteil der Bodenstrahlung?',
        ok: function(s){ return s.stufe >= 2 && s.gesehen[280] && s.gesehen[430]; },
        vergleich: 'Der Bereich um \\(15\\;\\mu\\text{m}\\) wird breiter: Mehr Gas nimmt auch an den Rändern des Bereichs auf, wo es schwächer aufnimmt. Der Anteil der Bodenstrahlung in den grauen Bereichen steigt im Bandmodell um rund \\(2\\) bis \\(3\\) Prozentpunkte. Mehr Wärmestrahlung bleibt in der Atmosphäre und wird auch zum Boden zurückgestrahlt — der Treibhauseffekt wird stärker.' },
      { text: 'Nimm auch Methan und Ozon dazu. Wo bleibt jetzt noch eine grosse Lücke, durch die Bodenstrahlung direkt ins All gelangt? Lies die Wellenlängen ab.',
        ok: function(s){ return s.stufe === 3; },
        vergleich: 'Zwischen rund \\(8\\;\\mu\\text{m}\\) und \\(13\\;\\mu\\text{m}\\), im «Fenster»; nur das Ozon nimmt darin schmal um \\(9.6\\;\\mu\\text{m}\\) auf. Gerade dort strahlt der Boden viel (je Mikrometer am stärksten um \\(10\\;\\mu\\text{m}\\)); durch dieses Fenster gelangt seine Strahlung im Modell ungehindert ins All.' },
      { text: 'Stelle mit allen Gasen \\(800\\;\\text{ppm}\\) Kohlendioxid ein. Warum ändert sich am Sonnenlicht fast nichts, an der Bodenstrahlung aber schon?',
        ok: function(s){ return s.stufe === 3 && s.ppm === 800; },
        vergleich: 'Sonnenlicht: fast unverändert (im Bandmodell \\(0.3\\;\\%\\)); Bodenstrahlung: im Bandmodell um rund \\(3\\) bis \\(4\\) Prozentpunkte mehr (von rund \\(60\\;\\%\\) auf \\(63\\;\\%\\)). Kohlendioxid nimmt vor allem im Infrarot um \\(15\\;\\mu\\text{m}\\) auf. Dort strahlt die Sonne fast nichts (je Mikrometer am stärksten um \\(0.5\\;\\mu\\text{m}\\)), der Boden dagegen viel. Mehr Kohlendioxid wirkt darum auf dem Rückweg der Strahlung, nicht auf dem Hinweg.' }
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
    // Einheit in LaTeX; µ gehört nicht in \text{} (HOWTO §15)
    function eh(u){ return u.charAt(0) === 'µ' ? '\\;\\mu\\text{' + u.slice(1) + '}' : '\\;\\text{' + u + '}'; }
    function ein(x, u){ return tz(x) + eh(u); }
    function lesen(s){
      var komma = /\d,\d/.test(s);
      s = String(s).trim().replace(/−/g, '-').replace(',', '.').replace(/\s+/g, '').replace(/^\+(?=[\d.])/, '');
      if (!s) return { wert: NaN, leer: true };
      var m = s.match(/^(-?(?:\d+(?:\.\d+)?|\.\d+))\/(\d+(?:\.\d+)?|\.\d+)$/);
      return { wert: m ? parseFloat(m[1]) / parseFloat(m[2]) : (/^-?(\d+(\.\d+)?|\.\d+)(e[-+]?\d+)?$/i.test(s) ? parseFloat(s) : NaN), komma: komma };
    }
    // Ergebnis mit «=» oder «≈», drei signifikante Stellen
    function erg(x, u){ var r = +(+x).toPrecision(3); return (Math.abs(r - x) < 1e-9 * Math.max(1, Math.abs(x)) ? '= ' : '\\approx ') + ein(r, u); }
    // Fehlermuster müssen verschiedene Zahlen ergeben (HOWTO §15): alle Werte paarweise 2 % auseinander
    function verschieden(l){ for (var i = 0; i < l.length; i++) for (var j = i + 1; j < l.length; j++) if (Math.abs(l[i] - l[j]) <= 0.02 * Math.max(Math.abs(l[i]), Math.abs(l[j]))) return false; return true; }
    var CTEX = '3.00 \\cdot 10^{8}\\;\\text{m/s}';
    // Feste Beispiele (Clips, Kontrollfragen, Leisten, Festhalten, Kapitelaufgaben, Gesamttest, Themenseite 6.1
    // und 6.1a) kommen in den Wertelisten nicht vor; geprüft mit scripts/lp/wellen/pruef_fest.py.

    // ---- Minidiagramm für «ablesen»: Momentbild oder Zeitdiagramm, Berge auf Gitterlinien
    function wellenbild(A){
      var w = 262, h = 150, ox = 30, oy = 76, R = w - ox - 14, ky = 14, n = A.zellen, kx = R / n, d = [], i;
      var t = ['<svg class="mini breit" viewBox="0 0 ' + w + ' ' + (h + 16) + '" role="img" aria-label="' + (A.art === 'mb' ? 'Momentbild einer Welle' : 'Zeitdiagramm eines Punkts') + '">'];
      for (i = 0; i <= n; i++) t.push('<line x1="' + (ox + i * kx).toFixed(1) + '" y1="' + (oy - 4.4 * ky) + '" x2="' + (ox + i * kx).toFixed(1) + '" y2="' + (oy + 4.4 * ky) + '" class="gitter"/>');
      for (i = -4; i <= 4; i++) t.push('<line x1="' + ox + '" y1="' + (oy - i * ky) + '" x2="' + (ox + R) + '" y2="' + (oy - i * ky) + '" class="gitter"/>');
      t.push('<line x1="' + ox + '" y1="' + oy + '" x2="' + (ox + R + 8) + '" y2="' + oy + '" class="achse"/><line x1="' + ox + '" y1="' + (oy + 4.6 * ky) + '" x2="' + ox + '" y2="' + (oy - 4.8 * ky) + '" class="achse"/>');
      for (i = A.lab; i <= n; i += A.lab) t.push('<text x="' + (ox + i * kx).toFixed(1) + '" y="' + (oy + 4.4 * ky + 12) + '" text-anchor="middle" class="skala">' + tz(+(i * A.gs).toPrecision(6)) + '</text>');
      [-3, 3].forEach(function(v){ t.push('<text x="' + (ox - 4) + '" y="' + (oy - v * ky + 3.5) + '" text-anchor="end" class="skala">' + (v < 0 ? '−' : '') + Math.abs(v) + '</text>'); });
      for (i = 0; i <= 400; i++){ var x = i / 400 * n * A.gs, y = 3 * Math.cos(2 * Math.PI * (x - A.x0) / A.wert); d.push((ox + x / A.gs * kx).toFixed(1) + ',' + (oy - y * ky).toFixed(1)); }
      t.push('<polyline points="' + d.join(' ') + '" class="kurve-mini k-w"/>');
      t.push('<text x="' + (ox + R + 8) + '" y="' + (oy + 4.4 * ky + 26) + '" text-anchor="end" class="achsname">' + (A.art === 'mb' ? 's [m]' : 't [s]') + '</text>');
      t.push('<text x="' + (ox + 4) + '" y="' + (oy - 4.8 * ky - 2) + '" class="achsname">y [cm]</text></svg>');
      return t.join('');
    }

    /* Zahlenpaare, die in festen Beispielen stehen (Clips, Aufgaben, Gesamttest, Themenseite 6.1 und 6.1a):
       Eine Zufallsaufgabe mit genau diesen sichtbaren Zahlen wird neu gewürfelt (scripts/lp/wellen/pruef_fest.py). */
    var FEST_PAARE = ['1|10', '1|7', '8|25', '1.2|2.5', '0.6|2.4', '1.5|2', '2|2.5', '4.8|6', '4|8', '4|6', '1.5|4', '2|4',
                      '0.5|1.5', '0.8|1.6', '2|6', '0.3|60', '0.8|2', '0.8|2.4', '1.5|6', '2|10', '1.5|2.5', '0.5|680',
                      '2|3', '0.3|3', '0.8|3', '1.5|3', '0.5|3', '2.4|3', '3|6', '1.5|20'];   // zweite Prüfung: Paare mit 3 (vorher als Konstante übersehen)
    function fest_(a, b){ return FEST_PAARE.indexOf([+a, +b].sort(function(x, y){ return x - y; }).join('|')) >= 0; }
    var TYPEN = {
      /* ----- Kapitel 1: Von der Schwingung zur Welle ----- */
      'periode': { felder: ['x'], muster: function(A){ return A.art === 'f' ? '<i>f</i> = {x} Hz' : '<i>T</i> = {x} s'; },
        neu: function(){
          var k, n, t, ts, art, l;
          do {
            k = zufall([['Eine Boje im Hafen hebt und senkt sich', 'min', [7, 9, 10, 20], [1, 1.5, 2]], ['Ein Kind auf der Schaukel schwingt', 's', [8, 10, 12], [24, 30]],
                        ['Ein Kolibri schlägt mit den Flügeln', 's', [100, 120, 150], [2, 2.5]], ['Die Membran eines Basslautsprechers schwingt', 's', [240, 300, 360], [4, 5]]]);
            n = zufall(k[2]); t = zufall(k[3]); ts = k[1] === 'min' ? 60 * t : t; art = zufall(['f', 'T']);
            l = [n / ts, ts / n]; if (k[1] === 'min') l.push(n / t, t / n);
          } while (!verschieden(l) || fest_(n, t));
          return { art: art, n: n, t: t, ts: ts, min: k[1] === 'min', x: art === 'f' ? n / ts : ts / n,
            text: k[0] + ' ' + n + '-mal in \\(' + ein(t, k[1]) + '\\). Wie gross ist ' + (art === 'f' ? 'die Frequenz' : 'die Periode') + '?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.art === 'f' ? A.ts / A.n : A.n / A.ts)) return A.art === 'f' ? 'Das ist die Dauer einer Schwingung, die Periode. Gefragt ist die Frequenz: Schwingungen pro Sekunde.' : 'Das ist die Anzahl Schwingungen pro Sekunde, die Frequenz. Gefragt ist die Dauer einer Schwingung.';
          if (A.min && nah(e.x, A.art === 'f' ? A.n / A.t : A.t / A.n)) return 'Die Zeit steht in Minuten. Rechne sie zuerst in Sekunden um: \\(1\\;\\text{min} = 60\\;\\text{s}\\).';
          return A.art === 'f' ? '\\(f = \\dfrac{\\text{Anzahl Schwingungen}}{\\text{Zeit}}\\), die Zeit in Sekunden.' : '\\(T = \\dfrac{\\text{Zeit}}{\\text{Anzahl Schwingungen}}\\), in Sekunden.'; },
        fehler: function(A){ var l = [[{ x: String(A.art === 'f' ? A.ts / A.n : A.n / A.ts) }, A.art === 'f' ? 'Periode' : 'Frequenz']]; if (A.min) l.push([{ x: String(A.art === 'f' ? A.n / A.t : A.t / A.n) }, 'Minuten']); return l; },
        loesung: function(A){ var z = A.min ? 't = ' + ein(A.t, 'min') + ' = ' + ein(A.ts, 's') + ',\\quad ' : '';
          return z + (A.art === 'f' ? 'f = \\dfrac{n}{t} = \\dfrac{' + A.n + '}{' + ein(A.ts, 's') + '} ' + erg(A.x, 'Hz') : 'T = \\dfrac{t}{n} = \\dfrac{' + ein(A.ts, 's') + '}{' + A.n + '} ' + erg(A.x, 's')); } },
      'laufzeit': { felder: ['x'], muster: function(A){ return { c: '<i>c</i> = {x} m/s', t: '<i>t</i> = {x} s', s: '<i>s</i> = {x} m' }[A.art]; },
        neu: function(){
          var k, art, s, t, c, cm, l;
          do {
            k = zufall([['Ein Stoss läuft über ein gespanntes Seil', [4.0, 6.4, 9.6, 12], [0.8, 1.2, 1.6, 2.4], [3.2, 4.5, 6.0, 8.0], false, 'er'],
                        ['Eine Wasserwelle läuft über einen Teich', [2.4, 3.6, 4.8], [4, 5, 6, 8], [0.4, 0.6, 0.75], false, 'sie'],
                        ['Eine Störung läuft über ein langes Gummiseil', [240, 300, 450], [1.2, 1.5, 2.5], [1.5, 2.0, 2.5], true, 'sie']]);
            art = zufall(['c', 't', 's']); cm = k[4];
            if (art === 'c'){ s = zufall(k[1]); t = zufall(k[2]); c = (cm ? s / 100 : s) / t; }
            else if (art === 't'){ s = zufall(k[1]); c = zufall(k[3]); t = (cm ? s / 100 : s) / c; }
            else { c = zufall(k[3]); t = zufall(k[2]); s = c * t; cm = false; }
            var sm = cm ? s / 100 : s;
            l = art === 'c' ? [c, t / sm, sm * t] : art === 't' ? [t, c / sm, sm * c] : [s, c / t, t / c];
            if (cm && art !== 's') l.push(art === 'c' ? s / t : s / c);
          } while (!verschieden(l) || (art === 'c' && (c < k[3][0] * 0.6 || c > k[3][k[3].length - 1] * 1.4)) || (art === 't' && (t < 0.4 || t > 30)) || fest_(art === 's' ? c : +(cm ? s : +s.toPrecision(3)), art === 't' ? c : +t.toPrecision(3)));
          var sTxt = cm ? ein(s, 'cm') : ein(+s.toPrecision(3), 'm');
          var text = art === 'c' ? k[0] + ' in \\(' + ein(+t.toPrecision(3), 's') + '\\) um \\(' + sTxt + '\\) weiter. Wie schnell läuft die Welle?'
                   : art === 't' ? k[0] + ' mit \\(c = ' + ein(c, 'm/s') + '\\). Wie lange braucht ' + k[5] + ' für \\(' + sTxt + '\\)?'
                   : k[0] + ' mit \\(c = ' + ein(c, 'm/s') + '\\). Wie weit kommt ' + k[5] + ' in \\(' + ein(t, 's') + '\\)?';
          return { art: art, s: s, t: t, c: c, cm: cm, sm: cm ? s / 100 : s, x: art === 'c' ? c : art === 't' ? t : s, text: text }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'c'){ if (nah(e.x, A.t / A.sm)) return 'Umgekehrt: Geschwindigkeit ist Weg durch Zeit.'; if (nah(e.x, A.sm * A.t)) return 'Weg und Zeit werden nicht multipliziert: \\(c = \\dfrac{s}{t}\\).'; if (A.cm && nah(e.x, A.s / A.t)) return 'Den Weg zuerst in Meter umrechnen: \\(100\\;\\text{cm} = 1\\;\\text{m}\\).'; }
          if (A.art === 't'){ if (nah(e.x, A.c / A.sm)) return 'Umgekehrt: Zeit ist Weg durch Geschwindigkeit.'; if (nah(e.x, A.sm * A.c)) return 'Nicht multiplizieren: \\(t = \\dfrac{s}{c}\\).'; if (A.cm && nah(e.x, A.s / A.c)) return 'Den Weg zuerst in Meter umrechnen: \\(100\\;\\text{cm} = 1\\;\\text{m}\\).'; }
          if (A.art === 's'){ if (nah(e.x, A.c / A.t) || nah(e.x, A.t / A.c)) return 'Weg ist Geschwindigkeit mal Zeit: \\(s = c \\cdot t\\).'; }
          return 'Die Störung läuft gleichförmig: \\(c = \\dfrac{s}{t}\\), umgestellt nach der gesuchten Grösse.'; },
        fehler: function(A){
          if (A.art === 's') return [[{ x: String(A.c / A.t) }, 'Weg ist'], [{ x: String(A.t / A.c) }, 'Weg ist']];
          var l = A.art === 'c' ? [[{ x: String(A.t / A.sm) }, 'Umgekehrt'], [{ x: String(A.sm * A.t) }, 'multipliziert']] : [[{ x: String(A.c / A.sm) }, 'Umgekehrt'], [{ x: String(A.sm * A.c) }, 'multiplizieren']];
          if (A.cm) l.push([{ x: String(A.art === 'c' ? A.s / A.t : A.s / A.c) }, 'Meter']); return l; },
        loesung: function(A){
          var sE = A.cm ? ein(A.s, 'cm') + ' = ' + ein(A.sm, 'm') : ein(+A.sm.toPrecision(3), 'm');
          if (A.art === 'c') return (A.cm ? 's = ' + sE + ',\\quad ' : '') + 'c = \\dfrac{s}{t} = \\dfrac{' + ein(A.sm, 'm') + '}{' + ein(+A.t.toPrecision(3), 's') + '} ' + erg(A.x, 'm/s');
          if (A.art === 't') return (A.cm ? 's = ' + sE + ',\\quad ' : '') + 't = \\dfrac{s}{c} = \\dfrac{' + ein(A.sm, 'm') + '}{' + ein(A.c, 'm/s') + '} ' + erg(A.x, 's');
          return 's = c \\cdot t = ' + ein(A.c, 'm/s') + ' \\cdot ' + ein(A.t, 's') + ' ' + erg(A.x, 'm'); } },
      'quer-laengs': { felder: ['w'], muster: 'Das ist eine {w:Querwelle|Längswelle|Welle, weder rein quer noch rein längs}.', klartext: true,
        neu: function(){
          var b = zufall([['Du bewegst das Ende eines Gartenschlauchs, der am Boden liegt, schnell nach links und rechts. Die Störung läuft dem Schlauch entlang.', 'Querwelle', 'Der Schlauch bewegt sich seitlich, quer zur Richtung, in der die Störung läuft.'],
                          ['Ein Lautsprecher bringt die Luft vor seiner Membran ins Schwingen; der Ton läuft zu deinem Ohr.', 'Längswelle', 'Die Luftteilchen schwingen hin und her in der Richtung, in der der Schall läuft: Verdichtungen und Verdünnungen.'],
                          ['Ein Delfin pfeift; der Ton läuft durch das Wasser.', 'Längswelle', 'Schall ist auch im Wasser eine Längswelle aus Druckschwankungen: Die Teilchen schwingen in Ausbreitungsrichtung.'],
                          ['Eine Gitarrensaite wird gezupft; die Störung läuft der Saite entlang.', 'Querwelle', 'Die Saite schwingt seitlich, quer zur Saite, die Störung läuft der Saite entlang.'],
                          ['Eine Lokomotive stösst beim Rangieren an eine Reihe Güterwagen: Ein Wagen nach dem anderen rückt kurz nach und wieder zurück, der Stoss läuft durch die Reihe.', 'Längswelle', 'Die Wagen bewegen sich vor und zurück — in derselben Richtung, in der der Stoss durch die Reihe läuft.'],
                          ['Ein Boot fährt vorbei; seine Wellen laufen über den See zum Ufer.', 'Welle, weder rein quer noch rein längs', 'An der Wasseroberfläche laufen die Teilchen auf Kreisbahnen: teils quer, teils längs.']]);
          return { w: b[1], text: b[0] + ' Welche Art Welle ist das?', erkl: b[2] }; },
        pruefen: function(A, e){
          if (e.w === A.w) return null;
          if (A.w.indexOf('weder') === 0) return 'Bewegt sich ein Wasserteilchen an der Oberfläche nur auf und ab? Welche Bahn hat es?';
          if (e.w.indexOf('weder') === 0) return 'Kreisbahnen gibt es bei Wasserwellen. Hier schwingt jedes Teilchen in nur einer Richtung — in welcher, verglichen mit der Ausbreitung?';
          return 'Vergleiche zwei Richtungen: Wohin bewegt sich ein einzelnes Teilchen, und wohin läuft die Welle? Gleich oder quer dazu?'; },
        fehler: function(A){ return ['Querwelle', 'Längswelle', 'Welle, weder rein quer noch rein längs'].filter(function(w){ return w !== A.w; }).map(function(w){ return [{ w: w }, null]; }); },
        loesung: function(A){ return A.w + ': ' + A.erkl; } },

      /* ----- Kapitel 2: Momentbild und Zeitdiagramm ----- */
      'ablesen': { felder: ['g', 'x'], muster: '{g:Wellenlänge λ|Periode T} = {x} (in m bzw. s)',
        neu: function(){
          var art = zufall(['mb', 'zd']), p = zufall(art === 'mb' ? [[0.2, [4, 8], 5], [0.5, [3, 5], 4], [0.1, [6, 8], 5]] : [[0.1, [6, 8], 5], [0.2, [3, 5, 7], 5], [0.5, [3, 4], 4]]);   // ohne λ = 1.2 m und T = 0.4 s (Aufgabe 2a)
          var gs = p[0], m = zufall(p[1]), k0, wert = +(gs * m).toPrecision(6), x0, z;
          do { k0 = 1 + Math.floor(Math.random() * (m - 1)); x0 = +(gs * k0).toPrecision(6); z = [wert, wert / 2, 2 * wert, x0, x0 + wert]; } while (!verschieden(z));
          var A = { art: art, gs: gs, m: m, wert: wert, x0: x0, zellen: 24, lab: p[2], g: art === 'mb' ? 'Wellenlänge λ' : 'Periode T' };
          A.text = (art === 'mb' ? 'Das Momentbild zeigt ein Seil zu einem festen Zeitpunkt.' : 'Das Zeitdiagramm zeigt, wie sich ein Punkt eines Seils im Lauf der Zeit bewegt.') + ' Welche Grösse kannst du hier ablesen, und wie gross ist sie?<br>' + wellenbild(A);
          return A; },
        eingabe: function(A){ return { g: A.g, x: String(A.wert) }; },
        pruefen: function(A, e){
          var gut = Math.abs(e.x - A.wert) <= 0.3 * A.gs, mb = A.art === 'mb';
          if (gut && e.g === A.g) return null;
          if (e.g !== A.g) return 'Schau zuerst auf die waagrechte Achse: ' + (mb ? 'Dort steht der Ort \\(s\\) in Metern — ein Abstand zweier Berge ist eine Länge.' : 'Dort steht die Zeit \\(t\\) in Sekunden — ein Abstand zweier Maxima ist eine Dauer.');
          if (Math.abs(e.x - A.wert / 2) <= 0.3 * A.gs) return 'Von einem Berg zum nächsten Tal ist es nur eine halbe ' + (mb ? 'Wellenlänge' : 'Periode') + '. Miss von Berg zu Berg.';
          if (Math.abs(e.x - 2 * A.wert) <= 0.3 * A.gs) return 'Das sind zwei ' + (mb ? 'Wellenlängen' : 'Perioden') + ': Zwischen deinen Bergen liegt noch einer.';
          if (Math.abs(e.x - A.x0) <= 0.3 * A.gs || Math.abs(e.x - A.x0 - A.wert) <= 0.3 * A.gs) return 'Das ist die Stelle eines Bergs auf der Achse, nicht der Abstand zweier benachbarter Berge.';
          return 'Miss auf der waagrechten Achse den Abstand zweier benachbarter Berge. Ein Kästchen ist \\(' + tz(A.gs) + (mb ? '\\;\\text{m}' : '\\;\\text{s}') + '\\).'; },
        fehler: function(A){ var g2 = A.art === 'mb' ? 'Periode T' : 'Wellenlänge λ';
          return [[{ g: g2, x: String(A.wert) }, 'Achse'], [{ g: A.g, x: String(A.wert / 2) }, 'halbe'], [{ g: A.g, x: String(2 * A.wert) }, 'zwei'], [{ g: A.g, x: String(A.x0 + A.wert) }, 'Stelle']]; },
        loesung: function(A){ return (A.art === 'mb' ? '\\text{Momentbild, Achse } s\\text{: } \\lambda' : '\\text{Zeitdiagramm, Achse } t\\text{: } T') + ' = ' + ein(A.x0 + A.wert, A.art === 'mb' ? 'm' : 's') + ' - ' + ein(A.x0, A.art === 'mb' ? 'm' : 's') + ' = ' + ein(A.wert, A.art === 'mb' ? 'm' : 's'); } },
      'phasengeschw': { felder: ['x'], muster: function(A){ return { c: '<i>c</i> = {x} m/s', T: '<i>T</i> = {x} s', lam: '<i>λ</i> = {x} m' }[A.art]; },
        neu: function(){
          var k, art, lg, lm, T, c, cm, x, l;
          do {
            k = zufall([['einer Seilwelle', [0.8, 1.5, 2.4, 3.2], [0.4, 0.5, 0.8], false], ['einer Welle im Wellenbad', [3.0, 4.0, 6.0], [2.0, 3.0, 4.0], false],
                        ['einer Welle auf einem Gummiseil', [40, 60, 90], [0.3, 0.5, 0.6], true]]);
            art = zufall(['c', 'T', 'lam']); lg = zufall(k[1]); T = zufall(k[2]);
            if (k[0].indexOf('Wellenbad') >= 0){ var pp = zufall([[4.4, 2.0], [3.6, 1.8], [3.3, 1.5]]); lg = pp[0]; T = pp[1]; }   // Wellenbad: c = 2.0 bis 2.2 m/s, Tiefe 0.5 bis 0.9 m (Dispersion ω² = g·k·tanh(k·h); λ < g·T²/2π)
            lm = k[3] ? lg / 100 : lg; c = lm / T;
            if (art !== 'c') c = +c.toPrecision(3);                  // gegeben: auf drei Stellen
            cm = k[3] && art !== 'lam';
            x = art === 'c' ? lm / T : art === 'T' ? lm / c : c * T;
            l = art === 'c' ? [x, lm * T, T / lm] : art === 'T' ? [x, lm * c, c / lm] : [x, c / T, T / c];
            if (cm) l.push(art === 'c' ? lg / T : lg / c);
          } while (!verschieden(l) || lm / T < 0.5 || lm / T > 9 || (k[0].indexOf('Wellenbad') >= 0 && lm / T < 1.5) || fest_(art === 'lam' ? c : lg, art === 'T' ? c : T));
          var lT = cm ? ein(lg, 'cm') : ein(lm, 'm'), cT = ein(c, 'm/s');
          var text = art === 'c' ? 'Bei ' + k[0] + ' haben benachbarte Berge \\(' + lT + '\\) Abstand; ein Punkt braucht für eine Schwingung \\(' + ein(T, 's') + '\\). Wie gross ist die Phasengeschwindigkeit?'
                   : art === 'T' ? 'Bei ' + k[0] + ' haben benachbarte Berge \\(' + lT + '\\) Abstand; die Welle läuft mit \\(' + cT + '\\). Wie lange dauert eine Schwingung eines Punkts?'
                   : 'Bei ' + k[0] + ' läuft die Welle mit \\(' + cT + '\\); ein Punkt braucht für eine Schwingung \\(' + ein(T, 's') + '\\). Wie gross ist die Wellenlänge?';
          return { art: art, lam: lg, lm: lm, T: T, c: c, cm: cm, x: x, text: text }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'c'){ if (nah(e.x, A.lm * A.T)) return 'Nicht multiplizieren: In einer Periode rückt die Welle um eine Wellenlänge weiter, \\(c = \\dfrac{\\lambda}{T}\\).'; if (nah(e.x, A.T / A.lm)) return 'Umgekehrt: \\(c = \\dfrac{\\lambda}{T}\\), Weg durch Zeit.'; if (A.cm && nah(e.x, A.lam / A.T)) return 'Die Wellenlänge zuerst in Meter umrechnen.'; }
          if (A.art === 'T'){ if (nah(e.x, A.lm * A.c)) return 'Aus \\(c = \\dfrac{\\lambda}{T}\\) folgt \\(T = \\dfrac{\\lambda}{c}\\) — nicht multiplizieren.'; if (nah(e.x, A.c / A.lm)) return 'Das ist die Frequenz \\(f = \\dfrac{c}{\\lambda}\\). Gefragt ist die Periode.'; if (A.cm && nah(e.x, A.lam / A.c)) return 'Die Wellenlänge zuerst in Meter umrechnen.'; }
          if (A.art === 'lam'){ if (nah(e.x, A.c / A.T)) return 'Aus \\(c = \\dfrac{\\lambda}{T}\\) folgt \\(\\lambda = c \\cdot T\\).'; if (nah(e.x, A.T / A.c)) return 'Aus \\(c = \\dfrac{\\lambda}{T}\\) folgt \\(\\lambda = c \\cdot T\\).'; }
          return '\\(c = \\dfrac{\\lambda}{T}\\), umgestellt nach der gesuchten Grösse; Längen in Meter.'; },
        fehler: function(A){
          if (A.art === 'c'){ var l = [[{ x: String(A.lm * A.T) }, 'multiplizieren'], [{ x: String(A.T / A.lm) }, 'Umgekehrt']]; if (A.cm) l.push([{ x: String(A.lam / A.T) }, 'Meter']); return l; }
          if (A.art === 'T'){ var m = [[{ x: String(A.lm * A.c) }, 'nicht multiplizieren'], [{ x: String(A.c / A.lm) }, 'Frequenz']]; if (A.cm) m.push([{ x: String(A.lam / A.c) }, 'Meter']); return m; }
          return [[{ x: String(A.c / A.T) }, 'folgt'], [{ x: String(A.T / A.c) }, 'folgt']]; },
        loesung: function(A){
          var lE = A.cm ? ein(A.lam, 'cm') + ' = ' + ein(A.lm, 'm') : ein(+A.lm.toPrecision(3), 'm');
          if (A.art === 'c') return (A.cm ? '\\lambda = ' + lE + ',\\quad ' : '') + 'c = \\dfrac{\\lambda}{T} = \\dfrac{' + ein(A.lm, 'm') + '}{' + ein(A.T, 's') + '} ' + erg(A.x, 'm/s');
          if (A.art === 'T') return (A.cm ? '\\lambda = ' + lE + ',\\quad ' : '') + 'T = \\dfrac{\\lambda}{c} = \\dfrac{' + ein(A.lm, 'm') + '}{' + ein(A.c, 'm/s') + '} ' + erg(A.x, 's');
          return '\\lambda = c \\cdot T = ' + ein(A.c, 'm/s') + ' \\cdot ' + ein(A.T, 's') + ' ' + erg(A.x, 'm'); } },

      /* ----- Kapitel 3: Sender und Medium ----- */
      'wellengleichung': { felder: ['x'], muster: function(A){ return { lam: '<i>λ</i> = {x} m', f: '<i>f</i> = {x} Hz' }[A.art]; },
        neu: function(){
          var med, f, khz, art, lam, l;
          do {
            med = zufall(['Luft', 'Helium', 'Wasser', 'Eisen']); f = zufall([125, 200, 300, 600, 1200, 3000, 6000]); khz = f >= 1000 && Math.random() < 0.7;
            art = zufall(['lam', 'f']); lam = SCHALL[med] / f;
            if (art === 'f') lam = +lam.toPrecision(3);
            l = art === 'lam' ? [lam, f / SCHALL[med]] : [SCHALL[med] / lam, lam / SCHALL[med]];
            if (med !== 'Luft') l.push(art === 'lam' ? 340 / f : 340 / lam);     // «mit Luft gerechnet» nur, wenn der Stoff nicht Luft ist
            if (khz) l.push(SCHALL[med] / (f / 1000));
          } while (!verschieden(l));
          var fT = khz ? ein(f / 1000, 'kHz') : ein(f, 'Hz'), cT = '\\(c = ' + ein(SCHALL[med], 'm/s') + '\\)';
          var wo = { 'Luft': 'in Luft', 'Helium': 'in Helium', 'Wasser': 'im Wasser', 'Eisen': 'in Eisen' }[med];
          return { art: art, med: med, c: SCHALL[med], f: art === 'lam' ? f : SCHALL[med] / lam, fn: f, khz: khz, lam: lam, x: art === 'lam' ? lam : SCHALL[med] / lam,
            text: art === 'lam' ? 'Ein Ton von \\(' + fT + '\\) läuft ' + wo + ' (' + cT + '). Wie lang ist seine Welle?'
                                : 'Ein Ton hat ' + wo + ' (' + cT + ') die Wellenlänge \\(' + ein(lam, 'm') + '\\). Welche Frequenz hat er?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'lam'){
            if (nah(e.x, A.f / A.c)) return 'Umgekehrt: \\(\\lambda = \\dfrac{c}{f}\\) — Geschwindigkeit durch Frequenz.';
            if (A.khz && nah(e.x, A.c / (A.f / 1000))) return 'Die Frequenz zuerst in Hertz umrechnen: \\(1\\;\\text{kHz} = 1000\\;\\text{Hz}\\).';
            if (A.med !== 'Luft' && nah(e.x, 340 / A.f)) return 'Das ist die Wellenlänge in Luft. Der Ton läuft hier in einem anderen Stoff — mit dessen Schallgeschwindigkeit.';
          } else {
            if (nah(e.x, A.lam / A.c)) return 'Umgekehrt: \\(f = \\dfrac{c}{\\lambda}\\) — Geschwindigkeit durch Wellenlänge.';
            if (A.med !== 'Luft' && nah(e.x, 340 / A.lam)) return 'Mit der Schallgeschwindigkeit von Luft gerechnet. Nimm die des Stoffs, in dem der Ton läuft.';
          }
          return 'Wellengleichung \\(c = \\lambda \\cdot f\\), nach der gesuchten Grösse umgestellt.'; },
        fehler: function(A){
          var l = A.art === 'lam' ? [[{ x: String(A.f / A.c) }, 'Umgekehrt']] : [[{ x: String(A.lam / A.c) }, 'Umgekehrt']];
          if (A.art === 'lam' && A.khz) l.push([{ x: String(A.c / (A.f / 1000)) }, 'Hertz']);
          if (A.med !== 'Luft') l.push([{ x: String(A.art === 'lam' ? 340 / A.f : 340 / A.lam) }, 'Luft']);
          return l; },
        loesung: function(A){
          if (A.art === 'lam') return (A.khz ? 'f = ' + ein(A.f / 1000, 'kHz') + ' = ' + ein(A.f, 'Hz') + ',\\quad ' : '') + '\\lambda = \\dfrac{c}{f} = \\dfrac{' + ein(A.c, 'm/s') + '}{' + ein(A.f, 'Hz') + '} ' + erg(A.x, 'm');
          return 'f = \\dfrac{c}{\\lambda} = \\dfrac{' + ein(A.c, 'm/s') + '}{' + ein(A.lam, 'm') + '} ' + erg(A.x, 'Hz'); } },
      'medium': { felder: ['x'], muster: '<i>λ</i><sub>2</sub> = {x} m',
        neu: function(){
          var p, l1, l2, l;
          do {
            p = zufall([['Luft', 'Wasser'], ['Wasser', 'Luft'], ['Luft', 'Eisen'], ['Luft', 'Helium'], ['Wasser', 'Eisen'], ['Helium', 'Luft']]);
            l1 = zufall([0.20, 0.25, 0.50, 1.2, 1.6, 2.8]);
            l2 = l1 * SCHALL[p[1]] / SCHALL[p[0]];
            l = [l2, l1, l1 * SCHALL[p[0]] / SCHALL[p[1]]];
          } while (!verschieden(l));
          var wo = { 'Luft': 'aus der Luft', 'Wasser': 'aus dem Wasser', 'Helium': 'aus Helium', 'Eisen': 'aus Eisen' }, hin = { 'Luft': 'in die Luft', 'Wasser': 'ins Wasser', 'Helium': 'in Helium', 'Eisen': 'in Eisen' };
          return { a: p[0], b: p[1], l1: l1, x: l2,
            text: 'Ein Ton geht ' + wo[p[0]] + ' (\\(c_1 = ' + ein(SCHALL[p[0]], 'm/s') + '\\)) ' + hin[p[1]] + ' (\\(c_2 = ' + ein(SCHALL[p[1]], 'm/s') + '\\)). Vorher ist seine Welle \\(' + ein(l1, 'm') + '\\) lang. Wie lang ist sie danach?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.l1)) return 'Gleich bleibt die Frequenz, nicht die Wellenlänge: Mit der Geschwindigkeit ändert sich auch \\(\\lambda = \\dfrac{c}{f}\\).';
          if (nah(e.x, A.l1 * SCHALL[A.a] / SCHALL[A.b])) return 'Verhältnis umgekehrt: Im schnelleren Stoff wird die Welle länger, im langsameren kürzer.';
          return 'Die Frequenz bleibt: \\(f = \\dfrac{c_1}{\\lambda_1}\\), dann \\(\\lambda_2 = \\dfrac{c_2}{f}\\).'; },
        fehler: function(A){ return [[{ x: String(A.l1) }, 'Frequenz'], [{ x: String(A.l1 * SCHALL[A.a] / SCHALL[A.b]) }, 'umgekehrt']]; },
        loesung: function(A){ var f = SCHALL[A.a] / A.l1;
          return 'f = \\dfrac{c_1}{\\lambda_1} = \\dfrac{' + ein(SCHALL[A.a], 'm/s') + '}{' + ein(A.l1, 'm') + '} ' + erg(f, 'Hz') + '\\text{ bleibt},\\quad \\lambda_2 = \\lambda_1 \\cdot \\dfrac{c_2}{c_1} = ' + ein(A.l1, 'm') + ' \\cdot \\dfrac{' + ein(SCHALL[A.b], 'm/s') + '}{' + ein(SCHALL[A.a], 'm/s') + '} ' + erg(A.x, 'm'); } },
      'hoerbar': { felder: ['b', 'x'], muster: function(A){ return 'Das ist {b:Infraschall|hörbarer Schall|Ultraschall}. <i>λ</i> in Luft = {x} ' + A.u; },
        neu: function(){
          var b = zufall([['Ein Elefant ruft mit', 15, 'Hz', 'Infraschall', 'm'], ['Ein Windrad erzeugt Druckschwankungen mit', 4, 'Hz', 'Infraschall', 'm'],
                          ['Eine Hundepfeife pfeift mit', 30, 'kHz', 'Ultraschall', 'cm'], ['Eine Einparkhilfe sendet mit', 48, 'kHz', 'Ultraschall', 'mm'],
                          ['Ein Marderschreck im Auto sendet mit', 35, 'kHz', 'Ultraschall', 'cm'], ['Ein Pfeifkessel pfeift mit', 3.2, 'kHz', 'hörbarer Schall', 'cm'],
                          ['Eine Bassgitarre spielt ihren tiefsten Ton mit', 41, 'Hz', 'hörbarer Schall', 'm'], ['Ein Kanarienvogel singt mit', 4.5, 'kHz', 'hörbarer Schall', 'cm']]);
          var f = b[2] === 'kHz' ? b[1] * 1000 : b[1], lam = 340 / f, fak = { m: 1, cm: 100, mm: 1000 }[b[4]];
          return { b: b[3], f: f, k: b[2] === 'kHz', u: b[4], fak: fak, x: lam * fak, lam: lam,
            text: b[0] + ' \\(' + ein(b[1], b[2]) + '\\). Ist das Infraschall, hörbarer Schall oder Ultraschall? Wie lang ist die Welle in Luft (\\(c = 340\\;\\text{m/s}\\))?' }; },
        eingabe: function(A){ return { b: A.b, x: String(A.x) }; },
        pruefen: function(A, e){
          var ok = nah(e.x, A.x);
          if (ok && e.b === A.b) return null;
          if (e.b !== A.b) return 'Der Mensch hört etwa von \\(20\\;\\text{Hz}\\) bis \\(20\\;\\text{kHz}\\). Darunter liegt Infraschall, darüber Ultraschall. Wo liegt diese Frequenz?';
          if (A.k && nah(e.x, 340 / (A.f / 1000) * A.fak)) return 'Die Frequenz zuerst in Hertz umrechnen: \\(1\\;\\text{kHz} = 1000\\;\\text{Hz}\\).';
          if (nah(e.x, A.lam)) return 'Das ist die Wellenlänge in Metern. Gefragt ist sie in ' + A.u + '.';
          if (nah(e.x, A.f / 340 * A.fak)) return 'Umgekehrt: \\(\\lambda = \\dfrac{c}{f}\\).';
          return '\\(\\lambda = \\dfrac{c}{f}\\) mit \\(f\\) in Hz, dann in ' + A.u + ' umrechnen.'; },
        fehler: function(A){ var andere = A.b === 'Ultraschall' ? 'hörbarer Schall' : A.b === 'Infraschall' ? 'hörbarer Schall' : 'Ultraschall';
          var l = [[{ b: andere, x: String(A.x) }, 'hört'], [{ b: A.b, x: String(A.f / 340 * A.fak) }, 'Umgekehrt']];
          if (A.k) l.push([{ b: A.b, x: String(340 / (A.f / 1000) * A.fak) }, 'Hertz']);
          if (A.u !== 'm') l.push([{ b: A.b, x: String(A.lam) }, 'Metern']);
          return l; },
        loesung: function(A){ return '\\text{' + A.b + '};\\quad \\lambda = \\dfrac{c}{f} = \\dfrac{340\\;\\text{m/s}}{' + ein(A.f, 'Hz') + '} ' + erg(A.lam, 'm') + (A.u !== 'm' ? ' ' + erg(A.x, A.u) : ''); } },

      /* ----- Kapitel 4: Elektromagnetische Wellen ----- */
      'em-rechnen': { felder: ['x'], muster: function(A){ return A.art === 'lam' ? '<i>λ</i> = {x} ' + A.u : '<i>f</i> = {x} Hz'; },
        neu: function(){
          var b = zufall([['Ein UKW-Sender sendet auf', [88.4, 91.2, 97.6, 103.4, 106.8], 'MHz', 1e6, 'm'], ['Ein Mittelwellensender sendet auf', [558, 765, 1404], 'kHz', 1e3, 'm'],
                          ['Ein Handy funkt mit', [0.80, 1.8, 2.6], 'GHz', 1e9, 'cm'], ['Ein Abstandsradar im Auto arbeitet mit', [77], 'GHz', 1e9, 'mm'],
                          ['Eine blaue Leuchtdiode leuchtet mit', [465, 475], 'nm', 1e-9, 'f'],
                          ['Ein roter Laserpointer leuchtet mit', [635, 670], 'nm', 1e-9, 'f'], ['Eine Fernbedienung sendet Infrarot mit', [940], 'nm', 1e-9, 'f'],
                          ['Eine Röntgenröhre beim Zahnarzt sendet Strahlung mit', [0.025, 0.040], 'nm', 1e-9, 'f']]);
          var v = zufall(b[1]), si = v * b[3], art = b[4] === 'f' ? 'f' : 'lam', fak = { m: 1, cm: 100, mm: 1000 }[b[4]] || 1;
          var x = art === 'lam' ? CL / si * fak : CL / si;
          return { art: art, v: v, e: b[2], si: si, u: art === 'lam' ? b[4] : 'Hz', fak: fak, x: x, faktor: b[3],
            text: b[0] + ' \\(' + ein(v, b[2]) + '\\). ' + (art === 'lam' ? 'Wie lang ist die Welle, in ' + b[4] + '?' : 'Welche Frequenz hat die Strahlung?') + ' (\\(c = ' + CTEX + '\\))' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          var r = e.x / A.x;
          if (A.art === 'lam' && nah(e.x, A.si / CL * A.fak)) return 'Umgekehrt: \\(\\lambda = \\dfrac{c}{f}\\).';
          if (A.art === 'f' && nah(e.x, A.si / CL)) return 'Umgekehrt: \\(f = \\dfrac{c}{\\lambda}\\).';
          if (A.art === 'lam' && nah(e.x, 340 / A.si * A.fak)) return 'Mit der Schallgeschwindigkeit gerechnet. Elektromagnetische Wellen laufen mit \\(' + CTEX + '\\).';
          if ([1e3, 1e6, 1e9, 1e-3, 1e-6, 1e-9, 1e2, 1e-2].some(function(q){ return nah(r, q, 0.01); })) return 'Die Grössenordnung stimmt nicht: Prüfe die Vorsilbe (k = \\(10^{3}\\), M = \\(10^{6}\\), G = \\(10^{9}\\), n = \\(10^{-9}\\)) und die Einheit der Antwort.';
          return A.art === 'lam' ? '\\(\\lambda = \\dfrac{c}{f}\\) mit \\(f\\) in Hz, dann in ' + A.u + ' umrechnen.' : '\\(f = \\dfrac{c}{\\lambda}\\) mit \\(\\lambda\\) in Meter.'; },
        fehler: function(A){
          var l = [[{ x: String(A.art === 'lam' ? A.si / CL * A.fak : A.si / CL) }, 'Umgekehrt'], [{ x: String(A.x * 1e3) }, 'Vorsilbe'], [{ x: String(A.x / 1e6) }, 'Vorsilbe']];
          if (A.art === 'lam') l.push([{ x: String(340 / A.si * A.fak) }, 'Schallgeschwindigkeit']);
          return l; },
        loesung: function(A){
          if (A.art === 'lam') return 'f = ' + ein(A.v, A.e) + ' = ' + ein(A.si, 'Hz') + ',\\quad \\lambda = \\dfrac{c}{f} = \\dfrac{' + CTEX + '}{' + ein(A.si, 'Hz') + '} ' + erg(A.x / A.fak, 'm') + (A.u !== 'm' ? ' ' + erg(A.x, A.u) : '');
          return '\\lambda = ' + ein(A.v, A.e) + ' = ' + ein(A.si, 'm') + ',\\quad f = \\dfrac{c}{\\lambda} = \\dfrac{' + CTEX + '}{' + ein(A.si, 'm') + '} ' + erg(A.x, 'Hz'); } },
      'bereich': { felder: ['b'], muster: 'Bereich: {b:Radiowellen|Mikrowellen|Infrarot|sichtbares Licht|Ultraviolett|Röntgenstrahlung|Gammastrahlung}', klartext: true,
        neu: function(){
          var b = zufall([['Die Antenne eines Langwellensenders strahlt Wellen von \\(1.5\\;\\text{km}\\) Länge ab.', 1500], ['Ein Wetterradar arbeitet mit Wellen von \\(5.3\\;\\text{cm}\\).', 0.053],
                          ['Ein Mikrowellenofen arbeitet mit Wellen von \\(12\\;\\text{cm}\\).', 0.12], ['Ein Kurzwellensender strahlt Wellen von \\(25\\;\\text{m}\\) ab.', 25],
                          ['Ein Präsenzmelder misst die Wärmestrahlung von Menschen um \\(9\\;\\mu\\text{m}\\).', 9e-6], ['Eine UV-Lampe zum Härten von Nagellack leuchtet mit \\(300\\;\\text{nm}\\).', 300e-9],
                          ['Ein Laser leuchtet mit \\(520\\;\\text{nm}\\).', 520e-9], ['Ein Computertomograf arbeitet mit Strahlung von \\(0.05\\;\\text{nm}\\).', 0.05e-9],
                          ['Ein radioaktives Präparat sendet Strahlung von \\(2.0\\;\\text{pm}\\).', 2.0e-12], ['Eine Welle hat die Frequenz \\(6.0 \\cdot 10^{14}\\;\\text{Hz}\\).', CL / 6.0e14],
                          ['Eine Welle hat die Frequenz \\(1.0 \\cdot 10^{16}\\;\\text{Hz}\\).', CL / 1.0e16]]);
          var band = bandVon(b[1]);
          return { b: band[2], lam: b[1], text: b[0] + ' In welchen Bereich des Spektrums gehört sie?' }; },
        pruefen: function(A, e){
          if (e.b === A.b) return null;
          var namen = BAENDER.map(function(x){ return x[2]; }), i = namen.indexOf(A.b), j = namen.indexOf(e.b);
          return 'Rechne die Wellenlänge in Meter um und ordne nach der Reihenfolge (von kurz nach lang): Gamma, Röntgen, Ultraviolett, sichtbar (\\(380\\) bis \\(780\\;\\text{nm}\\)), Infrarot, Mikrowellen, Radio. ' + (j > i ? 'Die Welle ist kürzer, als du gewählt hast.' : 'Die Welle ist länger, als du gewählt hast.'); },
        fehler: function(A){ var namen = BAENDER.map(function(x){ return x[2]; }), i = namen.indexOf(A.b); return [i - 1, i + 1].filter(function(k){ return k >= 0 && k < namen.length; }).map(function(k){ return [{ b: namen[k] }, k > i ? 'kürzer' : 'länger']; }); },
        loesung: function(A){ return A.b + ': λ = ' + laenge(A.lam, 2) + '.'; } },
      'wellentyp': { felder: ['t', 'm'], muster: 'Das ist {t:Schall|eine andere mechanische Welle|eine elektromagnetische Welle}; sie {m:braucht ein Medium|braucht kein Medium}.', klartext: true,
        neu: function(){
          var b = zufall([['Die Pfeife eines Schiedsrichters', 'Schall', 'braucht ein Medium'], ['Die Funkverbindung zu einer Raumsonde', 'eine elektromagnetische Welle', 'braucht kein Medium'],
                          ['Die Wellen auf einem Teich, in den ein Stein fällt', 'eine andere mechanische Welle', 'braucht ein Medium'], ['Die Strahlung, die eine Wärmebildkamera aufnimmt', 'eine elektromagnetische Welle', 'braucht kein Medium'],
                          ['Der Ultraschall eines Ultraschallgeräts beim Arzt', 'Schall', 'braucht ein Medium'], ['Wellen auf dem Tuch eines Trampolins', 'eine andere mechanische Welle', 'braucht ein Medium'],
                          ['Das Licht eines fernen Sterns', 'eine elektromagnetische Welle', 'braucht kein Medium'], ['Die Strahlung einer Röntgenröhre beim Arzt', 'eine elektromagnetische Welle', 'braucht kein Medium']]);
          return { t: b[1], m: b[2], name: b[0], text: b[0] + ': Welche Art Welle ist das, und braucht sie ein Medium?' }; },
        pruefen: function(A, e){
          if (e.t === A.t && e.m === A.m) return null;
          if (e.t !== A.t){
            if (A.t === 'Schall') return 'Eine Pfeife, ein Ultraschallgerät: Was senden sie aus — Druckschwankungen oder Licht? Auch Ultraschall ist Schall.';
            if (A.t === 'eine elektromagnetische Welle') return 'Gibt es hier ein Medium, das schwingt? Funk, Licht, Wärmestrahlung und Röntgen gehören zur selben Familie.';
            return 'Hier schwingt ein Stoff, aber was man misst, ist kein Ton, sondern die Bewegung des Stoffs selbst.';
          }
          return A.m === 'braucht ein Medium' ? 'Mechanische Wellen und Schall brauchen gekoppelte Teilchen, die die Schwingung weitergeben.' : 'Elektromagnetische Wellen sind schwingende Felder: Sie laufen auch durch das Vakuum.'; },
        fehler: function(A){ var andere = A.t === 'Schall' ? 'eine elektromagnetische Welle' : 'Schall', gegen = A.m === 'braucht ein Medium' ? 'braucht kein Medium' : 'braucht ein Medium';
          return [[{ t: andere, m: A.m }, null], [{ t: A.t, m: gegen }, null]]; },
        loesung: function(A){ return A.name + ': ' + A.t + '; sie ' + A.m + '.'; } },

      /* ----- Kapitel 5: Emission, Laser, Absorption ----- */
      'stufen': { felder: ['x'], muster: '<i>λ</i><sub>B</sub> = {x} nm',
        neu: function(){
          var l1, k, l;
          do { l1 = zufall([450, 500, 560, 620, 680, 720]); k = zufall([0.5, 0.8, 1.2, 1.6, 2, 2.5]); l = [l1 / k, l1 * k, l1]; } while (!verschieden(l) || l1 / k < 180 || l1 / k > 1600 || fest_(l1, k));
          return { l1: l1, k: k, x: l1 / k,
            text: 'Ein Atom sendet beim Sprung A Licht von \\(' + ein(l1, 'nm') + '\\) aus. Beim Sprung B ist die Energiestufe ' + (k < 1 ? 'nur ' : '') + '\\(' + tz(k) + '\\)-mal so gross. Welche Wellenlänge hat das Photon von Sprung B?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.l1 * A.k)) return 'Umgekehrt: Eine ' + (A.k > 1 ? 'grössere' : 'kleinere') + ' Stufe gibt eine ' + (A.k > 1 ? 'höhere' : 'tiefere') + ' Frequenz — und darum eine ' + (A.k > 1 ? 'kürzere' : 'längere') + ' Wellenlänge.';
          if (nah(e.x, A.l1)) return 'Eine andere Stufe gibt ein Photon mit anderer Energie, also anderer Frequenz und Wellenlänge.';
          return 'Die Energie des Photons ist die Stufe, \\(E = h \\cdot f\\): Die Frequenz wächst im selben Verhältnis wie die Stufe, die Wellenlänge \\(\\lambda = \\dfrac{c}{f}\\) umgekehrt.'; },
        fehler: function(A){ return [[{ x: String(A.l1 * A.k) }, 'Umgekehrt'], [{ x: String(A.l1) }, 'andere Stufe']]; },
        loesung: function(A){ return 'f_\\text{B} = ' + tz(A.k) + ' \\cdot f_\\text{A},\\quad \\lambda_\\text{B} = \\dfrac{\\lambda_\\text{A}}{' + tz(A.k) + '} = \\dfrac{' + ein(A.l1, 'nm') + '}{' + tz(A.k) + '} ' + erg(A.x, 'nm'); } },
      'licht-aussage': { felder: ['r'], muster: 'Die Aussage ist {r:richtig|falsch}.', klartext: true,
        neu: function(){
          var s = zufall([['Ein Atom kann Licht jeder beliebigen Wellenlänge aussenden.', 'falsch', 'Ein Atom hat feste Energiestufen; es sendet nur Photonen aus, deren Energie genau einem Sprung entspricht — darum nur bestimmte Wellenlängen.', 'Welche Energie hat ein Photon, das bei einem Sprung entsteht?'],
                          ['Je grösser die Energiestufe, desto kürzer die Wellenlänge des ausgesandten Photons.', 'richtig', 'Grössere Stufe, mehr Energie, höhere Frequenz (\\(E = h \\cdot f\\)) — und bei gleichem \\(c\\) eine kürzere Wellenlänge.', 'Wie hängen die Energie eines Photons, seine Frequenz und seine Wellenlänge zusammen?'],
                          ['Ein Atom, dessen Elektron auf E₁ sitzt, nimmt nur Photonen auf, deren Energie genau zu einem Sprung nach oben passt.', 'richtig', 'Absorption ist die Umkehrung der Emission: Nur passende Photonen heben das Elektron an; die anderen gehen durch.', 'Was geschah in der Simulation mit dem weissen Licht im Gas?'],
                          ['Laserlicht ist kohärent: Alle Photonen schwingen im gleichen Takt.', 'richtig', 'Bei der stimulierten Emission entsteht ein Photon gleicher Wellenlänge, gleicher Richtung und gleicher Phase.', 'Wie entsteht im Laser das zweite Photon aus dem ersten?'],
                          ['Ein Laser braucht keine Spiegel: Die Photonen laufen von selbst alle in dieselbe Richtung.', 'falsch', 'Die ersten Photonen entstehen spontan, in alle Richtungen. Erst die Spiegel schicken die Photonen, die längs laufen, immer wieder durch die angeregten Atome; nur sie lösen dort viele gleiche Photonen aus. So wird genau diese eine Richtung verstärkt.', 'In welche Richtung fliegt das Photon, das ein anderes Photon auslöst?'],
                          ['Ein Laser braucht keine Energie von aussen, weil sich die Photonen selbst vermehren.', 'falsch', 'Jedes neue Photon nimmt die Energie eines angeregten Atoms. Ohne Pumpen sind bald keine Atome mehr angeregt, und der Laser erlischt.', 'Woher kommt die Energie jedes neuen Photons?'],
                          ['Bei der spontanen Emission fliegt das Photon in eine zufällige Richtung.', 'richtig', 'Ein angeregtes Atom, das von selbst zurückspringt, sendet sein Photon in irgendeine Richtung aus — wie in der Simulation.', 'Was hast du in der Simulation bei mehreren Sprüngen beobachtet?'],
                          ['Infrarot entsteht, wenn ein Elektron über eine besonders grosse Stufe springt.', 'falsch', 'Eine kleine Stufe gibt wenig Energie, eine tiefe Frequenz und eine lange Wellenlänge — etwa Infrarot. Grosse Stufen geben Ultraviolett.', 'Infrarot hat eine lange Wellenlänge. Passt dazu viel oder wenig Energie?']]);
          return { r: s[1], text: '«' + s[0] + '» Stimmt das?', erkl: s[2], hinweis: s[3] }; },
        pruefen: function(A, e){ return e.r === A.r ? null : 'Noch nicht. ' + A.hinweis; },
        fehler: function(A){ return [[{ r: A.r === 'richtig' ? 'falsch' : 'richtig' }, 'Noch nicht']]; },
        loesung: function(A){ return (A.r === 'richtig' ? 'Richtig. ' : 'Falsch. ') + A.erkl; } },

      /* ----- Kapitel 6: Treibhauseffekt ----- */
      'zuordnen': { felder: ['q', 'a'], muster: 'Sie kommt vor allem {q:von der Sonne|vom Boden} und {a:wird stark aufgenommen|kommt weitgehend durch}.', klartext: true,
        neu: function(){
          var b = zufall([['\\(0.45\\;\\mu\\text{m}\\) (blaues Licht)', 'von der Sonne', 'kommt weitgehend durch', 'Sichtbares Licht kommt von der heissen Sonne, und die Atmosphäre lässt es durch.'],
                          ['\\(0.65\\;\\mu\\text{m}\\) (rotes Licht)', 'von der Sonne', 'kommt weitgehend durch', 'Sichtbares Licht kommt von der heissen Sonne, und die Atmosphäre lässt es durch.'],
                          ['\\(6.5\\;\\mu\\text{m}\\)', 'vom Boden', 'wird stark aufgenommen', 'Infrarot um \\(6.5\\;\\mu\\text{m}\\) strahlt der Boden; Wasserdampf nimmt es stark auf.'],
                          ['\\(10.5\\;\\mu\\text{m}\\)', 'vom Boden', 'kommt weitgehend durch', 'Um \\(10\\;\\mu\\text{m}\\) strahlt der Boden viel; zwischen rund \\(8\\) und \\(13\\;\\mu\\text{m}\\) liegt das Fenster (nur Ozon nimmt darin schmal um \\(9.6\\;\\mu\\text{m}\\) auf).'],
                          ['\\(9\\;\\mu\\text{m}\\)', 'vom Boden', 'kommt weitgehend durch', 'Das liegt im Fenster zwischen rund \\(8\\) und \\(13\\;\\mu\\text{m}\\), unterhalb des schmalen Ozonbereichs um \\(9.6\\;\\mu\\text{m}\\).'],
                          ['\\(16\\;\\mu\\text{m}\\)', 'vom Boden', 'wird stark aufgenommen', 'Kohlendioxid nimmt um \\(15\\;\\mu\\text{m}\\) stark auf, auch bei \\(16\\;\\mu\\text{m}\\).'],
                          ['\\(25\\;\\mu\\text{m}\\)', 'vom Boden', 'wird stark aufgenommen', 'Über rund \\(20\\;\\mu\\text{m}\\) nimmt Wasserdampf fast alles auf.']]);
          return { q: b[1], a: b[2], text: 'Strahlung mit der Wellenlänge ' + b[0] + ': Woher kommt sie vor allem, und was macht die Atmosphäre mit ihr?', erkl: b[3] }; },
        pruefen: function(A, e){
          if (e.q === A.q && e.a === A.a) return null;
          if (e.q !== A.q) return 'Die Sonne strahlt je Mikrometer am stärksten um \\(0.5\\;\\mu\\text{m}\\), der Boden um \\(10\\;\\mu\\text{m}\\). Wo liegt diese Wellenlänge näher?';
          return 'Sieh im Festhalten nach, wo die Bereiche von Wasserdampf, Kohlendioxid, Methan und Ozon liegen und wo das Fenster ist.'; },
        fehler: function(A){ var q2 = A.q === 'von der Sonne' ? 'vom Boden' : 'von der Sonne', a2 = A.a.indexOf('aufgenommen') > 0 ? 'kommt weitgehend durch' : 'wird stark aufgenommen';
          return [[{ q: q2, a: A.a }, 'Sonne strahlt'], [{ q: A.q, a: a2 }, 'Bereiche']]; },
        loesung: function(A){ return 'Sie kommt vor allem ' + A.q + ' und ' + A.a + '. ' + A.erkl; } },
      'treibhaus-aussage': { felder: ['r'], muster: 'Die Aussage ist {r:richtig|falsch}.', klartext: true,
        neu: function(){
          var s = zufall([['Die Treibhausgase lassen das kurzwellige Sonnenlicht fast ungehindert durch.', 'richtig', 'Ihre Aufnahmebereiche liegen im Infrarot, nicht dort, wo die Sonne am meisten strahlt.', 'Wo liegen die Aufnahmebereiche der Gase, wo das Maximum der Sonne?'],
                          ['Der Boden strahlt vor allem sichtbares Licht ab.', 'falsch', 'Der Boden ist mit rund 15 °C viel kühler als die Sonne; er strahlt im Infrarot, je Mikrometer am stärksten um 10 µm.', 'Bei welcher Wellenlänge strahlt ein Körper von rund 15 °C am meisten?'],
                          ['Kohlendioxid nimmt vor allem Infrarot auf, kaum sichtbares Licht.', 'richtig', 'Sein Aufnahmebereich liegt um 15 µm, im Infrarot.', 'Wo liegt der Bereich des Kohlendioxids im Spektrum?'],
                          ['Treibhausgase strahlen die aufgenommene Energie nur nach oben ins All ab.', 'falsch', 'Sie strahlen in alle Richtungen ab, auch zurück zum Boden. Dieser Teil wärmt den Boden zusätzlich.', 'In welche Richtungen strahlt ein Gas ab, das Strahlung aufgenommen hat?'],
                          ['Methan ist kein Treibhausgas, weil davon nur wenig in der Luft ist.', 'falsch', 'Methan nimmt im Infrarot um rund 7.7 µm auf und ist darum ein Treibhausgas, auch wenn es wenig davon gibt.', 'Was macht ein Gas zum Treibhausgas — seine Menge oder seine Aufnahmebereiche?'],
                          ['Ohne Treibhausgase wäre die Erde im Mittel deutlich kälter.', 'richtig', 'Ohne sie ginge die ganze Bodenstrahlung ins All: im Mittel rund −18 °C statt rund +15 °C.', 'Was geschähe mit der Wärmestrahlung des Bodens ohne Treibhausgase?'],
                          ['Mehr Kohlendioxid verbreitert den Bereich der Wellenlängen, in dem die Luft Wärmestrahlung aufnimmt.', 'richtig', 'An den Rändern seines Bereichs nimmt das Gas schwächer auf; mit mehr Gas reicht auch das. Der Bereich wird breiter, mehr Bodenstrahlung bleibt in der Atmosphäre.', 'Was zeigte die Simulation bei 280 und bei 430 ppm?'],
                          ['Wasserdampf ist das wichtigste natürliche Treibhausgas.', 'richtig', 'Wasserdampf hat die breitesten Aufnahmebereiche im Infrarot und trägt am meisten zum natürlichen Treibhauseffekt bei.', 'Welches Gas nahm in der Simulation allein schon rund ein Drittel der Bodenstrahlung auf?']]);
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
