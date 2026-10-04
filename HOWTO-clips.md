# HOWTO — Erklärclip bauen und einbauen

Ein Clip ist eine eigenständige HTML-Datei in `clips/`, die einen einzigen
Gedankengang in rund einer Minute aufbaut: animierte Zeilen auf einer Bühne von
1920 × 1080, dazu eine gesprochene Tonspur. Gebaut wird er nicht von Hand,
sondern aus einem **Drehbuch** — einer JSON-Datei daneben.

Stand 30.09.2026: **205 Clips, 222:51 min, in 25 Reihen.** Zwei Sorten:
**89 Clips zum Stoff** (83:14 min) — jede Themenseite der Lerngebiete 4 bis 6
hat ihre Reihe, dazu das Vorwissen; 50 bis 67 s, Mittel 56 s — und **116 Clips
zu je einer Animation** (139:37 min, Reihe «Animationen erklärt») — jede
Animation der Themen- und Vorwissenseiten hat ihren; 55 bis 87 s, Mittel 72 s.
Einbettungen je Lerngebiet (Mehrfachzuordnungen mitgezählt): Vorwissen 54,
Mechanik 70, Thermodynamik 47, Wellen und Elektrizität 47. Diese Anleitung ist
die Physik-Fassung; das Schwesterprojekt Mathe hat eine eigene mit demselben
Aufbau und — Stand 28.09.2026 — **391 Clips, 361:32 min, in 56 Reihen**.

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
| `theme` | `begreifbar-schlicht` für neue Clips (ohne Karo und Rand, seit 03.10.2026; siehe unten), `begreifbar` in den bestehenden, sonst `heft`, `tafel`, `papier` |
| `stufe`, `schlagworte` | für Suche und Filter |
| `nachlauf` | Standzeit nach der letzten Einblendung; in diesem Projekt `4.0` |
| `probe: true` | baut den Clip, hält ihn aber aus `clips.json` heraus — für Versuche |
| `voraussetzung` | Bedingungsleiste unter der Kopfzeile, siehe unten |

`lektion` ist eine Liste, weil ein Clip mehreren Seiten gehören darf. Er wird
dabei **einmal** gespeichert und mehrfach eingebunden: `p0-3-druck` steht auf
`p0-3`, `p0-2` und `p4-5`. Die Bibliothek zählt einzigartige Clips, nicht
Einbettungen.

### Die Bedingungsleiste `voraussetzung`

Eine schmale Leiste unter der Kopfzeile, die **über den ganzen Clip stehen
bleibt**. Dort steht die Bedingung, auf der alles Folgende ruht: «ohmsch,
Temperatur konstant», «\(p\) konstant», «ohne Reibung». Wer bei Minute zwei
einsteigt, sieht sonst die Rechnung, aber nicht, wofür sie gilt. Die Leiste
liegt ausserhalb des Szenenflusses und kostet darum keine Zeile. Übernommen
aus Mathe (28.09.2026).

```json
"voraussetzung": "p = \\text{konst.}"
"voraussetzung": {"text": "U = 12.0\\,\\mathrm{V}", "tag": "gilt ab", "ab": "Szenenname", "bis": "Szenenname"}
"voraussetzung": [ {…}, {…} ]
```

`tag` ist das kleine Etikett links (Standard «Voraussetzung»); `ab` und `bis`
begrenzen einen Eintrag auf einen Szenenbereich, mehrere stehen nebeneinander.

- **Nur, was von Anfang an gilt.** Was der Clip erst herleitet, gehört nicht
  hinein — sonst steht die Antwort in der Kopfzeile, bevor die Frage gestellt ist.
- **Szenen beginnen dann bei `oben` ≥ 170.** Die Leiste endet bei y = 150; der
  Generator bricht ab, wenn eine Szene höher beginnt. Physiks Schritt-Szenen
  stehen meist auf `oben: 150` und müssen mit einer Leiste um 20 px tiefer. Das
  Band für `mitnehmen` (ab 168 px) kollidiert nicht.
- Verwandt mit `halten`, aber nicht dasselbe: `halten` trägt eine Zeile *aus
  einer Szene* weiter und blockiert dort ihren Platz, die Leiste steht über dem
  *ganzen* Clip.

### Der Szenenbau

Bewährt in allen Clips zum Stoff (die Clips zu einer Animation weichen ab,
siehe «Clips zu einer einzelnen Animation» unten):

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
| `bild` | fertige SVG-Skizze, `datei` relativ zu `clips/` (z. B. `bilder/fi-normal.svg`) | — |
| `graf` | Koordinatenbild mit Geraden, Parabeln, Kurven, Punkten — auch bewegt (siehe unten) | — |

Gemeinsame Felder: `abstand` (Abstand zur nächsten Zeile in Pixel), `groesse`,
`anim` (`rise`, `pop`, `fade`, `wipe`), `ein` (Sekunde in der Szene; ohne Angabe
im Takt von 1.7 s gestaffelt), `x`/`y` für eine eigene Position, `breite`.

**`bild` — die Skizze einer Animation im Clip.** Zuerst am 27.09.2026 als
SVG-Skizze (`p6-2-fi-stromvergleich` zu «FI-Schutzschalter: der
Stromvergleich»); seit dem 28.09.2026 zeigen die Clips zu einer Animation fast
nur noch Aufnahmen der Animation selbst (siehe unten). Die SVG
wird beim Bauen eingegossen, der Clip bleibt eine Datei. Die Skizzen erzeugt
ein Skript neben der Quelle (`.quellen/clip-bilder/fi-schema.py`), das die
Werte aus der Rechnung der Animation nachrechnet — Zahlen im Bild und in der
Animation dürfen nie auseinanderlaufen. Im Schienen-Layout passt eine Skizze
von 1140 × 400 px über Formelzeile, Text und Notiz; `abstand` auf etwa 450
setzen. Das Drehbuch trägt dazu `"animation": "<Anker des h3>"`, die Reihe
`Animationen erklärt` und als `folge` die Nummer der Animation.
`build-clips-einbau.py` setzt dann den Eintrag «▶ Clip» rechts in die
Titelzeile der Animation, neben «Erkenntnis» (zwischen den Markern
`<!-- CLIP-ANIM … -->`, nie von Hand ändern), stellt den Clip auf der
Lektionsseite in eine eigene Gruppe «Clips zu den Animationen» und hebt ihn
dort wie in `clips.html` in Bernstein ab; vor jeder solchen Zeile führt der Link «Anim» zur Animation. Der Titel muss sich klar vom Stoff-Clip zum selben Thema unterscheiden — dieselbe Liste zeigt beide.

`bild` nimmt auch JPG und PNG: Aufnahmen der Animation selbst, gemacht mit
`node .claude/tools/aufnahme-anim.mjs <plan.json>` (Zustände per Klick,
Reglerwert oder JS-Aufruf, doppelte Pixeldichte, JPEG). Knöpfe lieber mit einer
`js`-Aktion auslösen (`document.querySelector(…).click()`): Im Leitprogramm
Elektrizität griffen die Mausklicks nicht, und zwei Clips bekamen Bilder im falschen
Zustand. **Jedes aufgenommene Bild ansehen**, bevor es in einen Clip geht. Das zeigt im Clip
genau das Bild, das auf der Seite steht; eine eigene SVG-Skizze lohnt nur,
wo die Animation etwas nicht zeigen kann.

### Koordinatenbild — `typ: "graf"`

*Aus Mathe begreifbar übernommen (03.10.2026), samt `bewegung`, `fragen` und dem Theme
`begreifbar-schlicht`; der Generator ist in beiden Repos derselbe (`scripts/abgleich.py`,
KERN). In Physik nutzen ihn die Clips `p6-2-lp-*` des Leitprogramms Elektrizität
(Q-t- und R-l-Geraden mit `bewegung`, Kontrollclips mit `fragen`); die Beispiele unten stammen
aus Mathe und zeigen das Format. Die Typen `boxplot` und `rechner` (TI-30X-Anzeige) kennt
der Generator ebenfalls; sie sind Mathe-Stoff und dort in `HOWTO-clips.md` beschrieben.*

Für Clips, die eine Gerade zeigen müssen. Kein Diagrammwerkzeug, nur so viel, wie ein
Clip braucht: Achsen mit Teilung, Geraden über Steigung und Achsenabschnitt, markierte
Punkte. Gezeichnet wird als SVG in den Theme-Farben.

```json
{"typ": "graf", "breite": 800, "hoehe": 620, "abstand": 650,
 "xbereich": [-1, 5], "ybereich": [-1, 8],
 "geraden": [{"m": -2, "q": 7, "farbe": 1, "beschriftung": "y = −2x + 7",
              "beschriftung_bei": [3.55, 1.15]},
             {"m": 2, "q": 1, "farbe": 2, "gestrichelt": true, "dicke": 9}],
 "punkte":  [{"x": 2, "y": 3, "farbe": 3, "beschriftung": "S(2 | 3)"}]}
```

Parabeln gehen genauso, als `parabeln` mit `a`, `b`, `c` für \(y = ax^2+bx+c\) —
gezeichnet als Streckenzug, der ausserhalb des Fensters abbricht und danach wieder
einsetzt.

Die Geraden werden **am Fenster** abgeschnitten, nicht an ihren Endpunkten — eine
Gerade, die aus dem Bild läuft, hört am Rand auf statt an einer willkürlichen Stelle
davor. `farbe` ist 1 bis 4 wie bei den Farbgruppen.

**`beschriftung_bei` gibt es für alle drei** — Geraden, Parabeln und Punkte. Ohne die
Angabe steht die Beschriftung eines Punktes rechts über ihm, und genau dort liegt am
Scheitel einer Parabel die Achsenbeschriftung. Die Koordinaten sind Datenkoordinaten,
nicht Pixel:

```json
"punkte": [{"x": 2, "y": -1, "farbe": 3,
            "beschriftung": "S(2 | −1)", "beschriftung_bei": [2.35, -1.35],
            "anker": "start"}]
```

**Die freie Stelle ausrechnen, nicht schätzen.** Vor dem Setzen kurz prüfen, wo die
Kurve an dieser Stelle verläuft — bei `y = x²` liegt die Kurve an `x = 1.35` auf `1.82`,
ein Label bei `7.6` ist also frei. Vier Kollisionen sind auf diese Weise entstanden und
erst im Bild aufgefallen, nicht in der Prüfung.

### Theme `begreifbar-schlicht` — Standard für neue Clips (in Physik seit 03.10.2026)

Wie `begreifbar`, aber **ohne Häuschenpapier und ohne roten Rand** (`karo: false`,
`rand: false`). Karo und Koordinatengitter eines `graf` stören sich, besonders in Bewegung.
Neue Clips setzen `"theme": "begreifbar-schlicht"`; bestehende bleiben, wie sie sind.
Das Theme kennt eine fünfte Farbe: `farbe: 5` ist Tinte, also «ungefärbt» — für Punkte und
Begleiter im `graf`, die keine der Termfarben tragen sollen (Nullstellen, \((0 \mid c)\),
gegebene Punkte). Farbe 1 ist in Physik Bernstein. (Vorbild in Mathe: In den Clips `g3-3-lp-*` gilt
durchgehend 1 = \(a\), 2 orange = \(x_s\), 3 grün = \(y_s\) bzw. Scheitel.)

### Achsen mit Pfeil und Namen: `pfeile`, `xname`, `yname` (seit 02.10.2026)

`"pfeile": true` setzt Pfeilspitzen in positiver Richtung; `"xname"`/`"yname"` ersetzen die
Beschriftung «x»/«y» — bei Anwendungen mit Grösse und Einheit: `"xname": "x [m]", "yname": "A [m²]"`.
Benannte Achsen werden zuletzt gezeichnet, mit einem Hof in der Papierfarbe, damit eine Kurve sie
nicht überdeckt. Ohne die Felder bleibt das Bild wie bisher (bestehende Clips bauen gleich).
Für neue Clips mit Koordinatenbild: `pfeile` immer setzen.

### Bewegte Parabel und Gerade im `graf`: `bewegung` (seit 02.10.2026)

Statt eines festen Bildes je Szene kann eine Parabel **während der Szene gleiten**:

```json
{"typ": "graf", "xbereich": [-4, 5], "ybereich": [-4, 6], "parabeln": [
  {"a": 1, "gestrichelt": true, "dicke": 3},
  {"bewegung": [[0.8, 1, 0, 0], [3.6, 1, 0, 2]], "farbe": 1, "scheitel": {"farbe": 3}}]}
```

`bewegung` ist eine Liste von Stützpunkten `[t, a, u, v]` für \(y = a(x-u)^2 + v\), `t` in
Sekunden **ab Szenenbeginn**. Dazwischen weich überblendet (smoothstep), vor dem ersten und
nach dem letzten Punkt steht die Parabel still. Ein einziger Stützpunkt ergibt eine stehende
Parabel, an der sich trotzdem Begleiter bewegen können.

Begleiter — alle aus derselben Zeit gerechnet, alle mit `farbe`:

| Schlüssel | zeigt |
|---|---|
| `"scheitel": {}` | Scheitelpunkt mit mitlaufender Beschriftung «S(u \| v)» |
| `"nullstellen": {}` | die beiden Nullstellen; sie laufen zusammen und verschwinden, wenn die Parabel die Achse verlässt; mit `"beschriftung": true` steht «(x \| 0)» daneben |
| `"yachse": {}` | den \(y\)-Achsenabschnitt mit «(0 \| c)» |
| `"marken": [{"x": 0, "text": "h(0) = {y}"}]` | Punkt an festem \(x\) mit Live-Wert |
| `"laeufer": {"bahn": [[t, x], …], "text": "A = {y}", "spiegel": true}` | Punkt, der auf der Kurve fährt; `spiegel` zeigt blass den Partner bei \(2u - x\) |

In `text` stehen `{x}` und `{y}` für die laufenden Werte (eine Nachkommastelle, echtes
Minus).

**Geraden bewegen sich genauso** (seit 03.10.2026). Der Stützpunkt ist `[t, m, q]` für
\(y = m x + q\); gezeichnet wird die am Fenster abgeschnittene Strecke:

```json
{"typ": "graf", "xbereich": [-4, 5], "ybereich": [-5, 6], "geraden": [
  {"m": 2, "q": 0, "gestrichelt": true, "farbe": 5, "dicke": 3},
  {"bewegung": [[0.8, 2, 0], [3.4, 2, 3]], "farbe": 1, "yachse": {"farbe": 2}}]}
```

Begleiter der bewegten Geraden — alle aus derselben Zeit gerechnet, alle mit `farbe`:

| Schlüssel | zeigt |
|---|---|
| `"yachse": {}` | den \(y\)-Achsenabschnitt mit «(0 \| q)»; `"beschriftung": false` lässt den Text weg |
| `"nullstelle": {}` | die Nullstelle mit «(x \| 0)»; verschwindet bei \(m = 0\) |
| `"marken": [{"x": 2, "text": "f(2) = {y}"}]` | Punkt an festem \(x\) mit Live-Wert |
| `"laeufer": {"bahn": [[t, x], …], "text": "{x} \| {y}"}` | Punkt, der auf der Geraden fährt |
| `"dreieck": {"x": -3, "dx": 2}` | mitlaufendes Steigungsdreieck ab \(x\), mit «Δx = …» und «Δy = …» |

In `text` gibt es zusätzlich `{m}` und `{q}`.

**`"ab": x`** (seit 03.10.2026, Physik) lässt eine bewegte Gerade erst bei diesem \(x\)
beginnen — eine \(Q\)-\(t\)- oder \(R\)-\(l\)-Gerade hat keinen Teil bei negativer Zeit
oder Länge. Ohne das Feld reicht sie wie bisher über das ganze Fenster. Begleiter links von
`ab` werden ausgeblendet.

**Prüfbild bei jeder Frage ansehen.** Bis zum 03.10.2026 lasen bewegte Geraden ihre
Startzeit falsch und standen sofort im Endzustand — die Drehbücher waren richtig, nur die
Bilder nicht. Ein Bild bei 0.3 s jeder Fragenszene und eines mitten in jeder Bewegung zeigt
so etwas sofort (`pruef-clip.mjs`, Zeiten aus `sprechzeiten.py`). Die Beschriftung setzt sich selbst auf die
Seite, auf der die Gerade *nicht* verläuft (bei \(m \gt 0\) unter den Punkt, sonst darüber) —
eine freie Stelle von Hand suchen muss man nur bei **festen** Punkten.

Gezeichnet wird im Abspieler, **allein aus der Zeit**: `seek(t)` wird nur in Clips mit
`bewegung` um `bewegen(t)` erweitert (`BEWEGUNG_JS` in `build-clips.py`). Darum stimmen
Pause, Spulen und die Bilder von `pruef-clip.mjs` — ein Prüfbild mitten in der Bewegung
zeigt den Zwischenstand. Alle anderen Clips bleiben beim Neubau Byte für Byte gleich.
«Bewegung reduzieren» im Betriebssystem lässt die Parabel von Stützpunkt zu Stützpunkt
springen statt gleiten.

**Stützpunkte an den Sprechertext legen:** Die Bewegung soll laufen, während der Satz sie
nennt — die Zeiten nach der Vertonung aus der Szenendauer wählen. Bewegungen von 2–3 s
wirken ruhig, unter 1 s hektisch. Geht \(a\) durch 0 (Umklappen), ist die Parabel
kurz eine Gerade — das ist gewollt und zeigt, was dabei passiert.

Im Einsatz (in Mathe): die fünf Clips `g3-3-lp-*` («Parabel sehen», Leitprogramm
Quadratische Funktionen) und die acht Clips `g3-2-lp-*` («Gerade sehen», Leitprogramm
Lineare Funktionen). Noch nicht: bewegte freie Kurven, Live-Zahlen in Formelzeilen.
**Formelzeile und Bewegung abstimmen:** Nennt die Formel links schon den Endwert, soll die
Bewegung früh und kurz sein (unter 2 s) — sonst steht im Text etwas anderes als im Bild.

### Fragen im Clip: `fragen` (Prototyp 02.10.2026)

Ein Clip kann **anhalten und fragen**, bevor der Sprecher die Auflösung nennt — die
Voraussage (predict–observe–explain) wandert in den Clip selbst:

```json
"fragen": [
  {"szene": "u schiebt", "bei": 0.35, "typ": "wahl",
   "text": "Gleich steht in der Klammer x − 2. Wohin wandert die Parabel?",
   "optionen": ["2 nach links", "2 nach rechts", "2 nach unten"], "richtig": 1,
   "rueck": {"0": "Das denken die meisten — wegen des Minus. Schau genau hin …"}},
  {"szene": "Zusammen", "bei": 0.38, "typ": "klick",
   "text": "y = (x − 2)² − 1: Wo landet der Scheitel? Tipp die Stelle ins Bild.",
   "ziel": [2, -1], "toleranz": 0.6, "richtig_text": "Getroffen …",
   "fallen": [{"bei": [-2, -1], "text": "Das Minus in der Klammer heisst rechts …"}],
   "falsch_text": "Nicht ganz …"}
]
```

- `bei` ist die Sekunde **ab Szenenbeginn** — vor `sprecher_bei` (0.4) legen, sonst
  bricht der Satz mitten im Wort ab.
- **Richtig → der Clip rollt sofort weiter** (kurzes ✓, keine Ansage). Nur eine falsche
  Antwort zeigt die Erklärung, liest sie vor und wartet auf «Weiter». Darum werden die
  Rückmeldungen zu richtigen Antworten nicht vertont (`fragen_texte()` lässt sie aus).
- `wahl`: Knöpfe, `rueck` gibt **je Antwort** eine eigene Rückmeldung. Bei einer
  falschen Voraussage die Lösung nicht verraten, sondern aufs Hinschauen lenken — der
  Clip löst sie gleich danach auf.
- `klick`: Tippen ins bewegte Bild der Szene (braucht ein `graf` mit `bewegung` —
  Parabel oder Gerade —, denn dessen Fenster rechnet den Tipp in Koordinaten um). `fallen` sind typische falsche
  Stellen mit eigener Rückmeldung; ein grüner Kreis zeigt danach die richtige Stelle.
  `toleranz` ist ein Abstand in Dateneinheiten — oder `[dx, dy]` je Achse, sobald die
  Achsen verschiedene Grössen tragen (`[0.4, 1.2]` bei \(t\) in s und \(Q\) in C: Sonst
  zählt ein Klick eine Sekunde daneben noch als Treffer). Mit `"eingabe": ["t in s", "Q in C"]`
  bekommt die Frage zwei Zahlfelder als gleichwertigen Weg ohne Maus (Tastatur,
  Screenreader); sie werden wie ein Tipp ausgewertet, `fallen` eingeschlossen. Seit
  04.10.2026 für jede neue `klick`-Frage setzen.
- **Bedienung per Tastatur:** Erscheint eine Frage, liegt der Fokus auf der ersten
  Antwort; Tab, Enter und Leertaste genügen. Die Leertaste schaltet nur ausserhalb von
  Knöpfen Play/Pause, Tastenkürzel wirken nicht in Eingabefeldern. Nach der Frage kehrt
  der Fokus zu Play/Pause zurück.
- **Richtige Antwort nicht immer an derselben Stelle:** `richtig` über die Positionen
  verteilen — am 04.10.2026 hatten alle 24 Auswahlfragen der Physik-Kontrollclips
  `richtig: 0`, und der erste Knopf löste jede. `rueck` bleibt an die Option gebunden,
  nicht an die Stelle; nach einem Umstellen den Frage-Ton neu erzeugen.
- Der Clip hält nur beim **Abspielen** an. Spulen erkennt `FRAGEN_JS` ausdrücklich
  (Klick auf die Zeitleiste, ← →), nicht am Zeitabstand zweier Bilder: Ein Sprung an
  einer Frage vorbei löst sie nicht aus, eine beantwortete Frage kommt beim Zurückspulen
  nicht wieder. Springt dagegen ein *Bild* über eine Frage (langsames Laden,
  Hintergrund-Tab), wird sie gestellt und der Clip an ihre Stelle zurückgesetzt.
  **R** und ein Sprung vor die erste Frage sind ein Neustart: offene Frage, Markierungen
  und Frage-Ton weg, alle Fragen wieder offen. Eine nur weggespulte, unbeantwortete
  Frage bleibt offen. Im Prüfmodus (`?render`, `pruef-clip.mjs`) gibt es keine Fragen.
- Wie `bewegung` nur in Clips mit `fragen` eingebaut (`FRAGEN_JS`); alle anderen bleiben
  Byte für Byte gleich.
- **Vorlesen:** Frage und Rückmeldung spricht dieselbe Stimme wie der Clip, sobald sie
  erscheinen — aber nur, wenn der Ton des Clips an ist. Erzeugt werden die Dateien
  getrennt von der Haupttonspur:
  ```sh
  python3 scripts/build-clip-fragen-ton.py <clip>   # je Text clips/ton/<clip>-f<i>-<schluessel>.mp3
  python3 scripts/build-clips.py <clip>             # danach: der Clip nimmt nur vorhandene Dateien auf
  ```
  Gesprochen wird der Wortlaut aus `sprich`, `rueck_sprich` (je Option), `richtig_sprich`,
  `falsch_sprich` und `fallen[].sprich` — wie beim Sprechertext ausgeschrieben («x minus
  zwei», nicht «x − 2»). Fehlt er, liest die Stimme den angezeigten Text. Welche Texte es
  gibt, steht an einer Stelle (`fragen_texte()` in `build-clips.py`); das Ton-Skript und der
  Abspieler benutzen dieselbe Liste. Das Skript stammt aus Mathe, steht nicht in `abgleich.py` und
  benutzt `sprich()` und `aussprache()` aus dem geteilten `build-clip-ton.py`, ohne es
  zu ändern. Stimme wie beim Clip: `de_DE-thorsten-high` (`PIPER_MODELL` setzen).
- **Lokal testen:** `python3 -m http.server` kann keine Bereichsanfragen; darum springt
  der Ton beim Spulen auf den Anfang zurück. Auf GitHub Pages tritt das nicht auf.

Im Einsatz (in Mathe): `g3-3-lp-verschieben` (drei Fragen) und die vier Kontrollclips
`g3-2-lp-kontrolle-*` (je fünf, `wahl` und `klick` gemischt). Prüfen:
`node .claude/tools/pruef-fragen.mjs clips/<name>.html`.

### Kurven im `graf`: `kurven`, `xteilung`/`yteilung`, `von`/`bis`

Bis zum 07.09.2026 konnte ein `graf` nur Geraden, Parabeln und Punkte. Für die Reihe zu
den trigonometrischen Funktionen kamen drei Dinge dazu.

**`kurven` zeichnet \(y = f(x)\) als Streckenzug.** Im Drehbuch steht die Formel, keine
Punktliste:

```json
{"typ": "graf", "kurven": [
  {"formel": "sin(x)", "farbe": 1, "beschriftung": "y = sin x", "beschriftung_bei": [1.8, 1.35]},
  {"formel": "3*sin(2*x-pi/2)", "farbe": 2}
]}
```

Erlaubt sind `sin cos tan asin acos atan sqrt exp log abs` sowie `pi` und `e` — mehr
nicht. Ein Drehbuch beschreibt eine Kurve, es rechnet nicht.

**Lücken entstehen von selbst.** Wo die Formel keinen Wert liefert oder der Wert aus dem
Fenster läuft, bricht der Streckenzug ab und beginnt danach neu. Genau daran entstehen
die Polstellen der Tangenskurve — im Drehbuch steht kein Wort über Pole.

**`xteilung` / `yteilung` ersetzen die ganzen Zahlen an der Achse.** Eine Sinuskurve
gehört bei \(\pi/2\) geteilt, nicht bei 1, 2, 3. Paare aus Stelle und Beschriftung; die
Beschriftung ist Text, denn das SVG kennt kein LaTeX — also `π/2`, nicht `\tfrac{\pi}{2}`:

```json
"xteilung": [[0, "0"], [1.5708, "π/2"], [3.1416, "π"]]
```

Das Karo folgt der Teilung mit; sonst stünde das Raster bei ganzen Zahlen und die Striche
bei Vielfachen von \(\pi\).

**`von` / `bis` begrenzen eine Kurve auf ein Stück des Fensters.** Gebraucht für
Hilfslinien: Eine Mittellinie `{"formel": "35", "von": 0, "bis": 24.6}` läuft sonst über
die Achsenbeschriftung am linken Rand — im Bild sichtbar, für den Prüfer unsichtbar.

**Zwei Fallstricke, beide beim Bau dieser Reihe bezahlt:**

1. **`abstand` bei einem `graf` ist die Bildhöhe plus rund 30**, kein Zeilenabstand. Mit
   `abstand: 120` unter einem 560 px hohen Bild überlappt die nächste Zeile um 62 px.
   Die Konvention der bestehenden Clips: `hoehe + 30`.
2. **Farbkopplung prüfen.** `farbe: 3` im `graf` und `\fc{…}` im Text sind dieselbe
   Farbe — beide greifen auf `farben` des Themes zu (1 bernstein, 2 orange, 3 grün, 4 rot).
   Wer im Text `\fd{v}` schreibt und die zugehörige Linie mit `farbe: 3` zeichnet,
   koppelt falsch. Der Prüfer sieht das nicht; im Bild fällt es sofort auf.

**Und: die Bedingungsleiste verträgt keine hohe Szene.** Trägt das Drehbuch eine
`voraussetzung`, bricht der Bau ab, wenn eine Szene mit `oben < 170` beginnt. Bei einer
Szene mit grossem Bild ist die Versuchung gross, `oben` klein zu setzen — dann lieber die
Bildhöhe verkleinern.

**Der senkrechte Strich `|` bricht im Fliesstext die Zeile.** Wer in einer Notiz
\(2|a|\) schreiben will, packt es in `@…@` — dort ist der Strich geschützt. Sonst steht
die Hälfte des Satzes auf einer neuen Zeile und die Betragsstriche sind weg.

**`abstand` von Hand setzen**, sonst überschreibt die nächste Zeile das Bild: Der
senkrechte Fluss nimmt ohne Angabe `hoehe` als Abstand, und dann beginnt die nächste
Zeile genau an der Unterkante. Faustregel: `hoehe` plus 30.

In einer Szene mit Merkschiene ist das Bild **nicht** zentriert (dort ist nichts
zentriert) — es steht bei `x`, standardmässig 680. Ein eigenes `x` richtet es an den
Formelzeilen darüber aus.

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

## Clips zu einer einzelnen Animation

Seit dem 28.09.2026 hat jede Animation der Themen- und Vorwissenseiten ihren
Clip (116, Reihe «Animationen erklärt»). Er fasst zusammen, was die Animation
zeigt, und zwar mit ihren eigenen Bildern. Wer eine Animation neu baut, baut
ihren Clip mit.

**Kopf:** wie jeder Clip, dazu `"animation": "<Anker des h3>"`,
`"reihe": "Animationen erklärt"`, `"folge"` = Nummer der Animation auf der
Seite, `lektion` = die Seite. Der Titel unterscheidet sich klar vom Stoff-Clip
zum selben Thema — beide stehen in derselben Liste.

**Szenenbau:** Titel (`zentriert`), vier Schritte (`schiene`, `oben: 150`),
Merksatz. Jeder Schritt beginnt mit einer Aufnahme (`bild`, `breite: 900`,
`abstand: 490`), darunter Formelzeile, Text, Notiz. Der Sprechertext beginnt
mit «In der Animation …» und führt durch vier aussagekräftige Zustände.

**Aufnehmen** mit `node .claude/tools/aufnahme-anim.mjs <plan.json>`:
- Laufende Animationen vorher anhalten (`…Loop.userPaused = true;
  …Loop.stop()`) und ihre Zeit per JS auf einen festen Wert setzen — sonst
  zeigt das Bild einen zufälligen Moment.
- Auf `p0-1` und `p0-2` stehen die Widgets mit ID-Präfix `b` in einer IIFE:
  deren Funktionen sind von aussen nicht erreichbar, Zustände dort per Klick
  oder Reglerwert setzen.
- Zwei Canvas eines Widgets (Momentbild und Mitschrieb) werden einzeln
  aufgenommen und übereinander gesetzt, mit 16 px weissem Streifen.
- **Bildnamen immer mit dem vollen Clipnamen als Präfix**
  (`bilder/p6-1a-anim-puls-1.jpg`). Zwei parallel arbeitende Stränge wählten
  am 28.09.2026 beide `p6-1a-puls-*` und überschrieben sich gegenseitig.
- **Den Aufnahmeplan aufbewahren.** Er lag bisher nur im Scratchpad der
  Sitzung; wurde die Animation später geändert, musste er aus dem Clip
  zurückgewonnen werden.
- **Zustände über ihre Knöpfe setzen, in der Reihenfolge der Animation.**
  Setzt eine Wahl die Animation zurück (Anim. 4 auf 6.2: jede Auftragswahl
  löst die Messleitungen), kommt sie im Plan zuerst. Liegen die Knöpfe in
  einem zugeklappten Aufklapper (Bedienung im Bild, STYLEGUIDE §5.12), klickt
  der Plan sie per JS (`document.querySelector(…).click()`).
- **Bild neben Bedienung** (STYLEGUIDE §5.11) macht das Bild schmaler, und
  manche Zeichnung ordnet sich dann anders an. Neu aufgenommene Bilder mit
  `pruef-clip` prüfen: Anim. 10 auf 6.2 brauchte danach eine kleinere
  Bildbreite im Drehbuch.
- **Die Planbreite entscheidet, welches Bild aufgenommen wird.** Bei einer
  Animation in `.anim-layout` liefert eine Breite ab 1100 px das schmale Bild
  neben der Bedienung, 1099 px das breite einspaltige. Die bestehenden Bilder
  von 6.1a Anim. 1 bis 6 sind breit; ihre Pläne stehen darum auf 1099. Vor dem
  Übernehmen neuer Bilder die Pixelmasse mit den alten vergleichen.
- **Bei schmaler Planbreite die Kopfzeile ausblenden.** Unter 1100 px schiebt
  sich die feste Kopfzeile ins Bild. Erste Aktion jedes Zustands:
  `{"js": "document.querySelectorAll('#nav-root').forEach(function(e){e.style.display='none';});"}`
  (so in den Plänen von 6.1a `puls`, `wackeln`, `gesichter`).

**Zahlen:** Jede Zahl im Clip kommt aus dem Code der Animation, mit python3
nachgerechnet, in **derselben Rundung** wie dort (Stilregel 10). Zeigt die
Animation eine Grösse gar nicht, rechnet der Clip ein ausdrücklich so
benanntes Beispiel.

**Fehler der Animation beheben, nicht umgehen.** Der Clipbau fährt jede
Animation Zustand für Zustand durch und ist darum ihre gründlichste Prüfung:
Am 28.09.2026 kamen dabei rund dreissig Fehler zum Vorschein — verdeckte
Beschriftungen, uneinheitliche Rundung, JavaScript-Zahlen wie `1e-7`, ein
verkehrter Umlaufsinn, ein Widerspruch zwischen Text und gezeigtem Wert.
Solche Fehler an der Animation beheben; ein Clip, der sie nur meidet, lässt
sie auf der Seite stehen.

**Wird die Animation geändert, zieht der Clip mit:** betroffene Bilder neu
aufnehmen, Zahlen in Formelzeilen und Sprechertext angleichen (Sprechertext
geändert → neu vertonen), neu bauen, `pruef-clip`.

**Parallel arbeiten** (mehrere Stränge, je eine Seite oder ein Teil davon):
- Während der Arbeit trägt jedes neue Drehbuch `"probe": true`.
  `build-clips.py` liest und schreibt bei jedem Lauf `clips/clips.json`; ohne
  `probe` überschreiben sich die Stränge den Index gegenseitig.
- `probe` am Ende zentral entfernen, alles neu bauen, dann einmal
  `build-clips-einbau.py --schreiben`, `build-suchindex.py`, `build-seo.py`.
- Solange Stränge laufen, gezielt committen, nie `git add -A` — sonst landen
  halbfertige Dateien im Commit.
- Aussprache-Verdachtsfälle melden die Stränge nur; eingetragen wird nach
  Hörprobe (die Tabellen gelten für beide Repos).

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

**Aussprache-Tabelle.** Liest die Stimme ein Fremdwort falsch, kommt es in
`AUSSPRACHE` in `scripts/build-clip-ton.py`: Wortstamm und Lautschrift (IPA),
Piper erhält es als `[[…]]`. Buchstabierte Abkürzungen stehen in
`ABKUERZUNGEN` (nur exakt als ganzes Wort: FI, LED, COP, SI, dazu «My» als «mü»), einfache
Worttausche ohne Lautschrift in `TAUSCH` (achthundert, Newtonmeter,
Lageenergie). Ebenfalls dort die **Wortfuge**: In Zusammensetzungen erkennt die
Stimme die Fuge nicht und liest «s-t» statt «scht» (Wärme-s-trahlung); ein
Bindestrich nur für die Stimme behebt das (`Wärme-strahlung`). Als allgemeine
Regel angehört und abgelehnt — bei Widerstand, Kilowattstunde u. a. klang es
ohne besser —, darum steht jedes Wort einzeln. Vorsilben (Milli-, Kilo-, Hekto-, …) und Zusammensetzungen
(Amperemeter, Zentripetalkraft) greifen mit. Jeder Eintrag ist nach Hörproben
entschieden; bewusst **nicht** geändert, weil die bisherige Lesart besser
klang: Archimedes, Perihel, Parabel, Mikrometer, Mikro, Volumen, linear, Erdbeschleunigung, Transversal-, Niveau, Photon, Gneis, Basalt, Lumen, Milliarden, Elementarladung, Einholzeit, Gegenrechnung — und als Wortfuge Widerstand, Kilowattstunde, Sonnenstunde, Marktstand, Kohlenstoff, Stickstoff. Die Tabellen sind seit dem 28.09.2026 in Physik und Mathe dieselben — ein neues Wort wird mit Sätzen aus beiden Repos angehört und gilt für beide. Zwei Fallen, beide im Skript abgefangen: Ein Satzzeichen direkt
nach `]]` verschluckt Piper samt Pause und klebt das nächste Wort an — es
gehört in die Klammer. Und ohne Wortgrenze träfe «ampere» auch
«Schlamperei». Probe vor dem Eintrag: `PiperVoice.load(modell).phonemize(text)`
zeigt, was die Stimme daraus macht; Hörproben mit `synthesize_wav`.

*Problemwörter finden* — zwei Durchgänge, am 27.09.2026 über alle Drehbücher:
(1) nach Schreibung: Einheiten, Personennamen, Abkürzungen, Fremdschreibungen
(c, y, ph, th, ou …) phonemisieren und die Lautschrift lesen; (2) über **alle**
Wörter der Sprechertexte (rund 2900): englische Laute (ɹ, ð, θ, w, æ …) und
Wörter mit drei und mehr Silben ohne Hauptbetonung. Der zweite fand
«Zentripetalkraft», das die Stimme englisch las. Ein deutsches Wort, das nur
auf der falschen Silbe betont ist, findet keiner der beiden — das hört man
nur. *Hörproben zeigen:* je Wort «bisher» und «Vorschlag» als WAV, dazu eine
kleine `index.html` mit `<audio>`-Knöpfen im selben Ordner; im Windows-Browser
über `file://wsl.localhost/Ubuntu/<pfad>/index.html` öffnen. Nach einem neuen
Eintrag die betroffenen Clips ermitteln (`aussprache(text) != text`) und neu
vertonen.

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
Seite in Ruhe. Das leere Markerpaar gehört von Hand hinein, **nach der
Zusammenfassung und vor dem Zusatzmaterial** (`<h2 id="downloads">`; ohne
Zusatzmaterial direkt nach der Zusammenfassung); den `<h2 id="clips">Clips</h2>`
bringt der Generator selbst mit.

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
Arbeitsverzeichnis. Im Repo-Wurzelverzeichnis liegen aus solchen Läufen
regelmässig ein paar `szene-*.png` — versioniert ist keines, `.gitignore`
fängt sie ab. Wegräumen schadet trotzdem nicht.

`pruef-mathjax.mjs` braucht eine ausgelieferte Seite, nicht `file://`:

```bash
python3 -m http.server 8912 --directory /home/paps/tals-physik &
node .claude/tools/pruef-mathjax.mjs http://localhost:8912/clips/<name>.html
```

**Spulen und Ton lokal testen:** `python3 -m http.server` beantwortet keine
Range-Anfragen (Antwort 200 statt 206) — der Ton springt dann beim Spulen auf 0,
obwohl der Clip in Ordnung ist. Spulen mit `file://` oder auf GitHub Pages
prüfen (dort 206). In der grossen Bühne bekommt der Clip beim Öffnen den Fokus
(`clipBuehne` in `physiklib.js`), damit ← → spulen und die Leertaste pausiert;
Escape schliesst über einen Listener im Clipdokument, unter `file://`
verweigert der Browser das — dann Knopf oder Klick auf den Rand.

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
nicht die Abschnittsfolge der Seite. Seit dem 08.09.2026 ist der Block ein
reines **Zitat** (STYLEGUIDE §4.1): Was dieses Haus zusätzlich unterrichtet,
steht in den Lernzielen darunter. Für die Clipreihe zählt der **Block**, nicht
die Lernziele — sonst wächst die Reihe über den Lehrplan hinaus. Die Prüfung ist eine Tabelle: jede
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
