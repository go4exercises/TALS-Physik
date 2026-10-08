"""Antwortbilder der Temperatur-Kontrollclips (07.10.2026).

  python3 scripts/lp/temperatur/antworten.py      # danach build-clips.py für die vier Kontrollclips

Jede Antwortszene «Frage 1» … «Frage 5» bekommt rechts ein Bild (x 1010, y 175, 760 × 760), das die
Antwort zeigt; es erscheint mit der Erklärung (ein 1.0), nach der Frage (bei 0.3). Wiederholbar: alte
Bilder (Kennung "antwort") werden zuerst entfernt. Alle Zahlen hier gerechnet. Farben wie clips.py:
1 Bernstein Celsius, 3 Grün Kelvin und absoluter Nullpunkt, 2 Orange Differenz, 4 Rot Druck, 5 Tinte.
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C  # noqa: E402  (nur Bausteine; clips.py schreibt beim Import nichts)

R = C.CLIPS + os.sep
CEL, ORA, KEL, DRU, TIN = C.CEL, C.ORA, C.KEL, C.DRU, C.TIN
S, P, T, F, rechteck, kreis = C.S, C.P, C.T, C.F, C.rechteck, C.kreis


def antwort(g, ein=1.0):
    g['antwort'] = True
    g['ein'] = ein
    g.pop('_anker', None)
    g.pop('_versatz', None)
    return g


def lade(n):
    d = json.load(open(R + n + '.json', encoding='utf-8'))
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]
    return d


def setze(d, szene, *els):
    for s in d['szenen']:
        if s['name'] == szene:
            s['elemente'].extend(els)
            return
    raise KeyError(szene)


def speichere(n, d):
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('ok', n)


def balken(werte, farbe, namen, unten=None, ymax=None, yname='T [K]', yt=(100, 200, 300, 400), mal=None):
    """Säulen ab null in einer Skala (Kelvin): Vergleiche im Verhältnis."""
    ymax = ymax or max(werte) * 1.25
    fl, tx, st = [], [], []
    for k, (w, n) in enumerate(zip(werte, namen)):
        x0 = 2 + 4 * k
        fl.append(F(rechteck(x0, 0, x0 + 2, w), farbe, 0.45))
        tx.append(T(x0 + 1, w + ymax * 0.04, n, farbe, 28))
        if unten:
            tx.append(T(x0 + 1, -ymax * 0.07, unten[k], CEL, 24))
    if mal:
        st += [S((2, werte[0]), (8.6, werte[0]), TIN, 3, gestrichelt=True), P((8.6, werte[0]), (8.6, werte[1] - ymax * 0.01), ORA, 5)]
        tx.append(T(8.8, (werte[0] + werte[1]) / 2, mal, ORA, 30, 'start'))
    return C.graf([-0.5, 10], [-ymax * 0.12, ymax], [], list(yt), '', yname, flaechen=fl, texte=tx, strecken=st)


# ======================================================== Kapitel 1: Teilchenbewegung
n = 'p5-1-lp-kontrolle-teilchen'; d = lade(n)
rnd = random.Random(3)
fl = [F(rechteck(1.5, 0.8, 8.5, 7.0), TIN, 0.10)]
st = [S((1.5, 8.6), (1.5, 0.8), TIN, 5), S((1.5, 0.8), (8.5, 0.8), TIN, 5), S((8.5, 0.8), (8.5, 8.6), TIN, 5), S((1.5, 7.0), (8.5, 7.0), TIN, 3)]
fig = []
for k in range(14):
    x, y = 2.3 + rnd.random() * 5.4, 1.6 + rnd.random() * 4.6
    w, l = rnd.random() * 2 * math.pi, 0.5 + rnd.random() * 0.7
    fig.append(kreis(x, y, 0.22, TIN, 0.9, 2))
    st.append(P((x, y), (x + l * math.cos(w), y + l * math.sin(w)), TIN, 3))
setze(d, 'Frage 1', antwort(C.graf([0, 10], [0, 10], achsen=False, flaechen=fl, strecken=st, figuren=fig,
      texte=[T(5, 9.3, 'ruhiges Glas, 18 °C:', TIN, 26), T(5, 8.6, 'Teilchen ständig in Bewegung', TIN, 26)])))
# F2: Tempi einzelner Teilchen als Pfeile, Mittelwert gestrichelt, ein Teilchen doppelt so schnell
q = [0.45, 0.7, 0.85, 1.0, 1.15, 1.3, 2.0, 0.55]
st, tx = [], []
for k, v in enumerate(q):
    y = 8.6 - 0.95 * k
    st.append(P((1, y), (1 + 2.8 * v, y), ORA if v == 2.0 else TIN, 5))
st.append(S((3.8, 0.6), (3.8, 9.2), KEL, 3, gestrichelt=True))
tx += [T(4.0, 0.5, 'Mittelwert → Temperatur', KEL, 24, 'start'), T(6.8, 8.6 - 0.95 * 6 + 0.25, 'doppelt so schnell', ORA, 24, 'start')]
setze(d, 'Frage 2', antwort(C.graf([0, 10], [0, 10], achsen=False, strecken=st, texte=tx)))
# F3: Kurve des mittleren Tempos bei 35 °C und 70 °C
setze(d, 'Frage 3', antwort(C.tempo_graf(punkte=[
    {'x': 35, 'y': round(C.vm(35), 2), 'farbe': CEL, 'beschriftung': '(35 °C; 483 m/s)', 'beschriftung_bei': [38, 360], 'anker': 'start'},
    {'x': 70, 'y': round(C.vm(70), 2), 'farbe': CEL, 'beschriftung': '(70 °C; 509 m/s)', 'beschriftung_bei': [66, 600], 'anker': 'end'}])))
# F4: zwei verschlossene Gläser mit Parfüm, kalt und warm: kurze und lange Pfeile der Duftteilchen
st, fig = [], []
for x0, l, fa in ((1.0, 0.55, TIN), (5.8, 1.15, ORA)):
    st += [S((x0, 0.8), (x0, 7.8), TIN, 4), S((x0 + 3.2, 0.8), (x0 + 3.2, 7.8), TIN, 4), S((x0, 0.8), (x0 + 3.2, 0.8), TIN, 4),
           S((x0 - 0.15, 7.9), (x0 + 3.35, 7.9), TIN, 8)]
    fig.append(kreis(x0 + 1.6, 1.15, 0.3, TIN, 0.6, 2))
    rr = random.Random(7)
    for k in range(7):
        x, y = x0 + 0.5 + rr.random() * 2.2, 1.6 + (k + 0.5) * (5.6 if l > 1 else 3.2) / 7
        w = rr.random() * 2 * math.pi
        fig.append(kreis(x, y, 0.16, fa, 0.9, 2))
        st.append(P((x, y), (x + l * math.cos(w), y + l * math.sin(w)), fa, 3))
setze(d, 'Frage 4', antwort(C.graf([0, 10], [0, 10], achsen=False, strecken=st, figuren=fig,
      texte=[T(2.6, 8.7, '10 °C', TIN, 26), T(7.4, 8.7, '30 °C', ORA, 26), T(7.4, 0.2, 'Duft schneller oben', ORA, 24)])))
# F5: Kurve bis zum absoluten Nullpunkt
g = C.graf([-300, 150], [-60, 700], [-200, -100, 100], [200, 400, 600], 'ϑ [°C]', 'Tempo [m/s]',
           kurven=[{'formel': C.VFORMEL, 'von': -150, 'bis': 150, 'farbe': TIN, 'dicke': 5, 'n': 300},
                   {'formel': C.VFORMEL, 'von': -255, 'bis': -150, 'farbe': TIN, 'dicke': 4, 'gestrichelt': True, 'n': 300}],
           strecken=[S((-273.15, -40), (-273.15, 640), KEL, 3, gestrichelt=True)],
           texte=[T(-266, 600, 'absoluter Nullpunkt:', KEL, 24, 'start'), T(-266, 545, 'Bewegung minimal', KEL, 24, 'start')])
setze(d, 'Frage 5', antwort(g))
speichere(n, d)

# ======================================================== Kapitel 2: Aggregatzustände
n = 'p5-1-lp-kontrolle-aggregat'; d = lade(n)
g = C.baender([('Sauerstoff', -219, -183)], -260, -140)
g['xteilung'] = [[v, ('%g' % v).replace('-', '−')] for v in (-240, -220, -200, -180, -160)]
g['strecken'] = [S((-200, -1.0), (-200, 9.6), CEL, 4, gestrichelt=True)]
g['texte'] += [T(-200, 9.75, '−200 °C', CEL, 26), T(-201, 6.2, 'flüssig', TIN, 26)]
setze(d, 'Frage 1', antwort(g))
g = C.baender([('Zinn', 232, 2602)], 0, 400)
g['xteilung'] = [[v, '%g' % v] for v in (100, 200, 300)]
g['strecken'] = [P((20, 6.6), (300, 6.6), ORA, 5)]
g['texte'] += [T(160, 5.7, 'von 20 °C auf 300 °C', ORA, 24), T(232, 9.6, 'schmelzen bei 232 °C', CEL, 26)]
setze(d, 'Frage 2', antwort(g))
setze(d, 'Frage 3', antwort(C.bild('p5-1-lp-aggregat-50.jpg', breite=330, x=1010, y=300)), antwort(C.bild('p5-1-lp-aggregat-120.jpg', breite=330, x=1400, y=300)),
      antwort(C.notiz('flüssig', x=1080, y=720, breite=250, g=38, ein=1.0)), antwort(C.notiz('gasförmig', x=1450, y=720, breite=280, g=38, ein=1.0)))
setze(d, 'Frage 4', antwort(C.bild('p5-1-lp-aggregat-50.jpg', breite=480, x=1100, y=230)), antwort(C.bild('p5-1-lp-aggregat-m15.jpg', breite=480, x=1100, y=230), 3.0),
      antwort(C.notiz('flüssig → fest', x=1150, y=850, breite=500, g=38, ein=1.0)))
g = C.baender([('Blei', 327, 1749), ('Eisen', 1538, 2862)], 0, 3000)
g['flaechen'].append(F(rechteck(1538, 4.4, 1749, 9.6), TIN, 0.15))
g['xteilung'] = [[v, '%g' % v] for v in (500, 1000, 1500, 2000, 2500)]
g['strecken'] = [S((1600, -1.0), (1600, 3.9), CEL, 4, gestrichelt=True), S((1600, 4.5), (1600, 9.6), CEL, 4, gestrichelt=True)]
g['texte'] += [T(1643, 3.0, 'beide flüssig', TIN, 24), T(1600, 9.75, '1600 °C', CEL, 26)]
setze(d, 'Frage 5', antwort(g))
speichere(n, d)

# ======================================================== Kapitel 3: Celsius und Kelvin
n = 'p5-1-lp-kontrolle-skalen'; d = lade(n)
g = C.thermometer(3.0, marken=[(3.0, '0 °C', '')])
g['flaechen'] = [F(rechteck(2.6, 0.2, 5.8, 3.6), TIN, 0.12)]
g['strecken'] += [S((2.6, 3.6), (5.8, 3.6), TIN, 3)]
g['figuren'] += [{'art': 'vieleck', 'punkte': [[4.9, 2.2], [5.5, 2.2], [5.5, 2.8], [4.9, 2.8]], 'farbe': TIN, 'fuellung': 0.15, 'dicke': 2},
                 {'art': 'vieleck', 'punkte': [[4.9, 2.4], [5.5, 2.4], [5.5, 3.0], [4.9, 3.0]], 'farbe': TIN, 'fuellung': 0.15, 'dicke': 2}]
g['texte'] += [T(5, 9.7, 'Eis schmilzt: Temperatur bleibt fest', TIN, 26)]
setze(d, 'Frage 1', antwort(g))
y = lambda cm: 1.5 + cm * 0.32
g = C.thermometer(y(7), marken=[(y(3), '3 cm', '0 °C'), (y(7), '7 cm', '20 °C'), (y(23), '23 cm', '100 °C')])
g['strecken'] += [P((6.8, y(3)), (6.8, y(7)), ORA, 4), P((8.2, y(3)), (8.2, y(23)), ORA, 4)]
g['texte'] += [T(6.95, (y(3) + y(7)) / 2 + 0.3, '4 cm', ORA, 24, 'start'), T(8.35, 6.0, '20 cm', ORA, 24, 'start')]
setze(d, 'Frage 2', antwort(g))
g = C.gasgraf([], gerade=[S((-273.15, 0), (120, 1200 * (120 + 273.15) / 273.15), DRU, 4), S((-273.15, 0), (120, 500 * 393.15 / 273.15), DRU, 4, gestrichelt=True)],
              extra={'punkte': [{'x': -273.15, 'y': 0, 'farbe': KEL}],
                     'strecken': [S((-273.15, 60), (-273.15, 520), KEL, 2, gestrichelt=True)],
                     'texte': [T(-310, 600, '−273.15 °C', KEL, 24, 'start'),
                               T(-70, 1150, 'viel Helium', DRU, 24, 'end'), T(118, 470, 'wenig Luft', DRU, 24, 'end')]})
setze(d, 'Frage 3', antwort(g))
g = C.doppelstrahl(-320, 140, [-200, -100, 0, 100], [0, 100, 200, 300, 400],
                   extra={'flaechen': [F(rechteck(-320, 1.6, -273.15, 8.0), TIN, 0.25)],
                          'strecken': [S((-273.15, 1.6), (-273.15, 8.0), KEL, 3, gestrichelt=True)],
                          'texte': [T(-318, 8.6, 'unmöglich', TIN, 24, 'start'), T(-273.15, 9.4, 'absoluter Nullpunkt: 0 K', KEL, 24, 'start')]})
setze(d, 'Frage 4', antwort(g))
setze(d, 'Frage 5', antwort(balken([100, 200], KEL, ['100 K', '200 K'], ymax=260, yt=(100, 200), mal='× 2')))
speichere(n, d)

# ======================================================== Kapitel 4: Umrechnen
n = 'p5-1-lp-kontrolle-umrechnen'; d = lade(n)
for frage, c, tc, tk in (('Frage 1', -25, '−25 °C', '248.15 K'), ('Frage 2', 93 - 273.15, '−180.15 °C', '93 K')):
    g = C.strahl()
    m = C.marke(round(c, 2), txt_c=tc, txt_k=tk)
    for k in ('strecken', 'punkte', 'texte'):
        g.setdefault(k, []).extend(m.get(k, []))
    setze(d, frage, antwort(g))
g = C.doppelstrahl(-20, 100, [0, 20, 40, 60, 80], [280, 300, 320, 340, 360],
                   extra={'strecken': [S((85, 5.6), (85, 7.4), TIN, 3), S((45, 5.6), (45, 7.4), TIN, 3), P((85, 8.2), (45, 8.2), ORA, 5),
                                       S((85, 2.1), (85, 3.9), TIN, 3), S((45, 2.1), (45, 3.9), TIN, 3), P((85, 1.2), (45, 1.2), ORA, 5)],
                          'texte': [T(65, 8.8, 'Δϑ = −40 °C', ORA, 28), T(65, 0.2, 'ΔT = −40 K', ORA, 28)]})
setze(d, 'Frage 3', antwort(g))
setze(d, 'Frage 4', antwort(balken([293.15, 313.15], KEL, ['293.15 K', '313.15 K'], unten=['20 °C', '40 °C'], ymax=400, yt=(100, 200, 300), mal='× 1.07')))
setze(d, 'Frage 5', antwort(balken([200.15, 400.15], KEL, ['200.15 K', '400.15 K'], unten=['−73 °C', '127 °C'], ymax=500, yt=(100, 200, 300, 400), mal='× 2.00')))
speichere(n, d)
