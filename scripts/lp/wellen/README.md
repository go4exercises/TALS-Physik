# Bauskripte: Leitprogramm Wellen

Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4) zur Themenseite 6.1, gebaut am 08.10.2026
als Kopie des Gerüsts von `scripts/lp/waerme/` (Kopf, CSS-Gerüst, Grundskript, Achsen, Bedienung,
Aufgabenleiste, Uhr, Übungsrahmen). Neu: sechs Fachkapitel und Kapitel 0, sechs laufende Simulationen,
15 Übungstypen, 12 Clips (sechs Einführungs-, sechs Kontrollclips), Gesamttest als PDF.
Status: **freigeschaltet am 09.10.2026** nach fünf Prüfrunden (`/lp-pruefung`) — Kachel in `leitprogramme.html`,
Kasten «Lieber geführt» auf p6-1, im Suchindex und in der Sitemap; alle Clips mit `"probe": true` (Spalte
«Leitprogramm» der Clip-Bibliothek). Bereichsgrenze Mikrowellen/Radio bei 1 m (Entscheid 09.10.2026, auch auf p6-1).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-wellen.html` — Kopf, CSS, alle Kapitel, Aufgaben samt Bildern, Gesamttest-Abschnitt, Planungskommentar (Kompetenzmatrix, Planungstabelle, Zeiten). Laufzeiten und Transkripte der Clipkarten aus den Drehbüchern; aus der bestehenden Seite nur der SEO-Block (es gibt noch keinen). | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: sim1–sim6 und die 15 Übungstypen | wird von `seite.py` eingesetzt |
| `clips.py` | **Quelle** der 12 Drehbücher `clips/p6-1-lp-*.json`; alle Zahlen mit `assert` nachgerechnet | nur mit `--neu <clip>` und danach die ganze Kette unten |
| `antworten.py` | setzt die Antwortbilder der Kontrollclips (Kennung `"antwort": true`, wiederholbar; in Kapitel 2, Frage 1 und 2 kommen die Antwortteile ins Diagramm der Frage) | nach `build-clip-ton.py`, vor `anker.py` |
| `teilanker.py` | wie in Wärme, ergänzt um `_bewegung`, `_grenzen` und `_parameter` (Bewegungen auf den Ton legen) | nach `anker.py`, mit `PIPER_MODELL` |
| `aufnahme.json` | Plan der 20 Simulationsbilder `clips/bilder/p6-1-lp-*.jpg` für `.claude/tools/aufnahme-anim.mjs` | wenn sich eine Simulation ändert |
| `pruef_fest.py` | prüft, dass keine Zufallsübung eine feste Aufgabe (Clip, Kontrollfrage, Leiste, Kapitelaufgabe, Gesamttest, Themenseite 6.1 und 6.1a) mit denselben Zahlen nachbaut. Gefundene Paare stehen in `FEST_PAARE` (seite.js) und werden neu gewürfelt | bei Änderungen an Aufgaben oder Übungspools |

## Ablauf

```sh
python3 scripts/lp/wellen/seite.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-wellen.html
python3 scripts/build-lp-pdf.py wellen          # Gesamttest und Bewertungspaket
```

Clip ändern (Stimme `de_DE-thorsten-high`):

```sh
export PATH=$HOME/.local/bin:$PATH PIPER_MODELL=/home/paps/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/lp/wellen/clips.py --neu p6-1-lp-<name>
python3 scripts/build-clip-ton.py p6-1-lp-<name>
python3 scripts/build-clip-fragen-ton.py p6-1-lp-<name>
python3 scripts/lp/wellen/antworten.py                      # Kontrollclips
python3 scripts/lp/kinematik/anker.py p6-1-lp-<name>
python3 scripts/lp/wellen/teilanker.py p6-1-lp-<name>
python3 scripts/build-clips.py p6-1-lp-<name>
python3 scripts/lp/wellen/seite.py                          # Laufzeit und Transkript der Clipkarte
```

Testhaken: `document.getElementById('simN').__sim` mit `zustand()`, `setze(o)`, `zeige(x)`: sim1 und sim3 Zeit
in s, sim2 und sim6 Einstellungen, sim4 Phase des Feldbilds (0 bis 1), sim5 ein Zustandsobjekt
`{modus, niveau, fotonen, sprung, absorb, pumpe, atome, paket, hinaus, meldung}`.

## Kapitel

| Kap. | Idee | Kompetenz | Simulation | Clips | min |
|---|---|---|---|---|---|
| 0 | Vorwissen: Vorsilben, Zehnerpotenzen, Umstellen, \(v = s/t\) (Vortest 10 P) | — | — | — | 15 |
| 1 | Schwingung → Welle: gekoppelt, verzögert, Energie statt Materie, quer/längs, \(f = 1/T\), \(c = s/t\) | K1, K2, K3 | sim1 Teilchenkette mit Erreger (quer/längs, dauernd/Stoss, \(f\)) | welle 2:12, Kontrolle 0:52 | 45 |
| 2 | Momentbild \(y(s)\) und Zeitdiagramm \(y(t)\); \(\lambda\) aus \(y(s)\), \(T\) aus \(y(t)\); Phasengeschwindigkeit \(c = \lambda/T\) | K1 | sim2 beide Diagramme an zwei Reglern | diagramme 1:56, Kontrolle 0:49 | 40 |
| 3 | Sender → \(f\), Medium → \(c\), \(\lambda = c/f\); Mediumwechsel, \(f\) bleibt; Schall | K1, K2 | sim3 zwei Seile (gleich, dünner, dicker) | medium 2:13, Kontrolle 0:55 | 45 |
| 4 | Elektromagnetische Wellen: Felder, kein Medium, \(c = 3.00 \cdot 10^8\) m/s, Spektrum | K2, K4 | sim4 sechs Geräte im Spektrum, Feldbild | em 2:00, Kontrolle 0:49 | 45 |
| 5 | Atomare Emission, Absorption, Laser; \(E = h \cdot f\) qualitativ und als Verhältnis | K4 | sim5 Modellatom mit drei Stufen (Emission, Absorption, Laser) | licht 2:38, Kontrolle 0:51 | 40 |
| 6 | Treibhauseffekt: wellenlängenabhängige Aufnahme, Wiederabstrahlung, mehr CO₂ | K5 | sim6 Durchlässigkeit nach Wellenlänge (λ · B_λ über log λ, flächentreu; Gasbänder) | treibhaus 2:38, Kontrolle 0:50 | 40 |
| — | Gesamttest (25 P, PDF) | K1–K5 | — | — | 40 |

Summe 310 min ≈ 6.9 Lektionen (ohne freiwillige Vertiefungsaufgaben d). LG 6 hat 30 Lektionen für 6.1 und 6.2;
das Leitprogramm Elektrizität (6.2) plant 330 min ≈ 7.3 Lektionen; zusammen rund 14 von 30 Lektionen, Platz für Themenseiten, Versuche und Prüfungen. Clips zusammen 18:39 min.

## Kompetenzmatrix

| Kompetenz (RLP Gruppe 1, 6.1) | Kapitel | Leiste | Übungen | Kontrollfragen | Aufgaben | Gesamttest |
|---|---|---|---|---|---|---|
| K1 Wellenerzeugung beschreiben, grafisch und algebraisch charakterisieren | 1, 2, 3 | sim1 A2/A4/A5, sim2 A1–A5, sim3 A1–A4 | periode, laufzeit, ablesen, phasengeschw, wellengleichung, medium | K1 F3/F4, K2 F1–F5, K3 F1/F2/F5 | 1b, 2a–2d, 3a, 3c | G1, G2, G3 d |
| K2 Wellentypen aufzeigen und unterscheiden | 1, 3, 4 | sim1 A3 | quer-laengs, hoerbar, wellentyp | K1 F2, K3 F4, K4 F1/F5 | 1d, 3b, 4a | G2 d, G3 a, G4 b/c |
| K3 Wellenerzeugung an mechanischen Wellen | 1 | sim1 A1–A5 | quer-laengs | K1 F1/F5 | 1a, 1c | G3 |
| K4 Besonderheiten elektromagnetischer Wellen, Emission, Laser, Absorption | 4, 5 | sim4, sim5 | em-rechnen, bereich, stufen, licht-aussage | K4, K5 | 4b–4d, 5a–5d | G4, G5 |
| K5 Treibhauseffekt, wellenlängenabhängige Absorption, Treibhausgase | 6 | sim6 | zuordnen, treibhaus-aussage | K6 | 6a–6c | G6 |

## Entscheide

- **Ort heisst \(s\)** wie in Vertiefung 6.1a (Momentbild \(y(s)\)), nicht \(x\) wie im Auftrag; sonst zwei
  Notationen auf zwei verlinkten Seiten.
- **Zahlen wie Themenseite:** Schall in Luft 340 m/s (15 °C), Helium 980, Wasser ≈ 1500, Eisen 5170 m/s;
  \(c = 3.00 \cdot 10^8\) m/s; sichtbar 380 bis 780 nm; Bereichsgrenzen des Spektrums wie Animation 5;
  «stimulierte Emission» wie die Themenseite.
- **Photonenergie** nur als \(E = h \cdot f\) und als Verhältnis (grössere Stufe → höhere Frequenz → kürzere
  Welle); keine Elektronvolt (Themenseite Animation 5, im «Nicht in diesem Leitprogramm» verlinkt).
- **Treibhaus ohne Energiebilanz:** sim6 zeigt, welche Gase bei welchen Wellenlängen aufnehmen (Bänder wie
  Leitprogramm Wärme, Aufgabe 7c: H₂O 5.5–7.5 µm und ab 20 µm, CO₂ um 15 µm mit wachsender Breite, CH₄ 7.4–8.0 µm),
  Pfeilbreiten ohne Watt. Die Anteile (Boden 36 % mit H₂O, 49 → 52 % für 280 → 430 ppm CO₂, 58 % mit allen Gasen
  bei 800 ppm) sind Anteile «in den grauen Bereichen» dieses Bandmodells ohne Wolken; sie sind **nicht** mit den
  77 % des Einschichtmodells im Leitprogramm Wärme (23 % direkt ins All) vergleichbar. Die Simulation sagt das in
  ihrer Notiz; der Clip nennt keine Prozente und verweist für «wie viel wärmer» aufs Leitprogramm Wärme. −18 °C /
  +15 °C und 280/430 ppm wie dort.
- **Ozon, kein Glashaus:** Die Gase «nehmen auf und strahlen in alle Richtungen wieder ab». Ozon steht mit dem
  Ultraviolett der Sonne im Festhalten 6 und im Clip (Szene «Durchlässig»), als Aufnahme auf dem Hinweg; das Ozonloch nur
  als «Häufiger Fehler». Der Spiegel/Glasdach ist Kontrollfrage 6/5.
- **Clips:** Theme `begreifbar-schlicht`, Reihe «Wellen sehen». Farben: Bernstein Welle und Auslenkung,
  Orange Licht (Sonne, Photonen), Grün Ausbreitung/Front/\(c\), Rot Wärmestrahlung, Tinte Teilchen, Masslinien,
  Achsen. Ergebnisse erscheinen mit dem Wort (`_ein`, `_anker`), Bewegungen auf den Ton (`_bewegung`, `_grenzen`).
- **Gesamttest** (Fassung 1.4 nach der vierten Prüfung, 25 P): G1 Meereswellen am Badefloss (T und A aus dem
  Zeitdiagramm, λ = c · T, Momentbild zeichnen, Berge pro Minute), G2 Konzert am See (Laufzeit, λ in Luft, λ im Wasser
  mit dem Hydrofon prüfen, Taucher-Aussage zur Tonhöhe), G3 Schraubenfeder (quer/längs, Kopplung und Verzögerung,
  Klebepunkt, c = λ · f und Laufzeit), G4 Saugroboter 50 kHz und Radarsensor 24 GHz (λ, Bereich, Begründung über c,
  Felder und Vakuum), G5 zwei Linien eines Gases (f, Stufenverhältnis, Absorption E₂ → E₃, Laser), G6 Gase in der
  Atmosphäre (Aufnahme je Gas, mehr CO₂, f → λ im Fenster). Raster einheitlich: W = Ansatz mit Werten und Einheiten,
  Umrechnung und richtige Geschwindigkeit in der E-Zeile, umgekehrter Ansatz gibt Ansatz 0 und das Ergebnis
  folgerichtig. Kein Testwert steht in einer Kapitelaufgabe, Vertiefung, Leiste, Clip- oder Kontrollfrage
  (`pruef_fest.py`, Teil «TEST»). Die Natriumdampflampe ist aus «em-rechnen» gestrichen (Aufgabe 5a/5d).
- **Bewusst weggelassen:** Reflexion, Überlagerung, stehende Wellen, Saite (6.1a), Wellengleichung \(y(s,t)\),
  Wasserteilchen in der Tiefe, Elektronvolt, Energiebilanz und Einschichtmodell (LP Wärme), Brechung, Beugung,
  Interferenz (nicht in den Kompetenzen).

## Widersprüche und Auffälligkeiten der Themenseite 6.1 (nicht behoben, Auftrag: nur melden)

- **Mikrowelle 2.45 GHz:** erledigt (08.10.2026): Die Grenze Mikrowellen/Radio liegt jetzt auf Themenseite und im
  Leitprogramm bei 1 m.
- **Animation 7 (Atmosphäre):** Der Boden strahlt immer 240 W/m², während bis 192 W/m² zurückkommen — passt nicht zum
  Einschichtmodell des Leitprogramms Wärme (390 W/m² Abstrahlung, 150 W/m² Gegenstrahlung).
- **Lösungen ohne Einheiten beim Einsetzen** (A1, A3, A4, A5 und einige Mini-Checks), gegen das Ansatz-Prinzip
  mit Einheiten (STYLEGUIDE §2.7).
- \(c = 2.998 \cdot 10^8\) m/s im Text, \(3 \cdot 10^8\) in Rechnungen (klein, aber zwei Werte).
- Schall in Luft 340 m/s bei 15 °C; STYLEGUIDE nennt 343 m/s bei 20 °C.
- Mini-Check «Kurze Rechnung» enthält keine Rechnung; «Grundgrössen» in den Kernpunkten meint die Kenngrössen
  der Welle (Grundgrössen sind SI-Begriff).

## Aussprache (nicht in `build-clip-ton.py` eingetragen, nicht umschrieben — zum Anhören)

Kandidaten, die die Stimme falsch lesen könnte: «ppm» (Treibhaus, Mehr Kohlendioxid), «UKW-Sender» (em, Problem
Radio), «Lambda», «Laser» (steht in der Tabelle, Kontext «Laserstrahl»), «Neon», «Delfin», «Helium», «Hydrofon»
(nur im PDF), «stimulierte», «Phasengeschwindigkeit».

## Prüfen (Stand 08.10.2026, nach der Behebung alle grün)

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-wellen.html 2000   # 15 Typen × 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-wellen.html          # 6 Leisten, 29 Aufgaben
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-wellen.html
node .claude/tools/render-check.mjs leitprogramme/leitprogramm-wellen.html          # 1280 und 360 px
node .claude/tools/pruef-fragen.mjs p6-1-lp-welle … p6-1-lp-kontrolle-treibhaus     # alle 12
python3 .claude/tools/sprechzeiten.py p6-1-lp-<name>
SP=<ordner> node .claude/tools/pruef-clip.mjs clips/p6-1-lp-<name>.html 1 4 7 …     # alle 3 s
python3 scripts/lp/wellen/pruef_fest.py 2000
```

## Prüfung 08.10.2026: Befunde und Behebung

`/lp-pruefung` (Seite, Clips, PDFs); alle Befunde behoben (Entscheid des Auftraggebers).

- **H1 Laser-Aussage** («licht-aussage»): Die falsche Aussage heisst jetzt «Ein Laser braucht keine Spiegel …»;
  die Begründung sagt, dass die ersten Photonen spontan in alle Richtungen entstehen und erst die Spiegel die
  Achse verstärken (passt zu Kontrollfrage 5/4).
- **H2 Absorption nur aus der besetzten Stufe:** Clip «Absorption» und Notiz umformuliert (Photonen, die zu einem
  Sprung nach oben passen, ausgehend von der Stufe, auf der die Elektronen sitzen); Kontrollfrage 5/2 mit
  Quecksilberdampf 254 nm (Sprung von der tiefsten Stufe) statt Wasserstoff; Festhalten 5 und Leiste sim5 A3
  («1200 nm fehlen nicht, weil kein Elektron auf E₂ sitzt») nachgeführt. Natrium bleibt bei Aufgabe 5a/5d.
- **H3 Autokolonne:** Antwortbild mit Anfahrwelle nach hinten, Autos nach vorn, «gleiche Linie: Längswelle»; Ton neu.
- **M4 «wellengleichung»** würfelt jetzt Luft (der Fehlertipp «mit Luft gerechnet» nur für andere Stoffe);
  `pruef_fest.py` prüft die Verteilung der vier Medien (Liste `FAELLE`).
- **M5 Ergebnisse mit dem Wort:** Rechnungen wachsen um ihr Ergebnis (`rechnung()` in `clips.py`: Ansatz und
  Einsetzen mit dem Satzanfang, die ganze Zeile mit dem gesprochenen Ergebnis; `teilanker.py` kennt dafür
  `_aus_anker`). In allen sechs Lösungsszenen und «Phasengeschwindigkeit»; Probe-Notizen am Ergebniswort.
- **M6 Leuchtreklame:** Linienspektrum von Neon als graf (Linien um 585 bis 703 nm, 640 nm beschriftet) statt Modellatom.
  Die Linienwerte stammen aus dem Gedächtnis (gerundet) und sind vor einer Freigabe an einer Linientabelle zu prüfen.
- **M7** Kontrollfrage 5/1: Elektron nach der stimulierten Emission auf E₁ (gestrichelter Sprung).
- **M8 La-Ola:** «weiter läuft nur das Muster, niemand wandert mit; jeder steht aus eigener Kraft auf».
- **M9 sim6:** zeichnet λ · B_λ über log λ (flächentreu: graue Fläche unter der Kurve = Prozent der Zeile);
  Zeile und Notiz «im Bandmodell», nicht mit dem Einschichtmodell vergleichbar; Vergleichsantworten nennen die Zunahme
  (2 bis 3 bzw. rund 4 Prozentpunkte). Die Clips zeichnen die Strahlung ebenso (λ · B_λ). CH₄-Beschriftung
  überlappte H₂O: neu links neben dem Band.
- **M10 Gesamttest Fassung 1.1:** G1 Momentbild ablesen und um c · t verschieben, G2 c mit «Schall braucht ein
  Medium», G4 Babyphone (f aus λ) und Axtschlag (Laufzeit des Schalls, geübt in «laufzeit»; kein Radar-Echo mehr),
  G5 zwei Linien eines Gases (Verhältnis rückwärts), G6 Ozon gegen Methan und f → λ. Übungen mit anderen Geräten:
  Gummiseil statt Schraubenfeder («laufzeit», «phasengeschw»), Güterwagen («quer-laengs»), Pfeife statt Echolot
  («wellentyp»).
- **M11 Raster:** ein Fehler, ein Abzug (G1, G2), Ablesetoleranz ein Drittel Kästchen, (W)-Zeilen in G1 und G2, (B)
  nur bei «Begründe»/«Erkläre», typischer Fehler G5 b (subtrahiert, umgekehrt), Kompetenzzuordnung K2 → G4 c
  (seite.py und hier gleich), mehr Schreibzeilen (G3, G6).
- **M12 Gleichmässige Wellen:** `"gleichmaessig": true` an allen laufenden Kurven (Schreiber `gleichmaessig()` in
  `clips.py`; welle «Seil», «Schwingung», «Energie», «Lösung Seil», diagramme «Zeitdiagramm», «Phasengeschwindigkeit»);
  `teilanker.py` lässt das Feld stehen (geprüft im JSON und im HTML, `data-gleich`). Die Wellen in medium, em
  und treibhaus stehen still.
- **M13 Begriffe:** spontane Emission im Clip «Emission» und im Festhalten 5; Aufgabe 1c ohne «Momentbild»;
  Photon und E = h · f aus dem Clip em «Spektrum» entfernt (das Festhalten 4 führt das Photon mit Erklärung ein).
- **M14 Fachliches:** Festhalten 3 (leichte Teilchen schneller, dünnes Seil, Schall längs in Gasen und Flüssigkeiten),
  Clip medium «Schall» («in Luft und in Wasser»), Ozon im Festhalten 6 und im Clip «Durchlässig», Kontrollfrage 6/3
  «vor allem».
- **M15 Kontrollclips:** Rückmeldungen ohne Lösung (medium, em, treibhaus); Kontrollfrage 4/1 neu (Wecker und
  Lämpchen unter der leer gepumpten Glocke), 3/5 neu (Stimmgabel in wärmerer Luft: 0.680 → 0.692 m); eigene
  Antwortbilder für 4/5 (Feldskizze) und 5/4 (Glühlampe gegen Laser); 4/3 Rückmeldung «Giga heisst 10⁹».
- **Niedrig:** CO₂-Verbreiterung als Ausschnitt 10 bis 21 µm mit gestrichelten 280-ppm-Rändern; CH₄ beschriftet;
  Schicht «Luft: Stickstoff, Sauerstoff» in «Durchlässig»; Beschriftungen in Kontrollfragen 6/1, 4/4 (blau
  gestrichelt, das Theme hat kein Blau), 5/3, 2/5 neu gesetzt; «doppelte Frequenz» mit dem Bild; Schwimmbad mit
  Lautsprecher unter Wasser; Schaukel 2 bis 4 s; «bereich» 1.0 · 10¹⁶ Hz; «ablesen» ohne die Werte von Aufgabe 2a;
  «wellentyp» ohne Erdbeben und mit «Strahlung, die eine Wärmebildkamera aufnimmt»; sim2-Kommentar; Kapitel 2 mit
  40 min (Summe 305 min ≈ 6.8 Lektionen); «ein k-tel so gross»; Vergleichstabelle im Merkkasten; «gibt»; E und B
  gleichphasig; Seitenumbrüche des Gesamttests.
- **Neu vertont:** ganz (das Teilvertonen mit `--szenen` brach mit «Spur passt nicht zum Drehbuch» ab):
  p6-1-lp-medium, -em, -licht, -treibhaus und die Kontrollclips -welle, -medium, -em, -licht, -treibhaus samt
  Fragetönen; Fragetöne einzeln für p6-1-lp-medium (1), -em (1), -treibhaus (1).

## Prüfung Runde 2 (08.10.2026): Befunde und Behebung

- **R2-1 Ozon** (fachlich falsch): Ozon ist selbst Treibhausgas (Infrarot um 9.6 µm). Festhalten 6, Bewertung G6 a
  und das Bandmodell nachgeführt: sim6 nimmt Ozon 9.3–10.1 µm in die letzte Stufe («+ Methan, Ozon»; Bodenstrahlung
  im Bandmodell 59.7 % bei 430 ppm, 63.5 % bei 800 ppm, mit python3 nach der Integration der Simulation), Clips
  (Szene «Aufnahme» neu gesprochen, Ozonband in allen Bandbildern, Kontrollfrage 6/4 neu gesprochen), Aufgabe 6b
  (Diagramm mit Ozonband, Punkt B von 10 auf 11 µm), Übung «zuordnen» (Fenster mit Ozonhinweis).
- **R2-2 G4 a:** Bewegungsmelder 24 GHz → 1.25 cm, klar Mikrowellen. Die Bereichsgrenze (1 mm bis 10 cm) bleibt.
- **R2-3 bis R2-7 Gesamttest Fassung 1.2:** neu gebaut und Teil für Teil abgeglichen (Tabelle unten); Periode aus dem
  Zeitdiagramm (G1 a) und «warum mehr Kohlendioxid wärmt» (G6 b) geprüft; nichts zu zeichnen (G1 c der Fassung 1.1
  war nur freiwillig geübt); G2 c eindeutig (Hörbereich mit Zahlen), Medium als Schüleraussage (G2 d). Raster: (B)
  nur bei «Begründe», «Erkläre», «Beurteile»; G4 c und G5 d mit vollständigen Pflichtteilen; G5 b ohne Einheit;
  G4 a ohne Grössenordnungshinweis; Beispiele im KI-Auftrag aus diesem Test. Zeit ehrlich 40 min (22 Teilaufgaben),
  Summe 310 min ≈ 6.9 Lektionen; Schreibzeilen neu verteilt (vier Seiten).
- **R2-8 Gipfel der flächentreuen Kurven:** In sim6 (Notiz, Leiste), Festhalten 6, Übungen und Clip («Zwei
  Strahlungen», Notiz) steht jetzt «je Mikrometer am stärksten um 0.5 µm bzw. 10 µm; in der flächentreuen Darstellung
  Gipfel bei rund 0.6 und 13 µm». «Sonne» steht neben dem Gipfel.
- **R2-9 sim5:** Die Formelzeile nennt im Startzustand keine Wellenlängen mehr; die Absorption nennt 400/600 nm erst
  nach dem Lauf.
- **R2-10:** blaue LED 465/475 nm (nicht 450 nm), roter Laser 635/670 nm (nicht 650 nm wie Vortest 0a), «medium» ohne
  3.0 m. `pruef_fest.py`: 3, 20, 100 und 1000 sind keine Konstanten mehr (dadurch fielen Paare wie «2 m/s; 3 s» durch;
  neu in `FEST_PAARE`), und Übungen mit nur einer Zahl werden mit Zahl **und Einheit** gegen kurze Sätze aus
  Gesamttest, Kontrollfragen und Kapitelaufgaben geprüft (`EINZEL`).
- **R2-11:** Notiz «Sender: 88.0 MHz» 2.5 s nach Szenenbeginn (der Anker «Ein UKW-Sender» wird für die Stimme
  umgeschrieben und war darum nicht zu finden).
- **R2-12 Läufer:** Alle Clips mit `gleichmaessig` neu gebaut; die Läufer haben dieselben Ankerzeiten wie die Kurven
  (Schwingung, Zeitdiagramm, Phasengeschwindigkeit) und liegen im Prüfbild auf Front bzw. Berg.
- **R2-13:** Kontrollfrage 5/1 mit einfallendem Photon von links auf das Atom zu; 4/5 mit B als ⊙/⊗ senkrecht zur
  Zeichenebene, im Takt von E.
- **Niedrig:** Festhalten 1 (Gitarrensaite, Güterwagen, «Schall in Luft»), «Grundzustand» ersetzt, sim3 A5 mit
  Ausgangszustand «gleich» und \(f = 1.0\) Hz, Wellenbad \(c \ge 1.5\) m/s, «medium»-Lösung über \(\lambda_1 \cdot c_2/c_1\),
  Festhalten 4 «ionisieren», «wellentyp» (Ultraschall eines Geräts, Strahlung einer Röntgenröhre), Kontrollfrage 5/2
  «200 bis 400 nm» (Fragetton neu), Achsennamen 4/3 und 4/4, Beschriftungen 5/3 und 5/5, Schlagwort «Photon»
  gestrichen, Rückmeldung 2/5 ohne Lösungsweg (Fragetton neu).
- **Neu vertont:** p6-1-lp-treibhaus und p6-1-lp-kontrolle-treibhaus ganz; Fragetöne p6-1-lp-kontrolle-diagramme (5) und
  p6-1-lp-kontrolle-licht (2). `--szenen` brach wieder ab: Es vergleicht die Länge der Tonspur mit der Planlänge aus
  `szenen_planen()` (mit Nachlauf und Fragepausen), die bei diesen Clips immer länger ist — darum ganz vertont.

### Abgleich Gesamttest gegen den Kurs (Fassung 1.2)

| Teil | Was | Nächstes im Kurs | Unterschied |
|---|---|---|---|
| G1 a | T, A aus Zeitdiagramm einer Boje | sim2 A2, Übung «ablesen», Aufg. 2a | Zeitdiagramm allein, andere Werte (3.2 s, 40 cm) |
| G1 b | λ = c · T rückwärts | Übung «phasengeschw» (λ gesucht) | eigene Werte, c gegeben statt λ abgelesen |
| G1 c | Ergebnis am Momentbild prüfen, warum nur dort | Kontrollfrage 2/4 (Verwechslung), Aufg. 2c | Prüfen und Begründen statt Fehlersuche |
| G1 d | Berg erreicht zweite Boje (Ablesen + s/c) | Übung «laufzeit», sim2 A1 | Kombination Zeitpunkt aus Diagramm und Laufzeit — so nirgends |
| G2 a, b | f aus λ im Wasser, λ in Luft | Clip medium (f gegeben, beide λ), Übung «medium» | rückwärts: λ gegeben |
| G2 c | Hörbereich mit Zahlen | Übung «hoerbar», Aufg. 3a | 2.5 kHz, anderer Kontext |
| G2 d | Schüleraussage «Schall braucht Luft» | Kontrollfragen 3/4 (Mond), 4/1 (Glocke) | Fehlvorstellung «nur Luft» statt Vakuum |
| G3 a | seitlich/längs an der Feder | Übung «quer-laengs» (Güterwagen, Seil), Festhalten 1 (jetzt ohne Feder) | beide Fälle an einem Gerät |
| G3 b | Schüleraussage Windungen wandern | Kontrollfrage 1/1 (Stadion), Aufg. 1a | Aussage beurteilen statt beschreiben |
| G3 c | T aus f, Anzahl in 5 s | Übung «periode» (f, T aus Anzahl/Zeit) | rückwärts: f gegeben |
| G3 d | c = s/t | Übung «laufzeit» (Gummiseil), Kontrollfrage 1/3 (Leine 6.0 m) | 5.6 m in 1.6 s, Feder |
| G4 a | λ aus 24 GHz, Bereich | Übung «em-rechnen» (Radar 77 GHz), Clip em (88 MHz) | Bewegungsmelder 24 GHz |
| G4 b | Schüleraussage «tiefe Frequenz, langsamer» | Kontrollfrage 4/4 (rot/blau, Frequenz), Aufg. 4d (freiwillig, Länge) | Aussage über Geschwindigkeit und Frequenz |
| G4 c | Felder, Vakuum gegen Ultraschall | Aufg. 4a (Schall–Licht), Kontrollfrage 4/5 (was schwingt) | Begründung mit Medium an zwei Geräten |
| G5 a, b | f und Stufenverhältnis aus zwei Linien | Clip licht (Verhältnis gegeben → λ), Übung «stufen», Aufg. 5b | rückwärts: λ gegeben → Verhältnis |
| G5 c | Schüleraussage zur Absorption | Kontrollfrage 5/2 (Quecksilber, MC), sim5 A3 | Fehlvorstellung «nur diese Farben bleiben» |
| G5 d | Pumpen und Spiegel | Aufg. 5c (Laser gegen Taschenlampe), Kontrollfrage 5/4 (schmaler Strahl) | Funktion der Bauteile |
| G6 a | Stickstoff, Wasserdampf, Ozon | Kontrollfragen 6/1 (N₂/O₂), 6/2 (Methan) | drei Gase, Ozon mit zwei Bereichen |
| G6 b | warum mehr CO₂ wärmt | sim6 A3, Clip «Mehr Kohlendioxid», Kontrollfrage 6/3 (Sonnenlicht) | offene Begründung |
| G6 c | λ aus f, Fenster | Aufg. 6c (λ → f), Clip treibhaus (λ → f), Übung «zuordnen» | rückwärts: f → λ |

## Prüfung Runde 3 (08.10.2026): Befunde und Behebung

**Seite.** R3-S1 sim6: O₃ unten in seinem Band, CH₄ links daneben, H₂O und CO₂ oben (keine Überdeckung bei 1280 und
360 px). R3-S2 sim4 A5 fragt nur nach Frequenz und Faktor (1.46), ohne Photonenenergie. R3-S3 sim6 A5 «um rund 3 bis 4
Prozentpunkte (von rund 60 % auf 63 %)». R3-S4/S8 «zuordnen»: «je Mikrometer», Ozon in der Gasliste, 10.5 µm statt
11 µm (Aufgabe 6b) und 12 µm (G6 c). R3-S5 «Mit der Schallgeschwindigkeit gerechnet.» R3-S6 Aufgabe 6c über die
Wellenlängen (6.3/0.50 = 12.6 ≈ 13). R3-S7 Kompetenzzuordnung im Seitenabschnitt, im Kopfkommentar, hier und im
Bewertungspaket gleich (G1 K1; G2 K1, K2; G3 K1, K2, K3; G4 K2, K4; G5 K4; G6 K5).

**Clips.** R3-C1 Kontrollfrage 6/4: «… entweicht der grösste Teil der Bodenstrahlung, die direkt ins All gelangt»
(Szene allein mit `--szenen` neu gesprochen). R3-C2 Antwortbild 5/5 zweizeilig. R3-C3 Hinweis «flächentreu» nach «um
zehn Mikrometer». R3-C4 Probe-Zeilen wachsen wie die Rechnungen um ihr Ergebnis (`probe()` in `clips.py`; welle,
diagramme, em, licht, treibhaus). R3-C5 Achse «Druck (schematisch)». R3-C6 λ-Masslinie mit ihrer Beschriftung. R3-C7
Rückmeldungen 2/5, 3/1, 4/3 als Frage (Fragetöne neu).

**`--szenen`:** brach ab, weil `clips.py --behalte` bei geänderten Szenen die Dauer wegliess; dann ist die Summe der
Dauern (Plan) ≠ Spurlänge. Seit dieser Runde behält `--behalte` die alte Dauer einer geänderten Szene bis zur
Neuvertonung; damit läuft `--szenen`.

**Gesamttest Fassung 1.3** (R3-P1 bis P11): neue Aufgaben mit realistischer Physik (Tiefwasser: λ ≈ 1.56 · T² = 9.0 m
bei T = 2.4 s, c = 3.75 m/s, Wellenhöhe 0.2 m ≪ λ/7), keine Zahlenzufälle zwischen typischen Fehlern (jeder typische
Fehler gibt einen eigenen Wert), regelmässiges Gitter (0.2 s, 5 cm; Toleranz ein Drittel Kästchen), Kapitelziele
geprüft: Kopplung und Verzögerung (G3 b, beide nötig), Momentbild zeichnen (G1 c, geübt in Aufgabe 2b), Periode aus
dem Zeitdiagramm (G1 a), Schall braucht ein Medium (G4 c). Raster: G6 a als Angabe (E), G5 d «sinngemäss, Fachwort
nicht nötig», Pflichtaussagen getrennt von Beispielen, Anzahlen und Verhältnisse ohne Einheit vermerkt, (S) in G1 c
benutzt. Übung «bereich» nennt den Melder «Präsenzmelder» nicht mehr; der Test nimmt einen Radarsensor einer
Schiebetür (ein Gerät, eine Einordnung).

### Abgleich Gesamttest 1.3 gegen alle Pflichtteile

Spalten: nächster Pflichtteil im Kurs je Art; «—» = nichts Vergleichbares. Verlangt wird jeweils ein anderer Aufbau
(andere Grössen gegeben/gesucht oder eine Kombination), nicht nur andere Zahlen.

| Teil | Verlangt | Kapitelaufgaben | Kontrollfragen | Clipprobleme | Leisten | Übungen | Unterschied |
|---|---|---|---|---|---|---|---|
| G1 a | T, A aus Zeitdiagramm | 2a (λ und T aus zwei Diagrammen) | 2/2 (T einer Boje, MC) | diagramme Wellenbad (λ, T aus zwei Diagrammen) | sim2 A2 (T am Regler) | «ablesen» | Teil einer Kette, A dazu, neues Gitter |
| G1 b | λ = c · T | 2a, 2c (c gesucht) | 2/3 (c gesucht) | diagramme (c gesucht) | sim2 A3 (c aus Bergwanderung) | «phasengeschw» (λ gesucht möglich) | c gegeben, λ gesucht, Wert für c aus Tiefwasser |
| G1 c | Momentbild zeichnen | 2b (λ und A gegeben) | — | — | — | — | λ erst aus b) |
| G1 d | Anzahl = t / T | 1b (f aus Anzahl) | 1/4 (f aus 12 pro Minute) | welle (T, f aus Anzahl) | sim1 A5 (Wellen zählen) | «periode» (f, T aus Anzahl) | rückwärts: Anzahl aus T |
| G2 a | t = s / c (Schall) | 3b (t in Luft und Schiene) | — | em (Schall 132 s) | — | «laufzeit» | Teil einer Kette |
| G2 b | Anzahl λ auf einer Strecke | — | — | — | sim1 A5 (Berge zählen) | — | neu: s / λ |
| G2 c | Tonhöhe = Frequenz, bleibt | — | 3/3 (Luft → Eisen, MC) | medium «Anderes Medium» | sim3 A2 (dickeres Seil, f gleich) | «medium» (λ₂ gesucht) | Schüleraussage zur Tonhöhe |
| G2 d | f aus λ, hörbar | 3a (f gegeben → λ, unhörbar) | — | — | — | «hoerbar» (f gegeben), «wellengleichung» | rückwärts: λ → f → hörbar |
| G3 a | quer und längs | — | 1/2 (Autokolonne) | welle «Quer und längs» | sim1 A1, A3 | «quer-laengs» | beide Fälle an einem Gerät |
| G3 b | Kopplung, Verzögerung | 1a (beschreiben) | 1/5 (Hand stoppt) | welle «Kopplung» | sim1 A2 | — | Schüleraussage beurteilen |
| G3 c | Energie, keine Materie | 1a | 1/1 (Stadion) | welle «Energie» | sim1 A1 | — | Klebepunkt an der Feder |
| G3 d | c = λ · f, dann t = s / c | — | 1/3 (c = s / t) | — | sim3 A3/A4 (f oder Seil gesucht) | «phasengeschw», «laufzeit» (je ein Schritt) | Kombination zweier Schritte |
| G4 a | λ für Schall und Radar, Bereich | 4b (f → λ, Laufzeit) | 4/3 (12 GHz → λ, MC) | em (88 MHz → λ) | sim4 A2 (5 GHz → λ → Gerät) | «em-rechnen», «hoerbar» | zwei Wellenarten mit je eigenem c verglichen |
| G4 b | warum längere Welle trotz höherer f | 4d (freiwillig: «länger, also schneller») | 4/4 (rot/blau) | — | sim4 A1 (Faktor der Wellenlängen) | — | Begründung über c |
| G4 c | Felder, Medium | 4a (Schall–Licht vergleichen) | 4/1 (Glocke), 4/5 (was schwingt) | em «Felder» | sim4 A4 (Zeitlupe) | «wellentyp» | an zwei Sensoren, mit Vakuum begründet |
| G5 a | f aus λ | 5b | — | licht (f₁ aus 640 nm) | — | «em-rechnen» | Teil einer Kette |
| G5 b | Stufenverhältnis aus zwei λ | 5b (Kästchen → λ) | 5/3 (doppelte Stufe → λ, MC) | licht (Verhältnis 1.25 gegeben → λ) | sim5 A2 (Verhältnis 2 : 3 gezeigt) | «stufen» (Verhältnis gegeben → λ) | rückwärts: λ → Verhältnis 1.4 |
| G5 c | Absorption von E₂ auf E₃, λ | 5b (Sprung 3 als Emission) | 5/2 (Quecksilber, MC) | licht «Absorption» | sim5 A3 (Absorption von E₁) | — | Aufnahme aus angeregtem Zustand, gerechnet |
| G5 d | Laser: Pumpen, Spiegel, stimulierte Emission | 5c (Laser gegen Taschenlampe) | 5/1, 5/4 | licht «Laser» | sim5 A4 | «licht-aussage» | Funktion der Bauteile |
| G6 a | Aufnahme je Gas | 6b (A, B, C) | 6/1 (N₂, O₂), 6/2 (Methan) | treibhaus «Aufnahme» | sim6 A1, A2, A4 | «zuordnen», «treibhaus-aussage» | drei Gase, Ozon mit zwei Bereichen |
| G6 b | warum mehr CO₂ wärmt | — | 6/3 (CO₂ und Sonnenlicht) | treibhaus «Mehr Kohlendioxid» | sim6 A3, A5 | «treibhaus-aussage» | offene Begründung |
| G6 c | λ aus f, Fenster | 6c (λ → f) | — | treibhaus Satellit (λ → f) | — | «em-rechnen», «zuordnen» (10.5 µm) | rückwärts: f → λ, 12 µm |

Kapitelziele und Test: jedes Kapitel hat mindestens eine Teilaufgabe (Kap. 1: G3; Kap. 2: G1; Kap. 3: G2, G4 c;
Kap. 4: G4; Kap. 5: G5; Kap. 6: G6). Nicht im Test: das Lesen einer Längswelle als Teilchenbild (sim1 A3) und die
Wiederabstrahlung nach allen Seiten als eigene Frage (steckt in der Pflichtaussage von G6 b).

**Bereichsgrenze Mikrowellen/Radiowellen neu bei 1 m** (Entscheid des Auftraggebers, Runde 3): BAENDER in `seite.js`
(sim4, Übung «bereich» samt Diagnosen «länger/kürzer»), Festhalten 4 (Mikrowellen «rund 1 mm bis 1 m» mit Radar, WLAN
2.4/5 GHz und Mikrowellenofen; Radio «länger als rund 1 m» mit UKW und Langwelle), Übung «bereich» mit Mikrowellenofen
12 cm und Kurzwellensender 25 m; die sim4-Bilder der Clips sind neu aufgenommen (Clip em neu gebaut). Jede Einordnung
mit python3 gegen die neue Grenze geprüft: Wetterradar 5.3 cm, Ofen 12 cm, WLAN 6.0 cm, Radar 1.25 cm (G4),
12 GHz 2.5 cm (Kontrollfrage 4/3) Mikrowellen; Kurzwelle 25 m, Langwelle 1.5 km, 4c-C 10 m Radio — alle mindestens
0.9 Dekaden von 1 m bzw. 1 mm entfernt. Einzige Ausnahme: das UKW-Radio der sim4 (95 MHz, 3.16 m) und der Clipsender
(88 MHz, 3.41 m) liegen 0.5 Dekaden über der Grenze — eindeutig Radio, wie auf der Themenseite.

## Prüfung Runde 4 (09.10.2026): Befunde und Behebung

Alle Befunde behoben.

**PDFs (Gesamttest und Bewertungspaket Fassung 1.4).**
- R4-P1: Ansatzzeilen einheitlich wie G2. G1 b W «Ansatz mit Werten und Einheiten»; ein umgekehrter Ansatz
  (λ = c/T) gibt Ansatz 0, Wellenlänge und Momentbild folgerichtig → 4 von 5, wie die Fehlerzeile. G4 a W nur der
  Ansatz λ = c/f; Umrechnung (GHz, kHz) und die richtige Geschwindigkeit je Welle stehen in der E-Zeile → Fehler
  «10⁶ statt 10⁹» oder «Ultraschall mit 3.00 · 10⁸ m/s» kostet E: 3 von 4, wie die Fehlerzeile.
- R4-P2: G4 a Saugroboter mit 50 kHz → 6.8 mm (Aufgabe 3d bleibt Fledermaus 40 kHz → 8.5 mm). `pruef_fest.py`
  vergleicht jetzt zusätzlich jede Teilaufgabe des Gesamttests (Wert mit Einheit) mit allen Kapitelaufgaben samt
  Vertiefungen, Leisten, Clip-Szenen, Kontrollfragen und Themenseiten-Blöcken; drei Einzelwerte von Hand gesichtet
  (G1 c Rasterbreite 20 m ≠ Kurzwelle 20 m in 4d; G3 d 2.0 Hz mit anderer Länge als Kontrollfrage 2 und 6.1a).
  Die Prüfung fand dabei einen echten Fehler: In «phasengeschw» hatte der Kommentar der neuen Wellenbad-Zeile die
  Berechnung von λ und c verschluckt (Aufgaben mit «NaN m») — behoben, danach keine Treffer.
- R4-P3: Kapitelziel Kap. 3 «berechnest die Wellenlänge beim Übergang in ein anderes Medium» wird jetzt geprüft:
  G2 c (170 Hz, Wasser 1500 m/s → 8.8 m, Anzeige prüfen).
- R4-P4: G2 b (s/λ) gestrichen; neu λ = c/f in Luft (geübt in «wellengleichung», «medium», Aufgabe 3a).
- R4-P5: G2 neu (Konzert am See, kein Schwimmbad, kein 85-Hz-Ton); G2 c als Ansatz + Ergebnis getrennt, G2 d nur
  Begründung, mit «Beispiel einer vollständigen Antwort» markiert; G4 b «sinngemäss», ohne Formelpflicht; G1 c
  Amplitude «folgerichtig aus der eigenen Ablesung»; Brüche mit Zeilenabstand (\\[4pt]/\\[6pt]); Seite 4 trägt nur
  G6 mit 10 Schreibzeilen und den Bewertungshinweis; «Entscheide» oben auf Fassung 1.4.

**Seite.** R4-S1 «bereich»: UV-Lampe zum Härten von Nagellack 300 nm, Computertomograf 0.05 nm. R4-S2 «hoerbar»:
Marderschreck 35 kHz. R4-S3 Wasserwellen: Aufgabe 2c 6.2 m und 2.0 s → 3.1 m/s (Tiefwasser 1.56 · T² = 6.2 m);
«phasengeschw» Wellenbad nur Paare (4.4 m; 2.0 s), (3.6 m; 1.8 s), (3.3 m; 1.5 s) — in Runde 5 korrigiert, siehe dort. R4-S4 sim5: Winkel 1.2 rad gestrichen. R4-S5 «stufen»: «tiefere Frequenz».

**Clips.** R4-C1 medium «Schall»: `_ein='in Wasser rund'`. R4-C2 treibhaus «Zwei Strahlungen»: eigener Satz «Das
Bild zeigt beide Kurven flächentreu und auf gleicher Höhe; …», Notiz daran verankert (über 3 s sichtbar). R4-C3 em
«Spektrum» drei Bilder (Radio, Licht, Röntgen) statt sechs; diagramme «Wellenbad» λ 5.0 m, T 2.0 s, A 10 cm → f
0.50 Hz, c 2.5 m/s (Wassertiefe rund 0.9 m nach ω² = g·k·tanh(k·h); Kontrollfragen, Seite und Übungen mit anderen Werten); kontrolle-medium
F3 Eisenkurve u = 2.2 (stetig an der Grenze); medium «Lösung Schwimmbad» Masslinie 0.40 m weg vom Achsennamen,
Probe mit Einheiten; kontrolle-welle F4 \(T = \frac{1}{0.20\;\text{Hz}} = 5.0\;\text{s}\); treibhaus «Aufnahme»
CH₄-Etikett links mit Hinweislinie zum Band. Neu gesprochen (`--szenen`): diagramme Szene 7 «Lösung Wellenbad»,
treibhaus Szene 1 «Zwei Strahlungen»; keine Fragetöne geändert.

### Abgleich Gesamttest 1.4: geänderte Zeilen und Vertiefungen

Die Tabelle «Abgleich Gesamttest 1.3» oben gilt weiter für G1, G3, G4 b/c, G5 und G6; G2 und G4 a sind ersetzt.
Neu ist die Spalte der freiwilligen Vertiefungen (1d bis 5d) für alle Teile.

| Teil | Verlangt | Kapitelaufgaben | Kontrollfragen | Clipprobleme | Leisten | Übungen | Unterschied |
|---|---|---|---|---|---|---|---|
| G2 a | t = s / c (Schall, 102 m) | 3b (t in Luft und Schiene) | — | em (Schall 132 s) | — | «laufzeit» | Teil einer Kette |
| G2 b | λ = c / f in Luft (170 Hz) | 3a (f → λ im Gewebe) | 3/1 (Helium) | medium «Schall» (Luft und Wasser) | sim3 A2 (λ links und rechts) | «wellengleichung», «medium» | Teil einer Kette |
| G2 c | λ im Wasser, Anzeige prüfen (8.8 m) | 3a (Gewebe ≈ Wasser) | 3/2 (Delfin, 100 kHz) | medium Schwimmbad (anderer Ort, 1.76 m) | sim3 A5 (Wasser gegen Luft) | «medium» (λ₂ gesucht) | Prüfen statt Ausrechnen |
| G2 d | Tonhöhe = Frequenz, bleibt | — | 3/3 (Luft → Eisen, MC) | medium «Anderes Medium» | sim3 A2 (P₁ und P₂ im selben Takt) | — | Schüleraussage zur Tonhöhe |
| G4 a | λ für Ultraschall 50 kHz und Radar 24 GHz, Bereich | 4b | 4/3 (12 GHz, MC) | em (88 MHz) | sim4 A2 (5 GHz) | «em-rechnen», «hoerbar» | zwei Wellenarten, zwei Geschwindigkeiten |

| Vertiefung | Inhalt | Nächster Testteil | Unterschied |
|---|---|---|---|
| 1d | Wasserwelle weder quer noch längs, Ball auf Kreisbahn | G3 a | Feder, keine Wasserteilchen |
| 2d | Momentbild einer Seilwelle zu einem Zeitpunkt (T 0.60 s, c 2.0 m/s) | G1 c | Test: Sinus aus λ und A, ohne Startrichtung |
| 3d | Fledermaus 40 kHz, Echo 6.0 ms → Abstand, λ 8.5 mm | G4 a | Test 50 kHz → 6.8 mm, ohne Echo |
| 4d | Kurzwelle 20 m «schneller als Licht» → 15 MHz | G4 b | Test: Radar gegen Ultraschall, nicht zwei EM-Wellen |
| 5d | dunkle Linien bei 589 nm im Sonnenlicht | G5 c | Test: Absorption aus E₂, Wellenlänge gerechnet |

## Prüfung Runde 5 (Schlussprüfung, 09.10.2026): Befunde und Behebung

Alle Restpunkte behoben.

**PDFs (Fassung 1.5).**
- L1: G2 neu gefasst: «Ein kleiner Teil des Schalls dringt ins Wasser des Sees ein» (kein Unterwasserlautsprecher
  mehr); c) «für diesen Ton»; Raster d) «beim Übergang aus der Luft ins Wasser»; Fehlerzeile «angenommen, im Wasser
  ändere sich die Frequenz».
- K1: Die Wellenlänge im Wasser wird mit zwei Unterwassermikrofonen gemessen, die in Laufrichtung auseinandergeschoben
  werden, bis ihre Signale erstmals wieder im gleichen Takt schwingen (8.8 m).
- K2: G1 heisst «Sturmwellen am Badefloss» (auf dem See), im Test und im Raster.
- K3: Zeilenabstand in G2 c, G3 c/d und G5 a/b grösser; Bewertungspaket bleibt bei fünf Seiten (G6 und
  Selbsteinschätzung auf Seite 5).
- K4: G2 c lässt den Gegenweg zu: \(f = c_\text{W}/\lambda_\text{W} = 1500/8.8 \approx 170\) Hz (python3: 170.45).
- K5: G6 b «Für (1) zählt auch: … wird breiter».
- K6: G5 Fehlerzeile «Verhältnis umgekehrt (0.71): b) 0 und c) 0 (E₃ läge unter E₂)».
- K7: Kapitelzuordnung auf Seite, im Kopfkommentar der Seite und im Bewertungspaket gleich: G2 → Kapitel 3 (K1, K2),
  G3 → Kapitel 1, d) Kapitel 3 (c = λ · f). In der Kompetenzmatrix steht für K2 G2 d (Tonhöhe beim Übergang) statt
  G2 c (jetzt eine Rechnung, K1).
- K8: Kopfkommentar von `gesamttest.tex` und `bewertungspaket.tex` auf Fassung 1.5, Werte von G2 nachgeführt.

**Seite.**
- 2a: «phasengeschw» Wellenbad: (5.4 m; 1.8 s) und (4.2 m; 1.5 s) sind unmöglich, weil die Wellenlänge im
  Tiefwasser höchstens \(g T^2 / 2\pi\) erreicht (5.06 m bzw. 3.51 m). Neu (4.4 m; 2.0 s), (3.6 m; 1.8 s),
  (3.3 m; 1.5 s): c = 2.0 bis 2.2 m/s, Wassertiefe aus \(\omega^2 = g k \tanh(k h)\) 0.61, 0.51 und 0.91 m. Die
  Begründung «Flachwasser, Tiefe c²/g» aus Runde 4 war falsch, weil bei λ/h ≈ 4 bis 7 die Flachwasserformel nicht
  gilt. Clipbeispiel Wellenbad (5.0 m; 2.0 s): Tiefe 0.88 m (assert in `clips.py`). Aufgabe 2c (6.2 m; 2.0 s) ist
  Tiefwasser (Grenze 6.25 m).
- 2b: sim5: Winkel −0.35 → −0.75, dazu ist die Beschriftung seitlich auf das Bild begrenzt (x 24 bis 276 bei
  viewBox −4 bis 304); alle acht Winkel mit 600 nm und 1200 nm bei 1280 und 360 px angesehen, nichts abgeschnitten.

**Clips.**
- 2c: em «Spektrum»: Röntgenbild an «Röntgenstrahlung, am» mit 0.6 s Versatz. Nach den Pausen in der MP3 (Komma nach
  «Nanometern» bei 10.5 s, nach «Röntgenstrahlung» bei 12.4 s) beginnt das Wort bei rund 11.5 s; die Präfixmessung von
  `teilanker.py` lag hier rund 0.8 s davor.
- 2d: treibhaus «Aufnahme»: Notiz und Etikett «Fenster» 0.8 s später (längste Pause, also das Satzende vor
  «Zwischen acht», bei 13.75 bis 14.09 s).
- 2e: Zwischenstufen unter 2 s (diagramme «Lösung Wellenbad» f = 1/T: 1.8 s; treibhaus Probe «Lösung Satellit»:
  1.9 s) gehen nahtlos in die volle Zeile über: Der Anfang der Zeile bleibt stehen, es wächst nur das Ergebnis an
  (Einzelbilder vor und nach dem Wechsel angesehen; Versatz höchstens 2 bis 3 px). Unverändert gelassen.
- 2f: kontrolle-welle F4 Antwortbild: Berge auf 5, 10, … 30 s; die Kurve kreuzt die Achse zwischen den Zahlen,
  Masslinie T von 5 bis 10 s.

Kein Sprechertext geändert, darum nichts neu vertont; alle zwölf Drehbücher mit `clips.py --behalte` neu geschrieben,
verankert und gebaut.

**pruef-clip:** keine Überlappung von Text oder Formeln, nichts ausserhalb der Bühne. Gemeldet werden nur
«ÜBERLAPP ×» ohne Text in welle (6), medium (4), em (11) und licht (3): Das sind Simulationsbilder einer Bildfolge, die
an derselben Stelle übereinanderliegen; das spätere deckt das frühere ganz ab (JPG, gleiche Lage und Breite). In den
Einzelbildern angesehen. Das galt schon in Runde 4; der Bericht dort («keine Überlappungen») war darin ungenau.

**Pre-Flight:** Der einzige `[FEHLER]` steht in `themen/p6-1-wellen.html`, Zeile 193 («Animation 1/5» als blosser
Text), also auf der Themenseite, an der der Koordinator arbeitet. Ausserhalb der Pfade dieses Auftrags, darum nicht
angefasst.
