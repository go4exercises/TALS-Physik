"""ARCHIV, VERALTET — bricht beim Start ab. Erzeugte einst die zehn Drehbücher des Leitprogramms Wärmeausdehnung und Gase (clips/p5-3-lp-*.json).

  python3 scripts/lp/ausdehnung/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/ausdehnung/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/ausdehnung/clips.py --neu p5-3-lp-laenge …   # nur diese

Archiv-Werkzeug wie scripts/lp/hydrostatik/clips.py: Nach der Vertonung sind die JSONs in clips/
die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf mit --neu
würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7). Die Antwortbilder
der Kontrollclips setzt antworten.py (wiederholbar), die Einblendezeiten scripts/lp/kinematik/anker.py.

Farben (Theme begreifbar-schlicht, wie im Leitprogramm): 1 Bernstein = Ausdehnung (Δl, ΔV, Δh) und der
neue Zustand, 2 Orange = Temperatur, 3 Grün = Volumen, 4 Rot = Druck, 5 Tinte = Ausgangszustand, Gefässe.
Bilder: Aufnahmen der Simulationen (clips/bilder/p5-3-lp-*.jpg, Plan aufnahme.json) und gezeichnete
Skizzen und Diagramme (graf). Zahlen im Sprechertext ausgeschrieben (CLAUDE.md). Kontrollclips: neue
Beispiele (nicht Clip, Leiste, Aufgaben oder Mini-Checks der Themenseite), richtige Antwort an wechselnden
Stellen, jede falsche Antwort ein benannter Fehler, Lösung erst nach der Antwort.
"""

import sys
# VERALTET (Prüfung 07./08.10.2026): Die Drehbücher clips/p5-3-lp-*.json sind die Quelle und weichen
# von diesem Archiv inzwischen ab (neue Kontrollfragen, Ebenen, Einblendezeiten). Ein Lauf würde die
# geprüfte Fassung zurückdrehen — darum bricht das Skript hier ab. Korrekturen direkt im JSON.
sys.exit('clips.py ist veraltet und nur Archiv: Quelle sind die JSONs in clips/ (siehe README, Abschnitt Prüfung). Nichts geschrieben.')

import json
import math
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv
NUR = [a for a in sys.argv[1:] if not a.startswith('--')]
AUS, TEMP, VOL, DRU, TIN = 1, 2, 3, 4, 5

KOPF = {
    'themenbereich': 'Thermodynamik · BM', 'lerngebiet': '5 · Thermodynamik',
    'lektion': ['p5-3'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-07', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Ausdehnung sehen', 'nachlauf': 2.6, 'probe': True,
}
JETZT = {'name': 'Jetzt du', 'layout': 'zentriert', 'oben': 200,
         'sprecher': 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
         'elemente': [{'typ': 'titel', 'text': 'Jetzt du', 'x': 150, 'y': 280, 'groesse': 86},
                      {'typ': 'notiz', 'text': 'Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.',
                       'x': 150, 'y': 430, 'groesse': 50, 'farbe': 'blau', 'ein': 0.6}]}
EIN = 'Einführungsclip des Leitprogramms Wärmeausdehnung und Gase, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Wärmeausdehnung und Gase, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
K1 = r'\;\tfrac{1}{\text{K}}'


# ------------------------------------------------------------------ Bausteine
def formel(t, y=300, g=46, anker=None, ein=0.8):
    e = {'typ': 'formel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'ein': ein}
    if anker:
        e['_anker'] = anker
    return e


def notiz(t, y=460, anker=None, ein=2.4, g=44, farbe='tinte'):
    e = {'typ': 'notiz', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'farbe': farbe, 'ein': ein}
    if anker:
        e['_anker'] = anker
    return e


def titel(t, y=280, g=72):
    return {'typ': 'titel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g}


def bild(datei, anker=None, ein=0.05, versatz=None):
    e = {'typ': 'bild', 'datei': 'bilder/' + datei + '.jpg', 'x': 1050, 'y': 180, 'breite': 640, 'abstand': 0, 'anim': 'fade', 'ein': ein}
    if anker:
        e['_anker'] = anker
    if versatz:
        e['_versatz'] = versatz
    return e


def graf(xb, yb, xt=(), yt=(), xname='', yname='', anker=None, ein=0.05, achsen=True, **kw):
    g = {'typ': 'graf', 'x': 1010, 'y': 175, 'breite': 760, 'hoehe': 760, 'abstand': 0, 'anim': 'fade', 'ein': ein,
         'pfeile': achsen, 'xbereich': list(xb), 'ybereich': list(yb),
         'xteilung': [v if isinstance(v, list) else [v, ('%g' % v).replace('-', '−')] for v in xt] or [[1e9, '']],
         'yteilung': [v if isinstance(v, list) else [v, ('%g' % v).replace('-', '−')] for v in yt] or [[1e9, '']],
         'xname': xname, 'yname': yname}
    if not achsen:
        g['achsen'] = False
    g.update(kw)
    if anker:
        g['_anker'] = anker
    return g


def ebene(xb, yb, anker=None, ein=0.05, **kw):
    """deckungsgleiche Ebene ohne Achsen über einem graf mit demselben Fenster"""
    return graf(xb, yb, anker=anker, ein=ein, achsen=False, **kw)


def S(von, bis, farbe=TIN, dicke=4, **kw):
    d = {'von': [round(von[0], 4), round(von[1], 4)], 'bis': [round(bis[0], 4), round(bis[1], 4)], 'farbe': farbe, 'dicke': dicke}
    d.update(kw)
    return d


def P(von, bis, farbe, dicke=6, **kw):
    return S(von, bis, farbe, dicke, pfeil=True, **kw)


def T(x, y, text, farbe=TIN, groesse=28, anker='middle'):
    return {'bei': [round(x, 4), round(y, 4)], 'text': text, 'farbe': farbe, 'groesse': groesse, 'anker': anker}


def F(pts, farbe=TIN, deckung=0.15, **kw):
    d = {'punkte': [[round(x, 4), round(y, 4)] for x, y in pts], 'farbe': farbe, 'deckung': deckung}
    d.update(kw)
    return d


def rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def umriss(x0, y0, x1, y1, farbe=TIN, dicke=4, **kw):
    p = rechteck(x0, y0, x1, y1)
    return [S(p[i], p[(i + 1) % 4], farbe, dicke, **kw) for i in range(4)]


def kreis(cx, cy, r, farbe=TIN, dicke=4):
    return [{'formel': '%g%+g*sqrt(abs(%g-(x-(%g))*(x-(%g))))' % (cy, vz, r * r, cx, cx), 'von': cx - r, 'bis': cx + r,
             'farbe': farbe, 'dicke': dicke, 'n': 200} for vz in (1, -1)]


def sz(name, sprecher, *elemente):
    return {'name': name, 'layout': 'zentriert', 'oben': 200, 'sprecher': sprecher, 'elemente': list(elemente)}


def wahl(szene, text, optionen, richtig, rueck, sprich=None, rueck_sprich=None, kopf=None):
    f = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'text': text, 'optionen': optionen, 'richtig': richtig,
         'rueck': {str(k): v for k, v in rueck.items()}}
    if kopf:
        f['kopf'] = kopf
    f['sprich'] = sprich or text
    f['rueck_sprich'] = {str(k): v for k, v in (rueck_sprich or rueck).items()}
    return f


DREH = []

# ================================================================== Kapitel 1: Länge
ST = 12e-6
# Teilchen kalt (Abstand 1.3) und warm (1.55, stark übertrieben)
kalt = [k for i in range(6) for k in kreis(1.2 + 1.3 * i, 7.0, 0.42, TIN, 4)]
warm = [k for i in range(6) for k in kreis(1.2 + 1.55 * i, 3.4, 0.42, AUS, 4)]
rohr = (umriss(1.0, 4.6, 9.0, 5.4, TIN, 4) + [S((0.6, 3.8), (0.6, 6.2), TIN, 10), S((9.4, 3.8), (9.4, 6.2), TIN, 10)])
DREH.append(dict(KOPF, titel='Ausdehnung sehen: der Stab wird länger', dateiname='p5-3-lp-laenge',
    kurzbeschrieb='Warum ein Stab beim Erwärmen länger wird, die Formel Δl = α · l₀ · ΔT mit der Temperaturdifferenz, das Abkühlen — und ein vorgerechnetes Problem: die Fernwärmeleitung.',
    schlagworte=['Längenausdehnung', 'Ausdehnungskoeffizient', 'Temperaturdifferenz', 'Dehnungsbogen', 'Fernwärme'], _probe=EIN % 1,
    szenen=[
        sz('Teilchen', 'Wird ein Stab wärmer, schwingen seine Teilchen heftiger. Sie werden dabei nicht grösser, aber ihr Abstand wächst. Über die ganze Länge zusammengezählt wird der Stab messbar länger.',
           titel('Warum wird ein Stab länger?', g=62),
           notiz('Teilchen gleich gross,|Abstand grösser', y=430, anker='ihr Abstand wächst'),
           ebene([0, 10], [0, 10], ein=0.3, kurven=kalt, texte=[T(0.3, 8.3, 'kalt', TIN, 30, 'start')]),
           ebene([0, 10], [0, 10], anker='ihr Abstand wächst', kurven=warm,
                 strecken=[S((7.7, 6.2), (7.7, 2.3), TIN, 2, gestrichelt=True), P((7.7, 2.3), (9.0, 2.3), AUS, 5)],
                 texte=[T(0.3, 4.7, 'warm', AUS, 30, 'start'), T(8.35, 1.5, 'Δl', AUS, 30)])),
        sz('Formel', 'Die Längenänderung Delta l ist proportional zur Anfangslänge l null und zur Temperaturänderung Delta T. Dazu kommt ein Faktor alpha, der vom Material abhängt. Stahl hat zwölf Millionstel pro Kelvin, Aluminium dreiundzwanzig Komma acht Millionstel: Es dehnt sich fast doppelt so stark aus.',
           formel(r'\Delta l = \alpha \cdot l_0 \cdot \Delta T', y=280, g=56, anker='Die Längenänderung'),
           notiz(r'Stahl: @\alpha = 12 \cdot 10^{-6}' + K1 + '@', y=420, anker='Stahl hat'),
           notiz(r'Aluminium: @\alpha = 23.8 \cdot 10^{-6}' + K1 + '@', y=520, anker='Aluminium dreiundzwanzig'),
           bild('p5-3-lp-laenge-st20', ein=0.05),
           bild('p5-3-lp-laenge-st40', anker='zur Temperaturänderung'),
           bild('p5-3-lp-laenge-st60', anker='zur Temperaturänderung', versatz=0.9),
           bild('p5-3-lp-laenge-al60', anker='Aluminium dreiundzwanzig')),
        sz('Differenz', 'Delta T ist eine Temperaturdifferenz: die zweite Temperatur minus die erste. In Kelvin ist sie gleich gross wie in Grad Celsius. Kühlt der Stab ab, ist Delta T negativ, und der Stab wird kürzer. Die neue Länge ist l null plus Delta l.',
           formel(r'\Delta T = \vartheta_2 - \vartheta_1', y=280, g=52, anker='Delta T ist'),
           notiz('Abkühlen: @\\Delta T \\lt 0@, @\\Delta l \\lt 0@', y=400, anker='Kühlt der Stab'),
           formel(r'l = l_0 + \Delta l', y=530, g=52, anker='Die neue Länge'),
           bild('p5-3-lp-laenge-st20', ein=0.05),
           bild('p5-3-lp-laenge-st0', anker='Kühlt der Stab'),
           bild('p5-3-lp-laenge-stm20', anker='Kühlt der Stab', versatz=0.9)),
        sz('Problem Fernwärme', 'Jetzt ein ganzes Problem. Eine Fernwärmeleitung aus Stahl ist zwischen zwei Fixpunkten hundertzwanzig Meter lang. Sie wird bei zehn Grad eingebaut. Im Betrieb fliesst Wasser von neunzig Grad hindurch. Um wie viel wird die Leitung länger?',
           notiz('Stahlrohr, 120 m lang,|eingebaut bei 10 °C', y=300, anker='Eine Fernwärmeleitung'),
           notiz('im Betrieb: 90 °C', y=430, anker='Im Betrieb'),
           notiz('gesucht: @\\Delta l@', y=540, anker='Um wie viel'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=rohr,
                 flaechen=[F(rechteck(1.0, 4.6, 9.0, 5.4), TIN, 0.12)],
                 texte=[T(5, 6.3, '120 m', TIN, 32), T(0.6, 3.1, 'Fixpunkt', TIN, 24), T(9.4, 3.1, 'Fixpunkt', TIN, 24)]),
           ebene([0, 10], [0, 10], anker='Im Betrieb', flaechen=[F(rechteck(1.0, 4.6, 9.0, 5.4), TEMP, 0.35)],
                 texte=[T(5, 3.8, 'Wasser 90 °C', TEMP, 30)])),
        sz('Vorgehen Fernwärme', 'In die Formel gehört die Änderung: neunzig Grad minus zehn Grad, also achtzig Kelvin. Alpha für Stahl steht in der Tabelle, zwölf Millionstel pro Kelvin, und l null sind hundertzwanzig Meter.',
           formel(r'\Delta T = 90\;^\circ\text{C} - 10\;^\circ\text{C} = 80\;\text{K}', y=300, g=40, anker='neunzig Grad minus'),
           notiz(r'@\alpha = 12 \cdot 10^{-6}' + K1 + r'@|@l_0 = 120\;\text{m}@', y=440, anker='Alpha für Stahl'),
           graf([-12, 105], [-30, 87], [0, 20, 40, 60, 80, 100], [], 'ϑ [°C]', '', ein=0.05,
                strecken=[S((10, 0), (10, 30), TEMP, 4, gestrichelt=True), S((90, 0), (90, 30), TEMP, 4, gestrichelt=True)],
                punkte=[{'x': 10, 'y': 0, 'farbe': TIN}, {'x': 90, 'y': 0, 'farbe': TEMP}],
                texte=[T(10, 36, 'eingebaut', TIN, 26), T(90, 36, 'Betrieb', TEMP, 26)]),
           ebene([-12, 105], [-30, 87], anker='neunzig Grad minus', strecken=[P((10, 18), (90, 18), TEMP, 5)],
                 texte=[T(50, 24, 'ΔT = 80 K', TEMP, 32)])),
        sz('Lösung Fernwärme', 'Delta l gleich alpha mal l null mal Delta T: zwölf Millionstel mal hundertzwanzig Meter mal achtzig Kelvin. Das sind null Komma eins eins fünf zwei Meter, rund hundertfünfzehn Millimeter. Probe: Alpha mal Delta T ist knapp ein Tausendstel. Ein Tausendstel von hundertzwanzig Metern sind zwölf Zentimeter. Das passt. Darum braucht die Leitung Dehnungsbogen.',
           formel(r'\Delta l = \alpha \cdot l_0 \cdot \Delta T = 12 \cdot 10^{-6}' + K1 + r' \cdot 120\;\text{m} \cdot 80\;\text{K}', y=290, g=32, anker='Delta l gleich'),
           formel(r'= 0.1152\;\text{m} \approx 115\;\text{mm}', y=390, g=42, anker='Das sind null Komma'),
           notiz('Probe: @\\alpha \\cdot \\Delta T \\approx 0.001@|ein Tausendstel von 120 m: 12 cm', y=500, g=40, anker='Probe'),
           graf([-12, 105], [-15, 132], [20, 40, 60, 80, 100], [25, 50, 75, 100, 125], 'ΔT [K]', 'Δl [mm]', ein=0.05,
                strecken=[S((0, 0), (100, 144), AUS, 5)]),
           ebene([-12, 105], [-15, 132], anker='Das sind null Komma',
                 strecken=[S((80, 0), (80, 115.2), TIN, 3, gestrichelt=True), S((0, 115.2), (80, 115.2), TIN, 3, gestrichelt=True)],
                 punkte=[{'x': 80, 'y': 115.2, 'farbe': AUS, 'beschriftung': '(80 K; 115 mm)', 'beschriftung_bei': [52, 124], 'anker': 'middle'}])),
        sz('Merke', 'Zum Mitnehmen: Die Längenänderung ist alpha mal Anfangslänge mal Temperaturänderung. In die Formel gehört immer die Differenz der Temperaturen.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\Delta l = \alpha \cdot l_0 \cdot \Delta T', y=420, g=52, ein=0.4),
           notiz('@\\Delta T = \\vartheta_2 - \\vartheta_1@ in K', y=560, ein=1.2)),
        JETZT,
    ]))

# ================================================================== Kapitel 2: Volumen
w0 = umriss(1.5, 1.5, 6.0, 6.0, TIN, 4, gestrichelt=True) + [S((1.5, 6.0), (3.0, 7.5), TIN, 3, gestrichelt=True), S((6.0, 6.0), (7.5, 7.5), TIN, 3, gestrichelt=True), S((3.0, 7.5), (7.5, 7.5), TIN, 3, gestrichelt=True), S((6.0, 1.5), (7.5, 3.0), TIN, 3, gestrichelt=True), S((7.5, 3.0), (7.5, 7.5), TIN, 3, gestrichelt=True)]
w1 = umriss(1.5, 1.5, 6.8, 6.8, AUS, 5) + [S((1.5, 6.8), (3.3, 8.6), AUS, 4), S((6.8, 6.8), (8.6, 8.6), AUS, 4), S((3.3, 8.6), (8.6, 8.6), AUS, 4), S((6.8, 1.5), (8.6, 3.3), AUS, 4), S((8.6, 3.3), (8.6, 8.6), AUS, 4)]
pf3 = [P((6.1, 4.0), (6.9, 4.0), AUS, 5), P((4.0, 6.1), (4.0, 6.9), AUS, 5), P((7.6, 5.0), (8.6, 6.0), AUS, 5)]
GAM = [('Stahl', 0.036), ('Aluminium', 0.0714), ('Quecksilber', 0.18), ('Ethanol', 1.10)]
balken = [F(rechteck(0.6 + 2.3 * i, 0, 2.2 + 2.3 * i, g), AUS if n in ('Stahl', 'Ethanol') else TIN, 0.5 if n in ('Stahl', 'Ethanol') else 0.22) for i, (n, g) in enumerate(GAM)]
kan = umriss(2.0, 1.0, 7.0, 7.0, TIN, 5) + [S((5.0, 7.0), (5.0, 8.0), TIN, 5), S((6.2, 7.0), (6.2, 8.0), TIN, 5), S((5.0, 8.0), (6.2, 8.0), TIN, 5)]
DREH.append(dict(KOPF, titel='Ausdehnung sehen: in drei Richtungen', dateiname='p5-3-lp-volumen',
    kurzbeschrieb='Warum das Volumen eines Festkörpers mit γ ≈ 3α wächst, warum Flüssigkeiten sich viel stärker ausdehnen — und ein vorgerechnetes Problem: der randvolle Kanister in der Sonne.',
    schlagworte=['Volumenausdehnung', 'Volumenausdehnungskoeffizient', 'gamma gleich drei alpha', 'Flüssigkeit', 'Ethanol'], _probe=EIN % 2,
    szenen=[
        sz('Würfel', 'Ein Würfel wird beim Erwärmen nicht nur länger, sondern auch breiter und höher. Jede Kante wächst um den Anteil alpha mal Delta T. Im Volumen kommen die drei Richtungen zusammen: Gamma ist ungefähr drei mal alpha.',
           titel('In drei Richtungen', g=66),
           formel(r'\gamma \approx 3 \cdot \alpha', y=430, g=56, anker='Gamma ist ungefähr'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=w0, texte=[T(3.75, 0.7, 'kalt', TIN, 28)]),
           ebene([0, 10], [0, 10], anker='Jede Kante wächst', strecken=w1, texte=[T(9.0, 1.2, 'warm (übertrieben)', AUS, 26, 'end')]),
           ebene([0, 10], [0, 10], anker='die drei Richtungen', strecken=pf3)),
        sz('Formel', 'Für das Volumen gilt dieselbe Form: Delta V gleich gamma mal V null mal Delta T. Flüssigkeiten haben keine eigene Form; für sie steht gamma direkt in der Tabelle. Ethanol hat eins Komma eins null Tausendstel pro Kelvin, rund dreissigmal so viel wie Stahl. Die Teilchen einer Flüssigkeit sind schwächer gebunden.',
           formel(r'\Delta V = \gamma \cdot V_0 \cdot \Delta T', y=280, g=56, anker='Delta V gleich'),
           notiz(r'Ethanol: @\gamma = 1.10 \cdot 10^{-3}' + K1 + '@', y=420, anker='Ethanol hat'),
           notiz(r'Stahl: @\gamma = 0.036 \cdot 10^{-3}' + K1 + '@', y=520, anker='rund dreissigmal'),
           graf([-0.6, 9.8], [-0.14, 1.3], [], [0.25, 0.5, 0.75, 1.0], '', 'γ [10⁻³ 1/K]', anker='Ethanol hat', flaechen=balken,
                texte=[T(1.4 + 2.3 * i, g + 0.05, n, AUS if n in ('Stahl', 'Ethanol') else TIN, 24) for i, (n, g) in enumerate(GAM)])),
        sz('Vergleich', 'In der Simulation: Ein Liter Ethanol, von zwanzig auf sechzig Grad erwärmt, wächst um vierundvierzig Milliliter. Ein Liter Aluminium wächst bei derselben Erwärmung nur um knapp drei Milliliter.',
           formel(r'\Delta V = 1.10 \cdot 10^{-3}' + K1 + r' \cdot 1\;\text{l} \cdot 40\;\text{K} = 44\;\text{ml}', y=290, g=34, anker='wächst um vierundvierzig'),
           formel(r'\Delta V = 71.4 \cdot 10^{-6}' + K1 + r' \cdot 1\;\text{l} \cdot 40\;\text{K} \approx 2.9\;\text{ml}', y=420, g=34, anker='nur um knapp'),
           bild('p5-3-lp-volumen-et20', ein=0.05),
           bild('p5-3-lp-volumen-et40', anker='von zwanzig auf sechzig'),
           bild('p5-3-lp-volumen-et60', anker='von zwanzig auf sechzig', versatz=1.0),
           bild('p5-3-lp-volumen-al60', anker='Ein Liter Aluminium')),
        sz('Problem Kanister', 'Jetzt ein ganzes Problem. Ein Kanister fasst zwanzig Liter. Er wird bei acht Grad randvoll mit Brennsprit, also Ethanol, gefüllt und steht dann in der Sonne, bis der Inhalt achtunddreissig Grad hat. Wie viel läuft aus? Der Kanister selbst dehnt sich viel weniger aus; wir rechnen ihn starr.',
           notiz('20 l Ethanol, randvoll bei 8 °C', y=300, anker='Ein Kanister fasst'),
           notiz('in der Sonne: 38 °C', y=400, anker='steht dann in der Sonne'),
           notiz('gesucht: @\\Delta V@, das ausläuft|Kanister starr (Modell)', y=500, anker='Wie viel läuft'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=kan, flaechen=[F(rechteck(2.0, 1.0, 7.0, 7.0), TIN, 0.12)],
                 texte=[T(4.5, 4.0, '20 l', TIN, 34), T(4.5, 0.3, '8 °C', TIN, 28)]),
           ebene([0, 10], [0, 10], anker='steht dann in der Sonne', flaechen=[F(rechteck(2.0, 1.0, 7.0, 7.0), TEMP, 0.25)],
                 texte=[T(8.6, 8.8, '38 °C', TEMP, 32)])),
        sz('Vorgehen Kanister', 'Ethanol ist eine Flüssigkeit: Gamma steht in der Tabelle, ohne Faktor drei. Delta T ist achtunddreissig minus acht, also dreissig Kelvin. V null sind die zwanzig Liter.',
           formel(r'\gamma = 1.10 \cdot 10^{-3}' + K1, y=300, g=44, anker='Gamma steht'),
           formel(r'\Delta T = 38\;^\circ\text{C} - 8\;^\circ\text{C} = 30\;\text{K}', y=420, g=40, anker='Delta T ist'),
           notiz(r'@V_0 = 20\;\text{l}@', y=530, anker='V null sind'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=kan, flaechen=[F(rechteck(2.0, 1.0, 7.0, 7.0), TEMP, 0.25)],
                 texte=[T(4.5, 4.0, '20 l', TIN, 34), T(8.6, 8.8, '38 °C', TEMP, 32)])),
        sz('Lösung Kanister', 'Delta V gleich gamma mal V null mal Delta T: eins Komma eins null Tausendstel mal zwanzig Liter mal dreissig Kelvin. Das sind null Komma sechs sechs Liter, die auslaufen. Probe: Gamma mal Delta T sind drei Komma drei Prozent, und drei Komma drei Prozent von zwanzig Litern sind zwei Drittel Liter.',
           formel(r'\Delta V = \gamma \cdot V_0 \cdot \Delta T = 1.10 \cdot 10^{-3}' + K1 + r' \cdot 20\;\text{l} \cdot 30\;\text{K}', y=290, g=32, anker='Delta V gleich'),
           formel(r'= 0.66\;\text{l}', y=390, g=44, anker='Das sind null Komma'),
           notiz('Probe: @\\gamma \\cdot \\Delta T = 3.3\\;\\%@|3.3 % von 20 l: 0.66 l', y=500, g=40, anker='Probe'),
           graf([-4, 42], [-0.1, 0.98], [10, 20, 30, 40], [0.2, 0.4, 0.6, 0.8], 'ΔT [K]', 'ΔV [l]', ein=0.05,
                strecken=[S((0, 0), (40, 0.88), AUS, 5)]),
           ebene([-4, 42], [-0.1, 0.98], anker='Das sind null Komma',
                 strecken=[S((30, 0), (30, 0.66), TIN, 3, gestrichelt=True), S((0, 0.66), (30, 0.66), TIN, 3, gestrichelt=True)],
                 punkte=[{'x': 30, 'y': 0.66, 'farbe': AUS, 'beschriftung': '(30 K; 0.66 l)', 'beschriftung_bei': [20, 0.73], 'anker': 'middle'}])),
        sz('Merke', 'Zum Mitnehmen: Das Volumen wächst um gamma mal Anfangsvolumen mal Temperaturänderung. Bei Festkörpern ist gamma ungefähr drei mal alpha, bei Flüssigkeiten steht es in der Tabelle.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\Delta V = \gamma \cdot V_0 \cdot \Delta T', y=420, g=52, ein=0.4),
           notiz('Festkörper: @\\gamma \\approx 3 \\cdot \\alpha@|Flüssigkeit: γ aus der Tabelle', y=550, ein=1.2)),
        JETZT,
    ]))

# ================================================================== Kapitel 3: Wasser und Meer
RHO = '(999.83952+16.945176*x-0.0079870401*x**2-0.000046170461*x**3+0.00000010556302*x**4-0.00000000028054253*x**5)/(1+0.01687985*x)'
box_k = umriss(1.0, 1.5, 3.8, 4.3, TIN, 4)
box_w = umriss(5.2, 1.5, 8.6, 4.9, AUS, 5)
see = [F(rechteck(1, 1, 9, 2.6), TIN, 0.35), F(rechteck(1, 2.6, 9, 4.6), TIN, 0.22), F(rechteck(1, 4.6, 9, 6.4), TIN, 0.12), F(rechteck(1, 6.4, 9, 7.0), TIN, 0.04)]
DREH.append(dict(KOPF, titel='Ausdehnung sehen: Wasser und Meeresspiegel', dateiname='p5-3-lp-meer',
    kurzbeschrieb='Warum die Dichte beim Erwärmen sinkt, wo Wasser eine Ausnahme macht (Anomalie), wie aus ΔV = γ · V₀ · ΔT der Anstieg Δh = γ · h₀ · ΔT wird — und ein vorgerechnetes Problem: das erwärmte Meer.',
    schlagworte=['Dichte', 'Anomalie des Wassers', 'Meeresspiegelanstieg', 'thermische Ausdehnung', 'Meer'], _probe=EIN % 3,
    szenen=[
        sz('Dichte', 'Beim Erwärmen bleibt die Masse gleich, aber das Volumen wächst. Darum sinkt die Dichte: rho gleich rho null durch eins plus gamma mal Delta T. Warmes Wasser steigt deshalb in kaltem auf.',
           formel(r'\rho = \frac{m}{V}', y=280, g=52, ein=0.5),
           formel(r'\rho = \frac{\rho_0}{1 + \gamma \cdot \Delta T}', y=430, g=52, anker='rho gleich'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=box_k, flaechen=[F(rechteck(1.0, 1.5, 3.8, 4.3), TIN, 0.25)],
                 texte=[T(2.4, 2.9, 'm', TIN, 34), T(2.4, 0.6, 'kalt', TIN, 28)]),
           ebene([0, 10], [0, 10], anker='aber das Volumen wächst', strecken=box_w, flaechen=[F(rechteck(5.2, 1.5, 8.6, 4.9), AUS, 0.15)],
                 texte=[T(6.9, 3.2, 'm', AUS, 34), T(6.9, 0.6, 'warm: V grösser', AUS, 28)])),
        sz('Anomalie', 'Wasser ist eine Ausnahme. Seine Dichte ist bei vier Grad am grössten. Zwischen null und vier Grad zieht es sich beim Erwärmen zusammen. Und beim Gefrieren dehnt es sich um rund neun Prozent aus.',
           notiz('grösste Dichte bei 4 °C', y=300, anker='bei vier Grad'),
           notiz('0 °C bis 4 °C: wärmer|heisst kleineres Volumen', y=400, anker='Zwischen null'),
           notiz('Eis: rund 9 % mehr Volumen', y=530, anker='beim Gefrieren'),
           # Fenster ohne ρ = 0: gezeichnet wird ρ − 999.4 kg/m³, die Teilung nennt die echten Werte; die x-Achse liegt am unteren Rand
           graf([-1.4, 12.6], [-0.08, 0.66], [2, 4, 6, 8, 10, 12], [[0.1, '999.5'], [0.2, '999.6'], [0.3, '999.7'], [0.4, '999.8'], [0.5, '999.9'], [0.6, '1000']], 'ϑ [°C]', 'ρ [kg/m³]',
                ein=0.05, kurven=[{'formel': RHO + '-999.4', 'von': 0, 'bis': 12, 'farbe': AUS, 'dicke': 5, 'n': 200}]),
           ebene([-1.4, 12.6], [-0.08, 0.66], anker='bei vier Grad',
                 punkte=[{'x': 4, 'y': 0.572, 'farbe': AUS, 'beschriftung': '4 °C: grösste Dichte', 'beschriftung_bei': [4.6, 0.62], 'anker': 'start'}]),
           ebene([-1.4, 12.6], [-0.08, 0.66], anker='Zwischen null', strecken=[P((0.3, 0.2), (3.7, 0.2), TEMP, 5)],
                 texte=[T(2.0, 0.15, 'wärmer, dichter', TEMP, 24)])),
        sz('See', 'Im Winter sinkt darum das Wasser von vier Grad auf den Grund eines Sees. Darüber liegt kälteres Wasser, und ganz oben schwimmt das Eis. Für Wasser ist gamma also keine Konstante: Null Komma zwei eins Tausendstel pro Kelvin gilt nur um zwanzig Grad.',
           notiz('Grund: 4 °C, oben Eis', y=300, anker='auf den Grund'),
           formel(r'\gamma_\text{Wasser} = 0.21 \cdot 10^{-3}' + K1, y=430, g=42, anker='Null Komma zwei eins'),
           notiz('nur um 20 °C', y=530, anker='gilt nur um'),
           ebene([0, 10], [0, 10], ein=0.05, flaechen=see,
                 strecken=[S((1, 7.0), (9, 7.0), TIN, 6), S((0.6, 8.0), (0.6, 1.0), TIN, 4), S((9.4, 8.0), (9.4, 1.0), TIN, 4), S((0.6, 1.0), (9.4, 1.0), TIN, 4)],
                 texte=[T(5, 7.5, 'Eis 0 °C', TIN, 26), T(5, 5.3, '1 °C bis 3 °C', TIN, 26), T(5, 1.6, '4 °C (am dichtesten)', AUS, 28)])),
        sz('Meer', 'Auch das Meer dehnt sich aus, wenn es wärmer wird. Weil die Fläche gleich bleibt, kann es nur nach oben. Aus Delta V gleich gamma mal V null mal Delta T wird Delta h gleich gamma mal h null mal Delta T. Dabei ist h null die Dicke der Schicht, die sich erwärmt.',
           formel(r'\Delta V = \gamma \cdot V_0 \cdot \Delta T', y=280, g=46, anker='Aus Delta V'),
           formel(r'\Delta h = \gamma \cdot h_0 \cdot \Delta T', y=400, g=52, anker='wird Delta h'),
           notiz('@h_0@: Dicke der erwärmten Schicht', y=520, anker='Dabei ist h null'),
           bild('p5-3-lp-meer-h1500-00', ein=0.05),
           bild('p5-3-lp-meer-h1500-05', anker='wenn es wärmer wird'),
           bild('p5-3-lp-meer-h1500-10', anker='wenn es wärmer wird', versatz=1.0)),
        sz('Problem Meer', 'Jetzt ein ganzes Problem. Ein Ozean ist im Mittel rund dreitausendsiebenhundert Meter tief. Nimm an, die obersten fünfhundert Meter erwärmen sich um eins Komma fünf Kelvin; das Tiefenwasser bleibt gleich. Um wie viel steigt der Meeresspiegel allein durch die Ausdehnung?',
           notiz('Tiefe rund 3700 m', y=300, anker='Ein Ozean'),
           notiz('oberste 500 m: +1.5 K|Tiefenwasser unverändert', y=400, anker='Nimm an'),
           notiz('gesucht: @\\Delta h@', y=530, anker='Um wie viel'),
           bild('p5-3-lp-meer-h500-00', ein=0.05)),
        sz('Vorgehen Meer', 'Ausdehnen kann sich nur das Wasser, das wärmer wird: h null ist die Dicke der erwärmten Schicht, fünfhundert Meter. Gamma für Wasser ist null Komma zwei eins Tausendstel pro Kelvin, Delta T eins Komma fünf Kelvin.',
           formel(r'h_0 = 500\;\text{m}', y=300, g=48, anker='h null ist'),
           formel(r'\gamma = 0.21 \cdot 10^{-3}' + K1 + r',\quad \Delta T = 1.5\;\text{K}', y=420, g=40, anker='Gamma für Wasser'),
           bild('p5-3-lp-meer-h500-00', ein=0.05)),
        sz('Lösung Meer', 'Delta h gleich gamma mal h null mal Delta T: null Komma zwei eins Tausendstel mal fünfhundert Meter mal eins Komma fünf Kelvin. Das sind null Komma eins fünf acht Meter, also gut fünfzehn Zentimeter. Probe: Gamma mal Delta T sind gut drei Zehntausendstel, und drei Zehntausendstel von fünfhundert Metern sind fünfzehn Zentimeter. Schmelzende Gletscher kämen noch dazu.',
           formel(r'\Delta h = \gamma \cdot h_0 \cdot \Delta T = 0.21 \cdot 10^{-3}' + K1 + r' \cdot 500\;\text{m} \cdot 1.5\;\text{K}', y=290, g=30, anker='Delta h gleich'),
           formel(r'\approx 0.158\;\text{m} = 15.8\;\text{cm}', y=390, g=42, anker='Das sind null Komma'),
           notiz('Probe: @\\gamma \\cdot \\Delta T \\approx 0.0003@|0.0003 · 500 m = 0.15 m', y=500, g=40, anker='Probe'),
           bild('p5-3-lp-meer-h500-00', ein=0.05),
           bild('p5-3-lp-meer-h500-05', anker='Delta h gleich', versatz=1.5),
           bild('p5-3-lp-meer-h500-10', anker='Delta h gleich', versatz=3.0),
           bild('p5-3-lp-meer-h500-15', anker='Das sind null Komma')),
        sz('Merke', 'Zum Mitnehmen: Warmes Wasser braucht mehr Platz, ausser zwischen null und vier Grad. Im Meer hebt die erwärmte Schicht den Spiegel um gamma mal h null mal Delta T.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\Delta h = \gamma \cdot h_0 \cdot \Delta T', y=420, g=52, ein=0.4),
           notiz('Anomalie: grösste Dichte bei 4 °C', y=560, ein=1.2)),
        JETZT,
    ]))

# ================================================================== Kapitel 4: Gasgleichung
def saeulen(werte, ebene_von=0.0):
    """Säulen für den Druck: Luftdruck (Tinte) unten, Überdruck (Rot) darauf; werte = [(x, p_ue, text)]"""
    fl, tx = [], []
    for x, pu, t in werte:
        fl += [F(rechteck(x - 0.7, 0, x + 0.7, 1.0), TIN, 0.25), F(rechteck(x - 0.7, 1.0, x + 0.7, 1.0 + pu), DRU, 0.4)]
        tx += [T(x, 1.0 + pu + 0.12, t, DRU, 26)]
    return fl, tx


fl1, tx1 = saeulen([(2.0, 2.0, 'Überdruck')])
DREH.append(dict(KOPF, titel='Ausdehnung sehen: ein Gas, drei Grössen', dateiname='p5-3-lp-gas',
    kurzbeschrieb='Der Zustand einer festen Gasmenge mit Druck, Volumen und Temperatur, die Regeln Kelvin und absoluter Druck, die allgemeine Gasgleichung — und ein vorgerechnetes Problem: der Fussball in der Sonne.',
    schlagworte=['ideales Gas', 'allgemeine Gasgleichung', 'absoluter Druck', 'Überdruck', 'Kelvin'], _probe=EIN % 4,
    szenen=[
        sz('Zustand', 'Ein Gas ist in einem Zylinder mit Kolben eingeschlossen. Seine Teilchen fliegen umher und prallen gegen die Wände; ihre Stösse sind der Druck. Den Zustand des Gases beschreiben drei Grössen: Druck, Volumen und Temperatur. Die Gasmenge bleibt dabei gleich.',
           notiz('Druck: Stösse der Teilchen', y=300, anker='ihre Stösse'),
           notiz('Zustand: @p@, @V@, @T@', y=400, anker='drei Grössen'),
           notiz('Gasmenge fest', y=500, anker='Die Gasmenge'),
           bild('p5-3-lp-gas-z1', ein=0.05)),
        sz('Zwei Regeln', 'Zwei Regeln. Erstens gehört die Temperatur in Kelvin: T gleich Celsius-Temperatur plus zweihundertdreiundsiebzig Komma eins fünf Kelvin. Zweitens zählt der absolute Druck. Ein Manometer zeigt meist nur den Überdruck; dazu kommt der Luftdruck von rund einem Bar.',
           formel(r'T = \vartheta + 273.15\;\text{K}', y=290, g=48, anker='Erstens'),
           formel(r'p = p_\text{ü} + p_\text{L}', y=420, g=48, anker='Ein Manometer'),
           notiz(r'@p_\text{L} \approx 1.0\;\text{bar}@', y=530, anker='dazu kommt'),
           graf([-1, 9], [-0.5, 4.5], [], [1, 2, 3, 4], '', 'p [bar]', anker='Zweitens', flaechen=fl1[:1],
                texte=[T(2.0, 0.5, 'Luftdruck', TIN, 24), T(5.4, 1.1, '1 bar', TIN, 26, 'start')],
                strecken=[S((1.3, 1.0), (5.2, 1.0), TIN, 2, gestrichelt=True)]),
           ebene([-1, 9], [-0.5, 4.5], anker='Ein Manometer', flaechen=fl1[1:],
                 texte=[T(2.0, 2.0, 'Überdruck', DRU, 24), T(5.4, 3.1, 'absolut: 3 bar', DRU, 26, 'start')],
                 strecken=[S((1.3, 3.0), (5.2, 3.0), DRU, 2, gestrichelt=True)])),
        sz('Gesetz', 'Erwärmt man das Gas bei gleichem Volumen, werden die Teilchen schneller und stossen härter: Der Druck steigt. Drückt man es zusammen, treffen die Teilchen öfter auf die Wand: Der Druck steigt auch. Zusammen gilt: p mal V durch T bleibt gleich.',
           notiz('wärmer: Druck steigt', y=290, anker='Erwärmt man'),
           notiz('kleiner: Druck steigt', y=390, anker='Drückt man'),
           formel(r'\frac{p_1 \cdot V_1}{T_1} = \frac{p_2 \cdot V_2}{T_2}', y=500, g=50, anker='Zusammen gilt'),
           bild('p5-3-lp-gas-z1', ein=0.05),
           bild('p5-3-lp-gas-warm-05', anker='Erwärmt man', versatz=0.8),
           bild('p5-3-lp-gas-warm-10', anker='Erwärmt man', versatz=1.8),
           bild('p5-3-lp-gas-z1', anker='Drückt man'),
           bild('p5-3-lp-gas-klein-05', anker='Drückt man', versatz=0.8),
           bild('p5-3-lp-gas-klein-10', anker='Drückt man', versatz=1.8)),
        sz('Problem Fussball', 'Jetzt ein ganzes Problem. Ein Fussball wird im Keller bei zwölf Grad auf null Komma neun Bar Überdruck gepumpt; er fasst fünf Komma vier Liter. Auf dem Kunstrasen in der Sonne wird die Luft darin zweiundvierzig Grad warm, und der Ball dehnt sich auf fünf Komma fünf Liter. Was zeigt das Manometer jetzt?',
           notiz('Keller: 0.9 bar Überdruck,|5.4 l, 12 °C', y=300, anker='Ein Fussball'),
           notiz('Sonne: 5.5 l, 42 °C', y=430, anker='Auf dem Kunstrasen'),
           notiz('gesucht: Überdruck', y=530, anker='Was zeigt'),
           ebene([0, 10], [0, 10], ein=0.05, kurven=kreis(5, 5, 3.2, TIN, 5),
                 texte=[T(5, 5.4, 'Luft: 5.4 l', TIN, 30), T(5, 4.4, '12 °C', TIN, 30)]),
           ebene([0, 10], [0, 10], anker='Auf dem Kunstrasen', kurven=kreis(5, 5, 3.4, AUS, 5),
                 texte=[T(5, 8.9, 'Sonne: 5.5 l, 42 °C', AUS, 30)])),
        sz('Vorgehen Fussball', 'In die Gasgleichung gehört der absolute Druck: null Komma neun Bar Überdruck plus ein Bar Luftdruck, also eins Komma neun Bar. Die Temperaturen in Kelvin: zweihundertfünfundachtzig Komma eins fünf und dreihundertfünfzehn Komma eins fünf Kelvin.',
           formel(r'p_1 = 0.9\;\text{bar} + 1.0\;\text{bar} = 1.9\;\text{bar}', y=300, g=42, anker='null Komma neun Bar Überdruck'),
           formel(r'T_1 = 285.15\;\text{K},\quad T_2 = 315.15\;\text{K}', y=420, g=42, anker='Die Temperaturen'),
           graf([-1, 9], [-0.3, 2.8], [], [1, 2], '', 'p [bar]', ein=0.05,
                flaechen=[F(rechteck(1.3, 0, 2.7, 1.0), TIN, 0.25), F(rechteck(1.3, 1.0, 2.7, 1.9), DRU, 0.4)],
                texte=[T(2.0, 0.5, 'Luftdruck', TIN, 22), T(2.0, 1.45, 'Überdruck', DRU, 22), T(3.0, 1.95, 'p₁ = 1.9 bar (absolut)', DRU, 26, 'start')])),
        sz('Lösung Fussball', 'Umgestellt nach p zwei: p eins mal V eins mal T zwei durch T eins mal V zwei. Eins Komma neun Bar mal fünf Komma vier Liter mal dreihundertfünfzehn Komma eins fünf Kelvin, durch zweihundertfünfundachtzig Komma eins fünf Kelvin mal fünf Komma fünf Liter: rund zwei Komma null sechs Bar absolut. Das Manometer zeigt also eins Komma null sechs Bar Überdruck. Probe: Die Temperatur steigt um gut zehn Prozent, das Volumen um knapp zwei. Der Druck steigt also um gut acht Prozent. Das passt.',
           formel(r'p_2 = \frac{p_1 \cdot V_1 \cdot T_2}{T_1 \cdot V_2} = \frac{1.9\;\text{bar} \cdot 5.4\;\text{l} \cdot 315.15\;\text{K}}{285.15\;\text{K} \cdot 5.5\;\text{l}}', y=300, g=32, anker='Umgestellt'),
           formel(r'\approx 2.06\;\text{bar} \;\Rightarrow\; p_\text{ü} \approx 1.06\;\text{bar}', y=440, g=40, anker='rund zwei Komma null sechs'),
           notiz('Probe: T +10 %, V +2 % → p +8 %', y=550, g=40, anker='Probe'),
           graf([-1, 9], [-0.3, 2.8], [], [1, 2], '', 'p [bar]', ein=0.05,
                flaechen=[F(rechteck(1.3, 0, 2.7, 1.0), TIN, 0.25), F(rechteck(1.3, 1.0, 2.7, 1.9), DRU, 0.4)],
                texte=[T(2.0, 0.5, 'Luftdruck', TIN, 22), T(2.0, 2.15, 'vorher 1.9 bar', DRU, 24)]),
           ebene([-1, 9], [-0.3, 2.8], anker='rund zwei Komma null sechs',
                 flaechen=[F(rechteck(5.3, 0, 6.7, 1.0), TIN, 0.25), F(rechteck(5.3, 1.0, 6.7, 2.0617), DRU, 0.4)],
                 texte=[T(6.0, 0.5, 'Luftdruck', TIN, 22), T(6.0, 2.32, 'nachher 2.06 bar', DRU, 24)]),
           ebene([-1, 9], [-0.3, 2.8], anker='Das Manometer zeigt',
                 strecken=[P((7.0, 1.0), (7.0, 2.0617), DRU, 4), P((7.0, 2.0617), (7.0, 1.0), DRU, 4)],
                 texte=[T(7.25, 1.5, 'Manometer: 1.06 bar', DRU, 24, 'start')])),
        sz('Merke', 'Zum Mitnehmen: Für eine feste Gasmenge bleibt p mal V durch T gleich. Die Temperatur steht in Kelvin, der Druck absolut.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\frac{p_1 \cdot V_1}{T_1} = \frac{p_2 \cdot V_2}{T_2}', y=420, g=50, ein=0.4),
           notiz('T in Kelvin, p absolut, Gasmenge fest', y=580, ein=1.2)),
        JETZT,
    ]))

# ================================================================== Kapitel 5: Spezialfälle
T1 = 293.15
tank = umriss(2.0, 1.5, 6.5, 7.0, TIN, 6)
DREH.append(dict(KOPF, titel='Ausdehnung sehen: eine Grösse hält still', dateiname='p5-3-lp-spezialfaelle',
    kurzbeschrieb='Wie aus der allgemeinen Gasgleichung die Gesetze von Boyle-Mariotte, Gay-Lussac und Amontons werden, mit Hyperbel und Ursprungsgeraden — und ein vorgerechnetes Problem: der Druckluftbehälter in der Sonne.',
    schlagworte=['isotherm', 'isobar', 'isochor', 'Boyle-Mariotte', 'Gay-Lussac', 'Amontons'], _probe=EIN % 5,
    szenen=[
        sz('Kürzen', 'Bleibt bei einer Zustandsänderung eine Grösse gleich, steht sie in der Gasgleichung links und rechts gleich und kürzt sich heraus. So entstehen drei Spezialfälle.',
           formel(r'\frac{p_1 \cdot V_1}{T_1} = \frac{p_2 \cdot V_2}{T_2}', y=290, g=52, ein=0.5),
           notiz('eine Grösse konstant:|sie kürzt sich heraus', y=440, anker='kürzt sich heraus'),
           ebene([0, 10], [0, 10], anker='So entstehen', texte=[T(0.5, 8.0, 'T konstant:  p₁ · V₁ = p₂ · V₂', TIN, 30, 'start'),
                                                                  T(0.5, 5.5, 'p konstant:  V₁ / T₁ = V₂ / T₂', TIN, 30, 'start'),
                                                                  T(0.5, 3.0, 'V konstant:  p₁ / T₁ = p₂ / T₂', TIN, 30, 'start')])),
        sz('Isotherm', 'Bleibt die Temperatur gleich, heisst die Änderung isotherm: p eins mal V eins gleich p zwei mal V zwei, das Gesetz von Boyle und Mariotte. Halbes Volumen, doppelter Druck. Im p-V-Diagramm liegen die Zustände auf einer Hyperbel.',
           formel(r'p_1 \cdot V_1 = p_2 \cdot V_2', y=290, g=52, anker='p eins mal V eins'),
           notiz('isotherm: @T@ konstant|(Boyle-Mariotte)', y=420, anker='Bleibt die Temperatur'),
           graf([-0.5, 6.6], [-0.5, 6.6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 'V [l]', 'p [bar]', ein=0.05,
                kurven=[{'formel': '3/x', 'von': 0.5, 'bis': 6.4, 'farbe': AUS, 'dicke': 5, 'n': 300,
                         'laeufer': {'bahn': [[0.0, 3.0], [6.0, 3.0], [6.05, 2.0], [7.2, 2.0], [7.25, 1.5]], 'text': '({x} l; {y} bar)', 'farbe': AUS, 'lage': 'oben rechts'}}])),
        sz('Isobar', 'Bleibt der Druck gleich, etwa unter einem frei beweglichen Kolben mit Gewicht, heisst die Änderung isobar: V durch T bleibt gleich, das Gesetz von Gay-Lussac. Im Diagramm Volumen über Temperatur liegen die Zustände auf einer Geraden. Verlängert man sie, trifft sie den Ursprung, null Kelvin.',
           formel(r'\frac{V_1}{T_1} = \frac{V_2}{T_2}', y=290, g=52, anker='V durch T'),
           notiz('isobar: @p@ konstant|(Gay-Lussac)', y=430, anker='Bleibt der Druck'),
           graf([-50, 650], [-0.6, 6.6], [100, 200, 300, 400, 500, 600], [1, 2, 3, 4, 5, 6], 'T [K]', 'V [l]', ein=0.05,
                strecken=[S((150, 3 * 150 / T1), (600, 3 * 600 / T1), VOL, 5)],
                punkte=[{'x': T1, 'y': 3.0, 'farbe': VOL, 'beschriftung': '(293 K; 3.0 l)', 'beschriftung_bei': [310, 2.5], 'anker': 'start'}]),
           ebene([-50, 650], [-0.6, 6.6], anker='Verlängert man', strecken=[S((0, 0), (150, 3 * 150 / T1), VOL, 3, gestrichelt=True)],
                 punkte=[{'x': 0, 'y': 0, 'farbe': TIN, 'beschriftung': '0 K', 'beschriftung_bei': [20, 0.45], 'anker': 'start'}])),
        sz('Isochor', 'Bleibt das Volumen gleich, in einem starren Behälter, heisst die Änderung isochor: p durch T bleibt gleich, das Gesetz von Amontons. Auch hier liegen die Zustände auf einer Geraden durch den Ursprung, aber nur, wenn die Temperatur in Kelvin steht.',
           formel(r'\frac{p_1}{T_1} = \frac{p_2}{T_2}', y=290, g=52, anker='p durch T'),
           notiz('isochor: @V@ konstant|(Amontons)', y=430, anker='Bleibt das Volumen'),
           graf([-50, 650], [-0.2, 2.2], [100, 200, 300, 400, 500, 600], [0.5, 1, 1.5, 2], 'T [K]', 'p [bar]', ein=0.05,
                strecken=[S((150, 150 / T1), (600, 600 / T1), DRU, 5)]),
           ebene([-50, 650], [-0.2, 2.2], anker='Auch hier', strecken=[S((0, 0), (150, 150 / T1), DRU, 3, gestrichelt=True)],
                 punkte=[{'x': 0, 'y': 0, 'farbe': TIN, 'beschriftung': '0 K', 'beschriftung_bei': [20, 0.15], 'anker': 'start'}])),
        sz('Problem Druckluft', 'Jetzt ein ganzes Problem. Ein Druckluftbehälter aus Stahl steht bei fünfzehn Grad unter sechs Bar, absolut. In der Sonne wird er fünfundfünfzig Grad warm. Sein Sicherheitsventil öffnet bei sieben Bar. Öffnet es?',
           notiz('Stahlbehälter: 6.0 bar bei 15 °C', y=300, anker='Ein Druckluftbehälter'),
           notiz('Sonne: 55 °C', y=400, anker='In der Sonne'),
           notiz('Ventil öffnet bei 7.0 bar', y=500, anker='Sein Sicherheitsventil'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=tank + [S((4.25, 7.0), (4.25, 8.2), TIN, 5), S((3.6, 8.2), (4.9, 8.2), TIN, 8)],
                 flaechen=[F(rechteck(2.0, 1.5, 6.5, 7.0), TIN, 0.1)],
                 texte=[T(4.25, 4.4, '6.0 bar', DRU, 32), T(4.25, 3.4, '15 °C', TIN, 28), T(5.2, 8.6, 'Ventil: 7.0 bar', TIN, 26, 'start')]),
           ebene([0, 10], [0, 10], anker='In der Sonne', flaechen=[F(rechteck(2.0, 1.5, 6.5, 7.0), TEMP, 0.25)],
                 texte=[T(8.2, 4.4, '55 °C', TEMP, 32)])),
        sz('Vorgehen Druckluft', 'Der Behälter ist starr, sein Volumen bleibt: isochor. Die Temperaturen gehören in Kelvin: zweihundertachtundachtzig Komma eins fünf und dreihundertachtundzwanzig Komma eins fünf Kelvin.',
           formel(r'V\;\text{konstant:}\quad \frac{p_1}{T_1} = \frac{p_2}{T_2}', y=300, g=44, anker='Der Behälter ist starr'),
           formel(r'T_1 = 288.15\;\text{K},\quad T_2 = 328.15\;\text{K}', y=440, g=40, anker='Die Temperaturen'),
           ebene([0, 10], [0, 10], ein=0.05, strecken=tank, flaechen=[F(rechteck(2.0, 1.5, 6.5, 7.0), TEMP, 0.25)],
                 texte=[T(4.25, 4.4, 'V bleibt', TIN, 30)])),
        sz('Lösung Druckluft', 'p zwei gleich p eins mal T zwei durch T eins: sechs Bar mal dreihundertachtundzwanzig Komma eins fünf durch zweihundertachtundachtzig Komma eins fünf, rund sechs Komma acht drei Bar. Das ist weniger als sieben Bar: Das Ventil bleibt zu. Probe: Die Kelvin-Temperatur steigt um knapp vierzehn Prozent, der Druck auch.',
           formel(r'p_2 = p_1 \cdot \frac{T_2}{T_1} = 6.0\;\text{bar} \cdot \frac{328.15\;\text{K}}{288.15\;\text{K}}', y=290, g=38, anker='p zwei gleich'),
           formel(r'\approx 6.83\;\text{bar} \lt 7.0\;\text{bar}', y=420, g=44, anker='rund sechs Komma acht drei'),
           notiz('Ventil bleibt zu.|Probe: T +14 %, p +14 %', y=530, g=40, anker='Das ist weniger'),
           graf([-30, 380], [-0.6, 8.6], [100, 200, 300], [2, 4, 6, 8], 'T [K]', 'p [bar]', ein=0.05,
                strecken=[S((0, 0), (360, 6.0 * 360 / 288.15), DRU, 4), S((0, 7.0), (360, 7.0), TIN, 3, gestrichelt=True)],
                texte=[T(20, 7.35, 'Ventil: 7.0 bar', TIN, 24, 'start')],
                punkte=[{'x': 288.15, 'y': 6.0, 'farbe': TIN, 'beschriftung': '15 °C', 'beschriftung_bei': [270, 5.4], 'anker': 'end'}]),
           ebene([-30, 380], [-0.6, 8.6], anker='rund sechs Komma acht drei',
                 punkte=[{'x': 328.15, 'y': 6.0 * 328.15 / 288.15, 'farbe': DRU, 'beschriftung': '(328 K; 6.83 bar)', 'beschriftung_bei': [318, 5.9], 'anker': 'end'}])),
        sz('Merke', 'Zum Mitnehmen: Was konstant bleibt, kürzt sich aus der Gasgleichung heraus. Isotherm heisst p mal V konstant, isobar V durch T, isochor p durch T, mit T in Kelvin.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'p \cdot V,\quad \frac{V}{T},\quad \frac{p}{T}\;\text{konstant}', y=420, g=46, ein=0.4),
           notiz('isotherm, isobar, isochor', y=560, ein=1.2)),
        JETZT,
    ]))

FRAGEN = {
    'p5-3-lp-laenge': [wahl('Vorgehen Fernwärme', 'Welche Temperaturänderung setzt du ein?', ['90 K', '80 K', '363 K'], 1,
                            {0: 'Wurde die Leitung bei null Grad eingebaut?', 2: 'In der Formel steht eine Temperaturänderung, keine Temperatur.'}, kopf='Dein Vorgehen')],
    'p5-3-lp-volumen': [wahl('Vorgehen Kanister', 'Welchen Koeffizienten nimmst du für das Ethanol?', ['γ = 1.10·10⁻³ 1/K', 'γ = 3 · 1.10·10⁻³ 1/K', 'α = 1.10·10⁻³ 1/K'], 0,
                             {1: 'Gilt der Faktor drei auch für eine Flüssigkeit? Was steht für Ethanol in der Tabelle?', 2: 'Eine Flüssigkeit hat keine eigene Länge. Welcher Koeffizient beschreibt ihr Volumen?'},
                             sprich='Welchen Koeffizienten nimmst du für das Ethanol? Gamma gleich eins Komma eins null Tausendstel pro Kelvin, gamma gleich drei mal eins Komma eins null Tausendstel, oder alpha gleich eins Komma eins null Tausendstel pro Kelvin?',
                             kopf='Dein Vorgehen')],
    'p5-3-lp-meer': [wahl('Vorgehen Meer', 'Welche Höhe setzt du für h₀ ein?', ['3700 m', '500 m', '3200 m'], 1,
                          {0: 'Dehnt sich auch Wasser aus, das nicht wärmer wird?', 2: 'Welche Schicht wird wärmer, die obere oder die untere?'},
                          sprich='Welche Höhe setzt du für h null ein?', kopf='Dein Vorgehen')],
    'p5-3-lp-gas': [wahl('Vorgehen Fussball', 'Welchen Druck setzt du für p₁ ein?', ['0.9 bar', '1.9 bar', '−0.1 bar'], 1,
                         {0: 'Das Manometer zeigt den Überdruck. Welcher Druck gehört in die Gasgleichung?', 2: 'Wird der Luftdruck abgezählt oder dazugezählt?'},
                         sprich='Welchen Druck setzt du für p eins ein?', kopf='Dein Vorgehen')],
    'p5-3-lp-spezialfaelle': [wahl('Vorgehen Druckluft', 'Welches Gesetz passt?', ['isotherm: p · V konstant', 'isochor: p / T konstant', 'isobar: V / T konstant'], 1,
                                   {0: 'Bleibt die Temperatur in der Sonne gleich?', 2: 'Kann der Druck in einem starren Behälter gleich bleiben?'},
                                   sprich='Welches Gesetz passt? Isotherm, p mal V konstant, isochor, p durch T konstant, oder isobar, V durch T konstant?', kopf='Dein Vorgehen')],
}
for d in DREH:
    d['fragen'] = FRAGEN[d['dateiname']]


# ================================================================== Kontrollclips
def kontrolle(n, kap, titel_, kurz, schlag, fragen):
    """fragen: [(text, optionen, richtig, rueck, antwort_sprecher, formel, sprich, rueck_sprich, extra_elemente)]"""
    szenen, fr = [], []
    for i, (text, opt, ri, rueck, sprecher, fml, sprich, rs, extra) in enumerate(fragen, 1):
        el = []
        if fml:
            el.append(formel(fml[0], y=300, g=fml[1], ein=1.0))
        el += extra
        szenen.append({'name': 'Frage %d' % i, 'layout': 'zentriert', 'oben': 200, 'sprecher': sprecher, 'elemente': el})
        fr.append(wahl('Frage %d' % i, text, opt, ri, rueck, sprich=sprich, rueck_sprich=rs))
    return dict(KOPF, titel='Ausdehnung sehen: ' + titel_, dateiname=n, kurzbeschrieb=kurz, schlagworte=schlag, _probe=KTRL % kap,
                szenen=szenen, fragen=fr)


def nz(t, y=470, g=42):
    return notiz(t, y=y, ein=1.0, g=g)


# Bild zur Frage 2 der Länge: drei Geraden ohne Namen (die Namen setzt antworten.py nach der Antwort)
drei = graf([-6, 84], [-0.4, 4.6], [20, 40, 60], [1, 2, 3, 4], 'ΔT [K]', 'Δl [mm]', ein=0.05,
            strecken=[S((0, 0), (60, a * 3 * 60 * 1000), AUS, 5) for a in (12e-6, 18.4e-6, 23.8e-6)])
KONTROLLE = [
    kontrolle('p5-3-lp-kontrolle-laenge', 1, 'Kontrollfragen zur Längenausdehnung',
              'Vier Fragen zur Längenausdehnung: Temperaturdifferenz mit Minus, welche Gerade zu welchem Werkstoff gehört, die neue Länge beim Abkühlen und α aus einer Messung.',
              ['Längenausdehnung', 'Ausdehnungskoeffizient', 'Kontrollfragen'], [
        ('Das Stahlseil einer Seilbahn ist 900 m lang. Im Winter hat es −10 °C, im Sommer 25 °C. Um wie viel ist es im Sommer länger?',
         ['16.2 cm', '37.8 cm', '3.22 m'], 1,
         {0: 'Wie gross ist der Abstand von −10 °C bis 25 °C?', 2: 'In der Formel steht die Temperaturänderung, nicht eine Temperatur in Kelvin.'},
         'Delta T ist fünfundzwanzig minus minus zehn, also fünfunddreissig Kelvin. Zwölf Millionstel mal neunhundert Meter mal fünfunddreissig Kelvin ergibt null Komma drei sieben acht Meter, rund achtunddreissig Zentimeter.',
         (r'\Delta l = 12 \cdot 10^{-6}' + K1 + r' \cdot 900\;\text{m} \cdot 35\;\text{K} \approx 0.378\;\text{m}', 32),
         'Das Stahlseil einer Seilbahn ist neunhundert Meter lang. Im Winter hat es minus zehn Grad, im Sommer fünfundzwanzig Grad. Um wie viel ist es im Sommer länger?',
         {0: 'Wie gross ist der Abstand von minus zehn Grad bis fünfundzwanzig Grad?', 2: 'In der Formel steht die Temperaturänderung, nicht eine Temperatur in Kelvin.'}, []),
        ('Drei gleich lange Stäbe aus Stahl, Messing und Aluminium werden erwärmt. Welche Gerade im Bild gehört zu Messing?',
         ['die steilste', 'die mittlere', 'die flachste'], 1,
         {0: 'Welcher der drei Werkstoffe hat das grösste α?', 2: 'Welcher der drei Werkstoffe hat das kleinste α?'},
         'Je grösser alpha, desto steiler die Gerade. Messing liegt mit achtzehn Komma vier Millionstel zwischen Stahl mit zwölf und Aluminium mit dreiundzwanzig Komma acht. Seine Gerade ist die mittlere.',
         None, None, {0: 'Welcher der drei Werkstoffe hat das grösste alpha?', 2: 'Welcher der drei Werkstoffe hat das kleinste alpha?'},
         [nz('Steigung ~ α', y=300), drei]),
        ('Eine Aluminiumleiste ist bei 20 °C genau 2.500 m lang. Wie lang ist sie bei −20 °C?',
         ['2.5024 m', '−2.38 mm', '2.4976 m'], 2,
         {0: 'Wird die Leiste beim Abkühlen länger?', 1: 'Das ist die Änderung. Wonach ist gefragt?'},
         'Delta T ist minus vierzig Kelvin. Dreiundzwanzig Komma acht Millionstel mal zwei Komma fünf Meter mal minus vierzig Kelvin ergibt minus zwei Komma drei acht Millimeter. Die Leiste ist dann zwei Komma vier neun sieben sechs Meter lang.',
         (r'\Delta l = 23.8 \cdot 10^{-6}' + K1 + r' \cdot 2.5\;\text{m} \cdot (-40\;\text{K}) \approx -2.38\;\text{mm}', 30),
         'Eine Aluminiumleiste ist bei zwanzig Grad genau zwei Komma fünf null null Meter lang. Wie lang ist sie bei minus zwanzig Grad?', None,
         [nz(r'@l = 2.500\;\text{m} - 0.00238\;\text{m} \approx 2.4976\;\text{m}@', y=430, g=36)]),
        ('Ein Stab von 5.00 m wird um 50 K wärmer und dabei 4.6 mm länger. Wie gross ist α?',
         ['18.4·10⁻³ 1/K', '54 300 1/K', '18.4·10⁻⁶ 1/K'], 2,
         {0: 'In welcher Einheit hast du Δl eingesetzt?', 1: 'Steht Δl im Zähler oder im Nenner?'},
         'Alpha ist Delta l durch l null mal Delta T: null Komma null null vier sechs Meter durch fünf Meter mal fünfzig Kelvin. Das gibt achtzehn Komma vier Millionstel pro Kelvin. Der Stab ist aus Messing.',
         (r'\alpha = \frac{\Delta l}{l_0 \cdot \Delta T} = \frac{0.0046\;\text{m}}{5.00\;\text{m} \cdot 50\;\text{K}} = 18.4 \cdot 10^{-6}' + K1, 30),
         'Ein Stab von fünf Metern wird um fünfzig Kelvin wärmer und dabei vier Komma sechs Millimeter länger. Wie gross ist alpha?',
         {0: 'In welcher Einheit hast du Delta l eingesetzt?', 1: 'Steht Delta l im Zähler oder im Nenner?'}, [nz('Messing', y=460)]),
    ]),
    kontrolle('p5-3-lp-kontrolle-volumen', 2, 'Kontrollfragen zur Volumenausdehnung',
              'Vier Fragen zur Volumenausdehnung: γ aus α für einen Würfel, der randvolle Behälter, der Platz im Tank und wie ΔV mit Volumen und Erwärmung wächst.',
              ['Volumenausdehnung', 'gamma', 'Kontrollfragen'], [
        ('Ein Messingwürfel (α = 18.4·10⁻⁶ 1/K) hat 500 cm³. Um wie viel wächst sein Volumen bei 100 K Erwärmung?',
         ['0.92 cm³', '1.84 cm³', '2.76 cm³'], 2,
         {0: 'Hast du α direkt eingesetzt? Für das Volumen braucht es γ.', 1: 'In wie viele Richtungen wächst ein Würfel?'},
         'Gamma ist drei mal alpha, fünfundfünfzig Komma zwei Millionstel pro Kelvin. Mal fünfhundert Kubikzentimeter mal hundert Kelvin: zwei Komma sieben sechs Kubikzentimeter.',
         (r'\Delta V = 3 \cdot 18.4 \cdot 10^{-6}' + K1 + r' \cdot 500\;\text{cm}^3 \cdot 100\;\text{K} = 2.76\;\text{cm}^3', 30),
         'Ein Messingwürfel mit alpha gleich achtzehn Komma vier Millionstel pro Kelvin hat fünfhundert Kubikzentimeter. Um wie viel wächst sein Volumen bei hundert Kelvin Erwärmung?',
         {0: 'Hast du alpha direkt eingesetzt? Für das Volumen braucht es gamma.', 1: 'In wie viele Richtungen wächst ein Würfel?'}, []),
        ('Ein randvoller Behälter aus Stahl mit Ethanol wird erwärmt. Läuft etwas über?',
         ['nein, der Behälter wächst mit', 'ja, das Ethanol wächst viel stärker', 'nein, Ethanol zieht sich zusammen'], 1,
         {0: 'Vergleiche γ von Ethanol und von Stahl.', 2: 'Was tun die meisten Stoffe beim Erwärmen?'},
         'Auch der Behälter wächst, aber Stahl hat ein rund dreissigmal kleineres Gamma als Ethanol. Das Ethanol wächst viel stärker; der Unterschied läuft über.',
         None, None, {0: 'Vergleiche gamma von Ethanol und von Stahl.', 2: 'Was tun die meisten Stoffe beim Erwärmen?'},
         [nz('Es läuft über:|@\\Delta V_\\text{Fl} - \\Delta V_\\text{Gef}@', y=300)]),
        ('Ein Tank mit 1000 l Ethanol kann sich um 25 K erwärmen. Wie viel Platz muss frei bleiben?',
         ['27.5 l', '0.0275 l', '5.25 l'], 0,
         {1: 'Welche Zehnerpotenz hat γ von Ethanol?', 2: 'Mit welchem Stoffwert hast du gerechnet?'},
         'Eins Komma eins null Tausendstel mal tausend Liter mal fünfundzwanzig Kelvin: Siebenundzwanzig Komma fünf Liter müssen frei bleiben.',
         (r'\Delta V = 1.10 \cdot 10^{-3}' + K1 + r' \cdot 1000\;\text{l} \cdot 25\;\text{K} = 27.5\;\text{l}', 32),
         'Ein Tank mit tausend Litern Ethanol kann sich um fünfundzwanzig Kelvin erwärmen. Wie viel Platz muss frei bleiben?',
         {1: 'Welche Zehnerpotenz hat gamma von Ethanol?', 2: 'Mit welchem Stoffwert hast du gerechnet?'}, []),
        ('1 l Ethanol wächst bei 20 K Erwärmung um 22 ml. Um wie viel wachsen 3 l bei 40 K?',
         ['66 ml', '132 ml', '44 ml'], 1,
         {0: 'Hast du auch die doppelte Erwärmung berücksichtigt?', 2: 'Hast du auch das dreifache Volumen berücksichtigt?'},
         'Dreifaches Volumen gibt dreimal so viel, doppelte Erwärmung noch einmal doppelt so viel: zweiundzwanzig mal drei mal zwei, hundertzweiunddreissig Milliliter.',
         (r'\Delta V = 22\;\text{ml} \cdot 3 \cdot 2 = 132\;\text{ml}', 40),
         'Ein Liter Ethanol wächst bei zwanzig Kelvin Erwärmung um zweiundzwanzig Milliliter. Um wie viel wachsen drei Liter bei vierzig Kelvin?', None, []),
    ]),
    kontrolle('p5-3-lp-kontrolle-meer', 3, 'Kontrollfragen zu Wasser und Meeresspiegel',
              'Vier Fragen: die Dichte nach dem Erwärmen, das Volumen von Wasser zwischen 1 °C und 4 °C, der Anstieg des Meeres und die nötige Erwärmung rückwärts.',
              ['Dichte', 'Anomalie', 'Meeresspiegel', 'Kontrollfragen'], [
        ('Ethanol hat bei 20 °C eine Dichte von 789 kg/m³. Wie gross ist sie bei 50 °C?',
         ['815 kg/m³', '789 kg/m³', '764 kg/m³'], 2,
         {0: 'Das Volumen wächst, die Masse bleibt. Wird die Dichte dann grösser?', 1: 'Bleibt das Volumen beim Erwärmen gleich?'},
         'Rho null durch eins plus gamma mal Delta T: siebenhundertneunundachtzig durch eins Komma null drei drei, rund siebenhundertvierundsechzig Kilogramm pro Kubikmeter.',
         (r'\rho = \frac{789\;\text{kg/m}^3}{1 + 1.10 \cdot 10^{-3}' + K1 + r' \cdot 30\;\text{K}} \approx 764\;\text{kg/m}^3', 32),
         'Ethanol hat bei zwanzig Grad eine Dichte von siebenhundertneunundachtzig Kilogramm pro Kubikmeter. Wie gross ist sie bei fünfzig Grad?', None, []),
        ('Wasser wird von 1 °C auf 4 °C erwärmt. Was geschieht mit seinem Volumen?',
         ['es wächst', 'es nimmt ab', 'es bleibt gleich'], 1,
         {0: 'Bei welcher Temperatur hat Wasser seine grösste Dichte?', 2: 'Ist die Dichte bei 1 °C und bei 4 °C gleich?'},
         'Bis vier Grad steigt die Dichte von Wasser. Gleiche Masse und grössere Dichte heisst: Das Volumen nimmt ab. Das ist die Anomalie des Wassers.',
         None, 'Wasser wird von einem Grad auf vier Grad erwärmt. Was geschieht mit seinem Volumen?',
         {0: 'Bei welcher Temperatur hat Wasser seine grösste Dichte?', 2: 'Ist die Dichte bei einem Grad und bei vier Grad gleich?'},
         [nz('Dichte steigt bis 4 °C:|Volumen nimmt ab', y=300)]),
        ('Das Meer ist hier 3700 m tief. Die obersten 250 m erwärmen sich um 2 K. Um wie viel steigt der Meeresspiegel?',
         ['10.5 cm', '1.55 m', '0.105 mm'], 0,
         {1: 'Dehnt sich auch das Tiefenwasser aus, das nicht wärmer wird?', 2: 'Welche Zehnerpotenz hat γ von Wasser?'},
         'Nur die erwärmte Schicht zählt: null Komma zwei eins Tausendstel mal zweihundertfünfzig Meter mal zwei Kelvin, das sind null Komma eins null fünf Meter, also zehn Komma fünf Zentimeter.',
         (r'\Delta h = 0.21 \cdot 10^{-3}' + K1 + r' \cdot 250\;\text{m} \cdot 2\;\text{K} = 0.105\;\text{m}', 32),
         'Das Meer ist hier dreitausendsiebenhundert Meter tief. Die obersten zweihundertfünfzig Meter erwärmen sich um zwei Kelvin. Um wie viel steigt der Meeresspiegel?',
         {1: 'Dehnt sich auch das Tiefenwasser aus, das nicht wärmer wird?', 2: 'Welche Zehnerpotenz hat gamma von Wasser?'}, []),
        ('Wie stark muss sich eine 400 m dicke Schicht erwärmen, damit das Meer um 6 cm steigt?',
         ['1.4 K', '71 K', '0.71 K'], 2,
         {0: 'Steht Δh im Zähler oder im Nenner?', 1: 'In welcher Einheit hast du Δh eingesetzt?'},
         'Delta T ist Delta h durch gamma mal h null: null Komma null sechs Meter durch null Komma zwei eins Tausendstel mal vierhundert Meter, rund null Komma sieben eins Kelvin.',
         (r'\Delta T = \frac{\Delta h}{\gamma \cdot h_0} = \frac{0.06\;\text{m}}{0.21 \cdot 10^{-3}' + K1 + r' \cdot 400\;\text{m}} \approx 0.71\;\text{K}', 30),
         'Wie stark muss sich eine vierhundert Meter dicke Schicht erwärmen, damit das Meer um sechs Zentimeter steigt?',
         {0: 'Steht Delta h im Zähler oder im Nenner?', 1: 'In welcher Einheit hast du Delta h eingesetzt?'}, []),
    ]),
    kontrolle('p5-3-lp-kontrolle-gas', 4, 'Kontrollfragen zur Gasgleichung',
              'Vier Fragen zur allgemeinen Gasgleichung: Kelvin statt Celsius, absoluter Druck und Überdruck, wann die Gasmenge gleich bleibt, und die aufsteigende Luftblase.',
              ['ideales Gas', 'Gasgleichung', 'Überdruck', 'Kontrollfragen'], [
        ('Luft in einer starren Flasche hat 1.2 bar bei 10 °C. Sie wird auf 30 °C erwärmt. Wie gross ist der Druck jetzt?',
         ['3.6 bar', '1.28 bar', '1.12 bar'], 1,
         {0: 'Mit welcher Temperaturskala hast du gerechnet?', 2: 'Wird der Druck beim Erwärmen kleiner?'},
         'V eins gleich V zwei kürzt sich. In Kelvin: zweihundertdreiundachtzig Komma eins fünf und dreihundertdrei Komma eins fünf. Eins Komma zwei Bar mal dreihundertdrei Komma eins fünf durch zweihundertdreiundachtzig Komma eins fünf, rund eins Komma zwei acht Bar.',
         (r'p_2 = 1.2\;\text{bar} \cdot \frac{303.15\;\text{K}}{283.15\;\text{K}} \approx 1.28\;\text{bar}', 38),
         'Luft in einer starren Flasche hat eins Komma zwei Bar bei zehn Grad. Sie wird auf dreissig Grad erwärmt. Wie gross ist der Druck jetzt?', None, []),
        ('Ein Reifen zeigt bei 5 °C einen Überdruck von 1.6 bar. Bei 35 °C, Volumen gleich: Was zeigt das Manometer?',
         ['1.77 bar', '2.88 bar', '1.88 bar'], 2,
         {0: 'Mit welchem Druck hast du gerechnet: mit dem Überdruck oder mit dem absoluten?', 1: 'Was zeigt ein Manometer an: den absoluten Druck oder den Überdruck?'},
         'Absolut sind es zwei Komma sechs Bar. Mal dreihundertacht Komma eins fünf durch zweihundertachtundsiebzig Komma eins fünf: zwei Komma acht acht Bar absolut. Das Manometer zeigt den Überdruck, eins Komma acht acht Bar.',
         (r'p_2 = 2.6\;\text{bar} \cdot \frac{308.15\;\text{K}}{278.15\;\text{K}} \approx 2.88\;\text{bar}', 38),
         'Ein Reifen zeigt bei fünf Grad einen Überdruck von eins Komma sechs Bar. Bei fünfunddreissig Grad, mit gleichem Volumen: Was zeigt das Manometer?', None,
         [nz(r'@p_\text{ü} = 2.88\;\text{bar} - 1.0\;\text{bar} = 1.88\;\text{bar}@', y=440, g=38)]),
        ('Ein Ballon verliert über Nacht Gas durch die Hülle. Darf man die Gasgleichung zwischen Abend und Morgen anwenden?',
         ['ja, wenn T in Kelvin steht', 'nein, die Gasmenge ändert sich', 'ja, immer'], 1,
         {0: 'Kelvin ist nötig. Aber was muss sonst noch gleich bleiben?', 2: 'Gilt die Gleichung auch, wenn Gas hinausströmt?'},
         'Die Gasgleichung vergleicht zwei Zustände derselben Gasmenge. Strömt Gas hinaus, stimmt sie nicht mehr.',
         None, None, None, [nz('nur für eine feste Gasmenge', y=300)]),
        ('Eine Luftblase hat in der Tiefe 6 cm³ bei 3.0 bar und 8 °C. An der Oberfläche herrschen 1.0 bar und 16 °C. Welches Volumen hat sie dort?',
         ['2.06 cm³', '18.5 cm³', '36 cm³'], 1,
         {0: 'Der Druck nimmt ab. Wird die Blase grösser oder kleiner?', 2: 'Mit welcher Temperaturskala hast du gerechnet?'},
         'V zwei gleich p eins mal V eins mal T zwei durch T eins mal p zwei: drei Bar mal sechs Kubikzentimeter mal zweihundertneunundachtzig Komma eins fünf Kelvin, durch zweihunderteinundachtzig Komma eins fünf Kelvin mal ein Bar. Das sind rund achtzehn Komma fünf Kubikzentimeter.',
         (r'V_2 = \frac{3.0\;\text{bar} \cdot 6\;\text{cm}^3 \cdot 289.15\;\text{K}}{281.15\;\text{K} \cdot 1.0\;\text{bar}} \approx 18.5\;\text{cm}^3', 32),
         'Eine Luftblase hat in der Tiefe sechs Kubikzentimeter bei drei Bar und acht Grad. An der Oberfläche herrschen ein Bar und sechzehn Grad. Welches Volumen hat sie dort?', None, []),
    ]),
    kontrolle('p5-3-lp-kontrolle-spezialfaelle', 5, 'Kontrollfragen zu den Spezialfällen',
              'Vier Fragen: welcher Fall bei einer erhitzten Dose vorliegt, der Druck in der zugehaltenen Pumpe, wie eine Isobare im V-T-Diagramm verläuft und das Volumen bei konstantem Druck.',
              ['isotherm', 'isobar', 'isochor', 'Kontrollfragen'], [
        ('Eine verschlossene, starre Konservendose wird im Feuer erhitzt. Welcher Fall liegt vor?',
         ['isotherm', 'isobar', 'isochor'], 2,
         {0: 'Bleibt die Temperatur im Feuer gleich?', 1: 'Kann der Druck in der starren Dose gleich bleiben?'},
         'Die Dose ist starr, ihr Volumen bleibt: isochor. Der Druck steigt mit der absoluten Temperatur, darum kann sie platzen.',
         None, None, None, [nz('Volumen konstant: isochor', y=300)]),
        ('Eine zugehaltene Velopumpe: 180 cm³ Luft bei 1.0 bar werden langsam auf 60 cm³ gedrückt. Wie gross ist der absolute Druck?',
         ['0.33 bar', '2.0 bar', '3.0 bar'], 2,
         {0: 'Wird der Druck beim Zusammendrücken kleiner?', 1: 'Hast du den Luftdruck abgezählt? Gefragt ist der absolute Druck.'},
         'Isotherm: p eins mal V eins gleich p zwei mal V zwei. Ein Drittel des Volumens gibt den dreifachen Druck: drei Bar.',
         (r'p_2 = \frac{1.0\;\text{bar} \cdot 180\;\text{cm}^3}{60\;\text{cm}^3} = 3.0\;\text{bar}', 40),
         'Eine zugehaltene Velopumpe: hundertachtzig Kubikzentimeter Luft bei einem Bar werden langsam auf sechzig Kubikzentimeter gedrückt. Wie gross ist der absolute Druck?', None, []),
        ('Im V-T-Diagramm, mit T in Kelvin: Wie verläuft eine Isobare?',
         ['als Gerade durch den Ursprung', 'waagrecht', 'als Hyperbel'], 0,
         {1: 'Bleibt das Volumen beim Erwärmen gleich, wenn der Druck konstant ist?', 2: 'Welche Grössen gehören zur Hyperbel?'},
         'Bei konstantem Druck ist V durch T konstant: Volumen und Kelvin-Temperatur sind proportional. Das gibt eine Gerade durch den Ursprung.',
         None, 'Im V-T-Diagramm, mit T in Kelvin: Wie verläuft eine Isobare?', None, [nz('@\\dfrac{V}{T}@ konstant', y=300)]),
        ('Ein Zylinder mit frei beweglichem Kolben enthält 2.5 l Luft bei 27 °C. Sie wird auf 87 °C erwärmt. Welches Volumen hat sie dann?',
         ['8.06 l', '2.08 l', '3.00 l'], 2,
         {0: 'Mit welcher Temperaturskala hast du gerechnet?', 1: 'Wird das Volumen beim Erwärmen kleiner?'},
         'Isobar: V zwei gleich V eins mal T zwei durch T eins. Zwei Komma fünf Liter mal dreihundertsechzig Komma eins fünf durch dreihundert Komma eins fünf: drei Liter.',
         (r'V_2 = 2.5\;\text{l} \cdot \frac{360.15\;\text{K}}{300.15\;\text{K}} \approx 3.00\;\text{l}', 38),
         'Ein Zylinder mit frei beweglichem Kolben enthält zwei Komma fünf Liter Luft bei siebenundzwanzig Grad. Sie wird auf siebenundachtzig Grad erwärmt. Welches Volumen hat sie dann?', None, []),
    ]),
]

for d in DREH + KONTROLLE:
    n = d['dateiname']
    if NUR and n not in NUR:
        continue
    p = os.path.join(CLIPS, n + '.json')
    if os.path.exists(p) and not NEU:
        print('vorhanden', n)
        continue
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('geschrieben', n)
