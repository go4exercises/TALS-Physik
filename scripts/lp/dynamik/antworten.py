"""Antwortbilder der Dynamik-Kontrollclips (06.10.2026), nach dem Muster der Kinematik.

Jede Antwortszene bekommt rechts ein Bild (x 1010, y 175, 760 x 760), Kennung "antwort": true,
damit ein zweiter Lauf die alten zuerst entfernt. Klick-Fragen (grundgesetz F4, gesamtkraft F4)
tragen schon ein graf mit bewegter Geraden: die Antwort kommt dort als deckungsgleiche Ebene ohne
Achsen darüber, erst wenn die Gerade steht (ein 3.3).

Farben nach README Dynamik: Gewichtskraft 1 Bernstein, v 3 Grün, Widerstand/Zentripetalkraft/
Gravitation zur Mitte 4 Rot, alle übrigen Kräfte und a 5 Tinte (Blau/Violett gibt es im Theme nicht).
Zweite v-Gerade zum Vergleich: 2 Orange. Kraftbilder ohne Achsen im Fenster 0..10 x 0..10 (quadratisch,
damit Kästen und Pfeillängen waagrecht wie senkrecht gleich gemessen werden).
"""
import os
import json, math

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
G_ = 9.81
BERN, ORANGE, GRUEN, ROT, TINTE = 1, 2, 3, 4, 5


def fmt(v):
    return ('%g' % v).replace('-', '−')


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": xb, "ybereich": yb,
         "xteilung": [[v, fmt(v)] for v in xt], "yteilung": [[v, fmt(v)] for v in yt],
         "xname": xname, "yname": yname}
    g.update(kw)
    return g


def bild(ein=1.0, fenster=(0, 10, 0, 10), strecken=(), texte=(), flaechen=(), kurven=(), punkte=()):
    """Zeichnung ohne Achsen (Kräfteplan, Draufsicht), quadratisches Fenster."""
    x0, x1, y0, y1 = fenster
    return graf([x0, x1], [y0, y1], [], [], '', '', ein=ein, achsen=False, pfeile=False,
                strecken=list(strecken), texte=list(texte), flaechen=list(flaechen),
                kurven=list(kurven), punkte=list(punkte))


def kreis(cx, cy, r, farbe=5, dicke=4, gestrichelt=False, nur=None):
    k = []
    for vz in (1, -1):
        if nur == 'oben' and vz < 0:
            continue
        k.append({"formel": "%g%+g*sqrt(abs(%g-(x-(%g))*(x-(%g))))" % (cy, vz, r * r, cx, cx), "von": cx - r, "bis": cx + r,
                  "farbe": farbe, "dicke": dicke, "n": 600, **({"gestrichelt": True} if gestrichelt else {})})
    return k


def kasten(x0, y0, x1, y1, farbe=TINTE, deckung=0.10, dicke=3, text=None, tgroesse=26):
    """Rechteck: Fläche + Umriss; Text in der Mitte."""
    fl = [{"punkte": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], "farbe": farbe, "deckung": deckung}]
    st = [{"von": a, "bis": b, "farbe": farbe, "dicke": dicke}
          for a, b in [([x0, y0], [x1, y0]), ([x1, y0], [x1, y1]), ([x1, y1], [x0, y1]), ([x0, y1], [x0, y0])]]
    tx = [{"bei": [(x0 + x1) / 2, (y0 + y1) / 2 - 0.17], "text": text, "farbe": farbe, "groesse": tgroesse, "anker": "middle"}] if text else []
    return fl, st, tx


def pf(von, bis, farbe=TINTE, text=None, bei=None, anker="start", gestr=False, dicke=6, groesse=27):
    s = {"von": list(von), "bis": list(bis), "farbe": farbe, "pfeil": True, "dicke": dicke}
    if gestr:
        s["gestrichelt"] = True
        s["dicke"] = 4
    if text:
        s["beschriftung"] = text
        s["beschriftung_bei"] = list(bei)
        s["anker"] = anker
        if groesse != 27:
            s["groesse"] = groesse
    return s


def li(von, bis, farbe=TINTE, gestr=False, dicke=None):
    s = {"von": list(von), "bis": list(bis), "farbe": farbe}
    if gestr:
        s["gestrichelt"] = True
    if dicke:
        s["dicke"] = dicke
    return s


def tx(bei, text, farbe=TINTE, groesse=27, anker="start"):
    return {"bei": list(bei), "text": text, "farbe": farbe, "groesse": groesse, "anker": anker}


class Z:
    """Sammelt Teile einer Zeichnung."""
    def __init__(self):
        self.st, self.tx, self.fl, self.kv, self.pt = [], [], [], [], []

    def kasten(self, *a, **k):
        f, s, t = kasten(*a, **k)
        self.fl += f; self.st += s; self.tx += t

    def bild(self, ein=1.0, fenster=(0, 10, 0, 10)):
        return bild(ein, fenster, self.st, self.tx, self.fl, self.kv, self.pt)


def setze(d, szene, el):
    for s in d['szenen']:
        if s['name'] == szene:
            s['elemente'].append(el)
            return
    raise KeyError(szene)


def lade(n):
    return json.load(open(R + n + '.json'))


def speichere(n, d):
    for s_ in d['szenen']:
        if any(e['typ'] == 'graf' for e in s_['elemente']):
            for e in s_['elemente']:
                if e['typ'] == 'formel' and len(e['text']) > 75:
                    e['groesse'] = min(e.get('groesse', 54), 40)
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def ohne_alte_antworten(d):
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]


def A(el):
    el['antwort'] = True
    return el


def r2(x):
    return round(x, 4)


# ======================================================== Grundgesetz (Kapitel 1)
d = lade('p4-2-lp-kontrolle-grundgesetz'); ohne_alte_antworten(d)

# F1: Wagen 5 kg, Gesamtkraft 15 N -> a = 3 m/s²
assert 15 / 5 == 3
z = Z()
z.st.append(li([0.4, 3.3], [9.6, 3.3], dicke=4))
z.kasten(1.6, 4.0, 4.6, 5.8, text="Wagen 5 kg")
z.kv += kreis(2.3, 3.65, 0.35, dicke=4) + kreis(3.9, 3.65, 0.35, dicke=4)
z.st.append(pf([4.6, 4.9], [9.1, 4.9], text="F = 15 N", bei=[6.85, 5.3], anker="middle"))       # 0.3 Einheiten je N
z.st.append(pf([1.6, 6.9], [4.6, 6.9], gestr=True, text="a = 3 m/s²", bei=[3.1, 7.3], anker="middle"))
z.tx += [tx([5, 1.9], "15 N : 5 kg = 3 m/s²", groesse=30, anker="middle"),
         tx([5, 8.9], "Kraft und Beschleunigung: gleiche Richtung", groesse=24, anker="middle")]
setze(d, 'Frage 1', A(z.bild()))

# F2: dreifache Kraft -> dreifache Beschleunigung
z = Z()
for y0, k, nm in ((6.0, 1, "einfach"), (1.8, 3, "Kraft verdreifacht")):
    z.st.append(li([0.4, y0], [9.6, y0], dicke=3))
    z.kasten(0.8, y0 + 0.1, 2.6, y0 + 1.4, text="m")
    z.st.append(pf([2.6, y0 + 0.75], [2.6 + 1.5 * k, y0 + 0.75], text=("F" if k == 1 else "3 · F"),
                   bei=[2.75 + 1.5 * k, y0 + 0.62]))
    z.st.append(pf([0.8, y0 + 2.0], [0.8 + 1.2 * k, y0 + 2.0], gestr=True, text=("a" if k == 1 else "3 · a"),
                   bei=[0.95 + 1.2 * k, y0 + 1.87]))
    z.tx.append(tx([0.4, y0 + 2.75], nm, groesse=25))
setze(d, 'Frage 2', A(z.bild()))

# F3: gleiche Kraft, Beispiel F = 5 N: a_A = 1 m/s², a_B = 5 m/s²
setze(d, 'Frage 3', A(graf([-0.45, 4.6], [-1.4, 13.4], [1, 2, 3, 4], [2, 4, 6, 8, 10, 12], 't [s]', 'v [m/s]',
    strecken=[{"von": [0, 0], "bis": [4.3, 4.3], "farbe": ORANGE, "dicke": 5},
              {"von": [0, 0], "bis": [2.5, 12.5], "farbe": GRUEN, "dicke": 5},
              li([1, 5], [2, 5], gestr=True), li([2, 5], [2, 10], gestr=True),
              li([3, 3], [4, 3], gestr=True), li([4, 3], [4, 4], gestr=True)],
    texte=[tx([1.5, 4.0], "1 s", anker="middle", groesse=25), tx([2.1, 7.2], "Δv = 5 m/s", GRUEN, 25),
           tx([3.5, 2.0], "1 s", anker="middle", groesse=25), tx([4.1, 3.2], "1 m/s", ORANGE, 25),
           tx([2.65, 11.6], "B (1 kg): steiler", GRUEN, 27), tx([3.15, 5.4], "A (5 kg)", ORANGE, 27),
           tx([0.25, 11.2], "Beispiel: F = 5 N", TINTE, 25)])))

# F4: Overlay auf die klick-Gerade v = 2 t (Fenster wie das graf der Szene)
assert 6 / 3 * 4 == 8
setze(d, 'Frage 4', A(graf([-0.7, 6.6], [-3, 27], [], [], 't [s]', 'v [m/s]', ein=3.3, achsen=False,
    strecken=[li([4, 0], [4, 8], gestr=True), li([0, 8], [4, 8], gestr=True),
              li([4, 8], [5, 8], gestr=True), li([5, 8], [5, 10], gestr=True)],
    punkte=[{"x": 4, "y": 8, "farbe": GRUEN, "beschriftung": "(4 s; 8 m/s)", "beschriftung_bei": [3.8, 10.2], "anker": "end"}],
    texte=[tx([4.5, 6.2], "1 s", anker="middle", groesse=25), tx([5.12, 8.4], "2 m/s", groesse=25),
           tx([0.3, 23.5], "a = 6 N : 3 kg = 2 m/s²", groesse=27)])))

# F5: leer 2 m/s², beladen 2/1.5 = 1.33 m/s²; nach 3 s: 6 m/s und 4 m/s
a2 = 2 / 1.5
assert abs(a2 * 3 - 4) < 1e-9
setze(d, 'Frage 5', A(graf([-0.5, 6.7], [-1.5, 14.5], [1, 2, 3, 4, 5, 6], [2, 4, 6, 8, 10, 12, 14], 't [s]', 'v [m/s]',
    strecken=[{"von": [0, 0], "bis": [6.2, 12.4], "farbe": GRUEN, "dicke": 5},
              {"von": [0, 0], "bis": [6.4, r2(6.4 * a2)], "farbe": ORANGE, "dicke": 5},
              li([3, 0], [3, 6], gestr=True)],
    punkte=[{"x": 3, "y": 6, "farbe": GRUEN, "beschriftung": "(3 s; 6 m/s)", "beschriftung_bei": [2.85, 7.0], "anker": "end"},
            {"x": 3, "y": 4, "farbe": ORANGE, "beschriftung": "(3 s; 4 m/s)", "beschriftung_bei": [3.2, 3.0], "anker": "start"}],
    texte=[tx([5.55, 11.9], "leer: 2 m/s²", GRUEN, 27, "end"), tx([6.6, 4.2], "beladen: 1.33 m/s²", ORANGE, 27, "end"),
           tx([0.3, 13.0], "anderthalbfache Masse: flacher", TINTE, 25)])))
speichere('p4-2-lp-kontrolle-grundgesetz', d)

# ======================================================== Gesamtkraft (Kapitel 2)
d = lade('p4-2-lp-kontrolle-gesamtkraft'); ohne_alte_antworten(d)

# F1: Zug 50 N, Reibung 20 N -> 30 N; Massstab 0.07 Einheiten je N
s_ = 0.07
z = Z()
z.st.append(li([0.3, 5.4], [9.7, 5.4], dicke=3))
z.kasten(3.0, 5.6, 5.4, 7.0, text="Schlitten")
z.st.append(li([2.8, 5.5], [5.6, 5.5], dicke=4))
z.st.append(pf([5.4, 6.3], [5.4 + 50 * s_, 6.3], text="Zug 50 N", bei=[5.4 + 25 * s_, 6.65], anker="middle"))
z.st.append(pf([3.0, 6.3], [3.0 - 20 * s_, 6.3], ROT, text="Reibung 20 N", bei=[2.25, 7.4], anker="middle"))
# Summe Kopf an Fuss
z.st.append(pf([1.0, 3.6], [1.0 + 50 * s_, 3.6], text="50 N", bei=[1.0 + 25 * s_, 3.9], anker="middle"))
z.st.append(pf([1.0 + 50 * s_, 3.0], [1.0 + 30 * s_, 3.0], ROT, text="20 N", bei=[1.0 + 50 * s_ + 0.2, 2.85]))
z.st.append(li([1.0 + 50 * s_, 3.6], [1.0 + 50 * s_, 3.0], gestr=True))
z.st.append(pf([1.0, 2.0], [1.0 + 30 * s_, 2.0], dicke=7, text="Gesamtkraft 30 N", bei=[1.0, 1.25]))
z.st.append(li([1.0 + 30 * s_, 3.0], [1.0 + 30 * s_, 2.0], gestr=True))
setze(d, 'Frage 1', A(z.bild()))

# F2: Auto mit konstant 80 km/h: Antrieb = Widerstand
z = Z()
z.st.append(li([0.3, 4.3], [9.7, 4.3], dicke=3))
z.kasten(3.0, 4.8, 7.0, 6.2, text="Auto")
z.kv += kreis(3.8, 4.65, 0.35) + kreis(6.2, 4.65, 0.35)
z.st.append(pf([7.0, 5.5], [9.6, 5.5], text="Antrieb", bei=[8.3, 5.85], anker="middle"))
z.st.append(pf([3.0, 5.5], [0.4, 5.5], ROT, text="Widerstand", bei=[1.7, 5.85], anker="middle"))
z.st.append(pf([3.0, 7.3], [7.0, 7.3], GRUEN, text="v = 80 km/h, konstant", bei=[5.0, 7.7], anker="middle"))
z.tx += [tx([5, 3.0], "gleich lang, entgegengesetzt:", anker="middle"),
         tx([5, 2.2], "Gesamtkraft 0, a = 0", groesse=30, anker="middle")]
setze(d, 'Frage 2', A(z.bild()))

# F3: Bus bremst, Fahrgast behält sein Tempo
z = Z()
z.tx.append(tx([0.4, 9.0], "vor dem Bremsen", groesse=27))
z.st.append(pf([2.6, 7.9], [7.6, 7.9], GRUEN)); z.tx.append(tx([2.4, 7.75], "Bus", GRUEN, 26, "end"))
z.st.append(pf([2.6, 6.9], [7.6, 6.9], GRUEN)); z.tx.append(tx([2.4, 6.75], "Fahrgast", GRUEN, 26, "end"))
z.tx.append(tx([7.8, 7.3], "gleich", TINTE, 25))
z.tx.append(tx([0.4, 5.0], "beim Bremsen", groesse=27))
z.st.append(pf([2.6, 3.9], [5.0, 3.9], GRUEN)); z.tx.append(tx([2.4, 3.75], "Bus", GRUEN, 26, "end"))
z.st.append(li([5.0, 3.9], [7.6, 3.9], gestr=True))
z.st.append(pf([2.6, 2.9], [7.6, 2.9], GRUEN)); z.tx.append(tx([2.4, 2.75], "Fahrgast", GRUEN, 26, "end"))
z.tx += [tx([0.4, 1.4], "Der Fahrgast ist schneller als der Bus:", groesse=25),
         tx([0.4, 0.6], "gegenüber dem Bus nach vorn", groesse=25)]
setze(d, 'Frage 3', A(z.bild()))

# F4: Overlay auf die klick-Gerade v = 3 + 0.5 t; a = 40 N : 80 kg = 0.5 m/s²
assert (70 - 30) / 80 == 0.5 and 3 + 0.5 * 4 == 5
setze(d, 'Frage 4', A(graf([-0.9, 8.8], [-1.3, 12.5], [], [], 't [s]', 'v [m/s]', ein=3.3, achsen=False,
    strecken=[li([4, 0], [4, 3], gestr=True), li([0, 3], [4, 3], gestr=True), li([4, 3], [4, 5], gestr=True),
              li([0, 5], [4, 5], gestr=True)],
    punkte=[{"x": 0, "y": 3, "farbe": GRUEN},
            {"x": 4, "y": 5, "farbe": GRUEN, "beschriftung": "(4 s; 5 m/s)", "beschriftung_bei": [3.8, 6.3], "anker": "end"}],
    texte=[tx([2, 2.1], "Δt = 4 s", anker="middle", groesse=25), tx([4.15, 3.75], "Δv = 2 m/s", groesse=25),
           tx([0.3, 11.0], "a = 40 N : 80 kg = 0.5 m/s²", groesse=27)])))

# F5: Velo rollt aus: nur der Widerstand, nach hinten
z = Z()
z.st.append(li([0.3, 3.6], [9.7, 3.6], dicke=3))
z.kv += kreis(3.6, 4.5, 0.9, dicke=4) + kreis(6.6, 4.5, 0.9, dicke=4)
z.st += [li([3.6, 4.5], [5.1, 4.5], dicke=4), li([5.1, 4.5], [6.0, 5.9], dicke=4), li([3.6, 4.5], [4.6, 5.9], dicke=4),
         li([4.6, 5.9], [6.0, 5.9], dicke=4), li([6.0, 5.9], [6.6, 4.5], dicke=4), li([4.4, 6.3], [4.9, 6.3], dicke=5),
         li([4.6, 5.9], [4.6, 6.3], dicke=4)]
z.st.append(pf([3.6, 7.4], [7.6, 7.4], GRUEN, text="v (Fahrtrichtung)", bei=[5.6, 7.8], anker="middle"))
z.st.append(pf([2.6, 5.2], [0.5, 5.2], ROT, text="Widerstand", bei=[1.55, 5.55], anker="middle"))
z.tx += [tx([5, 2.5], "kein Antrieb:", anker="middle"),
         tx([5, 1.6], "Gesamtkraft = Widerstand, nach hinten", ROT, 26, "middle")]
setze(d, 'Frage 5', A(z.bild()))
speichere('p4-2-lp-kontrolle-gesamtkraft', d)

# ======================================================== Aufzug (Kapitel 3)
d = lade('p4-2-lp-kontrolle-aufzug'); ohne_alte_antworten(d)


def kabine(z, v=None, a=None, seil=True):
    """Kabine links (0.5..3.5), Person auf der Waage; v (grün) und a (gestrichelt) rechts daneben."""
    z.kasten(0.5, 2.6, 3.4, 7.4, deckung=0.05)
    if seil:
        z.st.append(li([1.95, 7.4], [1.95, 9.8], dicke=3))
    else:
        z.st += [li([1.95, 7.4], [1.95, 8.3], dicke=3), li([1.95, 9.0], [1.95, 9.8], dicke=3)]
        z.tx.append(tx([2.15, 8.55], "gerissen", groesse=22))
    z.kasten(1.3, 2.6, 2.6, 2.95, deckung=0.35, dicke=2)
    z.kasten(1.6, 2.95, 2.3, 5.0, text=None)
    z.kv += kreis(1.95, 5.4, 0.35, dicke=3)
    if v:
        z.st.append(pf([4.0, 5.0 - 1.2 * v], [4.0, 5.0 + 1.2 * v], GRUEN))
        z.tx.append(tx([3.82, 4.85], "v", GRUEN, 27, "end"))
    if a:
        z.st.append(pf([4.7, 5.0 - 1.2 * a], [4.7, 5.0 + 1.2 * a], gestr=True))
        z.tx.append(tx([4.88, 4.85], "a", TINTE, 27, "start"))
    z.tx.append(tx([1.95, 1.9], "Kabine", groesse=24, anker="middle"))


def person_kraefte(z, FN, FG, s, cy=5.0, fn_text=None, fg_text=None):
    """Kräfte auf die Person, als Punkt rechts (x 7.2)."""
    z.pt.append({"x": 7.2, "y": cy, "farbe": TINTE})
    if FN > 0:
        z.st.append(pf([7.0, cy], [7.0, r2(cy + FN * s)]))
        z.tx += [tx([6.75, cy + FN * s - 0.35], "Normalkraft", anker="end", groesse=25)]
        if fn_text:
            z.tx.append(tx([6.75, cy + FN * s - 1.05], fn_text, anker="end", groesse=25))
    z.st.append(pf([7.4, cy], [7.4, r2(cy - FG * s)], BERN))
    z.tx += [tx([7.65, cy - FG * s + (0.85 if fg_text else 0.15)], "Gewichtskraft", BERN, 25)]
    if fg_text:
        z.tx.append(tx([7.65, cy - FG * s + 0.15], fg_text, BERN, 25))
    z.tx.append(tx([7.2, 9.4], "Kräfte auf die Person", groesse=24, anker="middle"))


# F1: 3 kg -> 29.4 N
FG1 = 3 * G_
assert abs(FG1 - 29.43) < 1e-9
z = Z()
z.kasten(3.8, 5.6, 6.2, 7.6)
z.tx.append(tx([5.0, 6.85], "3 kg", anker="middle", groesse=26))
z.st.append(pf([5.0, 6.3], [5.0, 2.3], BERN, dicke=7))           # 4 Einheiten
z.tx += [tx([5.3, 3.9], "Gewichtskraft", BERN, 27), tx([5.3, 3.1], "29.4 N", BERN, 27)]
z.st.append(li([0.6, 1.6], [9.4, 1.6], dicke=4))
z.tx += [tx([5, 0.8], "Erde: g = 9.81 m/s²", anker="middle", groesse=25),
         tx([5, 8.6], "Masse in kg, Gewichtskraft in N", groesse=24, anker="middle")]
setze(d, 'Frage 1', A(z.bild()))

# F2: Anfahren nach oben (keine Zahlen in der Frage: Längen nur im Verhältnis)
z = Z(); kabine(z, v=0.6, a=1)
person_kraefte(z, 3.2, 2.5, 1.0)
z.tx.append(tx([5.0, 0.7], "Normalkraft > Gewichtskraft: Waage zeigt mehr", groesse=24, anker="middle"))
setze(d, 'Frage 2', A(z.bild()))

# F3: konstant nach unten
z = Z(); kabine(z, v=-1)
person_kraefte(z, 2.8, 2.8, 1.0)
z.tx += [tx([4.5, 5.9], "a = 0", TINTE, 25, "start")]
z.tx.append(tx([5.0, 0.7], "Normalkraft = Gewichtskraft: wie in Ruhe", groesse=24, anker="middle"))
setze(d, 'Frage 3', A(z.bild()))

# F4: 70 kg, nach unten, bremst mit 1.5 m/s² (a nach oben): F_N = 70 kg · 11.31 m/s² = 791.7 N
FG4, FN4 = 70 * G_, 70 * (G_ + 1.5)
assert round(FN4) == 792 and round(FG4, 1) == 686.7 and abs(FN4 - FG4 - 105) < 1e-9
z = Z(); kabine(z, v=-1, a=0.6)
person_kraefte(z, FN4, FG4, 0.0045, cy=4.9, fn_text="792 N", fg_text="687 N")
z.tx.append(tx([5.0, 0.7], "Gesamtkraft: 792 N − 687 N = 105 N nach oben", groesse=23, anker="middle"))
setze(d, 'Frage 4', A(z.bild()))

# F5: freier Fall: nur die Gewichtskraft, a = g
z = Z(); kabine(z, v=-1, a=-1, seil=False)
person_kraefte(z, 0, 2.8, 1.0)
z.tx += [tx([5.2, 6.6], "Normalkraft 0", groesse=25)]
z.tx.append(tx([5.0, 0.7], "a = g nach unten: die Waage zeigt null", groesse=24, anker="middle"))
setze(d, 'Frage 5', A(z.bild()))
for s_ in d['szenen']:
    for e in s_['elemente']:
        if e['typ'] == 'formel' and s_['name'] in ('Frage 4', 'Frage 5'):
            e['groesse'] = {'Frage 4': 38, 'Frage 5': 44}[s_['name']]
speichere('p4-2-lp-kontrolle-aufzug', d)

# ======================================================== Faden (Kapitel 4)
d = lade('p4-2-lp-kontrolle-faden'); ohne_alte_antworten(d)
m1, m2 = 3.0, 0.5
a1 = m2 * G_ / (m1 + m2)
FS1 = m1 * a1
assert round(a1, 2) == 1.40 and round(FS1, 1) == 4.2 and round(m2 * G_, 1) == 4.9


def tisch(z, wagen_text, koerper_text, haengt_y=3.0):
    z.kasten(0.3, 5.4, 5.6, 6.0, deckung=0.18, dicke=3)                  # Tischplatte
    z.st += [li([0.8, 5.4], [0.8, 1.0], dicke=4), li([5.1, 5.4], [5.1, 1.0], dicke=4)]
    z.kasten(1.4, 6.45, 4.0, 7.65, text=wagen_text)
    z.kv += kreis(1.9, 6.22, 0.22, dicke=3) + kreis(3.5, 6.22, 0.22, dicke=3)
    z.st.append(li([5.6, 5.95], [6.15, 5.45], dicke=3))                  # Halter der Rolle
    z.kv += kreis(6.15, 6.6, 0.5, dicke=4)
    z.st.append(li([4.0, 7.1], [6.15, 7.1], dicke=3))                    # Faden waagrecht
    z.st.append(li([6.65, 6.6], [6.65, haengt_y + 1.0], dicke=3))        # Faden senkrecht
    z.kasten(6.15, haengt_y, 7.15, haengt_y + 1.0, text=None)
    z.tx.append(tx([6.65, haengt_y + 0.32], koerper_text, groesse=22, anker="middle"))


# F1: a = 0.5 kg · 9.81 m/s² : 3.5 kg = 1.40 m/s²
z = Z(); tisch(z, "3 kg", "0.5 kg", haengt_y=3.4)
z.st.append(pf([6.65, 3.4], [6.65, 1.4], BERN))
z.tx += [tx([6.9, 1.9], "4.9 N", BERN, 27)]
z.st.append(pf([1.4, 8.6], [4.0, 8.6], gestr=True))
z.st.append(pf([8.3, 5.4], [8.3, 2.8], gestr=True))
z.tx += [tx([2.7, 8.95], "a = 1.40 m/s²", anker="middle", groesse=26), tx([8.45, 6.0], "a", groesse=27, anker="middle"),
         tx([0.3, 0.3], "4.9 N beschleunigen 3 kg + 0.5 kg", groesse=25)]
setze(d, 'Frage 1', A(z.bild()))

# F2: am hängenden Körper (Zahlen aus Frage 1): Fadenkraft 4.2 N < Gewichtskraft 4.9 N
z = Z()
z.st.append(li([5.0, 6.0], [5.0, 9.6], dicke=3))
z.kasten(4.2, 4.0, 5.8, 6.0, text=None)
s2 = 0.75
z.st.append(pf([4.75, 5.0], [4.75, r2(5.0 + FS1 * s2)]))
z.st.append(pf([5.25, 5.0], [5.25, r2(5.0 - m2 * G_ * s2)], BERN))
z.tx += [tx([4.5, 7.6], "Fadenkraft", anker="end", groesse=26), tx([4.5, 6.85], "4.2 N", anker="end", groesse=26),
         tx([5.5, 2.4], "Gewichtskraft", BERN, 26), tx([5.5, 1.65], "4.9 N", BERN, 26)]
z.st.append(pf([8.6, 6.2], [8.6, 3.8], gestr=True))
z.tx += [tx([8.8, 4.9], "a", groesse=27)]
z.tx += [tx([0.3, 9.3], "Beispiel aus Frage 1", groesse=24),
         tx([0.3, 0.5], "Gesamtkraft 0.7 N nach unten", groesse=25)]
setze(d, 'Frage 2', A(z.bild()))

# F3: Auto 1000 kg + Anhänger 500 kg, 3000 N -> a = 2 m/s², Kupplung 1000 N; 0.001 Einheiten je N
a3 = 3000 / 1500
assert a3 == 2 and 500 * a3 == 1000
z = Z()
z.tx.append(tx([0.3, 9.2], "ganzes System: 1500 kg", groesse=26))
z.st.append(li([0.3, 5.9], [9.7, 5.9], dicke=3))
z.kasten(0.6, 6.2, 2.6, 7.4, text="500 kg", tgroesse=24)
z.st.append(li([2.6, 6.5], [3.1, 6.5], dicke=4))
z.kasten(3.1, 6.2, 5.9, 7.8, text="1000 kg", tgroesse=24)
z.kv += kreis(1.1, 6.05, 0.15, dicke=3) + kreis(2.1, 6.05, 0.15, dicke=3) + kreis(3.6, 6.05, 0.15, dicke=3) + kreis(5.4, 6.05, 0.15, dicke=3)
z.st.append(pf([5.9, 7.0], [8.9, 7.0], text="Antrieb 3000 N", bei=[7.4, 7.35], anker="middle", groesse=25))
z.tx.append(tx([0.3, 8.35], "a = 3000 N : 1500 kg = 2 m/s²", groesse=25))
z.tx.append(tx([0.3, 4.4], "Anhänger allein: 500 kg", groesse=26))
z.st.append(li([0.3, 1.9], [9.7, 1.9], dicke=3))
z.kasten(0.6, 2.2, 2.6, 3.4, text="500 kg", tgroesse=24)
z.kv += kreis(1.1, 2.05, 0.15, dicke=3) + kreis(2.1, 2.05, 0.15, dicke=3)
z.st.append(pf([2.6, 2.8], [3.6, 2.8], text="Kupplung 1000 N", bei=[3.8, 2.65], groesse=25))
z.tx.append(tx([0.3, 0.8], "500 kg · 2 m/s² = 1000 N", groesse=25))
setze(d, 'Frage 3', A(z.bild()))

# F4: Wagen festgehalten, 1 kg hängt: Fadenkraft = Gewichtskraft = 9.81 N
z = Z(); tisch(z, "Wagen", "1 kg", haengt_y=3.4)
s4 = 0.2
z.st.append(pf([6.65, 4.4], [6.65, r2(4.4 + 9.81 * s4)]))
z.st.append(pf([6.65, 3.4], [6.65, r2(3.4 - 9.81 * s4)], BERN))
z.tx += [tx([7.35, 5.35], "Fadenkraft", groesse=25), tx([7.35, 4.65], "9.81 N", groesse=25),
         tx([7.35, 2.0], "Gewichtskraft", BERN, 25), tx([7.35, 1.3], "9.81 N", BERN, 25)]
z.st.append(pf([1.4, 7.05], [0.3, 7.05], text=None))
z.tx += [tx([0.3, 8.4], "festgehalten: a = 0", groesse=26)]
setze(d, 'Frage 4', A(z.bild()))

# F5: Wagen 3 kg; 0.5 kg -> 1.40 m/s², 1 kg -> 2.45 m/s², doppelt wäre 2.80 m/s²
aa = 0.5 * G_ / 3.5; ab = 1.0 * G_ / 4.0
assert round(aa, 2) == 1.40 and round(ab, 2) == 2.45 and round(2 * aa, 2) == 2.80
b = 0.09
setze(d, 'Frage 5', A(graf([-0.17, 1.45], [-0.4, 3.6], [0.5, 1], [0.5, 1, 1.5, 2, 2.5, 3], 'm₂ [kg]', 'a [m/s²]',
    flaechen=[{"punkte": [[0.5 - b, 0], [0.5 + b, 0], [0.5 + b, r2(aa)], [0.5 - b, r2(aa)]], "farbe": TINTE, "deckung": 0.30},
              {"punkte": [[1 - b, 0], [1 + b, 0], [1 + b, r2(ab)], [1 - b, r2(ab)]], "farbe": TINTE, "deckung": 0.30}],
    strecken=[li([1 - b, r2(ab)], [1 - b, r2(2 * aa)], gestr=True), li([1 + b, r2(ab)], [1 + b, r2(2 * aa)], gestr=True),
              li([1 - b, r2(2 * aa)], [1 + b, r2(2 * aa)], gestr=True)],
    texte=[tx([0.5, aa + 0.12], "1.40 m/s²", groesse=25, anker="middle"),
           tx([1.0 + b + 0.02, ab - 0.12], "2.45 m/s²", groesse=25, anker="start"),
           tx([1.0, 2 * aa + 0.1], "doppelt wäre 2.80", groesse=25, anker="middle"),
           tx([0.12, 3.2], "Wagen 3 kg", groesse=25)])))
for s_ in d['szenen']:
    if s_['name'] == 'Frage 1':
        for e in s_['elemente']:
            if e['typ'] == 'formel': e['groesse'] = 34
speichere('p4-2-lp-kontrolle-faden', d)

# ======================================================== Kurve (Kapitel 5)
d = lade('p4-2-lp-kontrolle-kurve'); ohne_alte_antworten(d)

# F1: 0.5 kg, 4 m/s, r = 4 m -> 2 N; Bahn 1:1 in m, v-Pfeil 0.75 m je m/s, Kraft 1 m je N
assert 0.5 * 4 ** 2 / 4 == 2
z = Z()
z.kv += kreis(0, 0, 4, dicke=4)
z.st.append(li([0, 0], [r2(4 * math.cos(math.radians(-35))), r2(4 * math.sin(math.radians(-35)))], gestr=True))
z.tx.append(tx([1.9, -0.75], "r = 4 m", groesse=26))
z.pt += [{"x": 0, "y": 0, "farbe": TINTE}, {"x": 0, "y": 4, "farbe": TINTE}]
z.st.append(pf([0, 4], [-3, 4], GRUEN, text="v = 4 m/s", bei=[-1.5, 4.4], anker="middle"))
z.st.append(pf([0, 4], [0, 2], ROT))
z.tx += [tx([0.3, 2.8], "2 N", ROT, 26), tx([0, 1.25], "Zentripetalkraft", ROT, 26, "middle"), tx([0.35, 4.4], "0.5 kg", groesse=25),
         tx([0, -0.9], "Mitte", groesse=24, anker="middle")]
setze(d, 'Frage 1', A(z.bild(fenster=(-5.5, 5.5, -5.5, 5.5))))

# F2: F = m v² / r, Beispiel aus Frage 1 (0.5 kg, r = 4 m): F = v²/8; 2 m/s -> 0.5 N, 6 m/s -> 4.5 N
assert 0.5 * 2 ** 2 / 4 == 0.5 and 0.5 * 6 ** 2 / 4 == 4.5
setze(d, 'Frage 2', A(graf([-0.7, 7.6], [-0.6, 6.2], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6], 'v [m/s]', 'F [N]',
    kurven=[{"formel": "x*x/8", "von": 0, "bis": 6.85, "farbe": ROT, "dicke": 5}],
    strecken=[li([2, 0], [2, 0.5], gestr=True), li([0, 0.5], [2, 0.5], gestr=True),
              li([6, 0], [6, 4.5], gestr=True), li([0, 4.5], [6, 4.5], gestr=True)],
    punkte=[{"x": 2, "y": 0.5, "farbe": ROT, "beschriftung": "(2 m/s; 0.5 N)", "beschriftung_bei": [2.25, 0.12], "anker": "start"},
            {"x": 6, "y": 4.5, "farbe": ROT, "beschriftung": "(6 m/s; 4.5 N)", "beschriftung_bei": [5.8, 5.0], "anker": "end"}],
    texte=[tx([0.6, 5.2], "3 · v  →  9 · F", groesse=30),
           tx([0.3, 4.0], "0.5 kg auf r = 4 m", groesse=24)])))

# F3: Mond auf der Bahn um die Erde (nicht massstäblich)
w = math.radians(40); mx, my = 4 * math.cos(w), 4 * math.sin(w)
z = Z()
z.kv += kreis(0, 0, 4, dicke=3, gestrichelt=True) + kreis(0, 0, 0.7, farbe=GRUEN, dicke=4)
z.pt.append({"x": r2(mx), "y": r2(my), "farbe": TINTE})
z.st.append(pf([r2(mx), r2(my)], [r2(mx * 0.45), r2(my * 0.45)], ROT))
z.st.append(pf([r2(mx), r2(my)], [r2(mx - 2.4 * math.sin(w)), r2(my + 2.4 * math.cos(w))], GRUEN, text="v", bei=[r2(mx - 2.4 * math.sin(w) - 0.5), r2(my + 2.4 * math.cos(w) - 0.1)], anker="end"))
z.tx += [tx([0, -0.15], "Erde", GRUEN, 25, "middle"), tx([mx + 0.35, my - 0.15], "Mond", TINTE, 26),
         tx([mx * 0.7 + 0.25, my * 0.7 - 0.55], "Gravitation", ROT, 26),
         tx([0, -4.75], "Bahn des Mondes (nicht massstäblich)", groesse=23, anker="middle")]
setze(d, 'Frage 3', A(z.bild(fenster=(-5.5, 5.5, -5.5, 5.5))))

# F4: Schnur reisst oben: geradeaus, tangential
z = Z()
z.kv += kreis(0, 0, 3.5, dicke=3, gestrichelt=True)
z.st.append(li([0, 0], [0, 3.5], gestr=True))
z.pt += [{"x": 0, "y": 0, "farbe": TINTE}, {"x": 0, "y": 3.5, "farbe": TINTE}]
z.st.append(pf([0, 3.5], [-4.9, 3.5], GRUEN))
z.pt += [{"x": -1.6, "y": 3.5, "farbe": GRUEN}, {"x": -3.2, "y": 3.5, "farbe": GRUEN}]
z.tx += [tx([-2.4, 4.05], "geradeaus, tangential", GRUEN, 26, "middle"),
         tx([0.25, 1.6], "Schnur reisst", groesse=24),
         tx([0, -4.6], "keine Kraft mehr zur Mitte", ROT, 26, "middle")]
setze(d, 'Frage 4', A(z.bild(fenster=(-5.5, 5.5, -5.5, 5.5))))

# F5: Auto in der Kurve, Draufsicht: Haftreibung zur Kurvenmitte
z = Z()
z.kv += kreis(0, 0, 4.6, dicke=4, nur='oben') + kreis(0, 0, 3.0, dicke=4, nur='oben') + kreis(0, 0, 3.8, dicke=2, gestrichelt=True, nur='oben')
z.kasten(-0.35, 3.45, 0.35, 4.15, deckung=0.4, dicke=2)
z.st.append(pf([0, 3.8], [-3.2, 3.8], GRUEN, text="v", bei=[-2.9, 4.15], anker="middle"))
z.st.append(pf([0, 3.8], [0, 1.3], ROT))
z.pt.append({"x": 0, "y": 0, "farbe": TINTE})
z.tx += [tx([0.3, 1.7], "Haftreibung", ROT, 25),
         tx([0, -0.75], "Kurvenmitte", groesse=24, anker="middle"),
         tx([0, 5.1], "Draufsicht", groesse=24, anker="middle")]
setze(d, 'Frage 5', A(z.bild(fenster=(-5.2, 5.2, -2.0, 8.4))))
speichere('p4-2-lp-kontrolle-kurve', d)
print('ok')
