#!/usr/bin/env node
/* ─────────────────────────────────────────────────────────────
   Automatische Tests fuer die Simulation Schiefe Ebene
   (simulationen/schiefe-ebene.html, Fassung des Auftraggebers).

   Laedt die Seite in jsdom, fuehrt das Seitenskript aus und prueft das
   Modell von aussen (die Seite selbst bleibt unveraendert):
     - Losrutschen genau bei tan(alpha) > mu_H (sonst Haften, a = 0)
     - Rampe: a = g (sin(alpha) - mu_G cos(alpha)), unabhaengig von m;
       v am Fusspunkt aus v^2 = 2 a L, Zeit aus L = a t^2 / 2
     - Horizontale: a = -mu_G g, Bremsweg v^2 / (2 mu_G g)
     - Energie: E_mech + E_diss = E_0 = m g L sin(alpha) zu jeder Zeit,
       E_diss nie negativ und nie abnehmend; im Stillstand
       E_0 = mu_G m g cos(alpha) L + mu_G m g s_B (Reibungsarbeit)
     - Zahlformat mit Dezimalpunkt (fnum)

   Aufruf vom Repo-Root:  node scripts/verify_schiefe_ebene.js
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

const datei = path.join(__dirname, '..', 'simulationen', 'schiefe-ebene.html');
if (!fs.existsSync(datei)) {
  console.error('[FEHLER] ' + datei + ' nicht gefunden');
  process.exit(1);
}

const html = fs.readFileSync(datei, 'utf8');
const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true });
const skripte = [...dom.window.document.querySelectorAll('script')]
  .filter(s => !s.src && s.textContent.indexOf('function model') !== -1);
if (!skripte.length) {
  console.error('[FEHLER] Seitenskript mit model() nicht gefunden');
  process.exit(1);
}
try {
  // Seitenskript laeuft im strikten Modus; seine Funktionen fuer den Test herausreichen
  dom.window.eval(skripte[0].textContent + '\n;window.__seModell = { model, fnum };');
} catch (e) {
  console.error('[FEHLER] Seitenskript laeuft nicht: ' + e.message);
  process.exit(1);
}
const { model, fnum } = dom.window.__seModell;
const g = 9.81;

const fehler = []; let faelle = 0;
const F = (ok, was) => { faelle++; if (!ok) fehler.push(was); };
const rel = (a, b) => Math.abs(a - b) / Math.max(1e-9, Math.abs(b));
const t0 = Date.now();

for (const alpha of [5, 15, 25, 30, 35, 45]) for (const muH of [0, 0.2, 0.4, 0.7]) for (const muG of [0, 0.1, 0.3, 0.6])
for (const L of [5, 10, 15]) for (const m of [20, 80]) {
  const p = { alpha, m, L, muH, muG }, S = model(p), w = `alpha=${alpha} muH=${muH} muG=${muG} L=${L} m=${m}`;
  const a = alpha * Math.PI / 180, sn = Math.sin(a), cs = Math.cos(a);
  const aR = g * (sn - muG * cs);
  const rutscht = Math.tan(a) > muH && aR > 1e-10;
  F(S.moving === rutscht, w + ': Losrutschen falsch');
  if (!rutscht) {
    F(Array.from(S.v).every(x => x === 0) && Array.from(S.acc).every(x => x === 0), w + ': haftet, bewegt sich aber');
    continue;
  }
  F(rel(S.accRamp, aR) < 1e-12, w + ': Rampenbeschleunigung');
  F(rel(model({ ...p, m: 110 }).accRamp, aR) < 1e-12, w + ': Beschleunigung haengt von m ab');
  F(rel(S.vRamp, Math.sqrt(2 * aR * L)) < 1e-9, w + ': v am Fusspunkt');
  F(rel(S.tRamp, Math.sqrt(2 * L / aR)) < 1e-9, w + ': Zeit auf der Rampe');
  F(Math.abs(S.aFlat + muG * g) < 1e-12, w + ': Verzoegerung auf der Horizontalen');
  const E0 = m * g * L * sn / 1000;
  F(rel(S.E0, E0) < 1e-12, w + ': E_0');
  let dE = 0, mono = true;
  for (let i = 0; i < S.N; i++) {
    dE = Math.max(dE, Math.abs(S.Emech[i] + S.Ediss[i] - E0));
    if (S.Ediss[i] < 0 || (i && S.Ediss[i] < S.Ediss[i - 1] - 1e-9)) mono = false;
  }
  F(dE < 1e-9, w + ': E_mech + E_diss nicht konstant');
  F(mono, w + ': E_diss negativ oder abnehmend');
  if (muG > 0) {
    const sB = S.vRamp * S.vRamp / (2 * muG * g);
    F(rel(S.braking, sB) < 1e-9, w + ': Bremsweg');
    F(rel((muG * m * g * cs * L + muG * m * g * sB) / 1000, E0) < 1e-9, w + ': Reibungsarbeit ungleich E_0');
    if (S.tStop <= S.horizon) F(Math.abs(S.s[S.N - 1] - (L + sB)) < 1e-9, w + ': Endlage');
  } else {
    F(!Number.isFinite(S.braking), w + ': ohne Gleitreibung endlicher Bremsweg');
  }
}
F(fnum(1.25, 2).indexOf(',') < 0 && fnum(-12.5, 1).indexOf(',') < 0, 'fnum: Dezimalkomma');

console.log('Schiefe Ebene: ' + faelle + ' Pruefungen in ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');
if (fehler.length) {
  console.error('[FEHLER] ' + fehler.length + ' Testfaelle fehlgeschlagen:');
  fehler.slice(0, 25).forEach(f => console.error('   - ' + f));
  process.exit(1);
}
console.log('SUMME: 0 Fehler');
process.exit(0);
