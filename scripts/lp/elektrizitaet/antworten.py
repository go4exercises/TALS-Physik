"""Antwortbilder der Kontrollclips Elektrizität (p6-2-lp-kontrolle-*, 06.10.2026).

Nach dem Muster der Kinematik (scripts/lp/kinematik/antworten.py). Jede Antwortszene
bekommt rechts ein Bild (x 1010, y 175, 760 x 760), das die Antwort zeigt.
Hat die Szene schon ein bewegtes graf (Q-t, R-l), kommt die Antwort als zweite
Ebene "achsen": false mit demselben Fenster darüber, nach der Bewegung.
Schaltskizzen und Pfeilbilder ohne Achsen im Fenster [0, 10] x [0, 10] (1:1).
Farben wie im Leitprogramm: 1 Bernstein = U, 2 Orange = I, 3 Grün = R,
4 Rot = Gefahr/Auslösen, 5 Tinte. Alle Zahlen hier gerechnet.
Wiederholbar: Elemente mit "antwort": true werden zuerst entfernt, ersetzte
Simulationsaufnahmen (bild) ebenso.
"""
import os
import json, math

R_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
E_LAD = 1.602e-19


def fmt(v):
    return ('%g' % v).replace('-', '−')


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": xb, "ybereich": yb,
         "xteilung": [[v, fmt(v)] for v in xt] or [[1e9, ""]], "yteilung": [[v, fmt(v)] for v in yt] or [[1e9, ""]],
         "xname": xname, "yname": yname}
    g.update(kw)
    return g


def skizze(ein=1.0, **kw):
    """Zeichnung ohne Achsen, Fenster 0..10 in beide Richtungen (1:1)."""
    return graf([0, 10], [0, 10], [], [], '', '', ein=ein, achsen=False, pfeile=False, **kw)


def ebene(vorlage, ein, **kw):
    """Deckungsgleiche Ebene über einem bestehenden graf (gleiches Fenster)."""
    return graf(vorlage['xbereich'], vorlage['ybereich'], [], [], '', '', ein=ein, achsen=False, pfeile=False, **kw)


def draht(a, b, **kw):
    return dict({"von": list(a), "bis": list(b), "farbe": 5, "dicke": 4}, **kw)


def widerstand(cx, cy, senkrecht=False, lang=1.7, breit=0.62, farbe=3):
    """Rechteck als Widerstandssymbol: Fläche + vier Kanten."""
    if senkrecht:
        x0, x1, y0, y1 = cx - breit / 2, cx + breit / 2, cy - lang / 2, cy + lang / 2
    else:
        x0, x1, y0, y1 = cx - lang / 2, cx + lang / 2, cy - breit / 2, cy + breit / 2
    fl = {"punkte": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], "farbe": farbe, "deckung": 0.16}
    kanten = [draht((x0, y0), (x1, y0), farbe=farbe), draht((x1, y0), (x1, y1), farbe=farbe),
              draht((x1, y1), (x0, y1), farbe=farbe), draht((x0, y1), (x0, y0), farbe=farbe)]
    return fl, kanten


def quelle(x, y):
    """Spannungsquelle in einem senkrechten Draht bei x: langer Strich oben (+), kurzer unten (−)."""
    return [draht((x - 0.6, y + 0.18), (x + 0.6, y + 0.18), farbe=1, dicke=5),
            draht((x - 0.3, y - 0.18), (x + 0.3, y - 0.18), farbe=1, dicke=9)]


def rechteck(x0, y0, x1, y1, farbe, deckung=0.22, **kw):
    return dict({"punkte": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], "farbe": farbe, "deckung": deckung}, **kw)


def rahmen(x0, y0, x1, y1, farbe=5, dicke=4):
    return [draht((x0, y0), (x1, y0), farbe=farbe, dicke=dicke), draht((x1, y0), (x1, y1), farbe=farbe, dicke=dicke),
            draht((x1, y1), (x0, y1), farbe=farbe, dicke=dicke), draht((x0, y1), (x0, y0), farbe=farbe, dicke=dicke)]


def knoten(x, y, r=0.11):
    """Kleiner gefüllter Verzweigungspunkt (Achteck)."""
    return {"punkte": [[round(x + r * math.cos(k * math.pi / 4), 4), round(y + r * math.sin(k * math.pi / 4), 4)] for k in range(8)],
            "farbe": 5, "deckung": 1}


def szene(d, name):
    for s in d['szenen']:
        if s['name'] == name:
            return s
    raise KeyError(name)


def setze(d, name, el, ersetze_bild=False):
    s = szene(d, name)
    if ersetze_bild:
        s['elemente'] = [e for e in s['elemente'] if e['typ'] != 'bild']
    el['antwort'] = True
    s['elemente'].append(el)


def vorhandener_graf(d, name):
    return next(e for e in szene(d, name)['elemente'] if e['typ'] == 'graf' and not e.get('antwort'))


def lade(n):
    d = json.load(open(R_ + n + '.json'))
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]
    return d


def speichere(n, d):
    for s_ in d['szenen']:
        if any(e['typ'] in ('graf', 'bild') for e in s_['elemente']):
            for e in s_['elemente']:
                if e['typ'] == 'formel' and len(e['text']) > 75:
                    e['groesse'] = min(e.get('groesse', 54), 40)
    with open(R_ + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


# ======================================================================== Ladung
n = 'p6-2-lp-kontrolle-ladung'
d = lade(n)
# F1: Glasstab gibt Elektronen ans Tuch ab
plus = [{"bei": [1.25 + 0.75 * k, 6.12], "text": "+", "farbe": 4, "groesse": 44, "anker": "middle"} for k in range(5)]
minus_ = [{"bei": [5.95 + 0.7 * k, 3.05], "text": "−", "farbe": 5, "groesse": 48, "anker": "middle"} for k in range(5)]
setze(d, 'Frage 1', skizze(
    flaechen=[rechteck(0.7, 5.75, 4.8, 6.95, 4, 0.12), rechteck(5.5, 2.5, 9.3, 4.2, 5, 0.10)],
    strecken=rahmen(0.7, 5.75, 4.8, 6.95, farbe=4) + rahmen(5.5, 2.5, 9.3, 4.2)
    + [{"von": [4.2, 5.4], "bis": [6.0, 4.55], "farbe": 5, "pfeil": True, "dicke": 4,
        "beschriftung": "Elektronen", "beschriftung_bei": [5.35, 5.35]}],
    texte=plus + minus_ + [
        {"bei": [0.7, 7.45], "text": "Glasstab: Elektronenmangel, positiv", "farbe": 4, "groesse": 27},
        {"bei": [5.5, 1.65], "text": "Tuch: Überschuss, negativ", "farbe": 5, "groesse": 27},
        {"bei": [0.7, 8.9], "text": "+5 und −5: zusammen null", "farbe": 5, "groesse": 30}]))
# F2: Steigungsdreieck auf der Q-t-Geraden (Steigung 2 A), nach der Bewegung
g2 = vorhandener_graf(d, 'Frage 2')
setze(d, 'Frage 2', ebene(g2, 4.2,
    strecken=[{"von": [5, 10], "bis": [8, 10], "farbe": 5, "gestrichelt": True,
               "beschriftung": "Δt = 3 s", "beschriftung_bei": [6.5, 8.0], "anker": "middle"},
              {"von": [8, 10], "bis": [8, 16], "farbe": 5, "gestrichelt": True,
               "beschriftung": "ΔQ = 6 C", "beschriftung_bei": [8.2, 12.4]}],
    texte=[{"bei": [0.3, 26.5], "text": "Steigung: 6 C : 3 s = 2 A", "farbe": 2, "groesse": 30}]))
# F3 (klick): abgelesener Punkt (6 s; 15 C), nach der Bewegung
g3 = vorhandener_graf(d, 'Frage 3')
assert abs(2.5 * 6 - 15) < 1e-12
setze(d, 'Frage 3', ebene(g3, 3.3,
    strecken=[{"von": [6, 0], "bis": [6, 15], "farbe": 5, "gestrichelt": True},
              {"von": [0, 15], "bis": [6, 15], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 6, "y": 15, "farbe": 5, "beschriftung": "(6 s; 15 C)", "beschriftung_bei": [6.35, 13.0], "anker": "start"}],
    texte=[{"bei": [0.3, 26.5], "text": "Steigung 2.5 A", "farbe": 2, "groesse": 30}]))
# F4: doppelte Zeit, doppelte Ladung auf derselben Geraden (I = 1.5 A)
g4 = vorhandener_graf(d, 'Frage 4')
assert abs(1.5 * 4 - 6) < 1e-12 and abs(1.5 * 8 - 12) < 1e-12
setze(d, 'Frage 4', ebene(g4, 3.7,
    strecken=[{"von": [4, 0], "bis": [4, 6], "farbe": 5, "gestrichelt": True},
              {"von": [0, 6], "bis": [4, 6], "farbe": 5, "gestrichelt": True},
              {"von": [8, 0], "bis": [8, 12], "farbe": 5, "gestrichelt": True},
              {"von": [0, 12], "bis": [8, 12], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 4, "y": 6, "farbe": 5, "beschriftung": "(4 s; 6 C)", "beschriftung_bei": [3.8, 7.6], "anker": "end"},
            {"x": 8, "y": 12, "farbe": 5, "beschriftung": "(8 s; 12 C)", "beschriftung_bei": [7.8, 13.6], "anker": "end"}],
    texte=[{"bei": [0.3, 26.5], "text": "doppelte Zeit → doppelte Ladung", "farbe": 5, "groesse": 30}]))
# F5: Q-n-Gerade, Steigung e; 1 C bei 6.24·10¹⁸ Elektronen
nC = 1 / E_LAD / 1e18
assert abs(nC - 6.2422) < 1e-3
setze(d, 'Frage 5', graf([-0.85, 8.6], [-0.14, 1.36], [2, 4, 6, 8], [0.5, 1], 'n [10¹⁸]', 'Q [C]',
    strecken=[{"von": [0, 0], "bis": [8.2, 8.2 * 0.1602], "farbe": 5, "dicke": 5},
              {"von": [nC, 0], "bis": [nC, 1], "farbe": 5, "gestrichelt": True},
              {"von": [0, 1], "bis": [nC, 1], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": round(nC, 4), "y": 1, "farbe": 2, "beschriftung": "(6.24·10¹⁸; 1 C)", "beschriftung_bei": [nC - 0.15, 1.07], "anker": "end"}],
    texte=[{"bei": [0.4, 1.25], "text": "je Elektron 1.602·10⁻¹⁹ C", "farbe": 5, "groesse": 27}]))
speichere(n, d)

# ==================================================================== Widerstand
n = 'p6-2-lp-kontrolle-widerstand'
d = lade(n)
# F1: R-l-Gerade (Steigung 0.05 Ω/m), 10 m -> 30 m: 0.5 Ω -> 1.5 Ω
g = vorhandener_graf(d, 'Frage 1')
setze(d, 'Frage 1', ebene(g, 1.0,
    strecken=[{"von": [10, 0], "bis": [10, 0.5], "farbe": 5, "gestrichelt": True},
              {"von": [0, 0.5], "bis": [10, 0.5], "farbe": 5, "gestrichelt": True},
              {"von": [30, 0], "bis": [30, 1.5], "farbe": 5, "gestrichelt": True},
              {"von": [0, 1.5], "bis": [30, 1.5], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 10, "y": 0.5, "farbe": 5, "beschriftung": "(10 m; 0.5 Ω)", "beschriftung_bei": [11.5, 0.22], "anker": "start"},
            {"x": 30, "y": 1.5, "farbe": 5, "beschriftung": "(30 m; 1.5 Ω)", "beschriftung_bei": [29, 1.82], "anker": "end"}],
    texte=[{"bei": [3, 4.6], "text": "3 · Länge → 3 · Widerstand", "farbe": 3, "groesse": 30}]))
# F2: halber Querschnitt: Steigung 0.05 -> 0.1 Ω/m; bei 30 m 1.5 Ω -> 3 Ω
g = vorhandener_graf(d, 'Frage 2')
setze(d, 'Frage 2', ebene(g, 1.0,
    strecken=[{"von": [0, 0], "bis": [62, 3.1], "farbe": 3, "gestrichelt": True, "dicke": 3},
              {"von": [30, 0], "bis": [30, 3], "farbe": 5, "gestrichelt": True},
              {"von": [0, 3], "bis": [30, 3], "farbe": 5, "gestrichelt": True},
              {"von": [0, 1.5], "bis": [30, 1.5], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 30, "y": 1.5, "farbe": 5, "beschriftung": "(30 m; 1.5 Ω)", "beschriftung_bei": [32, 1.05], "anker": "start"},
            {"x": 30, "y": 3, "farbe": 5, "beschriftung": "(30 m; 3 Ω)", "beschriftung_bei": [29, 3.32], "anker": "end"}],
    texte=[{"bei": [52, 2.0], "text": "voller Querschnitt", "farbe": 3, "groesse": 26, "anker": "middle"},
           {"bei": [3, 4.95], "text": "halber Querschnitt: doppelt so steil", "farbe": 3, "groesse": 28}]))
# F3: Aluminium 2.5 mm², R = 0.028/2.5 · l; 80 m Leiter (hin und zurück)
k = 0.028 / 2.5
R40, R80 = k * 40, k * 80
assert abs(R80 - 0.896) < 1e-9
setze(d, 'Frage 3', graf([-11, 104], [-0.13, 1.37], [20, 40, 60, 80, 100], [0.5, 1], 'l [m]', 'R [Ω]',
    strecken=[{"von": [0, 0], "bis": [100, 100 * k], "farbe": 3, "dicke": 5},
              {"von": [40, 0], "bis": [40, R40], "farbe": 5, "gestrichelt": True},
              {"von": [80, 0], "bis": [80, R80], "farbe": 5, "gestrichelt": True},
              {"von": [0, R80], "bis": [80, R80], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 40, "y": round(R40, 4), "farbe": 5, "beschriftung": "eine Ader: 0.45 Ω", "beschriftung_bei": [38, 0.53], "anker": "end"},
            {"x": 80, "y": round(R80, 4), "farbe": 3, "beschriftung": "(80 m; 0.90 Ω)", "beschriftung_bei": [78, 0.98], "anker": "end"}],
    texte=[{"bei": [4, 1.25], "text": "Aluminium, 2.5 mm²: hin 40 m und zurück 40 m", "farbe": 5, "groesse": 25}]))
# F4: U-I-Kennlinie, Steigung R = 60 Ω, Punkt (0.2 A; 12 V)
setze(d, 'Frage 4', graf([-0.032, 0.33], [-1.9, 19.8], [0.1, 0.2, 0.3], [5, 10, 15], 'I [A]', 'U [V]',
    strecken=[{"von": [0, 0], "bis": [0.3, 18], "farbe": 3, "dicke": 5},
              {"von": [0.2, 0], "bis": [0.2, 12], "farbe": 2, "gestrichelt": True},
              {"von": [0, 12], "bis": [0.2, 12], "farbe": 1, "gestrichelt": True}],
    punkte=[{"x": 0.2, "y": 12, "farbe": 5, "beschriftung": "(0.2 A; 12 V)", "beschriftung_bei": [0.21, 10.2], "anker": "start"}],
    texte=[{"bei": [0.015, 17.2], "text": "Steigung: 12 V : 0.2 A = 60 Ω", "farbe": 3, "groesse": 28}]))
# F5: Glühlampe (Beispiel U = 4 Ω·I + 80 Ω/A²·I³: 12 V bei 0.5 A) gegen ohmsche Gerade
fU = lambda I: 4 * I + 80 * I ** 3
a, b = 0.0, 1.0
for _ in range(60):
    m = (a + b) / 2
    a, b = (m, b) if fU(m) < 2 else (a, m)
I2 = a                      # 0.236 A bei 2 V
assert abs(fU(0.5) - 12) < 1e-12 and abs(2 / I2 - 8.47) < 0.01
setze(d, 'Frage 5', graf([-0.06, 0.62], [-1.5, 17.5], [0.2, 0.4, 0.6], [4, 8, 12], 'I [A]', 'U [V]',
    kurven=[{"formel": "4*x+80*x*x*x", "von": 0, "bis": 0.52, "farbe": 4, "dicke": 5}],
    strecken=[{"von": [0, 0], "bis": [0.6, 0.6 * 2 / I2], "farbe": 3, "gestrichelt": True},
              {"von": [0, 0], "bis": [0.6, 14.4], "farbe": 3, "gestrichelt": True}],
    punkte=[{"x": round(I2, 4), "y": 2, "farbe": 4, "beschriftung": "2 V : 0.24 A ≈ 8.5 Ω", "beschriftung_bei": [0.27, 0.75], "anker": "start"},
            {"x": 0.5, "y": 12, "farbe": 4, "beschriftung": "12 V : 0.5 A = 24 Ω", "beschriftung_bei": [0.47, 12.7], "anker": "end"}],
    texte=[{"bei": [0.06, 16.3], "text": "Glühlampe (Beispiel): U/I wächst", "farbe": 4, "groesse": 27},
           {"bei": [0.06, 15.0], "text": "gestrichelt: Steigung U/I", "farbe": 3, "groesse": 25}]))
speichere(n, d)

# ====================================================================== Leistung
n = 'p6-2-lp-kontrolle-leistung'
d = lade(n)
# F1: P-I-Gerade an 230 V, Steigung U; Punkt (2 A; 460 W)
setze(d, 'Frage 1', graf([-0.33, 3.3], [-75, 760], [1, 2, 3], [200, 400, 600], 'I [A]', 'P [W]',
    strecken=[{"von": [0, 0], "bis": [3.1, 3.1 * 230], "farbe": 1, "dicke": 5},
              {"von": [2, 0], "bis": [2, 460], "farbe": 2, "gestrichelt": True},
              {"von": [0, 460], "bis": [2, 460], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 2, "y": 460, "farbe": 5, "beschriftung": "(2 A; 460 W)", "beschriftung_bei": [2.1, 400], "anker": "start"}],
    texte=[{"bei": [0.12, 660], "text": "Steigung: U = 230 V", "farbe": 1, "groesse": 30}]))
# F2: Rechteck 2 kW · 0.5 h im P-t-Diagramm, auf der 1-kWh-Linie P · t = 1 kWh
# (ersetzt die Aufnahme der Simulation: dort 8.7 A, also 2001 W und «E ≈ 1 kWh», Beschriftung auf der Hyperbel)
setze(d, 'Frage 2', graf([-0.33, 3.3], [-0.27, 2.75], [1, 2, 3], [0.5, 1, 1.5, 2, 2.5], 't [h]', 'P [kW]',
    flaechen=[rechteck(0, 0, 0.5, 2, 4, 0.28, beschriftung="1 kWh", beschriftung_bei=[0.25, 0.95])],
    kurven=[{"formel": "1/x", "von": 0.37, "bis": 3.25, "farbe": 5, "dicke": 3, "gestrichelt": True}],
    strecken=[{"von": [0, 2], "bis": [0.5, 2], "farbe": 4, "dicke": 5}, {"von": [0.5, 2], "bis": [0.5, 0], "farbe": 4, "dicke": 4}],
    punkte=[{"x": 0.5, "y": 2, "farbe": 4, "beschriftung": "(0.5 h; 2 kW)", "beschriftung_bei": [0.62, 2.12], "anker": "start"}],
    texte=[{"bei": [1.4, 1.0], "text": "Strichlinie: P · t = 1 kWh", "farbe": 5, "groesse": 25}]), ersetze_bild=True)
# F3: W-Q-Gerade, jedes Coulomb 12 J; Punkt (5 C; 60 J)
setze(d, 'Frage 3', graf([-0.65, 6.5], [-8, 80], [1, 2, 3, 4, 5, 6], [20, 40, 60], 'Q [C]', 'W [J]',
    strecken=[{"von": [0, 0], "bis": [6.2, 74.4], "farbe": 1, "dicke": 5},
              {"von": [1, 12], "bis": [2, 12], "farbe": 5, "gestrichelt": True,
               "beschriftung": "1 C", "beschriftung_bei": [1.5, 6.5], "anker": "middle"},
              {"von": [2, 12], "bis": [2, 24], "farbe": 5, "gestrichelt": True,
               "beschriftung": "12 J", "beschriftung_bei": [2.12, 16]},
              {"von": [5, 0], "bis": [5, 60], "farbe": 5, "gestrichelt": True},
              {"von": [0, 60], "bis": [5, 60], "farbe": 5, "gestrichelt": True}],
    punkte=[{"x": 5, "y": 60, "farbe": 5, "beschriftung": "(5 C; 60 J)", "beschriftung_bei": [5.1, 52], "anker": "start"}],
    texte=[{"bei": [0.1, 73], "text": "Steigung: U = 12 V = 12 J/C", "farbe": 1, "groesse": 28}]))
# F4: Energie als Rechteckfläche im P-t-Diagramm
assert abs(1.8 / 3 - 0.6) < 1e-12 and abs(0.12 * 4 - 0.48) < 1e-12
setze(d, 'Frage 4', graf([-0.45, 4.6], [-0.22, 2.2], [1, 2, 3, 4], [0.5, 1, 1.5, 2], 't [h]', 'P [kW]',
    flaechen=[rechteck(0, 0, 1 / 3, 1.8, 4, 0.30), rechteck(0, 0, 4, 0.12, 5, 0.30)],
    strecken=[{"von": [0, 1.8], "bis": [1 / 3, 1.8], "farbe": 4, "dicke": 5},
              {"von": [1 / 3, 1.8], "bis": [1 / 3, 0], "farbe": 4, "dicke": 4},
              {"von": [0, 0.12], "bis": [4, 0.12], "farbe": 5, "dicke": 5},
              {"von": [4, 0.12], "bis": [4, 0], "farbe": 5, "dicke": 4}],
    texte=[{"bei": [0.45, 1.25], "text": "Föhn: 1.8 kW · 1/3 h = 0.6 kWh", "farbe": 4, "groesse": 27},
           {"bei": [1.0, 0.24], "text": "Fernseher: 0.12 kW · 4 h = 0.48 kWh", "farbe": 5, "groesse": 25},
           {"bei": [0.45, 1.95], "text": "Energie = Fläche: rote Fläche grösser", "farbe": 5, "groesse": 27}]))
# F5: Zähler zwischen Netz und Gerät: Ladung hin = zurück, gezählt wird Energie
setze(d, 'Frage 5', skizze(
    flaechen=[rechteck(0.4, 3.2, 2.0, 6.8, 5, 0.08), rechteck(7.9, 3.2, 9.6, 6.8, 4, 0.12), rechteck(3.9, 3.0, 5.9, 7.0, 5, 0.10)],
    strecken=rahmen(0.4, 3.2, 2.0, 6.8) + rahmen(7.9, 3.2, 9.6, 6.8, farbe=4) + rahmen(3.9, 3.0, 5.9, 7.0)
    + [draht((2.0, 6.0), (3.9, 6.0)), draht((5.9, 6.0), (7.9, 6.0)), draht((2.0, 4.0), (3.9, 4.0)), draht((5.9, 4.0), (7.9, 4.0)),
       {"von": [6.2, 6.45], "bis": [7.6, 6.45], "farbe": 2, "pfeil": True, "dicke": 4},
       {"von": [7.6, 3.55], "bis": [6.2, 3.55], "farbe": 2, "pfeil": True, "dicke": 4}],
    texte=[{"bei": [1.2, 4.85], "text": "Netz", "farbe": 5, "anker": "middle"},
           {"bei": [8.75, 4.85], "text": "Gerät", "farbe": 4, "anker": "middle"},
           {"bei": [4.9, 5.15], "text": "Zähler", "farbe": 5, "anker": "middle"},
           {"bei": [4.9, 4.45], "text": "kWh", "farbe": 5, "anker": "middle", "groesse": 30},
           {"bei": [6.9, 6.8], "text": "hin", "farbe": 2, "anker": "middle", "groesse": 25},
           {"bei": [6.9, 2.85], "text": "zurück", "farbe": 2, "anker": "middle", "groesse": 25},
           {"bei": [0.4, 8.6], "text": "Ladung: hin = zurück, nichts verbraucht", "farbe": 2, "groesse": 27},
           {"bei": [0.4, 1.6], "text": "Energie: im Gerät umgesetzt (Wärme, Licht)", "farbe": 4, "groesse": 27},
           {"bei": [0.4, 0.75], "text": "der Zähler zählt E = P · t in kWh", "farbe": 5, "groesse": 27}]))
speichere(n, d)

# =================================================================== Schaltungen
n = 'p6-2-lp-kontrolle-schaltungen'
d = lade(n)
# F1: Reihenschaltung, überall derselbe Strom 40 mA (ersetzt die Aufnahme, die nur die Spannungen zeigt)
assert abs(12 / 300 - 0.040) < 1e-12
fl1, k1 = widerstand(3.3, 7.0)
fl2, k2 = widerstand(6.7, 7.0)
setze(d, 'Frage 1', skizze(
    flaechen=[fl1, fl2],
    strecken=k1 + k2 + quelle(1.0, 5.0)
    + [draht((1.0, 7.0), (2.45, 7.0)), draht((4.15, 7.0), (5.85, 7.0)), draht((7.55, 7.0), (9.0, 7.0)),
       draht((9.0, 7.0), (9.0, 3.0)), draht((9.0, 3.0), (1.0, 3.0)), draht((1.0, 3.0), (1.0, 4.82)), draht((1.0, 5.18), (1.0, 7.0)),
       {"von": [4.4, 7.45], "bis": [5.6, 7.45], "farbe": 2, "pfeil": True, "dicke": 4},
       {"von": [9.45, 6.0], "bis": [9.45, 4.0], "farbe": 2, "pfeil": True, "dicke": 4},
       {"von": [5.6, 2.55], "bis": [4.4, 2.55], "farbe": 2, "pfeil": True, "dicke": 4}],
    texte=[{"bei": [3.3, 7.65], "text": "150 Ω", "farbe": 3, "anker": "middle"},
           {"bei": [6.7, 7.65], "text": "150 Ω", "farbe": 3, "anker": "middle"},
           {"bei": [1.75, 4.8], "text": "12 V", "farbe": 1},
           {"bei": [5.0, 7.95], "text": "40 mA", "farbe": 2, "anker": "middle"},
           {"bei": [8.75, 4.8], "text": "40 mA", "farbe": 2, "anker": "end"},
           {"bei": [5.0, 1.75], "text": "40 mA", "farbe": 2, "anker": "middle"},
           {"bei": [5.0, 9.0], "text": "Gesamtwiderstand 300 Ω", "farbe": 3, "anker": "middle", "groesse": 30},
           {"bei": [5.0, 0.6], "text": "überall derselbe Strom", "farbe": 2, "anker": "middle", "groesse": 28}]), ersetze_bild=True)
# F3: 60 Ω parallel 30 Ω wirkt wie ein Ersatzwiderstand 20 Ω (ersetzt die Aufnahme mit den Teilströmen)
assert abs(1 / (1 / 60 + 1 / 30) - 20) < 1e-9
fa, ka = widerstand(2.0, 5.0, senkrecht=True)
fb, kb = widerstand(4.2, 5.0, senkrecht=True)
fe, ke = widerstand(8.3, 5.0, senkrecht=True)
setze(d, 'Frage 3', skizze(
    flaechen=[fa, fb, fe, knoten(2.0, 7.0), knoten(2.0, 3.0)],
    strecken=ka + kb + ke
    + [draht((0.6, 7.0), (4.2, 7.0)), draht((0.6, 3.0), (4.2, 3.0)),
       draht((2.0, 7.0), (2.0, 5.85)), draht((2.0, 4.15), (2.0, 3.0)), draht((4.2, 7.0), (4.2, 5.85)), draht((4.2, 4.15), (4.2, 3.0)),
       draht((6.9, 7.0), (8.3, 7.0)), draht((6.9, 3.0), (8.3, 3.0)), draht((8.3, 7.0), (8.3, 5.85)), draht((8.3, 4.15), (8.3, 3.0))],
    texte=[{"bei": [2.45, 4.8], "text": "60 Ω", "farbe": 3},
           {"bei": [4.65, 4.8], "text": "30 Ω", "farbe": 3},
           {"bei": [8.75, 4.8], "text": "20 Ω", "farbe": 3, "groesse": 30},
           {"bei": [5.85, 4.75], "text": "=", "farbe": 5, "groesse": 48, "anker": "middle"},
           {"bei": [2.4, 7.7], "text": "parallel", "farbe": 5, "anker": "middle"},
           {"bei": [7.6, 7.7], "text": "Ersatzwiderstand", "farbe": 3, "anker": "middle"},
           {"bei": [5.0, 1.6], "text": "20 Ω: kleiner als der kleinste (30 Ω)", "farbe": 3, "anker": "middle", "groesse": 28}]), ersetze_bild=True)
# F5: Beispiel aus Frage 4 (12 V; 40 Ω und 120 Ω), dazu 60 Ω: Gesamtstrom 400 mA -> 600 mA
I1, I2_, I3 = 12 / 40 * 1000, 12 / 120 * 1000, 12 / 60 * 1000
assert (round(I1), round(I2_), round(I3)) == (300, 100, 200)
vorher, nachher = I1 + I2_, I1 + I2_ + I3
setze(d, 'Frage 5', graf([-1.5, 10.6], [-110, 790], [], [200, 400, 600], '', 'I [mA]', xteilung=[[99, ""]],
    flaechen=[rechteck(0.5, 0, 2.1, I1, 2, 0.45), rechteck(0.5, I1, 2.1, vorher, 2, 0.22),
              rechteck(5.6, 0, 7.2, I1, 2, 0.45), rechteck(5.6, I1, 7.2, vorher, 2, 0.22), rechteck(5.6, vorher, 7.2, nachher, 2, 0.70)],
    strecken=rahmen(0.5, 0, 2.1, vorher, farbe=2, dicke=3) + rahmen(5.6, 0, 7.2, nachher, farbe=2, dicke=3)
    + [draht((0.5, I1), (2.1, I1), farbe=2, dicke=3), draht((5.6, I1), (7.2, I1), farbe=2, dicke=3), draht((5.6, vorher), (7.2, vorher), farbe=2, dicke=3)],
    texte=[{"bei": [2.3, 140], "text": "40 Ω: 300 mA", "farbe": 5, "groesse": 24},
           {"bei": [2.3, 335], "text": "120 Ω: 100 mA", "farbe": 5, "groesse": 24},
           {"bei": [7.4, 140], "text": "40 Ω: 300 mA", "farbe": 5, "groesse": 24},
           {"bei": [7.4, 335], "text": "120 Ω: 100 mA", "farbe": 5, "groesse": 24},
           {"bei": [7.4, 485], "text": "neu 60 Ω:", "farbe": 2, "groesse": 24},
           {"bei": [7.4, 445], "text": "200 mA", "farbe": 2, "groesse": 24},
           {"bei": [1.3, 425], "text": "400 mA", "farbe": 2, "anker": "middle", "groesse": 30},
           {"bei": [6.4, 625], "text": "600 mA", "farbe": 2, "anker": "middle", "groesse": 30},
           {"bei": [1.3, -70], "text": "2 Zweige", "farbe": 5, "anker": "middle"},
           {"bei": [6.4, -70], "text": "3 Zweige", "farbe": 5, "anker": "middle"},
           {"bei": [0.2, 735], "text": "Beispiel an 12 V: jeder Zweig bringt Strom dazu", "farbe": 5, "groesse": 24}]))
speichere(n, d)

# ====================================================================== Gefahren
n = 'p6-2-lp-kontrolle-gefahren'
d = lade(n)
# F1: Körper als Widerstand 2.3 kΩ: I = U/R, Punkt (230 V; 100 mA), FI-Schwelle 30 mA
assert abs(230 / 2300 - 0.1) < 1e-12
setze(d, 'Frage 1', graf([-27, 262], [-12, 127], [50, 100, 150, 200, 250], [30, 60, 90, 120], 'U [V]', 'I [mA]',
    strecken=[{"von": [0, 0], "bis": [250, 250 / 2.3], "farbe": 3, "dicke": 5},
              {"von": [230, 0], "bis": [230, 100], "farbe": 1, "gestrichelt": True},
              {"von": [0, 100], "bis": [230, 100], "farbe": 2, "gestrichelt": True},
              {"von": [0, 30], "bis": [255, 30], "farbe": 4, "gestrichelt": True,
               "beschriftung": "FI-Schwelle 30 mA", "beschriftung_bei": [215, 21], "anker": "end"}],
    punkte=[{"x": 230, "y": 100, "farbe": 2, "beschriftung": "(230 V; 100 mA)", "beschriftung_bei": [220, 109], "anker": "end"}],
    texte=[{"bei": [128, 75], "text": "Körper: 2.3 kΩ", "farbe": 3, "groesse": 28, "anker": "end"}]), ersetze_bild=True)
# F2: 0.1 A neben 13 A
setze(d, 'Frage 2', graf([-1.6, 10], [-1.9, 15.3], [], [5, 10], '', 'I [A]', xteilung=[[99, ""]],
    flaechen=[rechteck(1.8, 0, 3.8, 0.1, 2, 0.9), rechteck(6.0, 0, 8.0, 13, 5, 0.18)],
    strecken=rahmen(6.0, 0, 8.0, 13, farbe=5, dicke=3) + [draht((1.8, 0.1), (3.8, 0.1), farbe=2, dicke=5)],
    texte=[{"bei": [2.8, 0.8], "text": "0.1 A", "farbe": 2, "anker": "middle", "groesse": 30},
           {"bei": [7.0, 13.6], "text": "13 A", "farbe": 5, "anker": "middle", "groesse": 30},
           {"bei": [2.8, -1.2], "text": "Körperstrom", "farbe": 2, "anker": "middle"},
           {"bei": [7.0, -1.2], "text": "LS B13", "farbe": 5, "anker": "middle"},
           {"bei": [0.5, 7.0], "text": "Der LS merkt", "farbe": 5, "groesse": 27},
           {"bei": [0.5, 6.0], "text": "nichts davon.", "farbe": 5, "groesse": 27}]))
# F3: Hinleiter trägt 8.7 + 8.7 + 3.9 = 21.3 A > 13 A; Rückleiter gleich viel -> FI bleibt ein
iw, ih, it = 2000 / 230, 2000 / 230, 900 / 230
ig = iw + ih + it
assert abs(ig - 21.3) < 0.01
setze(d, 'Frage 3', graf([-1.6, 10], [-3.6, 27.5], [], [5, 10, 15, 20, 25], '', 'I [A]', xteilung=[[99, ""]],
    flaechen=[rechteck(1.5, 0, 3.7, iw, 2, 0.55), rechteck(1.5, iw, 3.7, iw + ih, 2, 0.32), rechteck(1.5, iw + ih, 3.7, ig, 2, 0.14),
              rechteck(6.0, 0, 8.2, ig, 2, 0.32)],
    strecken=rahmen(1.5, 0, 3.7, ig, farbe=2, dicke=3) + rahmen(6.0, 0, 8.2, ig, farbe=2, dicke=3)
    + [draht((1.5, iw), (3.7, iw), farbe=2, dicke=3), draht((1.5, iw + ih), (3.7, iw + ih), farbe=2, dicke=3),
       {"von": [0, 13], "bis": [9.8, 13], "farbe": 4, "gestrichelt": True, "dicke": 4,
        "beschriftung": "LS 13 A", "beschriftung_bei": [9.8, 14.0], "anker": "end"}],
    texte=[{"bei": [2.6, 3.6], "text": "Wasserkocher", "farbe": 5, "anker": "middle", "groesse": 23},
           {"bei": [2.6, 1.0 + iw], "text": "Heizlüfter", "farbe": 5, "anker": "middle", "groesse": 23},
           {"bei": [2.6, 1.0 + iw + ih], "text": "Toaster", "farbe": 5, "anker": "middle", "groesse": 23},
           {"bei": [2.6, ig + 0.8], "text": "21.3 A", "farbe": 2, "anker": "middle", "groesse": 30},
           {"bei": [7.1, ig + 0.8], "text": "21.3 A", "farbe": 2, "anker": "middle", "groesse": 30},
           {"bei": [2.6, -1.9], "text": "hin (L)", "farbe": 5, "anker": "middle"},
           {"bei": [7.1, -1.9], "text": "zurück (N)", "farbe": 5, "anker": "middle"},
           {"bei": [7.1, 7.0], "text": "gleich viel:", "farbe": 5, "anker": "middle", "groesse": 25},
           {"bei": [7.1, 5.6], "text": "FI bleibt ein", "farbe": 5, "anker": "middle", "groesse": 25},
           {"bei": [0.2, 25.6], "text": "über 13 A: LS trennt nach einiger Zeit", "farbe": 4, "groesse": 26}]))
# F4: Schutzklasse II, doppelt isoliert (Schnitt durch ein Gerät)
setze(d, 'Frage 4', skizze(
    flaechen=[rechteck(0.8, 2.6, 9.2, 7.4, 3, 0.18), rechteck(1.8, 3.6, 8.2, 6.4, 1, 0.28)],
    strecken=rahmen(0.8, 2.6, 9.2, 7.4, farbe=3) + rahmen(1.8, 3.6, 8.2, 6.4, farbe=1)
    + [draht((0.0, 5.0), (7.6, 5.0), farbe=4, dicke=8),
       {"von": [5.6, 3.6], "bis": [6.2, 4.45], "farbe": 4, "dicke": 5},
       {"von": [6.2, 3.6], "bis": [5.6, 4.45], "farbe": 4, "dicke": 5}]
    + rahmen(8.05, 8.35, 9.35, 9.65, farbe=5, dicke=4) + rahmen(8.35, 8.65, 9.05, 9.35, farbe=5, dicke=4),
    texte=[{"bei": [2.2, 5.35], "text": "Leiter (230 V)", "farbe": 4, "groesse": 25},
           {"bei": [2.2, 3.95], "text": "Basisisolierung", "farbe": 1, "groesse": 25},
           {"bei": [1.0, 2.95], "text": "zusätzliche Isolierung", "farbe": 3, "groesse": 25},
           {"bei": [6.5, 4.1], "text": "Fehler", "farbe": 4, "groesse": 25},
           {"bei": [0.8, 8.6], "text": "Schutzklasse II", "farbe": 5, "groesse": 30},
           {"bei": [0.8, 1.6], "text": "Ein Fehler: Die zweite Schicht hält,", "farbe": 5, "groesse": 26},
           {"bei": [0.8, 0.75], "text": "das Gehäuse bleibt spannungsfrei.", "farbe": 5, "groesse": 26}]))
# F5: Auslösebereiche des unverzögerten FI (Modell der Seite: bis 15 mA nicht, 15–30 mA darf, ab 30 mA muss)
setze(d, 'Frage 5', graf([-1.6, 10], [-4.2, 42], [], [15, 20, 30, 40], '', 'I [mA]', xteilung=[[99, ""]],
    flaechen=[rechteck(0.9, 0, 9.6, 15, 3, 0.14), rechteck(0.9, 15, 9.6, 30, 2, 0.18), rechteck(0.9, 30, 9.6, 41, 4, 0.18)],
    strecken=[{"von": [0.9, 20], "bis": [3.4, 20], "farbe": 4, "dicke": 5}],
    punkte=[{"x": 3.4, "y": 20, "farbe": 4, "beschriftung": "20 mA durch den Körper", "beschriftung_bei": [3.85, 19.0], "anker": "start"}],
    texte=[{"bei": [9.4, 35], "text": "FI muss auslösen", "farbe": 4, "anker": "end"},
           {"bei": [9.4, 25.5], "text": "FI darf auslösen", "farbe": 2, "anker": "end"},
           {"bei": [9.4, 6.5], "text": "FI löst nicht aus", "farbe": 3, "anker": "end"},
           {"bei": [3.85, 16.3], "text": "kein sicherer Schutz und", "farbe": 4, "groesse": 24},
           {"bei": [3.85, 13.9], "text": "trotzdem gefährlich", "farbe": 4, "groesse": 24},
           {"bei": [0.3, -3.0], "text": "30 mA: Auslöseschwelle, keine Gefahrengrenze", "farbe": 5, "groesse": 24}]))
speichere(n, d)
print('ok')
