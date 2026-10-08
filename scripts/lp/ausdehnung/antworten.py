"""Antwortbilder der Kontrollclips des Leitprogramms Wärmeausdehnung und Gase (07.10.2026).

  python3 scripts/lp/ausdehnung/antworten.py

Jede Antwortszene «Frage 1» … «Frage 4» bekommt rechts ein Bild (x 1010, y 175, 760 x 760), das die
Antwort zeigt; es erscheint mit der Erklärung (ein 1.0, nach der Frage bei 0.3). Wiederholbar: alte
Bilder (Kennung "antwort") werden zuerst entfernt; die gemessenen Dauern bleiben. Alle Zahlen hier
gerechnet. Nach dem Lauf build-clips.py für die fünf Kontrollclips.

Farben wie im Leitprogramm und in clips.py: 1 Bernstein Ausdehnung und neuer Zustand, 2 Orange Temperatur,
3 Grün Volumen, 4 Rot Druck, 5 Tinte Ausgangszustand und Gefässe.
"""
import json
import math
import os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
AUS, TEMP, VOL, DRU, TIN = 1, 2, 3, 4, 5
K0 = 273.15


def fmt(v):
    return ('%g' % v).replace('-', '−')


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": xb, "ybereich": yb,
         "xteilung": [v if isinstance(v, list) else [v, fmt(v)] for v in xt] or [[1e9, '']],
         "yteilung": [v if isinstance(v, list) else [v, fmt(v)] for v in yt] or [[1e9, '']],
         "xname": xname, "yname": yname, "antwort": True}
    g.update(kw)
    return g


def skizze(x0, y0, span, **kw):
    """Bild ohne Achsen, quadratisches Fenster (1:1)."""
    return graf([x0, x0 + span], [y0, y0 + span], [], [], '', '', achsen=False, pfeile=False, **kw)


def r4(v):
    return round(v, 4)


def S(von, bis, farbe=TIN, dicke=4, **kw):
    d = {"von": [r4(von[0]), r4(von[1])], "bis": [r4(bis[0]), r4(bis[1])], "farbe": farbe, "dicke": dicke}
    d.update(kw)
    return d


def P(von, bis, farbe, dicke=5, **kw):
    return S(von, bis, farbe, dicke, pfeil=True, **kw)


def T(x, y, text, farbe=TIN, groesse=27, anker="middle"):
    return {"bei": [r4(x), r4(y)], "text": text, "farbe": farbe, "groesse": groesse, "anker": anker}


def F(pts, farbe=TIN, deckung=0.15):
    return {"punkte": [[r4(x), r4(y)] for x, y in pts], "farbe": farbe, "deckung": deckung}


def rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def umriss(x0, y0, x1, y1, farbe=TIN, dicke=4, **kw):
    p = rechteck(x0, y0, x1, y1)
    return [S(p[i], p[(i + 1) % 4], farbe, dicke, **kw) for i in range(4)]


def kreis(cx, cy, r, farbe=TIN, dicke=4):
    return [{"formel": "%g%+g*sqrt(abs(%g-(x-(%g))*(x-(%g))))" % (cy, vz, r * r, cx, cx), "von": cx - r, "bis": cx + r,
             "farbe": farbe, "dicke": dicke, "n": 200} for vz in (1, -1)]


def pt(x, y, farbe, text=None, bei=None, anker='start'):
    p = {"x": r4(x), "y": r4(y), "farbe": farbe}
    if text:
        p.update({"beschriftung": text, "beschriftung_bei": [r4(bei[0]), r4(bei[1])], "anker": anker})
    return p


def setze(d, szene, el):
    for s in d['szenen']:
        if s['name'] == szene:
            s['elemente'].append(el)
            return
    raise KeyError(szene)


def lade(n):
    d = json.load(open(R + n + '.json', encoding='utf-8'))
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]
    return d


def speichere(n, d):
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


# ======================================================== Länge (Kapitel 1)
n = 'p5-3-lp-kontrolle-laenge'; d = lade(n)
dl1 = 12e-6 * 900 * 35
assert abs(dl1 - 0.378) < 1e-9
setze(d, 'Frage 1', graf([-28, 44], [-12, 60], [-20, -10, 10, 20, 30, 40], [], 'ϑ [°C]', '',
    strecken=[S((-10, 0), (-10, 26), TIN, 3, gestrichelt=True), S((25, 0), (25, 26), TEMP, 3, gestrichelt=True), P((-10, 20), (25, 20), TEMP, 5)],
    punkte=[pt(-10, 0, TIN), pt(25, 0, TEMP)],
    texte=[T(-10, 31, 'Winter', TIN, 26), T(25, 31, 'Sommer', TEMP, 26), T(7.5, 24, 'ΔT = 35 K', TEMP, 30), T(24, 46, 'Δl = 0.378 m', AUS, 32)]))
# Frage 2: Namen an die drei Geraden des Fragebilds (gleiches Fenster)
lab = []
for name, a, far in (('Stahl', 12e-6, TIN), ('Messing', 18.4e-6, AUS), ('Aluminium', 23.8e-6, TIN)):
    lab.append(T(61.5, a * 3 * 60 * 1000, name, far, 28 if name != 'Messing' else 32, 'start'))
setze(d, 'Frage 2', graf([-6, 84], [-0.4, 4.6], [], [], '', '', achsen=False, pfeile=False, texte=lab,
    strecken=[S((0, 0), (60, 18.4e-6 * 3 * 60 * 1000), AUS, 9)]))
setze(d, 'Frage 3', skizze(0, 0, 10,
    strecken=umriss(1, 6.0, 9, 7.0, TIN, 4) + umriss(1, 3.0, 8.2, 4.0, AUS, 5) + [S((9, 2.4), (9, 7.6), TIN, 3, gestrichelt=True), P((9, 2.6), (8.2, 2.6), AUS, 5)],
    flaechen=[F(rechteck(1, 6.0, 9, 7.0), TIN, 0.12), F(rechteck(1, 3.0, 8.2, 4.0), AUS, 0.15)],
    texte=[T(5, 7.5, '20 °C: 2.500 m', TIN, 28), T(4.6, 4.5, '−20 °C: 2.4976 m', AUS, 28), T(8.6, 1.6, 'Δl = −2.38 mm', AUS, 26), T(5, 0.6, 'Längenänderung übertrieben', TIN, 22)]))
a4 = 0.0046 / (5.0 * 50)
assert abs(a4 - 18.4e-6) < 1e-12
setze(d, 'Frage 4', graf([-0.6, 9.6], [-3.2, 30], [], [5, 10, 15, 20, 25], '', 'α [10⁻⁶ 1/K]',
    flaechen=[F(rechteck(0.8, 0, 2.6, 12), TIN, 0.25), F(rechteck(3.8, 0, 5.6, 18.4), AUS, 0.5), F(rechteck(6.8, 0, 8.6, 23.8), TIN, 0.25)],
    texte=[T(1.7, 12.8, 'Stahl 12', TIN, 26), T(4.7, 19.2, 'Messing 18.4', AUS, 28), T(7.7, 24.6, 'Aluminium 23.8', TIN, 26), T(4.7, 27.6, 'gemessen: 18.4', AUS, 28)]))
speichere(n, d)

# ======================================================== Volumen (Kapitel 2)
n = 'p5-3-lp-kontrolle-volumen'; d = lade(n)
e = 18.4e-6 * 500 * 100
assert abs(e - 0.92) < 1e-9 and abs(3 * e - 2.76) < 1e-9
setze(d, 'Frage 1', graf([-0.8, 9], [-0.3, 3.3], [], [1, 2, 3], '', 'ΔV [cm³]',
    flaechen=[F(rechteck(2, 0, 4.5, e), AUS, 0.25), F(rechteck(2, e, 4.5, 2 * e), AUS, 0.4), F(rechteck(2, 2 * e, 4.5, 3 * e), AUS, 0.55)],
    strecken=[S((2, e), (4.5, e), AUS, 3), S((2, 2 * e), (4.5, 2 * e), AUS, 3)],
    texte=[T(3.25, e / 2 - 0.08, 'Länge', TIN, 24), T(3.25, 1.5 * e - 0.08, 'Breite', TIN, 24), T(3.25, 2.5 * e - 0.08, 'Höhe', TIN, 24),
           T(5.0, 0.46, 'α allein: 0.92 cm³', TIN, 26, 'start'), T(5.0, 2.68, '3 · α: 2.76 cm³', AUS, 28, 'start')]))
fl, st = 1.10e-3 * 1 * 20 * 1000, 36e-6 * 1 * 20 * 1000      # je Liter und 20 K, in ml
setze(d, 'Frage 2', graf([-0.8, 9], [-2.5, 26], [], [5, 10, 15, 20, 25], '', 'ΔV [ml] je l, 20 K',
    flaechen=[F(rechteck(1.2, 0, 3.4, fl), AUS, 0.45), F(rechteck(5.0, 0, 7.2, st), TIN, 0.4)],
    strecken=[S((3.4, st), (5.0, st), TIN, 2, gestrichelt=True), P((4.2, st), (4.2, fl), AUS, 5)],
    texte=[T(2.3, fl + 0.8, 'Ethanol 22 ml', AUS, 26), T(6.1, st + 1.2, 'Stahl 0.72 ml', TIN, 26), T(4.5, 12.5, 'läuft über', AUS, 28, 'start')]))
setze(d, 'Frage 3', graf([-3.5, 33], [-3.5, 36], [5, 10, 15, 20, 25, 30], [10, 20, 30], 'ΔT [K]', 'ΔV [l]',
    strecken=[S((0, 0), (30, 33), AUS, 5), S((25, 0), (25, 27.5), TIN, 3, gestrichelt=True), S((0, 27.5), (25, 27.5), TIN, 3, gestrichelt=True)],
    punkte=[pt(25, 27.5, AUS, '(25 K; 27.5 l)', (14, 30.5), 'middle')]))
blk = []
txt = []
for i in range(3):
    for j in range(2):
        x0, y0 = 1.0 + 2.6 * i, 1.5 + 2.6 * j
        blk.append(F(rechteck(x0, y0, x0 + 2.2, y0 + 2.2), AUS, 0.3 + 0.1 * j))
        txt.append(T(x0 + 1.1, y0 + 0.9, '66 ml', TIN, 26))
setze(d, 'Frage 4', skizze(0, 0, 10, flaechen=blk, texte=txt + [T(4.9, 0.7, '× 3: dreifaches Volumen', VOL, 26), T(4.9, 7.4, '× 2: doppelte Erwärmung', TEMP, 26), T(4.9, 8.6, '6 · 66 ml = 396 ml', AUS, 32)]))
speichere(n, d)

# ======================================================== Wasser und Meer (Kapitel 3)
n = 'p5-3-lp-kontrolle-meer'; d = lade(n)
r50 = 789 / (1 + 1.10e-3 * 30)
assert abs(r50 - 763.79) < 0.01
setze(d, 'Frage 1', skizze(0, 0, 10,
    strecken=umriss(1.0, 2.0, 4.0, 5.0, TIN, 4) + umriss(5.4, 2.0, 8.6, 5.2, AUS, 5),
    flaechen=[F(rechteck(1.0, 2.0, 4.0, 5.0), TIN, 0.25), F(rechteck(5.4, 2.0, 8.6, 5.2), AUS, 0.15)],
    texte=[T(2.5, 3.5, 'm', TIN, 34), T(7.0, 3.6, 'm', AUS, 34), T(2.5, 1.2, '20 °C: 789 kg/m³', TIN, 24), T(7.0, 1.2, '50 °C: 764 kg/m³', AUS, 24),
           T(5, 6.6, 'gleiche Masse, grösseres Volumen', TIN, 26), T(5, 7.6, 'kleinere Dichte', AUS, 30)]))
RHO = '(999.83952+16.945176*x-0.0079870401*x**2-0.000046170461*x**3+0.00000010556302*x**4-0.00000000028054253*x**5)/(1+0.01687985*x)'
def rho(t):
    return (999.83952 + 16.945176 * t - 7.9870401e-3 * t ** 2 - 46.170461e-6 * t ** 3 + 105.56302e-9 * t ** 4 - 280.54253e-12 * t ** 5) / (1 + 16.879850e-3 * t)
# Frage 2: kleinstes Volumen = grösste Dichte bei 4 °C; Achse beginnt bei 999.4 kg/m³ (Bruchzeichen)
setze(d, 'Frage 2', graf([-1.4, 12.6], [-0.08, 0.66], [2, 4, 6, 8, 10, 12], [[0.0, '999.4'], [0.1, '999.5'], [0.2, '999.6'], [0.3, '999.7'], [0.4, '999.8'], [0.5, '999.9'], [0.6, '1000']], 'ϑ [°C]', 'ρ [kg/m³]',
    kurven=[{"formel": RHO + '-999.4', "von": 0, "bis": 12, "farbe": AUS, "dicke": 5, "n": 200}],
    punkte=[pt(8, rho(8) - 999.4, TIN, '8 °C', (8.3, rho(8) - 999.4 + 0.04)), pt(0, rho(0) - 999.4, TIN, '0 °C', (0.3, rho(0) - 999.4 - 0.06)),
            pt(4, rho(4) - 999.4, AUS, '4 °C: grösste Dichte', (4.6, rho(4) - 999.4 + 0.045))],
    strecken=[S((-0.35, 0.025), (0.35, 0.055), TIN, 4), S((-0.35, 0.055), (0.35, 0.085), TIN, 4)],
    texte=[T(0.4, 0.05, 'Achse beginnt bei 999.4 kg/m³', TIN, 22, 'start')]))
h3 = 0.21e-3 * 700 * 1
assert abs(h3 - 0.147) < 1e-12
setze(d, 'Frage 3', skizze(0, 0, 10,
    flaechen=[F(rechteck(2, 1, 9, 8), TIN, 0.12), F(rechteck(2, 7.2, 9, 8), TEMP, 0.35)],
    strecken=[S((2, 8.0), (9, 8.0), TIN, 3, gestrichelt=True), S((2, 8.4), (9, 8.4), AUS, 4), P((1.4, 8.0), (1.4, 8.4), AUS, 4), S((2, 1), (9, 1), TIN, 4)],
    texte=[T(5.5, 7.4, 'obere 700 m: +1 K', TEMP, 24), T(5.5, 4.5, '4200 m tief: Tiefenwasser bleibt', TIN, 24), T(5.5, 9.0, 'Δh = 14.7 cm (übertrieben)', AUS, 28)]))
t4 = 0.06 / (0.21e-3 * 400)
assert abs(t4 - 0.7143) < 1e-4
setze(d, 'Frage 4', graf([-0.12, 1.05], [-0.9, 9.6], [0.2, 0.4, 0.6, 0.8, 1.0], [2, 4, 6, 8], 'ΔT [K]', 'Δh [cm]',
    strecken=[S((0, 0), (1.0, 8.4), AUS, 5), S((t4, 0), (t4, 6), TIN, 3, gestrichelt=True), S((0, 6), (t4, 6), TIN, 3, gestrichelt=True)],
    punkte=[pt(t4, 6, AUS, '(0.71 K; 6 cm)', (0.45, 6.7), 'middle')], texte=[T(0.6, 9.0, 'h₀ = 400 m', TIN, 26, 'start')]))
speichere(n, d)

# ======================================================== Gasgleichung (Kapitel 4)
n = 'p5-3-lp-kontrolle-gas'; d = lade(n)
p1 = 1.2 * (30 + K0) / (10 + K0)
assert abs(p1 - 1.2848) < 1e-4
setze(d, 'Frage 1', graf([-0.8, 9], [-35, 360], [], [100, 200, 300], '', 'T [K]',
    flaechen=[F(rechteck(1.5, 0, 3.5, 283.15), TIN, 0.3), F(rechteck(5.0, 0, 7.0, 303.15), TEMP, 0.4)],
    texte=[T(2.5, 300, '10 °C = 283 K', TIN, 24), T(6.0, 320, '30 °C = 303 K', TEMP, 24), T(4.3, 150, '+7 %', TEMP, 34), T(4.3, 345, 'p: 1.2 bar → 1.28 bar', DRU, 26)]))
pa = 2.6 * (35 + K0) / (5 + K0)
assert abs(pa - 2.8804) < 1e-4
setze(d, 'Frage 2', graf([-1, 9], [-0.3, 3.4], [], [1, 2, 3], '', 'p [bar]',
    flaechen=[F(rechteck(1.3, 0, 2.7, 1.0), TIN, 0.25), F(rechteck(1.3, 1.0, 2.7, 2.6), DRU, 0.4), F(rechteck(5.3, 0, 6.7, 1.0), TIN, 0.25), F(rechteck(5.3, 1.0, 6.7, pa), DRU, 0.4)],
    strecken=[P((7.0, 1.0), (7.0, pa), DRU, 4), P((7.0, pa), (7.0, 1.0), DRU, 4)],
    texte=[T(2.0, 0.5, 'Luftdruck', TIN, 22), T(6.0, 0.5, 'Luftdruck', TIN, 22), T(2.0, 2.8, '5 °C: 2.6 bar', DRU, 24), T(6.0, pa + 0.2, '35 °C: 2.88 bar', DRU, 24),
           T(7.25, 1.9, 'Manometer:', DRU, 22, 'start'), T(7.25, 1.6, '1.88 bar', DRU, 26, 'start')]))
import random
random.seed(5)
viel = [(1.4 + 2.9 * random.random(), 3.0 + 4.0 * random.random()) for _ in range(26)]
wenig = [(5.9 + 2.9 * random.random(), 3.0 + 4.0 * random.random()) for _ in range(14)]
setze(d, 'Frage 3', skizze(0, 0, 10,
    strecken=umriss(1.1, 2.7, 4.6, 7.3, TIN, 4) + umriss(5.6, 2.7, 9.1, 7.3, TIN, 4),
    punkte=[pt(x, y, TIN) for x, y in viel] + [pt(x, y, AUS) for x, y in wenig],
    texte=[T(2.85, 1.9, 'Abend', TIN, 28), T(7.35, 1.9, 'Morgen', AUS, 28), T(5, 8.4, 'weniger Gas: Gleichung gilt nicht', TIN, 26)]))
v2 = 3.0 * 6 * (16 + K0) / ((8 + K0) * 1.0)
assert abs(v2 - 18.512) < 1e-3
r1, r2 = 1.0, (v2 / 6) ** (1 / 3)
setze(d, 'Frage 4', skizze(0, 0, 10, kurven=kreis(2.6, 4.5, r1, TIN, 4) + kreis(6.8, 4.5, r2 * 1.0, VOL, 5),
    texte=[T(2.6, 2.6, 'Tiefe: 6 cm³', TIN, 26), T(2.6, 1.8, '3.0 bar; 8 °C', TIN, 22), T(6.8, 2.2, 'oben: 18.5 cm³', VOL, 28), T(6.8, 1.4, '1.0 bar; 16 °C', VOL, 22), T(5, 8.4, 'Volumen ×3.1', VOL, 30)]))
speichere(n, d)

# ======================================================== Spezialfälle (Kapitel 5)
n = 'p5-3-lp-kontrolle-spezialfaelle'; d = lade(n)
setze(d, 'Frage 1', graf([-40, 700], [-0.25, 2.6], [100, 200, 300, 400, 500, 600], [0.5, 1, 1.5, 2, 2.5], 'T [K]', 'p [bar]',
    strecken=[S((0, 0), (650, 650 / 293.15), DRU, 5), P((300, 300 / 293.15 + 0.12), (560, 560 / 293.15 + 0.12), TEMP, 4)],
    texte=[T(420, 1.95, 'erhitzen', TEMP, 26), T(60, 2.35, 'V konstant: p / T konstant', TIN, 26, 'start')]))
setze(d, 'Frage 2', graf([-15, 215], [-0.3, 4.2], [50, 100, 150, 200], [1, 2, 3, 4], 'V [cm³]', 'p [bar]',
    kurven=[{"formel": "100/x", "von": 30, "bis": 210, "farbe": AUS, "dicke": 5, "n": 300}],
    punkte=[pt(100, 1.0, TIN, '(100 cm³; 1.0 bar)', (110, 1.45)), pt(75, 100 / 75, AUS, '(75 cm³; 1.33 bar)', (85, 1.95))]))
setze(d, 'Frage 3', graf([-40, 700], [-0.6, 7], [100, 200, 300, 400, 500, 600], [2, 4, 6], 'T [K]', 'V [l]',
    strecken=[S((150, 1.5), (650, 6.5), VOL, 5), S((0, 0), (150, 1.5), VOL, 3, gestrichelt=True)],
    punkte=[pt(0, 0, TIN, '0 K', (20, 0.5))], texte=[T(60, 6.3, 'p konstant: V / T konstant', TIN, 26, 'start')]))
v4 = 2.5 * (87 + K0) / (27 + K0)
assert abs(v4 - 2.9998) < 1e-3
setze(d, 'Frage 4', graf([-40, 420], [-0.4, 4.2], [100, 200, 300, 400], [1, 2, 3, 4], 'T [K]', 'V [l]',
    strecken=[S((0, 0), (400, 2.5 * 400 / 300.15), VOL, 5)],
    punkte=[pt(300.15, 2.5, TIN, '(300 K; 2.5 l)', (290, 2.75), 'end'), pt(360.15, v4, VOL, '(360 K; 3.0 l)', (350, 3.35), 'end')]))
speichere(n, d)
print('Antwortbilder gesetzt')
