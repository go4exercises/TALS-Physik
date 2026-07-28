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

### Verifikation pro Port
1. Mathe-Pre-Flight: `ALLE CHECKS BESTANDEN`.
2. `node --check` auf geänderte Inline-Scripts (macht der Pre-Flight i. d. R. mit).
3. Render-Check 1280 px + 360 px — in Mathe mit `.claude/tools/screenshot-widgets.mjs`,
   in Physik mit einem Playwright-Skript (Chromium liegt unter `~/.cache/ms-playwright/`).
4. CSS-Klammerbilanz: `python3 -c "s=open('style.css').read(); print(s.count('{')==s.count('}'))"`.
