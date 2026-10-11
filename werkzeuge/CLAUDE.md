# Werkzeuge (Trainer) — Details

Aus der Wurzel-`CLAUDE.md` ausgelagert (11.10.2026, /doctor): Claude Code lädt diese Datei, sobald in diesem
Ordner gearbeitet wird. Die Regeln der Wurzel-`CLAUDE.md` gelten weiter; bei Widerspruch gilt STYLEGUIDE.md.

- `werkzeuge/einheitentrainer.html` — Übungsseite mit drei Modi (Freies Üben,
  Lernmodus, Prüfungsmodus), bis 10.10.2026 Themenseite 0.4. Einziger Ort im Repo, der
  `localStorage` nutzt (Key `tals-physik-p0-4-lernstand-v1` — der alte Name bleibt,
  damit der Lernstand beim Umzug nicht verloren geht —, Lernstand mit Rücksetzknopf) — deshalb hält
  `rechtliches.html` das ausdrücklich fest. Einheiten und Faktoren stehen dort in
  **einer** Datenstruktur (`ET_GRUPPEN`), aus der Aufgaben, Diagnosen und die
  Umrechnungstabellen zugleich entstehen; Faktoren nie an zweiter Stelle notieren.
  Verweise (eine Aufgabenart, also je Seite einmal): Themenseiten 0.2, 0.5 und 4.3, Leitprogramme
  Vorwissen (Schluss), Rechnen, Energie und Statik (je in einer Lösung).
- `werkzeuge/freischneiden.html` — Trainer Freischneiden (4.2/4.4, seit 10.10.2026): Kräfte
  selbst einzeichnen (Palette mit echten Kräften **und Fallen**: Bewegungs-, Hangabtriebs-,
  Zentrifugalkraft, Kraft auf die Unterlage), Richtung im 15°-Raster, Diagnose je Fehlerbild,
  danach die Frage nach der Resultierenden und die Lösung mit Rechenweg und Kräfteplan.
  17 Szenen in drei Stufen (seit 11.10.2026 dazu: schneller gezogen, Aufzug, Kiste gleitet die Rampe hinauf).
  Fallen-Texte je Szene (keine «Ebene» ohne Ebene); Haftreibung mit \(\mu_H\) («nur so gross wie nötig»). Alles in drei Strukturen: `FS_KRAEFTE`, `FS_DIAGNOSE`,
  `FS_SZENEN` (jede Szene baut aus Zufallswerten ihre Musterlösung). Selbsttest
  `fsSelbsttest` über `scripts/verify_freischneiden.js` im Pre-Flight: Musterlösung richtig,
  Gleichgewicht bzw. Resultierende passt zur Antwort, \(F_G = m g\), \(F_R = \mu F_N\),
  \(F_R = m a\), jeder typische Fehler bekommt seine Diagnose. Testhaken `window.__fs`
  (`szene(id, seed)`, `muster()`, `mass()` prüft, ob Pfeile samt Etikett im Bild liegen).
  Kein `localStorage`. Seit 10.10.2026 zwei Aufgabenarten als Reiter (Anker `#aufgabe-freischneiden`,
  `#aufgabe-kraefteplan`): (2) **Kräfteplan** — Art und Richtung gegeben, bekannt sind \(F_G\) und
  `gegeben`; die übrigen Längen zieht man auf Karopapier (¼ Kästchen), Massstab der feinste, bei dem die grösste
  Kraft höchstens 12 Kästchen misst, jeder gesuchte Pfeil mindestens 2 Kästchen; die Liste nennt auch die Länge des Summenpfeils; geschlossen bei Gleichgewicht, sonst zeigt der Schlusspfeil in Richtung der
  Beschleunigung; danach Ablesen mit Diagnosen (Kästchen statt N, sin/cos vertauscht über `vertauscht` — je Kraft Wert und eigener Text —,
  F_G statt). Szenen mit Beträgen unter einem Kästchen tragen `ohnePlan` (Schlitten, Lieferwagen).
  Verweise je Aufgabenart: Themenseiten 4.2 (`#schiefe-ebene`) und 4.4 (`#resultierende`), Leitprogramm
  Dynamik Kapitel 2 (beide), Statik Kapitel 2 (Kräfteplan) und 3 (Freischneiden).
- `werkzeuge/bewegungsdiagramme.html` — Trainer Bewegungsdiagramme (4.1, seit 11.10.2026), drei
  Aufgabenarten als Reiter (Anker `#aufgabe-zuordnen`, `#aufgabe-ablesen`, `#aufgabe-worte`): s-t ↔ v-t
  und v-t → a-t, ab Stufe 2 auch a-t → v-t und s-t → a-t zuordnen (vier Diagramme, die falschen je aus einem Fehlbild: Form übernommen, Vorzeichen,
  Ruhe im falschen Diagramm, Gerade statt Parabel, Krümmung, Betrag), Steigung und Fläche ablesen (Diagnosen:
  Wert statt Steigung, Kehrwert, Vorzeichen, Rechteck statt Trapez, nur Dreieck) und eine Beschreibung in
  Worten als Diagramm erkennen (dazu Reihenfolge, Stillstand). Eine Bewegung ist eine Kette von Abschnitten
  {d, v, a} in `BD_VORLAGEN` (13 Vorlagen, drei Stufen); daraus Diagramme, Text, Fragen und Fehlbilder.
  Eigenes Raster je Achse (`bdRaster`: alle Eckwerte auf Linien). Selbsttest `bdSelbsttest` über
  `scripts/verify_bewegungsdiagramme.js` im Pre-Flight (Ableitungen und Fläche numerisch nachgerechnet,
  Fehlbilder sichtbar verschieden, jede Diagnose). Verweise je Aufgabenart: Themenseite 4.1 `#darstellungen`
  (Zuordnen, In Worten) und `#theorie` (Ablesen), Leitprogramm Kinematik Kapitel 1 und 2. Kein `localStorage`.
- `werkzeuge/fall-und-wurf.html` — Trainer Fall und Wurf (4.1, seit 11.10.2026): freier Fall, senkrecht nach
  oben (aus der Hand oder vom Balkon) und nach unten, waagrechter und schiefer Wurf, schief nach oben und (seit 11.10.2026,
  \(\alpha < 0\), vom Turm) nach unten (Filter je Bewegung, «Gemischt»). Objekte ohne nennenswerten Luftwiderstand (Golfball
  statt Tennisball).
  \(y\) zeigt immer nach oben, auch beim freien Fall (Hinweis auf der Seite: die Themenseite misst dort nach unten).
  Platzsparend (ganzer Trainer auf einem Bildschirm; Muster für alle Trainer, HOWTO-werkzeuge §3; physikspezifisch, nicht nach Mathe übertragen): Aufgabe, Bewegung und Knöpfe in einer schmalen Spalte rechts
  (unter 640 px Breite des Trainers oben bzw. unten, Container-Abfrage); Szene, Auftrag und Eingabe in einer Karte neben der
  Skizze. Bezugssystem und Luftwiderstand stehen nicht im Aufgabentext, sondern am Achsenkreuz der Skizze (\(x\), \(y\), \(F_W = 0\)).
  Drei Aufgabenarten (Anker `#aufgabe-zuordnen`, `#aufgabe-stellen`, `#aufgabe-ablesen`): (1) zur beschriebenen
  Szene mit Skizze das passende \(y\)-\(t\)-, \(v_y\)-\(t\)-, \(a_y\)-\(t\)-, \(x\)-\(t\)-, \(v_x\)-\(t\)-Diagramm
  oder die Bahnkurve (1:1) wählen, die falschen je aus einer Fehlvorstellung (oben Halt, Betrag statt \(v_y\),
  \(a\) in Bewegungsrichtung, \(a = 0\), Wurf vergrössert \(a\), \(v_x\) nimmt ab, erst geradeaus und dann fallen,
  waagrecht länger in der Luft, Komponente vergessen, Fallweg statt Höhe …; Reserve: Wertefehler); (2) die Stelle
  im Diagramm oder auf der Bahn mit Punkten in gleichen Zeitabständen antippen (Scheitel, \(v_y = 0\), am
  schnellsten/langsamsten, wieder auf Abwurfhöhe, halbe Fallhöhe, halbe Flugzeit) oder «Nirgends»/«Überall gleich»
  wählen (\(a_y = 0\)? \(v_x\) am grössten?), Diagnose je typischer falscher Stelle; Tastatur: Pfeile, Eingabe;
  (3) Steigzeit, Steighöhe (Fläche), \(a_y\) (Steigung), \(v_y\) beim Aufprall, Fallhöhe (Fläche, \(h_0\) im Text
  verdeckt), Flugzeit, \(v_x\) und \(v\) im Scheitel aus den Punktabständen ablesen; Toleranz aus dem feinen Raster
  (`fwAchse`, dieselbe Rechnung wie beim Zeichnen), zu kleine Werte werden nicht gefragt. Szenen in `FW_SZENEN`,
  Rückmeldungen in `FW_DIAGNOSE`, `FW_STELLE`, `FW_ABLESEN`. Selbsttest `fwSelbsttest` über
  `scripts/verify_fall_und_wurf.js` im Pre-Flight (Ableitungen, Energie, Fläche unter \(v_y\) = \(-h_0\), Scheitel,
  Wurfweite, jede Lösung erfüllt ihre Frage, jede Diagnose greift, Pflichtdiagnosen je Ablesefrage). Testhaken
  `window.__fw` (u. a. `alleTexte(n)` für die MathJax-Prüfung). Ablesen auch Wurfweite und Betrag der
  Aufprallgeschwindigkeit. Anker mit Bewegung: `#aufgabe-<art>-<bewegung>` (z. B. `#aufgabe-stellen-schief`) setzt Aufgabe
  und Bewegung. Verweise je Aufgabenart: Themenseite 4.1 `#freier-fall`
  (Zuordnen) und `#wurfparabel` (Stellen, Ablesen, je mit `-schief`), Leitprogramm Kinematik Kapitel 4 (alle drei). Kein `localStorage`.
- `werkzeuge/formeln-umstellen.html` — Trainer Formeln umstellen (alle Lerngebiete, seit 11.10.2026), zwei
  Aufgabenarten (Anker `#aufgabe-schritte`, `#aufgabe-einsetzen`): Schritt für Schritt mit dem Waage-Prinzip
  (je Schritt die richtige Operation und falsche mit Diagnose: durch eine Summe geteilt, Nenner geteilt, Faktor
  abgezogen, Wurzel zu früh, Quadrat halbiert) und umstellen und einsetzen (vier Umstellungen, die falschen aus
  Kehrwert, Wurzel vergessen, Faktor, Teil, Summe; danach mit Zahlen, Diagnose über den Zahlenwert). Ein kleiner
  Algebra-Kern stellt jede Formel nach jeder Grösse um, die nur einmal vorkommt (Produkte mit Exponenten ±1, ±2,
  ±½, eine Summe); Formeln in `FU_FORMELN` (41, ~90 Aufgaben, drei Stufen), Grössen mit Einheit und Dimension in
  `FU_GR`. Selbsttest `fuSelbsttest` über `scripts/verify_formeln.js` im Pre-Flight (Einheiten jeder Formel,
  Lösung und jeder Zwischenstand mit Zufallszahlen in der Ausgangsformel, Einheitenprobe, Diagnosen).
  Die Umformung endet immer mit der gesuchten Grösse allein links (sonst tauscht der Trainer die Seiten selbst als
  letzte Zeile, ohne Frage — Entscheid des Auftraggebers 11.10.2026; erlaubte Umwege wie «:2» in einer Summe oder Wurzel
  zu früh gelten als gültig, ohne Fehlversuch, gelb «Erlaubt, aber ein Umweg»), damit die Zahlengleichung direkt anschliesst; die Einheitenprobe steht im selben Kasten
  rechts neben dem Ergebnis. Einsetzen: eine Kette x = Term = Zahlen mit Einheiten ≈ Ergebnis.
  Verweise: Themenseite 0.1 `#umformen`, Leitprogramm Rechnen Schritt 4. Kein `localStorage`.
- `werkzeuge/schaltungen-zusammenfassen.html` — Trainer Schaltungen zusammenfassen (6.2, seit
  10.10.2026), drei Aufgabenarten als Reiter: (1, Voreinstellung) Kurzformel
  aus Knöpfen setzen (Parser ohne Vorrang: + und ∥ auf einer Ebene brauchen eine Klammer; Vergleich
  über eine kanonische Form, Diagnose der innersten Gruppe, die es so nicht gibt), (2) zusammenfassen
  und zurückrechnen, links das Original, rechts der jeweilige Zwischenstand bis zum Ersatzschema, (3) Teilströme
  und Teilspannungen aller Widerstände bei gegebenem R_ges und I, Probe mit Kirchhoff
  (Knoten- und Maschenregel als Summe = 0), rechts das gefundene Ersatzschema, (4) Messen: Gerät
  (Voltmeter/Amperemeter) und Anschluss (in Reihe an einer Einsetzstelle `L.stellen` / parallel an zwei
  angetippten Knoten) wählen, ohne Prüfknopf: Steht alles fest, zeigt das Gerät seinen Wert, bei einem Fehler rot mit dem Wert, den es falsch angeschlossen zeigen würde (`szMessAnzeige`: Voltmeter 10 MΩ in der aufgetrennten Leitung, Amperemeter parallel mit 0.1 Ω; Kurzschluss der Quelle «OL»); Diagnosen Kurzschluss, Voltmeter im Stromweg, falsches Gerät, falsche Knoten,
  falscher Zweig. Welchen Strom eine Einsetzstelle misst, sagt `L.klasse` (in Reihe derselbe Strom wie die
  Gruppe darüber), auf den Schienen `summe` (Teilsumme der Zweige darunter, etwa \(I_2 + I_3\)); der Selbsttest gleicht jede Stelle mit der Knotenrechnung ab. Verweise je Aufgabenart einmal (Anker `#aufgabe-<art>` öffnet die Aufgabe): Themenseite 6.2 `#gemischt` (1–3) und `#messen` (4), Leitprogramm Elektrizität Kapitel 4 (Messen), 5 (zusammenfassen, Teilströme) und 6 (Kurzformel); Regel in `HOWTO-werkzeuge.md` §5. Jedes Bild trägt den
  Spannungspfeil der Quelle, der Gesamtstrom steht auf der Zuleitung, sobald er bekannt ist. Knoten sind
  von Anfang an gefärbt und tragen Buchstaben A, B, C … (`szKnotenMarken`, für Farbschwache); rechts in denselben Farben wie links (`szKnotenZuordnung`, über Bau und Potential;
  ein Knoten, den es links nicht gibt, bekommt eine eigene Farbe). In (2): zwei Widerstände antippen, «in Reihe» oder «parallel» wählen, Ersatzwiderstand
  eingeben, bis \(R_\text{ges}\) übrig ist; danach zurückrechnen bis zu einem Zielwiderstand, mit
  Proben. Knopf «Knoten färben». Stufe 1 = reine Reihe/parallel (RLP), Stufen 2 und 3 gemischt
  (weiterführend). Schaltungen als Baum in `SZ_VORLAGEN` (16 Bauformen), daraus Schaltbild,
  Knoten, erlaubte Schritte, Rückweg; Texte in `SZ_DIAGNOSE`. Richtig ist eine Eingabe auf 2 %
  am gerundeten **oder** am exakten Weg (Rundung über fünf Schritte summiert sich sonst über 1 %).
  Selbsttest `szSelbsttest` über `scripts/verify_schaltungen.js` im Pre-Flight: rechnet jede
  Schaltung unabhängig mit Knotenpotentialen nach (R_ges, jeder Rückwegschritt), «in Reihe» ⇔
  gleicher Strom und «parallel» ⇔ gleiche Knoten für jedes Paar in jedem Zwischenstand, jedes
  Fehlerbild bekommt seine Diagnose, Beschriftungen ohne Überlappung bei 280/300/380/1000 px,
  berührende Leitungen im selben Knoten. Testhaken `window.__sz`. Kein `localStorage`.
