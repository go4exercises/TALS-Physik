#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  TALS — Abgleich der beiden Schwesterrepos
#
#  Physik und Mathe teilen rund 5200 Zeilen Werkzeug: Build-Skripte,
#  Pruefer, suche.js, das Druck-CSS. Gepflegt wird es zweimal, und es
#  laeuft darum auseinander. Beispiele aus dem September 2026:
#
#    - build-seo.py: `noindex=True` setzte in Physik keine Robots-Marke,
#      in Mathe schon. Eine so markierte Seite blieb indexierbar.
#    - build-suchindex.py: Mathe hing ein Feature zurueck — 213 Eintraege
#      fuer 162 Clips, jeder Treffer auf eine Lektionsseite statt auf den Clip.
#    - preflight.py: check_html_in_math gab es nur in Physik, check_clips
#      nur in Mathe. Jedes Repo hatte ein Gatter, das dem anderen fehlte.
#
#  Dieses Skript verhindert die Drift nicht — es macht sie sichtbar, am Tag
#  ihrer Entstehung statt Monate spaeter. Es schreibt nie etwas.
#
#  Aufruf (vom Repo-Root):
#      python3 scripts/abgleich.py                 # Bericht
#      python3 scripts/abgleich.py --check         # Exit 1 bei neuer Drift
#      python3 scripts/abgleich.py --diff DATEI    # die Unterschiede selbst
#      python3 scripts/abgleich.py --gegen PFAD    # anderes Schwesterrepo
#
#  Fehlt das Schwesterrepo, endet das Skript mit Exit 0 und einem Hinweis.
#  Es darf nie der Grund sein, dass ein Pre-Flight scheitert.
#
#  DIE DREI KLASSEN
#
#  GLEICH   Fremdgut und echte Gemeingueter. Jeder Unterschied ist ein
#           Befund — hier gibt es nichts zu spezialisieren.
#  KERN     Geteiltes Werkzeug mit projekteigenen Konstanten. Verglichen
#           wird gegen die GRUNDLINIE unten: den Stand vom 13.09.2026.
#           Faellt die Aehnlichkeit darunter, ist neue Drift entstanden.
#           Die Grundlinie darf nur steigen — wer zwei Fassungen angleicht,
#           traegt den neuen, hoeheren Wert ein.
#  FACH     Bewusst verschieden, mit Begruendung. Wird nicht verglichen;
#           die Liste ist die Stelle, an der die Begruendung steht.
#
#  DIE WARTESCHLANGE (OFFEN)
#
#  Beide Repos duerfen einander nur LESEN, nie beschreiben (CLAUDE.md,
#  Abschnitt «Schwesterprojekt»). Ein Uebertrag braucht darum einen Kanal,
#  den beide Seiten sehen — und das ist diese Datei: Sie liegt in beiden
#  Repos und steht in ihrer eigenen KERN-Liste mit Grundlinie 1.000.
#
#  Daraus folgt der Mechanismus: Wer hier einen OFFEN-Eintrag hinzufuegt,
#  macht die Datei ungleich. Das Schwesterrepo meldet beim naechsten
#  Pre-Flight `[WARN] abgleich`, und `--diff scripts/abgleich.py` zeigt den
#  neuen Eintrag. Die dortige Sitzung arbeitet ihn ab, streicht ihn und
#  uebernimmt diese Datei — alles Schreiben bleibt im eigenen Repo.
#
#  Eine Notiz in einer lokalen Datei taugt dafuer nicht: Sie ist
#  ausgeschlossen, reist nicht mit, und die andere Seite weiss nichts von
#  ihr. Genau daran ist der erste Versuch am 13.09.2026 gescheitert.
# ─────────────────────────────────────────────────────────────

import argparse
import difflib
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GLEICH_PRAEFIX = ['vendor/', 'schriften/']
GLEICH = [
    'minicheck.js',
    'downloads/diagram.js',
    'autor.jpg',
    'clips/themes/heft.json',
    'clips/themes/papier.json',
    'clips/themes/tafel.json',
]

# Stand 13.09.2026. Nur nach oben korrigieren.
GRUNDLINIE = {
    'scripts/abgleich.py': 1.000,   # Traeger der Warteschlange — muss gleich sein
    'suche.js': 0.982,
    'anim-hinweise.js': 0.923,
    'schriften.css': 0.773,
    'package.json': 0.880,
    '.gitignore': 0.740,
    'downloads/print.css': 0.900,
    'feedback.html': 0.977,
    'LICENSE': 0.955,
    'scripts/build-suchindex.py': 0.962,
    'scripts/build-clips.py': 0.782,
    'scripts/build-clips-einbau.py': 0.806,
    'scripts/build-clip-ton.py': 0.575,   # zurueck auf 1.000, sobald Mathe OFFEN abgearbeitet hat
    'scripts/build-seo.py': 0.520,
    'scripts/schriften-lokal.py': 0.961,
    'scripts/mathjax-lokal.py': 0.853,
    'scripts/verify_mathjax.js': 0.941,
    'scripts/verify_js_runtime.js': 0.942,
    'scripts/check_identifier_collisions.py': 0.940,
    '.claude/tools/pruef-mathjax.mjs': 0.962,
    '.claude/tools/pruef-clip.mjs': 0.880,
    '.claude/tools/scan-live.mjs': 0.761,
    '.claude/tools/render-check.mjs': 0.968,
    '.claude/tools/build-bilder.mjs': 0.753,
    '.claude/skills/preflight/preflight.py': 0.849,
    '.claude/skills/preflight/SKILL.md': 0.659,
    '.claude/settings.json': 0.509,
}

# Was tief unter seiner Grundlinie liegt, ist kein Naturgesetz, sondern eine
# offene Baustelle. Hier steht, was daran zu tun waere.
BAUSTELLE = {
    'scripts/build-clip-ton.py':
        'Physik ist die Fassung ohne Zweitstimme; Mathe traegt die Mechanik noch, '
        'obwohl seit dem 07.09.2026 keine Spur sie nutzt. Rueckbau: siehe OFFEN.',
    'scripts/build-seo.py':
        'Grosse Teile sind Projektdatei (SEITEN, Lerngebiete). Die Logik ist seit '
        'dem 13.09.2026 gleich (argparse, --dry-run, einsetzen, main). Trennen '
        'waere der naechste Schritt.',
    '.claude/skills/preflight/preflight.py':
        'Alle Pruefungen geteilt (check_html_in_math seit 13.09.2026, '
        'check_clips seit 26.09.2026 in beiden). Verschieden bleiben Ordner und '
        'Bibliotheksname, dazu Einzelheiten: Slot-Limits nur in Physik, '
        'Skelett-Ausnahmen (EIGENES_SKELETT) nur in Mathe.',
    '.claude/settings.json':
        'Erlaubnislisten verschieden lang. Die deny-Listen sind seit dem '
        '13.09.2026 deckungsgleich; das ist der Teil, auf den es ankommt.',
}

# Offene Uebertraege. 'quelle' ist das Repo, in dem die bessere Fassung
# liegt; abgearbeitet wird im jeweils anderen. Wer einen Eintrag erledigt,
# streicht ihn hier und uebernimmt die Datei ins eigene Repo.
OFFEN = [
    dict(quelle='Physik', was='Regel «Eine Rechnung, eine Zeile» (Entscheid Auftraggeber 26.09.2026)',
         wie='Formelzeichen = Formel = Zahlen (mit Einheiten) = Ergebnis als EINE Kette in einer '
             '.fl-eq statt Formel- und Zahlenzeile untereinander; fehlt der Platz, Umbruch nur vor '
             'einem «=». Quelle Physik: STYLEGUIDE §2.8 (Absatz «Eine Rechnung, eine Zeile»), '
             'CLAUDE.md Stilcheck-Regel 9, physiklib.js flTex/flHtml/flTeil (Z. 95-130; Glieder '
             'als Inline-Formeln mit \\displaystyle, dazwischen <wbr>, fuehrendes = mit {}, '
             'Container inline-block, Frame-Drosselung + serielle Typeset-Kette). Commits '
             'f8c108d, ff768a1. Stand Mathe (gezaehlt 26.09.2026): 34 Seiten mit 147 .fl-eq; '
             'nur 5 statisch LaTeX, 83 per innerHTML + mjTypeset (20 Seiten) — dort sitzt das '
             'Zusammenlegen; mathlib.js hat mjTypeset, aber kein flTex. Typisches Paar: '
             's3-4a bk-eq (Formelzeile darueber, Zahlenzeile darunter). Sonderfaelle: '
             'farbige tx-gruen/tx-blau-Spans in g5-1 (wp-*-eq, sw-eq) muessen als \\color '
             'oder Fach-Ausnahme mit; reine Wertanzeigen (g5-1 wv-grad, py-min/py-c/py-max, '
             'zt-frage) sind keine Rechnung und bleiben. Nebenbefund Physik: LaTeX im Kopf '
             'einer ❓-Frage braucht <summary><span>…</span></summary>, sonst zerlegt der '
             'Flex-Container den Satz (Mathe-style.css pruefen). Falle beim Patchen: \\\\; in '
             'eingetippten Skripten kam als \\; an — Backslashes per chr(92) schreiben.'),
    dict(quelle='Physik', was='Zweitstimme zurueckbauen (Entscheid Auftraggeber 26.09.2026)',
         wie='Die Mechanik war fuer de_CH-kohler-medium gebaut; seit dem 07.09.2026 '
             'gibt es keine Kohler-Spur mehr (clips/ton: 0 Treffer), sie laeuft leer. '
             'Zu entfernen: (1) scripts/build-clip-ton.py — --zweitstimme, --modell2, '
             '--noise-scale, --noise-w, --klang, --tempo, mittleres_spektrum, '
             'klangkurve, klang_anwenden, Dehnung, Lautheitsangleichung, Beipackzettel; '
             'Ziel ist Physiks Fassung (155 Zeilen), danach 1:1 kopieren. Nebenbei weg: '
             'bei festem --tempo druckte der Szenen-Print dehnungen[-1] = Szenenindex '
             'als Faktor. (2) scripts/build-clips.py — STANDARDSTIMME (Z. 56-59), die '
             'Stimmenliste weitere/liste/stimmen_js (Z. 814-841), im Player STIMMEN, '
             'dehnung und der Umschalter (Z. 1218-1259); t * dehnung wird t. '
             '(3) HOWTO-clips.md — die vier Abschnitte «Zweite Stimme» bis «Wenn die '
             'Stimme dafuer zu schnell wird» (Z. 795-912); «Lizenzlage» bleibt. '
             '(4) Alle 203 Clips neu bauen — jede clips/*.html traegt den toten '
             'STIMMEN-Code. Danach in Physik die Grundlinie build-clip-ton wieder 1.000.'),
    dict(quelle='Physik', was='Clips zu einzelnen Animationen: bild, animation, Einbau (27.09.2026, optional)',
         wie='scripts/build-clips.py, element_html: neuer Zweig typ == "bild" (liest '
             'el["datei"] relativ zu CLIPS, prueft auf <svg, giesst die SVG ein; Klasse graf) '
             'und "bild" in den beiden Ausnahmelisten ("graf", "bild", "strich") fuer die '
             'Breite. 12 Zeilen. Doku: HOWTO-clips.md, Tabelle Elementtypen + Absatz «bild». '
             'Anlass: Clip zu einer einzelnen Animation (p6-2-fi-stromvergleich), der deren '
             'Skizze zeigt. Seit 91bd722/586c637 dazu: bild nimmt JPG/PNG (data:-URL); '
             'Drehbuch-Feld animation (Anker des h3) wandert nach clips.json; '
             'build-clips-einbau.py setzt «▶ Clip» in die .widget-titelzeile (Marker '
             'CLIP-ANIM), eigene Gruppe auf der Lektionsseite, Zeilen cl-anim mit vorangestelltem '
             'Link «Anim» (a.cl-animlink neben dem Knopf); style.css .ah-clip-knopf/.cl-anim*; Werkzeug '
             '.claude/tools/aufnahme-anim.mjs. Ohne Uebernahme sinkt die KERN-Aehnlichkeit von build-clips.py '
             '(Physik 78.2 -> 78.0 %); Grundlinie dann auf 0.780 senken oder uebernehmen. ' 
             'FARBE (nachgeprueft 27.09.2026): style.css ist FACH — die Physik-Regeln .ah-clip-knopf, .cl-anim, .cl-anim .cl-clip/.cl-folge, .cl-animlink, .cl-animkopf '
             '(physik style.css Z. 911-916 und ab Z. 1292) NICHT kopieren, sondern in Mathes Farbe nachbauen: Sie '
             'benutzen var(--bernstein), --bernstein-hell, --bernstein-rand und #fcf1e1 — diese Variablen gibt es in '
             'Mathe nicht, die Regeln fielen still auf keine Farbe zurueck. In Mathes Clip-Liste sind Blau-Nuancen '
             '(Zeilen, --blau/--blau-hell), Lila (.cl-sp Schwerpunktfach) und Orange (.cl-tr) schon vergeben; die '
             'Animationsclips brauchen eine Farbe, die sich davon klar abhebt — Wahl beim Auftraggeber.'),
    dict(quelle='Physik', was='clipBuehne: Fokus in den Clip (Fehler, 27.09.2026)',
         wie='mathlib.js Z. 466 setzt den Fokus nach dem Oeffnen der Buehne auf .cb-zu. '
             'Folge: Pfeiltasten spulen nicht (sie gehen an die Seite), die Leertaste '
             'drueckt «Schliessen» statt zu pausieren. Physik-Fix physiklib.js clipBuehne '
             '(Commit 86d3071): iframe fokussieren, sofort und im load-Handler; dort '
             'zusaetzlich clipEscape per try an f.contentWindow.document haengen, sonst '
             'schliesst Escape nicht mehr (unter file:// verweigert — Knopf und Rand '
             'bleiben). Die Clips selbst brauchen keinen Neubau. Testfalle: python3 -m '
             'http.server kann keine Range-Anfragen, der Ton springt beim Spulen auf 0 — '
             'mit file:// oder auf GitHub Pages (206) pruefen.'),
    dict(quelle='Physik', was='build-clip-ton: Aussprache-Tabellen (27.09.2026)',
         wie='Physik ba888a2/8559cc9/02c0c1b: AUSSPRACHE (Wortstamm -> IPA als [[…]]), '
             'ABKUERZUNGEN (nur exakt als ganzes Wort), TAUSCH (reiner Worttausch), '
             'VORSILBEN; aussprache(text) wirkt nur auf den Text an Piper. Mathe: in '
             'sprich(...) an allen vier Aufrufstellen (Z. 182, 193, 199, 213) den Text '
             'durch aussprache(text) ersetzen — oder erst die Zweitstimme zurueckbauen '
             '(eigener OFFEN-Eintrag), dann bleibt eine Stelle. Nachgezaehlt 27.09.2026: '
             '9 von 204 Mathe-Drehbuechern betroffen — Pythagoras 7 (g5-2a-pythagoras, '
             'g5-3-cosinussatz, g5-4-spezialwinkel, g5-4-trig-pythagoras, s4-2b-…), '
             'achthundert 1 (trigo2-3-ballon-zwei-fehler), Megahertz 1 (g1-4-ti30x-ee-eng); '
             'danach diese 9 neu vertonen. Die Tabellen sind nach Hoerproben des '
             'Auftraggebers entschieden und gelten fuer Thorsten in beiden Repos. Fallen: '
             'Satzzeichen muss in die Klammer (sonst verschluckt, Wort klebt an), '
             'Wortgrenze/Vorsilbe noetig («Schlamperei»). Empfohlen: Mathes eigenes '
             'Vokabular mit denselben zwei Suchdurchgaengen pruefen (HOWTO-clips.md, '
             'Abschnitt Ton; Physik fand so «Zentripetalkraft» englisch gelesen) — '
             'Entscheid je Wort per Hoerprobe durch den Auftraggeber.'),
    dict(quelle='Physik', was='build-seo: tex_weg loest Brueche und LaTeX-Abstaende auf (Fehler in Mathe)',
         wie='Physik cac3db1: bruch_auf(x) loest \\frac/\\tfrac/\\dfrac{a}{b} zu a/b auf '
             '(von innen nach aussen), dazu \\, \\; \\: \\! -> Leerzeichen und ^\\circ -> °. '
             'In Mathe nachgewiesen (27.09.2026): grundlagen/g5-4-einheitskreis.html '
             'schreibt in teaches «sin(/π2-φ) = cos(φ)» statt «sin(π/2-φ)». Betroffen '
             'sind die rlp-kompetenzen von 4 Seiten: g5-4-einheitskreis (frac), '
             's1-3-logarithmen, s3-4a-exponentialfunktionen, s3-4b-logarithmusfunktionen '
             '(Abstaende). Uebernehmen: bruch_auf und die zwei re.sub-Zeilen in innen(); '
             'danach build-seo.py laufen lassen und die vier Beschreibungen ansehen. '
             'Die Drift von build-seo.py (50.9 % gegen Grundlinie 52 %) kommt sonst aus '
             'Projektdaten (SEITEN-Tabelle), nicht aus der Logik.'),
    dict(quelle='Physik', was='Clips auf der Themenseite vor das Zusatzmaterial (Entscheid Auftraggeber 27.09.2026)',
         wie='Physik b0079f0: der Clip-Block steht nach der Zusammenfassung und VOR dem Zusatzmaterial '
             '(<h2 id="downloads">), nicht mehr danach. Physik-Doku: STYLEGUIDE §4 Skelett-Zeile 11b, '
             'HOWTO-clips.md Abschnitt «Einbauen» (Markerpaar «nach der Zusammenfassung und vor dem '
             'Zusatzmaterial; ohne Zusatzmaterial direkt nach der Zusammenfassung»). build-clips-einbau.py '
             'blieb unveraendert — es schreibt nur zwischen die Marker; verschoben wird das Markerpaar '
             'selbst, samt Inhalt. Stand Mathe (gezaehlt 28.09.2026): 45 Seiten mit CLIPS-Markern '
             '(grundlagen/ und schwerpunkt/), auf ALLEN die Folge zusammenfassung -> downloads -> '
             'CLIPS -> ressourcen; alle 45 haben id="zusammenfassung" und id="downloads". Also: Block '
             '<!-- CLIPS:ANFANG ... CLIPS:ENDE --> je Seite ausschneiden und direkt vor <h2 id="downloads"> '
             'setzen (ein Skript, nicht 45 Edits), danach build-clips-einbau.py --schreiben (muss '
             '«aktuell» melden), build-suchindex.py, Pre-Flight. Fuenf Seiten haben den Block leer, ohne '
             '<h2 id="clips">: g5-2b-vierecke, s1-1-, s2-1-, s3-1-, s4-1-grundlagen; auch dort '
             'verschieben, damit ein spaeterer Clip gleich richtig steht. Doku in Mathe mitziehen: STYLEGUIDE §4 Seitenschema '
             '(Z. ~410: Clips als eigener Punkt zwischen 8. Zusammenfassung und 9. Zusatzmaterial '
             'nennen, dort fehlen sie bisher ganz) und HOWTO-clips.md «Schritt 3» (Z. ~456: heute '
             '«sinnvollerweise direkt vor <h2 id="ressourcen">»).'),
    dict(quelle='Physik', was='.gitignore: Wegwerfskripte ausschliessen (28.09.2026)',
         wie='Physik fuehrt vier Zeilen, Mathe keine davon: __*.mjs, __*.py (seit einem __sem.mjs, das '
             'von August bis September 2026 unter physik.begreifbar.ch lag) und neu .*.mjs, .*.py '
             '(Physik a1fc9d9, nach .k3.mjs aus b0079f0, entfernt in fcd55ca). Das Repo ist die '
             'Website — was dort liegt, wird ausgeliefert. Stand Mathe (gezaehlt 28.09.2026): '
             'keine solche Datei versioniert oder im Wurzelverzeichnis, die Regel ist also reine '
             'Vorsorge und aendert nichts am Bestand. Die vier Zeilen samt Kommentar aus Physiks '
             '.gitignore (Abschnitt «Wegwerf-Pruefskripte») uebernehmen; vorher mit git ls-files -ci '
             '--exclude-standard pruefen, dass keine versionierte Datei darunter faellt. Danach in '
             'Physik die KERN-Grundlinie fuer .gitignore neu messen und anheben (heute 0.740, '
             'Physik gemessen 71.8 %).'),
    dict(quelle='Physik', was='build-clip-ton: Aussprache-Tabellen vereinheitlicht (Entscheid Auftraggeber 28.09.2026)',
         wie='Ersetzt Mathes TODO-schwesterprojekt-Eintrag «Aussprache-Tabellen um Mathe-Woerter erweitert» '
             '(dort als erledigt markieren). Der Auftraggeber hat die Unterschiede in Saetzen aus BEIDEN Repos '
             'angehoert und je Wort einmal fuer beide entschieden. Physiks scripts/build-clip-ton.py ist jetzt '
             'Mathes Fassung mit genau diesen Aenderungen — danach 1:1 nach Mathe kopieren, die Datei ist dann '
             'gleich (KERN-Grundlinie in beiden Repos auf 1.000): (1) ENTFERNT, also ohne Lautschrift wie '
             'frueher: volumen, lineares/linearen/lineare/linear, erdbeschleunigung. (2) BLEIBT: sechstel, '
             'komponentenweise und alle uebrigen Mathe-Woerter (in Physik 0 Stellen, also ohne Wirkung dort). '
             '(3) NEU: ABKUERZUNGEN ("My", "mˈyː") — Reibungszahl, in Mathe 0 Stellen. (4) Kommentare: Kopf des '
             'Blocks «Nach Hoerproben 28.09.2026, in Saetzen aus beiden Repos», Liste «Nicht geaendert» um '
             'Mikrometer, Mikro, Volumen, linear, Erdbeschleunigung ergaenzt. In Mathe danach neu vertonen, '
             'was (1) trifft — nachgezaehlt 28.09.2026 (nur gelesen): volumen 11 Stellen in 5 Clips, linear-'
             'Familie 38 Stellen in 30 Clips, erdbeschleunigung 1 Stelle (g1-4-ti30x-konstanten); ermitteln '
             'mit aussprache(alt) != aussprache(neu) ueber alle Drehbuecher. In Physik neu vertont: '
             'p0-3-masse-gewicht (Sechstel), p4-4-kraefte-zerlegen (komponentenweise), vorher schon '
             'p4-2-anim-hang, p4-4-anim-ebene, p5-3-anim-gasgesetze (Tangens, My, Hyperbel). '
             'OFFEN: «Menue» (nur Mathe, 16 Stellen in 8 Clips) — Hoerprobe laeuft, Eintrag folgt.'),

]

FACH = {
    'nav.js': 'Seitenbaum und Lerngebiete — je Fach ein anderer.',
    'style.css': 'Leitfarbe Bernstein gegen Blau, eigene Bausteine je Fach.',
    'index.html': 'Startseite je Fach.',
    'glossar.html': 'Fachbegriffe.',
    'formelsammlung.html': 'Formeln.',
    'clips.html': 'Bibliothek; Mathe gruppiert nach Fach, Physik nach Lerngebiet.',
    'leitprogramme.html': 'Andere Leitprogramme.',
    'rechtliches.html': 'Nennt das jeweilige Angebot.',
    'CLAUDE.md': 'Projektregeln je Repo.',
    'STYLEGUIDE.md': 'Fachkonventionen.',
    'README.md': 'Projektbeschreibung.',
    'SETUP.md': 'Projektbeschreibung.',
    'HOWTO-clips.md': 'Zahlen und Beispiele je Fach.',
    'HOWTO-neue-themenseite.md': 'Seitenskelett je Fach.',
    'HOWTO-leitprogramme.md': 'Je Fach eigene Erfahrungen.',
    'HOWTO-externe-ressourcen.md': 'Andere Anbieter je Fach.',
    'clips/clips.json': 'generiert.',
    'clips/vorlage.json': 'Beispieldrehbuch je Fach.',
    'clips/themes/begreifbar.json': 'Leitfarbe je Fach.',
    'suchindex.js': 'generiert.',
    'sitemap.xml': 'generiert.',
    'robots.txt': 'generiert.',
    'favicon.svg': 'Fachzeichen.',
    'package-lock.json': 'erzeugt aus package.json.',
}


def geschwister(root, vorgabe=None):
    """Pfad zum anderen Repo. Erkannt wird es an seiner Canvas-Bibliothek."""
    if vorgabe:
        return os.path.abspath(vorgabe)
    hier = 'physiklib.js' if os.path.exists(os.path.join(root, 'physiklib.js')) else 'mathlib.js'
    dort = 'mathlib.js' if hier == 'physiklib.js' else 'physiklib.js'
    neben = os.path.dirname(root)
    for name in sorted(os.listdir(neben)):
        kandidat = os.path.join(neben, name)
        if kandidat != root and os.path.isdir(kandidat) \
                and os.path.exists(os.path.join(kandidat, dort)):
            return kandidat
    return None


def aehnlichkeit(a, b):
    """Zeilenweise. Binaerdateien: gleich oder nicht.

    Die Reihenfolge der beiden Seiten wird festgelegt, bevor gemessen wird:
    difflib.SequenceMatcher.ratio() ist NICHT symmetrisch (build-clips-einbau.py
    ergab 0.8083 in der einen und 0.8061 in der anderen Richtung). Ohne diese
    Festlegung misst jedes Repo einen anderen Wert, und eine Grundlinie, die
    hier passt, schlaegt drueben an.
    """
    a, b = sorted((os.path.abspath(a), os.path.abspath(b)))
    try:
        ta = open(a, encoding='utf-8').read().splitlines()
        tb = open(b, encoding='utf-8').read().splitlines()
    except (UnicodeDecodeError, ValueError):
        return 1.0 if open(a, 'rb').read() == open(b, 'rb').read() else 0.0
    if ta == tb:
        return 1.0
    return difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()


def umbruch(text, breite):
    """Fliesstext auf feste Breite, ohne Fremdmodul."""
    zeilen, zeile = [], ''
    for wort in text.split():
        if zeile and len(zeile) + 1 + len(wort) > breite:
            zeilen.append(zeile)
            zeile = wort
        else:
            zeile = (zeile + ' ' + wort).strip()
    if zeile:
        zeilen.append(zeile)
    return zeilen


def gleich_dateien(root, gegen):
    """GLEICH-Liste plus alles unter den Fremdgut-Praefixen, das es in
    beiden Repos gibt."""
    aus = list(GLEICH)
    for praefix in GLEICH_PRAEFIX:
        basis = os.path.join(root, praefix)
        if not os.path.isdir(basis):
            continue
        for ordner, _, dateien in os.walk(basis):
            for d in dateien:
                rel = os.path.relpath(os.path.join(ordner, d), root)
                if os.path.exists(os.path.join(gegen, rel)):
                    aus.append(rel)
    return sorted(set(aus))


def main(argv):
    ap = argparse.ArgumentParser(
        prog='abgleich.py',
        description='Vergleicht das geteilte Werkzeug mit dem Schwesterrepo. '
                    'Schreibt nie etwas.',
        epilog='Ohne Schalter wird berichtet.')
    ap.add_argument('--check', action='store_true',
                    help='Exit 1, wenn neue Drift entstanden ist (so ruft der Pre-Flight auf)')
    ap.add_argument('--diff', metavar='DATEI',
                    help='die Unterschiede einer Datei zeigen')
    ap.add_argument('--gegen', metavar='PFAD',
                    help='Pfad zum Schwesterrepo (Standard: daneben gesucht)')
    a = ap.parse_args(argv)

    gegen = geschwister(WURZEL, a.gegen)
    if not gegen or not os.path.isdir(gegen):
        print('Schwesterrepo nicht gefunden — Abgleich übersprungen.')
        return 0
    print(f'Abgleich: {os.path.basename(WURZEL)}  gegen  {os.path.basename(gegen)}')

    if a.diff:
        p, q = os.path.join(WURZEL, a.diff), os.path.join(gegen, a.diff)
        if not (os.path.isfile(p) and os.path.isfile(q)):
            print(f'  {a.diff}: fehlt auf einer Seite.')
            return 0
        for z in difflib.unified_diff(
                open(q, encoding='utf-8').read().splitlines(),
                open(p, encoding='utf-8').read().splitlines(),
                fromfile=f'{os.path.basename(gegen)}/{a.diff}',
                tofile=f'{os.path.basename(WURZEL)}/{a.diff}', lineterm='', n=2):
            print('  ' + z)
        return 0

    befunde = []

    # ── GLEICH ───────────────────────────────────────────────────────────
    gl = gleich_dateien(WURZEL, gegen)
    ungleich = [f for f in gl
                if os.path.isfile(os.path.join(WURZEL, f))
                and open(os.path.join(WURZEL, f), 'rb').read()
                != open(os.path.join(gegen, f), 'rb').read()]
    print(f'\nGLEICH   {len(gl)} Dateien (Fremdgut und Gemeingut)')
    if ungleich:
        for f in ungleich:
            print(f'   [DRIFT] {f} — muss Zeichen für Zeichen gleich sein')
            befunde.append(f)
    else:
        print('   alle deckungsgleich')

    # ── KERN ─────────────────────────────────────────────────────────────
    print(f'\nKERN     {len(GRUNDLINIE)} Dateien (geteiltes Werkzeug)')
    for f in sorted(GRUNDLINIE):
        p, q = os.path.join(WURZEL, f), os.path.join(gegen, f)
        if not os.path.isfile(p) or not os.path.isfile(q):
            wo = 'hier' if not os.path.isfile(p) else 'dort'
            print(f'   [DRIFT] {f:48s} fehlt {wo}')
            befunde.append(f)
            continue
        ist, soll = aehnlichkeit(p, q), GRUNDLINIE[f]
        if ist + 0.005 < soll:
            print(f'   [DRIFT] {f:48s} {ist*100:5.1f} %  (Grundlinie {soll*100:.0f} %)')
            befunde.append(f)
        elif ist > soll + 0.015:
            print(f'   [besser] {f:47s} {ist*100:5.1f} %  (Grundlinie {soll*100:.0f} % '
                  f'— bitte nachtragen)')
        else:
            print(f'            {f:47s} {ist*100:5.1f} %')

    offen = [f for f in BAUSTELLE if f in GRUNDLINIE and GRUNDLINIE[f] < 0.75]
    if offen:
        print(f'\n         offene Baustellen ({len(offen)}):')
        for f in sorted(offen):
            print(f'           {f}\n             {BAUSTELLE[f]}')

    # ── FACH ─────────────────────────────────────────────────────────────
    print(f'\nFACH     {len(FACH)} Dateien, bewusst verschieden — nicht verglichen')

    # ── OFFEN ────────────────────────────────────────────────────────────
    hier = 'Physik' if os.path.exists(os.path.join(WURZEL, 'physiklib.js')) else 'Mathe'
    meine = [e for e in OFFEN if e['quelle'] != hier]
    fremde = [e for e in OFFEN if e['quelle'] == hier]
    print(f'\nOFFEN    {len(OFFEN)} Überträge in der Warteschlange')
    if meine:
        print(f'         HIER ({hier}) abzuarbeiten — die bessere Fassung liegt drüben:')
        for e in meine:
            print(f'           · {e["was"]}')
            for z in umbruch(e['wie'], 74):
                print(f'             {z}')
    if fremde:
        print(f'         drüben abzuarbeiten (Quelle {hier}) — dort meldet der '
              f'Pre-Flight sie als Drift:')
        for e in fremde:
            print(f'           · {e["was"]}')

    if befunde:
        print(f'\nNEUE DRIFT in {len(befunde)} Datei(en). '
              f'Ansehen mit: python3 scripts/abgleich.py --diff <Datei>')
        if 'scripts/abgleich.py' in befunde:
            print('\n  Dieses Skript selbst ist gedriftet. Es traegt die Warteschlange —'
                  '\n  solange drueben die aeltere Fassung liegt, sieht die dortige Sitzung'
                  '\n  keinen der OFFEN-Eintraege. Der naechste Durchgang im Schwesterrepo'
                  '\n  kopiert darum ZUERST scripts/abgleich.py herueber (Schreiben im'
                  '\n  eigenen Repo, also erlaubt) und arbeitet dann die Liste ab.')
        return 1
    print('\nKeine neue Drift.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
