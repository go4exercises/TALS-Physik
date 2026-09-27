// ─────────────────────────────────────────────────────────────
//  Physik begreifbar — Shared Library (physiklib.js)
//
//  Single Source of Truth für alle Themenseiten:
//    - Canvas-Helper (initCanvas, drawGrid, drawAxesUnits, drawArrow, drawVector)
//    - Zahlen-Formatierer (fmt, fmtS, fmtSig)
//    - Lösungs-Toggle (toggleL)
//    - MathJax-Re-Typeset, serialisiert (mjTypeset)
//    - Formelzeilen in LaTeX, eine Rechnung pro Zeile (flTex, texE, texO)
//    - Clip-Start/-Stop fuer die Erklaerclips (clipStart, clipStop)
//
//  Einbindung auf Themenseiten:
//    <script src="../physiklib.js"></script>
//
//  Pfad-Konvention: Themenseiten liegen in themen/, also wird die Lib
//  über ../physiklib.js eingebunden.
// ─────────────────────────────────────────────────────────────

/* ── Zahlen-Formatierer ──────────────────────────────────── */
// Standardformatter: ganze Zahlen ohne Nachkommastelle, sonst 1-2 Stellen.
// Konvention: Dezimal-PUNKT (Schweizer Schul-Konvention, vgl. STYLEGUIDE §2.5).
const fmt = n => {
  if (n === 0) return '0';
  if (Math.abs(n) >= 100) return n.toFixed(0);
  if (n % 1 === 0) return n.toString();
  if (Math.abs(n) >= 10) return n.toFixed(1);
  return n.toFixed(2);
};
// Vorzeichen-Term für Verkettung: '+ 5' / '− 5' (Unicode-Minus U+2212)
const fmtS = n => n >= 0 ? `+ ${fmt(n)}` : `− ${fmt(Math.abs(n))}`;
// Signifikante Stellen (für Physik-Werte typisch 2-3)
const fmtSig = (n, k = 3) => {
  if (n === 0) return '0';
  const abs = Math.abs(n);
  const order = Math.floor(Math.log10(abs));
  const factor = Math.pow(10, k - 1 - order);
  return (Math.round(n * factor) / factor).toString();
};

/* ── Lösungs-Toggle ──────────────────────────────────────── */
function toggleL(id) {
  const b = document.getElementById(id);
  const btn = b.previousElementSibling;
  const o = b.classList.toggle('sichtbar');
  btn.textContent = o ? '▼ Lösung verbergen' : '▶ Lösung';
}

/* ── MathJax: serialisiertes, Startup-gegateetes Typesetting ───────────────────
   Zentraler Ersatz für direkte MathJax.typesetPromise(...)-Aufrufe. Behebt zwei
   Races, die einzelne Formeln sporadisch leer rendern liessen (vor allem beim
   Hard-Refresh, nicht beim Zurückblättern aus dem bfcache):
     1) eigene Typeset-Aufrufe beim Laden, die mit MathJax' initialem Render der
        ganzen Seite kollidieren  → die erste Queue-Stufe wartet auf
        MathJax.startup.promise, läuft also erst NACH dem Initial-Render;
     2) sich überlappende Re-Typesets auf denselben Elementen (verstärkt durch
        svg.fontCache:'global')  → alle Aufrufe werden seriell verkettet, ein
        neuer startet erst, wenn der vorige fertig ist.
   Nur bei dynamisch (per innerHTML) geänderter Mathematik aufrufen — statische
   HTML-Formeln rendert MathJax beim Laden selbst.
   Aufruf:  mjTypeset([el, ...])   bzw.   mjTypeset()  für die ganze Seite.
   Gibt das Promise des Durchlaufs zurück (für optionales .then()/await). */
let _mjTypesetQueue = null;
function mjTypeset(els) {
  if (!(window.MathJax && MathJax.typesetPromise)) return Promise.resolve();
  if (!_mjTypesetQueue) {
    _mjTypesetQueue = (MathJax.startup && MathJax.startup.promise) || Promise.resolve();
  }
  _mjTypesetQueue = _mjTypesetQueue
    .then(() => MathJax.typesetPromise(els))
    .catch(err => console.error('mjTypeset:', err));
  return _mjTypesetQueue;
}

/* ── Formelzeilen in LaTeX (flTex) ─────────────────────────
   Für jede .fl-eq mit Live-Werten. Auf allen Themenseiten dieselbe Umsetzung;
   Regeln: STYLEGUIDE §2.8 («Eine Rechnung, eine Zeile»).
   Aufruf:  flTex(id, ['I = \\frac{U}{R}', '= \\frac{'+texE(6,'V')+'}{'+texO(100)+'}', '= '+texE(60,'mA')])
─────────────────────────────────────────────────────────── */
// Formel und Zahlengleichung stehen in LaTeX; MathJax muss darum bei jeder
// Reglerbewegung neu setzen. Jede Zeile wird auf einen Frame gedrosselt, alle
// Zeilen laufen in EINER Promise-Kette — sonst überholen sich zwei Läufe und
// hinterlassen halb gesetzte Formeln. Muster aus p5-2, Animation 2.
let flKette = Promise.resolve();
const flOffen = new Map();
// Eine Rechnung steht auf EINER Zeile: Formelzeichen = Formel = Zahlen mit
// Einheiten = Ergebnis. Sie wird als Array von Gliedern übergeben
// (['I = \\frac{U}{R}', '= \\frac{…}{…}', '= 60\\;\\text{mA}']); jedes Glied ist
// eine eigene Formel, dazwischen eine Umbruchstelle ohne Abstand (<wbr> — ein
// Leerzeichen käme zum Abstand vor dem «=» noch dazu). Reicht der Platz nicht, bricht
// die Zeile darum nur vor einem Gleichheitszeichen um — nie mitten im Bruch.
// tex: String oder Glieder-Array = eine Rechnung; Array von Rechnungen = mehrere,
// durch Strichpunkt getrennt. '' leert und versteckt die Zeile.
// Ein «=» am Anfang eines Glieds bekäme von MathJax links keinen Abstand;
// das leere {} davor macht es zum gewöhnlichen Relationszeichen.
const flTeil = t => '\\(\\displaystyle ' + (t.charAt(0) === '=' ? '{}' : '') + t + '\\)';
function flHtml(tex){
  const liste = (Array.isArray(tex) && tex.some(Array.isArray)) ? tex : [tex];
  return liste.map((r, i) => {
    const glieder = Array.isArray(r) ? r.slice() : [r];
    if(i < liste.length-1) glieder[glieder.length-1] += ';';
    return glieder.map(flTeil).join('<wbr>');
  }).join('&ensp; ');
}
function flTex(id, tex){
  const el = document.getElementById(id); if(!el) return;
  el.style.display = tex === '' ? 'none' : '';
  const h = tex === '' ? '' : flHtml(tex);
  const wartet = flOffen.has(el);
  if(!wartet && el.dataset.stand === h) return;           // nichts geändert
  flOffen.set(el, h);
  if(wartet) return;
  requestAnimationFrame(() => {
    const h2 = flOffen.get(el); flOffen.delete(el);
    if(el.dataset.stand === h2) return;
    el.dataset.stand = h2;
    flKette = flKette
      .then(() => window.MathJax && MathJax.startup && MathJax.startup.promise)
      .then(() => {
        if(window.MathJax && MathJax.typesetClear) MathJax.typesetClear([el]);
        el.innerHTML = h2;
        return (window.MathJax && MathJax.typesetPromise) ? MathJax.typesetPromise([el]) : null;
      }).then(() => {
        // Jedes Glied als inline-block: dann reserviert die Zeile die volle Höhe
        // der Brüche, und umgebrochene Glieder berühren sich nicht.
        el.querySelectorAll('mjx-container').forEach(c => { c.style.display = 'inline-block'; c.style.margin = '2px 0'; });
      }).catch(() => {});
  });
}
// Zahl mit Einheit, STYLEGUIDE §2.3: \; vor der Einheit, Einheit aufrecht
const texE = (zahl, einheit) => zahl + '\\;\\text{' + einheit + '}';
const texO = zahl => zahl + '\\;\\Omega';

/* ── Canvas-Helper ───────────────────────────────────────────
   initCanvas(id, H, square)
     id      : Canvas-Element-ID
     H       : gewünschte Höhe in CSS-Pixeln (wird ignoriert, wenn square=true)
     square  : true → Höhe = Breite (1:1-Plot, reine Mathematik)
               false → frei wählbar (Anwendung)
   Liefert {ctx, W, H}: ctx ist auf logische Pixel skaliert (DPR-korrekt).
─────────────────────────────────────────────────────────── */
function initCanvas(id, H, square) {
  const c = document.getElementById(id);
  const dpr = window.devicePixelRatio || 1;
  // Pixel-Fixierung einer früheren Zeichnung lösen, damit die echte aktuelle
  // Container-Breite gemessen wird (sonst passt sich die Grafik erst beim Neuladen an).
  c.style.width = '';
  const W = c.offsetWidth || 600;
  const actualH = square ? W : H;
  c.width = W * dpr; c.height = actualH * dpr;
  c.style.width = W + 'px'; c.style.height = actualH + 'px';
  const ctx = c.getContext('2d'); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.scale(dpr, dpr);
  return { ctx, W, H: actualH };
}

/* niceStep: wählt einen "schönen" Tick-Abstand für eine Achse, so dass die
   Tick-Beschriftungen lesbar bleiben. range = (max - min) im Logik-Koordinaten,
   pixels = verfügbare Pixel-Länge, targetPx = Wunsch-Abstand zwischen Ticks
   (typisch 55-70 für x, 35-50 für y). Liefert Schritt aus 1·10ⁿ, 2·10ⁿ, 5·10ⁿ. */
function niceStep(range, pixels, targetPx) {
  if (range <= 0 || pixels <= 0) return 1;
  const rough = range * targetPx / pixels;
  const pow = Math.pow(10, Math.floor(Math.log10(rough)));
  const norm = rough / pow;
  let nice;
  if (norm < 1.5)      nice = 1;
  else if (norm < 3.5) nice = 2;
  else if (norm < 7.5) nice = 5;
  else                 nice = 10;
  return nice * pow;
}

/* fmtTick: formatiert einen Tick-Wert mit der minimalen sinnvollen Anzahl
   Nachkommastellen, abhängig vom Schritt. Verhindert Dinge wie "0.30000000004". */
function fmtTick(v, step) {
  if (Math.abs(v) < step * 1e-6) return '0';
  const decimals = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
  return v.toFixed(decimals);
}

/* drawGrid: kartesisches Gitter + Achsen + Pfeile + Default-Zahlenlabels.
   Verwendet automatische Tick-Schrittweite ("nice ticks") damit Beschriftungen
   bei beliebigen Bereichen lesbar bleiben. Liefert die Pixel-Konverter cx und cy. */
/* Skalenzahlen nach den Kurven noch einmal setzen.
   drawGrid zeichnet die Zahlen, bevor die Seite ihre Kurven, Flächen und Pfeile
   darüberlegt. Liegt die Achse am Rand, stehen die Zahlen im Diagramm und werden
   von Linien gekreuzt. Darum merkt sich drawGrid die Zahlen samt der aktuellen
   Transformation und prüft in einem Microtask — er läuft, sobald die synchrone
   Zeichenfunktion der Seite fertig ist, und noch vor dem Neuzeichnen des
   Bildschirms, also ohne Flackern —, was aus jeder Zahl geworden ist:
     - noch grösstenteils sichtbar (nur gekreuzt): neu setzen, mit schmalem
       weissem Rand um die Ziffern;
     - grösstenteils verschwunden (ein Punkt, eine Fläche oder ein Pfeil liegt
       darauf, oder die Seite hat sie absichtlich übermalt): so lassen.
   Ein Kästchen statt des Rands wäre zu grob — es zerschneidet Pfeile und stanzt
   Löcher in Flächen. Gemessen wird am Bild: Anteil der Pixel in Zahlenfarbe,
   verglichen mit der Ziffernmenge derselben Zahl auf einem Hilfs-Canvas. */
const _tickTinte = new Map();          // Schrift|Text|Massstab -> Anzahl Ziffernpixel
function _tickPixel(font, text, scale) {
  const key = font + '|' + text + '|' + scale;
  if (_tickTinte.has(key)) return _tickTinte.get(key);
  const c = document.createElement('canvas'); c.width = 200 * scale; c.height = 24 * scale;
  const g = c.getContext('2d', { willReadFrequently: true });
  g.scale(scale, scale); g.font = font; g.fillStyle = '#6b7280'; g.textBaseline = 'top'; g.fillText(text, 2, 2);
  const d = g.getImageData(0, 0, c.width, c.height).data; let n = 0;
  for (let k = 0; k < d.length; k += 4) if (d[k + 3] > 200) n++;
  _tickTinte.set(key, n); return n;
}
const _tickOffen = new WeakMap();       // Kontext -> noch nicht gesetzte Zahlen
const _tickEntscheid = new WeakMap();   // Kontext -> letzte Messung (für laufende Animationen)
function tickNachzeichnen(ctx, labels, font, farbe) {
  if (!labels.length || typeof ctx.getTransform !== 'function') return;
  const T = ctx.getTransform();
  if (!T || typeof T.a !== 'number' || !ctx.canvas) return;   // jsdom-Attrappe u. ä.
  const eintrag = { T, labels, font, farbe };
  const offen = _tickOffen.get(ctx);
  if (offen) { offen.push(eintrag); return; }
  _tickOffen.set(ctx, [eintrag]);
  Promise.resolve().then(() => {
    const alle = _tickOffen.get(ctx); _tickOffen.delete(ctx);
    const cv = ctx.canvas, BW = cv.width, BH = cv.height;
    // Laufende Animation (nächster Aufruf < 60 ms nach dem letzten): nur jedes
    // achte Bild neu messen und dazwischen die letzte Entscheidung verwenden.
    // Jedes Rücklesen zwingt den Browser, auf die Grafikkarte zu warten —
    // auch kleine Flächen kosteten zusammen rund 3 ms pro Bild.
    const jetzt = performance.now(), alt = _tickEntscheid.get(ctx);
    const schluessel = alle.map(g => g.labels.map(l => l.t + '@' + Math.round(l.x) + ',' + Math.round(l.y)).join('|')).join('#');
    if (alt && alt.schluessel === schluessel && jetzt - alt.zuletzt < 60 && alt.frei < 7) {
      alt.zuletzt = jetzt; alt.frei++;
      for (const [gi, li] of alt.plan) zeichne(alle[gi], alle[gi].labels[li]);
      return;
    }
    // Nur die Flächen der Zahlen auslesen, nicht das ganze Bild: In laufenden
    // Animationen geschieht das in jedem Bild, und ein Rücklesen des ganzen
    // Canvas kostete gemessen 8 ms pro Bild (Wechselspannung, 2 Diagramme).
    // Erst messen, dann zeichnen — sonst läse die zweite Zahl die erste mit.
    const plan = [];
    for (const g of alle) {
      const T = g.T;
      ctx.save(); ctx.setTransform(T); ctx.font = g.font;
      for (const l of g.labels) {
        const w = ctx.measureText(l.t).width, h = 14;
        const x0 = l.a === 'center' ? l.x - w / 2 : (l.a === 'right' ? l.x - w : l.x);
        const y0 = l.b === 'top' ? l.y : (l.b === 'bottom' ? l.y - h : l.y - h / 2);
        const X0 = Math.max(0, Math.floor(T.a * x0 + T.e)), X1 = Math.min(BW, Math.ceil(T.a * (x0 + w) + T.e));
        const Y0 = Math.max(0, Math.floor(T.d * y0 + T.f)), Y1 = Math.min(BH, Math.ceil(T.d * (y0 + h) + T.f));
        if (X1 <= X0 || Y1 <= Y0) continue;
        let d;
        try { d = ctx.getImageData(X0, Y0, X1 - X0, Y1 - Y0).data; } catch (e) { ctx.restore(); return; }   // «tainted»
        let n = 0;
        for (let k = 0; k < d.length; k += 4)
          if (d[k + 3] > 200 && Math.abs(d[k] - 107) + Math.abs(d[k + 1] - 114) + Math.abs(d[k + 2] - 128) < 60) n++;
        const soll = _tickPixel(g.font, l.t, Math.abs(T.a) || 1);
        if (soll && n / soll >= 0.5) plan.push([alle.indexOf(g), g.labels.indexOf(l)]);   // sonst zugedeckt oder absichtlich entfernt
      }
      ctx.restore();
    }
    _tickEntscheid.set(ctx, { schluessel, plan, zuletzt: jetzt, frei: 0 });
    for (const [gi, li] of plan) zeichne(alle[gi], alle[gi].labels[li]);
  });
  function zeichne(g, l) {
    ctx.save();
    ctx.setTransform(g.T); ctx.globalAlpha = 1; ctx.setLineDash([]); ctx.font = g.font;
    ctx.textAlign = l.a; ctx.textBaseline = l.b;
    ctx.lineJoin = 'round'; ctx.lineWidth = 3; ctx.strokeStyle = '#fff';
    ctx.strokeText(l.t, l.x, l.y);
    ctx.fillStyle = g.farbe; ctx.fillText(l.t, l.x, l.y);
    ctx.restore();
  }
}

function drawGrid(ctx, W, H, xMin, xMax, yMin, yMax) {
  const cx = x => (x - xMin) / (xMax - xMin) * W;
  const cy = y => H - (y - yMin) / (yMax - yMin) * H;
  // Tick-Schritte automatisch wählen
  const stepX = niceStep(xMax - xMin, W, 65);
  const stepY = niceStep(yMax - yMin, H, 40);
  // Tick-Werte aus Vielfachen des Schritts (nicht aus integer-Sprüngen)
  const xTicks = [];
  for (let v = Math.ceil(xMin / stepX) * stepX; v <= xMax + stepX * 1e-6; v += stepX) xTicks.push(v);
  const yTicks = [];
  for (let v = Math.ceil(yMin / stepY) * stepY; v <= yMax + stepY * 1e-6; v += stepY) yTicks.push(v);

  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
  // Vertikales Gitter
  for (const v of xTicks) {
    const isZero = Math.abs(v) < stepX * 1e-6;
    ctx.strokeStyle = isZero ? '#b8c4d4' : '#eff1f5';
    ctx.lineWidth = isZero ? 1.5 : 1;
    ctx.beginPath(); ctx.moveTo(cx(v), 0); ctx.lineTo(cx(v), H); ctx.stroke();
  }
  // Horizontales Gitter
  for (const v of yTicks) {
    const isZero = Math.abs(v) < stepY * 1e-6;
    ctx.strokeStyle = isZero ? '#b8c4d4' : '#eff1f5';
    ctx.lineWidth = isZero ? 1.5 : 1;
    ctx.beginPath(); ctx.moveTo(0, cy(v)); ctx.lineTo(W, cy(v)); ctx.stroke();
  }
  // Hauptachsen (durch 0 bzw. Rand wenn 0 nicht im Bereich)
  const xAxisY = (yMin <= 0 && 0 <= yMax) ? cy(0) : (yMin > 0 ? cy(yMin) : cy(yMax));
  const yAxisX = (xMin <= 0 && 0 <= xMax) ? cx(0) : (xMin > 0 ? cx(xMin) : cx(xMax));
  ctx.strokeStyle = '#374151'; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(0, xAxisY);   ctx.lineTo(W, xAxisY);   ctx.stroke();
  ctx.beginPath(); ctx.moveTo(yAxisX, 0);   ctx.lineTo(yAxisX, H);   ctx.stroke();
  // Pfeilköpfe
  ctx.fillStyle = '#374151';
  ctx.beginPath(); ctx.moveTo(W - 8, xAxisY - 4); ctx.lineTo(W, xAxisY); ctx.lineTo(W - 8, xAxisY + 4); ctx.fill();
  ctx.beginPath(); ctx.moveTo(yAxisX - 4, 8);     ctx.lineTo(yAxisX, 0); ctx.lineTo(yAxisX + 4, 8);     ctx.fill();
  // Tick-Beschriftungen (Zahlen)
  ctx.font = '13px JetBrains Mono,monospace'; ctx.fillStyle = '#6b7280';
  // x-Tick-Labels: oben oder unten relativ zur x-Achse, je nach verfügbarem Platz
  const xLblBelow = (H - xAxisY) >= 18;
  ctx.textAlign = 'center'; ctx.textBaseline = xLblBelow ? 'top' : 'bottom';
  const tickLabels = [];                               // für das Nachzeichnen, s. unten
  for (const v of xTicks) {
    if (Math.abs(v) < stepX * 1e-6) continue;
    if (cx(v) < 14 || cx(v) > W - 72) continue;        // Rand-Bereich für x-Label reserviert
    const py = xAxisY + (xLblBelow ? 5 : -5);
    ctx.fillText(fmtTick(v, stepX), cx(v), py);
    tickLabels.push({ t: fmtTick(v, stepX), x: cx(v), y: py, a: 'center', b: ctx.textBaseline });
  }
  // y-Tick-Labels: je nach Platz links oder rechts der Y-Achse anbringen
  ctx.textBaseline = 'middle';
  // Maximale Textbreite abschätzen
  let maxLblW = 0;
  for (const v of yTicks) {
    if (Math.abs(v) < stepY * 1e-6) continue;
    maxLblW = Math.max(maxLblW, ctx.measureText(fmtTick(v, stepY)).width);
  }
  const labelLeft = yAxisX >= maxLblW + 8;
  ctx.textAlign = labelLeft ? 'right' : 'left';
  for (const v of yTicks) {
    if (Math.abs(v) < stepY * 1e-6) continue;
    if (cy(v) < 22 || cy(v) > H - 6) continue;          // Bereich oben für y-Label reserviert
    const px = labelLeft ? yAxisX - 5 : yAxisX + 5;
    ctx.fillText(fmtTick(v, stepY), px, cy(v));
    tickLabels.push({ t: fmtTick(v, stepY), x: px, y: cy(v), a: ctx.textAlign, b: 'middle' });
  }
  ctx.textBaseline = 'alphabetic';
  tickNachzeichnen(ctx, tickLabels, '13px JetBrains Mono,monospace', '#6b7280');
  // Default-Achsenlabels "x" und "y" (werden ggf. von drawAxesUnits überschrieben)
  ctx.fillStyle = '#374151'; ctx.font = 'bold 13px monospace';
  ctx.textAlign = 'left';   ctx.fillText('x', W - 14, xAxisY - 7);
  ctx.textAlign = 'center'; ctx.fillText('y', yAxisX + 13, 14);
  return { cx, cy, stepX, stepY };
}

/* drawAxesUnits: nach drawGrid aufrufen, um die generischen „x"/„y"-Labels
   mit Grösse + Einheit zu überschreiben. Beispiel:
     drawAxesUnits(ctx, W, H, cx, cy, 't [s]', 'v [m/s]');
*/
function drawAxesUnits(ctx, W, H, cx, cy, xLabel, yLabel, xLblDy) {
  // Position der Achsen (auch wenn 0 nicht im Bereich liegt)
  const xAxisPy = (typeof cy === 'function')
    ? (cy(0) >= 0 && cy(0) <= H ? cy(0) : (cy(0) < 0 ? 0 : H))
    : cy;
  const yAxisPx = (typeof cx === 'function')
    ? (cx(0) >= 0 && cx(0) <= W ? cx(0) : (cx(0) < 0 ? 0 : W))
    : cx;
  ctx.font = 'bold 13px JetBrains Mono,monospace';
  const xLblW = Math.ceil(ctx.measureText(xLabel).width) + 8;
  const yLblW = Math.ceil(ctx.measureText(yLabel).width) + 8;
  // Generisches Default-Label überdecken (bedarfsorientiert tight)
  // xLblDy: negativer Versatz, wenn die Tick-Beschriftungen derselben Achse in
  // derselben Zeile liegen (z.B. wenn die Achse am unteren Rand klebt)
  const dyX = xLblDy || 0;
  ctx.fillStyle = '#fff';
  // Bei Versatz zwei Flecken: ein schmaler ueber dem generischen Default-Label
  // (sonst bleibt das 'x' sichtbar) und der breite in der neuen Zeile. Ein
  // breiter Fleck ueber beide Zeilen wuerde die letzte Tick-Beschriftung fressen.
  if (dyX) ctx.fillRect(W - 18, xAxisPy - 19, 16, 17);
  ctx.fillRect(W - xLblW, xAxisPy - 19 + dyX, xLblW - 2, 17);
  ctx.fillRect(yAxisPx + 2, 0, yLblW, 18);
  // Neu zeichnen
  ctx.fillStyle = '#374151';
  ctx.textAlign = 'right'; ctx.textBaseline = 'alphabetic';
  ctx.fillText(xLabel, W - 4, xAxisPy - 6 + dyX);
  ctx.textAlign = 'left';
  ctx.fillText(yLabel, yAxisPx + 6, 12);
}

/* drawArrow: Pfeil von (x1,y1) nach (x2,y2) in Pixel-Koordinaten.
   color: Strichfarbe; lw: Strichbreite; head: Pfeilkopf-Länge in px. */
function drawArrow(ctx, x1, y1, x2, y2, color, lw = 2, head = 9) {
  const dx = x2 - x1, dy = y2 - y1;
  const len = Math.hypot(dx, dy);
  if (len < 1e-6) return;
  const ux = dx / len, uy = dy / len;
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = lw; ctx.setLineDash([]);
  // Schaft endet kurz vor Spitze, damit der Kopf sauber sitzt
  const xs = x2 - ux * head * 0.85;
  const ys = y2 - uy * head * 0.85;
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(xs, ys); ctx.stroke();
  // Pfeilkopf als Dreieck
  const perpX = -uy, perpY = ux;
  const bx = x2 - ux * head, by = y2 - uy * head;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(bx + perpX * head * 0.4, by + perpY * head * 0.4);
  ctx.lineTo(bx - perpX * head * 0.4, by - perpY * head * 0.4);
  ctx.closePath(); ctx.fill();
}

/* drawVector: Pfeil im logischen Koordinatensystem (cx/cy-Funktionen)
   vom Punkt (x0,y0) mit Komponenten (dx,dy). Mit optionalem Label. */
function drawVector(ctx, cx, cy, x0, y0, dx, dy, color, label, lw = 2.2) {
  const px1 = cx(x0), py1 = cy(y0);
  const px2 = cx(x0 + dx), py2 = cy(y0 + dy);
  drawArrow(ctx, px1, py1, px2, py2, color, lw, 10);
  if (label) {
    ctx.fillStyle = color;
    ctx.font = 'bold 13px JetBrains Mono,monospace';
    ctx.textAlign = 'center';
    // Label mittig über dem Pfeil — ausser bei STEILEN Pfeilen: dort liegt es
    // sonst auf den Achsenwerten, darum wandert es zur Seite (in Pfeilrichtung
    // gesehen nach rechts).
    const vdx = px2 - px1, vdy = py2 - py1;
    let lx, ly;
    if (Math.abs(vdy) > 2 * Math.abs(vdx)) {
      lx = (px1 + px2) / 2 + (vdy < 0 ? 11 : -11);
      ly = (py1 + py2) / 2 + 4;
    } else {
      lx = (px1 + px2) / 2;
      ly = (py1 + py2) / 2 - 7;
    }
    ctx.fillText(label, lx, ly);
  }
}

/* drawDot: Punkt im logischen Koordinatensystem */
function drawDot(ctx, cx, cy, x, y, color, r) {
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(cx(x), cy(y), r || 6, 0, Math.PI * 2); ctx.fill();
}

/* drawCurve: zeichnet eine parametrische Kurve t→(x(t),y(t)) im
   logischen Koordinatensystem. tMin, tMax: Parameterbereich, steps:
   Anzahl Stützstellen. */
function drawCurve(ctx, cx, cy, xFn, yFn, tMin, tMax, steps, color, lw = 2.5) {
  ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.setLineDash([]);
  ctx.beginPath();
  const dt = (tMax - tMin) / steps;
  for (let i = 0; i <= steps; i++) {
    const t = tMin + i * dt;
    const px = cx(xFn(t)), py = cy(yFn(t));
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();
}

/* ── Clip starten und wieder schliessen ───────────────────────────────────────
   Ein Clip wird bewusst nicht beim Seitenaufruf geladen. Sichtbar ist zuerst
   nur der Knopf; erst der Klick setzt das <iframe> ein. So laeuft bei mehreren
   Clips keiner von selbst los, und die Seite laedt nicht N Dokumente mit.

   Zwei Spielarten, gesteuert ueber data-modus am .clip-Element:
     ohne Angabe  — der Clip laeuft an Ort und Stelle. So auf den
                    Lektionsseiten, wo er zwischen Theorie und Aufgaben gehoert.
     "gross"      — der Clip laeuft ueber dem Fenster. So in der Bibliothek,
                    wo die Zeile viel zu schmal waere.
   Markup erzeugt scripts/build-clips-einbau.py. */
function clipStart(btn) {
  const karte = btn.closest('.clip');
  if (!karte) return;
  const quelle = karte.dataset.clip;
  const titel  = karte.dataset.titel || 'Clip';
  if (!quelle) return;

  if (karte.dataset.modus === 'gross') {
    if (document.querySelector('.clip-buehne')) return;
    clipBuehne(quelle, titel);
    return;
  }
  if (karte.querySelector('.clip-ansicht')) return;

  const ansicht = document.createElement('div');
  ansicht.className = 'clip-ansicht';
  ansicht.appendChild(clipKnopf('clip-zu', '✕ Clip schliessen'));
  ansicht.appendChild(clipRahmen('clip-rahmen', quelle, titel));
  btn.hidden = true;
  karte.appendChild(ansicht);
  ansicht.querySelector('iframe').focus({ preventScroll: true });
}

/* Grosse Buehne ueber dem Fenster. Bewusst kein neuer Tab: Der wuerde die
   Liste verlassen, und ein vergessener Tab spielt weiter. Wer projizieren
   will, findet im Kopf trotzdem einen Link in einen eigenen Tab. */
function clipBuehne(quelle, titel) {
  // Die Buehne deckt die Seite ab; scrollte sie darunter weiter, verlaesst
  // man beim Schliessen die Stelle, an der man war.
  clipRueckkehr = document.activeElement;
  document.body.style.overflow = 'hidden';
  const buehne = document.createElement('div');
  buehne.className = 'clip-buehne';
  buehne.setAttribute('role', 'dialog');
  buehne.setAttribute('aria-modal', 'true');
  buehne.setAttribute('aria-label', 'Clip: ' + titel);

  const kopf = document.createElement('div');
  kopf.className = 'cb-kopf';
  const t = document.createElement('span');
  t.className = 'cb-titel';
  t.textContent = titel;
  const tab = document.createElement('a');
  tab.className = 'cb-tab';
  tab.href = quelle;
  tab.target = '_blank';
  tab.rel = 'noopener';
  tab.textContent = 'eigener Tab ↗';
  kopf.appendChild(t);
  kopf.appendChild(tab);
  kopf.appendChild(clipKnopf('cb-zu', '✕ Schliessen'));

  buehne.appendChild(kopf);
  buehne.appendChild(clipRahmen('cb-rahmen', quelle, titel));

  // Klick auf den dunklen Rand schliesst, Klick auf den Clip nicht.
  buehne.addEventListener('click', e => { if (e.target === buehne) clipZu(); });
  document.addEventListener('keydown', clipEscape);
  document.body.appendChild(buehne);
  // Der Fokus gehoert in den Clip, nicht auf «Schliessen»: Sonst landen
  // Pfeiltasten (spulen) auf der Seite, und die Leertaste (Pause) drueckt
  // den Knopf und schliesst den Clip. Escape faengt der Clip nicht selbst
  // ab — darum haengt sich clipEscape nach dem Laden auch an sein Dokument
  // (gleiche Herkunft; bei file:// verweigert, dann bleiben Knopf und Rand).
  const f = buehne.querySelector('iframe');
  f.focus({ preventScroll: true });
  f.addEventListener('load', () => {
    f.focus({ preventScroll: true });
    try { f.contentWindow.document.addEventListener('keydown', clipEscape); } catch (e) {}
  });
}

function clipKnopf(klasse, text) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = klasse;
  b.textContent = text;
  b.setAttribute('onclick', 'clipStop(this)');
  return b;
}

function clipRahmen(klasse, quelle, titel) {
  const rahmen = document.createElement('div');
  rahmen.className = klasse;
  const f = document.createElement('iframe');
  f.src = quelle;
  f.title = 'Clip: ' + titel;
  f.setAttribute('allowfullscreen', '');
  // Der Clip startet den Ton selbst. Ohne diese Erlaubnis verweigert der
  // Browser das im eingebetteten Rahmen, obwohl der Klick auf die Karte
  // die noetige Geste war — der Clip faellt dann still auf stumm zurueck.
  f.setAttribute('allow', 'autoplay');
  rahmen.appendChild(f);
  return rahmen;
}

function clipEscape(e) { if (e.key === 'Escape') clipZu(); }

// Wohin der Fokus nach dem Schliessen zurueckgeht. Ohne das landet er am
// Seitenanfang, und wer per Tastatur bedient, sucht seine Stelle neu.
let clipRueckkehr = null;

function clipZu() {
  const buehne = document.querySelector('.clip-buehne');
  if (!buehne) return;
  buehne.remove();                       // entfernt das iframe, der Clip haelt an
  document.removeEventListener('keydown', clipEscape);
  document.body.style.overflow = '';     // Seite wieder scrollbar
  if (clipRueckkehr) { clipRueckkehr.focus({ preventScroll: true }); clipRueckkehr = null; }
}

function clipStop(knopf) {
  if (knopf.closest('.clip-buehne')) { clipZu(); return; }
  const karte = knopf.closest('.clip');
  if (!karte) return;
  const ansicht = karte.querySelector('.clip-ansicht');
  if (ansicht) ansicht.remove();
  const btn = karte.querySelector('.clip-start');
  if (btn) { btn.hidden = false; btn.focus({ preventScroll: true }); }
}

/* Ein Sprungziel in einem zugeklappten <details> waere sonst unerreichbar:
   Die Suche fuehrt auf #clip-…, das steht im Transkript-Aufklapper. */
(function () {
  function oeffneZiel() {
    if (!location.hash) return;
    const ziel = document.getElementById(location.hash.slice(1));
    if (!ziel) return;
    let d = ziel.closest('details');
    while (d) { d.open = true; d = d.parentElement && d.parentElement.closest('details'); }
    ziel.scrollIntoView();
  }
  window.addEventListener('hashchange', oeffneZiel);
  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', oeffneZiel);
  else oeffneZiel();
})();
