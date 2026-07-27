# TALS-Physik · Styleguide

**Version 1.1 · Stand: Juni 2026** · (1.1: §3.6 Label-Robustheit, §3.7 Einheiten-Zweitzeile, §5.3 Gruppierung, §5.8 Direkt-Manipulation — Referenz-Implementierung p4-1 Einstiegs-Animation, Phasen 5.28–5.30)

Verbindliche Referenz für alle Themenseiten des Lehrmittels „TALS-Physik". Sichert Konsistenz in Notation, Aufbau, Sprache und visuellem Design — themenübergreifend und chatübergreifend.

Geforkt aus dem Styleguide von TALS-Mathematik (v1.8); nur die für Physik abweichenden Punkte sind hier ausführlich behandelt. Wo nichts anderes steht, gilt die Mathe-Konvention identisch weiter.

---

## 1. Verbindliche Quellen

| Bereich | Quelle |
|---|---|
| Notation, Symbole, Einheiten | **SI-Einheitensystem** (BIPM 2019) · DIN 1304 für Formelzeichen |
| Lehrziele, Kompetenzen | **RLP-BM 2030** (Rahmenlehrplan vom 13. Juni 2025, ab 2030 verbindlich), Ziff. 7.5.4.1 (Gruppe 1: Technik, Architektur, Life Sciences) |
| Hilfsmittel-Status | **SBFI-Hilfsmittel-Liste Mathematik/Physik** + **Formelsammlung für die Berufsmaturität** (HEP-Verlag) — offizielle BM-Hilfsmittel |
| Vollständigkeit, Beispiel-Steinbruch | Gescanntes Physik-Skript der BM (im Project-Knowledge, nur als Referenz — keine wörtliche Übernahme) |

**Sprachregelung:**
- „RLP-BM 2030" — verbindliche Schreibweise
- „Berufsmaturität Technik, Architektur, Life Sciences" — Vollform; Kürzel **TALS** nur in Logos/Pills
- Keine Abkürzungen für Lerngebiete („LG4" o.ä.) — immer „Lerngebiet 4 Mechanik"

---

## 2. Physikalische Notation

### 2.1 Multiplikation

- **Mit Multiplikationspunkt** (`·`) zwischen Zahl und Variable in **Live-Anzeigen** (interaktive Widgets), Tabellen, Formelboxen:
  `v = 9.81·t` ✓
- **In LaTeX:** `\cdot` für den Punkt; `*` ist verboten.
- **In LaTeX-Display-Formeln** darf `\cdot` weggelassen werden, wenn Multiplikation typografisch eindeutig ist (z.B. `v_0 t`), aber bei Zahl·Variable (`2 \cdot t`) und bei mehreren Skalaren (`v_0 \cdot \cos\alpha`) IMMER setzen.
- **Vektor·Skalar** und **Skalarprodukt**: immer mit `\cdot` (`\vec{F} \cdot \vec{s}`).
- **Der Punkt ist reserviert (verbindlich, Stichwort «Stilcheck»):** In allen
  **Rechen- und Wertanzeigen** — `.fl-eq`, `.lb-val`, Canvas-Beschriftungen mit
  Zahlen, Lösungswege — bedeutet `·` ausschliesslich Multiplikation und wird
  **nie** als Trennzeichen verwendet. Das ist dort nicht bloss unschön, sondern
  falsch lesbar: `… = 83 °C · ΔT = …` liest sich als Produkt. Stehen zwei
  Gleichungen nebeneinander, bekommt **jede eine eigene Zeile** (mehrere
  `.fl-eq` in derselben `.formel-live`; `style.css` setzt den Abstand über
  `.fl-eq + .fl-eq`).
  *Nicht betroffen:* Titel, Breadcrumbs, Quellen- und Fusszeilen
  (`Physik · Lerngebiet 5`, `Animation 4 · Doppelter Zahlenstrahl`) — dort ist
  der Punkt etablierte Typografie ohne Rechenkontext und bleibt.
- **Ansatz vor Werten, auch in Live-Anzeigen (verbindlich, Stichwort «Stilcheck»):**
  Eine `.fl-eq` nennt zuerst die Formel symbolisch, dann erst die Zahlen:
  `Δϑ = ϑ₂ − ϑ₁ = 95 − 12 = 83 °C` ✓, nicht `Δϑ = 95 − 12 = 83 °C` ✗.
  Das ist das Ansatz-Prinzip aus CLAUDE.md, angewandt auf die Widgets — die
  Live-Zeile soll zeigen, *welche* Beziehung gerade ausgerechnet wird.
  Referenz: `themen/p5-1-temperatur.html`, Animation 4.

### 2.2 Vektoren und Skalare

| Was | Schreibweise | Beispiel |
|---|---|---|
| Skalare (Beträge) | kursiv | $v$, $a$, $t$, $m$ |
| Vektoren | mit Pfeil | $\vec{v}$, $\vec{a}$, $\vec{F}$ |
| Komponenten | mit Index | $v_x$, $v_y$, $F_z$ |
| Einheitsvektoren | mit Dach | $\hat{e}_x$ |
| Mittelwert | mit Querstrich | $\bar{v}$ |

In LaTeX:
```latex
\vec{v} = v_x \cdot \hat{e}_x + v_y \cdot \hat{e}_y
```

### 2.3 Einheiten

- **SI-Einheiten** als Standard. Üblicherweise zusätzlich angegebene Praxiseinheiten: km/h, kWh, °C, bar — immer mit Hinweis auf die Umrechnung.
- **Zwischen Zahl und Einheit:** kein normales Leerzeichen, sondern **geschütztes Leerzeichen** in HTML (`&nbsp;`) bzw. `\;` in LaTeX:
  `9.81\;\text{m/s}^2` ✓
- **Einheit ist nicht kursiv**: Variable kursiv, Einheit aufrecht. In LaTeX die Einheit immer in `\text{...}` setzen.
- **Bruchstrich bei Einheiten:** `m/s` oder `m·s⁻¹`; die Slash-Variante ist üblicher und in der BM-Formelsammlung dominant.

### 2.4 Konstanten

| Konstante | Wert (BM-rundungstauglich) | Symbol |
|---|---|---|
| Erdbeschleunigung | $g = 9.81\;\text{m/s}^2$ | $g$ |
| Schallgeschwindigkeit (Luft, 20°C) | $c_S \approx 343\;\text{m/s}$ | $c_S$ |
| Lichtgeschwindigkeit (Vakuum) | $c \approx 3.00 \cdot 10^8\;\text{m/s}$ | $c$ |
| Spezifische Wärmekapazität Wasser | $c_W = 4.19\;\text{kJ/(kg·K)}$ | $c_W$ |
| Dichte Wasser (4°C) | $\rho_W = 1000\;\text{kg/m}^3$ | $\rho_W$ |

Im JS-Code von Themenseiten als globale `const` gleich am Anfang der `<script>`-Sektion definieren (siehe `themen/p4-1-kinematik.html` für das Muster).

### 2.5 Dezimalpunkt (Schweizer Schul-Konvention)

**Schweizer Schul-Konvention**: Dezimal**punkt**, nicht Dezimalkomma. Gilt einheitlich für TALS-Mathe und TALS-Physik.

- **In Aufgabentexten und LaTeX-Werten**: `9.81\;\text{m/s}^2`, nicht `9,81` oder `9{,}81`.
- **In Live-Anzeigen** (über `fmt()` aus `physiklib.js`): automatisch Punkt (JS `toFixed` liefert Punkt von Haus aus).
- **In JS-Code-Literalen** (Slider-`min`/`max`/`step`, Konstanten wie `const g = 9.81`): Punkt — passt zu allem anderen.
- **Konvertierungs-Werkzeug**: bei Bedarf `scripts/convert_decimals.py` aufrufen — wandelt sicher Dezimalkomma → Dezimalpunkt um, ohne Koordinaten-Tupel, LaTeX-Subscripts, Google-Fonts-URLs oder SVG-Attribute zu zerschiessen.

### 2.6 Schreibweise von Werten und Toleranzen

- Signifikante Stellen: in der BM üblicherweise **3 Stellen** Genauigkeit. Endergebnisse passen ihr Stellenwerk an die Eingangsdaten an.
- Vorzeichen: bei negativen Werten Unicode-Minus `−` (U+2212) in Live-Anzeigen verwenden, nicht ASCII-Bindestrich `-`. Die `fmtS()`-Funktion in `physiklib.js` macht das automatisch.

---

### 2.6b Preis und Kosten sauber trennen (verbindlich, Stichwort «Stilcheck»)

Zwei Grössen, die der Alltag beide «Preis» nennt, im Lehrmittel aber nie:

| Grösse | Bedeutung | Einheit |
|---|---|---|
| **Preis** \(p\) | Kosten **pro Einheit** | \(\text{CHF/kg}\), \(\text{CHF/km}\), \(\text{CHF/L}\) |
| **Kosten** \(K\) | der **Gesamtbetrag** | \(\text{CHF}\) |

\[ K = m \cdot p \]

**«Preis» erscheint nie mit der Einheit CHF.** Wo ein Franken-Betrag steht, heisst
die Grösse *Kosten* — in Fliesstext, Achsenbeschriftungen, Live-Boxen und
Lösungswegen gleichermassen. Falsch also: «doppelte Menge → doppelter Preis»,
Achsenlabel `Preis [CHF]`, «Preis der Zielmenge: 12.50 CHF».

*Nicht betroffen:* die übertragene Redewendung («Was ist der Preis? Der längere
Weg») — dort steht kein Geldbetrag dahinter.
Referenz: `themen/p0-0-vorwissen-kompakt.html`, Animation 1.

### 2.7 Einsetzen mit Einheiten (verbindlich, Stichwort «Stilcheck»)

In **jeder** Rechnung — Lösungswege, Mini-Check-Antworten und **Live-Anzeigen
(`.fl-eq`)** — werden die Werte **mit ihrer Einheit** eingesetzt, nie als nackte
Zahlen:

- `Q = m · c · ΔT = 1.0 kg · 4182 J/(kg·K) · 50 K = 209 100 J` ✓
- `Q = m · c · ΔT = 1.0 · 4182 · 50 = 209 100 J` ✗

Der Grund ist nicht Kosmetik: Das Mitführen der Einheiten ist die einzige
Selbstkontrolle, die Lernende beim Einsetzen haben. Wer nur Zahlen einsetzt,
merkt einen Einheitenfehler (Gramm statt Kilogramm, °C statt K) erst nie.

**Bezugsgrössen konkret machen:** Wo eine Animation mit dimensionslosen «Teilen»
oder Prozenten arbeiten würde, wird stattdessen eine konkrete Bezugsgrösse mit
Einheit gewählt (z.B. Wärmepumpe: \(1\;\text{kWh}\) Strom statt «1 Teil»).
Referenz: `themen/p5-2-waerme.html`, Animationen 1, 2, 3 und 6.

**Ausnahme:** Zwischenschritte, deren Einheit selbst unanschaulich wäre, dürfen
übersprungen werden — dann trägt das Ergebnis die Einheit. Nie weggelassen wird
sie beim **Einsetzen** und beim **Resultat**.

**Sonderfall Skalen- und Einheitenumrechnung.** Wo die Einheit nicht mitgeführt
werden *kann*, weil die Gleichung Zahlenwerte zweier Skalen verknüpft, wird die
Einheit in eckigen Klammern an die Grösse geschrieben statt an die Zahl:

- `T [K] = ϑ [°C] + 273.15` → `T [K] = 20.00 + 273.15 = 293.15` ✓
- `T = ϑ + 273.15 = 20.00 + 273.15 = 293.15 K` ✗ (Zahlen ohne Skala)
- `T = 20.00 °C + 273.15 K` ✗ (addiert zwei verschiedene Einheiten)

Damit sieht die Leserin an jeder Zahl, in welcher Skala sie steht, ohne dass die
Gleichung dimensionell falsch wird. Gleiches Muster bei km/h ↔ m/s.
Referenzen: `themen/p5-1-temperatur.html` a3, `themen/p0-3-vorwissen-technik.html` a2.

Echte **Differenzen** sind davon nicht betroffen — dort wird ganz normal mit
Einheit eingesetzt: `Δϑ = ϑ₂ − ϑ₁ = 95 °C − 12 °C = 83 °C` (p5-1 a4).

### 2.8 Brüche als Brüche (verbindlich, Stichwort «Stilcheck»)

Ein Bruch in einer Formelzeile wird als **echte LaTeX-Bruchdarstellung**
gesetzt, nicht als Schrägstrich-Zeile:

- \[ \vartheta_\text{m} = \frac{m_1 c_1\,\vartheta_1 + m_2 c_2\,\vartheta_2}{m_1 c_1 + m_2 c_2} \] ✓
- `ϑm = (m₁c₁ϑ₁ + m₂c₂ϑ₂) / (m₁c₁ + m₂c₂)` ✗

**Auch die Zahlengleichung wird in LaTeX gesetzt** — nicht nur die symbolische
Formel. Dafür muss MathJax bei jeder Reglerbewegung neu rendern; damit das nicht
ruckelt und sich zwei Läufe nicht überholen, gilt das Muster aus
`themen/p5-2-waerme.html` (Animation 2):

- alle Formelzeilen liegen in **einem** Container-`<div>`;
- Schreiben und Rendern werden per `requestAnimationFrame` auf einen Frame
  gedrosselt und in einer **Promise-Kette serialisiert**;
- vor dem Neuschreiben `MathJax.typesetClear([box])`, danach
  `MathJax.typesetPromise([box])`;
- die Kette startet auf `MathJax.startup.promise`, damit der erste Lauf nicht vor
  dem Laden von MathJax feuert;
- ein `dataset.stand`-Vergleich verhindert Neu-Rendern, wenn sich nichts ändert.

**Escaping-Falle:** In JS-Strings muss der LaTeX-Backslash **doppelt** stehen.
`'\;\text{kg}'` ✗ liefert `;\text{kg}` — JavaScript verschluckt den einzelnen
Backslash. Richtig ist `'\\;\\text{kg}'`. Nach jeder Änderung an solchen
Strings die erzeugte Zeichenkette einmal in Node ausgeben lassen.

**Zu breite Formeln:** Displayformeln brechen nicht um. `.formel-live` hat darum
`overflow-x:auto` — auf schmalen Viewports scrollt die Box, statt die Formel
rechts abzuschneiden. Herunterskalieren wäre die schlechtere Wahl (unlesbar).

**Fallunterscheidung sichtbar machen:** Vereinfacht sich die Formel in einem
Sonderfall (z.B. \(c_1 = c_2\) → \(c\) kürzt sich), bekommt der Sonderfall
eine eigene Formelzeile, die nur in diesem Fall eingeblendet wird.
Referenz: `themen/p5-2-waerme.html`, Animation 2.

## 3. Achsenskalierung

Physik unterscheidet sich grundlegend von Mathematik: **Achsen tragen IMMER Einheiten**. Es gibt keine reinen 1:1-Achsen wie im Mathe-Repo.

### 3.1 Konvention: aufgabenbezogen mit Einheit

Alle Diagramme zeigen physikalische Grössen mit ihren Einheiten. Die Skalierung ist **immer aufgabenbezogen** (z.B. `t` in Sekunden geht bis 10 s, `s` in Metern geht bis 200 m — unterschiedliche Pixelmasse).

**Code-Konvention:** `initCanvas(id, H, false)` setzen (`square=false`), dann nach `drawGrid` die Achsen-Labels mit `drawAxesUnits` überschreiben:
```js
const {ctx, W, H} = initCanvas('a1-cv-st', 280, false);
const {cx, cy} = drawGrid(ctx, W, H, -1, 11, -5, 50);
drawAxesUnits(ctx, W, H, cx, cy, 't [s]', 's [m]');
```

### 3.2 Bahnkurven (x-y-Raum)

Bei Bewegungen im physikalischen Raum (Wurfparabel, Kreisbahn) sind beide Achsen Längen mit gleicher Einheit (m). **Ausnahme**: hier 1:1-Skalierung anstreben, damit die Bahnkurve geometrisch korrekt aussieht. Im Code: Skalierungsfaktor pro Pixel für beide Achsen gleich setzen.

### 3.3 Mehrere Diagramme nebeneinander

Wenn drei Diagramme `a(t)`, `v(t)`, `s(t)` gleichzeitig dargestellt werden (siehe Animation 2 in p4-1), haben sie identische `t`-Achse (also gleicher Pixelbereich auf der x-Achse), aber unterschiedliche y-Skalen.

### 3.4 Lesbare Achsenbeschriftungen — Automatik

Seit `physiklib.js v2` wählt `drawGrid` automatisch sinnvolle Tick-Schrittweiten aus der Folge `{1, 2, 5}·10ⁿ` (so dass ca. 65 px auf der x-Achse und 40 px auf der y-Achse zwischen Labels bleiben). Du musst **keine** manuellen Tick-Schritte angeben — egal ob der Wertebereich `0..10` oder `0..1334` ist.

**Was die Automatik leistet** (du musst dich darum nicht kümmern):
- Tick-Schrittweite passt sich dem Bereich an: `[0, 10]` → 1er-Schritte, `[0, 100]` → 20er-Schritte, `[0, 1334]` → 200er-Schritte
- Tick-Werte werden mit minimaler Anzahl Nachkommastellen formatiert (`fmtTick`)
- Y-Tick-Labels wechseln auf die rechte Seite der Y-Achse, wenn links kein Platz ist (z.B. wenn `xMin ≈ -0.5` knapp neben dem linken Canvas-Rand liegt)
- X-Tick-Labels wandern oberhalb der X-Achse, wenn diese am unteren Canvas-Rand sitzt (typisch bei `yMin = -pMax*0.05`)
- `drawAxesUnits` zeichnet seinen Overlay-Hintergrund passend zur tatsächlichen Label-Breite — keine Tick-Werte mehr durch zu grosse Boxen überdeckt

**Best Practice — Wertebereich grosszügig wählen:**
```js
// gut: ein bisschen Reserve links/unten, damit 0 nicht direkt am Canvas-Rand klebt
const grid = drawGrid(ctx, W, H, -0.5, hMax + 0.5, -pMax*0.05, pMax*1.05);
drawAxesUnits(ctx, W, H, grid.cx, grid.cy, 'h [m]', 'p_S [kPa]');
```

**Anti-Pattern — vermeiden:**
- ❌ Wertebereich exakt von 0 bis Max — Achse klebt am Canvas-Rand
- ❌ Wertebereich der nur ein, zwei Hauptticks enthält (z.B. `0..0.05` wenn nicht in passende Einheit konvertiert) — lieber in `mbar`, `kPa`, `kN` umrechnen vor dem Plotten
- ❌ Sehr breite Wertebereiche (z.B. mehrere Grössenordnungen): die nice-tick-Automatik wählt einen sinnvollen Schritt, aber bei Bedarf logarithmische Achse erwägen (separater Helper nötig — derzeit nicht in `physiklib.js`)

**Eigene Tick-Schritte erzwingen** (Sonderfall, nicht empfohlen):
- Möglich, indem nach `drawGrid` direkt mit `ctx.fillText` über die Labels gezeichnet wird. Nutze diesen Workaround nur, wenn die Automatik wirklich nicht passt — meistens deutet das auf einen schlecht gewählten Wertebereich hin.

### 3.5 Inhaltliche Overlays (Wurfweiten-Marker, Maxima)

Wenn an einer Stelle im Plot ein Hilfsmarker mit Text sitzt (z.B. `W = 40.8 m` an der Wurfweite), kann er mit den Tick-Labels darunter zusammenfallen. Lösungen:
- Hilfsmarker `cy(0) - 18` setzen (oberhalb der Achse statt darunter)
- Oder den Wertebereich so wählen, dass `0` nicht am Canvas-Boden klebt — dann steht unter der x-Achse Platz für beides
- Oder den Marker als kleineres Label und mit kontrastierender Farbe absetzen

### 3.6 Label-Robustheit auf Canvas (verbindlich für NEUE Labels)

Frei positionierte Canvas-Labels (Marker-Beschriftungen, Hilfstexte) erhalten zwei Schutzmechanismen:

- **Weisser Halo:** vor dem `fillText` ein weisses `fillRect` hinter dem Text (Breite via `measureText`), damit das Label Tick-Beschriftungen und Gitterlinien überdeckt statt mit ihnen zu kollidieren.
- **Rand-Klammerung:** liegt der Label-Anker nahe am Canvas-Rand, kippt das Label auf die Innenseite seiner Bezugslinie (Wechsel von `textAlign` `left` ↔ `right`), damit es nicht abgeschnitten wird.

Referenz-Implementierung: Funktion `a0Lbl` in `themen/p4-1-kinematik.html` (Einstiegs-Animation, Marker t₁/t₂ bei 0 und 60 min voll lesbar). **Bestehende, visuell abgenommene Animationen werden NICHT nachgerüstet** — die Regel gilt nur für neue Labels.

### 3.7 Einheiten-Zweitzeile an Achsen

Technik für Achsen mit zwei didaktisch tragenden Einheiten (z.B. Stunden und Minuten): Die Achse läuft in der Haupteinheit über `drawGrid` (Auto-Ticks). Darunter wird eine eigene zweite Beschriftungszeile in der Nebeneinheit gezeichnet — kleinere graue Schrift, Tick-Positionen aus `gr.stepX`, Caption der Nebeneinheit rechts. Den y-Wertebereich nach unten erweitern, damit die Zusatzzeile Platz hat (z.B. `yMin = -25`).

Hinweis: `drawGrid` wählt Schritte adaptiv — auf sehr schmalen Canvases vergröbert sich der Schritt (z.B. 0.1 h → 0.2 h); das ist akzeptiert, `physiklib.js` wird dafür nicht verbogen.

Referenz: Minuten-Zeile in `drawA0` in `themen/p4-1-kinematik.html`.

---

## 4. Master-Schema einer Themenseite (13 Punkte)

Jede Themenseite folgt diesem Aufbau. Punkte mit (*) können je nach Themenumfang zusammengezogen oder gestrichen werden.

| # | Abschnitt | Inhalt |
|---|---|---|
| 1 | **Titel + RLP** | `.page-titel` mit Lerngebiet, `.rlp-kompetenzen` mit den RLP-Stichpunkten 1:1 |
| 2 | **Einstieg** | Konkretes Alltagsphänomen, einleitende Frage, evtl. `.block-experiment` |
| 3 | **Grundbegriffe** | `.block-def` für jeden zentralen Begriff (Schwerpunkt, Bahnkurve, Geschwindigkeit, Beschleunigung …) |
| 4 | **Animation 1** | Hauptphänomen interaktiv (z.B. gleichförmige Bewegung) — `.widget` mit `.cv-wrap`; Titelzeile mit Hinweisen «Worauf achten?» / «Erkenntnis» (§5.6) |
| 5 | **Theorie + Animation 2** | Herleitung der Bewegungsgleichungen mit `.block-beweis`, dann gekoppelte Diagramme |
| 6-9 | **Spezialfälle als Animationen** | Pro Spezialfall ein `.widget` (freier Fall, Wurf, Kreisbewegung, Vektoraddition …). Ziel: 5-10 Animationen total |
| 10 | **Aufgaben A1-A6** | Stufenweise nach Schwierigkeit: A1 ablesen → A2 rechnen einfach → A3 mehrteilig → A4-A6 Anwendung. **Alle sechs** Aufgaben nutzen identisch das `.block-aufg`-Muster aus §5.5 (siehe dort) mit `toggleL('lX')` — keine Sonderbehandlung einzelner Aufgaben |
| 11 | **Zusammenfassung** | `.ftb-tabelle` mit allen Formeln + `.merksatz` |
| 12 | **Zusatzmaterial** | `.dl-grid` mit den 5 Druckseiten + Anki-Deck |
| 13 | **Externe Ressourcen** | **Dreispaltig**: 🎬 Videos · 🧪 Simulationen · 📝 Aufgaben |

### 4.1 Sub-Splits

Bei umfangreichen Themen kann das `.widget`-Schema mit `id`-Suffix `a`/`b`/`c` strukturiert werden. Beispiel für ein langes Mechanik-Thema: 5 Animationen zur Translation + 2 zur Rotation. Trotzdem bleibt es **eine** Themenseite — kein zweites HTML-File.

### 4.2 Mindest- und Höchstinhalt

- **Mindestens** 5 Canvas-Animationen pro Themenseite
- **Höchstens** 10 Canvas-Animationen (sonst wird die Seite unleserlich; bei Bedarf Themenseite splitten)
- **Genau** 6 Aufgaben (A1-A6), nicht mehr — die Aufgabenserie unter „Zusatzmaterial" deckt mehr ab
- **Genau** 5 Druckseiten + 1 Anki-Deck unter „Zusatzmaterial"

---

## 5. Visuelle Konventionen

### 5.1 Bereichsfarbe Bernstein

`--bernstein: #8a4a0e` / `--bernstein-hell: #fbecd2` / `--bernstein-rand: #c98028` — das ist die **Physik-Bereichsfarbe**. Sie ersetzt das Blau aus Mathe in: Logo-Pill, Header-Unterstrich, Nav-Hover, Toc-Aktiv, Aufgaben-Slider-Akzent, RLP-Box „ohm"-Chip, Bereich-Kopf auf der Index-Seite, Themenkarten-Highlight, Sticky-ToC-Akzent, Live-Box (Werteanzeige).

Wichtig: Die **didaktischen Farben** (blau=Definition, grün=Beispiel, orange=Aufgabe, rot=Fehler, violett=Beweis/Herleitung) bleiben **unverändert** wie in Mathe. Sie haben fachübergreifend dieselbe Bedeutung.

### 5.2 Animations-Farbcodes

Innerhalb einer Animation folgt die Farbgebung einer Konvention:

| Was | Farbe | Hex |
|---|---|---|
| Weg / Position `s` | Bernstein | `#8a4a0e` |
| Geschwindigkeit `v` | Grün | `#1f6b3a` |
| Beschleunigung `a`, Komponenten-Vektoren | Violett | `#5b2d8e` |
| Zentripetal / Resultierende | Rot | `#9b1c1c` |
| Resultierender Hauptvektor | Blau | `#1a4f8a` |
| Mittelpunkt / Ursprung | Tinte (Schwarz) | `#1c1a17` |

Diese sind in der Mathe-Welt teilweise anders belegt; in Physik ist eine eindeutige semantische Zuordnung wichtig (z.B. „grüner Pfeil = Geschwindigkeit" auf jeder Themenseite).

### 5.3 Live-Box

Für die laufende Wertanzeige neben jeder grossen Animation gilt die Klasse `.live-box` (Bernstein-Hintergrund). Mehrere `.lb-item` darin mit `.lb-lab` (Label, klein, oben) und `.lb-val` (Wert, gross, unten). Beispiel:

```html
<div class="live-box">
  <div class="lb-item">
    <span class="lb-lab">v(t)</span>
    <span class="lb-val">10.0 m/s</span>
  </div>
  <div class="lb-item">
    <span class="lb-lab">s(t)</span>
    <span class="lb-val">25.0 m</span>
  </div>
</div>
```

**Gruppierung:** Logisch zusammengehörende Wertegruppen (z.B. Momentan- vs. Intervallwerte) werden optisch getrennt, indem das letzte `.lb-item` der ersten Gruppe `style="margin-right:30px"` erhält. Referenz: Phase-Item der a0-live-box in `themen/p4-1-kinematik.html`.

**Spaltenabstand (verbindlich, Stichwort «Stilcheck»):** Die Werte müssen als
*getrennte Grössen* lesbar bleiben. `style.css` staffelt darum den `column-gap`
nach Anzahl Werte: 70 px (bis 3), 40 px (ab 4), 24 px (ab 6). Der Abstand darf
**nie** auf den Zeilenabstand zusammenfallen — zwei Werte, die gleich weit
auseinanderstehen wie zwei Zeilen, lesen sich als eine Tabelle ohne Struktur.
Reicht die Breite nicht, bricht `flex-wrap` um; ein Umbruch ist besser als eine
gedrängte Zeile. **Wer einer bestehenden Live-Box einen Wert hinzufügt, prüft
danach die Darstellung** — der Sprung über eine Stufengrenze (3→4, 5→6) ändert
das Bild der ganzen Box, nicht nur des neuen Werts.

### 5.4 HiDPI-Rendering

Pflicht für alle Canvas: nutze `initCanvas()` aus `physiklib.js`. Diese Funktion skaliert das Canvas auf `devicePixelRatio` — sonst sieht es auf Retina-Displays verwaschen aus.

### 5.5 Aufgaben-Struktur (verbindlich, identisch zur Mathe-Plattform)

**Alle** Aufgaben einer Themenseite (A1 bis A6) verwenden dieselbe Struktur. Es gibt **keine** Sonderbehandlung für „einfache" vs. „Anwendungs"-Aufgaben. Sämtliche Klassen kommen aus `style.css`; **nichts** davon lokal in der Themenseite redefinieren. Insbesondere ist das frühere `aw`/`aw-head`/`aw-nr`/`aw-titel`-Wrapper-System **abgeschafft** und darf nicht mehr verwendet werden.

**Aufgaben-Karte** (jede Aufgabe ist eine `block-aufg`-Karte mit Pillen-Titel):

```html
<div class="block block-aufg">
  <div class="block-titel">🟠 <span class="aufg-nr-tag">A1</span><span class="aufg-titel-text">Werte ablesen</span></div>
  <p>Einleitender Aufgabentext …</p>
  <ol class="aufg-liste">
    <li>Erste Teilaufgabe …</li>
    <li>Zweite Teilaufgabe …</li>
  </ol>
  <button class="loesung-toggle" onclick="toggleL('l1')">▶ Lösung</button>
  <div class="loesung-body" id="l1">
    <div class="block block-bsp" style="margin:6px 0 0">
      <div class="block-titel">🟢 Lösung</div>
      <ol class="aufg-liste">
        <li>Lösung zur ersten Teilaufgabe, Inline-Mathe \(p = \rho g h\) … \[ \text{Display-Formeln dürfen im } li \text{ stehen} \]</li>
        <li>Lösung zur zweiten Teilaufgabe …</li>
      </ol>
    </div>
  </div>
</div>
```

Verbindliche Regeln:

- **Titel:** `🟠 <span class="aufg-nr-tag">A1</span><span class="aufg-titel-text">Titel</span></span>`. Die `aufg-nr-tag`-Pille ist orange, monospace. **Verboten** ist das alte Spiegelstrich-Muster `🟠 A1 — Titel`.
- **Teilaufgaben** (sowohl in der Aufgabenstellung als auch in der Lösung) stehen als `<ol class="aufg-liste">` mit `<li>`. Die `1.`, `2.`, `3.`-Pillen werden per CSS-Counter erzeugt. **Verboten** sind das alte `teil-aufg`/`ta-lb`-Muster und manuell gesetzte `<strong>a)</strong>`-Marker in Lösungen.
- **Display-Formeln** `\[…\]` dürfen innerhalb eines `<li>` stehen — die Listennummerierung bleibt korrekt.
- **Lösungs-Wrapper:** immer `block block-bsp` mit `style="margin:6px 0 0"` und Titel `🟢 Lösung`.
- Hat eine Aufgabe nur einen einzigen Lösungsweg ohne Teile, entfällt die `aufg-liste`; dann steht die Lösung als Fliesstext mit `<p>` und Display-Formeln.

### 5.6 Animations-Hinweise («Worauf achten?» / «Erkenntnis»)

Jede Animation trägt in der **Titelzeile** zwei dezente Rollover-Hinweise: nach dem Titel «💡 Worauf achten?», ganz rechts «✓ Erkenntnis». Sie ersetzen die frühere Bedienungszeile unter dem Titel (deren Inhalt steht jetzt in «Worauf achten?»).

- **Struktur:** Titel und beide Hinweise stehen gemeinsam in `<div class="widget-titelzeile">` (statt `<h3>` allein im `.widget-header`). Markup pro Hinweis:
  ```html
  <div class="anim-hinweis links">   <!-- bzw. "rechts" für Erkenntnis -->
    <span class="ah-trigger" tabindex="0" role="button" aria-haspopup="true" aria-label="…">💡 Worauf achten?</span>
    <div class="ah-pop" role="tooltip">
      <span class="ah-titel">Worauf achten?</span>
      <div class="ah-text"><ul><li>…</li></ul></div>
      <button type="button" class="ah-speak" data-vorlesen="Klartext-Fassung" aria-pressed="false">🔊 vorlesen</button>
    </div>
  </div>
  ```
- **Inhalt — animationsspezifisch, mehrere Aspekte (je 4–5 Punkte):**
  - «Worauf achten?» = was man ausprobieren/beobachten soll (Slider-Verhalten, Grenzfälle, was in der Live-Anzeige zu verfolgen ist).
  - «Erkenntnis» = die physikalischen Schlüsse inkl. der zugehörigen Formeln.
- **Notation:** sichtbarer Text in **Projekt-Notation** (MathJax `\(…\)`, Dezimalpunkt, korrekte Symbole/Vektoren wie §2). Kein rohes `<` in der Mathe (sonst HTML-Konflikt) — «negativ» schreiben oder `\lt` verwenden.
- **Vorlesen:** Die `\(…\)`-Formeln würden als roher LaTeX-Code vorgelesen. Darum trägt jede `.ah-speak`-Schaltfläche eine **Klartext-Fassung** im Attribut `data-vorlesen` (Formeln in Worten, z.B. «s von t gleich s null plus v mal t»).
- **Zentral, nicht pro Seite duplizieren:** Gestaltung in `style.css` (Abschnitt «Animations-Hinweise»), Logik in `anim-hinweise.js` (auf jeder Themenseite nach `physiklib.js` eingebunden). Die Logik regelt Hover/Fokus-Anzeige, **Klick fixiert** das Rollover (damit der Vorleseknopf erreichbar ist, auch auf Touch), Aussenklick/Escape schliesst, Sprachausgabe läuft weiter.

### 5.7 Mini-Checks (Selbsttest pro Abschnitt)

Am Ende **jedes Inhaltsabschnitts** (zwischen den `<h2>`-Abschnitten, eingefügt direkt vor dem nächsten `<h2 id="…">`) steht ein einklappbarer Mini-Check. Er prüft genau den vorangehenden Abschnitt.

- **Struktur:** ein natives `<details class="minicheck">` (standardmässig **zu** → wenig visuelles Gewicht) mit `<summary class="mc-kopf">✏️ Mini-Check</summary>` und genau **vier** `.mc-item` in fester Reihenfolge:
  ```html
  <details class="minicheck">
    <summary class="mc-kopf">✏️ Mini-Check</summary>
    <div class="mc-item"><span class="mc-typ">Multiple Choice</span><p class="mc-frage">…</p>
      <ul class="mc-optionen"><li data-opt="A">…</li>…</ul>
      <details class="mc-loesung"><summary>Lösung anzeigen</summary><div class="mc-antwort">…</div></details></div>
    <div class="mc-item"><span class="mc-typ">Lückentext</span> … <span class="mc-luecke"></span> … </div>
    <div class="mc-item"><span class="mc-typ">Kurze Rechnung</span> … </div>
    <div class="mc-item"><span class="mc-typ">Transfer</span> …
      <details class="mc-loesung"><summary>Lösungsweg anzeigen</summary>…</details></div>
  </details>
  ```
- **Teilaufgaben:** Multiple Choice (3 Optionen), Lückentext (mit `<span class="mc-luecke">`-Ausfüllstrich), kurze Rechnung und **Transfer** (gleichwertige vierte Teilaufgabe — **kein** gesonderter «für Leistungsstarke»-Block). Jede Teilaufgabe hat ihre eigene Lösungseinblendung via `<details class="mc-loesung">`.
- **Notation & Sprache:** sichtbarer Text in Projekt-Notation (`\(…\)`, Dezimalpunkt, Symbole wie §2), Schweizer Hochdeutsch, kein ß. Alle Zahlenwerte vor dem Einbau in Python verifizieren.
- **Akkordeon:** Es ist immer höchstens **ein** Mini-Check offen — beim Öffnen des nächsten schliesst der vorher offene. Diese Logik liegt zentral in `minicheck.js` (auf jeder Themenseite nach `anim-hinweise.js` eingebunden); die inneren `.mc-loesung` bleiben davon unberührt. Gestaltung zentral in `style.css` (Abschnitt «Mini-Checks»).
- **Aufbau:** mit `scripts/minicheck_lib.py` (`mc`, `lueck`, `rech`, `block`, `apply_page`) — fügt jeden Block vor dem Ziel-`<h2>` ein, bindet `minicheck.js` ein und besitzt einen Idempotenz-Guard.

### 5.8 Direkt-Manipulation im Canvas (optionales Interaktionsmuster)

Punkt oder Marker direkt im Canvas ziehen statt über Schieberegler — **KEIN Pflicht-Rollout**, sondern eine Option für Animationen, bei denen das Ziehen den Lerngegenstand unmittelbarer macht. Bausteine:

- Pointer-Events `pointerdown/move/up/cancel` plus `setPointerCapture` (ein Code-Pfad für Maus und Touch).
- **Hit-Test auf den nächstgelegenen Griff** mit Schwellen: Punkt ~18 px radial, Linien-Griffe ~12 px horizontal; Klick neben den Griffen lässt den Punkt dorthin springen.
- **Werte-Raster** beim Ziehen (z.B. 0.5), damit Live-Werte reproduzierbar bleiben.
- **Hover-Cursor** als Affordanz: `grab` über dem Punkt, `ew-resize` über vertikalen Linien-Griffen.
- `style="touch-action:pan-y"` am Canvas — horizontales Ziehen geht ans Canvas, vertikales Scrollen auf Mobile bleibt frei.

Referenz-Implementierung: `a0Hit` (Hit-Test), `a0EvtT` (Event-Koordinaten), `a0Apply` (Drag-Anwendung) in `themen/p4-1-kinematik.html` (Einstiegs-Animation, Phase 5.29).

---

## 6. Code-Konventionen

### 6.1 HTML-Skelett

Strikt einhalten, sonst bricht das Layout. Jede Themenseite hat folgende Wurzelstruktur:

```html
<body>
<div id="nav-root"></div>     <!-- Wird von nav.js befüllt -->
<div class="page-wrap">
  <main class="content">
    <!-- ... gesamter Themen-Inhalt ... -->
  </main>
  <aside class="toc-wrap">
    <div id="toc"></div>       <!-- Wird von buildToC befüllt -->
  </aside>
</div>
<footer class="site-footer">...</footer>
<script src="../nav.js"></script>
<script src="../physiklib.js"></script>
<script>
  buildNav({ id, kapitelNr, kapitelTitel, prev, next });
  // ... Animation-Code ...
</script>
</body>
```

### 6.2 buildNav-Signatur

```js
buildNav({
  id: 'p4-1',
  kapitelNr: '4.1',
  kapitelTitel: 'Kinematik des Schwerpunkts',
  prev: null,  // oder { nr, titel, url }
  next: { nr: '4.2', titel: 'Dynamik', url: 'p4-2-dynamik.html' }
});
```

`prev` und `next` sind URLs relativ zum `themen/`-Ordner. Auf der Index-Seite (homepage:true) entfallen `kapitelNr` und `kapitelTitel`.

> **Lokaler `<style>`-Block:** bleibt minimal. Alle gemeinsamen Komponenten — Block-Karten, Aufgaben (`aufg-*`), Animations-Widgets (`widget`, `sl-row`, `sl-vert`, `live-box`, `cv-wrap`, `typ-btn`, `play-btn`, `formel-live`, Spalten-Layouts) — sind zentral in `style.css`. Lokal nur Klassen, die ausschliesslich auf dieser einen Seite vorkommen (z.B. ein Sonder-Grid wie `einstieg-layout` für eine bestimmte Animation).

### 6.3 IDs für Animationen

Konvention: `a<N>-<element>` — z.B. `a1-v`, `a1-cv-st`, `a3-btn`. Das macht das Code-Lesen einfach und vermeidet Kollisionen bei mehreren Animationen pro Seite.

### 6.4 Resize-Handler

Animationen sind responsive — bei Fenstergrössen-Änderung müssen sie neu gezeichnet werden:

```js
function renderAll() {
  drawA1(); drawA2(); /* ... */
}
document.addEventListener('DOMContentLoaded', renderAll);
window.addEventListener('resize', renderAll);
```

Bei RAF-Animationen (z.B. Animation 3 Freier Fall) zusätzlich darauf achten, dass `requestAnimationFrame`-Loops bei Pause sauber abbrechen, sonst werden mehrere Loops gleichzeitig gestartet.

---

## 7. Inhaltliche Quellen-Politik

### 7.1 Was wir tun

- **Selbst formulieren**: alle Texte, Definitionen, Erklärungen, Aufgabentexte. Eigene Worte, eigener didaktischer Aufbau.
- **Skript als Steinbruch nutzen**: vor jeder Themenseite das entsprechende Skript-Kapitel überfliegen — als Vollständigkeits-Check (welche Begriffe und Beispiele sind in der BM üblich?) und als Inspiration für Aufgabenszenarien.
- **Aufgabenzahlen anpassen**: wenn das Skript ein Beispiel mit `v_0 = 12 m/s` rechnet, wählen wir `v_0 = 13 m/s` — gleiche Struktur, andere Zahlen, neue Aufgabe.

### 7.2 Was wir nicht tun

- Keine wörtliche Übernahme von Skript-Passagen
- Keine 1:1-Kopie von Aufgabentexten (auch nicht aus dem Aufgabenanhang)
- Keine Übernahme von Skript-Grafiken — alle Visualisierungen sind Canvas-Animationen, selbst gebaut

### 7.3 Externe Ressourcen — Anbieter-Reihenfolge

Für Sektion 13 in jeder Themenseite. Reihenfolge ist verbindlich (siehe `HOWTO-externe-ressourcen.md`):

**🎬 Videos** (jeweils max. 4 pro Themenseite, alle per `web_fetch` verifiziert):
1. musstewissen Physik
2. Lehrerschmidt
3. Doc Schuster
4. Alexander Fufaev
5. Phil's Physics
6. MrWissen2go Physik

**🧪 Simulationen** (max. 4):
1. PhET (University of Colorado Boulder) — deutsch
2. Walter Fendt (HTML5-Sammlung)
3. LEIFIphysik Simulationen
4. oPhysics (englisch, hochwertig)

**📝 Aufgabensammlungen** (max. 4):
1. LEIFIphysik (Aufgaben pro Lerngebiet)
2. serlo.org Physik
3. SwissEduc (PrismaPhysik, falls thematisch passend)
4. abi-physik.de (Abi-fokussiert, mit Lösungen — nur einsetzen, wenn Slots 1-3 nicht reichen)

---

## 8. Was sich gegenüber TALS-Mathematik geändert hat

| Was | Mathe | Physik |
|---|---|---|
| Bereichsfarbe | Blau (`#1a4f8a`) | Bernstein (`#8a4a0e`) |
| Bereiche | Grundlagenfach + Schwerpunktfach | Nur ein Bereich (RLP-Pflicht) |
| Themen-Ordner | `grundlagen/`, `schwerpunkt/` | `themen/` |
| Library-Datei | `mathlib.js` | `physiklib.js` |
| Achsenskalierung | 1:1 für reine Mathe, aufgabenbezogen für Anwendungen | IMMER aufgabenbezogen mit Einheit (ausser x-y-Raum: 1:1) |
| Sektion 10 | Zweispaltig: Videos · Aufgaben | **Dreispaltig**: Videos · Simulationen · Aufgaben |
| Zusätzliche Klasse | — | `.block-experiment` (für Phänomene/Versuche) |
| Aufgaben-Reihenfolge | A1 ablesen, A2 konstruieren, A3 rechnen, A4-A6 Anwendung | A1 ablesen, A2 rechnen, A3 mehrteilig, A4-A6 Anwendung |
| Aufgaben-Markup | `block-aufg` + `aufg-nr-tag` + `aufg-liste` (zentral) | **identisch** (seit Phase 2.2, siehe §5.5) |
| Skript-Quelle | FTB-Buch | BM-Physik-Skript (im Project-Knowledge) — nur als Steinbruch |

---

## 9. Qualitäts-Checkliste vor Veröffentlichung

Bevor eine Themenseite live geht, prüfe:

**Inhalt**
- [ ] Alle RLP-Kompetenzen des Themas abgedeckt
- [ ] „mit/ohne Hilfsmittel"-Hinweise gemäss RLP gesetzt
- [ ] Mindestens ein Alltagsphänomen im Einstieg
- [ ] 5–10 Canvas-Animationen, Spezialfälle visualisiert
- [ ] Genau 6 Aufgaben (A1–A6) mit zunehmender Selbstständigkeit
- [ ] Zusammenfassung als kompakte `.ftb-tabelle` + `.merksatz`

**Notation (siehe §2)**
- [ ] Multiplikationspunkt in Live-Anzeigen (`2·x`, nicht `2x`)
- [ ] Dezimal**punkt**, nicht Komma
- [ ] Kein ß (Schweizer Konvention: `ss`)
- [ ] Einheiten mit schmalem Abstand vor der Einheit, LaTeX für alle Formeln
- [ ] Konstanten konsistent (`g = 9.81 m/s²`, `ρ_W = 1000 kg/m³`, `p_0 = 1013 hPa`)
- [ ] **MathJax-Delimiter im Head-Config doppelt maskiert**: im JS-String `'\\('`/`'\\)'`/`'\\['`/`'\\]'` (nicht `'\('` — das wertet JS zu `'('` aus und MathJax behandelt dann normale Klammern als Mathe-Begrenzer, wodurch Formeln nur teilweise/falsch rendern). Schnelltest: `grep -F "inlineMath:[['\(','\)']]" themen/*.html` darf **nichts** finden.

**Grafik (siehe §3)**
- [ ] Achsenbeschriftung aufgabenbezogen mit Einheit (`h [m]`), ausser x-y-Raum (1:1)
- [ ] Canvas läuft bei keinem Schieber-Wert über (HiDPI via `initCanvas()`)
- [ ] Animations-Farbcodes gemäss §5.2 (grün = Geschwindigkeit, violett = Beschleunigung …)

**Aufgaben-Markup (siehe §5.5) — verbindlich**
- [ ] **Alle** Aufgaben in `block-aufg` mit Pillen-Titel `🟠 <span class="aufg-nr-tag">A1</span><span class="aufg-titel-text">…</span>`
- [ ] **Kein** Spiegelstrich-Titel `🟠 A1 — …`, **kein** `aw`/`aw-head`/`aw-nr`-Wrapper
- [ ] Teilaufgaben (Stellung *und* Lösung) als `<ol class="aufg-liste">`, **kein** `teil-aufg`/`ta-lb`, **kein** `<strong>a)</strong>`
- [ ] Lösungs-Wrapper `block block-bsp` mit `style="margin:6px 0 0"`, Titel `🟢 Lösung`
- [ ] Lösungen zugeklappt by default, `toggleL('lX')` aus `physiklib.js`

**Struktur & Konventionen**
- [ ] Zusatzmaterial-Sektion vor externen Ressourcen, alle 5 Druckseiten + Anki-Deck verlinkt
- [ ] Druckseiten öffnen in neuem Tab (`target="_blank" rel="noopener"`)
- [ ] Externe Ressourcen **dreispaltig** (🎬 Videos · 🧪 Simulationen · 📝 Aufgaben), alle per `web_fetch` verifiziert
- [ ] Block-Modifier nur aus dem Inventar von §5.1 plus `block-experiment` — **keine Eigenkreationen**
- [ ] **Keine lokale Redefinition** zentraler Klassen (`widget`, `sl-row`, `live-box`, `aufg-*`, …) im `<style>` der Themenseite — nur genuin seitenspezifische Layouts dürfen lokal stehen

**HTML-Skelett (siehe §6.1)**
- [ ] Body-Struktur: `body > div#nav-root > div.page-wrap > main.content` + Geschwister `aside.toc-wrap`
- [ ] `<main class="content">` — nicht `inhalt` o.Ä.
- [ ] Anker-IDs direkt am `<h2 id="…">` — keine `<section>`-Wrapper
- [ ] `<script src="../nav.js">` direkt vor dem `buildNav()`-Inline-Script
- [ ] `../style.css` und `../physiklib.js` verlinkt
- [ ] Pre-Flight-Bash-Check ausgeführt: Tag-Balance (`div`/`ol`/`li`), Skelett-Marker, `bad=0`, JS-Syntax via `node --check`

**Druckseiten (`downloads/.../*.html`)**
- [ ] Handout nur Theorie; „Seite drucken"-Knopf + Rück-Link; `print.css` eingebunden
- [ ] Saubere A4-Seitenwechsel; Anki-Deck erstellt und als `.apkg` verlinkt

**Technisch**
- [ ] MathJax lädt, alle Widgets funktionieren
- [ ] Responsiv auf Mobile (≤500 px Viewport)
