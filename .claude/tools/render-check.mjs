#!/usr/bin/env node
/**
 * render-check.mjs — Render-Kontrolle der Themenseiten bei 1280 und 360 px.
 *
 * Prueft, was der Pre-Flight prinzipiell nicht pruefen kann: jsdom hat kein
 * Layout, MathJax-SVG-Breiten existieren dort nicht. Hier laeuft ein echter
 * Chromium, MathJax rendert, danach wird gemessen.
 *
 * Drei Befunde:
 *   1. OVERFLOW   — die Seite laesst sich seitlich ziehen: window.scrollX
 *                   aendert sich nach scrollTo(9999, y). Frueher body.scrollWidth
 *                   gegen clientWidth — unter `html { zoom: 0.9 }` (style.css ab
 *                   1100 px) rechnet body.scrollWidth in Seiten-px (1422 bei
 *                   1280 px Fenster) und meldete falschen Ueberlauf. Die Zahlen
 *                   in der Ausgabe sind documentElement.scrollWidth/clientWidth
 *                   (im Standardmodus Bildschirm-px, auch unter zoom).
 *   2. GECLIPPT   — Formel/Tabelle ragt hinaus UND ein Vorfahr hat overflow:hidden.
 *                   Das ist der gefaehrliche Fall: unsichtbar, weil .page-wrap
 *                   unter 900 px kappt — der Inhalt fehlt einfach.
 * Alle <details> werden vor der Messung geoeffnet — die Mini-Check-Loesungen
 * sind sonst zu und ihre Formeln ungemessen. Achtung: minicheck.js ist ein
 * Akkordeon und laesst hoechstens ein details.minicheck offen. Ein blosses
 * «alle oeffnen» klappt sich also selbst wieder zu und misst pro Seite nur
 * einen Mini-Check. Deshalb wird jeder einzeln geoeffnet und gemessen.
 *
 * Dazu ein Vorher/Nachher-Vergleich fuer Eingriffe an der Formel-Darstellung:
 * overflow != visible auf einem inline-block verschiebt dessen Baseline. Ein
 * Absolutwert sagt darueber nichts (mehrzeilige Elternelemente verrauschen ihn),
 * die Differenz gegen einen frueheren Stand dagegen schon.
 *
 * Aufruf (vom Repo-Root):
 *   npm run render-check                 alle Themenseiten
 *   node .claude/tools/render-check.mjs themen/p4-3-energie.html
 *   node .claude/tools/render-check.mjs --shots            zusaetzlich check_*.png
 *   node .claude/tools/render-check.mjs --snapshot vorher.json    Geometrie sichern
 *   node .claude/tools/render-check.mjs --vergleich vorher.json   dagegen pruefen
 *   node .claude/tools/render-check.mjs --breiten 1280x720,1100x800 index.html
 *                                         andere Fenstermasse (Standard 1280x900, 360x900)
 *
 * Masse: getBoundingClientRect() liefert Bildschirm-px, offsetWidth und
 * body.scrollWidth Seiten-px; unter zoom 0.9 unterscheiden sie sich um den
 * Faktor 0.9. Verglichen werden Rechtecke darum mit documentElement.clientWidth,
 * das auch unter zoom in Bildschirm-px zaehlt.
 *
 * Exit-Code 1, sobald Overflow oder geclippter Inhalt gefunden wird.
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const argv = process.argv.slice(2);
const shots = argv.includes('--shots');
const flagWert = (name) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : null; };
const snapshotZiel = flagWert('--snapshot');
const vergleichQuelle = flagWert('--vergleich');
const breitenArg = flagWert('--breiten');
const dateien = argv.filter((a, i) =>
  !a.startsWith('--') && !['--snapshot', '--vergleich', '--breiten'].includes(argv[i - 1]));
const root = process.cwd();

const seiten = dateien.length
  ? dateien.map(f => path.relative(root, path.resolve(root, f)))
  : fs.readdirSync(path.join(root, 'themen'))
      .filter(f => f.endsWith('.html')).sort().map(f => 'themen/' + f);

const BREITEN = (breitenArg || '1280x900,360x900').split(',').map(t => {
  const [w, h] = t.split('x').map(Number);
  return { w, h: h || 900 };
});

/* Im Seitenkontext: alles messen, was nicht umbrechen kann.
   mcIndex begrenzt die Messung auf einen einzelnen Mini-Check — sonst wuerde
   der uebrige Seiteninhalt bei jedem Durchgang erneut gezaehlt. */
function messen(mcIndex) {
  const de = document.documentElement;
  const zoom = parseFloat(getComputedStyle(de).zoom) || 1;
  // Ueberlauf: laesst sich die Seite seitlich rollen? Unabhaengig von zoom.
  const sy = window.scrollY;
  window.scrollTo(9999, sy);
  const rollt = window.scrollX > 0;
  window.scrollTo(0, sy);
  // Vergleichsbreite in Bildschirm-px wie getBoundingClientRect. Im
  // Standardmodus liefert documentElement.clientWidth schon Bildschirm-px
  // (Fenster ohne Rollbalken), body.clientWidth dagegen Seiten-px (1422 bei
  // 1280 px Fenster und zoom 0.9). innerWidth faengt den Quirks-Modus ab.
  const cw = Math.min(de.clientWidth, window.innerWidth);
  const befund = { sw: de.scrollWidth, cw: de.clientWidth, rollt, zoom, geclippt: [], geometrie: [] };
  const wurzel = mcIndex == null
    ? document.querySelector('main') || document.body
    : document.querySelectorAll('details.minicheck')[mcIndex];
  if (!wurzel) return befund;

  for (const e of wurzel.querySelectorAll('mjx-container, table, pre, img')) {
    if (e.closest('mjx-assistive-mml')) continue;   // unsichtbare Screenreader-Kopie
    /* Chromium legt den Inhalt eines geschlossenen <details> bereits aus (fuer
       Suchen-auf-der-Seite). Im Seiten-Durchgang wuerden die Mini-Checks damit
       doppelt gezaehlt — sie kommen weiter unten einzeln und im geoeffneten
       Zustand dran. */
    if (mcIndex == null && e.closest('details.minicheck')) continue;
    const b = e.getBoundingClientRect();
    if (b.width === 0 || b.right <= cw + 1) continue;

    let a = e.parentElement, kappt = null;
    while (a) {
      const ov = getComputedStyle(a).overflowX;
      if (ov === 'hidden' || ov === 'clip') { kappt = a.tagName.toLowerCase() + '.' + String(a.className).split(' ')[0]; break; }
      if (ov === 'auto' || ov === 'scroll') break;   // scrollt in sich selbst — in Ordnung
      a = a.parentElement;
    }
    if (kappt) befund.geclippt.push({
      ueber: Math.round(b.right - cw), kappt,
      txt: (e.textContent || '').replace(/\s+/g, ' ').slice(0, 60)
    });
  }

  /* Lage jeder Inline-Formel relativ zu ihrem Elternelement — als Vergleichsbasis.
     Absolut ist der Wert nichtssagend, die Differenz gegen einen frueheren Stand
     zeigt dagegen genau, ob ein CSS-Eingriff die Formeln verschoben hat. */
  let i = 0;
  for (const e of wurzel.querySelectorAll('mjx-container:not([display="true"])')) {
    const p = e.parentElement;
    if (!p || e.closest('mjx-assistive-mml')) continue;
    if (mcIndex == null && e.closest('details.minicheck')) continue;
    const b = e.getBoundingClientRect(), pb = p.getBoundingClientRect();
    if (b.height === 0) continue;
    befund.geometrie.push({
      k: i++ + '|' + (e.textContent || '').replace(/\s+/g, '').slice(0, 24),
      dy: Math.round((b.top - pb.top) * 10) / 10,
      h: Math.round(b.height * 10) / 10
    });
  }
  return befund;
}

const alt = vergleichQuelle ? JSON.parse(fs.readFileSync(vergleichQuelle, 'utf8')) : null;
const neu = {};

const browser = await chromium.launch();
let fehler = 0, geclipptGes = 0, verschobenGes = 0;

for (const { w: breite, h: hoehe } of BREITEN) {
  const ctx = await browser.newContext({ viewport: { width: breite, height: hoehe } });
  console.log(`\n════ ${breite}×${hoehe} px ${'═'.repeat(48)}`);

  for (const s of seiten) {
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(root, s));
    await page.waitForTimeout(1000);

    /* Erst alles ausser den Mini-Check-Akkordeons oeffnen (Loesungswege,
       Herleitungen). Die bleiben offen, das Akkordeon greift nur auf
       details.minicheck. */
    await page.evaluate(() => document.querySelectorAll('details:not(.minicheck)')
      .forEach(d => (d.open = true)));
    await page.waitForTimeout(1500);

    const r = await page.evaluate(messen, null);

    /* Dann jeden Mini-Check einzeln — das Akkordeon schliesst den vorigen. */
    const anzahlMc = await page.evaluate(() => document.querySelectorAll('details.minicheck').length);
    for (let i = 0; i < anzahlMc; i++) {
      await page.evaluate(k => {
        const d = document.querySelectorAll('details.minicheck')[k];
        d.open = true;
        d.querySelectorAll('details').forEach(x => (x.open = true));
      }, i);
      await page.waitForTimeout(700);   // MathJax rendert das Aufgeklappte nach
      const t = await page.evaluate(messen, i);
      r.sw = Math.max(r.sw, t.sw);
      r.rollt = r.rollt || t.rollt;
      r.geclippt.push(...t.geclippt);
      r.geometrie.push(...t.geometrie.map(g => ({ ...g, k: 'mc' + i + '-' + g.k })));
    }
    const name = path.basename(s);
    const schluessel = (hoehe === 900 ? breite : breite + 'x' + hoehe) + ' ' + s;
    neu[schluessel] = r.geometrie;

    /* Verschiebungen gegen den gesicherten Stand */
    const verschoben = [];
    if (alt && alt[schluessel]) {
      const vorher = new Map(alt[schluessel].map(g => [g.k, g]));
      for (const g of r.geometrie) {
        const v = vorher.get(g.k);
        if (v && Math.abs(g.dy - v.dy) > 1) verschoben.push({ k: g.k, von: v.dy, auf: g.dy });
      }
    }

    const ok = !r.rollt && r.geclippt.length === 0 && verschoben.length === 0;
    const zz = r.zoom !== 1 ? ` zoom=${r.zoom}` : '';
    console.log(`${ok ? '  ok  ' : '  !!  '}${name.padEnd(40)} scrollWidth=${r.sw} clientWidth=${r.cw}${zz}`);

    if (r.rollt) { console.log(`        OVERFLOW ${r.sw - r.cw} px (seitlich rollbar)`); fehler++; }
    for (const g of r.geclippt) {
      console.log(`        GECLIPPT ${String(g.ueber).padStart(3)} px von ${g.kappt}  « ${g.txt} »`);
      geclipptGes++; fehler++;
    }
    for (const v of verschoben.slice(0, 5)) {
      console.log(`        VERSCHOBEN ${v.von} → ${v.auf} px  « ${v.k.split('|')[1]} »`);
    }
    if (verschoben.length > 5) console.log(`        … und ${verschoben.length - 5} weitere`);
    verschobenGes += verschoben.length;
    if (shots) await page.screenshot({ path: `check_${name.replace(/\.html$/, '')}_${breite}.png`, fullPage: true });
    await page.close();
  }
  await ctx.close();
}
await browser.close();

if (snapshotZiel) {
  fs.writeFileSync(snapshotZiel, JSON.stringify(neu));
  console.log(`\nGeometrie gesichert: ${snapshotZiel}`);
}

console.log('\n' + '─'.repeat(70));
console.log(`geclippte Formeln/Tabellen: ${geclipptGes}`);
if (alt) console.log(`vertikal verschobene Inline-Formeln: ${verschobenGes}`);
console.log(fehler === 0 ? 'RENDER-CHECK BESTANDEN' : `RENDER-CHECK FEHLGESCHLAGEN (${fehler} Befunde)`);
process.exit(fehler === 0 ? 0 : 1);
