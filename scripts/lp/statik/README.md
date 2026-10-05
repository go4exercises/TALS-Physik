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
alle 28 ✓, keine schon im Startzustand erfüllt.

## Entscheide

- **Umfang nach RLP:** fünf Kompetenzen, sechs Kapitel (285 min): K5 verlangt das Gleichgewicht
  «auf der horizontalen und schiefen Ebene» — die schiefe Ebene steht mit den Kräften am ruhenden
  Körper in Kapitel 3, das Momentengleichgewicht in Kapitel 5 (Hebel) und 6 (beide Bedingungen,
  Auflagerkräfte). Die allgemeinen Seilkraft-Formeln bei ungleichen Winkeln bleiben auf der Themenseite.
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
