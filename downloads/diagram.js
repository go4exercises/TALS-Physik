/* ═══════════════════════════════════════════════════════════
   TALS-Mathematik · Druck-Diagramme
   SVG-Helper für Achsenkreuze und Geraden in Druckseiten.
   Druckt sauber und skalierbar (auch ohne Browser-JS rendert
   das SVG, weil hier keine JS-Manipulation passiert).
   ═══════════════════════════════════════════════════════════ */

window.TalsDiagram = (function () {
  /**
   * Erzeugt ein SVG-Achsenkreuz und eine Liste von Geraden/Punkten.
   * Wird in DOM-Container <div data-diagram="..."> eingebaut.
   *
   * @param {Object} cfg
   * @param {number[]} cfg.xRange  [xMin, xMax]
   * @param {number[]} cfg.yRange  [yMin, yMax]
   * @param {number}   cfg.xTick   Schrittweite x-Achse
   * @param {number}   cfg.yTick   Schrittweite y-Achse
   * @param {string}   [cfg.xLabel='x']  Achsenbeschriftung x
   * @param {string}   [cfg.yLabel='y']  Achsenbeschriftung y
   * @param {number}   [cfg.width=420]   SVG-Breite in px (Bildschirm)
   * @param {number}   [cfg.height=300]  SVG-Höhe in px (Bildschirm)
   * @param {boolean}  [cfg.square=false] 1:1-Skalierung erzwingen
   * @param {Array}    [cfg.lines=[]]    [{m, b, color, label}, ...]   Geraden y = m·x + b
   * @param {Array}    [cfg.segments=[]] [{x1,y1,x2,y2,color,label,dashed}, ...]   freie Strecken
   * @param {Array}    [cfg.curves=[]]   [{fn, color, label, labelX, dashed, xFrom, xTo}, ...]   beliebige Funktionen y = fn(x)
   * @param {Array}    [cfg.points=[]]   [{x,y,label,color,labelPos}, ...]
   * @param {Array}    [cfg.markers=[]]  [{x,y,label,color}, ...] = Achsen-Marker (mit gestrichelten Linien)
   * @returns {string} SVG-String
   */
  function build(cfg) {
    const {
      xRange, yRange, xTick, yTick,
      xLabel = 'x', yLabel = 'y',
      width = 420, height = 300,
      square = false,
      lines = [], segments = [], curves = [], points = [], markers = [],
      title = '',
    } = cfg;

    // Innenränder für Achsen-Beschriftung
    const padL = 38, padR = 14, padT = 14, padB = 32;

    // Sichtbare Plot-Fläche
    let plotW = width - padL - padR;
    let plotH = height - padT - padB;

    const xMin = xRange[0], xMax = xRange[1];
    const yMin = yRange[0], yMax = yRange[1];

    // Bei 1:1 (reine Mathematik) gleiche Pixel pro Einheit
    let sx = plotW / (xMax - xMin);
    let sy = plotH / (yMax - yMin);
    if (square) {
      const s = Math.min(sx, sy);
      sx = sy = s;
      plotW = sx * (xMax - xMin);
      plotH = sy * (yMax - yMin);
    }

    // Welt → SVG
    const X = x => padL + (x - xMin) * sx;
    const Y = y => padT + (yMax - y) * sy;

    const out = [];
    out.push(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" ` +
      `style="width:100%;max-width:${width}px;height:auto;font-family:'JetBrains Mono','Courier New',monospace;font-size:9pt">`
    );

    // ── Hintergrund ──
    out.push(
      `<rect x="${padL}" y="${padT}" width="${plotW}" height="${plotH}" ` +
      `fill="#ffffff" stroke="#c8c8c8" stroke-width="0.6"/>`
    );

    // ── Gitter ──
    out.push('<g stroke="#e5e5e5" stroke-width="0.4">');
    for (let v = Math.ceil(xMin / xTick) * xTick; v <= xMax + 1e-9; v += xTick) {
      if (Math.abs(v) < 1e-9) continue;
      const px = X(v);
      out.push(`<line x1="${px}" y1="${padT}" x2="${px}" y2="${padT + plotH}"/>`);
    }
    for (let v = Math.ceil(yMin / yTick) * yTick; v <= yMax + 1e-9; v += yTick) {
      if (Math.abs(v) < 1e-9) continue;
      const py = Y(v);
      out.push(`<line x1="${padL}" y1="${py}" x2="${padL + plotW}" y2="${py}"/>`);
    }
    out.push('</g>');

    // ── Achsen (durch Ursprung, falls im Bereich, sonst am Rand) ──
    const x0 = Math.max(xMin, Math.min(xMax, 0));
    const y0 = Math.max(yMin, Math.min(yMax, 0));
    const axX = X(x0), axY = Y(y0);

    out.push('<g stroke="#1a1a1a" stroke-width="0.9" fill="none">');
    out.push(`<line x1="${padL}" y1="${axY}" x2="${padL + plotW}" y2="${axY}"/>`);
    out.push(`<line x1="${axX}" y1="${padT}" x2="${axX}" y2="${padT + plotH}"/>`);
    // Pfeilspitzen
    out.push(`<polygon points="${padL + plotW},${axY} ${padL + plotW - 5},${axY - 3} ${padL + plotW - 5},${axY + 3}" fill="#1a1a1a"/>`);
    out.push(`<polygon points="${axX},${padT} ${axX - 3},${padT + 5} ${axX + 3},${padT + 5}" fill="#1a1a1a"/>`);
    out.push('</g>');

    // ── Tick-Beschriftung ──
    out.push('<g fill="#1a1a1a" stroke="none">');
    for (let v = Math.ceil(xMin / xTick) * xTick; v <= xMax + 1e-9; v += xTick) {
      if (Math.abs(v) < 1e-9) continue;
      const px = X(v);
      out.push(`<line x1="${px}" y1="${axY - 3}" x2="${px}" y2="${axY + 3}" stroke="#1a1a1a" stroke-width="0.7"/>`);
      out.push(`<text x="${px}" y="${axY + 13}" text-anchor="middle" font-size="8.5">${fmt(v)}</text>`);
    }
    for (let v = Math.ceil(yMin / yTick) * yTick; v <= yMax + 1e-9; v += yTick) {
      if (Math.abs(v) < 1e-9) continue;
      const py = Y(v);
      out.push(`<line x1="${axX - 3}" y1="${py}" x2="${axX + 3}" y2="${py}" stroke="#1a1a1a" stroke-width="0.7"/>`);
      out.push(`<text x="${axX - 6}" y="${py + 3}" text-anchor="end" font-size="8.5">${fmt(v)}</text>`);
    }
    // Ursprung 0
    if (xMin <= 0 && xMax >= 0 && yMin <= 0 && yMax >= 0) {
      out.push(`<text x="${X(0) - 6}" y="${Y(0) + 13}" text-anchor="end" font-size="8.5">0</text>`);
    }
    out.push('</g>');

    // ── Achsen-Beschriftung ──
    out.push(
      `<text x="${padL + plotW + 2}" y="${axY + 4}" font-size="9.5" font-style="italic" fill="#1a1a1a">${escape(xLabel)}</text>`
    );
    out.push(
      `<text x="${axX + 5}" y="${padT - 3}" font-size="9.5" font-style="italic" fill="#1a1a1a">${escape(yLabel)}</text>`
    );

    // ── Geraden ──
    const colorList = ['#1a4f8a', '#b85a00', '#2d6a3e', '#a02828', '#5e2d8a'];
    lines.forEach((ln, i) => {
      const color = ln.color || colorList[i % colorList.length];
      // Schneide an Plot-Rändern
      const pts = clipLine(ln.m, ln.b, xMin, xMax, yMin, yMax);
      if (!pts) return;
      const [x1, y1, x2, y2] = pts;
      out.push(
        `<line x1="${X(x1)}" y1="${Y(y1)}" x2="${X(x2)}" y2="${Y(y2)}" ` +
        `stroke="${color}" stroke-width="1.6" fill="none" ${ln.dashed ? 'stroke-dasharray="4 3"' : ''}/>`
      );
      if (ln.label) {
        // Label am rechten Ende
        const lx = X(x2) - 4, ly = Y(y2) - 4;
        out.push(
          `<text x="${lx}" y="${ly}" text-anchor="end" fill="${color}" font-size="9" font-weight="700">${escape(ln.label)}</text>`
        );
      }
    });

    // ── Strecken ──
    segments.forEach((sg, i) => {
      const color = sg.color || colorList[i % colorList.length];
      out.push(
        `<line x1="${X(sg.x1)}" y1="${Y(sg.y1)}" x2="${X(sg.x2)}" y2="${Y(sg.y2)}" ` +
        `stroke="${color}" stroke-width="1.6" fill="none" ${sg.dashed ? 'stroke-dasharray="4 3"' : ''}/>`
      );
      if (sg.label) {
        const mx = (X(sg.x1) + X(sg.x2)) / 2 + 6;
        const my = (Y(sg.y1) + Y(sg.y2)) / 2 - 6;
        out.push(`<text x="${mx}" y="${my}" fill="${color}" font-size="9" font-weight="700">${escape(sg.label)}</text>`);
      }
    });

    // ── Kurven (beliebige Funktionen y = fn(x), z.B. Parabeln) ──
    curves.forEach((cv, i) => {
      const color = cv.color || colorList[(lines.length + i) % colorList.length];
      const fn = cv.fn;
      if (typeof fn !== 'function') return;
      const xa = (cv.xFrom !== undefined) ? cv.xFrom : xMin;
      const xb = (cv.xTo   !== undefined) ? cv.xTo   : xMax;
      const N = 200;
      const dx = (xb - xa) / N;
      // Sammle Polylinie, breche bei out-of-range Werten in Segmente
      const segs = [];
      let cur = [];
      for (let k = 0; k <= N; k++) {
        const xv = xa + k * dx;
        const yv = fn(xv);
        if (!isFinite(yv) || yv < yMin - 1e-9 || yv > yMax + 1e-9) {
          if (cur.length > 1) segs.push(cur);
          cur = [];
          continue;
        }
        cur.push([X(xv), Y(yv)]);
      }
      if (cur.length > 1) segs.push(cur);
      segs.forEach((seg) => {
        const d = 'M ' + seg.map(p => p[0].toFixed(2) + ' ' + p[1].toFixed(2)).join(' L ');
        out.push(
          `<path d="${d}" stroke="${color}" stroke-width="1.6" fill="none" ` +
          `${cv.dashed ? 'stroke-dasharray="4 3"' : ''}/>`
        );
      });
      // Label: an cv.labelX, sonst am rechten Rand der Kurve
      if (cv.label && segs.length) {
        const lastSeg = segs[segs.length - 1];
        let lx, ly;
        if (cv.labelX !== undefined) {
          lx = X(cv.labelX);
          ly = Y(fn(cv.labelX)) - 6;
        } else {
          const last = lastSeg[lastSeg.length - 1];
          lx = last[0] - 4;
          ly = last[1] - 4;
        }
        out.push(
          `<text x="${lx}" y="${ly}" text-anchor="end" fill="${color}" font-size="9" font-weight="700">${escape(cv.label)}</text>`
        );
      }
    });


    markers.forEach((mk) => {
      const color = mk.color || '#1a4f8a';
      out.push(`<line x1="${X(mk.x)}" y1="${axY}" x2="${X(mk.x)}" y2="${Y(mk.y)}" stroke="${color}" stroke-width="0.8" stroke-dasharray="3 2"/>`);
      out.push(`<line x1="${axX}" y1="${Y(mk.y)}" x2="${X(mk.x)}" y2="${Y(mk.y)}" stroke="${color}" stroke-width="0.8" stroke-dasharray="3 2"/>`);
      out.push(`<circle cx="${X(mk.x)}" cy="${Y(mk.y)}" r="2.5" fill="${color}"/>`);
      if (mk.label) {
        out.push(`<text x="${X(mk.x) + 5}" y="${Y(mk.y) - 5}" fill="${color}" font-size="8.5" font-weight="700">${escape(mk.label)}</text>`);
      }
    });

    // ── Punkte ──
    points.forEach((p, i) => {
      const color = p.color || '#1a1a1a';
      out.push(`<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="2.6" fill="${color}"/>`);
      if (p.label) {
        const dx = (p.labelPos === 'l') ? -8 : 6;
        const dy = (p.labelPos === 't') ? -6 : 11;
        const ta = (p.labelPos === 'l') ? 'end' : 'start';
        out.push(`<text x="${X(p.x) + dx}" y="${Y(p.y) + dy}" text-anchor="${ta}" fill="${color}" font-size="9" font-weight="700">${escape(p.label)}</text>`);
      }
    });

    // ── Titel ──
    if (title) {
      out.push(`<text x="${padL + plotW / 2}" y="${padT - 2}" text-anchor="middle" font-size="9" font-weight="700" fill="#1a1a1a">${escape(title)}</text>`);
    }

    out.push('</svg>');
    return out.join('');
  }

  // Schneide Gerade y = m·x + b am Rechteck und gib zwei Endpunkte
  function clipLine(m, b, xMin, xMax, yMin, yMax) {
    const candidates = [];
    // Schnitte mit linker und rechter Seite
    const yL = m * xMin + b;
    const yR = m * xMax + b;
    if (yL >= yMin && yL <= yMax) candidates.push([xMin, yL]);
    if (yR >= yMin && yR <= yMax) candidates.push([xMax, yR]);
    // Schnitte mit Ober- und Unterkante (m≠0)
    if (Math.abs(m) > 1e-12) {
      const xT = (yMax - b) / m;
      const xB = (yMin - b) / m;
      if (xT >= xMin && xT <= xMax) candidates.push([xT, yMax]);
      if (xB >= xMin && xB <= xMax) candidates.push([xB, yMin]);
    }
    if (candidates.length < 2) return null;
    // Nimm äusserste zwei
    candidates.sort((a, b) => a[0] - b[0]);
    const p1 = candidates[0];
    const p2 = candidates[candidates.length - 1];
    return [p1[0], p1[1], p2[0], p2[1]];
  }

  function fmt(v) {
    if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
    // Wenige Nachkommastellen
    return (Math.round(v * 100) / 100).toString();
  }

  function escape(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /**
   * Inline-Builder: schreibt SVG sofort in alle <div data-diagram="ID"></div>,
   * wo ID auf eine globale Konfig zugreift in window.TalsDiagrams[ID].
   */
  function renderAll() {
    const containers = document.querySelectorAll('[data-diagram]');
    containers.forEach((el) => {
      const id = el.getAttribute('data-diagram');
      const cfg = (window.TalsDiagrams || {})[id];
      if (!cfg) {
        el.innerHTML = '<div style="color:#a02828;font-family:sans-serif;font-size:10pt">⚠ Diagramm-Konfig fehlt: ' + id + '</div>';
        return;
      }
      el.innerHTML = build(cfg);
    });
  }

  return { build, renderAll };
})();

// Auto-render beim DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function () { window.TalsDiagram.renderAll(); });
} else {
  window.TalsDiagram.renderAll();
}
