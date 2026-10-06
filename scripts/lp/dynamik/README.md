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
