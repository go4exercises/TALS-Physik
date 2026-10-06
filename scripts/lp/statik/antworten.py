"""Antwortbilder der Statik-Kontrollclips (06.10.2026).

Jede Antwortszene «Frage n» bekommt rechts ein Bild (x 1010, y 175, 760 x 760), das
die Antwort zeigt. Wiederholbar: Elemente mit "antwort": true werden zuerst entfernt.
Alle Fenster quadratisch (gleiche Spannweite in x und y): Kraftpläne 1:1.

Farben (Theme begreifbar-schlicht, angelehnt an README Statik / Themenseite 4.4):
  1 Bernstein  Gewichtskraft, Last
  2 Orange     Einzel-, Seil-, Zug-, Handkräfte (Seite: Blau), Haftreibung (Seite: Türkis)
  3 Grün       Normalkraft, Auflagerkraft
  4 Rot        Resultierende
  5 Tinte      Komponenten, Hebelarme, Hilfslinien, Bauteile
"""
import os
import json, math

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
G_ = 9.81
GEW, KRAFT, NORM, RES, TINTE = 1, 2, 3, 4, 5


def fmt(v):
    return ('%g' % v).replace('-', '−')


def graf(xb, yb, ein=1.0, xt=None, yt=None, xname='', yname='', **kw):
    assert abs((xb[1] - xb[0]) - (yb[1] - yb[0])) < 1e-9, 'Fenster nicht quadratisch'
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "xbereich": xb, "ybereich": yb}
    if xt is None:
        g.update(achsen=False, pfeile=False)
    else:
        g.update(pfeile=True, xteilung=[[v, fmt(v)] for v in xt], yteilung=[[v, fmt(v)] for v in yt],
                 xname=xname, yname=yname)
    for k, v in kw.items():
        if v:
            g[k] = v
    return g


def P(von, bis, farbe, text=None, bei=None, anker='start', **kw):
    s = {"von": [round(von[0], 4), round(von[1], 4)], "bis": [round(bis[0], 4), round(bis[1], 4)],
         "farbe": farbe, "pfeil": True}
    if text:
        s["beschriftung"] = text
        if bei:
            s["beschriftung_bei"] = [round(bei[0], 4), round(bei[1], 4)]
        s["anker"] = anker
    s.update(kw)
    return s


def L(von, bis, farbe=TINTE, text=None, bei=None, anker='start', **kw):
    s = P(von, bis, farbe, text, bei, anker, **kw)
    del s["pfeil"]
    return s


def T(bei, text, farbe=TINTE, groesse=27, anker='start', **kw):
    t = {"bei": [round(bei[0], 4), round(bei[1], 4)], "text": text, "farbe": farbe, "groesse": groesse, "anker": anker}
    t.update(kw)
    return t


def rechteck(x0, y0, x1, y1, farbe=TINTE, dicke=4):
    e = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    return [L(a, b, farbe, dicke=dicke) for a, b in zip(e, e[1:])]


def vieleck(pk, farbe=TINTE, dicke=4):
    pk = list(pk) + [pk[0]]
    return [L(a, b, farbe, dicke=dicke) for a, b in zip(pk, pk[1:])]


def kreis(cx, cy, r, farbe=5, dicke=4, gestrichelt=False):
    k = []
    for vz in (1, -1):
        k.append({"formel": "%g%+g*sqrt(abs(%g-(x-(%g))*(x-(%g))))" % (cy, vz, r * r, cx, cx), "von": cx - r, "bis": cx + r,
                  "farbe": farbe, "dicke": dicke, "n": 600, **({"gestrichelt": True} if gestrichelt else {})})
    return k


def bogen(cx, cy, r, w0, w1, farbe=TINTE, dicke=3, n=24):
    """Winkelbogen als Streckenzug (Grad, gegen den Uhrzeigersinn von w0 bis w1)."""
    pk = [(cx + r * math.cos(math.radians(w0 + (w1 - w0) * i / n)), cy + r * math.sin(math.radians(w0 + (w1 - w0) * i / n)))
          for i in range(n + 1)]
    return [L(a, b, farbe, dicke=dicke) for a, b in zip(pk, pk[1:])]


def lager(x, y, h=0.45, farbe=TINTE):
    """Auflager-/Drehpunktdreieck mit Spitze bei (x, y)."""
    return vieleck([(x, y), (x - h * 0.7, y - h), (x + h * 0.7, y - h)], farbe, 4)


def masz(a, b, text, versatz, farbe=TINTE, anker='middle', tbei=None):
    """Masslinie zwischen a und b (waagrecht), um versatz in y verschoben."""
    y = a[1] + versatz
    s = [L((a[0], y), (b[0], y), farbe, gestrichelt=True, dicke=3),
         L((a[0], y - 0.12), (a[0], y + 0.12), farbe, dicke=3), L((b[0], y - 0.12), (b[0], y + 0.12), farbe, dicke=3)]
    s[0]["beschriftung"] = text
    s[0]["beschriftung_bei"] = list(tbei) if tbei else [(a[0] + b[0]) / 2, y + (0.2 if versatz > 0 else -0.55)]
    s[0]["anker"] = anker
    return s


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


def ohne_alte_antworten(d):
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]


def A(el):
    el['antwort'] = True
    return el


def formelgroesse(d, szene, groesse):
    for s in d['szenen']:
        if s['name'] == szene:
            for e in s['elemente']:
                if e['typ'] == 'formel':
                    e['groesse'] = groesse


# ======================================================== Vektor
d = lade('p4-4-lp-kontrolle-vektor'); ohne_alte_antworten(d)
# F1: Kiste, Kraft 40 N unter 30° am Angriffspunkt; Länge = Betrag (Massstab 10 N)
w = math.radians(30); ap = (1.6, 3.0); sp = (ap[0] + 4 * math.cos(w), ap[1] + 4 * math.sin(w))
setze(d, 'Frage 1', A(graf([-1, 9], [-1, 9],
    strecken=rechteck(-0.4, 2.0, 1.6, 4.0)
    + [L(ap, (ap[0] + 3.0, ap[1]), gestrichelt=True)]
    + bogen(ap[0], ap[1], 1.45, 0, 30)
    + [L((ap[0] - 1.6 * math.cos(w), ap[1] - 1.6 * math.sin(w)), (sp[0] + 1.6 * math.cos(w), sp[1] + 1.6 * math.sin(w)),
         gestrichelt=True, dicke=2),
       P(ap, sp, KRAFT, "Betrag: 40 N", (3.2, 5.25), dicke=6),
       L((0, 0.2), (1, 0.2), KRAFT, "Massstab: 10 N", (-0.3, -0.45), dicke=5),
       L((0, 0.05), (0, 0.35), KRAFT, dicke=3), L((1, 0.05), (1, 0.35), KRAFT, dicke=3)],
    punkte=[{"x": ap[0], "y": ap[1], "farbe": TINTE}],
    texte=[T((3.25, 3.25), "Richtung: 30°"), T((1.9, 2.45), "Angriffspunkt"), T((-0.3, 8.2), "Kraft = Pfeil:", groesse=30),
           T((-0.3, 7.5), "Länge, Richtung, Fusspunkt", groesse=27)])))
# F2: 200 N senkrecht nach oben, Schatten auf der x-Achse ist ein Punkt
setze(d, 'Frage 2', A(graf([-135, 135], [-40, 230], xt=[-100, 100], yt=[50, 100, 150], xname='x [N]', yname='y [N]',
    strecken=[P((0, 0), (0, 200), KRAFT, "200 N", (12, 120), dicke=6)],
    punkte=[{"x": 0, "y": 0, "farbe": RES, "beschriftung": "x-Komponente 0 N", "beschriftung_bei": [8, -33]}],
    texte=[T((-110, 175), "φ = 90°", groesse=29), T((-110, 145), "cos 90° = 0", groesse=29)])))
# F3: 40 N unter 30°, Komponenten 34.6 N und 20 N
fx, fy = 40 * math.cos(w), 40 * math.sin(w)
assert abs(fy - 20) < 1e-9 and abs(fx - 34.641) < 1e-3
setze(d, 'Frage 3', A(graf([-6, 46], [-16, 36], xt=[40], yt=[-10, 10, 20, 30], xname='x [N]', yname='y [N]',
    strecken=[P((0, 0), (fx, fy), KRAFT, "40 N", (13, 11.5), dicke=6),
              L((fx, 0), (fx, -1.2), TINTE, dicke=2), L((0, 0), (0, -1.2), TINTE, dicke=2),
              P((0, -1.2), (fx, -1.2), TINTE, "34.6 N", (17.3, -5), "middle", gestrichelt=True, dicke=4),
              P((fx, 0), (fx, fy), RES, "20 N", (fx + 1.2, 9), dicke=5)]
    + bogen(0, 0, 9, 0, 30),
    texte=[T((10, 1.8), "30°", groesse=25), T((20, 29), "senkrecht: Sinus", RES, groesse=29)])))
# F4: Pfeil nach links unten, beide Komponenten negativ
setze(d, 'Frage 4', A(graf([-45, 25], [-50, 20], xt=[-40, -20, 20], yt=[-40, -20], xname='x [N]', yname='y [N]',
    strecken=[P((0, 0), (-32, -24), KRAFT, "Kraft", (-12, -20), "start", dicke=6),
              P((0, 0), (-32, 0), RES, "x-Komponente < 0", (-30, 4), dicke=4, gestrichelt=True),
              P((-32, 0), (-32, -24), RES, "y-Komponente < 0", (-30, -33), dicke=4, gestrichelt=True)])))
# F5: 9 N und 12 N, Betrag 15 N
setze(d, 'Frage 5', A(graf([-3, 17], [-3, 17], xt=[12, 15], yt=[3, 6, 9, 12, 15], xname='x [N]', yname='y [N]',
    strecken=[L((9, 0), (9, -0.6), TINTE, dicke=2), L((0, 0), (0, -0.6), TINTE, dicke=2),
              P((0, -0.6), (9, -0.6), TINTE, "9 N", (4.5, -1.9), "middle", gestrichelt=True, dicke=4),
              P((9, 0), (9, 12), TINTE, "12 N", (9.4, 5.5), gestrichelt=True, dicke=4),
              P((0, 0), (9, 12), KRAFT, "15 N", (3.4, 7.3), "end", dicke=6)],
    texte=[T((5.5, 15.6), "9² + 12² = 225 = 15²", groesse=28)])))
speichere('p4-4-lp-kontrolle-vektor', d)

# ======================================================== Resultierende
d = lade('p4-4-lp-kontrolle-resultierende'); ohne_alte_antworten(d)
# F1: 30 N und 40 N gleich gerichtet, Spitze an Fuss: 70 N
setze(d, 'Frage 1', A(graf([-8, 82], [-45, 45],
    strecken=[P((0, 12), (30, 12), KRAFT, "30 N", (15, 16), "middle", dicke=6),
              P((30, 12), (70, 12), KRAFT, "40 N", (50, 16), "middle", dicke=6),
              L((0, 14), (0, -10), TINTE, gestrichelt=True, dicke=2), L((70, 14), (70, -10), TINTE, gestrichelt=True, dicke=2),
              P((0, -6), (70, -6), RES, "Resultierende 70 N", (35, -15), "middle", dicke=6)],
    punkte=[{"x": 0, "y": 12, "farbe": TINTE}],
    texte=[T((0, 32), "Spitze an Fuss: Beträge addieren", groesse=27)])))
# F2: 120 N und 35 N rechtwinklig, Kräfteparallelogramm 1:1
assert abs(math.hypot(35, 120) - 125) < 1e-9
setze(d, 'Frage 2', A(graf([-15, 140], [-40, 115], xt=[40, 80, 120], yt=[40, 80], xname='x [N]', yname='y [N]',
    strecken=[L((120, 0), (120, 35), TINTE, gestrichelt=True), L((0, 35), (120, 35), TINTE, gestrichelt=True),
              P((0, 0), (120, 0), KRAFT, "120 N", (70, -14), "middle", dicke=6),
              P((0, 0), (0, 35), KRAFT, "35 N", (4, 45), dicke=6),
              P((0, 0), (120, 35), RES, "125 N", (90, 12), "start", dicke=6)],
    texte=[T((4, 60), "35² + 120² = 125²", groesse=28)])))
# F3: drei Kräfte 80 N, Spitze an Fuss: geschlossenes Dreieck (wie Clip und Simulation)
v = [(80 * math.cos(math.radians(a)), 80 * math.sin(math.radians(a))) for a in (90, 210, 330)]
p0 = (20, -40); p1 = (p0[0] + v[0][0], p0[1] + v[0][1]); p2 = (p1[0] + v[1][0], p1[1] + v[1][1]); p3 = (p2[0] + v[2][0], p2[1] + v[2][1])
assert math.dist(p3, p0) < 1e-9
setze(d, 'Frage 3', A(graf([-75, 75], [-75, 75],
    strecken=[P(p0, p1, KRAFT, "80 N", (p0[0] + 5, 0), dicke=6), P(p1, p2, KRAFT, "80 N", (-20, 26), "end", dicke=6),
              P(p2, p0, KRAFT, "80 N", (-12, -36), "middle", dicke=6)],
    punkte=[{"x": p0[0], "y": p0[1], "farbe": RES, "beschriftung": "Start = Ende", "beschriftung_bei": [p0[0] + 8, p0[1] - 12]}],
    texte=[T((-70, 62), "Resultierende: 0 N", RES, groesse=30)])))
# F4: 50 N und 40 N entgegengesetzt: 10 N
setze(d, 'Frage 4', A(graf([-55, 65], [-60, 60],
    strecken=[P((0, 15), (50, 15), KRAFT, "50 N", (25, 20), "middle", dicke=6),
              P((0, 15), (-40, 15), KRAFT, "40 N", (-20, 20), "middle", dicke=6),
              L((10, 15), (10, -14), TINTE, gestrichelt=True, dicke=2), L((0, 15), (0, -14), TINTE, gestrichelt=True, dicke=2),
              P((0, -10), (10, -10), RES, "Resultierende 10 N", (5, -24), "middle", dicke=6)],
    punkte=[{"x": 0, "y": 15, "farbe": TINTE}],
    texte=[T((-50, 45), "kleiner als jede Einzelkraft", groesse=28)])))
# F5: Ring, 60 N rechts, 60 N links, 25 N oben
setze(d, 'Frage 5', A(graf([-75, 75], [-80, 70],
    kurven=kreis(0, 10, 4, TINTE, 4) + kreis(0, -55, 4, TINTE, 4),
    strecken=[P((4, 10), (64, 10), KRAFT, "60 N", (34, 15), "middle", dicke=6),
              P((-4, 10), (-64, 10), KRAFT, "60 N", (-34, 15), "middle", dicke=6),
              P((0, 14), (0, 39), KRAFT, "25 N", (4, 30), dicke=6),
              P((0, -51), (0, -26), RES, dicke=6)],
    texte=[T((0, -73), "Resultierende 25 N nach oben", RES, groesse=27, anker="middle"), T((0, -5), "60 N − 60 N = 0", groesse=27, anker="middle")])))
speichere('p4-4-lp-kontrolle-resultierende', d)

# ======================================================== Ruhe
d = lade('p4-4-lp-kontrolle-ruhe'); ohne_alte_antworten(d)


def rampe(al, x0, x1, y0=0.0):
    """Rampe ab (x0, y0) mit Neigung al (Grad) bis x1; liefert Linien und Richtungen."""
    a = math.radians(al)
    top = (x1, y0 + (x1 - x0) * math.tan(a))
    linien = vieleck([(x0, y0), (x1, y0), top], TINTE, 4)
    ab = (-math.cos(a), -math.sin(a))      # hangabwärts
    n = (-math.sin(a), math.cos(a))        # aus der Fläche heraus
    return linien, ab, n


def kiste(al, x0, s_, kante, y0=0.0):
    """Kiste der Kante kante auf der Rampe, Unterkante bei Weglänge s_ ab (x0, y0)."""
    a = math.radians(al); t = (math.cos(a), math.sin(a)); n = (-math.sin(a), math.cos(a))
    p = (x0 + s_ * t[0], y0 + s_ * t[1])
    e = [p, (p[0] + kante * t[0], p[1] + kante * t[1]),
         (p[0] + kante * t[0] + kante * n[0], p[1] + kante * t[1] + kante * n[1]), (p[0] + kante * n[0], p[1] + kante * n[1])]
    m = (p[0] + kante / 2 * (t[0] + n[0]), p[1] + kante / 2 * (t[1] + n[1]))
    auf = (p[0] + kante / 2 * t[0], p[1] + kante / 2 * t[1])
    return vieleck(e, TINTE, 4), m, auf


# F1: waagrechter Boden, Normalkraft = Gewichtskraft
setze(d, 'Frage 1', A(graf([-5, 5], [-5, 5],
    strecken=[L((-4.5, -1), (4.5, -1), TINTE, dicke=5)] + rechteck(-1.2, -1, 1.2, 1.4)
    + [P((0.2, 0.2), (0.2, -2.8), GEW, "Gewichtskraft", (0.45, -2.55), dicke=6),
       P((-0.2, -1), (-0.2, 2.0), NORM, "Normalkraft", (-0.45, 2.3), "end", dicke=6)],
    texte=[T((-4.5, 4.0), "gleich lang, entgegengesetzt", groesse=28), T((-4.5, -1.6), "Boden", groesse=26)])))
# F2: Rampe 10°, 50 kg: F_G = 490.5 N, F_H = 85.2 N, senkrecht 483.0 N (1 Einheit = 111.1 N)
al = 10; a = math.radians(al)
FG = 50 * G_; FH = FG * math.sin(a); FS = FG * math.cos(a)
assert abs(FH - 85.17) < 0.01 and abs(FS - 483.05) < 0.01
lin, ab, n = rampe(al, -4.8, 4.8, -0.6)
kl, m, auf = kiste(al, -4.8, 3.6, 1.5, -0.6)
sk = 0.009  # Einheiten je N
eH = (m[0] + FH * sk * ab[0], m[1] + FH * sk * ab[1]); eS = (m[0] - FS * sk * n[0], m[1] - FS * sk * n[1])
eG = (m[0], m[1] - FG * sk)
assert math.dist(eG, (eH[0] - FS * sk * n[0], eH[1] - FS * sk * n[1])) < 1e-9
setze(d, 'Frage 2', A(graf([-5, 5], [-5.4, 4.6],
    strecken=lin + kl + [L(eH, eG, TINTE, gestrichelt=True, dicke=2), L(eS, eG, TINTE, gestrichelt=True, dicke=2),
       P(m, eG, GEW, dicke=6),
       P(m, eS, TINTE, gestrichelt=True, dicke=4),
       P(m, eH, RES, dicke=6)]
    + bogen(-4.8, -0.6, 1.6, 0, al),
    texte=[T((-2.9, -0.45), "10°", groesse=25),
           T((eG[0] - 0.25, eG[1] + 0.9), "Gewichtskraft", GEW, groesse=26, anker="end"),
           T((eG[0] - 0.25, eG[1] + 0.45), "490.5 N", GEW, groesse=26, anker="end"),
           T((eS[0] + 0.25, eS[1] + 0.9), "senkrecht zur", TINTE, groesse=26),
           T((eS[0] + 0.25, eS[1] + 0.45), "Rampe 483 N", TINTE, groesse=26),
           T((eH[0] - 0.2, eH[1] - 0.1), "Hangabtrieb 85.2 N", RES, groesse=27, anker="end")])))
# F3: Kiste ruht, Hangabtrieb 40 N, Haftreibung 40 N (höchstens 70 N); 1 Einheit = 15 N
al = 20
lin, ab, n = rampe(al, -4.8, 4.8, -3.5)
kl, m, auf = kiste(al, -4.8, 3.4, 1.4, -3.5)
sk = 1 / 15
t_ = (-ab[0], -ab[1])
eH = (m[0] + 40 * sk * ab[0], m[1] + 40 * sk * ab[1])
r0 = (auf[0] + 0.05 * n[0], auf[1] + 0.05 * n[1])
eR = (r0[0] + 40 * sk * t_[0], r0[1] + 40 * sk * t_[1]); eRmax = (r0[0] + 70 * sk * t_[0], r0[1] + 70 * sk * t_[1])
setze(d, 'Frage 3', A(graf([-5, 5], [-5, 5],
    strecken=lin + kl + [
       L(eR, eRmax, KRAFT, gestrichelt=True, dicke=3),
       P(m, eH, TINTE, dicke=6),
       P(r0, eR, KRAFT, dicke=6)],
    punkte=[{"x": round(eRmax[0], 4), "y": round(eRmax[1], 4), "farbe": KRAFT}],
    texte=[T((-4.7, -0.7), "Hangabtrieb 40 N", TINTE, groesse=27),
           T((0.2, -2.4), "Haftreibung 40 N", KRAFT, groesse=27),
           T((eRmax[0] + 0.2, eRmax[1] + 0.5), "höchstens 70 N", KRAFT, groesse=25, anker="end"),
           T((-4.7, 3.0), "so viel wie nötig: 40 N", KRAFT, groesse=29)])))
# F4: Grenzwinkel arctan 0.25 = 14.0°, Steigungsdreieck 4 m : 1 m
ag = math.degrees(math.atan(0.25)); assert abs(ag - 14.04) < 0.01
setze(d, 'Frage 4', A(graf([-0.6, 5.2], [-2.4, 3.4],
    strecken=[L((0, 0), (4.8, 1.2), TINTE, dicke=5),
              L((0, 0), (4, 0), TINTE, "4 m", (2, -0.32), "middle", gestrichelt=True, dicke=3),
              L((4, 0), (4, 1), RES, "1 m", (4.12, 0.42), dicke=4)]
    + bogen(0, 0, 1.3, 0, ag),
    texte=[T((1.4, 0.1), "14.0°", groesse=25), T((0, 2.7), "tan α = 1 m : 4 m = 0.25", groesse=29),
           T((0, -1.25), "steiler als 14.0°: rutscht", groesse=27), T((0, -1.75), "flacher: haftet", groesse=27)])))
# F5: 20° gegen Grenzwinkel arctan 0.5 = 26.6°
ag = math.degrees(math.atan(0.5)); assert abs(ag - 26.57) < 0.01 and math.tan(math.radians(20)) < 0.5
lg = 4.8
setze(d, 'Frage 5', A(graf([-0.6, 5.4], [-1.6, 4.4],
    strecken=[L((0, 0), (lg, 0), TINTE, dicke=4),
              L((0, 0), (lg * math.cos(math.radians(ag)), lg * math.sin(math.radians(ag))), RES,
                "Grenze 26.6°", (lg * math.cos(math.radians(ag)) - 0.1, lg * math.sin(math.radians(ag)) + 0.2), "end",
                gestrichelt=True, dicke=3),
              L((0, 0), (lg * math.cos(math.radians(20)), lg * math.sin(math.radians(20))), NORM,
                "Rampe 20°", (lg * math.cos(math.radians(20)) + 0.05, lg * math.sin(math.radians(20)) - 0.55), "end", dicke=5)]
    + kiste(20, 0, 2.6, 0.7)[0] + bogen(0, 0, 1.2, 0, 20, NORM) + bogen(0, 0, 1.75, 0, ag, RES, 2),
    texte=[T((0, 3.8), "tan 20° ≈ 0.364 < 0.5", groesse=29), T((0, -0.9), "20° < 26.6°: haftet", NORM, groesse=29)])))
speichere('p4-4-lp-kontrolle-ruhe', d)

# ======================================================== Drehmoment
d = lade('p4-4-lp-kontrolle-drehmoment'); ohne_alte_antworten(d)
# F1: 50 N senkrecht, 0.3 m: 15 Nm
setze(d, 'Frage 1', A(graf([-1, 5], [-3.5, 2.5],
    kurven=kreis(0, 0, 0.12, TINTE, 4),
    strecken=[L((0, 0), (4, 0), TINTE, dicke=9), L((3, -0.15), (3, 0.15), TINTE, dicke=3)]
    + masz((0, 0), (3, 0), "0.3 m", 0.7, tbei=(1.5, 0.9))
    + [P((3, 0), (3, -2.5), KRAFT, "50 N", (3.15, -1.6), dicke=6)],
    punkte=[{"x": 0, "y": 0, "farbe": TINTE, "beschriftung": "Drehachse", "beschriftung_bei": [-0.4, -0.65]}],
    texte=[T((-0.6, 2.0), "M = 50 N · 0.3 m = 15 Nm", groesse=29)])))
# F2: schräge Kraft am Hebel; wirksamer Hebelarm = Lot auf die Wirkungslinie
Pk = (4, 0); u = (0.5, -math.sqrt(3) / 2)
fu = (Pk[0] - 2 * u[0], Pk[1] - 2 * u[1])
assert abs(math.hypot(*fu) - 4 * math.sqrt(3) / 2) < 1e-9 and abs(fu[0] * u[0] + fu[1] * u[1]) < 1e-9
aa = (-fu[0] / math.hypot(*fu), -fu[1] / math.hypot(*fu)); bb = (-u[0], -u[1]); q = 0.3
setze(d, 'Frage 2', A(graf([-1, 6], [-3.6, 3.4],
    strecken=[L((0, 0), Pk, TINTE, dicke=9),
              L((Pk[0] - 3 * u[0], Pk[1] - 3 * u[1]), Pk, KRAFT, "Wirkungslinie", (2.55, 2.95), "start", gestrichelt=True, dicke=3),
              P(Pk, (Pk[0] + 2.6 * u[0], Pk[1] + 2.6 * u[1]), KRAFT, "Kraft", (5.35, -2.0), dicke=6),
              L((0, 0), fu, RES, dicke=5),
              L((fu[0] + q * aa[0], fu[1] + q * aa[1]), (fu[0] + q * aa[0] + q * bb[0], fu[1] + q * aa[1] + q * bb[1]), RES, dicke=2),
              L((fu[0] + q * bb[0], fu[1] + q * bb[1]), (fu[0] + q * aa[0] + q * bb[0], fu[1] + q * aa[1] + q * bb[1]), RES, dicke=2)]
    + masz((0, 0), Pk, "Länge des Hebels", -0.75, tbei=(2, -1.35)),
    kurven=kreis(0, 0, 0.12, TINTE, 4),
    punkte=[{"x": 0, "y": 0, "farbe": TINTE, "beschriftung": "Drehachse", "beschriftung_bei": [-0.9, -0.45]}],
    texte=[T((0.55, 1.6), "wirksamer", RES, groesse=28, anker="end"), T((0.55, 1.2), "Hebelarm", RES, groesse=28, anker="end")])))
# F3: Einheit: N mal m
setze(d, 'Frage 3', A(graf([-1, 5], [-3.5, 2.5],
    kurven=kreis(0, 0, 0.12, TINTE, 4),
    strecken=[L((0, 0), (3.6, 0), TINTE, dicke=9)]
    + masz((0, 0), (3.6, 0), "Hebelarm in m", 0.7, tbei=(1.8, 0.9))
    + [P((3.6, 0), (3.6, -2.2), KRAFT, "Kraft in N", (3.45, -1.5), "end", dicke=6)],
    punkte=[{"x": 0, "y": 0, "farbe": TINTE}],
    texte=[T((-0.6, 2.0), "Kraft · Hebelarm", groesse=30), T((-0.6, -3.0), "N · m = Nm", groesse=34)])))
# F4: Schraube 24 Nm, 0.4 m: 60 N
assert abs(24 / 0.4 - 60) < 1e-9
setze(d, 'Frage 4', A(graf([-1, 5], [-3.5, 2.5],
    kurven=kreis(0, 0, 0.45, TINTE, 4),
    strecken=vieleck([(0.3, 0), (0.15, 0.26), (-0.15, 0.26), (-0.3, 0), (-0.15, -0.26), (0.15, -0.26)], TINTE, 3)
    + [L((0.45, 0), (4, 0), TINTE, dicke=12)]
    + masz((0, 0), (4, 0), "0.4 m", 0.8, tbei=(2, 1.0))
    + [P((4, 0), (4, -2.6), KRAFT, "60 N", (4.15, -1.6), dicke=6)],
    texte=[T((-0.6, 2.0), "24 Nm : 0.4 m = 60 N", groesse=29), T((0, -0.95), "Schraube", groesse=25, anker="middle")])))
# F5: Radkreuz: langer Arm, kleine Kraft
setze(d, 'Frage 5', A(graf([-4, 4], [-4, 4],
    kurven=kreis(0, 0, 0.35, TINTE, 4),
    strecken=[L((-3, 0), (3, 0), TINTE, dicke=10), L((0, -3), (0, 3), TINTE, dicke=10),
              P((3, 0), (3, 1.0), KRAFT, "kleine Kraft", (3.15, 1.3), "end", dicke=6),
              P((-3, 0), (-3, -1.0), KRAFT, "kleine Kraft", (-3.15, -1.6), "start", dicke=6)]
    + masz((0, 0), (3, 0), "langer Arm", -0.55, RES, tbei=(1.5, -1.1)),
    texte=[T((-3.8, 3.4), "M = F · r", groesse=30), T((-3.8, 2.8), "grosses r: kleines F", groesse=28)])))
speichere('p4-4-lp-kontrolle-drehmoment', d)

# ======================================================== Hebel
d = lade('p4-4-lp-kontrolle-hebel'); ohne_alte_antworten(d)
SK = 1 / 200  # Einheiten je N


def wippe(x0, x1, farbe=TINTE):
    return [L((x0, 0), (x1, 0), farbe, dicke=9)] + lager(0, -0.06, 0.5)


def last(x, masse, text_bei=None, breite=0.55):
    """Klotz auf der Wippe, Gewichtskraft ab dem Balken nach unten."""
    h = 0.3 + masse / 100
    st = rechteck(x - breite / 2, 0.06, x + breite / 2, 0.06 + h, TINTE, 3)
    st.append(P((x, 0), (x, -masse * G_ * SK), GEW, dicke=6))
    tx = [T(text_bei or (x, 0.18 + h), "%g kg" % masse, groesse=26, anker="middle")]
    return st, tx


# F1: 20 kg bei 2 m, 50 kg bei 0.8 m
assert abs(20 * 2 / 50 - 0.8) < 1e-12
s1, t1 = last(-2, 20); s2, t2 = last(0.8, 50)
setze(d, 'Frage 1', A(graf([-3, 3], [-3.5, 2.5],
    strecken=wippe(-2.6, 2.6) + s1 + s2 + masz((-2, 0), (0, 0), "2 m", -1.25, tbei=(-1.0, -1.7))
    + masz((0, 0), (0.8, 0), "0.8 m", -1.25, tbei=(0.4, -1.7)),
    texte=t1 + t2 + [T((-2.8, 2.0), "20 kg · 2 m = 50 kg · 0.8 m", groesse=28)])))
# F2: gleich schwer, eines weiter aussen: kippt nach aussen (Drehpfeil im Uhrzeigersinn)
setze(d, 'Frage 2', A(graf([-3, 3], [-3.5, 2.5],
    strecken=wippe(-2.6, 2.6) + last(-1.0, 30)[0] + last(2.2, 30)[0]
    + masz((-1.0, 0), (0, 0), "kurz", -0.75, tbei=(-0.5, -1.2)) + masz((0, 0), (2.2, 0), "lang", -0.75, tbei=(1.1, -1.2))
    + bogen(0, 0, 1.15, 125, 45, RES, 3) + [P((1.15 * math.cos(math.radians(50)), 1.15 * math.sin(math.radians(50))),
                                            (1.15 * math.cos(math.radians(38)), 1.15 * math.sin(math.radians(38))), RES, dicke=3, spitze=18)],
    texte=last(-1.0, 30)[1] + last(2.2, 30)[1]
    + [T((-2.8, 2.1), "gleiche Kraft, längerer Arm:", groesse=28), T((-2.8, 1.65), "grösseres Moment, kippt nach rechts", RES, groesse=26)])))
# F3: Brechstange, Kraftarm 5-mal Lastarm: Kraft = Last / 5
setze(d, 'Frage 3', A(graf([-1.6, 5.4], [-4.0, 3.0],
    strecken=[L((-1, 0), (5, 0), TINTE, dicke=9)] + lager(0, -0.06, 0.45)
    + [P((-1, 2.5), (-1, 0.05), GEW, "Last", (-0.85, 1.5), dicke=6),
       P((5, 0.5), (5, 0.05), KRAFT, "Last : 5", (4.85, 0.75), "end", dicke=6)]
    + masz((-1, 0), (0, 0), "1 Teil", -0.8, tbei=(-0.5, -1.3)) + masz((0, 0), (5, 0), "5 Teile", -0.8, tbei=(2.5, -1.3)),
    texte=[T((-0.5, -1.85), "Lastarm", groesse=25, anker="middle"), T((2.5, -1.85), "Kraftarm", groesse=25, anker="middle"),
           T((-1.4, -3.2), "Last · 1 = Kraft · 5", groesse=29)])))
# F4: Schubkarre, Last näher an der Radachse: Kraft an den Griffen kleiner
# Beispiel: Last-Pfeil 2.6, Kraftarm 5; Lastarm 2 -> 1.04, Lastarm 1 -> 0.52
setze(d, 'Frage 4', A(graf([-1.2, 6.8], [-3.8, 4.2],
    kurven=kreis(0, 0, 0.6, TINTE, 4),
    strecken=[L((0, 0), (5, 0.0), TINTE, dicke=9),
              P((2, 0.05), (2, -2.6), GEW, "vorher", (2.12, -2.2), gestrichelt=True, dicke=4),
              P((1, 0.05), (1, -2.6), GEW, "näher", (0.88, -2.2), "end", dicke=6),
              P((4.8, 0.05), (4.8, 1.09), KRAFT, "vorher", (4.65, 1.0), "end", gestrichelt=True, dicke=4),
              P((5.15, 0.05), (5.15, 0.57), KRAFT, "kleiner", (5.3, 0.25), "start", dicke=6)],
    punkte=[{"x": 0, "y": 0, "farbe": TINTE, "beschriftung": "Radachse", "beschriftung_bei": [-0.6, -1.1]}],
    texte=[T((-1.0, 3.5), "kürzerer Lastarm,", groesse=28), T((-1.0, 3.0), "gleicher Kraftarm: weniger Kraft", groesse=28)])))
# F5: 20 kg bei 1 m und 10 kg bei 2 m links, 40 kg bei 1 m rechts
assert 20 * 1 + 10 * 2 == 40 * 1
s1, t1 = last(-1, 20); s2, t2 = last(-2, 10); s3, t3 = last(1, 40)
setze(d, 'Frage 5', A(graf([-3, 3], [-3.5, 2.5],
    strecken=wippe(-2.6, 2.6) + s1 + s2 + s3 + masz((-1, 0), (0, 0), "1 m", -1.25, tbei=(-0.5, -1.7))
    + masz((-2, 0), (0, 0), "2 m", -2.3, tbei=(-1.0, -2.75)) + masz((0, 0), (1, 0), "1 m", -1.25, tbei=(0.5, -1.7)),
    texte=t1 + t2 + t3 + [T((-2.8, 2.0), "20 kg·m + 20 kg·m = 40 kg·m", groesse=28)])))
speichere('p4-4-lp-kontrolle-hebel', d)

# ======================================================== Auflager
d = lade('p4-4-lp-kontrolle-auflager'); ohne_alte_antworten(d)


def balken(x0, x1):
    return [L((x0, 0), (x1, 0), TINTE, dicke=10)]


# F1: 8 m, 400 N bei 2 m von A: F_B = 100 N, F_A = 300 N; 1 Einheit = 100 N
FB = 400 * 2 / 8; FA = 400 - FB
assert FB == 100 and FA == 300
setze(d, 'Frage 1', A(graf([-1.5, 9.5], [-5.5, 5.5],
    strecken=balken(-0.3, 8.3)
    + [P((2, 4.0), (2, 0.1), GEW, "Last 400 N", (2.2, 2.2), dicke=6),
       P((0, -3.0), (0, -0.1), NORM, "300 N", (0.2, -2.0), dicke=6),
       P((8, -1.0), (8, -0.1), NORM, "100 N", (7.8, -0.9), "end", dicke=6)]
    + masz((0, 0), (2, 0), "2 m", 0.75, tbei=(1, 0.95)) + masz((0, 0), (8, 0), "8 m", -4.0, tbei=(4, -4.55)),
    punkte=[{"x": 0, "y": 0, "farbe": NORM, "beschriftung": "A", "beschriftung_bei": [-0.75, 0.3]},
            {"x": 8, "y": 0, "farbe": NORM, "beschriftung": "B", "beschriftung_bei": [8.3, 0.3]}],
    texte=[T((-1.2, 5.0), "näher an A: A trägt mehr", NORM, groesse=28)])))
# F2: beide Bedingungen; oben Kräftepaar (Kräfte null, dreht), unten Balken in Ruhe
setze(d, 'Frage 2', A(graf([-1, 9], [-5, 5],
    strecken=[L((0.5, 2.0), (7.5, 2.0), TINTE, dicke=10),
              P((0.5, 0.6), (0.5, 1.95), KRAFT, dicke=6), P((7.5, 3.4), (7.5, 2.05), KRAFT, dicke=6),
              L((0.5, -2.5), (7.5, -2.5), TINTE, dicke=10),
              P((4, -0.9), (4, -2.45), GEW, dicke=6),
              P((0.5, -3.3), (0.5, -2.55), NORM, dicke=6), P((7.5, -3.3), (7.5, -2.55), NORM, dicke=6)]
    + bogen(4, 2.0, 1.1, 160, 25, RES, 3) + [P((4 + 1.1 * math.cos(math.radians(30)), 2 + 1.1 * math.sin(math.radians(30))),
                                               (4 + 1.1 * math.cos(math.radians(18)), 2 + 1.1 * math.sin(math.radians(18))), RES, dicke=3, spitze=18)],
    texte=[T((-0.8, 4.3), "Kräfte null, Momente nicht: dreht", RES, groesse=27),
           T((-0.8, -0.3), "Kräfte null und Momente null: ruht", NORM, groesse=27)])))
# F3: Last genau über B: F_A = 0
setze(d, 'Frage 3', A(graf([-1.5, 9.5], [-5.5, 5.5],
    strecken=balken(-0.3, 8.3)
    + [P((8, 3.5), (8, 0.1), GEW, "Last", (7.8, 2.0), "end", dicke=6),
       P((8, -3.5), (8, -0.1), NORM, "ganze Last", (7.8, -2.0), "end", dicke=6)],
    punkte=[{"x": 0, "y": 0, "farbe": NORM, "beschriftung": "A: 0 N", "beschriftung_bei": [0, -0.85], "anker": "middle"},
            {"x": 8, "y": 0, "farbe": NORM, "beschriftung": "B", "beschriftung_bei": [8.3, 0.3]}],
    texte=[T((-1.2, 5.0), "um B: kein Hebelarm", groesse=28), T((-1.2, 4.4), "A trägt nichts", NORM, groesse=28)])))
# F4: 900 N, A 600 N, B 300 N; 1 Einheit = 225 N, Last bei 2 m von A auf 6 m
assert 900 * 4 / 6 == 600 and 900 - 600 == 300
sk = 1 / 225
setze(d, 'Frage 4', A(graf([-1, 7], [-3.6, 4.4],
    strecken=balken(-0.3, 6.3)
    + [P((2, 900 * sk + 0.1), (2, 0.1), GEW, "900 N", (2.15, 2.0), dicke=6),
       P((0, -600 * sk - 0.1), (0, -0.1), NORM, "600 N", (0.15, -1.6), dicke=6),
       P((6, -300 * sk - 0.1), (6, -0.1), NORM, "300 N", (5.85, -1.0), "end", dicke=6)],
    punkte=[{"x": 0, "y": 0, "farbe": NORM, "beschriftung": "A", "beschriftung_bei": [-0.55, 0.25]},
            {"x": 6, "y": 0, "farbe": NORM, "beschriftung": "B", "beschriftung_bei": [6.25, 0.25]}],
    texte=[T((1.0, -3.2), "600 N + 300 N = 900 N", NORM, groesse=29)])))
# F5: Brücke 20 kN Eigengewicht in der Mitte: je 10 kN
setze(d, 'Frage 5', A(graf([-1.5, 11.5], [-6.5, 6.5],
    flaechen=[{"punkte": [[0, -0.25], [10, -0.25], [10, 0.25], [0, 0.25]], "farbe": GEW, "deckung": 0.9}],
    strecken=balken(-0.2, 10.2) + lager(0, -0.08, 0.5) + lager(10, -0.08, 0.5)
    + [P((5, 0), (5, -4.0), GEW, "Eigengewicht 20 kN", (5.2, -3.4), dicke=6),
       P((-0.6, -2.0), (-0.6, -0.1), NORM, "10 kN", (-0.4, -1.6), dicke=6),
       P((10.6, -2.0), (10.6, -0.1), NORM, "10 kN", (10.4, -1.6), "end", dicke=6)],
    punkte=[{"x": 5, "y": 0, "farbe": GEW, "beschriftung": "Mitte", "beschriftung_bei": [5, 0.6], "anker": "middle"}],
    texte=[T((-1.2, 5.5), "gleich weit von A und B:", groesse=28), T((-1.2, 4.8), "jede Stütze die Hälfte", NORM, groesse=28)])))
speichere('p4-4-lp-kontrolle-auflager', d)
print('ok')
