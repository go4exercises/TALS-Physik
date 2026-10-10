# Bauskripte: Leitprogramm Temperatur

Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4) zu Teilgebiet **5.1 Temperatur**,
als Kopie von `scripts/lp/hydrostatik/` entstanden (07.10.2026). Kopf, CSS-Gerüst, Grundskript, Bausteine
und das Gerüst von `seite.js` (Achsen, Bedienung, Aufgabenleiste mit Vergleichsantwort, Uhr, Übungsrahmen)
sind von dort; `Achsen()` hat zusätzlich `ya` (wie Energie) und schützt die Teilungszahlen einzeln, `etikett()`
nimmt bei lauter belegten Lagen die mit den wenigsten Konflikten. Neu sind vier Kapitel, vier Simulationen,
zehn Übungstypen, acht Clips und der Gesamttest. **Freigeschaltet am 08.10.2026** nach drei
Prüfrunden (`/lp-pruefung`): Kachel in `leitprogramme.html`, Kasten «Lieber geführt» auf p5-1, im Suchindex und in der Sitemap.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-temperatur.html` (Kopf, CSS, Grundskript, Kapitel, Aufgabenbilder); Laufzeiten der Clipkarten aus den Drehbüchern | **ja**, für jede Änderung an Text, Aufgaben, Aufbau |
| `seite.js` | sim1 Luftteilchen in der Box (mittleres Tempo über ϑ), sim2 drei Stoffe bei derselben Temperatur, sim3 Gasthermometer (Messpunkte, Gerade bis p = 0), sim4 Temperaturverlauf mit Celsius- und Kelvin-Achse; zehn Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die acht Drehbücher `clips/p5-1-lp-*.json` erzeugt; Bausteine (graf, Schienen, Thermometer, Zahlenstrahlen) für `antworten.py` | **nein** (`--neu` überschriebe die gemessenen Dauern); späte Änderungen im JSON |
| `antworten.py` | Antwortbilder der vier Kontrollclips (Kennung `"antwort": true`, wiederholbar) | nach Änderungen an Kontrollfragen, **danach** `achse_baender.py p5-1-lp-kontrolle-aggregat` |
| `achse_baender.py` | ersetzt in den Zustandsschienen die Achsen durch eine eigene Temperaturachse unten (die y-Achse bei 0 °C lief durch die Bänder) | nach `antworten.py` bzw. einem Neuschreiben von `p5-1-lp-aggregat` |
| `zeiten.py` | legt die Bewegung des Thermometerfadens (`_bahn`) im Clip `p5-1-lp-skalen` auf die Sprechzeiten; Teile in `strecken`, `punkte`, `texte`, `flaechen`, `figuren` mit `_anker`/`_aus_anker` bekommen `ein`/`aus` (Sprechzeit − 0.2 s) | nach jeder Neuvertonung von `p5-1-lp-skalen` und `p5-1-lp-teilchen`, nach `anker.py` |
| `aufnahmen.json` | Aufnahmeplan der Clipbilder (`node .claude/tools/aufnahme-anim.mjs scripts/lp/temperatur/aufnahmen.json`) | wenn sich eine Simulation ändert; jedes Bild ansehen |

Testhaken: `document.getElementById('sim1').__sim.zeige(ϑ, t)` (Teilchenlage allein aus der Zeit),
`sim2 … zeige(ϑ, t)`, `sim3 … zeige([[ϑ, 'A'|'B'], …], Bad ϑ, Gas, Gerade)`, `sim4 … zeige('tee'|'winter', t1, t2)`.

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/temperatur/seite.py
python3 scripts/build-seo.py                    # Footer und SEO-Kopf, nach jedem Bau
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-temperatur.html
# Clip: JSON bearbeiten, dann (Sprechertext geändert) build-clip-ton.py → build-clip-fragen-ton.py →
# scripts/lp/kinematik/anker.py <clip> → (skalen) zeiten.py → build-clips.py <clip>; danach seite.py
python3 scripts/build-lp-pdf.py temperatur
```

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-temperatur.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-temperatur.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-temperatur.html
node .claude/tools/pruef-fragen.mjs p5-1-lp-kontrolle-teilchen p5-1-lp-kontrolle-aggregat p5-1-lp-kontrolle-skalen \
     p5-1-lp-kontrolle-umrechnen p5-1-lp-teilchen p5-1-lp-aggregat p5-1-lp-skalen p5-1-lp-umrechnen
node .claude/tools/render-check.mjs leitprogramme/leitprogramm-temperatur.html
```

Lösbarkeit der Leisten (alle 20 Aufgaben der Reihe nach, über Regler, Knöpfe und Aktionen) beim Bau mit einem
Prüfskript bestätigt; keine Aufgabe ist beim Erscheinen gelöst.

## Planung

**Kompetenzen** (RLP-BM 2030, 7.5.4.1 Gruppe 1, wörtlich wie im Kompetenzblock der Themenseite):
K1 die Temperatur, mit Bezug auf die Teilchenbewegung, definieren und einen Zusammenhang mit den
Aggregatzuständen herstellen · K2 den Ursprung und die Anwendungen der Celsius- und der Kelvin-Temperaturskala
erklären · K3 Grad Celsius in Grad Kelvin umrechnen und umgekehrt.

**Kompetenzmatrix** (Hilfsmittel überall Taschenrechner und Formelsammlung):

| Kompetenz | Kapitel | Übungen | Kontrollfragen | Aufgaben | Gesamttest |
|---|---|---|---|---|---|
| K1 Teilchenbewegung | 1 | aussage, beobachtung | Kontrolle Teilchen 1–5 | 1a–1e | G1 |
| K1 Aggregatzustände | 2 | zustand, uebergang | Kontrolle Aggregat 1–5 | 2a–2e | G2 |
| K2 Ursprung, Anwendungen | 3 | eichen, nullpunkt, skala | Kontrolle Skalen 1–5 | 3a–3d | G3, G4 |
| K3 Umrechnen | 4 | umrechnen, differenz, faktor | Kontrolle Umrechnen 1–5 | 4a–4d | G5, G6 |

**Kapitel** (ein Kapitel = eine Idee; K1 trägt zwei Ideen und bekommt zwei Kapitel): 0 Vorwissen 10 min ·
1 Temperatur und Teilchenbewegung 45 · 2 Aggregatzustände im Teilchenbild 45 · 3 Celsius und Kelvin: Ursprung und
Anwendungen 45 · 4 Umrechnen und Temperaturdifferenz 45 · Gesamttest 30 = 220 min ≈ 4.9 Lektionen. Das Teilgebiet
ist klein; vier Kapitel statt fünf, jedes knapp eine Lektion.

**Roter Faden:** «Doppelt so viele Grad Celsius, doppelt so schnell?» stellt Kapitel 1 (Föhn, 20 → 80 °C: nur
rund 10 % schneller) und lässt es offen; Kapitel 3 beantwortet es mit dem willkürlichen Celsius-Nullpunkt und der
Proportionalität der mittleren Bewegungsenergie zur Kelvin-Temperatur; Kapitel 4 übt das Verhältnis in Kelvin.

**Kern / Vertiefung / weggelassen.** Kern: Definition über die mittlere Bewegungsenergie, Mittelwert, tiefste
Temperatur; Zustände im Teilchenbild, Übergänge, Schmelz- und Siedepunkt; Fixpunkte, Normaldruck, Extrapolation
des Gasdrucks, Kelvin-Skala, Anwendungen; Umrechnen, Differenz, Verhältnis in Kelvin. Zahlen zum mittleren Tempo
(Stickstoff, m/s) nur als Anschauung und zum Ablesen, nie als Formel. Weggelassen (Themenseite oder später):
latente Wärme und Heizkurve (5.2), Wärme gegen Temperatur (5.2), Gasgesetze (5.3), Wurzelgesetz des Tempos
(Themenseite 5.1, Häufiges Missverständnis), Fahrenheit (nicht im RLP; Mini-Check der Themenseite).

**Konventionen** wie Themenseite 5.1: ϑ in °C, T in K, `\,^\circ\text{C}`, `\;\text{K}`, 273.15, «Kelvin» ohne
«Grad» (der RLP-Wortlaut «Grad Kelvin» bleibt im Kompetenzblock, mit Hinweis), absoluter Nullpunkt
«Bewegung minimal». Umrechnung in der Schreibweise von STYLEGUIDE §2.7 (`T [K] = ϑ [°C] + 273.15`), wie die
Live-Zeile der Themenseite (Animation 3); der Festhalten-Kasten nennt die Kurzform der Themenseite.
Schmelz- und Siedepunkte (Normaldruck, gerundet): Wasser 0/100, Brom −7/59, Essigsäure 17/118 (wie Themenseite),
Ethanol −114/78, Quecksilber −39/357, Stickstoff −210/−196, Sauerstoff −219/−183, Zinn 232/2602, Blei 327/1749,
Eisen 1538/2862. Mittleres Tempo von Stickstoff: v = √(8RT/(πM)), M = 0.028 kg/mol (20 °C: 471 m/s).

**Farben** (Farbe = eine Bedeutung, Seite und Clips): Celsius-Temperatur Bernstein (1), Kelvin-Temperatur und
absoluter Nullpunkt Grün (3), Temperaturdifferenz Orange (2), Druck Rot (4), Teilchen, Kurven, Stoffe Tinte (5).

**Widersprüche und Auffälligkeiten der Themenseite 5.1** (gemeldet, nicht übernommen):
1. Drei Schreibweisen der Umrechnung: Merkkasten `T = ϑ + 273.15`, Mini-Check `T/K = ϑ/°C + 273.15`, Animation 3
   `T [K] = ϑ [°C] + 273.15`. Die Lösungen A1, A5 und die Mini-Checks rechnen `T = 37 + 273.15 = 310.15 K` —
   Zahlen ohne Skala, von STYLEGUIDE §2.7 ausdrücklich als ✗ geführt.
2. Differenzen in A2 und A6 ohne Einheiten eingesetzt (`95 − 12 = 83 °C`), gegen §2.7 (das sich auf p5-1 a4 beruft).
3. Absoluter Nullpunkt: «thermische Bewegung minimal» (Grundbegriffe) gegen «kommt praktisch zum Erliegen»
   (Abschnitt Teilchen) und «die Teilchen kommen zur Ruhe» (Worauf achten?, Animation 1). Leitprogramm: «minimal».
4. Mini-Check (Umrechnen, Transfer): Kelvin «vermeidet das negative Vorzeichen» bei Differenzen — falsch; eine
   Abkühlung hat auch in Kelvin ein negatives ΔT, so sagt es die Erkenntnis zu Animation 4.
5. Animationen 1 und 5 zeigen Tempo und Druck in Prozent (dimensionslose «Teile», Stilcheck-Regel 4).
6. Mini-Check «Beim Schmelzen bleibt die Temperatur konstant» gehört zu 5.2 (latente Wärme).

## Clips

| Clip | Dauer | Inhalt |
|---|---|---|
| `p5-1-lp-teilchen` | 2:15 | Brown'sche Bewegung (wachsender Weg, Stösse mal von links, mal von rechts), Definition, Mittelwert, kälter → langsamer, absoluter Nullpunkt; Problem Föhn 20 → 80 °C (517 m/s, knapp 10 %) |
| `p5-1-lp-kontrolle-teilchen` | 0:53 | ruhiges Glas, schnelles Einzelteilchen, Auto 35/70 °C, zwei verschlossene Gläser 10/30 °C, Abkühlen |
| `p5-1-lp-aggregat` | 2:30 | Eis, Wasser, Dampf als Bildfolge aus sim2; Übergänge, Sieden und Verdunsten; Anziehungskräfte; Schmelz- und Siedepunkte (Wasser, Ethanol, Glycerin) als Schienen; Problem Thermometerflüssigkeit Davos (Ethanol) / Backofen (Glycerin) |
| `p5-1-lp-kontrolle-aggregat` | 0:46 | Sauerstoff −200 °C, Zinn schmilzt, Gas zusammendrücken, Kerzenwachs, Blei und Eisen bei 1600 °C |
| `p5-1-lp-skalen` | 3:06 | Thermometer mit wanderndem Faden, Fixpunkte (Celsius 1742 umgekehrt, später gedreht), willkürlicher Nullpunkt; Gasthermometer aus sim3, Gerade bis −273.15 °C (ideales Gas); Kelvin; Anwendungen mit Säulen 150/300 K; Problem Messreihe (≈ −273 °C) |
| `p5-1-lp-kontrolle-skalen` | 0:51 | Eis als Fixpunkt, selbst gebautes Thermometer, zwei Gasthermometer, −20 K, 100 → 200 K |
| `p5-1-lp-umrechnen` | 2:17 | Doppelter Zahlenstrahl, 82 °C, 500 K, −12 °C, Differenz 15 → 65 °C, wann umrechnen; Problem Impfstoff 279.6 K |
| `p5-1-lp-kontrolle-umrechnen` | 0:48 | −25 °C, 93 K, Suppe 85 → 45 °C, wann umrechnen, Faktor −73 → 127 °C |

Zusammen 13:27 (etwas über den 8–12 Minuten aus STYLEGUIDE §6.5, wie bei den Mechanik-Leitprogrammen mit
vorgerechneten Problemen). Alle `probe: true`, Theme `begreifbar-schlicht`, Stimme `de_DE-thorsten-high`.
Bilder: `clips/bilder/p5-1-lp-*.jpg` (Aufnahmen aus sim1 bis sim3). Die Szene «Wann» im Umrechnen-Clip ist eine
Regel und steht ohne Bild.

## Prüfung 07.10.2026: Befunde und Behebung

`/lp-pruefung` (drei Prüfagenten: Seite, Clips, PDFs) am 07.10.2026; Entscheid des Auftraggebers: alle Befunde
beheben. Was geändert wurde:

- **Zeitanker in `p5-1-lp-skalen` und `-umrechnen`** waren nie gesetzt (Anker «im Alltag Celsius» klein, `anker.py`
  brach ab; bei umrechnen nie gelaufen). Anker korrigiert, `anker.py` je Clip einzeln mit Exit-Prüfung (teilchen 25,
  aggregat 29, skalen 44, umrechnen 25 Anker; keiner mehr auf Vorgabezeit), danach `zeiten.py`. **Lehre:** `anker.py`
  nie in einer `&&`-Kette über mehrere Clips; einzeln laufen lassen und die Zahl der gesetzten Anker ansehen.
- **Celsius-Geschichte:** 1742 setzte Celsius 0 beim Sieden und 100 beim Gefrieren; kurz nach seinem Tod umgedreht.
  So in Festhalten 3 und im Clip skalen; Kontrollfrage 1 fragt jetzt, warum schmelzendes Eis als Fixpunkt taugt
  (Ablenker «am dichtesten»: Wasser ist bei rund 4 °C am dichtesten).
- **Tempo gegen Bewegungsenergie:** Die mittlere Bewegungsenergie ist proportional zur Kelvin-Temperatur, das Tempo
  wächst langsamer (doppelte Kelvin-Temperatur → rund 41 % schneller; halbes Tempo bei einem Viertel der
  Kelvin-Temperatur). Nur als Aussage (Festhalten 1 und 3, Leiste sim1 Aufgabe 4, Clip skalen «Anwendungen»), kein
  Rechenstoff. Werte als Stickstoff ausgewiesen (Hauptteil der Luft); Kurve in Aufgabe 1b erst ab −190 °C.
- **Diffusion:** Übung «beobachtung» und Kontrollfrage 4 (teilchen) nur noch mit kurzer Strecke in ruhigem,
  geschlossenem Gefäss (Parfüm im Glaskasten, zwei verschlossene Gläser 10/30 °C).
- **Nullpunkt-Übung:** Messfehler ±0.1 %, Fixpunkte 0 bis 20 °C und 80 bis 100 °C, Toleranz 2 °C; −273 und −273.15
  werden mit eigener Rückmeldung («Das ist der Literaturwert …») angenommen. Übung «eichen»: Fadenstand ≥ 0.5 cm,
  Toleranz 0.2 wie in der Anleitung. Wirkungslose Einträge in `FEST` entfernt.
- **Kapitel 2:** Tabelle mit Ordnung (Kristall / ungeordnet), Anziehungskräfte (warum Schmelzpunkte vom Stoff
  abhängen), Sieden im ganzen Volumen, Verdunsten unterhalb des Siedepunkts — Festhalten und Clip aggregat.
  sim2 schwingt am Schmelzpunkt schwächer (Gitter neben Flüssigkeit erkennbar), Bild `aggregat-0` neu aufgenommen.
- **Kapitel 3:** Gültigkeit der Extrapolation (ideales Gas, solange es nicht kondensiert); Kelvin seit 2019 über die
  Boltzmann-Konstante (ein Satz).
- **Clips:** `rueck_sprich` überall ausgeschrieben; Quecksilber-Backofenthermometer durch Glycerin ersetzt
  (Hg-Thermometer in der Schweiz verboten); Kontrollfrage 5 (aggregat) mit Blei/Eisen statt der Werte des
  Einführungsclips; Stösse «mal von links, mal von rechts» als zwei Pfeilgruppen nacheinander; Kurve in Kontrollfrage 5
  (teilchen) endet vor dem Nullpunkt, Linie «Bewegung minimal»; Rückmeldung F1 (umrechnen) verrät den Weg nicht
  mehr; Formel `{-273.15}`; Lösung Impfstoff Δϑ = 1.55 °C, dann ΔT = 1.55 K; Bänderbilder ohne Kerben, gestrichelte
  Messlinien unterbrochen an den Zahlen. Alle acht Clips neu vertont (Thorsten) und gebaut.
- **Gesamttest Fassung 1.1** (25 P): G1 schematische Spuren (Faktor 1.6 statt 2.5) und neue Teilaufgabe zur
  Definition der Temperatur als Mittelwert; G2d Verdunsten von Ethanol statt Brom im Kolben; G3 y-Achse
  0.0075 cm/hPa, Ablesen folgerichtig zur eigenen Geraden (±12.5 °C), (E) in c) nur mit Rechnung, Kehrwert-Weg und
  Folgewert −3345 °C geregelt, d) Anwendungen der Skalen statt «nichts unter 0 K»; G4 mit vier Aussagen (Fixpunkte
  beider Art, Kelvin-Schritt); G6b Druckfaktor statt Fehlersuche. Bewertungspaket: Begriffsfehler (Celsius-Verhältnis)
  zählen je Aufgabe, Rechenfehler nur einmal; (E) ohne Einheit bei Zuordnungen; Differenz in °C zählt;
  Zahlenwertgleichung mit [K] zählt als Weg; Temperaturtoleranz ±2 K statt 2 %; jede (B)-Zeile mit Pflicht / genügt
  nicht / gleichwertig; K1 bis K3 erklärt.
- **Nicht in `build-clip-ton.py` eingetragen** (Entscheid: der Auftraggeber entscheidet nach Hörprobe): Aussprache von
  «Davos» und «Anders».

## Prüfung 08.10.2026 (zweite Runde): Restbefunde und Behebung

- **Nullpunkt-Übung:** Der Literaturwert (−273.15 °C, auch −273 °C) wird jetzt *vor* der Toleranzprüfung
  angenommen, mit Hinweis auf den Wert aus den eigenen Messwerten (vorher in 7 von 96 Fällen abgewiesen).
  c₁ = 0 °C entfernt (toter Eintrag); Fixpunkte jetzt 5 bis 20 °C und 80 bis 100 °C. Nachgeprüft mit 3000 Fällen:
  −273.15 und −273 immer angenommen, Ergebnisse −276.2 bis −271.0 °C.
- **Messpunkte von Hand eintragen:** neue Aufgabe 1e (Tempo-Tabelle von Stickstoff auf Papier eintragen, Kurve,
  bei 0 °C ablesen; Lösungsbild). Bewusst in Kapitel 1 und nicht in 3b: So bleibt G3 im Gesamttest keine Kopie
  von 3b.
- **Anziehungskräfte üben:** neue Aufgabe 2e (Ethanol flüssig, Wasser fest bei −50 °C; Kräfte gegen Bewegung,
  Folge für die Schmelzpunkte). Kapitel 1 und 2 je 15 P und 45 min.
- **Kleinigkeiten:** 454 statt 455 m/s (sim1 Aufgabe 2, Diagramm 1b); Vortest 0a ohne Verweis (nirgends im Repo
  wird Rechnen mit negativen Zahlen behandelt), dafür ein Hinweis zum Zahlenstrahl; Übung «beobachtung»: «im Lauf
  einiger Stunden», Rückmeldung «Niemand rührt — was bewegt sich trotzdem …».
- **Gesamttest Fassung 1.2:** G1b über das Bild («Woran erkennst du es?»); G3d prüft mit den Messwerten, ob der
  Druck zur Celsius- oder zur Kelvin-Temperatur proportional ist, und fragt, wann Celsius genügt (statt der Kopie
  von Aufgabe 3d); G4b ohne den Satz über die Skala; G4d ist jetzt richtig (15 K = 15 °C als Erwärmung); alle
  (B)-Zeilen von G4 mit Pflicht / gleichwertig / genügt nicht; Begriffsfehler einheitlich «G4a, G6a und G6b»;
  `\clearpage` vor Teil B (sonst stand der Teilkopf allein auf Seite 3). Halbleere Seiten dürfen bleiben.
- **Clips:** Ergebnisglieder auf das gesprochene Ergebnis geankert (umrechnen «Minus», «Differenz», «Lösung
  Impfstoff»; skalen «Lösung Messreihe»); skalen «Anwendungen»: Säulen mit «Von hundertfünfzig», 77 K als eigene
  Notiz mit dem Ton; aggregat «Lösung Thermometer»: Notizen und Zustandsmarken je mit dem gesprochenen Satz,
  «Merke» mit Anziehungskräften; teilchen «Stösse»: Satz verlängert, rechte Gruppe rund 5 s sichtbar, orange
  Ebene mit «stossen die Teilchen heftiger»; teilchen «Merke» mit «wärmer: im Mittel schneller»; Föhn und
  Kontrollfrage 3 sprechen und schreiben «Stickstoff» (Hauptteil der Luft); kontrolle-umrechnen F3:
  Δϑ = −40 °C, dann ΔT = −40 K, angezeigte Rückmeldung wie gesprochen; kontrolle-skalen F2 angezeigt wie
  gesprochen, F3 Beschriftung −273.15 °C links oben, frei von den Geraden. Neu vertont: alle ausser
  kontrolle-aggregat. Zeitmessung der Anker zusätzlich mit Piper (Sprechertext bis zum Anker), Abweichung
  höchstens rund 0.5 s.
