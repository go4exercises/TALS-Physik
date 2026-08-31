# SETUP — TALS Physik lokal mit Claude Code

Einmalige Einrichtung und der laufende Arbeits-Workflow. Stand: Juni 2026.

## 1. Einmalig: Claude Code installieren

Empfohlen ist der native Installer (braucht kein Node.js, aktualisiert sich selbst):

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash
# Windows: in PowerShell den entsprechenden Befehl von code.claude.com/docs/setup
```

Alternativ via npm (braucht Node.js 18+, **nie mit sudo**):

```bash
npm install -g @anthropic-ai/claude-code
```

Prüfen und anmelden:

```bash
claude --version     # Versionsnummer muss erscheinen
claude doctor        # diagnostiziert Installation/Auth/Config
```

Voraussetzung ist ein bezahltes Konto (Pro / Max / Team / Enterprise / Console) —
der Gratis-Plan schaltet Claude Code nicht frei. Beim ersten Start öffnet sich der
Browser zur Anmeldung.

## 2. Einmalig: Projekt vorbereiten

Dieses Kit (`CLAUDE.md`, `.claude/skills/preflight/`, `.claude/tools/`, `.gitignore`,
`SETUP.md`) liegt im
**Wurzelverzeichnis** deiner bestehenden Projektstruktur — neben `themen/`, `physiklib.js`,
`style.css` usw. Es fasst deine Inhalte nicht an.

Falls noch nicht unter Git:

```bash
cd /pfad/zu/tals-physik
git init
git add -A
git commit -m "Ausgangsstand + Claude-Code-Kit"
```

`node` sollte verfügbar sein (für die Tiefen-Checks im Pre-Flight): `node --version`.
Für die Tiefen-Checks (MathJax-Render + JS-Laufzeit) einmalig im Repo-Root:
`npm install mathjax-full jsdom`. Ohne diese Module laufen nur die schnellen Eigen-Checks;
die Tiefen-Checks werden mit `[WARN]` übersprungen (kein Blocker).
Die Browser-Werkzeuge in `.claude/tools/` (`render-check.mjs`, `scan-live.mjs`,
`build-bilder.mjs`) laufen unter Node, nicht unter Python. `playwright` steht in den
`devDependencies`, ein `npm install` im Repo-Root genügt also; die Browser-Binärdatei
kommt einmalig mit `npx playwright install chromium` dazu.

## 3. Laufender Workflow

```bash
cd /pfad/zu/tals-physik
claude
```

Claude Code liest `CLAUDE.md` automatisch und kennt damit alle Konventionen.

Dieses Repo ist auf `acceptEdits` konfiguriert (`.claude/settings.json`): Edits werden
ohne einzelne Diff-Bestätigung übernommen, und nach jedem Durchgang committet Claude Code
automatisch. Pro Arbeitseinheit:

1. **Auftrag bündeln.** Alle Änderungen einer Seite in einer Anweisung, z.B.
   „In p4-2-dynamik.html: Mini-Check 3 umformulieren, Beispiel 2 mit Ansatz-Prinzip
   neu, Reibungs-Abschnitt um eine ❓-Frage ergänzen."
2. **Claude Code editiert** direkt die lokale Datei — ohne Diff-Bestätigung.
3. **Pre-Flight + Commit laufen automatisch:** Claude Code führt den Pre-Flight aus und
   committet bei `ALLE CHECKS BESTANDEN` mit aussagekräftiger Message. Schlägt der Check
   fehl, wird nicht committet, sondern gemeldet und behoben.
4. **Browser-Sichtprüfung:** Datei lokal öffnen (Doppelklick oder
   `python3 -m http.server` im Wurzelverzeichnis, dann `localhost:8000/themen/…`).
   Nicht zufrieden? Per Anweisung nachjustieren — oder `git restore <datei>` /
   auf einen früheren Commit zurück.

Git ist das Sicherheitsnetz: `git diff`/`git log` zeigen jede Änderung im Nachhinein,
`git restore <datei>` rollt sauber zurück. Der **`git push` bleibt manuell bei dir** und
löst erst dann die Aktualisierung der Live-Website aus.

## 4. Was im Chat (Sandbox-Werkstatt) bleibt

Inhalts-Edits an Themenseiten und Anki-Rebuilds gehen lokal. Nur wo Spezial-Werkzeug
fehlt, lohnt der Umweg über den Chat:

| Aufgabe | Lokal möglich? |
|---|---|
| HTML/CSS/JS der Themenseiten | ja, Claude Code |
| Anki-APKG-Rebuild (ZIP+SQLite) | ja, wenn Python steht |
| xlsx-Recalc (Kalender, Soll-Ist) | nur mit LibreOffice installiert, sonst Chat |
| docx-Generierung (Lernziele) | nur mit docx-Libs/Skill, sonst Chat |

Reihenfolge bei Abhängigkeit: Inhalt lokal fertig → abgeleitetes Artefakt danach
regenerieren.

## 5. GitHub Pages (wenn so weit)

Repo zu GitHub pushen, in den Repo-Settings unter „Pages" den Branch als Quelle wählen.
Voraussetzung erfüllt: keine absoluten internen Pfade (alle Links relativ).
