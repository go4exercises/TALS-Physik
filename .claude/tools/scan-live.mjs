#!/usr/bin/env node
/**
 * scan-live.mjs — sucht den Malpunkt als Trennzeichen (STYLEGUIDE §2.1).
 *
 * In Rechen- und Wertanzeigen bedeutet `·` ausschliesslich Multiplikation.
 * Der Blick in den Quelltext genuegt dafuer nicht, aus zwei Gruenden:
 *
 *   1. Die meisten Anzeigen entstehen erst zur Laufzeit — aus JS-Stringliteralen,
 *      oft in Zweigen, die nur ein bestimmter Reglerwert oder Modus erreicht.
 *   2. Animationsbeschriftungen stehen auf einem **Canvas** und damit ueberhaupt
 *      nicht im DOM. In Physik lagen fuenf von sieben Fundstellen genau dort;
 *      ein Werkzeug, das nur `innerText` liest, sieht sie nicht.
 *
 * Darum liest dieses Skript beides: den sichtbaren Text der Wertanzeigen **und**
 * jeden `fillText`-Aufruf der Canvas — im Startzustand, nach jedem Umschaltknopf
 * und mit jedem Regler an beiden Anschlaegen.
 *
 *   node .claude/tools/scan-live.mjs themen/*.html
 *   node .claude/tools/scan-live.mjs themen/p0-5-si-einheiten.html --alle
 *
 * Ohne `--alle` werden nur **Verdachtsfaelle** gemeldet (siehe verdacht() unten).
 * Mit `--alle` kommt jede Zeile mit `·` aus einer Wertanzeige — fuer die
 * gruendliche Sichtung, etwa beim Stichwort «Stilcheck».
 *
 * Exit 1, sobald ein Verdachtsfall gefunden wurde.
 */
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

// Wo Werte angezeigt werden. Titel, Navigation, Fusszeile und Bedienhinweise
// stehen bewusst NICHT hier: dort ist `·` etablierte Typografie (STYLEGUIDE §2.1).
const ANZEIGEN = '.fl-eq, .lb-val, .sl-val, .et-fb, .formel-live, .live-box';
// Umschalter, die andere Anzeige-Zweige erreichbar machen.
const KNOEPFE = '.typ-btn, [data-modus], [data-stoff], [data-ort], [data-e]';

const argv = process.argv.slice(2);
const alle = argv.includes('--alle');
const seiten = argv.filter(a => !a.startsWith('--'));

if (!seiten.length) {
  console.error('Aufruf: node .claude/tools/scan-live.mjs <seiten.html …> [--alle]');
  process.exit(2);
}

/**
 * Verdachtsfall? Multiplikation und Trennung lassen sich nicht sicher
 * auseinanderhalten — «1.0 kg · 4182 J/(kg·K)» ist ein Produkt, «250 mA · 120 ms»
 * ein Trenner, und beide sehen gleich aus. Ein Muster traegt aber zuverlaessig:
 *
 *   Zahlen links UND rechts vom Punkt, aber **kein `=` in der Zeile**.
 *   Ein Produkt steht praktisch immer in einer Gleichung (Ansatz-Prinzip §2.1:
 *   erst die Formel, dann die Werte, dann das Ergebnis); ein Trennzeichen nie.
 *
 * Zehnerpotenzen (`9.5·10¹⁴`) sind ausgenommen — dort ist der Punkt Teil der
 * Zahl. Ebenso ausgenommen sind Punkte zwischen Symbolen ohne Ziffern
 * (`v₀ · t`, `kg · m / s²`).
 *
 * NICHT automatisch erkennbar und darum Sache von `--alle`:
 *   - «Etikett · Wert = …» («Erde · g = 9.81 m/s²») — traegt ein `=`;
 *   - zwei vollstaendige Gleichungen nebeneinander («1 A = 1 C/s · 1 C = …»),
 *     die strukturgleich zu einer korrekten Kette «P = 230 V · 8.0 A = 1840 W»
 *     sind und sich davon nicht durch ein Muster trennen lassen.
 * Das Skript ist damit ein Filter, kein Beweis: es faengt die gefaehrlichen
 * Zahl-·-Zahl-Faelle, die Sichtung mit `--alle` ersetzt es nicht.
 */
function verdacht(zeile) {
  // Vergleichszeichen jeder Art heisst: hier wird gerechnet, nicht getrennt.
  // Auch ≠ und ≈ zaehlen — die Kibble-Waage in p0-5 stellt damit ihr
  // Kraeftegleichgewicht dar.
  if (/[=≠≈<>≤≥]/.test(zeile)) return null;
  // Klammern kennzeichnen einen Term, dessen Gleichung in einer anderen Zeile
  // steht (p0-5: «m = U · I / (g · v)» oben, die Werte darunter).
  if (/[()]/.test(zeile)) return null;
  // Zehnerpotenzen: dort gehoert der Punkt zur Zahl. Achtung, ¹ ² ³ liegen
  // NICHT im Unicode-Block ⁰-⁹ (U+2070…), sie muessen einzeln stehen.
  const rein = zeile.replace(/·\s*10\s*(\^\s*-?\d+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)/g, ' ');
  for (const m of rein.matchAll(/·/g)) {
    const links = rein.slice(0, m.index).split('·').pop();
    const rechts = rein.slice(m.index + 1).split('·')[0];
    if (/\d/.test(links) && /\d/.test(rechts)) return 'Zahl · Zahl ohne Gleichung';
  }
  return null;
}

const browser = await chromium.launch();
let verdachtsfaelle = 0;

for (const seite of seiten) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const jsFehler = [];
  page.on('pageerror', e => jsFehler.push(String(e).slice(0, 120)));

  // Canvas-Beschriftungen mitschneiden — sie stehen in keinem DOM-Knoten.
  await page.addInitScript(() => {
    window.__cvText = [];
    const orig = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function (t) {
      try { window.__cvText.push(String(t)); } catch (e) { /* Zeichnen nie brechen */ }
      return orig.apply(this, arguments);
    };
  });

  await page.goto(pathToFileURL(resolve(seite)).href, { waitUntil: 'load' });
  await page.waitForTimeout(400);

  // Bedienzustaende durchfahren und nach JEDEM Zustand einsammeln. Einmal am
  // Ende genuegt nicht: Teile der Seite sind nur in einem Modus sichtbar (im
  // Einheitentrainer erscheint «Lernen starten» erst im Lernmodus), und der
  // DOM-Text des vorigen Zustands ist dann schon ueberschrieben. Die
  // Canvas-Texte sammelt der fillText-Haken ohnehin durchgehend.
  const gesammelt = new Map();

  const sammle = async () => {
    const neu = await page.evaluate(([anzeigen]) => {
      const raus = [];
      for (const el of document.querySelectorAll(anzeigen)) {
        for (const z of (el.innerText || '').split('\n')) {
          const t = z.replace(/\s+/g, ' ').trim();
          if (t.includes('·')) raus.push(t);
        }
      }
      return raus;
    }, [ANZEIGEN]);
    for (const t of neu) if (!gesammelt.has(t)) gesammelt.set(t, 'DOM');
  };

  // Was ein Mensch nach einem Moduswechsel tut: die Uebung starten, etwas
  // Ungueltiges und etwas Gueltiges eintippen, pruefen lassen. Erst dann
  // stehen Rueckmeldungstexte wie «Erlaubt sind …» ueberhaupt auf der Seite.
  const nachfassen = wert => page.evaluate(async (wert) => {
    const warte = ms => new Promise(r => setTimeout(r, ms));
    const sicht = sel => [...document.querySelectorAll(sel)].filter(e => e.offsetParent);
    const knopf = re => sicht('button').filter(b => re.test(b.textContent || ''));
    // Frueher Ausstieg: die meisten Themenseiten haben weder Eingabefeld noch
    // Startknopf. Ohne diese Pruefung wartet das Skript dort nach jedem der bis
    // zu 24 Umschalter rund anderthalb Sekunden ins Leere.
    if (!sicht('input[type=text], input[type=number]').length
        && !knopf(/starten|beginnen/i).length) return;
    for (const b of knopf(/starten|beginnen/i).slice(0, 3)) {
      try { b.click(); } catch (e) { /* egal */ }
      await warte(300);
    }
    for (const feld of sicht('input[type=text], input[type=number]').slice(0, 3)) {
      feld.value = wert;
      feld.dispatchEvent(new Event('input', { bubbles: true }));
      feld.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
      feld.dispatchEvent(new Event('change', { bubbles: true }));
      await warte(120);
      for (const b of knopf(/prüfen|antwort/i).slice(0, 2)) {
        try { b.click(); } catch (e) { /* egal */ }
        await warte(200);
      }
    }
  }, wert);

  await sammle();
  for (const v of ['xyz', '1']) { await nachfassen(v); await sammle(); }

  const knoepfe = await page.$$(KNOEPFE);
  for (const k of knoepfe.slice(0, 24)) {
    try { await k.click({ timeout: 1500 }); } catch (e) { continue; }
    await page.waitForTimeout(120);
    await sammle();
    for (const v of ['xyz', '1']) { await nachfassen(v); await sammle(); }
  }

  await page.evaluate(async () => {
    const warte = ms => new Promise(r => setTimeout(r, ms));
    for (const r of document.querySelectorAll('input[type=range]')) {
      for (const v of [r.min, r.max, r.defaultValue]) {
        r.value = v;
        r.dispatchEvent(new Event('input', { bubbles: true }));
        await warte(60);
      }
    }
  });
  await page.waitForTimeout(200);
  await sammle();

  const cvTexte = await page.evaluate(() => window.__cvText || []);
  for (const t of cvTexte) {
    const z = t.replace(/\s+/g, ' ').trim();
    if (z.includes('·') && !gesammelt.has(z)) gesammelt.set(z, 'Canvas');
  }

  const funde = [...gesammelt].map(([t, h]) => ({ t, h }));

  const gemeldet = funde
    .map(f => ({ ...f, grund: verdacht(f.t) }))
    .filter(f => alle || f.grund);

  if (gemeldet.length || jsFehler.length) {
    console.log(`\n${seite}`);
    for (const f of gemeldet) {
      const marke = f.grund ? '!!' : '  ';
      console.log(`  ${marke} [${f.h.padEnd(6)}] ${f.t}`);
      if (f.grund) console.log(`         ^ ${f.grund}`);
    }
    for (const e of jsFehler) console.log(`  !! JS-Fehler: ${e}`);
  }
  verdachtsfaelle += gemeldet.filter(f => f.grund).length;
  await page.close();
}

await browser.close();
console.log(`\n${seiten.length} Seite(n) geprüft — ${verdachtsfaelle} Verdachtsfall/-fälle.`);
if (!alle && !verdachtsfaelle) {
  console.log('Für die vollständige Sichtung aller `·` in Wertanzeigen: --alle');
}
process.exit(verdachtsfaelle ? 1 : 0);
