# TODO — Didaktisches Review aller Canvas-Animationen

Stand: 25.07.2026. Grundlage: systematische Durchsicht aller 16 Themenseiten
(~130 Canvas-Elemente) samt umgebendem HTML, Bedienelementen, Hinweis-Popups und
Zeichencode. Bewertungskriterien: Verständlichkeit, Nachvollziehbarkeit der
Kausalzusammenhänge, Explorations-Anreiz, Parameterwahl, Struktur (Streichung /
Zusammenlegung / Ergänzung).

Prioritäten: **[HOCH]** = Bild widerspricht dem eigenen Lehrtext, ist fachlich
falsch oder der Kern-Lerneffekt ist unsichtbar. **[MITTEL]** = deutlicher
didaktischer Gewinn mit vertretbarem Aufwand. **[NIEDRIG]** = Feinschliff.

Positiv vorweg: Das Muster «Szene + Diagramm + formel-live + Live-Box» trägt
durchgehend; p6-1a ist auf dem höchsten Niveau (Grid + Achsen, Tempo/Reset,
Momentbild + Mitschrieb, dynamische Labels) und taugt als hausinterner Standard.
Streichungen sind fast nirgends nötig — die Probleme sind reparierbar.

---

> **Stand 28.07.2026 — alle [HOCH]-Punkte sind erledigt.**
> Abgearbeitet sind: Block B (fachliche Fehler), die Querschnittspunkte Q1 und Q2,
> sämtliche [HOCH]-Einzelpunkte aller 16 Themenseiten sowie ein Stilcheck über
> alle Seiten. Offen sind noch 45 Punkte: Q3–Q6, die [MITTEL]- und
> [NIEDRIG]-Einträge je Seite und Abschnitt D (neue Animationen).

## A. Querschnittsbefunde (mehrere Seiten, gemeinsame Ursache)

- [x] **[HOCH] Q1 — Mitwachsende/adaptive Achsen neutralisieren den Lerneffekt.**
  Die Achse skaliert mit dem Parameter mit, dadurch sieht der Graph bei jeder
  Einstellung gleich aus; genau der versprochene Vergleich (Steigung, wandernder
  Punkt) wird unsichtbar. Fix: feste Achsen oder feste Referenzkurve.
  Betroffen: ~~p0-4 a1 (Feder), p0-4 a2 (s = v·t), p0-4 a4 (Einholproblem),
  p4-5 a1-cv-ph (p(h) je Dichte), p5-2 a1 (Wärmebedarf-Balken), p6-1 a3
  (Schall-Balken), p6-2 a1 (U-I-Kennlinie), p0-0 a6 / p0-2 a1 (Dichte-Balken)~~ ✓
  — **vollständig erledigt am 28.07.2026.**

  Die drei letzten Fälle brauchten je eine eigene Antwort, weil die Wertebereiche
  sehr unterschiedlich weit sind:
  - **p4-5 a1-ph** (Dichte 500 … 14 000 kg/m³, Spanne 28×): feste p-Achse
    0 … 1400 kPa plus eine dauerhaft eingezeichnete Wasser-Referenzgerade.
    Damit leichte Flüssigkeiten trotz flacher Geraden unterscheidbar bleiben,
    steht die Steigung zusätzlich beziffert im Bild (ρ·g in kPa/m) — Öl gegen
    Meerwasser ist optisch sonst nicht auflösbar.
  - **p6-2 a1** (R 10 … 500 Ω, Spanne 50×): feste I-Achse 0 … 1200 mA plus
    Referenzkennlinie 100 Ω. Die Aussage «Steigung = R» wird damit erst sichtbar;
    vorher sprang xMax in Stufen mit und jede Kennlinie sah gleich steil aus.
  - **p6-1 a3** (λ von 0.17 m bis 103 m, Spanne 608×): hier war eine lineare
    feste Achse unmöglich. Die auf die längste Wellenlänge normierten Balken sind
    darum durch eine **feste logarithmische λ-Achse** (0.1 … 200 m) mit vier
    Medienmarken ersetzt. Eine Frequenzänderung verschiebt jetzt alle vier Marken
    gemeinsam — der Regler wirkt sichtbar, während die Abstände der Medien
    (feste c-Verhältnisse) korrekt konstant bleiben.
- [x] **[HOCH] Q2 — Überhöhungsfaktoren nicht am Reglermaximum kalibriert (Sättigung).**
  ~~p5-3 a1 (Faktor 4000 → ≈260), p5-3 a2 (120 → ≈4.5), p5-3 a4 (120 → ≈46)~~ ✓:
  Die Grafik klemmt über weite Bereiche am Anschlag, Materialwechsel und
  ΔT-Regler ändern das Bild nicht. Ein gemeinsamer, kleiner Fix.
  *Erledigt 26.07.2026 — die Liste betraf nur p5-3, alle drei Faktoren neu kalibriert.*
- [ ] **[MITTEL] Q3 — Pfeillängen mit Sockel/Cap oder fix statt proportional.**
  Wo der Grössenvergleich der Pfeile die Botschaft ist, muss streng proportional
  skaliert werden. ~~Betroffen: p4-1 a5, p4-2 a2, p4-2 a6, p4-5 a5.~~
  ✓ **vollständig erledigt am 28.07.2026.** Vorbild: p4-2 a5.
- [ ] **[MITTEL] Q4 — «Worauf achten»-Aufträge, die das Widget nicht ausführen kann.**
  Entweder Feature nachrüsten (bevorzugt, siehe Einzelpunkte) oder Hinweistext
  anpassen: ~~p4-1 a3 (Fallwege vergleichen ohne Zeitlupe/Spur)~~ ✓,
  ~~p4-2 a3 (Bezugssystem wechseln ohne Umschalter)~~ ✓,
  ~~p4-2 a4 («losruckt» ohne Bewegung)~~ ✓,
  p6-1a a2 (zwei Teilchen vergleichen, nur eines markierbar), ~~p5-2 a4
  (Vakuum-Frage ohne Vakuum)~~ ✓, ~~p0-2 a1 (Balken reagieren nicht)~~ ✓.
- [ ] **[MITTEL] Q5 — Vergleiche ohne Gedächtnis.** Serielle Vergleiche (erst A
  einstellen, dann B, Wert merken) durch Geister-/Referenzdarstellungen ersetzen:
  ~~p4-2 a2 («letzter Lauf»-Zeile)~~ ✓, ~~p4-3 a2-diag (Geister-Punkt bei 2v)~~ ✓,
  ~~p0-2 a2 (Referenzmarken Erde/Mond/Mars)~~ ✓, ~~p4-1 a4 («Bahn festhalten»)~~ ✓,
  ~~p5-3 a1/a2
  (Referenzstab/-gefäss Eisen)~~ ✓.
- [ ] **[MITTEL] Q6 — Tempo-Regler + Reset (p6-1a-Standard) nachrüsten** bei den
  animierten Widgets ohne: ~~p4-1 a3 (freier Fall)~~ ✓, p6-1 ein-cv, a1, a2, a5.
- [x] **Q7 — Stilcheck über alle 16 Themenseiten** (28.07.2026). Geprüft wurde
  nicht der Quelltext, sondern der **gerenderte Zustand**: Playwright lädt jede
  Seite, scrollt alle Widgets ins Sichtfeld und liest 45 `formel-live`-Blöcke,
  87 Live-Boxen und 1117 Canvas-Beschriftungen aus (`fillText` wird dafür
  mitgeschnitten). Der Quelltext-Scan hatte zu wenig gefunden, weil fast alle
  `.fl-eq` erst von JS gefüllt werden.

  Befunde und Korrekturen — 13 Formel-Blöcke auf 8 Seiten:
  - **Regel 3+4** (Formel vor Werten, Werte mit Einheit): p4-1 a1, p4-2 a1/a5,
    p4-3 a1/a2/a4, p4-4 a1/a4/a5, p4-5 a1, p6-1 a3, p6-2 a1/a2/a3/a4/a5 haben
    jetzt durchgehend eine symbolische Formelzeile und Werte mit Einheit
    (`p_S = 1000 kg/m³ · 9.81 m/s² · 3.0 m`, `E = ½ · 1200 kg · (14 m/s)²`).
  - **Regel 2** (je Gleichung eine Zeile): p4-4 a1 und a5 sowie p6-2 a3 und a5
    quetschten zwei Gleichungen mit «·» in eine Zeile — jetzt je zwei Paare aus
    Formel- und Wertzeile. Achtung beim Nachbauen: zwei Formeln mit Leerraum in
    *eine* `.fl-eq` zu setzen funktioniert nicht, HTML kollabiert die Abstände.
  - **Regel 2 in Canvas-Texten**: p5-2 a7 («Atmosphäre · CO₂ 430 ppm») und
    p5-3 a5 («V = 3.0 L · T = 293 K») ersetzt.
  - **Regel 1** (Spaltenabstand): alle 87 Live-Boxen korrekt — die gestaffelte
    `:has()`-Regel in `style.css` greift überall, kein Handlungsbedarf.
  - **Regel 5/6**: keine Befunde.

  Zwei bewusst stehengelassene Fehlalarme des Prüfers: `5·10⁰ m = 5 m` (p0-3 a1)
  ist eine Wertdarstellung ohne einzusetzende Formel, und bei
  `Q_warm = COP · E_el = 3.5 · 1.0 kWh` ist der COP dimensionslos.

  Alle geänderten Zahlenwerte in Python nachgerechnet, Render-Check bei 1280 px
  und 360 px.

---

## B. Fachliche Fehler (vor allem anderen beheben)

*Vollständig abgearbeitet am 28.07.2026 — dabei ein achter Fehler entdeckt und
mitbehoben (invertierte Dichtefärbung in p6-1 a2).*

- [x] **[HOCH] p6-2 ein-cv:** Elektronen laufen aussen von + nach −; die
  Erkenntnis-Box lehrt das Gegenteil. Umlaufrichtung umkehren, Pfeile
  «Elektronen» vs. «technische Stromrichtung» beschriften.
  *Erledigt 28.07.2026: Der Umlauf zählte im Uhrzeigersinn, damit ging es vom
  Minuspol direkt aufwärts zum Pluspol — durch die Batterie statt durch den
  äusseren Kreis. Jetzt Gegenuhrzeigersinn; zusätzlich zwei benannte Pfeile
  (blau «Elektronen: – → +», bernstein «technische Stromrichtung I»).*
- [x] **[HOCH] p6-1 a2:** Labels «Verdichtung»/«Verdünnung» stehen ortsfest,
  das Dichtemuster wandert — Beschriftung meist an der falschen Stelle.
  Labelposition aus der Phase berechnen (Lösung existiert in p6-1a, Z. 1094 ff.).
  *Erledigt 28.07.2026: Beide Labels sitzen jetzt auf dem berechneten
  Dichte-Extremum und tragen eine Führungslinie zur Teilchenreihe.*
- [x] **[HOCH] p6-1 a2 — zweiter, schwererer Fehler (beim Fix entdeckt):** Die
  Einfärbung war invertiert. Der Code setzte `dens = +cos(k·x − ph)` und färbte
  `dens > 0` rot als «Verdichtung». Die Teilchendichte ist aber
  \(\propto -\partial(\text{Auslenkung})/\partial x = -A k \cos(\dots)\), also
  maximal beim **negativen** Cosinus. Nachgerechnet: an der bisher rot gefärbten
  Stelle war die lokale Dichte 5- bis 11-mal *kleiner* als an der blauen. Rot
  markierte damit durchgehend die verdünnten Zonen. Vorzeichen korrigiert und
  über fünf Phasenlagen nachgerechnet (28.07.2026).
- [x] **[HOCH] p6-1 a1 (c = λ·f):** λ und f unabhängig einstellbar, c abgeleitet —
  erzeugt das Fehlkonzept «Medium passt seine Geschwindigkeit an», im Widerspruch
  zum eigenen Theorieblock und zu p6-1a A2. Kausalität umdrehen (Regler f und c,
  λ = c/f abgeleitet); zudem Gitter + s-Achse ergänzen.
  *Erledigt 28.07.2026: Regler sind jetzt \(c\) (1 … 6 m/s, «Medium») und \(f\)
  (1 … 4 Hz, «Sender»); \(\lambda = c/f\) steht als abgeleitete Grösse in der
  Live-Box, dazu die Probe \(\lambda \cdot f\). Feste s-Achse 0 … 6 m mit
  Meter-Gitter (Q1), λ-Klammer mit Endmarken, Laufrichtungspfeil mit \(c\).
  Beide Hinweisboxen und der Einleitungstext auf die neue Kausalität umgeschrieben.*
- [x] **[HOCH] p5-2 a6 (Treibhaus):** Bei 280 ppm wird kein einziger IR-Strahl
  zurückgeworfen — der natürliche Treibhauseffekt (Mini-Check!) existiert im
  Modell nicht. Basis-Rückhaltung > 0 bei 280 ppm, Regler-Effekt als «zusätzlich»
  beschriften; Rückstrahlung als Re-Emission statt Spiegelreflexion zeichnen [MITTEL].
  *Erledigt 26.07.2026 (jetzt Animation 7): 7 von 12 Strahlen natürlich, bis zu
  3 zusätzlich; Absorption + Re-Emission statt Spiegelung.*
- [x] **[HOCH] p5-1 a1 (Gasteilchen):** Alle Teilchen haben exakt dasselbe Tempo —
  der direkt folgende Missverständnis-Block lehrt «Temperatur ist nur der
  Mittelwert». Feste Geschwindigkeitsstreuung (Faktor ≈0.5–1.6) einbauen.
  *Erledigt 26.07.2026: Faktoren 0.52 … 1.60, Mittelwert exakt 1.*
- [x] **[HOCH] p0-3 a1 (Präfix-Leiter):** Im Zeit-Modus erscheinen die Sprossen
  «hs», «ks», «Ms» — widerspricht dem eigenen Lehrtext («oberhalb der Sekunde
  nicht dezimal»). Obere Sprossen ausblenden oder durch min/h ersetzen.
  *Erledigt 27.07.2026: durchgestrichen ausgewiesen, min und h ergänzt.*
- [x] **[HOCH] p6-2 a4 (Parallelschaltung):** Der rechte Rahmen ist topologisch
  ein Kurzschluss-Zweig ohne Strompunkte. Leitung beim zweiten Zweig enden lassen.
  *Erledigt 28.07.2026: Sammelschienen enden bei R₂. Zusätzlich führt der Trunk
  zwischen den Zweigen jetzt sichtbar nur noch I₂ (Punktdichte proportional zum
  Strom, Farbe wechselt an der Verzweigung) — die Aufteilung wird damit ablesbar.*
- [x] **[MITTEL] p6-2 a6:** Zonengrenzen sind vereinfachte Eigenformeln, aber mit
  «IEC» beschriftet — «vereinfacht nach IEC 60479» deklarieren oder verifizieren.
  *Erledigt 28.07.2026: als «vereinfacht nach IEC 60479-1» deklariert — im
  Bildtitel, im Fliesstext und als Kommentar über den beiden Näherungsformeln.
  Nicht verifiziert: die Norm liegt nicht vor, und Grenzkurven werden nicht
  geraten (CLAUDE.md, Verifikations-Standard).*
- [x] **[MITTEL] p4-3 a4:** Text sagt «Dehnung», gezeichnet ist eine Stauchung —
  Bild oder Wortwahl («Auslenkung») vereinheitlichen.
  *Erledigt 28.07.2026: das Bild folgt dem Text, weil Regler, Mini-Check und
  Transferaufgabe («gespanntes Gummiband») durchgehend von Dehnung sprechen.
  Die Feder wird jetzt länger, dazu eine gestrichelte Ruhelage-Marke und der
  Massband-Pfeil von der Ruhelage zum Block.*
- [x] **[MITTEL] p4-5 a2:** Titel «Drei verbundene Gefässe», gezeichnet sind
  getrennte Gefässe — Titel korrigieren oder Verbindungsrohr einzeichnen.
  *Erledigt 28.07.2026: Titel korrigiert. Ein Verbindungsrohr wäre der falsche
  Weg — das Paradoxon lebt davon, dass drei **getrennte** Gefässe bei gleicher
  Füllhöhe denselben Bodendruck zeigen. Überschrift, Fliesstext und Hinweisboxen
  sagten das bereits richtig, nur der Bildtitel nicht.*

---

## C. Todo je Seite

### p0-0 Vorwissen kompakt
*Alle Punkte umgesetzt am 27.07.2026. Achtung: Animation 2 (Dreisatz) ist in
Animation 1 aufgegangen, die folgenden sind um eins nach vorne gerückt —
alt a3…a8 entsprechen neu a2…a7.*
- [x] [HOCH] a6 (neu a5) Dichte-Würfel: feste, beschriftete Skala statt
  Normierung aufs Maximum. → Verglichen wird jetzt die **Masse von 1 Liter**
  auf einer dauerhaft festen Skala 0 … 12 kg. Eine feste *Massen*skala ist
  nachweislich unmöglich: Blei ist 567-mal dichter als Styropor, dazu kommt die
  dritte Potenz der Kantenlänge — selbst ohne Schieber bliebe Styropor bei
  0.18 % der Skala. Die Masse von 1 Liter hängt dagegen nicht von der
  Würfelgrösse ab, darum muss die Skala nie angepasst werden. Wasserlinie bei
  1.00 kg als Grenze schwimmt/sinkt; die echte Würfelmasse steht als Fusszeile
  und in der Live-Box, dort wirkt der Kantenregler weiterhin.
  **Offen: p0-2 a1 trägt denselben duplizierten Code und ist noch nicht angepasst.**
- [x] [HOCH] a8 (neu a7) Teilchenmodell: Autostart beim Sichtbarwerden per
  IntersectionObserver; wer selbst pausiert, wird beim Zurückscrollen nicht
  überfahren (`userPaused`).
  **Offen: p0-2 a6 trägt denselben duplizierten Code.**
- [x] [HOCH] a2 Dreisatz: mit a1 zusammengelegt — a1 hat jetzt vier Szenarien
  (Taxi ohne/mit Grundgebühr, Äpfel lose/in Harassen) und macht sichtbar, wann
  der Dreisatz gilt und wann nicht.
- [x] [MITTEL] a1: zweiter Regler für den Preis (Steigung als Ursache erlebbar),
  dazu feste Kostenachse, damit der Preis die Steigung sichtbar verändert.
- [x] [MITTEL] a3 (neu a2) Zylinder: Volumen-Balken mit fester Literskala
  (0 … 6300 L) neben der Zeichnung; zusätzlich zwei Diagramme V(h) und V(r),
  die linear bzw. quadratisch zeigen.
- [x] [MITTEL] a4 (neu a3) Tempo-Doppelskala: formel-live mit beiden
  Umrechnungsrichtungen; dazu zwei gekoppelte Regler für km/h und m/s.
- [x] [MITTEL] a7 (neu a6) Treppenlauf: Masse-Regler (40 … 120 kg) und
  Arbeitsbalken neben dem Leistungsbalken, beide mit fester Skala (24 kJ bzw.
  2400 W). Der Kontrast ist damit prüfbar: bei 40 kg und 120 s bleibt W bei
  7.8 kJ, während P auf 65 W fällt. Dazu Aufstiegshöhe einstellbar und ein
  Play-Knopf, der den Aufstieg in der eingestellten Laufzeit abspielt.
  Ergänzt 27.07.2026: Reset-Knopf; das Treppenhaus ist fest 20 m hoch und die
  Person steigt nur bis zur eingestellten Höhe (Zielmarke im Bild); beim
  Abspielen wächst der Arbeitsbalken mit W(t) = m·g·h(t) auf die gestrichelte
  E_pot-Marke zu, während der Leistungsbalken konstant bleibt; die Masse steuert
  Strichstärke und Beschriftung der Figur.
- [x] [NIEDRIG] a5 (neu a4) Faustregel-Diagramm: Abweichung als Klammer zwischen
  den beiden Kurven, mit Betrag und Prozentwert (bei 40 m: +0.063 bar, +1.28 %).

### p0-1 Vorwissen Mathematik
- [x] [HOCH] a1-sz Tauchszene: lastende Wassersäule über dem Taucher eingefärbt
  und beschriftet (26.07.2026, beim Umbau von a1 auf zwei Szenarien).
- [x] [HOCH] a2 Hyperbel: konstantes Produkt als halbtransparentes Rechteck unter
  dem Kurvenpunkt. Beim neuen Standard-Beispiel Butterbrot ist die Rechteckfläche
  buchstäblich die Butter (10 cm³), beim Tempo die Strecke (120 km).
- [x] [HOCH] a6 Formel-Waage: komplett neu aufgebaut (27.07.2026). Jede Zeile
  trägt jetzt die Äquivalenzumformung, die als Nächstes angesetzt wird; dazwischen
  liegt ein eigener Zwischenschritt, in dem dasselbe violette Kärtchen auf beiden
  Schalen liegt (Operation angesetzt, noch nicht zusammengefasst). Knopf
  «⚠ nur eine Seite umformen» legt das Kärtchen nur rechts hin — die Waage kippt
  um 7°, das Gleichheitszeichen wird zum «≠», Text und Historie werden rot.
  Schritthistorie doppelt: als `.fl-eq`-Zeilen in der Formel-Box und als Kasten
  unter der Waage, jede Zeile mit «‖ beide Seiten : (π · h)» rechts.
- [x] [MITTEL] a4 Bogenmass: Knöpfe «genau 1 rad (57.3°)», «π/2 = 90°»,
  «π = 180°», «2π = 360°» plus Vergleichsband unten (Bogen s über Radius r);
  bei φ = 1 rad erscheint «s = r → φ = 1 rad» (27.07.2026).
- [x] [MITTEL] a5 Zehnerpotenz-Leiter: Leiter auf zwei Zeilen (10⁻⁶…10² und
  10²…10¹⁰), damit der Sliderbereich bis 9.9·10⁹ vollständig abgedeckt ist;
  Vergleichsobjekte auf die passende Zeile verteilt (27.07.2026).
- [x] [MITTEL] a1-ph: Steigungsdreieck an der Geraden, in beiden Szenarien.
- [x] [NIEDRIG] a3 Zylindertank: Volumen-Balken auf fester Skala 0…6300 L
  ergänzt (27.07.2026).
- [x] Stilcheck 27.07.2026: a3 und a4 haben jetzt eine symbolische Formelzeile
  vor der Zahlengleichung, a3 setzt die Werte mit Einheiten ein
  (`V = π · (0.50 m)² · 1.00 m`); «Fr.» durchgehend auf «CHF» vereinheitlicht;
  in a5 der Punkt als Achsentrenner durch «—» ersetzt.

### p0-2 Vorwissen Physik
- [x] [HOCH] a1 Dichte-Würfel + a6 Teilchenmodell: identische Fixes wie p0-0
  (feste Skala, Autostart) — beide portiert am 27.07.2026. a1 vergleicht jetzt
  die Masse von 1 Liter auf fester Skala 0 … 12 kg (Begründung siehe p0-0 a5),
  a6 startet beim Sichtbarwerden und respektiert eine eigene Pause.
- [x] [HOCH] a3 Hubarbeit: W als Balken mit fester Skala 0 … 1500 Nm; Kistengrösse
  von der Masse entkoppelt; formel-live ergänzt. Zusätzlich Einheit Nm statt J
  und Play/Reset: die Arbeit summiert sich beim Heben auf und wird oben als
  Lageenergie ausgewiesen.
- [x] [MITTEL] a2 Federwaage: alle drei Orte dauerhaft an der Skala, der aktive
  durchgezogen, die anderen gestrichelt. Bei 10 kg stehen 98.1 N (Erde),
  37.1 N (Mars) und 16.2 N (Mond) nebeneinander — der Sechstel-Vergleich
  (9.81 / 1.62 = 6.06) ist damit ablesbar.
- [x] [MITTEL] a4 Rutsche: Play- und Reset-Knopf. Die Position folgt dem
  Energiesatz (v = √(2g(h₀−h))), das Kind wird unterwegs sichtbar schneller —
  ohne dass ½mv² vorweggenommen wird.
- [x] [MITTEL] a5 Treppenlauf: wie p0-0 a6 portiert — Masse- und Höhenregler,
  Arbeits- und Leistungsbalken mit fester Skala, festes Treppenhaus von 20 m,
  Play und Reset, aufsummierende Arbeit gegen die E_pot-Marke.

- [x] Stilcheck 27.07.2026: keine Befunde — Formelzeilen benennen die Formel vor
  den Werten, Werte tragen Einheiten, «·» steht überall für Multiplikation, alle
  Live-Boxen liegen bei 3 oder 4 Werten (gestaffelter Spaltenabstand greift).
### p0-3 Vorwissen Technik
- [x] [HOCH] a1 Präfix-Leiter: Zeit-Modus gefixt — hs, ks, Ms ausgegraut und
  durchgestrichen, dafür min (60 s) und h (3600 s) an ihren echten Positionen;
  Live-Box zeigt beide mit Umrechnung im Label.
- [x] [HOCH] a2 Tempo-Umrechner: formel-live mit beiden Umrechnungsrichtungen,
  Ansatz und Werten samt Einheiten; Umrechnungsfaktor zusätzlich in der Live-Box.
- [x] [HOCH] a3: der n³-Wert ist eingelöst — die Animation zeigt jetzt vier
  Modi: Länge, Fläche und Volumen einzeln, dann alle drei verknüpft. Der
  Volumen-Modus zeichnet den Würfel isometrisch mit unterteilten Sichtflächen
  und einem hervorgehobenen Teilwürfel. Die verknüpfte Ansicht stellt n¹, n²
  und n³ nebeneinander und macht damit sichtbar, dass der Exponent die Dimension
  ist — daraus folgt 1 m = 100 cm, 1 m² = 10 000 cm², 1 m³ = 1 000 000 cm³.
- [x] [MITTEL] a4 Temperaturverlauf: Umschalter «Tangente | Sekante»; im
  Sekanten-Modus ein zweiter Punkt per Regler, mit Steigungsdreieck (Δt, ΔT) und
  mittlerer Rate in der Live-Box.
- [x] [MITTEL] a5 Tauchgang: Differenz-Panel unter dem Hauptplot — Δp gespreizt
  von −0.013 bar an der Oberfläche auf +0.063 bar (+1.28 %) bei 40 m.
- [x] [MITTEL] a1: Hinweis «Skala logarithmisch — gleicher Abstand bedeutet
  Faktor 10» oben links im Canvas.

- [x] Stilcheck 27.07.2026: in a4 stand der Multiplikationspunkt als Trenner
  zwischen Uhrzeit und Temperatur («08:30 · 12.4 °C») — durch Leerraum ersetzt.
  Sonst keine Befunde.
### p0-4 Vorwissen Logik
*Alle Punkte umgesetzt am 27.07.2026.*
- [x] [HOCH] a1 Feder: y-Achse fest auf 0 … 85 cm (Maximum 2 kg an D = 25 N/m
  ergibt 78.5 cm); die jeweils andere Feder bleibt als graue Gerade stehen.
  Erst damit ändert der Federwechsel sichtbar die Steigung (39.2 gegen 78.5 cm).
- [x] [HOCH] a2 s = v·t: feste s-Achse 0 … 600 m in beiden Modi (Maximum
  10 m/s · 60 s). Die Gerade kippt jetzt beim Verstellen der Konstante sichtbar.
- [x] [HOCH] a4 Einholproblem: Achsen fest auf 0 … 120 s und 0 … 1060 m
  (100 m + 8 m/s · 120 s). Bei kleiner Geschwindigkeitsdifferenz wandert t*
  sichtbar nach rechts aus dem Bild, statt optisch stehen zu bleiben.
- [x] [HOCH] a5 Gegenrechnung: Umschalter «richtig rechnen | Fehler einbauen».
  Im Fehlermodus rechnet die Animation t = d/vA statt d/(vA+vB); die
  Gegenrechnung schlägt dann fehl und beziffert die Differenz (bei 300 m,
  12 und 8 m/s: A wäre bei 300 m, B bei 100 m). Der verwendete Ansatz steht in
  einer formel-live.
- [x] [MITTEL] a5 visuell von a4 abgesetzt: 1D-Strassenleiste mit beiden Velos,
  Startpunkten und Treffpunktmarke über dem Diagramm.
- [x] [MITTEL] a3 Dreisatz: Marker bei (1 kg, 2.50 CHF) mit Beschriftung
  «auf 1 zurück» — der Zwischenschritt war bisher nur eine Zeile in der Rechnung.
- [x] [MITTEL] a2: der Regler, der gerade die Konstante hält, ist hervorgehoben
  (Rahmen, Hintergrund und Zusatz «(konstant)» am Label).

- [x] Stilcheck 27.07.2026: a2 setzte die Werte ohne Einheiten ein
  («s = v·t = 6·45») — jetzt Formelzeile plus «s = 6 m/s · 45 s = 270 m».
  a3 quetschte drei Aussagen mit «|» in eine Zeile — jetzt vier Zeilen, je
  Dreisatz-Schritt eine benannte Formel und eine Zahlengleichung. a5 zeigte nur
  den symbolischen Ansatz — jetzt zusätzlich die Zahlengleichung mit Einheiten,
  im Fehlermodus entsprechend «t = 300 m / 12 m/s = 25 s».
  Im Beispielblock «ein falsches Resultat fliegt auf» ersetzt die konkrete
  Spanne «20 km bis 50 km» das vage «einige Dutzend Kilometer» (auf Ansage).
### p4-1 Kinematik
- [x] [HOCH] a1: t-Regler ergänzen, Fläche unter v(t) nur bis t einfärben,
  Live-Anzeige «Fläche = v·t = … m» — macht Fläche = Weg quantitativ prüfbar.
  *Erledigt 28.07.2026: t-Regler 0 … 10 s, Rechteck nur bis t gefüllt und
  umrandet, Beschriftung «Fläche = v · t = 75 m» in der Fläche (bei schmalem
  Rechteck daneben). Im s-t-Diagramm wandert der Punkt mit und trägt Lote auf
  beide Achsen — damit ist auch der [NIEDRIG]-Punkt erledigt: der bisher
  unbeschriftete Fixpunkt bei t = 5 s ist jetzt der einstellbare Zeitpunkt.*
- [x] [HOCH] a2 (Dreier-Diagramm): Flächen unter a(t) und v(t) bis zum
  eingestellten t einfärben und als «Fläche = Δv» / «Fläche = s» ausweisen —
  die Erkenntnis-Box behauptet es, kein Diagramm zeigt es.
  *Erledigt 28.07.2026: Rechteck unter a(t) («Fläche = Δv = 10.0 m/s») und
  Trapez unter v(t) («Fläche = s = 25.0 m»), beide bis zum eingestellten t.
  Gemeinsamer Helfer `flaechenLabel` setzt die Beschriftung mittig hinein oder
  daneben, je nach Platz.*
- [x] [HOCH] a3 Freier Fall: Tempo-Regler + Stroboskop-Spur ✓ 28.07.2026:
  Zeitlupenregler 0.1× … 1× (Default 0.4×) und blasse Apfel-Silhouetten alle
  0.25 s mit Zeitmarke. Die Abstände wachsen von 0.31 m auf 4.60 m — das
  Quadratgesetz ist damit direkt ablesbar. Zeitmarken werden ausgelassen, wo
  die Bilder oben zu dicht stehen.
  Ebenfalls erledigt 28.07.2026: h₀-Regler 5 … 40 m mit Live-Fallzeit und
  Aufprall-Tempo, dazu eine 5-kg-Kugel neben dem 0.1-kg-Apfel — beide fallen
  sichtbar gleich schnell (Massenunabhängigkeit).
- [x] [HOCH] a4 Schiefer Wurf: Play-Knopf mit Projektionen ✓ 28.07.2026:
  «▶ Wurf abspielen» mit Pause und Reset; der fliegende Punkt trägt Lote auf
  beide Achsen, die x-Marke wandert gleichförmig, die y-Marke wird langsamer,
  kehrt um und wird wieder schneller. Beide Werte zusätzlich in der Live-Box.
  Der bereits geflogene Bahnteil wird kräftiger nachgezeichnet.
  Ebenfalls erledigt 28.07.2026: Knopf «◻ Bahn festhalten» legt eine violett
  gestrichelte Vergleichsbahn ins Bild — damit ist der 30°/60°-Vergleich (beide
  35.3 m) in einem Blick zu sehen. Winkelbogen am Abwurfpunkt mit α, dazu der
  Hinweis, dass die verschieden skalierten Achsen den Winkel optisch verzerren.
- [x] [HOCH] a6 Schwimmer: animierte Querung mit Bahn und Landepunkt-Versatz in m;
  [MITTEL] Ziel-Fähnchen + Status «trifft das Ziel» bei γ ≈ 0.
  *Beides erledigt 28.07.2026: zweite Leinwand mit der Aufsicht auf einen 40 m
  breiten Fluss, feste x-Skala −40 … 140 m (Q1). Die Bahn wird im Zeitraffer 4×
  nachgezeichnet, am Zielufer stehen Fähnchen (senkrecht gegenüber) und
  Ankunftspunkt; dazwischen ein bezifferter Versatzpfeil. Bei |Δx| < 0.5 m
  erscheint «✓ trifft das Ziel». Querzeit und Versatz zusätzlich in der
  Live-Box. Bei β = 0° oder 180° gibt es keine Querkomponente — dann steht
  statt der Bahn der Hinweis, dass das Zielufer nie erreicht wird.*
- [x] [MITTEL] a0 Zugfahrt: v̄ als gestrichelte Rechteckhöhe über dem Intervall.
  *Erledigt 28.07.2026, mit dem Zusatz «gleiche Fläche wie die Kurve».*
- [x] [MITTEL] a5 Kreisbewegung: Pause-Knopf; Pfeile streng proportional (Q3).
  *Erledigt 28.07.2026: beide Pfeile ohne Sockel und Cap — vorher 50 + v·8 bzw.
  30 + a_z·4, damit war der Vergleich wertlos. Feste Skalen am Reglermaximum
  (v bis 9 m/s, a_z bis 27 m/s²); die Zahlenwerte stehen als Legende oben links,
  weil kurze Pfeile keine Beschriftung tragen können.*
- [x] [MITTEL] herl-cv Trapez: Zerlegung in Rechteck (v0·t) + Dreieck (½at²) tönen.
  *Erledigt 28.07.2026: grünes Rechteck v₀·t, violettes Dreieck ½·a·t².*
- [x] [MITTEL] Neu: Mini-Canvas «Sekante → Tangente» (Δt-Regler) im
  Definitions-Abschnitt Momentangeschwindigkeit. *Erledigt 28.07.2026: eigenes
  Widget mit s(t) = ½·a·t² (a = 2 m/s²), Reglern für t₀ und Δt, Steigungsdreieck,
  Sekante (violett gestrichelt) und Tangente (grün). Die Differenz ist exakt
  a·Δt/2 — bei Δt = 3 s sind es 3.00 m/s, bei Δt = 0.1 s noch 0.10 m/s.*
- [x] [NIEDRIG] a1: unbeschrifteten Fixpunkt bei t = 5 s beschriften oder entfernen.
  *Mit dem t-Regler erledigt — der Punkt ist jetzt der eingestellte Zeitpunkt
  und trägt seinen s-Wert.*

### p4-2 Dynamik
- [x] [HOCH] a3 Trägheit: Umschalter «Bezugssystem: Strasse | Wagen» — der
  Hinweis verlangt den Vergleich, das Widget kann ihn nicht; ausserdem feste
  Bodenmarken. *Erledigt 28.07.2026: Zwei Knöpfe schalten die Kamera um. Im
  Strassensystem steht sie fest, der Wagen fährt aus dem Bild; im Wagensystem
  hängt sie am Wagen, dafür wandern Strasse und Kiste nach links. Metermarken
  an Weltpositionen machen die Bewegung in beiden Systemen sichtbar — ohne sie
  ist im mitfahrenden System nicht zu erkennen, dass sich überhaupt etwas regt.
  Der Hinweistext wechselt mit, und im Wagensystem steht die Warnung, dass
  dieses Bezugssystem selbst beschleunigt ist und das Trägheitsgesetz dort
  nicht gilt.*
- [x] [HOCH] a5 Hang: Zerlegungs-Rechteck gestrichelt einzeichnen — der Abschnitt
  heisst «Kräfte zerlegen», die Konstruktion fehlt. ✓ 28.07.2026: gestricheltes
  Rechteck von der F_H-Spitze über die F_G-Spitze zur Normalkomponente, mit
  rechtem Winkel an der Hangecke. In Python gegengerechnet:
  sin α · û − cos α · n̂ = (0, 1) für jeden Winkel, das Rechteck schliesst also
  exakt auf F_G.
  Ebenfalls erledigt 28.07.2026: Live-Box mit F_H, F_N und F_R in Newton und der
  ausdrücklich deklarierten Bezugsmasse 1.0 kg.
- [x] [MITTEL] a1 Feder: Modus «Masse anhängen», Steigungsdreieck, g-Umschalter.
  *Alles erledigt 28.07.2026: Zwei Modi — «Dehnung vorgeben» (wie bisher) und
  «Masse anhängen», wo die Gewichtskraft die Feder dehnt bis F = F_G. Die
  Rechnung steht als eigene Zeile (F_G = m · g → s = F_G / D). Im Modus «Masse»
  erscheint der Ortsumschalter Erde/Mond: 0.8 kg dehnen die Feder auf der Erde
  um 9.8 cm, auf dem Mond nur um 1.6 cm. Im Diagramm ein Steigungsdreieck
  Δs = 0.08 m mit ΔF und D = ΔF/Δs.*
- [x] [MITTEL] a2 F = m·a: «Letzter Lauf»-Zeile (Q5); Pfeile proportional (Q3).
  *Erledigt 28.07.2026: Alle drei Pfeile ohne Sockel, v zusätzlich ohne Cap;
  feste Skalen am Reglermaximum (F bis 40 N, a bis 80 m/s², v bis 35.8 m/s).
  Nach jedem vollständigen Lauf bleibt eine graue Zeile mit F, m, a und der
  Zeit für die 8 m stehen — damit lässt sich der nächste Lauf vergleichen,
  ohne Werte im Kopf zu behalten.*
- [x] [MITTEL] a4 Reibung: Losruckeln, Knickpunkt, a = (F_zug − F_R)/m.
  *Alles erledigt 28.07.2026: Beim Überschreiten von F_H,max ruckt die Kiste
  0.55 s lang gedämpft — der Hinweistext sprach davon, ohne dass etwas passierte
  (Q4). Im Diagramm markieren eine gestrichelte Vertikale und ein Punkt den
  Knick bei μ_H · F_N. Solange die Kiste haftet, steht «a = 0», sobald sie
  gleitet die vollständige Rechnung mit Werten und Einheiten.*
- [x] [MITTEL] a6 Rückstoss: Produkte m·|v|, Pfeil-Cap entfernt, Feder-Expansion.
  *Alles erledigt 28.07.2026: Beide Impulsbeträge stehen im Bild und sind bei
  jeder Massenkombination gleich gross (2 kg · 3.00 m/s = 4 kg · 1.50 m/s
  = 6.00 kg·m/s) — actio = reactio wird damit quantitativ. Der Cap bei 70 px
  ist weg, feste Skala bis 6 m/s. Neue Phase «exp»: die Feder drückt 0.35 s
  lang, die Wagen beschleunigen auf ihr Endtempo, statt schlagartig loszuspringen.*

### p4-3 Energie
- [x] [HOCH] a1: α-Slider auf 0–90° erweitern — der Kernfall W = 0 bei 90°
  (Erkenntnis + Mini-Check) ist derzeit nicht einstellbar.
  *Erledigt 28.07.2026: Regler bis 90°, dazu eine eigene Formelzeile, die bei
  genau 90° erscheint: «cos 90° = 0 → die Kraft steht senkrecht auf dem Weg und
  verrichtet keine Arbeit».*
- [x] [HOCH] a2: Geister-Punkt bei 2v («×4») bzw. Referenzkurve 2m («×2») in der
  E(v)-Parabel; Bremsweg-Balken in der Szene. *Alles erledigt 28.07.2026:*
  - *Geister-Punkt bei 2v mit Loten auf beide Achsen und Marke «2v → ×4»,
    gestrichelte Referenzkurve für die doppelte Masse.*
  - *Dabei fiel eine mitwachsende Achse auf (Q1): die E-Achse richtete sich nach
    der eingestellten Masse, dadurch sah die Parabel bei 200 kg genauso aus wie
    bei 2000 kg. Jetzt fest 0 … 900 kJ (Reglermaximum).*
  - *Bremsweg-Balken in der Szene auf fester Skala 0 … 60 m, mit Geisterbalken
    für doppeltes Tempo. Aus ½mv² = μmgs folgt s = v²/(2μg) — die Masse kürzt
    sich heraus. Bei μ = 0.8: 30 km/h → 4.4 m, 50 km/h → 12.3 m, Verhältnis
    2.78 = (50/30)². Damit ist a2-cv-szene kein Streichkandidat mehr.*
- [x] [MITTEL] a3 Pendel: Umschalter «mit Reibung», Pendellänge deklariert.
  *Erledigt 28.07.2026: Im Reibungsmodus dämpft ein Term −0.35·ω die Bewegung;
  die entzogene Arbeit wird aufsummiert und als vierter Balken «Wärme»
  dargestellt. Die Summe aus mechanischer Energie und Wärme bleibt konstant —
  damit beantwortet das Widget die ❓-Frage des Abschnitts, statt sie offen zu
  lassen. Pendellänge L = 1.2 m steht neben den Knöpfen.*
- [x] [MITTEL] a5 Heben: zwei Kisten parallel (t fix vs. Slider-t).
  *Erledigt 28.07.2026: links die graue Referenzkiste mit fester Zeit 3.0 s,
  rechts die eingestellte. Beide heben dieselbe Masse auf dieselbe Höhe, oben
  steht die gemeinsame Arbeit, unten je die Leistung — der Unterschied ist in
  einem Blick zu sehen statt durch Merken von Werten.*
- [x] [MITTEL] a6 Wirkungsgrad: Umschalter «zwei Stufen hintereinander».
  *Erledigt 28.07.2026: Die zweite Maschine wird ins Flussdiagramm gezeichnet,
  der Gesamtwirkungsgrad ist das Produkt — bei 60 % je Stufe bleiben 36 %,
  aus 500 J werden 180 J. Die Rechnung steht als eigene Formelzeile.*
- [x] [NIEDRIG] a4-diag: Querverweis Rechteck vs. Dreieck.
  *Erledigt 28.07.2026 als Legende unter dem Diagramm: bei konstanter Kraft ist
  die Fläche ein Rechteck (W = F · s), bei der Feder ein Dreieck — daher ½.*

### p4-4 Statik
- [x] [HOCH] a3 Seile: Werte S₁/S₂/F_G direkt an die Pfeile, bei S > F_G rot —
  der Aha-Effekt «flache Seile → riesige Kräfte» ist sonst nur in der Live-Box.
  *Erledigt 28.07.2026: Werte stehen an den Pfeilen, Seilkräfte über F_G werden
  rot, und unten erscheint der Faktor. Bei α = β = 10° trägt jedes Seil 2.9× die
  Last, bei 5° schon 5.7×.*
- [x] [HOCH] a4 Hebel: F⊥-Sicht zusätzlich zur r-Konstruktion. ✓ 28.07.2026: F wird am Angriffs-
  punkt in F⊥ (grün, senkrecht zum Hebel) und F∥ (grau, dreht nicht) zerlegt,
  mit gestricheltem Ergänzungsrechteck. Unten stehen beide Rechenwege je auf
  eigener Zeile — M = F · r und M = F⊥ · l — und liefern denselben Wert.
  Ebenfalls erledigt 28.07.2026: M als bernsteinfarbener Bogenpfeil um D, dessen
  Öffnungswinkel mit dem Moment wächst, mit Wert darüber.
- [x] [MITTEL] a5 vs. ae-cv (Wippe): a5 aufgewertet statt gestrichen.
  *Erledigt 28.07.2026: Über dem Hebel stehen jetzt zwei Momenten-Balken M₁ und
  M₂ mit ihren Werten und einem Vergleichszeichen (=, < oder >). Damit hat a5
  einen eigenen Inhalt — die Wippe im Einstieg zeigt das Kippen, a5 zeigt die
  beiden Momente als Grössen und schlägt die Brücke zu a4 (M = F · r).*
- [x] [MITTEL] a1: Winkelbogen φ am Ursprung (warum wird Fx negativ?).
  *Erledigt 28.07.2026: Bogen mit Wert am Ursprung; sobald F_x negativ wird,
  erscheint der Hinweis «φ > 90° → cos φ < 0 → F_x zeigt nach links».*
- [x] [MITTEL] a3-tri: Beträge (N) an die Dreieckseiten.
  *Erledigt 28.07.2026: jede Seite trägt ihren Betrag, z.B. F_G = 78 N,
  S1 = S2 = 55 N bei 45°/45°.*
- [x] [MITTEL] a7 Schiefe Ebene: Live-Vergleich tan α vs. μ_H und Grenzwinkel.
  *Erledigt 28.07.2026: eigene Formelzeile zeigt, wie sich die Masse herauskürzt
  (m·g·sin α ≤ μ_H·m·g·cos α → tan α ≤ μ_H), darunter der aktuelle Vergleich mit
  Zahlen und dem Grenzwinkel arctan μ_H. Bei μ = 0.5 liegt er bei 26.6°.*
- [x] [NIEDRIG] ae-cv: «m₁ = 25 kg (fix)» im Canvas anschreiben; a6: formel-live.
  *Beides erledigt 28.07.2026: die feste linke Last steht im Bild, und a6 hat
  eine formel-live mit dem Momentengleichgewicht um A — je Gleichung eine Zeile
  aus Ansatz und Werten.*

### p4-5 Hydrostatik
- [x] [HOCH] a1-ph: Wasser-Referenzgerade fest einzeichnen oder y-Achse fixieren —
  die adaptive Skala macht den Dichtevergleich unsichtbar (Q1).
  *Erledigt 28.07.2026: beides — feste Achse 0 … 1400 kPa, Wasser-Referenzgerade
  und bezifferte Steigung.*
- [x] [HOCH] a3 Presse: Knopf «▶ Pressen» ✓ 28.07.2026: «▶ Pressen»
  mit Pause und Reset; der linke Kolben sinkt um s₁, der rechte steigt um
  s₂ = s₁ · A₁/A₂. Unten steht das verdrängte Volumen A₁ · s₁ = A₂ · s₂ als Zahl.
  Vorher standen beide Kolben starr in Mittellage — «kleiner Weg, grosse Kraft»
  war nur eine Zeile in der Live-Box.
  *Der [MITTEL]-Zusatz «Slider reduzieren» bleibt bewusst offen: vier Regler
  sind bei 360 px eng, aber ein Verhältnis-Regler A₂/A₁ würde die Einzelflächen
  verstecken, die in der Rechnung vorkommen.*
- [x] [HOCH] a5 Schwimmen/Sinken: F_G/F_A-Pfeile proportional statt fix 35 px —
  der Pfeilvergleich IST die Lernbotschaft (Q3). *Erledigt 28.07.2026: beide
  Pfeile streng proportional, feste Skala am Reglermaximum kalibriert
  (3000 kg/m³ → 74 px, Q2). Bei Aluminium ist F_G jetzt 2.7-mal so lang wie
  F_A; die Differenz F_G − F_A ist zusätzlich beziffert. Das Becken musste dafür
  höher werden — der längste Pfeil lief sonst aus der Leinwand.*
- [x] [MITTEL] a2 Paradoxon: Titel/Bild angleichen (Block B); «Bodenkraft F = p·A».
  *Beides erledigt: Titel am 28.07.2026 (Block B), Bodenkraft am selben Tag als
  Umschalter. Bei 12 cm Füllhöhe zeigen alle drei Manometer 11.8 mbar, die
  Bodenkräfte betragen aber 5.92 N, 0.83 N und 23.67 N — genau die Trennung von
  Druck und Kraft aus dem Häufiger-Fehler-Block.*
- [x] [MITTEL] a4-quader: Haltestab einzeichnen; eingetauchtes Volumen schraffieren.
  *Beides erledigt 28.07.2026: Stab bis zur Decke mit der Notiz «wird gehalten»,
  und der eingetauchte Teil ist grün schraffiert — er allein bestimmt V_e und
  damit F_A.*
- [x] [MITTEL] a6 U-Rohr: Vergleichshöhe durchgehend + Druckgleichheit.
  *Erledigt 28.07.2026: Die gestrichelte Linie läuft jetzt durch beide Schenkel,
  darüber steht die Bedingung ρ_Öl · g · h_Öl = ρ_W · g · h_W mit dem aktuellen
  Wert. Bei 10 cm Öl (800 kg/m³) sind das 7.8 mbar auf beiden Seiten.*
- [x] [MITTEL] Neu (in a4 integriert): Federwaage «scheinbares Gewicht».
  *Erledigt 28.07.2026: Rechts im Bild eine Waage, deren Füllstand F_G − F_A
  anzeigt. Der Holzquader (ρ = 700 kg/m³) wiegt bei 10 cm Kante 6.87 N; bei
  6 cm Eintauchtiefe zeigt die Waage noch 0.98 N, ab voller Tauchung 0 N.*

### p5-1 Temperatur
*Alle Punkte umgesetzt am 26.07.2026; a3 (Render-Check) und der Stilcheck für
a3/a4 nachgetragen am 27.07.2026.*
- [x] [HOCH] ein-cv Brown: Knopf «Wasserteilchen anzeigen» (Default aus) —
  erst das rätselhafte Zittern, dann die Ursache; sonst ist die Pointe verschenkt.
- [x] [HOCH] a1 Gasteilchen: Geschwindigkeitsstreuung (Block B); [MITTEL] ein
  markiertes Teilchen mit Momentantempo neben dem Mittelwert.
  → feste Faktoren 0.52 … 1.60, Mittelwert exakt 1.000 (die Anzeige
  «mittl. Tempo» bleibt damit korrekt); markiertes Teilchen mit Faktor 1.42.
- [x] [HOCH] a5 Extrapolation: zweite Gasgerade (anderer Anfangsdruck) — beide
  treffen −273.15 °C; [MITTEL] Extrapolation als Entdeckung (Knopf
  «Geraden verlängern», vorher nur Messpunkte).
  → Gas B mit 60 % des Drucks von Gas A; Achsenschnitt zeigt «?», bis verlängert wird.
- [x] [HOCH] a2 Aggregatzustände: Tm/Tb-Marken des gewählten Stoffs — macht
  Vorhersagen möglich statt Absuchen; [MITTEL] Koexistenz-Zone um Tm.
  → Temperaturschiene mit drei Zonen unter dem Behälter (statt am Regler, dafür
  ist kein neues CSS nötig); Koexistenz exakt bei \(T = T_m\) bzw. \(T = T_b\) —
  physikalisch korrekt statt als Temperaturfenster (ein Reinstoff hat dort keinen
  Temperaturbereich; der «Bereich» liegt in der Energie → Heizkurve p5-2 a3).
  Damit die eine Reglerstellung ohne Zielen erreichbar ist: Sprungknöpfe
  «→ Schmelzpunkt» / «→ Siedepunkt», beschriftet mit den Werten des gewählten
  Stoffs und hervorgehoben, solange der Punkt eingestellt ist.
- [x] [MITTEL] a3 Thermometer: Sprungknöpfe «0 K · 0 °C · 37 °C · 100 °C».
- [x] [MITTEL] a4 Zahlenstrahl: Vorzeichen der Differenz vereinheitlichen.
  → durchgehend **mit** Vorzeichen (nicht per `abs()`), plus Richtungspfeil und
  «Erwärmung/Abkühlung» — Vorbereitung auf \(Q = c\,m\,\Delta T\) und \(\Delta l = \alpha\,l_0\,\Delta T\).
  Typografisches Minus (U+2212) dabei auf der ganzen Seite vereinheitlicht.
- [x] [MITTEL] a3 Thermometer (neu entdeckt beim Render-Check): Die Fixpunkt-
  Beschriftungen waren bei 360 px rechts abgeschnitten («siedet 100…», «abs. Nullp…»),
  weil sie fix bei \(x = 0{.}73\,W\) begannen. Behoben am 27.07.2026: unter 480 px
  rückt die Röhre nach links (\(x = 0.34\,W\)), die Marken hängen jetzt an der Röhre
  statt an der Leinwandbreite, und passt ein Text trotzdem nicht, wird die Kurzform
  gezeichnet («0 °C», «100 °C», «37 °C», «0 K»).
- [x] Stilcheck 27.07.2026 (a3 und a4): a3 setzte die Zahlen ohne ihre Skala ein
  («T = ϑ + 273.15 = 20.00 + 273.15») — jetzt Klammer-Notation wie in p0-3 a2,
  Formelzeile «T [K] = ϑ [°C] + 273.15» vor der Zahlengleichung. Im Bildtitel
  stand der Multiplikationspunkt als Trenner («Celsius links · Kelvin rechts»)
  — durch ein Komma ersetzt. In a4 fehlten die Einheiten beim Einsetzen
  («95 − 12»); die Differenzzeilen liegen jetzt zu je zwei Zeilen vor (Ansatz,
  dann Werte mit Einheit), sonst brechen sie bei 360 px mitten im Term um.
  Auch die Canvas-Zahl trägt ihre Einheit («Δϑ = ΔT = 83 K») und hat einen Halo,
  damit sie über den gestrichelten Marken lesbar bleibt.

### p5-2 Wärme
*Alle Punkte umgesetzt am 26.07.2026.*
- [x] [HOCH] a1 Wärmebedarf: feste kJ-Achse statt qmax-Normierung — m- und
  ΔT-Regler haben derzeit keinerlei sichtbare Wirkung (Q1); Achse beschriften.
  → Achse fest 0 … 2100 kJ (= grösstmöglicher Reglerwert 5 kg · 4182 · 100 K),
  Gitter alle 500 kJ, Achsenlabel «Q [kJ]».
- [x] [HOCH] a3 Heizkurve: aktive Teilformel je Phase anzeigen; [MITTEL]
  Segment-Energien (4.2/33.4/41.8/225.6 kJ) als Klammern.
  → formel-live «gerade aktiv» mit Ansatz + Werten + Temperaturverhalten je
  Abschnitt; Klammern unter der Kurve, aktive hervorgehoben. Die zwei schmalsten
  Segmente (4.2 und 10.05 kJ) tragen keine Beschriftung — dort ist kein Platz;
  der Wert steht in der formel-live, sobald man in der Phase ist.
- [x] [HOCH] a4 Transportarten: Umschalter «Vakuum» — beantwortet die eigene
  Leitfrage und den Thermoskannen-Transfer.
  → Leitung und Konvektion zeigen im Vakuum Quelle und Körper ohne Medium und
  bleiben wirkungslos; nur die Strahlung kommt durch.
- [x] [HOCH] a6 Treibhaus (jetzt a7): natürlicher Treibhauseffekt eingebaut (Block B).
  → 12 Strahlen, 7 hält die Atmosphäre schon bei 280 ppm zurück; der Regler fügt
  bis zu 3 weitere hinzu (violett, als «zusätzlich» beschriftet). Rückhaltung als
  Absorption + Re-Emission gezeichnet, Rückweg mit anderer Richtung als der Hinweg.
- [x] [MITTEL] a2 Mischen: Temperatur-Zahlenstrahl (ϑ₂ … ϑm … ϑ₁) mit Marker
  («Hebelgesetz» der Massen); zweiter Stoff (Öl) → volle Formel.
  → Zahlenstrahl mit beiden Spannen und dem Nachweis m₁c₁(ϑ₁−ϑm) = m₂c₂(ϑm−ϑ₂)
  in Zahlen; Stoffwahl Wasser/Öl für Portion 2, formel-live mit voller Formel.
- [x] [MITTEL] ein-cv: kleines ϑ(t)-Diagramm unter den Boxen (Prozess konservieren).
  → 30-s-Fenster, beide Kurven laufen sichtbar aufeinander zu.
- [x] [MITTEL] Neu: Wärmepumpen-Sankey (Strom 1 Teil + Umgebung 2–4 Teile →
  Heizwärme, COP-Regler).
  → neue Animation 6 in eigener Sektion «Wärmepumpe»; Treibhaus dadurch zu
  Animation 7 umbenannt. Mit ❓-Frage zur COP-Grenze und eigenem Mini-Check;
  Wirkungsgrad-Mini-Check an seine Sektion zurückgesetzt.

### p5-3 Wärmeausdehnung
*Alle Punkte umgesetzt am 26.07.2026.*
- [x] [HOCH] a1 Stab: Überhöhung neu kalibriert (260 statt 4000, Q2), Ausgangsstab
  skaliert mit l₀ mit; damit ist die gezeichnete Verlängerung proportional zum
  echten Δl. Reglerminimum von 1 m auf 10 m gehoben — bei 1 m wäre der Stab
  ein Strich. Dazu Referenzstab Eisen (Q5).
- [x] [HOCH] a2 Volumen: Überhöhung 4.5 statt 120 (Q2); Ethanol, Wasser und
  Quecksilber sind jetzt unterscheidbar.
  Komplett auf isometrische 3D-Darstellung umgestellt: Festkörper als Würfel mit
  drei beschrifteten Kantenpfeilen α·ΔT (macht γ = 3α sichtbar), Flüssigkeiten als
  Gefäss, dessen Säule mit V₀ mitwächst — damit ist der gezeichnete Anstieg
  proportional zum echten ΔV, gleiches Prinzip wie a1. Daneben in beiden Fällen
  Eisen als stehende Referenz (Q5). Kompaktmodus unter 560 px (Text unter das Bild).
- [x] [MITTEL] a4 Meeresspiegel: Faktor 46 statt 120 (Q2), Klemme entfällt.
- [x] [MITTEL] a3 Anomalie: Seebild an den Regler gekoppelt (passende Schicht
  hervorgehoben). Zusätzlich auf −20 °C erweitert: eigener Eis-Ast bei 917 kg/m³
  auf unterbrochener Achse, Sprung beim Gefrieren beziffert, Wasserlinie in der
  Eisdecke mit 91.7 % Eintauchtiefe. Dazu zwei Erklärblöcke (Herleitung aus dem
  Auftrieb, Folgen für den See).
- [x] [MITTEL] a5 Gasgesetz: Zeile «p·V/T = … — bleibt konstant» ergänzt.
- [x] [MITTEL] ein-cv Schiene: Grenztemperatur im Warnzustand ausgewiesen
  (geschlossen ab 43.3 °C).
- [x] [MITTEL] a6: im Amontons-Modus Ursprung beschriftet «0 K = absoluter
  Nullpunkt (vgl. Kapitel 5.1)», mit Führungslinie.
- [x] [NIEDRIG] Neu: Bimetallstreifen-Mini-Animation mit Thermostat-Kontakt
  (schaltet bei 70 °C).

### p6-1 Wellen
- [x] [HOCH] a1 c = λ·f: Kausalität umdrehen (Block B). *Erledigt 28.07.2026.*
- [x] [HOCH] a2 Quer-/Längswelle: wandernde Labels fixen (Block B).
  *Erledigt 28.07.2026, dazu die invertierte Dichtefärbung — siehe Block B.*
- [x] [HOCH] a3 Schall in Medien: feste, bezifferte λ-Achse — Balken reagieren
  sichtbar auf den f-Regler (Q1). *Erledigt 28.07.2026: feste logarithmische
  λ-Achse 0.1 … 200 m mit vier Medienmarken statt normierter Balken.*
- [ ] ~~[HOCH] a5 Emission/Laser: Photonrichtung randomisieren, am Elektron starten
  («zufällige Richtung» wird derzeit behauptet, aber nicht gezeigt)~~ ✓ 28.07.2026:
  Das Photon startete bisher immer am selben festen Punkt und flog immer nach
  rechts oben. Jetzt startet es dort, wo das Elektron beim Rücksprung steht, und
  fliegt in eine je Zyklus andere Richtung. Die letzten fünf Richtungen bleiben
  blass stehen — erst dadurch ist die Zufälligkeit im Bild und nicht nur im Text.
  Der Winkel wird deterministisch aus der Zyklusnummer berechnet (`a5PhotonWinkel`),
  nicht mit `Math.random()` pro Frame — sonst zappelt das Photon.
  **Offen bleibt:** [MITTEL] E1/E2-Niveauschema mit ΔE = hf; [MITTEL] Laser:
  Pumpen + Photonen-Vermehrung.
- [x] [HOCH] a6 Absorption: Energiefluss-Panel Sonne/Boden/Atmosphäre ergänzen —
  die Transmissionskurve allein trägt den Mechanismus (Aufgabe A6.3) nicht;
  λ-Achse in µm beziffern. *Erledigt 28.07.2026, beides:*
  - *Die x-Achse war eine unbezifferte 0…1-Hilfsgrösse — man konnte nicht sehen,
    WO die Absorption einsetzt. Jetzt feste logarithmische Achse 0.2 … 100 µm
    (linear unmöglich: Sonnenlicht 0.4 … 0.8 µm, Erdabstrahlung 4 … 50 µm), das
    sichtbare Band ist markiert, der Abfall liegt bei 3 … 5 µm.*
  - *Zweite Leinwand mit der Bilanz: 240 W/m² kurzwellig durch die Atmosphäre zum
    Boden, 240 W/m² langwellig zurück, davon (1−g) ins All und g zum Boden.
    Pfeilbreiten proportional zur Leistung, Werte auch in der Live-Box.
    Als «vereinfachte Bilanz» deklariert — die realen Absorptionsbanden sind
    zerklüftet, hier geht es um das Prinzip.*
- [ ] [MITTEL] a4 EM-Spektrum: gegenläufige f-Achse unter dem Balken; E = hf als
  Live-Grösse (bereitet den UV-Transfer vor).
- [ ] [MITTEL] Tempo/Reset-Standard auf ein-cv, a1, a2, a5 übertragen (Q6);
  Verweise «vertieft in 6.1a» statt Duplikation.

### p6-1a Wellenexperimente
Insgesamt die stärkste Seite — nur Feinschliff, keine Streichungen:
- [ ] [MITTEL] a1: y(t)-Achse an die tatsächliche Durchlaufzeit anpassen
  (bei c = 4 bleiben derzeit drei Viertel des Diagramms leer).
- [ ] [MITTEL] a2: optionales zweites markiertes Teilchen (Checkbox, zweite
  Spurfarbe) — der Hinweis «vergleiche zwei Teilchen» ist sonst nicht ausführbar.
- [ ] [MITTEL] a4 Reflexion: Checkbox «Spiegelpuls zeigen» (wird intern bereits
  gerechnet) — erklärt Berg→Tal konstruktiv statt nur als Resultat.
- [ ] [MITTEL] a6 stehende Welle: gestrichelte Einhüllende ±2A·cos(2πs/λ) im
  Steh-Modus (wie in a7) — beim Nulldurchgang wirkt es sonst wie «keine Welle».
- [ ] [MITTEL] a7 Eigenmoden: Preset «Gitarrensaite e¹» (L = 0.65 m, c = 429 m/s)
  oder c-Regler — die Erkenntnis rechnet das Beispiel vor, die Simulation kann
  es nicht darstellen. [NIEDRIG] Ton hörbar machen (WebAudio-Sinus bei f_n).

### p6-2 Elektrizität
- [ ] ~~[HOCH] ein-cv: Elektronenrichtung fixen (Block B)~~ ✓ 28.07.2026;
  **offen bleibt** [MITTEL] Schalter klickbar machen (trägt «Strom nur im
  geschlossenen Kreis»).
- [x] [HOCH] a1 Kennlinie: Achse fixieren oder Referenzgerade (Block B / Q1).
  *Erledigt 28.07.2026: beides — feste I-Achse 0 … 1200 mA und Referenzkennlinie
  100 Ω.*
- [x] [HOCH] a4 Parallelschaltung: Kurzschluss-Rahmen entfernen (Block B);
  [MITTEL] Trunk-Punktdichte mit I skalieren — Knotenregel I = I₁ + I₂ sichtbar.
  *Beides erledigt 28.07.2026.*
- [ ] ~~[HOCH] a5 Leistung: durch P-t-Diagramm mit Rechteckfläche = E ersetzen
  (2000 W · 0.5 h = gleiche Fläche wie 500 W · 2 h) — aktuell reine Dekoration~~
  ✓ 28.07.2026: Der Balken zeigte nur die Momentanleistung — die Dauer kam darin
  gar nicht vor, obwohl das Produkt \(P \cdot t\) der Kern der Animation ist.
  Jetzt ein P-t-Diagramm mit festen Achsen (0 … 4200 W, 0 … 12.5 h, Q1); das
  Rechteck trägt seine Fläche als «Fläche = E = … kWh».
  Dazu zwei Ergänzungen, die den genannten Vergleich erst durchführbar machen:
  eine gestrichelte Hyperbel \(P = 1\,\text{kWh}/t\) («alle Punkte darauf:
  1 kWh») und ein Knopf «◻ Vergleich festhalten», der das aktuelle Rechteck als
  violette Kontur stehen lässt (Q5, Vergleich ohne Gedächtnis). Damit wird
  2000 W · 0.5 h gegen 500 W · 2 h als *gleich grosse Fläche* sichtbar, und beide
  Ecken liegen auf der 1-kWh-Kurve.
  **Offen bleibt:** [MITTEL] Geräte-Presets (Wasserkocher, LED, Ladegerät).
- [ ] [MITTEL] a3 Reihenschaltung: U₁/U₂ als proportionale Farbbalken unter den
  Widerstandsboxen (Spannungsteilung sichtbar statt nur lesbar).
- [ ] [MITTEL] a2 Leiterwiderstand: Konsequenz zeigen (I bzw. Verlustleistung
  bei festem U — Überlandleitungs-Transfer).
- [ ] [MITTEL] a6 Gefahren: Markerlinie 30 mA «FI/RCD löst aus» + Szenario-Presets
  («230 V, 1 kΩ → 230 mA»); IEC-Vereinfachung deklarieren.
- [ ] [MITTEL] Neu: Coulomb-Widget (Q₁, Q₂, r; Kraftpfeile; 1/r²) — einziger
  Formelblock der Seite ohne Visualisierung.
- [ ] [NIEDRIG] Neu: statisches U(t)-Panel AC vs. DC (230 V eff / 325 V Scheitel).

---

## D. Neue Animationen (gesammelt, priorisiert)

| Prio | Seite | Vorschlag |
|---|---|---|
| MITTEL | p4-1 | Sekante → Tangente (Δt-Regler) zur Momentangeschwindigkeit |
| ~~MITTEL~~ ✓ | p5-2 | ~~Wärmepumpen-Sankey mit COP-Regler~~ — umgesetzt als Animation 6 |
| MITTEL | p6-2 | Coulomb-Gesetz (1/r²-Widget) |
| MITTEL | p4-5 | Federwaage «scheinbares Gewicht» (in Anim. 4 integrierbar) |
| MITTEL | p0-1 | Runden-Widget (Kommastellen vs. signifikante Stellen) |
| MITTEL | p0-2 | Wärmestrom-Widget (zwei Körper, Pfeil ∝ ΔT) zu «Temperatur ≠ Wärme» |
| MITTEL | p0-3 | DEG/RAD-Vergleichswidget (sin x in beiden Modi, ohne Canvas machbar) |
| MITTEL | p0-4 | Streudiagramm «Korrelation ≠ Kausalität» (dritte Variable als Farbe) |
| ~~NIEDRIG~~ ✓ | p5-3 | ~~Bimetallstreifen~~ — umgesetzt |
| NIEDRIG | p6-1 | Wasserwellen-Kreisbahnen |
| NIEDRIG | p6-2 | AC/DC-U(t)-Panel |

## E. Streichungen / Ersatz / Zusammenlegungen

- ~~**Ersetzen:** p6-2 a5 (Leistungsbalken) → P-t-Flächendiagramm.~~ ✓ 28.07.2026.
- ~~**Streichkandidat (nur falls nicht aufgewertet):** p4-3 a2-cv-szene (statisches
  Auto) — ohne Bremsweg-Erweiterung trägt es nichts, was das Diagramm nicht zeigt.~~
  ✓ 28.07.2026 aufgewertet: Bremsweg-Balken mit Geisterbalken bei 2v. Bleibt.
- **Zusammenlegen oder differenzieren:** ~~p0-0 a1 + a2 (zweimal dieselbe
  Preis-Mengen-Gerade)~~ ✓ *erledigt 26.07.2026: a2 entfallen, a1 trägt jetzt vier
  Szenarien (Taxi ohne/mit Grundgebühr, Äpfel lose/in Harasse)*.
  p4-4 ae-cv + a5 (zweimal Hebelgesetz mit Kipp-Feedback) — a5 aufwerten oder
  streichen. ~~p0-4 a4 + a5 visuell differenzieren~~ ✓ *erledigt 27.07.2026:
  a5 hat jetzt die 1D-Strassenleiste über dem Diagramm*.
- **Bewusst behalten trotz Überlappung:** p4-1 a1/a2 (gleichförmig → beschleunigt,
  saubere Stufung), p4-5 ae/a1 (Phänomen → Formel), p5-1 a3/a4 (Wert → Differenz),
  p6-1 vs. p6-1a (Überblick vs. Vertiefung — aber a1 kausal korrigieren).

## F. Empfohlene Reihenfolge der Umsetzung

1. ~~**Block B** (fachliche Fehler) — kleine Eingriffe, grösster Schaden behoben.~~
   ✓ erledigt 28.07.2026.
2. ~~**Q1 + Q2** (feste Achsen, Überhöhungs-Kalibrierung) — eine Fix-Familie,
   betrifft ~10 Widgets, macht tote Regler wieder lernwirksam.~~
   ✓ erledigt 28.07.2026.
3. ~~**[HOCH]-Einzelpunkte** je Seite (Abschnitt C).~~
   ✓ **alle erledigt am 28.07.2026** — p4-1 bis p4-5, p6-1 und p6-2.
   p6-1a hatte keine HOCH-Punkte. Damit sind die Schritte 1 bis 3 der
   empfohlenen Reihenfolge durch; es verbleiben Q3–Q6, die [MITTEL]- und
   [NIEDRIG]-Punkte sowie Abschnitt D (neue Animationen).
4. **Q3–Q6 und [MITTEL]** nach Gelegenheit, seitenweise beim nächsten Besuch.
5. **Neue Animationen** (Abschnitt D) zuletzt — der Bestand hat Vorrang.
