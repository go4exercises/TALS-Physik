"""Baut leitprogramme/leitprogramm-ausdehnung.html aus einer Kapitelbeschreibung (seit 07.10.2026).

  python3 scripts/lp/ausdehnung/seite.py

Leitprogramm Wärmeausdehnung und Gase (RLP 5.3) nach dem Kapitelmuster (HOWTO-leitprogramme.md §4),
als Kopie von scripts/lp/hydrostatik/ entstanden: Kopf, CSS, Grundskript und Bausteine von dort, neu
sind Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Siehe README.md.
"""
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-ausdehnung.html'
TS = '../themen/p5-3-waermeausdehnung.html'
RLP = '5.3'

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
<title>Leitprogramm Wärmeausdehnung und Gase</title>
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
/* Diagramme und Szenen, Farbe = eine Bedeutung: Ausdehnung (Δl, ΔV, Δh) und der laufende Zustand Bernstein,
   Ausgangszustand und voriger Lauf grau gestrichelt, Temperatur Orange, Druck Rot, Volumen Grün;
   Wasser Hellblau, Gas hellgrau, Gefässe und Kolben Grau */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.sim .skala.klein{font-size:8px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.vorher{fill:none;stroke:var(--tinte-2);stroke-width:1.8;stroke-dasharray:5 4;opacity:.6}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
text.p-text.p-dl{fill:var(--bernstein)} text.p-text.p-eins{fill:var(--tinte-2)}
.p-dl{fill:var(--bernstein)} .p-eins{fill:var(--tinte-2)}
.pf-linie{stroke-width:2.6;fill:none}
.pf-linie.pf-dl{stroke:var(--bernstein)} .pf-kopf.pf-dl{fill:var(--bernstein)}
.pf-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:3.5px;paint-order:stroke;fill:var(--tinte)}
text.t-dl{fill:var(--bernstein)} text.t-temp{fill:var(--orange)} text.t-druck{fill:var(--rot)} text.t-vol{fill:var(--gruen)}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bt-meldung{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:10.5px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.legende{fill:var(--tinte-2);font-family:var(--sans);font-size:10px;font-weight:700}
.legende.l-dl{fill:var(--bernstein)} .legende.t-temp{fill:var(--orange)}
.kurve-dl{fill:none;stroke:var(--bernstein);stroke-width:2.6}
.kurve-hilf{fill:none;stroke:var(--tinte-2);stroke-width:1.6;stroke-dasharray:5 4;opacity:.75}
.kurve-iso{fill:none;stroke:var(--orange);stroke-width:1.6;stroke-dasharray:5 4}
.weg{fill:none;stroke:var(--bernstein);stroke-width:2.2;opacity:.7}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
.tick{stroke:var(--tinte-2);stroke-width:1.2}
.saeule-text{fill:var(--weiss);font-family:var(--sans);font-size:9px;font-weight:700}
/* Körper, Gefässe, Thermometer, Manometer */
.wand{fill:var(--tinte-2);opacity:.55}
.stab{fill:#b9bec4;stroke:var(--tinte-2);stroke-width:1.2}
.thermo-glas{fill:var(--karte);stroke:var(--tinte-2);stroke-width:1.2}
.thermo-saeule,.thermo-kugel{fill:var(--orange)}
.fluessig{fill:#c9a35a;opacity:.45}
.glas{fill:none;stroke:var(--tinte-2);stroke-width:1.8;stroke-linejoin:round}
.wuerfel{fill:#b9bec4;stroke:var(--bernstein);stroke-width:2}
.meer{fill:#5fa9c6;opacity:.35}
.warm{fill:var(--orange)}
.land{fill:#b8a98c;opacity:.7}
.gefaess{fill:none;stroke:var(--tinte-2);stroke-width:2;stroke-linejoin:round}
.masslinie{stroke:var(--tinte);stroke-width:1.4}
.pegel{fill:var(--karte);stroke:var(--tinte-2);stroke-width:1.2}
.pegel-wasser{fill:var(--bernstein);opacity:.75}
.lupe{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:2 3}
.gas{fill:var(--papier-2)}
.teilchen{fill:var(--tinte-2)}
.kolben{fill:var(--tinte-2)} .stange{stroke:var(--tinte-2);stroke-width:3}
.gewicht{fill:var(--tinte);opacity:.8}
.bad{fill:#5fa9c6;opacity:.22}
.flasche-wand{fill:none;stroke:var(--tinte);stroke-width:4;stroke-linejoin:round}
.manometer{fill:var(--karte);stroke:var(--tinte);stroke-width:2}
.zeiger{stroke:var(--rot);stroke-width:2.2;stroke-linecap:round}
.schlauch{stroke:var(--tinte-2);stroke-width:2}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
svg.mini.breit{width:260px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.kurve-dl{stroke:var(--bernstein)} .kurve-mini.kurve-p{stroke:var(--rot)} .kurve-mini.kurve-v{stroke:var(--gruen)}
.kurve-mini.kurve-gestr{stroke-dasharray:6 4}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.p-mini{fill:var(--tinte)}
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
  var KEY = 'leitprogramm-ausdehnung-v1';

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

# Footer: nur die Marken. Den Inhalt setzt scripts/build-seo.py — nach jedem Bau laufen lassen.
FUSS = '''<!-- FUSS:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->
<!-- FUSS:ENDE -->

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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">{RLP} · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


def figur_anim(sid, label, svg_box, inhalt, knoepfe='', hilfs=None):
    """Simulation mit laufender Animation: Aktionsknöpfe (Start, Zurück …) setzt seite.js in .sim-aktionen.
    hilfs: Schalter für die gestrichelten Hilfslinien (HOWTO-leitprogramme §4)."""
    h = f'\n        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien ({hilfs})</label>' if hilfs else ''
    return f'''      <figure class="sim sim-gross" id="{sid}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="{svg_box}" role="img" aria-label="{label}"></svg>{h}
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


def linien_bild(punkte, x0, x1, y0, y1, xt, yt, label, xname, yname, cls='kurve-v', waagrecht=None, weitere=(), waagrecht_cls='vorher', marken=(), xs=1, ys=1):
    """Diagramm für Aufgaben: Streckenzug durch die Punkte, Gitter je xt und yt, Achsen mit Einheit.
    marken: [(x, y, text, dx, dy)] Punkte mit Namen (Versatz in px); xs, ys: nur jede xs-te bzw. ys-te
    Gitterlinie beschriftet."""
    w, h, ox, oy = 250, 150, 44, 126
    kx, ky = (w - ox - 16) / (x1 - x0), (oy - 18) / (y1 - y0)
    X = lambda x: ox + (x - x0) * kx
    Y = lambda y: oy - (y - y0) * ky
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 8}" role="img" aria-label="{label}">']
    x, k = x0, 0
    while x <= x1 + 1e-9:
        t.append(f'<line x1="{X(x):.1f}" y1="{Y(y1):.1f}" x2="{X(x):.1f}" y2="{oy}" class="gitter"/>')
        if k and k % xs == 0: t.append(f'<text x="{X(x):.1f}" y="{oy + 13}" text-anchor="middle" class="skala">{x:g}</text>')
        x += xt; k += 1
    y, k = y0, 0
    while y <= y1 + 1e-9:
        t.append(f'<line x1="{ox}" y1="{Y(y):.1f}" x2="{X(x1):.1f}" y2="{Y(y):.1f}" class="gitter"/>')
        if k % ys == 0: t.append(f'<text x="{ox - 5}" y="{Y(y) + 4:.1f}" text-anchor="end" class="skala">{round(y, 6):g}</text>')
        y += yt; k += 1
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{X(x1) + 8:.1f}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{Y(y1) - 8:.1f}" class="achse"/>')
    if waagrecht is not None:
        t.append(f'<line x1="{ox}" y1="{Y(waagrecht):.1f}" x2="{X(x1):.1f}" y2="{Y(waagrecht):.1f}" class="{waagrecht_cls}"/>')
    for pk, ck in [(punkte, cls)] + list(weitere):     # weitere Kurven: [(punkte, klasse), …]
        t.append('<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in pk) + f'" class="kurve-mini {ck}"/>')
    for mx, my, mt, dx, dy in marken:
        t.append(f'<circle cx="{X(mx):.1f}" cy="{Y(my):.1f}" r="3" class="p-mini"/>')
        if mt: t.append(f'<text x="{X(mx) + dx:.1f}" y="{Y(my) + dy:.1f}" text-anchor="middle" class="mini-name">{mt}</text>')
    t.append(f'<text x="{X(x1) + 8:.1f}" y="{oy - 6}" text-anchor="end" class="achsname">{tief(xname)}</text><text x="{ox + 6}" y="{Y(y1) - 2:.1f}" class="achsname">{tief(yname)}</text></svg>')
    return ''.join(t)




def tief(s):
    """«F_y [N]» für SVG-Text: Index tiefgestellt (wie stext in seite.js)."""
    import re as _re
    return _re.sub(r'_([A-Za-z0-9,]+)(.*)', r'<tspan dy="3" font-size="0.78em">\1</tspan><tspan dy="-3">\2</tspan>', s)



# ------------------------------------------------------------------ Kapitel 0: Vorwissen
LPV = 'leitprogramm-vorwissen.html'
LPR = 'leitprogramm-rechnen.html'
P51 = '../themen/p5-1-temperatur.html'
P01 = '../themen/p0-1-vorwissen-mathematik.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 5.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Zehnerpotenzen, Volumen- und Längeneinheiten, Celsius und Kelvin, Gleichungen umstellen. Wenn das wackelt: <a href="''' + LPR + '''">Leitprogramm Rechnen und Schliessen</a> und <a href="''' + P51 + '''#umrechnen">Themenseite 5.1, Umrechnen und Temperaturdifferenz</a>.</p>
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Rechne mit dem Taschenrechner und gib das Ergebnis ohne Zehnerpotenz an: \(12 \cdot 10^{-6} \cdot 40 \cdot 25\) und \(2.1 \cdot 10^{-4} \cdot 3500 \cdot 0.8\). Schreibe \(0.00024\) als Zehnerpotenz.',
     r'<p>\(12 \cdot 10^{-6} \cdot 40 \cdot 25 = 0.012\); \(2.1 \cdot 10^{-4} \cdot 3500 \cdot 0.8 = 0.588\); \(0.00024 = 2.4 \cdot 10^{-4}\).</p><p class="komm">Falsch? <a href="' + LPR + r'#ls5">Leitprogramm Rechnen und Schliessen: Zehnerpotenzen und die EE-Taste</a></p>', ''),
    ('0b', 3, r'Rechne um: \(2.5\;\text{l}\) in \(\text{cm}^3\) und in \(\text{m}^3\), \(0.045\;\text{m}\) in mm und \(350\;\text{cm}^3\) in Liter.',
     r'<p>\(2.5\;\text{l} = 2500\;\text{cm}^3\) (\(1\;\text{l} = 1000\;\text{cm}^3\)) \(= 0.0025\;\text{m}^3\) (\(1\;\text{l} = 10^{-3}\;\text{m}^3\)); \(0.045\;\text{m} = 45\;\text{mm}\); \(350\;\text{cm}^3 = 0.35\;\text{l}\).</p><p class="komm">Falsch? <a href="' + LPV + r'#ls3">Leitprogramm Grössen, Messen, Druck: Fläche und Volumen umrechnen</a></p>', ''),
    ('0c', 2, r'Rechne \(37\;^\circ\text{C}\) in Kelvin um. Wie gross ist die Temperaturdifferenz zwischen \(-12\;^\circ\text{C}\) und \(18\;^\circ\text{C}\), in Kelvin?',
     r'<p>\(T\;[\text{K}] = \vartheta\;[^\circ\text{C}] + 273.15\) \(= 37 + 273.15 = 310.15\), also \(T = 310.15\;\text{K}\).</p><p>\(\Delta T = 18\;^\circ\text{C} - (-12\;^\circ\text{C}) = 30\;\text{K}\): Eine Differenz ist in Kelvin gleich gross wie in Grad Celsius.</p><p class="komm">Falsch? <a href="' + P51 + r'#umrechnen">Themenseite 5.1, Umrechnen und Temperaturdifferenz</a></p>', ''),
    ('0d', 2, r'Stelle \(\Delta l = \alpha \cdot l_0 \cdot \Delta T\) nach \(\Delta T\) um und \(\dfrac{p_1 \cdot V_1}{T_1} = \dfrac{p_2 \cdot V_2}{T_2}\) nach \(p_2\).',
     r'<p>\(\Delta T = \dfrac{\Delta l}{\alpha \cdot l_0}\); \(p_2 = \dfrac{p_1 \cdot V_1 \cdot T_2}{T_1 \cdot V_2}\).</p><p class="komm">Falsch? <a href="' + LPR + r'#ls4">Leitprogramm Rechnen und Schliessen: Gleichungen umstellen</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Ein links eingespannter Stab wird erwärmt oder abgekühlt; sein freies Ende wandert um die Längenänderung; darunter die Längenänderung über der Temperatur für drei Werkstoffe', '-4 -4 308 346',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'l0', '<i>l</i><sub>0</sub> Länge', 1, 100, 1, 70, 'm', 0) + '\n          '
    + regler('s1', 't', '<i>ϑ</i> Temperatur', -30, 80, 1, 35, '°C', 0) + '\n        </div>',
    knoepfe('mat', 'Werkstoff', [('st', 'Stahl'), ('me', 'Messing'), ('al', 'Aluminium')], 'st'), hilfs='andere Werkstoffe')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Längenausdehnung</div>
          <p>Wird ein fester Körper wärmer, schwingen seine Teilchen stärker und brauchen mehr Platz — er wird länger. Die Längenänderung ist proportional zur Anfangslänge \(l_0\) und zur Temperaturänderung \(\Delta T\):</p>
          <p>\[ \Delta l = \alpha \cdot l_0 \cdot \Delta T \qquad l = l_0 + \Delta l \]</p>
          <p>\(\alpha\): Längenausdehnungskoeffizient, Einheit \(\tfrac{1}{\text{K}}\). Stahl \(12\), Messing \(18.4\), Aluminium \(23.8\), je \(10^{-6}\;\tfrac{1}{\text{K}}\). \(\Delta T = \vartheta_2 - \vartheta_1\) ist eine Temperaturdifferenz: in Kelvin gleich gross wie in Grad Celsius. Beim Abkühlen sind \(\Delta T\) und \(\Delta l\) negativ.</p>
          <p>Jede Strecke im Körper wächst um denselben Anteil \(\alpha \cdot \Delta T\) — auch der Durchmesser eines Lochs. Gültig ohne Wechsel des Aggregatzustands, mit \(\alpha\) als konstantem Tabellenwert (um \(20\;^\circ\text{C}\)). Kann sich ein Bauteil nicht ausdehnen, entstehen grosse Kräfte: darum Dehnungsfugen und Rollenlager.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Eine Temperatur statt der Temperaturänderung eingesetzt: Ein Aluminiumrohr, das von \(15\;^\circ\text{C}\) auf \(35\;^\circ\text{C}\) erwärmt wird, hat \(\Delta T = 20\;\text{K}\), nicht \(35\;\text{K}\) und nicht \(308\;\text{K}\).</p>
          <p>Die Zehnerpotenz vergessen: \(12 \cdot 10^{-6}\;\tfrac{1}{\text{K}}\) heisst \(0.000012\) je Kelvin. \(\Delta l\) kommt in der Einheit von \(l_0\) heraus, meist in Meter — dann in mm umrechnen.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Eine Brücke liegt an einem Ende auf Rollen, und zwischen Brücke und Strasse greifen Stahlzähne ineinander (Fahrbahnübergang). Erkläre mit dem Teilchenmodell, warum sich die Brücke beim Erwärmen verlängert, und begründe, warum man sie nicht an beiden Enden fest einmauert.',
     r'<p>Bei höherer Temperatur schwingen die Teilchen stärker um ihre Plätze; ihr mittlerer Abstand wächst. Über die ganze Länge summiert wird die Brücke messbar länger — die Teilchen selbst werden nicht grösser.</p><p>An beiden Enden fest eingemauert, könnte sie sich nicht ausdehnen: Es entstünden sehr grosse Druckkräfte, die Brücke würde sich verbiegen oder die Widerlager beschädigen. Rollen und Fahrbahnübergang lassen die Längenänderung zu.</p>', ''),
    ('1b', 3, r'Die Stahlfahrbahn einer \(380\;\text{m}\) langen Brücke wird bei \(12\;^\circ\text{C}\) eingebaut. Im Winter kann sie \(-25\;^\circ\text{C}\) kalt, im Sommer \(45\;^\circ\text{C}\) warm werden. Um wie viel ändert sich ihre Länge bis zu diesen beiden Temperaturen? Wie viel Bewegung muss der Fahrbahnübergang insgesamt erlauben?',
     r'<p>Winter: \(\Delta T = -25\;^\circ\text{C} - 12\;^\circ\text{C} = -37\;\text{K}\); \(\Delta l = \alpha \cdot l_0 \cdot \Delta T\) \(= 12 \cdot 10^{-6}\;\tfrac{1}{\text{K}} \cdot 380\;\text{m} \cdot (-37\;\text{K})\) \(\approx -0.169\;\text{m}\).</p><p>Sommer: \(\Delta T = 45\;^\circ\text{C} - 12\;^\circ\text{C} = 33\;\text{K}\); \(\Delta l = 12 \cdot 10^{-6}\;\tfrac{1}{\text{K}} \cdot 380\;\text{m} \cdot 33\;\text{K}\) \(\approx 0.150\;\text{m}\).</p><p>Insgesamt \(0.169\;\text{m} + 0.150\;\text{m} \approx 0.319\;\text{m}\), rund \(32\;\text{cm}\) — gleich viel wie \(\alpha \cdot l_0 \cdot 70\;\text{K}\).</p>', ''),
    ('1c', 3, r'Das Diagramm zeigt die Längenänderung zweier Stäbe A und B, beide \(4.0\;\text{m}\) lang, über der Temperaturänderung. Lies bei \(\Delta T = 50\;\text{K}\) ab, bestimme \(\alpha\) für beide Stäbe und ordne den Werkstoff zu (Tabelle im Festhalten).',
     r'<p>A: \(\Delta l \approx 4.8\;\text{mm}\); \(\alpha = \dfrac{\Delta l}{l_0 \cdot \Delta T}\) \(= \dfrac{0.0048\;\text{m}}{4.0\;\text{m} \cdot 50\;\text{K}}\) \(= 24 \cdot 10^{-6}\;\tfrac{1}{\text{K}}\): Aluminium (\(23.8\)).</p><p>B: \(\Delta l = 2.4\;\text{mm}\); \(\alpha = \dfrac{0.0024\;\text{m}}{4.0\;\text{m} \cdot 50\;\text{K}}\) \(= 12 \cdot 10^{-6}\;\tfrac{1}{\text{K}}\): Stahl.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 0), (60, 23.8e-6 * 4000 * 60)], 0, 60, 0, 6.0, 10, 0.4, 'Längenänderung über der Temperaturänderung für zwei Stäbe: A steigt auf rund 4.8 mm bei 50 K, B auf 2.4 mm bei 50 K', 'ΔT [K]', 'Δl [mm]', 'kurve-dl',
                                                      weitere=[([(0, 0), (60, 12e-6 * 4000 * 60)], 'kurve-dl kurve-gestr')], marken=[(50, 23.8e-6 * 4000 * 50, 'A', -8, -8), (50, 2.4, 'B', 8, 14)], ys=2) + '</div>'),
    ('1d', 3, r'Ein Stahlring hat bei \(20\;^\circ\text{C}\) einen Innendurchmesser von \(49.95\;\text{mm}\). Er soll auf eine Welle mit \(50.00\;\text{mm}\) Durchmesser geschoben werden. Auf welche Temperatur muss man den Ring mindestens erwärmen? Begründe, warum dabei auch das Loch grösser wird.',
     r'<p>Der Ring dehnt sich in alle Richtungen um denselben Anteil aus; das Loch wächst wie das Material darum herum. Der Innendurchmesser ist eine Länge: \(\Delta l = 0.05\;\text{mm}\), \(l_0 = 49.95\;\text{mm}\).</p><p>\(\Delta T = \dfrac{\Delta l}{\alpha \cdot l_0}\) \(= \dfrac{0.05\;\text{mm}}{12 \cdot 10^{-6}\;\tfrac{1}{\text{K}} \cdot 49.95\;\text{mm}}\) \(\approx 83\;\text{K}\), also auf rund \(20\;^\circ\text{C} + 83\;\text{K} \approx 103\;^\circ\text{C}\). Erkaltet sitzt der Ring fest (Schrumpfverbindung).</p>', ''),
])
k1 = kapitel(1, 'laenge', 'Längenausdehnung', 'K1', 45,
    r'Du berechnest mit \(\Delta l = \alpha \cdot l_0 \cdot \Delta T\), um wie viel ein fester Körper beim Erwärmen länger und beim Abkühlen kürzer wird, und bestimmst daraus die neue Länge \(l = l_0 + \Delta l\).',
    ('p5-3-lp-laenge', 'Ausdehnung sehen: der Stab wird länger'),
    sim1, ('p5-3-lp-kontrolle-laenge', 'Kontrollfragen zur Längenausdehnung'),
    fest1, [uebung('laenge', 'Längenänderung'), uebung('temperatur', 'Wann schliesst sich die Fuge?'), uebung('alpha', 'Welcher Werkstoff?')],
    auf1, f'<a href="{TS}#laenge">Themenseite 5.3, Längenausdehnung berechnen</a> · <a href="{TS}#definition">Grundbegriffe</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur_anim('sim2', 'Eine Flüssigkeit in einem Gefäss mit Steigrohr oder ein Würfel wird erwärmt; die Volumenzunahme steigt im Rohr bzw. der Würfel wächst; darunter die Volumenzunahme über der Erwärmung für vier Stoffe', '-4 -4 308 346',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'V0', '<i>V</i><sub>0</sub> Volumen', 0.1, 5, 0.1, 1.5, 'l', 1) + '\n          '
    + regler('s2', 't', '<i>ϑ</i> Temperatur', 20, 80, 1, 35, '°C', 0) + '\n        </div>',
    knoepfe('stoff', 'Stoff', [('et', 'Ethanol'), ('hg', 'Quecksilber'), ('al', 'Aluminium'), ('st', 'Stahl')], 'et'), hilfs='andere Stoffe')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Volumenausdehnung</div>
          <p>\[ \Delta V = \gamma \cdot V_0 \cdot \Delta T \qquad V = V_0 + \Delta V \]</p>
          <p>\(\gamma\): Volumenausdehnungskoeffizient in \(\tfrac{1}{\text{K}}\). <b>Festkörper</b> wachsen in drei Richtungen: \(\gamma \approx 3 \cdot \alpha\) (eine Näherung, weil \(\alpha \cdot \Delta T\) sehr klein ist). <b>Flüssigkeiten</b> haben keine eigene Form; für sie steht \(\gamma\) in der Tabelle: Ethanol \(1.10 \cdot 10^{-3}\;\tfrac{1}{\text{K}}\), Quecksilber \(0.18 \cdot 10^{-3}\;\tfrac{1}{\text{K}}\). Sie dehnen sich viel stärker aus als Festkörper (Ethanol rund dreissigmal so stark wie Stahl), weil ihre Teilchen schwächer gebunden sind.</p>
          <p><b>Im Gefäss</b> wächst auch der Innenraum, als wäre er aus dem Material des Gefässes. Überlaufen kann nur die Differenz \(\Delta V_\text{Fl} - \Delta V_\text{Gef}\); bei Ethanol im Metallgefäss ist sie nur wenig kleiner als \(\Delta V_\text{Fl}\), bei Quecksilber merklich (im Glasthermometer rund \(13\;\%\) weniger).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Bei einem Festkörper mit \(\alpha\) statt mit \(3 \cdot \alpha\) gerechnet: Das Volumen wächst dreimal so stark wie eine Kante.</p>
          <p>Die Zehnerpotenzen verwechselt: Flüssigkeiten \(10^{-3}\), Metalle \(10^{-6}\). Und Liter in Milliliter: \(1\;\text{l} = 1000\;\text{ml}\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Erkläre mit den Teilchen, warum sich Flüssigkeiten beim Erwärmen viel stärker ausdehnen als Festkörper. Warum hat ein Flüssigkeitsthermometer unten ein grosses Vorratsgefäss und darüber eine sehr dünne Kapillare? Rechne für \(0.30\;\text{cm}^3\) Quecksilber und eine Kapillare mit \(A = 0.010\;\text{mm}^2\): Um wie viel steigt der Faden je Kelvin (Säule: \(V = A \cdot h\))?',
     r'<p>In einem Festkörper sitzen die Teilchen an festen Plätzen; starke Bindungen lassen den Abstand nur wenig wachsen. In einer Flüssigkeit sind sie beweglich und schwächer gebunden — stärkere Bewegung vergrössert ihren Abstand viel mehr (\(\gamma\) rund \(10^{-3}\;\tfrac{1}{\text{K}}\) statt rund \(10^{-5}\;\tfrac{1}{\text{K}}\)).</p><p>\(\Delta V\) wächst mit \(V_0\): Viel Flüssigkeit gibt ein messbares \(\Delta V\). In der dünnen Kapillare wird dieses kleine Volumen zu einer langen Säule — die Anzeige wird gut ablesbar.</p><p>\(\Delta V = \gamma \cdot V_0 \cdot \Delta T\) \(= 0.18 \cdot 10^{-3}\;\tfrac{1}{\text{K}} \cdot 300\;\text{mm}^3 \cdot 1\;\text{K}\) \(= 0.054\;\text{mm}^3\) (\(1\;\text{cm}^3 = 1000\;\text{mm}^3\)); \(h = \dfrac{\Delta V}{A}\) \(= \dfrac{0.054\;\text{mm}^3}{0.010\;\text{mm}^2}\) \(= 5.4\;\text{mm}\) je Kelvin.</p>', ''),
    ('2b', 3, r'Ein Kolben aus Aluminium hat bei \(20\;^\circ\text{C}\) das Volumen \(350\;\text{cm}^3\). Im Motor wird er \(220\;^\circ\text{C}\) heiss. Um wie viel wächst sein Volumen? Gib die Zunahme auch in Prozent an.',
     r'<p>\(\gamma \approx 3 \cdot \alpha\) \(= 3 \cdot 23.8 \cdot 10^{-6}\;\tfrac{1}{\text{K}}\) \(= 71.4 \cdot 10^{-6}\;\tfrac{1}{\text{K}}\); \(\Delta T = 200\;\text{K}\).</p><p>\(\Delta V = \gamma \cdot V_0 \cdot \Delta T\) \(= 71.4 \cdot 10^{-6}\;\tfrac{1}{\text{K}} \cdot 350\;\text{cm}^3 \cdot 200\;\text{K}\) \(\approx 5.0\;\text{cm}^3\). Das sind \(\gamma \cdot \Delta T \approx 1.4\;\%\) des Volumens.</p>', ''),
    ('2c', 3, r'Für \(4.0\;\text{l}\) einer Flüssigkeit zeigt das Diagramm die Volumenzunahme über der Erwärmung. Lies einen Punkt ab, bestimme \(\gamma\) und entscheide: Wasser (\(0.21\), Wert bei \(20\;^\circ\text{C}\)), Quecksilber (\(0.18\)) oder Ethanol (\(1.10\), je \(10^{-3}\;\tfrac{1}{\text{K}}\))?',
     r'<p>Bei \(50\;\text{K}\) liest man \(36\;\text{ml}\) ab. \(\gamma = \dfrac{\Delta V}{V_0 \cdot \Delta T}\) \(= \dfrac{36\;\text{ml}}{4000\;\text{ml} \cdot 50\;\text{K}}\) \(= 0.18 \cdot 10^{-3}\;\tfrac{1}{\text{K}}\): Quecksilber. Wasser gäbe \(42\;\text{ml}\), Ethanol \(220\;\text{ml}\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 0), (50, 0.18e-3 * 4000 * 50)], 0, 50, 0, 48, 10, 4, 'Volumenzunahme über der Erwärmung: Gerade durch den Ursprung und den Punkt 50 K, 36 ml', 'ΔT [K]', 'ΔV [ml]', 'kurve-dl', marken=[(50, 36, '', 0, 0)], ys=2) + '</div>'),
    ('2d', 3, r'Eine Aluminiumflasche (Innenvolumen \(1.5\;\text{l}\)) wird bei \(15\;^\circ\text{C}\) randvoll mit Ethanol gefüllt und auf \(40\;^\circ\text{C}\) erwärmt. Wie viel liefe über, wenn die Flasche starr wäre? Wie viel läuft wirklich über?',
     r'<p>Starre Flasche: \(\Delta V_\text{Fl} = \gamma \cdot V_0 \cdot \Delta T\) \(= 1.10 \cdot 10^{-3}\;\tfrac{1}{\text{K}} \cdot 1.5\;\text{l} \cdot 25\;\text{K}\) \(\approx 0.0413\;\text{l} = 41.3\;\text{ml}\).</p><p>Der Innenraum wächst wie Aluminium: \(\Delta V_\text{Gef} = 71.4 \cdot 10^{-6}\;\tfrac{1}{\text{K}} \cdot 1.5\;\text{l} \cdot 25\;\text{K}\) \(\approx 0.0027\;\text{l} = 2.7\;\text{ml}\). Es läuft \(41.3\;\text{ml} - 2.7\;\text{ml} \approx 38.6\;\text{ml}\) über.</p>', ''),
])
k2 = kapitel(2, 'volumen', 'Volumenausdehnung', 'K1', 45,
    r'Du berechnest die Volumenänderung \(\Delta V = \gamma \cdot V_0 \cdot \Delta T\) von Festkörpern (mit \(\gamma \approx 3 \cdot \alpha\)) und von Flüssigkeiten und begründest, warum sich Flüssigkeiten viel stärker ausdehnen.',
    ('p5-3-lp-volumen', 'Ausdehnung sehen: in drei Richtungen'),
    sim2, ('p5-3-lp-kontrolle-volumen', 'Kontrollfragen zur Volumenausdehnung'),
    fest2, [uebung('volumen', 'Flüssigkeit erwärmen'), uebung('volumen-fest', 'Festkörper: γ aus α'), uebung('fuellen', 'Wie viel darf hinein?')],
    auf2, f'<a href="{TS}#volumen">Themenseite 5.3, Volumenausdehnung von Festkörpern und Flüssigkeiten</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Schnitt durch ein Meer: Die oberste Schicht erwärmt sich und dehnt sich aus, ein Pegel zeigt den Anstieg in Zentimeter; darunter der Anstieg über der Erwärmung', '-4 -4 308 346',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'h0', '<i>h</i><sub>0</sub> Schicht', 50, 2000, 50, 1200, 'm', 0) + '\n          '
    + regler('s3', 'dT', 'Δ<i>T</i> Erwärmung', 0.1, 3, 0.1, 0.8, 'K', 1) + '\n        </div>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wasser: Dichte, Anomalie, Meeresspiegel</div>
          <p><b>Dichte.</b> Beim Erwärmen bleibt die Masse gleich, das Volumen wächst — die Dichte sinkt:</p>
          <p>\[ \rho = \frac{\rho_0}{1 + \gamma \cdot \Delta T} \]</p>
          <p><b>Anomalie des Wassers.</b> Wasser hat seine grösste Dichte bei \(4\;^\circ\text{C}\) (rund \(1000\;\text{kg/m}^3\)). Zwischen \(0\;^\circ\text{C}\) und \(4\;^\circ\text{C}\) zieht es sich beim Erwärmen zusammen, und beim Gefrieren dehnt es sich um rund \(9\;\%\) aus (Eis: \(917\;\text{kg/m}^3\)). Darum liegt im Winter Wasser von \(4\;^\circ\text{C}\) am Grund eines Sees, das Eis schwimmt oben, und volle Wasserleitungen platzen beim Gefrieren. Für Wasser ist \(\gamma\) keine Konstante; \(0.21 \cdot 10^{-3}\;\tfrac{1}{\text{K}}\) gilt um \(20\;^\circ\text{C}\).</p>
          <p><b>Meeresspiegel.</b> Erwärmt sich die oberste Schicht der Dicke \(h_0\) um \(\Delta T\), steigt das Meer um</p>
          <p>\[ \Delta h = \gamma \cdot h_0 \cdot \Delta T \]</p>
          <p>(aus \(\Delta V = \gamma \cdot V_0 \cdot \Delta T\) mit \(V = A \cdot h\) und gleichbleibender Fläche \(A\)). Modell: \(\gamma\) konstant, die Schicht überall gleich warm; schmelzende Gletscher kommen noch dazu.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die ganze Meerestiefe eingesetzt: Es dehnt sich nur das Wasser aus, das wärmer wird — \(h_0\) ist die Dicke der erwärmten Schicht.</p>
          <p>\(\Delta h\) kommt in der Einheit von \(h_0\) heraus, in Meter: \(0.15\;\text{m} = 15\;\text{cm}\).</p>
        </div>
      </div>'''
P3C = [(t / 10, ((999.83952 + 16.945176 * t / 10 - 7.9870401e-3 * (t / 10) ** 2 - 46.170461e-6 * (t / 10) ** 3 + 105.56302e-9 * (t / 10) ** 4 - 280.54253e-12 * (t / 10) ** 5) / (1 + 16.879850e-3 * t / 10))) for t in range(0, 101, 2)]
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Eine volle Wasserleitung im unbeheizten Keller gefriert im Winter und platzt. Erkläre mit der Anomalie des Wassers. Wie viel Volumen braucht \(1.0\;\text{kg}\) Eis (\(917\;\text{kg/m}^3\)) im Vergleich zu \(1.0\;\text{kg}\) Wasser (\(1000\;\text{kg/m}^3\))?',
     r'<p>Anders als die meisten Stoffe dehnt sich Wasser beim Gefrieren aus: Eis hat die kleinere Dichte, dieselbe Masse braucht mehr Platz. Die Leitung kann nicht nachgeben und platzt.</p><p>\(V = \dfrac{m}{\rho}\): Wasser \(\dfrac{1.0\;\text{kg}}{1000\;\text{kg/m}^3} = 1.0 \cdot 10^{-3}\;\text{m}^3 = 1.0\;\text{l}\); Eis \(\dfrac{1.0\;\text{kg}}{917\;\text{kg/m}^3} \approx 1.09 \cdot 10^{-3}\;\text{m}^3 = 1.09\;\text{l}\) — rund \(9\;\%\) mehr.</p>', ''),
    ('3b', 3, r'Vergleiche zwei Annahmen für ein Meer: (1) Die obersten \(1500\;\text{m}\) erwärmen sich um \(0.6\;\text{K}\). (2) Nur die obersten \(500\;\text{m}\) erwärmen sich, dafür um \(1.8\;\text{K}\). Berechne beide Anstiege und begründe das Ergebnis mit der Formel.',
     r'<p>(1) \(\Delta h = \gamma \cdot h_0 \cdot \Delta T\) \(= 0.21 \cdot 10^{-3}\;\tfrac{1}{\text{K}} \cdot 1500\;\text{m} \cdot 0.6\;\text{K}\) \(\approx 0.189\;\text{m}\). (2) \(\Delta h = 0.21 \cdot 10^{-3}\;\tfrac{1}{\text{K}} \cdot 500\;\text{m} \cdot 1.8\;\text{K}\) \(\approx 0.189\;\text{m}\).</p><p>Gleich viel, rund \(19\;\text{cm}\): Es zählt nur das Produkt \(h_0 \cdot \Delta T\), in beiden Fällen \(900\;\text{m} \cdot \text{K}\) — dreimal so dick, dafür ein Drittel der Erwärmung.</p>', ''),
    ('3c', 3, r'Das Diagramm zeigt die Dichte von Wasser zwischen \(0\;^\circ\text{C}\) und \(10\;^\circ\text{C}\). Lies ab, bei welcher Temperatur die Dichte am grössten ist und welche andere Temperatur dieselbe Dichte hat wie Wasser von \(0\;^\circ\text{C}\). Begründe, warum Wasser von \(2\;^\circ\text{C}\) in einem See über dem Wasser von \(4\;^\circ\text{C}\) liegt.',
     r'<p>Am grössten bei \(4\;^\circ\text{C}\) (knapp \(1000\;\text{kg/m}^3\)). Dieselbe Dichte wie bei \(0\;^\circ\text{C}\) (rund \(999.84\;\text{kg/m}^3\)) hat Wasser bei rund \(8\;^\circ\text{C}\).</p><p>Wasser von \(2\;^\circ\text{C}\) ist weniger dicht als Wasser von \(4\;^\circ\text{C}\) und schwimmt darum darüber; am Grund sammelt sich das dichteste Wasser.</p>',
     '\n            <div class="mini-reihe">' + linien_bild(P3C, 0, 10, 999.65, 1000.0, 1, 0.05, 'Dichte von Wasser über der Temperatur: steigt von 999.84 kg/m³ bei 0 °C auf knapp 1000 kg/m³ bei 4 °C und fällt bis 10 °C auf 999.70 kg/m³', 'ϑ [°C]', 'ρ [kg/m³]', '', xs=2, ys=2) + '</div>'),
    ('3d', 3, r'In einem Boiler hat das Wasser unten \(20\;^\circ\text{C}\) (\(998\;\text{kg/m}^3\)) und oben \(60\;^\circ\text{C}\). Berechne die Dichte bei \(60\;^\circ\text{C}\) mit \(\gamma = 0.21 \cdot 10^{-3}\;\tfrac{1}{\text{K}}\). Gemessen sind \(983\;\text{kg/m}^3\). Begründe, warum die Rechnung abweicht.',
     r'<p>\(\rho = \dfrac{\rho_0}{1 + \gamma \cdot \Delta T}\) \(= \dfrac{998\;\text{kg/m}^3}{1 + 0.21 \cdot 10^{-3}\;\tfrac{1}{\text{K}} \cdot 40\;\text{K}}\) \(\approx 990\;\text{kg/m}^3\).</p><p>\(0.21 \cdot 10^{-3}\;\tfrac{1}{\text{K}}\) gilt nur um \(20\;^\circ\text{C}\). Bei Wasser wächst \(\gamma\) mit der Temperatur stark (unter \(4\;^\circ\text{C}\) ist es wegen der Anomalie sogar negativ); mit konstantem \(\gamma\) unterschätzt man die Ausdehnung bei \(60\;^\circ\text{C}\). Das warme Wasser ist trotzdem weniger dicht und liegt oben.</p>', ''),
])
k3 = kapitel(3, 'wasser', 'Wasser: Dichte, Anomalie und Meeresspiegel', 'K1', 45,
    r'Du berechnest, wie stark der Meeresspiegel steigt, wenn sich das Meerwasser erwärmt (\(\Delta h = \gamma \cdot h_0 \cdot \Delta T\)), erklärst, warum die Dichte beim Erwärmen sinkt, und ordnest die Anomalie des Wassers ein.',
    ('p5-3-lp-meer', 'Ausdehnung sehen: Wasser und Meeresspiegel'),
    sim3, ('p5-3-lp-kontrolle-meer', 'Kontrollfragen zu Wasser und Meeresspiegel'),
    fest3, [uebung('dichte', 'Dichte nach dem Erwärmen'), uebung('meer', 'Anstieg des Meeresspiegels'), uebung('erwaermung', 'Welche Erwärmung?')],
    auf3, f'<a href="{TS}#meeresspiegel">Themenseite 5.3, Meeresspiegelanstieg</a> · <a href="{TS}#anomalie">Die Anomalie des Wassers</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Gas in einem Zylinder mit Kolben, Thermometer und Manometer: Es geht vom Zustand 1 in den eingestellten Zustand 2 über; darunter der Weg im Druck-Volumen-Diagramm', '-4 -4 308 346',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 'V', '<i>V</i><sub>2</sub> Volumen', 0.5, 4, 0.1, 1.6, 'l', 1) + '\n          '
    + regler('s4', 't', '<i>ϑ</i><sub>2</sub> Temperatur', -50, 150, 5, 50, '°C', 0) + '\n        </div>', hilfs='Isothermen')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ideales Gas: allgemeine Gasgleichung</div>
          <p>Der Zustand einer festen Gasmenge ist durch drei Grössen bestimmt: Druck \(p\), Volumen \(V\) und Temperatur \(T\). Im Modell des idealen Gases sind die Teilchen punktförmig, ziehen sich nicht an und stossen elastisch; der Druck entsteht durch ihre Stösse auf die Wand.</p>
          <p>\[ \frac{p_1 \cdot V_1}{T_1} = \frac{p_2 \cdot V_2}{T_2} \]</p>
          <p>Gilt, solange die <b>Gasmenge gleich</b> bleibt (nichts strömt hinein oder hinaus), für Gase weit weg vom Flüssigwerden und bei nicht zu hohem Druck. Zwei Regeln: <b>Temperatur in Kelvin</b>, \(T\;[\text{K}] = \vartheta\;[^\circ\text{C}] + 273.15\). <b>Druck absolut</b>: Ein Manometer zeigt meist den Überdruck, \(p = p_\text{ü} + p_\text{L}\) mit dem Luftdruck \(p_\text{L} \approx 1.0\;\text{bar}\). Druck und Volumen dürfen in beliebigen Einheiten stehen, aber auf beiden Seiten in denselben.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>In Grad Celsius gerechnet: Von \(10\;^\circ\text{C}\) auf \(20\;^\circ\text{C}\) verdoppelt sich die Temperatur nicht — sie steigt von \(283\;\text{K}\) auf \(293\;\text{K}\), um \(3.5\;\%\).</p>
          <p>Den Überdruck vom Manometer direkt eingesetzt: Ein Reifen mit \(2\;\text{bar}\) Überdruck hat \(3\;\text{bar}\) absolut.</p>
        </div>
      </div>'''
P4C = [(v / 20, 3 / (v / 20)) for v in range(15, 85)]
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Erkläre mit dem Teilchenmodell, warum der Druck in einer verschlossenen Flasche steigt, wenn man sie erwärmt, und warum er steigt, wenn man ein Gas zusammendrückt. Warum gehört die Temperatur in Kelvin in die Gasgleichung?',
     r'<p>Wärmer heisst schnellere Teilchen: Sie stossen öfter und heftiger gegen die Wand, der Druck steigt. Beim Zusammendrücken bleiben die Teilchen gleich schnell, haben aber weniger Platz und treffen öfter auf die Wand — auch das gibt mehr Druck.</p><p>Die Kelvin-Skala beginnt beim absoluten Nullpunkt, wo die Teilchenbewegung aufhört. Nur von dort aus gemessen sagt ein Verhältnis wie \(\dfrac{T_2}{T_1}\) etwas über die Bewegung der Teilchen; in Grad Celsius wäre \(20\;^\circ\text{C}\) «doppelt so warm» wie \(10\;^\circ\text{C}\).</p>', ''),
    ('4b', 3, r'In einem Kompressor werden \(3.0\;\text{l}\) Luft (\(1.0\;\text{bar}\), \(20\;^\circ\text{C}\)) auf \(0.50\;\text{l}\) zusammengedrückt; dabei erwärmt sich die Luft auf \(140\;^\circ\text{C}\). Wie gross ist der Druck jetzt? Wie gross wäre er ohne Erwärmung?',
     r'<p>\(T_1 = 293.15\;\text{K}\), \(T_2 = 413.15\;\text{K}\).</p><p>\(p_2 = \dfrac{p_1 \cdot V_1 \cdot T_2}{T_1 \cdot V_2}\) \(= \dfrac{1.0\;\text{bar} \cdot 3.0\;\text{l} \cdot 413.15\;\text{K}}{293.15\;\text{K} \cdot 0.50\;\text{l}}\) \(\approx 8.5\;\text{bar}\).</p><p>Ohne Erwärmung (\(T_2 = T_1\)): \(p_2 = \dfrac{1.0\;\text{bar} \cdot 3.0\;\text{l}}{0.50\;\text{l}} = 6.0\;\text{bar}\) — die Erwärmung bringt rund \(2.5\;\text{bar}\) dazu.</p>', ''),
    ('4c', 3, r'Das Diagramm zeigt zwei Zustände 1 und 2 derselben Gasmenge, dazu gestrichelt alle Zustände mit derselben Temperatur wie Zustand 1 (\(T_1 = 300\;\text{K}\)). Lies \(p\) und \(V\) ab und berechne \(T_2\). Begründe am Diagramm, ob das Gas in Zustand 2 wärmer oder kälter ist als in Zustand 1.',
     r'<p>Zustand 1: \(2\;\text{l}\), \(1.5\;\text{bar}\); Zustand 2: \(1\;\text{l}\), \(4\;\text{bar}\).</p><p>\(T_2 = \dfrac{p_2 \cdot V_2 \cdot T_1}{p_1 \cdot V_1}\) \(= \dfrac{4\;\text{bar} \cdot 1\;\text{l} \cdot 300\;\text{K}}{1.5\;\text{bar} \cdot 2\;\text{l}}\) \(= 400\;\text{K}\).</p><p>Wärmer: Zustand 2 liegt über der gestrichelten Kurve — bei \(1\;\text{l}\) hätte das Gas mit \(300\;\text{K}\) nur \(3\;\text{bar}\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild(P4C, 0, 4.5, 0, 6, 0.5, 1, 'Druck über dem Volumen: gestrichelte Kurve gleicher Temperatur durch Zustand 1 bei 2 l und 1.5 bar; Zustand 2 bei 1 l und 4 bar liegt darüber', 'V [l]', 'p [bar]', 'kurve-hilf', marken=[(2, 1.5, '1', 0, -8), (1, 4, '2', 9, -6)], xs=2) + '</div>'),
    ('4d', 3, r'Entscheide und begründe, ob die Gasgleichung hier brauchbare Ergebnisse liefert: (a) Die Luft in einem Fussball wird in der Sonne wärmer. (b) Ein Feuerzeug, in dem das Butan zum grössten Teil flüssig ist, wird erwärmt. (c) Mit einer Velopumpe wird Luft in einen Reifen gepumpt; man vergleicht die Luft im Reifen vorher und nachher.',
     r'<p>(a) Ja: Luft bei Zimmertemperatur und mässigem Druck verhält sich fast wie ein ideales Gas, und die Gasmenge im Ball bleibt gleich.</p><p>(b) Nein: Ein grossteils flüssiges Gas ist kein ideales Gas; beim Erwärmen verdampft Flüssigkeit, die Gasmenge ändert sich.</p><p>(c) Nein: Beim Pumpen kommt Luft dazu — die Gasmenge im Reifen bleibt nicht gleich.</p>', ''),
])
k4 = kapitel(4, 'gasgleichung', 'Ideales Gas: die allgemeine Gasgleichung', 'K2', 45,
    r'Du beschreibst den Zustand einer festen Gasmenge mit Druck, Volumen und Temperatur, setzt den absoluten Druck und die Temperatur in Kelvin ein und berechnest mit \(\dfrac{p_1 \cdot V_1}{T_1} = \dfrac{p_2 \cdot V_2}{T_2}\) die fehlende Grösse.',
    ('p5-3-lp-gas', 'Ausdehnung sehen: ein Gas, drei Grössen'),
    sim4, ('p5-3-lp-kontrolle-gas', 'Kontrollfragen zur Gasgleichung'),
    fest4, [uebung('gas-p', 'Druck nach der Zustandsänderung'), uebung('gas-v', 'Volumen der Luftblase'), uebung('reifen', 'Was zeigt das Manometer?')],
    auf4, f'<a href="{TS}#gasgesetz">Themenseite 5.3, Das ideale Gasgesetz im Kolben</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur_anim('sim5', 'Dieselbe Gasmenge wahlweise bei konstanter Temperatur, konstantem Druck oder konstantem Volumen; darunter das passende Diagramm', '-4 -4 308 346',
    '        <div class="reglerfeld" data-fall="T">\n          '
    + regler('s5', 'V', '<i>V</i><sub>2</sub> Volumen', 0.5, 6, 0.1, 2.4, 'l', 1) + '\n        </div>\n'
    '        <div class="reglerfeld" data-fall="pV" hidden>\n          '
    + regler('s5', 't', '<i>ϑ</i><sub>2</sub> Temperatur', -150, 330, 5, 60, '°C', 0) + '\n        </div>',
    knoepfe('fall', 'Konstant', [('T', 'isotherm: T'), ('p', 'isobar: p'), ('V', 'isochor: V')], 'T'), hilfs='Verlängerung bis 0 K')
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Spezialfälle der Gasgleichung</div>
          <div class="tabhuelle"><table class="gesetze">
            <tr><th>konstant</th><th>Fall</th><th>Gesetz</th><th>Diagramm</th></tr>
            <tr><td>\(T\)</td><td class="wort">isotherm (Boyle-Mariotte)</td><td>\(p_1 \cdot V_1 = p_2 \cdot V_2\)</td><td class="wort">\(p\)-\(V\): Hyperbel</td></tr>
            <tr><td>\(p\)</td><td class="wort">isobar (Gay-Lussac)</td><td>\(\dfrac{V_1}{T_1} = \dfrac{V_2}{T_2}\)</td><td class="wort">\(V\)-\(T\): Gerade durch den Ursprung</td></tr>
            <tr><td>\(V\)</td><td class="wort">isochor (Amontons)</td><td>\(\dfrac{p_1}{T_1} = \dfrac{p_2}{T_2}\)</td><td class="wort">\(p\)-\(T\): Gerade durch den Ursprung</td></tr>
          </table></div>
          <p>Jedes Gesetz ist die allgemeine Gasgleichung, aus der die konstante Grösse herausgekürzt ist — eine Abkürzung, die nur gilt, wenn diese Grösse wirklich gleich bleibt: langsam drücken (isotherm), ein frei beweglicher Kolben unter gleicher Last (isobar; ein Ballon nur ungefähr), ein starrer Behälter (isochor). Die Geraden gehen nur in Kelvin durch den Ursprung; ihre Verlängerung zeigt auf den absoluten Nullpunkt. Im Zweifel: die allgemeine Gasgleichung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Isotherm mit «doppeltes Volumen, doppelter Druck» verwechselt: \(p\) und \(V\) sind umgekehrt proportional.</p>
          <p>Bei \(0\;^\circ\text{C}\) ist das Volumen eines Gases nicht null: Proportional sind \(V\) und \(T\) nur in Kelvin.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Warum muss man eine zugehaltene Velopumpe langsam zusammendrücken, damit \(p_1 \cdot V_1 = p_2 \cdot V_2\) gilt? Und warum hält ein Latexballon den Druck nur ungefähr konstant?',
     r'<p>Beim schnellen Zusammendrücken erwärmt sich die Luft; die Temperatur bleibt nicht gleich, und der Druck steigt stärker als nach Boyle-Mariotte. Langsam gibt die Luft die Wärme an die Umgebung ab und bleibt bei Zimmertemperatur.</p><p>Die Hülle gibt nach und hält den Innendruck nahe beim Aussendruck. Ihre Spannung drückt aber etwas mit, und die hängt davon ab, wie stark der Ballon gedehnt ist — der Druck bleibt nicht genau gleich.</p>', ''),
    ('5b', 3, r'Eine oben geschlossene, zylindrische Taucherglocke (Höhe \(2.0\;\text{m}\)) enthält \(4.0\;\text{m}^3\) Luft bei \(1.0\;\text{bar}\). Sie wird abgesenkt, bis die Luft darin unter \(1.6\;\text{bar}\) (absolut) steht; die Temperatur bleibt gleich. Wie viel Luftvolumen bleibt? Wie hoch steht das Wasser in der Glocke?',
     r'<p>Isotherm: \(V_2 = \dfrac{p_1 \cdot V_1}{p_2}\) \(= \dfrac{1.0\;\text{bar} \cdot 4.0\;\text{m}^3}{1.6\;\text{bar}}\) \(= 2.5\;\text{m}^3\).</p><p>Das Wasser füllt \(4.0\;\text{m}^3 - 2.5\;\text{m}^3 = 1.5\;\text{m}^3\), also \(\dfrac{1.5\;\text{m}^3}{4.0\;\text{m}^3} = 37.5\;\%\) der Höhe: \(0.375 \cdot 2.0\;\text{m} = 0.75\;\text{m}\).</p>', ''),
    ('5c', 3, r'Das Diagramm zeigt den Druck einer Gasmenge in einem starren Behälter über der Temperatur in Kelvin. Lies die beiden markierten Punkte ab, prüfe, ob \(\dfrac{p}{T}\) gleich bleibt, und bestimme den Druck bei \(100\;^\circ\text{C}\). Wohin zeigt die Verlängerung der Geraden?',
     r'<p>\((250\;\text{K};\;1.0\;\text{bar})\) und \((375\;\text{K};\;1.5\;\text{bar})\): \(\dfrac{1.0\;\text{bar}}{250\;\text{K}} = \dfrac{1.5\;\text{bar}}{375\;\text{K}} = 0.004\;\tfrac{\text{bar}}{\text{K}}\) — gleich, isochor.</p><p>Bei \(100\;^\circ\text{C}\) ist \(T = 373.15\;\text{K}\): \(p = 0.004\;\tfrac{\text{bar}}{\text{K}} \cdot 373.15\;\text{K}\) \(\approx 1.49\;\text{bar}\). Die Gerade zeigt auf den Ursprung, \(T = 0\;\text{K}\): den absoluten Nullpunkt.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(200, 0.8), (500, 2.0)], 0, 500, 0, 2, 125, 0.5, 'Druck über der Temperatur in Kelvin: Gerade durch die Punkte 250 K, 1.0 bar und 375 K, 1.5 bar', 'T [K]', 'p [bar]', 'kurve-p', marken=[(250, 1.0, '', 0, 0), (375, 1.5, '', 0, 0)]) + '</div>'),
    ('5d', 3, r'Ein Gas (\(4.0\;\text{l}\), \(1.0\;\text{bar}\), \(20\;^\circ\text{C}\)) wird zuerst isotherm auf \(2.0\;\text{l}\) zusammengedrückt und dann im festen Volumen auf \(80\;^\circ\text{C}\) erwärmt. Berechne den Druck nach jedem Schritt und prüfe das Ergebnis mit der allgemeinen Gasgleichung.',
     r'<p>Schritt 1, isotherm, bis zum Zwischendruck \(p_\text{Z}\): \(p_\text{Z} = \dfrac{p_1 \cdot V_1}{V_2} = \dfrac{1.0\;\text{bar} \cdot 4.0\;\text{l}}{2.0\;\text{l}} = 2.0\;\text{bar}\).</p><p>Schritt 2, isochor: \(p_2 = p_\text{Z} \cdot \dfrac{T_2}{T_1} = 2.0\;\text{bar} \cdot \dfrac{353.15\;\text{K}}{293.15\;\text{K}}\) \(\approx 2.41\;\text{bar}\).</p><p>Probe: \(p_2 = \dfrac{p_1 \cdot V_1 \cdot T_2}{T_1 \cdot V_2}\) \(= \dfrac{1.0\;\text{bar} \cdot 4.0\;\text{l} \cdot 353.15\;\text{K}}{293.15\;\text{K} \cdot 2.0\;\text{l}}\) \(\approx 2.41\;\text{bar}\) — dasselbe: Die allgemeine Gasgleichung fasst die beiden Schritte zusammen.</p>', ''),
])
k5 = kapitel(5, 'spezialfaelle', 'Isotherm, isobar, isochor', 'K2', 45,
    r'Du erkennst, welche Grösse bei einer Zustandsänderung konstant bleibt, kürzt die allgemeine Gasgleichung zum Gesetz von Boyle-Mariotte, Gay-Lussac oder Amontons und liest die Zusammenhänge in den Diagrammen ab.',
    ('p5-3-lp-spezialfaelle', 'Ausdehnung sehen: eine Grösse hält still'),
    sim5, ('p5-3-lp-kontrolle-spezialfaelle', 'Kontrollfragen zu den Spezialfällen'),
    fest5, [uebung('isotherm', 'Isotherm: Druck oder Volumen'), uebung('isobar', 'Isobar: Volumen'), uebung('fall', 'Welcher Fall — und wie viel?')],
    auf5, f'<a href="{TS}#diagramme">Themenseite 5.3, Die beiden Spezialfälle grafisch</a> · <a href="{TS}#gasgesetz">Das ideale Gasgesetz</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/ausdehnung/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">5.3 · K1 und K2</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg. Erlaubt sind Taschenrechner und Formelsammlung.<br>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a> → K1 · G2 → <a href="#k2">2</a> → K1 · G3 → <a href="#k3">3</a> → K1 · G4 → <a href="#k4">4</a> → K2 · G5 → <a href="#k5">5</a> → K2</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Der Bimetallstreifen im Thermostat → <a href="{TS}#laenge">Themenseite 5.3, Längenausdehnung berechnen</a></li>
        <li>Warum Eis schwimmt und welcher Teil eines Eisbergs unter Wasser liegt → <a href="{TS}#anomalie">Themenseite 5.3, Die Anomalie des Wassers</a></li>
        <li>Normbedingungen und die Masse einer Gasfüllung → <a href="{TS}#clip-p5-3-gas-normbedingungen">Themenseite 5.3, Clips «Normbedingungen» und «Die Masse einer Gasfüllung»</a></li>
        <li>Wie viel Wärme es braucht, um einen Körper zu erwärmen → <a href="../themen/p5-2-waerme.html">Themenseite 5.2 Wärme</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Wärmeausdehnung und Gase, Version 1.0 (07.10.2026), Erprobung: unverlinkt (noindex in
     build-seo.py, UNVERLINKT in build-suchindex.py) bis nach /lp-pruefung.
     Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip mit vorgerechnetem Problem → ② laufende Simulation mit Aufgabenleiste →
     ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/ausdehnung/*.tex).
     Quelle: scripts/lp/ausdehnung/seite.py; Planung und Entscheide: scripts/lp/ausdehnung/README.md.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 5.3 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 den Effekt der Wärmeausdehnung (linear und volumenbezogen) in Abhängigkeit von der Temperatur
          quantifizieren (z. B. den Meeresspiegelanstieg aufgrund der Wassererwärmung berechnen)
       K2 das Modell der idealen Gase anwenden, um Druck-, Temperatur- und Volumenänderungen von Gasen zu
          berechnen, bei gleichbleibender Teilchenmenge

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 linear      → Kap. 1 · Übungen laenge, temperatur, alpha · Aufg. 1a–1d · Kontrollclip laenge · G1
       K1 volumen     → Kap. 2 · Übungen volumen, volumen-fest, fuellen · Aufg. 2a–2d · Kontrollclip volumen · G2
       K1 Meeresspiegel (Beispiel des RLP), Dichte, Anomalie als Einordnung
                      → Kap. 3 · Übungen dichte, meer, erwaermung · Aufg. 3a–3d · Kontrollclip meer · G3
       K2 allgemein   → Kap. 4 · Übungen gas-p, gas-v, reifen · Aufg. 4a–4d · Kontrollclip gas · G4
       K2 Spezialfälle → Kap. 5 · Übungen isotherm, isobar, fall · Aufg. 5a–5d · Kontrollclip spezialfaelle · G5
     Bewusst weggelassen (auf der Themenseite): Bimetall, Eisberg und Schwimmen von Eis, Normbedingungen und
     Masse einer Gasfüllung (die Teilchenmenge bleibt im RLP gleich).
     Zeiten: K0 10 · K1–K5 je 45 · Gesamttest 30 = 265 min ≈ 5.9 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Wärmeausdehnung und Gase</h1>
      <p class="unter">Länge und Volumen fester Körper und Flüssigkeiten, Wasser und der Meeresspiegel, das ideale Gas und seine drei Spezialfälle — mit laufenden Simulationen. Fünf Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 5 · Teilgebiet 5.3</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Längenausdehnung</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Volumenausdehnung</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Wasser und Meeresspiegel</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Allgemeine Gasgleichung</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Isotherm, isobar, isochor</span></a></li></ol>
    <p class="lekt">Abschluss</p>
    <ol><li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li></ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 6 Aufgabenblöcken bearbeitet</p>
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
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 5, Teilgebiet 5.3 Wärmeausdehnung</p>
        <ul>
          <li><b>K1</b> den Effekt der Wärmeausdehnung (linear und volumenbezogen) in Abhängigkeit von der Temperatur quantifizieren (z. B. den Meeresspiegelanstieg aufgrund der Wassererwärmung berechnen)</li>
          <li><b>K2</b> das Modell der idealen Gase anwenden, um Druck-, Temperatur- und Volumenänderungen von Gasen zu berechnen, bei gleichbleibender Teilchenmenge</li>
        </ul>
        <p class="rlp-fuss">Kapitel 1 bis 3 gehören zu K1, Kapitel 4 und 5 zu K2. Die Themenseite <a href="''' + TS + '''">5.3 Wärmeausdehnung</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Wärmeausdehnung und Gase · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Länge') + k1 + band(2, 'Volumen') + k2 + band(3, 'Wasser') + k3
        + band(4, 'Gasgleichung') + k4 + band(5, 'Spezialfälle') + k5 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
