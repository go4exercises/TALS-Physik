# Bauskripte: Leitprogramm Wärmeausdehnung und Gase

Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4) zur Themenseite 5.3, als Kopie von
`scripts/lp/hydrostatik/` entstanden (07.10.2026). Kopf, CSS-Gerüst, Grundskript, Bausteine und das Gerüst von
`seite.js` (Achsen, Bedienung, Aufgabenleiste, Uhr, Übungsrahmen, Minigrafen) sind wörtlich von dort; neu sind
fünf Kapitel, fünf laufende Simulationen, 15 Übungstypen, zehn Clips und der Gesamttest. **Freigeschaltet am 08.10.2026**
nach drei Prüfrunden (`/lp-pruefung`): Kachel in `leitprogramme.html`, Kasten «Lieber geführt» auf p5-3, im
Suchindex und in der Sitemap. Die alten Leitprogramme Wärmeausdehnung und Ideale Gase sind seither veraltet.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-ausdehnung.html` — Kopf, CSS, Grundskript, Kapitel, Aufgabenbilder; Laufzeiten der Clipkarten aus den Drehbüchern; aus der bestehenden Seite nur den SEO-Block | **ja**, für jede Änderung an Text, Aufgaben, Aufbau |
| `seite.js` | Seitenskript: sim1 Stab (Längenänderung über ϑ), sim2 Gefäss mit Steigrohr bzw. Würfel (ΔV über ΔT), sim3 Meeresschicht mit Pegel (Δh über ΔT), sim4 Gas im Zylinder (Zustand 1 → 2, p-V-Diagramm), sim5 isotherm/isobar/isochor (p-V, V-T, p-T); 15 Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die zehn Drehbücher `clips/p5-3-lp-*.json` erzeugt | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt `dauer`); späte Korrekturen (Läufer, Beschriftungen, `\dfrac`) stehen nur im JSON |
| `antworten.py` | setzt die Antwortbilder der fünf Kontrollclips (Kennung `antwort`) | ja, wiederholbar; danach `build-clips.py` |
| `aufnahme.json` | Aufnahmeplan der Simulationsbilder `clips/bilder/p5-3-lp-*.jpg` (Element `#simN > svg`, Testhaken `__sim.setze/zeige`) | `node .claude/tools/aufnahme-anim.mjs scripts/lp/ausdehnung/aufnahme.json` |

Testhaken `document.getElementById('simN').__sim.zeige(x)`: sim1 und sim2 Temperatur in °C, sim3 Erwärmung in K,
sim4 und sim5 Anteil des Wegs vom Zustand 1 zum eingestellten Zustand 2 (0 bis 1).

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/ausdehnung/seite.py
python3 scripts/build-seo.py                    # Footer und SEO-Kopf, nach jedem Bau
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-ausdehnung.html
python3 scripts/build-lp-pdf.py ausdehnung          # Gesamttest und Bewertungspaket
```

Clips: JSON bearbeiten → `build-clip-ton.py` (nur bei geändertem Sprechertext) → `build-clip-fragen-ton.py` →
`scripts/lp/kinematik/anker.py` → `build-clips.py` (Stimme `de_DE-thorsten-high`), danach `seite.py`.

## Planung (HOWTO §2)

**Kompetenzen** (RLP-BM 2030, 7.5.4.1 Gruppe 1, 5.3, wörtlich wie im Kompetenzblock der Themenseite):
K1 den Effekt der Wärmeausdehnung (linear und volumenbezogen) in Abhängigkeit von der Temperatur quantifizieren
(z. B. den Meeresspiegelanstieg aufgrund der Wassererwärmung berechnen) · K2 das Modell der idealen Gase anwenden,
um Druck-, Temperatur- und Volumenänderungen von Gasen zu berechnen, bei gleichbleibender Teilchenmenge.

**Kompetenzmatrix** (Hilfsmittel überall Taschenrechner und Formelsammlung):

| Kompetenz | Kapitel | Übungen | Kontrollclip | Aufgaben | Gesamttest |
|---|---|---|---|---|---|
| K1 linear | 1 Längenausdehnung | laenge, temperatur, alpha | kontrolle-laenge | 1a–1d | G1 (Diagramm) |
| K1 volumenbezogen | 2 Volumenausdehnung | volumen, volumen-fest, fuellen | kontrolle-volumen | 2a–2d | G2 |
| K1 Meeresspiegel (Beispiel des RLP), Dichte, Anomalie als Einordnung | 3 Wasser | dichte, meer, erwaermung | kontrolle-meer | 3a–3d | G3 (Diagramm) |
| K2 Zustand, Kelvin, absoluter Druck, allgemeine Gasgleichung | 4 | gas-p, gas-v, reifen | kontrolle-gas | 4a–4d | G4 |
| K2 isotherm, isobar, isochor | 5 | isotherm, isobar, fall | kontrolle-spezialfaelle | 5a–5d | G5 (Diagramm) |

**Planungstabelle**

| Kap. | Lernziel | Clip (vorgerechnetes Problem) | Simulation | Häufiger Fehler | min |
|---|---|---|---|---|---|
| 0 | Vortest: Zehnerpotenzen, Einheiten, Kelvin, Umstellen | — | — | — | 10 |
| 1 | Δl = α · l₀ · ΔT, Abkühlen, l = l₀ + Δl | Fernwärmeleitung 120 m, 10 → 90 °C: 115 mm | Stab, drei Werkstoffe | Temperatur statt Differenz; 10⁻⁶ | 45 |
| 2 | ΔV = γ · V₀ · ΔT, γ ≈ 3α, Flüssigkeiten | Kanister 20 l Ethanol, 8 → 38 °C: 0.66 l | Steigrohr / Würfel, vier Stoffe | α statt 3α; 10⁻³/10⁻⁶ | 45 |
| 3 | ρ = ρ₀/(1 + γΔT), Anomalie, Δh = γ · h₀ · ΔT | Ozean, obere 500 m +1.5 K: 15.8 cm | Meeresschicht mit Pegel | ganze Tiefe statt Schicht | 45 |
| 4 | p₁V₁/T₁ = p₂V₂/T₂, Kelvin, absoluter Druck | Fussball 0.9 bar Ü, 5.4 → 5.5 l, 12 → 42 °C: 1.06 bar Ü | Gas im Zylinder, p-V | Celsius; Überdruck | 45 |
| 5 | isotherm/isobar/isochor als Kürzung, Diagramme | Druckluftbehälter 6.0 bar, 15 → 55 °C: 6.83 bar < 7 bar | drei Fälle mit Diagramm | umgekehrt/direkt; 0 °C ≠ 0 K | 45 |
| ✓ | Gesamttest (PDF) | | | | 30 |

Summe 265 min ≈ 5.9 Lektionen. Clips: zehn, zusammen rund 13:20 min (Einführungsclips 1:47 bis 2:00 mit
vorgerechnetem Problem, Kontrollclips 0:35 bis 0:55 ohne die Wartezeit der Fragen) — etwas über der Zielgrösse
8 bis 12 min, wie die übrigen Kapitelmuster-Leitprogramme.

**Kern / Vertiefung / weggelassen.** Kern: je Kapitel Clip, Simulation, Übungen, Aufgaben a–c. Vertiefung: 1d
(Ring auf Welle), 2d (Gefäss dehnt sich mit), 3d (Boiler: γ von Wasser ist nicht konstant), 4d (Modellgrenzen),
5d (zwei Schritte = allgemeine Gasgleichung). Bewusst weggelassen (Themenseite): Bimetall, Eisberg und Schwimmen
von Eis (4.5), Normbedingungen und Masse einer Gasfüllung (der RLP verlangt gleichbleibende Teilchenmenge),
Flächenausdehnung.

**Reihenfolge.** Erst die allgemeine Gasgleichung (Kapitel 4), dann die Spezialfälle als Kürzung (Kapitel 5):
HOWTO §15 «erst das allgemeine Verfahren, dann die Abkürzung — mit ihrer Bedingung»; so steht es auch im Text
der Themenseite (Gasgesetz, dann «Die beiden Spezialfälle grafisch»). Die Anomalie steht als Einordnung im
Wasser-Kapitel neben dem Meeresspiegel, weil beides vom γ des Wassers handelt.

## Konventionen

- Formelzeichen wie Themenseite: α, γ (γ ≈ 3α), l₀, Δl, V₀, ΔV, h₀, Δh, ϑ in °C, T in K, p absolut.
- Koeffizienten der Themenseite: Stahl 12, Messing 18.4, Aluminium 23.8 (10⁻⁶ 1/K); Ethanol 1.10, Quecksilber
  0.18, Wasser (20 °C) 0.21 (10⁻³ 1/K). Einheit überall 1/K.
- **T = ϑ + 273.15 K** (Themenseite 5.1 und STYLEGUIDE §2.7), Luftdruck 1.0 bar (Themenseite: «≈ 1 bar»).
- Farben (Farbe = eine Bedeutung, Seite und Clips): Ausdehnung (Δl, ΔV, Δh) und neuer Zustand Bernstein (Clip 1),
  Temperatur Orange (2), Volumen Grün (3), Druck Rot (4), Ausgangszustand und Gefässe Tinte/grau gestrichelt (5).
  Clips ohne Blau, darum Druck auch auf der Seite Rot.

## Widersprüche auf der Themenseite 5.3 (gemeldet, nicht angeglichen)

1. **273 gegen 273.15:** Die Themenseite rechnet mit \(T = \vartheta + 273\) (A5: 283 K, 298 K; ❓ «293 K auf 586 K»;
   Animation 5 «293 K»), Themenseite 5.1 und STYLEGUIDE §2.7 mit 273.15. Das Leitprogramm nimmt 273.15; die
   Ergebnisse unterscheiden sich in der dritten Stelle nicht. Das Bewertungspaket lässt beides gelten.
2. **Zwei oder drei Spezialfälle:** «Grundbegriffe» spricht von «zwei Spezialfällen» (Boyle-Mariotte, Amontons),
   Lernziele, Mini-Check (2 l, 300 K → 600 K) und Clip `p5-3-gas-isobar` (Gay-Lussac) führen drei. Das Leitprogramm
   behandelt alle drei.
3. **Mini-Checks ohne Einheiten:** «\(12\cdot10^{-6} \cdot 10 \cdot 30 = 3.6\cdot10^{-3}\)» und ähnliche setzen
   Zahlen ohne Einheit ein (STYLEGUIDE §2.7); A6 rechnet mit «⇒»-Kette; «Alustange (α = 23·10⁻⁶)» weicht von der
   Tabelle (23.8) ab; α steht abwechselnd in K⁻¹ und 1/K.
4. **❓ an falscher Stelle:** Die Verständnisfrage zum See im Winter (4 °C) steht im Abschnitt «Volumenausdehnung»,
   vor dem Abschnitt «Anomalie», der den Stoff erst bringt (CLAUDE.md: am Ende des Abschnitts).

## Entscheide

- **Meeresspiegel:** Modell der Themenseite (γ = 0.21·10⁻³ 1/K konstant), aber mit erwärmter Schicht h₀ über
  unverändertem Tiefenwasser — damit die Wahl von h₀ eine Frage ist (Strategiefrage im Clip). Die Anomalie wird
  nicht aufs Meer übertragen (Meerwasser mit 35 ‰ Salz hat kein Dichtemaximum über dem Gefrierpunkt); Aufgabe 3d
  sagt nur, dass γ von Wasser mit der Temperatur wächst; im Clip steht «als Modell: γ wie bei zwanzig Grad».
- **Dichtekurve im Clip:** Fenster ohne ρ = 0 — gezeichnet wird ρ − 999.4 kg/m³, die Teilung nennt die echten Werte
  (Formel nach Kell, 0 bis 12 °C).
- **Simulationen** zeigen in der Formelzeile den Zustand im Bild (nach dem Lauf: Endzustand), Werte während des
  Laufs in ganzen Schritten (1 °C, 0.1 l, 5 °C in sim5). Regler mit höchstens 110 Schritten.
- **Zufallsübungen:** Wertelisten schliessen die festen Beispiele aus; `FEST` ist seit der Prüfung leer (die
  Velopumpe ist aus den Kontrollfragen verschwunden). Temperaturen werden auf 0.25 °C genau angenommen.
- **Gesamttest:** G1, G3, G5 am Diagramm (ablesen, rückwärts), G2 Messkolben mit V = A · h und Glas mit γ ≈ 3 · α,
  G3 mit Dichtefrage, G4 PET-Flasche vom Pass (allgemeine Gasgleichung, Temperatur ausrechnen), G5 isobar in °C und
  Manometer (Überdruck). Raster mit (E), (A), (W), (B), «ein Fehler, ein Abzug».

## Prüfung 07.10.2026: Befunde und Behebung

Drei Prüfagenten (Seite, Clips, PDFs) und ein Clip-Nachtrag. Quelle der Clips sind seither die **JSON-Drehbücher**
(`clips/p5-3-lp-*.json`); `clips.py` ist nur noch Archiv, veraltet und bricht seit Runde 2 beim Start ab. Antwortbilder: `antworten.py`.

**Seite**
- Sim 3 «grauer voriger Lauf»: `vorher` übernimmt den letzten fertigen Lauf (`letzter`), auch über Aufgabenwechsel.
- Doppelte Zahlen: 1c jetzt 3.0 m bei 50 K; 2c V₀ = 4.0 l (36 ml Hg); Kontrollfrage Volumen 4 «2 l bei 10 K → 22 ml»;
  Leiste Sim 5 Aufgabe 1 «auf 1.2 l» (2.5 bar); Leiste Sim 1 mit 30 m / 60 m (Rundung 17.85 entfällt).
- Festhalten K2: «bei Ethanol nur wenig, bei Quecksilber merklich (rund 13 %)». Sim 3 Aufgabe 5: Salzwasser-Grund
  statt Küstenform. «Fass … Es» je Gegenstand. Kelvin überall als T [K] = ϑ [°C] + 273.15. Dichtekurve 3c neutral.
  Übung «fall» isotherm: Paare mit p₂ ≤ 3 bar.
- Neu in 2a: Fadenhöhe h = ΔV/A gerechnet (übt G2b). Etiketten der Simulationen weichen Kurven und Rand aus
  (dreistufige Suche in `Achsen.etikett`); Schlauch in Sim 4 um die Achsenbeschriftung geführt; Bilder neu aufgenommen.

**Clips** (neu vertont mit Thorsten: laenge, volumen, meer, gas, spezialfaelle, kontrolle-meer, kontrolle-gas,
kontrolle-spezialfaelle; fragen-ton für alle zehn, anker für die fünf Einführungsclips, `ein` teils von Hand nach
`sprechzeiten.py`)
- Keine verratenen Antworten mehr: gas Vorgehen (Überdruck/p₁ in Schichten), spezialfaelle «V bleibt» an
  «sein Volumen bleibt», meer Problem/Vorgehen mit Skizze ohne h₀, Simulationsbild erst bei «h null ist».
- Ergebnisse mit dem Ton: Fussball-Lösung geteilt («≈ 2.06 bar», dann p_ü ≈ 1.06 bar), ΔT/h₀/p₁ einzeln verankert,
  Druckluft-Lösung: «Ventil bleibt zu.» und «Probe: T +14 %; p +14 %» getrennt. Manometertext zweizeilig.
- Absolut-/Überdruck eindeutig («7.0 bar (absolut)», kontrolle-gas F1 «1.2 bar (absolut)»); «Zeigt das Manometer
  zwei Bar, sind es absolut drei Bar» im Ton. Ideales Gas in Zustand, Merkbild und kontrolle-gas F3.
- Dichtekurve: Teilstrich 999.4, Bruchzeichen, Notiz «Achse beginnt bei 999.4 kg/m³» (meer und kontrolle-meer F2).
  «Über vier Grad steigt warmes Wasser …». Meer: «als Modell … γ wie für Wasser bei zwanzig Grad»; Szene Meer
  spricht 1500 m / 1 K.
- Neue Szenarien in Kontrollfragen: spezialfaelle F2 Kolbenprober 100 → 40 cm³ (2.5 bar), kontrolle-gas F2
  Drucksprühgerät (starrer Tank), kontrolle-meer F3 4200 m, kontrolle-meer F2 neu (kleinstes Volumen zwischen 8 °C
  und 0 °C) statt Wiederholung der Clipnotiz. Bleiben: Luftblase (gas F4, Entscheid) und Konservendose
  (spezialfaelle F1: ein starrer Behälter ist das Wesen von isochor, ein anderer Gegenstand wäre ein Umbau ohne Gewinn).
- Teilchen schwingen sichtbar (Doppelpfeile kalt klein, warm gross, «schwingen heftiger»); volumen: Aluminium und
  Quecksilber im Ton, Balken in Tinte, Achsenteilung 0.25/0.75 nicht mehr angeschnitten; Notizen isotherm/isobar/
  isochor an «heisst die Änderung …»; Isotherm-Punkte mit gleicher Rundung; «(288 K; 6.0 bar)» statt «15 °C»;
  Fussball-Etiketten ausserhalb, «(Grössen übertrieben)»; Strichpunkt in Probe-Notizen; Farben nach Bedeutung.
- Aussprache: Amontons, isochor und Anomalie klingen unsauber, **nicht** in `build-clip-ton.py` eingetragen
  (geteilte Tabelle, Hörprobe beim Auftraggeber). «Fernwärmeleitung» durch «Fernwärmerohr» ersetzt.

**PDFs** (beide neu gebaut, zwei Läufe, 25 Punkte)
- Geprüfte Kapitelziele ergänzt: G2c Glas mit γ ≈ 3 · α (0.12 mm³), G3c Dichte, G4d Temperatur aus der Gasgleichung
  (356 K ≈ 83 °C; geübt in Aufgabe 4c und Leiste Sim 4/5), G5d Manometer (0.25 bar Überdruck).
- G3 mit 1200 m / 400 m bei 2.5 K (63 / 21 cm auf Gitterlinien). G5b rechnet das Volumen bei −100 °C (1.27 l)
  statt den Nullpunkt zu extrapolieren; G5c nennt den Fall nicht mehr und das Raster listet die zulässigen Gründe.
  G1c liest die Temperatur zu −30 mm ab (−10 °C); G1d nennt die Einbautemperatur.
- Raster: Celsius-Fehler in G4 «Ansatz 0, Volumen folgerichtig», Regel für c) nach Folgefehler; G4 «fast viermal so
  grosses Volumen» entfällt mit der alten d); Gleichwertigkeiten (125 000 mm, cm-Rechnung, 273) auch in Abschnitt 3;
  Zeilenabstand je Zelle und `\addlinespace` (keine Brüche mehr an der Nachbarzeile); Schreibraum G1 8 Zeilen, G2 16.
- Die Selbsteinschätzung steht weiter allein auf Seite 6: Seite 5 ist mit G4 und G5 voll (`\needspace` jetzt 10).

### Runde 2 (08.10.2026)

**Seite**
- Verhältnis 2/5 → 2.5 bar stand viermal: Sim 4 Aufgabe 3 jetzt 0.5 l (4.0 bar), Sim 5 Aufgabe 1 jetzt 0.6 l
  (5.0 bar), Aufgabe 5b 1.6 bar (2.5 m³, Wasser 0.75 m), Kontrollfrage Spezialfälle 2 jetzt 100 → 80 cm³ (1.25 bar).
  Sim 5 Aufgabe 5 (war das Clipbeispiel 3 → 1.5 l) jetzt 1.2 bar → 2.5 l.
- 1c mit 4.0 m (4.8 / 2.4 mm); 2d mit 1.5 l und 25 K (41 ml; 2.7 ml; 38.6 ml läuft über).
- Volumenbeschriftung in Sim 4 fest unter dem Druckwert, in Sim 5 rechts oben unter p (nicht mehr am Kolben,
  Schlauch und Wasserbad); Sim 4: Isotherme und Legende zum Zustand im Bild (Zwischenbilder stimmen), x-Achse bis 4.9;
  Sim 5: Hyperbel endet vor «V [l]»; Sim 1 beim Abkühlen: Etikett unten rechts (dort ist das Diagramm immer frei).
- Sim 3 Aufgabe 5: Grund «Meerwasser ist salzig …» gestrichen (das kleine γ des Tiefenwassers kommt von der Kälte).
  Übung «fuellen»: Rückmeldung sagt «Gefäss».

**Clips** (neu vertont: kontrolle-meer, kontrolle-volumen, kontrolle-spezialfaelle; fragen-ton zusätzlich laenge)
- meer: «3700 m» innerhalb des Fensters (Anker start, unter dem Simulationsbild verdeckt); h₀ bei «fünfhundert»,
  γ und ΔT getrennt am Ton. gas: T₁/T₂ getrennt am Ton, p_ü und Manometer bei 18.3 s, Probe bei 20.8 s.
  spezialfaelle: Ventil-Etikett und Sonne am Ton, T₁/T₂ getrennt, «6.0 bar (absolut)». laenge: warme Reihe mit
  «schwingen heftiger» bei 1.5 s, Δl erst bei 4.9 s; «ΔT = 80 K» im Graf bei 4.3 s. volumen: Balken Aluminium und
  Quecksilber bei 14.6 s. Neue Ebenen sind eigene `graf`-Elemente ohne Achsen über demselben Rahmen.
- Strichpunkt statt Komma in allen Notizen, Graf-Texten und Formeln mit Wertepaaren (gas, meer, spezialfaelle,
  kontrolle-gas). Punkt «4 °C» in kontrolle-meer F2 Bernstein wie im Einführungsclip. laenge F1: «Rohr» statt «Leitung».
- Kontrollfragen ohne Zahlen aus dem Einführungsclip: kontrolle-meer F3 700 m / 1 K (14.7 cm; 300 m / 2 K wäre Leiste Sim 3 Aufgabe 1), kontrolle-volumen F4
  «3 l bei 10 K → 33 ml; 9 l bei 20 K?» (198 ml; Distraktoren 99 / 66 ml).
- Bilder aus den Simulationen neu aufgenommen (`aufnahme.json`).

**PDFs**
- G4: Celsius-Fehler nur einmal abgezogen, auch über d); c) folgerichtig aus dem eigenen b).
- G2 als Messkolben (250 cm³ Ethanol, Hals 0.80 cm², 4 K: 1.1 cm³; 14 mm; Glas 0.024 cm³) — Verfahren wie in 2a,
  anderer Gegenstand (Entscheid D3). G3: 1750 m / 750 m bei 2 K (73.5 / 31.5 cm auf 3.5-cm-Linien), keine Gerade aus
  Kontrollfragen oder Leisten. G1c verlangt dazu l = l₀ + Δl (124.97 m). Zuordnung: G5d auch Kapitel 4.
- Kelvin auch im PDF als T [K] = ϑ [°C] + 273.15; `\addlinespace` 6 pt; mehr Schreibraum bei G2 und G4.

### Runde 3 (Schlussprüfung, 08.10.2026)

- **M1:** Kontrollfrage Spezialfälle 2 war dieselbe Rechnung wie G5d; jetzt 100 → 75 cm³ (1.33 bar; Distraktoren
  0.75 bar Kehrwert, 0.33 bar Luftdruck abgezählt), neu vertont.
- **M2:** Raster G1c als (E): −10 °C und 124.97 m bzw. 124 970 mm; 125 m zählt hier nicht (Ausnahme von der
  Rundungsregel).
- **K4:** Kontrollfrage Volumen 4 jetzt «6 l bei 10 K → 66 ml; 18 l bei 20 K?» (396 ml; 198 / 132 ml), weil 3 l Ethanol
  und 99 ml die Leiste Sim 2 Aufgabe 5 sind; neu vertont.
- **N1:** Zwischenbild der Szene «Meer» bei 0.4 K (`meer-h1500-04.jpg`, 12.6 cm) statt 0.5 K (15.8 cm wäre die
  Lösung der Meer-Aufgabe).
- **N2/N3/K5:** am Ton: meer «Problem» (3700 m bei 4.0 s, +1.5 K bei 8.0 s), meer «Vorgehen» h₀ bei 5.2 s;
  spezialfaelle «Problem» (15 °C 4.0 s, 6.0 bar 5.3 s); laenge «Vorgehen» α bei 8.0 s, l₀ bei 10.4 s; Proben geteilt:
  gas «Probe: T +10 %; V +2 %» 21.4 s, «→ p +8 %» 25.3 s; spezialfaelle «Probe: T +14 %» 14.4 s, «→ p +14 %» 16.6 s;
  gas «absolut: 3 bar» 17.6 s.
- **K1:** Sim 3: Etikett «h₀ = … m; +… K» in dunkler Schrift; Lupenlinie über den Tiefenmarken geführt (Bilder neu).
  **K2:** Sim 5 zeigt V wie Etikett und Formelzeile (isotherm eine Nachkommastelle); volumen «Vergleich» 2.86 ml wie im
  Bild; 2d durchgehend 41.3 ml. **K3:** Sim 5 isotherm: x-Achse bis 7.1, «V [l]» bleibt bei 6 l frei.
