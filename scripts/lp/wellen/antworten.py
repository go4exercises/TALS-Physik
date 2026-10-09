"""Antwortbilder der Kontrollclips des Leitprogramms Wellen (08.10.2026).

  python3 scripts/lp/wellen/antworten.py      (nach build-clip-ton.py, vor anker.py und build-clips.py)

Jede Antwortszene «Frage 1» … «Frage 5» bekommt rechts ein Bild (x 1010, y 175, 760 x 760), das die
Antwort zeigt. Wiederholbar: alte Bilder und Zusatzteile (Kennung "antwort") werden zuerst entfernt.
Zwei Szenen tragen schon das Diagramm der Frage (Kapitel 2, Frage 1 und 2): Dort kommen die Antwortteile
(Masslinie λ bzw. T, der gesuchte Berg) in dasselbe Diagramm, mit "ein" nach der Frage.
Bausteine und Farben aus clips.py (1 Bernstein Welle, 2 Orange Licht, 3 Grün Ausbreitung, 4 Rot Wärme-
strahlung, 5 Tinte Teilchen, Masslinien, Achsen). Alle Zahlen hier gerechnet (assert).
"""
import json
import math
import os
import sys

sys.argv = sys.argv[:1]                       # clips.py liest die Kommandozeile; hier nichts schreiben
from clips import (BER, ORA, GRU, ROT, TIN, C, S, P, T, F, rechteck, umriss, mass, welle, graf, skizze, r4,
                   niveaus, elektron, photon, strahlung, atmo_skizze, band, LX, CLIPS)

R = CLIPS + os.sep
EIN = 1.0


def antwort(g):
    g['ein'] = EIN
    g['antwort'] = True
    return g


def lade(n):
    d = json.load(open(R + n + '.json', encoding='utf-8'))
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]
        for e in s['elemente']:
            if e.get('typ') == 'graf':
                for k in ('strecken', 'texte', 'punkte', 'kurven', 'flaechen'):
                    if k in e:
                        e[k] = [t for t in e[k] if not t.get('antwort')]
    return d


def setze(d, szene, el):
    for s in d['szenen']:
        if s['name'] == szene:
            assert not any(e['typ'] in ('graf', 'bild') for e in s['elemente']), szene
            s['elemente'].append(antwort(el))
            return
    raise KeyError(szene)


def ergaenze(d, szene, **teile):
    """Antwortteile in das Diagramm der Frage legen (erscheinen mit ein = EIN)."""
    for s in d['szenen']:
        if s['name'] == szene:
            g = [e for e in s['elemente'] if e['typ'] == 'graf'][0]
            for k, v in teile.items():
                g.setdefault(k, [])
                g[k] += [dict(t, ein=EIN, antwort=True) for t in v]
            return
    raise KeyError(szene)


def bild(datei):
    return {'typ': 'bild', 'datei': 'bilder/' + datei, 'x': 1000, 'y': 190, 'breite': 700, 'abstand': 0, 'anim': 'fade'}


def speichere(n, d):
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(n, 'gespeichert')


def mass_v(x, y1, y2, text, tx=None, farbe=TIN, groesse=26, anker_='start'):
    """Senkrechte Masslinie mit zwei Spitzen."""
    m = (y1 + y2) / 2
    return [P((x, m), (x, y1), farbe, dicke=3), P((x, m), (x, y2), farbe, dicke=3)], [T(x + 0.25 if tx is None else tx, m - 0.15, text, farbe, groesse, anker_)]


# ======================================================== Kapitel 1: Entstehung einer Welle
n = 'p6-1-lp-kontrolle-welle'; d = lade(n)
# F1 Stadion: Zuschauer auf festen Plätzen, die Bewegung läuft weiter
leute = []
for i in range(9):
    x = 1.0 + i
    h = 1.6 * math.exp(-((x - 4.0) / 1.1) ** 2)
    leute += [{'art': 'kreis', 'm': [r4(x), r4(4.2 + h)], 'r': 0.32, 'farbe': TIN, 'fuellung': 0.6}]
setze(d, 'Frage 1', skizze(figuren=leute,
                           strecken=[S((0.4, 3.6), (9.6, 3.6), TIN, dicke=3)] + [S((1.0 + i, 3.0), (1.0 + i, 3.6), TIN, dicke=2) for i in range(9)]
                           + [P((3.0, 7.3), (6.5, 7.3), GRU, dicke=6)],
                           texte=[T(4.75, 7.9, 'das Muster läuft weiter', GRU, 26), T(5.0, 2.2, 'jeder bleibt auf seinem Platz', TIN, 26)]))
# F2 Autokolonne: Autos rollen nach vorn (rechts), die Anfahrwelle läuft nach hinten (links) — beides auf derselben Linie
autos = []
for i, x in enumerate([1.0, 2.0, 3.0, 4.6, 6.6, 8.6]):
    autos += umriss(x - 0.35, 4.6, x + 0.35, 5.4, TIN, 4)
setze(d, 'Frage 2', skizze(strecken=autos + [S((0.3, 4.3), (9.7, 4.3), TIN, dicke=3)]
                           + [P((4.6, 6.0), (5.4, 6.0), TIN, dicke=5), P((6.6, 6.0), (7.4, 6.0), TIN, dicke=5), P((8.6, 6.0), (9.4, 6.0), TIN, dicke=5)]
                           + [P((6.0, 7.8), (2.0, 7.8), GRU, dicke=6)],
                           texte=[T(2.0, 3.6, 'dicht', TIN, 24), T(7.6, 3.6, 'Abstand gross', TIN, 24), T(7.0, 6.6, 'Autos rollen nach vorn', TIN, 24),
                                  T(4.0, 8.4, 'Anfahrwelle läuft nach hinten', GRU, 26), T(5.0, 1.8, 'gleiche Linie: Längswelle', TIN, 28)]))
# F3 Wäscheleine: 6.0 m in 1.5 s
assert abs(6.0 / 1.5 - 4.0) < 1e-12
st3, tx3 = mass(0.6, 9.0, 3.6, '6.0 m in 1.5 s', ty=2.8)
setze(d, 'Frage 3', skizze(strecken=[S((0.6, 5.0), (9.4, 5.0), TIN, dicke=3), P((5.0, 7.0), (8.4, 7.0), GRU, dicke=6)] + st3,
                           kurven=[{'trig': 'sin', 'bewegung': [[0, 1.1, r4(math.pi / 1.2), 7.8, 5.0]], 'von': 7.8, 'bis': 9.0, 'farbe': BER, 'dicke': 6}],
                           texte=tx3 + [T(6.7, 7.6, 'c = 4.0 m/s', GRU, 28)]))
# F4 Boot: 12 Schwingungen pro Minute, T = 5.0 s
assert abs(60 / 12 - 5.0) < 1e-12
st4, tx4 = mass(5.0, 10.0, 1.35, 'T = 5.0 s', ty=1.5)   # Berge auf den Teilstrichen 5, 10, … 30 s: die Kurve kreuzt die Achse zwischen den Zahlen
setze(d, 'Frage 4', graf((-2.5, 31), (-1.6, 1.8), [5, 10, 15, 20, 25, 30], [-1, 1], 't [s]', 'y [m]',
                         kurven=[welle(1.0, 5.0, 5.0, von=0, bis=30)], strecken=st4, texte=tx4 + [T(15, -1.45, 'f = 1 / T = 0.20 Hz', TIN, 26)]))
# F5 Hand hört auf: der Berg läuft weiter
setze(d, 'Frage 5', skizze(strecken=[S((0.6, 5.0), (9.4, 5.0), TIN, dicke=3), P((6.2, 7.4), (8.6, 7.4), GRU, dicke=6)],
                           kurven=[{'trig': 'sin', 'bewegung': [[0, 1.6, r4(math.pi / 2.0), 5.0, 5.0]], 'von': 5.0, 'bis': 7.0, 'farbe': BER, 'dicke': 6}],
                           texte=[T(0.6, 4.2, 'Hand ruht', TIN, 24, 'start'), T(7.4, 8.0, 'läuft weiter', GRU, 26), T(3.0, 5.6, 'Seil ruhig', TIN, 24)]))
speichere(n, d)

# ======================================================== Kapitel 2: Momentbild und Zeitdiagramm
n = 'p6-1-lp-kontrolle-diagramme'; d = lade(n)
s1, _ = mass(1.0, 2.5, -5.2, '')
ergaenze(d, 'Frage 1', strecken=s1, texte=[T(2.65, -5.45, 'λ = 1.5 m', TIN, 26, 'start')], punkte=[{'x': 2.5, 'y': 4, 'farbe': GRU}])
s2, t2 = mass(1.0, 4.0, 50, 'T = 3.0 s', ty=56)
ergaenze(d, 'Frage 2', strecken=s2 + [S((4.0, 40), (4.0, 50), TIN, dicke=2, gestrichelt=True), S((1.0, 40), (1.0, 50), TIN, dicke=2, gestrichelt=True)], texte=t2)
# F3: λ = 0.60 m, in T = 0.25 s eine Wellenlänge weiter
assert abs(0.60 / 0.25 - 2.4) < 1e-12
s3, t3 = mass(0.15, 0.75, 5.3, 'λ = 0.60 m', ty=5.85)
setze(d, 'Frage 3', graf((-0.15, 2.0), (-7, 7), [0.5, 1.0, 1.5], [-4, 4], 's [m]', 'y [cm]',
                         kurven=[welle(4, 0.6, 0.15, von=0, bis=1.85)], strecken=s3 + [P((0.15, -5.3), (0.75, -5.3), GRU, dicke=5)],
                         texte=t3 + [T(0.45, -6.3, 'in T = 0.25 s', GRU, 24)]))
# F4: Zeitdiagramm, Abstand 0.4 s ist die Periode
s4, t4 = mass(0.1, 0.5, 5.3, 'T = 0.4 s', ty=5.85)
setze(d, 'Frage 4', graf((-0.12, 1.35), (-7, 7), [0.2, 0.4, 0.6, 0.8, 1.0, 1.2], [-4, 4], 't [s]', 'y [cm]',
                         kurven=[welle(4, 0.4, 0.1, von=0, bis=1.25)], strecken=s4, texte=t4 + [T(0.65, -6.3, 'Zeitachse: eine Zeit, keine Länge', TIN, 24)]))
# F5: Berg rückt 1.5 m in 0.5 s; λ = 0.75 m
assert abs(1.5 / 0.5 / 0.75 - 4.0) < 1e-12
setze(d, 'Frage 5', graf((-0.2, 3.3), (-8.4, 7.5), [[0.75, ''], [1.5, ''], [2.25, ''], [3.0, '']], [-4, 4], 's [m]', 'y [cm]',
                         kurven=[welle(4, 0.75, 2.1, von=0, bis=3.1)], punkte=[{'x': 0.6, 'y': 4, 'farbe': TIN}, {'x': 2.1, 'y': 4, 'farbe': GRU}],
                         strecken=[P((0.6, 5.0), (2.1, 5.0), GRU, dicke=5)] + mass(2.1, 2.85, -5.3, 'λ = 0.75 m', ty=-6.3)[0],
                         texte=[T(1.35, 5.6, '1.5 m in 0.5 s', GRU, 24), T(0.6, 6.6, 'Berg vorher', TIN, 22), T(2.1, 6.6, 'nachher', GRU, 22)]
                         + [T(x, -7.9, t, TIN, 22) for x, t in ((0.75, '0.75'), (1.5, '1.5'), (2.25, '2.25'), (3.0, '3'))]
                         + mass(2.1, 2.85, -5.3, 'λ = 0.75 m', ty=-6.3)[1]))
speichere(n, d)


# ======================================================== Kapitel 3: Sender und Medium
def saeulen(eintraege, ymax, yt, yname):
    fl, tx = [], []
    for i, (et, v, fa, vt) in enumerate(eintraege):
        x = 1 + 2.0 * i
        fl.append(F(rechteck(x - 0.6, 0, x + 0.6, v), fa, 0.55))
        tx += [T(x, -0.08 * ymax, et, TIN, 24), T(x, v + 0.04 * ymax, vt, fa, 26)]
    return graf((-0.6, 1 + 2.0 * (len(eintraege) - 1) + 1.0), (-0.15 * ymax, 1.15 * ymax), [], yt, '', yname, flaechen=fl, texte=tx)


n = 'p6-1-lp-kontrolle-medium'; d = lade(n)
assert round(340 / 680, 2) == 0.5 and round(980 / 680, 2) == 1.44
setze(d, 'Frage 1', saeulen([('Luft', 0.5, TIN, '0.50 m'), ('Helium', 980 / 680, BER, '1.44 m')], 1.6, [0.5, 1.0, 1.5], 'λ [m]'))
assert round(340 / 100e3 * 1000, 1) == 3.4 and round(1500 / 100e3 * 1000, 1) == 15.0
setze(d, 'Frage 2', saeulen([('Luft', 3.4, TIN, '3.4 mm'), ('Wasser', 15.0, BER, '15 mm')], 16, [5, 10, 15], 'λ [mm]'))
# F3: Luft → Eisen (nicht massstäblich: im Eisen 15-mal länger)
assert abs(5170 / 340 - 15.2) < 0.05
setze(d, 'Frage 3', skizze(flaechen=[F(rechteck(5.0, 3.0, 9.7, 7.0), TIN, 0.18)],
                           kurven=[{'trig': 'sin', 'bewegung': [[0, 1.0, r4(2 * math.pi / 0.8), 0.3, 5.0]], 'von': 0.3, 'bis': 5.0, 'farbe': BER, 'dicke': 5},
                                   {'trig': 'sin', 'bewegung': [[0, 1.0, r4(2 * math.pi / 3.2), 2.2, 5.0]], 'von': 5.0, 'bis': 9.7, 'farbe': BER, 'dicke': 5}],
                           texte=[T(2.6, 7.6, 'Luft', TIN, 26), T(7.3, 7.6, 'Eisen', TIN, 26), T(5.0, 1.8, 'f bleibt; c und λ werden grösser', TIN, 26),
                                  T(5.0, 0.9, 'nicht massstäblich', TIN, 20)]))
# F4: Mond, kein Medium
setze(d, 'Frage 4', skizze(figuren=[{'art': 'kreis', 'm': [2.5, 5.0], 'r': 1.0, 'farbe': TIN, 'fuellung': 0.2}, {'art': 'kreis', 'm': [7.5, 5.0], 'r': 1.0, 'farbe': TIN, 'fuellung': 0.2},
                                    {'art': 'bogen', 'm': [2.5, 5.0], 'r': 1.6, 'von': -35, 'bis': 35, 'farbe': BER, 'dicke': 4, 'gestrichelt': True}],
                           strecken=[S((4.4, 4.2), (5.6, 5.8), TIN, dicke=5), S((4.4, 5.8), (5.6, 4.2), TIN, dicke=5)],
                           texte=[T(5.0, 7.4, 'Vakuum: kein Medium', TIN, 28), T(5.0, 2.4, 'kein Schall', TIN, 28)]))
# F5: Stimmgabel 500 Hz, 15 °C (340 m/s) und 25 °C (346 m/s)
assert round(340 / 500, 3) == 0.68 and round(346 / 500, 3) == 0.692
setze(d, 'Frage 5', saeulen([('15 °C', 0.680, TIN, '0.680 m'), ('25 °C', 0.692, BER, '0.692 m')], 0.8, [0.2, 0.4, 0.6], 'λ [m]'))
speichere(n, d)

# ======================================================== Kapitel 4: Elektromagnetische Wellen
n = 'p6-1-lp-kontrolle-em'; d = lade(n)
glocke = [{'art': 'bogen', 'm': [5.0, 3.0], 'r': 3.4, 'von': 0, 'bis': 180, 'farbe': TIN, 'dicke': 5},
          {'art': 'kreis', 'm': [3.8, 3.7], 'r': 0.55, 'farbe': TIN, 'fuellung': 0.3}, {'art': 'kreis', 'm': [6.3, 3.6], 'r': 0.3, 'farbe': ORA, 'fuellung': 0.8}]
setze(d, 'Frage 1', skizze(figuren=glocke,
                           strecken=[S((1.2, 3.0), (8.8, 3.0), TIN, dicke=5), S((5.0, 3.0), (5.0, 1.6), TIN, dicke=4), P((5.0, 1.6), (7.6, 1.6), TIN, dicke=4)]
                           + [P((6.3 + 0.45 * dx, 3.6 + 0.45 * dy), (6.3 + 1.1 * dx, 3.6 + 1.1 * dy), ORA, dicke=4) for dx, dy in ((1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7))],
                           texte=[T(3.0, 2.3, 'Wecker: kaum hörbar', BER, 22), T(7.2, 2.3, 'Lämpchen: gleich hell', ORA, 22),
                                  T(7.8, 0.9, 'Luft abgepumpt', TIN, 22), T(5.0, 7.4, 'Schall braucht ein Medium, Licht nicht', TIN, 24)]))
reihe = ['Gamma', 'Röntgen', 'UV', 'Licht', 'Infrarot', 'Mikrowellen', 'Radio']
setze(d, 'Frage 2', skizze(strecken=[S((0.5, 5.6 - 0.0), (9.5, 5.6), TIN, dicke=3)] + [S((0.5 + 9.0 * i / 7, 5.2), (0.5 + 9.0 * i / 7, 6.0), TIN, dicke=3) for i in range(8)]
                           + [P((1.0, 3.2), (9.0, 3.2), TIN, dicke=5)],
                           texte=[T(0.5 + 9.0 * (i + 0.5) / 7, 6.6 + 0.8 * (i % 2), r, TIN, 24) for i, r in enumerate(reihe)]
                           + [T(5.0, 2.4, 'Wellenlänge wird länger', TIN, 26)]))
assert abs(C / 12e9 - 0.025) < 1e-12
setze(d, 'Frage 3', graf((-0.4, 8.6), (-6.6, 6.6), [2.5, 5, 7.5], [], 's [cm]', 'E (schematisch)',
                         kurven=[welle(3, 2.5, 1.25, von=0, bis=8.2)], strecken=mass(1.25, 3.75, 4.3, 'λ = 2.5 cm')[0],
                         texte=mass(1.25, 3.75, 4.3, 'λ = 2.5 cm', ty=4.9)[1] + [T(4.1, -5.0, 'f = 12 GHz', TIN, 26)]))
assert round(C / 700e-9 / 1e14, 1) == 4.3 and round(C / 450e-9 / 1e14, 1) == 6.7
setze(d, 'Frage 4', graf((-120, 2300), (-6.6, 6.6), [700, 1400, 2100], [], 's [nm]', 'E (schematisch)',
                         kurven=[{'trig': 'sin', 'bewegung': [[0, 1.2, r4(2 * math.pi / 700), 0, 3.0]], 'von': 0, 'bis': 2150, 'farbe': ROT, 'dicke': 5},
                                 {'trig': 'sin', 'bewegung': [[0, 1.2, r4(2 * math.pi / 450), 0, -2.6]], 'von': 0, 'bis': 2150, 'farbe': TIN, 'dicke': 5, 'gestrichelt': True}],
                         texte=[T(1075, 5.0, 'rot: 700 nm; 4.3 · 10¹⁴ Hz', ROT, 24), T(1075, -5.0, 'blau (gestrichelt): 450 nm; 6.7 · 10¹⁴ Hz', TIN, 24)]))
bfeld, bkreuz = [], []
for k in range(5):                                    # Berge und Täler von E bei x = 1.75 + 1.5 k
    x = 1.75 + 1.5 * k
    bfeld.append({'art': 'kreis', 'm': [r4(x), 5.0], 'r': 0.28, 'farbe': TIN, 'fuellung': 0, 'dicke': 3})
    if k % 2 == 0:                                    # E oben: B aus der Ebene heraus (Punkt)
        bfeld.append({'art': 'kreis', 'm': [r4(x), 5.0], 'r': 0.07, 'farbe': TIN, 'fuellung': 1, 'dicke': 2})
    else:                                             # E unten: B in die Ebene hinein (Kreuz)
        bkreuz += [S((x - 0.18, 4.82), (x + 0.18, 5.18), TIN, dicke=3), S((x - 0.18, 5.18), (x + 0.18, 4.82), TIN, dicke=3)]
setze(d, 'Frage 5', skizze(kurven=[{'trig': 'sin', 'bewegung': [[0, 1.8, r4(2 * math.pi / 3.0), 1.0, 5.0]], 'von': 1.0, 'bis': 8.5, 'farbe': BER, 'dicke': 6}],
                           figuren=bfeld,
                           strecken=[S((0.6, 5.0), (8.9, 5.0), TIN, dicke=2), P((8.6, 5.0), (9.6, 5.0), GRU, dicke=6)] + bkreuz,
                           texte=[T(9.4, 5.5, 'c', GRU, 30), T(1.6, 7.6, 'E: elektrisches Feld, auf und ab', BER, 22, 'start'),
                                  T(1.6, 2.2, 'B: senkrecht zur Zeichenebene (⊙ heraus, ⊗ hinein)', TIN, 22, 'start'), T(1.6, 1.4, 'beide quer zur Ausbreitung, im gleichen Takt', TIN, 22, 'start')]))
speichere(n, d)

# ======================================================== Kapitel 5: Atom und Laser
n = 'p6-1-lp-kontrolle-licht'; d = lade(n)
st, tx = niveaus(x0=4.2, x1=6.4, mit3=False)
k_in, p_in = photon(0.4, 3.4, 6.7)
k1, p1 = photon(6.9, 9.7, 6.6)
k2, p2 = photon(6.9, 9.7, 5.4)
setze(d, 'Frage 1', skizze(strecken=st + [p_in, p1, p2, P((5.3, 5.7), (5.3, 2.35), TIN, dicke=3, gestrichelt=True)], kurven=[k_in, k1, k2],
                           figuren=[elektron(5.3, 2.0), {'art': 'kreis', 'm': [5.3, 6.0], 'r': 0.22, 'farbe': TIN, 'fuellung': 0, 'gestrichelt': True}],
                           texte=tx + [T(1.9, 7.6, 'ein Photon', ORA, 24), T(8.3, 7.5, 'zwei gleiche', ORA, 24), T(5.5, 4.0, 'Elektron: E₂ → E₁', TIN, 22, 'start')]))
setze(d, 'Frage 2', graf((190, 420), (-0.5, 1.6), [200, 250, 300, 350, 400], [], 'λ [nm]', '',
                         flaechen=[F(rechteck(200, 0, 400, 1.0), ORA, 0.25), F(rechteck(252.5, 0, 255.5, 1.0), TIN, 1.0)],
                         texte=[T(254, 1.15, '254', TIN, 24), T(300, 1.4, 'UV-Licht hinter kaltem Quecksilberdampf', TIN, 22)]))
st, tx = niveaus(mit3=False)
setze(d, 'Frage 3', skizze(strecken=[S((1.4, 2.0), (6.0, 2.0), TIN, dicke=4), S((1.4, 4.0), (6.0, 4.0), TIN, dicke=4), S((1.4, 6.0), (6.0, 6.0), TIN, dicke=4),
                                     P((2.2, 3.85), (2.2, 2.15), TIN, dicke=4), P((4.4, 5.85), (4.4, 2.15), TIN, dicke=4)],
                           texte=[T(1.2, 1.85, 'E₁', TIN, 26, 'end'), T(1.2, 3.85, 'E₂', TIN, 26, 'end'), T(1.2, 5.85, 'E₃', TIN, 26, 'end'),
                                  T(2.35, 3.0, '800 nm', TIN, 22, 'start'), T(4.55, 3.0, '400 nm', TIN, 22, 'start'),
                                  T(5.0, 8.2, 'doppelte Stufe: halbe Wellenlänge', TIN, 24)]))
strahlen = [P((2.4 + 0.6 * math.cos(w), 5.0 + 0.6 * math.sin(w)), (2.4 + 1.8 * math.cos(w), 5.0 + 1.8 * math.sin(w)), ORA, dicke=4)
            for w in [k * math.pi / 4 for k in range(8)]]
laser = []
for y in (4.2, 5.0, 5.8):
    k_, p_ = photon(6.0, 9.6, y, lam=0.5)
    laser += [(k_, p_)]
setze(d, 'Frage 4', skizze(figuren=[{'art': 'kreis', 'm': [2.4, 5.0], 'r': 0.45, 'farbe': ORA, 'fuellung': 0.6}],
                           strecken=strahlen + umriss(4.6, 3.9, 5.9, 6.1, TIN, 4) + [p_ for _, p_ in laser],
                           kurven=[k_ for k_, _ in laser],
                           texte=[T(2.4, 2.6, 'Glühlampe:', ORA, 22), T(2.4, 1.9, 'alle Richtungen', ORA, 22), T(7.6, 3.3, 'Laser: eine Richtung,', TIN, 22), T(7.6, 2.6, 'gleicher Takt', TIN, 22)]))
setze(d, 'Frage 5', skizze(flaechen=[F(rechteck(4.4, 2.0, 5.6, 8.0), GRU, 0.3)],
                           strecken=[P((0.5, 6.0), (4.3, 6.0), TIN, dicke=7), P((5.7, 6.0), (9.4, 6.0), GRU, dicke=5),
                                     P((0.5, 4.0), (4.9, 4.0), ORA, dicke=4), P((0.5, 3.2), (4.9, 3.2), ROT, dicke=4)],
                           texte=[T(2.4, 6.6, 'weiss', TIN, 26), T(7.5, 6.6, 'nur Grün', GRU, 26), T(5.0, 8.5, 'grünes Glas', TIN, 24),
                                  T(0.4, 2.5, 'andere Farben:', TIN, 22, 'start'), T(0.4, 1.8, 'im Glas aufgenommen', TIN, 22, 'start')]))
speichere(n, d)

# ======================================================== Kapitel 6: Treibhauseffekt
n = 'p6-1-lp-kontrolle-treibhaus'; d = lade(n)
setze(d, 'Frage 1', strahlung(texte=[T(LX(2.2), 1.17, 'Stickstoff, Sauerstoff: keine grauen Bereiche', TIN, 22)]))
setze(d, 'Frage 2', strahlung(flaechen=[band(7.4, 8.0, deckung=0.45)], strecken=[S((LX(7.7), -0.05), (LX(7.7), 1.12), TIN, dicke=3, gestrichelt=True)],
                              texte=[T(LX(7.7), 1.17, 'CH₄: 7.7 µm', TIN, 22)]))
setze(d, 'Frage 3', strahlung(flaechen=[F(rechteck(LX(0.38), 0, LX(0.78), 1.12), ORA, 0.12), band(13.5, 17.0, deckung=0.35)],
                              texte=[T(LX(15.1), 1.17, 'CO₂', TIN, 22), T(LX(0.55), -0.1, 'Licht geht durch', ORA, 22)]))
setze(d, 'Frage 4', strahlung(flaechen=[band(5.5, 7.5), band(20, 200), band(13.5, 17.0), band(7.4, 8.0), band(9.3, 10.1), F(rechteck(LX(8.0), 0, LX(13.0), 1.12), GRU, 0.12)],
                              texte=[T(LX(10.2), 1.17, 'Fenster', GRU, 22)]))
setze(d, 'Frage 5', atmo_skizze(strecken=[P((4.5, 1.5), (4.5, 5.8), ROT, dicke=8)]
                                + [P((4.5, 6.0), (4.5 + dx, 6.0 + dy), ROT, dicke=5) for dx, dy in [(0, 2.6), (1.9, 1.9), (2.6, 0), (1.9, -1.9), (-1.9, 1.9), (-2.6, 0), (-1.9, -1.9)]],
                                texte=[T(4.8, 3.0, 'Bodenstrahlung', ROT, 24, 'start'), T(1.0, 9.2, 'in alle Richtungen, kein Spiegel', TIN, 24, 'start')]))
speichere(n, d)
