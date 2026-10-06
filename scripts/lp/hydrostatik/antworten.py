"""Antwortbilder der Hydrostatik-Kontrollclips (06.10.2026).

Jede Antwortszene «Frage 1» … «Frage 5» bekommt rechts ein Bild (x 1010, y 175,
760 x 760), das die Antwort zeigt. Wiederholbar: alte Bilder (Kennung "antwort")
werden zuerst entfernt. Alle Zahlen hier gerechnet.

Farben (Theme begreifbar-schlicht hat kein Blau und kein Violett):
  1 Bernstein  Gewichtskraft (wie Leitprogramm und Statik)
  2 Orange     Tiefen, Höhen, verdrängtes Volumen (Leitprogramm: Violett)
  3 Grün       Auftrieb (wie Leitprogramm)
  4 Rot        Druck in der Flüssigkeit, Kolbenkräfte, Kraft der Federwaage
               (Leitprogramm: Blau — die blaue Rolle geht geschlossen an Rot)
  5 Tinte      Luftdruck (Leitprogramm: Grau), Gefässe, Flüssigkeiten (Fläche hell)
Skizzen ohne Achsen haben ein quadratisches Fenster (1:1).
"""
import os
import json, math

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
G = 9.81
GEW, ORA, AUF, DRU, TIN = 1, 2, 3, 4, 5


def fmt(v):
    return ('%g' % v).replace('-', '−')


def tz(v):
    """Tausender mit schmalem Abstand: 25000 -> «25 000»."""
    s = '%d' % v
    if len(s) > 4:
        s = s[:-3] + ' ' + s[-3:]
    return s


def graf(xb, yb, xt, yt, xname, yname, ein=1.0, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": True, "xbereich": xb, "ybereich": yb,
         "xteilung": [v if isinstance(v, list) else [v, fmt(v)] for v in xt],
         "yteilung": [v if isinstance(v, list) else [v, fmt(v)] for v in yt],
         "xname": xname, "yname": yname, "antwort": True}
    g.update(kw)
    return g


def skizze(x0, y0, span, **kw):
    """Bild ohne Achsen, quadratisches Fenster (1:1)."""
    return graf([x0, x0 + span], [y0, y0 + span], [], [], '', '', achsen=False, pfeile=False, **kw)


def r4(v):
    return round(v, 4)


def S(von, bis, farbe=TIN, **kw):
    d = {"von": [r4(von[0]), r4(von[1])], "bis": [r4(bis[0]), r4(bis[1])], "farbe": farbe}
    d.update(kw)
    return d


def P(von, bis, farbe, **kw):
    return S(von, bis, farbe, pfeil=True, **kw)


def T(x, y, text, farbe=TIN, groesse=27, anker="middle", **kw):
    d = {"bei": [r4(x), r4(y)], "text": text, "farbe": farbe, "groesse": groesse, "anker": anker}
    d.update(kw)
    return d


def F(pts, farbe=TIN, deckung=0.12, **kw):
    d = {"punkte": [[r4(x), r4(y)] for x, y in pts], "farbe": farbe, "deckung": deckung}
    d.update(kw)
    return d


def rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def umriss(x0, y0, x1, y1, farbe=TIN, dicke=3, **kw):
    p = rechteck(x0, y0, x1, y1)
    return [S(p[i], p[(i + 1) % 4], farbe, dicke=dicke, **kw) for i in range(4)]


def becher(x0, x1, yb, yo, dicke=5):
    return [S((x0, yo), (x0, yb), dicke=dicke), S((x0, yb), (x1, yb), dicke=dicke), S((x1, yb), (x1, yo), dicke=dicke)]


def kreispunkte(cx, cy, r, n=72):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def kreislinie(cx, cy, r, farbe=TIN, dicke=4, gestrichelt=False):
    p = kreispunkte(cx, cy, r, 96)
    return [S(p[k], p[(k + 1) % 96], farbe, dicke=dicke, **({"gestrichelt": True} if gestrichelt else {}))
            for k in range(96) if not gestrichelt or k % 2 == 0]


def setze(d, szene, el):
    for s in d['szenen']:
        if s['name'] == szene:
            s['elemente'].append(el)
            return
    raise KeyError(szene)


def lade(n):
    d = json.load(open(R + n + '.json'))
    for s in d['szenen']:
        s['elemente'] = [e for e in s['elemente'] if not e.get('antwort')]
    return d


GROESSE = {('p4-5-lp-kontrolle-schweredruck', 'Frage 1'): 36, ('p4-5-lp-kontrolle-schweredruck', 'Frage 3'): 36,
            ('p4-5-lp-kontrolle-schwimmen', 'Frage 3'): 40}


def speichere(n, d):
    # Neben dem Antwortbild hat die Formel links nur 820 px: wo sie hineinragt, kleiner setzen
    for s_ in d['szenen']:
        g_ = GROESSE.get((n, s_['name']))
        if g_:
            for e in s_['elemente']:
                if e['typ'] == 'formel':
                    e['groesse'] = g_
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


# ======================================================== Druck (Kapitel 1)
n = 'p4-5-lp-kontrolle-druck'; d = lade(n)
# F1: p über A bei F = 300 N, abgelesen bei 0.012 m²
p1 = 300 / 0.012
assert abs(p1 - 25000) < 1e-6
setze(d, 'Frage 1', graf([-0.0095, 0.047], [-9000, 89000], [0.01, 0.02, 0.03, 0.04],
    [[v, tz(v)] for v in (20000, 40000, 60000, 80000)], 'A [m²]', 'p [Pa]',
    kurven=[{"formel": "300/x", "von": 300 / 85000, "bis": 0.046, "farbe": DRU, "dicke": 5}],
    strecken=[S((0.012, 0), (0.012, p1), gestrichelt=True), S((0, p1), (0.012, p1), gestrichelt=True)],
    punkte=[{"x": 0.012, "y": p1, "farbe": DRU, "beschriftung": "(0.012 m²; 25 000 Pa)", "beschriftung_bei": [0.0145, 30500], "anker": "start"}],
    texte=[T(0.0285, 52000, "Kraft F = 300 N", GEW, 28),
           T(0.0285, 45000, "kleinere Fläche: grösserer Druck", TIN, 24)]))
# F2: Doppelskala bar / hPa
st = [S((0, 0), (1, 0), dicke=5)]
for v in (0, 0.25, 0.5, 0.75, 1):
    st.append(S((v, -0.06), (v, 0.06), dicke=4))
st.append(S((0, 0.24), (0.5, 0.24), DRU, dicke=5))
st += [S((0, 0.19), (0, 0.29), DRU, dicke=4), S((0.5, 0.19), (0.5, 0.29), DRU, dicke=4)]
setze(d, 'Frage 2', skizze(-0.2, -0.7, 1.4, strecken=st,
    punkte=[{"x": 0.5, "y": 0, "farbe": DRU}],
    texte=[T(0, 0.1, "0", groesse=30), T(0.5, 0.1, "0.5 bar", DRU, 30), T(1, 0.1, "1 bar", groesse=30),
           T(0, -0.17, "0", groesse=30), T(0.5, -0.17, "500 hPa", DRU, 30), T(1, -0.17, "1000 hPa", groesse=30),
           T(0.25, 0.33, "die Hälfte", DRU, 27),
           T(0.5, 0.5, "1 bar = 1000 hPa", TIN, 32),
           T(0.5, -0.43, "halb so viel Bar: halb so viele Hektopascal", TIN, 24)]))
# F3: gleiche Kraft auf drei Flächen
st = [S((0.2, 0), (11.8, 0), dicke=4)]
# Nadel
st += [S((1.85, 2.2), (2, 0.05), dicke=3), S((2.15, 2.2), (2, 0.05), dicke=3), S((1.85, 2.2), (2.15, 2.2), dicke=3)]
# Fussball (Kreis, berührt den Boden)
st += kreislinie(6, 1.0, 1.0, dicke=3)
# Schneeschuh
st += umriss(8.3, 0, 11.7, 0.25, dicke=3)
# Kontaktflächen rot
st += [S((1.96, 0), (2.04, 0), DRU, dicke=9), S((5.7, 0), (6.3, 0), DRU, dicke=9), S((8.3, 0), (11.7, 0), DRU, dicke=9)]
# gleiche Kraft
for c, y0 in ((2, 2.3), (6, 2.1), (10, 0.35)):
    st.append(P((c, y0 + 2.4), (c, y0), GEW, dicke=5))
setze(d, 'Frage 3', skizze(0, -5.5, 12, strecken=st,
    texte=[T(2, 5.6, "gleiche Kraft", GEW, 26, anker="middle"), T(6, 5.6, "gleiche Kraft", GEW, 26), T(10, 5.6, "gleiche Kraft", GEW, 26),
           T(2, -1.0, "Nadel"), T(6, -1.0, "Fussball"), T(10, -1.0, "Schneeschuh"),
           T(2, -2.1, "Fläche winzig", groesse=24), T(6, -2.1, "Fläche klein", groesse=24), T(10, -2.1, "Fläche gross", groesse=24),
           T(2, -3.3, "grösster Druck", DRU, 27), T(6, -3.3, "kleiner", DRU, 27), T(10, -3.3, "am kleinsten", DRU, 27)]))
# F4: Kraft pro Flächenstück, 4 Stücke mit F/4 gegen 2 Stücke mit F
st = []
fl = [F(rechteck(0.8, -0.35, 4.8, 0)), F(rechteck(7.2, -0.35, 9.2, 0))]
for x0, k in ((0.8, 4), (7.2, 2)):
    st += umriss(x0, -0.35, x0 + k, 0, dicke=3)
    for i in range(1, k):
        st.append(S((x0 + i, -0.35), (x0 + i, 0), dicke=2))
L = 1.0
for i in range(4):
    st.append(P((1.3 + i, L + 0.05), (1.3 + i, 0.05), GEW, dicke=4))
for i in range(2):
    st.append(P((7.7 + i, 4 * L + 0.05), (7.7 + i, 0.05), GEW, dicke=4))
setze(d, 'Frage 4', skizze(0, -4, 12, flaechen=fl, strecken=st,
    texte=[T(2.8, -1.2, "Kraft F auf Fläche A", groesse=25), T(8.2, -1.2, "Kraft 2 · F auf A/2", groesse=25),
           T(2.8, 1.6, "je Stück F/4", GEW, 24), T(8.2, 4.6, "je Stück F", GEW, 24),
           T(2.8, -2.5, "Druck p", DRU, 30), T(8.2, -2.5, "Druck 4 · p", DRU, 30),
           T(6, 7.0, "Kraft pro Flächenstück: viermal so gross", TIN, 26)]))
# F5: 1 N auf 1 m²
st = umriss(1, -0.4, 9, 0, dicke=3)
st += [P((1.5 + i, 1.25), (1.5 + i, 0.05), GEW, dicke=4) for i in range(8)]
st += [S((1, -1.0), (9, -1.0), dicke=3), S((1, -1.2), (1, -0.8), dicke=3), S((9, -1.2), (9, -0.8), dicke=3)]
setze(d, 'Frage 5', skizze(0, -4, 10, flaechen=[F(rechteck(1, -0.4, 9, 0))], strecken=st,
    texte=[T(5, 1.8, "Kraft: zusammen 1 N", GEW, 28), T(5, -1.6, "Fläche: 1 m²", TIN, 28),
           T(5, -2.9, "Druck: 1 N/m² = 1 Pa", DRU, 32), T(5, 4.0, "Druck = Kraft durch Fläche", TIN, 28)]))
speichere(n, d)

# ======================================================== Schweredruck (Kapitel 2)
n = 'p4-5-lp-kontrolle-schweredruck'; d = lade(n)
pw = lambda h, rho=1000: rho * G * h / 1000          # kPa
assert round(pw(3), 1) == 29.4
# F1: p_S über h für Wasser
setze(d, 'Frage 1', graf([-0.6, 5.6], [-6, 56], [1, 2, 3, 4, 5], [10, 20, 30, 40, 50], 'h [m]', 'Schweredruck [kPa]',
    strecken=[S((0, 0), (5.3, pw(5.3)), DRU, dicke=5),
              S((3, 0), (3, pw(3)), gestrichelt=True), S((0, pw(3)), (3, pw(3)), gestrichelt=True)],
    punkte=[{"x": 3, "y": r4(pw(3)), "farbe": DRU, "beschriftung": "(3 m; 29.4 kPa)", "beschriftung_bei": [3.2, 25.0], "anker": "start"}],
    texte=[T(0.3, 46, "Wasser: 9.81 kPa je Meter", TIN, 26, anker="start")]))
# F2: Platte waagrecht und senkrecht in derselben Tiefe
fl = [F(rechteck(0.3, -0.6, 9.7, 8))]
st = [S((0.3, 8), (9.7, 8), dicke=3),
      S((2.5, 4), (4.5, 4), dicke=8), S((7, 3), (7, 5), dicke=8),
      P((3.5, 5.55), (3.5, 4.18), DRU, dicke=5), P((3.5, 2.45), (3.5, 3.82), DRU, dicke=5),
      P((5.45, 4), (6.82, 4), DRU, dicke=5), P((8.55, 4), (7.18, 4), DRU, dicke=5),
      S((1.0, 8), (1.0, 4), ORA, gestrichelt=True, dicke=4), S((1.0, 4), (2.4, 4), ORA, gestrichelt=True, dicke=3)]
setze(d, 'Frage 2', skizze(0, -1, 10, flaechen=fl, strecken=st,
    texte=[T(1.2, 6.0, "4 m", ORA, 27, anker="start"), T(5, 8.4, "Wasseroberfläche", TIN, 24),
           T(3.5, 1.5, "waagrecht"), T(7, 1.5, "senkrecht"),
           T(5, 0.2, "gleiche Tiefe: gleich starker Druck", DRU, 27)]))
# F3: Heizöl gegen Wasser, h = 3.5 m
po, pwa = pw(3.5, 850), pw(3.5)
assert round(po, 1) == 29.2 and round(pwa, 1) == 34.3
setze(d, 'Frage 3', graf([-0.5, 5.4], [-5, 46], [1, 2, 3, 4, 5], [10, 20, 30, 40], 'h [m]', 'Schweredruck [kPa]',
    strecken=[S((0, 0), (4.3, pw(4.3)), TIN, dicke=4, gestrichelt=True),
              S((0, 0), (4.3, pw(4.3, 850)), DRU, dicke=5),
              S((3.5, 0), (3.5, pwa), gestrichelt=True), S((0, po), (3.5, po), gestrichelt=True)],
    punkte=[{"x": 3.5, "y": r4(po), "farbe": DRU, "beschriftung": "(3.5 m; 29.2 kPa)", "beschriftung_bei": [3.65, 25.3], "anker": "start"},
            {"x": 3.5, "y": r4(pwa), "farbe": TIN, "beschriftung": "Wasser: 34.3 kPa", "beschriftung_bei": [3.3, 38.0], "anker": "end"}],
    texte=[T(4.4, 34.0, "Heizöl", DRU, 27, anker="start"), T(4.4, 43.0, "Wasser", TIN, 27, anker="start")]))
# F4: Gesamtdruck in bar über h
p0, ps40 = 1.013, pw(40) / 100
assert round(ps40, 2) == 3.92 and round(p0 + ps40, 1) == 4.9
setze(d, 'Frage 4', graf([-5, 57], [-0.6, 6.4], [10, 20, 30, 40, 50], [1, 2, 3, 4, 5, 6], 'h [m]', 'p [bar]',
    strecken=[S((0, p0), (50, p0 + pw(50) / 100), DRU, dicke=5),
              S((0, p0), (40, p0), TIN, gestrichelt=True),
              S((40, 0), (40, p0), TIN, dicke=8), S((40, p0), (40, p0 + ps40), DRU, dicke=8)],
    punkte=[{"x": 40, "y": r4(p0 + ps40), "farbe": DRU, "beschriftung": "(40 m; 4.9 bar)", "beschriftung_bei": [38.5, 5.3], "anker": "end"}],
    texte=[T(41.5, 3.15, "Schweredruck", DRU, 26, anker="start"), T(41.5, 2.75, "3.92 bar", DRU, 26, anker="start"),
           T(38.8, 0.35, "Luftdruck 1.013 bar", TIN, 26, anker="end")]))
# F5: rückwärts ablesen, Meerwasser
hm = 120000 / (1025 * G)
assert round(hm, 1) == 11.9
setze(d, 'Frage 5', graf([-1.6, 15.6], [-15, 165], [2, 4, 6, 8, 10, 12, 14], [20, 40, 60, 80, 100, 120, 140, 160], 'h [m]', 'Schweredruck [kPa]',
    strecken=[S((0, 0), (15, pw(15, 1025)), DRU, dicke=5),
              P((0, 120), (hm - 0.15, 120), TIN, gestrichelt=True, dicke=3),
              P((hm, 120), (hm, 1.5), TIN, gestrichelt=True, dicke=3)],
    punkte=[{"x": r4(hm), "y": 120, "farbe": DRU, "beschriftung": "(11.9 m; 120 kPa)", "beschriftung_bei": [11.4, 128], "anker": "end"}],
    texte=[T(12.3, 98, "Meerwasser", DRU, 26, anker="start")]))
speichere(n, d)

# ======================================================== Luftdruck (Kapitel 3)
n = 'p4-5-lp-kontrolle-luftdruck'; d = lade(n)
# F1: Strohhalm im Glas
fl = [F(rechteck(2, 1, 8, 4), deckung=0.14), F(rechteck(4.6, 4, 5.4, 7), deckung=0.14)]
st = becher(2, 8, 1, 5.2) + [S((4.6, 1.4), (4.6, 9), dicke=3), S((5.4, 1.4), (5.4, 9), dicke=3), S((2, 4), (8, 4), dicke=2)]
st += [P((x, 5.9), (x, 4.1), TIN, dicke=5) for x in (2.8, 3.8, 6.2, 7.2)]
st += [P((5, 4.4), (5, 6.7), DRU, dicke=4)]
setze(d, 'Frage 1', skizze(0, 0, 10, flaechen=fl, strecken=st,
    texte=[T(3.3, 6.3, "Luftdruck"), T(6.7, 6.3, "Luftdruck"),
           T(5, 9.4, "Mund: nur weniger Druck", TIN, 26),
           T(5.65, 7.6, "hochgedrückt", DRU, 25, anker="start"),
           T(5, 0.3, "Die Luft draussen drückt.", TIN, 27)]))
# F2: Luftdruck über der Höhe (Modell des Leitprogramms)
pl = lambda h: 1013 * math.exp(-h / 8400)
orte = [(0, 1013), (1560, 841), (3454, 671)]
for h, p in orte:
    assert round(pl(h)) == p
setze(d, 'Frage 2', graf([-480, 5600], [-110, 1170], [1000, 2000, 3000, 4000, 5000], [200, 400, 600, 800, 1000], 'Höhe [m]', 'p [hPa]',
    kurven=[{"formel": "1013*exp(-x/8400)", "von": 0, "bis": 5000, "farbe": TIN, "dicke": 5}],
    punkte=[{"x": h, "y": p, "farbe": TIN} for h, p in orte],
    texte=[T(130, 1075, "Meereshöhe (0 m; 1013 hPa)", TIN, 25, anker="start"),
           T(1680, 930, "Davos", TIN, 25, anker="start"), T(1680, 885, "(1560 m; 841 hPa)", TIN, 25, anker="start"),
           T(3570, 760, "Jungfraujoch", TIN, 25, anker="start"), T(3570, 715, "(3454 m; 671 hPa)", TIN, 25, anker="start")]))
# F3: 50 hPa weniger im Halm: 0.51 m Wasser
hs = 5000 / (1000 * G)
assert round(hs, 2) == 0.51
fl = [F(rechteck(-0.1, -0.1, 0.1, 0), deckung=0.14), F(rechteck(-0.012, 0, 0.012, hs), deckung=0.14)]
st = becher(-0.1, 0.1, -0.1, 0.035) + [S((-0.012, -0.085), (-0.012, 0.6), dicke=3), S((0.012, -0.085), (0.012, 0.6), dicke=3),
                                        S((-0.1, 0), (0.1, 0), dicke=2)]
st += [P((-0.056, 0.09), (-0.056, 0.006), TIN, dicke=4), P((0.056, 0.09), (0.056, 0.006), TIN, dicke=4)]
st += [S((0.012, hs), (0.12, hs), gestrichelt=True), S((0.1, 0), (0.12, 0), gestrichelt=True),
       P((0.12, hs / 2), (0.12, hs - 0.004), ORA, dicke=4), P((0.12, hs / 2), (0.12, 0.004), ORA, dicke=4)]
setze(d, 'Frage 3', skizze(-0.35, -0.15, 0.8, flaechen=fl, strecken=st,
    texte=[T(0.14, 0.255, "h ≈ 0.51 m", ORA, 28, anker="start"),
           T(-0.03, 0.62, "im Halm: 50 hPa weniger", DRU, 26, anker="middle"),
           T(-0.115, 0.06, "Luftdruck", TIN, 25, anker="end"),
           T(0.0, -0.135, "Wasser", TIN, 24)]))
# F4: Wasser- und Quecksilbersäule, massstäblich
hw, hq = 101300 / (1000 * G), 101300 / (13600 * G)
assert round(hw, 1) == 10.3 and round(hq, 2) == 0.76
fl = [F(rechteck(0.4, -0.5, 4.2, 0), deckung=0.14), F(rechteck(2.0, 0, 2.6, hw), deckung=0.14),
      F(rechteck(5.6, -0.5, 9.4, 0), deckung=0.55), F(rechteck(7.2, 0, 7.8, hq), deckung=0.55)]
st = becher(0.4, 4.2, -0.5, 0.4) + becher(5.6, 9.4, -0.5, 0.4)
st += [S((2.0, -0.3), (2.0, 11), dicke=3), S((2.6, -0.3), (2.6, 11), dicke=3), S((2.0, 11), (2.6, 11), dicke=3),
       S((7.2, -0.3), (7.2, 1.1), dicke=3), S((7.8, -0.3), (7.8, 1.1), dicke=3), S((7.2, 1.1), (7.8, 1.1), dicke=3)]
st += [S((2.6, hw), (3.3, hw), gestrichelt=True), P((3.15, 5), (3.15, hw - 0.05), ORA, dicke=4), P((3.15, 5), (3.15, 0.05), ORA, dicke=4),
       S((7.8, hq), (8.6, hq), gestrichelt=True)]
setze(d, 'Frage 4', skizze(-0.6, -1.4, 12.5, flaechen=fl, strecken=st,
    texte=[T(3.35, 5.3, "10.3 m", ORA, 28, anker="start"), T(8.75, 0.62, "0.76 m", ORA, 28, anker="start"),
           T(2.3, -1.2, "Wasser"), T(7.5, -1.2, "Quecksilber"),
           T(7.5, 3.3, "13.6-mal dichter:", TIN, 26), T(7.5, 2.7, "13.6-mal kürzer", TIN, 26)]))
# F5: Barometer morgens und abends (qualitativ)
fl, st = [], []
for x0, hsaeule, L, wort in ((1.3, 4.6, 0.9, "morgens"), (6.0, 5.8, 1.6, "abends")):
    fl += [F(rechteck(x0, 0, x0 + 3, 0.5), deckung=0.55), F(rechteck(x0 + 1.2, 0.5, x0 + 1.8, hsaeule), deckung=0.55)]
    st += becher(x0, x0 + 3, 0, 0.9)
    st += [S((x0 + 1.2, 0.2), (x0 + 1.2, 6.9), dicke=3), S((x0 + 1.8, 0.2), (x0 + 1.8, 6.9), dicke=3), S((x0 + 1.2, 6.9), (x0 + 1.8, 6.9), dicke=3)]
    st += [P((x0 + 0.5, 0.55 + L), (x0 + 0.5, 0.55), TIN, dicke=5), P((x0 + 2.5, 0.55 + L), (x0 + 2.5, 0.55), TIN, dicke=5)]
st += [S((4.1, 4.6), (7.2, 4.6), ORA, gestrichelt=True, dicke=3), P((8.3, 4.6), (8.3, 5.75), ORA, dicke=4)]
setze(d, 'Frage 5', skizze(0, -1.9, 10, flaechen=fl, strecken=st,
    texte=[T(2.8, -0.7, "morgens"), T(7.5, -0.7, "abends"),
           T(2.8, -1.4, "Luftdruck kleiner", TIN, 24), T(7.5, -1.4, "Luftdruck grösser", TIN, 24),
           T(8.5, 5.0, "steigt", ORA, 26, anker="start"),
           T(5, 7.45, "Säule höher: Luftdruck höher", TIN, 28)]))
speichere(n, d)

# ======================================================== Pascal (Kapitel 4)
n = 'p4-5-lp-kontrolle-pascal'; d = lade(n)
# F1: Pascal'sche Kugel
cx, cy, rk = 0.8, -0.2, 2.6
yb = math.sqrt(rk ** 2 - 0.6 ** 2)
fl = [F(kreispunkte(cx, cy, rk), deckung=0.14), F(rechteck(-3.3, cy - 0.6, cx - yb, cy + 0.6), deckung=0.14)]
st = kreislinie(cx, cy, rk, dicke=4)
st += [S((-4.2, cy + 0.6), (cx - yb, cy + 0.6), dicke=4), S((-4.2, cy - 0.6), (cx - yb, cy - 0.6), dicke=4),
       S((-3.3, cy - 0.58), (-3.3, cy + 0.58), dicke=9), S((-4.6, cy), (-3.3, cy), dicke=4)]
st += [P((-4.95, cy + 1.1), (-3.5, cy + 1.1), DRU, dicke=5)]
for wg in (0, 40, -40, 80, -80, 120, -120):
    w = math.radians(wg)
    st.append(P((cx + (rk + 0.12) * math.cos(w), cy + (rk + 0.12) * math.sin(w)),
                (cx + (rk + 1.25) * math.cos(w), cy + (rk + 1.25) * math.sin(w)), DRU, dicke=5))
setze(d, 'Frage 1', skizze(-5, -5, 10, flaechen=fl, strecken=st,
    texte=[T(-4.95, cy + 1.45, "hineindrücken", DRU, 25, anker="start"), T(cx, cy - 0.1, "gleicher Druck", DRU, 26),
           T(cx, -4.75, "aus allen Löchern gleich stark", TIN, 26)]))


def presse(xk0, xk1, xg0, xg1, ykolben_k, ykolben_g, yo_k, yo_g, yu=0.0, kanal=1.0):
    """Hydraulische Presse im Schnitt: kleiner Zylinder links, grosser rechts, Kanal unten."""
    fl = [F([(xk0, yu), (xg1, yu), (xg1, ykolben_g), (xg0, ykolben_g), (xg0, yu + kanal), (xk1, yu + kanal), (xk1, ykolben_k), (xk0, ykolben_k)], deckung=0.14)]
    st = [S((xk0, yo_k), (xk0, yu), dicke=4), S((xk0, yu), (xg1, yu), dicke=4), S((xg1, yu), (xg1, yo_g), dicke=4),
          S((xk1, yo_k), (xk1, yu + kanal), dicke=4), S((xk1, yu + kanal), (xg0, yu + kanal), dicke=4), S((xg0, yu + kanal), (xg0, yo_g), dicke=4),
          S((xk0 + 0.04, ykolben_k), (xk1 - 0.04, ykolben_k), dicke=9), S((xg0 + 0.04, ykolben_g), (xg1 - 0.04, ykolben_g), dicke=9)]
    return fl, st


# F2: 60 N, 25-fache Fläche (Durchmesser 5-fach)
fl, st = presse(1.5, 2.5, 5.5, 10.5, 5, 5, 6.5, 6.5)
st += [P((2, 8.4), (2, 5.15), DRU, dicke=5), P((8, 5.15), (8, 9.0), DRU, dicke=9)]
setze(d, 'Frage 2', skizze(0, -2.2, 12, flaechen=fl, strecken=st,
    texte=[T(2.3, 7.2, "60 N", DRU, 28, anker="start"), T(8.35, 7.5, "1500 N", DRU, 30, anker="start"),
           T(2, -0.75, "Fläche A", TIN, 25), T(8, -0.75, "Fläche 25 · A", TIN, 25), T(8, -1.55, "(Durchmesser 5-mal)", TIN, 22),
           T(8, 2.6, "gleicher Druck", DRU, 26)]))
# F3: 40 cm hinein, 20-fache Fläche: 2 cm hoch (Kolben mit gleicher Tiefe, Fläche ~ Breite)
assert 40 * 1.5 == 2 * 30
fl, st = presse(2, 3.5, 20, 50, 4, 6, 46, 14, yu=-8, kanal=4)
fl += [F(rechteck(2, 4, 3.5, 44), ORA, 0.45), F(rechteck(20, 4, 50, 6), ORA, 0.45)]
st += [S((2.05, 44), (3.45, 44), gestrichelt=True, dicke=4), S((20.05, 4), (49.95, 4), gestrichelt=True, dicke=2),
       S((3.5, 44), (6.5, 44), gestrichelt=True, dicke=2), S((3.5, 4), (6.5, 4), gestrichelt=True, dicke=2),
       P((5.5, 24), (5.5, 43.6), ORA, dicke=4), P((5.5, 24), (5.5, 4.4), ORA, dicke=4),
       S((50, 6), (53, 6), gestrichelt=True, dicke=2)]
setze(d, 'Frage 3', skizze(-4, -15, 64, flaechen=fl, strecken=st,
    texte=[T(6.5, 22.5, "40 cm", ORA, 28, anker="start"), T(51.5, 8.8, "2 cm", ORA, 28, anker="start"),
           T(35, 17, "gleiches Volumen,", ORA, 26), T(35, 13, "20-mal so breit", ORA, 26),
           T(2.75, -12.5, "Fläche A", TIN, 24), T(35, -12.5, "Fläche 20 · A", TIN, 24),
           T(35, 26, "vorher: gestrichelt", TIN, 22)]))
# F4: Auto 4000 N auf 250 cm², kleiner Kolben 5 cm²: 80 N
assert 4000 * 5 / 250 == 80
r_ = math.sqrt(250 / 5)
xg0 = 4.9; xg1 = xg0 + 0.8 * r_
fl, st = presse(1.4, 2.2, xg0, xg1, 5, 5, 6.3, 6.3)
st += [P((1.8, 7.6), (1.8, 5.15), DRU, dicke=5), P(((xg0 + xg1) / 2, 9.2), ((xg0 + xg1) / 2, 5.15), DRU, dicke=9)]
setze(d, 'Frage 4', skizze(0, -2.2, 12, flaechen=fl, strecken=st,
    texte=[T(2.1, 6.6, "80 N", DRU, 28, anker="start"), T((xg0 + xg1) / 2 + 0.35, 7.6, "4000 N (Auto)", DRU, 28, anker="start"),
           T(1.8, -0.75, "5 cm²", TIN, 25), T((xg0 + xg1) / 2, -0.75, "250 cm²", TIN, 25),
           T((xg0 + xg1) / 2, 2.6, "gleicher Druck", DRU, 26),
           T(1.8, -1.6, "1 Teil", TIN, 23), T((xg0 + xg1) / 2, -1.6, "50 Teile", TIN, 23)]))
# F5: 50 N auf 2 cm²
assert abs(50 / 0.0002 - 250000) < 1e-6
fl = [F(rechteck(4, 0.5, 6, 5), deckung=0.14)]
st = becher(4, 6, 0.5, 7.2) + [S((4.04, 5), (5.96, 5), dicke=9)]
st += [P((5, 8.6), (5, 5.15), DRU, dicke=5),
       P((5, 2.7), (5.82, 2.7), DRU, dicke=4), P((5, 2.7), (4.18, 2.7), DRU, dicke=4),
       P((5, 2.7), (5, 0.68), DRU, dicke=4), P((5, 2.7), (5, 4.82), DRU, dicke=4)]
setze(d, 'Frage 5', skizze(0, -1.4, 10, flaechen=fl, strecken=st,
    texte=[T(5.3, 7.6, "50 N", DRU, 28, anker="start"), T(6.3, 2.55, "p = 2.5 bar", DRU, 30, anker="start"),
           T(6.3, 1.85, "überall", DRU, 25, anker="start"),
           T(5, -0.25, "A = 2 cm²", TIN, 27), T(5, -1.0, "= 0.0002 m²", TIN, 27)]))
speichere(n, d)

# ======================================================== Auftrieb (Kapitel 5)
n = 'p4-5-lp-kontrolle-auftrieb'; d = lade(n)
# F1: 0.5 l unter Wasser — Auftrieb gleich dem Gewicht von 0.5 l Wasser
fa1 = 1000 * 0.0005 * G
assert round(fa1, 1) == 4.9
fl = [F(rechteck(0.5, 0, 5.5, 6), deckung=0.14), F(rechteck(2.0, 2.4, 3.6, 4.0), TIN, 0.35),
      F(rechteck(7.0, 2.4, 8.6, 4.0), deckung=0.14)]
st = becher(0.5, 5.5, 0, 7) + [S((0.5, 6), (5.5, 6), dicke=2)] + umriss(2.0, 2.4, 3.6, 4.0, dicke=3) + umriss(7.0, 2.4, 8.6, 4.0, dicke=3, gestrichelt=True)
st += [P((2.8, 3.2), (2.8, 5.7), AUF, dicke=6), P((7.8, 3.2), (7.8, 0.7), GEW, dicke=6)]
setze(d, 'Frage 1', skizze(0, -1, 10, flaechen=fl, strecken=st,
    texte=[T(3.05, 4.85, "Auftrieb", AUF, 26, anker="start"), T(3.05, 4.3, "4.9 N", AUF, 26, anker="start"),
           T(7.8, 4.35, "0.5 l Wasser", TIN, 26), T(8.05, 1.3, "wiegt", GEW, 26, anker="start"), T(8.05, 0.75, "4.9 N", GEW, 26, anker="start"),
           T(3.0, -0.6, "Körper, 0.5 l"), T(7.8, -0.6, "verdrängtes Wasser"),
           T(5, 8.2, "Auftrieb = Gewicht des verdrängten Wassers", TIN, 25)]))
# F2: 300 cm³ in Wasser und in Spiritus
fw, fs = 1000 * 0.0003 * G, 790 * 0.0003 * G
assert round(fw, 2) == 2.94 and round(fs, 2) == 2.32
k = 0.9
fl = [F(rechteck(0.5, 0, 4.5, 5.6), deckung=0.14), F(rechteck(5.5, 0, 9.5, 5.6), deckung=0.07),
      F(rechteck(1.8, 1.9, 3.2, 3.3), TIN, 0.35), F(rechteck(6.8, 1.9, 8.2, 3.3), TIN, 0.35)]
st = becher(0.5, 4.5, 0, 6.4) + becher(5.5, 9.5, 0, 6.4) + [S((0.5, 5.6), (4.5, 5.6), dicke=2), S((5.5, 5.6), (9.5, 5.6), dicke=2)]
st += umriss(1.8, 1.9, 3.2, 3.3, dicke=3) + umriss(6.8, 1.9, 8.2, 3.3, dicke=3)
st += [P((2.5, 2.6), (2.5, 2.6 + k * fw), AUF, dicke=6, gestrichelt=True), P((7.5, 2.6), (7.5, 2.6 + k * fs), AUF, dicke=6)]
setze(d, 'Frage 2', skizze(0, -1.4, 10, flaechen=fl, strecken=st,
    texte=[T(2.75, 4.55, "2.94 N", AUF, 26, anker="start"), T(7.75, 4.0, "2.32 N", AUF, 28, anker="start"),
           T(2.5, -0.65, "in Wasser", TIN, 26), T(7.5, -0.65, "in Spiritus", AUF, 26),
           T(5, 7.9, "gleiches Volumen, 300 cm³:", TIN, 26), T(5, 7.2, "Spiritus ist weniger dicht", TIN, 26)]))
# F3: Würfel unter Wasser, Druck wächst mit der Tiefe
fl = [F(rechteck(0.3, -0.75, 9.7, 7.5)), F(rechteck(3.5, 1.5, 6.5, 4.5), TIN, 0.3)]
st = [S((0.3, 7.5), (9.7, 7.5), dicke=3)] + umriss(3.5, 1.5, 6.5, 4.5, dicke=3)
kD = 0.3            # Pfeillänge je Meter Tiefe, Oberfläche bei y 7.5
oben, unten, mitte = 7.5 - 4.5, 7.5 - 1.5, 7.5 - 3.0
st += [P((5, 4.5 + kD * oben + 0.08), (5, 4.58), DRU, dicke=5), P((5, 1.5 - kD * unten - 0.08), (5, 1.42), DRU, dicke=5),
       P((3.5 - kD * mitte - 0.08, 3.0), (3.42, 3.0), DRU, dicke=5), P((6.5 + kD * mitte + 0.08, 3.0), (6.58, 3.0), DRU, dicke=5),
       P((8.7, 1.8), (8.7, 4.2), AUF, dicke=6)]
setze(d, 'Frage 3', skizze(0, -1.5, 10, flaechen=fl, strecken=st,
    texte=[T(5, 6.15, "oben: weniger tief, kleinerer Druck", DRU, 25),
           T(5, -1.25, "unten: tiefer, grösserer Druck", DRU, 25),
           T(9.6, 4.65, "Auftrieb", AUF, 25, anker="end")]))
# F4: Federwaage 12 N an der Luft, 3 N Auftrieb: 9 N
kN = 0.3
fl = [F(rechteck(1.0, -0.8, 9.0, 5.5), deckung=0.14), F(rechteck(3.8, 3.1, 5.2, 4.5), TIN, 0.35)]
st = becher(1.0, 9.0, -0.8, 6.2) + [S((1.0, 5.5), (9.0, 5.5), dicke=2)] + umriss(3.8, 3.1, 5.2, 4.5, dicke=3)
st += [S((4.5, 4.5), (4.5, 7.5), dicke=2)] + umriss(4.1, 7.5, 4.9, 8.6, dicke=3)
st += [P((4.5, 3.8), (4.5, 3.8 - 12 * kN), GEW, dicke=6), P((4.15, 3.8), (4.15, 3.8 + 3 * kN), AUF, dicke=6),
       P((4.85, 3.8), (4.85, 3.8 + 9 * kN), DRU, dicke=6)]
setze(d, 'Frage 4', skizze(0, -1.0, 10, flaechen=fl, strecken=st,
    texte=[T(4.3, 0.45, "Gewichtskraft 12 N", GEW, 26, anker="end"), T(3.7, 4.25, "Auftrieb 3 N", AUF, 26, anker="end"),
           T(5.05, 6.15, "Waage 9 N", DRU, 26, anker="start"), T(5.1, 7.9, "zeigt 9 N", DRU, 26, anker="start"),
           T(6.2, 2.0, "9 N + 3 N = 12 N", TIN, 25, anker="start")]))
# F5: derselbe Körper in Süss- und Salzwasser (Beispiel 1 l, Meerwasser 1025 kg/m³)
fsu, fsa = 1000 * 0.001 * G, 1025 * 0.001 * G
assert round(fsu, 2) == 9.81 and round(fsa, 2) == 10.06
k = 0.3
fl = [F(rechteck(0.5, 0, 4.5, 5.6), deckung=0.10), F(rechteck(5.5, 0, 9.5, 5.6), deckung=0.24),
      F(rechteck(1.8, 1.4, 3.2, 2.8), TIN, 0.35), F(rechteck(6.8, 1.4, 8.2, 2.8), TIN, 0.35)]
st = becher(0.5, 4.5, 0, 6.4) + becher(5.5, 9.5, 0, 6.4) + [S((0.5, 5.6), (4.5, 5.6), dicke=2), S((5.5, 5.6), (9.5, 5.6), dicke=2)]
st += umriss(1.8, 1.4, 3.2, 2.8, dicke=3) + umriss(6.8, 1.4, 8.2, 2.8, dicke=3)
st += [P((2.5, 2.1), (2.5, 2.1 + k * fsu), AUF, dicke=6), P((7.5, 2.1), (7.5, 2.1 + k * fsa), AUF, dicke=6),
       S((2.5, 2.1 + k * fsu), (9.3, 2.1 + k * fsu), gestrichelt=True, dicke=2)]
setze(d, 'Frage 5', skizze(0, -1.4, 10, flaechen=fl, strecken=st,
    texte=[T(2.75, 4.35, "9.81 N", AUF, 27, anker="start"), T(7.75, 4.0, "10.06 N", AUF, 28, anker="start"),
           T(2.5, -0.55, "Süsswasser", TIN, 25), T(2.5, -1.15, "1000 kg/m³", TIN, 23),
           T(7.5, -0.55, "Salzwasser", TIN, 25), T(7.5, -1.15, "1025 kg/m³", TIN, 23),
           T(5, 7.9, "Beispiel: Körper mit 1 l Volumen", TIN, 26), T(5, 7.2, "dichter: grösserer Auftrieb", AUF, 26)]))
speichere(n, d)

# ======================================================== Schwimmen (Kapitel 6)
n = 'p4-5-lp-kontrolle-schwimmen'; d = lade(n)
# F1: 1200 kg/m³ ganz unter Wasser: Gewichtskraft 6/5 des Auftriebs
kR = 0.0025
fl = [F(rechteck(1, 0, 9, 7), deckung=0.14), F(rechteck(4.2, 3.2, 5.8, 4.8), TIN, 0.4)]
st = becher(1, 9, 0, 7.6) + [S((1, 7), (9, 7), dicke=2)] + umriss(4.2, 3.2, 5.8, 4.8, dicke=3)
st += [P((4.75, 4.0), (4.75, 4.0 - kR * 1200), GEW, dicke=6), P((5.25, 4.0), (5.25, 4.0 + kR * 1000), AUF, dicke=6)]
setze(d, 'Frage 1', skizze(0, -1.4, 10, flaechen=fl, strecken=st,
    texte=[T(4.55, 1.3, "Gewichtskraft", GEW, 26, anker="end"), T(5.45, 6.0, "Auftrieb", AUF, 26, anker="start"),
           T(5.45, 1.3, "(1200)", GEW, 24, anker="start"), T(5.45, 5.4, "(1000)", AUF, 24, anker="start"),
           T(5, -0.75, "Gewichtskraft > Auftrieb: sinkt", TIN, 27),
           T(5, 8.1, "Dichte 1200 kg/m³ > Wasser 1000 kg/m³", TIN, 25)]))


def schwimmer(anteil, hoehe, x0=2.5, x1=7.5, yw=5.0, k=2.0, texte_=()):
    yu = yw - anteil * hoehe
    yo = yu + hoehe
    xm = (x0 + x1) / 2
    fl = [F(rechteck(0.3, -0.6, 9.7, yw), deckung=0.14), F(rechteck(x0, yu, x1, yo), GEW, 0.30)]
    st = [S((0.3, yw), (9.7, yw), dicke=3)] + umriss(x0, yu, x1, yo, GEW, dicke=3)
    st += [P((xm + 0.4, yu + hoehe / 2), (xm + 0.4, yu + hoehe / 2 - k), GEW, dicke=6),
           P((xm - 0.4, yu + anteil * hoehe / 2), (xm - 0.4, yu + anteil * hoehe / 2 + k), AUF, dicke=6)]
    st += [S((x1, yu), (8.4, yu), gestrichelt=True, dicke=2), S((x1, yo), (8.4, yo), gestrichelt=True, dicke=2),
           P((8.1, (yu + yw) / 2), (8.1, yu + 0.03), ORA, dicke=4), P((8.1, (yu + yw) / 2), (8.1, yw - 0.03), ORA, dicke=4),
           P((8.1, (yw + yo) / 2), (8.1, yw + 0.03), ORA, dicke=4), P((8.1, (yw + yo) / 2), (8.1, yo - 0.03), ORA, dicke=4)]
    return fl, st, xm, yu, yo


# F2: Balken 750 kg/m³: 75 % unter Wasser
assert 750 / 1000 == 0.75
fl, st, xm, yu, yo = schwimmer(0.75, 2.4)
setze(d, 'Frage 2', skizze(0, -1, 10, flaechen=fl, strecken=st,
    texte=[T(8.45, (yu + 5) / 2 - 0.15, "75 %", ORA, 27, anker="start"), T(8.45, (5 + yo) / 2 - 0.15, "25 %", ORA, 27, anker="start"),
           T(xm - 0.6, yu + 0.9 + 2.0, "Auftrieb", AUF, 26, anker="end"),
           T(xm + 0.6, yu + 1.2 - 2.0 - 0.1, "Gewichtskraft", GEW, 26, anker="start"),
           T(5, 8.3, "schwimmt: Auftrieb = Gewichtskraft", TIN, 26),
           T(5, -0.25, "750 : 1000 = 75 % unter Wasser", TIN, 26)]))
# F3: Brett 30 % eingetaucht: 300 kg/m³
fl, st, xm, yu, yo = schwimmer(0.30, 2.0, yw=4.4)
setze(d, 'Frage 3', skizze(0, -1, 10, flaechen=fl, strecken=st,
    texte=[T(8.45, (yu + 4.4) / 2 - 0.15, "30 %", ORA, 27, anker="start"), T(8.45, (4.4 + yo) / 2 - 0.15, "70 %", ORA, 27, anker="start"),
           T(xm - 0.6, yu + 0.3 + 2.0 + 0.1, "Auftrieb", AUF, 26, anker="end"),
           T(xm + 0.6, yu + 1.0 - 2.0 - 0.15, "Gewichtskraft", GEW, 26, anker="start"),
           T(5, 8.3, "30 % unter Wasser:", TIN, 26), T(5, 7.6, "Dichte 0.3 · 1000 kg/m³ = 300 kg/m³", TIN, 26)]))
# F4: Ball 150 kg/m³ unter Wasser: Auftrieb ist 6.7-mal die Gewichtskraft
kB = 0.0033
rB = 0.9
lo, hi = 0.0, 2 * rB                                      # eingetauchte Kappenhöhe für 15 % des Volumens
for _ in range(60):
    m = (lo + hi) / 2
    if math.pi * m * m * (3 * rB - m) / 3 / (4 / 3 * math.pi * rB ** 3) < 0.15:
        lo = m
    else:
        hi = m
hK = lo
yw = 6.8
fl = [F(rechteck(0.3, -0.7, 9.7, yw), deckung=0.14), F(kreispunkte(3.2, 2.8, rB), TIN, 0.25)]
st = [S((0.3, yw), (9.7, yw), dicke=3)] + kreislinie(3.2, 2.8, rB, dicke=3) + kreislinie(7.4, yw - hK + rB, rB, dicke=3, gestrichelt=True)
st += [P((3.2, 2.8), (3.2, 2.8 + kB * 1000), AUF, dicke=6), P((3.2, 2.8), (3.2, 2.8 - kB * 150), GEW, dicke=6),
       P((4.4, 3.3), (6.5, yw - 0.6), TIN, gestrichelt=True, dicke=3)]
setze(d, 'Frage 4', skizze(0, -1.4, 10, flaechen=fl, strecken=st,
    texte=[T(3.45, 5.3, "Auftrieb", AUF, 27, anker="start"), T(3.2, 1.35, "Gewichtskraft", GEW, 26),
           T(3.2, 0.75, "(klein)", GEW, 23),
           T(7.6, 4.2, "steigt, bis er schwimmt", TIN, 25),
           T(5, -1.15, "ganz unter Wasser: Auftrieb > Gewichtskraft", TIN, 25)]))
# F5: Würfel 500 und 900 kg/m³
fl = [F(rechteck(0.3, -0.6, 9.7, 4.5), deckung=0.14)]
st = [S((0.3, 4.5), (9.7, 4.5), dicke=3)]
for x0, a in ((1.6, 0.5), (6.0, 0.9)):
    yu = 4.5 - a * 2.4
    fl.append(F(rechteck(x0, yu, x0 + 2.4, yu + 2.4), GEW, 0.30))
    st += umriss(x0, yu, x0 + 2.4, yu + 2.4, GEW, dicke=3)
    if a == 0.5:
        yo = yu + 2.4
        st += [S((x0 + 2.4, yo), (x0 + 3.1, yo), gestrichelt=True, dicke=2),
               P((x0 + 2.85, (4.5 + yo) / 2), (x0 + 2.85, yo - 0.03), ORA, dicke=4),
               P((x0 + 2.85, (4.5 + yo) / 2), (x0 + 2.85, 4.53), ORA, dicke=4)]
setze(d, 'Frage 5', skizze(0, -1.4, 10, flaechen=fl, strecken=st,
    texte=[T(2.8, 1.9, "500 kg/m³", TIN, 25), T(2.8, 1.3, "50 % unter Wasser", TIN, 23),
           T(7.2, 1.2, "900 kg/m³", TIN, 25), T(7.2, 0.6, "90 % unter Wasser", TIN, 23),
           T(4.7, 6.3, "ragt weiter heraus", ORA, 26, anker="start"),
           T(5, -1.15, "kleinere Dichte: kleinerer Anteil unter Wasser", TIN, 24)]))
speichere(n, d)
print('ok')
