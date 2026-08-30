// build-bilder.mjs — erzeugt die Bild-Assets fuer die Auffindbarkeit:
//   favicon-32.png (32x32), apple-touch-icon.png (180x180)  aus favicon.svg
//   og-bild.png (1200x630)                                   aus der Vorlage unten
//
// Aufruf vom Repo-Root (Chromium kommt aus playwright):
//   node .claude/tools/build-bilder.mjs
//
// Laeuft nur bei Bedarf — die PNGs sind versioniert und aendern sich nur, wenn
// Farben, Wortlaut, Adresse oder Schrift der Vorlage angepasst werden. Vorher
// entstanden sie von Hand; darum stand im OG-Bild nach dem Domain-Umzug noch
// die alte Adresse. Farben sind die Projektvariablen aus style.css.
// Die Schriften kommen von Google Fonts (wie auf den Seiten selbst), das
// Skript braucht also einmalig eine Netzverbindung.

import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const REPO = process.cwd();
const svg = readFileSync(resolve(REPO, 'favicon.svg'), 'utf8');

const FONTS = 'https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,700&family=JetBrains+Mono:wght@400;700&display=swap';

// Projektfarben (style.css): --papier, --tinte, --tinte-2, --bernstein
const OG = `<!doctype html><html><head><meta charset="utf-8">
<link href="${FONTS}" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1200px; height:630px; background:#f8f6f1; font-family:'Source Serif 4',serif;
         display:flex; align-items:center; }
  .balken { width:22px; height:100%; background:#8a4a0e; }
  .inhalt { padding:0 70px; }
  /* 25px/1.6 statt 26px/1.9: bei 26px misst die Zeile 1033 von 1038 verfuegbaren
     Pixeln — im handgebauten Vorgaengerbild brach «TALS» darum auf eine zweite
     Zeile um. Etwas kleiner haelt sie stabil einzeilig. */
  .ew  { font-family:'JetBrains Mono',monospace; font-size:25px; letter-spacing:1.6px;
         color:#5a5040; margin-bottom:30px; line-height:1.45; }
  .ew b { color:#8a4a0e; font-weight:700; }
  h1   { font-size:104px; font-weight:700; line-height:1.06; color:#1c1a17; }
  h1 span { color:#8a4a0e; }   /* laeuft im Fluss weiter, kein Zeilenumbruch erzwungen */
  .ut  { font-size:34px; color:#5a5040; margin-top:36px; line-height:1.35; }
  .url { font-family:'JetBrains Mono',monospace; font-size:23px; color:#5a5040; margin-top:32px; }
</style></head><body>
<div class="balken"></div>
<div class="inhalt">
  <div class="ew">Berufsmaturität <b>T</b>echnik, <b>A</b>rchitektur, <b>L</b>ife <b>S</b>ciences — <b>TALS</b></div>
  <h1>Physik <span>nach BM RLP 2030</span></h1>
  <div class="ut">Interaktives Lehrmittel mit Animationen, Aufgaben und Formelsammlung</div>
  <div class="url">physik.begreifbar.ch · CC BY-NC 4.0</div>
</div>
</body></html>`;

const IKON = (px) => `<!doctype html><html><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; } html,body { width:${px}px; height:${px}px; }
  svg { width:${px}px; height:${px}px; display:block; }
</style></head><body>${svg}</body></html>`;

const browser = await chromium.launch();

for (const [datei, px] of [['favicon-32.png', 32], ['apple-touch-icon.png', 180]]) {
  const ctx = await browser.newContext({ viewport: { width: px, height: px }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.setContent(IKON(px));
  await page.screenshot({ path: resolve(REPO, datei), omitBackground: false });
  await ctx.close();
  console.log(`  ${datei.padEnd(22)} ${px}x${px}`);
}

{
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.setContent(OG, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // Kontrolle: die Schrift muss wirklich geladen sein, sonst faellt das Bild
  // stillschweigend auf eine Systemschrift zurueck.
  const ok = await page.evaluate(() => document.fonts.check("700 104px 'Source Serif 4'"));
  if (!ok) { console.error('FEHLER: Source Serif 4 nicht geladen — Netzverbindung?'); process.exit(1); }
  await page.screenshot({ path: resolve(REPO, process.env.OG_ZIEL || 'og-bild.png') });
  await ctx.close();
  console.log(`  ${process.env.OG_ZIEL || 'og-bild.png'}            1200x630`);
}

await browser.close();
console.log('Bild-Assets geschrieben.');
