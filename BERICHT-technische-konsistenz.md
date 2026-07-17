# Bericht — Technische Konsistenz TALS-Physik

Stand: 2026-06-24. Geprüft: 10 Themenseiten, `physiklib.js`, `style.css`, gemeinsame
Skripte, Pre-Flight (inkl. Tiefen-Checks), Asset-Einbindung, Animations-Architektur,
Git-/Setup-Hygiene. Methode: Pre-Flight + systematische `grep`/`diff`-Stichproben.

## Gesamtbild

Inhaltlich und im Markup ist das Projekt **sehr konsistent** — der Pre-Flight läuft auf
allen 10 Seiten fehlerfrei durch (inkl. der autoritativen Tiefen-Checks
`verify_mathjax.js` und `verify_js_runtime.js`). Die offenen Punkte betreffen die
**JS-Architektur der Animationen** (zwei parallele Muster, dupliziertes Helfer-Coding)
sowie etwas **Git-/Setup-Hygiene**. Keiner der Befunde ist ein akuter Fehler; es sind
Wartbarkeits- und UX-Konsistenz-Themen.

---

## ✅ Konsistent (kein Handlungsbedarf)

- **Pre-Flight:** 2400 Math-Ausdrücke, 0 Fehler; alle Seiten `libs=ok nav=ok toc=ok`.
- **Asset-Einbindung:** alle 10 Seiten laden dieselben 6 Ressourcen in derselben
  Reihenfolge (`style.css`, MathJax 3 `tex-svg` via jsdelivr, `nav.js`, `physiklib.js`,
  `anim-hinweise.js`, `minicheck.js`).
- **MathJax:** überall dieselbe Version/Variante; Delimiter-Parität ok (Pre-Flight).
- **Resize:** genau 1 `resize`-Handler pro Seite.
- **Sauberkeit:** keine `console.log`/`TODO`/`FIXME`-Reste im Auslieferungs-Code.
- **Canvas-Schrift:** nach der jüngsten Anpassung durchgängig ≥ 13 px (kein `<13px` mehr).
- **Zentrale CSS-Änderungen** (Live-Box-Abstand, Anim-Hinweis-Rollover) greifen
  einheitlich über alle Seiten; die einzige lokale `.live-box`-Regel (p4-5,
  `.einstieg-layout .live-box`) ist ein zulässiges seitenspezifisches Layout und
  verträgt sich mit dem neuen `gap:14px 70px` (vertikal → nur 14 px wirksam).

---

## 🔧 Befunde & TODO (nach Priorität)

### 1. [Mittel] Zwei Animations-Loop-Architekturen
- **p4-1 … p4-5:** eigene `requestAnimationFrame`-Loops, **kein** `IntersectionObserver`,
  Start meist erst per Klick auf „▶ Start", **kein** automatischer Stopp ausserhalb des
  sichtbaren Bereichs. Schon innerhalb p4-x uneinheitlich (p4-3 ohne „▶ Start"-Label).
- **p5-1 … p6-2:** gemeinsamer `makeLoop` + `IntersectionObserver` → Autostart beim
  Scrollen ins Bild und Stopp beim Verlassen.
- **Folge:** uneinheitliche UX (Autostart vs. Klick) und Performance (p4-x-Animationen
  können nach dem Start auch ausser Sicht weiterlaufen).
- [ ] **TODO:** Loop-Verhalten vereinheitlichen — p4-x auf `makeLoop`/IntersectionObserver
  umstellen (bevorzugt) oder bewusst dokumentieren, warum p4-x abweicht.

### 2. [Mittel] `makeLoop` / `lerpCol` inline dupliziert statt in `physiklib.js`
- `makeLoop` ist in **5** Seiten separat inline definiert, `lerpCol` in **4**.
  In `physiklib.js` stehen sie **nicht**.
- Die `makeLoop`-Kopien sind funktional gleich, aber **textuell auseinandergelaufen**
  (zwei Formatierungsvarianten: p5-1/p5-2 ausführlich 22–23 Zeilen, p5-3/p6-1/p6-2
  kompakt 13 Zeilen). Ein echter Logik-Fix müsste heute 5× von Hand erfolgen und liesse
  sich wegen der Textunterschiede nicht sauber skripten.
- [ ] **TODO:** `makeLoop`, `lerpCol` (und den zugehörigen `LOOPS`/IntersectionObserver-
  Autostart) **einmal** nach `physiklib.js` ziehen, inline-Kopien entfernen. Danach
  Pre-Flight + JS-Laufzeit-Check über alle Seiten.

### 3. [Niedrig/UX] Play-/Pause-Knopf uneinheitlich
- Nach den jüngsten Einzelanpassungen haben einige Animationen keinen Knopf mehr
  (Autostart, z. B. p5-1 „a2", p5-2 „ein"/„a4"), andere weiterhin schon (z. B. p5-2 „a6",
  alle p6-x). Über die Seiten gemischt.
- [ ] **TODO:** eine einheitliche Linie festlegen — entweder alle Animationen ohne
  Play-/Pause-Knopf (reiner Autostart) **oder** alle mit Knopf — und konsequent umsetzen.

### 4. [Niedrig] Git-/Setup-Hygiene
- `package.json` und `package-lock.json` sind **untracked**: die Tiefen-Check-
  Abhängigkeiten (`mathjax-full`, `jsdom`) sind damit nicht versioniert → `npm install`
  ist für Mitarbeitende/CI nicht reproduzierbar.
- Mehrere Meta-Dateien sind **modifiziert, aber nicht committet**
  (`.claude/settings.json`, `.claude/skills/preflight/SKILL.md`, `preflight.py`,
  `CLAUDE.md`, `SETUP.md`, `.gitignore`).
- [ ] **TODO:** `package.json` + `package-lock.json` committen (und prüfen, dass
  `node_modules` in `.gitignore` steht). Meta-/Tooling-Änderungen in einem eigenen
  Commit festhalten.

### 5. [Niedrig/Info] `:has()` in `style.css`
- Die neue Live-Box-Regel `.live-box:has(> .lb-item:nth-child(4))` nutzt `:has()`
  (Browser-Baseline seit Ende 2023). Für GitHub Pages unkritisch; sehr alte Browser
  ignorieren die Regel und zeigen den weiten Spaltenabstand auch bei dichten Boxen —
  rein kosmetisch.
- [ ] **TODO (optional):** im STYLEGUIDE notieren, dass `:has()` bewusst eingesetzt wird.

### 6. [Info] Visueller Render-Check ausstehend
- Playwright liess sich lokal nicht installieren (kein `pip`/`npm`-CLI für den
  Browser-Download in dieser Umgebung). Die rechnerische Geometrie- und
  Laufzeitprüfung ist erfolgt, aber die **visuelle** Kontrolle der jüngsten Canvas- und
  Rollover-Änderungen bei **1280 px und 360 px** steht noch aus.
- [ ] **TODO:** Sobald ein Browser verfügbar ist, Screenshots der geänderten
  Animationen (p5-1 a2, p5-2 a4/a5/a6 + Treibhausgas-Grafik) und der Anim-Hinweis-
  Rollover bei beiden Breiten sichten.

---

## Nicht-Befunde (geprüft, in Ordnung)
- Keine doppelten HTML-IDs, keine Phantom-Klassen, kein `ß`, keine Dezimalkommas in
  Body-Math (Pre-Flight bestätigt für alle Seiten).
- `nav.js`/TOC-Verknüpfungen auf allen Seiten konsistent (`nav=ok toc=ok`).
- Tiefen-Check-Module (`mathjax-full`, `jsdom`) lokal installiert und vom Pre-Flight
  genutzt.
