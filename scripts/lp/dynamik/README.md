# Bauskripte: Leitprogramm Dynamik

Drittes Physik-Leitprogramm nach dem Kapitelmuster (`HOWTO-leitprogramme.md` §4), als Kopie von
`scripts/lp/kinematik/` entstanden (04.10.2026). Kopf, CSS, Grundskript, Bausteine und das
Gerüst von `seite.js` (Achsen, Bedienung, Aufgabenleiste mit Vergleichsantwort, Übungsrahmen)
sind wörtlich von dort. Neu sind Kapitel, Übungstypen, Clips und die **laufenden Simulationen**:
Die Bewegung läuft auf Knopfdruck ab (`Uhr`, `aktionen` in `seite.js`), das v-t-Diagramm entsteht
dabei, und der vorige Lauf bleibt grau gestrichelt als Vergleich stehen.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/leitprogramm-dynamik.html` — Kopf, CSS, Grundskript, alle Kapitel, die Aufgabenbilder (v-t-Diagramme, Minigrafen). Die Laufzeiten der Clipkarten liest es aus den Drehbüchern. Aus der bestehenden Seite übernimmt es nur den SEO-Block. | **ja** — für jede Änderung an Text, Aufgaben, Kapitelaufbau |
| `seite.js` | Seitenskript: Simulationen sim1–sim5 (Wagen F/m, Velo mit Antrieb und Widerstand, Aufzug mit Waage, Wagen am Faden, Kugel an der Schnur), 15 Übungstypen (`TYPEN`, je mit `fehler()`), Minigrafen | wird von `seite.py` eingesetzt |
| `clips.py` | Archiv: hat die zehn Drehbücher `clips/p4-2-lp-*.json` erzeugt | **nein** — nach der Vertonung sind die JSONs die Quelle (`--neu` überschreibt die gemessenen Dauern). Die Einblendezeiten sind danach im JSON auf die Sprechzeiten gelegt worden (`sprechzeiten.py`). |

## Ablauf bei einer Änderung

```sh
python3 scripts/lp/dynamik/seite.py
python3 scripts/build-seo.py
python3 .claude/skills/preflight/preflight.py leitprogramme/leitprogramm-dynamik.html
```

Änderungen **nur hier** machen, nicht direkt in der HTML-Datei — der nächste Lauf überschreibt sie.

Clips ändern: Drehbuch `clips/p4-2-lp-*.json` bearbeiten, dann `build-clip-ton.py` (Sprechertext
geändert) → `build-clip-fragen-ton.py` (Kontrollclips) → `build-clips.py` (Stimme
`de_DE-thorsten-high`), danach `seite.py` (Laufzeiten). Die Bilder `clips/bilder/p4-2-lp-*.jpg`
sind Aufnahmen der Simulationen (`.claude/tools/aufnahme-anim.mjs`, Selektor `#simN > svg`,
Regler per `js`-Aktion, Start per `js`-Klick auf `.aktion`, danach so lange warten, bis die Fahrt
zu Ende ist). Ändert sich eine Simulation: neu aufnehmen und jedes Bild ansehen. Die Dynamik-Simulationen
haben (noch) keinen Testhaken `zeige(…)`; Abläufe zeigen die Clips darum als `graf` (v-t-Geraden,
Kräftepläne), nicht als Bildfolge.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/dynamik/*.tex`, bauen mit
`python3 scripts/build-lp-pdf.py dynamik`. Das Bewertungspaket folgt der Kinematik-Fassung
(Punktarten E, W, B, A; Folgefehler überall gleich).

## Prüfen

```sh
node .claude/tools/pruef-uebungen.mjs leitprogramme/leitprogramm-dynamik.html 2000
node .claude/tools/pruef-leiste.mjs leitprogramme/leitprogramm-dynamik.html
node .claude/tools/pruef-formelsatz.mjs leitprogramme/leitprogramm-dynamik.html
node .claude/tools/pruef-fragen.mjs p4-2-lp-kontrolle-grundgesetz p4-2-lp-kontrolle-gesamtkraft \
     p4-2-lp-kontrolle-aufzug p4-2-lp-kontrolle-faden p4-2-lp-kontrolle-kurve
```

Ob jede Aufgabe der Leisten **lösbar** ist, prüft `pruef-leiste` nicht — beim Bau am 04.10.2026
mit einem Prüfskript gelöst, das jede Aufgabe mit den Zielwerten einstellt und die Fahrten über die
Knöpfe auslöst (mit `reducedMotion: 'reduce'` laufen sie sofort durch; alle 30 ✓, keine schon im
Startzustand erfüllt).

## Entscheide

- **Umfang nach RLP:** 4.2 hat in Gruppe 1 nur zwei Kompetenzen (Zusammenhang F, m, a; zweites
  newtonsches Gesetz bei gleichmässig beschleunigter Bewegung und gleichförmiger Kreisbewegung).
  Federkraft, Wechselwirkungsgesetz, Reibungszahl und schiefe Ebene bleiben auf der Themenseite
  (Reibung und schiefe Ebene gehören im RLP zu 4.4 Statik). Reibung kommt nur als gegebene
  Widerstandskraft vor.
- **Bezeichnungen:** \(F_W\) für jeden Widerstand. Die Themenseite benutzt \(F_G\) und \(F_H\) teils
  für Gleit- und Haftreibung, obwohl sie Gewichtskraft und Hangabtrieb heissen.
- **Farben** wie STYLEGUIDE §5.2: v Grün, a Violett, Gewichtskraft Bernstein, Widerstand und
  Zentripetalkraft Rot, übrige Kräfte (Antrieb, Faden, Normalkraft) Blau. Das Clip-Theme kennt
  weder Blau noch Violett: Diese Grössen bleiben in den Clips ungefärbt.
- **Massstäbe:** Faden-Simulation 80 px je m waagrecht wie senkrecht (der Faden ist undehnbar);
  Kreis 60 px je m, Kraftpfeil 2.5 px je N, gekürzt mit Hinweis, wenn er nicht in den Kreis passt.
- **Velo-Modell:** Steht das Velo und reicht der Antrieb nicht (\(F_A \le F_W\)), hält der Widerstand
  nur so stark dagegen, wie der Antrieb zieht: Bild und Formelzeile zeigen \(F_\text{ges} = 0\), \(a = 0\).
  Dasselbe nach dem Halt beim Ausrollen.
- **Aufzug** läuft wie alle Simulationen erst auf Knopfdruck («Fahrt zeigen»); Kräfte und Waage gelten
  sofort. Mit «weniger Bewegung» dreht «Kreisen» in Sim 5 in Schritten weiter.
- **Nach /lp-pruefung (04.10.2026)** behoben: Velo im Stand, voriger Lauf, Aufzug ohne Knopf, Regler im
  Flug, gerundete Zwischenwerte in den Formelzeilen, doppelte Beispiele (Clip, Kontrollfrage, Leiste,
  Festhalten, Mini-Checks), ω eingeführt, Gesamttest G1 d/G3–G6 neu, Raster präzisiert.
- **Freigeschaltet am 06.10.2026:** Karte in `leitprogramme.html` (Lerngebiet 4), Kasten «Lieber geführt
  durcharbeiten?» auf der Themenseite, im Suchindex und in der Sitemap.

## Fassung 1.1 (06.10.2026)

Nach der zweiten Prüfung (Querschnitt aller Leitprogramme und Befundliste Dynamik) behoben:

- **Einführungsclips** mit vorgerechnetem Problem (Problem → Vorgehen mit Strategiefrage «Dein Vorgehen» →
  Lösung mit Probe), je vor «Zum Mitnehmen»: E-Trottinett (Zeit aus F und m), Kiste gegen Reibung (Zugkraft),
  Waage im Aufzug (a aus der Anzeige), Lieferwagen mit Anhänger (Kupplungskraft; bereitet Kontrollfrage 3 vor),
  Kind im Karussell (v aus der Umlaufzeit). Die Einblendungen hängen jetzt an `_anker` (`scripts/lp/kinematik/anker.py`).
- **Clipbilder:** stehende Geraden mit Läufer statt drehender (grundgesetz, gesamtkraft «Ausrollen» bis 12 s,
  dann v = 0, Antwortbilder der Kontrollclips); Steigungsdreiecke als eigene Strecken mit «Δt = 1 s», «Δv = 4 m/s»;
  v grün, Gesamtkraft, Faden, a ungefärbt; Ergebnisse erst mit dem Ton (Aufzug als Bildfolge, Fadenkraft, 4500 N, 9 N);
  «Gesamtkraft: 2.45 N» statt «Rest»; Einheiten bei «= 0 N»; Modellannahme «glatter Tisch» bei der Kugel an der Schnur;
  Gesamtkraft in Kapitel 1 eingeführt (Clip und Festhalten).
- **Kontrollfragen** mit neuen Beispielen (Ketchupflasche, Velo 75 kg, Fadenkraft bei 0.4 kg, Kugel auf r = 2 m,
  Zug in der Kurve), Rückmeldungen ohne Lösung, jede falsche Option ein benannter Fehler.
- **Simulationen:** Startwerte weder Clipbeispiel noch Leistenziel (7 N/5 kg; 50 N/25 N; 55 kg, 1 m/s²; 2.5 kg/0.8 kg;
  1.5 kg, 2.5 m/s, 1.2 m); jede Leistenaufgabe mit Denkauftrag und Vergleichsantwort; Ziel «gestrichelte Gerade» in
  Sim 2 nicht schon eingestellt; Punkt bleibt am Rand, wenn die Gerade aus dem Diagramm läuft; Formelzeile der
  Fadenkraft mit symbolischem Zwischenschritt; Knopf «bremst die Fahrt nach oben».
- **Übungen:** feste Beispiele ausgeschlossen (Liste `FEST_FM` und je Typ), m₁ = 1 kg beim Faden ausgelassen,
  plausible Werte (Wagen bis 12 m/s, Fahrwiderstand ans Tempo gebunden), Folgewerte aus auf drei Stellen
  gerundeten Zwischenwerten angenommen, Lösungen mit eingesetzten Werten, «g» statt «Ortsfaktor».
- **Seite:** Vorzeichenregel «eine Richtung wählen und nennen», Freikörperbild im Festhalten, Haftreibung mit
  Höchstwert (Verweis Statik, Kapitel 3), neue Aufgaben 4a (rückwärts), 4d (am Diagramm), 5d (Wäscheschleuder),
  Kapitelzeit 45 min.
- **Gesamttest (Fassung 3):** G1d, G2 bis G6 neu (keine Wiederholung von Kapitel-, Leisten- oder Übungsaufgaben),
  G4 5 P, G6 4 P; Raster «ein Fehler, ein Abzug», Rundung 2 %, (B) nur bei Begründen/Erklären/Formulieren,
  `arraystretch` 1.5, Gesamttest auf drei Seiten.
