# Leitprogramme — Details

Aus der Wurzel-`CLAUDE.md` ausgelagert (11.10.2026, /doctor): Claude Code lädt diese Datei, sobald in diesem
Ordner gearbeitet wird. Die Regeln der Wurzel-`CLAUDE.md` gelten weiter; bei Widerspruch gilt STYLEGUIDE.md.

- `leitprogramme.html` + `leitprogramme/` — **Selbstlerneinheiten**, aktuell vierzehn: zehn nach dem Kapitelmuster (`leitprogramm-elektrizitaet`, `leitprogramm-kinematik`, `-dynamik`, `-energie`, `-statik`, `-hydrostatik`, `-temperatur`, `-waerme`, `-ausdehnung`, `-wellen`) und vier klassische (unten):
  `leitprogramm-rechnen` (Proportionalität, Dreisatz, Umstellen,
  Zehnerpotenzen, Bogenmass, Plausibilität — sechs Clips, fünf Simulationen),
  `leitprogramm-vorwissen` (Grössen, Messen, Druck — sieben Clips, fünf
  Simulationen) und `leitprogramm-experimente-waerme` (der Einstieg
  über sieben Schulversuche statt über die Formel — sechs Clips, sieben
  gerechnete Simulationen), dazu der Prüfungsbogen (unten). Die drei früheren Elektrizitäts-Leitprogramme
  (`leitprogramm-schaltungen`, `-widerstand-leistung`, `-gefahren`) sind seit
  dem 06.10.2026 im Leitprogramm Elektrizität und auf der Themenseite 6.2
  aufgegangen (TODO-E), die vier klassischen der Wärmelehre
  (`leitprogramm-waermemenge`, `-heizen`, `-waermeausdehnung`, `-ideale-gase`) seit dem
  08.10.2026 in den Leitprogrammen Temperatur, Wärme und Wärmeausdehnung und Gase
  (5.1 bis 5.3). Sie stehen bis zur Löschung noch als **veraltet** im
  Netz: roter Hinweis im Seitenkopf mit Links auf die Kapitel des neuen
  Leitprogramms, eigener Abschnitt «Veraltet: wird entfernt» auf
  `leitprogramme.html`, `noindex` in `build-seo.py`, in `UNVERLINKT` von
  `build-suchindex.py`. Gelöscht werden sie auf Anweisung des Auftraggebers;
  dann an ihre Adressen Weiterleitungen auf die Themenseite (Muster im
  Git-Verlauf, Commit c0a56ec). Dazu als Sonderfall `uebungstest-waermelehre` — ein
  **Prüfungsbogen statt eines Stoffgebiets**: fünfzehn Aufgaben, je eine mit
  Aufgabentext, eigenem Erklärclip, Musterlösung und Fehlerkasten, dazu die
  Darstellungsregeln als roter Faden (16.09.2026). Alle starten ihre
  Clips über `.clipkarte`
  aus `clips/`; eigener, ins Dokument eingebetteter Ton gehört nicht hinein
  (siehe `HOWTO-leitprogramme.md`, §12 Punkt 11). Vorgehen beim
  Übertrag einer fremden Datei **und** beim Schreiben einer neuen:
  `HOWTO-leitprogramme.md` — seit 03.10.2026 Mathes Gesamtfassung, an Physik
  angepasst (RLP-Bindung, Planung, Kapitelmuster, Übungen, PDF-Gesamttest,
  Prüfung vor der Freischaltung; die früheren zwölf Punkte mit Fehlerbild in
  §12), verbindlich dahinter STYLEGUIDE §6.5. Gilt für **neue** Leitprogramme;
  die klassischen bleiben, ob ihre HTML-Gesamttests auf PDF
  (`scripts/build-lp-pdf.py`, `downloads/leitprogramme/lp-druck.sty`) umgestellt
  werden, ist offen. Vor der Freischaltung: Skill `/lp-pruefung` (drei
  Prüfagenten; Werkzeuge `.claude/tools/pruef-uebungen.mjs`, `pruef-leiste.mjs`,
  `pruef-fragen.mjs`, `sprechzeiten.py` und `pruef-formelsatz.mjs` — Letzteres setzt
  die Zufallsübungen mit echtem MathJax, das `pruef-uebungen` abschaltet). Erstes Leitprogramm nach dem
  Kapitelmuster: `leitprogramm-elektrizitaet` (6.2, fünf Kapitel, zehn eigene
  Clips `p6-2-lp-*` mit `probe: true`, Gesamttest als PDF), gebaut mit
  `scripts/lp/elektrizitaet/` (README dort) — freigeschaltet am 03.10.2026 nach
  `/lp-pruefung`; als zweites folgte `leitprogramm-kinematik` (4.1, `scripts/lp/kinematik/`,
  freigeschaltet am 04.10.2026), dann Dynamik, Energie, Statik und Hydrostatik
  (4.2 bis 4.5, `scripts/lp/<name>/`, freigeschaltet am 06.10.2026), zuletzt Temperatur,
  Wärme und Wärmeausdehnung und Gase (5.1 bis 5.3, `scripts/lp/temperatur/`, `waerme/`,
  `ausdehnung/`, freigeschaltet am 08.10.2026), dann Wellen (6.1, `scripts/lp/wellen/`,
  freigeschaltet am 09.10.2026 nach fünf Prüfrunden) (eine Erprobung läuft unverlinkt: `noindex` in `build-seo.py`,
  Menge `UNVERLINKT` in `build-suchindex.py`, keine Karte). Für eine
  Seite aus einem Prüfungs-PDF zusätzlich `HOWTO-uebungspruefung.md` (PDF
  misstrauisch lesen, `probe: true` für die Clips, die `</head>`-Falle, und
  wie ein Prüfungsrahmen wegbleibt, ohne dass die Aufgaben leiden). Die
  Bibliotheksseite trägt nur die Kacheln — seit 07.10.2026 wie in Mathe eine je
  Leitprogramm (Kopf: Titel des Leitprogramms, darunter je Themenseite eine Zeile mit
  Nummernpille; CSS im `<style>` der Seite; die alten `.lp-*`-Karten in `style.css` nur noch
  für «Veraltet: wird entfernt»); jedes
  Leitprogramm ist eine **eigenständige Seite mit eigenem Inhalts-CSS**; Aufbau
  und Ablauf sind auf das Leitprogramm zugeschnitten. Kopfnavigation und Suche
  gehören trotzdem dazu: vor `</body>` stehen `../physiklib.js`, `../nav.js`,
  `../suche.js` und `buildNav({ id: 'leitprogramme' })` — ohne `physiklib.js`
  läuft jede Clipkarte ins Leere, weil `clipBuehne` von dort kommt (so bei
  `leitprogramm-schaltungen` vom 13.09. bis 27.09.2026). Verbindlich bleiben: keine Fremdhosts
  (`../schriften.css`, `../vendor/mathjax/tex-svg.js`) und je ein Anker auf den
  `<h2>`, damit `build-suchindex.py` dort Abschnitte schneiden kann.
