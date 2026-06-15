// ─────────────────────────────────────────────────────────────
//  TALS Physik — Shared Library (physiklib.js)
//
//  Single Source of Truth für alle Themenseiten:
//    - Canvas-Helper (initCanvas, drawGrid, drawAxesUnits, drawArrow, drawVector)
//    - Zahlen-Formatierer (fmt, fmtS, fmtSig)
//    - Lösungs-Toggle (toggleL)
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
  ctx.font = '11px JetBrains Mono,monospace'; ctx.fillStyle = '#6b7280';
  // x-Tick-Labels: oben oder unten relativ zur x-Achse, je nach verfügbarem Platz
  const xLblBelow = (H - xAxisY) >= 18;
  ctx.textAlign = 'center'; ctx.textBaseline = xLblBelow ? 'top' : 'bottom';
  for (const v of xTicks) {
    if (Math.abs(v) < stepX * 1e-6) continue;
    if (cx(v) < 14 || cx(v) > W - 72) continue;        // Rand-Bereich für x-Label reserviert
    const py = xAxisY + (xLblBelow ? 5 : -5);
    ctx.fillText(fmtTick(v, stepX), cx(v), py);
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
  }
  ctx.textBaseline = 'alphabetic';
  // Default-Achsenlabels "x" und "y" (werden ggf. von drawAxesUnits überschrieben)
  ctx.fillStyle = '#374151'; ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'left';   ctx.fillText('x', W - 14, xAxisY - 7);
  ctx.textAlign = 'center'; ctx.fillText('y', yAxisX + 13, 14);
  return { cx, cy, stepX, stepY };
}

/* drawAxesUnits: nach drawGrid aufrufen, um die generischen „x"/„y"-Labels
   mit Grösse + Einheit zu überschreiben. Beispiel:
     drawAxesUnits(ctx, W, H, cx, cy, 't [s]', 'v [m/s]');
*/
function drawAxesUnits(ctx, W, H, cx, cy, xLabel, yLabel) {
  // Position der Achsen (auch wenn 0 nicht im Bereich liegt)
  const xAxisPy = (typeof cy === 'function')
    ? (cy(0) >= 0 && cy(0) <= H ? cy(0) : (cy(0) < 0 ? 0 : H))
    : cy;
  const yAxisPx = (typeof cx === 'function')
    ? (cx(0) >= 0 && cx(0) <= W ? cx(0) : (cx(0) < 0 ? 0 : W))
    : cx;
  ctx.font = 'bold 12px JetBrains Mono,monospace';
  const xLblW = Math.ceil(ctx.measureText(xLabel).width) + 8;
  const yLblW = Math.ceil(ctx.measureText(yLabel).width) + 8;
  // Generisches Default-Label überdecken (bedarfsorientiert tight)
  ctx.fillStyle = '#fff';
  ctx.fillRect(W - xLblW, xAxisPy - 19, xLblW - 2, 17);
  ctx.fillRect(yAxisPx + 2, 0, yLblW, 18);
  // Neu zeichnen
  ctx.fillStyle = '#374151';
  ctx.textAlign = 'right'; ctx.textBaseline = 'alphabetic';
  ctx.fillText(xLabel, W - 4, xAxisPy - 6);
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
    ctx.font = 'bold 12px JetBrains Mono,monospace';
    ctx.textAlign = 'center';
    // Label leicht über dem Pfeilkopf
    const lx = (px1 + px2) / 2 + (py2 < py1 ? 0 : 0);
    const ly = (py1 + py2) / 2 - 7;
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
