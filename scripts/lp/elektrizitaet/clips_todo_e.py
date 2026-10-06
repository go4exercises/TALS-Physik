"""Leitprogramm Elektrizität, Clips nach TODO-E (06.10.2026): vorgerechnete Probleme mit Strategiefrage in den
Einführungsclips der Kapitel 1, 2, 3, 5, 7 und vier neue Clips für die Kapitel 4 und 6.
ARCHIV — nicht mehr laufen lassen: Seit der Visualisierung vom 06.10.2026 sind die Drehbücher die Quelle.
Früher wiederholbar: Szenen
mit Namen «Problem …», «Vorgehen …», «Lösung …» werden vor dem Einfügen entfernt. Elemente mit «_anker»
bekommen nach der Vertonung ihr «ein» (scripts/lp/kinematik/anker.py)."""
import json, math, os

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'clips') + os.sep
FARBE = {'U': 1, 'I': 2, 'R': 3}            # wie im Leitprogramm: U Bernstein, I Orange, R Grün; 5 Tinte, 4 Rot


def lade(n):
    return json.load(open(R + n + '.json'))


def speichere(n, d):
    with open(R + n + '.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def sz(name, sprecher, *el):
    return {"name": name, "layout": "zentriert", "oben": 200, "sprecher": sprecher, "elemente": list(el)}


def formel(t, y, g=44, anker=None, ein=0.8):
    e = {"typ": "formel", "text": t, "x": 150, "y": y, "breite": 820, "groesse": g, "ein": ein}
    if anker: e['_anker'] = anker
    return e


def notiz(t, y, anker=None, ein=1.0, g=44, farbe='tinte'):
    e = {"typ": "notiz", "text": t, "x": 150, "y": y, "breite": 820, "groesse": g, "farbe": farbe, "ein": ein}
    if anker: e['_anker'] = anker
    return e


def titel(t, y=260, g=64):
    return {"typ": "titel", "text": t, "x": 150, "y": y, "breite": 820, "groesse": g}


def graf(xb, yb, xt=(), yt=(), xname='', yname='', anker=None, ein=0.05, achsen=True, **kw):
    g = {"typ": "graf", "x": 1010, "y": 175, "breite": 760, "hoehe": 760, "abstand": 0, "anim": "fade", "ein": ein,
         "pfeile": achsen, "xbereich": list(xb), "ybereich": list(yb),
         "xteilung": [[v, ('%g' % v)] for v in xt] or [[1e9, '']], "yteilung": [[v, ('%g' % v)] for v in yt] or [[1e9, '']],
         "xname": xname, "yname": yname}
    if not achsen: g['achsen'] = False
    g.update(kw)
    if anker: g['_anker'] = anker
    return g


def kreis(cx, cy, r, farbe=5, dicke=4):
    return [{"formel": "%g%+g*sqrt(abs(%g-(x-(%g))*(x-(%g))))" % (cy, vz, r * r, cx, cx), "von": cx - r, "bis": cx + r,
             "farbe": farbe, "dicke": dicke, "n": 400} for vz in (1, -1)]


# ---------------------------------------------------------------- Schaltskizzen im Fenster 0..10 x 0..10
def draht(pts, farbe=5, dicke=4):
    return [{"von": list(a), "bis": list(b), "farbe": farbe, "dicke": dicke} for a, b in zip(pts, pts[1:])]


def widerstand(x1, y1, x2, y2, text=None, bei=None, anker='middle', farbe=3):
    s = draht([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], farbe=5, dicke=4)
    f = [{"punkte": [[x1, y1], [x2, y1], [x2, y2], [x1, y2]], "farbe": farbe, "deckung": 0.10}]
    t = [{"bei": bei, "text": text, "farbe": 5, "groesse": 28, "anker": anker}] if text else []
    return s, f, t


def quelle(x, ym, text=None):
    """Batterie senkrecht bei x: langer Strich (+) oben bei ym+0.2, kurzer dicker darunter."""
    s = [{"von": [x - 0.55, ym + 0.2], "bis": [x + 0.55, ym + 0.2], "farbe": 5, "dicke": 4},
         {"von": [x - 0.28, ym - 0.2], "bis": [x + 0.28, ym - 0.2], "farbe": 5, "dicke": 10}]
    t = [{"bei": [x + 0.75, ym - 0.15], "text": text, "farbe": 1, "groesse": 28}] if text else []
    return s, t


def messgeraet(x, y, b, r=0.55):
    return kreis(x, y, r, farbe=5, dicke=4), [{"bei": [x, y - 0.22], "text": b, "farbe": 5, "groesse": 30, "anker": "middle"}]


def schaltbild(teile, **kw):
    """Beliebig verschachtelte Listen von Strecken, Flächen, Texten und Kurven einsammeln."""
    s, f, t, k = [], [], [], []
    def sammle(x):
        if isinstance(x, (list, tuple)):
            for y in x: sammle(y)
        elif isinstance(x, dict):
            if 'formel' in x: k.append(x)
            elif 'punkte' in x: f.append(x)
            elif 'von' in x: s.append(x)
            else: t.append(x)
    sammle(teile)
    return dict(strecken=s, flaechen=f, texte=t, kurven=k, **kw)


def ohne(d, namen):
    d['szenen'] = [s for s in d['szenen'] if not any(s['name'].startswith(n) for n in namen)]


def vor_merke(d, neue):
    i = [k for k, s in enumerate(d['szenen']) if s['name'] == 'Merke'][0]
    d['szenen'][i:i] = neue


def frage(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None):
    f = {"szene": szene, "bei": 0.3, "typ": "wahl", "text": text, "optionen": opt, "richtig": richtig, "rueck": {str(k): v for k, v in rueck.items()}}
    if sprich: f['sprich'] = sprich
    if rueck_sprich: f['rueck_sprich'] = {str(k): v for k, v in rueck_sprich.items()}
    return f


def setze_fragen(d, neue):
    namen = {f['szene'] for f in neue}
    d['fragen'] = [f for f in d.get('fragen', []) if f['szene'] not in namen] + neue
    if not d['fragen']: d.pop('fragen')


PROB = ('Problem', 'Vorgehen', 'Lösung')

# ===================================================================== Kapitel 1: Ladung
d = lade('p6-2-lp-ladung'); ohne(d, PROB)
stab = schaltbild([[draht([(2, 5.4), (8, 5.4), (8, 4.6), (2, 4.6), (2, 5.4)], dicke=5)],
                   [[{"punkte": [[2, 4.6], [8, 4.6], [8, 5.4], [2, 5.4]], "farbe": 4, "deckung": 0.12}]],
                   [[{"bei": [2.6 + 0.9 * i, 4.85], "text": "+", "farbe": 4, "groesse": 40, "anker": "middle"} for i in range(6)]],
                   [[{"bei": [5, 3.4], "text": "Glasstab: Q = +3.2 nC", "farbe": 5, "groesse": 30, "anker": "middle"}]]])
vor_merke(d, [
    sz('Problem Ladung', 'Jetzt ein ganzes Problem. Ein Glasstab wurde mit einem Seidentuch gerieben und trägt nun plus drei Komma zwei Nanocoulomb. Hat er Elektronen zu viel oder zu wenig, und wie viele?',
       formel(r'Q = +3.2\;\text{nC}', 300, g=50, anker='trägt nun plus'),
       notiz('zu viel oder zu wenig?|wie viele Elektronen?', 440, anker='Hat er Elektronen'),
       graf((0, 10), (0, 10), achsen=False, anker='Ein Glasstab', **stab)),
    sz('Vorgehen Ladung', 'Der Reihe nach: Zuerst das Vorzeichen deuten. Dann Nanocoulomb in Coulomb umrechnen, durch die Elementarladung teilen und am Schluss die Grössenordnung prüfen.',
       notiz('1. Vorzeichen deuten|2. nC in C umrechnen|3. durch e teilen|4. Grössenordnung prüfen', 300, anker='Zuerst das Vorzeichen')),
    sz('Lösung Ladung', 'Plus heisst: Dem Stab fehlen Elektronen. Drei Komma zwei Nanocoulomb sind drei Komma zwei mal zehn hoch minus neun Coulomb. Geteilt durch die Elementarladung ergibt das rund zwei mal zehn hoch zehn: So viele Elektronen fehlen. Probe: Coulomb durch Coulomb gibt eine reine Anzahl, und schon eine winzige Ladung sind Milliarden Elektronen.',
       notiz('plus: Elektronenmangel', 300, anker='Plus heisst'),
       formel(r'|Q| = 3.2\;\text{nC} = 3.2 \cdot 10^{-9}\;\text{C}', 420, g=42, anker='Drei Komma zwei Nanocoulomb'),
       formel(r'n = \dfrac{|Q|}{e} = \dfrac{3.2 \cdot 10^{-9}\;\text{C}}{1.602 \cdot 10^{-19}\;\text{C}} \approx 2.0 \cdot 10^{10}', 560, g=40, anker='Geteilt durch die Elementarladung'),
       graf((0, 10), (0, 10), achsen=False, **stab)),
])
setze_fragen(d, [frage('Vorgehen Ladung', 'Der Stab trägt +3.2 nC. Womit beginnst du?',
    ['3.2 mit 1.602 multiplizieren', 'mit dem Vorzeichen: Was heisst «plus»?', 'die Ladung durch eine Zeit teilen'], 1,
    {0: 'Die Frage hat zwei Teile. Welcher lässt sich ohne Rechnung beantworten?', 2: 'Hier fliesst kein Strom: Gefragt ist die Ladung, die auf dem Stab sitzt.'},
    sprich='Der Stab trägt plus drei Komma zwei Nanocoulomb. Womit beginnst du?',
    rueck_sprich={0: 'Die Frage hat zwei Teile. Welcher lässt sich ohne Rechnung beantworten?', 2: 'Hier fliesst kein Strom. Gefragt ist die Ladung, die auf dem Stab sitzt.'})])
d['kurzbeschrieb'] = 'Woher Ladung kommt, was die Elementarladung ist, warum die Stromstärke die Steigung im Q-t-Diagramm ist — und ein vorgerechnetes Problem: Elektronenmangel eines Glasstabs.'
speichere('p6-2-lp-ladung', d)

# ===================================================================== Kapitel 2: Leistung und Energie
d = lade('p6-2-lp-leistung'); ohne(d, PROB)
pt = dict(flaechen=[{"punkte": [[0, 0], [0, 1.5], [1 / 3, 1.5], [1 / 3, 0]], "farbe": 1, "deckung": 0.28, "beschriftung": "0.5 kWh", "beschriftung_bei": [1 / 6, 0.65]}],
          strecken=[{"von": [0, 1.5], "bis": [1 / 3, 1.5], "farbe": 1, "dicke": 5}, {"von": [1 / 3, 1.5], "bis": [1 / 3, 0], "farbe": 5, "dicke": 3, "gestrichelt": True}],
          texte=[{"bei": [0.36, 1.58], "text": "1.5 kW während 1/3 h", "farbe": 5, "groesse": 26}])
vor_merke(d, [
    sz('Problem Heizgerät', 'Jetzt ein ganzes Problem. Ein Heizgerät, das wie ein Widerstand wirkt, nimmt am Netz fünfzehnhundert Watt auf und läuft zwanzig Minuten. Welcher Strom fliesst, wie viel Energie wird umgesetzt, und was kostet das bei null Komma zwei fünf Franken pro Kilowattstunde?',
       notiz('Heizgerät: 1500 W an 230 V|läuft 20 min|Preis: 0.25 CHF/kWh', 300, anker='Ein Heizgerät'),
       notiz('gesucht: Strom, Energie, Kosten', 520, anker='Welcher Strom')),
    sz('Vorgehen Heizgerät', 'Für die Energie in Kilowattstunden zuerst umrechnen: fünfzehnhundert Watt sind eins Komma fünf Kilowatt, zwanzig Minuten sind ein Drittel Stunde. Den Strom liefert P gleich U mal I, umgestellt nach I. Am Schluss Energie mal Preis.',
       formel(r'1500\;\text{W} = 1.5\;\text{kW} \qquad 20\;\text{min} = \tfrac13\;\text{h}', 300, g=42, anker='fünfzehnhundert Watt sind'),
       formel(r'\fb{I} = \dfrac{P}{U} \qquad \text{(aus } P = U \cdot \fb{I}\text{)}', 440, g=42, anker='Den Strom liefert')),
    sz('Lösung Heizgerät', 'Der Strom: fünfzehnhundert Watt durch zweihundertdreissig Volt, rund sechs Komma fünf zwei Ampere. Die Energie: eins Komma fünf Kilowatt mal ein Drittel Stunde, null Komma fünf Kilowattstunden — die Fläche des Rechtecks. Die Kosten: null Komma fünf Kilowattstunden mal null Komma zwei fünf Franken pro Kilowattstunde, rund zwölf Komma fünf Rappen. Probe: Kilowatt mal Stunde ist Kilowattstunde.',
       formel(r'\fb{I} = \dfrac{P}{\fa{U}} = \dfrac{1500\;\text{W}}{\fa{230\;\text{V}}} \approx \fb{6.52\;\text{A}}', 290, g=40, anker='Der Strom'),
       formel(r'E = P \cdot t = 1.5\;\text{kW} \cdot \tfrac13\;\text{h} = 0.5\;\text{kWh}', 420, g=40, anker='Die Energie'),
       formel(r'\text{Kosten} = 0.5\;\text{kWh} \cdot 0.25\;\text{CHF/kWh} \approx 0.13\;\text{CHF}', 550, g=32, anker='Die Kosten'),
       graf((-0.07, 0.62), (-0.2, 2.15), (0.2, 0.4, 0.6), (0.5, 1, 1.5, 2), 't [h]', 'P [kW]', anker='Die Energie', **pt)),
])
setze_fragen(d, [frage('Vorgehen Heizgerät', 'Bevor du E = P · t rechnest: Was tust du zuerst?',
    ['1500 mit 20 multiplizieren', 'P durch U teilen und mit t multiplizieren', 'auf Kilowatt und Stunden umrechnen'], 2,
    {0: 'Welche Einheit hätte das Ergebnis? Auf der Rechnung stehen Kilowattstunden.', 1: 'P durch U gibt den Strom. Strom mal Zeit ist eine Ladung, keine Energie.'},
    sprich='Bevor du E gleich P mal t rechnest: Was tust du zuerst?',
    rueck_sprich={0: 'Welche Einheit hätte das Ergebnis? Auf der Rechnung stehen Kilowattstunden.', 1: 'P durch U gibt den Strom. Strom mal Zeit ist eine Ladung, keine Energie.'})])
d['kurzbeschrieb'] = 'Spannung als Energie je Ladung, Leistung als Höhe und Energie als Fläche im P-t-Diagramm — und ein vorgerechnetes Problem: Strom, Energie und Kosten eines Heizgeräts.'
speichere('p6-2-lp-leistung', d)

# ===================================================================== Kapitel 3: Widerstand (die Szene «Zwei Adern» wird zum Problem)
d = lade('p6-2-lp-widerstand'); ohne(d, PROB + ('Zwei Adern',))
rl = dict(geraden=[], strecken=[{"von": [0, 0], "bis": [50, 0.017 * 50 / 1.5], "farbe": 3, "dicke": 5},
                               {"von": [0, 0], "bis": [50, 0.017 * 50 / 3], "farbe": 3, "dicke": 3, "gestrichelt": True},
                               {"von": [40, 0], "bis": [40, 0.017 * 40 / 1.5], "farbe": 5, "dicke": 3, "gestrichelt": True},
                               {"von": [0, 0.017 * 40 / 1.5], "bis": [40, 0.017 * 40 / 1.5], "farbe": 5, "dicke": 3, "gestrichelt": True}],
          punkte=[{"x": 40, "y": round(0.017 * 40 / 1.5, 4), "farbe": 3, "beschriftung": "(40 m; 0.453 Ω)", "beschriftung_bei": [38.5, 0.5], "anker": "end"}],
          texte=[{"bei": [51, 0.25], "text": "3 mm²", "farbe": 3, "groesse": 24, "anker": "end"}, {"bei": [48, 0.6], "text": "1.5 mm²", "farbe": 3, "groesse": 24, "anker": "end"}])
vor_merke(d, [
    sz('Problem Kabel', 'Vorsicht beim Kabel: Der Strom fliesst hin und zurück. Jetzt ein ganzes Problem. Ein Verlängerungskabel aus Kupfer ist zwanzig Meter lang, mit zwei Adern zu je eins Komma fünf Quadratmillimetern. Welchen Widerstand hat die Leitung?',
       notiz('Kupferkabel, 20 m lang|2 Adern, je 1.5 mm²|ρ = 0.017 Ω·mm²/m', 300, anker='Ein Verlängerungskabel'),
       notiz('gesucht: R der Leitung', 520, anker='Welchen Widerstand')),
    sz('Vorgehen Kabel', 'Der Strom fliesst durch die eine Ader hin und durch die andere zurück: Die Leiterlänge ist doppelt so gross wie das Kabel, vierzig Meter. Dann die Einheiten prüfen: rho in Ohm Quadratmillimeter pro Meter, l in Metern, A in Quadratmillimetern — sie passen zusammen.',
       formel(r'l = 2 \cdot 20\;\text{m} = 40\;\text{m}', 300, g=48, anker='Die Leiterlänge'),
       notiz('Einheiten: Ω·mm²/m · m / mm² = Ω', 450, anker='Dann die Einheiten')),
    sz('Lösung Kabel', 'R gleich rho mal l durch A: null Komma null eins sieben mal vierzig durch eins Komma fünf, rund null Komma vier fünf drei Ohm. Probe mit dem Querschnitt: Mit drei Quadratmillimetern wäre der Widerstand halb so gross, null Komma zwei zwei sieben Ohm.',
       formel(r'\fc{R} = \rho \cdot \dfrac{l}{A} = 0.017\;\dfrac{\Omega\,\text{mm}^2}{\text{m}} \cdot \dfrac{40\;\text{m}}{1.5\;\text{mm}^2} \approx \fc{0.453\;\Omega}', 300, g=31, anker='R gleich rho'),
       notiz('doppelter Querschnitt:|halber Widerstand, 0.227 Ω', 460, anker='Probe mit dem Querschnitt'),
       graf((-4, 54), (-0.08, 0.72), (10, 20, 30, 40, 50), (0.2, 0.4, 0.6), 'l [m]', 'R [Ω]', anker='R gleich rho', **rl)),
])
setze_fragen(d, [frage('Vorgehen Kabel', 'Welche Länge setzt du für l ein?', ['20 m', '40 m', '10 m'], 1,
    {0: 'Der Strom fliesst hin und zurück. Wie lang ist sein ganzer Weg im Kabel?', 2: 'Geteilt wird nichts: Beide Adern liegen im Stromweg.'},
    sprich='Welche Länge setzt du für l ein?',
    rueck_sprich={0: 'Der Strom fliesst hin und zurück. Wie lang ist sein ganzer Weg im Kabel?', 2: 'Geteilt wird nichts. Beide Adern liegen im Stromweg.'})])
d['kurzbeschrieb'] = 'Widerstand als U durch I, Länge, Querschnitt und Material eines Leiters — und ein vorgerechnetes Problem: der Widerstand eines Kupferkabels mit Hin- und Rückleiter.'
speichere('p6-2-lp-widerstand', d)

# ===================================================================== Kapitel 5: Reihe und parallel
d = lade('p6-2-lp-schaltungen'); ohne(d, PROB)
d['_probe'] = d['_probe'].replace('Kapitel 4;', 'Kapitel 5;')
s1, t1 = quelle(1.5, 5, '12 V')
r1 = widerstand(3.3, 7.6, 5.0, 8.4, 'R₁ = 270 Ω', [4.15, 8.8])
r2 = widerstand(6.3, 7.6, 8.0, 8.4, 'R₂ = 330 Ω', [7.15, 8.8])
reihe = schaltbild([[draht([(1.5, 5.2), (1.5, 8), (3.3, 8)]), draht([(5.0, 8), (6.3, 8)]), draht([(8.0, 8), (9, 8), (9, 2), (1.5, 2), (1.5, 4.8)])],
                    [s1], [t1], list(r1), list(r2)])
vor_merke(d, [
    sz('Problem Reihe', 'Jetzt ein ganzes Problem. Zweihundertsiebzig Ohm und dreihundertdreissig Ohm liegen in Reihe an zwölf Volt. Gesucht sind der Gesamtwiderstand, der Strom und die beiden Teilspannungen.',
       notiz('270 Ω und 330 Ω in Reihe|an 12 V', 300, anker='Zweihundertsiebzig Ohm'),
       notiz('gesucht: R ges, I, U₁, U₂', 460, anker='Gesucht sind'),
       graf((0, 10), (0, 10), achsen=False, anker='Zweihundertsiebzig Ohm', **reihe)),
    sz('Vorgehen Reihe', 'Zuerst die Widerstände addieren. Mit dem Gesamtwiderstand und den ganzen zwölf Volt folgt der Strom. Mit dem Strom die beiden Teilspannungen. Am Schluss prüfen, ob sie zusammen zwölf Volt ergeben.',
       notiz('1. R addieren|2. Strom aus der ganzen Spannung|3. Teilspannungen|4. Summe prüfen', 300, anker='Zuerst die Widerstände'),
       graf((0, 10), (0, 10), achsen=False, **reihe)),
    sz('Lösung Reihe', 'Sechshundert Ohm. Zwölf Volt durch sechshundert Ohm: zwanzig Milliampere, überall gleich. Über zweihundertsiebzig Ohm liegen fünf Komma vier Volt, über dreihundertdreissig Ohm sechs Komma sechs Volt. Probe: Zusammen zwölf Volt.',
       formel(r'\fc{R_\text{ges}} = 270\;\Omega + 330\;\Omega = \fc{600\;\Omega}', 280, g=40, anker='Sechshundert Ohm'),
       formel(r'\fb{I} = \dfrac{\fa{12\;\text{V}}}{\fc{600\;\Omega}} = \fb{20\;\text{mA}}', 390, g=40, anker='Zwölf Volt durch'),
       formel(r'\fa{U_1} = \fb{20\;\text{mA}} \cdot 270\;\Omega = \fa{5.4\;\text{V}} \qquad \fa{U_2} = \fa{6.6\;\text{V}}', 510, g=36, anker='Über zweihundertsiebzig'),
       formel(r'\text{Probe: } 5.4\;\text{V} + 6.6\;\text{V} = 12\;\text{V}', 620, g=38, anker='Probe'),
       graf((0, 10), (0, 10), achsen=False, **reihe),
       graf((0, 10), (0, 10), achsen=False, anker='Über zweihundertsiebzig',
            texte=[{"bei": [4.15, 6.7], "text": "5.4 V", "farbe": 1, "groesse": 30, "anker": "middle"}, {"bei": [7.15, 6.7], "text": "6.6 V", "farbe": 1, "groesse": 30, "anker": "middle"},
                   {"bei": [5.6, 2.35], "text": "I = 20 mA", "farbe": 2, "groesse": 30, "anker": "middle"}])),
])
setze_fragen(d, [frage('Vorgehen Reihe', 'In welcher Reihenfolge rechnest du?',
    ['Teilspannungen → Strom → Gesamtwiderstand', 'Gesamtwiderstand → Strom → Teilspannungen → Summe prüfen', 'Strom durch R₁ = 12 V : 270 Ω → Teilspannungen'], 1,
    {0: 'Für die Teilspannungen brauchst du den Strom. Woher kommt er?', 2: 'Liegen an R₁ wirklich die ganzen 12 V?'},
    sprich='In welcher Reihenfolge rechnest du?',
    rueck_sprich={0: 'Für die Teilspannungen brauchst du den Strom. Woher kommt er?', 2: 'Liegen an R eins wirklich die ganzen zwölf Volt?'})])
d['kurzbeschrieb'] = 'Reihe teilt die Spannung, parallel den Strom — und ein vorgerechnetes Problem: zwei Widerstände in Reihe an 12 V, mit Probe.'
speichere('p6-2-lp-schaltungen', d)

# ===================================================================== Kapitel 7: Gefahren und Schutz
d = lade('p6-2-lp-gefahren'); ohne(d, PROB)
d['_probe'] = d['_probe'].replace('Kapitel 5;', 'Kapitel 7;')
bal = [(1, 12.17, 2, 'Betrieb 12.2 A'), (3, 13.0, 5, 'LS 13 A'), (5, 10.0, 4, 'abgerollt 10 A'), (7, 4.35, 4, 'aufgerollt 4.3 A')]
balken = dict(flaechen=[{"punkte": [[x - 0.6, 0], [x - 0.6, h], [x + 0.6, h], [x + 0.6, 0]], "farbe": f, "deckung": 0.35} for x, h, f, _ in bal],
              texte=[{"bei": [x, h + 0.4], "text": t, "farbe": f, "groesse": 24, "anker": "middle"} for x, h, f, t in bal],
              strecken=[{"von": [0, 12.17], "bis": [8.2, 12.17], "farbe": 2, "dicke": 3, "gestrichelt": True}])
vor_merke(d, [
    sz('Problem Kabelrolle', 'Jetzt ein ganzes Problem. Der Leitungsschutzschalter ist für die feste Leitung in der Wand bemessen. Eine Kabelrolle trägt die Aufschrift: aufgerollt tausend Watt, abgerollt zweitausenddreihundert Watt. Daran hängen zwei Heizgeräte, zusammen zweitausendachthundert Watt am Netz. Der LS hat dreizehn Ampere. Reicht die Beurteilung «der LS bleibt ein»?',
       notiz('Kabelrolle: aufgerollt 1000 W,|abgerollt 2300 W|2 Heizgeräte: 2800 W an 230 V|LS: 13 A', 300, anker='Eine Kabelrolle'),
       notiz('«Der LS bleibt ein» — reicht das?', 580, anker='Reicht die Beurteilung')),
    sz('Vorgehen Kabelrolle', 'Zuerst den Betriebsstrom bestimmen. Dann mit dem Nennstrom des LS vergleichen und danach mit beiden Angaben der Kabelrolle. Am Schluss fragen: Welche Einrichtung schützt welchen Teil?',
       notiz('1. Betriebsstrom I = P / U|2. mit LS vergleichen|3. mit beiden Angaben der Rolle vergleichen|4. Wer schützt was?', 300, anker='Zuerst den Betriebsstrom')),
    sz('Lösung Kabelrolle', 'Zweitausendachthundert Watt durch zweihundertdreissig Volt: rund zwölf Komma zwei Ampere. Das ist unter dreizehn Ampere, der LS bleibt ein. Die Kabelrolle ist aber abgerollt nur für zweitausenddreihundert Watt gebaut, aufgerollt für tausend. Beide Angaben sind überschritten: Das Kabel wird heiss, aufgerollt kann es die Wärme kaum abgeben. Es droht ein Brand. Der LS schützt die feste Leitung, nicht die Kabelrolle. Die Beurteilung reicht also nicht: Ein Gerät gehört an eine andere Steckdose.',
       formel(r'\fb{I} = \dfrac{P}{\fa{U}} = \dfrac{2800\;\text{W}}{\fa{230\;\text{V}}} \approx \fb{12.2\;\text{A}} \lt 13\;\text{A}', 290, g=38, anker='Zweitausendachthundert Watt'),
       formel(r'2800\;\text{W} \gt 2300\;\text{W} \gt 1000\;\text{W}', 420, g=40, anker='Beide Angaben'),
       notiz('LS schützt die feste Leitung,|nicht die Kabelrolle', 540, anker='Der LS schützt', farbe='rot'),
       graf((-0.9, 8.2), (-0.8, 15.5), (), (5, 10), '', 'I [A]', anker='Zweitausendachthundert Watt', **balken)),
])
setze_fragen(d, [frage('Vorgehen Kabelrolle', 'Womit beginnst du die Beurteilung?',
    ['mit dem Betriebsstrom I = P / U', 'mit dem FI: Er merkt Überlast sofort', 'mit dem LS: Bleibt er ein, ist alles in Ordnung'], 0,
    {1: 'Der FI vergleicht Hin- und Rückstrom. Gibt es hier eine Differenz?', 2: 'Wofür ist der LS bemessen — für die feste Leitung oder für die Kabelrolle?'},
    sprich='Womit beginnst du die Beurteilung?',
    rueck_sprich={1: 'Der FI vergleicht Hin- und Rückstrom. Gibt es hier eine Differenz?', 2: 'Wofür ist der LS bemessen, für die feste Leitung oder für die Kabelrolle?'})])
d['kurzbeschrieb'] = 'Wer misst was, wer trennt wann: FI, Schutzleiter, Leitungsschutzschalter — und ein vorgerechnetes Problem: eine überlastete Kabelrolle, bei der der LS eingeschaltet bleibt.'
speichere('p6-2-lp-gefahren', d)

for k, alt, neu in [('p6-2-lp-kontrolle-schaltungen', 'Kapitel 4;', 'Kapitel 5;'), ('p6-2-lp-kontrolle-gefahren', 'Kapitel 5;', 'Kapitel 7;')]:
    d = lade(k); d['_probe'] = d['_probe'].replace(alt, neu); speichere(k, d)

# ===================================================================== Kapitel 4 neu: Messen und Kennlinien
KOPF = {k: v for k, v in lade('p6-2-lp-ladung').items() if k in ('themenbereich', 'lerngebiet', 'lektion', 'stufe', 'theme', 'latex', 'reihe', 'nachlauf', 'probe')}
KOPF['datum'] = '2026-10-06'
JETZT = lade('p6-2-lp-ladung')['szenen'][-1]


def kreis_mess(v_parallel=True, a_reihe=True, wert_v=None, wert_a=None):
    s1, t1 = quelle(1.2, 5, None)
    rr = widerstand(4.6, 6.6, 6.4, 7.4)
    teile = [[draht([(1.2, 5.2), (1.2, 7), (2.6, 7)]), draht([(3.7, 7), (4.6, 7)]), draht([(6.4, 7), (9, 7), (9, 2.4), (1.2, 2.4), (1.2, 4.8)])],
             [s1], list(rr)]
    am = messgeraet(3.15, 7, 'A'); teile += [am[0], am[1]]
    if v_parallel:
        teile.append(draht([(4.2, 7), (4.2, 8.8), (4.95, 8.8)])); teile.append(draht([(6.05, 8.8), (6.8, 8.8), (6.8, 7)]))
        vm = messgeraet(5.5, 8.8, 'V'); teile += [vm[0], vm[1]]
    extra = []
    if wert_a: extra.append({"bei": [3.15, 5.7], "text": wert_a, "farbe": 2, "groesse": 28, "anker": "middle"})
    if wert_v: extra.append({"bei": [7.2, 8.65], "text": wert_v, "farbe": 1, "groesse": 28})
    teile.append(extra)
    return schaltbild(teile)


ui = lambda **kw: graf((-0.006, 0.062), (-1.3, 13.5), (0.02, 0.04, 0.06), (3, 6, 9, 12), 'I [A]', 'U [V]', **kw)
lampe = "50*x+41667*x*x*x"
d = dict(KOPF, titel='Strom sehen: messen und Kennlinien', dateiname='p6-2-lp-messen',
         kurzbeschrieb='Voltmeter parallel, Amperemeter in den Stromweg, R aus einem Messwertepaar und die U-I-Kennlinie: ohmsch oder nicht — mit einem vorgerechneten Messproblem.',
         schlagworte=['Messen', 'Voltmeter', 'Amperemeter', 'Kennlinie', 'ohmsch', 'Widerstand'],
         _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 4; gehört dorthin, nicht in die Clip-Bibliothek.')
d['szenen'] = [
    sz('Spannung', 'Spannung liegt zwischen zwei Punkten. Darum kommt das Voltmeter an die beiden Anschlüsse des Bauteils, parallel dazu. Ein ideales Voltmeter lässt dabei keinen Strom durch.',
       titel('Richtig messen'),
       notiz('Voltmeter: an die zwei Anschlüsse,|parallel', 420, anker='Darum kommt das Voltmeter'),
       graf((0, 10), (0, 10), achsen=False, anker='Darum kommt', **kreis_mess())),
    sz('Strom', 'Stromstärke ist die Ladung, die pro Sekunde durch einen Querschnitt fliesst. Darum muss der Strom durch das Amperemeter fliessen: Es kommt in den Stromweg, in Reihe. Ein ideales Amperemeter hat keinen Widerstand.',
       notiz('Amperemeter: in den Stromweg,|in Reihe', 300, anker='Darum muss der Strom'),
       graf((0, 10), (0, 10), achsen=False, **kreis_mess())),
    sz('Falsch angeschlossen', 'Vertauscht man die beiden, geht es schief. Ein Voltmeter im Stromweg unterbricht den Kreis: Es fliesst kein Strom. Ein Amperemeter parallel zum Bauteil überbrückt es, ein Kurzschluss.',
       notiz('Voltmeter im Stromweg:|Kreis unterbrochen', 300, anker='Ein Voltmeter im Stromweg', farbe='rot'),
       notiz('Amperemeter parallel:|Kurzschluss', 470, anker='Ein Amperemeter parallel', farbe='rot')),
    sz('Widerstand', 'Aus den beiden Anzeigen folgt der Widerstand: Spannung durch Stromstärke, den Strom in Ampere.',
       formel(r'\fc{R} = \dfrac{\fa{U}}{\fb{I}} \qquad \fb{I}\ \text{in A}', 320, g=52, anker='Spannung durch')),
    sz('Kennlinie', 'Trägt man mehrere Messpunkte ein, Strom nach rechts, Spannung nach oben, entsteht die Kennlinie. Liegen die Punkte auf einer Geraden durch den Ursprung, ist der Widerstand konstant: Das Bauteil ist ohmsch, und die Steigung ist R. Beim Lämpchen krümmt sich die Kurve: Sein Widerstand wächst mit dem Strom.',
       notiz('Ursprungsgerade: ohmsch,|Steigung R', 300, anker='Liegen die Punkte'),
       notiz('Lämpchen: gekrümmt,|R wächst', 470, anker='Beim Lämpchen'),
       ui(anker='Trägt man', strecken=[{"von": [0, 0], "bis": [0.06, 9.0], "farbe": 3, "dicke": 5}],
          punkte=[{"x": x, "y": 150 * x, "farbe": 3} for x in (0.02, 0.04, 0.06)],
          texte=[{"bei": [0.018, 4.4], "text": "150 Ω", "farbe": 3, "groesse": 26, "anker": "end"}]),
       ui(anker='Beim Lämpchen', achsen=False, kurven=[{"formel": lampe, "von": 0, "bis": 0.06, "farbe": 1, "dicke": 4, "gestrichelt": True}],
          texte=[{"bei": [0.048, 12.6], "text": "Lämpchen (Beispiel)", "farbe": 1, "groesse": 26, "anker": "end"}])),
    sz('Problem Messung', 'Jetzt ein ganzes Problem. An einem Widerstand werden neun Volt und dreissig Milliampere gemessen. Wo sitzen die Messgeräte, wie gross ist der Widerstand, und wo liegt der Punkt in der Kennlinie?',
       notiz('gemessen: 9.0 V und 30 mA', 300, anker='An einem Widerstand'),
       notiz('gesucht: Anschlüsse, R,|Punkt in der Kennlinie', 440, anker='Wo sitzen'),
       graf((0, 10), (0, 10), achsen=False, anker='An einem Widerstand', **kreis_mess(wert_v='9.0 V', wert_a='30 mA'))),
    sz('Vorgehen Messung', 'Das Amperemeter sitzt im Stromweg, das Voltmeter an den Anschlüssen. Vor dem Rechnen die Milliampere in Ampere umrechnen: dreissig Milliampere sind null Komma null drei null Ampere. Dann R gleich U durch I, und den Punkt mit dem Strom nach rechts, der Spannung nach oben eintragen.',
       formel(r'30\;\text{mA} = 0.030\;\text{A}', 300, g=48, anker='Vor dem Rechnen'),
       notiz('Achsen: I nach rechts, U nach oben', 440, anker='und den Punkt'),
       graf((0, 10), (0, 10), achsen=False, **kreis_mess(wert_v='9.0 V', wert_a='30 mA'))),
    sz('Lösung Messung', 'Neun Volt durch null Komma null drei Ampere: dreihundert Ohm. In der Kennlinie liegt der Punkt bei null Komma null drei Ampere und neun Volt. Probe: Volt durch Ampere ist Ohm, und die Gerade vom Ursprung durch den Punkt hat die Steigung dreihundert Ohm.',
       formel(r'\fc{R} = \dfrac{\fa{9.0\;\text{V}}}{\fb{0.030\;\text{A}}} = \fc{300\;\Omega}', 300, g=48, anker='Neun Volt durch'),
       notiz('Punkt: (0.030 A; 9.0 V)', 460, anker='In der Kennlinie'),
       ui(anker='In der Kennlinie', strecken=[{"von": [0, 0], "bis": [0.04, 12], "farbe": 3, "dicke": 4},
                                              {"von": [0.03, 0], "bis": [0.03, 9], "farbe": 5, "dicke": 3, "gestrichelt": True},
                                              {"von": [0, 9], "bis": [0.03, 9], "farbe": 5, "dicke": 3, "gestrichelt": True}],
          punkte=[{"x": 0.03, "y": 9, "farbe": 3, "beschriftung": "(0.030 A; 9.0 V)", "beschriftung_bei": [0.033, 8.0], "anker": "start"}])),
    sz('Merke', 'Zum Mitnehmen: Das Voltmeter kommt parallel an die zwei Punkte, das Amperemeter in den Stromweg. Der Widerstand ist U durch I, mit I in Ampere. Und eine Ursprungsgerade in der Kennlinie heisst: ohmsch.',
       titel('Zum Mitnehmen', 260, 76),
       formel(r'\fc{R} = \dfrac{\fa{U}}{\fb{I}}', 420, g=50, ein=0.4),
       notiz('Voltmeter: parallel|Amperemeter: in Reihe|Ursprungsgerade: ohmsch', 540, ein=1.2)),
    dict(JETZT)]
d['fragen'] = [frage('Vorgehen Messung', 'Bevor du R = U / I rechnest: Was tust du?',
    ['I durch U teilen', 'den Punkt bei (9; 30) eintragen', '30 mA in 0.030 A umrechnen'], 2,
    {0: 'R = U / I: Was steht im Zähler, was im Nenner?', 1: 'Welche Grösse gehört nach rechts, welche nach oben — und in welcher Einheit?'},
    sprich='Bevor du R gleich U durch I rechnest: Was tust du?',
    rueck_sprich={0: 'R gleich U durch I. Was steht im Zähler, was im Nenner?', 1: 'Welche Grösse gehört nach rechts, welche nach oben, und in welcher Einheit?'})]
speichere('p6-2-lp-messen', d)

# ===================================================================== Kapitel 6 neu: Schaltungen erkennen
s7, t7 = quelle(1.2, 5, '9 V')
ra = widerstand(3.2, 7.6, 5.0, 8.4, 'R₁ = 200 Ω', [4.1, 8.8])
rb = widerstand(6.6, 3.4, 7.4, 5.2, 'R₂ = 200 Ω', [6.35, 4.1], anker='end')
DR = {'a': [(1.2, 5.2), (1.2, 8), (3.2, 8)], 'a2': [(2.2, 8), (2.2, 6.2), (7, 6.2), (7, 5.2)],
      'b': [(5.0, 8), (9, 8), (9, 2), (1.2, 2), (1.2, 4.8)], 'b2': [(7, 3.4), (7, 2)]}


def ungewohnt(farbig=False):
    teile = []
    if farbig:
        teile += [draht(DR['a'], farbe=4, dicke=12), draht(DR['a2'], farbe=4, dicke=12), draht(DR['b'], farbe=1, dicke=12), draht(DR['b2'], farbe=1, dicke=12)]
    teile += [draht(DR['a']), draht(DR['a2']), draht(DR['b']), draht(DR['b2']), [s7], [t7], list(ra), list(rb)]
    s = schaltbild(teile)
    s['punkte'] = [{"x": 2.2, "y": 8, "farbe": 5}, {"x": 7, "y": 2, "farbe": 5}]
    return s


d = dict(KOPF, titel='Strom sehen: Verbindungen zählen, nicht die Lage', dateiname='p6-2-lp-erkennen',
         kurzbeschrieb='Reihe oder parallel erkennt man an den Verbindungen, nicht an der Lage; Ladungserhaltung und Energiebilanz begründen Strom- und Spannungsaufteilung — mit einem ungewohnt gezeichneten Problem.',
         schlagworte=['Reihenschaltung', 'Parallelschaltung', 'Verbindungspunkt', 'Ladungserhaltung', 'Energiebilanz', 'Probe'],
         _probe='Einführungsclip des Leitprogramms Elektrizität, Kapitel 6; gehört dorthin, nicht in die Clip-Bibliothek.')
d['szenen'] = [
    sz('Verbindungen', 'Ob zwei Widerstände in Reihe oder parallel liegen, zeigt nicht ihre Lage auf dem Blatt, sondern ihre Verbindungen. Alle Drähte, die ohne Bauteil dazwischen zusammenhängen, sind ein einziger Verbindungspunkt.',
       titel('Verbindungen zählen'),
       notiz('ein Draht ohne Bauteil dazwischen:|ein Verbindungspunkt', 420, anker='Alle Drähte'),
       graf((0, 10), (0, 10), achsen=False, anker='Alle Drähte', **ungewohnt(True))),
    sz('Parallel oder Reihe', 'Parallel heisst: Beide Widerstände verbinden dieselben zwei Verbindungspunkte. In Reihe teilen sie sich einen Punkt, an dem sonst nichts hängt.',
       notiz('parallel: dieselben zwei Punkte', 300, anker='Parallel heisst'),
       notiz('in Reihe: ein gemeinsamer Punkt,|an dem sonst nichts hängt', 440, anker='In Reihe teilen')),
    sz('Strom teilt sich', 'Warum teilt sich der Strom parallel auf? Ladung bleibt erhalten: Was in eine Verzweigung hineinfliesst, fliesst wieder hinaus. Der Gesamtstrom ist die Summe der Zweigströme.',
       formel(r'\fb{I} = \fb{I_1} + \fb{I_2}', 320, g=56, anker='Ladung bleibt erhalten'),
       notiz('Ladung bleibt erhalten', 470, anker='Ladung bleibt erhalten')),
    sz('Spannung teilt sich', 'Und warum teilt sich in Reihe die Spannung? Die Quelle gibt jedem Coulomb ihre Energie mit, und die Widerstände geben sie zusammen wieder ab. Die Teilspannungen ergeben zusammen die Quellenspannung.',
       formel(r'\fa{U} = \fa{U_1} + \fa{U_2}', 320, g=56, anker='Die Quelle gibt'),
       notiz('Energiebilanz', 470, anker='Die Quelle gibt')),
    sz('Problem Zeichnung', 'Jetzt ein ganzes Problem. Zwei Widerstände von je zweihundert Ohm, ungewohnt gezeichnet, an neun Volt. Wie sind sie geschaltet, und welche Ströme fliessen?',
       notiz('2 · 200 Ω an 9 V,|ungewohnt gezeichnet', 300, anker='Zwei Widerstände'),
       notiz('gesucht: Schaltungsart,|Ströme, R ges', 460, anker='Wie sind sie'),
       graf((0, 10), (0, 10), achsen=False, anker='Zwei Widerstände', **ungewohnt())),
    sz('Vorgehen Zeichnung', 'Zuerst die Verbindungen verfolgen: Wo beginnt und wo endet jeder Widerstand? Erst wenn die Schaltungsart klar ist, kommen die Ströme, der Gesamtstrom und die Probe.',
       notiz('1. Verbindungen verfolgen|2. Schaltungsart|3. Ströme, Gesamtstrom|4. Probe', 300, anker='Zuerst die Verbindungen'),
       graf((0, 10), (0, 10), achsen=False, **ungewohnt()),
       graf((0, 10), (0, 10), achsen=False, anker='Wo beginnt', **ungewohnt(True))),
    sz('Lösung Zeichnung', 'Beide Widerstände beginnen am Draht vom Pluspol und enden am Draht zum Minuspol: Sie sind parallel. An jedem liegen neun Volt, also fliessen je fünfundvierzig Milliampere, zusammen neunzig. Der Gesamtwiderstand ist neun Volt durch neunzig Milliampere, hundert Ohm. Probe: Hundert Ohm ist kleiner als zweihundert, wie es parallel sein muss.',
       notiz('parallel', 280, anker='Sie sind parallel', farbe='rot'),
       formel(r'\fb{I_1} = \fb{I_2} = \dfrac{\fa{9.0\;\text{V}}}{\fc{200\;\Omega}} = \fb{45\;\text{mA}}', 390, g=40, anker='An jedem liegen'),
       formel(r'\fb{I} = 45\;\text{mA} + 45\;\text{mA} = \fb{90\;\text{mA}}', 500, g=40, anker='zusammen neunzig'),
       formel(r'\fc{R_\text{ges}} = \dfrac{9.0\;\text{V}}{0.090\;\text{A}} = \fc{100\;\Omega} \lt 200\;\Omega', 610, g=38, anker='Der Gesamtwiderstand'),
       graf((0, 10), (0, 10), achsen=False, **ungewohnt(True))),
    sz('Merke', 'Zum Mitnehmen: Verbindungen zählen, nicht die Lage. Ladung bleibt erhalten, darum addieren sich an einer Verzweigung die Ströme. Die Energiebilanz sagt: In Reihe addieren sich die Spannungen. Und jede Rechnung bekommt eine Probe.',
       titel('Zum Mitnehmen', 260, 76),
       formel(r'\fb{I} = \fb{I_1} + \fb{I_2} \qquad \fa{U} = \fa{U_1} + \fa{U_2}', 420, g=46, ein=0.4),
       notiz('Verbindungen statt Lage|Probe: Summen, R ges < kleinster Zweig', 540, ein=1.2)),
    dict(JETZT)]
d['fragen'] = [frage('Vorgehen Zeichnung', 'Was tust du zuerst?',
    ['die Widerstände addieren, weil sie hintereinander stehen', 'Verbindungen verfolgen: Wo beginnt und endet jeder Widerstand?', 'den Strom durch den oberen Widerstand berechnen'], 1,
    {0: 'Stehen sie wirklich hintereinander — oder nur auf dem Blatt?', 2: 'Welche Spannung liegt an ihm? Das weisst du erst, wenn die Schaltung klar ist.'},
    sprich='Was tust du zuerst?',
    rueck_sprich={0: 'Stehen sie wirklich hintereinander, oder nur auf dem Blatt?', 2: 'Welche Spannung liegt an ihm? Das weisst du erst, wenn die Schaltung klar ist.'})]
speichere('p6-2-lp-erkennen', d)


# ===================================================================== Kontrollclips Kapitel 4 und 6 (mit Antwortbildern)
def A(e):
    e['antwort'] = True; e['ein'] = 1.0
    return e


d = dict(KOPF, titel='Strom sehen: Kontrollfragen zum Messen und zu Kennlinien', dateiname='p6-2-lp-kontrolle-messen',
         kurzbeschrieb='Fünf Fragen zum Anschluss von Voltmeter und Amperemeter, zum Widerstand aus Messwerten und aus einem Kennlinienpunkt und zur Ursprungsgeraden.',
         schlagworte=['Messen', 'Kennlinie', 'Kontrollfragen'],
         _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 4; gehört dorthin, nicht in die Clip-Bibliothek.')
lampe_kreis = lambda **kw: kreis_mess(**kw)
d['szenen'] = [
    sz('Frage 1', 'Spannung liegt zwischen zwei Punkten: Das Voltmeter kommt an die beiden Anschlüsse der Lampe, parallel zu ihr.',
       notiz('Voltmeter:|an die zwei Anschlüsse, parallel', 320, ein=1.0),
       A(graf((0, 10), (0, 10), achsen=False, **kreis_mess()))),
    sz('Frage 2', 'Der Strom durch die Lampe muss auch durch das Messgerät fliessen: Das Amperemeter kommt in den Stromweg, in Reihe.',
       notiz('Amperemeter:|in den Stromweg, in Reihe', 320, ein=1.0),
       A(graf((0, 10), (0, 10), achsen=False, **kreis_mess()))),
    sz('Frage 3', 'Fünf Volt durch null Komma null zwei fünf Ampere: zweihundert Ohm.',
       formel(r'\fc{R} = \dfrac{\fa{5.0\;\text{V}}}{\fb{0.025\;\text{A}}} = \fc{200\;\Omega}', 300, g=48, ein=1.0),
       A(ui(strecken=[{"von": [0, 0], "bis": [0.0605, 12.1], "farbe": 3, "dicke": 4}, {"von": [0.025, 0], "bis": [0.025, 5], "farbe": 5, "dicke": 3, "gestrichelt": True},
                      {"von": [0, 5], "bis": [0.025, 5], "farbe": 5, "dicke": 3, "gestrichelt": True}],
            punkte=[{"x": 0.025, "y": 5, "farbe": 3, "beschriftung": "(0.025 A; 5.0 V)", "beschriftung_bei": [0.028, 4.0], "anker": "start"}]))),
    sz('Frage 4', 'Achtzehn Volt durch null Komma null vier Ampere: vierhundertfünfzig Ohm.',
       formel(r'\fc{R} = \dfrac{\fa{18\;\text{V}}}{\fb{0.04\;\text{A}}} = \fc{450\;\Omega}', 300, g=48, ein=1.0),
       A(graf((-0.005, 0.052), (-2, 22), (0.01, 0.02, 0.03, 0.04, 0.05), (5, 10, 15, 20), 'I [A]', 'U [V]',
              strecken=[{"von": [0, 0], "bis": [0.044, 19.8], "farbe": 3, "dicke": 4}, {"von": [0.04, 0], "bis": [0.04, 18], "farbe": 5, "dicke": 3, "gestrichelt": True},
                        {"von": [0, 18], "bis": [0.04, 18], "farbe": 5, "dicke": 3, "gestrichelt": True}],
              punkte=[{"x": 0.04, "y": 18, "farbe": 3, "beschriftung": "(0.04 A; 18 V)", "beschriftung_bei": [0.038, 19.6], "anker": "end"}],
              texte=[{"bei": [0.02, 3.5], "text": "Steigung = R", "farbe": 3, "groesse": 26, "anker": "middle"}]))),
    sz('Frage 5', 'Auf einer Ursprungsgeraden ist U durch I überall gleich: Der Widerstand ist konstant, das Bauteil ohmsch.',
       notiz('Ursprungsgerade:|R konstant, ohmsch', 320, ein=1.0),
       A(ui(strecken=[{"von": [0, 0], "bis": [0.06, 12], "farbe": 3, "dicke": 4}],
            punkte=[{"x": x, "y": 200 * x, "farbe": 3} for x in (0.015, 0.03, 0.045)],
            texte=[{"bei": [0.03, 2.2], "text": "U : I überall 200 Ω", "farbe": 3, "groesse": 26, "anker": "middle"}]))),
]
d['fragen'] = [
    frage('Frage 1', 'Du willst die Spannung an einer Lampe messen. Wo schliesst du das Voltmeter an?',
          ['in den Stromweg vor der Lampe', 'an die beiden Anschlüsse der Lampe', 'zwischen Schalter und Batterie'], 1,
          {0: 'Spannung liegt zwischen zwei Punkten. Zwischen welchen?', 2: 'Dort liegt es im Stromweg. Was misst man zwischen zwei Punkten?'}),
    frage('Frage 2', 'Wohin gehört das Amperemeter, um den Strom durch die Lampe zu messen?',
          ['parallel zur Lampe', 'an die Pole der Batterie', 'in den Stromweg zur Lampe'], 2,
          {0: 'Ein ideales Amperemeter hat keinen Widerstand. Was geschieht parallel zur Lampe?', 1: 'Muss der Strom durch das Messgerät fliessen — oder daran vorbei?'}),
    frage('Frage 3', 'Gemessen: 5.0 V und 25 mA. Wie gross ist der Widerstand?', ['0.2 Ω', '200 Ω', '125 Ω'], 1,
          {0: 'Milliampere in Ampere umgerechnet?', 2: 'Geteilt oder mal?'},
          sprich='Gemessen werden fünf Volt und fünfundzwanzig Milliampere. Wie gross ist der Widerstand?'),
    frage('Frage 4', 'In einer U-I-Kennlinie (I nach rechts, U nach oben) liegt ein Messpunkt bei (0.04 A; 18 V). Welcher Widerstand?', ['450 Ω', '0.0022 Ω', '0.72 Ω'], 0,
          {1: 'Umgekehrt? R = U / I.', 2: 'Geteilt, nicht mal.'},
          sprich='In einer U-I-Kennlinie, I nach rechts, U nach oben, liegt ein Messpunkt bei null Komma null vier Ampere und achtzehn Volt. Welcher Widerstand?',
          rueck_sprich={1: 'Umgekehrt? R gleich U durch I.', 2: 'Geteilt, nicht mal.'}),
    frage('Frage 5', 'Die Messpunkte eines Bauteils liegen auf einer Geraden durch den Ursprung. Was heisst das?',
          ['Der Widerstand wächst mit der Spannung.', 'Es fliesst kein Strom.', 'Der Widerstand ist konstant: Das Bauteil ist ohmsch.'], 2,
          {0: 'Wie ändert sich U / I entlang einer Ursprungsgeraden?', 1: 'Die Punkte liegen bei Strömen grösser null.'},
          rueck_sprich={0: 'Wie ändert sich U durch I entlang einer Ursprungsgeraden?', 1: 'Die Punkte liegen bei Strömen grösser null.'}),
]
speichere('p6-2-lp-kontrolle-messen', d)

par = lambda texte=(): schaltbild([draht([(1.2, 5.2), (1.2, 8), (7, 8)]), draht([(1.2, 4.8), (1.2, 2), (7, 2)]), [quelle(1.2, 5, None)[0]],
                                   draht([(4, 8), (4, 6.1)]), draht([(4, 3.9), (4, 2)]), draht([(7, 8), (7, 6.1)]), draht([(7, 3.9), (7, 2)]),
                                   list(widerstand(3.6, 3.9, 4.4, 6.1)), list(widerstand(6.6, 3.9, 7.4, 6.1)), [list(texte)]])
d = dict(KOPF, titel='Strom sehen: Kontrollfragen zum Erkennen und Prüfen', dateiname='p6-2-lp-kontrolle-erkennen',
         kurzbeschrieb='Fünf Fragen zu drei Fehlvorstellungen über den Strom, zur Spannungsprobe in Reihe und zum Erkennen einer Parallelschaltung an den Verbindungen.',
         schlagworte=['Reihenschaltung', 'Parallelschaltung', 'Fehlvorstellungen', 'Probe', 'Kontrollfragen'],
         _probe='Kontrollclip des Leitprogramms Elektrizität, Kapitel 6; gehört dorthin, nicht in die Clip-Bibliothek.')
d['szenen'] = [
    sz('Frage 1', 'Der zweite Zweig liegt an derselben Spannung und nimmt denselben Strom auf. Aus der Quelle fliesst jetzt doppelt so viel: achtzig statt vierzig Milliampere.',
       formel(r'\fb{I} = 40\;\text{mA} + 40\;\text{mA} = \fb{80\;\text{mA}}', 300, g=46, ein=1.0),
       A(graf((0, 10), (0, 10), achsen=False, **par([{"bei": [4.6, 5.3], "text": "40 mA", "farbe": 2, "groesse": 28}, {"bei": [7.6, 5.3], "text": "40 mA", "farbe": 2, "groesse": 28},
                                                       {"bei": [2.3, 8.5], "text": "80 mA", "farbe": 2, "groesse": 30}, {"bei": [1.8, 5.3], "text": "12 V", "farbe": 1, "groesse": 28}])))),
    sz('Frage 2', 'Strom wird nicht verbraucht. In Reihe fliesst überall derselbe Strom, auch zurück zur Quelle: zwanzig Milliampere.',
       notiz('überall 20 mA:|nichts verbraucht', 320, ein=1.0),
       A(graf((0, 10), (0, 10), achsen=False, **schaltbild([draht([(1.2, 5.2), (1.2, 8), (3.3, 8)]), draht([(5.0, 8), (6.3, 8)]), draht([(8.0, 8), (9, 8), (9, 2), (1.2, 2), (1.2, 4.8)]),
                                                           [quelle(1.2, 5, None)[0]], list(widerstand(3.3, 7.6, 5.0, 8.4, 'R₁', [4.15, 8.8])), list(widerstand(6.3, 7.6, 8.0, 8.4, 'R₂', [7.15, 8.8])),
                                                           [[{"bei": [2.3, 8.45], "text": "20 mA", "farbe": 2, "groesse": 26, "anker": "middle"}, {"bei": [5.65, 8.45], "text": "20 mA", "farbe": 2, "groesse": 26, "anker": "middle"},
                                                             {"bei": [5.2, 2.4], "text": "20 mA zurück", "farbe": 2, "groesse": 28, "anker": "middle"}]]])))),
    sz('Frage 3', 'Durch jeden Zweig fliesst Spannung durch Widerstand: achtzig Milliampere durch hundert Ohm, zwanzig durch vierhundert. Der kleinere Widerstand bekommt mehr, aber nicht alles.',
       formel(r'\fb{I_1} = \dfrac{8\;\text{V}}{100\;\Omega} = 80\;\text{mA} \qquad \fb{I_2} = \dfrac{8\;\text{V}}{400\;\Omega} = 20\;\text{mA}', 300, g=36, ein=1.0),
       A(graf((0, 10), (0, 10), achsen=False, **par([{"bei": [4.6, 5.3], "text": "80 mA", "farbe": 2, "groesse": 28}, {"bei": [7.6, 5.3], "text": "20 mA", "farbe": 2, "groesse": 28}, {"bei": [3.4, 4.5], "text": "100 Ω", "farbe": 3, "groesse": 26, "anker": "end"}, {"bei": [6.4, 4.5], "text": "400 Ω", "farbe": 3, "groesse": 26, "anker": "end"},
                                                       {"bei": [1.8, 5.3], "text": "8 V", "farbe": 1, "groesse": 28}])))),
    sz('Frage 4', 'Energiebilanz: Die Teilspannungen ergeben zusammen die Quellenspannung. Fünf und acht Volt sind dreizehn, nicht zwölf — da stimmt etwas nicht.',
       formel(r'5\;\text{V} + 8\;\text{V} = 13\;\text{V} \ne 12\;\text{V}', 300, g=46, ein=1.0),
       A(graf((0, 10), (-0.5, 15), (), (12,), '', 'U [V]',
              flaechen=[{"punkte": [[2, 0], [2, 5], [4, 5], [4, 0]], "farbe": 1, "deckung": 0.35}, {"punkte": [[2, 5], [2, 13], [4, 13], [4, 5]], "farbe": 1, "deckung": 0.18}],
              strecken=[{"von": [0, 12], "bis": [9.5, 12], "farbe": 4, "dicke": 3, "gestrichelt": True}],
              texte=[{"bei": [3, 2.3], "text": "5 V", "farbe": 1, "groesse": 28, "anker": "middle"}, {"bei": [3, 8.8], "text": "8 V", "farbe": 1, "groesse": 28, "anker": "middle"},
                     {"bei": [9.3, 12.5], "text": "Quelle: 12 V", "farbe": 4, "groesse": 28, "anker": "end"}, {"bei": [4.4, 13.4], "text": "13 V: zu viel", "farbe": 4, "groesse": 28}]))),
    sz('Frage 5', 'Beide verbinden dieselben zwei Punkte A und B: Sie sind parallel geschaltet, ganz gleich, wie sie gezeichnet sind.',
       notiz('dieselben zwei Punkte:|parallel', 320, ein=1.0),
       A(graf((0, 10), (0, 10), achsen=False, **schaltbild([draht([(2, 5), (3, 5), (3, 7), (4, 7)]), draht([(3, 5), (3, 3), (4, 3)]), draht([(6, 7), (7, 7), (7, 5), (8, 5)]), draht([(6, 3), (7, 3), (7, 5)]),
                                                           list(widerstand(4, 6.6, 6, 7.4, 'R₁', [5, 7.8])), list(widerstand(4, 2.6, 6, 3.4, 'R₂', [5, 2.0])),
                                                           [[{"bei": [2.6, 5.5], "text": "A", "farbe": 4, "groesse": 32, "anker": "end"}, {"bei": [7.4, 5.5], "text": "B", "farbe": 1, "groesse": 32}]]])))),
]
d['fragen'] = [
    frage('Frage 1', 'An einer 12-V-Quelle hängt ein 300-Ω-Widerstand. Ein zweiter 300-Ω-Widerstand kommt parallel dazu. Was macht der Strom aus der Quelle?',
          ['Er bleibt gleich: Die Quelle liefert immer denselben Strom.', 'Er verdoppelt sich.', 'Er halbiert sich.'], 1,
          {0: 'Liefert eine Quelle immer denselben Strom? Woran liegt der Strom in jedem Zweig?', 2: 'Wird es für den Strom schwieriger oder leichter, wenn ein zweiter Weg dazukommt?'},
          sprich='An einer Zwölf-Volt-Quelle hängt ein Dreihundert-Ohm-Widerstand. Ein zweiter Dreihundert-Ohm-Widerstand kommt parallel dazu. Was macht der Strom aus der Quelle?'),
    frage('Frage 2', 'Zwei Widerstände in Reihe. Vor R₁ fliessen 20 mA. Wie viel fliesst zwischen R₂ und der Quelle zurück?',
          ['weniger: R₁ und R₂ verbrauchen Strom', '0 mA', '20 mA'], 2,
          {0: 'Wird Strom verbraucht — oder Energie umgesetzt?', 1: 'Wo bliebe dann die Ladung?'},
          sprich='Zwei Widerstände in Reihe. Vor R eins fliessen zwanzig Milliampere. Wie viel fliesst zwischen R zwei und der Quelle zurück?',
          rueck_sprich={0: 'Wird Strom verbraucht, oder Energie umgesetzt?', 1: 'Wo bliebe dann die Ladung?'}),
    frage('Frage 3', '100 Ω und 400 Ω liegen parallel an 8 V. Wo fliesst Strom?',
          ['durch beide: 80 mA und 20 mA', 'nur durch 100 Ω', 'durch beide gleich viel: je 50 mA'], 0,
          {1: 'Liegt am 400-Ω-Zweig keine Spannung?', 2: 'Bei gleicher Spannung: Lässt der grössere Widerstand gleich viel durch?'},
          sprich='Hundert Ohm und vierhundert Ohm liegen parallel an acht Volt. Wo fliesst Strom?',
          rueck_sprich={1: 'Liegt am Vierhundert-Ohm-Zweig keine Spannung?', 2: 'Bei gleicher Spannung: Lässt der grössere Widerstand gleich viel durch?'}),
    frage('Frage 4', 'In Reihe an 12 V misst jemand 5 V und 8 V an den beiden Widerständen. Kann das stimmen?',
          ['ja, das passt', 'nur bei grossem Strom', 'nein: Zusammen müssen es 12 V sein'], 2,
          {0: 'Rechne die beiden Teilspannungen zusammen.', 1: 'Hängt die Summe der Teilspannungen vom Strom ab?'},
          sprich='In Reihe an zwölf Volt misst jemand fünf Volt und acht Volt an den beiden Widerständen. Kann das stimmen?'),
    frage('Frage 5', 'R₁ und R₂ sind beide mit Punkt A und mit Punkt B verbunden, sonst mit nichts. Wie sind sie geschaltet?',
          ['in Reihe', 'parallel', 'gemischt'], 1,
          {0: 'In Reihe teilen sie sich einen Punkt, an dem sonst nichts hängt. Ist das hier so?', 2: 'Gemischt braucht mindestens drei Widerstände.'},
          sprich='R eins und R zwei sind beide mit Punkt A und mit Punkt B verbunden, sonst mit nichts. Wie sind sie geschaltet?',
          rueck_sprich={0: 'In Reihe teilen sie sich einen Punkt, an dem sonst nichts hängt. Ist das hier so?', 2: 'Gemischt braucht mindestens drei Widerstände.'}),
]
speichere('p6-2-lp-kontrolle-erkennen', d)
print('ok')
