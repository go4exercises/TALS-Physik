<script>
/* Leitprogramm Statik — laufende Simulationen mit Aufgabenleiste, Übungen mit Rückmeldung,
   Minigrafen. Gerüst (Achsen, Bedienung, Leiste mit Vergleichsantwort, Uhr, Übungsrahmen,
   Minigrafen) wörtlich aus dem Leitprogramm Energie; neu sind die Simulationen (Kraft dreht
   sich, Kräfte am Ring aneinanderhängen, Rampe neigen, Schraube lösen, Wippe loslassen, Wagen
   über die Brücke) und die Übungstypen für 4.4. g = 9.81 m/s² wie Themenseite 4.4. Farben wie
   dort: Seil-, Zug- und Einzelkräfte Blau, Gewichtskraft Bernstein, Normal- und Auflagerkraft
   Grün, Reibung Türkis, Komponenten und Hebelarm Violett, Resultierende Rot (STYLEGUIDE §5.2).
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


  var G = 9.81;                                          // wie Themenseite 4.4
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
  /* Bewegte Punkte im Diagramm vollständig beschriften: «(φ; F)» mit Einheiten (06.10.2026).
     Rechts vom Punkt, wo die Spur noch nicht verläuft; reicht der Platz nicht, links davon —
     oberhalb, wenn die Kurve von unten kommt, sonst unterhalb (oder auf Punkthöhe, wenn dort ein
     anderer Punkt liegt). Liegen zwei Beschriftungen
     zu nah, rücken sie auseinander; die Legende oben rechts bleibt frei. Zwei Punkte mit gleichem
     Wert tragen eine Beschriftung «… beide». liste: [{ x, y, f (Kurve), text, cls }]. */
  function etiketten(K, W, H, liste, legende){
    var seiten = { start: [], end: [] }, y0 = K.Y(0), L = legende || [W, 0, W, 0];   // Legende: [x0, y0, x1, y1]
    // Gleiche Beschriftung zweier Punkte (z. B. F_H = μ_H · F_N an der Grenze) nur einmal, mit «beide»
    liste = liste.filter(function(q, k){
      var zwilling = liste.slice(k + 1).filter(function(r){ return r.text === q.text; }).length > 0;
      if (zwilling) return false;
      if (liste.slice(0, k).some(function(r){ return r.text === q.text; })) q = (q.text += ' beide', q);
      return true;
    });
    var pys = liste.map(function(q){ return K.Y(q.y); });
    function frei(ly, ich){                                                // keine fremden Punkte, nicht auf Achse und Zahlen
      if (ly > y0 - 4 && ly - 11 < y0 + 17) return false;
      return pys.every(function(py, k){ return k === ich || py < ly - 15 || py > ly + 7; });
    }
    function inLegende(e){                                                 // Textkasten trifft die Legende
      var a = e.anker === 'start' ? e.lx : e.lx - e.b, b = e.anker === 'start' ? e.lx + e.b : e.lx;
      return a < L[2] && b > L[0] && e.ly - 11 < L[3] && e.ly + 3 > L[1];
    }
    liste.forEach(function(q, k){
      var px = K.X(q.x), py = pys[k];
      if (px < 0 || px > W || py < 0 || py > H) return;
      var breite = q.text.length * 6.3, rechts = px + 9 + breite <= W - 2, ly = py + 4;
      if (!rechts){                                                        // links: auf die Seite, von der die Kurve nicht kommt
        var vor = K.Y(q.f(q.x - 18 / (K.X(1) - K.X(0)))), weg = vor > py ? py - 8 : py + 17;
        if (frei(weg, k)) ly = weg;
      }
      if (ly > y0 - 4 && ly - 11 < y0 + 17) ly = ly < y0 + 6 ? y0 - 5 : y0 + 29;
      seiten[rechts ? 'start' : 'end'].push({ q: q, lx: rechts ? px + 9 : px - 9, ly: ly, b: breite, anker: rechts ? 'start' : 'end' });
    });
    ['start', 'end'].forEach(function(a){
      var s = seiten[a].sort(function(u, v){ return u.ly - v.ly; }), i;
      for (i = 0; i < s.length; i++){
        if (i > 0 && s[i].ly - s[i - 1].ly < 13) s[i].ly = s[i - 1].ly + 13;
        if (inLegende(s[i])) s[i].ly = L[3] + 13;                          // unter die Legende
        if (i > 0 && s[i].ly - s[i - 1].ly < 13) s[i].ly = s[i - 1].ly + 13;
      }
      for (i = s.length - 1; i >= 0; i--){ var max = H - 3 - 13 * (s.length - 1 - i); if (s[i].ly > max) s[i].ly = max; }
      for (i = 0; i < s.length; i++){ var min = 11 + 13 * i; if (s[i].ly < min) s[i].ly = min; }
      s.forEach(function(e){ el(K.ebene, 'text', { x: e.lx, y: e.ly, 'text-anchor': a, 'class': 'p-text ' + e.q.cls }, e.q.text); });
    });
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


  function grd(a){ return a * Math.PI / 180; }
  // Kreisbogen um (cx, cy) von Winkel a0 bis a1 (Grad, mathematisch positiv, y nach oben)
  function bogen(eltern, cx, cy, r, a0, a1, cls){
    if (Math.abs(a1 - a0) < 0.5) return;
    var p0 = [cx + r * Math.cos(grd(a0)), cy - r * Math.sin(grd(a0))], p1 = [cx + r * Math.cos(grd(a1)), cy - r * Math.sin(grd(a1))];
    var gross = Math.abs(a1 - a0) > 180 ? 1 : 0, sinn = a1 > a0 ? 0 : 1;
    el(eltern, 'path', { d: 'M' + p0[0].toFixed(1) + ' ' + p0[1].toFixed(1) + ' A' + r + ' ' + r + ' 0 ' + gross + ' ' + sinn + ' ' + p1[0].toFixed(1) + ' ' + p1[1].toFixed(1), 'class': cls });
  }
  function wink(x){ return zahl(x) + '°'; }
  // Kraftebene, die mit den Kräften mitwächst: Fenster ±gr (Vielfaches von 25 N), Beschriftung je 2 Gitterlinien
  function ebeneZu(ext){
    var gr = Math.max(50, Math.ceil(ext * 1.12 / 25) * 25), t = gr <= 100 ? 25 : (gr <= 250 ? 50 : 100), m = [];
    for (var v = 2 * t; v < gr - 1e-9; v += 2 * t){ m.push(v); m.unshift(-v); }
    if (!m.length){ m = [-t, t]; }
    return { gr: gr, t: t, m: m };
  }
  // Achsenteilung zum grössten Wert: höchstens vier beschriftete Striche
  function skala(max){
    var st = [5, 10, 20, 25, 50, 100, 200, 250, 500], i = 0;
    while (i < st.length - 1 && max / st[i] > 4) i++;
    var s = st[i], oben = Math.ceil(max * 1.08 / s) * s, ym = [];
    for (var v = s; v <= oben + 1e-9; v += s) ym.push(v);
    return { y0: -0.1 * oben, y1: oben * 1.04, sy: s / 2, ym: ym };
  }
  function kn(x){ return sig(x) + NB + 'N'; }
  function F_(i){ return v_('F') + '<sub>' + i + '</sub>'; }

  /* ---------- Kapitel 1: Kraft als Vektor ----------
     Nimmt Animation 1 der Themenseite (Kraftvektor und Komponenten) als laufende Szene: Auf
     Knopfdruck dreht sich die Kraft von 0° bis zum eingestellten Winkel φ. Ihre Komponenten
     F_x = F · cos φ und F_y = F · sin φ wachsen und schrumpfen mit, und im Diagramm darunter
     zeichnen sie ihre Spur über φ. Kraft Blau, Komponenten Violett (Themenseite 4.4).
     Clipbeispiel: F = 60 N bei 40°; Startwerte F = 100 N, φ = 60° (kein Leistenziel). */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var ebene = g_(svg), dia = g_(svg, { transform: 'translate(0,238)' }), P = null, K = null, fenster = 0;
    function achsen(F){                                                    // nur neu bauen, wenn sich das Fenster ändert
      var e = ebeneZu(F); if (e.gr === fenster) { P.leeren(); K.leeren(); return; }
      fenster = e.gr; leeren(ebene); leeren(dia);
      P = Achsen(ebene, { w: 300, h: 220, x0: -e.gr * 300 / 220, x1: e.gr * 300 / 220, y0: -e.gr, y1: e.gr, sx: e.t, sy: e.t, xm: e.m, ym: e.m, xname: 'F_x [N]', yname: 'F_y [N]' });
      K = Achsen(dia, { w: 300, h: 130, x0: -30, x1: 380, y0: -e.gr, y1: e.gr, sx: 45, sy: e.t, xm: [90, 180, 270, 360], ym: e.m.length ? [-e.m[e.m.length - 1], e.m[e.m.length - 1]] : [], xname: 'φ [°]', yname: 'F [N]' });
    }
    var B = Bedienung(fig, function(){ uhr.stop(); phi = 0; zeichnen(); });
    var phi = 0, lauf = null, laeufe = [], pruefen = function(){};
    function werte(){ var F = B.wert('F'), p = B.wert('phi'); return { F: F, phi: p, Fx: F * Math.cos(grd(p)), Fy: F * Math.sin(grd(p)) }; }
    var uhr = Uhr(function(tt){
      var w = werte(); phi = Math.min(tt * 120, w.phi); zeichnen();          // 120° je Sekunde
      if (phi >= w.phi){ lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Drehen', function(){ var w = werte(); if (WENIGER){ phi = w.phi; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); phi = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); phi = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(p){ uhr.stop(); phi = p; zeichnen(); }                  // Testhaken für Clipbilder
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), F = w.F, c = Math.cos(grd(phi)), s = Math.sin(grd(phi)), fx = F * c, fy = F * s;
      B.anzeigen(); achsen(F);
      var x0 = P.X(0), y0 = P.Y(0), xe = P.X(fx), ye = P.Y(fy);
      // Komponenten (Violett) längs der Achsen, gestrichelt zur Spitze ergänzt
      if (Math.abs(fx) > 3 && Math.abs(fy) > 3){ el(P.ebene, 'line', { x1: x0, y1: ye, x2: xe, y2: ye, 'class': 'hilfslinie' }); el(P.ebene, 'line', { x1: xe, y1: y0, x2: xe, y2: ye, 'class': 'hilfslinie' }); }
      if (Math.abs(fx) > 3){ pfeil(P.ebene, x0, y0, xe, y0, 'pf-a', 7); marke(P.ebene, (x0 + xe) / 2, y0 + (fy >= 0 ? 15 : -7), 'F', 'x', 'pf-text pf-a'); }
      if (Math.abs(fy) > 3){ pfeil(P.ebene, x0, y0, x0, ye, 'pf-a', 7); marke(P.ebene, x0 + (fx >= 0 ? -6 : 6), ye + (fy >= 0 ? 14 : -6), 'F', 'y', 'pf-text pf-a', fx >= 0 ? 'end' : 'start'); }   // nahe der Spitze: weg vom Winkelbogen
      if (F > 0){ pfeil(P.ebene, x0, y0, xe, ye, 'pf-f', 9); marke(P.ebene, xe + 8 * c + (c >= 0 ? 2 : -2), ye - 8 * s + 4, 'F', '', 'pf-text pf-f', c >= 0 ? 'start' : 'end'); }
      var rb = Math.min(24, 0.45 * Math.hypot(xe - x0, ye - y0));
      bogen(P.ebene, x0, y0, rb, 0, phi, 'winkelbogen');
      var pl = grd(Math.min(phi / 2, 16));                                   // nahe der x-Achse: kollidiert nicht mit F_y
      if (phi > 12 && rb > 12) el(P.ebene, 'text', { x: x0 + (rb + 8) * Math.cos(pl), y: y0 - (rb + 8) * Math.sin(pl) + 4, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'φ');
      // Diagramm: Spur der Komponenten bis zum aktuellen Winkel
      if (phi > 0){
        K.kurve(function(p){ return F * Math.cos(grd(p)); }, 'kurve-fx', 0, phi);
        K.kurve(function(p){ return F * Math.sin(grd(p)); }, 'kurve-fy', 0, phi);
      }
      K.punkt(phi, fx, 'p-fx'); K.punkt(phi, fy, 'p-fy');
      stext(K.ebene, { x: 296, y: 14, 'text-anchor': 'end', 'class': 'legende l-fx' }, '— F_x');
      stext(K.ebene, { x: 296, y: 27, 'text-anchor': 'end', 'class': 'legende l-fy' }, '- - F_y');
      var pr = Math.round(phi), gx = F * Math.cos(grd(pr)), gy = F * Math.sin(grd(pr));   // Zeile mit dem angezeigten ganzen Winkel
      if (Math.abs(gx) < 1e-9) gx = 0; if (Math.abs(gy) < 1e-9) gy = 0;
      if (F > 0) etiketten(K, 300, 130, [
        { x: phi, y: fx, f: function(p){ return F * Math.cos(grd(p)); }, cls: 'p-fx', text: '(' + wink(pr) + '; ' + sig(gx) + NB + 'N)' },
        { x: phi, y: fy, f: function(p){ return F * Math.sin(grd(p)); }, cls: 'p-fy', text: '(' + wink(pr) + '; ' + sig(gy) + NB + 'N)' }], [262, 2, 300, 31]);
      var z = '<span>' + v_('F') + '<sub>x</sub> = ' + v_('F') + ' · cos ' + v_('φ') + ' = ' + zahl(F) + NB + 'N · cos ' + wink(pr) + ' ' + ist(gx, sig(gx)) + sig(gx) + NB + 'N</span>';
      z += '<span>' + v_('F') + '<sub>y</sub> = ' + v_('F') + ' · sin ' + v_('φ') + ' = ' + zahl(F) + NB + 'N · sin ' + wink(pr) + ' ' + ist(gy, sig(gy)) + sig(gy) + NB + 'N</span>';
      z += '<span class="sim-notiz">' + v_('φ') + ' wird von der positiven ' + v_('x') + '-Achse aus gegen den Uhrzeigersinn gemessen. Die Vorzeichen der Komponenten ergeben sich von selbst.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, F, p){ return s.lauf && s.lauf.F === F && s.lauf.phi === p; }
    pruefen = Leiste(fig, [
      { text: 'Lass eine Kraft von \\(150\\;\\text{N}\\) einmal ganz herum drehen (\\(\\varphi = 360^\\circ\\)). Bei welchen Winkeln ist \\(F_x\\) null, bei welchen \\(F_y\\)? Wo ist \\(F_x\\) negativ? Notiere deine Antwort.', ok: function(s){ return hat(s, 150, 360); },
        vergleich: '\\(F_x = 0\\) bei \\(90^\\circ\\) und \\(270^\\circ\\) (die Kraft zeigt senkrecht), \\(F_y = 0\\) bei \\(0^\\circ\\), \\(180^\\circ\\) und \\(360^\\circ\\) (waagrecht). \\(F_x\\) ist zwischen \\(90^\\circ\\) und \\(270^\\circ\\) negativ — dort zeigt die Kraft nach links. Keine Komponente wird grösser als \\(F\\): Beide bleiben zwischen \\(-150\\;\\text{N}\\) und \\(150\\;\\text{N}\\).' },
      { text: 'Stelle eine Kraft ein, deren Komponenten \\(F_x = 0\\;\\text{N}\\) und \\(F_y = -120\\;\\text{N}\\) sind, und dreh sie dorthin. Notiere Betrag und Winkel und begründe beide.', ok: function(s){ return hat(s, 120, 270); },
        vergleich: '\\(F_x = 0\\) heisst: Die Kraft steht senkrecht, \\(F_y < 0\\): Sie zeigt nach unten, also \\(\\varphi = 270^\\circ\\). Die ganze Kraft liegt in der \\(y\\)-Richtung, darum ist ihr Betrag \\(F = |F_y| = 120\\;\\text{N}\\).' },
      { text: 'Eine Kraft von \\(160\\;\\text{N}\\) soll nach rechts oben zeigen und eine waagrechte Komponente von genau \\(80\\;\\text{N}\\) haben. Welcher Winkel? Notiere ihn samt Rechnung, stelle ein und dreh.', ok: function(s){ return hat(s, 160, 60); },
        vergleich: '\\(\\cos\\varphi = \\dfrac{F_x}{F} = \\dfrac{80\\;\\text{N}}{160\\;\\text{N}} = 0.5\\), also \\(\\varphi = 60^\\circ\\). Die senkrechte Komponente ist dann \\(F_y = 160\\;\\text{N} \\cdot \\sin 60^\\circ \\approx 138.6\\;\\text{N}\\) — grösser als die waagrechte.' },
      { text: 'Gesucht ist eine Kraft nach links oben mit \\(F_x = -100\\;\\text{N}\\) und \\(F_y = 100\\;\\text{N}\\). Welcher Betrag, welcher Winkel? Stelle ein (Betrag auf \\(10\\;\\text{N}\\) genau) und dreh.', ok: function(s){ return hat(s, 140, 135); },
        vergleich: '\\(F = \\sqrt{F_x^2 + F_y^2} = \\sqrt{(100\\;\\text{N})^2 + (100\\;\\text{N})^2} \\approx 141\\;\\text{N}\\) — der Regler hat \\(140\\;\\text{N}\\). Gleich grosse Komponenten heissen \\(45^\\circ\\) zur Achse; nach links oben ist das \\(\\varphi = 180^\\circ - 45^\\circ = 135^\\circ\\).' },
      { text: 'Im Diagramm schneiden sich die Kurven von \\(F_x\\) und \\(F_y\\). Bei welchem Winkel zum ersten Mal? Dreh eine Kraft genau bis dorthin.', ok: function(s){ return s.lauf && s.lauf.F > 0 && s.lauf.phi === 45; },
        vergleich: 'Bei \\(45^\\circ\\): Dort ist \\(\\cos 45^\\circ = \\sin 45^\\circ \\approx 0.707\\), beide Komponenten sind gleich gross. Ein zweites Mal schneiden sich die Kurven bei \\(225^\\circ\\), wo beide negativ sind.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 2: Resultierende Kraft ----------
     Nimmt Animation 2 der Themenseite (Vektoraddition) als laufende Szene: Bis zu drei Kräfte
     greifen an einem Ring an. Auf Knopfdruck wandert der zweite Pfeil an die Spitze des ersten,
     der dritte an die Spitze des zweiten (Spitze an Fuss); dann erscheint die Resultierende vom
     Anfang zum Ende. Ist sie nicht null, setzt sich der Ring in ihre Richtung in Bewegung; ist
     sie null, bleibt er in Ruhe. Kräfte Blau, Resultierende Rot (Themenseite 4.4).
     Clipbeispiel: 70 N bei 0° und 70 N bei 60°; Startwerte 100 N bei 0°, 80 N bei 90°. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var flaeche = g_(svg), P = null, fenster = 0;
    function achsen(w){                                                    // Fenster nach dem weitesten Punkt der Pfeilkette
      var x = 0, y = 0, ext = w.R;
      w.k.forEach(function(k){ ext = Math.max(ext, k.F); x += k.x; y += k.y; ext = Math.max(ext, Math.abs(x), Math.abs(y)); });
      var e = ebeneZu(ext); if (e.gr === fenster){ P.leeren(); return; }
      fenster = e.gr; leeren(flaeche);
      P = Achsen(flaeche, { w: 300, h: 300, x0: -e.gr, x1: e.gr, y0: -e.gr, y1: e.gr, sx: e.t, sy: e.t, xm: e.m, ym: e.m, xname: 'F_x [N]', yname: 'F_y [N]' });
    }
    var B = Bedienung(fig, function(){ uhr.stop(); t = 0; zeichnen(); });
    var t = 0, lauf = null, laeufe = [], pruefen = function(){};
    function werte(){
      var k = [], Rx = 0, Ry = 0;
      [1, 2, 3].forEach(function(i){ var F = B.wert('F' + i), p = B.wert('p' + i); var x = F * Math.cos(grd(p)), y = F * Math.sin(grd(p)); if (Math.abs(x) < 1e-9) x = 0; if (Math.abs(y) < 1e-9) y = 0; k.push({ F: F, p: p, x: x, y: y }); Rx += x; Ry += y; });
      if (Math.abs(Rx) < 1e-9) Rx = 0; if (Math.abs(Ry) < 1e-9) Ry = 0;
      var R = Math.hypot(Rx, Ry);
      return { k: k, Rx: Rx, Ry: Ry, R: R, pR: R < 1e-9 ? 0 : ((Math.atan2(Ry, Rx) * 180 / Math.PI) + 360) % 360,
               F1: k[0].F, p1: k[0].p, F2: k[1].F, p2: k[1].p, F3: k[2].F, p3: k[2].p };
    }
    // Ablauf: 0–1 s F₂ wandert, 1–2 s F₃ wandert, 2–2.6 s Resultierende wächst, danach 2 s Bewegung
    var uhr = Uhr(function(tt){
      var w = werte(); t = tt; zeichnen();
      if (t >= (w.R > 0.5 ? 4.6 : 2.6)){ t = 9; lauf = w; laeufe.push(w); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Aneinanderhängen', function(){ if (WENIGER){ var w = werte(); t = 9; lauf = w; laeufe.push(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); t = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); t = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); t = x; zeichnen(); }
    };
    fig.__sim = sim;
    function glatt(u){ u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); }
    function zeichnen(){
      var w = werte(); B.anzeigen(); achsen(w);
      var u2 = glatt(t), u3 = glatt(t - 1), uR = glatt((t - 2) / 0.6), um = Math.max(0, Math.min(2, t - 2.6));
      // Bewegung des Rings: wächst quadratisch, höchstens 70 px
      var d = w.R > 0.5 ? Math.min(70, 9 * um * um) : 0, ox = d * (w.Rx / (w.R || 1)), oy = -d * (w.Ry / (w.R || 1));
      function X(x){ return P.X(x) + ox; } function Y(y){ return P.Y(y) + oy; }
      var a = [0, 0], fuss = [[0, 0], [w.k[0].x * u2, w.k[0].y * u2], [(w.k[0].x + w.k[1].x) * u3, (w.k[0].y + w.k[1].y) * u3]];
      var gezeigt = 0;
      w.k.forEach(function(k, i){
        if (k.F <= 0) return; gezeigt++;
        var f = fuss[i];
        if (i > 0 && t > 0) pfeil(P.ebene, X(0), Y(0), X(k.x), Y(k.y), 'pf-f geist', 7);   // ursprüngliche Lage blass
        pfeil(P.ebene, X(f[0]), Y(f[1]), X(f[0] + k.x), Y(f[1] + k.y), 'pf-f', 9);
        var c = Math.cos(grd(k.p)), s = Math.sin(grd(k.p));
        marke(P.ebene, X(f[0] + k.x * 0.55) + 12 * s, Y(f[1] + k.y * 0.55) + 12 * c + 4, 'F', String(i + 1), 'pf-text pf-f');
      });
      if (uR > 0 && w.R > 0.5){
        pfeil(P.ebene, X(0), Y(0), X(w.Rx * uR), Y(w.Ry * uR), 'pf-res', 10);
        if (uR >= 1) marke(P.ebene, X(w.Rx * 0.5) - 16 * Math.sin(grd(w.pR)), Y(w.Ry * 0.5) - 16 * Math.cos(grd(w.pR)) + 4, 'F', 'res', 'pf-text pf-res');
      }
      if (d > 0) el(P.ebene, 'line', { x1: P.X(0), y1: P.Y(0), x2: X(0), y2: Y(0), 'class': 'spur' });
      el(P.ebene, 'circle', { cx: X(0), cy: Y(0), r: 7, 'class': 'ring' });
      if (t >= 2.6 && w.R <= 0.5) el(P.ebene, 'text', { x: 150, y: 290, 'text-anchor': 'middle', 'class': 'bt-meldung' }, 'Gleichgewicht: Der Ring bleibt in Ruhe.');
      else if (t >= 2.6) stext(P.ebene, { x: 150, y: 290, 'text-anchor': 'middle', 'class': 'bt-meldung' }, 'Der Ring setzt sich in Richtung F_res in Bewegung.');
      // Formelzeilen aus den Eingaben (keine gerundeten Zwischenwerte)
      var aktiv = w.k.map(function(k, i){ return [k, i + 1]; }).filter(function(q){ return q[0].F > 0; });
      function summe(fn, ach){
        if (!aktiv.length) return '0';
        return aktiv.map(function(q){ return zahl(q[0].F) + NB + 'N · ' + fn + ' ' + wink(q[0].p); }).join(' + ');
      }
      var z = '<span>' + v_('F') + '<sub>res,x</sub> = Σ ' + v_('F') + ' · cos ' + v_('φ') + ' = ' + summe('cos') + ' ' + ist(w.Rx, sig(w.Rx)) + sig(w.Rx) + NB + 'N</span>';
      z += '<span>' + v_('F') + '<sub>res,y</sub> = Σ ' + v_('F') + ' · sin ' + v_('φ') + ' = ' + summe('sin') + ' ' + ist(w.Ry, sig(w.Ry)) + sig(w.Ry) + NB + 'N</span>';
      z += '<span>' + v_('F') + '<sub>res</sub> = √(' + v_('F') + '<sub>res,x</sub>² + ' + v_('F') + '<sub>res,y</sub>²) ' + ist(w.R, sig(w.R)) + sig(w.R) + NB + 'N' + (w.R > 0.5 ? '; Richtung ' + v_('φ') + ' ' + ist(w.pR, sig(w.pR)) + sig(w.pR) + '°' : '') + '</span>';
      z += '<span class="sim-notiz">Ein Regler auf 0 N blendet die Kraft aus. Die Pfeile zeigen Kräfte (Achsen in N), der Ring nur, wohin er sich bewegt.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function zwischen(l){ var d = Math.abs(l.p1 - l.p2) % 360; return d > 180 ? 360 - d : d; }
    function paar(l, a, b){ return l.F3 === 0 && ((l.F1 === a && l.F2 === b) || (l.F1 === b && l.F2 === a)); }
    pruefen = Leiste(fig, [
      { text: 'Zwei Kräfte von je \\(100\\;\\text{N}\\) (\\(F_3 = 0\\)): Häng sie gleichgerichtet, rechtwinklig und entgegengesetzt aneinander. Wie hängt die Resultierende vom Winkel zwischen den Kräften ab? Notiere deine Antwort.',
        ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (paar(l, 100, 100)) n[zwischen(l)] = true; }); return n[0] && n[90] && n[180]; },
        vergleich: 'Gleichgerichtet \\(200\\;\\text{N}\\), rechtwinklig \\(\\sqrt{(100\\;\\text{N})^2 + (100\\;\\text{N})^2} \\approx 141\\;\\text{N}\\), entgegengesetzt \\(0\\;\\text{N}\\). Je grösser der Winkel zwischen den Kräften, desto kleiner die Resultierende. Nur gleichgerichtete Kräfte darf man einfach addieren.' },
      { text: '\\(F_1 = 100\\;\\text{N}\\) bei \\(0^\\circ\\) und \\(F_2 = 100\\;\\text{N}\\) bei \\(120^\\circ\\) sind eingestellt. Finde die dritte Kraft, mit der der Ring in Ruhe bleibt.',
        setup: function(S){ S.setze({ F1: 100, p1: 0, F2: 100, p2: 120, F3: 0, p3: 0 }); },
        ok: function(s){ var l = s.lauf; return l && l.F1 === 100 && l.p1 === 0 && l.F2 === 100 && l.p2 === 120 && l.R < 0.5; },
        vergleich: 'Die beiden ergeben \\(F_\\text{res} = 100\\;\\text{N}\\) bei \\(60^\\circ\\). Die dritte Kraft muss gleich gross und entgegengesetzt sein: \\(F_3 = 100\\;\\text{N}\\) bei \\(240^\\circ\\). Die drei Pfeile schliessen sich dann zu einem Dreieck.' },
      { text: '\\(F_1 = 100\\;\\text{N}\\) bei \\(30^\\circ\\) ist eingestellt. Wähle \\(F_2\\) (Betrag und Richtung) so, dass die Resultierende genau \\(100\\;\\text{N}\\) senkrecht nach oben zeigt. Notiere, wie du \\(F_2\\) gefunden hast.',
        setup: function(S){ S.setze({ F1: 100, p1: 30, F2: 50, p2: 0, F3: 0, p3: 0 }); },
        ok: function(s){ var l = s.lauf; return l && l.F1 === 100 && l.p1 === 30 && l.F3 === 0 && Math.abs(l.Rx) < 0.5 && Math.abs(l.Ry - 100) < 0.5; },
        vergleich: 'Über die Komponenten: \\(F_1\\) hat \\(F_{1,x} = 100\\;\\text{N} \\cdot \\cos 30^\\circ \\approx 86.6\\;\\text{N}\\) und \\(F_{1,y} = 50\\;\\text{N}\\). Für \\(F_\\text{res} = 100\\;\\text{N}\\) nach oben braucht \\(F_2\\) also \\(F_{2,x} = -86.6\\;\\text{N}\\) und \\(F_{2,y} = 50\\;\\text{N}\\): \\(F_2 = 100\\;\\text{N}\\) bei \\(150^\\circ\\) — das Spiegelbild von \\(F_1\\).' },
      { text: 'Kann die Resultierende aus \\(60\\;\\text{N}\\) und \\(80\\;\\text{N}\\) (\\(F_3 = 0\\)) \\(150\\;\\text{N}\\) betragen? Häng die beiden unter mindestens drei verschiedenen Winkeln aneinander. Begründe.',
        ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (paar(l, 60, 80)) n[zwischen(l)] = true; }); return Object.keys(n).length >= 3; },
        vergleich: 'Nein. Die Resultierende liegt zwischen \\(80\\;\\text{N} - 60\\;\\text{N} = 20\\;\\text{N}\\) (entgegengesetzt) und \\(80\\;\\text{N} + 60\\;\\text{N} = 140\\;\\text{N}\\) (gleichgerichtet). Mehr als die Summe der Beträge geht nie.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 3: Kräfte am ruhenden Körper ----------
     Nimmt Animation 7 der Themenseite (Klotz auf der schiefen Ebene) als laufende Szene: Auf
     Knopfdruck neigt sich die Rampe von 0° bis zum eingestellten Winkel. Gewichtskraft
     (Bernstein), Normalkraft (Grün) und Haftreibung (Türkis) passen sich laufend an; die
     Komponenten der Gewichtskraft sind violett. Im Diagramm wachsen F_H, F_N und die Grenze
     μ_H · F_N über α mit. Wird tan α grösser als μ_H, rutscht die Kiste. Clipbeispiel:
     m = 12 kg, μ_H = 0.65; Startwerte m = 10 kg, μ_H = 0.40, bis 15°. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,212)' });
    var K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); los(); zeichnen(); });
    var al = 0, rutsch = 0, gerutscht = false, lauf = null, laeufe = [], pruefen = function(){};
    var HX = 22, HY = 168, LB = 262, PXM = 100;                            // Gelenk, Brettlänge, 100 px je m
    function werte(){ var m = B.wert('m'), mu = B.wert('mu'), ae = B.wert('ae'); return { m: m, mu: mu, ae: ae, FG: m * G, ag: Math.atan(mu) * 180 / Math.PI }; }
    var t1 = 0;
    var uhr = Uhr(function(tt){
      var w = werte(), te = w.ae / 6;                                    // 6° je Sekunde
      if (!gerutscht){
        al = Math.min(tt * 6, w.ae);
        if (Math.tan(grd(al)) > w.mu + 1e-12){ al = w.ag; gerutscht = true; t1 = tt; }
        else if (al >= w.ae){ lauf = fertig(w); zeichnen(); return false; }
      }
      if (gerutscht){
        var a = G * (Math.sin(grd(al)) - 0.8 * w.mu * Math.cos(grd(al))), s = 0.5 * a * (tt - t1) * (tt - t1);
        rutsch = Math.min(s, 1.4);
        if (rutsch >= 1.4){ lauf = fertig(w); zeichnen(); return false; }
      }
      zeichnen();
    });
    function fertig(w){ var l = { m: w.m, mu: w.mu, ae: w.ae, rutscht: gerutscht, al: al }; laeufe.push(l); return l; }
    function los(){ al = 0; rutsch = 0; gerutscht = false; }
    aktionen(fig, [['start', '▶ Neigen', function(){ uhr.stop(); los(); if (WENIGER){ var w = werte(); if (Math.tan(grd(w.ae)) > w.mu + 1e-12){ al = w.ag; gerutscht = true; rutsch = 1.4; } else al = w.ae; lauf = fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); los(); zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); los(); B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(a){ uhr.stop(); los(); al = a; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), r = grd(al), c = Math.cos(r), s = Math.sin(r);
      var FH = w.FG * s, FN = w.FG * c, Fmax = w.mu * FN, FR = gerutscht ? 0.8 * Fmax : FH;
      B.anzeigen(); leeren(szene); leeren(dia);
      var sk = skala(w.FG * 1.4);                                           // Luft über F_G für die Legende
      K = Achsen(dia, { w: 300, h: 140, x0: -3, x1: 48, y0: sk.y0, y1: sk.y1, sx: 5, sy: sk.sy, xm: [10, 20, 30, 40], ym: sk.ym, xname: 'α [°]', yname: 'F [N]' });
      // Rampe: Gelenk links unten, Brett steigt nach rechts
      var ux = Math.cos(r), uy = -Math.sin(r), nx = -Math.sin(r), ny = -Math.cos(r);   // längs (aufwärts) und senkrecht (nach aussen)
      el(szene, 'line', { x1: 8, y1: HY, x2: 296, y2: HY, 'class': 'boden' });
      el(szene, 'polygon', { points: HX + ',' + HY + ' ' + (HX + LB * ux) + ',' + (HY + LB * uy) + ' ' + (HX + LB * ux) + ',' + HY, 'class': 'rampe' });
      el(szene, 'line', { x1: HX, y1: HY, x2: HX + LB * ux, y2: HY + LB * uy, 'class': 'brett' });
      el(szene, 'line', { x1: HX + 6 * ux - 0 * nx, y1: HY + 6 * uy, x2: HX + 6 * ux + 12 * nx, y2: HY + 6 * uy + 12 * ny, 'class': 'anschlag' });
      bogen(szene, HX, HY, 46, 0, al, 'winkelbogen');
      if (al > 4) el(szene, 'text', { x: HX + 54 * Math.cos(r / 2) + 2, y: HY - 54 * Math.sin(r / 2) + 4, 'class': 'bt-klein' }, 'α = ' + sig(al) + '°');
      // Kiste: Mitte 1.7 m vom Gelenk, rutscht um «rutsch» m hinunter
      var d = (1.7 - rutsch) * PXM, bw = 40, bh = 30;
      var mx = HX + d * ux + bh / 2 * nx, my = HY + d * uy + bh / 2 * ny;     // Mittelpunkt der Kiste
      el(szene, 'rect', { x: -bw / 2, y: -bh / 2, width: bw, height: bh, rx: 2, 'class': 'kiste', transform: 'translate(' + mx.toFixed(1) + ',' + my.toFixed(1) + ') rotate(' + (-al).toFixed(2) + ')' });
      var k = 50 / w.FG, kx = HX + d * ux, ky = HY + d * uy;                  // Gewichtskraft immer 50 px lang; Kontaktpunkt
      if (gerutscht && rutsch > 0.15){ zeichneDia(); return; }                 // unten angekommen: nur noch die Kiste
      // Gewichtskraft und ihre Komponenten
      pfeil(szene, mx, my, mx, my + w.FG * k, 'pf-g', 8); marke(szene, mx + 5, my + w.FG * k + 2, 'F', 'G', 'pf-text pf-g', 'start');
      if (al > 1){
        pfeil(szene, mx, my, mx - FH * k * ux, my - FH * k * uy, 'pf-a duenn', 6); marke(szene, mx - FH * k * ux - 4, my - FH * k * uy - 6, 'F', 'H', 'pf-text pf-a', 'end');
        pfeil(szene, mx, my, mx - FN * k * nx, my - FN * k * ny, 'pf-a duenn', 6);
        el(szene, 'line', { x1: mx - FH * k * ux, y1: my - FH * k * uy, x2: mx, y2: my + w.FG * k, 'class': 'hilfslinie' });
      }
      // Normalkraft am Kontakt nach aussen, Reibung am Kontakt hangaufwärts
      pfeil(szene, kx - 8 * ux, ky - 8 * uy, kx - 8 * ux + FN * k * nx, ky - 8 * uy + FN * k * ny, 'pf-n', 8);
      marke(szene, kx - 8 * ux + FN * k * nx - 6, ky - 8 * uy + FN * k * ny + 2, 'F', 'N', 'pf-text pf-n', 'end');
      if (FR * k > 2){ pfeil(szene, kx + bw / 2 * ux, ky + bw / 2 * uy, kx + bw / 2 * ux + FR * k * ux, ky + bw / 2 * uy + FR * k * uy, 'pf-reib', 7); marke(szene, kx + (bw / 2 + FR * k) * ux + 4, ky + (bw / 2 + FR * k) * uy + 12, 'F', 'R', 'pf-text pf-reib', 'start'); }
      zeichneDia();
    }
    function zeichneDia(){
      var w = werte(), r = grd(al), FH = w.FG * Math.sin(r), FN = w.FG * Math.cos(r), Fmax = w.mu * FN;
      if (gerutscht) stext(szene, { x: 296, y: 22, 'text-anchor': 'end', 'class': 'bt-meldung' }, 'tan α > μ_H: Die Kiste rutscht.');
      // Diagramm: Kräfte über dem Winkel bis zum aktuellen Winkel
      K.kurve(function(a){ return w.FG; }, 'vorher', 0, 45);
      if (al > 0){
        K.kurve(function(a){ return w.FG * Math.sin(grd(a)); }, 'kurve-fh', 0, al);
        K.kurve(function(a){ return w.FG * Math.cos(grd(a)); }, 'kurve-fn', 0, al);
        K.kurve(function(a){ return w.mu * w.FG * Math.cos(grd(a)); }, 'kurve-fr', 0, al);
      }
      K.punkt(al, FH, 'p-fh'); K.punkt(al, FN, 'p-fn'); K.punkt(al, Fmax, 'p-fr');
      var aw = wink(+al.toFixed(1));                                          // wie in der Formelzeile
      etiketten(K, 300, 140, [
        { x: al, y: FN, f: function(a){ return w.FG * Math.cos(grd(a)); }, cls: 'p-fn', text: '(' + aw + '; ' + sig(FN) + NB + 'N)' },
        { x: al, y: FH, f: function(a){ return w.FG * Math.sin(grd(a)); }, cls: 'p-fh', text: '(' + aw + '; ' + sig(FH) + NB + 'N)' },
        { x: al, y: Fmax, f: function(a){ return w.mu * w.FG * Math.cos(grd(a)); }, cls: 'p-fr', text: '(' + aw + '; ' + sig(Fmax) + NB + 'N)' }], [228, 2, 300, 51]);
      if (gerutscht) el(K.ebene, 'line', { x1: K.X(w.ag), y1: K.Y(0), x2: K.X(w.ag), y2: K.Y(FH), 'class': 'hilfslinie' });
      stext(K.ebene, { x: 296, y: 12, 'text-anchor': 'end', 'class': 'legende l-fn' }, '— F_N');
      stext(K.ebene, { x: 296, y: 24, 'text-anchor': 'end', 'class': 'legende l-fh' }, '— F_H');
      stext(K.ebene, { x: 296, y: 36, 'text-anchor': 'end', 'class': 'legende l-fr' }, '- - μ_H · F_N');
      stext(K.ebene, { x: 296, y: 48, 'text-anchor': 'end', 'class': 'legende' }, '- - F_G');
      var A = wink(+al.toFixed(1));
      var z = '<span>' + F_('H') + ' = ' + v_('m') + ' · ' + v_('g') + ' · sin ' + v_('α') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² · sin ' + A + ' ' + ist(FH, sig(FH)) + sig(FH) + NB + 'N</span>';
      z += '<span>' + F_('N') + ' = ' + v_('m') + ' · ' + v_('g') + ' · cos ' + v_('α') + ' = ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² · cos ' + A + ' ' + ist(FN, sig(FN)) + sig(FN) + NB + 'N</span>';
      z += '<span>' + F_('R,max') + ' = ' + v_('μ') + '<sub>H</sub> · ' + v_('m') + ' · ' + v_('g') + ' · cos ' + v_('α') + ' = ' + zahl(w.mu) + ' · ' + zahl(w.m) + NB + 'kg · 9.81' + NB + 'm/s² · cos ' + A + ' ' + ist(Fmax, sig(Fmax)) + sig(Fmax) + NB + 'N</span>';
      z += '<span class="sim-notiz">Pfeile im Massstab der Gewichtskraft. ' + (gerutscht ? 'Rutschen: Die Haftreibung reicht nicht mehr, es wirkt die kleinere Gleitreibung (hier 80 % von ' + F_('R,max') + ') — die Bewegung ist Stoff der Dynamik.'
                                                : 'Die Kiste haftet: Die Haftreibung ist genau so gross wie nötig, ' + F_('R') + ' = ' + F_('H') + ' ' + ist(FH, sig(FH)) + sig(FH) + NB + 'N. Sie kann höchstens ' + F_('R,max') + ' werden.') + '</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    pruefen = Leiste(fig, [
      { text: 'Neige die Rampe bis \\(45^\\circ\\) mit \\(\\mu_H = 0.70\\). Bei welchem Winkel beginnt die Kiste zu rutschen? Wo siehst du das im Diagramm? Notiere, dann vergleiche.', ok: function(s){ return s.lauf && s.lauf.mu === 0.7 && s.lauf.ae === 45 && s.lauf.rutscht; },
        vergleich: 'Bei rund \\(35^\\circ\\): Dort wird \\(\\tan\\alpha\\) grösser als \\(\\mu_H = 0.70\\), denn \\(\\arctan 0.70 \\approx 35.0^\\circ\\). Im Diagramm schneidet die Kurve \\(F_H\\) dort die gestrichelte Grenze \\(\\mu_H \\cdot F_N\\).' },
      { text: 'Eine Kiste mit \\(m = 20\\;\\text{kg}\\), \\(\\mu_H = 0.60\\): Neige bis \\(20^\\circ\\). Wie gross sind Normalkraft und Haftreibung? Notiere, dann vergleiche.', ok: function(s){ return s.lauf && s.lauf.m === 20 && s.lauf.mu === 0.6 && s.lauf.ae === 20 && !s.lauf.rutscht; },
        vergleich: '\\(F_N = m \\cdot g \\cdot \\cos\\alpha = 20\\;\\text{kg} \\cdot 9.81\\;\\text{m/s}^2 \\cdot \\cos 20^\\circ \\approx 184\\;\\text{N}\\). Die Haftreibung ist so gross wie die Hangabtriebskraft, \\(F_R = F_H \\approx 67.1\\;\\text{N}\\) — nicht \\(\\mu_H \\cdot F_N \\approx 111\\;\\text{N}\\). Das ist nur ihr Höchstwert.' },
      { text: 'Lass die Kiste mit zwei verschiedenen Massen, aber derselben Haftreibungszahl rutschen. Hängt der Grenzwinkel von der Masse ab? Begründe.', ok: function(s){ var n = {}; s.laeufe.forEach(function(l){ if (l.rutscht){ n[l.mu] = n[l.mu] || {}; n[l.mu][l.m] = true; } }); for (var mu in n) if (Object.keys(n[mu]).length >= 2) return true; return false; },
        vergleich: 'Nein. Hangabtrieb \\(m \\cdot g \\cdot \\sin\\alpha\\) und grösste Haftreibung \\(\\mu_H \\cdot m \\cdot g \\cdot \\cos\\alpha\\) wachsen beide mit der Masse. Setzt man sie gleich, kürzt sich \\(m \\cdot g\\): \\(\\tan\\alpha = \\mu_H\\).' },
      { text: 'Stelle die kleinste Haftreibungszahl ein, bei der die Kiste bis \\(40^\\circ\\) liegen bleibt, und prüfe es.', ok: function(s){ return s.lauf && s.lauf.ae === 40 && s.lauf.mu === 0.85 && !s.lauf.rutscht; },
        vergleich: '\\(\\mu_H \\ge \\tan 40^\\circ \\approx 0.839\\). Auf dem Regler ist \\(0.85\\) der kleinste Wert, der reicht; bei \\(0.80\\) rutscht die Kiste schon bei rund \\(38.7^\\circ\\).' },
      { text: 'Eine Kiste mit \\(30\\;\\text{kg}\\) liegt auf der waagrechten Rampe (\\(\\alpha = 0^\\circ\\)). Starte. Welche Kräfte wirken, und wie gross ist die Reibung? Begründe.', ok: function(s){ return s.lauf && s.lauf.ae === 0 && s.lauf.m === 30; },
        vergleich: 'Gewichtskraft und Normalkraft, beide \\(30\\;\\text{kg} \\cdot 9.81\\;\\text{m/s}^2 \\approx 294\\;\\text{N}\\), entgegengesetzt. Reibung wirkt keine: Nichts zieht die Kiste seitlich, also muss die Haftreibung nichts ausgleichen.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 4: Drehmoment am Schraubenschlüssel ----------
     Nimmt Animation 4 der Themenseite (Drehmoment, Hebelarm und Winkel) als laufende Szene:
     Auf Knopfdruck wächst die Zugkraft am Schlüssel von 0 bis F; das Drehmoment M = F · l · sin α
     steigt im Balken mit. Erreicht es das Losbrechmoment der Schraube, dreht sich der Schlüssel,
     sonst hält die Schraube. Wirksamer Hebelarm r = l · sin α violett gestrichelt.
     Clipbeispiel: 120 N an 0.25 m; Startwerte 100 N, 0.20 m, 90°, Schraube 60 Nm. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,228)' });
    var B = Bedienung(fig, function(){ uhr.stop(); los(); zeichnen(); });
    var Fj = 0, dreh = 0, geloest = false, ende = false, lauf = null, laeufe = [], pruefen = function(){};
    var DX = 236, DY = 60, PX = 520;                                       // Drehachse rechts, Schlüssel nach links, 520 px je m
    function werte(){ var F = B.wert('F'), l = B.wert('l'), a = B.wert('al'), Ml = +B.wert('Ml'); return { F: F, l: l, a: a, Ml: Ml, r: l * Math.sin(grd(a)), M: F * l * Math.sin(grd(a)) }; }
    function los(){ Fj = 0; dreh = 0; geloest = false; ende = false; }
    var tg = 0;
    var uhr = Uhr(function(tt){
      var w = werte();
      if (!geloest){
        Fj = Math.min(w.F, tt / 1.6 * 400);                                  // 250 N je Sekunde
        if (w.r > 1e-9 && Fj * w.r >= w.Ml - 1e-9){ Fj = w.Ml / w.r; geloest = true; tg = tt; }
        else if (Fj >= w.F){ lauf = fertig(w); zeichnen(); return false; }
      }
      if (geloest){ dreh = Math.min(25, (tt - tg) * 30); if (dreh >= 25){ lauf = fertig(w); zeichnen(); return false; } }
      zeichnen();
    });
    function fertig(w){ ende = true; var l = { F: w.F, l: w.l, a: w.a, Ml: w.Ml, M: w.M, geloest: geloest }; laeufe.push(l); return l; }
    aktionen(fig, [['start', '▶ Ziehen', function(){ uhr.stop(); los(); if (WENIGER){ var w = werte(); if (w.r > 1e-9 && w.M >= w.Ml - 1e-9){ Fj = w.Ml / w.r; geloest = true; dreh = 25; } else Fj = w.F; lauf = fertig(w); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); los(); zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); los(); B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(F){ uhr.stop(); los(); Fj = F; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), M = Fj * w.r;
      B.anzeigen(); leeren(szene); leeren(dia);
      // Schlüssel zeigt nach links, Kraft nach unten: Er dreht gegen den Uhrzeigersinn — so löst man ein Rechtsgewinde
      var th = grd(dreh), ux = -Math.cos(th), uy = Math.sin(th);
      var L = w.l * PX, ex = DX + L * ux, ey = DY + L * uy;
      // Schraube (Sechskant) und Schlüssel
      var pts = []; for (var i = 0; i < 6; i++){ var q = th + i * Math.PI / 3; pts.push((DX + 15 * Math.cos(q)).toFixed(1) + ',' + (DY + 15 * Math.sin(q)).toFixed(1)); }
      el(szene, 'polygon', { points: pts.join(' '), 'class': 'mutter' });
      el(szene, 'line', { x1: DX, y1: DY, x2: ex, y2: ey, 'class': 'schluessel' });
      el(szene, 'circle', { cx: DX, cy: DY, r: 3, 'class': 'achspunkt' });
      el(szene, 'text', { x: DX + 20, y: DY - 18, 'class': 'bt-klein' }, 'D');
      // Kraft am Ende unter α zum Schlüssel (α = 90°: senkrecht nach unten)
      var fr = th + grd(w.a), fx = -Math.cos(fr), fy = Math.sin(fr), k = 0.2;
      // Wirkungslinie und wirksamer Hebelarm
      el(szene, 'line', { x1: ex - 110 * fx, y1: ey - 110 * fy, x2: ex + 95 * fx, y2: ey + 95 * fy, 'class': 'wirkungslinie' });
      var tt = (DX - ex) * fx + (DY - ey) * fy, lx = ex + tt * fx, ly = ey + tt * fy;
      if (w.r * PX > 3) el(szene, 'line', { x1: DX, y1: DY, x2: lx, y2: ly, 'class': 'hebelarm' });
      if (w.r * PX > 18){ var nx = (ly - DY) / (w.r * PX), ny = -(lx - DX) / (w.r * PX); if (ny > 0){ nx = -nx; ny = -ny; }   // Normale nach oben
        el(szene, 'text', { x: (DX + lx) / 2 + 12 * nx, y: (DY + ly) / 2 + 12 * ny + 4, 'text-anchor': 'middle', 'class': 'pf-text pf-a' }, 'r'); }
      var lF = Math.max(Fj, 0) * k;
      if (lF > 2){ pfeil(szene, ex, ey, ex + lF * fx, ey + lF * fy, 'pf-f', 9); marke(szene, ex + lF * fx - 7, ey + lF * fy + 4, 'F', '', 'pf-text pf-f', 'end'); }
      if (w.a > 0 && w.a < 90) bogen(szene, ex, ey, 18, 180 + dreh, 180 + dreh + w.a, 'winkelbogen');
      var lnx = -uy, lny = ux; if (lny < 0){ lnx = -lnx; lny = -lny; }    // Normale nach unten
      el(szene, 'text', { x: (DX + ex) / 2 + 14 * lnx, y: (DY + ey) / 2 + 14 * lny + 4, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'l = ' + zahl(w.l) + ' m');
      if (geloest) el(szene, 'text', { x: 4, y: 16, 'text-anchor': 'start', 'class': 'bt-meldung' }, 'Die Schraube löst sich.');
      else if (ende) el(szene, 'text', { x: 4, y: 16, 'text-anchor': 'start', 'class': 'bt-meldung' }, 'Die Schraube hält.');
      // Balken: Drehmoment gegen Losbrechmoment, 0 bis 120 Nm
      var X = function(m){ return 30 + m * 2.2; };
      el(dia, 'rect', { x: 30, y: 10, width: 264, height: 22, 'class': 'balken-leer' });
      if (M > 0) el(dia, 'rect', { x: 30, y: 10, width: Math.min(264, M * 2.2), height: 22, 'class': 'balken-m' });
      el(dia, 'line', { x1: X(w.Ml), y1: 4, x2: X(w.Ml), y2: 38, 'class': 'grenze' });
      el(dia, 'text', { x: X(w.Ml), y: 50, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'Schraube: ' + w.Ml + ' Nm');
      el(dia, 'text', { x: 24, y: 26, 'text-anchor': 'end', 'class': 'achsname' }, 'M');
      [0, 40, 80].forEach(function(m){ el(dia, 'text', { x: X(m), y: 64, 'text-anchor': 'middle', 'class': 'skala' }, m); });
      el(dia, 'text', { x: 296, y: 64, 'text-anchor': 'end', 'class': 'achsname' }, '120 Nm');
      var z = '<span>' + v_('r') + ' = ' + v_('l') + ' · sin ' + v_('α') + ' = ' + zahl(w.l) + NB + 'm · sin ' + wink(w.a) + ' ' + ist(w.r, sig(w.r)) + sig(w.r) + NB + 'm</span>';
      z += '<span>' + v_('M') + ' = ' + v_('F') + ' · ' + v_('l') + ' · sin ' + v_('α') + ' = ' + sig(Fj) + NB + 'N · ' + zahl(w.l) + NB + 'm · sin ' + wink(w.a) + ' ' + ist(M, sig(M)) + sig(M) + NB + 'Nm</span>';
      z += '<span class="sim-notiz">Beim Ziehen wächst die Kraft von 0 bis ' + zahl(w.F) + NB + 'N; die Zeile zeigt die momentane Kraft. ' + v_('α') + ': Winkel zwischen Schlüssel und Kraft. ' + v_('r') + ': senkrechter Abstand der Wirkungslinie von der Drehachse D (wirksamer Hebelarm).</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, F, l, a, Ml){ return s.lauf && s.lauf.F === F && s.lauf.l === l && s.lauf.a === a && s.lauf.Ml === Ml; }
    pruefen = Leiste(fig, [
      { text: 'Die Schraube sitzt mit \\(90\\;\\text{Nm}\\) fest. Löse sie mit einem \\(0.30\\;\\text{m}\\) langen Schlüssel, senkrecht ziehend, mit der kleinsten Kraft, die reicht. Notiere zuerst deine Rechnung.', ok: function(s){ return hat(s, 300, 0.3, 90, 90) && s.lauf.geloest; },
        vergleich: '\\(F = \\dfrac{M}{r} = \\dfrac{90\\;\\text{Nm}}{0.30\\;\\text{m}} = 300\\;\\text{N}\\). Mit weniger Kraft bleibt das Drehmoment unter dem Losbrechmoment, und die Schraube hält.' },
      { text: 'Jetzt dieselben \\(300\\;\\text{N}\\) am selben Schlüssel, aber unter \\(30^\\circ\\) zum Schlüssel. Zieh. Warum löst sich die Schraube nicht? Wie viel Kraft bräuchte es?', ok: function(s){ return hat(s, 300, 0.3, 30, 90); },
        vergleich: 'Der wirksame Hebelarm ist nur \\(r = 0.30\\;\\text{m} \\cdot \\sin 30^\\circ = 0.15\\;\\text{m}\\), das Drehmoment \\(300\\;\\text{N} \\cdot 0.15\\;\\text{m} = 45\\;\\text{Nm}\\) — die Hälfte. Für \\(90\\;\\text{Nm}\\) bräuchte es \\(F = \\dfrac{90\\;\\text{Nm}}{0.15\\;\\text{m}} = 600\\;\\text{N}\\), mehr als der Regler hergibt.' },
      { text: 'Die \\(60\\)-Nm-Schraube soll mit nur \\(150\\;\\text{N}\\) aufgehen, senkrecht gezogen. Wie lang muss der Schlüssel mindestens sein? Notiere deine Rechnung, stelle ein und zieh.', ok: function(s){ return hat(s, 150, 0.4, 90, 60) && s.lauf.geloest; },
        vergleich: '\\(r = \\dfrac{M}{F} = \\dfrac{60\\;\\text{Nm}}{150\\;\\text{N}} = 0.40\\;\\text{m}\\). Ein längerer Schlüssel geht auch, ein kürzerer nicht: Je kleiner die Kraft, desto länger muss der Hebelarm sein.' },
      { text: 'Mit \\(240\\;\\text{N}\\) am \\(0.25\\;\\text{m}\\) langen Schlüssel soll die \\(30\\)-Nm-Schraube aufgehen. Unter welchem kleinsten Winkel geht es gerade noch? Notiere deine Rechnung, dann prüfe.', ok: function(s){ return hat(s, 240, 0.25, 30, 30) && s.lauf.geloest; },
        vergleich: '\\(M = F \\cdot l \\cdot \\sin\\alpha\\), also \\(\\sin\\alpha = \\dfrac{30\\;\\text{Nm}}{240\\;\\text{N} \\cdot 0.25\\;\\text{m}} = 0.5\\) und \\(\\alpha = 30^\\circ\\). Senkrecht gezogen wären es \\(60\\;\\text{Nm}\\) — doppelt so viel wie nötig.' },
      { text: 'Zieh mit \\(400\\;\\text{N}\\) genau längs des Schlüssels (\\(\\alpha = 0^\\circ\\)). Warum dreht sich nichts, egal wie stark du ziehst? Begründe.', ok: function(s){ return s.lauf && s.lauf.F === 400 && s.lauf.a === 0; },
        vergleich: 'Die Wirkungslinie geht durch die Drehachse: Der wirksame Hebelarm ist \\(r = l \\cdot \\sin 0^\\circ = 0\\), also auch \\(M = F \\cdot r = 0\\). Eine Kraft, die auf die Achse zeigt, dreht nicht.' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 5: Hebelgesetz an der Wippe ----------
     Nimmt Animation 5 der Themenseite (zweiarmiger Hebel) und die Einstiegs-Wippe als laufende
     Szene: Die Wippe wird zuerst waagrecht gehalten. Auf Knopfdruck wird sie losgelassen; sind
     die Drehmomente verschieden, kippt sie zur Seite des grösseren Moments, bis ein Ende den
     Boden berührt (Drehbeschleunigung aus Moment und Trägheit). Gleich grosse Momente: Sie
     bleibt waagrecht. Gewichtskräfte Bernstein, Momente in zwei Balken.
     Clipbeispiel: 30 kg bei 1.6 m gegen 40 kg; Startwerte 35 kg bei 1.4 m, 20 kg bei 1.5 m. */
  (function(){
    var fig = document.getElementById('sim5'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,176)' });
    var B = Bedienung(fig, function(){ uhr.stop(); th = 0; om = 0; ende = null; zeichnen(); });
    var th = 0, om = 0, ende = null, lauf = null, laeufe = [], pruefen = function(){};
    var DX = 150, DY = 128, PX = 62, HOCH = 0.5, HALB = 2.2, TMAX = Math.asin(HOCH / HALB);   // Drehpunkt 0.5 m hoch, Brett 4.4 m
    function werte(){ var m1 = B.wert('m1'), r1 = B.wert('r1'), m2 = B.wert('m2'), r2 = B.wert('r2'); return { m1: m1, r1: r1, m2: m2, r2: r2, M1: m1 * G * r1, M2: m2 * G * r2 }; }
    function gleich(w){ return Math.abs(w.m1 * w.r1 - w.m2 * w.r2) < 1e-9; }
    var tl = 0;
    var uhr = Uhr(function(tt){
      var w = werte(), dt = Math.min(0.05, tt - tl); tl = tt;
      if (gleich(w)){ if (tt > 1.2){ lauf = fertig(w, 0); zeichnen(); return false; } zeichnen(); return; }
      var I = w.m1 * w.r1 * w.r1 + w.m2 * w.r2 * w.r2 + 40 * HALB * HALB / 3;   // Brett 40 kg
      var Mn = G * (w.m2 * w.r2 - w.m1 * w.r1) * Math.cos(th);                 // positiv: rechts nach unten
      om += Mn / I * dt; th += om * dt;
      if (Math.abs(th) >= TMAX){ th = Math.sign(th) * TMAX; om = 0; lauf = fertig(w, Math.sign(th)); zeichnen(); return false; }
      zeichnen();
    });
    function fertig(w, seite){ ende = seite; var l = { m1: w.m1, r1: w.r1, m2: w.m2, r2: w.r2, M1: w.M1, M2: w.M2, kippt: seite }; laeufe.push(l); return l; }
    aktionen(fig, [['start', '▶ Loslassen', function(){ uhr.stop(); th = 0; om = 0; tl = 0; ende = null; var w = werte(); if (WENIGER){ th = gleich(w) ? 0 : (w.M2 > w.M1 ? TMAX : -TMAX); lauf = fertig(w, Math.sign(th)); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Halten', function(){ uhr.stop(); th = 0; om = 0; ende = null; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); th = 0; om = 0; ende = null; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(x){ uhr.stop(); th = x; om = 0; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), c = Math.cos(th), s = Math.sin(th);
      B.anzeigen(); leeren(szene); leeren(dia);
      var boden = DY + HOCH * PX;
      el(szene, 'line', { x1: 4, y1: boden, x2: 296, y2: boden, 'class': 'boden' });
      el(szene, 'polygon', { points: DX + ',' + DY + ' ' + (DX - 14) + ',' + boden + ' ' + (DX + 14) + ',' + boden, 'class': 'lager' });
      function P(x, h){ return [DX + (x * c - h * s) * PX, DY + (x * s + h * c) * PX]; }   // x längs des Bretts (rechts +), h senkrecht (nach unten +)
      var a = P(-HALB, 0), b = P(HALB, 0);
      el(szene, 'line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], 'class': 'brett' });
      for (var x = -2; x <= 2.01; x += 0.5){ var q = P(x, 0.0), q2 = P(x, 0.09); el(szene, 'line', { x1: q[0], y1: q[1], x2: q2[0], y2: q2[1], 'class': 'tick' }); }
      if (ende === null && !uhr.laeuft()) el(szene, 'text', { x: 150, y: boden + 16, 'text-anchor': 'middle', 'class': 'bt-klein' }, 'gehalten — «Loslassen» gibt die Wippe frei');
      // Personen als Klötze, Grösse nach Masse
      [[-w.r1, w.m1, '1'], [w.r2, w.m2, '2']].forEach(function(p){
        var gr = 10 + p[1] * 0.32, m = P(p[0], -gr / PX / 2);
        el(szene, 'rect', { x: -gr / 2, y: -gr / 2, width: gr, height: gr, rx: 3, 'class': 'kiste', transform: 'translate(' + m[0].toFixed(1) + ',' + m[1].toFixed(1) + ') rotate(' + (th * 180 / Math.PI).toFixed(2) + ')' });
        el(szene, 'text', { x: m[0], y: m[1] + 4, 'text-anchor': 'middle', 'class': 'klotz-zahl' }, zahl(p[1]));
        var k = 0.065, F = p[1] * G;
        pfeil(szene, m[0], m[1] - gr / 2 - 4 - F * k, m[0], m[1] - gr / 2 - 4, 'pf-g', 7);
        marke(szene, m[0] + (p[0] < 0 ? -6 : 6), m[1] - gr / 2 - 8 - F * k * 0.6, 'F', p[2], 'pf-text pf-g', p[0] < 0 ? 'end' : 'start');
      });
      // Hebelarme waagrecht (wirksam): unter der Wippe, bei waagrechtem Brett
      if (Math.abs(th) < 1e-6){
        var y = DY + 26;
        el(szene, 'line', { x1: DX - w.r1 * PX, y1: y, x2: DX, y2: y, 'class': 'hebelarm' }); el(szene, 'text', { x: DX - w.r1 * PX / 2, y: y + 13, 'text-anchor': 'middle', 'class': 'pf-text pf-a' }, 'r₁ = ' + zahl(w.r1) + ' m');
        el(szene, 'line', { x1: DX, y1: y, x2: DX + w.r2 * PX, y2: y, 'class': 'hebelarm' }); el(szene, 'text', { x: DX + w.r2 * PX / 2, y: y + 13, 'text-anchor': 'middle', 'class': 'pf-text pf-a' }, 'r₂ = ' + zahl(w.r2) + ' m');
      }
      if (ende !== null) el(szene, 'text', { x: 150, y: 18, 'text-anchor': 'middle', 'class': 'bt-meldung' }, ende === 0 ? 'Gleichgewicht: Die Wippe bleibt waagrecht.' : 'Die Wippe kippt nach ' + (ende > 0 ? 'rechts.' : 'links.'));
      // Balken: Drehmomente links und rechts, 0 bis 1200 Nm
      var kx = 0.2;
      [[w.M1, 'M₁ links', 8], [w.M2, 'M₂ rechts', 34]].forEach(function(q){
        el(dia, 'rect', { x: 64, y: q[2], width: 240 * 0.98, height: 18, 'class': 'balken-leer' });
        el(dia, 'rect', { x: 64, y: q[2], width: q[0] * kx, height: 18, 'class': 'balken-m' });
        el(dia, 'text', { x: 58, y: q[2] + 13, 'text-anchor': 'end', 'class': 'bt-klein' }, q[1]);
        var lang = q[0] * kx > 150; el(dia, 'text', { x: lang ? 60 + q[0] * kx : 68 + q[0] * kx, y: q[2] + 13, 'text-anchor': lang ? 'end' : 'start', 'class': lang ? 'saeule-text' : 'bt-wert' }, sig(q[0]) + NB + 'Nm');
      });
      var z = '<span>' + v_('M') + '<sub>1</sub> = ' + v_('m') + '<sub>1</sub> · ' + v_('g') + ' · ' + v_('r') + '<sub>1</sub> = ' + zahl(w.m1) + NB + 'kg · 9.81' + NB + 'm/s² · ' + zahl(w.r1) + NB + 'm ' + ist(w.M1, sig(w.M1)) + sig(w.M1) + NB + 'Nm</span>';
      z += '<span>' + v_('M') + '<sub>2</sub> = ' + v_('m') + '<sub>2</sub> · ' + v_('g') + ' · ' + v_('r') + '<sub>2</sub> = ' + zahl(w.m2) + NB + 'kg · 9.81' + NB + 'm/s² · ' + zahl(w.r2) + NB + 'm ' + ist(w.M2, sig(w.M2)) + sig(w.M2) + NB + 'Nm</span>';
      z += '<span class="sim-notiz">Die Wippe ist symmetrisch: Ihr eigenes Gewicht greift im Drehpunkt an und hat keinen Hebelarm.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, m1, r1, m2, r2){ var l = s.lauf; return l && l.m1 === m1 && l.r1 === r1 && l.m2 === m2 && l.r2 === r2; }
    pruefen = Leiste(fig, [
      { text: 'Links sitzt ein Kind mit \\(36\\;\\text{kg}\\) bei \\(1.0\\;\\text{m}\\). Wo muss rechts ein Kind mit \\(24\\;\\text{kg}\\) sitzen, damit die Wippe beim Loslassen waagrecht bleibt? Notiere deine Rechnung, stelle ein und lass los.', ok: function(s){ return hat(s, 36, 1, 24, 1.5) && s.lauf.kippt === 0; },
        vergleich: '\\(m_1 \\cdot r_1 = m_2 \\cdot r_2\\), also \\(r_2 = \\dfrac{36\\;\\text{kg} \\cdot 1.0\\;\\text{m}}{24\\;\\text{kg}} = 1.5\\;\\text{m}\\). Das leichtere Kind sitzt weiter aussen; \\(g\\) kürzt sich.' },
      { text: 'Statt des Kindes setzt sich rechts ein Erwachsener mit \\(60\\;\\text{kg}\\) hin. Wo muss er sitzen? Notiere zuerst deine Rechnung.', ok: function(s){ return hat(s, 36, 1, 60, 0.6) && s.lauf.kippt === 0; },
        vergleich: '\\(r_2 = \\dfrac{36\\;\\text{kg} \\cdot 1.0\\;\\text{m}}{60\\;\\text{kg}} = 0.6\\;\\text{m}\\). Der Erwachsene ist schwerer als das linke Kind und sitzt darum näher an der Achse.' },
      { text: 'Bring die Wippe dazu, nach rechts zu kippen, obwohl rechts das leichtere Kind sitzt. Begründe, warum das geht.', ok: function(s){ var l = s.lauf; return l && l.m2 < l.m1 && l.kippt > 0; },
        vergleich: 'Es zählt nicht die Kraft allein, sondern Kraft mal Hebelarm. Sitzt das leichtere Kind weit genug aussen, ist sein Drehmoment \\(m_2 \\cdot g \\cdot r_2\\) grösser als \\(m_1 \\cdot g \\cdot r_1\\).' },
      { text: 'Finde ein Gleichgewicht, bei dem ein Kind genau dreimal so schwer ist wie das andere. Lass los und prüfe.', ok: function(s){ var l = s.lauf; return l && l.kippt === 0 && (l.m1 === 3 * l.m2 || l.m2 === 3 * l.m1); },
        vergleich: 'Das schwerere Kind sitzt dreimal so nah an der Achse: \\(3 \\cdot m \\cdot g \\cdot r = m \\cdot g \\cdot 3 \\cdot r\\). Zum Beispiel \\(45\\;\\text{kg}\\) bei \\(0.6\\;\\text{m}\\) und \\(15\\;\\text{kg}\\) bei \\(1.8\\;\\text{m}\\).' }
    ], sim);
    zeichnen();
  })();

  /* ---------- Kapitel 6: Auflagerkräfte einer Brücke ----------
     Nimmt Animation 6 der Themenseite (Balken auf zwei Stützen) als laufende Szene: Ein Wagen
     (Last F_L) fährt über eine Brücke der Stützweite L = 10 m und hält bei x. Auflagerkräfte
     (Grün) aus dem Momentengleichgewicht um A und dem Kräftegleichgewicht; das Eigengewicht F_E
     der Brücke greift in der Mitte an. Im Diagramm zeichnen F_A und F_B ihre Spur über x.
     Clipbeispiel: 50 kN bei 2 m und 7 m; Startwerte 60 kN, F_E = 0, Halt bei 5 m. */
  (function(){
    var fig = document.getElementById('sim6'); if (!fig) return;
    var svg = fig.querySelector('svg');
    var szene = g_(svg), dia = g_(svg, { transform: 'translate(0,192)' });
    var K = null;
    var B = Bedienung(fig, function(){ uhr.stop(); x = 0; zeichnen(); });
    var x = 0, lauf = null, laeufe = [], pruefen = function(){};
    var L = 10, AX = 36, PX = 23.2, BY = 104;                                 // Stützweite 10 m, 23.2 px je m
    function werte(){ var FL = B.wert('FL'), FE = B.wert('FE'), xh = B.wert('x'); return { FL: FL, FE: FE, xh: xh }; }
    function kn(v){ return zahl(+v.toFixed(2)); }                            // kN auf zwei Stellen: Beschriftung und Formelzeile gleich
    function lager(w, xx){ var FB = (w.FL * xx + w.FE * L / 2) / L; return { FB: FB, FA: w.FL + w.FE - FB }; }
    var uhr = Uhr(function(tt){
      var w = werte(); x = Math.min(tt * 2.5, w.xh); zeichnen();               // 2.5 m je Sekunde
      if (x >= w.xh){ var k = lager(w, w.xh); lauf = { FL: w.FL, FE: w.FE, x: w.xh, FA: k.FA, FB: k.FB }; laeufe.push(lauf); zeichnen(); return false; }
    });
    aktionen(fig, [['start', '▶ Fahren', function(){ var w = werte(); if (WENIGER){ x = w.xh; var k = lager(w, x); lauf = { FL: w.FL, FE: w.FE, x: x, FA: k.FA, FB: k.FB }; laeufe.push(lauf); zeichnen(); } else uhr.start(0); }],
                   ['zurueck', '↺ Zurück', function(){ uhr.stop(); x = 0; zeichnen(); }]]);
    var sim = {
      zustand: function(){ var w = werte(); w.lauf = lauf; w.laeufe = laeufe; return w; },
      zeichnen: function(){ zeichnen(); }, setze: function(o){ uhr.stop(); x = 0; B.setze(o); zeichnen(); },
      aufraeumen: function(){ lauf = null; laeufe = []; B.zuruecksetzen(); },
      zeige: function(xx){ uhr.stop(); x = xx; zeichnen(); }
    };
    fig.__sim = sim;
    function zeichnen(){
      var w = werte(), k = lager(w, x), s = 50 / (w.FL + w.FE);               // Gesamtlast 50 px
      B.anzeigen(); leeren(szene); leeren(dia);
      var sk = skala(w.FL + w.FE);
      K = Achsen(dia, { w: 300, h: 140, x0: -0.6, x1: 11, y0: sk.y0, y1: sk.y1, sx: 1, sy: sk.sy, xm: [2, 4, 6, 8, 10], ym: sk.ym, xname: 'x [m]', yname: 'F [kN]' });
      var X = function(m){ return AX + m * PX; };
      // Stützen, Brücke, Bemassung
      el(szene, 'rect', { x: X(0) - 6, y: BY, width: X(L) - X(0) + 12, height: 8, 'class': 'brett' });
      [[0, 'A'], [L, 'B']].forEach(function(q){ el(szene, 'polygon', { points: X(q[0]) + ',' + (BY + 8) + ' ' + (X(q[0]) - 10) + ',' + (BY + 26) + ' ' + (X(q[0]) + 10) + ',' + (BY + 26), 'class': 'lager' }); el(szene, 'text', { x: X(q[0]) + (q[0] ? 14 : -14), y: BY + 24, 'text-anchor': 'middle', 'class': 'bt-klein' }, q[1]); });
      el(szene, 'line', { x1: 4, y1: BY + 26, x2: 296, y2: BY + 26, 'class': 'boden' });
      // Wagen
      var wx = X(x);
      el(szene, 'rect', { x: wx - 16, y: BY - 18, width: 32, height: 14, rx: 3, 'class': 'kiste' });
      el(szene, 'circle', { cx: wx - 9, cy: BY - 3, r: 3.5, 'class': 'rad' }); el(szene, 'circle', { cx: wx + 9, cy: BY - 3, r: 3.5, 'class': 'rad' });
      pfeil(szene, wx, BY - 22 - w.FL * s, wx, BY - 20, 'pf-g', 7); marke(szene, wx + 6, BY - 24 - w.FL * s * 0.5, 'F', 'L', 'pf-text pf-g', 'start');
      if (w.FE > 0){ var mx = X(L / 2); pfeil(szene, mx, BY + 8, mx, BY + 8 + w.FE * s, 'pf-g duenn', 6); marke(szene, mx + 5, BY + 4 + w.FE * s, 'F', 'E', 'pf-text pf-g', 'start'); }
      if (k.FA > 0.5){ pfeil(szene, X(0), BY + 30 + k.FA * s, X(0), BY + 28, 'pf-n', 8); marke(szene, X(0) + 7, BY + 40 + k.FA * s * 0.5, 'F', 'A', 'pf-text pf-n', 'start'); }
      if (k.FB > 0.5){ pfeil(szene, X(L), BY + 30 + k.FB * s, X(L), BY + 28, 'pf-n', 8); marke(szene, X(L) - 7, BY + 40 + k.FB * s * 0.5, 'F', 'B', 'pf-text pf-n', 'end'); }
      el(szene, 'line', { x1: X(0), y1: 18, x2: wx, y2: 18, 'class': 'hebelarm' });
      el(szene, 'text', { x: (X(0) + wx) / 2, y: 13, 'text-anchor': 'middle', 'class': 'pf-text pf-a' }, x > 0.4 ? 'x = ' + zahl(+x.toFixed(1)) + ' m' : '');
      el(szene, 'text', { x: X(L) + 10, y: 13, 'text-anchor': 'end', 'class': 'bt-klein' }, 'L = 10 m');
      // Diagramm: Spur von F_A und F_B bis zur aktuellen Stelle, Gesamtlast gestrichelt
      K.kurve(function(){ return w.FL + w.FE; }, 'vorher', 0, L);
      if (x > 0){ K.kurve(function(q){ return lager(w, q).FA; }, 'kurve-fa', 0, x); K.kurve(function(q){ return lager(w, q).FB; }, 'kurve-fb', 0, x); }
      K.punkt(x, k.FA, 'p-fn'); K.punkt(x, k.FB, 'p-fn');
      var xs = zahl(+x.toFixed(2)) + NB + 'm; ';                              // wie in der Formelzeile
      etiketten(K, 300, 140, [
        { x: x, y: k.FA, f: function(q){ return lager(w, q).FA; }, cls: 'p-fn', text: '(' + xs + kn(k.FA) + NB + 'kN)' },
        { x: x, y: k.FB, f: function(q){ return lager(w, q).FB; }, cls: 'p-fn', text: '(' + xs + kn(k.FB) + NB + 'kN)' }], [110, 2, 190, 16]);
      stext(K.ebene, { x: 150, y: 12, 'text-anchor': 'middle', 'class': 'legende l-fn' }, '— F_A   - - F_B');   // Mitte: rechts oben reicht der Pfeil F_B hinein
      var z = '<span>Momente um A: ' + F_('B') + ' · ' + v_('L') + ' = ' + F_('L') + ' · ' + v_('x') + ' + ' + F_('E') + ' · ' + v_('L') + '/2' + '</span>';
      z += '<span>' + F_('B') + ' = (' + zahl(w.FL) + NB + 'kN · ' + zahl(+x.toFixed(2)) + NB + 'm + ' + zahl(w.FE) + NB + 'kN · 5' + NB + 'm) / 10' + NB + 'm ' + ist(k.FB, kn(k.FB)) + kn(k.FB) + NB + 'kN</span>';
      z += '<span>' + F_('A') + ' = ' + F_('L') + ' + ' + F_('E') + ' − ' + F_('B') + ' = ' + zahl(w.FL) + NB + 'kN + ' + zahl(w.FE) + NB + 'kN − ' + kn(k.FB) + NB + 'kN ' + ist(k.FA, kn(k.FA)) + kn(k.FA) + NB + 'kN</span>';
      z += '<span class="sim-notiz">Pfeillängen im Massstab der Gesamtlast.</span>';
      rolle(fig, 'formel').innerHTML = z;
      pruefen();
    }
    function hat(s, FL, FE, xx){ var l = s.lauf; return l && l.FL === FL && l.FE === FE && l.x === xx; }
    pruefen = Leiste(fig, [
      { text: 'Ein Wagen mit \\(F_L = 80\\;\\text{kN}\\) fährt auf eine Brücke ohne Eigengewicht und hält bei \\(x = 2.5\\;\\text{m}\\). Rechne zuerst \\(F_A\\) und \\(F_B\\), dann fahr hin und vergleiche.', ok: function(s){ return hat(s, 80, 0, 2.5); } },
      { text: 'Fahr den Wagen ganz über die Brücke (bis \\(10\\;\\text{m}\\)). Wie verlaufen \\(F_A\\) und \\(F_B\\) im Diagramm? Was bleibt dabei gleich? Notiere deine Antwort.', ok: function(s){ return s.lauf && s.lauf.x === 10; },
        vergleich: 'Beide verlaufen geradlinig: \\(F_A\\) nimmt ab, \\(F_B\\) nimmt im gleichen Mass zu. Ihre Summe bleibt die Gesamtlast (gestrichelt) — das verlangt \\(\\sum F_y = 0\\). Über der Stütze A trägt A alles, über B trägt B alles.' },
      { text: 'Ohne Eigengewicht: Wo muss der Wagen halten, damit Stütze B dreimal so viel trägt wie Stütze A? Begründe mit den Momenten.', ok: function(s){ return s.lauf && s.lauf.FE === 0 && s.lauf.x === 7.5; },
        vergleich: '\\(F_B = F_L \\cdot \\dfrac{x}{L}\\) und \\(F_A = F_L \\cdot \\dfrac{L - x}{L}\\). \\(F_B = 3 \\cdot F_A\\) heisst \\(x = 3 \\cdot (L - x)\\), also \\(x = 7.5\\;\\text{m}\\) — unabhängig von der Last.' },
      { text: 'Jetzt hat die Brücke ein Eigengewicht \\(F_E = 100\\;\\text{kN}\\) (in der Mitte). Ein Wagen mit \\(100\\;\\text{kN}\\) hält bei \\(4\\;\\text{m}\\). Wie gross ist \\(F_A\\)? Rechne, dann fahr hin.', ok: function(s){ return hat(s, 100, 100, 4); } },
      { text: 'Stütze B darf höchstens \\(120\\;\\text{kN}\\) tragen. Brücke \\(F_E = 60\\;\\text{kN}\\), Wagen \\(150\\;\\text{kN}\\): Wie weit darf der Wagen höchstens fahren? Notiere deine Rechnung, stelle ein und fahr.', ok: function(s){ return hat(s, 150, 60, 6); },
        vergleich: '\\(F_B = \\dfrac{F_L \\cdot x + F_E \\cdot \\tfrac{L}{2}}{L}\\): \\(120\\;\\text{kN} = \\dfrac{150\\;\\text{kN} \\cdot x + 60\\;\\text{kN} \\cdot 5\\;\\text{m}}{10\\;\\text{m}}\\) ergibt \\(x = 6\\;\\text{m}\\). Weiter rechts trägt B mehr als erlaubt.' }
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

    var TYPEN = {
      /* ----- Kapitel 1: Kraft als Vektor ----- */
      'komponenten': { felder: ['x'], muster: function(A){ return '<i>F</i><sub>' + A.art + '</sub> = {x} N'; },
        neu: function(){
          var F, p;
          do { F = zufall([40, 60, 75, 120, 180, 250, 320]); p = zufall([10, 20, 25, 35, 50, 65, 110, 140, 160, 200, 230, 250, 290, 320, 340]); }
          while ((F === 120 && p === 35) || F === p);   // Themenseite A1
          var art = Math.random() < 0.5 ? 'x' : 'y', x = art === 'x' ? F * Math.cos(grad(p)) : F * Math.sin(grad(p));
          return { art: art, x: x, F: F, p: p,
            text: 'Eine Kraft von \\(' + ein(F, 'N') + '\\) zeigt unter \\(\\varphi = ' + p + '^\\circ\\) zur positiven \\(x\\)-Achse. Wie gross ist ihre ' + (art === 'x' ? 'waagrechte Komponente \\(F_x\\)' : 'senkrechte Komponente \\(F_y\\)') + ', mit Vorzeichen?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          var tausch = A.art === 'x' ? A.F * Math.sin(grad(A.p)) : A.F * Math.cos(grad(A.p));
          if (nah(e.x, -A.x)) return 'Der Betrag stimmt, das Vorzeichen nicht. Zeigt die Kraft nach ' + (A.art === 'x' ? 'links oder rechts' : 'oben oder unten') + '?';
          if (nah(e.x, tausch) || nah(e.x, -tausch)) return A.art === 'x' ? 'Die waagrechte Komponente gehört zum Kosinus: \\(F_x = F \\cdot \\cos\\varphi\\).' : 'Die senkrechte Komponente gehört zum Sinus: \\(F_y = F \\cdot \\sin\\varphi\\).';
          var rad = A.art === 'x' ? A.F * Math.cos(A.p) : A.F * Math.sin(A.p);
          if (nah(e.x, rad, 0.01)) return 'Der Taschenrechner steht auf Bogenmass (RAD). Stelle ihn auf Grad (DEG).';
          return A.art === 'x' ? '\\(F_x = F \\cdot \\cos\\varphi\\), Winkel in Grad.' : '\\(F_y = F \\cdot \\sin\\varphi\\), Winkel in Grad.'; },
        fehler: function(A){ var t = A.art === 'x' ? A.F * Math.sin(grad(A.p)) : A.F * Math.cos(grad(A.p)); return [[{ x: String(-A.x) }, 'Vorzeichen'], [{ x: String(t) }, A.art === 'x' ? 'Kosinus' : 'Sinus'], [{ x: String(A.art === 'x' ? A.F * Math.cos(A.p) : A.F * Math.sin(A.p)) }, 'Bogenmass']]; },
        loesung: function(A){ return A.art === 'x' ? 'F_x = F \\cdot \\cos\\varphi = ' + ein(A.F, 'N') + ' \\cdot \\cos ' + A.p + '^\\circ ' + erg(A.x, 'N')
                                                   : 'F_y = F \\cdot \\sin\\varphi = ' + ein(A.F, 'N') + ' \\cdot \\sin ' + A.p + '^\\circ ' + erg(A.x, 'N'); } },
      'betrag': { felder: ['F'], muster: '<i>F</i> = {F} N',
        neu: function(){
          var a, b;
          do { a = zufall([30, 45, 60, 90, 120, 150, 200]) * zufall([1, -1]); b = zufall([20, 40, 50, 75, 110, 160]) * zufall([1, -1]); }
          while ((Math.abs(a) === 120 && Math.abs(b) === 50) || (Math.abs(a) === 30 && Math.abs(b) === 40) || (Math.abs(a) === 90 && Math.abs(b) === 40));   // Aufgabe 2a, Festhalten Kapitel 1 und 2
          return { F: Math.hypot(a, b), a: a, b: b,
            text: 'Eine Kraft hat die Komponenten \\(F_x = ' + ein(a, 'N') + '\\) und \\(F_y = ' + ein(b, 'N') + '\\). Wie gross ist ihr Betrag?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, Math.abs(A.a) + Math.abs(A.b)) || nah(e.F, A.a + A.b)) return 'Komponenten stehen senkrecht aufeinander und dürfen nicht einfach addiert werden. Pythagoras: \\(F = \\sqrt{F_x^2 + F_y^2}\\).';
          if (nah(e.F, A.a * A.a + A.b * A.b)) return 'Noch die Wurzel ziehen.';
          if (e.F < 0) return 'Ein Betrag ist nie negativ.';
          return '\\(F = \\sqrt{F_x^2 + F_y^2}\\) — die Vorzeichen fallen beim Quadrieren weg.'; },
        fehler: function(A){ return [[{ F: String(Math.abs(A.a) + Math.abs(A.b)) }, 'addiert'], [{ F: String(A.a * A.a + A.b * A.b) }, 'Wurzel']]; },
        loesung: function(A){ return 'F = \\sqrt{F_x^2 + F_y^2} = \\sqrt{(' + ein(A.a, 'N') + ')^2 + (' + ein(A.b, 'N') + ')^2} ' + erg(A.F, 'N'); } },
      'winkel': { felder: ['p'], muster: '<i>φ</i> = {p} °',
        neu: function(){
          var a, b;
          do { a = zufall([20, 35, 50, 80, 120, 150]) * zufall([1, -1]); b = zufall([15, 30, 45, 60, 90, 100]) * zufall([1, -1]); }
          while (Math.abs(a) === Math.abs(b) || (Math.abs(a) === 80 && Math.abs(b) === 60));   // Clipbeispiel
          var p = (Math.atan2(b, a) * 180 / Math.PI + 360) % 360;
          return { p: p, a: a, b: b,
            text: 'Eine Kraft hat die Komponenten \\(F_x = ' + ein(a, 'N') + '\\) und \\(F_y = ' + ein(b, 'N') + '\\). Unter welchem Winkel \\(\\varphi\\) zur positiven \\(x\\)-Achse zeigt sie (zwischen \\(0^\\circ\\) und \\(360^\\circ\\))? Mach zuerst eine Skizze.' }; },
        pruefen: function(A, e){
          if (Math.abs(e.p - A.p) <= 0.5) return null;   // auf ein halbes Grad
          var roh = Math.atan(A.b / A.a) * 180 / Math.PI, g = Math.abs(roh);
          function trifft(l){ return l.some(function(w){ return Math.abs(w - A.p) > 0.5 && Math.abs(e.p - w) <= 0.5; }); }
          // Bezugswinkel richtig, nur der Quadrant falsch
          if (trifft([roh, roh + 180, roh + 360, g, 180 - g, 180 + g, 360 - g, -g])){
            if (A.a > 0 && A.b > 0) return 'Die Kraft zeigt nach rechts oben (beide Komponenten positiv): Der Winkel des Taschenrechners stimmt hier schon.';
            return 'Der Taschenrechner kennt nur Winkel zwischen \\(-90^\\circ\\) und \\(90^\\circ\\). Schau in der Skizze, in welche Richtung die Kraft zeigt: ' + (A.a < 0 ? 'nach links, also \\(180^\\circ\\) zum Rechnerwinkel dazuzählen.' : 'nach rechts unten, also \\(360^\\circ\\) zum Rechnerwinkel dazuzählen.');
          }
          // Katheten vertauscht: Bezugswinkel 90° − g, in irgendeinem Quadranten
          if (trifft([90 - g, 90 + g, 270 - g, 270 + g])) return '\\(\\tan\\varphi = \\dfrac{F_y}{F_x}\\): Gegenkathete durch Ankathete, und dann die Richtung aus der Skizze.';
          return '\\(\\tan\\varphi = \\dfrac{F_y}{F_x}\\), dann den Winkel nach der Skizze in den richtigen Quadranten legen.'; },
        fehler: function(A){ var roh = Math.atan(A.b / A.a) * 180 / Math.PI, g = Math.abs(roh);
          return (A.a > 0 && A.b > 0) ? [[{ p: String(90 - g) }, 'Gegenkathete'], [{ p: String(roh + 180) }, 'rechts oben']] : [[{ p: String(roh) }, 'Taschenrechner'], [{ p: String(90 - g) }, 'Gegenkathete']]; },
        loesung: function(A){ var roh = Math.atan(A.b / A.a) * 180 / Math.PI;
          return '\\arctan\\dfrac{' + ein(A.b, 'N') + '}{' + ein(A.a, 'N') + '} ' + erg(roh, '°').replace('\\;\\text{°}', '^\\circ') + (A.a < 0 ? ',\\quad \\varphi = ' + tz(+roh.toPrecision(4)) + '^\\circ + 180^\\circ ' : (A.b < 0 ? ',\\quad \\varphi = ' + tz(+roh.toPrecision(4)) + '^\\circ + 360^\\circ ' : ',\\quad \\varphi ')) + erg(A.p, '°').replace('\\;\\text{°}', '^\\circ'); } },

      /* ----- Kapitel 2: Resultierende Kraft ----- */
      'res-recht': { felder: ['F'], muster: '<i>F</i><sub>res</sub> = {F} N',
        neu: function(){
          var a, b;
          do { a = zufall([25, 40, 70, 90, 140, 210, 300]); b = zufall([20, 35, 50, 80, 110, 160, 240]); } while (a === b);
          var ctx = zufall([['Zwei Kinder ziehen an einem Schlitten', 'nach vorn', 'zur Seite'], ['Zwei Seile halten einen Ballon', 'waagrecht', 'senkrecht nach unten'], ['Strömung und Motor wirken auf ein Boot', 'quer zum Fluss', 'flussabwärts']]);
          return { F: Math.hypot(a, b), a: a, b: b,
            text: ctx[0] + ': \\(' + ein(a, 'N') + '\\) ' + ctx[1] + ' und \\(' + ein(b, 'N') + '\\) ' + ctx[2] + ', im rechten Winkel zueinander. Wie gross ist die Resultierende?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.a + A.b)) return 'Addieren darf man nur gleichgerichtete Kräfte. Hier stehen sie senkrecht: Pythagoras.';
          if (nah(e.F, Math.abs(A.a - A.b))) return 'Subtrahieren darf man nur entgegengesetzte Kräfte. Hier stehen sie senkrecht: Pythagoras.';
          if (nah(e.F, A.a * A.a + A.b * A.b)) return 'Noch die Wurzel ziehen.';
          return 'Die Pfeile bilden mit der Resultierenden ein rechtwinkliges Dreieck: \\(F_\\text{res} = \\sqrt{F_1^2 + F_2^2}\\).'; },
        fehler: function(A){ return [[{ F: String(A.a + A.b) }, 'gleichgerichtete'], [{ F: String(A.a * A.a + A.b * A.b) }, 'Wurzel']]; },
        loesung: function(A){ return 'F_\\text{res} = \\sqrt{F_1^2 + F_2^2} = \\sqrt{(' + ein(A.a, 'N') + ')^2 + (' + ein(A.b, 'N') + ')^2} ' + erg(A.F, 'N'); } },
      'res-zwei': { felder: ['F'], muster: '<i>F</i><sub>res</sub> = {F} N',
        neu: function(){
          var a, b, g;
          var Rx, Ry;
          do { a = zufall([40, 60, 80, 100, 150]); b = zufall([30, 50, 70, 120]); g = zufall([30, 50, 60, 120, 140]); Rx = a + b * Math.cos(grad(g)); Ry = b * Math.sin(grad(g)); }
          while (a === b || !verschieden([Math.hypot(Rx, Ry), a + b, Math.hypot(a, b), Math.hypot(a - b * Math.cos(grad(g)), Ry), Rx, Ry]));
          return { F: Math.hypot(Rx, Ry), a: a, b: b, g: g, Rx: Rx, Ry: Ry,
            text: 'Am selben Punkt greifen \\(F_1 = ' + ein(a, 'N') + '\\) in Richtung \\(0^\\circ\\) und \\(F_2 = ' + ein(b, 'N') + '\\) in Richtung \\(' + g + '^\\circ\\) an. Wie gross ist die Resultierende? Rechne über die Komponenten.' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.a + A.b)) return 'Die Beträge addieren geht nur bei gleicher Richtung. Zerlege \\(F_2\\) in Komponenten.';
          if (nah(e.F, Math.hypot(A.a, A.b))) return 'Pythagoras mit den Beträgen gilt nur im rechten Winkel. Erst die Komponenten addieren: \\(F_{\\text{res},x} = F_1 + F_2 \\cdot \\cos\\varphi_2\\).';
          if (nah(e.F, Math.hypot(A.a - A.b * Math.cos(grad(A.g)), A.Ry))) return 'Vorzeichen prüfen: \\(F_{\\text{res},x} = F_1 + F_2 \\cdot \\cos\\varphi_2\\), der Kosinus bringt sein Vorzeichen selbst mit.';
          if (nah(e.F, A.Rx) || nah(e.F, A.Ry)) return 'Das ist nur eine Komponente der Resultierenden. Betrag: \\(\\sqrt{F_{\\text{res},x}^2 + F_{\\text{res},y}^2}\\).';
          return '\\(F_{\\text{res},x} = F_1 + F_2 \\cdot \\cos\\varphi_2\\), \\(F_{\\text{res},y} = F_2 \\cdot \\sin\\varphi_2\\), dann Pythagoras.'; },
        fehler: function(A){ return [[{ F: String(A.a + A.b) }, 'Beträge'], [{ F: String(Math.hypot(A.a, A.b)) }, 'rechten Winkel'], [{ F: String(A.Rx) }, 'Komponente']]; },
        loesung: function(A){ return 'F_{\\text{res},x} = ' + ein(A.a, 'N') + ' + ' + ein(A.b, 'N') + ' \\cdot \\cos ' + A.g + '^\\circ ' + erg(A.Rx, 'N') + ',\\quad F_{\\text{res},y} = ' + ein(A.b, 'N') + ' \\cdot \\sin ' + A.g + '^\\circ ' + erg(A.Ry, 'N') + ',\\quad F_\\text{res} = \\sqrt{F_{\\text{res},x}^2 + F_{\\text{res},y}^2} ' + erg(A.F, 'N'); } },
      'seil': { felder: ['S'], muster: '<i>F</i><sub>S</sub> = {S} N',
        neu: function(){
          var m, a;
          m = zufall([2, 4, 5, 12, 15, 25, 40]); a = zufall([10, 15, 20, 25, 35, 40, 50, 55, 70]);
          return { S: m * G / (2 * Math.sin(grad(a))), m: m, a: a,
            text: 'Eine Last mit \\(m = ' + ein(m, 'kg') + '\\) hängt in der Mitte an zwei gleich langen Seilen; beide steigen unter \\(\\alpha = ' + a + '^\\circ\\) zur Waagrechten an. Wie gross ist die Kraft in jedem Seil?' }; },
        pruefen: function(A, e){
          if (nah(e.S, A.S)) return null;
          var FG = A.m * G;
          if (nah(e.S, FG / 2)) return 'Die Hälfte der Gewichtskraft tragen die Seile nur senkrecht. Hier trägt nur der senkrechte Anteil \\(F_S \\cdot \\sin\\alpha\\).';
          if (nah(e.S, FG / (2 * Math.cos(grad(A.a))))) return 'Der Winkel liegt zur Waagrechten: Die senkrechte Komponente ist \\(F_S \\cdot \\sin\\alpha\\), nicht \\(\\cos\\alpha\\).';
          if (nah(e.S, FG / Math.sin(grad(A.a)))) return 'Zwei Seile teilen sich die Last: \\(2 \\cdot F_S \\cdot \\sin\\alpha = F_G\\).';
          if (nah(e.S, A.m / (2 * Math.sin(grad(A.a))))) return 'Kraft in Newton: zuerst \\(F_G = m \\cdot g\\).';
          return 'Senkrecht im Gleichgewicht: \\(2 \\cdot F_S \\cdot \\sin\\alpha = m \\cdot g\\).'; },
        fehler: function(A){ var FG = A.m * G; return [[{ S: String(FG / 2) }, 'Hälfte'], [{ S: String(FG / (2 * Math.cos(grad(A.a)))) }, 'sin'], [{ S: String(FG / Math.sin(grad(A.a))) }, 'Zwei Seile'], [{ S: String(A.m / (2 * Math.sin(grad(A.a)))) }, 'Newton']]; },
        loesung: function(A){ return '2 \\cdot F_S \\cdot \\sin\\alpha = m \\cdot g,\\quad F_S = \\dfrac{' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2}{2 \\cdot \\sin ' + A.a + '^\\circ} ' + erg(A.S, 'N'); } },

      /* ----- Kapitel 3: Kräfte am ruhenden Körper ----- */
      'zerlegen': { felder: ['x'], muster: function(A){ return '<i>F</i><sub>' + A.art + '</sub> = {x} N'; },
        neu: function(){
          var m, a;
          m = zufall([4, 8, 15, 35, 60, 120, 250]); a = zufall([8, 12, 18, 25, 30, 35, 50]);
          var art = Math.random() < 0.5 ? 'H' : 'N';
          return { art: art, x: m * G * (art === 'H' ? Math.sin(grad(a)) : Math.cos(grad(a))), m: m, a: a,
            text: 'Ein Körper mit \\(m = ' + ein(m, 'kg') + '\\) liegt auf einer schiefen Ebene mit \\(\\alpha = ' + a + '^\\circ\\). Wie gross ist ' + (art === 'H' ? 'die Hangabtriebskraft \\(F_H\\)' : 'die Normalkraft \\(F_N\\)') + '?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          var FG = A.m * G, tausch = FG * (A.art === 'H' ? Math.cos(grad(A.a)) : Math.sin(grad(A.a)));
          if (nah(e.x, tausch)) return A.art === 'H' ? 'Die Hangabtriebskraft ist die Komponente längs der Ebene, gegenüber dem Winkel: \\(F_H = F_G \\cdot \\sin\\alpha\\).' : 'Die Normalkraft gleicht die Komponente senkrecht zur Ebene aus: \\(F_N = F_G \\cdot \\cos\\alpha\\).';
          if (nah(e.x, FG)) return A.art === 'N' ? 'Nur auf der waagrechten Ebene ist \\(F_N = F_G\\). Auf der schiefen ist es die Komponente senkrecht zur Ebene.' : 'Das ist die ganze Gewichtskraft. Gesucht ist ihr Anteil längs der Ebene.';
          if (nah(e.x, A.x / G)) return 'Kraft in Newton: \\(F_G = m \\cdot g\\).';
          return A.art === 'H' ? '\\(F_H = m \\cdot g \\cdot \\sin\\alpha\\).' : '\\(F_N = m \\cdot g \\cdot \\cos\\alpha\\).'; },
        fehler: function(A){ var FG = A.m * G, t = FG * (A.art === 'H' ? Math.cos(grad(A.a)) : Math.sin(grad(A.a))); return [[{ x: String(t) }, A.art === 'H' ? 'gegenüber' : 'senkrecht'], [{ x: String(FG) }, A.art === 'N' ? 'waagrechten' : 'ganze'], [{ x: String(A.x / G) }, 'Newton']]; },
        loesung: function(A){ return A.art === 'H' ? 'F_H = m \\cdot g \\cdot \\sin\\alpha = ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot \\sin ' + A.a + '^\\circ ' + erg(A.x, 'N')
                                                   : 'F_N = m \\cdot g \\cdot \\cos\\alpha = ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 \\cdot \\cos ' + A.a + '^\\circ ' + erg(A.x, 'N'); } },
      'grenzwinkel': { felder: ['x'], muster: function(A){ return A.art === 'a' ? '<i>α</i> = {x} °' : '<i>μ</i><sub>H</sub> = {x}'; },
        neu: function(){
          if (Math.random() < 0.5){
            var st = zufall([['Holz auf Holz', 0.45], ['Gummi auf nassem Asphalt', 0.55], ['Gummi auf Beton', 0.8], ['Gummi auf rauem Fels', 0.9]]);   // nicht 0.25, 0.35, 0.4, 0.5, 0.6, 0.65, 0.7: Kontrollfrage, Gesamttest, Aufgabe 3c, Themenseite, Clip, Leiste; nicht unter 0.3: dort liegt arcsin zu nah an arctan
            return { art: 'a', x: Math.atan(st[1]) * 180 / Math.PI, mu: st[1],
              text: 'Haftreibungszahl für ' + st[0] + ': \\(\\mu_H = ' + tz(st[1]) + '\\). Bis zu welchem Neigungswinkel bleibt ein Körper darauf von selbst liegen?' };
          }
          var a = zufall([10, 18, 24, 28, 36, 38, 42]);   // nicht 12, 14, 22, 31, 33, 35: Aufgabe 3b, Kontrollfrage, Aufgabe 3c, Themenseite, Clip, Leiste
          return { art: 'm', x: Math.tan(grad(a)), a: a,
            text: 'Ein Klotz beginnt auf einer schiefen Ebene bei \\(\\alpha = ' + a + '^\\circ\\) gerade zu rutschen. Wie gross ist die Haftreibungszahl \\(\\mu_H\\)?' }; },
        pruefen: function(A, e){
          if (A.art === 'a' ? Math.abs(e.x - A.x) <= 0.5 : nah(e.x, A.x)) return null;   // Winkel auf ein halbes Grad
          if (A.art === 'a'){
            if (nah(e.x, Math.asin(A.mu) * 180 / Math.PI) || nah(e.x, Math.acos(A.mu) * 180 / Math.PI)) return 'Grenze: \\(m \\cdot g \\cdot \\sin\\alpha = \\mu_H \\cdot m \\cdot g \\cdot \\cos\\alpha\\), also \\(\\tan\\alpha = \\mu_H\\). Mit \\(\\tan^{-1}\\).';
            if (nah(e.x, Math.atan(A.mu))) return 'Das ist Bogenmass. Taschenrechner auf Grad (DEG).';
            return '\\(\\tan\\alpha = \\mu_H\\), also \\(\\alpha = \\arctan\\mu_H\\).';
          }
          if (nah(e.x, Math.sin(grad(A.a))) || nah(e.x, Math.cos(grad(A.a)))) return 'An der Grenze ist \\(F_H = \\mu_H \\cdot F_N\\): \\(\\mu_H = \\dfrac{\\sin\\alpha}{\\cos\\alpha} = \\tan\\alpha\\).';
          if (nah(e.x, Math.tan(A.a), 0.01)) return 'Der Taschenrechner steht auf Bogenmass (RAD). Stelle ihn auf Grad (DEG).';
          return 'An der Grenze gilt \\(\\mu_H = \\tan\\alpha\\).'; },
        fehler: function(A){ return A.art === 'a' ? [[{ x: String(Math.asin(A.mu) * 180 / Math.PI) }, 'tan'], [{ x: String(Math.atan(A.mu)) }, 'Bogenmass']] : [[{ x: String(Math.sin(grad(A.a))) }, 'Grenze'], [{ x: String(Math.tan(A.a)) }, 'Bogenmass']]; },
        loesung: function(A){ return A.art === 'a' ? '\\tan\\alpha = \\mu_H,\\quad \\alpha = \\arctan ' + tz(A.mu) + ' ' + erg(A.x, '°').replace('\\;\\text{°}', '^\\circ')
                                                   : '\\mu_H = \\tan\\alpha = \\tan ' + A.a + '^\\circ ' + erg(A.x, '').replace('\\;\\text{}', ''); } },
      'haftgrenze': { felder: ['x'], muster: '<i>F</i><sub>R</sub> = {x} N',
        neu: function(){
          var m, mu;
          m = zufall([6, 15, 30, 45, 70, 120]); mu = zufall([0.25, 0.35, 0.45, 0.6, 0.75]);
          var max = mu * m * G;
          if (Math.random() < 0.5) return { art: 'max', x: max, m: m, mu: mu,
            text: 'Eine Kiste mit \\(m = ' + ein(m, 'kg') + '\\) steht auf waagrechtem Boden, \\(\\mu_H = ' + tz(mu) + '\\). Wie gross ist die Haftreibung höchstens — mit welcher waagrechten Kraft kann man schieben, bevor sie rutscht?' };
          var F = +(max * zufall([0.3, 0.5, 0.7])).toPrecision(2);
          return { art: 'ist', x: F, F: F, m: m, mu: mu, max: max,
            text: 'Eine Kiste mit \\(m = ' + ein(m, 'kg') + '\\) steht auf waagrechtem Boden, \\(\\mu_H = ' + tz(mu) + '\\). Du schiebst waagrecht mit \\(' + ein(F, 'N') + '\\), sie bewegt sich nicht. Wie gross ist die Reibungskraft?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'ist'){
            if (nah(e.x, A.max)) return 'Das ist der Höchstwert. Die Haftreibung ist nur so gross wie nötig: Die Kiste ruht, also gleicht sie genau deine Kraft aus.';
            return 'Die Kiste ruht: \\(\\sum F_x = 0\\). Die Reibung ist gleich gross wie die Schubkraft.';
          }
          if (nah(e.x, A.mu * A.m)) return 'Mit der Normalkraft in Newton rechnen: \\(F_N = m \\cdot g\\).';
          if (nah(e.x, A.m * G)) return 'Das ist die Normalkraft. Die grösste Haftreibung ist \\(\\mu_H \\cdot F_N\\).';
          return '\\(F_{R,\\text{max}} = \\mu_H \\cdot F_N = \\mu_H \\cdot m \\cdot g\\).'; },
        fehler: function(A){ return A.art === 'ist' ? [[{ x: String(A.max) }, 'Höchstwert']] : [[{ x: String(A.mu * A.m) }, 'Newton'], [{ x: String(A.m * G) }, 'Normalkraft']]; },
        loesung: function(A){ return A.art === 'ist' ? '\\sum F_x = 0:\\quad F_R = F = ' + ein(A.F, 'N') + '\\;(\\text{kleiner als } \\mu_H \\cdot m \\cdot g ' + erg(A.max, 'N') + ')'
                                                     : 'F_{R,\\text{max}} = \\mu_H \\cdot m \\cdot g = ' + tz(A.mu) + ' \\cdot ' + ein(A.m, 'kg') + ' \\cdot 9.81\\;\\text{m/s}^2 ' + erg(A.x, 'N'); } },

      /* ----- Kapitel 4: Drehmoment ----- */
      'moment': { felder: ['M'], muster: '<i>M</i> = {M} Nm',
        neu: function(){
          var F, l, a;
          do { F = zufall([15, 35, 80, 150, 220, 360]); l = zufall([12, 20, 35, 45, 60, 80]); a = zufall([90, 90, 30, 50, 70, 120, 150]); }
          while (F === 150 && l === 20 && a === 90);   // Festhalten Kapitel 4
          return { M: F * l / 100 * Math.sin(grad(a)), F: F, l: l, a: a,
            text: 'Eine Kraft \\(F = ' + ein(F, 'N') + '\\) greift \\(' + ein(l, 'cm') + '\\) von der Drehachse an einem Hebel an; der Winkel zwischen Hebel und Kraft ist \\(\\alpha = ' + a + '^\\circ\\). Wie gross ist das Drehmoment?' }; },
        pruefen: function(A, e){
          if (nah(e.M, A.M)) return null;
          if (nah(e.M, A.M * 100)) return 'Den Hebel in Meter umrechnen: \\(' + ein(A.l, 'cm') + ' = ' + ein(A.l / 100, 'm') + '\\).';
          if (A.a !== 90 && nah(e.M, A.F * A.l / 100)) return 'Nur der Anteil senkrecht zum Hebel dreht: \\(M = F \\cdot l \\cdot \\sin\\alpha\\).';
          if (A.a !== 90 && nah(Math.abs(e.M), Math.abs(A.F * A.l / 100 * Math.cos(grad(A.a))))) return '\\(\\alpha\\) ist der Winkel zwischen Hebel und Kraft: \\(\\sin\\alpha\\), nicht \\(\\cos\\alpha\\).';
          if (nah(e.M, A.F / (A.l / 100))) return 'Drehmoment ist Kraft <em>mal</em> Hebelarm.';
          return '\\(M = F \\cdot l \\cdot \\sin\\alpha\\), \\(l\\) in Meter.'; },
        fehler: function(A){ var l = [[{ M: String(A.M * 100) }, 'Meter'], [{ M: String(A.F / (A.l / 100)) }, 'mal']]; if (A.a !== 90) l.push([{ M: String(A.F * A.l / 100) }, 'senkrecht'], [{ M: String(A.F * A.l / 100 * Math.cos(grad(A.a))) }, 'cos']); return l; },
        loesung: function(A){ return 'M = F \\cdot l \\cdot \\sin\\alpha = ' + ein(A.F, 'N') + ' \\cdot ' + ein(A.l / 100, 'm') + ' \\cdot \\sin ' + A.a + '^\\circ ' + erg(A.M, 'Nm'); } },
      'kraft': { felder: ['x'], muster: function(A){ return A.art === 'F' ? '<i>F</i> = {x} N' : '<i>r</i> = {x} m'; },
        neu: function(){
          // Werte je Gegenstand (plausibel: Handkraft bis rund 450 N, Hebel passend zum Werkzeug)
          var ctx = zufall([
            { was: 'Eine Radmutter', tun: 'zum Lösen', am: 'am Radkreuz', M: [90, 120, 140], r: [0.3, 0.35, 0.4], F: [250, 300, 350] },
            { was: 'Eine Schraube am Velo', tun: 'zum Lösen', am: 'am Schraubenschlüssel', M: [5, 8, 12], r: [0.1, 0.12, 0.15], F: [40, 60, 80] },
            { was: 'Das Handrad eines Ventils', tun: 'zum Öffnen', am: 'am Rand des Handrads', M: [8, 12, 20], r: [0.1, 0.15, 0.2], F: [60, 80, 120] }]);
          var M, r, F;
          do { M = zufall(ctx.M); r = zufall(ctx.r); F = zufall(ctx.F); } while (F === 10 * M);   // sonst r · 100 = F / M: zwei Fehler, eine Zahl
          if (Math.random() < 0.5) return { art: 'F', x: M / r, M: M, r: r,
            text: ctx.was + ' braucht ' + ctx.tun + ' \\(M = ' + ein(M, 'Nm') + '\\). Man zieht senkrecht ' + ctx.am + ', \\(' + ein(r, 'm') + '\\) von der Drehachse. Welche Kraft braucht es mindestens?' };
          return { art: 'r', x: M / F, M: M, F: F,
            text: ctx.was + ' braucht ' + ctx.tun + ' \\(M = ' + ein(M, 'Nm') + '\\). Du ziehst senkrecht ' + ctx.am + ' mit \\(' + ein(F, 'N') + '\\). Wie weit von der Drehachse musst du mindestens greifen?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'F' && nah(e.x, A.M * A.r)) return 'Umstellen: \\(F = \\dfrac{M}{r}\\), nicht mal.';
          if (A.art === 'r' && nah(e.x, A.M * A.F)) return 'Umstellen: \\(r = \\dfrac{M}{F}\\), nicht mal.';
          if (A.art === 'r' && nah(e.x, A.x * 100)) return 'Gefragt ist der Abstand in Meter.';
          if (A.art === 'r' && nah(e.x, A.F / A.M)) return 'Umgekehrt: \\(r = \\dfrac{M}{F}\\).';
          return A.art === 'F' ? '\\(M = F \\cdot r\\), also \\(F = \\dfrac{M}{r}\\).' : '\\(M = F \\cdot r\\), also \\(r = \\dfrac{M}{F}\\).'; },
        fehler: function(A){ return A.art === 'F' ? [[{ x: String(A.M * A.r) }, 'Umstellen']] : [[{ x: String(A.M * A.F) }, 'Umstellen'], [{ x: String(A.x * 100) }, 'Meter'], [{ x: String(A.F / A.M) }, 'Umgekehrt']]; },
        loesung: function(A){ return A.art === 'F' ? 'F = \\dfrac{M}{r} = \\dfrac{' + ein(A.M, 'Nm') + '}{' + ein(A.r, 'm') + '} ' + erg(A.x, 'N') : 'r = \\dfrac{M}{F} = \\dfrac{' + ein(A.M, 'Nm') + '}{' + ein(A.F, 'N') + '} ' + erg(A.x, 'm'); } },
      'losbrechen': { felder: ['F'], muster: '<i>F</i> = {F} N',
        neu: function(){
          var M, l, a;
          M = zufall([20, 35, 50, 80]); l = zufall([0.25, 0.3, 0.4]); a = zufall([40, 55, 65, 75]);   // höchstens rund 500 N
          return { F: M / (l * Math.sin(grad(a))), M: M, l: l, a: a,
            text: 'Eine Schraube löst sich bei \\(M = ' + ein(M, 'Nm') + '\\). Der Schlüssel ist \\(' + ein(l, 'm') + '\\) lang, man kann nur unter \\(\\alpha = ' + a + '^\\circ\\) zum Schlüssel ziehen. Welche Kraft braucht es?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.M / A.l)) return 'Schräg gezogen ist der wirksame Hebelarm nur \\(r = l \\cdot \\sin\\alpha\\).';
          if (nah(e.F, A.M / (A.l * Math.cos(grad(A.a))))) return '\\(\\alpha\\) ist der Winkel zwischen Schlüssel und Kraft: \\(r = l \\cdot \\sin\\alpha\\).';
          if (nah(e.F, A.M * A.l * Math.sin(grad(A.a)))) return 'Umstellen: \\(F = \\dfrac{M}{l \\cdot \\sin\\alpha}\\).';
          return '\\(F = \\dfrac{M}{l \\cdot \\sin\\alpha}\\).'; },
        fehler: function(A){ return [[{ F: String(A.M / A.l) }, 'Schräg'], [{ F: String(A.M / (A.l * Math.cos(grad(A.a)))) }, 'Winkel'], [{ F: String(A.M * A.l * Math.sin(grad(A.a))) }, 'Umstellen']]; },
        loesung: function(A){ return 'F = \\dfrac{M}{l \\cdot \\sin\\alpha} = \\dfrac{' + ein(A.M, 'Nm') + '}{' + ein(A.l, 'm') + ' \\cdot \\sin ' + A.a + '^\\circ} ' + erg(A.F, 'N'); } },

      /* ----- Kapitel 5: Hebelgesetz ----- */
      'wippe': { felder: ['x'], muster: function(A){ return A.art === 'r' ? '<i>r</i><sub>2</sub> = {x} m' : '<i>m</i><sub>2</sub> = {x} kg'; },
        neu: function(){
          var m1, r1, m2, r2;
          do { m1 = zufall([18, 22, 27, 32, 45, 54]); r1 = zufall([0.8, 1.2, 1.4, 1.6, 1.8]); m2 = zufall([20, 30, 36, 40, 48]); r2 = zufall([0.9, 1.1, 1.5, 2]); }
          while (m1 === m2 || (m1 * r1) / m2 > 2.2 || (m1 * r1) / r2 > 90 || (m1 * r1) / r2 < 15);   // gesuchte Masse 15 bis 90 kg
          if (Math.random() < 0.5) return { art: 'r', x: m1 * r1 / m2, m1: m1, r1: r1, m2: m2,
            text: 'Auf einer Wippe sitzt links ein Kind mit \\(' + ein(m1, 'kg') + '\\), \\(' + ein(r1, 'm') + '\\) von der Drehachse. Wie weit von der Achse muss rechts ein Kind mit \\(' + ein(m2, 'kg') + '\\) sitzen, damit Gleichgewicht herrscht?' };
          return { art: 'm', x: m1 * r1 / r2, m1: m1, r1: r1, r2: r2,
            text: 'Auf einer Wippe sitzt links ein Kind mit \\(' + ein(m1, 'kg') + '\\), \\(' + ein(r1, 'm') + '\\) von der Drehachse. Welche Masse muss rechts im Abstand \\(' + ein(r2, 'm') + '\\) sitzen, damit Gleichgewicht herrscht?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (A.art === 'r' && nah(e.x, A.m2 * A.r1 / A.m1)) return 'Umgekehrt: Das leichtere Kind muss weiter aussen sitzen. \\(m_1 \\cdot r_1 = m_2 \\cdot r_2\\).';
          if (A.art === 'm' && nah(e.x, A.m1 * A.r2 / A.r1)) return 'Umgekehrt: Weiter aussen braucht es weniger Masse. \\(m_1 \\cdot r_1 = m_2 \\cdot r_2\\).';
          if (nah(e.x, A.x * G) || nah(e.x, A.x / G)) return '\\(g\\) steht auf beiden Seiten und kürzt sich: \\(m_1 \\cdot g \\cdot r_1 = m_2 \\cdot g \\cdot r_2\\).';
          return 'Gleichgewicht der Drehmomente: \\(m_1 \\cdot g \\cdot r_1 = m_2 \\cdot g \\cdot r_2\\).'; },
        fehler: function(A){ return A.art === 'r' ? [[{ x: String(A.m2 * A.r1 / A.m1) }, 'Umgekehrt'], [{ x: String(A.x * G) }, 'kürzt']] : [[{ x: String(A.m1 * A.r2 / A.r1) }, 'Umgekehrt'], [{ x: String(A.x * G) }, 'kürzt']]; },
        loesung: function(A){ return A.art === 'r' ? 'm_1 \\cdot g \\cdot r_1 = m_2 \\cdot g \\cdot r_2,\\quad r_2 = \\dfrac{m_1 \\cdot r_1}{m_2} = \\dfrac{' + ein(A.m1, 'kg') + ' \\cdot ' + ein(A.r1, 'm') + '}{' + ein(A.m2, 'kg') + '} ' + erg(A.x, 'm')
                                                   : 'm_1 \\cdot g \\cdot r_1 = m_2 \\cdot g \\cdot r_2,\\quad m_2 = \\dfrac{m_1 \\cdot r_1}{r_2} = \\dfrac{' + ein(A.m1, 'kg') + ' \\cdot ' + ein(A.r1, 'm') + '}{' + ein(A.r2, 'm') + '} ' + erg(A.x, 'kg'); } },
      'hebel': { felder: ['F'], muster: '<i>F</i> = {F} N',
        neu: function(){
          // Werte je Gegenstand: Schubkarre bis 80 kg Ladung, Hubkraft höchstens rund 350 N
          var ctx = zufall([
            ['Mit einer Brechstange hebt man eine Steinplatte', 'Steinplatte', 'Ende der Stange', [800, 1200, 2000], [0.08, 0.1, 0.15], [1.0, 1.2, 1.4]],
            ['Mit einer Schubkarre hebt man eine Ladung', 'Ladung', 'Griffen', [400, 550, 800], [0.3, 0.45, 0.5], [1.1, 1.3, 1.5]],
            ['Mit einem Kistenheber hebt man eine Kiste', 'Kiste', 'Griff', [300, 500, 700], [0.1, 0.15], [0.6, 0.9]]]);
          var FL = zufall(ctx[3]), a = zufall(ctx[4]), b = zufall(ctx[5]), schub = ctx[1] === 'Ladung';
          return { F: FL * a / b, FL: FL, a: a, b: b,
            text: ctx[0] + ' (Gewichtskraft \\(' + ein(FL, 'N') + '\\)). Der Drehpunkt ' + (schub ? 'ist die Radachse' : 'liegt auf dem Boden') + '; die ' + ctx[1] + ' greift \\(' + ein(a, 'm') + '\\) davon entfernt an, ' + (schub ? 'die Hände an den Griffen' : 'die Hand am ' + ctx[2]) + ' \\(' + ein(b, 'm') + '\\). Welche Kraft braucht es, senkrecht zum Hebel?' }; },
        pruefen: function(A, e){
          if (nah(e.F, A.F)) return null;
          if (nah(e.F, A.FL * A.b / A.a)) return 'Umgekehrt: Am langen Arm braucht es die kleinere Kraft. \\(F \\cdot r_K = F_L \\cdot r_L\\).';
          if (nah(e.F, A.FL * A.a / (A.b - A.a))) return 'Der Abstand der Hand wird vom Drehpunkt aus gemessen, so wie er dasteht.';
          return 'Hebelgesetz: \\(F \\cdot r_K = F_L \\cdot r_L\\) (Kraft mal Kraftarm gleich Last mal Lastarm).'; },
        fehler: function(A){ return [[{ F: String(A.FL * A.b / A.a) }, 'Umgekehrt']]; },
        loesung: function(A){ return 'F \\cdot r_K = F_L \\cdot r_L,\\quad F = \\dfrac{' + ein(A.FL, 'N') + ' \\cdot ' + ein(A.a, 'm') + '}{' + ein(A.b, 'm') + '} ' + erg(A.F, 'N'); } },
      'mobile': { felder: ['r'], muster: '<i>r</i><sub>3</sub> = {r} m',
        neu: function(){
          var m1, r1, m2, r2, m3;
          do { m1 = zufall([10, 15, 20, 25]); r1 = zufall([0.5, 0.8, 1.2]); m2 = zufall([12, 18, 30]); r2 = zufall([1.6, 1.8, 2]); m3 = zufall([35, 40, 55, 70]); }
          while (r1 === r2 || (m1 * r1 + m2 * r2) / m3 > 2 || m1 === m2);
          return { r: (m1 * r1 + m2 * r2) / m3, m1: m1, r1: r1, m2: m2, r2: r2, m3: m3,
            text: 'Auf der linken Seite einer Wippe sitzen zwei Kinder: \\(' + ein(m1, 'kg') + '\\) bei \\(' + ein(r1, 'm') + '\\) und \\(' + ein(m2, 'kg') + '\\) bei \\(' + ein(r2, 'm') + '\\). Wo muss rechts eine Person mit \\(' + ein(m3, 'kg') + '\\) sitzen, damit Gleichgewicht herrscht?' }; },
        pruefen: function(A, e){
          if (nah(e.r, A.r)) return null;
          if (nah(e.r, A.m1 * A.r1 / A.m3) || nah(e.r, A.m2 * A.r2 / A.m3)) return 'Beide Kinder links drehen in dieselbe Richtung: ihre Momente addieren.';
          if (nah(e.r, (A.m1 + A.m2) * (A.r1 + A.r2) / A.m3) || nah(e.r, (A.m1 + A.m2) * (A.r1 + A.r2) / 2 / A.m3)) return 'Jede Last mit ihrem eigenen Hebelarm: \\(m_1 \\cdot r_1 + m_2 \\cdot r_2\\).';
          return '\\(\\sum M = 0\\): \\(m_1 \\cdot g \\cdot r_1 + m_2 \\cdot g \\cdot r_2 = m_3 \\cdot g \\cdot r_3\\).'; },
        fehler: function(A){ return [[{ r: String(A.m1 * A.r1 / A.m3) }, 'addieren'], [{ r: String((A.m1 + A.m2) * (A.r1 + A.r2) / A.m3) }, 'eigenen']]; },
        loesung: function(A){ return 'm_1 \\cdot r_1 + m_2 \\cdot r_2 = m_3 \\cdot r_3,\\quad r_3 = \\dfrac{' + ein(A.m1, 'kg') + ' \\cdot ' + ein(A.r1, 'm') + ' + ' + ein(A.m2, 'kg') + ' \\cdot ' + ein(A.r2, 'm') + '}{' + ein(A.m3, 'kg') + '} ' + erg(A.r, 'm'); } },

      /* ----- Kapitel 6: Auflagerkräfte ----- */
      'auflager': { felder: ['x'], muster: function(A){ return '<i>F</i><sub>' + A.art + '</sub> = {x} kN'; },
        neu: function(){
          var L, F, x;
          do { L = zufall([4, 5, 6, 8, 12]); F = zufall([6, 15, 24, 40, 90]); x = zufall([1, 1.5, 2, 3, 4.5, 7, 9]); }
          while (x >= L || (L === 8 && F === 40 && x === 2) || !verschieden([F * x / L, F * (L - x) / L, F * x, F * (L - x), F / 2]));   // Aufgabe 6b
          var art = Math.random() < 0.5 ? 'A' : 'B';
          return { art: art, x: art === 'B' ? F * x / L : F * (L - x) / L, L: L, F: F, xx: x,
            text: 'Ein Balken ohne Eigengewicht liegt auf zwei Stützen A und B im Abstand \\(L = ' + ein(L, 'm') + '\\). Eine Last von \\(' + ein(F, 'kN') + '\\) steht \\(' + ein(x, 'm') + '\\) von A entfernt. Wie gross ist die Auflagerkraft \\(F_' + art + '\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.F - A.x)) return 'Das ist die andere Stütze. Die nähere Stütze trägt mehr.';
          if (nah(e.x, A.F * A.xx) || nah(e.x, A.F * (A.L - A.xx))) return 'Das ist ein Drehmoment. Momente um ' + (A.art === 'B' ? 'A' : 'B') + ': \\(F_' + A.art + ' \\cdot L = \\ldots\\), dann durch \\(L\\) teilen.';
          if (nah(e.x, A.F / 2)) return 'Halb und halb gilt nur in der Mitte.';
          return 'Drehachse dort, wo die andere Auflagerkraft angreift: \\(F_B \\cdot L = F \\cdot x\\), dann \\(F_A = F - F_B\\).'; },
        fehler: function(A){ return [[{ x: String(A.F - A.x) }, 'andere'], [{ x: String(A.art === 'B' ? A.F * A.xx : A.F * (A.L - A.xx)) }, 'Drehmoment'], [{ x: String(A.F / 2) }, 'Mitte']]; },
        loesung: function(A){ var B = A.F * A.xx / A.L;
          return '\\sum M_A = 0:\\; F_B \\cdot L = F \\cdot x,\\quad F_B = \\dfrac{' + ein(A.F, 'kN') + ' \\cdot ' + ein(A.xx, 'm') + '}{' + ein(A.L, 'm') + '} ' + erg(B, 'kN') + (A.art === 'A' ? ',\\quad F_A = F - F_B ' + erg(A.x, 'kN') : ''); } },
      'auflager-e': { felder: ['x'], muster: function(A){ return '<i>F</i><sub>' + A.art + '</sub> = {x} kN'; },
        neu: function(){
          var L, FE, FL, x;
          var FB;
          do { L = zufall([6, 8, 10, 12]); FE = zufall([4, 10, 18, 30]); FL = zufall([7, 12, 25, 50]); x = zufall([1, 2, 2.5, 3, 7, 9]); FB = (FL * x + FE * L / 2) / L; }
          while (x >= L || FE === FL || !verschieden([FB, FL + FE - FB, FL * x / L, FL * (L - x) / L, FL * x / L + FE, FL * (L - x) / L + FE]));
          var art = Math.random() < 0.5 ? 'A' : 'B';
          return { art: art, x: art === 'B' ? FB : FL + FE - FB, L: L, FE: FE, FL: FL, xx: x, FB: FB,
            text: 'Eine Brücke (Stützweite \\(L = ' + ein(L, 'm') + '\\), Eigengewicht \\(F_E = ' + ein(FE, 'kN') + '\\) in der Mitte) liegt auf den Stützen A und B. Ein Wagen mit \\(F_L = ' + ein(FL, 'kN') + '\\) steht \\(' + ein(x, 'm') + '\\) von A entfernt. Wie gross ist \\(F_' + art + '\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          var ohne = A.art === 'B' ? A.FL * A.xx / A.L : A.FL * (A.L - A.xx) / A.L;
          if (nah(e.x, ohne)) return 'Das Eigengewicht fehlt: Es greift in der Mitte an, jede Stütze trägt die Hälfte davon.';
          if (nah(e.x, ohne + A.FE)) return 'Das Eigengewicht greift in der Mitte an: Jede Stütze trägt nur die Hälfte davon.';
          if (nah(e.x, A.FL + A.FE - A.x)) return 'Das ist die andere Stütze.';
          return '\\(\\sum M_A = 0\\): \\(F_B \\cdot L = F_L \\cdot x + F_E \\cdot \\tfrac{L}{2}\\), dann \\(F_A = F_L + F_E - F_B\\).'; },
        fehler: function(A){ var ohne = A.art === 'B' ? A.FL * A.xx / A.L : A.FL * (A.L - A.xx) / A.L; return [[{ x: String(ohne) }, 'Eigengewicht fehlt'], [{ x: String(ohne + A.FE) }, 'Hälfte'], [{ x: String(A.FL + A.FE - A.x) }, 'andere']]; },
        loesung: function(A){ return 'F_B = \\dfrac{F_L \\cdot x + F_E \\cdot \\tfrac{L}{2}}{L} = \\dfrac{' + ein(A.FL, 'kN') + ' \\cdot ' + ein(A.xx, 'm') + ' + ' + ein(A.FE, 'kN') + ' \\cdot ' + ein(A.L / 2, 'm') + '}{' + ein(A.L, 'm') + '} ' + erg(A.FB, 'kN') + (A.art === 'A' ? ',\\quad F_A = F_L + F_E - F_B ' + erg(A.x, 'kN') : ''); } },
      'zwei-lasten': { felder: ['x'], muster: '<i>F</i><sub>A</sub> = {x} N',
        neu: function(){
          var L, F1, x1, F2, x2;
          var FB;
          do { L = zufall([3, 4, 5]); F1 = zufall([150, 240, 600, 750]); x1 = zufall([0.5, 1, 1.5]); F2 = zufall([90, 200, 350]); x2 = zufall([2, 2.5, 3.5, 4.5]); FB = (F1 * x1 + F2 * x2) / L; }
          while (x2 >= L || !verschieden([F1 + F2 - FB, FB, F1 * (L - x1) / L, F2 * (L - x2) / L, (F1 + F2) / 2]));
          return { x: F1 + F2 - FB, FB: FB, L: L, F1: F1, x1: x1, F2: F2, x2: x2,
            text: 'Ein Brett ohne Eigengewicht liegt auf zwei Böcken A und B im Abstand \\(' + ein(L, 'm') + '\\). Darauf stehen \\(' + ein(F1, 'N') + '\\) bei \\(' + ein(x1, 'm') + '\\) und \\(' + ein(F2, 'N') + '\\) bei \\(' + ein(x2, 'm') + '\\), beide von A aus gemessen. Wie gross ist \\(F_A\\)?' }; },
        pruefen: function(A, e){
          if (nah(e.x, A.x)) return null;
          if (nah(e.x, A.FB)) return 'Das ist \\(F_B\\). Gesucht ist \\(F_A = F_1 + F_2 - F_B\\).';
          if (nah(e.x, A.F1 * (A.L - A.x1) / A.L) || nah(e.x, A.F2 * (A.L - A.x2) / A.L)) return 'Beide Lasten zählen: jede mit ihrem Hebelarm.';
          if (nah(e.x, (A.F1 + A.F2) / 2)) return 'Halb und halb gilt nur, wenn die Lasten symmetrisch stehen.';
          return 'Momente um A: \\(F_B \\cdot L = F_1 \\cdot x_1 + F_2 \\cdot x_2\\), dann \\(F_A = F_1 + F_2 - F_B\\).'; },
        fehler: function(A){ return [[{ x: String(A.FB) }, 'Das ist'], [{ x: String(A.F1 * (A.L - A.x1) / A.L) }, 'Beide'], [{ x: String((A.F1 + A.F2) / 2) }, 'symmetrisch']]; },
        loesung: function(A){ return 'F_B = \\dfrac{' + ein(A.F1, 'N') + ' \\cdot ' + ein(A.x1, 'm') + ' + ' + ein(A.F2, 'N') + ' \\cdot ' + ein(A.x2, 'm') + '}{' + ein(A.L, 'm') + '} ' + erg(A.FB, 'N') + ',\\quad F_A = F_1 + F_2 - F_B ' + erg(A.x, 'N'); } }
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
