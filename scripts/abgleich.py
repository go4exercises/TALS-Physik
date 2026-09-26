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
    'scripts/build-clip-ton.py': 0.575,
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
    '.claude/skills/preflight/preflight.py': 0.760,
    '.claude/skills/preflight/SKILL.md': 0.659,
    '.claude/settings.json': 0.509,
}

# Was tief unter seiner Grundlinie liegt, ist kein Naturgesetz, sondern eine
# offene Baustelle. Hier steht, was daran zu tun waere.
BAUSTELLE = {
    'scripts/build-seo.py':
        'Grosse Teile sind Projektdatei (SEITEN, Lerngebiete). Die Logik ist seit '
        'dem 13.09.2026 gleich (argparse, --dry-run, einsetzen, main). Trennen '
        'waere der naechste Schritt.',
    'scripts/build-clip-ton.py':
        'Mathe kann Klangkurve, Zweitstimme und Tempo; Physik nicht. Kein Fach-'
        'unterschied, nur Rueckstand.',
    '.claude/skills/preflight/preflight.py':
        'Neun Pruefungen geteilt (check_html_in_math seit 13.09.2026 in beiden). '
        'Offen: check_clips nur in Mathe.',
    '.claude/settings.json':
        'Erlaubnislisten verschieden lang. Die deny-Listen sind seit dem '
        '13.09.2026 deckungsgleich; das ist der Teil, auf den es ankommt.',
}

# Offene Uebertraege. 'quelle' ist das Repo, in dem die bessere Fassung
# liegt; abgearbeitet wird im jeweils anderen. Wer einen Eintrag erledigt,
# streicht ihn hier und uebernimmt die Datei ins eigene Repo.
OFFEN = [
    dict(quelle='Mathe', was='scripts/build-clip-ton.py',
         wie='Mathe kann Klangkurve, Zweitstimme, Tempo und Rausch-Parameter '
             '(342 Zeilen gegen 155). Kein Fachunterschied, nur Rueckstand.'),
    dict(quelle='Mathe', was='check_clips im Pre-Flight',
         wie='Gibt es nur in Mathe.'),
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
