# HOWTO — eine Übungsprüfung Aufgabe für Aufgabe erklären

Aus einem Prüfungs-PDF wird eine Seite unter `leitprogramme/`, auf der **jede
Aufgabe** ihren eigenen vertonten Clip hat. Es ist ein Sonderfall des
Leitprogramms: gleiches Skelett, gleicher Kopf, gleicher Fuss, gleiche Klassen —
aber die Gliederung kommt nicht aus dem Stoff, sondern aus dem Prüfungsbogen.

Diese Datei ist aus dem ersten Physik-Durchgang entstanden
(`uebungstest-waermelehre`, 16.09.2026: 15 Aufgaben, 15 Clips, 13:54 min). Jeder
Punkt unten stand für ein Problem, das tatsächlich aufgetreten ist, oder für
eine Zahl, die tatsächlich nachgemessen wurde.

Das Schwesterprojekt hat eine eigene Fassung (`tals-mathe/HOWTO-uebungspruefung.md`,
entstanden am 06.09.2026 aus `uebungspruefung-1`, inzwischen auch für `trigo2`
benutzt). Sie war die Vorlage für den Ablauf — die
Klassennamen, die Prüfwerkzeuge und drei Fallen sind hier aber **andere**; der
Abschnitt «Wo Physik anders ist als Mathe» ganz unten zählt sie auf. Wer aus
einer Physik-Sitzung heraus etwas an Mathe angleichen will: nicht dort
hineinschreiben, sondern einen Eintrag in `scripts/abgleich.py` (Liste `OFFEN`)
setzen — siehe CLAUDE.md.

Verwandte Dokumente: `HOWTO-leitprogramme.md` (das allgemeine Format),
`HOWTO-clips.md` (Drehbücher und Ton), `STYLEGUIDE.md` §2.1, §2.5, §2.7, §2.8,
`CLAUDE.md` (Pre-Flight und Commit-Regel).

---

## Was am Schluss dasteht

```
leitprogramme/<name>.html                   die Seite
clips/<name>-<aufgabe>-<fokus>.json         je Aufgabe ein Drehbuch
clips/<name>-<aufgabe>-<fokus>.html         generiert
clips/ton/<name>-….mp3                      generiert
clips/sprechertext-<name>-….txt             generiert
```

Aufbau der Seite, von oben nach unten:

1. **Wegleitung** — wie man damit arbeitet, als `details.wegleitung` eingeklappt.
   Der erste Punkt lautet immer: *zuerst schreiben, dann lesen.*
2. **Ein Schritt vor allen Aufgaben** — bei einer Prüfungsseite ist das der
   richtige Ort für das, was in jeder Aufgabe gilt: Darstellungsregeln,
   Stoffwerte, eine Tabelle, die mehrere Aufgaben zugleich vorwegnimmt.
3. **Ein `section.step` je Aufgabe** (A1, A2, … C5): Aufgabentext → Clip →
   Musterlösung im `details.sol` → Kasten «typischer Fehler» → Hakenfeld.
4. **Selbstkontrolle und Auswertung** — woran man die eigene Lösung misst und
   welcher Abschnitt welcher Themenseite nachzulesen ist.

**Ein Schritt je Aufgabe, nicht je Teilaufgabe.** Das Hakenfeld speist den
Fortschrittsbalken, und man hakt eine Aufgabe ab, nicht eine halbe. Die
Teilaufgaben a), b), c) stehen als `<ul>` im Aufgabentext und als **fette
Marken** in der Musterlösung.

---

## Schritt 0 — Das PDF lesen, und zwar misstrauisch

**`pdftotext` ist auf dieser Maschine nicht installiert** — `pypdf` dagegen
schon. Also:

```python
import pypdf
r = pypdf.PdfReader(PDF)
for i, p in enumerate(r.pages):
    print("=" * 20, "SEITE", i + 1, "=" * 20)
    print(p.extract_text())
```

**Die Textextraktion verliert Hoch- und Überstriche.** Das ist der teuerste
Fehler in diesem ganzen Ablauf, weil er nicht auffällt: Es kommt ein plausibler
Text heraus, nur eben ein anderer als der gedruckte. In Physik trifft es vor
allem:

| gefährdet | woran man es merkt |
|---|---|
| Zehnerpotenzen \(10^{-6}\) | die Musterlösung rechnet mit einem anderen Faktor |
| Quadrat und Kubik in `m^2`, `cm^3` | Fläche und Volumen werden verwechselt |
| Indizes \(\rho_0\), \(T_1\), \(c_\text{W}\) | fallen zu `0`, `1`, `W` neben dem Symbol zusammen |
| Griechisches im Subset-Font | verschwindet spurlos (siehe CLAUDE.md, RLP-PDF) |

> **Immer beide PDF lesen — Aufgaben *und* Lösungen — und jede Lösung
> nachrechnen. Wo Rechnung und Musterlösung auseinandergehen, ist meist die
> Extraktion schuld, nicht die Musterlösung.**

Im ersten Durchgang war die Extraktion **sauber**. Das ist kein Zufallsbefund,
sondern das Ergebnis von Schritt 1: Alle fünfzehn Musterlösungen wurden
nachgerechnet, und alle fünfzehn stimmten. Ohne diese Probe wüsste man es
nicht — die Kontrolle bleibt also auch dann Pflicht, wenn der Text gut aussieht.

Die Technik, einen Überstrich am Inhaltsstrom des PDF nachzuweisen, steht in
der Mathe-Fassung dieser Anleitung; in Physik war sie bisher nicht nötig.

---

## Schritt 1 — Jede Lösung nachrechnen, keine ausgenommen

Bevor eine Zeile Drehbuch entsteht. Ein einziges Skript, das den ganzen Bogen
durchrechnet und die Werte neben die Musterlösung stellt:

```python
def sig(x, n=3):
    return float(f'%.{n}g' % x)

print(" A2 rho", sig(940 / 120))                      # 7.83 g/cm^3
print(" A4 dA/A", sig(2 * 12.0e-6 * 280 * 100), "%")  # 0.672 %
print(" B2 p2", 980 * 278.15 / 293.15)                # 929.855 hPa
print(" C4 m", sig(26.294 / (2.10*12 + 333.8 + 4.182*4) * 1000), "g")
```

Drei Dinge, an denen es in Physik hängt und die man deshalb einzeln prüft:

- **Kelvin gegen Celsius.** In einem *Verhältnis* muss absolut gerechnet
  werden, in einer *Differenz* ist die Zahl in beiden Skalen dieselbe. Beide
  Fälle kommen im selben Bogen vor.
- **\(\gamma = 3\alpha\) und \(2\alpha\) für Flächen.** Der Faktor ist die
  häufigste Fehlerquelle der Wärmeausdehnung — auch in der eigenen Prüfzeile.
- **Gerundete Zwischenwerte.** Die Musterlösung gibt oft den gerundeten Wert an
  und rechnet mit dem vollen weiter. Wer den gedruckten Wert einsetzt, bekommt
  eine Abweichung und hält sie fälschlich für einen Fehler im PDF. A6 ist genau
  so ein Fall: \(998 \cdot 1.18 = 1178\) gegen \(998 \cdot 1.17810 = 1176\).

Wo die Musterlösung **zwei** Werte angibt (Wasserdichte 998 gegen die
Schulnäherung 1000), gehören beide auch in die Seite. Nicht einer davon
verschwindet, weil er unbequem ist.

---

## Schritt 2 — Die Drehbücher

Alles Übrige steht in `HOWTO-clips.md`; hier nur, was für Prüfungsclips gilt.

### Benennung

```
<seitenname>-<aufgabe>-<fokus>
uebungstest-a4-bohrung
uebungstest-c2-mischtemperatur-rueckwaerts
```

Die Aufgabennummer steht im Namen, sonst findet man unter fünfzehn Dateien
nichts wieder. Der Fokus dahinter sagt, **was der Clip zeigt** — nicht
«Loesung» oder «Teil 3».

### `"probe": true` — der Clip gehört zur Seite, nicht in die Bibliothek

**Jedes Prüfungs-Drehbuch bekommt `"probe": true`.** Das Feld war ursprünglich
für Versuchsclips gedacht und leistet hier genau das Richtige: Der Clip wird
gebaut und ausgeliefert, aber

- er kommt **nicht** in `clips/clips.json`,
- er erscheint **nicht** in der Bibliothek `clips.html`,
- er wird **nicht** auf eine Lektionsseite eingebaut.

Nachgemessen im ersten Durchgang: `clips.json` blieb Zeichen für Zeichen
unverändert bei 86 Einträgen, und `build-clips-einbau.py` meldete «0 Seiten zu
aktualisieren, 16 bereits aktuell». **Schritt 4 des Clip-HOWTO (Einbauen)
entfällt damit** — es gibt nichts einzubauen.

Weil das Feld hier etwas anderes bedeutet als «Versuch», gehört eine Zeile dazu:

```json
"probe": true,
"_probe": "Pruefungserklaerung — gehoert zum Leitprogramm <name>, nicht in die Clip-Bibliothek."
```

`lektion`, `reihe` und `folge` trotzdem sinnvoll ausfüllen. Sie werden heute
nicht ausgewertet, aber wer den Clip später doch in die Bibliothek heben will,
soll nur ein Feld löschen müssen.

### Szenenschema

Sechs Szenen tragen eine Aufgabe zuverlässig, auch eine vierteilige:

| Szene | Layout | `oben` | Inhalt |
|---|---|---|---|
| Titel | `zentriert` | 244 | Aufgabennummer, die Frage, die gegebenen Werte, die Falle als rote `notiz` |
| Schritt 1 | `schiene` | **178** | der Ansatz oder die Beobachtung |
| Schritt 2–4 | `schiene` | **430** | je ein Rechen- oder Denkschritt, das *Warum* als `notiz` daneben |
| Merksatz | `zentriert` | 248 | der übertragbare Satz, **nicht** die Wiederholung des Resultats |

Die `schiene` hat **vier** Einträge. Mehr Szenen als Schienenschritte sind
erlaubt: Zwei Szenen dürfen dieselbe `schritt`-Nummer tragen, dann bleibt der
Eintrag über beide hervorgehoben (in A7 sind das «Wie tief · Gamma» und
«Wie tief · Die Zahlen»).

**Ansatz vor Zahlen gilt auch im Bild.** Wo eine Szene die Formel der
vorherigen einsetzt, trägt jene Formel `mitnehmen: true` — sonst steht die
Zahlengleichung allein da und das Prinzip ist nicht mehr zu sehen.

### Drei Fallen, die im ersten Durchgang zuschlugen

**Es gibt genau vier Farbmakros: `\fa`, `\fb`, `\fc`, `\fd`.** Ein erfundenes
`\fe{\rho}` wird von MathJax nicht aufgelöst; in drei Drehbüchern stand es.
Gebaut wird der Clip trotzdem — der Fehler zeigt sich erst im Bild. Wer eine
fünfte Grösse führen will, lässt sie **ungefärbt** (das ist ohnehin die bessere
Wahl: zwei bis drei Farben je Clip reichen).

```bash
grep -o '\\\\f[e-z]{' clips/<name>-*.json | sort -u   # muss leer sein
```

**`halten` verlangt den Szenennamen auf das Zeichen genau.** Steht dort
«Schritt 2 · Wie tief», die Szene heisst aber «Schritt 2 · Wie tief · Gamma»,
bricht `build-clips.py` **nur diesen einen Clip** ab:

```
halten verweist auf unbekannte Szene: Schritt 2 · Wie tief
```

In einer Schleife über fünfzehn Clips geht diese Zeile zwischen den
Fortschrittsausgaben unter, und am Schluss liegen 14 statt 15 HTML-Dateien da.
Darum **nach dem Bauen zählen**:

```bash
ls clips/<name>-*.html | wc -l      # muss der Anzahl Drehbücher entsprechen
```

**Backslashes in Python-Strings.** Wer die Drehbücher mit einem Python-Skript
schreibt: `"\;"` ist keine gültige Escape-Sequenz, Python lässt sie stehen und
warnt. Das Ergebnis im JSON stimmt zwar, aber die Warnungen verdecken echte
Meldungen. `r"..."` benutzen.

### Sprechertext

- **Zahlen als Wörter**, Messwerte als Stellenfolge: «sieben Komma acht drei»,
  nicht «7.83». Warum, steht in CLAUDE.md unter `build-clip-ton.py`.
- Ein bis drei Sätze je Szene. Die Einblendungen kommen im Takt von 1.7 s — viel
  mehr Text als Zeilen, und die Stimme läuft dem Bild davon.
- **`"nachlauf": 4.0`** setzen, wie bei allen Clips dieses Projekts.

---

## Schritt 3 — Vertonen und bauen

Die Reihenfolge ist zwingend: Ton misst die Dauern, Bau setzt sie ins HTML.

```bash
export PATH="$HOME/.local/bin:$PATH" \
       PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx

for f in clips/<name>-*.json; do n=$(basename "$f" .json)
  python3 scripts/build-clip-ton.py "$n"; done
for f in clips/<name>-*.json; do n=$(basename "$f" .json)
  python3 scripts/build-clips.py    "$n"; done
```

Gemessen im ersten Durchgang: **16.2 s je Clip** für die Vertonung (15 Clips in
227 s). Der Bau danach fällt nicht ins Gewicht — vierzehn Clips lagen innerhalb
**einer Sekunde** fertig da. Die Vertonung im Hintergrund laufen lassen und
derweil die Seite schreiben; der Bau ist ein Zwischenruf.

**Erst danach stimmen die Laufzeiten.** Vorher schätzt der Generator aus der
Wortzahl. Die fünfzehn Clips landeten zwischen 54 und 58 s — mitten im Zielband
von 45 bis 90 s aus der didaktischen Prüfliste.

### Die Laufzeiten in die Seite holen

Nicht abtippen. Im Markup einen Platzhalter setzen und danach füllen:

```html
<span class="clip-zeit" data-zeit="uebungstest-a1-einheiten">0:00</span>
```

```python
sek = round(sum(sz['dauer'] for sz in d['szenen']) + d.get('nachlauf', 0))
zeit = f'{sek // 60}:{sek % 60:02d}'
```

Der `nachlauf` gehört dazu — er ist Teil der Spielzeit, die der Betrachter sieht.

---

## Schritt 4 — Layout aller Clips prüfen

Nicht am geschätzten Raster, sondern an den **echten Szenenenden**. Zwei Marken
je Szene (Mitte und kurz vor Schluss) sind dicht genug:

```python
import json, glob, os
for f in sorted(glob.glob('clips/<name>-*.json')):
    d = json.load(open(f, encoding='utf-8')); t = 0.0; m = []
    for sz in d['szenen']:
        t += sz['dauer']
        m += [round(t - 1.0, 1), round(t - sz['dauer'] / 2, 1)]
    print(os.path.basename(f)[:-5], ' '.join(str(x) for x in sorted(set(m))))
```

Die Ausgabe direkt an den Prüfer geben:

```bash
export SP=/pfad/zum/ablageordner
while read -r name rest; do
  node .claude/tools/pruef-clip.mjs "clips/$name.html" $rest
done < zeiten.txt
```

Erwartet wird je Clip «keine Überlappungen, nichts ausserhalb der Bühne». Die
**unterste Kante** in der Ausgabe ist die zweite Kontrolle: Sie blieb im ersten
Durchgang überall unter 964 px, die Bühne ist 1080 px hoch.

`$SP` setzen, sonst landen die Bilder im Arbeitsverzeichnis. **Und die Bilder
ansehen** — der Prüfer sieht Überlappung und Überlauf, nicht Gestaltung.

---

## Schritt 5 — Die Seite

Kopf, `<style>`-Block, Fortschritts- und Clipkarten-Skript **wörtlich** aus
einem bestehenden Leitprogramm übernehmen (`leitprogramm-experimente-waerme.html` ist eine
klassische Vorlage; `leitprogramm-schaltungen.html` ist seit dem 06.10.2026, `leitprogramm-heizen.html`
seit dem 08.10.2026 veraltet). Neu geschrieben wird nur der Inhalt.

### Die Falle, die diesen Durchgang gekostet hat: `</head>`

Wer den Kopf programmatisch herausschneidet —

```python
kopf = src[:src.index("</head>")]      # schneidet </head> WEG
kopf = src[:src.index("</head>")] + "</head>"    # so ist es richtig
```

— sonst verliert man das schliessende Tag. Und dann:

> **Der Pre-Flight meldet das nicht.** Nachgemessen: Mit fehlendem `</head>`
> lief er auf `ALLE CHECKS BESTANDEN` durch, inklusive 235 fehlerfrei
> gesetzter Ausdrücke. Seine Tag-Bilanz zählt `div` und `details`, nicht `head`.

Gemeldet hat es ein anderes Werkzeug:

```
leitprogramme/<name>.html     0 Abschnitte
```

`build-suchindex.py` überspringt den `<head>`-Inhalt und findet das Ende nie —
die **ganze Seite** verschwindet aus der Volltextsuche, lautlos. Die Kontrolle
ist deshalb die Abschnittszahl nach dem Indexlauf. Sie ist **Anzahl `h2[id]`
plus eins**: Der erste Eintrag trägt keinen Anker und hält Titel und Vorspann.
Im ersten Durchgang: 20 Überschriften, 21 Abschnitte.

### Welche Klassen benutzt werden

**Keine erfinden** (CLAUDE.md). Alles Nötige steht im geerbten `<style>`-Block:

| wofür | Klasse |
|---|---|
| Abschnitt je Aufgabe | `section.step.prose` mit `.step-head`, `.step-num`, `h2.step-title`, `.step-goal` |
| Einstiegsfrage | `.frage` |
| Aufgabentext | `.task` mit `<span class="task-id">A1</span>` |
| Punkte, falls sie bleiben | `<span class="pts">3 P</span>` innerhalb der `.task-id` |
| Kern gegen Vertiefung | `<span class="kern">` / `<span class="vert">` |
| Musterlösung | `details.sol > summary` + `.sol-body` |
| Merksatz, Hinweiskasten | `.merksatz`, `.card` mit `.card-label` |
| Tabelle | `.table-scroll > table`, erste Spalte `td.q` |
| Abbildung | `figure > .fig-frame > svg` + `figcaption`, SVG-Klassen `.svg-axis`, `.svg-curve`, `.svg-dash`, `.svg-grid`, `.svg-label`, `.svg-label-em` |
| Clipkarte | `.clipkarte` mit `data-clip` und `data-titel` |
| Hakenfeld | `label.done-row` mit `data-step` |

Die Clipkarte sitzt **zwischen** Aufgabentext und Lösungsaufklapper und braucht
in Physik keine Sonderregel: `.task` hat keine Nummernspalte, die sie zerreissen
könnte.

Der Fortschritts-Schlüssel wird je Seite neu vergeben:

```js
var KEY = 'leitprogramm-<name>-v1';
```

### Was sonst noch zu beachten ist

- **`\lt` und `\gt`, nie `&lt;`/`&gt;`.** Der Pre-Flight liest den Quelltext und
  meldet die Entität als Fehler.
- **Lange Formelketten abgesetzt** (`\[ … \]`), nicht inline. Sonst werden sie
  bei 360 px geschrumpft, statt zu brechen — in diesem Durchgang durchgehend so
  gemacht, und der `render-check` blieb sauber.
- **Kein LaTeX in `figcaption`, `.step-goal`, `.sim-lab`, `.sim-out`,
  `.scene-cap`** (HOWTO-leitprogramme Punkt 10). Kontrolle:
  ```bash
  grep -n 'class="step-goal"\|<figcaption>\|class="sim-out"' <datei> | grep -c '\\('
  ```
  muss **0** ergeben.
- **Der Malpunkt ist Multiplikation, kein Trennzeichen** (STYLEGUIDE §2.1).
  Getrennt wird mit Strichpunkt. Ausgenommen sind Titel, Fuss und Breadcrumbs —
  und die sind auf dieser Seitenart fast die einzigen Stellen, an denen ein `·`
  überhaupt vorkommen darf.

### Ein roter Faden vor den Aufgaben

Was die Seite über eine Sammlung von Lösungen hebt, ist der Abschnitt, der
mehrere Aufgaben zugleich erklärt. Im ersten Durchgang war das der Schritt
**«Die Darstellung»** — vier Regeln, die in jeder der fünfzehn Aufgaben
wiederkehren, dazu dieselbe Rechnung einmal knapp und einmal richtig
aufgeschrieben. Solcher Abschnitt gehört **vor** die erste Aufgabe, und was
darin steht, wird in den Fehlerkästen wieder aufgegriffen.

---

## Schritt 6 — Eintragen, oder bewusst nicht

Eine Übungsprüfung ist nicht immer für die ganze Welt gedacht. Zwei Wege.

### a) Öffentlich, wie jedes Leitprogramm

| Datei | was |
|---|---|
| `leitprogramme.html` | Karte im Block zwischen den `LEITPROGRAMME`-Markern (von Hand gepflegt, kein Generator) |
| `scripts/build-seo.py` | Zeile in `SEITEN`, **ohne** `noindex` |
| `scripts/build-suchindex.py` | nichts zu tun — alles in `leitprogramme/` wird automatisch erfasst |

Danach `python3 scripts/build-seo.py` und `python3 scripts/build-suchindex.py`.

**Und nach dem ersten Commit noch einmal `build-seo.py`.** Das `dateModified`
im JSON-LD und das `lastmod` in der Sitemap kommen aus dem **Git-Datum** der
Datei. Solange die Seite unversioniert ist, gibt es keines — sie erbt dann das
Datum, das im kopierten Skelett stand (im ersten Durchgang: `2026-08-01`, ein
Monat zu früh). Der Pre-Flight meldet das anschliessend brav als
«[WARN] seo: Metadaten/sitemap veraltet»; ein zweiter Lauf und ein zweiter
Commit räumen es auf.

### b) Unverlinkt, nur über den Direktlink

**Hier weicht Physik von Mathe ab, und zwar entscheidend.**
`build-suchindex.py` liest das Verzeichnis `leitprogramme/` **vollständig** aus:

```python
for datei in sorted(os.listdir(lp)):
    if datei.endswith('.html'):
        seiten.append({...})
```

Eine Seite, die dort liegt, lässt sich also **nicht** dadurch aus der
Volltextsuche halten, dass man einen Eintrag weglässt — es gibt keinen Eintrag,
den man weglassen könnte. Wer sie wirklich unauffindbar will, legt sie
**ausserhalb** von `leitprogramme/` ab. Das Muster dafür steht schon im Repo:
`loesungen/gravitation-und-elektronen-im-feld.html` — nachgeprüft, es kommt in
`suchindex.js` nicht vor.

| | |
|---|---|
| Ablage | eigener Ordner, z. B. `loesungen/` — **nicht** `leitprogramme/` |
| `leitprogramme.html` | **keine** Karte |
| `scripts/build-seo.py` | Eintrag **mit `noindex=True`** — nicht weglassen, sonst fehlen Beschreibung und canonical |

`noindex=True` nimmt die Seite aus `sitemap.xml` **und** setzt
`<meta name="robots" content="noindex, nofollow">` in den generierten Kopfblock.
Beides zusammen ist nötig: Die Sitemap allein hält keine Suchmaschine ab, die
die URL anderswoher kennt.

**Kein `Disallow` in `robots.txt`.** Die Datei ist öffentlich lesbar; ein
Eintrag dort würde die URL gerade bekanntmachen, statt sie zu verbergen.

**Und die Grenze aussprechen:** Das ist Unauffindbarkeit, keine Zugangskontrolle.
Wer den Link hat, kommt hinein, und wer ihn weitergibt, gibt den Zugang weiter.
Für echten Schutz bräuchte es etwas anderes als GitHub Pages.

---

## Wenn der Prüfungsrahmen wegbleiben soll

Im ersten Durchgang lautete der Auftrag, **die Rahmenbedingungen und den
Einleitungsteil des Tests wegzulassen und nur den Aspekt der Darstellung zu
behalten**. Das ist eine sinnvolle Bestellung — der Bogen wird damit vom
Prüfungsdokument zum Lehrmittel — und sie zieht ein paar Entscheidungen nach
sich, die man besser einmal festhält.

**Weg:** Punkte je Teilaufgabe und Punktesumme, Notenformel und
Bestehensgrenze, Bearbeitungszeit als Prüfungszeit, Schule, Klasse und
Schuljahr, der «Aufbau»-Absatz, der erklärt, wie das PDF gebaut ist — und die
Aufforderung, den Bogen am Stück unter Prüfungsbedingungen zu schreiben.
Damit entfällt auch die `.pts`-Marke im Markup und die Punktezeile unter der
Lösung.

**Bleibt:** alles, was zum Rechnen gebraucht wird. Die **Stoffwerteliste** ist
keine Rahmenbedingung, sondern Arbeitsmaterial — ohne \(c_\text{W}\),
\(L_f\) und die \(\alpha\)-Werte ist keine Aufgabe lösbar. Sie wandert in den
Schritt vor den Aufgaben, unter einer Überschrift, die sie als Werkzeug
ausweist («Stoffwerte, mit denen hier gerechnet wird»), nicht als Vorgabe.
Ebenso bleibt ein Hinweis wie «die Tabelle gibt 998, die Schulnäherung 1000 ist
ebenso gültig» — das ist Physik, nicht Prüfungsorganisation.

**Und die Darstellung wird zum roten Faden statt zu einer Zeile im Kopf.**
Aus dem einen Satz des Bogens werden drei Orte auf der Seite:

1. ein eigener Schritt **vor** der ersten Aufgabe, mit den Regeln einzeln
   begründet und einem Beispiel «so nicht / so»,
2. die Musterlösungen selbst, die die Regeln durchgehend vorführen —
   Ansatz symbolisch, dann Zahlengleichung mit Einheiten, dann Resultat,
3. eine **Selbstkontrolle am Schluss**, die dieselben Regeln als Fragen an die
   eigenen Blätter stellt.

Der Ersatz für den entfallenen Kapiteltest ist genau diese Selbstkontrolle:
Ein Leitprogramm braucht am Ende einen Punkt, an dem man das Eigene prüft —
nur misst man hier die Form, nicht noch einmal die Zahlen.

---

## Schritt 7 — Prüfen

```bash
python3 .claude/skills/preflight/preflight.py \
        leitprogramme/<name>.html leitprogramme.html clips/<name>-*.html
node .claude/tools/render-check.mjs leitprogramme/<name>.html leitprogramme.html

python3 -m http.server 8912 --directory /home/paps/tals-physik &
node .claude/tools/pruef-mathjax.mjs http://localhost:8912/leitprogramme/<name>.html
for f in clips/<name>-*.html; do
  node .claude/tools/pruef-mathjax.mjs "http://localhost:8912/clips/$(basename $f)"
done
```

Erwartet: `ALLE CHECKS BESTANDEN`, `RENDER-CHECK BESTANDEN`, und je Datei
`merror: 0`. Der `[WARN] abgleich` ist kein Blocker — aber nachsehen, ob man
ihn selbst verursacht hat (`git status scripts/abgleich.py`).

**Was keine Prüfung sieht** — dafür in den Browser, hell **und** dunkel, 1280 px
**und** 360 px:

- **Ein fehlendes `</head>`** (siehe Schritt 5). Kontrolle ist die
  Abschnittszahl von `build-suchindex.py`, nicht der Pre-Flight.
- **Beschriftungen, die sich in einer SVG-Skizze überlagern.** Im ersten
  Durchgang lagen die Marke «1295» und die Achsenbeschriftung «Q in kJ»
  übereinander — beide rechts unten, in zwei Textknoten, die nichts
  voneinander wissen. Keine Prüfung meldet das; es stand im Screenshot.
- **Griechisches, das wie eine Ziffer aussieht.** «ϑ in °C» als Achsentitel
  liest sich bei 10.5 px wie «9 in °C». Abhilfe ist nicht eine andere Schrift,
  sondern ein Wort davor: «Temperatur ϑ in °C», «Wärme Q in kJ».
- **Der Ton beim Spulen.** `python3 -m http.server` kann keine Range-Requests;
  der Klick auf den Fortschrittsbalken wirft den Ton an den Anfang zurück. Das
  sieht wie ein Fehler im Clip aus und ist keiner.
- Dazu die fünf Punkte aus `HOWTO-leitprogramme.md` («Was keine Prüfung sieht»).

Zuletzt: `ls clips/<name>-*.html | wc -l` gegen die Anzahl Drehbücher, und
`git status --short clips/clips.json` muss **leer** sein — sonst hat ein
Drehbuch sein `probe`-Feld nicht.

---

## Wo Physik anders ist als Mathe

Wer die Mathe-Fassung kennt, findet hier vier Unterschiede. Alle nachgeprüft:

| | Mathe | Physik |
|---|---|---|
| Aufgabenmarkup | `.test`, `.aufg`, `.loes`, `.inhaltbox`, `.merk`, `.pkt-hinweis` | `.task`, `details.sol`, `.sol-body`, `.card`, `.merksatz` — die Zusatzregeln für `.clipkarte.zu-aufg` und `.pkt-hinweis` braucht es hier **nicht** |
| Clip-Prüfung im Pre-Flight | `check_clips` vorhanden | **gibt es nicht** — die Konsistenz der Clipablage prüft in Physik niemand automatisch |
| Unverlinkte Seite | Eintrag in `build-suchindex.py` weglassen | geht nicht: `leitprogramme/` wird komplett eingelesen — Seite ausserhalb ablegen |
| Granularität | ein Clip je **Teil**aufgabe (26 Clips) | ein Clip je **Aufgabe** (15 Clips), Teilaufgaben innerhalb des Clips |

Die letzte Zeile ist eine Entscheidung, keine Vorschrift. Bei vier
Teilaufgaben, die aufeinander aufbauen (B2: Unterdruck, Kraft, Masse, Dichte),
trägt ein Clip mit vier Schritten den Zusammenhang besser als vier Clips, die
ihn zerschneiden. Umgekehrt gehört eine Teilaufgabe, die einen eigenen
Gedankengang hat, in einen eigenen Clip.

---

## Aufwand — was der erste Physik-Durchgang gekostet hat

| | |
|---|---|
| Aufgaben | 15 (A1–A7, B1–B3, C1–C5) |
| Clips | 15, zusammen 13:54 min, je 54 bis 58 s |
| Vertonung | 227 s Rechenzeit (16.2 s je Clip, Thorsten) |
| Clipbau | vernachlässigbar — 14 Clips in rund 1 s |
| Tonspuren | 4.0 MB |
| Seite | 1907 Zeilen, 235 gesetzte Ausdrücke (mit Clips 486) |
| Suchabschnitte | 21 |
| Fehler aus der PDF-Extraktion | 0 von 15 — nachgewiesen durch Nachrechnen, nicht vermutet |
| Fehler, die erst ein Werkzeug zeigte | 3 (fehlendes `</head>`, erfundenes `\fe`, `halten` auf falschen Szenennamen) |
| Fehler, die erst der Browser zeigte | 2 (überlagerte SVG-Beschriftung, ϑ wie eine Ziffer) |
