"""Antwortbilder der Energie-Kontrollclips p4-3-lp-kontrolle-* (06.10.2026).

Jede Antwortszene («Frage 1» … «Frage 5») bekommt rechts ein Bild (x 1010, y 175,
760 x 760), das die Antwort zeigt: Energiesäulen als Flächen, Kraft-Weg- und
Leistung-Zeit-Diagramme mit der Fläche als Arbeit, Kurven E(v), P(T), Bahnprofile.
Kennung "antwort": true — ein zweiter Lauf entfernt die alten Bilder zuerst.

Farben wie im Leitprogramm (README scripts/lp/energie/): 1 Bernstein = Lageenergie,
3 Grün = Bewegungsenergie und v, 4 Rot = Wärme/Reibung/Wärmestrahlung. Blau (Kräfte,
zugeführte Energie) und Violett (Arbeit als Fläche) kennt das Clip-Theme nicht:
Kräfte in Tinte (5), Arbeit und zugeführte Energie in Orange (2).
"""
import os
import json, math

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
G_ = 9.81
SIG = 5.67e-8
KEINE = [[1e6, ""]]          # leere Teilung (eine leere Liste gäbe die ganzen Zahlen)


def fmt(v):
    return ('%g' % v).replace('-', '−')


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": xb, "ybereich": yb,
         "xteilung": [[v, fmt(v)] if not isinstance(v, list) else v for v in xt] or KEINE,
         "yteilung": [[v, fmt(v)] if not isinstance(v, list) else v for v in yt] or KEINE,
         "xname": xname, "yname": yname}
    g.update(kw)
    return g


def bild(xb, yb, **kw):
    """Zeichnung ohne Achsen (Säulen, Kräfteplan, Seitenansicht)."""
    return graf(xb, yb, [], [], '', '', achsen=False, pfeile=False, **kw)


def balken(x0, x1, y0, y1, farbe, beschriftung=None, bei=None, deckung=0.3):
    """Säule als Fläche mit Rand: (flaechen, strecken)."""
    fl = {"punkte": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], "farbe": farbe, "deckung": deckung}
    if beschriftung:
        fl["beschriftung"] = beschriftung
        if bei:
            fl["beschriftung_bei"] = bei
    rand = [{"von": a, "bis": b, "farbe": farbe, "dicke": 3}
            for a, b in [([x0, y0], [x0, y1]), ([x0, y1], [x1, y1]), ([x1, y1], [x1, y0])]]
    return [fl], rand


def saeulen(*teile):
    fl, st = [], []
    for f, s in teile:
        fl += f; st += s
    return fl, st


def T(bei, text, farbe=5, groesse=27, anker="middle", **kw):
    t = {"bei": bei, "text": text, "farbe": farbe, "groesse": groesse, "anker": anker}
    t.update(kw)
    return t


def setze(d, szene, el):
    for s in d['szenen']:
        if s['name'] == szene:
            s['elemente'].append(el)
            return
    raise KeyError(szene)


def lade(n):
    return json.load(open(R + n + '.json'))


def speichere(n, d):
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def formelgroesse(d, szene, g):
    """Neben dem Antwortbild hat die Formel links nur 820 px."""
    for s_ in d['szenen']:
        if s_['name'] == szene:
            for e in s_['elemente']:
                if e['typ'] == 'formel':
                    e['groesse'] = g


def ohne_alte_antworten(d):
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]


def A(el):
    el['antwort'] = True
    return el


# ======================================================== Arbeit
d = lade('p4-3-lp-kontrolle-arbeit'); ohne_alte_antworten(d)
# F1: F-s-Diagramm, Rechteck 50 N x 8 m = 400 J
assert 50 * 8 == 400
setze(d, 'Frage 1', A(graf([-1, 10], [-8, 70], [2, 4, 6, 8], [20, 40, 60], 's [m]', 'F [N]',
    flaechen=[{"punkte": [[0, 0], [8, 0], [8, 50], [0, 50]], "farbe": 2, "deckung": 0.25,
               "beschriftung": "W = 400 J", "beschriftung_bei": [4, 27]}],
    strecken=[{"von": [0, 50], "bis": [8, 50], "farbe": 5, "dicke": 5,
               "beschriftung": "F = 50 N", "beschriftung_bei": [4, 54], "anker": "middle"},
              {"von": [8, 0], "bis": [8, 50], "farbe": 2, "dicke": 3}],
    texte=[T([4, 13], "50 N · 8 m", 2, 27)])))
# F2: Kräfteplan 1:1, 100 N unter 60°, Anteil in Wegrichtung 50 N
fx, fy = 100 * math.cos(math.radians(60)), 100 * math.sin(math.radians(60))
assert abs(fx - 50) < 1e-9 and abs(fx * 10 - 500) < 1e-6
setze(d, 'Frage 2', A(bild([-25, 115], [-35, 105],
    flaechen=[{"punkte": [[-20, 0], [0, 0], [0, 20], [-20, 20]], "farbe": 5, "deckung": 0.25}],
    strecken=[{"von": [-25, 0], "bis": [115, 0], "farbe": 5, "dicke": 4},
              {"von": [50, 10], "bis": [50, round(10 + fy, 2)], "farbe": 5, "gestrichelt": True},
              {"von": [0, 10], "bis": [50, round(10 + fy, 2)], "farbe": 5, "pfeil": True, "dicke": 6,
               "beschriftung": "F = 100 N", "beschriftung_bei": [19, 60], "anker": "end"},
              {"von": [0, 10], "bis": [50, 10], "farbe": 2, "pfeil": True, "dicke": 6},
              {"von": [0, -14], "bis": [55, -14], "farbe": 5, "pfeil": True, "dicke": 4,
               "beschriftung": "Weg s = 10 m", "beschriftung_bei": [60, -17], "anker": "start"}],
    texte=[T([13, 13.5], "60°", 5, 26, "start"),
           T([55, 33], "Anteil in Wegrichtung:", 2, 26, "start"),
           T([55, 15], "100 N · cos 60° = 50 N", 2, 27, "start")])))
# F3: Halten: Weg null, keine Fläche; Hochstemmen zum Vergleich gestrichelt
setze(d, 'Frage 3', A(graf([-0.25, 2.25], [-0.25, 2.25], [], [], 's [m]', 'F [N]',
    flaechen=[{"punkte": [[0, 0], [0.8, 0], [0.8, 1.5], [0, 1.5]], "farbe": 2, "deckung": 0.10}],
    strecken=[{"von": [0, 1.5], "bis": [0.8, 1.5], "farbe": 2, "gestrichelt": True},
              {"von": [0.8, 0], "bis": [0.8, 1.5], "farbe": 2, "gestrichelt": True}],
    punkte=[{"x": 0, "y": 1.5, "farbe": 4, "beschriftung": "Haltekraft F", "beschriftung_bei": [0.08, 1.62]}],
    texte=[T([0.4, 0.85], "Hochstemmen:", 2, 24), T([0.4, 0.62], "W = F · s", 2, 24),
           T([1.0, 1.2], "Halten: s = 0", 4, 28, "start"),
           T([1.0, 1.0], "keine Fläche, W = 0", 4, 28, "start")])))
# F4: Föhn — Energiesäulen: elektrisch hinein = Wärme + Bewegung der Luft
fl, st = saeulen(balken(0.5, 2.9, 1, 8, 2, "elektrisch", [1.7, 4.5]),
                 balken(5.1, 7.5, 1, 7, 4, "Wärme", [6.3, 4]),
                 balken(5.1, 7.5, 7, 8, 3))
setze(d, 'Frage 4', A(bild([0, 10], [0, 10], flaechen=fl,
    strecken=st + [{"von": [0.4, 1], "bis": [9.6, 1], "farbe": 5, "dicke": 3},
                   {"von": [3.2, 4.5], "bis": [4.8, 4.5], "farbe": 5, "pfeil": True, "dicke": 5},
                   {"von": [2.9, 8], "bis": [5.1, 8], "farbe": 5, "gestrichelt": True}],
    texte=[T([4.0, 5.0], "Föhn", 5, 27), T([7.65, 7.65], "Bewegung", 3, 25, "start"), T([7.65, 7.1], "der Luft", 3, 25, "start"),
           T([1.7, 0.4], "hinein", 5, 26), T([6.3, 0.4], "heraus", 5, 26),
           T([5.0, 9.0], "gleich viel Energie", 5, 27)])))
# F5: F-h-Diagramm, m · g = 78.5 N über 1.5 m: 118 J
Fg = 8 * G_
assert round(Fg, 1) == 78.5 and round(Fg * 1.5) == 118
setze(d, 'Frage 5', A(graf([-0.2, 2.0], [-10, 100], [0.5, 1, 1.5], [20, 40, 60], 'h [m]', 'F [N]',
    flaechen=[{"punkte": [[0, 0], [1.5, 0], [1.5, Fg], [0, Fg]], "farbe": 2, "deckung": 0.25,
               "beschriftung": "W ≈ 118 J", "beschriftung_bei": [0.75, 40]}],
    strecken=[{"von": [0, Fg], "bis": [1.5, Fg], "farbe": 5, "dicke": 5,
               "beschriftung": "m · g ≈ 78.5 N", "beschriftung_bei": [0.75, 84], "anker": "middle"},
              {"von": [1.5, 0], "bis": [1.5, Fg], "farbe": 2, "dicke": 3}],
    texte=[T([0.75, 22], "78.5 N · 1.5 m", 2, 27)])))
formelgroesse(d, 'Frage 5', 36)
speichere('p4-3-lp-kontrolle-arbeit', d)

# ======================================================== Bremsen
d = lade('p4-3-lp-kontrolle-bremsen'); ohne_alte_antworten(d)
# F1: E(v) = ½ · 0.4 kg · v², Punkt (10 m/s; 20 J)
assert abs(0.5 * 0.4 * 100 - 20) < 1e-9
setze(d, 'Frage 1', A(graf([-1.2, 13], [-3.5, 36], [2, 4, 6, 8, 10, 12], [10, 20, 30], 'v [m/s]', 'E [J]',
    kurven=[{"formel": "0.2*x*x", "von": 0, "bis": 13, "farbe": 3, "dicke": 5}],
    strecken=[{"von": [10, 0], "bis": [10, 20], "farbe": 5, "gestrichelt": True},
              {"von": [0, 20], "bis": [10, 20], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 10, "y": 20, "farbe": 3, "beschriftung": "(10 m/s; 20 J)", "beschriftung_bei": [9.6, 22.2], "anker": "end"}],
    texte=[T([0.6, 30.5], "E kin = ½ · 0.4 kg · v²", 3, 27, "start")])))
# F2: (3 v)² = 9 v² als Quadrat aus neun Feldern
q = 1.2
fl, st = saeulen(balken(0.5, 0.5 + q, 0.5, 0.5 + q, 3, None, deckung=0.25),
                 balken(3.5, 3.5 + 3 * q, 0.5, 0.5 + 3 * q, 3, None, deckung=0.25))
st += [{"von": [0.5, 0.5], "bis": [0.5 + q, 0.5], "farbe": 3, "dicke": 3},
       {"von": [3.5, 0.5], "bis": [3.5 + 3 * q, 0.5], "farbe": 3, "dicke": 3}]
for k in (1, 2):
    st += [{"von": [3.5 + k * q, 0.5], "bis": [3.5 + k * q, 0.5 + 3 * q], "farbe": 3, "dicke": 2},
           {"von": [3.5, 0.5 + k * q], "bis": [3.5 + 3 * q, 0.5 + k * q], "farbe": 3, "dicke": 2}]
tx = [T([0.5 + q / 2, 0.5 + q / 2 - 0.12], "v²", 3, 30)]
for i in range(3):
    for j in range(3):
        tx.append(T([3.5 + (i + 0.5) * q, 0.5 + (j + 0.5) * q - 0.12], "v²", 3, 30))
tx += [T([0.5 + q / 2, -0.1], "v", 5, 28), T([3.5 + 1.5 * q, -0.1], "3 · v", 5, 28),
       T([0.5 + q / 2, 2.0], "E", 3, 30), T([3.5 + 1.5 * q, 4.4], "9 · E", 3, 30),
       T([4.0, 5.9], "dreifaches Tempo:", 5, 28), T([4.0, 5.35], "neunfache Energie", 5, 28)]
setze(d, 'Frage 2', A(bild([0, 8], [-1, 7], flaechen=fl, strecken=st, texte=tx)))
# F3: Kiste auf dem Schrank, Seitenansicht 1:1
fl, st = saeulen(balken(0, 1.0, 0, 2.0, 5, None, deckung=0.10), balken(0.25, 0.75, 2.0, 2.45, 1, None, deckung=0.45))
st += [{"von": [-1.6, 0], "bis": [2.8, 0], "farbe": 5, "dicke": 4},
       {"von": [-0.7, 2.0], "bis": [0.25, 2.0], "farbe": 5, "gestrichelt": True},
       {"von": [-0.35, 0], "bis": [-0.35, 2.0], "farbe": 5, "pfeil": True, "dicke": 4,
        "beschriftung": "h = 2 m", "beschriftung_bei": [-0.47, 0.95], "anker": "end"}]
assert abs(5 * G_ * 2 - 98.1) < 1e-9
setze(d, 'Frage 3', A(bild([-1.6, 2.8], [-0.7, 3.7], flaechen=fl, strecken=st,
    texte=[T([0.85, 2.12], "5 kg", 1, 27, "start"), T([0.5, 3.0], "Lageenergie ≈ 98.1 J", 1, 30),
           T([0.6, -0.42], "Bezug: Boden, h = 0", 5, 25)])))
# F4: Bremskraft über dem Weg, Fläche = Bewegungsenergie 72 kJ
assert 0.5 * 1000 * 12 ** 2 == 72000 and 72000 / 4000 == 18
setze(d, 'Frage 4', A(graf([-2.3, 23], [-550, 5400], [5, 10, 15, 20], [1000, 2000, 3000, 4000, 5000], 's [m]', 'F [N]',
    flaechen=[{"punkte": [[0, 0], [18, 0], [18, 4000], [0, 4000]], "farbe": 3, "deckung": 0.25,
               "beschriftung": "F · s = E kin = 72 kJ", "beschriftung_bei": [9, 1900]}],
    strecken=[{"von": [0, 4000], "bis": [18, 4000], "farbe": 5, "dicke": 5,
               "beschriftung": "Bremskraft 4000 N", "beschriftung_bei": [9, 4250], "anker": "middle"},
              {"von": [18, 0], "bis": [18, 4000], "farbe": 3, "dicke": 3}],
    texte=[T([18.3, 2700], "s = 18 m", 5, 27, "start")])))
# F5: E(v) = ½ · 90 kg · v², von 1125 J aus abgelesen: 5 m/s
assert abs(0.5 * 90 * 25 - 1125) < 1e-9
setze(d, 'Frage 5', A(graf([-0.8, 7.6], [-170, 2350], [1, 2, 3, 4, 5, 6, 7], [500, 1000, 1500, 2000], 'v [m/s]', 'E [J]',
    kurven=[{"formel": "45*x*x", "von": 0, "bis": 7.2, "farbe": 3, "dicke": 5}],
    strecken=[{"von": [0, 1125], "bis": [5, 1125], "farbe": 5, "gestrichelt": True},
              {"von": [5, 1125], "bis": [5, 0], "farbe": 5, "gestrichelt": True, "pfeil": True}],
    punkte=[{"x": 5, "y": 1125, "farbe": 3, "beschriftung": "(5 m/s; 1125 J)", "beschriftung_bei": [5.2, 960], "anker": "start"}],
    texte=[T([0.3, 2030], "E kin = ½ · 90 kg · v²", 3, 27, "start")])))
speichere('p4-3-lp-kontrolle-bremsen', d)

# ======================================================== Erhaltung
d = lade('p4-3-lp-kontrolle-erhaltung'); ohne_alte_antworten(d)
# F1: Stein aus 5 m, Energiesäulen oben/unten gleich hoch
v1 = math.sqrt(2 * G_ * 5); assert round(v1, 1) == 9.9
fl, st = saeulen(balken(5.0, 6.3, 0, 5, 1, "E pot", [5.65, 2.5]), balken(7.3, 8.6, 0, 5, 3, "E kin", [7.95, 2.5]))
st += [{"von": [0.2, 0], "bis": [3.4, 0], "farbe": 5, "dicke": 4},
       {"von": [4.7, 0], "bis": [8.9, 0], "farbe": 5, "dicke": 3},
       {"von": [1.5, 5], "bis": [1.5, 0.35], "farbe": 5, "gestrichelt": True},
       {"von": [0.9, 0], "bis": [0.9, 5], "farbe": 5, "pfeil": True, "dicke": 3,
        "beschriftung": "5 m", "beschriftung_bei": [0.78, 2.4], "anker": "end"},
       {"von": [2.0, 1.6], "bis": [2.0, 0.25], "farbe": 3, "pfeil": True, "dicke": 5},
       {"von": [6.3, 5], "bis": [7.3, 5], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 1', A(bild([0, 10], [-1.5, 8.5], flaechen=fl, strecken=st,
    punkte=[{"x": 1.5, "y": 5, "farbe": 1}, {"x": 1.5, "y": 0.35, "farbe": 3}],
    texte=[T([1.75, 5.45], "Start: v = 0", 1, 26, "start"), T([2.2, 0.75], "v ≈ 9.9 m/s", 3, 26, "start"),
           T([5.65, -0.6], "oben", 5, 26), T([7.95, -0.6], "unten", 5, 26),
           T([6.8, 5.5], "gleich viel", 5, 26)])))
# F2: Bahnprofil 1:1, Start und Umkehr auf 12 m
prof = {"formel": "6+6*cos(2*pi*(x-2)/22)", "von": 2, "bis": 24, "farbe": 5, "dicke": 5}
setze(d, 'Frage 2', A(graf([-3, 27], [-8, 22], [5, 10, 15, 20], [4, 8, 12, 16], 'x [m]', 'h [m]',
    kurven=[prof],
    strecken=[{"von": [0, 12], "bis": [26, 12], "farbe": 1, "gestrichelt": True}],
    punkte=[{"x": 2, "y": 12, "farbe": 1, "beschriftung": "Start: v = 0", "beschriftung_bei": [1.3, 14], "anker": "start"},
            {"x": 24, "y": 12, "farbe": 1, "beschriftung": "kurz still: 12 m", "beschriftung_bei": [25.3, 14], "anker": "end"}],
    texte=[T([13, 10.3], "gleiche Höhe, ohne Reibung", 1, 26)])))
# F3: Ball senkrecht hoch, 6 m/s → 1.83 m; Säulen unten E kin = oben E pot
hm = 36 / (2 * G_); assert round(hm, 2) == 1.83
fl, st = saeulen(balken(2.5, 3.1, 0, hm, 3, "E kin", [2.8, hm / 2]), balken(3.5, 4.1, 0, hm, 1, "E pot", [3.8, hm / 2]))
st += [{"von": [0.2, 0], "bis": [1.7, 0], "farbe": 5, "dicke": 4},
       {"von": [2.35, 0], "bis": [4.25, 0], "farbe": 5, "dicke": 3},
       {"von": [0.9, 0.15], "bis": [0.9, hm], "farbe": 5, "gestrichelt": True},
       {"von": [0.55, 0.15], "bis": [0.55, 1.0], "farbe": 3, "pfeil": True, "dicke": 5},
       {"von": [1.35, 0], "bis": [1.35, hm], "farbe": 5, "pfeil": True, "dicke": 3,
        "beschriftung": "h ≈ 1.83 m", "beschriftung_bei": [1.45, 0.85], "anker": "start"},
       {"von": [3.1, hm], "bis": [3.5, hm], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 3', A(bild([0, 4.4], [-0.9, 3.5], flaechen=fl, strecken=st,
    punkte=[{"x": 0.9, "y": 0.15, "farbe": 3}, {"x": 0.9, "y": round(hm, 3), "farbe": 1}],
    texte=[T([0.47, 0.5], "6 m/s", 3, 26, "end"), T([0.78, 2.0], "v = 0", 1, 26, "end"),
           T([2.8, -0.35], "unten", 5, 25), T([3.8, -0.35], "oben", 5, 25)])))
# F4: Säulen je kg: oben 98.1 + 8 J/kg, im Tal 106.1 J/kg
ep, ek = G_ * 10, 0.5 * 16; tot = ep + ek; v4 = math.sqrt(2 * tot)
assert round(v4, 1) == 14.6 and round(tot, 1) == 106.1
fl, st = saeulen(balken(0.5, 2.0, 0, ep, 1, "E pot: 98.1", [1.25, 45]), balken(0.5, 2.0, ep, tot, 3),
                 balken(3.0, 4.5, 0, tot, 3, "E kin: 106.1", [3.75, 45]))
st += [{"von": [2.0, tot], "bis": [3.0, tot], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 4', A(graf([-0.6, 5.4], [-14, 135], [], [20, 40, 60, 80, 100, 120], '', 'E/m [J/kg]',
    flaechen=fl, strecken=st,
    texte=[T([2.08, 98.5], "E kin: 8", 3, 24, "start"),
           T([1.25, -9], "oben", 5, 26), T([3.75, -9], "im Tal", 5, 26),
           T([0.3, 122], "v = √(2 · 106.1 J/kg) ≈ 14.6 m/s", 3, 27, "start")])))
# F5: Start aus der Ruhe auf 15 m, Hügel 16 m: Umkehr auf 15 m
xu = 14 + 14 * math.acos(-7 / 8) / math.pi
assert abs(8 - 8 * math.cos(math.pi * (xu - 14) / 14) - 15) < 1e-9
setze(d, 'Frage 5', A(graf([-3, 33], [-6, 30], [10, 20, 30], [5, 10, 15, 20, 25], 'x [m]', 'h [m]',
    kurven=[{"formel": "7.5+7.5*cos(pi*(x-2)/12)", "von": 2, "bis": 14, "farbe": 5, "dicke": 5},
            {"formel": "8-8*cos(pi*(x-14)/14)", "von": 14, "bis": 32, "farbe": 5, "dicke": 5}],
    strecken=[{"von": [0, 15], "bis": [32, 15], "farbe": 1, "gestrichelt": True}],
    punkte=[{"x": 2, "y": 15, "farbe": 1, "beschriftung": "Start: 15 m, v = 0", "beschriftung_bei": [1.3, 17.6], "anker": "start"},
            {"x": round(xu, 3), "y": 15, "farbe": 4, "beschriftung": "kehrt um", "beschriftung_bei": [round(xu, 3) - 1.0, 17.6], "anker": "end"},
            {"x": 28, "y": 16, "farbe": 5, "beschriftung": "16 m", "beschriftung_bei": [28.3, 18.2], "anker": "start"}],
    texte=[T([13, 12.3], "Energie reicht bis 15 m", 1, 26)])))
formelgroesse(d, 'Frage 4', 36)
speichere('p4-3-lp-kontrolle-erhaltung', d)

# ======================================================== Reibung
d = lade('p4-3-lp-kontrolle-reibung'); ohne_alte_antworten(d)
# F1: Säulen vorher/nachher, ein Teil der Bewegungsenergie ist Wärme
fl, st = saeulen(balken(1.5, 3.5, 0, 6, 3, "E kin", [2.5, 3]),
                 balken(6.0, 8.0, 0, 2.5, 3, "E kin", [7.0, 1.25]), balken(6.0, 8.0, 2.5, 6, 4, "Wärme", [7.0, 4.6]))
st += [{"von": [1.0, 0], "bis": [8.6, 0], "farbe": 5, "dicke": 3},
       {"von": [3.5, 6], "bis": [6.0, 6], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 1', A(bild([0, 10], [-1.5, 8.5], flaechen=fl, strecken=st,
    texte=[T([7.0, 3.55], "3000 J", 4, 27), T([2.5, -0.6], "vorher", 5, 26), T([7.0, -0.6], "nachher", 5, 26),
           T([4.75, 6.35], "gleich viel", 5, 26), T([5.0, 7.5], "Kufen und Schnee: wärmer", 4, 28)])))
# F2: Rutschbahn: 736 J oben = 313 J Bewegung + 423 J Wärme
ep2, ek2 = 25 * G_ * 3, 0.5 * 25 * 25; w2 = ep2 - ek2
assert round(ep2) == 736 and ek2 == 312.5 and round(w2) == 423
fl, st = saeulen(balken(0.4, 2.1, 0, ep2, 1, "E pot: 736 J", [1.25, 340]),
                 balken(2.9, 4.6, 0, ek2, 3, "E kin: 312.5 J", [3.75, 140]), balken(2.9, 4.6, ek2, ep2, 4, "Wärme: 423 J", [3.75, 510]))
st += [{"von": [2.1, ep2], "bis": [2.9, ep2], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 2', A(graf([-0.6, 5.4], [-85, 900], [], [200, 400, 600, 800], '', 'E [J]',
    flaechen=fl, strecken=st,
    texte=[T([1.25, -55], "oben", 5, 26), T([3.75, -55], "unten", 5, 26)])))
# F3: Lift: Motorarbeit 63.9 kJ = Hubarbeit 58.9 kJ + Reibung 5 kJ
hub, rb = 600 * G_ * 10 / 1000, 500 * 10 / 1000
assert round(hub, 1) == 58.9 and round(hub + rb, 1) == 63.9
fl, st = saeulen(balken(0.3, 1.8, 0, hub + rb, 2, "63.9 kJ", [1.05, 30]),
                 balken(2.6, 4.1, 0, hub, 1, "58.9 kJ", [3.35, 30]), balken(2.6, 4.1, hub, hub + rb, 4))
st += [{"von": [1.8, hub + rb], "bis": [2.6, hub + rb], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 3', A(graf([-0.6, 5.8], [-8, 75], [], [20, 40, 60], '', 'W [kJ]',
    flaechen=fl, strecken=st,
    texte=[T([4.2, 59.6], "Reibung 5 kJ", 4, 26, "start"), T([3.35, 20], "Hubarbeit", 1, 25),
           T([1.05, -5], "Motor", 5, 26), T([3.35, -5], "Hub + Reibung", 5, 26)])))
# F4: drei Säulen: oben E pot; unten ohne Reibung alles E kin; mit Reibung E kin + Wärme
fl, st = saeulen(balken(0.6, 2.6, 0, 6, 1, "E pot", [1.6, 3]), balken(3.8, 5.8, 0, 6, 3, "E kin", [4.8, 3]),
                 balken(7.0, 9.0, 0, 3.8, 3, "E kin", [8.0, 1.9]), balken(7.0, 9.0, 3.8, 6, 4, "Wärme", [8.0, 4.9]))
st += [{"von": [0.3, 0], "bis": [9.4, 0], "farbe": 5, "dicke": 3},
       {"von": [2.6, 6], "bis": [7.0, 6], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 4', A(bild([0, 10], [-1.6, 8.4], flaechen=fl, strecken=st,
    texte=[T([1.6, -0.55], "oben", 5, 25), T([4.8, -0.55], "unten", 5, 25), T([8.0, -0.55], "unten", 5, 25),
           T([4.8, -1.15], "ohne Reibung", 5, 24), T([8.0, -1.15], "mit Reibung", 5, 24),
           T([5.0, 7.3], "mit Reibung: weniger E kin,", 4, 27), T([5.0, 6.65], "also langsamer", 4, 27)])))
# F5: Summe bleibt gleich, die Anteile wechseln
fl, st = saeulen(balken(0.6, 2.6, 0, 6, 1, "E pot", [1.6, 3]),
                 balken(4.0, 6.0, 0, 3, 1, "E pot", [5.0, 1.5]), balken(4.0, 6.0, 3, 5, 3, "E kin", [5.0, 4.0]),
                 balken(4.0, 6.0, 5, 6, 4, "Wärme", [5.0, 5.5]),
                 balken(7.4, 9.4, 0, 4, 3, "E kin", [8.4, 2]), balken(7.4, 9.4, 4, 6, 4, "Wärme", [8.4, 5]))
st += [{"von": [0.3, 0], "bis": [9.7, 0], "farbe": 5, "dicke": 3},
       {"von": [0.3, 6], "bis": [9.7, 6], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 5', A(bild([0, 10], [-1.4, 8.6], flaechen=fl, strecken=st,
    texte=[T([1.6, -0.6], "oben", 5, 26), T([5.0, -0.6], "unterwegs", 5, 26), T([8.4, -0.6], "unten", 5, 26),
           T([5.0, 6.6], "Summe bleibt gleich", 5, 29)])))
formelgroesse(d, 'Frage 2', 34)
formelgroesse(d, 'Frage 3', 32)
speichere('p4-3-lp-kontrolle-reibung', d)

# ======================================================== Leistung
d = lade('p4-3-lp-kontrolle-leistung'); ohne_alte_antworten(d)
# F1: W-t-Gerade, Steigung = Leistung 196 W
W1 = 300 * G_ * 4 / 1000; P1 = W1 * 1000 / 60
assert round(W1, 1) == 11.8 and round(P1) == 196
setze(d, 'Frage 1', A(graf([-7, 75], [-1.3, 14.5], [20, 40, 60], [4, 8, 12], 't [s]', 'W [kJ]',
    strecken=[{"von": [0, 0], "bis": [70, round(P1 * 70 / 1000, 3)], "farbe": 2, "dicke": 5},
              {"von": [60, 0], "bis": [60, round(W1, 3)], "farbe": 5, "gestrichelt": True},
              {"von": [0, round(W1, 3)], "bis": [60, round(W1, 3)], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 60, "y": round(W1, 3), "farbe": 2, "beschriftung": "(60 s; 11.8 kJ)", "beschriftung_bei": [57, 12.6], "anker": "end"}],
    texte=[T([22, 3.0], "Steigung: P ≈ 196 W", 2, 27, "start"),
           T([22, 1.6], "11.8 kJ : 60 s", 2, 25, "start")])))
# F2: Säulen: 500 W hinein = 400 W nutzbar + 100 W Verlust
fl, st = saeulen(balken(0.4, 2.1, 0, 500, 2, "500 W", [1.25, 250]),
                 balken(2.9, 4.6, 0, 400, 3), balken(2.9, 4.6, 400, 500, 4))
st += [{"von": [2.1, 500], "bis": [2.9, 500], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 2', A(graf([-0.6, 5.4], [-60, 600], [], [100, 200, 300, 400, 500], '', 'P [W]',
    flaechen=fl, strecken=st,
    texte=[T([3.75, 215], "nutzbar", 3, 25), T([3.75, 170], "400 W", 3, 29),
           T([3.75, 455], "Verlust", 4, 25), T([3.75, 413], "100 W", 4, 25),
           T([1.25, -40], "aufgenommen", 5, 25), T([3.75, -40], "abgegeben", 5, 25),
           T([0.3, 545], "η = 400 W : 500 W = 0.8", 5, 28, "start")])))
# F3: P-t-Diagramm, Rechteck 2 kW x 0.5 h = 1 kWh
setze(d, 'Frage 3', A(graf([-0.07, 0.95], [-0.3, 2.8], [0.25, 0.5, 0.75], [1, 2], 't [h]', 'P [kW]',
    flaechen=[{"punkte": [[0, 0], [0.5, 0], [0.5, 2], [0, 2]], "farbe": 2, "deckung": 0.25,
               "beschriftung": "E = 1 kWh", "beschriftung_bei": [0.25, 1.05]}],
    strecken=[{"von": [0, 2], "bis": [0.5, 2], "farbe": 5, "dicke": 5,
               "beschriftung": "P = 2 kW", "beschriftung_bei": [0.25, 2.12], "anker": "middle"},
              {"von": [0.5, 0], "bis": [0.5, 2], "farbe": 2, "dicke": 3}],
    texte=[T([0.25, 0.5], "2 kW · 0.5 h", 2, 27), T([0.55, 1.3], "30 min = 0.5 h", 5, 27, "start")])))
# F4: Velo: Antrieb = Widerstand = 30 N, v = 5 m/s; je Sekunde 150 J
assert 30 * 5 == 150
setze(d, 'Frage 4', A(bild([-5, 5], [-4, 6],
    flaechen=[{"punkte": [[-1, 0], [1, 0], [1, 1.2], [-1, 1.2]], "farbe": 5, "deckung": 0.15}],
    strecken=[{"von": [-5, 0], "bis": [5, 0], "farbe": 5, "dicke": 3},
              {"von": [1, 0.6], "bis": [3.6, 0.6], "farbe": 5, "pfeil": True, "dicke": 6},
              {"von": [-1, 0.6], "bis": [-3.6, 0.6], "farbe": 4, "pfeil": True, "dicke": 6},
              {"von": [-1.2, 2.6], "bis": [2.2, 2.6], "farbe": 3, "pfeil": True, "dicke": 6}],
    texte=[T([0, 0.42], "Velo", 5, 26), T([2.35, 1.55], "Antrieb 30 N", 5, 26), T([-2.35, 1.55], "Widerstand 30 N", 4, 26),
           T([0.5, 3.05], "v = 5 m/s", 3, 28),
           T([0, -1.1], "konstantes Tempo: Antrieb = Widerstand", 5, 25),
           T([0, -2.2], "je Sekunde: 30 N · 5 m = 150 J", 2, 28),
           T([0, -3.2], "also P = 150 W", 2, 28)])))
# F5: P-t-Rechtecke gleicher Fläche: P über t, 2 P über t/2
setze(d, 'Frage 5', A(graf([-0.18, 2.5], [-0.25, 2.5], [[1, "½ · t"], [2, "t"]], [[1, "P"], [2, "2 · P"]], 't [s]', 'P [W]',
    flaechen=[{"punkte": [[0, 0], [2, 0], [2, 1], [0, 1]], "farbe": 5, "deckung": 0.12},
              {"punkte": [[0, 0], [1, 0], [1, 2], [0, 2]], "farbe": 2, "deckung": 0.25}],
    strecken=[{"von": [0, 1], "bis": [2, 1], "farbe": 5, "dicke": 4},
              {"von": [2, 0], "bis": [2, 1], "farbe": 5, "dicke": 4},
              {"von": [0, 2], "bis": [1, 2], "farbe": 2, "dicke": 4},
              {"von": [1, 0], "bis": [1, 2], "farbe": 2, "dicke": 4}],
    texte=[T([1.5, 1.08], "langsamer Kran", 5, 26), T([0.5, 2.08], "schneller Kran", 2, 26),
           T([1.6, 1.75], "gleiche Fläche:", 5, 27, "start"), T([1.6, 1.55], "gleiche Arbeit", 5, 27, "start")])))
speichere('p4-3-lp-kontrolle-leistung', d)

# ======================================================== Erde
d = lade('p4-3-lp-kontrolle-erde'); ohne_alte_antworten(d)
S4 = 1361 / 4
au30, au35 = 0.70 * S4, 0.65 * S4
assert round(au30) == 238 and round(au35) == 221 and round(S4) == 340
fl, st = saeulen(balken(0.4, 2.1, 0, au30, 2), balken(0.4, 2.1, au30, S4, 5, deckung=0.12),
                 balken(2.9, 4.6, 0, au35, 2), balken(2.9, 4.6, au35, S4, 5, deckung=0.12))
st += [{"von": [0.2, S4], "bis": [4.8, S4], "farbe": 5, "gestrichelt": True}]
setze(d, 'Frage 1', A(graf([-0.6, 5.4], [-40, 400], [], [100, 200, 300], '', 'P/A [W/m²]',
    flaechen=fl, strecken=st,
    texte=[T([1.25, 135], "aufgenommen", 2, 24), T([1.25, 100], "238 W/m²", 2, 27),
           T([3.75, 127], "aufgenommen", 2, 24), T([3.75, 92], "221 W/m²", 2, 27),
           T([1.25, 297], "zurück", 5, 23), T([1.25, 264], "102 W/m²", 5, 23),
           T([3.75, 290], "zurück", 5, 23), T([3.75, 257], "119 W/m²", 5, 23),
           T([1.25, -27], "a = 0.30", 5, 26), T([3.75, -27], "a = 0.35", 5, 26),
           T([2.5, 362], "S/4 ≈ 340 W/m² treffen ein", 5, 25)])))
# F2: P/A = σ T⁴, Punkt (288 K; 390 W/m²)
assert round(SIG * 288 ** 4) == 390
setze(d, 'Frage 2', A(graf([-25, 345], [-60, 800], [100, 200, 300], [200, 400, 600], 'T [K]', 'P/A [W/m²]',
    kurven=[{"formel": "5.67e-8*x**4", "von": 0, "bis": 340, "farbe": 4, "dicke": 5}],
    strecken=[{"von": [288, 0], "bis": [288, 390], "farbe": 5, "gestrichelt": True},
              {"von": [0, 390], "bis": [288, 390], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 288, "y": 390, "farbe": 4, "beschriftung": "(288 K; 390 W/m²)", "beschriftung_bei": [270, 425], "anker": "end"}],
    texte=[T([20, 690], "wärmer: mehr Abstrahlung", 4, 27, "start")])))
# F3: Strahlungsfluss heute / mehr CO₂ (Pfeildicke ~ Strahlung)
setze(d, 'Frage 3', A(bild([0, 10], [0, 10],
    flaechen=[{"punkte": [[0, 0], [10, 0], [10, 1], [0, 1]], "farbe": 1, "deckung": 0.25},
              {"punkte": [[0, 4.5], [10, 4.5], [10, 6], [0, 6]], "farbe": 5, "deckung": 0.12}],
    strecken=[{"von": [2.5, 1.1], "bis": [2.5, 4.4], "farbe": 4, "pfeil": True, "dicke": 9},
              {"von": [2.5, 6.1], "bis": [2.5, 8.8], "farbe": 4, "pfeil": True, "dicke": 6},
              {"von": [7.5, 1.1], "bis": [7.5, 4.4], "farbe": 4, "pfeil": True, "dicke": 9},
              {"von": [7.5, 6.1], "bis": [7.5, 8.8], "farbe": 4, "pfeil": True, "dicke": 3},
              {"von": [5, 1], "bis": [5, 9.6], "farbe": 5, "gestrichelt": True, "dicke": 2}],
    texte=[T([2.5, 9.3], "heute", 5, 28), T([7.5, 9.3], "mehr CO₂", 5, 28),
           T([2.8, 7.3], "238 W/m²", 4, 25, "start"), T([7.8, 7.3], "weniger", 4, 25, "start"),
           T([2.8, 2.6], "390 W/m²", 4, 25, "start"), T([7.8, 2.6], "390 W/m²", 4, 25, "start"),
           T([5, 5.1], "Atmosphäre hält zurück", 5, 25),
           T([5, 0.35], "Erdoberfläche", 5, 25)])))
# F4: Modell des Leitprogramms (Sim 6): 1 W/m² mehr aufgenommen
C, JAHR = 4.2e8, 3.156e7
T0 = (0.7 * S4 / (0.61 * SIG)) ** 0.25
lam = 4 * 0.61 * SIG * T0 ** 3
dT, tau = 1 / lam, C / lam / JAHR
Tk = T0; dt = JAHR / 200
for i in range(200 * 30):
    Tk += dt * (0.7 * S4 + 1 - 0.61 * SIG * Tk ** 4) / C
assert abs((Tk - T0) - dT * (1 - math.exp(-30 / tau))) < 0.002 and round(dT, 1) == 0.3
steig = JAHR / C          # K pro Jahr ohne steigende Abstrahlung
setze(d, 'Frage 4', A(graf([-2.5, 32], [-0.04, 0.44], [10, 20, 30], [0.1, 0.2, 0.3, 0.4], 't [Jahre]', 'ΔT [K]',
    kurven=[{"formel": "%.4f*(1-exp(-x/%.3f))" % (dT, tau), "von": 0, "bis": 31, "farbe": 4, "dicke": 5}],
    strecken=[{"von": [0, 0], "bis": [round(0.4 / steig, 2), 0.4], "farbe": 5, "gestrichelt": True},
              {"von": [0, round(dT, 4)], "bis": [31, round(dT, 4)], "farbe": 4, "gestrichelt": True, "dicke": 2}],
    texte=[T([6.3, 0.385], "ohne mehr Abstrahlung: ohne Ende", 5, 24, "start"),
           T([30.5, 0.33], "Abstrahlung passt: + 0.3 K", 4, 26, "end"),
           T([9, 0.12], "Aufnahme > Abstrahlung: wärmer", 4, 24, "start")])))
# F5: 300 K und 600 K: 16-mal so viel, die grosse Säule in 16 Streifen
p3, p6 = SIG * 300 ** 4, SIG * 600 ** 4
assert abs(p6 / p3 - 16) < 1e-9 and round(p3) == 459 and round(p6) == 7348
fl, st = saeulen(balken(0.6, 2.0, 0, p3, 4), balken(3.0, 4.4, 0, p6, 4))
st += [{"von": [3.0, round(k * p3, 1)], "bis": [4.4, round(k * p3, 1)], "farbe": 4, "dicke": 1.5} for k in range(1, 16)]
setze(d, 'Frage 5', A(graf([-0.6, 5.4], [-850, 8600], [], [2000, 4000, 6000, 8000], '', 'P/A [W/m²]',
    flaechen=fl, strecken=st,
    texte=[T([1.3, 750], "459 W/m²", 4, 27), T([3.7, 7700], "7348 W/m² = 16 · 459 W/m²", 4, 26),
           T([1.3, -500], "300 K", 5, 26), T([3.7, -500], "600 K", 5, 26)])))
speichere('p4-3-lp-kontrolle-erde', d)
print('ok')
