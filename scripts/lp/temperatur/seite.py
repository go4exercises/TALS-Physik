"""Baut leitprogramme/leitprogramm-temperatur.html aus einer Kapitelbeschreibung (seit 07.10.2026).

  python3 scripts/lp/temperatur/seite.py

Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4) zu Teilgebiet 5.1, als Kopie
von scripts/lp/hydrostatik/ entstanden: Kopf, CSS-Gerüst, Grundskript und Bausteine von dort, neu sind
Kapitel, Simulationen und Übungstypen (seite.js) und die Aufgabenbilder. Nur den SEO-Block übernimmt
das Skript aus der bestehenden Seite. Wiederholbar. Planung, Kompetenzmatrix und Entscheide: README.md.
"""
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-temperatur.html'
TS = '../themen/p5-1-temperatur.html'

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
<title>Leitprogramm Temperatur</title>
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
/* Diagramme und Szenen, Farbe = eine Bedeutung: Celsius-Temperatur Bernstein, Kelvin-Temperatur und
   absoluter Nullpunkt Grün, Temperaturdifferenz Orange, Druck Rot, Teilchen, Messkurven und Stoffe Tinte */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.sim .skala.skala-k,svg.mini .skala.skala-k{fill:var(--gruen)}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.achsname.achsname-k{fill:var(--gruen)}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.pf-linie{stroke-width:2.2;fill:none}
.pf-linie.pf-delta{stroke:var(--orange)} .pf-kopf.pf-delta{fill:var(--orange)} text.p-delta{fill:var(--orange)}
.p-c{fill:var(--bernstein)} .p-k{fill:var(--gruen)} .p-druck{fill:var(--rot)}
.p-offen{fill:none;stroke:var(--rot);stroke-width:1.8}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bt-meldung{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bt-druck{fill:var(--rot);font-family:var(--sans);font-size:17px;font-weight:700}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
.sim-aktionen .aktion.an{background:var(--gruen-hell);border-color:var(--gruen-rand)}
.box-grund{fill:var(--papier-2)} .box-rand{fill:none;stroke:var(--tinte-2);stroke-width:1.6}
.teilchen{fill:var(--tinte-2)}
.teilchen-mark{fill:var(--karte);stroke:var(--tinte);stroke-width:2} .teilchen-kern{fill:var(--tinte)}
.kurve-v{fill:none;stroke:var(--tinte);stroke-width:2.2}
.box-titel,.box-zustand{fill:var(--tinte);font-family:var(--sans);font-size:11px;font-weight:700}
.zust-fest{fill:var(--tinte-2);opacity:.5} .zust-fl{fill:var(--tinte-2);opacity:.26} .zust-gas{fill:var(--tinte-2);opacity:.08}
.zust-name{fill:var(--tinte);font-family:var(--sans);font-size:9px;font-weight:700}
.zust-zahl{fill:var(--tinte);font-family:var(--sans);font-size:8.5px}
.linie-c{stroke:var(--bernstein);stroke-width:2} .kopf-c{fill:var(--bernstein)}
.legende{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bad{fill:#5fa9c6;opacity:.3} .bad.kalt{fill:#7fa7d6;opacity:.45} .bad.oel{fill:#e3c75a;opacity:.45}
.badlinie{stroke:#3a7a96;stroke-width:1.4}
.gefaess{fill:none;stroke:var(--tinte-2);stroke-width:2;stroke-linejoin:round}
.eis{fill:#f4fbff;stroke:#9fb3c8;stroke-width:1.2} .blase{fill:none;stroke:#3a7a96;stroke-width:1.2}
.glas{fill:var(--karte);fill-opacity:.6;stroke:var(--tinte-2);stroke-width:1.6}
.rohr-linie{fill:none;stroke:var(--tinte-2);stroke-width:3}
.messgeraet{fill:var(--karte);stroke:var(--tinte);stroke-width:1.6}
.kurve-druck{fill:none;stroke:var(--rot);stroke-width:2.2} .kurve-druck.ext{stroke-dasharray:6 4}
.achse-k{stroke:var(--gruen);stroke-width:1.4}
.fuehrung{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:3 3;opacity:.7}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
svg.mini.breit{width:280px}
.kurve-mini{fill:none;stroke:var(--tinte);stroke-width:2.2}
.kurve-mini.kurve-druck{stroke:var(--rot)} .kurve-mini.kurve-k{stroke:var(--gruen)}
.kurve-mini.ext{stroke-dasharray:5 4}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:10px;font-weight:700}
.p-mini{fill:var(--tinte)}
.mini-reihe{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 6px calc(5.8em + 11px)}
table.daten{border-collapse:collapse;margin:8px 0 4px;font-family:var(--sans);font-size:.88rem}
table.daten th,table.daten td{border-bottom:1px solid var(--linie);padding:4px 10px;text-align:left}
table.daten th{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--tinte-2)}

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
  var KEY = 'leitprogramm-temperatur-v1';

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
  <p>Leitprogramm · Temperatur</p>
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.0 · Stand 7. Oktober 2026</p>
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">5.1 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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



# ------------------------------------------------------------------ Aufgabenbilder (Minigrafen in Python gerechnet)
def tief(s):
    """«p_S [hPa]» für SVG-Text: Index tiefgestellt."""
    return re.sub(r'_([A-Za-z0-9,]+)(.*)', r'<tspan dy="3" font-size="0.78em">\1</tspan><tspan dy="-3">\2</tspan>', s)


def diagramm(x0, x1, y0, y1, gx, gy, lx, ly, xname, yname, label, kurven=(), punkte=(), w=280, h=180, rechts=None):
    """Diagramm zum Ablesen: Gitter je gx/gy, beschriftet je lx/ly, Achsen am linken und unteren Rand.
    kurven: [(punkte, klasse)], punkte: [(x, y, klasse)], rechts: zweite Achse [(y, text)] mit Namen."""
    ox, oy, rr, oo = 42, h - 26, 34 if rechts else 14, 18
    X = lambda x: ox + (x - x0) / (x1 - x0) * (w - ox - rr)
    Y = lambda y: oy - (y - y0) / (y1 - y0) * (oy - oo)
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">']
    def schritte(a, b, s):
        k = math.ceil(a / s - 1e-9)
        while k * s <= b + 1e-9:
            yield round(k * s, 9)
            k += 1
    for x in schritte(x0, x1, gx):
        t.append(f'<line x1="{X(x):.1f}" y1="{oo}" x2="{X(x):.1f}" y2="{oy}" class="gitter"/>')
    for y in schritte(y0, y1, gy):
        t.append(f'<line x1="{ox}" y1="{Y(y):.1f}" x2="{X(x1):.1f}" y2="{Y(y):.1f}" class="gitter"/>')
    for x in schritte(x0, x1, lx):
        t.append(f'<text x="{X(x):.1f}" y="{oy + 13}" text-anchor="middle" class="skala">{("%g" % x).replace("-", "−")}</text>')
    for y in schritte(y0, y1, ly):
        t.append(f'<text x="{ox - 5}" y="{Y(y) + 3.5:.1f}" text-anchor="end" class="skala">{("%g" % y).replace("-", "−")}</text>')
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{X(x1) + 6:.1f}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oo - 6}" class="achse"/>')
    for pk, ck in kurven:
        t.append('<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in pk) + f'" class="kurve-mini {ck}"/>')
    for x, y, ck in punkte:
        t.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.4" class="{ck}"/>')
    if rechts:
        werte, rname = rechts
        t.append(f'<line x1="{X(x1):.1f}" y1="{oy}" x2="{X(x1):.1f}" y2="{oo - 6}" class="achse-k"/>')
        for y, s in werte:
            t.append(f'<text x="{X(x1) + 4:.1f}" y="{Y(y) + 3.5:.1f}" class="skala skala-k">{s}</text>')
        t.append(f'<text x="{w - 2}" y="{oo - 8}" text-anchor="end" class="achsname achsname-k">{rname}</text>')
    t.append(f'<text x="{X(x1) + 4:.1f}" y="{oy - 5}" text-anchor="end" class="achsname">{tief(xname)}</text>'
             f'<text x="{ox + 5}" y="{oo - 8}" class="achsname">{tief(yname)}</text></svg>')
    return ''.join(t)


def zustandsbild(smp, sdp, c0, c1, label, w=280, h=96):
    """Schiene eines Stoffes: fest (dunkel), flüssig (mittel), gasförmig (hell) über der Temperatur."""
    ox, rr = 12, 12
    X = lambda c: ox + (c - c0) / (c1 - c0) * (w - ox - rr)
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">']
    for c in range(c0, c1 + 1, 10):
        t.append(f'<line x1="{X(c):.1f}" y1="14" x2="{X(c):.1f}" y2="52" class="gitter"/>')
    t.append(f'<rect x="{ox}" y="22" width="{X(smp) - ox:.1f}" height="22" class="zust-fest"/>')
    t.append(f'<rect x="{X(smp):.1f}" y="22" width="{X(sdp) - X(smp):.1f}" height="22" class="zust-fl"/>')
    t.append(f'<rect x="{X(sdp):.1f}" y="22" width="{X(c1) - X(sdp):.1f}" height="22" class="zust-gas"/>')
    for a, b, s in ((ox, X(smp), 'fest'), (X(smp), X(sdp), 'flüssig'), (X(sdp), X(c1), 'gasförmig')):
        t.append(f'<text x="{(a + b) / 2:.1f}" y="37" text-anchor="middle" class="zust-name">{s}</text>')
    t.append(f'<line x1="{ox}" y1="52" x2="{X(c1) + 5:.1f}" y2="52" class="achse"/>')
    for c in range(c0, c1 + 1, 50):
        t.append(f'<text x="{X(c):.1f}" y="65" text-anchor="middle" class="skala">{str(c).replace("-", "−")}</text>')
    t.append(f'<text x="{w - 4}" y="82" text-anchor="end" class="achsname">ϑ [°C]</text>'
             f'<text x="{ox}" y="82" class="legende">Striche alle 10 °C</text></svg>')
    return ''.join(t)


def vmit(c):
    return math.sqrt(8 * 8.314 * (c + 273.15) / (math.pi * 0.028))


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P01 = '../themen/p0-1-vorwissen-mathematik.html'
P02 = '../themen/p0-2-vorwissen-physik.html'
P43 = '../themen/p4-3-energie.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 4.3</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Rechnen mit negativen Zahlen, eine Gerade bis zur Achse verlängern, Bewegungsenergie. Die Aggregatzustände im Teilchenmodell kennst du aus <a href="''' + P02 + '''#aggregat">Vorwissen 0.2, Aggregatzustände und Temperatur</a> — Kapitel 2 baut darauf auf.</p>
''' + test('t0', 'Vortest', 9, [
    ('0a', 3, r'Rechne: \((-18) - 7\), \(12 - (-5)\) und \(-183 + 273\). Welche Temperatur ist tiefer: \(-35\,^\circ\text{C}\) oder \(-8\,^\circ\text{C}\)?',
     r'<p>\((-18) - 7 = -25\), \(12 - (-5) = 17\), \(-183 + 273 = 90\).</p><p>\(-35\,^\circ\text{C}\) ist tiefer: Auf dem Zahlenstrahl liegt \(-35\) weiter links als \(-8\).</p><p class="komm">Falsch? Denk an den Zahlenstrahl: Minus heisst nach links, Plus nach rechts. Ein Minus vor einer Klammer mit negativer Zahl wird zum Plus.</p>', ''),
    ('0b', 3, r'Eine Gerade geht durch die Punkte \((0 \mid 600)\) und \((100 \mid 820)\). Wie gross ist ihre Steigung? Bei welchem \(x\) schneidet sie die \(x\)-Achse?',
     r'<p>Steigung \(m = \dfrac{\Delta y}{\Delta x} = \dfrac{820 - 600}{100 - 0} = 2.2\).</p><p>Die Gerade ist \(y = 2.2 \cdot x + 600\). Auf der \(x\)-Achse ist \(y = 0\): \(2.2 \cdot x + 600 = 0\), also \(x = -\dfrac{600}{2.2} \approx -273\).</p><p class="komm">Falsch? <a href="' + P02 + r'#diagramme">Vorwissen 0.2, Diagramme lesen</a> · <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umstellen</a></p>', ''),
    ('0c', 3, r'Für die Bewegungsenergie gilt \(E_\text{kin} = \tfrac{1}{2} \cdot m \cdot v^2\). Ein Ball fliegt doppelt so schnell wie vorher. Wie viel mal grösser ist seine Bewegungsenergie? In welcher Einheit misst man Energie?',
     r'<p>\(v\) verdoppelt: \(v^2\) wird \(2^2 = 4\)-mal so gross, also auch \(E_\text{kin}\). Die Einheit der Energie ist das Joule (J).</p><p class="komm">Falsch? <a href="' + P43 + r'#kinetisch">Themenseite 4.3, Kinetische Energie</a> · <a href="leitprogramm-energie.html">Leitprogramm Energie</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 6 von 9 Punkten: zuerst die Hinweise und verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
# Unterschied zur Themenseite (Animation 1): Regler in °C, Tempi in m/s, Kurve zum Ablesen, Aufträge in der Leiste.
sim1 = figur_anim('sim1', 'Stickstoffteilchen fliegen in einer Box, ein markiertes Teilchen ist schneller als das Mittel; darunter das mittlere Tempo über der Temperatur', '-4 -4 308 326',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'c', '<i>ϑ</i> Temperatur', -150, 300, 5, 150, '°C', 0) + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Temperatur</div>
          <p>Alle Stoffe bestehen aus Teilchen (Atomen oder Molekülen), die sich ständig ungeordnet bewegen: Sie fliegen umher, gleiten aneinander vorbei oder schwingen um feste Plätze. Diese Bewegung heisst <b>thermische Bewegung</b>.</p>
          <p>Die <b>Temperatur</b> ist ein Mass für die <b>mittlere Bewegungsenergie</b> der Teilchen. Je höher die Temperatur, desto schneller bewegen sich die Teilchen im Mittel.</p>
          <p>Die Temperatur ist ein <b>Mittelwert</b> über sehr viele Teilchen: Einzelne sind schneller oder langsamer, ein einzelnes Teilchen hat keine Temperatur. Sichtbar wird die Bewegung in der <b>Brown'schen Bewegung</b>: Ein kleines Tröpfchen zittert, weil unsichtbare Teilchen es von allen Seiten anstossen.</p>
          <p>Kühlt man ab, wird die Bewegung schwächer. Es gibt eine tiefste Temperatur, bei der sie minimal ist: den <b>absoluten Nullpunkt</b> bei \(-273.15\,^\circ\text{C}\) (Kapitel 3).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Bei \(0\,^\circ\text{C}\) bewegen sich die Teilchen nicht mehr.» Bei \(0\,^\circ\text{C}\) gefriert nur das Wasser; die Teilchen bewegen sich weiter. Minimal ist die Bewegung erst am absoluten Nullpunkt.</p>
          <p>«Doppelte Temperatur, doppelt so schnell.» Von \(10\,^\circ\text{C}\) auf \(20\,^\circ\text{C}\) werden Stickstoffteilchen (der Hauptteil der Luft) im Mittel nur von \(463\;\text{m/s}\) auf \(471\;\text{m/s}\) schneller. Die Celsius-Zahl verdoppelt sich, die Bewegung nicht: Der Nullpunkt der Celsius-Skala ist willkürlich (Kapitel 3), und das Tempo wächst langsamer als die Temperatur.</p>
        </div>
      </div>'''
kurve_v = [(c, vmit(c)) for c in range(-190, 301, 10)]      # Stickstoff ist unter −196 °C flüssig
auf1 = test('t1', 'Aufgaben · Kapitel 1', 15, [
    ('1a', 3, r'In einer Rauchkammer beobachtet man unter dem Mikroskop helle Rauchteilchen, die unaufhörlich zittern, obwohl die Luft in der Kammer ruhig ist. Erkläre das Zittern mit dem Teilchenmodell. Was beobachtet man, wenn man die Kammer erwärmt? Begründe.',
     r'<p>Die Rauchteilchen werden von unzähligen unsichtbaren Luftteilchen angestossen, die sich ständig ungeordnet bewegen. Weil die Stösse zufällig einmal von der einen, einmal von der anderen Seite überwiegen, zittert das Rauchteilchen auf einem Zickzackweg (Brown\'sche Bewegung).</p><p>Wärmer: Die Luftteilchen bewegen sich im Mittel schneller, die Stösse werden heftiger — das Zittern wird stärker.</p>', ''),
    ('1b', 3, r'Das Diagramm zeigt das mittlere Tempo von Stickstoffteilchen über der Temperatur. Lies es bei \(-50\,^\circ\text{C}\) und bei \(250\,^\circ\text{C}\) ab. Um wie viel Prozent ist es bei \(250\,^\circ\text{C}\) grösser? Begründe mit dem Diagramm, dass die Teilchen auch bei \(-50\,^\circ\text{C}\) nicht stillstehen.',
     r'<p>Abgelesen: rund \(410\;\text{m/s}\) bei \(-50\,^\circ\text{C}\) und rund \(630\;\text{m/s}\) bei \(250\,^\circ\text{C}\) (genauer \(411\;\text{m/s}\) und \(629\;\text{m/s}\)).</p><p>Zunahme: \(\dfrac{630\;\text{m/s} - 410\;\text{m/s}}{410\;\text{m/s}} \approx 0.54\), also rund \(54\,\%\) (mit den genaueren Werten \(53\,\%\)).</p><p>Bei \(-50\,^\circ\text{C}\) liegt die Kurve bei rund \(410\;\text{m/s}\), weit über null: Auch bei dieser Kälte fliegen die Teilchen schnell umher.</p>',
     '\n            <div class="mini-reihe">' + diagramm(-200, 300, 0, 800, 50, 100, 100, 200, 'ϑ [°C]', 'Tempo [m/s]', 'Mittleres Tempo von Stickstoff über der Temperatur (ab −190 °C, darunter ist Stickstoff flüssig): steigende, leicht gebogene Kurve, rund 411 m/s bei −50 °C, 454 m/s bei 0 °C, 629 m/s bei 250 °C', [(kurve_v, '')]) + '</div>'),
    ('1c', 3, r'Ein Glas Wasser und eine volle Badewanne haben beide \(25\,^\circ\text{C}\). In welchem der beiden bewegen sich die Wasserteilchen im Mittel heftiger? Begründe mit der Definition der Temperatur.',
     r'<p>In beiden gleich heftig. Die Temperatur misst die mittlere Bewegungsenergie der Teilchen, nicht ihre Anzahl oder die Menge Wasser. Gleiche Temperatur heisst gleiche mittlere Bewegung; in der Badewanne bewegen sich nur viel mehr Teilchen.</p>', ''),
    ('1d', 3, r'Begründe, warum es eine tiefste Temperatur gibt, aber keine höchste.',
     r'<p>Die Temperatur misst die Bewegung der Teilchen. Weniger als die kleinstmögliche Bewegung gibt es nicht: Dort liegt die tiefste Temperatur, der absolute Nullpunkt (\(-273.15\,^\circ\text{C}\)). Nach oben gibt es keine solche Grenze — die Teilchen können sich immer noch heftiger bewegen.</p>', ''),
    ('1e', 3, r'Für Stickstoff gibt eine Tabelle das mittlere Tempo der Teilchen an: \(-150\,^\circ\text{C}\): \(305\;\text{m/s}\); \(-50\,^\circ\text{C}\): \(411\;\text{m/s}\); \(50\,^\circ\text{C}\): \(494\;\text{m/s}\); \(150\,^\circ\text{C}\): \(566\;\text{m/s}\); \(250\,^\circ\text{C}\): \(629\;\text{m/s}\). Zeichne auf Papier ein Diagramm (Temperatur von \(-200\,^\circ\text{C}\) bis \(300\,^\circ\text{C}\), \(1\;\text{cm}\) für \(50\,^\circ\text{C}\); Tempo von \(0\) bis \(700\;\text{m/s}\), \(1\;\text{cm}\) für \(100\;\text{m/s}\)), trage die fünf Punkte ein und verbinde sie mit einer glatten Kurve. Lies das Tempo bei \(100\,^\circ\text{C}\) an deiner Kurve ab.',
     r'<p>Die Punkte liegen auf einer steigenden, leicht gebogenen Kurve (Bild). Jeden Punkt so eintragen: auf der Temperaturachse den Wert suchen, senkrecht hinauf bis zur Höhe des Tempos — bei \(411\;\text{m/s}\) knapp über der Linie \(400\).</p><p>Bei \(100\,^\circ\text{C}\) abgelesen: rund \(530\;\text{m/s}\) (genauer \(531\;\text{m/s}\); zählt: \(520\) bis \(540\;\text{m/s}\)). Der Wert liegt zwischen den Nachbarpunkten \(494\;\text{m/s}\) und \(566\;\text{m/s}\), knapp über ihrer Mitte (\(530\;\text{m/s}\)), weil die Kurve nach oben gewölbt ist und flacher wird.</p>'
     + '<div class="mini-reihe">' + diagramm(-200, 300, 0, 700, 50, 100, 100, 100, 'ϑ [°C]', 'Tempo [m/s]', 'Lösungsbild: fünf eingetragene Punkte des mittleren Tempos von Stickstoff bei −150, −50, 50, 150 und 250 °C, verbunden durch eine steigende, leicht gebogene Kurve von −150 °C bis 250 °C; bei 100 °C rund 531 m/s', [([(c, vmit(c)) for c in range(-150, 251, 10)], '')], [(c, vmit(c), 'p-mini') for c in (-150, -50, 50, 150, 250)]) + '</div>', ''),
])
k1 = kapitel(1, 'teilchen', 'Temperatur und Teilchenbewegung', 'K1', 45,
    r'Du definierst die Temperatur über die Bewegung der Teilchen und begründest, warum sie ein Mittelwert ist und eine untere Grenze hat.',
    ('p5-1-lp-teilchen', 'Temperatur sehen: was sich bewegt, wenn es wärmer wird'),
    sim1, ('p5-1-lp-kontrolle-teilchen', 'Kontrollfragen zur Temperatur'),
    fest1, [uebung('aussage', 'Richtig oder falsch?'), uebung('beobachtung', 'Eine Beobachtung erklären')],
    auf1, f'<a href="{TS}#definition">Themenseite 5.1, Grundbegriffe</a> · <a href="{TS}#teilchen">Temperatur und Teilchengeschwindigkeit</a> · <a href="{TS}#einstieg">Brown\'sche Bewegung</a>')

# ------------------------------------------------------------------ Kapitel 2
# Unterschied zur Themenseite (Animation 2): drei Stoffe zugleich bei derselben Temperatur, Vergleichsaufträge.
sim2 = figur_anim('sim2', 'Wasser, Brom und Essigsäure in drei Boxen bei derselben Temperatur; darunter je Stoff die Bereiche fest, flüssig und gasförmig', '-4 -4 308 262',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'c', '<i>ϑ</i> Temperatur', -20, 130, 1, 70, '°C', 0) + '\n        </div>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Aggregatzustände im Teilchenmodell</div>
          <div class="tabhuelle"><table class="gesetze">
            <tr><th>Zustand</th><th>Teilchen</th><th>Eigenschaften</th></tr>
            <tr><td>fest</td><td class="wort">an festen Plätzen, oft regelmässig angeordnet (Kristall), schwingen nur um ihre Ruhelage</td><td class="wort">formstabil, kaum verformbar</td></tr>
            <tr><td>flüssig</td><td class="wort">berühren sich, ungeordnet, lassen sich gegeneinander verschieben</td><td class="wort">nimmt die Form des Gefässes an, kaum zusammendrückbar</td></tr>
            <tr><td>gasförmig</td><td class="wort">grosse Abstände, fliegen frei, stossen nur gelegentlich zusammen</td><td class="wort">füllt jeden Raum, leicht zusammendrückbar</td></tr>
          </table></div>
          <p>Zwischen den Teilchen wirken <b>Anziehungskräfte</b>. Welcher Zustand vorliegt, hängt davon ab, ob die Bewegung der Teilchen — also die Temperatur — gegen diese Kräfte ankommt. Weil die Kräfte von Stoff zu Stoff verschieden stark sind, hat jeder Stoff eigene Schmelz- und Siedepunkte. Die Teilchen selbst bleiben dieselben.</p>
          <p>Übergänge: fest → flüssig <b>schmelzen</b> (umgekehrt <b>erstarren</b>), flüssig → gasförmig <b>verdampfen</b> (umgekehrt <b>kondensieren</b>). Schmelzen geschieht am <b>Schmelzpunkt</b>; dort bestehen fest und flüssig nebeneinander. Am <b>Siedepunkt</b> siedet die Flüssigkeit: Dampf bildet sich im ganzen Innern. Beide Punkte sind stoffspezifisch und gelten bei Normaldruck (\(1013\;\text{hPa}\)).</p>
          <p><b>Verdunsten</b> gibt es schon unter dem Siedepunkt: Einzelne besonders schnelle Teilchen verlassen die Oberfläche (Pfütze, nasses Tuch).</p>
          <p>Unter dem Schmelzpunkt ist ein Stoff fest, zwischen Schmelz- und Siedepunkt flüssig, über dem Siedepunkt gasförmig.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Vorsicht mit dem Minus: Ethanol (Schmelzpunkt \(-114\,^\circ\text{C}\)) ist bei \(-80\,^\circ\text{C}\) flüssig, denn \(-80\,^\circ\text{C}\) ist wärmer als \(-114\,^\circ\text{C}\).</p>
          <p>«Beim Verdampfen werden die Teilchen grösser.» Die Teilchen bleiben gleich; nur ihre Abstände und ihre Bewegung ändern sich.</p>
        </div>
      </div>'''
tab2 = ('\n            <div class="mini-reihe"><table class="daten"><tr><th>Stoff</th><th>Schmelzpunkt</th><th>Siedepunkt</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>\\({a}\\,^\\circ\\text{{C}}\\)</td><td>\\({b}\\,^\\circ\\text{{C}}\\)</td></tr>'
                  for n, a, b in (('Quecksilber', -39, 357), ('Ethanol', -114, 78), ('Stickstoff', -210, -196), ('Zinn', 232, 2602)))
        + '</table></div>')
auf2 = test('t2', 'Aufgaben · Kapitel 2', 15, [
    ('2a', 3, r'Du hältst eine Spritze vorne mit dem Finger zu. Ist sie mit Luft gefüllt, lässt sich der Kolben ein gutes Stück hineindrücken; ist sie mit Wasser gefüllt, fast gar nicht. Begründe mit dem Teilchenmodell.',
     r'<p>In der Luft (gasförmig) haben die Teilchen grosse Abstände: Man kann sie näher zusammenschieben. Im Wasser (flüssig) berühren sich die Teilchen schon; es bleibt kaum Platz, darum lässt es sich kaum zusammendrücken.</p>', ''),
    ('2b', 3, r'Die Tabelle nennt Schmelz- und Siedepunkte bei Normaldruck. In welchem Zustand ist jeder Stoff bei \(25\,^\circ\text{C}\)? Und bei \(-50\,^\circ\text{C}\)?',
     r'<p>Bei \(25\,^\circ\text{C}\): Quecksilber flüssig, Ethanol flüssig, Stickstoff gasförmig, Zinn fest.</p><p>Bei \(-50\,^\circ\text{C}\): Quecksilber fest (\(-50\,^\circ\text{C}\) liegt unter \(-39\,^\circ\text{C}\)), Ethanol flüssig (zwischen \(-114\,^\circ\text{C}\) und \(78\,^\circ\text{C}\)), Stickstoff gasförmig (über \(-196\,^\circ\text{C}\)), Zinn fest.</p>', tab2),
    ('2c', 3, r'Das Bild zeigt für einen Stoff, in welchem Zustand er bei welcher Temperatur ist. Lies Schmelz- und Siedepunkt ab. Welcher Stoff aus Aufgabe 2b ist es? Welche Übergänge durchläuft er, wenn man ihn von \(-150\,^\circ\text{C}\) auf \(100\,^\circ\text{C}\) erwärmt?',
     r'<p>Schmelzpunkt rund \(-115\,^\circ\text{C}\), Siedepunkt rund \(80\,^\circ\text{C}\) (abgelesen auf \(5\,^\circ\text{C}\) genau): Ethanol (\(-114\,^\circ\text{C}\) und \(78\,^\circ\text{C}\)).</p><p>Beim Erwärmen von \(-150\,^\circ\text{C}\) auf \(100\,^\circ\text{C}\): zuerst schmelzen (fest → flüssig), dann verdampfen (flüssig → gasförmig).</p>',
     '\n            <div class="mini-reihe">' + zustandsbild(-114, 78, -150, 150, 'Zustand eines Stoffes über der Temperatur von −150 °C bis 150 °C: fest bis rund −114 °C, flüssig bis rund 78 °C, darüber gasförmig') + '</div>'),
    ('2d', 3, r'Beim Kochen von Nudeln beschlägt der kalte Deckel innen mit Tropfen. Wie heisst dieser Übergang? Beschreibe, was die Wasserteilchen dabei tun.',
     r'<p>Kondensieren (gasförmig → flüssig). Die Teilchen des Wasserdampfs treffen auf den kalten Deckel und werden langsamer. Sie rücken zusammen, bleiben aneinander und am Deckel haften und bilden Tropfen.</p>', ''),
    ('2e', 3, r'Bei \(-50\,^\circ\text{C}\) ist Ethanol flüssig, Wasser aber fest — obwohl die Teilchen beider Stoffe bei derselben Temperatur dieselbe mittlere Bewegungsenergie haben. Begründe mit den Kräften zwischen den Teilchen. Was folgt daraus für die Schmelzpunkte?',
     r'<p>Zwischen Wasserteilchen wirken stärkere Anziehungskräfte als zwischen Ethanolteilchen. Bei \(-50\,^\circ\text{C}\) ist die Bewegung zu schwach, um die Wasserteilchen von ihren festen Plätzen zu lösen: Wasser ist fest. Die schwächeren Kräfte zwischen den Ethanolteilchen halten sie bei derselben Bewegung nicht mehr auf festen Plätzen; sie bleiben beieinander, lassen sich aber gegeneinander verschieben: Ethanol ist flüssig.</p><p>Daraus folgt: Je stärker die Anziehungskräfte, desto heftiger muss die Bewegung sein, bis der Stoff schmilzt — desto höher liegt der Schmelzpunkt (Wasser \(0\,^\circ\text{C}\), Ethanol \(-114\,^\circ\text{C}\)).</p>', ''),
])
k2 = kapitel(2, 'aggregat', 'Aggregatzustände im Teilchenbild', 'K1', 45,
    r'Du beschreibst fest, flüssig und gasförmig im Teilchenbild, benennst die Übergänge und bestimmst mit Schmelz- und Siedepunkt, in welchem Zustand ein Stoff bei einer bestimmten Temperatur ist.',
    ('p5-1-lp-aggregat', 'Temperatur sehen: fest, flüssig, gasförmig'),
    sim2, ('p5-1-lp-kontrolle-aggregat', 'Kontrollfragen zu den Aggregatzuständen'),
    fest2, [uebung('zustand', 'Welcher Zustand?'), uebung('uebergang', 'Welcher Übergang?')],
    auf2, f'<a href="{TS}#aggregat">Themenseite 5.1, Aggregatzustände und ihre Übergänge</a> · <a href="{P02}#aggregat">Vorwissen 0.2, Aggregatzustände und Temperatur</a>')

# ------------------------------------------------------------------ Kapitel 3
# Unterschied zur Themenseite (Animation 5): Messpunkte selbst aufnehmen, Bäder als Fixpunkte, Druck in hPa, Zielaufgaben.
sim3 = figur_anim('sim3', 'Ein Glaskolben mit Gas steht in einem Bad, ein Messgerät zeigt den Druck; darunter die Messpunkte im Druck-Temperatur-Diagramm, auf Wunsch mit der bis zum Druck null verlängerten Geraden', '-4 -4 308 364',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'c', '<i>ϑ</i> Bad', -200, 200, 5, 50, '°C', 0) + '\n        </div>',
    knoepfe('gas', 'Gas im Kolben', [('A', 'A (mehr Gas)'), ('B', 'B (weniger Gas)')], 'A'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Celsius-Skala</div>
          <p>Anders Celsius schlug 1742 eine Skala mit zwei <b>Fixpunkten</b> des Wassers vor, beide bei Normaldruck (\(1013\;\text{hPa}\)): schmelzendes Eis und siedendes Wasser, der Abstand in \(100\) gleiche Schritte geteilt. Er selbst setzte 100 beim Gefrieren und 0 beim Sieden; kurz nach seinem Tod wurde die Skala umgedreht. Heute gilt: Schmelzpunkt \(0\,^\circ\text{C}\), Siedepunkt \(100\,^\circ\text{C}\). Bei tieferem Luftdruck, etwa in den Bergen, siedet Wasser schon unter \(100\,^\circ\text{C}\); darum gehört der Normaldruck zum Fixpunkt.</p>
          <p>Praktisch, weil Wasser überall verfügbar ist — aber an einen Stoff gebunden und darum <b>willkürlich</b>: Bei \(0\,^\circ\text{C}\) hört keine Bewegung auf, und es gibt negative Celsius-Temperaturen.</p>
          <div class="titel" style="margin-top:14px">Absoluter Nullpunkt und Kelvin-Skala</div>
          <p>Bei festem Volumen nimmt der Druck eines Gases beim Abkühlen gleichmässig ab. Verlängert man die Gerade bis zum Druck null, trifft sie die Temperaturachse bei \(-273.15\,^\circ\text{C}\) — für jedes Gas und jede Gasmenge. Das gilt im Modell des idealen Gases, solange das Gas nicht flüssig wird; gemessen wird darum bei Temperaturen, bei denen es gasförmig bleibt, und die Gerade verlängert. Kälter geht es nicht: Dort liegt der <b>absolute Nullpunkt</b>, die Teilchenbewegung ist minimal. Ganz erreichen lässt er sich nie.</p>
          <p>William Thomson (Lord Kelvin) legte den Nullpunkt seiner <b>absoluten Temperaturskala</b> dorthin, mit derselben Schrittweite wie Celsius. Die Einheit ist das <b>Kelvin</b> (\(\text{K}\), ohne «Grad»), die SI-Basiseinheit der Temperatur; das Formelzeichen ist \(T\). Negative Kelvin-Temperaturen gibt es nicht. Bei festem Volumen ist der Druck eines Gases proportional zur Kelvin-Temperatur. Seit 2019 ist das Kelvin über die Boltzmann-Konstante festgelegt (\(k = 1.380649 \cdot 10^{-23}\;\text{J/K}\), ein fester Zahlenwert), und das Grad Celsius wird über das Kelvin definiert.</p>
          <p>\[ 0\;\text{K} = -273.15\,^\circ\text{C} \qquad 273.15\;\text{K} = 0\,^\circ\text{C} \]</p>
          <div class="titel" style="margin-top:14px">Anwendungen</div>
          <p><b>Celsius</b> im Alltag: Wetter, Fieber, Kochen, Heizung. <b>Kelvin</b> in Wissenschaft und Technik: wo eine Temperatur selbst als Faktor oder in einem Verhältnis steht — die mittlere Bewegungsenergie der Teilchen ist proportional zur Kelvin-Temperatur, doppelte Kelvin-Temperatur heisst doppelte mittlere Bewegungsenergie; das Tempo der Teilchen wächst dabei nur um rund \(41\,\%\) —, in den Gasgesetzen und bei sehr tiefen Temperaturen (flüssiger Stickstoff siedet bei \(77\;\text{K}\)).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Doppelt so viele Grad Celsius, doppelt so warm.» Ein Verhältnis von Celsius-Zahlen sagt nichts, weil der Celsius-Nullpunkt willkürlich liegt. Verhältnisse nur in Kelvin.</p>
          <p>«\(0\,^\circ\text{C}\) ist der Nullpunkt der Temperatur.» Es ist der Nullpunkt der Celsius-Skala. Der Nullpunkt der Temperatur liegt bei \(-273.15\,^\circ\text{C} = 0\;\text{K}\).</p>
          <p>«Grad Kelvin», «°K»: Die Einheit heisst seit 1967 nur noch Kelvin, \(273\;\text{K}\).</p>
        </div>
      </div>'''
p3 = [(0, 750), (50, 887), (100, 1025)]
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Warum wählte Celsius gerade den Schmelz- und den Siedepunkt des Wassers als Fixpunkte? Warum gehört die Angabe «bei Normaldruck» dazu? Was ist an dieser Wahl willkürlich?',
     r'<p>Wasser ist überall verfügbar, und solange Eis schmilzt oder Wasser siedet, bleibt die Temperatur fest: Die beiden Punkte lassen sich überall genau wieder herstellen.</p><p>Der Siedepunkt hängt vom Luftdruck ab (in den Bergen siedet Wasser unter \(100\,^\circ\text{C}\)); erst mit festem Druck ist der Fixpunkt eindeutig.</p><p>Willkürlich: Die Skala hängt an einem bestimmten Stoff. Bei \(0\,^\circ\text{C}\) hört die Teilchenbewegung nicht auf; es gibt auch negative Celsius-Temperaturen.</p>', ''),
    ('3b', 3, r'Das Diagramm zeigt drei Messpunkte eines Gasthermometers (Volumen fest). Bei welcher Temperatur wäre der Druck null, wenn man die Gerade verlängert? Welchen Druck erwartest du bei \(-100\,^\circ\text{C}\)?',
     r'<p>Steigung: \(\dfrac{\Delta p}{\Delta\vartheta} = \dfrac{1025\;\text{hPa} - 750\;\text{hPa}}{100\,^\circ\text{C} - 0\,^\circ\text{C}} = 2.75\;\tfrac{\text{hPa}}{^\circ\text{C}}\).</p><p>Von \(0\,^\circ\text{C}\) aus bis zum Druck null: \(\dfrac{750\;\text{hPa}}{2.75\;\text{hPa}/^\circ\text{C}} \approx 273\,^\circ\text{C}\) tiefer, also bei rund \(-273\,^\circ\text{C}\).</p><p>Bei \(-100\,^\circ\text{C}\): \(p = 750\;\text{hPa} - 100\,^\circ\text{C} \cdot 2.75\;\tfrac{\text{hPa}}{^\circ\text{C}}\) \(= 475\;\text{hPa}\). Im Diagramm: Gerade verlängern und bei \(-100\,^\circ\text{C}\) ablesen.</p>',
     '\n            <div class="mini-reihe">' + diagramm(-300, 100, 0, 1200, 50, 100, 100, 200, 'ϑ [°C]', 'p [hPa]', 'Druck eines Gases über der Temperatur: drei Messpunkte bei 0 °C (750 hPa), 50 °C (887 hPa) und 100 °C (1025 hPa), Gerade zwischen ihnen; die Achse reicht bis −300 °C', [(p3, 'kurve-druck')], [(x, y, 'p-druck') for x, y in p3]) + '</div>'),
    ('3c', 3, r'Warum beginnt die Kelvin-Skala genau bei \(-273.15\,^\circ\text{C}\)? Warum gibt es keine negativen Kelvin-Temperaturen? Was haben Celsius- und Kelvin-Skala gemeinsam?',
     r'<p>Bei \(-273.15\,^\circ\text{C}\) liegt der absolute Nullpunkt: Dort würde der Druck eines Gases null, die Teilchenbewegung ist minimal. Tiefer geht es nicht; Kelvin legte den Nullpunkt seiner Skala genau dorthin.</p><p>Weil keine Temperatur unter dem absoluten Nullpunkt liegt, gibt es keine negativen Kelvin-Werte.</p><p>Gemeinsam ist die Schrittweite: \(1\;\text{K}\) ist genau so gross wie \(1\,^\circ\text{C}\). Die Skalen sind nur gegeneinander verschoben.</p>', ''),
    ('3d', 3, r'Nenne je zwei Anwendungen, in denen man üblicherweise mit Grad Celsius und mit Kelvin misst oder rechnet. Begründe bei einer Kelvin-Anwendung, warum Celsius dort nicht taugt.',
     r'<p>Celsius: Wetterbericht, Fiebermessen, Kochen, Raumtemperatur.</p><p>Kelvin: Verhältnisse wie die mittlere Bewegungsenergie der Teilchen, Gasgesetze, Tieftemperaturphysik (flüssiger Stickstoff \(77\;\text{K}\)), Temperaturdifferenzen in Technik und Wissenschaft.</p><p>Begründung, zum Beispiel: Die mittlere Bewegungsenergie ist proportional zur Temperatur ab dem absoluten Nullpunkt. Mit Celsius-Zahlen stimmt das Verhältnis nicht, weil deren Nullpunkt willkürlich ist.</p>', ''),
])
k3 = kapitel(3, 'skalen', 'Celsius und Kelvin: Ursprung und Anwendungen', 'K2', 45,
    r'Du erklärst, wie die Celsius-Skala aus zwei Fixpunkten des Wassers entsteht, wie man den absoluten Nullpunkt findet und warum die Kelvin-Skala dort beginnt — und wo man welche Skala braucht.',
    ('p5-1-lp-skalen', 'Temperatur sehen: zwei Skalen, zwei Nullpunkte'),
    sim3, ('p5-1-lp-kontrolle-skalen', 'Kontrollfragen zu Celsius und Kelvin'),
    fest3, [uebung('eichen', 'Ein Thermometer ablesen'), uebung('nullpunkt', 'Den absoluten Nullpunkt bestimmen'), uebung('skala', 'Celsius oder Kelvin?')],
    auf3, f'<a href="{TS}#skalen">Themenseite 5.1, Celsius und Kelvin im Vergleich</a> · <a href="{TS}#nullpunkt">Woher kennt man den absoluten Nullpunkt?</a>')

# ------------------------------------------------------------------ Kapitel 4
# Unterschied zur Themenseite (Animationen 3 und 4): Messkurve mit zwei Achsen, Zeitpunkte als Regler, Leiste.
sim4 = figur('sim4', 'Messkurve einer Temperatur über der Zeit mit Celsius-Achse links und Kelvin-Achse rechts; zwei Zeitpunkte mit der Temperaturänderung in beiden Skalen', '-4 -4 308 232',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 't1', '<i>t</i><sub>1</sub> Zeitpunkt', 0, 40, 1, 5, 'min', 0) + '\n          '
    + regler('s4', 't2', '<i>t</i><sub>2</sub> Zeitpunkt', 0, 40, 1, 20, 'min', 0) + '\n        </div>\n        '
    + knoepfe('sz', 'Messkurve', [('tee', 'Tee in der Tasse'), ('winter', 'Wintertag')], 'tee'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Umrechnen</div>
          <p>\[ T\,[\text{K}] = \vartheta\,[^\circ\text{C}] + 273.15 \qquad \vartheta\,[^\circ\text{C}] = T\,[\text{K}] - 273.15 \]</p>
          <p>Die Einheit in eckigen Klammern sagt, in welcher Skala die Zahl steht; gerechnet wird mit den Zahlenwerten. Die Themenseite schreibt kurz \(T = \vartheta + 273.15\). Für einen Überschlag genügt \(273\).</p>
          <div class="titel" style="margin-top:14px">Temperaturdifferenz</div>
          <p>\[ \Delta T = T_2 - T_1 = \vartheta_2 - \vartheta_1 = \Delta\vartheta \]</p>
          <p>Beide Skalen haben dieselbe Schrittweite; die \(273.15\) steckt in beiden Werten und fällt beim Subtrahieren weg. Eine Differenz hat in °C und in K dieselbe Zahl, man gibt sie meist in Kelvin an. Abkühlen gibt ein negatives \(\Delta T\).</p>
          <div class="titel" style="margin-top:14px">Wann umrechnen?</div>
          <p>In Kelvin rechnen, wo eine Temperatur selbst als Faktor oder in einem Verhältnis steht: Die mittlere Bewegungsenergie der Teilchen ändert sich um den Faktor \(\dfrac{T_2}{T_1}\), beide in Kelvin. Bei einer Differenz muss man nicht umrechnen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Minus vergessen: \(-30\,^\circ\text{C}\) sind \(T\,[\text{K}] = -30 + 273.15 = 243.15\), also \(243.15\;\text{K}\) — nicht \(303.15\;\text{K}\).</p>
          <p>Bei einer Differenz \(273.15\) dazugezählt: Von \(20\,^\circ\text{C}\) auf \(50\,^\circ\text{C}\) sind es \(30\;\text{K}\), nicht \(303.15\;\text{K}\).</p>
          <p>Ein Verhältnis mit Celsius-Zahlen gerechnet: Von \(20\,^\circ\text{C}\) auf \(50\,^\circ\text{C}\) wächst die mittlere Bewegungsenergie um den Faktor \(\dfrac{323.15\;\text{K}}{293.15\;\text{K}} \approx 1.10\), nicht \(2.5\).</p>
        </div>
      </div>'''
kuehl = [(0, 275), (6, 289)]
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Rechne in Kelvin um: Ethanol siedet bei \(78\,^\circ\text{C}\), Eisen schmilzt bei \(1538\,^\circ\text{C}\). Rechne in Grad Celsius um: Helium siedet bei \(4.2\;\text{K}\), Trockeneis hat \(194.65\;\text{K}\).',
     r'<p>\(T\,[\text{K}] = \vartheta\,[^\circ\text{C}] + 273.15\): \(78 + 273.15 = 351.15\), also \(351.15\;\text{K}\); \(1538 + 273.15 = 1811.15\), also \(1811.15\;\text{K}\).</p><p>\(\vartheta\,[^\circ\text{C}] = T\,[\text{K}] - 273.15\): \(4.2 - 273.15 = -268.95\), also \(-268.95\,^\circ\text{C}\); \(194.65 - 273.15 = -78.5\), also \(-78.5\,^\circ\text{C}\).</p>', ''),
    ('4b', 3, r'Ein Pizzastein wird von \(21\,^\circ\text{C}\) auf \(250\,^\circ\text{C}\) erhitzt. Wie gross ist die Temperaturänderung in Kelvin? Ein Mitschüler rechnet \(523.15\;\text{K} - 21\,^\circ\text{C} = 502.15\;\text{K}\). Was ist falsch?',
     r'<p>\(\Delta T = \Delta\vartheta = \vartheta_2 - \vartheta_1\) \(= 250\,^\circ\text{C} - 21\,^\circ\text{C}\) \(= 229\,^\circ\text{C}\), also \(\Delta T = 229\;\text{K}\).</p><p>Er zieht eine Celsius-Zahl von einer Kelvin-Zahl ab — zwei verschiedene Skalen. Richtig wäre \(523.15\;\text{K} - 294.15\;\text{K} = 229\;\text{K}\).</p>', ''),
    ('4c', 3, r'Ein Datenlogger in einer Kühlbox zeichnet die Temperatur in Kelvin auf (Diagramm). Lies die Temperatur zu Beginn und nach \(6\;\text{h}\) ab und rechne beide in Grad Celsius um. Um wie viel Kelvin hat sich die Kühlbox erwärmt?',
     r'<p>Abgelesen: \(275\;\text{K}\) zu Beginn, \(289\;\text{K}\) nach \(6\;\text{h}\).</p><p>\(\vartheta\,[^\circ\text{C}] = T\,[\text{K}] - 273.15\): \(275 - 273.15 = 1.85\), also \(1.85\,^\circ\text{C}\); \(289 - 273.15 = 15.85\), also \(15.85\,^\circ\text{C}\).</p><p>\(\Delta T = 289\;\text{K} - 275\;\text{K} = 14\;\text{K}\) (gleich \(15.85\,^\circ\text{C} - 1.85\,^\circ\text{C}\)).</p>',
     '\n            <div class="mini-reihe">' + diagramm(0, 7, 270, 295, 1, 1, 1, 5, 't [h]', 'T [K]', 'Temperatur einer Kühlbox in Kelvin über der Zeit: Gerade von 275 K zu Beginn bis 289 K nach 6 h', [(kuehl, 'kurve-k')], [(0, 275, 'p-k'), (6, 289, 'p-k')]) + '</div>'),
    ('4d', 3, r'Luft in einer verschlossenen Flasche wird von \(15\,^\circ\text{C}\) auf \(90\,^\circ\text{C}\) erwärmt. Um welchen Faktor wächst die mittlere Bewegungsenergie der Luftteilchen? Warum ist \(\dfrac{90}{15} = 6\) falsch?',
     r'<p>In Kelvin: \(T_1 = 15 + 273.15 = 288.15\), \(T_2 = 90 + 273.15 = 363.15\) (in K). Faktor \(\dfrac{T_2}{T_1} = \dfrac{363.15\;\text{K}}{288.15\;\text{K}} \approx 1.26\).</p><p>Die mittlere Bewegungsenergie ist proportional zur Temperatur ab dem absoluten Nullpunkt. Der Nullpunkt der Celsius-Skala ist willkürlich; ein Verhältnis von Celsius-Zahlen hat darum keine Bedeutung.</p>', ''),
])
k4 = kapitel(4, 'umrechnen', 'Umrechnen und Temperaturdifferenz', 'K3', 45,
    r'Du rechnest Grad Celsius in Kelvin um und umgekehrt, bestimmst Temperaturdifferenzen und entscheidest, wann umgerechnet werden muss.',
    ('p5-1-lp-umrechnen', 'Temperatur sehen: von Celsius zu Kelvin und zurück'),
    sim4, ('p5-1-lp-kontrolle-umrechnen', 'Kontrollfragen zum Umrechnen'),
    fest4, [uebung('umrechnen', 'Celsius und Kelvin umrechnen'), uebung('differenz', 'Temperaturänderung'), uebung('faktor', 'Faktor der Bewegungsenergie')],
    auf4, f'<a href="{TS}#umrechnen">Themenseite 5.1, Umrechnen und Temperaturdifferenz</a> · <a href="{TS}#skalen">Celsius und Kelvin im Vergleich</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/temperatur/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">5.1 · K1 bis K3</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg und Begründungen. Erlaubt sind Taschenrechner und Formelsammlung.<br>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a> → K1 · G2 → <a href="#k2">2</a> → K1 · G3 → <a href="#k3">3</a> → K2 · G4 → <a href="#k3">3</a> → K2 (a: auch <a href="#k1">1</a>, d: auch <a href="#k4">4</a>) · G5 → <a href="#k4">4</a> → K3 · G6 → <a href="#k4">4</a> → K3 (Druck und Verhältnis in Kelvin: auch <a href="#k3">3</a>, K2)</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Warum die Temperatur beim Schmelzen und Sieden stehen bleibt (latente Wärme), und wie viel Energie das Erwärmen braucht → <a href="../themen/p5-2-waerme.html#heizkurve">Themenseite 5.2, Der Temperaturverlauf</a></li>
        <li>Wärme und Temperatur unterscheiden → <a href="../themen/p5-2-waerme.html#definition">Themenseite 5.2, Grundbegriffe</a></li>
        <li>Druck, Volumen und Temperatur eines Gases berechnen (Gasgesetze) → <a href="../themen/p5-3-waermeausdehnung.html#gasgesetz">Themenseite 5.3, Das ideale Gasgesetz</a></li>
        <li>Das mittlere Tempo wächst mit der Wurzel der Kelvin-Temperatur → <a href="{TS}#teilchen">Themenseite 5.1, Temperatur und Teilchengeschwindigkeit</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Temperatur, Version 1.0 (07.10.2026, Erprobung: unverlinkt bis nach /lp-pruefung).
     Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip → ② laufende Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF (downloads/leitprogramme/temperatur/*.tex). Quelle: scripts/lp/temperatur/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 5.1 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 die Temperatur, mit Bezug auf die Teilchenbewegung, definieren und einen Zusammenhang mit
          den Aggregatzuständen herstellen
       K2 den Ursprung und die Anwendungen der Celsius- und der Kelvin-Temperaturskala erklären
       K3 Grad Celsius in Grad Kelvin umrechnen und umgekehrt

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1 (Temperatur und Teilchenbewegung), Kap. 2 (Aggregatzustände) · Aufg. 1a–2e · G1, G2
       K2 → Kap. 3 (Celsius, absoluter Nullpunkt, Kelvin, Anwendungen) · Aufg. 3a–3d · G3, G4 (G6b Druck, Verhältnis)
       K3 → Kap. 4 (Umrechnen, Differenz, wann umrechnen) · Aufg. 4a–4d · G5, G6
     Planung: K1 enthält zwei Ideen (Temperatur als Mass der Teilchenbewegung; Aggregatzustände) und
     bekommt zwei Kapitel; K2 und K3 je eines. Ein Kapitel = eine Idee; das Teilgebiet ist klein,
     darum vier Kapitel zu je knapp einer Lektion.
     Bewusst weggelassen (Themenseite oder spätere Teilgebiete): latente Wärme und Heizkurve (5.2),
     Wärme gegen Temperatur (5.2), Gasgesetze (5.3), Wurzelgesetz des Tempos (Themenseite 5.1),
     Fahrenheit (nicht im RLP).
     Zeiten: K0 10 · K1 45 · K2 45 · K3 45 · K4 45 · Gesamttest 30 = 220 min ≈ 4.9 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Temperatur</h1>
      <p class="unter">Teilchenbewegung, Aggregatzustände, Celsius und Kelvin, Umrechnen — mit laufenden Simulationen. Vier Kapitel zu je knapp einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 5 · Teilgebiet 5.1</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Temperatur und Teilchenbewegung</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Aggregatzustände</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Celsius und Kelvin</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Umrechnen und Differenz</span></a></li></ol>
    <p class="lekt">Abschluss</p>
    <ol><li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li></ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 5 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen.</li>
          <li><b>② Tüfteln:</b> Die Teilchen laufen auf Knopfdruck; die anderen Simulationen folgen den Reglern. Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma, negative Zahlen mit Minus. Umgerechnete und abgelesene Temperaturen gelten auf 0.2 genau, der aus Messwerten bestimmte Nullpunkt auf 2 °C, alles andere auf drei signifikante Stellen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 5, Teilgebiet 5.1 Temperatur</p>
        <ul>
          <li><b>K1</b> die Temperatur, mit Bezug auf die Teilchenbewegung, definieren und einen Zusammenhang mit den Aggregatzuständen herstellen</li>
          <li><b>K2</b> den Ursprung und die Anwendungen der Celsius- und der Kelvin-Temperaturskala erklären</li>
          <li><b>K3</b> Grad Celsius in Grad Kelvin umrechnen und umgekehrt</li>
        </ul>
        <p class="rlp-fuss">Die Einheit heisst seit 1967 nur noch Kelvin, ohne «Grad» — so steht es auch auf der Themenseite. Die Themenseite <a href="''' + TS + '''">5.1 Temperatur</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Temperatur · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Teilchenbewegung') + k1 + band(2, 'Aggregatzustände') + k2
        + band(3, 'Celsius und Kelvin') + k3 + band(4, 'Umrechnen') + k4 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
