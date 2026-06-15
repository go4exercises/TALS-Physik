# HOWTO — Externe Videos, Simulationen und Aufgabensammlungen kuratieren

Dieser Leitfaden beschreibt den Workflow, mit dem die Sektion **„Externe Videos, Simulationen &amp; Aufgabensammlungen"** (Master-Schema §13) jeder Themenseite kuratiert wird. Adressat sind sowohl der Auftraggeber als auch Claude in jedem zukünftigen Chat.

Verwandte Dokumente: `STYLEGUIDE.md` §7.3, `HOWTO-neue-themenseite.md`, `COLLABORATION.md` §9.

> **Unterschied zu Mathe:** Physik-Themenseiten haben **drei** Spalten in dieser Sektion (Videos · Simulationen · Aufgaben), während Mathe nur zwei hat (Videos · Aufgaben). Interaktive Simulationen sind in Physik so verbreitet und didaktisch wertvoll (PhET, Walter Fendt, LEIFI), dass sie eine eigene Spalte verdienen.

---

## 1. Verbindliche Anbieter-Listen

Die Reihenfolge ist **strikt bindend**. Anbieter werden in genau dieser Reihenfolge geprüft, bis 4 Slots gefüllt sind (oder die Liste erschöpft ist).

### 1.1 Erklärvideos — bevorzugte YouTube-Kanäle

| # | Anbieter | YouTube-Handle | Charakter |
|---|---|---|---|
| 1 | musstewissen Physik | @MusstewissenPhysik | Sek I/II Schul-Erklärstil, MrWissen2go-nah, gut strukturiert |
| 2 | Lehrerschmidt | @lehrerschmidt | bis Klasse 10, breit, klare Themen-Erklärungen |
| 3 | Doc Schuster | @DocSchuster | Oberstufe/Abi, gründlich, sehr passende Tiefe für BM |
| 4 | Alexander Fufaev | @AlexanderFufaeV | Animationen + Theorie, sehr klare Visualisierung |
| 5 | Phil's Physics | @PhilsPhysics | Praxisnah, Schweizer Bezug |
| 6 | MrWissen2go Physik | (manche Physik-Videos auf @MrWissen2go) | sporadisch passend |

### 1.2 Interaktive Simulationen — bevorzugte Anbieter

| # | Plattform | URL | Charakter |
|---|---|---|---|
| 1 | PhET Boulder | https://phet.colorado.edu/de/simulations/category/physics | Klassiker, viele auf Deutsch, RLP-nah |
| 2 | Walter Fendt | https://www.walter-fendt.de/html5/phde/ | Sehr lange Bestand, HTML5, immer noch top |
| 3 | LEIFIphysik | https://www.leifiphysik.de/ | Themenstrukturierte Simulationen + Erklärtexte |
| 4 | oPhysics | https://ophysics.com/ | Sehr hochwertig, englisch (nur einsetzen, wenn deutsche Alternative fehlt) |

### 1.3 Aufgabensammlungen — bevorzugte Plattformen

| # | Plattform | URL | Charakter |
|---|---|---|---|
| 1 | LEIFIphysik | https://www.leifiphysik.de/ | Pro Lerngebiet eigene Aufgabenseiten mit Lösungen, RLP-nah |
| 2 | serlo.org | https://de.serlo.org/physik | frei lizenziert, breit |
| 3 | SwissEduc PrismaPhysik | https://www.swisseduc.ch/physik/ | Schweizer Lehrmittel-Quelle (für ausgewählte Themen) |
| 4 | abi-physik.de | https://www.abi-physik.de/ | Abi-fokussiert, Lösungen vorhanden |

---

## 2. Regeln für die Auswahl

### 2.1 Videos
- **Maximal 4 Links** pro Themenseite.
- **Pro Anbieter höchstens eine Playlist** (Vielfalt vor Tiefe).
- **Playlists strikt bevorzugt.** Wenn ein Anbieter zum Thema keine Playlist hat, weiter zum nächsten.
- **Falls nach Durchlauf aller 6 Anbieter weniger als 4 Playlists**: mit Einzelvideos auffüllen, wieder in derselben Anbieter-Reihenfolge.

### 2.2 Simulationen
- **Maximal 4 Links** pro Themenseite.
- **Pro Anbieter mehrere Simulationen erlaubt**, wenn sie unterschiedliche Aspekte des Themas abdecken (z.B. Walter Fendt hat zu Kinematik mehrere passende Sims).
- **Direkt-Links bevorzugt**, nicht Kategorie-Übersichtsseiten.
- **Deutsch bevorzugt** über Englisch, ausser die englische Version ist deutlich hochwertiger.

### 2.3 Aufgabensammlungen
- **Maximal 4 Links** pro Themenseite.
- **Lösungen müssen vorhanden sein.** Reine Aufgabenlisten ohne Musterlösung sind ausgeschlossen.
- **Pro Plattform sind mehrere Aufgabenseiten erlaubt**, wenn sie unterschiedliche Aspekte abdecken.

### 2.4 Negativ-Liste
- `physikunterricht-online.de` — Werbung-lastig, nicht systematisch
- `physikbuch.de` — Lizenz oft unklar
- YouTube-Suchergebnis-URLs (`/results?…`) — keine stabilen Links
- YouTube-Kurz-URLs (`youtu.be/…`) — Lang-Form bevorzugt
- Wikipedia — Nachschlagewerk, aber kein Erklärvideo oder Aufgabenset

---

## 3. Verifikationsmethode

> **Playlist-ID-Präfixe sind keine zuverlässigen Kanal-Indikatoren.**

### 3.1 Die zuverlässige Methode: `web_fetch` auf die Kandidaten-URL

```
web_fetch("https://www.youtube.com/playlist?list=<PLAYLIST_ID>")
web_fetch("https://www.leifiphysik.de/mechanik/<thema>/aufgaben")
web_fetch("https://phet.colorado.edu/de/simulations/<slug>")
```

Antwort enthält Titel, Anbieter und ggf. Inhaltsbeschreibung. Damit ist der Anbieter eindeutig identifiziert. Diese Verifikation kostet einen einzigen Tool-Aufruf pro Kandidat — das ist billiger als jede Heuristik, die später Fehler korrigieren muss.

### 3.2 Bei Simulationen zusätzlich prüfen
- Funktioniert die Simulation noch (kein Flash, kein Java-Applet, sondern HTML5/WebGL)?
- Ist sie auf Deutsch verfügbar?
- Behandelt sie genau das Phänomen, das auf der Themenseite zentral ist?

### 3.3 Bei Aufgaben zusätzlich prüfen
- Sind die Lösungen tatsächlich auf derselben Seite oder verlinkt?
- Niveau passt zu BM (nicht Bachelor-Physik, nicht Primar-Sachunterricht)?

---

## 4. HTML-Vorlage für die Sektion

Mit den drei Spalten:

```html
<h2 id="ressourcen">Externe Videos, Simulationen &amp; Aufgabensammlungen</h2>

<div class="ressourcen-subtitel">🎬 Erklärvideos</div>
<div class="links-grid">
  <a href="https://www.youtube.com/playlist?list=…" target="_blank" rel="noopener" class="lk">
    <span class="lk-ic">▶️</span>
    <div><div class="lk-t">⟪Titel⟫ — Playlist</div><div class="lk-s">⟪Anbieter⟫ · ⟪Videocount⟫</div></div>
  </a>
  <!-- weitere Karten -->
</div>

<div class="ressourcen-subtitel">🧪 Interaktive Simulationen</div>
<div class="links-grid">
  <a href="https://phet.colorado.edu/de/simulations/…" target="_blank" rel="noopener" class="lk sim">
    <span class="lk-ic">🧪</span>
    <div><div class="lk-t">⟪Titel⟫</div><div class="lk-s">⟪Anbieter⟫ · ⟪Kurzbeschreibung⟫</div></div>
  </a>
</div>

<div class="ressourcen-subtitel">📝 Aufgabensammlungen</div>
<div class="links-grid">
  <a href="https://…" target="_blank" rel="noopener" class="lk aufg">
    <span class="lk-ic">📝</span>
    <div><div class="lk-t">⟪Plattform⟫ — ⟪Thema⟫</div><div class="lk-s">⟪Aspekt⟫ · mit Lösungen</div></div>
  </a>
</div>
```

Beachte: nur Karten haben Klassen `.lk`, `.lk sim`, `.lk aufg` — der `<a>`-Tag selbst, nicht ein Wrapper.

---

## 5. Platzhalter bei Verifikation ausstehend

Wenn Verifikation in einem Chat aus Zeitgründen nicht abschliessend möglich war, MUSS die Karte einen Platzhalter-Vermerk tragen:

```html
<a href="https://…" target="_blank" rel="noopener" class="lk">
  <span class="lk-ic">▶️</span>
  <div><div class="lk-t">⟪Titel⟫</div><div class="lk-s">⟪Anbieter⟫ · Verifikation ausstehend</div></div>
</a>
```

Das ermöglicht, die Sektion in einem späteren Chat gezielt durchzuarbeiten und die Vermerke nach erfolgreicher Verifikation zu entfernen.
