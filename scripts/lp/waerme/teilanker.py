"""Legt «ein» und «aus» von Teilen eines graf (Strecken, Flächen, Texte, Punkte, Kurven, Geraden) auf
den Sprechertext — die Ergänzung zu scripts/lp/kinematik/anker.py, das nur ganze Elemente verschiebt.

  python3 scripts/lp/waerme/teilanker.py <clip> …      (nach build-clip-ton.py, vor build-clips.py)

Ein Teil trägt "_ein": "<Textstelle>" und/oder "_aus": "<Textstelle>", dazu optional "_ein_versatz" /
"_aus_versatz" in Sekunden. Mit PIPER_MODELL (wie für build-clip-ton.py) kommt die Wortzeit aus einer
Neusynthese, per Abgleich auf die Tonspur übertragen (synthgeber, unten); dann setzt das Skript auch die Elemente mit «_anker» neu,
die anker.py nur anteilig nach Zeichen gelegt hat. Ohne PIPER_MODELL wie in anker.py (Zeiten aus
.claude/tools/sprechzeiten.py, Satzstücke eins zu eins oder anteilig). Gezeigt wird 0.1 s nach dem Wortbeginn (die Neusynthese trifft auf rund ±0.3 s). Bei einer Läufer-
"bahn" mit "_bahn": [["<Textstelle>", versatz, x], …] werden die Zeiten der Stützpunkte gesetzt.
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


def zeitgeber(seg, text):
    chunks = [c for c in re.split(r'(?<=[,.:;?!])\s+', text) if c.strip()]

    def stimmig():
        if len(chunks) != len(seg):
            return False
        tempo = [len(c) / max(0.2, b - a) for c, (a, b) in zip(chunks, seg)]
        mittel = sum(len(c) for c in chunks) / sum(max(0.2, b - a) for a, b in seg)
        return all(0.6 * mittel <= t <= 1.6 * mittel for t in tempo)
    eins = stimmig()

    def t_von(phrase):
        i = text.find(phrase)
        assert i >= 0, phrase
        if eins:
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
    return t_von


TEILE = ('strecken', 'flaechen', 'texte', 'punkte', 'kurven', 'geraden', 'figuren')

# ---- Wortzeit aus einer Neusynthese (genauer als anteilig nach Zeichen)
# Die Tonspur ist Piper; derselbe Text, neu gesprochen, hat fast dieselbe Zeitstruktur. Gesucht ist der
# Lautbeginn des Ankerworts: Ende des gesprochenen Satzanfangs davor, dann der nächste Laut der ganzen
# Synthese. Diese Zeit wird linear auf den Sprechbereich der echten Szene (erstes bis letztes Tonstück
# laut sprechzeiten.py) übertragen. Nachgemessen am 08.10.2026: anteilig nach Zeichen lagen Anker bis 1.6 s
# vor ihrem Wort, so innerhalb weniger Zehntelsekunden.
_ton = None
_cache = {}
_wav = {}


def _laut(text):
    global _ton
    import importlib.util
    import tempfile
    import numpy as np
    import soundfile as sf
    if _ton is None:
        spec = importlib.util.spec_from_file_location('bct', R + 'scripts/build-clip-ton.py')
        _ton = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_ton)
    if text in _cache:
        return _cache[text]
    with tempfile.TemporaryDirectory() as td:
        q, w = os.path.join(td, 't.txt'), os.path.join(td, 't.wav')
        open(q, 'w').write(_ton.aussprache(text))
        subprocess.run(['piper', '-m', os.environ['PIPER_MODELL'], '-i', q, '-f', w], capture_output=True, check=True)
        x, sr = sf.read(w, dtype='float32')
    if x.ndim > 1:
        x = x.mean(1)
    _wav[text] = (x, sr)
    fr = int(0.01 * sr)
    env = np.array([np.abs(x[k:k + fr]).max() for k in range(0, len(x) - fr, fr)])
    laut = env > 0.02 * env.max()
    _cache[text] = laut
    return laut


def _ton_synth(text):
    _laut(text)
    return _wav[text]


def _merkmale(x, sr):
    """log. Energie in 30 Frequenzbändern (80 Hz bis 7 kHz), Fenster 40 ms, Schritt 20 ms"""
    import numpy as np
    n, h = int(0.04 * sr), int(0.02 * sr)
    w = np.hanning(n)
    fr = np.array([x[k:k + n] * w for k in range(0, max(1, len(x) - n), h)])
    S = np.abs(np.fft.rfft(fr, axis=1))
    f = np.fft.rfftfreq(n, 1 / sr)
    r = np.geomspace(80, 7000, 31)
    B = np.stack([S[:, (f >= r[i]) & (f < r[i + 1])].sum(1) for i in range(30)], 1)
    return np.log(B + 1e-4)


def _dtw(A, B, offen=False):
    """kürzester Weg durch die Abstandsmatrix (Schritte rechts, unten, diagonal); gibt je Zeile von A
    die erste zugeordnete Spalte von B zurück"""
    import numpy as np
    n, m = len(A), len(B)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0
    for i in range(1, n + 1):
        c = np.sqrt(((B - A[i - 1]) ** 2).sum(1))          # Abstände zeilenweise: spart Speicher
        zeile = np.minimum(D[i - 1, 1:], D[i - 1, :-1]) + c
        cs = np.cumsum(c)
        D[i, 1:] = np.minimum.accumulate(zeile - cs) + cs
    if offen:                                          # Ende frei: bester Endpunkt je Länge
        return int(np.argmin(D[n, 1:] / np.arange(1, m + 1)))
    i, j, erste = n, m, {}
    while i > 0 and j > 0:
        erste[i - 1] = j - 1
        k = int(np.argmin([D[i - 1, j - 1], D[i - 1, j], D[i, j - 1]]))
        if k == 0:
            i, j = i - 1, j - 1
        elif k == 1:
            i -= 1
        else:
            j -= 1
    return erste


_audio = {}


def synthgeber(clip, name, text):
    """Wortzeit per Abgleich: Die Neusynthese der ganzen Szene wird mit der echten Tonspur der Szene
    zeitlich verzerrt abgeglichen (dynamische Zeitverzerrung über Bandenergien); der Lautbeginn des
    Ankerworts in der Neusynthese wird so in die Tonspur übertragen. Eine lineare Umrechnung über die
    ganze Szene lief in langen Szenen bis 1.8 s nach, eine stückweise nach Sprechpausen lag bis 5 s
    daneben (dritte Prüfung 08.10.2026)."""
    import importlib.util
    import numpy as np
    import soundfile as sf
    if clip not in _audio:
        spec = importlib.util.spec_from_file_location('bcl', R + 'scripts/build-clips.py')
        bcl = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bcl)
        d = json.load(open(R + 'clips/' + clip + '.json'))
        plan, _ = bcl.szenen_planen(d)
        x, sr = sf.read(R + 'clips/ton/' + clip + '.mp3', dtype='float32')
        if x.ndim > 1:
            x = x.mean(1)
        _audio[clip] = (x, sr, {s['name']: (p['start'], s['dauer']) for p, s in zip(plan, d['szenen'])})
    x, sr, start = _audio[clip]
    a, dauer = start[name]
    echt = x[int(a * sr):int((a + dauer) * sr)]
    y, sr2 = _ton_synth(text)
    My = _merkmale(y, sr2)
    weg = _dtw(My, _merkmale(echt, sr))
    voll = _laut(text)

    def t_von(phrase):
        i = text.find(phrase)
        assert i >= 0, phrase
        k = 0
        if i > 0:
            # wo endet der Satzanfang innerhalb der ganzen Synthese? (Satzanfang allein gesprochen hat
            # ein anderes Tempo am Schluss, darum ebenfalls per Abgleich, Ende frei)
            vor = _laut(text[:i].rstrip(' ,:;'))
            pidx = [j for j, v in enumerate(vor) if v]
            ende = pidx[-1] if pidx else 0
            yv, srv = _ton_synth(text[:i].rstrip(' ,:;'))
            Mv = _merkmale(yv, srv)[:int(ende * 0.01 / 0.02) + 1]
            k = int((_dtw(Mv, My, offen=True) * 0.02 + 0.05) / 0.01)
        while k < len(voll) and not voll[k]:
            k += 1
        z = min(int(k * 0.01 / 0.02), max(weg))
        return weg.get(z, weg[max(weg)]) * 0.02
    return t_von


for clip in sys.argv[1:]:
    p = R + 'clips/' + clip + '.json'
    d = json.load(open(p))
    zt = zeiten(clip)
    n = 0
    for s in d['szenen']:
        if s['name'] not in zt:
            continue
        t_von = synthgeber(clip, s['name'], s['sprecher']) if os.environ.get('PIPER_MODELL') else zeitgeber(zt[s['name']], s['sprecher'])
        frage = [f['bei'] for f in d.get('fragen', []) if f['szene'] == s['name']]
        for e in s['elemente']:
            if e.get('_anker'):                     # ganze Elemente: setzt die Zeit von anker.py genauer neu
                i = s['sprecher'].find(e['_anker'])
                e['ein'] = round(max(0.05 if e['typ'] in ('graf', 'bild') and i == 0 else 0.2, t_von(e['_anker']) + 0.1) + e.get('_versatz', 0), 2)
                if frage and e['typ'] not in ('graf', 'bild'):
                    e['ein'] = max(e['ein'], round(frage[0] + 0.5, 1))
                n += 1
            if e.get('typ') != 'graf':
                continue
            for k in TEILE:
                for teil in e.get(k, []):
                    if teil.get('_ein'):
                        teil['ein'] = round(max(0.1, t_von(teil['_ein']) + 0.1 + teil.get('_ein_versatz', 0)), 2); n += 1
                    if teil.get('_aus'):
                        teil['aus'] = round(max(0.2, t_von(teil['_aus']) + 0.1 + teil.get('_aus_versatz', 0)), 2); n += 1
                    lf = teil.get('laeufer')
                    if lf and lf.get('_bahn'):
                        lf['bahn'] = [[round(max(0.1, t_von(a) + v), 2), x] for a, v, x in lf['_bahn']]; n += 1
                    if lf and lf.get('_ein'):
                        lf['ein'] = round(max(0.1, t_von(lf['_ein']) + 0.1), 2); n += 1
                    if lf and lf.get('_aus'):
                        lf['aus'] = round(max(0.2, t_von(lf['_aus']) + 0.1), 2); n += 1
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'{clip}: {n} Zeiten gesetzt')
