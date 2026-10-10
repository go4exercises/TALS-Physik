#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer den Trainer Bewegungsdiagramme
   (werkzeuge/bewegungsdiagramme.html).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   bdSelbsttest() auf. Diese prueft je Vorlage mit vielen Zufallswerten
   (reproduzierbar, fester Startwert):
     - Ort immer stetig, Geschwindigkeit ab Stufe 2 stetig
     - unabhaengig nachgerechnet: v ist die numerische Ableitung von s,
       a die von v; die Flaeche unter v (1000 Streifen je Sekunde) ist die Ortsaenderung
     - jede Achse hat ein Raster, auf dem alle Eckwerte liegen
     - Auswahl (Zuordnen und In Worten): vier Diagramme, genau eines richtig,
       jedes Fehlbild sichtbar verschieden vom richtigen und von den anderen,
       jedes mit Rueckmeldung
     - Beschreibung in Worten: jede Dauer und jede Geschwindigkeit steht darin
     - Ablesen: Soll gegen Steigung bzw. Flaeche der Kurven, richtige Antwort
       gilt, jedes Fehlbild (Wert statt Steigung, Kehrwert, Vorzeichen,
       Rechteck statt Trapez, nur Dreieck, ...) bekommt seine Diagnose
     - Eingabe- und Zahlformate

   Aufruf vom Repo-Root:
     node scripts/verify_bewegungsdiagramme.js           # 30 je Vorlage
     node scripts/verify_bewegungsdiagramme.js --gross   # 400 je Vorlage
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

const datei = path.join(__dirname, '..', 'werkzeuge', 'bewegungsdiagramme.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren; BD_TEST haelt die Oberflaeche aus dem Test heraus.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('bdSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit bdSelbsttest() nicht gefunden');
  process.exit(1);
}

try {
  dom.window.eval('window.BD_TEST = true;\n' + skripte[0].textContent);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const gross = process.argv.indexOf('--gross') !== -1;
const proSzene = gross ? 400 : 30;
const t0 = Date.now();
const ergebnis = dom.window.eval('bdSelbsttest(' + proSzene + ')');
console.log('Bewegungsdiagramme: ' + ergebnis.vorlagen + ' Vorlagen, ' + proSzene + ' Aufgaben je Vorlage, ' +
            ergebnis.faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  if (ergebnis.fehler.length > 25) console.error('   … und ' + (ergebnis.fehler.length - 25) + ' weitere');
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
