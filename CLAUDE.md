# CLAUDE.md — Physik begreifbar

Statisches HTML/CSS/JS-Lehrmittel für die BM (RLP-BM 2030), gehostet via GitHub Pages
unter `physik.begreifbar.ch` (Datei `CNAME`; bis 10.08.2026 `go4exercises.github.io/TALS-Physik`).
Schwester-Projekt zu Mathe begreifbar (Repo `tals-mathe`, `mathe.begreifbar.ch`). Diese Datei ist die lokale Claude-Code-Variante der
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
  eintragen, sonst fehlen ihr Beschreibung und Sitemap-Eintrag. `--check` prüft
  ohne zu schreiben (Exit 1 = veraltet; so ruft der Pre-Flight es auf und warnt),
  `--dry-run` zeigt, welche Dateien sich ändern würden, `--dry-run --diff`
  zusätzlich die Zeilen selbst.
- `scripts/verify_einheitentrainer.js` — Selbsttest des Einheitentrainers: lädt
  `p0-4` in jsdom und ruft dort `etSelbsttest(n)` auf (jedes angebotene
  Einheitenpaar hin und zurück, Referenzwerte, Grenzfälle, Generator, Toleranz,
  Eingabeformate, Diagnosekategorien). Standard 5 Zufallsaufgaben je Paar,
  `--gross` fährt 200 je Paar (über 50 000). Läuft im Pre-Flight mit.
- `suche.js` — Volltextsuche (Logik + Trefferpanel). `suchindex.js` — **generiert**,
  nie von Hand ändern: `python3 scripts/build-suchindex.py` (siehe Pre-Flight).
  Der Generator läuft in **beiden** TALS-Repos (erkennt Physik/Mathe an
  `physiklib.js`/`mathlib.js`); projektabhängig ist allein die Liste `PROJEKTE`
  am Dateikopf. `--check` prüft ohne zu schreiben (Exit 1 = veraltet; so ruft
  der Pre-Flight es auf), `--dry-run` baut und sagt, ob und um wie viele
  Abschnitte sich der Index ändern würde, `--root PFAD` zielt aufs
  Schwesterprojekt. **Clips stehen einzeln im Index** (Kurzbeschrieb,
  Transkript, Stichworte; Ziel `clips.html#clip-<name>`) — der
  Transkript-Aufklapper der Lektionsseite ist darum vom Index ausgenommen.
  Die Kopfzeile von `suchindex.js` sagt noch «TALS Physik» — **bewusst**: Der
  Name steht im geteilten Generator, und eine einseitige Änderung wäre Drift
  gegen Mathe. Nicht von Hand «korrigieren».
- `scripts/abgleich.py` — vergleicht das **geteilte Werkzeug** mit dem
  Schwesterrepo `tals-mathe`. Physik und Mathe teilen rund 5200 Zeilen
  Build-Skripte und Prüfer; gepflegt werden sie zweimal, und sie laufen
  auseinander. Das Skript verhindert das nicht, es macht es sichtbar: drei
  Klassen (`GLEICH` Fremdgut — jeder Unterschied ist ein Befund; `KERN`
  geteiltes Werkzeug, gemessen gegen eine **Grundlinie**, die nur steigen
  darf; `FACH` bewusst verschieden, mit Begründung). `--check` gibt Exit 1
  bei neuer Drift, `--diff DATEI` zeigt sie, `--gegen PFAD` wählt das
  Gegenüber. Es schreibt nie etwas, und fehlt das Schwesterrepo, endet es
  mit Exit 0. Der Pre-Flight ruft es auf und meldet Drift als **[WARN]** —
  ein Hinweis, kein Blocker. Dieselbe Datei liegt in beiden Repos; wer eine
  Fassung angleicht, trägt die neue, höhere Grundlinie dort ein.
- `scripts/check_identifier_collisions.py` — findet Symbole in den
  Inline-Skripten der Themenseiten, die mit `physiklib.js` oder `nav.js`
  kollidieren. Ein kollidierendes `const` ist **blockierend**: Der Browser
  bricht das ganze Inline-Skript beim Parsen ab, und jede Funktion darin ist
  weg. `function`/`var` überleben, überschreiben aber die Bibliotheksfassung.
  Läuft im Pre-Flight mit; aus tals-mathe übernommen (13.09.2026).
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
- `.claude/tools/pruef-clip.mjs` — dasselbe für einen einzelnen Clip, dazu die
  Geometrie: Es springt in einzelne Sekunden, misst die sichtbaren Zeilen und
  meldet Überlappungen sowie alles, was über die Bühne hinausragt. Gemessen wird
  seit dem 07.09.2026 der **Inhalt**, nicht der Container — eine Formelzeile
  trägt `white-space:nowrap`, läuft über ihren 1140 px breiten Container hinaus
  und wurde vorher nicht bemerkt. Zeitmarken dicht setzen (alle 2 bis 4 s), sonst
  trifft man den Zustand nicht, in dem sich etwas berührt. Bilder landen in `$SP`;
  ohne die Variable im Arbeitsverzeichnis (`szene-*.png` ist darum in
  `.gitignore`).
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
- `.claude/tools/aufnahme-anim.mjs` — nimmt Zustände einer Animation als JPEG
  für Clips auf (Plan-JSON: Seite, Element, Aktionen per Klick, Reglerwert oder
  JS; doppelte Pixeldichte). Eine Animation mit eigenem Loop vorher anhalten
  (`…Loop.userPaused = true; …Loop.stop()`), sonst startet sie beim
  Hineinscrollen und das Bild zeigt einen anderen Zeitpunkt; kein
  `scrollIntoView` im Plan — das holt die Kopfzeile mit ins Bild.
- `.claude/tools/build-bilder.mjs` — baut `favicon-32.png`, `apple-touch-icon.png`
  (aus `favicon.svg`) und `og-bild.png` (aus einer HTML-Vorlage im Skript) mit
  Playwright neu. Nur bei Bedarf laufen lassen: die PNGs sind versioniert und
  ändern sich nur, wenn Farbe, Wortlaut, Adresse oder Schrift der Vorlage
  angepasst werden. Wortlaut und Adresse gehören in die Vorlage, nicht ins Bild.
- `.quellen/formelsammlung/` — LaTeX-Quelle der illustrierten Formelsammlung samt
  Bauanleitung (`README-Build.md`). Punkt-Ordner, damit GitHub Pages ihn nicht
  ausliefert. Das fertige PDF steht als `TALS-Physik-Formelsammlung.pdf` im Root;
  nach einem Neubau (`latexmk -pdf formelsammlung.tex`) dorthin kopieren. Der
  **Dateiname bleibt** trotz neuer Marke — Menü, Sitemap und p0-4 zeigen darauf.
  LaTeX (TeX Live 2025) ist lokal installiert, der Neubau braucht keinen Chat
  mehr. Zwei Fallen, beide in `README-Build.md`: mindestens zwei Läufe (die
  laufende Kopfzeile liest ihre Marken aus der `.aux`), und babel heisst
  `german`, nicht `ngerman` (seit TeX Live 2025 ein Abbruch).
- `scripts/build-clip-ton.py` — **Vertonung** eines Clips, lokal und offline mit
  Piper. Erzeugt **eine** MP3 je Clip (`clips/ton/<name>.mp3`) und schreibt die
  gemessene Sprechdauer je Szene als `dauer` ins Drehbuch zurück — danach sitzt
  Bild auf Sprache. Danach den Clip mit `build-clips.py` neu bauen.

  **Keine Zweitstimme.** Mathe hatte zeitweise `--zweitstimme` samt
  Umschalter im Player — gebaut für das persönliche Modell, das hier nicht
  verwendet wird. Am 26.09.2026 bewusst nicht übernommen; der Rückbau in
  Mathe steht in der Warteschlange von `scripts/abgleich.py`.

  **Stimme: `de_DE-thorsten-high` (verbindlich, bis der Auftraggeber es ändert).**

  ```bash
  export PIPER_MODELL=/home/paps/piper-stimmen/de_DE-thorsten-high.onnx
  python3 scripts/build-clip-ton.py <clipname>
  python3 scripts/build-clips.py    <clipname>
  ```

  Datensatz Thorsten-Voice, CC0 — dieselbe Stimme wie in Mathe begreifbar. Das
  persönliche Modell `de_CH-kohler-medium` wird **nicht** verwendet. Kein
  Stimmmodell gehört ins Repo.

  **Aussprache von Fremdwörtern:** Die Tabellen `AUSSPRACHE`, `ABKUERZUNGEN`
  und `TAUSCH` in `build-clip-ton.py` ändern nur den Text an Piper;
  Transkript und Suchindex behalten die Schreibweise. Stand 27.09.2026, jeder
  Eintrag nach Hörproben entschieden: Einheiten (Ampere, Coulomb, Joule,
  Pascal, Hertz), Namen (Boyle, Mariotte, Gay-Lussac, Hooke, Pythagoras),
  Fremdwörter (u. a. Zentripetal…, das die Stimme englisch las),
  buchstabierte Abkürzungen (FI, LED, COP, SI) und drei Worttausche
  (achthundert, Newtonmeter, Lageenergie). Archimedes, Perihel und Parabel
  bleiben bewusst ungeändert. Ein neues Wort gehört in diese Tabellen, nicht
  als Umschreibung ins Drehbuch; betroffene Clips danach neu vertonen. Wie man
  Problemwörter findet und Hörproben zeigt: `HOWTO-clips.md`, Abschnitt «Ton».

  **Zahlen im `sprecher`-Text ausschreiben.** Nachgemessen über die Sprechdauer
  desselben Satzes in fünf Varianten: Beide Stimmen lesen `1.62` als
  zusammengesetzte Zahl («… zweiundsechzig») statt als Stellenfolge
  («… sechs zwei»), kohler zusätzlich den Dezimalpunkt als «Punkt». Bei
  Messwerten ist die Stellenfolge die übliche Lesart — darum ausschreiben. In
  Mathes 162 Clips steht aus demselben Grund fast nirgends eine Ziffer im
  Sprechertext; die Ausnahmen sind Geräte- und Listennamen (`TI-30X`, `L1`) —
  das sind Namen, keine Werte. Die Reihe `trigo2` hält sich als einzige nicht
  daran (18 Szenen, Stand 13.09.2026).
- `clips.html` + `clips/` — **Erklärclips** (Bibliotheksseite und Drehbücher).
  Ein Clip wird nie beim Seitenaufruf geladen: sichtbar ist zuerst nur der
  Startknopf, erst der Klick setzt das `<iframe>` ein (`clipStart` in
  `physiklib.js`). `scripts/build-clips.py` baut aus einem Drehbuch
  (`clips/<name>.json`) den Clip, `scripts/build-clips-einbau.py` trägt ihn in
  die Lektionsseite und zwischen die Marker `<!-- CLIPS-BIBLIOTHEK:ANFANG/ENDE -->`
  in `clips.html` ein. Stand 28.09.2026: **151 Clips in 25 Reihen, 155:47 min** (davon 62 zu einzelnen Animationen auf 4.1 bis 5.3 und 6.2, Reihe «Animationen erklärt») —
  jede der zehn Themenseiten der Lerngebiete 4 bis 6 hat ihre Reihe, dazu das
  Vorwissen. Anders als Mathe gruppiert die Bibliothek nur nach Lerngebiet
  (kein Grundlagen-/Schwerpunktfach), und sie zieht die Gruppen aus `nav.js`,
  nicht aus dem Freitextfeld `lerngebiet` im Drehbuch.
  Ein Clip liegt **einmal** und darf über die Liste `lektion` auf mehreren
  Seiten stehen; elf tun das — die Bibliothek zeigt das mit der Zeile
  «↳ auch in 4.5 Hydrostatik» unter dem Titel. Über der Liste steht eine
  **Sofortsuche** (Titel, Reihe, Kurzbeschrieb, Schlagworte, Lektionsnummer);
  Feld und Filterskript stehen **ausserhalb** der Marker und werden von Hand
  gepflegt, das `data-suche` je Zeile kommt aus dem Generator.
  Auf der Themenseite steht der Clip-Block **nach der Zusammenfassung, vor dem
  Zusatzmaterial** (STYLEGUIDE §4, Zeile 11b).
  **Clips zu einer einzelnen Animation** (Prototyp 6.2, 27.09.2026): Drehbuch-Feld
  `animation` (Anker des `h3`), Reihe «Animationen erklärt», `folge` = Nummer der
  Animation. Der Generator setzt dann «▶ Clip» in die Titelzeile der Animation,
  stellt den Clip auf der Seite in die Gruppe «Clips zu den Animationen» und
  hebt ihn in beiden Listen in Bernstein ab, mit dem Link «Anim» davor. Bilder
  darin sind Aufnahmen der Animation selbst (`bild` mit JPG,
  `.claude/tools/aufnahme-anim.mjs`); der Titel muss sich klar vom Stoff-Clip
  zum selben Thema unterscheiden.
  Bauanleitung, Stolpersteine und die didaktische Prüfliste: `HOWTO-clips.md`.
- `leitprogramme.html` + `leitprogramme/` — **Selbstlerneinheiten**, aktuell elf:
  `leitprogramm-rechnen` (Proportionalität, Dreisatz, Umstellen,
  Zehnerpotenzen, Bogenmass, Plausibilität — sechs Clips, fünf Simulationen),
  `leitprogramm-vorwissen` (Grössen, Messen, Druck — sieben Clips, fünf
  Simulationen), `leitprogramm-waermemenge` (Temperatur, Wärmemenge, Bilanz,
  latente Wärme, Heizkurve, Heizzeit — zehn Clips, sieben Simulationen),
  `leitprogramm-heizen` (Wirkungsgrad, Heizwert, Wärmepumpe, Energiequellen,
  Wärmetransport, Treibhauseffekt — neun Clips, fünf Simulationen),
  `leitprogramm-waermeausdehnung` (Feststoffe und Flüssigkeiten
  — sieben Clips, sechs Simulationen), `leitprogramm-ideale-gase` (acht
  Clips, fünf Simulationen) und `leitprogramm-experimente-waerme` (der Einstieg
  über sieben Schulversuche statt über die Formel — sechs Clips, sieben
  gerechnete Simulationen) und `leitprogramm-schaltungen` (Knoten- und
  Maschenregel, Reihe, Spannungsteiler, Parallel, gemischte Schaltungen,
  Leistung — vier Clips, vier Simulationen; das erste ausserhalb der
  Thermodynamik; die Frage «40 W oder 60 W in Reihe?» bleibt von Schritt 2
  bis 6 offen), `leitprogramm-widerstand-leistung` (ohmsches Gesetz,
  Kennlinien, Messen, Leiterwiderstand, Leistung, Energie, Verlustleistung —
  sechs Clips, sieben Simulationen) und `leitprogramm-gefahren` (Erde als
  Rückleiter, Wirkung, FI, Schutzleiter, LS, Übersicht — zwei Clips, vier
  Simulationen); die drei Elektrizitäts-Leitprogramme folgen
  `Leitprogramme-Elektrizitaet-Architektur.md` (liegt neben dem Repo, nicht
  darin), mit den am 27.09.2026 korrigierten Merksätzen. Dazu als Sonderfall `uebungstest-waermelehre` — ein
  **Prüfungsbogen statt eines Stoffgebiets**: fünfzehn Aufgaben, je eine mit
  Aufgabentext, eigenem Erklärclip, Musterlösung und Fehlerkasten, dazu die
  Darstellungsregeln als roter Faden (16.09.2026). Alle elf starten ihre
  Clips über `.clipkarte`
  aus `clips/`; eigener, ins Dokument eingebetteter Ton gehört nicht hinein
  (siehe `HOWTO-leitprogramme.md`, Punkt 11). Vorgehen beim
  Übertrag einer fremden Datei **und** beim Schreiben einer neuen:
  `HOWTO-leitprogramme.md` (zwölf Punkte,
  je mit dem Fehlerbild, an dem man merkt, dass der Punkt fehlt); für eine
  Seite aus einem Prüfungs-PDF zusätzlich `HOWTO-uebungspruefung.md` (PDF
  misstrauisch lesen, `probe: true` für die Clips, die `</head>`-Falle, und
  wie ein Prüfungsrahmen wegbleibt, ohne dass die Aufgaben leiden). Die
  Bibliotheksseite trägt nur die Karten (`.lp-*` in `style.css`); jedes
  Leitprogramm ist eine **eigenständige Seite mit eigenem Inhalts-CSS**; Aufbau
  und Ablauf sind auf das Leitprogramm zugeschnitten. Kopfnavigation und Suche
  gehören trotzdem dazu: vor `</body>` stehen `../physiklib.js`, `../nav.js`,
  `../suche.js` und `buildNav({ id: 'leitprogramme' })` — ohne `physiklib.js`
  läuft jede Clipkarte ins Leere, weil `clipBuehne` von dort kommt (so bei
  `leitprogramm-schaltungen` vom 13.09. bis 27.09.2026). Verbindlich bleiben: keine Fremdhosts
  (`../schriften.css`, `../vendor/mathjax/tex-svg.js`) und je ein Anker auf den
  `<h2>`, damit `build-suchindex.py` dort Abschnitte schneiden kann.
- `rechtliches.html` — Haftung + Datenschutz, verlinkt aus Footer und Feedbackformular
  (bewusst **kein** eigener Headerpunkt). Kontakt läuft ausschliesslich über
  `feedback.html` („Kontakt & Feedback") — es gibt keine veröffentlichte E-Mail-Adresse.
- Pilot-/Referenzseite für jedes Skelett: `themen/p4-1-kinematik.html`.

## Kompetenzblock: Wortlaut aus dem RLP, Ausformulierung in den Lernzielen

Der Block `.rlp-kompetenzen` zuoberst auf jeder Themenseite ist ein **Zitat**:
der Wortlaut des Rahmenlehrplans, Zeile für Zeile, in seiner Reihenfolge, ohne
Kürzung und ohne Zusatz. Alles, was dieses Haus daraus macht — Formeln,
zusätzliche Teilfähigkeiten, die Ich-Form — steht in den `.lernziele` **direkt
darunter**. Dort darf über den RLP hinausgegangen werden, im Block nicht.

**Quelle:** SBFI, *Rahmenlehrplan für die Berufsmaturität*, 13.06.2025, in
Kraft seit 01.03.2026, Abschnitt **7.5.4.1 Gruppe 1**, S. 85–88. Der Auszug
liegt als `../physik.pdf` neben dem Arbeitsverzeichnis, nicht im Repo — das
vollständige PDF steht beim SBFI. 44 Kompetenzen in den Lerngebieten 4, 5 und 6.

**Zwei Fallen, beide am 08.09.2026 zugeschlagen** — Details und Belege in
STYLEGUIDE §4.1: Der RLP führt Physik **viermal**, je Berufsgruppe; verbindlich
ist Gruppe 1. Gruppe 3 sagt an derselben Stelle «Brennwert», wo Gruppe 1
«Heizwert» sagt. Und zwei tragende Halbsätze stehen im PDF in einem
Subset-Font, den keine naive Textextraktion mitliest — «das zweite
Newton’sche Gesetz in einfachen Fällen (…» und «das Pascal’sche Gesetz anhand
einfacher Aufgaben anwenden».

## Clips: Massstab ist der Kompetenzblock

Eine Clipreihe zu einer Lektion ist vollständig, wenn sie die **RLP-Kompetenzen
der Themenseite** abdeckt — nicht, wenn eine Stichwortliste abgearbeitet ist.
Der Block steht zuoberst auf jeder Seite der Lerngebiete 4 bis 6
(«📋 Kompetenzen nach RLP-BM 2030 …») und ist vor der Planung zu lesen; was
dort nicht steht, gehört auch nicht in die Reihe. Bauanleitung und Prüfliste:
`HOWTO-clips.md`.

## Querverweise ins Vorwissen

Jede Themenseite der Lerngebiete 4 bis 6 trägt direkt unter dem
Kompetenzblock einen `.block-tipp` **«💡 Vorwissen zu dieser Seite»** mit den
zwei bis drei Abschnitten, die sie voraussetzt — verlinkt als **Anker**
(`p0-2-vorwissen-physik.html#praefixe`), nicht als blosser Seitenlink.
Umgekehrt trägt jede der sechs Vorwissenseiten einen Kasten **«💡 Lieber
geführt durcharbeiten?»**, der auf das passende Leitprogramm zeigt und sagt,
was nur auf der Seite steht. Wer eine Seite neu anlegt oder einen Abschnitt
umbenennt, führt beides nach; die Anker sind Teil der Verabredung.

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
(Selbsttest von p0-4), dazu `check_clips` — die Clip-Ablage gegen `clips/clips.json`:
Clip ohne Eintrag, Eintrag ohne Datei, `lektion`-Code, den `nav.js` nicht kennt
(alle `[FEHLER]`), fehlender Sprechertext (`[WARN]`); Drehbücher mit `probe: true`
sind ausgenommen. Aus tals-mathe übernommen (26.09.2026). `verify_js_runtime.js` bekommt nur `themen/`-Seiten zu sehen —
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
| 8 | **Kein Gedankenstrich an einer Formel im Titel** — gerendert liest er sich als Vorzeichen. Vor der Formel: Doppelpunkt (nach `?`/`!` ersatzlos). Nach der Formel: Titel umstellen, Formel ans Ende. Nur direkter Kontakt zählt; Fliesstext bleibt. Gilt für `h2`, `h3`, `.block-titel`, `.aufg-titel-text`. **Ebenso kein Mittepunkt `·` direkt vor einer Formel** (liest sich als Malpunkt: `Animation 3 · \(R…\)`) — in Titeln und Knopfbeschriftungen durch Doppelpunkt ersetzen. | §2.9 |
| 9 | **Eine Rechnung, eine Zeile:** Formelzeichen = Formel = Zahlen mit Einheiten = Ergebnis als eine Kette in **einer** `.fl-eq`, nicht Formel und Zahlengleichung auf zwei Zeilen. Fehlt der Platz, Umbruch nur vor einem `=` (Glieder als Inline-Formeln, `flTex` aus `physiklib.js`). Verschiedene Rechnungen bleiben getrennte Zeilen. | §2.8 |
| 10 | **Werte und Bewegung in Animationen:** dieselbe Grösse überall mit derselben Rundung (Canvas, Live-Box, Formelzeile); Voreinstellungen und Geräteknöpfe treffen die Werte der Seite exakt (sonst Regler `step="any"`); kein Punkt, der ohne Anlass selbst durchs Diagramm wandert — Momentanwerte per Regler; Beschriftungen auf Kurven mit hellem Grund, bewegliche weichen festen aus. | §5.10 |

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
  **Playwright-Falle:** Die Option heisst `viewport`, nicht `viewportSize` —
  `newPage({ viewportSize: … })` wird stillschweigend ignoriert, die Seite läuft
  dann mit 1280 px, und jede «360-px-Messung» ist wertlos, ohne dass etwas
  auffällt. Im Zweifel `window.innerWidth` mitmessen. Die Werkzeuge in
  `.claude/tools/` machen es richtig; der Fehler passiert in schnell
  hingeschriebenen Prüfskripten.
- **Keine erfundenen Quellen, Zitate oder Lehrplan-Stellen.** Im Zweifel: „muss
  verifiziert werden" schreiben, nicht raten.

## Schwesterprojekt TALS Mathe — Übertrag per Todo, nicht direkt

Gespiegelt aus `tals-mathe/CLAUDE.md`, wo diese Regel seit Längerem steht. Sie
fehlte hier — und genau deshalb wurde sie am 13.09.2026 zweimal gebrochen
(Clip-Port und `abgleich.py`, beide aus einer Physik-Sitzung heraus nach Mathe
geschrieben). Beide Male stimmte das Ergebnis, aber der Weg war der falsche.
Jetzt steht die Regel auf beiden Seiten.

- **Lesen ja, schreiben nie.** Claude Code darf `../tals-mathe` jederzeit
  *lesen* — zählen, vergleichen, Zahlen für einen Übertrag holen. Geschrieben
  wird ausschliesslich in diesem Repo. Kein Edit, kein `git`-Befehl, kein
  Skriptlauf, der dort hineinschreibt.
- **Warum die Trennung nicht Vorsicht, sondern Struktur ist:** Der Harness lädt
  `CLAUDE.md` und `.claude/settings.json` des *primären* Arbeitsverzeichnisses.
  Aus einer Physik-Sitzung heraus gälten in Mathe also Physiks Konventionen,
  während Mathes eigene `CLAUDE.md` und `STYLEGUIDE.md` stumm blieben — und
  Mathe hat eigene (zwei Fächer statt flacher Lerngebiete, Blau statt
  Bernstein, andere Klassennamen, eigene deny-Liste). Dazu kommt: die
  Werkzeugskripte hier leiten ihr Wurzelverzeichnis aus dem eigenen Dateipfad
  ab (`ROOT = dirname(dirname(abspath(__file__)))`) und schreiben rekursiv —
  aus dem falschen Ordner aufgerufen patchen sie das falsche Repo, in
  `acceptEdits` ohne Rückfrage.
- **Auch `--root PFAD` ist Schreiben.** `build-suchindex.py` und
  `build-animationen.py` nehmen den Schalter und schreiben damit ins andere
  Repo. Erlaubt ist er nur zusammen mit `--dry-run` beziehungsweise `--check`.
- **`scripts/abgleich.py` liest nur** und ist darum ausdrücklich erlaubt. Sein
  `[WARN]` im Pre-Flight ist der Anlass für einen Todo-Eintrag, nicht für einen
  Quer-Edit.
- **Die Warteschlange steht in `scripts/abgleich.py`, Liste `OFFEN`.** Dort,
  weil beide Repos dieselbe Datei führen und sie in ihrer eigenen KERN-Liste
  mit Grundlinie `1.000` steht: Wer einen Eintrag hinzufügt, macht die Datei
  ungleich — das Schwesterrepo meldet beim nächsten Pre-Flight `[WARN]
  abgleich`, und `--diff scripts/abgleich.py` zeigt den neuen Eintrag. Die
  dortige Sitzung arbeitet ihn ab und übernimmt die Datei; alles Schreiben
  bleibt im eigenen Repo.
  **Eine lokale Notizdatei taugt dafür nicht.** Der erste Versuch am
  13.09.2026 legte `.quellen/todo-schwesterprojekt.md` an — per `.gitignore`
  ausgeschlossen, weil das Repo die veröffentlichte Website ist. Damit reiste
  sie nicht mit, und nichts in Mathe zeigte auf sie: ein Kanal, den die
  Gegenseite nie sieht. Wieder entfernt.
  Die Gegenrichtung läuft weiter über Mathes `TODO-schwesterprojekt.md` im
  Wurzelverzeichnis — dort ist eine versionierte Arbeitsdatei erlaubt. Vor
  einem Übertrag nach Physik dort nachsehen.
- **Ein guter Eintrag ist nachgezählt, nicht geschätzt.** Vor dem Schreiben im
  Mathe-Repo nachsehen und die konkreten Zahlen aufnehmen: wie viele Dateien
  betroffen sind, welche Sonderfälle es dort gibt, was dort anders heisst. Ein
  Eintrag, aus dem sich die Portiersitzung direkt abarbeiten lässt, ist die
  halbe Arbeit; einer aus Vermutungen kostet sie doppelt.

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
