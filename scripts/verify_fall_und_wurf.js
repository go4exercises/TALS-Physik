#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer den Trainer Fall und Wurf
   (werkzeuge/fall-und-wurf.html).

   Laedt die Seite in jsdom und ruft die dort definierte Funktion
   fwSelbsttest() auf. Diese prueft je Bewegung (freier Fall, senkrecht
   nach oben und unten, waagrechter und schiefer Wurf) mit vielen
   Zufallswerten (reproduzierbar, fester Startwert):
     - unabhaengig nachgerechnet: Start in h0, Aufprall bei y = 0, nie
       vorher unter dem Boden; v_y ist die numerische Ableitung von y,
       a_y = -g; Energie v_x^2 + v_yF^2 = v0^2 + 2 g h0; Flaeche unter v_y
       (4000 Streifen) = -h0; Scheitel = groesstes y; Wurfweite vom Boden
       = v0^2 sin(2 alpha) / g; waagrecht: Flugzeit = Fallzeit
     - Zuordnen: vier Diagramme, genau eines richtig, jedes Fehlbild
       sichtbar verschieden vom richtigen und von den anderen, jedes mit
       Rueckmeldung; Rechenweg ohne NaN und Dezimalkomma
     - Stellen finden: jede Loesung erfuellt die Frage (hoechster Punkt,
       v_y = 0, groesster/kleinster Betrag, wieder auf Abwurfhoehe, halbe
       Hoehe, halbe Weite), wird angenommen; jede typische falsche Stelle
       und jeder falsche Knopf bekommt seine Diagnose
     - Ablesen: Soll unabhaengig nachgerechnet (Nullstelle, Flaeche,
       Steigung), richtige Antwort und Ablesefehler bis 0.9 Toleranz
       gelten, jedes Fehlbild bekommt seine Diagnose, die gesuchte Groesse
       steht nicht im Aufgabentext
     - Eingabe- und Zahlformate

   Aufruf vom Repo-Root:
     node scripts/verify_fall_und_wurf.js           # 30 je Bewegung
     node scripts/verify_fall_und_wurf.js --gross   # 400 je Bewegung
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

const datei = path.join(__dirname, '..', 'werkzeuge', 'fall-und-wurf.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

// Nur das Seitenskript ausfuehren; FW_TEST haelt die Oberflaeche aus dem Test heraus.
const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });

const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('fwSelbsttest') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit fwSelbsttest() nicht gefunden');
  process.exit(1);
}

try {
  dom.window.eval('window.FW_TEST = true;\n' + skripte[0].textContent);
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}

const gross = process.argv.indexOf('--gross') !== -1;
const proWurf = gross ? 400 : 30;
const t0 = Date.now();
const ergebnis = dom.window.eval('fwSelbsttest(' + proWurf + ')');
console.log('Fall und Wurf: ' + ergebnis.wuerfe + ' Bewegungen, ' + proWurf + ' Szenen je Bewegung, ' +
            ergebnis.faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');

if (ergebnis.fehler.length) {
  console.error('[FEHLER] ' + ergebnis.fehler.length + ' Testfaelle fehlgeschlagen:');
  ergebnis.fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  if (ergebnis.fehler.length > 25) console.error('   … und ' + (ergebnis.fehler.length - 25) + ' weitere');
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
