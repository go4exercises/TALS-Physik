"""Baut leitprogramme/leitprogramm-energie.html aus einer Kapitelbeschreibung (seit 04.10.2026).

  python3 scripts/lp/energie/seite.py

Viertes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4), als Kopie von
scripts/lp/dynamik/ entstanden: Kopf, CSS, Grundskript und Bausteine von dort, neu sind
Kapitel, die laufenden Simulationen und die Übungstypen (seite.js). Nur den SEO-Block
übernimmt das Skript aus der bestehenden Seite. Wiederholbar. Danach build-seo.py, Pre-Flight.
Siehe README.md.
"""
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-energie.html'
TS = '../themen/p4-3-energie.html'

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
<title>Leitprogramm Energie</title>
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
/* Diagramme und Szenen: Farben wie auf Themenseite 4.3 (STYLEGUIDE §5.2) — Lageenergie
   Bernstein, Bewegungsenergie und v Grün, Wärme und Reibung Rot, Kräfte und zugeführte Energie
   Blau, Kraftanteil in Wegrichtung Violett; Ziele Lila gestrichelt, voriger Lauf grau gestrichelt */
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
.kurve-mini.kurve-v{stroke:var(--gruen);stroke-width:2.2} .kurve-mini.kurve-f{stroke:var(--rot);stroke-width:2.2} .kurve-mini.kurve-epot{stroke:var(--bernstein);stroke-width:2.2}
svg.mini.breit{width:260px}
.mini-name{fill:var(--tinte);font-family:var(--sans);font-size:12px;font-weight:700}
.p-mini{fill:var(--tinte)}
.kiste{fill:var(--bernstein-hell);stroke:var(--bernstein);stroke-width:1.6}
.hilfslinie{stroke:var(--lila);stroke-width:1;stroke-dasharray:3 3;opacity:.7}
.flaeche-w{fill:var(--lila-hell);opacity:.85}
.zielflaeche{fill:none;stroke:var(--lila);stroke-width:2.4;stroke-dasharray:7 5}
.vorher-flaeche{fill:none;stroke:var(--tinte-2);stroke-width:1.6;stroke-dasharray:5 4;opacity:.7}
.kurve-fs{fill:none;stroke:var(--lila);stroke-width:2.6}
.flaeche-name{fill:var(--lila);font-family:var(--sans);font-size:14px;font-weight:700}
.zielstrich{stroke:var(--lila);stroke-width:2.4;stroke-dasharray:5 4}
.bremsspur{stroke:var(--tinte);stroke-width:2.5;opacity:.55}
.auto{fill:var(--papier-2);stroke:var(--tinte);stroke-width:1.6;stroke-linejoin:round}
.kurve-ekin{fill:none;stroke:var(--gruen);stroke-width:2.6}
.schiene{fill:none;stroke:var(--tinte);stroke-width:2.4;stroke-linejoin:round}
.saeule{stroke:var(--tinte);stroke-width:.8}
.saeule.e-pot{fill:var(--bernstein)} .saeule.e-kin{fill:var(--gruen)} .saeule.e-ges{fill:var(--tinte-2)}
.saeule.e-motor{fill:var(--blau)} .saeule.e-waerme{fill:var(--rot)}
.saeule-text{fill:var(--weiss);font-family:var(--sans);font-size:9.5px;font-weight:700}
.bt-wert{fill:var(--tinte);font-family:var(--sans);font-size:10.5px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.rampe{fill:var(--papier-2);stroke:none}
.masslinie{stroke:var(--tinte-2);stroke-width:1;stroke-dasharray:3 3}
.mast{fill:var(--tinte-2)}
.motor{fill:var(--blau-hell);stroke:var(--blau);stroke-width:1.4}
.sonne{fill:var(--orange-hell);stroke:var(--orange);stroke-width:2}
.erde{fill:var(--gruen-hell);stroke:var(--gruen);stroke-width:1.6}
.atmosphaere{fill:var(--tinte-2);stroke:var(--tinte-2);stroke-width:.8;stroke-dasharray:3 3}
.erde-text{fill:var(--tinte);font-family:var(--sans);font-size:13px;font-weight:700}
.strahl{fill:none;opacity:.75}
.strahl.ein{stroke:var(--orange)} .strahl-kopf.ein{fill:var(--orange)}
.strahl.zurueck{stroke:var(--tinte-2);opacity:.45} .strahl-kopf.zurueck{fill:var(--tinte-2);opacity:.45}
.strahl.aus{stroke:var(--rot)} .strahl-kopf.aus{fill:var(--rot)}
.gleichgewicht{fill:none;stroke:var(--tinte-2);stroke-width:1.4;stroke-dasharray:5 4}
.gleichgewicht-text{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.kurve-t{fill:none;stroke:var(--rot);stroke-width:2.6}
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
  var KEY = 'leitprogramm-energie-v1';

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
  <p>Leitprogramm · Energie</p>
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">4.3 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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


def linien_bild(punkte, x0, x1, y0, y1, xt, yt, label, xname, yname, cls='kurve-v', waagrecht=None):
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
    t.append('<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in punkte) + f'" class="kurve-mini {cls}"/>')
    t.append(f'<text x="{X(x1) + 8:.1f}" y="{oy - 6}" text-anchor="end" class="achsname">{xname}</text><text x="{ox + 6}" y="{Y(y1) - 2:.1f}" class="achsname">{yname}</text></svg>')
    return ''.join(t)


# ------------------------------------------------------------------ Kapitel 0: Vorwissen
P01 = '../themen/p0-1-vorwissen-mathematik.html'
P02 = '../themen/p0-2-vorwissen-physik.html'
k0 = '''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2 · 4.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Kraft und Beschleunigung aus 4.2, Gewichtskraft, Gleichungen umstellen, Einheiten umrechnen. Wenn das wackelt: <a href="leitprogramm-dynamik.html">Leitprogramm Dynamik</a> und <a href="leitprogramm-rechnen.html">Leitprogramm Rechnen</a>.</p>
      ''' + clipkarte('p0-3-masse-gewicht', 'Masse und Gewicht: was die Waage wirklich zeigt', '0:53') + r'''
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Ein Auto (\(1200\;\text{kg}\)) wird in \(8\;\text{s}\) gleichmässig aus dem Stand auf \(20\;\text{m/s}\) beschleunigt. Wie gross sind Beschleunigung und Gesamtkraft?',
     r'<p>\(a = \dfrac{\Delta v}{\Delta t}\) \(= \dfrac{20\;\text{m/s}}{8\;\text{s}}\) \(= 2.5\;\text{m/s}^2\), \(F = m \cdot a\) \(= 1200\;\text{kg} \cdot 2.5\;\text{m/s}^2\) \(= 3000\;\text{N}\).</p><p class="komm">Falsch? <a href="leitprogramm-dynamik.html#k1">Leitprogramm Dynamik, Kapitel 1</a></p>', ''),
    ('0b', 2, r'Wie gross ist die Gewichtskraft auf einen Koffer von \(25\;\text{kg}\)?',
     r'<p>\(F_G = m \cdot g\) \(= 25\;\text{kg} \cdot 9.81\;\text{m/s}^2\) \(\approx 245\;\text{N}\).</p><p class="komm">Falsch? <a href="leitprogramm-dynamik.html#k3">Leitprogramm Dynamik, Kapitel 3</a></p>', ''),
    ('0c', 3, r'Stelle \(E = \tfrac12 \cdot m \cdot v^2\) nach \(v\) um, \(P = \dfrac{W}{t}\) nach \(t\) und \(W = F \cdot s\) nach \(s\).',
     r'<p>\(v = \sqrt{\dfrac{2 \cdot E}{m}}\), \(t = \dfrac{W}{P}\), \(s = \dfrac{W}{F}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umstellen</a></p>', ''),
    ('0d', 2, r'Rechne um: \(2.5\;\text{kW}\) in Watt und \(3\;\text{h}\) in Sekunden.',
     r'<p>\(2.5\;\text{kW} = 2500\;\text{W}\), \(3\;\text{h} = 3 \cdot 3600\;\text{s}\) \(= 10\,800\;\text{s}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#praefixe">Vorwissen 0.2, Vorsilben</a> · <a href="../werkzeuge/einheitentrainer.html">Einheitentrainer</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = figur_anim('sim1', 'Kiste wird mit einer Kraft unter einem Winkel gezogen; darunter das Kraft-Weg-Diagramm, in dem sich die Fläche als Arbeit füllt', '-4 -4 308 318',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'F', '<i>F</i> Kraft', 0, 400, 10, 100, 'N', 0) + '\n          '
    + regler('s1', 'al', '<i>α</i> Winkel', 0, 80, 5, 20, '°', 0) + '\n          '
    + regler('s1', 's', '<i>s</i> Weg', 1, 8, 0.5, 3, 'm', 1) + '\n        </div>\n'
    + '        <p class="sim-notiz">Die Kiste gleitet gleichmässig; Reibung und Gewichtskraft sind nicht gezeichnet.</p>')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Energie und Arbeit</div>
          <p><b>Energie</b> ist die Fähigkeit, Arbeit zu verrichten. Sie tritt in verschiedenen Formen auf: Lageenergie, Bewegungsenergie, Spannenergie, Wärme (innere Energie), chemische, elektrische, Strahlungs- und Kernenergie. Energie wird umgewandelt, aber nicht erzeugt oder vernichtet. Einheit: das Joule, \(1\;\text{J} = 1\;\text{N} \cdot \text{m}\).</p>
          <p><b>Arbeit</b> verrichtet eine Kraft, die einen Körper längs eines Weges verschiebt. Es zählt nur der Anteil der Kraft in Wegrichtung. Für eine konstante Kraft auf einem geraden Weg gilt:</p>
          <p>\[ W = F \cdot s \cdot \cos\alpha \]</p>
          <p>Im Kraft-Weg-Diagramm ist die Arbeit die Fläche unter der Kraft — so auch, wenn sich die Kraft unterwegs ändert (Rechteck, Dreieck, zusammengesetzt). Steht die Kraft senkrecht zum Weg (\(\alpha = 90^\circ\)), ist die Arbeit null. Wer einen Körper um \(h\) hebt, verrichtet die <b>Hubarbeit</b> \(W = m \cdot g \cdot h\).</p>
          <p>Grosse Energien gibt man oft in <b>Kilowattstunden</b> an: \(1\;\text{kWh} = 1000\;\text{W} \cdot 3600\;\text{s}\) \(= 3.6 \cdot 10^{6}\;\text{J}\) \(= 3.6\;\text{MJ}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Anstrengung ist Arbeit.» Wer eine Tasche hält oder waagrecht trägt, ermüdet, verrichtet aber an der Tasche keine Arbeit: Die Haltekraft zeigt nach oben, der Weg ist null oder waagrecht.</p>
          <p>Den Winkel falsch genommen: \(\alpha\) ist der Winkel zwischen Kraft und Weg. \(100\;\text{N}\) unter \(40^\circ\) über \(10\;\text{m}\) geben \(100\;\text{N} \cdot 10\;\text{m} \cdot \cos 40^\circ \approx 766\;\text{J}\), nicht \(643\;\text{J}\) (mit dem Sinus).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 3, r'Nenne für jedes Beispiel, welche Energieform hineingeht und welche herauskommt: ein Wasserkraftwerk, eine Solarzelle, eine Velofahrerin, die bremst.',
     r'<p>Wasserkraftwerk: Lageenergie des Wassers → Bewegungsenergie → elektrische Energie (dazu etwas Wärme). Solarzelle: Strahlungsenergie → elektrische Energie und Wärme. Bremsende Velofahrerin: Bewegungsenergie → Wärme in Bremsen und Reifen.</p>', ''),
    ('1b', 3, r'Ein Kind zieht einen Schlitten \(50\;\text{m}\) weit; die Schnur zieht mit \(80\;\text{N}\) unter \(30^\circ\) zum Boden. Wie gross ist die Arbeit? Wie viel wäre es, wenn die Schnur waagrecht zöge?',
     r'<p>\(W = F \cdot s \cdot \cos\alpha\) \(= 80\;\text{N} \cdot 50\;\text{m} \cdot \cos 30^\circ\) \(\approx 3464\;\text{J}\).</p><p>Waagrecht: \(W = 80\;\text{N} \cdot 50\;\text{m}\) \(= 4000\;\text{J}\) — mehr, weil die ganze Kraft in Wegrichtung zeigt.</p>', ''),
    ('1c', 3, r'Das Diagramm zeigt den Anteil der Kraft in Wegrichtung, mit dem eine Kiste über den Boden geschoben wird: zuerst konstant, dann lässt die Schiebende gleichmässig nach. Wie viel Arbeit wird insgesamt verrichtet? Wie viele Kilowattstunden sind das?',
     r'<p>Die Arbeit ist die Fläche unter der Kraft, ein Rechteck und ein Dreieck: \(W = 40\;\text{N} \cdot 3\;\text{m} + \tfrac12 \cdot 40\;\text{N} \cdot 3\;\text{m}\) \(= 120\;\text{J} + 60\;\text{J} = 180\;\text{J}\).</p><p>\(1\;\text{kWh} = 3.6 \cdot 10^{6}\;\text{J}\), also \(\dfrac{180\;\text{J}}{3.6 \cdot 10^{6}\;\text{J/kWh}} = 5 \cdot 10^{-5}\;\text{kWh}\) — eine winzige Energie.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 40), (3, 40), (6, 0), (7, 0)], 0, 7, 0, 50, 1, 10, 'Kraft-Weg-Diagramm: 40 N über die ersten 3 m, dann gleichmässig fallend auf 0 N bei 6 m', 's [m]', 'Fₛ [N]', 'kurve-fs') + '</div>'),
    ('1d', 2, r'Ein Satellit kreist mit konstantem Tempo um die Erde. Verrichtet die Gravitation an ihm Arbeit? Begründe.',
     r'<p>Nein. Die Gravitation zeigt zur Erdmitte, also senkrecht zur Bewegung auf der Kreisbahn: \(\cos 90^\circ = 0\). Darum ändert sich seine Bewegungsenergie nicht — er bleibt gleich schnell.</p>', ''),
])
k1 = kapitel(1, 'energie-arbeit', 'Energie und Arbeit', 'K1 · K2', 40,
    r'Du definierst Energie, zählst die wichtigsten Energieformen auf und berechnest die Arbeit \(W = F \cdot s \cdot \cos\alpha\), auch als Fläche im Kraft-Weg-Diagramm.',
    ('p4-3-lp-arbeit', 'Energie sehen: Arbeit ist Kraft mal Weg'),
    sim1, ('p4-3-lp-kontrolle-arbeit', 'Kontrollfragen zu Energie und Arbeit'),
    fest1, [uebung('arbeit', 'Arbeit mit Winkel'), uebung('hub', 'Hubarbeit'), uebung('kwh', 'Joule und Kilowattstunden umrechnen')],
    auf1, f'<a href="{TS}#definition">Themenseite 4.3, Grundbegriffe</a> · <a href="{TS}#arbeit">Arbeit</a>')

# ------------------------------------------------------------------ Kapitel 2
sim2 = figur_anim('sim2', 'Auto bremst mit konstanter Kraft bis zum Stillstand; darunter die Bewegungsenergie über der Geschwindigkeit als Parabel, auf der ein Punkt hinuntergleitet', '-4 -4 308 324',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'm', '<i>m</i> Masse', 800, 2000, 100, 1200, 'kg', 0) + '\n          '
    + regler('s2', 'v', '<i>v</i> Tempo', 5, 25, 1, 8, 'm/s', 0) + '\n          '
    + regler('s2', 'F', '<i>F</i><sub>B</sub> Bremskraft', 4000, 8000, 500, 7000, 'N', 0) + '\n        </div>')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Mechanische Energie</div>
          <p><b>Lageenergie</b> (potentielle Energie): Ein Körper, der um \(h\) über ein frei gewähltes Nullniveau gehoben wurde, speichert die Hubarbeit:</p>
          <p>\[ E_\text{pot} = m \cdot g \cdot h \]</p>
          <p><b>Bewegungsenergie</b> (kinetische Energie): Ein Körper mit der Geschwindigkeit \(v\) trägt die Arbeit, die nötig war, um ihn aus der Ruhe zu beschleunigen — und die nötig ist, um ihn wieder anzuhalten:</p>
          <p>\[ E_\text{kin} = \tfrac12 \cdot m \cdot v^2 \]</p>
          <p>Lageenergie wächst linear mit der Höhe, Bewegungsenergie quadratisch mit dem Tempo. Bremst eine konstante Kraft bis zum Stillstand, gilt \(F_B \cdot s = E_\text{kin}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Faktor \(\tfrac12\) oder das Quadrat vergessen: Ein Ball von \(0.4\;\text{kg}\) mit \(15\;\text{m/s}\) hat \(\tfrac12 \cdot 0.4\;\text{kg} \cdot (15\;\text{m/s})^2 = 45\;\text{J}\), nicht \(90\;\text{J}\) und nicht \(3\;\text{J}\).</p>
          <p>Geschwindigkeit in km/h eingesetzt: Joule verlangen m/s. Erst durch \(3.6\) teilen.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 12, [
    ('2a', 3, r'Ein Auto (\(1500\;\text{kg}\)) fährt mit \(72\;\text{km/h}\). Wie gross ist seine Bewegungsenergie? Wie viel ist es bei \(36\;\text{km/h}\)?',
     r'<p>\(v = \dfrac{72}{3.6}\;\text{m/s}\) \(= 20\;\text{m/s}\), \(E_\text{kin} = \tfrac12 \cdot m \cdot v^2\) \(= \tfrac12 \cdot 1500\;\text{kg} \cdot (20\;\text{m/s})^2\) \(= 300\;\text{kJ}\).</p><p>Bei \(36\;\text{km/h} = 10\;\text{m/s}\): \(\tfrac12 \cdot 1500\;\text{kg} \cdot (10\;\text{m/s})^2 = 75\;\text{kJ}\) — ein Viertel, weil das Tempo im Quadrat steht.</p>', ''),
    ('2b', 3, r'Das Diagramm zeigt die Bewegungsenergie zweier Körper A und B über \(v^2\). Welche Masse hat jeder? (Punkte auf Gitterpunkten)',
     r'<p>\(E_\text{kin} = \tfrac12 \cdot m \cdot v^2\): Die Steigung über \(v^2\) ist \(\tfrac{m}{2}\).</p><p>A: \(\dfrac{40\;\text{J}}{16\;\text{m}^2/\text{s}^2} = 2.5\;\text{kg}\), also \(m_A = 5\;\text{kg}\). B: \(\dfrac{20\;\text{J}}{20\;\text{m}^2/\text{s}^2} = 1\;\text{kg}\), also \(m_B = 2\;\text{kg}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="2.5;1" data-namen="A;B" data-farbe="kurve-v" data-fenster="20,50" data-teilung="2,5" data-punkte="16,40;20,20" data-xname="v² [m²/s²]" data-yname="E [J]" aria-label="Bewegungsenergie über v-Quadrat, zwei Ursprungsgeraden A und B"></svg></div>'),
    ('2c', 3, r'Ein Hammer (\(1.5\;\text{kg}\)) liegt auf einem Regal, \(2\;\text{m}\) über dem Boden. Wie gross ist seine Lageenergie bezogen auf den Boden? Wie gross bezogen auf eine Tischplatte in \(0.8\;\text{m}\) Höhe? Warum sind beide Antworten richtig?',
     r'<p>Boden: \(E_\text{pot} = m \cdot g \cdot h\) \(= 1.5\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 2\;\text{m}\) \(\approx 29.4\;\text{J}\). Tisch: \(1.5\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 1.2\;\text{m} \approx 17.7\;\text{J}\).</p><p>Das Nullniveau ist frei wählbar. Physikalisch zählt nur die Differenz: Fällt der Hammer auf den Tisch, werden in beiden Rechnungen \(17.7\;\text{J}\) frei.</p>', ''),
    ('2d', 3, r'Ein Auto hat bei \(30\;\text{km/h}\) einen Bremsweg von \(6\;\text{m}\). Wie lang ist er bei \(50\;\text{km/h}\), gleich stark gebremst? Begründe mit der Energie.',
     r'<p>Die Bremse muss die Bewegungsenergie abbauen: \(F_B \cdot s = \tfrac12 \cdot m \cdot v^2\). Bei gleicher Bremskraft wächst der Bremsweg wie \(v^2\).</p><p>\(s = 6\;\text{m} \cdot \left(\dfrac{50}{30}\right)^2\) \(\approx 16.7\;\text{m}\) — knapp dreimal so lang.</p>', ''),
])
k2 = kapitel(2, 'mechanische-energie', 'Lage- und Bewegungsenergie', 'K3', 40,
    r'Du berechnest Lageenergie \(E_\text{pot} = m \cdot g \cdot h\) und Bewegungsenergie \(E_\text{kin} = \tfrac12 \cdot m \cdot v^2\) und erklärst damit, warum doppeltes Tempo den vierfachen Bremsweg braucht.',
    ('p4-3-lp-bremsen', 'Energie sehen: Lage- und Bewegungsenergie'),
    sim2, ('p4-3-lp-kontrolle-bremsen', 'Kontrollfragen zu Lage- und Bewegungsenergie'),
    fest2, [uebung('ekin', 'Bewegungsenergie'), uebung('vaus', 'Tempo aus der Energie'), uebung('bremsweg', 'Bremsweg aus der Energie')],
    auf2, f'<a href="{TS}#definition">Themenseite 4.3, Lage- und Bewegungsenergie</a> · <a href="{TS}#kinetisch">Kinetische Energie</a>')

# ------------------------------------------------------------------ Kapitel 3
sim3 = figur_anim('sim3', 'Achterbahnwagen ohne Reibung: Start auf der Höhe h₀, Tal, zweiter Hügel h₂; darunter Säulen für Lage-, Bewegungsenergie und ihre Summe', '-4 -4 308 336',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'h0', '<i>h</i>₀ Start', 5, 30, 0.5, 15, 'm', 1) + '\n          '
    + regler('s3', 'h2', '<i>h</i>₂ Hügel 2', 0, 30, 0.1, 8, 'm', 1) + '\n          '
    + regler('s3', 'v0', '<i>v</i>₀ Start', 0, 15, 0.1, 0, 'm/s', 1) + '\n          '
    + regler('s3', 'm', '<i>m</i> Wagen', 100, 600, 50, 300, 'kg', 0) + '\n        </div>\n'
    + '        <p class="sim-notiz">Ohne Reibung und Luftwiderstand; Höhen und Längen im selben Massstab.</p>')
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Erhaltung der mechanischen Energie</div>
          <p>Ohne Reibung und ohne Antrieb bleibt die Summe aus Lage- und Bewegungsenergie gleich. Sie wandelt sich nur um:</p>
          <p>\[ m \cdot g \cdot h_1 + \tfrac12 \cdot m \cdot v_1^2 = m \cdot g \cdot h_2 + \tfrac12 \cdot m \cdot v_2^2 \]</p>
          <p>Die Masse kürzt sich. Aus der Ruhe gilt nach dem Höhenunterschied \(h\): \(v = \sqrt{2 \cdot g \cdot h}\). Die Form der Bahn spielt keine Rolle, nur die Höhen. So rechnet man, ohne die Kräfte unterwegs zu kennen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Geschwindigkeiten statt Energien addiert: Wer mit \(3\;\text{m/s}\) startet und \(5\;\text{m}\) hinunterfährt, ist nicht \(3\;\text{m/s} + \sqrt{2 \cdot g \cdot 5\;\text{m}} \approx 12.9\;\text{m/s}\) schnell, sondern \(\sqrt{(3\;\text{m/s})^2 + 2 \cdot g \cdot 5\;\text{m}} \approx 10.3\;\text{m/s}\).</p>
          <p>Die Wurzel vergessen: \(2 \cdot g \cdot h\) ist \(v^2\), nicht \(v\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 12, [
    ('3a', 3, r'Ein Skater startet aus der Ruhe am Rand einer Halfpipe, \(3.2\;\text{m}\) über dem Boden. Wie schnell ist er unten? Wie hoch kommt er auf der anderen Seite, ohne Reibung?',
     r'<p>\(m \cdot g \cdot h = \tfrac12 \cdot m \cdot v^2\), \(v = \sqrt{2 \cdot g \cdot h}\) \(= \sqrt{2 \cdot 9.81\;\text{m/s}^2 \cdot 3.2\;\text{m}}\) \(\approx 7.92\;\text{m/s}\).</p><p>Wieder \(3.2\;\text{m}\): Dort ist die ganze Bewegungsenergie wieder Lageenergie.</p>', ''),
    ('3b', 3, r'Ein Ball wird mit \(12\;\text{m/s}\) senkrecht hochgeworfen. Wie hoch steigt er? Wie schnell ist er in \(4\;\text{m}\) Höhe?',
     r'<p>\(\tfrac12 \cdot m \cdot v_0^2 = m \cdot g \cdot h\), \(h = \dfrac{v_0^2}{2 \cdot g}\) \(= \dfrac{(12\;\text{m/s})^2}{2 \cdot 9.81\;\text{m/s}^2}\) \(\approx 7.34\;\text{m}\).</p><p>\(v = \sqrt{v_0^2 - 2 \cdot g \cdot h}\) \(= \sqrt{(12\;\text{m/s})^2 - 2 \cdot 9.81\;\text{m/s}^2 \cdot 4\;\text{m}}\) \(\approx 8.09\;\text{m/s}\).</p>', ''),
    ('3c', 3, r'Das Diagramm zeigt die Lageenergie eines Wagens (\(100\;\text{kg}\)) längs einer reibungsfreien Bahn; er startet ganz links aus der Ruhe. Gestrichelt: seine Gesamtenergie. Wie gross ist seine Bewegungsenergie bei \(x = 2\;\text{m}\), und wie schnell ist er dort? Wo ist er am schnellsten?',
     r'<p>Die Summe bleibt \(20\;\text{kJ}\). Bei \(x = 2\;\text{m}\) ist \(E_\text{pot} = 5\;\text{kJ}\), also \(E_\text{kin} = 20\;\text{kJ} - 5\;\text{kJ}\) \(= 15\;\text{kJ}\).</p><p>\(v = \sqrt{\dfrac{2 \cdot E_\text{kin}}{m}}\) \(= \sqrt{\dfrac{2 \cdot 15\,000\;\text{J}}{100\;\text{kg}}}\) \(\approx 17.3\;\text{m/s}\). Am schnellsten ab \(x = 6\;\text{m}\) (von \(6\) bis \(7\;\text{m}\)), wo die Lageenergie null ist.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 20), (2, 5), (4, 12), (6, 0), (7, 0)], 0, 7, 0, 25, 1, 5, 'Lageenergie über dem Ort: 20 kJ am Start, 5 kJ bei 2 m, 12 kJ bei 4 m, 0 ab 6 m; gestrichelt die Gesamtenergie 20 kJ', 'x [m]', 'E [kJ]', 'kurve-epot', 20) + '</div>'),
    ('3d', 3, r'Zwei Kinder (\(25\;\text{kg}\) und \(50\;\text{kg}\)) rutschen reibungsfrei zwei Rutschen mit demselben Höhenunterschied hinunter: das leichtere eine gerade, das schwerere eine gewellte. Wer ist unten schneller? Begründe.',
     r'<p>Beide gleich schnell. In \(m \cdot g \cdot h = \tfrac12 \cdot m \cdot v^2\) kürzt sich die Masse, und es zählt nur der Höhenunterschied, nicht die Form der Bahn — ohne Reibung geht unterwegs keine Energie verloren.</p>', ''),
])
k3 = kapitel(3, 'energieerhaltung', 'Energieerhaltung', 'K3', 40,
    r'Du nutzt die Erhaltung der mechanischen Energie, um Geschwindigkeiten und Höhen zu berechnen, ohne die Kräfte unterwegs zu kennen.',
    ('p4-3-lp-erhaltung', 'Energie sehen: die Summe bleibt'),
    sim3, ('p4-3-lp-kontrolle-erhaltung', 'Kontrollfragen zur Energieerhaltung'),
    fest3, [uebung('fall', 'Tempo nach dem Fall'), uebung('hoehe', 'Steighöhe'), uebung('huegel', 'Über den Hügel')],
    auf3, f'<a href="{TS}#erhaltung">Themenseite 4.3, Energieerhaltung</a>')

# ------------------------------------------------------------------ Kapitel 4
sim4 = figur_anim('sim4', 'Wagen auf einer 40 m langen Rampe mit Reibung und Motor; darunter zwei gleich hohe Säulen: zugeführte Energie und wohin sie gegangen ist', '-4 -4 308 324',
    '        <div class="reglerfeld">\n          '
    + regler('s4', 'm', '<i>m</i> Wagen', 40, 150, 5, 100, 'kg', 0) + '\n          '
    + regler('s4', 'h', '<i>h</i> hinunter', -10, 20, 1, 5, 'm', 0) + '\n          '
    + regler('s4', 'FR', '<i>F</i><sub>R</sub> Reibung', 0, 200, 10, 0, 'N', 0) + '\n          '
    + regler('s4', 'FM', '<i>F</i><sub>M</sub> Motor', 0, 400, 10, 0, 'N', 0) + '\n        </div>\n'
    + '        <p class="sim-notiz">Negatives \\(h\\): Das Ende liegt höher, der Wagen fährt bergauf. Er startet aus der Ruhe.</p>')
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Energieerhaltung mit Reibung und Motor</div>
          <p>Energie geht nie verloren. Was fehlt, ist in eine andere Form übergegangen. Die <b>Reibung</b> wandelt die Arbeit \(F_R \cdot s\) in Wärme um (konstante Reibungskraft längs des Weges \(s\)); ein <b>Motor</b> führt die Arbeit \(W_M\) zu. Die Bilanz:</p>
          <p>\[ E_\text{vorher} + W_M = E_\text{nachher} + F_R \cdot s \]</p>
          <p>mit \(E = m \cdot g \cdot h + \tfrac12 \cdot m \cdot v^2\). Die Wärme ist für die Bewegung verloren — man sagt, sie ist «entwertet» —, aber sie ist noch da. Das ist der <b>Energieerhaltungssatz</b>: In einem abgeschlossenen System bleibt die Summe aller Energien gleich.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Reibungsarbeit addiert statt abgezogen: Die Reibung nimmt der Bewegung Energie weg. Ein Motor, der gegen Reibung hochfährt, muss sie dagegen zusätzlich liefern.</p>
          <p>Bei der Hubarbeit die Streckenlänge statt des Höhenunterschieds genommen: \(m \cdot g \cdot h\) mit der Höhe, \(F_R \cdot s\) mit der Strecke.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 11, [
    ('4a', 3, r'Ein Velofahrer (\(85\;\text{kg}\) mit Velo) rollt ohne zu treten eine Passstrasse hinunter. Er startet mit \(4\;\text{m/s}\), kommt \(60\;\text{m}\) tiefer an und ist dort \(15\;\text{m/s}\) schnell. Wie viel Energie wurde durch Reibung und Luftwiderstand zu Wärme? Welcher Anteil seiner Energie am Anfang ist das?',
     r'<p>Am Anfang: \(E = m \cdot g \cdot h + \tfrac12 \cdot m \cdot v_0^2\) \(= 85\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 60\;\text{m}\) \(+ \tfrac12 \cdot 85\;\text{kg} \cdot (4\;\text{m/s})^2\) \(\approx 50\,031\;\text{J} + 680\;\text{J} \approx 50.7\;\text{kJ}\).</p><p>Unten: \(E_\text{kin} = \tfrac12 \cdot 85\;\text{kg} \cdot (15\;\text{m/s})^2 \approx 9.56\;\text{kJ}\). Wärme: \(50.7\;\text{kJ} - 9.56\;\text{kJ} \approx 41.1\;\text{kJ}\), also \(\dfrac{41.1\;\text{kJ}}{50.7\;\text{kJ}} \approx 81\;\%\) — bei diesem Tempo bremst vor allem die Luft.</p>', ''),
    ('4b', 3, r'Ein Schlitten (\(40\;\text{kg}\)) gleitet auf einer ebenen Strecke aus. Das Diagramm zeigt seine Bewegungsenergie über dem Weg. Wie gross ist die Reibungskraft? Wie schnell war er am Anfang?',
     r'<p>Die Reibung nimmt auf jedem Meter gleich viel Energie weg: \(F_R \cdot s = \Delta E\), also \(F_R = \dfrac{600\;\text{J}}{20\;\text{m}}\) \(= 30\;\text{N}\) — der Betrag der Steigung der Geraden (sie fällt um \(30\;\text{J}\) je Meter).</p><p>\(v = \sqrt{\dfrac{2 \cdot E_\text{kin}}{m}}\) \(= \sqrt{\dfrac{2 \cdot 600\;\text{J}}{40\;\text{kg}}}\) \(\approx 5.48\;\text{m/s}\).</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 600), (20, 0)], 0, 24, 0, 700, 4, 100, 'Bewegungsenergie über dem Weg: Gerade von 600 J bei 0 m auf 0 J bei 20 m', 's [m]', 'E [J]', 'kurve-v') + '</div>'),
    ('4c', 3, r'Ein Kind zieht seinen Schlitten (\(12\;\text{kg}\)) mit konstantem Tempo einen \(30\;\text{m}\) langen Hang hinauf, \(6\;\text{m}\) Höhenunterschied; die Reibung beträgt \(15\;\text{N}\). Wie viel Arbeit verrichtet das Kind am Schlitten, und wohin geht sie? Mit welcher Kraft zieht es längs des Hangs?',
     r'<p>Konstantes Tempo: \(E_\text{kin}\) bleibt. \(W = m \cdot g \cdot h + F_R \cdot s\) \(= 12\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 6\;\text{m} + 15\;\text{N} \cdot 30\;\text{m}\) \(\approx 706\;\text{J} + 450\;\text{J} \approx 1156\;\text{J}\): rund \(706\;\text{J}\) werden Lageenergie, \(450\;\text{J}\) Wärme.</p><p>Die Zugkraft verrichtet diese Arbeit längs der \(30\;\text{m}\): \(F = \dfrac{W}{s} = \dfrac{1156\;\text{J}}{30\;\text{m}} \approx 38.5\;\text{N}\).</p>', ''),
    ('4d', 2, r'Ein Pendel schwingt in der Luft immer weniger weit und bleibt schliesslich hängen. Ist seine Energie verschwunden? Begründe mit dem Energieerhaltungssatz.',
     r'<p>Nein. Luftwiderstand und Reibung an der Aufhängung haben sie bei jeder Schwingung zum Teil in Wärme verwandelt. Luft und Aufhängung sind ein wenig wärmer geworden; die Summe aller Energien ist gleich geblieben.</p>', ''),
])
k4 = kapitel(4, 'reibung-motor', 'Reibung und Motor', 'K4', 40,
    r'Du formulierst den Energieerhaltungssatz mit Reibung und Motor und rechnest mit der Bilanz \(E_\text{vorher} + W_M = E_\text{nachher} + F_R \cdot s\).',
    ('p4-3-lp-reibung', 'Energie sehen: wohin die Energie geht'),
    sim4, ('p4-3-lp-kontrolle-reibung', 'Kontrollfragen zu Reibung und Motor'),
    fest4, [uebung('reibung', 'Mit Reibung hinunter'), uebung('waerme', 'Wie viel wird Wärme?'), uebung('motor', 'Mit Motor hinauf')],
    auf4, f'<a href="{TS}#erhaltung">Themenseite 4.3, Energieerhaltung</a> · <a href="{TS}#wirkungsgrad">Energiefluss und Verluste</a>')

# ------------------------------------------------------------------ Kapitel 5
sim5 = figur_anim('sim5', 'Kran hebt eine Last in der Hubzeit t; daneben Säulen: zugeführte Energie, Nutzen (Lageenergie) und Verlust', '0 0 300 300',
    '        <div class="reglerfeld">\n          '
    + regler('s5', 'm', '<i>m</i> Last', 50, 500, 10, 100, 'kg', 0) + '\n          '
    + regler('s5', 'h', '<i>h</i> Höhe', 2, 20, 1, 5, 'm', 0) + '\n          '
    + regler('s5', 't', '<i>t</i> Hubzeit', 5, 60, 1, 10, 's', 0) + '\n          '
    + regler('s5', 'eta', '<i>η</i> Wirkungsgrad', 0.5, 0.95, 0.05, 0.9, '', 2) + '\n        </div>')
fest5 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Leistung und Wirkungsgrad</div>
          <p><b>Leistung</b> ist Arbeit pro Zeit, also wie schnell Energie umgesetzt wird. Einheit: das Watt, \(1\;\text{W} = 1\;\text{J/s}\). Bei konstantem Tempo gilt auch \(P = F \cdot v\).</p>
          <p>\[ P = \frac{W}{t} \qquad \eta = \frac{E_\text{nutz}}{E_\text{zu}} = \frac{P_\text{nutz}}{P_\text{zu}} \]</p>
          <p>Der <b>Wirkungsgrad</b> \(\eta\) (sprich «eta») sagt, welcher Anteil der zugeführten Energie nutzbar herauskommt; der Rest wird meist Wärme. Er ist immer kleiner als 1. <b>Energieeffizienz</b> heisst: dieselbe Nutzung mit möglichst wenig zugeführter Energie.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Leistung und Energie verwechselt: Die Kilowattstunde ist eine Energie (\(1\;\text{kW}\) während \(1\;\text{h}\)), das Kilowatt eine Leistung.</p>
          <p>Den Wirkungsgrad umgekehrt: Nutzen durch Aufwand. Ein Ergebnis über 1 ist immer falsch.</p>
        </div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Eine Person (\(70\;\text{kg}\)) steigt in \(20\;\text{s}\) eine Treppe hoch, \(15\;\text{m}\) Höhenunterschied. Wie gross ist ihre Hubleistung? Warum ist es anstrengender, die Treppe in \(10\;\text{s}\) hochzurennen, obwohl die Arbeit gleich bleibt? Begründe.',
     r'<p>\(P = \dfrac{m \cdot g \cdot h}{t}\) \(= \dfrac{70\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 15\;\text{m}}{20\;\text{s}}\) \(\approx 515\;\text{W}\).</p><p>In \(10\;\text{s}\) ist die Arbeit dieselbe, aber sie muss in der halben Zeit verrichtet werden: Die Leistung verdoppelt sich auf rund \(1030\;\text{W}\). Die Muskeln müssen die Energie doppelt so schnell umsetzen.</p>', ''),
    ('5b', 3, r'Ein Elektroauto fährt mit konstant \(72\;\text{km/h}\); der Motor gibt \(15\;\text{kW}\) an die Räder ab. Wie gross ist die Antriebskraft? Welche Leistung liefert die Batterie, wenn der Antrieb einen Wirkungsgrad von \(0.85\) hat?',
     r'<p>\(v = 20\;\text{m/s}\), \(F = \dfrac{P}{v}\) \(= \dfrac{15\,000\;\text{W}}{20\;\text{m/s}}\) \(= 750\;\text{N}\).</p><p>\(P_\text{zu} = \dfrac{P_\text{nutz}}{\eta}\) \(= \dfrac{15\;\text{kW}}{0.85}\) \(\approx 17.6\;\text{kW}\).</p>', ''),
    ('5c', 3, r'Das Diagramm zeigt die Arbeit, die zwei Motoren A und B beim Heben verrichten, über der Zeit. Wie gross ist die Leistung jedes Motors? Wie lange braucht B für \(30\;\text{kJ}\)? (Punkte auf Gitterpunkten)',
     r'<p>Die Leistung ist die Steigung: A: \(P = \dfrac{20\;\text{kJ}}{10\;\text{s}}\) \(= 2\;\text{kW}\). B: \(P = \dfrac{10\;\text{kJ}}{20\;\text{s}}\) \(= 0.5\;\text{kW}\).</p><p>\(t = \dfrac{W}{P}\) \(= \dfrac{30\;\text{kJ}}{0.5\;\text{kW}}\) \(= 60\;\text{s}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="2;0.5" data-namen="A;B" data-farbe="" data-fenster="25,25" data-teilung="2.5,2.5" data-punkte="10,20;20,10" data-xname="t [s]" data-yname="W [kJ]" aria-label="Arbeit über der Zeit, zwei Ursprungsgeraden A und B"></svg></div>'),
    ('5d', 3, r'Eine LED-Lampe (\(8\;\text{W}\), \(\eta = 0.35\)) ersetzt eine Glühlampe (\(60\;\text{W}\), \(\eta = 0.05\)). Geben beide etwa gleich viel Licht? Wie viel Energie spart man in \(1000\) Betriebsstunden?',
     r'<p>Licht: LED \(0.35 \cdot 8\;\text{W} = 2.8\;\text{W}\), Glühlampe \(0.05 \cdot 60\;\text{W} = 3\;\text{W}\) — etwa gleich viel.</p><p>Ersparnis: \((60\;\text{W} - 8\;\text{W}) \cdot 1000\;\text{h} = 52\;\text{kWh}\). Die LED ist energieeffizienter: dieselbe Nutzung mit rund 13 % der Energie.</p>', ''),
])
k5 = kapitel(5, 'leistung-wirkungsgrad', 'Leistung und Wirkungsgrad', 'K6', 40,
    r'Du definierst Leistung und Wirkungsgrad, rechnest mit \(P = \dfrac{W}{t}\), \(P = F \cdot v\) und \(\eta = \dfrac{E_\text{nutz}}{E_\text{zu}}\) und beurteilst die Energieeffizienz technischer Geräte.',
    ('p4-3-lp-leistung', 'Energie sehen: wie schnell und wie gut'),
    sim5, ('p4-3-lp-kontrolle-leistung', 'Kontrollfragen zu Leistung und Wirkungsgrad'),
    fest5, [uebung('leistung', 'Hubleistung'), uebung('pfv', 'Leistung und Antriebskraft'), uebung('eta', 'Wirkungsgrad'), uebung('pt', 'Energie aus Leistung und Zeit')],
    auf5, f'<a href="{TS}#leistung">Themenseite 4.3, Leistung</a> · <a href="{TS}#wirkungsgrad">Wirkungsgrad</a>')

# ------------------------------------------------------------------ Kapitel 6
sim6 = figur_anim('sim6', 'Die Erde zwischen Sonnenstrahlung und Abstrahlung ins All, mit Treibhausgas-Hülle; darunter der Temperaturverlauf über 30 Jahre', '0 0 300 330',
    '        <div class="reglerfeld">\n          '
    + regler('s6', 'al', '<i>a</i> Albedo', 0.2, 0.4, 0.01, 0.32, '', 2) + '\n          '
    + regler('s6', 'f', '<i>f</i> Anteil ins All', 0.55, 1, 0.01, 0.63, '', 2) + '\n        </div>\n'
    + '        <p class="sim-notiz">\\(f\\): Anteil der Wärmestrahlung der Oberfläche, der durch die Atmosphäre ins Weltall gelangt. Mehr Treibhausgas heisst kleineres \\(f\\). Vereinfachtes Modell mit einem Mittelwert für die ganze Erde.</p>')
fest6 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Energiebilanz der Erde</div>
          <p>Die Erde nimmt Energie fast nur als Sonnenstrahlung auf und gibt sie nur als Wärmestrahlung ins Weltall ab. Ausserhalb der Atmosphäre trifft auf jeden Quadratmeter senkrecht zu den Strahlen \(S \approx 1361\;\text{W/m}^2\) (<b>Solarkonstante</b>). Die Erde fängt diese Strahlung mit ihrer Querschnittsfläche \(\pi \cdot R^2\) auf, verteilt sie aber über die ganze Kugeloberfläche \(4 \cdot \pi \cdot R^2\): Im Mittel treffen darum \(\dfrac{S}{4} \approx 340\;\text{W/m}^2\) ein. Den Anteil \(a \approx 0.30\) (<b>Albedo</b>) werfen Wolken, Eis und Luft zurück. Aufgenommen wird</p>
          <p>\[ (1 - a) \cdot \frac{S}{4} \approx 238\;\text{W/m}^2 \]</p>
          <p>Jeder Körper strahlt, und zwar mit der vierten Potenz seiner absoluten Temperatur. Ein idealer Strahler gibt je Quadratmeter ab (Gesetz von Stefan und Boltzmann): \(\dfrac{P}{A} = \sigma \cdot T^4\) mit \(\sigma = 5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4)\) und \(T\) in Kelvin; reale Oberflächen strahlen etwas weniger. Doppelte Temperatur heisst sechzehnfache Abstrahlung. Darum stellt sich ein <b>Gleichgewicht</b> ein: Die Temperatur bleibt, wenn gleich viel hinaus- wie hereinkommt. Strahlt ein Körper so viel ab, wie er aufnimmt, folgt seine <b>Gleichgewichtstemperatur</b> aus \(\sigma \cdot T^4 = \dfrac{P}{A}\):</p>
          <p>\[ T = \sqrt[4]{\frac{P/A}{\sigma}} \]</p>
          <p class="komm">Taschenrechner: hoch \(0.25\) (Taste \(x^y\) oder \(\wedge\)) oder zweimal die Quadratwurzel.</p>
          <p>Treibhausgase (Wasserdampf, \(\text{CO}_2\), Methan) halten einen Teil der Wärmestrahlung zurück — ohne sie wäre die Erde rund \(-18\;^\circ\text{C}\) kalt statt \(+15\;^\circ\text{C}\).</p>
          <p><b>Erderwärmung:</b> Mehr Treibhausgas lässt weniger Wärmestrahlung ins All, schmelzendes Eis senkt die Albedo. Beides macht die Bilanz positiv, und die Erde erwärmt sich, bis sie bei höherer Temperatur wieder ausgeglichen ist. Dass die Erwärmung weiteres Eis schmelzen lässt und sich so selbst verstärkt, heisst <b>Rückkopplung</b>.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>«Das Treibhausgas erzeugt Wärme.» Es erzeugt keine Energie, es hält einen Teil der abgehenden Wärmestrahlung zurück. Die Energie kommt von der Sonne.</p>
          <p>«Im Gleichgewicht fliesst nichts.» Es fliessen ständig rund \(238\;\text{W/m}^2\) herein und genauso viel hinaus.</p>
        </div>
      </div>'''
auf6 = test('t6', 'Aufgaben · Kapitel 6', 12, [
    ('6a', 3, r'Satelliten messen: Von den im Mittel eintreffenden \(\dfrac{S}{4} \approx 340\;\text{W/m}^2\) wirft die Erde \(102\;\text{W/m}^2\) zurück. Wie gross ist ihre Albedo, und wie viel nimmt sie je Quadratmeter auf? Würden wegen schmelzenden Eises nur noch \(95\;\text{W/m}^2\) zurückgeworfen: Was folgte daraus für die Temperatur? Begründe.',
     r'<p>Die Albedo ist der zurückgeworfene Anteil: \(a = \dfrac{102\;\text{W/m}^2}{340\;\text{W/m}^2} = 0.30\). Aufgenommen wird der Rest: \((1 - a) \cdot \dfrac{S}{4}\) \(= 340\;\text{W/m}^2 - 102\;\text{W/m}^2\) \(= 238\;\text{W/m}^2\).</p><p>Mit \(95\;\text{W/m}^2\) zurück (\(a \approx 0.28\)) nimmt die Erde \(245\;\text{W/m}^2\) auf, \(7\;\text{W/m}^2\) mehr. Zuerst kommt mehr herein als hinaus; die Erde erwärmt sich, bis ihre Abstrahlung wieder zur grösseren Aufnahme passt.</p>', ''),
    ('6b', 3, r'Das Diagramm zeigt die Temperatur eines Planeten nach einer Änderung. In welchem Zeitabschnitt nimmt er mehr Energie auf, als er abstrahlt? Ab wann ist die Bilanz ausgeglichen? Begründe.',
     r'<p>Von \(0\) bis rund \(10\) Jahren steigt die Temperatur: Es kommt mehr herein als hinaus. Mit der Temperatur steigt die Abstrahlung (\(\sigma \cdot T^4\)), bis sie zur Aufnahme passt.</p><p>Ab rund \(10\) Jahren bleibt die Temperatur gleich: Die Bilanz ist ausgeglichen — es fliesst weiter Energie, aber gleich viel hinein wie hinaus.</p>',
     '\n            <div class="mini-reihe">' + linien_bild([(0, 288), (2, 289.2), (4, 289.8), (6, 290.1), (10, 290.3), (20, 290.3)], 0, 20, 287, 291, 5, 1, 'Temperatur über der Zeit: steigt von 288 K in rund 10 Jahren auf 290.3 K und bleibt dann gleich', 't [Jahre]', 'T [K]', 'kurve-t') + '</div>'),
    ('6c', 3, r'Ein dunkler Stein liegt in der Sonne, seine Oberfläche hat \(310\;\text{K}\). Wie viel Leistung je Quadratmeter strahlt er ab (\(\sigma = 5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4)\), als idealer Strahler)? Wie viel mehr ist das als nachts bei \(280\;\text{K}\) — als Differenz und als Faktor?',
     r'<p>\(\dfrac{P}{A} = \sigma \cdot T^4\) \(= 5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4) \cdot (310\;\text{K})^4\) \(\approx 524\;\text{W/m}^2\).</p><p>Bei \(280\;\text{K}\): \(\approx 349\;\text{W/m}^2\). Differenz: \(524\;\text{W/m}^2 - 349\;\text{W/m}^2 \approx 175\;\text{W/m}^2\). Faktor: \(\left(\dfrac{310\;\text{K}}{280\;\text{K}}\right)^4 \approx 1.50\) — rund anderthalbmal so viel, obwohl die Temperatur nur um \(11\;\%\) höher ist.</p>', ''),
    ('6d', 3, r'Nenne zwei Gründe der heutigen Erderwärmung. Ordne jeden einem Teil der Bilanz zu — der Aufnahme \((1 - a) \cdot \tfrac{S}{4}\) oder der Abstrahlung ins All — und begründe, warum er die Erde wärmer macht.',
     r'<p>Mehr Treibhausgase (vor allem \(\text{CO}_2\) aus Kohle, Öl und Gas): Weniger Wärmestrahlung gelangt ins All, die Bilanz wird positiv. Kleinere Albedo, wenn Eis und Schnee schmelzen: Die Erde nimmt mehr Sonnenstrahlung auf.</p><p>In beiden Fällen kommt zuerst mehr herein als hinaus, und die Temperatur steigt, bis die Bilanz wieder ausgeglichen ist.</p>', ''),
])
k6 = kapitel(6, 'energiebilanz-erde', 'Die Energiebilanz der Erde', 'K5', 40,
    r'Du beschreibst die Energiebilanz der Erde mit Sonneneinstrahlung, Albedo und Abstrahlung ins Weltall und erklärst damit die Gründe der Erderwärmung.',
    ('p4-3-lp-erde', 'Energie sehen: die Bilanz der Erde'),
    sim6, ('p4-3-lp-kontrolle-erde', 'Kontrollfragen zur Energiebilanz der Erde'),
    fest6, [uebung('albedo', 'Was der Planet aufnimmt'), uebung('strahlung', 'Was eine Fläche abstrahlt'), uebung('gleichgewicht', 'Temperatur im Gleichgewicht')],
    auf6, f'<a href="{TS}#strahlungsbilanz">Themenseite 4.3, Energiebilanz der Erde</a> · <a href="leitprogramm-waerme.html#treibhauseffekt">Leitprogramm Wärme, Kapitel 7: Treibhauseffekt</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/energie/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">4.3 · K1 bis K6</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a>, <a href="#k5">5</a> → K1, K6 · G2 → <a href="#k1">1</a> → K2 · G3 → <a href="#k2">2</a>, <a href="#k3">3</a> → K3 · G4 → <a href="#k1">1</a>, <a href="#k4">4</a> → K2, K4 · G5 → <a href="#k5">5</a> → K6 · G6 → <a href="#k6">6</a> → K5</p>
        </div>
      </div>
    </section>'''

weiter = rf'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Spannenergie einer Feder, \(E = \tfrac12 \cdot D \cdot s^2\) → <a href="{TS}#elastisch">Themenseite 4.3, Elastische Energie</a></li>
        <li>Wirkungsgrade in Serie und Energieflussdiagramme ganzer Anlagen → <a href="{TS}#wirkungsgrad">Themenseite 4.3, Wirkungsgrad</a>; Heizen und Wärmepumpe → <a href="leitprogramm-waerme.html#energiesysteme">Leitprogramm Wärme, Kapitel 5</a></li>
        <li>Wie der Treibhauseffekt im Einzelnen abläuft (Strahlung, Absorption) → <a href="../themen/p5-2-waerme.html#treibhaus">Themenseite 5.2, Treibhauseffekt</a> · <a href="../themen/p6-1-wellen.html#absorption">Themenseite 6.1, Absorption</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Energie, Version 1.1 (06.10.2026: Prüfbefunde behoben, vorgerechnetes Problem in jedem
     Einführungsclip; Version 1.0 vom 04.10.2026, nach /lp-pruefung am 06.10.2026 freigeschaltet).
     Viertes Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip → ② laufende Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen →
     Festhalten → ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und
     Bewertungspaket nur als PDF (downloads/leitprogramme/energie/*.tex). Quelle: scripts/lp/energie/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 4.3 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 den Begriff «Energie» definieren und die wesentlichen Energieformen aufzählen
       K2 den Begriff «Arbeit» definieren und bei einfachen Objekt-Bewegungen anwenden
       K3 die mechanische Energie (kinetische Energie und potentielle Energie) definieren und das
          Prinzip ihrer Erhaltung in einfachen Berechnungen nutzen
       K4 das Prinzip der Energieerhaltung formulieren (inkl. Motor und Reibung) und in einfachen
          Berechnungen anwenden
       K5 die Energie-Bilanz der Erde mit Sonneneinstrahlung und Abstrahlung ins Universum und die
          Gründe der Erderwärmung beschreiben
       K6 die Begriffe «Leistung» und «Energieeffizienz» definieren und sie auf technische
          Anwendungen übertragen

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1 · Aufg. 1a · G1     K2 → Kap. 1 · Aufg. 1b–1d · G2 G4
       K3 → Kap. 2, 3 · Aufg. 2a–3d · G3     K4 → Kap. 4 · Aufg. 4a–4d · G4
       K5 → Kap. 6 · Aufg. 6a–6d · G6     K6 → Kap. 5 · Aufg. 5a–5d · G1 G5
     Jedes Kapitel im Gesamttest: G1 (1, 5) · G2 (1) · G3 (2, 3) · G4 (1, 4) · G5 (5) · G6 (6).
     Bewusst weggelassen: Spannenergie (in keiner Kompetenz genannt), Wirkungsgrade in Serie
     (auf der Themenseite). Albedo heisst wie auf der Themenseite a.
     Zeiten: K0 10 · K1–K6 je 40 · Gesamttest 30 = 280 min ≈ 6.2 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Energie</h1>
      <p class="unter">Arbeit, Lage- und Bewegungsenergie, Energieerhaltung mit Reibung und Motor, Leistung und Wirkungsgrad, die Energiebilanz der Erde — mit laufenden Simulationen. Sechs Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 4 · Teilgebiet 4.3</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Energie und Arbeit</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Lage- und Bewegungsenergie</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Energieerhaltung</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Reibung und Motor</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Leistung und Wirkungsgrad</span></a></li></ol>
    <p class="lekt">Lektion 6</p>
    <ol><li><a href="#k6"><span class="nr">6</span><span>Die Energiebilanz der Erde</span></a></li></ol>
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
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 4, Teilgebiet 4.3 Energie</p>
        <ul>
          <li><b>K1</b> den Begriff «Energie» definieren und die wesentlichen Energieformen aufzählen</li>
          <li><b>K2</b> den Begriff «Arbeit» definieren und bei einfachen Objekt-Bewegungen anwenden</li>
          <li><b>K3</b> die mechanische Energie (kinetische Energie und potentielle Energie) definieren und das Prinzip ihrer Erhaltung in einfachen Berechnungen nutzen</li>
          <li><b>K4</b> das Prinzip der Energieerhaltung formulieren (inkl. Motor und Reibung) und in einfachen Berechnungen anwenden</li>
          <li><b>K5</b> die Energie-Bilanz der Erde mit Sonneneinstrahlung und Abstrahlung ins Universum und die Gründe der Erderwärmung beschreiben</li>
          <li><b>K6</b> die Begriffe «Leistung» und «Energieeffizienz» definieren und sie auf technische Anwendungen übertragen</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">4.3 Energie</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Energie · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Arbeit') + k1 + band(2, 'Mechanische Energie') + k2 + band(3, 'Erhaltung') + k3
        + band(4, 'Reibung und Motor') + k4 + band(5, 'Leistung') + k5 + band(6, 'Erde') + k6 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
