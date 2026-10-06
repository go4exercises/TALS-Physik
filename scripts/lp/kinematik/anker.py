"""Setzt "ein" jedes Elements mit "_anker" auf den Beginn dieses Texts im Sprechertext
(Zeiten aus .claude/tools/sprechzeiten.py, nach der Vertonung). Aufruf: anker.py <clip> …"""
import os
import json, re, subprocess, sys

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..') + os.sep


def zeiten(clip):
    out = subprocess.run(['python3', R + '.claude/tools/sprechzeiten.py', clip], capture_output=True, text=True).stdout
    z = {}
    for zeile in out.splitlines():
        m = re.match(r'^(\S.*?)\s+ab [\d.]+ s, dauer [\d.]+: (.*)$', zeile)
        if m:
            z[m.group(1).strip()] = [tuple(map(float, s.split('–'))) for s in m.group(2).split()]
    return z


for clip in sys.argv[1:]:
    p = R + 'clips/' + clip + '.json'
    d = json.load(open(p))
    zt = zeiten(clip)
    for s in d['szenen']:
        els = [e for e in s['elemente'] if e.get('_anker')]
        if not els:
            continue
        seg, text = zt[s['name']], s['sprecher']
        chunks = [c for c in re.split(r'(?<=[,.:;?!])\s+', text) if c.strip()]

        def t_von(i):
            if len(chunks) == len(seg):
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
        for e in els:
            i = text.find(e['_anker'])
            assert i >= 0, (clip, s['name'], e['_anker'])
            alt = e.get('ein')
            e['ein'] = round(max(0.05 if e['typ'] in ('graf', 'bild') and i == 0 else 0.2, t_von(i) - 0.2), 1)
            print(f"{clip:26s} {s['name']:18s} {e['_anker'][:26]:26s} {alt} -> {e['ein']}  ({len(chunks)}/{len(seg)})")
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
