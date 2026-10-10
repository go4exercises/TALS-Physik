# HOWTO — Simulationen

**Gilt seit 10.10.2026.** Wann ein Inhalt eine eigene Simulationsseite bekommt, wo sie liegt,
wie sie gebaut, eingetragen und verlinkt wird. Das Gegenstück für Trainer und Rechner ist
`HOWTO-werkzeuge.md`; beide Anleitungen sind gleich gegliedert und in Mathe gleich gebaut.
Bei Widerspruch gilt `STYLEGUIDE.md` §6.6.

---

## 1 · Wozu und Abgrenzung

| Form | Wo | Was man tut | Beispiel |
|---|---|---|---|
| **Animation** | in der Themenseite, `.widget` | Regler bewegen, einen Zusammenhang sehen — ein Bildschirm | Schwingendes Pendel in 4.3 |
| **Simulation** | eigene Seite in `simulationen/` | einen Vorgang beobachten und Grössen verändern, oft in mehreren Schritten | Bungee-Sprung: Seillänge, Masse und Federkonstante wählen, Fall, Dehnung und Energien verfolgen |
| **Werkzeug** | eigene Seite in `werkzeuge/` | eigene Aufgaben oder Messwerte eingeben, üben | Einheitentrainer |

**Eine eigene Seite** bekommt ein Inhalt nur, wenn er mindestens eines erfüllt:

- er braucht mehr als einen Bildschirm,
- er hat eine eigene Abfolge (Phasen, Schritte, Szenen),
- er wird auch ohne die Themenseite benutzt (im Unterricht projiziert, als Link verschickt).

Sonst bleibt er eine Animation in der Themenseite. **Gibt man eigene Daten ein**, ist es ein
Werkzeug, auch wenn sich dabei etwas bewegt.

## 2 · Ablage und Name

- Ordner `simulationen/` im Repo-Root, eine Ebene tief wie `themen/` und `leitprogramme/`.
- Dateiname kebab-case, sprechend, **ohne Nummer**: `bungee-sprung.html`. Eine Simulation hat
  keine Kapitelnummer und steht nicht im Themen-Menü.
- Ein Ereignis darf das Datum tragen (`sonnenfinsternis-12-08-2026.html`).

## 3 · Seitenaufbau

**Vorlage:** Das Skelett einer Themenseite (`themen/p4-1-kinematik.html`: `#nav-root`,
`.page-wrap`, `main.content`, `aside.toc-wrap`, leere FUSS-Marken — den Footer schreibt `build-seo.py`) — ohne Kompetenzblock,
Aufgaben, Zusammenfassung und Ressourcen. Die bestehende Seite
`simulationen/sonnenfinsternis-12-08-2026.html` hat einen eigenen Aufbau (Ereignisseite) und ist
**keine** Vorlage für neue Simulationen.

Einbindungen, alle relativ eine Ebene hoch — **kein fremder Host**:

```html
<link rel="stylesheet" href="../schriften.css">
<link rel="stylesheet" href="../style.css">
<script src="../vendor/mathjax/tex-svg.js"></script>   <!-- nur mit Formeln -->
…
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script src="../physiklib.js"></script>
<script src="../anim-hinweise.js"></script>
<script>buildNav({ id:'simulationen' });</script>
```

- `buildNav` ohne `homepage`, `kapitelNr`, `prev`, `next` — das Menü markiert «Simulationen»
  unter «Nachschlagen».
- **Kopf:** `pt-bereich` «SIM · Simulationen», `h1` mit dem Titel, `pt-untertitel` mit einem
  Satz, was man tut. **Rücklink als letzter Satz von `pt-untertitel`**, per Anker auf den
  Abschnitt: «Erklärt wird das auf der Themenseite
  `<a href="../themen/p4-3-energie.html#erhaltung">4.3 Energieerhaltung</a>`.» Seiten ausserhalb
  der Lerngebiete haben keinen Rücklink.
- **`anim-hinweise.js` ist Pflicht** (👁/💡-Hinweise wie bei jeder interaktiven Animation).
- Canvas-Code mit `physiklib.js` (`initCanvas`, `drawGrid`, `drawAxesUnits`, `drawArrow` …),
  Achsen immer mit Einheiten (STYLEGUIDE §3).
- **Geometrie und Werte vorab in Python durchrechnen** — Stützpunkte, Schnittpunkte,
  Endwerte, Label-Positionen —, bevor Zeichencode entsteht. Beim Bungee-Sprung etwa tiefster
  Punkt und maximale Geschwindigkeit aus der Energiebilanz, nicht aus der Animation abgelesen.
- Clips sind möglich, nicht Pflicht; wenn, dann nach `HOWTO-clips.md`.

## 4 · Eintragen

An drei Stellen, sonst fehlt die Seite in Übersicht, Suche oder Sitemap:

1. **Übersicht `simulationen.html`**, zwischen `<!-- SIMULATIONEN:ANFANG -->` und
   `<!-- SIMULATIONEN:ENDE -->`, unter dem Lerngebiet (`<h2 id="lg4">` usw., bei Bedarf neu
   anlegen) oder unter `<h2 id="ausserhalb">`. Eine Kachel:

   ```html
   <div class="karte-lp">
     <a href="simulationen/bungee-sprung.html" class="karte" aria-label="Simulation Bungee-Sprung"></a>
     <div class="lp-kopf">Bungee-Sprung</div>
     <div class="lp-satz">Ein Satz, was man dort tut.</div>
     <div class="lp-zeile"><span class="k-tit">Energieerhaltung</span><a href="themen/p4-3-energie.html#erhaltung" class="ts-link" title="Themenseite 4.3 Energie">4.3</a></div>
   </div>
   ```

   Je Themenseite, die auf die Simulation verweist, eine Zeile mit Pille.
2. **`scripts/build-seo.py`**, Tabelle `SEITEN`: Schlüssel `'simulationen/bungee-sprung.html'`,
   `typ='article', lrt='Simulation'`, Beschreibung 140–165 Zeichen, `themen=[…]`,
   `ort='Simulationen · ⟪Name⟫'` (Footer-Ortszeile). Dann
   `python3 scripts/build-seo.py` — zweimal, der zweite Lauf nach dem Commit (Git-Datum,
   Kopfkommentar des Skripts).
3. **Suchindex:** nichts einzutragen — `build-suchindex.py` liest `simulationen/` von selbst
   (Titel aus `<title>`). Nur `python3 scripts/build-suchindex.py` laufen lassen.

## 5 · Verlinken in der Themenseite

- **Im Abschnitt**, in den der Inhalt gehört — am Ende des Abschnitts, vor den
  Verständnisfragen (❓) und dem Mini-Check. **Nicht** am Seitenanfang (dort steht der
  Leitprogramm-Kasten) und **nicht** auf den Kacheln von `index.html`.
- Baustein, wörtlich:

  ```html
  <div class="block block-tipp">
    <div class="block-titel">🧪 Simulation: Bungee-Sprung</div>
    <p>Ein Satz, was man dort tut. <a href="../simulationen/bungee-sprung.html">Zur Simulation →</a></p>
  </div>
  ```

- Gehört die Simulation zu mehreren Abschnitten, steht der Baustein in jedem — und in der
  Übersicht je eine Pille.
- Ein Leitprogramm darf im passenden Schritt auf die Simulation verweisen, statt sie
  nachzubauen.

## 6 · Prüfen

- Pre-Flight mit der neuen Seite und den geänderten Themenseiten:
  `python3 .claude/skills/preflight/preflight.py simulationen/bungee-sprung.html themen/p4-3-energie.html`.
  `check_sim_wz` meldet als **[FEHLER]**: Kachel fehlt in der Übersicht, Rücklink-Anker zeigt
  ins Leere, Themenseite verlinkt eine Datei, die es nicht gibt; als `[WARN]`: keine
  Themenseite verlinkt darauf. `verify_js_runtime.js` prüft die Seite mit.
- `node .claude/tools/render-check.mjs simulationen/bungee-sprung.html` — 1280 und 360 px,
  Screenshots der Canvases ansehen.
- Alle Zahlen der Seite (Startwerte, Ergebnisse, Beschriftungen) mit `python3` nachgerechnet.

## 7 · Verschieben und Umbenennen

Eine veröffentlichte Adresse steht in Lesezeichen, Unterlagen und Suchmaschinen. Wer eine
Seite verschiebt oder umbenennt:

1. `git mv`, Pfade in der Seite anpassen (`../` je nach Tiefe), Einträge in `build-seo.py`,
   Übersicht und allen Verweisen umstellen (`grep -rn alter-name`), auch in den
   Leitprogramm-Generatoren unter `scripts/lp/` — sonst kommt der alte Link beim nächsten Bau
   zurück.
2. **Alte Adresse in `404.html` eintragen**, Tabelle `WEITERLEITUNGEN`
   (`'/alter/pfad.html': '/neuer/pfad.html'`). GitHub Pages liefert `404.html` für jede
   fehlende Adresse aus, das Skript leitet weiter und behält den Anker. **Keine Hilfsseite an
   der alten Stelle** — sie läge in jedem `themen/*.html`-Glob der Prüfskripte.
3. Gespeicherter Zustand (`localStorage`-Key) behält seinen Namen, auch wenn er nicht mehr
   passt.

Vorbild: der Umzug vom 10.10.2026 (`sonnenfinsternis-12-08-2026.html` →
`simulationen/`, `themen/p0-4-einheitentrainer.html` → `werkzeuge/einheitentrainer.html`).

## 8 · Checkliste

- [ ] Eigene Seite gerechtfertigt (§1)? Sonst Animation in der Themenseite.
- [ ] `simulationen/<name>.html`, kebab-case, ohne Nummer.
- [ ] Skelett, Einbindungen `../`, `buildNav({ id:'simulationen' })`, `anim-hinweise.js`.
- [ ] Kopf «SIM · Simulationen», Rücklink mit Anker am Ende von `pt-untertitel`.
- [ ] Werte und Geometrie in Python nachgerechnet.
- [ ] Kachel in `simulationen.html`, Pille je verweisende Themenseite.
- [ ] `build-seo.py` eingetragen und gelaufen (zweimal), `build-suchindex.py` gelaufen.
- [ ] Baustein «🧪 Simulation: …» im Abschnitt der Themenseite.
- [ ] Pre-Flight `ALLE CHECKS BESTANDEN`, ohne `[WARN]` aus `check_sim_wz`.
- [ ] Render-Check 1280/360 px, Bilder angesehen.
