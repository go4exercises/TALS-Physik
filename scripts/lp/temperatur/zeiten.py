"""Legt die Bewegung des Thermometerfadens auf den Ton (nach der Vertonung, nach anker.py).

  python3 scripts/lp/temperatur/zeiten.py p5-1-lp-skalen …

Eine Figur mit "_bahn": [[Textstelle, Versatz s, Höhe], …] bekommt eine "bewegung" mit Stützpunkten zu den
Sprechzeiten dieser Textstellen (plus Versatz): der Faden steigt oder sinkt, während der Sprecher es sagt.
Ein Teil im graf (Strecke, Punkt, Text, Fläche, Figur) mit "_anker" bzw. "_aus_anker" bekommt "ein" bzw. "aus"
zur Sprechzeit dieser Textstelle (anker.py setzt nur ganze Elemente).
Die Sprechzeiten rechnet es wie scripts/lp/kinematik/anker.py (dort nur benutzt, nicht geändert):
Satzstücke eins zu eins auf die Tonstücke, wenn das Tempo stimmt, sonst anteilig. Wiederholbar.
"""
import json
import os
import re
import subprocess
import sys

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..') + os.sep


def zeiten(clip):
    out = subprocess.run(['python3', R + '.claude/tools/sprechzeiten.py', clip], capture_output=True, text=True).stdout
    z = {}
    for zeile in out.splitlines():
        m = re.match(r'^(\S.*?)\s+ab [\d.]+ s, dauer [\d.]+: (.*)$', zeile)
        if m:
            z[m.group(1).strip()] = [tuple(map(float, s.split('–'))) for s in m.group(2).split()]
    return z


def zeit_von(text, seg, stelle):
    i = text.find(stelle)
    assert i >= 0, stelle
    chunks = [c for c in re.split(r'(?<=[,.:;?!])\s+', text) if c.strip()]
    if len(chunks) == len(seg):
        tempo = [len(c) / max(0.2, b - a) for c, (a, b) in zip(chunks, seg)]
        mittel = sum(len(c) for c in chunks) / sum(max(0.2, b - a) for a, b in seg)
        if all(0.6 * mittel <= t <= 1.6 * mittel for t in tempo):
            pos = 0
            for c, (a, b) in zip(chunks, seg):
                if i < pos + len(c) + 1:
                    return a + (b - a) * max(0, i - pos) / len(c)
                pos += len(c) + 1
            return seg[-1][1]
    tot = sum(b - a for a, b in seg)
    ziel = i / len(text) * tot
    for a, b in seg:
        if ziel <= b - a:
            return a + ziel
        ziel -= b - a
    return seg[-1][1]


for clip in sys.argv[1:]:
    p = R + 'clips/' + clip + '.json'
    d = json.load(open(p, encoding='utf-8'))
    zt = zeiten(clip)
    for s in d['szenen']:
        for e in s['elemente']:
            for f in e.get('figuren', []):
                if '_bahn' not in f:
                    continue
                x0, x1, yb = f['punkte'][0][0], f['punkte'][1][0], f['punkte'][0][1]
                stuetz = []
                for stelle, versatz, h in f['_bahn']:
                    t = round(zeit_von(s['sprecher'], zt[s['name']], stelle) + versatz, 2)
                    stuetz.append([t, {'punkte': [[x0, yb], [x1, yb], [x1, h], [x0, h]]}])
                f['bewegung'] = stuetz
                print(clip, s['name'], [b[0] for b in stuetz])
            for art in ('strecken', 'punkte', 'texte', 'flaechen', 'figuren'):
                for t in e.get(art, []):
                    if '_anker' in t:
                        t['ein'] = round(max(0.05, zeit_von(s['sprecher'], zt[s['name']], t['_anker']) - 0.2), 2)
                    if '_aus_anker' in t:
                        t['aus'] = round(max(0.1, zeit_von(s['sprecher'], zt[s['name']], t['_aus_anker']) - 0.2), 2)
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
