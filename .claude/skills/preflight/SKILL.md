---
name: preflight
description: Pflicht-Qualitätscheck für TALS-Physik-Themenseiten. IMMER ausführen, bevor Änderungen an einer Datei in themen/*.html committet werden. Prüft div/details-Tag-Bilanz, MathJax-Delimiter-Parität, doppelte HTML-IDs, verbotenes ß, Dezimalkommas innerhalb von Math-Delimitern, Node-Syntax aller Inline-Scripts, Skelett-Marker, erfundene Phantom-Klassen, physiklib.js-Abhängigkeit bei Lösungs-Toggles sowie Duplicate-Marker und Slot-Limits in der Ressourcen-Sektion.
---

# Pre-Flight für TALS-Physik-Themenseiten

Vor jedem Commit, der eine oder mehrere Dateien in `themen/*.html` betrifft, läuft dieser
Check. Er ersetzt die früheren grep-Blöcke aus der COLLABORATION.md durch ein einziges
deterministisches Skript.

## Ausführen

```bash
python3 .claude/skills/preflight/preflight.py themen/p4-1-kinematik.html
# mehrere Dateien / alle:
python3 .claude/skills/preflight/preflight.py themen/*.html
```

Voraussetzung: `node` muss auf dem PATH sein (für den Syntax-Check der Inline-Scripts).
Fehlt `node`, meldet das Skript das pro Datei als Warnung und überspringt nur diesen
Teilcheck — alle anderen laufen normal.

## Erwartetes Ergebnis

Letzte Zeile lautet `ALLE CHECKS BESTANDEN`. Exit-Code 0.
Jede `[FEHLER]`- oder `[WARN]`-Zeile zeigt einen Schaden, der dem Nutzer sonst erst im
Browser auffiele. **Vor dem Commit beheben, dann erneut laufen lassen.** Exit-Code ≠ 0
heisst: nicht committen.

## Was geprüft wird (Kurzreferenz)

1. `<div>`/`</div>` und `<details>`/`</details>` paarweise ausgeglichen.
2. MathJax: gleich viele `\(` wie `\)` und gleich viele `\[` wie `\]`.
3. Keine doppelt vergebene `id="…"` innerhalb derselben Datei.
4. Kein `ß` irgendwo in der Datei.
5. Keine Dezimalkommas (`Ziffer,Ziffer`) **innerhalb** von `\(…\)`/`\[…\]` —
   ausserhalb (URLs, SVG-Pfade, JS-Arrays) wird bewusst nicht geprüft.
6. `node --check` auf jedem `<script>…</script>`-Block ohne `src`.
7. Skelett-Marker: genau 1× `page-wrap`, 1× `main class="content"`, `nav.js` ohne
   `defer`; keine Phantom-Klassen (`inhalt`, `ressourcen-grid`, `dl-box`, …).
8. Lösungs-Toggle (`loesung-toggle`) vorhanden ⇒ `physiklib.js` eingebunden.
9. Ressourcen-Sektion: kritische Marker (🎬/🧪/📝, `toc-wrap`, Footer) genau 1×;
   `<a class="lk">`-Tag-Bilanz; je Sektion höchstens 4 `<a href=…>`.

Details und Hintergrund zu jedem Check stehen als Kommentar im Skript.
