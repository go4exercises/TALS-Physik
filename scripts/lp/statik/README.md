# Bauskripte: Leitprogramm Statik

Fünftes Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4), als Kopie von
`scripts/lp/energie/` entstanden (05.10.2026). Kopf, CSS-Gerüst, Grundskript, Bausteine und das Gerüst von
`seite.js` (Achsen, Bedienung, Aufgabenleiste, Uhr für die laufenden Simulationen, Übungsrahmen,
Minigrafen) sind wörtlich von dort; neu sind sechs Kapitel, sechs laufende Simulationen, 18 Übungstypen,
zwölf Clips und Gesamttest.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-statik.html` — Kopf, CSS, Grundskript, alle Kapitel, Aufgabenbilder (`linien_bild`, `vek_bild` für Kraftpfeile im Gitter). Die Laufzeiten der Clipkarten liest es aus den Drehbüchern. Aus der bestehenden Seite übernimmt es nur den SEO-Block. | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: sim1 Kraft dreht sich (Komponenten und ihre Spur über φ), sim2 bis zu drei Kräfte am Ring Spitze an Fuss, Resultierende, Ring bewegt sich oder ruht, sim3 Rampe neigt sich (Gewicht, Normalkraft, Haftreibung, Kiste rutscht ab tan α > μ_H), sim4 Schraubenschlüssel (Kraft wächst, Schraube löst sich beim Losbrechmoment), sim5 Wippe loslassen (kippt oder bleibt), sim6 Wagen fährt über eine Brücke (Auflagerkräfte und ihre Spur); 18 Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die zwölf Drehbücher `clips/p4-4-lp-*.json` erzeugt | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt die gemessenen Dauern). Einblendezeiten im JSON auf die Sprechzeiten gelegt (`sprechzeiten.py`). |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/statik/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-statik.html
```

Änderungen **nur hier** machen, nicht in der HTML-Datei. Clips: Drehbuch `clips/p4-4-lp-*.json`
bearbeiten, dann `build-clip-ton.py` → `build-clip-fragen-ton.py` (Kontrollclips) →
`build-clips.py` (Stimme `de_DE-thorsten-high`), danach `seite.py`. Die Bilder
`clips/bilder/p4-4-lp-*.jpg` sind Aufnahmen der Simulationen (`.claude/tools/aufnahme-anim.mjs`).
Jede Simulation hat den Testhaken `document.getElementById('simN').__sim.zeige(x)`: sim1 Winkel φ,
sim2 Zeit im Ablauf (1.3 s: zweiter Pfeil angehängt, 2.6 s: Resultierende, 9: Ende), sim3 Neigung,
sim4 momentane Zugkraft, sim5 Kippwinkel in rad, sim6 Stelle des Wagens.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/statik/*.tex`, bauen mit
`python3 scripts/build-lp-pdf.py statik`.

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-statik.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-statik.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-statik.html
node .claude/tools/pruef-fragen.mjs p4-4-lp-kontrolle-vektor p4-4-lp-kontrolle-resultierende p4-4-lp-kontrolle-ruhe \
     p4-4-lp-kontrolle-drehmoment p4-4-lp-kontrolle-hebel p4-4-lp-kontrolle-auflager
```

Lösbarkeit der Leisten mit einem Prüfskript (Fahrten über die Knöpfe, `reducedMotion: 'reduce'`):
alle 29 ✓, keine schon im Startzustand erfüllt (die drei neuen Ziele der Fassung 1.1 einzeln nachgefahren).

## Entscheide

- **Umfang nach RLP:** fünf Kompetenzen, sechs Kapitel: K5 verlangt das Gleichgewicht
  «auf der horizontalen und schiefen Ebene» — die schiefe Ebene steht mit den Kräften am ruhenden
  Körper in Kapitel 3, das Momentengleichgewicht in Kapitel 5 (Hebel) und 6 (beide Bedingungen,
  Auflagerkräfte). Die allgemeinen Seilkraft-Formeln bei ungleichen Winkeln bleiben auf der Themenseite.
- **Zeit (Fassung 1.1):** je Kapitel rund 50 min — zwei Clips mit vorgerechnetem Problem (zusammen gut 3 min),
  Tüfteln 10, drei Übungen 10, vier Aufgaben auf Papier 20, Festhalten und Lesen 5. Mit Vorwissen (15) und
  Gesamttest (40) sind es 355 min ≈ 7.9 Lektionen, ohne beides 6.7 — über der Zielgrösse von HOWTO §3
  (Kapitelmuster bis 5 Lektionen). Bewusst nicht geteilt: Die sechs Kapitel bauen aufeinander auf
  (Komponenten → Resultierende → Kräfte am Körper; Drehmoment → Hebel → beide Bedingungen), und K5 braucht
  Kraft- *und* Momentengleichgewicht; ein zweites Leitprogramm «Drehmoment und Gleichgewicht» hätte keinen eigenen
  RLP-Teilgebietsbezug. Die frühere Angabe (40 min je Kapitel, 30 min Gesamttest) war geschätzt, nicht gemessen.
- **Winkelfunktionen:** stehen in keiner Vorwissensseite (der Link der Themenseite «Winkelfunktionen
  samt Bogenmass» zeigt auf 0.1 `#kreiszahl`, dort nur Bogenmass). Kapitel 0 bringt sie in einem Kasten.
- **Notation:** Resultierende \(F_\text{res}\) (Themenseite auch \(F_R\)), weil \(F_R\) hier die Reibung ist
  wie in Energie und auf der Themenseite (Tabelle «Die wesentlichen Kräfte»). Hangabtrieb \(F_H\),
  Haftreibungszahl \(\mu_H\), Auflagerkräfte \(F_A\), \(F_B\), Brücke: Last \(F_L\), Eigengewicht \(F_E\).
- **Farben** wie Themenseite 4.4: Seil-, Zug- und Einzelkräfte Blau, Gewichtskraft Bernstein, Normal-
  und Auflagerkraft Grün, Reibung Türkis (`--teal`), Komponenten und Hebelarm Violett, Resultierende Rot.
- **Kraftebenen wachsen mit:** sim1 und sim2 wählen das Fenster nach den Kräften (Vielfache von 25 N),
  sim3 und sim6 die Achse des Diagramms nach der Gewichtskraft bzw. der Gesamtlast; die Pfeile in sim3
  und sim6 sind im Massstab der Gewichtskraft bzw. Gesamtlast gezeichnet (Hinweis in der Formelzeile).
- **Gleichgewicht im Clip:** Auf dem Reglerraster (10 N, 5°) sind drei Kräfte im Gleichgewicht nur
  symmetrisch möglich (120° Abstand). Der Clip zeigt 3 × 80 N bei 90°, 210°, 330°, die Leiste fragt nach
  der dritten Kraft zu 100 N bei 0° und 120°.
- **Rutschen:** Nach dem Losrutschen wirkt in der Simulation eine Gleitreibung von 80 % der
  Haftreibungsgrenze; die Bewegung ist Stoff der Dynamik und wird nicht abgefragt.
- **Schraube lösen:** Schlüssel nach links, Kraft nach unten — er dreht gegen den Uhrzeigersinn, so löst
  man ein Rechtsgewinde.
- **Zufallswerte je Gegenstand** (Radmutter, Veloschraube, Handrad; Brechstange, Schubkarre, Kistenheber):
  Handkraft höchstens 450 N, Radkreuz höchstens 0.45 m — die Grenzen stehen im Generator (`rmax`, `Fmax`).
- **Clipfarben:** Das Theme `begreifbar-schlicht` hat nur fünf Farben (1 Bernstein, 2 Orange, 3 Grün, 4 Rot,
  5 Tinte); Blau, Violett und Türkis der Seite fehlen. In den gezeichneten Bildern gilt darum: Gewichtskraft
  Bernstein, Zug-, Hand- und Einzelkräfte sowie Haftreibung Orange, Normal- und Auflagerkraft Grün, Resultierende
  und «nötig»/Grenze Rot, Komponenten (auch der Hangabtrieb) und Hebelarme Tinte gestrichelt. Die Aufnahmen der
  Simulationen behalten die Seitenfarben.
- **Nach /lp-pruefung (05.10.2026)** behoben: Bezug im Ruhe-Clip (Hangabtrieb und grösste Haftreibung),
  Brechstange nicht mehr als einarmig genannt, Sim 3 setzt nach Reglerbewegung alles zurück, Sim 4 löst
  gegen den Uhrzeigersinn, Sim 6 rechnet ungerundet weiter, Rückmeldungen der Übungen «Winkel» und
  «Grenzwinkel», plausible Zufallswerte, Festhalten (+360°, waagrechter Boden, Eigengewicht, negative
  Auflagerkraft), Kontrollfragen ohne Wiederholung von Clip und Leiste, Ergebnisbilder erst nach der
  Rechnung, Gesamttest G2 bis G6 neu (Fassung 2).
- **Freigeschaltet am 06.10.2026:** Karte in `leitprogramme.html` (Lerngebiet 4), Kasten «Lieber geführt
  durcharbeiten?» auf der Themenseite, im Suchindex und in der Sitemap.

## Fassung 1.1 (06.10.2026)

Zweite Prüfung umgesetzt (Version 1.1, Fusszeile «Stand 6. Oktober 2026»):

- **Vorgerechnete Probleme** in allen sechs Einführungsclips (HOWTO §4, TODO-E), je «Problem / Vorgehen / Lösung»
  mit Strategiefrage «Dein Vorgehen»: Drachenschnur (−50 N; 70 N → 86.0 N, 125.5°), zwei Pferde (600 N und
  400 N unter 50° → 910 N, 19.7°), Sofa auf der Rampe (55 kg, 18°, μ_H = 0.42 → haftet, 166.7 N), Brandschutztür
  (40 N schräg unter 50°, 0.9 m → 27.6 Nm < 30 Nm), Schubkarre (90 kg, 0.35 m / 1.4 m → 220.7 N), Fussgängerbrücke
  (12 m, 30 kN, 24 kN bei 3 m → 33 kN und 21 kN).
- **Clips:** gleicher Massstab in Vektorbildern; Ergebnisse und Grenzen erst mit dem Ton; Bildfolge statt
  Endzustand (Gleichgewicht am Ring, Haftreibung); «Länger» neu gedacht (dieselben 120 N am doppelten Schlüssel
  geben die nötigen 60 Nm); Pfeile im Hebelbild im Verhältnis; Kontrollfragen ohne Unterstriche, mit neuen Werten
  (nicht Clip, Leiste, Mini-Check), jede falsche Antwort ein benannter Fehler, Ansatz in jeder Formelzeile;
  Last heisst überall F_L.
- **Simulationen:** sim1 mit mehr Luft über der Spitze (F, F_y, Achsenname getrennt); sim3 zeigt α mit einer
  Nachkommastelle und an der Grenze «tan α = μ_H erreicht», Testhaken `zeige(α, {ohneGrenze, grenze})`; sim4
  rechnet die Formelzeile mit den gezeigten Faktoren («≈» bei 231 N); sim5 ohne Bedienhinweis im Testbild und mit
  dem Hinweis oben statt auf den Hebelarmen; sim6 hält die Gesamtlast unter der Legende.
- **Leisten:** neue Aufgabe «zwei mögliche Richtungen» (sim1), «schräg am langen = senkrecht am kurzen Schlüssel»
  statt «α = 0°» (das zeigt der Clip, sim4), Vergleichsantworten in sim6, «ohne Eigengewicht» wo nötig.
- **Übungen:** Weiterrechnen mit F_B auf drei Stellen gilt (Auflager, Eigengewicht, zwei Lasten); Wertebereiche je
  Gegenstand; Leisten-, Fehlerkasten- und Aufgabenwerte ausgeschlossen; Lösungen mit symbolischem Ansatz und
  gleicher Rundung.
- **Seite:** Festhalten mit «zwei mögliche Richtungen», «Last an zwei Seilen» (2 · F_S · sin α = m · g) und
  «Schwerkraft» = Gewichtskraft; Vortest ohne noch unbekannte Formelzeichen; 1b, 1c, 2c (Skizze), 4b, 5b
  (zweiarmig), 5c (Gitterpunkte, Bernstein), 5d (Nussknacker statt der Leistenfrage), 6d (bis wohin darf der
  Maler?); Zeiten 50 min je Kapitel, Gesamttest 40 min.
- **Gesamttest Fassung 3** und Bewertungspaket: siehe Kopf von `gesamttest.tex`; «derselbe Fehler kostet nur
  einmal» und 2 % Rundung in Raster und Auftrag an die KI, Folgewerte vollständig, Raster mit Zeilenabstand.

## Clips nach der zweiten Visualisierungsprüfung (07.10.2026)

Gesagtes und Notiertes stehen jetzt zur selben Zeit im Bild, Veränderungen laufen als Bildfolge oder Läufer,
Pfeile gleicher Grösse im gleichen Massstab, Ergebnisse erst mit dem Ton. Entscheide:
- drehmoment, Szene 2: gezeichnet statt aufgenommen — der Längenregler reicht bis 0.4 m, ein 0.5-m-Schlüssel
  läge links ausserhalb der Simulation.
- auflager, Szene 4: Die Beschriftung des Läufers von B steht bis 2 m über der Geraden, weil er dort auf einer
  `parabel` mit winzigem negativem a fährt (Abweichung höchstens 0.00025 kN) — Kunstgriff, solange der
  Generator keine Lage der Läuferbeschriftung kennt.
- vektor S1, drehmoment S2, auflager S2: `ein` von Hand nach `sprechzeiten.py`; `anker.py` lag bis 1.5 s daneben.
- auflager, Szene 7: F_B, F_A und Probe erscheinen mit dem gesprochenen Ergebnis.
