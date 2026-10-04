"""Baut leitprogramme/leitprogramm-kinematik.html aus einer Kapitelbeschreibung (seit 04.10.2026).

  python3 scripts/lp/kinematik/seite.py

Zweites Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4), als Kopie von
scripts/lp/elektrizitaet/ entstanden: Kopf, CSS, Grundskript und Bausteine wörtlich von dort,
neu sind Kapitel, Simulationen und Übungstypen (seite.js). Nur den SEO-Block übernimmt das Skript
aus der bestehenden Seite, damit build-seo.py ihn pflegen kann. Wiederholbar. Danach
build-seo.py, Pre-Flight. Siehe README.md.
"""
import os
import re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/leitprogramm-kinematik.html'
TS = '../themen/p4-1-kinematik.html'

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
<title>Leitprogramm Kinematik</title>
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
/* Diagramme: Farben wie auf Themenseite 4.1 (STYLEGUIDE §5.2) — s Bernstein, v Grün,
   a und Komponenten Violett, a_z und Resultierende Rot; Ziele Lila gestrichelt */
.sim .gitter,svg.mini .gitter{stroke:var(--linie);stroke-width:.6}
.sim .achse,svg.mini .achse{stroke:var(--tinte-2);stroke-width:1.2}
.sim .pfeil,svg.mini .pfeil{fill:var(--tinte-2)}
.sim .skala,svg.mini .skala{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.achsname{fill:var(--tinte);font-family:var(--sans);font-size:11.5px;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.hilf-text{fill:var(--tinte-2);font-family:var(--sans);font-size:10px}
.sim .zielkurve{fill:none;stroke:var(--lila);stroke-width:3;stroke-dasharray:7 5;opacity:.9}
.ziel-text{fill:var(--lila);font-family:var(--sans);font-size:11px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.zielmarke{fill:var(--lila-hell);stroke:var(--lila);stroke-width:1.5}
.kurve-s{fill:none;stroke:var(--bernstein);stroke-width:2.6}
.kurve-v{fill:none;stroke:var(--gruen);stroke-width:2.6}
.kurve-weiter{fill:none;stroke:var(--gruen);stroke-width:1.6;stroke-dasharray:3 4;opacity:.45}
.dreieck{fill:none;stroke:var(--tinte-2);stroke-width:1.3;stroke-dasharray:4 3}
.sim .feld{fill:var(--bernstein-hell);stroke:var(--bernstein);stroke-width:1;opacity:.95}
.sim .feld-neg{fill:var(--rot-hell);stroke:var(--rot);stroke-width:1;stroke-dasharray:4 3;opacity:.95}
.flaeche-text{fill:var(--bernstein);font-family:var(--sans);font-size:12px;font-weight:700;stroke:var(--karte);stroke-width:3px;paint-order:stroke}
.p-s{fill:var(--bernstein)} .p-v{fill:var(--gruen)} .p-land{fill:var(--tinte)}
text.p-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:4px;paint-order:stroke}
.bahn{fill:none;stroke:var(--bernstein);stroke-width:1.6;opacity:.7}
.turm{stroke:var(--tinte-2);stroke-width:4}
.proj{stroke:var(--bernstein);stroke-width:1.4}
.wasser{fill:var(--blau-hell)}
.uferlinie{stroke:var(--tinte-2);stroke-width:1.5}
.bahn-weg{stroke:var(--rot);stroke-width:1.5;stroke-dasharray:5 4}
.pf-linie{stroke-width:2.6;fill:none}
.pf-linie.pf-v{stroke:var(--gruen)} .pf-kopf.pf-v{fill:var(--gruen)}
.pf-linie.pf-f{stroke:var(--lila)} .pf-kopf.pf-f{fill:var(--lila)}
.pf-linie.pf-r,.pf-linie.pf-a{stroke:var(--rot)} .pf-kopf.pf-r,.pf-kopf.pf-a{fill:var(--rot)}
.pf-linie.pf-stroem{stroke:var(--blau);stroke-width:1.3;opacity:.7} .pf-kopf.pf-stroem{fill:var(--blau);opacity:.7}
.pf-text{font-family:var(--sans);font-size:11.5px;font-weight:700;stroke:var(--karte);stroke-width:3.5px;paint-order:stroke}
text.pf-v{fill:var(--gruen)} text.pf-f{fill:var(--lila)} text.pf-r,text.pf-a{fill:var(--rot)}
.bahn-kreis{fill:none;stroke:var(--tinte-2);stroke-width:1.6}
.radius{stroke:var(--tinte-2);stroke-width:1.2;stroke-dasharray:4 3}
.koerper{fill:var(--karte);stroke:var(--tinte);stroke-width:2}
.knoten{fill:var(--tinte)}
.bt-text{fill:var(--tinte);font-family:var(--sans);font-size:11px}
.bt-klein{fill:var(--tinte-2);font-family:var(--sans);font-size:9.5px}
svg.mini{width:190px;height:auto;background:var(--karte);border:1px solid var(--linie);border-radius:6px}
.kurve-mini{fill:none;stroke:var(--tinte-2);stroke-width:2.2}
.kurve-mini.kurve-s{stroke:var(--bernstein);stroke-width:2.2} .kurve-mini.kurve-v{stroke:var(--gruen);stroke-width:2.2}
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
  var KEY = 'leitprogramm-kinematik-v1';

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
  <p>Leitprogramm · Kinematik</p>
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


def clipkarte(datei, titel, zeit):
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
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz">4.1 · {komp}</span><span class="zeit">≈ {zeit} min</span></div>
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
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz">Vorwissen · 0.1 · 0.2</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">km/h und m/s, Gleichungen umstellen, Sinus und Kosinus, Bogenmass. Wenn das wackelt: <a href="leitprogramm-rechnen.html">Leitprogramm Rechnen und Schliessen</a> und <a href="leitprogramm-vorwissen.html">Leitprogramm Grössen, Messen, Druck</a>.</p>
      ''' + clipkarte('p0-1-umstellen', 'Gleichungen umstellen: auf beiden Seiten dasselbe tun', '0:56') + r'''
''' + test('t0', 'Vortest', 10, [
    ('0a', 3, r'Rechne um: \(72\;\text{km/h}\) in \(\text{m/s}\), \(15\;\text{m/s}\) in \(\text{km/h}\), \(2.5\;\text{min}\) in \(\text{s}\).',
     r'<p>\(\dfrac{72}{3.6}\;\text{m/s} = 20\;\text{m/s}\), \(15 \cdot 3.6\;\text{km/h} = 54\;\text{km/h}\), \(2.5 \cdot 60\;\text{s} = 150\;\text{s}\).</p><p class="komm">Falsch? <a href="' + P02 + r'#umrechnen">Vorwissen 0.2, Einheiten umrechnen</a></p>', ''),
    ('0b', 3, r'Stelle \(s = \tfrac12 \cdot a \cdot t^2\) nach \(a\) und nach \(t\) um, und \(v = \omega \cdot r\) nach \(\omega\).',
     r'<p>\(a = \dfrac{2s}{t^2}\), \(t = \sqrt{\dfrac{2s}{a}}\), \(\omega = \dfrac{v}{r}\).</p><p class="komm">Falsch? Der Clip oben und <a href="' + P01 + r'#umformen">Vorwissen 0.1, Gleichungen umstellen</a></p>', ''),
    ('0c', 2, r'Taschenrechner im Gradmodus: \(\sin 30^\circ\), \(\cos 60^\circ\) und \(\sqrt{3^2 + 4^2}\)?',
     r'<p>\(\sin 30^\circ = 0.5\), \(\cos 60^\circ = 0.5\), \(\sqrt{9 + 16} = 5\).</p><p class="komm">Kommt bei \(\sin 30\) etwas Negatives heraus, steht der Rechner im Bogenmass: <a href="' + P02 + r'#rechner">Vorwissen 0.2, DEG oder RAD</a></p>', ''),
    ('0d', 2, r'Wie viele Radiant sind eine volle Umdrehung? Wie lange dauert eine Umdrehung bei \(120\) Umdrehungen pro Minute?',
     r'<p>\(2\pi \approx 6.28\) rad. \(\dfrac{60\;\text{s}}{120} = 0.5\;\text{s}\).</p><p class="komm">Falsch? <a href="' + P01 + r'#kreiszahl">Vorwissen 0.1, Kreiszahl und Bogenmass</a></p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: zuerst die verlinkten Stellen zu den falschen Aufgaben, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Kapitel 1: Ort und Geschwindigkeit
sim1 = figur('sim1', 'Ort s über der Zeit t: Gerade mit der Geschwindigkeit v als Steigung und dem Startort als Achsenabschnitt', '-4 -4 308 268',
    '        <div class="reglerfeld">\n          '
    + regler('s1', 'v', '<i>v</i> Tempo', -5, 12, 0.5, 5, 'm/s', 1) + '\n          '
    + regler('s1', 's0', '<i>s</i>₀ Start', 0, 60, 5, 20, 'm', 0) + '\n          '
    + regler('s1', 't', '<i>t</i> Zeit', 0, 12, 0.5, 8, 's', 1) + '\n        </div>',
    'Steigungsdreieck')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Bewegung beschreiben</div>
          <p><b>Schwerpunkt:</b> der Punkt, der sich so verhält, als wäre die ganze Masse des Körpers in ihm vereinigt. Für eine Verschiebung ohne Drehung genügt seine Bewegung. <b>Bahnkurve:</b> die Linie, die der Schwerpunkt im Lauf der Zeit durchläuft — gerade, kreisförmig oder gekrümmt.</p>
          <p><b>Geschwindigkeit:</b> zurückgelegte Strecke pro Zeit. Die Durchschnittsgeschwindigkeit gilt für ein ganzes Zeitintervall, die Momentangeschwindigkeit für einen Zeitpunkt (das zeigt der Tacho). Auf einer Geraden zeigt das Vorzeichen von \(v\) die Richtung: negativ heisst zurück, zum Nullpunkt hin.</p>
          <p>\[ \bar v = \frac{\Delta s}{\Delta t}, \qquad 1\;\text{m/s} = 3.6\;\text{km/h} \]</p>
          <p>Geradlinig gleichförmig heisst: \(v\) ist konstant. Dann gilt</p>
          <p>\[ s(t) = s_0 + v \cdot t \]</p>
          <p>Im \(s\)-\(t\)-Diagramm ist das eine Gerade: Ihre Steigung ist \(v\), ihr Achsenabschnitt der Startort \(s_0\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>km/h nicht umgerechnet: \(72\;\text{km/h}\) während \(10\;\text{s}\) sind nicht \(720\;\text{m}\). Zuerst \(72\;\text{km/h} = 20\;\text{m/s}\), dann \(s = 20\;\text{m/s} \cdot 10\;\text{s} = 200\;\text{m}\).</p>
          <p>Die Durchschnittsgeschwindigkeit ist nicht der Mittelwert zweier Tachowerte, sondern die ganze Strecke durch die ganze Zeit.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 11, [
    ('1a', 3, r'Erkläre in je einem Satz, was der Schwerpunkt und was die Bahnkurve eines Körpers ist. Nenne zu jeder Bahnform — gerade, kreisförmig, gekrümmt — ein Beispiel.',
     r'<p>Der Schwerpunkt ist der Punkt, der sich so bewegt, als wäre die ganze Masse in ihm vereinigt. Die Bahnkurve ist die Linie, die er im Lauf der Zeit durchläuft.</p><p>Beispiele: gerade — ein Auto auf gerader Strasse; kreisförmig — eine Gondel des Riesenrads; gekrümmt — ein geworfener Ball (Wurfparabel). Andere passende Beispiele zählen ebenso.</p>', ''),
    ('1b', 3, r'Ein Velofahrer fährt \(12\;\text{km}\) in \(40\;\text{min}\). Am Berg zeigt sein Tacho \(9\;\text{km/h}\), in der Abfahrt \(45\;\text{km/h}\). Wie gross ist seine Durchschnittsgeschwindigkeit, in km/h und in m/s? Was zeigt der Tacho?',
     r'<p>\(\bar v = \dfrac{\Delta s}{\Delta t} = \dfrac{12\;\text{km}}{\tfrac{40}{60}\;\text{h}} = 18\;\text{km/h}\), und \(\dfrac{18}{3.6}\;\text{m/s} = 5\;\text{m/s}\).</p><p>Der Tacho zeigt die Momentangeschwindigkeit, also das Tempo im jeweiligen Augenblick.</p><p class="komm">Nicht \(\tfrac{9 + 45}{2} = 27\;\text{km/h}\): Am Berg ist er viel länger unterwegs als in der Abfahrt.</p>', ''),
    ('1c', 3, r'Das Diagramm zeigt zwei Läufer A und B. Lies für beide Startort und Geschwindigkeit ab. Wann und wo holt A den B ein? (Punkte auf Gitterpunkten)',
     r'<p>A: \(s_0 = 0\;\text{m}\), \(v = \dfrac{12\;\text{m}}{6\;\text{s}} = 2\;\text{m/s}\). B: \(s_0 = 12\;\text{m}\), \(v = \dfrac{14\;\text{m} - 12\;\text{m}}{4\;\text{s}} = 0.5\;\text{m/s}\).</p><p>Die Geraden schneiden sich bei \(t = 8\;\text{s}\), \(s = 16\;\text{m}\). Probe: \(2\;\text{m/s} \cdot 8\;\text{s} = 16\;\text{m}\) und \(12\;\text{m} + 0.5\;\text{m/s} \cdot 8\;\text{s} = 16\;\text{m}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="2;0.5,12" data-namen="A;B" data-farbe="kurve-s" data-fenster="10,24" data-teilung="1,2" data-punkte="6,12;0,12;4,14;8,16" data-xname="t [s]" data-yname="s [m]" aria-label="s-t-Diagramm mit zwei Geraden A und B"></svg></div>'),
    ('1d', 2, r'Warum bedeutet eine fallende Gerade im \(s\)-\(t\)-Diagramm, dass sich der Körper zurück bewegt? Und warum steht er bei einer waagrechten Geraden still?',
     r'<p>Die Steigung ist die Geschwindigkeit. Fällt die Gerade, wird der Ort \(s\) mit der Zeit kleiner: \(v\) ist negativ, der Körper bewegt sich zum Nullpunkt hin.</p><p>Bei einer waagrechten Geraden ändert sich \(s\) nicht: \(v = 0\), der Körper bleibt am selben Ort.</p>', ''),
])
k1 = kapitel(1, 'ort-und-geschwindigkeit', 'Ort, Bahn und Geschwindigkeit', 'K1 · K3', 40,
    r'Du erklärst Schwerpunkt, Bahnkurve und Geschwindigkeit, unterscheidest Durchschnitts- und Momentangeschwindigkeit und rechnest mit \(s = s_0 + v \cdot t\).',
    ('p4-1-lp-gleichfoermig', 'Bewegung sehen: Ort, Bahn und Tempo', '1:32'),
    sim1, ('p4-1-lp-kontrolle-gleichfoermig', 'Kontrollfragen zu Ort und Geschwindigkeit', '0:34'),
    fest1, [uebung('ort', 'Ort bei konstanter Geschwindigkeit'), uebung('mittel', 'Durchschnittsgeschwindigkeit'),
            uebung('einholen', 'Einholen')],
    auf1, f'<a href="{TS}#definition">Themenseite 4.1, Grundbegriffe</a> · <a href="{TS}#darstellungen">Geradlinig gleichförmige Bewegung</a>')

# ------------------------------------------------------------------ Kapitel 2: Beschleunigung
sim2 = figur('sim2', 'Geschwindigkeit v über der Zeit t: Gerade mit der Beschleunigung a als Steigung, die Fläche darunter ist der Weg s', '-4 -4 308 268',
    '        <div class="reglerfeld">\n          '
    + regler('s2', 'v0', '<i>v</i>₀ Start', 0, 30, 1, 0, 'm/s', 0) + '\n          '
    + regler('s2', 'a', '<i>a</i>', -6, 4, 0.5, 2.5, 'm/s²', 1) + '\n          '
    + regler('s2', 't', '<i>t</i> Zeit', 0, 10, 0.5, 8, 's', 1) + '\n        </div>',
    'Steigungsdreieck')
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Beschleunigung</div>
          <p><b>Beschleunigung:</b> die Änderung der Geschwindigkeit pro Zeit. Positiv in Bewegungsrichtung heisst schneller werden, negativ (Bremsbeschleunigung) langsamer werden.</p>
          <p>\[ a = \frac{\Delta v}{\Delta t}, \qquad [a] = \text{m/s}^2 \]</p>
          <p>Für eine <b>konstante</b> Beschleunigung gelten die drei Bewegungsgleichungen:</p>
          <p>\[ v = v_0 + a \cdot t \qquad s = s_0 + v_0 \cdot t + \tfrac12 \cdot a \cdot t^2 \qquad v^2 = v_0^2 + 2 \cdot a \cdot (s - s_0) \]</p>
          <p>Im \(v\)-\(t\)-Diagramm ist die Steigung die Beschleunigung, die Fläche unter der Geraden die Ortsänderung — solange \(v\) das Vorzeichen nicht wechselt, ist das der zurückgelegte Weg. Bremsweg bis zum Stillstand: \(s = \dfrac{v_0^2}{2 \cdot |a|}\) — doppeltes Tempo, vierfacher Bremsweg.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Den Faktor \(\tfrac12\) vergessen: Aus dem Stand mit \(2\;\text{m/s}^2\) sind es nach \(10\;\text{s}\) nicht \(200\;\text{m}\), sondern \(s = \tfrac12 \cdot 2\;\text{m/s}^2 \cdot (10\;\text{s})^2 = 100\;\text{m}\) — die Fläche ist ein Dreieck.</p>
          <p>Beim Bremsen ist \(a\) negativ. Wer \(a = -5\;\text{m/s}^2\) positiv einsetzt, bekommt einen negativen Bremsweg.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 13, [
    ('2a', 3, r'Ein Tram beschleunigt in \(12\;\text{s}\) gleichmässig aus dem Stand auf \(36\;\text{km/h}\). Wie gross ist die Beschleunigung? Welchen Weg legt es dabei zurück?',
     r'<p>\(v = \dfrac{36}{3.6}\;\text{m/s} = 10\;\text{m/s}\).</p><p>\(a = \dfrac{\Delta v}{\Delta t} = \dfrac{10\;\text{m/s}}{12\;\text{s}} \approx 0.833\;\text{m/s}^2\).</p><p>Mit dem genauen Wert \(a = \tfrac56\;\text{m/s}^2\): \(s = \tfrac12 \cdot a \cdot t^2\) \(= \tfrac12 \cdot \tfrac56\;\text{m/s}^2 \cdot (12\;\text{s})^2\) \(= 60\;\text{m}\) — oder als Dreiecksfläche \(\tfrac12 \cdot 12\;\text{s} \cdot 10\;\text{m/s} = 60\;\text{m}\).</p>', ''),
    ('2b', 3, r'Das \(v\)-\(t\)-Diagramm zeigt einen Körper mit konstanter Beschleunigung. Lies \(v_0\) und \(a\) ab. Welchen Weg legt er in den ersten \(6\;\text{s}\) zurück? (Punkte auf Gitterpunkten)',
     r'<p>\(v_0 = 2\;\text{m/s}\) (Achsenabschnitt). \(a = \dfrac{\Delta v}{\Delta t} = \dfrac{14\;\text{m/s} - 2\;\text{m/s}}{6\;\text{s}} = 2\;\text{m/s}^2\) (Steigung).</p><p>Weg = Trapezfläche: \(s = \dfrac{2\;\text{m/s} + 14\;\text{m/s}}{2} \cdot 6\;\text{s} = 48\;\text{m}\). Probe: \(s = v_0 \cdot t + \tfrac12 \cdot a \cdot t^2\) \(= 12\;\text{m} + 36\;\text{m} = 48\;\text{m}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini" data-geraden="2,2" data-farbe="kurve-v" data-fenster="8,16" data-teilung="1,2" data-punkte="0,2;6,14" data-xname="t [s]" data-yname="v [m/s]" aria-label="v-t-Diagramm: Gerade von 2 m/s bei 0 s bis 14 m/s bei 6 s"></svg></div>'),
    ('2c', 5, r'Ein Auto fährt mit \(90\;\text{km/h}\). Die Fahrerin reagiert nach \(1\;\text{s}\) und bremst dann gleichmässig mit \(6\;\text{m/s}^2\) bis zum Stillstand. Wie lang ist der Anhalteweg (Reaktionsweg plus Bremsweg)? Skizziere das \(v\)-\(t\)-Diagramm des ganzen Vorgangs.',
     r'<p>\(v_0 = \dfrac{90}{3.6}\;\text{m/s} = 25\;\text{m/s}\).</p><p>Reaktionsweg, gleichförmig: \(s_1 = v_0 \cdot t = 25\;\text{m/s} \cdot 1\;\text{s} = 25\;\text{m}\).</p><p>Bremsweg aus \(v^2 = v_0^2 + 2 \cdot a \cdot s\) mit \(v = 0\): \(s_2 = \dfrac{v_0^2}{2 \cdot |a|} = \dfrac{(25\;\text{m/s})^2}{2 \cdot 6\;\text{m/s}^2} \approx 52.1\;\text{m}\).</p><p>Anhalteweg: \(s = 25\;\text{m} + 52.1\;\text{m} \approx 77.1\;\text{m}\).</p><p>Skizze: \(t\) in s nach rechts, \(v\) in m/s nach oben. Eine waagrechte Linie bei \(25\;\text{m/s}\) bis \(1\;\text{s}\), dann eine fallende Gerade bis \(v = 0\) bei \(t = 1\;\text{s} + \dfrac{25\;\text{m/s}}{6\;\text{m/s}^2} \approx 5.17\;\text{s}\). Die Fläche darunter — Rechteck plus Dreieck — ist der Anhalteweg.</p>', ''),
    ('2d', 2, r'Ein Auto braucht bei \(30\;\text{km/h}\) einen Bremsweg von \(6\;\text{m}\). Wie lang ist er bei \(50\;\text{km/h}\), gleich stark gebremst? Begründe, ohne \(a\) auszurechnen.',
     r'<p>Im Bremsweg \(s = \dfrac{v_0^2}{2 \cdot |a|}\) steht die Geschwindigkeit im Quadrat. Das Tempo wächst um den Faktor \(\tfrac{50}{30} = \tfrac53\), der Bremsweg also um \(\left(\tfrac53\right)^2 = \tfrac{25}{9}\): \(s = 6\;\text{m} \cdot \tfrac{25}{9} \approx 16.7\;\text{m}\).</p><p class="komm">Kein Umrechnen in m/s nötig: Es zählt nur das Verhältnis der Geschwindigkeiten.</p>', ''),
])
k2 = kapitel(2, 'beschleunigung', 'Beschleunigung und Bremsweg', 'K1 · K3', 40,
    r'Du erklärst die Beschleunigung, liest \(v\)-\(t\)-Diagramme über Steigung und Fläche und löst Aufgaben mit den Bewegungsgleichungen für konstante Beschleunigung.',
    ('p4-1-lp-beschleunigt', 'Bewegung sehen: Beschleunigung ist Steigung, Weg ist Fläche', '1:22'),
    sim2, ('p4-1-lp-kontrolle-beschleunigt', 'Kontrollfragen zur Beschleunigung', '0:33'),
    fest2, [uebung('beschl', 'Beschleunigung aus zwei Geschwindigkeiten'), uebung('endwerte', 'Geschwindigkeit und Weg nach der Zeit t'),
            uebung('bremsweg', 'Bremsweg')],
    auf2, f'<a href="{TS}#definition">Themenseite 4.1, Grundbegriffe</a> · <a href="{TS}#theorie">Gleichmässig beschleunigte Bewegung</a>')

# ------------------------------------------------------------------ Kapitel 3: Fall und Wurf
sim3 = figur('sim3', 'Wurfbahn in der x-y-Ebene, Massstab 1:1: der Ort alle 0.25 s als Punkte, mit Abwurfhöhe, Abwurftempo und Winkel', '-4 -4 308 220',
    '        <div class="reglerfeld">\n          '
    + regler('s3', 'v0', '<i>v</i>₀ Tempo', 0, 20, 0.5, 8, 'm/s', 1) + '\n          '
    + regler('s3', 'al', '<i>α</i> Winkel', 0, 80, 5, 0, '°', 0) + '\n          '
    + regler('s3', 'h0', '<i>h</i>₀ Höhe', 0, 30, 1, 20, 'm', 0) + '\n        </div>',
    'Projektion auf die Achsen')


def wurfbild():
    """Aufgabe 3d: waagrechter Wurf, h0 = 5 m, v0 = 4 m/s, Ort alle 0.2 s. Massstab 1:1 (24 px je m)."""
    import math
    k, ox, oy = 24, 34, 140
    t = ['<svg class="mini breit" viewBox="0 0 240 158" role="img" aria-label="Waagrechter Wurf aus 5 m Höhe mit 4 m/s: sechs Punkte im Abstand von 0.2 s">',
         f'<line x1="{ox}" y1="{oy}" x2="{ox + 5.4 * k:.0f}" y2="{oy}" class="achse"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - 5.6 * k:.0f}" class="achse"/>']
    for m in range(1, 6):
        t.append(f'<line x1="{ox + m * k}" y1="{oy - 3}" x2="{ox + m * k}" y2="{oy + 3}" class="achse"/><text x="{ox + m * k}" y="{oy + 13}" text-anchor="middle" class="skala">{m}</text>')
        t.append(f'<line x1="{ox - 3}" y1="{oy - m * k}" x2="{ox + 3}" y2="{oy - m * k}" class="achse"/><text x="{ox - 6}" y="{oy - m * k + 4}" text-anchor="end" class="skala">{m}</text>')
    for i in range(6):
        tt = 0.2 * i
        x, y = 4 * tt, 5 - 0.5 * 9.81 * tt * tt
        t.append(f'<line x1="{ox + x * k:.1f}" y1="{oy - 3}" x2="{ox + x * k:.1f}" y2="{oy + 3}" class="proj"/>'
                 f'<line x1="{ox - 3}" y1="{oy - y * k:.1f}" x2="{ox + 3}" y2="{oy - y * k:.1f}" class="proj"/>'
                 f'<circle cx="{ox + x * k:.1f}" cy="{oy - y * k:.1f}" r="3.4" class="p-s"/>')
    t.append(f'<text x="{ox + 5.4 * k:.0f}" y="{oy - 6}" text-anchor="end" class="achsname">x [m]</text><text x="{ox + 6}" y="{oy - 5.6 * k + 10:.0f}" class="achsname">y [m]</text></svg>')
    return ''.join(t)


fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Fall und Wurf</div>
          <p><b>Freier Fall</b> (ohne Luftwiderstand): gleichmässig beschleunigt mit \(g = 9.81\;\text{m/s}^2\) nach unten, für alle Körper gleich, unabhängig von der Masse. Aus der Ruhe:</p>
          <p>\[ v = g \cdot t \qquad h = \tfrac12 \cdot g \cdot t^2 \qquad t = \sqrt{\frac{2h}{g}} \]</p>
          <p><b>Wurf:</b> zwei Bewegungen, die sich nicht stören — waagrecht gleichförmig, senkrecht wie der freie Fall. Mit Abwurftempo \(v_0\), Winkel \(\alpha\) und Abwurfhöhe \(h_0\):</p>
          <p>\[ x(t) = v_0 \cdot \cos\alpha \cdot t \qquad y(t) = h_0 + v_0 \cdot \sin\alpha \cdot t - \tfrac12 \cdot g \cdot t^2 \]</p>
          <p>Die Bahnkurve ist eine Parabel. Beim waagrechten Wurf ist \(\alpha = 0^\circ\): Die Flugzeit hängt nur von der Höhe ab, und senkrecht wird der Körper wie im freien Fall schneller, \(v_y = g \cdot t\). Landet der Körper auf Abwurfhöhe (\(h_0 = 0\)), gilt \(t_F = \dfrac{2 \cdot v_0 \cdot \sin\alpha}{g}\) und \(s_x = \dfrac{v_0^2 \cdot \sin(2\alpha)}{g}\) — am weitesten bei \(45^\circ\), gleich weit bei \(\alpha\) und \(90^\circ - \alpha\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Die Wurzel vergessen: Aus \(20\;\text{m}\) fällt ein Stein nicht \(\dfrac{2 \cdot 20}{9.81} \approx 4.1\;\text{s}\), sondern \(\sqrt{\dfrac{2 \cdot 20\;\text{m}}{9.81\;\text{m/s}^2}} \approx 2.02\;\text{s}\).</p>
          <p>Taschenrechner im Bogenmass: \(\sin 30\) gibt dann \(-0.988\) statt \(0.5\). Für Winkel in Grad muss er auf DEG stehen.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 11, [
    ('3a', 3, r'Ein Schlüssel fällt aus \(12\;\text{m}\) Höhe frei (ohne Luftwiderstand). Wie lange fällt er? Mit welcher Geschwindigkeit trifft er auf, in m/s und km/h?',
     r'<p>\(t = \sqrt{\dfrac{2h}{g}} = \sqrt{\dfrac{2 \cdot 12\;\text{m}}{9.81\;\text{m/s}^2}} \approx 1.56\;\text{s}\).</p><p>\(v = g \cdot t = 9.81\;\text{m/s}^2 \cdot 1.564\;\text{s} \approx 15.3\;\text{m/s}\), das sind \(15.34 \cdot 3.6\;\text{km/h} \approx 55.2\;\text{km/h}\).</p>', ''),
    ('3b', 3, r'Ein Wasserstrahl tritt \(1.25\;\text{m}\) über dem Boden waagrecht mit \(4\;\text{m/s}\) aus einem Rohr. Wie lange ist ein Tropfen unterwegs, und wie weit vom Rohr trifft er den Boden?',
     r'<p>Senkrecht wie im freien Fall: \(t = \sqrt{\dfrac{2h}{g}} = \sqrt{\dfrac{2 \cdot 1.25\;\text{m}}{9.81\;\text{m/s}^2}} \approx 0.505\;\text{s}\).</p><p>Waagrecht gleichförmig: \(x = v_0 \cdot t = 4\;\text{m/s} \cdot 0.505\;\text{s} \approx 2.02\;\text{m}\).</p>', ''),
    ('3c', 3, r'Ein Fussball wird vom Boden mit \(18\;\text{m/s}\) unter \(30^\circ\) gekickt und landet wieder auf dem Boden. Wie lange fliegt er, und wie weit? (ohne Luftwiderstand)',
     r'<p>Senkrecht: \(v_0 \cdot \sin\alpha = 18\;\text{m/s} \cdot \sin 30^\circ = 9\;\text{m/s}\); aus \(y(t_F) = 0\): \(t_F = \dfrac{2 \cdot 9\;\text{m/s}}{9.81\;\text{m/s}^2} \approx 1.83\;\text{s}\).</p><p>Waagrecht: \(v_0 \cdot \cos\alpha = 18\;\text{m/s} \cdot \cos 30^\circ \approx 15.6\;\text{m/s}\); \(s_x = 15.59\;\text{m/s} \cdot 1.835\;\text{s} \approx 28.6\;\text{m}\). Probe: \(s_x = \dfrac{v_0^2 \cdot \sin(2\alpha)}{g}\) \(= \dfrac{(18\;\text{m/s})^2 \cdot \sin 60^\circ}{9.81\;\text{m/s}^2}\) \(\approx 28.6\;\text{m}\).</p>', ''),
    ('3d', 2, r'Das Bild zeigt einen waagrecht geworfenen Ball alle \(0.2\;\text{s}\). Woran erkennst du, dass die waagrechte Bewegung gleichförmig und die senkrechte beschleunigt ist?',
     r'<p>Waagrecht liegen die Punkte immer gleich weit auseinander (je \(0.8\;\text{m}\)): gleiche Wege in gleichen Zeiten, also gleichförmig. Senkrecht werden die Abstände von Punkt zu Punkt grösser (rund \(0.2\), \(0.6\), \(1.0\), \(1.4\), \(1.8\;\text{m}\)): Die Geschwindigkeit nach unten wächst, die Bewegung ist beschleunigt.</p>',
     '\n            <div class="mini-reihe">' + wurfbild() + '</div>'),
])
k3 = kapitel(3, 'fall-und-wurf', 'Freier Fall und Wurf', 'K3', 45,
    r'Du löst Aufgaben zum freien Fall und zum Wurf, indem du die Bewegung in eine waagrechte gleichförmige und eine senkrechte beschleunigte Bewegung zerlegst.',
    ('p4-1-lp-wurf', 'Bewegung sehen: Fall und Wurf in zwei Richtungen', '1:26'),
    sim3, ('p4-1-lp-kontrolle-wurf', 'Kontrollfragen zu Fall und Wurf', '0:37'),
    fest3, [uebung('fall', 'Freier Fall'), uebung('waagrecht', 'Waagrechter Wurf'), uebung('schief', 'Schiefer Wurf vom Boden')],
    auf3, f'<a href="{TS}#freier-fall">Themenseite 4.1, Freier Fall</a> · <a href="{TS}#wurfparabel">Parabolische Bewegung</a>')

# ------------------------------------------------------------------ Kapitel 4: Geschwindigkeit als Vektor
sim4 = f'''      <figure class="sim sim-gross" id="sim4">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 150" role="img" aria-label="Fluss von oben, 40 m breit: Geschwindigkeitspfeile des Schwimmers, der Strömung und ihre Summe, dazu die Bahn bis zum Zielufer"></svg>
        <div class="reglerfeld">
          {regler('s4', 'vS', '<i>v</i><sub>S</sub> Schwimmer', 0.5, 4, 0.25, 2, 'm/s', 2)}
          {regler('s4', 'be', '<i>β</i> Richtung', 30, 150, 1, 90, '°', 0)}
          {regler('s4', 'vF', '<i>v</i><sub>F</sub> Strömung', 0, 3, 0.25, 1, 'm/s', 2)}
        </div>
        <p class="sim-notiz">Draufsicht 1:1. Pfeile: \\(1\\;\\text{{m/s}}\\) entspricht \\(8\\;\\text{{m}}\\). \\(\\beta\\) wird von der Strömungsrichtung aus gemessen; \\(90^\\circ\\) heisst quer zum Ufer.</p>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Geschwindigkeit als Vektor</div>
          <p>Eine Geschwindigkeit hat Betrag und Richtung: Sie ist ein Vektor, gezeichnet als Pfeil. Bewegt sich ein Körper gegenüber einem Träger, der sich selbst bewegt (Person im Zug, Schwimmer im Fluss), ist das seine <b>Relativbewegung</b>. Seine Bewegung gegenüber dem Boden oder dem Ufer — die <b>absolute Bewegung</b> — ist die Summe der Vektoren:</p>
          <p>\[ \vec v_\text{Ufer} = \vec v_S + \vec v_F \]</p>
          <p>Auf einer Geraden genügen Vorzeichen: \(30\;\text{m/s} + 1.5\;\text{m/s}\) in Fahrtrichtung, \(30\;\text{m/s} - 1.5\;\text{m/s}\) dagegen. Stehen die Pfeile senkrecht aufeinander, gilt Pythagoras: \(|\vec v_\text{Ufer}| = \sqrt{v_S^2 + v_F^2}\), und für den Driftwinkel \(\tan\gamma = \dfrac{v_F}{v_S}\).</p>
          <p>Die Schwimmrichtung \(\beta\) wird von der Strömungsrichtung aus gemessen: \(\beta = 90^\circ\) heisst quer zum Ufer, \(\beta \gt 90^\circ\) schräg gegen die Strömung. Querzeit \(t = \dfrac{b}{v_S \cdot \sin\beta}\) — nur die Querkomponente bringt hinüber. Versatz \(d = (v_F + v_S \cdot \cos\beta) \cdot t\). Genau gegenüber kommt an, wer so schräg gegen die Strömung hält, dass \(v_S \cdot \cos\beta = -v_F\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p>Quer stehende Geschwindigkeiten als Zahlen addieren: \(3\;\text{m/s}\) quer und \(4\;\text{m/s}\) Strömung ergeben nicht \(7\;\text{m/s}\), sondern \(\sqrt{9 + 16}\;\text{m/s} = 5\;\text{m/s}\).</p>
          <p>Die Querzeit mit dem Betrag \(|\vec v_\text{Ufer}|\) rechnen: Die Strömung trägt das Boot nur flussabwärts, nicht hinüber.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 12, [
    ('4a', 3, r'Ein Laufband (\(54\;\text{m}\) lang) bewegt sich mit \(1.2\;\text{m/s}\). Du gehst darauf mit \(1.5\;\text{m/s}\) in Laufrichtung. Wie schnell bist du gegenüber dem Boden, und wie lange brauchst du? Wie wäre es gegen die Laufrichtung?',
     r'<p>In Laufrichtung: \(v = 1.2\;\text{m/s} + 1.5\;\text{m/s} = 2.7\;\text{m/s}\), \(t = \dfrac{54\;\text{m}}{2.7\;\text{m/s}} = 20\;\text{s}\).</p><p>Dagegen: \(v = 1.5\;\text{m/s} - 1.2\;\text{m/s} = 0.3\;\text{m/s}\), \(t = \dfrac{54\;\text{m}}{0.3\;\text{m/s}} = 180\;\text{s}\).</p><p class="komm">Gegenüber dem Band bist du in beiden Fällen gleich schnell (\(1.5\;\text{m/s}\)); gegenüber dem Boden nicht.</p>', ''),
    ('4b', 3, r'Ein Flugzeug fliegt mit \(70\;\text{m/s}\) gegenüber der Luft nach Norden; der Wind weht mit \(20\;\text{m/s}\) nach Osten. Zeichne die Pfeile. Wie schnell ist es über Grund, und um welchen Winkel wird es abgetrieben?',
     r'<p>Die Pfeile stehen senkrecht: \(|\vec v| = \sqrt{(70\;\text{m/s})^2 + (20\;\text{m/s})^2}\) \(\approx 72.8\;\text{m/s}\).</p><p>\(\tan\gamma = \dfrac{20\;\text{m/s}}{70\;\text{m/s}}\), also \(\gamma \approx 15.9^\circ\) nach Osten.</p><p class="komm">Skizze: Pfeil nach Norden (70), an seiner Spitze ein Pfeil nach Osten (20), Summe vom Anfang des ersten zur Spitze des zweiten.</p>', ''),
    ('4c', 4, r'Eine Fähre überquert einen \(120\;\text{m}\) breiten Fluss mit \(4\;\text{m/s}\) gegenüber dem Wasser; die Strömung hat \(2\;\text{m/s}\). (a) Sie fährt quer zum Ufer: Wie lange dauert es, und wie weit wird sie versetzt? (b) Unter welchem Winkel \(\beta\) zur Strömung muss sie fahren, um genau gegenüber anzukommen, und wie lange dauert es dann?',
     r'<p>(a) \(t = \dfrac{b}{v_S} = \dfrac{120\;\text{m}}{4\;\text{m/s}} = 30\;\text{s}\), \(d = v_F \cdot t = 2\;\text{m/s} \cdot 30\;\text{s} = 60\;\text{m}\).</p><p>(b) Die Längskomponente muss die Strömung aufheben: \(v_S \cdot \cos\beta = -v_F\), also \(\cos\beta = -\dfrac{2}{4} = -0.5\) und \(\beta = 120^\circ\) — \(30^\circ\) gegen die Strömung geneigt.</p><p>Quergeschwindigkeit \(v_S \cdot \sin\beta = 4\;\text{m/s} \cdot \sin 120^\circ \approx 3.46\;\text{m/s}\), also \(t = \dfrac{120\;\text{m}}{3.464\;\text{m/s}} \approx 34.6\;\text{s}\).</p>', ''),
    ('4d', 2, r'Zwei Schwimmer queren denselben Fluss quer zum Ufer, A mit \(1\;\text{m/s}\), B mit \(2\;\text{m/s}\). Wird B halb so weit versetzt wie A? Begründe.',
     r'<p>Ja. Die Strömung hat keinen Anteil quer über den Fluss; hinüber bringt allein die eigene Geschwindigkeit. B braucht darum nur die halbe Querzeit \(t = \dfrac{b}{v_S}\). Der Versatz \(d = v_F \cdot t\) wächst mit der Zeit, in der die Strömung wirkt: halbe Zeit, halber Versatz.</p>', ''),
])
k4 = kapitel(4, 'vektoren', 'Geschwindigkeit als Vektor', 'K2', 40,
    r'Du stellst Geschwindigkeiten als Pfeile dar und berechnest damit Relativbewegungen und Bewegungen gegenüber dem Boden — auf einer Geraden mit Vorzeichen, quer dazu mit Komponenten.',
    ('p4-1-lp-vektor', 'Bewegung sehen: Geschwindigkeiten addieren sich als Pfeile', '1:24'),
    sim4, ('p4-1-lp-kontrolle-vektor', 'Kontrollfragen zur Vektoraddition', '0:41'),
    fest4, [uebung('eindim', 'Relativ und gegenüber dem Boden'), uebung('quer', 'Quer zur Strömung: Betrag und Winkel'),
            uebung('fluss', 'Querzeit und Versatz')],
    auf4, f'<a href="{TS}#relativbewegung">Themenseite 4.1, Vektoraddition — Relativbewegung</a>')

# ------------------------------------------------------------------ Kapitel 5: Kreisbewegung
sim5 = figur('sim5', 'Kreisbahn von oben: Körper mit Geschwindigkeitspfeil tangential und Zentripetalbeschleunigung zur Mitte', '0 0 300 280',
    '        <div class="reglerfeld">\n          '
    + regler('s5', 'r', '<i>r</i> Radius', 0.5, 5, 0.5, 4, 'm', 1) + '\n          '
    + regler('s5', 'T', '<i>T</i> Umlauf', 3, 12, 0.5, 4, 's', 1) + '\n          '
    + regler('s5', 'ph', '<i>φ</i> Ort', 0, 345, 15, 45, '°', 0) + '\n        </div>\n'
    + '        <p class="sim-notiz">Drehsinn gegen den Uhrzeigersinn. Pfeillängen proportional: \\(v\\) mit 8 px je m/s, \\(a_z\\) mit 4 px je m/s².</p>',
    'Radius')


def kreisbild():
    """Aufgabe 5d: Kreisbahn mit zwei Orten P und Q, ohne Pfeile."""
    import math
    cx, cy, R = 80, 75, 52
    t = [f'<svg class="mini" viewBox="0 0 160 150" role="img" aria-label="Kreisbahn mit Mittelpunkt M und zwei Orten P und Q, Drehsinn gegen den Uhrzeigersinn">',
         f'<circle cx="{cx}" cy="{cy}" r="{R}" class="bahn-kreis"/><circle cx="{cx}" cy="{cy}" r="2.5" class="knoten"/><text x="{cx + 5}" y="{cy + 13}" class="bt-text">M</text>']
    for n, w in (('P', 20), ('Q', 160)):
        x, y = cx + R * math.cos(math.radians(w)), cy - R * math.sin(math.radians(w))
        t.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" class="koerper"/><text x="{x + (8 if w < 90 else -8):.1f}" y="{y - 7:.1f}" text-anchor="{"start" if w < 90 else "end"}" class="mini-name">{n}</text>')
    t.append(f'<text x="{cx}" y="146" text-anchor="middle" class="bt-klein">Drehsinn: gegen den Uhrzeigersinn</text></svg>')
    return ''.join(t)


fest5 = r'''      <div class="tabhuelle">
        <table class="gesetze">
          <thead><tr><th>Grösse</th><th>Symbol</th><th>Definition</th><th>Einheit</th></tr></thead>
          <tbody>
            <tr><td>Umlaufzeit (Periode)</td><td>\(T\)</td><td class="wort">Zeit für einen Umlauf</td><td>s</td></tr>
            <tr><td>Rotationsfrequenz</td><td>\(f\)</td><td>\(f = \dfrac{1}{T}\)</td><td>Hz (1/s)</td></tr>
            <tr><td>Winkelgeschwindigkeit</td><td>\(\omega\)</td><td>\(\omega = \dfrac{2\pi}{T} = 2\pi \cdot f\)</td><td>rad/s</td></tr>
            <tr><td>Bahngeschwindigkeit</td><td>\(v\)</td><td>\(v = \omega \cdot r = \dfrac{2\pi \cdot r}{T}\)</td><td>m/s</td></tr>
            <tr><td>Zentripetalbeschleunigung</td><td>\(a_z\)</td><td>\(a_z = \dfrac{v^2}{r} = \omega^2 \cdot r\)</td><td>\(\text{m/s}^2\)</td></tr>
          </tbody>
        </table>
      </div>
      <div class="festhalten">
        <div class="merk"><div class="titel">Merke</div><p>Bei der gleichförmigen Kreisbewegung ist das Tempo \(|\vec v|\) konstant, aber die Richtung von \(\vec v\) ändert sich ständig: \(\vec v\) liegt tangential an der Bahn. Darum gibt es eine Beschleunigung, obwohl das Tempo gleich bleibt — die Zentripetalbeschleunigung \(\vec a_z\), die immer zur Kreismitte zeigt.</p></div>
        <div class="warn"><div class="titel">Häufiger Fehler</div><p>Umdrehungen pro Minute als Frequenz nehmen: \(120\) Umdrehungen pro Minute sind \(f = \dfrac{120}{60\;\text{s}} = 2\;\text{Hz}\), nicht \(120\;\text{Hz}\). Und \(\omega\) braucht den Faktor \(2\pi\): \(\omega = 2\pi \cdot 2\;\text{Hz} \approx 12.6\;\text{rad/s}\).</p></div>
      </div>'''
auf5 = test('t5', 'Aufgaben · Kapitel 5', 12, [
    ('5a', 3, r'Die Erde dreht sich in \(24\;\text{h}\) einmal um ihre Achse. Ein Punkt am Äquator ist \(6370\;\text{km}\) von der Achse entfernt. Berechne \(\omega\), \(v\) (in km/h) und \(a_z\).',
     r'<p>\(T = 24 \cdot 3600\;\text{s} = 86\,400\;\text{s}\), \(\omega = \dfrac{2\pi}{T} = \dfrac{2\pi}{86\,400\;\text{s}} \approx 7.27 \cdot 10^{-5}\;\text{rad/s}\).</p><p>\(v = \omega \cdot r\) \(= 7.272 \cdot 10^{-5}\;\text{rad/s} \cdot 6.37 \cdot 10^{6}\;\text{m}\) \(\approx 463\;\text{m/s} \approx 1670\;\text{km/h}\).</p><p>\(a_z = \omega^2 \cdot r \approx 0.0337\;\text{m/s}^2\) — klein gegen \(g\).</p>', ''),
    ('5b', 3, r'Eine CD dreht sich mit \(500\) Umdrehungen pro Minute. Wie gross sind Rotationsfrequenz, Winkelgeschwindigkeit und die Bahngeschwindigkeit am Rand (\(r = 6\;\text{cm}\))?',
     r'<p>\(f = \dfrac{500}{60\;\text{s}} \approx 8.33\;\text{Hz}\), \(\omega = 2\pi \cdot f \approx 52.4\;\text{rad/s}\).</p><p>\(v = \omega \cdot r\) \(= 52.36\;\text{rad/s} \cdot 0.06\;\text{m}\) \(\approx 3.14\;\text{m/s}\).</p>', ''),
    ('5c', 3, r'Ein Auto fährt mit \(54\;\text{km/h}\) durch eine Kurve mit \(r = 50\;\text{m}\). Wie gross ist die Zentripetalbeschleunigung? Wie viel Prozent von \(g\) ist das?',
     r'<p>\(v = \dfrac{54}{3.6}\;\text{m/s} = 15\;\text{m/s}\), \(a_z = \dfrac{v^2}{r} = \dfrac{(15\;\text{m/s})^2}{50\;\text{m}} = 4.5\;\text{m/s}^2\).</p><p>\(\dfrac{4.5\;\text{m/s}^2}{9.81\;\text{m/s}^2} \approx 0.459\), also rund \(46\;\%\) von \(g\).</p>', ''),
    ('5d', 3, r'Ein Körper läuft gleichförmig auf der Kreisbahn um. Zeichne bei P und bei Q den Pfeil \(\vec v\) und den Pfeil \(\vec a_z\) ein. Warum ist der Körper beschleunigt, obwohl sein Tempo konstant ist?',
     r'<p>\(\vec v\) liegt an beiden Orten tangential an der Bahn und zeigt in Drehrichtung (gegen den Uhrzeigersinn): bei P fast senkrecht nach oben, leicht nach links geneigt, bei Q fast senkrecht nach unten, ebenfalls leicht nach links. \(\vec a_z\) zeigt an beiden Orten zum Mittelpunkt M.</p><p>Die beiden Pfeile \(\vec v\) sind gleich lang, zeigen aber in verschiedene Richtungen. Eine Änderung der Richtung ist eine Änderung des Vektors \(\vec v\) — also eine Beschleunigung.</p>',
     '\n            <div class="mini-reihe">' + kreisbild() + '</div>'),
])
k5 = kapitel(5, 'kreisbewegung', 'Gleichförmige Kreisbewegung', 'K4 · K1', 40,
    r'Du bestimmst Umlaufzeit, Rotationsfrequenz, Winkelgeschwindigkeit, Bahngeschwindigkeit und Zentripetalbeschleunigung und erklärst, warum eine gleichförmige Kreisbewegung beschleunigt ist.',
    ('p4-1-lp-kreis', 'Bewegung sehen: Kreisbahn mit konstantem Tempo', '1:28'),
    sim5, ('p4-1-lp-kontrolle-kreis', 'Kontrollfragen zur Kreisbewegung', '0:38'),
    fest5, [uebung('umlauf', 'Frequenz und Winkelgeschwindigkeit'), uebung('bahn', 'Bahngeschwindigkeit und Zentripetalbeschleunigung'),
            uebung('zentripetal', 'Kurvenfahrt')],
    auf5, f'<a href="{TS}#kreisbewegung">Themenseite 4.1, Gleichförmige Kreisbewegung</a>')

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/kinematik/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz">4.1 · K1–K4</span><span class="zeit">≈ 25 min · 25 Punkte</span></div>
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
          <p>Aufgabe → Kapitel → Kompetenz: G1 → <a href="#k1">1</a>, <a href="#k2">2</a>, <a href="#k5">5</a> → K1 · G2 → <a href="#k1">1</a>, <a href="#k2">2</a> → K1, K3 · G3, G4 → <a href="#k3">3</a> → K3 · G5 → <a href="#k4">4</a> → K2 · G6 → <a href="#k5">5</a> → K4, K1</p>
        </div>
      </div>
    </section>'''

weiter = f'''
    <section class="kap weiter" id="weiter">
      <h2 id="weiter-titel">Nicht in diesem Leitprogramm</h2>
      <ul>
        <li>Momentangeschwindigkeit als Grenzwert (Sekante wird Tangente) → <a href="{TS}#definition">Themenseite 4.1, Grundbegriffe</a></li>
        <li>Herleitung der Bewegungsgleichungen aus der Fläche unter dem \\(v\\)-\\(t\\)-Diagramm → <a href="{TS}#theorie">Themenseite 4.1, Gleichmässig beschleunigte Bewegung</a></li>
        <li>Die drei Diagramme \\(a\\)-\\(t\\), \\(v\\)-\\(t\\) und \\(s\\)-\\(t\\) nebeneinander → <a href="{TS}#anim-gleichmaessig-beschleunigte">Themenseite 4.1, Animation 2</a></li>
        <li>Warum sich etwas bewegt: Kräfte und die newtonschen Gesetze → <a href="../themen/p4-2-dynamik.html">Themenseite 4.2 Dynamik</a></li>
      </ul>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Kinematik, Version 1.0 (04.10.2026), unverlinkt in Erprobung bis nach /lp-pruefung.
     Zweites Physik-Leitprogramm nach dem Kapitelmuster (HOWTO-leitprogramme.md §4): je Kapitel
     ① Einführungsclip → ② Simulation mit Aufgabenleiste → ③ Kontrollclip mit Fragen → Festhalten →
     ④ Übungen mit Rückmeldung → ⑤ Aufgaben mit Lösungen. Gesamttest und Bewertungspaket nur als PDF
     (downloads/leitprogramme/kinematik/*.tex). Quelle: scripts/lp/kinematik/seite.py.

     RLP-BM 2030, 7.5.4.1 Gruppe 1, Teilgebiet 4.1 (wörtlich wie im Kompetenzblock der Themenseite):
       K1 die Begriffe «Schwerpunkt», «Bahnkurve», «Geschwindigkeit» und «Beschleunigung» definieren
       K2 Die Geschwindigkeit in Vektor-Form darstellen und damit Relativbewegungen und absolute
          Bewegungen berechnen
       K3 Aufgabenstellungen zu folgenden Bewegungsarten lösen: Geradlinig gleichförmige Bewegung,
          gleichmässig beschleunigte Bewegung, freier Fall, parabolische Bewegung
       K4 die gleichförmige Kreisbewegung mit den dazugehörigen Grössen (Rotationsfrequenz,
          Winkelgeschwindigkeit, Zentripetalbeschleunigung) bestimmen und damit einfache Berechnungen
          durchführen

     Kompetenzmatrix (Hilfsmittel überall Taschenrechner und Formelsammlung):
       K1 → Kap. 1, 2, 5 · Aufg. 1a 1b 1d 5d · G1 G2 G6
       K2 → Kap. 4 · Aufg. 4a–4d · G5
       K3 → Kap. 1, 2, 3 · Aufg. 1b 1c 2a–2d 3a–3d · G2 G3 G4
       K4 → Kap. 5 · Aufg. 5a–5c · G6
     Bewusst weggelassen (RLP verlangt es nicht): Grenzwert Δt → 0 formal, Herleitung der zeitlosen
     Gleichung, Wurf mit Luftwiderstand, Kräfte — Verweise unter «Nicht in diesem Leitprogramm».
     Konventionen wie Themenseite 4.1: g = 9.81 m/s², ω in rad/s, β = Schwimmrichtung gegen die
     Strömung gemessen (90° = quer), γ = Driftwinkel mit tan γ = v_F / v_S. Die Themenseite nennt beim
     Vorhalten (Mini-Check Transfer) mit γ auch den Winkel gegen die Senkrechte; das Leitprogramm
     rechnet das Vorhalten darum allein mit β (v_S · cos β = −v_F).
     Zeiten: K0 10 · K1 40 · K2 40 · K3 45 · K4 40 · K5 40 · Gesamttest 25 = 240 min ≈ 5.3 Lektionen. -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Physik begreifbar · Leitprogramm</p>
      <h1>Kinematik</h1>
      <p class="unter">Ort, Geschwindigkeit, Beschleunigung, Fall und Wurf, Vektoren und Kreisbahn — zuschauen, tüfteln, kontrollieren, üben. Fünf Kapitel zu je rund einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Lerngebiet 4 · Teilgebiet 4.1</span>
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
    <ol><li><a href="#k1"><span class="nr">1</span><span>Ort und Geschwindigkeit</span></a></li></ol>
    <p class="lekt">Lektion 2</p>
    <ol><li><a href="#k2"><span class="nr">2</span><span>Beschleunigung</span></a></li></ol>
    <p class="lekt">Lektion 3</p>
    <ol><li><a href="#k3"><span class="nr">3</span><span>Fall und Wurf</span></a></li></ol>
    <p class="lekt">Lektion 4</p>
    <ol><li><a href="#k4"><span class="nr">4</span><span>Geschwindigkeit als Vektor</span></a></li></ol>
    <p class="lekt">Lektion 5</p>
    <ol><li><a href="#k5"><span class="nr">5</span><span>Kreisbewegung</span></a></li></ol>
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
          <li><b>② Tüfteln:</b> Aufgaben in der Animation lösen — sie zeigt ✓, wenn es stimmt.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Zahlen ohne Einheit, mit Punkt oder Komma; Brüche wie <code>1/2</code> und Zehnerpotenzen wie <code>2.4e-3</code> gehen auch. Richtig ist, was auf drei signifikante Stellen stimmt.</li>
          <li><b>⑤ Aufgaben</b> auf Papier, dann Lösung aufklappen und abhaken.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen nach Lehrplan</h2></summary>
        <p class="rlp-quelle">RLP-BM 2030, Lerngebiet 4, Teilgebiet 4.1 Kinematik</p>
        <ul>
          <li><b>K1</b> die Begriffe «Schwerpunkt», «Bahnkurve», «Geschwindigkeit» und «Beschleunigung» definieren</li>
          <li><b>K2</b> Die Geschwindigkeit in Vektor-Form darstellen und damit Relativbewegungen und absolute Bewegungen berechnen</li>
          <li><b>K3</b> Aufgabenstellungen zu folgenden Bewegungsarten lösen: Geradlinig gleichförmige Bewegung, gleichmässig beschleunigte Bewegung, freier Fall, parabolische Bewegung</li>
          <li><b>K4</b> die gleichförmige Kreisbewegung mit den dazugehörigen Grössen (Rotationsfrequenz, Winkelgeschwindigkeit, Zentripetalbeschleunigung) bestimmen und damit einfache Berechnungen durchführen</li>
        </ul>
        <p class="rlp-fuss">Die Themenseite <a href="''' + TS + '''">4.1 Kinematik</a> ist das Nachschlagewerk; dieses Leitprogramm ist der Kurs.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Kinematik · Clips von physik.begreifbar.ch</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''


def band(n, t):
    return f'\n    <div class="band"><span>{n if isinstance(n, str) else "Lektion " + str(n)}</span><span class="strich"></span><span>{t}</span></div>\n'


body = (oben + band('Vorbereitung', 'Vorwissen') + k0 + band(1, 'Bewegung') + k1 + band(2, 'Beschleunigung') + k2 + band(3, 'Fall und Wurf') + k3
        + band(4, 'Vektoren') + k4 + band(5, 'Kreisbahn') + k5 + band('Abschluss', 'Gesamttest') + gt + weiter + unten)
seite = KOPF + CSS + '</style>\n</head>\n<body>\n' + body + '\n' + BASIS + '\n' + open(SP + 'seite.js', encoding='utf-8').read() + '\n' + FUSS
open(ZIEL, 'w', encoding='utf-8').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
