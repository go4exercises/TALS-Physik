"""Zustandsschienen in den Clips ohne y-Achse: Die Achse bei 0 °C liefe sonst mitten durch die Bänder.
Ersetzt die Achsen jedes Schienenbilds (graf mit xname «ϑ [°C]», Fenster y −1.5 bis 10) durch eine
eigene Temperaturachse unten. Wiederholbar.   python3 scripts/lp/temperatur/achse_baender.py <clip> …"""
import json, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
for c in sys.argv[1:]:
    d = json.load(open(R + c + '.json', encoding='utf-8'))
    n = 0
    for s in d['szenen']:
        for g in s['elemente']:
            if g.get('typ') != 'graf' or g.get('ybereich') != [-1.5, 10] or g.get('xname') != 'ϑ [°C]':
                continue
            x0, x1 = g['xbereich']
            ticks = [t for t, _ in g.get('xteilung', []) if t < 1e8]
            g['achsen'] = False; g['pfeile'] = False; g['xname'] = ''
            g['xteilung'] = [[1e9, '']]; g['yteilung'] = [[1e9, '']]
            st = g.setdefault('strecken', []); tx = g.setdefault('texte', [])
            st.insert(0, {'von': [x0, -0.6], 'bis': [x1, -0.6], 'farbe': 5, 'dicke': 3, 'pfeil': True})
            for t in ticks:
                st.insert(1, {'von': [t, -0.85], 'bis': [t, -0.35], 'farbe': 5, 'dicke': 3})
                tx.append({'bei': [t, -1.35], 'text': ('%g' % t).replace('-', '−'), 'farbe': 5, 'groesse': 22, 'anker': 'middle'})
            tx.append({'bei': [x1, -0.1], 'text': 'ϑ [°C]', 'farbe': 5, 'groesse': 24, 'anker': 'end'})
            n += 1
    json.dump(d, open(R + c + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(R + c + '.json', 'a').write('\n')
    print(c, n, 'Schienenbilder')
