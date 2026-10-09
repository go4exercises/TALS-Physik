"""Erzeugt die zwölf Drehbücher des Leitprogramms Wellen (clips/p6-1-lp-*.json).

  python3 scripts/lp/wellen/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/wellen/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/wellen/clips.py --neu p6-1-lp-welle …   # nur diese

Dieses Skript ist die Quelle der Drehbücher (wie README.md sagt): Späte Korrekturen hier machen, nicht im
JSON — ein Lauf mit --neu überschreibt das JSON samt «dauer», «ein»/«aus» und Antwortbildern. Darum nach
jedem --neu die ganze Kette unten laufen lassen; erst build-clip-ton.py schreibt die gemessene Dauer wieder hinein.

Ablauf je Clip: clips.py → build-clip-ton.py → (Kontrollclips) build-clip-fragen-ton.py → antworten.py
(Antwortbilder der Kontrollclips) → scripts/lp/kinematik/anker.py (Elemente mit «_anker») →
scripts/lp/wellen/teilanker.py (Teile eines graf mit «_ein»/«_aus»/«_bahn»/«_bewegung»/«_grenzen») → build-clips.py.

Farben (Theme begreifbar-schlicht: 1 Bernstein, 2 Orange, 3 Grün, 4 Rot, 5 Tinte), wie im Leitprogramm:
  1 Bernstein  Welle und Auslenkung (Kurven, Seil, E-Feld)
  2 Orange     Licht der Sonne
  3 Grün       Ausbreitung, Front, Geschwindigkeit c
  4 Rot        Wärmestrahlung, Infrarot
  5 Tinte      Teilchen, markierte Punkte, Masslinien (λ, T), Achsen, B-Feld
Bilder: Aufnahmen der Simulationen (clips/bilder/p6-1-lp-*.jpg, Plan: aufnahme.json) und Skizzen als graf.
Zahlen im Sprechertext ausgeschrieben (CLAUDE.md). Alle Zahlen mit python3 nachgerechnet (Asserts unten, README).
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
    'themenbereich': 'Wellen · BM', 'lerngebiet': '6 · Einführung in andere Bereiche der Physik',
    'lektion': ['p6-1'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-08', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Wellen sehen', 'nachlauf': 2.6, 'probe': True,
}
JETZT = {'name': 'Jetzt du', 'layout': 'zentriert', 'oben': 200,
         'sprecher': 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
         'elemente': [{'typ': 'titel', 'text': 'Jetzt du', 'x': 150, 'y': 280, 'groesse': 86},
                      {'typ': 'notiz', 'text': 'Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.',
                       'x': 150, 'y': 430, 'groesse': 50, 'farbe': 'blau', 'ein': 0.6}]}
BER, ORA, GRU, ROT, TIN = 1, 2, 3, 4, 5
C = 3.00e8


# ------------------------------------------------------------------ Bausteine
def anker(e, a, versatz=None):
    if a:
        e['_anker'] = a
    if versatz:
        e['_versatz'] = versatz
    return e


def formel(t, y=300, g=46, a=None, ein=0.8, v=None):
    return anker({'typ': 'formel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'ein': ein}, a, v)


def rechnung(t, y=300, g=46, a=None, a_erg=None, trenn=None):
    """Rechnung, die um ihr Ergebnis wächst: zuerst Ansatz und Einsetzen (bis vor das letzte «=» bzw. «≈»),
    mit dem gesprochenen Ergebnis (a_erg) die ganze Zeile an derselben Stelle (HOWTO §15: Ergebnis mit dem Wort)."""
    k = t.rfind(trenn) if trenn else max(t.rfind(' = '), t.rfind(r' \approx '))
    teil = formel(t[:k], y, g, a)
    teil['_aus_anker'] = a_erg
    return [teil, formel(t, y, g, a_erg)]


def probe(vor, nach, y=560, g=36, a='Probe', a_erg=None):
    """Probe-Notiz in zwei Stufen: Ansatz der Probe mit «Probe», das Ergebnis erst mit dem gesprochenen Ergebnis."""
    teil = notiz(vor + ('@' if vor.count('@') % 2 else ''), y=y, g=g, a=a)   # offene Formel im Teilstück schliessen
    teil['_aus_anker'] = a_erg
    return [teil, notiz(vor + nach, y=y, g=g, a=a_erg)]


def notiz(t, y=460, farbe='tinte', g=42, a=None, ein=2.0, v=None):
    return anker({'typ': 'notiz', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'farbe': farbe, 'ein': ein}, a, v)


def titel(t, y=300, g=72):
    return {'typ': 'titel', 'text': t, 'x': 150, 'y': y, 'breite': 1640, 'groesse': g}


def bild(datei, a=None, ein=0.05, v=None, breite=None, y=190, x=None):
    breite = breite or (700 if '-em-' in datei else 840)   # Feldbilder sind hoch; die übrigen breit
    x = x or (1000 if breite == 700 else 990)
    return anker({'typ': 'bild', 'datei': 'bilder/' + datei, 'x': x, 'y': y, 'breite': breite, 'abstand': 0, 'anim': 'fade', 'ein': ein}, a, v)


def teilung(werte):
    return [x if isinstance(x, list) else [x, ('%g' % x).replace('-', '−')] for x in werte] or [[1e9, '']]


def graf(xb, yb, xt=(), yt=(), xname='', yname='', a=None, ein=0.05, achsen=True, v=None, y=175, hoehe=760, **kw):
    g = {'typ': 'graf', 'x': 1010, 'y': y, 'breite': 760, 'hoehe': hoehe, 'abstand': 0, 'anim': 'fade', 'ein': ein,
         'pfeile': achsen, 'xbereich': list(xb), 'ybereich': list(yb),
         'xteilung': teilung(xt), 'yteilung': teilung(yt), 'xname': xname, 'yname': yname}
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


def mass(x1, x2, y, text, ty=None, farbe=TIN, groesse=26, **kw):
    """Masslinie mit Spitzen an beiden Enden (λ, T), Text darüber; kw (_ein, _aus) gelten für alle Teile."""
    m = (x1 + x2) / 2
    st = [P((m, y), (x1, y), farbe, dicke=3, **kw), P((m, y), (x2, y), farbe, dicke=3, **kw)]
    tx = [T(m, y if ty is None else ty, text, farbe, groesse, **kw)]
    return st, tx


def welle(A, lam, xc, farbe=BER, von=None, bis=None, dicke=5, **kw):
    """Stehende Sinuskurve y = A·sin(2π/λ·(x − u)) mit einem Berg bei xc (u = xc − λ/4); als bewegte Kurve
    mit einem Stützpunkt, damit Marken mitlaufen und Klickfragen gehen."""
    b = 2 * math.pi / lam
    d = {'trig': 'sin', 'bewegung': [[0, A, r4(b), r4(xc - lam / 4), 0]], 'farbe': farbe, 'dicke': dicke}
    if von is not None:
        d['von'] = von
    if bis is not None:
        d['bis'] = bis
    d.update(kw)
    return d


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
EIN = 'Einführungsclip des Leitprogramms Wellen, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Wellen, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'


def merke(sprecher, f, n):
    return sz('Merke', sprecher, titel('Zum Mitnehmen', y=260, g=76), formel(f, y=420, g=46, ein=0.4), notiz(n, y=570, ein=1.2))


def seil_skizze(ende=6.0, **kw):
    """Seil in Ruhe (Fenster 0…10 waagrecht = 0…6 m), Hand links, Wand rechts."""
    return [S((0.6, 5), (9.4, 5), TIN, dicke=2, gestrichelt=True)]


# ================================================================== Kapitel 1: Schwingung und Welle
# Problem: Hand 5-mal in 4.0 s → T = 0.80 s, f = 1.25 Hz; Band 3.6 m nach 2.4 s → c = 1.5 m/s; λ = c·T = 1.2 m
assert abs(4.0 / 5 - 0.8) < 1e-12 and abs(5 / 4.0 - 1.25) < 1e-12 and abs(3.6 / 2.4 - 1.5) < 1e-12 and abs(1.5 * 0.8 - 1.2) < 1e-12
LP1 = 1.2                     # λ in m (Problem)
B1 = 2 * math.pi / LP1
DREH.append(dict(KOPF, titel='Wellen sehen: aus der Schwingung wird eine Welle', dateiname='p6-1-lp-welle',
    kurzbeschrieb='Wie aus der Schwingung einer Hand über gekoppelte, verzögert mitschwingende Teilchen eine Welle wird, die Energie, aber keine Materie transportiert; Quer- und Längswelle — und ein vorgerechnetes Problem: Periode, Frequenz und Geschwindigkeit einer Seilwelle.',
    schlagworte=['Schwingung', 'Welle', 'Periode', 'Frequenz', 'Ausbreitungsgeschwindigkeit', 'Querwelle', 'Längswelle'], _probe=EIN % 1,
    szenen=[
        sz('Seil', 'Du hältst das Ende eines langen Seils und bewegst die Hand auf und ab. Eine Welle läuft das Seil entlang bis zur Wand. Was läuft da eigentlich — das Seil?',
           titel('Was läuft da?', g=66),
           notiz('Hand bewegt sich auf und ab|— die Welle läuft weg', y=460, a='Du hältst'),
           graf((-0.4, 6.4), (-1.6, 1.6), achsen=False,
                strecken=[S((0, 0), (6.0, 0), TIN, dicke=2, gestrichelt=True), S((6.05, -1.2), (6.05, 1.2), TIN, dicke=8)],
                kurven=[{'trig': 'sin', 'bewegung': [[0.3, -0.7, r4(B1), 0, 0], [5.0, -0.7, r4(B1), 6.0, 0]], 'grenzen': [[0.3, 0, 0], [5.0, 0, 6.0]],
                         'farbe': BER, 'dicke': 6, '_bewegung': [['Du hältst', 0.3, -0.7, r4(B1), 0, 0], ['bis zur Wand', 0.6, -0.7, r4(B1), 6.0, 0]],
                         '_grenzen': [['Du hältst', 0.3, 0, 0], ['bis zur Wand', 0.6, 0, 6.0]]}],
                texte=[T(0, -1.45, 'Hand', TIN, 26), T(6.0, -1.45, 'Wand', TIN, 26), T(3.0, 1.35, '?', TIN, 44, _ein='Was läuft da')])),
        sz('Schwingung', 'Am Anfang steht eine Schwingung: Die Hand bewegt sich periodisch um eine Ruhelage. Die grösste Auslenkung heisst Amplitude. Die Dauer einer ganzen Schwingung ist die Periode T. Die Frequenz f zählt die Schwingungen pro Sekunde: f gleich eins durch T, gemessen in Hertz.',
           notiz('Schwingung: periodisch|um eine Ruhelage', y=280, a='Am Anfang'),
           notiz('Amplitude @A@: grösste Auslenkung', y=430, a='Die grösste Auslenkung'),
           notiz('Periode @T@: Dauer einer Schwingung', y=500, a='Die Dauer'),
           formel(r'f = \frac{1}{T}, \quad [f] = \text{Hz} = \frac{1}{\text{s}}', y=600, g=44, a='f gleich'),
           graf((-0.25, 3.3), (-28, 28), [1, 2, 3], [-20, 20], 't [s]', 'y [cm]',
                kurven=[{'trig': 'sin', 'bewegung': [[0, 20, r4(2 * math.pi / 1.0), 0, 0]], 'grenzen': [[0.3, 0, 0], [4.0, 0, 3.0]],
                         'farbe': BER, 'dicke': 6, 'laeufer': {'bahn': [[0.3, 0], [4.0, 3.0]], 'farbe': TIN, '_bahn': [['Am Anfang', 0.2, 0], ['um eine Ruhelage', 0.8, 3.0]]},
                         '_grenzen': [['Am Anfang', 0.2, 0, 0], ['um eine Ruhelage', 0.8, 0, 3.0]]}],
                strecken=[S((0, 0), (3.2, 0), TIN, dicke=2, gestrichelt=True)]
                + mass(0.25, 1.25, 24, 'T', ty=25.5, _ein='Die Dauer')[0]
                + [P((0.25, 0), (0.25, 20), TIN, dicke=3, _ein='Die grösste Auslenkung')],
                texte=mass(0.25, 1.25, 24, 'T', ty=25.5, _ein='Die Dauer')[1]
                + [T(0.33, 9, 'A', TIN, 30, 'start', _ein='Die grösste Auslenkung'), T(3.15, -25.5, 'Ruhelage', TIN, 22, 'end')])),
        sz('Kopplung', 'Die Teile des Seils sind gekoppelt: Jedes zieht seinen Nachbarn mit. Der Nachbar macht dieselbe Bewegung, aber etwas später. Genau diese Verzögerung macht aus der Schwingung eine laufende Welle.',
           notiz('gekoppelt: jedes Teilchen zieht|seinen Nachbarn mit', y=300, a='Die Teile des Seils'),
           notiz('derselbe Takt, aber verzögert', y=460, a='Der Nachbar macht'),
           notiz('→ eine laufende Welle', y=560, a='Genau diese Verzögerung', farbe='gruen'),
           bild('p6-1-lp-welle-k1.jpg', a='Die Teile des Seils'),
           bild('p6-1-lp-welle-k2.jpg', a='Der Nachbar macht'),
           bild('p6-1-lp-welle-k3.jpg', a='Genau diese Verzögerung')),
        sz('Energie', 'Das markierte Teilchen P schwingt nur auf und ab und kehrt immer wieder an seinen Platz zurück. Weiter läuft die Form der Welle, und mit ihr die Energie. Transportiert wird Energie, keine Materie.',
           notiz('P schwingt nur um seinen Platz', y=300, a='Das markierte Teilchen'),
           notiz('Energie läuft weiter,|keine Materie', y=440, a='Transportiert wird'),
           graf((-0.4, 6.4), (-1.6, 1.6), achsen=False,
                strecken=[S((0, 0), (6.0, 0), TIN, dicke=2, gestrichelt=True), S((3.0, -1.1), (3.0, 1.1), TIN, dicke=2, gestrichelt=True)],
                kurven=[{'trig': 'sin', 'bewegung': [[0.3, 0.8, r4(B1), 0, 0], [6.0, 0.8, r4(B1), 2 * LP1, 0]], 'farbe': BER, 'dicke': 6,
                         '_bewegung': [['Das markierte Teilchen', 0.4, 0.8, r4(B1), 0, 0], ['Transportiert wird', 0.0, 0.8, r4(B1), 2 * LP1, 0]],
                         'marken': [{'x': 3.0, 'text': 'P', 'farbe': TIN}]}],
                texte=[T(3.0, -1.45, 'Platz von P', TIN, 24), T(5.6, 1.35, 'Welle läuft →', GRU, 26, 'end', _ein='Weiter läuft die Form')])),
        sz('Quer und längs', 'Schwingen die Teilchen quer zur Ausbreitung, heisst die Welle Querwelle, wie beim Seil. Schwingen sie in Ausbreitungsrichtung, rücken sie stellenweise zusammen und auseinander: eine Längswelle. So läuft Schall durch die Luft.',
           notiz('Querwelle: quer zur Ausbreitung', y=300, a='Schwingen die Teilchen quer'),
           notiz('Längswelle: in Ausbreitungsrichtung,|Verdichtungen und Verdünnungen', y=440, a='Schwingen sie in Ausbreitungsrichtung'),
           notiz('Schall in Luft: längs', y=600, a='So läuft Schall'),
           bild('p6-1-lp-welle-quer.jpg', a='Schwingen die Teilchen quer'),
           bild('p6-1-lp-welle-laengs.jpg', a='Schwingen sie in Ausbreitungsrichtung')),
        sz('Problem Seil', 'Jetzt ein ganzes Problem. Die Hand schwingt fünfmal in vier Sekunden auf und ab. Ein Stoffband sitzt drei Komma sechs Meter weiter am Seil. Es beginnt zwei Komma vier Sekunden nach der Hand zu schwingen. Wie gross sind Periode und Frequenz? Und wie schnell läuft die Welle?',
           notiz('Hand: 5 Schwingungen in 4.0 s', y=300, a='Die Hand schwingt'),
           notiz('Band: 3.6 m weiter', y=370, a='Ein Stoffband'),
           notiz('beginnt 2.4 s später', y=440, a='Es beginnt'),
           notiz('gesucht: @T@, @f@ und @c@', y=550, a='Wie gross sind'),
           graf((-0.4, 6.4), (-1.6, 1.6), achsen=False,
                strecken=[S((0, 0), (6.0, 0), BER, dicke=4), S((3.6, -0.35), (3.6, 0.35), TIN, dicke=10, _ein='Ein Stoffband')]
                + mass(0, 3.6, -0.9, '3.6 m', ty=-1.3, _ein='Ein Stoffband')[0],
                texte=mass(0, 3.6, -0.9, '3.6 m', ty=-1.3, _ein='Ein Stoffband')[1]
                + [T(0, 0.6, 'Hand', TIN, 26), T(3.6, 0.6, 'Band', TIN, 26, _ein='Ein Stoffband')])),
        sz('Vorgehen Seil', 'Die Periode ist die Zeit für eine Schwingung, die Frequenz ihr Kehrwert. Für die Geschwindigkeit teilst du den Weg der Störung bis zum Band durch ihre Laufzeit.',
           formel(r'T = \frac{t}{n}', y=290, g=46, a='Die Periode'),
           formel(r'f = \frac{1}{T}', y=400, g=46, a='die Frequenz ihr'),
           formel(r'c = \frac{s}{t}', y=510, g=46, a='Für die Geschwindigkeit'),
           graf((-0.4, 6.4), (-1.6, 1.6), achsen=False,
                strecken=[S((0, 0), (6.0, 0), BER, dicke=4), S((3.6, -0.35), (3.6, 0.35), TIN, dicke=10),
                          P((0.2, 0.75), (3.5, 0.75), GRU, dicke=5, _ein='Für die Geschwindigkeit')],
                texte=[T(1.8, 1.1, 'Störung: Weg in der Laufzeit', GRU, 24, _ein='Für die Geschwindigkeit'), T(0, -0.6, 'Hand', TIN, 26), T(3.6, -0.6, 'Band', TIN, 26)])),
        sz('Lösung Seil', 'Eine Schwingung dauert vier Sekunden durch fünf, also null Komma acht Sekunden. Die Frequenz ist eins durch null Komma acht Sekunden, eins Komma zwei fünf Hertz. Die Störung braucht für drei Komma sechs Meter zwei Komma vier Sekunden: c gleich drei Komma sechs Meter durch zwei Komma vier Sekunden, eins Komma fünf Meter pro Sekunde. Probe: In zwei Komma vier Sekunden kommt die Welle eins Komma fünf mal zwei Komma vier, also drei Komma sechs Meter weit.',
           *rechnung(r'T = \frac{4.0\;\text{s}}{5} = 0.80\;\text{s}', y=240, g=38, a='Eine Schwingung dauert', a_erg='also null Komma acht Sekunden'),
           *rechnung(r'f = \frac{1}{T} = \frac{1}{0.80\;\text{s}} = 1.25\;\text{Hz}', y=350, g=38, a='Die Frequenz ist', a_erg='eins Komma zwei fünf Hertz'),
           *rechnung(r'c = \frac{s}{t} = \frac{3.6\;\text{m}}{2.4\;\text{s}} = 1.5\;\text{m/s}', y=470, g=38, a='c gleich', a_erg='eins Komma fünf Meter pro Sekunde'),
           *probe('Probe: @1.5\\;\\text{m/s} \\cdot 2.4\\;\\text{s}', ' = 3.6\\;\\text{m}@', y=600, g=38, a_erg='also drei Komma sechs Meter weit'),
           graf((-0.4, 6.4), (-1.6, 1.6), achsen=False,
                strecken=[S((0, 0), (6.0, 0), TIN, dicke=2, gestrichelt=True), S((3.6, -0.35), (3.6, 0.35), TIN, dicke=10)],
                kurven=[{'trig': 'sin', 'bewegung': [[0.5, -0.6, r4(B1), 0, 0], [3.0, -0.6, r4(B1), 3.6, 0]], 'grenzen': [[0.5, 0, 0], [3.0, 0, 3.6]],
                         'farbe': BER, 'dicke': 6,
                         '_bewegung': [['Die Störung braucht', 0.2, -0.6, r4(B1), 0, 0], ['c gleich', 0.0, -0.6, r4(B1), 3.6, 0]],
                         '_grenzen': [['Die Störung braucht', 0.2, 0, 0], ['c gleich', 0.0, 0, 3.6]]}],
                texte=[T(0, -0.9, 'Hand', TIN, 26), T(3.6, -0.9, 'Band', TIN, 26), T(1.8, 1.2, 'c = 1.5 m/s', GRU, 28, _ein='eins Komma fünf Meter pro Sekunde')])),
        merke('Zum Mitnehmen: Eine Welle ist eine Schwingung, die über gekoppelte Teilchen weitergegeben wird, jedes etwas später. Sie transportiert Energie, keine Materie. Ob quer oder längs, entscheidet die Schwingungsrichtung der Teilchen.',
              r'f = \frac{1}{T}, \qquad c = \frac{s}{t}', 'Welle: weitergegebene Schwingung|Energie, keine Materie|quer oder längs'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Seil', 'Wie bestimmst du die Geschwindigkeit der Welle?', ['Wie oft die Hand pro Sekunde schwingt', 'Weg der Störung bis zum Band durch ihre Laufzeit', 'Wie hoch die Hand ausschlägt'], 1,
                 {0: 'Das ist die Frequenz — sie sagt, wie oft, nicht wie schnell die Störung vorankommt.', 2: 'Das ist die Amplitude. Wie weit kommt die Störung in welcher Zeit?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 1
assert abs(6.0 / 1.5 - 4.0) < 1e-12 and abs(12 / 60 - 0.2) < 1e-12
DREH.append(dict(KOPF, titel='Wellen sehen: Kontrollfragen zur Entstehung einer Welle', dateiname='p6-1-lp-kontrolle-welle',
    kurzbeschrieb='Fünf Fragen: was eine Stadionwelle transportiert, ob eine anfahrende Autokolonne eine Quer- oder Längswelle ist, die Geschwindigkeit eines Stosses, die Frequenz eines Boots und was ein Wellenberg tut, wenn die Hand aufhört.',
    schlagworte=['Welle', 'Energie', 'Längswelle', 'Frequenz', 'Ausbreitungsgeschwindigkeit', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Jeder Zuschauer bleibt auf seinem Platz und steht auf, wenn sein Nachbar aufsteht. Weiter läuft nur das Muster der Bewegung, niemand wandert mit. Anders als beim Seil steht hier jeder aus eigener Kraft auf: Die Energie gibt nicht der Nachbar weiter.',
           notiz('Jeder bleibt auf seinem Platz;|weiter läuft nur das Muster', y=320, ein=1.0)),
        sz('Frage 2', 'Die Autos rollen nach vorn, die Anfahrwelle läuft nach hinten durch die Kolonne. Beides liegt auf derselben Linie, der Strasse. Darum ist es eine Längswelle, mit Verdichtungen und Verdünnungen.',
           notiz('Autos und Welle auf derselben|Linie: längs', y=320, ein=1.0)),
        sz('Frage 3', 'Geschwindigkeit ist Weg durch Zeit: sechs Meter durch eins Komma fünf Sekunden, vier Meter pro Sekunde.',
           formel(r'c = \frac{s}{t} = \frac{6.0\;\text{m}}{1.5\;\text{s}} = 4.0\;\text{m/s}', y=320, g=44, ein=1.0)),
        sz('Frage 4', 'Zwölf Schwingungen in sechzig Sekunden: Die Frequenz ist zwölf durch sechzig Sekunden, null Komma zwei Hertz. Eine Schwingung dauert fünf Sekunden.',
           formel(r'f = \frac{12}{60\;\text{s}} = 0.20\;\text{Hz}', y=300, g=46, ein=1.0),
           formel(r'T = \frac{1}{f} = \frac{1}{0.20\;\text{Hz}} = 5.0\;\text{s}', y=420, g=46, ein=1.0)),
        sz('Frage 5', 'Die Teilchen weiter vorne sind schon in Bewegung und geben sie weiter, auch ohne die Hand. Der Berg läuft weiter bis ans Ende; hinter ihm bleibt das Seil in Ruhe.',
           notiz('Der Berg läuft weiter;|dahinter bleibt das Seil ruhig', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Im Stadion stehen die Zuschauer der Reihe nach auf und setzen sich wieder. Eine Welle läuft ums Stadion. Was wird transportiert?',
             ['Nur die Bewegung: Jeder bleibt an seinem Platz.', 'Die Zuschauer wandern mit der Welle mit.', 'Gar nichts, weil niemand den Platz wechselt.'], 0,
             {1: 'Bleibt nicht jeder auf seinem Sitz? Was wandert dann ums Stadion?', 2: 'Etwas läuft ja ums Stadion — was ist es, wenn nicht die Menschen?'}),
        wahl('Frage 2', 'An einer Ampel fährt eine Autokolonne an: Ein Auto nach dem anderen rollt los. Ist diese Welle eine Quer- oder eine Längswelle?', ['Querwelle', 'Längswelle'], 1,
             {0: 'In welche Richtung bewegt sich jedes Auto — quer zur Strasse oder der Strasse entlang?'}),
        wahl('Frage 3', 'Ein Stoss läuft auf einer gespannten Wäscheleine 6.0 m weit in 1.5 s. Wie schnell läuft die Welle?', ['0.25 m/s', '9.0 m/s', '4.0 m/s'], 2,
             {0: 'Umgekehrt geteilt: Geschwindigkeit ist Weg durch Zeit.', 1: 'Weg und Zeit multipliziert? Geschwindigkeit ist Weg pro Zeit.'},
             sprich='Ein Stoss läuft auf einer gespannten Wäscheleine sechs Meter weit in eins Komma fünf Sekunden. Wie schnell läuft die Welle?'),
        wahl('Frage 4', 'Ein Boot hebt und senkt sich 12-mal pro Minute. Wie gross ist die Frequenz?', ['5.0 Hz', '12 Hz', '0.20 Hz'], 2,
             {0: 'Sechzig durch zwölf ergibt die Dauer einer Schwingung. Gefragt ist die Anzahl pro Sekunde.', 1: 'Die zwölf Schwingungen dauern eine Minute, nicht eine Sekunde.'},
             sprich='Ein Boot hebt und senkt sich zwölfmal pro Minute. Wie gross ist die Frequenz?'),
        wahl('Frage 5', 'Die Hand am Seil hört plötzlich auf zu schwingen. Was geschieht mit dem Wellenberg, der schon unterwegs ist?', ['Er bleibt sofort stehen.', 'Er läuft weiter bis ans Ende des Seils.', 'Er läuft zur Hand zurück.'], 1,
             {0: 'Die Teilchen weiter vorne sind ja schon in Bewegung. Brauchen sie die Hand noch?', 2: 'Wer gibt die Bewegung weiter: die Hand oder die Nachbarn?'}),
    ]))

# ================================================================== Kapitel 2: Momentbild und Zeitdiagramm
# Begriffe: λ = 1.6 m, T = 2.0 s → c = 0.80 m/s; Problem Wellenbad: λ = 5.0 m, T = 2.0 s → f = 0.50 Hz, c = 2.5 m/s
# (Wellenbad rund 0.9 m tief nach ω² = g·k·tanh(k·h); λ = 5.0 m < g·T²/2π = 6.2 m; Amplitude 10 cm)
assert abs(1.6 / 2.0 - 0.8) < 1e-12 and abs(1 / 2.0 - 0.5) < 1e-12 and abs(5.0 / 2.0 - 2.5) < 1e-12 and abs(5.0 * 0.5 - 2.5) < 1e-12 and 5.0 < 9.81 * 2.0 ** 2 / (2 * math.pi) and abs(math.atanh((2 * math.pi / 2.0) ** 2 / (9.81 * 2 * math.pi / 5.0)) / (2 * math.pi / 5.0) - 0.875) < 0.01
LB, TB = 1.6, 2.0


def momentbild(y=175, hoehe=360, kurve=None, **kw):
    return graf((-0.35, 5.3), (-6.5, 6.5), [1, 2, 3, 4, 5], [-4, 4], 's [m]', 'y [cm]', y=y, hoehe=hoehe,
                kurven=[kurve or welle(4, LB, 0.4, von=0, bis=5.0)], **kw)


def zeitdiagramm(y=575, hoehe=360, kurve=None, **kw):
    return graf((-0.45, 6.6), (-6.5, 6.5), [1, 2, 3, 4, 5, 6], [-4, 4], 't [s]', 'y [cm]', y=y, hoehe=hoehe,
                kurven=[kurve or welle(4, TB, 0.5, von=0, bis=6.2)], **kw)


m2_s, m2_t = mass(0.4, 2.0, 5.2, 'λ = 1.6 m', ty=5.9, _ein='Der Abstand')
XT_BAD = [[2.5, ''], [5, '5'], [7.5, ''], [10, '10'], [12.5, ''], [15, '15']]
TT_BAD = [[x / 2, ('%g' % (x / 2)) if x % 2 == 0 else ''] for x in range(1, 17)]
z2_s, z2_t = mass(0.5, 2.5, 5.2, 'T = 2.0 s', ty=5.9, _ein='Der Abstand')
DREH.append(dict(KOPF, titel='Wellen sehen: Momentbild und Zeitdiagramm', dateiname='p6-1-lp-diagramme',
    kurzbeschrieb='Dieselbe Welle als Momentbild y(s) und als Zeitdiagramm y(t): Wellenlänge und Periode ablesen, die Phasengeschwindigkeit c = λ/T — und ein vorgerechnetes Problem: die Wellen eines Wellenbads.',
    schlagworte=['Momentbild', 'Zeitdiagramm', 'Wellenlänge', 'Periode', 'Phasengeschwindigkeit'], _probe=EIN % 2,
    szenen=[
        sz('Zwei Bilder', 'Eine Welle läuft über ein Seil. Man kann sie auf zwei Arten zeichnen: als Foto des ganzen Seils, oder als Aufzeichnung eines einzigen Punkts über die Zeit. Beide Bilder sehen ähnlich aus — und zeigen doch etwas ganz anderes.',
           titel('Zwei Bilder einer Welle', g=62),
           notiz('Foto des ganzen Seils', y=440, a='als Foto'),
           notiz('ein Punkt über die Zeit', y=520, a='oder als Aufzeichnung'),
           momentbild(a='als Foto'),
           zeitdiagramm(a='oder als Aufzeichnung')),
        sz('Momentbild', 'Im Momentbild steht die Zeit still. Auf der Achse steht der Ort s in Metern. Der Abstand von einem Berg zum nächsten ist die Wellenlänge Lambda, hier eins Komma sechs Meter.',
           notiz('Momentbild @y(s)@:|die Zeit steht still', y=300, a='Im Momentbild'),
           notiz('Achse: Ort @s@ in m', y=440, a='Auf der Achse'),
           notiz('Berg zu Berg: Wellenlänge @\\lambda@', y=540, a='Der Abstand'),
           momentbild(strecken=m2_s, texte=m2_t)),
        sz('Zeitdiagramm', 'Im Zeitdiagramm steht der Ort fest. Man verfolgt einen einzigen Punkt, und auf der Achse steht die Zeit t in Sekunden. Der Abstand von einem Maximum zum nächsten ist die Periode T, hier zwei Sekunden.',
           notiz('Zeitdiagramm @y(t)@:|der Ort steht fest', y=300, a='Im Zeitdiagramm'),
           notiz('Achse: Zeit @t@ in s', y=440, a='auf der Achse steht die Zeit'),
           notiz('Maximum zu Maximum: Periode @T@', y=540, a='Der Abstand'),
           zeitdiagramm(y=175, hoehe=360, kurve=dict(welle(4, TB, 0.5, von=0, bis=6.2), grenzen=[[0.3, 0, 0], [3.0, 0, 6.2]],
                                                     laeufer={'bahn': [[0.3, 0], [3.0, 6.2]], 'farbe': TIN, '_bahn': [['Man verfolgt', 0.0, 0], ['auf der Achse steht die Zeit', 0.6, 6.2]]},
                                                     _grenzen=[['Man verfolgt', 0.0, 0, 0], ['auf der Achse steht die Zeit', 0.6, 0, 6.2]]),
                        strecken=z2_s, texte=z2_t)),
        sz('Phasengeschwindigkeit', 'In einer Periode rückt jeder Berg genau um eine Wellenlänge weiter. Darum ist die Phasengeschwindigkeit c gleich Lambda durch T, oder Lambda mal f. Hier: eins Komma sechs Meter in zwei Sekunden, null Komma acht Meter pro Sekunde.',
           notiz('in einer Periode:|ein Berg rückt um @\\lambda@ weiter', y=290, a='In einer Periode'),
           formel(r'c = \frac{\lambda}{T} = \lambda \cdot f', y=440, g=50, a='Darum ist'),
           *rechnung(r'c = \frac{1.6\;\text{m}}{2.0\;\text{s}} = 0.80\;\text{m/s}', y=560, g=40, a='Hier:', a_erg='null Komma acht Meter pro Sekunde'),
           momentbild(kurve=dict(welle(4, LB, 0.4, von=0, bis=5.0), bewegung=[[0.5, 4, r4(2 * math.pi / LB), 0, 0], [3.0, 4, r4(2 * math.pi / LB), LB, 0]],
                                 _bewegung=[['In einer Periode', 0.3, 4, r4(2 * math.pi / LB), 0, 0], ['Darum ist', -0.3, 4, r4(2 * math.pi / LB), LB, 0]],
                                 laeufer={'bahn': [[0.5, 2.0], [3.0, 3.6]], 'farbe': TIN, '_bahn': [['In einer Periode', 0.3, 2.0], ['Darum ist', -0.3, 3.6]]}),
                      strecken=[S((2.0, 0), (2.0, 4.0), TIN, dicke=2, gestrichelt=True)] + mass(2.0, 3.6, -5.3, '', _ein='Darum ist')[0],
                      texte=[T(2.0, 4.9, 'Berg vorher', TIN, 22)] + [T(3.75, -5.65, 'λ in T', TIN, 26, 'start', _ein='Darum ist')])),
        sz('Problem Wellenbad', 'Jetzt ein ganzes Problem. In einem Wellenbad zeigt ein Foto der Wasseroberfläche die Wellenberge. Eine Boje wird gefilmt; ihr Zeitdiagramm steht darunter. Wie gross sind Wellenlänge, Periode, Frequenz und Phasengeschwindigkeit?',
           notiz('Foto: Momentbild', y=300, a='zeigt ein Foto'),
           notiz('Boje: Zeitdiagramm', y=370, a='Eine Boje'),
           notiz('gesucht: @\\lambda@, @T@, @f@, @c@', y=480, a='Wie gross sind'),
           graf((-1.1, 16.2), (-18, 18), XT_BAD, [-10, 10], 's [m]', 'y [cm]', y=175, hoehe=360, a='zeigt ein Foto',
                kurven=[welle(10, 5.0, 2.5, von=0, bis=15.4)]),
           graf((-0.55, 8.1), (-18, 18), TT_BAD, [-10, 10], 't [s]', 'y [cm]', y=575, hoehe=360, a='Eine Boje',
                kurven=[welle(10, 2.0, 1.0, von=0, bis=7.8)])),
        sz('Vorgehen Wellenbad', 'Lies die Wellenlänge dort ab, wo der Ort auf der Achse steht, und die Periode dort, wo die Zeit steht. Daraus folgen Frequenz und Geschwindigkeit.',
           formel(r'\lambda: \text{ im Momentbild}', y=290, g=42, a='Lies die Wellenlänge'),
           formel(r'T: \text{ im Zeitdiagramm}', y=390, g=42, a='und die Periode'),
           formel(r'f = \frac{1}{T}, \quad c = \frac{\lambda}{T}', y=500, g=42, a='Daraus folgen'),
           graf((-1.1, 16.2), (-18, 18), XT_BAD, [-10, 10], 's [m]', 'y [cm]', y=175, hoehe=360, kurven=[welle(10, 5.0, 2.5, von=0, bis=15.4)]),
           graf((-0.55, 8.1), (-18, 18), TT_BAD, [-10, 10], 't [s]', 'y [cm]', y=575, hoehe=360, kurven=[welle(10, 2.0, 1.0, von=0, bis=7.8)])),
        sz('Lösung Wellenbad', 'Im Momentbild liegen die Berge fünf Meter auseinander: Lambda gleich fünf Meter. Im Zeitdiagramm liegen die Maxima zwei Sekunden auseinander: T gleich zwei Sekunden. Die Frequenz ist eins durch T, null Komma fünf Hertz. c gleich Lambda durch T, fünf Meter durch zwei Sekunden, zwei Komma fünf Meter pro Sekunde. Probe: Lambda mal f, fünf Meter mal null Komma fünf Hertz, gibt ebenfalls zwei Komma fünf Meter pro Sekunde.',
           *rechnung(r'\lambda = 5.0\;\text{m}, \quad T = 2.0\;\text{s}', y=240, g=38, a='Lambda gleich fünf Meter', a_erg='T gleich zwei Sekunden', trenn=','),
           *rechnung(r'f = \frac{1}{T} = \frac{1}{2.0\;\text{s}} = 0.50\;\text{Hz}', y=340, g=38, a='Die Frequenz ist', a_erg='null Komma fünf Hertz'),
           *rechnung(r'c = \frac{\lambda}{T} = \frac{5.0\;\text{m}}{2.0\;\text{s}} = 2.5\;\text{m/s}', y=460, g=38, a='c gleich', a_erg='zwei Komma fünf Meter pro Sekunde'),
           *probe('Probe: @5.0\\;\\text{m} \\cdot 0.50\\;\\text{Hz}', ' = 2.5\\;\\text{m/s}@', y=590, g=36, a_erg='gibt ebenfalls zwei Komma fünf Meter pro Sekunde'),
           graf((-1.1, 16.2), (-18, 18), XT_BAD, [-10, 10], 's [m]', 'y [cm]', y=175, hoehe=360,
                kurven=[welle(10, 5.0, 2.5, von=0, bis=15.4)],
                strecken=mass(2.5, 7.5, 14, 'λ = 5.0 m', ty=16, _ein='Lambda gleich fünf')[0], texte=mass(2.5, 7.5, 14, 'λ = 5.0 m', ty=16, _ein='Lambda gleich fünf')[1]),
           graf((-0.55, 8.1), (-18, 18), TT_BAD, [-10, 10], 't [s]', 'y [cm]', y=575, hoehe=360,
                kurven=[welle(10, 2.0, 1.0, von=0, bis=7.8)],
                strecken=mass(1.0, 3.0, 14, 'T = 2.0 s', ty=16, _ein='T gleich zwei Sekunden')[0], texte=mass(1.0, 3.0, 14, 'T = 2.0 s', ty=16, _ein='T gleich zwei Sekunden')[1])),
        merke('Zum Mitnehmen: Die Wellenlänge liest man im Momentbild ab, die Periode im Zeitdiagramm. Zuerst die Achse lesen: Ort oder Zeit? Und die Phasengeschwindigkeit ist Lambda durch T.',
              r'c = \frac{\lambda}{T} = \lambda \cdot f', 'Momentbild: @\\lambda@ in m|Zeitdiagramm: @T@ in s'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Wellenbad', 'Woraus liest du die Wellenlänge ab?', ['aus dem Zeitdiagramm: Abstand zweier Maxima', 'aus dem Momentbild: Abstand zweier Berge', 'aus der Höhe der Berge'], 1,
                 {0: 'Was steht auf der Achse des Zeitdiagramms — Meter oder Sekunden?', 2: 'Die Höhe ist die Amplitude. Die Wellenlänge ist ein Abstand entlang der Welle.'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 2
# F1 Klick: Berge bei 1.0, 2.5, 4.0 m (λ = 1.5 m); F2: Maxima bei 1, 4, 7 s (T = 3.0 s); F3: 0.60 m / 0.25 s = 2.4 m/s; F5: c = 3.0 m/s, f = 4.0 Hz
assert abs(0.60 / 0.25 - 2.4) < 1e-12 and abs((1.5 / 0.5) / 0.75 - 4.0) < 1e-12
DREH.append(dict(KOPF, titel='Wellen sehen: Kontrollfragen zu Momentbild und Zeitdiagramm', dateiname='p6-1-lp-kontrolle-diagramme',
    kurzbeschrieb='Fünf Fragen: den nächsten Wellenberg antippen, die Periode einer Boje ablesen, die Phasengeschwindigkeit aus λ und T, ein verwechseltes Diagramm und die Frequenz aus dem Lauf eines Bergs.',
    schlagworte=['Momentbild', 'Zeitdiagramm', 'Wellenlänge', 'Periode', 'Phasengeschwindigkeit', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Eine Wellenlänge weiter rechts liegt der nächste Berg, bei zwei Komma fünf Metern. Das Tal dazwischen ist nur eine halbe Wellenlänge entfernt.',
           notiz('nächster Berg: eine Wellenlänge|weiter, bei 2.5 m', y=320, ein=1.0),
           graf((-0.35, 6.3), (-6.5, 6.5), [1, 2, 3, 4, 5, 6], [-4, 4], 's [m]', 'y [cm]', y=175, hoehe=420, tippbar=True,
                kurven=[welle(4, 1.5, 1.0, von=0, bis=6.0)],
                punkte=[{'x': 1.0, 'y': 4, 'farbe': TIN, 'beschriftung': 'markierter Berg', 'beschriftung_bei': [1.0, 5.4]}])),
        sz('Frage 2', 'Von einem Maximum zum nächsten vergehen drei Sekunden: von einer zu vier, von vier zu sieben Sekunden. Die Periode ist drei Sekunden.',
           notiz('Maximum zu Maximum: @T = 3.0\\;\\text{s}@', y=320, ein=1.0),
           graf((-0.6, 8.6), (-60, 60), [2, 4, 6, 8], [-40, 40], 't [s]', 'y [cm]', y=175, hoehe=420,
                kurven=[welle(40, 3.0, 1.0, von=0, bis=8.3)])),
        sz('Frage 3', 'Phasengeschwindigkeit: Wellenlänge durch Periode, null Komma sechs Meter durch null Komma zwei fünf Sekunden, zwei Komma vier Meter pro Sekunde.',
           formel(r'c = \frac{\lambda}{T} = \frac{0.60\;\text{m}}{0.25\;\text{s}} = 2.4\;\text{m/s}', y=320, g=42, ein=1.0)),
        sz('Frage 4', 'Im Zeitdiagramm steht die Zeit auf der Achse. Zwei Maxima im Abstand von null Komma vier Sekunden geben die Periode, keine Wellenlänge. Eine Zeit kann keine Länge sein.',
           notiz('Zeitdiagramm: Abstand der Maxima|ist die Periode, eine Zeit', y=320, ein=1.0)),
        sz('Frage 5', 'Der Berg kommt in null Komma fünf Sekunden eins Komma fünf Meter weit: c gleich drei Meter pro Sekunde. Die Frequenz ist c durch Lambda, drei durch null Komma sieben fünf, vier Hertz.',
           formel(r'c = \frac{1.5\;\text{m}}{0.5\;\text{s}} = 3.0\;\text{m/s}', y=290, g=42, ein=1.0),
           formel(r'f = \frac{c}{\lambda} = \frac{3.0\;\text{m/s}}{0.75\;\text{m}} = 4.0\;\text{Hz}', y=420, g=42, ein=1.0)),
    ],
    fragen=[
        {'szene': 'Frage 1', 'bei': 0.3, 'typ': 'klick', 'text': 'Das Momentbild zeigt ein Seil. Tipp den Wellenberg an, der genau eine Wellenlänge rechts vom markierten Berg liegt — oder gib seine Lage ein.',
         'sprich': 'Das Momentbild zeigt ein Seil. Tipp den Wellenberg an, der genau eine Wellenlänge rechts vom markierten Berg liegt, oder gib seine Lage ein.',
         'ziel': [2.5, 4], 'toleranz': [0.3, 1.5], 'eingabe': ['s in m', 'y in cm'], 'richtig_text': 'Getroffen.',
         'fallen': [{'bei': [1.75, -4], 'text': 'Das ist ein Tal, eine halbe Wellenlänge weiter. Gesucht ist der nächste Berg.', 'sprich': 'Das ist ein Tal, eine halbe Wellenlänge weiter. Gesucht ist der nächste Berg.'},
                    {'bei': [4.0, 4], 'text': 'Das sind zwei Wellenlängen. Dazwischen liegt noch ein Berg.', 'sprich': 'Das sind zwei Wellenlängen. Dazwischen liegt noch ein Berg.'}],
         'falsch_text': 'Nicht ganz. Von Berg zu Berg ist eine Wellenlänge.', 'falsch_sprich': 'Nicht ganz. Von Berg zu Berg ist eine Wellenlänge.'},
        wahl('Frage 2', 'Das Zeitdiagramm zeigt eine Boje. Wie gross ist die Periode?', ['4.0 s', '1.5 s', '3.0 s'], 2,
             {0: 'Das ist der Zeitpunkt eines Maximums, nicht der Abstand zweier Maxima.', 1: 'Von einem Maximum zum nächsten Minimum ist nur eine halbe Periode.'},
             rueck_sprich={0: 'Das ist der Zeitpunkt eines Maximums, nicht der Abstand zweier Maxima.', 1: 'Von einem Maximum zum nächsten Minimum ist nur eine halbe Periode.'}),
        wahl('Frage 3', 'Eine Welle hat die Wellenlänge 0.60 m und die Periode 0.25 s. Wie gross ist die Phasengeschwindigkeit?', ['0.15 m/s', '0.42 m/s', '2.4 m/s'], 2,
             {0: 'Multipliziert statt geteilt: In einer Periode rückt die Welle um eine Wellenlänge weiter.', 1: 'Umgekehrt geteilt: Weg durch Zeit.'},
             sprich='Eine Welle hat die Wellenlänge null Komma sechs Meter und die Periode null Komma zwei fünf Sekunden. Wie gross ist die Phasengeschwindigkeit?'),
        wahl('Frage 4', 'Lea sieht im Zeitdiagramm zwei Maxima im Abstand von 0.4 s und schreibt: λ = 0.4 m. Was ist falsch?', ['Nichts, λ ist 0.4 m.', 'Das ist die Periode, eine Zeit — keine Wellenlänge.', 'Sie hätte von Berg zu Tal messen müssen.'], 1,
             {0: 'Was steht auf der Achse eines Zeitdiagramms?', 2: 'Von Berg zu Tal ist nur die Hälfte. Und welche Grösse ist es überhaupt?'},
             sprich='Lea sieht im Zeitdiagramm zwei Maxima im Abstand von null Komma vier Sekunden und schreibt: Lambda gleich null Komma vier Meter. Was ist falsch?'),
        wahl('Frage 5', 'Ein Wellenberg rückt in 0.5 s um 1.5 m weiter. Die Berge liegen 0.75 m auseinander. Wie gross ist die Frequenz?', ['4.0 Hz', '2.0 Hz', '0.25 Hz'], 0,
             {1: 'Ist 0.5 s wirklich eine Periode? Vergleiche den Weg des Bergs mit dem Abstand der Berge.', 2: 'Umgekehrt geteilt: Welche Grösse gehört in den Zähler?'},
             sprich='Ein Wellenberg rückt in null Komma fünf Sekunden um eins Komma fünf Meter weiter. Die Berge liegen null Komma sieben fünf Meter auseinander. Wie gross ist die Frequenz?',
             rueck_sprich={1: 'Ist eine halbe Sekunde wirklich eine Periode? Vergleiche den Weg des Bergs mit dem Abstand der Berge.', 2: 'Umgekehrt geteilt: Welche Grösse gehört in den Zähler?'}),
    ]))

# ================================================================== Kapitel 3: Sender und Medium
# Problem Schwimmbad: 850 Hz; Luft 340 m/s → 0.40 m; Wasser 1500 m/s → 1.76 m; Verhältnis 4.41
LW3 = 1500 / 850               # λ im Wasser (Problem)
assert abs(340 / 850 - 0.4) < 1e-12 and abs(1500 / 850 - 1.7647) < 1e-4 and abs(1500 / 340 - 4.4118) < 1e-4


def lautsprecher(x0=1.0, y0=5.0, n=7, lam=1.1, ein_=None):
    """Lautsprecher links, davor Verdichtungen als senkrechte Striche im Abstand λ (Längswelle)."""
    st = umriss(x0 - 0.6, y0 - 0.7, x0, y0 + 0.7, TIN, 4) + [S((x0, y0 - 0.7), (x0 + 0.6, y0 - 1.4), TIN, dicke=4), S((x0, y0 + 0.7), (x0 + 0.6, y0 + 1.4), TIN, dicke=4),
                                                         S((x0 + 0.6, y0 - 1.4), (x0 + 0.6, y0 + 1.4), TIN, dicke=4)]
    for i in range(n):
        x = x0 + 1.1 + i * lam
        kw = {'_ein': ein_, '_ein_versatz': 0.15 * i} if ein_ else {}
        st += [S((x, y0 - 1.2), (x, y0 + 1.2), BER, dicke=7, **kw), S((x + 0.18, y0 - 1.2), (x + 0.18, y0 + 1.2), BER, dicke=4, **kw)]
    return st


DREH.append(dict(KOPF, titel='Wellen sehen: Sender und Medium', dateiname='p6-1-lp-medium',
    kurzbeschrieb='Der Sender legt die Frequenz fest, das Medium die Geschwindigkeit, die Wellenlänge folgt aus c = λ · f; beim Übergang in ein anderes Medium bleibt die Frequenz. Schall braucht ein Medium — und ein vorgerechnetes Problem: ein Ton im Schwimmbad.',
    schlagworte=['Wellengleichung', 'Frequenz', 'Medium', 'Schall', 'Schallgeschwindigkeit', 'Mediumwechsel'], _probe=EIN % 3,
    szenen=[
        sz('Ein Ton', 'Ein Lautsprecher spielt einen Ton. Der Schall läuft durch die Luft zu deinem Ohr. Was legt dabei der Lautsprecher fest, und was die Luft?',
           titel('Wer bestimmt was?', g=66),
           notiz('Lautsprecher: ?|Luft: ?', y=460, a='Was legt dabei'),
           skizze(strecken=lautsprecher(ein_='Der Schall läuft'),
                  texte=[T(1.0, 7.2, 'Lautsprecher', TIN, 26), T(6.5, 7.2, 'Verdichtungen der Luft', BER, 24, _ein='Der Schall läuft')])),
        sz('Sender und Medium', 'Die Frequenz kommt vom Sender: Er schwingt so oft pro Sekunde. Die Geschwindigkeit gehört zum Medium: In Luft läuft Schall mit dreihundertvierzig Metern pro Sekunde. Die Wellenlänge stellt sich daraus ein: Lambda gleich c durch f.',
           notiz('Sender → Frequenz @f@', y=290, a='Die Frequenz kommt'),
           notiz('Medium → Geschwindigkeit @c@', y=370, a='Die Geschwindigkeit gehört'),
           formel(r'c = \lambda \cdot f \quad\Longrightarrow\quad \lambda = \frac{c}{f}', y=490, g=46, a='Die Wellenlänge stellt'),
           skizze(strecken=lautsprecher() + mass(2.1, 3.2, 3.2, '', _ein='Die Wellenlänge stellt')[0] + [P((6.0, 8.2), (8.6, 8.2), GRU, dicke=5, _ein='Die Geschwindigkeit gehört')],
                  texte=[T(1.0, 7.2, 'f: Takt', TIN, 26, _ein='Die Frequenz kommt'), T(7.3, 8.8, 'c = 340 m/s', GRU, 26, _ein='Die Geschwindigkeit gehört'),
                         T(2.65, 2.4, 'λ', TIN, 30, _ein='Die Wellenlänge stellt')])),
        sz('Höherer Ton', 'Spielt der Sender einen doppelt so hohen Ton, schwingt er doppelt so oft. Die Welle läuft trotzdem gleich schnell: Ihre Front kommt in derselben Zeit gleich weit. Jede Welle wird nur halb so lang.',
           notiz('doppelte Frequenz', y=300, a='schwingt er doppelt'),
           notiz('gleich schnell: Front gleich weit', y=380, a='Die Welle läuft trotzdem'),
           notiz('halbe Wellenlänge', y=460, a='Jede Welle wird nur halb'),
           bild('p6-1-lp-medium-f05.jpg', a='Spielt der Sender'),
           bild('p6-1-lp-medium-f10.jpg', a='schwingt er doppelt')),
        sz('Anderes Medium', 'Läuft die Welle in ein anderes Medium, bleibt die Frequenz: Der Takt kommt weiter vom Sender. Im schnelleren Medium wird die Welle länger, im langsameren kürzer — im selben Verhältnis wie die Geschwindigkeit.',
           notiz('Frequenz bleibt', y=300, a='Läuft die Welle'),
           notiz('schneller: länger', y=380, a='Im schnelleren'),
           notiz('langsamer: kürzer', y=440, a='im langsameren kürzer'),
           formel(r'\frac{\lambda_2}{\lambda_1} = \frac{c_2}{c_1}', y=560, g=46, a='im selben Verhältnis'),
           bild('p6-1-lp-medium-duenn.jpg', a='Im schnelleren'),
           bild('p6-1-lp-medium-dick.jpg', a='im langsameren kürzer')),
        sz('Schall', 'In Luft und in Wasser ist Schall eine Längswelle aus Druckschwankungen. Er braucht Teilchen, die sich anstossen: in Luft dreihundertvierzig, in Wasser rund eintausendfünfhundert, in Eisen fünftausendeinhundertsiebzig Meter pro Sekunde. Im Vakuum gibt es keinen Schall. Hören kann der Mensch etwa zwanzig Hertz bis zwanzig Kilohertz.',
           notiz('Schall in Luft und Wasser:|Längswelle; braucht ein Medium', y=290, a='In Luft und in Wasser'),
           notiz('Vakuum: kein Schall', y=440, a='Im Vakuum'),
           notiz('hörbar: 20 Hz bis 20 kHz', y=520, a='Hören kann'),
           graf((-0.5, 5.6), (-900, 6100), [], [1000, 2000, 3000, 4000, 5000, 6000], '', 'c [m/s]',
                flaechen=[F(rechteck(0.6, 0, 1.4, 340), BER, 0.55, _ein='in Luft'), F(rechteck(1.8, 0, 2.6, 1500), BER, 0.55, _ein='in Wasser rund'),
                          F(rechteck(3.0, 0, 3.8, 5170), BER, 0.55, _ein='in Eisen')],
                texte=[T(1.0, -400, 'Luft', TIN, 24), T(2.2, -400, 'Wasser', TIN, 24), T(3.4, -400, 'Eisen', TIN, 24), T(4.6, -400, 'Vakuum', TIN, 24),
                       T(1.0, 650, '340', BER, 26, _ein='in Luft'), T(2.2, 1800, '1500', BER, 26, _ein='in Wasser rund'), T(3.4, 5450, '5170', BER, 26, _ein='in Eisen'),
                       T(4.6, 400, 'kein Schall', TIN, 24, _ein='Im Vakuum')])),
        sz('Problem Schwimmbad', 'Jetzt ein ganzes Problem. Im Schwimmbad spielt ein Lautsprecher unter Wasser einen Ton von achthundertfünfzig Hertz. Der Schall läuft durchs Wasser, ein kleiner Teil gelangt an der Oberfläche in die Luft. Welche Wellenlänge hat er im Wasser, welche in der Luft? Und welche Frequenz hört der Bademeister am Rand?',
           notiz('Ton: 850 Hz', y=300, a='einen Ton'),
           notiz('Wasser: @c = 1500\\;\\text{m/s}@', y=370, a='Der Schall läuft durchs Wasser'),
           notiz('Luft: @c = 340\\;\\text{m/s}@', y=440, a='in die Luft'),
           notiz('gesucht: @\\lambda_\\text{Wasser}@, @\\lambda_\\text{Luft}@, @f@ in der Luft', y=550, a='Welche Wellenlänge'),
           skizze(flaechen=[F(rechteck(0.5, 1.0, 9.5, 5.0), TIN, 0.15)],
                  strecken=[S((0.5, 5.0), (9.5, 5.0), TIN, dicke=3)] + umriss(1.2, 2.2, 2.2, 3.4, TIN, 4),
                  texte=[T(1.7, 1.5, 'Lautsprecher', TIN, 24), T(5.0, 3.0, 'Wasser', TIN, 26, _ein='Der Schall läuft durchs Wasser'), T(6.5, 7.0, 'Luft', TIN, 26, _ein='in die Luft'),
                         T(8.4, 5.6, 'Bademeister', TIN, 24, _ein='hört der Bademeister')])),
        sz('Vorgehen Schwimmbad', 'Die Frequenz kommt vom Lautsprecher und bleibt in der Luft gleich. Für jedes Medium rechnest du Lambda gleich c durch f, mit seiner eigenen Geschwindigkeit.',
           formel(r'f = 850\;\text{Hz} \text{ in beiden Medien}', y=300, g=40, a='Die Frequenz kommt'),
           formel(r'\lambda = \frac{c}{f} \text{ je Medium}', y=420, g=42, a='Für jedes Medium'),
           skizze(flaechen=[F(rechteck(0.5, 1.0, 9.5, 5.0), TIN, 0.15)],
                  strecken=[S((0.5, 5.0), (9.5, 5.0), TIN, dicke=3)] + umriss(1.2, 2.2, 2.2, 3.4, TIN, 4),
                  texte=[T(6.5, 7.0, 'Luft: 340 m/s', TIN, 26), T(5.0, 3.8, 'Wasser: 1500 m/s', TIN, 26), T(1.7, 1.5, '850 Hz', TIN, 24)])),
        sz('Lösung Schwimmbad', 'In der Luft: Lambda gleich dreihundertvierzig Meter pro Sekunde durch achthundertfünfzig Hertz, null Komma vier Meter. Im Wasser: eintausendfünfhundert durch achthundertfünfzig, rund eins Komma sieben sechs Meter. Der Bademeister hört dieselben achthundertfünfzig Hertz. Probe: Die Wellenlängen stehen im Verhältnis der Geschwindigkeiten, eins Komma sieben sechs durch null Komma vier gibt rund vier Komma vier, und eintausendfünfhundert durch dreihundertvierzig auch.',
           *rechnung(r'\lambda_\text{L} = \frac{340\;\text{m/s}}{850\;\text{Hz}} = 0.40\;\text{m}', y=240, g=38, a='In der Luft', a_erg='null Komma vier Meter'),
           *rechnung(r'\lambda_\text{W} = \frac{1500\;\text{m/s}}{850\;\text{Hz}} \approx 1.76\;\text{m}', y=360, g=38, a='Im Wasser', a_erg='rund eins Komma sieben sechs Meter'),
           notiz('Bademeister: 850 Hz', y=470, g=38, a='Der Bademeister hört'),
           notiz('Probe: @\\frac{1.76\\;\\text{m}}{0.40\\;\\text{m}} \\approx 4.4 \\approx \\frac{1500\\;\\text{m/s}}{340\\;\\text{m/s}}@', y=560, g=34, a='gibt rund vier Komma vier'),
           graf((-0.25, 4.0), (-4.2, 4.2), [1, 2, 3], [], 's [m]', 'Druck (schematisch)', y=175, hoehe=760,
                kurven=[dict(welle(0.9, 0.4, 0.1, von=0, bis=3.2), bewegung=[[0, 0.9, r4(2 * math.pi / 0.4), 0.0, 2.0]], _ein='In der Luft'),
                        dict(welle(0.9, LW3, 0.4, von=0, bis=3.2), bewegung=[[0, 0.9, r4(2 * math.pi / LW3), r4(0.4 - LW3 / 4), -1.8]], _ein='Im Wasser')],
                strecken=mass(1.3, 1.7, 3.3, '0.40 m', ty=3.75, _ein='null Komma vier Meter')[0] + mass(0.4 + LW3 / 2, 0.4 + 1.5 * LW3, -3.3, '1.76 m', ty=-3.85, _ein='rund eins Komma sieben')[0],
                texte=mass(1.3, 1.7, 3.3, '0.40 m', ty=3.75, _ein='null Komma vier Meter')[1] + mass(0.4 + LW3 / 2, 0.4 + 1.5 * LW3, -3.3, '1.76 m', ty=-3.85, _ein='rund eins Komma sieben')[1]
                + [T(3.3, 1.85, 'Luft', TIN, 26, 'start', _ein='In der Luft'), T(3.3, -1.95, 'Wasser', TIN, 26, 'start', _ein='Im Wasser')])),
        merke('Zum Mitnehmen: Der Sender legt die Frequenz fest, das Medium die Geschwindigkeit. Die Wellenlänge folgt aus c gleich Lambda mal f. Wechselt die Welle das Medium, bleibt die Frequenz.',
              r'c = \lambda \cdot f', 'Sender: @f@|Medium: @c@|Wellenlänge: @\\lambda = c / f@'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Schwimmbad', 'Was bleibt beim Übergang in die Luft gleich?', ['die Wellenlänge', 'die Geschwindigkeit', 'die Frequenz'], 2,
                 {0: 'Die Wellenlänge hängt auch von der Geschwindigkeit ab. Ist die in Luft dieselbe wie in Wasser?', 1: 'Die Geschwindigkeit gehört zum Medium. Ist Luft dasselbe Medium wie Wasser?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 3
assert abs(980 / 680 - 1.4412) < 1e-4 and abs(1500 / 100e3 - 0.015) < 1e-12
DREH.append(dict(KOPF, titel='Wellen sehen: Kontrollfragen zu Sender, Medium und Schall', dateiname='p6-1-lp-kontrolle-medium',
    kurzbeschrieb='Fünf Fragen: ein Ton in Helium, die Klicks eines Delfins im Wasser, ein Ton, der in Eisen übergeht, zwei Astronauten auf dem Mond und eine Stimmgabel in wärmerer Luft.',
    schlagworte=['Wellengleichung', 'Schall', 'Medium', 'Frequenz', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'In Helium läuft der Schall mit neunhundertachtzig Metern pro Sekunde. Lambda gleich c durch f: neunhundertachtzig durch sechshundertachtzig, rund eins Komma vier vier Meter.',
           formel(r'\lambda = \frac{c}{f} = \frac{980\;\text{m/s}}{680\;\text{Hz}} \approx 1.44\;\text{m}', y=320, g=44, ein=1.0)),
        sz('Frage 2', 'Hundert Kilohertz sind hunderttausend Hertz. Im Wasser: eintausendfünfhundert Meter pro Sekunde durch hunderttausend Hertz, null Komma null eins fünf Meter, also eins Komma fünf Zentimeter.',
           formel(r'\lambda = \frac{1500\;\text{m/s}}{100\,000\;\text{Hz}} = 0.015\;\text{m} = 1.5\;\text{cm}', y=320, g=40, ein=1.0)),
        sz('Frage 3', 'Die Frequenz kommt vom Sender und bleibt. Eisen ist viel schneller als Luft, darum wird die Welle im Eisen im selben Verhältnis länger.',
           notiz('@f@ bleibt; @c@ und @\\lambda@|werden grösser', y=320, ein=1.0)),
        sz('Frage 4', 'Auf dem Mond gibt es keine Luft. Ohne Medium, ohne Teilchen, die sich anstossen, läuft kein Schall. Berühren sich die Helme, geht der Schall durch sie hindurch.',
           notiz('keine Luft: kein Medium,|kein Schall', y=320, ein=1.0)),
        sz('Frage 5', 'Die Frequenz kommt von der Stimmgabel und bleibt. In der wärmeren Luft läuft der Schall etwas schneller, dreihundertsechsundvierzig statt dreihundertvierzig Meter pro Sekunde. Darum wird die Welle etwas länger: null Komma sechs neun statt null Komma sechs acht Meter.',
           notiz('@f@ bleibt; wärmer: @c@ grösser|→ Welle etwas länger', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Ton von 680 Hz läuft in Helium (980 m/s). Wie lang ist seine Welle?', ['1.44 m', '0.69 m', '0.50 m'], 0,
             {1: 'Umgekehrt geteilt: Welche Grösse teilst du durch welche?', 2: 'Das wäre die Wellenlänge in Luft. Der Ton läuft hier in Helium.'},
             sprich='Ein Ton von sechshundertachtzig Hertz läuft in Helium, mit neunhundertachtzig Metern pro Sekunde. Wie lang ist seine Welle?',
             rueck_sprich={1: 'Umgekehrt geteilt: Welche Grösse teilst du durch welche?', 2: 'Das wäre die Wellenlänge in Luft. Der Ton läuft hier in Helium.'}),
        wahl('Frage 2', 'Ein Delfin ortet im Wasser (1500 m/s) mit Klicks von 100 kHz. Wie lang ist die Welle?', ['15 m', '1.5 cm', '3.4 mm'], 1,
             {0: 'Kilohertz in Hertz umgerechnet? 100 kHz sind 100 000 Hz.', 2: 'Das wäre in Luft. Der Delfin ortet im Wasser.'},
             sprich='Ein Delfin ortet im Wasser mit Klicks von hundert Kilohertz. Im Wasser läuft der Schall mit eintausendfünfhundert Metern pro Sekunde. Wie lang ist die Welle?',
             rueck_sprich={0: 'Kilohertz in Hertz umgerechnet? Hundert Kilohertz sind hunderttausend Hertz.', 2: 'Das wäre in Luft. Der Delfin ortet im Wasser.'}),
        wahl('Frage 3', 'Ein Ton geht aus der Luft in eine Eisenschiene über. Was gilt?', ['f wird grösser; λ bleibt gleich', 'f bleibt; λ wird kleiner', 'f bleibt; c und λ werden grösser'], 2,
             {0: 'Woher kommt die Frequenz — vom Sender oder vom Medium?', 1: 'Eisen ist schneller als Luft. Was folgt aus λ = c / f, wenn f bleibt?'},
             rueck_sprich={0: 'Woher kommt die Frequenz, vom Sender oder vom Medium?', 1: 'Eisen ist schneller als Luft. Was folgt aus Lambda gleich c durch f, wenn f bleibt?'}),
        wahl('Frage 4', 'Zwei Astronauten stehen auf dem Mond nebeneinander. Ohne Funk hören sie einander nicht. Warum?', ['Der Schall ist dort zu langsam.', 'Auf dem Mond gibt es keine Luft: Schall braucht ein Medium.', 'Die Helme schlucken jeden Ton.'], 1,
             {0: 'Auch nach langer Zeit käme nichts an. Was fehlt zwischen den beiden?', 2: 'Berühren sich die Helme, hören sie einander. Was fehlt sonst?'}),
        wahl('Frage 5', 'Eine Stimmgabel mit 500 Hz klingt am Morgen in Luft von 15 °C, am Nachmittag in Luft von 25 °C (346 m/s statt 340 m/s). Was gilt am Nachmittag?', ['Die Welle ist etwas länger.', 'Die Welle ist gleich lang.', 'Die Welle ist etwas kürzer.'], 0,
             {1: 'Die Frequenz bleibt. Was ändert sich mit der Temperatur, und was folgt daraus für λ = c / f?', 2: 'Ist der Schall in warmer Luft schneller oder langsamer? Was folgt für λ = c / f?'},
             sprich='Eine Stimmgabel mit fünfhundert Hertz klingt am Morgen in Luft von fünfzehn Grad, am Nachmittag in Luft von fünfundzwanzig Grad. Dort läuft der Schall mit dreihundertsechsundvierzig statt dreihundertvierzig Metern pro Sekunde. Was gilt am Nachmittag?',
             rueck_sprich={1: 'Die Frequenz bleibt. Was ändert sich mit der Temperatur, und was folgt daraus für Lambda gleich c durch f?', 2: 'Ist der Schall in warmer Luft schneller oder langsamer? Was folgt für Lambda gleich c durch f?'}),
    ]))

# ================================================================== Kapitel 4: Elektromagnetische Wellen
# Problem Radio: 88.0 MHz → λ = 3.41 m; 45 km → t = 1.5·10⁻⁴ s; Schall 132 s
assert abs(C / 88.0e6 - 3.409) < 1e-3 and abs(45e3 / C - 1.5e-4) < 1e-12 and abs(45e3 / 340 - 132.35) < 0.01
SPEK = ['radio', 'wlan', 'ir', 'gruen', 'uv', 'roentgen']
DREH.append(dict(KOPF, titel='Wellen sehen: elektromagnetische Wellen', dateiname='p6-1-lp-em',
    kurzbeschrieb='Elektromagnetische Wellen als schwingende elektrische und magnetische Felder, ohne Medium, im Vakuum alle mit Lichtgeschwindigkeit; das Spektrum von Radio bis Gamma — und ein vorgerechnetes Problem: Wellenlänge und Laufzeit eines UKW-Senders.',
    schlagworte=['elektromagnetische Welle', 'Lichtgeschwindigkeit', 'Spektrum', 'Wellengleichung'], _probe=EIN % 4,
    szenen=[
        sz('Sonnenlicht', 'Das Licht der Sonne erreicht uns durch hundertfünfzig Millionen Kilometer fast leeren Raum. Ein Ton käme dort nicht durch. Was für eine Welle ist das Licht?',
           titel('Licht durchs Vakuum', g=64),
           notiz('Licht: kommt an|Schall: käme nicht durch', y=460, a='Ein Ton'),
           skizze(figuren=[{'art': 'kreis', 'm': [1.6, 5.0], 'r': 1.1, 'farbe': ORA, 'fuellung': 0.5}, {'art': 'kreis', 'm': [8.6, 5.0], 'r': 0.45, 'farbe': TIN, 'fuellung': 0.35}],
                  strecken=[P((2.9, 5.0), (7.9, 5.0), ORA, dicke=6, _ein='Das Licht der Sonne')],
                  texte=[T(1.6, 3.4, 'Sonne', ORA, 26), T(8.6, 3.9, 'Erde', TIN, 26), T(5.3, 5.6, 'Vakuum', TIN, 24, _ein='fast leeren Raum'),
                         T(5.3, 6.5, '150 Millionen km', TIN, 24, _ein='hundertfünfzig Millionen')])),
        sz('Felder', 'Elektromagnetische Wellen bestehen aus einem elektrischen und einem magnetischen Feld. Sie schwingen senkrecht zueinander und quer zur Ausbreitung: eine Querwelle. Es schwingen keine Teilchen, darum braucht die Welle kein Medium.',
           notiz('elektrisches Feld @E@ und|magnetisches Feld @B@', y=290, a='Elektromagnetische Wellen'),
           notiz('senkrecht zueinander,|quer zur Ausbreitung', y=430, a='Sie schwingen'),
           notiz('keine Teilchen: kein Medium nötig', y=570, a='Es schwingen keine', farbe='gruen'),
           bild('p6-1-lp-em-feld-a.jpg', a='Elektromagnetische Wellen', y=250),
           bild('p6-1-lp-em-feld-b.jpg', a='Sie schwingen', v=0.8, y=250)),
        sz('Lichtgeschwindigkeit', 'Im Vakuum laufen alle elektromagnetischen Wellen gleich schnell: c gleich drei Komma null null mal zehn hoch acht Meter pro Sekunde, rund dreihunderttausend Kilometer in jeder Sekunde. Auch hier gilt c gleich Lambda mal f.',
           formel(r'c = 3.00 \cdot 10^{8}\;\text{m/s}', y=300, g=50, a='c gleich'),
           notiz('rund 300 000 km in jeder Sekunde', y=430, a='rund dreihunderttausend'),
           formel(r'c = \lambda \cdot f', y=540, g=50, a='Auch hier'),
           skizze(strecken=[P((1.0, 7.5), (8.6, 7.5), GRU, dicke=6, _ein='alle elektromagnetischen'), P((1.0, 5.0), (8.6, 5.0), GRU, dicke=6, _ein='alle elektromagnetischen', _ein_versatz=0.3),
                            P((1.0, 2.5), (8.6, 2.5), GRU, dicke=6, _ein='alle elektromagnetischen', _ein_versatz=0.6)],
                  texte=[T(1.0, 8.2, 'Radiowelle', TIN, 26, 'start', _ein='alle elektromagnetischen'), T(1.0, 5.7, 'Licht', TIN, 26, 'start', _ein='alle elektromagnetischen', _ein_versatz=0.3),
                         T(1.0, 3.2, 'Röntgenstrahlung', TIN, 26, 'start', _ein='alle elektromagnetischen', _ein_versatz=0.6), T(5.0, 1.2, 'gleich schnell', GRU, 28, _ein='gleich schnell')])),
        sz('Spektrum', 'Nach der Wellenlänge geordnet bilden sie ein Spektrum: Radiowellen, Mikrowellen, Infrarot, sichtbares Licht von dreihundertachtzig bis siebenhundertachtzig Nanometern, Ultraviolett und Röntgenstrahlung, am kurzen Ende die Gammastrahlung. Je kürzer die Welle, desto höher die Frequenz.',
           notiz('Radio · Mikrowellen · Infrarot ·|sichtbar (380 bis 780 nm) ·|UV · Röntgen · Gamma', y=270, a='Nach der Wellenlänge'),
           notiz('kürzer → höhere Frequenz', y=470, a='Je kürzer'),
           bild('p6-1-lp-em-radio.jpg', a='Radiowellen'), bild('p6-1-lp-em-gruen.jpg', a='sichtbares Licht'), bild('p6-1-lp-em-roentgen.jpg', a='Röntgenstrahlung, am', v=0.6)),
        sz('Problem Radio', 'Jetzt ein ganzes Problem. Ein UKW-Sender sendet auf achtundachtzig Megahertz. Wie lang sind seine Wellen? Und wie lange braucht sein Signal zu einem Radio in fünfundvierzig Kilometern Entfernung?',
           notiz('Sender: 88.0 MHz', y=300, a='Jetzt ein ganzes Problem', v=2.5),
           notiz('Radio: 45 km entfernt', y=370, a='zu einem Radio'),
           notiz('gesucht: @\\lambda@ und Laufzeit @t@', y=480, a='Wie lang sind'),
           skizze(strecken=[S((1.2, 2.0), (1.2, 7.0), TIN, dicke=6), S((0.6, 2.0), (1.2, 7.0), TIN, dicke=3), S((1.8, 2.0), (1.2, 7.0), TIN, dicke=3)]
                  + umriss(8.0, 2.0, 9.2, 3.0, TIN, 4) + mass(1.2, 8.6, 4.5, '45 km', ty=5.0, _ein='zu einem Radio')[0],
                  texte=[T(1.2, 1.2, 'Sender', TIN, 26), T(8.6, 1.2, 'Radio', TIN, 26, _ein='zu einem Radio')] + mass(1.2, 8.6, 4.5, '45 km', ty=5.0, _ein='zu einem Radio')[1])),
        sz('Vorgehen Radio', 'Zuerst die Frequenz in Hertz umrechnen. Dann Lambda gleich c durch f, und für die Laufzeit t gleich s durch c.',
           formel(r'88.0\;\text{MHz} = 8.80 \cdot 10^{7}\;\text{Hz}', y=290, g=40, a='Zuerst'),
           formel(r'\lambda = \frac{c}{f}, \qquad t = \frac{s}{c}', y=410, g=44, a='Dann Lambda'),
           skizze(strecken=[S((1.2, 2.0), (1.2, 7.0), TIN, dicke=6), S((0.6, 2.0), (1.2, 7.0), TIN, dicke=3), S((1.8, 2.0), (1.2, 7.0), TIN, dicke=3)]
                  + umriss(8.0, 2.0, 9.2, 3.0, TIN, 4) + mass(1.2, 8.6, 4.5, '45 km', ty=5.0)[0],
                  texte=[T(1.2, 1.2, 'Sender', TIN, 26), T(8.6, 1.2, 'Radio', TIN, 26)] + mass(1.2, 8.6, 4.5, '45 km', ty=5.0)[1])),
        sz('Lösung Radio', 'Lambda gleich drei Komma null null mal zehn hoch acht Meter pro Sekunde durch acht Komma acht null mal zehn hoch sieben Hertz, rund drei Komma vier eins Meter. Für fünfundvierzig Kilometer braucht das Signal t gleich s durch c, eins Komma fünf mal zehn hoch minus vier Sekunden, das sind null Komma eins fünf Millisekunden. Schall bräuchte über zwei Minuten. Probe: drei Komma vier eins Meter mal acht Komma acht null mal zehn hoch sieben Hertz gibt wieder drei mal zehn hoch acht Meter pro Sekunde.',
           *rechnung(r'\lambda = \frac{3.00 \cdot 10^{8}\;\text{m/s}}{8.80 \cdot 10^{7}\;\text{Hz}} \approx 3.41\;\text{m}', y=240, g=36, a='Lambda gleich', a_erg='rund drei Komma vier eins Meter'),
           *rechnung(r't = \frac{s}{c} = \frac{4.5 \cdot 10^{4}\;\text{m}}{3.00 \cdot 10^{8}\;\text{m/s}} = 1.5 \cdot 10^{-4}\;\text{s}', y=370, g=36, a='Für fünfundvierzig', a_erg='eins Komma fünf mal zehn hoch minus vier'),
           notiz('Schall: über 2 min', y=490, g=38, a='Schall bräuchte'),
           *probe('Probe: @3.41\\;\\text{m} \\cdot 8.80 \\cdot 10^{7}\\;\\text{Hz}', ' \\approx 3.00 \\cdot 10^{8}\\;\\text{m/s}@', y=580, g=32, a_erg='gibt wieder drei mal zehn hoch acht'),
           skizze(strecken=[S((1.2, 2.0), (1.2, 7.0), TIN, dicke=6), S((0.6, 2.0), (1.2, 7.0), TIN, dicke=3), S((1.8, 2.0), (1.2, 7.0), TIN, dicke=3)]
                  + umriss(8.0, 2.0, 9.2, 3.0, TIN, 4) + mass(1.2, 8.6, 4.5, '45 km', ty=5.0)[0]
                  + [P((1.6, 6.3), (8.0, 6.3), GRU, dicke=5, _ein='Für fünfundvierzig')],
                  texte=[T(1.2, 1.2, 'Sender', TIN, 26), T(8.6, 1.2, 'Radio', TIN, 26)] + mass(1.2, 8.6, 4.5, '45 km', ty=5.0)[1]
                  + [T(4.8, 7.0, 'Radiowelle: 0.15 ms', GRU, 26, _ein='das sind null Komma eins fünf'), T(4.8, 3.6, 'Schall: 132 s', TIN, 24, _ein='Schall bräuchte'),
                     T(5.0, 9.0, 'λ ≈ 3.41 m', TIN, 28, _ein='rund drei Komma vier eins')])),
        merke('Zum Mitnehmen: Elektromagnetische Wellen sind schwingende Felder, quer zur Ausbreitung. Sie brauchen kein Medium und laufen im Vakuum alle mit Lichtgeschwindigkeit. Verschieden sind nur Wellenlänge und Frequenz.',
              r'c = \lambda \cdot f = 3.00 \cdot 10^{8}\;\text{m/s}', 'schwingende Felder, quer|kein Medium nötig|verschieden: @\\lambda@ und @f@'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Radio', 'Welche Geschwindigkeit setzt du für die Radiowelle ein?', ['340 m/s wie beim Schall', 'sie hängt von der Frequenz ab', '3.00 · 10⁸ m/s'], 2,
                 {0: 'Ist eine Radiowelle Schall? Braucht sie Luft?', 1: 'Was hat der Clip über die Geschwindigkeit von Radiowellen, Licht und Röntgenstrahlung im Vakuum gesagt?'},
                 sprich='Welche Geschwindigkeit setzt du für die Radiowelle ein?',
                 rueck_sprich={0: 'Ist eine Radiowelle Schall? Braucht sie Luft?', 1: 'Was hat der Clip über die Geschwindigkeit von Radiowellen, Licht und Röntgenstrahlung im Vakuum gesagt?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 4
assert abs(C / 12e9 - 0.025) < 1e-12 and abs(C / 12e6 - 25) < 1e-9 and abs(12e9 / C - 40) < 1e-9
DREH.append(dict(KOPF, titel='Wellen sehen: Kontrollfragen zu den elektromagnetischen Wellen', dateiname='p6-1-lp-kontrolle-em',
    kurzbeschrieb='Fünf Fragen: ein Wecker und ein Lämpchen unter einer leer gepumpten Glocke, die Reihenfolge des Spektrums, die Welle eines Fernsehsatelliten, rotes gegen blaues Licht und was bei einer elektromagnetischen Welle schwingt.',
    schlagworte=['elektromagnetische Welle', 'Spektrum', 'Lichtgeschwindigkeit', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Je weniger Luft unter der Glocke ist, desto leiser wird der Wecker: Schall braucht Teilchen, die sich anstossen. Das Licht des Lämpchens braucht kein Medium; es bleibt gleich hell.',
           notiz('Licht: kein Medium nötig|Schall: braucht eines', y=320, ein=1.0)),
        sz('Frage 2', 'Von kurz nach lang: Gamma, Röntgen, Ultraviolett, sichtbares Licht, Infrarot, Mikrowellen, Radio.',
           notiz('Gamma · Röntgen · UV · Licht ·|Infrarot · Mikrowellen · Radio', y=320, ein=1.0)),
        sz('Frage 3', 'Zwölf Gigahertz sind eins Komma zwei mal zehn hoch zehn Hertz. Lambda gleich drei mal zehn hoch acht durch eins Komma zwei mal zehn hoch zehn, null Komma null zwei fünf Meter, zwei Komma fünf Zentimeter.',
           formel(r'\lambda = \frac{3.00 \cdot 10^{8}\;\text{m/s}}{1.2 \cdot 10^{10}\;\text{Hz}} = 0.025\;\text{m} = 2.5\;\text{cm}', y=320, g=38, ein=1.0)),
        sz('Frage 4', 'Beide laufen gleich schnell. Aus c gleich Lambda mal f folgt: Die kürzere Welle hat die höhere Frequenz. Das ist das blaue Licht.',
           notiz('gleiches @c@: kürzere Welle,|höhere Frequenz: blau', y=320, ein=1.0)),
        sz('Frage 5', 'Bei einer elektromagnetischen Welle schwingen ein elektrisches und ein magnetisches Feld, quer zur Ausbreitung. Teilchen braucht es dafür keine.',
           notiz('elektrisches und magnetisches|Feld, quer zur Ausbreitung', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Unter einer Glasglocke klingelt ein Wecker, daneben leuchtet ein Lämpchen. Die Luft wird abgepumpt. Was beobachtest du?', ['Das Lämpchen leuchtet weiter, den Wecker hört man kaum noch.', 'Den Wecker hört man weiter, das Lämpchen wird dunkler.', 'Beides bleibt, wie es ist.'], 0,
             {1: 'Was braucht eine Welle aus Druckschwankungen, das ein elektromagnetisches Feld nicht braucht?', 2: 'Woraus besteht Schall? Und was wird abgepumpt?'}),
        wahl('Frage 2', 'Welche Reihenfolge stimmt, von der kürzesten zur längsten Welle?', ['Radio, Mikrowellen, Infrarot, Licht, UV, Röntgen, Gamma', 'Gamma, Röntgen, UV, Licht, Infrarot, Mikrowellen, Radio', 'Licht, UV, Infrarot, Radio, Röntgen, Gamma, Mikrowellen'], 1,
             {0: 'Das ist dieselbe Reihe, aber von der längsten zur kürzesten Welle.', 2: 'Wo liegt das sichtbare Licht? Zwischen Infrarot und Ultraviolett.'}),
        wahl('Frage 3', 'Ein Fernsehsatellit sendet mit 12 GHz. Wie lang ist seine Welle?', ['25 m', '40 m', '2.5 cm'], 2,
             {0: 'Giga heisst 10⁹, nicht 10⁶.', 1: 'Umgekehrt geteilt: Welche Grösse teilst du durch welche?'},
             sprich='Ein Fernsehsatellit sendet mit zwölf Gigahertz. Wie lang ist seine Welle?',
             rueck_sprich={0: 'Giga heisst zehn hoch neun, nicht zehn hoch sechs.', 1: 'Umgekehrt geteilt: Welche Grösse teilst du durch welche?'}),
        wahl('Frage 4', 'Rotes Licht hat 700 nm, blaues 450 nm. Welches hat die höhere Frequenz?', ['das rote', 'das blaue', 'beide gleich, weil beide gleich schnell sind'], 1,
             {0: 'Längere Welle bei gleicher Geschwindigkeit: Was folgt aus c = λ · f für f?', 2: 'Gleich schnell ja — aber c = λ · f. Was folgt bei kürzerer Wellenlänge?'},
             sprich='Rotes Licht hat siebenhundert Nanometer, blaues vierhundertfünfzig Nanometer. Welches hat die höhere Frequenz?',
             rueck_sprich={0: 'Längere Welle bei gleicher Geschwindigkeit: Was folgt aus c gleich Lambda mal f für f?', 2: 'Gleich schnell ja, aber c gleich Lambda mal f. Was folgt bei kürzerer Wellenlänge?'}),
        wahl('Frage 5', 'Was schwingt bei einer elektromagnetischen Welle?', ['Luftteilchen, hin und her', 'Elektronen, die mit Lichtgeschwindigkeit mitfliegen', 'ein elektrisches und ein magnetisches Feld, quer zur Ausbreitung'], 2,
             {0: 'Licht kommt auch durchs Vakuum. Gibt es dort Luft?', 1: 'Es fliegt nichts mit. Was schwingt an jeder Stelle der Welle?'}),
    ]))

# ================================================================== Kapitel 5: Licht aus dem Atom
# Problem: E2→E1 gibt 640 nm; Stufe E3→E1 1.25-mal so gross → f 1.25-mal so gross → λ = 512 nm
assert abs(C / 640e-9 - 4.6875e14) < 1e3 and abs(1.25 * C / 640e-9 - 5.859375e14) < 1e3 and abs(640 / 1.25 - 512) < 1e-9
NEON = [585.2, 614.3, 621.7, 633.4, 640.2, 650.7, 667.8, 692.9, 703.2]   # helle Neonlinien (Ne I) in nm, gerundet; geprüft am 08.10.2026 an den NIST-Tabellen (5852.49, 6143.06, 6402.25, 6506.53, 7032.41 Å …)
NIV = {1: 2.0, 2: 6.0, 3: 7.0}            # Fensterhöhe der Stufen (E2 − E1 : E3 − E1 = 4 : 5)


def niveaus(x0=1.2, x1=4.6, mit3=True, **kw):
    st, tx = [], []
    for k, y in NIV.items():
        if k == 3 and not mit3:
            continue
        st.append(S((x0, y), (x1, y), TIN, dicke=4, **kw))
        tx.append(T(x0 - 0.2, y - 0.15, 'E%s' % '₁₂₃'[k - 1], TIN, 28, 'end', **kw))
    return st, tx


def elektron(x, y, **kw):
    d = {'art': 'kreis', 'm': [r4(x), r4(y)], 'r': 0.22, 'farbe': TIN, 'fuellung': 1}
    d.update(kw)
    return d


def photon(x0, x1, y, lam=0.5, farbe=ORA, **kw):
    """Gewellter Pfeil (Photon) waagrecht von x0 nach x1 auf Höhe y."""
    b = 2 * math.pi / lam
    r = 1 if x1 > x0 else -1                  # Richtung: Spitze bei x1
    k = {'trig': 'sin', 'bewegung': [[0, 0.28, r4(b), r4(x0), r4(y)]], 'von': r4(min(x0, x1 - 0.25 * r)), 'bis': r4(max(x0, x1 - 0.25 * r)),
         'farbe': farbe, 'dicke': 5}
    k.update(kw)
    return k, P((x1 - 0.45 * r, y), (x1, y), farbe, dicke=5, **kw)


DREH.append(dict(KOPF, titel='Wellen sehen: Licht aus dem Atom', dateiname='p6-1-lp-licht',
    kurzbeschrieb='Wie ein Atom Licht aussendet und aufnimmt: Elektronen springen zwischen Energiestufen, jedes Photon trägt genau die Energie einer Stufe; im Laser lösen Photonen weitere, gleiche Photonen aus — und ein vorgerechnetes Problem: die Farbe eines zweiten Sprungs.',
    schlagworte=['Atom', 'Energiestufe', 'Photon', 'Emission', 'Absorption', 'Laser', 'Spektrallinie'], _probe=EIN % 5,
    szenen=[
        sz('Leuchtreklame', 'Eine Leuchtröhre mit Neon leuchtet rot, eine mit anderem Gas in einer anderen Farbe. Zerlegt man das Licht, findet man nur einzelne, ganz bestimmte Wellenlängen. Woher kommen sie?',
           titel('Woher kommt die Farbe?', g=66),
           notiz('Neon: rot|nur bestimmte Wellenlängen', y=460, a='Zerlegt man'),
           graf((360, 840), (-0.45, 1.5), [400, 500, 600, 700], [], 'λ [nm]', '', a='Zerlegt man',
                flaechen=[F(rechteck(380, 0, 780, 1.0), TIN, 0.85)] + [F(rechteck(l - 1.6, 0, l + 1.6, 1.0), ORA, 1.0) for l in NEON],
                texte=[T(580, 1.2, 'Licht einer Neonröhre, zerlegt', TIN, 26), T(640.2, -0.32, '640', ORA, 22)])),
        sz('Energiestufen', 'In einem Atom kann ein Elektron nur ganz bestimmte Energien haben, die Energiestufen. Wird das Atom angeregt, durch einen Stoss oder durch Licht, springt das Elektron auf eine höhere Stufe.',
           notiz('nur bestimmte Energien:|Energiestufen', y=290, a='In einem Atom'),
           notiz('Anregung: Stoss oder Licht|→ höhere Stufe', y=450, a='Wird das Atom angeregt'),
           skizze(strecken=niveaus()[0] + [P((2.0, 2.35), (2.0, 5.65), TIN, dicke=4, gestrichelt=True, _ein='springt das Elektron')],
                  texte=niveaus()[1] + [T(2.9, 4.0, 'Anregung', TIN, 26, 'start', _ein='Wird das Atom angeregt')],
                  figuren=[elektron(2.0, 2.0, bewegung=[[0.1, {}]], _bewegung=[['springt das Elektron', 0.0, {'m': [2.0, 2.0]}], ['springt das Elektron', 0.6, {'m': [2.0, 6.0]}]])])),
        sz('Emission', 'Von selbst springt das Elektron bald zurück, zu einem zufälligen Zeitpunkt: die spontane Emission. Die Energie, die es dabei abgibt, nimmt ein Photon mit, ein Lichtteilchen. Seine Energie ist genau die Stufe: E gleich h mal f. Eine grössere Stufe gibt eine höhere Frequenz und damit eine kürzere Welle. Jedes Gas hat seine eigenen Stufen, darum seine eigenen Farben.',
           notiz('spontane Emission: Sprung|nach unten → Photon', y=270, a='Von selbst'),
           formel(r'E_\text{Photon} = h \cdot f = \text{Stufe}', y=410, g=42, a='Seine Energie ist'),
           notiz('grössere Stufe: höheres @f@,|kürzeres @\\lambda@', y=500, a='Eine grössere Stufe'),
           notiz('jedes Gas: eigene Linien', y=630, a='Jedes Gas hat'),
           skizze(strecken=niveaus()[0] + [P((1.8, 5.65), (1.8, 2.35), TIN, dicke=4, _ein='Von selbst'), photon(3.3, 7.3, 4.0)[1] | {'_ein': 'nimmt ein Photon mit'},
                                           P((2.8, 4.0), (2.8, 2.1), TIN, dicke=3, _ein='Seine Energie ist'), P((2.8, 4.0), (2.8, 5.9), TIN, dicke=3, _ein='Seine Energie ist')],
                  kurven=[photon(3.3, 7.3, 4.0)[0] | {'_ein': 'nimmt ein Photon mit'}],
                  texte=niveaus()[1] + [T(5.3, 4.7, 'Photon', ORA, 26, _ein='nimmt ein Photon mit'),
                                        T(3.0, 5.0, 'Stufe', TIN, 26, 'start', _ein='Seine Energie ist')],
                  figuren=[elektron(1.8, 6.0, bewegung=[[0.1, {}]], _bewegung=[['Von selbst', 0.2, {'m': [1.8, 6.0]}], ['Von selbst', 0.8, {'m': [1.8, 2.0]}]])])),
        sz('Absorption', 'Umgekehrt nimmt ein Atom ein Photon nur auf, wenn dessen Energie genau zu einer Stufe passt. Das Elektron springt dann hinauf. Alle anderen Photonen gehen ungehindert vorbei. Darum fehlen im Licht, das durch ein Gas geht, einzelne Farben: die Photonen, die zu einem Sprung nach oben passen, ausgehend von der Stufe, auf der die Elektronen sitzen.',
           notiz('Photon passt genau → aufgenommen', y=280, a='Umgekehrt'),
           notiz('passt nicht → geht vorbei', y=390, a='Alle anderen'),
           notiz('dunkle Linien: Photonen, die zu|einem Sprung nach oben passen', y=500, a='Darum fehlen'),
           skizze(strecken=niveaus(mit3=False)[0] + [photon(9.0, 5.0, 4.0)[1] | {'_aus': 'Das Elektron springt'}, photon(9.6, 1.2, 8.6, lam=0.7, farbe=TIN)[1] | {'_ein': 'Alle anderen'},
                                                    P((2.0, 2.35), (2.0, 5.65), TIN, dicke=4, gestrichelt=True, _ein='Das Elektron springt')],
                  kurven=[photon(9.0, 5.0, 4.0)[0] | {'_aus': 'Das Elektron springt'}, photon(9.6, 1.2, 8.6, lam=0.7, farbe=TIN)[0] | {'_ein': 'Alle anderen'}],
                  texte=niveaus(mit3=False)[1] + [T(7.0, 3.1, 'passt', ORA, 26, _aus='Das Elektron springt'), T(7.6, 9.4, 'passt nicht', TIN, 26, _ein='Alle anderen')],
                  figuren=[elektron(2.0, 2.0, bewegung=[[0.1, {}]], _bewegung=[['Das Elektron springt', 0.0, {'m': [2.0, 2.0]}], ['Das Elektron springt', 0.6, {'m': [2.0, 6.0]}]])])),
        sz('Laser', 'Trifft ein passendes Photon ein Atom, das schon angeregt ist, löst es ein zweites Photon aus: gleiche Wellenlänge, gleiche Phase, gleiche Richtung. Das ist die stimulierte Emission. Im Laser laufen so immer mehr gleiche Photonen zwischen zwei Spiegeln hin und her; ein Teil tritt als scharf gebündelter Strahl aus, in einer einzigen Farbe.',
           notiz('angeregtes Atom + passendes Photon|→ zwei gleiche Photonen', y=270, a='Trifft ein passendes'),
           notiz('gleiche Wellenlänge, Phase|und Richtung', y=420, a='gleiche Wellenlänge'),
           notiz('Laser: gebündelt, eine Farbe', y=560, a='Im Laser'),
           bild('p6-1-lp-licht-erzwungen.jpg', a='Trifft ein passendes'),
           bild('p6-1-lp-licht-laser.jpg', a='Im Laser')),
        sz('Problem Atom', 'Jetzt ein ganzes Problem. Ein Atom gibt beim Sprung von der zweiten auf die erste Stufe rotes Licht von sechshundertvierzig Nanometern ab. Die Stufe von der dritten auf die erste ist eins Komma zwei fünf mal so gross. Welche Frequenz hat das rote Licht? Und welche Wellenlänge hat das Licht aus dem grösseren Sprung?',
           notiz('E₂ → E₁: 640 nm', y=300, a='Ein Atom gibt'),
           notiz('E₃ → E₁: 1.25-mal so grosse Stufe', y=370, a='Die Stufe von der dritten'),
           notiz('gesucht: @f@ für 640 nm|und @\\lambda@ für E₃ → E₁', y=480, a='Welche Frequenz'),
           skizze(strecken=niveaus()[0] + [P((2.0, 5.65), (2.0, 2.35), TIN, dicke=4, _ein='Ein Atom gibt'), P((3.4, 6.65), (3.4, 2.35), TIN, dicke=4, _ein='Die Stufe von der dritten')],
                  texte=niveaus()[1] + [T(2.15, 3.6, '640 nm', TIN, 26, 'start', _ein='Ein Atom gibt'), T(3.55, 4.6, '?', TIN, 34, 'start', _ein='Die Stufe von der dritten')])),
        sz('Vorgehen Atom', 'Die Frequenz kommt aus c gleich Lambda mal f. Die Energie eines Photons ist h mal f, darum wächst die Frequenz im selben Verhältnis wie die Stufe. Aus der neuen Frequenz folgt die neue Wellenlänge.',
           formel(r'f_1 = \frac{c}{\lambda_1}', y=280, g=44, a='Die Frequenz kommt'),
           formel(r'E = h \cdot f \;\Rightarrow\; f_2 = 1.25 \cdot f_1', y=390, g=40, a='Die Energie eines Photons'),
           formel(r'\lambda_2 = \frac{c}{f_2}', y=510, g=44, a='Aus der neuen'),
           skizze(strecken=niveaus()[0] + [P((2.0, 5.65), (2.0, 2.35), TIN, dicke=4), P((3.4, 6.65), (3.4, 2.35), TIN, dicke=4)],
                  texte=niveaus()[1] + [T(2.15, 3.6, '640 nm', TIN, 26, 'start'), T(3.55, 4.6, '?', TIN, 34, 'start')])),
        sz('Lösung Atom', 'f eins gleich drei Komma null null mal zehn hoch acht Meter pro Sekunde durch sechshundertvierzig mal zehn hoch minus neun Meter, rund vier Komma sechs neun mal zehn hoch vierzehn Hertz. Die grössere Stufe gibt eins Komma zwei fünf mal so viel: rund fünf Komma acht sechs mal zehn hoch vierzehn Hertz. Daraus Lambda zwei gleich c durch f zwei, rund fünfhundertzwölf Nanometer: grünes Licht. Probe: sechshundertvierzig durch eins Komma zwei fünf gibt ebenfalls fünfhundertzwölf.',
           *rechnung(r'f_1 = \frac{3.00 \cdot 10^{8}\;\text{m/s}}{640 \cdot 10^{-9}\;\text{m}} \approx 4.69 \cdot 10^{14}\;\text{Hz}', y=240, g=34, a='f eins gleich', a_erg='rund vier Komma sechs neun'),
           *rechnung(r'f_2 = 1.25 \cdot 4.69 \cdot 10^{14}\;\text{Hz} \approx 5.86 \cdot 10^{14}\;\text{Hz}', y=360, g=34, a='Die grössere Stufe', a_erg='rund fünf Komma acht sechs'),
           *rechnung(r'\lambda_2 = \frac{3.00 \cdot 10^{8}\;\text{m/s}}{5.86 \cdot 10^{14}\;\text{Hz}} \approx 512\;\text{nm}', y=480, g=34, a='Daraus Lambda', a_erg='rund fünfhundertzwölf Nanometer'),
           *probe('Probe: @\\frac{640\\;\\text{nm}}{1.25}', ' = 512\\;\\text{nm}@', y=600, g=36, a_erg='gibt ebenfalls fünfhundertzwölf'),
           skizze(strecken=niveaus()[0] + [P((2.0, 5.65), (2.0, 2.35), TIN, dicke=4), P((3.4, 6.65), (3.4, 2.35), TIN, dicke=4)],
                  texte=niveaus()[1] + [T(2.15, 3.6, '640 nm', TIN, 26, 'start'), T(3.55, 4.6, '512 nm', TIN, 26, 'start', _ein='rund fünfhundertzwölf')])),
        merke('Zum Mitnehmen: Atome haben feste Energiestufen. Springt ein Elektron hinunter, nimmt ein Photon genau die Energie der Stufe mit. Ein Atom nimmt nur Photonen auf, die genau zu einer Stufe passen. Im Laser lösen Photonen gleiche Photonen aus.',
              r'E_\text{Photon} = h \cdot f', 'Sprung hinunter: Photon|nur passende Photonen werden aufgenommen|Laser: gleiche Photonen, gebündelt'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Atom', 'Die Stufe ist 1.25-mal so gross. Was gilt für das neue Licht?', ['1.25-mal so lange Welle', 'gleiche Wellenlänge, nur heller', '1.25-mal so hohe Frequenz, kürzere Welle'], 2,
                 {0: 'Mehr Energie je Photon heisst E = h · f grösser. Was macht dann f, was λ?', 1: 'Die Farbe hängt an der Energie des Photons. Bleibt die gleich?'},
                 sprich='Die Stufe ist eins Komma zwei fünf mal so gross. Was gilt für das neue Licht?',
                 rueck_sprich={0: 'Mehr Energie je Photon heisst E gleich h mal f grösser. Was macht dann f, was Lambda?', 1: 'Die Farbe hängt an der Energie des Photons. Bleibt die gleich?'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 5
assert abs(800 / 2 - 400) < 1e-12
DREH.append(dict(KOPF, titel='Wellen sehen: Kontrollfragen zu Atom und Laser', dateiname='p6-1-lp-kontrolle-licht',
    kurzbeschrieb='Fünf Fragen: ein Photon trifft ein angeregtes Atom, die dunkle Linie von Quecksilberdampf, ein doppelt so grosser Sprung, warum ein Laserstrahl gebündelt bleibt und warum ein grünes Glas grün aussieht.',
    schlagworte=['Atom', 'Photon', 'Absorption', 'Laser', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Das ist die stimulierte Emission: Das Photon löst ein zweites aus, mit gleicher Wellenlänge, gleicher Phase und gleicher Richtung. Aus einem Photon werden zwei.',
           notiz('stimulierte Emission:|zwei gleiche Photonen', y=320, ein=1.0)),
        sz('Frage 2', 'Im kalten Dampf sitzen die Elektronen auf der tiefsten Stufe. Der Sprung, der zweihundertvierundfünfzig Nanometer gibt, endet dort; umgekehrt heben genau diese Photonen ein Elektron von dort hinauf. Darum fehlen danach die zweihundertvierundfünfzig Nanometer.',
           notiz('es fehlen genau die 254 nm:|Sprung von der tiefsten Stufe', y=320, ein=1.0)),
        sz('Frage 3', 'Doppelte Stufe heisst doppelte Energie, also doppelte Frequenz. Bei gleicher Geschwindigkeit ist die Welle dann halb so lang: vierhundert Nanometer.',
           notiz('doppelte Stufe: doppeltes @f@,|halbes @\\lambda@: 400 nm', y=320, ein=1.0)),
        sz('Frage 4', 'Im Laser lösen Photonen gleiche Photonen aus, und zwischen den Spiegeln verstärken sich nur die, die genau längs laufen. Darum laufen alle in dieselbe Richtung und im Gleichtakt.',
           notiz('gleiche Richtung, gleiche Phase:|stimulierte Emission zwischen Spiegeln', y=320, ein=1.0)),
        sz('Frage 5', 'Das Glas nimmt die anderen Farben auf, das grüne Licht geht durch. Hinter dem Glas fehlt also alles ausser Grün.',
           notiz('andere Farben aufgenommen,|Grün geht durch', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein passendes Photon trifft ein Atom, das schon angeregt ist. Was geschieht?', ['Das Atom nimmt es auf und springt noch höher.', 'Es löst ein zweites, gleiches Photon aus.', 'Es geht unverändert vorbei.'], 1,
             {0: 'Das Elektron sitzt schon oben. Wohin kann es mit dem passenden Photon springen?', 2: 'Das Photon passt genau zur Stufe. Bleibt das ohne Wirkung?'}),
        wahl('Frage 2', 'Quecksilberdampf leuchtet unter anderem mit 254 nm (Ultraviolett); dieses Photon entsteht beim Sprung auf die tiefste Stufe. UV-Licht von 200 nm bis 400 nm geht durch kalten Quecksilberdampf. Was fehlt danach?', ['genau die 254 nm', 'alles ausser 254 nm', 'nichts'], 0,
             {1: 'Das Gas nimmt nur auf, was zu einem Sprung nach oben passt. Welche Photonen sind das?', 2: 'Ein Teil des Lichts passt genau zu einem Sprung von der tiefsten Stufe aus. Was geschieht mit ihm?'},
             sprich='Quecksilberdampf leuchtet unter anderem mit zweihundertvierundfünfzig Nanometern, im Ultraviolett. Dieses Photon entsteht beim Sprung auf die tiefste Stufe. UV-Licht von zweihundert bis vierhundert Nanometern geht durch kalten Quecksilberdampf. Was fehlt danach?'),
        wahl('Frage 3', 'Ein Sprung gibt Licht von 800 nm. Ein anderer Sprung im selben Atom ist doppelt so gross. Welche Wellenlänge hat sein Licht?', ['1600 nm', '800 nm', '400 nm'], 2,
             {0: 'Mehr Energie je Photon: höhere oder tiefere Frequenz?', 1: 'Ein anderer Sprung gibt andere Energie. Was bedeutet das für λ?'},
             sprich='Ein Sprung gibt Licht von achthundert Nanometern. Ein anderer Sprung im selben Atom ist doppelt so gross. Welche Wellenlänge hat sein Licht?',
             rueck_sprich={0: 'Mehr Energie je Photon: höhere oder tiefere Frequenz?', 1: 'Ein anderer Sprung gibt andere Energie. Was bedeutet das für Lambda?'}),
        wahl('Frage 4', 'Warum bleibt ein Laserstrahl auch über viele Meter schmal?', ['Der Laser ist sehr heiss.', 'Eine Linse biegt das Licht ständig nach innen.', 'Seine Photonen laufen alle in dieselbe Richtung und im Gleichtakt.'], 2,
             {0: 'Eine Glühlampe ist heisser — und ihr Licht läuft in alle Richtungen. Was ist beim Laser anders?', 1: 'Nach dem Austritt ist keine Linse mehr da. Was haben die Photonen gemeinsam?'}),
        wahl('Frage 5', 'Weisses Licht fällt durch ein grünes Glas. Warum ist das Licht danach grün?', ['Das Glas färbt das Licht grün ein.', 'Das Glas nimmt die anderen Farben auf, Grün geht durch.', 'Das Glas wandelt alle Farben in Grün um.'], 1,
             {0: 'Das Glas fügt nichts hinzu. Was nimmt es weg?', 2: 'Jedes Photon behält seine Energie. Was geschieht mit den anderen Farben?'}),
    ]))

# ================================================================== Kapitel 6: Treibhauseffekt
# Problem: Bodenstrahlung bei 15 µm → f = 2.0·10¹³ Hz; Sonnenlicht um 0.5 µm → 6.0·10¹⁴ Hz; CO₂-Bereich 13.5 bis 17 µm (430 ppm)
assert abs(C / 15e-6 - 2.0e13) < 1 and abs(C / 0.5e-6 - 6.0e14) < 1 and abs(C / 7.7e-6 - 3.896e13) < 1e10
NS5800, NS288 = 0.12621869631889754, 7.673290982313504e-07      # Höchstwerte von λ⁻⁴/(e^(c₂/λT) − 1) = λ · B_λ, λ in µm (python3)
L10 = 'exp((x-1.2)*log(10))'           # x = log10(λ/µm) + 1.2, damit die y-Achse links steht
SONNE = '%s**(-4)/(exp(14388/(%s*5800))-1)/%r' % (L10, L10, NS5800)
BODEN = '%s**(-4)/(exp(14388/(%s*288))-1)/%r' % (L10, L10, NS288)
def LX(l):
    return math.log10(l) + 1.2


def band(a, b, farbe=TIN, deckung=0.18, **kw):
    return F(rechteck(LX(a), 0, LX(b), 1.12), farbe, deckung, **kw)


def strahlung(**kw):
    """Normierte Strahlung von Sonne und Boden über λ (logarithmisch)."""
    kw.setdefault('kurven', [])
    kw['kurven'] = [{'formel': SONNE, 'von': 0.2, 'bis': 3.5, 'farbe': ORA, 'dicke': 6},
                    {'formel': BODEN, 'von': 1.4, 'bis': 3.5, 'farbe': ROT, 'dicke': 6}] + kw['kurven']
    kw.setdefault('texte', [])
    kw['texte'] = [T(LX(0.5) + 0.2, 1.0, 'Sonne', ORA, 26, 'start'), T(LX(10) + 0.35, 1.0, 'Boden', ROT, 26, 'start')] + kw['texte']
    return graf((-0.05, 3.65), (-0.16, 1.25), [[0.2, '0.1'], [1.2, '1'], [2.2, '10'], [3.2, '100']], [], 'λ [µm]', 'relativ', **kw)


def ausschnitt_co2():
    """Ausschnitt 10 bis 21 µm (x = 10 · log10(λ / 10 µm)): die Bande des Kohlendioxids bei 280 ppm (gestrichelte
    Ränder, 13.77 bis 16.73 µm) und bei 430 ppm (13.5 bis 17.0 µm), dazu die Bodenstrahlung λ · B_λ (288 K)."""
    X = lambda l: 10 * math.log10(l / 10)
    b28 = (15.25 - 1.75 * (1 + 0.25 * math.log2(280 / 430)), 15.25 + 1.75 * (1 + 0.25 * math.log2(280 / 430)))
    assert abs(b28[0] - 13.77) < 0.01 and abs(b28[1] - 16.73) < 0.01
    lam = 'exp((1+x/10)*log(10))'
    boden = '%s**(-4)/(exp(14388/(%s*288))-1)/%r' % (lam, lam, NS288)
    return graf((-0.25, 3.45), (-0.16, 1.25), [[X(l), str(l)] for l in (12, 14, 16, 18, 20)], [], 'λ [µm]', 'relativ',
                kurven=[{'formel': boden, 'von': 0, 'bis': 3.2, 'farbe': ROT, 'dicke': 6}],
                flaechen=[F(rechteck(X(b28[0]), 0, X(b28[1]), 1.12), TIN, 0.18, _aus='Der Bereich wird breiter'),
                          F(rechteck(X(13.5), 0, X(17.0), 1.12), TIN, 0.18, _ein='Der Bereich wird breiter')],
                strecken=[S((X(b28[0]), 0), (X(b28[0]), 1.12), TIN, dicke=2, gestrichelt=True, _ein='Der Bereich wird breiter'),
                          S((X(b28[1]), 0), (X(b28[1]), 1.12), TIN, dicke=2, gestrichelt=True, _ein='Der Bereich wird breiter')],
                texte=[T(X(15.25), 1.17, 'CO₂', TIN, 22), T(X(20.5), 1.0, 'Boden', ROT, 24, 'end'),
                       T(X(13.0), 0.35, '280 ppm: gestrichelt', TIN, 20, 'end', _ein='Der Bereich wird breiter')])


def atmo_skizze(schicht='Treibhausgase', **kw):
    st = [S((0.3, 1.2), (9.7, 1.2), TIN, dicke=6)] + kw.pop('strecken', [])
    fl = [F(rechteck(0.3, 5.0, 9.7, 7.0), TIN, 0.12)] + kw.pop('flaechen', [])
    tx = [T(9.6, 0.5, 'Boden', TIN, 24, 'end'), T(9.6, 7.4, schicht, TIN, 24, 'end')] + kw.pop('texte', [])
    return skizze(strecken=st, flaechen=fl, texte=tx, **kw)


DREH.append(dict(KOPF, titel='Wellen sehen: der Treibhauseffekt', dateiname='p6-1-lp-treibhaus',
    kurzbeschrieb='Warum die Atmosphäre Sonnenlicht durchlässt, die Wärmestrahlung des Bodens aber zum Teil zurückhält: Treibhausgase nehmen Infrarot in bestimmten Wellenlängenbereichen auf und strahlen es in alle Richtungen wieder ab — und ein vorgerechnetes Problem: die Frequenz der Bodenstrahlung bei 15 µm.',
    schlagworte=['Treibhauseffekt', 'Infrarot', 'Absorption', 'Kohlendioxid', 'Wasserdampf', 'Methan', 'Spektrum'], _probe=EIN % 6,
    szenen=[
        sz('Zwei Strahlungen', 'Die Sonne ist rund fünftausendfünfhundert Grad heiss. Sie strahlt vor allem um einen halben Mikrometer, im sichtbaren Licht. Der Boden hat im Mittel rund fünfzehn Grad. Er strahlt viel langwelliger, im Infrarot um zehn Mikrometer. Das Bild zeigt beide Kurven flächentreu und auf gleicher Höhe; ihre Gipfel liegen darum etwas weiter rechts.',
           notiz('Sonne: um 0.5 µm, sichtbar', y=290, a='Sie strahlt vor allem'),
           notiz('Boden: um 10 µm, Infrarot', y=400, a='Er strahlt viel'),
           notiz('Kurven flächentreu, auf gleiche Höhe;|Gipfel darum bei 0.6 µm und 13 µm', y=560, g=30, a='Das Bild zeigt beide'),
           strahlung(flaechen=[F(rechteck(LX(0.38), 0, LX(0.78), 1.12), ORA, 0.12, _ein='im sichtbaren Licht')])),
        sz('Durchlässig', 'Stickstoff und Sauerstoff, fast die ganze Luft, lassen beide Strahlungen durch. Das Sonnenlicht kommt darum weitgehend bis zum Boden und wärmt ihn. Nur das Ultraviolett der Sonne nimmt zum grossen Teil schon hoch oben das Ozon auf.',
           notiz('Stickstoff und Sauerstoff:|lassen beides durch', y=290, a='Stickstoff'),
           notiz('Licht kommt bis zum Boden', y=440, a='Das Sonnenlicht'),
           notiz('Ultraviolett: grossteils vom|Ozon hoch oben aufgenommen', y=520, a='Nur das Ultraviolett'),
           atmo_skizze('Luft: Stickstoff, Sauerstoff', strecken=[P((1.5, 9.4), (1.5, 1.5), ORA, dicke=8, _ein='Das Sonnenlicht')],
                       texte=[T(1.9, 8.8, 'Licht', ORA, 26, 'start', _ein='Das Sonnenlicht')])),
        sz('Aufnahme', 'Anders die Treibhausgase: Wasserdampf, Kohlendioxid und Methan nehmen Infrarot auf, jedes Gas in eigenen Wellenlängenbereichen. Diese Bereiche liegen dort, wo der Boden strahlt, kaum dort, wo die Sonne strahlt. Zwischen acht und dreizehn Mikrometern bleibt ein Fenster weitgehend offen; darin nimmt nur das Ozon schmal um neun Komma sechs Mikrometer auf.',
           notiz('Wasserdampf, Kohlendioxid,|Methan: nehmen Infrarot auf', y=270, a='Anders die Treibhausgase'),
           notiz('je eigene Bereiche', y=420, a='jedes Gas in eigenen'),
           notiz('Fenster: 8 bis 13 µm,|darin Ozon um 9.6 µm', y=520, a='Zwischen acht', v=0.8),
           strahlung(flaechen=[band(5.5, 7.5, _ein='Wasserdampf'), band(20, 200, _ein='Wasserdampf'), band(13.5, 17.0, _ein='Kohlendioxid'), band(7.4, 8.0, _ein='und Methan'), band(9.3, 10.1, _ein='nur das Ozon')],
                     strecken=[S((LX(6.65), 0.88), (LX(7.7), 0.97), TIN, dicke=2, _ein='und Methan')],
                     texte=[T(LX(6.0), 1.17, 'H₂O', TIN, 22, _ein='Wasserdampf'), T(LX(60), 1.17, 'H₂O', TIN, 22, _ein='Wasserdampf'),
                            T(LX(15.1), 1.17, 'CO₂', TIN, 22, _ein='Kohlendioxid'), T(LX(6.6), 0.85, 'CH₄', TIN, 22, 'end', _ein='und Methan'),
                            T(LX(9.7), 1.17, 'O₃', TIN, 22, _ein='nur das Ozon'), T(LX(11.4), 0.35, 'Fenster', TIN, 22, _ein='Zwischen acht', _ein_versatz=0.8)])),
        sz('Wieder abstrahlen', 'Was ein Gas aufnimmt, strahlt es wieder ab, in alle Richtungen, also auch zurück zum Boden. Der Boden bekommt so zum Sonnenlicht noch diese Gegenstrahlung und wird wärmer: Statt rund minus achtzehn Grad hat er im Mittel rund plus fünfzehn. Das ist der natürliche Treibhauseffekt. Die Gase spiegeln nichts, sie nehmen auf und strahlen neu ab.',
           notiz('aufnehmen, in alle Richtungen|wieder abstrahlen', y=270, a='Was ein Gas aufnimmt'),
           notiz('Boden: rund +15 °C statt −18 °C', y=420, a='Statt rund'),
           notiz('nicht spiegeln: aufnehmen|und neu abstrahlen', y=530, a='Die Gase spiegeln'),
           atmo_skizze(strecken=[P((1.5, 9.4), (1.5, 1.5), ORA, dicke=8), P((4.5, 1.5), (4.5, 5.8), ROT, dicke=8)]
                       + [P((4.5, 6.0), (4.5 + dx, 6.0 + dy), ROT, dicke=5, _ein='in alle Richtungen') for dx, dy in [(0, 2.6), (1.9, 1.9), (2.6, 0), (1.9, -1.9), (-1.9, 1.9), (-2.6, 0)]]
                       + [P((7.5, 4.9), (7.5, 1.5), ROT, dicke=8, _ein='also auch zurück')],
                       texte=[T(1.9, 8.8, 'Licht', ORA, 26, 'start'), T(4.8, 3.0, 'Bodenstrahlung', ROT, 24, 'start'), T(7.8, 3.0, 'zurück', ROT, 24, 'start', _ein='also auch zurück')])),
        sz('Mehr Kohlendioxid', 'Vor der Industrialisierung enthielt die Luft rund zweihundertachtzig ppm Kohlendioxid, heute rund vierhundertdreissig. Mehr Gas nimmt auch an den Rändern seines Bereichs auf: Der Bereich wird breiter, mehr Bodenstrahlung bleibt in der Atmosphäre. Der Treibhauseffekt wird stärker. Am Sonnenlicht ändert das fast nichts. Wie viel wärmer es dadurch wird, rechnet das Leitprogramm Wärme.',
           notiz('280 ppm → 430 ppm', y=270, a='Vor der Industrialisierung'),
           notiz('Bereich wird breiter|→ verstärkter Treibhauseffekt', y=380, a='Der Bereich wird breiter'),
           notiz('Sonnenlicht: fast unverändert', y=540, a='Am Sonnenlicht'),
           ausschnitt_co2()),
        sz('Problem Satellit', 'Jetzt ein ganzes Problem. Ein Satellit misst die Wärmestrahlung, die bei fünfzehn Mikrometern von unten kommt. Welche Frequenz hat diese Strahlung? Und welches Gas nimmt sie auf dem Weg nach oben auf?',
           notiz('Strahlung bei 15 µm', y=300, a='Ein Satellit misst'),
           notiz('gesucht: @f@ und das Gas', y=410, a='Welche Frequenz'),
           strahlung(flaechen=[band(5.5, 7.5), band(20, 200), band(13.5, 17.0), band(7.4, 8.0), band(9.3, 10.1)],
                     strecken=[S((LX(15), -0.05), (LX(15), 1.12), TIN, dicke=3, gestrichelt=True, _ein='bei fünfzehn Mikrometern')],
                     texte=[T(LX(15), -0.11, '15', TIN, 22, _ein='bei fünfzehn Mikrometern')])),
        sz('Vorgehen Satellit', 'Die Wellenlänge in Meter umrechnen und f gleich c durch Lambda rechnen. Für das Gas schaust du, in welchem Bereich fünfzehn Mikrometer liegen.',
           formel(r'15\;\mu\text{m} = 1.5 \cdot 10^{-5}\;\text{m}', y=290, g=42, a='Die Wellenlänge'),
           formel(r'f = \frac{c}{\lambda}', y=400, g=46, a='und f gleich'),
           notiz('Gas: Bereich ablesen', y=510, a='Für das Gas'),
           strahlung(flaechen=[band(5.5, 7.5), band(20, 200), band(13.5, 17.0), band(7.4, 8.0), band(9.3, 10.1)],
                     strecken=[S((LX(15), -0.05), (LX(15), 1.12), TIN, dicke=3, gestrichelt=True)])),
        sz('Lösung Satellit', 'f gleich drei Komma null null mal zehn hoch acht Meter pro Sekunde durch eins Komma fünf mal zehn hoch minus fünf Meter, zwei Komma null mal zehn hoch dreizehn Hertz. Fünfzehn Mikrometer liegen im Bereich des Kohlendioxids. Probe: Sonnenlicht um einen halben Mikrometer hat sechs mal zehn hoch vierzehn Hertz, dreissigmal mehr, und die Wellenlänge ist dreissigmal kürzer. Das passt.',
           *rechnung(r'f = \frac{3.00 \cdot 10^{8}\;\text{m/s}}{1.5 \cdot 10^{-5}\;\text{m}} = 2.0 \cdot 10^{13}\;\text{Hz}', y=250, g=36, a='f gleich', a_erg='zwei Komma null mal zehn hoch dreizehn'),
           notiz('15 µm: Bereich von CO₂', y=380, a='Fünfzehn Mikrometer'),
           *probe('Probe: 0.5 µm @\\rightarrow 6.0 \\cdot 10^{14}\\;\\text{Hz}@', ',|30-mal kürzer, 30-mal höher', y=480, g=36, a='sechs mal zehn hoch vierzehn', a_erg='dreissigmal mehr'),
           strahlung(flaechen=[band(5.5, 7.5), band(20, 200), band(13.5, 17.0), band(7.4, 8.0), band(9.3, 10.1)],
                     strecken=[S((LX(15), -0.05), (LX(15), 1.12), TIN, dicke=3, gestrichelt=True)],
                     texte=[T(LX(15.1), 1.17, 'CO₂', TIN, 22, _ein='Fünfzehn Mikrometer')])),
        merke('Zum Mitnehmen: Die Atmosphäre lässt das kurzwellige Sonnenlicht weitgehend durch. Die langwellige Wärmestrahlung des Bodens nehmen Treibhausgase in ihren Bereichen auf und strahlen sie in alle Richtungen wieder ab, auch zurück. Mehr Treibhausgas verstärkt den Effekt.',
              r'\text{Licht: kurz} \quad \text{Bodenstrahlung: lang}', 'Gase nehmen Infrarot auf|und strahlen in alle Richtungen ab|mehr Gas: stärkerer Effekt'),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Satellit', 'Wie rechnest du die Frequenz?', ['f = λ / c', 'f = c / λ', 'f = c · λ'], 1,
                 {0: 'Prüfe die Einheit: m durch m/s gibt Sekunden, nicht Hertz.', 2: 'Prüfe die Einheit: m/s mal m gibt keine Hertz.'},
                 sprich='Wie rechnest du die Frequenz?',
                 rueck_sprich={0: 'Prüfe die Einheit: Meter durch Meter pro Sekunde gibt Sekunden, nicht Hertz.', 2: 'Prüfe die Einheit: Meter pro Sekunde mal Meter gibt keine Hertz.'}, kopf='Dein Vorgehen')]))

# ------------------------------------------------------------------ Kontrollfragen Kapitel 6
DREH.append(dict(KOPF, titel='Wellen sehen: Kontrollfragen zum Treibhauseffekt', dateiname='p6-1-lp-kontrolle-treibhaus',
    kurzbeschrieb='Fünf Fragen: warum Stickstoff und Sauerstoff keine Treibhausgase sind, wen Methan bei 7.7 µm trifft, was mehr Kohlendioxid am Sonnenlicht ändert, was das Fenster ist und ob die Gase spiegeln.',
    schlagworte=['Treibhauseffekt', 'Infrarot', 'Absorption', 'Kontrollfragen'], _probe=KTRL % 6,
    szenen=[
        sz('Frage 1', 'Stickstoff und Sauerstoff machen fast die ganze Luft aus, nehmen aber weder Licht noch Wärmestrahlung nennenswert auf. Darum tragen sie zum Treibhauseffekt nichts bei.',
           notiz('nehmen kaum Infrarot auf', y=320, ein=1.0)),
        sz('Frage 2', 'Sieben Komma sieben Mikrometer liegen im Infrarot. Dort strahlt der Boden, die Sonne fast nicht. Methan trifft also die Bodenstrahlung.',
           notiz('7.7 µm: Infrarot,|die Bodenstrahlung', y=320, ein=1.0)),
        sz('Frage 3', 'Kohlendioxid nimmt vor allem im Infrarot um fünfzehn Mikrometer auf. Sichtbares Licht geht durch. Am Sonnenlicht ändert sich darum kaum etwas.',
           notiz('Sonnenlicht: kaum verändert', y=320, ein=1.0)),
        sz('Frage 4', 'Zwischen acht und dreizehn Mikrometern nehmen die Gase wenig auf, nur das Ozon in einem schmalen Bereich um neun Komma sechs Mikrometer. Durch dieses Fenster entweicht der grösste Teil der Bodenstrahlung, die direkt ins All gelangt.',
           notiz('8 bis 13 µm: kaum Aufnahme,|Strahlung geht ins All', y=320, ein=1.0)),
        sz('Frage 5', 'Die Gase spiegeln nicht. Sie nehmen die Wärmestrahlung auf und strahlen sie in alle Richtungen wieder ab, ein Teil davon zurück zum Boden.',
           notiz('aufnehmen und in alle|Richtungen abstrahlen', y=320, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Warum zählen Stickstoff und Sauerstoff nicht zu den Treibhausgasen?', ['Es hat zu wenig davon in der Luft.', 'Sie verschlucken das Sonnenlicht.', 'Sie nehmen Wärmestrahlung kaum auf.'], 2,
             {0: 'Zusammen sind sie fast die ganze Luft. Woran liegt es also?', 1: 'Dann wäre es am Boden dunkel. Was tun sie mit der Wärmestrahlung?'}),
        wahl('Frage 2', 'Methan nimmt Strahlung um 7.7 µm auf. Welche Strahlung trifft das vor allem?', ['die Wärmestrahlung des Bodens', 'das Sonnenlicht', 'beide gleich stark'], 0,
             {1: 'Die Sonne strahlt vor allem um 0.5 µm. Liegt 7.7 µm dort?', 2: 'Wo strahlt die Sonne, wo der Boden?'},
             sprich='Methan nimmt Strahlung um sieben Komma sieben Mikrometer auf. Welche Strahlung trifft das vor allem?',
             rueck_sprich={1: 'Die Sonne strahlt vor allem um einen halben Mikrometer. Liegt sieben Komma sieben Mikrometer dort?', 2: 'Wo strahlt die Sonne, wo der Boden?'}),
        wahl('Frage 3', 'Es kommt mehr Kohlendioxid in die Luft. Was ändert sich am Sonnenlicht, das den Boden erreicht?', ['deutlich weniger Licht', 'kaum etwas', 'deutlich mehr Licht'], 1,
             {0: 'In welchem Bereich nimmt Kohlendioxid auf — im sichtbaren Licht?', 2: 'Kohlendioxid erzeugt kein Licht. Wo nimmt es auf?'}),
        wahl('Frage 4', 'Was ist das «Fenster» zwischen 8 µm und 13 µm?', ['Dort nehmen die Gase besonders stark auf.', 'Dort strahlt die Sonne am stärksten.', 'Dort geht Bodenstrahlung fast ungehindert ins All.'], 2,
             {0: 'Ein Fenster ist offen. Was geht dort durch?', 1: 'Die Sonne strahlt am stärksten um 0.5 µm. Wer strahlt um 10 µm?'},
             sprich='Was ist das Fenster zwischen acht und dreizehn Mikrometern?',
             rueck_sprich={0: 'Ein Fenster ist offen. Was geht dort durch?', 1: 'Die Sonne strahlt am stärksten um einen halben Mikrometer. Wer strahlt um zehn Mikrometer?'}),
        wahl('Frage 5', 'Jemand sagt: «Die Treibhausgase spiegeln die Wärmestrahlung zum Boden zurück wie ein Glasdach.» Was stimmt?', ['Genau so ist es.', 'Sie nehmen sie auf und strahlen sie in alle Richtungen wieder ab.', 'Sie vernichten sie.'], 1,
             {0: 'Ein Spiegel wirft alles in eine Richtung zurück. Wohin strahlt ein Gas, das Strahlung aufgenommen hat?', 2: 'Energie wird nicht vernichtet. Wohin geht sie?'},
             sprich='Jemand sagt: Die Treibhausgase spiegeln die Wärmestrahlung zum Boden zurück wie ein Glasdach. Was stimmt?'),
    ]))


# ------------------------------------------------------------------ schreiben
# --behalte: schreibt die Drehbücher neu, übernimmt aber «dauer» jeder Szene, deren Name und Sprechertext
# gleich geblieben sind, und meldet die Szenen (ab 1) und Fragen, die neu zu sprechen sind:
#   build-clip-ton.py <clip> --szenen <liste>; build-clip-fragen-ton.py <clip> --fragen <liste>
BEHALTE = '--behalte' in sys.argv


def gleichmaessig(d):
    """Befund 12: Jede laufende Welle (Kurve mit mehreren Stützpunkten oder wandernden Grenzen) gleichmässig."""
    for s_ in d['szenen']:
        for e in s_['elemente']:
            for k in e.get('kurven', []) if e.get('typ') == 'graf' else []:
                if len(k.get('bewegung', [])) > 1 or k.get('grenzen') or k.get('_bewegung') or k.get('_grenzen'):
                    k['gleichmaessig'] = True


for d_ in DREH:
    gleichmaessig(d_)
if __name__ == '__main__':
    for d in DREH:
        pfad = os.path.join(CLIPS, d['dateiname'] + '.json')
        if NUR and d['dateiname'] not in NUR:
            continue
        if os.path.exists(pfad) and not (NEU or BEHALTE):
            print('vorhanden, unverändert:', d['dateiname'])
            continue
        neu_sz, neu_fr = [], []
        if BEHALTE and os.path.exists(pfad):
            alt = json.load(open(pfad, encoding='utf-8'))
            alt_sz = {(s_['name'], s_['sprecher']): s_.get('dauer') for s_ in alt['szenen']}
            alt_name = {s_['name']: s_.get('dauer') for s_ in alt['szenen']}
            for k, s_ in enumerate(d['szenen'], 1):
                if alt_sz.get((s_['name'], s_['sprecher'])):
                    s_['dauer'] = alt_sz[(s_['name'], s_['sprecher'])]
                else:
                    neu_sz.append(k)
                    # alte Dauer behalten, bis neu gesprochen ist: --szenen vergleicht die Spurlänge mit der Summe
                    # der Dauern und bricht sonst ab («Spur … passt nicht mehr zusammen»)
                    if alt_name.get(s_['name']):
                        s_['dauer'] = alt_name[s_['name']]
            alt_fr = alt.get('fragen', [])
            for k, f_ in enumerate(d.get('fragen', []), 1):
                a_ = alt_fr[k - 1] if k <= len(alt_fr) else {}
                schl = ('sprich', 'rueck_sprich', 'text', 'optionen', 'falsch_sprich', 'fallen', 'richtig')
                if any(json.dumps(a_.get(x), sort_keys=True) != json.dumps(f_.get(x), sort_keys=True) for x in schl):
                    neu_fr.append(k)
        with open(pfad, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print('geschrieben:', d['dateiname'], len(d['szenen']), 'Szenen',
              ('| neu sprechen: Szenen %s | Fragen %s' % (','.join(map(str, neu_sz)) or '-', ','.join(map(str, neu_fr)) or '-')) if BEHALTE else '')
