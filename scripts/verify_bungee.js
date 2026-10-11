#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer die Simulation Bungee-Sprung
   (simulationen/bungee-sprung.html).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   bjSelbsttest() auf. Sie prueft:
     - lineares Seil ohne Daempfung (27 Kombinationen von m, L0, D):
       tiefster Punkt und groesste Geschwindigkeit gegen die Energiebilanz,
       Gleichgewichtslage s_G = L0 + m g / D, t1 = Wurzel(2 L0 / g),
       Phasen in der Reihenfolge, mechanische Energie auf 0.5 % erhalten,
       Beschleunigung am tiefsten Punkt
     - Latexseil (Gent-Modell): Energie erhalten, s_G erfuellt F_el = m g,
       angenommene Eichung bei 75 kg (Dehnung 2, Spitzenkraft 3 m g)
     - Daempfung: E_diss nie negativ und nie abnehmend, E_mech sinkt,
       das Seil drueckt nie
     - Zahlformat (Dezimalpunkt) und Phasentexte (Energieaussage je nach c)

   Aufruf vom Repo-Root:  node scripts/verify_bungee.js
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

const datei = path.join(__dirname, '..', 'simulationen', 'bungee-sprung.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren; BJ_TEST haelt die Oberflaeche aus dem Test heraus.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('bjSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit bjSelbsttest() nicht gefunden');
  process.exit(1);
}

try {
  dom.window.eval('window.BJ_TEST = true;\n' + skripte[0].textContent);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const t0 = Date.now();
const ergebnis = dom.window.eval('bjSelbsttest()');
console.log('Bungee-Sprung: ' + ergebnis.faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
