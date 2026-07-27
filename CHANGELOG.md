# CHANGELOG — TALS Physik

> **Abgeschlossen — ab 14.06.2026 führt der Git-Verlauf die Änderungen.**
>
> Diese Datei stammt aus dem ZIP-Workflow, in dem es keine Versionsgeschichte
> gab. Seit der Umstellung auf Git ist der Commit-Verlauf die massgebliche
> Quelle; hier wird nichts mehr nachgetragen. Der letzte Eintrag unten ist
> Phase 5.41 vom 13.06.2026.
>
> **Wo steht seither was?**
> - Was wann geändert wurde: `git log --oneline` bzw. `git log -p <datei>`
> - Stand und Begründungen der Animations-Überarbeitung: `TODO-animationen.md`
> - Verbindliche Konventionen: `STYLEGUIDE.md`, Kurzfassung in `CLAUDE.md`
>
> Die Einträge unterhalb dieser Linie bleiben als Projektgeschichte bis
> Phase 5.41 erhalten und werden nicht mehr verändert.

---

## Archiv bis 13.06.2026

Alle bedeutenden Änderungen am Repository bis Phase 5.41, neueste zuerst.

Format an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/) angelehnt, gestrafft.

---

## 2026-06-13 · Phase 5.41 — .gitignore ergänzt

`.gitignore` schliesst vom Push aus: `COLLABORATION.md` (Project-Knowledge-Meta), `master-todoliste.md` (interne Liste), `node_modules/`, `package*.json`, OS-Artefakte. Bei bereits getrackten Dateien einmalig `git rm --cached` nötig.

## 2026-06-13 · Phase 5.40 — LICENSE und .nojekyll ergänzt

Repo-Hygiene für die GitHub-Pages-Veröffentlichung als Schwesterseite:
- **LICENSE** (CC BY-NC 4.0, Projektzeile «TALS Physik») im Repo-Root — von GitHub im Repo-Header erkannt.
- **.nojekyll** (leer) — Jekyll-Verarbeitung deaktiviert (Absicherung gegen Unterstrich-Pfade).

## 2026-06-13 · Phase 5.39 — Cross-Repo-Links auf korrekte absolute URLs

Vorbereitung der Veröffentlichung als Schwesterseite auf GitHub Pages (`go4exercises.github.io/TALS-Physik/`). Die Mathe-Verweise zeigten auf `tals-mathe` (klein) — auf case-sensitiven Pages-URLs falsch.

**Korrigiert:** alle Mathe-Querlinks (Header-Link «Mathematik ↗», index.html, Meta-Menü) auf `https://go4exercises.github.io/TALS-Mathe/` bzw. `github.com/go4exercises/TALS-Mathe`. Self-Repo-Links vereinheitlicht auf `TALS-Physik`. Schreibweisen jetzt konsistent: TALS-Physik (self) / TALS-Mathe (cross). `node --check` grün.

## 2026-06-13 · Phase 5.38 — Header entschlackt: «Übersicht»-Link und Breadcrumb-Zeile entfernt

Spiegelbildliche Anpassung zum Schwesterprojekt TALS-Mathematik [65]. Beide Elemente waren redundant: der «Übersicht»-Link dupliziert das zur Startseite führende Logo, die zweite Headerzeile (Breadcrumb + Vor/Zurück) wiederholt den Titelblock der Seite bzw. die Prev/Next-Links der TOC-Seitenleiste.

**Entfernt (`nav.js`):** der Desktop-Header-Link «Übersicht»; die komplette `breadcrumb-bar` samt `prevBtn`/`nextBtn`/`bcHTML`; Injection vereinfacht zu `nav-root.innerHTML = headerHTML`.

**Erhalten:** `cfg.prev`/`cfg.next` (TOC-Seitenleiste nutzt sie weiter für ← 4.2 / 4.4 →); mobiles «← Übersicht» im Flyout-Menü; Top-Level-Querlink «Mathematik ↗».

**Mobile-Abwägung** (wie in Mathe): TOC ab 900px ausgeblendet, Kapitelwechsel bleibt mobil über das «Themen»-Dropdown möglich (Direktsprung); Hauptnavigation vollständig erhalten.

**CSS aufgeräumt:** alle verwaisten Regeln entfernt (`.breadcrumb-bar`, `.breadcrumb`, `.bc-sep`, `.bc-cur`, `.prev-next`, `.pn-btn` samt Varianten und 700px-/640px-Sonderregeln).

**Verifiziert:** `node --check nav.js` grün; keine breadcrumb-/pn-/bc-Reste in nav.js oder style.css; jsdom-Render Homepage + `themen/p4-3-energie.html`: keine Breadcrumb-Zeile, kein Übersicht-Header-Link, Logo «Physik», «Mathematik ↗» erhalten, TOC behält prev (← 4.2) und next (4.4 →), mobiles «← Übersicht» erhalten.


## 2026-06-13 · Phase 5.37 — Header: Logo ohne TALS-Pille

Das Logo zeigt nur noch «Physik» — die `<span class="logo-pill">TALS</span>`-Pille ist entfernt (analoge Anpassung im Schwesterprojekt TALS-Mathematik, wo das Logo neu nur «Mathematik» zeigt). Die `.logo-pill`-CSS-Regel bleibt ungenutzt in `style.css`. Der bestehende Top-Level-Querlink «Mathematik ↗» im Header bleibt unverändert.

**Verifiziert:** `node --check nav.js` grün; keine `logo-pill`-Referenz mehr im JS; jsdom-Render (homepage): Logo-Inhalt nur «Physik», «Mathematik ↗» weiterhin als Top-Level-Link vorhanden.


## 2026-06-13 · Phase 5.36 — TOC: Kapiteltitel als «nach oben», sofortige Aktiv-Markierung, Kapitelnummer klein

Übernahme dreier Navigations-Verbesserungen aus dem Schwesterprojekt TALS-Mathematik (dort ZIP 62/63), Struktur war in `buildToC()` identisch.

- **Kapiteltitel klickbar = Sprung an den Seitenanfang.** Der TOC-Titel (`KAPITEL 4.3`) ist neu ein `<button class="toc-title">` und scrollt bei Klick instant nach oben (`window.scrollTo(0,0)`, kein Smooth-Scroll), bereinigt den URL-Hash und entfernt die Aktiv-Markierung. Entdeckbarkeit über dezenten ↑-Indikator (`.toc-title-pfeil`, nur bei Hover/Fokus sichtbar) plus Hover-/Fokus-Färbung (Bernstein); echtes Button-Element, tastatur-fokussierbar (`:focus-visible`), Pfeil `aria-hidden`. Ersetzt die Notwendigkeit eines separaten «nach oben»-Links; Vor/Zurück-Zeilen bleiben symmetrisch (oben nur prev, unten nur next).
- **Sofortige, konsistente Aktiv-Markierung beim Klick.** Bisher setzte nur der IntersectionObserver die `toc-aktiv`-Markierung (verzögert beim Klick, hängend beim Sprung oberhalb des ersten beobachteten h2). Ein Klick-Handler setzt sie nun unmittelbar auf den geklickten Titel; der Titel-Klick (Seitenanfang) entfernt sie. Verhalten bei Klick und Sprung damit einheitlich.
- **Kapitelnummer im TOC-Titel klein.** Der Titel hat `text-transform:uppercase`; die Kapitelnummer steht jetzt in `<span class="toc-kapnr">` mit `text-transform:none`, sodass allfällige Sub-Kennungen (a/b) klein bleiben — konsistent mit der Vor-/Zurück-Beschriftung. (In Physik ohne Sub-Buchstaben aktuell ohne sichtbaren Effekt, aber gleichgezogen, damit Mathe und Physik identische nav.js-Logik führen.)

**Verifiziert:** `node --check nav.js` grün; jsdom-Render auf `themen/p4-3-energie.html` (13 TOC-Einträge): Titel ist Button mit Pfeil-Indikator, Kapitelnummer im kapnr-Span, obere Zeile nur prev, untere nur next; Klick-Simulation auf den Titel löst `scrollTo(0,0)` aus und entfernt die Aktiv-Markierung. CSS auf Bernstein-Akzent adaptiert (nicht Mathe-Blau).


## 2026-06-10 · Phase 5.35 — Diagrammtitel und live-box-Labels: physikalische Grössen exakt geschrieben

- **Befund:** `.cv-titel` und `.live-box .lb-lab` setzen designbedingt `text-transform:uppercase` — Plaintext-Grössen wurden dadurch verfälscht: s(t)→S(T), a(t)→A(T), F(s)→F(S), p→P, f→F, h_e→H_E, und auch griechische Kleinbuchstaben (μ→Μ, λ→Λ, ω→Ω, γ→Γ) sowie Einheiten (bar→BAR, kWh→KWH). Vollinventar über alle uppercase-Klassen: betroffen waren ausschliesslich cv-titel (15) und lb-lab (12); block-titel/fl-label/h2/h3 enthalten keine case-sensitiven Plaintext-Grössen.
- **Fix nach bestehender Konvention** (kein neues CSS): die 27 Stellen auf 7 Seiten in MathJax gesetzt — wie bereits etabliert bei «Druck \\(p\\) über Temperatur \\(\\vartheta\\)» (cv-titel) und «Zeit \\(t\\)» (lb-lab). MathJax-Ausgabe ist von text-transform unberührt. Notation seitenkonform (\\(\\mu_{\\text{H}}\\) wie p4-2-Lösungen, \\(p_S\\) wie p4-5, \\(|\\vec{v}_{\\text{Ufer}}|\\) wie p4-1 A6); Einheiten upright via \\(\\text{bar}\\)/\\(\\text{mbar}\\)/\\(\\text{kWh}\\).
- Korrekt-grossgeschriebene Titel unverändert (U-I-Kennlinie, ΔT, «Umlaufzeit T», «Eingetauchtes V»).
- **Verifiziert:** Pre-Flight grün auf allen 7 geänderten Seiten (div/details-Bilanz, MathJax-Delimiter inline+display, keine Doppel-IDs, kein ß, keine Dezimalkommas); kein JS berührt (IDs nur auf lb-val).


## 2026-06-10 · Phase 5.34 — Slider-Zeilen zusammengelegt: mehrere Regler pro Animation in EINER sl-row

- **Diagnose:** 41 Animations-Stellen auf allen 10 Themenseiten verwendeten je eine eigene `.sl-row`-Box pro Schieberegler, untereinander gestapelt (2–4 Regler pro Animation; p4-4 Anim 2 als `zwei-spalten`-Variante mit 4 Reglern).
- **CSS zentral (`style.css`):** `.sl-row` um `flex-wrap:wrap` ergänzt; neue Klasse `.sl-grp` — jede Einheit Label+Slider+Wert ist eine unzertrennliche Flex-Gruppe (`flex:1 1 210px`, Label-min-width aufgehoben, Slider-min-width 60 px). Auf Desktop stehen damit alle Regler einer Animation auf einer Zeile; auf schmalen Screens brechen ganze Gruppen um — kein Overflow, kein vom Regler getrenntes Label.
- **HTML:** alle 41 Stapel per Skript zu je EINER `.sl-row` mit n `.sl-grp`-Kindern zusammengeführt (94 Gruppen gesamt); der `zwei-spalten`-Wrapper von p4-4 Anim 2 entfiel dabei (übrige `zwei-spalten`-Nutzungen sind Canvas-Layouts, unberührt). Slider-IDs, Wertebereiche und Inline-JS unverändert.
- **Verifiziert:** Pre-Flight grün auf allen 10 Seiten (div/details-Bilanz, MathJax-Delimiter, keine Doppel-IDs, kein ß, keine Dezimalkommas); Slider-Anzahl pro Seite identisch zu vorher; kein JS greift strukturell auf `.sl-row` zu; `node --check` aller Inline-Skripte OK.
- **Offen (lokaler Render-Check empfohlen):** Pixel-Sicht bei 1280/360 px (Playwright) — in der Sandbox nicht möglich (Browser-Binaries nicht erreichbar). Erwartung: 2–3er-Gruppen einzeilig ab ~700 px Inhaltsbreite, 4er-Gruppen (p4-4 a2, p4-5 a3, p5-2 a2) je nach Viewport ein- oder zweizeilig umbrechend.


## 2026-06-10 · Phase 5.33 — STYLEGUIDE v1.1: vier p4-1-Muster dokumentiert + Ideenlisten-Eintrag (todo-restpunkte Etappe 3, reine Doku)

- **STYLEGUIDE auf Version 1.1** (Stand Juni 2026), vier Einträge mit Verweis auf die Referenz-Implementierung in `themen/p4-1-kinematik.html` (Einstiegs-Animation `a0`, Phasen 5.28–5.30):
  - **§3.6 Label-Robustheit auf Canvas** (verbindlich für NEUE Labels): weisser Halo via measureText/fillRect + Rand-Klammerung (textAlign-Wechsel an der Innenseite der Bezugslinie); bestehende abgenommene Animationen werden nicht nachgerüstet. Referenz `a0Lbl`.
  - **§3.7 Einheiten-Zweitzeile an Achsen**: Hauptachse über drawGrid, zweite Zeile in der Nebeneinheit (graue Schrift, `gr.stepX`, Caption rechts), y-Bereich nach unten erweitert; adaptive drawGrid-Vergröberung auf schmalen Canvases akzeptiert. Referenz Minuten-Zeile in `drawA0`.
  - **§5.3 live-box-Gruppierung**: `style="margin-right:30px"` auf dem letzten Item der ersten Wertegruppe. Referenz Phase-Item der a0-live-box.
  - **§5.8 Direkt-Manipulation im Canvas** (optionales Interaktionsmuster, KEIN Pflicht-Rollout): Pointer-Events + setPointerCapture, Hit-Test mit Schwellen (~18 px Punkt, ~12 px Linien), Sprung-Klick, Werte-Raster, Hover-Cursor, `touch-action:pan-y`. Referenz `a0Hit`/`a0EvtT`/`a0Apply`.
- **master-todoliste, «Ideen für später»:** Einstiegs-Animationen für die übrigen 9 Themenseiten nach dem p4-1-Muster (pro Seite eigener Entwurfs- und Verifikationsaufwand).
- Alle fünf referenzierten Anker (`a0Hit`, `a0EvtT`, `a0Apply`, `a0Lbl`, `drawA0`) per grep in p4-1 bestätigt. Kein Code geändert.
- **Hinweis:** Die Project-Knowledge-Kopie des STYLEGUIDE muss manuell auf v1.1 synchronisiert werden.


## 2026-06-10 · Phase 5.32 — Druckseiten-Stichprobe Ansatz-Prinzip (todo-restpunkte Etappe 2)

Stichprobe je `teste-dich-selbst.html` und `aufgabenserie.html` von p4-3, p5-2 und p6-2 (4–5 Lösungen pro Datei) gegen das Ansatz-Prinzip gelesen — ergänzend zur grep-Diagnose vom 2026-06-09 (0 ⇒-Ketten, 0 v=s/t-Kurzformen).

- **Ein Trivialfix:** p4-3 `aufgabenserie.html`, Lösung 2 (Vollbremsung): «90 km/h = 25 m/s» → explizite Erst-Umrechnung der Seite «90 km/h = 90 000 m / 3600 s = 25 m/s». Python: 25.0 ✓. Pre-Flight der Datei grün.
- **Kein Befund sonst:** p4-3 (beide), p5-2 (beide; kWh = 3.6 MJ im Aufgaben-Intro definiert und in den Lösungen explizit verwendet), p6-1 nicht im Sample. p6-2 (beide, konsolidierte Lösungsboxen): inhaltlich sauber — symbolische Ansätze durchgängig, Ah→C explizit (3.0·3600 As), Stromsummen-Proben vorhanden; einzige ⇒ einschrittig.
- **Strukturelle Beobachtung (nur Meldung, gemäss Abgrenzung):** das konsolidierte p6-2-Lösungsformat («Lösungen 1–12» in einer Box statt Einzelboxen) bleibt formal abweichend von den übrigen Druckseiten; inhaltlich kein Handlungsbedarf.


## 2026-06-10 · Phase 5.31 — Tiefenprüfung A-Aufgaben-Lösungen aller 10 Themenseiten (Ansatz-Prinzip, todo-restpunkte Etappe 1)

Alle ~60 `loesung-body`-Blöcke gegen das Ansatz-Prinzip geprüft: (a) Beginn mit eingeführter Grundformel/benanntem Ansatz, (b) explizite Einheiten-Umrechnung beim ersten Auftreten pro Seite, (c) keine Inline-⇒-Ketten bei mehrschrittigen Umformungen.

- **p4-1 A4 (Kugelstossen):** «bekannte Reichweitenformel» ersetzt durch Herleitung aus den Wurf-Bewegungsgleichungen der Seite — Flugzeit aus \\(y(t_F)=0\\) (t_F ≈ 1.70 s), dann \\(s_x = v_0\\cos\\alpha \\cdot t_F \\approx 17.0\\) m. Python: t_F = 1.7036 s, s_x = 16.97 m — identisch mit dem alten Formelresultat. (Die separate Befundlisten-Iteration war in diesem Stand noch nicht enthalten; Treffer hier behoben.)
- **p4-2 A2:** Nebensatz «rund 16 km/h» → explizite Umrechnung 4.5 m/s = 4.5·3600 m/h = 16 200 m/h = 16.2 km/h (erste m/s→km/h-Umrechnung der Seite).
- **p4-3 A1:** symbolischer Ansatz W = F·s·cos α vorangestellt. **A2:** erste km/h-Umrechnung der Seite explizit (30 km/h = 30 000 m / 3600 s ≈ 8.33 m/s), Ansatz E_kin = ½mv² benannt.
- **p5-2 A1/A3/A4:** symbolische Ansätze ergänzt (Q = m·c·ΔT; Q = m·L_f beim Schmelzen). **A2:** Mischungsformel aus der Theorie vorangestellt, bevor c gekürzt wird. **A6:** symbolische COP-Formel COP_max = T_warm/(T_warm − T_kalt) ergänzt.
- **p5-3 A1/A2/A4:** symbolische Ansätze ergänzt (Δl = α·l₀·ΔT; γ = 3α; ΔV = γ·V₀·ΔT; Δh = γ·h₀·ΔT). **A5:** Kelvin-Umrechnung explizit (T₁ = 10 + 273 = 283 K, T₂ = 25 + 273 = 298 K) — erste der Seite.
- **Kein Befund:** p4-4 (Seilkraft-Formel in der Theorie hergeleitet), p4-5, p5-1, p6-1, p6-2 (durchgängig symbolische Ansätze; einzige ⇒ einschrittig). p6-2-Lösungsformat unverändert (konsolidierte Boxen, gemäss Abgrenzung nur Beobachtung).
- **Verifiziert:** alle 14 umgebauten/berührten Zahlenwerte Python-gegengerechnet (alle OK, Resultate unverändert); Pre-Flight grün auf allen 5 geänderten Seiten (div/details-Bilanz, MathJax-Delimiter inline+display balanciert, keine Doppel-IDs, kein ß, keine Dezimalkommas in Mathe); kein JS berührt.


## 2026-06-09 · Phase 5.30 — p4-1: live-box-Feinschliff, Herleitung mit Grafik + Eliminierung, Lösungs-Strukturierung (Auftrag 4_1b)

- **live-box der Einstiegs-Animation:** deutlicher Abstand nach dem Phase-Item (margin-right 30 px trennt Momentan- von Intervall-Grössen); Label «Δs (Fläche)»; Label «Δt = t₂ − t₁»; Δt-Wert neu in Stunden (toFixed(3), z.B. 7 min → 0.117 h) — macht die Division zu v̄ in km/h transparent (16.7 km / 0.117 h ≈ 142.9 km/h, headless gegengeprueft).
- **❓-Verständnisfrage nach Animation 1 ersetzt** (Bremsweg quadratisch — gut, aber verfrüht, braucht beschleunigte Bewegung + zeitlose Gleichung): neu «Was passiert mit der s-t-Geraden, wenn du die Geschwindigkeit verdoppelst?» mit Bezug auf Steigung, v-t-Linie und Fläche, direkt in Animation 1 nachvollziehbar.
- **Läufer-Einhol-Transfer (Mini-Check Darstellungen):** Lösung umstrukturiert — Ansatz \\(s_A(t_{einholen}) = s_B(t_{einholen})\\) vorangestellt, dann die Auflösungsschritte als einzelne Display-Zeilen untereinander (6·t = 30 + 4·t → 2·t = 30 → t = 15 s), Ort separat. SymPy-gegengerechnet.
- **Herleitung gleichmässig beschleunigte Bewegung:** (a) integrierte Trapez-Grafik — neues statisches Canvas `herl-cv` (max-width 430 px, zentriert) mit v(t)-Gerade, schraffiertem Trapez (parallele Seiten v₀ und v(t), Breite t), Flächen-Label «Fläche = s − s₀», role=img + aria-label; gezeichnet via `drawHerleitung()` in `renderAll` (resize-fähig); Geraden-Label rechtsbündig verankert, damit die steigende Gerade es nicht durchschneidet. (b) **Eliminierung als expliziter Zusatzschritt:** t = (v − v₀)/a in s(t) eingesetzt, Zwischenschritt bis (v² − v₀²)/(2a), dann umgestellt zur zeitlosen Gleichung — Algebra mit SymPy verifiziert (Differenz exakt 0).
- **Verifiziert:** Pre-Flight grün (div 319/319, span 159/159, MathJax-Delimiter 320/320 inline + 27/27 display, keine Doppel-IDs, `node --check` OK); Headless-Render mit lokal gerouteter MathJax-Kopie: live-box, Herleitungs-Block, Trapez-Grafik und Läufer-Lösung pixelgeprüft. Notiz: `minicheck.js`-Akkordeon schliesst beim programmatischen Massen-Öffnen andere Checks — für Screenshot-Automation gezielt nur den Ziel-Check öffnen.


## 2026-06-09 · Phase 5.29 — p4-1 Einstiegs-Animation: Direkt-Manipulation + Kompakt-Layout (Auftrag 4_1a.md)

- **Punkt und Marker direkt im Canvas ziehbar** (Pointer-Events mit `setPointerCapture`, Raster 0.5 min): oranger Momentanpunkt per Drag entlang der Kurve, Marker t₁/t₂ an den gestrichelten Linien (mit Griff-Punkten oben); Klick neben den Griffen lässt den Punkt dorthin springen. Hover-Cursor (grab/ew-resize) als Affordanz, `touch-action: pan-y` hält vertikales Scrollen auf Mobile frei. Die drei Schieberegler entfallen — Hit-Test bevorzugt den nächstgelegenen Griff, Clamps wie zuvor (t₁ < t₂, min. 0.5 min).
- **Layout kompakter:** Einstiegs-Absatz vor dem Widget entfernt (Inhalt steckt in Titel + «Worauf achten?»); v̄-Berechnung aus der separaten formel-live-Zeile in die live-box verschoben, direkt hinter Δs und Δt; Diagrammtitel auf «v(t) — Momentangeschwindigkeit der ganzen Fahrt» gekürzt.
- **Überstrich korrekt:** live-box-Label als MathJax `\\(\\bar{v} = \\Delta s / \\Delta t\\)` — Strich steht über dem v (verifiziert im Headless-Render mit lokal gerouteter MathJax-Kopie: 338 mjx-Container, 7 in der live-box).
- **x-Achse in Stunden und Minuten:** Bereich auf −0.05…1.05 h umgestellt, `niceStep` liefert auf normaler Breite exakt 0.1 h = 6 min; zweite Beschriftungszeile mit Minutenwerten (6, 12, … 60) + «min»-Caption unter den Stunden-Ticks (yMin auf −25 erweitert für die Zusatzzeile). Auf sehr schmalen Canvases (≈ 360 px) adaptiv 0.2 h = 12 min im selben Schema.
- **Marker-Labels robust:** weisser Halo + Seitenwechsel-Klammerung am Canvas-Rand (t₁ bei 0 und t₂ bei 60 voll lesbar, keine Tick-Kollision).
- **Mini-Check Einstieg, Transfer ersetzt:** Tunnel-Aufgabe (Zuglänge addieren — verfrüht) durch passendere ersetzt: erste 20 km in 10 min → v̄ = 120 km/h trotz zeitweise 150 km/h (Anfangsbeschleunigung drückt den Schnitt); direkt mit den Markern in der Animation nachprüfbar (s(10 min) = 20.0 km exakt im Profil).
- **Verifiziert:** Drag-Interaktion headless durchgespielt (Punkt 24→31 min → 60 km/h «bremst»; Marker 12..19 → Δs 16.7 km, Δt 7.0 min, v̄ 142.9 km/h; Touch-Tap auf Halt → 0 km/h) — identisch mit Python-Gegenrechnung; 0 px Mobile-Overflow; Pre-Flight grün (div 318/318, span 159/159, MathJax-Delimiter 317/317 + 23/23, keine Doppel-IDs, `node --check` OK).


## 2026-06-09 · Phase 5.28 — p4-1 Einstieg interaktiv + Mini-Check-Lösungen vereinheitlicht (Auftrag 4_1.md)

- **Einstiegs-Animation neu (`a0`):** interaktives v(t)-Diagramm der Zugfahrt Bern–Zürich, passend zum Einstiegsbeispiel — stückweise lineares Profil mit 60 min Gesamtfahrzeit und **exakt 120 km** Fläche unter der Kurve (Python-verifiziert; Plateaus 140/150/160 km/h, Zwischenhalt bei min 32.5–35.5). Schieberegler bewegt einen Punkt auf dem Graphen mit Live-Anzeige der Momentangeschwindigkeit und der Phase; Kurvensegmente farblich nach Phase markiert (grün a>0, rot a<0, blau konstant) mit `canvas-legend`-Legende. Zwei schiebbare Marker t₁/t₂ (gegenseitig geklemmt, min. 0.5 min Abstand) wählen ein freies Intervall: Live-Anzeige von Δs, Δt und v̄ = Δs/Δt in der `formel-live`-Zeile, Intervallfläche unter der Kurve schraffiert (= Δs). Default t₁=0, t₂=60 → v̄ = 120 km/h wie im Text. Canvas mit `role="img"` + ausführlichem `aria-label`.
- **Einstiegs-Text konsistent gemacht:** «die ganze Fahrt über 140–160 km/h» → «auf freier Strecke 140–160 km/h, beim Zwischenhalt 0 km/h» (sonst widerspräche der 120-km/h-Schnitt der Anzeige).
- **Mini-Check nach Einstieg, Lösungen 1–4 gemäss Auftrag:** (1)+(2) verwenden jetzt explizit die Einstiegs-Formel v̄ = Δs/Δt statt v = s/t; (3) zeigt die Umrechnung 72 km/h = 72000 m / 3600 s = 20 m/s (Schnellweg ÷3.6 als Zusatz); (4) Tunnel-Transfer startet mit v̄ = Δs/Δt und stellt nach Δt um.
- **Verifiziert:** Profil-Integral, v(31)=60 km/h, Δs(28..40)=12.5 km, v̄(12..19)=142.9 km/h per Python gegengerechnet und im Headless-Browser identisch; Pre-Flight grün (Marker, div/span-Bilanz 323/323 u. 160/160, MathJax-Delimiter balanciert, keine doppelten IDs, `node --check` OK); Playwright-Render bei 1280 px und 360 px — Marker-Labels t₁/t₂ nach erstem Render von der Oberkante weg auf feste Höhe seitlich der Linien verlegt (Clipping behoben).


## 2026-06-08 · Phase 5.27 — Wurf-Label-Überlappung behoben (P3-2 Nachgang)

- **p4-1 Wurfparabel (`a4`):** das `sₓ`-Auftreffweite-Label lag bei `cy(0)+18`, also in der x-Achsen-Tick-Zeile, und überlappte die Ticks „40"/„45" sowie den Landepunkt. Jetzt über die Achse versetzt (`cy(0)-8`, rechts vom Auftreffpunkt, linksbündig) mit Rand-Klammerung: bei grossem sₓ (bis ~92 m bei festem xMax=100) kippt das Label automatisch nach links (rechtsbündig), damit es nicht über den rechten Canvas-Rand läuft. `physiklib.js` unberührt.
- **Hebel-Tilt (p4-4, Bild 9 aus dem Review):** vom Auftraggeber bestätigt — der Balken pendelt sich waagrecht ein, der gekippte Screenshot war nur ein Animations-Frame. Kein Fix nötig.
- **Verifiziert:** p4-1 `<div>`-Bilanz ausgeglichen, Inline-JS `node --check` + jsdom-Laufzeit grün, MathJax 0 Fehler.

Damit ist der visuelle Review von P2-3/P3-2 vollständig abgeschlossen: Overflow ueberall OK, alle Achsen-Ticks lesbar, vier Label-Positionierungen korrigiert (p4-5 s₂, p4-5 h_e, p5-2 Mischung, p4-1 sₓ), Physik in allen geprueften Animationen korrekt.

## 2026-06-08 · Phase 5.26 — Visueller Render-Check abgeschlossen + Label-Clippings behoben (P2-3/P3-2 lokal)

Der Auftraggeber hat den Render-Check lokal auf Win 11 (Playwright/Chromium) gefahren — Ergebnisse hier ausgewertet.

- **Mobile-Overflow (P2-3):** ueberall OK (kein horizontaler Overflow bei 360/390 px) -> der 5.20-Layout-Fix ist visuell bestaetigt.
- **Achsen-Ticks (P3-2):** alle Diagramme lesbar (p_S-h, Heizkurve, p-ϑ mit Extrapolation, Celsius/Kelvin, F_A-h_e, p-V, p-T) — keine abgeschnittenen/gequetschten Tick-Werte.
- **Gas-Frage p5-3 geklaert (kein Bug):** Animation 6 (Boyle/Amontons) ist in sich konsistent (p·V = 6.0 bar·L, Marker 2.0 L | 3.00 bar; Amontons p/T = 1/300 bar/K). Die abweichenden 3.0 L / 1.00 bar stammen vom separaten Teilchenmodell-Widget — zwei unabhaengige Darstellungen.
- **Drei Label-Clippings am Canvas-Rand behoben** (Positionierung angepasst, `physiklib.js` unberuehrt — STYLEGUIDE §3.4):
  - **p4-5 hydraulische Presse** (`s₂`-Label): Hubweg-Pfeil + Label von rechts (ueber den Canvas-Rand) auf die Innenseite des grossen Kolbens gespiegelt, rechtsbuendig — analog zu `s₁`.
  - **p4-5 Auftrieb/Quader** (`h_e`-Label): Tiefen-Label vom linken Aussenrand (abgeschnitten) nach innen ins Becken verschoben, linksbuendig; Tiefen-Pfeil bleibt im Rand.
  - **p5-2 Mischungstemperatur**: Becher-Grundlinie von `H·0.88` auf `H-40` gesenkt, damit die untere Wertezeile (`Xkg · Y°C`, vorher bei 241 px in 240-px-Canvas) vollstaendig in den Canvas passt.
- **Verifiziert nach Fix:** beide Seiten `<div>`-Bilanz ausgeglichen, Inline-JS `node --check` + jsdom-Laufzeit grün (Libs/Nav/ToC rendern, 0 Fehler), MathJax 0 Fehler. Pixel-genaue Sicht bestaetigt der Auftraggeber mit einem erneuten Render-Lauf der drei Canvas.

## 2026-06-08 · Phase 5.25 — Druckseiten-Dichte und Achsen-Ticks geprüft (Audit P3-1, P3-2)

Zwei Verifikations-Checks (keine Inhaltsänderung).

**P3-1 — Aufgaben-Dichte der Druckseiten** (Soll: teste-dich-selbst 12, aufgabenserie 8; Zählung über `aufg-rahmen`/`aufg-nr` + Lösungs-Parität):
- **8 von 10 Themen exakt konform:** je 12 teste + 8 serie, jede Aufgabe mit eigener `loes`-Lösungsbox (p4-1, p4-2, p4-3, p4-4, p5-1, p5-2, p5-3, p6-1).
- **p4-5 Hydrostatik:** 13 teste + 9 serie — je **eine mehr** als der Standard, intern konsistent (Lösungen vorhanden). Kein Defekt, nur Abweichung vom dokumentierten Soll.
- **p6-2 Elektrizität:** korrekte Anzahl (12 + 8), Lösungen **vorhanden**, aber in **konsolidiertem `<ol>`-Listenformat** («Lösungen 1–12») statt je Aufgabe einer `loes`-Box wie auf den anderen 9 Seiten. Markup-/Formatabweichung, kein Inhaltsdefizit.
- Beide Abweichungen bewusst **nicht** automatisch geändert (kein unaufgeforderter Inhalts-Eingriff) — Normalisierung auf Wunsch.

**P3-2 — Achsen-Tick-Lesbarkeit der dichtesten Seiten** (p4-3, p4-4):
- Echter Browser für Screenshots nicht verfügbar (Chromium gesperrt, wie P2-3). Stattdessen die `niceStep`-Tick-Generierung für die literalen `drawGrid`-Bereiche durchgerechnet (Plotbreite mobil ~300 px / Desktop ~520 px).
- Ergebnis: alle Achsen-Diagramme liefern **4–11 Haupt-Ticks pro Achse** — im lesbaren Band (3–12), keine Ein-Tick-/Klebe-am-Rand-Anti-Patterns (STYLEGUIDE §3.4). Variablen-Bereiche (`Fmax*1.05` usw.) nutzen dieselbe Automatik mit +5%-Reserve. Die übrigen Canvas auf p4-3/p4-4 sind schematische/Vektor-Darstellungen ohne numerische Achsen (kein Tick-Thema).
- **Offen (braucht Render):** visuelle Bestätigung, dass Labels nicht abgeschnitten werden und nicht mit Inhalts-Markern überlappen — per lokalem Browser auf dem Win-11-Rechner abzuschliessen.

## 2026-06-08 · Phase 5.24 — Render-Verifikation, browserlos (Audit P2-3)

Ein echter Headless-Browser ist in der Arbeitsumgebung **nicht verfügbar** (Chromium-Download über `cdn.playwright.dev` ist netzseitig gesperrt — 403; Ubuntu-24-Chromium ist Snap-only). Daher die Render-Verifikation browserlos mit echten Engines durchgefuehrt (npm erlaubt):

- **MathJax (echt, `mathjax-full` in Node, tex2svg):** alle Formel-Ausdruecke der gesamten Suite einzeln durch MathJax geschickt — **4659 Ausdruecke** (2492 auf 10 Themen- + 3 Hub-Seiten, 2167 auf 40 Druckseiten), **0 Parser-Fehler / 0 `merror`**. Bestaetigt, dass der Phase-5.16-Fix haelt und P2-1/P2-2 nichts gebrochen haben.
- **MathJax-Delimiter-Config:** 0 Dateien mit fehlerhaft einfach-maskiertem Delimiter; `\(…\)`/`\[…\]`-Balance ueber alle HTML ausgeglichen.
- **JS-Laufzeit (jsdom, `runScripts:'dangerously'`):** alle 10 Themenseiten geladen mit Stubs fuer Canvas-2D-Kontext, `IntersectionObserver`, `requestAnimationFrame`, `matchMedia`, `speechSynthesis`, MathJax; `DOMContentLoaded`/`load`/`resize` ausgeloest. Ergebnis je Seite: geteilte Libs laden und definieren `buildNav`/`initCanvas`/`toggleL`, `#nav-root` und `#toc` werden tatsaechlich befuellt, **0 JS-Laufzeitfehler**. Geht ueber `node --check` (nur Syntax) hinaus — faengt `ReferenceError` in der Animations-Init ab.
- **Pruefskripte ins Repo gelegt** (reproduzierbar): `scripts/verify_mathjax.js`, `scripts/verify_js_runtime.js` (benoetigen `npm install mathjax-full jsdom`).
- **Weiterhin offen (braucht echten Browser):** visuelle Layout-Pruefung inkl. Mobile-0px-Overflow (Bestaetigung des 5.20-Fixes) und Canvas-Pixelausgabe / Tick-Lesbarkeit (COLLABORATION §3.9). jsdom rechnet kein Layout und rendert kein Canvas. Als Pre-Launch-Gate vorgemerkt, sobald Chromium verfuegbar ist.

## 2026-06-08 · Phase 5.23 — Dokumentsprache auf `de-CH` (Audit P2-2)

- **`<html lang="de">` → `<html lang="de-CH">`** in **allen 54 HTML-Dateien** (10 Themenseiten, index, glossar, formelsammlung, TEMPLATE, 40 Druckseiten). Präziser für ein Schweizer Lehrmittel: passt zur ß-losen Konvention und gibt Screenreadern/Browsern die korrekte Sprachvariante (Aussprache, Silbentrennung).
- **Bewusst unberührt:** die TTS-Locale `lang='de-DE'` in `anim-hinweise.js` (Sprachausgabe-Stimme der Vorlese-Funktion, nicht die Dokumentsprache) — `de-CH` hat keine eigene Vorlese-Stimme, `de-DE` bleibt die sinnvolle Wahl.
- **Verifiziert:** 54× `lang="de-CH"`, 0× verbliebenes `lang="de"`; reiner Attributwert-Wechsel, keine Tag-Änderung.

## 2026-06-08 · Phase 5.22 — Dünne Ressourcen-Spalten aufgefüllt (Audit P2-1)

Die im Audit als dünn markierten Ressourcen-Spalten mit **verifizierten** Links aufgefüllt (kein Padding mit Unverifiziertem; HOWTO §9.1-Reihenfolge). Alle Ergänzungen vorab per Suche bestätigt (serlo-/LEIFI-URLs wörtlich als Treffer, musstewissen-Physik-Kanal existiert).

- **p4-3 Energie** [3,4,2] → **[3,4,3]:** +Aufgaben serlo `50784/energie` (frei lizenziert, mit Musterlösungen).
- **p5-2 Wärme** [2,3,2] → **[3,3,3]:** +Video musstewissen Physik (Kanalsuche «wärme»), +Aufgaben serlo `50791/thermische-energie`.
- **p5-3 Wärmeausdehnung** [2,3,2] → **[3,3,2]:** +Video musstewissen Physik (Kanalsuche «wärmeausdehnung»). Aufgaben-Spalte bleibt bei 2 (beide LEIFI-Themen on-topic, mit Musterlösungen — laut HOWTO zulässig).
- **p6-1 Wellen** [2,3,1] → **[3,3,3]:** +Video musstewissen Physik (Kanalsuche «wellen»), +Aufgaben serlo `50810/mechanische-schwingungen-und-wellen` und LEIFI `akustik/akustische-wellen` (Schallwellen, Doppler · mit Musterlösungen).
- **Video-Links bewusst als Kanalsuche** (`@musstewissenPhysik/search?query=…`), nicht als einzelne Video-IDs — stabil auf Kanal-Ebene und damit nicht von der P1-3-Unsicherheit einzelner YouTube-IDs betroffen. Etabliertes Muster (bereits p4-1, p4-5).
- **Verifiziert:** alle vier Seiten — neue Karten in der korrekten Spalte, `<a>`/`<div>`-Bilanz ausgeglichen, je 3 Ressourcen-Subtitel, keine Duplicate-Marker, Slot-Limits eingehalten (alle Spalten ≤4), VID-Card-Icon konsistent (▶️), kein ß, Inline-JS `node --check` grün.

## 2026-06-08 · Phase 5.21 — Externe Links verifiziert (Audit P1-3, Link-Rot-Prüfung)

Erreichbarkeits- und Owner-Prüfung der 86 distinkten externen Ressourcen-Links nach HOWTO §9.3 (Suche → Fetch → Owner/Schema). Methodisch ehrlich: YouTube ist aus der Arbeitsumgebung nicht verlässlich per Fetch prüfbar (429 bzw. vergiftete/identische Junk-Antworten unabhängig von der ID) — daher separat über Kanal-Existenz behandelt und im Übrigen für einen Browser-Spot-Check offengelassen.

- **Verifiziert live (hohe Sicherheit):**
  - **PhET** (17 Sims): 16 sind aktuelle HTML5-Sims; Ausnahme siehe unten.
  - **Walter Fendt**: HTML5-Sammlung lebt (57 Apps, Stand 2025-03-30), deutsches `_de.htm`-Schema über die englischen Parallelseiten bestätigt.
  - **LEIFIphysik**: `www.leifiphysik.de`-Schema aktuell; zwei Aufgaben-URLs wörtlich mit Musterlösungen bestätigt (`einfache-maschinen/aufgaben`, `kraft-und-bewegungsaenderung/aufgaben`); Themen-Taxonomie aktuell.
  - **serlo**: zwei URLs wörtlich live bestätigt (`43283/elektrischer-widerstand-und-das-ohmsche-gesetz`, `50762/temperatur-und-teilchenbewegung`); numerische-ID- und `/mechanik/klassische-mechanik/`-Pfadschema aktuell.
  - **Lehrer-Schmidt**: Site lebt; alle referenzierten Bereiche (`/physik/`, `/physik/mechanik/`, `/physik/wärmelehre/`, `/physik/elektrizität/`) existieren.
- **Gefunden und behoben (3 Links entfernt):**
  - **PhET `ramp-forces-and-motion`** (p4-2): nur noch als Java-Legacy-Sim erreichbar (`/legacy/`), läuft nicht mehr im Browser. Entfernt — der Fendt-`inclinedplane` deckt die schiefe Ebene bereits ab. Simulationen-Spalte p4-2: 4 → 3.
  - **SwissEduc `swisseduc.ch/physik/`** (p4-2 und p4-5): blanke Bereichs-Landing ohne spezifische Aufgaben-mit-Lösung (taucht in Aufgaben-Suchen nicht auf). Beide entfernt — wie schon zuvor auf p4-4. Aufgaben-Spalten: p4-2 4 → 3, p4-5 4 → 3.
- **Nicht aus der Umgebung verifizierbar (Browser-Spot-Check empfohlen):**
  - **YouTube** (18 URLs): Kanäle existieren (musstewissen, Lehrerschmidt bestätigt), aber die einzelnen opaken Video-IDs und zwei Playlists lassen sich hier nicht auf «lebt noch» prüfen. Empfehlung: fragile Einzelvideo-Links langfristig auf stabile Kanal-/Playlist-Links umstellen.
  - **Fufaev** (`de.fufaev.org/mechanik`, `/druck`): Domain lebt, aber die blanken Kategorie-Pfade nicht belegt (Seite umorganisiert).
- **Verifiziert nach den Edits:** p4-2/p4-5 — `<a>`/`<div>`-Bilanz ausgeglichen, je 3 Ressourcen-Subtitel, `<aside>`/`<footer>` intakt, Slots p4-2 [3,3,3] / p4-5 [4,4,3] (alle ≤4 und ≥3), Inline-JS `node --check` grün.

## 2026-06-07 · Phase 5.20 — Technische und organisatorische Qualität (Priorität 5, #35–#42)

Technik- und Organisations-Durchgang. Headless mit Playwright real verifiziert (Mobile 360/390 px, Desktop 1280 px).

- **#35 Projektstruktur aufgeräumt:** Keine verschachtelten ZIPs im Projekt. Build-Cache (`__pycache__`, `*.pyc`) und temporäre `*.bak` aus dem Paket ausgeschlossen; Auslieferung als einzelner Top-Ordner `tals-physik/` (keine doppelte `tals-physik/tals-physik/`-Schachtelung mehr). Quell-Skripte (`scripts/*.py`) bleiben im Repo.
- **#36 Template gekennzeichnet:** `TEMPLATE.html` trägt bereits Kommentar-Header + sichtbaren Vorlage-Banner (blendet sich aus, sobald `style.css` lädt). Zusätzlich `<title>` mit `[VORLAGE]`-Präfix versehen, damit auch der Browser-Tab die Vorlage ausweist. Platzhalterlinks (⟪…⟫) bleiben bewusst bestehen.
- **#37 Navigation getestet:** Statische Link-Auflösung — alle 84 echten internen Links lösen auf existierende Dateien auf (die 6 „defekten" sind die gewollten Platzhalter in `TEMPLATE.html`). Playwright: jede der 10 Themenseiten lädt von der Startseite aus, besitzt einen funktionierenden Zurück-Link zur `index.html`, 0 JS-Fehler.
- **#40 Performance/Mobile:** Animations-Architektur geprüft — keine Dauerläufer: button-gesteuert (p4-1/2/3), statisch (p4-4/5) oder per `IntersectionObserver` off-screen pausiert (p5/p6). **Mobile-Layout-Bug gefixt:** Der Mobile-Grid-Override (`@media max-width:900px`) setzte `grid-template-columns: 1fr` und löste damit einen Grid-Blowout aus (min-content breiter Tabellen/Live-Boxen blähte die Spalte auf 628–855 px auf → 185–479 px horizontaler Overflow auf **jeder** Themenseite). Fix in `style.css`: Spalte auf `minmax(0, 1fr)`, breite Datentabellen/Live-Boxen mobil horizontal scrollbar (`display:block; overflow-x:auto`), `.page-wrap` mobil mit `overflow-x:hidden` als Riegel. Ergebnis: 0 px Overflow bei 360/390 px **und** Desktop unverändert (TOC-Sidebar erhalten, 0 px).
- **#41 Version/Stand:** `Version 0.9 · Stand Juni 2026` im Footer **aller** Seiten (14 HTML-Dateien) sowie als eigener Abschnitt in `README.md`.
- **#42 Changelog:** `CHANGELOG.md` (diese Datei) in `README.md` verlinkt und als Pflege-Ort benannt.
- **Verifiziert:** Playwright Mobile (360/390) + Desktop (1280) — alle Seiten 0 JS-Fehler, alle Canvases gezeichnet, 0 Overflow, Versionszeile sichtbar, Back-Link vorhanden. Tag-Balance der footer-editierten Seiten geprüft.

## 2026-06-07 · Phase 5.19 — Sprache und Stil vereinheitlicht (Priorität 4, #29–#34)

Suite-weiter Sprach- und Stil-Durchgang. Befund: Die zehn Themenseiten waren bereits weitgehend konventionskonform; nur wenige Ausreisser.

- **#29 Anrede vereinheitlicht:** Konvention 1:1 aus TALS Mathematik bestätigt — Theorie unpersönlich (man/wer/Passiv), Aufgaben und interaktive Prompts im **du-Imperativ**, kein „Sie". Einziger Ausreisser war `downloads/themen/p4-5-hydrostatik/aufgabenserie.html` mit 12 Höflichkeits-Imperativen; auf du-Imperativ umgestellt (Verwende, Diskutiere, Begründe, Vergleiche, Stelle … auf, Bestimme, Schätze … ab, Berechne, Gib … an). Alle anderen 34 „Sie"-Treffer in der Suite sind satzinitiales Pronomen „sie" (die Kraft → sie …), keine Anrede.
- **#30 Begriffe konsequent:** „Schnelligkeit" kommt nirgends vor. „Tempo" bleibt als feste Komposita (Tempomat, Tempolimit) sowie als bewusst umgangssprachliches Synonym in Intuitions-Kontexten (p4-3, p5-1). Einmalige Klärung an der Erstdefinition in p4-1 ergänzt: Betrag der Geschwindigkeit = umgangssprachlich Tempo.
- **#31 Schweizer Rechtschreibung:** Suite-weiter ß-Scan — **0 Treffer** in allen Inhalts-HTML. Bereits sauber.
- **#32 Formulierungen vereinfacht:** Längste Theorie-Sätze identifiziert (≥32 Wörter). Zwei echte verschachtelte Brocken geteilt: p5-2 (Wärmepumpe/Wärme-Kraft-Kopplung, 44 W → 4 Sätze) und p4-5 (Archimedes-Satz am Gedankenstrich). Die übrigen langen Sätze sind bewusste „roter Faden"-Aufzählungen im Einstieg (A, B, C und D) bzw. bereits per Doppelpunkt gegliedert — absichtlich belassen.
- **#33 Überschriften vereinheitlicht:** h2-Reihenfolge über alle zehn Seiten geprüft — bereits durchgehend identisch (Einstieg → Grundbegriffe → Themenabschnitte → Aufgaben → Zusammenfassung → Zusatzmaterial → Externe). Keine Änderung nötig.
- **#34 Rechtschreibung final:** ß-, Dezimalkomma- und Tag-/LaTeX-Balance-Scan über die geänderten Dateien. Nebenbefund (Prio-3-Notation, nicht Prio 4): ein Dezimalkomma in einem JS-Kommentar in p4-1 (`91,7`/`22,9`) auf Punkt korrigiert.
- **Verifiziert:** Geänderte Themenseiten — `<p>`/`<div>`/`\(…\)`/`\[…\]` balanciert, Skelett-Marker `pw=1 mc=1 ml=1 bad=0`, Inline-JS `node --check` grün, kein ß.

## 2026-06-07 · Phase 5.18 — Mini-Checks zentralisiert und auf alle Themenseiten ausgerollt

Nach Freigabe des p4-1-Prototyps (Phase 5.17) wurde das Muster vereinheitlicht und flächendeckend eingesetzt.

- **Zentralisiert:** Die Akkordeon-Logik (immer höchstens ein Mini-Check offen) liegt jetzt in der neuen gemeinsamen Datei **`minicheck.js`** (auf jeder Themenseite nach `anim-hinweise.js` eingebunden). Das Inline-Skript auf p4-1 wurde durch diese Einbindung ersetzt — keine Duplizierung mehr pro Seite. Gestaltung weiterhin zentral in `style.css` (Abschnitt «Mini-Checks»).
- **Ausgerollt:** Auf **allen 10 Themenseiten** trägt jeder Inhaltsabschnitt am Ende einen einklappbaren Mini-Check (standardmässig zu) mit vier Teilaufgaben — Multiple Choice, Lückentext, kurze Rechnung und Transfer — samt Lösungseinblendung je Teilaufgabe. Jeder Check prüft genau den vorangehenden Abschnitt. Summe: **81 Mini-Checks** (p4-1: 8, p4-2: 8, p4-3: 9, p4-4: 9, p4-5: 8, p5-1: 7, p5-2: 8, p5-3: 8, p6-1: 8, p6-2: 8).
- **Inhalt verifiziert:** Alle Zahlenwerte vorab in Python nachgerechnet (Asserts in den Aufbau-Skripten). Schweizer Hochdeutsch, Dezimalpunkt.
- **Dokumentiert:** STYLEGUIDE §5.7 (Mini-Check-Muster), HOWTO und COLLABORATION §3.8 (Abhängigkeit `minicheck.js`).
- **Verifiziert:** Suite-weit div-Balance und `\(…\)`-Balance ausgeglichen, kein ß, je Mini-Check genau 4 Teilaufgaben, `minicheck.js` auf allen Seiten eingebunden, `node --check` grün. Echtes Rendering headless auf Stichprobe (p4-4, p5-2, p6-2): standardmässig alle zu, Akkordeon schliesst den vorigen beim Öffnen des nächsten (max. 1 offen), 0 `merror`, 0 Rohformeln, 0 JS-Fehler.

Aufbau-Hilfsskripte: `scripts/minicheck_lib.py` (Builder + `apply_page`) und `scripts/_mc_batch1.py … _mc_batch5.py` (Inhalte pro Seite, mit Zahlen-Asserts).

---

## 2026-06-06 · Phase 5.17 — Prototyp: Mini-Checks + Transferfragen pro Abschnitt (nur p4-1)

Test auf der Prototyp-Seite p4-1 (Kinematik): nach jedem inhaltlichen Abschnitt ein kleiner Selbsttest.

- **Mini-Check** je Abschnitt, **einklappbar** (natives `<details>`, standardmässig zu → wenig visuelles Gewicht). Klick auf die Kopfzeile «✏️ Mini-Check» öffnet ihn; ein kleines Akkordeon-Skript sorgt dafür, dass **immer höchstens ein** Mini-Check offen ist (beim Öffnen des nächsten schliesst der vorherige).
- Vier Teilaufgaben pro Mini-Check: **Multiple Choice**, **Lückentext** (mit Ausfüll-Strich), **kurze Rechnung** und **Transfer** (als gleichwertige vierte Teilaufgabe integriert, ohne gesonderten «für Leistungsstarke»-Block).
- **Lösungseinblendung** je Teilaufgabe über natives `<details>` (kein JS, tastatur-/screenreader-tauglich) — gleiche Mechanik wie die bestehenden Verständnisfragen/Lernziele.
- Abgedeckt: alle 8 Inhaltsabschnitte; jeder Check prüft genau den vorangehenden Abschnitt.
- Gestaltung zentral in `style.css` (Abschnitt «Mini-Checks»), durchgehend Bernstein; keine erfundenen Klassen. Akkordeon-Logik vorerst als kleines Inline-Skript auf p4-1 (wird bei Freigabe analog zu den Hinweisen zentralisiert).
- Verifiziert: alle Zahlen in Python nachgerechnet; alle 295 Formel-Spans der Seite einzeln durch echtes MathJax (0 Fehler); echtes Rendering headless — standardmässig alle zu, Akkordeon schliesst den vorigen beim Öffnen des nächsten (max. 1 offen), alle Teilaufgaben und Lösungen rendern, keine `merror`, keine JS-Fehler. Noch **nicht** auf die übrigen Seiten ausgerollt — wartet auf deine Freigabe.

---

## 2026-06-06 · Phase 5.16 — Fix: MathJax-Delimiter auf 6 Seiten (Formeln rendern wieder vollständig)

Beim Prüfen aller Dokumente fiel auf, dass auf sechs Seiten Formeln nur teilweise/falsch gerendert wurden.

- **Ursache (Alt-Bug, nicht aus dem Hinweis-Rollout):** Im MathJax-Head-Config stand der Delimiter als JS-String `'\('` statt `'\\('`. JavaScript wertet `'\('` zu `'('` aus — MathJax behandelte dadurch **normale Klammern** als Inline-Mathe-Begrenzer statt `\(…\)`. Folge: echte `\(…\)`-Formeln wurden nur teils erkannt, Reste blieben als Rohtext stehen, vereinzelt landete ein `\(` in einer gerenderten `mtext`.
- **Betroffen:** p4-4, p5-1, p5-2, p5-3, p6-1, p6-2 (jeweils `inlineMath`/`displayMath` von `'\('`/`'\)'`/`'\['`/`'\]'` auf doppelt maskiert `'\\('` … korrigiert). p4-1/p4-2/p4-3/p4-5, alle Druckseiten, Glossar, Formelsammlung und TEMPLATE.html waren bereits korrekt.
- **Verifiziert** mit echtem MathJax (lokales `tex-svg`-Bundle, headless): nach dem Fix rendern alle sechs Seiten vollständig (z.B. p4-4 von 55 auf 250 gesetzte Ausdrücke), kein sichtbarer Rohtext, keine `merror`. Zusätzlich alle 4125 Formel-Spans aller Dokumente einzeln durch MathJax getestet — 0 Parser-Fehler.
- **Vorbeugung:** Checklistenpunkt in STYLEGUIDE §9 ergänzt (Delimiter doppelt maskieren, `grep`-Schnelltest).

---

## 2026-06-06 · Phase 5.15 — Animations-Hinweise zentralisiert, dokumentiert und auf alle Seiten ausgerollt

Nach Freigabe des p4-1-Prototyps (Phase 5.14) wurde das Muster vereinheitlicht und flächendeckend eingesetzt.

- **Zentralisiert:** Gestaltung von p4-1 nach `style.css` verschoben (neuer Abschnitt «Animations-Hinweise»), Logik in die neue gemeinsame Datei **`anim-hinweise.js`** ausgelagert (auf jeder Themenseite nach `physiklib.js` eingebunden). Die lokalen `<style>`-/`<script>`-Blöcke in p4-1 wurden entfernt; keine Duplizierung mehr pro Seite.
- **Dokumentiert:** STYLEGUIDE §5.6 (Struktur, Inhaltsregeln, Notation/Vorlesen, zentrale Dateien) und Verweis aus dem 13-Punkte-Master-Schema; HOWTO §2.2 (Skelett-Einbindung), §3.4 (Titelzeile-Hinweise) und §6.1 (Pre-Flight-Einbindungs-Check).
- **Ausgerollt:** Auf **allen 10 Themenseiten** trägt jede Animation in der Titelzeile «💡 Worauf achten?» und «✓ Erkenntnis» — animationsspezifisch (je 4–5 Aspekte), Anzeige in Projekt-Notation `\(…\)`, Vorlese-Klartext in `data-vorlesen`. Die bisherige Bedienungszeile unter dem Titel wurde dabei entfernt (Inhalt steht jetzt in «Worauf achten?»).
- Schweizer Hochdeutsch, Dezimalpunkt. Verifiziert via Playwright (Hinweise rendern, Rollover bleibt nach Klick offen, Vorleseknopf klickbar, balancierte `\(…\)`-Begrenzer, keine JS-Fehler).

---

## 2026-06-06 · Phase 5.14 — Prototyp: Animations-Hinweise mit Vorlese-Option (nur p4-1)

> Experimenteller Prototyp auf **ausschliesslich p4-1** zur Bewertung, bevor er ggf. auf weitere Seiten ausgerollt wird. Vollständig lokal in p4-1 gehalten (lokaler `<style>`- und `<script>`-Block), kein Eingriff in `style.css`, `nav.js` oder andere Seiten.

- Bei jeder der 6 Animationen stehen **direkt in der Titelzeile** (gleiche Zeile wie der Animationstitel) zwei Hinweis-Auslöser: nach dem Titel «💡 Worauf achten?», ganz rechts «✓ Erkenntnis». Beide öffnen ein Rollover bei Hover bzw. Tastatur-Fokus.
- Beide Hinweise führen **mehrere animationsspezifische Aspekte** als Liste auf (je 4–5 Punkte: Slider-Verhalten, Diagramm-Zusammenhänge, Grenzfälle, zugehörige Formeln) — in **Projekt-Notation** (MathJax/LaTeX, Dezimalpunkt, korrekte Symbole wie \(s_0\), \(v_0\), \(a_z\), \(\vec v\)).
- Die bisherige **Bedienungszeile unter dem Titel** wurde entfernt, da ihr Inhalt jetzt in «Worauf achten?» steht.
- **Vorlese-Schaltfläche** («🔊 vorlesen») je Hinweis auf Basis der Web Speech API (`speechSynthesis`, `lang="de-DE"`). Vorgelesen wird eine **separate Klartext-Fassung** (`data-vorlesen`), damit Formeln verständlich klingen statt als roher LaTeX-Code. Erneutes Klicken oder Escape stoppt; die Sprachausgabe läuft weiter, auch wenn das Rollover schliesst.
- **Erreichbarkeit des Knopfs gelöst:** unsichtbare Hover-Brücke zwischen Auslöser und Rollover plus **Klick fixiert das Rollover** (`.fixiert`), sodass der Vorleseknopf sicher anklickbar ist — auch auf Touchgeräten. Klick ausserhalb bzw. Escape schliesst wieder. Das rechte Rollover ist rechtsbündig.
- On-brand (Bernstein-Palette), Schweizer Hochdeutsch, Dezimalpunkt. Verifiziert via Playwright: Titel und beide Auslöser auf einer Zeile, «Erkenntnis» ganz rechts, alte Bedienungszeile entfernt, Widget-Bedienelemente intakt, Rollover bleibt nach Klick offen, Vorleseknopf klickbar, balancierte \(…\)-Begrenzer, keine JS-Fehler.

---

## 2026-06-06 · Phase 5.13 — Priorität-2-Politur (Lernziele, Kernpunkte, Verständnisfragen, Nachschlagewerk)

Umsetzung der Todo-Liste «Priorität 2» (#12–#20). Durchgehend Schweizer Hochdeutsch (kein ß, Dezimalpunkt).

- **#20 Zentrales Nachschlagewerk:** Zwei neue Seiten im Wurzelverzeichnis — `glossar.html` (rund 40 Kernbegriffe A–Z mit Sprungleiste, je Begriff/Formel/Definition/Querverweis) und `formelsammlung.html` (Konstanten + alle verifizierten Formeln nach LG4/5/6, jede mit Rücklink zur Themenseite). Im Header `nav.js` neues Pulldown **«Nachschlagen ▾»** neben «Themen» (Desktop + Mobile); der frühere externe Formelsammlung-Link wurde dadurch ersetzt. Themen-Button markiert sich nicht mehr fälschlich auf den Nachschlage-Seiten.
- **#18 Lernziele je Seite:** Auf allen 10 Themenseiten ein ausklappbarer `<details class="lernziele">`-Block vor dem Einstieg — als Verfeinerung der RLP-Kompetenzen in Ich-kann-Form.
- **#19 Zusammenfassungen angeglichen:** Jede Seite erhält in der Zusammenfassung eine `<ul class="kernpunkte">`-Liste mit 5–8 Kernpunkten (zwischen Zusammenfassungstabelle und Merksatz).
- **#16 Mehr Verständnisfragen:** Je Seite zwei ausklappbare «Was passiert, wenn …?»-Fragen (`<details class="frage">`) — eine im Theorieteil, eine vor den Aufgaben. Bewusst qualitativ formuliert.
- **Zentrale CSS-Komponenten** in `style.css` ergänzt: `.lernziele`/`.lz-body`, `.frage`/`.frage-antwort`, `.kernpunkte` sowie `.fs-link`, `.glossar-az`, `.glossar-eintrag` für die Nachschlage-Seiten. Keine erfundenen Klassen, native `<details>` (kein Konflikt mit `toggleL`).
- **Hilfsskripte:** `scripts/insert_p2.py` (idempotente Einfügung der drei Blocktypen an stabilen Ankern) und `scripts/fix_umlaute_p2.py` (Korrektur der Umlaute in den eingefügten Blöcken).
- **Verifikation:** Tag-Balance je Seite geprüft (div/details ausgeglichen), Playwright-Smoke-Test (Blöcke rendern und klappen auf, keine JS-Fehler), kein ß im gesamten Themenordner.
- **#12 Notation / #13 Einheiten / #15 Lösungen — Audit:** Alle Aufgabenbereiche maschinell gescannt. Notation durchgängig konsistent (DIN 1304). Einheiten-Scan ergab nur eine fehlende Einheit in einem Klammer-Rückverweis (p4-1, `v_0 = 13\;\text{m/s}` ergänzt). **40 berechnete Lösungsgleichungen numerisch in Python nachgerechnet — alle korrekt** (die 8 vom Skript «markierten» Fälle waren reine Einheiten-Präfix-Skalierungen J→kJ, Pa→kPa, N→kN bzw. %, bestätigt durch exakte Faktoren ×1000/×100). **#14 Formelkästen** sind durch die zentrale `formelsammlung.html` (einheitliche Formel-/Symbol-/Einheiten-Darstellung) abgedeckt; Seiten nutzen einheitlich `block-def`-Karten.

---

## 2026-06-06 · Phase 5.12 — Fachliche Präzisierungen (Wellen, Wärme, Wurfweite-Symbol)

- **p6-1 Wellen — Ausbreitungsgeschwindigkeit:** Aussage „hängt nur vom Medium ab" ersetzt durch korrektes „hängt vom **Wellentyp** und den **Eigenschaften des Mediums** ab (Dichte, Steifigkeit)"; im selben Medium können verschiedene Wellentypen unterschiedlich schnell sein. Frequenzunabhängigkeit nur noch bei gleichem Wellentyp/Medium formuliert. Auch im Merksatz korrigiert.
- **p6-1 Wellen — Wasserwellen:** nicht mehr als rein transversal dargestellt. „Wasserwelle" aus den Transversal-Beispielen entfernt; neuer Hinweis, dass Oberflächenteilchen näherungsweise auf **Kreis-/Ellipsenbahnen** laufen. Einstieg (Korken) entsprechend von „auf und ab" auf kreisförmige Bahn umformuliert; Einstieg-Animation explizit als idealisierte Transversalwelle (Seil) gekennzeichnet.
- **p5-2 Wärme — Wärme-Kraft-Kopplung:** WKK (und Wärmepumpe) nicht mehr als „erneuerbare Energiequelle" bezeichnet, sondern als **Technologie zur effizienteren Nutzung zugeführter Energie** (WKK nutzt Abwärme der Stromerzeugung mit). Im Handout parallel korrigiert.
- **p5-2 Wärme — Begriff Wärme:** Definition als **Prozessgrösse** (Energieübertragung aufgrund eines Temperaturunterschieds) geschärft; explizit abgegrenzt vom gespeicherten „Wärmevorrat" — ein Körper enthält innere Energie, nicht Wärme. Im Handout parallel.
- **p4-1 Kinematik — Symbol Wurfweite:** Symbol \(W\) (bzw. \(x_W\) in den Druckmaterialien) durchgängig auf \(s_x\) umgestellt — Formeln (A4-Aufgabe), Live-Box/Canvas-Label (sₓ) sowie Handout und Formelauszug. Interne Canvas-Breiten-Variable `cv.W` unverändert.

---

## 2026-06-06 · Phase 5.11 — Externe Ressourcen geprüft, alle «Verifikation ausstehend»-Hinweise entfernt

Alle 10 Themenseiten durchgegangen; jeder bislang gehedgte Link fachlich geprüft (Suche liefert Titel/Beschreibung/Datum der Videos; stabile Anbieter-Hubs zusätzlich abgerufen). Methodenhinweis: einzelne YouTube-Seiten liefern beim direkten Abruf 429 (rate-limited); die Prüfung erfolgte daher über die Suchergebnisse (realer Titel + Beschreibung = fachliche Bestätigung) und über abrufbare, stabile Anbieter-Themenseiten.

### Entfernte Hinweise / Korrekturen
- **p4-4 Statik:** Aufgaben-Karte „SwissEduc — Physik (Mechanik)" entfernt (generische Portalseite, keine belegbare Statik-Aufgabensammlung mit Lösungen). Es bleiben 3 verifizierte Aufgabenquellen (2× LEIFI + serlo).
- **p5-2 Wärme:** themenfremdes Video „Wirkungsgrad berechnen" (tatsächlich Lehrerschmidt *Elektrizität*) ersetzt durch 2 verifizierte Wärme-Videos: Lehrerschmidt-Themenseite „Wärmelehre" + „Was genau ist Wärme?" (Thermodynamik).
- **p5-3 Wärmeausdehnung:** verifiziertes Lehrerschmidt-Video „Wärmeausdehnung — thermische Ausdehnung berechnen" behalten; zweites verifiziertes Video (Feststoffe/Flüssigkeiten/Gase) ergänzt; Hinweis-Absatz entfernt.
- **p6-1 Wellen:** leere Video-Spalte mit 2 verifizierten Videos gefüllt („Grundbegriffe zu Wellen" + „Wellen — Periodendauer, Frequenz, Wellenlänge"); Hinweis-Absatz entfernt.
- **p6-2 Elektrizität:** verifizierte Lehrerschmidt-Themenseite „Elektrizität" behalten; verifiziertes Lehrerschmidt-Video „Ohmsches Gesetz mit Beispielen" ergänzt; Hinweis-Absatz entfernt.

### Geprüfte Anbieter (live + themengenau bestätigt)
Lehrerschmidt-Themenseiten Mechanik / Wärmelehre / Elektrizität; Fufaev (de.fufaev.org/mechanik); LEIFI mechanische Wellen; sowie Einzelvideos (musstewissen „Was ist Kraft?", Lehrerschmidt „Arbeit W=F·s" auf p4-3, Lehrerschmidt „Grad Celsius/Fahrenheit/Kelvin" auf p5-1).

### Offen / transparenter Vorbehalt
Die beiden musstewissen-**Playlists** (p4-2, p4-3) liessen sich als Playlist-IDs nicht einzeln per Abruf bestätigen (Kanal selbst ist verifiziert echt); sie sind nicht gehedgt und korrekt beschriftet. Stabile institutionelle Links (PhET, Walter Fendt, LEIFI, serlo) gelten als anbieterverifiziert. Auf Wunsch ist ein vertiefter Einzel-Audit dieser Restpunkte möglich.

---

## 2026-06-06 · Phase 5.10 — Status- und Dokumentationsabgleich nach Projektabschluss

### Geändert
- **`README.md`**: Status-Tabelle aktualisiert — alle 10 Teilgebiete auf «✅ fertig» (zuvor nur 4.1 fertig, Rest «📋 geplant»); Stand-Hinweis ergänzt, der den vollständigen Ausbau beschreibt
- **`HOWTO-neue-themenseite.md`**: veraltete Angaben ersetzt — Projektstand-Hinweis am Kopf (alle 10 RLP-Teilgebiete fertig; Anleitung gilt nun für zusätzliche/optionale Seiten); §4.1 nav.js-Beschreibung korrigiert (nav.js führt kein Status-Feld; Status lebt in `index.html`); §4.2 hartkodierte Zählung «fertig: 2 / geplant: 8» durch generische Anweisung + aktuellen Stand (10/0/0) ersetzt
- **`nav.js`**: «Ausblick»-Panel aktualisiert — «Erstellt» listet nun alle 10 Teilgebiete; «Geplant» auf optionale Erweiterungen (Magnetismus/Elektromagnetismus, Schwingungen) umgestellt (zuvor «Pilot 4.1 erstellt, Rest geplant»)

### Kontrolliert
- **`index.html`** bereits korrekt: Stats 10 fertig / 0 in Arbeit / 0 geplant, alle 10 Karten `.karte fertig`, alle Themen-Links auflösbar — keine Änderung nötig

---

## 2026-06-06 · Phase 5.9 — p6-2 Elektrizität vollständig: Zusatzmaterial + externe Ressourcen — **Projekt komplett (10/10 Themenseiten)**

### Hinzugefügt
- **5 Druckseiten/Materialien für `p6-2-elektrizitaet`** unter `downloads/themen/p6-2-elektrizitaet/`:
  - `handout.html` (Theorie: Ladung/Elementarladung/Coulomb, Strom \\\\(I=Q/t\\\\) und Spannung, ohmsches Gesetz \\\\(U=R\\,I\\\\) mit Leiterwiderstand \\\\(R=\\rho\\,l/A\\\\) und \\\\(\\rho\\\\)-Tabelle, Reihen-/Parallelschaltung-Tabelle, Leistung \\\\(P=U\\,I\\\\) und Energie in kWh, Gefahren des elektrischen Stroms; Merksatz)
  - `formelauszug.html` (Grössen/Symbole, Konstanten, alle Formeln, \\\\(\\rho\\\\)-Tabelle, Schaltungs-Tabelle, Merkpunkte, Merksatz)
  - `teste-dich-selbst.html` (12 Grundaufgaben mit steigender Schwierigkeit + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit TALS-Bezug: LED-Vorwiderstand, Überlandleitung, Solarmodul, Mehrfachsteckdose, Akkukapazität, Körperstrom, Heizdraht, gemischte Schaltung + Lösungen)
  - `ankideck.apkg` (**31 Karten**, erzeugt via `scripts/build_apkg_p6-2.py`; Deck `TALS Physik::6.2 Elektrizität`)
- **`scripts/build_apkg_p6-2.py`** — Anki-Build auf Basis von `build_apkg_p6-1.py` (gleiches Schema/CSS, neue Elektrizitäts-Karten)

### Geändert (`themen/p6-2-elektrizitaet.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`, Anki-Deck ohne)
- **Externe Ressourcen** (§13): Platzhalter durch dreispaltige Sektion ersetzt:
  - 🎬 Videos (1): Lehrerschmidt „Elektrizität\" (Themenseite per `web_fetch` als themengenau bestätigt). Für die übrigen Prioritätsanbieter (musstewissen Physik führt keine Elektrizitäts-Inhalte; Doc Schuster/Fufaev-Playlists per YouTube nicht titel-/inhaltsverifizierbar — 404 bzw. 429) transparenter «Verifikation ausstehend»-Hinweis gemäss HOWTO §5 statt Fehlzuordnung
  - 🧪 Simulationen (3): PhET „Stromkreis-Baukasten (DC)\" (`circuit-construction-kit-dc`, de), PhET „Ohmsches Gesetz\" (`ohms-law`, de), PhET „Widerstand in einem Draht\" (`resistance-in-a-wire`, de) — alle per `web_fetch` deutsch/HTML5 bestätigt
  - 📝 Aufgaben (4): LEIFI „Ohmsches Gesetz / Kennlinien\", LEIFI „Komplexere Schaltkreise\", LEIFI „Elektrische Energie\" (je mit Musterlösungen) und serlo „Elektrischer Widerstand und das ohmsche Gesetz\"

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie + Anki) vorab in Python geprüft (u.a. \\\\(Q=I\\,t\\\\), Coulomb \\\\(F=k\\,Q^2/r^2\\\\), \\\\(R=\\rho\\,l/A\\\\) für Cu/Al/Konstantan, Reihen-/Parallelwiderstand, \\\\(P=U\\,I\\\\), Energie in kWh)
- Externe Links per `web_search`/`web_fetch` geprüft (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`); 3 PhET-Sims + 4 Aufgabensammlungen bestätigt; Videos-Spalte mit ehrlichem Vermerk (HOWTO §5)
- Pre-Flight: 5 `dl`-Karten, 3 `ressourcen-subtitel`, Slots vid=1 sim=3 auf=4 (≤4 je Spalte), A1–A6 (6 `block-aufg`); `buildNav` 6.1 Wellen → (Ende), `next:null` korrekt; `#downloads`-Anker vorhanden; alle 5 Download-Dateien vorhanden; `<a>`/`</a>` balanciert (13/13); kein ß, keine echten Dezimalkommas (nur Font-URL); alle genutzten CSS-Klassen in `style.css`; Anki-Deck 31 Notes/31 Cards
- **Meilenstein: Alle 10 Themenseiten (p4-1 bis p6-2) vollständig ausgebaut** — je mit Animationen, Aufgaben, Zusammenfassung, Merksatz, 5 Druckseiten/Materialien und dreispaltiger Ressourcen-Sektion

---

## 2026-06-06 · Phase 5.8 — p6-1 Wellen vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p6-1-wellen`** unter `downloads/themen/p6-1-wellen/`:
  - `handout.html` (Theorie in 7 Abschnitten: von der Schwingung zur Welle, Wellengleichung \\(c = \\lambda\\,f\\), Transversal-/Longitudinalwellen, Schall in verschiedenen Medien, elektromagnetisches Spektrum, Lichterzeugung (Wärmestrahlung/atomare Emission/Laser), wellenlängenabhängige Absorption und Treibhauseffekt; Auf-einen-Blick-Tabelle + Merksatz)
  - `formelauszug.html` (Symbole, alle Formeln, Schallgeschwindigkeiten in Medien, EM-Spektrum-Bereiche, Merksatz)
  - `teste-dich-selbst.html` (12 Grundaufgaben in Gruppen + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit TALS-Bezug Technik/Architektur/Life Sciences: Echolot, UKW-Antenne, Mikrowelle, Fledermaus-Echoortung, Erdbeben-P/S-Wellen-Laufzeit, Laser-Wellenlänge u.a. + Lösungen)
  - `ankideck.apkg` (**31 Karten**, erzeugt via `scripts/build_apkg_p6-1.py`; Deck `TALS Physik::6.1 Wellen`)
- **`scripts/build_apkg_p6-1.py`** — Anki-Build auf Basis von `build_apkg_p5-3.py` (gleiches Schema/CSS, neue Wellen-Karten)

### Geändert (`themen/p6-1-wellen.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`, Anki-Deck ohne)
- **Externe Ressourcen** (§13): Platzhalter durch dreispaltige Sektion ersetzt:
  - 🎬 Videos: kein Link übernommen. Recherche durch die Prioritätsanbieter (musstewissen Physik, Lehrerschmidt, Doc Schuster, Alexander Fufaev) lieferte keine themengenaue Playlist, die sich zweifelsfrei dem jeweiligen Kanal über eine stabile URL zuordnen liess (in Videobeschreibungen verlinkte Playlist-URLs lösten auf Fremdkanäle um oder gaben 404; YouTube-Playlist-Seiten sind JS-gerendert und per `web_fetch` nicht titel-/inhaltsverifizierbar). Daher transparenter «Verifikation ausstehend»-Hinweis gemäss HOWTO §5 statt einer Fehlzuordnung
  - 🧪 Simulationen (3): PhET „Wellen auf einer Schnur" (`wave-on-a-string`, de), Walter Fendt „Elektromagnetische Welle" (per `web_fetch` als HTML5/deutsch bestätigt), Walter Fendt „Stehende Längswellen" (deutsch, HTML5)
  - 📝 Aufgaben (1): LEIFI „Mechanische Wellen — Aufgaben" (mit einblendbaren Musterlösungen)

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie + Anki) vorab in Python geprüft (u.a. Schall \\(\\lambda=0.77\\,\\text{m}\\), Echolot \\(d=300\\,\\text{m}\\), UKW \\(\\lambda=3.06\\,\\text{m}\\)/\\(\\lambda/4=0.77\\,\\text{m}\\), Mikrowelle \\(\\lambda=12.2\\,\\text{cm}\\), Fledermaus \\(29\\,\\text{ms}\\), Erdbeben \\(\\Delta t=8.75\\,\\text{s}\\), Laser \\(650\\,\\text{nm}\\to 4.6\\cdot10^{14}\\,\\text{Hz}\\))
- Externe Links per `web_search`/`web_fetch` geprüft (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`); Walter-Fendt-EM-Wellen-Sim per `web_fetch` bestätigt; Videos-Spalte nach mehreren Suchläufen bewusst leer mit ehrlichem Vermerk (HOWTO §5)
- Pre-Flight: 5 `dl`-Karten, 3 `ressourcen-subtitel`, Slots vid=0 sim=3 auf=1 (≤4), A1–A6 (6 `block-aufg`); `buildNav` 5.3 Wärmeausdehnung → 6.2 Elektrizität korrekt; alle 5 Download-Dateien vorhanden; HTML wohlgeformt; LaTeX-Delimiter balanciert; kein ß, keine echten Dezimalkommas (nur JS-Koordinaten/Font-URL); alle genutzten CSS-Klassen in `style.css`; Anki-Deck 31 Notes/31 Cards
- **Render-Check:** Playwright/Chromium-Download durch Sandbox-Netzwerkrestriktion blockiert → ersatzweise statische JS-Validierung: `node --check` für `physiklib.js`, `nav.js`, `downloads/diagram.js` und die Inline-Skripte von p6-1 alle fehlerfrei; alle aufgerufenen physiklib-Helfer (`initCanvas` 7×, `drawArrow` 3×, `fmtSig`) und lokalen Helfer (`makeLoop`/`tickFn`, `xOf`) sauber aufgelöst, keine undefinierten Referenzen

---

## 2026-06-06 · Phase 5.7 — p5-3 Wärmeausdehnung vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p5-3-waermeausdehnung`** unter `downloads/themen/p5-3-waermeausdehnung/`:
  - `handout.html` (Theorie: Ausdehnung im Teilchenbild, Längenausdehnung \\(\\Delta l = \\alpha\\,l_0\\,\\Delta T\\), Volumenausdehnung \\(\\Delta V = \\gamma\\,V_0\\,\\Delta T\\) mit \\(\\gamma \\approx 3\\alpha\\) für Festkörper, Dichteänderung \\(\\rho = \\rho_0/(1+\\gamma\\,\\Delta T)\\), Wasseranomalie bei 4 °C, Meeresspiegelanstieg \\(\\Delta h = \\gamma\\,h_0\\,\\Delta T\\), ideales Gasgesetz \\(pV/T=\\text{const}\\) mit Boyle-Mariotte/Amontons; Auf-einen-Blick-Tabelle + Merksatz)
  - `formelauszug.html` (Symbole, alle Formeln, Materialwerte \\(\\alpha\\)/\\(\\gamma\\), Kelvin-Umrechnung, Merksatz)
  - `teste-dich-selbst.html` (12 Grundaufgaben in 4 Gruppen: Begriffe, Längenausdehnung, Volumen/Dichte, Gasgesetz + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit TALS-Bezug Technik/Architektur/Life Sciences: Heizrohr, Alu-Profil, Ethanoltank, Meeresspiegel, Gasflasche, Tauchen, kombinierte Zustandsänderung, Frostsprengung + Lösungen)
  - `ankideck.apkg` (**31 Karten**, erzeugt via `scripts/build_apkg_p5-3.py`; Deck `TALS Physik::Thermodynamik::p5-3 Wärmeausdehnung`)
- **`scripts/build_apkg_p5-3.py`** — Anki-Build auf Basis von `build_apkg_p5-2.py` (gleiches Schema/CSS, neue Wärmeausdehnungs-Karten)

### Geändert (`themen/p5-3-waermeausdehnung.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`, Anki-Deck ohne)
- **Externe Ressourcen** (§13): Platzhalter durch kuratierte, web-verifizierte Karten in drei Spalten ersetzt:
  - 🎬 Videos (1 + Hinweis): Lehrerschmidt „Wärmeausdehnung — thermische Ausdehnung berechnen" (kanaleindeutiger Titel). YouTube-Watch-Seiten gaben durchgehend 429 (rate-limited) → Owner-Verifikation per `web_fetch` nicht möglich; daher nur Video mit kanaleindeutigem Titel übernommen, sonst ehrlicher „Verifikation ausstehend"-Hinweis für Wasseranomalie/Gasgesetz (HOWTO §5)
  - 🧪 Simulationen (3): PhET „Eigenschaften von Gasen", Walter Fendt „Zustandsänderungen eines idealen Gases" (per `web_fetch` als HTML5/deutsch/isobar-isochor-isotherm bestätigt), Walter Fendt „Teilchenbewegung in einem idealen Gas" (alle deutsch, HTML5)
  - 📝 Aufgaben (2): LEIFI „Ausdehnung bei Erwärmung", LEIFI „Allgemeines Gasgesetz" (beide mit Musterlösungen)

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie + Anki) vorab in Python geprüft (\\(\\alpha_\\text{Al}=23.8\\cdot10^{-6}\\), \\(\\alpha_\\text{Stahl}=12\\cdot10^{-6}\\), \\(\\gamma_\\text{Ethanol}=1.10\\cdot10^{-3}\\), Gasgesetz mit \\(T\\) in Kelvin und absolutem Druck)
- Externe Links per `web_search`/`web_fetch` geprüft (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`); Walter-Fendt-Gasprozess-Sim per `web_fetch` bestätigt; LEIFI-Aufgaben-Hubs suchergebnisbestätigt
- Pre-Flight §6.1: `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0 tog=6/ok`; §3.7: keine Duplicate-Marker, `<a class="lk">`-Bilanz 6/6, Slots vid=1 sim=3 auf=2 (≤4); §3.8 physiklib: ok; Inline-JS `node --check` OK; kein ß, keine echten Dezimalkommas in Inhalten (nur JS-Koordinaten/Font-URL); alle div-Tags in Druckseiten ausgeglichen; `buildNav` 5.2 → 5.3 → 6.1 korrekt; Anki-Deck 31 Notes/31 Cards

---

## 2026-06-06 · Phase 5.6 — p5-2 Wärme vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p5-2-waerme`** unter `downloads/themen/p5-2-waerme/`:
  - `handout.html` (Theorie: Wärme/innere Energie, spezifische Wärmekapazität \(Q=m\,c\,\Delta T\), Wärmebilanz/Mischtemperatur, latente Wärme, Leistung/Wirkungsgrad/Heizwert, drei Wärmetransportarten, Wärmepumpe/COP, Treibhauseffekt; Auf-einen-Blick-Tabelle + Merksatz)
  - `formelauszug.html` (Symbole, alle Formeln, Konstanten Wasser, Transportarten, Merksatz)
  - `teste-dich-selbst.html` (12 Grundaufgaben in 4 Gruppen + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit TALS-Bezug Technik/Architektur/Life Sciences + Lösungen)
  - `ankideck.apkg` (**35 Karten**, erzeugt via `scripts/build_apkg_p5-2.py`)
- **`scripts/build_apkg_p5-2.py`** — Anki-Build auf Basis von `build_apkg_p5-1.py` (gleiches Schema/CSS, neue Wärme-Karten; Deck `TALS Physik::Thermodynamik::p5-2 Wärme`)

### Geändert (`themen/p5-2-waerme.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt
- **Externe Ressourcen** (§13): Platzhalter durch kuratierte, web-verifizierte Karten in drei Spalten ersetzt:
  - 🎬 Videos (1 + Hinweis): Lehrerschmidt „Wirkungsgrad berechnen" (Kanal verifiziert). Bevorzugter Anbieterpool für die Kernthemen (spezifische Wärmekapazität, latente Wärme, Wärmetransport) auf BM-Niveau erschöpft: musstewissen ohne Wärmelehre (nur Mechanik), Lehrerschmidt ohne Kalorimetrie-Video (Klimaanlage-Video tot/404), Doc Schuster englischsprachig (AP Physics), Fufaev/universaldenker Uni-Niveau (molare Wärmekapazität, Freiheitsgrade) → ehrlicher „Verifikation ausstehend"-Hinweis statt falscher/toter Links (HOWTO §5)
  - 🧪 Simulationen (3): PhET „Energieformen und Energieumwandlungen", „Aggregatzustände (Grundbegriffe)", „Der Treibhauseffekt" (alle deutsch, HTML5)
  - 📝 Aufgaben (2): LEIFI „Innere Energie und Wärmekapazität" · Aufgabenübersicht, LEIFI „Spezifische Wärmekapazitäten" (beide mit Musterlösungen, live verifiziert)

### Geprüft
- Tag-Balance (div/ol/li/table/tr/td/a) ausgeglichen; kein ß; keine echten Dezimalkommata (nur JS-Code/Font-URL); alle 5 `dl-grid`-Links lösen auf; `.lk`/`.lk.sim`/`.lk.aufg` + alle §12/§13-Klassen in `style.css` vorhanden; Inline-JS `node --check` OK; `buildNav` 5.1 → 5.2 → 5.3 korrekt; Anki-Deck 35 Notes/35 Cards; alle Physik-Werte vorab in Python verifiziert

---

## 2026-06-06 · Phase 5.5 — p5-1 Temperatur vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p5-1-temperatur`** unter `downloads/themen/p5-1-temperatur/`:
  - `handout.html` (Theorie: Temperatur im Teilchenmodell, Brown'sche Bewegung, Aggregatzustände + Übergänge, Celsius-Skala, absoluter Nullpunkt + Kelvin-Skala, Umrechnung und Temperaturdifferenz, Zusammenfassung + Merksatz)
  - `formelauszug.html` (alle Formeln/Fixpunkte/Symbole auf einer Seite)
  - `teste-dich-selbst.html` (12 Grundaufgaben in 4 Gruppen + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit TALS-Bezug Technik/Architektur/Life Sciences, eine mit SVG-Skizze + Lösungen)
  - `ankideck.apkg` (**31 Karten**, erzeugt via `scripts/build_apkg_p5-1.py`)
- **`scripts/build_apkg_p5-1.py`** — Anki-Build auf Basis von `build_apkg_p4-4.py` (gleiches Schema/CSS, neue Temperatur-Karten; Deck `TALS Physik::Thermodynamik::p5-1 Temperatur`)

### Geändert (`themen/p5-1-temperatur.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`, Anki-Deck ohne)
- **Externe Ressourcen** (§13): Platzhalter durch kuratierte, web-verifizierte Karten in drei Spalten ersetzt:
  - 🎬 Videos (3): Lehrerschmidt „Grad Celsius, Grad Fahrenheit und Kelvin", „Aggregatzustände — fest, flüssig, gasförmig", „Thermometer" (alle über die offizielle lehrer-schmidt.de-Wärmelehre-Seite kanalbestätigt). musstewissen deckt Temperatur nicht ab (nur Mechanik/Optik); Phil's Physics ist DIY-Kanal („Breaking Lab"); Doc Schuster/Fufaev ohne sauber verifizierbare Temperatur-Playlist → Einzelvideo-Fallback (§2.1)
  - 🧪 Simulationen (3): PhET „Eigenschaften von Gasen", „Aggregatzustände (Grundlagen)", „Aggregatzustände" (alle deutsch, HTML5, ©2026). Walter Fendt ohne themenscharfe Temperatur-/Teilchen-Sim
  - 📝 Aufgaben (4): LEIFI „Temperatur und Teilchenmodell" · Aufgabenübersicht, LEIFI „Temperaturumrechnung" · Aufgaben, LEIFI „Bestimmung des absoluten Nullpunktes" (Gay-Lussac), serlo „Temperatur und Teilchenbewegung" (alle mit Lösungen)

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie + Anki) vorab in Python geprüft
- Externe Links per `web_search`/`web_fetch` geprüft (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`): PhET-Sims per `web_fetch` als deutsch/HTML5/aktuell bestätigt; LEIFI-Temperatur-Hub als kanonische Quelle (Celsius, absoluter Nullpunkt, Teilchenmodell, Umrechnung) per `web_fetch` verifiziert; Lehrerschmidt-Videos über Anbieter-Website kanalbestätigt (Watch-Seiten gaben 429)
- Pre-Flight: Skelett-Marker vollständig, Tag-Bilanz (div/ol/li/a) ausgeglichen, nur `style.css`-Klassen; §3.7: keine Duplicate-Marker, `<a class="lk">`-Bilanz 10/10, Slots vid=3 sim=3 auf=4 (≤4); JS-Inline-Script `node --check` OK; kein ß, keine Dezimalkommas in Inhalten

---

## 2026-06-06 · Phase 5 — p4-4 Statik vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p4-4-statik`** unter `downloads/themen/p4-4-statik/` (analog p4-2/p4-3):
  - `handout.html` (Theorie: Kraft als Vektor/Wirkungslinie, Komponenten, Resultierende, Drehmoment, Hebelgesetz, Gleichgewichtsbedingungen, Seil- und Auflagerkräfte, schiefe Ebene, Zusammenfassung + Merksatz)
  - `formelauszug.html` (alle Formeln auf einer Seite)
  - `teste-dich-selbst.html` (12 Grundaufgaben in 4 Gruppen + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit SVG-Skizzen + Lösungen)
  - `ankideck.apkg` (**31 Karten**, erzeugt via `scripts/build_apkg_p4-4.py`)
- **`scripts/build_apkg_p4-4.py`** — Anki-Build auf Basis von `build_apkg_p4-2.py` (gleiches Schema/CSS, neue Statik-Karten)

### Geändert (`themen/p4-4-statik.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`, Anki-Deck ohne)
- **Externe Ressourcen** (§13): Platzhalter durch kuratierte, web-verifizierte Karten in drei Spalten ersetzt:
  - 🎬 Videos (4): musstewissen Physik „Was ist Kraft?" und „Kräfteparallelogramm und Kräftegleichgewicht"; Lehrerschmidt „Kraftdiagramm" und „Hebelgesetz – einseitiger und zweiseitiger Hebel" (alle Kanal-bestätigt)
  - 🧪 Simulationen (4): PhET „Balanceakt" (Hebel/Drehmoment), Walter Fendt „Zerlegung einer Kraft", „Gesamtkraft mehrerer Kräfte", „Kräfte an der schiefen Ebene" (alle deutsch, HTML5)
  - 📝 Aufgaben (4): LEIFI „Kräfteaddition und -zerlegung" · Aufgaben, LEIFI „Einfache Maschinen (Hebel/Drehmoment)" · Aufgaben, serlo „Aufgaben zur Kraft" (alle mit Musterlösungen), SwissEduc Physik/Mechanik (Verifikation ausstehend, §5)

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie) vorab in Python geprüft
- Externe Links per `web_search`/`web_fetch` geprüft (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`): Videos auf die zwei erstgelisteten Kanäle (musstewissen, Lehrerschmidt) gestützt, da diese keine sauberen Themen-Playlists führen → Einzelvideo-Fallback (§2.1); Walter-Fendt-Sims decken Komponenten/Resultierende/schiefe Ebene direkt ab; SwissEduc als 4. Aufgaben-Slot mit §5-Vermerk, da keine themenscharfe Aufgaben-mit-Lösungen-Seite bestätigt
- Pre-Flight §3.6: `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0`; §3.7: keine Duplicate-Marker, Tag-Bilanz ausgeglichen, Slots vid=4 sim=4 auf=4 (≤4); §3.8: 6 Toggles + physiklib eingebunden
- Tag-Bilanz gesamt div 234/234, a 17/17, ol 10/10, li 33/33, table 2/2; `node --check` des Inline-Scripts ok; alle 5 Download-Ziele vorhanden
- Karten-Slots: dl=5; apkg-Test: 31 notes, Deck `TALS Physik::Mechanik::p4-4 Statik`
- Notation: kein ß, Dezimalpunkt statt Komma; alle verwendeten CSS-Klassen existieren in `style.css`

---

## 2026-06-06 · Phase 5 — p4-3 Energie vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p4-3-energie`** unter `downloads/themen/p4-3-energie/` (analog p4-2):
  - `handout.html` (Theorie: Arbeit/Hubarbeit, Energieformen, Energieerhaltung, Leistung, Wirkungsgrad, Zusammenfassung + Merksatz)
  - `formelauszug.html` (alle Formeln auf einer Seite, Spezialfälle und typische Werte)
  - `teste-dich-selbst.html` (12 Grundaufgaben + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit SVG-Skizzen + Lösungen)
  - `ankideck.apkg` (**26 Karten**, erzeugt via `scripts/build_apkg_p4-3.py`)
- **`scripts/build_apkg_p4-3.py`** — Anki-Build auf Basis von `build_apkg_p4-2.py` (gleiches Schema/CSS, neue Energie-Karten)

### Geändert (`themen/p4-3-energie.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`)
- **Externe Ressourcen** (§13): Überschrift auf den **dreispaltigen** Physik-Titel korrigiert („… Simulationen …"); Platzhalter durch kuratierte, web-verifizierte Karten ersetzt:
  - 🎬 Videos (3): musstewissen Physik (Kanal-**Playlist**, Owner per `web_fetch` bestätigt), Lehrerschmidt „Arbeit (W=F·s)" (**YouTube-Video**, Kanal UCy0Fx… bestätigt), Alexander Fufaev „Klassische Mechanik" (fufaev.org Lernhub)
  - 🧪 Simulationen (4): PhET „Energieskatepark", PhET „Energieformen und Energieumwandlungen", Walter Fendt „Fadenpendel", Walter Fendt „Federpendel" (alle deutsch, HTML5)
  - 📝 Aufgaben (2): LEIFI „Arbeit, Energie und Leistung" · Aufgaben, LEIFI „Energieerhaltung und -umwandlung" · Aufgaben (beide mit ausführlichen Musterlösungen)

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie) vorab in Python geprüft
- Externe Links per `web_search`/`web_fetch` **owner-verifiziert** (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`):
  - Erstentwurf-Korrekturen: musstewissen Einzelvideo → Kanal-Playlist (§2.1 „Playlists strikt bevorzugt"); Lehrerschmidt/Fufaev Anbieter-Websites → verifizierte YouTube-/Hub-Quellen; LEIFI-Grundwissen-Seite → echte `/aufgaben`-Seite; serlo-Karte entfernt (Artikel ohne Musterlösungen, §2.3)
  - Mehrere als „Fufaev/Doc Schuster" gelistete Playlists entpuppten sich per `web_fetch` als Dritt-Kompilationen (z.B. „Think Logic", „Skillz-By _CJ") und wurden verworfen; Doc Schuster (deutsch) und SwissEduc/abi-physik mangels sauber verifizierbarer Energie-Ressource übersprungen
- Pre-Flight: Tag-Bilanz div 188/188, ol 11/11, li 29/29; `bad=0`; `node --check` der 3 Inline-Scripts ok; alle 5 Download-Ziele vorhanden; Navigation p4-2 → p4-3 → p4-4 korrekt
- Karten-Slots: dl=5, Ressourcen vid=3 sim=4 auf=3; apkg-Test: 26 notes / 26 cards
- Notation: kein ß, Dezimalpunkt statt Komma (Komma-Treffer ausschliesslich in SVG-Koordinaten und Font-URL); alle verwendeten CSS-Klassen existieren in `style.css`

---

## 2026-06-06 · Phase 5 (Start) — p4-2 Dynamik vollständig: Zusatzmaterial + externe Ressourcen

### Hinzugefügt
- **5 Druckseiten/Materialien für `p4-2-dynamik`** unter `downloads/themen/p4-2-dynamik/` (analog p4-1/p4-5):
  - `handout.html` (Theorie: Kraft/Masse, drei Newtonsche Gesetze, Hooke, Reibung, schiefe Ebene, Atwood, Zusammenfassung + Merksatz)
  - `formelauszug.html` (alle Formeln auf einer Seite, inkl. typischer Reibungszahlen)
  - `teste-dich-selbst.html` (12 Grundaufgaben + Lösungen)
  - `aufgabenserie.html` (8 Anwendungsaufgaben mit SVG-Skizzen + Lösungen)
  - `ankideck.apkg` (**28 Karten**, erzeugt via `scripts/build_apkg_p4-2.py`)
- **`scripts/build_apkg_p4-2.py`** — Anki-Build auf Basis von `build_apkg_p4-5.py` (gleiches Schema/CSS, neue Karten)

### Geändert (`themen/p4-2-dynamik.html`)
- **Zusatzmaterial-Sektion** (§12): Platzhalter durch `dl-grid` mit den 5 Materialien ersetzt (Druckseiten `target="_blank"`)
- **Externe Ressourcen** (§13): Überschrift auf den **dreispaltigen** Physik-Titel korrigiert („… Simulationen …"); Platzhalter durch kuratierte, web-verifizierte Karten ersetzt:
  - 🎬 Videos (3): musstewissen Physik – Kräfte (Playlist, Owner per `web_fetch` bestätigt), Lehrerschmidt Mechanik, Alexander Fufaev Klassische Mechanik
  - 🧪 Simulationen (4): PhET „Grundlagen", PhET „Schiefe Ebene", Walter Fendt „Fahrbahnversuch 2. Newton", Walter Fendt „Schiefe Ebene" (alle deutsch, HTML5)
  - 📝 Aufgaben (4): LEIFI „Kraft und Bewegungsänderung", LEIFI „Kräfteaddition und -zerlegung", serlo „Kraft", SwissEduc Physik (alle mit Lösungen)

### Verifiziert
- Alle Aufgaben-Rechnungen (Teste-dich-selbst + Aufgabenserie) vorab in Python geprüft
- Externe Links per `web_search`/`web_fetch` bestätigt (Anbieter-Reihenfolge gemäss `HOWTO-externe-ressourcen.md`)
- Pre-Flight (§3.6): `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0`; Struktur (§3.7): keine Duplikat-Marker, `<a class="lk">`-Bilanz 11/11, Slots vid=3 sim=4 auf=4; physiklib (§3.8) ok
- Notation: kein ß, Dezimalpunkt statt Komma (Komma-Treffer ausschliesslich in SVG-Koordinaten und Font-URL); alle verwendeten CSS-Klassen existieren in `style.css` (keine Phantom-Klassen)

---

## 2026-06-05 · Phase 2.4 — Alle Themenseiten voll ausgebaut · p6-2 auditiert

### Geändert
- **Alle 8 Stubs zu vollwertigen Themenseiten ausgebaut** (je ~5–7 Animationen und 6 Aufgaben, analog p4-1/p4-5): `p4-2`, `p4-3`, `p4-4`, `p5-1`, `p5-2`, `p5-3`, `p6-1`, `p6-2`
- **`index.html`** — Status-Konsistenz hergestellt: alle 10 Karten auf `fertig`, Zähler auf **10 fertig / 0 geplant** (vorher fälschlich 2/8, obwohl die Seiten bereits ausgebaut waren)

### Behoben (Audit `p6-2-elektrizitaet.html`)
- **Coulomb-Gesetz ergänzt** (Grundbegriffe + Zusammenfassungstabelle): \(F=k\,Q_1Q_2/r^2\), \(k=8.99\cdot10^{9}\,\text{Nm}^2/\text{C}^2\) — schliesst die Abweichung zum Skript §18.1
- **Gefahren-Wording** an Skript S. 32 angeglichen: «Ströme über 500 mA …» statt «Schon 500 mA …»; FI-Auslösewert \(30\,\text{mA}\) ergänzt (Skript S. 34)
- **Leistung:** Effektivwert-Hinweis für \(P=U\cdot I\) bei Wechselstrom (nur ohmsche Verbraucher) ergänzt (Skript S. 19)
- **Animation 1:** `drawDot`-Aufruf auf das vorgesehene `g.cx`/`g.cy`-Muster umgestellt (vorher Identitäts-Funktionen)
- **Animation 6:** Slider-Beschriftungen mit Formelsymbolen \(I\) und \(t\) (Konsistenz mit übrigen Widgets)

### Verifiziert
- Alle Rechnungen (A1–A6, Animationen 1–6) gegen `8_PhysikBMElektrizität.pdf` geprüft — korrekt; Batterie-, Reihen-, Parallel- und Wirkungsgrad-Beispiele decken sich mit dem Skript
- IEC-Gefahrendiagramm (Animation 6) reproduziert die drei Lesebeispiele des Skripts (100 mA bei 25/250/500 ms → Bereich 2/3/4) exakt
- prev/next-Kette und nav.js-Dropdown unverändert lückenlos; `e=1.602\cdot10^{-19}` bewusst bei \(6.24\cdot10^{18}\) Elementarladungen/C belassen (intern konsistent, genauer als Skript-Rundung 6.25)

---

## 2026-05-31 · Phase 2.3 — Alle Themenseiten als reduzierte Stubs angelegt

### Hinzugefügt
- **8 reduzierte Themenseiten-Stubs** (analog Mathe-Schwerpunktfach), generiert via `scripts/gen_stubs.py`:
  - Lerngebiet 4: `p4-2-dynamik`, `p4-3-energie`, `p4-4-statik`
  - Lerngebiet 5: `p5-1-temperatur`, `p5-2-waerme`, `p5-3-waermeausdehnung`
  - Lerngebiet 6: `p6-1-wellen`, `p6-2-elektrizitaet`
  - Jeder Stub: Titel-Header, fachlich korrekte RLP-Kompetenzen (aus den BM-Skripten), Stub-Banner „In Vorbereitung", Abschnitts-Gerüst und vollständige `style.css`/`physiklib.js`/`nav.js`-Einbindung
- **`scripts/gen_stubs.py`** — Generator, der die Stubs aus einer zentralen Themen-Tabelle baut (konsistente prev/next-Verkettung)

### Behoben / Verifiziert
- **Alle Links funktionieren:** nav.js-Dropdown (10 URLs), Index-Karten (10), prev/next-Kette lückenlos p4-1 → … → p6-2 in beide Richtungen — alle Ziele existieren jetzt
- Index-Statuszähler stimmt: 2 fertig (p4-1, p4-5), 8 geplant (Stubs)
- Tag-Balance und Skelett-Marker aller 8 Stubs geprüft (div 8/8, page-wrap, main.content, buildNav, rlp-kompetenzen, stub-banner)

---

## 2026-05-31 · Phase 2.2 — Einheitlicher Aufgaben-Style (Angleichung an TALS-Mathematik)

### Geändert
- **`style.css`** — die Aufgaben-Komponenten der Mathe-Plattform übernommen, damit beide Fächer denselben Aufbau teilen (nur Bereichsfarbe unterscheidet sich):
  - Neue zentrale Klassen `aufg-nr-tag` (orange Pillen-Nummer), `aufg-titel-text`, `aufg-vertiefung`, `aufg-liste` (CSS-Counter-Nummerierung für Teilaufgaben)
  - Den gemeinsamen Animations-Widget-Block (`widget`, `sl-row`, `sl-vert`, `live-box`, `cv-wrap`, `typ-btn`, `play-btn`, `formel-live`, Spalten-Layouts) aus den einzelnen Themenseiten **zentralisiert** — verhindert künftige Divergenz zwischen Seiten
- **`themen/p4-5-hydrostatik.html`**, **`themen/p4-1-kinematik.html`** — alle Aufgaben A1–A6 auf das einheitliche `block-aufg`-Muster umgestellt:
  - Das alte `aw`/`aw-head`/`aw-nr`/`aw-titel`-Wrapper-System vollständig entfernt
  - Spiegelstrich-Titel `🟠 A4 — Anwendung` → Pillen-Titel `🟠 <span class="aufg-nr-tag">A4</span>…`
  - Teilaufgaben `teil-aufg`/`ta-lb` → `<ol class="aufg-liste">`; auch in den Lösungen `<strong>a)</strong>` → `aufg-liste`
  - Lokale CSS-Blöcke aus beiden Seiten entfernt (jetzt zentral); nur seitenspezifische Layouts (`einstieg-layout`, `a1-layout`) bleiben lokal
- **`TEMPLATE.html`** — Aufgaben-Beispiel und Style-Block auf den neuen Standard gebracht, damit neue Seiten konsistent starten

### Behoben
- Inkonsistenz innerhalb der Themenseiten: A1–A3 waren ohne `block-aufg`, A4–A6 mit doppeltem Wrapper und Spiegelstrich-Titel gerendert. Jetzt alle sechs identisch.

### Dokumentation
- **`STYLEGUIDE.md`** — neuer verbindlicher Abschnitt 5.5 „Aufgaben-Struktur" mit vollständigem Code-Muster; das alte `aw`-System und der Spiegelstrich-Titel sind als abgeschafft/verboten markiert. Master-Schema-Punkt 10 entsprechend korrigiert.

---

## 2026-05-17 · Phase 2.1 — Lesbare Achsenbeschriftungen in allen Diagrammen

### Geändert
- **`physiklib.js`** — `drawGrid` und `drawAxesUnits` überarbeitet:
  - Neue Helper `niceStep(range, pixels, targetPx)`: wählt Tick-Schritte aus `{1, 2, 5}·10ⁿ` so, dass ca. 65 px (x) bzw. 40 px (y) zwischen Labels bleiben — keine Mehrfach-Überdeckung mehr bei grossen Wertebereichen
  - Neue Helper `fmtTick(v, step)`: minimale sinnvolle Nachkomma-Stellen je nach Schritt (verhindert „0.30000000004")
  - `drawGrid` nutzt nun nice-ticks statt jedes Integer-Sprungs — bei z.B. `pMax ≈ 98 kPa` werden 20er-Schritte gewählt statt 98 Striche pro Pixel
  - Y-Tick-Labels werden bei knappem Platz links automatisch **rechts** der Y-Achse platziert (verhindert Abschneiden am linken Canvas-Rand)
  - X-Tick-Labels werden bei x-Achse am unteren Canvas-Rand automatisch **oberhalb** platziert
  - `drawAxesUnits` Overlay-Box ist nun bedarfsorientiert breit (`measureText(label)+8`) — verhindert Überdeckung benachbarter Tick-Werte

### Dokumentation
- **`STYLEGUIDE.md` §3.4 (neu)** — Beschreibung der Tick-Automatik, Best-Practice für Wertebereiche, Anti-Patterns
- **`STYLEGUIDE.md` §3.5 (neu)** — Umgang mit inhaltlichen Overlays (Wurfweiten-Marker etc.)
- **`HOWTO-neue-themenseite.md` §3.1** — Hinweis auf klugen Wertebereich (Reserve, passende Einheit)
- **`COLLABORATION.md` §3.9 (neu)** — Pre-Flight-Verfahren via Playwright-Screenshot, damit Achsen-Probleme bei neuen Themenseiten visuell verifiziert werden, bevor das ZIP gepackt wird
- **`COLLABORATION.md` §3.8** — `niceStep` und `fmtTick` zur Liste der reservierten Namen ergänzt

### Ergebnis
- Alle Plot-Animationen in p4-1 (Kinematik) und p4-5 (Hydrostatik) zeigen klar lesbare Achsen
- Keine API-Änderung — beide Themenseiten profitieren ohne Anpassung der Aufrufer
- Mit Playwright in 10 realen Wertebereichen verifiziert (s-t, v-t, a-t, Wurfparabel, Schweredruck Wasser/Hg, Auftrieb)
- Konventions-Dokumente halten die neuen Best-Practices für künftige Themenseiten fest

---

## 2026-05-17 · Phase 2 — p4-5 Hydrostatik (zweite Themenseite)

### Hinzugefügt
- **`themen/p4-5-hydrostatik.html`** — vollständige Themenseite nach 13-Punkte-Master-Schema mit 7 Canvas-Animationen:
  1. **Einstieg-Animation** (RAF, Play/Pause/Reset): Schwimmerin taucht in 5 s von 0 auf 3 m hinunter; Live-Anzeige von Tiefe, Schweredruck und Gesamtdruck — numerisch angenähert, weckt Interesse ohne Aufgabe zu lösen
  2. **Anim 1 Schweredruck**: Flüssigkeitssäule mit h/ρ-Slider, Material-Buttons (Wasser/Öl/Meerwasser/Hg), Manometer + p(h)-Diagramm
  3. **Anim 2 Hydrostatisches Paradoxon**: drei Gefässe (Zylinder, Trichter, umgekehrter Trichter) bei gleicher Füllhöhe, drei Manometer mit identischer Anzeige, Volumen-Vergleich
  4. **Anim 3 Hydraulische Presse**: F₁/A₁/A₂/s₁-Slider, Live-Werte für Druck, F₂, Hubverhältnis, s₂, Arbeit
  5. **Anim 4 Auftrieb**: Quader sinkt in Wasser, h_e- und Kanten-Slider, F_A(h_e)-Diagramm mit Knick bei „voll eingetaucht"
  6. **Anim 5 Schwimmen/Schweben/Sinken**: Würfel mit ρ_K-Slider, Material-Buttons (Kork/Eiche/Eis/Wasser/Alu), Kräftepfeile, Modus-Label
  7. **Anim 6 U-Rohr mit Öl und Wasser**: h_Öl- und ρ_Öl-Slider, Visualisierung der Spiegel-Differenz
- 6 Aufgaben A1-A6 (Werte ablesen → Aquarium → Hydraulische Hebebühne → Korkblock → Eisberg → U-Rohr) mit verifizierten Musterlösungen
- Druckseiten für p4-5 in `downloads/themen/p4-5-hydrostatik/`:
  - `handout.html` — vollständige Theorie auf A4
  - `formelauszug.html` — kompakte Formelsammlung mit Dichten-Tabelle
  - `teste-dich-selbst.html` — 12 Aufgaben mit Lösungen
  - `aufgabenserie.html` — 8 Anwendungs­aufgaben (U-Boot-Luke, Wasserturm, Hydraulische Hebebühne, Heissluftballon, Frachter-Beladung, Goldkrone des Hieron, Aräometer, Wassertank)
  - `ankideck.apkg` — 33 Anki-Karten (deterministisch generiert)
- `scripts/build_apkg_p4-5.py` — Anki-Build-Skript (basiert auf p4-1-Vorbild)

### Geändert
- `index.html`: p4-5-Karte von `karte geplant` auf `karte fertig`, Stats von „1 fertig / 9 geplant" auf „2 fertig / 8 geplant"
- `master-todoliste.md`: p4-5 als `[x]` markiert

### Offen
- Externe Ressourcen auf p4-5 via `web_fetch` verifizieren (12 Platzhalter-Links mit Vermerk „Verifikation ausstehend")
- prev-Link von p4-5 zeigt auf p4-4 Statik, das noch nicht existiert — funktioniert in nav.js (Reihenfolge bekannt), wird sichtbar sobald p4-4 vorhanden

---

## 2026-05-17 · Phase 1 — Komplettierung (Druckseiten + Anki + Dezimalpunkt-Konvention)

### Hinzugefügt
- Druckseiten für p4-1 in `downloads/themen/p4-1-kinematik/`:
  - `handout.html` — vollständige Theorie auf A4 nach 10-Punkte-Schema
  - `formelauszug.html` — kompakte Formelsammlung
  - `teste-dich-selbst.html` — 12 Aufgaben mit Lösungen (Selbstkontrolle)
  - `aufgabenserie.html` — 8 Anwendungs­aufgaben mit Skizzen + Musterlösungen
  - `ankideck.apkg` — 35 Anki-Karteikarten (deterministisch generiert)
- `downloads/print.css` — gespiegelt aus Mathe, Bereichsfarbe auf Bernstein umgestellt
- `downloads/diagram.js` — gespiegelt aus Mathe für statische Druckdiagramme
- `scripts/build_apkg_p4-1.py` — Anki-Build-Skript (basiert auf Mathe-Vorbild)
- `scripts/convert_decimals.py` — Konvertierungs-Skript (1:1 aus Mathe-Repo gespiegelt) für sichere Umstellung von Dezimalkomma → Dezimalpunkt

### Geändert
- **Dezimalpunkt** als Konvention bestätigt — identisch zur TALS-Mathe-Konvention (Schweizer Schul-Konvention). Die in einer früheren Iteration kurzzeitig erwogene Komma-Variante wurde verworfen, um Mathe und Physik einheitlich zu halten. 222 Stellen in 6 Dateien per Skript auf Punkt-Konvention zurückgestellt:
  - `themen/p4-1-kinematik.html` (66 Stellen)
  - `downloads/themen/p4-1-kinematik/{handout,formelauszug,teste-dich-selbst,aufgabenserie}.html` (153 Stellen)
  - `TEMPLATE.html` (3 Stellen)
  - Plus rgba-Schreibfehler in `TEMPLATE.html` (Box-Shadow) repariert
  - `physiklib.js` `fmt()`/`fmtS()`/`fmtSig()` zurück auf Punkt (kein `replace('.', ',')` mehr)
  - STYLEGUIDE §2.5, COLLABORATION §5: Konvention dokumentiert
- COLLABORATION §9 Anbieter-Liste auf Physik-Anbieter aktualisiert (musstewissen, Lehrerschmidt, Doc Schuster, Alexander Fufaev, Phil's Physics, MrWissen2go Physik · PhET, oPhysics, LEIFI, Walter Fendt · LEIFI-Aufgaben, SwissEduc, serlo Physik)
- Master-Todoliste: Phase 1 als abgeschlossen markiert, Skript-Dateinamen in Phasen 2-4 korrigiert

---

## 2026-05-17 · Phase 1 — Initiales Setup

### Hinzugefügt
- Repo-Gerüst: `index.html`, `style.css`, `nav.js`, `physiklib.js`
- Pilot-Themenseite `themen/p4-1-kinematik.html` mit 6 Canvas-Animationen:
  1. Geradlinig gleichförmige Bewegung (s-t und v-t gekoppelt)
  2. Gleichmässig beschleunigte Bewegung (a-t, v-t, s-t Triplet mit Live-Box)
  3. Freier Fall — RAF-animierte Apfel-Fallszene mit Stoppuhr
  4. Schiefer Wurf — Bahnkurve mit Vektorzerlegung
  5. Gleichförmige Kreisbewegung — RAF-Animation, v-Tangente + a_z-Pfeil
  6. Schwimmer im Fluss — Vektoraddition
- 6 Aufgaben A1-A6 nach Stufenkonzept
- Infrastruktur: `README.md`, `STYLEGUIDE.md`, `COLLABORATION.md`, `HOWTO-externe-ressourcen.md`, `HOWTO-neue-themenseite.md`, `master-todoliste.md`, `TEMPLATE.html`, `CHANGELOG.md`
- Bereichsfarbe Bernstein (`#8a4a0e`) als visuelles Pendant zu Mathe-Blau
- Dreispaltige Sektion 10: Videos · Simulationen · Aufgaben
- Klasse `.block-experiment` für Phänomen-Blöcke (Bernstein-Hintergrund)

### Offen für Phase 2
- Externe Ressourcen auf p4-1 via web_fetch verifizieren (12 Platzhalter-Links in Sektion 10 mit Vermerk „Verifikation ausstehend")
- Folge-Themenseiten ab p4-2 Dynamik

### Quellen
- Geforkt aus TALS Mathematik v1.8 (siehe github.com/go4exercises/tals-mathe)
- RLP-BM 2030 Ziff. 7.5.4.1, Gruppe 1
- Physik-Skript (im Project-Knowledge) als Vollständigkeits-Steinbruch
