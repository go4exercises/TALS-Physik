# TODO — Beschriftungskonflikte in Canvas-Animationen

Befund vom **30.07.2026**, Korrekturen in zwei Durchgängen am **30.07.2026**. Geprüft
wurden **alle 136 Canvas auf den 14 Themenseiten** in der **Startposition** bei
**1280 px** (Gegenmessung bei 1440 und 1920 px).

**Stand: alle 19 Befunde behoben.** Der erste Durchgang hat ausschliesslich Text
verschoben (14 Fälle). Im zweiten Durchgang wurden nach Rückmeldung auch die fünf Fälle
gelöst, in denen ein anderes Grafikelement die Beschriftung deckte — dort war eine
Änderung am Element unvermeidlich —, und einige Stellen nachgebessert, an denen
Beschriftungen auf Linien oder Kurven lagen (Abschnitt E).

Die Links öffnen die Stelle direkt. Voraussetzung ist der lokale Server:

```bash
python3 -m http.server 8000
```

---

## A · Korrigiert — Beschriftung lag auf anderer Beschriftung

- [x] **[4.1 Herleitung](http://localhost:8000/themen/p4-1-kinematik.html#theorie)** ·
  Herleitungsgrafik zum Trapez (`herl-cv`) — „Fläche = s − s₀" lag zu 87 % auf „v₀ · t".
  → „v₀ · t" steht jetzt im linken Drittel seines Rechtecks statt in der Mitte.

- [x] **[6.2 Ohmsches Gesetz](http://localhost:8000/themen/p6-2-elektrizitaet.html#ohm)** ·
  Animation 1 · U-I-Kennlinie (`a1-cv`) — „100 Ω (Referenz)" lag auf „(60 mA | 6.0 V)".
  → Die Referenz-Beschriftung sitzt 2.8 V höher an derselben Geraden.

- [x] **[5.1 Skalen](http://localhost:8000/themen/p5-1-temperatur.html#skalen)** ·
  Animation 3 · Thermometer (`a3-cv`) — „°C" und „K" sassen auf „150" und „423".
  → Beide Skalenköpfe stehen 14 px höher, über den obersten Werten.

- [x] **[0.1 Je–desto](http://localhost:8000/themen/p0-1-vorwissen-mathematik.html#jedesto)** ·
  Animation 1 · Glacé und Sonnenbrand (`b6-korr-cv`) — Achsentitel „Glacé [Portionen]"
  lag auf dem Wert „340".
  → Der Titel steht eine Zeile höher (neuer optionaler Versatz-Parameter in
  `drawAxesUnits`, nur diese Grafik nutzt ihn).

- [x] **[4.1 Einstieg](http://localhost:8000/themen/p4-1-kinematik.html#einstieg)** ·
  Einstiegs-Animation · Zugfahrt (`a0-cv`) — Marke „t₁" lag auf dem Wert „160".
  → Das Marker-Label kippt auf die Innenseite der Linie, sobald es links in die
  Wertespalte geriete, und steht dort eine Zeile tiefer als der Achsentitel.

- [x] **[4.4 Resultierende](http://localhost:8000/themen/p4-4-statik.html#resultierende)** ·
  Animation 2 · Vektoraddition (`a2-cv`) — „F2" lag auf dem Wert „40".
  → `drawVector` setzt Pfeil-Labels bei **steilen** Pfeilen seitlich statt darüber;
  flache Pfeile bleiben unverändert.

- [x] **[5.2 Treibhauseffekt](http://localhost:8000/themen/p5-2-waerme.html#treibhaus)** ·
  Treibhausgas-Vergleich (`thg-ch4`) — gedrehter Achsentitel „ppb" kreuzte „1000".
  → Die Einheit steht waagrecht unter dem Achsenfuss; in der Wertespalte war kein Platz.

- [x] **[6.2 Gefahren](http://localhost:8000/themen/p6-2-elektrizitaet.html#gefahren)** ·
  Animation 6 · Stromstärke-Zeit-Diagramm (`a6-cv`) — „Einwirkzeit [ms]" kreuzte „1000"
  und „10000".
  → Der gedrehte Titel steht 20 px weiter links, ausserhalb der Wertespalte.

- [x] **[4.4 Drehmoment](http://localhost:8000/themen/p4-4-statik.html#drehmoment)** ·
  Animation 4 · Drehmoment und Hebelarm (`a4-cv`) — „r = 0.26 m" berührte „l = 0.30 m".
  → „l = 0.30 m" steht 16 px tiefer.

- [x] **[4.5 Auftrieb](http://localhost:8000/themen/p4-5-hydrostatik.html#auftrieb)** ·
  Animation 4 · Auftriebskraft (`a4-cv-quader`) — „F_A = 5.89 N" stiess an „0.98 N".
  → „F_A = …" steht 14 px höher.

- [x] **[4.1 Kreisbewegung](http://localhost:8000/themen/p4-1-kinematik.html#kreisbewegung)** ·
  Animation 5 · Gleichförmige Kreisbewegung (`a5-cv`) — „r" berührte „a_z".
  → „r" sitzt auf 35 % des Radius und quer zur Radiusrichtung versetzt; der a_z-Pfeil
  liegt auf dem Radius selbst.

- [x] **[6.1 Spektrum](http://localhost:8000/themen/p6-1-wellen.html#spektrum)** ·
  Animation 4 · Elektromagnetisches Spektrum (`a4-cv`) — „sichtbares Licht" stiess an
  „Ultraviolett".
  → Das Band trägt einen eigenen Label-Versatz (12 px nach rechts); die übrigen
  Bandnamen bleiben, wo sie waren.

## B · Korrigiert — Beschriftung lief aus der Zeichenfläche

- [x] **[4.5 Pascal](http://localhost:8000/themen/p4-5-hydrostatik.html#pascal)** ·
  Animation 3 · Hydraulische Presse (`a3-cv`) — „s₁=20 cm" begann 6 px links ausserhalb.
  → Die rechtsbündige Position wird jetzt auf die Textbreite begrenzt.

- [x] **[4.3 Kinetische Energie](http://localhost:8000/themen/p4-3-energie.html#kinetisch)** ·
  Animation 2 · Fahrzeug in Bewegung (`a2-cv-szene`) — die Massstabswerte „0 m" … „60 m"
  ragten unten heraus.
  → Alle vier stehen 3 px höher und liegen vollständig in der Fläche.

## D · Behoben — anderes Grafikelement deckte die Beschriftung

Hier war eine Textverschiebung nicht möglich: die Werte kommen aus `drawGrid` und gehören
an ihre Teilstriche. Gelöst über die Ursache.

- [x] **[4.5 Schweredruck](http://localhost:8000/themen/p4-5-hydrostatik.html#schweredruck)** ·
  Animation 1 · Flüssigkeitssäule (`a1-cv-saeule`) — Manometerkasten über „0 m", Zeile
  „(0.29 bar)" breiter als der Kasten.
  → Kasten von 65 auf 84 px verbreitert und 26 px weiter rechts; die Verbindungslinie
  folgt. Alle drei Zeilen stehen jetzt im Kasten, die Tiefenskala bleibt frei.

- [x] **[4.3 Arbeit](http://localhost:8000/themen/p4-3-energie.html#arbeit)** ·
  Animation 1 · Arbeit als Fläche (`a1-cv-diag`) — „2.0" von der Flächenkante zerschnitten.
  → Ursache war `drawGrid`: bleiben unter der Achse keine 18 px, setzt es die x-Werte
  **über** die Achse — mitten in die Fläche. Untere Bereichsgrenze von −5 N auf −10 % von
  F_max gesetzt; die Werte stehen jetzt unter der Achse.

- [x] **[0.1 Proportionalität](http://localhost:8000/themen/p0-1-vorwissen-mathematik.html#proportional)** ·
  Animation 5 · Indirekte Proportionalität (`a2-cv`) — Tönung über den Werten 20–100.
  → Gleiche Ursache, gleiche Lösung (yMin von −5 % auf −10 % von yMax).

- [x] **[6.1a Saite](http://localhost:8000/themen/p6-1a-wellenexperimente.html#saite)** ·
  Animation 7 · Eigenschwingungen (`a7-cv`) — Einspannbalken über „2", „4" und „2.0".
  → Klemmen sitzen jetzt mittig auf den Endpunkten statt daneben (damit sind die y-Werte
  frei), und der letzte x-Wert wird nach den Klemmen noch einmal gezeichnet.

- [x] **[6.1a Reflexion](http://localhost:8000/themen/p6-1a-wellenexperimente.html#reflexion)** ·
  Animation 4 · Reflexion am festen Ende (`a4-cv`) — Wandbalken über „8.0".
  → Der Wert wird nach der Wand wiederholt; die Wand selbst bleibt, wo sie hingehört.

## E · Zweiter Durchgang — Beschriftungen auf Linien, Symbole, Bedienung

Diese Punkte kamen aus der Sichtprüfung am Bildschirm; die Messung erfasst sie nicht
(Text über Linien und Kurven wird nicht geprüft).

- [x] **[6.2 Ohmsches Gesetz](http://localhost:8000/themen/p6-2-elektrizitaet.html#ohm)** ·
  `a1-cv` — die Referenzgerade schnitt mitten durch „100 Ω (Referenz)".
  → Beschriftung von 70 mA auf 107 mA verschoben, also rechts neben die Gerade.

- [x] **[4.1 Einstieg](http://localhost:8000/themen/p4-1-kinematik.html#einstieg)** ·
  `a0-cv` — „v̄ = 120.0 km/h" und „gleiche Fläche wie die Kurve" lagen auf der Bremsflanke.
  → Beide stehen jetzt bei 30 % des Intervalls, wo die Kurve waagrecht läuft.

- [x] **[4.4 Drehmoment](http://localhost:8000/themen/p4-4-statik.html#drehmoment)** ·
  `a4-cv` — Winkelbogen und α lagen auf der falschen Seite, auf dem Hebel.
  → Der Bogen spannt jetzt von −α bis 0, also zwischen Hebelrichtung und Kraft; α sitzt
  aussen auf der Winkelhalbierenden.

- [x] **[4.5 Pascal](http://localhost:8000/themen/p4-5-hydrostatik.html#pascal)** ·
  `a3-cv` — Rohrzeichnung: eine Wand lief quer über die Rohrmündungen, die beiden
  Steigrohre wirkten vom Kanal getrennt.
  → Der Kanaldeckel liegt nur noch **zwischen** den Rohren, die Aussenwände laufen bis
  auf den Boden durch. Das Gefäss liest sich jetzt als ein zusammenhängendes U-Rohr.

- [x] **[4.1 Kreisbewegung](http://localhost:8000/themen/p4-1-kinematik.html#kreisbewegung)** ·
  `a5-cv` — bei kleinem r und kleinem ω liegen r und a_z zwangsläufig nah beieinander.
  → Neuer Knopf „Radius \(r\) zeigen" (`.typ-btn`, standardmässig an): blendet Radiuslinie
  und Beschriftung zusammen aus.

- [x] **[6.1 Spektrum](http://localhost:8000/themen/p6-1-wellen.html#spektrum)** ·
  `a4-cv` — „sichtbares Licht" war nicht mehr lesbar.
  → Alle gedrehten Bandnamen stehen 12 px tiefer, vollständig unter dem Balken; der
  Zeiger unter dem Balken ist von 26 auf 14 px gekürzt, damit er nicht durch die Namen
  läuft.

- [x] **[4.5 Pascal](http://localhost:8000/themen/p4-5-hydrostatik.html#pascal)** ·
  `a3-cv` — „s₁=20 cm" berührte das dünne Massband; links vom kleinen Kolben ist für
  eine Zeile kein Platz (der Text ist 62 px breit, der Rand 53 px).
  → Zweizeilig: „s₁" über „20 cm", rechtsbündig links vom Massband.

- [x] **[4.4 Drehmoment](http://localhost:8000/themen/p4-4-statik.html#drehmoment)** ·
  `a4-cv` — die gestrichelte Wirkungslinie kreuzte „l = 0.30 m".
  → Das Label bleibt rechts von der Linie: die x-Position der Linie wird auf der
  Label-Höhe aus dem Winkel berechnet, bei flachen Winkeln steht es wieder mittig.

### Ausserdem beobachtet, ohne sichtbaren Konflikt

Auf **[6.2 Gefahren](http://localhost:8000/themen/p6-2-elektrizitaet.html#gefahren)**
(`a6-cv`) wird die Zonennummer „1" 30 px links **ausserhalb** der Zeichenfläche gezeichnet:
Zone 1 liegt unter 0.5 mA und damit vor dem Beginn der Achse. Die Nummer ist unsichtbar
und kollidiert mit nichts. Sie in die Fläche zu holen würde sie neben Zone 2 setzen und
damit falsch beschriften — darum bleibt sie unangetastet.

---

## Prüfmethode

Im Browser werden `fillText`/`strokeText` samt **Transformationsmatrix** mitgeschrieben —
ohne Matrix-Verfolgung stimmen die Textrahmen gedrehter Achsentitel nicht (21 Fehlalarme
statt 6 echter Randläufer). Ausgewertet wird je Canvas der **erste Frame**
(Animationsschleifen nach wenigen Ticks eingefroren) auf drei objektive Kriterien: Text
über Text, Text aus der Zeichenfläche hinausgelaufen, Text von einer später gezeichneten
Fläche verdeckt. Nötig ist ein **Sichtbarkeitsfilter**: `drawAxesUnits` übermalt die
generischen Achsenbuchstaben „x"/„y" absichtlich und zeichnet neu — ohne Filter entstehen
rund 250 Scheintreffer.

**Ergebnis:** 29 Befunde in 19 Canvas → **erster Durchgang 9 Befunde**, nach dem zweiten
Durchgang **2 Befunde**: der doppelt gezeichnete Wert „8.0" auf 6.1a (die verdeckte erste
Ausgabe wird gezählt, die sichtbare zweite liegt darüber) und die unsichtbare Zonennummer
auf 6.2. Jede Korrektur wurde einzeln am Bild kontrolliert; drei Rückschläge sind dabei
aufgefallen und behoben worden (ein Pfeil-Label auf 4.1, das durch die neue seitliche
Platzierung auf ein anderes rutschte; ein weisser Deckfleck, der nach dem Verschieben des
Achsentitels den letzten Wert verdeckte; und der Spektrum-Zeiger, der nach dem
Tieferstellen der Bandnamen durch sie hindurchlief).

## Was diese Liste nicht abdeckt

- **Nur 1280 px.** Bei 360 px sind weitere Kollisionen zu erwarten, gerade bei den langen
  Achsentiteln. Eigener Durchgang nötig.
- **Nur die Startposition.** Mitlaufende Marken und Werte können in bewegten Zuständen auf
  andere Elemente treffen. Beispiel: die Referenz-Beschriftung auf 6.2 `a1-cv` liegt
  zwischen etwa 8.6 V und 9.7 V wieder in der Nähe des Punkt-Labels.
- **Keine Prüfung Text über Linien/Kurven.** Über den Gitternetzlinien liegt jede
  Beschriftung per Konstruktion; Kollisionen mit Kurven, Pfeilen und Vektoren sind nicht
  erfasst.
