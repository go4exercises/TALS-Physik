#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer den Trainer Schaltungen zusammenfassen
   (werkzeuge/schaltungen-zusammenfassen.html).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   szSelbsttest() auf. Diese prueft je Bauform mit vielen Zufallswerten
   (reproduzierbar, fester Startwert):
     - Baum normal (keine Reihe in der Reihe, keine Parallelgruppe in der
       Parallelgruppe), Werte aus der Liste, Nummern in Lesereihenfolge
     - R_ges, jeder Schritt des Rueckwegs und das Ergebnis am Ziel gegen
       eine unabhaengige Knotenpotential-Rechnung (Gauss) auf der Netzliste
       des Schaltbilds
     - jedes Paar von Widerstaenden in jedem Zwischenstand: «in Reihe» ist
       genau dann richtig, wenn derselbe Strom fliesst (zwei Wertesaetze),
       «parallel» genau dann, wenn beide an denselben zwei Knoten haengen;
       jede falsche Wahl bekommt einen Text
     - Ersatzwiderstand und Rueckweg: richtige und gerundete Antworten
       gelten, jedes Fehlerbild (parallel addiert, Kehrwert, Produkt,
       ganze Spannung, Gesamtstrom, Stromteilung vertauscht, mA/A, mV/V)
       bekommt seine Diagnose
     - Proben gehen auf, Zusammenfassen in beliebiger Reihenfolge ergibt R_ges
     - Schaltbild bei 300, 380 und 1000 px: Beschriftungen im Bild, ohne
       Ueberlappung untereinander, mit Leitungen oder Widerstaenden
     - Eingabeformate (Punkt, Komma, Einheit, Tausender-Apostroph)

   Aufruf vom Repo-Root:
     node scripts/verify_schaltungen.js           # 30 Aufgaben je Bauform
     node scripts/verify_schaltungen.js --gross   # 400 je Bauform
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

const datei = path.join(__dirname, '..', 'werkzeuge', 'schaltungen-zusammenfassen.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren; SZ_TEST haelt die Oberflaeche aus dem Test heraus.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('szSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit szSelbsttest() nicht gefunden');
  process.exit(1);
}

try {
  dom.window.eval('window.SZ_TEST = true;\n' + skripte[0].textContent);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const gross = process.argv.indexOf('--gross') !== -1;
const proSzene = gross ? 400 : 30;
const t0 = Date.now();
const ergebnis = dom.window.eval('szSelbsttest(' + proSzene + ')');
console.log('Schaltungen zusammenfassen: ' + ergebnis.vorlagen + ' Bauformen, ' + proSzene + ' Aufgaben je Bauform, ' +
            ergebnis.faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  if (ergebnis.fehler.length > 25) console.error('   … und ' + (ergebnis.fehler.length - 25) + ' weitere');
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
