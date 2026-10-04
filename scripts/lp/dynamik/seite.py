"""Baut leitprogramme/leitprogramm-dynamik.html aus einer Kapitelbeschreibung (seit 04.10.2026).

  python3 scripts/lp/dynamik/seite.py

Drittes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4), als Kopie von
scripts/lp/kinematik/ entstanden: Kopf, CSS, Grundskript und Bausteine von dort, neu sind
Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Siehe README.md.
"""
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-dynamik.html'
TS = '../themen/p4-2-dynamik.html'

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
<title>Leitprogramm Dynamik</title>
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
/* Diagramme und Szenen: Farben wie auf Themenseite 4.2 (STYLEGUIDE §5.2) — v Grün,
   a Violett, Antriebs-, Zug-, Faden- und Normalkraft Blau, Gewichtskraft Bernstein,
   Widerstand und Zentripetalkraft Rot; Ziele Lila gestrichelt, voriger Lauf grau gestrichelt */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.hilf-text{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.sim .zielkurve{fill:none;stroke:var(--lila);stroke-width:3;stroke-dasharray:7 5;opacity:.9}
.vorher{fill:none;stroke:var(--tinte-2);stroke-width:1.8;stroke-dasharray:5 4;opacity:.6}
.kurve-v{fill:none;stroke:var(--gruen);stroke-width:2.6}
.p-v{fill:var(--gruen)}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.boden{stroke:var(--tinte-2);stroke-width:2}
.markierung{stroke:var(--tinte-2);stroke-width:2;opacity:.5}
.wagen{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.6}
.rad{fill:var(--tinte-2)}
.velo-rad{fill:none;stroke:var(--tinte);stroke-width:2} .speiche{stroke:var(--tinte-2);stroke-width:.9} .rahmen{fill:none;stroke:var(--tinte-2);stroke-width:2.2;stroke-linejoin:round}
.pf-linie{stroke-width:2.6;fill:none}
.pf-linie.pf-v{stroke:var(--gruen)} .pf-kopf.pf-v{fill:var(--gruen)}
.pf-linie.pf-a{stroke:var(--lila)} .pf-kopf.pf-a{fill:var(--lila)}
.pf-linie.pf-f{stroke:var(--blau)} .pf-kopf.pf-f{fill:var(--blau)}
.pf-linie.pf-g{stroke:var(--bernstein)} .pf-kopf.pf-g{fill:var(--bernstein)}
.pf-linie.pf-w,.pf-linie.pf-z{stroke:var(--rot)} .pf-kopf.pf-w,.pf-kopf.pf-z{fill:var(--rot)}
.pf-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:3.5px;paint-order:stroke}
text.pf-v{fill:var(--gruen)} text.pf-a{fill:var(--lila)} text.pf-f{fill:var(--blau)} text.pf-g{fill:var(--bernstein)} text.pf-w,text.pf-z{fill:var(--rot)}
.schacht{fill:var(--papier-2);stroke:var(--linie)}
.wandmarke{stroke:var(--tinte-2);stroke-width:1.4;opacity:.6}
.kabine{fill:var(--karte);stroke:var(--tinte);stroke-width:1.8}
.seil,.faden,.schnur{stroke:var(--tinte);stroke-width:1.4;fill:none}
.waage{fill:var(--tinte-2)}
.mensch{fill:none;stroke:var(--tinte);stroke-width:2.2;stroke-linecap:round}
.anzeige{fill:var(--papier-2);stroke:var(--tinte-2)}
.anzeige-zahl{fill:var(--tinte);font-family:var(--mono);font-size:13px;font-weight:700}
.tisch{fill:var(--tinte-2)}
.rolle{fill:var(--karte);stroke:var(--tinte);stroke-width:1.6}
.gewicht{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.6}
.bahn-kreis{fill:none;stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:4 4}
.flugbahn{stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:3 4}
.kugel{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.8}
.knoten{fill:var(--tinte)}
.bt-text{fill:var(--tinte);font-family:var(--sans);font-size:11px}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
.sim-aktionen{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:2px 0 8px}
.sim-aktionen .aktion{font-family:var(--sans);font-size:.82rem;font-weight:600;cursor:pointer;border-radius:999px;padding:5px 14px;
  border:1px solid var(--bernstein-rand);background:var(--bernstein-hell);color:var(--tinte)}
.sim-aktionen .aktion:hover{box-shadow:var(--sl)}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.kurve-v{stroke:var(--gruen);stroke-width:2.2} .kurve-mini.kurve-f{stroke:var(--rot);stroke-width:2.2}
svg.mini.breit{width:260px}
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
  var KEY = 'leitprogramm-dynamik-v1';

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
  <p>Leitprogramm · Dynamik</p>
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.0 · Stand 4. Oktober 2026</p>
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">4.2 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


def vt_bild(punkte, xmax, ymax, xt, yt, label, yname='v [m/s]'):
    """Statisches v-t-Diagramm für Aufgaben: Streckenzug durch Punkte auf Gitterpunkten."""
    w, h, ox, oy = 230, 140, 34, 118
    kx, ky = (w - ox - 14) / xmax, (oy - 16) / ymax
    t = [f'<svg class="mini breit" viewBox="0 0 {w} {h + 8}" role="img" aria-label="{label}">']
    for x in range(0, xmax + 1, xt):
        t.append(f'<line x1="{ox + x * kx:.1f}" y1="{oy - ymax * ky:.1f}" x2="{ox + x * kx:.1f}" y2="{oy}" class="gitter"/>')
        if x: t.append(f'<text x="{ox + x * kx:.1f}" y="{oy + 13}" text-anchor="middle" class="skala">{x}</text>')
    for y in range(0, ymax + 1, yt):
        t.append(f'<line x1="{ox}" y1="{oy - y * ky:.1f}" x2="{ox + xmax * kx:.1f}" y2="{oy - y * ky:.1f}" class="gitter"/>')
        if y: t.append(f'<text x="{ox - 5}" y="{oy - y * ky + 4:.1f}" text-anchor="end" class="skala">{y}</text>')
    t.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + xmax * kx + 8:.1f}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - ymax * ky - 8:.1f}" class="achse"/>')
    t.append('<polyline points="' + ' '.join(f'{ox + x * kx:.1f},{oy - y * ky:.1f}' for x, y in punkte) + '" class="kurve-mini kurve-v"/>')
    for x, y in punkte:
        t.append(f'<circle cx="{ox + x * kx:.1f}" cy="{oy - y * ky:.1f}" r="3" class="p-mini"/>')
    t.append(f'<text x="{ox + xmax * kx + 8:.1f}" y="{oy - 6}" text-anchor="end" class="achsname">t [s]</text><text x="{ox + 6}" y="{oy - ymax * ky - 2:.1f}" class="achsname">{yname}</text></svg>')
    return ''.join(t)


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P01 = '../themen/p0-1-vorwissen-mathematik.html'
P03 = '../themen/p0-3-messen-waagen-dichte.html'
TK = '../themen/p4-1-kinematik.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.3 · 4.1</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Beschleunigung und Bewegungsgleichungen aus 4.1, Masse und Gewichtskraft, Gleichungen umstellen. Wenn das wackelt: <a href="leitprogramm-kinematik.html">Leitprogramm Kinematik</a> und <a href="leitprogramm-vorwissen.html">Leitprogramm Grössen, Messen, Druck</a>.</p>
      ''' + clipkarte('p0-3-masse-gewicht', 'Masse und Gewicht: was die Waage wirklich zeigt') + r'''
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Ein Auto beschleunigt gleichmässig in \(5\;\text{s}\) aus dem Stand auf \(20\;\text{m/s}\). Wie gross ist die Beschleunigung, und welchen Weg legt es dabei zurück?',
     r'<p>\(a = \dfrac{\Delta v}{\Delta t} = \dfrac{20\;\text{m/s}}{5\;\text{s}} = 4\;\text{m/s}^2\), \(s = \tfrac12 \cdot a \cdot t^2 = \tfrac12 \cdot 4\;\text{m/s}^2 \cdot (5\;\text{s})^2 = 50\;\text{m}\).</p><p class="komm">Falsch? <a href="leitprogramm-kinematik.html#k2">Leitprogramm Kinematik, Kapitel 2</a></p>', ''),
    ('0b', 2, r'Ein Rucksack hat \(8\;\text{kg}\). Ist das seine Masse oder seine Gewichtskraft? Wie gross ist seine Gewichtskraft auf der Erde (\(g = 9.81\;\text{m/s}^2\))?',
     r'<p>\(8\;\text{kg}\) ist die Masse. \(F_G = m \cdot g = 8\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 78.5\;\text{N}\).</p><p class="komm">Falsch? Der Clip oben und <a href="' + P03 + r'#masse-kraft">Vorwissen 0.3, Masse und Gewicht</a></p>', ''),
    ('0c', 3, r'Stelle \(F = m \cdot a\) nach \(m\) und nach \(a\) um, und \(F = \dfrac{m \cdot v^2}{r}\) nach \(v\).',
     r'<p>\(m = \dfrac{F}{a}\), \(a = \dfrac{F}{m}\), \(v = \sqrt{\dfrac{F \cdot r}{m}}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umstellen</a></p>', ''),
    ('0d', 2, r'Ein Körper fährt mit \(10\;\text{m/s}\) auf einem Kreis mit \(r = 20\;\text{m}\). Wie gross ist seine Zentripetalbeschleunigung?',
     r'<p>\(a_z = \dfrac{v^2}{r} = \dfrac{(10\;\text{m/s})^2}{20\;\text{m}} = 5\;\text{m/s}^2\).</p><p class="komm">Falsch? <a href="leitprogramm-kinematik.html#k5">Leitprogramm Kinematik, Kapitel 5</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Wagen auf einer reibungsfreien Bahn, darunter das v-t-Diagramm, das während der Fahrt entsteht', '-4 22 308 296',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'F', '<i>F</i> Kraft', 0, 20, 1, 4, 'N', 0) + '\n          '
    + regler('s1', 'm', '<i>m</i> Masse', 0.5, 8, 0.5, 2, 'kg', 1) + '\n        </div>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Kraft, Masse, Beschleunigung</div>
          <p><b>Kraft:</b> die Ursache dafür, dass ein Körper beschleunigt (oder verformt) wird. Kräfte sind Vektoren; man erkennt sie an ihrer Wirkung. Einheit: das Newton, \(1\;\text{N} = 1\;\text{kg} \cdot \text{m/s}^2\).</p>
          <p><b>Grundgesetz</b> (zweites newtonsches Gesetz): Die Gesamtkraft auf einen Körper ist Masse mal Beschleunigung, und Kraft und Beschleunigung zeigen in dieselbe Richtung.</p>
          <p>\[ F_\text{ges} = m \cdot a \qquad a = \frac{F_\text{ges}}{m} \]</p>
          <p>Doppelte Kraft bei gleicher Masse: doppelte Beschleunigung. Doppelte Masse bei gleicher Kraft: halbe Beschleunigung. Die Masse ist das Mass für die Trägheit eines Körpers.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Kraft bestimmt die Geschwindigkeit.» Sie bestimmt deren <em>Änderung</em>: Eine konstante Kraft von \(4\;\text{N}\) auf \(2\;\text{kg}\) macht den Wagen jede Sekunde um \(2\;\text{m/s}\) schneller — nicht \(2\;\text{m/s}\) schnell.</p>
          <p>Masse in Gramm eingesetzt: \(4\;\text{N}\) auf \(500\;\text{g}\) gibt \(a = \dfrac{4\;\text{N}}{0.5\;\text{kg}} = 8\;\text{m/s}^2\), nicht \(0.008\;\text{m/s}^2\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 3, r'Ein Velo samt Fahrerin (\(80\;\text{kg}\)) wird mit einer Gesamtkraft von \(120\;\text{N}\) aus dem Stand beschleunigt. Wie gross ist die Beschleunigung? Wie schnell ist das Velo nach \(4\;\text{s}\), und welchen Weg hat es dann zurückgelegt?',
     r'<p>\(a = \dfrac{F_\text{ges}}{m} = \dfrac{120\;\text{N}}{80\;\text{kg}} = 1.5\;\text{m/s}^2\).</p><p>\(v = a \cdot t = 1.5\;\text{m/s}^2 \cdot 4\;\text{s} = 6\;\text{m/s}\), \(s = \tfrac12 \cdot a \cdot t^2\) \(= \tfrac12 \cdot 1.5\;\text{m/s}^2 \cdot (4\;\text{s})^2\) \(= 12\;\text{m}\).</p>', ''),
    ('1b', 3, r'Auf zwei Wagen A und B wirkt dieselbe Kraft. Das Diagramm zeigt ihre Geschwindigkeit. A hat \(2\;\text{kg}\). Wie gross ist die Kraft, und welche Masse hat B? (Punkte auf Gitterpunkten)',
     r'<p>A: \(a = \dfrac{\Delta v}{\Delta t} = \dfrac{6\;\text{m/s}}{2\;\text{s}} = 3\;\text{m/s}^2\), also \(F = m \cdot a = 2\;\text{kg} \cdot 3\;\text{m/s}^2 = 6\;\text{N}\).</p><p>B: \(a = \dfrac{\Delta v}{\Delta t} = \dfrac{6\;\text{m/s}}{8\;\text{s}} = 0.75\;\text{m/s}^2\), also \(m = \dfrac{F}{a} = \dfrac{6\;\text{N}}{0.75\;\text{m/s}^2} = 8\;\text{kg}\) — viermal so viel Masse, darum ein Viertel der Beschleunigung.</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="3;0.75" data-namen="A;B" data-farbe="kurve-v" data-fenster="8,12" data-teilung="1,2" data-punkte="2,6;8,6" data-xname="t [s]" data-yname="v [m/s]" aria-label="v-t-Diagramm mit zwei Ursprungsgeraden A und B"></svg></div>'),
    ('1c', 2, r'Warum braucht ein voll beladener Lastwagen bei gleicher Antriebskraft länger als ein leerer, um auf \(50\;\text{km/h}\) zu kommen?',
     r'<p>Beladen hat er die grössere Masse. Nach \(a = \dfrac{F}{m}\) ist bei gleicher Kraft die Beschleunigung kleiner, er braucht also mehr Zeit für dieselbe Geschwindigkeitsänderung. Die Masse macht den Körper träger.</p>', ''),
    ('1d', 3, r'Ein Sprinter (\(75\;\text{kg}\)) erreicht aus dem Stand in \(2.5\;\text{s}\) gleichmässig \(9\;\text{m/s}\). Wie gross ist die Kraft, mit der er sich im Mittel vorwärts stösst?',
     r'<p>\(a = \dfrac{\Delta v}{\Delta t} = \dfrac{9\;\text{m/s}}{2.5\;\text{s}} = 3.6\;\text{m/s}^2\).</p><p>\(F = m \cdot a = 75\;\text{kg} \cdot 3.6\;\text{m/s}^2 = 270\;\text{N}\).</p>', ''),
])
k1 = kapitel(1, 'kraft-masse-beschleunigung', 'Kraft, Masse, Beschleunigung', 'K1', 40,
    r'Du beschreibst die Kraft als Ursache einer Bewegungsänderung und den Zusammenhang \(F_\text{ges} = m \cdot a\): doppelte Kraft, doppelte Beschleunigung; doppelte Masse, halbe Beschleunigung.',
    ('p4-2-lp-grundgesetz', 'Kraft sehen: doppelte Kraft, doppelte Beschleunigung', None),
    sim1, ('p4-2-lp-kontrolle-grundgesetz', 'Kontrollfragen zu Kraft, Masse und Beschleunigung', None),
    fest1, [uebung('fma', 'Kraft, Masse oder Beschleunigung'), uebung('anfahren', 'Anfahren aus dem Stand'),
            uebung('faktor', 'Was ändert sich?')],
    auf1, f'<a href="{TS}#definition">Themenseite 4.2, Grundbegriffe</a> · <a href="{TS}#grundgesetz">Das Grundgesetz</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur_anim('sim2', 'Velo mit Antriebs- und Widerstandskraft, die Strasse zieht vorbei; darunter das v-t-Diagramm der Fahrt', '-4 -4 308 322',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'v0', '<i>v</i>₀ Start', 0, 8, 1, 0, 'm/s', 0) + '\n          '
    + regler('s2', 'FA', '<i>F</i><sub>A</sub> Antrieb', 0, 120, 5, 60, 'N', 0) + '\n          '
    + regler('s2', 'FW', '<i>F</i><sub>W</sub> Widerstand', 0, 120, 5, 20, 'N', 0) + '\n        </div>\n'
    + '        <p class="sim-notiz">Velo mit Fahrerin: \\(m = 80\\;\\text{kg}\\). Der Widerstand wirkt gegen die Bewegung.</p>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Gesamtkraft und Trägheit</div>
          <p>Wirken mehrere Kräfte auf einer Geraden, zählt nur ihre Summe mit Vorzeichen, die <b>Gesamtkraft</b>: Kräfte in Bewegungsrichtung positiv, Kräfte dagegen negativ.</p>
          <p>\[ F_\text{ges} = F_A - F_W \qquad a = \frac{F_\text{ges}}{m} \]</p>
          <p><b>Trägheitsgesetz</b> (erstes newtonsches Gesetz): Ist die Gesamtkraft null, ist auch die Beschleunigung null. Der Körper behält seinen Bewegungszustand — er bleibt in Ruhe oder fährt mit konstanter Geschwindigkeit geradeaus weiter.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Wer fährt, braucht eine Kraft in Fahrtrichtung.» Bei konstantem Tempo ist die Gesamtkraft null: Der Antrieb gleicht nur den Widerstand aus. Ohne Widerstand, etwa ein Puck auf glattem Eis, gleitet ein Körper ganz ohne Kraft weiter.</p>
          <p>Kräfte in Gegenrichtung addiert: \(70\;\text{N}\) Zug und \(25\;\text{N}\) Reibung geben \(F_\text{ges} = 45\;\text{N}\), nicht \(95\;\text{N}\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Ein Schlitten (\(30\;\text{kg}\)) wird mit \(90\;\text{N}\) gezogen; die Reibung beträgt \(30\;\text{N}\). Wie gross sind Gesamtkraft und Beschleunigung? Wie schnell ist er nach \(5\;\text{s}\), wenn er aus dem Stand startet?',
     r'<p>\(F_\text{ges} = F_A - F_W = 90\;\text{N} - 30\;\text{N} = 60\;\text{N}\), \(a = \dfrac{F_\text{ges}}{m} = \dfrac{60\;\text{N}}{30\;\text{kg}} = 2\;\text{m/s}^2\).</p><p>\(v = a \cdot t = 2\;\text{m/s}^2 \cdot 5\;\text{s} = 10\;\text{m/s}\).</p>', ''),
    ('2b', 3, r'Das Diagramm zeigt die Fahrt eines Wagens (\(50\;\text{kg}\)). In welcher Phase ist die Gesamtkraft positiv, null, negativ? Wie gross ist sie in den ersten \(2\;\text{s}\) und in den letzten \(2\;\text{s}\)?',
     r'<p>0 bis 2 s: \(v\) steigt, \(F_\text{ges} \gt 0\). 2 bis 6 s: \(v\) konstant, \(F_\text{ges} = 0\). 6 bis 8 s: \(v\) sinkt, \(F_\text{ges} \lt 0\).</p><p>Erste Phase: \(a = \dfrac{\Delta v}{\Delta t} = \dfrac{4\;\text{m/s}}{2\;\text{s}} = 2\;\text{m/s}^2\), \(F_\text{ges} = m \cdot a = 50\;\text{kg} \cdot 2\;\text{m/s}^2 = 100\;\text{N}\). Letzte Phase: \(a = \dfrac{-4\;\text{m/s}}{2\;\text{s}} = -2\;\text{m/s}^2\), \(F_\text{ges} = m \cdot a\) \(= 50\;\text{kg} \cdot (-2\;\text{m/s}^2) = -100\;\text{N}\) (gegen die Fahrtrichtung).</p>',
     '\n            <div class="mini-reihe">' + vt_bild([(0, 0), (2, 4), (6, 4), (8, 0)], 8, 5, 1, 1, 'v-t-Diagramm: in 2 s von 0 auf 4 m/s, bis 6 s konstant, bis 8 s zurück auf 0') + '</div>'),
    ('2c', 3, r'Eine Raumsonde fliegt mit abgeschaltetem Triebwerk weit weg von allen Planeten. Welche Kraft hält sie in Bewegung? Begründe.',
     r'<p>Keine. Auf die Sonde wirkt (fast) keine Kraft, also ist ihre Beschleunigung null: Sie behält Tempo und Richtung bei — das Trägheitsgesetz. Eine Kraft wäre nur nötig, um die Bewegung zu ändern.</p>', ''),
    ('2d', 3, r'Eine Fallschirmspringerin (\(70\;\text{kg}\) mit Ausrüstung) sinkt mit konstant \(5\;\text{m/s}\). Wie gross ist der Luftwiderstand? Kurz nach dem Öffnen des Schirms war der Widerstand \(1500\;\text{N}\): Wie gross war die Beschleunigung, und wohin zeigte sie?',
     r'<p>Konstantes Tempo heisst \(F_\text{ges} = 0\): \(F_W = F_G = m \cdot g\) \(= 70\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 687\;\text{N}\).</p><p>Beim Öffnen wirken die Kräfte senkrecht; die positive Richtung darf man frei wählen, wenn man sie nennt — hier nach oben: \(F_\text{ges} = F_W - F_G\) \(= 1500\;\text{N} - 687\;\text{N} = 813\;\text{N}\), \(a = \dfrac{F_\text{ges}}{m} = \dfrac{813\;\text{N}}{70\;\text{kg}} \approx 11.6\;\text{m/s}^2\) nach oben — sie wird stark abgebremst, fällt aber weiter nach unten.</p>', ''),
])
k2 = kapitel(2, 'gesamtkraft-traegheit', 'Gesamtkraft und Trägheit', 'K1 · K2', 40,
    r'Du bestimmst die Gesamtkraft aus Kräften auf einer Geraden, erkennst mit dem Trägheitsgesetz, wann sich die Geschwindigkeit nicht ändert, und rechnest mit \(F_\text{ges} = m \cdot a\).',
    ('p4-2-lp-gesamtkraft', 'Kraft sehen: Antrieb gegen Widerstand', None),
    sim2, ('p4-2-lp-kontrolle-gesamtkraft', 'Kontrollfragen zu Gesamtkraft und Trägheit', None),
    fest2, [uebung('gesamt', 'Gesamtkraft und Beschleunigung'), uebung('konstant', 'Antriebskraft'), uebung('bremsen', 'Ausrollen bis zum Stillstand')],
    auf2, f'<a href="{TS}#traegheit">Themenseite 4.2, Das Trägheitsgesetz</a> · <a href="{TS}#grundgesetz">Das Grundgesetz</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Aufzugkabine im Schacht mit Person auf einer Waage; Gewichtskraft, Normalkraft und Beschleunigung als Pfeile, die Waage zeigt live an', '0 0 300 262',
    '        ' + knoepfe('ph', 'Fahrt', [('ruhe', 'steht'), ('auf', 'fährt nach oben an'), ('konst', 'fährt gleichmässig'), ('brems', 'bremst (nach oben)'), ('fall', 'Seil reisst')], 'auf')
    + '\n        <div class="reglerfeld">\n          '
    + regler('s3', 'm', '<i>m</i> Person', 40, 100, 1, 60, 'kg', 0) + '\n          '
    + regler('s3', 'a', '|<i>a</i>| Betrag', 0.5, 5, 0.1, 2, 'm/s²', 1) + '\n        </div>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Gewichtskraft und Normalkraft</div>
          <p>Die Erde zieht jede Masse mit der <b>Gewichtskraft</b> \(F_G = m \cdot g\) an, \(g = 9.81\;\text{m/s}^2\). Fällt ein Körper frei, ist sie die einzige Kraft: \(a = \dfrac{F_G}{m} = g\) — für alle Körper gleich, unabhängig von der Masse (ohne Luftwiderstand).</p>
          <p>Eine Unterlage drückt mit der <b>Normalkraft</b> \(F_N\) senkrecht zurück. Eine Personenwaage misst \(F_N\). Im Aufzug gilt mit «nach oben positiv»:</p>
          <p>\[ F_N - F_G = m \cdot a \qquad F_N = m \cdot (g + a) \]</p>
          <p>Beschleunigung nach oben: Die Waage zeigt mehr. Nach unten: weniger. Im freien Fall: null.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Die Waage misst die Masse.» Sie misst die Kraft, mit der sie drücken muss, und rechnet in kg um. Darum zeigt sie im anfahrenden Aufzug mehr, obwohl die Masse gleich bleibt.</p>
          <p>Richtung verwechselt: Ein Aufzug, der die <em>Abwärts</em>fahrt bremst, beschleunigt nach <em>oben</em> — die Waage zeigt mehr.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 3, r'Ein Kran hebt eine Last von \(500\;\text{kg}\) und beschleunigt sie dabei mit \(0.8\;\text{m/s}^2\) nach oben. Wie gross ist die Seilkraft? Wie gross wäre sie, wenn die Last mit konstantem Tempo gehoben würde?',
     r'<p>Ansatz (nach oben positiv): \(F_S - F_G = m \cdot a\), also \(F_S = m \cdot (g + a)\) \(= 500\;\text{kg} \cdot (9.81\;\text{m/s}^2 + 0.8\;\text{m/s}^2)\) \(\approx 5305\;\text{N}\).</p><p>Konstantes Tempo: \(a = 0\), \(F_S = F_G = 500\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 4905\;\text{N}\).</p>', ''),
    ('3b', 3, r'Das Diagramm zeigt eine Aufzugsfahrt nach oben (nach oben positiv). Eine Person (\(50\;\text{kg}\)) steht auf einer Waage. Welche Normalkraft misst die Waage in den drei Phasen?',
     r'<p>0 bis 2 s: \(a = \dfrac{\Delta v}{\Delta t} = \dfrac{3\;\text{m/s}}{2\;\text{s}} = 1.5\;\text{m/s}^2\), \(F_N = m \cdot (g + a)\) \(= 50\;\text{kg} \cdot (9.81 + 1.5)\;\text{m/s}^2\) \(\approx 566\;\text{N}\).</p><p>2 bis 6 s: \(a = 0\), \(F_N = m \cdot g = 50\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 491\;\text{N}\).</p><p>6 bis 9 s: \(a = \dfrac{\Delta v}{\Delta t} = \dfrac{-3\;\text{m/s}}{3\;\text{s}} = -1\;\text{m/s}^2\), \(F_N = m \cdot (g + a)\) \(= 50\;\text{kg} \cdot (9.81 - 1)\;\text{m/s}^2\) \(\approx 441\;\text{N}\).</p>',
     '\n            <div class="mini-reihe">' + vt_bild([(0, 0), (2, 3), (6, 3), (9, 0)], 9, 4, 1, 1, 'v-t-Diagramm einer Aufzugsfahrt: in 2 s auf 3 m/s, bis 6 s konstant, bis 9 s zurück auf 0') + '</div>'),
    ('3c', 2, r'Auf dem Mond fallen ein Hammer und eine Feder gleich schnell. Warum, obwohl die Gewichtskraft auf den Hammer viel grösser ist?',
     r'<p>Die grössere Gewichtskraft muss auch die grössere Masse beschleunigen. In \(a = \dfrac{F_G}{m} = \dfrac{m \cdot g}{m} = g\) kürzt sich die Masse: Beide fallen mit derselben Beschleunigung. Auf der Erde bremst der Luftwiderstand die Feder; auf dem Mond gibt es keine Luft.</p>', ''),
    ('3d', 3, r'Ein Astronaut (\(90\;\text{kg}\) mit Anzug) steht in einer Rakete, die mit \(15\;\text{m/s}^2\) senkrecht startet. Mit welcher Kraft drückt der Boden auf ihn? Das Wievielfache seiner Gewichtskraft ist das?',
     r'<p>\(F_N = m \cdot (g + a)\) \(= 90\;\text{kg} \cdot (9.81\;\text{m/s}^2 + 15\;\text{m/s}^2)\) \(\approx 2233\;\text{N}\).</p><p>\(F_G = 90\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 883\;\text{N}\), also \(\dfrac{2233\;\text{N}}{883\;\text{N}} \approx 2.5\) — er fühlt sich rund zweieinhalbmal so schwer.</p>', ''),
])
k3 = kapitel(3, 'gewicht-und-aufzug', 'Gewichtskraft, Fall und Aufzug', 'K1 · K2', 40,
    r'Du erklärst mit \(F = m \cdot a\), warum alle Körper gleich schnell fallen, und berechnest die Normalkraft in einem beschleunigten Aufzug.',
    ('p4-2-lp-aufzug', 'Kraft sehen: was die Waage im Aufzug zeigt', None),
    sim3, ('p4-2-lp-kontrolle-aufzug', 'Kontrollfragen zu Gewichtskraft und Aufzug', None),
    fest3, [uebung('gewicht', 'Gewichtskraft'), uebung('aufzug', 'Waage im Aufzug'), uebung('anzeige', 'Beschleunigung aus der Anzeige')],
    auf3, f'<a href="{TS}#definition">Themenseite 4.2, Gewichtskraft und Normalkraft</a> · <a href="{TS}#aufgaben">Aufgabe A6, Aufzug</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Wagen auf einem Tisch, über eine Rolle von einem hängenden Körper gezogen; darunter das v-t-Diagramm der Fahrt', '-4 -4 308 410',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 'm1', '<i>m</i>₁ Wagen', 0.5, 5, 0.5, 3, 'kg', 1) + '\n          '
    + regler('s4', 'm2', '<i>m</i>₂ hängend', 0.1, 3, 0.1, 1, 'kg', 1) + '\n        </div>\n'
    + '        <p class="sim-notiz">Reibungsfrei; Faden und Rolle masselos.</p>')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zwei Körper, ein Faden</div>
          <p>Hängen Körper an einem gespannten Faden, bewegen sie sich gemeinsam. Für das <b>ganze System</b> gilt: Die antreibende Kraft beschleunigt die Gesamtmasse. Beim Wagen auf dem Tisch treibt die Gewichtskraft des hängenden Körpers:</p>
          <p>\[ m_2 \cdot g = (m_1 + m_2) \cdot a \qquad a = \frac{m_2 \cdot g}{m_1 + m_2} \]</p>
          <p>Die <b>Fadenkraft</b> findet man an einem Körper allein: Den Wagen beschleunigt nur der Faden, \(F_S = m_1 \cdot a\). Gilt für reibungsfreie Bewegung mit masselosem Faden und masseloser Rolle.</p>
          <p>Ebenso beim Auto mit Anhänger: Die Antriebskraft beschleunigt beide zusammen, den Anhänger allein zieht die <b>Kupplungskraft</b> \(F_K = m_\text{Anhänger} \cdot a\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Fadenkraft am falschen Körper ausgerechnet: \(F_S = m_1 \cdot a\) gilt am Wagen, weil ihn nur der Faden zieht. Am hängenden Körper wirkt zusätzlich seine Gewichtskraft.</p>
          <p>Nur durch \(m_1\) geteilt: Die Gewichtskraft beschleunigt beide Körper, also durch \(m_1 + m_2\) teilen.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 4, r'Ein Auto (\(1200\;\text{kg}\)) zieht einen Anhänger (\(600\;\text{kg}\)) mit einer Antriebskraft von \(2700\;\text{N}\); Widerstände vernachlässigt. Wie gross ist die Beschleunigung? Welche Kraft überträgt die Kupplung?',
     r'<p>System: \(a = \dfrac{F}{m_1 + m_2} = \dfrac{2700\;\text{N}}{1800\;\text{kg}} = 1.5\;\text{m/s}^2\).</p><p>Anhänger allein: \(F_K = m_2 \cdot a = 600\;\text{kg} \cdot 1.5\;\text{m/s}^2 = 900\;\text{N}\).</p><p class="komm">Probe am Auto: \(2700\;\text{N} - 900\;\text{N} = 1800\;\text{N} = 1200\;\text{kg} \cdot 1.5\;\text{m/s}^2\).</p>', ''),
    ('4b', 3, r'Übertrag auf einen neuen Aufbau: Über eine reibungsfreie Rolle hängen an einem Faden zwei Körper, A mit \(0.6\;\text{kg}\) und B mit \(0.4\;\text{kg}\). Mit welcher Beschleunigung bewegen sie sich? Wie gross ist die Fadenkraft? (Tipp: wie beim Wagen — was treibt an, was wird beschleunigt?)',
     r'<p>Angetrieben wird durch den Unterschied der Gewichtskräfte, beschleunigt werden beide: \(a = \dfrac{(m_A - m_B) \cdot g}{m_A + m_B}\) \(= \dfrac{0.2\;\text{kg} \cdot 9.81\;\text{m/s}^2}{1.0\;\text{kg}}\) \(\approx 1.96\;\text{m/s}^2\).</p><p>Am leichteren Körper B (steigt, nach oben positiv): \(F_S - m_B \cdot g = m_B \cdot a\), also \(F_S = m_B \cdot (g + a)\) \(F_S = 0.4\;\text{kg} \cdot (9.81 + 1.962)\;\text{m/s}^2\) \(\approx 4.71\;\text{N}\).</p>', ''),
    ('4c', 2, r'Zeichne für den Wagen auf dem Tisch und für den hängenden Körper je alle Kräfte als Pfeile (Freikörperbild). Welche Pfeile sind gleich lang?',
     r'<p>Wagen: Gewichtskraft nach unten, Normalkraft des Tisches nach oben (gleich lang, sie heben sich auf), Fadenkraft \(F_S\) zur Rolle hin. Hängender Körper: Gewichtskraft \(m_2 \cdot g\) nach unten, Fadenkraft \(F_S\) nach oben, kürzer als die Gewichtskraft.</p><p>Gleich lang sind die beiden Fadenkräfte (ein Faden, masselose Rolle) und am Wagen Gewichts- und Normalkraft.</p>', ''),
    ('4d', 3, r'Warum ist die Fadenkraft kleiner als die Gewichtskraft des hängenden Körpers, solange alles beschleunigt? Was misst man, wenn man den Wagen festhält?',
     r'<p>Am hängenden Körper wirken \(m_2 \cdot g\) nach unten und \(F_S\) nach oben. Er beschleunigt nach unten, also muss die Gesamtkraft nach unten zeigen: \(F_S \lt m_2 \cdot g\).</p><p>Hält man den Wagen fest, ruht alles: \(a = 0\), die Gesamtkraft am hängenden Körper ist null, also \(F_S = m_2 \cdot g\).</p>', ''),
])
k4 = kapitel(4, 'zwei-koerper', 'Zwei Körper, ein Faden', 'K2', 40,
    r'Du wendest \(F = m \cdot a\) auf zusammenhängende Körper an: Die antreibende Kraft beschleunigt die Gesamtmasse, die Faden- oder Kupplungskraft bestimmst du an einem Körper allein.',
    ('p4-2-lp-faden', 'Kraft sehen: wer zieht wen am Faden', None),
    sim4, ('p4-2-lp-kontrolle-faden', 'Kontrollfragen zu Faden und Kupplung', None),
    fest4, [uebung('faden', 'Wagen und hängender Körper'), uebung('zug', 'Auto mit Anhänger'), uebung('faden_m2', 'Rückwärts: die hängende Masse')],
    auf4, f'<a href="{TS}#aufgaben">Themenseite 4.2, Aufgabe A5 (Fallmaschine)</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur_anim('sim5', 'Kugel an einer Schnur auf einer Kreisbahn von oben; Geschwindigkeit tangential, Zentripetalkraft zur Mitte; die Schnur lässt sich kappen', '0 0 300 280',
    '        <div class="reglerfeld">\n          '
    + regler('s5', 'm', '<i>m</i> Masse', 0.5, 3, 0.5, 2, 'kg', 1) + '\n          '
    + regler('s5', 'v', '<i>v</i> Tempo', 1, 6, 0.5, 3, 'm/s', 1) + '\n          '
    + regler('s5', 'r', '<i>r</i> Radius', 0.5, 2, 0.1, 1, 'm', 1) + '\n        </div>\n'
    + '        <p class="sim-notiz">Von oben gesehen, Drehsinn gegen den Uhrzeigersinn. Pfeillängen proportional zu \\(v\\) und \\(F_z\\); ein Kraftpfeil, der nicht in den Kreis passt, wird gekürzt.</p>')
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Kraft zur Mitte</div>
          <p>Auf der Kreisbahn ändert sich die Richtung der Geschwindigkeit ständig: Der Körper hat die Zentripetalbeschleunigung \(a_z = \dfrac{v^2}{r}\) zur Mitte (4.1). Nach dem Grundgesetz braucht es dafür eine Gesamtkraft zur Mitte, die <b>Zentripetalkraft</b>:</p>
          <p>\[ F_z = m \cdot a_z = \frac{m \cdot v^2}{r} = m \cdot \omega^2 \cdot r \]</p>
          <p>Mit der Umlaufzeit \(T\): Winkelgeschwindigkeit \(\omega = \dfrac{2\pi}{T}\) und \(v = \omega \cdot r\) (<a href="leitprogramm-kinematik.html#k5">Leitprogramm Kinematik, Kapitel 5</a>).</p>
          <p>Sie ist keine neue Kraftart, sondern eine Rolle, die eine vorhandene Kraft übernimmt: die Schnur beim Hammerwurf, die Haftreibung zwischen Reifen und Strasse in der Kurve, die Gravitation beim Mond. Fehlt sie, fliegt der Körper tangential geradeaus weiter — das Trägheitsgesetz.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«In der Kurve drückt eine Kraft nach aussen.» Von der Strasse aus gesehen wirkt nur eine Kraft nach innen; der Körper will geradeaus weiter, und Türe oder Gurt zwingen ihn auf die Kurve. Die «Zentrifugalkraft» gibt es nur im mitdrehenden Bezugssystem, als Scheinkraft.</p>
          <p>Das Quadrat vergessen: Doppeltes Tempo braucht die <em>vierfache</em> Kraft.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Ein Velofahrer (\(85\;\text{kg}\) mit Velo) fährt mit \(18\;\text{km/h}\) durch eine Kurve mit \(r = 12\;\text{m}\). Wie gross ist die Zentripetalkraft? Welche Kraft übernimmt diese Rolle?',
     r'<p>\(v = \dfrac{18}{3.6}\;\text{m/s} = 5\;\text{m/s}\), \(F_z = \dfrac{m \cdot v^2}{r} = \dfrac{85\;\text{kg} \cdot (5\;\text{m/s})^2}{12\;\text{m}} \approx 177\;\text{N}\).</p><p>Die Haftreibung zwischen Reifen und Strasse, gerichtet zur Kurvenmitte.</p>', ''),
    ('5b', 3, r'Die Raumstation ISS (\(420\;\text{t}\)) kreist auf \(r = 6770\;\text{km}\) um den Erdmittelpunkt, mit \(7.67\;\text{km/s}\). Wie gross ist die Kraft, die sie auf der Bahn hält? Welche Kraft ist das?',
     r'<p>Umrechnen: \(420\;\text{t} = 4.2 \cdot 10^{5}\;\text{kg}\), \(7.67\;\text{km/s} = 7670\;\text{m/s}\), \(6770\;\text{km} = 6.77 \cdot 10^{6}\;\text{m}\).</p><p>\(a_z = \dfrac{v^2}{r} = \dfrac{(7670\;\text{m/s})^2}{6.77 \cdot 10^{6}\;\text{m}} \approx 8.69\;\text{m/s}^2\).</p><p>\(F_z = m \cdot a_z\) \(= 4.2 \cdot 10^{5}\;\text{kg} \cdot 8.69\;\text{m/s}^2\) \(\approx 3.65 \cdot 10^{6}\;\text{N}\) — die Gravitation der Erde. Die ISS fällt dauernd um die Erde herum.</p>', ''),
    ('5c', 3, r'Das Diagramm zeigt die Zentripetalkraft zweier Körper A und B auf derselben Kreisbahn (\(r = 2\;\text{m}\)), aufgetragen über \(v^2\). Welche Masse hat jeder? (Punkte auf Gitterpunkten)',
     r'<p>\(F_z = \dfrac{m}{r} \cdot v^2\): Die Steigung ist \(\dfrac{m}{r}\).</p><p>A: \(\dfrac{16\;\text{N}}{16\;\text{m}^2/\text{s}^2} = 1\;\text{kg/m}\), also \(m = 1\;\text{kg/m} \cdot 2\;\text{m} = 2\;\text{kg}\). B: \(\dfrac{8\;\text{N}}{16\;\text{m}^2/\text{s}^2} = 0.5\;\text{kg/m}\), also \(m = 1\;\text{kg}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="1;0.5" data-namen="A;B" data-farbe="kurve-f" data-fenster="20,20" data-teilung="2,2" data-punkte="16,16;16,8" data-xname="v² [m²/s²]" data-yname="F [N]" aria-label="Zentripetalkraft über v-Quadrat, zwei Ursprungsgeraden A und B"></svg></div>'),
    ('5d', 3, r'Im Auto wird man in der Kurve gegen die Türe gedrückt. Gibt es eine Kraft, die nach aussen zieht? Erkläre mit dem Trägheitsgesetz.',
     r'<p>Nein. Der Körper will nach dem Trägheitsgesetz geradeaus weiter. Das Auto biegt unter ihm weg, bis die Türe ihn erreicht. Die Türe drückt ihn dann nach <em>innen</em> auf die Kreisbahn — diese Kraft spürt man. Eine Kraft nach aussen braucht nur, wer sich im mitdrehenden Auto beschreibt (Scheinkraft).</p>', ''),
])
k5 = kapitel(5, 'kreisbewegung', 'Die Kraft zur Mitte', 'K2', 40,
    r'Du berechnest die Zentripetalkraft \(F_z = \dfrac{m \cdot v^2}{r}\), nennst, welche Kraft diese Rolle übernimmt, und erklärst, warum ein Körper ohne sie tangential weiterfliegt.',
    ('p4-2-lp-kurve', 'Kraft sehen: die Kraft, die im Kreis hält', None),
    sim5, ('p4-2-lp-kontrolle-kurve', 'Kontrollfragen zur Zentripetalkraft', None),
    fest5, [uebung('zentri', 'Zentripetalkraft'), uebung('vmax', 'Höchsttempo an der Schnur'), uebung('omega', 'Mit der Umlaufzeit')],
    auf5, f'<a href="{TS}#kreisbewegung">Themenseite 4.2, Kreisbewegung — die Kraft zur Mitte</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/dynamik/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">4.2 · K1 · K2</span><span class="zeit">≈ 25 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a>, <a href="#k2">2</a>, <a href="#k3">3</a> → K1 · G2, G3 → <a href="#k1">1</a>, <a href="#k2">2</a> → K1, K2 · G4 → <a href="#k3">3</a> → K2 · G5 → <a href="#k4">4</a> → K2 · G6 → <a href="#k5">5</a> → K2</p>
        </div>
      </div>
    </section>'''

weiter = f'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Das Wechselwirkungsgesetz (actio = reactio) und die Federkraft (Hooke) → <a href="{TS}#wechselwirkung">Themenseite 4.2, Wechselwirkungsgesetz</a> · <a href="{TS}#federkraft">Federkraft</a></li>
        <li>Haft- und Gleitreibung mit Reibungszahl, Kräfte an der schiefen Ebene → <a href="{TS}#reibung">Themenseite 4.2, Reibung</a> · <a href="{TS}#schiefe-ebene">Schiefe Ebene</a>; im RLP bei 4.4 Statik</li>
        <li>Die Bewegung selbst beschreiben (Ort, Geschwindigkeit, Diagramme) → <a href="leitprogramm-kinematik.html">Leitprogramm Kinematik</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Dynamik, Version 1.0 (04.10.2026), unverlinkt in Erprobung bis nach /lp-pruefung.
     Drittes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip → ② laufende Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF (downloads/leitprogramme/dynamik/*.tex). Quelle: scripts/lp/dynamik/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 4.2 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 den Zusammenhang zwischen Kraft, Masse und Beschleunigung beschreiben
       K2 das zweite Newton’sche Gesetz in einfachen Fällen (gleichmässig beschleunigte geradlinige
          Bewegung und gleichförmige Kreisbewegung) anwenden

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1, 2, 3 · Aufg. 1a–1d 2b 2c 3c · G1 G2 G3
       K2 → Kap. 2, 3, 4, 5 · Aufg. 2a 2d 3a 3b 3d 4a–4d 5a–5d · G2 G3 G4 G5 G6
     Bewusst weggelassen: Der RLP nennt für 4.2 nur diese zwei Kompetenzen. Wechselwirkungsgesetz
     und Federkraft stehen in keiner Kompetenz, Reibungszahl und schiefe Ebene unter 4.4 Statik —
     sie bleiben auf der Themenseite (Verweise unter «Nicht in diesem Leitprogramm»). Reibung kommt
     hier nur als gegebene Widerstandskraft vor.
     Widersprüche der Themenseite, hier nicht übernommen: Gleit- und Haftreibung heissen dort zum Teil
     F_G und F_H (vergeben für Gewichtskraft und Hangabtrieb) — hier F_W für jeden Widerstand; in
     Animation 6 ist v blau statt grün — hier grün wie sonst überall.
     Zeiten: K0 10 · K1 40 · K2 40 · K3 40 · K4 40 · K5 40 · Gesamttest 25 = 235 min ≈ 5.2 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Dynamik</h1>
      <p class="unter">Kraft, Masse und Beschleunigung — vom anfahrenden Wagen über den Aufzug bis zur Kugel an der Schnur, mit laufenden Simulationen. Fünf Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 4 · Teilgebiet 4.2</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Kraft, Masse, Beschleunigung</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Gesamtkraft und Trägheit</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Gewichtskraft, Fall und Aufzug</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Zwei Körper, ein Faden</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Die Kraft zur Mitte</span></a></li></ol>
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
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 4, Teilgebiet 4.2 Dynamik</p>
        <ul>
          <li><b>K1</b> den Zusammenhang zwischen Kraft, Masse und Beschleunigung beschreiben</li>
          <li><b>K2</b> das zweite Newton’sche Gesetz in einfachen Fällen (gleichmässig beschleunigte geradlinige Bewegung und gleichförmige Kreisbewegung) anwenden</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">4.2 Dynamik</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Dynamik · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Grundgesetz') + k1 + band(2, 'Gesamtkraft') + k2 + band(3, 'Aufzug') + k3
        + band(4, 'Faden') + k4 + band(5, 'Kreisbahn') + k5 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
