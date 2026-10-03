"""Erzeugt die zehn Drehbücher des Leitprogramms Elektrizität (clips/p6-2-lp-*.json).

  python3 scripts/lp/elektrizitaet/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/elektrizitaet/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)

Archiv-Werkzeug wie kontrollclips.py im Mathe-Vorbild: Nach der Vertonung sind die JSONs in
clips/ die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf
mit --neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).

Farben wie in der Simulation: \\fa U (Bernstein), \\fb I (Orange), \\fc R (Grün); Ladung,
Leistung und Energie ungefärbt. Zahlen im Sprechertext ausgeschrieben (CLAUDE.md).
"""
import json
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv

KOPF = {
    'themenbereich': 'Elektrizität · BM', 'lerngebiet': '6 · Einführung in andere Bereiche der Physik',
    'lektion': ['p6-2'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-03', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Strom sehen', 'nachlauf': 2.6, 'probe': True,
}
JETZT = {'name': 'Jetzt du', 'layout': 'zentriert', 'oben': 200,
         'sprecher': 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
         'elemente': [{'typ': 'titel', 'text': 'Jetzt du', 'x': 150, 'y': 280, 'groesse': 86},
                      {'typ': 'notiz', 'text': 'Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.',
                       'x': 150, 'y': 430, 'groesse': 50, 'farbe': 'blau', 'ein': 0.6}]}


def formel(t, y=300, g=54, ein=0.8):
    return {'typ': 'formel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'ein': ein}


def notiz(t, y=460, farbe='blau', ein=2.4, g=46):
    return {'typ': 'notiz', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'farbe': farbe, 'ein': ein}


def titel(t, y=300, g=86):
    return {'typ': 'titel', 'text': t, 'x': 150, 'y': y, 'breite': 1640, 'groesse': g}


def bild(datei, breite=760, y=200, ein=0.05):
    return {'typ': 'bild', 'datei': 'bilder/' + datei, 'x': 1010, 'y': y, 'breite': breite, 'abstand': 0, 'anim': 'fade', 'ein': ein}


# Koordinatenbilder: dieselben Fenster wie die Simulationen der Seite
def graf_qt(geraden, punkte=None):
    g = {'typ': 'graf', 'x': 1010, 'y': 175, 'breite': 760, 'hoehe': 760, 'abstand': 0, 'anim': 'fade', 'ein': 0.05,
         'geraden': geraden, 'pfeile': True, 'xbereich': [-0.9, 11], 'ybereich': [-2.6, 31],
         'xteilung': [[2, '2'], [4, '4'], [6, '6'], [8, '8'], [10, '10']], 'yteilung': [[10, '10'], [20, '20'], [30, '30']],
         'xname': 't [s]', 'yname': 'Q [C]'}
    if punkte:
        g['punkte'] = punkte
    return g


def graf_rl(geraden, punkte=None):
    g = {'typ': 'graf', 'x': 1010, 'y': 175, 'breite': 760, 'hoehe': 760, 'abstand': 0, 'anim': 'fade', 'ein': 0.05,
         'geraden': geraden, 'pfeile': True, 'xbereich': [-6.5, 64], 'ybereich': [-0.6, 5.5],
         'xteilung': [[10, '10'], [20, '20'], [30, '30'], [40, '40'], [50, '50'], [60, '60']], 'yteilung': [[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']],
         'xname': 'l [m]', 'yname': 'R [Ω]'}
    if punkte:
        g['punkte'] = punkte
    return g


def sz(name, sprecher, *elemente):
    return {'name': name, 'layout': 'zentriert', 'oben': 200, 'sprecher': sprecher, 'elemente': list(elemente)}


def wahl(szene, text, optionen, rueck, sprich=None, rueck_sprich=None):
    F = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'text': text, 'optionen': optionen, 'richtig': 0,
         'rueck': {str(k): v for k, v in rueck.items()}}
    if sprich:
        F['sprich'] = sprich
    if rueck_sprich:
        F['rueck_sprich'] = {str(k): v for k, v in rueck_sprich.items()}
    return F


DREH = []

# ================================================================== Kapitel 1
DREH.append(dict(KOPF, titel='Strom sehen: vom Elektron zum Ampere', dateiname='p6-2-lp-ladung',
    kurzbeschrieb='Woher Ladung kommt, was die Elementarladung ist und warum die Stromstärke die Steigung im Q-t-Diagramm ist.',
    schlagworte=['Ladung', 'Elementarladung', 'Stromstärke', 'Ampere', 'Coulomb'],
    _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 1; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Ladung', 'Jedes Atom hat einen positiven Kern und eine Hülle aus negativen Elektronen. Hat ein Körper Elektronen zu viel, ist er negativ geladen. Fehlen ihm welche, ist er positiv.',
           titel('Woher kommt Ladung?'),
           notiz('Kern: positiv (Protonen)|Hülle: negativ (Elektronen)', y=440, ein=1.2),
           notiz('Elektronen zu viel: negativ|Elektronen zu wenig: positiv', y=620, farbe='rot', ein=4.0)),
        sz('Elementarladung', 'Jede Ladung ist ein ganzes Vielfaches der Elementarladung e: eins Komma sechs null zwei mal zehn hoch minus neunzehn Coulomb. Und Ladung entsteht nie neu. Beim Reiben wandern nur Elektronen vom einen Körper auf den anderen.',
           formel(r'Q = n \cdot e \qquad e = 1.602 \cdot 10^{-19}\;\text{C}', g=58),
           notiz('Ladung wird nicht erzeugt,|nur verschoben.', ein=5.0)),
        sz('Strom', 'Bewegt sich Ladung, fliesst Strom. Die Stromstärke ist Ladung pro Zeit; ein Ampere heisst ein Coulomb pro Sekunde. Im Diagramm wächst die Ladung mit der Zeit. Die Steigung der Geraden ist die Stromstärke.',
           formel(r'\fb{I} = \dfrac{Q}{t} \qquad 1\;\text{A} = 1\;\dfrac{\text{C}}{\text{s}}', g=58),
           notiz('Die Steigung|ist die Stromstärke.', ein=7.0),
           graf_qt([{'bewegung': [[3.0, 0, 0], [6.0, 2, 0]], 'farbe': 2}])),
        sz('Zwei Ampere', 'Zwei Ampere während fünf Sekunden: Ladung gleich Stromstärke mal Zeit, zwei mal fünf, also zehn Coulomb.',
           formel(r'Q = \fb{I} \cdot t = \fb{2\;\text{A}} \cdot 5\;\text{s} = 10\;\text{C}'),
           graf_qt([{'bewegung': [[0, 2, 0]], 'farbe': 2, 'marken': [{'x': 5, 'text': 'Q = {y} C', 'farbe': 5}]}])),
        sz('Mehr Strom', 'Mehr Strom heisst: steilere Gerade. Bei drei Ampere sind es nach fünf Sekunden fünfzehn Coulomb.',
           formel(r'Q = \fb{3\;\text{A}} \cdot 5\;\text{s} = 15\;\text{C}'),
           notiz('steiler:|mehr Strom', ein=2.0),
           graf_qt([{'bewegung': [[0.6, 2, 0], [3.0, 3, 0]], 'farbe': 2, 'marken': [{'x': 5, 'text': 'Q = {y} C', 'farbe': 5}]}])),
        sz('Elektronen zählen', 'Und wie viele Elektronen sind zehn Coulomb? Zehn geteilt durch die Elementarladung: rund sechs Komma zwei vier mal zehn hoch neunzehn. Eine gewaltige Zahl, darum rechnet man in Coulomb.',
           formel(r'n = \dfrac{Q}{e} = \dfrac{10\;\text{C}}{1.602 \cdot 10^{-19}\;\text{C}} \approx 6.24 \cdot 10^{19}', g=46),
           graf_qt([{'bewegung': [[0, 2, 0]], 'farbe': 2}], [{'x': 5, 'y': 10, 'farbe': 5, 'beschriftung': '10 C', 'beschriftung_bei': [5.5, 8.4]}])),
        sz('Merke', 'Zum Mitnehmen: Ladung ist ein Vielfaches der Elementarladung. Stromstärke ist Ladung pro Zeit, und die Zeit gehört in Sekunden.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'Q = n \cdot e \qquad \fb{I} = \dfrac{Q}{t}', y=420, ein=0.4),
           notiz('Überschuss: negativ|Mangel: positiv|Zeit in Sekunden', y=560, ein=1.2, g=44)),
        JETZT,
    ]))

DREH.append(dict(KOPF, titel='Strom sehen: Kontrollfragen zu Ladung und Stromstärke', dateiname='p6-2-lp-kontrolle-ladung',
    kurzbeschrieb='Fünf Fragen zu Ladung, Elementarladung und Stromstärke, eine davon im Q-t-Diagramm.',
    schlagworte=['Ladung', 'Stromstärke', 'Elementarladung', 'Kontrollfragen'],
    _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 1; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Frage 1', 'Elektronen abgegeben heisst: Mangel an negativer Ladung. Der Stab ist positiv, das Tuch gleich stark negativ. Die Summe bleibt null.',
           formel(r'\text{Elektronenmangel} \;\Longrightarrow\; Q \gt 0', ein=1.0),
           notiz('Die Elektronen sitzen jetzt|auf dem Tuch.', ein=3.0)),
        sz('Frage 2', 'Ladung pro Zeit: sechs Coulomb durch drei Sekunden, zwei Ampere. Im Diagramm ist das die Steigung.',
           formel(r'\fb{I} = \dfrac{Q}{t} = \dfrac{6\;\text{C}}{3\;\text{s}} = \fb{2\;\text{A}}', ein=1.0),
           graf_qt([{'bewegung': [[1.0, 0, 0], [3.2, 2, 0]], 'farbe': 2, 'marken': [{'x': 3, 'text': 'Q = {y} C', 'farbe': 5}]}])),
        sz('Frage 3', 'Ladung gleich Stromstärke mal Zeit: eins Komma fünf mal vier, sechs Coulomb.',
           formel(r'Q = \fb{1.5\;\text{A}} \cdot 4\;\text{s} = 6\;\text{C}', ein=1.0),
           graf_qt([{'bewegung': [[1.0, 0, 0], [3.2, 1.5, 0]], 'farbe': 2}])),
        sz('Frage 4', 'Doppelte Zeit, doppelte Ladung. Auf derselben Geraden geht es von sechs auf zwölf Coulomb.',
           formel(r'Q = \fb{I} \cdot t', ein=1.0),
           graf_qt([{'bewegung': [[0, 1.5, 0]], 'farbe': 2, 'laeufer': {'bahn': [[1.2, 4], [3.6, 8]], 'text': 'Q = {y} C', 'farbe': 5}}])),
        sz('Frage 5', 'Ein Coulomb geteilt durch die Elementarladung: rund sechs Komma zwei vier mal zehn hoch achtzehn Elektronen.',
           formel(r'n = \dfrac{1\;\text{C}}{1.602 \cdot 10^{-19}\;\text{C}} \approx 6.24 \cdot 10^{18}', g=48, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Glasstab hat beim Reiben Elektronen an ein Tuch abgegeben. Wie ist er geladen?',
             ['positiv', 'negativ', 'neutral'],
             {1: 'Elektronen sind negativ. Wer welche abgibt, behält mehr positive Ladung.',
              2: 'Neutral ist er nur, solange Elektronen und Protonen gleich viele sind.'}),
        wahl('Frage 2', 'In 3 s fliessen 6 C durch einen Draht. Wie gross ist die Stromstärke?',
             ['2 A', '18 A', '0.5 A'],
             {1: 'Das ist Ladung mal Zeit. Stromstärke ist Ladung pro Zeit.', 2: 'Umgekehrt: Ladung durch Zeit, nicht Zeit durch Ladung.'},
             sprich='In drei Sekunden fliessen sechs Coulomb durch einen Draht. Wie gross ist die Stromstärke?'),
        {'szene': 'Frage 3', 'bei': 0.3, 'typ': 'klick',
         'text': 'Es fliessen 1.5 A. Wie viel Ladung ist nach 4 s geflossen? Tipp den Punkt ins Bild.',
         'sprich': 'Es fliessen eins Komma fünf Ampere. Wie viel Ladung ist nach vier Sekunden geflossen? Tipp den Punkt ins Bild.',
         'ziel': [4, 6], 'toleranz': 1.3, 'richtig_text': 'Getroffen: 6 C.',
         'fallen': [{'bei': [4, 1.5], 'text': 'Das ist die Stromstärke. Die Ladung ist Stromstärke mal Zeit.'},
                    {'bei': [1.5, 4], 'text': 'Achsen vertauscht: Die Zeit steht rechts, die Ladung oben.'}],
         'falsch_text': 'Nicht ganz. Der grüne Kreis zeigt die Stelle: 1.5 A mal 4 s.',
         'falsch_sprich': 'Nicht ganz. Der grüne Kreis zeigt die Stelle: eins Komma fünf Ampere mal vier Sekunden.'},
        wahl('Frage 4', 'Gleicher Strom, doppelte Zeit. Was geschieht mit der Ladung, die durch den Draht fliesst?',
             ['sie verdoppelt sich', 'sie bleibt gleich', 'sie halbiert sich'],
             {1: 'Der Strom bleibt, aber er fliesst länger.', 2: 'Mehr Zeit heisst mehr Ladung, nicht weniger.'}),
        wahl('Frage 5', 'Ungefähr wie viele Elektronen sind 1 C?',
             ['6.24·10¹⁸', '1.602·10⁻¹⁹', '6.24·10⁻¹⁸'],
             {1: 'Das ist die Ladung eines einzigen Elektrons, in Coulomb.', 2: 'Viele Elektronen, nicht ein Bruchteil: Die Hochzahl ist positiv.'},
             sprich='Ungefähr wie viele Elektronen sind ein Coulomb?'),
    ]))

# ================================================================== Kapitel 2
DREH.append(dict(KOPF, titel='Strom sehen: Leistung ist Höhe, Energie ist Fläche', dateiname='p6-2-lp-leistung',
    kurzbeschrieb='Spannung als Energie je Ladung, Leistung als Höhe und Energie als Fläche im P-t-Diagramm, abgerechnet in Kilowattstunden.',
    schlagworte=['Spannung', 'Leistung', 'Energie', 'Kilowattstunde', 'P-t-Diagramm'],
    _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 2; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Spannung', 'Spannung ist Energie je Ladung. Eine Neun-Volt-Batterie gibt jedem Coulomb, das sie durch den Kreis schiebt, neun Joule mit.',
           titel('Was ist Spannung?'),
           formel(r'\fa{U} = \dfrac{W}{Q} \qquad 1\;\text{V} = 1\;\dfrac{\text{J}}{\text{C}}', y=440, ein=1.0),
           notiz('9-V-Batterie:|jedes Coulomb bekommt 9 J', y=600, ein=4.0)),
        sz('Leistung', 'Die Leistung ist Spannung mal Stromstärke. Ein Wasserkocher am Netz: zweihundertdreissig Volt mal acht Komma sieben Ampere, rund zweitausend Watt. Im Diagramm ist das die Höhe.',
           formel(r'P = \fa{U} \cdot \fb{I} = \fa{230\;\text{V}} \cdot \fb{8.7\;\text{A}} \approx 2000\;\text{W}', g=46),
           notiz('Leistung:|Höhe des Rechtecks', ein=6.0),
           bild('p6-2-lp-leistung-1.jpg', ein=0.4)),
        sz('Energie', 'Er läuft eine Viertelstunde. Die Energie ist Leistung mal Zeit, die Fläche des Rechtecks: zwei Kilowatt mal null Komma zwei fünf Stunden, eine halbe Kilowattstunde.',
           formel(r'E = P \cdot t = 2\;\text{kW} \cdot 0.25\;\text{h} = 0.5\;\text{kWh}', g=46),
           notiz('Energie: Fläche|vorher in kW und h umrechnen', ein=4.0),
           bild('p6-2-lp-leistung-1.jpg')),
        sz('Gleich hoch, breiter', 'Ein Heizlüfter mit derselben Leistung läuft anderthalb Stunden. Gleich hoch, aber sechsmal so breit: sechsmal so viel Energie, drei Kilowattstunden.',
           formel(r'E = 2\;\text{kW} \cdot 1.5\;\text{h} = 3\;\text{kWh}'),
           notiz('gleich hoch, sechsmal so breit:|sechsmal so viel Energie', ein=3.0),
           bild('p6-2-lp-leistung-2.jpg')),
        sz('Nicht verbraucht', 'Und auf der Rechnung? Strom wird nicht verbraucht, er fliesst vollständig zur Quelle zurück. Bezahlt wird die umgesetzte Energie, in Kilowattstunden. Eine Stunde Wasserkocher: zwei Kilowattstunden.',
           formel(r'1\;\text{kWh} = 3.6\;\text{MJ}'),
           notiz('Strom fliesst ganz zurück.|Umgesetzt wird Energie.', ein=1.6, farbe='rot'),
           bild('p6-2-lp-leistung-3.jpg', ein=6.0)),
        sz('Merke', 'Zum Mitnehmen: Leistung ist Spannung mal Stromstärke, die Höhe. Energie ist Leistung mal Zeit, die Fläche. Gerechnet in Kilowatt und Stunden.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'P = \fa{U} \cdot \fb{I} \qquad E = P \cdot t', y=420, ein=0.4),
           notiz('Leistung: Höhe|Energie: Fläche', y=560, ein=1.2, g=44)),
        JETZT,
    ]))

DREH.append(dict(KOPF, titel='Strom sehen: Kontrollfragen zu Spannung, Leistung und Energie', dateiname='p6-2-lp-kontrolle-leistung',
    kurzbeschrieb='Fünf Fragen zu Leistung, Energie in Kilowattstunden und Spannung als Energie je Ladung.',
    schlagworte=['Leistung', 'Energie', 'Spannung', 'Kilowattstunde', 'Kontrollfragen'],
    _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 2; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Frage 1', 'Leistung gleich Spannung mal Stromstärke: zweihundertdreissig mal zwei, vierhundertsechzig Watt.',
           formel(r'P = \fa{230\;\text{V}} \cdot \fb{2\;\text{A}} = 460\;\text{W}', ein=1.0)),
        sz('Frage 2', 'Dreissig Minuten sind eine halbe Stunde. Zwei Kilowatt mal null Komma fünf Stunden: eine Kilowattstunde.',
           formel(r'E = P \cdot t = 2\;\text{kW} \cdot 0.5\;\text{h} = 1\;\text{kWh}', g=48, ein=1.0),
           bild('p6-2-lp-leistung-k2.jpg', ein=1.0)),
        sz('Frage 3', 'Jedes Coulomb bekommt zwölf Joule. Fünf Coulomb: sechzig Joule.',
           formel(r'W = \fa{U} \cdot Q = 12\;\text{V} \cdot 5\;\text{C} = 60\;\text{J}', ein=1.0)),
        sz('Frage 4', 'Der Föhn: ein Komma acht Kilowatt mal ein Drittel Stunde, null Komma sechs Kilowattstunden. Der Fernseher: null Komma eins zwei Kilowatt mal vier Stunden, null Komma vier acht. Der Föhn setzt mehr um.',
           formel(r'1.8\;\text{kW} \cdot \tfrac{1}{3}\;\text{h} = 0.6\;\text{kWh}', y=280, g=48, ein=1.0),
           formel(r'0.12\;\text{kW} \cdot 4\;\text{h} = 0.48\;\text{kWh}', y=420, g=48, ein=5.0)),
        sz('Frage 5', 'Der Zähler zählt die umgesetzte Energie, in Kilowattstunden. Die Ladung fliesst ja zurück.',
           formel(r'E = P \cdot t \quad\text{in kWh}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Gerät an 230 V zieht 2 A. Welche Leistung setzt es um?', ['460 W', '115 W', '232 W'],
             {1: 'Geteilt statt mal: P = U · I.', 2: 'Nicht addieren: P = U · I.'},
             sprich='Ein Gerät an zweihundertdreissig Volt zieht zwei Ampere. Welche Leistung setzt es um?',
             rueck_sprich={1: 'Geteilt statt mal: P gleich U mal I.', 2: 'Nicht addieren: P gleich U mal I.'}),
        wahl('Frage 2', 'Ein Gerät mit 2 kW läuft 30 min. Wie viel Energie setzt es um?', ['1 kWh', '60 kWh', '60 000 kWh'],
             {1: 'Minuten in Stunden umrechnen: 30 min = 0.5 h.', 2: 'Erst in kW und h umrechnen, dann multiplizieren.'},
             sprich='Ein Gerät mit zwei Kilowatt läuft dreissig Minuten. Wie viel Energie setzt es um?',
             rueck_sprich={1: 'Minuten in Stunden umrechnen: dreissig Minuten sind null Komma fünf Stunden.', 2: 'Erst in Kilowatt und Stunden umrechnen, dann multiplizieren.'}),
        wahl('Frage 3', 'Eine 12-V-Batterie schiebt 5 C durch den Kreis. Welche Arbeit verrichtet sie?', ['60 J', '2.4 J', '17 J'],
             {1: 'Spannung ist Energie je Ladung. Für 5 C also mal 5.', 2: 'Nicht addieren: W = U · Q.'},
             sprich='Eine Zwölf-Volt-Batterie schiebt fünf Coulomb durch den Kreis. Welche Arbeit verrichtet sie?',
             rueck_sprich={1: 'Spannung ist Energie je Ladung. Für fünf Coulomb also mal fünf.', 2: 'Nicht addieren: W gleich U mal Q.'}),
        wahl('Frage 4', 'Ein Föhn (1800 W) läuft 20 min, ein Fernseher (120 W) läuft 4 h. Wer setzt mehr Energie um?',
             ['der Föhn', 'der Fernseher', 'beide gleich viel'],
             {1: 'Länger ist nicht mehr: Es zählt Leistung mal Zeit.', 2: 'Rechne nach: 0.6 kWh gegen 0.48 kWh.'},
             sprich='Ein Föhn mit tausendachthundert Watt läuft zwanzig Minuten, ein Fernseher mit hundertzwanzig Watt läuft vier Stunden. Wer setzt mehr Energie um?',
             rueck_sprich={2: 'Rechne nach: null Komma sechs Kilowattstunden gegen null Komma vier acht.'}),
        wahl('Frage 5', 'Was zählt der Stromzähler zu Hause?', ['die Energie in kWh', 'die Ladung in C', 'die Stromstärke in A'],
             {1: 'Die Ladung fliesst zurück. Gezählt wird, was umgesetzt wird.', 2: 'Strom wird nicht verbraucht. Gezählt wird Energie.'}),
    ]))

# ================================================================== Kapitel 3
DREH.append(dict(KOPF, titel='Strom sehen: Länge, Querschnitt, Material', dateiname='p6-2-lp-widerstand',
    kurzbeschrieb='Widerstand als U durch I, ohmsch oder nicht, und wie Länge, Querschnitt und Material den Widerstand eines Drahts bestimmen.',
    schlagworte=['Widerstand', 'ohmsches Gesetz', 'spezifischer Widerstand', 'Leiterlänge', 'Querschnitt'],
    _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 3; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Widerstand', 'Der Widerstand ist Spannung geteilt durch Stromstärke. Bleibt er gleich, gilt das ohmsche Gesetz: U gleich R mal I. Eine Glühlampe ist nicht ohmsch. Ihr Draht wird heiss, und der Widerstand wächst.',
           titel('Was ist Widerstand?'),
           formel(r'\fc{R} = \dfrac{\fa{U}}{\fb{I}} \qquad \fa{U} = \fc{R} \cdot \fb{I}', y=440, ein=1.0),
           notiz('ohmsch: R bleibt gleich|Glühlampe: R wächst mit der Temperatur', y=600, ein=6.0)),
        sz('Länge', 'Ein Eisendraht mit einem Quadratmillimeter Querschnitt. Zwanzig Meter haben zwei Ohm. Doppelt so lang: doppelter Widerstand, vier Ohm.',
           formel(r'\fc{R} = \rho \cdot \dfrac{l}{A}', g=60),
           notiz('Eisen, 1 mm²:|20 m: 2 Ω|40 m: 4 Ω', ein=3.0),
           graf_rl([{'bewegung': [[0, 0.1, 0]], 'farbe': 3, 'laeufer': {'bahn': [[3.4, 20], [5.8, 40]], 'text': 'R = {y} Ω', 'farbe': 5}}])),
        sz('Querschnitt', 'Jetzt doppelt so dick, zwei Quadratmillimeter. Der Strom hat mehr Platz, der Widerstand halbiert sich: bei vierzig Metern von vier auf zwei Ohm.',
           formel(r'\fc{R} = 0.10\;\dfrac{\Omega\,\text{mm}^2}{\text{m}} \cdot \dfrac{40\;\text{m}}{2\;\text{mm}^2} = 2\;\Omega', g=40),
           notiz('doppelter Querschnitt:|halber Widerstand', ein=3.0),
           graf_rl([{'bewegung': [[1.0, 0.1, 0], [3.4, 0.05, 0]], 'farbe': 3, 'marken': [{'x': 40, 'text': 'R = {y} Ω', 'farbe': 5}]}])),
        sz('Material', 'Und das Material? Das sagt der spezifische Widerstand rho. Eisen hat null Komma eins, Kupfer null Komma null eins sieben: Kupfer leitet rund sechsmal besser. Darum sind Kabel aus Kupfer.',
           formel(r'\rho_\text{Eisen} = 0.10 \qquad \rho_\text{Kupfer} = 0.017', g=52),
           notiz('in Ω·mm²/m|Kupfer leitet rund sechsmal besser.', ein=6.0),
           graf_rl([{'bewegung': [[2.0, 0.1, 0], [4.6, 0.017, 0]], 'farbe': 3}])),
        sz('Zwei Adern', 'Vorsicht beim Kabel: Der Strom fliesst hin und zurück. Fünfundzwanzig Meter Kupferkabel mit eins Komma fünf Quadratmillimetern sind fünfzig Meter Leiter, rund null Komma fünf sieben Ohm.',
           formel(r'\fc{R} = 0.017\;\dfrac{\Omega\,\text{mm}^2}{\text{m}} \cdot \dfrac{50\;\text{m}}{1.5\;\text{mm}^2} \approx 0.57\;\Omega', g=38),
           notiz('25 m Kabel = 50 m Leiter:|hin und zurück', farbe='rot', ein=1.4),
           graf_rl([{'bewegung': [[0, 0.017 / 1.5, 0]], 'farbe': 3}], [{'x': 50, 'y': 0.567, 'farbe': 5, 'beschriftung': '0.57 Ω', 'beschriftung_bei': [48, 1.1], 'anker': 'end'}])),
        sz('Merke', 'Zum Mitnehmen: Länger heisst grösserer Widerstand, dicker heisst kleinerer. Das Material steckt in rho. Und beim Kabel zählt die Länge doppelt.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fc{R} = \rho \cdot \dfrac{l}{A}', y=420, ein=0.4),
           notiz('länger: grösser|dicker: kleiner|Kabel: Länge mal zwei', y=580, ein=1.2, g=44)),
        JETZT,
    ]))

DREH.append(dict(KOPF, titel='Strom sehen: Kontrollfragen zum Widerstand', dateiname='p6-2-lp-kontrolle-widerstand',
    kurzbeschrieb='Fünf Fragen zu Länge, Querschnitt, Kabelwiderstand, ohmschem Gesetz und Glühlampe.',
    schlagworte=['Widerstand', 'Leiterwiderstand', 'ohmsches Gesetz', 'Kontrollfragen'],
    _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 3; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Frage 1', 'Der Widerstand wächst mit der Länge: doppelt so lang, doppelt so gross.',
           formel(r'\fc{R} \sim l', ein=1.0),
           graf_rl([{'bewegung': [[0, 0.1, 0]], 'farbe': 3, 'laeufer': {'bahn': [[1.2, 20], [3.4, 40]], 'text': 'R = {y} Ω', 'farbe': 5}}])),
        sz('Frage 2', 'Doppelter Querschnitt, halber Widerstand. Die Gerade wird flacher.',
           formel(r'\fc{R} \sim \dfrac{1}{A}', ein=1.0),
           graf_rl([{'bewegung': [[1.0, 0.1, 0], [3.2, 0.05, 0]], 'farbe': 3, 'marken': [{'x': 40, 'text': 'R = {y} Ω', 'farbe': 5}]}])),
        sz('Frage 3', 'Achtzig Meter Leiter, hin und zurück. Null Komma null zwei acht mal achtzig durch zwei Komma fünf: rund null Komma neun Ohm.',
           formel(r'\fc{R} = 0.028\;\dfrac{\Omega\,\text{mm}^2}{\text{m}} \cdot \dfrac{80\;\text{m}}{2.5\;\text{mm}^2} \approx 0.90\;\Omega', g=38, ein=1.0)),
        sz('Frage 4', 'Widerstand gleich Spannung durch Stromstärke: zwölf durch null Komma zwei, sechzig Ohm.',
           formel(r'\fc{R} = \dfrac{\fa{U}}{\fb{I}} = \dfrac{\fa{12\;\text{V}}}{\fb{0.2\;\text{A}}} = \fc{60\;\Omega}', ein=1.0)),
        sz('Frage 5', 'Ohmsch heisst: Der Widerstand bleibt gleich. Bei der Glühlampe wächst er mit der Temperatur, sie ist nicht ohmsch.',
           formel(r'\dfrac{\fa{U}}{\fb{I}} \text{ nicht konstant}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Draht wird doppelt so lang, Material und Querschnitt bleiben. Sein Widerstand …',
             ['verdoppelt sich', 'halbiert sich', 'bleibt gleich'],
             {1: 'Mehr Weg heisst mehr Widerstand, nicht weniger.', 2: 'Die Länge steht in R = ρ · l / A im Zähler.'},
             rueck_sprich={2: 'Die Länge steht in der Formel im Zähler.'}),
        wahl('Frage 2', 'Derselbe Draht bekommt den doppelten Querschnitt. Sein Widerstand …',
             ['halbiert sich', 'verdoppelt sich', 'bleibt gleich'],
             {1: 'Der Querschnitt steht im Nenner: Mehr Platz für den Strom, weniger Widerstand.', 2: 'A steht in R = ρ · l / A im Nenner.'},
             rueck_sprich={2: 'A steht in der Formel im Nenner.'}),
        wahl('Frage 3', 'Ein Aluminiumkabel ist 40 m lang und hat zwei Adern zu 2.5 mm² (ρ = 0.028 Ω·mm²/m). Widerstand der Leitung?',
             ['0.90 Ω', '0.45 Ω', '5.6 Ω'],
             {1: 'Hin und zurück: Die Leiterlänge ist 80 m.', 2: 'Durch den Querschnitt teilen, nicht malnehmen.'},
             sprich='Ein Aluminiumkabel ist vierzig Meter lang und hat zwei Adern zu je zwei Komma fünf Quadratmillimetern. Wie gross ist der Widerstand der Leitung?',
             rueck_sprich={1: 'Hin und zurück: Die Leiterlänge ist achtzig Meter.'}),
        wahl('Frage 4', 'An einem Widerstand liegen 12 V, es fliessen 0.2 A. Wie gross ist er?', ['60 Ω', '2.4 Ω', '0.017 Ω'],
             {1: 'Mal statt geteilt: R = U / I.', 2: 'Umgekehrt: Spannung durch Stromstärke.'},
             sprich='An einem Widerstand liegen zwölf Volt, es fliessen null Komma zwei Ampere. Wie gross ist er?',
             rueck_sprich={1: 'Mal statt geteilt: R gleich U durch I.'}),
        wahl('Frage 5', 'Bei einer Glühlampe ist U/I bei 2 V kleiner als bei 12 V. Ist sie ein ohmsches Bauteil?', ['nein', 'ja'],
             {1: 'Ohmsch heisst: R bleibt gleich. Hier wächst R mit der Temperatur.'},
             sprich='Bei einer Glühlampe ist U durch I bei zwei Volt kleiner als bei zwölf Volt. Ist sie ein ohmsches Bauteil?'),
    ]))

# ================================================================== Kapitel 4
DREH.append(dict(KOPF, titel='Strom sehen: Reihe teilt die Spannung, parallel den Strom', dateiname='p6-2-lp-schaltungen',
    kurzbeschrieb='Zwei Widerstände an 12 V: in Reihe derselbe Strom und geteilte Spannung, parallel dieselbe Spannung und geteilter Strom.',
    schlagworte=['Reihenschaltung', 'Parallelschaltung', 'Gesamtwiderstand', 'Spannungsteiler', 'Stromteiler'],
    _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 4; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('In Reihe', 'Zwei Widerstände in Reihe an zwölf Volt. Der Strom hat nur einen Weg, er ist überall gleich. Die Widerstände addieren sich: dreihundertzwanzig Ohm, also siebenunddreissig Komma fünf Milliampere.',
           formel(r'R_\text{ges} = R_1 + R_2 = 320\;\Omega', g=50),
           formel(r'\fb{I} = \dfrac{\fa{12\;\text{V}}}{320\;\Omega} = \fb{37.5\;\text{mA}}', y=420, g=50, ein=6.0),
           notiz('ein Weg:|derselbe Strom überall', y=600, ein=3.0),
           bild('p6-2-lp-schaltungen-1.jpg', y=240)),
        sz('Spannung teilt sich', 'Die zwölf Volt teilen sich auf: drei Komma sieben fünf Volt über hundert Ohm, acht Komma zwei fünf Volt über zweihundertzwanzig Ohm. Über dem grösseren Widerstand liegt die grössere Spannung.',
           formel(r'\fa{U_1} = \fb{I} \cdot R_1 = 3.75\;\text{V}', g=50),
           formel(r'\fa{U_2} = \fb{I} \cdot R_2 = 8.25\;\text{V}', y=420, g=50, ein=3.0),
           notiz('grösserer Widerstand:|grössere Spannung', y=600, ein=6.0),
           bild('p6-2-lp-schaltungen-1.jpg', y=240)),
        sz('Doppelt so gross', 'Ist R zwei doppelt so gross wie R eins, liegt dort doppelt so viel Spannung: vier und acht Volt.',
           formel(r'\fa{U_1} : \fa{U_2} = R_1 : R_2 = 1 : 2'),
           bild('p6-2-lp-schaltungen-2.jpg', y=240)),
        sz('Parallel', 'Jetzt parallel. Beide Widerstände liegen an den vollen zwölf Volt. Der Strom teilt sich: hundertzwanzig Milliampere durch hundert Ohm, vierundfünfzig Komma fünf durch zweihundertzwanzig. Durch den kleineren fliesst mehr.',
           formel(r'\fb{I_1} = \dfrac{\fa{12\;\text{V}}}{100\;\Omega} = 120\;\text{mA}', g=48),
           formel(r'\fb{I_2} = \dfrac{\fa{12\;\text{V}}}{220\;\Omega} \approx 54.5\;\text{mA}', y=440, g=48, ein=6.0),
           notiz('dieselbe Spannung an beiden', y=620, ein=2.0),
           bild('p6-2-lp-schaltungen-3.jpg', y=240)),
        sz('Gesamtwiderstand parallel', 'Bei der Parallelschaltung addieren sich die Kehrwerte. Zwei gleiche Widerstände von hundert Ohm ergeben fünfzig Ohm, weniger als jeder einzelne. Der Strom hat zwei Wege.',
           formel(r'\dfrac{1}{R_\text{ges}} = \dfrac{1}{R_1} + \dfrac{1}{R_2}', g=50),
           formel(r'R_\text{ges} = \dfrac{100\;\Omega}{2} = 50\;\Omega', y=450, g=50, ein=4.5),
           notiz('kleiner als der kleinste', y=620, ein=6.5),
           bild('p6-2-lp-schaltungen-4.jpg', y=240)),
        sz('Merke', 'Zum Mitnehmen: In Reihe ist der Strom gleich, die Spannung teilt sich, die Widerstände addieren sich. Parallel ist die Spannung gleich, der Strom teilt sich, und die Kehrwerte addieren sich.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'R_\text{ges} = R_1 + R_2 \qquad \dfrac{1}{R_\text{ges}} = \dfrac{1}{R_1} + \dfrac{1}{R_2}', y=420, g=46, ein=0.4),
           notiz('Reihe: gleicher Strom, Spannung teilt sich|parallel: gleiche Spannung, Strom teilt sich', y=580, ein=1.2, g=42)),
        JETZT,
    ]))

DREH.append(dict(KOPF, titel='Strom sehen: Kontrollfragen zu Reihe und parallel', dateiname='p6-2-lp-kontrolle-schaltungen',
    kurzbeschrieb='Fünf Fragen zu Strom, Spannungsteilung und Gesamtwiderstand in Reihen- und Parallelschaltungen.',
    schlagworte=['Reihenschaltung', 'Parallelschaltung', 'Gesamtwiderstand', 'Kontrollfragen'],
    _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 4; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Frage 1', 'In Reihe addieren sich die Widerstände: dreihundert Ohm. Zwölf Volt durch dreihundert Ohm, vierzig Milliampere.',
           formel(r'\fb{I} = \dfrac{\fa{12\;\text{V}}}{300\;\Omega} = \fb{40\;\text{mA}}', ein=1.0),
           bild('p6-2-lp-schaltungen-2.jpg', y=240, ein=1.0)),
        sz('Frage 2', 'Derselbe Strom durch beide: Über zweihundert Ohm liegt doppelt so viel Spannung, acht Volt gegen vier.',
           formel(r'\fa{U_1} = 4\;\text{V} \qquad \fa{U_2} = 8\;\text{V}', ein=1.0),
           bild('p6-2-lp-schaltungen-2.jpg', y=240, ein=1.0)),
        sz('Frage 3', 'Zwei gleiche parallel: die Hälfte, fünfzig Ohm.',
           formel(r'R_\text{ges} = \dfrac{100\;\Omega}{2} = 50\;\Omega', ein=1.0),
           bild('p6-2-lp-schaltungen-4.jpg', y=240, ein=1.0)),
        sz('Frage 4', 'Beide liegen an derselben Spannung. Durch den kleineren Widerstand fliesst mehr: hundertzwanzig gegen vierundfünfzig Komma fünf Milliampere.',
           formel(r'\fb{I_1} = 120\;\text{mA} \qquad \fb{I_2} \approx 54.5\;\text{mA}', ein=1.0),
           bild('p6-2-lp-schaltungen-3.jpg', y=240, ein=1.0)),
        sz('Frage 5', 'Ein weiterer Zweig ist ein weiterer Weg. Der Gesamtwiderstand sinkt, der Gesamtstrom steigt.',
           formel(r'R_\text{ges}\ \text{sinkt} \;\Longrightarrow\; \fb{I} = \dfrac{\fa{U}}{R_\text{ges}}\ \text{steigt}', g=46, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', '100 Ω und 200 Ω liegen in Reihe an 12 V. Welcher Strom fliesst?', ['40 mA', '180 mA', '120 mA'],
             {1: 'Das wäre parallel. In Reihe addieren sich die Widerstände.', 2: 'Das wäre der Strom durch 100 Ω allein.'},
             sprich='Hundert Ohm und zweihundert Ohm liegen in Reihe an zwölf Volt. Welcher Strom fliesst?',
             rueck_sprich={2: 'Das wäre der Strom durch hundert Ohm allein.'}),
        wahl('Frage 2', 'In dieser Reihenschaltung: Wo liegt die grössere Spannung?', ['über 200 Ω', 'über 100 Ω', 'über beiden gleich viel'],
             {1: 'Gleicher Strom: Je grösser R, desto grösser U = R · I.', 2: 'Gleich viel nur bei gleichen Widerständen.'},
             sprich='In dieser Reihenschaltung: Wo liegt die grössere Spannung?',
             rueck_sprich={1: 'Gleicher Strom: Je grösser R, desto grösser die Spannung.'}),
        wahl('Frage 3', 'Zwei Widerstände von je 100 Ω liegen parallel. Wie gross ist der Gesamtwiderstand?', ['50 Ω', '200 Ω', '100 Ω'],
             {1: 'Das wäre die Reihe. Parallel hat der Strom zwei Wege.', 2: 'Der Gesamtwiderstand ist kleiner als der kleinste.'},
             sprich='Zwei Widerstände von je hundert Ohm liegen parallel. Wie gross ist der Gesamtwiderstand?'),
        wahl('Frage 4', 'Parallel an 12 V: 100 Ω und 220 Ω. Durch welchen fliesst mehr Strom?', ['durch 100 Ω', 'durch 220 Ω', 'durch beide gleich viel'],
             {1: 'Beide haben dieselbe Spannung. Der grössere Widerstand lässt weniger durch.', 2: 'Gleich viel nur bei gleichen Widerständen.'},
             sprich='Parallel an zwölf Volt: hundert Ohm und zweihundertzwanzig Ohm. Durch welchen fliesst mehr Strom?'),
        wahl('Frage 5', 'Ein dritter Widerstand wird parallel dazugeschaltet. Was macht der Gesamtstrom?', ['er steigt', 'er sinkt', 'er bleibt gleich'],
             {1: 'Ein weiterer Weg senkt den Gesamtwiderstand.', 2: 'Die anderen Zweige bleiben, und es kommt einer dazu.'}),
    ]))

# ================================================================== Kapitel 5
DREH.append(dict(KOPF, titel='Strom sehen: wer misst was, wer trennt wann', dateiname='p6-2-lp-gefahren',
    kurzbeschrieb='Körperstrom, FI-Schutzschalter, Schutzleiter und Leitungsschutzschalter an vier Fällen: normal, Mensch am Gehäuse, Schutzleiter, Kurzschluss.',
    schlagworte=['Körperstrom', 'FI-Schutzschalter', 'Schutzleiter', 'Leitungsschutzschalter', 'Kurzschluss'],
    _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 5; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Gefahr', 'Nerven, Muskeln und Herz arbeiten mit elektrischen Impulsen. Gefährlich ist der Strom durch den Körper: zweihundertdreissig Volt an tausend Ohm nasser Haut geben zweihundertdreissig Milliampere. Lebensgefährlich.',
           titel('Warum ist Strom gefährlich?', g=72),
           formel(r'\fb{I_\text{K}} = \dfrac{\fa{U}}{R_\text{K}} = \dfrac{\fa{230\;\text{V}}}{1000\;\Omega} = \fb{230\;\text{mA}}', y=440, g=46, ein=5.0),
           notiz('Muskeln verkrampfen,|das Herz kann flimmern.', y=620, farbe='rot', ein=2.0)),
        sz('Normalbetrieb', 'Im Normalbetrieb fliesst durch den Aussenleiter gleich viel Strom hin wie durch den Neutralleiter zurück. Der FI-Schutzschalter vergleicht die beiden: keine Differenz, er bleibt ein.',
           formel(r'\fb{I_\text{L}} = \fb{I_\text{N}}'),
           notiz('Der FI vergleicht|hin und zurück.', ein=4.0),
           bild('p6-2-lp-gefahren-1.jpg', y=240)),
        sz('Mensch am Gehäuse', 'Fehlt der Schutzleiter, und jemand fasst ans defekte Gehäuse, fliesst ein Teil des Stroms über den Körper zur Erde. Er fehlt auf dem Rückweg. Der FI sieht zweihundertdreissig Milliampere Differenz und trennt in höchstens vierzig Millisekunden. Der Leitungsschutzschalter merkt davon nichts.',
           formel(r'\Delta \fb{I} = 230\;\text{mA} \gt 30\;\text{mA}'),
           notiz('FI trennt in höchstens 40 ms.|Der LS merkt nichts.', ein=8.0),
           bild('p6-2-lp-gefahren-2.jpg', y=240)),
        sz('Schutzleiter', 'Mit Schutzleiter fliesst der Fehlerstrom über ihn zur Erde, rund hundertfünfzehn Ampere. Das ist so viel, dass der Leitungsschutzschalter sofort trennt, und der FI ebenfalls.',
           formel(r'\fb{I_\text{F}} = \dfrac{\fa{230\;\text{V}}}{2\;\Omega} = \fb{115\;\text{A}}', g=50),
           notiz('Der Schutzleiter leitet ab,|die Schalter trennen.', ein=4.0),
           bild('p6-2-lp-gefahren-3.jpg', y=240)),
        sz('Kurzschluss', 'Beim Kurzschluss zwischen Aussen- und Neutralleiter fliesst ein riesiger Strom, aber alles kommt zurück. Keine Differenz, der FI bleibt ein. Hier schützt der Leitungsschutzschalter die Leitung.',
           formel(r'\fb{I_\text{Kurz}} = \dfrac{\fa{230\;\text{V}}}{0.5\;\Omega} = \fb{460\;\text{A}}', g=50),
           notiz('keine Differenz:|nur der LS trennt', ein=4.5),
           bild('p6-2-lp-gefahren-4.jpg', y=240)),
        sz('Merke', 'Zum Mitnehmen: Der FI schützt Menschen, weil er Hin- und Rückstrom vergleicht. Der Schutzleiter leitet den Fehlerstrom ab. Der Leitungsschutzschalter schützt die Leitung. Und dreissig Milliampere sind keine Grenze für ungefährlichen Strom.',
           titel('Zum Mitnehmen', y=260, g=76),
           notiz('FI: vergleicht, schützt Menschen|Schutzleiter: leitet zur Erde ab|LS: schützt die Leitung', y=400, ein=0.4, g=44),
           notiz('30 mA ist keine Grenze|für ungefährlichen Strom.', y=640, farbe='rot', ein=10.0, g=44)),
        JETZT,
    ]))

DREH.append(dict(KOPF, titel='Strom sehen: Kontrollfragen zu Gefahren und Schutz', dateiname='p6-2-lp-kontrolle-gefahren',
    kurzbeschrieb='Fünf Fragen zu Körperstrom, Leitungsschutzschalter, FI, Schutzleiter und der 30-mA-Schwelle.',
    schlagworte=['Körperstrom', 'FI-Schutzschalter', 'Schutzleiter', 'Leitungsschutzschalter', 'Kontrollfragen'],
    _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 5; gehört dorthin, nicht in die Clip-Bibliothek.',
    szenen=[
        sz('Frage 1', 'Zweihundertdreissig Volt durch zweitausend Ohm: hundertfünfzehn Milliampere, weit im gefährlichen Bereich.',
           formel(r'\fb{I_\text{K}} = \dfrac{\fa{230\;\text{V}}}{2000\;\Omega} = \fb{115\;\text{mA}}', g=50, ein=1.0),
           bild('p6-2-lp-gefahren-k2.jpg', y=240, ein=1.0)),
        sz('Frage 2', 'Hundertfünfzehn Milliampere sind weniger als ein Hundertstel von dreizehn Ampere. Der Leitungsschutzschalter merkt nichts.',
           formel(r'0.115\;\text{A} \ll 13\;\text{A}', ein=1.0)),
        sz('Frage 3', 'Beim Kurzschluss kommt der ganze Strom zurück. Keine Differenz: Der FI bleibt ein, der Leitungsschutzschalter trennt.',
           formel(r'\fb{I_\text{L}} = \fb{I_\text{N}} \approx 469\;\text{A}', ein=1.0),
           bild('p6-2-lp-gefahren-4.jpg', y=240, ein=1.0)),
        sz('Frage 4', 'Der Fehlerstrom fliesst über den Schutzleiter, rund hundertfünfzehn Ampere. Der Leitungsschutzschalter trennt sofort, der FI ebenfalls.',
           formel(r'\fb{I_\text{F}} \approx 115\;\text{A}', ein=1.0),
           bild('p6-2-lp-gefahren-3.jpg', y=240, ein=1.0)),
        sz('Frage 5', 'Dreissig Milliampere sind die Auslöseschwelle des FI, keine Grenze für ungefährlichen Strom. Auch zwanzig Milliampere können gefährlich sein.',
           notiz('Der FI ist zusätzlicher Schutz,|keine Garantie.', y=320, farbe='rot', ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Jemand mit trockener Haut (2 kΩ) berührt 230 V. Wie gross ist der Körperstrom?', ['115 mA', '460 A', '0.115 mA'],
             {1: 'Mal statt geteilt: I = U / R.', 2: '115 mA sind 0.115 A. Die Einheit im Blick behalten.'},
             sprich='Jemand mit trockener Haut, zwei Kiloohm, berührt zweihundertdreissig Volt. Wie gross ist der Körperstrom?',
             rueck_sprich={1: 'Mal statt geteilt: I gleich U durch R.', 2: 'Hundertfünfzehn Milliampere sind null Komma eins eins fünf Ampere. Die Einheit im Blick behalten.'}),
        wahl('Frage 2', 'Bei 115 mA durch den Körper: Löst ein 13-A-Leitungsschutzschalter aus?', ['nein', 'ja'],
             {1: '115 mA sind weniger als ein Hundertstel von 13 A. Der LS merkt nichts.'},
             sprich='Bei hundertfünfzehn Milliampere durch den Körper: Löst ein Dreizehn-Ampere-Leitungsschutzschalter aus?',
             rueck_sprich={1: 'Hundertfünfzehn Milliampere sind weniger als ein Hundertstel von dreizehn Ampere. Der Leitungsschutzschalter merkt nichts.'}),
        wahl('Frage 3', 'Aussen- und Neutralleiter berühren sich direkt. Wer trennt?', ['der Leitungsschutzschalter', 'der FI', 'beide'],
             {1: 'Der FI vergleicht hin und zurück. Beim Kurzschluss kommt alles zurück.', 2: 'Der FI sieht keine Differenz, er bleibt ein.'}),
        wahl('Frage 4', 'Ein Metallgehäuse mit Schutzleiter bekommt Kontakt zum Aussenleiter. Was geschieht?',
             ['Fehlerstrom über den Schutzleiter, die Schalter trennen sofort', 'nichts, der Schutzleiter hält die Spannung weg', 'nur der FI trennt, der LS bleibt ein'],
             {1: 'Der Schutzleiter schaltet nichts ab. Er führt den Fehlerstrom, und der ist so gross, dass abgeschaltet wird.', 2: 'Rund 115 A: Auch der Leitungsschutzschalter trennt sofort.'},
             rueck_sprich={2: 'Rund hundertfünfzehn Ampere: Auch der Leitungsschutzschalter trennt sofort.'}),
        wahl('Frage 5', 'Der FI löst ab 30 mA aus. Sind 20 mA durch den Körper also harmlos?', ['nein', 'ja'],
             {1: '30 mA ist die Auslöseschwelle des FI, keine Grenze für ungefährlichen Strom.'},
             sprich='Der FI löst ab dreissig Milliampere aus. Sind zwanzig Milliampere durch den Körper also harmlos?',
             rueck_sprich={1: 'Dreissig Milliampere sind die Auslöseschwelle des FI, keine Grenze für ungefährlichen Strom.'}),
    ]))

for d in DREH:
    pfad = os.path.join(CLIPS, d['dateiname'] + '.json')
    if os.path.exists(pfad) and not NEU:
        print('  bleibt  ', d['dateiname'])
        continue
    with open(pfad, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('  geschrieben', d['dateiname'], len(d['szenen']), 'Szenen', len(d.get('fragen', [])), 'Fragen')
