# Clips und Vertonung — Details

Aus der Wurzel-`CLAUDE.md` ausgelagert (11.10.2026, /doctor): Claude Code lädt diese Datei, sobald in diesem
Ordner gearbeitet wird. Die Regeln der Wurzel-`CLAUDE.md` gelten weiter; bei Widerspruch gilt STYLEGUIDE.md.

- `scripts/build-clip-ton.py` — **Vertonung** eines Clips, lokal und offline mit
  Piper. Erzeugt **eine** MP3 je Clip (`clips/ton/<name>.mp3`) und schreibt die
  gemessene Sprechdauer je Szene als `dauer` ins Drehbuch zurück — danach sitzt
  Bild auf Sprache. Danach den Clip mit `build-clips.py` neu bauen. Nach einer
  Textkorrektur nur die geänderten Szenen neu sprechen: `--szenen 2,5` (die übrigen
  behalten Ton und `dauer`); für Fragetöne `build-clip-fragen-ton.py --fragen 2,5:r1`
  (seit 08.10.2026, aus Mathe).

  **Keine Zweitstimme.** Mathe hatte zeitweise `--zweitstimme` samt
  Umschalter im Player — gebaut für das persönliche Modell, das hier nicht
  verwendet wird. Am 26.09.2026 bewusst nicht übernommen; der Rückbau in
  Mathe steht in der Warteschlange von `scripts/abgleich.py`.

  **Stimme: `de_DE-thorsten-high` (verbindlich, bis der Auftraggeber es ändert).**

  ```bash
  export PIPER_MODELL=/home/paps/piper-stimmen/de_DE-thorsten-high.onnx
  python3 scripts/build-clip-ton.py <clipname>
  python3 scripts/build-clips.py    <clipname>
  ```

  Datensatz Thorsten-Voice, CC0 — dieselbe Stimme wie in Mathe begreifbar. Das
  persönliche Modell `de_CH-kohler-medium` wird **nicht** verwendet. Kein
  Stimmmodell gehört ins Repo.

  **Aussprache von Fremdwörtern:** Die Tabellen `AUSSPRACHE`, `ABKUERZUNGEN`
  und `TAUSCH` in `build-clip-ton.py` ändern nur den Text an Piper;
  Transkript und Suchindex behalten die Schreibweise. Stand 28.09.2026, jeder
  Eintrag nach Hörproben entschieden: Einheiten (Ampere, Coulomb, Joule,
  Pascal, Hertz), Namen (Boyle, Mariotte, Gay-Lussac, Hooke, Pythagoras),
  Fremdwörter (u. a. Zentripetal…, das die Stimme englisch las), Mathes
  Wörter (Hyperbel, Tangens, Sechstel, komponentenweise, Hypotenuse, Menü
  hinten betont, TI-30X-Tasten …), exakte Wörter (FI, LED, COP, SI buchstabiert; «My» als «mü»,
  sonst englisch «Mai»), Oktave, Ellipse, Longitudinal-, Laser, orange,
  Radio-, elektromagnetisch, Glacé, Caesium, Granit, Candela, dazu Worttausche (achthundert, Newtonmeter,
  Lageenergie, TI-30X) und die **Wortfuge per Bindestrich** für einzelne
  Zusammensetzungen, in denen die Stimme «s-t» statt «scht» las
  (Wärme-strahlung, Gamma-strahlung, Nachkomma-stellen, Zahlen-strahl,
  Häufigkeits-spalte, Bewegungszu-stand, Tabellen-dichte, Norm-dichte,
  Komma-stellen).
  Archimedes, Perihel, Parabel, Mikrometer, Mikro, Volumen, linear,
  Erdbeschleunigung, Transversal-, Niveau, Photon, Gneis, Basalt, Lumen,
  Milliarden, Elementarladung, Einholzeit und Gegenrechnung bleiben bewusst
  ungeändert, ebenso Widerstand, Kilowattstunde und die übrigen Fugenwörter
  (als allgemeine Regel angehört und abgelehnt). **Die
  Tabellen sind in beiden Repos dieselben** (am 28.09.2026 in Sätzen aus
  beiden angehört und je Wort einmal entschieden); ein neues Wort gilt also
  für beide — Hörprobe mit Sätzen aus beiden, Übertrag über `abgleich.py`. Ein neues Wort gehört in diese Tabellen, nicht
  als Umschreibung ins Drehbuch; betroffene Clips danach neu vertonen. Wie man
  Problemwörter findet und Hörproben zeigt: `HOWTO-clips.md`, Abschnitt «Ton».

  **Zahlen im `sprecher`-Text ausschreiben.** Nachgemessen über die Sprechdauer
  desselben Satzes in fünf Varianten: Beide Stimmen lesen `1.62` als
  zusammengesetzte Zahl («… zweiundsechzig») statt als Stellenfolge
  («… sechs zwei»), kohler zusätzlich den Dezimalpunkt als «Punkt». Bei
  Messwerten ist die Stellenfolge die übliche Lesart — darum ausschreiben. In
  Mathes 162 Clips steht aus demselben Grund fast nirgends eine Ziffer im
  Sprechertext; die Ausnahmen sind Geräte- und Listennamen (`TI-30X`, `L1`) —
  das sind Namen, keine Werte.
- `clips.html` + `clips/` — **Erklärclips** (Bibliotheksseite und Drehbücher).
  Ein Clip wird nie beim Seitenaufruf geladen: sichtbar ist zuerst nur der
  Startknopf, erst der Klick setzt das `<iframe>` ein (`clipStart` in
  `physiklib.js`). `scripts/build-clips.py` baut aus einem Drehbuch
  (`clips/<name>.json`) den Clip, `scripts/build-clips-einbau.py` trägt ihn in
  die Lektionsseite und zwischen die Marker `<!-- CLIPS-BIBLIOTHEK:ANFANG/ENDE -->`
  in `clips.html` ein. Stand 09.10.2026: **205 Clips in 25 Reihen, 222:52 min** (davon 116 zu einzelnen Animationen — jede Animation der Themenseiten, von 6.1a und der Vorwissenseiten hat ihren Clip — Reihe «Animationen erklärt») —
  jede der zehn Themenseiten der Lerngebiete 4 bis 6 hat ihre Reihe, dazu das
  Vorwissen. Anders als Mathe gruppiert die Bibliothek nur nach Lerngebiet
  (kein Grundlagen-/Schwerpunktfach), und sie zieht die Gruppen aus `nav.js`,
  nicht aus dem Freitextfeld `lerngebiet` im Drehbuch.
  Seit 07.10.2026 (aus Mathe übernommen) steht im Lerngebiet **je Themenseite
  eine dreispaltige Tabelle**: Animationen (116, mit «Anim») · Leitprogramm
  (129: die eigenen `"probe": true`-Clips der sichtbaren Leitprogramme vor
  `<h2 id="veraltet">` in `leitprogramme.html`, dazu die 15 des Prüfungsbogens
  `uebungstest-waermelehre`; vorn «LP» auf `#simN` des Kapitels bzw. auf die
  Aufgabe) · Weitere Clips; unter 720 px untereinander, leere Spalte «—».
  Gebaut von `scripts/clips_bibliothek.py` (Fachgut, mit eigenem `REIHEN_VORN`,
  das nur in der Bibliothek gilt); `build-clips-einbau.py` ruft es mit zwei
  Zeilen auf. CSS im `<style>` von `clips.html`, nicht in `style.css`. Details:
  `HOWTO-clips.md`, «Bibliotheksseite».
  Ein Clip liegt **einmal** und darf über die Liste `lektion` auf mehreren
  Seiten stehen; elf tun das — die Bibliothek zeigt das mit der Zeile
  «↳ auch in 4.5 Hydrostatik» unter dem Titel. Über der Liste steht eine
  **Sofortsuche** (Titel, Reihe, Kurzbeschrieb, Schlagworte, Lektionsnummer);
  Feld und Filterskript stehen **ausserhalb** der Marker und werden von Hand
  gepflegt, das `data-suche` je Zeile kommt aus dem Generator.
  Auf der Themenseite steht der Clip-Block **nach der Zusammenfassung, vor dem
  Zusatzmaterial** (STYLEGUIDE §4, Zeile 11b).
  **Clips zu einer einzelnen Animation** (seit 28.09.2026 zu jeder der heute 116
  Animationen der Themen- und Vorwissenseiten; wer eine Animation neu baut,
  baut ihren Clip mit): Drehbuch-Feld
  `animation` (Anker des `h3`), Reihe «Animationen erklärt», `folge` = Nummer der
  Animation. Der Generator setzt dann «▶ Clip» in die Titelzeile der Animation,
  stellt den Clip auf der Seite in die Gruppe «Clips zu den Animationen» und
  hebt ihn in beiden Listen in Bernstein ab, mit dem Link «Anim» davor. Bilder
  darin sind Aufnahmen der Animation selbst (`bild` mit JPG,
  `.claude/tools/aufnahme-anim.mjs`); der Titel muss sich klar vom Stoff-Clip
  zum selben Thema unterscheiden. **Wird eine Animation geändert, zieht ihr
  Clip mit:** betroffene Bilder neu aufnehmen, Zahlen in Formelzeilen und
  Sprechertext an die Animation angleichen (Sprechertext geändert → neu
  vertonen), neu bauen, `pruef-clip`. Umgekehrt ist der Clipbau die
  gründlichste Prüfung einer Animation: Am 28.09.2026 kamen dabei rund
  dreissig Darstellungsfehler zum Vorschein — sie werden an der Animation
  behoben, nicht im Clip umgangen.
  Bauanleitung, Stolpersteine und die didaktische Prüfliste: `HOWTO-clips.md`.
  Seit 03.10.2026 kann der Generator (aus Mathe) auch **Koordinatenbilder**
  (`graf`) mit **Bewegung** und **Fragen im Clip** (`fragen`, vorgelesen über
  `scripts/build-clip-fragen-ton.py`); neue Clips nehmen das Theme
  `begreifbar-schlicht` (ohne Karo und Rand). Eine bewegte Gerade kann mit
  `"ab"` erst bei einem \(x\) beginnen (keine negative Zeit); der Fehler,
  durch den bewegte Geraden im Endzustand standen, ist seit 03.10.2026 behoben.
  Seit 07.10.2026 ist `build-clips.py` wieder dieselbe Datei wie in Mathe (nur
  `KARO_OHNE_ACHSEN`, `TEXTBREITE_BEGRENZEN` und der Seitenname sind Projektwerte): Teile im
  `graf` tragen eigenes `ein`/`aus`, Läufer fahren auch auf Kurven und kennen `lage`
  (HOWTO-clips, «Später einblenden, bewegen, mitlaufen»). Seit 08.10.2026 (dritte Runde aus Mathe)
  trägt jedes Element ein `aus`, auch `bild` und `formel`; dazu Kreisbewegung über einen Winkel,
  Grad-Kurven, Strecken als Klickziel u. a. (HOWTO-clips, «Dritte Runde»). Klickfragen: Liegt ein
  Tipp in mehreren Fallen, gewinnt die nächste. Bewegte Kurven mit `"gleichmaessig": true` laufen linear statt weich
  (laufende Wellen, seit 08.10.2026 aus Physik, von Mathe übernommen).
