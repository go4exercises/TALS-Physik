# HOWTO — Erklärclip bauen und einbauen

Ein Clip ist eine eigenständige HTML-Datei in `clips/`, die einen einzigen
Gedankengang in rund einer Minute aufbaut: animierte Zeilen auf einer Bühne von
1920 × 1080, dazu eine gesprochene Tonspur. Gebaut wird er nicht von Hand,
sondern aus einem **Drehbuch** — einer JSON-Datei daneben.

Stand 07.09.2026: **81 Clips, 74:42 min, in 22 Reihen** — jede Themenseite der
Lerngebiete 4 bis 6 hat ihre Reihe, dazu das Vorwissen. Verteilung nach
Lerngebiet (Mehrfachzuordnungen mitgezählt): Vorwissen 11, Mechanik 36,
Thermodynamik 28, Wellen und Elektrizität 18. Kürzester Clip 50 s, längster
64 s, Mittel 55 s. Diese Anleitung ist die Physik-Fassung; das
Schwesterprojekt Mathe hat eine eigene mit demselben Aufbau und 50 Clips.

> **Autoritativ bleiben CLAUDE.md und STYLEGUIDE.md.** Alles hier Beschriebene
> gilt zusätzlich, nichts davon hebt eine dortige Regel auf — Dezimalpunkt statt
> Komma, kein ß, Liter klein, Ansatz vor Zahlengleichung.

---

## Der Weg in fünf Schritten

```bash
# 1. Drehbuch schreiben:  clips/<lektion>-<name>.json   (Vorlage: clips/vorlage.json)

# 2. Vertonen — misst die Sprechdauer und schreibt sie ins Drehbuch zurück
export PIPER_MODELL=/home/paps/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py <name>

# 3. Bauen
python3 scripts/build-clips.py <name>          # ohne Argument: alle

# 4. Einbauen (Lektionsseite + clips.html + Transkript)
python3 scripts/build-clips-einbau.py --schreiben
python3 scripts/build-suchindex.py
python3 scripts/build-seo.py

# 5. Prüfen
node .claude/tools/pruef-clip.mjs clips/<name>.html 2 6 10 14 18 22 26 30 34 38 42 46 50
node .claude/tools/pruef-mathjax.mjs http://localhost:8912/clips/<name>.html
python3 .claude/skills/preflight/preflight.py themen/<lektionsseite>.html
```

**Die Reihenfolge ist nicht beliebig.** `build-clips-einbau.py` liest nur
`clips/clips.json` und baut selbst nichts; ohne vorherigen `build-clips.py`-Lauf
stehen in der Seite die alte Dauer und der alte Kurzbeschrieb. Und ohne
vorherige Vertonung schätzt der Generator die Szenendauer aus der Wortzahl —
danach sitzt das Bild nicht auf der Sprache.

---

## Das Drehbuch

### Kopf

| Feld | was |
|---|---|
| `titel` | Schema «Reihe: Fokus». Der Fokus ist die eine Frage, die dieser Clip beantwortet. |
| `kurzbeschrieb` | ein bis zwei Sätze für die Bibliothek — der Gedanke, nicht das Inhaltsverzeichnis |
| `lerngebiet` | `0 · Vorwissen`, `4 · Mechanik`, `5 · Thermodynamik`, `6 · …` — steuert die Gruppe in `clips.html` |
| `reihe` / `folge` | didaktische Familie und Platz darin; Clips einer Reihe stehen beieinander |
| `lektion` | **Liste** von Codes aus `nav.js` — auf diesen Seiten erscheint der Clip |
| `themenbereich` | steht klein rechts oben im Bild, z. B. `Thermodynamik · BM` |
| `theme` | `begreifbar` (Standard in diesem Projekt), sonst `heft`, `tafel`, `papier` |
| `stufe`, `schlagworte` | für Suche und Filter |
| `nachlauf` | Standzeit nach der letzten Einblendung; in diesem Projekt `4.0` |
| `probe: true` | baut den Clip, hält ihn aber aus `clips.json` heraus — für Versuche |

`lektion` ist eine Liste, weil ein Clip mehreren Seiten gehören darf. Er wird
dabei **einmal** gespeichert und mehrfach eingebunden: `p0-3-druck` steht auf
`p0-3`, `p0-2` und `p4-5`. Die Bibliothek zählt einzigartige Clips, nicht
Einbettungen.

### Der Szenenbau

Bewährt und in allen 79 Clips gleich:

| Szene | Layout | `oben` | Aufgabe |
|---|---|---|---|
| Titel | `zentriert` | 244 | das beobachtbare Phänomen und die Frage |
| Schritt 1 | `schiene` | **178** | der erste Begriff, meist die Definition |
| Schritt 2 | `schiene` | **430** | das Bild dahinter (Teilchen, Anschauung) |
| Schritt 3 | `schiene` | **430** | das Gesetz |
| Schritt 4 | `schiene` | **430** | ein durchgerechnetes Beispiel |
| Merksatz | `zentriert` | 248 | ein Satz, der bleibt — plus zwei Randnotizen |

Die `schiene` ist der Merkweg links: vier Einträge, der aktuelle hervorgehoben,
die anderen gedämpft. Sie kommt aus dem Feld `schiene` im Kopf und braucht in
jeder Schritt-Szene das Feld `schritt: 1…4`.

### Das Band oben — der Anschluss an den letzten Schritt

Das Schienen-Layout beginnt bei `oben: 168`. Trotzdem stehen die Schritte 2 bis 4
auf `430`. **Das dazwischenliegende Band ist kein Zufall und keine Lücke: Dort
steht, woran der laufende Schritt anknüpft.**

Zwei Mechanismen füllen es, und sie sind nicht dasselbe:

| | `halten` | `mitnehmen` |
|---|---|---|
| Schreibweise | `"halten": "Schritt 2 · Name"` oder `true` | `"mitnehmen": true` |
| Wirkung | Element bleibt **an seinem Platz** stehen | Element erscheint in der **nächsten** Schritt-Szene noch einmal, oben im Band |
| passt für | Schritt 1 — er steht ohnehin schon oben | jeden späteren Schritt |

Ohne das eine oder das andere ist beim Szenenwechsel weg, was der nächste
Schritt gerade einsetzt. Auf der Schiene steht dann zwar noch, *dass* es einen
Schritt davor gab, aber nicht mehr, *was* er ergeben hat — und das
**Ansatz-Prinzip ist im Bild nicht mehr zu sehen**: Die Zahlengleichung steht
allein da, die Formel, aus der sie kommt, ist verschwunden.

Die Regel lautet darum:

> **Wo ein Schritt die Formel des vorherigen einsetzt, trägt jene Formel
> `mitnehmen: true`.** Das betrifft vor allem den Übergang «Das Gesetz» →
> «Ein Beispiel».

`mitnehmen` setzt das Element an den Kopf der nächsten Szene (links 680, oben
168), gleich wo es vorher stand, und blendet es dort weich ein. Es wirkt nur,
wenn die nächste Szene das Layout `schiene` hat; sonst meldet der Generator eine
Warnung und lässt es weg.

**`halten` erreicht das Band nur vom ersten Element des ersten Schritts aus.**
Ein Element weiter unten in der Szene behält beim Halten seine eigene Höhe — bei
der dritten Zeile sind das rund 420 px, und dort beginnt schon der Inhalt der
nächsten Szene. Für alles ausser der ersten Zeile ist `mitnehmen` das richtige
Werkzeug.

Mehr als **eine** Zeile gehört nie ins Band. Sie ist der Faden, nicht die
Zusammenfassung. Und das Band bleibt leer, wo der Faden nur begrifflich läuft:
Dass es einen Schritt davor gab, sagt die Merkschiene links ohnehin. Ins Band
gehört nur, was der laufende Schritt **einsetzt oder fortschreibt** — sonst
steht dort Dekoration.

### Elementtypen

| Typ | wofür | Standardgrösse |
|---|---|---|
| `titel` | Handschrift-Titel der Titelszene | 132 |
| `untertitel` | ein Satz darunter, blau | 48 |
| `aussage` | der Merksatz der Schlussszene | 116 |
| `formel` | Formelzeile — Ansatz, Zahlengleichung, Ergebnis | 56 |
| `text` | Fliesstext, erklärt die Formel darüber | 50 |
| `notiz` | Handnotiz; `farbe`: `blau`, `rot`, `gruen`, `tinte` | 52 |
| `box` | gerahmtes Ergebnis, `farbe: gruen` für die Lösung | — |
| `karte` | gerahmter Zwischenschritt | 42 |
| `liste` | nummerierte Merkliste, braucht `punkte: [...]` | — |
| `strich` | roter Unterstreichungsstrich | — |

Gemeinsame Felder: `abstand` (Abstand zur nächsten Zeile in Pixel), `groesse`,
`anim` (`rise`, `pop`, `fade`, `wipe`), `ein` (Sekunde in der Szene; ohne Angabe
im Takt von 1.7 s gestaffelt), `x`/`y` für eine eigene Position, `breite`.

### Formeln und Farben

Formeln stehen in LaTeX (`"latex": true` ist Standard), wie auf den
Lektionsseiten — eine Formel lässt sich von dort kopieren. Gesetzt wird mit dem
lokalen MathJax aus `vendor/mathjax/tex-svg.js`; der Paketumfang von `tex-svg`
schliesst `ams` ein, `\xrightarrow` und `\rightleftharpoons` funktionieren also.

Vier Farbgruppen führen einen Term durch den ganzen Clip:

```
\fa{…}  \fb{…}  \fc{…}  \fd{…}
```

In der Reihe «Ideale Gase» steht durchgehend `\fa` für den Druck, `\fb` für das
Volumen, `\fc` für die Temperatur und `\fd` für das Ergebnis. Wer eine solche
Zuordnung je Reihe festlegt und durchhält, macht sichtbar, was von
wo nach wo wandert. Sparsam bleiben — ein Bild mit sechs Farben erklärt nichts
mehr.

In Prosa-Typen (`text`, `notiz`, …) steht eine eingebettete Formel in `@…@`,
ein Zeilenumbruch als `|`, gedämpfter Text in `~…~`. **Auch in der `schiene`.**

---

## Ton

**Stimme: `de_DE-thorsten-high`, verbindlich** (Datensatz Thorsten-Voice, CC0 —
dieselbe wie in Mathe). Kein Stimmmodell gehört ins Repo.

```bash
export PIPER_MODELL=/home/paps/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py <name>
```

Das Skript erzeugt **eine** MP3 je Clip unter `clips/ton/<name>.mp3` und schreibt
die gemessene Sprechdauer je Szene als `dauer` ins Drehbuch zurück. Der Clip
referenziert die Datei extern (`src="ton/<name>.mp3"`); nur `--eigenstaendig`
giesst sie als base64 hinein. Das ist mit Absicht so: Eine Seite, die eine
Minute Ton als Datei-URI mitschleppt, wächst um rund 300 kB, die vor dem ersten
Buchstaben geladen werden.

**Der Ton startet hörbar — und das hängt an zwei Stellen.** Der Clip setzt beim
Laden `muted = false` und ruft `play()`. Erlaubt ist das nur, weil der Klick auf
die Clipkarte die nötige Nutzergeste war **und** das `<iframe>` sie über
`allow="autoplay"` weitergereicht bekommt; gesetzt wird das Attribut in
`clipRahmen` in `physiklib.js`, also für alle drei Wege zugleich — Lektionsseite,
Bibliothek und Leitprogramm. Fehlt es, verweigert der Browser den Ton im Rahmen,
obwohl geklickt wurde.

Schlägt `play()` trotzdem fehl — etwa wenn jemand die Clipdatei direkt aufruft,
ohne vorher irgendwo zu klicken —, schaltet der Clip auf stumm und spielt weiter;
sichtbar wird das am Knopf, der dann «🔇 Ton an» statt «🔊 Ton aus» zeigt. Prüfen
lässt sich beides nur mit strenger Autoplay-Regel, sonst erlaubt der Testbrowser
ohnehin alles:

```bash
chromium --autoplay-policy=document-user-activation-required
```

**Zahlen im `sprecher`-Text ausschreiben.** Beide Piper-Stimmen lesen `1.62` als
zusammengesetzte Zahl («… zweiundsechzig») statt als Stellenfolge — bei
Messwerten ist die Stellenfolge die übliche Lesart. Also «zwei Komma fünf bar»,
nicht «2.5 bar». In den sichtbaren Elementen steht selbstverständlich die Ziffer.

---

## Einbauen

`build-clips-einbau.py` schreibt zwischen die Marker — von Hand gepflegt wird
nur, was ausserhalb steht:

| Datei | Marker |
|---|---|
| Lektionsseite | `<!-- CLIPS:ANFANG … -->` … `<!-- CLIPS:ENDE -->` |
| `clips.html` | `<!-- CLIPS-BIBLIOTHEK:ANFANG … -->` … `<!-- CLIPS-BIBLIOTHEK:ENDE -->` |

**Eine Seite, die noch nie einen Clip hatte, hat den Marker nicht.** Das Skript
meldet dann `[WARN] pX-Y hat 1 Clip(s), aber keine CLIPS-Marker` und lässt die
Seite in Ruhe. Das leere Markerpaar gehört von Hand hinein, direkt vor
`</main>`; den `<h2 id="clips">Clips</h2>` bringt der Generator selbst mit.

Der Block enthält je Clip eine Startkarte und darunter das **Transkript** aus
`clips/sprechertext-*.txt`. Das Transkript ist kein Beiwerk: Von einem animierten
Clip sieht eine Suchmaschine nichts, und die Volltextsuche der Site ebenso wenig.

In der **Volltextsuche** steht jeder Clip einzeln: `build-suchindex.py` legt je
Clip einen Eintrag aus Kurzbeschrieb, Transkript und Stichworten an und zielt auf
`clips.html#clip-<name>`; die Bibliothek klappt beim Ankommen sein Lerngebiet auf
und legt einen Ring um die Zeile. Darum indexiert der Generator den
Transkript-Aufklapper der Lektionsseite (`.clip-transkripte`) **nicht** mehr —
sonst fände man denselben Satz zweimal, und der zweite Treffer führte nur auf
eine Seite mit zwanzig Clips. Die Zeile in der Bibliothek trägt dafür ihre ID;
vergeben wird sie beim **ersten** Vorkommen, denn ein Clip zweier Lerngebiete
steht zweimal in der Liste.

Ein Clip lädt nie beim Seitenaufruf — sichtbar ist zuerst nur der Startknopf,
erst der Klick setzt das `<iframe>` ein (`clipStart` in `physiklib.js`).
Leitprogramme benutzen dieselbe Bühne über `clipBuehne`; wer an ihr etwas
ändert, ändert es dort mit.

---

## Prüfen

| Werkzeug | sieht |
|---|---|
| `pruef-clip.mjs <datei> <sekunden…>` | Überlappungen und alles, was über die Bühne hinausragt — je Zeitmarke |
| `pruef-mathjax.mjs <url>` | ob wirklich jeder Ausdruck gesetzt wurde und keine TeX-Erweiterung fehlt |
| Pre-Flight | die Lektionsseite, in der der Clip steckt |

`pruef-clip.mjs` braucht eine **dichte** Folge von Zeitmarken — alle 2 bis 4
Sekunden. Eine Überlappung entsteht erst, wenn das letzte Element einer Szene
eingeblendet ist; wer nur drei Marken setzt, trifft sie nicht. Die Bilder legt
das Werkzeug in `$SP` ab; ohne gesetzte Variable landen sie im
Arbeitsverzeichnis — im Repo-Wurzelverzeichnis liegen aus einem solchen Lauf
sechs versehentlich versionierte `szene-*.png`.

`pruef-mathjax.mjs` braucht eine ausgelieferte Seite, nicht `file://`:

```bash
python3 -m http.server 8912 --directory /home/paps/tals-physik &
node .claude/tools/pruef-mathjax.mjs http://localhost:8912/clips/<name>.html
```

Das ist nicht dasselbe, was `verify_mathjax.js` im Pre-Flight tut: Jenes setzt
mit `mathjax-full` aus `node_modules` und schaut nie in `vendor/`. Fehlt dort
eine nachgeladene Erweiterung, bleibt die **ganze Seite** ohne Formelsatz, ohne
Fehlermeldung im Bild.

---

## Häufige Stolpersteine

**LaTeX in der Merkschiene braucht `@…@`.** Die Einträge des Feldes `schiene`
gehen durch `text_html`, nicht durch den Formelsatz. `"Die Formel|~\\Delta l =
\\alpha l_0 \\Delta T~"` erscheint darum als roher Quelltext im Bild — so stand
es fünf Tage lang in `p5-3-ausdehnung-feststoffe`. Richtig ist
`"Die Formel|~@\\Delta l = \\alpha\\, l_0\\, \\Delta T@~"`.

**Zu lange `text`-Zeilen kollidieren mit der Notiz darunter.** Im
Schienen-Layout (Breite 1140) bricht eine Zeile bei Grösse 52 nach rund **55
Zeichen** um, im Layout `zentriert` (Breite 1660) nach rund **70**. Ein
`abstand: 150` reicht für **eine** Zeile; die zweite braucht rund 70 px mehr.
Entweder kürzen oder `abstand: 220` setzen. Der Fehler ist im Drehbuch nicht zu
sehen — nur `pruef-clip.mjs` meldet ihn.

**Eine Formelzeile bricht nicht um — sie läuft aus dem Bild.** `formel`, `box`
und `karte` tragen `white-space:nowrap`. Wird die Zeile zu lang, wächst sie über
ihren 1140 px breiten Container hinaus und im Zweifel über die Bühne; sichtbar
bleibt, was links von 1920 px steht, der Rest ist weg. Faustwerte für die
Textspalte (680 bis 1820 px): bei Grösse 50 rund **34 Zeichen** Formeltext, bei
Grösse 42 rund **40**. Eine Aufzählung mit vier Einträgen ist meist die Grenze —
sonst zwei `formel`-Zeilen daraus machen oder die Grösse senken.

`pruef-clip.mjs` hat das bis zum 07.09.2026 **nicht** gemeldet: Es mass den
Container, und der bleibt 1140 px breit, egal was herausragt. Seit dem misst es
den Inhalt; zehn abgeschnittene Zeilen in fünf Clips kamen bei der Umstellung
zum Vorschein.

**`<` und `>` gehören als `\lt` und `\gt` ins Drehbuch.** Der Formelsatz
maskiert selbst; ein direkt geschriebenes `<` wird zu `&lt;` und MathJax bricht
daran ab. Für `≤` und `≥` schreibt man `\le` und `\ge`.

**Brüche gibt es nur in Formel-Elementen.** `formel`, `karte` und `box` schicken
ihren ganzen Text durch den Formelsatz. In `text` oder `notiz` gehört eine
Formel in `@…@`; ein `|` darin würde sonst zuerst zum Zeilenumbruch.

**Eine gehaltene Zeile belegt das Band oben.** Wer `halten` benutzt, muss die
Folgeszenen tiefer beginnen lassen (`oben: 430`), sonst rendern beide
übereinander. Dasselbe gilt für `mitnehmen`.

**Der Clip liegt genau eine Ebene unter der Wurzel.** Er zieht Schriften und
MathJax über `../`. Verschiebt man `clips/` tiefer, fallen die Schriften still
auf eine Systemschrift zurück.

**`\,\mathrm{l}` neben einer mehrstelligen Zahl liest sich als Ziffer.**
`2207\,\mathrm{l}` sieht aus wie «22071». Der Liter bleibt klein (STYLEGUIDE
§2.3) — aber wo es eng wird, lieber in `\mathrm{m^3}` angeben oder die
Farbfläche die Gruppierung tragen lassen.

**Nach jedem Drehbuch-Edit alle vier Skripte**, in dieser Reihenfolge:
`build-clip-ton.py` (nur wenn sich der Sprechertext geändert hat) →
`build-clips.py` → `build-clips-einbau.py --schreiben` → `build-suchindex.py` →
`build-seo.py`.

---

## Der Massstab: die RLP-Kompetenzen der Seite

**Bevor eine Clipreihe geplant wird, wird der Kompetenzblock der Themenseite
gelesen.** Er steht ganz oben auf jeder Seite der Lerngebiete 4 bis 6:

```
📋 Kompetenzen nach RLP-BM 2030 · Lerngebiet 4.1 · 100 Lektionen
```

Darin steht wörtlich, was der Rahmenlehrplan verlangt — und genau das ist der
Massstab für die Vollständigkeit einer Reihe, nicht eine Stichwortliste und
nicht die Abschnittsfolge der Seite. Die Prüfung ist eine Tabelle: jede
Kompetenz in eine Zeile, daneben der Clip, der sie trägt. Bleibt eine Zeile
leer, fehlt ein Clip.

Am 07.09.2026 hat dieser Schritt gefehlt, und es zeigte sich sofort, was das
kostet: In 4.1 fehlten die parabolische Bewegung, die Kreisbewegung und die
Relativbewegung in Vektor-Form — alle drei stehen wörtlich im RLP —, dazu die
Begriffe Schwerpunkt und Bahnkurve. In 4.2 fehlte das Hookesche Gesetz, in 5.2
der Vergleich der Energiesysteme. Sechs Clips, die niemand vermisst hätte, weil
die Reihe für sich rund aussah.

Umgekehrt begrenzt der Block auch: Was dort nicht steht, gehört nicht in die
Reihe. Brechung, Beugung und Interferenz etwa kommen in den Kompetenzen zu 6.1
nicht vor — darum stehen sie auch nicht auf der Themenseite, und darum braucht
es keine Clips dazu.

Ein Clip darf mehrere Kompetenzen bedienen und eine Kompetenz mehrere Clips
brauchen. Wo eine Kompetenz schon von einem Clip einer anderen Lektion getragen
wird, bekommt jener einen Eintrag mehr in `lektion` — kein zweiter Clip mit
demselben Lernziel.

---

## Didaktische Prüfliste

Für jeden neuen Clip. Die ersten drei Punkte prüft der Generator mit, der Rest
ist Handarbeit.

| # | Anforderung | prüfbar |
|---|---|---|
| 1 | **Genau ein physikalischer Kerngedanke** | am Titel: Passt er in «Reihe: eine Frage»? |
| 2 | **45–90 Sekunden** (Bestand: 54–68 s) | Summe der `dauer` nach der Vertonung |
| 3 | Schluss mit einem kurzen **Merksatz** | Schlussszene mit `typ: "aussage"` |
| 4 | Start mit einem **beobachtbaren Phänomen** | Titelszene: Daumen und Nadel, Ballon im Gefrierschrank, Flasche auf der Waage |
| 5 | Erst Vorstellung und Alltag, dann Fachsprache und Formel | Reihenfolge der Schritte |
| 6 | Mindestens **ein konkretes Beispiel**, durchgerechnet | Schritt 4 |
| 7 | **Ansatz vor Zahlen** — Formel symbolisch, dann Werte einsetzen | zwei `formel`-Zeilen; die erste steht per `mitnehmen` noch im Band |
| 8 | **Werte mit Einheit** einsetzen, nicht nur Zahlen | jede Zahlengleichung |
| 9 | **Modellannahmen aussprechen** | «ideales Gas», «starre Wand», «feste Gasmenge» |
| 10 | **Näherungen als Näherungen** kennzeichnen | «nahezu», «rund», «im Modell gerechnet» |
| 11 | **Keine absolute Formulierung, wo Ausnahmen existieren** | «die meisten Stoffe», nicht «Stoffe» |
| 12 | Bedingung nennen, unter der eine Formel gilt | in Klammern hinter der Formel: `(T konstant)` |
| 13 | Symbol, Grösse und Einheit sauber trennen | `\fa{p}` gegen `\text{in Pa oder bar}` |
| 14 | Eine **typische Fehlvorstellung** aufgreifen, wo es sich anbietet | «Eis ist leichter», «Strom wird verbraucht» |
| 15 | Diagramme und Animationen **kausal** aufbauen | Ursache links, Folge rechts; `\Longrightarrow` statt Aufzählung |
| 16 | Prüfen, ob es **schon einen Clip mit demselben Lernziel** gibt | `clips.json` nach `reihe` und `schlagworte` durchsehen |
| 17 | Der Clip muss **allein verständlich** sein, nicht nur im Leitprogramm | Er wird über `clips.html` gefunden, ohne Vorgeschichte |
| 18 | Die **RLP-Kompetenzen** der Lektion sind von der Reihe vollständig abgedeckt | Kompetenzblock der Themenseite gegen die Clipliste stellen (siehe oben) |

Punkt 17 ist der Grund, warum es keine zweite Sorte Clip gibt. Was im
Leitprogramm gebraucht wird, ist ein gewöhnlicher Clip aus `clips/` — nichts,
was nur dort funktioniert und nur dort gespeichert ist.

---

## Bibliotheksseite `clips.html`

Gruppiert nach **Lerngebiet**, darin nach **Reihe**, darin nach `folge`. Anders
als in Mathe gibt es keine Trennung in Grundlagen- und Schwerpunktfach. Die
Lerngebiete sind beim Laden zugeklappt; die Kopfzeile nennt Anzahl und
Gesamtdauer — gezählt werden **einzigartige Clips**, nicht Einbettungen.

Über der Liste steht eine **Sofortsuche**: Sie vergleicht die getippten Wörter
mit `data-suche` an jeder Zeile — Titel, Reihe, Kurzbeschrieb, Schlagworte und
Lektionsnummer, alles klein geschrieben, mehrere Wörter UND-verknüpft. Lerngebiete
mit Treffern klappen dabei auf, leere verschwinden. Wer denselben Clip in zwei
Lerngebieten sieht, erkennt das an der Zeile «↳ auch in 4.5 Hydrostatik»
darunter; gebaut wird beides in `build-clips-einbau.py` (`suchtext`, `auch_in`).
