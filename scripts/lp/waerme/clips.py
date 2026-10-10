"""Erzeugt die vierzehn Drehbücher des Leitprogramms Wärme (clips/p5-2-lp-*.json).

  python3 scripts/lp/waerme/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/waerme/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/waerme/clips.py --neu p5-2-lp-bilanz …   # nur diese

Dieses Skript ist die Quelle der Drehbücher (wie README.md sagt): Späte Korrekturen hier machen, nicht im
JSON — ein Lauf mit --neu überschreibt das JSON samt «dauer», «ein»/«aus» und Antwortbildern. Darum nach
jedem --neu die ganze Kette unten laufen lassen (Skript neu.sh im Arbeitsordner oder von Hand); erst
build-clip-ton.py schreibt die gemessene Dauer wieder hinein.

Ablauf je Clip: clips.py → build-clip-ton.py → (Kontrollclips) build-clip-fragen-ton.py → antworten.py
(Antwortbilder der Kontrollclips) → scripts/lp/kinematik/anker.py (Elemente mit «_anker») →
scripts/lp/waerme/teilanker.py (Teile eines graf mit «_ein»/«_aus»/«_bahn») → build-clips.py.

Farben (Theme begreifbar-schlicht: 1 Bernstein, 2 Orange, 3 Grün, 4 Rot, 5 Tinte), wie im Leitprogramm:
  1 Bernstein  Temperatur eines Körpers
  2 Orange     zugeführte Energie, Licht
  3 Grün       Nutzen (Strom, Nutzwärme)
  4 Rot        Wärme (übertragen, abgestrahlt, Verlust)
  5 Tinte      Wasser (Leitprogramm: Blau — das Theme kennt kein Blau), Körper, Gefässe, Achsen
Bilder: Aufnahmen der Simulationen (clips/bilder/p5-2-lp-*.jpg, Plan: aufnahme.json) und Skizzen als graf.
Zahlen im Sprechertext ausgeschrieben (CLAUDE.md). Alle Zahlen mit python3 nachgerechnet (siehe README).
"""
import json
import math
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv
NUR = [a for a in sys.argv[1:] if not a.startswith('--')]

KOPF = {
    'themenbereich': 'Thermodynamik · BM', 'lerngebiet': '5 · Thermodynamik',
    'lektion': ['p5-2'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-07', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Wärme sehen', 'nachlauf': 2.6, 'probe': True,
}
JETZT = {'name': 'Jetzt du', 'layout': 'zentriert', 'oben': 200,
         'sprecher': 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
         'elemente': [{'typ': 'titel', 'text': 'Jetzt du', 'x': 150, 'y': 280, 'groesse': 86},
                      {'typ': 'notiz', 'text': 'Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.',
                       'x': 150, 'y': 430, 'groesse': 50, 'farbe': 'blau', 'ein': 0.6}]}
BER, ORA, GRU, ROT, TIN = 1, 2, 3, 4, 5


# ------------------------------------------------------------------ Bausteine
def anker(e, a, versatz=None):
    if a:
        e['_anker'] = a
    if versatz:
        e['_versatz'] = versatz
    return e


def formel(t, y=300, g=46, a=None, ein=0.8, v=None):
    return anker({'typ': 'formel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'ein': ein}, a, v)


def notiz(t, y=460, farbe='tinte', g=42, a=None, ein=2.0, v=None):
    return anker({'typ': 'notiz', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'farbe': farbe, 'ein': ein}, a, v)


def titel(t, y=300, g=72):
    return {'typ': 'titel', 'text': t, 'x': 150, 'y': y, 'breite': 1640, 'groesse': g}


def bild(datei, a=None, ein=0.05, v=None, breite=640, y=180):
    return anker({'typ': 'bild', 'datei': 'bilder/' + datei, 'x': 1010, 'y': y, 'breite': breite, 'abstand': 0, 'anim': 'fade', 'ein': ein}, a, v)


def graf(xb, yb, xt=(), yt=(), xname='', yname='', a=None, ein=0.05, achsen=True, v=None, **kw):
    g = {'typ': 'graf', 'x': 1010, 'y': 175, 'breite': 760, 'hoehe': 760, 'abstand': 0, 'anim': 'fade', 'ein': ein,
         'pfeile': achsen, 'xbereich': list(xb), 'ybereich': list(yb),
         'xteilung': [x if isinstance(x, list) else [x, ('%g' % x).replace('-', '−')] for x in xt] or [[1e9, '']],
         'yteilung': [y if isinstance(y, list) else [y, ('%g' % y).replace('-', '−')] for y in yt] or [[1e9, '']],
         'xname': xname, 'yname': yname}
    if not achsen:
        g['achsen'] = False
    g.update(kw)
    return anker(g, a, v)


def skizze(a=None, ein=0.05, span=10, **kw):
    """Bild ohne Achsen, quadratisches Fenster 0…span (1:1)."""
    return graf((0, span), (0, span), achsen=False, a=a, ein=ein, **kw)


def r4(v):
    return round(v, 4)


def S(von, bis, farbe=TIN, **kw):
    d = {'von': [r4(von[0]), r4(von[1])], 'bis': [r4(bis[0]), r4(bis[1])], 'farbe': farbe}
    d.update(kw)
    return d


def P(von, bis, farbe, **kw):
    kw.setdefault('dicke', 6)
    return S(von, bis, farbe, pfeil=True, **kw)


def T(x, y, text, farbe=TIN, groesse=26, anker_='middle', **kw):
    d = {'bei': [r4(x), r4(y)], 'text': text, 'farbe': farbe, 'groesse': groesse, 'anker': anker_}
    d.update(kw)
    return d


def F(pts, farbe=TIN, deckung=0.15, **kw):
    d = {'punkte': [[r4(x), r4(y)] for x, y in pts], 'farbe': farbe, 'deckung': deckung}
    d.update(kw)
    return d


def rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def umriss(x0, y0, x1, y1, farbe=TIN, dicke=4, **kw):
    p = rechteck(x0, y0, x1, y1)
    return [S(p[i], p[(i + 1) % 4], farbe, dicke=dicke, **kw) for i in range(4)]


def becher(x0, x1, yb, yo, dicke=5, **kw):
    return [S((x0, yo), (x0, yb), dicke=dicke, **kw), S((x0, yb), (x1, yb), dicke=dicke, **kw), S((x1, yb), (x1, yo), dicke=dicke, **kw)]


def welle(x, y0, y1, farbe=ROT, n=6, amp=0.18, **kw):
    """senkrechte Wellenlinie aus Strecken (Strahlung), Pfeil am Ende"""
    pts = []
    for i in range(n * 8 + 1):
        t = i / (n * 8)
        pts.append((x + amp * math.sin(2 * math.pi * n * t), y0 + (y1 - y0) * t))
    st = [S(pts[i], pts[i + 1], farbe, dicke=4, **kw) for i in range(len(pts) - 1)]
    st[-1]['pfeil'] = True
    return st


def sz(name, sprecher, *elemente):
    return {'name': name, 'layout': 'zentriert', 'oben': 200, 'sprecher': sprecher, 'elemente': list(elemente)}


def wahl(szene, text, optionen, richtig, rueck, sprich=None, rueck_sprich=None, kopf=None):
    F_ = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'text': text, 'optionen': optionen, 'richtig': richtig,
          'rueck': {str(k): v for k, v in rueck.items()}}
    if kopf:
        F_['kopf'] = kopf
    F_['sprich'] = sprich or text
    F_['rueck_sprich'] = {str(k): v for k, v in (rueck_sprich or rueck).items()}
    return F_


DREH = []
EIN = 'Einführungsclip des Leitprogramms Wärme, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Wärme, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'


def merke(sprecher, f, n):
    return sz('Merke', sprecher, titel('Zum Mitnehmen', y=260, g=76), formel(f, y=420, g=46, ein=0.4), notiz(n, y=570, ein=1.2))


# ================================================================== Kapitel 1: Wärme und Temperatur
def topf(extra_s=(), extra_t=()):
    """Stahltopf mit Wasser auf der Platte (Fenster 0…10)."""
    st = becher(2.5, 7.5, 3.0, 6.6, dicke=8) + [S((2.0, 2.55), (8.0, 2.55), TIN, dicke=12)] + list(extra_s)
    fl = [F(rechteck(2.62, 3.12, 7.38, 5.9), TIN, 0.12)]
    tx = [T(5, 7.3, 'Topf: 0.9 kg Stahl'), T(5, 4.4, 'Wasser: 1.5 l'), T(5, 1.75, 'von 15 °C auf 95 °C')] + list(extra_t)
    return st, fl, tx


LINKS = [(1.4, 3.1), (2.9, 3.7), (4.1, 3.0), (1.8, 5.1), (3.3, 5.5), (4.25, 6.4), (1.3, 6.9), (2.6, 7.3)]
RICHT = [0.5, 2.2, 3.9, 5.4, 1.2, 2.9, 4.6, 0.1]


def teilchen(punkte, laenge, farbe=TIN, **kw):
    st = []
    for (x, y), w in zip(punkte, RICHT):
        st.append(P((x, y), (x + laenge * math.cos(w), y + laenge * math.sin(w)), farbe, dicke=4, **kw))
    return st


rechts = [(x + 4.4, y) for x, y in LINKS]
s_t, f_t, t_t = topf()
t_t = [dict(t, _ein=w) for t, w in zip(t_t, ['Stahltopf von null', 'eineinhalb Liter', 'von fünfzehn'])]   # gegebene Werte erst mit dem Wort
s_t2, f_t2, t_t2 = topf([P((5.0, 2.7), (5.0, 3.9), ROT, dicke=7, _ein='jeder mit seinem eigenen c'),
                         P((7.95, 2.7), (7.95, 5.0), ROT, dicke=7, _ein='jeder mit seinem eigenen c', _ein_versatz=0.4)],
                        [T(5.45, 3.6, 'Q Wasser', ROT, 26, 'start', _ein='jeder mit seinem eigenen c'),
                         T(8.35, 4.6, 'Q Topf', ROT, 26, 'start', _ein='jeder mit seinem eigenen c', _ein_versatz=0.4)])
QW, QT = 1.5 * 4182 * 80, 0.9 * 450 * 80
assert abs(QW - 501840) < 1e-6 and abs(QT - 32400) < 1e-6 and abs((QW + QT) / 1000 - 534.24) < 1e-9
gl_k = lambda t, a: 50 + a * 30 * math.exp(-t / 10)
DREH.append(dict(KOPF, titel='Wärme sehen: Energie, die fliesst', dateiname='p5-2-lp-waerme',
    kurzbeschrieb='Wärme als Energie, die wegen eines Temperaturunterschieds durch Teilchenstösse übertragen wird, das thermische Gleichgewicht und die Wärmemenge Q = m · c · ΔT — mit einem vorgerechneten Problem: Wasser im Stahltopf.',
    schlagworte=['Wärme', 'Temperatur', 'Teilchenbewegung', 'thermisches Gleichgewicht', 'spezifische Wärmekapazität'], _probe=EIN % 1,
    szenen=[
        sz('Tasse', 'Du hältst eine heisse Tasse Tee in kalten Händen. Nach kurzer Zeit sind die Hände warm und der Tee etwas kühler. Was ist da von der Tasse in die Hände gegangen?',
           titel('Was geht in die Hände?', g=66),
           notiz('heisser Tee,|kalte Hände', y=460, a='Du hältst'),
           skizze(strecken=becher(3.6, 6.4, 2.6, 7.2, dicke=6) + [
                      P((3.4, 4.6), (2.3, 4.6), ROT, dicke=7, _ein='Was ist da'), P((6.6, 4.6), (7.7, 4.6), ROT, dicke=7, _ein='Was ist da')],
                  flaechen=[F(rechteck(3.66, 2.66, 6.34, 6.4), TIN, 0.14),
                            F([(1.1, 3.2), (3.5, 3.0), (3.55, 6.3), (2.2, 6.6), (1.1, 5.6)], TIN, 0.3),
                            F([(8.9, 3.2), (6.5, 3.0), (6.45, 6.3), (7.8, 6.6), (8.9, 5.6)], TIN, 0.3)],
                  texte=[T(5, 4.6, 'Tee, heiss'), T(2.1, 2.2, 'Hand, kalt'), T(7.9, 2.2, 'Hand, kalt'),
                         T(5, 8.1, '?', ROT, 44, _ein='Was ist da')])),
        sz('Teilchen', 'Die Temperatur misst, wie heftig sich die Teilchen im Mittel bewegen: im heissen Tee schnell, in der kalten Hand langsamer. An der Berührfläche stossen die schnellen Teilchen die langsamen an und geben ihnen Bewegungsenergie ab. Diese übertragene Energie heisst Wärme.',
           notiz('Temperatur: wie heftig sich|die Teilchen bewegen (Zustand)', y=300, a='Die Temperatur misst'),
           notiz('Wärme @Q@: übertragene Energie|(Vorgang, in Joule)', y=470, a='Diese übertragene Energie', farbe='rot'),
           skizze(strecken=[S((5, 1.6), (5, 8.4), TIN, dicke=3)]
                  + teilchen(LINKS, 1.05, _aus='geben ihnen Bewegungsenergie ab') + teilchen(rechts, 0.45, _aus='geben ihnen Bewegungsenergie ab')
                  + teilchen(LINKS, 0.8, _ein='geben ihnen Bewegungsenergie ab') + teilchen(rechts, 0.7, _ein='geben ihnen Bewegungsenergie ab')
                  + [P((3.6, 9.0), (6.4, 9.0), ROT, dicke=7, beschriftung='Wärme Q', beschriftung_bei=[5, 9.45], groesse=28, _ein='Diese übertragene Energie')],
                  flaechen=[F(rechteck(0.6, 1.6, 4.95, 8.4), TIN, 0.08), F(rechteck(5.05, 1.6, 9.4, 8.4), TIN, 0.04),
                            F(rechteck(4.7, 1.6, 5.3, 8.4), ROT, 0.25, _ein='An der Berührfläche', _aus='Diese übertragene Energie')],
                  punkte=[{'x': x, 'y': y, 'farbe': TIN} for x, y in LINKS + rechts],
                  texte=[T(2.75, 0.9, 'Tee: schnell'), T(7.25, 0.9, 'Hand: langsamer'),
                         T(5, 0.25, 'Berührfläche', ROT, 24, _ein='An der Berührfläche', _aus='Diese übertragene Energie')])),
        sz('Gleichgewicht', 'Von selbst fliesst Wärme nur vom wärmeren zum kälteren Körper. Der warme wird kühler, der kalte wärmer, bis beide gleich warm sind. Dann hört der Fluss auf: Das ist das thermische Gleichgewicht. Hier liegt es genau in der Mitte, weil beide gleich viel Wasser sind.',
           notiz('von selbst nur:|warm → kalt', y=300, a='Von selbst', farbe='rot'),
           notiz('gleich warm: Der Fluss hört auf.|thermisches Gleichgewicht', y=470, a='Dann hört der Fluss auf'),
           graf((-7, 64), (-11, 105), [10, 20, 30, 40, 50, 60], [20, 40, 60, 80, 100], 't [s]', 'ϑ [°C]',
                kurven=[{'formel': '50+30*exp(-x/10)', 'von': a, 'bis': b, 'farbe': BER, 'dicke': 5, '_ein': 'Der warme wird kühler', '_ein_versatz': 0.6 * i}
                        for i, (a, b) in enumerate([(0, 10), (10, 20), (20, 30), (30, 40), (40, 60)])]
                       + [{'formel': '50-30*exp(-x/10)', 'von': a, 'bis': b, 'farbe': TIN, 'dicke': 5, '_ein': 'Der warme wird kühler', '_ein_versatz': 0.6 * i}
                          for i, (a, b) in enumerate([(0, 10), (10, 20), (20, 30), (30, 40), (40, 60)])]
                       + [{'formel': '50+30*exp(-x/10)', 'von': 0, 'bis': 60, 'farbe': BER, 'dicke': 0.01,
                           'laeufer': {'_bahn': [['Der warme wird kühler', 0.6 * i, x] for i, x in enumerate([0, 10, 20, 30, 40])], 'farbe': BER}},
                          {'formel': '50-30*exp(-x/10)', 'von': 0, 'bis': 60, 'farbe': TIN, 'dicke': 0.01,
                           'laeufer': {'_bahn': [['Der warme wird kühler', 0.6 * i, x] for i, x in enumerate([0, 10, 20, 30, 40])], 'farbe': TIN}}],
                strecken=[S((0, 50), (62, 50), BER, dicke=3, gestrichelt=True, _ein='Das ist das thermische Gleichgewicht')],
                texte=[T(3, 86, 'warm: 80 °C', BER, 26, 'start'), T(3, 13, 'kalt: 20 °C', TIN, 26, 'start'),
                       T(60, 56, 'gleich warm: 50 °C', BER, 26, 'end', _ein='Das ist das thermische Gleichgewicht'),
                       T(60, 41, 'Mitte: gleiches m · c', BER, 22, 'end', _ein='genau in der Mitte')])),
        sz('Wärmemenge', 'Wie viel Wärme braucht ein Körper, um wärmer zu werden? Das hängt an drei Dingen: an der Masse, am Stoff und an der Temperaturänderung. Q gleich m mal c mal Delta T. Die spezifische Wärmekapazität c sagt, wie viel Wärme ein Kilogramm für ein Kelvin braucht: bei Wasser viertausendeinhundertzweiundachtzig Joule, bei Eisen nur vierhundertfünfzig.',
           formel(r'Q = m \cdot c \cdot \Delta T', y=290, g=60, a='Q gleich'),
           notiz('@m@: Masse in kg|@c@: spezifische Wärmekapazität|@\\Delta T@: Temperaturänderung in K', y=420, a='an der Masse'),
           graf((-1300, 4800), (-0.8, 6), [1000, 2000, 3000, 4000], [], 'c [J/(kg·K)]', '',
                flaechen=[F(rechteck(0, 3.7, 4182, 4.5), TIN, 0.35, _ein='bei Wasser'), F(rechteck(0, 1.7, 450, 2.5), TIN, 0.35, _ein='bei Eisen')],
                texte=[T(1750, 3.0, 'Wie viel Wärme?', ROT, 36, _aus='bei Wasser'), T(-120, 4.0, 'Wasser', TIN, 28, 'end', _ein='bei Wasser'), T(-120, 2.0, 'Eisen', TIN, 28, 'end', _ein='bei Eisen'),
                       T(2091, 4.85, '4182 J/(kg·K)', TIN, 28, _ein='bei Wasser'), T(700, 2.85, '450 J/(kg·K)', TIN, 28, 'start', _ein='bei Eisen')])),
        sz('Vergleich', 'Ein halbes Kilogramm Wasser und ein halbes Kilogramm Speiseöl bekommen je zwanzig Kilojoule. Das Wasser wird um knapp zehn Kelvin wärmer, das Öl um zwanzig. Gleiche Wärme, ganz verschiedene Temperaturänderung: Wärme und Temperatur sind eben nicht dasselbe.',
           notiz('je 0.5 kg, je 20 kJ', y=300, a='Ein halbes Kilogramm'),
           formel(r'\Delta T = \frac{Q}{m \cdot c}', y=410, g=50, a='Das Wasser wird'),
           notiz('gleiche Wärme,|andere Temperaturänderung', y=560, a='Gleiche Wärme', farbe='rot'),
           graf((-2.6, 23), (-2.6, 23), [5, 10, 15, 20], [5, 10, 15, 20], 'Q [kJ]', 'ΔT [K]',
                geraden=[{'bewegung': [[0, 1 / 2.091, 0]], 'ab': 0, 'farbe': TIN, 'dicke': 5, '_ein': 'Das Wasser wird', '_ein_versatz': -0.2,
                          'laeufer': {'_bahn': [['Das Wasser wird', 0.0, 0], ['Das Wasser wird', 1.6, 20]], 'farbe': TIN}},
                         {'bewegung': [[0, 1.0, 0]], 'ab': 0, 'farbe': TIN, 'dicke': 5, 'gestrichelt': True, '_ein': 'das Öl um zwanzig', '_ein_versatz': -0.6,
                          'laeufer': {'_bahn': [['das Öl um zwanzig', -0.4, 0], ['das Öl um zwanzig', 1.2, 20]], 'farbe': TIN}}],
                punkte=[{'x': 20, 'y': 20000 / (0.5 * 4182), 'farbe': TIN, 'beschriftung': '(20 kJ; 9.6 K)', 'beschriftung_bei': [19.6, 11.3], 'anker': 'end', '_ein': 'das Öl um zwanzig'},
                        {'x': 20, 'y': 20, 'farbe': TIN, 'beschriftung': '(20 kJ; 20 K)', 'beschriftung_bei': [19.4, 21.4], 'anker': 'end', '_ein': 'Gleiche Wärme'}],
                texte=[T(13.5, 3.8, 'Wasser', TIN, 28, _ein='Das Wasser wird'), T(8.5, 12.5, 'Speiseöl (gestrichelt)', TIN, 26, 'end', _ein='das Öl um zwanzig')])),
        sz('Problem Topf', 'Jetzt ein ganzes Problem. In einem Stahltopf von null Komma neun Kilogramm sind eineinhalb Liter Wasser. Beides soll von fünfzehn auf fünfundneunzig Grad warm werden. Wie viel Wärme braucht es? Stahl hat wie Eisen vierhundertfünfzig Joule pro Kilogramm und Kelvin.',
           notiz('Topf: 0.9 kg Stahl', y=300, a='Stahltopf von null'),
           notiz('Wasser: 1.5 l = 1.5 kg', y=360, a='eineinhalb Liter'),
           notiz('von 15 °C auf 95 °C', y=420, a='von fünfzehn'),
           notiz('gesucht: Wärme @Q@', y=530, a='Wie viel Wärme', farbe='rot'),
           notiz(r'@c_\text{Stahl} = 450\;\text{J/(kg·K)}@', y=650, a='Stahl hat'),
           skizze(strecken=s_t, flaechen=f_t, texte=t_t)),
        sz('Vorgehen Topf', 'Beide werden um achtzig Kelvin wärmer. Für jeden Körper gilt Q gleich m mal c mal Delta T, jeder mit seinem eigenen c. Am Schluss addiert man die beiden Wärmen.',
           formel(r'\Delta T = 95\;^\circ\text{C} - 15\;^\circ\text{C} = 80\;\text{K}', y=300, g=40, a='Beide werden'),
           formel(r'Q = m \cdot c \cdot \Delta T \;\text{je Körper}', y=420, g=40, a='Für jeden Körper'),
           formel(r'Q = Q_\text{W} + Q_\text{T}', y=540, g=46, a='Am Schluss'),
           skizze(strecken=s_t2, flaechen=f_t2, texte=t_t2)),
        sz('Lösung Topf', 'Wasser: eins Komma fünf Kilogramm mal viertausendeinhundertzweiundachtzig mal achtzig Kelvin, rund fünfhundertzwei Kilojoule. Topf: null Komma neun Kilogramm mal vierhundertfünfzig mal achtzig Kelvin, zweiunddreissig Komma vier Kilojoule. Zusammen rund fünfhundertvierunddreissig Kilojoule. Probe: Die Einheiten ergeben Joule, und der Topf braucht nur gut sechs Prozent, weil sein c viel kleiner ist.',
           formel(r'Q = m \cdot c \cdot \Delta T \;\text{je Körper}', y=210, g=34, ein=0.3),
           formel(r'Q_\text{W} = 1.5\;\text{kg} \cdot 4182\;\tfrac{\text{J}}{\text{kg·K}} \cdot 80\;\text{K}', y=280, g=34, a='Wasser:'),
           formel(r'\phantom{Q_\text{W}} \approx 502\;\text{kJ}', y=330, g=34, a='rund fünfhundertzwei'),
           formel(r'Q_\text{T} = 0.9\;\text{kg} \cdot 450\;\tfrac{\text{J}}{\text{kg·K}} \cdot 80\;\text{K}', y=400, g=34, a='Topf: null'),
           formel(r'\phantom{Q_\text{T}} = 32.4\;\text{kJ}', y=450, g=34, a='zweiunddreissig Komma vier'),
           formel(r'Q = Q_\text{W} + Q_\text{T} \approx 534\;\text{kJ}', y=530, g=40, a='Zusammen'),
           notiz('Probe: kg · J/(kg·K) · K = J', y=610, g=36, a='Die Einheiten ergeben'),
           notiz('Topf nur gut 6 %', y=670, g=36, a='sechs Prozent'),
           graf((-0.6, 4.2), (-60, 600), [], [100, 200, 300, 400, 500], '', 'Q [kJ]', a='Wasser:',
                flaechen=[F(rechteck(0.6, 0, 1.6, QW / 1000), ROT, 0.55, _ein='rund fünfhundertzwei'), F(rechteck(2.4, 0, 3.4, QT / 1000), ROT, 0.55, _ein='zweiunddreissig Komma vier')],
                texte=[T(1.1, -35, 'Wasser', TIN, 26), T(2.9, -35, 'Topf', TIN, 26),
                       T(1.1, 520, '502 kJ', ROT, 28, _ein='rund fünfhundertzwei'), T(2.9, 55, '32.4 kJ', ROT, 28, _ein='zweiunddreissig Komma vier')])),
        merke('Zum Mitnehmen: Die Temperatur ist ein Zustand, die Wärme ist übertragene Energie. Wie viel Wärme es braucht, sagt Q gleich m mal c mal Delta T.',
              r'Q = m \cdot c \cdot \Delta T', 'Temperatur: Zustand|Wärme: übertragene Energie'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Topf', 'Was musst du alles erwärmen?', ['nur das Wasser', 'Wasser und Topf, jedes mit seinem eigenen c', 'Wasser und Topf, beide mit dem c von Wasser'], 1,
                 {0: 'Steht der Topf nicht auch auf der heissen Platte?', 2: 'Ist der Topf aus Wasser? Jeder Stoff hat sein eigenes c.'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 1
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zu Wärme und Temperatur', dateiname='p5-2-lp-kontrolle-waerme',
    kurzbeschrieb='Fünf Fragen: was Wärme ist, warum ein Thermometer Zeit braucht, die Wärme für einen Pflasterstein, Proportionalität und welche Gerade zu Wasser gehört.',
    schlagworte=['Wärme', 'Temperatur', 'Wärmemenge', 'thermisches Gleichgewicht', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Wärme ist Energie, die wegen eines Temperaturunterschieds von einem Körper auf den anderen übergeht. Was ein Körper gespeichert hat, heisst innere Energie.',
           notiz('Wärme: übertragene Energie|Gespeichert: innere Energie', y=320, ein=1.0)),
        sz('Frage 2', 'Ein Thermometer zeigt immer seine eigene Temperatur. Es nimmt Wärme vom Tee auf, bis beide gleich warm sind. Erst im thermischen Gleichgewicht zeigt es die Temperatur des Tees.',
           notiz('Thermometer zeigt seine eigene|Temperatur: erst im Gleichgewicht|die des Tees', y=320, ein=1.0)),
        sz('Frage 3', 'Q gleich m mal c mal Delta T: zwei Komma fünf Kilogramm mal siebenhundertneunzig Joule pro Kilogramm und Kelvin mal zwölf Kelvin. Das sind dreiundzwanzigtausendsiebenhundert Joule, also rund dreiundzwanzig Komma sieben Kilojoule.',
           formel(r'Q = m \cdot c \cdot \Delta T', y=290, g=50, ein=1.0),
           formel(r'= 2.5\;\text{kg} \cdot 790\;\tfrac{\text{J}}{\text{kg·K}} \cdot 12\;\text{K} \approx 23.7\;\text{kJ}', y=400, g=34, ein=1.0)),
        sz('Frage 4', 'Die Wärme wächst proportional mit der Temperaturänderung. Für acht Kelvin braucht der Körper zwölf Kilojoule, für ein Kelvin also eins Komma fünf Kilojoule. Für zwanzig Kelvin sind es dreissig Kilojoule.',
           formel(r'\frac{12\;\text{kJ}}{8\;\text{K}} = 1.5\;\text{kJ/K}', y=300, g=46, ein=1.0),
           formel(r'1.5\;\text{kJ/K} \cdot 20\;\text{K} = 30\;\text{kJ}', y=430, g=46, ein=1.0)),
        sz('Frage 5', 'Wasser braucht je Kelvin viel mehr Wärme als Sand. Ist die Wärme nach oben aufgetragen, steigt seine Gerade darum steiler. A ist das Wasser.',
           notiz('grosses @c@: viel Wärme je Kelvin,|steile Gerade', y=320, ein=1.0),
           graf((-2.6, 23), (-18, 190), [5, 10, 15, 20], [40, 80, 120, 160], 'ΔT [K]', 'Q [kJ]', tippbar=False,
                strecken=[S((0, 0), (21, 21 * 2 * 4.182), TIN, dicke=5), S((0, 0), (21, 21 * 2 * 0.835), TIN, dicke=5)],
                texte=[T(16.5, 160, 'A', TIN, 34), T(19, 22, 'B', TIN, 34), T(5, 150, 'je 2 kg', TIN, 26, 'start')])),
    ],
    fragen=[
        wahl('Frage 1', 'Was ist Wärme?', ['die Energie, die ein heisser Körper gespeichert hat', 'Energie, die wegen eines Temperaturunterschieds übertragen wird', 'ein anderes Wort für hohe Temperatur'], 1,
             {0: 'Was ein Körper gespeichert hat, hat einen eigenen Namen. Wann spricht man von Wärme?', 2: 'Temperatur ist ein Zustand. Was geschieht, wenn sich zwei verschieden warme Körper berühren?'}),
        wahl('Frage 2', 'Du hältst ein Thermometer in heissen Tee. Warum musst du kurz warten, bevor du ablesen kannst?',
             ['Das Thermometer muss erst Wärme vom Tee aufnehmen, bis es dieselbe Temperatur hat.', 'Der Tee muss erst wärmer werden.', 'Das Thermometer muss erst seine Kälte an den Tee abgeben.'], 0,
             {1: 'Wird der Tee wärmer, wenn du ein kaltes Thermometer hineinhältst?', 2: 'Fliesst Kälte? Was fliesst wirklich, und in welche Richtung?'}),
        wahl('Frage 3', 'Ein Pflasterstein aus Granit (2.5 kg, c = 790 J/(kg·K)) wird in der Sonne um 12 K wärmer. Wie viel Wärme nimmt er auf?', ['23.7 kJ', '9.5 kJ', '237 kJ'], 0,
             {1: 'Hast du alle drei Grössen eingesetzt, auch die Masse?', 2: 'Prüfe die Umrechnung von Joule in Kilojoule.'},
             sprich='Ein Pflasterstein aus Granit, zwei Komma fünf Kilogramm schwer, mit siebenhundertneunzig Joule pro Kilogramm und Kelvin, wird in der Sonne um zwölf Kelvin wärmer. Wie viel Wärme nimmt er auf?'),
        wahl('Frage 4', 'Ein Körper nimmt 12 kJ auf und wird 8 K wärmer. Wie viel Wärme braucht er für 20 K?', ['24 kJ', '30 kJ', '4.8 kJ'], 1,
             {0: 'Du hast 12 kJ dazugezählt. Wächst die Wärme nicht im selben Verhältnis wie die Temperaturänderung?', 2: 'Mehr Erwärmung braucht mehr Wärme, nicht weniger.'},
             sprich='Ein Körper nimmt zwölf Kilojoule auf und wird acht Kelvin wärmer. Wie viel Wärme braucht er für zwanzig Kelvin?',
             rueck_sprich={0: 'Du hast zwölf Kilojoule dazugezählt. Wächst die Wärme nicht im selben Verhältnis wie die Temperaturänderung?', 2: 'Mehr Erwärmung braucht mehr Wärme, nicht weniger.'}),
        wahl('Frage 5', 'Je 2 kg Wasser und Sand bekommen Wärme. Das Diagramm zeigt die Wärme über der Temperaturänderung. Welche Gerade gehört zum Wasser?', ['A', 'B'], 0,
             {1: 'Welcher Stoff braucht für ein Kelvin mehr Wärme? Die Wärme ist nach oben aufgetragen.'},
             sprich='Je zwei Kilogramm Wasser und Sand bekommen Wärme. Das Diagramm zeigt die Wärme über der Temperaturänderung. Welche Gerade gehört zum Wasser?'),
    ]))

# ================================================================== Kapitel 2: Wärmebilanz
mA, mW = 0.25 * 896, 0.8 * 4182
tmA = (mA * 200 + mW * 15) / (mA + mW)
assert abs(tmA - 26.609) < 1e-3 and abs(mA * (200 - tmA) - mW * (tmA - 15)) < 1e-6 and abs(mA * (200 - tmA) - 38839.6) < 0.1


def zahlenstrahl(x0, x1, ticks, y=1.0):
    """Waagrechter Zahlenstrahl für Temperaturen (Fenster in °C)."""
    st = [S((x0, y), (x1, y), TIN, dicke=3, pfeil=True)]
    st += [S((t, y - 0.12), (t, y + 0.12), TIN, dicke=3) for t in ticks]
    tx = [T(t, y - 0.55, '%g' % t, TIN, 24) for t in ticks] + [T(x1, y + 0.45, 'ϑ [°C]', TIN, 24, 'end')]
    return st, tx


zs_s, zs_t = zahlenstrahl(0, 104, [0, 20, 40, 60, 80, 100], y=1.2)
za_s, za_t = zahlenstrahl(0, 215, [0, 50, 100, 150, 200], y=1.2)
DREH.append(dict(KOPF, titel='Wärme sehen: was der eine abgibt, nimmt der andere auf', dateiname='p5-2-lp-bilanz',
    kurzbeschrieb='Thermisches Gleichgewicht und Wärmebilanz Q_ab = Q_auf, die Mischtemperatur als mit m · c gewichteter Mittelwert — und ein vorgerechnetes Problem: ein heisses Aluminiumteil im Wasser.',
    schlagworte=['Wärmebilanz', 'thermisches Gleichgewicht', 'Mischtemperatur', 'spezifische Wärmekapazität'], _probe=EIN % 2,
    szenen=[
        sz('Mischen', 'Ein heisses Stück Metall kommt in kaltes Wasser. Welche Temperatur stellt sich ein? Liegt sie einfach in der Mitte?',
           titel('Wo landet die Temperatur?', g=62),
           notiz('heiss und kalt zusammen:|in der Mitte?', y=460, a='Liegt sie'),
           bild('p5-2-lp-bilanz-t0.jpg')),
        sz('Gleichgewicht', 'Das Eisen kühlt ab, das Wasser wird wärmer, bis beide gleich warm sind: thermisches Gleichgewicht. Im abgeschlossenen System geht dabei keine Energie verloren. Was das Eisen abgibt, nimmt das Wasser auf.',
           notiz('Eisen: 0.6 kg, 250 °C|Wasser: 0.8 kg, 20 °C', y=300, a='Das Eisen kühlt ab'),
           notiz('gleich warm:|thermisches Gleichgewicht', y=470, a='bis beide gleich warm'),
           notiz('abgegeben = aufgenommen', y=640, a='Was das Eisen abgibt', farbe='rot'),
           bild('p5-2-lp-bilanz-t0.jpg'),
           bild('p5-2-lp-bilanz-t5.jpg', a='Das Eisen kühlt ab', v=0.8),
           bild('p5-2-lp-bilanz-t15.jpg', a='das Wasser wird wärmer', v=0.6),
           bild('p5-2-lp-bilanz-ende.jpg', a='bis beide gleich warm')),
        sz('Bilanz', 'Das ist die Wärmebilanz: Q ab gleich Q auf. Jede Seite rechnet man mit m mal c mal ihrer Temperaturänderung bis zur Mischtemperatur. Für zwei Körper ohne Phasenwechsel lässt sich das nach der Mischtemperatur auflösen: ein Mittelwert, gewichtet mit m mal c.',
           formel(r'Q_\text{ab} = Q_\text{auf}', y=280, g=54, a='Das ist die Wärmebilanz'),
           formel(r'm_1 c_1 (\vartheta_1 - \vartheta_\text{m}) = m_2 c_2 (\vartheta_\text{m} - \vartheta_2)', y=400, g=36, a='Jede Seite'),
           formel(r'\vartheta_\text{m} = \frac{m_1 c_1 \vartheta_1 + m_2 c_2 \vartheta_2}{m_1 c_1 + m_2 c_2}', y=530, g=40, a='lässt sich das nach'),
           graf((-0.6, 4.2), (-12, 70), [], [], '', 'Q [kJ]', achsen=True, a='Das ist die Wärmebilanz',
                flaechen=[F(rechteck(0.6, 0, 1.6, 57.5), ROT, 0.55), F(rechteck(2.4, 0, 3.4, 57.5), ROT, 0.55)],
                strecken=[S((0.6, 57.5), (1.6, 57.5), ROT, dicke=3, _ein='Jede Seite'), S((2.4, 57.5), (3.4, 57.5), ROT, dicke=3, _ein='Jede Seite')],
                texte=[T(1.1, -7, 'Eisen gibt ab', TIN, 24), T(2.9, -7, 'Wasser nimmt auf', TIN, 24), T(2.0, 63, 'je 57.5 kJ', ROT, 28)])),
        sz('Gewichtet', 'Gleich viel Wasser von neunzig und von dreissig Grad gibt sechzig Grad, genau die Mitte. Doppelt so viel kaltes Wasser zieht die Mischung auf fünfzig Grad. Die Portion mit dem grösseren m mal c zieht die Temperatur zu sich.',
           formel(r'\vartheta_\text{m} = \frac{1\;\text{kg} \cdot 90\;^\circ\text{C} + 1\;\text{kg} \cdot 30\;^\circ\text{C}}{2\;\text{kg}} = 60\;^\circ\text{C}', y=300, g=32, a='gibt sechzig Grad'),
           formel(r'\vartheta_\text{m} = \frac{1\;\text{kg} \cdot 90\;^\circ\text{C} + 2\;\text{kg} \cdot 30\;^\circ\text{C}}{3\;\text{kg}} = 50\;^\circ\text{C}', y=440, g=32, a='auf fünfzig Grad'),
           notiz('grösseres @m \\cdot c@ zieht|die Mischung zu sich', y=580, a='Die Portion mit dem grösseren'),
           graf((-6, 110), (0, 10), achsen=False,
                strecken=zs_s + [S((30, 3.7), (30, 1.4), TIN, dicke=3, gestrichelt=True), S((90, 3.7), (90, 1.4), BER, dicke=3, gestrichelt=True)],
                flaechen=[F(rechteck(22, 5.2, 38, 6.4), TIN, 0.35), F(rechteck(82, 5.2, 98, 6.4), BER, 0.4),
                          F(rechteck(22, 6.6, 38, 7.8), TIN, 0.35, _ein='Doppelt so viel')],
                geraden=[{'bewegung': [[0, 0, 1.2]], 'farbe': TIN, 'dicke': 0.01,
                          'laeufer': {'_bahn': [['gibt sechzig Grad', 0, 60], ['auf fünfzig Grad', -1.3, 60], ['auf fünfzig Grad', 0, 50]], 'farbe': BER, '_ein': 'gibt sechzig Grad'}}],
                texte=zs_t + [T(30, 4.2, 'kalt: 30 °C', TIN, 26), T(90, 4.2, 'heiss: 90 °C', BER, 26), T(30, 8.4, '2 kg', TIN, 26, _ein='Doppelt so viel'),
                              T(60, 2.6, 'Mitte: 60 °C', BER, 26, _ein='gibt sechzig Grad', _aus='auf fünfzig Grad'),
                              T(50, 2.6, 'Mischung: 50 °C', BER, 26, _ein='auf fünfzig Grad')])),
        sz('Problem Aluminium', 'Jetzt ein ganzes Problem. Ein Aluminiumteil von null Komma zwei fünf Kilogramm kommt mit zweihundert Grad aus dem Ofen und wird in null Komma acht Kilogramm Wasser von fünfzehn Grad getaucht. Welche Temperatur stellt sich ein? Aluminium hat achthundertsechsundneunzig Joule pro Kilogramm und Kelvin; Gefäss und Umgebung nehmen nichts auf.',
           notiz('Aluminium: 0.25 kg, 200 °C', y=300, a='mit zweihundert Grad'),
           notiz('Wasser: 0.8 kg, 15 °C', y=360, a='Wasser von fünfzehn'),
           notiz('gesucht: Mischtemperatur @\\vartheta_\\text{m}@', y=470, a='Welche Temperatur', farbe='rot'),
           notiz(r'@c_\text{Al} = 896\;\text{J/(kg·K)}@', y=590, a='Aluminium hat'),
           notiz('ohne Verluste', y=670, a='Gefäss und Umgebung'),
           skizze(strecken=becher(2.0, 8.0, 1.5, 6.5, dicke=5) + umriss(4.2, 7.0, 5.8, 8.6, TIN, 4),
                  flaechen=[F(rechteck(2.1, 1.6, 7.9, 5.6), TIN, 0.12), F(rechteck(4.2, 7.0, 5.8, 8.6), TIN, 0.35)],
                  texte=[T(6.2, 7.8, 'Aluminium, 200 °C', BER, 26, 'start', _ein='mit zweihundert Grad'), T(5.0, 3.4, 'Wasser, 15 °C', TIN, 26, _ein='Wasser von fünfzehn')])),
        sz('Vorgehen Aluminium', 'Das Aluminium gibt Wärme ab, bis es die Mischtemperatur hat; das Wasser nimmt sie auf. Also Q ab gleich Q auf, jede Seite mit ihrem eigenen c und ihrer eigenen Temperaturänderung.',
           formel(r'Q_\text{ab} = Q_\text{auf}', y=300, g=50, a='Also Q ab'),
           formel(r'm_\text{A} c_\text{A} (200\;^\circ\text{C} - \vartheta_\text{m}) = m_\text{W} c_\text{W} (\vartheta_\text{m} - 15\;^\circ\text{C})', y=430, g=28, a='jede Seite'),
           skizze(strecken=becher(2.0, 8.0, 1.5, 6.5, dicke=5) + umriss(4.2, 2.0, 5.8, 3.6, TIN, 4)
                  + [P((5.9, 2.8), (7.3, 2.8), ROT, dicke=6, _ein='Das Aluminium gibt Wärme ab'), P((4.1, 2.8), (2.7, 2.8), ROT, dicke=6, _ein='Das Aluminium gibt Wärme ab')],
                  flaechen=[F(rechteck(2.1, 1.6, 7.9, 5.6), TIN, 0.12), F(rechteck(4.2, 2.0, 5.8, 3.6), TIN, 0.35)],
                  texte=[T(5.0, 4.2, 'Aluminium gibt ab', BER, 26, _ein='Das Aluminium gibt Wärme ab'), T(5.0, 6.0, 'Wasser nimmt auf', TIN, 26, _ein='das Wasser nimmt sie auf')])),
        sz('Lösung Aluminium', 'Aluminium: null Komma zwei fünf mal achthundertsechsundneunzig, zweihundertvierundzwanzig Joule pro Kelvin. Wasser: null Komma acht mal viertausendeinhundertzweiundachtzig, rund dreitausenddreihundertsechsundvierzig Joule pro Kelvin. Eingesetzt und aufgelöst: rund sechsundzwanzig Komma sechs Grad. Probe: Das Aluminium kühlt um hundertdreiundsiebzig Kelvin ab und gibt rund achtunddreissig Komma acht Kilojoule ab, das Wasser wird um knapp zwölf Kelvin wärmer und nimmt dieselben auf.',
           formel(r'm_\text{A} c_\text{A} = 0.25\;\text{kg} \cdot 896\;\tfrac{\text{J}}{\text{kg·K}} = 224\;\tfrac{\text{J}}{\text{K}}', y=280, g=32, a='zweihundertvierundzwanzig'),
           formel(r'm_\text{W} c_\text{W} = 0.8\;\text{kg} \cdot 4182\;\tfrac{\text{J}}{\text{kg·K}} \approx 3346\;\tfrac{\text{J}}{\text{K}}', y=370, g=32, a='rund dreitausenddreihundertsechsundvierzig'),
           formel(r'\vartheta_\text{m} = \frac{224\;\text{J/K} \cdot 200\;^\circ\text{C} + 3346\;\text{J/K} \cdot 15\;^\circ\text{C}}{3570\;\text{J/K}} \approx 26.6\;^\circ\text{C}', y=480, g=32, a='rund sechsundzwanzig Komma sechs'),
           notiz('Probe: je rund 38.8 kJ', y=620, g=40, a='rund achtunddreissig'),
           graf((-14, 230), (0, 10), achsen=False,
                strecken=za_s + [S((200, 6.6), (26.6, 6.6), BER, dicke=5, pfeil=True, _ein='Das Aluminium kühlt um'),
                                 S((15, 4.0), (26.6, 4.0), TIN, dicke=5, pfeil=True, _ein='das Wasser wird um knapp zwölf')],
                punkte=[{'x': 15, 'y': 1.2, 'farbe': TIN}, {'x': 200, 'y': 1.2, 'farbe': BER},
                        {'x': 26.6, 'y': 1.2, 'farbe': BER, '_ein': 'rund sechsundzwanzig Komma sechs'}],
                texte=za_t + [T(15, 2.3, '15 °C', TIN, 24), T(200, 2.3, '200 °C', BER, 24),
                              T(40, 2.6, 'Mischung ≈ 26.6 °C', BER, 26, 'start', _ein='rund sechsundzwanzig Komma sechs'),
                              T(113, 7.4, 'Aluminium: 173 K', BER, 26, _ein='Das Aluminium kühlt um'),
                              T(32, 4.0, 'Wasser: 11.6 K', TIN, 26, 'start', _ein='das Wasser wird um knapp zwölf')])),
        merke('Zum Mitnehmen: In der Wärmebilanz gibt der warme Körper so viel ab, wie der kalte aufnimmt. Die Mischtemperatur liegt dazwischen, näher bei dem mit dem grösseren m mal c.',
              r'Q_\text{ab} = Q_\text{auf}', 'Mischtemperatur: dazwischen,|näher beim grösseren @m \\cdot c@'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Aluminium', 'Welche Gleichung stellst du auf?', ['Mittelwert: (200 °C + 15 °C) / 2', 'Q_ab = Q_auf, jede Seite mit m · c · Temperaturänderung', 'Q_ab = Q_auf, beide Seiten mit c von Wasser'], 1,
                 {0: 'Der einfache Mittelwert gilt nur für gleiches m · c. Ist das hier so?', 2: 'Ist das Aluminiumteil aus Wasser?'},
                 sprich='Welche Gleichung stellst du auf?',
                 rueck_sprich={0: 'Der einfache Mittelwert gilt nur für gleiches m mal c. Ist das hier so?', 2: 'Ist das Aluminiumteil aus Wasser?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 2
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zur Wärmebilanz', dateiname='p5-2-lp-kontrolle-bilanz',
    kurzbeschrieb='Fünf Fragen zur Mischtemperatur gleicher und verschiedener Stoffe (Wasser, Nagel im Tee, Kupfer im Wasser), zum thermischen Gleichgewicht und zu den Verlusten im Versuch.',
    schlagworte=['Wärmebilanz', 'Mischtemperatur', 'thermisches Gleichgewicht', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Gleicher Stoff, also gewichtet mit der Masse: null Komma zwei mal siebzig plus null Komma sechs mal zehn, geteilt durch null Komma acht. Das gibt fünfundzwanzig Grad. Die dreimal grössere kalte Portion zieht die Mischung zu sich.',
           formel(r'\vartheta_\text{m} = \frac{0.2\;\text{kg} \cdot 70\;^\circ\text{C} + 0.6\;\text{kg} \cdot 10\;^\circ\text{C}}{0.8\;\text{kg}} = 25\;^\circ\text{C}', y=320, g=30, ein=1.0)),
        sz('Frage 2', 'Der Nagel hat nur rund zwei Komma drei Joule pro Kelvin, der Tee rund tausendsechsundvierzig. Die Mischung bleibt darum knapp über sechzig Grad, bei rund sechzig Komma fünf.',
           notiz(r'Nagel: @m \cdot c \approx 2.3\;\text{J/K}@|Tee: @m \cdot c \approx 1046\;\text{J/K}@', y=320, ein=1.0)),
        sz('Frage 3', 'Im thermischen Gleichgewicht haben beide dieselbe Temperatur. Ihre inneren Energien können ganz verschieden sein, und Wärme hat ein Körper nicht — sie fliesst nur.',
           notiz('Gleichgewicht:|dieselbe Temperatur', y=320, ein=1.0)),
        sz('Frage 4', 'Gewichtet wird mit m mal c. Das Kupfer hat nur hundertvierundfünfzig Joule pro Kelvin, das Wasser rund zweitausendfünfhundertneun. Die Mischung landet bei rund fünfundzwanzig Komma sechs Grad, nahe beim Wasser.',
           formel(r'\vartheta_\text{m} = \frac{154\;\text{J/K} \cdot 150\;^\circ\text{C} + 2509\;\text{J/K} \cdot 18\;^\circ\text{C}}{2663\;\text{J/K}} \approx 25.6\;^\circ\text{C}', y=320, g=30, ein=1.0)),
        sz('Frage 5', 'Gefäss, Thermometer und Umgebung nehmen einen Teil der Wärme auf. Dieser Teil fehlt in der Bilanz. Verschwunden ist er nicht, und Kälte fliesst nie.',
           notiz('Gefäss und Umgebung|nehmen Wärme auf', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', '0.2 kg Wasser von 70 °C und 0.6 kg Wasser von 10 °C werden gemischt. Welche Mischtemperatur?', ['40 °C', '55 °C', '25 °C'], 2,
             {0: 'Das ist der einfache Mittelwert. Gilt er auch bei verschiedenen Massen?', 1: 'Prüfe, welche Masse zu welcher Temperatur gehört.'},
             sprich='Null Komma zwei Kilogramm Wasser von siebzig Grad und null Komma sechs Kilogramm Wasser von zehn Grad werden gemischt. Welche Mischtemperatur?'),
        wahl('Frage 2', 'Ein heisser Nagel (5 g Eisen, 300 °C) fällt in eine Tasse Tee (0.25 kg, 60 °C). Wo liegt die Endtemperatur?', ['knapp über 60 °C', 'in der Mitte, bei 180 °C', 'knapp unter 300 °C'], 0,
             {1: 'Die Mitte gilt nur für gleiches m · c. Vergleiche m · c von Nagel und Tee.', 2: 'Welcher Körper hat das viel grössere m · c?'},
             sprich='Ein heisser Nagel, fünf Gramm Eisen von dreihundert Grad, fällt in eine Tasse Tee mit null Komma zwei fünf Kilogramm und sechzig Grad. Wo liegt die Endtemperatur?',
             rueck_sprich={1: 'Die Mitte gilt nur für gleiches m mal c. Vergleiche m mal c von Nagel und Tee.', 2: 'Welcher Körper hat das viel grössere m mal c?'}),
        wahl('Frage 3', 'Was gilt im thermischen Gleichgewicht?', ['Beide Körper haben dieselbe innere Energie.', 'Beide Körper haben dieselbe Temperatur.', 'Beide Körper enthalten gleich viel Wärme.'], 1,
             {0: 'Ein kleiner und ein grosser Körper — haben sie gleich viel Energie, wenn sie gleich warm sind?', 2: 'Enthält ein Körper überhaupt Wärme?'}),
        wahl('Frage 4', '0.4 kg Kupfer (c = 385 J/(kg·K)) von 150 °C kommen in 0.6 kg Wasser von 18 °C. Welche Temperatur stellt sich ein?', ['70.8 °C', '134 °C', '25.6 °C'], 2,
             {0: 'Du hast nur mit den Massen gewichtet. Haben Kupfer und Wasser dasselbe c?', 1: 'Prüfe, welches c zu welchem Körper gehört.'},
             sprich='Null Komma vier Kilogramm Kupfer mit dreihundertfünfundachtzig Joule pro Kilogramm und Kelvin kommen mit hundertfünfzig Grad in null Komma sechs Kilogramm Wasser von achtzehn Grad. Welche Temperatur stellt sich ein?'),
        wahl('Frage 5', 'Im Versuch misst du 2 K weniger, als die Bilanz ergibt. Woran liegt das?', ['Gefäss und Umgebung haben Wärme aufgenommen.', 'Ein Teil der Energie ist verschwunden.', 'Das kalte Wasser hat Kälte abgegeben.'], 0,
             {1: 'Energie verschwindet nicht. Wohin könnte sie gegangen sein?', 2: 'Es fliesst nur Wärme, und zwar vom wärmeren zum kälteren Körper.'},
             sprich='Im Versuch misst du zwei Kelvin weniger, als die Bilanz ergibt. Woran liegt das?'),
    ]))


# ================================================================== Kapitel 3: Latente Wärme und Heizkurve
q1, q2, q3 = 0.5 * 2100 * 10, 0.5 * 334000, 0.5 * 4182 * 80
t1, t2, t3 = q1 / 1200, q2 / 1200, q3 / 1200
assert abs((q1 + q2 + q3) - 344780) < 1e-6 and abs((t1 + t2 + t3) - 287.3167) < 1e-3
kE, kW = 600 / (0.25 * 2100) * 60, 600 / (0.25 * 4182) * 60          # K je min bei 0.25 kg und 600 W
assert abs(kE - 68.571) < 1e-3 and abs(kW - 34.433) < 1e-3
tE = 20 / kE; tS = tE + 0.25 * 334000 / 600 / 60; tW = tS + 100 / kW
DREH.append(dict(KOPF, titel='Wärme sehen: wenn die Temperatur stehen bleibt', dateiname='p5-2-lp-heizkurve',
    kurzbeschrieb='Latente Wärme beim Schmelzen und Verdampfen, die Heizkurve mit ihren waagrechten Stücken und Steigungen — und ein vorgerechnetes Problem: Schnee wird auf dem Gaskocher zu Teewasser.',
    schlagworte=['latente Wärme', 'Schmelzwärme', 'Verdampfungswärme', 'Heizkurve', 'Phasenwechsel'], _probe=EIN % 3,
    szenen=[
        sz('Eiswasser', 'In einem Glas Wasser schwimmen Eiswürfel. Das Glas steht im warmen Zimmer, und trotzdem zeigt das Thermometer null Grad, bis das letzte Eis geschmolzen ist. Wohin geht die Wärme aus dem Zimmer?',
           titel('Wohin geht die Wärme?', g=66),
           notiz('warmes Zimmer,|Thermometer: 0 °C', y=460, a='trotzdem zeigt'),
           skizze(strecken=becher(3.0, 7.0, 1.5, 7.2, dicke=5) + umriss(3.6, 4.9, 4.8, 6.0) + umriss(5.1, 4.6, 6.3, 5.7)
                  + [S((6.6, 2.0), (6.6, 7.8), TIN, dicke=8), P((1.0, 4.0), (2.7, 4.0), ROT, dicke=6, _ein='Wohin geht die Wärme'),
                     P((9.0, 4.0), (7.3, 4.0), ROT, dicke=6, _ein='Wohin geht die Wärme')],
                  flaechen=[F(rechteck(3.1, 1.6, 6.9, 6.2), TIN, 0.12), F(rechteck(3.6, 4.9, 4.8, 6.0), TIN, 0.08), F(rechteck(5.1, 4.6, 6.3, 5.7), TIN, 0.08)],
                  texte=[T(6.6, 8.3, '0 °C', BER, 32, _ein='trotzdem zeigt'), T(5.0, 8.9, 'Eis im Wasser', TIN, 26),
                         T(1.4, 3.3, 'Zimmer', ROT, 26, _ein='Wohin geht die Wärme')])),
        sz('Latente Wärme', 'Beim Schmelzen geht die zugeführte Energie nicht in die Bewegung der Teilchen, sondern in das Lösen ihres Verbands. Darum steigt die Temperatur nicht.',
           notiz('Energie löst den Teilchenverband:|Temperatur bleibt', y=300, a='Beim Schmelzen'),
           skizze(punkte=[{'x': 1.2 + 0.9 * i, 'y': 3.2 + 0.9 * j, 'farbe': TIN} for i in range(4) for j in range(4)]
                         + [dict({'x': x, 'y': y, 'farbe': TIN}, _ein='in das Lösen ihres Verbands') for x, y in
                            [(6.3, 3.3), (7.4, 3.6), (8.6, 3.2), (6.8, 4.5), (8.0, 4.7), (9.0, 4.2), (6.2, 5.6), (7.5, 5.9), (8.7, 5.5), (6.9, 6.7), (8.2, 6.9), (9.2, 6.4), (6.4, 7.5), (7.6, 7.9), (8.9, 7.6), (7.2, 3.0)]],
                  strecken=[P((4.5, 5.4), (5.7, 5.4), ROT, dicke=7, _ein='Beim Schmelzen')],
                  texte=[T(2.55, 2.3, 'Eis: fester Verband', TIN, 24), T(7.7, 2.3, 'Wasser: Verband gelöst', TIN, 24, _ein='in das Lösen ihres Verbands'),
                         T(5.1, 6.0, 'Energie', ROT, 24, _ein='Beim Schmelzen'),
                         T(2.55, 7.0, '0 °C', BER, 30), T(7.7, 8.7, '0 °C', BER, 30, _ein='Darum steigt')])),
        sz('Schmelzwärme', 'Diese Wärme heisst latente Wärme: Q gleich m mal L. Wasser braucht zum Schmelzen dreihundertvierunddreissig Kilojoule pro Kilogramm, zum Verdampfen zweitausendzweihundertsechsundfünfzig — fast siebenmal so viel.',
           formel(r'Q = m \cdot L_\text{f} \qquad Q = m \cdot L_\text{v}', y=300, g=44, a='Q gleich m mal L'),
           notiz('latente Wärme:|Schmelzen und Verdampfen', y=430, a='Diese Wärme heisst'),
           graf((-0.6, 4.4), (-300, 2700), [], [500, 1000, 1500, 2000, 2500], '', 'L [kJ/kg]', a='Wasser braucht zum Schmelzen',
                flaechen=[F(rechteck(0.6, 0, 1.6, 334), ROT, 0.5), F(rechteck(2.6, 0, 3.6, 2256), ROT, 0.5, _ein='zum Verdampfen')],
                texte=[T(1.1, -150, 'Schmelzen', TIN, 26), T(3.1, -150, 'Verdampfen', TIN, 26),
                       T(1.1, 450, '334', ROT, 30), T(3.1, 2370, '2256', ROT, 30, _ein='zum Verdampfen'),
                       T(1.1, 1100, 'fast 7-mal', ROT, 30, _ein='fast siebenmal')])),
        sz('Heizkurve', 'Heizt eine Platte gleichmässig, entsteht die Heizkurve. Das Eis wird wärmer, bei null Grad schmilzt es, dann wird das Wasser wärmer, und bei hundert Grad siedet es. Wo die Kurve waagrecht ist, wechselt der Stoff seine Phase.',
           notiz('0.25 kg Eis von −20 °C,|Platte: 600 W', y=300, a='Heizt eine Platte'),
           notiz('waagrecht:|Phasenwechsel', y=470, a='Wo die Kurve waagrecht', farbe='rot'),
           bild('p5-2-lp-heizkurve-a.jpg', a='Das Eis wird wärmer'),
           bild('p5-2-lp-heizkurve-b.jpg', a='bei null Grad schmilzt'),
           bild('p5-2-lp-heizkurve-c.jpg', a='dann wird das Wasser wärmer'),
           bild('p5-2-lp-heizkurve-d.jpg', a='bei hundert Grad siedet'),
           bild('p5-2-lp-heizkurve-e.jpg', a='Wo die Kurve waagrecht')),
        sz('Steigung', 'Eis steigt doppelt so steil wie Wasser: Bei gleicher Leistung und Masse wird es je Minute rund neunundsechzig Kelvin wärmer, das Wasser nur rund vierunddreissig. Der Grund: c von Eis ist mit zweitausendeinhundert Joule pro Kilogramm und Kelvin nur halb so gross. Die waagrechten Stücke dauern t gleich m mal L durch P.',
           notiz('Eis: rund 69 K/min', y=300, a='je Minute rund neunundsechzig'),
           notiz('Wasser: rund 34 K/min', y=360, a='vierunddreissig. Der'),
           formel(r'c_\text{Eis} = 2100\;\tfrac{\text{J}}{\text{kg·K}}', y=450, g=40, a='Der Grund'),
           formel(r't = \frac{m \cdot L}{P}', y=570, g=48, a='Die waagrechten Stücke'),
           graf((-0.8, 6.4), (-34, 112), [1, 2, 3, 4, 5, 6], [-20, 20, 40, 60, 80, 100], 't [min]', 'ϑ [°C]', ya=-34,
                strecken=[S((0, -20), (tE, 0), BER, dicke=5), S((tE, 0), (tS, 0), BER, dicke=5), S((tS, 0), (tW, 100), BER, dicke=5), S((tW, 100), (6.3, 100), BER, dicke=5),
                          S((tS + 1, kW), (tS + 2, kW), BER, dicke=3, gestrichelt=True, _ein='vierunddreissig. Der'), S((tS + 2, kW), (tS + 2, 2 * kW), BER, dicke=3, gestrichelt=True, _ein='vierunddreissig. Der')],
                texte=[T(0.45, -14, 'Eis: 20 K in 0.29 min ≈ 69 K/min', BER, 24, 'start', _ein='je Minute rund neunundsechzig'),
                       T(tS + 1.5, kW - 9, '1 min', BER, 24, _ein='vierunddreissig. Der'),
                       T(tS + 2.12, 1.5 * kW, '34 K', BER, 24, 'start', _ein='vierunddreissig. Der'),
                       T(tS + 1.25, 1.5 * kW + 6, 'Wasser', BER, 24, 'end', _ein='vierunddreissig. Der'),
                       T((tE + tS) / 2, 8, 'm · L / P', TIN, 26, _ein='Die waagrechten Stücke')])),
        sz('Problem Schnee', 'Jetzt ein ganzes Problem. Auf einem Gaskocher sollen null Komma fünf Kilogramm Schnee von minus zehn Grad zu Teewasser von achtzig Grad werden. Der Kocher gibt dem Topfinhalt zwölfhundert Watt ab. Wie lange dauert das?',
           notiz('0.5 kg Schnee, −10 °C', y=300, a='von minus zehn Grad zu'),
           notiz('bis Wasser von 80 °C', y=360, a='von achtzig Grad werden'),
           notiz('Kocher: 1200 W an den Inhalt', y=420, a='zwölfhundert Watt ab'),
           notiz('gesucht: Zeit @t@', y=540, a='Wie lange', farbe='rot'),
           skizze(strecken=becher(2.6, 7.4, 3.2, 6.6, dicke=6) + [S((3.4, 2.8), (6.6, 2.8), TIN, dicke=8)]
                  + [P((4.2, 1.6), (4.2, 2.6), ROT, dicke=5), P((5.0, 1.4), (5.0, 2.6), ROT, dicke=5), P((5.8, 1.6), (5.8, 2.6), ROT, dicke=5)],
                  flaechen=[F([(2.7, 3.3), (7.3, 3.3), (7.3, 4.6), (6.0, 5.3), (4.2, 5.1), (2.7, 4.7)], TIN, 0.1)],
                  texte=[T(5.0, 4.1, 'Schnee, −10 °C', TIN, 26, _ein='von minus zehn Grad zu'), T(5.0, 0.8, 'Kocher: 1200 W', ROT, 26, _ein='zwölfhundert Watt ab'), T(5.0, 7.4, 'Ziel: Wasser, 80 °C', BER, 26, _ein='von achtzig Grad werden')])),
        sz('Vorgehen Schnee', 'Über die Phasengrenze rechnet man abschnittsweise: zuerst das Eis von minus zehn auf null Grad erwärmen, dann schmelzen, dann das Wasser von null auf achtzig Grad erwärmen. Am Schluss die Wärmen addieren und durch die Leistung teilen.',
           formel(r'Q = Q_1 + Q_2 + Q_3', y=320, g=50, a='Am Schluss'),
           formel(r't = \frac{Q}{P}', y=450, g=50, a='durch die Leistung'),
           graf((-0.12, 1.08), (-34, 112), [], [-10, 0, 20, 40, 60, 80, 100], 't [s]', 'ϑ [°C]', ya=-34,
                strecken=[S((0, -10), (0.08, 0), BER, dicke=5, _ein='zuerst das Eis'), S((0.08, 0), (0.5, 0), BER, dicke=5, _ein='dann schmelzen'),
                          S((0.5, 0), (0.95, 80), BER, dicke=5, _ein='dann das Wasser von null')],
                texte=[T(0.12, -20, '1: Eis erwärmen', BER, 24, 'start', _ein='zuerst das Eis'), T(0.29, 8, '2: schmelzen', BER, 24, _ein='dann schmelzen'),
                       T(0.7, 30, '3: Wasser erwärmen', BER, 24, 'start', _ein='dann das Wasser von null')])),
        sz('Lösung Schnee', 'Eis erwärmen: null Komma fünf mal zweitausendeinhundert mal zehn, zehn Komma fünf Kilojoule. Schmelzen: null Komma fünf mal dreihundertvierunddreissig, hundertsiebenundsechzig Kilojoule. Wasser erwärmen: null Komma fünf mal viertausendeinhundertzweiundachtzig mal achtzig, rund hundertsiebenundsechzig Komma drei Kilojoule. Zusammen rund dreihundertvierundvierzig Komma acht Kilojoule. Geteilt durch zwölfhundert Watt sind das rund zweihundertsiebenundachtzig Sekunden, knapp fünf Minuten. Probe: Joule durch Watt gibt Sekunden, und das Schmelzen kostet fast die Hälfte.',
           formel(r'Q_1 = 0.5\;\text{kg} \cdot 2100\;\tfrac{\text{J}}{\text{kg·K}} \cdot 10\;\text{K} = 10.5\;\text{kJ}', y=250, g=30, a='zehn Komma fünf Kilojoule'),
           formel(r'Q_2 = 0.5\;\text{kg} \cdot 334\;\tfrac{\text{kJ}}{\text{kg}} = 167\;\text{kJ}', y=320, g=30, a='hundertsiebenundsechzig Kilojoule'),
           formel(r'Q_3 = 0.5\;\text{kg} \cdot 4182\;\tfrac{\text{J}}{\text{kg·K}} \cdot 80\;\text{K} \approx 167.3\;\text{kJ}', y=390, g=30, a='rund hundertsiebenundsechzig Komma drei'),
           formel(r'Q = Q_1 + Q_2 + Q_3 \approx 344.8\;\text{kJ}', y=460, g=32, a='Zusammen'),
           formel(r't = \frac{Q}{P} = \frac{344.8\;\text{kJ}}{1200\;\text{W}} \approx 287\;\text{s} \approx 4.8\;\text{min}', y=545, g=32, a='rund zweihundertsiebenundachtzig'),
           notiz('Probe: J / W = s', y=640, g=34, a='Probe'),
           notiz('Schmelzen: fast die Hälfte', y=690, g=34, a='fast die Hälfte'),
           graf((-30, 315), (-34, 112), [50, 100, 150, 200, 250, 300], [-10, 20, 40, 60, 80, 100], 't [s]', 'ϑ [°C]', ya=-34, a='Eis erwärmen',
                strecken=[S((0, -10), (t1, 0), BER, dicke=5), S((t1, 0), (t1 + t2, 0), BER, dicke=5, _ein='Schmelzen:'),
                          S((t1 + t2, 0), (t1 + t2 + t3, 80), BER, dicke=5, _ein='rund hundertsiebenundsechzig Komma drei'),
                          S((t1 + t2 + t3, -34), (t1 + t2 + t3, 80), TIN, dicke=3, gestrichelt=True, _ein='rund zweihundertsiebenundachtzig')],
                texte=[T(12, -22, '10.5 kJ', ROT, 24, 'start', _ein='zehn Komma fünf Kilojoule'), T((t1 + t1 + t2) / 2, 8, '167 kJ', ROT, 26, _ein='hundertsiebenundsechzig Kilojoule'),
                       T(205, 26, '167.3 kJ', ROT, 26, 'start', _ein='rund hundertsiebenundsechzig Komma drei'),
                       T(282, 92, '287 s', TIN, 26, 'end', _ein='rund zweihundertsiebenundachtzig')])),
        merke('Zum Mitnehmen: Beim Schmelzen und Sieden bleibt die Temperatur stehen; die latente Wärme Q gleich m mal L löst den Teilchenverband. Über eine Phasengrenze rechnet man abschnittsweise.',
              r'Q = m \cdot L', 'waagrecht: Phasenwechsel|abschnittsweise rechnen'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Schnee', 'Welche Abschnitte rechnest du?', ['einen: Q = m · c · ΔT von −10 °C bis 80 °C', 'zwei: schmelzen und Wasser erwärmen', 'drei: Eis erwärmen, schmelzen, Wasser erwärmen'], 2,
                 {0: 'Gilt ein einziges c über die Phasengrenze hinweg? Was geschieht bei 0 °C?', 1: 'Bei welcher Temperatur beginnt der Schnee?'},
                 sprich='Welche Abschnitte rechnest du?',
                 rueck_sprich={0: 'Gilt ein einziges c über die Phasengrenze hinweg? Was geschieht bei null Grad?', 1: 'Bei welcher Temperatur beginnt der Schnee?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 3
HK = [((0, -20), (0.4, 0)), ((0.4, 0), (3.6, 0)), ((3.6, 0), (7.6, 100)), ((7.6, 100), (20, 100))]   # Eis 50 K/min, Wasser 25 K/min; Plateau 334/418.2 · 4 min ≈ 3.2 min
assert abs(334000 / (4182 * 100) * 4 - 3.2) < 0.01
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zu latenter Wärme und Heizkurve', dateiname='p5-2-lp-kontrolle-heizkurve',
    kurzbeschrieb='Fünf Fragen: das Sieden in der Heizkurve, die Verdampfungswärme, Eis gegen kaltes Wasser, das Erstarren und Erwärmen gegen Schmelzen.',
    schlagworte=['latente Wärme', 'Heizkurve', 'Schmelzen', 'Verdampfen', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'Bei D ist die Kurve waagrecht bei hundert Grad: Dort siedet das Wasser. B ist das Schmelzen bei null Grad, A und C sind Erwärmen.',
           notiz('waagrecht bei 100 °C:|Sieden', y=320, ein=1.0),
           graf((-2, 21), (-34, 112), [5, 10, 15, 20], [-20, 20, 40, 60, 80, 100], 't [min]', 'ϑ [°C]', ya=-34,
                strecken=[S(a, b, BER, dicke=5) for a, b in HK],
                texte=[T(0.8, -14, 'A', TIN, 32, 'start'), T(2.0, 9, 'B', TIN, 32), T(5.2, 56, 'C', TIN, 32, 'end'), T(14, 107, 'D', TIN, 32)])),
        sz('Frage 2', 'Beim Verdampfen gilt die Verdampfungswärme: null Komma eins fünf Kilogramm mal zweitausendzweihundertsechsundfünfzig Kilojoule pro Kilogramm, rund dreihundertachtunddreissig Kilojoule. Die Temperatur bleibt dabei bei hundert Grad.',
           formel(r'Q = m \cdot L_\text{v} = 0.15\;\text{kg} \cdot 2256\;\tfrac{\text{kJ}}{\text{kg}} \approx 338\;\text{kJ}', y=320, g=34, ein=1.0)),
        sz('Frage 3', 'Beide nehmen Wärme aus dem Getränk auf, bis sie gleich warm sind. Das Eis braucht vorher noch die Schmelzwärme: null Komma null fünf mal dreihundertvierunddreissig, rund sechzehn Komma sieben Kilojoule, ohne wärmer zu werden.',
           formel(r'Q = m \cdot L_\text{f} = 0.05\;\text{kg} \cdot 334\;\tfrac{\text{kJ}}{\text{kg}} = 16.7\;\text{kJ}', y=320, g=34, ein=1.0)),
        sz('Frage 4', 'Beim Erstarren wird dieselbe Energie frei, die das Schmelzen gekostet hat: null Komma fünf Kilogramm mal dreihundertvierunddreissig Kilojoule pro Kilogramm, hundertsiebenundsechzig Kilojoule, die das Wasser an den Tiefkühler abgibt, bei gleichbleibenden null Grad.',
           notiz('Erstarren:|Schmelzwärme wird frei', y=320, ein=1.0),
           formel(r'Q = m \cdot L_\text{f} = 0.5\;\text{kg} \cdot 334\;\tfrac{\text{kJ}}{\text{kg}} = 167\;\text{kJ}', y=470, g=32, ein=1.0)),
        sz('Frage 5', 'Erwärmen: null Komma drei mal zweitausendeinhundert mal acht, rund fünf Kilojoule. Schmelzen: null Komma drei mal dreihundertvierunddreissig, rund hundert Kilojoule — rund zwanzigmal so viel.',
           formel(r'Q_\text{erw} = 0.3\;\text{kg} \cdot 2100\;\tfrac{\text{J}}{\text{kg·K}} \cdot 8\;\text{K} \approx 5.0\;\text{kJ}', y=290, g=30, ein=1.0),
           formel(r'Q_\text{schm} = 0.3\;\text{kg} \cdot 334\;\tfrac{\text{kJ}}{\text{kg}} \approx 100\;\text{kJ}', y=390, g=30, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Das ist die Heizkurve von Eis auf einer Platte. In welchem Abschnitt siedet das Wasser?', ['A', 'B', 'C', 'D'], 3,
             {0: 'Steigt in diesem Abschnitt die Temperatur?', 1: 'Bei welcher Temperatur liegt dieses waagrechte Stück?', 2: 'Siedet Wasser, während seine Temperatur steigt?'}),
        wahl('Frage 2', 'Wie viel Wärme braucht es, um 0.15 kg Wasser von 100 °C ganz zu verdampfen?', ['50.1 kJ', '62.7 kJ', '338 kJ'], 2,
             {0: 'Das ist die Schmelzwärme. Welches L gilt beim Verdampfen?', 1: 'Das wäre Erwärmen um 100 K. Ändert sich beim Verdampfen die Temperatur?'},
             sprich='Wie viel Wärme braucht es, um null Komma eins fünf Kilogramm Wasser von hundert Grad ganz zu verdampfen?',
             rueck_sprich={0: 'Das ist die Schmelzwärme. Welches L gilt beim Verdampfen?', 1: 'Das wäre Erwärmen um hundert Kelvin. Ändert sich beim Verdampfen die Temperatur?'}),
        wahl('Frage 3', 'Was kühlt ein Getränk stärker: 50 g Eis von 0 °C oder 50 g Wasser von 0 °C?', ['Beide kühlen gleich stark.', 'Das Eis kühlt stärker.', 'Das Wasser kühlt stärker.'], 1,
             {0: 'Beide haben 0 °C — aber muss mit dem Eis vorher noch etwas geschehen?', 2: 'Was braucht das Eis zusätzlich, bevor es wärmer wird?'},
             sprich='Was kühlt ein Getränk stärker: fünfzig Gramm Eis von null Grad oder fünfzig Gramm Wasser von null Grad?',
             rueck_sprich={0: 'Beide haben null Grad — aber muss mit dem Eis vorher noch etwas geschehen?', 2: 'Was braucht das Eis zusätzlich, bevor es wärmer wird?'}),
        wahl('Frage 4', '0.5 kg Wasser von 0 °C gefrieren im Tiefkühler ganz zu Eis. Was geschieht mit der Energie?', ['Das Wasser gibt 167 kJ ab.', 'Das Wasser nimmt 167 kJ auf.', 'Es fliesst keine Energie, die Temperatur bleibt ja gleich.'], 0,
             {1: 'Schmelzen kostet Energie. Was geschieht auf dem Rückweg?', 2: 'Auch ohne Temperaturänderung kann Energie fliessen. Denk an das Schmelzen.'},
             sprich='Null Komma fünf Kilogramm Wasser von null Grad gefrieren im Tiefkühler ganz zu Eis. Was geschieht mit der Energie?',
             rueck_sprich={1: 'Schmelzen kostet Energie. Was geschieht auf dem Rückweg?', 2: 'Auch ohne Temperaturänderung kann Energie fliessen. Denk an das Schmelzen.'}),
        wahl('Frage 5', '0.3 kg Eis von −8 °C: Was kostet mehr Wärme — das Erwärmen bis 0 °C oder das Schmelzen?', ['Das Erwärmen: Es muss zuerst 8 K wärmer werden.', 'Beide kosten gleich viel.', 'Das Schmelzen, rund zwanzigmal so viel.'], 2,
             {0: 'Rechne beide aus: m · c · ΔT gegen m · L.', 1: 'Rechne beide aus: m · c · ΔT gegen m · L.'},
             sprich='Null Komma drei Kilogramm Eis von minus acht Grad: Was kostet mehr Wärme — das Erwärmen bis null Grad oder das Schmelzen?',
             rueck_sprich={0: 'Rechne beide aus: m mal c mal Delta T gegen m mal L.', 1: 'Rechne beide aus: m mal c mal Delta T gegen m mal L.'}),
    ]))


# ================================================================== Kapitel 4: Heizwert und Wirkungsgrad
mP = 2800 * 3.6 / (0.88 * 17.0)
assert abs(mP - 673.797) < 1e-3
QZ, QN = mP * 17.0, 2800 * 3.6


def balken_h(werte, xmax, xt, a=None, **kw):
    """waagrechte Balken (Fenster x 0…xmax, y 0…10): werte = [(Name, Wert, Farbe, _ein)]"""
    fl, tx = [], []
    for i, (n, w, f, e) in enumerate(werte):
        y = 8.2 - i * 2.6
        d = {'_ein': e} if e else {}
        fl.append(F(rechteck(0, y - 0.8, w, y + 0.8), f, 0.55, **d))
        tx.append(T(-0.02 * xmax, y - 0.3, n, TIN, 26, 'end', **d))
        tx.append(T(w + 0.02 * xmax, y - 0.3, ('%g' % w) if not isinstance(w, float) or w == int(w) else '%.0f' % w, f, 26, 'start', **d))
    return fl, tx


hfl, htx = balken_h([('Heizöl', 42.6, ORA, 'Heizöl liefert'), ('Erdgas', 50.0, ORA, 'Erdgas fünfzig'), ('Holzpellets', 17.0, ORA, 'Holzpellets siebzehn')], 58, 10)
for t_ in htx:
    if t_['text'] in ('43', '50', '17'):
        t_['text'] = {'43': '42.6 MJ/kg', '50': '50.0 MJ/kg', '17': '17.0 MJ/kg'}[t_['text']]
DREH.append(dict(KOPF, titel='Wärme sehen: vom Brennstoff zur Nutzwärme', dateiname='p5-2-lp-heizwert',
    kurzbeschrieb='Der Heizwert macht aus einer Brennstoffmenge eine Energie, der Wirkungsgrad sagt, wie viel davon als Nutzwärme ankommt — mit Strom wie mit Brennstoff. Vorgerechnet: Wie viel Holzpellets ein Haus im Januar braucht.',
    schlagworte=['Heizwert', 'Wirkungsgrad', 'Brennstoff', 'Nutzwärme', 'Heizzeit'], _probe=EIN % 4,
    szenen=[
        sz('Pellets', 'In einem Kessel verbrennen Holzpellets, kleine Holzstäbchen. Wie viel Wärme steckt in einem Kilogramm davon, und wie viel kommt im Boiler an?',
           titel('Was steckt im Brennstoff?', g=62),
           notiz('verbrannt wird Holz:|wie viel kommt an?', y=460, a='und wie viel kommt'),
           bild('p5-2-lp-heizwert-pellets.jpg')),
        sz('Heizwert', 'Der Heizwert H sagt, wie viel Energie beim Verbrennen von einem Kilogramm frei wird. Heizöl liefert zweiundvierzig Komma sechs Megajoule, Erdgas fünfzig, Holzpellets siebzehn. Mal die Masse ergibt das die zugeführte Energie: Q zu gleich m mal H.',
           notiz('Heizwert @H@: Energie je kg|in MJ/kg', y=300, a='Der Heizwert H'),
           formel(r'Q_\text{zu} = m \cdot H', y=460, g=54, a='Mal die Masse'),
           graf((-24, 76), (0, 10), achsen=False, a='Heizöl liefert', flaechen=hfl, texte=htx + [T(26, 1.0, 'Heizwert je Kilogramm', TIN, 26)])),
        sz('Wirkungsgrad', 'Nicht alles kommt im Wasser an: Ein Teil geht mit dem heissen Abgas durch den Kamin. Nutzbar ist der Anteil Eta: Q nutz gleich Eta mal m mal H. Hier verbrennen null Komma acht Kilogramm Erdgas mit einem Wirkungsgrad von null Komma neun: Von vierzig Megajoule kommen sechsunddreissig im Boiler an.',
           formel(r'Q_\text{nutz} = \eta \cdot m \cdot H', y=290, g=50, a='Q nutz gleich'),
           notiz('0.8 kg Erdgas, @\\eta = 0.9@', y=420, a='Wirkungsgrad von null'),
           notiz('40 MJ zugeführt', y=500, a='sechsunddreissig im'),
           notiz('36 MJ genutzt', y=560, a='sechsunddreissig im'),
           bild('p5-2-lp-heizwert-a-leer.jpg'),
           bild('p5-2-lp-heizwert-a.jpg', a='Wirkungsgrad von null'),
           bild('p5-2-lp-heizwert-c.jpg', a='sechsunddreissig im')),
        sz('Strom', 'Mit Strom ist die zugeführte Energie Leistung mal Zeit. Der Heizstab macht aus dem Strom fast ganz Wärme, aber der Boiler gibt einen Teil an die Umgebung ab. Für hundert Kilojoule Nutzwärme braucht ein Boiler mit dem Wirkungsgrad null Komma neun rund hundertelf Kilojoule Strom. Die Zeit ist darum t gleich Q nutz durch Eta mal P: Der Wirkungsgrad steht im Nenner.',
           formel(r'E_\text{zu} = P \cdot t', y=290, g=50, a='Mit Strom'),
           formel(r't = \frac{Q_\text{nutz}}{\eta \cdot P}', y=440, g=50, a='Die Zeit ist darum'),
           notiz('Verluste: mehr Strom,|mehr Zeit', y=580, a='Der Wirkungsgrad steht im Nenner', farbe='rot'),
           graf((-45, 135), (0, 10), achsen=False,
                flaechen=[F(rechteck(0, 7.4, 111.1, 9.0), ORA, 0.55, _ein='rund hundertelf'), F(rechteck(0, 4.8, 100, 6.4), GRU, 0.55, _ein='Für hundert Kilojoule'), F(rechteck(0, 2.2, 11.1, 3.8), ROT, 0.55, _ein='rund hundertelf')],
                texte=[T(-2, 7.9, 'Strom', TIN, 26, 'end'), T(-2, 5.3, 'Nutzwärme', TIN, 26, 'end'), T(-2, 2.7, 'Verlust', TIN, 26, 'end'),
                       T(113, 7.9, '111 kJ', ORA, 26, 'start', _ein='rund hundertelf'), T(102, 5.3, '100 kJ', GRU, 26, 'start', _ein='Für hundert Kilojoule'), T(13, 2.7, '11 kJ', ROT, 26, 'start', _ein='rund hundertelf'),
                       T(0, 0.8, 'Boiler mit Heizstab', TIN, 26, 'start'), T(70, 0.8, 'η = 0.9', TIN, 26, 'start', _ein='Wirkungsgrad null Komma neun')])),
        sz('Problem Pellets', 'Jetzt ein ganzes Problem. Ein Haus braucht im Januar zweitausendachthundert Kilowattstunden Wärme. Der Pelletofen hat einen Wirkungsgrad von null Komma acht acht, und Holzpellets liefern siebzehn Megajoule pro Kilogramm. Wie viele Kilogramm Holzpellets verbrennt er?',
           notiz('Wärme im Januar: 2800 kWh', y=300, a='zweitausendachthundert Kilowattstunden'),
           notiz(r'@\eta = 0.88@', y=360, a='null Komma acht acht'),
           notiz(r'Holzpellets: @H = 17.0\;\text{MJ/kg}@', y=420, a='siebzehn Megajoule'),
           notiz('gesucht: Masse @m@', y=540, a='Wie viele Kilogramm', farbe='rot'),
           skizze(strecken=[S((1.5, 1.5), (8.5, 1.5), TIN, dicke=5), S((1.5, 1.5), (1.5, 6), TIN, dicke=5), S((8.5, 1.5), (8.5, 6), TIN, dicke=5),
                            S((1.0, 5.6), (5, 8.8), TIN, dicke=5), S((5, 8.8), (9.0, 5.6), TIN, dicke=5)] + umriss(3.8, 1.6, 6.2, 4.4, TIN, 4),
                  flaechen=[F(rechteck(3.8, 1.6, 6.2, 4.4), ORA, 0.25)],
                  texte=[T(5, 3.0, 'Pelletofen', TIN, 26), T(5, 6.3, '2800 kWh', ROT, 30, _ein='zweitausendachthundert Kilowattstunden')])),
        sz('Vorgehen Pellets', 'Zuerst die Kilowattstunden in Megajoule umrechnen. Dann umstellen: m gleich Q nutz durch Eta mal H. Der Wirkungsgrad steht im Nenner, weil wegen der Verluste mehr Brennstoff nötig ist, als die Nutzwärme allein verlangt.',
           formel(r'1\;\text{kWh} = 3.6\;\text{MJ}', y=300, g=46, a='Zuerst die Kilowattstunden'),
           formel(r'm = \frac{Q_\text{nutz}}{\eta \cdot H}', y=440, g=50, a='Dann umstellen'),
           graf((-40, 125), (0, 10), achsen=False, a='weil wegen der Verluste',
                flaechen=[F(rechteck(0, 6.2, 113.6, 7.8), ORA, 0.55), F(rechteck(0, 3.4, 100, 5.0), GRU, 0.55)],
                texte=[T(-2, 6.7, 'Brennstoff', TIN, 26, 'end'), T(-2, 3.9, 'Nutzwärme', TIN, 26, 'end'), T(57, 1.4, 'Brennstoff = Nutzwärme / 0.88', TIN, 26)])),
        sz('Lösung Pellets', 'Q nutz: zweitausendachthundert mal drei Komma sechs, zehntausendachtzig Megajoule. Masse: zehntausendachtzig durch null Komma acht acht mal siebzehn, rund sechshundertvierundsiebzig Kilogramm. Probe: Sechshundertvierundsiebzig Kilogramm liefern rund elftausendvierhundertsechzig Megajoule, davon achtundachtzig Prozent sind wieder rund zehntausendachtzig. Ohne Verluste wären es nur rund fünfhundertdreiundneunzig Kilogramm.',
           formel(r'Q_\text{nutz} = 2800\;\text{kWh} \cdot 3.6\;\tfrac{\text{MJ}}{\text{kWh}} = 10\,080\;\text{MJ}', y=280, g=32, a='zehntausendachtzig Megajoule'),
           formel(r'm = \frac{10\,080\;\text{MJ}}{0.88 \cdot 17.0\;\tfrac{\text{MJ}}{\text{kg}}} \approx 674\;\text{kg}', y=400, g=36, a='rund sechshundertvierundsiebzig'),
           notiz('Probe: 674 kg · 17.0 MJ/kg ≈ 11 460 MJ', y=520, g=34, a='rund elftausend'),
           notiz('davon 88 %: rund 10 080 MJ', y=575, g=34, a='davon achtundachtzig'),
           notiz('ohne Verluste: rund 593 kg', y=650, g=34, a='Ohne Verluste'),
           graf((-4000, 16000), (0, 10), achsen=False, a='Q nutz:',
                flaechen=[F(rechteck(0, 4.8, QN, 6.4), GRU, 0.55, _ein='zehntausendachtzig Megajoule'), F(rechteck(0, 7.4, QZ, 9.0), ORA, 0.55, _ein='rund elftausend'), F(rechteck(0, 2.2, QZ - QN, 3.8), ROT, 0.55, _ein='davon achtundachtzig')],
                texte=[T(-200, 5.3, 'Nutzwärme', TIN, 26, 'end', _ein='zehntausendachtzig Megajoule'), T(QN + 200, 5.3, '10 080 MJ', GRU, 26, 'start', _ein='zehntausendachtzig Megajoule'),
                       T(-200, 7.9, 'Pellets', TIN, 26, 'end', _ein='rund elftausend'), T(QZ + 200, 7.9, '≈ 11 460 MJ', ORA, 26, 'start', _ein='rund elftausend'),
                       T(-200, 2.7, 'Verlust', TIN, 26, 'end', _ein='davon achtundachtzig')])),
        merke('Zum Mitnehmen: Der Heizwert macht aus einer Menge Brennstoff eine Energie. Nutzbar ist der Anteil Eta. Ist die Menge gesucht, steht Eta im Nenner.',
              r'Q_\text{nutz} = \eta \cdot m \cdot H', 'Menge gesucht:|@\\eta@ im Nenner'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Pellets', 'Wo steht der Wirkungsgrad, wenn die Brennstoffmenge gesucht ist?', ['im Zähler: m = η · Q_nutz / H', 'gar nicht: m = Q_nutz / H', 'im Nenner: m = Q_nutz / (η · H)'], 2,
                 {0: 'Braucht ein Ofen mit Verlusten mehr oder weniger Brennstoff als einer ohne?', 1: 'Kommt die ganze Energie des Brennstoffs als Nutzwärme an?'},
                 sprich='Wo steht der Wirkungsgrad, wenn die Brennstoffmenge gesucht ist?', kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 4
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zu Heizwert und Wirkungsgrad', dateiname='p5-2-lp-kontrolle-heizwert',
    kurzbeschrieb='Fünf Fragen: Nutzwärme aus Holz, Megajoule und Kilowattstunden, die Heizzeit eines Wasserkochers, wohin der Verlust geht und Heizöl in Litern.',
    schlagworte=['Heizwert', 'Wirkungsgrad', 'Heizzeit', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Q nutz gleich Eta mal m mal H: null Komma sieben fünf mal zwei Kilogramm mal fünfzehn Megajoule pro Kilogramm, zweiundzwanzig Komma fünf Megajoule.',
           formel(r'Q_\text{nutz} = \eta \cdot m \cdot H = 0.75 \cdot 2\;\text{kg} \cdot 15\;\tfrac{\text{MJ}}{\text{kg}} = 22.5\;\text{MJ}', y=320, g=30, ein=1.0)),
        sz('Frage 2', 'Eine Kilowattstunde sind drei Komma sechs Megajoule. Vierundfünfzig Megajoule geteilt durch drei Komma sechs: fünfzehn Kilowattstunden.',
           formel(r'\frac{54\;\text{MJ}}{3.6\;\tfrac{\text{MJ}}{\text{kWh}}} = 15\;\text{kWh}', y=320, g=44, ein=1.0)),
        sz('Frage 3', 'Zuerst die Wärme: eins Komma zwei mal viertausendeinhundertzweiundachtzig mal achtzig, rund vierhunderteins Kilojoule. Dann t gleich Q nutz durch Eta mal P: rund zweihunderteinundfünfzig Sekunden, also rund vier Komma zwei Minuten.',
           formel(r'Q_\text{nutz} = 1.2\;\text{kg} \cdot 4182\;\tfrac{\text{J}}{\text{kg·K}} \cdot 80\;\text{K} \approx 401\;\text{kJ}', y=280, g=30, ein=1.0),
           formel(r't = \frac{Q_\text{nutz}}{\eta \cdot P} = \frac{401\,472\;\text{J}}{0.8 \cdot 2000\;\text{W}} \approx 251\;\text{s} \approx 4.2\;\text{min}', y=400, g=30, ein=1.0)),
        sz('Frage 4', 'Was nicht Nutzwärme wird, verlässt den Kessel als Wärme: im heissen Abgas durch den Kamin und an die Umgebung. Verschwunden ist es nicht.',
           notiz('Verlust: Wärme im Abgas|und an die Umgebung', y=320, ein=1.0)),
        sz('Frage 5', 'Zehn Liter Heizöl wiegen acht Komma vier Kilogramm. Mal zweiundvierzig Komma sechs Megajoule pro Kilogramm sind das rund dreihundertachtundfünfzig Megajoule.',
           formel(r'm = 10\;\text{l} \cdot 0.84\;\tfrac{\text{kg}}{\text{l}} = 8.4\;\text{kg}', y=280, g=36, ein=1.0),
           formel(r'Q_\text{zu} = 8.4\;\text{kg} \cdot 42.6\;\tfrac{\text{MJ}}{\text{kg}} \approx 358\;\text{MJ}', y=400, g=36, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Kachelofen verbrennt 2 kg Buchenholz (H = 15 MJ/kg) mit dem Wirkungsgrad 0.75. Wie viel Nutzwärme gibt er ab?', ['30 MJ', '40 MJ', '22.5 MJ'], 2,
             {0: 'Das ist die ganze Energie im Holz. Kommt sie ganz im Raum an?', 1: 'Durch den Wirkungsgrad geteilt? Die Nutzwärme ist kleiner als die zugeführte Energie.'},
             sprich='Ein Kachelofen verbrennt zwei Kilogramm Buchenholz mit fünfzehn Megajoule pro Kilogramm, Wirkungsgrad null Komma sieben fünf. Wie viel Nutzwärme gibt er ab?'),
        wahl('Frage 2', 'Wie viele Kilowattstunden sind 54 MJ?', ['15 kWh', '194.4 kWh', '54 000 kWh'], 0,
             {1: 'Mal 3.6 gerechnet? Eine Kilowattstunde ist mehr als ein Megajoule — also werden es weniger Kilowattstunden.', 2: 'Das wären Kilojoule. Wie viele Megajoule hat eine Kilowattstunde?'},
             sprich='Wie viele Kilowattstunden sind vierundfünfzig Megajoule?',
             rueck_sprich={1: 'Mal drei Komma sechs gerechnet? Eine Kilowattstunde ist mehr als ein Megajoule — also werden es weniger Kilowattstunden.', 2: 'Das wären Kilojoule. Wie viele Megajoule hat eine Kilowattstunde?'}),
        wahl('Frage 3', 'Ein Wasserkocher (2000 W, Wirkungsgrad 0.8) bringt 1.2 kg Wasser von 20 °C auf 100 °C. Wie lange dauert das?', ['2.7 min', '4.2 min', '3.3 min'], 1,
             {0: 'Mit Verlusten dauert es länger. Wo steht der Wirkungsgrad?', 2: 'Das wäre ohne Verluste. Was macht der Wirkungsgrad mit der Zeit?'},
             sprich='Ein Wasserkocher mit zweitausend Watt und dem Wirkungsgrad null Komma acht bringt eins Komma zwei Kilogramm Wasser von zwanzig auf hundert Grad. Wie lange dauert das?'),
        wahl('Frage 4', 'Wohin geht die Energie, die im Kessel nicht zu Nutzwärme wird?', ['Sie verschwindet beim Verbrennen.', 'Sie geht als Wärme mit dem Abgas und an die Umgebung.', 'Sie bleibt im Brennstoff.'], 1,
             {0: 'Energie verschwindet nie. Was ist warm, das den Kessel verlässt?', 2: 'Der Brennstoff verbrennt ganz. Was verlässt den Kessel durch den Kamin?'}),
        wahl('Frage 5', 'Wie viel Energie steckt in 10 l Heizöl (0.84 kg/l, H = 42.6 MJ/kg)?', ['507 MJ', '426 MJ', '358 MJ'], 2,
             {0: 'Durch die Dichte geteilt? Ein Liter Heizöl wiegt weniger als ein Kilogramm.', 1: 'Liter wie Kilogramm eingesetzt? Der Heizwert gilt je Kilogramm.'},
             sprich='Wie viel Energie steckt in zehn Litern Heizöl mit null Komma acht vier Kilogramm pro Liter und zweiundvierzig Komma sechs Megajoule pro Kilogramm?'),
    ]))


# ================================================================== Kapitel 5: Energiesysteme
A_G = 2e6 / 220
A_CH, A_PV = 41285, 60e9 / 220 / 1e6
assert abs(A_G - 9090.9) < 0.1 and abs(A_PV - 272.73) < 0.01 and 0.005 < A_PV / A_CH < 0.007


def saison(xb, bars, ymax=80, a=None, **kw):
    """Sommer- und Winterhalbjahr: bars = [(Name, [Sommer, Winter], Farbe, gestrichelt, _ein)]"""
    fl, st, tx = [], [], []
    n = len(bars)
    for j, (name, w, f, gestr, e) in enumerate(bars):
        d = {'_ein': e} if e else {}
        for i in range(2):
            x0 = 1 + i * 6 + j * 1.6
            if gestr:
                st += [S(p, q, f, dicke=4, gestrichelt=True, **d) for p, q in zip(rechteck(x0, 0, x0 + 1.3, w[i]), rechteck(x0, 0, x0 + 1.3, w[i])[1:] + [(x0, 0)])]
            else:
                fl.append(F(rechteck(x0, 0, x0 + 1.3, w[i]), f, 0.55, **d))
            tx.append(T(x0 + 0.65, w[i] + 2.5, '%g' % w[i], f, 24, **d))
        tx.append(T(0.6 + 4.2 * j, -15, name, f, 26, 'start', **d))
    tx += [T(1 + 0.8 * n, -5, 'Sommerhalbjahr', TIN, 24), T(7 + 0.8 * n, -5, 'Winterhalbjahr', TIN, 24)]
    return graf(xb, (-21, ymax * 1.08), [], [20, 40, 60, 80], '', 'Anteil [%]', a=a, flaechen=fl, strecken=st, texte=tx, **kw)


DREH.append(dict(KOPF, titel='Wärme sehen: Energiesysteme im Vergleich', dateiname='p5-2-lp-energiesysteme',
    kurzbeschrieb='Wasserkraft, Wind, Sonne, Biogas, Wärmepumpe, Wärme-Kraft-Kopplung und Kernenergie nach Quelle oder Technik, Wirkungsgrad, Verfügbarkeit und Kohlendioxid — vorgerechnet: wie viel Solarfläche eine Gemeinde bräuchte und was im Winter fehlt.',
    schlagworte=['Energiesysteme', 'erneuerbare Energien', 'Photovoltaik', 'Wasserkraft', 'Windkraft', 'Kernenergie', 'Wärme-Kraft-Kopplung'], _probe=EIN % 5,
    szenen=[
        sz('Sieben Systeme', 'Wasserkraft, Wind, Sonne, Biogas, Wärmepumpe, Wärme-Kraft-Kopplung und Kernenergie: Woher kommt unser Strom, und wie vergleicht man so verschiedene Systeme?',
           titel('Wie vergleicht man sie?', g=62),
           skizze(texte=[T(3.0, 8.4, 'Wasserkraft', TIN, 30, _ein='Wasserkraft'), T(7.2, 8.0, 'Wind', TIN, 30, _ein='Wind'), T(2.3, 6.4, 'Sonne', TIN, 30, _ein='Sonne'),
                         T(6.4, 6.1, 'Biogas', TIN, 30, _ein='Biogas'), T(3.6, 4.2, 'Wärmepumpe', TIN, 30, _ein='Wärmepumpe'),
                         T(5.4, 2.4, 'Wärme-Kraft-Kopplung', TIN, 30, _ein='Wärme-Kraft'), T(7.6, 4.4, 'Kernenergie', TIN, 30, _ein='Kernenergie')])),
        sz('Quelle oder Technik', 'Wasser, Wind, Sonne und Biogas sind erneuerbare Quellen: Ihre Energie fliesst laufend nach, fast immer letztlich von der Sonne. Die Kernenergie ist eine Quelle, aber nicht erneuerbar: Uran ist ein Vorrat. Wärmepumpe und Wärme-Kraft-Kopplung sind keine Quellen, sondern Techniken: Sie nutzen zugeführte Energie besser.',
           notiz('erneuerbar: fliesst nach', y=300, a='Wasser, Wind', farbe='gruen'),
           notiz('nicht erneuerbar: Vorrat', y=420, a='Die Kernenergie'),
           notiz('Technik, keine Quelle', y=540, a='Wärmepumpe und', farbe='rot'),
           skizze(a='Wasser, Wind', strecken=umriss(0.4, 6.2, 9.6, 9.4, GRU, 4) + umriss(0.4, 3.6, 9.6, 5.6, TIN, 4, _ein='Die Kernenergie') + umriss(0.4, 0.6, 9.6, 3.0, ROT, 4, _ein='Wärmepumpe und'),
                  texte=[T(5, 8.6, 'erneuerbare Quellen', GRU, 28), T(5, 7.0, 'Wasser · Wind · Sonne · Biogas', TIN, 28),
                         T(5, 4.9, 'Quelle, nicht erneuerbar', TIN, 28, _ein='Die Kernenergie'), T(5, 4.0, 'Kernenergie', TIN, 28, _ein='Die Kernenergie'),
                         T(5, 2.3, 'Techniken', ROT, 28, _ein='Wärmepumpe und'), T(5, 1.2, 'Wärmepumpe · Wärme-Kraft-Kopplung', TIN, 28, _ein='Wärmepumpe und')])),
        sz('Wirkungsgrad', 'Je hundert Kilowattstunden, die hineinfliessen: Die Wasserkraft macht fünfundachtzig daraus Strom, die Photovoltaik zwanzig. Ein Kernkraftwerk macht dreiunddreissig Strom, zwei Drittel sind Abwärme. Die Wärme-Kraft-Kopplung nutzt die Abwärme mit: fünfunddreissig Strom und fünfundfünfzig Nutzwärme.',
           notiz('Wirkungsgrad: welcher Anteil|als Nutzen herauskommt', y=300, a='Je hundert'),
           notiz('Wasserkraft: 85 % Strom', y=430, g=38, a='fünfundachtzig'),
           notiz('Photovoltaik: 20 % Strom', y=490, g=38, a='die Photovoltaik zwanzig'),
           notiz('Kernkraftwerk: 33 % Strom', y=550, g=38, a='dreiunddreissig Strom'),
           notiz('WKK: 35 % Strom + 55 % Wärme', y=610, g=38, a='fünfunddreissig Strom'),
           bild('p5-2-lp-energiesysteme-wasser.jpg', a='Die Wasserkraft'),
           bild('p5-2-lp-energiesysteme-pv.jpg', a='die Photovoltaik'),
           bild('p5-2-lp-energiesysteme-kern.jpg', a='dreiunddreissig Strom'),
           bild('p5-2-lp-energiesysteme-wkk.jpg', a='fünfunddreissig Strom')),
        sz('Verfügbarkeit', 'Entscheidend ist auch, wann die Energie kommt. Die Photovoltaik liefert rund siebzig Prozent im Sommerhalbjahr, gebraucht wird aber mehr im Winter. Wind liefert im Winter rund zwei Drittel. Speicherseen und Biogas halten Energie bereit und liefern auf Abruf.',
           notiz('Photovoltaik: Sommer', y=300, a='Die Photovoltaik'),
           notiz('Wind: Winter', y=360, a='Wind liefert'),
           notiz('Speichersee, Biogas: auf Abruf', y=420, a='Speicherseen und Biogas'),
           saison((-0.5, 13), [('Photovoltaik', [70, 30], GRU, False, 'rund siebzig'), ('Bedarf', [45, 55], TIN, True, 'gebraucht wird aber'),
                               ('Wind', [35, 65], TIN, False, 'Wind liefert')], a='Die Photovoltaik')),
        sz('Kohlendioxid', 'Über den ganzen Lebensweg gerechnet, mit Bau und Brennstoff, stossen Wind und Kernenergie je Kilowattstunde Strom rund elf bis zwölf Gramm Kohlendioxid aus, die Wasserkraft rund vierundzwanzig, die Photovoltaik rund einundvierzig. Ein Erdgaskraftwerk stösst rund vierhundertneunzig Gramm aus.',
           notiz('Kohlendioxid je kWh Strom,|über den Lebensweg', y=300, a='Über den ganzen'),
           notiz('Medianwerte IPCC 2014', y=470, g=34, a='Über den ganzen'),
           graf((-190, 560), (0, 10), achsen=False, a='stossen Wind',
                flaechen=[F(rechteck(0, 8.6, 11, 9.4), TIN, 0.5, _ein='rund elf bis zwölf'), F(rechteck(0, 7.1, 12, 7.9), TIN, 0.5, _ein='rund elf bis zwölf'), F(rechteck(0, 5.6, 24, 6.4), TIN, 0.5, _ein='die Wasserkraft'),
                          F(rechteck(0, 4.1, 41, 4.9), TIN, 0.5, _ein='die Photovoltaik'), F(rechteck(0, 2.6, 490, 3.4), TIN, 0.5, _ein='vierhundertneunzig')],
                texte=[T(-8, 8.75, 'Wind', TIN, 26, 'end'), T(-8, 7.25, 'Kernenergie', TIN, 26, 'end'), T(-8, 5.75, 'Wasserkraft', TIN, 26, 'end', _ein='die Wasserkraft'),
                       T(-8, 4.25, 'Photovoltaik', TIN, 26, 'end', _ein='die Photovoltaik'), T(-8, 2.75, 'Erdgas', TIN, 26, 'end', _ein='Ein Erdgaskraftwerk'),
                       T(18, 8.75, '11 g', TIN, 24, 'start', _ein='rund elf bis zwölf'), T(19, 7.25, '12 g', TIN, 24, 'start', _ein='rund elf bis zwölf'), T(31, 5.75, '24 g', TIN, 24, 'start', _ein='die Wasserkraft'),
                       T(48, 4.25, '41 g', TIN, 24, 'start', _ein='die Photovoltaik'), T(480, 2.0, '490 g', TIN, 24, 'end', _ein='vierhundertneunzig')])),
        sz('Problem Gemeinde', 'Jetzt ein ganzes Problem. Eine Gemeinde braucht im Jahr zwei Millionen Kilowattstunden Strom, fünfundfünfzig Prozent davon im Winterhalbjahr. Wie viel Modulfläche bräuchte eine Photovoltaikanlage dafür? Rechne mit tausendeinhundert Kilowattstunden Sonnenlicht pro Quadratmeter und Jahr und einem Wirkungsgrad von null Komma zwei. Und reicht sie im Winter, wenn sie dann nur dreissig Prozent liefert?',
           notiz('Strom: 2 000 000 kWh im Jahr', y=290, g=38, a='zwei Millionen'),
           notiz('davon 55 % im Winterhalbjahr', y=345, g=38, a='fünfundfünfzig Prozent'),
           notiz('Licht: 1100 kWh je m² und Jahr', y=430, g=38, a='tausendeinhundert Kilowattstunden Sonnenlicht'),
           notiz('@\\eta = 0.2@', y=485, g=38, a='Wirkungsgrad von null'),
           notiz('im Winter nur 30 %', y=540, g=38, a='dreissig Prozent liefert'),
           notiz('gesucht: Fläche @A@', y=610, a='Wie viel Modulfläche', farbe='rot'),
           skizze(strecken=[P((2.0, 8.0), (3.6, 6.0), ORA, dicke=6), P((2.6, 8.4), (4.4, 6.2), ORA, dicke=6)] + umriss(3.2, 4.0, 7.4, 6.0, TIN, 4),
                  flaechen=[F(rechteck(3.2, 4.0, 7.4, 6.0), TIN, 0.25)], kurven=[{'formel': '8.6+sqrt(abs(0.49-(x-1.4)*(x-1.4)))', 'von': 0.7, 'bis': 2.1, 'farbe': ORA, 'dicke': 4},
                                                                              {'formel': '8.6-sqrt(abs(0.49-(x-1.4)*(x-1.4)))', 'von': 0.7, 'bis': 2.1, 'farbe': ORA, 'dicke': 4}],
                  texte=[T(5.3, 4.9, 'Module: A = ?', TIN, 28), T(5.3, 2.4, '2 000 000 kWh im Jahr', TIN, 28, _ein='zwei Millionen')])),
        sz('Vorgehen Gemeinde', 'Ein Quadratmeter liefert Eta mal tausendeinhundert Kilowattstunden Strom im Jahr. Die nötige Fläche ist die Jahresenergie geteilt durch diesen Ertrag je Quadratmeter.',
           formel(r'E_{1\,\text{m}^2} = \eta \cdot 1100\;\text{kWh}', y=300, g=44, a='Ein Quadratmeter'),
           formel(r'A = \frac{E}{\eta \cdot 1100\;\text{kWh/m}^2}', y=440, g=44, a='Die nötige Fläche'),
           skizze(strecken=umriss(3.5, 3.5, 6.5, 6.5, TIN, 4) + [P((5, 9.2), (5, 6.7), ORA, dicke=10), P((6.7, 5), (9.2, 5), GRU, dicke=5, _ein='Strom im Jahr'),
                                                               P((5, 3.3), (5, 1.4), ROT, dicke=8, _ein='Strom im Jahr')],
                  flaechen=[F(rechteck(3.5, 3.5, 6.5, 6.5), TIN, 0.25)],
                  texte=[T(5, 5, '1 m²', TIN, 30), T(5.3, 9.5, '1100 kWh Licht', ORA, 26, 'start'), T(9.2, 5.6, 'Strom: η · 1100 kWh', GRU, 26, 'end', _ein='Strom im Jahr'),
                         T(5.3, 1.6, 'Abwärme', ROT, 26, 'start', _ein='Strom im Jahr')])),
        sz('Lösung Gemeinde', 'Ein Quadratmeter liefert zweihundertzwanzig Kilowattstunden. Zwei Millionen geteilt durch zweihundertzwanzig: rund neuntausendeinhundert Quadratmeter, knapp ein Hektar. Im Winterhalbjahr liefert die Anlage aber nur dreissig Prozent, sechshunderttausend Kilowattstunden, gebraucht werden eins Komma eins Millionen. Probe: Neuntausendeinhundert mal zweihundertzwanzig gibt wieder rund zwei Millionen. Übers Jahr reicht es, im Winter fehlt fast die Hälfte.',
           formel(r'E_{1\,\text{m}^2} = 0.2 \cdot 1100\;\text{kWh} = 220\;\text{kWh}', y=270, g=34, a='zweihundertzwanzig Kilowattstunden'),
           formel(r'A = \frac{2\,000\,000\;\text{kWh}}{220\;\text{kWh/m}^2} \approx 9100\;\text{m}^2', y=380, g=34, a='rund neuntausendeinhundert'),
           formel(r'0.3 \cdot 2\,000\,000\;\text{kWh} = 600\,000\;\text{kWh}', y=490, g=32, a='sechshunderttausend'),
           notiz('gebraucht: 1 100 000 kWh', y=580, g=34, a='gebraucht werden'),
           notiz('Probe: 9100 m² · 220 kWh/m² ≈ 2 000 000 kWh', y=635, g=34, a='Probe'),
           notiz('im Winter fehlt fast die Hälfte', y=690, g=34, a='im Winter fehlt', farbe='rot'),
           graf((-1.6, 13), (-0.2, 1.62), [], [0.4, 0.8, 1.2, 1.6], '', 'E [GWh]', a='Im Winterhalbjahr',
                flaechen=[F(rechteck(1.0, 0, 2.3, 1.4), GRU, 0.55, _ein='sechshunderttausend'), F(rechteck(7.0, 0, 8.3, 0.6), GRU, 0.55, _ein='sechshunderttausend')],
                strecken=[S(p, q, TIN, dicke=4, gestrichelt=True, _ein='gebraucht werden') for x0, h in ((2.6, 0.9), (8.6, 1.1))
                          for p, q in zip(rechteck(x0, 0, x0 + 1.3, h), rechteck(x0, 0, x0 + 1.3, h)[1:] + [(x0, 0)])],
                texte=[T(1.65, 1.46, '1.4', GRU, 24, _ein='sechshunderttausend'), T(7.65, 0.66, '0.6', GRU, 24, _ein='sechshunderttausend'), T(3.25, 0.96, '0.9', TIN, 24, _ein='gebraucht werden'),
                       T(9.25, 1.16, '1.1', TIN, 24, _ein='gebraucht werden'), T(2.2, -0.12, 'Sommerhalbjahr', TIN, 24), T(8.2, -0.12, 'Winterhalbjahr', TIN, 24),
                       T(12.5, 1.55, 'Lieferung', GRU, 26, 'end', _ein='sechshunderttausend'), T(12.5, 1.42, 'Bedarf (gestrichelt)', TIN, 26, 'end', _ein='gebraucht werden')])),
        sz('Potential', 'Und das ganze Land? Für rund sechzig Terawattstunden Strom im Jahr, etwa den Bedarf der Schweiz, bräuchte es rund zweihundertsiebzig Quadratkilometer Module: gut ein halbes Prozent der Landesfläche. Das Potential der Sonne ist gross. Für den Winter braucht es aber Speicher und Systeme, die dann liefern.',
           notiz('Schweiz: rund 60 TWh Strom im Jahr', y=280, g=38, a='Und das ganze Land'),
           formel(r'A = \frac{60 \cdot 10^9\;\text{kWh}}{220\;\text{kWh/m}^2} \approx 270\;\text{km}^2', y=380, g=36, a='bräuchte es rund'),
           notiz('gut 0.5 % der Landesfläche|von 41 285 km²', y=500, a='gut ein halbes Prozent'),
           notiz('Winter: Speicher, Wind, Biogas', y=640, a='Für den Winter', farbe='rot'),
           graf((0, 220), (0, 220), achsen=False, a='Und das ganze Land',
                strecken=umriss(8, 8, 8 + A_CH ** 0.5, 8 + A_CH ** 0.5, TIN, 4) + umriss(100, 100, 100 + A_PV ** 0.5, 100 + A_PV ** 0.5, ORA, 4, _ein='gut ein halbes Prozent'),
                flaechen=[F(rechteck(100, 100, 100 + A_PV ** 0.5, 100 + A_PV ** 0.5), ORA, 0.6, _ein='gut ein halbes Prozent')],
                texte=[T(110, 190, 'Landesfläche: 41 285 km²', TIN, 28), T(122, 108, 'Module: 270 km²', ORA, 28, 'start', _ein='gut ein halbes Prozent')])),
        merke('Zum Mitnehmen: Quellen liefern Energie, Techniken nutzen sie besser. Verglichen wird nach Verfügbarkeit, Wirkungsgrad und Kohlendioxid, und die Jahressumme ist noch nicht der Winter.',
              r'\eta = \frac{E_\text{nutz}}{E_\text{zu}}', 'Quelle oder Technik?|vergleichen: Verfügbarkeit, Wirkungsgrad,|Kohlendioxid; Jahressumme ist nicht der Winter'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Gemeinde', 'Wie rechnest du die Modulfläche?', ['A = E · η / (1100 kWh/m²)', 'A = E / (η · 1100 kWh/m²)', 'A = E / (1100 kWh/m²)'], 1,
                 {0: 'Wird mit Verlusten mehr oder weniger Fläche gebraucht?', 2: 'Wird das ganze Sonnenlicht zu Strom?'},
                 sprich='Wie rechnest du die Modulfläche?', kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 5
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zu den Energiesystemen', dateiname='p5-2-lp-kontrolle-energiesysteme',
    kurzbeschrieb='Fünf Fragen: die Wärmepumpe als Technik, der Ertrag eines Sonnenkollektors, warum es Speicher braucht, Lageenergie im Speichersee und was eine Windturbine nicht nutzen kann.',
    schlagworte=['Energiesysteme', 'Photovoltaik', 'Wasserkraft', 'Kohlendioxid', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Die Wärmepumpe ist keine Quelle, sondern eine Technik: Sie hebt mit Strom Umgebungswärme auf Heiztemperatur. Erneuerbar ist allenfalls die Umgebungswärme, die sie nutzt.',
           notiz('Wärmepumpe: Technik,|braucht Strom', y=320, ein=1.0)),
        sz('Frage 2', 'E gleich Eta mal A mal Sonnenlicht je Quadratmeter: null Komma fünf mal sechs Quadratmeter mal tausendzweihundert Kilowattstunden, dreitausendsechshundert Kilowattstunden Wärme im Jahr.',
           formel(r'E = \eta \cdot A \cdot I = 0.5 \cdot 6\;\text{m}^2 \cdot 1200\;\tfrac{\text{kWh}}{\text{m}^2} = 3600\;\text{kWh}', y=320, g=32, ein=1.0)),
        sz('Frage 3', 'Die Photovoltaik liefert nachts nichts und im Winter wenig. Speicherseen geben Energie auf Abruf ab, Wind liefert im Winter mehr.',
           notiz('Sonne: Sommer, Tag|Speicher und Wind: Winter', y=320, ein=1.0)),
        sz('Frage 4', 'Lageenergie m mal g mal h: tausend Kilogramm mal neun Komma acht eins mal zweihundert Meter, rund eins Komma neun sechs Megajoule. Geteilt durch drei Komma sechs Millionen Joule sind das rund null Komma fünf vier fünf Kilowattstunden.',
           formel(r'E = m \cdot g \cdot h = 1000\;\text{kg} \cdot 9.81\;\tfrac{\text{m}}{\text{s}^2} \cdot 200\;\text{m} \approx 1.96\;\text{MJ}', y=290, g=30, ein=1.0),
           formel(r'= \frac{1.962 \cdot 10^6\;\text{J}}{3.6 \cdot 10^6\;\text{J/kWh}} \approx 0.545\;\text{kWh}', y=400, g=32, ein=1.0)),
        sz('Frage 5', 'Hinter der Turbine strömt die Luft langsamer weiter. Die übrigen fünfundfünfzig Prozent bleiben zum grössten Teil als Bewegungsenergie im Wind; ganz abbremsen kann eine Turbine die Luft nicht, sonst käme keine neue nach.',
           notiz('Rest bleibt im Wind:|die Luft strömt langsamer weiter', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Prospekt nennt die Wärmepumpe «eine erneuerbare Energiequelle». Was stimmt?', ['Stimmt: Sie liefert mehr Wärme, als sie Strom braucht.', 'Stimmt nicht: Sie ist eine Technik, die mit Strom Umgebungswärme anhebt.', 'Stimmt: Sie erzeugt Wärme aus der Luft.'], 1,
             {0: 'Woher kommt die zusätzliche Wärme? Wird sie erzeugt?', 2: 'Erzeugt die Wärmepumpe Wärme, oder hebt sie vorhandene an?'}),
        wahl('Frage 2', 'Ein Sonnenkollektor fürs Warmwasser hat 6 m² Fläche und den Wirkungsgrad 0.5; am Ort fallen 1200 kWh Licht je m² und Jahr. Wie viel Wärme liefert er im Jahr?', ['3600 kWh', '7200 kWh', '14 400 kWh'], 0,
             {1: 'Das ist das ganze Sonnenlicht auf die Fläche. Wird alles zu Wärme?', 2: 'Durch den Wirkungsgrad geteilt? Die Wärme ist kleiner als das Licht.'},
             sprich='Ein Sonnenkollektor fürs Warmwasser hat sechs Quadratmeter Fläche und den Wirkungsgrad null Komma fünf; am Ort fallen tausendzweihundert Kilowattstunden Licht je Quadratmeter und Jahr. Wie viel Wärme liefert er im Jahr?'),
        wahl('Frage 3', 'Warum braucht ein Land mit viel Photovoltaik auch Speicherseen oder Windkraft?', ['Weil Photovoltaik nachts nichts und im Winter wenig liefert.', 'Weil Photovoltaik viel Kohlendioxid ausstösst.', 'Weil Photovoltaik einen Wirkungsgrad über 100 % hat.'], 0,
             {1: 'Vergleiche die Gramm Kohlendioxid je Kilowattstunde.', 2: 'Kann ein Wirkungsgrad über 100 % liegen?'},
             rueck_sprich={1: 'Vergleiche die Gramm Kohlendioxid je Kilowattstunde.', 2: 'Kann ein Wirkungsgrad über hundert Prozent liegen?'}),
        wahl('Frage 4', '1 m³ Wasser fällt 200 m tief. Wie viel Energie wird frei (ohne Verluste)?', ['0.545 kWh', '0.0556 kWh', '1960 kWh'], 0,
             {1: 'Lageenergie ist m · g · h. Fehlt etwas?', 2: 'Das wären Kilojoule. Wie viele Joule hat eine Kilowattstunde?'},
             sprich='Ein Kubikmeter Wasser fällt zweihundert Meter tief. Wie viel Energie wird frei, ohne Verluste?',
             rueck_sprich={1: 'Lageenergie ist m mal g mal h. Fehlt etwas?', 2: 'Das wären Kilojoule. Wie viele Joule hat eine Kilowattstunde?'}),
        wahl('Frage 5', 'Eine Windturbine macht rund 45 % der Bewegungsenergie der Luft, die durch den Rotor strömt, zu Strom. Was geschieht mit dem Rest?', ['Er bleibt als Bewegungsenergie in der Luft, die langsamer weiterströmt.', 'Er wird im Kühlturm als Abwärme abgegeben.', 'Er verschwindet.'], 0,
             {1: 'Hat eine Windturbine einen Kühlturm? Was ist hinter dem Rotor anders als davor?', 2: 'Energie verschwindet nicht. Wie schnell strömt die Luft hinter dem Rotor?'},
             sprich='Eine Windturbine macht rund fünfundvierzig Prozent der Bewegungsenergie der Luft, die durch den Rotor strömt, zu Strom. Was geschieht mit dem Rest?'),
    ]))


# ================================================================== Kapitel 6: Wärmetransport
def heizkoerper(x0=0.6, y0=2.0, b=1.6, h=4.0):
    st = umriss(x0, y0, x0 + b, y0 + h, TIN, 5) + [S((x0 + b * k / 4, y0 + 0.3), (x0 + b * k / 4, y0 + h - 0.3), TIN, dicke=3) for k in (1, 2, 3)]
    return st, [F(rechteck(x0, y0, x0 + b, y0 + h), ROT, 0.18)]


hk_s, hk_f = heizkoerper()
kette = [(1.0 + 1.1 * i, 5.0) for i in range(8)]
DREH.append(dict(KOPF, titel='Wärme sehen: drei Wege der Wärme', dateiname='p5-2-lp-transport',
    kurzbeschrieb='Wärmeleitung, Konvektion und Wärmestrahlung: was die Energie jeweils trägt, was jeder Weg braucht und wie man ihn bremst — vorgerechnet am Weg vom Heizwasser bis zur Hand neben dem Heizkörper.',
    schlagworte=['Wärmetransport', 'Wärmeleitung', 'Konvektion', 'Wärmestrahlung', 'Wärmeleitfähigkeit'], _probe=EIN % 6,
    szenen=[
        sz('Heizkörper', 'Ein Heizkörper wärmt das ganze Zimmer. Wie kommt die Wärme vom heissen Wasser in ihm bis zu dir? Es gibt drei Wege.',
           titel('Drei Wege der Wärme', g=66),
           notiz('vom Heizwasser|bis zur Hand', y=460, a='Wie kommt die Wärme'),
           skizze(strecken=hk_s + [S((0.3, 1.2), (9.7, 1.2), TIN, dicke=4), S((0.3, 1.2), (0.3, 9.4), TIN, dicke=4)],
                  flaechen=hk_f + [F([(7.6, 2.6), (8.6, 2.6), (8.6, 4.4), (8.2, 4.9), (7.6, 4.6)], TIN, 0.3)],
                  texte=[T(1.4, 6.6, 'Heizkörper', TIN, 26), T(8.1, 2.0, 'Hand', TIN, 26), T(5, 9.0, 'Zimmer', TIN, 26)])),
        sz('Leitung', 'Bei der Wärmeleitung geben die Teilchen ihre Bewegungsenergie an die Nachbarn weiter, ohne selbst zu wandern. Metalle leiten gut, Holz und Luft schlecht.',
           notiz('Leitung: Energie wandert|von Teilchen zu Teilchen', y=300, a='Bei der Wärmeleitung'),
           notiz('Metalle leiten gut;|Holz und Luft schlecht', y=470, a='Metalle leiten gut'),
           skizze(punkte=[{'x': x, 'y': y, 'farbe': TIN} for x, y in kette],
                  strecken=[P((x + 0.15, 5.3), (x + 0.95, 5.3), ROT, dicke=5, _ein='geben die Teilchen ihre Bewegungsenergie', _ein_versatz=0.45 * i) for i, (x, y) in enumerate(kette[:-1])]
                           + [S((0.6, 4.4), (9.4, 4.4), TIN, dicke=3), S((0.6, 5.9), (9.4, 5.9), TIN, dicke=3)],
                  flaechen=[F(rechteck(0.6, 4.4, 9.4, 5.9), TIN, 0.08)],
                  texte=[T(0.6, 6.6, 'heiss', ROT, 26, 'start'), T(9.4, 6.6, 'kalt', TIN, 26, 'end'), T(5, 7.6, 'Teilchen bleiben am Ort', TIN, 26, _ein='ohne selbst zu wandern')])),
        sz('Konvektion', 'Bei der Konvektion strömt der Stoff selbst: Die warme Luft über dem Heizkörper steigt auf, kühlt an der Decke ab und sinkt an der anderen Seite wieder nach unten. So verteilt sie die Wärme im ganzen Zimmer. Das geht nur in Flüssigkeiten und Gasen.',
           notiz('Konvektion: der Stoff|strömt selbst', y=300, a='Bei der Konvektion'),
           notiz('nur in Flüssigkeiten|und Gasen', y=470, a='Das geht nur'),
           skizze(strecken=hk_s + [S((0.3, 1.2), (9.7, 1.2), TIN, dicke=4), S((0.3, 9.4), (9.7, 9.4), TIN, dicke=4),
                                   P((1.4, 6.4), (1.4, 8.6), ROT, dicke=6, _ein='steigt auf'), P((2.0, 8.9), (8.4, 8.9), ROT, dicke=6, _ein='kühlt an der Decke'),
                                   P((8.9, 8.4), (8.9, 2.2), TIN, dicke=6, _ein='sinkt an der anderen Seite'), P((8.4, 1.6), (2.6, 1.6), TIN, dicke=6, _ein='So verteilt sie')],
                  flaechen=hk_f)),
        sz('Strahlung', 'Bei der Wärmestrahlung trägt Infrarotstrahlung die Energie, wie Licht, nur langwelliger. Sie braucht keinen Stoff dazwischen, so wie das Licht der Sonne.',
           notiz('Strahlung: Infrarot,|wie Licht, nur langwelliger', y=300, a='Bei der Wärmestrahlung'),
           notiz('braucht keinen Stoff', y=470, a='Sie braucht keinen Stoff'),
           skizze(strecken=hk_s + [s_ for k, y in enumerate((3.0, 4.0, 5.0)) for s_ in [dict(w, _ein='Bei der Wärmestrahlung', _ein_versatz=0.3 * k) for w in
                                                                         [S(((2.4 + 5.0 * i / 40), y + 0.2 * math.sin(2 * math.pi * 6 * i / 40)), ((2.4 + 5.0 * (i + 1) / 40), y + 0.2 * math.sin(2 * math.pi * 6 * (i + 1) / 40)), ROT, dicke=4) for i in range(40)]]],
                  flaechen=hk_f + [F([(7.6, 2.6), (8.6, 2.6), (8.6, 4.4), (8.2, 4.9), (7.6, 4.6)], TIN, 0.3)],
                  texte=[T(5.0, 6.0, 'Infrarot', ROT, 28), T(8.1, 2.0, 'Hand', TIN, 26)])),
        sz('Problem Hand', 'Jetzt ein ganzes Problem. Deine Hand ist zwei Meter neben einem Heizkörper. Auf welchen Wegen kommt die Wärme vom heissen Wasser im Heizkörper bis zu deiner Hand?',
           notiz('Hand: 2 m neben dem Heizkörper', y=300, a='zwei Meter'),
           notiz('gesucht: alle Wege der Wärme', y=450, a='Auf welchen Wegen', farbe='rot'),
           skizze(strecken=hk_s + [S((0.3, 1.2), (9.7, 1.2), TIN, dicke=4), S((2.4, 3.6), (7.4, 3.6), TIN, dicke=3, gestrichelt=True, _ein='zwei Meter')],
                  flaechen=hk_f + [F([(7.6, 2.6), (8.6, 2.6), (8.6, 4.4), (8.2, 4.9), (7.6, 4.6)], TIN, 0.3)],
                  texte=[T(4.9, 3.0, '2 m', TIN, 28, _ein='zwei Meter'), T(1.4, 6.6, 'Heizkörper mit heissem Wasser', TIN, 24, 'start'), T(8.1, 2.0, 'Hand', TIN, 26)])),
        sz('Vorgehen Hand', 'Geh den Weg Stück für Stück: zuerst durch die Metallwand des Heizkörpers, dann von seiner Oberfläche durch die Luft zur Hand. Für jedes Stück fragst du: Wandert nur Energie, strömt Stoff, oder kommt Strahlung ohne Stoff?',
           notiz('Stück 1: durch die Metallwand', y=300, a='zuerst durch die Metallwand'),
           notiz('Stück 2: durch die Luft zur Hand', y=360, a='dann von seiner'),
           notiz('Energie wandert? Stoff strömt?|Strahlung?', y=480, a='Für jedes Stück'),
           skizze(strecken=hk_s + [S((0.3, 1.2), (9.7, 1.2), TIN, dicke=4)],
                  flaechen=hk_f + [F([(7.6, 2.6), (8.6, 2.6), (8.6, 4.4), (8.2, 4.9), (7.6, 4.6)], TIN, 0.3),
                                   F(rechteck(2.0, 2.0, 2.4, 6.0), ORA, 0.5, _ein='zuerst durch die Metallwand'), F(rechteck(2.6, 2.0, 7.4, 6.0), ORA, 0.15, _ein='dann von seiner Oberfläche')],
                  texte=[T(2.2, 6.5, '1', ORA, 32, _ein='zuerst durch die Metallwand'), T(5.0, 6.5, '2', ORA, 32, _ein='dann von seiner Oberfläche'), T(8.1, 2.0, 'Hand', TIN, 26)])),
        sz('Lösung Hand', 'Durch die Metallwand: Wärmeleitung. Von der Oberfläche wird die Luft warm, steigt auf und verteilt sich im Zimmer: Konvektion. Gleichzeitig strahlt die warme Fläche Infrarot ab, das die Hand direkt trifft: Strahlung. Probe: Über dem Heizkörper ist die Luft viel wärmer als daneben, und seitlich spürt man die Strahlung im Gesicht, auch wenn die Luft noch kühl ist.',
           notiz('1 Metallwand: Leitung', y=290, a='Durch die Metallwand', farbe='rot'),
           notiz('2 Luft: Konvektion', y=390, a='Konvektion. Gleich', farbe='rot'),
           notiz('2 direkt: Strahlung', y=490, a='Strahlung. Probe', farbe='rot'),
           notiz('Probe: über dem Heizkörper warm,|seitlich Strahlung im Gesicht', y=620, g=36, a='Probe'),
           skizze(strecken=hk_s + [S((0.3, 1.2), (9.7, 1.2), TIN, dicke=4), P((1.0, 4.0), (2.6, 4.0), ROT, dicke=5, _ein='Durch die Metallwand'),
                                   P((1.4, 6.4), (1.4, 8.4), ROT, dicke=6, _ein='steigt auf'), P((2.0, 8.7), (7.6, 8.7), ROT, dicke=6, _ein='verteilt sich im Zimmer')]
                  + [dict(S(((2.6 + 4.8 * i / 40), 3.6 + 0.18 * math.sin(2 * math.pi * 6 * i / 40)), ((2.6 + 4.8 * (i + 1) / 40), 3.6 + 0.18 * math.sin(2 * math.pi * 6 * (i + 1) / 40)), ROT, dicke=4), _ein='Gleichzeitig strahlt') for i in range(40)],
                  flaechen=hk_f + [F([(7.6, 2.6), (8.6, 2.6), (8.6, 4.4), (8.2, 4.9), (7.6, 4.6)], TIN, 0.3)],
                  texte=[T(2.9, 4.6, 'Leitung', ROT, 24, 'start', _ein='Durch die Metallwand'), T(4.8, 9.2, 'Konvektion', ROT, 24, _ein='Konvektion. Gleich'),
                         T(5.0, 2.6, 'Strahlung', ROT, 24, _ein='Strahlung. Probe'), T(8.1, 2.0, 'Hand', TIN, 26)])),
        merke('Zum Mitnehmen: Leitung braucht Stoff, aber keine Strömung. Konvektion braucht strömenden Stoff. Strahlung braucht gar nichts.',
              r'\text{Leitung; Konvektion; Strahlung}', 'Leitung: Stoff, keine Strömung|Konvektion: strömender Stoff|Strahlung: kein Stoff'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Hand', 'Welcher Weg bringt die Wärme durch die Metallwand des Heizkörpers?', ['Konvektion', 'Leitung', 'Strahlung'], 1,
                 {0: 'Strömt die Metallwand?', 2: 'Liegt zwischen Wasser und Wand leerer Raum, oder berühren sie sich?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 6
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zum Wärmetransport', dateiname='p5-2-lp-kontrolle-transport',
    kurzbeschrieb='Fünf Fragen: Föhn, Daunenjacke, Wärmebildkamera, Kochtopf mit Kupferboden und die glänzende Seite einer Rettungsdecke.',
    schlagworte=['Wärmetransport', 'Leitung', 'Konvektion', 'Strahlung', 'Kontrollfragen'], _probe=KTRL % 6,
    szenen=[
        sz('Frage 1', 'Der Föhn bläst erwärmte Luft auf die Haare. Die Luft strömt und trägt die Wärme mit: Konvektion.',
           notiz('strömende warme Luft:|Konvektion', y=320, ein=1.0)),
        sz('Frage 2', 'Die Daunen halten viel Luft in kleinen Kammern fest. Ruhende Luft leitet sehr schlecht, und in den kleinen Kammern kann sie kaum strömen: Leitung und Konvektion sind gebremst.',
           notiz('eingeschlossene Luft:|Leitung und Konvektion gebremst', y=320, ein=1.0)),
        sz('Frage 3', 'Auch ein Mensch von rund dreissig Grad Hauttemperatur strahlt Infrarot ab, ganz ohne Licht. Diese Wärmestrahlung fängt die Kamera auf und macht sie sichtbar.',
           notiz('jeder Körper strahlt:|die Kamera fängt Infrarot auf', y=320, ein=1.0)),
        sz('Frage 4', 'Kupfer leitet die Wärme rund siebenundzwanzigmal besser als Edelstahl: rund vierhundert gegen fünfzehn Watt pro Meter und Kelvin. Der Kupferboden verteilt die Wärme der Platte rasch und gleichmässig über den ganzen Topfboden.',
           notiz('Kupfer: 400 W/(m·K)|Edelstahl: 15 W/(m·K)', y=320, ein=1.0)),
        sz('Frage 5', 'Die glänzende Seite wirft die Wärmestrahlung des Körpers zurück. Zusätzlich hält die geschlossene Folie den Wind ab; das aber kann jede Plastikfolie.',
           notiz('glänzende Fläche:|Strahlung zurück', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Föhn trocknet die Haare mit warmer Luft. Welcher Weg der Wärme ist das vor allem?', ['Leitung', 'Strahlung', 'Konvektion'], 2,
             {0: 'Berührt der Föhn die Haare?', 1: 'Was kommt aus dem Föhn heraus?'}),
        wahl('Frage 2', 'Warum hält eine Daunenjacke warm?', ['Die Daunen erzeugen selbst Wärme.', 'Sie hält viel Luft in kleinen Kammern fest: Leitung und Konvektion sind gebremst.', 'Sie wirft die Kälte zurück.'], 1,
             {0: 'Kann eine Jacke Energie erzeugen?', 2: 'Fliesst Kälte? Was fliesst wirklich, und in welche Richtung?'}),
        wahl('Frage 3', 'Eine Wärmebildkamera zeigt dich auch in einem völlig dunklen Raum. Was empfängt sie?', ['warme Luft, die von dir aufsteigt', 'Wärmestrahlung, die dein Körper abgibt', 'Wärme, die durch das Kameragehäuse geleitet wird'], 1,
             {0: 'Steigt die warme Luft zur Kamera, die weit weg steht?', 2: 'Berührt die Kamera dich?'}),
        wahl('Frage 4', 'Ein Kochtopf aus Edelstahl hat einen dicken Boden aus Kupfer. Wozu?', ['Kupfer leitet die Wärme der Platte rasch und gleichmässig in den Topf.', 'Kupfer strahlt mehr Wärme ab als Edelstahl.', 'Kupfer hält die Wärme vom Topf fern.'], 0,
             {1: 'Der Boden liegt auf der Platte. Welcher Weg der Wärme zählt dort?', 2: 'Soll die Wärme der Platte in den Topf oder nicht?'}),
        wahl('Frage 5', 'Eine Rettungsdecke hat eine glänzende, spiegelnde Seite. Was bewirkt diese glänzende Fläche vor allem?', ['Sie wirft die Wärmestrahlung des Körpers zurück.', 'Sie leitet die Wärme schneller vom Körper weg.', 'Sie erzeugt Wärme aus dem Licht der Umgebung.'], 0,
             {1: 'Soll die Decke die Wärme wegleiten oder beim Körper halten?', 2: 'Kann eine Folie Energie erzeugen? Was kann eine spiegelnde Fläche?'}),
    ]))

# ================================================================== Kapitel 7: Treibhauseffekt
L10 = math.log(10)


def LX(lam):
    """x-Koordinate im Spektrum: log10(λ/µm) + 1.2 (y-Achse links von 0.1 µm)"""
    return math.log10(lam) + 1.2


def planck(T, K):
    return 'exp(-5*(x-1.2)*%.6f)/(exp(14388/(exp((x-1.2)*%.6f)*%d))-1)*%.6g' % (L10, L10, T, K)


assert abs(10 ** (-5 * math.log10(0.4996552)) / (math.exp(14388 / (0.4996552 * 5800)) - 1) * 4.430951 - 1) < 1e-4
SPEK = dict(xteilung=[[LX(0.1), '0.1'], [LX(0.5), '0.5'], [LX(1), '1'], [LX(5), '5'], [LX(10), '10'], [LX(50), '50'], [LX(100), '100']],
            )


def spektrum(a=None, baender=None, sonne_ein=None, erde_ein=None):
    kv = [dict({'formel': planck(5800, 4.430951), 'von': 0.2, 'bis': 3.2, 'farbe': ORA, 'dicke': 5, 'n': 400}, **({'_ein': sonne_ein} if sonne_ein else {})),
          dict({'formel': planck(288, 14678255.42), 'von': 0.2, 'bis': 3.2, 'farbe': ROT, 'dicke': 5, 'n': 400}, **({'_ein': erde_ein} if erde_ein else {}))]
    fl = []
    if baender is not None:
        fl = [F(rechteck(LX(p), 0, LX(q), 1.12), TIN, 0.25, **({'_ein': baender} if baender else {})) for p, q in ((5.5, 7.5), (13.5, 17.0), (20, 100))]
    tx = [dict(T(LX(0.5), 1.05, 'Sonne', ORA, 28), **({'_ein': sonne_ein} if sonne_ein else {})),
          dict(T(LX(10), 1.05, 'Erde', ROT, 28), **({'_ein': erde_ein} if erde_ein else {}))]
    g = graf((-0.36, 3.32), (-0.12, 1.2), [], [], 'λ [µm]', 'relativ', a=a, kurven=kv, flaechen=fl, texte=tx, **SPEK)
    g['yteilung'] = [[0.5, '0.5'], [1, '1']]
    return g


ERDE = [S((0.5, 1.5), (9.5, 1.5), TIN, dicke=6)]
DREH.append(dict(KOPF, titel='Wärme sehen: Licht hinein, Wärmestrahlung hinaus', dateiname='p5-2-lp-treibhaus',
    kurzbeschrieb='Warum die Sonne Licht und die Erde Wärmestrahlung abgibt, warum die Atmosphäre das eine durchlässt und das andere aufhält, die Gegenstrahlung und der verstärkte Treibhauseffekt — vorgerechnet: −18 °C ohne Atmosphäre gegen 15 °C mit ihr.',
    schlagworte=['Treibhauseffekt', 'Wärmestrahlung', 'Infrarot', 'Atmosphäre', 'Gegenstrahlung', 'Kohlendioxid'], _probe=EIN % 7,
    szenen=[
        sz('Kalt', 'Die Erde nimmt im Mittel rund zweihundertvierzig Watt Sonnenlicht pro Quadratmeter auf. Müsste der Boden genau diese Energie selbst wieder abstrahlen, wäre er eiskalt. Warum ist er es nicht?',
           titel('Warum nicht eiskalt?', g=66),
           notiz('aufgenommen:|rund 240 W/m² Sonnenlicht', y=460, a='Die Erde nimmt'),
           skizze(strecken=ERDE + [P((2.5, 9.0), (2.5, 1.8), ORA, dicke=12, _ein='Die Erde nimmt')],
                  kurven=[{'formel': '9.2+sqrt(abs(0.36-(x-1.0)*(x-1.0)))', 'von': 0.4, 'bis': 1.6, 'farbe': ORA, 'dicke': 4},
                          {'formel': '9.2-sqrt(abs(0.36-(x-1.0)*(x-1.0)))', 'von': 0.4, 'bis': 1.6, 'farbe': ORA, 'dicke': 4}],
                  texte=[T(3.0, 5.0, '240 W/m² Licht', ORA, 28, 'start', _ein='Die Erde nimmt'), T(5, 0.8, 'Boden', TIN, 26),
                         T(7.0, 5.0, '?', ROT, 48, _ein='Warum ist er es nicht')])),
        sz('Zwei Strahlungen', 'Jeder Körper strahlt, und je heisser er ist, desto kürzer ist die Wellenlänge, bei der er am meisten strahlt. Die rund fünftausendfünfhundert Grad heisse Sonne strahlt vor allem sichtbares Licht, um einen halben Mikrometer. Die Erde mit rund fünfzehn Grad strahlt Wärmestrahlung im Infrarot, um zehn Mikrometer: zwanzigmal langwelliger.',
           notiz('je heisser, desto kürzer die|Wellenlänge der stärksten Strahlung', y=300, a='Jeder Körper strahlt'),
           notiz('Sonne: Licht, um 0.5 µm', y=450, a='Die rund fünftausendfünfhundert', farbe='gold'),
           notiz('Erde: Infrarot, um 10 µm', y=560, a='Die Erde mit rund', farbe='rot'),
           spektrum(a='Jeder Körper strahlt', sonne_ein='Die rund fünftausendfünfhundert', erde_ein='Die Erde mit rund')),
        sz('Durchlässig', 'Für das Licht ist die Atmosphäre weitgehend durchlässig. Die Wärmestrahlung dagegen nehmen Wasserdampf und Kohlendioxid in breiten Bereichen auf. Stickstoff und Sauerstoff, der grösste Teil der Luft, lassen beides durch.',
           notiz('Licht: kommt durch', y=300, a='Für das Licht', farbe='gold'),
           notiz('Infrarot: grau = von Wasserdampf|und Kohlendioxid aufgenommen', y=430, a='Die Wärmestrahlung dagegen', farbe='rot'),
           notiz('Stickstoff, Sauerstoff:|lassen beides durch', y=600, a='Stickstoff und Sauerstoff'),
           spektrum(baender='Die Wärmestrahlung dagegen')),
        sz('Gegenstrahlung', 'Was die Gase aufnehmen, strahlen sie in alle Richtungen wieder ab, auch zurück zum Boden. Der Boden bekommt so Sonnenlicht und Gegenstrahlung und wird wärmer. Im Einschichtmodell geht hier das Licht ganz durch und dreiundzwanzig Prozent der Wärmestrahlung direkt hinaus: Der Boden hat dann fünfzehn Grad, so viel wie gemessen.',
           notiz('Gase strahlen in alle Richtungen,|auch zum Boden: Gegenstrahlung', y=300, a='Was die Gase aufnehmen'),
           notiz('Einschichtmodell: Licht 100 % durch,', y=480, a='Im Einschichtmodell'),
           notiz('23 % der Wärmestrahlung hinaus', y=540, a='dreiundzwanzig Prozent der'),
           notiz('Boden: rund 15 °C', y=620, a='fünfzehn Grad, so'),
           skizze(strecken=ERDE + [P((1.6, 9.6), (1.6, 1.8), ORA, dicke=12, _ein='Sonnenlicht und'),
                                   P((4.4, 1.8), (4.4, 5.9), ROT, dicke=12),
                                   P((5.6, 7.5), (5.6, 9.6), ROT, dicke=7, _ein='in alle Richtungen'),
                                   P((8.2, 5.9), (8.2, 1.8), ROT, dicke=7, _ein='auch zurück zum Boden'),
                                   P((3.2, 1.8), (3.2, 9.6), ROT, dicke=3, _ein='dreiundzwanzig Prozent der')],
                  flaechen=[F(rechteck(0.2, 6.0, 9.8, 7.4), TIN, 0.25)],
                  texte=[T(9.7, 6.5, 'Atmosphäre: Gase', TIN, 24, 'end'), T(1.9, 4.0, 'Licht', ORA, 26, 'start', _ein='Sonnenlicht und'),
                         T(4.7, 3.6, 'Wärmestrahlung', ROT, 24, 'start'), T(7.9, 3.0, 'Gegenstrahlung', ROT, 26, 'end', _ein='Gegenstrahlung und'),
                         T(3.4, 8.8, '23 %', ROT, 24, 'start', _ein='dreiundzwanzig Prozent der'), T(5, 0.8, 'Boden', TIN, 26)])),
        sz('Problem Strahlung', 'Jetzt ein ganzes Problem. Ohne Atmosphäre müsste der Boden die zweihundertvierzig Watt pro Quadratmeter selbst abstrahlen. Welche Temperatur hätte er dann? Und wie viel strahlt er bei den gemessenen fünfzehn Grad ab?',
           notiz('ohne Atmosphäre:|Boden strahlt 240 W/m² ab', y=300, a='Ohne Atmosphäre'),
           notiz('gesucht: Temperatur @T@;|Abstrahlung bei 15 °C', y=470, a='Welche Temperatur', farbe='rot'),
           skizze(strecken=ERDE + [P((3.0, 9.0), (3.0, 1.8), ORA, dicke=12), P((7.0, 1.8), (7.0, 9.0), ROT, dicke=12, _ein='selbst abstrahlen')],
                  texte=[T(3.4, 6.0, '240 W/m²', ORA, 28, 'start'), T(7.4, 6.0, '240 W/m²', ROT, 28, 'start', _ein='selbst abstrahlen'), T(5, 0.8, 'Boden: T = ?', TIN, 26)])),
        sz('Vorgehen Strahlung', 'Die Abstrahlung je Quadratmeter ist P durch A gleich Sigma mal T hoch vier, mit T in Kelvin. Nach T aufgelöst: die vierte Wurzel aus P durch A, geteilt durch Sigma.',
           formel(r'\frac{P}{A} = \sigma \cdot T^4', y=300, g=50, a='Die Abstrahlung je'),
           formel(r'T = \sqrt[4]{\frac{P/A}{\sigma}}', y=450, g=50, a='Nach T aufgelöst'),
           notiz('@T@ in Kelvin;|@\\sigma = 5.67 \\cdot 10^{-8}\\;\\text{W/(m}^2\\text{K}^4)@', y=600, g=36, a='mit T in Kelvin')),
        sz('Lösung Strahlung', 'Ohne Atmosphäre: die vierte Wurzel aus zweihundertvierzig durch fünf Komma sechs sieben mal zehn hoch minus acht, rund zweihundertfünfundfünfzig Kelvin, also minus achtzehn Grad. Bei fünfzehn Grad, das sind zweihundertachtundachtzig Kelvin, strahlt der Boden rund dreihundertneunzig Watt pro Quadratmeter ab. Probe im Einschichtmodell: Die Differenz von rund hundertfünfzig Watt pro Quadratmeter kommt als Gegenstrahlung zurück. In Wirklichkeit ist die Gegenstrahlung grösser, rund dreihundertvierzig, weil der Boden auch durch Verdunstung und aufsteigende Luft Wärme abgibt und die Atmosphäre einen Teil des Sonnenlichts selbst aufnimmt.',
           formel(r'T = \sqrt[4]{\frac{240\;\text{W/m}^2}{5.67 \cdot 10^{-8}\;\text{W/(m}^2\text{K}^4)}} \approx 255\;\text{K}', y=280, g=30, a='rund zweihundertfünfundfünfzig'),
           notiz('also rund −18 °C', y=410, g=40, a='also minus achtzehn'),
           formel(r'\frac{P}{A} = 5.67 \cdot 10^{-8}\;\tfrac{\text{W}}{\text{m}^2\text{K}^4} \cdot (288\;\text{K})^4 \approx 390\;\tfrac{\text{W}}{\text{m}^2}', y=500, g=30, a='rund dreihundertneunzig'),
           notiz('Modell: 390 − 240 = 150 W/m²|Gegenstrahlung', y=600, g=34, a='hundertfünfzig Watt'),
           notiz('wirklich: rund 340 W/m²', y=690, g=34, a='rund dreihundertvierzig'),
           graf((-0.6, 4.6), (-50, 470), [], [100, 200, 300, 400], '', 'P/A [W/m²]', a='Ohne Atmosphäre',
                flaechen=[F(rechteck(0.5, 0, 1.4, 240), ORA, 0.55), F(rechteck(1.8, 0, 2.7, 390), ROT, 0.55, _ein='rund dreihundertneunzig'),
                          F(rechteck(3.1, 0, 4.0, 150), ROT, 0.3, _ein='hundertfünfzig Watt')],
                texte=[T(0.95, 260, '240', ORA, 26), T(2.25, 410, '390', ROT, 26, _ein='rund dreihundertneunzig'), T(3.55, 170, '150', ROT, 26, _ein='hundertfünfzig Watt'),
                       T(0.95, -28, 'Licht', TIN, 22), T(2.25, -28, 'Boden', TIN, 22, _ein='rund dreihundertneunzig'), T(3.55, -28, 'zurück', TIN, 22, _ein='hundertfünfzig Watt')])),
        sz('Mehr Kohlendioxid', 'Vor der Industrialisierung enthielt die Luft rund zweihundertachtzig ppm, parts per million, Kohlendioxid, heute rund vierhundertdreissig. Mehr Treibhausgas hält mehr Wärmestrahlung zurück. Im Einschichtmodell gingen vorher fünfundzwanzig Prozent der Wärmestrahlung direkt hinaus, heute dreiundzwanzig. Der Boden wird dadurch von rund dreizehn Komma sieben auf rund vierzehn Komma neun Grad wärmer, um gut ein Grad. Das ist etwa so viel, wie sich die Erde seither erwärmt hat.',
           notiz('Kohlendioxid vorher: 280 ppm', y=280, a='zweihundertachtzig'),
           notiz('heute: 430 ppm', y=340, a='vierhundertdreissig'),
           notiz('Modell vorher: 25 % hinaus', y=420, a='gingen vorher'),
           notiz('Modell heute: 23 % hinaus', y=490, a='heute dreiundzwanzig'),
           notiz('Boden: 13.7 °C → 14.9 °C', y=580, a='vierzehn Komma neun'),
           notiz('gemessen seither: rund +1.2 K', y=660, g=34, a='Das ist etwa so viel'),
           graf((-0.6, 4.6), (-80, 520), [], [100, 200, 300, 400], '', 'CO₂ [ppm]', x=1025, breite=610, hoehe=570, y=195,
                flaechen=[F(rechteck(0.6, 0, 1.8, 280), TIN, 0.4, _ein='zweihundertachtzig'), F(rechteck(2.6, 0, 3.8, 430), TIN, 0.4, _ein='vierhundertdreissig')],
                texte=[T(1.2, 305, '280 ppm', TIN, 26, _ein='zweihundertachtzig'), T(3.2, 455, '430 ppm', TIN, 26, _ein='vierhundertdreissig'),
                       T(1.2, -45, 'vorher', TIN, 24), T(3.2, -45, 'heute', TIN, 24)]),
           bild('p5-2-lp-treibhaus-25-modell.jpg', a='gingen vorher'),
           bild('p5-2-lp-treibhaus-23-modell.jpg', a='heute dreiundzwanzig'),
           bild('p5-2-lp-treibhaus-23.jpg', a='vierzehn Komma neun')),
        merke('Zum Mitnehmen: Die Atmosphäre lässt Licht leichter durch als Wärmestrahlung. Darum ist es am Boden wärmer als ohne sie. Mehr Treibhausgas verstärkt diesen Effekt.',
              r'\frac{P}{A} = \sigma \cdot T^4', 'Licht hinein: leicht|Wärmestrahlung hinaus: schwer|mehr Treibhausgas: stärkerer Effekt'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Strahlung', 'Womit rechnest du die Temperatur aus der Abstrahlung?', ['Q = m · c · ΔT', 'P/A = σ · ϑ⁴ mit ϑ in °C', 'P/A = σ · T⁴ mit T in Kelvin'], 2,
                 {0: 'Hier wird nichts erwärmt — der Boden strahlt ab. Welche Formel beschreibt die Abstrahlung?', 1: 'In welcher Einheit setzt man die Temperatur in σ · T⁴ ein?'},
                 sprich='Womit rechnest du die Temperatur aus der Abstrahlung?',
                 rueck_sprich={0: 'Hier wird nichts erwärmt — der Boden strahlt ab. Welche Formel beschreibt die Abstrahlung?', 1: 'In welcher Einheit setzt man die Temperatur in Sigma mal T hoch vier ein?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 7
DREH.append(dict(KOPF, titel='Wärme sehen: Kontrollfragen zum Treibhauseffekt', dateiname='p5-2-lp-kontrolle-treibhaus',
    kurzbeschrieb='Fünf Fragen: warum die Erde nicht leuchtet, welche Gase Wärmestrahlung aufnehmen, die Abstrahlung bei 30 °C, was die Gase mit der Strahlung tun und warum klare Nächte kalt sind.',
    schlagworte=['Treibhauseffekt', 'Wärmestrahlung', 'Kontrollfragen'], _probe=KTRL % 7,
    szenen=[
        sz('Frage 1', 'Die Erde ist zu kalt, um sichtbares Licht abzugeben. Kühle Körper strahlen langwellig, im Infrarot. Erst sehr heisse Körper wie die Sonne strahlen vor allem Licht.',
           notiz('kühl: Infrarot|sehr heiss: Licht', y=320, ein=1.0)),
        sz('Frage 2', 'Wasserdampf und Kohlendioxid nehmen Wärmestrahlung auf. Stickstoff und Sauerstoff, der grösste Teil der Luft, lassen sie fast ungehindert durch.',
           notiz('Treibhausgase:|Wasserdampf, Kohlendioxid', y=320, ein=1.0)),
        sz('Frage 3', 'Die Temperatur in Kelvin: dreihundertdrei Komma eins fünf. Sigma mal T hoch vier gibt rund vierhundertneunundsiebzig Watt pro Quadratmeter.',
           formel(r'\frac{P}{A} = 5.67 \cdot 10^{-8}\;\tfrac{\text{W}}{\text{m}^2\text{K}^4} \cdot (303.15\;\text{K})^4 \approx 479\;\tfrac{\text{W}}{\text{m}^2}', y=320, g=30, ein=1.0)),
        sz('Frage 4', 'Treibhausgase nehmen die Wärmestrahlung auf und strahlen sie in alle Richtungen wieder ab — ein Teil geht zurück zum Boden. Sie spiegeln nicht.',
           notiz('aufnehmen und in alle|Richtungen abstrahlen', y=320, ein=1.0)),
        sz('Frage 5', 'Wolken bestehen aus Wasser. Sie nehmen die Wärmestrahlung des Bodens auf und strahlen einen Teil zurück. In klaren Nächten geht viel mehr direkt ins All.',
           notiz('Wolken: Gegenstrahlung|klar: mehr geht ins All', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Warum gibt die Erde kein sichtbares Licht ab, die Sonne aber schon?', ['Die Erde ist zu kalt: Kühle Körper strahlen im Infrarot.', 'Die Atmosphäre schluckt das Licht der Erde.', 'Die Erde strahlt gar nicht.'], 0,
             {1: 'Auch ohne Atmosphäre — würde ein 15 °C warmer Stein leuchten?', 2: 'Jeder Körper strahlt. Wovon hängt ab, in welchem Bereich?'},
             rueck_sprich={1: 'Auch ohne Atmosphäre — würde ein fünfzehn Grad warmer Stein leuchten?', 2: 'Jeder Körper strahlt. Wovon hängt ab, in welchem Bereich?'}),
        wahl('Frage 2', 'Welche Gase halten Wärmestrahlung zurück?', ['Stickstoff und Sauerstoff', 'Wasserdampf und Kohlendioxid', 'Helium und Argon'], 1,
             {0: 'Diese beiden machen fast die ganze Luft aus — und lassen beide Strahlungen durch.', 2: 'Edelgase nehmen kaum Infrarot auf. Welche Gase nennt der Clip als Treibhausgase?'}),
        wahl('Frage 3', 'Wie viel Wärmestrahlung gibt ein 30 °C warmer Boden je Quadratmeter ab (σ = 5.67 · 10⁻⁸ W/(m²K⁴))?', ['0.046 W/m²', '479 W/m²', '8.4 · 10⁹ W/m²'], 1,
             {0: 'Die Temperatur in Kelvin einsetzen.', 2: 'Hast du mit σ multipliziert?'},
             sprich='Wie viel Wärmestrahlung gibt ein dreissig Grad warmer Boden je Quadratmeter ab?',
             rueck_sprich={0: 'Die Temperatur in Kelvin einsetzen.', 2: 'Hast du mit Sigma multipliziert?'}),
        wahl('Frage 4', 'Was machen Treibhausgase mit der Wärmestrahlung des Bodens?', ['Sie spiegeln sie wie ein Spiegel zum Boden zurück.', 'Sie vernichten sie.', 'Sie nehmen sie auf und strahlen sie in alle Richtungen wieder ab.'], 2,
             {0: 'Ein Spiegel wirft alles in eine Richtung zurück. Wohin strahlt ein Gas, das sich erwärmt hat?', 1: 'Energie wird nicht vernichtet. Wohin geht sie?'}),
        wahl('Frage 5', 'Warum kühlt der Boden in einer klaren Winternacht stärker ab als in einer bewölkten?', ['Wolken halten Wärmestrahlung zurück und strahlen zum Boden zurück.', 'Wolken lassen Wärmestrahlung leichter durch als klare Luft.', 'In klaren Nächten weht immer Wind.'], 0,
             {1: 'Wolken bestehen aus Wasser. Lässt Wasser Infrarot leicht durch?', 2: 'Es geht nicht um Wind. Woraus bestehen Wolken?'}),
    ]))


# ------------------------------------------------------------------ schreiben
for d in DREH:
    pfad = os.path.join(CLIPS, d['dateiname'] + '.json')
    if NUR and d['dateiname'] not in NUR:
        continue
    if os.path.exists(pfad) and not NEU:
        print('vorhanden, unverändert:', d['dateiname'])
        continue
    with open(pfad, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('geschrieben:', d['dateiname'], len(d['szenen']), 'Szenen')
