# Bauskripte: Leitprogramm Hydrostatik

Sechstes Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4), als Kopie von
`scripts/lp/statik/` entstanden (05.10.2026). Kopf, CSS-Gerüst, Grundskript, Bausteine und das Gerüst von
`seite.js` (Achsen, Bedienung, Aufgabenleiste, Uhr für die laufenden Simulationen, Übungsrahmen,
Minigrafen) sind wörtlich von dort; neu sind sechs Kapitel, sechs laufende Simulationen, 18 Übungstypen,
zwölf Clips und Gesamttest.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-hydrostatik.html` — Kopf, CSS, Grundskript, alle Kapitel, Aufgabenbilder. Die Laufzeiten der Clipkarten liest es aus den Drehbüchern. Aus der bestehenden Seite übernimmt es nur den SEO-Block. | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: sim1 Person sinkt in den Schnee ein (Druck über der Fläche), sim2 Taucherin mit Manometer (Druck über der Tiefe), sim3 Saugrohr: der Luftdruck drückt Wasser oder Quecksilber hoch, sim4 hydraulische Hebebühne mit fünf Pumpstössen, sim5 Körper an der Federwaage wird eingetaucht (Anzeige und Auftrieb über der Eintauchtiefe), sim6 Würfel pendelt sich ein, schwebt oder sinkt (Eintauchtiefe über der Zeit); 18 Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die zwölf Drehbücher `clips/p4-5-lp-*.json` erzeugt | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt die gemessenen Dauern). Einblendezeiten im JSON auf die Sprechzeiten gelegt; Bilder mit Ergebnissen erscheinen erst, wenn der Ton das Ergebnis sagt. |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/hydrostatik/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-hydrostatik.html
```

Änderungen **nur hier** machen, nicht in der HTML-Datei. Clips: Drehbuch `clips/p4-5-lp-*.json`
bearbeiten, dann `build-clip-ton.py` → `build-clip-fragen-ton.py` (Kontrollclips) →
`build-clips.py` (Stimme `de_DE-thorsten-high`), danach `seite.py`. Die Bilder
`clips/bilder/p4-5-lp-*.jpg` sind Aufnahmen der Simulationen (`.claude/tools/aufnahme-anim.mjs`).
Jede Simulation hat den Testhaken `document.getElementById('simN').__sim.zeige(x)`: sim1 Fortschritt 0 bis 1,
sim2 Tiefe, sim3 Innendruck in hPa, sim4 Pumpstösse 0 bis 5, sim5 Eintauchtiefe in cm, sim6 ohne Zahl den
ganzen Lauf bis zum Endzustand, mit Zahl den Zustand nach so vielen Sekunden (Bildfolge Schwimmen/Sinken).

Gesamttest und Bewertungspaket: `downloads/leitprogramme/hydrostatik/*.tex`, bauen mit
`python3 scripts/build-lp-pdf.py hydrostatik`.

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-hydrostatik.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-hydrostatik.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-hydrostatik.html
node .claude/tools/pruef-fragen.mjs p4-5-lp-kontrolle-druck p4-5-lp-kontrolle-schweredruck p4-5-lp-kontrolle-luftdruck \
     p4-5-lp-kontrolle-pascal p4-5-lp-kontrolle-auftrieb p4-5-lp-kontrolle-schwimmen
```

Lösbarkeit der Leisten mit einem Prüfskript (Fahrten über die Knöpfe, `reducedMotion: 'reduce'`):
alle Leisten lösbar, keine schon im Startzustand erfüllt (Stand nach der Behebung).

## Entscheide

- **Umfang nach RLP:** fünf Kompetenzen, sechs Kapitel (370 min, je Kapitel 55 min): K3 verlangt den Druck in der Flüssigkeit
  *und* die Verbindung zum Luftdruck — Schweredruck (Kapitel 2) und Luftdruck mit Saugrohr und Barometer
  (Kapitel 3); K5 Auftrieb (Kapitel 5) und Schwimmen, Schweben, Sinken (Kapitel 6). Das U-Rohr mit zwei
  Flüssigkeiten steht in keiner Kompetenz und bleibt auf der Themenseite.
- **Vorwissen:** Dichte und Druckeinheiten stehen im Leitprogramm «Grössen, Messen, Druck»; Kapitel 0 und
  Kapitel 1 verweisen dorthin, Kapitel 1 vertieft den Druck zwischen Festkörpern.
- **Notation** wie Themenseite 4.5: \(p\), \(p_S\), \(p_0\), \(F_A\) (Auftrieb), \(V_e\), \(\rho_K\), \(\rho_{Fl}\),
  \(F_1, A_1, s_1\) und \(F_2, A_2, s_2\) an der Presse, \(p_i\) Innendruck im Saugrohr.
- **Farben (Farbe = eine Bedeutung, Fassung 1.1):**

  | Bedeutung | Leitprogramm (SVG) | Clips (Theme ohne Blau und Violett) |
  |---|---|---|
  | Gewichtskraft (sonst nichts in Bernstein) | Bernstein | 1 Bernstein |
  | Auftrieb | Grün | 3 Grün |
  | Druck und die Kräfte, die er an Kolben ausübt | Blau | 4 Rot |
  | Anzeige der Federwaage | Tinte | 5 Tinte |
  | Tiefen, Höhen, Wege | Violett | 2 Orange |
  | Luftdruck, Gefässe, Flüssigkeiten, Körper (Holz hellgrau-beige, Metall grau) | Grau | 5 Tinte |

  Die Themenseite 4.5 zeichnet die Gewichtskraft rot.
- **Luftdruck der Orte:** Mittelwerte aus \(p = 1013\;\text{hPa} \cdot e^{-h/8400\;\text{m}}\): Zürich 965, Davos 841,
  Jungfraujoch 671 hPa.
- **Schneemodell** (sim1): Eindrucktiefe \(d = 40\;\text{cm} \cdot \dfrac{p}{p + 10\;\text{kPa}}\), nur zur Anschauung;
  abgefragt wird nur der Druck.
- **Würfel** (sim6): gedämpfte Bewegung aus Gewichtskraft und Auftrieb, Dämpfung \(6\;\text{s}^{-1}\), ohne
  mitbewegtes Wasser; abgefragt werden nur Endzustände.

## Nach /lp-pruefung (05.10.2026)

- **Clipbeispiele auf dem Reglerraster:** Der Druck-Clip rechnet mit \(55\;\text{kg}\) auf \(250\;\text{cm}^2\) und
  Schneeschuhen von \(1500\;\text{cm}^2\) — Werte, die sim1 genau einstellt; die Bilder sind Aufnahmen davon.
- **Kontrollfragen:** Jeder falsche Wert entsteht aus einem benannten Fehler, und die Rückmeldung nennt ihn.
  Fragen, die ein Leistenziel oder einen Festhalten-Kasten vorwegnahmen, sind ersetzt (Heizöltank,
  Meerwasser, Barometer steigt, Pascal'sche Kugel, Kraft am kleinen Kolben, Spiritus, Druck an der Unterseite,
  Dichte aus dem Anteil).
- **sim6** meldet den Endzustand des Laufs (nahe der Schwebedichte steigt oder sinkt der Würfel nach 10 s
  noch), nicht das Ergebnis des Dichtevergleichs.
- **Gesamttest:** G1 am Diagramm (ablesen, rückwärts, begründen), G3 Pascals Fassversuch für das
  hydrostatische Paradoxon (Kapitel 2), G4 Wagenheber rückwärts, G6 Aräometer. Kapitel 3 steckt im Luftdruck
  von G2. Raster: derselbe Fehler in mehreren Teilaufgaben kostet einen Punkt.
- **Statik** trug Speicherschlüssel und Fusszeile von Energie; mit dieser Behebung korrigiert.
- **Freigeschaltet am 06.10.2026:** Karte in `leitprogramme.html` (Lerngebiet 4), Kasten «Lieber geführt
  durcharbeiten?» auf der Themenseite, im Suchindex und in der Sitemap.

## Fassung 1.1 (06.10.2026)

Behebung der Prüfbefunde (Version 1.1, Fusszeile «Stand 6. Oktober 2026»):

- **Einführungsclips** mit vorgerechnetem Problem (Problem, Vorgehen mit Strategiefrage, Lösung mit Probe):
  Kiste auf vier Füssen, Wasserturm, Brunnen in Chur, Holzspalter, Stein im Überlaufgefäss, Eichenbalken im Meer.
  Dazu: Bilder ohne vorweggenommene Ergebnisse (Einsinken, Becken ohne Gesamtdruck, Waage und kleiner Kolben
  erst ohne Wert), Taucherin, Luftsäulen und Druckpfeile ergänzt, Barometer im gemeinsamen Massstab,
  Kolbenwege als Skizze mit s₁ und s₂, Gesamtdruck mit Steigungsdreieck in Einheiten, Text «sinkt ein Stück ein».
- **Kontrollclips:** Luftdruck mit neuen Fällen (Saugnapf, Wasserbarometer auf dem Säntis, Höhenmesser,
  Spiritus im Saugrohr); Diesel statt Heizöl; neues Auto an der Presse (11 000 N, 88 N); jeder Distraktor ein
  benannter Fehler, Rückmeldungen ohne Rechenweg; «nicht massstäblich» an den Pressebildern.
- **Simulationen:** sim3 Regler in 5 hPa, sim6 in 25 kg/m³ (alle Leistenziele auf dem Raster); sim2 neu skaliert,
  Legende unter dem Diagramm; sim4 Gewichtskraftpfeil höchstens 110 px mit Bruchzeichen; sim5 Kräfte auf 0.01 N,
  Etiketten bei tiefem Eintauchen nicht mehr abgeschnitten; sim6 Formelzeile nach dem Dichtevergleich.
- **Leisten** mit Denkauftrag; Ziele, die Kapitelaufgaben wiederholten, ersetzt (sim1: 3000 cm², 2.5 kPa;
  sim2: 24 m; sim3: mindestens 6 m; sim6: Fichte 450, Kerzenwachs 900).
- **Übungen:** feste Beispiele über `FEST`/`istFest()` ausgeschlossen; Auftrieb in Luft (Ballon); mittlere Dichte
  mit Auswahl «schwimmt/sinkt», Sandsack statt Tauchgewicht.
- **Seite:** ρ_Fl statt ρ_W, Quaderhöhe H, Festhalten 2 und 4 präzisiert, Kleinigkeiten in 1b, 2b, 3b, 5a;
  Kapitel 3 verweist auf den neuen Abschnitt «Luftdruck: Saugrohr und Barometer» der Themenseite.
- **Gesamttest:** G1 zwei Kurven, G2 mit Saughöhe (Kapitel 3), G4c Ölmenge und Arbeit, G5 Auftrieb in Luft,
  Federwaage unter Wasser und Druckunterschied, G6 mit Dichtevergleich; Raster mit Folgewerten, Zeilenabstand 1.5.
