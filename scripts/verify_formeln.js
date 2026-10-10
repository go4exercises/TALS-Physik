#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer den Trainer Formeln umstellen
   (werkzeuge/formeln-umstellen.html).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   fuSelbsttest() auf. Diese prueft je Formel und gesuchte Groesse:
     - die Formel selbst ist einheitenrichtig (Dimension jedes Summanden)
     - die gesuchte Groesse kommt genau einmal vor; der Weg endet mit ihr
       allein auf einer Seite, in hoechstens sechs Schritten
     - unabhaengig: mit Zufallszahlen eingesetzt erfuellt die Loesung die
       Ausgangsformel, und jeder Zwischenstand bleibt eine wahre Gleichung
     - die Einheitenprobe der Loesung ergibt die Einheit der Groesse
     - jeder Schritt hat falsche Alternativen mit Diagnose, keine sieht
       aus wie der richtige
     - Aufgabe 2: vier verschiedene Umstellungen zur Auswahl; das Soll aus
       den angezeigten Zahlen erfuellt die Formel; richtige Zahl gilt, jede
       falsche Umstellung gibt ihre Diagnose
     - TeX mit geschlossenen Klammern, Eingabe- und Zahlformate

   Aufruf vom Repo-Root:
     node scripts/verify_formeln.js           # 20 Zahlensaetze je Aufgabe
     node scripts/verify_formeln.js --gross   # 200
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

const datei = path.join(__dirname, '..', 'werkzeuge', 'formeln-umstellen.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren; FU_TEST haelt die Oberflaeche aus dem Test heraus.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('fuSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit fuSelbsttest() nicht gefunden');
  process.exit(1);
}

try {
  dom.window.eval('window.FU_TEST = true;\n' + skripte[0].textContent);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const gross = process.argv.indexOf('--gross') !== -1;
const proSzene = gross ? 200 : 20;
const t0 = Date.now();
const ergebnis = dom.window.eval('fuSelbsttest(' + proSzene + ')');
console.log('Formeln umstellen: ' + ergebnis.formeln + ' Formeln, ' + ergebnis.aufgaben + ' Aufgaben, ' + proSzene + ' Zahlensaetze je Aufgabe, ' +
            ergebnis.faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  if (ergebnis.fehler.length > 25) console.error('   … und ' + (ergebnis.fehler.length - 25) + ' weitere');
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
