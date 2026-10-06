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
| `anker.py` | legt `ein` jedes Elements mit `"_anker"` auf die Sprechzeit dieser Textstelle | nach jeder Neuvertonung eines Clips mit Ankern |
| `clips.py` | Archiv: hat die zehn Drehbücher `clips/p4-1-lp-*.json` erzeugt | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt die gemessenen Dauern). Die Einblendezeiten sind danach im JSON auf die Sprechzeiten gelegt worden (`sprechzeiten.py`). |

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
- **Kreis-Simulation** mit T ≥ 3 s und festem Pfeilmassstab (v 8 px je m/s, a_z 4 px je m/s²): So
  reicht a_z nie über die Mitte, und alle Pfeile bleiben im Bild (vorab mit python3 geprüft).
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
