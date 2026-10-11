#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer die Simulation Bungee-Sprung
   (simulationen/bungee-sprung.html, Fassung des Auftraggebers).

   Laedt die Seite in jsdom, fuehrt das Seitenskript aus und prueft das
   Modell von aussen (die Seite selbst bleibt unveraendert):
     - lineares Seil ohne Daempfung (27 Kombinationen von m, L0, k):
       tiefster Punkt und groesste Geschwindigkeit gegen die Energiebilanz,
       Gleichgewichtslage s_G = L0 + m g / k, t1 = Wurzel(2 L0 / g),
       Phasenzeiten in der Reihenfolge t1 < t2 < t3, Energie E_tot auf
       0.5 % erhalten, Beschleunigung am tiefsten Punkt nach oben und
       groesser als g
     - Latexseil (Gent-Modell): Energie erhalten, s_G erfuellt F_el = m g,
       angenommene Eichung bei 75 kg (Dehnung 2, Spitzenkraft 3 m g)
     - Daempfung: E_diss nie negativ und nie abnehmend, E_tot sinkt,
       das Seil drueckt nie
     - Zahlformat mit Dezimalpunkt (fnum)

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

const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });
const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('function simulate') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit simulate() nicht gefunden');
  process.exit(1);
}
try {
  // Seitenskript laeuft im strikten Modus; seine Funktionen fuer den Test herausreichen
  dom.window.eval(skripte[0].textContent + '\n;window.__bjModell = { simulate, elasticForce, fnum };');
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}
const W = dom.window;
const { simulate, elasticForce, fnum } = W.__bjModell;
const g = 9.81;

const fehler = []; let faelle = 0;
const F = (ok, was) => { faelle++; if (!ok) fehler.push(was); };
const rel = (a, b) => Math.abs(a - b) / Math.max(1e-9, Math.abs(b));
const t0 = Date.now();

// 1. Lineares Seil ohne Daempfung gegen die Energiebilanz
for (const m of [50, 75, 110]) for (const L0 of [10, 20, 30]) for (const k of [30, 60, 150]) {
  const p = { m, L0, k, c: 0, mode: 'hooke' }, S = simulate(p), w = `m=${m} L0=${L0} k=${k}`, mg = m * g;
  const x = (mg + Math.sqrt(mg * mg + 2 * k * mg * L0)) / k;
  F(rel(S.sMax, L0 + x) < 2e-3, w + ': s_max ' + S.sMax + ' statt ' + (L0 + x));
  const vMax = Math.sqrt(2 * g * (L0 + mg / k) - k / m * (mg / k) * (mg / k));
  F(rel(S.vMax, vMax) < 2e-3, w + ': v_max ' + S.vMax + ' statt ' + vMax);
  F(rel(S.sG, L0 + mg / k) < 1e-6, w + ': s_G falsch');
  F(Math.abs(S.t1 - Math.sqrt(2 * L0 / g)) < 0.01, w + ': t1 falsch');
  F(S.t1 < S.t2 && S.t2 < S.t3, w + ': Phasen nicht in der Reihenfolge');
  let dE = 0; for (let i = 0; i < S.N; i++) dE = Math.max(dE, Math.abs(S.Et[i] - S.Et[0]));
  F(dE <= 0.005 * S.Et[0], w + ': E_tot nicht erhalten (' + dE + ' kJ)');
  const iT = Math.round(S.t3 / 0.002);
  F(S.a[iT] < -g, w + ': Beschleunigung am tiefsten Punkt nicht groesser als g nach oben');
}
// 2. Latexseil (Gent-Modell)
{
  const p = { m: 75, L0: 20, k: 60, c: 0, mode: 'gent' }, S = simulate(p);
  F(Math.abs((S.sMax - 20) / 20 - 2) < 0.02, 'Gent: Dehnung ' + (S.sMax - 20) / 20 + ' statt 2');
  F(Math.abs(Math.max(...S.Fs) / (75 * g) - 3) < 0.03, 'Gent: Spitzenkraft nicht 3 m g');
  F(Math.abs(elasticForce(S.sG - 20, p) - 75 * g) < 0.5, 'Gent: s_G erfuellt F_el = m g nicht');
  let dE = 0; for (let i = 0; i < S.N; i++) dE = Math.max(dE, Math.abs(S.Et[i] - S.Et[0]));
  F(dE <= 0.005 * S.Et[0], 'Gent: E_tot nicht erhalten');
}
// 3. Daempfung
for (const c of [15, 60]) for (const mode of ['hooke', 'gent']) {
  const S = simulate({ m: 75, L0: 20, k: 60, c, mode }), w = mode + ' c=' + c;
  let ok = true; for (let i = 1; i < S.N; i++) if (S.Ed[i] < 0 || S.Ed[i] < S.Ed[i - 1] - 1e-6) { ok = false; break; }
  F(ok, w + ': E_diss negativ oder abnehmend');
  F(S.Et[S.N - 1] < 0.9 * S.Et[0], w + ': E_tot sinkt nicht');
  F(Array.from(S.Fs).every(x => x >= 0), w + ': Seil drueckt');
}
// 4. Zahlformat
F(fnum(1.25, 1).indexOf(',') < 0 && fnum(-12.5, 1).indexOf(',') < 0, 'fnum: Dezimalkomma');

console.log('Bungee-Sprung: ' + faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');
if (fehler.length) {
  console.error('[FEHLER] ' + fehler.length + ' Testfaelle fehlgeschlagen:');
  fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
