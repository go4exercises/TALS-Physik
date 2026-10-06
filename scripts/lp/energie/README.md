# Bauskripte: Leitprogramm Energie

Viertes Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4), als Kopie von
`scripts/lp/dynamik/` entstanden (04.10.2026). Kopf, CSS, Grundskript, Bausteine und das Gerüst von
`seite.js` (Achsen, Bedienung, Aufgabenleiste, Uhr für die laufenden Simulationen, Übungsrahmen,
Minigrafen) sind wörtlich von dort; neu sind sechs Kapitel (RLP 4.3 hat sechs Kompetenzen),
sechs laufende Simulationen, 19 Übungstypen (seit 06.10.2026), zwölf Clips und Gesamttest.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-energie.html` — Kopf, CSS, Grundskript, alle Kapitel, Minigraf 2b. Die Laufzeiten der Clipkarten liest es aus den Drehbüchern. Aus der bestehenden Seite übernimmt es nur den SEO-Block. | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: sim1 Arbeit als Fläche (Kiste unter Winkel α), sim2 Bremsen und Energie-Parabel, sim3 Achterbahn mit Energiesäulen, sim4 Rampe mit Reibung und Motor (Energiebilanz als zwei gleich hohe Säulen), sim5 Kran mit Leistung und Wirkungsgrad, sim6 Energiebilanz der Erde (Temperaturverlauf über 30 Jahre); 19 Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die zwölf Drehbücher `clips/p4-3-lp-*.json` erzeugt | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt die gemessenen Dauern). Einblendezeiten im JSON auf die Sprechzeiten gelegt (`sprechzeiten.py`), lange Formeln dort in zwei Zeilen geteilt. |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/energie/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-energie.html
```

Änderungen **nur hier** machen, nicht in der HTML-Datei. Clips: Drehbuch `clips/p4-3-lp-*.json`
bearbeiten, dann `build-clip-ton.py` → `build-clip-fragen-ton.py` (Kontrollclips) →
`build-clips.py` (Stimme `de_DE-thorsten-high`), danach `seite.py`. Die Bilder
`clips/bilder/p4-3-lp-*.jpg` sind Aufnahmen der Simulationen (`.claude/tools/aufnahme-anim.mjs`).
Testhaken `document.getElementById('simN').__sim.zeige(…)`: sim3 setzt den Wagen an die Stelle
\(x\) (Tal \(x = 17\;\text{m}\), Kuppe \(x = 32\;\text{m}\)), sim5 zeigt den Kran nach \(x\) Sekunden
Hubzeit, sim6 lässt \(j\) Jahre laufen (`zeige(j, true)` ab heute, sonst ab der aktuellen Temperatur).
Damit entstehen die Bildfolgen der Clips (seit 06.10.2026); die übrigen Bilder sind Endzustände.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/energie/*.tex`, bauen mit
`python3 scripts/build-lp-pdf.py energie`.

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-energie.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-energie.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-energie.html
node .claude/tools/pruef-fragen.mjs p4-3-lp-kontrolle-arbeit p4-3-lp-kontrolle-bremsen p4-3-lp-kontrolle-erhaltung \
     p4-3-lp-kontrolle-reibung p4-3-lp-kontrolle-leistung p4-3-lp-kontrolle-erde
```

Lösbarkeit der Leisten mit einem Prüfskript (Fahrten über die Knöpfe, `reducedMotion: 'reduce'`):
alle 35 ✓, keine schon im Startzustand erfüllt. Die Achterbahn zusätzlich mit echter Bewegung
prüfen (Umkehr bei 7.6 m/s ohne ✓, Kuppe bei 7.7 m/s mit ✓, Halt nach dem Zurückrollen).

## Entscheide

- **Umfang nach RLP:** sechs Kompetenzen, sechs Kapitel (275 min). Spannenergie steht in keiner
  Kompetenz und bleibt auf der Themenseite, ebenso Wirkungsgrade in Serie.
- **Farben** wie Themenseite 4.3: Lageenergie Bernstein, Bewegungsenergie und v Grün, Wärme Rot,
  Kräfte und zugeführte Energie Blau, Kraftanteil in Wegrichtung und Arbeit-Fläche Violett.
  In den Clips (Theme `begreifbar-schlicht`, kein Blau und Violett): Lageenergie Bernstein (1),
  Arbeit und zugeführte Energie Orange (2), Bewegungsenergie, v und Nutzen eines Motors Grün (3),
  Wärme und Wärmestrahlung Rot (4), Kräfte und alles andere ungefärbt (5). Rot nur für Wärme.
- **Erde-Modell:** null-dimensional, \(C \cdot \tfrac{dT}{dt} = (1 - a) \cdot \tfrac{S}{4} - f \cdot \sigma \cdot T^4\)
  mit \(C = 4.2 \cdot 10^8\;\text{J/(m}^2\text{K)}\) (rund 100 m Ozean). \(f\) ist der Anteil der
  Wärmestrahlung der Oberfläche, der ins All gelangt — so beschreibt es die Themenseite
  (390 W/m² abgestrahlt, 238 W/m² gelangen hinaus, \(f \approx 0.61\)). Albedo heisst wie dort \(a\).
- **Achterbahn:** Bahn ohne flache Startplattform (Viertel-Sinus), sonst schleicht der Wagen oben;
  Massstab in beiden Richtungen 4.6 px je m.
- **Rampe:** Steht der Wagen und reicht der Antrieb nicht, fährt er nicht los; die Meldung nennt je
  nach Fall Hangabtrieb, Motor und Reibung richtig (bergauf wirkt der Hangabtrieb gegen den Motor).
- **Nach /lp-pruefung (05.10.2026)** behoben: Kuppe nur bei genug Energie, Halt nach der Umkehr,
  Leistenziele und Startwerte verschieden von den Clipbeispielen, Stefan-Boltzmann und \(P = F \cdot v\)
  in Clip und Festhalten, Diagramm-Aufgaben in allen Kapiteln ausser 2 (dort 2b), neue Aufgaben 6a–6c,
  Kontrollfragen ohne Doppelungen, Gesamttest mit Motor (G4) und Gründen der Erderwärmung (G6),
  30 min.
- **Freigeschaltet am 06.10.2026:** Karte in `leitprogramme.html` (Lerngebiet 4), Kasten «Lieber geführt
  durcharbeiten?» auf der Themenseite, im Suchindex und in der Sitemap.
- **Fassung 1.1 (06.10.2026)** nach der Befundliste der Prüfung:
  - Jeder Einführungsclip rechnet vor «Zum Mitnehmen» ein Problem vor (Problem → Vorgehen mit
    Strategiefrage → Lösung mit Probe): Kinderanhänger (Arbeit und kWh), Lieferwagen (Bremsweg),
    Bob (Energieerhaltung mit Anfangstempo), Schlitten (Reibungskraft aus der Bilanz), Bauaufzug
    (Leistung, Wirkungsgrad, kWh), Mars (Gleichgewichtstemperatur). Alle sechs neu vertont.
  - Ergebnisse in den Clipbildern erst mit dem Ton (Ebenen mit `_anker`); Steigungsdreieck mit
    Einheiten und stehende Gerade bis 20 s im Leistungsclip; Kranbilder vor «Wirkungsgrad» mit
    η = 1 aufgenommen (Testhaken: `max` des Reglers auf 1 gesetzt); Achterbahn ohne Rücksprung;
    Bildfolge «Hinaus» passend zum Ton; Δh statt h im Motor-Bild; Farben vereinheitlicht.
  - Kilowattstunde schon in Kapitel 1 (Festhalten, Clip); Übung `kwh` nur Umrechnen, E = P · t als
    neue Übung `pt` in Kapitel 5. Festhalten 6 mit Solarkonstante, Grund für S/4, idealem Strahler
    und Gleichgewichtstemperatur samt Tastenhinweis.
  - Jede Leistenaufgabe mit Notierauftrag und Vergleich; sim6 setzt für die Aufgaben «ab heute» die
    Temperatur zurück (`sim.heute()`), «ausgeglichen» heisst in Formelzeile und Leiste dasselbe
    (|Ein − Aus| < 0.1 W/m²), Startwerte a = 0.32, f = 0.63 (kein Leistenziel).
  - Aufgaben 1c (Dreieck im Kraft-Weg-Diagramm), 4a, 4c, 6a neu (nicht mehr gleich wie Kontrollfragen),
    6c mit Differenz und Faktor; Kontrollfragen arbeit F2, bremsen F2, leistung F5, erde F5 neu,
    überall zuerst der symbolische Ansatz.
  - Gesamttest Fassung 3: G2 (Trapez, Winkel rückwärts), G3 (Erhaltung und Bremsweg, Kapitel 2 und 3),
    G4 (Skilift, Reibung aus der Seilarbeit), G6d (zwei konkrete Änderungen der Erdbilanz, je 1 P);
    G2 3 P, G6 5 P. Bewertungspaket mit «ein Fehler, ein Abzug», gleichartigen Fehlern gleich
    bewertet, Zeilenabstand 1.5 in den Rastern.
  - Vortest-Clip: «Masse und Gewicht» (p0-3) statt der Hubarbeit-Animation.

