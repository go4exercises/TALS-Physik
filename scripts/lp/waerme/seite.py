"""Baut leitprogramme/leitprogramm-waerme.html aus einer Kapitelbeschreibung (seit 07.10.2026).

  python3 scripts/lp/waerme/seite.py

Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4) für das Teilgebiet 5.2 Wärme,
als Kopie von scripts/lp/hydrostatik/ entstanden: Kopf, CSS-Gerüst, Grundskript und Bausteine von dort,
neu sind sieben Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Planung (Kompetenzmatrix, Planungstabelle, Kern/Vertiefung/weggelassen, Konventionen und Widersprüche
der Themenseite): Kopfkommentar der Seite (Variable «oben» unten) und README.md.
"""
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-waerme.html'
TS = '../themen/p5-2-waerme.html'

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
<title>Leitprogramm Wärme</title>
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
/* Diagramme und Szenen, Farbe = eine Bedeutung: Temperatur eines Körpers Bernstein, Wasser Blau,
   Wärme (übertragen, abgestrahlt, Verlust) Rot, zugeführte Energie und Licht Orange, Nutzen (Strom,
   Nutzwärme) Grün, Körper, Gefässe, Achsen Grau; voriger Lauf grau gestrichelt */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.sim .skala.klein{font-size:8px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.vorher{fill:none;stroke:var(--tinte-2);stroke-width:1.8;stroke-dasharray:5 4;opacity:.6}
.gleich{fill:none;stroke:var(--bernstein);stroke-width:1.3;stroke-dasharray:3 3}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.p-t{fill:var(--bernstein)} text.p-t{fill:var(--bernstein)}
.t-kurve{fill:none;stroke:var(--bernstein);stroke-width:2.6}
.w-kurve{fill:none;stroke:var(--blau);stroke-width:2.6}
.pf-linie{stroke-width:2.6;fill:none}
.pf-linie.pf-q{stroke:var(--rot)} .pf-kopf.pf-q{fill:var(--rot)}
.pf-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:3.5px;paint-order:stroke}
text.pf-q{fill:var(--rot)} text.pf-zu{fill:var(--orange)} text.pf-nutz{fill:var(--gruen)}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bt-meldung{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:10.5px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.bt-wert.t-text{fill:var(--bernstein)} .bt-wert.w-text{fill:var(--blau)}
.bt-wert.l-licht{fill:var(--orange)} .bt-wert.l-ir{fill:var(--rot)}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
svg.mini.breit{width:260px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.k-t{stroke:var(--bernstein)} .kurve-mini.k-t2{stroke:var(--bernstein);stroke-dasharray:7 4} .kurve-mini.k-w{stroke:var(--blau)} .kurve-mini.k-g{stroke:var(--tinte-2);stroke-dasharray:6 4}
.kurve-mini.k-ir{stroke:var(--rot)} .kurve-mini.k-licht{stroke:var(--orange)}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.mini-name.k-t,.mini-name.k-t2{fill:var(--bernstein)} .mini-name.k-w{fill:var(--blau)} .mini-name.k-ir{fill:var(--rot)} .mini-name.k-licht{fill:var(--orange)}
.p-mini{fill:var(--tinte)}
.legende{fill:var(--tinte-2);font-family:var(--sans);font-size:10px;font-weight:700}
.legende.l-t{fill:var(--bernstein)} .legende.l-w{fill:var(--blau)}
/* Körper, Stoffe, Geräte */
.wasser{fill:#5fa9c6;opacity:.35} .wasser.heiss{fill:#c0542f;opacity:.25}
.oel{fill:#e3c75a;opacity:.55}
.koerper{fill:#c9cdd2;stroke:var(--tinte-2);stroke-width:1.4} .koerper.alu{fill:#dde1e5} .koerper.eisen{fill:#9aa1a8}
.gefaess{fill:none;stroke:var(--tinte-2);stroke-width:2;stroke-linejoin:round}
.wasserlinie{stroke:#3a7a96;stroke-width:1.6}
.faden{stroke:var(--tinte);stroke-width:1.2}
.teilchen{fill:var(--tinte)} .tpfeil{stroke:var(--tinte-2);stroke-width:1.3}
.platte{fill:var(--tinte-2)} .platte.an{fill:var(--rot)}
.thermo{fill:var(--karte);stroke:var(--tinte-2);stroke-width:1.2} .thermo-kugel{fill:var(--bernstein)} .thermo-saeule{fill:var(--bernstein)}
.eis{fill:#e8f3fa;stroke:#8fb4cc;stroke-width:1.2} .dampf{fill:none;stroke:var(--tinte-2);stroke-width:1.4;opacity:.7}
.bal-q{fill:var(--rot);opacity:.8} .bal-zu{fill:var(--orange);opacity:.85} .bal-nutz{fill:var(--gruen);opacity:.85} .bal-verl{fill:var(--rot);opacity:.8}
.brennstoff{fill:var(--orange-hell);stroke:var(--orange-rand);stroke-width:1.4}
.kessel{fill:var(--papier-2);stroke:var(--tinte-2);stroke-width:1.6} .kamin{fill:var(--papier-2);stroke:var(--tinte-2);stroke-width:1.4}
.boiler{fill:var(--papier-2);stroke:var(--tinte-2);stroke-width:1.6}
.strom{fill:none;stroke-linecap:butt;opacity:.85} .strom.zu{stroke:var(--orange)} .strom.nutz{stroke:var(--gruen)} .strom.verlust{stroke:var(--rot)}
.fl-zu{fill:var(--orange);opacity:.85} .fl-umg{fill:var(--orange);opacity:.45} .fl-nutz{fill:var(--gruen);opacity:.85} .fl-waerme{fill:var(--gruen);opacity:.5}
.fl-verl{fill:var(--rot);opacity:.75} .fl-rest{fill:var(--tinte-2);opacity:.35}
.band{opacity:.28} .fl-nutz.abruf{opacity:.5}
.bedarf{fill:none;stroke:var(--tinte);stroke-width:1.4;stroke-dasharray:4 3}
.schicht{stroke:none} .schicht.kupfer{fill:#c47a3c;opacity:.75} .schicht.holz{fill:#d8c29a} .schicht.wasser{fill:#5fa9c6;opacity:.35}
.schicht.luft{fill:var(--papier-2)} .schicht.vakuum{fill:var(--karte)}
.platte-heiss{fill:var(--rot);opacity:.85} .platte-kalt{fill:var(--tinte-2);opacity:.6}
.warnzeile{color:var(--rot)}
.platte-heiss.spiegel,.platte-kalt.spiegel{stroke:#c9ced3;stroke-width:3}
.konv{fill:none;stroke:var(--rot);stroke-width:2;stroke-dasharray:5 3}
.welle{fill:none;stroke:var(--rot);stroke-width:2} .welle.duenn{stroke-width:1;opacity:.6}
.atmo{fill:var(--tinte-2)} .boden{fill:#8a6a43;opacity:.75} .sonne{fill:#e8a317}
.licht{fill:var(--orange);opacity:.75} .ir{fill:var(--rot);opacity:.7} .ir.atm{opacity:.5}
.boden-text{fill:var(--karte);stroke:none}
.task-id.vert{font-family:var(--sans);font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--lila);
  border:1px solid var(--lila-rand);border-radius:999px;padding:1px 8px;margin-right:6px;white-space:nowrap}
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
  var KEY = 'leitprogramm-waerme-v1';

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


def teile(html, grenze=28):
    """Lange Inline-Formeln \\(…\\) an Gleichheitszeichen der obersten Ebene in mehrere Formeln teilen,
    damit die Zeile bei 360 px umbrechen kann (HOWTO-leitprogramme §16, render-check)."""
    def zerlege(f):
        if len(re.sub(r'\\[a-z]+|[{}\\]', '', f)) <= grenze:
            return [f]
        teile_, tiefe, start, i = [], 0, 0, 0
        while i < len(f):
            c = f[i]
            if c in '{(': tiefe += 1
            elif c in '})': tiefe -= 1
            elif tiefe == 0 and i > start + 8 and (f.startswith(' = ', i) or f.startswith(' \\approx ', i)):
                teile_.append(f[start:i].strip()); start = i + 1
            i += 1
        teile_.append(f[start:].strip())
        return teile_
    def ersetze(m):
        return ' '.join('\\(' + s + '\\)' for s in zerlege(m.group(1)))
    return re.sub(r'\\\((.+?)\\\)', ersetze, html)


def test(tid, titel, punkte, aufgaben, zwei=False):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        loes = teile(loes)
        lis.append(f'''          <li>
            <div class="a-frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte)
    # Vertiefungsaufgaben sind freiwillig und nicht in der Zeitangabe des Kapitels
    frei = sum(a[1] for a in aufgaben if 'task-id vert' in a[2])
    summe = f'· {punkte - frei} P, dazu {frei} P freiwillig' if frei else f'· {punkte} P'
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">{summe}</span></h3>
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">5.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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




def tief(s):
    """«F_y [N]» für SVG-Text: Index tiefgestellt (wie stext in seite.js)."""
    import re as _re
    return _re.sub(r'_([A-Za-z0-9,]+)(.*)', r'<tspan dy="3" font-size="0.78em">\1</tspan><tspan dy="-3">\2</tspan>', s)





def balken_bild(rows, xmax, xt, label, xname):
    """Waagrechte Balken zum Ablesen (ohne Werte): rows = [(Name, Wert, Klasse)], Gitter je xt."""
    w, ox, oy, h = 260, 86, 10, 22
    k = (w - ox - 14) / xmax
    H = oy + len(rows) * (h + 8) + 4
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {H + 30}" role="img" aria-label="{label}">']
    x = xt
    while x <= xmax + 1e-9:
        t.append(f'<line x1="{ox + x * k:.1f}" y1="{oy - 4}" x2="{ox + x * k:.1f}" y2="{H}" class="gitter"/>')
        t.append(f'<text x="{ox + x * k:.1f}" y="{H + 13}" text-anchor="middle" class="skala">{x:g}</text>')
        x += xt
    t.append(f'<line x1="{ox}" y1="{oy - 4}" x2="{ox}" y2="{H}" class="achse"/><line x1="{ox}" y1="{H}" x2="{w - 6}" y2="{H}" class="achse"/>')
    for i, (name, v, cls) in enumerate(rows):
        y = oy + i * (h + 8)
        t.append(f'<rect x="{ox}" y="{y}" width="{v * k:.1f}" height="{h}" class="{cls}"/>')
        t.append(f'<text x="{ox - 5}" y="{y + 15}" text-anchor="end" class="skala">{name}</text>')
    t.append(f'<text x="{w - 6}" y="{H + 26}" text-anchor="end" class="achsname">{xname}</text></svg>')
    return ''.join(t)


def saison_bild(liefer, bedarf, ymax, yt, label, yname):
    """Sommer- und Winterhalbjahr: Lieferung (grün) neben Bedarf (gestrichelt), ohne Werte."""
    w, h, ox, oy = 260, 150, 40, 126
    k = (oy - 14) / ymax
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 18}" role="img" aria-label="{label}">']
    y = yt
    while y <= ymax + 1e-9:
        t.append(f'<line x1="{ox}" y1="{oy - y * k:.1f}" x2="{w - 8}" y2="{oy - y * k:.1f}" class="gitter"/><text x="{ox - 5}" y="{oy - y * k + 4:.1f}" text-anchor="end" class="skala">{y:g}</text>')
        y += yt
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{w - 8}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="6" class="achse"/>')
    for i, name in enumerate(['Sommerhalbjahr', 'Winterhalbjahr']):
        x = ox + 18 + i * 104
        t.append(f'<rect x="{x}" y="{oy - liefer[i] * k:.1f}" width="34" height="{liefer[i] * k:.1f}" class="fl-nutz"/>')
        t.append(f'<rect x="{x + 38}" y="{oy - bedarf[i] * k:.1f}" width="34" height="{bedarf[i] * k:.1f}" class="bedarf"/>')
        t.append(f'<text x="{x + 36}" y="{oy + 13}" text-anchor="middle" class="skala">{name}</text>')
    t.append(f'<text x="{ox + 6}" y="12" class="achsname">{yname}</text>')
    t.append(f'<text x="{w - 8}" y="{h + 14}" text-anchor="end" class="legende">grün: Lieferung; gestrichelt: Bedarf</text></svg>')
    return ''.join(t)


def spektrum_bild(label):
    """Strahlung der Sonne (5800 K) und der Erde (288 K), je auf gleiche Höhe gebracht, über der
    Wellenlänge (logarithmisch, 0.1 µm bis 100 µm); grau: Bereiche, die Wasserdampf und Kohlendioxid
    stark aufnehmen (vereinfacht)."""
    w, h, ox, oy = 260, 150, 30, 120
    lx = lambda lam: ox + (math.log10(lam) + 1) / 3 * (w - ox - 10)
    def planck(lam, T):
        return lam ** -5 / (math.exp(14388 / (lam * T)) - 1)
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 22}" role="img" aria-label="{label}">']
    for a, b in ((5.5, 7.5), (13.5, 17.0), (20, 100)):
        t.append(f'<rect x="{lx(a):.1f}" y="10" width="{lx(b) - lx(a):.1f}" height="{oy - 10}" class="fl-rest"/>')
    for lam, s in ((0.1, '0.1'), (0.2, ''), (0.5, '0.5'), (1, '1'), (2, ''), (5, '5'), (10, '10'), (20, ''), (50, '50'), (100, '100')):
        t.append(f'<line x1="{lx(lam):.1f}" y1="10" x2="{lx(lam):.1f}" y2="{oy}" class="gitter"/>')
        if s:
            t.append(f'<text x="{lx(lam):.1f}" y="{oy + 13}" text-anchor="middle" class="skala">{s}</text>')
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{w - 6}" y2="{oy}" class="achse"/>')
    for T, cls, name, nx in ((5800, 'k-licht', 'Sonne', 1.0), (288, 'k-ir', 'Erde', 40)):
        lm = 2898 / T
        mx = planck(lm, T)
        pts = []
        for i in range(241):
            lam = 10 ** (-1 + 3 * i / 240)
            y = oy - (oy - 18) * planck(lam, T) / mx
            pts.append(f'{lx(lam):.1f},{y:.1f}')
        t.append('<polyline points="' + ' '.join(pts) + f'" class="kurve-mini {cls}"/>')
        t.append(f'<text x="{lx(nx):.1f}" y="16" text-anchor="middle" class="mini-name {cls}">{name}</text>')
    t.append(f'<text x="{w - 6}" y="{oy + 26}" text-anchor="end" class="achsname">λ [µm], logarithmisch</text></svg>')
    return ''.join(t)


def kurven_bild(kurven, x0, x1, y0, y1, xt, yt, label, xname, yname):
    """Mehrere Streckenzüge: kurven = [(punkte, klasse, name, [x, y] für den Namen)]."""
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
    for pk, ck, name, bei in kurven:
        t.append('<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in pk) + f'" class="kurve-mini {ck}"/>')
        if name:
            t.append(f'<text x="{X(bei[0]):.1f}" y="{Y(bei[1]):.1f}" class="mini-name {ck}">{name}</text>')
    t.append(f'<text x="{X(x1) + 8:.1f}" y="{oy - 6}" text-anchor="end" class="achsname">{tief(xname)}</text><text x="{ox + 6}" y="{Y(y1) - 2:.1f}" class="achsname">{tief(yname)}</text></svg>')
    return ''.join(t)


def mini(svg):
    return '\n            <div class="mini-reihe">' + svg + '</div>'


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P51 = '../themen/p5-1-temperatur.html'
P02 = '../themen/p0-2-vorwissen-physik.html'
P01 = '../themen/p0-1-vorwissen-mathematik.html'
LPE = 'leitprogramm-energie.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 4.3 · 5.1</span><span class="zeit">≈ 15 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Celsius und Kelvin, Energie, Leistung und Wirkungsgrad, Gleichungen umstellen. Wenn das wackelt: <a href="''' + P51 + '''">Themenseite 5.1 Temperatur</a> und das <a href="''' + LPE + '''">Leitprogramm Energie</a>.</p>
''' + test('t0', 'Vortest', 11, [
    ('0a', 2, r'Rechne \(18\;^\circ\text{C}\) in Kelvin um. Ein Tee kühlt von \(85\;^\circ\text{C}\) auf \(60\;^\circ\text{C}\) ab: Wie gross ist die Temperaturänderung in Kelvin?',
     r'<p>\(T\;[\text{K}] = \vartheta\;[^\circ\text{C}] + 273.15\) \(= 18 + 273.15 = 291.15\), also \(291.15\;\text{K}\).</p><p>\(\Delta T = 85\;^\circ\text{C} - 60\;^\circ\text{C} = 25\;\text{K}\): Eine Temperaturdifferenz ist in Kelvin und in Grad Celsius gleich gross.</p><p class="komm">Falsch? <a href="' + P51 + r'#umrechnen">Themenseite 5.1: Umrechnen und Temperaturdifferenz</a></p>', ''),
    ('0b', 3, r'Ein Föhn mit \(1800\;\text{W}\) läuft \(5\;\text{min}\). Wie viel Energie bezieht er, in kJ und in kWh?',
     r'<p>\(E = P \cdot t\) \(= 1800\;\text{W} \cdot 300\;\text{s}\) \(= 540\,000\;\text{J} = 540\;\text{kJ}\).</p><p>\(1\;\text{kWh} = 1000\;\text{W} \cdot 3600\;\text{s} = 3.6 \cdot 10^6\;\text{J}\), also \(\dfrac{540\,000\;\text{J}}{3.6 \cdot 10^6\;\text{J/kWh}} = 0.15\;\text{kWh}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#energie">Vorwissen 0.2: Arbeit, Energie und Leistung</a> · <a href="' + LPE + r'#k5">Leitprogramm Energie, Kapitel 5</a></p>', ''),
    ('0c', 2, r'Ein Motor bekommt \(50\;\text{kJ}\) und gibt \(18\;\text{kJ}\) als Bewegungsenergie ab. Wie gross ist sein Wirkungsgrad, und wo bleibt der Rest?',
     r'<p>\(\eta = \dfrac{E_\text{nutz}}{E_\text{zu}}\) \(= \dfrac{18\;\text{kJ}}{50\;\text{kJ}} = 0.36\).</p><p>Die übrigen \(32\;\text{kJ}\) sind nicht verschwunden: Sie gehen als Wärme an Motor, Abgas und Umgebung.</p><p class="komm">Falsch? <a href="' + LPE + r'#k5">Leitprogramm Energie, Kapitel 5: Leistung und Wirkungsgrad</a></p>', ''),
    ('0d', 2, r'Stelle \(Q = m \cdot c \cdot \Delta T\) nach \(m\) um und \(E = P \cdot t\) nach \(t\).',
     r'<p>\(m = \dfrac{Q}{c \cdot \Delta T}\) und \(t = \dfrac{E}{P}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1: Gleichungen umstellen</a></p>', ''),
    ('0e', 2, r'Ein Körper ist \(27\;^\circ\text{C}\) warm. Wie viel Wärmestrahlung gibt er je Quadratmeter ab? Rechne mit \(\dfrac{P}{A} = \sigma \cdot T^4\) und \(\sigma = 5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4)\).',
     r'<p>\(T = 27 + 273.15 = 300.15\;\text{K}\) (Temperatur in Kelvin!).</p><p>\(\dfrac{P}{A} = \sigma \cdot T^4\) \(= 5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4) \cdot (300.15\;\text{K})^4\) \(\approx 460\;\text{W/m}^2\).</p><p class="komm">Falsch? <a href="' + LPE + r'#k6">Leitprogramm Energie, Kapitel 6: Die Energiebilanz der Erde</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 8 von 11 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Ein Körper auf einer Heizplatte bekommt Wärme; die Pfeile an den Teilchen wachsen; darunter die Temperatur über der zugeführten Wärme', '-4 -4 308 340',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'm', '<i>m</i> Masse', 0.2, 2.0, 0.05, 1.0, 'kg', 2) + '\n          '
    + regler('s1', 'Q', '<i>Q</i> Wärme', 0, 50, 0.5, 10, 'kJ', 1) + '\n        </div>',
    knoepfe('stoff', 'Stoff', [('wasser', 'Wasser'), ('oel', 'Speiseöl'), ('alu', 'Aluminium'), ('eisen', 'Eisen')], 'wasser'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wärme und Temperatur</div>
          <p>Die <b>Temperatur</b> misst die mittlere Bewegung der Teilchen eines Körpers — ein <b>Zustand</b> (\(\vartheta\) in °C, \(T\) in K).</p>
          <p>Die <b>Wärme</b> \(Q\) ist Energie, die <b>wegen eines Temperaturunterschieds</b> von einem Körper auf einen anderen übertragen wird: An der Berührfläche stossen die schnelleren Teilchen die langsameren an und geben ihnen Bewegungsenergie ab. Wärme ist ein <b>Vorgang</b>, gemessen in Joule. Ein Körper «enthält» keine Wärme, sondern innere Energie.</p>
          <p>Von selbst fliesst Wärme nur vom wärmeren zum kälteren Körper. Vorzeichen: \(Q \gt 0\) heisst aufgenommen, \(Q \lt 0\) abgegeben.</p>
          <p>Ohne Phasenwechsel gilt für die Wärmemenge:</p>
          <p>\[ Q = m \cdot c \cdot \Delta T \]</p>
          <p>\(c\): spezifische Wärmekapazität, die Wärme für \(1\;\text{kg}\) und \(1\;\text{K}\), in \(\text{J/(kg·K)}\). \(\Delta T\) in K ist gleich gross wie die Differenz in °C. Wasser \(4182\), Ethanol \(2430\), Speiseöl \(\approx 2000\), Aluminium \(896\), Sand \(835\), Eisen \(450\;\text{J/(kg·K)}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Ein heisser Körper enthält viel Wärme.» Ein Glas Wasser von \(70\;^\circ\text{C}\) ist heisser als ein Schwimmbecken, gibt beim Abkühlen auf \(20\;^\circ\text{C}\) aber nur rund \(42\;\text{kJ}\) ab (\(0.2\;\text{kg}\)) — das Becken schon bei \(1\;\text{K}\) Abkühlung Gigajoule.</p>
          <p>Die Endtemperatur statt der Temperaturänderung eingesetzt: In \(Q = m \cdot c \cdot \Delta T\) steht immer die Differenz.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Ein Fingerhut mit \(3\;\text{g}\) Wasser von \(90\;^\circ\text{C}\) und ein Eimer mit \(8\;\text{kg}\) Wasser von \(40\;^\circ\text{C}\): Welcher hat die höhere Temperatur? Mit welchem kannst du mehr Eis schmelzen? Begründe mit Wärme und Temperatur.',
     r'<p>Die höhere Temperatur hat der Fingerhut: Seine Teilchen bewegen sich im Mittel schneller.</p><p>Mehr Eis schmilzt der Eimer. Beim Abkühlen auf \(0\;^\circ\text{C}\) gibt er \(Q = m \cdot c \cdot \Delta T\) \(= 8\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 40\;\text{K}\) \(\approx 1.34\;\text{MJ}\) ab, der Fingerhut nur \(0.003\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 90\;\text{K}\) \(\approx 1.13\;\text{kJ}\) — über tausendmal weniger.</p><p>Wie viel Wärme ein Körper abgeben kann, hängt von Masse, Stoff und Temperaturänderung ab, nicht von der Temperatur allein.</p>', ''),
    ('1b', 3, r'Ein Kuchenblech aus Aluminium (\(0.60\;\text{kg}\)) wird im Ofen von \(20\;^\circ\text{C}\) auf \(180\;^\circ\text{C}\) erhitzt. Wie viel Wärme nimmt es auf, in kJ und in kWh?',
     r'<p>\(Q = m \cdot c \cdot \Delta T\) \(= 0.60\;\text{kg} \cdot 896\;\text{J/(kg·K)} \cdot 160\;\text{K}\) \(= 86\,016\;\text{J} \approx 86.0\;\text{kJ}\).</p><p>\(\dfrac{86\,016\;\text{J}}{3.6 \cdot 10^6\;\text{J/kWh}} \approx 0.0239\;\text{kWh}\).</p>', ''),
    ('1c', 3, r'Das Diagramm zeigt, wie die Temperatur zweier Körper mit der zugeführten Wärme steigt: A hat \(0.40\;\text{kg}\), B hat \(0.45\;\text{kg}\). Lies je einen Punkt ab, bestimme die spezifische Wärmekapazität beider Körper und suche den Stoff in der Tabelle. Welcher erwärmt sich bei gleicher Wärme stärker?',
     r'<p>Aus \(Q = m \cdot c \cdot \Delta T\) folgt \(c = \dfrac{Q}{m \cdot \Delta T}\).</p><p>A: \(9\;\text{kJ}\) geben \(50\;\text{K}\): \(c = \dfrac{9000\;\text{J}}{0.40\;\text{kg} \cdot 50\;\text{K}}\) \(= 450\;\text{J/(kg·K)}\) — Eisen.</p><p>B: \(18\;\text{kJ}\) geben \(20\;\text{K}\): \(c = \dfrac{18\,000\;\text{J}}{0.45\;\text{kg} \cdot 20\;\text{K}}\) \(= 2000\;\text{J/(kg·K)}\) — Speiseöl.</p><p>A steigt steiler: Bei gleicher Wärme wird das Eisen viel wärmer (kleines \(m \cdot c\)).</p>',
     mini(kurven_bild([([(0, 0), (18, 100)], 'k-t', 'A', [13.2, 86]), ([(0, 0), (18, 20)], 'k-t2', 'B', [15.5, 27])], 0, 18, 0, 100, 3, 10,
                      'Temperaturänderung über der zugeführten Wärme: Gerade A durch 9 kJ und 50 K, Gerade B (gestrichelt) durch 18 kJ und 20 K', 'Q [kJ]', 'ΔT [K]'))),
    ('1d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Warum fliesst in Heizungsrohren Wasser und nicht Luft? Rechne: Wie viel Wärme gibt \(1\;\text{l}\) Wasser ab, wenn es von \(55\;^\circ\text{C}\) auf \(35\;^\circ\text{C}\) abkühlt, und wie viel \(1\;\text{l}\) Luft (\(\rho = 1.2\;\text{kg/m}^3\), \(c \approx 1000\;\text{J/(kg·K)}\))?',
     r'<p>Wasser: \(m = 1\;\text{kg}\), \(Q = m \cdot c \cdot \Delta T\) \(= 1\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 20\;\text{K}\) \(\approx 83.6\;\text{kJ}\).</p><p>Luft: \(m = \rho \cdot V = 1.2\;\text{kg/m}^3 \cdot 0.001\;\text{m}^3 = 0.0012\;\text{kg}\), \(Q = 0.0012\;\text{kg} \cdot 1000\;\text{J/(kg·K)} \cdot 20\;\text{K}\) \(= 24\;\text{J}\).</p><p>Derselbe Liter Wasser trägt rund \(3500\)-mal so viel Wärme: grosse Masse je Volumen und grosses \(c\). Für Luft bräuchte es riesige Kanäle.</p>', ''),
])
k1 = kapitel(1, 'waerme-temperatur', 'Wärme und Temperatur', 'K1 · K2', 55,
    r'Du erklärst Wärme als Energie, die wegen eines Temperaturunterschieds durch Teilchenstösse übertragen wird, unterscheidest sie von der Temperatur und berechnest die Wärmemenge \(Q = m \cdot c \cdot \Delta T\).',
    ('p5-2-lp-waerme', 'Wärme sehen: Energie, die fliesst'),
    sim1, ('p5-2-lp-kontrolle-waerme', 'Kontrollfragen zu Wärme und Temperatur'),
    fest1, [uebung('waermemenge', 'Wärmemenge'), uebung('erwaermung', 'Wie warm wird es?'), uebung('c-messen', 'Den Stoff an c erkennen')],
    auf1, f'<a href="{TS}#definition">Themenseite 5.2, Grundbegriffe</a> · <a href="{TS}#waermemenge">Wie viel Wärme braucht das Erwärmen?</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur_anim('sim2', 'Ein heisser Körper wird in kaltes Wasser getaucht; Balken für abgegebene und aufgenommene Wärme; darunter beide Temperaturen über der Zeit', '-4 -4 308 334',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'mk', '<i>m</i><sub>K</sub> Körper', 0.1, 1.0, 0.05, 0.3, 'kg', 2) + '\n          '
    + regler('s2', 'tk', '<i>ϑ</i><sub>K</sub> Körper', 40, 300, 5, 150, '°C', 0) + '\n          '
    + regler('s2', 'mw', '<i>m</i><sub>W</sub> Wasser', 0.1, 1.0, 0.05, 0.4, 'kg', 2) + '\n        </div>',
    knoepfe('k', 'Körper', [('alu', 'Aluminium'), ('eisen', 'Eisen'), ('wasser', 'heisses Wasser')], 'alu'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wärmebilanz und thermisches Gleichgewicht</div>
          <p>Berühren sich zwei Körper verschiedener Temperatur, fliesst Wärme vom wärmeren zum kälteren, bis beide <b>dieselbe Temperatur</b> haben: das <b>thermische Gleichgewicht</b> bei der Mischtemperatur \(\vartheta_\text{m}\).</p>
          <p>In einem <b>abgeschlossenen System</b> (Gefäss und Umgebung nehmen nichts auf) geht keine Energie verloren — die <b>Wärmebilanz</b>:</p>
          <p>\[ \sum Q_i = 0 \quad\Longleftrightarrow\quad Q_\text{ab} = Q_\text{auf} \]</p>
          <p>Mit Beträgen: \(Q_\text{ab} = m_1 \cdot c_1 \cdot (\vartheta_1 - \vartheta_\text{m})\), \(Q_\text{auf} = m_2 \cdot c_2 \cdot (\vartheta_\text{m} - \vartheta_2)\). Ist eine Masse oder eine Anfangstemperatur gesucht, die Bilanz nach ihr auflösen.</p>
          <p><b>Abkürzung</b> für zwei Körper ohne Phasenwechsel (aus der Bilanz aufgelöst; bei gleichem Stoff kürzt sich \(c\)):</p>
          <p>\[ \vartheta_\text{m} = \frac{m_1 c_1 \vartheta_1 + m_2 c_2 \vartheta_2}{m_1 c_1 + m_2 c_2} \]</p>
          <p>Die Mischtemperatur liegt immer zwischen den Anfangstemperaturen, näher bei dem Körper mit dem grösseren \(m \cdot c\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den einfachen Mittelwert genommen: \(0.10\;\text{kg}\) Wasser von \(90\;^\circ\text{C}\) und \(0.40\;\text{kg}\) von \(10\;^\circ\text{C}\) ergeben \(26\;^\circ\text{C}\), nicht \(50\;^\circ\text{C}\).</p>
          <p>\(c\) gekürzt, obwohl die Stoffe verschieden sind: Bei Metall und Wasser bleibt \(c\) stehen.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'In der Badewanne sind \(80\;\text{l}\) Wasser von \(12\;^\circ\text{C}\). Wie viel Wasser von \(55\;^\circ\text{C}\) musst du dazugiessen, damit das Bad \(38\;^\circ\text{C}\) hat? Verluste vernachlässigt, \(1\;\text{l}\) Wasser \(\approx 1\;\text{kg}\).',
     r'<p>\(Q_\text{ab} = Q_\text{auf}\): \(m_h \cdot c \cdot (55\;^\circ\text{C} - 38\;^\circ\text{C}) = 80\;\text{kg} \cdot c \cdot (38\;^\circ\text{C} - 12\;^\circ\text{C})\). Gleicher Stoff, \(c\) kürzt sich.</p><p>\(m_h = 80\;\text{kg} \cdot \dfrac{26\;\text{K}}{17\;\text{K}}\) \(\approx 122\;\text{kg}\), also rund \(122\;\text{l}\) heisses Wasser.</p>', ''),
    ('2b', 3, r'Ein unbekanntes Metallstück (\(0.35\;\text{kg}\), \(98\;^\circ\text{C}\)) kommt in \(0.40\;\text{kg}\) Wasser von \(18\;^\circ\text{C}\). Die Mischtemperatur ist \(30.6\;^\circ\text{C}\). Bestimme die spezifische Wärmekapazität des Metalls. Welches Metall ist es?',
     r'<p>\(Q_\text{auf} = m_W \cdot c_W \cdot (\vartheta_\text{m} - \vartheta_W)\) \(= 0.40\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 12.6\;\text{K}\) \(\approx 21\,077\;\text{J}\).</p><p>\(Q_\text{ab} = Q_\text{auf}\): \(c_K = \dfrac{Q_\text{auf}}{m_K \cdot (\vartheta_K - \vartheta_\text{m})}\) \(= \dfrac{21\,077\;\text{J}}{0.35\;\text{kg} \cdot 67.4\;\text{K}}\) \(\approx 893\;\text{J/(kg·K)}\) — Aluminium (\(896\)).</p>', ''),
    ('2c', 3, r'Das Diagramm zeigt die Temperaturen eines Körpers und von \(0.45\;\text{kg}\) Wasser, nachdem der Körper ins Wasser getaucht wurde. Welche Kurve gehört zum Wasser? Lies die Mischtemperatur ab und berechne, wie viel Wärme das Wasser aufgenommen hat. Warum enden beide Kurven bei derselben Temperatur?',
     r'<p>Die untere Kurve (B) gehört zum Wasser: Es startet kalt und wird wärmer. Mischtemperatur: \(30\;^\circ\text{C}\).</p><p>\(Q_\text{auf} = m \cdot c \cdot \Delta T\) \(= 0.45\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 10\;\text{K}\) \(\approx 18.8\;\text{kJ}\) — genau so viel hat der Körper abgegeben.</p><p>Wärme fliesst, solange ein Temperaturunterschied besteht. Bei gleicher Temperatur hört der Fluss auf: thermisches Gleichgewicht.</p>',
     mini(kurven_bild([([(t, 30 + 60 * math.exp(-t / 10)) for t in range(0, 61, 2)], 'k-t', 'A', [8, 82]),
                       ([(t, 30 - 10 * math.exp(-t / 10)) for t in range(0, 61, 2)], 'k-t2', 'B', [3, 12])], 0, 60, 0, 100, 10, 10,
                      'Temperatur zweier Körper über der Zeit: A fällt von 90 °C auf 30 °C, B (gestrichelt) steigt von 20 °C auf 30 °C', 't [s]', 'ϑ [°C]'))),
    ('2d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> \(1\;\text{kg}\) Wasser von \(60\;^\circ\text{C}\) und \(1\;\text{kg}\) Wasser von \(20\;^\circ\text{C}\) ergeben \(40\;^\circ\text{C}\). Jemand sagt: «\(1\;\text{kg}\) Eisen von \(60\;^\circ\text{C}\) in \(1\;\text{kg}\) Wasser von \(20\;^\circ\text{C}\) ergibt auch \(40\;^\circ\text{C}\).» Stimmt das? Begründe zuerst ohne Rechnung, dann rechne nach.',
     r'<p>Nein. Eisen gibt je Kilogramm und Kelvin Abkühlung viel weniger Wärme ab (\(450\) statt \(4182\;\text{J/(kg·K)}\)). Damit das Wasser um \(1\;\text{K}\) wärmer wird, muss das Eisen um gut \(9\;\text{K}\) abkühlen — die Endtemperatur liegt nahe bei \(20\;^\circ\text{C}\).</p><p>\(\vartheta_\text{m} = \dfrac{m_1 c_1 \vartheta_1 + m_2 c_2 \vartheta_2}{m_1 c_1 + m_2 c_2}\) mit \(m_1 c_1 = 1\;\text{kg} \cdot 450\;\text{J/(kg·K)} = 450\;\text{J/K}\) und \(m_2 c_2 = 1\;\text{kg} \cdot 4182\;\text{J/(kg·K)} = 4182\;\text{J/K}\):</p><p>\(\vartheta_\text{m} = \frac{450\;\text{J/K} \cdot 60\;^\circ\text{C} + 4182\;\text{J/K} \cdot 20\;^\circ\text{C}}{4632\;\text{J/K}}\) \(\approx 23.9\;^\circ\text{C}\).</p>', ''),
])
k2 = kapitel(2, 'waermebilanz', 'Wärmebilanz und thermisches Gleichgewicht', 'K2', 55,
    r'Du stellst die Wärmebilanz \(Q_\text{ab} = Q_\text{auf}\) auf und berechnest die Temperatur im thermischen Gleichgewicht — auch für zwei verschiedene Stoffe und rückwärts.',
    ('p5-2-lp-bilanz', 'Wärme sehen: was der eine abgibt, nimmt der andere auf'),
    sim2, ('p5-2-lp-kontrolle-bilanz', 'Kontrollfragen zur Wärmebilanz'),
    fest2, [uebung('mischen', 'Mischtemperatur'), uebung('abschrecken', 'Metall im Wasser'), uebung('mischen-rueck', 'Rückwärts: Masse oder Temperatur')],
    auf2, f'<a href="{TS}#mischung">Themenseite 5.2, Mischtemperatur berechnen</a> · <a href="{TS}#einstieg">Thermisches Gleichgewicht</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Eis in einem Topf auf einer Heizplatte schmilzt, wird zu Wasser und verdampft; darunter die Heizkurve: Temperatur über der Zeit', '-4 -4 308 336',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'm', '<i>m</i> Eis', 0.1, 1.0, 0.05, 0.6, 'kg', 2) + '\n          '
    + regler('s3', 'P', '<i>P</i> Platte', 200, 2000, 50, 800, 'W', 0) + '\n          '
    + regler('s3', 't0', '<i>ϑ</i><sub>0</sub> Start', -30, 0, 1, -10, '°C', 0) + '\n        </div>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Latente Wärme und Heizkurve</div>
          <p>Beim <b>Schmelzen</b> und <b>Verdampfen</b> bleibt die Temperatur konstant, obwohl Wärme zugeführt wird: Die Energie löst die Teilchen aus ihrem Verband, statt sie schneller zu machen. Diese Wärme heisst <b>latente Wärme</b>:</p>
          <p>\[ Q = m \cdot L_\text{f} \;\;\text{(Schmelzen)} \qquad Q = m \cdot L_\text{v} \;\;\text{(Verdampfen)} \]</p>
          <p>Wasser: \(L_\text{f} = 334\;\text{kJ/kg}\), \(L_\text{v} = 2256\;\text{kJ/kg}\) — fast siebenmal so viel. Beim <b>Erstarren</b> und <b>Kondensieren</b> wird dieselbe Energie wieder frei.</p>
          <p><b>Heizkurve:</b> Temperatur über der Zeit (oder der zugeführten Wärme) bei gleichmässiger Heizleistung \(P\). Schräge Stücke: erwärmen, umso flacher, je grösser \(m \cdot c\). Waagrechte Stücke: Phasenwechsel bei \(0\;^\circ\text{C}\) und \(100\;^\circ\text{C}\), Dauer \(t = \dfrac{m \cdot L}{P}\).</p>
          <p><b>Über eine Phasengrenze</b> wird abschnittsweise gerechnet und erst am Schluss addiert: Eis erwärmen (\(c_\text{Eis} = 2100\;\text{J/(kg·K)}\)), schmelzen, Wasser erwärmen. In einer Wärmebilanz mit Eis zählen Schmelzen und Erwärmen des Schmelzwassers zur aufgenommenen Wärme.</p>
          <p><b>Schmilzt alles Eis?</b> Zuerst prüfen: Die Wärme, die das Getränk bis \(0\;^\circ\text{C}\) abgeben kann, \(m_\text{G} \cdot c \cdot (\vartheta_\text{G} - 0\;^\circ\text{C})\), mit der Schmelzwärme \(m_\text{Eis} \cdot L_\text{f}\) vergleichen. Reicht sie, gilt die Bilanz oben. Reicht sie nicht, <b>bleibt Eis übrig</b>: Die Mischung hat \(0\;^\circ\text{C}\), und geschmolzen ist nur \(m = \dfrac{Q}{L_\text{f}}\).</p>
          <p>Beispiel: \(0.15\;\text{kg}\) Wasser von \(10\;^\circ\text{C}\) und \(0.10\;\text{kg}\) Eis von \(0\;^\circ\text{C}\). Das Wasser gibt bis \(0\;^\circ\text{C}\) höchstens \(Q = 0.15\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 10\;\text{K}\) \(= 6273\;\text{J}\) ab; alles Eis zu schmelzen bräuchte \(0.10\;\text{kg} \cdot 334\,000\;\text{J/kg}\) \(= 33\,400\;\text{J}\). Es schmelzen nur \(\dfrac{6273\;\text{J}}{334\,000\;\text{J/kg}} \approx 0.019\;\text{kg}\), rund \(0.081\;\text{kg}\) Eis bleiben übrig, die Mischung hat \(0\;^\circ\text{C}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Mit \(Q = m \cdot c \cdot \Delta T\) über die Phasengrenze gerechnet: Von \(-10\;^\circ\text{C}\) bis \(20\;^\circ\text{C}\) fehlt so das ganze Schmelzen — der grösste Beitrag.</p>
          <p>Die Bilanz mit Eis ohne Prüfung gerechnet: Kommt eine Temperatur unter \(0\;^\circ\text{C}\) heraus, schmilzt nicht alles Eis — die Mischung bleibt bei \(0\;^\circ\text{C}\).</p>
          <p>\(L_\text{f}\) und \(L_\text{v}\) vertauscht, oder kJ/kg wie J/kg eingesetzt.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Skizziere die Heizkurve von \(0.20\;\text{kg}\) Eis von \(-15\;^\circ\text{C}\), das auf einer gleichmässig heizenden Platte liegt, bis alles verdampft ist. Beschrifte beide Achsen mit Grösse und Einheit und jeden Abschnitt. Welcher Abschnitt dauert am längsten, und warum?',
     r'<p>Achsen: Zeit \(t\) in min (oder zugeführte Wärme \(Q\) in kJ) nach rechts, Temperatur \(\vartheta\) in °C nach oben. Abschnitte: steil von \(-15\;^\circ\text{C}\) auf \(0\;^\circ\text{C}\) (Eis wird wärmer), waagrecht bei \(0\;^\circ\text{C}\) (schmilzt), schräg bis \(100\;^\circ\text{C}\), halb so steil wie beim Eis (Wasser wird wärmer), waagrecht bei \(100\;^\circ\text{C}\) (siedet).</p><p>Am längsten dauert das Sieden: \(Q = m \cdot L_\text{v} = 0.20\;\text{kg} \cdot 2256\;\text{kJ/kg} = 451.2\;\text{kJ}\), mehr als alle anderen Abschnitte zusammen (\(6.3\;\text{kJ} + 66.8\;\text{kJ} + 83.6\;\text{kJ}\)).</p>', ''),
    ('3b', 3, r'Ein Eiswürfel (\(25\;\text{g}\), \(0\;^\circ\text{C}\)) kommt in \(0.30\;\text{kg}\) Saft von \(22\;^\circ\text{C}\) (Stoffwerte wie Wasser). Welche Temperatur hat der Saft, wenn das Eis ganz geschmolzen ist? Verluste vernachlässigt.',
     r'<p>\(Q_\text{ab} = Q_\text{auf}\): Der Saft kühlt ab; das Eis schmilzt und das Schmelzwasser wird wärmer:</p><p>\[ m_S \cdot c \cdot (22\;^\circ\text{C} - \vartheta_\text{m}) = m_E \cdot L_\text{f} + m_E \cdot c \cdot (\vartheta_\text{m} - 0\;^\circ\text{C}) \]</p><p>\(0.30\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot (22\;^\circ\text{C} - \vartheta_\text{m})\) \(= 0.025\;\text{kg} \cdot 334\,000\;\text{J/kg}\) \(+ 0.025\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot \vartheta_\text{m}\)</p><p>\(27\,601\;\text{J} - 1254.6\;\text{J/K} \cdot \vartheta_\text{m}\) \(= 8350\;\text{J} + 104.6\;\text{J/K} \cdot \vartheta_\text{m}\), also \(\vartheta_\text{m} = \dfrac{19\,251\;\text{J}}{1359.2\;\text{J/K}} \approx 14.2\;^\circ\text{C}\).</p><p>Probe: Zum Schmelzen braucht es \(8.35\;\text{kJ}\), der Saft könnte bis \(0\;^\circ\text{C}\) \(27.6\;\text{kJ}\) abgeben — das Eis schmilzt ganz.</p>', ''),
    ('3c', 3, r'Kerzenwachs (\(0.10\;\text{kg}\)) wird mit \(50\;\text{W}\) gleichmässig erwärmt (Diagramm). Bei welcher Temperatur schmilzt es? Bestimme aus dem Diagramm die spezifische Schmelzwärme des Wachses.',
     r'<p>Das waagrechte Stück liegt bei \(60\;^\circ\text{C}\): die Schmelztemperatur. Es dauert von \(3\;\text{min}\) bis \(10\;\text{min}\), also \(7\;\text{min} = 420\;\text{s}\).</p><p>\(Q = P \cdot t = 50\;\text{W} \cdot 420\;\text{s} = 21\,000\;\text{J}\), und \(Q = m \cdot L_\text{f}\) gibt \(L_\text{f} = \dfrac{Q}{m} = \dfrac{21\,000\;\text{J}}{0.10\;\text{kg}}\) \(= 210\,000\;\text{J/kg} = 210\;\text{kJ/kg}\).</p>',
     mini(kurven_bild([([(0, 20), (3, 60), (10, 60), (13, 90)], 'k-t', '', None)], 0, 14, 0, 100, 1, 10,
                      'Heizkurve von Kerzenwachs: von 20 °C bei 0 min auf 60 °C bei 3 min, waagrecht bis 10 min, dann bis 90 °C bei 13 min', 't [min]', 'ϑ [°C]'))),
    ('3d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Bei Frost besprühen Obstbauern ihre Blüten laufend mit Wasser, das auf den Blüten gefriert. Erkläre, warum das die Blüten schützt. Wie viel Wärme gibt \(1\;\text{kg}\) Wasser beim Gefrieren ab, verglichen mit dem Abkühlen von \(10\;^\circ\text{C}\) auf \(0\;^\circ\text{C}\)?',
     r'<p>Beim Erstarren wird die Schmelzwärme frei: \(Q = m \cdot L_\text{f} = 1\;\text{kg} \cdot 334\;\text{kJ/kg} = 334\;\text{kJ}\). Solange Wasser gefriert, bleibt die Eisschicht bei \(0\;^\circ\text{C}\), und die Blüte kühlt nicht tiefer ab.</p><p>Abkühlen: \(Q = m \cdot c \cdot \Delta T = 1\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 10\;\text{K} \approx 41.8\;\text{kJ}\). Das Gefrieren liefert rund achtmal so viel Wärme.</p>', ''),
])
k3 = kapitel(3, 'heizkurve', 'Latente Wärme und Heizkurve', 'K2 · K3', 60,
    r'Du rechnest mit der latenten Wärme \(Q = m \cdot L\), stellst den Temperaturverlauf beim Erwärmen über Schmelzen und Sieden als Heizkurve dar und stellst Wärmebilanzen mit Zustandsänderung abschnittsweise auf.',
    ('p5-2-lp-heizkurve', 'Wärme sehen: wenn die Temperatur stehen bleibt'),
    sim3, ('p5-2-lp-kontrolle-heizkurve', 'Kontrollfragen zu latenter Wärme und Heizkurve'),
    fest3, [uebung('latent', 'Latente Wärme'), uebung('abschnitte', 'Vom Eis zum Wasser'), uebung('eiswuerfel', 'Eiswürfel im Getränk'), uebung('plateau', 'Wie lange dauert der Phasenwechsel?')],
    auf3, f'<a href="{TS}#heizkurve">Themenseite 5.2, der Temperaturverlauf: Eis, Wasser, Dampf</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Ein Kessel verbrennt Brennstoff und heizt einen Boiler mit 200 Liter Wasser; ein Teil der Energie geht durch den Kamin; darunter die Energien als Balken', '-4 -4 308 332',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 'm', '<i>m</i> Brennstoff', 0.1, 1.5, 0.05, 0.6, 'kg', 2) + '\n          '
    + regler('s4', 'eta', '<i>η</i> Kessel', 0.5, 1.0, 0.01, 0.8, '', 2) + '\n        </div>',
    knoepfe('f', 'Brennstoff', [('oel', 'Heizöl'), ('gas', 'Erdgas'), ('pel', 'Holzpellets')], 'oel'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Heizwert und Wirkungsgrad</div>
          <p>Der <b>Heizwert</b> \(H\) ist die Energie, die beim vollständigen Verbrennen von \(1\;\text{kg}\) Brennstoff frei wird. Aus einer Menge wird so eine Energie:</p>
          <p>\[ Q_\text{zu} = m \cdot H \]</p>
          <p>Heizöl \(42.6\;\text{MJ/kg}\) (\(1\;\text{l}\) wiegt \(0.84\;\text{kg}\)), Erdgas \(50.0\), Propan \(46.4\) (rund \(13\;\text{kWh/kg}\)), Holzpellets \(17.0\), trockenes Buchenholz \(15.0\;\text{MJ/kg}\).</p>
          <p>Nutzbar ist nur der Anteil \(\eta = \dfrac{E_\text{nutz}}{E_\text{zu}} \le 1\) (Wirkungsgrad, aus 4.3):</p>
          <p>\[ Q_\text{nutz} = \eta \cdot m \cdot H \qquad m = \frac{Q_\text{nutz}}{\eta \cdot H} \]</p>
          <p>Ist die Menge gesucht, steht \(\eta\) im Nenner. Elektrisch ist die zugeführte Energie \(E = P \cdot t\), also \(t = \dfrac{Q_\text{nutz}}{\eta \cdot P}\). Umrechnen: \(1\;\text{kWh} = 3.6\;\text{MJ}\). Was nicht Nutzwärme wird, verschwindet nicht: Es geht als Wärme an Abgas, Kamin und Umgebung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Wirkungsgrad multipliziert, wenn die Menge gesucht ist: Für \(100\;\text{MJ}\) Nutzwärme braucht ein Kessel mit \(\eta = 0.80\) Brennstoff für \(125\;\text{MJ}\), nicht für \(80\;\text{MJ}\).</p>
          <p>kWh und MJ gemischt, oder Liter Heizöl wie Kilogramm eingesetzt.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Ein Haus wechselt vom Ölkessel (\(\eta = 0.90\)) zur Pelletheizung (\(\eta = 0.85\)). Im Jahr hat es bisher \(1000\;\text{l}\) Heizöl (\(0.84\;\text{kg/l}\)) verbraucht. Wie viele Kilogramm Holzpellets braucht es für dieselbe Nutzwärme? Warum braucht das Pelletlager trotzdem viel mehr Platz als der Öltank (Pellets: \(650\;\text{kg}\) je \(\text{m}^3\))?',
     r'<p>Nutzwärme bisher: \(m_\text{Öl} = 1000\;\text{l} \cdot 0.84\;\text{kg/l} = 840\;\text{kg}\); \(Q_\text{nutz} = \eta \cdot m \cdot H = 0.90 \cdot 840\;\text{kg} \cdot 42.6\;\text{MJ/kg}\) \(\approx 32\,200\;\text{MJ}\).</p><p>\(m_\text{P} = \dfrac{Q_\text{nutz}}{\eta_\text{P} \cdot H_\text{P}}\) \(= \dfrac{32\,206\;\text{MJ}}{0.85 \cdot 17.0\;\text{MJ/kg}}\) \(\approx 2230\;\text{kg}\).</p><p>Platz: \(V = \dfrac{2230\;\text{kg}}{650\;\text{kg/m}^3} \approx 3.4\;\text{m}^3\) Pellets gegen \(1\;\text{m}^3\) Öl. Pellets haben einen kleineren Heizwert je Kilogramm, und als Schüttgut wiegt ein Kubikmeter viel weniger als Öl.</p>', ''),
    ('4b', 3, r'Ein Boiler mit \(150\;\text{l}\) Wasser und einem Heizstab von \(3\;\text{kW}\) braucht \(3.0\;\text{h}\), um das Wasser von \(12\;^\circ\text{C}\) auf \(60\;^\circ\text{C}\) aufzuheizen. Wie gross ist sein Wirkungsgrad? Wohin geht die Energie, die nicht im Wasser ankommt?',
     r'<p>\(Q_\text{nutz} = m \cdot c \cdot \Delta T\) \(= 150\;\text{kg} \cdot 4182\;\text{J/(kg·K)} \cdot 48\;\text{K}\) \(\approx 30.1\;\text{MJ}\).</p><p>\(E_\text{zu} = P \cdot t = 3000\;\text{W} \cdot 10\,800\;\text{s}\) \(= 32.4\;\text{MJ}\); \(\eta = \dfrac{Q_\text{nutz}}{E_\text{zu}} = \dfrac{30.1\;\text{MJ}}{32.4\;\text{MJ}} \approx 0.93\).</p><p>Der Heizstab macht aus dem Strom praktisch ganz Wärme; rund \(7\;\%\) gehen aber über Boilerwand und Leitungen an die Umgebung — verschwunden ist die Energie nicht.</p>', ''),
    ('4c', 3, r'Das Balkendiagramm zeigt die Energien eines Holzofens an einem Abend. Lies ab und bestimme den Wirkungsgrad und den Verlust. Wie viel trockenes Buchenholz (\(H = 15.0\;\text{MJ/kg}\)) wurde verbrannt?',
     r'<p>Zugeführt \(60\;\text{MJ}\), Nutzwärme \(48\;\text{MJ}\): \(\eta = \dfrac{Q_\text{nutz}}{Q_\text{zu}} = \dfrac{48\;\text{MJ}}{60\;\text{MJ}} = 0.80\); Verlust \(60\;\text{MJ} - 48\;\text{MJ} = 12\;\text{MJ}\).</p><p>\(m = \dfrac{Q_\text{zu}}{H} = \dfrac{60\;\text{MJ}}{15.0\;\text{MJ/kg}} = 4.0\;\text{kg}\).</p>',
     mini(balken_bild([('zugeführt', 60, 'bal-zu'), ('Nutzwärme', 48, 'bal-nutz')], 70, 10, 'Balken: zugeführte Energie 60 MJ, Nutzwärme 48 MJ', 'Q [MJ]'))),
    ('4d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Frisch geschlagenes Holz liefert je Kilogramm viel weniger Nutzwärme als trockenes. Nenne zwei Gründe und verbinde einen davon mit Kapitel 3.',
     r'<p>Erstens ist ein Teil der Masse Wasser, das selbst nicht brennt: Ein Kilogramm nasses Holz enthält weniger brennbaren Stoff.</p><p>Zweitens muss dieses Wasser beim Verbrennen verdampfen. Die Verdampfungswärme (\(2256\;\text{kJ}\) je Kilogramm Wasser, Kapitel 3) geht mit dem Abgas zum Kamin hinaus und fehlt als Nutzwärme.</p>', ''),
])
k4 = kapitel(4, 'heizwert', 'Heizwert und Wirkungsgrad', 'K2 · K4', 55,
    r'Du berechnest mit dem Heizwert die beim Verbrennen frei werdende Energie, berücksichtigst den Wirkungsgrad und bestimmst daraus Nutzwärme, Brennstoffmenge oder Heizzeit.',
    ('p5-2-lp-heizwert', 'Wärme sehen: vom Brennstoff zur Nutzwärme'),
    sim4, ('p5-2-lp-kontrolle-heizwert', 'Kontrollfragen zu Heizwert und Wirkungsgrad'),
    fest4, [uebung('heizwert', 'Nutzwärme aus dem Brennstoff'), uebung('brennstoff', 'Wie viel Brennstoff?'), uebung('heizzeit', 'Heizzeit mit Strom')],
    auf4, f'<a href="{TS}#definition">Themenseite 5.2, Grundbegriffe: Leistung, Wirkungsgrad und Heizwert</a> · <a href="{TS}#wirkungsgrad">Wirkungsgrad</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur('sim5', 'Energiefluss eines gewählten Energiesystems je 100 Kilowattstunden und seine Lieferung im Sommer- und im Winterhalbjahr gegen den Bedarf', '-4 -4 308 300',
    '        <div class="reglerfeld">\n          '
    + regler('s5', 'E', '<i>E</i> Strom', 1000, 10000, 100, 3000, 'kWh', 0) + '\n        </div>\n        '
    + knoepfe('sys', 'System', [('wasser', 'Wasserkraft'), ('wind', 'Wind'), ('pv', 'Photovoltaik'), ('wkk', 'Biogas-WKK'), ('kern', 'Kernkraftwerk'), ('wp', 'Wärmepumpe')], 'wkk'))
fest5 = r'''      <div class="merk">
        <div class="titel">Energiesysteme vergleichen</div>
        <p><b>Quelle oder Technik?</b> Wasserkraft, Wind, Sonne und Biogas sind <b>erneuerbare Quellen</b>: Die Energie fliesst laufend nach, fast immer letztlich von der Sonne. Kernenergie ist eine Quelle, aber <b>nicht erneuerbar</b> (Uranvorrat). Die <b>Wärmepumpe</b> und die <b>Wärme-Kraft-Kopplung</b> (WKK, auch Kraft-Wärme-Kopplung) sind <b>keine Quellen</b>: Techniken, die zugeführte Energie besser nutzen — die Wärmepumpe hebt Umgebungswärme mit Strom auf Heiztemperatur (\(\text{COP} = \dfrac{Q_\text{warm}}{E_\text{el}}\)), die WKK nutzt die Abwärme der Stromerzeugung als Heizwärme.</p>
        <p>Verglichen wird nach drei Gesichtspunkten: <b>Verfügbarkeit</b> (wann liefert es, lässt es sich speichern?), <b>Wirkungsgrad</b> und <b>Kohlendioxid</b> über den ganzen Lebensweg.</p>
      </div>
      <div class="tabhuelle"><table class="gesetze">
        <thead><tr><th>System</th><th>Wirkungsgrad (Modell)</th><th>Verfügbarkeit</th><th>CO₂ je kWh</th><th>Grössenordnung</th></tr></thead>
        <tbody>
          <tr><td>Wasserkraft (Speichersee)</td><td class="wort">rund 85 %</td><td class="wort">speicherbar, auf Abruf</td><td class="wort">rund 24 g</td><td class="wort">\(1\;\text{m}^3\) Wasser, \(500\;\text{m}\) Fallhöhe: \(\eta \cdot m \cdot g \cdot h \approx 1.2\;\text{kWh}\)</td></tr>
          <tr><td>Windkraft</td><td class="wort">rund 45 % der Windenergie</td><td class="wort">wetterabhängig, im Winter mehr</td><td class="wort">rund 11 g</td><td class="wort">Turbine mit \(2\;\text{MW}\), rund \(1800\) Volllaststunden: \(3.6\;\text{GWh}\) im Jahr</td></tr>
          <tr><td>Photovoltaik</td><td class="wort">rund 20 %</td><td class="wort">nur bei Tag, im Winter wenig</td><td class="wort">rund 41 g</td><td class="wort">\(1\;\text{m}^2\) Modul: \(0.20 \cdot 1100\;\text{kWh} = 220\;\text{kWh}\) im Jahr</td></tr>
          <tr><td>Biogas mit WKK</td><td class="wort">Strom 35 %, Wärme 55 %</td><td class="wort">speicherbar, gleichmässig</td><td class="wort">gering, aus Gülle und Abfällen</td><td class="wort">\(1\;\text{m}^3\) Biogas: \(6\;\text{kWh}\), davon \(2.1\;\text{kWh}\) Strom</td></tr>
          <tr><td>Kernkraftwerk</td><td class="wort">rund 33 %, Rest Abwärme</td><td class="wort">gleichmässig, Tag und Nacht</td><td class="wort">rund 12 g</td><td class="wort">\(1\;\text{g}\) Uran-235: rund \(22\,800\;\text{kWh}\) Wärme; radioaktiver Abfall, Störfallrisiko</td></tr>
          <tr><td>Wärmepumpe</td><td class="wort">COP 3 bis 5</td><td class="wort">braucht vor allem im Winter Strom</td><td class="wort">je nach Herkunft des Stroms</td><td class="wort">\(1\;\text{kWh}\) Strom und \(3\;\text{kWh}\) Umgebungswärme geben \(4\;\text{kWh}\) Heizwärme (COP 4)</td></tr>
          <tr><td>Sonnenkollektor (Solarwärme)</td><td class="wort">rund 50 % (Wärme)</td><td class="wort">nur bei Tag, im Sommer viel mehr; Speicher: Warmwassertank</td><td class="wort">gering</td><td class="wort">\(1\;\text{m}^2\) Kollektor bei \(1100\;\text{kWh}\) Sonnenlicht im Jahr: höchstens rund \(0.5 \cdot 1100\;\text{kWh} = 550\;\text{kWh}\) Wärme, im Betrieb meist weniger</td></tr>
        </tbody>
      </table></div>
      <p class="komm">CO₂: Medianwerte über den Lebensweg (IPCC 2014); zum Vergleich ein Erdgaskraftwerk rund 490 g je kWh Strom. Halbjahre, Wirkungsgrade und Volllaststunden sind gerundete Modellannahmen.</p>
      <div class="festhalten">
        <div class="merk">
          <div class="titel">Potential</div>
          <p>Die Sonne liefert bei uns rund \(1100\;\text{kWh}\) je Quadratmeter und Jahr. Für rund \(60\;\text{TWh}\) Strom im Jahr — etwa den Bedarf der Schweiz — bräuchte es \(\dfrac{60 \cdot 10^9\;\text{kWh}}{220\;\text{kWh/m}^2} \approx 270\;\text{km}^2\) Module, gut ein halbes Prozent der Landesfläche. Das Potential ist gross, aber im Winterhalbjahr käme nur rund ein Drittel. Darum zählen speicherbare Systeme (Speicherseen, Biogas) und solche, die im Winter mehr liefern (Wind).</p>
          <p><b>Solarwärme:</b> Ein Sonnenkollektor macht aus dem Sonnenlicht direkt Wärme, meist fürs Warmwasser — mit rund \(50\;\%\) Wirkungsgrad mehr als doppelt so viel Energie je Quadratmeter wie ein Photovoltaikmodul (Strom, rund \(20\;\%\)). Gespeichert wird im Warmwassertank, für Tage, nicht für den Winter.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Wärmepumpe ist eine erneuerbare Energiequelle.» Sie braucht Strom und hebt vorhandene Wärme an; erneuerbar ist allenfalls die Umgebungswärme, die sie nutzt.</p>
          <p>Die Jahressumme mit der Versorgung im Winter verwechselt: \(4500\;\text{kWh}\) Solarstrom im Jahr decken einen Jahresbedarf von \(4500\;\text{kWh}\) im Winterhalbjahr noch lange nicht (dort kommen rund \(30\;\%\), gebraucht werden \(55\;\%\)).</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Ein Speichersee enthält \(2.0\;\text{Mio. m}^3\) Wasser, das \(800\;\text{m}\) tief zur Zentrale fällt (\(\eta = 0.85\)). Wie viel Strom entsteht, in kWh? Wie viele Haushalte mit \(4500\;\text{kWh}\) im Jahr könnte das versorgen?',
     r'<p>\(E = \eta \cdot m \cdot g \cdot h\) mit \(m = \rho \cdot V = 1000\;\text{kg/m}^3 \cdot 2.0 \cdot 10^6\;\text{m}^3 = 2.0 \cdot 10^9\;\text{kg}\).</p><p>\(E = 0.85 \cdot 2.0 \cdot 10^9\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 800\;\text{m}\) \(\approx 1.33 \cdot 10^{13}\;\text{J}\) \(= \dfrac{1.33 \cdot 10^{13}\;\text{J}}{3.6 \cdot 10^6\;\text{J/kWh}} \approx 3.71 \cdot 10^6\;\text{kWh}\).</p><p>\(\dfrac{3.71 \cdot 10^6\;\text{kWh}}{4500\;\text{kWh}} \approx 820\) Haushalte — und das auf Abruf, auch im Winter.</p>', ''),
    ('5b', 3, r'Ein Haus heizt mit einer Wärmepumpe (\(\text{COP} = 3.5\)) und braucht \(14\,000\;\text{kWh}\) Heizwärme im Jahr, drei Viertel davon im Winterhalbjahr. Auf dem Dach liegen \(40\;\text{m}^2\) Module (\(220\;\text{kWh}\) je m² und Jahr, \(30\;\%\) davon im Winterhalbjahr). Reicht der Solarstrom für die Wärmepumpe — übers Jahr und im Winter?',
     r'<p>Strom der Wärmepumpe: \(E_\text{el} = \dfrac{Q_\text{warm}}{\text{COP}} = \dfrac{14\,000\;\text{kWh}}{3.5} = 4000\;\text{kWh}\), davon im Winter \(0.75 \cdot 4000\;\text{kWh} = 3000\;\text{kWh}\).</p><p>Solarstrom: \(40\;\text{m}^2 \cdot 220\;\text{kWh/m}^2 = 8800\;\text{kWh}\) im Jahr, im Winter \(0.30 \cdot 8800\;\text{kWh} = 2640\;\text{kWh}\).</p><p>Übers Jahr reicht es gut, im Winter nicht ganz (\(2640\;\text{kWh}\) gegen \(3000\;\text{kWh}\)) — und der übrige Strom des Haushalts ist noch nicht gerechnet.</p>', ''),
    ('5c', 3, r'Das Diagramm zeigt für eine Gemeinde, wie viel Strom ihre Anlagen im Sommer- und im Winterhalbjahr liefern (grün) und wie viel sie braucht (gestrichelt), in GWh. Lies den Überschuss und die Lücke ab. Nenne zwei Systeme, die die Lücke schliessen könnten, und begründe.',
     r'<p>Sommer: \(70\;\text{GWh}\) geliefert, \(50\;\text{GWh}\) gebraucht — \(20\;\text{GWh}\) Überschuss. Winter: \(40\;\text{GWh}\) geliefert, \(60\;\text{GWh}\) gebraucht — \(20\;\text{GWh}\) Lücke.</p><p>Zum Beispiel ein Speichersee (Sommerwasser speichern, im Winter auf Abruf liefern), Windkraft (liefert im Winter mehr) oder Biogas mit WKK (speicherbar, gleichmässig, liefert dazu Heizwärme). Eine weitere Solaranlage hilft kaum: Sie vergrössert vor allem den Sommerüberschuss.</p>',
     mini(saison_bild([70, 40], [50, 60], 80, 10, 'Sommer: Lieferung 70, Bedarf 50; Winter: Lieferung 40, Bedarf 60 GWh', 'E [GWh]'))),
    ('5d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Vergleiche ein Kernkraftwerk und eine Windturbine nach den drei Gesichtspunkten Verfügbarkeit, Wirkungsgrad und Kohlendioxid. Nenne für jedes einen weiteren Punkt, der in diesen drei nicht vorkommt.',
     r'<p>Verfügbarkeit: Das Kernkraftwerk liefert gleichmässig, Tag und Nacht; die Windturbine nur bei Wind, im Winter mehr. Wirkungsgrad: rund \(33\;\%\) (zwei Drittel Abwärme) gegen rund \(45\;\%\) der Windenergie — beim Wind ist die Quelle aber gratis und unerschöpflich. Kohlendioxid: beide gering über den Lebensweg (rund \(12\;\text{g}\) und \(11\;\text{g}\) je kWh).</p><p>Weitere Punkte: beim Kernkraftwerk radioaktiver Abfall, Störfallrisiko und der begrenzte Uranvorrat; bei der Windturbine Landschaftsbild und Lärm, und es braucht Speicher oder andere Kraftwerke für windstille Tage.</p>', ''),
])
k5 = kapitel(5, 'energiesysteme', 'Energiesysteme vergleichen', 'K5', 55,
    r'Du beschreibst das Potential der erneuerbaren Energien und vergleichst Wasserkraft, Wind, Sonne, Biogas, Wärmepumpe, Wärme-Kraft-Kopplung und Kernenergie nach Verfügbarkeit, Wirkungsgrad und Kohlendioxid — mit nachgerechneten Grössenordnungen.',
    ('p5-2-lp-energiesysteme', 'Wärme sehen: Energiesysteme im Vergleich'),
    sim5, ('p5-2-lp-kontrolle-energiesysteme', 'Kontrollfragen zu den Energiesystemen'),
    fest5, [uebung('pv', 'Solaranlage'), uebung('wasserkraft', 'Strom aus dem Speichersee'), uebung('waermepumpe', 'Strom für die Wärmepumpe')],
    auf5, f'<a href="{TS}#definition">Themenseite 5.2, Grundbegriffe: Wärmepumpe und erneuerbare Energien</a> · <a href="{TS}#waermepumpe">Wärmepumpe</a>')

# ------------------------------------------------------------------ Kapitel 6
sim6 = figur_anim('sim6', 'Zwischen einer heissen und einer kalten Platte liegt eine Schicht; gemessen wird der Wärmestrom durch Leitung, Konvektion und Strahlung', '-4 -4 308 290', '',
    knoepfe('fu', 'Schicht', [('kupfer', 'Kupfer'), ('holz', 'Holz'), ('wasser', 'Wasser'), ('luft', 'Luft'), ('vakuum', 'Vakuum')], 'luft') + '\n        '
    + knoepfe('lage', 'heisse Platte', [('unten', 'unten'), ('oben', 'oben')], 'oben') + '\n        '
    + knoepfe('ob', 'Oberflächen', [('schwarz', 'schwarz'), ('spiegel', 'verspiegelt')], 'schwarz'))
fest6 = r'''      <div class="tabhuelle"><table class="gesetze">
        <thead><tr><th>Weg</th><th>Was die Energie trägt</th><th>Braucht</th><th>Bremsen mit</th></tr></thead>
        <tbody>
          <tr><td>Wärmeleitung</td><td class="wort">Teilchen geben Bewegungsenergie an ihre Nachbarn weiter; der Stoff bleibt am Ort</td><td class="wort">Stoff</td><td class="wort">schlechten Leitern: Holz, Kork, eingeschlossener Luft</td></tr>
          <tr><td>Konvektion (Strömung)</td><td class="wort">warmer Stoff strömt selbst und nimmt die Energie mit: warm steigt auf, kalt sinkt nach</td><td class="wort">Flüssigkeit oder Gas, das strömen kann</td><td class="wort">dichten Fugen, Abdecken, Luft in kleinen Kammern</td></tr>
          <tr><td>Wärmestrahlung</td><td class="wort">Infrarotstrahlung (elektromagnetisch, wie Licht, aber langwelliger)</td><td class="wort">nichts — auch durch Vakuum</td><td class="wort">spiegelnden (glänzenden) Flächen, die sie zurückwerfen; helle Farbe wirkt vor allem gegen Sonnenlicht</td></tr>
        </tbody>
      </table></div>
      <div class="festhalten">
        <div class="merk">
          <div class="titel">Wärmetransport</div>
          <p>Wie gut ein Stoff leitet, sagt die <b>Wärmeleitfähigkeit</b> \(\lambda\) in \(\text{W/(m·K)}\): Kupfer \(400\), Eisen \(80\), Glas \(0.8\), Wasser \(0.6\), Holz \(0.15\), Mineralwolle \(0.04\), ruhende Luft \(0.026\). Bei gleicher Fläche, Dicke und Temperaturdifferenz fliesst durch die Platte mit dem doppelten \(\lambda\) doppelt so viel Wärme je Sekunde.</p>
          <p><b>Warm oder kalt anfühlen:</b> Die Haut spürt, wie schnell sie Wärme verliert, nicht die Temperatur des Gegenstands. Ein guter Leiter zieht die Wärme rasch von der Berührstelle weg, die Haut dort kühlt ab — er fühlt sich kälter an als ein schlechter Leiter mit derselben Temperatur.</p>
          <p>Durchsichtig für Licht heisst nicht durchlässig für Wärmestrahlung: Wasser und Glas lassen Licht durch, schlucken aber Infrarot.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Konvektion mit Leitung verwechselt: Konvektion heisst immer, dass sich der Stoff selbst bewegt. Bei der Leitung wandert nur die Energie.</p>
          <p>«Die Kälte kriecht durch die Wand herein.» Es fliesst nur Wärme — von innen nach aussen.</p>
        </div>
      </div>'''
auf6 = test('t6', 'Aufgaben · Kapitel 6', 13, [
    ('6a', 4, r'Ordne jedem Vorgang den Weg der Wärme zu und begründe in einem Satz: (1) Eine Fussbodenheizung wärmt die nackten Füsse. (2) Warme Luft aus dem offenen Backofen steigt zur Decke. (3) Eine Infrarotlampe im Badezimmer wärmt die Haut, obwohl die Luft kühl bleibt. Dazu (4) in zwei Sätzen: Unter nackten Füssen fühlt sich der Fliesenboden im Badezimmer kälter an als der Holzboden im Flur; beide liegen seit Tagen im selben, \(20\;^\circ\text{C}\) warmen Haus. Ist der Fliesenboden kälter? Woher kommt der Eindruck?',
     r'<p>(1) Wärmeleitung: Die Füsse berühren den warmen Boden, Energie geht von Teilchen zu Teilchen über.</p><p>(2) Konvektion: Die warme Luft strömt selbst nach oben und nimmt die Energie mit.</p><p>(3) Wärmestrahlung: Das Infrarot der Lampe trägt die Energie durch die Luft, ohne sie stark zu erwärmen.</p><p>(4) Beide Böden haben dieselbe Temperatur — kälter ist der Fliesenboden nicht. Wärmeleitung: Die Fliesen leiten viel besser als Holz und ziehen die Wärme rasch aus den Fusssohlen; die Haut an der Berührstelle kühlt ab, und das spürt man als «kalt».</p>', ''),
    ('6b', 3, r'Ein modernes Fenster hat zwei oder drei Scheiben, dazwischen eine schmale Schicht Argon, und auf dem Glas eine unsichtbare Beschichtung, die Infrarot spiegelt. Welche Massnahme bremst welchen Weg? Begründe.',
     r'<p>Die Gasschicht bremst die Leitung: Gas leitet viel schlechter als Glas (Argon noch etwas schlechter als Luft).</p><p>Weil die Schicht schmal ist, kommt die Strömung kaum in Gang: Auch die Konvektion bleibt klein.</p><p>Die Beschichtung wirft die Wärmestrahlung des Zimmers zurück, lässt das Licht aber durch.</p>', ''),
    ('6c', 3, r'Das Diagramm zeigt, wie viel Wärme je Sekunde durch ein altes Fenster mit zwei Scheiben auf welchem Weg nach draussen geht. Welcher Weg trägt am meisten? Welche Massnahme bringt darum am meisten, und wie viel Prozent des Verlusts betrifft sie?',
     r'<p>Leitung \(20\;\text{W}\), Konvektion \(35\;\text{W}\), Strahlung \(45\;\text{W}\), zusammen \(100\;\text{W}\). Am meisten trägt die Strahlung.</p><p>Am meisten bringt darum eine Infrarot-Beschichtung, die die Strahlung zurückwirft: Sie betrifft \(\dfrac{45\;\text{W}}{100\;\text{W}} = 45\;\%\) des Verlusts.</p>',
     mini(balken_bild([('Leitung', 20, 'bal-q'), ('Konvektion', 35, 'bal-q'), ('Strahlung', 45, 'bal-q')], 50, 5, 'Balken: Leitung 20 W, Konvektion 35 W, Strahlung 45 W', 'P [W]'))),
    ('6d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> In einem Iglu ist es mit ein paar Menschen darin deutlich über \(0\;^\circ\text{C}\) warm, obwohl draussen \(-20\;^\circ\text{C}\) herrschen und die Wände aus Schnee sind. Erkläre mit den drei Wegen.',
     r'<p>Leitung: Schnee enthält viel eingeschlossene Luft und leitet sehr schlecht — die Wärme der Menschen geht nur langsam durch die Wand.</p><p>Konvektion: Die Wände halten den Wind ab; die warme Luft bleibt im Iglu, der tief liegende Eingang lässt sie oben nicht entweichen.</p><p>Strahlung: Die Wärmestrahlung der Menschen trifft die Innenwand, statt in den kalten Nachthimmel zu gehen.</p>', ''),
])
k6 = kapitel(6, 'waermetransport', 'Wärmetransport', 'K6', 50,
    r'Du unterscheidest Wärmeleitung, Konvektion und Wärmestrahlung, ordnest Vorgänge aus dem Alltag zu und begründest, welche Massnahme welchen Weg bremst.',
    ('p5-2-lp-transport', 'Wärme sehen: drei Wege der Wärme'),
    sim6, ('p5-2-lp-kontrolle-transport', 'Kontrollfragen zum Wärmetransport'),
    fest6, [uebung('weg', 'Welcher Weg?'), uebung('bremsen', 'Was bremst die Massnahme?'), uebung('leitfaehigkeit', 'Guter und schlechter Leiter')],
    auf6, f'<a href="{TS}#transport">Themenseite 5.2, die drei Arten des Wärmetransports</a>')

# ------------------------------------------------------------------ Kapitel 7
sim7 = figur('sim7', 'Sonnenlicht und Wärmestrahlung zwischen Weltall, Atmosphäre und Boden; die Bodentemperatur hängt davon ab, wie viel Licht und wie viel Wärmestrahlung die Atmosphäre durchlässt', '-4 -4 308 290',
    '        <div class="reglerfeld">\n          '
    + regler('s7', 'dl', '<i>D</i><sub>L</sub> Licht', 0, 100, 1, 80, '%', 0) + '\n          '
    + regler('s7', 'dw', '<i>D</i><sub>W</sub> Wärmestr.', 0, 100, 1, 60, '%', 0) + '\n        </div>')
fest7 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Licht hinein, Wärmestrahlung hinaus</div>
          <p>Jeder Körper strahlt — je heisser, desto mehr (\(\dfrac{P}{A} = \sigma \cdot T^4\), \(T\) in Kelvin; umgekehrt \(T = \sqrt[4]{\dfrac{P/A}{\sigma}}\)) und desto kürzer die Wellenlänge. Die Sonne (rund \(5500\;^\circ\text{C}\)) strahlt vor allem <b>sichtbares Licht</b> (um \(0.5\;\mu\text{m}\)), die Erde (rund \(15\;^\circ\text{C}\)) <b>Wärmestrahlung</b> im Infrarot (um \(10\;\mu\text{m}\)).</p>
          <p>Die Atmosphäre ist für <b>Licht weitgehend durchlässig</b>, für <b>Wärmestrahlung nur zum kleinen Teil</b>: Wasserdampf, Kohlendioxid und Methan nehmen Infrarot auf und strahlen es nach allen Seiten wieder ab — auch zum Boden zurück (<b>Gegenstrahlung</b>). Stickstoff und Sauerstoff lassen beides durch.</p>
          <p><b>Natürlicher Treibhauseffekt:</b> Ohne ihn müsste der Boden die rund \(240\;\text{W/m}^2\) Sonnenlicht selbst abstrahlen — bei rund \(-18\;^\circ\text{C}\). Gemessen sind rund \(+15\;^\circ\text{C}\); dann strahlt der Boden rund \(390\;\text{W/m}^2\) ab. <b>Im Einschichtmodell</b> (Simulation: Licht \(100\;\%\) durch, \(23\;\%\) der Wärmestrahlung direkt hinaus) kommt die Differenz von rund \(150\;\text{W/m}^2\) als Gegenstrahlung zurück. In Wirklichkeit ist die Gegenstrahlung grösser, rund \(340\;\text{W/m}^2\): Die Atmosphäre nimmt auch einen Teil des Sonnenlichts auf, und der Boden gibt zusätzlich Wärme durch Verdunstung und aufsteigende Luft ab.</p>
          <p><b>Verstärkter Treibhauseffekt:</b> Mehr Treibhausgas (Kohlendioxid von rund \(280\;\text{ppm}\) vor der Industrialisierung auf rund \(430\;\text{ppm}\) heute) hält mehr Wärmestrahlung zurück; der Boden erwärmt sich, bis er wieder so viel abgibt, wie hereinkommt. Im Einschichtmodell entspricht das etwa \(23\;\%\) statt \(25\;\%\) direkt hinaus: von \(13.7\;^\circ\text{C}\) auf \(14.9\;^\circ\text{C}\), rund \(1.2\;\text{K}\) — etwa so viel, wie sich die Erde seither erwärmt hat.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Treibhausgase spiegeln die Wärme zurück.» Sie nehmen die Wärmestrahlung auf und strahlen sie in alle Richtungen ab, nur ein Teil davon geht nach unten.</p>
          <p>Treibhauseffekt und Ozonloch verwechselt: Das Ozonloch betrifft das Ultraviolett der Sonne, nicht die Wärmestrahlung.</p>
        </div>
      </div>'''
auf7 = test('t7', 'Aufgaben · Kapitel 7', 12, [
    ('7a', 3, r'Erkläre in drei Schritten, warum die mittlere Bodentemperatur der Erde über \(-18\;^\circ\text{C}\) liegt. Verwende die Wörter Licht, Wärmestrahlung und Durchlässigkeit.',
     r'<p>1. Das Licht der Sonne kommt durch die Atmosphäre, die dafür weitgehend durchlässig ist, und erwärmt den Boden.</p><p>2. Der Boden strahlt die Energie als Wärmestrahlung (Infrarot) ab. Dafür ist die Atmosphäre nur wenig durchlässig: Wasserdampf und Kohlendioxid nehmen einen grossen Teil auf.</p><p>3. Die Gase strahlen die aufgenommene Energie nach allen Seiten ab, auch zurück zum Boden. Der Boden bekommt Sonnenlicht und Gegenstrahlung und wird wärmer, als er ohne Atmosphäre wäre.</p>', ''),
    ('7b', 3, r'Der Boden hat im Mittel \(15\;^\circ\text{C}\). Wie viel Wärmestrahlung strahlt er je Quadratmeter ab? Im Einschichtmodell gelangen davon \(23\;\%\) direkt ins All. Wie viel ist das, und was geschieht im Modell mit dem Rest?',
     r'<p>\(T = 15 + 273.15 = 288.15\;\text{K}\); \(\dfrac{P}{A} = \sigma \cdot T^4\) \(= 5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4) \cdot (288.15\;\text{K})^4\) \(\approx 391\;\text{W/m}^2\).</p><p>Direkt ins All: \(0.23 \cdot 391\;\text{W/m}^2 \approx 90\;\text{W/m}^2\).</p><p>Den Rest, rund \(301\;\text{W/m}^2\), nimmt die Modell-Atmosphäre auf und strahlt ihn je zur Hälfte nach oben und nach unten ab: rund \(150\;\text{W/m}^2\) Gegenstrahlung zum Boden. Wirklich ist die Gegenstrahlung grösser (rund \(340\;\text{W/m}^2\)), weil die Atmosphäre auch Sonnenlicht aufnimmt und vom Boden Wärme durch Verdunstung und aufsteigende Luft bekommt.</p>', ''),
    ('7c', 3, r'Das Diagramm zeigt, bei welchen Wellenlängen die Sonne und die Erde am meisten strahlen (beide Kurven auf gleiche Höhe gebracht). Grau: Bereiche, die Wasserdampf und Kohlendioxid stark aufnehmen. Lies die beiden Wellenlängen mit der stärksten Strahlung ab. Welche Strahlung wird von der Atmosphäre stärker aufgehalten? Begründe am Diagramm.',
     r'<p>Sonne: rund \(0.5\;\mu\text{m}\) (sichtbares Licht). Erde: rund \(10\;\mu\text{m}\) (Infrarot), rund zwanzigmal länger.</p><p>Die Sonnenkurve liegt fast ganz ausserhalb der grauen Bereiche — das Licht kommt durch. Die Erdkurve liegt zu einem grossen Teil in den grauen Bereichen; nur um \(10\;\mu\text{m}\) bleibt ein «Fenster». Die Wärmestrahlung wird stärker aufgehalten.</p>',
     mini(spektrum_bild('Spektren der Sonne mit Höchstwert bei 0.5 Mikrometer und der Erde mit Höchstwert bei 10 Mikrometer; grau die Aufnahmebereiche von Wasserdampf und Kohlendioxid'))),
    ('7d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Ein Gewächshaus aus Glas wird in der Sonne warm. Was ist gleich wie bei der Atmosphäre, was ist anders?',
     r'<p>Gleich: Licht kommt durch das Glas herein und erwärmt den Boden; dessen Wärmestrahlung kann durch das Glas kaum hinaus.</p><p>Anders: Im Gewächshaus hält vor allem das Glas die warme Luft fest — die Konvektion nach draussen fällt weg. Die Atmosphäre hat keine Hülle; dort wirkt allein die Strahlung, die die Gase aufnehmen und zurückstrahlen. Der Name «Treibhauseffekt» ist ein Vergleich.</p>', ''),
])
k7 = kapitel(7, 'treibhauseffekt', 'Durchlässigkeit der Atmosphäre und Treibhauseffekt', 'K7', 55,
    r'Du beschreibst, warum die Atmosphäre sichtbares Licht weitgehend durchlässt, Wärmestrahlung aber nur zum kleinen Teil, und erklärst damit den natürlichen und den verstärkten Treibhauseffekt.',
    ('p5-2-lp-treibhaus', 'Wärme sehen: Licht hinein, Wärmestrahlung hinaus'),
    sim7, ('p5-2-lp-kontrolle-treibhaus', 'Kontrollfragen zum Treibhauseffekt'),
    fest7, [uebung('abstrahlung', 'Wie viel strahlt ein Körper ab?'), uebung('durchlaessig', 'Wie durchlässig?'), uebung('aussage', 'Richtig oder falsch?')],
    auf7, f'<a href="{TS}#treibhaus">Themenseite 5.2, der Treibhauseffekt</a> · <a href="{LPE}#k6">Leitprogramm Energie, Kapitel 6: die Energiebilanz der Erde</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/waerme/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">5.2 · K1 bis K7</span><span class="zeit">≈ 40 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a>, <a href="#k2">2</a> → K1, K2 (ohne Zustandsänderung) · G2 → <a href="#k3">3</a> → K2 (mit Zustandsänderung) · G3 → <a href="#k3">3</a> → K2, K3 · G4 → <a href="#k4">4</a> → K2, K4 · G5 → <a href="#k5">5</a> → K5 · G6 → <a href="#k6">6</a> → K6 · G7 → <a href="#k7">7</a> → K7</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Die obere Grenze der Leistungszahl, \(\text{{COP}}_\text{{max}} = \dfrac{{T_\text{{warm}}}}{{T_\text{{warm}} - T_\text{{kalt}}}}\) → <a href="{TS}#waermepumpe">Themenseite 5.2, Wärmepumpe</a></li>
        <li>Die Messreihen der Treibhausgase (Kohlendioxid über 800 000 Jahre, Methan, Lachgas) → <a href="{TS}#treibhaus">Themenseite 5.2, Treibhauseffekt</a></li>
        <li>Die Energiebilanz der ganzen Erde mit Albedo und ihr zeitlicher Verlauf → <a href="{LPE}#k6">Leitprogramm Energie, Kapitel 6</a></li>
        <li>Warum die Gase gerade das Infrarot aufnehmen und das Sonnenlicht durchlassen (Absorption nach Wellenlänge, Ozon) → <a href="leitprogramm-wellen.html#treibhauseffekt">Leitprogramm Wellen, Kapitel 6</a></li>
        <li>Temperatur, Teilchenbewegung und die Celsius- und Kelvin-Skala → <a href="{P51}">Themenseite 5.1 Temperatur</a></li>
        <li>Wirkungsgrade einer ganzen Energiekette → <a href="../themen/p4-3-energie.html#wirkungsgrad">Themenseite 4.3, Wirkungsgrad</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Wärme, Version 1.0 (07.10.2026), Erprobung: unverlinkt bis nach /lp-pruefung.
     Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip mit vorgerechnetem Problem → ② laufende Simulation mit Aufgabenleiste →
     ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/waerme/*.tex).
     Quelle: scripts/lp/waerme/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 5.2 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 den Begriff «Wärme» bezüglich übertragener Teilchenbewegungen definieren und die Beziehung
          zwischen Wärme und Temperatur erklären
       K2 die Wärmebilanz und das thermische Gleichgewicht berechnen (mit und ohne Zustandsänderung)
          unter Gebrauch der Begriffe «spezifische Wärmekapazität», «Wirkungsgrad», «latente Wärme»
       K3 den entsprechenden Temperaturverlauf grafisch darstellen
       K4 die Energieerzeugung mit Hilfe des Heizwertes, unter Berücksichtigung des Wirkungsgrades, berechnen
       K5 das Potential der erneuerbaren Energien beschreiben und sie mit anderen Energie erzeugenden
          Systemen vergleichen (Wasserkraft, Windenergie, Solarenergie, Wärmepumpe, Biogas,
          Wärme-Kraft-Kopplungen, Kernenergie)
       K6 die verschiedenen Formen des Wärmetransportes unterscheiden
       K7 die unterschiedliche Durchlässigkeit der Atmosphäre für Licht und Wärmestrahlung und ihre
          Auswirkung auf den Treibhaus-Effekt beschreiben

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1 · Leiste sim1 A1, A3 · Kontrollclip 1 · Aufg. 1a · G1a
       K2 → Kap. 1 (c), 2 (Bilanz ohne Zustandsänderung), 3 (mit Zustandsänderung: latente Wärme,
            Übung «eiswuerfel», Aufg. 3b), 4 (Wirkungsgrad) · Aufg. 1b–1c, 2a–2c, 3b, 4b · G1b (Mischtemperatur:
            Bilanz ohne Zustandsänderung), G2 (Eis in der Limonade: mit Zustandsänderung), G3, G4
       K3 → Kap. 3 · sim3 · Aufg. 3a (Skizze), 3c (Diagramm) · G3 (ablesen und weiterzeichnen)
       K4 → Kap. 4 · sim4 · Aufg. 4a, 4c, 4d · G4
       K5 → Kap. 5 · sim5 · Aufg. 5a–5d · G5
       K6 → Kap. 6 · sim6 · Aufg. 6a–6d · G6
       K7 → Kap. 7 · sim7 · Aufg. 7a–7d · G7
     Planungstabelle (Lernziel · Clip · Erkundung · Problem im Clip · häufiger Fehler · min):
       1 Wärme ist übertragene Energie, Q = m·c·ΔT · p5-2-lp-waerme · sim1 Wärme zuführen · Topf mit Wasser
         · «heiss heisst viel Wärme» · 55
       2 Wärmebilanz, thermisches Gleichgewicht · p5-2-lp-bilanz · sim2 Kalorimeter · Aluminium in Wasser
         · einfacher Mittelwert · 55
       3 Latente Wärme, Heizkurve · p5-2-lp-heizkurve · sim3 Heizkurve · Schnee zu Teewasser · über die
         Phasengrenze mit m·c·ΔT · 60
       4 Heizwert und Wirkungsgrad · p5-2-lp-heizwert · sim4 Kessel und Boiler · Pelletofen · η im Zähler · 55
       5 Energiesysteme vergleichen · p5-2-lp-energiesysteme · sim5 Systemvergleich · Solarstrom für eine
         Gemeinde · Wärmepumpe als Quelle · 55
       6 Wärmetransport · p5-2-lp-transport · sim6 Wärmewege · vom Heizkörper zur Hand · Leitung und
         Konvektion verwechselt · 50
       7 Durchlässigkeit, Treibhauseffekt · p5-2-lp-treibhaus · sim7 Einschichtmodell · −18 °C gegen 15 °C ·
         «Gase spiegeln» · 55
     Kern: alle Kapitel; Vertiefung (freiwillig, nicht in den Zeiten): Aufgaben 1d, 2d, 3d, 4d, 5d, 6d, 7d. Bewusst weggelassen: COP_max,
     Messreihen der Treibhausgase, Energiebilanz der Erde (Leitprogramm Energie), Celsius und Kelvin (5.1),
     Wirkungsgrade in Serie, Brennwert.
     Konventionen wie Themenseite 5.2: Q, m, c in J/(kg·K), ΔT, ϑ_m, L_f, L_v, η = E_nutz / E_zu, COP = Q_warm / E_el;
     c_W = 4182 J/(kg·K). Der Heizwert hat auf der Themenseite kein Formelzeichen: hier H wie in den
     Leitprogrammen Heizen und Wärmemenge. Widersprüche der Themenseite: siehe README.md.
     Zeiten (Clips 7, Leiste 13, Festhalten 5, Übungen 17 bzw. 23, drei Aufgaben 13 min; ohne Vertiefung):
     K0 15 · K1 55 · K2 55 · K3 60 · K4 55 · K5 55 · K6 50 · K7 55 · Gesamttest 40 = 440 min ≈ 9.8 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Wärme</h1>
      <p class="unter">Wärme und Temperatur, Wärmebilanz, latente Wärme und Heizkurve, Heizwert, Energiesysteme, Wärmetransport und Treibhauseffekt — mit laufenden Simulationen. Sieben Kapitel zu je 50 bis 60 Minuten, dazu Vorwissen und Gesamttest — zusammen rund zehn Lektionen; die Vertiefungsaufgaben sind freiwillig.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 5 · Teilgebiet 5.2</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Wärme und Temperatur</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Wärmebilanz</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Latente Wärme und Heizkurve</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Heizwert und Wirkungsgrad</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Energiesysteme</span></a></li></ol>
    <p class="lekt">Lektion 6</p>
    <ol><li><a href="#k6"><span class="nr">6</span><span>Wärmetransport</span></a></li></ol>
    <p class="lekt">Lektion 7</p>
    <ol><li><a href="#k7"><span class="nr">7</span><span>Treibhauseffekt</span></a></li></ol>
    <p class="lekt">Abschluss</p>
    <ol><li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li></ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 8 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen — er rechnet ein Problem vor und hält einmal an: Wie gehst du vor?</li>
          <li><b>② Tüfteln:</b> Die Simulationen laufen auf Knopfdruck. Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt; deine Antwort notierst du und vergleichst sie dann.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma; Brüche wie <code>1/2</code> und Zehnerpotenzen wie <code>2.4e-3</code> gehen auch. Richtig ist, was auf drei signifikante Stellen stimmt.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 5, Teilgebiet 5.2 Wärme</p>
        <ul>
          <li><b>K1</b> den Begriff «Wärme» bezüglich übertragener Teilchenbewegungen definieren und die Beziehung zwischen Wärme und Temperatur erklären</li>
          <li><b>K2</b> die Wärmebilanz und das thermische Gleichgewicht berechnen (mit und ohne Zustandsänderung) unter Gebrauch der Begriffe «spezifische Wärmekapazität», «Wirkungsgrad», «latente Wärme»</li>
          <li><b>K3</b> den entsprechenden Temperaturverlauf grafisch darstellen</li>
          <li><b>K4</b> die Energieerzeugung mit Hilfe des Heizwertes, unter Berücksichtigung des Wirkungsgrades, berechnen</li>
          <li><b>K5</b> das Potential der erneuerbaren Energien beschreiben und sie mit anderen Energie erzeugenden Systemen vergleichen (Wasserkraft, Windenergie, Solarenergie, Wärmepumpe, Biogas, Wärme-Kraft-Kopplungen, Kernenergie)</li>
          <li><b>K6</b> die verschiedenen Formen des Wärmetransportes unterscheiden</li>
          <li><b>K7</b> die unterschiedliche Durchlässigkeit der Atmosphäre für Licht und Wärmestrahlung und ihre Auswirkung auf den Treibhaus-Effekt beschreiben</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">5.2 Wärme</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Wärme · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Wärme und Temperatur') + k1 + band(2, 'Wärmebilanz') + k2
        + band(3, 'Latente Wärme') + k3 + band(4, 'Heizwert') + k4 + band(5, 'Energiesysteme') + k5 + band(6, 'Wärmetransport') + k6
        + band(7, 'Treibhauseffekt') + k7 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
