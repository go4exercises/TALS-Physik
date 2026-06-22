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

Dieses Kit (`CLAUDE.md`, `.claude/skills/preflight/`, `.gitignore`, `SETUP.md`) liegt im
**Wurzelverzeichnis** deiner bestehenden Projektstruktur — neben `themen/`, `physiklib.js`,
`style.css` usw. Es fasst deine Inhalte nicht an.

Falls noch nicht unter Git:

```bash
cd /pfad/zu/tals-physik
git init
git add -A
git commit -m "Ausgangsstand + Claude-Code-Kit"
```

`node` sollte verfügbar sein (für den JS-Syntax-Check im Pre-Flight): `node --version`.
Für optionale Render-Checks: `pip install playwright && playwright install chromium`.

## 3. Laufender Workflow

```bash
cd /pfad/zu/tals-physik
claude
```

Claude Code liest `CLAUDE.md` automatisch und kennt damit alle Konventionen.

Pro Arbeitseinheit:

1. **Auftrag bündeln.** Alle Änderungen einer Seite in einer Anweisung, z.B.
   „In p4-2-dynamik.html: Mini-Check 3 umformulieren, Beispiel 2 mit Ansatz-Prinzip
   neu, Reibungs-Abschnitt um eine ❓-Frage ergänzen."
2. **Claude Code editiert** direkt die lokale Datei. Jede Änderung kommt als Diff —
   du bestätigst mit Yes / Yes-and-don't-ask-again / No.
3. **Pre-Flight läuft** (Claude Code kennt die Pflicht aus CLAUDE.md; sonst anstossen):
   ```bash
   python3 .claude/skills/preflight/preflight.py themen/p4-2-dynamik.html
   ```
   Muss `ALLE CHECKS BESTANDEN` zeigen.
4. **Browser-Sichtprüfung:** Datei lokal öffnen (Doppelklick oder
   `python3 -m http.server` im Wurzelverzeichnis, dann `localhost:8000/themen/…`).
5. **Committen** mit aussagekräftiger Message:
   ```bash
   git add themen/p4-2-dynamik.html
   git commit -m "p4-2: Beispiel 2 auf Ansatz-Prinzip, ❓ Reibung, MC3 umformuliert"
   ```

Git ist das Sicherheitsnetz: `git diff` zeigt jede Änderung, `git restore <datei>`
rollt sauber zurück. Keine ZIP-Snapshots mehr nötig.

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
