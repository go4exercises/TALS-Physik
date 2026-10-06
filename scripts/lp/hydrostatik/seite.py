"""Baut leitprogramme/leitprogramm-hydrostatik.html aus einer Kapitelbeschreibung (seit 05.10.2026).

  python3 scripts/lp/hydrostatik/seite.py

Sechstes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4), als Kopie von
scripts/lp/statik/ entstanden: Kopf, CSS, Grundskript und Bausteine von dort, neu sind
Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Siehe README.md.
"""
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-hydrostatik.html'
TS = '../themen/p4-5-hydrostatik.html'

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
<title>Leitprogramm Hydrostatik</title>
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
/* Diagramme und Szenen: Gewichtskraft Bernstein (wie Statik und Dynamik), Auftrieb Grün, Kräfte
   an Kolben Blau, Luftdruck Grau, Tiefe und Höhe Violett, Wasser Hellblau; voriger Lauf grau gestrichelt */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.sim .skala.klein{font-size:8px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.vorher{fill:none;stroke:var(--tinte-2);stroke-width:1.8;stroke-dasharray:5 4;opacity:.6}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.rad{fill:var(--tinte-2)}
.pf-linie{stroke-width:2.6;fill:none}
.pf-linie.pf-f{stroke:var(--blau)} .pf-kopf.pf-f{fill:var(--blau)}
.pf-linie.pf-g{stroke:var(--bernstein)} .pf-kopf.pf-g{fill:var(--bernstein)}
.pf-linie.pf-n{stroke:var(--gruen)} .pf-kopf.pf-n{fill:var(--gruen)}
.pf-linie.pf-luft{stroke:var(--tinte-2);stroke-width:1.6} .pf-kopf.pf-luft{fill:var(--tinte-2)}
.pf-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:3.5px;paint-order:stroke}
text.pf-a{fill:var(--lila)} text.pf-f{fill:var(--blau)} text.pf-g{fill:var(--bernstein)} text.pf-n{fill:var(--gruen)}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bt-meldung{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:10.5px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.kurve-p{stroke:var(--blau)} .kurve-mini.kurve-fa{stroke:var(--gruen)} .kurve-mini.kurve-waage{stroke:var(--blau)}
.kurve-mini.kurve-fg{stroke:var(--bernstein);stroke-dasharray:6 4}
svg.mini.breit{width:260px}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.p-mini{fill:var(--tinte)}
.hebelarm{stroke:var(--lila);stroke-width:2;stroke-dasharray:5 3}
.tick{stroke:var(--tinte-2);stroke-width:1.2}
.saeule-text{fill:var(--weiss);font-family:var(--sans);font-size:9px;font-weight:700}
.klotz-zahl{fill:var(--tinte);font-family:var(--sans);font-size:9px;font-weight:700}
.legende{fill:var(--tinte-2);font-family:var(--sans);font-size:10px;font-weight:700}
.legende.l-p,.legende.l-waage{fill:var(--blau)} .legende.l-ps{fill:var(--blau);opacity:.75} .legende.l-fa{fill:var(--gruen)}
.kurve-p{fill:none;stroke:var(--blau);stroke-width:2.4} .kurve-ps{fill:none;stroke:var(--blau);stroke-width:2;stroke-dasharray:6 4;opacity:.75}
.kurve-waage{fill:none;stroke:var(--blau);stroke-width:2.4} .kurve-fa{fill:none;stroke:var(--gruen);stroke-width:2.2;stroke-dasharray:6 4}
.kurve-tiefe{fill:none;stroke:var(--lila);stroke-width:2.4}
.p-p,.p-waage{fill:var(--blau)} .p-ps{fill:var(--blau);opacity:.6} .p-fa{fill:var(--gruen)}
.schnee{fill:#eef3f8;stroke:none} .schnee-rand{stroke:#9fb3c8;stroke-width:1.5} .mulde{fill:#d6e0ea}
.sohle{fill:var(--tinte-2)}
.mensch{fill:none;stroke:var(--tinte);stroke-width:2.2;stroke-linecap:round}
.kopf{fill:var(--karte);stroke:var(--tinte);stroke-width:2}
.wasser{fill:#5fa9c6;opacity:.35} .wasser.salzig{fill:#3a7a96;opacity:.4} .wasser.spiritus{fill:#b9d8e4;opacity:.55}
.wasserlinie{stroke:#3a7a96;stroke-width:1.6}
.quecksilber{fill:#9aa4ad;opacity:.85}
.oel{fill:#e3c75a;opacity:.55}
.gefaess{fill:none;stroke:var(--tinte-2);stroke-width:2;stroke-linejoin:round}
.rohr{fill:var(--karte);stroke:var(--tinte-2);stroke-width:1.6}
.pumpe{fill:var(--tinte-2)}
.taucher{fill:var(--tinte-2)} .flasche{fill:var(--bernstein)}
.manometer{fill:var(--karte);stroke:var(--tinte);stroke-width:2}
.zeiger{stroke:var(--rot);stroke-width:2.2;stroke-linecap:round}
.kolben{fill:var(--tinte-2)} .stange{stroke:var(--tinte-2);stroke-width:3}
.auto{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.6;stroke-linejoin:round}
.waage-gehaeuse{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.4}
.feder{fill:none;stroke:var(--tinte);stroke-width:1.4}
.faden{stroke:var(--tinte);stroke-width:1.2}
.koerper{fill:#c9cdd2;stroke:var(--tinte-2);stroke-width:1.4} .koerper.holz{fill:var(--bernstein-hell);stroke:var(--bernstein)}
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
  var KEY = 'leitprogramm-hydrostatik-v1';

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
  <p>Leitprogramm · Hydrostatik</p>
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.0 · Stand 5. Oktober 2026</p>
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">4.5 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


def linien_bild(punkte, x0, x1, y0, y1, xt, yt, label, xname, yname, cls='kurve-v', waagrecht=None, weitere=(), waagrecht_cls='vorher'):
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
        t.append(f'<line x1="{ox}" y1="{Y(waagrecht):.1f}" x2="{X(x1):.1f}" y2="{Y(waagrecht):.1f}" class="{waagrecht_cls}"/>')
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
LPV = 'leitprogramm-vorwissen.html'
P01 = '../themen/p0-1-vorwissen-mathematik.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 4.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Dichte, Gewichtskraft, Flächen und Volumen umrechnen, Gleichungen umstellen. Wenn das wackelt: <a href="''' + LPV + '''">Leitprogramm Grössen, Messen, Druck</a> — dort stehen Dichte und Druckeinheiten als Kurs.</p>
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Ein Stein hat die Masse \(2.6\;\text{kg}\) und das Volumen \(1.0\;\text{l}\). Wie gross ist seine Dichte in \(\text{kg/m}^3\)? Wie gross ist die Gewichtskraft auf eine Person mit \(80\;\text{kg}\)?',
     r'<p>\(\rho = \dfrac{m}{V}\) \(= \dfrac{2.6\;\text{kg}}{0.001\;\text{m}^3}\) \(= 2600\;\text{kg/m}^3\).</p><p>\(F_G = m \cdot g\) \(= 80\;\text{kg} \cdot 9.81\;\text{m/s}^2\) \(\approx 785\;\text{N}\).</p><p class="komm">Falsch? <a href="' + LPV + r'#ls6">Leitprogramm Grössen, Messen, Druck: Dichte</a> · <a href="' + LPV + r'#ls5">Masse und Gewichtskraft</a></p>', ''),
    ('0b', 3, r'Rechne um: \(250\;\text{cm}^2\) in \(\text{m}^2\), \(2.5\;\text{l}\) in \(\text{m}^3\) und \(400\;\text{cm}^3\) in \(\text{m}^3\).',
     r'<p>\(250\;\text{cm}^2 = 0.025\;\text{m}^2\) (\(1\;\text{cm}^2 = 10^{-4}\;\text{m}^2\)), \(2.5\;\text{l} = 0.0025\;\text{m}^3\) (\(1\;\text{l} = 10^{-3}\;\text{m}^3\)), \(400\;\text{cm}^3 = 4 \cdot 10^{-4}\;\text{m}^3\) (\(1\;\text{cm}^3 = 10^{-6}\;\text{m}^3\)).</p><p class="komm">Falsch? <a href="' + LPV + r'#ls3">Leitprogramm Grössen, Messen, Druck: Fläche und Volumen umrechnen</a></p>', ''),
    ('0c', 4, r'Stelle um: \(p = \dfrac{F}{A}\) nach \(A\), \(p = \rho \cdot g \cdot h\) nach \(h\), \(F = \rho \cdot V \cdot g\) nach \(V\) und \(\dfrac{F_1}{A_1} = \dfrac{F_2}{A_2}\) nach \(F_2\).',
     r'<p>\(A = \dfrac{F}{p}\), \(h = \dfrac{p}{\rho \cdot g}\), \(V = \dfrac{F}{\rho \cdot g}\), \(F_2 = F_1 \cdot \dfrac{A_2}{A_1}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umstellen</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Eine Person steht auf einer Auflagefläche im Schnee und sinkt je nach Druck ein; darunter der Druck über der Fläche', '-4 -4 308 334',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'm', '<i>m</i> Masse', 20, 120, 1, 50, 'kg', 0) + '\n          '
    + regler('s1', 'A', '<i>A</i> Fläche', 100, 4000, 50, 600, 'cm²', 0) + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Druck</div>
          <p>Der <b>Druck</b> ist die Kraft, die senkrecht auf eine Fläche wirkt, geteilt durch diese Fläche:</p>
          <p>\[ p = \frac{F}{A} \]</p>
          <p>Einheit: das <b>Pascal</b>, \(1\;\text{Pa} = 1\;\text{N/m}^2\). Weitere Einheiten: \(1\;\text{hPa} = 1\;\text{mbar} = 100\;\text{Pa}\), \(1\;\text{kPa} = 1000\;\text{Pa}\), \(1\;\text{bar} = 1000\;\text{hPa} = 100\,000\;\text{Pa}\). Der Luftdruck auf Meereshöhe ist rund \(1013\;\text{hPa} \approx 1\;\text{bar}\).</p>
          <p><b>Zwischen zwei Festkörpern</b> (Schuh auf Schnee, Kiste auf Boden) ist \(F\) meist die Gewichtskraft und \(A\) die Auflagefläche. Dieselbe Kraft auf kleiner Fläche gibt grossen Druck (Messerschneide, Nadel), auf grosser Fläche kleinen Druck (Schneeschuh, Raupe).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Fläche in cm² eingesetzt: \(450\;\text{N}\) auf \(150\;\text{cm}^2\) sind \(\dfrac{450\;\text{N}}{0.015\;\text{m}^2} = 30\,000\;\text{Pa}\), nicht \(3\;\text{Pa}\). Erst in m² umrechnen: \(1\;\text{cm}^2 = 10^{-4}\;\text{m}^2\).</p>
          <p>Die Masse statt der Kraft eingesetzt: Druck braucht Newton, also \(F = m \cdot g\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Ein Messer hat eine scharfe Schneide, ein Traktor breite Reifen. Erkläre beides mit dem Druck und begründe, warum sich ein stumpfes Messer schlecht zum Schneiden eignet.',
     r'<p>\(p = \dfrac{F}{A}\): Die scharfe Schneide hat eine winzige Fläche, schon eine kleine Kraft gibt einen sehr grossen Druck, der das Material trennt. Die breiten Reifen verteilen die grosse Gewichtskraft des Traktors auf eine grosse Fläche: kleiner Druck, er sinkt im Feld nicht ein.</p><p>Beim stumpfen Messer ist die Fläche grösser — für denselben Druck braucht es viel mehr Kraft.</p>', ''),
    ('1b', 3, r'Ein Ziegelstein (\(2.4\;\text{kg}\), \(24\;\text{cm} \times 11.5\;\text{cm} \times 7.1\;\text{cm}\)) liegt einmal auf der grössten, einmal auf der kleinsten Seite. Wie gross ist der Druck auf die Unterlage in beiden Fällen?',
     r'<p>\(F = m \cdot g\) \(= 2.4\;\text{kg} \cdot 9.81\;\text{m/s}^2\) \(\approx 23.5\;\text{N}\).</p><p>Grösste Seite: \(A = 24\;\text{cm} \cdot 11.5\;\text{cm}\) \(= 276\;\text{cm}^2\) \(= 0.0276\;\text{m}^2\), \(p = \dfrac{23.5\;\text{N}}{0.0276\;\text{m}^2}\) \(\approx 853\;\text{Pa}\). Kleinste Seite: \(A = 11.5\;\text{cm} \cdot 7.1\;\text{cm} \approx 81.7\;\text{cm}^2\), \(p = \dfrac{23.5\;\text{N}}{0.00817\;\text{m}^2}\) \(\approx 2880\;\text{Pa}\) — rund 3.4-mal so viel bei gleicher Kraft.</p>', ''),
    ('1c', 3, r'Das Diagramm zeigt den Druck, den eine Person auf den Boden ausübt, über der Auflagefläche. Lies den Druck bei \(250\;\text{cm}^2\) ab und bestimme daraus die Gewichtskraft und die Masse der Person. Bei welcher Fläche ist der Druck \(5\;\text{kPa}\)?',
     r'<p>Bei \(250\;\text{cm}^2\) liest man \(20\;\text{kPa}\) ab. \(F = p \cdot A\) \(= 20\,000\;\text{Pa} \cdot 0.025\;\text{m}^2\) \(= 500\;\text{N}\), \(m = \dfrac{F}{g}\) \(\approx 51\;\text{kg}\).</p><p>\(5\;\text{kPa}\) bei \(A = \dfrac{500\;\text{N}}{5000\;\text{Pa}}\) \(= 0.1\;\text{m}^2 = 1000\;\text{cm}^2\) — auch im Diagramm ablesbar.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(a, 500 / (a / 1e4) / 1000) for a in range(200, 2001, 25)], 0, 2000, 0, 25, 250, 5, 'Druck über der Fläche: fallende Kurve, 20 kPa bei 250 cm², 10 kPa bei 500 cm², 5 kPa bei 1000 cm², 2.5 kPa bei 2000 cm²', 'A [cm²]', 'p [kPa]', 'kurve-p') + '</div>'),
    ('1d', 3, r'Der Wetterbericht meldet einen Luftdruck von \(985\;\text{hPa}\). Gib ihn in bar, kPa und Pa an. In einem Velopneu herrscht ein Druck von \(4.5\;\text{bar}\) — wie viele kPa sind das?',
     r'<p>\(985\;\text{hPa} = 0.985\;\text{bar}\) \(= 98.5\;\text{kPa}\) \(= 98\,500\;\text{Pa}\).</p><p>\(4.5\;\text{bar} = 450\,000\;\text{Pa} = 450\;\text{kPa}\).</p>', ''),
])
k1 = kapitel(1, 'druck', 'Druck', 'K1 · K2', 40,
    r'Du definierst den Druck \(p = \dfrac{F}{A}\), rechnest zwischen Pa, hPa, kPa und bar um und berechnest den Druck zwischen zwei Festkörpern.',
    ('p4-5-lp-druck', 'Hydrostatik sehen: Kraft auf Fläche'),
    sim1, ('p4-5-lp-kontrolle-druck', 'Kontrollfragen zum Druck'),
    fest1, [uebung('druck', 'Druck auf den Boden'), uebung('flaeche', 'Wie viel Fläche braucht es?'), uebung('einheiten', 'Druckeinheiten umrechnen')],
    auf1, f'<a href="{TS}#definition">Themenseite 4.5, Grundbegriffe</a> · <a href="{LPV}#ls7">Leitprogramm Grössen, Messen, Druck</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur_anim('sim2', 'Eine Taucherin taucht bis zur eingestellten Tiefe; ein Manometer zeigt den Druck; darunter der Druck über der Tiefe', '-4 -4 308 350',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'h', '<i>h</i> Tiefe', 0, 40, 0.5, 8, 'm', 1) + '\n        </div>',
    knoepfe('rho', 'Gewässer', [('1000', 'See (1000 kg/m³)'), ('1025', 'Meer (1025 kg/m³)'), ('1240', 'Totes Meer (1240 kg/m³)')], '1000'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Schweredruck</div>
          <p>In einer ruhenden Flüssigkeit drückt das Gewicht der Flüssigkeitssäule darüber. Dieser <b>Schweredruck</b> wächst linear mit der Tiefe (hydrostatische Grundgleichung):</p>
          <p>\[ p_S = \rho \cdot g \cdot h \qquad p = p_0 + p_S \]</p>
          <p>\(\rho\): Dichte der Flüssigkeit, \(h\): Tiefe unter der Oberfläche. Zum Schweredruck kommt der Luftdruck \(p_0\), der auf die Oberfläche drückt; zusammen ergibt das den Gesamtdruck \(p\). In Wasser kommt je \(10\;\text{m}\) Tiefe rund \(1\;\text{bar}\) dazu. Der Druck wirkt an jeder Stelle nach allen Seiten gleich stark.</p>
          <p><b>Hydrostatisches Paradoxon:</b> Der Bodendruck hängt nur von der Füllhöhe ab, nicht von der Form des Gefässes oder der Wassermenge.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Schweredruck und Gesamtdruck verwechselt: In \(7\;\text{m}\) Wassertiefe ist \(p_S \approx 0.69\;\text{bar}\), der Druck auf die Ohren aber \(p \approx 1.70\;\text{bar}\).</p>
          <p>Die Tiefe in cm eingesetzt: \(h\) in Meter, sonst wird der Druck hundertmal zu gross.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Hinter einer Staumauer ist das Wasser \(85\;\text{m}\) tief. Wie gross ist der Schweredruck am Grund, in bar? Begründe, warum Staumauern unten dicker gebaut werden als oben.',
     r'<p>\(p_S = \rho \cdot g \cdot h\) \(= 1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2 \cdot 85\;\text{m}\) \(\approx 834\,000\;\text{Pa} \approx 8.34\;\text{bar}\).</p><p>Der Druck wächst mit der Tiefe; unten drückt das Wasser am stärksten gegen die Mauer, oben fast gar nicht.</p>', ''),
    ('2b', 3, r'Ein schmaler Messzylinder, eine breite Schüssel und ein Trichter sind alle \(30\;\text{cm}\) hoch mit Wasser gefüllt. Wie gross ist der Schweredruck am Boden jedes Gefässes? Begründe, warum er gleich ist, obwohl die Wassermengen verschieden sind.',
     r'<p>Überall \(p_S = 1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2 \cdot 0.30\;\text{m}\) \(\approx 2940\;\text{Pa}\).</p><p>In \(p_S = \rho \cdot g \cdot h\) kommen weder Fläche noch Menge vor: Mehr Wasser verteilt sich auf mehr Bodenfläche, und bei schrägen Wänden tragen die Wände einen Teil (hydrostatisches Paradoxon).</p>', ''),
    ('2c', 3, r'Das Diagramm zeigt den Schweredruck in einer unbekannten Flüssigkeit über der Tiefe. Lies einen Punkt ab und bestimme die Dichte. Um welche Flüssigkeit könnte es sich handeln?',
     r'<p>Bei \(6\;\text{m}\) liest man \(50\;\text{kPa}\) ab. \(\rho = \dfrac{p_S}{g \cdot h}\) \(= \dfrac{50\,000\;\text{Pa}}{9.81\;\text{m/s}^2 \cdot 6\;\text{m}}\) \(\approx 850\;\text{kg/m}^3\) — zum Beispiel Heizöl.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 0), (8, 400 / 6)], 0, 8, 0, 70, 1, 10, 'Schweredruck über der Tiefe: Gerade durch den Ursprung und den Punkt 6 m, 50 kPa', 'h [m]', 'p_S [kPa]', 'kurve-p') + '</div>'),
    ('2d', 3, r'Ein Taucher ist im Meer (\(1025\;\text{kg/m}^3\)) in \(20\;\text{m}\) Tiefe. Wie gross ist der Gesamtdruck in bar? Seine Kamera steckt in einem dichten Gehäuse, in dem die Luft den Druck \(p_0\) von der Oberfläche behält. Mit welcher Kraft drückt das Wasser zusätzlich auf das Frontglas (\(120\;\text{cm}^2\))?',
     r'<p>\(p_S = 1025\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2 \cdot 20\;\text{m}\) \(\approx 201\,000\;\text{Pa}\); \(p = p_0 + p_S\) \(\approx 1.013\;\text{bar} + 2.01\;\text{bar} \approx 3.02\;\text{bar}\).</p><p>Innen drückt \(p_0\), aussen \(p_0 + p_S\): Es bleibt der Schweredruck. \(F = p_S \cdot A\) \(\approx 201\,000\;\text{Pa} \cdot 0.012\;\text{m}^2\) \(\approx 2410\;\text{N}\) — so viel wie die Gewichtskraft von rund \(250\;\text{kg}\). Darum braucht das Gehäuse dickes Glas.</p>', ''),
])
k2 = kapitel(2, 'schweredruck', 'Schweredruck', 'K3', 40,
    r'Du berechnest den Druck in einer Flüssigkeit mit der hydrostatischen Grundgleichung \(p_S = \rho \cdot g \cdot h\), setzt ihn mit dem Luftdruck zum Gesamtdruck zusammen und erklärst das hydrostatische Paradoxon.',
    ('p4-5-lp-schweredruck', 'Hydrostatik sehen: Druck in der Tiefe'),
    sim2, ('p4-5-lp-kontrolle-schweredruck', 'Kontrollfragen zum Schweredruck'),
    fest2, [uebung('schweredruck', 'Schweredruck'), uebung('tiefe', 'Tiefe aus dem Druck'), uebung('gesamtdruck', 'Gesamtdruck beim Tauchen')],
    auf2, f'<a href="{TS}#schweredruck">Themenseite 4.5, Schweredruck</a> · <a href="{TS}#paradoxon">Hydrostatisches Paradoxon</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Ein oben geschlossenes Rohr steht in einem Becken; eine Pumpe saugt die Luft ab, und der Luftdruck drückt die Flüssigkeit hoch', '-4 -4 308 312',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'pi', '<i>p</i><sub>i</sub> Innendruck', 0, 1013, 0.5, 800, 'hPa', 1) + '\n        </div>',
    knoepfe('ort', 'Ort', [('1013', 'Meereshöhe'), ('965', 'Zürich'), ('841', 'Davos'), ('671', 'Jungfraujoch')], '1013')
    + '\n        ' + knoepfe('fl', 'Flüssigkeit', [('1000', 'Wasser'), ('13600', 'Quecksilber')], '1000'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Luftdruck</div>
          <p>Auch die Luft hat ein Gewicht: Der <b>Luftdruck</b> ist der Schweredruck der Luftsäule über uns, auf Meereshöhe im Mittel \(p_0 \approx 1013\;\text{hPa}\). Je höher man steigt, desto weniger Luft liegt darüber — auf \(3500\;\text{m}\) sind es nur noch rund zwei Drittel.</p>
          <p>Senkt man in einem Rohr den Druck auf \(p_i\), drückt der Luftdruck draussen die Flüssigkeit hoch, bis ihr Schweredruck den Unterschied ausgleicht:</p>
          <p>\[ \rho \cdot g \cdot h = p_0 - p_i \]</p>
          <p>Mehr als den ganzen Luftdruck (\(p_i = 0\), Vakuum) gibt es nicht: Eine Saugpumpe hebt Wasser höchstens rund \(10\;\text{m}\). Im <b>Quecksilberbarometer</b> hält eine Quecksilbersäule dem Luftdruck das Gleichgewicht; ihre Höhe zeigt den Luftdruck an.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Pumpe zieht das Wasser hoch.» Sie senkt nur den Druck im Rohr; hochgedrückt wird das Wasser vom Luftdruck draussen.</p>
          <p>hPa nicht umgerechnet: In \(\rho \cdot g \cdot h\) steht der Druck in Pascal, \(1\;\text{hPa} = 100\;\text{Pa}\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Magdeburger Halbkugeln: Zwei Halbkugeln mit \(50\;\text{cm}\) Durchmesser werden zusammengesetzt und innen fast luftleer gepumpt. Mit welcher Kraft drückt der Luftdruck (\(1013\;\text{hPa}\)) sie zusammen (wirksame Fläche: Kreis mit \(50\;\text{cm}\) Durchmesser)? Wie viele Pferde, die je mit \(1000\;\text{N}\) ziehen, braucht es auf jeder Seite?',
     r'<p>\(A = \pi \cdot r^2 = \pi \cdot (0.25\;\text{m})^2\) \(\approx 0.196\;\text{m}^2\), \(F = p_0 \cdot A\) \(= 101\,300\;\text{Pa} \cdot 0.196\;\text{m}^2\) \(\approx 19\,900\;\text{N}\).</p><p>Rund \(20\) Pferde auf jeder Seite (auf der anderen Seite könnte auch eine Wand halten).</p>', ''),
    ('3b', 3, r'Das Diagramm zeigt den mittleren Luftdruck über der Höhe über Meer. Lies den Luftdruck in \(3000\;\text{m}\) Höhe ab. Wie hoch kann eine Saugpumpe dort Wasser höchstens heben?',
     r'<p>Abgelesen: rund \(710\;\text{hPa}\).</p><p>\(h = \dfrac{p_0}{\rho \cdot g}\) \(= \dfrac{71\,000\;\text{Pa}}{1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2}\) \(\approx 7.2\;\text{m}\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 1013), (1000, 899), (2000, 798), (3000, 709), (4000, 629)], 0, 4000, 500, 1100, 1000, 100, 'Luftdruck über der Höhe: fallende Kurve von 1013 hPa auf Meereshöhe über rund 800 hPa in 2000 m bis rund 630 hPa in 4000 m', 'Höhe [m]', 'p_0 [hPa]', 'kurve-p') + '</div>'),
    ('3c', 3, r'Du tauchst einen Trinkhalm ins Glas, hältst ihn oben mit dem Finger zu und hebst ihn heraus. Das Getränk bleibt im Halm. Begründe mit dem Druck.',
     r'<p>Von unten drückt die Luft mit \(p_0\) auf das Getränk im Halm. Oben ist der Halm zu; die eingeschlossene Luft dehnt sich ein wenig aus, ihr Druck sinkt etwas unter \(p_0\). Der Unterschied trägt die kurze Flüssigkeitssäule — erst wenn man den Finger wegnimmt, drückt oben wieder der volle Luftdruck, und das Getränk läuft aus.</p>', ''),
    ('3d', 3, r'Blaise Pascal baute ein Barometer mit Wasser statt Quecksilber. Wie hoch stünde die Wassersäule bei einem Luftdruck von \(990\;\text{hPa}\)? Begründe, warum man Barometer mit Quecksilber baut.',
     r'<p>\(h = \dfrac{p_0}{\rho \cdot g}\) \(= \dfrac{99\,000\;\text{Pa}}{1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2}\) \(\approx 10.1\;\text{m}\).</p><p>Quecksilber ist \(13.6\)-mal dichter: Die Säule ist nur rund \(74\;\text{cm}\) hoch, handlich statt zehn Meter.</p>', ''),
])
k3 = kapitel(3, 'luftdruck', 'Luftdruck', 'K3', 40,
    r'Du verbindest den Druck in Flüssigkeiten mit dem Luftdruck: Du erklärst, warum der Luftdruck eine Flüssigkeit in einem Rohr hochdrückt, berechnest \(\rho \cdot g \cdot h = p_0 - p_i\) und verstehst das Barometer.',
    ('p4-5-lp-luftdruck', 'Hydrostatik sehen: die Luft drückt mit'),
    sim3, ('p4-5-lp-kontrolle-luftdruck', 'Kontrollfragen zum Luftdruck'),
    fest3, [uebung('saughoehe', 'Wie hoch saugt eine Pumpe?'), uebung('unterdruck', 'Trinken mit dem Strohhalm'), uebung('barometer', 'Quecksilberbarometer')],
    auf3, f'<a href="{TS}#definition">Themenseite 4.5, Schweredruck und Luftdruck \\(p = p_0 + p_S\\)</a> · <a href="{LPV}#ls8">Überdruck und absoluter Druck</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Hydraulische Hebebühne: Auf Knopfdruck pumpt der kleine Kolben fünfmal; reicht die Kraft am grossen Kolben, hebt sich das Auto', '-4 -4 308 290',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 'F1', '<i>F</i><sub>1</sub> Kraft', 50, 500, 10, 150, 'N', 0) + '\n          '
    + regler('s4', 'A1', '<i>A</i><sub>1</sub> klein', 2, 20, 1, 10, 'cm²', 0) + '\n          '
    + regler('s4', 'A2', '<i>A</i><sub>2</sub> gross', 50, 1000, 10, 300, 'cm²', 0) + '\n          '
    + regler('s4', 'm', '<i>m</i> Auto', 500, 2000, 50, 1000, 'kg', 0) + '\n        </div>')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Pascal'sches Gesetz</div>
          <p>Ein Druck, den man von aussen auf eine eingeschlossene Flüssigkeit ausübt, breitet sich unverändert in der ganzen Flüssigkeit aus (<b>Pascal'sches Gesetz</b>). In der hydraulischen Presse wirkt darum auf beide Kolben derselbe Druck:</p>
          <p>\[ p = \frac{F_1}{A_1} = \frac{F_2}{A_2} \qquad A_1 \cdot s_1 = A_2 \cdot s_2 \]</p>
          <p>Der grosse Kolben bekommt die grosse Kraft, \(F_2 = F_1 \cdot \dfrac{A_2}{A_1}\). Bezahlt wird mit dem Weg: Das verdrängte Volumen ist gleich, der kleine Kolben bewegt sich viel weiter. Die Arbeit \(F_1 \cdot s_1 = F_2 \cdot s_2\) bleibt gleich (ohne Reibung). Anwendungen: Hebebühne, Wagenheber, Bremse, Bagger.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Kraft ist überall gleich.» Gleich ist der Druck. Die Kraft wächst mit der Fläche.</p>
          <p>Den Weg falsch herum gerechnet: Der grosse Kolben bewegt sich <em>weniger</em> weit als der kleine, \(s_2 = s_1 \cdot \dfrac{A_1}{A_2}\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'In einer Autobremse drückt der Fuss mit \(150\;\text{N}\) auf den Kolben des Hauptzylinders (\(3\;\text{cm}^2\)); der Kolben am Rad hat \(12\;\text{cm}^2\). Wie gross ist der Druck in der Bremsflüssigkeit? Mit welcher Kraft drückt der Radkolben auf den Bremsbelag?',
     r'<p>\(p = \dfrac{F_1}{A_1}\) \(= \dfrac{150\;\text{N}}{0.0003\;\text{m}^2}\) \(= 500\,000\;\text{Pa} = 5\;\text{bar}\).</p><p>\(F_2 = p \cdot A_2\) \(= 500\,000\;\text{Pa} \cdot 0.0012\;\text{m}^2\) \(= 600\;\text{N}\) — viermal die Fusskraft.</p>', ''),
    ('4b', 3, r'Die Bremsflüssigkeit muss frei von Luftblasen sein. Begründe, warum Luft in der Leitung die Bremse unwirksam macht.',
     r'<p>Flüssigkeiten lassen sich kaum zusammendrücken: Der Druck wird sofort und ganz an den Radkolben weitergegeben. Luft lässt sich zusammendrücken — der Pedalweg geht dafür drauf, den Luftblasen das Volumen zu nehmen, statt den Radkolben zu bewegen. Das Pedal wird «weich», die Bremskraft bleibt aus.</p>', ''),
    ('4c', 3, r'Das Diagramm zeigt für eine Presse die Kraft \(F_2\) am grossen Kolben über dessen Fläche \(A_2\), bei immer gleichem Druck. Wie gross ist der Druck? Welche Kraft \(F_1\) drückt auf den kleinen Kolben, wenn \(A_1 = 4\;\text{cm}^2\) ist?',
     r'<p>Die Steigung ist der Druck: \(p = \dfrac{F_2}{A_2}\) \(= \dfrac{6000\;\text{N}}{300\;\text{cm}^2}\) \(= 20\;\text{N/cm}^2 = 200\,000\;\text{Pa} = 2\;\text{bar}\).</p><p>\(F_1 = p \cdot A_1\) \(= 20\;\text{N/cm}^2 \cdot 4\;\text{cm}^2\) \(= 80\;\text{N}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="20" data-namen="" data-farbe="kurve-p" data-fenster="400,8000" data-teilung="50,1000" data-punkte="100,2000;300,6000" data-xname="A₂ [cm²]" data-yname="F₂ [N]" aria-label="Kraft am grossen Kolben über dessen Fläche: Ursprungsgerade durch 100 cm², 2000 N und 300 cm², 6000 N"></svg></div>'),
    ('4d', 3, r'Eine Hebebühne hebt ein Auto (\(1400\;\text{kg}\)); \(A_2 = 600\;\text{cm}^2\), die Handpumpe hat \(A_1 = 3\;\text{cm}^2\) und einen Hub von \(15\;\text{cm}\). Welche Kraft braucht es an der Pumpe? Wie viele Pumpstösse braucht es, um das Auto \(30\;\text{cm}\) zu heben?',
     r'<p>\(F_1 = m \cdot g \cdot \dfrac{A_1}{A_2}\) \(= 1400\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot \dfrac{3\;\text{cm}^2}{600\;\text{cm}^2}\) \(\approx 68.7\;\text{N}\).</p><p>Je Pumpstoss \(s_2 = 15\;\text{cm} \cdot \dfrac{3\;\text{cm}^2}{600\;\text{cm}^2}\) \(= 0.075\;\text{cm}\); für \(30\;\text{cm}\) braucht es \(\dfrac{30\;\text{cm}}{0.075\;\text{cm}} = 400\) Pumpstösse.</p>', ''),
])
k4 = kapitel(4, 'pascal', "Das Pascal'sche Gesetz", 'K4', 40,
    r"Du wendest das Pascal'sche Gesetz an hydraulischen Anlagen an: gleicher Druck auf beide Kolben, \(F_2 = F_1 \cdot \dfrac{A_2}{A_1}\), und den Tausch von Kraft gegen Weg.",
    ('p4-5-lp-pascal', 'Hydrostatik sehen: Druck pflanzt sich fort'),
    sim4, ('p4-5-lp-kontrolle-pascal', "Kontrollfragen zum Pascal'schen Gesetz"),
    fest4, [uebung('presse', 'Kraft am grossen Kolben'), uebung('kolbenweg', 'Kolbenwege'), uebung('druck-presse', 'Druck in der Hydraulik')],
    auf4, f'<a href="{TS}#pascal">Themenseite 4.5, Prinzip von Pascal</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur_anim('sim5', 'Ein Zylinder hängt an einer Federwaage und wird auf Knopfdruck eingetaucht; die Anzeige sinkt um den Auftrieb; darunter Anzeige und Auftrieb über der Eintauchtiefe', '-4 -4 308 380',
    '        <div class="reglerfeld">\n          '
    + regler('s5', 'he', '<i>h</i><sub>e</sub> eintauchen bis', 0, 14, 0.5, 4, 'cm', 1) + '\n        </div>',
    knoepfe('stoff', 'Körper', [('2700', 'Aluminium'), ('8500', 'Messing'), ('7870', 'Eisen'), ('7290', 'Stoff X')], '2700')
    + '\n        ' + knoepfe('fl', 'Flüssigkeit', [('1000', 'Wasser'), ('790', 'Spiritus')], '1000'))
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Archimedisches Prinzip</div>
          <p>Ein Körper in einer Flüssigkeit erfährt eine <b>Auftriebskraft</b> nach oben. Sie ist so gross wie die Gewichtskraft der Flüssigkeit, die er verdrängt (<b>archimedisches Prinzip</b>):</p>
          <p>\[ F_A = \rho_{Fl} \cdot V_e \cdot g \]</p>
          <p>\(\rho_{Fl}\): Dichte der Flüssigkeit, \(V_e\): eingetauchtes Volumen. Der Auftrieb entsteht, weil der Druck unten am Körper grösser ist als oben. Ganz eingetaucht hängt er nicht mehr von der Tiefe ab. An einer Federwaage zeigt sich der Körper um \(F_A\) leichter: Anzeige \(= F_G - F_A\). Das Prinzip gilt auch in Gasen: Ein Ballon erfährt Auftrieb, weil er Luft verdrängt (\(\rho_\text{Luft} \approx 1.2\;\text{kg/m}^3\)).</p>
          <p><b>Dichte mit der Federwaage:</b> Ganz eingetaucht verdrängt ein Körper sein eigenes Volumen, \(V = \dfrac{F_A}{\rho_{Fl} \cdot g}\). Mit \(F_G = \rho_K \cdot V \cdot g\) folgt \(\rho_K = \dfrac{F_G}{F_A} \cdot \rho_{Fl}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Dichte des Körpers eingesetzt: Für den Auftrieb zählt die Dichte der <em>Flüssigkeit</em>. Ein Eisen- und ein Aluminiumkörper mit gleichem Volumen erfahren denselben Auftrieb.</p>
          <p>Das Volumen nicht in m³: \(1\;\text{l} = 10^{-3}\;\text{m}^3\), \(1\;\text{cm}^3 = 10^{-6}\;\text{m}^3\).</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Ein Stein (\(2.8\;\text{kg}\), \(1.1\;\text{l}\)) liegt im See. Wie gross ist der Auftrieb? Mit welcher Kraft muss eine Taucherin ihn halten, um ihn zu heben?',
     r'<p>\(F_A = \rho_{Fl} \cdot V_e \cdot g\) \(= 1000\;\text{kg/m}^3 \cdot 0.0011\;\text{m}^3 \cdot 9.81\;\text{m/s}^2\) \(\approx 10.8\;\text{N}\).</p><p>\(F_G = 2.8\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 27.5\;\text{N}\); halten: \(27.5\;\text{N} - 10.8\;\text{N} \approx 16.7\;\text{N}\).</p>', ''),
    ('5b', 3, r'Erkläre mit dem Schweredruck, warum ein eingetauchter Würfel Auftrieb erfährt. Warum hängt der Auftrieb nicht davon ab, wie tief der Würfel ganz unter Wasser liegt? Begründe.',
     r'<p>Auf die Unterseite drückt das Wasser stärker nach oben als auf die Oberseite nach unten, denn unten ist es tiefer: \(p = \rho \cdot g \cdot h\). Der Unterschied der beiden Kräfte ist der Auftrieb; die Seitenkräfte heben sich auf.</p><p>Liegt der Würfel tiefer, wachsen beide Drücke um gleich viel — ihr Unterschied hängt nur von der Würfelhöhe ab, also vom Volumen.</p>', ''),
    ('5c', 3, r'Ein Körper an einer Federwaage wird langsam in Wasser getaucht. Das Diagramm zeigt die Anzeige über der Eintauchtiefe. Wie gross ist der Auftrieb, wenn er ganz eingetaucht ist? Welches Volumen hat er? Was würde die Waage zeigen, wenn er ganz in Spiritus (\(790\;\text{kg/m}^3\)) taucht?',
     r'<p>Anzeige an der Luft \(6\;\text{N}\), ganz eingetaucht \(4\;\text{N}\): \(F_A = 2\;\text{N}\).</p><p>\(V = \dfrac{F_A}{\rho_W \cdot g}\) \(= \dfrac{2\;\text{N}}{1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2}\) \(\approx 204\;\text{cm}^3\).</p><p>In Spiritus ist der Auftrieb im Verhältnis der Dichten kleiner: \(F_A = 2\;\text{N} \cdot \dfrac{790}{1000}\) \(= 1.58\;\text{N}\), die Waage zeigt \(6\;\text{N} - 1.58\;\text{N}\) \(= 4.42\;\text{N}\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 6), (8, 4), (12, 4)], 0, 12, 0, 7, 2, 1, 'Anzeige der Federwaage über der Eintauchtiefe: fällt von 6 N bei 0 cm geradlinig auf 4 N bei 8 cm und bleibt dann bei 4 N', 'h_e [cm]', 'F [N]', 'kurve-waage') + '</div>'),
    ('5d', 3, r'Archimedes sollte prüfen, ob eine Krone aus reinem Gold (\(19\,300\;\text{kg/m}^3\)) ist. An der Luft zeigt die Waage \(9.81\;\text{N}\), ganz in Wasser \(9.15\;\text{N}\). Ist die Krone aus reinem Gold? Begründe mit einer Rechnung.',
     r'<p>\(F_A = 9.81\;\text{N} - 9.15\;\text{N} = 0.66\;\text{N}\), \(V = \dfrac{F_A}{\rho_W \cdot g}\) \(\approx 67.3\;\text{cm}^3\).</p><p>\(\rho = \dfrac{F_G}{F_A} \cdot \rho_W\) \(\approx 14\,900\;\text{kg/m}^3\) — viel weniger als Gold. Die Krone ist mit einem leichteren Metall (zum Beispiel Silber) gestreckt.</p>', ''),
])
k5 = kapitel(5, 'auftrieb', 'Auftrieb', 'K5', 40,
    r'Du formulierst das archimedische Prinzip \(F_A = \rho_{Fl} \cdot V_e \cdot g\), erklärst den Auftrieb mit dem Druckunterschied und berechnest Auftrieb und Anzeige einer Federwaage.',
    ('p4-5-lp-auftrieb', 'Hydrostatik sehen: leichter im Wasser'),
    sim5, ('p4-5-lp-kontrolle-auftrieb', 'Kontrollfragen zum Auftrieb'),
    fest5, [uebung('auftrieb', 'Auftriebskraft'), uebung('waage', 'Was zeigt die Waage?'), uebung('dichte-waage', 'Dichte mit der Federwaage')],
    auf5, f'<a href="{TS}#auftrieb">Themenseite 4.5, Auftrieb</a>')

# ------------------------------------------------------------------ Kapitel 6
sim6 = figur_anim('sim6', 'Ein Würfel wird an der Wasseroberfläche losgelassen und pendelt sich ein, schwebt oder sinkt; darunter seine Eintauchtiefe über der Zeit', '-4 -4 308 334',
    '        <div class="reglerfeld">\n          '
    + regler('s6', 'rk', '<i>ρ</i><sub>K</sub> Würfel', 100, 3000, 5, 400, 'kg/m³', 0) + '\n        </div>',
    knoepfe('fl', 'Flüssigkeit', [('1000', 'Süsswasser'), ('1025', 'Meerwasser'), ('790', 'Spiritus')], '1000'))
fest6 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Schwimmen, Schweben, Sinken</div>
          <p>Ganz eingetaucht entscheidet der Vergleich der Dichten:</p>
          <ul>
            <li>\(\rho_K < \rho_{Fl}\): Der Auftrieb ist grösser als die Gewichtskraft, der Körper steigt und <b>schwimmt</b>. Er taucht nur so weit ein, bis \(F_A = F_G\).</li>
            <li>\(\rho_K = \rho_{Fl}\): Er <b>schwebt</b> in jeder Tiefe.</li>
            <li>\(\rho_K > \rho_{Fl}\): Er <b>sinkt</b>.</li>
          </ul>
          <p>Für einen schwimmenden Körper folgt aus \(\rho_{Fl} \cdot V_e \cdot g = \rho_K \cdot V \cdot g\):</p>
          <p>\[ \frac{V_e}{V} = \frac{\rho_K}{\rho_{Fl}} \]</p>
          <p>Bei Hohlkörpern (Schiff, Boje) zählt die <b>mittlere Dichte</b> aus Material und eingeschlossener Luft.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Schwere Körper sinken.» Ein Schiff mit \(80\,000\;\text{t}\) schwimmt, ein Nagel sinkt: Es zählt die Dichte, nicht die Masse.</p>
          <p>Das Verhältnis umgedreht: Der eingetauchte Anteil ist \(\dfrac{\rho_K}{\rho_{Fl}}\) und damit kleiner als 1.</p>
        </div>
      </div>'''
auf6 = test('t6', 'Aufgaben · Kapitel 6', 12, [
    ('6a', 3, r'Ein Floss besteht aus sechs Baumstämmen von je \(0.15\;\text{m}^3\) Holz mit \(600\;\text{kg/m}^3\). Wie viel Last (in kg) trägt es höchstens, bevor es ganz untertaucht?',
     r'<p>\(V = 6 \cdot 0.15\;\text{m}^3 = 0.9\;\text{m}^3\). Ganz eingetaucht: \(F_A = 1000\;\text{kg/m}^3 \cdot 0.9\;\text{m}^3 \cdot 9.81\;\text{m/s}^2\) \(\approx 8830\;\text{N}\); \(F_G = 600\;\text{kg/m}^3 \cdot 0.9\;\text{m}^3 \cdot 9.81\;\text{m/s}^2\) \(\approx 5300\;\text{N}\).</p><p>Zuladung: \(8830\;\text{N} - 5300\;\text{N} \approx 3530\;\text{N}\), also rund \(360\;\text{kg}\).</p>', ''),
    ('6b', 3, r'Ein Frachtschiff fährt vom Rhein (Süsswasser) in die Nordsee (Meerwasser). Taucht es tiefer oder weniger tief ein? Begründe.',
     r'<p>Weniger tief. Das Schiff schwimmt, also \(F_A = F_G\) — die Gewichtskraft bleibt gleich, also muss auch der Auftrieb gleich bleiben. Meerwasser ist dichter: Für denselben Auftrieb genügt ein kleineres verdrängtes Volumen.</p>', ''),
    ('6c', 3, r'Ein Quader (Höhe \(20\;\text{cm}\), Grundfläche \(100\;\text{cm}^2\)) wird aufrecht ins Wasser gesetzt. Das Diagramm zeigt den Auftrieb über der Eintauchtiefe und gestrichelt seine Gewichtskraft. Wie tief taucht er ein? Welche Dichte hat er?',
     r'<p>Er schwimmt dort, wo der Auftrieb die Gewichtskraft erreicht: beim Schnittpunkt, rund \(12\;\text{cm}\) (genau \(h_e = \dfrac{12\;\text{N}}{1000\;\text{kg/m}^3 \cdot 0.01\;\text{m}^2 \cdot 9.81\;\text{m/s}^2}\) \(\approx 0.122\;\text{m} = 12.2\;\text{cm}\)).</p><p>\(\rho_K = \rho_W \cdot \dfrac{h_e}{H}\) \(\approx 1000\;\text{kg/m}^3 \cdot \dfrac{12.2\;\text{cm}}{20\;\text{cm}}\) \(\approx 610\;\text{kg/m}^3\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 0), (20, 1000 * 0.01 * 0.2 * 9.81), (24, 1000 * 0.01 * 0.2 * 9.81)], 0, 24, 0, 22, 4, 4, 'Auftrieb über der Eintauchtiefe: steigt geradlinig von 0 N auf rund 19.6 N bei 20 cm und bleibt dann gleich; gestrichelt die Gewichtskraft 12 N', 'h_e [cm]', 'F [N]', 'kurve-fa', 12, waagrecht_cls='kurve-mini kurve-fg') + '</div>'),
    ('6d', 3, r'Ein U-Boot kann abtauchen, in einer Tiefe schweben und wieder auftauchen. Es hat Tanks, die es mit Wasser fluten oder mit Druckluft leeren kann. Erkläre die drei Zustände mit der mittleren Dichte.',
     r'<p>Leere Tanks: Die mittlere Dichte ist kleiner als die des Wassers, es schwimmt an der Oberfläche. Geflutete Tanks: Die mittlere Dichte wird grösser, es sinkt. Genau so viel Wasser, dass die mittlere Dichte gleich der des Wassers ist: Es schwebt. Zum Auftauchen bläst Druckluft das Wasser aus den Tanks.</p>', ''),
])
k6 = kapitel(6, 'schwimmen', 'Schwimmen, Schweben, Sinken', 'K5', 40,
    r'Du entscheidest aus dem Vergleich der Dichten, ob ein Körper schwimmt, schwebt oder sinkt, und berechnest den eingetauchten Anteil \(\dfrac{V_e}{V} = \dfrac{\rho_K}{\rho_{Fl}}\).',
    ('p4-5-lp-schwimmen', 'Hydrostatik sehen: schwimmen oder sinken'),
    sim6, ('p4-5-lp-kontrolle-schwimmen', 'Kontrollfragen zum Schwimmen'),
    fest6, [uebung('anteil', 'Wie viel liegt unter Wasser?'), uebung('eintauchtiefe', 'Eintauchtiefe eines Quaders'), uebung('mittlere-dichte', 'Mittlere Dichte')],
    auf6, f'<a href="{TS}#schwimmen">Themenseite 4.5, Schwimmen, Schweben, Sinken</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/hydrostatik/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">4.5 · K1 bis K5</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a> → K1, K2 · G2 → <a href="#k2">2</a>, <a href="#k3">3</a> → K3 · G3 → <a href="#k2">2</a> → K3 · G4 → <a href="#k4">4</a> → K4 · G5 → <a href="#k5">5</a> → K5 · G6 → <a href="#k6">6</a> → K5</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Das U-Rohr mit zwei Flüssigkeiten, \(\rho_1 \cdot h_1 = \rho_2 \cdot h_2\), und die Schlauchwaage → <a href="{TS}#u-rohr">Themenseite 4.5, U-Rohr</a></li>
        <li>Überdruck und absoluter Druck in Reifen und Flaschen → <a href="{LPV}#ls8">Leitprogramm Grössen, Messen, Druck</a></li>
        <li>Wie sich ein Gas zusammendrücken lässt (Boyle-Mariotte) → <a href="leitprogramm-ideale-gase.html">Leitprogramm Ideale Gase</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Hydrostatik, Version 1.0 (05.10.2026, nach /lp-pruefung am 06.10.2026 freigeschaltet).
     Sechstes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip → ② laufende Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF (downloads/leitprogramme/hydrostatik/*.tex). Quelle: scripts/lp/hydrostatik/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 4.5 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 den Grundbegriff «Druck» definieren und die wichtigsten Einheiten angeben
       K2 den Druck zwischen zwei Festkörpern berechnen
       K3 den Druck in einer Flüssigkeit berechnen (hydrostatische Grundgleichung) und mit dem
          Luftdruck in Verbindung bringen
       K4 das Pascal’sche Gesetz anhand einfacher Aufgaben anwenden
       K5 das archimedische Prinzip definieren und in einfachen Aufgaben anwenden

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1, K2 → Kap. 1 · Aufg. 1a–1d · G1      K3 → Kap. 2, 3 · Aufg. 2a–3d · G2 G3 (G3: Paradoxon)
       K4 → Kap. 4 · Aufg. 4a–4d · G4          K5 → Kap. 5, 6 · Aufg. 5a–6d · G5 G6
     Bewusst weggelassen: U-Rohr mit zwei Flüssigkeiten (in keiner Kompetenz genannt, auf der Themenseite).
     Zeiten: K0 10 · K1–K6 je 40 · Gesamttest 30 = 280 min ≈ 6.2 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Hydrostatik</h1>
      <p class="unter">Druck, Schweredruck, Luftdruck, hydraulische Presse, Auftrieb, Schwimmen und Sinken — mit laufenden Simulationen. Sechs Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 4 · Teilgebiet 4.5</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Druck</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Schweredruck</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Luftdruck</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Pascal'sches Gesetz</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Auftrieb</span></a></li></ol>
    <p class="lekt">Lektion 6</p>
    <ol><li><a href="#k6"><span class="nr">6</span><span>Schwimmen, Schweben, Sinken</span></a></li></ol>
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
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma; Brüche wie <code>1/2</code> und Zehnerpotenzen wie <code>2.4e-3</code> gehen auch. Richtig ist, was auf drei signifikante Stellen stimmt.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 4, Teilgebiet 4.5 Hydrostatik</p>
        <ul>
          <li><b>K1</b> den Grundbegriff «Druck» definieren und die wichtigsten Einheiten angeben</li>
          <li><b>K2</b> den Druck zwischen zwei Festkörpern berechnen</li>
          <li><b>K3</b> den Druck in einer Flüssigkeit berechnen (hydrostatische Grundgleichung) und mit dem Luftdruck in Verbindung bringen</li>
          <li><b>K4</b> das Pascal’sche Gesetz anhand einfacher Aufgaben anwenden</li>
          <li><b>K5</b> das archimedische Prinzip definieren und in einfachen Aufgaben anwenden</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">4.5 Hydrostatik</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Hydrostatik · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Druck') + k1 + band(2, 'Schweredruck') + k2 + band(3, 'Luftdruck') + k3
        + band(4, 'Pascal') + k4 + band(5, 'Auftrieb') + k5 + band(6, 'Schwimmen') + k6 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
