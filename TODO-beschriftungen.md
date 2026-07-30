# TODO — Beschriftungskonflikte in Canvas-Animationen

Befund vom **30.07.2026**. Geprüft wurden **alle 136 Canvas auf den 14 Themenseiten**
in der **Startposition** bei **1280 px**. Gefunden: **19 Grafiken** mit Beschriftungen,
die mit anderen Grafikelementen kollidieren. **An den Animationen wurde nichts geändert** —
diese Liste ist reine Bestandsaufnahme.

Die Links öffnen die Stelle direkt. Voraussetzung ist der lokale Server:

```bash
cd /home/paps/tals-physik && python3 -m http.server 8000
```

Der Link springt auf den Abschnitt; die betroffene Grafik steht dort in der genannten
Animation (Canvas-ID in Klammern, im Browser über die Entwicklerwerkzeuge auffindbar).

---

## A · Deutlich — Beschriftung unlesbar oder verstümmelt

- [ ] **[4.1 Herleitung](http://localhost:8000/themen/p4-1-kinematik.html#theorie)** ·
  Herleitungsgrafik zum Trapez unter dem v-t-Graph (`herl-cv`)
  → „Fläche = s − s₀" liegt zu 87 % auf „v₀ · t"; beide Wörter überlagern sich zu einer
  unlesbaren Zeile.

- [ ] **[6.2 Ohmsches Gesetz](http://localhost:8000/themen/p6-2-elektrizitaet.html#ohm)** ·
  Animation 1 · U-I-Kennlinie (`a1-cv`)
  → „100 Ω (Referenz)" und „(60 mA | 6.0 V)" liegen übereinander.

- [ ] **[4.5 Schweredruck](http://localhost:8000/themen/p4-5-hydrostatik.html#schweredruck)** ·
  Animation 1 · Flüssigkeitssäule mit Manometer (`a1-cv-saeule`)
  → Der Messkasten „p_S / 29.4 kPa / (0.29 bar)" liegt auf der Skalenmarke „0 m";
  „(0.29 bar)" wird zusätzlich vom Kastenrand angeschnitten.

- [ ] **[5.1 Skalen](http://localhost:8000/themen/p5-1-temperatur.html#skalen)** ·
  Animation 3 · Thermometer mit beiden Skalen (`a3-cv`)
  → Die Skalenköpfe „°C" und „K" sitzen auf den obersten Teilstrichwerten „150" und „423".

- [ ] **[0.1 Je–desto](http://localhost:8000/themen/p0-1-vorwissen-mathematik.html#jedesto)** ·
  Animation 1 · Glacé und Sonnenbrand (`b6-korr-cv`)
  → Achsentitel „Glacé [Portionen]" liegt auf dem letzten Teilstrichwert „340", der dadurch
  auf „3" verkürzt erscheint.

- [ ] **[4.3 Arbeit](http://localhost:8000/themen/p4-3-energie.html#arbeit)** ·
  Animation 1 · Arbeit als Fläche im F-s-Diagramm (`a1-cv-diag`)
  → Der Achsenwert „2.0" wird von der Rechteckkante zerschnitten und liest sich als „2  0".

- [ ] **[4.1 Einstieg](http://localhost:8000/themen/p4-1-kinematik.html#einstieg)** ·
  Einstiegs-Animation · Zugfahrt Bern–Zürich im v-t-Diagramm (`a0-cv`)
  → Die Marke „t₁" liegt auf dem Achsenwert „160".

- [ ] **[4.4 Resultierende](http://localhost:8000/themen/p4-4-statik.html#resultierende)** ·
  Animation 2 · Vektoraddition zweier Kräfte (`a2-cv`)
  → Vektorname „F2" liegt auf dem Achsenwert „40".

- [ ] **[5.2 Treibhauseffekt](http://localhost:8000/themen/p5-2-waerme.html#treibhaus)** ·
  Methan-Panel im Treibhausgas-Vergleich (`thg-ch4`)
  → Gedrehter Achsentitel „ppb" kreuzt den Wert „1000".

- [ ] **[6.2 Gefahren](http://localhost:8000/themen/p6-2-elektrizitaet.html#gefahren)** ·
  Animation 6 · Stromstärke-Zeit-Diagramm (`a6-cv`)
  → Gedrehter Achsentitel „Einwirkzeit [ms]" kreuzt „1000" und „10000"; der Wert „1" ragt
  30 px über den linken Rand hinaus.

- [ ] **[4.4 Drehmoment](http://localhost:8000/themen/p4-4-statik.html#drehmoment)** ·
  Animation 4 · Drehmoment, Hebelarm und Winkel (`a4-cv`)
  → „r = 0.26 m" und „l = 0.30 m" berühren sich, das „m" sitzt auf dem „l =".

- [ ] **[4.5 Auftrieb](http://localhost:8000/themen/p4-5-hydrostatik.html#auftrieb)** ·
  Animation 4 · Auftriebskraft beim Eintauchen (`a4-cv-quader`)
  → „F_A = 5.89 N" stösst an „0.98 N"; „0.98 N" und „von 6.87 N" laufen in den rechten Rand.

## B · Am Rand abgeschnitten oder hinter Bauteilen

- [ ] **[4.5 Pascal](http://localhost:8000/themen/p4-5-hydrostatik.html#pascal)** ·
  Animation 3 · Hydraulische Presse (`a3-cv`)
  → „s₁=20 cm" beginnt 6 px links ausserhalb der Zeichenfläche — das „s" fehlt.

- [ ] **[4.3 Kinetische Energie](http://localhost:8000/themen/p4-3-energie.html#kinetisch)** ·
  Animation 2 · Fahrzeug in Bewegung (`a2-cv-szene`)
  → Die vier Massstabswerte „0 m" bis „60 m" ragen unten aus der Zeichenfläche und sind
  halb abgeschnitten.

- [ ] **[6.1a Saite](http://localhost:8000/themen/p6-1a-wellenexperimente.html#saite)** ·
  Animation 7 · Eigenschwingungen der eingespannten Saite (`a7-cv`)
  → Die Einspannbalken liegen über den Achsenwerten: „2" und „4" links verdeckt,
  „2.0" rechts zerschnitten.

- [ ] **[6.1a Reflexion](http://localhost:8000/themen/p6-1a-wellenexperimente.html#reflexion)** ·
  Animation 4 · Reflexion am festen und am losen Ende (`a4-cv`)
  → Der Wandbalken bei s = 8 m zerschneidet den Achsenwert „8.0".

- [ ] **[0.1 Proportionalität](http://localhost:8000/themen/p0-1-vorwissen-mathematik.html#proportional)** ·
  Animation 5 · Indirekte Proportionalität (`a2-cv`)
  → Die getönte Rechteckfläche liegt über den Achsenwerten 20–100, „100" zur Hälfte.

## C · Geringfügig — nur bei genauem Hinsehen

- [ ] **[4.1 Kreisbewegung](http://localhost:8000/themen/p4-1-kinematik.html#kreisbewegung)** ·
  Animation 5 · Gleichförmige Kreisbewegung (`a5-cv`)
  → „r" berührt „a_z".

- [ ] **[6.1 Spektrum](http://localhost:8000/themen/p6-1-wellen.html#spektrum)** ·
  Animation 4 · Elektromagnetisches Spektrum (`a4-cv`)
  → Die gedrehten Bandnamen „Ultraviolett" und „sichtbares Licht" berühren sich;
  „sichtbares Licht" wird zusätzlich von der Markierungslinie gekreuzt.

---

## Prüfmethode

Im Browser wurden `fillText`/`strokeText` samt **Transformationsmatrix** mitgeschrieben —
ohne Matrix-Verfolgung stimmen die Textrahmen gedrehter Achsentitel nicht, was 21
Fehlalarme statt der 6 echten Randläufer ergab. Ausgewertet wurde je Canvas der **erste
Frame** (Animationsschleifen nach wenigen Ticks eingefroren) auf drei objektive Kriterien:
Text über Text, Text aus der Zeichenfläche hinausgelaufen, Text von einer später
gezeichneten Fläche verdeckt.

Nötig war ein **Sichtbarkeitsfilter**: `drawAxesUnits` in `physiklib.js` übermalt die
generischen Achsenbuchstaben „x"/„y" absichtlich mit weissen Flecken und zeichnet die
echten Einheiten neu. Ohne diesen Filter entstehen rund 250 Scheintreffer.

Von 136 Canvas blieben 19 verdächtig; alle 19 wurden als Einzelbild gesichtet und
bestätigt. Keine Kollision wurde allein aus der Messung übernommen.

## Was diese Liste nicht abdeckt

- **Nur 1280 px.** Bei 360 px sind weitere Kollisionen zu erwarten, gerade bei den
  langen Achsentiteln. Eigener Durchgang nötig.
- **Nur die Startposition.** Mitlaufende Marken und Werte können in bewegten Zuständen
  auf andere Elemente treffen.
- **Keine Prüfung Text über Linien/Kurven.** Über den Gitternetzlinien liegt jede
  Beschriftung per Konstruktion; eine Prüfung dagegen hätte fast jede Grafik gemeldet.
  Kollisionen mit Kurven, Pfeilen und Vektoren sind darum nicht erfasst.
