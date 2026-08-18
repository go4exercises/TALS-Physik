# HOWTO — Neue Themenseite anlegen

Schritt-für-Schritt-Anleitung für das Hinzufügen einer neuen RLP-Themenseite zu TALS-Physik. Folgt dem Master-Schema aus `STYLEGUIDE.md` §4.

> **Projektstand (August 2026):** Alle 10 RLP-Teilgebiete (p4-1 bis p6-2) sind vollständig ausgebaut, dazu die fünfteilige Vorwissen-Reihe p0-0 bis p0-4. Diese Anleitung dient damit als Referenz für **zusätzliche oder optionale** Seiten über die RLP-Grundlagen hinaus (z.B. Magnetismus / Elektromagnetismus, Schwingungen) sowie als Nachschlagewerk für Aufbau und Konventionen. Als gespiegelte Vorlage eignet sich jede fertige Themenseite; als Referenzmuster für Animationsstruktur dient `p4-5-hydrostatik.html`.

---

## 1. Vorbereitung

### 1.1 RLP-Kompetenzen extrahieren

Aus dem RLP-BM 2030 (im Project-Knowledge als `physik.pdf`) die Kompetenzen für das jeweilige Teilgebiet 1:1 herausziehen. Beispiel für 4.2 Dynamik:
- Die drei Newtonschen Gesetze beschreiben und auf Aufgabenstellungen anwenden
- Trägheits- und Federkräfte berechnen
- Gleitreibung und Haftreibung definieren und Aufgaben dazu lösen
- … (siehe physik.pdf Seite 2)

### 1.2 Skript-Kapitel überfliegen

Das entsprechende PDF aus dem Project-Knowledge ansehen (z.B. `2_PhysikBMDynamik.pdf` für 4.2):
- Welche Begriffe deckt das Skript ab, die im RLP nicht expliziert sind, aber didaktisch dazugehören?
- Welche Beispielszenarien sind in der BM üblich? (Auto auf Strasse, Lift, schiefe Ebene, …)
- Welche Spezialfälle und Aufgabenstellungen werden behandelt?

Ergebnis ist eine Vollständigkeits-Checkliste, KEINE Vorlage zum Abschreiben.

### 1.3 Animationsplan skizzieren

5-10 Canvas-Animationen pro Themenseite. Beispielplan für 4.2 Dynamik:
1. Trägheit (Auto bremst, Insasse fährt weiter)
2. F=m·a mit Schiebern für m und F
3. Aktio = Reaktio (zwei Kugeln, Impulserhaltung)
4. Reibung auf schiefer Ebene (Winkel-Schieber)
5. Federkraft (Hookesches Gesetz mit Schieber für x)
6. Atwoodsche Fallmaschine (zwei Massen, Beschleunigung)

---

## 2. HTML-Datei erstellen

### 2.1 Pfad und Benennung

```
themen/p<lerngebiet>-<nr>-<kurzname>.html
```

Beispiele:
- `themen/p4-1-kinematik.html`
- `themen/p4-2-dynamik.html`
- `themen/p5-1-temperatur.html`

Kurzname: in Kleinbuchstaben, mit Bindestrichen, ohne Umlaute (statt `wärmeausdehnung` → `waermeausdehnung`).

### 2.2 Skelett

Mindestens muss vorhanden sein:

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>X.Y Themenname — TALS Physik</title>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4...&family=Source+Sans+3...&family=JetBrains+Mono...&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  <!-- MathJax-Setup wie in p4-1-kinematik.html -->
  <style>/* Widget-Styles spezifisch für diese Seite */</style>
</head>
<body>
  <div id="nav-root"></div>
  <div class="page-wrap">
    <main class="content">
      <!-- 13-Punkte-Master-Schema -->
    </main>
    <aside class="toc-wrap"><div id="toc"></div></aside>
  </div>
  <footer class="site-footer">…</footer>
  <script src="../nav.js"></script>
  <script src="../suche.js"></script>
  <script src="../physiklib.js"></script>
  <script src="../anim-hinweise.js"></script>
  <script>
    buildNav({ id: 'p4-2', kapitelNr: '4.2', kapitelTitel: 'Dynamik',
               prev: { nr: '4.1', titel: 'Kinematik des Schwerpunkts', url: 'p4-1-kinematik.html' },
               next: { nr: '4.3', titel: 'Energie', url: 'p4-3-energie.html' } });
    // … Animationscode …
  </script>
</body>
</html>
```

### 2.3 Vorlage zum Spiegeln

Die beste Vorlage ist `themen/p4-1-kinematik.html`. Reihenfolge zum Bauen:

1. Skelett kopieren, IDs anpassen
2. Punkt 1 (Titel + RLP) ausfüllen
3. Punkt 2 (Einstieg) — ein kurzer Phänomen-Block
4. Punkt 3 (Definitionen) — pro Begriff ein `.block-def`
5. Animationen anlegen (jeweils mit `<canvas id="aN-cv">` + zugehörige `drawAN()`-Funktion)
6. Aufgaben A1-A6 — **alle** im einheitlichen `block-aufg`-Muster (STYLEGUIDE §5.5), nie das alte `aw`-System
7. Zusammenfassung
8. Zusatzmaterial — die Druckseiten-Links zeigen auf `../downloads/themen/p4-2-dynamik/...`
   (Handout, Anki-Deck, Teste-dich-selbst, Aufgabenserie)
9. Externe Ressourcen — Sektion 13 nach HOWTO-externe-ressourcen.md

---

## 3. Animationscode

### 3.1 Standardmuster für Schieber-Animation

```js
function drawA1() {
  const v  = +document.getElementById('a1-v').value;
  document.getElementById('a1-v-val').textContent = v + ' m/s';

  const cv = initCanvas('a1-cv', 280, false);
  const grid = drawGrid(cv.ctx, cv.W, cv.H, -1, 11, -5, 50);
  drawAxesUnits(cv.ctx, cv.W, cv.H, grid.cx, grid.cy, 't [s]', 's [m]');

  // ... eigentliche Zeichnung
  cv.ctx.strokeStyle = '#8a4a0e';
  cv.ctx.lineWidth = 2.8;
  // ...
}
document.getElementById('a1-v').addEventListener('input', drawA1);
```

**Achsen-Wertebereich klug wählen** (`drawGrid` wählt Tick-Schritte automatisch — siehe STYLEGUIDE §3.4):
- Etwas Reserve links/unten: `-0.5, hMax+0.5, -pMax*0.05, pMax*1.05` statt `0, hMax, 0, pMax`
- Werte in passender Einheit aufbereiten (Pa → kPa, N → kN, m → cm), damit Tick-Werte ein- bis dreistellig bleiben
- Bei sehr grossen Bereichen (z.B. `0..1334 kPa`) ist nichts zu tun — `niceStep` wählt 200er-Schritte automatisch

### 3.2 Standardmuster für RAF-Animation (Play/Pause)

Siehe Animation 3 (Freier Fall) und Animation 5 (Kreisbewegung) in `p4-1-kinematik.html`.

### 3.3 Globale renderAll() + resize

Alle Animationen müssen sich nach Fenstergrösse anpassen:

```js
function renderAll() {
  drawA1(); drawA2(); drawA3(); /* ... */
}
document.addEventListener('DOMContentLoaded', renderAll);
window.addEventListener('resize', renderAll);
```

### 3.4 Animations-Hinweise in der Titelzeile

Jede Animation erhält statt der Bedienungszeile unter dem Titel eine `<div class="widget-titelzeile">`, die den `<h3>`-Titel und die beiden Rollover-Hinweise «💡 Worauf achten?» und «✓ Erkenntnis» auf einer Zeile bündelt (Muster und Inhaltsregeln: STYLEGUIDE §5.6). Gestaltung kommt aus `style.css`, die Logik aus `anim-hinweise.js` — also nichts pro Seite duplizieren, nur das Markup einsetzen. Wichtig: sichtbarer Text in Projekt-Notation `\(…\)`.

Der `<h3>` trägt einen **Anker**, die Nummer schreibt der Generator (STYLEGUIDE §5.9):

```html
<h3 id="anim-schiefer-wurf">Animation 4 · Schiefer Wurf</h3>
…
Probe mit <a class="anim-ref" href="#anim-schiefer-wurf">Animation 4</a> (Winkel 40°) …
```

Nach jedem Einfügen, Löschen oder Verschieben einer Animation `python3 scripts/build-animationen.py` laufen lassen — er zieht Titel- und Verweisnummern gemeinsam nach, sodass ein Einschub keinen Textverweis mehr brechen kann. Nummern nie von Hand setzen; der Pre-Flight meldet Abweichungen als `[FEHLER]`.

---

## 4. Navigation aktualisieren

### 4.1 nav.js

In `nav.js` sind alle bestehenden Themenseiten der Sidebar über die zentrale Seitenliste (`id`/`nr`/`titel`/`url`) erfasst; ein Status-Feld („fertig\"/„geplant\") führt `nav.js` nicht — der Status lebt allein in den Karten von `index.html`. **Für eine zusätzliche Seite genügt ein neuer Listeneintrag** mit korrekter `url`, sobald die HTML-Datei am erwarteten Pfad existiert. Das «Ausblick»-Panel in `nav.js` (Abschnitte „Erstellt\"/„Ideen für den Ausbau\") bei Bedarf an den neuen Stand anpassen.

### 4.2 index.html

Auf der Index-Seite die Karte von `.karte geplant` auf `.karte fertig` umstellen:

```html
<a href="themen/p4-2-dynamik.html" class="karte fertig">
  <span class="k-id">4.2</span>
  <span class="k-tit">Dynamik</span>
</a>
```

Und im Stats-Block die Zahlen anpassen: `fertig` hochzählen, `geplant` herunterzählen (Stand nach Abschluss aller RLP-Teilgebiete: `fertig: 10`, `in Arbeit: 0`, `geplant: 0`). Eine zusätzliche Seite über die 10 RLP-Teilgebiete hinaus erhöht entsprechend `fertig` und die Teilgebiet-Gesamtzahl.

### 4.3 prev/next in Nachbar-Seiten

Die buildNav-Aufrufe der Nachbar-Themenseiten anpassen, sodass sie auf die neue Seite zeigen.

---

## 5. Druckseiten (Zusatzmaterial)

Pro Themenseite werden 3 Druckseiten und 1 Anki-Deck angelegt unter:

```
downloads/themen/p<lg>-<nr>-<kurzname>/
├── handout.html
├── ankideck.apkg
├── teste-dich-selbst.html
└── aufgabenserie.html
```

Skelett aus der Pilot-Themenseite p4-1 holen (`downloads/themen/p4-1-kinematik/...`) und anpassen:
- Header umtitulieren („Handout — Theorie zu Dynamik")
- Backlink ändern: `../../../themen/p4-2-dynamik.html#downloads`
- Inhalte 1:1 aus der Themenseite übernehmen (nur Theorie-Teile, keine Animationen — die Druckseiten sind reine A4-Theorie)

CSS in `downloads/print.css` (gespiegelt aus Mathe mit Bernstein-Akzent).

---

## 6. Pre-Flight

Die Handprüfungen von früher sind abgelöst: Alles, was hier stand — Skelett,
Klassen, physiklib-Abhängigkeit, buildNav, LaTeX-Konventionen —, prüft das
Skript automatisch und gründlicher.

```bash
python3 .claude/skills/preflight/preflight.py themen/<datei>.html
# oder über alle: python3 .claude/skills/preflight/preflight.py themen/*.html
```

Erwartete Ausgabe: `ALLE CHECKS BESTANDEN`. Jede `[FEHLER]`-Meldung wird vor dem
Commit behoben, `[WARN]` ist kein Blocker. Was geprüft wird, steht in `CLAUDE.md`
im Abschnitt Pre-Flight; die Details stehen im Skript selbst.

Vor dem Pre-Flight laufen bei Bedarf die Generatoren:

```bash
python3 scripts/build-animationen.py   # Animationsnummern aus der Dokumentreihenfolge
python3 scripts/build-suchindex.py     # Volltextindex; suchindex.js gehört in den Commit
python3 scripts/build-seo.py           # Metadaten, sitemap.xml, robots.txt
```

Neue Seite? Dann zusätzlich: Eintrag in `nav.js` (SITE und GROUPS), Karte in
`index.html`, `prev`/`next` der Nachbarseiten und die Tabelle `SEITEN` in
`scripts/build-seo.py`.

---

## 7. Ausliefern

Es gibt keine ZIP-Lieferung mehr. Der Git-Verlauf ist die Dokumentation, und die
Veröffentlichung läuft über GitHub Pages:

```bash
git add -A
git commit -m "p4-2: … "   # Seite + was geändert wurde
```

`git push` bleibt beim Auftraggeber (siehe `CLAUDE.md`).
