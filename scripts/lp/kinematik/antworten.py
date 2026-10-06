"""Antwortbilder der Kinematik-Kontrollclips (06.10.2026, Fassung 2 vom 06.10.2026: neue
Kontrollfragen kreis F2/F3, wurf F2, gleichförmig F5, beschleunigt F1; Antwortpunkt der
klick-Fragen erst nach der Bewegung der Geraden; Träger und Strömung in Tinte).

Jede Antwortszene bekommt ein Koordinatenbild rechts (x 1010, y 175, 760 x 760).
Steht in der Szene schon ein graf (klick-Frage), kommt die Antwort als zweite
Ebene mit "achsen": false deckungsgleich darüber, damit sie erst nach der Frage
erscheint. Alle Zahlen hier gerechnet.
"""
import os
import json, math, sys

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
G_ = 9.81


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": xb, "ybereich": yb,
         "xteilung": [[v, fmt(v)] for v in xt], "yteilung": [[v, fmt(v)] for v in yt],
         "xname": xname, "yname": yname}
    g.update(kw)
    return g


def fmt(v):
    return ('%g' % v).replace('-', '−')


def kreis(cx, cy, r, farbe=5, dicke=4, gestrichelt=False):
    """Kreis aus zwei Halbkurven."""
    k = []
    for vz in (1, -1):
        k.append({"formel": "%g%+g*sqrt(abs(%g-(x-(%g))*(x-(%g))))" % (cy, vz, r * r, cx, cx), "von": cx - r, "bis": cx + r,
                  "farbe": farbe, "dicke": dicke, "n": 600, **({"gestrichelt": True} if gestrichelt else {})})
    return k


def setze(d, szene, el, ersetze_graf=False):
    for s in d['szenen']:
        if s['name'] == szene:
            if ersetze_graf:
                s['elemente'] = [e for e in s['elemente'] if e['typ'] != 'graf']
            s['elemente'].append(el)
            return
    raise KeyError(szene)


def lade(n):
    return json.load(open(R + n + '.json'))


def speichere(n, d):
    # Neben einem Antwortbild hat die Formel links nur 820 px: lange Zeilen kleiner setzen
    for s_ in d['szenen']:
        if any(e['typ'] == 'graf' for e in s_['elemente']):
            for e in s_['elemente']:
                if e['typ'] == 'formel' and len(e['text']) > 75:
                    e['groesse'] = min(e.get('groesse', 54), 40)
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def ohne_alte_antworten(d):
    """Wiederholbar: frühere Antwortbilder (Kennung "antwort") entfernen."""
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]


def A(el):
    el['antwort'] = True
    return el


# ======================================================== gleichförmig
d = lade('p4-1-lp-kontrolle-gleichfoermig'); ohne_alte_antworten(d)
# F1: Fahrt mit Halten, Sekante = Durchschnittsgeschwindigkeit
fahrt = [(0, 0), (0.35, 35), (0.55, 35), (1.0, 75), (1.2, 75), (1.5, 90)]
setze(d, 'Frage 1', A(graf([-0.15, 1.75], [-18, 108], [0.5, 1, 1.5], [20, 40, 60, 80, 100], 't [h]', 's [km]',
    strecken=[{"von": list(a), "bis": list(b), "farbe": 1, "dicke": 5} for a, b in zip(fahrt, fahrt[1:])]
    + [{"von": [0, 0], "bis": [1.5, 90], "farbe": 3, "dicke": 4, "gestrichelt": True},
       {"von": [0, 0], "bis": [1.5, 0], "farbe": 5, "gestrichelt": True, "beschriftung": "Δt = 1.5 h", "beschriftung_bei": [0.75, -14], "anker": "middle"},
       {"von": [1.5, 0], "bis": [1.5, 90], "farbe": 5, "gestrichelt": True, "beschriftung": "Δs = 90 km", "beschriftung_bei": [1.47, 48], "anker": "end"}],
    texte=[{"bei": [0.3, 62], "text": "v̄ = 60 km/h", "farbe": 3, "groesse": 30}])))
# F2: Karussell von oben
setze(d, 'Frage 2', A(graf([-3.4, 3.4], [-3.4, 3.4], [], [], 'x [m]', 'y [m]', pfeile=False,
    kurven=kreis(0, 0, 2.5, farbe=1, dicke=5),
    strecken=[{"von": [0, 0], "bis": [1.77, 1.77], "farbe": 5, "gestrichelt": True, "beschriftung": "r", "beschriftung_bei": [0.62, 1.12]}],
    punkte=[{"x": 0, "y": 0, "farbe": 5, "beschriftung": "Achse", "beschriftung_bei": [0.15, -0.45]},
            {"x": 1.77, "y": 1.77, "farbe": 3, "beschriftung": "Kind", "beschriftung_bei": [1.95, 2.2]}],
    texte=[{"bei": [-3.1, -3.0], "text": "Bahnkurve: Kreis", "farbe": 1, "groesse": 30}])))
# F3: Overlay auf die klick-Gerade s = 10 + 4 t
setze(d, 'Frage 3', A(graf([-1.2, 11], [-7, 62], [], [], 't [s]', 's [m]', achsen=False, ein=3.3,
    strecken=[{"von": [5, 0], "bis": [5, 30], "farbe": 5, "gestrichelt": True},
              {"von": [0, 30], "bis": [5, 30], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 5, "y": 30, "farbe": 3, "beschriftung": "(5 s; 30 m)", "beschriftung_bei": [5.3, 26], "anker": "start"}])))
# F4: zwei Geraden, A steiler
setze(d, 'Frage 4', A(graf([-0.8, 8.6], [-7, 62], [2, 4, 6, 8], [10, 20, 30, 40, 50, 60], 't [s]', 's [m]',
    geraden=[],
    strecken=[{"von": [0, 5], "bis": [8, 53], "farbe": 1, "dicke": 5, "beschriftung": "A", "beschriftung_bei": [7.2, 55]},
              {"von": [0, 20], "bis": [8, 36], "farbe": 3, "dicke": 5, "beschriftung": "B", "beschriftung_bei": [7.7, 39]},
              {"von": [2, 17], "bis": [4, 17], "farbe": 1, "gestrichelt": True, "beschriftung": "2 s", "beschriftung_bei": [3, 13.5], "anker": "middle"},
              {"von": [4, 17], "bis": [4, 29], "farbe": 1, "gestrichelt": True, "beschriftung": "12 m", "beschriftung_bei": [4.15, 22]},
              {"von": [5, 30], "bis": [7, 30], "farbe": 3, "gestrichelt": True, "beschriftung": "2 s", "beschriftung_bei": [6, 26.5], "anker": "middle"},
              {"von": [7, 30], "bis": [7, 34], "farbe": 3, "gestrichelt": True, "beschriftung": "4 m", "beschriftung_bei": [7.15, 30.5]}],
    texte=[{"bei": [2.0, 57], "text": "steiler: schneller", "farbe": 5, "groesse": 30, "anker": "start"}])))
# F5: v in km/h über v in m/s, Steigung 3.6
setze(d, 'Frage 5', A(graf([-1.5, 17.5], [-6, 62], [4, 8, 12], [10, 20, 30, 40, 50, 60], 'v [m/s]', 'v [km/h]',
    strecken=[{"von": [0, 0], "bis": [16.5, 59.4], "farbe": 3, "dicke": 5},
              {"von": [12, 0], "bis": [12, 43.2], "farbe": 5, "gestrichelt": True},
              {"von": [0, 43.2], "bis": [12, 43.2], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 12, "y": 43.2, "farbe": 3, "beschriftung": "12 m/s ≙ 43.2 km/h", "beschriftung_bei": [11.5, 47.5], "anker": "end"}],
    texte=[{"bei": [9.5, 18], "text": "mal 3.6", "farbe": 5, "groesse": 30}])))
speichere('p4-1-lp-kontrolle-gleichfoermig', d)

# ======================================================== beschleunigt
d = lade('p4-1-lp-kontrolle-beschleunigt'); ohne_alte_antworten(d)
# F1: 8 -> 23 m/s in 5 s
setze(d, 'Frage 1', A(graf([-0.7, 6.4], [-3, 28], [1, 2, 3, 4, 5, 6], [5, 10, 15, 20, 25], 't [s]', 'v [m/s]',
    strecken=[{"von": [0, 8], "bis": [5, 20], "farbe": 3, "dicke": 5},
              {"von": [0, 8], "bis": [5, 8], "farbe": 5, "gestrichelt": True, "beschriftung": "Δt = 5 s", "beschriftung_bei": [2.5, 6.0], "anker": "middle"},
              {"von": [5, 8], "bis": [5, 20], "farbe": 3, "gestrichelt": True, "beschriftung": "Δv = 12 m/s", "beschriftung_bei": [5.15, 13.5]}],
    )))
# F2: Fläche unter der v-t-Geraden = Weg
setze(d, 'Frage 2', A(graf([-0.8, 8.6], [-3, 26], [2, 4, 6, 8], [5, 10, 15, 20, 25], 't [s]', 'v [m/s]',
    flaechen=[{"punkte": [[0, 0], [0, 6], [6, 18], [6, 0]], "farbe": 1, "beschriftung": "Weg s", "beschriftung_bei": [3, 6]}],
    strecken=[{"von": [0, 6], "bis": [8, 22], "farbe": 3, "dicke": 5}],
    texte=[{"bei": [3, 2.2], "text": "m/s · s = m", "farbe": 1, "groesse": 27, "anker": "middle"}])))
# F3: Overlay auf die klick-Gerade v = 3 + 1.5 t
setze(d, 'Frage 3', A(graf([-1.2, 11], [-3, 26], [], [], 't [s]', 'v [m/s]', achsen=False, ein=3.3,
    strecken=[{"von": [6, 0], "bis": [6, 12], "farbe": 5, "gestrichelt": True},
              {"von": [0, 12], "bis": [6, 12], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 6, "y": 12, "farbe": 3, "beschriftung": "(6 s; 12 m/s)", "beschriftung_bei": [6.35, 10.2], "anker": "start"}])))
# F4: Bremsweg bei 50 und 100 km/h, gleiche Verzögerung
v1, v2 = 50 / 3.6, 100 / 3.6
a = v1 ** 2 / (2 * 20)
t1, t2 = v1 / a, v2 / a
assert abs(0.5 * t2 * v2 - 80) < 1e-6
setze(d, 'Frage 4', A(graf([-0.6, 6.8], [-3, 31], [1, 2, 3, 4, 5, 6], [5, 10, 15, 20, 25, 30], 't [s]', 'v [m/s]',
    flaechen=[{"punkte": [[0, 0], [0, v2], [t2, 0]], "farbe": 1, "deckung": 0.14, "beschriftung": "80 m", "beschriftung_bei": [1.9, 12.5]},
              {"punkte": [[0, 0], [0, v1], [t1, 0]], "farbe": 1, "deckung": 0.36, "beschriftung": "20 m", "beschriftung_bei": [0.85, 3.6]}],
    strecken=[{"von": [0, v2], "bis": [t2, 0], "farbe": 3, "dicke": 5},
              {"von": [0, v1], "bis": [t1, 0], "farbe": 3, "dicke": 4, "gestrichelt": True}],
    texte=[{"bei": [0.15, v2 + 1.3], "text": "100 km/h", "farbe": 3, "groesse": 26},
           {"bei": [3.1, v1 + 0.6], "text": "doppelt so hoch, doppelt so breit", "farbe": 5, "groesse": 24},
           {"bei": [0.15, v1 + 1.3], "text": "50 km/h", "farbe": 3, "groesse": 26}])))
# F5: bremsen, Gerade fällt
setze(d, 'Frage 5', A(graf([-0.7, 6.4], [-3, 24], [1, 2, 3, 4, 5, 6], [5, 10, 15, 20], 't [s]', 'v [m/s]',
    strecken=[{"von": [0, 20], "bis": [5, 0], "farbe": 3, "dicke": 5},
              {"von": [1, 16], "bis": [3, 16], "farbe": 5, "gestrichelt": True, "beschriftung": "Δt = 2 s", "beschriftung_bei": [2, 17.3], "anker": "middle"},
              {"von": [3, 16], "bis": [3, 8], "farbe": 3, "gestrichelt": True, "beschriftung": "Δv = −8 m/s", "beschriftung_bei": [3.15, 11.5]}],
    texte=[{"bei": [2.6, 21], "text": "a = −4 m/s² < 0", "farbe": 5, "groesse": 28}])))
for s_ in d['szenen']:
    if s_['name'] == 'Frage 3':
        for e in s_['elemente']:
            if e['typ'] == 'formel': e['groesse'] = 34
speichere('p4-1-lp-kontrolle-beschleunigt', d)

# ======================================================== Wurf
d = lade('p4-1-lp-kontrolle-wurf'); ohne_alte_antworten(d)
# F1: v = g t
setze(d, 'Frage 1', A(graf([-0.35, 3.3], [-3, 33], [1, 2, 3], [5, 10, 15, 20, 25, 30], 't [s]', 'v [m/s]',
    strecken=[{"von": [0, 0], "bis": [3.1, 3.1 * G_], "farbe": 3, "dicke": 5},
              {"von": [2.5, 0], "bis": [2.5, 2.5 * G_], "farbe": 5, "gestrichelt": True},
              {"von": [0, 2.5 * G_], "bis": [2.5, 2.5 * G_], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 2.5, "y": 2.5 * G_, "farbe": 3, "beschriftung": "(2.5 s; 24.5 m/s)", "beschriftung_bei": [2.35, 27.3], "anker": "end"}],
    texte=[{"bei": [1.5, 5.5], "text": "Steigung g = 9.81 m/s²", "farbe": 5, "groesse": 26, "anker": "middle"}])))
# F2: Fallzeit über der Höhe, t = Wurzel(2h/g): viermal so hoch, doppelt so lange
t7, t28 = math.sqrt(14 / G_), math.sqrt(56 / G_)
setze(d, 'Frage 2', A(graf([-2.5, 33], [-0.25, 3.0], [7, 14, 21, 28], [0.5, 1, 1.5, 2, 2.5], 'h [m]', 't [s]',
    kurven=[{"formel": "sqrt(2*x/%g)" % G_, "von": 0, "bis": 32, "farbe": 5, "dicke": 4, "n": 400}],
    strecken=[{"von": [7, 0], "bis": [7, round(t7, 4)], "farbe": 5, "gestrichelt": True},
              {"von": [0, round(t7, 4)], "bis": [7, round(t7, 4)], "farbe": 5, "gestrichelt": True},
              {"von": [28, 0], "bis": [28, round(t28, 4)], "farbe": 5, "gestrichelt": True},
              {"von": [0, round(t28, 4)], "bis": [28, round(t28, 4)], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 7, "y": round(t7, 4), "farbe": 1, "beschriftung": "(7 m; 1.19 s)", "beschriftung_bei": [8, 0.95], "anker": "start"},
            {"x": 28, "y": round(t28, 4), "farbe": 1, "beschriftung": "(28 m; 2.39 s)", "beschriftung_bei": [27, 2.62], "anker": "end"}],
    texte=[{"bei": [10, 2.0], "text": "4 · h: 2 · t", "farbe": 5, "groesse": 30, "anker": "middle"}])))
# F3/F4: Ball über die Tischkante, 3 m/s, 0.8 m
tf = math.sqrt(2 * 0.8 / G_); xf = 3 * tf
pk = [{"x": round(3 * t, 3), "y": round(0.8 - 0.5 * G_ * t * t, 3), "farbe": 1} for t in [0.1 * i for i in range(4)]]
bahn = {"formel": "0.8-%.5f*x*x" % (0.5 * G_ / 9), "von": 0, "bis": xf, "farbe": 1, "dicke": 4}
tisch = [{"von": [-0.45, 0.8], "bis": [0, 0.8], "farbe": 5, "dicke": 7}, {"von": [-0.05, 0.8], "bis": [-0.05, 0], "farbe": 5, "dicke": 5}]
bahn3 = dict(bahn, bis=0.9)   # F3 verrät die Weite (F4) nicht: Bahn endet vor der Landung, keine x-Teilung
setze(d, 'Frage 3', A(graf([-0.6, 1.7], [-0.1, 1.11], [], [0.5, 1], 'x [m]', 'y [m]', hoehe=400, y=355,
    kurven=[bahn3], punkte=pk,
    strecken=tisch + [{"von": [0.15, 0.8], "bis": [0.15, 0.0], "farbe": 5, "pfeil": True}],
    texte=[{"bei": [0.25, 0.22], "text": "senkrecht: wie freier Fall aus 0.8 m", "farbe": 5, "groesse": 24, "anker": "start"}])))
setze(d, 'Frage 4', A(graf([-0.6, 1.7], [-0.1, 1.11], [0.5, 1, 1.5], [0.5, 1], 'x [m]', 'y [m]', hoehe=400, y=355,
    kurven=[bahn], punkte=pk + [{"x": round(xf, 3), "y": 0, "farbe": 4}],
    strecken=tisch + [{"von": [0, 0.1], "bis": [xf, 0.1], "farbe": 1, "pfeil": True, "beschriftung": "1.2 m", "beschriftung_bei": [0.45, 0.15], "groesse": 28}])))
# F5 (neu): senkrechter Wurf, 10 m/s
ts, hm = 10 / G_, 100 / (2 * G_)
setze(d, 'Frage 5', A(graf([-0.25, 2.3], [-0.7, 7], [0.5, 1, 1.5, 2], [1, 2, 3, 4, 5, 6], 't [s]', 'h [m]',
    kurven=[{"formel": "10*x-%.5f*x*x" % (0.5 * G_), "von": 0, "bis": 2 * ts, "farbe": 1, "dicke": 5}],
    strecken=[{"von": [ts, 0], "bis": [ts, hm], "farbe": 5, "gestrichelt": True, "beschriftung": "1.02 s", "beschriftung_bei": [ts, -0.45], "anker": "middle"},
              {"von": [0, hm], "bis": [ts, hm], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": round(ts, 4), "y": round(hm, 4), "farbe": 3, "beschriftung": "höchster Punkt: 5.1 m", "beschriftung_bei": [ts + 0.06, hm + 0.35], "anker": "start"}])))
speichere('p4-1-lp-kontrolle-wurf', d)

# ======================================================== Vektor
d = lade('p4-1-lp-kontrolle-vektor'); ohne_alte_antworten(d)
OHNE = dict(achsen=False, pfeile=False)
setze(d, 'Frage 1', A(graf([-0.8, 9.6], [-3, 3], [], [], '', '', **OHNE,
    strecken=[{"von": [0, 1.4], "bis": [8, 1.4], "farbe": 5, "pfeil": True, "beschriftung": "Schiff: 8 m/s", "beschriftung_bei": [2.6, 1.75]},
              {"von": [8, 0.5], "bis": [6, 0.5], "farbe": 3, "pfeil": True, "beschriftung": "Person: 2 m/s nach hinten", "beschriftung_bei": [5.6, 0.62], "anker": "end"},
              {"von": [0, -1.2], "bis": [6, -1.2], "farbe": 4, "pfeil": True, "beschriftung": "gegenüber dem Ufer: 6 m/s", "beschriftung_bei": [0, -1.75]},
              {"von": [6, 0.5], "bis": [6, -1.2], "farbe": 5, "gestrichelt": True}])))
setze(d, 'Frage 2', A(graf([-0.2, 1.6], [-0.5, 1.3], [], [], '', '', **OHNE,
    strecken=[{"von": [0, 0], "bis": [1.2, 0], "farbe": 5, "pfeil": True, "beschriftung": "Laufkatze 1.2 m/s", "beschriftung_bei": [0.6, -0.13], "anker": "middle"},
              {"von": [1.2, 0], "bis": [1.2, 0.5], "farbe": 3, "pfeil": True, "beschriftung": "0.5 m/s", "beschriftung_bei": [1.24, 0.22]},
              {"von": [0, 0], "bis": [1.2, 0.5], "farbe": 4, "pfeil": True, "beschriftung": "1.3 m/s", "beschriftung_bei": [0.42, 0.3], "anker": "end"}],
    texte=[{"bei": [0.0, 0.95], "text": "rechter Winkel: Pythagoras", "farbe": 4, "groesse": 28}])))
setze(d, 'Frage 3', A(graf([-0.5, 4.6], [-0.9, 4.2], [], [], '', '', **OHNE,
    strecken=[{"von": [0.4, 0], "bis": [0.4, 2.5], "farbe": 3, "pfeil": True, "beschriftung": "quer 2.5 m/s", "beschriftung_bei": [0.5, 2.9]},
              {"von": [0.4, 2.5], "bis": [1.2, 2.5], "farbe": 5, "pfeil": True},
              {"von": [2.4, 0], "bis": [2.4, 2.5], "farbe": 3, "pfeil": True},
              {"von": [2.4, 2.5], "bis": [4.2, 2.5], "farbe": 5, "pfeil": True, "beschriftung": "Strömung stärker", "beschriftung_bei": [2.5, 2.9]},
              {"von": [-0.3, 2.5], "bis": [4.5, 2.5], "farbe": 5, "gestrichelt": True},
              {"von": [-0.3, 0], "bis": [4.5, 0], "farbe": 5, "gestrichelt": True}],
    texte=[{"bei": [2.1, 1.2], "text": "gleich hoch hinauf:", "farbe": 5, "groesse": 26, "anker": "middle"},
           {"bei": [2.1, 0.8], "text": "gleiche Querzeit", "farbe": 5, "groesse": 26, "anker": "middle"}])))
# F4: Draufsicht 1:1, Ufer bei y = 0 und y = 45 m
setze(d, 'Frage 4', A(graf([-22, 35], [-6, 51], [], [], '', '', **OHNE,
    strecken=[{"von": [-20, 45], "bis": [33, 45], "farbe": 5, "dicke": 4, "beschriftung": "Ufer", "beschriftung_bei": [22, 47.5]},
              {"von": [-20, 0], "bis": [33, 0], "farbe": 5, "dicke": 4, "beschriftung": "Ufer", "beschriftung_bei": [22, -4]},
              {"von": [-12, 0], "bis": [-12, 45], "farbe": 5, "gestrichelt": True, "beschriftung": "45 m", "beschriftung_bei": [-13, 22], "anker": "end"},
              {"von": [0, 0], "bis": [7.5, 45], "farbe": 4, "gestrichelt": True, "beschriftung": "Bahn", "beschriftung_bei": [5.5, 26]},
              {"von": [0, 45], "bis": [7.5, 45], "farbe": 1, "pfeil": True, "beschriftung": "7.5 m", "beschriftung_bei": [-0.5, 40.5], "anker": "end"},
              {"von": [0, 0], "bis": [0, 15], "farbe": 3, "pfeil": True, "beschriftung": "3 m/s", "beschriftung_bei": [-1.5, 8], "anker": "end"},
              {"von": [0, 0], "bis": [2.5, 0], "farbe": 5, "pfeil": True, "beschriftung": "0.5 m/s", "beschriftung_bei": [3.5, 2], "anker": "start"}],
    punkte=[{"x": 0, "y": 0, "farbe": 5}])))
# F5: Strömung 2 m/s, Schwimmerin 1.5 m/s: Kreis der möglichen Richtungen
setze(d, 'Frage 5', A(graf([-0.6, 4.2], [-2.2, 2.6], [1, 2, 3], [-2, -1, 1, 2], 'x [m/s]', 'y [m/s]',
    kurven=kreis(2, 0, 1.5, farbe=3, dicke=4, gestrichelt=True),
    strecken=[{"von": [0, 0], "bis": [2, 0], "farbe": 5, "pfeil": True, "beschriftung": "Strömung 2 m/s", "beschriftung_bei": [0.15, -0.35]},
              {"von": [2, 0], "bis": [2 - 1.5 * 0.6, 1.5 * 0.8], "farbe": 3, "pfeil": True, "beschriftung": "1.5 m/s", "beschriftung_bei": [1.72, 0.75]},
              {"von": [0, 0], "bis": [1.1, 1.2], "farbe": 4, "pfeil": True}],
    texte=[{"bei": [0.15, 2.05], "text": "jede Summe zeigt flussabwärts", "farbe": 4, "groesse": 26}])))
for s_ in d['szenen']:
    if s_['name'] == 'Frage 2':
        for e in s_['elemente']:
            if e['typ'] == 'formel': e['groesse'] = 38
speichere('p4-1-lp-kontrolle-vektor', d)

# ======================================================== Kreis
d = lade('p4-1-lp-kontrolle-kreis'); ohne_alte_antworten(d)
setze(d, 'Frage 1', A(graf([-0.12, 1.25], [-2.5, 25], [0.25, 0.5, 0.75, 1], [5, 10, 15, 20], 't [s]', 'Umdrehungen',
    strecken=[{"von": [0, 0], "bis": [1.15, 23], "farbe": 1, "dicke": 5},
              {"von": [1, 0], "bis": [1, 20], "farbe": 5, "gestrichelt": True},
              {"von": [0, 20], "bis": [1, 20], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 1, "y": 20, "farbe": 1, "beschriftung": "20 Umdrehungen in 1 s", "beschriftung_bei": [0.95, 21.6], "anker": "end"}],
    texte=[{"bei": [0.45, 4], "text": "f = 20 Hz", "farbe": 5, "groesse": 30}])))
setze(d, 'Frage 2', A(graf([-0.035, 0.46], [-0.8, 7.6], [0.1, 0.2, 0.3, 0.4], [], 't [s]', 'φ [rad]',
    yteilung=[[3.1416, "π"], [6.2832, "2π"]],
    strecken=[{"von": [0, 0], "bis": [0.3, 0.3 * 8 * math.pi], "farbe": 1, "dicke": 5},
              {"von": [0.25, 0], "bis": [0.25, 2 * math.pi], "farbe": 5, "gestrichelt": True, "beschriftung": "T = 0.25 s", "beschriftung_bei": [0.255, 0.5]},
              {"von": [0, 2 * math.pi], "bis": [0.25, 2 * math.pi], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 0.25, "y": round(2 * math.pi, 4), "farbe": 1, "beschriftung": "ein Umlauf: 2π", "beschriftung_bei": [0.235, 6.75], "anker": "end"}],
    texte=[{"bei": [0.265, 3.4], "text": "ω = 2π / 0.25 s", "farbe": 5, "groesse": 26}, {"bei": [0.265, 2.6], "text": "≈ 25.1 rad/s", "farbe": 5, "groesse": 26}])))
# F3: Δv-Skizze — zwei Geschwindigkeitspfeile, vom selben Punkt aus gezeichnet; ihre Differenz zeigt zur Mitte
L = 0.7
v1 = (-L * math.sin(math.radians(60)), L * math.cos(math.radians(60)))
v2 = (-L * math.sin(math.radians(120)), L * math.cos(math.radians(120)))
P1 = (math.cos(math.radians(60)), math.sin(math.radians(60)))
P2 = (math.cos(math.radians(120)), math.sin(math.radians(120)))
C = (0.75, -0.25)
r4 = lambda p: [round(p[0], 4), round(p[1], 4)]
setze(d, 'Frage 3', A(graf([-1.7, 1.7], [-1.7, 1.7], [], [], '', '', pfeile=False, achsen=False,
    kurven=kreis(0, 0, 1, farbe=5, dicke=4),
    strecken=[{"von": r4(P1), "bis": r4((P1[0] + v1[0], P1[1] + v1[1])), "farbe": 3, "pfeil": True, "beschriftung": "v₁", "beschriftung_bei": [0.3, 1.3]},
              {"von": r4(P2), "bis": r4((P2[0] + v2[0], P2[1] + v2[1])), "farbe": 3, "pfeil": True, "beschriftung": "v₂", "beschriftung_bei": [-1.25, 0.5], "anker": "end"},
              {"von": r4(C), "bis": r4((C[0] + v1[0], C[1] + v1[1])), "farbe": 3, "pfeil": True, "beschriftung": "v₁", "beschriftung_bei": [0.5, 0.2]},
              {"von": r4(C), "bis": r4((C[0] + v2[0], C[1] + v2[1])), "farbe": 3, "pfeil": True, "beschriftung": "v₂", "beschriftung_bei": [0.45, -0.66]},
              {"von": r4((C[0] + v1[0], C[1] + v1[1])), "bis": r4((C[0] + v2[0], C[1] + v2[1])), "farbe": 4, "pfeil": True, "dicke": 6,
               "beschriftung": "Δv", "beschriftung_bei": [0.0, -0.25], "anker": "end"}],
    punkte=[{"x": r4(P1)[0], "y": r4(P1)[1], "farbe": 5}, {"x": r4(P2)[0], "y": r4(P2)[1], "farbe": 5},
            {"x": 0, "y": 0, "farbe": 5, "beschriftung": "M", "beschriftung_bei": [-0.12, 0.05], "anker": "end"}],
    texte=[{"bei": [-1.6, -1.45], "text": "Δv zeigt zur Mitte", "farbe": 4, "groesse": 28}])))
# F4: r = 0.8 m, v = 4 m/s, a_z = 20 m/s²
setze(d, 'Frage 4', A(graf([-1.25, 1.25], [-1.25, 1.25], [], [], '', '', pfeile=False,
    kurven=kreis(0, 0, 0.8, farbe=5, dicke=4),
    strecken=[{"von": [0, 0], "bis": [0, 0.8], "farbe": 5, "gestrichelt": True, "beschriftung": "r = 0.8 m", "beschriftung_bei": [0.05, 0.3]},
              {"von": [0, 0.8], "bis": [-0.8, 0.8], "farbe": 3, "pfeil": True, "beschriftung": "v = 4 m/s", "beschriftung_bei": [-0.8, 0.9]},
              {"von": [0, 0.8], "bis": [0, 0.15], "farbe": 4, "pfeil": True}],
    punkte=[{"x": 0, "y": 0.8, "farbe": 5}],
    texte=[{"bei": [0.1, 0.55], "text": "20 m/s² zur Mitte", "farbe": 4, "groesse": 28}])))
# F5: gleich lange Pfeile, Richtung dreht
st = []
for wg in (90, 160, 230, 300, 20):
    w = math.radians(wg); px_, py_ = math.cos(w), math.sin(w)
    st.append({"von": [round(px_, 4), round(py_, 4)], "bis": [round(px_ - 0.55 * py_, 4), round(py_ + 0.55 * px_, 4)], "farbe": 3, "pfeil": True})
setze(d, 'Frage 5', A(graf([-1.7, 1.7], [-1.7, 1.7], [], [], '', '', pfeile=False,
    kurven=kreis(0, 0, 1, farbe=5, dicke=4), strecken=st,
    punkte=[{"x": round(math.cos(math.radians(wg)), 4), "y": round(math.sin(math.radians(wg)), 4), "farbe": 5} for wg in (90, 160, 230, 300, 20)],
    texte=[{"bei": [-1.6, -1.6], "text": "gleich lang, andere Richtung", "farbe": 3, "groesse": 26}])))
speichere('p4-1-lp-kontrolle-kreis', d)
print('ok')
