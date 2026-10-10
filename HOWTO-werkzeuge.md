# HOWTO — Werkzeuge

**Gilt seit 10.10.2026.** Wann ein Inhalt eine eigene Werkzeugseite bekommt — ein Trainer, ein
Rechner, eine Prüfhilfe —, wo sie liegt, wie sie gebaut, eingetragen und verlinkt wird. Das
Gegenstück für Simulationen ist `HOWTO-simulationen.md`; beide Anleitungen sind gleich
gegliedert und in Mathe gleich gebaut. Bei Widerspruch gilt `STYLEGUIDE.md` §6.6.

---

## 1 · Wozu und Abgrenzung

| Form | Wo | Was man tut | Beispiel |
|---|---|---|---|
| **Animation** | in der Themenseite, `.widget` | Regler bewegen, einen Zusammenhang sehen — ein Bildschirm | Schwingendes Pendel in 4.3 |
| **Simulation** | eigene Seite in `simulationen/` | einen Vorgang beobachten und Grössen verändern | Bungee-Sprung |
| **Werkzeug** | eigene Seite in `werkzeuge/` | eigene Aufgaben oder Messwerte eingeben, üben | Einheitentrainer; Standardabweichung mit eigenen Messwerten berechnen |

**Eine eigene Seite** bekommt ein Inhalt nur, wenn er mindestens eines erfüllt:

- er braucht mehr als einen Bildschirm,
- er hat eine eigene Abfolge (Modi, Runden, Lernstand),
- er wird auch ohne die Themenseite benutzt (zum Üben vor der Prüfung, im Unterricht).

**Gibt man eigene Daten ein**, ist es ein Werkzeug — auch wenn das Ergebnis als Diagramm
erscheint. Die Standardabweichung *zeigen* (Punkte verschieben, Streuung sehen) ist eine
Animation; die Standardabweichung *eigener Messwerte* Schritt für Schritt ausrechnen ist ein
Werkzeug.

## 2 · Ablage und Name

- Ordner `werkzeuge/` im Repo-Root, eine Ebene tief wie `themen/` und `leitprogramme/`.
- Dateiname kebab-case, sprechend, **ohne Nummer**: `einheitentrainer.html`,
  `standardabweichung.html`. Ein Werkzeug hat keine Kapitelnummer und steht nicht im
  Themen-Menü.

## 3 · Seitenaufbau

**Vorlage:** `werkzeuge/einheitentrainer.html` — Skelett einer Themenseite (`#nav-root`,
`.page-wrap`, `main.content`, `aside.toc-wrap`, `footer.site-footer`) mit Kopf, Werkzeug,
Erklärungsverweisen, Tabellen, häufigen Fehlern und Zusammenfassung; ohne Aufgaben und
Ressourcen.

Einbindungen, alle relativ eine Ebene hoch — **kein fremder Host**:

```html
<link rel="stylesheet" href="../schriften.css">
<link rel="stylesheet" href="../style.css">
<script src="../vendor/mathjax/tex-svg.js"></script>   <!-- nur mit Formeln -->
…
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script src="../physiklib.js"></script>
<script src="../anim-hinweise.js"></script>              <!-- mit .anim-hinweis -->
<script src="../minicheck.js"></script>                  <!-- mit .minicheck -->
<script>buildNav({ id:'werkzeuge' });</script>
```

- `buildNav` ohne `homepage`, `kapitelNr`, `prev`, `next` — das Menü markiert «Werkzeuge»
  unter «Nachschlagen».
- **Kopf:** `pt-bereich` «WZ · Werkzeuge», `h1` mit dem Titel, `pt-untertitel` mit einem Satz,
  was man tut. **Rücklink als letzter Satz von `pt-untertitel`**, per Anker auf den Abschnitt:
  «Erklärt wird das Umrechnen auf der Themenseite
  `<a href="../themen/p0-2-vorwissen-physik.html#umrechnen">0.2 Einheiten umrechnen</a>`.»
- **Daten in EINER Struktur.** Einheiten, Faktoren, Grenzen, Rückmeldetexte stehen an genau
  einer Stelle im Skript; Aufgaben, Diagnosen und Tabellen entstehen daraus. Vorbild:
  `ET_GRUPPEN` im Einheitentrainer. Nie einen Faktor an zweiter Stelle notieren.
- **Gespeicherter Zustand nur ausnahmsweise.** Wer `localStorage` braucht (Lernstand):
  eigener, versionierter Key nach dem Muster `tals-physik-<name>-<was>-v1`, ein sichtbarer
  Rücksetzknopf und ein Satz in `rechtliches.html` (Abschnitt Datenschutz, «Eine Ausnahme im
  Browser»). Keine Cookies, nichts verlässt das Gerät.
- **Selbsttest.** Ein Werkzeug, das rechnet oder bewertet, bringt eine Funktion mit, die sich
  selbst prüft (Referenzwerte, Hin- und Rückweg, Grenzfälle, Eingabeformate), und ein
  Skript `scripts/verify_<name>.js`, das die Seite in jsdom lädt und sie aufruft — Muster
  `scripts/verify_einheitentrainer.js`. Das Skript in den Pre-Flight (`run_deep`) aufnehmen.
- Eingaben akzeptieren Dezimalpunkt **und** Dezimalkomma; ausgegeben wird mit Punkt
  (STYLEGUIDE §2).

## 4 · Eintragen

An drei Stellen, sonst fehlt die Seite in Übersicht, Suche oder Sitemap:

1. **Übersicht `werkzeuge.html`**, zwischen `<!-- WERKZEUGE:ANFANG -->` und
   `<!-- WERKZEUGE:ENDE -->`, unter dem Lerngebiet (`<h2 id="lg0">` usw., bei Bedarf neu
   anlegen) oder unter `<h2 id="ausserhalb">`. Eine Kachel:

   ```html
   <div class="karte-lp">
     <a href="werkzeuge/einheitentrainer.html" class="karte" aria-label="Werkzeug Einheitentrainer"></a>
     <div class="lp-kopf">Einheitentrainer</div>
     <div class="lp-satz">Ein Satz, was man dort tut.</div>
     <div class="lp-zeile"><span class="k-tit">Einheiten umrechnen</span><a href="themen/p0-2-vorwissen-physik.html#umrechnen" class="ts-link" title="Themenseite 0.2 Grössen, Einheiten und Messen">0.2</a></div>
   </div>
   ```

   Je Themenseite, die auf das Werkzeug verweist, eine Zeile mit Pille.
2. **`scripts/build-seo.py`**, Tabelle `SEITEN`: Schlüssel `'werkzeuge/<name>.html'`,
   `typ='article', lrt='Werkzeug'`, Beschreibung 140–165 Zeichen, `themen=[…]`. Dann
   `python3 scripts/build-seo.py` — zweimal, der zweite Lauf nach dem Commit (Git-Datum,
   Kopfkommentar des Skripts).
3. **Suchindex:** nichts einzutragen — `build-suchindex.py` liest `werkzeuge/` von selbst
   (Titel aus `<title>`). Nur `python3 scripts/build-suchindex.py` laufen lassen.

## 5 · Verlinken in der Themenseite

- **Im Abschnitt**, in den der Inhalt gehört — am Ende des Abschnitts, vor den
  Verständnisfragen (❓) und dem Mini-Check. **Nicht** am Seitenanfang (dort steht der
  Leitprogramm-Kasten) und **nicht** auf den Kacheln von `index.html`.
- Baustein, wörtlich:

  ```html
  <div class="block block-tipp">
    <div class="block-titel">🛠 Werkzeug: Einheitentrainer</div>
    <p>Ein Satz, was man dort tut. <a href="../werkzeuge/einheitentrainer.html">Zum Werkzeug →</a></p>
  </div>
  ```

  Vorbild: `themen/p0-2-vorwissen-physik.html`, Abschnitt `#umrechnen`.
- Ein Verweis im Fliesstext (`übt der <a href="../werkzeuge/…">Einheitentrainer</a>`) ist
  zusätzlich erlaubt; der Baustein steht trotzdem dort, wo das Werkzeug inhaltlich hingehört.
- Ein Leitprogramm darf im passenden Schritt auf das Werkzeug verweisen.

## 6 · Prüfen

- Pre-Flight mit der neuen Seite und den geänderten Themenseiten:
  `python3 .claude/skills/preflight/preflight.py werkzeuge/<name>.html themen/<seite>.html`.
  `check_sim_wz` meldet als **[FEHLER]**: Kachel fehlt in der Übersicht, Rücklink-Anker zeigt
  ins Leere, Themenseite verlinkt eine Datei, die es nicht gibt; als `[WARN]`: keine
  Themenseite verlinkt darauf. `verify_js_runtime.js` und der Selbsttest prüfen die Seite mit.
- `node .claude/tools/render-check.mjs werkzeuge/<name>.html` — 1280 und 360 px; Eingabefelder
  und Rückmeldungen auf dem Handy ansehen.
- Jede Referenzlösung, jeder Faktor mit `python3` nachgerechnet.

## 7 · Verschieben und Umbenennen

Eine veröffentlichte Adresse steht in Lesezeichen, Unterlagen und Suchmaschinen. Wer eine
Seite verschiebt oder umbenennt:

1. `git mv`, Pfade in der Seite anpassen (`../` je nach Tiefe), Einträge in `build-seo.py`,
   Übersicht, Selbsttest-Skript und allen Verweisen umstellen (`grep -rn alter-name`), auch in
   den Leitprogramm-Generatoren unter `scripts/lp/` — sonst kommt der alte Link beim nächsten
   Bau zurück.
2. **Alte Adresse in `404.html` eintragen**, Tabelle `WEITERLEITUNGEN`
   (`'/alter/pfad.html': '/neuer/pfad.html'`). GitHub Pages liefert `404.html` für jede
   fehlende Adresse aus, das Skript leitet weiter und behält den Anker. **Keine Hilfsseite an
   der alten Stelle** — sie läge in jedem `themen/*.html`-Glob der Prüfskripte.
3. **Den `localStorage`-Key nicht umbenennen** — sonst ist der Lernstand der Lernenden weg.
   Der Einheitentrainer heisst darum weiter `tals-physik-p0-4-lernstand-v1`.

Vorbild: der Umzug vom 10.10.2026 (`themen/p0-4-einheitentrainer.html` →
`werkzeuge/einheitentrainer.html`; die Nummer 0.4 bleibt frei).

## 8 · Checkliste

- [ ] Eigene Seite gerechtfertigt (§1)? Eigene Daten → Werkzeug, sonst vielleicht Simulation
      oder Animation.
- [ ] `werkzeuge/<name>.html`, kebab-case, ohne Nummer.
- [ ] Skelett, Einbindungen `../`, `buildNav({ id:'werkzeuge' })`.
- [ ] Kopf «WZ · Werkzeuge», Rücklink mit Anker am Ende von `pt-untertitel`.
- [ ] Daten in einer Struktur; Werte in Python nachgerechnet.
- [ ] `localStorage` nur mit eigenem Key, Rücksetzknopf und Satz in `rechtliches.html`.
- [ ] Selbsttest-Funktion und `scripts/verify_<name>.js`, im Pre-Flight.
- [ ] Kachel in `werkzeuge.html`, Pille je verweisende Themenseite.
- [ ] `build-seo.py` eingetragen und gelaufen (zweimal), `build-suchindex.py` gelaufen.
- [ ] Baustein «🛠 Werkzeug: …» im Abschnitt der Themenseite.
- [ ] Pre-Flight `ALLE CHECKS BESTANDEN`, ohne `[WARN]` aus `check_sim_wz`.
- [ ] Render-Check 1280/360 px, Bilder angesehen.
