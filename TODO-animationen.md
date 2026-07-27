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

## A. Querschnittsbefunde (mehrere Seiten, gemeinsame Ursache)

- [ ] **[HOCH] Q1 — Mitwachsende/adaptive Achsen neutralisieren den Lerneffekt.**
  Die Achse skaliert mit dem Parameter mit, dadurch sieht der Graph bei jeder
  Einstellung gleich aus; genau der versprochene Vergleich (Steigung, wandernder
  Punkt) wird unsichtbar. Fix: feste Achsen oder feste Referenzkurve.
  Betroffen: p0-4 a1 (Feder), p0-4 a2 (s = v·t), p0-4 a4 (Einholproblem),
  p4-5 a1-cv-ph (p(h) je Dichte), ~~p5-2 a1 (Wärmebedarf-Balken)~~ ✓, p6-1 a3
  (Schall-Balken), p6-2 a1 (U-I-Kennlinie), ~~p0-0 a6~~ ✓ / p0-2 a1 (Dichte-Balken).
- [ ] **[HOCH] Q2 — Überhöhungsfaktoren nicht am Reglermaximum kalibriert (Sättigung).**
  ~~p5-3 a1 (Faktor 4000 → ≈260), p5-3 a2 (120 → ≈4.5), p5-3 a4 (120 → ≈46)~~ ✓:
  Die Grafik klemmt über weite Bereiche am Anschlag, Materialwechsel und
  ΔT-Regler ändern das Bild nicht. Ein gemeinsamer, kleiner Fix.
- [ ] **[MITTEL] Q3 — Pfeillängen mit Sockel/Cap oder fix statt proportional.**
  Wo der Grössenvergleich der Pfeile die Botschaft ist, muss streng proportional
  skaliert werden. Betroffen: p4-1 a5 (v/a_z), p4-2 a2 (F/a), p4-2 a6
  (v-Pfeile gecappt), p4-5 a5 (F_G/F_A fix 35 px). Vorbild: p4-2 a5.
- [ ] **[MITTEL] Q4 — «Worauf achten»-Aufträge, die das Widget nicht ausführen kann.**
  Entweder Feature nachrüsten (bevorzugt, siehe Einzelpunkte) oder Hinweistext
  anpassen: p4-1 a3 (Fallwege vergleichen ohne Zeitlupe/Spur), p4-2 a3
  (Bezugssystem wechseln ohne Umschalter), p4-2 a4 («losruckt» ohne Bewegung),
  p6-1a a2 (zwei Teilchen vergleichen, nur eines markierbar), ~~p5-2 a4
  (Vakuum-Frage ohne Vakuum)~~ ✓, p0-2 a1 (Balken reagieren nicht).
- [ ] **[MITTEL] Q5 — Vergleiche ohne Gedächtnis.** Serielle Vergleiche (erst A
  einstellen, dann B, Wert merken) durch Geister-/Referenzdarstellungen ersetzen:
  p4-2 a2 («letzter Lauf»-Zeile), p4-3 a2-diag (Geister-Punkt bei 2v), p0-2 a2
  (Referenzmarken Erde/Mond/Mars), p4-1 a4 («Bahn festhalten»), ~~p5-3 a1/a2
  (Referenzstab/-gefäss Eisen)~~ ✓.
- [ ] **[MITTEL] Q6 — Tempo-Regler + Reset (p6-1a-Standard) nachrüsten** bei den
  animierten Widgets ohne: p4-1 a3 (freier Fall), p6-1 ein-cv, a1, a2, a5.

---

## B. Fachliche Fehler (vor allem anderen beheben)

- [ ] **[HOCH] p6-2 ein-cv:** Elektronen laufen aussen von + nach −; die
  Erkenntnis-Box lehrt das Gegenteil. Umlaufrichtung umkehren, Pfeile
  «Elektronen» vs. «technische Stromrichtung» beschriften.
- [ ] **[HOCH] p6-1 a2:** Labels «Verdichtung»/«Verdünnung» stehen ortsfest,
  das Dichtemuster wandert — Beschriftung meist an der falschen Stelle.
  Labelposition aus der Phase berechnen (Lösung existiert in p6-1a, Z. 1094 ff.).
- [ ] **[HOCH] p6-1 a1 (c = λ·f):** λ und f unabhängig einstellbar, c abgeleitet —
  erzeugt das Fehlkonzept «Medium passt seine Geschwindigkeit an», im Widerspruch
  zum eigenen Theorieblock und zu p6-1a A2. Kausalität umdrehen (Regler f und c,
  λ = c/f abgeleitet); zudem Gitter + s-Achse ergänzen.
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
- [ ] **[HOCH] p0-3 a1 (Präfix-Leiter):** Im Zeit-Modus erscheinen die Sprossen
  «hs», «ks», «Ms» — widerspricht dem eigenen Lehrtext («oberhalb der Sekunde
  nicht dezimal»). Obere Sprossen ausblenden oder durch min/h ersetzen.
- [ ] **[HOCH] p6-2 a4 (Parallelschaltung):** Der rechte Rahmen ist topologisch
  ein Kurzschluss-Zweig ohne Strompunkte. Leitung beim zweiten Zweig enden lassen.
- [ ] **[MITTEL] p6-2 a6:** Zonengrenzen sind vereinfachte Eigenformeln, aber mit
  «IEC» beschriftet — «vereinfacht nach IEC 60479» deklarieren oder verifizieren.
- [ ] **[MITTEL] p4-3 a4:** Text sagt «Dehnung», gezeichnet ist eine Stauchung —
  Bild oder Wortwahl («Auslenkung») vereinheitlichen.
- [ ] **[MITTEL] p4-5 a2:** Titel «Drei verbundene Gefässe», gezeichnet sind
  getrennte Gefässe — Titel korrigieren oder Verbindungsrohr einzeichnen.

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
- [x] [NIEDRIG] a5 (neu a4) Faustregel-Diagramm: Abweichung als Klammer zwischen
  den beiden Kurven, mit Betrag und Prozentwert (bei 40 m: +0.063 bar, +1.28 %).

### p0-1 Vorwissen Mathematik
- [ ] [HOCH] a1-sz Tauchszene: lastende Wassersäule über dem Taucher einfärben —
  der Mechanismus «mehr Wasser über dir → mehr Druck» ist sonst unsichtbar.
- [ ] [HOCH] a2 Hyperbel: konstantes Produkt als halbtransparentes Rechteck unter
  dem Kurvenpunkt («Fläche = v·t = 120 km») — zeigt, warum die Kurve so fällt.
- [ ] [HOCH] a6 Formel-Waage: Fehler-Demo «nur eine Seite ·t» → Waage kippt
  sichtbar. Sonst ist die Waage Dekoration. Dazu [MITTEL] Schritthistorie
  (alle bisherigen Gleichungszeilen) unter der Waage.
- [ ] [MITTEL] a4 Bogenmass: Rastpunkt/Knopf «1 rad (57.3°)» + Radiuslänge als
  gerades Vergleichssegment an den Bogen anlegen.
- [ ] [MITTEL] a5 Zehnerpotenz-Leiter: Achse und Sliderbereich konsistent machen
  (bei n = 9, m > 1 läuft der Punkt über das Achsenende hinaus).
- [ ] [MITTEL] a1-ph: Steigungsdreieck (1 m / 9.81 kPa) an der Geraden.
- [ ] [NIEDRIG] a3 Zylindertank: Volumen-Balken (wie p0-0 a3, Code dupliziert).

### p0-2 Vorwissen Physik
- [ ] [HOCH] a1 Dichte-Würfel + a6 Teilchenmodell: identische Fixes wie p0-0
  (feste Massenskala, Autostart) — in beiden Dateien konsistent umsetzen.
- [ ] [HOCH] a3 Hubarbeit: W als Balken mit fester Joule-Skala; Kistengrösse von
  der Masse entkoppeln (suggeriert sonst Masse ∝ Volumen — direkt nach dem
  Dichte-Abschnitt). Dazu [MITTEL] formel-live-Zeile.
- [ ] [MITTEL] a2 Federwaage: Referenzmarken der anderen Orte dauerhaft an der
  Skala (Erde/Mars/Mond) — der Sechstel-Vergleich wird zum Ablesen.
- [ ] [MITTEL] a4 Rutsche: Play-Knopf «rutschen lassen» (beschleunigt) —
  Geschwindigkeitszunahme sichtbar, ohne ½mv² vorwegzunehmen.
- [ ] [MITTEL] a5 Treppenlauf: wie p0-0 a7 (Code dupliziert).

### p0-3 Vorwissen Technik
- [ ] [HOCH] a1 Präfix-Leiter: Zeit-Modus fixen (siehe Block B).
- [ ] [HOCH] a2 Tempo-Umrechner: formel-live-Zeile mit der Division durch 3.6.
- [ ] [HOCH] a3 Quadratmeter-Raster: den n³-Wert visuell einlösen (Mini-Würfel
  oder Textzeile unter dem Canvas) — aktuell 2D-Bild mit unbelegter 3D-Zahl.
- [ ] [MITTEL] a4 Temperaturverlauf: Umschalter «Tangente | Sekante» mit zweitem
  ziehbarem Punkt (deckt Aufgabe A4.3 ab, bereitet Kinematik vor).
- [ ] [MITTEL] a5 Tauchgang: Differenz-Panel (Δp gespreizt) unter dem Hauptplot.
- [ ] [MITTEL] a1: Hinweis «Skala logarithmisch — gleicher Abstand = Faktor 10».

### p0-4 Vorwissen Logik
- [ ] [HOCH] a1 Feder: y-Achse fest (0–85 cm), inaktive Feder-Gerade grau stehen
  lassen — erst dann ändert der Federwechsel sichtbar die Steigung.
- [ ] [HOCH] a2 s = v·t: feste s-Achse 0–600 m in beiden Modi — die Gerade kippt
  beim Verstellen der Konstante; genau dieser Unterschied ist die Lektion.
- [ ] [HOCH] a4 Einholproblem: Zeitachse fixieren (0–120 s) — t* «explodiert»
  dann sichtbar nach rechts, statt optisch stehen zu bleiben.
- [ ] [HOCH] a5 Gegenrechnung: «Fehler einbauen»-Knopf (z.B. t = d/vA) — der
  ✓-Check kann derzeit nie fehlschlagen, der Prüf-Nutzen ist unerlebbar.
- [ ] [MITTEL] a5 visuell von a4 absetzen (1D-Strassenleiste mit Velos statt
  zweitem fast identischem s-t-Graphen).
- [ ] [MITTEL] a3 Dreisatz: Marker bei (1 kg, 2.50 CHF) «auf 1 zurück»; optional
  Toggle «mit Mengenrabatt» (Grenze des Dreisatzes explorierbar).
- [ ] [MITTEL] a2: aktiven «Konstante»-Slider visuell markieren.

### p4-1 Kinematik
- [ ] [HOCH] a1: t-Regler ergänzen, Fläche unter v(t) nur bis t einfärben,
  Live-Anzeige «Fläche = v·t = … m» — macht Fläche = Weg quantitativ prüfbar.
- [ ] [HOCH] a2 (Dreier-Diagramm): Flächen unter a(t) und v(t) bis zum
  eingestellten t einfärben und als «Fläche = Δv» / «Fläche = s» ausweisen —
  die Erkenntnis-Box behauptet es, kein Diagramm zeigt es.
- [ ] [HOCH] a3 Freier Fall: Tempo-Regler (0.25x–1x) + Stroboskop-Spur (alle
  0.25 s eine blasse Silhouette → s ∝ t² direkt sichtbar); [MITTEL] h₀-Regler
  mit Live-Fallzeit; [MITTEL] zweiter, schwererer Körper (Massenunabhängigkeit).
- [ ] [HOCH] a4 Schiefer Wurf: Play-Knopf mit fliegendem Punkt und mitlaufenden
  Projektionen auf beide Achsen (Überlagerungsprinzip); [MITTEL] Geisterkurve
  «Bahn festhalten» (30°/60°-Vergleich); [MITTEL] Winkelbogen mit α einzeichnen
  (nicht-isometrische Achsen verzerren den Winkel).
- [ ] [HOCH] a6 Schwimmer: animierte Querung mit Bahn und Landepunkt-Versatz in m;
  [MITTEL] Ziel-Fähnchen + Status «trifft das Ziel» bei γ ≈ 0.
- [ ] [MITTEL] a0 Zugfahrt: v̄ als gestrichelte Rechteckhöhe über dem Intervall.
- [ ] [MITTEL] a5 Kreisbewegung: Pause-Knopf; Pfeile streng proportional (Q3).
- [ ] [MITTEL] herl-cv Trapez: Zerlegung in Rechteck (v0·t) + Dreieck (½at²) tönen.
- [ ] [MITTEL] Neu: Mini-Canvas «Sekante → Tangente» (Δt-Regler) im
  Definitions-Abschnitt Momentangeschwindigkeit.
- [ ] [NIEDRIG] a1: unbeschrifteten Fixpunkt bei t = 5 s beschriften oder entfernen.

### p4-2 Dynamik
- [ ] [HOCH] a3 Trägheit: Umschalter «Bezugssystem: Strasse | Wagen» — der
  Hinweis verlangt den Vergleich, das Widget kann ihn nicht; ausserdem feste
  Bodenmarken (die mitfahrende Kamera ist selbst ein beschleunigtes Bezugssystem).
- [ ] [HOCH] a5 Hang: Zerlegungs-Rechteck gestrichelt einzeichnen — der Abschnitt
  heisst «Kräfte zerlegen», die Konstruktion fehlt; [MITTEL] Live-Box mit
  F_H/F_N/F_R in N und Deklaration der Masse.
- [ ] [MITTEL] a1 Feder: Modus «Masse anhängen» (m-Regler, s = mg/D) — verbindet
  Hooke mit F_G = m·g und Aufgabe A1; Steigungsdreieck «D = …» im Diagramm;
  optional g-Umschalter Erde/Mond (deckt Mond-Transfer im Mini-Check ab).
- [ ] [MITTEL] a2 F = m·a: «Letzter Lauf»-Zeile (Q5); Pfeile proportional (Q3).
- [ ] [MITTEL] a4 Reibung: Block beim Übergang kurz losruckeln lassen; Knickpunkt
  beschriften (μ_H·F_N, gestrichelte Vertikale); a = (F_zug − F_R)/m anzeigen.
- [ ] [MITTEL] a6 Rückstoss: Produkte m·|v| beidseitig anzeigen (actio = reactio
  quantitativ); Pfeil-Cap entfernen; kurze Feder-Expansionsphase animieren.

### p4-3 Energie
- [ ] [HOCH] a1: α-Slider auf 0–90° erweitern — der Kernfall W = 0 bei 90°
  (Erkenntnis + Mini-Check) ist derzeit nicht einstellbar.
- [ ] [HOCH] a2: Geister-Punkt bei 2v («×4») bzw. Referenzkurve 2m («×2») in der
  E(v)-Parabel; Bremsweg-Balken in der Szene (v²-Wirkung körperlich sichtbar,
  trägt den 30/50-km/h-Einstieg) — sonst ist a2-cv-szene Streichkandidat.
- [ ] [MITTEL] a3 Pendel: Checkbox «mit Reibung» (E_ges sinkt, Kategorie «Wärme»
  wächst — beantwortet die ❓-Frage); Pendellänge L = 1.2 m deklarieren.
- [ ] [MITTEL] a5 Heben: zwei Kisten parallel (t fix vs. Slider-t) — Leistung
  als Unterschied auf einen Blick statt seriell.
- [ ] [MITTEL] a6 Wirkungsgrad: Checkbox «zweite Stufe» (η_ges = η₁·η₂ —
  Transferaufgabe des Mini-Checks).
- [ ] [NIEDRIG] a4-diag: Querverweis Rechteck (konstante Kraft) vs. Dreieck
  (lineare Kraft, Faktor ½) im Text/Popup.

### p4-4 Statik
- [ ] [HOCH] a3 Seile: Werte S₁/S₂/F_G direkt an die Pfeile, bei S > F_G rot —
  der Aha-Effekt «flache Seile → riesige Kräfte» ist sonst nur in der Live-Box.
- [ ] [HOCH] a4 Hebel: F⊥-Sicht zusätzlich zur r-Konstruktion darstellen (der
  Beweis-Block verspricht beide Sichtweisen); [MITTEL] M als Bogenpfeil um D.
- [ ] [MITTEL] a5 vs. ae-cv (Wippe): doppeln sich — a5 aufwerten (Momenten-Balken
  M₁/M₂ oder Kraft unter Winkel als Brücke zu a4), sonst a5 streichen und das
  Hebelgesetz an der Wippe formalisieren.
- [ ] [MITTEL] a1: Winkelbogen φ am Ursprung (warum wird Fx negativ?).
- [ ] [MITTEL] a3-tri: Beträge (N) an die Dreieckseiten.
- [ ] [MITTEL] a7 Schiefe Ebene: Live-Vergleich tan α vs. μ_H bzw. Grenzwinkel
  arctan μ_H anzeigen.
- [ ] [NIEDRIG] ae-cv: «m₁ = 25 kg (fix)» im Canvas anschreiben; a6: formel-live.

### p4-5 Hydrostatik
- [ ] [HOCH] a1-ph: Wasser-Referenzgerade fest einzeichnen oder y-Achse fixieren —
  die adaptive Skala macht den Dichtevergleich unsichtbar (Q1).
- [ ] [HOCH] a3 Presse: Knopf «▶ Pressen» (Kolben fahren gegenläufig, Volumen-
  erhaltung animiert) — trägt den ganzen Abschnitt; [MITTEL] Slider reduzieren
  (F₁ + Verhältnis A₂/A₁ + s₁ statt vier Einzelregler).
- [ ] [HOCH] a5 Schwimmen/Sinken: F_G/F_A-Pfeile proportional statt fix 35 px —
  der Pfeilvergleich IST die Lernbotschaft (Q3).
- [ ] [MITTEL] a2 Paradoxon: Titel/Bild angleichen (Block B); Checkbox
  «Bodenkraft F = p·A» (koppelt an den Häufiger-Fehler-Block).
- [ ] [MITTEL] a4-quader: Haltestab/Hand einzeichnen («wird gehalten» — der
  frei schwebende Holzquader irritiert); eingetauchtes Volumen schraffieren.
- [ ] [MITTEL] a6 U-Rohr: Vergleichshöhe als durchgehende Linie durch beide
  Schenkel + Druckgleichheit an der Grenzfläche anschreiben.
- [ ] [MITTEL] Neu (in a4 integrierbar): Federwaage «scheinbares Gewicht»
  (Anzeige sinkt beim Eintauchen um F_A) — Transfer «Stein unter Wasser».

### p5-1 Temperatur
*Alle Punkte umgesetzt am 26.07.2026.*
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
- [ ] [MITTEL] a3 Thermometer (neu entdeckt beim Render-Check): Die Fixpunkt-
  Beschriftungen sind bei 360 px rechts abgeschnitten («siedet 100…», «abs. Nullp…»),
  weil sie fix bei \(x = 0{.}73\,W\) beginnen. Textbreite messen und Anker
  umschalten oder Labels bei schmalem Canvas kürzen.

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
- [ ] [HOCH] a1 c = λ·f: Kausalität umdrehen (Block B).
- [ ] [HOCH] a2 Quer-/Längswelle: wandernde Labels fixen (Block B).
- [ ] [HOCH] a3 Schall in Medien: feste, bezifferte λ-Achse — Balken reagieren
  sichtbar auf den f-Regler (Q1).
- [ ] [HOCH] a5 Emission/Laser: Photonrichtung randomisieren, am Elektron starten
  («zufällige Richtung» wird derzeit behauptet, aber nicht gezeigt); [MITTEL]
  E1/E2-Niveauschema mit ΔE = hf; [MITTEL] Laser: Pumpen + Photonen-Vermehrung.
- [ ] [HOCH] a6 Absorption: Energiefluss-Panel Sonne/Boden/Atmosphäre ergänzen —
  die Transmissionskurve allein trägt den Mechanismus (Aufgabe A6.3) nicht;
  λ-Achse in µm beziffern.
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
- [ ] [HOCH] ein-cv: Elektronenrichtung fixen (Block B); [MITTEL] Schalter
  klickbar machen (trägt «Strom nur im geschlossenen Kreis»).
- [ ] [HOCH] a1 Kennlinie: Achse fixieren oder Referenzgerade (Block B / Q1).
- [ ] [HOCH] a4 Parallelschaltung: Kurzschluss-Rahmen entfernen (Block B);
  [MITTEL] Trunk-Punktdichte mit I skalieren — Knotenregel I = I₁ + I₂ sichtbar.
- [ ] [HOCH] a5 Leistung: durch P-t-Diagramm mit Rechteckfläche = E ersetzen
  (2000 W · 0.5 h = gleiche Fläche wie 500 W · 2 h) — aktuell reine Dekoration;
  [MITTEL] Geräte-Presets (Wasserkocher, LED, Ladegerät) für die Kostenanzeige.
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

- **Ersetzen:** p6-2 a5 (Leistungsbalken) → P-t-Flächendiagramm.
- **Streichkandidat (nur falls nicht aufgewertet):** p4-3 a2-cv-szene (statisches
  Auto) — ohne Bremsweg-Erweiterung trägt es nichts, was das Diagramm nicht zeigt.
- **Zusammenlegen oder differenzieren:** p0-0 a1 + a2 (zweimal dieselbe
  Preis-Mengen-Gerade) — ein Widget mit Modus-Umschalter, oder a2 mit
  1-kg-Punkt aufwerten. p4-4 ae-cv + a5 (zweimal Hebelgesetz mit Kipp-Feedback) —
  a5 aufwerten oder streichen. p0-4 a4 + a5 visuell differenzieren (derzeit fast
  identisches Bild für zwei verschiedene Konzepte).
- **Bewusst behalten trotz Überlappung:** p4-1 a1/a2 (gleichförmig → beschleunigt,
  saubere Stufung), p4-5 ae/a1 (Phänomen → Formel), p5-1 a3/a4 (Wert → Differenz),
  p6-1 vs. p6-1a (Überblick vs. Vertiefung — aber a1 kausal korrigieren).

## F. Empfohlene Reihenfolge der Umsetzung

1. **Block B** (fachliche Fehler) — kleine Eingriffe, grösster Schaden behoben.
2. **Q1 + Q2** (feste Achsen, Überhöhungs-Kalibrierung) — eine Fix-Familie,
   betrifft ~10 Widgets, macht tote Regler wieder lernwirksam.
3. **[HOCH]-Einzelpunkte** je Seite (Abschnitt C).
4. **Q3–Q6 und [MITTEL]** nach Gelegenheit, seitenweise beim nächsten Besuch.
5. **Neue Animationen** (Abschnitt D) zuletzt — der Bestand hat Vorrang.
