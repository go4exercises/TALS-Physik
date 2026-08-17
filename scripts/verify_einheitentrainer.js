#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer den Einheitentrainer (themen/p0-4).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   etSelbsttest() auf. Diese prueft:
     - jedes Einheitenpaar hin und zurueck (Rundreise-Toleranz)
     - feste Referenzwerte aus dem Lehrmittel (m/km, m²/cm², kWh/J, °C/K …)
     - keine NaN-/Infinity-Werte, keine negativen Kelvinwerte
     - den Aufgabengenerator (lesbare Zahlen, keine Rundungsartefakte)
     - die Antworttoleranz (richtig ja, Faktor 10 nein)
     - die Eingabeformate (Punkt, Komma, e-Notation, 10^-Schreibweise)
     - die Fehlerdiagnose-Kategorien

   Aufruf vom Repo-Root:  node scripts/verify_einheitentrainer.js
   Exit 0 = alles gruen, Exit 1 = mindestens ein Fehler.
   ───────────────────────────────────────────────────────────── */

const fs = require('fs');
const path = require('path');

let JSDOM;
try {
  ({ JSDOM } = require('jsdom'));
} catch (e) {
  console.log('jsdom fehlt — `npm install jsdom`. Test uebersprungen.');
  process.exit(0);
}

const datei = path.join(__dirname, '..', 'themen', 'p0-4-einheitentrainer.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren: die externen Skripte (nav.js, MathJax) bleiben
// aussen vor, damit der Test ohne Netz und ohne Navigationsgeruest laeuft.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('etSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit etSelbsttest() nicht gefunden');
  process.exit(1);
}

// buildNav ist im Test nicht vorhanden — durch eine leere Funktion ersetzen.
const quelle = 'window.buildNav = function(){};\n' + skripte[0].textContent;
try {
  dom.window.eval(quelle);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const ergebnis = dom.window.eval('etSelbsttest()');
console.log('Einheitentrainer: ' + ergebnis.paare + ' Einheitenpaare, ' +
            ergebnis.faelle + ' Umrechnungsfaelle geprueft');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  if (ergebnis.fehler.length > 25) console.error('   … und ' + (ergebnis.fehler.length - 25) + ' weitere');
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
