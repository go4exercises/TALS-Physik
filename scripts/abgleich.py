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
#           Projektdaten darin (Seitenlisten) laesst DATEN beim Messen weg.
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
    '.gitignore': 0.793,
    'downloads/print.css': 0.900,
    'feedback.html': 0.977,
    'LICENSE': 0.955,
    'scripts/build-suchindex.py': 0.957,   # ohne DATEN gemessen; 0.963 -> 0.957: Physik liest LP-Titel aus <title> (07.10.2026, auf Mathes Vorschlag)
    'scripts/build-clips.py': 0.998,   # gemeinsamer Bauer, drei Projektwerte (07.10.2026)
    'scripts/build-clips-einbau.py': 0.830,
    'scripts/build-clip-ton.py': 1.000,
    'scripts/build-seo.py': 0.898,         # ohne DATEN gemessen (07.10.2026; mit Daten 0.533)
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
    '.claude/skills/preflight/SKILL.md': 0.680,
    '.claude/settings.json': 0.509,
}

# Projektdaten in KERN-Dateien: Diese Python-Zuweisungen auf oberster Ebene
# werden auf BEIDEN Seiten weggelassen, bevor gemessen wird (seit 07.10.2026).
# Sie wachsen mit jeder neuen Seite und liessen die Aehnlichkeit sinken, ohne
# dass am Werkzeug etwas auseinanderlief — ein Fehlalarm, der jeden echten
# uebertoent. Fehlt ein Name auf einer Seite, wird dort nichts weggelassen.
# --diff zeigt weiterhin die ganze Datei.
DATEN = {
    'scripts/build-seo.py': ('SEITEN', 'LG_G', 'LG_S'),
    'scripts/build-suchindex.py': ('ZUSATZSEITEN', 'UNVERLINKT'),
}

# Was tief unter seiner Grundlinie liegt, ist kein Naturgesetz, sondern eine
# offene Baustelle. Hier steht, was daran zu tun waere.
BAUSTELLE = {
    'scripts/build-seo.py':
        'Die Projektdaten (SEITEN, Lerngebiete) misst DATEN seit dem 07.10.2026 nicht '
        'mehr mit. Was bleibt, ist bewusst: Mathe leitet Fach und Lerngebiet aus dem '
        'Dateinamen ab (fach_lg) und hat darum eine Brotkrume mehr.',
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
    dict(quelle='Physik', was='Mathes zwei Eintraege vom 08.10.2026 abgearbeitet (--szenen/--fragen, dritte Runde build-clips)',
         wie='build-clip-ton.py ganz uebernommen (100 %), build-clips.py ganz uebernommen mit KARO_OHNE_ACHSEN = False, '
             'TEXTBREITE_BEGRENZEN = True, Seitenname, "werkzeug" weiter weggelassen (99.8 %, Grundlinie bleibt 0.998); '
             '--fragen-Block in build-clip-fragen-ton.py. Stichprobe neu gebaut: 10 Clips ohne fragen byte-gleich, '
             '12 mit fragen nur im FRAGEN_JS verschieden (alle 12 dieselbe Aenderung), pruef-fragen gruen; der '
             'Rest baut beim naechsten Bau des jeweiligen Clips mit. HOWTO-clips: «Dritte Runde», --szenen, --fragen. '
             'In Mathe: diese Datei uebernehmen und die zwei Eintraege in TODO-schwesterprojekt.md loeschen.'),
    dict(quelle='Physik', was='build-clips.py: "gleichmaessig": true an bewegten Kurven (08.10.2026)',
         wie='Stuetzpunkte und "grenzen" einer bewegten Kurve linear statt mit Smoothstep ueberblenden (laufende '
             'Welle mit konstanter Geschwindigkeit, Leitprogramm Wellen 6.1). Neun Stellen: data-gleich im '
             'Kurven-Pfad, lin im Teil-Objekt, bewZustand(k, t, lin), kGrenzen, bewegeKurve, kmX (Laeufer/Marken '
             'mit bahn) und die Kreisbahn in bewegeTrig reichen T.lin durch. Ohne das Feld baut jeder Clip byte-gleich (geprueft an vier Clips mit bewegung). '
             'HOWTO-clips: Absatz «Gleichmaessig statt weich» nach «Bereich, der wandert». In Mathe: die Stellen '
             'aus python3 scripts/abgleich.py --diff scripts/build-clips.py uebernehmen, Grundlinie bleibt.'),
]
FACH = {
    'scripts/clips_bibliothek.py': 'Bibliothek in drei Spalten; Lerngebiete, Farben und REIHEN_VORN je Fach.',
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


def ohne_daten(zeilen, namen):
    """Zeilen ohne die Zuweisungen auf oberster Ebene an `namen` (DATEN)."""
    if not namen:
        return zeilen
    import ast
    try:
        baum = ast.parse('\n'.join(zeilen))
    except SyntaxError:
        return zeilen
    weg = set()
    for k in baum.body:
        ziele = k.targets if isinstance(k, ast.Assign) else [k.target] if isinstance(k, ast.AnnAssign) else []
        if any(isinstance(z, ast.Name) and z.id in namen for z in ziele):
            weg.update(range(k.lineno - 1, k.end_lineno))
    return [z for i, z in enumerate(zeilen) if i not in weg]


def aehnlichkeit(a, b, daten=()):
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
    ta, tb = ohne_daten(ta, daten), ohne_daten(tb, daten)
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
        ist, soll = aehnlichkeit(p, q, DATEN.get(f, ())), GRUNDLINIE[f]
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
