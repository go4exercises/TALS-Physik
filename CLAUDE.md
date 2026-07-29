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

- `themen/` — Vorwissen: `p0-0` (Alltagstour), `p0-1` (Rechnen und Schliessen),
  `p0-2` (Grössen, Einheiten und Messen). Auf `p0-1`/`p0-2` tragen die aus den
  früheren Seiten 0.3/0.4 übernommenen Widgets den ID-Präfix `b` statt `a`; ihr
  Skript steht gekapselt in einer IIFE am Dateiende.
- `themen/` — 10 Themenseiten: `p4-1`…`p4-5` (Mechanik), `p5-1`…`p5-3` (Thermo),
  `p6-1`,`p6-2` (Wellen/Elektrizität). Alle inhaltlich fertig und auditiert.
- `physiklib.js` — Canvas-Bibliothek + globale Helfer (`toggleL`, `fmt`, `initCanvas`,
  `drawGrid`, `drawAxesUnits`, `drawArrow`, `drawVector`, `drawDot`, …).
- `minicheck.js` — Akkordeon-Logik der Mini-Checks. `anim-hinweise.js` — Hinweis-Logik.
- `nav.js` — Navigation (`buildNav`) inkl. Suchfeld im Header rechts. `style.css` — gesamtes Design.
- `suche.js` — Volltextsuche (Logik + Trefferpanel). `suchindex.js` — **generiert**,
  nie von Hand ändern: `python3 scripts/build-suchindex.py` (siehe Pre-Flight).
- `rechtliches.html` — Haftung + Datenschutz, verlinkt aus Footer und Feedbackformular
  (bewusst **kein** eigener Headerpunkt). Kontakt läuft ausschliesslich über
  `feedback.html` („Kontakt & Feedback") — es gibt keine veröffentlichte E-Mail-Adresse.
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

Erwartete Ausgabe: `ALLE CHECKS BESTANDEN`. Jede `[FEHLER]`-Meldung wird vor dem Commit
behoben (`[WARN]` ist kein Blocker). Zweistufig: (1) schnelle Eigen-Checks — div/details-
Bilanz, doppelte IDs, kein ß, Dezimalkomma in Body-Math, Skelett, Phantom-Klassen,
physiklib-Einbindung, Ressourcen-Marker und Slot-Limits; (2) Aufruf der vorhandenen
Repo-Skripte `verify_mathjax.js` (echte Render-Prüfung) und `verify_js_runtime.js`
(JS-Laufzeit). Stufe 2 braucht einmalig `npm install mathjax-full jsdom` im Repo-Root;
fehlen die Module, werden diese Checks als `[WARN]` übersprungen. **Vom Repo-Root aufrufen.**

## Stichwort «Stilcheck»

Nennt der Auftraggeber im Prompt **„Stilcheck"**, dann gilt zusätzlich zum
eigentlichen Auftrag: **alle gesammelten Darstellungsregeln an den berührten
Stellen prüfen und korrigieren** — nicht nur die neu geschriebenen Zeilen,
sondern die ganze Animation / den ganzen Abschnitt, an dem gearbeitet wird.

Die Liste steht in `STYLEGUIDE.md` und wächst; aktuell:

| # | Regel | STYLEGUIDE |
|---|---|---|
| 1 | Live-Box: Spaltenabstand gestuft (70/40/24 px), nie auf Zeilenabstand zusammenfallen. Wer einen Wert hinzufügt, prüft die ganze Box. | §5.3 |
| 2 | In Rechen-/Wertanzeigen (`.fl-eq`, `.lb-val`, Canvas-Zahlen) heisst `·` nur Multiplikation — nie Trennzeichen. Zwei Gleichungen = zwei `.fl-eq`-Zeilen. Titel/Breadcrumbs sind ausgenommen. | §2.1 |
| 3 | **Jede** `.fl-eq` nennt zuerst die Formel symbolisch, dann die Werte (Ansatz-Prinzip in Live-Anzeigen) — auf der ganzen Seite prüfen, nicht nur an der geänderten Animation. | §2.1 |
| 4 | Werte werden **mit Einheit** eingesetzt, auch in `.fl-eq` (`1.0 kg · 4182 J/(kg·K) · 50 K`). Dimensionslose «Teile» durch eine konkrete Bezugsgrösse ersetzen. | §2.7 |
| 5 | Formelzeilen **komplett** in LaTeX — Formel *und* Zahlengleichung, Brüche als `\frac{…}{…}`. Dynamisches Neu-Rendern gedrosselt und serialisiert; auf doppelte Backslashes in JS-Strings achten. | §2.8 |
| 6 | **Preis** = Kosten pro Einheit (CHF/kg, CHF/km); **Kosten** = Gesamtbetrag (CHF). «Preis» nie mit der Einheit CHF — weder im Text noch an Achsen oder in Live-Boxen. | §2.6b |

Neue Regeln, die der Auftraggeber ansagt, werden in STYLEGUIDE.md aufgenommen
**und** hier in der Tabelle nachgeführt.

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

## Automatik: Diffs nicht bestätigen + Commit nach jedem Durchgang

Dieses Repo läuft im Modus `acceptEdits` (siehe `.claude/settings.json`): Datei-Edits
werden ohne einzelne Diff-Bestätigung übernommen. Das Sicherheitsnetz ist nicht mehr die
Vorab-Kontrolle, sondern Git — darum gilt verbindlich:

**Nach jedem abgeschlossenen Auftrag (= ein „Durchgang") automatisch, ohne Rückfrage:**

0. Wurde Fliesstext auf einer Themenseite, im Glossar oder in der Formelsammlung
   geändert: `python3 scripts/build-suchindex.py` (der Pre-Flight warnt sonst
   „Suchindex veraltet"). Die generierte `suchindex.js` gehört zum Commit.
1. Pre-Flight über die geänderten Themenseiten laufen lassen
   (`python3 .claude/skills/preflight/preflight.py themen/<datei>.html`).
2. **Nur wenn `ALLE CHECKS BESTANDEN`:** `git add -A` und `git commit` mit einer
   aussagekräftigen Message (Seite + was geändert wurde, z.B.
   `p4-2: Beispiel 2 auf Ansatz-Prinzip, ❓ Reibung, MC3 umformuliert`).
3. Schlägt der Pre-Flight fehl: **nicht committen**, Fehler melden und beheben, dann 1.
4. **Niemals `git push`.** Der Push bleibt manuell beim Auftraggeber.

`CHANGELOG.md` wird **nicht** mehr gepflegt — die Datei ist mit Phase 5.41
(13.06.2026) abgeschlossen, seither ist der Git-Verlauf die Quelle. Kein
Nachtragen, auch nicht rückwirkend.

`git add`, `git commit` und der Pre-Flight sind in der `settings.json` vorab erlaubt und
laufen darum prompt-frei. `git push` steht bewusst unter `ask` — es hält an.

## Was die Sandbox-Werkstatt (Chat) übernimmt

Abgeleitete Artefakte mit Spezial-Werkzeug bleiben besser im Chat, falls lokal nicht
installiert: **Anki-APKG-Rebuilds** (ZIP+SQLite — lokal ok, wenn Python steht),
**xlsx-Recalc** (braucht LibreOffice), **docx-Generierung** (braucht docx-Skill/Libs).
Inhalts-Edit lokal machen, abgeleitetes Artefakt danach regenerieren.
