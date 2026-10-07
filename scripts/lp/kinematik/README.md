# Bauskripte: Leitprogramm Kinematik

Zweites Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4), als Kopie von
`scripts/lp/elektrizitaet/` entstanden (04.10.2026). Kopf, CSS, Grundskript, Bausteine und das
Gerüst von `seite.js` (Achsen, Bedienung, Aufgabenleiste mit Vergleichsantwort, Übungsrahmen)
sind wörtlich von dort; neu sind Kapitel, Simulationen, Übungstypen und Clips.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-kinematik.html` — Kopf, CSS, Grundskript, alle Kapitel, die zwei Aufgabenbilder (Wurf, Kreis). Aus der bestehenden Seite übernimmt es nur den SEO-Block. | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: Simulationen sim1–sim5 (s-t, v-t mit Fläche, Wurfbahn 1:1, Fluss 1:1, Kreisbahn), 15 Übungstypen (`TYPEN`, je mit `fehler()`), Minigrafen mit Geraden `m` oder `m,q` | wird von `seite.py` eingesetzt |
| `antworten.py` | trägt die Antwortbilder der fünf Kontrollclips in die Drehbücher ein (Kennung `"antwort": true`, wiederholbar) | bei Änderungen an einer Kontrollfrage, danach `build-clips.py` |
| `anker.py` | legt `ein` jedes Elements mit `"_anker"` auf die Sprechzeit dieser Textstelle; `"_versatz"` legt es so viele Sekunden später (Bildfolgen), und in einer Frageszene erscheinen Text und Formeln erst nach der Frage — gilt für alle sechs Leitprogramme | nach jeder Neuvertonung eines Clips mit Ankern |
| `clips.py` | **Archiv, nicht mehr laufen lassen.** Hat am 04.10.2026 die zehn Drehbücher `clips/p4-1-lp-*.json` erzeugt; seither sind sie weit darüber hinaus bearbeitet (Visualisierung, Problem-Szenen, neue Kontrollfragen) | **nein, nie** — die JSONs sind die Quelle; `--neu` überschriebe alle späteren Änderungen und die gemessenen Dauern. Änderungen nur im JSON, danach `anker.py` und `build-clips.py`. |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/kinematik/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-kinematik.html
```

Änderungen **nur hier** machen, nicht direkt in der HTML-Datei — der nächste Lauf überschreibt sie.

Clips ändern: Drehbuch `clips/p4-1-lp-*.json` bearbeiten, dann `build-clip-ton.py` (Sprechertext
geändert) → `build-clip-fragen-ton.py` (Kontrollclips) → `build-clips.py` (Stimme
`de_DE-thorsten-high`). Laufzeiten auf den Clipkarten in `seite.py` nachführen. Die Bilder
`clips/bilder/p4-1-lp-*.jpg` sind Aufnahmen der Simulationen (`.claude/tools/aufnahme-anim.mjs`,
Selektor `#simN > svg`, Regler per `js`-Aktion setzen). Ändert sich eine Simulation: neu aufnehmen
und jedes Bild ansehen.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/kinematik/*.tex`, bauen mit
`python3 scripts/build-lp-pdf.py kinematik`. Das Bewertungspaket folgt der Elektrizitäts-Fassung
1.1: Folgefehler überall gleich, Begründungspunkte (B) ohne Formelpflicht.

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-kinematik.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-kinematik.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-kinematik.html
node .claude/tools/pruef-fragen.mjs p4-1-lp-kontrolle-gleichfoermig p4-1-lp-kontrolle-beschleunigt \
     p4-1-lp-kontrolle-wurf p4-1-lp-kontrolle-vektor p4-1-lp-kontrolle-kreis
```

Ob jede Aufgabe der Leisten **lösbar** ist, prüft `pruef-leiste` nicht — beim Bau am 04.10.2026
mit einem Prüfskript gelöst, das jede Aufgabe mit den Zielwerten einstellt (alle 30 ✓).

## Entscheide

- **Farben** wie Themenseite 4.1 (STYLEGUIDE §5.2): s Bernstein, v Grün, Komponenten Violett,
  a_z und Resultierende Rot. Das Clip-Theme kennt kein Violett: Beschleunigung und v_F bleiben in
  den Clips ungefärbt, statt eine Farbe mit anderer Bedeutung zu tragen.
- **Vorhalten** nur mit β (v_S · cos β = −v_F): Die Themenseite benutzt γ für den Driftwinkel und
  im Mini-Check auch für den Winkel gegen die Senkrechte.
- **Kreis-Simulation** mit r ≥ 1 m, T ≥ 3 s und festem Pfeilmassstab (v 8 px je m/s, a_z 3 px je m/s²),
  beide Pfeile ab dem Rand des Körpers und streng proportional: So reicht a_z nie über die Mitte
  (6 + 3 · (2π/T)² · r ≤ 20 · r), und alle Pfeile bleiben im Bild (vorab mit python3 geprüft). Bis
  06.10.2026 war a_z mit 4 px je m/s² nur durch Abschneiden an der Mitte zu halten — nicht proportional.
- **Startwerte der Simulationen** sind weder ein Clipbeispiel noch ein Leistenziel (sim1 6 m/s, 15 m,
  4 s; sim2 5 m/s, 1 m/s², 7 s; sim3 6 m/s, 30°, 10 m; sim4 1.5 m/s, 90°, 0.75 m/s; sim5 2.5 m, 7 s,
  60°). Die Clipbilder setzen ihre Werte in den Aufnahmeplänen ausdrücklich.
- **Freigeschaltet am 04.10.2026** nach `/lp-pruefung` (Befunde behoben): Karte in
  `leitprogramme.html` (Lerngebiet 4), Kasten «Lieber geführt durcharbeiten?» auf Themenseite 4.1,
  im Suchindex und in der Sitemap.

## Rückmeldung des Auftraggebers (06.10.2026)

- **Kapitel 3 und 4 getauscht:** zuerst die Überlagerung zweier gleichförmiger Bewegungen (Vektoren),
  dann die mit einer beschleunigten (Fall und Wurf). Sichtbar sind Nummern, Anker `#k3`/`#k4`,
  Aufgabenbezeichnungen und Reihenfolge geändert; **intern bleiben `sim3`, `s3-*`, `t3` beim Wurf und
  `sim4`, `s4-*`, `t4` bei den Vektoren**, weil der gespeicherte Fortschritt (`KEY`) an den
  Test-Kennungen hängt. Gesamttest: Teile in der neuen Folge, G3 Fähre, G4 Mauer, G5 Schuss.
- **Senkrechter Wurf** nach oben und unten im Wurfkapitel: Clipszenen «Nach oben» (12 m/s, 1.22 s,
  7.3 m) und «Nach unten» (aus 20 m mit 10 m/s, 1.24 s), Festhalten mit \(t_S\) und \(h_\text{max}\),
  sim3 mit \(\alpha\) von −90° bis 90° (senkrecht: Auf- und Abweg nebeneinander gezeichnet, mit Notiz),
  zwei Leistenaufgaben, Übungstyp `senkrecht`, Aufgabe 4b, Kontrollfrage 5, Gesamttest G5.
- **«Tempo» → Geschwindigkeit bzw. Betrag** in Seite, Clips und PDFs (STYLEGUIDE §2.2).
- **(t; s)** an den bewegten Punkten von sim1 und sim2; Steigungsdreieck in sim2 ab dem Punkt nach rechts.
- **Denkaufträge** in den Leisten (sim1 6, sim2 3, 5, 6) mit Vergleichsantworten.
- **Beschleunigungs-Clip:** Steigungsdreieck mit Δv und Δt im Diagramm, Einheit als (m/s)/s; die Wege
  (Dreieck, Trapez = Rechteck + Dreieck, Bremsweg, doppelte Geschwindigkeit) entwickeln sich im
  Diagramm statt als Simulationsbild.
- **Antworten der Kontrollclips im Bild** (`antworten.py`).

## Fassung 1.1 (06.10.2026) — nach der zweiten Prüfung

- **Einführungsclips mit vorgerechnetem Problem** (HOWTO §4): je drei Szenen «Problem / Vorgehen /
  Lösung» vor «Zum Mitnehmen», mit Strategiefrage «Dein Vorgehen» — Kreuzung (s₀ = −300 m), Hang
  (1.25 m/s², 26 m), Steg (36 m Versatz → 0.6 m/s), Golfball (20 m/s, 35°, 38.3 m), Salatschleuder
  (720 U/min, 682 m/s²). Clipkarten 2:10 bis 3:03.
- **Kontrollfragen** mit neuen Beispielen (Kreis F2 0.25 s, F3 Δv-Skizze; Wurf F2 7 m → 28 m;
  gleichförmig F5 12 m/s; beschleunigt F1 8 → 20 m/s), Antwortpunkte erst nach der Bewegung, F3 Wurf
  ohne verratene Landung. Clipbilder: Ergebnisse erst, wenn gesagt; Massstab 1:1 bei Wurf und Fluss;
  Steigungsdreiecke mit Einheiten; Farben nach den Entscheiden oben.
- **Simulationen:** Startwerte weder Clip noch Leiste; Punktbeschriftung gerundet wie die Formelzeile;
  Formelzeilen rechnen mit Eingaben oder schreiben «≈» vor gerundet eingesetzte Werte; sim5 mit
  proportionalen Pfeilen ab dem Körperrand (a_z 3 px je m/s², r ≥ 1 m); sim4-Regler «Boot».
- **Aufgabenleisten:** jede Aufgabe mit Denkauftrag und Vergleichsantwort; neue Werte, wo eine Aufgabe
  einer Kontrollfrage, Kapitelaufgabe oder Themenseite glich (Bus 27 km/h, Roller 3.5 m/s², Wurf aus
  25 m, Kreis T = 5 s / 10 s, v ≈ 2.09 m/s); statt «45° am weitesten» (sagt der Clip) der beste Winkel
  von 20 m Höhe (30°).
- **Übungen:** feste Beispiele ausgeschlossen, tote Ausschlüsse entfernt, Zusammenfälle (Δv = 1,
  v = 1 m/s, h = 5 m) ausgeschlossen, Schwimmerin höchstens 2 m/s, |a| ≤ 6 m/s²; Weiterrechnen mit auf
  drei Stellen gerundeten Zwischenwerten zählt (geprüft mit je 400 Fällen).
- **Seite:** Festhalten Kap. 1 «Ortsänderung pro Zeit», Kap. 3 Driftwinkel gegenüber der Querrichtung,
  Kap. 4 Fallweg und Höhe getrennt (nach unten / nach oben gemessen); Doppelungen entflochten
  (Vortest 80 U/min, Fehlerkästen 108 km/h, 2.4/0.7 m/s, 45 m, 180 U/min; Aufgaben 3c mit 3 m/s
  Strömung, 4d 16 m/s unter 40°); Kapitel 4 55 min; Zuordnung G1 → Kapitel 1, 2, 4.
- **Gesamttest Fassung 4 / Bewertungspaket:** G1 ohne Tacho-Frage (= 1b), dafür Geschwindigkeit
  definieren; G2 mit Sekunden-Nebengitter; G3 mit Richtung «flussaufwärts», c rückwärts (bis 2.0 m/s
  Strömung), d Relativbewegung auf einer Geraden (0.4 m/s, 750 s); G5 senkrechter Wurf nach unten,
  rückwärts (5.27 m/s, 17.0 m); G6 mit 2.8 m/s (T = 0.785 s). Raster: «ein Fehler, ein Abzug» auch über
  Teilaufgaben, Folgewerte der typischen Fehler, mehr Zeilenabstand, Flattersatz.

## Clips nach der zweiten Visualisierungsprüfung (07.10.2026)

Gesagtes und Notiertes stehen jetzt zur selben Zeit im Bild, Veränderungen laufen als Bildfolge oder Läufer,
Pfeile gleicher Grösse im gleichen Massstab, Ergebnisse erst mit dem Ton. Entscheide:
- kreis: Umlauf als Bildfolge in Echtzeit (`p4-1-lp-kreis-o000` … `o315` ohne Pfeile, `v045` … `v315` nur mit v);
  die Pfeile entfernt nur der Aufnahmeplan per JS, `seite.js` ist unverändert. `p4-1-lp-kreis-1.jpg` gelöscht
  (doppelt mit `w045`); `clips.py` nennt den Namen noch — Archiv.
- vektor, Szene 4: β-Bogen bewusst klein (r ≈ 20 px), sonst schneidet er die Beschriftung «v_Ufer» der Simulation.
- Zwei Zeitpunkte der Befundliste waren falsch zugeordnet (vektor «β: von der Strömung aus», wurf «45°: 22.9 m»)
  und blieben; korrigiert wurde stattdessen die Formel für \(s_x\).
