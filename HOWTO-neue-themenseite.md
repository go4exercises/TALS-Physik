# HOWTO — Neue Themenseite anlegen

Schritt-für-Schritt-Anleitung für das Hinzufügen einer neuen RLP-Themenseite zu TALS-Physik. Folgt dem Master-Schema aus `STYLEGUIDE.md` §4.

> **Projektstand (Juni 2026):** Alle 10 RLP-Teilgebiete (p4-1 bis p6-2) sind vollständig ausgebaut. Diese Anleitung dient damit als Referenz für **zusätzliche oder optionale** Seiten über die RLP-Grundlagen hinaus (z.B. Magnetismus / Elektromagnetismus, Schwingungen) sowie als Nachschlagewerk für Aufbau und Konventionen. Als gespiegelte Vorlage eignet sich jede fertige Themenseite; als Referenzmuster für Animationsstruktur dient `p4-5-hydrostatik.html`.

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
   (Handout, Anki-Deck, Teste-dich-selbst, Aufgabenserie; der Formelauszug wird erstellt,
   aber seit 30.07.2026 nicht mehr verlinkt)
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

Pro Themenseite werden 4 Druckseiten und 1 Anki-Deck angelegt unter (verlinkt werden
auf der Themenseite nur Handout, Teste-dich-selbst, Aufgabenserie und das Anki-Deck —
der Formelauszug bleibt als Datei bestehen, ohne Link):

```
downloads/themen/p<lg>-<nr>-<kurzname>/
├── handout.html
├── formelauszug.html
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

## 6. Pre-Flight-Checks

Vor dem ZIP-Bauen mindestens diese Checks fahren (per `bash_tool` / `grep`):

### 6.1 Strukturelle Integrität

```bash
# Es muss genau ein page-wrap geben
grep -c 'class="page-wrap"' themen/p4-2-dynamik.html  # erwartet: 1
# Es muss genau ein content-main geben
grep -c 'class="content"' themen/p4-2-dynamik.html    # erwartet: 1
# nav.js, physiklib.js und anim-hinweise.js müssen eingebunden sein
grep -c 'src="../nav.js"' themen/p4-2-dynamik.html         # erwartet: 1
grep -c 'src="../suche.js"' themen/p4-2-dynamik.html       # erwartet: 1
grep -c 'src="../physiklib.js"' themen/p4-2-dynamik.html   # erwartet: 1
grep -c 'src="../anim-hinweise.js"' themen/p4-2-dynamik.html # erwartet: 1
```

### 6.1a Suchindex neu bauen

Eine neue Seite ist erst auffindbar, wenn der Index sie kennt (er liest die Seitenliste
aus `nav.js`):

```bash
python3 scripts/build-suchindex.py          # neu bauen — suchindex.js gehört in den Commit
python3 scripts/build-suchindex.py --check  # Exit 1 = veraltet; der Pre-Flight warnt ebenfalls
```

### 6.2 Aufgaben mit toggleL

Falls `toggleL` verwendet wird, muss `physiklib.js` eingebunden sein (es enthält die Funktion):

```bash
toggle_count=$(grep -c "toggleL(" themen/p4-2-dynamik.html)
lib_count=$(grep -c 'src="../physiklib.js"' themen/p4-2-dynamik.html)
if [ "$toggle_count" -gt 0 ] && [ "$lib_count" -eq 0 ]; then
  echo "FEHLER: $toggle_count Toggle-Aufrufe, aber physiklib.js nicht eingebunden"
fi
```

### 6.3 Keine erfundenen CSS-Klassen

Alle verwendeten Klassen sollten in `style.css` oder in der seitenspezifischen `<style>`-Sektion definiert sein. Übliche Verdächtige bei Physik: `.live-box`, `.cv-titel`, `.drei-spalten`, `.block-experiment`, `.lk.sim`.

```bash
# Alle Klassen extrahieren und sehen, ob sie irgendwo definiert sind:
grep -oE 'class="[^"]*"' themen/p4-2-dynamik.html | grep -oE '[a-z][a-z0-9-]+' | sort -u
```

### 6.4 buildNav-Signatur

```bash
grep -A6 "buildNav({" themen/p4-2-dynamik.html
# Muss id, kapitelNr, kapitelTitel, prev, next enthalten
```

### 6.5 LaTeX-Konventionen

- `\cdot` zwischen Zahl und Variable (siehe STYLEGUIDE §2.1)
- Dezimal**punkt** (nicht Komma)
- Einheiten in `\text{...}` mit `\;` davor

---

## 7. ZIP-Lieferung

```bash
cd /home/claude
zip -r tals-physik_phaseN.zip tals-physik/ -x "*.DS_Store" -x "*/__pycache__/*"
ls -lh tals-physik_phaseN.zip
```

Dann mit `present_files` ausliefern.
