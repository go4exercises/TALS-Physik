---
name: preflight
description: Pflicht-Qualitätscheck für TALS-Physik-Themenseiten. IMMER ausführen, bevor Änderungen an einer Datei in themen/*.html committet werden. Zweistufig: schnelle Eigen-Checks (Tag-Bilanz, ß, Dezimalkomma in Math, doppelte IDs, Skelett, Phantom-Klassen, physiklib-Einbindung, Ressourcen-Marker inkl. Slot-Limits) plus Aufruf der autoritativen Repo-Skripte verify_mathjax.js (echte Render-Prüfung) und verify_js_runtime.js (JS-Laufzeit in jsdom). Fehlen die npm-Module mathjax-full/jsdom, werden die Tiefen-Checks sauber übersprungen.
---

# Pre-Flight für TALS-Physik-Themenseiten

Vor jedem Commit, der `themen/*.html` betrifft.
**Vom Repo-Wurzelverzeichnis aufrufen** (wegen `scripts/` und `node_modules/`).

## Ausführen

```bash
python3 .claude/skills/preflight/preflight.py themen/*.html
```

## Erwartetes Ergebnis

Letzte Zeile `ALLE CHECKS BESTANDEN`, Exit 0. Jede `[FEHLER]`-Zeile vor dem Commit
beheben. `[WARN]` ist kein Blocker (typisch: npm-Modul fehlt -> Tiefen-Check übersprungen).

## Stufe 1 — schnelle Eigen-Checks (ohne Abhängigkeiten)

div/details-Bilanz · doppelte HTML-`id` · kein `ß` · Dezimalkomma in Body-Math
(Index-Listen `x_{1,2}` ausgenommen, Scripts ausgeklammert) · Skelett (`page-wrap`,
`main class="content"`, `nav.js` ohne `defer`) · Phantom-Klassen (`rlp` ist legitim) ·
`physiklib.js` eingebunden bei Lösungs-Toggles · Ressourcen-Strukturmarker (🎬/🧪/📝)
und Slot-Limit (≤4 Links je Sektion).

## Stufe 2 — autoritative Repo-Skripte (in scripts/)

- **verify_mathjax.js** — rendert jeden Ausdruck mit `mathjax-full`, findet echte
  TeX-Fehler. Braucht `node_modules/mathjax-full`.
- **verify_js_runtime.js** — führt den Seiten-JS in jsdom aus, findet Laufzeitfehler.
  Braucht `node_modules/jsdom`.
- **check_identifier_collisions.py** — falls im Repo vorhanden; ohne npm.

Fehlt ein npm-Modul, meldet der Pre-Flight das als `[WARN]` und überspringt nur diesen
Teil. Einmalig installieren mit: `npm install mathjax-full jsdom` (im Repo-Root).
