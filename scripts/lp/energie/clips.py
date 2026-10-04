"""Erzeugt die zwölf Drehbücher des Leitprogramms Energie (clips/p4-3-lp-*.json).

  python3 scripts/lp/energie/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/energie/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/energie/clips.py --neu p4-3-lp-kontrolle-erde …   # nur diese

Archiv-Werkzeug wie scripts/lp/dynamik/clips.py: Nach der Vertonung sind die JSONs in clips/
die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf mit
--neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).

Farben wie in den Simulationen, soweit das Clip-Theme sie kennt: \\fa Lageenergie (Bernstein),
\\fc Bewegungsenergie und v (Grün), \\fd Wärme und Abstrahlung (Rot). Blau (Kräfte, zugeführte
Energie) und Violett kennt das Theme nicht — diese Grössen bleiben ungefärbt. Bilder: Aufnahmen
der Simulationen (clips/bilder/p4-3-lp-*.jpg). Zahlen im Sprechertext ausgeschrieben
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
    'lektion': ['p4-3'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-04', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Energie sehen', 'nachlauf': 2.6, 'probe': True,
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
EIN = 'Einführungsclip des Leitprogramms Energie, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Energie, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'

# ================================================================== Kapitel 1
DREH.append(dict(KOPF, titel='Energie sehen: Arbeit ist Kraft mal Weg', dateiname='p4-3-lp-arbeit',
    kurzbeschrieb='Energie als Fähigkeit, Arbeit zu verrichten, die wichtigsten Energieformen, Arbeit als Kraft mal Weg, der Winkel zwischen Kraft und Weg und die Hubarbeit.',
    schlagworte=['Energie', 'Energieformen', 'Arbeit', 'Hubarbeit', 'Joule'], _probe=EIN % 1,
    szenen=[
        sz('Energie', 'Energie ist die Fähigkeit, Arbeit zu verrichten. Sie steckt in vielen Formen: als Lageenergie in einem gehobenen Körper, als Bewegungsenergie, als Wärme, chemisch im Essen und im Benzin, elektrisch, als Strahlung im Sonnenlicht. Energie wird umgewandelt, aber nie erzeugt oder vernichtet.',
           titel('Was ist Energie?', g=76),
           notiz('Lage, Bewegung, Wärme,|chemisch, elektrisch,|Strahlung, Spannung, Kern', y=440, ein=4.0)),
        sz('Arbeit', 'Arbeit verrichtet eine Kraft, die einen Körper längs eines Weges verschiebt. Zieht man eine Kiste waagrecht mit zweihundert Newton fünf Meter weit, ist die Arbeit Kraft mal Weg: tausend Joule. Im Kraft-Weg-Diagramm ist das die Fläche unter der Kraft.',
           formel(r'W = F \cdot s = 200\;\text{N} \cdot 5\;\text{m} = 1000\;\text{J}', g=50, ein=6.0),
           notiz('Arbeit:|Fläche unter der Kraft', ein=12.0),
           bild('p4-3-lp-arbeit-1.jpg')),
        sz('Winkel', 'Zieht das Seil schräg nach oben, unter sechzig Grad, zählt nur der Anteil der Kraft in Wegrichtung: F mal Kosinus Alpha, hier hundert Newton. Die Arbeit halbiert sich auf fünfhundert Joule.',
           formel(r'W = F \cdot s \cdot \cos\alpha', g=54, ein=4.0),
           formel(r'= 200\;\text{N} \cdot 5\;\text{m} \cdot \cos 60^\circ = 500\;\text{J}', y=430, g=46, ein=8.0),
           bild('p4-3-lp-arbeit-2.jpg')),
        sz('Senkrecht', 'Steht die Kraft senkrecht zum Weg, zählt gar nichts: Der Kosinus von neunzig Grad ist null. Wer eine Tasche waagrecht trägt, verrichtet an ihr keine Arbeit, auch wenn die Arme müde werden.',
           formel(r'\cos 90^\circ = 0 \;\Rightarrow\; W = 0', g=54, ein=1.0),
           notiz('Kraft senkrecht zum Weg:|keine Arbeit', y=440, ein=5.0)),
        sz('Hubarbeit', 'Wer einen Körper hebt, zieht mit seiner Gewichtskraft nach oben, über die Höhe h. Die Hubarbeit ist m mal g mal h. Zehn Kilogramm einen Meter hoch: rund achtundneunzig Joule.',
           titel('Hubarbeit', y=260, g=76),
           formel(r'W = m \cdot g \cdot h = 10\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 1\;\text{m} \approx 98.1\;\text{J}', y=430, g=42, ein=5.0)),
        sz('Merke', 'Zum Mitnehmen: Energie ist die Fähigkeit, Arbeit zu verrichten, gemessen in Joule. Arbeit ist Kraft mal Weg, aber nur der Anteil der Kraft in Wegrichtung zählt.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'W = F \cdot s \cdot \cos\alpha \qquad 1\;\text{J} = 1\;\text{N} \cdot \text{m}', y=420, g=46, ein=0.4),
           notiz('senkrecht zum Weg: W = 0|Heben: W = m · g · h', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 2
DREH.append(dict(KOPF, titel='Energie sehen: Lage- und Bewegungsenergie', dateiname='p4-3-lp-bremsen',
    kurzbeschrieb='Lageenergie m · g · h mit frei wählbarem Nullniveau, Bewegungsenergie ½ · m · v² als Parabel und der Bremsweg aus F_B · s = E_kin.',
    schlagworte=['Lageenergie', 'Bewegungsenergie', 'kinetische Energie', 'potentielle Energie', 'Bremsweg'], _probe=EIN % 2,
    szenen=[
        sz('Lageenergie', 'Hebt man einen Körper, speichert er die Hubarbeit als Lageenergie: m mal g mal h. Gezählt wird die Höhe über einem Nullniveau, das man frei wählen darf. Drei Kilogramm auf zwei Metern Höhe haben rund achtundfünfzig Komma neun Joule.',
           titel('Lageenergie', y=260, g=76),
           formel(r'\fa{E_\text{pot}} = m \cdot g \cdot h = 3\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 2\;\text{m} \approx \fa{58.9\;\text{J}}', y=430, g=40, ein=9.0)),
        sz('Bewegungsenergie', 'Ein bewegter Körper trägt Bewegungsenergie: ein halb mal m mal v Quadrat. Ein Auto mit tausend Kilogramm und zehn Metern pro Sekunde hat fünfzigtausend Joule. Über dem Tempo aufgetragen wird daraus eine Parabel.',
           formel(r'\fc{E_\text{kin}} = \tfrac12 \cdot m \cdot v^2 = \tfrac12 \cdot 1000\;\text{kg} \cdot (10\;\text{m/s})^2 = \fc{50\;\text{kJ}}', g=36, ein=4.0),
           graf([], [-1.5, 27.5], [-25, 420], [5, 10, 15, 20, 25], [100, 200, 300, 400], 'v [m/s]', 'E [kJ]',
                punkte=[{'x': 10, 'y': 50, 'farbe': 3, 'beschriftung': '50 kJ', 'beschriftung_bei': [10.6, 62]}],
                kurven=[{'formel': '0.5*x**2', 'farbe': 3, 'von': 0, 'bis': 27}])),
        sz('Bremsen', 'Beim Bremsen nimmt die Bremskraft dem Auto diese Energie wieder ab: Bremskraft mal Bremsweg gleich Bewegungsenergie. Mit fünftausend Newton steht das Auto nach zehn Metern.',
           formel(r'F_B \cdot s = \fc{E_\text{kin}}', g=54, ein=4.0),
           formel(r's = \dfrac{50\,000\;\text{J}}{5000\;\text{N}} = 10\;\text{m}', y=440, g=48, ein=8.0),
           bild('p4-3-lp-bremsen-1.jpg')),
        sz('Doppelt', 'Bei doppeltem Tempo, zwanzig Metern pro Sekunde, ist die Energie viermal so gross: zweihunderttausend Joule. Mit derselben Bremskraft braucht das Auto den vierfachen Weg, vierzig Meter.',
           formel(r'\fc{E_\text{kin}} = \tfrac12 \cdot 1000\;\text{kg} \cdot (20\;\text{m/s})^2 = \fc{200\;\text{kJ}}', g=40, ein=4.0),
           notiz('doppeltes Tempo:|vierfache Energie,|vierfacher Bremsweg', y=460, ein=8.0),
           bild('p4-3-lp-bremsen-2.jpg')),
        sz('Merke', 'Zum Mitnehmen: Lageenergie wächst linear mit der Höhe, Bewegungsenergie quadratisch mit dem Tempo. Beim Bremsen wird die ganze Bewegungsenergie zu Wärme.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fa{E_\text{pot}} = m \cdot g \cdot h \qquad \fc{E_\text{kin}} = \tfrac12 \cdot m \cdot v^2', y=420, g=46, ein=0.4),
           notiz('Nullniveau frei wählbar|Bremsen: F_B · s = E_kin', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 3
DREH.append(dict(KOPF, titel='Energie sehen: die Summe bleibt', dateiname='p4-3-lp-erhaltung',
    kurzbeschrieb='Achterbahn ohne Reibung: Lage- und Bewegungsenergie wandeln sich um, die Summe bleibt; Tempo im Tal und auf einem Hügel, Umkehr, wenn die Energie nicht reicht.',
    schlagworte=['Energieerhaltung', 'mechanische Energie', 'Achterbahn', 'Lageenergie', 'Bewegungsenergie'], _probe=EIN % 3,
    szenen=[
        sz('Achterbahn', 'Ein Wagen startet aus der Ruhe auf zwanzig Metern Höhe. Ohne Reibung bleibt die Summe aus Lage- und Bewegungsenergie gleich, sie wechselt nur die Form. Oben ist alles Lageenergie.',
           formel(r'm \cdot g \cdot h_0 + \tfrac12 \cdot m \cdot v_0^2 = m \cdot g \cdot h + \tfrac12 \cdot m \cdot v^2', g=34, ein=5.0),
           bild('p4-3-lp-erhaltung-1.jpg')),
        sz('Tal', 'Im Tal ist alles Bewegungsenergie geworden. Die Masse kürzt sich: v gleich Wurzel aus zwei g h, hier neunzehn Komma acht Meter pro Sekunde, für jeden Wagen, ob leicht oder schwer.',
           formel(r'\fc{v} = \sqrt{2 \cdot g \cdot h_0} = \sqrt{2 \cdot 9.81\;\text{m/s}^2 \cdot 20\;\text{m}} \approx \fc{19.8\;\text{m/s}}', g=40, ein=4.0),
           notiz('die Masse kürzt sich', ein=8.0),
           bild('p4-3-lp-erhaltung-2.jpg')),
        sz('Hügel', 'Auf dem zweiten Hügel, zwölf Meter hoch, ist ein Teil wieder Lageenergie. Für die Bewegung bleiben die acht Meter Höhenunterschied: zwölf Komma fünf Meter pro Sekunde.',
           formel(r'\fc{v} = \sqrt{2 \cdot g \cdot (h_0 - h_2)} = \sqrt{2 \cdot 9.81\;\text{m/s}^2 \cdot 8\;\text{m}} \approx \fc{12.5\;\text{m/s}}', g=38, ein=4.0),
           bild('p4-3-lp-erhaltung-3.jpg')),
        sz('Umkehr', 'Ist der zweite Hügel höher als der Start, reicht die Energie nicht. Der Wagen kommt genau bis auf die Starthöhe, dann ist alles wieder Lageenergie, und er rollt zurück.',
           notiz('Energie reicht bis|zur Starthöhe,|dann kehrt er um', y=320, ein=5.0, g=48),
           bild('p4-3-lp-erhaltung-4.jpg')),
        sz('Merke', 'Zum Mitnehmen: Ohne Reibung bleibt die Summe aus Lage- und Bewegungsenergie gleich. Die Masse kürzt sich, und es zählen nur die Höhen, nicht die Form der Bahn.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fa{E_\text{pot}} + \fc{E_\text{kin}} = \text{konstant} \qquad \fc{v} = \sqrt{2 \cdot g \cdot h}', y=420, g=44, ein=0.4),
           notiz('Masse kürzt sich|nur die Höhen zählen', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 4
DREH.append(dict(KOPF, titel='Energie sehen: wohin die Energie geht', dateiname='p4-3-lp-reibung',
    kurzbeschrieb='Wagen auf der Rampe: ohne Reibung wird Lage- zu Bewegungsenergie, mit Reibung zum Teil zu Wärme; bergauf liefert ein Motor die Energie. Der Energieerhaltungssatz mit Reibung und Motor.',
    schlagworte=['Energieerhaltungssatz', 'Reibung', 'Wärme', 'Motor', 'Energiebilanz'], _probe=EIN % 4,
    szenen=[
        sz('Ohne Reibung', 'Ein Wagen mit achtzig Kilogramm rollt eine vierzig Meter lange Rampe hinunter, zehn Meter Höhenunterschied. Ohne Reibung wird die ganze Lageenergie, siebentausendachthundertachtundvierzig Joule, zu Bewegungsenergie.',
           formel(r'\fa{m \cdot g \cdot h} = 80\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 10\;\text{m} = \fa{7848\;\text{J}}', g=40, ein=8.0),
           bild('p4-3-lp-reibung-1.jpg')),
        sz('Mit Reibung', 'Mit hundert Newton Reibung werden auf den vierzig Metern viertausend Joule zu Wärme. Für die Bewegung bleiben dreitausendachthundertachtundvierzig Joule. Die Summe stimmt: Beide Säulen sind gleich hoch.',
           formel(r'\fc{E_\text{kin}} = m \cdot g \cdot h - \fd{F_R \cdot s}', g=50, ein=4.0),
           formel(r'= 7848\;\text{J} - \fd{4000\;\text{J}} = \fc{3848\;\text{J}}', y=430, g=46, ein=8.0),
           bild('p4-3-lp-reibung-2.jpg')),
        sz('Motor', 'Fährt der Wagen bergauf, muss ein Motor die Energie liefern: die Lageenergie, die der Wagen gewinnt, und die Wärme durch die Reibung. Was dann noch übrig ist, wird Bewegungsenergie.',
           formel(r'W_M = \fa{m \cdot g \cdot h} + \fd{F_R \cdot s} + \fc{E_\text{kin}}', g=46, ein=4.0),
           bild('p4-3-lp-reibung-3.jpg')),
        sz('Merke', 'Zum Mitnehmen: Energie geht nie verloren, sie wechselt nur die Form. Die Wärme durch Reibung ist für die Bewegung verloren, aber sie ist noch da. Das ist der Energieerhaltungssatz.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'E_\text{vorher} + W_M = E_\text{nachher} + \fd{F_R \cdot s}', y=420, g=46, ein=0.4),
           notiz('Reibung: Wärme|Motor: zugeführte Arbeit|Summe bleibt', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 5
DREH.append(dict(KOPF, titel='Energie sehen: wie schnell und wie gut', dateiname='p4-3-lp-leistung',
    kurzbeschrieb='Leistung als Arbeit pro Zeit am Kran, halbe Zeit gibt doppelte Leistung, Wirkungsgrad als Nutzen durch Aufwand und Energieeffizienz.',
    schlagworte=['Leistung', 'Watt', 'Wirkungsgrad', 'Energieeffizienz', 'Kran'], _probe=EIN % 5,
    szenen=[
        sz('Leistung', 'Ein Kran hebt zweihundert Kilogramm zehn Meter hoch. Die Arbeit ist rund neunzehntausendsechshundert Joule, egal wie schnell. Braucht er dafür zwanzig Sekunden, ist die Leistung neunhunderteinundachtzig Watt.',
           formel(r'P = \dfrac{W}{t} = \dfrac{m \cdot g \cdot h}{t} = \dfrac{200\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 10\;\text{m}}{20\;\text{s}} = 981\;\text{W}', g=34, ein=8.0),
           bild('p4-3-lp-leistung-1.jpg', breite=700)),
        sz('Schneller', 'Hebt er dieselbe Last in der halben Zeit, braucht er die doppelte Leistung: neunzehnhundertzweiundsechzig Watt. Die Arbeit bleibt gleich.',
           formel(r'P = \dfrac{19\,620\;\text{J}}{10\;\text{s}} = 1962\;\text{W}', g=50, ein=4.0),
           notiz('halbe Zeit:|doppelte Leistung,|gleiche Arbeit', y=460, ein=6.0)),
        sz('Wirkungsgrad', 'Der Motor muss mehr hineinstecken, als oben ankommt: Ein Teil wird Wärme. Der Wirkungsgrad eta ist Nutzen durch Aufwand. Bei null Komma acht braucht der Kran zwölfhundertsechsundzwanzig Watt.',
           formel(r'\eta = \dfrac{P_\text{nutz}}{P_\text{zu}}', g=54, ein=5.0),
           formel(r'P_\text{zu} = \dfrac{981\;\text{W}}{0.8} \approx 1226\;\text{W}', y=440, g=48, ein=9.0),
           bild('p4-3-lp-leistung-2.jpg', breite=700)),
        sz('Effizienz', 'Energieeffizienz heisst: dieselbe Nutzung mit möglichst wenig zugeführter Energie. Ein Elektroauto setzt rund neunzig Prozent der Energie aus der Batterie in Bewegung um, ein Benzinmotor nur rund ein Drittel.',
           titel('Energieeffizienz', y=260, g=76),
           notiz('Elektromotor: η ≈ 0.9|Benzinmotor: η ≈ 0.3', y=440, ein=6.0)),
        sz('Merke', 'Zum Mitnehmen: Leistung ist Arbeit pro Zeit, gemessen in Watt. Der Wirkungsgrad ist Nutzen durch Aufwand und immer kleiner als eins.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'P = \dfrac{W}{t} \qquad \eta = \dfrac{E_\text{nutz}}{E_\text{zu}}', y=420, g=48, ein=0.4),
           notiz('1 W = 1 J/s|kWh ist eine Energie', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 6
DREH.append(dict(KOPF, titel='Energie sehen: die Bilanz der Erde', dateiname='p4-3-lp-erde',
    kurzbeschrieb='Sonneneinstrahlung, Albedo und Abstrahlung ins All; das Gleichgewicht, der natürliche Treibhauseffekt und die Gründe der Erderwärmung.',
    schlagworte=['Energiebilanz', 'Albedo', 'Treibhauseffekt', 'Erderwärmung', 'Strahlung'], _probe=EIN % 6,
    szenen=[
        sz('Hinein', 'Die Sonne liefert ausserhalb der Atmosphäre dreizehnhunderteinundsechzig Watt pro Quadratmeter. Die Erde fängt sie mit ihrer Querschnittsfläche auf, verteilt sie aber über die ganze Kugel: Im Mittel kommt ein Viertel an, rund dreihundertvierzig Watt pro Quadratmeter.',
           formel(r'\dfrac{S}{4} = \dfrac{1361\;\text{W/m}^2}{4} \approx 340\;\text{W/m}^2', g=48, ein=12.0),
           bild('p4-3-lp-erde-1.jpg', breite=720)),
        sz('Albedo', 'Rund dreissig Prozent davon werfen Wolken, Eis und Luft gleich wieder zurück, die Albedo. Aufgenommen werden rund zweihundertachtunddreissig Watt pro Quadratmeter.',
           formel(r'(1 - a) \cdot \dfrac{S}{4} = 0.7 \cdot 340\;\text{W/m}^2 \approx 238\;\text{W/m}^2', g=44, ein=6.0),
           bild('p4-3-lp-erde-1.jpg', breite=720)),
        sz('Hinaus', 'Die Erde strahlt Wärme ins Weltall ab, umso mehr, je wärmer sie ist. Im Gleichgewicht geht genau so viel hinaus, wie hereinkommt. Ohne Treibhausgase stellte sich das bei minus achtzehn Grad ein, mit ihnen bei plus fünfzehn Grad.',
           notiz('Gleichgewicht:|hinaus = herein', y=300, ein=6.0, g=50),
           notiz('ohne Treibhausgase: −18 °C|mit: +15 °C', y=480, ein=11.0, g=44),
           bild('p4-3-lp-erde-2.jpg', breite=720)),
        sz('Erwärmung', 'Mehr Treibhausgas lässt weniger Wärmestrahlung ins All. Zuerst kommt mehr herein als hinaus, und die Erde erwärmt sich, bis die Abstrahlung wieder passt. Schmilzt Eis, sinkt die Albedo, und die Erde nimmt noch mehr auf.',
           notiz('mehr CO₂: weniger hinaus|weniger Eis: mehr herein|→ wärmer, bis es passt', y=320, ein=4.0, g=46),
           bild('p4-3-lp-erde-3.jpg', breite=720)),
        sz('Merke', 'Zum Mitnehmen: Im Gleichgewicht strahlt die Erde so viel ab, wie sie aufnimmt. Treibhausgase und Albedo verschieben dieses Gleichgewicht zu einer anderen Temperatur.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'(1 - a) \cdot \dfrac{S}{4} = \text{Abstrahlung ins All}', y=420, g=46, ein=0.4),
           notiz('mehr Treibhausgas: wärmer|kleinere Albedo: wärmer', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kontrollclips
DREH.append(dict(KOPF, titel='Energie sehen: Kontrollfragen zu Energie und Arbeit', dateiname='p4-3-lp-kontrolle-arbeit',
    kurzbeschrieb='Fünf Fragen zur Arbeit mit und ohne Winkel, zur Haltekraft, zur Solarzelle und zur Hubarbeit.',
    schlagworte=['Arbeit', 'Energieformen', 'Hubarbeit', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Kraft mal Weg: fünfzig Newton mal acht Meter, vierhundert Joule.',
           formel(r'W = F \cdot s = 50\;\text{N} \cdot 8\;\text{m} = 400\;\text{J}', ein=1.0)),
        sz('Frage 2', 'Nur der Anteil in Wegrichtung zählt: hundert Newton mal zehn Meter mal Kosinus sechzig Grad, fünfhundert Joule.',
           formel(r'W = 100\;\text{N} \cdot 10\;\text{m} \cdot \cos 60^\circ = 500\;\text{J}', g=48, ein=1.0)),
        sz('Frage 3', 'Die Haltekraft zeigt nach oben, der Weg waagrecht. Sie stehen senkrecht: keine Arbeit am Tablett.',
           formel(r'W = F \cdot s \cdot \cos 90^\circ = 0', ein=1.0)),
        sz('Frage 4', 'Die Solarzelle nimmt Strahlung auf und gibt elektrische Energie ab, dazu etwas Wärme.',
           notiz('Strahlung → elektrisch|(+ Wärme)', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Masse mal g mal Höhe: acht mal neun Komma acht eins mal eins Komma fünf, rund hundertachtzehn Joule.',
           formel(r'W = m \cdot g \cdot h = 8\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 1.5\;\text{m} \approx 118\;\text{J}', g=44, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Kraft von 50 N schiebt einen Wagen 8 m weit, genau in Bewegungsrichtung. Wie gross ist die Arbeit?',
             ['400 J', '6.25 J', '58 J'], 0,
             {1: 'Geteilt? Arbeit ist Kraft mal Weg.', 2: 'Addiert? Arbeit ist Kraft mal Weg.'},
             sprich='Eine Kraft von fünfzig Newton schiebt einen Wagen acht Meter weit, genau in Bewegungsrichtung. Wie gross ist die Arbeit?'),
        wahl('Frage 2', 'Eine Kraft von 100 N zieht unter 60° zum Weg einen Körper 10 m weit. Wie gross ist die Arbeit?',
             ['1000 J', '866 J', '500 J'], 2,
             {0: 'Nur der Anteil der Kraft in Wegrichtung zählt.', 1: 'Das ist mit dem Sinus. Der Winkel liegt zwischen Kraft und Weg: Kosinus.'},
             sprich='Eine Kraft von hundert Newton zieht unter sechzig Grad zum Weg einen Körper zehn Meter weit. Wie gross ist die Arbeit?'),
        wahl('Frage 3', 'Ein Kellner trägt ein Tablett waagrecht durch den Raum. Wie viel Arbeit verrichtet seine Haltekraft am Tablett?',
             ['viel, er wird ja müde', 'keine', 'so viel wie die Hubarbeit'], 1,
             {0: 'Müde werden ist keine Arbeit im Sinn der Physik. In welche Richtung zeigt die Haltekraft, in welche der Weg?', 2: 'Wird das Tablett gehoben?'}),
        wahl('Frage 4', 'Welche Umwandlung findet in einer Solarzelle statt?',
             ['Strahlungsenergie in elektrische Energie', 'elektrische Energie in Strahlungsenergie', 'Wärme in Lageenergie'], 0,
             {1: 'Das tut eine Lampe. Was nimmt die Solarzelle auf?', 2: 'Was trifft auf die Solarzelle, und was kommt aus dem Kabel?'}),
        wahl('Frage 5', 'Ein Rucksack (8 kg) wird 1.5 m hoch in ein Gepäckfach gehoben. Wie gross ist die Hubarbeit?',
             ['12 J', '118 J', '78.5 J'], 1,
             {0: 'Die Kraft zum Heben ist die Gewichtskraft m · g.', 2: 'Das ist nur die Gewichtskraft in Newton. Noch mal die Höhe.'},
             sprich='Ein Rucksack mit acht Kilogramm wird eins Komma fünf Meter hoch in ein Gepäckfach gehoben. Wie gross ist die Hubarbeit?',
             rueck_sprich={0: 'Die Kraft zum Heben ist die Gewichtskraft, m mal g.'}),
    ]))

DREH.append(dict(KOPF, titel='Energie sehen: Kontrollfragen zu Lage- und Bewegungsenergie', dateiname='p4-3-lp-kontrolle-bremsen',
    kurzbeschrieb='Fünf Fragen zur Bewegungsenergie, zum dreifachen Tempo, zur Lageenergie, zum Bremsweg und zum Tempo aus der Energie.',
    schlagworte=['Bewegungsenergie', 'Lageenergie', 'Bremsweg', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Ein halb mal null Komma vier mal zehn im Quadrat: zwanzig Joule.',
           formel(r'\fc{E_\text{kin}} = \tfrac12 \cdot 0.4\;\text{kg} \cdot (10\;\text{m/s})^2 = \fc{20\;\text{J}}', g=48, ein=1.0)),
        sz('Frage 2', 'Das Tempo steht im Quadrat: drei mal drei, neunmal so viel Energie.',
           formel(r'(3 \cdot v)^2 = 9 \cdot v^2', ein=1.0)),
        sz('Frage 3', 'Masse mal g mal Höhe: fünf mal neun Komma acht eins mal zwei, rund achtundneunzig Joule.',
           formel(r'\fa{E_\text{pot}} = 5\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 2\;\text{m} \approx \fa{98.1\;\text{J}}', g=48, ein=1.0)),
        sz('Frage 4', 'Die Bewegungsenergie ist neunzigtausend Joule. Durch sechstausend Newton: fünfzehn Meter.',
           formel(r's = \dfrac{\tfrac12 \cdot 800\;\text{kg} \cdot (15\;\text{m/s})^2}{6000\;\text{N}} = 15\;\text{m}', g=44, ein=1.0)),
        sz('Frage 5', 'Zwei mal die Energie durch die Masse, dann die Wurzel: fünf Meter pro Sekunde.',
           formel(r'\fc{v} = \sqrt{\dfrac{2 \cdot 1125\;\text{J}}{90\;\text{kg}}} = \fc{5\;\text{m/s}}', g=48, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Ball (0.4 kg) fliegt mit 10 m/s. Wie gross ist seine Bewegungsenergie?',
             ['20 J', '40 J', '2 J'], 0,
             {1: 'Der Faktor ½ fehlt.', 2: 'Die Geschwindigkeit steht im Quadrat.'},
             sprich='Ein Ball mit null Komma vier Kilogramm fliegt mit zehn Metern pro Sekunde. Wie gross ist seine Bewegungsenergie?',
             rueck_sprich={1: 'Der Faktor ein halb fehlt.'}),
        wahl('Frage 2', 'Das Tempo eines Körpers verdreifacht sich. Seine Bewegungsenergie …',
             ['verdreifacht sich', 'verneunfacht sich', 'versechsfacht sich'], 1,
             {0: 'Wie steht v in der Formel: einfach oder im Quadrat?', 2: 'Drei mal zwei? Das Tempo steht im Quadrat.'},
             sprich='Das Tempo eines Körpers verdreifacht sich. Wie ändert sich seine Bewegungsenergie?'),
        wahl('Frage 3', 'Eine Kiste (5 kg) steht auf einem 2 m hohen Schrank. Wie gross ist ihre Lageenergie bezogen auf den Boden?',
             ['10 J', '49.1 J', '98.1 J'], 2,
             {0: 'Die Gewichtskraft ist m · g, nicht m.', 1: 'Das ist nur die Gewichtskraft. Noch mal die Höhe.'},
             sprich='Eine Kiste mit fünf Kilogramm steht auf einem zwei Meter hohen Schrank. Wie gross ist ihre Lageenergie bezogen auf den Boden?',
             rueck_sprich={0: 'Die Gewichtskraft ist m mal g, nicht m.'}),
        wahl('Frage 4', 'Ein Auto (800 kg) bremst aus 15 m/s mit 6000 N. Wie lang ist der Bremsweg?',
             ['15 m', '30 m', '1 m'], 0,
             {1: 'Der Faktor ½ in der Bewegungsenergie fehlt.', 2: 'Die Geschwindigkeit steht im Quadrat.'},
             sprich='Ein Auto mit achthundert Kilogramm bremst aus fünfzehn Metern pro Sekunde mit sechstausend Newton. Wie lang ist der Bremsweg?',
             rueck_sprich={1: 'Der Faktor ein halb in der Bewegungsenergie fehlt.'}),
        wahl('Frage 5', 'Ein Velo mit Fahrer (90 kg) hat 1125 J Bewegungsenergie. Wie schnell fährt es?',
             ['25 m/s', '5 m/s', '3.54 m/s'], 1,
             {0: 'Das ist v². Noch die Wurzel ziehen.', 2: 'Der Faktor 2 fehlt: v = √(2 · E / m).'},
             sprich='Ein Velo mit Fahrer, neunzig Kilogramm, hat elfhundertfünfundzwanzig Joule Bewegungsenergie. Wie schnell fährt es?',
             rueck_sprich={0: 'Das ist v Quadrat. Noch die Wurzel ziehen.', 2: 'Der Faktor zwei fehlt: v gleich Wurzel aus zwei mal E durch m.'}),
    ]))

DREH.append(dict(KOPF, titel='Energie sehen: Kontrollfragen zur Energieerhaltung', dateiname='p4-3-lp-kontrolle-erhaltung',
    kurzbeschrieb='Fünf Fragen zum freien Fall, zu verschiedenen Massen, zur Steighöhe, zum Start mit Anfangstempo und zu einem zu hohen Hügel.',
    schlagworte=['Energieerhaltung', 'freier Fall', 'Steighöhe', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'Wurzel aus zwei g h: Wurzel aus zwei mal neun Komma acht eins mal fünf, rund neun Komma neun Meter pro Sekunde.',
           formel(r'\fc{v} = \sqrt{2 \cdot 9.81\;\text{m/s}^2 \cdot 5\;\text{m}} \approx \fc{9.9\;\text{m/s}}', g=48, ein=1.0)),
        sz('Frage 2', 'Die Masse kürzt sich. Beide Kugeln sind unten gleich schnell.',
           formel(r'm \cdot g \cdot h = \tfrac12 \cdot m \cdot v^2', ein=1.0)),
        sz('Frage 3', 'v Quadrat durch zwei g: sechsunddreissig durch neunzehn Komma sechs zwei, rund eins Komma acht drei Meter.',
           formel(r'h = \dfrac{(6\;\text{m/s})^2}{2 \cdot 9.81\;\text{m/s}^2} \approx 1.83\;\text{m}', g=48, ein=1.0)),
        sz('Frage 4', 'Die Energien addieren sich, nicht die Geschwindigkeiten: Wurzel aus vier Quadrat plus zwei g mal zehn, rund vierzehn Komma sechs Meter pro Sekunde.',
           formel(r'\fc{v} = \sqrt{(4\;\text{m/s})^2 + 2 \cdot 9.81\;\text{m/s}^2 \cdot 10\;\text{m}} \approx \fc{14.6\;\text{m/s}}', g=42, ein=1.0)),
        sz('Frage 5', 'Aus der Ruhe kommt der Wagen höchstens wieder auf seine Starthöhe, fünfzehn Meter. Der Hügel mit sechzehn Metern ist zu hoch.',
           notiz('höchstens Starthöhe:|15 m < 16 m', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Stein fällt aus 5 m Höhe, ohne Luftwiderstand. Wie schnell ist er unten?',
             ['9.9 m/s', '98.1 m/s', '7.0 m/s'], 0,
             {1: 'Das ist v². Noch die Wurzel ziehen.', 2: 'Der Faktor 2 fehlt: v = √(2 · g · h).'},
             sprich='Ein Stein fällt aus fünf Metern Höhe, ohne Luftwiderstand. Wie schnell ist er unten?',
             rueck_sprich={1: 'Das ist v Quadrat. Noch die Wurzel ziehen.', 2: 'Der Faktor zwei fehlt: v gleich Wurzel aus zwei g h.'}),
        wahl('Frage 2', 'Zwei Kugeln, 1 kg und 3 kg, rollen reibungsfrei dieselbe Rampe hinunter. Welche ist unten schneller?',
             ['die schwere', 'die leichte', 'beide gleich'], 2,
             {0: 'Die schwere hat mehr Energie, braucht aber auch mehr für dasselbe Tempo.', 1: 'Die leichte hat weniger Energie, braucht aber auch weniger.'},
             sprich='Zwei Kugeln, ein Kilogramm und drei Kilogramm, rollen reibungsfrei dieselbe Rampe hinunter. Welche ist unten schneller?'),
        wahl('Frage 3', 'Ein Ball wird mit 6 m/s senkrecht hochgeworfen. Wie hoch steigt er, ohne Luftwiderstand?',
             ['3.67 m', '1.83 m', '0.31 m'], 1,
             {0: 'Der Faktor 2 fehlt: h = v² / (2 · g).', 2: 'Die Geschwindigkeit steht im Quadrat.'},
             sprich='Ein Ball wird mit sechs Metern pro Sekunde senkrecht hochgeworfen. Wie hoch steigt er, ohne Luftwiderstand?',
             rueck_sprich={0: 'Der Faktor zwei fehlt: h gleich v Quadrat durch zwei g.'}),
        wahl('Frage 4', 'Ein Wagen fährt reibungsfrei mit 4 m/s auf 10 m Höhe los. Wie schnell ist er im Tal?',
             ['18.0 m/s', '14.0 m/s', '14.6 m/s'], 2,
             {0: 'Geschwindigkeiten addieren sich nicht — die Energien.', 1: 'Das Anfangstempo bringt Bewegungsenergie mit.'},
             sprich='Ein Wagen fährt reibungsfrei mit vier Metern pro Sekunde auf zehn Metern Höhe los. Wie schnell ist er im Tal?'),
        wahl('Frage 5', 'Ein Wagen startet reibungsfrei aus der Ruhe auf 15 m Höhe. Kommt er über einen 16 m hohen Hügel?',
             ['ja, mit genug Schwung', 'nein, er kehrt um', 'nur, wenn er schwer genug ist'], 1,
             {0: 'Woher sollte die Energie für den zusätzlichen Meter kommen?', 2: 'Die Masse kürzt sich. Woher sollte die Energie kommen?'},
             sprich='Ein Wagen startet reibungsfrei aus der Ruhe auf fünfzehn Metern Höhe. Kommt er über einen sechzehn Meter hohen Hügel?'),
    ]))

DREH.append(dict(KOPF, titel='Energie sehen: Kontrollfragen zu Reibung und Motor', dateiname='p4-3-lp-kontrolle-reibung',
    kurzbeschrieb='Fünf Fragen zur Wärme durch Reibung, zur Rutschbahn, zum Lift mit Reibung, zum Tempo mit Reibung und zum Energieerhaltungssatz.',
    schlagworte=['Energieerhaltungssatz', 'Reibung', 'Wärme', 'Motor', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Die Energie ist nicht verschwunden. Kufen und Schnee sind ein wenig wärmer geworden.',
           notiz('Reibung:|Bewegung → Wärme', y=320, ein=1.0, g=50)),
        sz('Frage 2', 'Lageenergie minus Bewegungsenergie: siebenhundertsechsunddreissig minus dreihundertzwölf Komma fünf, rund vierhundertdreiundzwanzig Joule.',
           formel(r'25\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 3\;\text{m} - \tfrac12 \cdot 25\;\text{kg} \cdot (5\;\text{m/s})^2 \approx \fd{423\;\text{J}}', g=38, ein=1.0)),
        sz('Frage 3', 'Hubarbeit plus Reibungsarbeit: achtundfünfzigtausendachthundertsechzig plus fünftausend Joule, rund dreiundsechzig Komma neun Kilojoule.',
           formel(r'W_M = 600\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 10\;\text{m} + 500\;\text{N} \cdot 10\;\text{m} \approx 63.9\;\text{kJ}', g=36, ein=1.0)),
        sz('Frage 4', 'Ein Teil der Lageenergie wird Wärme statt Bewegung. Darum ist der Wagen unten langsamer.',
           formel(r'\fc{E_\text{kin}} = m \cdot g \cdot h - \fd{F_R \cdot s}', ein=1.0)),
        sz('Frage 5', 'Die Summe aller Energien bleibt gleich. Einzelne Formen ändern sich.',
           notiz('Summe aller Energien|bleibt gleich', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Schlitten verliert auf einer Abfahrt 3000 J Bewegungsenergie durch Reibung. Wohin ist diese Energie gegangen?',
             ['Sie ist verschwunden.', 'In Wärme von Kufen und Schnee.', 'In Lageenergie.'], 1,
             {0: 'Energie verschwindet nie. In welche Form wandelt Reibung sie um?', 2: 'Ist der Schlitten höher gekommen?'},
             sprich='Ein Schlitten verliert auf einer Abfahrt dreitausend Joule Bewegungsenergie durch Reibung. Wohin ist diese Energie gegangen?'),
        wahl('Frage 2', 'Ein Kind (25 kg) rutscht 3 m hinunter und ist unten 5 m/s schnell. Wie viel Energie wurde zu Wärme?',
             ['423 J', '736 J', '313 J'], 0,
             {1: 'Das ist die ganze Lageenergie. Ein Teil steckt unten in der Bewegung.', 2: 'Das ist die Bewegungsenergie unten.'},
             sprich='Ein Kind mit fünfundzwanzig Kilogramm rutscht drei Meter hinunter und ist unten fünf Meter pro Sekunde schnell. Wie viel Energie wurde zu Wärme?'),
        wahl('Frage 3', 'Ein Lift (600 kg) fährt mit konstantem Tempo 10 m hoch, die Reibung beträgt 500 N. Wie viel Arbeit verrichtet der Motor?',
             ['58.9 kJ', '53.9 kJ', '63.9 kJ'], 2,
             {0: 'Das ist nur die Hubarbeit. Die Reibung kostet auch.', 1: 'Die Reibung arbeitet gegen den Motor: Ihre Arbeit kommt dazu.'},
             sprich='Ein Lift mit sechshundert Kilogramm fährt mit konstantem Tempo zehn Meter hoch, die Reibung beträgt fünfhundert Newton. Wie viel Arbeit verrichtet der Motor?'),
        wahl('Frage 4', 'Ein Wagen rollt einen Hang hinunter, einmal ohne, einmal mit Reibung. Wie ist er mit Reibung unten?',
             ['langsamer', 'schneller', 'gleich schnell'], 0,
             {1: 'Liefert die Reibung Energie, oder nimmt sie welche weg?', 2: 'Bleibt mit Reibung gleich viel für die Bewegung übrig?'}),
        wahl('Frage 5', 'Was sagt der Energieerhaltungssatz?',
             ['Die Bewegungsenergie bleibt immer gleich.', 'Die Summe aller Energien bleibt gleich.', 'Durch Reibung geht Energie verloren.'], 1,
             {0: 'Ein Wagen wird schneller und langsamer. Was bleibt dabei gleich?', 2: 'Die Energie wird zu Wärme. Ist sie dann weg?'}),
    ]))

DREH.append(dict(KOPF, titel='Energie sehen: Kontrollfragen zu Leistung und Wirkungsgrad', dateiname='p4-3-lp-kontrolle-leistung',
    kurzbeschrieb='Fünf Fragen zur Pumpenleistung, zum Wirkungsgrad, zur Kilowattstunde, zu P = F · v und zu zwei Kränen.',
    schlagworte=['Leistung', 'Wirkungsgrad', 'Kilowattstunde', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Hubarbeit durch Zeit: dreihundert mal neun Komma acht eins mal vier durch sechzig, rund hundertsechsundneunzig Watt.',
           formel(r'P = \dfrac{300\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot 4\;\text{m}}{60\;\text{s}} \approx 196\;\text{W}', g=44, ein=1.0)),
        sz('Frage 2', 'Nutzen durch Aufwand: vierhundert durch fünfhundert, null Komma acht.',
           formel(r'\eta = \dfrac{400\;\text{W}}{500\;\text{W}} = 0.8', ein=1.0)),
        sz('Frage 3', 'Ein Kilowatt während einer Stunde: Die Kilowattstunde ist eine Energie, drei Komma sechs Megajoule.',
           formel(r'1\;\text{kWh} = 1000\;\text{W} \cdot 3600\;\text{s} = 3.6\;\text{MJ}', g=48, ein=1.0)),
        sz('Frage 4', 'Kraft mal Geschwindigkeit: dreissig Newton mal fünf Meter pro Sekunde, hundertfünfzig Watt.',
           formel(r'P = F \cdot v = 30\;\text{N} \cdot 5\;\text{m/s} = 150\;\text{W}', ein=1.0)),
        sz('Frage 5', 'Die Arbeit ist gleich, die Zeit halb so lang: doppelte Leistung.',
           formel(r'P = \dfrac{W}{t}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Pumpe hebt in 60 s 300 kg Wasser 4 m hoch. Wie gross ist ihre Hubleistung?',
             ['196 W', '11.8 kJ', '20 W'], 0,
             {1: 'Das ist die Arbeit. Leistung ist Arbeit pro Zeit.', 2: 'Die Hubarbeit ist m · g · h — g fehlt.'},
             sprich='Eine Pumpe hebt in sechzig Sekunden dreihundert Kilogramm Wasser vier Meter hoch. Wie gross ist ihre Hubleistung?',
             rueck_sprich={2: 'Die Hubarbeit ist m mal g mal h, g fehlt.'}),
        wahl('Frage 2', 'Ein Motor nimmt 500 W auf und gibt 400 W nutzbar ab. Wie gross ist sein Wirkungsgrad?',
             ['1.25', '0.8', '100 W'], 1,
             {0: 'Umgekehrt: Nutzen durch Aufwand. Mehr als 1 geht nie.', 2: 'Das ist die Verlustleistung, nicht der Wirkungsgrad.'},
             sprich='Ein Motor nimmt fünfhundert Watt auf und gibt vierhundert Watt nutzbar ab. Wie gross ist sein Wirkungsgrad?',
             rueck_sprich={0: 'Umgekehrt: Nutzen durch Aufwand. Mehr als eins geht nie.'}),
        wahl('Frage 3', 'Was ist eine Kilowattstunde?',
             ['eine Leistung', 'eine Kraft', 'eine Energie'], 2,
             {0: 'Kilowatt ist eine Leistung. Was ergibt Leistung mal Zeit?', 1: 'Was ergibt Leistung mal Zeit?'}),
        wahl('Frage 4', 'Ein Velofahrer fährt konstant mit 5 m/s, Reibung und Luftwiderstand betragen zusammen 30 N. Welche Leistung braucht er dafür?',
             ['150 W', '6 W', '35 W'], 0,
             {1: 'Geteilt? Leistung ist Kraft mal Geschwindigkeit.', 2: 'Addiert? Leistung ist Kraft mal Geschwindigkeit.'},
             sprich='Ein Velofahrer fährt konstant mit fünf Metern pro Sekunde, Reibung und Luftwiderstand betragen zusammen dreissig Newton. Welche Leistung braucht er dafür?'),
        wahl('Frage 5', 'Zwei Kräne heben dieselbe Last gleich hoch, einer doppelt so schnell. Was ist beim schnelleren doppelt so gross?',
             ['die Arbeit', 'die Leistung', 'die Lageenergie oben'], 1,
             {0: 'Die Arbeit hängt von Last und Höhe ab, nicht von der Zeit.', 2: 'Beide Lasten sind gleich hoch.'}),
    ]))

DREH.append(dict(KOPF, titel='Energie sehen: Kontrollfragen zur Energiebilanz der Erde', dateiname='p4-3-lp-kontrolle-erde',
    kurzbeschrieb='Fünf Fragen zur aufgenommenen Leistung, zur Abstrahlung bei Erwärmung, zur Wirkung von CO₂, zum schmelzenden Eis und zum Stefan-Boltzmann-Gesetz.',
    schlagworte=['Energiebilanz', 'Albedo', 'Treibhauseffekt', 'Kontrollfragen'], _probe=KTRL % 6,
    szenen=[
        sz('Frage 1', 'Der Anteil eins minus a wird aufgenommen: null Komma sieben mal dreihundertvierzig, rund zweihundertachtunddreissig Watt pro Quadratmeter.',
           formel(r'(1 - 0.3) \cdot 340\;\text{W/m}^2 \approx 238\;\text{W/m}^2', ein=1.0)),
        sz('Frage 2', 'Je wärmer ein Körper, desto mehr strahlt er ab. Darum regelt sich das Gleichgewicht ein.',
           formel(r'\dfrac{P}{A} = \sigma \cdot T^4', ein=1.0)),
        sz('Frage 3', 'Das CO₂ erzeugt keine Wärme. Es hält einen Teil der Wärmestrahlung zurück, also gelangt weniger ins All.',
           notiz('weniger hinaus|→ wärmer, bis es passt', y=320, ein=1.0, g=50)),
        sz('Frage 4', 'Eis wirft viel Licht zurück, offenes Meer wenig. Schmilzt Eis, sinkt die Albedo.',
           notiz('Albedo kleiner|→ mehr aufgenommen', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Die Abstrahlung wächst mit der vierten Potenz der Temperatur: zwei hoch vier, sechzehnmal so viel.',
           formel(r'2^4 = 16', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Im Mittel treffen 340 W/m² auf die Erde, die Albedo ist 0.3. Wie viel nimmt die Erde je Quadratmeter auf?',
             ['102 W/m²', '238 W/m²', '340 W/m²'], 1,
             {0: 'Das ist der Anteil, der zurückgeworfen wird.', 2: 'Ein Teil wird zurückgeworfen: die Albedo.'},
             sprich='Im Mittel treffen dreihundertvierzig Watt pro Quadratmeter auf die Erde, die Albedo ist null Komma drei. Wie viel nimmt die Erde je Quadratmeter auf?'),
        wahl('Frage 2', 'Was geschieht mit der Abstrahlung der Erde ins All, wenn sie wärmer wird?',
             ['sie nimmt zu', 'sie nimmt ab', 'sie bleibt gleich'], 0,
             {1: 'Strahlt ein heisser Ofen weniger ab als ein kalter?', 2: 'Hängt die Abstrahlung von der Temperatur ab?'}),
        wahl('Frage 3', 'Was bewirkt mehr CO₂ in der Atmosphäre?',
             ['Es erzeugt Wärme.', 'Es wirft mehr Sonnenlicht zurück.', 'Es lässt weniger Wärmestrahlung ins All.'], 2,
             {0: 'Woher sollte das Gas die Energie nehmen?', 1: 'Das wäre eine grössere Albedo — die würde kühlen.'},
             sprich='Was bewirkt mehr C O zwei in der Atmosphäre?'),
        wahl('Frage 4', 'Meereis schmilzt. Was geschieht mit der Albedo der Erde?',
             ['sie wird grösser', 'sie wird kleiner', 'sie bleibt gleich'], 1,
             {0: 'Wirft offenes Meer mehr Licht zurück als Eis?', 2: 'Eis und Wasser werfen nicht gleich viel Licht zurück.'}),
        wahl('Frage 5', 'Eine Fläche hat 300 K, eine andere 600 K. Wie viel mehr strahlt die wärmere ab?',
             ['doppelt so viel', 'viermal so viel', 'sechzehnmal so viel'], 2,
             {0: 'Die Temperatur steht nicht einfach in der Formel.', 1: 'Nicht im Quadrat — in welcher Potenz steht T?'},
             sprich='Eine Fläche hat dreihundert Kelvin, eine andere sechshundert Kelvin. Wie viel mehr strahlt die wärmere ab?'),
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
