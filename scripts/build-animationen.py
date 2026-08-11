#!/usr/bin/env python3
"""Nummeriert die Animationen der Themenseiten aus der Dokumentreihenfolge.

Gepflegt wird im Quelltext nur der **Anker**, nie die Nummer:

    <h3 id="anim-federdehnung">Animation 2 · Je-desto-Explorer — Federdehnung</h3>
    … <a class="anim-ref" href="#anim-federdehnung">Animation 2</a> …

Dieses Skript schreibt beide Nummern — die im Titel und die im Verweistext —
aus der Reihenfolge der `<h3>`-Titel neu. Wird eine Animation eingeschoben,
verschieben sich die Nummern in Titeln und Verweisen gemeinsam; der Anker
bleibt derselbe. Damit kann ein Einschub keine Textverweise mehr brechen.

Weil die Nummern als Text im HTML stehen bleiben, sehen Suchindex, SEO-Block
und der Ausdruck sie weiterhin — anders als bei einer Nummerierung zur Laufzeit.

Verweise über Seitengrenzen tragen den Dateinamen mit:

    <a class="anim-ref" href="p0-1-vorwissen-mathematik.html#anim-dreisatz">Animation 6</a>

Steht der Verweis innerhalb einer Link-Karte (`<a class="lk">`), verbietet sich
ein verschachteltes `<a>`; dort gilt dieselbe Konvention mit `<span>`:

    <span class="anim-ref" data-anim-ref="p0-2-vorwissen-physik.html#anim-praefix-leiter">Animation 8</span>

Aufruf:
    python3 scripts/build-animationen.py            # schreibt
    python3 scripts/build-animationen.py --check     # prüft nur, Exit 1 bei Abweichung
    python3 scripts/build-animationen.py --root PFAD # Schwesterprojekt
"""

import argparse
import os
import re
import sys

H3 = re.compile(r'<h3(?P<attr>[^>]*)>Animation\s+(?P<nr>\d+)\s*·\s*(?P<titel>.*?)</h3>')
REF = re.compile(
    r'<(?P<tag>a|span)(?P<vor>[^>]*?)\bclass="anim-ref"(?P<nach>[^>]*)>'
    r'(?P<text>.*?)</(?P=tag)>'
)
ZIEL = re.compile(r'(?:href|data-anim-ref)="(?P<ziel>[^"]*)"')
# Verweis im Fliesstext, der noch nicht als Anker geschrieben ist
ROH = re.compile(r'Animation(?:en)?\s+\d+')
SKRIPT = re.compile(r'<(script|style)\b.*?</\1>', re.S)


def seiten(root):
    ordner = os.path.join(root, 'themen')
    return [os.path.join(ordner, n) for n in sorted(os.listdir(ordner))
            if n.endswith('.html')]


def anker_aus_attr(attr):
    m = re.search(r'\bid="(anim-[^"]+)"', attr)
    return m.group(1) if m else None


def lies_animationen(root):
    """{dateiname: [(anker, nr, titel), …]} in Dokumentreihenfolge."""
    karte = {}
    for pfad in seiten(root):
        eintraege = []
        for i, m in enumerate(H3.finditer(open(pfad, encoding='utf-8').read()), 1):
            anker = anker_aus_attr(m.group('attr'))
            if anker:
                eintraege.append((anker, i, m.group('titel')))
        if eintraege:
            karte[os.path.basename(pfad)] = eintraege
    return karte


def nummer(karte, datei, anker):
    for a, nr, _ in karte.get(datei, []):
        if a == anker:
            return nr
    return None


def bearbeite(pfad, karte, fehler):
    datei = os.path.basename(pfad)
    src = open(pfad, encoding='utf-8').read()
    neu = src

    # 1) Titel: Nummer = Position in der Dokumentreihenfolge
    zaehler = [0]

    def titel_ersatz(m):
        zaehler[0] += 1
        n = zaehler[0]
        if not anker_aus_attr(m.group('attr')):
            fehler.append(f'{datei}: <h3>Animation {m.group("nr")} · …> hat keinen '
                          f'Anker (id="anim-…") — Nummer nicht wartbar')
        return f'<h3{m.group("attr")}>Animation {n} · {m.group("titel")}</h3>'

    neu = H3.sub(titel_ersatz, neu)

    # 2) Verweise: Text aus dem Anker nachziehen
    def ref_ersatz(m):
        ziel = ZIEL.search(m.group('vor') + m.group('nach'))
        if not ziel:
            fehler.append(f'{datei}: <{m.group("tag")} class="anim-ref"> ohne '
                          f'href/data-anim-ref')
            return m.group(0)
        wohin = ziel.group('ziel')
        zieldatei, _, anker = wohin.rpartition('#')
        zieldatei = os.path.basename(zieldatei) or datei
        n = nummer(karte, zieldatei, anker)
        if n is None:
            fehler.append(f'{datei}: Verweis auf «{wohin}» — dort gibt es keine '
                          f'Animation mit diesem Anker')
            return m.group(0)
        return (f'<{m.group("tag")}{m.group("vor")}class="anim-ref"'
                f'{m.group("nach")}>Animation {n}</{m.group("tag")}>')

    neu = REF.sub(ref_ersatz, neu)

    # 3) Nicht migrierte Verweise melden (Skript-/Style-Blöcke ausgenommen:
    #    dort ist kein Markup möglich, die Nummer steht nur im Kommentar)
    def leeren(m):
        return re.sub(r'[^\n]', ' ', m.group(0))

    fuer_rohsuche = neu
    for muster in (SKRIPT, H3, REF):
        fuer_rohsuche = muster.sub(leeren, fuer_rohsuche)
    for m in ROH.finditer(fuer_rohsuche):
        zeile = fuer_rohsuche.count('\n', 0, m.start()) + 1
        fehler.append(f'{datei}:{zeile}: «{m.group(0)}» steht als blosser Text — '
                      f'als <a class="anim-ref" href="#anim-…"> schreiben')

    return neu if neu != src else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='nur prüfen, nichts schreiben (Exit 1 bei Abweichung)')
    ap.add_argument('--root', default='.', help='Projektwurzel')
    args = ap.parse_args()

    karte = lies_animationen(args.root)
    fehler, geaendert = [], []
    for pfad in seiten(args.root):
        neu = bearbeite(pfad, karte, fehler)
        if neu is None:
            continue
        geaendert.append(os.path.basename(pfad))
        if not args.check:
            open(pfad, 'w', encoding='utf-8').write(neu)

    for f in fehler:
        print(f'[FEHLER] {f}')

    if args.check:
        if geaendert:
            print('[FEHLER] Animationsnummern veraltet in: ' + ', '.join(geaendert))
            print('         → python3 scripts/build-animationen.py')
        if not geaendert and not fehler:
            n = sum(len(v) for v in karte.values())
            print(f'Animationsnummern aktuell ({n} Animationen auf '
                  f'{len(karte)} Seiten).')
        return 1 if (geaendert or fehler) else 0

    if geaendert:
        print('Nummern neu gesetzt in: ' + ', '.join(geaendert))
    else:
        n = sum(len(v) for v in karte.values())
        print(f'Nichts zu tun — {n} Animationen auf {len(karte)} Seiten '
              f'bereits korrekt nummeriert.')
    return 1 if fehler else 0


if __name__ == '__main__':
    sys.exit(main())
