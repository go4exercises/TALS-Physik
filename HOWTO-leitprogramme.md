# HOWTO — Leitprogramme

**Gilt seit 03.10.2026.** Was in ein Leitprogramm gehört, in welcher Reihenfolge, und wie es
technisch ins Repo kommt — für die Art «nach Thema». Die Art «Übungsprüfung» hat ihre eigene
Anleitung (`HOWTO-uebungspruefung.md`); Layout, Gerüst und Eintragen (§6, §11–§13) gelten für
beide. Bei Widerspruch gilt `STYLEGUIDE.md` §6.5.

Übernommen aus der Gesamtfassung in `tals-mathe/HOWTO-leitprogramme.md` (Stand 03.10.2026,
dort entstanden am 30.09.–02.10.2026 und erprobt an `leitprogramme/quadratische-funktionen.html`
und `lineare-funktionen.html`) und an Physik angepasst. Die frühere technische Physik-Fassung
(«ein Leitprogramm ins Repo holen», 385 Zeilen) ist darin aufgegangen: Ihre zwölf Punkte mit
Fehlerbild stehen unverändert in §12, ihre Erfahrungen aus den elf klassischen Leitprogrammen
in §16. Wo die Fassung bewusst von einem Vorgänger abweicht, steht es als **⟂ Entscheid** dabei;
die Vorgänger stehen in der Git-Geschichte.

**Was für die bestehenden Leitprogramme gilt:** Die **elf klassischen Physik-Leitprogramme** bleiben,
wie sie sind. Sie sind im Format «klassisch» gebaut (§3) — von Hand, ohne Generator, mit HTML-Gesamttest.
Die Fassung gilt für **neue** Leitprogramme. Ob die bestehenden HTML-Gesamttests auf PDF
umgestellt werden (§9), ist ein **offener Entscheid des Auftraggebers**.

**Vorbild für ein neues Leitprogramm:** `leitprogramme/leitprogramm-elektrizitaet.html`, das erste
Physik-Leitprogramm nach dem Kapitelmuster (§4), gebaut mit `scripts/lp/elektrizitaet/seite.py`
(03.10.2026, nach `/lp-pruefung` freigeschaltet; was die Prüfung fand, steht in der Prüfliste §15). Vorbild in Mathe: `leitprogramme/quadratische-funktionen.html`
und `lineare-funktionen.html`. Ein neues Leitprogramm beginnt mit einer Kopie von
`scripts/lp/elektrizitaet/` (§5).
**Vor der Freischaltung:** unabhängige Prüfung nach §15 (`/lp-pruefung`).

---

## 0 · Zwei Arten, ein Layout

| | gegliedert nach | Beispiele | Anleitung |
|---|---|---|---|
| **Thema** | dem Stoff: Vorwissen, Kapitel (bzw. Schritte), Gesamttest | Kapitelmuster: `leitprogramm-elektrizitaet`; klassisch: `leitprogramm-waermemenge`, `leitprogramm-schaltungen` | diese Datei |
| **Übungsprüfung** | dem Prüfungsbogen: je Aufgabe Clip, Musterlösung, Fehlerkasten | `uebungstest-waermelehre` | `HOWTO-uebungspruefung.md` |

Layout, Kopf, Fuss, Farbtokens und Clip-Bühne sind bei beiden dieselben (§11–§12 gelten
für beide).

---

## 1 · Grundsatz: RLP → Themenseite → Leitprogramm

Drei Ebenen, jede begrenzt die nächste:

1. **Der RLP bestimmt, *was* gelernt wird — und wie die Begriffe heissen.** Quelle: SBFI,
   *Rahmenlehrplan für die Berufsmaturität*, 13.06.2025, Abschnitt **7.5.4.1 Gruppe 1**,
   S. 85–88; der Auszug liegt als `../physik.pdf` neben dem Arbeitsverzeichnis (nicht im
   Repo). Verbindlich ist **Gruppe 1** — der RLP führt Physik viermal, und die Gruppen
   unterscheiden sich im Wortlaut (STYLEGUIDE §4.1). Ein Leitprogramm deckt die
   **fachlichen Kompetenzen genau eines Teilgebiets** ab (z. B. 5.2 oder 6.2) oder einer
   klar benannten Teilmenge davon — und **nichts darüber hinaus**. Für das Vorwissen
   (Lerngebiet 0) gibt es keinen RLP-Abschnitt; dort begrenzt die Vorwissenseite.
2. **Die Themenseite bestimmt, *wie* es aussieht:** Notation, Formelzeichen, Einheiten,
   Vorzeichenkonventionen, Achsen, Konstanten, Merksätze, Beispiele. Das Leitprogramm
   erfindet nichts Eigenes.
3. **Das Leitprogramm bestimmt nur den Weg:** Reihenfolge, Umfang, Tests.

### 1.1 Bindung an den RLP

- **Kompetenzliste wörtlich übernehmen.** Die Kompetenzen des Teilgebiets stehen
  wörtlich (1:1 wie im Block `.rlp-kompetenzen` der Themenseite) als Kommentarblock im
  Kopf der Leitprogramm-Datei und nummeriert (K1, K2, …) in der Planung (§2). Achtung:
  Zwei tragende Halbsätze stehen im PDF in einem Subset-Font, den keine naive
  Textextraktion mitliest (STYLEGUIDE §4.1) — den Wortlaut aus dem Kompetenzblock der
  Themenseite nehmen, nicht frisch aus dem PDF ziehen.
- **Jedes Kapitelziel gehört zu mindestens einer Kompetenz**, und jede Kompetenz des
  Teilgebiets zu mindestens einem Kapitel. Ein Ziel ohne Kompetenz fliegt raus; eine
  Kompetenz ohne Kapitel wird im Kopf ausdrücklich ausgeschlossen («nicht in diesem
  Leitprogramm: … → eigenes Leitprogramm / Themenseite»).
- **Vorwissen darf aus früheren Teilgebieten stammen** (mit Nummer, z. B. «4.1») und aus
  dem Vorwissen (Lerngebiet 0), aber nicht aus späteren Teilgebieten.
- **Was die Themenseite über den RLP hinaus bietet, bleibt dort** — Zusatzverfahren,
  Exkurse, Vertiefungen. Im Leitprogramm höchstens als Satz «Mehr dazu auf der
  Themenseite».
- **Hilfsmittel.** In Mathe ist der RLP-Vermerk «auch ohne Hilfsmittel» verbindlich für
  den Gesamttest. Der Physik-Auszug (Gruppe 1, `../physik.pdf`) enthält keinen solchen Vermerk
  (Textsuche nach «Hilfsmittel», 03.10.2026 — wegen der Subset-Font-Falle beim ersten
  Leitprogramm von Auge gegenlesen). Darum gilt: Taschenrechner und
  Formelsammlung sind die üblichen BM-Hilfsmittel (STYLEGUIDE §1), und die Hilfsmittel
  stehen im Kopf des Gesamttests, je Teil.
- **Zuordnung sichtbar machen.** Jedes Kapitel trägt in `.kap-meta` die RLP-Nummer
  (`5.2`) und die Kompetenz-Kürzel (`K1 · K2`); die Selbsteinschätzung verweist von
  Testteil über Kapitel auf die Kompetenz.

⟂ Entscheid (aus Mathe): Eine frühere Didaktik-Fassung sagte «keine Inhalte, die *weder*
auf der Themenseite *noch* im RLP stehen» — damit war alles erlaubt, was irgendwo auf der
Themenseite steht. Jetzt gilt: RLP **und** Themenseite.

### 1.2 Themenseite als fachliche Wahrheit

Variation zwischen den beiden Spuren ist erlaubt, wenn sie eine Funktion hat (anderes
Format, weniger Regler, anderer Kontext). Zufällige Abweichung ist ein Fehler.
**Prüfkriterium:** Lässt sich in einem Satz sagen, *warum* das Leitprogramm es anders
macht? Ja → bleibt, und der Satz steht als Kommentar im Code. Nein → angleichen.

| | Themenseite | Leitprogramm |
|---|---|---|
| Rolle | Referenz: nachschlagen, erkunden, im Unterricht zeigen | geführter Pfad: selbstständig erarbeiten, nachholen |
| Umfang | ganzes Teilgebiet, samt Exkursen | die RLP-Kompetenzen, ausdrücklich abgegrenzt |
| Reihenfolge | nach Sachlogik, springbar | linear, jeder Schritt baut auf dem vorigen auf |
| Animationen | offen, mehrere Regler | Erkundungsauftrag mit einer Frage |
| Übungen | Mini-Checks, Aufgaben A1–A6 | Vortest, Selbsttests mit Punkten, Gesamttest |

Die Themenseite verweist zurück: Kasten **«💡 Lieber geführt durcharbeiten?»** (§13).

---

## 2 · Planung (Pflicht, vor dem HTML)

Aus RLP, Themenseite, Clips und Styleguide entstehen vier Dinge:

**a) Kompetenzmatrix**

```
Kompetenz (RLP, wörtlich gekürzt) | Hilfsmittel | Kapitel | Selbsttest-Aufg. | Gesamttest-Aufg.
```

**b) Planungstabelle**

```
Kapitel | Lernziel («Du …») | Kompetenz | Clip(s) | Erkundung (Anker) | Beispiel (Quelle) | Häufiger Fehler | min
```

**c) Kern / Vertiefung / bewusst weggelassen.** Was weggelassen wird, steht später im
Leitprogramm als «Nicht in diesem Leitprogramm → Themenseite, Abschnitt …». Kern und
Vertiefung tragen in den bestehenden Physik-Leitprogrammen die Marken `.task-id .kern`
und `.task-id .vert` — dieselben Klassen weiter verwenden, nicht neu erfinden (und nicht
mit der Vertiefungsaufgabe der Themenseiten vermischen).

**d) Konventionen und Widersprüche.** Liste der Begriffe, Formelzeichen, Einheiten,
Vorzeichen, Achsen der Themenseite — und alles, was sich **in der Themenseite selbst**
widerspricht (Text gegen eigene Clips, Tabelle gegen Mini-Check, Animation gegen
Animationsclip). Widersprüche werden **nicht** ins Leitprogramm übernommen, sondern
gemeldet und zuerst in der Themenseite entschieden. Wo das Leitprogramm trotzdem schon
entstehen soll: die Konvention der Themenseite nehmen (nicht die des Clips) und die
Abweichung im Text in einem Satz benennen.

⟂ Entscheid (aus Mathe): Die Didaktik-Fassung verlangte, die Planungstabelle **vor**
jeder Zeile HTML vorzulegen; `CLAUDE.md` verlangt, klare Aufträge direkt umzusetzen.
Jetzt: Die Planung steht als HTML-Kommentar im Kopf der Datei und im Bericht (§14).
**Vorgelegt und abgewartet** wird nur, wenn (d) einen Widerspruch enthält, der ein
Kernkapitel betrifft, oder wenn eine RLP-Kompetenz sich nicht im Zeitrahmen von §3
unterbringen lässt.

---

## 3 · Umfang und Zeit

- **Eine Lektion = 45 Minuten.** Die Minuten der Kapitel (inkl. Vorwissen und
  Gesamttest) werden addiert; die Summe bestimmt die Lektionenzahl im Kopf. «Zwei
  Lektionen» bei 130 Minuten ist falsch.
- **Zielgrösse nach Format** (Entscheid Auftraggeber Mathe 03.10.2026, übernommen):

  | Format | Kapitel | Gesamt |
  |---|---|---|
  | **Kapitelmuster** (§4; Einführungsclip → Animation → Kontrollclip → Übungen → Aufgaben; Vorbild in Mathe *Quadratische Funktionen*) | 4–5 Kapitel, je 35–45 Minuten — ein Kapitel ≈ eine Lektion | bis 5 Lektionen plus Vorwissen und Gesamttest |
  | **klassisch** (die elf älteren Physik-Leitprogramme) | 4–7 Schritte, je höchstens 30 Minuten | 2–3 Lektionen plus Vorwissen und Gesamttest |

  Ein Kapitel = eine Idee, in beiden Formaten.
- **Clips:** rund 6–11 Clips, 8–12 Minuten Clipzeit (STYLEGUIDE §6.5).
- **Über der Zielgrösse (klassisch mehr als 4, Kapitelmuster mehr als 5 Lektionen ohne
  Gesamttest) oder deutlich mehr als 11 Clips → teilen**, jedes Teil mit eigenem
  Vorwissen und Gesamttest. Physik hat das früh so gehalten: Wärmemenge, Heizen,
  Wärmeausdehnung und ideale Gase sind vier Leitprogramme, nicht eines.
- Der Kern ist, was ohne Leitprogramm in der Prüfung fehlen würde. Parameter,
  Spezialfälle, zweite Methoden → «Vertiefung» oder Themenseite.

⟂ Entscheid: Die klassischen Physik-Leitprogramme haben vier bis sieben Schritte
(`leitprogramm-widerstand-leistung` sieben); das bleibt. Für das Kapitelmuster gilt **4–5**.

---

## 4 · Aufbau der Seite

```
Kopf          Titel · Standfirst · Lerngebiet + Teilgebiet (RLP) · Lektionen
Ablauf        Kapitelliste nach Lektionen, Fortschrittszähler      (Schiene links)
So arbeitest  ① Erfahren → ② Clip → ③ Verallgemeinern → ④ Üben (ohne Lösung) → abhaken
Kompetenzen   RLP-Liste des Teilgebiets, K1…Kn; Abgrenzung
Kapitel 0     Vorwissen: kurze Klärung + Vortest (Verweis auf Vorwissens-LP/Vorwissenseite)
Kapitel 1…n   je: Lernziel · ① Erfahren (Simulation) · ② Clip · ③ Verallgemeinern
              (Formel, Definition, Beispiel nach Ansatz-Prinzip, Häufiger Fehler) ·
              Ausführlich-Link · ④ Üben
Gesamttest    Teile A/B/C ↔ Kapitel ↔ Kompetenzen · Hilfsmittel je Teil · Punkte
Einschätzung  Punktebereiche → konkrete Rückverweise auf Kapitel
Weiter        nächstes Leitprogramm · Themenseite · bewusst Weggelassenes
```

### Innerhalb eines Kapitels: das Kapitelmuster (Mathe, Fassung 3, 02.10.2026)

In Physik erstmals am Leitprogramm Elektrizität umgesetzt (03.10.2026). Die Seite entsteht aus
einer Kapitelbeschreibung (`scripts/lp/elektrizitaet/seite.py`), damit es überall gleich bleibt.
Übernommen aus Mathe ist das Gerüst — Koordinatensystem `Achsen()`, die Aufgabenleiste
`Leiste()`, der Übungsrahmen mit `lesen()`/`pruefen()`/`loesung()`, die Minigrafen; neu für
Physik sind die Bedienung mit Knopfgruppen (`Bedienung()`, `sim.setze()`), die Übungstypen
(`TYPEN`, je mit `fehler()` für `pruef-uebungen`) und die Simulationen. Was dabei anders wurde
und warum: `scripts/lp/elektrizitaet/README.md`.

Phasen (`<p class="phase">`) über den Abschnitten — **kein** Fahrplan unter dem Kapiteltitel.
«So arbeitest du» und die RLP-Kompetenzen stehen oben, beide eingeklappt
(`details.anleitung`).

1. **① Clip.** Ein Einführungsclip zeigt **alles**, was das Kapitel bringt — in Bewegung —
   und endet mit dem allgemeinen Auftrag: «Erkunde diese Zusammenhänge in der nachfolgenden
   Animation und löse die Aufgaben.»
2. **② Tüfteln.** Die Simulation (§8) trägt ihre Aufgaben **selbst**. Reihenfolge: zuerst
   **Erkunden** (frei an allen Reglern ziehen), dann **konkrete Situationen zum Nachstellen**
   — nicht die Beispiele aus dem Clip —, dann Zielspiele. Hilfslinien (gestrichelte
   Bezugskurven) lassen sich in jeder Animation, die welche hat, mit einem Schalter aus- und
   einblenden (`<label class="hilfs-schalter">` in der Figur, Klasse `hilfslinie` am
   Element). Technik: eine Aufgabenleiste (`.leiste`) über dem Bild zeigt eine Aufgabe nach
   der anderen, setzt ✓, sobald der Zustand stimmt, und bietet «Nächste ▶» bzw.
   «überspringen». **Kein Text links daneben** — lange Aufträge schrecken ab. Eine Aufgabe =
   ein Satz. Zielspiele gehören als letzte Aufgaben dazu.
3. **③ Kontrollfragen.** Ein zweiter Clip mit **neuen** Beispielen — ohne Einleitungsszene,
   er beginnt direkt mit Frage 1 — hält an und fragt (Knöpfe oder Tippen ins Bild; Drehbuchfeld
   `fragen`, HOWTO-clips «Fragen im Clip»). Richtig → kurzes ✓, der Clip rollt sofort weiter;
   falsch → Erklärung (vorgelesen) und «Weiter». Danach **Festhalten**: ein Merkkasten
   (Formel und Definition im Wortlaut der Themenseite, kurz) und der Häufige Fehler in einem
   Satz.
4. **④ Üben mit Rückmeldung.** Zwei bis drei `.uebung`-Kästen (§9).
5. **⑤ Aufgaben mit Lösungen.** Drei bis vier Aufgaben auf Papier, Lösung aufklappbar, nach
   dem Ansatz-Prinzip (erst die Formel, dann die Werte mit Einheiten).

**Text aufs Nötigste.** Clip-Karten nur mit Titel und Dauer (keine Unterzeile). Lernziel ein
Satz, keine Einleitungsabsätze, keine Hinweise, die der Clip schon gibt; «Mehr dazu» als eine
Zeile mit Link.

Am Ende des Leitprogramms: **Gesamttest und Bewertungspaket als PDF** (§9).

Zeit: 35–45 Minuten je Kapitel (zwei Clips à ~1 min, Tüfteln ~8–10, Übungen ~8, Selbsttest
~15–20) — ein Kapitel ≈ eine Lektion (§3). Die Zeiten werden geschätzt, nicht aus der Planung
übernommen.

---

## 5 · Entstehung: im Repo, nicht extern

**Der Normalfall ist: eine bestehende Leitprogramm-Seite kopieren** und nur den Inhalt
ersetzen — Kopf, `<style>`-Block, Fortschritts- und Clipkarten-Skript **wörtlich** (bewährt:
aus `leitprogramm-waermemenge`), neu geschrieben werden nur Inhalt und Simulations-Skript.
Dann stehen Dokumentrahmen, Hosts, Stylesheets, Tokens, Dunkelmodus und Skripte schon richtig
(§11), und die Dateien bleiben beieinander. **Nicht vergessen:** den `localStorage`-Schlüssel
(`var KEY = 'leitprogramm-<name>-v1'`), sonst teilen zwei Leitprogramme einen
Fortschrittsstand — das Häkchen im einen erscheint im anderen.

Für ein Leitprogramm nach dem Kapitelmuster (§4) ist der Weg das Bauskript: `scripts/lp/elektrizitaet/`
kopieren, Kapitel, Simulationen und Übungstypen ersetzen, den Speicherschlüssel `KEY` ändern.

Kommt eine Datei von aussen, gilt die Übertragsliste in §12.

---

## 6 · Layout und Bildschirmbreite

### Befund

Das Raster der bestehenden Leitprogramme: Hülle max. 1180 px, Schiene links, Fliesstext
`.prose` max. 66ch — bei 17 px Serif rund 620 px. Auf einem 1280-px-Schirm bleibt rechts vom
Text viel Fläche leer, ab 1440 px wächst der leere Rand auf beiden Seiten. Beispiele, Tabellen
und Tests sind dadurch schmaler als nötig, und eine Simulation lässt sich nicht neben den Text
stellen, der sie erklärt.

### Regel für neue Leitprogramme: Fliesstext schmal, Arbeitsflächen breit

- **Fliesstext bleibt lesbar schmal:** Absätze, Lernziel, Überschriften höchstens
  **68ch**. Das ist die Zeilenlänge, bei der man am Stück lesen kann — sie wird nicht
  geopfert.
- **Arbeitsflächen nutzen die ganze Spalte:** Beispiel-Tabellen, Selbsttests,
  Gesamttest, Erkundungen, Simulationen, Merk-/Warnkästen. Dafür bekommt `.inhalt`
  **kein** `max-width` mehr; die Begrenzung sitzt auf den Textelementen.
- **Hülle breiter:** `.huelle` max. **1440 px**. Ab 1000 px Schiene links wie bisher.
- **Nebeneinander ab 1180 px:** Der Baustein `.duo` stellt zwei zusammengehörige Teile
  nebeneinander — Beispiel neben Diagramm, Clip + Merkkasten neben Häufigem Fehler,
  Simulation neben ihrer Anleitung. Darunter stapeln sie sich in Lesereihenfolge (erst
  links, dann rechts). **Die Reihenfolge im Quelltext ist die Lesereihenfolge auf dem
  Handy.**
- **Selbsttests zweispaltig ab 1180 px** (`.aufg.zwei`), wenn die Aufgaben kurz sind;
  jede Aufgabe samt aufklappbarer Lösung bleibt eine Zelle (`break-inside: avoid`).
- **Nicht alles verbreitern.** `.duo` nur, wo die beiden Hälften wirklich zusammen
  angeschaut werden. Zwei unabhängige Kästen nebeneinander zwingen das Auge zum
  Pendeln.
- **Kein Seiten-Zoom.** Eine zu hohe Simulation wird über das Layout gelöst, nicht über
  `zoom` — den Zoom stellt der Leser im Browser selbst ein.
- **Prüfen bei 360, 1280 und 1600 px** (§14); `render-check` meldet seitliches Scrollen.

```css
.huelle{max-width:1440px}
.inhalt{min-width:0}                        /* kein max-width mehr */
.kap>p,.kap>h2,.kap>h3,.ziel,.anleitung ol{max-width:68ch}
.duo{display:grid;gap:22px}
@media(min-width:1180px){
  .duo{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}
  .aufg.zwei{columns:2;column-gap:34px}
  .aufg.zwei>li{break-inside:avoid}
}
```

Die Klassennamen `.huelle`, `.inhalt`, `.kap`, `.duo` stammen aus dem Mathe-Vorbild; die
bestehenden Physik-Leitprogramme heissen anders (`.prose`, `.step-title`, …). **Entschieden am
Leitprogramm Elektrizität (03.10.2026): die Mathe-Namen** — ausser dort, wo Physiks `style.css`
einen Namen schon belegt: `sl-row`/`sl-grp`/`sl-val` heissen `reglerfeld`/`regler`/`regler-wert`,
`.frage` heisst `.a-frage` (§12 Punkt 9). Nicht in einer Seite mischen.

---

## 7 · Clips

- **Clips zeigen, sie erzählen nicht nur.** Wo es ein Diagramm oder eine Bewegung gibt,
  steht sie im Clip — als Aufnahme der Animation (`bild` mit JPG,
  `.claude/tools/aufnahme-anim.mjs`) oder als `graf` mit `geraden`, `parabeln`, `kurven`,
  `punkte` und, wo sich etwas während der Szene bewegt, `bewegung` (HOWTO-clips.md). Ein
  Clip, der «die Temperatur steigt linear» nur sagt, verfehlt sein Thema.
- **Je Kapitel zwei eigene Clips** im Kapitelmuster: Einführungsclip und Kontrollclip.
  Theme **`begreifbar-schlicht`** für Clips mit `graf` — ohne Häuschenpapier und roten Rand,
  weil sich Karo und Koordinatengitter stören. Notation wie im Leitprogramm; Achsen mit
  Grösse und Einheit (`xname`, `yname`, `pfeile`).
- **Leitprogramm-eigene Clips sind erlaubt**, wenn sie eine Simulation *des
  Leitprogramms* beschreiben oder zu einer Aufgabe des Leitprogramms gehören. Dann:
  `"probe": true` mit `_probe`-Begründung (nicht in der Bibliothek, auf keiner
  Themenseite), Dateiname `<lektion>-lp-<name>`, Startwert und Farben der Simulation.
  Layout, das sich in Mathe bewährt hat: Bild rechts (`x` 1010, `y` 175, 760 × 760),
  Formeln und Notizen links (`x` 150), `anim: "fade"` am Bild.
  **Werkstatt:** Drehbücher per Skript erzeugen (gleiche Fenster und Farben in allen
  Szenen), zuerst ohne Ton bauen und mit `pruef-clip.mjs` Szene für Szene ansehen, dann
  `build-clip-ton.py` → `build-clips.py` (Stimme `de_DE-thorsten-high`, siehe `CLAUDE.md`).
  **Nach der Vertonung das Erzeugerskript nicht mehr laufen lassen** — es überschreibt die
  gemessenen `dauer`; späte Layoutkorrekturen direkt im JSON und nur neu bauen.
- **Sonst nur bestehende Clips**, dieselben Dateien wie auf der Themenseite. Keine fast
  gleichen Varianten mit anderen Zahlen.
- **Themenclips** (Alltagsfrage, Verfahren, «Zum Mitnehmen») passen ins Leitprogramm.
- **Animations-Clips** (`*-anim-*`, Reihe «Animationen erklärt») setzen voraus, dass
  die Animation bedient wurde — nur nach einer Erkundung (§8a).
- **Clips anderer Themenseiten** sind im Vorwissen erwünscht.
- **Zahlen im Clip = Zahlen im Text direkt danach.** Widerspricht eine Simulation ihrem
  Clip, wird die Simulation angepasst, nicht der Clip (neu vertonen ist teuer).
- **Dauer** von der Themenseite übernehmen, bei eigenen Clips die Tonlänge aus
  `build-clip-ton.py` (abgerundet auf Sekunden) — nicht aus dem Drehbuch summieren.
- **Kein eingebetteter Ton** im Dokument — immer ein richtiger Clip aus `clips/`, gestartet
  über `.clipkarte` (§12, Punkt 11).
- Fehlt für einen Kernschritt ein Clip: melden, nicht ohne Auftrag bauen.

---

## 8 · Erkundungen und Simulationen

**Die eingebettete Simulation (b) ist der Normalfall.** Ein Link in einen zweiten Tab reisst
den Faden ab; wer erst suchen muss, wo er ist, erfährt nichts. Der Link auf die Themenseite
bleibt für die Vertiefung.

**Ist das zu nahe an der Themenseite?** Nein, solange die Rollen verschieden sind: Die
Themenseite ist der offene Spielplatz (alle Regler, alles gleichzeitig, kein Auftrag),
das Leitprogramm führt (ein bis drei Regler, eine Frage, Voraussage, Zielspiel, Treffer-
Rückmeldung). Gleich sein müssen Konventionen und Beispiele, nicht die Bedienung. Jede
Simulation trägt im Code einen Satz, worin sie sich von der Themenseiten-Animation
unterscheidet — lässt er sich nicht schreiben, ist sie überflüssig und der Link genügt.

Entscheid pro Kapitel:

**a) Die Animation der Themenseite passt genau so → Erkundungsauftrag, keine Code-Kopie.**
Kasten «🔍 Erkunden» mit Link auf den Anker (`../themen/<seite>.html#anim-…`, neuer Tab)
und einem **konkreten Auftrag**: was einstellen, was beobachten, was notieren. Die Frage
kommt im Selbsttest wieder. Danach darf der passende `*-anim-*`-Clip folgen. Höchstens eine
Erkundung pro Kapitel.

**b) Geführte Variante** (ein bis drei Regler, eine Aussage, eingebettet) → kleine
SVG-Simulation. Bewährte Muster: Regler + Bezugskurve (gestrichelt) · Zielspiel mit
Treffer-Rückmeldung · Knöpfe, die je ein Merkmal hervorheben · fester Zustand, der
«eingefangen» werden muss · Vorhersage vor dem Versuch (`leitprogramm-experimente-waerme`).
Verbindlich:
- Achsen **mit Einheit**, Formelzeichen, Konstanten und **Farbcodes** (STYLEGUIDE §5.2)
  identisch zur Themenseiten-Animation
- **Startwert = Beispiel im Text bzw. Clip** desselben Kapitels
- Merksatz in der Bildlegende gleichlautend wie in der «Erkenntnis» der Themenseite
- der Unterschied zur Themenseiten-Animation als Ein-Satz-Kommentar im Code
- Reglerenden und Sichtfenster vorab mit `python3` durchrechnen (bleibt die Kurve im
  Bild? sättigt ein Balken, während die Zahl weiterläuft? wo stehen Beschriftungen?)
- **an beiden Reglerenden** im Browser gegen nachgerechnete Werte stellen (§14)
- Wertanzeigen nach den Stilcheck-Regeln (STYLEGUIDE §2.1, §2.7, §5.10): `·` nur als
  Malpunkt, Werte mit Einheit, dieselbe Grösse überall gleich gerundet
- trägt im Kapitelmuster ihre Aufträge selbst: Aufgabenleiste `.leiste` mit
  `Leiste(fig, aufgaben, sim)` — je Aufgabe ein Satz (`text`), eine Prüfbedingung auf den
  Zustand (`ok`) und optional `setup` (Ziel einblenden, Modus wechseln); ✓ erscheint von
  selbst (§4)
- Werte im Text mit Dezimalpunkt und echtem Minus, gerundete mit «≈»

**c) Reine Rechentechnik → keine Animation.** Nur, wo sich wirklich nichts zeigen lässt.

---

## 9 · Selbsttests und Gesamttest

- **Vortest** prüft nur Voraussetzungen, 8–13 Punkte, mit Verweis bei Lücken.
- **Selbsttest je Kapitel**, 7–16 Punkte, 3–6 Aufgaben à 2–5 Punkte. Mischung:
  Rechnen · Erkennen/Entscheiden · Begründen (mindestens eine «Warum»-Frage).
- **Lösungen nach dem Ansatz-Prinzip:** erst die benannte Formel, dann die Werte **mit
  Einheiten** einsetzen; mehrstufige Umformungen auf getrennten Zeilen, keine `⇒`-Ketten.
- **Üben mit Rückmeldung vor dem Selbsttest** (Kapitelmuster; Vorbild Mathe
  `quadratische-funktionen.html`, Kapitel 1 und 3): `<div class="uebung" data-typ="…">` —
  jede Aufgabe würfelt neue Zahlen, die Eingabe wird im Browser geprüft (echtes Minus,
  `0.5`, `1/2`; Komma wird verstanden, aber angemerkt), und **jedes bekannte
  Fehlermuster hat eine eigene Rückmeldung** (in Physik etwa: Einheit nicht umgerechnet,
  °C statt K eingesetzt, Faktor 1000 bei kJ/J, Kehrwert genommen). Die Lösung erscheint
  erst nach dem zweiten Fehlversuch. Zähler «auf Anhieb richtig in Folge»; nichts wird
  gespeichert. Neue Aufgabentypen stehen als Objekt in `TYPEN` (Felder, Eingabemuster,
  `neu`, `pruefen`, `loesung`). Der Selbsttest mit Papier bleibt danach — er prüft das
  Aufschreiben.
- **Clips, die fragen**: Wo ein eigener Clip eine Voraussage zulässt, hält er an und
  fragt (HOWTO-clips, «Fragen im Clip»).
- **Mindestens eine Aufgabe am Diagramm je Kapitel**, wo es eines gibt: zuordnen
  (Diagramm ↔ Gleichung), ablesen (Wert oder Steigung aus dem Diagramm), skizzieren, am
  Bild entscheiden. Minigrafen als `<svg class="mini" …>`, gezeichnet vom Seitenskript —
  Punkte auf Gitterpunkte legen, sonst ist nichts ablesbar. Eine Aufgabe nimmt die
  Voraussage aus ① wieder auf.
- **Kein Selbsttest wiederholt ein Beispiel** (gleicher Typ, andere Zahlen), **kein
  Gesamttest einen Selbsttest.**
- **Jedes Kapitelziel wird geprüft; nichts wird geprüft, was nicht eingeführt ist.**
- **Lösung aufklappbar**, darunter optional eine Zeile `.komm` zur typischen
  Fehlerquelle.
- **Gesamttest und Bewertungspaket als PDF aus LaTeX** (Mathe-Entscheid 02.10.2026, für
  neue Physik-Leitprogramme übernommen). Quellen
  `downloads/leitprogramme/<name>/{gesamttest,bewertungspaket}.tex`, gemeinsame Gestaltung
  `downloads/leitprogramme/lp-druck.sty` (pdfLaTeX, Palatino über `mathpazo`, Diagramme mit
  pgfplots; Farbe Bernstein `#8A4A0E`, Fusszeile «physik.begreifbar.ch»). Bauen:
  `python3 scripts/build-lp-pdf.py [filter]` — übersetzt in einem temporären Ordner und
  legt nur das PDF neben die Quelle. LuaLaTeX geht auf diesem Rechner nicht
  (`luaotfload-tool` fehlt), darum pdfLaTeX. Im Leitprogramm steht nur ein Dreischritt mit
  den beiden Downloads und die Selbsteinschätzung.
  **Die acht bestehenden HTML-Gesamttests bleiben**, bis der Auftraggeber über eine
  Umstellung entscheidet (offen).
  - *Gesamttest-Blatt:* Feld «Code (kein Name)», Anleitung mit Zeit und Hilfsmitteln je
    Teil, Schreibflächen, Hinweis auf das Bewertungspaket.
  - *Bewertungspaket:* (1) So gehst du vor — erst lösen, fotografieren ohne Namen; ob und
    welche KI, entscheiden die Lernenden **selbst und in eigener Verantwortung** nach dem,
    was ihnen aufgrund von Alter und persönlicher Situation erlaubt ist (Altersgrenzen,
    Nutzungsbedingungen, allenfalls Einverständnis der Eltern) — die Seite ist frei
    zugänglich, nicht an eine Schule gebunden; ohne KI Selbstbewertung nach dem Raster;
    Lesung der KI prüfen; (2) **Auftrag an die KI** zum Kopieren — erst abschreiben, was
    sie liest, `[unsicher]` statt raten, Punkte nach Raster, Folgefehler nur einmal
    abziehen, andere Wege voll, jeden Abzug begründen, Musterlösung nicht abschreiben,
    Tabelle und Rückverweis aufs Kapitel, keine Note; (3) **Musterlösung und Punkteraster**
    je Aufgabe (Teilschritt · Punkt · Lösung) mit typischen Fehlern und Abzug; (4)
    Selbsteinschätzung.
  - Ganze Punkte je Teilschritt — halbe Punkte machen die KI-Bewertung unzuverlässig.
  - Einheiten zählen: Ein Ergebnis ohne oder mit falscher Einheit ist im Raster eigens
    geregelt (Ergebnispunkt), nicht dem Ermessen der KI überlassen.
- **Gesamttest** 20–25 Punkte, rund 20 Minuten, Teile = Kapitel = Kompetenzen,
  Hilfsmittel je Teil (§1.1).
- **Selbsteinschätzung** mit Punktebereichen, die auf **bestimmte Kapitel** zurückverweisen.
- Punkte summieren (Kopf = Summe der Aufgaben), Minuten summieren (§3).

---

## 10 · Notation und Fachsprache

Immer nach `STYLEGUIDE.md` §2 und den Stilcheck-Regeln in `CLAUDE.md`. Was im Leitprogramm
besonders oft schiefgeht:

| Was | Regel |
|---|---|
| Dezimaltrennzeichen | **Punkt**, nie Komma — in LaTeX (`9.81`, nicht `9{,}81`), Text, Live-Anzeigen, JS (§2.5) |
| Zahl und Einheit | geschütztes Leerzeichen; in LaTeX `9.81\;\text{m/s}^2`, Einheit aufrecht in `\text{…}` (§2.3) |
| Formelzeichen | kursiv, nach SI / DIN 1304; dieselben Zeichen wie auf der Themenseite (§1, §2) |
| Basis- und abgeleitete Grössen | sieben Basisgrössen; Fläche, Volumen, Kraft, Dichte usw. sind abgeleitet; Bezugseinheit = «Referenzeinheit» (§2.3) |
| Liter | klein: `l`, `ml`, `dl`, `kg/l` — nie `L`/`mL`; das grosse \(L\) bleibt für Längen und latente Wärme (§2.3) |
| Signifikante Stellen | in der BM üblich 3; Endergebnis an die Eingangsdaten anpassen, gerundet mit «≈» (§2.6) |
| Negative Werte | echtes Minus `−` (U+2212) in Anzeigen, `fmtS()` aus `physiklib.js` (§2.6) |
| Einsetzen | Werte **mit Einheit** einsetzen, auch in Live-Formelzeilen (§2.7) |
| Brüche | als `\frac{…}{…}`, nicht als Schrägstrich in einer Formelzeile (§2.8) |
| Malpunkt | `·` heisst nur Multiplikation; Trenner in Wertanzeigen ist der Strichpunkt `;` (§2.1) |
| Titel | kein Gedankenstrich und kein Mittepunkt direkt an einer Formel (§2.9) |
| Preis und Kosten | Preis = pro Einheit (CHF/kWh), Kosten = Betrag (CHF) (§2.6b) |
| Diagramme | Achsen **immer mit Einheit**; nur x-y-Bahnen 1:1 (§3) |
| Fachbegriffe | **der Begriff aus den RLP-Kompetenzen** (Gruppe 1, z. B. «Heizwert», nicht «Brennwert»); weicht die Themenseite oder ein Clip ab, deren Namen einmal in Klammern nennen |
| Methodenwahl | andere Hauptmethode als die Themenseite → beide nennen, Wahl in einem Satz begründen |

Sprache: Du-Form in Aufträgen, kurze Sätze, Schweizer Rechtschreibung (immer ss, kein Eszett), kein «wir».

---

## 11 · Technisches Gerüst (gilt immer)

Steht in jeder kopierten Vorlage schon richtig; bei einer Datei von aussen §12.

- Datei unter `leitprogramme/<name>.html`, **genau eine Ebene** unter der Wurzel.
- `<!DOCTYPE html>`, `<html lang="de-CH">`, `<meta charset="UTF-8">` in den ersten
  1024 Bytes, Viewport.
- **Kein fremder Host:** `../schriften.css`, `../vendor/mathjax/tex-svg.js`.
- **`../style.css` vor dem eigenen `<style>`** — der eigene gewinnt bei gleichem Gewicht.
- **Tokens erben:** im eigenen `:root` nur Übersetzungen (`--karte:var(--weiss)`) und
  der Dunkelmodus; dieser setzt `--weiss` mit und behandelt `.site-footer` eigens.
- **Kopf und Fuss der Site:** `<div id="nav-root">`, `.site-footer` nach STYLEGUIDE §6.1a,
  am Schluss `../physiklib.js`, `../nav.js`, `../suche.js` und
  `buildNav({ id: 'leitprogramme' })`. **Ohne `physiklib.js` läuft jede Clipkarte ins
  Leere**, weil `clipBuehne` von dort kommt (so bei `leitprogramm-schaltungen` vom 13.09.
  bis 27.09.2026).
- **Clip-Bühne aus `physiklib.js`** (`clipBuehne(quelle, titel)`), `BASIS = '../'`.
- **`h2` mit `id`** (Suche schneidet an `h2[id]`); keine `id` doppelt zwischen
  `<section>` und Überschrift.
- **Eigener `localStorage`-Schlüssel** (`leitprogramm-<name>-v1`).
- **Nicht in `page-wrap` + `main.content` pressen.**

---

## 12 · Übertragsliste für extern gebaute Dateien

Der Reihe nach abarbeiten. Nach jedem Punkt steht, woran man merkt, dass er fehlt. Gilt
auch beim Schreiben einer neuen Datei als Kontrollliste.

### 1. Datei nach `leitprogramme/<name>.html`

Genau **eine Ebene** unter der Wurzel, wie `clips/`. Alle relativen Pfade unten
setzen das voraus.

### 2. Fremde Hosts entfernen

Extern gebaute Dateien ziehen Schriften und MathJax typischerweise von Google und
einem CDN. Im Repo gilt: **keine Seite lädt etwas von einem fremden Host.**

```html
<link rel="stylesheet" href="../schriften.css">
<script src="../vendor/mathjax/tex-svg.js"></script>
```

Die `<link>`-Zeilen auf `fonts.googleapis.com`, `fonts.gstatic.com` und die
`preconnect` ersatzlos streichen. **Merkt man daran:** Der Pre-Flight meldet die
Hosts (`check_keine_fremdhosts`), und ohne Netz fällt die Seite auf Georgia zurück.

### 3. Dokumentrahmen und Zeichensatz

Von Hand gebaute Dateien beginnen gern direkt mit `<title>` — ohne `<!DOCTYPE>`,
ohne `<html>`, ohne `<head>`, ohne `<body>`. Ohne `<meta charset>` rät der Browser
die Kodierung, und über HTTP rät er falsch:

```
hÃ¤ngen · ErklÃ¤rung · â€"
```

Darum immer:

```html
<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
…
</head>
<body>
```

Das `charset` muss in den **ersten 1024 Bytes** stehen — also vor dem
SEO-Block, den `build-seo.py` nach dem `<title>` einsetzt.

**Merkt man daran:** Umlaute zerfallen — aber erst im Browser, nicht im Editor,
und in keiner Prüfung. Ohne Viewport ist zusätzlich die Mobilansicht kaputt.

### 4. Anker an die Kapitel

Die Volltextsuche schneidet ihre Abschnitte an `h2[id]`. Ohne `id` ist die ganze
Seite **ein** Treffer — beim Leitprogramm zu den idealen Gasen wären das 29 kB
Text unter einer einzigen Überschrift gewesen; mit Ankern sind es 13 Abschnitte.

Sitzt die `id` auf der umgebenden `<section>` und ist sie zugleich Sprungziel der
Ablaufspalte, **auf die Überschrift verschieben** statt sie zu verdoppeln: Der
Sprung funktioniert weiter und landet sogar präziser. Der Pre-Flight meldet
doppelte IDs.

### 5. Relative Basis für eingebettete Clips

Steht im Skript eine absolute Adresse

```js
var BASIS = 'https://physik.begreifbar.ch/';
```

dann kommen eingebettete Clips vom **Live-Stand**, nicht aus dem
Arbeitsverzeichnis. Eine lokale Vorschau zeigt den alten Clip, ohne Netz gar
keinen. Ersetzen durch `'../'`.

### 6. Kopf, Fuss und Bühne von der Site erben

```html
<link rel="stylesheet" href="../schriften.css">
<link rel="stylesheet" href="../style.css">   <!-- VOR dem eigenen <style> -->
…
<style> … eigenes Layout … </style>
```

**Die Reihenfolge ist der ganze Trick:** Der eigene `<style>` steht danach und
gewinnt bei gleichem Gewicht — das Layout des Leitprogramms bleibt unverändert.

Dazu im Körper:

```html
<body>
<div id="nav-root"></div>
…
<footer class="site-footer"> … </footer>
<script src="../physiklib.js"></script>
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script>buildNav({ id: 'leitprogramme' });</script>
</body>
```

`physiklib.js` bringt die Clip-Bühne mit (`clipBuehne`). Eine mitgelieferte Kopie
davon **löschen** — die Bühne ist überall dieselbe.

**Merkt man daran:** Ohne Kopf und Fuss ist die Seite eine Sackgasse — man kommt
nur mit dem Zurück-Knopf heraus. Ohne `physiklib.js` tut keine Clipkarte etwas.

### 7. Farbtokens erben, nicht kopieren

Extern gebaute Dateien tragen die Palette als eigenen `:root`-Block. Stimmt sie
mit `style.css` überein: **löschen**. Was bleibt, ist die Übersetzung abweichender
Namen (`:root{ --karte: var(--weiss); }`).

Beim Leitprogramm zu den idealen Gasen war das **nicht** der Fall: Es führt ein
eigenes Vokabular (`--ground`, `--surface`, `--ink`, `--accent`) mit eigenen
Werten. Dann bleibt der Block, wie er ist — die Palette nicht angleichen, sie
läuft sonst beim nächsten Update auseinander.

### 8. Dunkelmodus, falls die Datei einen hat

`style.css` kennt **keinen** — die Site hat keinen. Ein Leitprogramm darf einen
haben (man liest es am Stück), muss dann aber die geerbten Bausteine mitfärben.
Der Weg dazu ist **ein Token, nicht eine Liste von Klassen**: `style.css` färbt
seine Flächen über `--weiss`; ist das Token dunkel, ziehen Kopfleiste, Menü,
Suchfeld und Über-Panel von selbst nach.

```css
:root[data-theme="dark"]{ … --weiss:#201c16; --papier:#17140f; --tinte:#ede7de; … }
```

**Eine Ausnahme bleibt:** `.site-footer` benutzt `--tinte` als *Fläche*. Im
Dunkelmodus kippt `--tinte` mit dem Text nach hell — der Fuss würde weiss.

```css
:root[data-theme="dark"] .site-footer{
  background:var(--papier-2); color:var(--tinte-2); border-top:1px solid var(--linie);
}
:root[data-theme="dark"] .site-footer a{ color:var(--bernstein); }
```

> **Falle, die beim Physik-Übertrag zuschlug:** Die Systemvariante dieser Regel
> **muss in die Media-Abfrage**. Steht `:root:not([data-theme="light"]) .site-footer`
> global, trifft sie auch im **Hellmodus** zu — dort ist kein `data-theme` gesetzt —
> und färbt den Fuss fälschlich hell. Gemessen: `rgb(239,234,222)` statt
> `rgb(28,26,23)` wie auf jeder anderen Seite. Richtig:
>
> ```css
> @media (prefers-color-scheme: dark){
>   :root:not([data-theme="light"]) .site-footer{ … }
> }
> ```

### 9. Klassennamen, die mit `style.css` kollidieren

Weil `style.css` **vor** dem eigenen `<style>` steht, gewinnt der eigene Block
bei gleichem Gewicht — aber nur für **dieselbe Eigenschaft**. Setzt `style.css`
eine Eigenschaft, die das Leitprogramm gar nicht anfasst, bleibt sie stehen.

Gemessen an `.frage`: Auf einer Themenseite ist das das
Verständnisfrage-Akkordeon und trägt `background: var(--blau-hell)`, `border`
und `border-radius`. In den Leitprogrammen heisst `.frage` die
**Einstiegsfrage** und definiert nur `border-left` — die blaue Fläche kam also
ungefragt mit. Im Hellmodus leuchtete ein blauer Kasten in einer durchgehend
bernsteinfarbenen Seite; im Dunkelmodus stand heller Text (`--ink` kippt mit)
auf hellblauem Grund und war unlesbar. `--blau-hell` gehört zu den Tokens, die
ein Leitprogramm **nicht** umfärbt.

Darum: Wer eine Klasse benutzt, die es in `style.css` auch gibt, nimmt die
fremden Eigenschaften ausdrücklich zurück.

```css
.frage{ background:none; border:none; border-radius:0; overflow:visible;
        border-left:3px solid var(--rule-strong); }
```

**Merkt man daran:** gar nicht — bis man die Seite im Dunkelmodus anschaut.
Die Kandidaten findet man mit

```bash
grep -oE '^\.[a-z][a-z0-9-]*' style.css | sort -u > /tmp/site.txt
# dieselbe Liste aus dem <style> des Leitprogramms ziehen und schneiden
```

### 10. Kein LaTeX in den kleinen Textbausteinen

In `figcaption`, `.sim-lab`, `.sim-out`, `.step-goal` und `.scene-cap` wird MathJax
riesig gesetzt — ein einzelnes \(n\) erscheint sechzig Pixel hoch und sprengt
die Zeile. Die Leitprogramme vermeiden es dort darum durchgehend: Was in
einer Bildunterschrift oder an einem Regler steht, wird als Klartext
geschrieben (`Teile je Kante n`, `Volumen V`, `g/cm³`).

**Merkt man daran:** keine Prüfung meldet es, der Render-Check auch nicht —
es passt ja in die Zeile. Man sieht es nur im Bild. Die Kontrolle lautet

```bash
grep -n 'class="step-goal"\|<figcaption>\|class="sim-lab"\|class="sim-out"' <datei> | grep '\\('
```

und muss **0** ergeben. Beim dritten Leitprogramm ist die Falle zweimal
zugeschlagen: erst in den Lernzielen, nach deren Bereinigung noch einmal in
den vier Bildunterschriften.

Dazu gehört ein zweiter, verwandter Punkt: Lange deutsche Komposita sprengen
die schmale Spalte bei 360 px. «Volumenausdehnung» allein misst mehr als die
235 px, die dort für die Überschrift bleiben. Ein Wortumbruch kostet drei
Zeilen und rettet die Mobilansicht:

```css
.step-title, .step-goal, .masthead h1{ overflow-wrap:break-word; hyphens:auto; }
```

### 11. Eingebetteter Ton fesselt den Text — besser ein richtiger Clip

Eine fremde Datei kann ihre Erklärszenen als **base64-MP3 im `TON`-Block**
mitbringen. Das sieht bequem aus, bindet aber Hände: Der Text in
`<details class="script">` ist dann die Verschriftung genau dieses Tons und
lässt sich nicht mehr frei ändern. Beim Gase-Leitprogramm sprach die
mitgelieferte Stimme rund anderthalbmal schneller als `de_DE-thorsten-high`
(4.0 s gegen 6.15 s für denselben Satz), und die Zeitmarken in `TON[key].k`
waren auf sie eingemessen — nachsprechen liess sich das nicht. Solange der
Ton im Dokument steckt, ist auch das Umschreiben auf **du** blockiert: Ein
Transkript, das vom Ton abweicht, ist schlimmer als ein Sprecher, der siezt.

Dazu kommt das Gewicht. Acht vertonte Szenen als Datei-URI machten aus einer
130-kB-Seite eine von **1.05 MB**, die vollständig geladen wird, bevor der
erste Buchstabe steht.

**Die Auflösung ist ein richtiger Clip.** Am 07.09.2026 sind die acht Szenen
des Gase-Leitprogramms durch acht Clips in `clips/` ersetzt worden (Reihe
«Ideale Gase»): gebaut aus einem Drehbuch, vertont mit der Hausstimme,
zentral in `clips.html` auffindbar — und im Leitprogramm als `.clipkarte`,
die erst beim Klick lädt. Damit sieht das Gase-Leitprogramm aus wie die
anderen, und der Sprechertext lebt an genau einer Stelle.

**Merkt man daran:** an der Dateigrösse — und daran, dass sich ein Satz im
Transkript nicht ändern lässt, ohne dass Bild und Ton auseinanderlaufen.

### 12. Eintragen

Siehe §13 (vier Stellen). Danach Layout nach §6 nachziehen, soweit die Datei neu
aufgebaut wird.

---

## 13 · Verknüpfen und Eintragen

**Vier Stellen** — fehlt eine, ist die Seite unsichtbar, unauffindbar oder einseitig:

| Datei | was |
|---|---|
| `leitprogramme.html` | Karte im Block zwischen den `LEITPROGRAMME`-Markern, unter dem passenden Lerngebiet |
| `scripts/build-seo.py` | Eintrag in `SEITEN` — sonst fehlen Beschreibung und Sitemap |
| `scripts/build-suchindex.py` | nichts einzutragen: alles in `leitprogramme/` wird automatisch erfasst |
| Themenseite / Vorwissenseite | `.block-tipp` «💡 Lieber geführt durcharbeiten?» mit Link aufs Leitprogramm und einem Satz, was nur auf der Seite steht |
| `nav.js` | nur beim **ersten** Leitprogramm nötig, der Menüeintrag steht schon |

Danach `python3 scripts/build-seo.py` und `python3 scripts/build-suchindex.py` (beide
schreiben ohne Schalter).

Im Leitprogramm selbst: «Ausführlich»-Link je Kapitel (§4) — in den Auswertungstabellen
als dritte Spalte «ausführlich nachlesen» mit Anker auf die Themenseite —, Vorwissen
verweist auf das vorausgehende Leitprogramm, der Schluss auf das folgende und auf das
bewusst Weggelassene.

⟂ Entscheid (aus Mathe): Die Technik-Fassung kannte drei Stellen, die Didaktik-Fassung
forderte den Themenseiten-Kasten zusätzlich. Jetzt sind es vier; in Physik ist der
Kasten seit dem Querverweis-Entscheid (`CLAUDE.md`, «Querverweise ins Vorwissen») ohnehin
Teil der Verabredung.

**Unverlinkt veröffentlichen** (Erprobung, Übungsprüfung per Link): keine Karte, kein
Suchindex-Treffer, Themenseite ohne Kasten, aber `build-seo.py` **mit `noindex=True`**
(nicht weglassen). Kein `Disallow` in `robots.txt`. Es ist Unauffindbarkeit, keine
Zugangskontrolle. Weil `build-suchindex.py` alles in `leitprogramme/` erfasst, muss die
unverlinkte Seite dort **ausdrücklich ausgenommen** werden: Menge `UNVERLINKT` in
`build-suchindex.py` (seit 03.10.2026). Freischalten heisst: dort streichen, `noindex` in
`build-seo.py` entfernen, Karte in `leitprogramme.html` setzen, Kasten auf der Themenseite.
Prüfen:

```sh
grep -c "<dateiname>" sitemap.xml suchindex.js leitprogramme.html   # dreimal 0
grep 'name="robots"' leitprogramme/<name>.html                      # noindex, nofollow
```

---

## 14 · Abnahme vor dem Commit

1. **Jede Lösung nachrechnen** mit einem kurzen `python3`-Skript. Keine Zahl ungeprüft.
2. **Kompetenzmatrix vollständig:** jede Kompetenz ↔ Kapitel ↔ Test; kein Ziel ohne
   Kompetenz; Hilfsmittel im Gesamttest stimmen.
3. Punkte- und Minutensummen stimmen mit Kopf, Ablauf und Testköpfen überein.
4. Konventions-Grep gegen die Themenseite: Fachbegriffe, Formelzeichen, Einheiten
   (Liter klein, Dezimalpunkt), Achsen mit Einheit, Malpunkt nur als Multiplikation.
5. Clip-Zahlen gegen Text und Simulationsstartwerte desselben Kapitels.
6. Links in beide Richtungen; Anker der Erkundungen existieren
   (`grep -o 'id="anim-…"'` auf der Themenseite).
7. Kein Selbsttest wiederholt ein Beispiel, kein Gesamttest einen Selbsttest.
8. Technik:
   ```bash
   python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html leitprogramme.html
   python3 -m http.server 8899 &
   node .claude/tools/pruef-mathjax.mjs http://localhost:8899/leitprogramme/<name>.html
   node .claude/tools/render-check.mjs leitprogramme/<name>.html          # 1280 und 360 px
   node .claude/tools/scan-live.mjs leitprogramme/<name>.html             # Malpunkt als Trenner
   node .claude/tools/pruef-uebungen.mjs leitprogramme/<name>.html 1000   # Zufallsübungen
   node .claude/tools/pruef-leiste.mjs leitprogramme/<name>.html          # Aufgabenleisten
   node .claude/tools/pruef-fragen.mjs <clip> …                           # Fragen in Kontrollclips
   ```
   `pruef-uebungen`, `pruef-leiste` und `pruef-fragen` starten einen eigenen Server und
   enden mit Exit 1 bei einem Befund. `pruef-uebungen` braucht im Seitenskript die
   Testhaken `box.__aufgabe = A` und `box.__typ = T` (aus dem Kapitelmuster); die richtige
   Eingabe ist `A[feld]`, sonst liefert der Typ `eingabe(A)`. Gezielte Fehler mit
   erwarteter Meldung: `fehler(A)` → `[[{ feld: 'wert' }, 'Stichwort'], …]` — ohne sie
   prüft das Werkzeug nur, dass eine verschobene Eingabe nicht als richtig gilt, nicht, ob
   die Diagnose stimmt. Bewegung im Clip auf den Ton legen:
   `python3 .claude/tools/sprechzeiten.py <clip>`.
   Der Pre-Flight prüft Skelett, Bibliotheks-Einbindung und Ressourcen-Sektion nur für
   `themen/` — ein Leitprogramm hat bewusst kein `page-wrap` und kein `main.content`.
   Fremdhosts und doppelte IDs prüft er überall.
9. **Simulationen im Browser gegen nachgerechnete Werte stellen:** Regler auf einen Wert
   setzen, die Ausgabe auslesen und mit dem `python3`-Ergebnis vergleichen — **an beiden
   Reglerenden**, nicht nur in der Mitte. Ein Vorzeichen- oder Massstabsfehler im
   Zeichencode fällt sonst nirgends auf — die Grafik sieht immer plausibel aus.
10. **Hinschauen**: hell und dunkel, 360 / 1280 / 1600 px. Keine Prüfung sieht
    - zerfallene Umlaute (§12, Punkt 3)
    - eine weisse Kopfleiste über dunkler Seite (Punkt 8)
    - einen hellen Fuss im Hellmodus, weil die Dunkelregel zu weit greift (Punkt 8)
    - einen Clip, der vom Live-Stand kommt statt aus `clips/` (Punkt 5)
    - eine blaue Einstiegsfrage oder hellen Text auf hellem Grund, weil eine Klasse aus
      `style.css` durchschlägt (Punkt 9)
    - riesig gesetzte Formeln in Bildunterschriften, an Reglern und in `.sim-out`
      (Punkt 10)
    - einen Balken, der sättigt, während die Zahl daneben weiterläuft (§16)

    Beim ersten Übertrag ist jeder dieser Punkte erst im Bild aufgefallen.
11. **Bericht** an den Auftraggeber: Planung (§2), was bewusst anders ist als auf der
    Themenseite und warum, welche Widersprüche in der Themenseite gefunden wurden, welche
    Clips fehlen.

---

## 15 · Prüfung vor der Freischaltung

Die Selbstkontrolle in §14 macht, wer baut — und sieht darum, was er sehen will. Beim
Mathe-Vorbild haben zwei unabhängige Prüfungen nach bestandener §14 noch je rund 25 Befunde
gefunden (03.10.2026), darunter fachlich Falsches. Darum gilt für jedes neue Leitprogramm:

1. **Unverlinkt veröffentlichen** (§13), noch nicht freischalten.
2. **Unabhängige Prüfung:** Skill `/lp-pruefung leitprogramme/<name>.html`
   (`.claude/skills/lp-pruefung/SKILL.md`). Drei frische Agenten prüfen Seite, Clips und
   PDFs gegen die Prüfliste unten und rechnen jede Zahl nach; sie ändern nichts. Die
   Befunde werden nach HOCH / MITTEL / NIEDRIG geordnet und dem Auftraggeber berichtet —
   **keine** Befund- oder TODO-Datei im Repo (das Repo ist die veröffentlichte Website;
   `CLAUDE.md`, «Der Git-Verlauf ist die einzige Änderungsdokumentation»).
3. **Beheben**, Befund für Befund, mit §14 danach.
4. **Abnahme durch den Auftraggeber** (kann niemand sonst): Hörprobe aller neu vertonten
   Clips mit Fragen — je eine Frage absichtlich falsch beantworten —, und das
   Bewertungspaket mit einer absichtlich fehlerhaften Schülerlösung einer KI geben.
5. **Erst dann freischalten** (§13, alle vier Stellen).

Die Werkzeuge dazu: `.claude/tools/pruef-uebungen.mjs`, `.claude/tools/pruef-leiste.mjs`,
`.claude/tools/pruef-fragen.mjs` und `.claude/tools/sprechzeiten.py` (§14, Punkt 8).

### Prüfliste — was bei den Prüfungen aufgefallen ist

Jeder Punkt war ein echter Befund (Mathe-Vorbild, ergänzt um die Physik-Erfahrungen aus §16).
Wer baut, geht sie vor §15 selbst durch; wer prüft, prüft gegen sie und darüber hinaus.

**Fachlich**
- Voraussetzungen ausschreiben: Formeln mit ihren Gültigkeitsbedingungen (konstante
  Beschleunigung, ideales Gas, ohne Phasenübergang, Temperatur in Kelvin, ohmscher
  Widerstand), Sachaufgaben mit Grösse und zulässigem Bereich.
- Vorzeichen- und Richtungsregeln wörtlich prüfen (abgegebene gegen aufgenommene Wärme,
  Stromrichtung, Bezugsrichtung). Clip, Seite und Themenseite müssen dasselbe sagen.
- Erst das allgemeine Verfahren, dann die Abkürzung — und die Abkürzung als solche
  kennzeichnen, mit ihrer Bedingung.
- Nichts abfragen, was nicht eingeführt ist (Begriff, Formelzeichen, Verfahren). Jedes
  Verfahren, das der Gesamttest verlangt, wird in einem Kapitel geübt.
- Lösung und Aufgabenstellung passen zusammen («ohne Rechnen» + Lösung rechnet = Befund).
- Einheiten in jeder Zeile der Lösung; Umrechnungen beim ersten Vorkommen ausgeschrieben.

**Clips**
- Wenn eine Frage erscheint, steht ihre Antwort **nicht** im Bild (erster Stützpunkt
  neutral, Begleiter und Beschriftung erst nach der Antwort).
- Bild und Ton gleichzeitig: Bewegungen nach `sprechzeiten.py` legen, nicht nach Gefühl.
  Was der Ton sagt, zeigt das Bild genau so.
- Eindeutige Begriffe (nie «die Achse», wenn zwei in Frage kommen).
- Eine Farbe, eine Bedeutung — im ganzen Leitprogramm, Clips und Seite (STYLEGUIDE §5.2).
- Rückmeldungen lenken aufs Hinschauen und verraten die Lösung nicht; angezeigter Text =
  gesprochener Text.
- Notation wie im Leitprogramm, auch im Merkbild.
- Zahlen im Sprechertext ausgeschrieben (`CLAUDE.md`, Vertonung).
- **Bewegung im Prüfbild nachsehen**, nicht nur im Drehbuch: ein Bild bei 0.3 s jeder
  Fragenszene und eines mitten in jeder Bewegung. (Elektrizität, 03.10.2026: Ein Fehler im
  Generator liess jede bewegte Gerade sofort im Endzustand stehen — die Drehbücher waren
  richtig, die Bilder nicht; behoben in `build-clips.py`.)
- **Aufgenommene Bilder einer Simulation ansehen**, bevor sie in einen Clip gehen: Zeigt das
  Bild den Zustand, den der Ton beschreibt? (Elektrizität: Bilder mit 12 V statt 230 V und ein
  doppeltes Bild — die Mausklicks des Aufnahmewerkzeugs hatten nicht gegriffen. Knöpfe darum
  mit einer `js`-Aktion auslösen: `document.querySelector(…).click()`.)
- Kontrollfragen bringen **neue** Beispiele: weder die Werte des Einführungsclips noch seine
  Bilder, noch die Ziele der Aufgabenleiste. Auch nicht die Mini-Checks der Themenseite (Kinematik:
  «150 km in 2 h» und «schwere und leichte Kugel» standen dort wörtlich).
- **Ein Bild je Aussage**: Der Clip-Generator kann ein Element nicht ausblenden. Braucht eine Szene zwei
  Zustände (r = 2 m, dann r = 4 m bei T = 8 s), die Szene teilen — sonst steht eine Zahl neben dem falschen Bild.
- **Marken bei Klickfragen**: Eine `marke` an der gefragten Stelle zeigt beim Fragebeginn einen Wert
  (\(s = 0\;\text{m}\)) genau dort, wo getippt werden soll — bei Klickfragen weglassen.

**Animationen und Übungen**
- Kein Ziel der Aufgabenleiste ist schon im Startzustand erfüllt; Ziele sind nicht die
  Beispiele aus dem Clip; Überspringen wird als Überspringen gezählt (`pruef-leiste`).
- Zufallsübungen: nur lösbare, physikalisch sinnvolle Fälle (keine negativen Massen,
  keine Temperatur unter 0 K); Sonderwerte erzeugen keine falsche Diagnose; Randfälle
  des Stoffs mit üben; kein Zufallsfall gleich einer festen Aufgabe (`pruef-uebungen`
  mit `fehler()`).
- Hinweise rechnen nicht anders als die Lösung.
- **Formelsatz der Übungstexte prüfen**: `pruef-uebungen` schaltet MathJax ab und sieht
  darum weder Satzfehler noch LaTeX, das als Text erscheint. `.claude/tools/pruef-formelsatz.mjs` setzt Aufgabe,
  Rückmeldungen und Lösung vieler Zufallsfälle mit MathJax. Falle: `\mu` gehört nicht in
  `\text{…}` (`\;\mu\text{C}`, nicht `\text{\mu C}`).
- Klassennamen gegen Physiks `style.css` prüfen, bevor man sie aus Mathe übernimmt
  (`sl-row`, `sl-grp`, `sl-val`, `frage` sind dort belegt; §12 Punkt 9).
- Minigrafen: Beschriftungen in Fensteranteilen versetzen, nicht in Dateneinheiten — sonst
  landen sie bei kleinen Achsenwerten ausserhalb des Bildes.
- Live-Anzeigen runden nur mit «≈»; dieselbe Grösse überall gleich gerundet.
- **Zahlen, die zufällig zusammenfallen** (Kinematik, 04.10.2026): Bei \(t = 2\;\text{s}\) ist
  \(g \cdot t = \tfrac12 \cdot g \cdot t^2\) — wer Geschwindigkeit und Fallweg verwechselt, trifft die richtige
  Antwort. Ebenso \(t = 1\;\text{s}\) (\(t^2 = t\)), \(|a| = 1\) (Kehrwert gleich), \(v = 1\). Werte für Fragen
  und Zufallsübungen so wählen, dass jedes Fehlermuster eine andere Zahl ergibt.
- **Plausible Zufallswerte**: nicht nur lösbar, sondern realistisch — keine Läuferin über dem Weltrekord,
  keine Kurvenfahrt mit mehr als rund \(0.7\,g\). Grenzen im Generator, nicht in der Liste hoffen.
- **Gerundete Zwischenwerte**: Wer \(v\) richtig auf drei Stellen rundet und damit weiterrechnet, darf nicht
  abgewiesen werden (Folgewert mit der Eingabe prüfen); im Bewertungspaket eine Rundungsregel (rund 2 %).
- Je Kapitel mindestens eine «Warum»-Aufgabe und eine Aufgabe am Diagramm (§9).
- **Laufende Simulationen** (Fahrt auf Knopfdruck, Dynamik 04.10.2026): Nichts läuft von selbst los —
  auch keine «nur zur Anschauung» bewegte Kulisse. Der graue Vergleich «voriger Lauf» muss beim Start
  den *vorigen* Lauf übernehmen; wer ihn am Fahrtende setzt, zeigt den eben gefahrenen Lauf doppelt, und
  der Vergleich ist nie zu sehen. Mit «weniger Bewegung» und bei Reglerbewegung mitten im Lauf jeden Knopf
  einmal durchprobieren (Beschriftung und Zustand passen zusammen?).
- **Modellgrenzen in der Formelzeile**: Bleibt ein Körper im Modell stehen (Haftung, Stillstand nach dem
  Ausrollen), muss die Zeile \(F_\text{ges} = 0\) und \(a = 0\) zeigen — nie eine Gesamtkraft ohne
  Beschleunigung. Die Sonderfälle (Stand, Halt, gleich grosse Kräfte) gezielt einstellen und lesen.
- **Formelzeilen ohne gerundete Zwischenwerte**: Ein Ergebnis aus dem ungerundeten Wert hinter einem
  gerundet angezeigten Faktor ergibt «2 kg · 4.91 m/s² = 9.81 N». Die Zeile aus den Eingaben bauen
  (\(F_S = m_1 \cdot m_2 \cdot g / (m_1 + m_2)\)) oder mit den angezeigten Werten weiterrechnen.
- **Kein Beispiel doppelt**: Clipbeispiel, Kontrollfrage, Leistenziel, Festhalten-Kasten, Mini-Check der
  Themenseite, Kapitelaufgabe und Zufallsübung je mit eigenen Zahlen — der Festhalten-Kasten verrät sonst
  die Aufgabe, und die Kontrollfrage nimmt das Leistenziel vorweg. Feste Werte in die Ausschlusslisten der
  Generatoren, und jede Ausschlussbedingung prüfen, ob sie mit den Wertelisten überhaupt eintreten kann.

- **Was die Kontrollfragen verlangen, bringt der Einführungsclip** (Energie 05.10.2026): Der
  Kontrollclip steht *vor* dem Festhalten. \(P = F \cdot v\) und \(\sigma \cdot T^4\) wurden abgefragt, standen
  aber erst im Festhalten oder gar nicht. Ebenso müssen Formeln, die Übungen und Aufgaben brauchen,
  vorher eingeführt sein (mit Konstante und Einheit, z. B. «T in Kelvin»).
- **Leistenziele auf dem Reglerraster:** Ein richtig gerechnetes Ergebnis muss sich einstellen lassen,
  und das ✓ muss die Physik prüfen, nicht nur die Nähe: «Kuppe erreicht» erst, wenn die Energie
  reicht — sonst gab es ✓ für einen Wagen, der umkehrt. Liegt das Ergebnis zwischen zwei
  Reglerwerten, sagt der Auftrag «auf 0.1 genau» und die Vergleichsantwort, welcher Wert reicht.
- **Startwerte der Regler** sind weder Clipbeispiel noch Leistenziel; sonst löst ein Knopfdruck die
  Aufgabe, deren Antwort der Clip eben vorgerechnet hat.
- **Fragen eines Clips beginnen verschieden:** `pruef-fragen.mjs` erkennt eine offene Frage an den
  ersten 20 Zeichen ihres Texts. Zwei Fragen mit gleichem Anfang («Ein Wagen fährt reib…») lassen
  den Durchlauf-Test (H) die falsche Antwort klicken.
- **Zustand nach Reglerbewegung** (Statik 05.10.2026): Jede Meldung und jeder Pfeil, der zu einem
  Lauf gehört («Die Kiste rutscht», Gleitreibung), verschwindet, sobald ein Regler bewegt wird — der
  Rücksetzer der Simulation setzt *alle* Laufzustände zurück, nicht nur Zeit und Weg.
- **Drehsinn und Richtung physikalisch prüfen:** Ein Schlüssel, der im Uhrzeigersinn dreht, zieht ein
  Rechtsgewinde an; «lösen» heisst gegen den Uhrzeigersinn. Bild und Wort müssen dasselbe meinen.
- **Bezug im Merksatz:** «Gleich gross werden *sie*» zeigte auf Hangabtrieb und Normalkraft statt auf
  Hangabtrieb und grösste Haftreibung. Bei zwei Grössen im Satz das Paar ausschreiben.
- **Ein Gerät, eine Einordnung:** Die Brechstange war im Clip einarmig, in der Aufgabe zweiarmig.
  Beispiele für Begriffe (einarmig, zweiarmig) nur dort nennen, wo sie eindeutig sind.
- **Ergebnis erst nach der Rechnung im Bild:** Eine Simulationsaufnahme mit Endwerten (Auflagerkräfte,
  Gleichgewichtsabstand) erscheint erst, wenn der Ton das Ergebnis sagt — nicht beim Stellen der Frage.
- **Rückmeldungen mit Formeln** («F = M / r», «cos 90°») brauchen `rueck_sprich`, sonst liest die
  Stimme «F gleich M R».
- **Zufallswerte je Gegenstand:** Eine Liste für alle Werkzeuge erzeugt 2000 N Handkraft oder einen
  Schlüssel von 2.7 m. Wertebereiche an den Gegenstand im Text binden.
- **Querverweise «nicht hier»** dürfen nicht im Kreis zeigen (Statik verwies Gleitreibung an das
  Leitprogramm Dynamik, das sie seinerseits auslagert): auf die Stelle verweisen, die den Stoff wirklich hat.
- **Kopierte Kennungen ersetzen** (Hydrostatik 05.10.2026): Wer das Gerüst eines Leitprogramms kopiert,
  ersetzt Speicherschlüssel (`var KEY = 'leitprogramm-<name>-v1'`), Fusszeile, Titel und Stand. Statik trug
  den Schlüssel von Energie — beide Seiten hätten denselben Lernstand gelesen und überschrieben.
  Nach dem Kopieren `grep -n` auf den Namen der Vorlage.
- **Jede falsche Antwort ist ein benannter Fehler:** Distraktoren einer Kontrollfrage entstehen aus einem
  typischen Fehler (Einheit nicht umgerechnet, \(g\) vergessen, Verhältnis umgekehrt), und die Rückmeldung
  nennt genau diesen. «8000 Pa» mit «Mal gerechnet?» passte zu keiner Rechnung; «rund 5 cm» war nicht das,
  was die vergessene hPa-Umrechnung ergibt (0.51 cm).
- **Meldungen aus dem Zustand, nicht aus der Absicht:** Der Text einer laufenden Simulation beschreibt, was
  das Bild am Ende zeigt («Er sinkt langsam weiter»), nicht, was nach der Dichte geschehen sollte — nahe der
  Schwebedichte reicht die Laufzeit nicht bis zur Ruhe.

- **Antwort im Bild** (Kinematik 06.10.2026, Rückmeldung des Auftraggebers): Jede Antwortszene der
  Kontrollclips zeigt die Antwort auch als Bild — Steigungsdreieck mit Δ-Werten und Einheiten, Fläche
  unter der Kurve, Pfeile mit Namen und Betrag, abgelesener Punkt «(5 s; 30 m)». Bei klick-Fragen
  als zweite Ebene `"achsen": false`, damit die Antwort nicht schon während der Frage steht.
  Muster: `scripts/lp/kinematik/antworten.py`.
- **Rechnungen im Diagramm entwickeln:** Im Einführungsclip erscheinen Fläche, Breite, Höhe und
  Ergebnis im Diagramm, wenn der Ton sie nennt (Weg als Dreieck, Trapez = Rechteck + Dreieck);
  Beschleunigung mit Steigungsdreieck und der Einheit als (m/s)/s.
- **Denkauftrag in jeder Leistenaufgabe:** «Stelle ein» oder «Triff die Gerade» allein ist Fingerübung.
  Dazu ein Auftrag zum Notieren, Deuten oder Vergleichen und eine Vergleichsantwort.
- **Bewegte Punkte vollständig beschriften** «(t; s)» und Steigungsdreiecke so setzen, dass ihre
  Beschriftung frei steht (STYLEGUIDE §5.10).

**Gesamttest und Bewertungspaket**
- Jedes Kapitelziel hat eine Aufgabe; kein Modell aus Selbsttest oder Übung wiederholt.
- Raster mit (E) Ergebnis- und (A) Ablesepunkt, typische Fehler mit Restpunkten statt
  Abzügen, gleichwertige Schreibweisen geregelt (Einheiten-Präfixe, Rundung), Folgefehler
  je Aufgabe.
- Selbsteinschätzung verspricht keine Kompetenz, die der Test nicht prüft; jede Aufgabe ist
  einem Kapitel zugeordnet.
- Keine Gesamttest-Aufgabe mit dem Aufbau einer Kapitelaufgabe (Kinematik: Fähre quer, dann vorhalten
  = Aufgabe 4c). Rückwärts fragen, am gegebenen Diagramm ablesen lassen oder begründen lassen.
- Jede Rasterzeile passt zu ihrer Art: Eine Skizze ist kein Begründungspunkt (B), und (B) nur, wo die
  Aufgabe «Begründe» sagt.
- Ein Fehler, ein Abzug — auch über ähnliche Fälle gleich: Zwei Varianten desselben Fehlers (Eigengewicht
  vergessen, Eigengewicht am falschen Ort) kosten gleich viel, und die Folgewerte stehen bei beiden.
- Derselbe Fehler in mehreren Teilaufgaben (dieselbe fehlende Umrechnung in a, b und d) kostet einen Punkt,
  nicht drei — das steht im Raster *und* im Auftrag an die KI.
- Jedes Kapitel hat seine Aufgabe auch im Gesamttest: Hydrostatik prüfte zuerst den Luftdruck doppelt und das
  hydrostatische Paradoxon gar nicht. Zuordnung «Aufgabe → Kapitel» gegen die Kapitelziele lesen.
- Datenschutz: kein Name, keine Standortdaten im Foto.

**Zeit:** geschätzt aus den Teilen, nicht aus der Planung übernommen (§3).

---

## 16 · Erfahrungen aus den Physik-Leitprogrammen

Bestand (03.10.2026): **elf** Leitprogramme, alle im Format «klassisch» — `leitprogramm-rechnen`
und `leitprogramm-vorwissen` fürs Vorwissen; `leitprogramm-waermemenge`, `leitprogramm-heizen`,
`leitprogramm-waermeausdehnung`, `leitprogramm-ideale-gase` und
`leitprogramm-experimente-waerme` für die Thermodynamik; `leitprogramm-schaltungen`,
`leitprogramm-widerstand-leistung` und `leitprogramm-gefahren` für die Elektrizität; dazu die
Übungsprüfung `uebungstest-waermelehre`. Der erste Übertrag (`leitprogramm-ideale-gase`,
31.08.2026) brachte §12, die folgenden die Punkte unten. Jeder stand für ein Problem, das
tatsächlich aufgetreten ist.

- **Der `render-check` (1280 und 360 px) gehört dazu.** In zwei von drei neu geschriebenen
  Dateien (07.09.2026) und wieder in `leitprogramm-experimente-waerme` (08.09.2026) wurden
  lange Inline-Formelketten in Lösungen bei 360 px abgeschnitten, und keine andere Prüfung
  sieht das. Abhilfe wie auf den Themenseiten: die Kette in zwei Formeln teilen, damit die
  Zeile brechen kann — oder sie als abgesetzte Formel `\[ … \]` schreiben.
- **`&lt;` in einer LaTeX-Formel meldet der Pre-Flight als Fehler.** Im Browser
  funktioniert es, weil MathJax den DOM-Text liest; `verify_mathjax.js` liest den
  Quelltext und sieht `&lt;`. Richtig sind `\lt` und `\gt`.
- **Wenn ein Umschalter die Bedeutung des Reglers wechselt** (Fläche gegen Anzahl
  Maschinen, Kraft gegen Druck), müssen `min`, `max`, `step`, `value` und die Beschriftung
  im JS mitgesetzt werden. Sonst zeigt der Regler eine Zahl an, die es im neuen Fall gar
  nicht gibt.
- **Die Auswertungstabellen tragen eine dritte Spalte «ausführlich nachlesen»** mit einem
  Anker auf die zugehörige Themenseite. Das Leitprogramm ist der Kurs, die Themenseite das
  Nachschlagewerk — und beim Auswerten ist der Moment, in dem jemand tatsächlich
  nachschlägt.
- **Die Klassen `.svg-warm` und `.svg-water` sind Flächen, keine Linien** (`fill` mit
  Deckkraft). Als Klasse an einer `<polyline>` färben sie die Fläche unter der Kurve und
  ignorieren ein `fill="none"` im Attribut — CSS gewinnt gegen Präsentationsattribute. Für
  Kurven gehören `.svg-curve` und `.svg-dash` genommen, für Balken die Flächenklassen.
- **Ein Balken darf nie sättigen, während die Zahl daneben weiterläuft.** Mit fester Achse
  (20 bis 32 °C) und einem Regler, der die Mischtemperatur bis 37.8 °C treibt, endet der
  Balken am Achsenende und die Beschriftung widerspricht ihm. Entweder den Reglerbereich
  begrenzen oder — besser — die Skala mitwachsen lassen und die Achsenbeschriftungen im JS
  mitsetzen. Keine Prüfung meldet das; man sieht es nur, wenn man den Regler ans Ende
  zieht (§14, Punkt 9).
- **Punkt 10 (§12) schlägt auch in `.sim-out` zu** (`leitprogramm-schaltungen`,
  13.09.2026): Ein `\(R_\text{ges}\)` in der Anzeigezeile einer Simulation wurde über die
  halbe Simulation hoch gesetzt und war erst im Screenshot zu sehen. Die Kontrolle in §12
  ist entsprechend erweitert.
- **Der `</div>` für `.page` geht beim Zusammenbau verloren**, wenn man den Fuss aus einer
  bestehenden Datei ab `<footer class="site-footer">` herauskopiert: Das schliessende
  `</div>` steht davor. Der Pre-Flight meldet es sauber als «div-Bilanz: 118 offen, 117
  geschlossen» — aber erst, wenn die Datei fertig ist.
- **Eine neue Animation braucht eine Platzhalternummer.** `build-animationen.py` erkennt
  nur `Animation <Zahl> · …`; ein Titel ohne Zahl ist für den Generator unsichtbar und
  bleibt stumm ungezählt. Mit `Animation 0 · …` einsetzen, dann nummeriert der Generator
  richtig durch.
- **Der Einstieg über den Versuch** (`leitprogramm-experimente-waerme`): Jeder Schritt mit
  Vorhersage, Clip, gerechneter Simulation und Auswertung. Neu war nur der Aufbau der
  Schritte; Kopf, `<style>`-Block und Skripte blieben wörtlich aus
  `leitprogramm-waermemenge` — das ist der Weg aus §5.
- **Eine offene Frage über mehrere Schritte** (`leitprogramm-schaltungen`: «40 W oder 60 W
  in Reihe?» bleibt von Schritt 2 bis 6 offen) trägt ein ganzes Leitprogramm.

---

## Nicht tun

- Keine Inhalte jenseits der RLP-Kompetenzen des Teilgebiets.
- Keine Animation der Themenseite kopieren — verlinken (§8a) oder bewusst reduziert
  nachbauen (§8b).
- Keine neuen Beispiele erfinden, wenn die Themenseite ein passendes hat.
- Nicht still angleichen, wenn die Themenseite widersprüchlich ist. Melden.
- **Das Leitprogramm nicht in `page-wrap` + `main.content` pressen.** Es ist ein anderes
  Format als eine Themenseite; das hiesse, sein Layout neu zu bauen.
- **Die Bühne nicht doppelt halten.** Sie steht in `physiklib.js` und `style.css`.
- **Die Palette nicht kopieren.** Sie stimmt heute und läuft morgen auseinander.
- Keinen Ton ins Dokument einbetten (§12, Punkt 11).
