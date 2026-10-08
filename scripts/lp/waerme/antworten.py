"""Antwortbilder der Kontrollclips des Leitprogramms Wärme (07.10.2026).

  python3 scripts/lp/waerme/antworten.py      (nach build-clip-ton.py, vor anker.py und build-clips.py)

Jede Antwortszene «Frage 1» … «Frage 5» bekommt rechts ein Bild (x 1010, y 175, 760 x 760), das die
Antwort zeigt. Wiederholbar: alte Bilder (Kennung "antwort") werden zuerst entfernt. Szenen, die schon ein
eigenes Bild tragen (Kapitel 1, Frage 5; Kapitel 3, Frage 1: das Diagramm der Frage), bleiben ohne.
Alle Zahlen hier gerechnet (assert). Farben wie clips.py: 1 Bernstein Temperatur, 2 Orange zugeführte
Energie und Licht, 3 Grün Nutzen, 4 Rot Wärme, 5 Tinte Wasser, Körper, Achsen.
"""
import json
import math
import os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
BER, ORA, GRU, ROT, TIN = 1, 2, 3, 4, 5
CW, CEIS, LF, LV = 4182, 2100, 334000, 2256000


def fmt(v):
    return ('%g' % v).replace('-', '−')


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": list(xb), "ybereich": list(yb),
         "xteilung": [v if isinstance(v, list) else [v, fmt(v)] for v in xt] or [[1e9, '']],
         "yteilung": [v if isinstance(v, list) else [v, fmt(v)] for v in yt] or [[1e9, '']],
         "xname": xname, "yname": yname, "antwort": True}
    g.update(kw)
    return g


def skizze(x0=0, y0=0, span=10, **kw):
    return graf([x0, x0 + span], [y0, y0 + span], [], [], '', '', achsen=False, pfeile=False, **kw)


def r4(v):
    return round(v, 4)


def S(von, bis, farbe=TIN, **kw):
    d = {"von": [r4(von[0]), r4(von[1])], "bis": [r4(bis[0]), r4(bis[1])], "farbe": farbe}
    d.update(kw)
    return d


def P(von, bis, farbe, **kw):
    kw.setdefault('dicke', 6)
    return S(von, bis, farbe, pfeil=True, **kw)


def T(x, y, text, farbe=TIN, groesse=27, anker="middle", **kw):
    d = {"bei": [r4(x), r4(y)], "text": text, "farbe": farbe, "groesse": groesse, "anker": anker}
    d.update(kw)
    return d


def F(pts, farbe=TIN, deckung=0.15, **kw):
    d = {"punkte": [[r4(x), r4(y)] for x, y in pts], "farbe": farbe, "deckung": deckung}
    d.update(kw)
    return d


def rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def umriss(x0, y0, x1, y1, farbe=TIN, dicke=4, **kw):
    p = rechteck(x0, y0, x1, y1)
    return [S(p[i], p[(i + 1) % 4], farbe, dicke=dicke, **kw) for i in range(4)]


def becher(x0, x1, yb, yo, dicke=5, **kw):
    return [S((x0, yo), (x0, yb), dicke=dicke, **kw), S((x0, yb), (x1, yb), dicke=dicke, **kw), S((x1, yb), (x1, yo), dicke=dicke, **kw)]


def welle(x0, y0, x1, y1, farbe=ROT, n=5, amp=0.16):
    """Wellenlinie von (x0,y0) nach (x1,y1), Pfeil am Ende (Strahlung)."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    pts = []
    for i in range(n * 8 + 1):
        t = i / (n * 8)
        a = amp * math.sin(2 * math.pi * n * t)
        pts.append((x0 + (x1 - x0) * t - uy * a, y0 + (y1 - y0) * t + ux * a))
    st = [S(pts[i], pts[i + 1], farbe, dicke=4) for i in range(len(pts) - 1)]
    st[-1]['pfeil'] = True
    return st


def balken(eintraege, ymax, yt, yname, breite=1.2, wert=True, **kw):
    """eintraege: (Etikett, Wert, Farbe, Wertetext) — Säulen bei x = 1, 2.5, 4, …"""
    fl, tx = [], []
    for i, (et, v, fa, vt) in enumerate(eintraege):
        x = 1 + 1.6 * i
        fl.append(F(rechteck(x - breite / 2, 0, x + breite / 2, v), fa, 0.55))
        tx.append(T(x, -0.075 * ymax, et, TIN, 24))
        if wert and vt:
            tx.append(T(x, v + 0.04 * ymax, vt, fa, 26))
    n = len(eintraege)
    g = graf((-0.2 - 0.12 * max(len(fmt(v)) for v in yt), 1 + 1.6 * (n - 1) + 1.0), (-0.14 * ymax, 1.12 * ymax), [], yt, '', yname, **kw)
    g['flaechen'] = fl + g.get('flaechen', [])
    g['texte'] = tx + g.get('texte', [])
    return g


def lade(n):
    d = json.load(open(R + n + '.json'))
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]
    return d


def setze(d, szene, el):
    for s in d['szenen']:
        if s['name'] == szene:
            assert not any(e['typ'] in ('graf', 'bild') for e in s['elemente']), szene
            s['elemente'].append(el)
            return
    raise KeyError(szene)


def speichere(n, d):
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(n, 'gespeichert')


# ======================================================== Kapitel 1: Wärme und Temperatur
n = 'p5-2-lp-kontrolle-waerme'; d = lade(n)
# F1: Wärme fliesst vom heissen zum kalten Körper
setze(d, 'Frage 1', skizze(
    flaechen=[F(rechteck(0.8, 3.5, 3.8, 6.5), BER, 0.3), F(rechteck(6.2, 3.5, 9.2, 6.5), TIN, 0.15)],
    strecken=umriss(0.8, 3.5, 3.8, 6.5) + umriss(6.2, 3.5, 9.2, 6.5) + [P((4.1, 5.0), (5.9, 5.0), ROT, dicke=9)],
    texte=[T(2.3, 7.1, 'heiss', BER, 28), T(7.7, 7.1, 'kalt', TIN, 28), T(5.0, 5.6, 'Wärme', ROT, 28),
           T(2.3, 4.85, 'innere', TIN, 23), T(2.3, 4.2, 'Energie', TIN, 23), T(7.7, 4.85, 'innere', TIN, 23), T(7.7, 4.2, 'Energie', TIN, 23),
           T(5.0, 2.4, 'Wärme fliesst nur,', ROT, 26), T(5.0, 1.7, 'solange ein Temperaturunterschied besteht', ROT, 22)]))
# F2: Thermometer im Tee: beide Temperaturen bis zum Gleichgewicht (Modell, Zeitkonstante 4 s)
setze(d, 'Frage 2', graf((-3, 33), (-10, 92), [10, 20, 30], [20, 40, 60, 80], 't [s]', 'ϑ [°C]',
                         kurven=[{"formel": '69+1*exp(-x/4)', "von": 0, "bis": 30, "farbe": BER, "dicke": 5, "n": 100},
                                 {"formel": '69-49*exp(-x/4)', "von": 0, "bis": 30, "farbe": TIN, "dicke": 5, "n": 100}],
                         texte=[T(1, 80, 'Tee', BER, 26, 'start'), T(2.5, 26, 'Thermometer', TIN, 26, 'start'), T(29, 59, 'gleich warm: jetzt ablesen', BER, 24, 'end')]))
# F3: Granit, Q wächst mit ΔT bis 23.7 kJ
q3 = 2.5 * 790 * 12
assert q3 == 23700
setze(d, 'Frage 3', graf((-1.5, 15), (-3.5, 30), [4, 8, 12], [10, 20], 'ΔT [K]', 'Q [kJ]',
                         strecken=[S((0, 0), (12, 23.7), ROT, dicke=5), S((12, 0), (12, 23.7), TIN, dicke=2, gestrichelt=True), S((0, 23.7), (12, 23.7), TIN, dicke=2, gestrichelt=True)],
                         punkte=[{"x": 12, "y": 23.7, "farbe": ROT}], texte=[T(11.6, 26, '(12 K; 23.7 kJ)', ROT, 26, 'end'), T(6, 20, 'Granit: 2.5 kg', TIN, 24)]))
# F4: proportional: (8 K; 12 kJ) → (20 K; 30 kJ)
assert 12 / 8 * 20 == 30
setze(d, 'Frage 4', graf((-3, 24), (-4, 37), [8, 20], [12, 30], 'ΔT [K]', 'Q [kJ]',
                         strecken=[S((0, 0), (20, 30), ROT, dicke=5), S((8, 0), (8, 12), TIN, dicke=2, gestrichelt=True), S((0, 12), (8, 12), TIN, dicke=2, gestrichelt=True),
                                   S((20, 0), (20, 30), TIN, dicke=2, gestrichelt=True), S((0, 30), (20, 30), TIN, dicke=2, gestrichelt=True)],
                         punkte=[{"x": 8, "y": 12, "farbe": ROT}, {"x": 20, "y": 30, "farbe": ROT}],
                         texte=[T(8.6, 10.2, '(8 K; 12 kJ)', ROT, 25, 'start'), T(19, 32.5, '(20 K; 30 kJ)', ROT, 25, 'end'), T(13, 4, '1.5 kJ je Kelvin', TIN, 24)]))
speichere(n, d)

# ======================================================== Kapitel 2: Wärmebilanz
n = 'p5-2-lp-kontrolle-bilanz'; d = lade(n)


def hebel(t_kalt, t_heiss, t_m, gk, gh, ek, eh, xt):
    """Temperaturachse mit kalt, heiss und Mischtemperatur; Gewichte (m bzw. m · c) als Säulen über den Enden,
    ihre Werte unter der Achse."""
    sp = t_heiss - t_kalt
    hk, hh = 6 * gk / max(gk, gh), 6 * gh / max(gk, gh)
    return graf((max(t_kalt - 0.15 * sp, min(4, t_kalt - 0.1 * sp)), t_heiss + 0.15 * sp), (-4.2, 9.5), xt, [], 'ϑ [°C]', '', achsen=True,
                flaechen=[F(rechteck(t_kalt - 0.035 * sp, 0, t_kalt + 0.035 * sp, hk), TIN, 0.5),
                          F(rechteck(t_heiss - 0.035 * sp, 0, t_heiss + 0.035 * sp, hh), BER, 0.5)],
                strecken=[S((t_m, -0.4), (t_m, 8.0), BER, dicke=5)],
                texte=[T(t_kalt - 0.04 * sp, -2.6, ek, TIN, 24, 'start'), T(t_heiss + 0.04 * sp, -2.6, eh, BER, 24, 'end'), T(t_m + 0.02 * sp, 8.5, 'Mischung %s %s °C' % ('=' if abs(t_m - round(t_m, 1)) < 1e-9 else '≈', fmt(round(t_m, 1))), BER, 28, 'start')])


tm1 = (0.2 * 70 + 0.6 * 10) / 0.8
assert tm1 == 25
setze(d, 'Frage 1', hebel(10, 70, tm1, 0.6, 0.2, '0.6 kg', '0.2 kg', [10, 25, 40, 55, 70]))
mcn, mct = 0.005 * 450, 0.25 * CW
tm2 = (mcn * 300 + mct * 60) / (mcn + mct)
assert abs(mcn - 2.25) < 1e-12 and abs(mct - 1045.5) < 1e-9 and round(tm2, 1) == 60.5
setze(d, 'Frage 2', hebel(60, 300, tm2, mct, mcn, 'Tee: 1046 J/K', 'Nagel: 2.3 J/K', [60, 120, 180, 240, 300]))
# F3: zwei verschieden grosse Körper, gleiche Temperatur
setze(d, 'Frage 3', skizze(
    flaechen=[F(rechteck(0.8, 2.0, 2.8, 4.0), BER, 0.35), F(rechteck(4.2, 2.0, 9.2, 7.0), BER, 0.35)],
    strecken=umriss(0.8, 2.0, 2.8, 4.0) + umriss(4.2, 2.0, 9.2, 7.0),
    texte=[T(1.8, 4.6, '40 °C', BER, 30), T(6.7, 7.6, '40 °C', BER, 30), T(1.8, 1.3, 'wenig', TIN, 24), T(6.7, 1.3, 'viel', TIN, 24),
           T(5.0, 0.55, 'innere Energie', TIN, 24), T(5.0, 9.0, 'gleiche Temperatur: kein Wärmefluss mehr', ROT, 24)]))
mca, mcw = 0.4 * 385, 0.6 * CW
tm4 = (mca * 150 + mcw * 18) / (mca + mcw)
assert abs(mca - 154) < 1e-9 and round(mcw) == 2509 and round(tm4, 1) == 25.6
setze(d, 'Frage 4', hebel(18, 150, tm4, mcw, mca, 'Wasser: 2509 J/K', 'Kupfer: 154 J/K', [18, 50, 100, 150]))
# F5: Wärme an Gefäss und Umgebung
setze(d, 'Frage 5', skizze(
    flaechen=[F(rechteck(3.1, 3.1, 6.9, 6.2), TIN, 0.15)],
    strecken=becher(3.0, 7.0, 3.0, 7.0, dicke=6) + [P((3.6, 4.6), (2.0, 4.6), ROT), P((6.4, 4.6), (8.0, 4.6), ROT), P((5.0, 6.4), (5.0, 8.4), ROT), P((5.0, 3.4), (5.0, 1.6), ROT)],
    texte=[T(5.0, 4.6, 'Mischung', TIN, 24), T(1.6, 5.3, 'Umgebung', ROT, 24), T(8.4, 5.3, 'Umgebung', ROT, 24), T(5.0, 0.9, 'Gefäss', ROT, 24),
           T(5.0, 9.0, 'Thermometer, Luft', ROT, 24)]))
speichere(n, d)

# ======================================================== Kapitel 3: Latente Wärme
n = 'p5-2-lp-kontrolle-heizkurve'; d = lade(n)
q_erw, q_v = 0.15 * CW * 100, 0.15 * LV
assert round(q_erw / 1000, 1) == 62.7 and round(q_v / 1000) == 338
setze(d, 'Frage 2', balken([('0 → 100 °C', q_erw / 1000, ROT, '62.7 kJ'), ('Verdampfen', q_v / 1000, ROT, '338 kJ')], 350, [100, 200, 300], 'Q [kJ]',
                         texte=[T(2.6, 300, 'bei 100 °C', BER, 24)]))
q_s = 0.05 * LF
assert round(q_s / 1000, 1) == 16.7
setze(d, 'Frage 3', skizze(
    flaechen=[F(rechteck(1.5, 1.5, 3.5, 3.5), ROT, 0.3), F(rechteck(6.5, 1.5, 8.5, 3.5), ROT, 0.3), F(rechteck(6.5, 3.5, 8.5, 8.0), ROT, 0.6)],
    strecken=umriss(1.5, 1.5, 3.5, 8.0, dicke=2, gestrichelt=True) + umriss(6.5, 1.5, 8.5, 8.0, dicke=2),
    texte=[T(2.5, 0.8, '50 g Wasser', TIN, 24), T(7.5, 0.8, '50 g Eis', TIN, 24), T(2.5, 2.5, 'erwärmen', ROT, 22), T(7.5, 2.5, 'erwärmen', ROT, 22),
           T(7.5, 6.0, 'schmelzen', ROT, 24), T(7.5, 5.3, '16.7 kJ', ROT, 26), T(5.0, 9.2, 'Eis nimmt mehr Wärme auf', ROT, 26)]))
# F4: Erstarren gibt 334 kJ ab, bei 0 °C
setze(d, 'Frage 4', skizze(
    flaechen=[F(rechteck(3.0, 3.0, 7.0, 6.5), TIN, 0.3)],
    strecken=umriss(3.0, 3.0, 7.0, 6.5) + [P((7.2, 4.75), (9.4, 4.75), ROT, dicke=9)],
    texte=[T(5.0, 5.2, '0.5 kg Wasser', TIN, 26), T(5.0, 4.3, '→ Eis', TIN, 26), T(8.3, 5.4, '167 kJ', ROT, 28), T(5.0, 7.3, 'bleibt bei 0 °C', BER, 28),
           T(5.0, 1.8, 'gibt ab, was das Schmelzen gekostet hat', ROT, 22)]))
q5a, q5b = 0.3 * CEIS * 8, 0.3 * LF
assert round(q5a / 1000, 2) == 5.04 and round(q5b / 1000, 1) == 100.2 and round(q5b / q5a) == 20
setze(d, 'Frage 5', balken([('−8 → 0 °C', q5a / 1000, ROT, '5.0 kJ'), ('Schmelzen', q5b / 1000, ROT, '100 kJ')], 105, [25, 50, 75, 100], 'Q [kJ]'))
speichere(n, d)

# ======================================================== Kapitel 4: Heizwert und Wirkungsgrad
n = 'p5-2-lp-kontrolle-heizwert'; d = lade(n)
assert 2 * 15 == 30 and 0.75 * 30 == 22.5
setze(d, 'Frage 1', balken([('zugeführt', 30, ORA, '30 MJ'), ('Nutzwärme', 22.5, GRU, '22.5 MJ'), ('Verlust', 7.5, ROT, '7.5 MJ')], 32, [10, 20, 30], 'E [MJ]'))
assert 54 / 3.6 == 15
setze(d, 'Frage 2', graf((-2, 19), (-8, 66), [5, 10, 15], [18, 36, 54], 'E [kWh]', 'E [MJ]',
                         strecken=[S((0, 0), (17.5, 63), ORA, dicke=5), S((15, 0), (15, 54), TIN, dicke=2, gestrichelt=True), S((0, 54), (15, 54), TIN, dicke=2, gestrichelt=True)],
                         punkte=[{"x": 15, "y": 54, "farbe": ORA}], texte=[T(14.4, 58.5, '(15 kWh; 54 MJ)', ORA, 26, 'end'), T(11, 14, '1 kWh = 3.6 MJ', TIN, 26)]))
q3 = 1.2 * CW * 80
t3 = q3 / (0.8 * 2000)
assert round(q3 / 1000) == 401 and round(t3) == 251 and round(t3 / 60, 1) == 4.2
setze(d, 'Frage 3', balken([('Strom', 2000, ORA, '2000 W'), ('ins Wasser', 1600, GRU, '1600 W')], 2100, [500, 1000, 1500, 2000], 'P [W]',
                         texte=[T(2.6, 1900, '401 kJ ÷ 1600 W ≈ 251 s', TIN, 24)]))
setze(d, 'Frage 4', skizze(
    flaechen=[F(rechteck(2.5, 1.5, 6.0, 6.5), TIN, 0.12)],
    strecken=umriss(2.5, 1.5, 6.0, 6.5) + [S((4.2, 6.5), (4.2, 8.5), TIN, dicke=6), S((5.0, 6.5), (5.0, 8.5), TIN, dicke=6),
                                           P((0.3, 4.0), (2.4, 4.0), ORA, dicke=8), P((6.1, 3.0), (8.8, 3.0), GRU, dicke=8),
                                           P((4.6, 7.0), (4.6, 9.6), ROT, dicke=6), P((6.1, 5.5), (8.2, 6.5), ROT, dicke=5)],
    texte=[T(1.3, 4.6, 'Brennstoff', ORA, 22), T(7.5, 2.4, 'Nutzwärme', GRU, 24), T(5.3, 9.4, 'Abgas', ROT, 24, 'start'), T(8.3, 7.1, 'Umgebung', ROT, 24, 'end'),
           T(4.25, 4.0, 'Kessel', TIN, 26)]))
m5 = 10 * 0.84
assert abs(m5 - 8.4) < 1e-12 and round(m5 * 42.6) == 358
setze(d, 'Frage 5', balken([('10 l → 8.4 kg', m5 * 42.6, ORA, '358 MJ')], 400, [100, 200, 300, 400], 'E [MJ]', breite=1.4,
                         texte=[T(1.0, 120, '8.4 kg · 42.6 MJ/kg', TIN, 22)]))
speichere(n, d)

# ======================================================== Kapitel 5: Energiesysteme
n = 'p5-2-lp-kontrolle-energiesysteme'; d = lade(n)
setze(d, 'Frage 1', skizze(
    flaechen=[F(rechteck(3.5, 3.0, 6.5, 6.5), TIN, 0.12)],
    strecken=umriss(3.5, 3.0, 6.5, 6.5) + [P((0.4, 4.0), (3.3, 4.0), TIN, dicke=7), P((5.0, 9.4), (5.0, 6.7), ORA, dicke=7), P((6.7, 4.75), (9.6, 4.75), ROT, dicke=10)],
    texte=[T(1.8, 4.6, 'Umgebung', TIN, 24), T(5.3, 8.3, 'Strom', ORA, 26, 'start'), T(8.2, 5.5, 'Heizwärme', ROT, 24),
           T(5.0, 4.75, 'Technik', TIN, 26), T(5.0, 1.5, 'erneuerbar: allenfalls die Umgebungswärme', TIN, 21)]))
e2 = 0.5 * 6 * 1200
assert abs(e2 - 3600) < 1e-9
setze(d, 'Frage 2', balken([('Licht', 7200, ORA, '7200 kWh'), ('Wärme', e2, GRU, '3600 kWh')], 7600, [2000, 4000, 6000], 'E [kWh]',
                         texte=[T(2.6, 6600, '6 m² · 1200 kWh/m²', TIN, 22), T(2.6, 5900, '× 0.5', GRU, 24)]))
# F3: Saisonverlauf: PV Sommer, Speichersee/Wind Winter (qualitativ, Monate)
pv = 'max(0,0.95-0.8*(cos((x-0.5)*pi/6)+1)/2*1.15)'
setze(d, 'Frage 3', graf((-0.6, 12.6), (-0.16, 1.15), [[0.5, 'Jan'], [3.5, 'Apr'], [6.5, 'Jul'], [9.5, 'Okt']], [], 'Monat', 'relativ',
                         kurven=[{"formel": '0.5-0.4*cos((x-0.5)*pi/6)', "von": 0, "bis": 12, "farbe": GRU, "dicke": 5, "n": 200},
                                 {"formel": '0.55+0.3*cos((x-0.5)*pi/6)', "von": 0, "bis": 12, "farbe": TIN, "dicke": 5, "n": 200}],
                         texte=[T(6.5, 1.0, 'Photovoltaik', GRU, 26), T(0.6, 0.97, 'Wind', TIN, 26, 'start')]))
e4 = 1000 * 9.81 * 200
assert round(e4 / 1e6, 2) == 1.96 and round(e4 / 3.6e6, 3) == 0.545
setze(d, 'Frage 4', skizze(
    flaechen=[F(rechteck(1.0, 8.0, 3.0, 9.4), TIN, 0.4), F(rechteck(1.0, 1.0, 9.0, 1.6), TIN, 0.3)],
    strecken=umriss(1.0, 8.0, 3.0, 9.4) + [P((2.0, 7.8), (2.0, 1.8), TIN, dicke=6), S((3.3, 8.0), (4.3, 8.0), TIN, dicke=2, gestrichelt=True), S((3.3, 1.6), (4.3, 1.6), TIN, dicke=2, gestrichelt=True)],
    texte=[T(2.0, 9.9, '1 m³ = 1000 kg', TIN, 24), T(2.3, 4.8, '200 m', TIN, 28, 'start'), T(6.8, 5.6, '1.96 MJ', GRU, 32), T(6.8, 4.6, '≈ 0.545 kWh', GRU, 32)]))
setze(d, 'Frage 5', balken([('Wind davor', 100, ORA, '100 kWh'), ('Strom', 45, GRU, '45 kWh'), ('bleibt im Wind', 55, TIN, '55 kWh')], 110, [25, 50, 75, 100], 'E [kWh]',
                         texte=[T(2.6, 107, 'Luft strömt langsamer weiter', TIN, 22)]))
speichere(n, d)

# ======================================================== Kapitel 6: Wärmetransport
n = 'p5-2-lp-kontrolle-transport'; d = lade(n)
setze(d, 'Frage 1', skizze(
    flaechen=[F([(0.6, 4.2), (4.0, 4.2), (4.0, 6.2), (0.6, 6.2)], TIN, 0.2), F(rechteck(1.6, 2.0, 2.6, 4.2), TIN, 0.2)],
    strecken=umriss(0.6, 4.2, 4.0, 6.2) + [P((4.3, 5.4), (7.0, 5.4), ROT, dicke=6), P((4.3, 4.9), (7.0, 4.1), ROT, dicke=6), P((4.3, 5.9), (7.0, 6.7), ROT, dicke=6)],
    texte=[T(2.3, 5.2, 'Föhn', TIN, 26), T(8.4, 5.4, 'Haare', TIN, 26), T(5.6, 8.0, 'warme Luft strömt', ROT, 26), T(5.0, 1.0, 'Konvektion', ROT, 32)]))
kreise = [(x, y) for x in (1.5, 3.0, 4.5, 6.0, 7.5) for y in (3.0, 4.5, 6.0)]
setze(d, 'Frage 2', skizze(
    flaechen=[F(rechteck(0.6, 2.1, 8.4, 6.9), TIN, 0.08)],
    strecken=umriss(0.6, 2.1, 8.4, 6.9) + [S((x, 2.1), (x, 6.9), TIN, dicke=2) for x in (2.25, 3.75, 5.25, 6.75)]
             + [S((0.6, y), (8.4, y), TIN, dicke=2) for y in (3.75, 5.25)] + [P((8.6, 4.5), (9.5, 4.5), ROT, dicke=4)],
    texte=[T(4.5, 7.6, 'Luft in kleinen Kammern', TIN, 26), T(4.5, 1.2, 'Leitung und Konvektion gebremst', ROT, 24), T(9.05, 5.2, 'wenig', ROT, 22)]))
setze(d, 'Frage 3', skizze(
    flaechen=[F(rechteck(0.8, 2.0, 2.4, 6.5), BER, 0.3), F(rechteck(7.2, 3.6, 9.4, 5.2), TIN, 0.4)],
    strecken=umriss(0.8, 2.0, 2.4, 6.5) + umriss(7.2, 3.6, 9.4, 5.2) + welle(2.7, 4.4, 6.9, 4.4),
    texte=[T(1.6, 7.0, 'Mensch, rund 30 °C', BER, 24), T(8.3, 3.0, 'Kamera', TIN, 24), T(4.8, 5.4, 'Wärmestrahlung', ROT, 26), T(5.0, 1.0, 'auch im Dunkeln: jeder Körper strahlt', ROT, 22)]))
setze(d, 'Frage 4', balken([('Kupfer', 400, ROT, '400'), ('Edelstahl', 15, ROT, '15')], 420, [100, 200, 300, 400], 'λ [W/(m·K)]'))
setze(d, 'Frage 5', skizze(
    flaechen=[F(rechteck(2.5, 3.5, 7.5, 5.5), BER, 0.3)],
    strecken=[S((1.8, 6.4), (8.2, 6.4), ORA, dicke=6)] + welle(3.2, 5.0, 3.2, 6.2, n=3) + welle(6.8, 6.2, 6.8, 5.0, n=3),
    texte=[T(5.0, 4.5, 'Körper', TIN, 26), T(5.0, 7.0, 'glänzende Folie', ORA, 26), T(5.0, 2.2, 'Wärmestrahlung zurück zum Körper', ROT, 24)]))
speichere(n, d)

# ======================================================== Kapitel 7: Treibhauseffekt
n = 'p5-2-lp-kontrolle-treibhaus'; d = lade(n)
L10 = math.log(10)


def LX(lam):
    """x-Koordinate im Spektrum: log10(λ/µm) + 1.2 (y-Achse links von 0.1 µm)"""
    return math.log10(lam) + 1.2


def planck(T_, K):
    return 'exp(-5*(x-1.2)*%.6f)/(exp(14388/(exp((x-1.2)*%.6f)*%d))-1)*%.6g' % (L10, L10, T_, K)


XT = [[LX(0.1), '0.1'], [LX(0.5), '0.5'], [LX(1), '1'], [LX(10), '10'], [LX(100), '100']]
setze(d, 'Frage 1', graf((-0.36, 3.32), (-0.22, 1.2), XT, [], 'λ [µm]', 'relativ',
                         kurven=[{"formel": planck(5800, 4.430951), "von": 0.2, "bis": 3.2, "farbe": ORA, "dicke": 5, "n": 400},
                                 {"formel": planck(288, 14678255.42), "von": 0.2, "bis": 3.2, "farbe": ROT, "dicke": 5, "n": 400}],
                         flaechen=[F(rechteck(LX(0.38), 0, LX(0.78), 1.12), ORA, 0.12)],
                         texte=[T(LX(0.5), 1.05, 'Sonne 5800 K', ORA, 24), T(LX(10), 1.05, 'Erde 288 K', ROT, 24), T(LX(0.55), -0.17, 'sichtbar', ORA, 20)]))
gase = [('N₂', 78, TIN), ('O₂', 21, TIN), ('H₂O', 1, ROT), ('CO₂', 0.04, ROT)]
setze(d, 'Frage 2', balken([(a, v, f, '%g %%' % v if v >= 1 else '0.04 %') for a, v, f in gase], 85, [20, 40, 60, 80], 'Anteil [%]', breite=1.1,
                         texte=[T(5.0, 50, 'nehmen Infrarot auf', ROT, 24)]))
p3 = 5.67e-8 * 303.15 ** 4
assert round(p3) == 479
setze(d, 'Frage 3', graf((-15, 47), (-60, 560), [0, 15, 30], [100, 200, 300, 400, 500], 'ϑ [°C]', 'P/A [W/m²]',
                         kurven=[{"formel": '5.67e-8*(x+273.15)**4', "von": -10, "bis": 40, "farbe": ROT, "dicke": 5, "n": 100}],
                         strecken=[S((30, 0), (30, p3), TIN, dicke=2, gestrichelt=True), S((-10, p3), (30, p3), TIN, dicke=2, gestrichelt=True)],
                         punkte=[{"x": 30, "y": round(p3, 1), "farbe": ROT}], texte=[T(29, 515, '(30 °C; 479 W/m²)', ROT, 25, 'end'), T(10, 150, 'T in Kelvin einsetzen', TIN, 24)]))
setze(d, 'Frage 4', skizze(
    flaechen=[F(rechteck(0.3, 5.2, 9.7, 6.8), TIN, 0.12)],
    strecken=[S((0.3, 1.5), (9.7, 1.5), TIN, dicke=6)] + welle(5.0, 1.8, 5.0, 5.6) + welle(5.0, 6.4, 5.0, 9.4) + welle(3.6, 5.6, 3.6, 1.9)
             + welle(5.4, 6.0, 8.6, 6.0, n=4) + welle(4.6, 6.0, 1.4, 6.0, n=4),
    texte=[T(8.0, 7.2, 'Treibhausgase', TIN, 24), T(3.2, 3.5, 'zurück', ROT, 24, 'end'), T(5.5, 9.4, 'hinaus', ROT, 24, 'start'), T(5.0, 0.8, 'Boden', TIN, 24)]))
setze(d, 'Frage 5', skizze(
    flaechen=[F(rechteck(5.6, 6.4, 9.4, 7.8), TIN, 0.3)],
    strecken=[S((0.3, 1.5), (4.7, 1.5), TIN, dicke=6), S((5.3, 1.5), (9.7, 1.5), TIN, dicke=6), S((5.0, 1.0), (5.0, 9.5), TIN, dicke=2, gestrichelt=True)]
             + welle(2.5, 1.8, 2.5, 9.2) + welle(7.0, 1.8, 7.0, 6.2) + welle(8.0, 6.2, 8.0, 1.9),
    texte=[T(2.5, 9.6, 'klar', TIN, 26), T(7.5, 9.0, 'Wolken', TIN, 26), T(2.5, 0.8, 'kühlt stark ab', ROT, 22), T(7.5, 0.8, 'Gegenstrahlung', ROT, 22)]))
speichere(n, d)
