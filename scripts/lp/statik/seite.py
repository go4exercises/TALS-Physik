"""Baut leitprogramme/leitprogramm-statik.html aus einer Kapitelbeschreibung (seit 05.10.2026).

  python3 scripts/lp/statik/seite.py

Fünftes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4), als Kopie von
scripts/lp/energie/ entstanden: Kopf, CSS, Grundskript und Bausteine von dort, neu sind
Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Siehe README.md.
"""
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-statik.html'
TS = '../themen/p4-4-statik.html'

SEO_LEER = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->\n<!-- SEO:ENDE -->'
seo = SEO_LEER
if os.path.exists(ZIEL):
    m = re.search(r'<!-- SEO:ANFANG.*?<!-- SEO:ENDE -->', open(ZIEL, encoding='utf-8').read(), re.S)
    if m:
        seo = m.group(0)

KOPF = '''<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Leitprogramm Statik</title>
''' + seo + '''

<link rel="stylesheet" href="../schriften.css">
<!-- Die Seite erbt Farben, Karten und die Clip-Buehne von der Site.
     Reihenfolge zaehlt: der eigene <style> unten gewinnt bei gleichem
     Gewicht, das Leitprogramm behaelt also sein Layout. -->
<link rel="stylesheet" href="../style.css">
<style>
'''

# Gerüst-CSS aus dem Mathe-Vorbild (leitprogramme/quadratische-funktionen.html), mit
# Physiks Bereichsfarbe Bernstein für Chips, Links und PDF-Knöpfe; didaktische Farben
# (Blau = Definition, Rot = Fehler, Orange = Aufgabe) wie dort (STYLEGUIDE §5.1).
CSS = r'''
:root{ --karte:var(--weiss); --teal:#0f766e; }
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --papier:#171512; --papier-2:#1f1c17; --karte:#211e19; --weiss:#211e19;
    --tinte:#f1ece1; --tinte-2:#b6ab97; --linie:#3a342a;
    --blau:#8ab6e8; --blau-hell:#1b2a3d; --blau-rand:#3f6da3;
    --gruen:#79c894; --gruen-hell:#162c1f; --gruen-rand:#3f8058;
    --lila:#c3a0ec; --lila-hell:#251b33; --lila-rand:#7d5cae;
    --orange:#e9a25e; --orange-hell:#33240f; --orange-rand:#9c6a2c;
    --rot:#ef9393; --rot-hell:#331a1a; --rot-rand:#a35050;
    --bernstein:#f0a742; --bernstein-hell:#2a2117; --bernstein-rand:#6b4a1e; --teal:#5cc8bb;
    --s:0 2px 10px rgba(0,0,0,.35); --sl:0 4px 22px rgba(0,0,0,.5);
  }
}
:root[data-theme="dark"]{
  --papier:#171512; --papier-2:#1f1c17; --karte:#211e19; --weiss:#211e19;
  --tinte:#f1ece1; --tinte-2:#b6ab97; --linie:#3a342a;
  --blau:#8ab6e8; --blau-hell:#1b2a3d; --blau-rand:#3f6da3;
  --gruen:#79c894; --gruen-hell:#162c1f; --gruen-rand:#3f8058;
  --lila:#c3a0ec; --lila-hell:#251b33; --lila-rand:#7d5cae;
  --orange:#e9a25e; --orange-hell:#33240f; --orange-rand:#9c6a2c;
  --rot:#ef9393; --rot-hell:#331a1a; --rot-rand:#a35050;
  --bernstein:#f0a742; --bernstein-hell:#2a2117; --bernstein-rand:#6b4a1e; --teal:#5cc8bb;
  --s:0 2px 10px rgba(0,0,0,.35); --sl:0 4px 22px rgba(0,0,0,.5);
}

*{box-sizing:border-box}
body{margin:0;background:var(--papier);color:var(--tinte);
  font-family:var(--serif);font-size:17px;line-height:1.62;-webkit-text-size-adjust:100%}
h1,h2,h3,h4{text-wrap:balance;line-height:1.22;margin:0}
a{color:var(--bernstein)}
:focus-visible{outline:2.5px solid var(--bernstein-rand);outline-offset:2px;border-radius:3px}
mjx-container{overflow-x:auto;overflow-y:hidden;max-width:100%}

/* ---------- Gerüst (HOWTO-leitprogramme §6: Fliesstext schmal, Arbeitsflächen breit) ---------- */
.huelle{max-width:1440px;margin:0 auto;padding:0 20px 100px}
.raster{display:grid;grid-template-columns:1fr;gap:0}
@media(min-width:1000px){ .raster{grid-template-columns:236px minmax(0,1fr);gap:52px;align-items:start} }
.inhalt{min-width:0}
.kap>p,.kap>h2,.kap>h3,.ziel,.duo>div>p{max-width:68ch}
.duo{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px;align-items:start}
.duo>*{min-width:0}
@media(min-width:1180px){
  .duo{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .aufg.zwei{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:34px}
  .aufg.zwei>li:nth-last-child(2):nth-child(odd){border-bottom:none}
}

/* ---------- Kopf ---------- */
.kopf{border-bottom:1px solid var(--linie);background:var(--papier-2);margin-bottom:44px;padding:0 20px}
.kopf-innen{max-width:1440px;margin:0 auto;padding:30px 0 34px;
  display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between}
.marke{font-family:var(--sans);font-size:.76rem;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;color:var(--bernstein);margin:0 0 10px}
.kopf h1{font-size:clamp(2rem,5.2vw,2.9rem);font-weight:700;letter-spacing:-.015em}
.kopf .unter{font-family:var(--sans);color:var(--tinte-2);margin:10px 0 0;font-size:1rem;max-width:52ch}
.kopf-rechts{font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);text-align:right;
  display:flex;flex-direction:column;gap:8px;align-items:flex-end}
.themenschalter{font-family:var(--sans);font-size:.78rem;font-weight:600;color:var(--tinte-2);
  background:var(--karte);border:1px solid var(--linie);border-radius:999px;padding:6px 13px;cursor:pointer}
.themenschalter:hover{color:var(--tinte);border-color:var(--tinte-2)}

/* ---------- Seitenschiene ---------- */
.schiene{font-family:var(--sans);font-size:.87rem;margin-bottom:40px}
@media(min-width:1000px){.schiene{position:sticky;top:22px;margin-bottom:0}}
.schiene h2{font-family:var(--sans);font-size:.72rem;font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;color:var(--tinte-2);margin-bottom:12px}
.schiene ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px}
.schiene a{display:flex;gap:9px;align-items:baseline;padding:6px 8px;border-radius:5px;
  text-decoration:none;color:var(--tinte);border-left:2.5px solid transparent}
.schiene a:hover{background:var(--papier-2)}
.schiene a.aktiv{border-left-color:var(--bernstein-rand);background:var(--papier-2);font-weight:600}
.schiene .nr{font-family:var(--mono);font-size:.76rem;color:var(--tinte-2);min-width:1.6em}
.schiene .lekt{font-family:var(--sans);font-size:.68rem;font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;color:var(--tinte-2);margin:16px 0 5px;padding-left:8px}
.fortschritt{margin-top:22px;padding-top:16px;border-top:1px solid var(--linie)}
.balken{height:6px;background:var(--papier-2);border:1px solid var(--linie);border-radius:99px;overflow:hidden}
.balken i{display:block;height:100%;background:var(--gruen-rand);width:0;transition:width .35s ease}
.fortschritt p{margin:9px 0 0;font-size:.79rem;color:var(--tinte-2)}
.fortschritt button{margin-top:10px;font-family:var(--sans);font-size:.75rem;color:var(--tinte-2);
  background:none;border:none;padding:0;cursor:pointer;text-decoration:underline}

/* ---------- Anleitung und Kompetenzen (eingeklappt) ---------- */
.anleitung{background:var(--karte);border:1px solid var(--linie);border-radius:10px;
  padding:22px 26px;margin-bottom:24px;box-shadow:var(--s)}
.anleitung summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px}
.anleitung summary::-webkit-details-marker{display:none}
.anleitung summary::after{content:"";flex:none;margin-left:auto;width:.5em;height:.5em;
  border-right:2px solid var(--tinte-2);border-bottom:2px solid var(--tinte-2);
  transform:translateY(-.15em) rotate(45deg);transition:transform .2s}
.anleitung[open] summary::after{transform:translateY(.1em) rotate(-135deg)}
.anleitung h2{font-size:1.12rem}
.anleitung ol{margin:12px 0 0;padding-left:1.25em;font-family:var(--sans);font-size:.94rem;color:var(--tinte-2);max-width:68ch}
.anleitung li{margin:6px 0}
.anleitung li b{color:var(--tinte)}
.kompetenzen ul{margin:10px 0 0;padding-left:1.25em;font-family:var(--sans);font-size:.92rem}
.kompetenzen li{margin:5px 0}
.kompetenzen .rlp-quelle,.kompetenzen .rlp-fuss{font-family:var(--sans);font-size:.8rem;color:var(--tinte-2);margin:8px 0 0}

/* ---------- Lektionsband ---------- */
.band{display:flex;align-items:center;gap:14px;margin:56px 0 30px}
.band:first-of-type{margin-top:8px}
.band .strich{flex:1;height:1px;background:var(--linie)}
.band span{font-family:var(--sans);font-size:.74rem;font-weight:700;letter-spacing:.15em;
  text-transform:uppercase;color:var(--tinte-2);white-space:nowrap}
@media(max-width:600px){ .band span{white-space:normal} }

/* ---------- Kapitel ---------- */
.kap{margin-bottom:52px;scroll-margin-top:20px}
.kap-meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px}
.marker{font-family:var(--mono);font-size:.74rem;font-weight:700;letter-spacing:.04em;
  padding:3px 8px;border-radius:4px;background:var(--papier-2);color:var(--tinte-2)}
.abz{font-family:var(--sans);font-size:.72rem;font-weight:700;letter-spacing:.05em;
  padding:3px 9px;border-radius:999px;border:1px solid;
  color:var(--bernstein);border-color:var(--bernstein-rand);background:var(--bernstein-hell)}
.zeit{font-family:var(--sans);font-size:.78rem;color:var(--tinte-2)}
.kap h2{font-size:1.62rem;font-weight:700;letter-spacing:-.01em}
.ziel{font-family:var(--sans);font-size:.95rem;color:var(--tinte-2);
  border-left:2.5px solid var(--linie);padding-left:13px;margin:12px 0 22px}
.kap h3{font-family:var(--sans);font-size:1rem;font-weight:700;margin:30px 0 10px}
.kap p{margin:0 0 14px}
.phase{font-family:var(--sans);font-size:.74rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--tinte-2);margin:34px 0 8px;display:flex;align-items:center;gap:8px}
.phase span{display:inline-grid;place-items:center;width:1.7em;height:1.7em;border-radius:50%;
  background:var(--papier-2);border:1px solid var(--linie);color:var(--tinte);font-size:.9rem;letter-spacing:0}
.ausf{font-family:var(--sans);font-size:.92rem;border-top:1px solid var(--linie);padding-top:12px;margin-top:26px}
.komm{font-family:var(--sans);font-size:.87rem;color:var(--tinte-2)}

/* ---------- Clipkarte (Bühne aus ../physiklib.js) ---------- */
.clipkarte{margin:22px 0 26px;max-width:640px}
.clip-start{display:flex;width:100%;align-items:center;gap:15px;text-align:left;cursor:pointer;
  background:var(--lila-hell);border:1px solid var(--lila-rand);border-radius:10px;
  padding:14px 17px;font-family:var(--sans);color:var(--tinte)}
.clip-start:hover{box-shadow:var(--sl)}
.clip-play{flex:none;width:38px;height:38px;border-radius:50%;background:var(--lila);color:#fff;
  display:grid;place-items:center;font-size:.9rem;padding-left:3px}
:root[data-theme="dark"] .clip-play{color:#171512}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]) .clip-play{color:#171512} }
.clip-txt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.clip-titel{font-weight:600;font-size:.97rem;line-height:1.32}
.clip-zeit{font-family:var(--mono);font-size:.8rem;color:var(--tinte-2);flex:none}

/* ---------- Merkkasten, Häufiger Fehler, Tabellen ---------- */
.merk{background:var(--blau-hell);border:1px solid var(--blau-rand);border-left-width:4px;
  border-radius:8px;padding:16px 20px;margin:20px 0}
.merk .titel,.warn .titel{font-family:var(--sans);font-size:.73rem;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;margin-bottom:8px}
.merk .titel{color:var(--blau)}
.merk p:last-child,.warn p:last-child{margin-bottom:0}
.merk ul{margin:4px 0 0;padding-left:1.2em}
.warn{background:var(--rot-hell);border:1px solid var(--rot-rand);border-left-width:4px;
  border-radius:8px;padding:16px 20px;margin:20px 0}
.warn .titel{color:var(--rot)}
.festhalten{display:grid;grid-template-columns:minmax(0,1fr);gap:0 26px}
@media(min-width:1180px){.festhalten{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.tabhuelle{overflow-x:auto}
table.gesetze{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem}
table.gesetze th,table.gesetze td{border-bottom:1px solid var(--linie);padding:9px 10px;text-align:left;vertical-align:middle}
table.gesetze th{font-family:var(--sans);font-size:.74rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--tinte-2)}
table.gesetze td:first-child{font-family:var(--sans);font-size:.88rem;font-weight:600}
table.gesetze td.wort{font-family:var(--sans);font-size:.88rem;color:var(--tinte-2)}

/* ---------- Aufgaben mit Lösungen ---------- */
.test{border:1.5px solid var(--gruen-rand);border-radius:11px;background:var(--karte);margin:30px 0 0;overflow:hidden}
.test-kopf{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center;
  background:var(--gruen-hell);padding:11px 18px;border-bottom:1px solid var(--gruen-rand)}
.test-kopf h3{font-family:var(--sans);font-size:.94rem;font-weight:700;color:var(--gruen);margin:0}
.test-kopf .werkz{display:flex;gap:14px;align-items:center;font-family:var(--sans);font-size:.78rem}
.test-kopf button{font-family:var(--sans);font-size:.78rem;background:none;border:none;
  color:var(--gruen);cursor:pointer;text-decoration:underline;padding:0}
.test-kopf label{display:flex;gap:6px;align-items:center;color:var(--tinte-2);cursor:pointer}
.summe{font-family:var(--mono);font-size:.76rem;color:var(--tinte-2);white-space:nowrap}
.aufg{list-style:none;margin:0;padding:6px 18px 18px}
.aufg>li{border-bottom:1px dotted var(--linie);padding:11px 0}
.aufg>li:last-child{border-bottom:none;padding-bottom:2px}
.a-frage{display:flex;gap:11px;align-items:baseline}
.a-frage .nr{font-family:var(--mono);font-size:.83rem;font-weight:700;color:var(--gruen);flex:none;min-width:2.4em}
.a-frage .pkt{font-family:var(--mono);font-size:.72rem;color:var(--tinte-2);flex:none;min-width:3.4em;margin-left:-4px}
.a-frage .txt{flex:1;min-width:0}
details.loes{margin:7px 0 0 calc(5.8em + 11px)}
details.loes summary{font-family:var(--sans);font-size:.79rem;color:var(--tinte-2);
  cursor:pointer;list-style:none;display:inline-flex;gap:6px;align-items:center;
  border:1px solid var(--linie);border-radius:999px;padding:2px 11px}
details.loes summary::-webkit-details-marker{display:none}
details.loes summary:hover{border-color:var(--gruen-rand);color:var(--gruen)}
details.loes[open] summary{color:var(--gruen);border-color:var(--gruen-rand)}
details.loes .inhaltbox{border-left:2.5px solid var(--gruen-rand);padding:6px 0 2px 13px;margin-top:9px}
details.loes .inhaltbox p{margin:0 0 7px}
details.loes .inhaltbox p:last-child{margin-bottom:0}

/* ---------- Gesamttest ---------- */
.gesamt{border:2px solid var(--tinte-2);border-radius:12px;background:var(--karte);overflow:hidden;margin-top:20px}
.gesamt-kopf{background:var(--papier-2);padding:16px 20px;border-bottom:1px solid var(--linie)}
.gesamt-kopf h2{font-size:1.4rem}
.bewertung{margin:0;padding:16px 20px 20px;font-family:var(--sans);font-size:.88rem;color:var(--tinte-2)}
.bewertung table{width:100%;border-collapse:collapse;margin-top:8px}
.bewertung td{padding:5px 8px;border-bottom:1px solid var(--linie)}
.bewertung td:first-child{font-family:var(--mono);white-space:nowrap;width:1%;color:var(--tinte)}
.pdf-weg{margin:14px 0 4px;display:flex;flex-direction:column;gap:10px;font-family:var(--sans);font-size:.92rem}
.pdf-schritt{display:flex;gap:12px;align-items:flex-start}
.pdf-schritt .nr{flex:none;width:1.8em;height:1.8em;border-radius:50%;display:grid;place-items:center;
  background:var(--karte);border:1px solid var(--linie);font-weight:700}
.pdf-knopf{display:inline-block;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--bernstein-hell);
  border:1px solid var(--bernstein-rand);color:var(--tinte);text-decoration:none;font-weight:600}
.pdf-knopf:hover{box-shadow:var(--sl)}
.weiter ul{font-family:var(--sans);font-size:.92rem;padding-left:1.2em}

/* ---------- Fuss ---------- */
.fuss{margin-top:64px;padding-top:20px;border-top:1px solid var(--linie);
  font-family:var(--sans);font-size:.8rem;color:var(--tinte-2);display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between}
:root[data-theme="dark"] .site-footer{background:var(--papier-2);color:var(--tinte-2);border-top:1px solid var(--linie)}
:root[data-theme="dark"] .site-footer a{color:var(--bernstein)}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .site-footer{background:var(--papier-2);color:var(--tinte-2);border-top:1px solid var(--linie)}
  :root:not([data-theme="light"]) .site-footer a{color:var(--bernstein)}
}

/* ---------- Simulation mit Aufgabenleiste (HOWTO-leitprogramme §8) ---------- */
.sim{background:var(--karte);border:1px solid var(--linie);border-radius:10px;padding:14px 16px 12px}
.sim-gross{max-width:640px;margin:10px 0 6px}
.sim > svg{display:block;width:100%;max-width:440px;height:auto;margin:6px auto 10px}
.sim-formel{font-family:var(--sans);font-size:.95rem;text-align:center;padding:6px 8px;
  background:var(--papier-2);border-radius:6px;display:flex;flex-direction:column;gap:2px}
.sim-formel i{font-family:var(--serif)}
.sim-notiz{font-size:.82rem;color:var(--tinte-2)}
.reglerfeld[hidden]{display:none}
.reglerfeld{display:flex;flex-direction:column;gap:6px;font-family:var(--sans);font-size:.9rem}
.regler{display:flex;gap:10px;align-items:center}
.regler label{min-width:5.2em}
.regler input[type=range]{flex:1;min-width:0;accent-color:var(--bernstein)}
.regler-wert{font-family:var(--mono);font-size:.86rem;min-width:5.4em;text-align:right}
.sim-knoepfe{display:flex;flex-wrap:wrap;gap:6px;align-items:center;justify-content:center;margin:8px 0 4px;
  font-family:var(--sans);font-size:.8rem;color:var(--tinte-2)}
.sim-knoepfe button{font-family:var(--sans);font-size:.8rem;cursor:pointer;
  background:var(--karte);color:var(--tinte);border:1px solid var(--linie);border-radius:999px;padding:4px 12px}
.sim-knoepfe button.aktiv{background:var(--bernstein-hell);border-color:var(--bernstein-rand);color:var(--tinte);font-weight:700}
.hilfs-schalter{display:flex;gap:7px;align-items:center;justify-content:center;font-family:var(--sans);font-size:.82rem;color:var(--tinte-2);margin:2px 0 8px;cursor:pointer}
.ohne-hilfslinien .hilfslinie{display:none}
.leiste{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:0 0 10px;padding:9px 12px;border-radius:9px;
  background:var(--orange-hell);border:1px solid var(--orange-rand);font-family:var(--sans);font-size:.92rem}
.leiste .ls-nr{font-family:var(--mono);font-size:.78rem;color:var(--orange);font-weight:700}
.leiste .ls-text{flex:1 1 260px;min-width:0}
.leiste .ls-ok{color:var(--gruen);font-weight:700;font-size:1.1rem;min-width:1em}
.leiste .ls-weiter,.leiste .ls-neu{font-family:var(--sans);font-size:.8rem;cursor:pointer;border-radius:999px;padding:4px 12px;
  border:1px solid var(--linie);background:var(--karte);color:var(--tinte-2)}
.leiste.geloest,.leiste.fertig{background:var(--gruen-hell);border-color:var(--gruen-rand)}
.leiste.geloest .ls-weiter{border-color:var(--gruen-rand);color:var(--tinte);font-weight:700}
.leiste .ls-vergleich{flex:1 1 100%;font-size:.88rem}
.leiste .ls-vergleich summary{cursor:pointer;color:var(--tinte-2)}
.leiste .ls-vergleich div{margin-top:6px}
/* Diagramme und Szenen: Farben wie auf Themenseite 4.4 (STYLEGUIDE §5.2) — Seil-, Zug- und
   Einzelkräfte Blau, Gewichtskraft Bernstein, Normal- und Auflagerkraft Grün, Reibung Türkis,
   Komponenten und Hebelarm Violett, Resultierende Rot; voriger Lauf und Gesamtlast grau gestrichelt */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.vorher{fill:none;stroke:var(--tinte-2);stroke-width:1.8;stroke-dasharray:5 4;opacity:.6}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.boden{stroke:var(--tinte-2);stroke-width:2}
.rad{fill:var(--tinte-2)}
.pf-linie{stroke-width:2.6;fill:none}
.pf-linie.duenn{stroke-width:1.6;stroke-dasharray:4 3}
.pf-linie.geist,.pf-kopf.geist{opacity:.22}
.pf-linie.pf-a{stroke:var(--lila)} .pf-kopf.pf-a{fill:var(--lila)}
.pf-linie.pf-f{stroke:var(--blau)} .pf-kopf.pf-f{fill:var(--blau)}
.pf-linie.pf-g{stroke:var(--bernstein)} .pf-kopf.pf-g{fill:var(--bernstein)}
.pf-linie.pf-n{stroke:var(--gruen)} .pf-kopf.pf-n{fill:var(--gruen)}
.pf-linie.pf-reib{stroke:var(--teal)} .pf-kopf.pf-reib{fill:var(--teal)}
.pf-linie.pf-res{stroke:var(--rot);stroke-width:3.2} .pf-kopf.pf-res{fill:var(--rot)}
.pf-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:3.5px;paint-order:stroke}
text.pf-a{fill:var(--lila)} text.pf-f{fill:var(--blau)} text.pf-g{fill:var(--bernstein)} text.pf-n{fill:var(--gruen)} text.pf-reib{fill:var(--teal)} text.pf-res{fill:var(--rot)}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bt-meldung{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.kurve-fx,.kurve-mini.kurve-fh{stroke:var(--lila)} .kurve-mini.kurve-fn{stroke:var(--gruen)} .kurve-mini.kurve-fr{stroke:var(--teal);stroke-dasharray:6 4}
.kurve-mini.kurve-m{stroke:var(--blau)} .kurve-mini.kurve-fg{stroke:var(--bernstein)} .kurve-mini.kurve-fb{stroke:var(--gruen);stroke-dasharray:6 4}
svg.mini.breit{width:260px}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.p-mini{fill:var(--tinte)}
.kiste{fill:var(--bernstein-hell);stroke:var(--bernstein);stroke-width:1.6}
.hilfslinie{stroke:var(--lila);stroke-width:1;stroke-dasharray:3 3;opacity:.7}
.saeule-text{fill:var(--weiss);font-family:var(--sans);font-size:9.5px;font-weight:700}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:10.5px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.winkelbogen{fill:none;stroke:var(--tinte-2);stroke-width:1.3}
.kurve-fx{fill:none;stroke:var(--lila);stroke-width:2.4} .kurve-fy{fill:none;stroke:var(--lila);stroke-width:2.4;stroke-dasharray:6 4}
.p-fx,.p-fy,.p-fh{fill:var(--lila)} .p-fn{fill:var(--gruen)} .p-fr{fill:var(--teal)}
.legende{fill:var(--tinte-2);font-family:var(--sans);font-size:10px;font-weight:700}
.legende.l-fx,.legende.l-fy,.legende.l-fh{fill:var(--lila)} .legende.l-fn{fill:var(--gruen)} .legende.l-fr{fill:var(--teal)}
.ring{fill:var(--karte);stroke:var(--tinte);stroke-width:2.4}
.spur{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:3 4}
.rampe{fill:var(--papier-2);stroke:var(--tinte-2);stroke-width:1.2}
.anschlag{stroke:var(--tinte);stroke-width:3;stroke-linecap:round}
.kurve-fh{fill:none;stroke:var(--lila);stroke-width:2.4} .kurve-fn{fill:none;stroke:var(--gruen);stroke-width:2.4}
.kurve-fr{fill:none;stroke:var(--teal);stroke-width:2.4;stroke-dasharray:6 4}
.mutter{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.6}
.schluessel{stroke:var(--tinte-2);stroke-width:9;stroke-linecap:round;opacity:.85}
.achspunkt{fill:var(--tinte)}
.wirkungslinie{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:6 4;opacity:.7}
.hebelarm{stroke:var(--lila);stroke-width:2;stroke-dasharray:5 3}
.balken-leer{fill:var(--papier-2);stroke:var(--linie)}
.balken-m{fill:var(--blau);opacity:.85}
.grenze{stroke:var(--rot);stroke-width:2.4}
.lager{fill:var(--tinte-2)}
.brett{fill:var(--bernstein-hell);stroke:var(--bernstein);stroke-width:2.4}
line.brett{stroke-width:6;stroke-linecap:round}
.tick{stroke:var(--bernstein);stroke-width:1.2}
.kurve-fa{fill:none;stroke:var(--gruen);stroke-width:2.4} .kurve-fb{fill:none;stroke:var(--gruen);stroke-width:2.4;stroke-dasharray:6 4}
.vek-mini{stroke:var(--blau);stroke-width:2.2} .vek-kopf{fill:var(--blau)}
.klotz-zahl{fill:var(--tinte);font-family:var(--sans);font-size:9.5px;font-weight:700}
.merk-box{border:1px solid var(--blau-rand);background:var(--blau-hell);border-radius:10px;padding:10px 16px;margin:12px 0;max-width:68ch}
.mini-reihe{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 6px calc(5.8em + 11px)}

/* ---------- Üben mit Rückmeldung ---------- */
.uebung{border:1.5px solid var(--orange-rand);border-radius:11px;background:var(--karte);padding:12px 16px 14px;margin:14px 0}
.ue-kopf{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;font-family:var(--sans);font-size:.8rem;margin-bottom:6px}
.ue-titel{font-weight:700;color:var(--orange)}
.ue-serie{color:var(--tinte-2)}
.ue-aufgabe{margin:6px 0 10px}
.ue-zeile{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-family:var(--sans);font-size:.95rem}
.ue-eingabe{display:inline-flex;flex-wrap:wrap;gap:4px;align-items:center}
.ue-eingabe i{font-family:var(--serif)}
.ue-eingabe input{width:5.4em;font-family:var(--mono);font-size:.95rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);
  border-radius:6px;background:var(--papier);color:var(--tinte);text-align:center}
.ue-eingabe input:focus{outline:none;border-color:var(--orange-rand)}
.ue-eingabe input.falsch{border-color:var(--rot-rand)}
.ue-eingabe select{font-family:var(--sans);font-size:.88rem;padding:4px 6px;margin:0 3px;border:1.5px solid var(--linie);border-radius:6px;background:var(--papier);color:var(--tinte)}
.ue-zeile button,.ue-weiter{font-family:var(--sans);font-size:.8rem;cursor:pointer;border-radius:999px;padding:4px 12px;
  border:1px solid var(--orange-rand);background:var(--orange-hell);color:var(--tinte)}
.ue-zeile .ue-neu{background:none;border-color:var(--linie);color:var(--tinte-2)}
.ue-rueck{font-family:var(--sans);font-size:.9rem;margin-top:10px;border-radius:7px}
.ue-rueck:empty{display:none}
.ue-rueck.richtig{background:var(--gruen-hell);border-left:4px solid var(--gruen-rand);padding:8px 12px}
.ue-rueck.falsch{background:var(--rot-hell);border-left:4px solid var(--rot-rand);padding:8px 12px}
.ue-rueck.hinweis{background:var(--papier-2);padding:8px 12px}
.ue-loes{margin-top:6px} .ue-loes summary{cursor:pointer;color:var(--tinte-2)}

@media(max-width:600px){
  body{font-size:16px}
  .huelle{padding:0 15px 70px}
  details.loes{margin-left:0}
  .mini-reihe{margin-left:0}
  .regler label{min-width:4.2em}
}
@media print{
  .schiene,.themenschalter,.clip-buehne,.test-kopf .werkz,.clipkarte,.sim,.uebung{display:none}
  .kap{break-inside:avoid}
  details.loes{display:none}
  body{background:#fff}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
'''

# Grundskript aus dem Mathe-Vorbild: Theme, Clipkarten, «alle Lösungen», Fortschritt, Schiene.
BASIS = r'''<script>
  window.MathJax = {
    tex: { inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']] },
    svg: { fontCache: 'global' },
    options: { skipHtmlTags: ['script','noscript','style','textarea','pre'] }
  };
</script>
<script src="../vendor/mathjax/tex-svg.js"></script>

<script>
(function(){
  'use strict';
  // Relativ: die Clips kommen aus diesem Repo, eine Ebene höher.
  var BASIS = '../';
  var KEY = 'leitprogramm-statik-v1';

  /* ---- Theme ---- */
  var schalter = document.getElementById('themenschalter');
  function lesen(){ try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e){ return {}; } }
  function schreiben(s){ try { localStorage.setItem(KEY, JSON.stringify(s)); } catch(e){} }
  var gespeichert = lesen().thema;
  if (gespeichert === 'dark' || gespeichert === 'light') document.documentElement.setAttribute('data-theme', gespeichert);
  schalter.addEventListener('click', function(){
    var jetzt = document.documentElement.getAttribute('data-theme');
    if (!jetzt) jetzt = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var neu = jetzt === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', neu);
    var s = lesen(); s.thema = neu; schreiben(s);
  });

  /* ---- Clipkarten: Bühne aus ../physiklib.js (clipBuehne) ---- */
  document.querySelectorAll('.clipkarte').forEach(function(karte){
    karte.querySelector('.clip-start').addEventListener('click', function(){
      if (document.querySelector('.clip-buehne')) return;
      clipBuehne(BASIS + karte.dataset.clip, karte.dataset.titel || 'Clip');
    });
  });

  /* ---- Lösungen: alle auf/zu ---- */
  document.querySelectorAll('.alle-loesungen').forEach(function(knopf){
    knopf.addEventListener('click', function(){
      var alle = knopf.closest('.test').querySelectorAll('details.loes');
      var oeffnen = Array.prototype.some.call(alle, function(d){ return !d.open; });
      alle.forEach(function(d){ d.open = oeffnen; });
      knopf.textContent = oeffnen ? 'Lösungen zuklappen' : 'alle Lösungen';
    });
  });

  /* ---- Fortschritt ---- */
  var tests = Array.prototype.slice.call(document.querySelectorAll('.test'));
  var fuellung = document.getElementById('balken-fuellung');
  var text = document.getElementById('fortschritt-text');
  function zeichnen(){
    var fertig = tests.filter(function(t){ return t.querySelector('.erledigt').checked; }).length;
    fuellung.style.width = (fertig / tests.length * 100) + '%';
    text.textContent = fertig + ' von ' + tests.length + ' Aufgabenblöcken bearbeitet';
  }
  var stand = lesen().stand || {};
  tests.forEach(function(t){
    var box = t.querySelector('.erledigt');
    if (stand[t.dataset.test]) box.checked = true;
    box.addEventListener('change', function(){
      var s = lesen(); s.stand = s.stand || {}; s.stand[t.dataset.test] = box.checked; schreiben(s); zeichnen();
    });
  });
  zeichnen();
  document.getElementById('fortschritt-reset').addEventListener('click', function(){
    tests.forEach(function(t){ t.querySelector('.erledigt').checked = false; });
    var s = lesen(); s.stand = {}; schreiben(s); zeichnen();
  });

  /* ---- aktives Kapitel in der Schiene ---- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.schiene a'));
  var ziele = links.map(function(a){ return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  if ('IntersectionObserver' in window && ziele.length){
    var beobachter = new IntersectionObserver(function(eintraege){
      eintraege.forEach(function(e){
        if (!e.isIntersecting) return;
        links.forEach(function(a){ a.classList.toggle('aktiv', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    ziele.forEach(function(z){ beobachter.observe(z); });
  }
})();
</script>
'''

FUSS = '''<footer class="site-footer">
  <p>Physik begreifbar · Lehrmittel für die Berufsmaturität Technik, Architektur, Life Sciences · RLP-BM 2030</p>
  <p>Leitprogramm · Statik</p>
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.1 · Stand 6. Oktober 2026</p>
</footer>

<script src="../physiklib.js"></script>
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script>buildNav({ id: 'leitprogramme' });</script>
</body>
</html>
'''


# ------------------------------------------------------------------ Bausteine
def transkript(datei):
    """Gesprochener Text des Clips zum Nachlesen (Klasse aus style.css), aus
    clips/sprechertext-<clip>.txt — die Datei schreibt build-clips.py bei jedem Bau."""
    zeilen = []
    if not os.path.exists(R + 'clips/sprechertext-' + datei + '.txt'):
        return ''
    for z in open(R + 'clips/sprechertext-' + datei + '.txt', encoding='utf-8').read().splitlines():
        if not z.strip():
            continue
        t, text = z.split('\t', 1)
        s = int(float(t))
        zeilen.append(f'<li><span class="tk-zeit">{s // 60}:{s % 60:02d}</span><span>{text}</span></li>')
    return ('<details class="clip-transkript"><summary>Transkript</summary><ol>'
            + ''.join(zeilen) + '</ol></details>')


def clipkarte(datei, titel, zeit=None):
    """Ohne Laufzeit: aus den gemessenen Szenendauern im Drehbuch (gerundet wie build-clips.py)."""
    if zeit is None and not os.path.exists(R + 'clips/' + datei + '.json'):
        zeit = '0:00'
    if zeit is None:
        import json
        d = json.load(open(R + 'clips/' + datei + '.json', encoding='utf-8'))
        s = round(sum(x.get('dauer', 0) for x in d['szenen']))
        zeit = f'{s // 60}:{s % 60:02d}'
    return f'''<div class="clipkarte" data-clip="clips/{datei}.html" data-titel="{titel}">
        <button class="clip-start" type="button">
          <span class="clip-play" aria-hidden="true">▶</span>
          <span class="clip-txt"><span class="clip-titel">{titel}</span></span>
          <span class="clip-zeit">{zeit}</span>
        </button>
        {transkript(datei)}
      </div>'''


def uebung(typ, titel):
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def regler(sim, p, label, mn, mx, st, val, einheit, stellen=0):
    return (f'<div class="regler"><label for="{sim}-{p}">{label}</label>'
            f'<input type="range" id="{sim}-{p}" data-p="{p}" data-einheit="{einheit}" data-stellen="{stellen}" '
            f'min="{mn}" max="{mx}" step="{st}" value="{val}"><span class="regler-wert"></span></div>')


def knoepfe(p, titel, optionen, aktiv):
    b = ''.join('<button type="button" data-wert="%s"%s>%s</button>' % (w, ' class="aktiv"' if w == aktiv else '', t)
                for w, t in optionen)
    return f'<div class="sim-knoepfe" data-p="{p}" role="group" aria-label="{titel}"><span>{titel}:</span>{b}</div>'


def test(tid, titel, punkte, aufgaben, zwei=False):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        lis.append(f'''          <li>
            <div class="a-frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte)
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">· {punkte} P</span></h3>
          <span class="werkz"><button type="button" class="alle-loesungen">alle Lösungen</button><label title="Aufgaben auf Papier gelöst und mit den Lösungen verglichen — ob alles sitzt, zeigt der Gesamttest."><input type="checkbox" class="erledigt" aria-label="Aufgaben dieses Kapitels bearbeitet"> bearbeitet</label></span>
        </div>
        <ol class="aufg{' zwei' if zwei else ''}">
{chr(10).join(lis)}
        </ol>
      </div>'''


def kapitel(n, kid, titel, komp, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">4.4 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> Tüfteln</p>
{sim}

      <p class="phase"><span>③</span> Kontrollfragen</p>
      {clipkarte(*clip2)}

      <h3>Festhalten</h3>
{festhalten}

      <p class="phase"><span>④</span> Üben mit Rückmeldung</p>
      <div class="duo">
        {ue}
      </div>

      <p class="phase"><span>⑤</span> Aufgaben mit Lösungen</p>
{aufgaben}
      <p class="ausf">Mehr dazu: {mehr}</p>
    </section>'''


def figur_anim(sid, label, svg_box, inhalt, knoepfe=''):
    """Simulation mit laufender Animation: Aktionsknöpfe (Start, Zurück …) setzt seite.js in .sim-aktionen."""
    return f'''      <figure class="sim sim-gross" id="{sid}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="{svg_box}" role="img" aria-label="{label}"></svg>
        <div class="sim-aktionen"></div>{knoepfe}
{inhalt}
      </figure>'''


def figur(sid, label, svg_box, inhalt, hilfs=None):
    h = f'\n        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien ({hilfs})</label>' if hilfs else ''
    return f'''      <figure class="sim sim-gross" id="{sid}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="{svg_box}" role="img" aria-label="{label}"></svg>{h}
{inhalt}
      </figure>'''


def linien_bild(punkte, x0, x1, y0, y1, xt, yt, label, xname, yname, cls='kurve-v', waagrecht=None, weitere=()):
    """Diagramm für Aufgaben: Streckenzug durch die Punkte, Gitter je xt und yt, Achsen mit Einheit."""
    w, h, ox, oy = 250, 150, 38, 126
    kx, ky = (w - ox - 16) / (x1 - x0), (oy - 18) / (y1 - y0)
    X = lambda x: ox + (x - x0) * kx
    Y = lambda y: oy - (y - y0) * ky
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 8}" role="img" aria-label="{label}">']
    x = x0
    while x <= x1 + 1e-9:
        t.append(f'<line x1="{X(x):.1f}" y1="{Y(y1):.1f}" x2="{X(x):.1f}" y2="{oy}" class="gitter"/>')
        if x != x0: t.append(f'<text x="{X(x):.1f}" y="{oy + 13}" text-anchor="middle" class="skala">{x:g}</text>')
        x += xt
    y = y0
    while y <= y1 + 1e-9:
        t.append(f'<line x1="{ox}" y1="{Y(y):.1f}" x2="{X(x1):.1f}" y2="{Y(y):.1f}" class="gitter"/>')
        t.append(f'<text x="{ox - 5}" y="{Y(y) + 4:.1f}" text-anchor="end" class="skala">{y:g}</text>')
        y += yt
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{X(x1) + 8:.1f}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{Y(y1) - 8:.1f}" class="achse"/>')
    if waagrecht is not None:
        t.append(f'<line x1="{ox}" y1="{Y(waagrecht):.1f}" x2="{X(x1):.1f}" y2="{Y(waagrecht):.1f}" class="vorher"/>')
    for pk, ck in [(punkte, cls)] + list(weitere):     # weitere Kurven: [(punkte, klasse), …]
        t.append('<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in pk) + f'" class="kurve-mini {ck}"/>')
    t.append(f'<text x="{X(x1) + 8:.1f}" y="{oy - 6}" text-anchor="end" class="achsname">{tief(xname)}</text><text x="{ox + 6}" y="{Y(y1) - 2:.1f}" class="achsname">{tief(yname)}</text></svg>')
    return ''.join(t)




def vek_bild(vektoren, g, t, label, namen=None, achse='N'):
    """Kräfte als Pfeile vom Ursprung im Gitter: Fenster ±g, Gitter je t (Komponenten zum Ablesen)."""
    w = 200
    k = (w / 2 - 16) / g
    X = lambda x: w / 2 + x * k
    Y = lambda y: w / 2 - y * k
    o = [f'<svg class="mini" viewBox="0 0 {w} {w}" role="img" aria-label="{label}">']
    v = -g
    while v <= g + 1e-9:
        o.append(f'<line x1="{X(v):.1f}" y1="{Y(g):.1f}" x2="{X(v):.1f}" y2="{Y(-g):.1f}" class="gitter"/><line x1="{X(-g):.1f}" y1="{Y(v):.1f}" x2="{X(g):.1f}" y2="{Y(v):.1f}" class="gitter"/>')
        v += t
    o.append(f'<line x1="{X(-g):.1f}" y1="{Y(0):.1f}" x2="{X(g) + 6:.1f}" y2="{Y(0):.1f}" class="achse"/><line x1="{X(0):.1f}" y1="{Y(-g):.1f}" x2="{X(0):.1f}" y2="{Y(g) - 6:.1f}" class="achse"/>')
    for q in (t, 2 * t):
        if q <= g:
            o.append(f'<text x="{X(q):.1f}" y="{Y(0) + 12:.1f}" text-anchor="middle" class="skala">{q:g}</text><text x="{X(0) - 4:.1f}" y="{Y(q) + 3.5:.1f}" text-anchor="end" class="skala">{q:g}</text>')
    for i, (vx, vy) in enumerate(vektoren):
        x2, y2 = X(vx), Y(vy)
        L = math.hypot(x2 - X(0), y2 - Y(0)); ux, uy = (x2 - X(0)) / L, (y2 - Y(0)) / L
        o.append(f'<line x1="{X(0):.1f}" y1="{Y(0):.1f}" x2="{x2 - ux * 6:.1f}" y2="{y2 - uy * 6:.1f}" class="vek-mini"/>')
        o.append(f'<polygon points="{x2:.1f},{y2:.1f} {x2 - ux * 8 - uy * 3.6:.1f},{y2 - uy * 8 + ux * 3.6:.1f} {x2 - ux * 8 + uy * 3.6:.1f},{y2 - uy * 8 - ux * 3.6:.1f}" class="vek-kopf"/>')
        if namen:
            o.append(f'<text x="{x2 + ux * 9 - uy * 2:.1f}" y="{y2 + uy * 9 + 4:.1f}" text-anchor="middle" class="mini-name">{namen[i]}</text>')
    o.append(f'<text x="{w - 4}" y="{Y(0) - 5:.1f}" text-anchor="end" class="achsname">{tief('F_x [' + achse + ']')}</text><text x="{X(0) + 6:.1f}" y="12" class="achsname">{tief('F_y [' + achse + ']')}</text></svg>')
    return ''.join(o)


def tief(s):
    """«F_y [N]» für SVG-Text: Index tiefgestellt (wie stext in seite.js)."""
    import re as _re
    return _re.sub(r'_([A-Za-z0-9,]+)(.*)', r'<tspan dy="3" font-size="0.78em">\1</tspan><tspan dy="-3">\2</tspan>', s)


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P01 = '../themen/p0-1-vorwissen-mathematik.html'
P02 = '../themen/p0-2-vorwissen-physik.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 4.2</span><span class="zeit">≈ 15 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Gewichtskraft aus 4.2, Sinus, Kosinus und Tangens im rechtwinkligen Dreieck, Gleichungen umstellen, Einheiten umrechnen. Wenn das wackelt: <a href="leitprogramm-dynamik.html">Leitprogramm Dynamik</a> und <a href="leitprogramm-rechnen.html">Leitprogramm Rechnen</a>.</p>
      <div class="merk-box">
        <p><b>Winkelfunktionen im rechtwinkligen Dreieck.</b> Zum Winkel \\(\\alpha\\) gehören die Ankathete (liegt am Winkel), die Gegenkathete (liegt ihm gegenüber) und die Hypotenuse (gegenüber dem rechten Winkel):</p>
        <p>\\[ \\cos\\alpha = \\frac{\\text{Ankathete}}{\\text{Hypotenuse}} \\qquad \\sin\\alpha = \\frac{\\text{Gegenkathete}}{\\text{Hypotenuse}} \\qquad \\tan\\alpha = \\frac{\\text{Gegenkathete}}{\\text{Ankathete}} \\]</p>
        <p>Rückwärts liefert die Umkehrfunktion den Winkel, etwa \\(\\alpha = \\arctan 0.5 \\approx 26.6^\\circ\\) (Taste \\(\\tan^{-1}\\)). Der Taschenrechner muss auf Grad stehen (DEG), nicht auf Bogenmass (RAD).</p>
      </div>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Wie gross ist die Gewichtskraft auf einen Rucksack von \(15\;\text{kg}\)?',
     r'<p>\(F_G = m \cdot g\) \(= 15\;\text{kg} \cdot 9.81\;\text{m/s}^2\) \(\approx 147\;\text{N}\).</p><p class="komm">Falsch? <a href="leitprogramm-dynamik.html#k3">Leitprogramm Dynamik, Kapitel 3</a></p>', ''),
    ('0b', 3, r'Ein rechtwinkliges Dreieck hat die Hypotenuse \(10\;\text{cm}\) und den Winkel \(\alpha = 35^\circ\). Wie lang sind die Ankathete und die Gegenkathete von \(\alpha\)?',
     r'<p>Ankathete: \(10\;\text{cm} \cdot \cos 35^\circ\) \(\approx 8.19\;\text{cm}\). Gegenkathete: \(10\;\text{cm} \cdot \sin 35^\circ\) \(\approx 5.74\;\text{cm}\).</p><p class="komm">Falsch? Taschenrechner auf DEG? Sonst den Kasten oben nochmals lesen.</p>', ''),
    ('0c', 3, r'Stelle \(a = b \cdot c\) nach \(c\) um, \(p \cdot L = q \cdot x\) nach \(x\) und \(\tan\alpha = k\) nach \(\alpha\).',
     r'<p>\(c = \dfrac{a}{b}\), \(x = \dfrac{p \cdot L}{q}\), \(\alpha = \arctan k\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umstellen</a></p>', ''),
    ('0d', 2, r'Rechne um: \(18\;\text{cm}\) in Meter und \(2.5\;\text{kN}\) in Newton.',
     r'<p>\(18\;\text{cm} = 0.18\;\text{m}\), \(2.5\;\text{kN} = 2500\;\text{N}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#praefixe">Vorwissen 0.2, Vorsilben</a> · <a href="../werkzeuge/einheitentrainer.html">Einheitentrainer</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Eine Kraft dreht sich im x-y-System; ihre Komponenten Fx und Fy wachsen und schrumpfen mit; darunter zeichnen beide ihre Spur über dem Winkel', '-4 -4 308 376',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'F', '<i>F</i> Betrag', 0, 200, 10, 100, 'N', 0) + '\n          '
    + regler('s1', 'phi', '<i>φ</i> Winkel', 0, 360, 5, 60, '°', 0) + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Kraft als Vektor</div>
          <p>Eine <b>Kraft</b> verformt einen Körper oder ändert seinen Bewegungszustand. Einheit: das Newton, \(1\;\text{N} = 1\;\text{kg} \cdot \text{m/s}^2\). Eine Kraft ist ein <b>Vektor</b>: Sie hat einen Betrag, eine Richtung und einen Angriffspunkt. Man zeichnet sie als Pfeil; die Gerade durch den Pfeil heisst <b>Wirkungslinie</b>. Längs der Wirkungslinie darf man eine Kraft an einem starren Körper verschieben, quer dazu nicht.</p>
          <p>Mit dem Winkel \(\varphi\) zur positiven \(x\)-Achse (gegen den Uhrzeigersinn) zerlegt man sie in <b>Komponenten</b>; rückwärts gibt Pythagoras den Betrag:</p>
          <p>\[ F_x = F \cdot \cos\varphi \qquad F_y = F \cdot \sin\varphi \qquad F = \sqrt{F_x^2 + F_y^2} \]</p>
          <p>Die Vorzeichen ergeben sich von selbst: nach links \(F_x < 0\), nach unten \(F_y < 0\). Den Winkel liefert \(\tan\varphi = \dfrac{F_y}{F_x}\) — der Taschenrechner gibt aber nur Winkel zwischen \(-90^\circ\) und \(90^\circ\). Darum zuerst skizzieren: Zeigt die Kraft nach links, zählt man \(180^\circ\) dazu, zeigt sie nach rechts unten, \(360^\circ\).</p>
          <p>Kennt man nur den Betrag und <em>eine</em> Komponente, liefert Pythagoras die andere nur bis aufs Vorzeichen, etwa \(F_y = \pm\sqrt{F^2 - F_x^2}\): Es gibt <b>zwei mögliche Richtungen</b>, spiegelbildlich zur Achse. Erst eine Skizze oder eine weitere Angabe entscheidet.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Komponenten addiert statt mit Pythagoras: \(F_x = 30\;\text{N}\) und \(F_y = 40\;\text{N}\) geben \(\sqrt{(30\;\text{N})^2 + (40\;\text{N})^2} = 50\;\text{N}\), nicht \(70\;\text{N}\).</p>
          <p>Sinus und Kosinus vertauscht: Die Komponente <em>am</em> Winkel gehört zum Kosinus. Und der Taschenrechner muss auf Grad (DEG) stehen.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Was ist eine Kraft? Nenne ihre zwei Wirkungen und die drei Angaben, die eine Kraft festlegen. Begründe am Beispiel eines Fussballs, warum der Betrag allein nicht genügt.',
     r'<p>Eine Kraft verformt einen Körper oder ändert seinen Bewegungszustand (schneller, langsamer, andere Richtung). Festgelegt ist sie durch Betrag, Richtung und Angriffspunkt.</p><p>Fussball: Derselbe kräftige Stoss schickt den Ball nach vorn oder zur Seite, je nach Richtung. Trifft er den Ball mittig, fliegt er gerade; trifft er ihn seitlich, dreht er sich zusätzlich — Richtung und Angriffspunkt entscheiden mit.</p>', ''),
    ('1b', 3, r'Ein Kind zieht einen Schlitten an einer Schnur mit \(90\;\text{N}\); die Schnur steigt unter \(25^\circ\) zur Waagrechten an. Wie gross sind die waagrechte und die senkrechte Komponente? Was bewirkt jede?',
     r'<p>\(F_x = F \cdot \cos\varphi\) \(= 90\;\text{N} \cdot \cos 25^\circ\) \(\approx 81.6\;\text{N}\), \(F_y = F \cdot \sin\varphi\) \(= 90\;\text{N} \cdot \sin 25^\circ\) \(\approx 38.0\;\text{N}\).</p><p>Die waagrechte Komponente zieht den Schlitten vorwärts. Die senkrechte zieht ihn nach oben und entlastet den Boden: Die Normalkraft wird kleiner.</p>', ''),
    ('1c', 3, r'Das Bild zeigt eine Kraft im Gitter (ein Feld \(10\;\text{N}\)). Lies ihre Komponenten ab und berechne Betrag und Richtungswinkel \(\varphi\).',
     r'<p>Abgelesen: \(F_x = -30\;\text{N}\), \(F_y = 20\;\text{N}\). \(F = \sqrt{F_x^2 + F_y^2}\) \(= \sqrt{(-30\;\text{N})^2 + (20\;\text{N})^2}\) \(\approx 36.1\;\text{N}\).</p><p>\(\arctan\dfrac{20\;\text{N}}{-30\;\text{N}} \approx -33.7^\circ\); die Kraft zeigt nach links oben, also \(\varphi = -33.7^\circ + 180^\circ\) \(\approx 146.3^\circ\).</p>',
     '\n            <div class="mini-reihe">' + vek_bild([(-30, 20)], 50, 10, 'Kraftpfeil im Gitter vom Ursprung nach links oben, Spitze bei Fx gleich minus 30 N und Fy gleich 20 N', ['F']) + '</div>'),
    ('1d', 3, r'Ein Spannseil zieht an einem Zeltpfahl mit den Komponenten \(F_x = 240\;\text{N}\) und \(F_y = -70\;\text{N}\). Wie gross ist die Seilkraft, und in welche Richtung zieht sie (Winkel \(\varphi\) zwischen \(0^\circ\) und \(360^\circ\))?',
     r'<p>\(F = \sqrt{F_x^2 + F_y^2}\) \(= \sqrt{(240\;\text{N})^2 + (70\;\text{N})^2}\) \(= 250\;\text{N}\).</p><p>\(\arctan\dfrac{-70}{240} \approx -16.3^\circ\); nach rechts unten heisst das \(\varphi \approx 343.7^\circ\).</p>', ''),
])
k1 = kapitel(1, 'kraft-vektor', 'Kraft als Vektor', 'K1', 50,
    r'Du definierst die Kraft, stellst sie als Pfeil mit Betrag, Richtung und Angriffspunkt dar und zerlegst sie in die Komponenten \(F_x = F \cdot \cos\varphi\) und \(F_y = F \cdot \sin\varphi\).',
    ('p4-4-lp-vektor', 'Statik sehen: die Kraft als Pfeil'),
    sim1, ('p4-4-lp-kontrolle-vektor', 'Kontrollfragen zur Kraft als Vektor'),
    fest1, [uebung('komponenten', 'Komponenten einer Kraft'), uebung('betrag', 'Betrag aus den Komponenten'), uebung('winkel', 'Richtung aus den Komponenten')],
    auf1, f'<a href="{TS}#definition">Themenseite 4.4, Grundbegriffe</a> · <a href="{TS}#komponenten">Kraft als Vektor</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur_anim('sim2', 'Bis zu drei Kräfte greifen an einem Ring an; auf Knopfdruck wandern die Pfeile Spitze an Fuss, die Resultierende erscheint, und der Ring bewegt sich in ihre Richtung oder bleibt in Ruhe', '-4 -4 308 308',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'F1', '<i>F</i>₁', 0, 200, 10, 100, 'N', 0) + '\n          '
    + regler('s2', 'p1', '<i>φ</i>₁', 0, 355, 5, 0, '°', 0) + '\n          '
    + regler('s2', 'F2', '<i>F</i>₂', 0, 200, 10, 80, 'N', 0) + '\n          '
    + regler('s2', 'p2', '<i>φ</i>₂', 0, 355, 5, 90, '°', 0) + '\n          '
    + regler('s2', 'F3', '<i>F</i>₃', 0, 200, 10, 0, 'N', 0) + '\n          '
    + regler('s2', 'p3', '<i>φ</i>₃', 0, 355, 5, 225, '°', 0) + '\n        </div>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Resultierende Kraft</div>
          <p>Greifen mehrere Kräfte am selben Punkt an, wirken sie zusammen wie eine einzige Kraft, die <b>Resultierende</b> \(\vec{F}_\text{res}\) (die Themenseite schreibt auch \(\vec{F}_R\); hier heisst \(F_R\) die Reibung). Sie ist die Vektorsumme:</p>
          <p>\[ \vec{F}_\text{res} = \vec{F}_1 + \vec{F}_2 + \ldots \qquad F_{\text{res},x} = \sum F_x \qquad F_{\text{res},y} = \sum F_y \]</p>
          <p><b>Grafisch:</b> die Pfeile Spitze an Fuss aneinanderhängen; der Pfeil vom ersten Fuss zur letzten Spitze ist \(\vec{F}_\text{res}\). Bei zwei Kräften gibt das Kräfteparallelogramm dasselbe. <b>Rechnerisch:</b> Komponenten addieren, dann \(F_\text{res} = \sqrt{F_{\text{res},x}^2 + F_{\text{res},y}^2}\).</p>
          <p>Nur gleichgerichtete Beträge darf man addieren, entgegengesetzte subtrahieren. Ist \(\vec{F}_\text{res} = \vec{0}\), schliessen sich die Pfeile zu einem Krafteck: Ein ruhender Körper bleibt in Ruhe — das <b>Kräftegleichgewicht</b>.</p>
          <p><b>Last an zwei Seilen:</b> Hängt eine Last in der Mitte zweier gleich langer Seile, die beide unter \(\alpha\) zur Waagrechten ansteigen, heben sich die waagrechten Komponenten der Seilkräfte auf, die senkrechten tragen zusammen die Gewichtskraft:</p>
          <p>\[ 2 \cdot F_S \cdot \sin\alpha = m \cdot g \]</p>
          <p>Je flacher die Seile, desto kleiner \(\sin\alpha\) — und desto grösser die Seilkraft \(F_S\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Beträge addiert, obwohl die Kräfte verschieden gerichtet sind: \(90\;\text{N}\) nach Norden und \(40\;\text{N}\) nach Osten ergeben rund \(98.5\;\text{N}\), nicht \(130\;\text{N}\).</p>
          <p>Pythagoras mit den Beträgen gerechnet, obwohl die Kräfte nicht rechtwinklig stehen: erst die Komponenten addieren.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Zwei Hunde ziehen an einem Spielzeug: der eine mit \(120\;\text{N}\) nach Osten, der andere mit \(50\;\text{N}\) nach Norden. Wie gross ist die Resultierende, und unter welchem Winkel zur Ostrichtung zeigt sie?',
     r'<p>\(F_\text{res} = \sqrt{F_1^2 + F_2^2}\) \(= \sqrt{(120\;\text{N})^2 + (50\;\text{N})^2}\) \(= 130\;\text{N}\).</p><p>\(\tan\varphi = \dfrac{50\;\text{N}}{120\;\text{N}}\), \(\varphi \approx 22.6^\circ\) nördlich von Osten.</p>', ''),
    ('2b', 3, r'Drei Kräfte greifen an einem Punkt an (Bild, ein Feld \(10\;\text{N}\)). Lies die Komponenten ab und bestimme die Resultierende nach Betrag und Richtung.',
     r'<p>\(F_1 = (30\;\text{N};\, 20\;\text{N})\), \(F_2 = (-10\;\text{N};\, 30\;\text{N})\), \(F_3 = (20\;\text{N};\, -30\;\text{N})\). \(F_{\text{res},x} = 30\;\text{N} - 10\;\text{N} + 20\;\text{N}\) \(= 40\;\text{N}\), \(F_{\text{res},y} = 20\;\text{N} + 30\;\text{N} - 30\;\text{N}\) \(= 20\;\text{N}\).</p><p>\(F_\text{res} = \sqrt{(40\;\text{N})^2 + (20\;\text{N})^2}\) \(\approx 44.7\;\text{N}\), \(\varphi = \arctan\dfrac{20}{40}\) \(\approx 26.6^\circ\).</p>',
     '\n            <div class="mini-reihe">' + vek_bild([(30, 20), (-10, 30), (20, -30)], 50, 10, 'Drei Kraftpfeile vom Ursprung: F1 nach rechts oben bei 30 und 20, F2 nach links oben bei minus 10 und 30, F3 nach rechts unten bei 20 und minus 30', ['F₁', 'F₂', 'F₃']) + '</div>'),
    ('2c', 3, r'Eine Hängelampe (\(6\;\text{kg}\)) hängt in der Mitte zweier gleich langer Seile, die beide unter \(30^\circ\) zur Waagrechten ansteigen. Skizziere den Knoten mit allen Kräften, die an ihm angreifen, als Pfeile. Wie gross ist die Kraft in jedem Seil? Begründe, warum sie gleich gross ist wie die Gewichtskraft der Lampe.',
     r'<p>Skizze: am Knoten die Gewichtskraft der Lampe senkrecht nach unten und die beiden Seilkräfte längs der Seile schräg nach links oben und rechts oben, gleich lang. Am Knoten herrscht Gleichgewicht. Die waagrechten Komponenten der Seile heben sich auf, die senkrechten tragen die Lampe: \(2 \cdot F_S \cdot \sin 30^\circ = m \cdot g\).</p><p>\(F_S = \dfrac{6\;\text{kg} \cdot 9.81\;\text{m/s}^2}{2 \cdot \sin 30^\circ}\) \(\approx 58.9\;\text{N}\). Weil \(2 \cdot \sin 30^\circ = 1\) ist, trägt jedes Seil senkrecht nur die Hälfte, muss dafür aber mit der ganzen Gewichtskraft ziehen.</p>', ''),
    ('2d', 3, r'Ein Schiff wird von zwei Schleppern gezogen, je \(40\;\text{kN}\), unter \(20^\circ\) links und \(20^\circ\) rechts der Fahrtrichtung. Wie gross ist die Resultierende? Begründe, warum die Schlepper den Winkel möglichst klein halten.',
     r'<p>Die Querkomponenten heben sich auf, die Längskomponenten addieren sich: \(F_\text{res} = 2 \cdot 40\;\text{kN} \cdot \cos 20^\circ\) \(\approx 75.2\;\text{kN}\).</p><p>Je grösser der Winkel, desto kleiner \(\cos\) des Winkels: Bei \(40^\circ\) wären es nur \(\approx 61.3\;\text{kN}\). Die Querkomponenten heben sich nur auf, sie bringen das Schiff nicht vorwärts.</p>', ''),
])
k2 = kapitel(2, 'resultierende', 'Die resultierende Kraft', 'K4', 50,
    r'Du stellst alle Kräfte auf einen Körper als Pfeile dar, setzt sie grafisch (Spitze an Fuss) und rechnerisch (Komponenten) zur Resultierenden zusammen und erkennst das Kräftegleichgewicht \(\vec{F}_\text{res} = \vec{0}\).',
    ('p4-4-lp-resultierende', 'Statik sehen: Kräfte aneinanderhängen'),
    sim2, ('p4-4-lp-kontrolle-resultierende', 'Kontrollfragen zur resultierenden Kraft'),
    fest2, [uebung('res-recht', 'Zwei Kräfte im rechten Winkel'), uebung('res-zwei', 'Zwei Kräfte unter einem Winkel'), uebung('seil', 'Last an zwei Seilen')],
    auf2, f'<a href="{TS}#resultierende">Themenseite 4.4, Resultierende</a> · <a href="{TS}#punkt">Kräftegleichgewicht am Punkt</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Kiste auf einer Rampe, die sich auf Knopfdruck neigt; Gewichtskraft, Normalkraft, Haftreibung und die Komponenten der Gewichtskraft; darunter die Kräfte über dem Neigungswinkel', '-4 -4 308 368',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'm', '<i>m</i> Masse', 5, 40, 1, 10, 'kg', 0) + '\n          '
    + regler('s3', 'mu', '<i>μ</i><sub>H</sub> Haftreibung', 0.1, 1, 0.05, 0.3, '', 2) + '\n          '
    + regler('s3', 'ae', '<i>α</i> neigen bis', 0, 45, 1, 15, '°', 0) + '\n        </div>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Kräfte an einem ruhenden Körper</div>
          <ul>
            <li><b>Gewichtskraft</b> \(\vec{F}_G\) (im Lehrplan «Schwerkraft»): Die Erde zieht den Körper an, senkrecht nach unten, greift im Schwerpunkt an, \(F_G = m \cdot g\).</li>
            <li><b>Normalkraft</b> (Auflagerkraft) \(\vec{F}_N\): senkrecht zur Auflagefläche, von ihr weg. Sie ist so gross, dass der Körper nicht in die Unterlage einsinkt.</li>
            <li><b>Haftreibung</b> \(\vec{F}_R\) (eine Reibungskraft): längs der Fläche, der drohenden Bewegung entgegen. Sie ist nur so gross wie nötig, höchstens \(F_R \le \mu_H \cdot F_N\) (\(\mu_H\): Haftreibungszahl, ohne Einheit).</li>
          </ul>
          <p>Auf der <b>schiefen Ebene</b> zerlegt man die Gewichtskraft längs und senkrecht zur Ebene:</p>
          <p>\[ F_H = F_G \cdot \sin\alpha \qquad F_N = F_G \cdot \cos\alpha \]</p>
          <p>Der Körper ruht, solange die Haftreibung die Hangabtriebskraft \(F_H\) ausgleichen kann. Daraus folgt die Haftbedingung \(\tan\alpha \le \mu_H\); die Masse kürzt sich.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Auf der schiefen Ebene \(F_N = F_G\) gesetzt: Das gilt nur waagrecht. Schief ist \(F_N = F_G \cdot \cos\alpha\), kleiner als \(F_G\).</p>
          <p>Die Haftreibung immer gleich \(\mu_H \cdot F_N\) gesetzt: Das ist nur ihr Höchstwert. Eine Kiste auf waagrechtem Boden, an der niemand zieht, hat gar keine Reibung.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Ein Buch liegt auf einem schräg gestellten Pult und rutscht nicht. Zähle alle Kräfte auf, die auf das Buch wirken, mit Richtung und Angriffspunkt (Skizze). Wie gross ist ihre Summe? Begründe.',
     r'<p>Gewichtskraft (senkrecht nach unten, im Schwerpunkt), Normalkraft (senkrecht zur Pultfläche, nach oben weg von der Fläche, an der Auflagefläche), Haftreibung (längs der Pultfläche hangaufwärts, an der Auflagefläche).</p><p>Die Summe ist null: Das Buch ruht, also herrscht Kräftegleichgewicht. Die Haftreibung gleicht die Hangabtriebskraft aus, die Normalkraft die Komponente der Gewichtskraft senkrecht zum Pult.</p>', ''),
    ('3b', 3, r'Fahrer und Velo (zusammen \(90\;\text{kg}\)) stehen mit angezogenen Bremsen auf einer Strasse mit \(12^\circ\) Neigung. Wie gross sind Normalkraft und Hangabtriebskraft? Hält die Haftreibung, wenn \(\mu_H = 0.7\) ist (Gummi auf trockenem Asphalt)?',
     r'<p>\(F_G = m \cdot g\) \(= 90\;\text{kg} \cdot 9.81\;\text{m/s}^2\) \(\approx 883\;\text{N}\). \(F_N = F_G \cdot \cos\alpha\) \(\approx 864\;\text{N}\), \(F_H = F_G \cdot \sin\alpha\) \(\approx 184\;\text{N}\).</p><p>Höchstens \(\mu_H \cdot F_N = 0.7 \cdot 864\;\text{N}\) \(\approx 605\;\text{N}\) — weit mehr als nötig. Oder kürzer: \(\tan 12^\circ \approx 0.21 \le 0.7\). Das Velo hält.</p>', ''),
    ('3c', 3, r'Das Diagramm zeigt für einen Klotz mit \(F_G = 100\;\text{N}\) die Hangabtriebskraft (violett) und die grösste Haftreibung \(\mu_H \cdot F_N\) (türkis gestrichelt) über dem Neigungswinkel. Bis zu welchem Winkel haftet der Klotz? Wie gross ist \(\mu_H\)? Prüfe mit \(\tan\alpha = \mu_H\).',
     r'<p>Er haftet, solange die violette Kurve unter der türkisen liegt: bis zum Schnittpunkt bei rund \(22^\circ\).</p><p>Bei \(\alpha = 0^\circ\) ist \(F_N = F_G = 100\;\text{N}\) und die Grenze \(40\;\text{N}\), also \(\mu_H = \dfrac{40\;\text{N}}{100\;\text{N}} = 0.4\). Probe: \(\arctan 0.4 \approx 21.8^\circ\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(a, 100 * math.sin(a * 3.14159265 / 180)) for a in range(0, 46, 3)], 0, 45, 0, 80, 5, 10, 'Zwei Kurven über dem Neigungswinkel: Hangabtriebskraft steigt von 0 auf rund 71 N, die grösste Haftreibung fällt von 40 N auf rund 28 N; sie schneiden sich bei rund 22 Grad', 'α [°]', 'F [N]', 'kurve-fh', weitere=[([(a, 40 * math.cos(a * 3.14159265 / 180)) for a in range(0, 46, 3)], 'kurve-fr')]) + '</div>'),
    ('3d', 3, r'Eine Kiste (\(50\;\text{kg}\)) steht auf waagrechtem Boden, \(\mu_H = 0.45\). Du schiebst waagrecht mit \(120\;\text{N}\), sie bewegt sich nicht. Wie gross ist die Reibungskraft? Ab welcher Schubkraft rutscht sie? Begründe, warum die Reibung nicht immer \(\mu_H \cdot F_N\) ist.',
     r'<p>Die Kiste ruht, also \(\sum F_x = 0\): Die Haftreibung ist \(120\;\text{N}\), so gross wie deine Kraft.</p><p>Höchstens \(\mu_H \cdot F_N = 0.45 \cdot 50\;\text{kg} \cdot 9.81\;\text{m/s}^2\) \(\approx 221\;\text{N}\); erst darüber rutscht sie. \(\mu_H \cdot F_N\) ist die Grenze, keine feste Kraft — die Haftreibung passt sich an, bis die Grenze erreicht ist.</p>', ''),
])
k3 = kapitel(3, 'ruhender-koerper', 'Kräfte am ruhenden Körper', 'K3 · K5', 50,
    r'Du zählst die Kräfte an einem ruhenden Körper auf — Gewichtskraft, Normalkraft, Haftreibung —, charakterisierst sie und zeigst das Gleichgewicht auf der waagrechten und der schiefen Ebene mit \(F_H = F_G \cdot \sin\alpha\), \(F_N = F_G \cdot \cos\alpha\) und \(\tan\alpha \le \mu_H\).',
    ('p4-4-lp-ruhe', 'Statik sehen: Gewicht, Normalkraft und Haftreibung'),
    sim3, ('p4-4-lp-kontrolle-ruhe', 'Kontrollfragen zu den Kräften am ruhenden Körper'),
    fest3, [uebung('zerlegen', 'Kräfte auf der schiefen Ebene'), uebung('grenzwinkel', 'Grenzwinkel und Haftreibungszahl'), uebung('haftgrenze', 'Haftreibung auf waagrechtem Boden')],
    auf3, f'<a href="{TS}#definition">Themenseite 4.4, Die wesentlichen Kräfte</a> · <a href="{TS}#schiefe-ebene">Schiefe Ebene</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Schraubenschlüssel an einer festsitzenden Schraube; die Zugkraft wächst auf Knopfdruck, der wirksame Hebelarm ist gestrichelt; darunter ein Balken mit dem Drehmoment gegen das Moment, das die Schraube braucht', '-4 -4 308 300',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 'F', '<i>F</i> Kraft', 0, 400, 10, 100, 'N', 0) + '\n          '
    + regler('s4', 'l', '<i>l</i> Schlüssel', 0.1, 0.4, 0.05, 0.2, 'm', 2) + '\n          '
    + regler('s4', 'al', '<i>α</i> Winkel', 0, 90, 5, 90, '°', 0) + '\n        </div>',
    knoepfe('Ml', 'Schraube sitzt mit', [('30', '30 Nm'), ('60', '60 Nm'), ('90', '90 Nm')], '60'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Drehmoment</div>
          <p>Das <b>Drehmoment</b> \(M\) beschreibt die Drehwirkung einer Kraft um eine Drehachse. Es ist Kraft mal <b>wirksamer Hebelarm</b> \(r\), dem senkrechten Abstand der Wirkungslinie von der Drehachse:</p>
          <p>\[ M = F \cdot r = F \cdot l \cdot \sin\alpha \]</p>
          <p>\(l\): Abstand des Angriffspunkts von der Achse, \(\alpha\): Winkel zwischen Hebel und Kraft. Einheit: Newtonmeter, \(\text{Nm}\). Am grössten bei \(\alpha = 90^\circ\); null, wenn die Wirkungslinie durch die Achse geht. Vorzeichen: gegen den Uhrzeigersinn positiv, im Uhrzeigersinn negativ.</p>
          <p><b>Anwendungen:</b> Schraubenschlüssel und Radkreuz, Türgriff, Lenkrad, Velokurbel, Wippe und Hebel, Kran, Motoren (deren Drehmoment im Prospekt steht).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Schlüssel in Zentimeter eingesetzt: \(150\;\text{N}\) an \(20\;\text{cm}\) geben \(150\;\text{N} \cdot 0.2\;\text{m} = 30\;\text{Nm}\), nicht \(3000\).</p>
          <p>Den ganzen Hebel statt des wirksamen Hebelarms genommen, obwohl die Kraft schräg zieht: nur \(r = l \cdot \sin\alpha\) zählt.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Nenne drei Anwendungen des Drehmoments aus dem Alltag. Erkläre bei einer davon, wie man mit kleiner Kraft ein grosses Drehmoment erreicht, und begründe mit \(M = F \cdot r\).',
     r'<p>Zum Beispiel Radkreuz, Türgriff, Lenkrad, Velokurbel, Wippe, Flaschenöffner.</p><p>Radkreuz: Die Radmutter braucht ein festes Drehmoment. Mit langem Arm ist \(r\) gross, also genügt nach \(F = \dfrac{M}{r}\) eine kleine Kraft. Ein doppelt so langer Arm halbiert die nötige Kraft.</p>', ''),
    ('4b', 3, r'Eine Velofahrerin drückt mit \(400\;\text{N}\) senkrecht nach unten auf das Pedal; die Kurbel ist \(17\;\text{cm}\) lang. Wie gross ist das Drehmoment, wenn die Kurbel waagrecht steht? Und wenn sie \(60^\circ\) unter der Waagrechten steht? Warum tritt man ganz unten ins Leere?',
     r'<p>Waagrecht steht die Kraft senkrecht zur Kurbel: \(M = F \cdot l\) \(= 400\;\text{N} \cdot 0.17\;\text{m}\) \(= 68\;\text{Nm}\).</p><p>\(60^\circ\) unter der Waagrechten liegen zwischen Kurbel und Kraft nur noch \(30^\circ\): \(M = 400\;\text{N} \cdot 0.17\;\text{m} \cdot \sin 30^\circ\) \(= 34\;\text{Nm}\). Ganz unten steht die Kurbel senkrecht, die Kraft zeigt längs der Kurbel: Ihre Wirkungslinie geht durch die Achse, \(\sin 0^\circ = 0\), kein Drehmoment.</p>', ''),
    ('4c', 3, r'Das Diagramm zeigt das Drehmoment einer Kraft an einem \(0.25\;\text{m}\) langen Schlüssel über dem Winkel \(\alpha\) zwischen Schlüssel und Kraft. Lies das grösste Drehmoment ab und bestimme daraus die Kraft. Bei welchen Winkeln ist das Drehmoment halb so gross?',
     r'<p>Das grösste Drehmoment ist \(50\;\text{Nm}\) bei \(\alpha = 90^\circ\). Dort ist \(r = l\): \(F = \dfrac{M}{l}\) \(= \dfrac{50\;\text{Nm}}{0.25\;\text{m}}\) \(= 200\;\text{N}\).</p><p>Halb so gross, \(25\;\text{Nm}\), bei \(\sin\alpha = 0.5\): \(\alpha = 30^\circ\) und \(\alpha = 150^\circ\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(a, 50 * math.sin(a * 3.14159265 / 180)) for a in range(0, 181, 5)], 0, 180, 0, 60, 30, 10, 'Drehmoment über dem Winkel: Bogen von 0 Nm bei 0 Grad auf 50 Nm bei 90 Grad und zurück auf 0 Nm bei 180 Grad', 'α [°]', 'M [Nm]', 'kurve-m') + '</div>'),
    ('4d', 3, r'Radmuttern sollen mit \(110\;\text{Nm}\) angezogen werden. Du drückst mit \(250\;\text{N}\) senkrecht auf den Schlüssel. Wie weit von der Mutter musst du drücken? Was ändert sich, wenn du schräg drückst?',
     r'<p>\(r = \dfrac{M}{F}\) \(= \dfrac{110\;\text{Nm}}{250\;\text{N}}\) \(= 0.44\;\text{m}\).</p><p>Schräg ist der wirksame Hebelarm nur \(l \cdot \sin\alpha\), kleiner als \(l\): Man muss weiter aussen greifen oder stärker drücken.</p>', ''),
])
k4 = kapitel(4, 'drehmoment', 'Das Drehmoment', 'K2', 50,
    r'Du definierst das Drehmoment \(M = F \cdot r = F \cdot l \cdot \sin\alpha\) als Kraft mal wirksamen Hebelarm, rechnest damit und nennst Anwendungen.',
    ('p4-4-lp-drehmoment', 'Statik sehen: Kraft mal Hebelarm'),
    sim4, ('p4-4-lp-kontrolle-drehmoment', 'Kontrollfragen zum Drehmoment'),
    fest4, [uebung('moment', 'Drehmoment berechnen'), uebung('kraft', 'Kraft oder Hebelarm'), uebung('losbrechen', 'Schräg am Schlüssel')],
    auf4, f'<a href="{TS}#drehmoment">Themenseite 4.4, Drehmoment</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur_anim('sim5', 'Wippe mit zwei Personen, zuerst waagrecht gehalten; auf Knopfdruck losgelassen, kippt sie zur Seite des grösseren Drehmoments oder bleibt waagrecht; darunter Balken für beide Drehmomente', '-4 -4 308 238',
    '        <div class="reglerfeld">\n          '
    + regler('s5', 'm1', '<i>m</i>₁ links', 10, 60, 1, 35, 'kg', 0) + '\n          '
    + regler('s5', 'r1', '<i>r</i>₁ links', 0.5, 2, 0.1, 1.4, 'm', 1) + '\n          '
    + regler('s5', 'm2', '<i>m</i>₂ rechts', 10, 60, 1, 20, 'kg', 0) + '\n          '
    + regler('s5', 'r2', '<i>r</i>₂ rechts', 0.5, 2, 0.1, 1.5, 'm', 1) + '\n        </div>')
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Hebelgesetz</div>
          <p>Ein Hebel ist im Gleichgewicht, wenn sich die Drehmomente aufheben: Das Moment, das links herum dreht, ist so gross wie das Moment, das rechts herum dreht. Für zwei Kräfte ist das das <b>Hebelgesetz</b>:</p>
          <p>\[ F_1 \cdot r_1 = F_2 \cdot r_2 \]</p>
          <p>Am <b>zweiarmigen</b> Hebel (Wippe, Balkenwaage) liegen die Kräfte auf verschiedenen Seiten der Drehachse, am <b>einarmigen</b> (Schubkarre, Nussknacker) auf derselben Seite. Kraft mal Kraftarm gleich Last mal Lastarm: Ein langer Kraftarm spart Kraft. Bei mehreren Kräften zählt die Summe: \(\sum M = 0\).</p>
          <p>Hängt an jeder Seite eine Masse, kürzt sich \(g\): \(m_1 \cdot r_1 = m_2 \cdot r_2\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Abstand und Masse im gleichen statt im umgekehrten Verhältnis: Das schwerere Kind sitzt <em>näher</em> an der Achse. \(45\;\text{kg}\) bei \(0.8\;\text{m}\) gleichen \(30\;\text{kg}\) bei \(1.2\;\text{m}\) aus, nicht bei \(0.53\;\text{m}\).</p>
          <p>Bei zwei Lasten auf einer Seite die Massen addiert und mit einem einzigen Abstand gerechnet: Jede Last hat ihren eigenen Hebelarm.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Ein Vater (\(80\;\text{kg}\)) und seine Tochter (\(20\;\text{kg}\)) wollen wippen. Die Tochter sitzt ganz aussen, \(2.2\;\text{m}\) von der Achse. Wo muss der Vater sitzen? Begründe, warum er so nah an die Achse muss.',
     r'<p>\(m_1 \cdot r_1 = m_2 \cdot r_2\): \(r_\text{Vater} = \dfrac{20\;\text{kg} \cdot 2.2\;\text{m}}{80\;\text{kg}}\) \(= 0.55\;\text{m}\).</p><p>Er ist viermal so schwer; damit sein Drehmoment nicht grösser wird, braucht er einen viermal kleineren Hebelarm.</p>', ''),
    ('5b', 3, r'Mit einer \(1.2\;\text{m}\) langen Brechstange hebt man einen Stein (\(900\;\text{N}\)). Sie wirkt als <b>zweiarmiger</b> Hebel: Der Drehpunkt (ein untergelegter Klotz) liegt zwischen Stein und Hand, \(0.15\;\text{m}\) vom Stein entfernt; man drückt am anderen Ende senkrecht zur Stange. Welche Kraft braucht es?',
     r'<p>Lastarm \(0.15\;\text{m}\), Kraftarm \(1.2\;\text{m} - 0.15\;\text{m} = 1.05\;\text{m}\).</p><p>\(F \cdot r_K = F_L \cdot r_L\): \(F = \dfrac{900\;\text{N} \cdot 0.15\;\text{m}}{1.05\;\text{m}}\) \(\approx 129\;\text{N}\) — rund ein Siebtel der Last.</p>', ''),
    ('5c', 3, r'Das Diagramm zeigt für eine Wippe, welche Kraft \(F_2\) rechts im Abstand \(r_2\) ein linkes Drehmoment ausgleicht. Wie gross ist das linke Drehmoment? Welche Kraft braucht es bei \(1.2\;\text{m}\)? Wo genügen \(200\;\text{N}\)?',
     r'<p>Jeder Punkt der Kurve hat dasselbe Produkt, zum Beispiel \(F_2 \cdot r_2 = 600\;\text{N} \cdot 0.5\;\text{m} = 300\;\text{Nm}\) — das ist das linke Drehmoment.</p><p>Bei \(1.2\;\text{m}\): \(F_2 = \dfrac{300\;\text{Nm}}{1.2\;\text{m}} = 250\;\text{N}\). \(200\;\text{N}\) genügen bei \(r_2 = \dfrac{300\;\text{Nm}}{200\;\text{N}} = 1.5\;\text{m}\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(r / 20, 300 / (r / 20)) for r in range(10, 41)], 0, 2, 0, 700, 0.5, 100, 'Kraft über dem Abstand: fallende Kurve von 600 N bei 0.5 m über 300 N bei 1 m auf 150 N bei 2 m', 'r₂ [m]', 'F₂ [N]', 'kurve-fg') + '</div>'),
    ('5d', 3, r'Bei einem Nussknacker liegt das Gelenk am Ende. Die Hand drückt \(18\;\text{cm}\) vom Gelenk, die Nuss liegt \(2.5\;\text{cm}\) davon und knackt bei \(300\;\text{N}\). Ist das ein ein- oder ein zweiarmiger Hebel? Welche Handkraft braucht es? Begründe, warum man die Nuss möglichst nah ans Gelenk legt.',
     r'<p>Einarmig: Hand und Nuss liegen auf derselben Seite des Gelenks. \(F \cdot r_K = F_L \cdot r_L\): \(F = \dfrac{300\;\text{N} \cdot 0.025\;\text{m}}{0.18\;\text{m}}\) \(\approx 41.7\;\text{N}\).</p><p>Nah am Gelenk ist der Lastarm kurz. Bei gleichem Kraftarm genügt dann für dasselbe Drehmoment eine kleinere Handkraft.</p>', ''),
])
k5 = kapitel(5, 'hebelgesetz', 'Das Hebelgesetz', 'K5 · K2', 50,
    r'Du wendest das Gleichgewicht der Drehmomente \(F_1 \cdot r_1 = F_2 \cdot r_2\) an Wippe, Brechstange und Schubkarre an und erklärst, warum ein langer Hebelarm Kraft spart.',
    ('p4-4-lp-hebel', 'Statik sehen: das Hebelgesetz'),
    sim5, ('p4-4-lp-kontrolle-hebel', 'Kontrollfragen zum Hebelgesetz'),
    fest5, [uebung('wippe', 'Gleichgewicht auf der Wippe'), uebung('hebel', 'Kraft am Hebel'), uebung('mobile', 'Zwei Kinder auf einer Seite')],
    auf5, f'<a href="{TS}#hebel">Themenseite 4.4, Hebelgesetz</a> · <a href="{TS}#einstieg">Die Wippe</a>')

# ------------------------------------------------------------------ Kapitel 6
sim6 = figur_anim('sim6', 'Ein Wagen fährt auf Knopfdruck über eine Brücke auf zwei Stützen und hält an der Stelle x; die Auflagerkräfte FA und FB passen sich an; darunter ihre Spur über x', '-4 -4 308 340',
    '        <div class="reglerfeld">\n          '
    + regler('s6', 'FL', '<i>F</i><sub>L</sub> Wagen', 10, 200, 10, 60, 'kN', 0) + '\n          '
    + regler('s6', 'FE', '<i>F</i><sub>E</sub> Brücke', 0, 200, 10, 0, 'kN', 0) + '\n          '
    + regler('s6', 'x', '<i>x</i> Halt bei', 0, 10, 0.5, 5, 'm', 1) + '\n        </div>\n'
    + '        <p class="sim-notiz">Stützweite \\(L = 10\\;\\text{m}\\); das Eigengewicht \\(F_E\\) der Brücke greift in ihrer Mitte an.</p>')
fest6 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Statisches Gleichgewicht</div>
          <p>Ein Körper ist im <b>statischen Gleichgewicht</b>, wenn er in Ruhe bleibt: Er verschiebt sich nicht und beginnt sich nicht zu drehen. Dafür müssen zwei Bedingungen zugleich gelten:</p>
          <p>\[ \sum \vec{F} = \vec{0} \qquad \text{und} \qquad \sum M = 0 \]</p>
          <p>Die Kräftebedingung zerfällt in \(\sum F_x = 0\) und \(\sum F_y = 0\). Die Drehachse für die Momente darf man frei wählen — geschickt dort, wo eine unbekannte Kraft angreift, dann fällt sie heraus.</p>
          <p><b>Balken auf zwei Stützen</b> (Stützweite \(L\), Last \(F_L\) im Abstand \(x\) von A): Momente um A geben \(F_B \cdot L = F_L \cdot x\), die Kräfte \(F_A = F_L - F_B\). Das Eigengewicht eines gleichmässigen Balkens greift in seiner Mitte an. Die nähere Stütze trägt mehr; zusammen tragen beide immer die ganze Last. Eine Stütze kann nur drücken: Ergibt die Rechnung eine negative Auflagerkraft, müsste die Stütze ziehen — ohne Befestigung kippt der Balken.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Stützen vertauscht: Steht die Last nahe bei A, trägt A den grösseren Teil. Ohne Eigengewicht trägt A alles, wenn die Last genau über A steht.</p>
          <p>Nur eine Bedingung geprüft: \(\sum \vec{F} = \vec{0}\) allein reicht nicht. Zwei gleich grosse, entgegengesetzte Kräfte an verschiedenen Stellen eines Lenkrads drehen es, obwohl ihre Summe null ist.</p>
        </div>
      </div>'''
auf6 = test('t6', 'Aufgaben · Kapitel 6', 12, [
    ('6a', 3, r'Eine \(6\;\text{m}\) lange Holzbrücke (Eigengewicht \(3\;\text{kN}\), in der Mitte) liegt an den Ufern auf den Stützen A und B. Eine Kuh (\(6\;\text{kN}\)) steht \(2\;\text{m}\) von A entfernt. Wie gross sind \(F_A\) und \(F_B\)? Kontrolliere mit \(\sum F_y = 0\).',
     r'<p>\(\sum M_A = 0\): \(F_B \cdot 6\;\text{m} = 6\;\text{kN} \cdot 2\;\text{m} + 3\;\text{kN} \cdot 3\;\text{m}\), also \(F_B = \dfrac{21\;\text{kNm}}{6\;\text{m}}\) \(= 3.5\;\text{kN}\).</p><p>\(F_A = 6\;\text{kN} + 3\;\text{kN} - 3.5\;\text{kN}\) \(= 5.5\;\text{kN}\). Kontrolle: \(5.5\;\text{kN} + 3.5\;\text{kN} = 9\;\text{kN}\), die ganze Last.</p>', ''),
    ('6b', 3, r'Ein Wagen fährt über eine \(8\;\text{m}\) lange Brücke. Das Diagramm zeigt die Auflagerkraft \(F_B\) über seiner Stelle \(x\). Wie schwer ist der Wagen? Wie gross ist \(F_A\), wenn er bei \(2\;\text{m}\) steht? Hat die Brücke ein Eigengewicht? Begründe.',
     r'<p>Bei \(x = 8\;\text{m}\) steht der Wagen über B, B trägt alles: \(F_L = 40\;\text{kN}\). Bei \(x = 2\;\text{m}\) ist \(F_B = 10\;\text{kN}\), also \(F_A = 40\;\text{kN} - 10\;\text{kN} = 30\;\text{kN}\).</p><p>Kein Eigengewicht: Bei \(x = 0\) steht der Wagen über A, und \(F_B\) ist null. Mit Eigengewicht trüge B auch dann schon die Hälfte davon.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 0), (8, 40)], 0, 8, 0, 50, 1, 10, 'Auflagerkraft F B über x: Gerade von 0 kN bei 0 m auf 40 kN bei 8 m', 'x [m]', 'F_B [kN]', 'kurve-fb') + '</div>'),
    ('6c', 3, r'Ein Regalbrett liegt auf zwei Konsolen. Wohin stellst du die schweren Bücher, damit die linke Konsole möglichst wenig trägt? Ändert sich dabei die Summe der beiden Konsolenkräfte? Begründe mit den beiden Gleichgewichtsbedingungen.',
     r'<p>Möglichst nahe an die rechte Konsole: Momente um die rechte Konsole zeigen, dass die linke nur den Anteil \(F \cdot \dfrac{\text{Abstand zur rechten}}{L}\) trägt.</p><p>Die Summe bleibt gleich: \(\sum F_y = 0\) verlangt, dass beide zusammen immer die ganze Last tragen. Verteilt wird sie nach den Momenten.</p>', ''),
    ('6d', 3, r'Ein \(4\;\text{m}\) langes Brett (Eigengewicht \(300\;\text{N}\) in der Mitte) liegt auf Stützen bei \(0\;\text{m}\) (A) und \(3\;\text{m}\) (B). Ein Maler (\(750\;\text{N}\)) stellt sich ans überstehende Ende bei \(4\;\text{m}\). Berechne \(F_A\) und \(F_B\); was bedeutet das Vorzeichen von \(F_A\)? Bis wohin darf er gehen, ohne dass das Brett kippt?',
     r'<p>\(\sum M_A = 0\): \(F_B \cdot 3\;\text{m} = 300\;\text{N} \cdot 2\;\text{m} + 750\;\text{N} \cdot 4\;\text{m}\), \(F_B = \dfrac{3600\;\text{Nm}}{3\;\text{m}} = 1200\;\text{N}\). \(\sum F_y = 0\): \(F_A = 300\;\text{N} + 750\;\text{N} - 1200\;\text{N}\) \(= -150\;\text{N}\). Negativ heisst: A müsste nach <em>unten</em> ziehen. Eine Stütze kann nur drücken — ohne Befestigung kippt das Brett um B.</p><p>An der Kippgrenze ist \(F_A = 0\). Momente um B: Das Brett (\(1\;\text{m}\) links von B) hält gegen den Maler: \(300\;\text{N} \cdot 1\;\text{m} = 750\;\text{N} \cdot (x - 3\;\text{m})\), also \(x = 3.4\;\text{m}\). Weiter als \(0.4\;\text{m}\) über B hinaus darf er nicht.</p>', ''),
])
k6 = kapitel(6, 'auflagerkraefte', 'Statisches Gleichgewicht: Auflagerkräfte', 'K5', 50,
    r'Du definierst das statische Gleichgewicht mit \(\sum \vec{F} = \vec{0}\) und \(\sum M = 0\) und bestimmst damit die Auflagerkräfte eines Balkens auf zwei Stützen, auch mit Eigengewicht.',
    ('p4-4-lp-auflager', 'Statik sehen: zwei Stützen teilen sich die Last'),
    sim6, ('p4-4-lp-kontrolle-auflager', 'Kontrollfragen zum statischen Gleichgewicht'),
    fest6, [uebung('auflager', 'Auflagerkräfte'), uebung('auflager-e', 'Mit Eigengewicht'), uebung('zwei-lasten', 'Zwei Lasten auf einem Brett')],
    auf6, f'<a href="{TS}#auflager">Themenseite 4.4, Auflagerkräfte</a> · <a href="{TS}#definition">Statisches Gleichgewicht</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/statik/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">4.4 · K1 bis K5</span><span class="zeit">≈ 40 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg und Skizzen. Erlaubt sind Taschenrechner und Formelsammlung.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten lassen</b> — Lösung scannen oder fotografieren (ohne Namen und Standort) und mit dem Bewertungspaket einer KI geben, oder selbst nach dem Raster bewerten. Ob du eine KI nutzt und welche, entscheidest du selbst und in eigener Verantwortung (mehr dazu im Paket). Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>22 – 25 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals: Simulation und Übungen des Kapitels, in dem du die meisten Punkte verloren hast.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu Kapitel 1 und von dort der Reihe nach weiter.</td></tr>
          </table>
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a> → K1 · G2 → <a href="#k2">2</a>, <a href="#k3">3</a> → K4, K3 · G3 → <a href="#k4">4</a> → K2 · G4 → <a href="#k3">3</a> → K3, K5 · G5 → <a href="#k6">6</a> → K5 · G6 → <a href="#k6">6</a>, <a href="#k5">5</a> → K5, K2</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Die allgemeinen Formeln für die Seilkräfte bei ungleichen Winkeln, \(S_1 = F_G \cdot \dfrac{{\cos\beta}}{{\sin(\alpha + \beta)}}\) → <a href="{TS}#punkt">Themenseite 4.4, Last an zwei Seilen</a></li>
        <li>Gleitreibung und die Bewegung nach dem Rutschen → <a href="../themen/p4-2-dynamik.html#reibung">Themenseite 4.2, Reibung</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Statik, Version 1.1 (06.10.2026). Version 1.0 vom 05.10.2026, nach /lp-pruefung am
     06.10.2026 freigeschaltet; 1.1 setzt die Befunde der zweiten Prüfung um (README, «Fassung 1.1»).
     Fünftes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip → ② laufende Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF (downloads/leitprogramme/statik/*.tex). Quelle: scripts/lp/statik/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 4.4 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 den Begriff «Kraft» definieren und als Vektor darstellen
       K2 das Drehmoment einer Kraft definieren und Anwendungsgebiete nennen
       K3 die wesentlichen Kräfte, die auf einen Festkörper im Gleichgewicht wirken, aufzählen und
          charakterisieren (Schwerkraft, Auflagerkraft, Reibung)
       K4 die Gesamtheit der auf einen Körper wirkenden Kräfte darstellen und daraus die
          resultierende Kraft bestimmen
       K5 das statische Gleichgewicht eines Körpers definieren (Gleichgewicht der Momente und der
          Kräfte) und anhand verschiedener Beispiele auf der horizontalen und schiefen Ebene aufzeigen

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1 · Aufg. 1a–1d · G1     K2 → Kap. 4, 5 · Aufg. 4a–4d, 5a–5d · G3 G6
       K3 → Kap. 3 · Aufg. 3a–3d · G2 G4  K4 → Kap. 2 · Aufg. 2a–2d · G2
       K5 → Kap. 2 (Punkt), 3 (schiefe Ebene), 5, 6 · Aufg. 2c, 3b, 5a–6d · G4 G5 G6
     Winkelfunktionen stehen in keiner Vorwissensseite; Kapitel 0 bringt sie in einem Kasten.
     Resultierende heisst hier F_res (Themenseite auch F_R), weil F_R die Reibung ist.
     Zeiten: K0 15 · K1–K6 je 50 · Gesamttest 40 = 355 min ≈ 7.9 Lektionen (über der Zielgrösse von
     HOWTO \3; Begründung im README, «Umfang nach RLP»). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Statik</h1>
      <p class="unter">Kräfte als Pfeile, die resultierende Kraft, Gewicht, Normalkraft und Haftreibung, Drehmoment, Hebelgesetz und Auflagerkräfte — mit laufenden Simulationen. Sechs Kapitel zu je gut einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 4 · Teilgebiet 4.4</span>
    </div>
  </div>
</header>

<div class="huelle">
<div class="raster">

  <nav class="schiene" aria-label="Kapitelnavigation">
    <h2 id="ablauf">Ablauf</h2>
    <p class="lekt">Vorbereitung</p>
    <ol><li><a href="#k0"><span class="nr">0</span><span>Vorwissen</span></a></li></ol>
    <p class="lekt">Lektion 1</p>
    <ol><li><a href="#k1"><span class="nr">1</span><span>Kraft als Vektor</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Die resultierende Kraft</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Kräfte am ruhenden Körper</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Das Drehmoment</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Das Hebelgesetz</span></a></li></ol>
    <p class="lekt">Lektion 6</p>
    <ol><li><a href="#k6"><span class="nr">6</span><span>Auflagerkräfte</span></a></li></ol>
    <p class="lekt">Abschluss</p>
    <ol><li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li></ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 7 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen.</li>
          <li><b>② Tüfteln:</b> Die Simulationen laufen auf Knopfdruck. Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma; Brüche wie <code>1/2</code> und Zehnerpotenzen wie <code>2.4e-3</code> gehen auch. Richtig ist, was auf drei signifikante Stellen stimmt, Winkel auf ein halbes Grad.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 4, Teilgebiet 4.4 Statik von Festkörpern</p>
        <ul>
          <li><b>K1</b> den Begriff «Kraft» definieren und als Vektor darstellen</li>
          <li><b>K2</b> das Drehmoment einer Kraft definieren und Anwendungsgebiete nennen</li>
          <li><b>K3</b> die wesentlichen Kräfte, die auf einen Festkörper im Gleichgewicht wirken, aufzählen und charakterisieren (Schwerkraft, Auflagerkraft, Reibung)</li>
          <li><b>K4</b> die Gesamtheit der auf einen Körper wirkenden Kräfte darstellen und daraus die resultierende Kraft bestimmen</li>
          <li><b>K5</b> das statische Gleichgewicht eines Körpers definieren (Gleichgewicht der Momente und der Kräfte) und anhand verschiedener Beispiele auf der horizontalen und schiefen Ebene aufzeigen</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">4.4 Statik von Festkörpern</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Statik · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Kraft') + k1 + band(2, 'Resultierende') + k2 + band(3, 'Ruhender Körper') + k3
        + band(4, 'Drehmoment') + k4 + band(5, 'Hebel') + k5 + band(6, 'Auflager') + k6 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
