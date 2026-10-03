# Bauskripte: Leitprogramm Elektrizität

Erstes Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4), gebaut nach
dem Mathe-Vorbild `tals-mathe/scripts/lp/quadratische-funktionen/`.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-elektrizitaet.html` — Kopf, CSS, Grundskript, alle Kapitel. Aus der bestehenden Seite übernimmt es nur den SEO-Block. | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: Koordinatensystem `Achsen()`, Bedienung (Regler und Knöpfe), Aufgabenleiste `Leiste()`, Simulationen sim1–sim5, Übungen mit Rückmeldung (`TYPEN`), Minigrafen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die zehn Drehbücher `clips/p6-2-lp-*.json` erzeugt; die Kontrollclips in Fassung 2 (nach der Prüfung vom 03.10.2026) | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt die gemessenen Dauern; mit Clipnamen dahinter nur diese). Spätere Korrekturen an den Einführungsclips stehen nur in den JSONs. |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/elektrizitaet/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py themen/p6-2-elektrizitaet.html
```

Änderungen **nur hier** machen, nicht direkt in der HTML-Datei — der nächste Lauf überschreibt sie.

Clips ändern: Drehbuch `clips/p6-2-lp-*.json` bearbeiten, dann `build-clip-ton.py` (wenn sich
Sprechertext oder Szenen ändern) → `build-clip-fragen-ton.py` (Kontrollclips) → `build-clips.py`
(Stimme `de_DE-thorsten-high`, siehe `CLAUDE.md`). Laufzeiten auf den Clipkarten in `seite.py`
nachführen. Die Bilder `clips/bilder/p6-2-lp-*.jpg` sind Aufnahmen der Simulationen
(`.claude/tools/aufnahme-anim.mjs`, Selektor `#simN > svg` — ohne `>` trifft man die
MathJax-Formel in der Aufgabenleiste; Knöpfe mit einer `js`-Aktion klicken, die Mausklicks
des Werkzeugs griffen hier nicht). Ändert sich eine Simulation, neu aufnehmen und **jedes Bild
ansehen**.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/elektrizitaet/*.tex`, bauen mit
`python3 scripts/build-lp-pdf.py elektrizitaet`.

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-elektrizitaet.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-elektrizitaet.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-elektrizitaet.html   # Formelsatz der Übungen
node .claude/tools/pruef-fragen.mjs p6-2-lp-kontrolle-ladung p6-2-lp-kontrolle-leistung \
     p6-2-lp-kontrolle-widerstand p6-2-lp-kontrolle-schaltungen p6-2-lp-kontrolle-gefahren
```

`seite.js` setzt die Testhaken `box.__aufgabe` und `box.__typ`; jeder Übungstyp liefert mit
`fehler(A)` seine typischen Fehleingaben samt Stichwort der erwarteten Rückmeldung. Ob jede
Aufgabe der Leisten **lösbar** ist, prüft `pruef-leiste` nicht — beim Bau am 03.10.2026 mit
einem Prüfskript gelöst, das jede Aufgabe mit den Zielwerten einstellt (alle 30 ✓).

## Abweichungen vom Mathe-Vorbild

- Klassen `sl-row`, `sl-grp`, `sl-val` und `frage` heissen hier `reglerfeld`, `regler`,
  `regler-wert` und `a-frage`: Physiks `style.css` belegt die ursprünglichen Namen
  (Regler der Themenseiten, blauer Verständnisfragen-Kasten) — HOWTO §12 Punkt 9.
- Toleranz der Übungen relativ (0.6 %, drei signifikante Stellen) statt exakt; Zufallswerte, bei
  denen ein typischer Fehler dasselbe Ergebnis gäbe (z. B. \(I = 1\;\text{A}\) beim Kehrwert),
  werden neu gewürfelt.
- Freigeschaltet am 03.10.2026 nach `/lp-pruefung`: Karte in `leitprogramme.html`, Kasten
  «Lieber geführt durcharbeiten?» oben auf der Themenseite 6.2, im Suchindex und in der Sitemap.
