# TALS Physik

Interaktives Lehrmittel für das Fach **Physik** der Berufsmaturität Technik, Architektur, Life Sciences — 1:1 nach RLP-BM 2030.

Schwesterprojekt zu [TALS Mathematik](https://github.com/go4exercises/tals-mathe). Gleicher Aufbau, gleiche didaktische Konventionen, gleiches Werkzeug — angepasst an das Fach Physik.

## Inhalt

3 Lerngebiete, 10 Teilgebiete, 160 Lektionen — alle Pflicht-Inhalte nach RLP-BM 2030 Ziff. 7.5.4.1 (Gruppe 1: Technik, Architektur, Life Sciences).

**Stand:** Alle 10 Teilgebiete vollständig ausgebaut (10/10 ✅). Jede Themenseite umfasst interaktive Canvas-Animationen, Aufgaben A1–A6, Zusammenfassung mit Merksatz, Zusatzmaterial (Handout, Anki-Deck, Teste-dich-selbst, Aufgabenserie) sowie eine dreispaltige Sektion mit externen Ressourcen.

Davor steht die **Vorwissen-Reihe** (Themenkreis 0, kein RLP-Lerngebiet, 5 Seiten): 0.0 Alltagstour, 0.1 Rechnen und Schliessen, 0.2 Grössen, Einheiten und Messen, 0.3 Messen — Waagen, Dichte, Einheiten, 0.4 Einheitentrainer. Diese Seiten folgen dem 13-Punkte-Schema nur sinngemäss; 0.4 ist eine reine Übungsseite mit Freiem Üben, Lernmodus und Prüfungsmodus.

| Nr | Teilgebiet | Lektionen | Status |
|----|------------|----------:|--------|
| **4 — Mechanik** | | **100** | |
| 4.1 | Kinematik des Schwerpunkts | — | ✅ fertig |
| 4.2 | Dynamik | — | ✅ fertig |
| 4.3 | Energie | — | ✅ fertig |
| 4.4 | Statik von Festkörpern | — | ✅ fertig |
| 4.5 | Hydrostatik | — | ✅ fertig |
| **5 — Thermodynamik** | | **30** | |
| 5.1 | Temperatur | — | ✅ fertig |
| 5.2 | Wärme | — | ✅ fertig |
| 5.3 | Wärmeausdehnung | — | ✅ fertig |
| **6 — Einführung in andere Bereiche** | | **30** | |
| 6.1 | Wellen | — | ✅ fertig |
| 6.2 | Elektrizität | — | ✅ fertig |

## Aufbau einer Themenseite

Jede Themenseite der Lerngebiete 4 bis 6 folgt einem festen 13-Punkte-Master-Schema (siehe `STYLEGUIDE.md` §4); die Vorwissenseiten des Themenkreises 0 halten sich nur sinngemäss daran (kein Zusatzmaterial, keine externen Ressourcen):

1. Titel + RLP-Kompetenzen
2. Einstieg (konkretes Alltagsphänomen)
3. Grundbegriffe und Definitionen
4-9. Interaktive Animationen (5-10 pro Seite) mit eingebettetem Theorieteil
10. Aufgaben A1-A6 (zunehmend selbstständig)
11. Zusammenfassung mit Merksatz
12. Zusatzmaterial (Handout, Anki-Deck, Teste-dich-selbst, Aufgabenserie)
13. Externe Ressourcen — **dreispaltig**: 🎬 Videos · 🧪 Simulationen · 📝 Aufgaben

## Lokal testen

Da das Projekt vollständig statisch ist (HTML + CSS + JS), reicht ein einfacher Server:

```bash
cd tals-physik
python3 -m http.server 8000
```

Dann http://localhost:8000 öffnen. Alternativ direkt `index.html` im Browser öffnen — funktioniert auch, nur ohne MathJax-Live-Reload.

## Suche

Das Suchfeld oben rechts im Header durchsucht den Fliesstext aller Themenseiten sowie
Glossar und Formelsammlung — ohne Server, rein im Browser (`/` oder Strg/Cmd+K springt
ins Feld). Grundlage ist `suchindex.js`, erzeugt aus den Seiten:

```bash
python3 scripts/build-suchindex.py            # Index neu bauen
python3 scripts/build-suchindex.py --check    # prüft, ob er zum Stand passt
python3 scripts/build-suchindex.py --dry-run  # bauen und berichten, nichts schreiben
```

Der Generator ist projektübergreifend: er erkennt Physik und Mathe an der
Canvas-Bibliothek im Repo-Root und liest die Seitenliste aus `nav.js` — egal ob das
Projekt eine Liste führt oder mehrere. `--root PFAD` zielt aufs Schwesterprojekt.

Der Index wird erst beim ersten Tastendruck im Suchfeld nachgeladen. Nach jeder
inhaltlichen Änderung neu bauen — der Pre-Flight warnt, wenn er veraltet ist.
Nicht im Index: Mini-Checks, Verständnisfragen, Aufgaben, Zusatzmaterial und
externe Ressourcen.

## Auffindbarkeit

Jede Seite trägt eine eigene Beschreibung, `canonical`, Open-Graph-Daten für
Link-Vorschauen und strukturierte Daten nach `schema.org/LearningResource` (LRMI) —
inklusive Lizenz, Bildungsstufe, Zielgruppe und der RLP-Kompetenzen, die direkt aus
der Seite gelesen werden. Dazu `sitemap.xml` und `robots.txt`.

```bash
python3 scripts/build-seo.py            # Metadaten, sitemap.xml, robots.txt schreiben
python3 scripts/build-seo.py --check    # prüft, ob sie zum Stand passen
```

Gepflegt wird die Tabelle `SEITEN` im Skript; der Block in den Seiten selbst ist
generiert. Die Suche nimmt `?q=…` entgegen (`…/index.html?q=reibung`), darauf stützt
sich die `SearchAction` in den strukturierten Daten.

## Verwendete Technik

- **HTML5 + CSS3** für Layout und Stil (`style.css` für die ganze Site, kein Build-Schritt)
- **MathJax 3** (SVG-Output) für Formeln
- **Canvas 2D** für alle Animationen (keine externen Libraries)
- **physiklib.js** als geteilte Helper-Library (Canvas-Setup, Vektor-Pfeile, Zahlenformat)

## Version

**Version 1.0 · Stand 1. August 2026** — alle zehn Themenseiten inhaltlich fertig, dazu Vorwissen, Glossar, Formelsammlung, Volltextsuche und die Seite Rechtliches & Datenschutz. Die Versionszeile steht zusätzlich im Footer jeder Seite.

Seither hinzugekommen, ohne dass die Versionszeile angehoben wurde: die Vorwissenseiten 0.3 und 0.4 sowie die Extras-Seite zur Sonnenfinsternis vom 12. August 2026.

## Änderungen

Der **Git-Verlauf** ist die Änderungsdokumentation: `git log --oneline`. Eigene
Changelog- oder TODO-Dateien werden nicht geführt.

## Lizenz

Inhalte erstellt mit Unterstützung von Claude (Anthropic).
Veröffentlicht unter [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.de) — frei nutzbar für nicht-kommerzielle Zwecke.

## Feedback

Fehler oder Verbesserungen bitte über den [GitHub-Issue-Tracker](https://github.com/go4exercises/tals-physik/issues) melden.
