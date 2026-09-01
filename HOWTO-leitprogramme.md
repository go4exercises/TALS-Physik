# HOWTO — ein Leitprogramm ins Repo holen

Ein Leitprogramm ist eine **eigenständige Seite zum selbständigen Durcharbeiten**:
Vorwissenstest, Kapitel in kleinen Schritten, Selbstkontrolle nach jedem Schritt,
am Schluss ein Kapiteltest. Es ist ein anderes Format als eine Themenseite und
behält darum sein eigenes Layout — geerbt werden nur Kopf, Fuss und die Bühne.

Übernommen aus `tals-mathe/HOWTO-leitprogramme.md` (Stand 1.9.2026) und um das
ergänzt, was beim ersten Physik-Übertrag (`leitprogramm-ideale-gase`, 31.8.2026)
zusätzlich nötig war.

---

## Die Übertragsliste

Der Reihe nach abarbeiten. Nach jedem Punkt steht, woran man merkt, dass er fehlt.

### 1. Datei nach `leitprogramme/<name>.html`

Genau **eine Ebene** unter der Wurzel, wie `clips/`. Alle relativen Pfade unten
setzen das voraus.

### 2. Fremde Hosts entfernen

Extern gebaute Dateien ziehen Schriften und MathJax typischerweise von Google und
einem CDN. Im Repo gilt: **keine Seite lädt etwas von einem fremden Host.**

```html
<link rel="stylesheet" href="../schriften.css">
<script src="../vendor/mathjax/tex-svg.js"></script>
```

Die `<link>`-Zeilen auf `fonts.googleapis.com`, `fonts.gstatic.com` und die
`preconnect` ersatzlos streichen. **Merkt man daran:** Der Pre-Flight meldet die
Hosts (`check_keine_fremdhosts`), und ohne Netz fällt die Seite auf Georgia zurück.

### 3. Dokumentrahmen und Zeichensatz

Von Hand gebaute Dateien beginnen gern direkt mit `<title>` — ohne `<!DOCTYPE>`,
ohne `<html>`, ohne `<head>`, ohne `<body>`. Ohne `<meta charset>` rät der Browser
die Kodierung, und über HTTP rät er falsch:

```
hÃ¤ngen · ErklÃ¤rung · â€"
```

Darum immer:

```html
<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
…
</head>
<body>
```

Das `charset` muss in den **ersten 1024 Bytes** stehen — also vor dem
SEO-Block, den `build-seo.py` nach dem `<title>` einsetzt.

**Merkt man daran:** Umlaute zerfallen — aber erst im Browser, nicht im Editor,
und in keiner Prüfung. Ohne Viewport ist zusätzlich die Mobilansicht kaputt.

### 4. Anker an die Kapitel

Die Volltextsuche schneidet ihre Abschnitte an `h2[id]`. Ohne `id` ist die ganze
Seite **ein** Treffer — beim Leitprogramm zu den idealen Gasen wären das 29 kB
Text unter einer einzigen Überschrift gewesen; mit Ankern sind es 13 Abschnitte.

Sitzt die `id` auf der umgebenden `<section>` und ist sie zugleich Sprungziel der
Ablaufspalte, **auf die Überschrift verschieben** statt sie zu verdoppeln: Der
Sprung funktioniert weiter und landet sogar präziser. Der Pre-Flight meldet
doppelte IDs.

### 5. Relative Basis für eingebettete Clips

Steht im Skript eine absolute Adresse

```js
var BASIS = 'https://physik.begreifbar.ch/';
```

dann kommen eingebettete Clips vom **Live-Stand**, nicht aus dem
Arbeitsverzeichnis. Eine lokale Vorschau zeigt den alten Clip, ohne Netz gar
keinen. Ersetzen durch `'../'`.

### 6. Kopf, Fuss und Bühne von der Site erben

```html
<link rel="stylesheet" href="../schriften.css">
<link rel="stylesheet" href="../style.css">   <!-- VOR dem eigenen <style> -->
…
<style> … eigenes Layout … </style>
```

**Die Reihenfolge ist der ganze Trick:** Der eigene `<style>` steht danach und
gewinnt bei gleichem Gewicht — das Layout des Leitprogramms bleibt unverändert.

Dazu im Körper:

```html
<body>
<div id="nav-root"></div>
…
<footer class="site-footer"> … </footer>
<script src="../physiklib.js"></script>
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script>buildNav({ id: 'leitprogramme' });</script>
</body>
```

`physiklib.js` bringt die Clip-Bühne mit (`clipBuehne`). Eine mitgelieferte Kopie
davon **löschen** — die Bühne ist überall dieselbe.

**Merkt man daran:** Ohne Kopf und Fuss ist die Seite eine Sackgasse — man kommt
nur mit dem Zurück-Knopf heraus.

### 7. Farbtokens erben, nicht kopieren

Extern gebaute Dateien tragen die Palette als eigenen `:root`-Block. Stimmt sie
mit `style.css` überein: **löschen**. Was bleibt, ist die Übersetzung abweichender
Namen (`:root{ --karte: var(--weiss); }`).

Beim Leitprogramm zu den idealen Gasen war das **nicht** der Fall: Es führt ein
eigenes Vokabular (`--ground`, `--surface`, `--ink`, `--accent`) mit eigenen
Werten. Dann bleibt der Block, wie er ist — die Palette nicht angleichen, sie
läuft sonst beim nächsten Update auseinander.

### 8. Dunkelmodus, falls die Datei einen hat

`style.css` kennt **keinen** — die Site hat keinen. Ein Leitprogramm darf einen
haben (man liest es am Stück), muss dann aber die geerbten Bausteine mitfärben.
Der Weg dazu ist **ein Token, nicht eine Liste von Klassen**: `style.css` färbt
seine Flächen über `--weiss`; ist das Token dunkel, ziehen Kopfleiste, Menü,
Suchfeld und Über-Panel von selbst nach.

```css
:root[data-theme="dark"]{ … --weiss:#201c16; --papier:#17140f; --tinte:#ede7de; … }
```

**Eine Ausnahme bleibt:** `.site-footer` benutzt `--tinte` als *Fläche*. Im
Dunkelmodus kippt `--tinte` mit dem Text nach hell — der Fuss würde weiss.

```css
:root[data-theme="dark"] .site-footer{
  background:var(--papier-2); color:var(--tinte-2); border-top:1px solid var(--linie);
}
:root[data-theme="dark"] .site-footer a{ color:var(--bernstein); }
```

> **Falle, die beim Physik-Übertrag zuschlug:** Die Systemvariante dieser Regel
> **muss in die Media-Abfrage**. Steht `:root:not([data-theme="light"]) .site-footer`
> global, trifft sie auch im **Hellmodus** zu — dort ist kein `data-theme` gesetzt —
> und färbt den Fuss fälschlich hell. Gemessen: `rgb(239,234,222)` statt
> `rgb(28,26,23)` wie auf jeder anderen Seite. Richtig:
>
> ```css
> @media (prefers-color-scheme: dark){
>   :root:not([data-theme="light"]) .site-footer{ … }
> }
> ```

### 9. Eintragen

| Datei | was |
|---|---|
| `leitprogramme.html` | Karte im Block zwischen den `LEITPROGRAMME`-Markern |
| `scripts/build-seo.py` | Zeile in `SEITEN` — sonst fehlen Beschreibung und Sitemap |
| `scripts/build-suchindex.py` | wird automatisch erfasst: alles in `leitprogramme/` |
| `nav.js` | nur beim **ersten** Leitprogramm nötig, der Menüeintrag steht schon |

Danach `python3 scripts/build-seo.py` und `python3 scripts/build-suchindex.py`.

---

## Prüfen

```bash
python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html leitprogramme.html
python3 -m http.server 8899 &
node .claude/tools/pruef-mathjax.mjs http://localhost:8899/leitprogramme/<name>.html
```

Der Pre-Flight prüft Skelett, Bibliotheks-Einbindung und Ressourcen-Sektion nur
für `themen/` — ein Leitprogramm hat bewusst kein `page-wrap` und kein
`main.content`. Fremdhosts und doppelte IDs prüft er überall.

**Was keine Prüfung sieht** — dafür in den Browser schauen, hell **und** dunkel,
1280 px und 360 px:

- zerfallene Umlaute (Punkt 3)
- eine weisse Kopfleiste über dunkler Seite (Punkt 8)
- ein heller Fuss im Hellmodus, weil die Dunkelregel zu weit greift (Punkt 8)
- ein Clip, der vom Live-Stand kommt statt aus `clips/` (Punkt 5)

Beim ersten Übertrag ist jeder dieser Punkte erst im Bild aufgefallen.

---

## Nicht tun

- **Das Leitprogramm nicht in `page-wrap` + `main.content` pressen.** Es ist ein
  anderes Format als eine Themenseite; das hiesse, sein Layout neu zu bauen.
- **Die Bühne nicht doppelt halten.** Sie steht in `physiklib.js` und `style.css`.
- **Die Palette nicht kopieren.** Sie stimmt heute und läuft morgen auseinander.
