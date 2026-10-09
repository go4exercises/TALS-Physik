"""Baut leitprogramme/leitprogramm-wellen.html aus einer Kapitelbeschreibung (seit 08.10.2026).

  python3 scripts/lp/wellen/seite.py

Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4) für das Teilgebiet 6.1 Wellen,
als Kopie von scripts/lp/waerme/ entstanden: Kopf, CSS-Gerüst, Grundskript und Bausteine von dort,
neu sind sechs Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Planung (Kompetenzmatrix, Planungstabelle, Kern/Vertiefung/weggelassen, Konventionen und Widersprüche
der Themenseite): Kopfkommentar der Seite (Variable «oben» unten) und README.md.
"""
import math
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-wellen.html'
TS = '../themen/p6-1-wellen.html'
TSA = '../themen/p6-1a-wellenexperimente.html'

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
<title>Leitprogramm Wellen</title>
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
/* Diagramme und Szenen, Farbe = eine Bedeutung: Welle und Auslenkung (Kurven, Teilchen der Welle, E-Feld)
   Bernstein, Ausbreitung und Front Grün, Licht der Sonne Orange, Wärmestrahlung und Infrarot Rot,
   Teilchen, markierte Punkte, Masslinien, Achsen und B-Feld Tinte bzw. Grau; Photonen in ihrer Spektralfarbe */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
text.p-tinte,text.p-mark{fill:var(--tinte)}
.pf-linie{stroke-width:2.4;fill:none}
.pf-linie.pf-c{stroke:var(--gruen)} .pf-kopf.pf-c{fill:var(--gruen)}
.pf-linie.mass{stroke:var(--tinte-2);stroke-width:1.2} .pf-kopf.mass{fill:var(--tinte-2)}
.pf-linie.pf-licht{stroke:var(--orange);stroke-width:4} .pf-kopf.pf-licht{fill:var(--orange)}
.pf-linie.achse-pf{stroke:var(--tinte-2);stroke-width:1.2} .pf-kopf.achse-pf{fill:var(--tinte-2)}
.pf-linie.sprung{stroke:var(--tinte);stroke-width:1.8} .pf-kopf.sprung{fill:var(--tinte)}
.pf-linie.sprung-auf{stroke:var(--tinte-2);stroke-width:1.6} .pf-kopf.sprung-auf{fill:var(--tinte-2)}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.bt-meldung{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:10.5px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.bt-wert.c-text{fill:var(--gruen)} .bt-wert.e-text{fill:var(--bernstein)} .bt-wert.b-text{fill:var(--tinte-2)}
.bt-wert.l-licht{fill:var(--orange)} .bt-wert.l-ir{fill:var(--rot)} .bt-wert.mass-text{fill:var(--tinte)}
.warnzeile{color:var(--rot)}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
.sim-aktionen .aktion:disabled{opacity:.45;cursor:default;box-shadow:none}
.sim-aktionen .aktion[hidden]{display:none}
/* Welle, Teilchen, Seil */
.ruhe{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:4 4;opacity:.7}
.kette{fill:none;stroke:var(--bernstein);stroke-width:1.6}
.teilchen-w{fill:var(--bernstein)}
.windung{stroke:var(--bernstein);stroke-width:2.2}
.windung.p-bar{stroke:var(--tinte);stroke-width:3.4}
.p-mark{fill:var(--tinte);stroke:var(--karte);stroke-width:1.6}
.erreger{fill:var(--bernstein);stroke:var(--tinte);stroke-width:1}
.hilfslinie.fuehrung,.sim .hilfslinie{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:3 3}
.front-linie{stroke:var(--gruen);stroke-width:1.2;stroke-dasharray:4 3}
.w-kurve{fill:none;stroke:var(--bernstein);stroke-width:2.4}
.berg-mark{fill:var(--tinte-2)}
.seil{fill:none;stroke:var(--bernstein);stroke-linejoin:round}
.knoten{fill:var(--tinte)}
/* Spektrum und Feld */
.spek-band{opacity:.55} .b-gamma{fill:#6b4fa0} .b-roe{fill:#5566c0} .b-uv{fill:#7b86d4} .b-vis{fill:#ccc} .b-ir{fill:var(--rot)} .b-mw{fill:#b98a50} .b-radio{fill:#8a7a62}
.band-rahmen{fill:none;stroke:var(--tinte-2);stroke-width:1}
.marke-linie{stroke:var(--tinte);stroke-width:2.2} .marke-dreieck{fill:var(--tinte)}
.e-kurve{fill:none;stroke:var(--bernstein);stroke-width:2.4} .e-pfeil{stroke:var(--bernstein);stroke-width:1.1}
.b-kurve{fill:none;stroke:var(--tinte-2);stroke-width:1.8} .b-pfeil{stroke:var(--tinte-2);stroke-width:1}
/* Atom, Photonen, Laser */
.niveau{stroke:var(--tinte);stroke-width:2}
.elektron{fill:var(--tinte)}
.atom{fill:var(--papier-2);stroke:var(--tinte-2);stroke-width:1.2} .atom.angeregt{fill:var(--bernstein-hell);stroke:var(--bernstein-rand)}
.kern{fill:var(--tinte-2)}
.photon{fill:none;stroke-width:2.2} .photon.ir-photon{stroke-dasharray:4 3}
.ir-kaestchen{stroke:var(--tinte-2);stroke-dasharray:2 2}
.gaszelle{fill:var(--papier-2);stroke:var(--tinte-2);stroke-width:1.2}
.spiegel{stroke:var(--tinte);stroke-width:4} .spiegel.teil{stroke-dasharray:5 3}
/* Atmosphäre */
.fl-rest{fill:var(--tinte-2);opacity:.3} .fl-vis{fill:var(--orange);opacity:.12}
.gas-name{fill:var(--tinte)}
.k-sonne{fill:none;stroke:var(--orange);stroke-width:2.2} .k-boden{fill:none;stroke:var(--rot);stroke-width:2.2}
.atmo{fill:var(--tinte-2)} .boden{fill:#8a6a43;opacity:.75} .sonne{fill:#e8a317}
.licht{fill:var(--orange);opacity:.75} .ir{fill:var(--rot);opacity:.7} .ir.atm{opacity:.45}
/* Minigrafen der Aufgaben */
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
svg.mini.breit{width:262px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.k-w{stroke:var(--bernstein)} .kurve-mini.k-ir{stroke:var(--rot)} .kurve-mini.k-licht{stroke:var(--orange)}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.p-mini{fill:var(--tinte)}
.legende{fill:var(--tinte-2);font-family:var(--sans);font-size:10px;font-weight:700}
.task-id.vert{font-family:var(--sans);font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--lila);
  border:1px solid var(--lila-rand);border-radius:999px;padding:1px 8px;margin-right:6px;white-space:nowrap}
.mini-reihe{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 6px calc(5.8em + 11px)}
.inhaltbox .mini-reihe{margin-left:0}

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
  var KEY = 'leitprogramm-wellen-v1';

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
  <p>Leitprogramm · Wellen</p>
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.0 · Stand 8. Oktober 2026</p>
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">6.1 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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
    """Simulation mit laufender Animation: Aktionsknöpfe (Start, Pause …) setzt seite.js in .sim-aktionen."""
    return f'''      <figure class="sim sim-gross" id="{sid}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="{svg_box}" role="img" aria-label="{label}"></svg>
        <div class="sim-aktionen"></div>{knoepfe}
{inhalt}
      </figure>'''


def figur(sid, label, svg_box, inhalt, hilfs=None, knoepfe=''):
    h = f'\n        <label class="hilfs-schalter"><input type="checkbox" checked> Hilfslinien ({hilfs})</label>' if hilfs else ''
    return f'''      <figure class="sim sim-gross" id="{sid}">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="{svg_box}" role="img" aria-label="{label}"></svg>{h}{knoepfe}
{inhalt}
      </figure>'''


def mini(*svgs):
    return '\n            <div class="mini-reihe">' + ''.join(svgs) + '</div>'


def tief(s):
    """«λ_1 [m]» für SVG-Text: Index tiefgestellt (wie stext in seite.js)."""
    return re.sub(r'_([A-Za-z0-9,]+)(.*)', r'<tspan dy="3" font-size="0.78em">\1</tspan><tspan dy="-3">\2</tspan>', s)


def zahl_t(x):
    """Zahl für SVG-Text: ohne überflüssige Nullen, echtes Minus"""
    return ('%g' % x).replace('-', '−')


def welle_mini(label, xname, yname, wert, xc, xmax, gs, lab, amp=3, ymax=4, punkte=(), extra='', kurve=True):
    """Momentbild oder Zeitdiagramm einer Sinuswelle zum Ablesen: Berg bei xc, Abstand wert; Gitter je gs,
    Beschriftung jede lab-te Linie; punkte = [(x, Name, Lage)] auf der Kurve."""
    w, h, ox, oy = 262, 150, 30, 76
    R = w - ox - 14
    ky = (oy - 12) / ymax
    n = round(xmax / gs)
    kx = R / n
    X = lambda x: ox + x / gs * kx
    Y = lambda y: oy - y * ky
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 16}" role="img" aria-label="{label}">']
    for i in range(n + 1):
        t.append(f'<line x1="{X(i * gs):.1f}" y1="{Y(ymax):.1f}" x2="{X(i * gs):.1f}" y2="{Y(-ymax):.1f}" class="gitter"/>')
    for i in range(-ymax, ymax + 1):
        t.append(f'<line x1="{ox}" y1="{Y(i):.1f}" x2="{ox + R}" y2="{Y(i):.1f}" class="gitter"/>')
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + R + 8}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{Y(-ymax) + 2:.1f}" x2="{ox}" y2="{Y(ymax) - 6:.1f}" class="achse"/>')
    for i in range(lab, n + 1, lab):
        t.append(f'<text x="{X(i * gs):.1f}" y="{Y(-ymax) + 12:.1f}" text-anchor="middle" class="skala">{zahl_t(round(i * gs, 6))}</text>')
    for v in (-amp, amp):
        t.append(f'<text x="{ox - 4}" y="{Y(v) + 3.5:.1f}" text-anchor="end" class="skala">{zahl_t(v)}</text>')
    if kurve:
        d = []
        for i in range(401):
            x = i / 400 * xmax
            d.append(f'{X(x):.1f},{Y(amp * math.cos(2 * math.pi * (x - xc) / wert)):.1f}')
        t.append('<polyline points="' + ' '.join(d) + '" class="kurve-mini k-w"/>')
    for x, name, lage in punkte:
        y = amp * math.cos(2 * math.pi * (x - xc) / wert)
        t.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.6" class="p-mini"/>')
        dy = -8 if lage == 'oben' else 15
        t.append(f'<text x="{X(x) + 5:.1f}" y="{Y(y) + dy:.1f}" class="mini-name">{name}</text>')
    t.append(extra)
    t.append(f'<text x="{ox + R + 8}" y="{Y(-ymax) + 26:.1f}" text-anchor="end" class="achsname">{tief(xname)}</text>')
    t.append(f'<text x="{ox + 4}" y="{Y(ymax) - 8:.1f}" class="achsname">{tief(yname)}</text></svg>')
    return ''.join(t)


def spektrum_mini(label, punkte):
    """λ-Achse logarithmisch von 10⁻¹² m bis 10³ m, Gitter je Zehnerpotenz; punkte = [(log10 λ, Name)]."""
    w, ox, oy = 262, 14, 50
    R = w - 2 * ox
    X = lambda L: ox + (L + 12) / 15 * R
    t = [f'<svg class="mini breit" viewBox="0 0 {w} 96" role="img" aria-label="{label}">']
    for L in range(-12, 4):
        t.append(f'<line x1="{X(L):.1f}" y1="{oy - 18}" x2="{X(L):.1f}" y2="{oy + 4}" class="gitter"/>')
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + R + 6}" y2="{oy}" class="achse"/>')
    hoch = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    for L in range(-12, 4, 3):
        t.append(f'<text x="{X(L):.1f}" y="{oy + 16}" text-anchor="middle" class="skala">{"1" if L == 0 else "10" + str(L).translate(hoch)}</text>')
    for L, name in punkte:
        t.append(f'<circle cx="{X(L):.1f}" cy="{oy}" r="4" class="p-mini"/><text x="{X(L):.1f}" y="{oy - 22}" text-anchor="middle" class="mini-name">{name}</text>')
    t.append(f'<text x="{ox + R + 6}" y="{oy + 34}" text-anchor="end" class="achsname">λ [m], logarithmisch</text></svg>')
    return ''.join(t)


def niveau_mini(label, stufen, spruenge):
    """Energiestufen (in Kästchen) mit Sprüngen: spruenge = [(von, nach, x, Text)]."""
    w, h, ox, oy, k = 262, 170, 40, 150, 24
    Y = lambda e: oy - e * k
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">']
    for e in range(0, 6):
        t.append(f'<line x1="{ox}" y1="{Y(e)}" x2="{w - 16}" y2="{Y(e)}" class="gitter"/>')
        t.append(f'<text x="{ox - 6}" y="{Y(e) + 3.5}" text-anchor="end" class="skala">{e}</text>')
    t.append(f'<line x1="{ox}" y1="{oy + 4}" x2="{ox}" y2="{Y(5) - 8}" class="achse"/>')
    for name, e in stufen:
        t.append(f'<line x1="{ox + 6}" y1="{Y(e)}" x2="{w - 22}" y2="{Y(e)}" stroke="currentColor" class="achse" style="stroke-width:2.4"/>')
        t.append(f'<text x="{w - 18}" y="{Y(e) + 4}" class="mini-name">{tief(name)}</text>')
    for a, b, x, txt in spruenge:
        y1, y2 = Y(a) + 3, Y(b) - 3
        t.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 6}" class="achse" style="stroke:currentColor;stroke-width:1.6"/>')
        t.append(f'<polygon points="{x - 4},{y2 - 7} {x + 4},{y2 - 7} {x},{y2}" class="p-mini"/>')
        t.append(f'<text x="{x + 5}" y="{(y1 + y2) / 2 + 4:.1f}" class="mini-name" style="font-size:10.5px">{txt}</text>')
    t.append(f'<text x="{ox + 4}" y="{Y(5) - 10}" class="achsname">E [Kästchen]</text></svg>')
    return ''.join(t)


def durchlass_mini(label, punkte):
    """Durchgelassener Anteil über λ (0.1 µm bis 100 µm, logarithmisch), vereinfacht 0 oder 1 wie sim6."""
    w, h, ox, oy = 262, 150, 34, 116
    R = w - ox - 14
    X = lambda l: ox + (math.log10(l) + 1) / 3 * R
    Y = lambda a: oy - a * 90
    banden = [(5.5, 8.0), (9.3, 10.1), (13.5, 17.0), (20, 100)]
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 14}" role="img" aria-label="{label}">']
    for l, s in ((0.1, '0.1'), (0.2, ''), (0.5, '0.5'), (1, '1'), (2, ''), (5, '5'), (10, '10'), (20, ''), (50, '50'), (100, '100')):
        t.append(f'<line x1="{X(l):.1f}" y1="{Y(1.1):.1f}" x2="{X(l):.1f}" y2="{oy}" class="gitter"/>')
        if s:
            t.append(f'<text x="{X(l):.1f}" y="{oy + 13}" text-anchor="middle" class="skala">{s}</text>')
    for a in (0.5, 1):
        t.append(f'<line x1="{ox}" y1="{Y(a):.1f}" x2="{ox + R}" y2="{Y(a):.1f}" class="gitter"/><text x="{ox - 4}" y="{Y(a) + 3.5:.1f}" text-anchor="end" class="skala">{zahl_t(a)}</text>')
    for a, b in banden:
        t.append(f'<rect x="{X(a):.1f}" y="{Y(1.1):.1f}" width="{X(b) - X(a):.1f}" height="{oy - Y(1.1):.1f}" class="fl-rest"/>')
    pts, l = [], 0.1
    stufen = sorted([0.1, 100] + [x for ab in banden for x in ab])
    for i in range(len(stufen) - 1):
        a, b = stufen[i], stufen[i + 1]
        drin = any(p <= (a + b) / 2 <= q for p, q in banden)
        v = 0 if drin else 1
        pts += [f'{X(a):.1f},{Y(v):.1f}', f'{X(b):.1f},{Y(v):.1f}']
    t.append('<polyline points="' + ' '.join(pts) + '" class="kurve-mini"/>')
    for l, name in punkte:
        drin = any(p <= l <= q for p, q in banden)
        t.append(f'<circle cx="{X(l):.1f}" cy="{Y(0 if drin else 1):.1f}" r="3.6" class="p-mini"/><text x="{X(l) + 4:.1f}" y="{Y(0 if drin else 1) - 6:.1f}" class="mini-name">{name}</text>')
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + R + 6}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{Y(1.1) - 4:.1f}" class="achse"/>')
    t.append(f'<text x="{ox + R + 6}" y="{oy + 26}" text-anchor="end" class="achsname">λ [µm], logarithmisch</text>')
    t.append(f'<text x="{ox + 4}" y="{Y(1.1) - 6:.1f}" class="achsname">durchgelassener Anteil</text></svg>')
    return ''.join(t)


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P02 = '../themen/p0-2-vorwissen-physik.html'
P01 = '../themen/p0-1-vorwissen-mathematik.html'
LPK = 'leitprogramm-kinematik.html'
LPW = 'leitprogramm-waerme.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 4.1</span><span class="zeit">≈ 15 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Vorsilben und Zehnerpotenzen, Gleichungen umstellen, gleichförmige Bewegung, Umlaufzeit und Frequenz. Wenn das wackelt: <a href="''' + P02 + '''#praefixe">Vorwissen 0.2, Vorsilben</a> und das <a href="''' + LPK + '''">Leitprogramm Kinematik</a>.</p>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Schreibe mit Zehnerpotenzen und ohne Vorsilbe: \(2.4\;\text{GHz}\) in Hertz und \(650\;\text{nm}\) in Meter.',
     r'<p>Giga heisst \(10^{9}\): \(2.4\;\text{GHz} = 2.4 \cdot 10^{9}\;\text{Hz}\).</p><p>Nano heisst \(10^{-9}\): \(650\;\text{nm} = 650 \cdot 10^{-9}\;\text{m} = 6.5 \cdot 10^{-7}\;\text{m}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#praefixe">Vorwissen 0.2: Vorsilben</a></p>', ''),
    ('0b', 2, r'Rechne ohne Taschenrechner: \(\dfrac{3.0 \cdot 10^{8}}{1.5 \cdot 10^{6}}\) und \(3.0 \cdot 10^{8} \cdot 2.0 \cdot 10^{-7}\).',
     r'<p>\(\dfrac{3.0 \cdot 10^{8}}{1.5 \cdot 10^{6}} = \dfrac{3.0}{1.5} \cdot 10^{8-6} = 2.0 \cdot 10^{2} = 200\)</p><p>\(3.0 \cdot 10^{8} \cdot 2.0 \cdot 10^{-7} = 3.0 \cdot 2.0 \cdot 10^{8-7} = 6.0 \cdot 10^{1} = 60\)</p><p class="komm">Falsch? <a href="' + P01 + r'#potenzen">Vorwissen 0.1: Potenzen</a></p>', ''),
    ('0c', 2, r'Stelle \(v = \dfrac{s}{t}\) nach \(s\) und nach \(t\) um.',
     r'<p>\(s = v \cdot t\) und \(t = \dfrac{s}{v}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1: Gleichungen umstellen</a></p>', ''),
    ('0d', 2, r'Ein Zug fährt gleichförmig mit \(25\;\text{m/s}\). Wie weit kommt er in \(8.0\;\text{s}\)? Wie lange braucht er für \(1.0\;\text{km}\)?',
     r'<p>\(s = v \cdot t = 25\;\text{m/s} \cdot 8.0\;\text{s} = 200\;\text{m}\)</p><p>\(t = \dfrac{s}{v} = \dfrac{1000\;\text{m}}{25\;\text{m/s}} = 40\;\text{s}\)</p><p class="komm">Falsch? <a href="' + LPK + r'#ort-und-geschwindigkeit">Leitprogramm Kinematik, Kapitel 1</a></p>', ''),
    ('0e', 2, r'Ein Velorad dreht sich in \(2.5\;\text{s}\) 15-mal. Wie lange dauert eine Umdrehung (Umlaufzeit \(T\)), und wie viele Umdrehungen macht es pro Sekunde (Frequenz \(f\))?',
     r'<p>\(T = \dfrac{2.5\;\text{s}}{15} \approx 0.167\;\text{s}\)</p><p>\(f = \dfrac{15}{2.5\;\text{s}} = 6.0\;\text{Hz}\), mit \(1\;\text{Hz} = 1/\text{s}\). Frequenz und Umlaufzeit sind Kehrwerte: \(f = \dfrac{1}{T}\).</p><p class="komm">Falsch? <a href="' + LPK + r'#kreisbewegung">Leitprogramm Kinematik, Kreisbewegung</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Eine Kette aus gekoppelten Teilchen; das erste Teilchen ist der Erreger; die Welle läuft nach rechts, das markierte Teilchen P schwingt um seine Ruhelage', '-4 -4 308 160',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'f', '<i>f</i> Erreger', 0.25, 2.5, 0.05, 1.0, 'Hz', 2) + '\n        </div>',
    knoepfe('art', 'Welle', [('quer', 'Querwelle'), ('laengs', 'Längswelle')], 'quer')
    + knoepfe('erreger', 'Erreger', [('dauernd', 'dauernd'), ('stoss', 'ein Stoss')], 'dauernd'))
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Von der Schwingung zur Welle</div>
          <p>Eine <b>Schwingung</b> ist eine periodische Bewegung um eine Ruhelage; die grösste Auslenkung heisst <b>Amplitude</b> \(A\). Die <b>Periode</b> \(T\) ist die Dauer einer Schwingung, die <b>Frequenz</b> \(f\) die Anzahl Schwingungen pro Sekunde:</p>
          <p>\[ f = \frac{\text{Anzahl Schwingungen}}{\text{Zeit}} = \frac{1}{T}, \qquad [f] = \text{Hz} = \frac{1}{\text{s}} \]</p>
          <p><b>Wellenerzeugung:</b> Ein Erreger schwingt. Die Teilchen des Mediums sind <b>gekoppelt</b>: Jedes übernimmt die Bewegung seines Nachbarn, aber <b>verzögert</b>. So läuft die Störung als Welle weiter, mit der <b>Ausbreitungsgeschwindigkeit</b> \(c = \dfrac{s}{t}\) (Weg der Front durch Laufzeit). Jedes Teilchen schwingt nur um seine Ruhelage: Eine Welle transportiert <b>Energie, aber keine Materie</b>.</p>
          <p><b>Querwelle</b> (Transversalwelle): Die Teilchen schwingen quer zur Ausbreitung — Seilwelle, Welle auf einer gespannten Gitarrensaite. <b>Längswelle</b> (Longitudinalwelle): Sie schwingen in Ausbreitungsrichtung; es entstehen Verdichtungen und Verdünnungen — Stoss, der durch eine Reihe Güterwagen läuft, <b>Schall in Luft</b>. Wasserwellen sind weder rein quer noch rein längs: An der Oberfläche laufen die Teilchen auf Kreisbahnen.</p>
          <p><b>Mechanische Wellen</b> (Seil, Wasser, Erdbeben, Schall) brauchen ein Medium aus gekoppelten Teilchen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Welle trägt das Wasser mit.» Die Teilchen schwingen nur um ihren Platz; weiter läuft die Form der Welle — und mit ihr die Energie.</p>
          <p>Periode und Frequenz verwechselt: \(T\) ist eine Zeit in Sekunden, \(f\) eine Anzahl pro Sekunde in Hertz; ihr Produkt ist immer \(1\).</p>
        </div>
      </div>'''
SEIL = welle_mini('Momentbild einer Seilwelle, die nach rechts läuft; Berge bei 1.0 m und 3.0 m, Täler bei 0 m, 2.0 m und 4.0 m; markiert A bei 1.3 m, B bei 2.7 m und C bei 0.3 m',
                  's [m]', 'y [cm]', 2.0, 1.0, 4.0, 0.2, 5, amp=3, punkte=[(1.3, 'A', 'oben'), (2.7, 'B', 'oben'), (0.3, 'C', 'unten')],
                  extra='<text x="248" y="12" text-anchor="end" class="legende">die Welle läuft nach rechts →</text>')
auf1 = test('t1', 'Aufgaben · Kapitel 1', 12, [
    ('1a', 3, r'Beschreibe in drei Schritten, wie aus der Bewegung einer Hand am Ende eines Seils eine Welle wird. Verwende die Wörter gekoppelt, verzögert und Energie.',
     r'<p>1. Die Hand bewegt das erste Stück des Seils auf und ab: eine Schwingung.</p><p>2. Die Seilstücke sind gekoppelt: Jedes zieht seinen Nachbarn mit, und der macht dieselbe Bewegung etwas verzögert.</p><p>3. So läuft die Störung das Seil entlang, während jedes Stück nur um seine Ruhelage schwingt. Transportiert wird Energie, nicht das Seil.</p>', ''),
    ('1b', 3, r'Ein Wellenkamm braucht \(4.0\;\text{s}\) von einem Pfosten eines Bootsstegs zum nächsten, \(10\;\text{m}\) weiter. Ein Boot am Steg hebt und senkt sich 18-mal pro Minute. Berechne die Ausbreitungsgeschwindigkeit, die Frequenz und die Periode.',
     r'<p>\(c = \dfrac{s}{t} = \dfrac{10\;\text{m}}{4.0\;\text{s}} = 2.5\;\text{m/s}\)</p><p>\(f = \dfrac{18}{60\;\text{s}} = 0.30\;\text{Hz}\)</p><p>\(T = \dfrac{1}{f} = \dfrac{1}{0.30\;\text{Hz}} \approx 3.3\;\text{s}\)</p>', ''),
    ('1c', 3, r'Das Bild zeigt eine Seilwelle, die nach rechts läuft, zu einem festen Zeitpunkt (wie ein Foto). Jedes Teilchen übernimmt die Bewegung seines linken Nachbarn verzögert. Bewegen sich die Teilchen A, B und C gerade nach oben oder nach unten? Begründe für A.',
     r'<p>A: nach oben. Sein linker Nachbar ist schon höher (A liegt rechts vom Berg bei \(1.0\;\text{m}\)); A übernimmt diese Bewegung als Nächstes.</p><p>B: nach unten — sein linker Nachbar ist tiefer (B liegt links vom Berg bei \(3.0\;\text{m}\), nach dem Tal).</p><p>C: nach unten — auch sein linker Nachbar ist tiefer (C liegt kurz nach dem Tal bei \(0\;\text{m}\)).</p><p>Merkregel für eine Welle nach rechts: Vor einem Berg (rechts davon) geht es aufwärts, hinter ihm abwärts.</p>',
     mini(SEIL)),
    ('1d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Warum ist eine Wasserwelle weder eine reine Quer- noch eine reine Längswelle? Wie bewegt sich ein Ball, der im Meer schwimmt, während eine Welle unter ihm durchläuft?',
     r'<p>Die Wasserteilchen an der Oberfläche laufen auf Kreisbahnen: Sie bewegen sich zugleich auf und ab (quer) und hin und her (längs).</p><p>Der Ball macht diese Kreisbewegung mit: Auf dem Berg rückt er ein Stück vor, im Tal ein Stück zurück. Im Mittel bleibt er am selben Ort — weiter treiben ihn nur Wind und Strömung.</p>', ''),
])
k1 = kapitel(1, 'schwingung-welle', 'Von der Schwingung zur Welle', 'K1 · K2 · K3', 45,
    r'Du beschreibst, wie aus der Schwingung eines Erregers über gekoppelte Teilchen eine Welle entsteht, unterscheidest Quer- und Längswelle, rechnest mit Periode, Frequenz und Ausbreitungsgeschwindigkeit und erklärst, warum eine Welle Energie, aber keine Materie transportiert.',
    ('p6-1-lp-welle', 'Wellen sehen: aus der Schwingung wird eine Welle'),
    sim1, ('p6-1-lp-kontrolle-welle', 'Kontrollfragen zur Entstehung einer Welle'),
    fest1, [uebung('periode', 'Periode und Frequenz'), uebung('laufzeit', 'Wie schnell läuft die Störung?'), uebung('quer-laengs', 'Quer oder längs?')],
    auf1, f'<a href="{TS}#definition">Themenseite 6.1, Grundbegriffe</a> · <a href="{TS}#typen">Transversal- und Longitudinalwellen</a> · <a href="{TSA}#erreger">Vertiefung 6.1a: Vom Wackeln zur Welle</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur('sim2', 'Oben das Momentbild eines Seils zum Zeitpunkt t, unten das Zeitdiagramm des Punkts P; ein Dreieck markiert einen Wellenberg', '-4 -4 308 330',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 't', '<i>t</i> Zeitpunkt', 0, 6, 0.1, 0.5, 's', 1) + '\n          '
    + regler('s2', 'sp', '<i>s</i> von P', 0, 6, 0.5, 1.0, 'm', 1) + '\n        </div>',
    hilfs='Stelle von P, Zeitpunkt t',
    knoepfe=knoepfe('welle', 'Welle', [('A', 'Welle A'), ('B', 'Welle B')], 'A'))
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zwei Diagramme, zwei Grössen</div>
          <p>Eine Welle hängt vom Ort \(s\) und von der Zeit \(t\) ab. Ein Diagramm zeigt nur eines davon auf der waagrechten Achse:</p>
          <ul>
            <li><b>Momentbild</b> \(y(s)\): Die Zeit steht still, man sieht die ganze Welle. Der Abstand zweier benachbarter Berge — allgemein zweier Stellen gleicher Phase — ist die <b>Wellenlänge</b> \(\lambda\), eine Länge in Metern.</li>
            <li><b>Zeitdiagramm</b> \(y(t)\): Der Ort steht fest, man sieht einen Punkt im Lauf der Zeit. Der Abstand zweier Maxima ist die <b>Periode</b> \(T\), eine Zeit in Sekunden.</li>
          </ul>
          <p>Die Amplitude \(A\) ist in beiden Diagrammen die grösste Auslenkung. In einer Periode rückt jeder Berg genau um eine Wellenlänge weiter. Das ergibt die <b>Phasengeschwindigkeit</b> (Ausbreitungsgeschwindigkeit), die Geschwindigkeit einer Stelle gleicher Phase:</p>
          <p>\[ c = \frac{\lambda}{T} = \lambda \cdot f \]</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>\(\lambda\) im Zeitdiagramm abgelesen: Dort liegen zwischen zwei Maxima Sekunden, keine Meter. Zuerst die Achse lesen: Ort oder Zeit?</p>
          <p>Von Berg zu Tal gemessen: Das ist nur eine halbe Wellenlänge bzw. eine halbe Periode.</p>
        </div>
      </div>'''
MB2 = welle_mini('Momentbild einer Seilwelle: Berge bei 0.3 m, 1.5 m und 2.7 m, Gitter 0.2 m', 's [m]', 'y [cm]', 1.2, 0.3, 3.6, 0.2, 5)
ZD2 = welle_mini('Zeitdiagramm eines Punkts derselben Welle: Maxima bei 0.1 s, 0.5 s, 0.9 s und 1.3 s, Gitter 0.1 s', 't [s]', 'y [cm]', 0.4, 0.1, 1.6, 0.1, 5)
LOES2B = welle_mini('Lösung: Momentbild mit λ = 1.6 m und A = 5 cm, Berge bei 0, 1.6 m und 3.2 m', 's [m]', 'y [cm]', 1.6, 0.0, 4.0, 0.2, 5, amp=5, ymax=6)
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Die beiden Diagramme zeigen dieselbe Seilwelle: links das Momentbild, rechts das Zeitdiagramm eines Punkts. Lies \(\lambda\) und \(T\) ab und berechne \(f\) und \(c\).',
     r'<p>Momentbild (Achse \(s\)): von Berg zu Berg \(\lambda = 1.2\;\text{m}\). Zeitdiagramm (Achse \(t\)): von Maximum zu Maximum \(T = 0.40\;\text{s}\).</p><p>\(f = \dfrac{1}{T} = \dfrac{1}{0.40\;\text{s}} = 2.5\;\text{Hz}\)</p><p>\(c = \dfrac{\lambda}{T} = \dfrac{1.2\;\text{m}}{0.40\;\text{s}} = 3.0\;\text{m/s}\), ebenso \(c = \lambda \cdot f = 1.2\;\text{m} \cdot 2.5\;\text{Hz} = 3.0\;\text{m/s}\).</p>',
     mini(MB2, ZD2)),
    ('2b', 3, r'Eine Seilwelle hat die Wellenlänge \(\lambda = 1.6\;\text{m}\) und die Amplitude \(A = 5\;\text{cm}\). Zu einem Zeitpunkt sitzt bei \(s = 0\) ein Berg. Zeichne das Momentbild von \(s = 0\) bis \(s = 4.0\;\text{m}\) mit beschrifteten Achsen und markiere \(\lambda\) und \(A\).',
     r'<p>Achsen: \(s\) in m waagrecht, \(y\) in cm senkrecht. Berge (\(y = 5\;\text{cm}\)) bei \(s = 0\), \(1.6\;\text{m}\) und \(3.2\;\text{m}\); Täler (\(y = -5\;\text{cm}\)) bei \(0.8\;\text{m}\), \(2.4\;\text{m}\) und \(4.0\;\text{m}\); dazwischen \(y = 0\) bei \(0.4\), \(1.2\), \(2.0\), \(2.8\) und \(3.6\;\text{m}\).</p><p>\(\lambda\): Pfeil von einem Berg zum nächsten. \(A\): von der Ruhelage (\(y = 0\)) bis zu einem Berg.</p>' + mini(LOES2B), ''),
    ('2c', 3, r'Mia und Noah messen an derselben Wasserwelle. Mia misst von einem Wellenberg zum nächsten \(6.2\;\text{m}\), Noah stoppt bei einer Boje von einem Hochpunkt zum nächsten \(2.0\;\text{s}\). Noah sagt: «Die Wellenlänge ist \(2.0\), du hast dich vermessen.» Wer hat was gemessen? Berechne die Phasengeschwindigkeit.',
     r'<p>Beide haben richtig gemessen, aber verschiedene Grössen: Mia eine Länge am «Foto» der Welle, die Wellenlänge \(\lambda = 6.2\;\text{m}\); Noah eine Zeit an einer festen Stelle, die Periode \(T = 2.0\;\text{s}\). Eine Zeit kann keine Wellenlänge sein.</p><p>\(c = \dfrac{\lambda}{T} = \dfrac{6.2\;\text{m}}{2.0\;\text{s}} = 3.1\;\text{m/s}\)</p>', ''),
    ('2d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Eine Hand bewegt das Ende eines Seils ab \(t = 0\) zuerst nach oben, mit der Periode \(T = 0.60\;\text{s}\); die Welle läuft mit \(c = 2.0\;\text{m/s}\). Wann beginnt der Punkt bei \(s = 3.0\;\text{m}\) zu schwingen? Skizziere sein Zeitdiagramm von \(t = 0\) bis \(t = 3.0\;\text{s}\).',
     r'<p>\(t = \dfrac{s}{c} = \dfrac{3.0\;\text{m}}{2.0\;\text{m/s}} = 1.5\;\text{s}\). Bis dahin ist \(y = 0\).</p><p>Danach macht der Punkt dieselbe Bewegung wie die Hand, zuerst nach oben: Maxima bei \(1.5\;\text{s} + 0.15\;\text{s} = 1.65\;\text{s}\), dann alle \(0.60\;\text{s}\): \(2.25\;\text{s}\) und \(2.85\;\text{s}\).</p>', ''),
])
k2 = kapitel(2, 'momentbild-zeitdiagramm', 'Momentbild und Zeitdiagramm', 'K1', 40,
    r'Du liest im Momentbild die Wellenlänge und im Zeitdiagramm die Periode ab, zeichnest ein Momentbild und berechnest die Frequenz und die Phasengeschwindigkeit \(c = \dfrac{\lambda}{T} = \lambda \cdot f\).',
    ('p6-1-lp-diagramme', 'Wellen sehen: Momentbild und Zeitdiagramm'),
    sim2, ('p6-1-lp-kontrolle-diagramme', 'Kontrollfragen zu Momentbild und Zeitdiagramm'),
    fest2, [uebung('ablesen', 'λ oder T ablesen'), uebung('phasengeschw', 'Phasengeschwindigkeit')],
    auf2, f'<a href="{TS}#wellengleichung">Themenseite 6.1, die Wellengleichung</a> · <a href="{TSA}#gesichter">Vertiefung 6.1a: die zwei Gesichter der Welle</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Ein Sender schwingt links; die Welle läuft durch ein erstes Seil und an einer Knotenstelle in ein zweites, dünneres, gleiches oder dickeres Seil', '-4 -4 308 172',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'f', '<i>f</i> Sender', 0.25, 2.0, 0.05, 0.75, 'Hz', 2) + '\n        </div>',
    knoepfe('rechts', 'Seil 2', [('duenn', 'dünner'), ('gleich', 'gleich'), ('dick', 'dicker')], 'gleich'))
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Sender, Medium und Schall</div>
          <p>Die <b>Wellengleichung</b> verbindet die drei Grössen:</p>
          <p>\[ c = \lambda \cdot f \qquad\Longleftrightarrow\qquad \lambda = \frac{c}{f} \]</p>
          <p>Der <b>Sender</b> legt die Frequenz \(f\) fest, das <b>Medium</b> (und die Art der Welle) die Geschwindigkeit \(c\); die Wellenlänge stellt sich daraus ein. Ein schnellerer Sender macht die Welle kürzer, nicht schneller.</p>
          <p><b>Wechselt eine Welle das Medium</b>, bleibt die Frequenz gleich; Geschwindigkeit und Wellenlänge ändern sich im selben Verhältnis: \(\dfrac{\lambda_2}{\lambda_1} = \dfrac{c_2}{c_1}\).</p>
          <p><b>Schall</b> ist eine mechanische Welle aus Druckschwankungen; in Gasen und Flüssigkeiten ist er eine <b>Längswelle</b> (in festen Stoffen gibt es zusätzlich Querwellen). Er braucht ein Medium; im Vakuum gibt es keinen Schall. Je stärker die Teilchen eines Stoffs gekoppelt und je leichter sie sind, desto schneller läuft er: in Helium (leichte Atome) schneller als in Luft, in festen Stoffen meist am schnellsten.</p>
          <p>Dasselbe gilt fürs Seil der Simulation: Ein dünneres, leichteres Seil ist weniger träge, die Welle läuft darauf schneller.</p>
          <div class="tabhuelle"><table class="gesetze">
            <tr><th>Medium</th><th>Luft (\(15\;^\circ\text{C}\))</th><th>Helium</th><th>Wasser</th><th>Eisen</th></tr>
            <tr><td>\(c\) in m/s</td><td>\(340\)</td><td>\(980\)</td><td>\(\approx 1500\)</td><td>\(5170\)</td></tr>
          </table></div>
          <p>Der Mensch hört etwa \(20\;\text{Hz}\) bis \(20\;\text{kHz}\); tiefer liegt <b>Infraschall</b>, höher <b>Ultraschall</b>.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Höhere Frequenz, schnellere Welle.» Im selben Medium laufen alle Töne gleich schnell; die hohe Welle ist nur kürzer.</p>
          <p>Beim Übergang in ein anderes Medium die Frequenz geändert: Sie kommt vom Sender und bleibt.</p>
          <p>Kilohertz nicht in Hertz umgerechnet: \(1\;\text{kHz} = 1000\;\text{Hz}\).</p>
        </div>
      </div>'''
DRUCK3 = welle_mini('Momentbild der Druckschwankung eines Tons in einem unbekannten Stoff: Berge bei 0.5 m, 2.5 m, 4.5 m und 6.5 m, Gitter 0.5 m', 's [m]', 'Δp [Pa]', 2.0, 0.5, 8.0, 0.5, 2, amp=2, ymax=3)
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Ein Ultraschallgerät beim Arzt arbeitet mit \(5.0\;\text{MHz}\). Im Gewebe läuft der Schall etwa so schnell wie in Wasser. Wie lang ist die Welle dort? Warum hört man davon nichts?',
     r'<p>\(f = 5.0\;\text{MHz} = 5.0 \cdot 10^{6}\;\text{Hz}\)</p><p>\(\lambda = \dfrac{c}{f} = \dfrac{1500\;\text{m/s}}{5.0 \cdot 10^{6}\;\text{Hz}} = 3.0 \cdot 10^{-4}\;\text{m} = 0.30\;\text{mm}\)</p><p>\(5.0\;\text{MHz}\) liegt weit über \(20\;\text{kHz}\): Ultraschall, für das Ohr unhörbar.</p>', ''),
    ('3b', 3, r'In einem alten Film legt jemand das Ohr an die Eisenbahnschiene, um einen Zug früh zu hören (nicht nachmachen). Der Zug ist \(1.0\;\text{km}\) entfernt. Wie lange braucht sein Geräusch durch die Luft, wie lange durch die Schiene? Warum ist der Schall im Eisen so viel schneller?',
     r'<p>Luft: \(t = \dfrac{s}{c} = \dfrac{1000\;\text{m}}{340\;\text{m/s}} \approx 2.9\;\text{s}\)</p><p>Eisen: \(t = \dfrac{1000\;\text{m}}{5170\;\text{m/s}} \approx 0.19\;\text{s}\)</p><p>Im festen Eisen sind die Teilchen viel stärker aneinander gekoppelt als in der Luft: Jedes gibt die Bewegung schneller an den Nachbarn weiter.</p>', ''),
    ('3c', 3, r'Ein Ton von \(750\;\text{Hz}\) läuft durch einen unbekannten Stoff. Das Momentbild zeigt die Druckschwankung. Lies die Wellenlänge ab, berechne die Schallgeschwindigkeit und bestimme den Stoff mit der Tabelle im Festhalten.',
     r'<p>Von Berg zu Berg: \(\lambda = 2.0\;\text{m}\).</p><p>\(c = \lambda \cdot f = 2.0\;\text{m} \cdot 750\;\text{Hz} = 1500\;\text{m/s}\): Wasser.</p>',
     mini(DRUCK3)),
    ('3d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Eine Fledermaus ruft mit \(40\;\text{kHz}\). Das Echo von einem Insekt kommt nach \(6.0\;\text{ms}\) zurück. Wie weit ist das Insekt entfernt? Wie lang ist die Welle in Luft, verglichen mit einer Mücke von rund \(5\;\text{mm}\)?',
     r'<p>Der Ruf läuft hin und zurück: \(2d = c \cdot t\), also \(d = \dfrac{c \cdot t}{2} = \dfrac{340\;\text{m/s} \cdot 0.0060\;\text{s}}{2} \approx 1.0\;\text{m}\).</p><p>\(\lambda = \dfrac{c}{f} = \dfrac{340\;\text{m/s}}{40\,000\;\text{Hz}} = 0.0085\;\text{m} = 8.5\;\text{mm}\) — etwa so gross wie eine Mücke. Darum taugt so kurzwelliger Schall, um kleine Beute zu orten.</p>', ''),
])
k3 = kapitel(3, 'sender-medium', 'Sender und Medium: die Wellengleichung', 'K1 · K2', 45,
    r'Du wendest die Wellengleichung \(c = \lambda \cdot f\) an, unterscheidest, was der Sender (die Frequenz) und was das Medium (die Geschwindigkeit) festlegt, berechnest die Wellenlänge beim Übergang in ein anderes Medium und erklärst, warum Schall ein Medium braucht.',
    ('p6-1-lp-medium', 'Wellen sehen: Sender und Medium'),
    sim3, ('p6-1-lp-kontrolle-medium', 'Kontrollfragen zu Sender, Medium und Schall'),
    fest3, [uebung('wellengleichung', 'Wellengleichung'), uebung('medium', 'Ein anderes Medium'), uebung('hoerbar', 'Hörbar oder nicht?')],
    auf3, f'<a href="{TS}#wellengleichung">Themenseite 6.1, die Wellengleichung</a> · <a href="{TS}#schall">Schall in verschiedenen Medien</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Oben das elektromagnetische Spektrum mit einer Marke beim gewählten Gerät, unten das elektrische und das magnetische Feld der Welle', '-4 -4 308 296', '',
    knoepfe('geraet', 'Gerät', [('radio', 'UKW-Radio'), ('wlan', 'WLAN'), ('ir', 'Wärmebildkamera'), ('gruen', 'Laserpointer'), ('uv', 'UV-Lampe'), ('roentgen', 'Röntgenröhre')], 'radio'))
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Elektromagnetische Wellen</div>
          <p>Eine <b>elektromagnetische Welle</b> besteht aus einem elektrischen und einem magnetischen Feld, die einander erzeugen. Sie schwingen im gleichen Takt (gleichphasig), senkrecht zueinander und quer zur Ausbreitung — eine <b>Querwelle</b>. Es schwingen keine Teilchen; darum braucht sie <b>kein Medium</b> und läuft auch durchs Vakuum.</p>
          <p>Im Vakuum laufen alle mit der <b>Lichtgeschwindigkeit</b> \(c = 3.00 \cdot 10^{8}\;\text{m/s}\) (genauer \(2.998 \cdot 10^{8}\;\text{m/s}\)), in Luft praktisch gleich schnell. Auch hier gilt \(c = \lambda \cdot f\).</p>
          <div class="tabhuelle"><table class="gesetze">
            <tr><th>Bereich</th><th>Wellenlänge</th><th>Beispiele</th></tr>
            <tr><td>Radiowellen</td><td class="wort">länger als rund \(1\;\text{m}\)</td><td class="wort">UKW-Radio (rund \(3\;\text{m}\)), Langwelle</td></tr>
            <tr><td>Mikrowellen</td><td class="wort">rund \(1\;\text{mm}\) bis \(1\;\text{m}\)</td><td class="wort">Radar, WLAN (\(2.4\) und \(5\;\text{GHz}\)), Mikrowellenofen (\(2.45\;\text{GHz}\))</td></tr>
            <tr><td>Infrarot</td><td class="wort">\(780\;\text{nm}\) bis rund \(1\;\text{mm}\)</td><td class="wort">Wärmestrahlung, Fernbedienung</td></tr>
            <tr><td>sichtbares Licht</td><td class="wort">\(380\;\text{nm}\) (violett) bis \(780\;\text{nm}\) (rot)</td><td class="wort">Sonne, Lampen</td></tr>
            <tr><td>Ultraviolett</td><td class="wort">rund \(10\;\text{nm}\) bis \(380\;\text{nm}\)</td><td class="wort">Sonnenbrand, Schwarzlicht</td></tr>
            <tr><td>Röntgenstrahlung</td><td class="wort">rund \(10\;\text{pm}\) bis \(10\;\text{nm}\)</td><td class="wort">Röntgenbild</td></tr>
            <tr><td>Gammastrahlung</td><td class="wort">kürzer als rund \(10\;\text{pm}\)</td><td class="wort">radioaktive Stoffe</td></tr>
          </table></div>
          <p>Die Grenzen sind fliessend und werden nicht überall gleich gezogen. Nach unten in der Tabelle werden die Wellen kürzer, die Frequenz höher — und die Energie, die ein einzelnes <b>Photon</b> trägt, grösser: \(E = h \cdot f\) (\(h\): Planck-Konstante). Darum können Ultraviolett, Röntgen- und Gammastrahlung Atome ionisieren und Zellen schädigen, Radiowellen nicht.</p>
          <p><b>Wellen im Vergleich:</b></p>
          <div class="tabhuelle"><table class="gesetze">
            <tr><th>Welle</th><th>Was schwingt?</th><th>Medium</th><th>Art</th></tr>
            <tr><td>Seil, Wasser, Erdbeben</td><td class="wort">Teilchen des Stoffs</td><td class="wort">nötig</td><td class="wort">quer oder längs</td></tr>
            <tr><td>Schall</td><td class="wort">Druck und Teilchen</td><td class="wort">nötig</td><td class="wort">längs (in Gasen und Flüssigkeiten)</td></tr>
            <tr><td>elektromagnetisch</td><td class="wort">elektrisches und magnetisches Feld</td><td class="wort">nicht nötig</td><td class="wort">quer</td></tr>
          </table></div>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Radiowellen sind Schall.» Radio ist eine elektromagnetische Welle; erst der Lautsprecher macht daraus Schall.</p>
          <p>Mit \(340\;\text{m/s}\) gerechnet: Für elektromagnetische Wellen gilt \(3.00 \cdot 10^{8}\;\text{m/s}\) — auch für Licht hoher Frequenz, es ist nicht schneller.</p>
        </div>
      </div>'''
SPEK4 = spektrum_mini('Wellenlängen-Achse von 10 hoch minus 12 bis 10 hoch 3 Meter, logarithmisch; A bei 10 hoch minus 4 m, B bei 10 hoch minus 10 m, C bei 10 m',
                      [(-4, 'A'), (-10, 'B'), (1, 'C')])
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Vergleiche Schall und Licht in drei Punkten: was schwingt, ob ein Medium nötig ist und wie schnell sie in Luft sind.',
     r'<p>Was schwingt: Beim Schall schwingen die Teilchen der Luft (Druckschwankungen), beim Licht ein elektrisches und ein magnetisches Feld.</p><p>Medium: Schall braucht eines, Licht nicht — es kommt auch durchs Vakuum von der Sonne.</p><p>Geschwindigkeit in Luft: Schall rund \(340\;\text{m/s}\), Licht rund \(3.00 \cdot 10^{8}\;\text{m/s}\), fast eine Million Mal schneller.</p>', ''),
    ('4b', 3, r'Ein Navigationssatellit sendet aus rund \(20\,200\;\text{km}\) Höhe mit \(1.575\;\text{GHz}\). Wie lang ist die Welle, und wie lange braucht das Signal senkrecht bis zum Boden?',
     r'<p>\(\lambda = \dfrac{c}{f} = \dfrac{3.00 \cdot 10^{8}\;\text{m/s}}{1.575 \cdot 10^{9}\;\text{Hz}} \approx 0.190\;\text{m} = 19.0\;\text{cm}\)</p><p>\(t = \dfrac{s}{c} = \dfrac{2.02 \cdot 10^{7}\;\text{m}}{3.00 \cdot 10^{8}\;\text{m/s}} \approx 0.0673\;\text{s} = 67.3\;\text{ms}\)</p>', ''),
    ('4c', 3, r'Lies auf der Achse die Wellenlängen von A, B und C ab, nenne ihre Bereiche im Spektrum und ordne sie nach steigender Frequenz.',
     r'<p>A: \(10^{-4}\;\text{m} = 0.1\;\text{mm}\), Infrarot. B: \(10^{-10}\;\text{m} = 0.1\;\text{nm}\), Röntgenstrahlung. C: \(10\;\text{m}\), Radiowellen.</p><p>Je kürzer die Welle, desto höher die Frequenz (\(f = \dfrac{c}{\lambda}\)): C (\(3 \cdot 10^{7}\;\text{Hz}\)), A (\(3 \cdot 10^{12}\;\text{Hz}\)), B (\(3 \cdot 10^{18}\;\text{Hz}\)).</p>',
     mini(SPEK4)),
    ('4d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Ein Funkamateur sagt: «Meine Kurzwelle von \(20\;\text{m}\) Länge ist schneller unterwegs als das Licht meiner Lampe, weil sie länger ist.» Prüfe die Aussage und berechne die Frequenz der Kurzwelle.',
     r'<p>Die Aussage stimmt nicht: Im Vakuum (und praktisch auch in Luft) laufen alle elektromagnetischen Wellen gleich schnell. Die Länge bestimmt nicht die Geschwindigkeit, sondern zusammen mit ihr die Frequenz.</p><p>\(f = \dfrac{c}{\lambda} = \dfrac{3.00 \cdot 10^{8}\;\text{m/s}}{20\;\text{m}} = 1.5 \cdot 10^{7}\;\text{Hz} = 15\;\text{MHz}\)</p>', ''),
])
k4 = kapitel(4, 'elektromagnetische-wellen', 'Elektromagnetische Wellen und das Spektrum', 'K2 · K4', 45,
    r'Du beschreibst elektromagnetische Wellen als gekoppelte elektrische und magnetische Felder, die ohne Medium und im Vakuum alle mit \(c = 3.00 \cdot 10^{8}\;\text{m/s}\) laufen, ordnest Wellenlängen und Frequenzen ins Spektrum ein und unterscheidest sie von mechanischen Wellen und Schall.',
    ('p6-1-lp-em', 'Wellen sehen: elektromagnetische Wellen'),
    sim4, ('p6-1-lp-kontrolle-em', 'Kontrollfragen zu den elektromagnetischen Wellen'),
    fest4, [uebung('em-rechnen', 'Frequenz und Wellenlänge'), uebung('bereich', 'Wo im Spektrum?'), uebung('wellentyp', 'Welche Art Welle?')],
    auf4, f'<a href="{TS}#spektrum">Themenseite 6.1, das elektromagnetische Spektrum</a> · <a href="{TS}#definition">Grundbegriffe, elektromagnetische Wellen</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur_anim('sim5', 'Links die Energiestufen eines Modellatoms mit dem Elektron, rechts je nach Modus das Atom mit ausgesandtem Photon, ein Gas im weissen Licht oder ein Laser zwischen zwei Spiegeln', '-4 48 308 224', '',
    knoepfe('modus', 'Modus', [('emission', 'Emission'), ('absorption', 'Absorption'), ('laser', 'Laser')], 'emission'))
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Emission, Laser und Absorption</div>
          <p>Die Elektronen eines Atoms können nur bestimmte <b>Energiestufen</b> einnehmen (\(E_1, E_2, \ldots\)). Wird Energie zugeführt (Stoss, Strom, Licht), springt ein Elektron hinauf: Das Atom ist <b>angeregt</b>. Springt es von selbst zurück, wird die Differenz als <b>Photon</b> frei, zu einem zufälligen Zeitpunkt und in eine zufällige Richtung — <b>atomare Emission</b>, genauer <b>spontane Emission</b>:</p>
          <p>\[ E_\text{Photon} = E_\text{oben} - E_\text{unten} = h \cdot f \]</p>
          <p>Eine grössere Stufe gibt mehr Energie, eine höhere Frequenz und eine kürzere Wellenlänge \(\lambda = \dfrac{c}{f}\): Ist die Stufe \(k\)-mal so gross, ist \(f\) \(k\)-mal so gross und \(\lambda\) nur noch ein \(k\)-tel so gross. Weil die Stufen fest sind, sendet jedes Element nur bestimmte Wellenlängen aus (Linienspektrum).</p>
          <p><b>Laser:</b> Energie von aussen (<b>Pumpen</b>) hält viele Atome angeregt. Trifft ein Photon auf ein angeregtes Atom, löst es ein zweites aus — <b>stimulierte Emission</b>: gleiche Wellenlänge, gleiche Richtung, gleiche Phase. Zwischen zwei Spiegeln wird das Licht verstärkt; durch den teildurchlässigen Spiegel tritt der Strahl aus: einfarbig, <b>kohärent</b> (im gleichen Takt) und gebündelt.</p>
          <p><b>Absorption</b> ist die Umkehrung: Ein Atom nimmt nur ein Photon auf, dessen Energie genau zu einem Sprung nach oben passt — von der Stufe aus, auf der sein Elektron sitzt (in einem kalten Gas meist \(E_1\)); die anderen Wellenlängen gehen durch. Wie stark ein Stoff Strahlung aufnimmt, hängt darum von der Wellenlänge ab.</p>
          <p>Ein dritter Weg zu Licht: Heisse Körper wie die Sonne oder ein Glühdraht strahlen ein breites Spektrum ab, die <b>Wärmestrahlung</b>.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Grössere Stufe, längere Welle.» Umgekehrt: mehr Energie, höhere Frequenz, kürzere Welle.</p>
          <p>«Ein Laser ist einfach eine sehr helle Lampe.» Entscheidend ist, dass alle Photonen gleich sind: gleiche Wellenlänge, Richtung und Phase.</p>
        </div>
      </div>'''
NIV5 = niveau_mini('Energiestufen eines Atoms: E1 bei 0, E2 bei 3 und E3 bei 5 Kästchen; Sprung 1 von E2 nach E1 gibt 660 nm, Sprung 2 von E3 nach E1 und Sprung 3 von E3 nach E2 sind gesucht',
                   [('E_1', 0), ('E_2', 3), ('E_3', 5)], [(3, 0, 80, '1: 660 nm'), (5, 0, 150, '2: ?'), (5, 3, 210, '3: ?')])
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Eine Natriumdampflampe einer Strassenbeleuchtung leuchtet fast nur gelb, mit \(589\;\text{nm}\). Erkläre in drei Schritten, wie dieses Licht entsteht und warum es nur eine Farbe hat.',
     r'<p>1. Der Strom in der Lampe stösst die Natriumatome an: Ein Elektron springt auf eine höhere Energiestufe.</p><p>2. Es springt zurück und gibt die Differenz als Photon ab, \(E_\text{Photon} = E_\text{oben} - E_\text{unten} = h \cdot f\).</p><p>3. Natrium hat feste Stufen, und ein Sprung herrscht vor; seine Energie gehört zu \(589\;\text{nm}\). Darum leuchtet die Lampe in dieser einen Farbe und nicht weiss.</p>', ''),
    ('5b', 3, r'Im Schema eines Atoms gibt Sprung 1 (von E₂ nach E₁) rotes Licht mit \(660\;\text{nm}\). Bestimme mit den Kästchen die Wellenlängen von Sprung 2 und Sprung 3. Welche davon sieht man?',
     r'<p>Sprung 1 ist \(3\) Kästchen hoch, Sprung 2 \(5\), Sprung 3 \(2\). Die Wellenlänge ist umgekehrt proportional zur Stufe.</p><p>Sprung 2: \(\lambda = 660\;\text{nm} \cdot \dfrac{3}{5} = 396\;\text{nm}\) — violett, gerade noch sichtbar.</p><p>Sprung 3: \(\lambda = 660\;\text{nm} \cdot \dfrac{3}{2} = 990\;\text{nm}\) — Infrarot, unsichtbar.</p>',
     mini(NIV5)),
    ('5c', 3, r'Ein roter Laserpointer und eine Taschenlampe mit rotem Filter leuchten beide rot. Worin unterscheidet sich ihr Licht? Erkläre zwei Unterschiede mit der Entstehung.',
     r'<p>Wellenlänge: Der Laser leuchtet mit einer einzigen Wellenlänge; jedes Photon entsteht durch denselben Sprung. Das Filter lässt dagegen einen ganzen Bereich roter Wellenlängen durch und nimmt die übrigen Farben des Lampenlichts auf.</p><p>Richtung und Takt: Im Laser löst ein Photon ein gleiches aus, in dieselbe Richtung und im gleichen Takt — der Strahl ist gebündelt und kohärent. Die Lampe sendet ihre Photonen unabhängig voneinander in alle Richtungen.</p>', ''),
    ('5d', 3, r'<span class="task-id vert">freiwillig · Vertiefung</span> Im Licht der Sonne fehlen schmale Linien, zum Beispiel bei \(589\;\text{nm}\) — derselben Wellenlänge wie in Aufgabe 5a. Erkläre, wie diese dunkle Linie entsteht. (Die Sonne ist von einer kühleren Gashülle umgeben.)',
     r'<p>Die heisse Sonne strahlt ein breites Spektrum ab. Das Licht durchquert ihre kühlere Gashülle. Natriumatome darin nehmen genau die Photonen auf, deren Energie zu ihrem Sprung passt — die mit \(589\;\text{nm}\).</p><p>Sie strahlen diese Energie zwar wieder ab, aber in alle Richtungen; in unserer Richtung fehlt darum Licht dieser Wellenlänge: eine dunkle Linie. Absorption ist die Umkehrung der Emission.</p>', ''),
])
k5 = kapitel(5, 'licht-entsteht', 'Wie Licht entsteht und verschluckt wird', 'K4', 40,
    r'Du erklärst, wie ein Atom Licht aussendet (Elektronensprung, Photon mit der Energie der Stufe), wie ein Laser gleichartiges Licht erzeugt (stimulierte Emission) und warum ein Stoff nur bestimmte Wellenlängen aufnimmt (Absorption).',
    ('p6-1-lp-licht', 'Wellen sehen: wie Licht entsteht und verschluckt wird'),
    sim5, ('p6-1-lp-kontrolle-licht', 'Kontrollfragen zu Emission, Laser und Absorption'),
    fest5, [uebung('stufen', 'Stufe und Wellenlänge'), uebung('licht-aussage', 'Richtig oder falsch?')],
    auf5, f'<a href="{TS}#emission">Themenseite 6.1, atomare Emission und Laser</a> · <a href="{TS}#absorption">Wellenlängenabhängige Absorption</a>')

# ------------------------------------------------------------------ Kapitel 6
sim6 = figur('sim6', 'Strahlung der Sonne und des Bodens über der Wellenlänge, grau die Bereiche, in denen die gewählten Gase aufnehmen; darunter ein Schema mit den Anteilen', '-4 -4 308 300',
    '        <div class="reglerfeld">\n          '
    + regler('s6', 'ppm', 'CO₂-Gehalt', 0, 800, 10, 430, 'ppm', 0) + '\n        </div>',
    knoepfe=knoepfe('gase', 'Gase', [('0', 'keine Treibhausgase'), ('1', '+ Wasserdampf'), ('2', '+ Kohlendioxid'), ('3', '+ Methan, Ozon')], '2'))
fest6 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Treibhauseffekt: eine Frage der Wellenlänge</div>
          <p>Jeder Körper strahlt; je heisser er ist, desto kürzer die Wellenlänge, bei der er am meisten strahlt. Die Sonne (rund \(5800\;\text{K}\)) strahlt je Mikrometer am stärksten um \(0.5\;\mu\text{m}\), im sichtbaren Licht. Der Boden (rund \(15\;^\circ\text{C}\), also \(288\;\text{K}\)) strahlt im Infrarot, je Mikrometer am stärksten um \(10\;\mu\text{m}\) — rund zwanzigmal langwelliger. (In der Simulation ist die Strahlung flächentreu über der logarithmischen Achse gezeichnet; ihre Gipfel liegen darum bei rund \(0.6\) und \(13\;\mu\text{m}\).)</p>
          <p><b>Treibhausgase</b> nehmen Infrarot in bestimmten Bereichen auf: <b>Wasserdampf</b> (um \(6\;\mu\text{m}\) und über \(20\;\mu\text{m}\); das wichtigste natürliche Treibhausgas), <b>Kohlendioxid</b> (um \(15\;\mu\text{m}\)), <b>Methan</b> (um \(7.7\;\mu\text{m}\)) und <b>Ozon</b> (um \(9.6\;\mu\text{m}\)). Ihre Moleküle haben Energiestufen, die zu diesen Photonen passen (Absorption, Kapitel 5). Stickstoff und Sauerstoff, rund \(99\;\%\) der Luft, nehmen fast nichts auf. Zwischen rund \(8\) und \(13\;\mu\text{m}\) bleibt ein «Fenster», in dem nur das Ozon schmal aufnimmt.</p>
          <p>Auch auf dem Hinweg nimmt die Atmosphäre etwas auf: Das <b>Ultraviolett</b> der Sonne nimmt zum grossen Teil das <b>Ozon</b> in rund \(20\) bis \(30\;\text{km}\) Höhe auf (Ozonschicht); das schützt vor Sonnenbrand. Zudem nimmt Ozon Infrarot um \(9.6\;\mu\text{m}\) auf — es ist selbst ein Treibhausgas. Mit dem Ozonloch hat der Treibhauseffekt dagegen nichts zu tun.</p>
          <p><b>Treibhauseffekt:</b> Das Sonnenlicht kommt weitgehend durch und erwärmt den Boden. Dessen Wärmestrahlung nehmen die Treibhausgase zu einem grossen Teil auf und strahlen sie in alle Richtungen wieder ab, auch zurück zum Boden. So bleibt Energie in Bodennähe: im Mittel rund \(+15\;^\circ\text{C}\) statt rund \(-18\;^\circ\text{C}\) ohne Treibhausgase.</p>
          <p><b>Mehr Treibhausgas</b> — Kohlendioxid heute rund \(430\;\text{ppm}\) statt \(280\;\text{ppm}\) vor der Industrialisierung, vor allem aus Erdöl, Erdgas und Kohle — verbreitert die Bereiche, in denen die Luft aufnimmt: Der Effekt wird stärker, die Erde wärmer. Wie viel Energie das ausmacht, rechnet das Einschichtmodell im <a href="''' + LPW + '''#treibhauseffekt">Leitprogramm Wärme, Kapitel 7</a>.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Atmosphäre spiegelt die Wärme zurück wie ein Glashaus.» Die Gase nehmen die Strahlung auf und strahlen sie nach allen Seiten ab, nur ein Teil davon nach unten.</p>
          <p>«Kohlendioxid hält das Sonnenlicht ab.» Es nimmt fast nur Infrarot auf — es wirkt auf dem Rückweg der Strahlung, nicht auf dem Hinweg.</p>
          <p>Treibhauseffekt und Ozonloch verwechselt: Das Ozonloch betrifft das Ultraviolett der Sonne, nicht die Wärmestrahlung.</p>
        </div>
      </div>'''
DURCH6 = durchlass_mini('Durchgelassener Anteil der Atmosphäre über der Wellenlänge, 0.1 bis 100 Mikrometer: grau und null zwischen 5.5 und 8 Mikrometer, 9.3 und 10.1 Mikrometer, 13.5 und 17 Mikrometer sowie über 20 Mikrometer; A bei 0.5, B bei 11 und C bei 14 Mikrometer',
                        [(0.5, 'A'), (11, 'B'), (14, 'C')])
auf6 = test('t6', 'Aufgaben · Kapitel 6', 9, [
    ('6a', 3, r'In einer klaren, trockenen Wüstennacht kühlt der Boden viel stärker ab als in einer feuchten Nacht in den Tropen. Erkläre das mit der Wellenlänge und dem Wasserdampf.',
     r'<p>Nachts strahlt der Boden nur noch ab, im Infrarot um \(10\;\mu\text{m}\).</p><p>In den Tropen enthält die Luft viel Wasserdampf. Er nimmt die Wärmestrahlung in seinen Bereichen auf und strahlt einen Teil zurück zum Boden; der Boden kühlt langsam ab.</p><p>In der trockenen Wüstenluft fehlt der Wasserdampf fast ganz: Die Strahlung geht weitgehend ungehindert ins All, der Boden kühlt stark ab.</p>', ''),
    ('6b', 3, r'Das Diagramm zeigt vereinfacht, welchen Anteil die heutige Atmosphäre (Wasserdampf, Kohlendioxid, Methan und Ozon) je Wellenlänge durchlässt. Welche der Strahlungen A, B und C kommt durch? Woher stammt jede vor allem — von der Sonne oder vom Boden? Welches Gas hält C auf?',
     r'<p>A (\(0.5\;\mu\text{m}\)): kommt durch — sichtbares Licht der Sonne.</p><p>B (\(11\;\mu\text{m}\)): kommt durch — Wärmestrahlung des Bodens im Fenster zwischen rund \(8\) und \(13\;\mu\text{m}\) (nur das Ozon nimmt darin schmal um \(9.6\;\mu\text{m}\) auf).</p><p>C (\(14\;\mu\text{m}\)): wird aufgenommen — Wärmestrahlung des Bodens, im Bereich des Kohlendioxids um \(15\;\mu\text{m}\).</p>',
     mini(DURCH6)),
    ('6c', 3, r'Wasserdampf nimmt Strahlung um \(6.3\;\mu\text{m}\) auf. Berechne ihre Frequenz und die von grünem Licht mit \(0.50\;\mu\text{m}\). Wievielmal grösser ist die Frequenz des Lichts? Welche Photonen tragen mehr Energie?',
     r'<p>\(f = \dfrac{c}{\lambda} = \dfrac{3.00 \cdot 10^{8}\;\text{m/s}}{6.3 \cdot 10^{-6}\;\text{m}} \approx 4.8 \cdot 10^{13}\;\text{Hz}\)</p><p>\(f = \dfrac{3.00 \cdot 10^{8}\;\text{m/s}}{0.50 \cdot 10^{-6}\;\text{m}} = 6.0 \cdot 10^{14}\;\text{Hz}\)</p><p>Bei gleichem \(c\) stehen die Frequenzen umgekehrt wie die Wellenlängen: \(\dfrac{6.3\;\mu\text{m}}{0.50\;\mu\text{m}} = 12.6 \approx 13\). Die Frequenz des Lichts ist rund dreizehnmal so gross, und nach \(E = h \cdot f\) trägt jedes seiner Photonen rund dreizehnmal so viel Energie.</p>', ''),
])
k6 = kapitel(6, 'treibhauseffekt', 'Treibhauseffekt: Absorption nach Wellenlänge', 'K5', 40,
    r'Du beschreibst den Treibhauseffekt mit der wellenlängenabhängigen Absorption: Die Atmosphäre lässt das kurzwellige Sonnenlicht durch, Treibhausgase nehmen die langwellige Wärmestrahlung des Bodens auf und strahlen sie in alle Richtungen ab; und du erklärst, warum mehr Treibhausgas den Effekt verstärkt.',
    ('p6-1-lp-treibhaus', 'Wellen sehen: der Treibhauseffekt im Spektrum'),
    sim6, ('p6-1-lp-kontrolle-treibhaus', 'Kontrollfragen zum Treibhauseffekt'),
    fest6, [uebung('zuordnen', 'Sonne oder Boden?'), uebung('treibhaus-aussage', 'Richtig oder falsch?')],
    auf6, f'<a href="{TS}#absorption">Themenseite 6.1, wellenlängenabhängige Absorption und Treibhauseffekt</a> · <a href="{LPW}#treibhauseffekt">Leitprogramm Wärme, Kapitel 7: die Energiebilanz</a>')


# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/wellen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">6.1 · K1 bis K5</span><span class="zeit">≈ 40 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k2">2</a> → K1 · G2 → <a href="#k3">3</a> → K1, K2 · G3 → <a href="#k1">1</a>, d) <a href="#k3">3</a> → K1, K2, K3 · G4 → <a href="#k3">3</a> und <a href="#k4">4</a> → K2, K4 · G5 → <a href="#k5">5</a> → K4 · G6 → <a href="#k6">6</a> → K5</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Reflexion am festen und losen Ende, Überlagerung zweier Wellen, stehende Wellen und die Eigenschwingungen einer Saite → <a href="{TSA}#reflexion">Vertiefung 6.1a, Wellenexperimente</a></li>
        <li>Die Gleichung der Welle \(y(s, t) = A \cdot \sin\!\big(2\pi\,(t/T - s/\lambda)\big)\) → <a href="{TSA}#gesichter">Vertiefung 6.1a, die zwei Gesichter der Welle</a></li>
        <li>Die Bahnen der Wasserteilchen in der Tiefe → <a href="{TS}#definition">Themenseite 6.1, Animation 1</a></li>
        <li>Die Photonenergie in Zahlen (Elektronvolt) → <a href="{TS}#spektrum">Themenseite 6.1, Animation 5</a></li>
        <li>Die Energiebilanz der Erde und das Einschichtmodell der Atmosphäre mit Temperaturen → <a href="{LPW}#treibhauseffekt">Leitprogramm Wärme, Kapitel 7</a></li>
        <li>Brechung, Beugung und Interferenz stehen nicht in den Kompetenzen zu 6.1.</li>
      </ul>
      <p>Weiter im Lerngebiet 6: <a href="leitprogramm-elektrizitaet.html">Leitprogramm Elektrizität</a> (6.2).</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Wellen, Version 1.0 (08.10.2026), Erprobung: unverlinkt bis nach /lp-pruefung.
     Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip mit vorgerechnetem Problem → ② laufende Simulation mit Aufgabenleiste →
     ③ Kontrollclip mit Fragen → Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/wellen/*.tex).
     Quelle: scripts/lp/wellen/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 6.1 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 die Arten der Wellenerzeugung allgemein beschreiben und sie grafisch sowie algebraisch
          charakterisieren (Frequenz, Periode, Wellenlänge, Phasengeschwindigkeit)
       K2 die wichtigsten Wellentypen (mechanische Wellen, Schallwellen, elektromagnetische Wellen)
          aufzeigen und unterscheiden
       K3 die Wellenerzeugung am Beispiel der mechanischen Wellen aufzeigen
       K4 die Besonderheiten elektromagnetischer Wellen (Beschaffenheit, Spektrum, Geschwindigkeit, ihre
          Erzeugung (atomare Emission, Laser) und ihre Absorption) beschreiben
       K5 den Treibhaus-Effekt mit der wellenlängenabhängigen Absorption von Sonnen- und Wärmestrahlung in
          der Atmosphäre und die Bedeutung der Treibhaus-Gase beschreiben

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1 (Erreger, f = 1/T, c = s/t), 2 (grafisch: Momentbild, Zeitdiagramm, c = λ/T), 3 (algebraisch:
            c = λ · f, Sender und Medium) · Leisten sim1 A2, A4, A5, sim2 A1–A5, sim3 A1–A4 · Übungen «periode»,
            «laufzeit», «ablesen», «phasengeschw», «wellengleichung», «medium» · Kontrollclips 1 (F3, F4), 2 (F1–F5),
            3 (F1, F2, F5) · Aufg. 1b, 2a–2d, 3a, 3c · G1, G2, G3 d
       K2 → Kap. 1 (Quer- und Längswelle, mechanische Wellen), 3 (Schall braucht ein Medium), 4 (elektromagnetisch
            gegen mechanisch, Vergleichstabelle) · Übungen «quer-laengs», «hoerbar», «wellentyp» · Kontrollclips
            1 (F2), 3 (F4), 4 (F1, F5) · Aufg. 1d, 3b, 4a · G2 d, G3 a, G4 b/c
       K3 → Kap. 1 · sim1 · Kontrollclip 1 (F1, F5) · Aufg. 1a, 1c · G3
       K4 → Kap. 4 (Beschaffenheit, Spektrum, Geschwindigkeit), 5 (atomare Emission, Laser, Absorption) · sim4, sim5 ·
            Übungen «em-rechnen», «bereich», «stufen», «licht-aussage» · Kontrollclips 4, 5 · Aufg. 4b–4d, 5a–5d ·
            G4, G5
       K5 → Kap. 6 · sim6 · Übungen «zuordnen», «treibhaus-aussage» · Kontrollclip 6 · Aufg. 6a–6c · G6
     Planungstabelle (Lernziel · Clip · Erkundung · Problem im Clip · häufiger Fehler · min):
       1 Schwingung → Welle, quer/längs · p6-1-lp-welle · sim1 Teilchenkette mit Erreger · Seil: Hand 5-mal in
         4.0 s, Band 3.6 m nach 2.4 s · «die Welle trägt das Wasser mit» · 45
       2 Momentbild und Zeitdiagramm · p6-1-lp-diagramme · sim2 zwei Diagramme an zwei Reglern · Wellenbad:
         λ = 5.0 m, T = 2.0 s · λ im Zeitdiagramm abgelesen · 40
       3 Sender und Medium, Schall · p6-1-lp-medium · sim3 zwei Seile · 850 Hz von Luft in Wasser ·
         «höhere Frequenz, schnellere Welle» · 45
       4 Elektromagnetische Wellen, Spektrum · p6-1-lp-em · sim4 Geräte im Spektrum und Feldbild · UKW-Sender
         88.0 MHz, 45 km · «Radiowellen sind Schall», 340 m/s eingesetzt · 45
       5 Emission, Laser, Absorption · p6-1-lp-licht · sim5 Modellatom mit drei Stufen · Neon 640 nm, Stufe
         1.25-mal · «grössere Stufe, längere Welle» · 40
       6 Treibhauseffekt · p6-1-lp-treibhaus · sim6 Durchlässigkeit nach Wellenlänge · Kohlendioxid bei 15 µm:
         Frequenz, Sonne oder Boden? · «Spiegel», Ozon und Treibhauseffekt verwechselt · 40
     Kern: alle Kapitel; Vertiefung (freiwillig, nicht in den Zeiten): Aufgaben 1d, 2d, 3d, 4d, 5d. Bewusst
     weggelassen: Reflexion, Überlagerung, stehende Wellen (6.1a), die Wellengleichung y(s, t), Bahnen der
     Wasserteilchen in der Tiefe, Photonenergie in Elektronvolt, Energiebilanz der Atmosphäre (Leitprogramm Wärme).
     Konventionen wie Themenseite 6.1: f, T, λ, c (Phasengeschwindigkeit, Ausbreitungsgeschwindigkeit), A; Ort s
     (wie 6.1a: Momentbild y(s), Zeitdiagramm y(t)); Schall in Luft 340 m/s (15 °C), Helium 980, Wasser ≈ 1500,
     Eisen 5170 m/s; c = 3.00·10⁸ m/s; sichtbares Licht 380 bis 780 nm; Bereichsgrenzen des Spektrums wie
     Animation 5 der Themenseite. Widersprüche der Themenseite: siehe README.md.
     Zeiten (Clips 6, Leiste 10, Festhalten 4, Übungen 8 bis 12, drei Aufgaben 12 min; ohne Vertiefung):
     K0 15 · K1 45 · K2 40 · K3 45 · K4 45 · K5 40 · K6 40 · Gesamttest 40 = 310 min ≈ 6.9 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Wellen</h1>
      <p class="unter">Von der Schwingung zur Welle, Momentbild und Zeitdiagramm, Sender und Medium, elektromagnetische Wellen, Emission und Laser, Treibhauseffekt — mit laufenden Simulationen. Sechs Kapitel zu je 40 bis 45 Minuten, dazu Vorwissen und Gesamttest — zusammen rund sieben Lektionen; die Vertiefungsaufgaben sind freiwillig.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 6 · Teilgebiet 6.1</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Von der Schwingung zur Welle</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Momentbild und Zeitdiagramm</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Sender und Medium</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Elektromagnetische Wellen</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Emission, Laser, Absorption</span></a></li></ol>
    <p class="lekt">Lektion 6</p>
    <ol><li><a href="#k6"><span class="nr">6</span><span>Treibhauseffekt</span></a></li></ol>
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
          <li><b>① Clip</b> anschauen — er rechnet ein Problem vor und hält einmal an: Wie gehst du vor?</li>
          <li><b>② Tüfteln:</b> Manche Simulationen laufen auf Knopfdruck (Start, Pause), andere folgen den Reglern. Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt; deine Antwort notierst du und vergleichst sie dann.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma; Brüche wie <code>1/2</code> und Zehnerpotenzen wie <code>2.4e-3</code> gehen auch. Richtig ist, was auf drei signifikante Stellen stimmt; abgelesene Werte auf ein Drittel eines Kästchens.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 6, Teilgebiet 6.1 Wellen</p>
        <ul>
          <li><b>K1</b> die Arten der Wellenerzeugung allgemein beschreiben und sie grafisch sowie algebraisch charakterisieren (Frequenz, Periode, Wellenlänge, Phasengeschwindigkeit)</li>
          <li><b>K2</b> die wichtigsten Wellentypen (mechanische Wellen, Schallwellen, elektromagnetische Wellen) aufzeigen und unterscheiden</li>
          <li><b>K3</b> die Wellenerzeugung am Beispiel der mechanischen Wellen aufzeigen</li>
          <li><b>K4</b> die Besonderheiten elektromagnetischer Wellen (Beschaffenheit, Spektrum, Geschwindigkeit, ihre Erzeugung (atomare Emission, Laser) und ihre Absorption) beschreiben</li>
          <li><b>K5</b> den Treibhaus-Effekt mit der wellenlängenabhängigen Absorption von Sonnen- und Wärmestrahlung in der Atmosphäre und die Bedeutung der Treibhaus-Gase beschreiben</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">6.1 Wellen</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Wellen · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Schwingung und Welle') + k1 + band(2, 'Momentbild und Zeitdiagramm') + k2
        + band(3, 'Sender und Medium') + k3 + band(4, 'Elektromagnetische Wellen') + k4 + band(5, 'Emission und Laser') + k5
        + band(6, 'Treibhauseffekt') + k6 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
