#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer den Trainer Freischneiden
   (werkzeuge/freischneiden.html).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   fsSelbsttest() auf. Diese prueft je Szene mit vielen Zufallswerten
   (reproduzierbar, fester Startwert):
     - Datensatz: nur echte Kraefte, Richtungen im 15°-Raster, Betraege
       endlich und positiv, Rechenweg ohne NaN und ohne Dezimalkomma
     - die Musterloesung gilt als richtig
     - Gleichgewicht bzw. Resultierende: die Vektorsumme der Musterkraefte
       passt zur richtigen Antwort auf die Frage nach F_res (Richtung und
       Betrag, exakt gerechnet, unabhaengig von der Anzeige)
     - jede Antwort auf die Frage nach F_res hat eine passende Rueckmeldung
     - die Startrichtung einer neuen Kraft ist nie schon richtig
     - typische Fehler bekommen die richtige Diagnose: Gewicht fehlt oder
       zeigt falsch, Fallen (Bewegungs-, Hangabtriebs-, Zentrifugalkraft,
       Kraft auf die Unterlage), Normalkraft fehlt, umgekehrt, lotrecht auf
       der Rampe, ohne Unterlage; Reibung fehlt, umgekehrt, quer, ohne Grund;
       Seil schiebt, schief, zu viel, fehlt; Feder fehlt, drueckt, ohne Feder

   Aufruf vom Repo-Root:
     node scripts/verify_freischneiden.js           # 40 Aufgaben je Szene
     node scripts/verify_freischneiden.js --gross   # 1000 je Szene
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

const datei = path.join(__dirname, '..', 'werkzeuge', 'freischneiden.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren; FS_TEST haelt die Oberflaeche aus dem Test heraus.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('fsSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit fsSelbsttest() nicht gefunden');
  process.exit(1);
}

try {
  dom.window.eval('window.FS_TEST = true;\n' + skripte[0].textContent);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const gross = process.argv.indexOf('--gross') !== -1;
const proSzene = gross ? 1000 : 40;
const t0 = Date.now();
const ergebnis = dom.window.eval('fsSelbsttest(' + proSzene + ')');
console.log('Freischneiden: ' + ergebnis.szenen + ' Szenen, ' + proSzene + ' Aufgaben je Szene, ' +
            ergebnis.faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  if (ergebnis.fehler.length > 25) console.error('   … und ' + (ergebnis.fehler.length - 25) + ' weitere');
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
