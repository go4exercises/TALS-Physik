"""Erzeugt die zwölf Drehbücher des Leitprogramms Hydrostatik (clips/p4-5-lp-*.json).

  python3 scripts/lp/hydrostatik/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/hydrostatik/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/hydrostatik/clips.py --neu p4-5-lp-kontrolle-pascal …   # nur diese

Archiv-Werkzeug wie scripts/lp/statik/clips.py: Nach der Vertonung sind die JSONs in clips/
die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf mit
--neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).

Farben: Die Formeln bleiben ungefärbt; die Farben der Kräfte (Gewicht Bernstein, Auftrieb Grün,
Kolbenkräfte Blau) zeigen die Bilder. Bilder: Aufnahmen der Simulationen (clips/bilder/p4-5-lp-*.jpg). Zahlen im Sprechertext ausgeschrieben
(CLAUDE.md). Kontrollclips: neue Beispiele (nicht Clip, Leiste, Aufgaben oder Mini-Checks der
Themenseite), richtige Antwort an wechselnden Stellen, Lösung erst nach der Antwort.
"""
import json
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv

KOPF = {
    'themenbereich': 'Mechanik · BM', 'lerngebiet': '4 · Mechanik',
    'lektion': ['p4-5'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-05', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Hydrostatik sehen', 'nachlauf': 2.6, 'probe': True,
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
EIN = 'Einführungsclip des Leitprogramms Hydrostatik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Hydrostatik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
B = dict(breite=640, y=180)   # Simulationsbilder sind hoch: schmaler setzen, damit sie auf der Bühne bleiben

# ================================================================== Kapitel 1
DREH.append(dict(KOPF, titel='Hydrostatik sehen: Kraft auf Fläche', dateiname='p4-5-lp-druck',
    kurzbeschrieb='Druck als Kraft je Fläche, das Pascal und seine Vielfachen, der Druck zwischen Schuh und Schnee und warum Schneeschuhe tragen.',
    schlagworte=['Druck', 'Pascal', 'bar', 'Auflagefläche', 'Schneeschuh'], _probe=EIN % 1,
    szenen=[
        sz('Einsinken', 'Im tiefen Schnee sinkt man mit gewöhnlichen Schuhen ein, mit Schneeschuhen kaum — obwohl man gleich schwer ist. Es kommt darauf an, wie sich die Kraft auf die Fläche verteilt.',
           titel('Warum sinkt man ein?', g=72),
           notiz('gleiche Kraft,|andere Fläche', y=440, ein=6.0)),
        sz('Druck', 'Der Druck ist die Kraft, die senkrecht auf eine Fläche wirkt, geteilt durch die Fläche. Die Einheit ist das Pascal: ein Newton pro Quadratmeter.',
           formel(r'p = \frac{F}{A}', y=280, g=60, ein=1.5),
           formel(r'1\;\text{Pa} = 1\;\text{N/m}^2', y=430, g=48, ein=6.5)),
        sz('Schuhe', 'Eine Person mit fünfundfünfzig Kilogramm drückt mit rund fünfhundertvierzig Newton. Ihre Schuhe haben zusammen zweihundertfünfzig Quadratzentimeter, also null Komma null zwei fünf Quadratmeter. Der Druck ist rund einundzwanzigtausendsechshundert Pascal.',
           formel(r'F = m \cdot g = 55\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 540\;\text{N}', y=280, g=40, ein=0.5),
           formel(r'p = \frac{540\;\text{N}}{0.025\;\text{m}^2} \approx 21\,600\;\text{Pa}', y=420, g=44, ein=8.0),
           bild('p4-5-lp-druck-1.jpg', **B)),
        sz('Schneeschuhe', 'Mit Schneeschuhen von fünfzehnhundert Quadratzentimetern verteilt sich dieselbe Kraft auf die sechsfache Fläche. Der Druck sinkt auf ein Sechstel, rund dreitausendsechshundert Pascal, und man sinkt viel weniger ein.',
           formel(r'p = \frac{540\;\text{N}}{0.15\;\text{m}^2} \approx 3600\;\text{Pa}', y=300, g=44, ein=3.0),
           bild('p4-5-lp-druck-2.jpg', **B)),
        sz('Einheiten', 'Weil das Pascal klein ist, nimmt man oft Vielfache: das Hektopascal, hundert Pascal, das Kilopascal, tausend Pascal, und das Bar, hunderttausend Pascal. Der Luftdruck beträgt rund tausenddreizehn Hektopascal, also etwa ein Bar.',
           formel(r'1\;\text{hPa} = 100\;\text{Pa} \qquad 1\;\text{kPa} = 1000\;\text{Pa}', y=280, g=42, ein=3.0),
           formel(r'1\;\text{bar} = 100\,000\;\text{Pa} = 1000\;\text{hPa}', y=410, g=42, ein=8.0)),
        sz('Merke', 'Zum Mitnehmen: Druck ist Kraft durch Fläche. Kleine Fläche, grosser Druck — wie bei der Messerschneide. Grosse Fläche, kleiner Druck — wie beim Schneeschuh.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'p = \frac{F}{A} \qquad 1\;\text{bar} = 10^5\;\text{Pa}', y=420, g=46, ein=0.4),
           notiz('Fläche in m² einsetzen', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 2
DREH.append(dict(KOPF, titel='Hydrostatik sehen: Druck in der Tiefe', dateiname='p4-5-lp-schweredruck',
    kurzbeschrieb='Der Schweredruck als Gewicht der Wassersäule, die hydrostatische Grundgleichung, der Gesamtdruck mit dem Luftdruck, die Faustregel ein Bar je zehn Meter und das hydrostatische Paradoxon.',
    schlagworte=['Schweredruck', 'hydrostatische Grundgleichung', 'Gesamtdruck', 'Tauchen', 'hydrostatisches Paradoxon'], _probe=EIN % 2,
    szenen=[
        sz('Säule', 'Über einer Taucherin steht eine Wassersäule. Ihr Gewicht drückt auf die Fläche darunter. Gewicht durch Fläche: Die Fläche kürzt sich, es bleiben Dichte, g und Tiefe.',
           formel(r'p_S = \frac{F_G}{A} = \frac{\rho \cdot A \cdot h \cdot g}{A}', y=280, g=44, ein=4.0),
           formel(r'p_S = \rho \cdot g \cdot h', y=420, g=54, ein=10.0)),
        sz('Becken', 'Im fünf Meter tiefen Sprungbecken ist der Schweredruck tausend mal neun Komma acht eins mal fünf, rund neunundvierzigtausend Pascal, knapp ein halbes Bar.',
           formel(r'p_S = 1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2 \cdot 5\;\text{m}', y=280, g=40, ein=1.0),
           formel(r'= 49\,050\;\text{Pa} \approx 0.49\;\text{bar}', y=400, g=44, ein=7.0)),
        sz('Gesamtdruck', 'Auf die Wasseroberfläche drückt zusätzlich die Luft. Der Gesamtdruck ist Luftdruck plus Schweredruck: rund eins Komma fünf null Bar. Je zehn Meter Wasser kommt etwa ein Bar dazu.',
           formel(r'p = p_0 + p_S \approx 1.013\;\text{bar} + 0.491\;\text{bar} \approx 1.50\;\text{bar}', y=280, g=38, ein=2.0),
           notiz('je 10 m Wasser:|rund 1 bar mehr', y=440, ein=9.0),
           bild('p4-5-lp-schweredruck-1.jpg', **B)),
        sz('Paradoxon', 'In der Formel kommt nur die Tiefe vor, nicht die Form des Gefässes. Ein schmales Rohr und ein breites Becken haben bei gleicher Füllhöhe denselben Druck am Boden. Das heisst hydrostatisches Paradoxon. Und der Druck wirkt an jeder Stelle nach allen Seiten gleich.',
           titel('Hydrostatisches Paradoxon', y=260, g=60),
           notiz('gleiche Höhe:|gleicher Bodendruck', y=440, ein=6.0)),
        sz('Merke', 'Zum Mitnehmen: Der Schweredruck wächst linear mit der Tiefe und mit der Dichte. Dazu kommt der Luftdruck.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'p_S = \rho \cdot g \cdot h \qquad p = p_0 + p_S', y=420, g=46, ein=0.4),
           notiz('h in Meter', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 3
DREH.append(dict(KOPF, titel='Hydrostatik sehen: die Luft drückt mit', dateiname='p4-5-lp-luftdruck',
    kurzbeschrieb='Der Luftdruck als Schweredruck der Luft, wie er eine Flüssigkeit im Strohhalm und im Saugrohr hochdrückt, die Grenze von rund zehn Metern und das Quecksilberbarometer.',
    schlagworte=['Luftdruck', 'Strohhalm', 'Saugpumpe', 'Barometer', 'Unterdruck'], _probe=EIN % 3,
    szenen=[
        sz('Luft', 'Auch Luft hat ein Gewicht. Über uns liegt eine kilometerhohe Luftschicht. Ihr Schweredruck ist der Luftdruck, auf Meereshöhe rund tausenddreizehn Hektopascal. In den Bergen liegt weniger Luft darüber, der Luftdruck ist kleiner.',
           titel('Der Luftdruck', y=260, g=72),
           formel(r'p_0 \approx 1013\;\text{hPa}', y=430, g=50, ein=10.0)),
        sz('Strohhalm', 'Wer am Strohhalm saugt, senkt den Druck im Mund. Draussen drückt die Luft weiter auf das Getränk und schiebt es hoch, bis der Schweredruck der Säule den Unterschied ausgleicht. Hundert Hektopascal Unterdruck heben Wasser rund einen Meter.',
           formel(r'\rho \cdot g \cdot h = p_0 - p_i', y=280, g=50, ein=8.0),
           formel(r'h = \frac{10\,000\;\text{Pa}}{1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2} \approx 1.02\;\text{m}', y=420, g=38, ein=14.0),
           bild('p4-5-lp-luftdruck-1.jpg', **B)),
        sz('Grenze', 'Mehr als den ganzen Luftdruck kann die Luft nicht aufbringen. Selbst mit Vakuum im Rohr steigt Wasser auf Meereshöhe nur rund zehn Meter hoch. Darum kann keine Saugpumpe Wasser höher ansaugen.',
           formel(r'p_i = 0:\quad h = \frac{p_0}{\rho \cdot g} \approx 10\;\text{m}', y=300, g=46, ein=4.0),
           bild('p4-5-lp-luftdruck-2.jpg', **B)),
        sz('Barometer', 'Quecksilber ist dreizehn Komma sechs mal dichter als Wasser. Eine Quecksilbersäule ist darum dreizehn Komma sechs mal kürzer — handlich genug für ein Barometer. Die Höhe der Säule zeigt den Luftdruck an.',
           titel('Quecksilberbarometer', y=260, g=62),
           notiz('Säulenhöhe zeigt|den Luftdruck', y=440, ein=8.0)),
        sz('Merke', 'Zum Mitnehmen: Nicht die Pumpe zieht, die Luft drückt. Eine Flüssigkeitssäule steigt, bis ihr Schweredruck den Druckunterschied ausgleicht.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\rho \cdot g \cdot h = p_0 - p_i', y=420, g=48, ein=0.4),
           formel(r'\text{höchstens: } p_i = 0', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 4
DREH.append(dict(KOPF, titel='Hydrostatik sehen: Druck pflanzt sich fort', dateiname='p4-5-lp-pascal',
    kurzbeschrieb="Das Pascal'sche Gesetz, die hydraulische Presse mit gleichem Druck auf beiden Kolben, die Kraftverstärkung über das Flächenverhältnis und der Tausch von Kraft gegen Weg.",
    schlagworte=["Pascal'sches Gesetz", 'hydraulische Presse', 'Hebebühne', 'Druck', 'Kolben'], _probe=EIN % 4,
    szenen=[
        sz('Fortpflanzen', 'Drückt man auf eine eingeschlossene Flüssigkeit, breitet sich der Druck unverändert in der ganzen Flüssigkeit aus, in alle Richtungen. Das ist das Pascal\'sche Gesetz.',
           titel("Pascal'sches Gesetz", y=260, g=66),
           notiz('derselbe Druck|überall', y=440, ein=6.0)),
        sz('Kleiner Kolben', 'Am kleinen Kolben mit zehn Quadratzentimetern drückt eine Kraft von zweihundert Newton. Das gibt einen Druck von zweihunderttausend Pascal, zwei Bar, überall in der Flüssigkeit.',
           formel(r'p = \frac{F_1}{A_1} = \frac{200\;\text{N}}{0.001\;\text{m}^2} = 200\,000\;\text{Pa}', y=300, g=40, ein=4.0),
           bild('p4-5-lp-pascal-1.jpg', **B)),
        sz('Grosser Kolben', 'Am grossen Kolben mit fünfhundert Quadratzentimetern wirkt derselbe Druck, auf die fünfzigfache Fläche. Er drückt mit zehntausend Newton: genug, um ein Auto von tausend Kilogramm zu heben.',
           formel(r'F_2 = F_1 \cdot \frac{A_2}{A_1} = 200\;\text{N} \cdot \frac{500}{10} = 10\,000\;\text{N}', y=300, g=40, ein=3.0),
           bild('p4-5-lp-pascal-2.jpg', **B)),
        sz('Weg', 'Umsonst ist das nicht. Das Öl, das der kleine Kolben verdrängt, verteilt sich auf die grosse Fläche. Fünfundzwanzig Zentimeter am kleinen Kolben heben den grossen nur einen halben Zentimeter. Kraft mal Weg ist auf beiden Seiten gleich.',
           formel(r'A_1 \cdot s_1 = A_2 \cdot s_2', y=280, g=52, ein=4.0),
           formel(r's_2 = 25\;\text{cm} \cdot \frac{10}{500} = 0.5\;\text{cm}', y=420, g=44, ein=10.0)),
        sz('Merke', 'Zum Mitnehmen: In der Presse ist der Druck überall gleich. Die grosse Fläche bekommt die grosse Kraft, und dafür bewegt sie sich wenig. So arbeiten Hebebühne, Bremse und Bagger.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\frac{F_1}{A_1} = \frac{F_2}{A_2}', y=420, g=50, ein=0.4),
           notiz('Kraft gegen Weg', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 5
DREH.append(dict(KOPF, titel='Hydrostatik sehen: leichter im Wasser', dateiname='p4-5-lp-auftrieb',
    kurzbeschrieb='Ein Körper an der Federwaage wird im Wasser leichter: der Auftrieb aus dem Druckunterschied, das archimedische Prinzip und warum der Auftrieb nur vom verdrängten Volumen und der Dichte der Flüssigkeit abhängt.',
    schlagworte=['Auftrieb', 'archimedisches Prinzip', 'Federwaage', 'verdrängtes Volumen'], _probe=EIN % 5,
    szenen=[
        sz('Waage', 'Ein Messingzylinder mit zweihundert Kubikzentimetern hängt an einer Federwaage. An der Luft zeigt sie rund sechzehn Komma sieben Newton.',
           formel(r'F_G = \rho_K \cdot V \cdot g \approx 16.7\;\text{N}', y=300, g=48, ein=3.0),
           bild('p4-5-lp-auftrieb-1.jpg', **B)),
        sz('Eintauchen', 'Taucht man ihn ganz ins Wasser, zeigt die Waage nur noch rund vierzehn Komma sieben Newton. Das Wasser drückt mit knapp zwei Newton nach oben: der Auftrieb.',
           formel(r'F_A = 16.7\;\text{N} - 14.7\;\text{N} \approx 2.0\;\text{N}', y=300, g=46, ein=4.0),
           bild('p4-5-lp-auftrieb-2.jpg', **B)),
        sz('Druckunterschied', 'Woher kommt der Auftrieb? Unten am Körper ist das Wasser tiefer als oben, der Druck dort grösser. Von unten drückt das Wasser stärker nach oben als von oben nach unten. Der Unterschied ist der Auftrieb.',
           titel('Druck unten > Druck oben', y=260, g=56),
           notiz('Unterschied:|Auftrieb nach oben', y=440, ein=8.0)),
        sz('Archimedes', 'Archimedes fand: Der Auftrieb ist so gross wie das Gewicht der verdrängten Flüssigkeit. Zweihundert Kubikzentimeter Wasser wiegen eins Komma neun sechs Newton — genau der Auftrieb. Das gilt in jeder Flüssigkeit und auch in Luft.',
           formel(r'F_A = \rho_{Fl} \cdot V_e \cdot g', y=280, g=54, ein=4.0),
           formel(r'= 1000\;\text{kg/m}^3 \cdot 0.0002\;\text{m}^3 \cdot 9.81\;\text{m/s}^2 \approx 1.96\;\text{N}', y=420, g=36, ein=8.0)),
        sz('Merke', 'Zum Mitnehmen: Der Auftrieb hängt nur am eingetauchten Volumen und an der Dichte der Flüssigkeit, nicht am Material des Körpers.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_A = \rho_{Fl} \cdot V_e \cdot g', y=420, g=48, ein=0.4),
           formel(r'\text{Anzeige} = F_G - F_A', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 6
DREH.append(dict(KOPF, titel='Hydrostatik sehen: schwimmen oder sinken', dateiname='p4-5-lp-schwimmen',
    kurzbeschrieb='Gewichtskraft und Auftrieb entscheiden: Schwimmen, Schweben oder Sinken je nach Dichte, der eingetauchte Anteil eines schwimmenden Körpers und die mittlere Dichte von Hohlkörpern.',
    schlagworte=['Schwimmen', 'Schweben', 'Sinken', 'Dichte', 'mittlere Dichte'], _probe=EIN % 6,
    szenen=[
        sz('Vergleich', 'Ganz untergetaucht wirken zwei Kräfte: die Gewichtskraft nach unten, der Auftrieb nach oben. Beide haben dasselbe Volumen. Es entscheidet also der Vergleich der Dichten von Körper und Flüssigkeit.',
           formel(r'F_G = \rho_K \cdot V \cdot g \qquad F_A = \rho_{Fl} \cdot V \cdot g', y=300, g=40, ein=3.0),
           formel(r'\rho_K < \rho_{Fl}:\ \text{schwimmt} \quad \rho_K = \rho_{Fl}:\ \text{schwebt} \quad \rho_K > \rho_{Fl}:\ \text{sinkt}', y=440, g=34, ein=10.0)),
        sz('Schwimmen', 'Ein Holzwürfel mit sechshundert Kilogramm pro Kubikmeter steigt auf und taucht nur so weit ein, bis der Auftrieb seine Gewichtskraft trägt: sechzig Prozent seines Volumens.',
           formel(r'\frac{V_e}{V} = \frac{\rho_K}{\rho_{Fl}} = \frac{600}{1000} = 0.6', y=300, g=46, ein=6.0),
           bild('p4-5-lp-schwimmen-1.jpg', **B)),
        sz('Sinken', 'Ein Aluminiumwürfel ist dichter als Wasser. Der Auftrieb ist kleiner als seine Gewichtskraft, er sinkt auf den Boden.',
           notiz('2700 kg/m³ > 1000 kg/m³:|sinkt', y=320, ein=2.0, g=46),
           bild('p4-5-lp-schwimmen-2.jpg', **B)),
        sz('Schiff', 'Ein Schiff aus Stahl schwimmt trotzdem. Es zählt die mittlere Dichte aus Stahl und der Luft im Rumpf, und die ist kleiner als die des Wassers.',
           titel('Mittlere Dichte', y=260, g=70),
           notiz('Stahl + Luft im Rumpf|< Dichte des Wassers', y=440, ein=6.0)),
        sz('Merke', 'Zum Mitnehmen: Schwimmen, Schweben oder Sinken entscheidet der Vergleich der Dichten. Ein schwimmender Körper taucht zum Anteil Dichte Körper durch Dichte Flüssigkeit ein.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\frac{V_e}{V} = \frac{\rho_K}{\rho_{Fl}}', y=420, g=50, ein=0.4)),
        JETZT,
    ]))

# ================================================================== Kontrollclips
DREH.append(dict(KOPF, titel='Hydrostatik sehen: Kontrollfragen zum Druck', dateiname='p4-5-lp-kontrolle-druck',
    kurzbeschrieb='Fünf Fragen zum Druck aus Kraft und Fläche, zu Einheiten, zum grössten Druck und zur Verdoppelung.',
    schlagworte=['Druck', 'Einheiten', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Kraft durch Fläche: dreihundert Newton durch null Komma null eins zwei Quadratmeter, fünfundzwanzigtausend Pascal.',
           formel(r'p = \frac{300\;\text{N}}{0.012\;\text{m}^2} = 25\,000\;\text{Pa}', ein=1.0)),
        sz('Frage 2', 'Ein Bar sind tausend Hektopascal. Null Komma fünf Bar sind fünfhundert Hektopascal.',
           formel(r'0.5\;\text{bar} = 500\;\text{hPa}', ein=1.0)),
        sz('Frage 3', 'Die Nadelspitze hat die winzigste Fläche. Schon eine kleine Kraft gibt dort einen riesigen Druck.',
           notiz('kleinste Fläche:|grösster Druck', y=320, ein=1.0, g=50)),
        sz('Frage 4', 'Doppelte Kraft verdoppelt den Druck, halbe Fläche verdoppelt ihn noch einmal: viermal so gross.',
           formel(r'p = \frac{2 \cdot F}{\tfrac12 \cdot A} = 4 \cdot \frac{F}{A}', ein=1.0)),
        sz('Frage 5', 'Ein Pascal ist ein Newton pro Quadratmeter.',
           formel(r'1\;\text{Pa} = 1\;\text{N/m}^2', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Kiste drückt mit 300 N auf eine Fläche von 0.012 m². Wie gross ist der Druck?',
             ['3.6 Pa', '25 000 Pa', '250 Pa'], 1,
             {0: 'Mal gerechnet? Druck ist Kraft durch Fläche.', 2: 'Durch 0.012 teilen: Wird das Ergebnis grösser oder kleiner als 300?'},
             sprich='Eine Kiste drückt mit dreihundert Newton auf eine Fläche von null Komma null eins zwei Quadratmetern. Wie gross ist der Druck?',
             rueck_sprich={0: 'Mal gerechnet? Druck ist Kraft durch Fläche.', 2: 'Durch null Komma null eins zwei teilen: Wird das Ergebnis grösser oder kleiner als dreihundert?'}),
        wahl('Frage 2', 'Wie viele Hektopascal sind 0.5 bar?',
             ['50 hPa', '5000 hPa', '500 hPa'], 2,
             {0: 'Ein Bar sind tausend Hektopascal.', 1: 'Ein Bar sind tausend Hektopascal.'},
             sprich='Wie viele Hektopascal sind null Komma fünf Bar?'),
        wahl('Frage 3', 'Wo entsteht bei gleicher Kraft der grösste Druck?',
             ['an einer Nadelspitze', 'unter einem Schneeschuh', 'unter einem Fussball'], 0,
             {1: 'Grosse Fläche — grosser oder kleiner Druck?', 2: 'Welche Fläche ist am kleinsten?'}),
        wahl('Frage 4', 'Die Kraft wird verdoppelt und die Fläche halbiert. Was geschieht mit dem Druck?',
             ['er bleibt gleich', 'er wird viermal so gross', 'er verdoppelt sich'], 1,
             {0: 'Beide Änderungen wirken in dieselbe Richtung.', 2: 'Nicht nur die Kraft ändert sich — die Fläche auch.'}),
        wahl('Frage 5', 'Welcher Einheit entspricht ein Pascal?',
             ['N/m²', 'N · m²', 'kg/m³'], 0,
             {1: 'Druck ist Kraft <em>durch</em> Fläche.', 2: 'Das ist die Einheit der Dichte.'},
             sprich='Welcher Einheit entspricht ein Pascal?',
             rueck_sprich={1: 'Druck ist Kraft durch Fläche.', 2: 'Das ist die Einheit der Dichte.'}),
    ]))

DREH.append(dict(KOPF, titel='Hydrostatik sehen: Kontrollfragen zum Schweredruck', dateiname='p4-5-lp-kontrolle-schweredruck',
    kurzbeschrieb='Fünf Fragen zum Schweredruck in Wasser und Öl, zur Richtung des Drucks, zum Gesamtdruck und zur Tiefe aus dem Druck.',
    schlagworte=['Schweredruck', 'Gesamtdruck', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Dichte mal g mal Tiefe: tausend mal neun Komma acht eins mal drei, rund neunundzwanzig Komma vier Kilopascal.',
           formel(r'p_S = 1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2 \cdot 3\;\text{m} \approx 29.4\;\text{kPa}', g=40, ein=1.0)),
        sz('Frage 2', 'Der Druck wirkt an jeder Stelle nach allen Seiten gleich stark.',
           notiz('nach allen Seiten|gleich', y=320, ein=1.0, g=50)),
        sz('Frage 3', 'Dichte des Öls mal g mal Tiefe: achthundertfünfzig mal neun Komma acht eins mal drei Komma fünf, rund neunundzwanzig Komma zwei Kilopascal.',
           formel(r'p_S = 850\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2 \cdot 3.5\;\text{m} \approx 29.2\;\text{kPa}', g=40, ein=1.0)),
        sz('Frage 4', 'Vierzig Meter Wasser geben rund drei Komma neun Bar, dazu kommt der Luftdruck: rund vier Komma neun Bar.',
           formel(r'p = 1.013\;\text{bar} + 3.92\;\text{bar} \approx 4.9\;\text{bar}', g=44, ein=1.0)),
        sz('Frage 5', 'Umgestellt: Druck durch Dichte mal g. Hundertzwanzigtausend Pascal durch tausendfünfundzwanzig mal neun Komma acht eins, rund elf Komma neun Meter.',
           formel(r'h = \frac{120\,000\;\text{Pa}}{1025\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2} \approx 11.9\;\text{m}', g=42, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Wie gross ist der Schweredruck in 3 m Wassertiefe?',
             ['3 kPa', '29.4 kPa', '130.7 kPa'], 1,
             {0: 'Wo ist g geblieben?', 2: 'Gefragt ist nur der Schweredruck, ohne Luftdruck.'},
             sprich='Wie gross ist der Schweredruck in drei Metern Wassertiefe?'),
        wahl('Frage 2', 'Eine Taucherin hält eine kleine Platte in 4 m Tiefe einmal waagrecht, einmal senkrecht. Wo drückt das Wasser stärker?',
             ['waagrecht', 'senkrecht', 'gleich stark'], 2,
             {0: 'Wirkt der Druck nur von oben?', 1: 'Wirkt der Druck nur von der Seite?'},
             sprich='Eine Taucherin hält eine kleine Platte in vier Metern Tiefe einmal waagrecht, einmal senkrecht. Wo drückt das Wasser stärker?'),
        wahl('Frage 3', 'Ein Heizöltank ist 3.5 m hoch gefüllt (Heizöl: 850 kg/m³). Wie gross ist der Schweredruck am Boden?',
             ['29.2 kPa', '34.3 kPa', '2.98 kPa'], 0,
             {1: 'Mit welcher Dichte hast du gerechnet?', 2: 'Wo ist g geblieben?'},
             sprich='Ein Heizöltank ist drei Komma fünf Meter hoch gefüllt, Heizöl hat achthundertfünfzig Kilogramm pro Kubikmeter. Wie gross ist der Schweredruck am Boden?'),
        wahl('Frage 4', 'Wie gross ist der Gesamtdruck in 40 m Wassertiefe (Luftdruck 1013 hPa)?',
             ['3.9 bar', '40 bar', '4.9 bar'], 2,
             {0: 'Das ist nur der Schweredruck. Was drückt noch auf die Oberfläche?', 1: 'Je zehn Meter kommt etwa ein Bar dazu, nicht zehn.'},
             sprich='Wie gross ist der Gesamtdruck in vierzig Metern Wassertiefe, bei einem Luftdruck von tausenddreizehn Hektopascal?'),
        wahl('Frage 5', 'In welcher Tiefe beträgt der Schweredruck in Meerwasser (1025 kg/m³) 120 kPa?',
             ['rund 11.9 m', 'rund 0.012 m', 'rund 119 m'], 0,
             {1: 'Kilopascal in Pascal umrechnen: mal 1000.', 2: 'Je zehn Meter rund 100 kPa — passt das?'},
             sprich='In welcher Tiefe beträgt der Schweredruck in Meerwasser hundertzwanzig Kilopascal? Meerwasser hat tausendfünfundzwanzig Kilogramm pro Kubikmeter.',
             rueck_sprich={1: 'Kilopascal in Pascal umrechnen: mal tausend.', 2: 'Je zehn Meter rund hundert Kilopascal. Passt das?'}),
    ]))

DREH.append(dict(KOPF, titel='Hydrostatik sehen: Kontrollfragen zum Luftdruck', dateiname='p4-5-lp-kontrolle-luftdruck',
    kurzbeschrieb='Fünf Fragen dazu, wer die Flüssigkeit hochdrückt, zum Luftdruck in den Bergen, zum Strohhalm, zum Quecksilber und zum steigenden Barometer.',
    schlagworte=['Luftdruck', 'Saugpumpe', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'Der Mund senkt nur den Druck im Halm. Hochgedrückt wird das Getränk vom Luftdruck draussen.',
           notiz('Die Luft drückt,|der Mund zieht nicht', y=320, ein=1.0, g=50)),
        sz('Frage 2', 'Auf dem Berg liegt weniger Luft darüber. Der Luftdruck ist kleiner.',
           notiz('höher: weniger Luft|darüber, kleinerer Druck', y=320, ein=1.0, g=48)),
        sz('Frage 3', 'Fünfzig Hektopascal sind fünftausend Pascal. Durch tausend mal neun Komma acht eins: rund einundfünfzig Zentimeter.',
           formel(r'h = \frac{5000\;\text{Pa}}{1000\;\text{kg/m}^3 \cdot 9.81\;\text{m/s}^2} \approx 0.51\;\text{m}', g=42, ein=1.0)),
        sz('Frage 4', 'Quecksilber ist viel dichter. Für denselben Druck genügt eine viel kürzere Säule.',
           formel(r'h = \frac{p_0}{\rho \cdot g}', ein=1.0)),
        sz('Frage 5', 'Die Luft drückt die Säule hoch, bis ihr Schweredruck den Luftdruck ausgleicht. Steigt die Säule, ist der Luftdruck gestiegen.',
           notiz('Säule steigt:|Luftdruck steigt', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Du trinkst mit einem Strohhalm. Was drückt das Getränk nach oben?',
             ['der Luftdruck auf die Oberfläche im Glas', 'der Sog deines Mundes', 'das Getränk selbst'], 0,
             {1: 'Kann ein Unterdruck ziehen — oder fehlt nur Druck von oben?', 2: 'Woher sollte das Getränk die Kraft nehmen?'}),
        wahl('Frage 2', 'Wie ist der Luftdruck auf einem hohen Berg verglichen mit Meereshöhe?',
             ['grösser', 'kleiner', 'gleich'], 1,
             {0: 'Liegt auf dem Berg mehr oder weniger Luft über dir?', 2: 'Ist die Luftsäule über dir gleich hoch?'}),
        wahl('Frage 3', 'Du senkst den Druck im Strohhalm um 50 hPa. Wie hoch steigt Wasser höchstens?',
             ['rund 0.51 cm', 'rund 51 cm', 'rund 5.1 m'], 1,
             {0: 'Hektopascal in Pascal: mal hundert.', 2: 'Rechne nach: 5000 Pa durch 9810 Pa je Meter.'},
             sprich='Du senkst den Druck im Strohhalm um fünfzig Hektopascal. Wie hoch steigt Wasser höchstens?',
             rueck_sprich={0: 'Hektopascal in Pascal: mal hundert.', 2: 'Rechne nach: fünftausend Pascal durch neuntausendachthundertzehn Pascal je Meter.'}),
        wahl('Frage 4', 'Ein Barometer wird mit Quecksilber statt mit Wasser gebaut. Wie hoch ist die Säule?',
             ['viel kürzer', 'gleich hoch', 'viel höher'], 0,
             {1: 'Die Dichte steht im Nenner von h = p₀ / (ρ · g).', 2: 'Quecksilber ist dichter. Braucht es eine höhere Säule für denselben Druck?'},
             rueck_sprich={1: 'Die Dichte steht im Nenner von h gleich p null durch rho mal g.', 2: 'Quecksilber ist dichter. Braucht es eine höhere Säule für denselben Druck?'}),
        wahl('Frage 5', 'Die Quecksilbersäule eines Barometers steigt im Lauf des Tages. Was bedeutet das?',
             ['der Luftdruck sinkt', 'der Luftdruck steigt', 'nichts, die Höhe hängt nur vom Rohr ab'], 1,
             {0: 'Wer drückt die Säule hoch?', 2: 'Was gleicht der Schweredruck der Säule aus?'}),
    ]))

DREH.append(dict(KOPF, titel="Hydrostatik sehen: Kontrollfragen zum Pascal'schen Gesetz", dateiname='p4-5-lp-kontrolle-pascal',
    kurzbeschrieb="Fünf Fragen zur Ausbreitung des Drucks, zur Kraft am grossen und am kleinen Kolben, zum Kolbenweg und zum Druck aus Kraft und Fläche.",
    schlagworte=["Pascal'sches Gesetz", 'Presse', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Der Druck breitet sich in der eingeschlossenen Flüssigkeit nach allen Seiten gleich aus. Das Wasser spritzt aus allen Löchern gleich stark.',
           notiz('Druck nach allen|Seiten gleich', y=320, ein=1.0, g=50)),
        sz('Frage 2', 'Die fünfundzwanzigfache Fläche gibt die fünfundzwanzigfache Kraft: tausendfünfhundert Newton.',
           formel(r'F_2 = 60\;\text{N} \cdot 25 = 1500\;\text{N}', ein=1.0)),
        sz('Frage 3', 'Das verdrängte Volumen ist gleich. Auf der zwanzigfachen Fläche bewegt sich der Kolben zwanzigmal weniger: zwei Zentimeter.',
           formel(r's_2 = \frac{40\;\text{cm}}{20} = 2\;\text{cm}', ein=1.0)),
        sz('Frage 4', 'Gleicher Druck auf beiden Seiten: viertausend Newton mal fünf durch zweihundertfünfzig, achtzig Newton.',
           formel(r'F_1 = F_2 \cdot \frac{A_1}{A_2} = 4000\;\text{N} \cdot \frac{5\;\text{cm}^2}{250\;\text{cm}^2} = 80\;\text{N}', g=40, ein=1.0)),
        sz('Frage 5', 'Fünfzig Newton durch zwei Quadratzentimeter, also null Komma null null null zwei Quadratmeter: zweihundertfünfzigtausend Pascal, zwei Komma fünf Bar.',
           formel(r'p = \frac{50\;\text{N}}{0.0002\;\text{m}^2} = 250\,000\;\text{Pa} = 2.5\;\text{bar}', g=42, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Kugel mit vielen gleich grossen Löchern ist mit Wasser gefüllt. Du drückst den Kolben hinein. Wie spritzt das Wasser?',
             ['aus allen Löchern gleich stark', 'vor allem aus den Löchern gegenüber dem Kolben', 'nur aus den Löchern unten'], 0,
             {1: 'Breitet sich der Druck nur in Stossrichtung aus?', 2: 'Ist der Druck nur unten erhöht?'}),
        wahl('Frage 2', 'Am kleinen Kolben drücken 60 N. Der grosse Kolben hat die 25-fache Fläche. Welche Kraft entsteht dort?',
             ['2.4 N', '1500 N', '85 N'], 1,
             {0: 'Umgekehrt: Die grosse Fläche bekommt die grosse Kraft.', 2: 'Addiert? Die Kraft wächst im Verhältnis der Flächen.'},
             sprich='Am kleinen Kolben drücken sechzig Newton. Der grosse Kolben hat die fünfundzwanzigfache Fläche. Welche Kraft entsteht dort?'),
        wahl('Frage 3', 'Der kleine Kolben wird 40 cm hineingedrückt, der grosse hat die 20-fache Fläche. Um wie viel hebt er sich?',
             ['800 cm', '20 cm', '2 cm'], 2,
             {0: 'Der grosse Kolben bewegt sich weniger, nicht mehr.', 1: 'Subtrahiert? Das Volumen verteilt sich auf die zwanzigfache Fläche.'},
             sprich='Der kleine Kolben wird vierzig Zentimeter hineingedrückt, der grosse hat die zwanzigfache Fläche. Um wie viel hebt er sich?'),
        wahl('Frage 4', 'Ein Auto drückt mit 4000 N auf den grossen Kolben (250 cm²). Der kleine Kolben hat 5 cm². Welche Kraft braucht es dort?',
             ['80 N', '200 000 N', '16 N'], 0,
             {1: 'Am kleinen Kolben braucht es die kleine Kraft.', 2: 'Druck mal Fläche: Mit welcher Fläche hast du multipliziert?'},
             sprich='Ein Auto drückt mit viertausend Newton auf den grossen Kolben mit zweihundertfünfzig Quadratzentimetern. Der kleine Kolben hat fünf Quadratzentimeter. Welche Kraft braucht es dort?'),
        wahl('Frage 5', 'Du drückst mit 50 N auf einen Kolben mit 2 cm². Wie gross ist der Druck in der Flüssigkeit?',
             ['25 bar', '0.25 bar', '2.5 bar'], 2,
             {0: 'Quadratzentimeter in Quadratmeter: 2 cm² = 0.0002 m².', 1: 'Nachrechnen: 50 N durch 0.0002 m².'},
             sprich='Du drückst mit fünfzig Newton auf einen Kolben mit zwei Quadratzentimetern. Wie gross ist der Druck in der Flüssigkeit?',
             rueck_sprich={0: 'Quadratzentimeter in Quadratmeter: zwei Quadratzentimeter sind null Komma null null null zwei Quadratmeter.', 1: 'Nachrechnen: fünfzig Newton durch null Komma null null null zwei Quadratmeter.'}),
    ]))

DREH.append(dict(KOPF, titel='Hydrostatik sehen: Kontrollfragen zum Auftrieb', dateiname='p4-5-lp-kontrolle-auftrieb',
    kurzbeschrieb='Fünf Fragen zur Auftriebskraft in Wasser und Spiritus, zum Druck an Ober- und Unterseite, zur Anzeige der Federwaage und zum Salzwasser.',
    schlagworte=['Auftrieb', 'archimedisches Prinzip', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Ein halber Liter Wasser wiegt rund vier Komma neun Newton. So gross ist der Auftrieb.',
           formel(r'F_A = 1000\;\text{kg/m}^3 \cdot 0.0005\;\text{m}^3 \cdot 9.81\;\text{m/s}^2 \approx 4.9\;\text{N}', g=36, ein=1.0)),
        sz('Frage 2', 'Verdrängt wird Spiritus: siebenhundertneunzig mal null Komma null null null drei mal neun Komma acht eins, rund zwei Komma drei zwei Newton.',
           formel(r'F_A = 790\;\text{kg/m}^3 \cdot 0.0003\;\text{m}^3 \cdot 9.81\;\text{m/s}^2 \approx 2.32\;\text{N}', g=36, ein=1.0)),
        sz('Frage 3', 'Die Unterseite liegt tiefer, dort ist der Druck grösser. Dieser Unterschied ergibt den Auftrieb.',
           notiz('unten tiefer:|grösserer Druck', y=320, ein=1.0, g=50)),
        sz('Frage 4', 'Die Waage zeigt Gewichtskraft minus Auftrieb: zwölf minus drei, neun Newton.',
           formel(r'12\;\text{N} - 3\;\text{N} = 9\;\text{N}', ein=1.0)),
        sz('Frage 5', 'Salzwasser ist dichter. Dasselbe verdrängte Volumen wiegt mehr, der Auftrieb ist grösser.',
           formel(r'F_A = \rho_{Fl} \cdot V_e \cdot g', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Körper mit 0.5 l Volumen liegt ganz unter Wasser. Wie gross ist der Auftrieb?',
             ['0.5 N', '4.9 N', '4905 N'], 1,
             {0: 'Das ist die verdrängte Masse in kg. Die Kraft: mal g.', 2: 'Liter in m³ umrechnen: 0.5 l = 0.0005 m³.'},
             sprich='Ein Körper mit null Komma fünf Litern Volumen liegt ganz unter Wasser. Wie gross ist der Auftrieb?',
             rueck_sprich={0: 'Das ist die verdrängte Masse in Kilogramm. Die Kraft: mal g.', 2: 'Liter in Kubikmeter umrechnen: null Komma fünf Liter sind null Komma null null null fünf Kubikmeter.'}),
        wahl('Frage 2', 'Ein Körper mit 300 cm³ liegt ganz in Spiritus (790 kg/m³). Wie gross ist der Auftrieb?',
             ['2.32 N', '2.94 N', '2325 N'], 0,
             {1: 'Welche Flüssigkeit wird verdrängt?', 2: 'Kubikzentimeter in Kubikmeter: 300 cm³ = 0.0003 m³.'},
             sprich='Ein Körper mit dreihundert Kubikzentimetern liegt ganz in Spiritus, siebenhundertneunzig Kilogramm pro Kubikmeter. Wie gross ist der Auftrieb?',
             rueck_sprich={1: 'Welche Flüssigkeit wird verdrängt?', 2: 'Kubikzentimeter in Kubikmeter: dreihundert Kubikzentimeter sind null Komma null null null drei Kubikmeter.'}),
        wahl('Frage 3', 'Ein Würfel hängt ganz unter Wasser. Wo drückt das Wasser am stärksten auf ihn?',
             ['auf die Oberseite', 'auf die Unterseite', 'überall gleich stark'], 1,
             {0: 'Wo ist das Wasser tiefer?', 2: 'Ist der Druck in jeder Tiefe gleich?'}),
        wahl('Frage 4', 'Eine Federwaage zeigt an der Luft 12 N. Ganz eingetaucht beträgt der Auftrieb 3 N. Was zeigt sie dann?',
             ['15 N', '9 N', '3 N'], 1,
             {0: 'Der Auftrieb zeigt nach oben: Er entlastet die Waage.', 2: 'Das ist nur der Auftrieb.'},
             sprich='Eine Federwaage zeigt an der Luft zwölf Newton. Ganz eingetaucht beträgt der Auftrieb drei Newton. Was zeigt sie dann?'),
        wahl('Frage 5', 'Derselbe Körper wird einmal in Süsswasser, einmal in Salzwasser ganz eingetaucht. Wo ist der Auftrieb grösser?',
             ['im Salzwasser', 'im Süsswasser', 'gleich'], 0,
             {1: 'Welche Flüssigkeit ist dichter?', 2: 'Gleiches Volumen — aber gleich schweres Wasser?'}),
    ]))

DREH.append(dict(KOPF, titel='Hydrostatik sehen: Kontrollfragen zum Schwimmen', dateiname='p4-5-lp-kontrolle-schwimmen',
    kurzbeschrieb='Fünf Fragen zu Sinken und Schwimmen, zum eingetauchten Anteil, zur Dichte aus dem Anteil, zum Aufsteigen und zu zwei Holzarten.',
    schlagworte=['Schwimmen', 'Schweben', 'Sinken', 'Kontrollfragen'], _probe=KTRL % 6,
    szenen=[
        sz('Frage 1', 'Zwölfhundert ist mehr als tausend. Der Körper ist dichter als Wasser und sinkt.',
           notiz('1200 > 1000: sinkt', y=320, ein=1.0, g=50)),
        sz('Frage 2', 'Der eingetauchte Anteil ist Dichte Körper durch Dichte Wasser: siebenhundertfünfzig durch tausend, fünfundsiebzig Prozent.',
           formel(r'\frac{V_e}{V} = \frac{750}{1000} = 75\,\%', ein=1.0)),
        sz('Frage 3', 'Der eingetauchte Anteil ist Dichte Körper durch Dichte Wasser. Dreissig Prozent von tausend: dreihundert Kilogramm pro Kubikmeter.',
           formel(r'\rho_K = 0.3 \cdot 1000\;\text{kg/m}^3 = 300\;\text{kg/m}^3', ein=1.0)),
        sz('Frage 4', 'Ganz untergetaucht ist der Auftrieb grösser als die Gewichtskraft. Der Ball steigt, bis er nur noch zum Teil eintaucht.',
           formel(r'F_A > F_G', ein=1.0)),
        sz('Frage 5', 'Der leichtere Würfel taucht zu fünfzig Prozent ein, der schwerere zu neunzig. Der aus fünfhundert ragt weiter heraus.',
           notiz('500: 50 % unter Wasser|900: 90 % unter Wasser', y=320, ein=1.0, g=48)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Körper hat die Dichte 1200 kg/m³. Was geschieht in Wasser?',
             ['er schwimmt', 'er sinkt', 'er schwebt'], 1,
             {0: 'Vergleiche seine Dichte mit der von Wasser.', 2: 'Schweben heisst: genau gleiche Dichte.'},
             sprich='Ein Körper hat die Dichte zwölfhundert Kilogramm pro Kubikmeter. Was geschieht in Wasser?'),
        wahl('Frage 2', 'Ein Holzbalken (750 kg/m³) schwimmt in Wasser. Welcher Anteil liegt unter der Oberfläche?',
             ['25 %', '75 %', '133 %'], 1,
             {0: 'Das ist der Teil über Wasser.', 2: 'Umgekehrt: Dichte Körper durch Dichte Flüssigkeit, immer kleiner als 1.'},
             sprich='Ein Holzbalken mit siebenhundertfünfzig Kilogramm pro Kubikmeter schwimmt in Wasser. Welcher Anteil liegt unter der Oberfläche?',
             rueck_sprich={0: 'Das ist der Teil über Wasser.', 2: 'Umgekehrt: Dichte Körper durch Dichte Flüssigkeit, immer kleiner als eins.'}),
        wahl('Frage 3', 'Ein Brett schwimmt in Wasser und taucht zu 30 % ein. Welche Dichte hat es?',
             ['300 kg/m³', '700 kg/m³', '3333 kg/m³'], 0,
             {1: 'Das passt zum Teil über Wasser.', 2: 'Umgekehrt gerechnet? Ein schwimmender Körper ist weniger dicht als Wasser.'},
             sprich='Ein Brett schwimmt in Wasser und taucht zu dreissig Prozent ein. Welche Dichte hat es?'),
        wahl('Frage 4', 'Ein Ball (150 kg/m³) wird ganz unter Wasser gedrückt und losgelassen. Warum steigt er?',
             ['der Auftrieb ist grösser als die Gewichtskraft', 'Luft zieht ihn nach oben', 'der Druck unten ist kleiner'], 0,
             {1: 'Welche Kräfte wirken unter Wasser auf ihn?', 2: 'Ist der Druck unten kleiner oder grösser als oben?'},
             sprich='Ein Ball mit hundertfünfzig Kilogramm pro Kubikmeter wird ganz unter Wasser gedrückt und losgelassen. Warum steigt er?'),
        wahl('Frage 5', 'Zwei gleich grosse Holzwürfel, 500 kg/m³ und 900 kg/m³, schwimmen in Wasser. Welcher ragt weiter heraus?',
             ['der aus 900 kg/m³', 'beide gleich', 'der aus 500 kg/m³'], 2,
             {0: 'Welcher taucht zu einem grösseren Anteil ein?', 1: 'Der eingetauchte Anteil hängt von der Dichte ab.'},
             sprich='Zwei gleich grosse Holzwürfel, fünfhundert und neunhundert Kilogramm pro Kubikmeter, schwimmen in Wasser. Welcher ragt weiter heraus?'),
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
