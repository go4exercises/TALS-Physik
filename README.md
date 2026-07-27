# TALS Physik

Interaktives Lehrmittel für das Fach **Physik** der Berufsmaturität Technik, Architektur, Life Sciences — 1:1 nach RLP-BM 2030.

Schwesterprojekt zu [TALS Mathematik](https://github.com/go4exercises/tals-mathe). Gleicher Aufbau, gleiche didaktische Konventionen, gleiches Werkzeug — angepasst an das Fach Physik.

## Inhalt

3 Lerngebiete, 10 Teilgebiete, 160 Lektionen — alle Pflicht-Inhalte nach RLP-BM 2030 Ziff. 7.5.4.1 (Gruppe 1: Technik, Architektur, Life Sciences).

**Stand:** Alle 10 Teilgebiete vollständig ausgebaut (10/10 ✅). Jede Themenseite umfasst interaktive Canvas-Animationen, Aufgaben A1–A6, Zusammenfassung mit Merksatz, 5 Druckseiten/Materialien (Handout, Formelauszug, Anki-Deck, Teste-dich-selbst, Aufgabenserie) sowie eine dreispaltige Sektion mit externen Ressourcen.

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

Jede Themenseite folgt einem festen 13-Punkte-Master-Schema (siehe `STYLEGUIDE.md` §4):

1. Titel + RLP-Kompetenzen
2. Einstieg (konkretes Alltagsphänomen)
3. Grundbegriffe und Definitionen
4-9. Interaktive Animationen (5-10 pro Seite) mit eingebettetem Theorieteil
10. Aufgaben A1-A6 (zunehmend selbstständig)
11. Zusammenfassung mit Merksatz
12. Zusatzmaterial (5 Druckseiten: Handout, Formelauszug, Anki-Deck, Teste-dich-selbst, Aufgabenserie)
13. Externe Ressourcen — **dreispaltig**: 🎬 Videos · 🧪 Simulationen · 📝 Aufgaben

## Lokal testen

Da das Projekt vollständig statisch ist (HTML + CSS + JS), reicht ein einfacher Server:

```bash
cd tals-physik
python3 -m http.server 8000
```

Dann http://localhost:8000 öffnen. Alternativ direkt `index.html` im Browser öffnen — funktioniert auch, nur ohne MathJax-Live-Reload.

## Verwendete Technik

- **HTML5 + CSS3** für Layout und Stil (`style.css` für die ganze Site, kein Build-Schritt)
- **MathJax 3** (SVG-Output) für Formeln
- **Canvas 2D** für alle Animationen (keine externen Libraries)
- **physiklib.js** als geteilte Helper-Library (Canvas-Setup, Vektor-Pfeile, Zahlenformat)

## Version

**Version 0.9 · Stand Juni 2026** — alle zehn Themenseiten inhaltlich fertig; vor der ersten GitHub-Pages-Veröffentlichung. Die Versionszeile steht zusätzlich im Footer jeder Seite.

## Changelog

**Ab 14.06.2026 führt der Git-Verlauf die Änderungen** (`git log --oneline`). [`CHANGELOG.md`](CHANGELOG.md) ist abgeschlossen und dokumentiert die Projektgeschichte bis Phase 5.41 (13.06.2026) aus der Zeit vor der Git-Umstellung; dort wird nichts mehr nachgetragen. Stand und Begründungen der laufenden Animations-Überarbeitung stehen in [`TODO-animationen.md`](TODO-animationen.md).

## Lizenz

Inhalte erstellt mit Unterstützung von Claude (Anthropic).
Veröffentlicht unter [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.de) — frei nutzbar für nicht-kommerzielle Zwecke.

## Feedback

Fehler oder Verbesserungen bitte über den [GitHub-Issue-Tracker](https://github.com/go4exercises/tals-physik/issues) melden.
