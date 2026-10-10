# Physik begreifbar · Styleguide

**Version 1.5 · Stand: 31. August 2026** · (1.5: §2.9 kein Gedankenstrich an einer Formel im Titel, Stilcheck-Regel 8 · 1.4: §2.1 Ersatztabelle für den Malpunkt als Trennzeichen — Strichpunkt statt Komma, wie in Mathe; Prüforte HTML/JS/Canvas · 1.3: §2.3 Liter klein sowie Basisgrösse gegen
abgeleitete Grösse und «Referenzeinheit», §5.7 kein HTML in einem LaTeX-Ausdruck,
Stilcheck-Regel 7 · 1.2: §6.1a Footer, Volltextsuche und `suche.js` im
Skelett, Zusatzmaterial ohne Formelauszug, Stilcheck-Regeln 1–6 · 1.1: §3.6 Label-Robustheit,
§3.7 Einheiten-Zweitzeile, §5.3 Gruppierung, §5.8 Direkt-Manipulation)

Verbindliche Referenz für alle Themenseiten des Lehrmittels „Physik begreifbar". Sichert Konsistenz in Notation, Aufbau, Sprache und visuellem Design — themenübergreifend und chatübergreifend.

Geforkt aus dem Styleguide von Mathe begreifbar (v1.8); nur die für Physik abweichenden Punkte sind hier ausführlich behandelt. Wo nichts anderes steht, gilt die Mathe-Konvention identisch weiter.

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
  **Rechen- und Wertanzeigen** — `.fl-eq`, `.lb-val`, `.sl-val`,
  Canvas-Beschriftungen mit Zahlen, Lösungswege, Rückmeldungstexte — bedeutet
  `·` ausschliesslich Multiplikation und wird **nie** als Trennzeichen
  verwendet. Das ist dort nicht bloss unschön, sondern falsch lesbar:
  `… = 83 °C · ΔT = …` liest sich als Produkt, und `7 / 10 · 70 %` erst recht.
  Stehen zwei Gleichungen nebeneinander, bekommt **jede eine eigene Zeile**
  (mehrere `.fl-eq` in derselben `.formel-live`; `style.css` setzt den Abstand
  über `.fl-eq + .fl-eq`). Wo das nicht geht — eine Canvas-Zeile hat nur den
  Platz, den sie hat —, trennt der Strichpunkt.

  | Situation | Ersatz | Beispiel |
  |---|---|---|
  | Zwei Werte desselben Objekts (Koordinaten, Stoffdaten) | Strichpunkt `;` | `250 mA; 120 ms` |
  | Zwei gleichrangige Ergebnisse oder Gleichungen in einer Zeile | Strichpunkt `;` | `1 A = 1 C/s;   1 C = 1/e ≈ …` |
  | Aufzählung von Fällen oder Formaten | Strichpunkt `;` oder echte Liste | `12.5; 12,5; 1.25e1` |
  | Etikett vor einem Wert | Doppelpunkt `:` | `Erde: g = 9.81 m/s²` |
  | Zusatzangabe zu einem Wert | Klammer | `7 / 10 (70 %)` |
  | Zwei aufeinanderfolgende Rechenschritte | Pfeil `→` | `1 m = Lichtweg in … → 3.33564 ns je Meter` |

  **Kein Komma als Trenner**, auch wenn Physik den Dezimalpunkt verwendet und
  das Komma darum eindeutig wäre: Der Strichpunkt gilt in **beiden**
  TALS-Projekten (Mathe-Styleguide §2.1), und der Einheitentrainer akzeptiert
  `12,5` als Eingabe — in einer Aufzählung wäre das Komma dort mehrdeutig.

  *Nicht betroffen:* Titel, Breadcrumbs, Quellen- und Fusszeilen, Bedienhinweise
  ohne Rechenkontext (`Physik · Lerngebiet 5`, `Animation 4 · Doppelter
  Zahlenstrahl`, `5 Treffer · ↑ ↓ wählen`) — dort ist der Punkt etablierte
  Typografie und bleibt. Ebenso bleibt er, wo er **Wörter** statt Zahlen trennt
  (`Basalt · Gneis`).

  **Prüfen:** Der Quelltext allein genügt nicht — die meisten Vorkommen entstehen
  erst zur Laufzeit, und in Physik lagen fünf von sieben Fundstellen auf einem
  **Canvas**, also gar nicht im DOM. Dafür gibt es

  ```bash
  node .claude/tools/scan-live.mjs themen/*.html          # nur Verdachtsfälle
  node .claude/tools/scan-live.mjs themen/p4-1-*.html --alle   # jede `·`-Zeile
  ```

  Das Skript fährt jede Seite durch ihre Bedienzustände (Umschaltknöpfe, Regler
  an beiden Anschlägen, eine ungültige und eine gültige Eingabe in jedes
  Textfeld) und liest dabei **beides**: den Text der Wertanzeigen und jeden
  `fillText`-Aufruf der Canvas.

  Es meldet, was sich zuverlässig erkennen lässt: **Zahl · Zahl in einer Zeile
  ohne Vergleichszeichen** — ein Produkt steht praktisch immer in einer
  Gleichung, ein Trennzeichen nie. Nicht erkennbar und darum Sache von `--alle`:
  «Etikett · Wert = …» (trägt ein `=`) und zwei vollständige Gleichungen
  nebeneinander, die strukturgleich zur korrekten Kette
  `P = 230 V · 8.0 A = 1840 W` sind. Das Skript ist ein Filter, kein Beweis.
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

**Geschwindigkeit und Tempo (Entscheid 06.10.2026, Stichwort «Stilcheck»).** «Tempo» ist das
Alltagswort für den **Betrag** der Geschwindigkeit und steht so im Glossar. Es darf bleiben, wo
genau der Betrag gemeint ist («konstantes Tempo auf der Kreisbahn»). Wo das Vorzeichen zählt
(geradlinige Bewegung, Steigung im s-t-Diagramm, Regler für \(v\)) oder wo der Begriff
eingeführt wird, steht **Geschwindigkeit**; wo Betrag und Richtung auseinandergehalten werden,
**Betrag der Geschwindigkeit**. In den Leitprogrammen der Kinematik steht durchgehend
Geschwindigkeit bzw. Betrag. «Tempomat» und «Animationstempo» (Abspieltempo) sind nicht gemeint.

### 2.3 Einheiten

- **SI-Einheiten** als Standard. Üblicherweise zusätzlich angegebene Praxiseinheiten: km/h, kWh, °C, bar — immer mit Hinweis auf die Umrechnung.
- **Zwischen Zahl und Einheit:** kein normales Leerzeichen, sondern **geschütztes Leerzeichen** in HTML (`&nbsp;`) bzw. `\;` in LaTeX:
  `9.81\;\text{m/s}^2` ✓
- **Einheit ist nicht kursiv**: Variable kursiv, Einheit aufrecht. In LaTeX die Einheit immer in `\text{...}` setzen.
- **Bruchstrich bei Einheiten:** `m/s` oder `m·s⁻¹`; die Slash-Variante ist üblicher und in der BM-Formelsammlung dominant.
- **Basisgrösse oder abgeleitete Grösse** (verbindlich seit 18.08.2026): Das SI kennt
  genau **sieben Basisgrössen** mit je einer Basiseinheit — Länge (m), Masse (kg),
  Zeit (s), elektrische Stromstärke (A), thermodynamische Temperatur (K), Stoffmenge
  (mol), Lichtstärke (cd). Alles andere ist **abgeleitet**: Fläche (m²), Volumen (m³),
  Kraft (N), Druck (Pa), Energie (J), Leistung (W), Dichte (kg/m³) — und auch die
  Geschwindigkeit. Entsprechend heisst es nie „die Grundgrössen Weg, Zeit, Masse und
  Volumen" (p0-2, korrigiert am 17.08.2026) und nie „Basiseinheit m²".
  Braucht eine Darstellung eine Bezugseinheit, auf die andere umgerechnet werden
  (Einheitentrainer, Umrechnungstabellen), heisst sie **Referenzeinheit**.
- **Liter mit kleinem l** (verbindlich seit 13.08.2026): `l`, `ml`, `dl`, `cl`, `kg/l`, `g/l`, `t/m³`,
  `l/min` — nie `L`, `mL`, `kg/L`. Das gilt für LaTeX (`1\;\text{l}`), Fliesstext (`150 l`),
  Tabellen, Live-Anzeigen und Canvas-Beschriftungen gleichermassen. Das Wort «Liter» bleibt
  als Substantiv gross.
  Achtung beim Nachziehen: Das grosse `L` ist im Repo mehrfach anders belegt und darf dort
  **nicht** angefasst werden — Saitenlänge \(L\) (`2L/n`, `A1L…A7L` in p6-1a), Pendellänge in
  `g/L` (p4-3), Balkenlänge in `x/L`, spezifische latente Wärme in \(Q = m L\) (p5-2),
  `mL` als margin-left (p4-4, p5-3) und «100 L» für Lektionen (nav.js). Eindeutig ist die
  Einheit nur innerhalb von `\text{…}`; alles andere von Hand prüfen.

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

**Schweizer Schul-Konvention**: Dezimal**punkt**, nicht Dezimalkomma. Gilt einheitlich für Mathe begreifbar und Physik begreifbar.

- **In Aufgabentexten und LaTeX-Werten**: `9.81\;\text{m/s}^2`, nicht `9,81` oder `9{,}81`.
- **In Live-Anzeigen** (über `fmt()` aus `physiklib.js`): automatisch Punkt (JS `toFixed` liefert Punkt von Haus aus).
- **In JS-Code-Literalen** (Slider-`min`/`max`/`step`, Konstanten wie `const g = 9.81`): Punkt — passt zu allem anderen.
- **Konvertierungs-Werkzeug**: bei Bedarf `scripts/convert_decimals.py` aufrufen — wandelt sicher Dezimalkomma → Dezimalpunkt um, ohne Koordinaten-Tupel, LaTeX-Subscripts, Google-Fonts-URLs oder SVG-Attribute zu zerschiessen.

### 2.6 Schreibweise von Werten und Toleranzen

- Signifikante Stellen: in der BM üblicherweise **3 Stellen** Genauigkeit. Endergebnisse passen ihr Stellenwerk an die Eingangsdaten an.
- Vorzeichen: bei negativen Werten Unicode-Minus `−` (U+2212) in Live-Anzeigen verwenden, nicht ASCII-Bindestrich `-`. Die `fmtS()`-Funktion in `physiklib.js` macht das automatisch.

### 2.6a Aufzählende Mengen mit Strichpunkt (verbindlich seit 30.09.2026)

Aus Mathe begreifbar übernommen (dort §2.11, Entscheid Auftraggeber 30.09.2026). Die
Elemente einer aufzählenden Menge trennt ein **Strichpunkt**, wie die Wertepaare in den
Live-Anzeigen (§2.1): `\(\{3;\,4\}\)`, in JS-Text `{ 3; 4 }` — nicht `\{3,\,4\}`. Das
Komma bleibt der Aufzählung in Prosa vorbehalten. Koordinaten schreiben weiter `(3 | 4)`.
Stand 03.10.2026 steht in Physik keine aufzählende Menge; die Regel gilt für künftige
Inhalte.

---

### 2.6b Preis und Kosten sauber trennen (verbindlich, Stichwort «Stilcheck»)

Zwei Grössen, die der Alltag beide «Preis» nennt, im Lehrmittel aber nie:

| Grösse | Bedeutung | Einheit |
|---|---|---|
| **Preis** \(p\) | Kosten **pro Einheit** | \(\text{CHF/kg}\), \(\text{CHF/km}\), \(\text{CHF/l}\) |
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

**Innerhalb einer Zahlengleichung bleiben die Einheiten unter sich stimmig.**
Ein Stoffwert je Kilogramm verträgt keine Masse in Gramm daneben — auch dann
nicht, wenn intern richtig gerechnet wird und das Ergebnis stimmt:

- `ΔT = W / (m · c) = 1.00 J / (0.00015 kg · 450 J/(kg·K)) = 14.8 K` ✓
- `ΔT = W / (m · c) = 1.00 J / (0.15 g · 450 J/(kg·K)) = 14.8 K` ✗

Die zweite Zeile ist zum Abschreiben unbrauchbar: Wer sie übernimmt und selbst
rechnet, landet um den Faktor tausend daneben. Gefunden am 08.09.2026 in zwei
Live-Zeilen des Leitprogramms «Wärme im Experiment».

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
Referenzen: `themen/p5-1-temperatur.html` a3, `themen/p0-2-vorwissen-physik.html` b2
(Tempo-Umrechner, Animation 9).

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

**Eine Rechnung, eine Zeile** (verbindlich seit 26.09.2026, Stichwort
«Stilcheck»): Formelzeichen, Formel, Zahlen mit Einheiten und Ergebnis stehen
als **eine Kette** auf einer Zeile — nicht Formel und Zahlengleichung in zwei
getrennten `.fl-eq`:

- \( I = \frac{U}{R} = \frac{6.0\;\text{V}}{100\;\Omega} = 60\;\text{mA} \) ✓
- zwei Zeilen `I = U/R` und darunter `I = 6.0 V / 100 Ω = 60 mA` ✗

Reicht der Platz nicht (360 px), bricht die Kette **vor einem
Gleichheitszeichen** um, nie mitten in einem Bruch. Umsetzung: `flTex(id, glieder)`
aus `physiklib.js` (seit 26.09.2026 auf allen Themenseiten, dazu `texE(zahl, einheit)`): jedes Glied (`I = \frac{U}{R}`,
`= \frac{…}{…}`, `= 60\;\text{mA}`) ist eine eigene Inline-Formel mit
`\displaystyle`, dazwischen `<wbr>`; ein führendes `=` bekommt ein `{}` davor,
sonst fehlt ihm links der Abstand; die Formel-Container werden `inline-block`,
damit umgebrochene Brüche sich nicht berühren. **Verschiedene** Rechnungen
bleiben getrennte Zeilen (§2.1); reine Aufzählungen (gegebene Werte) stehen mit
Strichpunkt auf einer Zeile. Eine einzelne Kette, die selbst als Glied zu breit
ist, scrollt (siehe unten).

Steht LaTeX im Kopf einer ❓-Frage, gehört der Kopftext in ein `<span>`
(`<summary><span>❓ … \(…\) …</span></summary>`): `.frage > summary` ist ein
Flex-Container, und jede Formel würde sonst ein eigenes Flex-Element — der Satz
zerfällt in Spalten.

**Einzelne Re-Typesets laufen über `mjTypeset(els)`** aus `physiklib.js` statt über
einen direkten `MathJax.typesetPromise(…)`-Aufruf. Der Helfer verkettet alle
Durchläufe seriell und hängt die erste Stufe an `MathJax.startup.promise` — damit
kollidiert kein eigener Aufruf mit MathJax' initialem Seitenrender und keine zwei
Re-Typesets überlappen sich auf denselben Elementen. Nur bei **dynamisch** (per
`innerHTML`) geänderter Mathematik aufrufen; statische HTML-Formeln rendert MathJax
beim Laden selbst. Wo eine Animation wie oben eine eigene, bereits serialisierte
Kette mit `typesetClear` führt (p5-2, Animation 2), bleibt diese — dort sichert die
lokale Kette zusätzlich die Reihenfolge von `typesetClear` und `innerHTML`.

**Escaping-Falle:** In JS-Strings muss der LaTeX-Backslash **doppelt** stehen.
`'\;\text{kg}'` ✗ liefert `;\text{kg}` — JavaScript verschluckt den einzelnen
Backslash. Richtig ist `'\\;\\text{kg}'`. Nach jeder Änderung an solchen
Strings die erzeugte Zeichenkette einmal in Node ausgeben lassen.

**Zu breite Formeln:** Displayformeln brechen nicht um. `.formel-live` hat darum
`overflow-x:auto` — auf schmalen Viewports scrollt die Box, statt die Formel
rechts abzuschneiden. Herunterskalieren wäre die schlechtere Wahl (unlesbar).
Dasselbe gilt seit 28.07.2026 für **abgesetzte Formeln im Fliesstext**: die Regel
`mjx-container[display="true"] { overflow-x:auto }` in `style.css` lässt sie im
eigenen Kasten scrollen. Vorher kappte `.page-wrap { overflow-x:hidden }` bei
≤ 900 px jede zu breite Zeile — betroffen waren 120 der 245 Displayformeln.
Formelzeilen müssen darum **nicht** künstlich kurz gehalten werden; mehrere
kurze Zeilen bleiben trotzdem die bessere Wahl, wo das Ansatz-Prinzip sie ohnehin
verlangt. Inline-Mathe ist nicht betroffen — sie fliesst im Text mit.

**Fallunterscheidung sichtbar machen:** Vereinfacht sich die Formel in einem
Sonderfall (z.B. \(c_1 = c_2\) → \(c\) kürzt sich), bekommt der Sonderfall
eine eigene Formelzeile, die nur in diesem Fall eingeblendet wird.
Referenz: `themen/p5-2-waerme.html`, Animation 2.

### 2.9 Kein Gedankenstrich an einer Formel im Titel (verbindlich, Stichwort «Stilcheck»)

Gerendert klebt der Gedankenstrich an der Formel und liest sich als Vorzeichen:
aus «Das Grundgesetz — \(F = m \cdot a\)» wird optisch \(-F = m \cdot a\).
Betroffen sind alle Titelarten — `h2`, `h3`, `.block-titel`, `.aufg-titel-text`
und die Diagrammtitel `.cv-titel` (seit 28.09.2026, Entscheid Auftraggeber in Mathe).

**Steht der Strich vor der Formel**, ersetzt ihn der **Doppelpunkt**; nach einem
Frage- oder Ausrufezeichen entfällt er ersatzlos:

| statt | richtig |
|---|---|
| `Das Grundgesetz — \(F = m \cdot a\)` | `Das Grundgesetz: \(F = m \cdot a\)` |
| `Werte ablesen — \(v\)-\(t\)-Diagramm` | `Werte ablesen: \(v\)-\(t\)-Diagramm` |
| `Was ist konstant? — \(s = v \cdot t\) …` | `Was ist konstant? \(s = v \cdot t\) …` |

**Steht der Strich nach der Formel**, hilft kein Ersatzzeichen — dort hängt sich
das Minus ans Formelende. Der Titel wird umgestellt: die Tätigkeit oder
Beschreibung an den Anfang, die Formel ans Ende, wo neben ihr nichts mehr steht
(`Animation 2 · \(E_{\text{kin}}(v)\) — die Energie-Parabel` →
`Animation 2 · Die Energie-Parabel: \(E_{\text{kin}}(v)\)`). Trägt der erste
Teil dagegen bloss ein Etikett (`⚠ Wichtig`, `🟢 Beispiel 2`), wird nicht
umgestellt, sondern der Strich durch den Doppelpunkt ersetzt.

**Nur direkter Kontakt zählt.** Steht zwischen Formel und Strich noch ein Wort,
klärt es die Lesart und der Titel bleibt, wie er ist — `Werte ablesen —
Federkraft` ist einwandfrei. **Fliesstext wird nicht angefasst:** dort ist der
Gedankenstrich ein Satzzeichen mit grammatischer Funktion.

Suchmuster für beide Richtungen: `[—–]\s*\\(` und `\\)\s*[—–]`.

**Dasselbe gilt für den Mittepunkt `·` direkt vor einer Formel** (seit
26.09.2026). Gerendert liest er sich als Malpunkt: aus
`Animation 3 · \(R = \rho\,l/A\)` wird optisch «3 mal R». Ersatz ist der
Doppelpunkt nach einer Beschreibung — `Animation 3 · Widerstand eines Leiters:
\(R = \rho\,l/A\)`. Das gilt auch für **Knopfbeschriftungen** mit Nummer
(`2 · \(R_2 \parallel R_3\)` → `2: \(R_2 \parallel R_3\)`). Der Punkt zwischen
Nummer und **Wort** bleibt (`Animation 4 · Zwei Widerstände in Reihe`, §2.1).
Suchmuster: `·\s*\\(` in Titeln und `<button>`.

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

**Überdeckte Skalenzahlen:** `drawGrid` zeichnet eine Skalenzahl, die eine später
gezeichnete Linie durchstreicht, am Ende mit weissem Rand neu — ausser sie ist
absichtlich zugedeckt (Fläche, Kasten). Dafür liest es die Pixel **nur der
Zahlenflächen** zurück und misst in laufenden Animationen nur jedes achte Bild neu
(vorher 8 ms pro Bild, jetzt unter 2 ms). Eigene Zeichenroutinen lesen **nie** pro
Bild das ganze Canvas zurück (`getImageData`) — das bremst jede laufende Animation.

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
| 1 | **Titel + RLP** | `.page-titel` mit Lerngebiet, `.rlp-kompetenzen` mit dem **Wortlaut** des RLP (§4.1), darunter die `.lernziele` mit allem, was dieses Haus daraus macht |
| 1b | **Vorwissen-Kasten** | direkt darunter ein `.block-tipp` «💡 Vorwissen zu dieser Seite»: zwei bis drei Abschnitte der Vorwissen-Reihe, die diese Seite wirklich voraussetzt — als **Anker** (`p0-3-messen-waagen-dichte.html#dichte`), nicht als blosser Seitenlink, dazu der Hinweis aufs passende Leitprogramm |
| 2 | **Einstieg** | Konkretes Alltagsphänomen, einleitende Frage, evtl. `.block-experiment` — der Kasten trägt das **Phänomen**, nie die Bedienung einer Animation (§5.6) |
| 3 | **Grundbegriffe** | `.block-def` für jeden zentralen Begriff (Schwerpunkt, Bahnkurve, Geschwindigkeit, Beschleunigung …) |
| 4 | **Animation 1** | Hauptphänomen interaktiv (z.B. gleichförmige Bewegung) — `.widget` mit `.cv-wrap`; Titelzeile mit Hinweisen «Worauf achten?» / «Erkenntnis» (§5.6) |
| 5 | **Theorie + Animation 2** | Herleitung der Bewegungsgleichungen mit `.block-beweis`, dann gekoppelte Diagramme |
| 6-9 | **Spezialfälle als Animationen** | Pro Spezialfall ein `.widget` (freier Fall, Wurf, Kreisbewegung, Vektoraddition …). Ziel: 5-10 Animationen total |
| 10 | **Aufgaben A1-A6** | Stufenweise nach Schwierigkeit: A1 ablesen → A2 rechnen einfach → A3 mehrteilig → A4-A6 Anwendung. **Alle sechs** Aufgaben nutzen identisch das `.block-aufg`-Muster aus §5.5 (siehe dort) mit `toggleL('lX')` — keine Sonderbehandlung einzelner Aufgaben |
| 11 | **Zusammenfassung** | `.ftb-tabelle` mit allen Formeln + `.merksatz` |
| 11b | **Clips** | generiert zwischen `<!-- CLIPS:ANFANG/ENDE -->` (`build-clips-einbau.py`): Clips zum Stoff, darunter die Clips zu den Animationen. Immer **nach der Zusammenfassung, vor dem Zusatzmaterial** (Entscheid Auftraggeber 27.09.2026) |
| 12 | **Zusatzmaterial** | `.dl-grid` mit 3 Druckseiten + Anki-Deck |
| 13 | **Externe Ressourcen** | **Dreispaltig**: 🎬 Videos · 🧪 Simulationen · 📝 Aufgaben |

### 4.1 Kompetenzblock: Wortlaut, nichts anderes

Der Block `.rlp-kompetenzen` gibt den **Wortlaut des Rahmenlehrplans** wieder —
Zeile für Zeile, in der Reihenfolge des RLP, ohne Kürzung und ohne Zusatz. Er
ist ein Zitat, kein Inhaltsverzeichnis der Seite. Alles, was dieses Haus daraus
macht — Formeln, Beispiele, zusätzliche Teilfähigkeiten, die Sprache in der
Ich-Form — gehört in die `.lernziele` **direkt darunter**. Dort darf und soll
über den RLP hinausgegangen werden.

```html
<div class="rlp-kompetenzen">      <!-- Zitat, 1:1 -->
  <li>das zweite Newton’sche Gesetz in einfachen Fällen (gleichmässig
      beschleunigte geradlinige Bewegung und gleichförmige Kreisbewegung)
      anwenden</li>
</div>
<details class="lernziele">        <!-- Ausformulierung dieses Hauses -->
  <li>Ich kann die Zentripetalkraft \(F_z = m v^2/r\) berechnen …</li>
</details>
```

**Die Quelle.** SBFI, *Rahmenlehrplan für die Berufsmaturität*, Bern,
13. Juni 2025, in Kraft seit 1. März 2026 — Schwerpunktbereich, Abschnitt
**7.5 Naturwissenschaften**, Unterabschnitt **7.5.4.1 Gruppe 1**, Seiten 85–88.
Der Auszug liegt als `../physik.pdf` neben dem Arbeitsverzeichnis, nicht im
Repo; das vollständige PDF steht beim SBFI.
Für Physik begreifbar gelten dort die Lerngebiete **4 Mechanik (100 Lektionen)**,
**5 Thermodynamik (30)** und **6 Einführung in andere Bereiche der Physik (30)**
mit zusammen **44 Kompetenzen**.

> **Die Falle: Der RLP enthält Physik viermal.** Je Berufsgruppe steht im
> Schwerpunktfach Naturwissenschaften eine eigene Liste. Verbindlich ist
> Gruppe 1 — der RLP sagt es selbst in der Vorbemerkung zu Gruppe 2: «Das Fach
> Physik ist für die gesamte Ausrichtung der Berufsmaturität Technik,
> Architektur, Life Sciences dasselbe.» Die Listen sind aber **nicht** wörtlich
> gleich: Gruppe 1 verlangt in 5.2 die Energieerzeugung «mit Hilfe des
> **Heizwertes**», Gruppe 3 (Land- und Forstwirtschaft, Lerngebiet 12.2, S. 100)
> «mit Hilfe des **Brennwertes**». Wer aus der falschen Gruppe zitiert, ändert
> den Inhalt. Am 08.09.2026 ist genau das in einem externen Prüfbericht passiert.

> **Zweite Falle: zwei Textstellen fehlen in jeder naiven Textextraktion.**
> Sie stehen im PDF in einem Subset-Font mit eigener Glyphenkodierung. Es sind
> ausgerechnet die tragenden Halbsätze «das zweite **Newton’sche Gesetz in
> einfachen Fällen (**gleichmässig beschleunigte …» (4.2) und «**das
> Pascal’sche Gesetz anhand einfacher Aufgaben anwen**den» (4.5). Ohne sie sieht
> 4.2 wie eine Ein-Punkt-Kompetenz aus und das Pascal-Prinzip fehlt ganz.

**Drei bewusste Abweichungen vom Wortlaut** — nicht zurückändern:

| Stelle | RLP | Seite | Grund |
|---|---|---|---|
| 5.1 | «Grad Celsius in **Grad Kelvin** umrechnen» | wörtlich übernommen, im Lernziel darunter richtiggestellt | «Grad Kelvin» gibt es seit 1967 nicht mehr; ein Zitat darf falsch sein, die Seite nicht |
| 6.1 | «(Beschaffenheit, … und ihre Absorption beschreiben.» | Klammer geschlossen | offensichtlicher Satzfehler der Quelle |
| 6.1 | «Absorption Sonnen- und Wärmestrahlung» | «Absorption **von** Sonnen- und Wärmestrahlung» | fehlende Präposition |

### 4.2 Sub-Splits

Bei umfangreichen Themen kann das `.widget`-Schema mit `id`-Suffix `a`/`b`/`c` strukturiert werden. Beispiel für ein langes Mechanik-Thema: 5 Animationen zur Translation + 2 zur Rotation. Trotzdem bleibt es **eine** Themenseite — kein zweites HTML-File.

### 4.3 Mindest- und Höchstinhalt

- **Mindestens** 5 Canvas-Animationen pro Themenseite
- **Höchstens** 10 Canvas-Animationen (sonst wird die Seite unleserlich; bei Bedarf Themenseite splitten)
- **Genau** 6 Aufgaben (A1-A6), nicht mehr — die Aufgabenserie unter „Zusatzmaterial" deckt mehr ab.
  Optional dazu **eine** Vertiefungsaufgabe (A7, Pille «Vertiefung», §5.5), immer am Ende der Reihe.
  **Ausnahmen** (festgehalten 03.10.2026, Inhalt bleibt, wie er ist): die Vorwissenseiten
  `p0-1` und `p0-2` (je A1–A12) und `p6-2` (A1–A16) — ohne Vertiefungsmarkierung.
- **Genau** 3 Druckseiten + 1 Anki-Deck unter „Zusatzmaterial": Handout,
  Teste-dich-selbst, Aufgabenserie. Einen seitenweisen Formelauszug gibt es seit
  dem 01.08.2026 nicht mehr — an seine Stelle tritt die illustrierte
  Gesamt-Formelsammlung als PDF (Menü „Nachschlagen").

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
- **Vertiefung:** Eine Aufgabe über den Kern hinaus trägt hinter dem Titeltext die Pille `<span class="aufg-vertiefung">Vertiefung</span>`.

**Vertiefung steht am Ende der Reihe (verbindlich seit 30.09.2026, aus Mathe §5.4).** Aufgaben mit der Pille «Vertiefung» kommen nach allen übrigen. Kommt später eine reguläre Aufgabe dazu, wird sie *vor* der Vertiefung eingereiht und die Vertiefung umnummeriert — mit allen IDs, `toggleL`-Argumenten und Prüffunktionen. Nicht zu verwechseln mit `.task-id .kern` / `.vert` in den Leitprogrammen: dieselbe Idee, andere Klassen — nicht vermischen.

### 5.6 Animations-Hinweise («Worauf achten?» / «Erkenntnis»)

Jede Animation trägt in der **Titelzeile** zwei dezente Rollover-Hinweise: nach dem Titel «💡 Worauf achten?», ganz rechts «✓ Erkenntnis». Sie ersetzen die frühere Bedienungszeile unter dem Titel (deren Inhalt steht jetzt in «Worauf achten?»).

Sie ersetzen **auch** den früheren Kasten «🧪 Beobachte» vor der Einstiegs-Animation. Eine Bedienanweisung («Erhöhe die Spannung und beobachte …») steht nur im Rollover, nicht zusätzlich in einem `.block-experiment` darüber — sonst steht sie zweimal. Referenz ist p5-2: `<h2 id="einstieg">`, dann das Phänomen im Fliesstext, dann das `.widget`. Der `.block-experiment` im Einstieg bleibt dem **Alltagsphänomen** oder einem Versuch mit echtem Material vorbehalten (§4, Punkt 2). Hat der Einstieg keine eigene Animation, steht der Vorwärtsverweis (`<a class="anim-ref" …>`) als gewöhnlicher Fliesstext; die Beobachtungspunkte gehören ins Rollover der Zielanimation.

- **Struktur:** Titel und beide Hinweise stehen gemeinsam in `<div class="widget-titelzeile">` (statt `<h3>` allein im `.widget-header`). Markup pro Hinweis:
  ```html
  <div class="anim-hinweis links">   <!-- bzw. "rechts" für Erkenntnis -->
    <span class="ah-trigger" tabindex="0" role="button" aria-haspopup="true" aria-label="…">💡 Worauf achten?</span>
    <div class="ah-pop" role="tooltip">
      <span class="ah-titel">Worauf achten?</span>
      <div class="ah-text"><ul><li>…</li></ul></div>
    </div>
  </div>
  ```
- **Inhalt — animationsspezifisch, mehrere Aspekte (je 4–5 Punkte):**
  - «Worauf achten?» = was man ausprobieren/beobachten soll (Slider-Verhalten, Grenzfälle, was in der Live-Anzeige zu verfolgen ist).
  - «Erkenntnis» = die physikalischen Schlüsse inkl. der zugehörigen Formeln.
- **Notation:** sichtbarer Text in **Projekt-Notation** (MathJax `\(…\)`, Dezimalpunkt, korrekte Symbole/Vektoren wie §2). Kein rohes `<` in der Mathe (sonst HTML-Konflikt) — «negativ» schreiben oder `\lt` verwenden.
- **Dritter Eintrag «▶ Clip»:** Gibt es einen Erklärclip zu genau dieser Animation
  (Drehbuch-Feld `animation`), setzt `build-clips-einbau.py` rechts in die Titelzeile
  den Knopf «▶ Clip» (zwischen `<!-- CLIP-ANIM -->`-Markern, nie von Hand). Details:
  `HOWTO-clips.md`.
- **Zentral, nicht pro Seite duplizieren:** Gestaltung in `style.css` (Abschnitt «Animations-Hinweise»), Logik in `anim-hinweise.js` (auf jeder Themenseite nach `physiklib.js` eingebunden). Die Logik regelt Hover/Fokus-Anzeige, **Klick fixiert** das Rollover (damit es auf Touch offen bleibt), Aussenklick/Escape schliesst. Die frühere Vorlese-Funktion ist am 31.07.2026 entfernt worden.

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
- **Kein HTML innerhalb eines LaTeX-Ausdrucks** (verbindlich seit 17.08.2026): MathJax
  bricht daran ab und zeigt die ganze Formel als Rohtext — sichtbar erst, wenn jemand
  das Akkordeon öffnet. Die Ausfüllstriche eines Lückentexts gehören darum **ausserhalb**
  der Formel:
  ```html
  ✗ \(W = \Delta E_{\text{<span class="mc-luecke"></span>}}\)
  ✓ \(W = \Delta E_i\). Welcher Index gehört anstelle von \(i\): <span class="mc-luecke"></span>?
  ```
  Der Pre-Flight prüft das seit dem 17.08.2026 und meldet jeden Treffer als `[FEHLER]`;
  das Kleiner-Zeichen in `\(a < b\)` bleibt erlaubt.
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

### 5.9 Animationsnummern und Verweise (verbindlich)

**Die Nummer einer Animation wird nie von Hand geschrieben** — weder im Titel noch im Verweis. Gepflegt wird allein der **Anker**; `python3 scripts/build-animationen.py` setzt beide Nummern aus der Dokumentreihenfolge. Grund: Früher trug jede Animation ihre Nummer als blossen Text, und ein nachträglich eingeschobenes Widget liess sämtliche Rückverweise auf die falsche Animation zeigen — ein Fehler, der beim Lesen nicht auffällt, weil die Nummer ja *existiert*.

Titel — der Anker steht am `<h3>`, sonst unverändertes Widget-Skelett:

```html
<h3 id="anim-je-desto-explorer">Animation 2 · Je-desto-Explorer — Federdehnung</h3>
```

Verweis im Fliesstext, im Mini-Check oder in einer Aufgabe:

```html
Vergleiche mit <a class="anim-ref" href="#anim-je-desto-explorer">Animation 2</a>.
```

Über Seitengrenzen mit Dateinamen davor:

```html
<a class="anim-ref" href="p0-1-vorwissen-mathematik.html#anim-dreisatz">Animation 6</a>
```

Innerhalb einer Link-Karte (`<a class="lk">`) wäre ein verschachteltes `<a>` ungültiges HTML — dort dieselbe Konvention mit `<span>`, das Ziel in `data-anim-ref`:

```html
<span class="anim-ref" data-anim-ref="p0-2-vorwissen-physik.html#anim-praefix-leiter">Animation 8</span>
```

Regeln:

- **Anker sind stabil.** Der Slug wird einmal aus dem Titel gebildet und danach nicht mehr geändert — auch nicht, wenn der Titel umformuliert wird. Nur so überlebt ein Verweis eine Titeländerung.
- **Ein Verweis nennt genau eine Animation.** Statt «die Animationen 4 und 5» zwei Verweise setzen («Animation 4 und Animation 5»), sonst kann der Generator die zweite Nummer nicht nachziehen.
- **Kein blosser Text.** Der Pre-Flight meldet jedes freistehende «Animation N» im Markup als `[FEHLER]`. Ausgenommen sind `<script>`- und `<style>`-Blöcke, wo kein Markup möglich ist — dort steht die Nummer nur in Kommentaren und ist von Hand zu pflegen.
- Der Generator meldet ausserdem Titel ohne Anker und Verweise auf Anker, die es nicht gibt.

---

### 5.10 Werte und Bewegung in Animationen (Entscheide 27.09.2026)

- **Eine Grösse, eine Rundung.** Derselbe Wert steht im Canvas, in der Live-Box und in
  der Formelzeile mit denselben Stellen — nicht «U₁ = 3.75 V» an der Beschriftung und
  «3.8 V» im Balken, nicht «120 mA» neben «60.0 mA». Wer eine Anzeige ergänzt, prüft
  alle Stellen, an denen die Grösse sonst noch steht.
- **Voreinstellungen treffen die Werte der Seite.** Ein Regler, ein Gerät oder ein
  Szenario ergibt genau die Zahl, die der Text nennt: Scheitel 325.3 V (= 230 V · √2),
  damit der Effektivwert 230.0 V ist und nicht 229.8 V; ein Gerät «2000 W» setzt
  \(I = P/U\) exakt statt 8.7 A (= 2001 W). Rastet ein Regler auf ein Szenario ein
  und verfälscht es (230 mA → 229 mA), bekommt er `step="any"`. Verlangt «Worauf
  achten?» eine Einstellung, muss sie sich auch einstellen lassen.
- **Keine Bewegung ohne Anlass.** Ein Punkt, der von selbst durch ein Diagramm
  wandert, lenkt ab. Momentanwerte zeigt ein Regler «Zeitpunkt t», den man selbst
  verschiebt (Referenz: Animation «Wechselspannung und Effektivwert», p6-2). Selbst
  laufen darf, was das Phänomen selbst ist (Elektronenfluss, Welle).
- **Beschriftungen über Kurven bekommen einen hellen Grund**, und eine bewegliche
  Beschriftung weicht den festen aus — sie wählt die erste freie von mehreren Lagen um
  ihren Punkt, gemessen an den echten Rechtecken der festen Beschriftungen, Achsen
  und Skalenzahlen (Referenz: `wsMarke` in p6-2). Prüfen über **alle** Zustände, nicht
  an einem Bild.
- **Bewegte Punkte vollständig beschriften (06.10.2026, Stichwort «Stilcheck»):** Ein Punkt,
  der sich mit einem Regler durch ein Diagramm bewegt, trägt beide Koordinaten mit Einheit,
  «(8 s; 60 m)», nicht nur «s = 60 m» — man liest sonst den Zeitpunkt an der Achse nach.
  Trennzeichen ist der Strichpunkt (§2.6a).
- **Steigungsdreiecke lesbar (06.10.2026, Stichwort «Stilcheck»):** Die Schenkel und ihre
  Beschriftungen (Δt, Δv mit Einheit) liegen nicht unter der Punktbeschriftung, nicht auf der
  Fortsetzung der Geraden und nicht auf der Flächenbeschriftung. Bewährt: das Dreieck **ab dem
  Punkt nach rechts** ansetzen, Δ-Wert rechts neben dem senkrechten Schenkel (beim Fallen auf
  Höhe der oberen Kante).
- **Zeichnung und Rechnung trennen:** Die Rechnung bildet immer die reale Situation ab;
  ein Umschalter darf nur die Darstellung ändern (z. B. Schaltbild ↔ Ersatzschaltbild
  mit Innenwiderständen), nicht das Modell.

### 5.11 Bild neben Bedienung (`.anim-layout`, Entscheid 30.09.2026)

Üblich stehen Bedienung, Formelzeile, Live-Box und Bild untereinander.
**`.anim-layout` wird genommen, wenn Bedienung und Bild untereinander bei 1280×720 höher
als etwa 650 px würden** — dann sieht man beim Bedienen das Bild nicht mehr. Die Bedienung
rückt rechts neben das Bild; Formelzeile und Live-Box folgen darunter über die volle Breite.

```html
<div class="widget-body">
  <div class="anim-layout">
    <div class="anim-layout-bild"><div class="cv-wrap">…Titel, Canvas, Legende…</div></div>
    <div class="anim-layout-bedienung">…sl-row, typ-btns, play-btn…</div>
  </div>
  <div class="formel-live">…</div>
  <div class="live-box">…</div>
</div>
```

- Rechte Spalte 320 px. Darin stehen Reglerzeilen anders als sonst: Etikett oben, Regler
  über die volle Breite, Wert rechts daneben. Die Legende im Bild wird zweispaltig; ein
  einzelner Eintrag (ein Satz statt Linienmuster) läuft über beide Spalten. Das
  regelt `style.css` zentral, kein lokales CSS.
- **Unter 1100 px Fensterbreite einspaltig:** zuerst das Bild, darunter die Bedienung.
- Modifikator **`.voll`**: einspaltig auch in der Breite, die Bedienung rückt über das
  Bild. Für einen Zustand, der die ganze Breite braucht (Wassermodell: «Beide Kreise
  untereinander»). Die Animation setzt die Klasse selbst und löst danach ein `resize`
  aus, damit die Canvas neu misst.
- Canvas im Bild richten ihre Grösse nach `offsetWidth`, nie nach einer festen Breite —
  die Bildspalte ist bei 1280 px rund 600 px breit, nicht 900 px.
- **Mehrere Bilder in einer Animation:** Nur so viel in die Bildspalte, wie dort lesbar
  bleibt. Bei 6.1a «Die zwei Gesichter einer Welle» steht die 3D-Ansicht neben der
  Bedienung, Momentbild und Mitschrieb folgen darunter über die volle Breite.
- **Die Zeichnung im schmaleren Bild prüfen,** in allen Bedienzuständen und bei 1100 px
  (knapp über dem Umbruch): Breitenschwellen im Zeichencode (`schmal = W < …`) können jetzt
  auch auf dem Desktop greifen, und Beschriftungen stossen an (Stilregel 10).
- **Kein Seiten-Zoom als Ausweg** (Zoom 90 % am 30.09.2026 eingebaut, am 02.10.2026
  zurückgenommen): Den Zoom stellt der Leser im Browser selbst ein.
- Im Einsatz (Stand 02.10.2026): p6-2 Anim. 1 «Wassermodell», 3, 4, 9, 10 «Wechselspannung
  und Effektivwert», 11, 13; p6-1a Anim. 1 bis 6; p0-1 «Kreis, Winkel und Bogenmass» und
  «Gegenrechnung»; p0-3 «Dichte-Labor»; mit zweitem Bild über die volle Breite: p0-2
  «Tauchgang», p4-1 «Schwimmer im Fluss», p6-1 «Durchlässigkeit der Atmosphäre». Referenz für das Markup: p6-2
  `anim-wassermodell` und `anim-wechselspannung-effektivwert`.

### 5.12 Bedienung im Bild (Muster, Entscheid 30.09.2026)

Wo ein Gerät im Bild steht (Drehschalter, Buchsen, Schalter), darf man es dort anklicken.
Die Knöpfe bleiben trotzdem da und bleiben die **einzige Quelle des Zustands**:

- **Klickflächen beim Zeichnen registrieren.** Die Zeichenfunktion leert zu Beginn eine
  Liste und trägt jede Fläche in den Koordinaten ein, in denen sie sie gerade zeichnet
  (Rechteck, Kreis, Sektor), samt Selektor des zugehörigen Knopfs. So stimmen Bild und
  Fläche auch in der schmalen Fassung. Mindestmass etwa 38 Canvas-px.
- **Ein Klick ruft `.click()` auf den vorhandenen Knopf** — keine zweite Logik. Umrechnung
  der Mauskoordinaten über `getBoundingClientRect()` ins Canvas-System (unabhängig von
  `devicePixelRatio` und vom Browser-Zoom).
- **Affordanz:** Hover rahmt die Fläche in Bernstein und setzt `cursor:pointer` (nicht
  bei Touch); anklickbare Stellen tragen im Bild eine Pille, einen Ring oder ein
  Symbol (Schere zum Auftrennen). Der `cv-titel` sagt, was sich anklicken lässt.
- **Knöpfe als Tastatur-Ersatz** in einem zugeklappten Aufklapper direkt unter dem Bild:
  `<details class="mc-loesung">` mit dem Titel «Bedienung mit Knöpfen (auch per Tastatur)».
- Referenz: p6-2, Animation «Multimeter bedienen» (`mbZonen`, `mbRect`, `mbTreffer`,
  `mbHoverZeichnen`, Handler in `mbInit`).

## 6. Code-Konventionen

### 6.1 HTML-Skelett

Strikt einhalten, sonst bricht das Layout. Jede Themenseite hat folgende Wurzelstruktur:

Im `<head>` steht direkt nach dem `<title>` der generierte SEO-Block zwischen
`<!-- SEO:ANFANG -->` und `<!-- SEO:ENDE -->` (Beschreibung, canonical, Favicons,
Open Graph, JSON-LD). Er wird **nie von Hand** bearbeitet, sondern über
`scripts/build-seo.py` erzeugt; eine neue Seite muss dort in der Tabelle `SEITEN`
eingetragen werden.

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
<footer class="site-footer">...</footer>   <!-- 5 Zeilen, siehe §6.1a -->
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script src="../physiklib.js"></script>
<script>
  buildNav({ id, kapitelNr, kapitelTitel, prev, next });
  // ... Animation-Code ...
</script>
</body>
```

### 6.1a Footer

Auf jeder Seite identisch, nur die zweite Zeile ist seitenspezifisch. Relative Pfade
auf Themenseiten mit `../`, auf Root-Seiten ohne:

```html
<footer class="site-footer">
  <p><strong>Physik begreifbar</strong> — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences</p>
  <p>Physik · 4.2 Dynamik</p>                          <!-- seitenspezifisch -->
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.0 · Stand 1. August 2026</p>
</footer>
```

**Kein GitHub-Link im Footer** — er steht bewusst nur einmal, im Über-Panel unter
„Lizenz". „GitHub" ist für die Lernenden Fachjargon. Seit dem Umzug auf
`physik.begreifbar.ch` verrät die Adresse das Repo nicht mehr — der Link im Über-Panel
ist darum der einzige Weg dorthin, und er bleibt dort.

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

### 6.5 Leitprogramme (verbindlich, Fassung 03.10.2026)

Ein Leitprogramm ist eine eigenständige Seite unter `leitprogramme/` zum
selbstständigen Durcharbeiten. Es ist **keine Themenseite** und folgt darum nicht dem
Skelett aus §6.1. Es gibt zwei Arten, mit **identischem Layout** und verschiedener
Gliederung:

| | gegliedert nach | Beispiele (Stand 09.10.2026) | Anleitung |
|---|---|---|---|
| **Thema** | dem Stoff: Vortest, Kapitel bzw. Schritte, Gesamttest | klassisch: `leitprogramm-rechnen`, `leitprogramm-experimente-waerme` (drei aktive, dazu sieben veraltete); Kapitelmuster: `leitprogramm-elektrizitaet`, die fünf der Mechanik, die drei der Thermodynamik und `leitprogramm-wellen` | `HOWTO-leitprogramme.md` |
| **Übungsprüfung** | dem Prüfungsbogen: je Aufgabe ein Clip, Musterlösung, Fehlerkasten | `uebungstest-waermelehre` | `HOWTO-uebungspruefung.md` |

**Umfang eines Themen-Leitprogramms:** rund **6 bis 11 Clips** und **8 bis 12 Minuten**
Clipzeit, aufgeteilt auf vier bis fünf Kapitel (klassisches Format: bis sieben Schritte)
mit je einem Selbsttest, dazu ein Gesamttest von 20 bis 25 Punkten. Wird ein Thema
deutlich grösser, gehört es geteilt — zwei Programme mit je eigenem Vortest und
Gesamttest tragen mehr als eines mit zwei unverbundenen Hälften. Die Wärmelehre ist aus
diesem Grund auf vier Leitprogramme verteilt (Wärmemenge, Heizen, Wärmeausdehnung,
ideale Gase). Zeitrahmen und Kapitelmuster: `HOWTO-leitprogramme.md` §3–§4.

**Ein Leitprogramm je RLP-Teilgebiet (Entscheid 06.10.2026).** Pro Teilgebiet gibt es ein Leitprogramm als Kurs und die Themenseite als Nachschlagewerk; Weiterführendes gehört auf die Themenseite, nicht in ein zweites, überlappendes Leitprogramm. Wird ein Leitprogramm aufgelöst, steht es zuerst als veraltet markiert im Netz (Hinweis im Seitenkopf, Abschnitt «Veraltet: wird entfernt» auf `leitprogramme.html`, `noindex`), damit angefangene Arbeiten abgeschlossen werden können; nach der Löschung bleibt an seiner Adresse eine Weiterleitung (`meta refresh`, `canonical`, `noindex`) auf den passenden Abschnitt der Themenseite, und die Seite kommt in `UNVERLINKT`.

**Inhaltlich gebunden an RLP und Themenseite.** Ein Leitprogramm deckt die Kompetenzen
genau eines Teilgebiets ab (RLP 7.5.4.1, Gruppe 1, Wortlaut wie im Kompetenzblock der
Themenseite, §4.1) — nicht mehr. Notation, Formelzeichen, Einheiten und Beispiele kommen
von der Themenseite; das Leitprogramm bestimmt nur den Weg.

**Der `localStorage`-Schlüssel ist je Seite eigen** (`var KEY = 'leitprogramm-<name>-v1'`).
Wer eine Seite als Vorlage kopiert und ihn vergisst, lässt zwei Leitprogramme denselben
Fortschritt teilen: Das Häkchen im einen erscheint im anderen.

Hier nur, was für beide Arten nicht verhandelbar ist.

- **`leitprogramme/` liegt genau eine Ebene unter der Wurzel**, wie `clips/`. Alle
  relativen Pfade setzen das voraus.
- **Kein fremder Host.** Schriften über `../schriften.css`, MathJax über
  `../vendor/mathjax/tex-svg.js` — wie überall sonst (der Pre-Flight meldet
  `fonts.googleapis.com`, `fonts.gstatic.com` und `cdn.jsdelivr.net` als Fehler).
- **Vollständiger Dokumentrahmen.** `<!DOCTYPE html>`, `<html lang="de-CH">`,
  `<meta charset="UTF-8">` in den ersten 1024 Bytes, Viewport. Ohne Zeichensatz rät der
  Browser falsch, und die Umlaute zerfallen — sichtbar erst im Browser, in keiner Prüfung.
- **Kopf und Fuss der Site gehören dazu.** `<div id="nav-root">`, ein `.site-footer` nach
  §6.1a und vor `</body>` `../physiklib.js`, `../nav.js`, `../suche.js` und
  `buildNav({ id: 'leitprogramme' })`. Ohne Kopf und Fuss ist die Seite eine Sackgasse;
  ohne `physiklib.js` läuft jede Clipkarte ins Leere, weil `clipBuehne` von dort kommt.
- **Geerbt wird, nicht kopiert.** `../style.css` **vor** dem eigenen `<style>` einbinden
  (dann gewinnt das eigene Layout bei gleichem Gewicht), Farbtokens aus `style.css`
  nehmen, die Clip-Bühne aus `physiklib.js`. Eine mitgelieferte Kopie der Bühne oder der
  Palette wird gelöscht — sie stimmt heute und läuft morgen auseinander. Klassen, die es
  auch in `style.css` gibt (z. B. `.frage`), nehmen die fremden Eigenschaften ausdrücklich
  zurück.
- **Eigenes Layout ist erlaubt und erwünscht.** Ablaufspalte, Fortschrittszähler,
  Testköpfe stehen im eigenen `<style>`. Das Leitprogramm wird *nicht* in `page-wrap` +
  `main.content` gepresst.
- **Ein Dunkelmodus ist erlaubt** (man liest ein Leitprogramm am Stück), muss dann aber
  `--weiss` mitsetzen — `style.css` färbt seine Flächen damit — und `.site-footer`
  eigens behandeln, weil der `--tinte` als Fläche benutzt; die Systemvariante dieser
  Regel steht in der Media-Abfrage.
- **Kapitelüberschriften brauchen `id`.** Die Suche schneidet an `h2[id]`; ohne Anker
  ist die ganze Seite ein einziger Treffer.
- **Kein LaTeX in kleinen Textbausteinen** (`figcaption`, `.sim-lab`, `.sim-out`,
  `.step-goal`, `.scene-cap`) — MathJax setzt dort riesig.
- **Clips nur über `.clipkarte` aus `clips/`**, kein ins Dokument eingebetteter Ton.
  Leitprogramm-eigene Clips tragen `"probe": true` (nicht in der Bibliothek, auf keiner
  Themenseite).
- **Eintragen an vier Stellen:** Karte in `leitprogramme.html` (zwischen den
  `LEITPROGRAMME`-Markern, unter dem Lerngebiet), Eintrag in `build-seo.py`, Kasten
  «💡 Lieber geführt durcharbeiten?» auf der Themen- bzw. Vorwissenseite;
  `build-suchindex.py` erfasst `leitprogramme/` von selbst — ausser den Seiten in seiner
  Menge `UNVERLINKT`.
- **Unverlinkt veröffentlichen ist erlaubt — aber nur vollständig.** Soll eine Seite
  ausgeliefert, jedoch nicht gefunden werden (Erprobung vor der Freischaltung, eine
  Übungsprüfung per Link), dann: keine Karte in `leitprogramme.html`, kein Kasten auf der
  Themenseite, nicht im Suchindex (Pfad in `UNVERLINKT` von `build-suchindex.py`), und in `build-seo.py` ein Eintrag **mit
  `noindex=True`** (nicht das Weglassen — sonst fehlen Beschreibung und canonical).
  `noindex=True` nimmt die Seite aus der Sitemap *und* setzt
  `<meta name="robots" content="noindex, nofollow">`. **Kein `Disallow` in
  `robots.txt`** — die Datei ist öffentlich lesbar und würde die URL gerade
  bekanntmachen. Und es bleibt Unauffindbarkeit, keine Zugangskontrolle: Wer den Link
  hat, kommt hinein.
- **Kontrollfragen zeigen die Antwort im Bild (06.10.2026).** Jede Antwortszene eines
  Kontrollclips trägt neben Formel oder Notiz ein Bild, das die Antwort sichtbar macht
  (Steigungsdreieck, Fläche, Pfeile, abgelesener Punkt, Vergleich) — nicht nur eine
  Formelzeile. Steht in der Szene schon ein `graf` für eine klick-Frage, kommt die Antwort als
  zweite Ebene (`"achsen": false`) darüber, sonst stünde sie schon während der Frage im Bild.
- **Rechnungen im Einführungsclip entwickeln sich im Diagramm (06.10.2026).** Ein Weg als
  Fläche, eine Beschleunigung als Steigung: Fläche, Masse (Breite, Höhe) und Ergebnis
  erscheinen im Diagramm in dem Moment, in dem der Ton sie nennt — nicht ein fertiges
  Simulationsbild neben der Formel.
- **Jede Leistenaufgabe gibt etwas zu denken (06.10.2026).** Aufgaben, die nur «stelle ein» oder
  «triff» verlangen, bekommen einen Auftrag zum Notieren, Deuten oder Vergleichen («Welche
  Bewegungsart stellt der Graf dar?», «Notiere den Bremsweg — in der nächsten Aufgabe
  vergleichst du») und eine Vergleichsantwort.
- **Neue Leitprogramme werden vor der Freischaltung unabhängig geprüft**
  (`HOWTO-leitprogramme.md` §15, Skill `/lp-pruefung`); die bestehenden elf bleiben, wie
  sie sind.
- **Gesamttest neuer Leitprogramme als PDF aus LaTeX** mit getrenntem Bewertungspaket
  (`downloads/leitprogramme/lp-druck.sty`, `scripts/build-lp-pdf.py`;
  `HOWTO-leitprogramme.md` §9). Ob die bestehenden HTML-Gesamttests umgestellt werden,
  entscheidet der Auftraggeber.

#### Nur bei der Art «Übungsprüfung»

- **Die Aufgabentexte stehen wörtlich da**, samt Punktzahl — geglättete Formulierungen
  erklären eine andere Prüfung als die, die geschrieben wurde.
- **Je Aufgabe ein Clip**, und die Clips tragen `"probe": true` — sie gehören zur Seite,
  nicht in die Bibliothek und nicht auf eine Lektionsseite.
- **Das Prüfungs-PDF misstrauisch lesen**; der Prüfungsrahmen bleibt weg, ohne dass die
  Aufgaben leiden. Einzelheiten: `HOWTO-uebungspruefung.md`.

### 6.6 Simulationen und Werkzeuge (verbindlich seit 10.10.2026)

- **Drei Formen, eine Regel.** Eine *Animation* steht in der Themenseite. Eine eigene Seite
  bekommt ein Inhalt nur, wenn er mehr als einen Bildschirm braucht, eine eigene Abfolge hat
  oder auch ohne die Themenseite benutzt wird. Dann ist er eine **Simulation**
  (`simulationen/`: Vorgang beobachten, Grössen verändern) oder ein **Werkzeug**
  (`werkzeuge/`: eigene Aufgaben oder Messwerte eingeben, üben). Gibt man eigene Daten ein,
  ist es ein Werkzeug.
- **Verlinkt wird im Abschnitt**, in den der Inhalt gehört — nicht am Seitenanfang wie das
  Leitprogramm, nicht auf den Kacheln von `index.html`. Baustein, wörtlich:
  `<div class="block block-tipp"><div class="block-titel">🧪 Simulation: Titel</div><p>Ein Satz,
  was man dort tut. <a href="../simulationen/x.html">Zur Simulation →</a></p></div>` bzw.
  «🛠 Werkzeug: Titel» … «Zum Werkzeug →» mit `../werkzeuge/`.
- **Rücklink** als Satz am Ende von `pt-untertitel`, per Anker auf den Abschnitt
  (`../themen/x.html#anker`). Kopf: `pt-bereich` «SIM · Simulationen» bzw. «WZ · Werkzeuge».
- **Übersicht** `simulationen.html` / `werkzeuge.html` nach Lerngebiet, Seiten ohne
  Lerngebiet unter `<h2 id="ausserhalb">`. `buildNav({ id:'simulationen' })` bzw.
  `'werkzeuge'`, ohne `kapitelNr`, `prev`, `next`.
- Alles Weitere: `HOWTO-simulationen.md`, `HOWTO-werkzeuge.md`.

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

## 8. Was sich gegenüber Mathe begreifbar geändert hat

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
- [ ] Genau 6 Aufgaben (A1–A6) mit zunehmender Selbstständigkeit; optional eine Vertiefung (A7, Pille «Vertiefung») am Ende der Reihe. Ausnahmen: §4.3
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
- [ ] Zusatzmaterial-Sektion vor externen Ressourcen, 3 Druckseiten + Anki-Deck verlinkt
- [ ] Druckseiten öffnen in neuem Tab (`target="_blank" rel="noopener"`)
- [ ] Externe Ressourcen **dreispaltig** (🎬 Videos · 🧪 Simulationen · 📝 Aufgaben), alle per `web_fetch` verifiziert
- [ ] Block-Modifier nur aus dem Inventar von §5.1 plus `block-experiment` — **keine Eigenkreationen**
- [ ] **Keine lokale Redefinition** zentraler Klassen (`widget`, `sl-row`, `live-box`, `aufg-*`, …) im `<style>` der Themenseite — nur genuin seitenspezifische Layouts dürfen lokal stehen

**HTML-Skelett (siehe §6.1)**
- [ ] Body-Struktur: `body > div#nav-root > div.page-wrap > main.content` + Geschwister `aside.toc-wrap`
- [ ] `<main class="content">` — nicht `inhalt` o.Ä.
- [ ] Anker-IDs direkt am `<h2 id="…">` — keine `<section>`-Wrapper
- [ ] `<script src="../nav.js">` direkt vor dem `buildNav()`-Inline-Script
- [ ] `../style.css`, `../suche.js` und `../physiklib.js` verlinkt
- [ ] Footer nach §6.1a (fünf Zeilen, kapitelspezifische Zeile angepasst)
- [ ] Pre-Flight-Bash-Check ausgeführt: Tag-Balance (`div`/`ol`/`li`), Skelett-Marker, `bad=0`, JS-Syntax via `node --check`

**Druckseiten (`downloads/.../*.html`)**
- [ ] Handout nur Theorie; „Seite drucken"-Knopf + Rück-Link; `downloads/print.css` eingebunden
- [ ] Saubere A4-Seitenwechsel; Anki-Deck erstellt und als `.apkg` verlinkt

**Technisch**
- [ ] MathJax lädt, alle Widgets funktionieren
- [ ] Responsiv auf Mobile (≤500 px Viewport)
