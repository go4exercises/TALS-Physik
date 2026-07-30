# TODO — systemische Anpassungen auf TALS-Mathe übertragen

Diese Änderungen wurden in **TALS-Physik** gemacht und betreffen das gemeinsame Skelett
(CSS + Canvas-Bibliothek). Da TALS-Mathe dasselbe Skelett nutzt, sollten sie dort
1:1 nachgezogen werden — **aber nur die Layout-/Positions-Eigenschaften, nicht die Farben**:
Mathe hat Blau als Leitfarbe, Physik Bernstein. Beim Kopieren von CSS-Regeln die jeweils
eigenen Farb-Variablen (`--blau*` statt `--bernstein*`) der Mathe-Seite belassen.

> Vor dem Übertragen prüfen, ob die Klassennamen / Dateinamen in Mathe identisch sind
> (`style.css`, `physiklib.js` bzw. das dortige Pendant, `.live-box`, `.anim-hinweis`,
> `.widget-titelzeile`). Wo sie abweichen, Selektoren entsprechend anpassen. **Nicht
> jede Physik-Struktur hat in Mathe ein Pendant** — §2 unten ist das Beispiel dafür.
> Nach jeder Änderung den Mathe-Pre-Flight laufen lassen und einen Render-Check bei
> 1280 px **und** 360 px machen. Mathe hat dafür `.claude/tools/screenshot-widgets.mjs`;
> in Physik läuft Playwright seit dem 26.07.2026 lokal (Chromium unter
> `~/.cache/ms-playwright/`), ein eigenes Werkzeugskript fehlt hier noch.

> **Status-Hinweis:** Der massgebliche Stand steht in der Mathe-Kopie dieser Datei
> (`/home/paps/tals-mathe/TODO-port-to-tals-mathe.md`) — dort wird abgehakt, was
> tatsächlich portiert wurde. Diese Physik-Kopie ist die Absenderliste und wurde am
> 28.07.2026 mit dem Mathe-Stand abgeglichen.
>
> **§§ 6–10 ergänzt am 29.07.2026** (Suche, klebender Header, Rechtliches/Footer,
> Startseite, Kleinteiliges). Die Angaben zum Mathe-Stand darin sind am 29.07.2026
> direkt im Mathe-Repo nachgesehen, nicht geschätzt.

---

## 1. Canvas-Beschriftungen: Mindestgrösse 13 px  (Lesbarkeit)

**Was:** Alle Canvas-Schriftgrössen (`ctx.font = '…px …'`) unter 13 px wurden auf 13 px
angehoben — über alle Themenseiten **und** in `physiklib.js` (dort u. a. Achsen-Zahlen
11→13, Achsen-Einheiten/Pfeil-Labels 12→13). `bold` bleibt erhalten, ≥ 13 px unverändert.
Die Hierarchie trägt danach `bold` vs. normal.

**Warum:** 10–11 px sind auf den dpi-skalierten Canvas zu klein gegenüber dem Fliesstext.

**Wie (Skript, im Mathe-Repo-Root ausführen, Dateinamen ggf. anpassen):**

```python
import re, glob
FLOOR = 13
pat = re.compile(r"(font\s*=\s*'(?:bold )?)(\d+(?:\.\d+)?)px")
def bump(m):
    pre, size = m.group(1), float(m.group(2))
    return f"{pre}{FLOOR}px" if size < FLOOR else m.group(0)
# 'physiklib.js' ggf. durch den Namen der Mathe-Canvas-Bibliothek ersetzen
for f in sorted(glob.glob('themen/*.html')) + ['physiklib.js']:
    s = open(f, encoding='utf-8').read()
    changed = sum(1 for m in pat.finditer(s) if float(m.group(2)) < FLOOR)
    if changed:
        open(f, 'w', encoding='utf-8').write(pat.sub(bump, s))
        print(f"{changed:3}  {f}")
```

**Prüfen:** danach `grep -rE "font\s*=\s*'(bold )?(7|8|9|10|11|12)px" themen/*.html <lib>.js`
darf nichts mehr finden. Lange Satz-Beschriftungen auf 360 px gegen Überlauf sichten
(in Physik der einzige Restpunkt).

- [x] Skript in Mathe ausgeführt — 21 HTML-Seiten (grundlagen + schwerpunkt) und
  `mathlib.js` (Achsen-Zahlen 11→13, Achsen-Labels `bold 11`→`bold 13`).
- [x] keine `<13px`-Fonts mehr vorhanden (`grep` über grundlagen/schwerpunkt/mathlib.js leer)

---

## 2. Live-Box: grosszügiger Spaltenabstand  (`style.css`)

**Was:** Spaltenabstand der Wert-Boxen von `14px` auf **`14px 70px`** (Zeile/Spalte).
Dichte Boxen (≥ 4 Werte) bekommen den engen Abstand zurück.

**Warum:** Mehr horizontaler Abstand liest sich deutlich besser; getrennter Zeilen-/
Spaltenabstand hält die Werte beim Umbruch (Mobile) trotzdem eng beieinander.

**Diff (nur die `gap`-Zeile ändern + zwei neue Regeln; Farben/Übriges der Box lassen):**

```css
/* vorher: .live-box { … gap:14px … } */
.live-box { … gap:14px 70px … }
/* dichte Boxen gestuft verkleinern — NICHT bis auf den Zeilenabstand */
.live-box:has(> .lb-item:nth-child(4)) { column-gap:40px; }
.live-box:has(> .lb-item:nth-child(6)) { column-gap:24px; }
```

**Hinweis:** `:has()` ist seit Ende 2023 Baseline (alle aktuellen Browser) — für GitHub
Pages unkritisch.

> **KORREKTUR (27.07.2026):** Der ursprüngliche Vorschlag liess dichte Boxen (4+ Werte)
> auf `column-gap:14px` zurückfallen — also auf den Zeilenabstand. Das ist in Physik
> aufgefallen, sobald eine Animation einen vierten Wert bekam: die Werte klebten
> zusammen und waren nicht mehr als getrennte Grössen lesbar. Richtig ist die
> **gestaffelte** Verkleinerung 70 / 40 / 24 px oben. Wer den alten Stand kopiert,
> baut den Fehler nach. Daraus wurde Stilcheck-Regel 1 (STYLEGUIDE §5.3).

> **NICHT ÜBERTRAGBAR (2026-06-24, in Mathe geprüft):** TALS-Mathe hat keine
> `.live-box`/`.lb-item`-Struktur. Live-Werte stehen dort als vertikale Legende
> (`.legende` / `.legende-zeile`) oder inline als `.wert`-Spans in der Formel. Es gibt
> also keinen Spaltenabstand zwischen nebeneinanderliegenden Wert-Boxen, der sich
> vergrössern liesse — kein passendes Pendant. Punkt entfällt für Mathe.

- [~] `gap:14px 70px` gesetzt — entfällt (kein `.live-box` in Mathe, s. o.)
- [~] gestaffelte `:has()`-Ausnahmen ergänzt — entfällt (s. o.)

---

## 3. Animations-Hinweise: Rollover öffnet nach links, kein Abschneiden  (`style.css`)

**Was:** „Worauf achten?" und „Erkenntnis" stehen jetzt **beide am rechten Zeilenende**
und ihre Rollover öffnen **nach links** (vorher öffnete „Worauf achten?" nach rechts und
wurde bei schmalem Fenster abgeschnitten).

**Warum:** Das nach rechts öffnende Rollover lief aus dem Rahmen; rechtsbündig + nach
links öffnend passt auf jeder Breite.

**Diff (4 Stellen im `.anim-hinweis`/`.widget-titelzeile`-Block):**

```css
/* a) Titelzeile wird Bezugsrahmen + schiebt die Hinweise nach rechts */
.widget-titelzeile { position:relative; … }            /* position:relative ergänzen   */
.widget-titelzeile h3 { margin:0; margin-right:auto; }  /* margin-right:auto ergänzen    */

/* b) ENTFERNEN:  .anim-hinweis.rechts { margin-left:auto; }
      (wird durch h3{margin-right:auto} ersetzt; sonst entsteht eine Lücke) */

/* c) „Worauf achten?" (links) am rechten Rand der Titelzeile verankern */
.anim-hinweis.links { position:static; }

/* d) beide Rollover öffnen nach links */
.anim-hinweis.rechts .ah-pop,
.anim-hinweis.links  .ah-pop { left:auto; right:0; }    /* die .rechts-Regel gab es schon */
```

**Wirkung:** Beide Hinweise sitzen am rechten Titelende; das `.ah-pop` der linken
Variante richtet sich (über `position:static`) an der `.widget-titelzeile` aus und passt
mit `width:min(440px,86vw)` auf jeder Breite.

- [x] `.widget-titelzeile` → `position:relative`
- [x] `.widget-titelzeile h3` → `margin-right:auto`
- [x] `.anim-hinweis.rechts { margin-left:auto }` entfernt
- [x] `.anim-hinweis.links { position:static }` ergänzt
- [x] `.anim-hinweis.links .ah-pop` zur `left:auto; right:0`-Regel hinzugefügt

---

## 4. Optional / prüfen — Muster, kein Pflicht-Port

Diese Punkte wurden in Physik pro Animation umgesetzt; in Mathe nur übernehmen, wo es
inhaltlich passt:

- [ ] **Play-/Pause-Knöpfe entfernen, wo unnötig** — Animationen starten ohnehin per
  IntersectionObserver-Autostart (`makeLoop(canvasId, null, tick)` statt Button-ID).
- [ ] **Auswahl-Knöpfe + Regler in einer `.sl-row`** (Knöpfe zuerst, dann Regler-`.sl-grp`)
  als einheitliches Bedienmuster.
- [ ] **Texte auf Schweizer Hochdeutsch / Punkt als Dezimaltrennzeichen** gegenprüfen
  (gilt in Mathe ohnehin, aber bei kopierten Snippets kontrollieren).

---

## 5. Stilcheck-Regelwerk  (neu, 26.–28.07.2026)

**Was:** Aus der Überarbeitung der Canvas-Animationen sind sechs verbindliche
Darstellungsregeln entstanden, abrufbar über das Stichwort **«Stilcheck»** im Prompt.
Sie stehen in `STYLEGUIDE.md` (§2.1, §2.6b, §2.7, §2.8, §5.3) und als Tabelle in
`CLAUDE.md`.

**Warum als Port:** Die Regeln entstanden als Einzelbefunde («Abstände zu klein»,
«Punkt als Trenner geht gar nicht») und werden ohne Sammelstelle und Auslöser bei der
nächsten Änderung wieder verletzt — oft von der Ergänzung selbst.

**Wie:** Ein geprüftes Skript liegt bereits im Mathe-Repo:
`scripts/port_stilcheck_von_physik.py` (Trockenlauf ist Standard, idempotent).

```bash
cd /home/paps/tals-mathe
python3 scripts/port_stilcheck_von_physik.py all --apply   # Doku + 2 CSS-Zeilen
python3 scripts/port_stilcheck_von_physik.py check         # Befundliste Bestand
```

**Was dabei bewusst NICHT übertragen wird:**

- **Regel 1** (Live-Box-Spaltenabstand) entfällt — kein `.live-box` in Mathe (§2 oben).
  Mathe bekommt darum fünf statt sechs Regeln.
- **Zentralisierung der `.formel-live`-Inline-Stile** wurde getestet und verworfen:
  fünf Mathe-Seiten setzen `.fl-eq` ohne `font-style`, eine zentrale Regel mit
  `italic` würde sie kursivieren (CSS mischt eigenschaftsweise). Der Unterbefehl
  `inline` listet die Varianten je Datei auf — die Entscheidung bleibt redaktionell.
- **CHANGELOG-Ablösung** gilt nur für Physik. Mathes `CHANGELOG.md` wird weiter
  gepflegt (ZIP-Snapshot-Rhythmus, letzter Eintrag 11.07.2026).

**Achtung, sichtbare Änderung:** Die zentrale Regel `.fl-eq + .fl-eq { margin-top:6px }`
betrifft 130 mehrzeilige Anzeigen auf 32 Mathe-Seiten. Render-Check ist Pflicht.

- [ ] `docs` und `css` in Mathe ausgeführt
- [ ] Render-Check 1280 px + 360 px nach der CSS-Änderung
- [ ] `check`-Befundliste abgearbeitet (Stand 28.07.2026: 34 echte Treffer zu Regel 1,
  1 zu Regel «Preis/Kosten»; die 3 Treffer zu «Formel vor Werten» sind Fehlalarme)

---

---

## 6. Header bleibt beim Scrollen stehen  (`style.css`, 1 Zeile + 1 Regel)

**Was:** `#nav-root` wird selbst `sticky`. Dazu bekommt `.mobile-nav` eine Höhenbegrenzung
mit eigenem Scrolling.

```css
#nav-root { position: sticky; top: 0; z-index: 200; }

.mobile-nav {
  /* … bestehende Regeln … */
  max-height: calc(100vh - 54px); overflow-y: auto;
}
```

**Warum:** `.site-hdr` trägt zwar `position: sticky; top: 0`, klebt aber nie — der Header
liegt in `<div id="nav-root">`, und ein klebendes Element klebt nur innerhalb der Box
seines Containers. Der ist 54 px hoch und scrollt weg. In Physik gemessen: bei
Scrollposition 2500 lag die Header-Oberkante bei −2500, auf allen Breiten und Seiten.
Zweiter Effekt: das Burger-Menü liegt im Textfluss direkt unter dem Header und ging beim
Scrollen **ausserhalb des Bildschirms** auf (bei 360 px gemessen: Menü bei −4029, und die
eingefügten 1083 px schoben die Seite zusätzlich weiter). Ohne `max-height` ist das offene
Menü höher als der Schirm und die unteren Einträge sind unerreichbar.

**Mathe-Stand (29.07.2026 geprüft):** identischer Fehler. `style.css:53` setzt
`position: sticky` auf `.site-hdr`, eine Regel für `#nav-root` gibt es nicht;
`.mobile-nav` ist vorhanden. Der Port ist 1:1 möglich, keine Farbfrage.

**Dazu gehört:** Sprungziele nicht unter den Header rutschen lassen —

```css
.content h2[id], .content h3[id] { scroll-margin-top: 66px; }
```

Betrifft die Sprünge aus dem Inhaltsverzeichnis und (nach §7) aus der Suche. Mathe hat
heute kein `scroll-margin` im `style.css`.

- [ ] `#nav-root` sticky gesetzt, Header steht bei 1280 px und 360 px
- [ ] `.mobile-nav` mit `max-height` + `overflow-y`, Burger-Menü beim Scrollen brauchbar
- [ ] `scroll-margin-top` für `h2[id]`/`h3[id]`

---

## 7. Volltextsuche über die ganze Site  (neu: 3 Dateien + Header-Feld)

**Was:** Suchfeld oben rechts im Header, Trefferpanel mit Kapitelnummer, Abschnittstitel
und markiertem Textausschnitt, Sprung auf den `<h2>`-Anker. Rein statisch, kein Server,
keine Fremdbibliothek.

**Dateien aus Physik (in dieser Reihenfolge übernehmen):**

| Datei | Rolle | Anpassung für Mathe |
|---|---|---|
| `scripts/build-suchindex.py` | erzeugt den Index aus den Seiten | Seitenliste, Skip-Listen, Pfade |
| `suche.js` | Suchlogik + Panel | nur Pfad-/Textkosmetik |
| `suchindex.js` | **generiert** — nie von Hand ändern | entsteht beim ersten Lauf |
| `nav.js` | Suchfeld ins Header-Markup | 1:1 (Markup ist farbfrei) |
| `style.css` | Feld + Panel + Mobile-Lupe | `--bernstein*` → `--blau*` |

**Der Generator ist seit 29.07.2026 projektübergreifend — nichts umzubauen.**
`scripts/build-suchindex.py` erkennt das Projekt an der Canvas-Bibliothek im Repo-Root
(`physiklib.js` / `mathlib.js`), liest **alle** Listen aus dem `const SITE = {…}`-Block
(Physik: `themen`; Mathe: `grundlagen` + `schwerpunkt`) und hängt Glossar und
Formelsammlung an, sofern vorhanden. Projektabhängig ist nur ein Feld:

```python
PROJEKTE = [
    {'name': 'TALS Physik', 'kennung': 'physiklib.js',
     'skip_classes': {'widget-body'}},
    {'name': 'TALS Mathe',  'kennung': 'mathlib.js',
     'skip_classes': {'regler', 'legende', 'formel', 'wert', 'val', 'lab', …}},
]
```

Mathe hat kein `.widget-body`; die Bedienung liegt in `.bedien`, wo neben Reglern und
Legenden auch die `.erklaerung` steht — darum sind dort die Kinder einzeln ausgeschlossen
und `.bedien` selbst bleibt drin, sonst ginge der Erklärtext verloren. Die
Abschnittsnamen (`aufgaben`, `downloads`, `ressourcen`), das Glossar-Markup
(`.glossar-eintrag`/`.ge-begriff`/`.ge-quer`) und der `<h3>`-Aufbau der Formelsammlung
sind in beiden Projekten identisch — geprüft, nichts anzupassen.

**Datei einfach übernehmen und laufen lassen:**

```bash
cp /home/paps/tals-physik/scripts/build-suchindex.py scripts/
python3 scripts/build-suchindex.py --dry-run   # baut, schreibt nichts
python3 scripts/build-suchindex.py             # schreibt suchindex.js
```

Der Trockenlauf gegen das Mathe-Repo ist am 29.07.2026 gelaufen: **48 Seiten,
398 Abschnitte, 558 KB** (Physik: 208 / 247 KB). Stichproben bestanden — Mini-Check-Fragen,
Lösungen, Aufgaben-Marker und Legendenwerte fehlen im Index, die `.erklaerung`-Texte sind
drin. Ändert sich das Markup, wird nur `PROJEKTE` angefasst, nicht der Parser.

**Grösse:** Physik hat 507 KB Rohtext → 208 Abschnitte → `suchindex.js` 250 KB
(~45 KB über die Leitung). Mathe hat **1086 KB Rohtext über 48 Seiten**, also grob das
Doppelte. Der Index wird erst beim ersten Tastendruck im Suchfeld nachgeladen, das ist
verkraftbar — wenn er unangenehm gross wird, den Abschnittstext im Generator kappen
(z.B. 1500 Zeichen) statt Seiten wegzulassen.

**Warum `.js` statt `.json`:** `fetch()` auf eine JSON-Datei scheitert unter `file://` an
CORS. Als `window.SUCHINDEX = {…}` funktioniert die Suche auch, wenn jemand die Seiten
lokal öffnet.

**Pflege:** Nach jeder inhaltlichen Änderung `python3 scripts/build-suchindex.py`. In
Physik prüft der Pre-Flight das mit (`--check`, Exit 1 = veraltet) und meldet `[WARN]` —
denselben Aufruf in den Mathe-Pre-Flight aufnehmen. Der Fingerabdruck geht über den
*indexierten Inhalt*, nicht über die Rohdateien; Änderungen an Skripten oder Aufgaben
lösen also keine Fehlalarme aus.

- [ ] `scripts/build-suchindex.py` aus Physik kopiert (kein Umbau nötig)
- [ ] Stichprobe nach dem ersten Lauf: ein Aufgabentext und eine Mini-Check-Frage dürfen
  **nicht** im Index stehen, Einstiegstext und `.erklaerung` schon
- [ ] `suche.js` übernommen, `suchindex.js` gebaut
- [ ] Suchfeld in `nav.js` (Header rechts, Lupe ab 640 px) + CSS mit Mathe-Farben
- [ ] `<script src="…/suche.js">` auf allen Seiten eingebunden (in Physik per Skript
  direkt nach der `nav.js`-Zeile)
- [ ] Pre-Flight um den `--check`-Aufruf ergänzt
- [ ] Render-Check 1280 px + 360 px, Tastatur (`/`, Strg/Cmd+K, Pfeile, Enter, Esc)

---

## 8. Rechtliches, Footer und «Kontakt & Feedback»

**Was:** Autor, Lizenz, Haftung und Datenschutz sind belegt und von jeder Seite aus
erreichbar; Kontakt läuft ausschliesslich über das Feedbackformular, es gibt **keine**
veröffentlichte E-Mail-Adresse.

**Teile:**

1. **`rechtliches.html`** (neu, Root, kein eigener Headerpunkt): Verantwortlich · Haftung ·
   Datenschutz beim Seitenaufruf · Datenschutz beim Feedback · Betroffenenrechte · keine
   Cookies. Verlinkt aus Footer und Formular. **Pflicht, sobald `feedback.html` portiert
   ist** — die Physik-Fassung des Formulars verlinkt relativ auf `rechtliches.html`, in
   Mathe liefe der Link sonst ins Leere.
2. **`feedback.html`**: Die Datei ist in beiden Projekten dieselbe und erkennt das Projekt
   selbst aus der URL. Die Physik-Fassung kann **1:1** übernommen werden; sie enthält den
   Datenschutzhinweis unter dem Senden-Knopf (erscheint erst mit ihm), den kleinen Fuss und
   die entschärften Platzhalter („freiwillig — kann leer bleiben" statt „leer lassen =
   anonym"; „anonym" lässt sich bei Übermittlung über einen externen Dienst nicht
   absolut versprechen).
3. **Header-Beschriftung**: aus „Feedback" wird „Kontakt & Feedback" — in Mathe heisst der
   Punkt heute `FEEDBACK` (eigener `.nav-btn nav-meta`-Eintrag, Desktop und Mobil).
4. **Über-Panel** (`nav.js`): Autor namentlich, Unabhängigkeit von SBFI/Kanton/Schule,
   KI-Einsatz mit redaktioneller Verantwortung, CC BY-NC 4.0 mit empfohlener Namensnennung.
   Die Physik-Texte sind wörtlich übertragbar, nur „TALS Physik" → „TALS Mathematik".
5. **Einheitlicher Footer** auf allen Seiten:

```html
<footer class="site-footer">
  <p><strong>TALS Mathematik</strong> — Lernmaterial für die Berufsmaturität …</p>
  <p>Mathematik · 3.2 Lineare Funktionen</p>          <!-- seitenspezifisch -->
  <p>© 2026 Raphael Arnold Kohler · <a href="…by-nc/4.0/deed.de">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version X · Stand …</p>
</footer>
```

   **Kein GitHub-Link im Footer.** Er steht genau einmal, im Über-Panel unter „Lizenz"
   („→ Quelltext und Inhalte des Lehrmittels (GitHub)"). Begründung: für Lernende ist
   „GitHub" Fachjargon und eine Dateiliste wirkt wie ein Fehler; wer das Repo sucht, liest
   es ohnehin aus der Domain `go4exercises.github.io/…`. Mathes heutiger Footer nennt
   „GitHub Pages" in Zeile 2 — der fällt weg.

**Vor dem Behaupten prüfen:** Die Aussage „keine Cookies" gilt nur, solange nichts im
Browser gespeichert wird. In Physik geprüft: kein `document.cookie`, kein
`localStorage`/`sessionStorage`/`indexedDB` im ganzen Projekt. In Mathe vor der
Veröffentlichung derselbe Grep. Ebenso die Löschfrist im Datenschutztext (12 Monate) —
sie muss zur tatsächlichen Praxis im Apps Script und im Postfach passen.

- [ ] `rechtliches.html` erstellt (Texte aus Physik, Fach und Projektname angepasst)
- [ ] `feedback.html` aus Physik übernommen, Versand einmal echt getestet
- [ ] Headerpunkt „Kontakt & Feedback" (Desktop + Mobil)
- [ ] Über-Panel: Autor, Ausblick, Lizenz nachgeführt, GitHub-Link unter Lizenz
- [ ] Footer auf allen 48 Seiten + `TEMPLATE.html` vereinheitlicht
- [ ] Cookie-Grep und Löschfrist verifiziert

---

## 9. Startseite straffen  (korrigiert 29.07.2026 — jetzt mechanisch)

> **Korrektur.** Die erste Fassung dieses Abschnitts behauptete, Mathe sei anders
> aufgebaut und ein CSS-Port sei nicht möglich. Das war falsch: gesucht wurde in
> `style.css`, die Startseiten-Regeln stehen aber in **beiden** Projekten im
> `<style>`-Block **innerhalb von `index.html`**. Mathes Startseite hat dieselbe
> Struktur wie Physik vor dem Umbau. Darum hier die konkreten Schritte.

**Ziel:** Die Kapitelliste beginnt im ersten Bildschirm. Gemessen bei 1280 px vor dem
Umbau: erste `.kap`-Zeile bei **y = 543 px** (Hero bis 330, `.stats` bei 362,
erster `.bereich` bei 451). Erwartung danach: rund 260–280 px.

**1 · Hero** (`index.html`, `<style>` und Markup)

```css
.hero    { padding: 16px 40px 28px; }        /* vorher 50px 40px 42px */
.hero-ew { letter-spacing: 1px; color: var(--tinte-2); }   /* text-transform: uppercase ENTFERNEN */
.hero-ew strong { font-weight: 700; color: var(--blau); }
```

```html
<!-- Text in EIN span: .hero-ew ist ein Flex-Container mit gap — einzelne <strong>
     würden sonst zu eigenen Flex-Items mit Lücken davor und danach. -->
<div class="hero-ew"><span>Berufsmaturität <strong>T</strong>echnik,
  <strong>A</strong>rchitektur, <strong>L</strong>ife <strong>S</strong>ciences —
  <strong>TALS</strong></span></div>
<h1>Mathematik <span>nach BM RLP 2030</span></h1>   <!-- vorher zwei Zeilen mit <br> -->
```

**2 · Ersatzlos löschen**

- `<div class="chips">…</div>` (drei Chips: „Grundlagenfach · 18 Teilgebiete",
  „Schwerpunktfach · 13 Teilgebiete", „📄 Formelsammlung SBFI"). Die ersten beiden
  wiederholen die Bereichsköpfe, der dritte doppelt den Menüpunkt.
- `<div class="stats">…</div>` (Zählzeile „46 Themenseiten fertig · 31 RLP-Teilgebiete
  + 2 TALS-Ergänzungen · ▼ Lerngebiet anklicken zum Aufklappen").
- die **beiden** `<div class="b-desc">…</div>` (lange FH-Fachbereichs-Sätze in
  `#gl` und `#sp`).

**Nicht löschen:** die beiden `.bereich`-Köpfe selbst (`.bh` mit `.b-badge` und
`.b-titel`). Sie trennen Grundlagen- und Schwerpunktfach — das ist Inhalt, keine Deko.
Weil sie bleiben, entfällt der Physik-Zusatz `.kap:first-of-type { border-top … }`:
die Bereichsköpfe tragen den oberen Rahmen weiter.

**3 · Farbcode-Legende und Kapitelzeilen** (dieselbe Datei)

```css
/* feste Spaltenzahl statt auto-fill — Mathe hat FÜNF Kacheln, Physik sechs */
.ds-grid { grid-template-columns: repeat(5, 1fr); }

@media (max-width: 900px) { .ds-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 600px) {
  .hero { padding: 16px 16px 22px; }          /* vorher 28px 16px 24px */
  .ds-grid { grid-template-columns: repeat(2, 1fr); }
  /* Lektionsangabe darf umbrechen, sonst läuft die Kapitelzeile rechts aus dem Bild */
  .kap-hdr { align-items: flex-start; }
  .k-lek   { white-space: normal; text-align: right; line-height: 1.4; }
  .k-nr, .k-name { padding-top: 1px; }
}
```

**4 · Abstände unter dem Titel** (nachgezogen 30.07.2026)

Nach dem Entfernen der Chips steht der Titel als letztes Element im Hero — seine
`margin-bottom` ist dann toter Raum, und die alten Polsterwerte sind auf einen Hero mit
drei Elementen ausgelegt. Vier Werte, in Physik gemessen und übernommen:

```css
.hero    { padding: 16px 40px 18px; }   /* Unterkante 28 → 18 */
.hero h1 { margin-bottom: 0; }          /* vorher 12px — nur richtig, wenn .chips weg ist */
.page    { padding: 18px 22px 80px; }   /* Oberkante 32 → 18 */

@media (max-width: 600px) {
  .hero { padding: 16px 16px 14px; }    /* Unterkante 22 → 14 */
  .page { padding: 12px 12px 60px; }    /* Oberkante 18 → 12 */
}
```

**Mathe-Stand (30.07.2026 nachgesehen):** `.hero { padding: 16px 40px 28px }`,
`.hero h1 { margin-bottom: 12px }`, `.page { padding: 32px 22px 80px }` und mobil
`16px 16px 22px` / `18px 12px 60px` — also genau die Physik-Werte vor dieser Änderung.
Der Diff passt damit wörtlich, sobald Schritt 2 (`.chips` entfernt) erledigt ist.

**Wirkung in Physik**, gemessen als Abstand von der Titel-Unterkante bis zur ersten
Kapitelzeile:

| Breite | vorher | nachher |
|---|---:|---:|
| 1280 px | 73 px | **37 px** |
| 360 px | 53 px | **27 px** |

**Prüfen:** bei 1280 px die Position der ersten `.kap`-Zeile vorher/nachher vergleichen,
bei 360 px `document.body.scrollWidth === document.documentElement.clientWidth`
(kein Horizontalscroll) und die fett gesetzten T·A·L·S auf Lesbarkeit sichten.

- [ ] Hero gestrafft, Kopfzeile gemischt geschrieben, Titel einzeilig
- [ ] `.chips`, `.stats` und beide `.b-desc` entfernt, Bereichsköpfe behalten
- [ ] `.ds-grid` auf 5 Spalten, gestufte Media-Queries
- [ ] `.k-lek` bricht unter 600 px um
- [ ] Abstände unter dem Titel nach Schritt 4 (vier Werte, Diff passt wörtlich)
- [ ] Render-Check 1280 px + 360 px

---

## 10. Kleinteiliges aus demselben Durchgang

- [ ] **Links im Über-Panel bleiben inline.** `.dd-menu a { display:flex }` macht jeden
  Link im Panel zu einer eigenen Zeile; ein Link mitten im Satz bricht dadurch heraus.
  Gegenregel: `.ueber-panel .meta-link { display:inline; padding:0; }`. Mathe hat
  `.dd-menu a` und `.ueber-panel` — derselbe Fehler ist dort latent vorhanden.
- [ ] **`TOC_KURZ` für Nachschlagewerke füllen.** Auf der Formelsammlung standen im
  Inhaltsverzeichnis abgeschnittene „Lerngebiet 4 · Mec…"; kurze Ersatzlabels lösen das.
  In Mathe die dortigen `<h2 id>` der Formelsammlung ansehen.
- [ ] **Version und Datum einmal zentral prüfen.** In Physik standen 13 Seiten auf „Stand
  Juni", 4 auf „Juli"; jetzt einheitlich und auf 1.0 gehoben (README mitgeführt).

**Bereits erledigt, nichts zu tun:** Die Regel `mjx-container[display="true"]
{ overflow-x:auto }` aus dem Physik-Durchgang vom 28.07.2026 steht in Mathes `style.css`
bereits (Zeile 1099).

### Verifikation pro Port
1. Mathe-Pre-Flight: `ALLE CHECKS BESTANDEN`.
2. `node --check` auf geänderte Inline-Scripts (macht der Pre-Flight i. d. R. mit).
3. Render-Check 1280 px + 360 px — in Mathe mit `.claude/tools/screenshot-widgets.mjs`,
   in Physik mit einem Playwright-Skript (Chromium liegt unter `~/.cache/ms-playwright/`).
4. CSS-Klammerbilanz: `python3 -c "s=open('style.css').read(); print(s.count('{')==s.count('}'))"`.
