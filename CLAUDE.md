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

- `themen/` — Vorwissen (6 Seiten): `p0-0` (Alltagstour), `p0-1` (Rechnen und
  Schliessen), `p0-2` (Grössen, Einheiten und Messen), `p0-3` (Messen — Waagen,
  Dichte, Einheiten), `p0-4` (Einheitentrainer), `p0-5` (Die sieben SI-Basiseinheiten). Auf `p0-1`/`p0-2` tragen die aus
  den früheren Seiten 0.3/0.4 übernommenen Widgets den ID-Präfix `b` statt `a`; ihr
  Skript steht gekapselt in einer IIFE am Dateiende.
- `themen/p0-4-einheitentrainer.html` — Übungsseite mit drei Modi (Freies Üben,
  Lernmodus, Prüfungsmodus). Einziger Ort im Repo, der `localStorage` nutzt (Key
  `tals-physik-p0-4-lernstand-v1`, Lernstand mit Rücksetzknopf) — deshalb hält
  `rechtliches.html` das ausdrücklich fest. Einheiten und Faktoren stehen dort in
  **einer** Datenstruktur (`ET_GRUPPEN`), aus der Aufgaben, Diagnosen und die
  Umrechnungstabellen zugleich entstehen; Faktoren nie an zweiter Stelle notieren.
- `themen/` — 10 Themenseiten: `p4-1`…`p4-5` (Mechanik), `p5-1`…`p5-3` (Thermo),
  `p6-1`,`p6-2` (Wellen/Elektrizität). Alle inhaltlich fertig und auditiert.
  Dazu `p6-1a-wellenexperimente.html` — Vertiefung zu 6.1, im RLP nicht als
  eigenes Teilgebiet geführt (macht zusammen 17 Dateien in `themen/`).
- `physiklib.js` — Canvas-Bibliothek + globale Helfer (`toggleL`, `fmt`, `initCanvas`,
  `drawGrid`, `drawAxesUnits`, `drawArrow`, `drawVector`, `drawDot`, …).
- `minicheck.js` — Akkordeon-Logik der Mini-Checks. `anim-hinweise.js` — Hinweis-Logik.
- `nav.js` — Navigation (`buildNav`) inkl. Suchfeld im Header rechts. `style.css` — gesamtes Design.
- `scripts/build-seo.py` — erzeugt Seiten-Metadaten (Beschreibung, canonical, Open
  Graph, JSON-LD nach schema.org/LearningResource), `sitemap.xml` und `robots.txt`.
  Der Kopfblock zwischen `<!-- SEO:ANFANG -->` und `<!-- SEO:ENDE -->` ist
  **generiert** — gepflegt wird die Tabelle `SEITEN` im Skript. Neue Seite = dort
  eintragen, sonst fehlen ihr Beschreibung und Sitemap-Eintrag. Der Pre-Flight
  warnt, wenn die Metadaten veraltet sind.
- `scripts/verify_einheitentrainer.js` — Selbsttest des Einheitentrainers: lädt
  `p0-4` in jsdom und ruft dort `etSelbsttest(n)` auf (jedes angebotene
  Einheitenpaar hin und zurück, Referenzwerte, Grenzfälle, Generator, Toleranz,
  Eingabeformate, Diagnosekategorien). Standard 5 Zufallsaufgaben je Paar,
  `--gross` fährt 200 je Paar (über 50 000). Läuft im Pre-Flight mit.
- `suche.js` — Volltextsuche (Logik + Trefferpanel). `suchindex.js` — **generiert**,
  nie von Hand ändern: `python3 scripts/build-suchindex.py` (siehe Pre-Flight).
  Der Generator läuft in **beiden** TALS-Repos (erkennt Physik/Mathe an
  `physiklib.js`/`mathlib.js`); projektabhängig ist allein die Liste `PROJEKTE`
  am Dateikopf. `--dry-run` baut ohne zu schreiben, `--root PFAD` zielt aufs
  Schwesterprojekt.
- `scripts/build-animationen.py` — setzt die **Animationsnummern** aus der
  Dokumentreihenfolge, in den `<h3>`-Titeln wie in den Textverweisen. Gepflegt
  wird im Quelltext nur der Anker, nie die Nummer (Details: STYLEGUIDE §5.9).
  `--check` prüft ohne zu schreiben, `--root PFAD` zielt aufs Schwesterprojekt.
  Der Pre-Flight ruft `--check` auf und meldet Abweichungen als **[FEHLER]**.
- `schriften.css` + `schriften/` — **lokal ausgelieferte Schriften** (Source Serif 4,
  Source Sans 3, JetBrains Mono; Fontsource, OFL 1.1). Subsets latin / latin-ext /
  **greek** — Letzteres ist Pflicht: ausserhalb von MathJax stehen im Repo rund
  hundert griechische Zeichen (Ω, Δ, ϑ, α, λ, …). `vendor/mathjax/` — **lokales
  MathJax 3.2.2** (dieselbe Fassung, die das CDN lieferte), samt
  `input/tex/extensions/boldsymbol.js` (20 Seiten laden es), `output/chtml*` und
  `a11y/`+`sre/mathmaps/` für die Menüpunkte «Math Renderer» und «Accessibility».
  Umgestellt wird mit `scripts/schriften-lokal.py` und `scripts/mathjax-lokal.py`
  (`--schreiben`; wiederholbar, rechnen die `../`-Tiefe selbst aus).
  **Kein Aufruf an fonts.googleapis.com, fonts.gstatic.com oder cdn.jsdelivr.net** —
  der Pre-Flight meldet ihn als `[FEHLER]`.
- `.claude/tools/pruef-mathjax.mjs` — lädt eine **ausgelieferte** Seite im Browser,
  zählt die gesetzten Ausdrücke und meldet jede fehlgeschlagene Anfrage. Das sieht
  der Pre-Flight strukturell nicht: `verify_mathjax.js` setzt mit `mathjax-full`
  aus `node_modules` und schaut nie in `vendor/`. MathJax lädt TeX-Erweiterungen
  erst **bei Bedarf** nach — fehlt eine, bleibt die **komplette Seite** ohne
  Formelsatz, ohne Fehlermeldung im Bild. Darum liegt der ganze Ordner
  `vendor/mathjax/input/tex/extensions/` im Repo (34 Dateien, 340 kB, nur bei
  Bedarf geladen; `all-packages.js` fehlt bewusst — der Autoload fordert es nie an).
  Nachgemessen: ohne `color.js` rendert eine Seite mit einem einzigen `\textcolor`
  **0 von 162** Ausdrücken.
- `.claude/tools/pruef-clip.mjs` — dasselbe für einen einzelnen Clip.
- `.claude/tools/render-check.mjs` — Render-Kontrolle bei 1280 und 360 px in echtem
  Chromium: meldet seitlichen Überlauf und Inhalte, die ein Vorfahr mit
  `overflow:hidden` unsichtbar abschneidet. Das kann der Pre-Flight nicht — jsdom
  hat kein Layout.
- `.claude/tools/scan-live.mjs` — sucht den **Malpunkt als Trennzeichen** in
  Wertanzeigen (STYLEGUIDE §2.1). Fährt jede Seite durch ihre Bedienzustände und
  liest Wertanzeigen **und** Canvas-`fillText` — Letzteres ist der Grund für das
  eigene Werkzeug: Animationsbeschriftungen stehen in keinem DOM-Knoten.
  `--alle` listet jede `·`-Zeile für die vollständige Sichtung. Exit 1 bei
  Verdachtsfällen. Nicht im Pre-Flight (braucht einen echten Browser).
- `.claude/tools/build-bilder.mjs` — baut `favicon-32.png`, `apple-touch-icon.png`
  (aus `favicon.svg`) und `og-bild.png` (aus einer HTML-Vorlage im Skript) mit
  Playwright neu. Nur bei Bedarf laufen lassen: die PNGs sind versioniert und
  ändern sich nur, wenn Farbe, Wortlaut, Adresse oder Schrift der Vorlage
  angepasst werden. Wortlaut und Adresse gehören in die Vorlage, nicht ins Bild.
- `.quellen/formelsammlung/` — LaTeX-Quelle der illustrierten Formelsammlung samt
  Bauanleitung (`README-Build.md`). Punkt-Ordner, damit GitHub Pages ihn nicht
  ausliefert. Das fertige PDF steht als `TALS-Physik-Formelsammlung.pdf` im Root;
  nach einem Neubau (`latexmk -pdf formelsammlung.tex`) dorthin kopieren.
- `scripts/build-clip-ton.py` — **Vertonung** eines Clips, lokal und offline mit
  Piper. Erzeugt **eine** MP3 je Clip (`clips/ton/<name>.mp3`) und schreibt die
  gemessene Sprechdauer je Szene als `dauer` ins Drehbuch zurück — danach sitzt
  Bild auf Sprache. Aufruf mit `PIPER_MODELL=<pfad zur .onnx>`; danach den Clip
  mit `build-clips.py` neu bauen. **Zahlen im `sprecher`-Text ausschreiben:**
  nachgemessen liest die Stimme `1.62` als «eins Punkt zweiundsechzig» statt
  «ein Komma sechs zwei». Das Stimmmodell liegt bewusst ausserhalb des Repos.
- `clips.html` + `clips/` — **Erklärclips** (Bibliotheksseite und Drehbücher).
  Ein Clip wird nie beim Seitenaufruf geladen: sichtbar ist zuerst nur der
  Startknopf, erst der Klick setzt das `<iframe>` ein (`clipStart` in
  `physiklib.js`). `scripts/build-clips.py` baut aus einem Drehbuch
  (`clips/<name>.json`) den Clip, `scripts/build-clips-einbau.py` trägt ihn in
  die Lektionsseite und zwischen die Marker `<!-- CLIPS-BIBLIOTHEK:ANFANG/ENDE -->`
  in `clips.html` ein. Physik hat **noch keine Clips** — die Mechanik steht
  bereit, die Bibliothek sagt bis dahin «Noch keine Clips.». Anders als Mathe
  gruppiert die Bibliothek nur nach Lerngebiet (kein Grundlagen-/Schwerpunktfach).
- `leitprogramme.html` + `leitprogramme/` — **Selbstlerneinheiten**. Vorgehen beim
  Übertrag einer extern gebauten Datei: `HOWTO-leitprogramme.md` (neun Punkte,
  je mit dem Fehlerbild, an dem man merkt, dass der Punkt fehlt). Die
  Bibliotheksseite trägt nur die Karten (`.lp-*` in `style.css`); jedes
  Leitprogramm ist eine **eigenständige Seite mit eigenem Inhalts-CSS** und
  bewusst ohne `nav.js`/`style.css` — Aufbau und Ablauf sind auf das
  Leitprogramm zugeschnitten. Verbindlich bleiben: keine Fremdhosts
  (`../schriften.css`, `../vendor/mathjax/tex-svg.js`) und je ein Anker auf den
  `<h2>`, damit `build-suchindex.py` dort Abschnitte schneiden kann.
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

- Neue Seite / neuer Block: Skelett aus `themen/p4-1-kinematik.html`
  **1:1 kopieren**, nur Inhalt anpassen (die frühere `TEMPLATE.html` ist am
  31.07.2026 entfallen — die Pilotseite ist die Vorlage). CSS und `nav.js` sind auf die *exakten*
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
Bilanz, doppelte IDs, kein ß, Dezimalkomma in Body-Math, **HTML innerhalb eines
LaTeX-Ausdrucks**, Skelett, Phantom-Klassen, physiklib-Einbindung, Ressourcen-Marker,
Slot-Limits und **keine Fremdhosts** (`fonts.googleapis.com`, `fonts.gstatic.com`,
`cdn.jsdelivr.net`); (2) Aufruf der vorhandenen Repo-Skripte `verify_mathjax.js` (echte
Render-Prüfung), `verify_js_runtime.js` (JS-Laufzeit) und `verify_einheitentrainer.js`
(Selbsttest von p0-4). `verify_js_runtime.js` bekommt nur `themen/`-Seiten zu sehen —
es ersetzt Einbindungen der Form `src="../nav.js"` und meldet auf Wurzelseiten sonst
einen Fehler, der keiner ist. Stufe 2 braucht einmalig `npm install mathjax-full jsdom` im
Repo-Root; fehlen die Module, werden diese Checks als `[WARN]` übersprungen.
**Vom Repo-Root aufrufen.**

## Stichwort «Stilcheck»

Nennt der Auftraggeber im Prompt **„Stilcheck"**, dann gilt zusätzlich zum
eigentlichen Auftrag: **alle gesammelten Darstellungsregeln an den berührten
Stellen prüfen und korrigieren** — nicht nur die neu geschriebenen Zeilen,
sondern die ganze Animation / den ganzen Abschnitt, an dem gearbeitet wird.

Die Liste steht in `STYLEGUIDE.md` und wächst; aktuell:

| # | Regel | STYLEGUIDE |
|---|---|---|
| 1 | Live-Box: Spaltenabstand gestuft (70/40/24 px), nie auf Zeilenabstand zusammenfallen. Wer einen Wert hinzufügt, prüft die ganze Box. | §5.3 |
| 2 | In Rechen-/Wertanzeigen (`.fl-eq`, `.lb-val`, `.sl-val`, Canvas-Zahlen, Rückmeldungen) heisst `·` **nur Multiplikation — nie Trennzeichen**. Ersatz: Strichpunkt `;` (Wertepaare, gleichrangige Ergebnisse, Aufzählungen), Doppelpunkt (Etikett vor Wert), Klammer (Zusatzangabe), Pfeil `→` (Rechenschritte) — **kein Komma**, der Strichpunkt gilt in beiden TALS-Projekten. Zwei Gleichungen = zwei `.fl-eq`-Zeilen. Prüfen in HTML, JS-Strings **und** `fillText` über alle Bedienzustände. Titel, Breadcrumbs, Bedienhinweise und Wort-Trennungen (`Basalt · Gneis`) sind ausgenommen. | §2.1 |
| 3 | **Jede** `.fl-eq` nennt zuerst die Formel symbolisch, dann die Werte (Ansatz-Prinzip in Live-Anzeigen) — auf der ganzen Seite prüfen, nicht nur an der geänderten Animation. | §2.1 |
| 4 | Werte werden **mit Einheit** eingesetzt, auch in `.fl-eq` (`1.0 kg · 4182 J/(kg·K) · 50 K`). Dimensionslose «Teile» durch eine konkrete Bezugsgrösse ersetzen. | §2.7 |
| 5 | Formelzeilen **komplett** in LaTeX — Formel *und* Zahlengleichung, Brüche als `\frac{…}{…}`. Dynamisches Neu-Rendern gedrosselt und serialisiert; auf doppelte Backslashes in JS-Strings achten. | §2.8 |
| 6 | **Preis** = Kosten pro Einheit (CHF/kg, CHF/km); **Kosten** = Gesamtbetrag (CHF). «Preis» nie mit der Einheit CHF — weder im Text noch an Achsen oder in Live-Boxen. | §2.6b |
| 7 | **Liter klein**: `l`, `ml`, `dl`, `kg/l` — nie `L`/`mL`. Gilt in LaTeX, Fliesstext, Tabellen, Live-Boxen und Canvas. Das grosse `L` bleibt, wo es Saiten-/Pendel-/Balkenlänge, latente Wärme, `mL` als margin-left oder Lektionen meint. | §2.3 |
| 8 | **Kein Gedankenstrich an einer Formel im Titel** — gerendert liest er sich als Vorzeichen. Vor der Formel: Doppelpunkt (nach `?`/`!` ersatzlos). Nach der Formel: Titel umstellen, Formel ans Ende. Nur direkter Kontakt zählt; Fliesstext bleibt. Gilt für `h2`, `h3`, `.block-titel`, `.aufg-titel-text`. | §2.9 |

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

0. Wurde eine Animation eingefügt, entfernt oder verschoben:
   `python3 scripts/build-animationen.py` (setzt Titel- und Verweisnummern neu).
   Wurde Fliesstext auf einer Themenseite, im Glossar oder in der Formelsammlung
   geändert: `python3 scripts/build-suchindex.py` (der Pre-Flight warnt sonst
   „Suchindex veraltet"). Die generierte `suchindex.js` gehört zum Commit.
1. Pre-Flight über die geänderten Themenseiten laufen lassen
   (`python3 .claude/skills/preflight/preflight.py themen/<datei>.html`).
2. **Nur wenn `ALLE CHECKS BESTANDEN`:** `git add -A` und `git commit` mit einer
   aussagekräftigen Message (Seite + was geändert wurde, z.B.
   `p4-2: Beispiel 2 auf Ansatz-Prinzip, ❓ Reibung, MC3 umformuliert`).
3. Schlägt der Pre-Flight fehl: **nicht committen**, Fehler melden und beheben, dann 1.
4. **Niemals `git push`.** Der Push bleibt manuell beim Auftraggeber.

**Der Git-Verlauf ist die einzige Änderungsdokumentation.** `CHANGELOG.md` und die
TODO-/BERICHT-Dateien sind am 31.07.2026 aus dem Repo entfernt worden, weil das
Repo zugleich die veröffentlichte Website ist und die Entstehungsgeschichte nicht
öffentlich einsehbar sein soll. Kein Wiederanlegen, keine Änderungsprotokolle als
Datei — jede Änderung wird über eine aussagekräftige Commit-Message dokumentiert.

`git add`, `git commit` und der Pre-Flight sind in der `settings.json` vorab erlaubt und
laufen darum prompt-frei. `git push` steht bewusst unter `ask` — es hält an.

## Was die Sandbox-Werkstatt (Chat) übernimmt

Abgeleitete Artefakte mit Spezial-Werkzeug bleiben besser im Chat, falls lokal nicht
installiert: **Anki-APKG-Rebuilds** (ZIP+SQLite — lokal ok, wenn Python steht),
**xlsx-Recalc** (braucht LibreOffice), **docx-Generierung** (braucht docx-Skill/Libs).
Inhalts-Edit lokal machen, abgeleitetes Artefakt danach regenerieren.
