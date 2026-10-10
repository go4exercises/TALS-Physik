"""Baut leitprogramme/leitprogramm-elektrizitaet.html aus einer Kapitelbeschreibung (seit 03.10.2026).

  python3 scripts/lp/elektrizitaet/seite.py

Erstes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4), gebaut nach
dem Mathe-Vorbild scripts/lp/quadratische-funktionen/. Anders als dort steht hier alles im
Skript — Kopf, CSS, Grundskript —, nichts wird aus der bestehenden Seite gelesen. Nur den
SEO-Block übernimmt das Skript aus der Seite, damit build-seo.py ihn pflegen kann.
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach build-seo.py, Pre-Flight.
Siehe README.md.
"""
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-elektrizitaet.html'
TS = '../themen/p6-2-elektrizitaet.html'

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
<title>Leitprogramm Elektrizität</title>
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
:root{ --karte:var(--weiss); }
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --papier:#171512; --papier-2:#1f1c17; --karte:#211e19; --weiss:#211e19;
    --tinte:#f1ece1; --tinte-2:#b6ab97; --linie:#3a342a;
    --blau:#8ab6e8; --blau-hell:#1b2a3d; --blau-rand:#3f6da3;
    --gruen:#79c894; --gruen-hell:#162c1f; --gruen-rand:#3f8058;
    --lila:#c3a0ec; --lila-hell:#251b33; --lila-rand:#7d5cae;
    --orange:#e9a25e; --orange-hell:#33240f; --orange-rand:#9c6a2c;
    --rot:#ef9393; --rot-hell:#331a1a; --rot-rand:#a35050;
    --bernstein:#f0a742; --bernstein-hell:#2a2117; --bernstein-rand:#6b4a1e;
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
  --bernstein:#f0a742; --bernstein-hell:#2a2117; --bernstein-rand:#6b4a1e;
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
/* Kapitel 4 und 6 (neu 06.10.2026): Messgeräte, Kennlinie, Verbindungspunkte */
.sim svg.schalt{margin-bottom:4px}
.messgeraet{fill:var(--karte);stroke:var(--tinte);stroke-width:1.8}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:11px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
/* Lämpchen in Tinte: Bernstein gehört der Spannung */
.kennlinie{fill:none;stroke-width:2.2} .kl-a{stroke:var(--gruen)} .kl-b{stroke:var(--gruen-rand)} .kl-l{stroke:var(--tinte);stroke-dasharray:6 4}
.mp-a{fill:var(--gruen)} .mp-b{fill:var(--gruen-rand)} .mp-l{fill:var(--tinte)}
.mp-jetzt{fill:none;stroke:var(--tinte);stroke-width:1.6;stroke-dasharray:3 2}
.kl-name{font-family:var(--sans);font-size:11px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.kl-name-a{fill:var(--gruen)} .kl-name-b{fill:var(--gruen-rand)} .kl-name-l{fill:var(--tinte)}
.knoten-farbe{fill:none;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;opacity:.55}
/* Verbindungspunkte: Pluspol Bernstein (hohes Potential), Minuspol grau, dazwischen gepunktet —
   nicht Rot (Fehler), Blau (Ladung, Leistung) oder Lila (Ziel) */
.knoten-a{stroke:var(--bernstein)} .knoten-b{stroke:var(--tinte-2)} .knoten-c{stroke:var(--bernstein);stroke-dasharray:1 10;opacity:.8}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
.vorgerechnet{border-left:4px solid var(--bernstein-rand);background:var(--karte);border-radius:6px;padding:10px 14px;margin:12px 0}
.vorgerechnet .titel{font-family:var(--sans);font-weight:700;font-size:.9rem;margin-bottom:4px}
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
/* Diagramme: Farben im ganzen Leitprogramm — U Bernstein, I Orange, R Grün, Q und P Blau;
   die Energie als Fläche Bernstein-hell wie in den Clips */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.sim .normal{fill:none;stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:5 4;opacity:.7}
.hilf-text{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
/* Ziele lila gestrichelt: Grün gehört dem Widerstand */
.sim .zielkurve{fill:none;stroke:var(--lila);stroke-width:3;stroke-dasharray:7 5;opacity:.9}
.sim .zielflaeche{fill:none;stroke:var(--lila);stroke-width:2.5;stroke-dasharray:7 5}
.kurve-i{fill:none;stroke:var(--orange);stroke-width:2.6}
.kurve-p{fill:none;stroke:var(--blau);stroke-width:2.6}
.kurve-r{fill:none;stroke:var(--gruen);stroke-width:2.6}
.sim .feld{fill:var(--bernstein-hell);stroke:var(--bernstein);stroke-width:1;opacity:.9}
.flaeche-text{fill:var(--bernstein);font-family:var(--sans);font-size:12px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.p-q{fill:var(--tinte)} .p-r{fill:var(--gruen)}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bauteil{fill:var(--karte);stroke:var(--tinte);stroke-width:1.6}
.draht{fill:none;stroke:var(--tinte);stroke-width:1.6}
.quelle-lang{stroke:var(--tinte);stroke-width:2}
.quelle-kurz{stroke:var(--tinte);stroke-width:4}
.knoten{fill:var(--tinte)}
.bt-text{fill:var(--tinte);font-family:var(--sans);font-size:11px}
.bt-titel{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.balken-u1{fill:var(--bernstein)} .balken-u2{fill:var(--bernstein-rand)}
.balken-i1{fill:var(--orange)} .balken-i2{fill:var(--orange-rand)}
.leiter-l{stroke:#8a5a2b;stroke-width:2.4;fill:none}
.leiter-n{stroke:var(--blau);stroke-width:2.4;fill:none}
.leiter-pe{stroke:#4a8a2a;stroke-width:2.8;stroke-dasharray:8 5;fill:none}
.erde{stroke:var(--tinte-2);stroke-width:2}
.schutz{stroke-width:1.6}
.schutz-ein{fill:var(--karte);stroke:var(--tinte-2)}
.schutz-aus{fill:var(--rot-hell);stroke:var(--rot)}
.geraet{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.6}
.geraet-fehler{stroke:var(--rot);stroke-width:2.4}
.kurzschluss{fill:none;stroke:var(--rot);stroke-width:2.4}
.fehlerweg{fill:none;stroke:var(--rot);stroke-width:2.6;stroke-dasharray:7 4}
.mensch{fill:none;stroke:var(--tinte);stroke-width:2.4;stroke-linecap:round}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.kurve-i{stroke:var(--orange);stroke-width:2.2} .kurve-mini.kurve-r{stroke:var(--gruen);stroke-width:2.2}
svg.mini.schaltbild{width:200px} svg.mini.schaltbild.breit{width:280px}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.p-mini{fill:var(--tinte)}
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
  var KEY = 'leitprogramm-elektrizitaet-v1';

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
    if not os.path.exists(R + 'clips/sprechertext-' + datei + '.txt'):   # Clip noch nicht gebaut
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
    """Laufzeit aus den gemessenen Szenendauern im Drehbuch (seit 06.10.2026), sonst die angegebene."""
    import json, os
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips', datei + '.json')
    if os.path.exists(pfad):
        d = json.load(open(pfad, encoding='utf-8'))
        s = round(sum(x.get('dauer', 0) for x in d['szenen']))
        if s:
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">6.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


def figur(sid, label, svg_box, inhalt, hilfs=None):
    h = f'\n        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien ({hilfs})</label>' if hilfs else ''
    return f'''      <figure class="sim sim-gross" id="{sid}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="{svg_box}" role="img" aria-label="{label}"></svg>{h}
{inhalt}
      </figure>'''


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P01 = '../themen/p0-1-vorwissen-mathematik.html'
P02 = '../themen/p0-2-vorwissen-physik.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2</span><span class="zeit">≈ 15 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Vorsilben, Zehnerpotenzen, Gleichungen umstellen. Wenn das wackelt: <a href="leitprogramm-rechnen.html">Leitprogramm Rechnen und Schliessen</a>.</p>
      ''' + clipkarte('p0-2-vorsilben-ee', 'Einheiten umrechnen: Vorsilben sind Zehnerpotenzen — und die EE-Taste', '0:58') + r'''
      <div class="vorgerechnet">
        <div class="titel">Vorgerechnet: Vorsilbe, Zeit, einsetzen</div>
        <p>Wie viel Ladung fliesst, wenn \(400\;\text{mA}\) während \(3\;\text{min}\) fliessen? Die Beziehung \(Q = I \cdot t\) ist hier nur eine gegebene Rechenvorschrift — was Ladung und Strom sind, kommt in Kapitel 1.</p>
        <p>1. Vorsilbe umrechnen: \(400\;\text{mA} = 0.400\;\text{A}\). 2. Zeit in Sekunden: \(3\;\text{min} = 180\;\text{s}\). 3. Einsetzen:</p>
        <p>\[ Q = I \cdot t = 0.400\;\text{A} \cdot 180\;\text{s} = 72.0\;\text{C} \]</p>
        <p>Probe mit den Einheiten: \(\text{A} \cdot \text{s} = \text{C}\). Ohne Umrechnung käme \(400 \cdot 3 = 1200\) heraus — mit «mA·min» als Einheit, die niemand braucht.</p>
      </div>
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Rechne um: \(250\;\text{mA}\) in \(\text{A}\), \(4.7\;\text{k}\Omega\) in \(\Omega\), \(0.32\;\mu\text{C}\) in \(\text{C}\) (als Zehnerpotenz).',
     r'<p>\(0.25\;\text{A}\), \(4700\;\Omega\), \(3.2 \cdot 10^{-7}\;\text{C}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#praefixe">Vorwissen 0.2, Vorsilben</a> und der Clip oben.</p>', ''),
    ('0b', 2, r'Wie viele Sekunden sind \(15\;\text{min}\) und \(1.5\;\text{h}\)?',
     r'<p>\(15 \cdot 60\;\text{s} = 900\;\text{s}\) und \(1.5 \cdot 3600\;\text{s} = 5400\;\text{s}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#umrechnen">Vorwissen 0.2, Einheiten umrechnen</a></p>', ''),
    ('0c', 3, r'Stelle \(U = R \cdot I\) nach \(I\) und nach \(R\) um, und \(Q = I \cdot t\) nach \(t\).',
     r'<p>\(I = \dfrac{U}{R}\), \(R = \dfrac{U}{I}\), \(t = \dfrac{Q}{I}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umformen</a></p>', ''),
    ('0d', 2, r'Berechne ohne Rechner: \(\dfrac{6.4 \cdot 10^{-7}}{1.6 \cdot 10^{-19}}\).',
     r'<p>\(\dfrac{6.4}{1.6} = 4\) und \(10^{-7 - (-19)} = 10^{12}\): also \(4 \cdot 10^{12}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#potenzen">Vorwissen 0.1, Zehnerpotenzen</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1: Ladung und Stromstärke
sim1 = figur('sim1', 'Ladung Q über der Zeit t: Ursprungsgerade mit der Stromstärke I als Steigung', '-4 -4 308 268',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'I', '<i>I</i> Strom', 0, 3, 0.25, 1.25, 'A', 2) + '\n          '
    + regler('s1', 't', '<i>t</i> Zeit', 0, 10, 0.5, 3, 's', 1) + '\n        </div>',
    'Gerade für 1 A')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ladung und Stromstärke</div>
          <p>Im Atomkern sitzen die positiven Protonen, in der Hülle die negativen Elektronen. Negativ geladen ist ein Körper mit Elektronenüberschuss, positiv einer mit Elektronenmangel. Ladung wird nicht erzeugt, nur verschoben: In einem abgeschlossenen System bleibt die Summe aller Ladungen gleich.</p>
          <p>Die Elementarladung \(e\) ist ein Betrag: Ein Proton trägt \(+e\), ein Elektron \(-e\). Für \(n\) Elektronen zu viel ist \(Q = -n \cdot e\); den Betrag rechnet man mit</p>
          <p>\[ |Q| = n \cdot e, \qquad e = 1.602 \cdot 10^{-19}\;\text{C} \]</p>
          <p>Strom ist bewegte Ladung pro Zeit. Für die Ladung, die durch einen Leiterquerschnitt fliesst, und für die Stromstärke rechnet dieses Leitprogramm mit Beträgen. Für einen konstanten Strom gilt:</p>
          <p>\[ I = \frac{Q}{t}, \qquad Q = I \cdot t, \qquad 1\;\text{A} = 1\;\frac{\text{C}}{\text{s}} \]</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Zeit nicht in Sekunden umgerechnet: \(2\;\text{A}\) während \(5\;\text{min}\) sind \(Q = 2\;\text{A} \cdot 300\;\text{s} = 600\;\text{C}\), nicht \(10\;\text{C}\).</p>
          <p>Ebenso bei Akkus: \(2500\;\text{mAh} = 2.5\;\text{A} \cdot 3600\;\text{s} = 9000\;\text{C}\) (Amperestunden in Coulomb: mal \(3600\)). Das ist die Ladung, die beim Entladen durch den Stromkreis fliesst — geladen wie ein geriebener Stab ist der Akku nicht.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 3, r'Ein Kunststoffstab trägt \(Q = -4.8\;\text{nC}\). Hat er Elektronen zu viel oder zu wenig, und wie viele?',
     r'<p>Negativ: Elektronenüberschuss.</p><p>\(n = \dfrac{|Q|}{e} = \dfrac{4.8 \cdot 10^{-9}\;\text{C}}{1.602 \cdot 10^{-19}\;\text{C}} \approx 3.0 \cdot 10^{10}\) Elektronen.</p>', ''),
    ('1b', 3, r'Ein Handy-Akku ist mit \(4000\;\text{mAh}\) beschriftet: So viel Ladung kann er beim Entladen abgeben. Wie viel ist das in Coulomb, und wie lange liefert er konstant \(0.8\;\text{A}\) (idealisiert, ohne Verluste)?',
     r'<p>\(4000\;\text{mAh} = 4\;\text{Ah}\), also \(Q = I \cdot t = 4\;\text{A} \cdot 3600\;\text{s} = 14\,400\;\text{C}\).</p><p>\(t = \dfrac{Q}{I} = \dfrac{14\,400\;\text{C}}{0.8\;\text{A}} = 18\,000\;\text{s} = 5\;\text{h}\).</p><p class="komm">Diese Ladung fliesst beim Entladen durch den Stromkreis. Elektrisch geladen wie der Kunststoffstab aus 1a ist der Akku dabei nicht.</p>', ''),
    ('1c', 2, r'Hemd und Pullover sind zuerst neutral. Beim Ausziehen des Pullovers wird das Hemd negativ. Was ist mit dem Pullover passiert — und sind dabei Ladungen entstanden? (Ladung soll nur zwischen den beiden wandern.)',
     r'<p>Elektronen sind vom Pullover aufs Hemd gewandert: Der Pullover ist gleich stark positiv. Entstanden ist keine Ladung, sie wurde nur verschoben. Die Summe der beiden bleibt, was sie vorher war — hier null: \(Q_\text{Hemd} + Q_\text{Pullover} = 0\).</p>', ''),
    ('1d', 3, r'Das Diagramm zeigt die Ladung, die durch zwei Drähte A und B geflossen ist. Welche Stromstärke fliesst in A, welche in B? (Punkte auf Gitterpunkten)',
     r'<p>Die Steigung ist die Stromstärke: A: \(I = \dfrac{3\;\text{C}}{6\;\text{s}} = 0.5\;\text{A}\). B: \(I = \dfrac{6\;\text{C}}{3\;\text{s}} = 2\;\text{A}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="0.5;2" data-namen="A;B" data-farbe="kurve-i" data-fenster="8,8" data-teilung="1,1" data-punkte="6,3;3,6" data-xname="t [s]" data-yname="Q [C]" aria-label="Q-t-Diagramm mit zwei Ursprungsgeraden A und B"></svg></div>'),
])
k1 = kapitel(1, 'ladung-und-strom', 'Ladung und Stromstärke', 'K1 · K2', 40,
    r'Du beschreibst, woher elektrische Ladung kommt, rechnest mit \(|Q| = n \cdot e\) und \(I = Q/t\) und unterscheidest Ladung von Stromstärke.',
    ('p6-2-lp-ladung', 'Strom sehen: vom Elektron zum Ampere'),
    sim1, ('p6-2-lp-kontrolle-ladung', 'Kontrollfragen zu Ladung und Stromstärke'),
    fest1, [uebung('ladung', 'Ladung aus Strom und Zeit'), uebung('strom', 'Stromstärke aus Ladung und Zeit'),
            uebung('elektronen', 'Elektronen zählen')],
    auf1, f'<a href="{TS}#definition">Themenseite 6.2, Grundbegriffe</a>')

# ------------------------------------------------------------------ Kapitel 2: Spannung, Leistung, Energie
sim2 = figur('sim2', 'Leistung P über der Zeit t: die Rechteckfläche ist die Energie E', '-4 -4 308 268',
    '        ' + knoepfe('U', 'Spannung', [('12', '12 V Autobatterie'), ('230', '230 V Netz')], '230')
    + '\n        <div class="reglerfeld">\n          '
    + regler('s2', 'I', '<i>I</i> Strom', 0, 10, 0.1, 3.5, 'A', 1) + '\n          '
    + regler('s2', 't', '<i>t</i> Zeit', 0, 3, 0.25, 1.5, 'h', 2) + '\n        </div>',
    'Kurve gleicher Energie')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Spannung, Leistung, Energie</div>
          <p>Die Spannung ist die Arbeit, die an einer Ladung verrichtet wird, geteilt durch diese Ladung:</p>
          <p>\[ U = \frac{W}{Q}, \qquad 1\;\text{V} = 1\;\frac{\text{J}}{\text{C}} \]</p>
          <p>Die Leistung ist die umgesetzte Energie pro Zeit: Sie sagt, <b>wie schnell</b> Energie umgesetzt wird (Watt \(= \text{J/s}\)); die Energie sagt, <b>wie viel</b> insgesamt (Joule, Kilowattstunden). Elektrisch:</p>
          <p>\[ P = U \cdot I, \qquad E = P \cdot t, \qquad 1\;\text{kWh} = 3.6\;\text{MJ} \]</p>
          <p>\(E = P \cdot t\) gilt für eine konstant angenommene Leistung; im \(P\)-\(t\)-Diagramm ist die Energie die Fläche. Die Netzspannung ist eine Wechselspannung: Sie wechselt ständig ihre Richtung. Die Angabe \(230\;\text{V}\) ist ihr <b>Effektivwert</b> — so gross wie die Gleichspannung, die in einem Widerstand dieselbe Leistung umsetzt. Darum gilt \(P = U \cdot I\) mit \(230\;\text{V}\) für Geräte, die wie ein Widerstand wirken (Heizung, Wasserkocher, Lampe).</p>
          <p>Bei Akkus steht die Ladung, die sie beim Entladen abgeben können, in Amperestunden: \(1\;\text{V} \cdot 1\;\text{Ah} = 1\;\text{Wh} = 3600\;\text{J}\). Gerechnet wird mit einer konstant angenommenen Spannung und ohne Verluste.</p>
          <p>Strom wird nicht verbraucht: Er fliesst vollständig zur Quelle zurück. Umgesetzt wird Energie, und die zählt die Stromrechnung in Kilowattstunden.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(1500\;\text{W} \cdot 40\;\text{min}\) sind nicht \(60\,000\;\text{kWh}\). Zuerst in Kilowatt und Stunden umrechnen: \(E = 1.5\;\text{kW} \cdot \tfrac{2}{3}\;\text{h} = 1\;\text{kWh}\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Ein Velolicht-Akku ist mit \(3.7\;\text{V}\) und \(2.0\;\text{Ah}\) beschriftet. Wie viel Energie speichert er bei konstant angenommener Spannung, in Wattstunden und in Joule? Fliessen \(0.2\;\text{C}\) durch ein Bauteil, werden dort \(2.4\;\text{J}\) umgesetzt. Welche Spannung liegt am Bauteil?',
     r'<p>\(W = U \cdot Q = 3.7\;\text{V} \cdot 2.0\;\text{Ah} = 7.4\;\text{Wh}\), und mit \(1\;\text{Wh} = 3600\;\text{J}\): \(W = 26\,640\;\text{J}\).</p><p>\(U = \dfrac{W}{Q} = \dfrac{2.4\;\text{J}}{0.2\;\text{C}} = 12\;\text{V}\).</p>', ''),
    ('2b', 4, r'Eine Kochplatte am Netz (\(230\;\text{V}\)) wirkt wie ein Widerstand und zieht \(6.0\;\text{A}\). Welche Leistung nimmt sie auf? Laut Zähler hat sie in einem Monat \(13.8\;\text{kWh}\) umgesetzt: Wie viele Stunden lief sie? Was kostet das bei \(0.25\;\text{CHF/kWh}\)?',
     r'<p>\(P = U \cdot I\) \(= 230\;\text{V} \cdot 6.0\;\text{A}\) \(= 1380\;\text{W} = 1.38\;\text{kW}\).</p><p>\(E = P \cdot t\), also \(t = \dfrac{E}{P}\) \(= \dfrac{13.8\;\text{kWh}}{1.38\;\text{kW}} = 10\;\text{h}\).</p><p>\(\text{Kosten} = E \cdot \text{Preis}\) \(= 13.8\;\text{kWh} \cdot 0.25\;\text{CHF/kWh}\) \(= 3.45\;\text{CHF}\).</p><p class="komm">Die Leistung zuerst in Kilowatt: Mit \(1380\;\text{W}\) käme \(0.01\;\text{h}\) heraus.</p>', ''),
    ('2c', 2, r'Auf der Rechnung steht «Stromverbrauch». Was wird tatsächlich verbraucht?',
     r'<p>Strom wird nicht verbraucht: Was ins Gerät fliesst, fliesst wieder zurück. Umgesetzt wird Energie (in Wärme, Licht, Bewegung); bezahlt wird \(E = P \cdot t\) in Kilowattstunden.</p>', ''),
    ('2d', 3, r'Ein Toaster nimmt \(900\;\text{W}\) auf und läuft \(4\;\text{min}\), ein Laptop-Ladegerät nimmt \(60\;\text{W}\) auf und läuft \(1\;\text{h}\). Wer setzt mehr Energie um? Zeichne beide Rechtecke in ein gemeinsames \(P\)-\(t\)-Diagramm (\(t\) in \(\text{h}\), \(P\) in \(\text{W}\)) und begründe damit.',
     r'<p>Toaster: Höhe \(900\;\text{W}\), Breite \(4\;\text{min} = \tfrac{4}{60}\;\text{h} \approx 0.067\;\text{h}\). Fläche \(E = 900\;\text{W} \cdot \tfrac{1}{15}\;\text{h} = 60\;\text{Wh} = 0.060\;\text{kWh}\).</p><p>Ladegerät: Höhe \(60\;\text{W}\), Breite \(1\;\text{h}\). Fläche \(E = 60\;\text{W} \cdot 1\;\text{h} = 60\;\text{Wh} = 0.060\;\text{kWh}\).</p><p>Beide gleich viel: Das Rechteck des Toasters ist hoch und schmal, das des Ladegeräts niedrig und breit — die Flächen sind gleich gross, und es zählt die Fläche, nicht die Höhe.</p>', ''),
])
k2 = kapitel(2, 'spannung-leistung-energie', 'Spannung, Leistung und Energie', 'K2', 40,
    r'Du erklärst Spannung als Energie je Ladung und rechnest mit \(P = U \cdot I\) und \(E = P \cdot t\) — auch in Kilowattstunden.',
    ('p6-2-lp-leistung', 'Strom sehen: Leistung ist Höhe, Energie ist Fläche'),
    sim2, ('p6-2-lp-kontrolle-leistung', 'Kontrollfragen zu Spannung, Leistung und Energie'),
    fest2, [uebung('leistung', 'Leistung und Stromstärke'), uebung('energie', 'Energie in Kilowattstunden'),
            uebung('arbeit', 'Spannung als Energie je Ladung')],
    auf2, f'<a href="{TS}#leistung">Themenseite 6.2, Leistung und Energie</a>')

# ------------------------------------------------------------------ Kapitel 3: Widerstand
sim3 = figur('sim3', 'Widerstand R über der Leiterlänge l: Ursprungsgerade mit der Steigung rho durch A', '-4 -4 308 268',
    '        ' + knoepfe('m', 'Material', [('Cu', 'Kupfer'), ('Al', 'Aluminium'), ('Fe', 'Eisen'), ('Konst', 'Konstantan')], 'Al')
    + '\n        <div class="reglerfeld">\n          '
    + regler('s3', 'l', '<i>l</i> Länge', 0, 50, 1, 35, 'm', 0) + '\n          '
    + regler('s3', 'A', '<i>A</i> Querschnitt', 0.5, 4, 0.25, 1, 'mm²', 2) + '\n        </div>',
    'Kupfer, 1 mm²')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Widerstand</div>
          <p>Der Widerstand ist für jedes Bauteil definiert als \(R = \dfrac{U}{I}\) (Ohm, \(\Omega\)). Bleibt \(R\) bei jeder Spannung gleich, heisst das Bauteil ohmsch, und es gilt das ohmsche Gesetz \(U = R \cdot I\) mit festem \(R\). Wie man das misst und an der Kennlinie erkennt, zeigt Kapitel 4.</p>
          <p>Widerstand eines Leiters:</p>
          <p>\[ R = \rho \cdot \frac{l}{A} \]</p>
          <p>\(\rho\) in \(\Omega\,\text{mm}^2/\text{m}\) bei \(20\;^\circ\text{C}\): Kupfer \(0.017\), Aluminium \(0.028\), Eisen \(0.10\), Konstantan \(0.49\). Das Rechenmodell nimmt diese Temperatur an; ein heisser Draht hat einen grösseren Widerstand.</p>
          <p>\(A\) ist die Querschnittsfläche. Doppelter Querschnitt heisst halber Widerstand. Doppelter Durchmesser ist etwas anderes: Er vervierfacht die Fläche eines runden Drahts und viertelt \(R\).</p>
          <p>Auch eine Leitung ist ein Widerstand: Fliesst der Strom \(I\), liegt über ihr die Spannung \(U = R \cdot I\) — man sagt, sie fällt an der Leitung ab. Diese Spannung fehlt dem Gerät am Ende der Leitung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Bei einem Kabel mit Hin- und Rückleiter ist die Leiterlänge doppelt so gross wie die Kabellänge: \(10\;\text{m}\) Kabel heisst \(l = 20\;\text{m}\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 15, [
    ('3a', 4, r'Ein Lautsprecherkabel aus Kupfer ist \(15\;\text{m}\) lang und hat zwei Adern zu je \(0.75\;\text{mm}^2\). Welchen Widerstand hat die Leitung? Welche Spannung fällt an ihr ab, wenn \(2\;\text{A}\) fliessen?',
     r'<p>\(l = 2 \cdot 15\;\text{m} = 30\;\text{m}\).</p><p>\(R = \rho \cdot \dfrac{l}{A}\) \(= 0.017\;\dfrac{\Omega\,\text{mm}^2}{\text{m}} \cdot \dfrac{30\;\text{m}}{0.75\;\text{mm}^2}\) \(= 0.68\;\Omega\).</p><p>\(U = R \cdot I = 0.68\;\Omega \cdot 2\;\text{A} = 1.36\;\text{V}\) — so viel fehlt dem Lautsprecher.</p>', ''),
    ('3b', 3, r'Aus Konstantandraht mit \(0.5\;\text{mm}^2\) Querschnitt soll ein Messwiderstand von \(4.9\;\Omega\) werden. Wie lang muss der Draht sein? Wie gross wird \(R\), wenn man ihn halbiert?',
     r'<p>\(l = \dfrac{R \cdot A}{\rho} = \dfrac{4.9\;\Omega \cdot 0.5\;\text{mm}^2}{0.49\;\Omega\,\text{mm}^2/\text{m}} = 5\;\text{m}\).</p><p>Halb so lang: \(R = 2.45\;\Omega\) — \(R\) ist proportional zur Länge.</p>', ''),
    ('3c', 3, r'Ein runder Kupferdraht hat \(0.8\;\text{mm}\) Durchmesser und ist \(50\;\text{m}\) lang. Wie gross ist sein Widerstand?',
     r'<p>Querschnittsfläche, nicht Durchmesser: \(A = \pi \cdot r^2 = \pi \cdot (0.4\;\text{mm})^2 \approx 0.503\;\text{mm}^2\).</p><p>\(R = \rho \cdot \dfrac{l}{A}\) \(= 0.017\;\dfrac{\Omega\,\text{mm}^2}{\text{m}} \cdot \dfrac{50\;\text{m}}{0.5027\;\text{mm}^2}\) \(\approx 1.69\;\Omega\).</p><p class="komm">Mit \(0.8\;\text{mm}\) statt der Fläche gerechnet käme \(1.06\;\Omega\) heraus — falsch, weil \(\rho\) sich auf \(\text{mm}^2\) bezieht.</p>', ''),
    ('3d', 2, r'An einer Glühlampe misst man bei \(6\;\text{V}\) den Strom \(0.20\;\text{A}\). Darf man daraus schliessen, dass bei \(12\;\text{V}\) genau \(0.40\;\text{A}\) fliessen? Begründe.',
     r'<p>\(R = \dfrac{U}{I} = \dfrac{6\;\text{V}}{0.20\;\text{A}} = 30\;\Omega\) gilt nur für diesen einen Messpunkt. Der Schluss auf \(0.40\;\text{A}\) setzte ein konstantes \(R\) voraus. Beim Glühdraht wächst \(R\) mit der Temperatur, also fliesst bei \(12\;\text{V}\) weniger als \(0.40\;\text{A}\).</p>', ''),
    ('3e', 3, r'Das Diagramm zeigt den Widerstand von zwei Eisendrähten A und B (\(\rho = 0.10\;\Omega\,\text{mm}^2/\text{m}\)) über ihrer Länge. Lies für beide den Widerstand je Meter ab und bestimme daraus den Querschnitt. Welcher Draht ist dicker, und woran erkennt man das im Diagramm? (Punkte auf Gitterpunkten)',
     r'<p>Die Steigung ist der Widerstand je Meter, \(\dfrac{R}{l} = \dfrac{\rho}{A}\). A: \(\dfrac{4\;\Omega}{10\;\text{m}} = 0.4\;\Omega/\text{m}\). B: \(\dfrac{2\;\Omega}{40\;\text{m}} = 0.05\;\Omega/\text{m}\).</p><p>\(A = \dfrac{\rho}{R/l}\): A: \(\dfrac{0.10\;\Omega\,\text{mm}^2/\text{m}}{0.4\;\Omega/\text{m}} = 0.25\;\text{mm}^2\). B: \(\dfrac{0.10\;\Omega\,\text{mm}^2/\text{m}}{0.05\;\Omega/\text{m}} = 2\;\text{mm}^2\).</p><p>B ist dicker: Seine Gerade ist flacher. Bei gleichem Material heisst grösserer Querschnitt kleinerer Widerstand je Meter.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="0.4;0.05" data-namen="A;B" data-farbe="kurve-r" data-fenster="50,10" data-teilung="5,1" data-punkte="10,4;40,2" data-xname="l [m]" data-yname="R [Ω]" aria-label="R-l-Diagramm mit zwei Ursprungsgeraden A und B"></svg></div>'),
])
k3 = kapitel(3, 'widerstand', 'Der Widerstand eines Leiters', 'K2 · K3', 40,
    r'Du berechnest den Widerstand eines Leiters mit \(R = \rho \cdot l/A\) und rechnest mit \(U = R \cdot I\).',
    ('p6-2-lp-widerstand', 'Strom sehen: Länge, Querschnitt, Material'),
    sim3, ('p6-2-lp-kontrolle-widerstand', 'Kontrollfragen zum Widerstand'),
    fest3, [uebung('leiter', 'Widerstand eines Drahts'), uebung('ohm', 'Strom aus Spannung und Widerstand'),
            uebung('laenge', 'Drahtlänge für einen Widerstand')],
    auf3, f'<a href="{TS}#ohm">Themenseite 6.2, Das ohmsche Gesetz</a> · <a href="{TS}#leiter">Der Widerstand eines Leiters</a>')


# ------------------------------------------------------------------ Kapitel 4: Messen und Kennlinien (neu 06.10.2026, Test tm)
sim6 = f'''      <figure class="sim sim-gross" id="sim6">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg class="schalt" viewBox="0 0 330 150" role="img" aria-label="Stromkreis mit Quelle, Bauteil, Amperemeter und Voltmeter, je nach Wahl richtig oder falsch angeschlossen"></svg>
        <svg class="kennl" viewBox="-4 -4 308 228" role="img" aria-label="U-I-Kennlinie: eingetragene Messpunkte, I in mA nach rechts, U in V nach oben"></svg>
        <div class="sim-aktionen"><button type="button" class="aktion aktion-punkt">Messpunkt eintragen</button><button type="button" class="aktion aktion-loeschen">Punkte löschen</button></div>
        {knoepfe('bt', 'Bauteil', [('a', 'X'), ('b', 'Y'), ('l', 'Lämpchen')], 'a')}
        {knoepfe('am', 'Amperemeter', [('reihe', 'im Stromweg'), ('parallel', 'parallel zum Bauteil')], 'parallel')}
        {knoepfe('vm', 'Voltmeter', [('parallel', 'an den Anschlüssen'), ('reihe', 'im Stromweg')], 'reihe')}
        <div class="reglerfeld">
          {regler('s6', 'U', '<i>U</i> Quelle', 0, 12, 0.5, 3, 'V', 1)}
        </div>
        <p class="sim-notiz">Ideale Messgeräte: Das Voltmeter lässt keinen Strom durch, das Amperemeter hat keinen Widerstand. Kleinspannung bis \\(12\\;\\text{{V}}\\).</p>
      </figure>'''
fest6 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Messen</div>
          <p><b>Spannung</b> liegt zwischen zwei Punkten: Das Voltmeter kommt an die beiden Anschlüsse des Bauteils — parallel. <b>Stromstärke</b> ist Ladung pro Zeit durch einen Querschnitt: Der Strom muss durch das Amperemeter fliessen — es kommt in den Stromweg, in Reihe.</p>
          <p>Ideal lässt das Voltmeter keinen Strom durch, und das Amperemeter hat keinen Widerstand. Darum unterbricht ein Voltmeter im Stromweg den Kreis, und ein Amperemeter parallel zum Bauteil überbrückt es (Kurzschluss).</p>
          <p>Aus einem Messwertepaar folgt der Widerstand, mit \(I\) in Ampere:</p>
          <p>\[ R = \frac{U}{I} \]</p>
        </div>
        <div class="merk">
          <div class="titel">Kennlinie</div>
          <p>Messpunkte \((I;\ U)\) mit \(I\) nach rechts und \(U\) nach oben, Achsen mit Einheiten. Liegen sie auf einer Geraden durch den Ursprung, ist \(R\) konstant: Das Bauteil ist ohmsch, und die Steigung ist \(R\). Je steiler, desto grösser der Widerstand.</p>
          <p>Eine Glühlampe hat keine Gerade: Mit dem Strom wird der Draht heiss, und \(R = U/I\) wächst.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Milliampere nicht umgerechnet: \(7.5\;\text{V}\) und \(15\;\text{mA}\) geben \(R = \dfrac{7.5\;\text{V}}{0.015\;\text{A}} = 500\;\Omega\), nicht \(0.5\;\Omega\).</p>
          <p>Achsen vertauscht: Wer \(I\) nach oben aufträgt, liest als Steigung \(I/U\) ab — den Kehrwert von \(R\).</p>
        </div>
      </div>'''
mess_schaltung = ('<svg class="mini schaltbild" viewBox="0 0 185 112" role="img" aria-label="Messwerttabelle zu Aufgabe 4b">'
                  '<text x="6" y="16" class="mini-name">Messwerte</text>'
                  '<text x="20" y="40" class="bt-titel">U [V]</text><text x="105" y="40" class="bt-titel">I [mA]</text>'
                  '<line x1="14" y1="46" x2="170" y2="46" class="draht"/>'
                  '<text x="20" y="64" class="bt-text">2.0</text><text x="105" y="64" class="bt-text">8.0</text>'
                  '<text x="20" y="84" class="bt-text">4.0</text><text x="105" y="84" class="bt-text">16.0</text>'
                  '<text x="20" y="104" class="bt-text">6.0</text><text x="105" y="104" class="bt-text">24.0</text></svg>')
aufM = test('tm', 'Aufgaben · Kapitel 4', 11, [
    ('4a', 3, r'Zeichne ein Schaltbild: Batterie, Lampe, ein Amperemeter für den Strom durch die Lampe und ein Voltmeter für die Spannung an der Lampe. Begründe, warum jedes Messgerät so angeschlossen ist.',
     r'<p>Das Amperemeter liegt im Stromweg zwischen Batterie und Lampe (in Reihe): Der Strom durch die Lampe muss auch durch das Messgerät fliessen.</p><p>Das Voltmeter liegt an den beiden Anschlüssen der Lampe (parallel): Spannung ist eine Grösse zwischen zwei Punkten.</p><p class="komm">Falsch angeschlossen: Liegt nur das Voltmeter im Stromweg, unterbricht es den Kreis. Liegt nur das Amperemeter parallel zur Lampe, schliesst es sie kurz. Sind beide vertauscht, fliesst gar kein Strom — das Voltmeter im Stromweg unterbricht den Kreis.</p>', ''),
    ('4b', 3, r'An einem Bauteil werden diese Werte gemessen (Tabelle). Bestimme \(R\) für jedes Wertepaar. Ist das Bauteil ohmsch?',
     r'<p>\(R = \dfrac{U}{I}\) mit \(I\) in Ampere: \(\dfrac{2.0\;\text{V}}{0.0080\;\text{A}} = 250\;\Omega\), \(\dfrac{4.0\;\text{V}}{0.016\;\text{A}} = 250\;\Omega\), \(\dfrac{6.0\;\text{V}}{0.024\;\text{A}} = 250\;\Omega\).</p><p>Immer \(250\;\Omega\): \(R\) ist konstant, das Bauteil ist ohmsch. Im \(U\)-\(I\)-Diagramm liegen die Punkte auf einer Ursprungsgeraden.</p>',
     '\n            <div class="mini-reihe">' + mess_schaltung + '</div>'),
    ('4c', 3, r'Das \(U\)-\(I\)-Diagramm zeigt zwei ohmsche Widerstände A und B. Wie gross sind sie? (Punkte auf Gitterpunkten)',
     r'<p>Die Steigung ist der Widerstand: A: \(R = \dfrac{4\;\text{V}}{0.2\;\text{A}} = 20\;\Omega\). B: \(R = \dfrac{10\;\text{V}}{0.2\;\text{A}} = 50\;\Omega\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="20;50" data-namen="A;B" data-farbe="kurve-r" data-fenster="0.3,12" data-teilung="0.05,2" data-punkte="0.2,4;0.2,10" data-xname="I [A]" data-yname="U [V]" aria-label="U-I-Diagramm mit zwei Ursprungsgeraden A und B"></svg></div>'),
    ('4d', 2, r'Warum ist die \(U\)-\(I\)-Kennlinie einer Glühlampe keine Ursprungsgerade? Lässt sich \(R = U/I\) trotzdem ausrechnen?',
     r'<p>Mit dem Strom wird der Glühdraht heisser, und sein Widerstand wächst. \(R = U/I\) lässt sich für jeden Messpunkt ausrechnen, ist aber nicht konstant — die Lampe ist kein ohmsches Bauteil, und die Kennlinie krümmt sich.</p>', ''),
])
kM = kapitel(4, 'messen-und-kennlinien', 'Messen und Kennlinien', 'K2 · K3', 40,
    r'Du schliesst Voltmeter und Amperemeter richtig an, bestimmst einen Widerstand aus Messwerten und erkennst an der Kennlinie, ob ein Bauteil ohmsch ist.',
    ('p6-2-lp-messen', 'Strom sehen: messen und Kennlinien'),
    sim6, ('p6-2-lp-kontrolle-messen', 'Kontrollfragen zum Messen und zu Kennlinien'),
    fest6, [uebung('messwert', 'Widerstand aus Messwerten'), uebung('kennlinie', 'Kennlinie nutzen'), uebung('anschluss', 'Messgerät anschliessen')],
    aufM, f'<a href="{TS}#messen">Themenseite 6.2, Messen im Stromkreis</a> · <a href="{TS}#ohm">Das ohmsche Gesetz</a>')

# ------------------------------------------------------------------ Kapitel 5: Reihe und parallel (bis 06.10.2026 Kapitel 4; Test t4)
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 330 240" role="img" aria-label="Zwei Widerstände an 12 V, in Reihe oder parallel, mit Balken für die Aufteilung"></svg>
        {knoepfe('art', 'Schaltung', [('reihe', 'in Reihe'), ('parallel', 'parallel')], 'reihe')}
        <div class="reglerfeld">
          {regler('s4', 'R1', '<i>R</i>₁', 10, 500, 10, 120, 'Ω', 0)}
          {regler('s4', 'R2', '<i>R</i>₂', 10, 500, 10, 270, 'Ω', 0)}
        </div>
      </figure>'''
fest4 = r'''      <div class="tabhuelle">
        <table class="gesetze">
          <thead><tr><th></th><th>Reihenschaltung</th><th>Parallelschaltung</th></tr></thead>
          <tbody>
            <tr><td>Stromstärke</td><td>überall gleich: \(I = I_1 = I_2\)</td><td>teilt sich auf: \(I = I_1 + I_2\)</td></tr>
            <tr><td>Spannung</td><td>teilt sich auf: \(U = U_1 + U_2\)</td><td>überall gleich: \(U = U_1 = U_2\)</td></tr>
            <tr><td>Gesamtwiderstand</td><td>\(R_\text{ges} = R_1 + R_2\)</td><td>\(\dfrac{1}{R_\text{ges}} = \dfrac{1}{R_1} + \dfrac{1}{R_2}\)</td></tr>
            <tr><td>Teilerregel</td><td>\(U_1 : U_2 = R_1 : R_2\)</td><td>\(I_1 : I_2 = R_2 : R_1\)</td></tr>
          </tbody>
        </table>
      </div>
      <div class="festhalten">
        <div class="merk"><div class="titel">Merke</div><p>Der Spannungsteiler (zwei Widerstände in Reihe, Abgriff dazwischen) teilt so nur, solange am Abgriff kein weiterer Verbraucher hängt — unbelastet. In Reihe ist \(R_\text{ges}\) grösser als jeder Einzelwiderstand, parallel kleiner als der kleinste. Für zwei Widerstände parallel: \(R_\text{ges} = \dfrac{R_1 \cdot R_2}{R_1 + R_2}\). Im Haushalt sind alle Geräte parallel geschaltet.</p></div>
        <div class="warn"><div class="titel">Häufiger Fehler</div><p>Den Kehrwert vergessen: \(\dfrac{1}{20\;\Omega} + \dfrac{1}{30\;\Omega} = \dfrac{1}{12}\;\dfrac{1}{\Omega}\) ist \(\dfrac{1}{R_\text{ges}}\). Also \(R_\text{ges} = 12\;\Omega\), nicht \(0.083\;\Omega\).</p></div>
      </div>'''

def schaltbild(art, titel):
    """Kleines Schaltbild für Aufgaben: zwei Widerstände 30 Ω und 60 Ω an 9 V, in Reihe oder parallel."""
    q = ('<line x1="20" y1="50" x2="20" y2="58" class="draht"/><line x1="10" y1="58" x2="30" y2="58" class="quelle-lang"/>'
         '<line x1="15" y1="64" x2="25" y2="64" class="quelle-kurz"/><line x1="20" y1="64" x2="20" y2="72" class="draht"/>'
         '<text x="34" y="66" class="bt-text">9 V</text>')
    if art == 'reihe':
        z = ('<polyline points="20,50 20,20 50,20" class="draht"/><rect x="50" y="13" width="34" height="14" rx="2" class="bauteil"/>'
             '<line x1="84" y1="20" x2="104" y2="20" class="draht"/><rect x="104" y="13" width="34" height="14" rx="2" class="bauteil"/>'
             '<polyline points="138,20 160,20 160,100 20,100 20,72" class="draht"/>'
             '<text x="67" y="9" text-anchor="middle" class="bt-text">30 Ω</text><text x="121" y="9" text-anchor="middle" class="bt-text">60 Ω</text>')
    else:
        z = ('<polyline points="20,50 20,20 140,20" class="draht"/><polyline points="20,72 20,100 140,100" class="draht"/>'
             '<line x1="80" y1="20" x2="80" y2="43" class="draht"/><rect x="73" y="43" width="14" height="34" rx="2" class="bauteil"/><line x1="80" y1="77" x2="80" y2="100" class="draht"/>'
             '<line x1="140" y1="20" x2="140" y2="43" class="draht"/><rect x="133" y="43" width="14" height="34" rx="2" class="bauteil"/><line x1="140" y1="77" x2="140" y2="100" class="draht"/>'
             '<circle cx="80" cy="20" r="2.5" class="knoten"/><circle cx="80" cy="100" r="2.5" class="knoten"/>'
             '<text x="92" y="64" class="bt-text">30 Ω</text><text x="152" y="64" class="bt-text">60 Ω</text>')
    return (f'<svg class="mini schaltbild" viewBox="0 0 185 112" role="img" aria-label="Schaltbild {titel}">'
            f'<text x="4" y="12" class="mini-name">{titel}</text>{q}{z}</svg>')

auf4 = test('t4', 'Aufgaben · Kapitel 5', 14, [
    ('5a', 3, r'\(R_1 = 180\;\Omega\) und \(R_2 = 270\;\Omega\) liegen in Reihe an einer Quelle. Das Amperemeter zeigt \(40\;\text{mA}\). Welche Spannung liegt an jedem Widerstand, und welche Spannung hat die Quelle?',
     r'<p>In Reihe fliesst durch beide derselbe Strom: \(U_1 = I \cdot R_1 = 0.040\;\text{A} \cdot 180\;\Omega = 7.2\;\text{V}\), \(U_2 = I \cdot R_2 = 0.040\;\text{A} \cdot 270\;\Omega = 10.8\;\text{V}\).</p><p>\(U = U_1 + U_2 = 7.2\;\text{V} + 10.8\;\text{V} = 18\;\text{V}\).</p><p>Probe: \(U = I \cdot R_\text{ges} = 0.040\;\text{A} \cdot 450\;\Omega = 18\;\text{V}\).</p>', ''),
    ('5b', 3, r'Dieselben Widerstände liegen parallel an derselben Quelle. Berechne \(R_\text{ges}\), \(I_1\), \(I_2\) und \(I\).',
     r'<p>\(R_\text{ges} = \dfrac{R_1 \cdot R_2}{R_1 + R_2}\) \(= \dfrac{180\;\Omega \cdot 270\;\Omega}{450\;\Omega}\) \(= 108\;\Omega\).</p><p>\(I_1 = \dfrac{U}{R_1} = \dfrac{18\;\text{V}}{180\;\Omega} = 100\;\text{mA}\), \(I_2 = \dfrac{U}{R_2} = \dfrac{18\;\text{V}}{270\;\Omega} \approx 66.7\;\text{mA}\).</p><p>\(I = I_1 + I_2 \approx 167\;\text{mA}\). Probe: \(\dfrac{18\;\text{V}}{108\;\Omega} \approx 167\;\text{mA}\).</p>', ''),
    ('5c', 2, r'Drei gleiche Widerstände von je \(60\;\Omega\) liegen parallel. Wie gross ist \(R_\text{ges}\)? Warum ist er kleiner als jeder einzelne?',
     r'<p>\(\dfrac{1}{R_\text{ges}} = \dfrac{3}{60\;\Omega}\), also \(R_\text{ges} = 20\;\Omega\). Jeder Zweig öffnet dem Strom einen weiteren Weg — bei gleicher Spannung fliesst mehr Strom.</p>', ''),
    ('5d', 2, r'In einer alten Lichterkette in Reihe brennt eine Lampe durch: Ihr Glühdraht reisst. Warum bleibt die ganze Kette dunkel — und warum passiert das in der Wohnung nicht?',
     r'<p>In Reihe fliesst durch alle Lampen derselbe Strom; die defekte Lampe unterbricht den einzigen Weg. In der Wohnung sind die Geräte parallel: Jedes hat seinen eigenen Zweig an derselben Spannung.</p>', ''),
    ('5e', 2, r'An \(9\;\text{V}\) liegt \(R_1 = 1\;\text{k}\Omega\) in Reihe mit \(R_2\) (unbelastet: am Abgriff zwischen den beiden hängt kein weiterer Verbraucher). Über \(R_2\) sollen \(3\;\text{V}\) liegen. Wie gross muss \(R_2\) sein?',
     r'<p>\(U_1 = U - U_2 = 9\;\text{V} - 3\;\text{V} = 6\;\text{V}\), \(I = \dfrac{U_1}{R_1} = \dfrac{6\;\text{V}}{1000\;\Omega} = 6\;\text{mA}\).</p><p>\(R_2 = \dfrac{U_2}{I} = \dfrac{3\;\text{V}}{6\;\text{mA}} = 500\;\Omega\).</p>', ''),
    ('5f', 2, r'Dieselben zwei Widerstände an derselben Quelle, einmal so (A), einmal so (B). Welche Schaltung ist eine Reihen-, welche eine Parallelschaltung? In welcher fliesst der grössere Gesamtstrom, und wie gross ist er?',
     r'<p>A ist eine Reihenschaltung (ein einziger Weg), B eine Parallelschaltung (zwei Zweige zwischen denselben zwei Knoten).</p><p>A: \(R_\text{ges} = 90\;\Omega\), \(I = \dfrac{9\;\text{V}}{90\;\Omega} = 0.1\;\text{A}\). B: \(R_\text{ges} = \dfrac{30\;\Omega \cdot 60\;\Omega}{90\;\Omega} = 20\;\Omega\), \(I = \dfrac{9\;\text{V}}{20\;\Omega} = 0.45\;\text{A}\). Der grössere Strom fliesst in B.</p>',
     '\n            <div class="mini-reihe">' + schaltbild('reihe', 'A') + schaltbild('parallel', 'B') + '</div>'),
])
k4 = kapitel(5, 'reihe-und-parallel', 'Reihen- und Parallelschaltung', 'K4', 45,
    r'Du berechnest Gesamtwiderstand, Ströme und Spannungen in einfachen Reihen- und Parallelschaltungen.',
    ('p6-2-lp-schaltungen', 'Strom sehen: Reihe teilt die Spannung, parallel den Strom'),
    sim4, ('p6-2-lp-kontrolle-schaltungen', 'Kontrollfragen zu Reihe und parallel'),
    fest4, [uebung('reihe', 'Reihenschaltung'), uebung('parallel', 'Parallelschaltung'), uebung('teiler', 'Spannungsteiler')],
    auf4, f'<a href="{TS}#reihe">Themenseite 6.2, Reihenschaltung</a> · <a href="{TS}#parallel">Parallelschaltung</a> · weiterführend: <a href="{TS}#gemischt">Gemischte Schaltungen</a>')


# ------------------------------------------------------------------ Kapitel 6: Schaltungen erkennen, begründen und prüfen (neu 06.10.2026, Test te)
sim7 = f'''      <figure class="sim sim-gross ohne-hilfslinien" id="sim7">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 340 215" role="img" aria-label="Zwei Widerstände, 150 Ohm und 300 Ohm an 6 Volt, in vier verschiedenen Zeichnungen"></svg>
        <label class="hilfs-schalter"><input type="checkbox"> Verbindungspunkte färben</label>
        {knoepfe('z', 'Zeichnung', [('z1', '1'), ('z2', '2'), ('z3', '3'), ('z4', '4')], 'z1')}
        {knoepfe('antwort', 'Schaltung', [('offen', 'noch offen'), ('reihe', 'in Reihe'), ('parallel', 'parallel')], 'offen')}
      </figure>'''
fest7 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Erkennen: Verbindungen statt Lage</div>
          <p>Alle Drähte, die ohne Bauteil dazwischen zusammenhängen, bilden <b>einen</b> Verbindungspunkt — wie lang oder verwinkelt sie gezeichnet sind, spielt keine Rolle.</p>
          <p><b>Parallel:</b> Beide Widerstände verbinden dieselben zwei Verbindungspunkte. <b>In Reihe:</b> Sie teilen sich einen Verbindungspunkt, an dem sonst nichts hängt.</p>
        </div>
        <div class="merk">
          <div class="titel">Begründen und prüfen</div>
          <p><b>Ladung bleibt erhalten:</b> Was in eine Verzweigung hineinfliesst, fliesst wieder hinaus. Parallel \(I = I_1 + I_2\); in Reihe überall derselbe Strom.</p>
          <p><b>Energiebilanz:</b> Die Quelle gibt jedem Coulomb die Energie \(U \cdot 1\;\text{C}\) mit, und die Widerstände geben sie zusammen ab: in Reihe \(U = U_1 + U_2\); parallel liegt an jedem Zweig die ganze Spannung.</p>
          <p><b>Proben:</b> Summen der Ströme oder Spannungen nachrechnen; parallel muss \(R_\text{ges}\) kleiner sein als der kleinste Zweigwiderstand.</p>
        </div>
        <div class="warn">
          <div class="titel">Drei Fehlvorstellungen</div>
          <p>«Die Quelle liefert immer denselben Strom»: Nein — der Strom hängt vom Widerstand ab; ein zusätzlicher Zweig parallel vergrössert ihn.</p>
          <p>«Am Widerstand wird Strom verbraucht»: Nein — umgesetzt wird Energie; der Strom fliesst vollständig zurück.</p>
          <p>«Der Strom nimmt nur den kleinsten Widerstand»: Nein — durch jeden Zweig fliesst \(U/R\), durch den kleineren nur mehr.</p>
        </div>
      </div>'''
ungewohnt = ('<svg class="mini schaltbild" viewBox="0 0 200 120" role="img" aria-label="Ungewohnt gezeichnete Schaltung aus 40 Ohm und 120 Ohm an 12 Volt">'
             '<line x1="20" y1="20" x2="20" y2="50" class="draht"/><line x1="10" y1="50" x2="30" y2="50" class="quelle-lang"/>'
             '<line x1="15" y1="58" x2="25" y2="58" class="quelle-kurz"/><line x1="20" y1="58" x2="20" y2="100" class="draht"/>'
             '<text x="28" y="82" class="bt-text">12 V</text>'
             '<polyline points="20,20 70,20" class="draht"/><rect x="70" y="13" width="40" height="14" rx="2" class="bauteil"/>'
             '<text x="90" y="9" text-anchor="middle" class="bt-text">40 Ω</text>'
             '<polyline points="110,20 180,20 180,100 20,100" class="draht"/>'
             '<polyline points="45,20 45,42 140,42 140,55" class="draht"/><rect x="134" y="55" width="12" height="30" rx="2" class="bauteil"/>'
             '<text x="128" y="74" text-anchor="end" class="bt-text">120 Ω</text><polyline points="140,85 140,100" class="draht"/>'
             '<circle cx="45" cy="20" r="2.5" class="knoten"/><circle cx="140" cy="100" r="2.5" class="knoten"/></svg>')
aufE = test('te', 'Aufgaben · Kapitel 6', 11, [
    ('6a', 3, r'Die Schaltung im Bild ist ungewohnt gezeichnet. Zeichne sie so neu, dass man die Schaltungsart sofort sieht. Wie ist sie geschaltet? Berechne die Ströme und \(R_\text{ges}\).',
     r'<p>Parallel: Beide Widerstände beginnen am Verbindungspunkt beim Pluspol (der Draht zum \(120\text{-}\Omega\)-Widerstand zweigt oben links ab) und enden am Draht zum Minuspol.</p><p>\(I_1 = \dfrac{12\;\text{V}}{40\;\Omega} = 0.30\;\text{A}\), \(I_2 = \dfrac{12\;\text{V}}{120\;\Omega} = 0.10\;\text{A}\), \(I = I_1 + I_2 = 0.40\;\text{A}\).</p><p>\(R_\text{ges} = \dfrac{U}{I} = \dfrac{12\;\text{V}}{0.40\;\text{A}} = 30\;\Omega\) — kleiner als \(40\;\Omega\), wie es parallel sein muss.</p>',
     '\n            <div class="mini-reihe">' + ungewohnt + '</div>'),
    ('6b', 3, r'Jemand rechnet für \(120\;\Omega\) und \(60\;\Omega\) parallel an \(12\;\text{V}\): «\(R_\text{ges} = 120\;\Omega + 60\;\Omega = 180\;\Omega\), also \(I = \dfrac{12\;\text{V}}{180\;\Omega} \approx 66.7\;\text{mA}\).» Finde den Fehler, rechne richtig und prüfe mit einer Probe.',
     r'<p>Addiert wurden die Widerstände wie in Reihe. Parallel addieren sich die Kehrwerte: \(R_\text{ges} = \dfrac{120\;\Omega \cdot 60\;\Omega}{180\;\Omega} = 40\;\Omega\), also \(I = \dfrac{12\;\text{V}}{40\;\Omega} = 0.30\;\text{A}\).</p><p>Probe: \(I_1 = \dfrac{12\;\text{V}}{120\;\Omega} = 0.10\;\text{A}\), \(I_2 = \dfrac{12\;\text{V}}{60\;\Omega} = 0.20\;\text{A}\), Summe \(0.30\;\text{A}\). Und \(40\;\Omega\) ist kleiner als \(60\;\Omega\), der kleinste Zweig.</p><p class="komm">Schon die Plausibilität verrät den Fehler: Parallel kann \(R_\text{ges}\) nicht grösser sein als ein Zweig.</p>', ''),
    ('6c', 3, r'\(R_1 = 220\;\Omega\) und \(R_2 = 330\;\Omega\) liegen parallel an \(6.6\;\text{V}\). Jemand notiert als Messwerte: \(I_1 = 30\;\text{mA}\), \(I_2 = 20\;\text{mA}\), Gesamtstrom \(I = 60\;\text{mA}\). Prüfe die drei Werte mit zwei Proben. Welcher Wert kann nicht stimmen, und wie gross muss er sein?',
     r'<p>Probe mit \(I = \dfrac{U}{R}\) für jeden Zweig: \(\dfrac{6.6\;\text{V}}{220\;\Omega} = 30\;\text{mA}\) und \(\dfrac{6.6\;\text{V}}{330\;\Omega} = 20\;\text{mA}\) — beide Zweigströme stimmen.</p><p>Probe Ladungserhaltung: \(I = I_1 + I_2 = 30\;\text{mA} + 20\;\text{mA} = 50\;\text{mA}\). Der Gesamtstrom \(60\;\text{mA}\) kann nicht stimmen: Was in die Verzweigung hineinfliesst, fliesst wieder hinaus.</p><p class="komm">Gegenprobe: \(R_\text{ges} = \dfrac{6.6\;\text{V}}{0.050\;\text{A}} = 132\;\Omega\), kleiner als \(220\;\Omega\), wie es parallel sein muss.</p>', ''),
    ('6d', 2, r'«Wenn ich ein zweites Gerät parallel einstecke, bleibt der Strom aus der Steckdose gleich; er verteilt sich nur auf zwei Geräte.» Stimmt das? Begründe.',
     r'<p>Nein. Jedes Gerät liegt an der vollen Netzspannung und nimmt seinen Strom \(I = U/R\) auf, unabhängig vom anderen. Der Strom aus der Steckdose ist die Summe: Mit dem zweiten Gerät wird er grösser. Die Quelle liefert nicht immer denselben Strom.</p>', ''),
])
kE = kapitel(6, 'schaltungen-erkennen', 'Schaltungen erkennen, begründen und prüfen', 'K4 · K1 · K2', 40,
    r'Du erkennst Reihe und parallel an den Verbindungen, auch in ungewohnten Zeichnungen, begründest Strom- und Spannungsaufteilung mit Ladungserhaltung und Energiebilanz und prüfst Ergebnisse mit Proben.',
    ('p6-2-lp-erkennen', 'Strom sehen: Verbindungen zählen, nicht die Lage'),
    sim7, ('p6-2-lp-kontrolle-erkennen', 'Kontrollfragen zum Erkennen und Prüfen'),
    fest7, [uebung('erkennen', 'Reihe oder parallel?'), uebung('knoten', 'Ströme an der Verzweigung'), uebung('masche', 'Spannungen in der Schaltung')],
    aufE, f'<a href="{TS}#reihe">Themenseite 6.2, Reihenschaltung</a> · <a href="{TS}#parallel">Parallelschaltung</a> · weiterführend: <a href="{TS}#gemischt">Gemischte Schaltungen</a>')

# ------------------------------------------------------------------ Kapitel 7: Gefahren und Schutz (bis 06.10.2026 Kapitel 5; Test t5)
sim5 = f'''      <figure class="sim sim-gross" id="sim5">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 320 222" role="img" aria-label="Stromkreis mit Leitungsschutzschalter, FI-Schutzschalter und Gerät; je nach Fall Mensch, Schutzleiter oder Kurzschluss"></svg>
        {knoepfe('fall', 'Fall', [('normal', 'Normalbetrieb'), ('koerper', 'Mensch am Gehäuse'), ('pe', 'Gehäuse am Schutzleiter'), ('kurz', 'Kurzschluss L–N')], 'normal')}
        <div class="reglerfeld rk-zeile" hidden>
          {regler('s5', 'RK', '<i>R</i><sub>K</sub> Körper', 500, 10000, 100, 2500, 'Ω', 0)}
        </div>
      </figure>'''
fest5 = r'''      <div class="tabhuelle">
        <table class="gesetze">
          <thead><tr><th>Einrichtung</th><th>schützt</th><th>misst / überwacht</th><th>schaltet ab bei</th></tr></thead>
          <tbody>
            <tr><td>FI-Schutzschalter</td><td class="wort">Menschen (zusätzlich)</td><td class="wort">Differenz zwischen Hin- und Rückstrom</td><td class="wort">muss ab \(30\;\text{mA}\) Fehlerstrom auslösen (spätestens nach \(300\;\text{ms}\), ab dem Doppelten nach \(150\;\text{ms}\), ab dem Fünffachen nach \(40\;\text{ms}\)); über \(15\;\text{mA}\) darf er schon, bis \(15\;\text{mA}\) löst er nicht aus. Gilt für den üblichen unverzögerten FI am Netz.</td></tr>
            <tr><td>Schutzleiter (PE)</td><td class="wort">Menschen</td><td class="wort">schaltet nicht — führt den Fehlerstrom zur Quelle zurück</td><td class="wort">—</td></tr>
            <tr><td>Leitungsschutzschalter, z. B. B13</td><td class="wort">die Leitung</td><td class="wort">Strom in der Leitung</td><td class="wort">Überlast: thermisch. Deutlich über \(13\;\text{A}\) (ab rund dem \(1.45\)-Fachen) je nach Höhe nach Sekunden bis zu einer Stunde; knapp darüber erst nach langer Zeit. Kurzschluss: magnetisch, sofort — bei B13 sicher ab dem Fünffachen, \(65\;\text{A}\).</td></tr>
            <tr><td>Schutzklasse II</td><td class="wort">Menschen</td><td class="wort">schaltet nicht — doppelte oder verstärkte Isolierung</td><td class="wort">—</td></tr>
          </tbody>
        </table>
      </div>
      <div class="festhalten">
        <div class="merk"><div class="titel">Gefahr</div><p>Gefährlich ist der Strom durch den Körper, \(I_\text{K} = \dfrac{U}{R_\text{K}}\), und wie lange er wirkt. Muskeln verkrampfen, über das Herz kann Netzstrom Kammerflimmern auslösen.</p><p>Der Körperwiderstand \(R_\text{K}\) ist keine feste Zahl: Er sinkt mit Nässe und mit steigender Spannung, weil die Haut durchschlägt. Für den Körper allein ist am Netz mit \(1\) bis \(2\;\text{k}\Omega\) zu rechnen, bei Kleinspannung mit einigen \(\text{k}\Omega\). Fliesst der Strom über Schuhe und Boden zur Erde, kommt deren Widerstand dazu; Körper und Boden zusammen können dann einige \(\text{k}\Omega\) haben — verlassen kann man sich darauf nicht.</p><p>Auch eine kleine Spannung kann gefährlich sein: Überbrückt ein Werkzeug, ein Ring oder ein Kabel die beiden Pole einer Batterie (<b>Kurzschluss</b>), begrenzt fast nur der kleine Widerstand des Metalls den Strom. Bei einer Autobatterie fliessen dann Hunderte Ampere; das Metall glüht, es gibt Funken und Verbrennungen.</p></div>
        <div class="merk"><div class="titel">Der Fehlerstrom fliesst im Kreis</div><p>Die Quelle (Transformator) ist geerdet. Berührt der Aussenleiter ein Gehäuse mit Schutzleiter, fliesst der Fehlerstrom: Quelle → Aussenleiter L → Gehäuse → Schutzleiter PE → zurück zur Quelle. Die \(2\;\Omega\) im Modell sind der Widerstand dieser ganzen Schleife. Fehlt der Schutzleiter, schliesst sich der Kreis über den Menschen und den Boden zur geerdeten Quelle.</p><p>Beide Wege umgehen den Neutralleiter. Darum fehlt der Strom auf dem Rückweg, und der FI sieht eine Differenz.</p></div>
        <div class="warn"><div class="titel">Häufiger Fehler</div><p>«Die Sicherung schützt mich.» Ein Leitungsschutzschalter B13 bemerkt \(200\;\text{mA}\) durch einen Menschen nicht. Und \(30\;\text{mA}\) ist keine Grenze für ungefährlichen Strom — der FI ist zusätzlicher Schutz.</p></div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 7', 15, [
    ('7a', 3, r'Jemand mit feuchter Haut (\(R_\text{K} = 1.5\;\text{k}\Omega\)) berührt ein defektes Gehäuse unter \(230\;\text{V}\). Wie gross ist der Körperstrom? Was tun ein FI (\(30\;\text{mA}\), unverzögert) und ein Leitungsschutzschalter B13?',
     r'<p>\(I_\text{K} = \dfrac{U}{R_\text{K}} = \dfrac{230\;\text{V}}{1500\;\Omega} \approx 153\;\text{mA}\) — lebensgefährlich.</p><p>Das ist mehr als das Fünffache von \(30\;\text{mA}\): Der FI muss spätestens nach \(40\;\text{ms}\) trennen. Der Leitungsschutzschalter bemerkt \(0.15\;\text{A}\) neben seinen \(13\;\text{A}\) nicht.</p>', ''),
    ('7b', 2, r'Rechenmodell: Wie gross wäre der Strom durch einen Körper mit \(R_\text{K} = 5\;\text{k}\Omega\) (trockene Hände) zwischen den Polen einer \(12\text{-V}\)-Autobatterie? Warum ist die Batterie trotzdem nicht harmlos?',
     r'<p>\(I_\text{K} = \dfrac{U}{R_\text{K}} = \dfrac{12\;\text{V}}{5000\;\Omega} = 2.4\;\text{mA}\) — klein, weil die Spannung klein ist. Das ist eine Rechnung mit einem angenommenen Widerstand, keine Erlaubnis zum Anfassen.</p><p>Die Gefahr liegt woanders: Die Batterie kann sehr grosse Ströme liefern. Überbrückt ein Werkzeug, ein Ring oder ein Uhrband die Pole, fliessen Hunderte Ampere durch das Metall. Es glüht, es gibt Funken und Lichtbogen und schwere Verbrennungen.</p>', ''),
    ('7c', 2, r'Welche Einrichtung vergleicht Hin- und Rückstrom? Welche überwacht den Strom in der Leitung selbst? Welche schaltet gar nicht ab, sondern leitet ab?',
     r'<p>Der FI-Schutzschalter vergleicht Hin- und Rückstrom (er schützt Menschen). Der Leitungsschutzschalter überwacht den Strom selbst (er schützt die Leitung). Der Schutzleiter führt einen Fehlerstrom zur Quelle zurück, damit er gross wird und abgeschaltet wird.</p>', ''),
    ('7d', 2, r'Jemand steht auf einem isolierenden Boden und fasst mit der einen Hand den Aussenleiter, mit der anderen den Neutralleiter an. Schützt ihn der FI? Begründe.',
     r'<p>Nein. Der Strom fliesst über den Aussenleiter durch den Körper und über den Neutralleiter zurück: Hin- und Rückstrom sind gleich, der FI sieht keine Differenz. Für den FI sieht der Mensch aus wie ein Gerät.</p><p class="komm">Darum ist der FI ein zusätzlicher Schutz und keine Garantie.</p>', ''),
    ('7e', 3, r'An einem Gerät ohne Schutzleiter werden im Fehlerfall diese Ströme gemessen (Bild). Wie gross ist der Fehlerstrom, wohin fliesst er, und was tut ein FI mit \(30\;\text{mA}\)?',
     r'<p>\(\Delta I = I_\text{L} - I_\text{N}\) \(= 8.88\;\text{A} - 8.70\;\text{A}\) \(= 0.18\;\text{A} = 180\;\text{mA}\). Er fehlt auf dem Rückweg, fliesst also an N vorbei — hier über den Menschen am Gehäuse und den Boden zur geerdeten Quelle.</p><p>\(180\;\text{mA}\) ist mehr als das Fünffache von \(30\;\text{mA}\) (\(150\;\text{mA}\)): Ein unverzögerter FI muss spätestens nach \(40\;\text{ms}\) trennen.</p>',
     '\n            <div class="mini-reihe"><svg class="mini schaltbild breit" viewBox="0 0 240 120" role="img" aria-label="Aussenleiter mit 8.88 A hin, Neutralleiter mit 8.70 A zurück, ein Mensch berührt das Gehäuse und steht auf der Erde">'
     '<text x="4" y="24" class="bt-titel">L</text><text x="4" y="54" class="bt-titel">N</text>'
     '<line x1="16" y1="20" x2="170" y2="20" class="leiter-l"/><line x1="16" y1="50" x2="170" y2="50" class="leiter-n"/>'
     '<text x="60" y="15" class="bt-text">hin 8.88 A</text><text x="60" y="45" class="bt-text">zurück 8.70 A</text>'
     '<rect x="170" y="10" width="54" height="50" rx="5" class="geraet geraet-fehler"/><text x="197" y="39" text-anchor="middle" class="bt-text">Gerät</text>'
     '<line x1="10" y1="112" x2="232" y2="112" class="erde"/>'
     '<circle cx="186" cy="80" r="6" class="mensch"/><polyline points="186,86 186,100 180,111" class="mensch"/><polyline points="186,100 192,111" class="mensch"/><polyline points="186,90 196,86 202,60" class="mensch"/></svg></div>'),
    ('7f', 3, r'Ein Wasserkocher hat ein Metallgehäuse und einen Stecker mit Schutzleiterkontakt. Eine Bohrmaschine hat ein Kunststoffgehäuse, das Doppelquadrat-Symbol (Schutzklasse II) und einen Stecker ohne Schutzleiterkontakt. In beiden Geräten versagt an einer Stelle die Isolierung des Aussenleiters. Beurteile für beide: Stromweg → Schutzeinrichtung → verbleibende Gefahr.',
     r'<p>Wasserkocher: Der Aussenleiter berührt das Metallgehäuse. Der Fehlerstrom fliesst über das Gehäuse und den Schutzleiter zur Quelle zurück; die Schleife hat nur wenige Ohm, der Strom ist sehr gross. Der LS trennt magnetisch (bei B13 sicher ab \(65\;\text{A}\)), und der FI spricht an, weil der Strom auf dem Neutralleiter fehlt. Verbleibende Gefahr: Ist der Schutzleiter unterbrochen, steht das Gehäuse unter Spannung, und nur der FI schützt noch.</p><p>Bohrmaschine: Hinter der ersten Isolierung liegt eine zweite (doppelte oder verstärkte Isolierung). Ein einzelner Fehler setzt das berührbare Gehäuse nicht unter Spannung; es fliesst kein Fehlerstrom, und nichts muss abschalten. Darum braucht sie keinen Schutzleiter. Verbleibende Gefahr: Ist das Gehäuse beschädigt oder dringt Wasser ein, hilft die Isolierung nicht mehr; dann bleibt der FI.</p>', ''),
])
k5 = kapitel(7, 'gefahren-und-schutz', 'Gefahren und Schutzmassnahmen', 'K5', 45,
    r'Du zeigst auf, warum Strom durch den Körper gefährlich ist, ordnest FI-Schutzschalter, Schutzleiter, Leitungsschutzschalter und Schutzklasse II ihrer Schutzwirkung zu und beurteilst Alltagsfälle mit ihren Grenzen.',
    ('p6-2-lp-gefahren', 'Strom sehen: wer misst was, wer trennt wann'),
    sim5, ('p6-2-lp-kontrolle-gefahren', 'Kontrollfragen zu Gefahren und Schutz'),
    fest5, [uebung('koerperstrom', 'Körperstrom und FI'), uebung('schutz', 'Was schützt hier?')],
    auf5, f'<a href="{TS}#gefahren">Themenseite 6.2, Gefahren des elektrischen Stroms</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/elektrizitaet/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">6.2 · K1–K5</span><span class="zeit">≈ 25 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel: G1 → <a href="#k1">1</a> · G2, G3 → <a href="#k2">2</a> · G4 → <a href="#k3">3</a> · G5 → <a href="#k4">4</a> · G6 → <a href="#k5">5</a>, <a href="#k6">6</a> · G7 → <a href="#k7">7</a></p>
        </div>
      </div>
    </section>'''

weiter = f'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <p class="komm">Freiwillig zum Nachschlagen: Das alles steht auf der Themenseite 6.2, der Gesamttest setzt es nicht voraus.</p>
      <ul>
        <li>Schaltungen: <a href="{TS}#gemischt">gemischte Schaltungen</a>, <a href="{TS}#knoten-maschen">Knoten- und Maschenregel allgemein</a>, <a href="{TS}#spannungsteiler-belastet">belasteter Spannungsteiler</a>, <a href="{TS}#leistung-schaltung">Leistung in der Schaltung</a></li>
        <li>Messen und Kennlinien: <a href="{TS}#messfehler">Messgeräte, die den Kreis verändern</a>, <a href="{TS}#kennlinien">Glühlampe und Heissleiter (NTC)</a></li>
        <li>Energie: <a href="{TS}#wirkungsgrad">Wirkungsgrad</a>, <a href="{TS}#leitungsverluste">Leitungsverluste und Hochspannung</a> (den Spannungsfall an der Leitung rechnet Kapitel 3)</li>
        <li>Gefahren: <a href="{TS}#gefahr-erde">Stromweg über die Erde</a>, <a href="{TS}#gefahr-fi-grenzen">Grenzen des FI</a>, <a href="{TS}#gefahr-alltag">weitere Alltagsfälle</a></li>
        <li><a href="{TS}#definition">Coulomb-Gesetz</a>; <a href="{TS}#wechselstrom">Wechselspannung und Effektivwert</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Elektrizität, Fassung 2.0 (06.10.2026; 1.0 am 03.10.2026 nach /lp-pruefung freigeschaltet, 1.1 am 04.10.2026). Erstes Physik-
     Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel ① Einführungsclip →
     ② Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit
     Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als PDF
     (downloads/leitprogramme/elektrizitaet/*.tex). Quelle: scripts/lp/elektrizitaet/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 6.2 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 die Beschaffenheit von elektrischen Ladungen beschreiben (Ursprung, Einheit, Elementarladung)
       K2 die wichtigsten physikalischen Grössen definieren und charakterisieren (Ladung, Spannung,
          Stromstärke, Energie, Leistung)
       K3 den Widerstand eines Leiters berechnen
       K4 Berechnungen in einfachen seriellen oder parallelen Schaltkreisen von Widerständen durchführen
       K5 die wesentlichen Gefahren der Elektrizität, inklusive entsprechender Schutzmassnahmen, aufzeigen

     Fassung 2.0 (06.10.2026) nach TODO-E: sieben Fachkapitel. Neu Kapitel 4 «Messen und Kennlinien»
     (sim6, Test tm) und Kapitel 6 «Schaltungen erkennen, begründen und prüfen» (sim7, Test te); die
     bisherigen Kapitel 4 und 5 sind jetzt 5 und 7 (sim4/t4, sim5/t5 unverändert, damit der gespeicherte
     Fortschritt stimmt). Jeder Einführungsclip löst ein Problem vollständig vor, mit einer Frage nach
     dem nächsten Schritt, nachdem die Grundlagen eingeführt sind. Die drei Einzelprogramme
     (Widerstand/Leistung, Schaltungen, Gefahren) sind in dieses Leitprogramm und die Themenseite 6.2
     übergegangen.
     Kompetenzmatrix: K1 → Kap. 1, 6, Aufg. 1a 1c, G1 · K2 → Kap. 1–4, 6, Aufg. 1b 1d 2a–2d 3d 4a–4d, G1 G2 G3 G5 ·
     K3 → Kap. 3, 4, Aufg. 3a–3c 3e, G4 · K4 → Kap. 5, 6, Aufg. 5a–5f 6a–6d, G6 · K5 → Kap. 7, Aufg. 7a–7f, G7.
     Nachprüfung vom 06.10.2026 (Fassung 2.0, zweiter Durchgang): Aufgabe 3e am R-l-Diagramm, Kapitelaufgaben
     2b 5a 5b 6c 7f neu (nicht mehr wie die Clipprobleme), Startwerte und Leistenziele weg von Clip- und
     Kontrollfragewerten, Gesamttest mit sieben Aufgaben (jedes Kapitel geprüft, G5 Kennlinie, G6 ungewohnt
     gezeichnete Reihenschaltung, G7 rückwärts gefragt).
     Bewusst weggelassen (RLP verlangt es nicht oder nur «einfach»): gemischte Schaltungen, belasteter
     Teiler, Messgeräte-Innenwiderstände, nichtlineare Bauteilmodelle, Coulomb-Gesetz, Wechselspannung —
     auf der Themenseite, Verweise unter «Nicht in diesem Leitprogramm».
     Zeiten (Schätzung, nach einer Erprobung prüfen): K0 15 · K1–K4 je 40 · K5 45 · K6 40 · K7 45 ·
     Gesamttest 25 = 330 min ≈ 7.3 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Elektrizität</h1>
      <p class="unter">Ladung, Spannung, Widerstand, Messen, Schaltungen und Gefahren — zuschauen, tüfteln, kontrollieren, üben. Sieben Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 6 · Teilgebiet 6.2</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Ladung und Strom</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Leistung und Energie</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Widerstand</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Messen und Kennlinien</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Reihe und parallel</span></a></li></ol>
    <p class="lekt">Lektion 6</p>
    <ol><li><a href="#k6"><span class="nr">6</span><span>Schaltungen erkennen</span></a></li></ol>
    <p class="lekt">Lektion 7</p>
    <ol><li><a href="#k7"><span class="nr">7</span><span>Gefahren und Schutz</span></a></li></ol>
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
          <li><b>① Clip</b> anschauen.</li>
          <li><b>② Tüfteln:</b> Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma; Brüche wie <code>1/2</code> und Zehnerpotenzen wie <code>2.4e-3</code> gehen auch. Richtig ist, was auf drei signifikante Stellen stimmt.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 6, Teilgebiet 6.2 Elektrizität</p>
        <ul>
          <li><b>K1</b> die Beschaffenheit von elektrischen Ladungen beschreiben (Ursprung, Einheit, Elementarladung)</li>
          <li><b>K2</b> die wichtigsten physikalischen Grössen definieren und charakterisieren (Ladung, Spannung, Stromstärke, Energie, Leistung)</li>
          <li><b>K3</b> den Widerstand eines Leiters berechnen</li>
          <li><b>K4</b> Berechnungen in einfachen seriellen oder parallelen Schaltkreisen von Widerständen durchführen</li>
          <li><b>K5</b> die wesentlichen Gefahren der Elektrizität, inklusive entsprechender Schutzmassnahmen, aufzeigen</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">6.2 Elektrizität</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Elektrizität · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Ladung') + k1 + band(2, 'Energie') + k2 + band(3, 'Widerstand') + k3
        + band(4, 'Messen') + kM + band(5, 'Schaltungen') + k4 + band(6, 'Erkennen und prüfen') + kE + band(7, 'Sicherheit') + k5
        + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
