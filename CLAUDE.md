# CLAUDE.md — TALS Physik

Statisches HTML/CSS/JS-Lehrmittel für die BM (RLP-BM 2030), gehostet via GitHub Pages.
Schwester-Projekt zu TALS Mathe. Diese Datei ist die lokale Claude-Code-Variante der
COLLABORATION.md — sie ersetzt den alten ZIP-Workflow durch einen Git-Workflow.

**Autoritative Detail-Konventionen stehen in `STYLEGUIDE.md` (im Repo). Diese Datei
ist die Kurzfassung + der verbindliche Pre-Flight. Bei Widerspruch gilt STYLEGUIDE.md.**

## Sprache & Notation (nicht verhandelbar)

- Schweizer Hochdeutsch. **Kein ß** — immer „dass", „muss", „Schluss".
- **Dezimaltrennzeichen ist der Punkt, nie das Komma** — überall: LaTeX (`9.81`, nicht
  `9{,}81`), Aufgabentexte, Live-Anzeigen, JS-Code.
- MathJax-Delimiter: `\(…\)` inline, `\[…\]` abgesetzt. Niemals `$…$`.
- Formeln immer in LaTeX. Symbole/Einheiten nach SI (STYLEGUIDE §2).
- Bernstein/Amber als Leitfarbe (`#8A4A0E`); Blau gehört zu Mathe, nicht hierher.
- Register: **du** in Aufgaben, **unpersönlich** in der Theorie. Kein förmliches „Sie".

## Projektstruktur

- `themen/` — 10 Themenseiten: `p4-1`…`p4-5` (Mechanik), `p5-1`…`p5-3` (Thermo),
  `p6-1`,`p6-2` (Wellen/Elektrizität). Alle inhaltlich fertig und auditiert.
- `physiklib.js` — Canvas-Bibliothek + globale Helfer (`toggleL`, `fmt`, `initCanvas`,
  `drawGrid`, `drawAxesUnits`, `drawArrow`, `drawVector`, `drawDot`, …).
- `minicheck.js` — Akkordeon-Logik der Mini-Checks. `anim-hinweise.js` — Hinweis-Logik.
- `nav.js` — Navigation (`buildNav`). `style.css` — gesamtes Design.
- Pilot-/Referenzseite für jedes Skelett: `themen/p4-1-kinematik.html`.

## Inhaltliche Regeln

- **Ansatz-Prinzip:** Jede Lösung beginnt mit einer benannten Formel / symbolischem
  Ansatz, *dann* erst werden Werte eingesetzt. Keine Inline-`⇒`-Ketten — mehrstufige
  Algebra auf getrennte Display-Zeilen.
- **Einheitenumrechnungen** beim ersten Vorkommen pro Seite voll ausschreiben.
- **Verständnisfragen (❓)** stehen am *Ende* des Abschnitts, der den Stoff behandelt,
  direkt vor dem Mini-Check — nicht einen Abschnitt zu früh.
- Diagramm-Achsen tragen IMMER Einheiten. Nur x-y-Vektordiagramme sind 1:1 isometrisch.

## Skelett & Klassen — kopieren, nicht erfinden

- Neue Seite / neuer Block: Skelett aus `themen/p4-1-kinematik.html` (oder `TEMPLATE.html`)
  **1:1 kopieren**, nur Inhalt anpassen. CSS und `nav.js` sind auf die *exakten*
  Klassennamen ausgerichtet.
- **Niemals eigene Klassennamen, Container-Hierarchien oder API-Signaturen erfinden.**
  „Klingt vernünftig" reicht nicht — erfundene Klassen fallen still auf Block-Default
  zurück (Karten werden zu Listen, Sidebar überlappt).
- Jede Seite, die `onclick="toggleL(…)"` o.ä. nutzt, **muss `physiklib.js` einbinden**.
  Mit `.anim-hinweis`-Markup → `anim-hinweise.js`. Mit `.minicheck`-Markup → `minicheck.js`.

## Pre-Flight (verbindlich vor jedem Commit)

Nach jeder Änderung an Themenseiten, **bevor** committet wird:

```bash
python3 .claude/skills/preflight/preflight.py themen/<geänderte_datei>.html
# oder über alle: python3 .claude/skills/preflight/preflight.py themen/*.html
```

Erwartete Ausgabe: `ALLE CHECKS BESTANDEN`. Jede Meldung wird vor dem Commit behoben.
Geprüft wird: div/details-Bilanz, MathJax-Delimiter-Parität, doppelte IDs, kein ß,
keine Dezimalkommas in Math, `node --check` auf Inline-JS, Skelett-Marker,
Phantom-Klassen, physiklib-Abhängigkeit, Duplicate-Marker, Slot-Limits.

## Verifikations-Standard

- **Alle Zahlenwerte vor dem Einbau mit `python3` nachrechnen** — nie aus dem Gedächtnis.
- **Geometrie von Canvas-Animationen vorab in Python durchrechnen** (Vektor-Spitzen,
  Bahnkurven, Label-Positionen), bevor der Zeichencode geändert wird. Grad/Radiant prüfen.
- `node --check` auf jedem Script-Block (der Pre-Flight macht das mit).
- Render-Check bei Diagramm-Änderungen, wenn ein Browser verfügbar ist: Playwright
  headless bei 1280 px **und** 360 px, Screenshots der Canvases sichten (Tick-Werte
  lesbar, Achsenlabels überdecken nichts, keine Kollision mit Inhalts-Markern).
- **Keine erfundenen Quellen, Zitate oder Lehrplan-Stellen.** Im Zweifel: „muss
  verifiziert werden" schreiben, nicht raten.

## Externe Ressourcen

Anbieter-Reihenfolge strikt (Videos: musstewissen → Lehrerschmidt → Doc Schuster →
Fufaev → Phil's Physics → MrWissen2go; Sim: PhET → oPhysics → Leifi → Walter Fendt →
GeoGebra; Aufgaben: Leifi → SwissEduc → serlo). Playlists vor Einzelvideos. Max. 4 Links
je Sektion. **YouTube-Verifikation per `web_fetch` auf die Playlist-URL** (liefert Owner +
Anzahl) — Präfix-Heuristik ist unzuverlässig. Negativ-Liste und Details: STYLEGUIDE /
`HOWTO-externe-ressourcen.md`.

## Arbeitsweise

- **Bei klarem Auftrag direkt umsetzen**, keine Rückfrage. Annahme nötig → inline kurz
  erwähnen. Bei echter Mehrdeutigkeit max. 3 gebündelte Fragen, dann starten.
- **Keine ungebetene Verbesserungs-Initiative.** Was nicht Teil des Auftrags ist, wird
  nicht mit-gepatcht — höchstens im Output kurz erwähnt. Kein Refactoring „weil eleganter".
- Mehr als 3 gleichartige Edits → ein Skript (`sed`/`python`), nicht N Einzel-Edits.
- Vor gezielten Edits `grep -n` + enger `view`, um Whitespace/Sonderzeichen exakt zu treffen.
- Git ist das Sicherheitsnetz: vor grösseren Sessions committen, Diffs prüfen, sauber
  zurückrollen statt ZIP-Snapshots.

## Was die Sandbox-Werkstatt (Chat) übernimmt

Abgeleitete Artefakte mit Spezial-Werkzeug bleiben besser im Chat, falls lokal nicht
installiert: **Anki-APKG-Rebuilds** (ZIP+SQLite — lokal ok, wenn Python steht),
**xlsx-Recalc** (braucht LibreOffice), **docx-Generierung** (braucht docx-Skill/Libs).
Inhalts-Edit lokal machen, abgeleitetes Artefakt danach regenerieren.
