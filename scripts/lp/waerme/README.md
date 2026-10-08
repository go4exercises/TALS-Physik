# Bauskripte: Leitprogramm Wärme

Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4) zur Themenseite 5.2, gebaut am 07.10.2026
als Kopie des Gerüsts von `scripts/lp/hydrostatik/` (Kopf, CSS-Gerüst, Grundskript, Achsen, Bedienung,
Aufgabenleiste, Uhr, Übungsrahmen). Neu: sieben Fachkapitel und Kapitel 0, sieben laufende Simulationen,
22 Übungstypen, 14 Clips (sieben Einführungs-, sieben Kontrollclips), Gesamttest als PDF.
Status: **Erprobung, unverlinkt** — alle Clips mit `"probe": true`; Eintrag in `leitprogramme.html`,
`build-seo.py`, `build-suchindex.py` und Clip-Einbau macht die Koordination.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-waerme.html` — Kopf, CSS, alle Kapitel, Aufgaben samt Bildern, Gesamttest-Abschnitt. Laufzeiten der Clipkarten aus den Drehbüchern; aus der bestehenden Seite nur der SEO-Block. Lange Inline-Formeln in Lösungen bricht `teile()` an «=» und «≈» um (360 px). | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: sim1–sim7 und die 21 Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | **Quelle** der 14 Drehbücher `clips/p5-2-lp-*.json` (nach der Prüfung vom 08.10.2026 nachgeführt; die JSONs werden daraus erzeugt) | nur mit `--neu <clip>` und danach die ganze Kette unten — sonst fehlen Dauer, Anker und Antwortbilder. Späte Korrekturen hier machen, nicht im JSON |
| `antworten.py` | setzt die Antwortbilder der Kontrollclips (Kennung `"antwort": true`, wiederholbar) | nach `build-clip-ton.py`, vor `build-clips.py` |
| `teilanker.py` | legt `ein`/`aus` einzelner Teile eines `graf` (`_ein`, `_aus`, `_ein_versatz`) und Läuferbahnen (`_bahn`) auf den Sprechertext — Ergänzung zu `scripts/lp/kinematik/anker.py`, das nur ganze Elemente verschiebt. Mit `PIPER_MODELL` misst es die Wortzeit an einer Neusynthese (Satzanfang und ganze Szene) und überträgt sie per Abgleich (dynamische Zeitverzerrung über Bandenergien) auf die Tonspur und setzt auch die Elemente mit `_anker` neu (anteilig nach Zeichen lagen sie bis 1.6 s vor dem Wort, linear über die ganze Szene bis 1.8 s danach); rund 4 min je Einführungsclip | nach jeder Vertonung, nach anker.py |
| `aufnahme.json` | Aufnahmeplan der 18 Simulationsbilder `clips/bilder/p5-2-lp-*.jpg` für `.claude/tools/aufnahme-anim.mjs`. Abgeleitet, nicht im Plan (mit PIL übermalt, damit Werte erst mit dem Wort erscheinen): `treibhaus-25-modell.jpg` und `treibhaus-23-modell.jpg` = `treibhaus-25/-23` mit leerem Bodenbalken (ohne Bodentemperatur); `heizwert-a-leer.jpg` = `heizwert-a` ohne «0.8 kg», «η = 0.9» und «10.0 °C». (`heizwert-b.jpg` seit der dritten Prüfung gestrichen) | nur wenn sich eine Simulation ändert |
| `pruef_fest.py` | prüft, dass keine Zufallsübung eine feste Aufgabe (Clip, Kontrollfrage, Leiste, Kapitelaufgabe, Gesamttest, Themenseite) mit denselben Zahlen nachbaut | bei Änderungen an Aufgaben oder Übungspools |

## Ablauf

```sh
python3 scripts/lp/waerme/seite.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-waerme.html
python3 scripts/build-lp-pdf.py waerme          # Gesamttest und Bewertungspaket
```

Clip ändern (Stimme `de_DE-thorsten-high`):

```sh
export PATH=$HOME/.local/bin:$PATH PIPER_MODELL=/home/paps/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/lp/waerme/clips.py --neu p5-2-lp-<name>     # oder JSON direkt bearbeiten
python3 scripts/build-clip-ton.py p5-2-lp-<name>
python3 scripts/build-clip-fragen-ton.py p5-2-lp-<name>     # wenn sich eine Frage geändert hat
python3 scripts/lp/waerme/antworten.py                      # Kontrollclips
python3 scripts/lp/kinematik/anker.py p5-2-lp-<name>
PIPER_MODELL=… python3 scripts/lp/waerme/teilanker.py p5-2-lp-<name>   # nach anker.py, mit Stimme
python3 scripts/build-clips.py p5-2-lp-<name>
python3 scripts/lp/waerme/seite.py                          # Laufzeit der Clipkarte
```

Testhaken der Simulationen: `document.getElementById('simN').__sim` mit `zustand()`, `setze(o)`, `zeige(x)`:
sim1 zugeführte Wärme in kJ, sim2 Zeit in s (Ende 60 s = Gleichgewicht), sim3 Zeit in min, sim4 Anteil
0 bis 1 des Brennstoffs, sim5/sim7 ohne Zahl (Endzustand), sim6 Messung fertig.

## Prüfen (Stand 08.10.2026, alle grün)

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-waerme.html 2000   # 22 Typen × 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-waerme.html          # 7 Leisten
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-waerme.html
node .claude/tools/render-check.mjs leitprogramme/leitprogramm-waerme.html          # 1280 und 360 px
node .claude/tools/pruef-fragen.mjs p5-2-lp-waerme p5-2-lp-bilanz p5-2-lp-heizkurve p5-2-lp-heizwert \
     p5-2-lp-energiesysteme p5-2-lp-transport p5-2-lp-treibhaus p5-2-lp-kontrolle-waerme \
     p5-2-lp-kontrolle-bilanz p5-2-lp-kontrolle-heizkurve p5-2-lp-kontrolle-heizwert \
     p5-2-lp-kontrolle-energiesysteme p5-2-lp-kontrolle-transport p5-2-lp-kontrolle-treibhaus
SP=<ordner> node .claude/tools/pruef-clip.mjs clips/p5-2-lp-<name>.html 1 4 7 …   # alle 3 s
python3 scripts/lp/waerme/pruef_fest.py   # dazu Selbsttest: «eiswuerfel» erzeugt beide Fälle
```

`pruef-clip` meldet in den Einführungsclips Überlappungen ohne Namen: das sind die gestapelten Bilder einer
Bildfolge (jedes neue Bild deckt das vorige), wie in Hydrostatik; Text überlappt nirgends.

## Kapitel

| Kap. | Idee | Kompetenz | Simulation | min |
|---|---|---|---|---|
| 0 | Vorwissen: Celsius und Kelvin, Energie und Leistung, Wirkungsgrad, Gleichungen umstellen (Vortest 11 P) | — | — | 15 |
| 1 | Wärme ist übertragene Energie; \(Q = m \cdot c \cdot \Delta T\) | K1, K2 | sim1 Wärme zuführen (Teilchenpfeile, Thermometer) | 55 |
| 2 | Wärmebilanz, thermisches Gleichgewicht | K2 | sim2 Kalorimeter (Körper in Wasser, beide Kurven, \(Q_\text{ab}\)/\(Q_\text{auf}\)); Wasser nie über 100 °C | 55 |
| 3 | Latente Wärme, Heizkurve, Bilanz mit Zustandsänderung (Übung «eiswuerfel») | K2, K3 | sim3 Eis auf der Platte bis zum Verdampfen | 60 |
| 4 | Heizwert und Wirkungsgrad | K2, K4 | sim4 Kessel und Boiler (Heizöl, Erdgas, Pellets) | 55 |
| 5 | Energiesysteme vergleichen, Solarwärme | K5 | sim5 sechs Knöpfe (Biogas und WKK zusammen): Energiefluss, Halbjahre, Notiz | 55 |
| 6 | Wärmetransport | K6 | sim6 Schicht zwischen zwei Platten (Füllung, Lage, Oberfläche) | 50 |
| 7 | Durchlässigkeit, Treibhauseffekt | K7 | sim7 Einschichtmodell (Durchlässigkeit für Licht und Wärmestrahlung) | 55 |
| — | Gesamttest (25 P, PDF) | K1–K7 | — | 40 |

Summe 440 min ≈ 9.8 Lektionen, ohne die freiwilligen Vertiefungsaufgaben d). Geschätzt je Kapitel: Clips mit Fragen 7, Leiste 13, Festhalten 5, Übungen 17 (Kapitel 3 mit vier Übungen 23), drei Aufgaben 13 min. Der Gesamttest braucht bei sieben Kompetenzen rund 40 min (HOWTO \9 nennt rund 20 min für ein Leitprogramm mit drei bis fünf Kompetenzen); geschätzt nach Teilen 12 + 13 + 15 min. Kompetenzmatrix im Kommentar am Anfang der Seite (`seite.py`, `oben`).

## Entscheide

- **Mehr als fünf Kapitel:** sieben Kompetenzen, eine Idee je Kapitel. K2 ist auf vier Kapitel verteilt
  (ohne Zustandsänderung, mit Zustandsänderung, Wirkungsgrad); K5 und K7 beschreibend, aber mit
  nachgerechneten Grössenordnungen (Fläche für den Strom einer Gemeinde, Potential der Schweiz,
  −18 °C gegen 15 °C, Gegenstrahlung 150 W/m²).
- **Notation** wie Themenseite 5.2: \(Q\), \(m\), \(c\) in J/(kg·K), \(\Delta T\), \(\vartheta_\text{m}\),
  \(L_\text{f} = 334\) kJ/kg, \(L_\text{v} = 2256\) kJ/kg, \(c_\text{W} = 4182\), \(c_\text{Eis} = 2100\),
  \(\eta = E_\text{nutz}/E_\text{zu}\), COP \(= Q_\text{warm}/E_\text{el}\). Heizwert \(H\) (Themenseite hat kein Zeichen).
- **Heizwerte** wie Themenseite: Heizöl 42.6 MJ/kg (0.84 kg/l), Erdgas 50.0, Propan 46.4, Holzpellets 17.0,
  Buchenholz 15.0. **CO₂ je kWh** (Lebensweg): Medianwerte IPCC 2014 — Wind 11, Kern 12, Wasser 24,
  Photovoltaik (Dach) 41, Erdgas 490 g.
- **Einschichtmodell, eine Einstellung überall** (sim7, Festhalten, Clips, Aufgabe 7b, Übung «durchlaessig», G7):
  Sonnenlicht \(S = 240\) W/m² ganz zum Boden (\(D_L = 100\) %), \(23\) % der Wärmestrahlung direkt ins All: Boden
  14.9 °C (gemessen rund 15 °C), Abstrahlung 390 W/m², Gegenstrahlung 150 W/m². Überall steht «im Einschichtmodell»
  und dazu, dass die gemessene Gegenstrahlung rund 340 W/m² beträgt (die Atmosphäre nimmt auch Licht auf; der Boden
  gibt Wärme durch Verdunstung und aufsteigende Luft ab). CO₂ 280 → 430 ppm entspricht im Modell 25 % → 23 %:
  13.7 °C → 14.9 °C, +1.2 K wie gemessen seit vorindustriell. Formeln: \(U = S(1 + D_L)/(1 + D_W)\), \(T = (U/\sigma)^{1/4}\);
  (1; 1) → −18.1 °C.
- **sim6** rechnet die drei Wärmeströme zwischen zwei Platten (10 cm × 10 cm, 2 cm, 80 °C/20 °C) mit
  Tabellenwerten; Achse logarithmisch, sonst sieht man Strahlung und Leitung neben der Wasser-Konvektion nicht.
- **Clips:** Theme `begreifbar-schlicht`, Reihe «Wärme sehen». Farben: Bernstein Temperatur, Orange zugeführte
  Energie und Licht, Grün Nutzen, Rot Wärme (übertragen, abgestrahlt, Verlust), Tinte Wasser, Körper,
  Achsen (im Leitprogramm ist Wasser blau; das Theme hat kein Blau). Spektrum im Treibhausclip:
  normierte Planck-Kurven für 5800 K und 288 K über \(\log_{10}\lambda\), Maxima bei 0.50 µm und 10.1 µm.
- **Gesamttest** neu, keine Aufgabe aus `uebungstest-waermelehre` (Fassung 1.2 vom 08.10.2026): G1 Ethanol im
  Wasserbad (Wärme gegen Temperatur, Mischtemperatur: Kapitel 1 und 2, K2 ohne Zustandsänderung), G2 Eis in der
  Limonade (Bilanz mit Zustandsänderung, nicht alles schmilzt), G3 Heizkurve lesen und bis zum Verdampfen
  weiterzeichnen (K3: grafisch darstellen), G4 Campingkocher (Wirkungsgrad aus der Messung, Leistung), G5
  Biogas-WKK, G6 Solarkocher und Werkbank, G7 Temperatur aus der Abstrahlung und das Einschichtmodell (390, 240,
  150 W/m²) gegen die Wirklichkeit.
- **K5 im Gesamttest nur als Stichprobe (Entscheid):** G5 prüft Biogas, Wärme-Kraft-Kopplung und den Vergleich mit
  der Photovoltaik — Quelle oder Technik, Wirkungsgrad, Verfügbarkeit. Wärmepumpe, Wasserkraft, Wind, Kernenergie
  und das Potential prüfen Übungen («pv», «wasserkraft», «waermepumpe»), die Aufgaben 5a–5c und die Kontrollfragen
  von Kapitel 5. Eine zweite K5-Aufgabe sprengte die 40 Minuten; die Selbsteinschätzung schickt bei Punktverlust in
  G5 ins ganze Kapitel 5 zurück.
- **Bewusst weggelassen:** COP\(_\text{max}\) (Carnot), Messreihen der Treibhausgase, Energiebilanz der
  Erde (Leitprogramm Energie), Celsius und Kelvin als Stoff (5.1), Wirkungsgrade in Serie, Brennwert,
  Wärmedurchgang \(U\)-Wert, Wärmeleitungsgleichung (K6 verlangt Unterscheiden, nicht Rechnen).

## Widersprüche der Themenseite 5.2 (nicht behoben, Auftrag: nur melden)

- \(c_\text{W}\): 4182 J/(kg·K) im Text, 4180 in einem Mini-Check; STYLEGUIDE nennt 4.19 kJ.
- Mischtemperatur: \(\vartheta_\text{m}\) in der Definition, \(T_M\) in der Erkenntnis von Animation 2.
- Latente Wärme: \(L_\text{f}\)/\(L_\text{v}\) im Text, \(L_S\)/\(L_V\) in einem Mini-Check.
- «80°C» ohne Abstand in Mini-Checks.
- Heizwert und Energiesysteme haben keinen eigenen Abschnitt mit Anker, nur Definitionsblöcke; der Heizwert
  kein Formelzeichen.
- Clip `p5-2-energiequellen` sagt «sechs Wörter» und zählt sieben auf.
- Propan: Clip `p5-2-wirkungsgrad` 13 kWh/kg = 46.8 MJ/kg, Leitprogramm Heizen 46.4 MJ/kg (12.9 kWh/kg).
- Leitprogramm Heizen schreibt ε, \(Q_\text{ab}\), \(W_\text{el}\), die Themenseite COP, \(Q_\text{warm}\), \(E_\text{el}\).
- \(c_\text{Dampf}\): 2010 J/(kg·K) auf der Themenseite, 1870 im Leitprogramm Wärmemenge;
  `uebungstest-waermelehre` rechnet mit \(L_\text{f} = 333.8\) kJ/kg.
- Abschnitt `#treibhaus` sagt «mehr Wärme zurückgeworfen» (widerspricht der eigenen Erkenntnis: aufnehmen und
  wieder abstrahlen); der Transfer «Auto analog Treibhauseffekt» passt nicht dazu, dass beim Glas vor allem die
  Konvektion unterbunden wird (Aufgabe 7d).

## Prüfung 08.10.2026: Befunde und Behebung

`/lp-pruefung` (Seite, Clips Kapitel 1–4, Clips Kapitel 5–7, PDFs); Entscheide des Auftraggebers in Klammern.

- **Wasser über 100 °C** (sim2, Übung «abschrecken»): sim2 meldet «Das Wasser würde sieden: Das Modell gilt hier
  nicht» und taucht nicht ein, wenn die Mischtemperatur 100 °C erreichen würde; «abschrecken» würfelt nur Fälle unter
  90 °C. Regler für die Körpertemperatur in 5-°C-Schritten (Finger, 360 px); Leiste A4 auf 100 °C gelegt.
- **Bilanz mit Zustandsänderung:** neue Übung «eiswuerfel» (Kapitel 3; Diagnosen: Schmelzwärme vergessen,
  Schmelzwasser nicht miterwärmt, Ergebnis unter 0 °C = nicht alles Eis schmilzt) und Gesamttest G2. Der Anteil
  «Eis bleibt übrig» stimmte erst nach der zweiten Prüfung (siehe dort).
- **Einschichtmodell** (eine Einstellung, CO₂ realistisch): siehe «Entscheide». Bilder `treibhaus-23/25` neu,
  `treibhaus-20/26/40` gelöscht.
- **G3 zeichnen lassen** (K3): Zeitachse bis 40 min, Messung bricht bei 12 min ab; Rechnung und Zeichnung je ein
  Punkt, dazu ein Ablesepunkt (A).
- **Ergebnisse im Clip erst mit dem Ton:** alle gemeldeten Stellen auf das Ergebniswort gelegt (Notizen geteilt,
  Teile mit `_ein`), «Messen» in Kapitel 6 gestrichen (nahm die Leisten A1–A3 vorweg).
- **Doppelte Beispiele:** neue Kontrollfragen (Thermometer im Tee, Granit, Kupfer im Wasser, 0.5 kg gefrieren,
  0.3 kg Eis von −8 °C, 54 MJ, Sonnenkollektor, Windturbine, Wärmebildkamera, Kupferboden), Leiste sim1 A2
  (0.80 kg, 25 kJ), sim5 A6 (COP 4.0), sim6 A5 (ohne Thermoskanne), Aufgaben 4a/4b neu (Pellets statt Öl mit
  Lagerplatz; Wirkungsgrad eines Boilers rückwärts), G4/G6/G7 neu.
- **Solarwärme:** Sonnenkollektor in Tabelle und Festhalten von Kapitel 5, in der Übung «pv» (ein Drittel der
  Fälle) und in der Kontrollfrage 2.
- **Zeit:** Vertiefungsaufgaben d) als «freiwillig» markiert und aus der Zeit genommen; Kapitel 5 um die
  Speichersee-Rechnung der Leiste gekürzt (steht als Übung «wasserkraft»); Zeiten neu geschätzt (440 min).
- **Kleinere:** Pronomen in «waermemenge», «erwaermung», «abstrahlung»; Kontext und Temperatur in «mischen»
  gekoppelt; «heisses Wasser» in «mischen-rueck» mindestens 45 °C; Indizes heiss/kalt; Wirkungsgrade je Brennstoff;
  kJ-Diagnose in «wasserkraft»; negatives Vorzeichen in «latent» angenommen; Wachs-Plateau auf 60 °C; Heizstab →
  «Boiler mit Heizstab» (Verlust an die Umgebung); Kontrollheizkurve mit Eis doppelt so steil und Plateau 3.2 min;
  Rettungsdecke eindeutig; Farben (Temperatur Bernstein, kalte Platte grau, zweite Temperaturkurve gestrichelt);
  «hellen Flächen» nur gegen Sonnenlicht; sim5-Formel in Zehnerpotenz; Rundung in sim1; Vulkan → Russ;
  Achsentitel und Pfeilspitzen in Clips; Bewertungspaket mit Pflichtaussagen, (A)/(S), «folgerichtig» in G3 b,
  ohne widersprüchliche Einheiten-Gleichwertigkeiten; Zeilenumbrüche der Anleitung.
- **Nicht behoben:** «Heiss heisst nicht viel Wärme» steht weiter im Festhalten (Glas gegen Becken) und in Aufgabe 1a
  — die Kontrollfrage dazu ist ersetzt; die beiden verbleibenden Stellen haben verschiedene Rollen (Merksatz,
  Übungsaufgabe). Die Widersprüche der Themenseite bleiben (Auftrag: nur melden), ergänzt um «mehr Wärme
  zurückgeworfen» (#treibhaus) und den Auto-Vergleich gegen Aufgabe 7d.

## Zweite Prüfung 08.10.2026: Befunde und Behebung

- **«eiswuerfel» erzeugte nie «alles schmilzt»** (H1): `tm` stand doppelt in der Liste der Fehlerwerte, darum
  scheiterte `verschieden()` immer. Zeile gestrichen; heute rund 26 % «Eis bleibt übrig». `pruef_fest.py` prüft
  das als Selbsttest (Liste `FAELLE`) und liest jetzt auch die `text:`-Zeilen der Leisten.
- **Festhalten 7** (M1): «23 % statt 25 %», dazu «etwa so viel, wie sich die Erde erwärmt hat» (wie Leiste und Clip).
- **«Eis bleibt übrig» eingeführt** (M2): Prüfschritt und Beispiel im Festhalten 3 (0.15 kg Wasser von 10 °C,
  0.10 kg Eis: 0.019 kg schmelzen, 0.081 kg bleiben), dazu ein Satz unter «Häufiger Fehler».
- **Gesamttest 1.2:** G1 b Mischtemperatur (Kapitel 2 wieder im Test), G2 mit 0.25 kg (0.063 kg geschmolzen gegen
  0.037 kg übrig, vorher zufällig beide 0.050 kg), G3 mit 0.40 kg (nicht wie Leiste sim3 A1), G4 Campingkocher
  (nicht wie Übung «heizwert»), G7 a fragt jetzt auch, was die Gase mit der Strahlung tun, G7 c mit 390/240/150.
  Raster: Ansatz in G2 ist der Wegpunkt zu a), G3 c Rechnung zählt die Dauer, Zeichnung den Endpunkt (auch ab
  Minute 12 = 0), G6 a und G1 a mit eindeutigem «nötig», G7 b in Grad Celsius verlangt.
- **Geübt, was G6 b und G7 b verlangen:** «fühlt sich kälter an» im Festhalten 6 und als Aufgabe 6a (d);
  Übung «abstrahlung» zur Hälfte rückwärts (Temperatur aus \(P/A\)), Formel dazu im Festhalten 7.
- **Clips:** gegebene Werte und Ergebnisse Zeile für Zeile auf ihr Wort (Notizen geteilt, Skizzentexte mit `_ein`);
  `teilanker.py` legt alle Anker nach einer Neusynthese des Satzanfangs (vorher anteilig nach Zeichen, bis 1.6 s zu früh);
  «Gegenstrahlung» zeigt eine Skizze ohne Zahlen statt des sim7-Bilds (das nahm 390/150 des Problems vorweg);
  «Mehr Kohlendioxid» zeigt zuerst die ppm-Balken, dann das Modellbild ohne Bodentemperatur, die Temperaturen erst
  mit dem Wort; Lieferung grün (wie die Simulation), Wind gestrichelt; Merkbilder vollständig; leere Bühnen in
  «Strom» und «Lösung Topf» gefüllt; 1380 MJ ohne Ton entfernt, 593 kg mit Notiz; H der Pellets gesprochen.
  sim7: Wattzahlen ganzzahlig (90 statt 89.8), obere Beschriftung neben dem Pfeil.
- **Kleineres:** «je Kilogramm und Kelvin» (sim2, Aufgabe 2), sim4 «17.0 MJ/kg», sim6 «rund 5 W»,
  Halbsatz zum Sieden an der Berührfläche in sim2, Sonnenkollektor «höchstens rund 550 kWh», Aufgabe 4c mit
  η = 0.80 (nicht wie Kontrollfrage 1), «durchlaessig» mit im Modell stimmigen Paaren, Zeitangabe im Kopf.

## Dritte Prüfung 08.10.2026: Befunde und Behebung

- **Gerundete Ergebnisse abgewiesen:** «eiswuerfel» nimmt jetzt ±max(0.15 K, 1.2 %) an (auf 0.1 °C gerundet und mit
  dreistelligen Zwischenwerten gerechnet); der Generator würfelt nur Fälle, in denen jeder Fehlerwert mindestens das
  2.5-Fache davon entfernt liegt. «abstrahlung» rückwärts: ±0.6 K (T auf ganze Kelvin gerundet). `pruef_fest.py`
  prüft beides als Rundungstest (gerundete Eingaben angenommen, Fehlerwerte aus `fehler()` abgewiesen).
- **G6 b** fragt jetzt nach dem Holzgriff der Pfanne mit gegebenen Wärmeleitfähigkeiten (nicht wie Aufgabe 6a);
  **G4** mit 2.0 l Wasser von 12 °C, 30 g Butan in 8.0 min (736 kJ, 1371 kJ, η = 0.54, 2.86 kW), nicht wie das
  Clip-Problem «Topf». Gesamttest Fassung 1.3.
- **Aufgabe 6a:** Teile (1)–(4), 4 P (Kapitel 6 jetzt 13 P); (4) verlangt zwei Sätze.
- **Bewertungspaket:** Abstände an den Brüchen (G1 b, G3 a/c, G4 b/c) mit `\par\vspace` bzw. Strut. Die
  Selbsteinschätzung steht weiter allein auf Seite 6 (Entscheid): Der Abschnitt ist eine Tabelle von rund 13 Zeilen,
  die sich nicht teilen lässt, und auf Seite 5 bleiben nach G6 und G7 rund 15 % frei. Kürzen hiesse Raster von G6/G7
  zusammenstreichen; eine fast leere Schlussseite schadet dagegen nicht.
- **Übung «pv»:** Sonnenkollektor mit η 0.40 bis 0.50 (wie «rund 50 %» der Tabelle); die Tabelle nennt den Bezug
  (1100 kWh Sonnenlicht je m²).
- **Clips:** `teilanker.py` gleicht die Neusynthese per dynamischer Zeitverzerrung mit der Tonspur ab (vorher eine
  lineare Umrechnung über die ganze Szene, die in langen Lösungsszenen bis 1.8 s nachlief; eine stückweise Umrechnung
  nach Sprechpausen lag bis 5 s daneben und wurde verworfen); alte Ausgleichsversätze entfernt (Sieben
  Systeme, Heizwert). «Lösung Topf»: Rechnung und Ergebnis je auf eigener Zeile (Umbruch vor dem Gleichheitszeichen),
  die Rechnung erscheint, während sie gesprochen wird. «Wirkungsgrad»: zuerst Bild ohne Werte, die Werte mit dem
  Wort, 40/36 MJ zusammen mit dem Endbild. «Mehr Kohlendioxid»: Modellbild 23 % (ohne Bodentemperatur) zur Notiz
  «Modell heute». «Problem Hand»: «2 m» mit dem Wort, «Wasser 55 °C» gestrichen. «Boiler mit Heizstab» ohne Komma.
  Farben: Photovoltaik grün (auch Kontrollfrage 3), Wind Tinte (gestrichelt heisst nur noch Bedarf).
