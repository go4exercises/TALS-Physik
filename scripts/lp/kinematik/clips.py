"""Erzeugt die zehn Drehbücher des Leitprogramms Kinematik (clips/p4-1-lp-*.json).

  python3 scripts/lp/kinematik/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/kinematik/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/kinematik/clips.py --neu p4-1-lp-kontrolle-wurf …   # nur diese

Archiv-Werkzeug wie scripts/lp/elektrizitaet/clips.py: Nach der Vertonung sind die JSONs in
clips/ die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf
mit --neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).

Farben wie in den Simulationen, soweit das Clip-Theme sie kennt: \\fa s (Bernstein), \\fc v
(Grün), \\fd a_z und v_Ufer (Rot). Violett (a, v_F) kennt das Theme nicht — diese Grössen bleiben
ungefärbt, statt eine Farbe mit anderer Bedeutung zu tragen. Zahlen im Sprechertext ausgeschrieben
(CLAUDE.md). Kontrollclips: neue Beispiele, richtige Antwort an wechselnden Stellen, Bild erst
nach der Antwort.
"""
import json
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv

KOPF = {
    'themenbereich': 'Mechanik · BM', 'lerngebiet': '4 · Mechanik',
    'lektion': ['p4-1'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-04', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Bewegung sehen', 'nachlauf': 2.6, 'probe': True,
}
JETZT = {'name': 'Jetzt du', 'layout': 'zentriert', 'oben': 200,
         'sprecher': 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
         'elemente': [{'typ': 'titel', 'text': 'Jetzt du', 'x': 150, 'y': 280, 'groesse': 86},
                      {'typ': 'notiz', 'text': 'Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.',
                       'x': 150, 'y': 430, 'groesse': 50, 'farbe': 'blau', 'ein': 0.6}]}


def formel(t, y=300, g=54, ein=0.8):
    return {'typ': 'formel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'ein': ein}


def notiz(t, y=460, farbe='tinte', ein=2.4, g=46):
    return {'typ': 'notiz', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'farbe': farbe, 'ein': ein}


def titel(t, y=300, g=86):
    return {'typ': 'titel', 'text': t, 'x': 150, 'y': y, 'breite': 1640, 'groesse': g}


def bild(datei, breite=760, y=200, ein=0.05):
    return {'typ': 'bild', 'datei': 'bilder/' + datei, 'x': 1010, 'y': y, 'breite': breite, 'abstand': 0, 'anim': 'fade', 'ein': ein}


def graf(geraden, x, y, xt, yt, xname, yname, punkte=None, kurven=None):
    for ge in geraden:
        ge.setdefault('ab', 0)   # keine negative Zeit
    g = {'typ': 'graf', 'x': 1010, 'y': 175, 'breite': 760, 'hoehe': 760, 'abstand': 0, 'anim': 'fade', 'ein': 0.05,
         'geraden': geraden, 'pfeile': True, 'xbereich': x, 'ybereich': y,
         'xteilung': [[v, '%g' % v] for v in xt], 'yteilung': [[v, '%g' % v] for v in yt], 'xname': xname, 'yname': yname}
    if punkte:
        g['punkte'] = punkte
    if kurven:
        g['kurven'] = kurven
    return g


# s-t- und v-t-Fenster wie Simulation 1 und 2 der Seite
def graf_st(geraden, punkte=None):
    return graf(geraden, [-1.5, 12.6], [-16, 124], [2, 4, 6, 8, 10, 12], [20, 40, 60, 80, 100, 120], 't [s]', 's [m]', punkte)


def graf_vt(geraden, punkte=None):
    return graf(geraden, [-1.4, 11], [-4, 34], [2, 4, 6, 8, 10], [10, 20, 30], 't [s]', 'v [m/s]', punkte)


def sz(name, sprecher, *elemente):
    return {'name': name, 'layout': 'zentriert', 'oben': 200, 'sprecher': sprecher, 'elemente': list(elemente)}


def wahl(szene, text, optionen, richtig, rueck, sprich=None, rueck_sprich=None):
    F = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'text': text, 'optionen': optionen, 'richtig': richtig,
         'rueck': {str(k): v for k, v in rueck.items()}}
    if sprich:
        F['sprich'] = sprich
    if rueck_sprich:
        F['rueck_sprich'] = {str(k): v for k, v in rueck_sprich.items()}
    return F


DREH = []
EIN = 'Einführungsclip des Leitprogramms Kinematik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Kinematik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'

# ================================================================== Kapitel 1
DREH.append(dict(KOPF, titel='Bewegung sehen: Ort, Bahn und Tempo', dateiname='p4-1-lp-gleichfoermig',
    kurzbeschrieb='Schwerpunkt und Bahnkurve, Durchschnitts- und Momentangeschwindigkeit, und warum die Geschwindigkeit die Steigung im s-t-Diagramm ist.',
    schlagworte=['Schwerpunkt', 'Bahnkurve', 'Geschwindigkeit', 'gleichförmige Bewegung', 's-t-Diagramm'], _probe=EIN % 1,
    szenen=[
        sz('Schwerpunkt', 'Ein Velo samt Fahrerin besteht aus vielen Teilen. Für die Bewegung genügt ein einziger Punkt: der Schwerpunkt. Er bewegt sich so, als wäre die ganze Masse in ihm vereinigt.',
           titel('Ein Punkt genügt'),
           notiz('Schwerpunkt:|Punkt, in dem man sich|die ganze Masse denkt', y=440, ein=4.0)),
        sz('Bahnkurve', 'Die Linie, die der Schwerpunkt durchläuft, heisst Bahnkurve. Sie kann gerade sein wie auf einer geraden Strasse, kreisförmig wie beim Riesenrad oder gekrümmt wie beim geworfenen Ball.',
           titel('Die Bahnkurve', g=76),
           notiz('gerade: Strasse|kreisförmig: Riesenrad|gekrümmt: geworfener Ball', y=440, ein=3.0)),
        sz('Durchschnitt', 'Ein Zug fährt hundertzwanzig Kilometer in einer Stunde. Seine Durchschnittsgeschwindigkeit ist hundertzwanzig Kilometer pro Stunde, auch wenn die Anzeige im Wagen mal hundertfünfzig, mal null zeigt. Die Anzeige liefert die Momentangeschwindigkeit.',
           formel(r'\fc{\bar v} = \dfrac{\Delta s}{\Delta t} = \dfrac{120\;\text{km}}{1\;\text{h}} = \fc{120\;\text{km/h}}', g=50),
           notiz('Anzeige im Wagen:|Momentangeschwindigkeit', ein=9.0)),
        sz('Gleichförmig', 'Eine Velofahrerin startet zwanzig Meter nach dem Nullpunkt und fährt gleichförmig mit fünf Metern pro Sekunde. Ihr Ort ist der Startort plus Geschwindigkeit mal Zeit. Im Diagramm wird das eine Gerade.',
           formel(r'\fa{s} = \fa{s_0} + \fc{v} \cdot t = \fa{20\;\text{m}} + \fc{5\;\text{m/s}} \cdot t', g=48),
           notiz('Startort: Achsenabschnitt', ein=6.0),
           graf_st([{'bewegung': [[0.5, 0, 20], [7.0, 5, 20]], 'farbe': 1, 'yachse': {'farbe': 5}}])),
        sz('Steigung', 'Die Steigung der Geraden ist die Geschwindigkeit: In jeder Sekunde kommen fünf Meter dazu. Nach acht Sekunden ist sie bei zwanzig plus vierzig, also sechzig Metern.',
           formel(r'\fa{s} = 20\;\text{m} + \fc{5\;\text{m/s}} \cdot 8\;\text{s} = \fa{60\;\text{m}}', g=50, ein=4.0),
           notiz('Steigung:|Geschwindigkeit', ein=1.0),
           graf_st([{'bewegung': [[0, 5, 20]], 'farbe': 1, 'dreieck': {'x': 1, 'dx': 1}, 'marken': [{'x': 8, 'text': 's = {y} m', 'farbe': 5}]}])),
        sz('Schneller', 'Mit acht Metern pro Sekunde wird die Gerade steiler. Nach acht Sekunden ist sie bei vierundachtzig Metern. Und zum Umrechnen: Ein Meter pro Sekunde sind drei Komma sechs Kilometer pro Stunde.',
           formel(r'\fa{s} = 20\;\text{m} + \fc{8\;\text{m/s}} \cdot 8\;\text{s} = \fa{84\;\text{m}}', g=50),
           formel(r'1\;\text{m/s} = 3.6\;\text{km/h}', y=440, g=50, ein=7.0),
           graf_st([{'bewegung': [[0.6, 5, 20], [3.4, 8, 20]], 'farbe': 1, 'marken': [{'x': 8, 'text': 's = {y} m', 'farbe': 5}]}])),
        sz('Merke', 'Zum Mitnehmen: Ein Körper wird durch seinen Schwerpunkt beschrieben, sein Weg durch die Bahnkurve. Bei gleichförmiger Bewegung ist der Ort Startort plus Geschwindigkeit mal Zeit. Im Diagramm ist die Steigung die Geschwindigkeit.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fa{s} = \fa{s_0} + \fc{v} \cdot t', y=420, ein=0.4),
           notiz('Steigung: Geschwindigkeit|Achsenabschnitt: Startort|1 m/s = 3.6 km/h', y=560, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 2
DREH.append(dict(KOPF, titel='Bewegung sehen: Beschleunigung ist Steigung, Weg ist Fläche', dateiname='p4-1-lp-beschleunigt',
    kurzbeschrieb='Beschleunigung als Änderung der Geschwindigkeit pro Zeit, Steigung und Fläche im v-t-Diagramm und warum doppeltes Tempo den Bremsweg vervierfacht.',
    schlagworte=['Beschleunigung', 'v-t-Diagramm', 'Bewegungsgleichungen', 'Bremsweg'], _probe=EIN % 2,
    szenen=[
        sz('Beschleunigung', 'Ein Auto fährt aus dem Stand los und ist nach acht Sekunden zwanzig Meter pro Sekunde schnell. Die Beschleunigung ist die Änderung der Geschwindigkeit pro Zeit: zwanzig durch acht, zwei Komma fünf Meter pro Sekunde im Quadrat.',
           titel('Was ist Beschleunigung?', g=76),
           formel(r'a = \dfrac{\Delta \fc{v}}{\Delta t} = \dfrac{\fc{20\;\text{m/s}}}{8\;\text{s}} = 2.5\;\text{m/s}^2', y=440, g=50, ein=6.0),
           notiz('jede Sekunde|2.5 m/s schneller', y=620, ein=10.0)),
        sz('Gerade', 'Im v-t-Diagramm wird daraus eine Gerade. Ihre Steigung ist die Beschleunigung. Die Geschwindigkeit ist Anfangsgeschwindigkeit plus Beschleunigung mal Zeit.',
           formel(r'\fc{v} = \fc{v_0} + a \cdot t', g=56),
           notiz('Steigung:|Beschleunigung', ein=1.5),
           graf_vt([{'bewegung': [[0.5, 0, 0], [3.5, 2.5, 0]], 'farbe': 3, 'marken': [{'x': 8, 'text': 'v = {y} m/s', 'farbe': 5}]}])),
        sz('Fläche', 'Und der Weg? Er ist die Fläche unter der Geraden: ein Dreieck, ein halb mal acht Sekunden mal zwanzig Meter pro Sekunde, achtzig Meter. Dasselbe gibt ein halb mal a mal t Quadrat.',
           formel(r'\fa{s} = \tfrac12 \cdot a \cdot t^2 = \tfrac12 \cdot 2.5\;\text{m/s}^2 \cdot (8\;\text{s})^2 = \fa{80\;\text{m}}', g=40),
           notiz('Fläche unter der Geraden:|Weg', ein=1.0),
           bild('p4-1-lp-beschleunigt-1.jpg')),
        sz('Trapez', 'Fährt der Körper schon mit zehn Metern pro Sekunde und beschleunigt mit zwei, ist er nach fünf Sekunden zwanzig Meter pro Sekunde schnell. Die Fläche ist jetzt ein Trapez: fünfundsiebzig Meter.',
           formel(r'\fa{s} = \fc{v_0} \cdot t + \tfrac12 \cdot a \cdot t^2', g=50),
           formel(r'= \fc{10\;\text{m/s}} \cdot 5\;\text{s} + \tfrac12 \cdot 2\;\text{m/s}^2 \cdot (5\;\text{s})^2 = \fa{75\;\text{m}}', y=420, g=38, ein=5.0),
           bild('p4-1-lp-beschleunigt-2.jpg')),
        sz('Bremsen', 'Beim Bremsen ist die Beschleunigung negativ. Aus fünfzehn Metern pro Sekunde mit minus fünf Metern pro Sekunde im Quadrat steht das Auto nach drei Sekunden, nach zweiundzwanzig Komma fünf Metern.',
           formel(r'\fa{s} = \dfrac{\fc{v_0}^2}{2 \cdot |a|} = \dfrac{(\fc{15\;\text{m/s}})^2}{2 \cdot 5\;\text{m/s}^2} = \fa{22.5\;\text{m}}', g=44, ein=5.0),
           notiz('bremsen: a negativ', ein=1.0),
           bild('p4-1-lp-beschleunigt-3.jpg')),
        sz('Doppelt so schnell', 'Doppelt so schnell, dreissig Meter pro Sekunde: Das Dreieck wird doppelt so hoch und doppelt so breit. Der Bremsweg ist viermal so lang, neunzig Meter.',
           formel(r'\fa{s} = \dfrac{(\fc{30\;\text{m/s}})^2}{2 \cdot 5\;\text{m/s}^2} = \fa{90\;\text{m}}', g=44),
           notiz('doppeltes Tempo:|vierfacher Bremsweg', farbe='rot', ein=4.0),
           bild('p4-1-lp-beschleunigt-4.jpg')),
        sz('Merke', 'Zum Mitnehmen: Die Beschleunigung ist die Steigung im v-t-Diagramm, der Weg die Fläche darunter. Diese Gleichungen gelten nur bei konstanter Beschleunigung.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fc{v} = \fc{v_0} + a \cdot t \qquad \fa{s} = \fc{v_0} \cdot t + \tfrac12 \cdot a \cdot t^2', y=420, g=44, ein=0.4),
           notiz('Steigung: Beschleunigung|Fläche: Weg|nur für konstantes a', y=560, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 3
DREH.append(dict(KOPF, titel='Bewegung sehen: Fall und Wurf in zwei Richtungen', dateiname='p4-1-lp-wurf',
    kurzbeschrieb='Freier Fall mit g, dann der Wurf als zwei Bewegungen: waagrecht gleichförmig, senkrecht wie der freie Fall.',
    schlagworte=['freier Fall', 'Erdbeschleunigung', 'waagrechter Wurf', 'schiefer Wurf', 'Wurfparabel'], _probe=EIN % 3,
    szenen=[
        sz('Freier Fall', 'Ohne Luftwiderstand fallen alle Körper gleich: gleichmässig beschleunigt mit g, neun Komma acht eins Meter pro Sekunde im Quadrat. Nach drei Sekunden ist ein Stein neunundzwanzig Komma vier Meter pro Sekunde schnell.',
           titel('Alle fallen gleich', g=76),
           formel(r'\fc{v} = g \cdot t = 9.81\;\text{m/s}^2 \cdot 3\;\text{s} \approx \fc{29.4\;\text{m/s}}', y=440, g=48, ein=7.0),
           notiz('unabhängig von der Masse', y=620, ein=2.0)),
        sz('Fallweg', 'Der Fallweg wächst mit dem Quadrat der Zeit: ein halb mal g mal t Quadrat. Nach einer Sekunde vier Komma neun Meter, nach zwei Sekunden das Vierfache, neunzehn Komma sechs, nach drei Sekunden vierundvierzig.',
           formel(r'\fa{h} = \tfrac12 \cdot g \cdot t^2', g=56),
           notiz('doppelte Zeit:|vierfacher Weg', ein=5.0),
           graf([], [-0.35, 3.6], [-5, 50], [1, 2, 3], [10, 20, 30, 40], 't [s]', 'h [m]',
                punkte=[{'x': 1, 'y': 4.905, 'farbe': 1, 'beschriftung': '4.9 m', 'beschriftung_bei': [1.12, 2.0]},
                        {'x': 2, 'y': 19.62, 'farbe': 1, 'beschriftung': '19.6 m', 'beschriftung_bei': [2.12, 16.6]},
                        {'x': 3, 'y': 44.145, 'farbe': 1, 'beschriftung': '44.1 m', 'beschriftung_bei': [2.9, 46.0], 'anker': 'end'}],
                kurven=[{'formel': '0.5*9.81*x**2', 'farbe': 1, 'von': 0, 'bis': 3.15}])),
        sz('Waagrecht', 'Jetzt wird ein Ball aus zwanzig Metern Höhe waagrecht mit acht Metern pro Sekunde geworfen. Die Punkte zeigen ihn alle Viertelsekunden. Waagrecht kommen immer gleich viele Meter dazu: Diese Bewegung ist gleichförmig.',
           notiz('waagrecht:|gleiche Abstände,|gleichförmig', y=300, ein=6.0, g=50),
           bild('p4-1-lp-wurf-1.jpg', y=240)),
        sz('Senkrecht', 'Senkrecht fällt er wie ein fallen gelassener Stein, die Abstände wachsen. Darum dauert der Flug zwei Komma null zwei Sekunden, genau wie beim freien Fall aus zwanzig Metern. In dieser Zeit kommt er sechzehn Meter weit.',
           formel(r't = \sqrt{\dfrac{2h}{g}} = \sqrt{\dfrac{2 \cdot 20\;\text{m}}{9.81\;\text{m/s}^2}} \approx 2.02\;\text{s}', g=44),
           formel(r'x = \fc{v_0} \cdot t = \fc{8\;\text{m/s}} \cdot 2.02\;\text{s} \approx 16.2\;\text{m}', y=470, g=44, ein=9.0),
           bild('p4-1-lp-wurf-1.jpg', y=240)),
        sz('Schief', 'Wird der Ball schräg nach oben geworfen, steigt er zuerst. Vom Boden mit fünfzehn Metern pro Sekunde unter fünfundvierzig Grad fliegt er zwei Komma eins sechs Sekunden und landet zweiundzwanzig Komma neun Meter weit. Bei fünfundvierzig Grad ist die Weite am grössten.',
           formel(r'x = \fc{v_0} \cdot \cos\alpha \cdot t', y=280, g=48),
           formel(r'y = \fc{v_0} \cdot \sin\alpha \cdot t - \tfrac12 \cdot g \cdot t^2', y=400, g=48, ein=1.6),
           notiz('grösste Weite bei 45°', y=560, ein=12.0),
           bild('p4-1-lp-wurf-2.jpg', y=240)),
        sz('Merke', 'Zum Mitnehmen: Ein Wurf besteht aus zwei Bewegungen, waagrecht gleichförmig, senkrecht wie der freie Fall. Die Flugzeit kommt allein aus der senkrechten Bewegung.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fa{h} = \tfrac12 \cdot g \cdot t^2 \qquad g = 9.81\;\text{m/s}^2', y=420, g=48, ein=0.4),
           notiz('waagrecht: gleichförmig|senkrecht: freier Fall|Bahnkurve: Parabel', y=560, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 4
DREH.append(dict(KOPF, titel='Bewegung sehen: Geschwindigkeiten addieren sich als Pfeile', dateiname='p4-1-lp-vektor',
    kurzbeschrieb='Geschwindigkeit als Vektor: im Zug mit Vorzeichen, im Fluss mit Pythagoras, dazu Querzeit, Versatz und Vorhalten.',
    schlagworte=['Vektor', 'Relativbewegung', 'Vektoraddition', 'Querzeit', 'Versatz'], _probe=EIN % 4,
    szenen=[
        sz('Pfeil', 'Eine Geschwindigkeit hat einen Betrag und eine Richtung. Man zeichnet sie als Pfeil: Die Länge ist das Tempo, die Richtung zeigt, wohin es geht.',
           titel('Geschwindigkeit als Pfeil', g=76),
           notiz('Länge: Tempo|Richtung: wohin', y=440, ein=4.0)),
        sz('Im Zug', 'Im Zug, der mit dreissig Metern pro Sekunde fährt, geht jemand mit eins Komma fünf Metern pro Sekunde nach vorn. Gegenüber dem Boden ist er einunddreissig Komma fünf Meter pro Sekunde schnell. Geht er nach hinten, sind es achtundzwanzig Komma fünf.',
           formel(r'30\;\text{m/s} + 1.5\;\text{m/s} = 31.5\;\text{m/s}', g=50, ein=6.0),
           formel(r'30\;\text{m/s} - 1.5\;\text{m/s} = 28.5\;\text{m/s}', y=420, g=50, ein=13.0),
           notiz('gegenüber dem Zug: 1.5 m/s|gegenüber dem Boden: Summe', y=580, ein=2.0)),
        sz('Quer', 'Ein Schwimmer schwimmt mit zwei Metern pro Sekunde quer über einen Fluss, die Strömung hat einen Meter pro Sekunde. Die beiden Pfeile setzt man aneinander. Die Summe hat den Betrag Wurzel aus fünf, rund zwei Komma zwei vier Meter pro Sekunde.',
           formel(r'|\fd{\vec v_\text{Ufer}}| = \sqrt{(\fc{2\;\text{m/s}})^2 + (1\;\text{m/s})^2} \approx \fd{2.24\;\text{m/s}}', g=42, ein=8.0),
           notiz('Pfeile aneinandersetzen', ein=4.0),
           bild('p4-1-lp-vektor-1.jpg', y=280)),
        sz('Querzeit', 'Hinüber bringt ihn nur sein eigener Pfeil quer zum Ufer: vierzig Meter Flussbreite durch zwei Meter pro Sekunde, zwanzig Sekunden. In dieser Zeit treibt ihn die Strömung zwanzig Meter flussabwärts.',
           formel(r't = \dfrac{b}{\fc{v_S}} = \dfrac{40\;\text{m}}{\fc{2\;\text{m/s}}} = 20\;\text{s}', g=48),
           formel(r'd = v_F \cdot t = 1\;\text{m/s} \cdot 20\;\text{s} = 20\;\text{m}', y=450, g=48, ein=8.0),
           bild('p4-1-lp-vektor-1.jpg', y=280)),
        sz('Vorhalten', 'Soll er genau gegenüber ankommen, schwimmt er schräg gegen die Strömung. Bei hundertzwanzig Grad hebt sein Anteil gegen die Strömung den Fluss genau auf. Dafür dauert die Überquerung länger: rund dreiundzwanzig Sekunden.',
           formel(r'\fc{v_S} \cdot \cos 120^\circ = -1\;\text{m/s}', g=48, ein=4.0),
           formel(r't = \dfrac{40\;\text{m}}{\fc{2\;\text{m/s}} \cdot \sin 120^\circ} \approx 23.1\;\text{s}', y=450, g=46, ein=9.0),
           bild('p4-1-lp-vektor-2.jpg', y=280)),
        sz('Merke', 'Zum Mitnehmen: Geschwindigkeiten addieren sich als Pfeile. Auf einer Geraden mit Vorzeichen, quer dazu mit Pythagoras. Die Querzeit hängt nur vom Anteil quer zum Ufer ab.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fd{\vec v_\text{Ufer}} = \fc{\vec v_S} + \vec v_F', y=420, ein=0.4),
           notiz('gerade: Vorzeichen|quer: Pythagoras|Querzeit: nur der Anteil quer', y=560, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 5
DREH.append(dict(KOPF, titel='Bewegung sehen: Kreisbahn mit konstantem Tempo', dateiname='p4-1-lp-kreis',
    kurzbeschrieb='Umlaufzeit, Rotationsfrequenz und Winkelgeschwindigkeit, Bahngeschwindigkeit tangential und Zentripetalbeschleunigung zur Mitte.',
    schlagworte=['Kreisbewegung', 'Rotationsfrequenz', 'Winkelgeschwindigkeit', 'Zentripetalbeschleunigung'], _probe=EIN % 5,
    szenen=[
        sz('Umlauf', 'Ein Karussellsitz ist vier Meter von der Achse entfernt; ein Umlauf dauert vier Sekunden. Das ist die Umlaufzeit T. Ihr Kehrwert ist die Rotationsfrequenz: ein Viertel Umlauf pro Sekunde, null Komma zwei fünf Hertz.',
           titel('Im Kreis herum', g=76),
           formel(r'f = \dfrac{1}{T} = \dfrac{1}{4\;\text{s}} = 0.25\;\text{Hz}', y=440, g=50, ein=8.0)),
        sz('Winkelgeschwindigkeit', 'In einer Umlaufzeit dreht sich der Sitz um zwei Pi, einen ganzen Kreis im Bogenmass. Die Winkelgeschwindigkeit ist zwei Pi durch T: rund eins Komma fünf sieben Radiant pro Sekunde.',
           formel(r'\omega = \dfrac{2\pi}{T} = \dfrac{2\pi}{4\;\text{s}} \approx 1.57\;\text{rad/s}', g=50, ein=4.0),
           notiz('ein Umlauf: 2π rad', ein=1.0),
           bild('p4-1-lp-kreis-1.jpg', y=200)),
        sz('Bahngeschwindigkeit', 'Die Bahngeschwindigkeit ist Winkelgeschwindigkeit mal Radius: sechs Komma zwei acht Meter pro Sekunde. Ihr Pfeil liegt immer tangential an der Bahn.',
           formel(r'\fc{v} = \omega \cdot r = 1.57\;\text{rad/s} \cdot 4\;\text{m} \approx \fc{6.28\;\text{m/s}}', g=46),
           notiz('v: tangential', ein=5.0),
           bild('p4-1-lp-kreis-1.jpg', y=200)),
        sz('Zentripetal', 'Das Tempo bleibt gleich, aber die Richtung des Pfeils ändert sich ständig. Das ist eine Beschleunigung, und sie zeigt zur Mitte: die Zentripetalbeschleunigung, v Quadrat durch r, rund neun Komma acht sieben Meter pro Sekunde im Quadrat.',
           formel(r'\fd{a_z} = \dfrac{\fc{v}^2}{r} = \omega^2 \cdot r \approx \fd{9.87\;\text{m/s}^2}', g=50, ein=9.0),
           notiz('Richtung ändert sich:|Beschleunigung zur Mitte', ein=3.0),
           bild('p4-1-lp-kreis-2.jpg', y=200)),
        sz('Halber Radius', 'Mit halbem Radius, zwei Metern, bei gleicher Umlaufzeit ist auch die Zentripetalbeschleunigung halb so gross. Doppelte Umlaufzeit dagegen halbiert Omega, und Omega steht im Quadrat: nur noch ein Viertel.',
           formel(r'r = 2\;\text{m}: \quad \fd{a_z} \approx 4.93\;\text{m/s}^2', g=48, ein=1.0),
           formel(r'T = 8\;\text{s}: \quad \fd{a_z} \approx 2.47\;\text{m/s}^2', y=420, g=48, ein=8.0),
           bild('p4-1-lp-kreis-3.jpg', y=200)),
        sz('Merke', 'Zum Mitnehmen: f ist eins durch T, Omega zwei Pi durch T. Die Bahngeschwindigkeit ist Omega mal r und liegt tangential. Die Zentripetalbeschleunigung zeigt zur Mitte, obwohl das Tempo gleich bleibt.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\omega = \dfrac{2\pi}{T} \qquad \fc{v} = \omega \cdot r \qquad \fd{a_z} = \dfrac{\fc{v}^2}{r}', y=420, g=44, ein=0.4),
           notiz('v: tangential|Beschleunigung: zur Mitte', y=580, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kontrollclips
DREH.append(dict(KOPF, titel='Bewegung sehen: Kontrollfragen zu Ort und Geschwindigkeit', dateiname='p4-1-lp-kontrolle-gleichfoermig',
    kurzbeschrieb='Fünf Fragen zu Durchschnittsgeschwindigkeit, Bahnkurve, Ort im s-t-Diagramm, Steigung und km/h.',
    schlagworte=['Geschwindigkeit', 'Bahnkurve', 's-t-Diagramm', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Ganze Strecke durch ganze Zeit: hundertfünfzig Kilometer durch zwei Stunden, fünfundsiebzig Kilometer pro Stunde.',
           formel(r'\fc{\bar v} = \dfrac{150\;\text{km}}{2\;\text{h}} = \fc{75\;\text{km/h}}', ein=1.0)),
        sz('Frage 2', 'Der Schwerpunkt des Kindes bleibt immer gleich weit von der Achse entfernt: Seine Bahnkurve ist ein Kreis.',
           notiz('gleicher Abstand zur Achse:|Kreis', y=320, ein=1.0, g=50)),
        sz('Frage 3', 'Startort plus Geschwindigkeit mal Zeit: zehn plus vier mal fünf, dreissig Meter.',
           formel(r'\fa{s} = 10\;\text{m} + \fc{4\;\text{m/s}} \cdot 5\;\text{s} = \fa{30\;\text{m}}', ein=1.0),
           graf([{'bewegung': [[1.0, 0, 0], [3.2, 4, 10]], 'farbe': 1, 'marken': [{'x': 5, 'text': 's = {y} m', 'farbe': 5}]}],
                [-1.2, 11], [-7, 62], [2, 4, 6, 8, 10], [10, 20, 30, 40, 50, 60], 't [s]', 's [m]')),
        sz('Frage 4', 'Die Steigung ist die Geschwindigkeit: steiler heisst schneller. Wo eine Gerade beginnt, sagt nur der Achsenabschnitt.',
           notiz('steiler: schneller|Achsenabschnitt: Startort', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Ein Meter pro Sekunde sind drei Komma sechs Kilometer pro Stunde. Fünfundzwanzig mal drei Komma sechs: neunzig.',
           formel(r'25\;\text{m/s} = 25 \cdot 3.6\;\text{km/h} = 90\;\text{km/h}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Auto fährt 150 km in 2 h. Unterwegs zeigt der Tacho mal 120 km/h, mal 0 km/h. Wie gross ist die Durchschnittsgeschwindigkeit?',
             ['300 km/h', '75 km/h', '60 km/h'], 1,
             {0: 'Strecke mal Zeit? Die Durchschnittsgeschwindigkeit ist Strecke pro Zeit.', 2: 'Das ist der Mittelwert der beiden Tachowerte. Gefragt ist die ganze Strecke durch die ganze Zeit.'},
             sprich='Ein Auto fährt hundertfünfzig Kilometer in zwei Stunden. Unterwegs zeigt der Tacho mal hundertzwanzig, mal null Kilometer pro Stunde. Wie gross ist die Durchschnittsgeschwindigkeit?'),
        wahl('Frage 2', 'Ein Kind sitzt auf einem drehenden Karussell. Welche Form hat die Bahnkurve seines Schwerpunkts?',
             ['eine Gerade', 'eine Parabel', 'ein Kreis'], 2,
             {0: 'Kommt das Kind je weiter von der Achse weg?', 1: 'Eine Parabel entsteht beim Wurf. Wie läuft das Kind um die Achse?'}),
        {'szene': 'Frage 3', 'bei': 0.3, 'typ': 'klick',
         'text': 'Ein Velo startet bei 10 m und fährt mit 4 m/s. Wo ist es nach 5 s? Tipp den Punkt ins Bild oder gib ihn ein.',
         'sprich': 'Ein Velo startet bei zehn Metern und fährt mit vier Metern pro Sekunde. Wo ist es nach fünf Sekunden? Tipp den Punkt ins Bild oder gib ihn ein.',
         'ziel': [5, 30], 'toleranz': [0.4, 2.5], 'eingabe': ['t in s', 's in m'], 'richtig_text': 'Getroffen.',
         'fallen': [{'bei': [5, 20], 'text': 'Das ist nur der Weg seit dem Start. Der Startort kommt dazu.'},
                    {'bei': [5, 14], 'text': 'Startort plus Geschwindigkeit? Die Geschwindigkeit wird mit der Zeit multipliziert.'}],
         'falsch_text': 'Nicht ganz. Rechne Ort gleich Startort plus Geschwindigkeit mal Zeit und such den Wert bei t = 5 s.',
         'falsch_sprich': 'Nicht ganz. Rechne Ort gleich Startort plus Geschwindigkeit mal Zeit und such den Wert bei fünf Sekunden.'},
        wahl('Frage 4', 'Im s-t-Diagramm ist die Gerade von A steiler als die von B. Was heisst das?',
             ['A startet weiter vorn', 'A ist schneller', 'A startet früher'], 1,
             {0: 'Der Startort ist der Achsenabschnitt. Was sagt die Steigung?', 2: 'Beide Geraden zeigen dieselbe Zeit. Was sagt die Steigung?'}),
        wahl('Frage 5', '25 m/s sind wie viel km/h?', ['90 km/h', '6.9 km/h', '25 km/h'], 0,
             {1: 'Geteilt? Von Meter pro Sekunde in Kilometer pro Stunde wird die Zahl grösser.', 2: 'Die Zahl bleibt nicht gleich: Ein Meter pro Sekunde sind drei Komma sechs Kilometer pro Stunde.'},
             sprich='Fünfundzwanzig Meter pro Sekunde sind wie viel Kilometer pro Stunde?'),
    ]))

DREH.append(dict(KOPF, titel='Bewegung sehen: Kontrollfragen zur Beschleunigung', dateiname='p4-1-lp-kontrolle-beschleunigt',
    kurzbeschrieb='Fünf Fragen zu Beschleunigung, Fläche im v-t-Diagramm, Geschwindigkeit nach der Zeit t, Bremsweg und Vorzeichen.',
    schlagworte=['Beschleunigung', 'v-t-Diagramm', 'Bremsweg', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Die Geschwindigkeit ändert sich um fünfzehn Meter pro Sekunde, in fünf Sekunden: drei Meter pro Sekunde im Quadrat.',
           formel(r'a = \dfrac{\Delta \fc{v}}{\Delta t} = \dfrac{\fc{23\;\text{m/s}} - \fc{8\;\text{m/s}}}{5\;\text{s}} = 3\;\text{m/s}^2', g=46, ein=1.0)),
        sz('Frage 2', 'Höhe mal Breite: Meter pro Sekunde mal Sekunden gibt Meter. Die Fläche ist der Weg.',
           formel(r'\text{m/s} \cdot \text{s} = \text{m}', ein=1.0)),
        sz('Frage 3', 'Anfangsgeschwindigkeit plus Beschleunigung mal Zeit: vier plus zwei mal fünf, vierzehn Meter pro Sekunde.',
           formel(r'\fc{v} = \fc{4\;\text{m/s}} + 2\;\text{m/s}^2 \cdot 5\;\text{s} = \fc{14\;\text{m/s}}', g=50, ein=1.0),
           graf([{'bewegung': [[1.0, 0, 0], [3.2, 2, 4]], 'farbe': 3, 'marken': [{'x': 5, 'text': 'v = {y} m/s', 'farbe': 5}]}],
                [-1.2, 11], [-3, 26], [2, 4, 6, 8, 10], [5, 10, 15, 20, 25], 't [s]', 'v [m/s]')),
        sz('Frage 4', 'Doppeltes Tempo, vierfacher Bremsweg: Die Geschwindigkeit steht im Quadrat. Achtzig Meter.',
           formel(r'\fa{s} = \dfrac{\fc{v_0}^2}{2 \cdot |a|}', ein=1.0)),
        sz('Frage 5', 'Die Geschwindigkeit nimmt ab, ihre Änderung ist negativ. Also ist auch die Beschleunigung negativ.',
           formel(r'\Delta \fc{v} \lt 0 \;\Longrightarrow\; a \lt 0', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Motorrad wird in 5 s von 8 m/s auf 23 m/s schneller. Wie gross ist die Beschleunigung?',
             ['4.6 m/s²', '3 m/s²', '0.33 m/s²'], 1,
             {0: 'Das ist die Endgeschwindigkeit durch die Zeit. Gefragt ist die Änderung der Geschwindigkeit.', 2: 'Umgekehrt: Änderung der Geschwindigkeit durch die Zeit.'},
             sprich='Ein Motorrad wird in fünf Sekunden von acht auf dreiundzwanzig Meter pro Sekunde schneller. Wie gross ist die Beschleunigung?'),
        wahl('Frage 2', 'Was gibt im v-t-Diagramm die Fläche unter der Geraden an?',
             ['die Geschwindigkeit', 'die Beschleunigung', 'den Weg'], 2,
             {0: 'Die Geschwindigkeit liest man an der Höhe ab. Was ergibt Höhe mal Breite?', 1: 'Die Beschleunigung ist die Steigung. Was ergibt Höhe mal Breite?'},
             sprich='Was gibt im v-t-Diagramm die Fläche unter der Geraden an?'),
        {'szene': 'Frage 3', 'bei': 0.3, 'typ': 'klick',
         'text': 'Ein Auto fährt mit 4 m/s und beschleunigt mit 2 m/s². Wie schnell ist es nach 5 s? Tipp den Punkt ins Bild oder gib ihn ein.',
         'sprich': 'Ein Auto fährt mit vier Metern pro Sekunde und beschleunigt mit zwei Metern pro Sekunde im Quadrat. Wie schnell ist es nach fünf Sekunden? Tipp den Punkt ins Bild oder gib ihn ein.',
         'ziel': [5, 14], 'toleranz': [0.4, 1.2], 'eingabe': ['t in s', 'v in m/s'], 'richtig_text': 'Getroffen.',
         'fallen': [{'bei': [5, 10], 'text': 'Das ist nur Beschleunigung mal Zeit. Die Anfangsgeschwindigkeit kommt dazu.'},
                    {'bei': [5, 6], 'text': 'Die Beschleunigung wird mit der Zeit multipliziert, nicht nur dazugezählt.'}],
         'falsch_text': 'Nicht ganz. Rechne Anfangsgeschwindigkeit plus Beschleunigung mal Zeit und such den Wert bei t = 5 s.',
         'falsch_sprich': 'Nicht ganz. Rechne Anfangsgeschwindigkeit plus Beschleunigung mal Zeit und such den Wert bei fünf Sekunden.'},
        wahl('Frage 4', 'Bei 50 km/h braucht ein Auto 20 m Bremsweg. Wie lang ist er bei 100 km/h, gleich stark gebremst?',
             ['40 m', '80 m', '20 m'], 1,
             {0: 'Doppelt so lang wäre es, wenn die Geschwindigkeit einfach vorkäme. Sie steht im Bremsweg im Quadrat.', 2: 'Mehr Tempo, gleicher Bremsweg? Schau, wie die Geschwindigkeit im Bremsweg vorkommt.'},
             sprich='Bei fünfzig Kilometern pro Stunde braucht ein Auto zwanzig Meter Bremsweg. Wie lang ist er bei hundert Kilometern pro Stunde, gleich stark gebremst?'),
        wahl('Frage 5', 'Ein Auto fährt vorwärts und bremst. Welches Vorzeichen hat die Beschleunigung, wenn die Fahrtrichtung positiv zählt?',
             ['negativ', 'positiv', 'null'], 0,
             {1: 'Positiv hiesse: schneller werden in Fahrtrichtung.', 2: 'Null hiesse: Die Geschwindigkeit bleibt gleich.'}),
    ]))

DREH.append(dict(KOPF, titel='Bewegung sehen: Kontrollfragen zu Fall und Wurf', dateiname='p4-1-lp-kontrolle-wurf',
    kurzbeschrieb='Fünf Fragen zu Fallgeschwindigkeit, Masse im freien Fall, waagrechtem Wurf vom Tisch und gleich weiten Wurfwinkeln.',
    schlagworte=['freier Fall', 'waagrechter Wurf', 'schiefer Wurf', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'g mal t: neun Komma acht eins mal zwei, neunzehn Komma sechs Meter pro Sekunde.',
           formel(r'\fc{v} = g \cdot t = 9.81\;\text{m/s}^2 \cdot 2\;\text{s} \approx \fc{19.6\;\text{m/s}}', g=50, ein=1.0)),
        sz('Frage 2', 'Ohne Luftwiderstand ist die Beschleunigung für alle Körper dieselbe, g. Beide kommen gleichzeitig an.',
           notiz('g gilt für alle Körper,|schwer oder leicht', y=320, ein=1.0, g=50)),
        sz('Frage 3', 'Senkrecht wie im freien Fall: die Wurzel aus zwei mal null Komma acht durch neun Komma acht eins, rund null Komma vier Sekunden.',
           formel(r't = \sqrt{\dfrac{2h}{g}} = \sqrt{\dfrac{2 \cdot 0.8\;\text{m}}{9.81\;\text{m/s}^2}} \approx 0.40\;\text{s}', g=46, ein=1.0)),
        sz('Frage 4', 'Waagrecht gleichförmig: drei Meter pro Sekunde mal null Komma vier Sekunden, rund ein Komma zwei Meter.',
           formel(r'x = \fc{v_0} \cdot t = \fc{3\;\text{m/s}} \cdot 0.40\;\text{s} \approx 1.2\;\text{m}', g=50, ein=1.0)),
        sz('Frage 5', 'Zwei Winkel, die zusammen neunzig Grad ergeben, tragen gleich weit: siebzig und zwanzig Grad.',
           formel(r'\sin(2 \cdot 70^\circ) = \sin 140^\circ = \sin 40^\circ = \sin(2 \cdot 20^\circ)', g=44, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Stein fällt 2 s frei. Wie schnell ist er dann?', ['9.81 m/s', '39.2 m/s', '19.6 m/s'], 2,
             {0: 'So viel kommt in einer Sekunde dazu. Er fällt aber zwei Sekunden.', 1: 'Hier steht die Zeit im Quadrat. Die Geschwindigkeit wächst gleichmässig mit der Zeit.'},
             sprich='Ein Stein fällt zwei Sekunden frei. Wie schnell ist er dann?'),
        wahl('Frage 2', 'Eine schwere und eine leichte Kugel fallen ohne Luftwiderstand aus gleicher Höhe. Welche ist zuerst unten?',
             ['beide gleichzeitig', 'die schwere', 'die leichte'], 0,
             {1: 'Hängt die Fallbeschleunigung g von der Masse ab?', 2: 'Hängt die Fallbeschleunigung g von der Masse ab?'}),
        wahl('Frage 3', 'Ein Ball rollt mit 3 m/s waagrecht über eine 0.8 m hohe Tischkante. Wie lange fällt er?',
             ['0.27 s', '0.40 s', '0.16 s'], 1,
             {0: 'Höhe durch Tempo? Die Fallzeit hängt nur von der Höhe ab.', 2: 'Die Wurzel fehlt: Die Fallzeit ist die Wurzel aus zwei h durch g.'},
             sprich='Ein Ball rollt mit drei Metern pro Sekunde waagrecht über eine null Komma acht Meter hohe Tischkante. Wie lange fällt er?'),
        wahl('Frage 4', 'Wie weit vom Tisch entfernt landet derselbe Ball?', ['1.2 m', '0.8 m', '3 m'], 0,
             {1: 'Das ist die Höhe des Tischs. Waagrecht rollt er gleichförmig weiter.', 2: 'So weit käme er in einer ganzen Sekunde. Er fliegt aber nur null Komma vier Sekunden.'}),
        wahl('Frage 5', 'Ein Ball wird vom Boden unter 70° geworfen. Welcher andere Winkel gibt beim gleichen Tempo dieselbe Weite?',
             ['45°', '110°', '20°'], 2,
             {0: 'Fünfundvierzig Grad gibt die grösste Weite, nicht dieselbe.', 1: 'Hundertzehn Grad hiesse, nach hinten zu werfen.'},
             sprich='Ein Ball wird vom Boden unter siebzig Grad geworfen. Welcher andere Winkel gibt beim gleichen Tempo dieselbe Weite?'),
    ]))

DREH.append(dict(KOPF, titel='Bewegung sehen: Kontrollfragen zur Vektoraddition', dateiname='p4-1-lp-kontrolle-vektor',
    kurzbeschrieb='Fünf Fragen zu Relativbewegung auf dem Schiff, Seitenwind, Querzeit, Versatz und Vorhalten.',
    schlagworte=['Relativbewegung', 'Vektoraddition', 'Querzeit', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Nach hinten zeigt sein Pfeil gegen den Pfeil des Schiffs: acht minus zwei, sechs Meter pro Sekunde.',
           formel(r'8\;\text{m/s} - 2\;\text{m/s} = 6\;\text{m/s}', ein=1.0)),
        sz('Frage 2', 'Die Pfeile stehen senkrecht: Pythagoras. Wurzel aus sechzig im Quadrat plus elf im Quadrat, einundsechzig Meter pro Sekunde.',
           formel(r'|\fd{\vec v}| = \sqrt{(60\;\text{m/s})^2 + (11\;\text{m/s})^2} = \fd{61\;\text{m/s}}', g=46, ein=1.0)),
        sz('Frage 3', 'Die Strömung zeigt flussabwärts, sie hat keinen Anteil quer über den Fluss. Die Querzeit bleibt gleich, nur der Versatz wächst.',
           notiz('Strömung: nur flussabwärts|Querzeit: unverändert', y=320, ein=1.0, g=50)),
        sz('Frage 4', 'Querzeit: dreissig durch zwei, fünfzehn Sekunden. Versatz: ein Meter pro Sekunde mal fünfzehn Sekunden, fünfzehn Meter.',
           formel(r't = \dfrac{30\;\text{m}}{\fc{2\;\text{m/s}}} = 15\;\text{s}', g=50, ein=1.0),
           formel(r'd = 1\;\text{m/s} \cdot 15\;\text{s} = 15\;\text{m}', y=440, g=50, ein=4.0)),
        sz('Frage 5', 'Sie hält schräg gegen die Strömung. Ihr Anteil flussaufwärts hebt die Strömung auf, der Rest bringt sie hinüber.',
           formel(r'\fc{v_S} \cdot \cos\beta = -v_F', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Auf einem Schiff (8 m/s) geht jemand mit 2 m/s nach hinten. Wie schnell ist er gegenüber dem Ufer?',
             ['10 m/s', '6 m/s', '2 m/s'], 1,
             {0: 'Nach hinten zeigt sein Pfeil gegen den Pfeil des Schiffs.', 2: 'Das ist seine Geschwindigkeit gegenüber dem Schiff.'},
             sprich='Auf einem Schiff, das mit acht Metern pro Sekunde fährt, geht jemand mit zwei Metern pro Sekunde nach hinten. Wie schnell ist er gegenüber dem Ufer?'),
        wahl('Frage 2', 'Ein Flugzeug fliegt mit 60 m/s nach Norden, der Wind weht mit 11 m/s nach Osten. Wie schnell ist es über Grund?',
             ['71 m/s', '49 m/s', '61 m/s'], 2,
             {0: 'Die Pfeile stehen senkrecht aufeinander. Darf man da einfach addieren?', 1: 'Der Wind bremst nicht, er weht quer. Die Pfeile stehen senkrecht.'},
             sprich='Ein Flugzeug fliegt mit sechzig Metern pro Sekunde nach Norden, der Wind weht mit elf Metern pro Sekunde nach Osten. Wie schnell ist es über Grund?'),
        wahl('Frage 3', 'Ein Boot fährt quer zum Ufer über den Fluss. Die Strömung wird stärker. Was geschieht mit der Querzeit?',
             ['sie wird länger', 'sie bleibt gleich', 'sie wird kürzer'], 1,
             {0: 'Hat die Strömung einen Anteil quer über den Fluss?', 2: 'Hat die Strömung einen Anteil quer über den Fluss?'}),
        wahl('Frage 4', 'Fluss 30 m breit, Boot quer mit 2 m/s, Strömung 1 m/s. Wie weit wird es versetzt?',
             ['15 m', '30 m', '60 m'], 0,
             {1: 'Das ist die Flussbreite. Wie lange dauert die Überquerung?', 2: 'Rechne zuerst die Querzeit: Breite durch Bootsgeschwindigkeit.'},
             sprich='Ein Fluss ist dreissig Meter breit, ein Boot fährt quer mit zwei Metern pro Sekunde, die Strömung hat einen Meter pro Sekunde. Wie weit wird es versetzt?'),
        wahl('Frage 5', 'Wie richtet sich eine Schwimmerin aus, um genau gegenüber anzukommen?',
             ['genau quer zum Ufer', 'mit der Strömung', 'schräg gegen die Strömung'], 2,
             {0: 'Dann treibt sie die Strömung ab. Was muss ihr Pfeil ausgleichen?', 1: 'Dann treibt sie noch weiter ab.'}),
    ]))

DREH.append(dict(KOPF, titel='Bewegung sehen: Kontrollfragen zur Kreisbewegung', dateiname='p4-1-lp-kontrolle-kreis',
    kurzbeschrieb='Fünf Fragen zu Rotationsfrequenz, Winkelgeschwindigkeit, Richtung der Beschleunigung, Zentripetalbeschleunigung und konstantem Tempo.',
    schlagworte=['Kreisbewegung', 'Rotationsfrequenz', 'Zentripetalbeschleunigung', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Tausendzweihundert Umdrehungen pro Minute sind tausendzweihundert durch sechzig, zwanzig pro Sekunde: zwanzig Hertz.',
           formel(r'f = \dfrac{1200}{60\;\text{s}} = 20\;\text{Hz}', ein=1.0)),
        sz('Frage 2', 'Zwei Pi durch die Umlaufzeit: zwei Pi durch zwei Sekunden, rund drei Komma eins vier Radiant pro Sekunde.',
           formel(r'\omega = \dfrac{2\pi}{T} = \dfrac{2\pi}{2\;\text{s}} \approx 3.14\;\text{rad/s}', ein=1.0)),
        sz('Frage 3', 'Der Geschwindigkeitspfeil dreht sich mit dem Körper. Seine Änderung zeigt zur Mitte, und dorthin zeigt die Beschleunigung.',
           notiz('Beschleunigung:|zur Kreismitte', y=320, ein=1.0, g=50),
           bild('p4-1-lp-kreis-k3.jpg', y=200, ein=1.0)),
        sz('Frage 4', 'v Quadrat durch r: zwei im Quadrat durch null Komma fünf, acht Meter pro Sekunde im Quadrat.',
           formel(r'\fd{a_z} = \dfrac{\fc{v}^2}{r} = \dfrac{(\fc{2\;\text{m/s}})^2}{0.5\;\text{m}} = \fd{8\;\text{m/s}^2}', g=48, ein=1.0)),
        sz('Frage 5', 'Gleichförmig heisst: gleiches Tempo. Die Richtung ändert sich aber ständig, darum ist die Geschwindigkeit als Pfeil nicht konstant.',
           notiz('Betrag: konstant|Richtung: ändert sich', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Waschtrommel macht 1200 Umdrehungen pro Minute. Wie gross ist die Rotationsfrequenz?',
             ['1200 Hz', '20 Hz', '0.05 Hz'], 1,
             {0: 'Pro Minute, nicht pro Sekunde.', 2: 'Das ist die Umlaufzeit in Sekunden. Gesucht ist ihr Kehrwert.'},
             sprich='Eine Waschtrommel macht tausendzweihundert Umdrehungen pro Minute. Wie gross ist die Rotationsfrequenz?'),
        wahl('Frage 2', 'Ein Umlauf dauert 2 s. Wie gross ist die Winkelgeschwindigkeit?', ['0.5 rad/s', '12.6 rad/s', '3.14 rad/s'], 2,
             {0: 'Das ist die Frequenz. Ein Umlauf sind zwei Pi.', 1: 'Zwei Pi mal T? Die Winkelgeschwindigkeit ist zwei Pi durch T.'},
             sprich='Ein Umlauf dauert zwei Sekunden. Wie gross ist die Winkelgeschwindigkeit?'),
        wahl('Frage 3', 'Wohin zeigt bei der gleichförmigen Kreisbewegung die Beschleunigung?',
             ['zur Kreismitte', 'in Bewegungsrichtung', 'nach aussen'], 0,
             {1: 'Das Tempo bleibt gleich. Was ändert sich am Geschwindigkeitspfeil?', 2: 'Schau, wohin sich der Geschwindigkeitspfeil dreht.'}),
        wahl('Frage 4', 'Ein Punkt kreist mit 2 m/s auf r = 0.5 m. Wie gross ist die Zentripetalbeschleunigung?',
             ['4 m/s²', '8 m/s²', '1 m/s²'], 1,
             {0: 'v durch r: Das Quadrat fehlt.', 2: 'v mal r? Die Zentripetalbeschleunigung ist v Quadrat durch r.'},
             sprich='Ein Punkt kreist mit zwei Metern pro Sekunde auf einem Radius von null Komma fünf Metern. Wie gross ist die Zentripetalbeschleunigung?'),
        wahl('Frage 5', 'Bleibt die Geschwindigkeit bei der gleichförmigen Kreisbewegung konstant?',
             ['ja, ganz', 'nur ihr Betrag, nicht ihre Richtung', 'nein, ihr Betrag ändert sich'], 1,
             {0: 'Zeigt der Pfeil immer in dieselbe Richtung?', 2: 'Gleichförmig heisst: gleiches Tempo.'}),
    ]))

NUR = [a for a in sys.argv[1:] if not a.startswith('--')]   # nur diese Drehbücher schreiben
for d in DREH:
    pfad = os.path.join(CLIPS, d['dateiname'] + '.json')
    if NUR and d['dateiname'] not in NUR:
        continue
    if os.path.exists(pfad) and not NEU:
        print('  bleibt  ', d['dateiname'])
        continue
    with open(pfad, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('  geschrieben', d['dateiname'], len(d['szenen']), 'Szenen', len(d.get('fragen', [])), 'Fragen')
