"""Erzeugt die acht Drehbücher des Leitprogramms Temperatur (clips/p5-1-lp-*.json).

  python3 scripts/lp/temperatur/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/temperatur/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/temperatur/clips.py --neu p5-1-lp-kontrolle-skalen …   # nur diese

Archiv-Werkzeug wie scripts/lp/hydrostatik/clips.py: Nach der Vertonung sind die JSONs in clips/
die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf mit
--neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).
Antwortbilder der Kontrollclips: antworten.py (danach).

Farben (Theme begreifbar-schlicht: 1 Bernstein, 2 Orange, 3 Grün, 4 Rot, 5 Tinte), wie im Leitprogramm:
  1 Bernstein  Celsius-Temperatur (Skala, Marken in °C)
  3 Grün       Kelvin-Temperatur, absoluter Nullpunkt
  2 Orange     Temperaturdifferenz
  4 Rot        Druck
  5 Tinte      Teilchen, Messkurven, Stoffe, Gefässe
Zahlen im Sprechertext ausgeschrieben (CLAUDE.md). Bilder: Aufnahmen der Simulationen
(clips/bilder/p5-1-lp-*.jpg, Plan: aufnahmen.json) und Koordinatenbilder (graf).
"""
import json
import math
import os
import random
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv
NUR = [a for a in sys.argv[1:] if not a.startswith('--')]

KOPF = {
    'themenbereich': 'Thermodynamik · BM', 'lerngebiet': '5 · Thermodynamik',
    'lektion': ['p5-1'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-07', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Temperatur sehen', 'nachlauf': 2.6, 'probe': True,
}
CEL, ORA, KEL, DRU, TIN = 1, 2, 3, 4, 5
JETZT = {'name': 'Jetzt du', 'layout': 'zentriert', 'oben': 200,
         'sprecher': 'Jetzt du: Erkunde diese Zusammenhänge in der nachfolgenden Animation und löse die Aufgaben.',
         'elemente': [{'typ': 'titel', 'text': 'Jetzt du', 'x': 150, 'y': 280, 'groesse': 86},
                      {'typ': 'notiz', 'text': 'Erkunde diese Zusammenhänge|in der Animation unter dem Clip|und löse die Aufgaben.',
                       'x': 150, 'y': 430, 'groesse': 50, 'farbe': 'blau', 'ein': 0.6}]}


def anker(e, a, versatz=None):
    e['_anker'] = a
    if versatz:
        e['_versatz'] = versatz
    return e


def formel(t, y=300, g=46, ein=0.8, a=None):
    e = {'typ': 'formel', 'text': t, 'x': 150, 'y': y, 'breite': 820, 'groesse': g, 'ein': ein}
    return anker(e, a) if a else e


def notiz(t, y=460, farbe='tinte', ein=2.4, g=44, a=None, x=150, breite=820):
    e = {'typ': 'notiz', 'text': t, 'x': x, 'y': y, 'breite': breite, 'groesse': g, 'farbe': farbe, 'ein': ein}
    return anker(e, a) if a else e


def titel(t, y=280, g=68):
    return {'typ': 'titel', 'text': t, 'x': 150, 'y': y, 'breite': 1640, 'groesse': g}


def bild(datei, breite=620, y=190, ein=0.05, a=None, x=1040, versatz=None):
    e = {'typ': 'bild', 'datei': 'bilder/' + datei, 'x': x, 'y': y, 'breite': breite, 'abstand': 0, 'anim': 'fade', 'ein': ein}
    return anker(e, a, versatz) if a else e


def graf(xb, yb, xt=(), yt=(), xname='', yname='', ein=0.05, a=None, achsen=True, versatz=None, **kw):
    g = {'typ': 'graf', 'x': 1010, 'y': 175, 'breite': 760, 'hoehe': 760, 'abstand': 0, 'anim': 'fade', 'ein': ein,
         'pfeile': achsen, 'xbereich': list(xb), 'ybereich': list(yb),
         'xteilung': [[v, ('%g' % v).replace('-', '−')] for v in xt] or [[1e9, '']],
         'yteilung': [[v, ('%g' % v).replace('-', '−')] for v in yt] or [[1e9, '']],
         'xname': xname, 'yname': yname}
    if not achsen:
        g['achsen'] = False
    g.update(kw)
    return anker(g, a, versatz) if a else g


def S(von, bis, farbe=TIN, dicke=4, **kw):
    d = {'von': [round(von[0], 4), round(von[1], 4)], 'bis': [round(bis[0], 4), round(bis[1], 4)], 'farbe': farbe, 'dicke': dicke}
    d.update(kw)
    return d


def P(von, bis, farbe=TIN, dicke=5, **kw):
    return S(von, bis, farbe, dicke, pfeil=True, **kw)


def T(x, y, text, farbe=TIN, groesse=28, anker_='middle', **kw):
    d = {'bei': [round(x, 4), round(y, 4)], 'text': text, 'farbe': farbe, 'groesse': groesse, 'anker': anker_}
    d.update(kw)
    return d


def F(pts, farbe=TIN, deckung=0.18, **kw):
    d = {'punkte': [[round(x, 4), round(y, 4)] for x, y in pts], 'farbe': farbe, 'deckung': deckung}
    d.update(kw)
    return d


def rechteck(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def kreis(cx, cy, r, farbe=TIN, fuellung=None, dicke=4, **kw):
    d = {'art': 'kreis', 'm': [cx, cy], 'r': r, 'farbe': farbe, 'dicke': dicke}
    if fuellung:
        d['fuellung'] = fuellung
    d.update(kw)
    return d


def sz(name, sprecher, *elemente):
    return {'name': name, 'layout': 'zentriert', 'oben': 200, 'sprecher': sprecher, 'elemente': list(elemente)}


def wahl(szene, text, optionen, richtig, rueck, sprich=None, kopf=None, rueck_sprich=None):
    # rueck_sprich: gesprochene Fassung einzelner Rückmeldungen mit ausgeschriebenen Zahlen (CLAUDE.md)
    rs = dict(rueck); rs.update(rueck_sprich or {})
    F_ = {'szene': szene, 'bei': 0.3, 'typ': 'wahl', 'text': text, 'optionen': optionen, 'richtig': richtig,
          'rueck': {str(k): v for k, v in rueck.items()}, 'sprich': sprich or text,
          'rueck_sprich': {str(k): v for k, v in rs.items()}}
    if kopf:
        F_['kopf'] = kopf
    return F_


def vm(c):
    return math.sqrt(8 * 8.314 * (c + 273.15) / (math.pi * 0.028))


VFORMEL = 'sqrt(8*8.314*(x+273.15)/(pi*0.028))'
DREH = []
EIN = 'Einführungsclip des Leitprogramms Temperatur, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Temperatur, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'


# ------------------------------------------------------------------ Bausteine für Bilder
def tempo_graf(x0=-40, x1=140, ein=0.05, a=None, extra=None, punkte=None, **kw):
    """Mittleres Tempo von Stickstoff über der Temperatur (wie Simulation 1)."""
    g = graf([x0, x1], [-60, 700], [v for v in range(-200, 301, 20) if x0 < v < x1 and v != 0],
             [100, 200, 300, 400, 500, 600], 'ϑ [°C]', 'Tempo [m/s]', ein=ein, a=a,
             kurven=[{'formel': VFORMEL, 'von': max(x0, -150), 'bis': x1, 'farbe': TIN, 'dicke': 5, 'n': 300}], **kw)
    if punkte:
        g['punkte'] = punkte
    if extra:
        for k, v in extra.items():
            g.setdefault(k, []).extend(v)
    return g


def zickzack(n=26, seed=4):
    rnd = random.Random(seed)
    x, y, pts = 5.0, 5.0, [(5.0, 5.0)]
    for _ in range(n):
        w = rnd.random() * 2 * math.pi
        l = 0.35 + rnd.random() * 0.9
        x = min(9.2, max(0.8, x + l * math.cos(w)))
        y = min(9.2, max(0.8, y + l * math.sin(w)))
        pts.append((round(x, 3), round(y, 3)))
    return pts


# ================================================================== Kapitel 1: Teilchenbewegung
weg = zickzack()
weg_strecken = [S(weg[i], weg[i + 1], TIN, 3, ein=round(0.6 + 0.32 * i, 2)) for i in range(len(weg) - 1)]
# Das Tröpfchen steht immer am Ende des schon gezeichneten Wegs
weg_punkte = [{'x': weg[0][0], 'y': weg[0][1], 'farbe': TIN, 'aus': weg_strecken[0]['ein']}]
for i, sg in enumerate(weg_strecken):
    q = {'x': sg['bis'][0], 'y': sg['bis'][1], 'farbe': TIN, 'ein': sg['ein']}
    if i + 1 < len(weg_strecken):
        q['aus'] = weg_strecken[i + 1]['ein']
    weg_punkte.append(q)
rnd = random.Random(9)
umgeb = []
for k in range(14):
    w = 2 * math.pi * k / 14 + rnd.random() * 0.3
    umgeb.append((5 + 3.1 * math.cos(w), 5 + 3.1 * math.sin(w), w))
stoss_kurz = [P((x, y), (x - 0.7 * math.cos(w), y - 0.7 * math.sin(w)), TIN, 4) for x, y, w in umgeb]
# Überwiegen: erst links stärkere Stösse, dann rechts (Tinte), dann wärmer: alle stärker (Orange).
# "_anker"/"_aus_anker" an Teilen setzt zeiten.py nach der Vertonung auf die Sprechzeit.
stoss_seite = ([dict(P((x, y), (x - 1.25 * math.cos(w), y - 1.25 * math.sin(w)), TIN, 6), _anker='Mal überwiegen', _aus_anker='dann wieder die von rechts') for x, y, w in umgeb if x < 4.6]
               + [dict(P((x, y), (x - 1.25 * math.cos(w), y - 1.25 * math.sin(w)), TIN, 6), _anker='dann wieder die von rechts', _aus_anker='stossen die Teilchen heftiger') for x, y, w in umgeb if x > 5.4])
stoss_lang = [dict(P((x, y), (x - 1.4 * math.cos(w), y - 1.4 * math.sin(w)), ORA, 5), _anker='stossen die Teilchen heftiger') for x, y, w in umgeb]
teilchen_fig = [kreis(5, 5, 1.2, TIN, 0.25)] + [kreis(x, y, 0.25, TIN, 0.9, dicke=2) for x, y, w in umgeb]

DREH.append(dict(KOPF, titel='Temperatur sehen: was sich bewegt, wenn es wärmer wird', dateiname='p5-1-lp-teilchen',
    kurzbeschrieb='Die Brown\'sche Bewegung, die Temperatur als Mass für die mittlere Bewegungsenergie der Teilchen, der Mittelwert über viele Teilchen und die tiefste Temperatur — und ein vorgerechnetes Problem: wie viel schneller die Luft im Föhn wird.',
    schlagworte=['Temperatur', 'Teilchenbewegung', 'Brown\'sche Bewegung', 'mittlere Bewegungsenergie', 'absoluter Nullpunkt'], _probe=EIN % 1,
    szenen=[
        sz('Zittern', 'Unter dem Mikroskop zittert ein winziges Fetttröpfchen in Milch hin und her, ohne Pause. Niemand stösst es an — oder doch?',
           titel('Warum zittert das Tröpfchen?', y=280, g=60),
           notiz('Fetttröpfchen in Milch,|unter dem Mikroskop', y=440, ein=1.0),
           graf([0, 10], [0, 10], achsen=False, strecken=weg_strecken,
                punkte=weg_punkte, texte=[T(5, 0.4, 'Weg des Tröpfchens', TIN, 26)])),
        sz('Stösse', 'Das Tröpfchen ist von unzähligen Wasserteilchen umgeben, die sich ständig bewegen und es von allen Seiten anstossen. Mal überwiegen die Stösse von links, dann wieder die von rechts, und das Tröpfchen wird hin und her geschoben. Wird die Milch wärmer, stossen die Teilchen heftiger, und das Tröpfchen zittert stärker.',
           notiz('Stösse von allen Seiten', y=300, ein=1.0, a='von allen Seiten'),
           notiz('wärmer: heftigere Stösse', y=420, ein=8.0, a='Wird die Milch wärmer', farbe='gold'),
           graf([0, 10], [0, 10], achsen=False, figuren=teilchen_fig, strecken=stoss_kurz,
                texte=[T(5, 5, 'Tröpfchen', TIN, 26), T(5, 0.6, 'Wasserteilchen (vergrössert)', TIN, 24)]),
           graf([0, 10], [0, 10], achsen=False, strecken=stoss_seite + stoss_lang)),
        sz('Temperatur', 'Die Temperatur ist ein Mass für die mittlere Bewegungsenergie der Teilchen. In der Simulation fliegen Stickstoffteilchen, der Hauptteil der Luft: bei zwanzig Grad Celsius im Mittel mit rund vierhunderteinundsiebzig Metern pro Sekunde, bei hundertfünfzig Grad mit rund fünfhundertsechsundsechzig.',
           notiz('Temperatur: Mass für die|mittlere Bewegungsenergie|der Teilchen', y=280, ein=0.6, g=46),
           formel(r'20\,^\circ\text{C}: \;471\;\text{m/s}', y=520, g=44, a='bei zwanzig Grad'),
           formel(r'150\,^\circ\text{C}: \;566\;\text{m/s}', y=620, g=44, a='bei hundertfünfzig'),
           bild('p5-1-lp-teilchen-20.jpg', a='bei zwanzig Grad'),
           bild('p5-1-lp-teilchen-150.jpg', a='bei hundertfünfzig')),
        sz('Mittelwert', 'Nicht alle Teilchen sind gleich schnell. Das markierte fliegt bei zwanzig Grad mit rund sechshunderteinundachtzig Metern pro Sekunde, andere sind viel langsamer. Die Temperatur gehört zum Mittelwert über sehr viele Teilchen. Ein einzelnes Teilchen hat keine Temperatur.',
           notiz('◎ markiert: 681 m/s|Mittel: 471 m/s', y=300, ein=1.0, a='Das markierte'),
           notiz('Temperatur = Mittelwert|über sehr viele Teilchen', y=500, ein=6.0, a='Die Temperatur gehört', farbe='gold'),
           bild('p5-1-lp-teilchen-20.jpg')),
        sz('Kälter', 'Kühlt man ab, werden die Teilchen langsamer: bei hundertfünfzig Grad rund fünfhundertsechsundsechzig, bei fünfzig Grad rund vierhundertvierundneunzig, bei minus hundert Grad rund dreihundertzweiundsechzig Meter pro Sekunde. Es gibt eine tiefste Temperatur, bei der die Bewegung minimal ist: den absoluten Nullpunkt, bei minus zweihundertdreiundsiebzig Komma eins fünf Grad Celsius.',
           formel(r'150\,^\circ\text{C}: \;566\;\text{m/s}', y=280, g=42, a='bei hundertfünfzig'),
           formel(r'50\,^\circ\text{C}: \;494\;\text{m/s}', y=370, g=42, a='bei fünfzig'),
           formel(r'-100\,^\circ\text{C}: \;362\;\text{m/s}', y=460, g=42, a='bei minus hundert'),
           notiz('absoluter Nullpunkt:|−273.15 °C, Bewegung minimal', y=580, ein=12.0, a='den absoluten Nullpunkt', farbe='gruen'),
           bild('p5-1-lp-teilchen-150.jpg', a='bei hundertfünfzig'),
           bild('p5-1-lp-teilchen-50.jpg', a='bei fünfzig'),
           bild('p5-1-lp-teilchen-m100.jpg', a='bei minus hundert')),
        sz('Problem Föhn', 'Jetzt ein ganzes Problem. Ein Föhn erwärmt Luft von zwanzig auf achtzig Grad Celsius. Bei zwanzig Grad fliegen die Stickstoffteilchen, der Hauptteil der Luft, im Mittel mit vierhunderteinundsiebzig Metern pro Sekunde. Wie schnell sind sie bei achtzig Grad?',
           notiz('Föhn: Luft von 20 °C auf 80 °C|Stickstoff bei 20 °C: 471 m/s', y=300, ein=2.0, a='Ein Föhn'),
           notiz('gesucht: mittleres Tempo|bei 80 °C', y=480, ein=8.0, a='Wie schnell', farbe='gold'),
           tempo_graf(punkte=[{'x': 20, 'y': round(vm(20), 2), 'farbe': CEL, 'beschriftung': '(20 °C; 471 m/s)', 'beschriftung_bei': [26, 420], 'anker': 'start'}])),
        sz('Vorgehen Föhn', 'Die Kurve zeigt das mittlere Tempo zu jeder Temperatur. Also liest man bei achtzig Grad ab, statt mit den Celsius-Zahlen zu rechnen.',
           notiz('bei 80 °C an der Kurve ablesen', y=300, ein=1.0, a='Also liest man'),
           tempo_graf(punkte=[{'x': 20, 'y': round(vm(20), 2), 'farbe': CEL}]),
           graf([-40, 140], [-60, 700], achsen=False, a='Also liest man',
                strecken=[S((80, 0), (80, vm(80)), CEL, 3, gestrichelt=True), S((80, vm(80)), (0, vm(80)), CEL, 3, gestrichelt=True)])),
        sz('Lösung Föhn', 'Abgelesen: rund fünfhundertsiebzehn Meter pro Sekunde. Die Zunahme ist sechsundvierzig Meter pro Sekunde, geteilt durch vierhunderteinundsiebzig: knapp zehn Prozent, nicht das Vierfache. Probe: Die Kurve steigt flach. Viermal so viele Grad Celsius heisst nicht viermal so schnell.',
           formel(r'80\,^\circ\text{C}: \;517\;\text{m/s}', y=280, g=44, ein=0.4, a='Abgelesen'),
           formel(r'\frac{517\;\text{m/s} - 471\;\text{m/s}}{471\;\text{m/s}} \approx 0.098', y=400, g=40, a='Die Zunahme'),
           formel(r'\approx 10\,\%', y=520, g=44, a='knapp zehn Prozent'),
           notiz('Probe: Kurve flach —|nicht viermal so schnell', y=620, a='Probe', farbe='gold'),
           tempo_graf(punkte=[{'x': 20, 'y': round(vm(20), 2), 'farbe': CEL},
                              {'x': 80, 'y': round(vm(80), 2), 'farbe': CEL, 'beschriftung': '(80 °C; 517 m/s)', 'beschriftung_bei': [76, 590], 'anker': 'end'}]),
           graf([-40, 140], [-60, 700], achsen=False, a='Die Zunahme',
                strecken=[S((20, vm(20)), (80, vm(20)), TIN, 3, gestrichelt=True),
                          P((86, vm(20)), (86, vm(80)), ORA, 5)],
                texte=[T(90, 480, '+46 m/s', ORA, 28, 'start')])),
        sz('Merke', 'Zum Mitnehmen: Die Temperatur misst die mittlere Bewegungsenergie der Teilchen. Wärmer heisst im Mittel schneller. Die tiefste Temperatur ist der absolute Nullpunkt.',
           titel('Zum Mitnehmen', y=260, g=76),
           notiz('Temperatur: Mass für die|mittlere Bewegungsenergie', y=400, ein=0.6),
           notiz('wärmer: im Mittel schneller', y=560, a='Wärmer heisst', farbe='gold'),
           notiz('tiefste Temperatur: −273.15 °C', y=680, ein=6.0, a='Die tiefste', farbe='gruen')),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Föhn', 'Wie findest du das mittlere Tempo bei 80 °C?',
                 ['471 m/s mal 4, weil 80 °C viermal 20 °C sind', 'An der Kurve bei 80 °C ablesen', 'Es bleibt bei 471 m/s'], 1,
                 {0: 'Geht die Kurve durch den Nullpunkt der Celsius-Skala? Schau sie an.', 2: 'Wärmer heisst im Mittel schneller. Was zeigt die Kurve?'},
                 sprich='Wie findest du das mittlere Tempo bei achtzig Grad Celsius?', kopf='Dein Vorgehen')]))

DREH.append(dict(KOPF, titel='Temperatur sehen: Kontrollfragen zur Temperatur', dateiname='p5-1-lp-kontrolle-teilchen',
    kurzbeschrieb='Fünf Fragen zur Teilchenbewegung: ruhendes Wasser, ein schnelles Teilchen, Luft im heissen Auto, ein Duft im warmen Zimmer und die tiefste Temperatur.',
    schlagworte=['Temperatur', 'Teilchenbewegung', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Die Teilchen bewegen sich ständig und ungeordnet, auch wenn das Wasser von aussen ruht. Bei achtzehn Grad Celsius ist ihre Bewegung weit vom Minimum entfernt.',
           notiz('ständig und ungeordnet —|auch im ruhigen Glas', y=300, ein=1.0)),
        sz('Frage 2', 'Ein einzelnes Teilchen hat keine Temperatur. Die Temperatur gehört zum Mittelwert über sehr viele Teilchen; einzelne sind immer schneller oder langsamer.',
           notiz('Temperatur gehört|zum Mittelwert', y=300, ein=1.0)),
        sz('Frage 3', 'Schneller, aber nur um rund fünf Prozent: Die Stickstoffteilchen fliegen im Mittel statt mit rund vierhundertdreiundachtzig mit rund fünfhundertneun Metern pro Sekunde. Doppelte Celsius-Zahl heisst nicht doppeltes Tempo.',
           formel(r'35\,^\circ\text{C}: \;483\;\text{m/s}', y=280, g=42, ein=1.0),
           formel(r'70\,^\circ\text{C}: \;509\;\text{m/s}', y=380, g=42, ein=1.0),
           notiz('Stickstoff: nur rund 5 % schneller', y=500, ein=1.0)),
        sz('Frage 4', 'Im warmen Glas bewegen sich die Teilchen heftiger. Die Duftteilchen werden schneller durch das ganze Glas gestossen und sind früher oben am Deckel.',
           notiz('wärmer: heftigere Bewegung,|Duft verteilt sich schneller', y=300, ein=1.0)),
        sz('Frage 5', 'Die Teilchen werden immer langsamer. Bei minus zweihundertdreiundsiebzig Komma eins fünf Grad Celsius, dem absoluten Nullpunkt, ist die Bewegung minimal; kälter geht es nicht. Null Grad Celsius ist nur der Schmelzpunkt des Wassers.',
           notiz('absoluter Nullpunkt:|−273.15 °C', y=300, ein=1.0, farbe='gruen')),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Glas Wasser steht seit Stunden ruhig auf dem Tisch, bei 18 °C. Was tun seine Teilchen?',
             ['Sie ruhen, weil das Wasser ruht', 'Sie bewegen sich ständig und ungeordnet', 'Nur die Teilchen an der Oberfläche bewegen sich'], 1,
             {0: 'Kann man die Bewegung der Teilchen von aussen sehen? Denk an das zitternde Tröpfchen.', 2: 'Wovon hängt die Bewegung ab: von der Lage im Glas oder von der Temperatur?'},
             sprich='Ein Glas Wasser steht seit Stunden ruhig auf dem Tisch, bei achtzehn Grad Celsius. Was tun seine Teilchen?'),
        wahl('Frage 2', 'In der Luft fliegt ein Teilchen gerade doppelt so schnell wie der Durchschnitt. Was folgt daraus für die Temperatur?',
             ['Dieses Teilchen ist doppelt so heiss', 'Die Luft wird gerade wärmer', 'Nichts: Die Temperatur gehört zum Mittelwert'], 2,
             {0: 'Hat ein einzelnes Teilchen eine Temperatur?', 1: 'Ändert ein einzelnes schnelles Teilchen den Mittelwert von Milliarden?'}),
        wahl('Frage 3', 'Luft in einem Auto in der Sonne: am Morgen 35 °C, am Mittag 70 °C. Fliegen die Stickstoffteilchen der Luft am Mittag doppelt so schnell?',
             ['Nein: schneller, aber viel weniger als doppelt', 'Ja: doppelte Temperatur, doppeltes Tempo', 'Nein: gleich schnell'], 0,
             {1: 'Geht die Kurve des mittleren Tempos durch den Nullpunkt der Celsius-Skala?', 2: 'Was geschieht mit der Bewegung, wenn es wärmer wird?'},
             sprich='Luft in einem Auto in der Sonne: am Morgen fünfunddreissig Grad, am Mittag siebzig Grad Celsius. Fliegen die Stickstoffteilchen der Luft am Mittag doppelt so schnell?'),
        wahl('Frage 4', 'Zwei gleiche, verschlossene Gläser, unten je ein Tropfen Parfüm: eines bei 10 °C, eines bei 30 °C. In welchem riecht man den Duft oben am Deckel zuerst?',
             ['Im kalten: Kalte Luft trägt Duft besser', 'Gleich schnell: Die Gläser sind gleich gross', 'Im warmen: Die Teilchen bewegen sich heftiger'], 2,
             {0: 'Wovon hängt ab, wie heftig sich die Teilchen bewegen?', 1: 'Spielt die Temperatur für die Bewegung der Teilchen keine Rolle?'},
             sprich='Zwei gleiche, verschlossene Gläser, unten je ein Tropfen Parfüm: eines bei zehn Grad, eines bei dreissig Grad Celsius. In welchem riecht man den Duft oben am Deckel zuerst?'),
        wahl('Frage 5', 'Man kühlt ein Gas immer weiter ab. Was geschieht mit seinen Teilchen?',
             ['Bei 0 °C stehen sie still', 'Sie werden langsamer, bis die Bewegung bei −273.15 °C minimal ist', 'Sie werden langsamer, und man kann beliebig weit abkühlen'], 1,
             {0: 'Null Grad Celsius ist der Schmelzpunkt des Wassers. Bewegen sich Teilchen dort noch?', 2: 'Kann eine Bewegung kleiner werden als minimal?'},
             sprich='Man kühlt ein Gas immer weiter ab. Was geschieht mit seinen Teilchen?'),
    ]))

# ================================================================== Kapitel 2: Aggregatzustände
STOFFE3 = [('Wasser', 0, 100), ('Ethanol', -114, 78), ('Glycerin', 18, 290)]


def messlinie(x, farbe=CEL):
    """Senkrechte gestrichelte Linie über die drei Schienen, unterbrochen bei den Zahlen der Schmelz- und Siedepunkte."""
    st, y = [], -1.0
    for g in (1.45, 4.05, 6.65):
        st.append(S((x, y), (x, g), farbe, 4, gestrichelt=True)); y = g + 0.6
    st.append(S((x, y), (x, 9.6), farbe, 4, gestrichelt=True))
    return st


def baender(stoffe, x0, x1, ein=0.05, a=None, extra=None, nur=None, achsen=True):
    """Zustandsschienen (fest dunkel, flüssig mittel, gasförmig hell) je Stoff, Achse ϑ in °C, Fenster y −1.5 bis 10.
    nur: Indizes der Zeilen, die dieses Bild zeichnet (Ebenen für eine Bildfolge)."""
    fl, tx = [], []
    for k, (n, smp, sdp) in enumerate(stoffe):
        if nur is not None and k not in nur:
            continue
        y0 = 7.4 - 2.6 * k
        fl += [F(rechteck(x0, y0, smp, y0 + 1.4), TIN, 0.5), F(rechteck(smp, y0, sdp, y0 + 1.4), TIN, 0.26),
               F(rechteck(sdp, y0, x1, y0 + 1.4), TIN, 0.08)]
        tx += [T(x0 + (x1 - x0) * 0.01, y0 + 1.75, n, TIN, 26, 'start'),
               T(smp, y0 - 0.45, ('%g' % smp).replace('-', '−'), CEL, 22), T(sdp, y0 - 0.45, ('%g' % sdp).replace('-', '−'), CEL, 22)]
    if achsen:
        g = graf([x0, x1], [-1.5, 10], [v for v in range(-300, 3001, 100) if x0 < v < x1], [], 'ϑ [°C]', '', ein=ein, a=a, flaechen=fl, texte=tx)
    else:
        g = graf([x0, x1], [-1.5, 10], achsen=False, ein=ein, a=a, flaechen=fl, texte=tx)
    if extra:
        for k_, v in extra.items():
            g.setdefault(k_, []).extend(v)
    return g


DREH.append(dict(KOPF, titel='Temperatur sehen: fest, flüssig, gasförmig', dateiname='p5-1-lp-aggregat',
    kurzbeschrieb='Eis, Wasser und Dampf im Teilchenbild, die Übergänge und ihre Namen, Schmelz- und Siedepunkte als Eigenschaft des Stoffes — und ein vorgerechnetes Problem: welche Flüssigkeit in ein Thermometer passt.',
    schlagworte=['Aggregatzustand', 'Teilchenmodell', 'Schmelzpunkt', 'Siedepunkt', 'schmelzen', 'verdampfen'], _probe=EIN % 2,
    szenen=[
        sz('Eis', 'Eis, Wasser und Dampf bestehen aus denselben Wasserteilchen. Was sich ändert, ist ihre Anordnung und ihre Bewegung — und das hängt von der Temperatur ab.',
           titel('Eis, Wasser, Dampf', y=280, g=64),
           notiz('dieselben Teilchen,|andere Anordnung und Bewegung', y=440, ein=4.0, a='Was sich ändert'),
           bild('p5-1-lp-aggregat-m15.jpg', breite=240, x=1010, y=330, ein=0.4),
           bild('p5-1-lp-aggregat-50.jpg', breite=240, x=1270, y=330, ein=0.8),
           bild('p5-1-lp-aggregat-120.jpg', breite=240, x=1530, y=330, ein=1.2),
           notiz('Eis', x=1080, y=650, breite=200, ein=0.4, g=38), notiz('Wasser', x=1320, y=650, breite=200, ein=0.8, g=38),
           notiz('Dampf', x=1590, y=650, breite=200, ein=1.2, g=38)),
        sz('fest', 'Im festen Eis sitzen die Teilchen an festen Plätzen und schwingen nur um ihre Ruhelage. Darum behält ein Festkörper seine Form.',
           notiz('fest: feste Plätze,|nur Schwingen', y=300, ein=1.0, a='Im festen Eis'),
           notiz('formstabil', y=480, a='Darum behält'),
           bild('p5-1-lp-aggregat-m15.jpg', breite=520, x=1100, y=200)),
        sz('flüssig', 'Beim Schmelzpunkt, null Grad Celsius, verlassen die Teilchen ihre Plätze; Eis und Wasser bestehen nebeneinander. Im flüssigen Wasser berühren sich die Teilchen noch, lassen sich aber gegeneinander verschieben. Die Flüssigkeit nimmt die Form des Gefässes an.',
           notiz('schmelzen bei 0 °C', y=300, ein=1.0, a='Beim Schmelzpunkt'),
           notiz('flüssig: dicht,|verschiebbar', y=440, a='Im flüssigen Wasser'),
           bild('p5-1-lp-aggregat-0.jpg', breite=520, x=1100, y=200, a='Beim Schmelzpunkt'),
           bild('p5-1-lp-aggregat-50.jpg', breite=520, x=1100, y=200, a='Im flüssigen Wasser')),
        sz('gasförmig', 'Beim Siedepunkt, hundert Grad Celsius, siedet das Wasser: Im ganzen Innern bildet sich Dampf. Im Dampf fliegen die Teilchen mit grossen Abständen frei umher und füllen jeden Raum. Einzelne besonders schnelle Teilchen verlassen die Oberfläche schon vorher: Wasser verdunstet auch unter hundert Grad.',
           notiz('sieden bei 100 °C', y=280, ein=1.0, a='Beim Siedepunkt'),
           notiz('gasförmig: frei,|grosse Abstände', y=400, a='Im Dampf fliegen'),
           notiz('verdunsten: schon|unter 100 °C', y=560, a='Einzelne besonders schnelle', farbe='gold'),
           bild('p5-1-lp-aggregat-100.jpg', breite=520, x=1100, y=200, a='Beim Siedepunkt'),
           bild('p5-1-lp-aggregat-120.jpg', breite=520, x=1100, y=200, a='Im Dampf fliegen')),
        sz('Umgekehrt', 'Kühlt man ab, läuft alles rückwärts: Der Dampf kondensiert zu Wasser, das Wasser erstarrt zu Eis.',
           formel(r'\text{schmelzen} \;\leftrightarrow\; \text{erstarren}', y=300, g=46, ein=1.0),
           formel(r'\text{verdampfen} \;\leftrightarrow\; \text{kondensieren}', y=420, g=46, ein=1.0),
           bild('p5-1-lp-aggregat-120.jpg', breite=520, x=1100, y=200),
           bild('p5-1-lp-aggregat-50.jpg', breite=520, x=1100, y=200, a='kondensiert'),
           bild('p5-1-lp-aggregat-m15.jpg', breite=520, x=1100, y=200, a='erstarrt')),
        sz('Stoffe', 'Schmelz- und Siedepunkt gehören zum Stoff und gelten bei Normaldruck. Zwischen den Teilchen wirken Anziehungskräfte, und die sind von Stoff zu Stoff verschieden stark. Wasser: null und hundert Grad Celsius. Ethanol: minus hundertvierzehn und achtundsiebzig Grad. Glycerin: achtzehn und zweihundertneunzig Grad.',
           notiz('Schmelz- und Siedepunkt:|Eigenschaft des Stoffes|(bei Normaldruck)', y=280, ein=1.0),
           notiz('Anziehungskräfte zwischen|den Teilchen: je nach Stoff', y=480, a='Zwischen den Teilchen', farbe='gold', g=40),
           notiz('dunkel: fest|mittel: flüssig|hell: gasförmig', y=640, a='Wasser:', g=36),
           baender(STOFFE3, -150, 400, a='Wasser:', nur=[0]),
           baender(STOFFE3, -150, 400, a='Ethanol:', nur=[1], achsen=False),
           baender(STOFFE3, -150, 400, a='Glycerin:', nur=[2], achsen=False)),
        sz('Problem Thermometer', 'Jetzt ein ganzes Problem. Für ein Aussenthermometer in Davos, bis minus fünfundzwanzig Grad, und für ein Backofenthermometer, von fünfzig bis zweihundertfünfzig Grad, suchst du die Flüssigkeit: Wasser, Ethanol oder Glycerin. Welche bleibt im ganzen Messbereich flüssig?',
           notiz('Davos: bis −25 °C|Backofen: 50 °C bis 250 °C', y=300, ein=2.0, a='Für ein Aussenthermometer'),
           notiz('gesucht: flüssig im|ganzen Messbereich', y=480, a='Welche bleibt', farbe='gold'),
           baender(STOFFE3, -150, 400)),
        sz('Vorgehen Thermometer', 'Flüssig ist ein Stoff zwischen seinem Schmelz- und seinem Siedepunkt. Man legt also die Grenzen der Messbereiche neben die Bereiche der Stoffe.',
           notiz('flüssig: zwischen Schmelz-|und Siedepunkt', y=300, ein=1.0, a='Flüssig ist'),
           baender(STOFFE3, -150, 400),
           graf([-150, 400], [-1.5, 10], achsen=False, a='Man legt also',
                strecken=messlinie(-25) + messlinie(250),
                texte=[T(-25, 9.75, '−25 °C', CEL, 24), T(250, 9.75, '250 °C', CEL, 24)])),
        sz('Lösung Thermometer', 'Davos, minus fünfundzwanzig Grad: Wasser und Glycerin sind dort fest, denn minus fünfundzwanzig liegt unter ihren Schmelzpunkten. Ethanol ist flüssig. Backofen, bis zweihundertfünfzig Grad: Wasser und Ethanol sieden vorher, Glycerin erst bei zweihundertneunzig Grad. Also Ethanol für Davos und Glycerin für den Backofen; keine der drei passt für beide. Probe: Ethanol ist von minus hundertvierzehn bis achtundsiebzig Grad flüssig, Glycerin von achtzehn bis zweihundertneunzig.',
           notiz('Davos: Ethanol|(Wasser, Glycerin fest)', y=280, ein=1.0, a='Ethanol ist flüssig'),
           notiz('Backofen: Glycerin|(Wasser, Ethanol sieden)', y=440, a='Glycerin erst bei'),
           notiz('Probe: −114 °C bis 78 °C|und 18 °C bis 290 °C', y=620, a='Probe', farbe='gold'),
           baender(STOFFE3, -150, 400),
           graf([-150, 400], [-1.5, 10], achsen=False,
                strecken=messlinie(-25) + messlinie(250),
                texte=[T(-25, 9.75, '−25 °C', CEL, 24), T(250, 9.75, '250 °C', CEL, 24)]),
           graf([-150, 400], [-1.5, 10], achsen=False, a='Wasser und Glycerin sind dort fest',
                punkte=[{'x': -25, 'y': 8.1, 'farbe': TIN}, {'x': -25, 'y': 2.9, 'farbe': TIN}],
                texte=[T(-37, 8.6, 'fest', TIN, 22, 'end'), T(-37, 3.4, 'fest', TIN, 22, 'end')]),
           graf([-150, 400], [-1.5, 10], achsen=False, a='Ethanol ist flüssig',
                punkte=[{'x': -25, 'y': 5.5, 'farbe': TIN}], texte=[T(-13, 6.0, 'flüssig', TIN, 22, 'start')]),
           graf([-150, 400], [-1.5, 10], achsen=False, a='Wasser und Ethanol sieden vorher',
                punkte=[{'x': 250, 'y': 8.1, 'farbe': TIN}, {'x': 250, 'y': 5.5, 'farbe': TIN}],
                texte=[T(262, 8.6, 'gasförmig', TIN, 22, 'start'), T(262, 6.0, 'gasförmig', TIN, 22, 'start')]),
           graf([-150, 400], [-1.5, 10], achsen=False, a='Glycerin erst bei',
                punkte=[{'x': 250, 'y': 2.9, 'farbe': TIN}], texte=[T(262, 3.4, 'flüssig', TIN, 22, 'start')])),
        sz('Merke', 'Zum Mitnehmen: Anziehungskräfte halten die Teilchen zusammen. Je heftiger sich die Teilchen bewegen, desto weniger halten sie zusammen: fest, flüssig, gasförmig. Unter dem Schmelzpunkt fest, zwischen Schmelz- und Siedepunkt flüssig, darüber gasförmig.',
           titel('Zum Mitnehmen', y=260, g=76),
           notiz('Anziehungskräfte halten|die Teilchen zusammen', y=380, ein=0.6, farbe='gold'),
           notiz('je heftiger die Bewegung:|fest → flüssig → gasförmig', y=540, a='Je heftiger'),
           notiz('unter Schmelzpunkt fest,|darüber flüssig, über Siedepunkt gasförmig', y=700, a='Unter dem Schmelzpunkt', g=40)),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Thermometer', 'Was vergleichst du?',
                 ['Die Dichten der drei Flüssigkeiten', 'Den Messbereich mit Schmelz- und Siedepunkt', 'Nur den Siedepunkt'], 1,
                 {0: 'Was entscheidet, ob ein Stoff flüssig ist?', 2: 'Kann eine Thermometerflüssigkeit auch fest werden?'}, kopf='Dein Vorgehen')]))

DREH.append(dict(KOPF, titel='Temperatur sehen: Kontrollfragen zu den Aggregatzuständen', dateiname='p5-1-lp-kontrolle-aggregat',
    kurzbeschrieb='Fünf Fragen zu Aggregatzuständen: flüssiger Sauerstoff, schmelzendes Zinn, Gas und Flüssigkeit zusammendrücken, erstarrendes Kerzenwachs, Wasser und Ethanol.',
    schlagworte=['Aggregatzustand', 'Schmelzpunkt', 'Siedepunkt', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Minus zweihundert Grad liegt über dem Schmelzpunkt, minus zweihundertneunzehn Grad, und unter dem Siedepunkt, minus hundertdreiundachtzig Grad. Sauerstoff ist dort flüssig.',
           formel(r'-219\,^\circ\text{C} \lt -200\,^\circ\text{C} \lt -183\,^\circ\text{C}', y=300, g=40, ein=1.0),
           notiz('Sauerstoff flüssig', y=440, ein=1.0)),
        sz('Frage 2', 'Zwischen zwanzig und dreihundert Grad liegt der Schmelzpunkt von Zinn, zweihundertzweiunddreissig Grad. Das Zinn schmilzt: Es wird von fest zu flüssig.',
           notiz('schmelzen bei 232 °C|(fest → flüssig)', y=300, ein=1.0)),
        sz('Frage 3', 'Im Gas sind die Abstände zwischen den Teilchen gross; man kann sie zusammenschieben. In der Flüssigkeit berühren sich die Teilchen schon.',
           notiz('Gas: grosse Abstände|Flüssigkeit: Teilchen berühren sich', y=300, ein=1.0)),
        sz('Frage 4', 'Das Wachs erstarrt: Es wird von flüssig zu fest. Die Teilchen werden langsamer und finden feste Plätze, um die sie nur noch schwingen.',
           notiz('erstarren: flüssig → fest', y=300, ein=1.0),
           notiz('Teilchen langsamer,|feste Plätze', y=440, ein=1.0)),
        sz('Frage 5', 'Bei tausendsechshundert Grad Celsius sind beide flüssig: Eisen ist ab tausendfünfhundertachtunddreissig Grad geschmolzen, und Blei siedet erst bei tausendsiebenhundertneunundvierzig Grad.',
           notiz('beide flüssig zwischen|1538 °C und 1749 °C', y=300, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Sauerstoff schmilzt bei −219 °C und siedet bei −183 °C. In welchem Zustand ist er bei −200 °C?',
             ['fest', 'flüssig', 'gasförmig'], 1,
             {0: 'Liegt −200 °C unter dem Schmelzpunkt −219 °C? Vorsicht mit dem Minus.', 2: 'Liegt −200 °C über dem Siedepunkt −183 °C?'},
             rueck_sprich={0: 'Liegt minus zweihundert Grad unter dem Schmelzpunkt, minus zweihundertneunzehn Grad? Vorsicht mit dem Minus.',
                           2: 'Liegt minus zweihundert Grad über dem Siedepunkt, minus hundertdreiundachtzig Grad?'},
             sprich='Sauerstoff schmilzt bei minus zweihundertneunzehn Grad und siedet bei minus hundertdreiundachtzig Grad Celsius. In welchem Zustand ist er bei minus zweihundert Grad?'),
        wahl('Frage 2', 'Zinn schmilzt bei 232 °C und siedet bei 2602 °C. Ein Stück Zinn wird von 20 °C auf 300 °C erhitzt. Welcher Übergang findet statt?',
             ['verdampfen', 'erstarren', 'schmelzen'], 2,
             {0: 'Welcher Punkt liegt zwischen 20 °C und 300 °C: der Schmelz- oder der Siedepunkt?', 1: 'Wird das Zinn erwärmt oder abgekühlt?'},
             rueck_sprich={0: 'Welcher Punkt liegt zwischen zwanzig und dreihundert Grad: der Schmelz- oder der Siedepunkt?'},
             sprich='Zinn schmilzt bei zweihundertzweiunddreissig Grad und siedet bei zweitausendsechshundertzwei Grad Celsius. Ein Stück Zinn wird von zwanzig auf dreihundert Grad erhitzt. Welcher Übergang findet statt?'),
        wahl('Frage 3', 'Warum lässt sich ein Gas leicht zusammendrücken, eine Flüssigkeit kaum?',
             ['Im Gas sind die Abstände zwischen den Teilchen gross', 'Gasteilchen sind kleiner', 'Gasteilchen sind weicher'], 0,
             {1: 'Sind die Teilchen im Dampf kleiner als im Wasser?', 2: 'Lassen sich die Teilchen selbst zusammendrücken?'}),
        wahl('Frage 4', 'Flüssiges Kerzenwachs tropft auf den Tisch und wird hart. Wie heisst der Übergang, und was tun die Teilchen?',
             ['Schmelzen: Die Teilchen werden schneller', 'Erstarren: Die Teilchen werden langsamer und finden feste Plätze', 'Kondensieren: Die Teilchen rücken zusammen'], 1,
             {0: 'Wird das Wachs dabei wärmer oder kälter?', 2: 'Kondensieren beginnt bei einem Gas. War das Wachs ein Gas?'}),
        wahl('Frage 5', 'Blei schmilzt bei 327 °C und siedet bei 1749 °C, Eisen schmilzt bei 1538 °C und siedet bei 2862 °C. Bei welcher Temperatur sind beide flüssig?',
             ['1000 °C', '1800 °C', '1600 °C'], 2,
             {0: 'Ist Eisen bei 1000 °C schon geschmolzen?', 1: 'Ist Blei bei 1800 °C noch flüssig?'},
             sprich='Blei schmilzt bei dreihundertsiebenundzwanzig Grad und siedet bei tausendsiebenhundertneunundvierzig Grad, Eisen schmilzt bei tausendfünfhundertachtunddreissig Grad und siedet bei zweitausendachthundertzweiundsechzig Grad Celsius. Bei welcher Temperatur sind beide flüssig?',
             rueck_sprich={0: 'Ist Eisen bei tausend Grad schon geschmolzen?', 1: 'Ist Blei bei tausendachthundert Grad noch flüssig?'}),
    ]))

# ================================================================== Kapitel 3: Celsius und Kelvin


def thermometer(h, bahn=None, marken=(), ein=0.05, a=None, extra=None, ticks=False):
    """Thermometer: Röhre, Kugel, Faden (Bernstein) bis Höhe h; bahn [[Textstelle, Versatz s, Höhe], …] bewegt
    den Faden, sobald der Sprecher die Textstelle sagt (zeiten.py rechnet daraus die bewegung nach der Vertonung).
    marken [(y, Text links, Text rechts)]; Fenster 0 bis 10, quadratisch."""
    faden = {'art': 'vieleck', 'punkte': [[4.0, 1.85], [4.4, 1.85], [4.4, h], [4.0, h]], 'farbe': CEL, 'fuellung': 0.55, 'dicke': 0.01}
    if bahn:
        faden['_bahn'] = bahn
    fig = [kreis(4.2, 1.2, 0.75, TIN, None, 4), faden, kreis(4.2, 1.2, 0.62, CEL, 0.55, 0.01)]
    st = [S((3.95, 1.85), (3.95, 9.5), TIN, 4), S((4.45, 1.85), (4.45, 9.5), TIN, 4), S((3.95, 9.5), (4.45, 9.5), TIN, 4)]
    tx = []
    for y, links, rechts in marken:
        st.append(S((3.6, y), (4.8, y), CEL, 4))
        if links:
            tx.append(T(3.4, y - 0.15, links, CEL, 28, 'end'))
        if rechts:
            tx.append(T(5.0, y - 0.15, rechts, TIN, 26, 'start'))
    if ticks:
        for k in range(1, 10):
            st.append(S((4.45, 3 + 0.5 * k), (4.75, 3 + 0.5 * k), CEL, 2))
    g = graf([0, 10], [0, 10], achsen=False, ein=ein, a=a, figuren=fig, strecken=st, texte=tx)
    if extra:
        for k_, v in extra.items():
            g.setdefault(k_, []).extend(v)
    return g


def marken_ebene(marken, a, versatz=None, ticks=False):
    st, tx = [], []
    for y, links, rechts in marken:
        st.append(S((3.6, y), (4.8, y), CEL, 4))
        tx += [T(3.4, y - 0.15, links, CEL, 28, 'end'), T(5.0, y - 0.15, rechts, TIN, 26, 'start')]
    if ticks:
        st += [S((4.45, 3 + 0.5 * k), (4.75, 3 + 0.5 * k), CEL, 2) for k in range(1, 10)]
    return graf([0, 10], [0, 10], achsen=False, a=a, versatz=versatz, strecken=st, texte=tx)


def doppelstrahl(x0, x1, c_ticks, k_ticks, ein=0.05, a=None, extra=None, yc=6.5, yk=3.0):
    """Zwei Zahlenstrahlen: oben Celsius (Bernstein), unten Kelvin (Grün), x in °C."""
    st = [S((x0, yc), (x1, yc), CEL, 4), S((x0, yk), (x1, yk), KEL, 4)]
    tx = [T(x1, yc + 0.9, '°C', CEL, 28, 'end'), T(x1, yk + 0.9, 'K', KEL, 28, 'end')]
    for c in c_ticks:
        st.append(S((c, yc - 0.3), (c, yc + 0.3), CEL, 4))
        tx.append(T(c, yc - 0.9, ('%g' % c).replace('-', '−'), CEL, 24))
    for k in k_ticks:
        x = k - 273.15
        st.append(S((x, yk - 0.3), (x, yk + 0.3), KEL, 4))
        tx.append(T(x, yk - 0.9, '%g' % k, KEL, 24))
    g = graf([x0, x1], [0, 10], achsen=False, ein=ein, a=a, strecken=st, texte=tx)
    if extra:
        for k_, v in extra.items():
            g.setdefault(k_, []).extend(v)
    return g


def gasgraf(punkte, gerade=None, ein=0.05, a=None, extra=None):
    """Druck über Temperatur (Fenster wie Simulation 3)."""
    g = graf([-320, 130], [-150, 1650], [-300, -200, -100, 100], [500, 1000, 1500], 'ϑ [°C]', 'p [hPa]', ein=ein, a=a,
             punkte=[{'x': x, 'y': y, 'farbe': DRU} for x, y in punkte])
    if gerade:
        g['strecken'] = gerade
    if extra:
        for k_, v in extra.items():
            g.setdefault(k_, []).extend(v)
    return g


p20, p70 = 1000 * 293.15 / 273.15, 1000 * 343.15 / 273.15
q20, q70 = 600 * 293.15 / 273.15, 600 * 343.15 / 273.15
m1 = (1328 - 1035) / 80
n1 = 10 - 1035 / m1
DREH.append(dict(KOPF, titel='Temperatur sehen: zwei Skalen, zwei Nullpunkte', dateiname='p5-1-lp-skalen',
    kurzbeschrieb='Wie Celsius seine Skala an zwei Fixpunkten des Wassers festmachte, wie man mit einem Gasthermometer den absoluten Nullpunkt findet, warum die Kelvin-Skala dort beginnt und wo man welche Skala braucht — mit einem vorgerechneten Problem aus einer Messreihe.',
    schlagworte=['Celsius', 'Kelvin', 'Fixpunkt', 'absoluter Nullpunkt', 'Gasthermometer', 'Normaldruck'], _probe=EIN % 3,
    szenen=[
        sz('Skala', 'Ein Thermometer zeigt, wie hoch ein Flüssigkeitsfaden steigt. Damit daraus eine Temperatur wird, braucht die Skala feste Punkte.',
           titel('Woher kommen die Zahlen?', y=280, g=60),
           notiz('Skala braucht feste Punkte', y=440, a='braucht die Skala', farbe='gold'),
           thermometer(2.6, bahn=[['wie hoch', 0, 2.6], ['wie hoch', 2.0, 6.2]])),
        sz('Celsius', 'Anders Celsius schlug siebzehnhundertzweiundvierzig zwei Fixpunkte des Wassers vor, beide bei Normaldruck: schmelzendes Eis und siedendes Wasser. Heute gilt: Schmelzendes Eis hat null Grad, siedendes Wasser hundert Grad. Den Abstand teilt man in hundert gleiche Schritte. Celsius selbst hatte die Zahlen umgekehrt gesetzt; kurz nach seinem Tod wurde die Skala umgedreht.',
           notiz('Fixpunkte bei Normaldruck|(1013 hPa)', y=280, ein=1.0, a='beide bei Normaldruck'),
           notiz('heute: Eis 0 °C,|siedendes Wasser 100 °C', y=440, a='Heute gilt'),
           notiz('100 gleiche Schritte', y=600, a='Den Abstand', farbe='gold'),
           notiz('Celsius 1742: umgekehrt|(100 beim Eis, 0 beim Sieden)', y=700, a='Celsius selbst', g=36),
           thermometer(5.0, bahn=[['Schmelzendes Eis hat', 0, 5.0], ['Schmelzendes Eis hat', 1.5, 3.0], ['siedendes Wasser hundert', 0, 3.0], ['siedendes Wasser hundert', 1.8, 8.0]]),
           marken_ebene([(3.0, '0 °C', 'schmelzendes Eis')], 'Schmelzendes Eis hat', 1.5),
           marken_ebene([(8.0, '100 °C', 'siedendes Wasser')], 'siedendes Wasser hundert', 1.8),
           marken_ebene([], 'Den Abstand', ticks=True)),
        sz('Willkürlich', 'Die Wahl ist praktisch, denn Wasser gibt es überall. Aber sie hängt an einem einzigen Stoff: Bei null Grad Celsius hört keine Bewegung auf, und es gibt negative Temperaturen, zum Beispiel minus zwanzig Grad.',
           notiz('praktisch: Wasser gibt es überall', y=280, ein=1.0),
           notiz('aber willkürlich:|bei 0 °C keine Ruhe,|negative Temperaturen', y=440, a='Aber sie hängt', farbe='gold'),
           thermometer(4.0, bahn=[['und es gibt negative', 0, 4.0], ['und es gibt negative', 1.8, 2.0]],
                       marken=[(3.0, '0 °C', 'schmelzendes Eis'), (8.0, '100 °C', 'siedendes Wasser')], ticks=True),
           graf([0, 10], [0, 10], achsen=False, a='zum Beispiel minus zwanzig',
                strecken=[S((3.6, 2.0), (4.8, 2.0), CEL, 3)], texte=[T(3.4, 1.85, '−20 °C', CEL, 28, 'end')])),
        sz('Gas', 'Wo liegt der echte Nullpunkt? Man misst den Druck eines Gases in einem Kolben, dessen Volumen fest bleibt: bei zwanzig Grad tausenddreiundsiebzig Hektopascal, bei siebzig Grad tausendzweihundertsechsundfünfzig. Je kälter, desto kleiner der Druck.',
           notiz('Gas mit festem Volumen', y=280, ein=1.0, a='Man misst'),
           formel(r'20\,^\circ\text{C}: \;1073\;\text{hPa}', y=420, g=42, a='bei zwanzig Grad'),
           formel(r'70\,^\circ\text{C}: \;1256\;\text{hPa}', y=520, g=42, a='bei siebzig Grad'),
           bild('p5-1-lp-skalen-1.jpg', breite=600, a='bei zwanzig Grad'),
           bild('p5-1-lp-skalen-2.jpg', breite=600, a='bei siebzig Grad')),
        sz('Nullpunkt', 'Die Punkte liegen auf einer Geraden. Verlängert man sie bis zum Druck null, trifft sie die Temperaturachse bei minus zweihundertdreiundsiebzig Komma eins fünf Grad Celsius. Mit weniger Gas ist die Gerade flacher, trifft aber dieselbe Stelle. Das gilt für ein ideales Gas, solange es nicht flüssig wird. Kälter geht es nicht: Dort ist der absolute Nullpunkt, die Teilchenbewegung ist minimal.',
           notiz('Gerade bis p = 0 verlängern', y=280, ein=1.0, a='Verlängert man sie'),
           formel(r'p = 0 \text{ bei } {-273.15}\,^\circ\text{C}', y=400, g=42, a='trifft sie die Temperaturachse'),
           notiz('für jede Gasmenge', y=500, a='Mit weniger Gas'),
           notiz('(ideales Gas, nicht verflüssigt)', y=590, a='Das gilt für ein ideales', g=36),
           notiz('absoluter Nullpunkt', y=680, a='Kälter geht es nicht', farbe='gruen'),
           bild('p5-1-lp-skalen-2.jpg', breite=600),
           bild('p5-1-lp-skalen-3.jpg', breite=600, a='Verlängert man sie'),
           bild('p5-1-lp-skalen-4.jpg', breite=600, a='Mit weniger Gas')),
        sz('Kelvin', 'Lord Kelvin legte den Nullpunkt seiner Skala genau dorthin, mit derselben Schrittweite wie Celsius. Null Kelvin sind minus zweihundertdreiundsiebzig Komma eins fünf Grad Celsius; null Grad Celsius sind zweihundertdreiundsiebzig Komma eins fünf Kelvin. Negative Kelvin-Temperaturen gibt es nicht.',
           notiz('Kelvin: Nullpunkt am|absoluten Nullpunkt', y=280, ein=1.0, farbe='gruen'),
           formel(r'0\;\text{K} = -273.15\,^\circ\text{C}', y=440, g=44, a='Null Kelvin sind'),
           formel(r'273.15\;\text{K} = 0\,^\circ\text{C}', y=540, g=44, a='null Grad Celsius sind'),
           notiz('keine negativen Kelvin', y=650, a='Negative Kelvin', farbe='gold'),
           doppelstrahl(-320, 140, [-200, -100, 0, 100], [0, 100, 200, 300, 400], a='Lord Kelvin',
                        extra={'strecken': [S((-273.15, 2.0), (-273.15, 7.6), KEL, 3, gestrichelt=True, ein=0.6),
                                            S((0, 2.0), (0, 7.6), CEL, 3, gestrichelt=True, ein=0.6)],
                               'texte': [T(-268, 8.3, 'absoluter Nullpunkt', KEL, 24, 'start', ein=0.6)]})),
        sz('Anwendungen', 'Im Alltag rechnet man in Grad Celsius: Wetter, Fieber, Kochen. In Wissenschaft und Technik in Kelvin, etwa bei sehr tiefen Temperaturen: Flüssiger Stickstoff siedet bei siebenundsiebzig Kelvin. Und wo Temperaturen ein Verhältnis bilden: Die mittlere Bewegungsenergie der Teilchen ist proportional zur Kelvin-Temperatur. Von hundertfünfzig auf dreihundert Kelvin verdoppelt sie sich. Das Tempo der Teilchen wächst dabei nur um rund einundvierzig Prozent.',
           notiz('Celsius: Wetter, Fieber, Kochen', y=280, ein=1.0),
           notiz('Kelvin: Forschung, Technik,|tiefe Temperaturen', y=380, a='In Wissenschaft', farbe='gruen'),
           notiz('flüssiger Stickstoff: 77 K', y=510, a='Flüssiger Stickstoff siedet', farbe='gruen', g=38),
           formel(r'150\;\text{K} \to 300\;\text{K}: \;\text{doppelte Bewegungsenergie}', y=600, g=36, a='Von hundertfünfzig'),
           notiz('Tempo: nur rund 41 % mehr', y=690, a='Das Tempo der Teilchen', g=38),
           graf([-0.5, 10], [-40, 380], [], [100, 200, 300], '', 'T [K]', a='Von hundertfünfzig',
                flaechen=[F(rechteck(2, 0, 4, 150), KEL, 0.45), F(rechteck(6, 0, 8, 300), KEL, 0.45)],
                texte=[T(3, 165, '150 K', KEL, 28), T(7, 315, '300 K', KEL, 28),
                       T(3, -25, '−123 °C', CEL, 24), T(7, -25, '27 °C', CEL, 24)]),
           graf([-0.5, 10], [-40, 380], achsen=False, a='verdoppelt sie sich',
                strecken=[S((2, 150), (8.6, 150), TIN, 3, gestrichelt=True), P((8.6, 150), (8.6, 295), ORA, 5)],
                texte=[T(8.8, 225, '× 2', ORA, 30, 'start')])),
        sz('Problem Messreihe', 'Jetzt ein ganzes Problem. Eine Klasse misst mit einem Gasthermometer: bei zehn Grad Celsius tausendfünfunddreissig Hektopascal, bei neunzig Grad tausenddreihundertachtundzwanzig. Wo liegt nach diesen Messwerten der absolute Nullpunkt?',
           notiz('10 °C: 1035 hPa|90 °C: 1328 hPa', y=300, ein=2.0, a='bei zehn Grad'),
           notiz('gesucht: Temperatur bei p = 0', y=480, a='Wo liegt', farbe='gold'),
           gasgraf([(10, 1035), (90, 1328)])),
        sz('Vorgehen Messreihe', 'Zuerst die Steigung: wie viel Druck je Grad dazukommt. Dann rechnet man vom ersten Messpunkt aus so weit zurück, bis der Druck null ist.',
           notiz('1. Steigung: Druck je Grad', y=300, ein=1.0, a='Zuerst die Steigung'),
           notiz('2. vom Messpunkt bis p = 0|zurückrechnen', y=440, a='Dann rechnet man'),
           gasgraf([(10, 1035), (90, 1328)]),
           graf([-320, 130], [-150, 1650], achsen=False, a='Zuerst die Steigung',
                strecken=[S((10, 1035), (90, 1035), ORA, 4), S((90, 1035), (90, 1328), ORA, 4)],
                texte=[T(50, 930, 'Δϑ = 80 °C', ORA, 24), T(84, 1180, 'Δp = 293 hPa', ORA, 24, 'end')])),
        sz('Lösung Messreihe', 'Die Steigung ist zweihundertdreiundneunzig Hektopascal durch achtzig Grad, rund drei Komma sechs sechs Hektopascal pro Grad. Bis zum Druck null fehlen tausendfünfunddreissig Hektopascal, das sind rund zweihundertdreiundachtzig Grad. Zehn minus zweihundertdreiundachtzig: rund minus zweihundertdreiundsiebzig Grad Celsius. Probe: Der genaue Wert ist minus zweihundertdreiundsiebzig Komma eins fünf Grad.',
           formel(r'\frac{\Delta p}{\Delta\vartheta} = \frac{1328\;\text{hPa} - 1035\;\text{hPa}}{90\,^\circ\text{C} - 10\,^\circ\text{C}} \approx 3.66\;\tfrac{\text{hPa}}{^\circ\text{C}}', y=260, g=34, ein=0.4, a='rund drei Komma sechs sechs'),
           formel(r'\frac{1035\;\text{hPa}}{3.66\;\text{hPa}/^\circ\text{C}} \approx 283\,^\circ\text{C}', y=400, g=36, a='das sind rund zweihundertdreiundachtzig'),
           formel(r'\vartheta_0 \approx 10\,^\circ\text{C} - 283\,^\circ\text{C} = -273\,^\circ\text{C}', y=520, g=38, a='rund minus zweihundertdreiundsiebzig'),
           notiz('Probe: −273.15 °C', y=640, a='Probe', farbe='gold'),
           gasgraf([(10, 1035), (90, 1328)], gerade=[S((10, 1035), (90, 1328), DRU, 4)]),
           graf([-320, 130], [-150, 1650], achsen=False, a='Bis zum Druck null',
                strecken=[S((n1, 0), (10, 1035), DRU, 4, gestrichelt=True)]),
           graf([-320, 130], [-150, 1650], achsen=False, a='rund minus zweihundertdreiundsiebzig',
                punkte=[{'x': round(n1, 2), 'y': 0, 'farbe': KEL, 'beschriftung': '≈ −273 °C', 'beschriftung_bei': [-262, 120], 'anker': 'start'}])),
        sz('Merke', 'Zum Mitnehmen: Celsius hängt an zwei Fixpunkten des Wassers. Kelvin beginnt am absoluten Nullpunkt, mit derselben Schrittweite. Im Alltag Celsius, wo Verhältnisse zählen Kelvin.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'0\;\text{K} = -273.15\,^\circ\text{C}', y=420, g=46, ein=0.6),
           notiz('gleiche Schrittweite,|anderer Nullpunkt', y=540, a='Kelvin beginnt'),
           notiz('Verhältnisse nur in Kelvin', y=700, a='Im Alltag Celsius', farbe='gold')),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Messreihe', 'Was ist dein erster Schritt?',
                 ['273.15 abziehen', 'Die Steigung bestimmen: Druckzunahme je Grad', 'Die beiden Drücke zusammenzählen'], 1,
                 {0: 'Den Wert 273.15 sollst du hier gerade finden. Was brauchst du dafür aus den Messwerten?', 2: 'Was sagt eine Summe zweier Drücke über die Gerade?'},
                 sprich='Was ist dein erster Schritt?', kopf='Dein Vorgehen',
                 rueck_sprich={0: 'Den Wert zweihundertdreiundsiebzig Komma eins fünf sollst du hier gerade finden. Was brauchst du dafür aus den Messwerten?'})]))

DREH.append(dict(KOPF, titel='Temperatur sehen: Kontrollfragen zu Celsius und Kelvin', dateiname='p5-1-lp-kontrolle-skalen',
    kurzbeschrieb='Fünf Fragen zu den Temperaturskalen: Celsius\' Nullpunkt, ein selbst gebautes Thermometer, zwei Gasthermometer, eine unmögliche Angabe und die Bewegungsenergie in Kelvin.',
    schlagworte=['Celsius', 'Kelvin', 'absoluter Nullpunkt', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'Schmelzendes Eis lässt sich überall leicht herstellen, und seine Temperatur bleibt fest, solange es schmilzt. Darum taugt es als Fixpunkt. Die Teilchen bewegen sich dort weiter.',
           notiz('überall herstellbar,|Temperatur bleibt fest', y=300, ein=1.0)),
        sz('Frage 2', 'Vom Eiswasser-Strich aus gemessen sind es vier Zentimeter, die hundert Schritte sind zwanzig Zentimeter lang. Vier durch zwanzig mal hundert Grad: zwanzig Grad Celsius.',
           formel(r'\vartheta = \frac{7\;\text{cm} - 3\;\text{cm}}{23\;\text{cm} - 3\;\text{cm}} \cdot 100\,^\circ\text{C} = 20\,^\circ\text{C}', y=320, g=34, ein=1.0)),
        sz('Frage 3', 'Beide Geraden treffen die Temperaturachse bei minus zweihundertdreiundsiebzig Komma eins fünf Grad Celsius. Der absolute Nullpunkt hängt weder vom Gas noch von der Gasmenge ab.',
           notiz('beide bei −273.15 °C', y=300, ein=1.0, farbe='gruen')),
        sz('Frage 4', 'Minus zwanzig Kelvin ist unmöglich: Null Kelvin ist der absolute Nullpunkt, tiefer geht es nicht. Minus zwanzig Grad Celsius gibt es jeden Winter, zwanzig Kelvin im Labor.',
           notiz('unmöglich: −20 K', y=300, ein=1.0)),
        sz('Frage 5', 'Die mittlere Bewegungsenergie ist proportional zur Kelvin-Temperatur. Von hundert auf zweihundert Kelvin verdoppelt sie sich.',
           formel(r'\frac{200\;\text{K}}{100\;\text{K}} = 2', y=320, g=44, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Warum eignet sich schmelzendes Eis als Fixpunkt einer Temperaturskala?',
             ['Dort hört die Teilchenbewegung auf', 'Wasser ist dort am dichtesten', 'Seine Temperatur bleibt fest, und es lässt sich überall herstellen'], 2,
             {0: 'Bewegen sich die Teilchen in schmelzendem Eis noch?', 1: 'Am dichtesten ist Wasser bei rund 4 °C, und darauf kommt es bei einem Fixpunkt nicht an. Was macht einen Fixpunkt brauchbar?'},
             rueck_sprich={1: 'Am dichtesten ist Wasser bei rund vier Grad Celsius, und darauf kommt es bei einem Fixpunkt nicht an. Was macht einen Fixpunkt brauchbar?'}),
        wahl('Frage 2', 'Ein selbst gebautes Thermometer: Im Eiswasser steht der Faden bei 3.0 cm, im siedenden Wasser bei 23.0 cm. Heute steht er bei 7.0 cm. Welche Temperatur zeigt es?',
             ['35 °C', '20 °C', '30.4 °C'], 1,
             {0: 'Beginnt die Skala bei null Zentimetern?', 2: 'Wie lang ist der Abstand zwischen den beiden Fixpunkten?'},
             sprich='Ein selbst gebautes Thermometer: Im Eiswasser steht der Faden bei drei Zentimetern, im siedenden Wasser bei dreiundzwanzig Zentimetern. Heute steht er bei sieben Zentimetern. Welche Temperatur zeigt es?'),
        wahl('Frage 3', 'Zwei Gasthermometer mit festem Volumen: eines mit viel Helium, eines mit wenig Luft. Wo treffen ihre verlängerten Geraden die Temperaturachse?',
             ['Beide bei −273.15 °C', 'Die mit mehr Gas weiter links', 'Beide bei 0 °C'], 0,
             {1: 'Hängt der Nullpunkt der Temperatur von der Gasmenge ab?', 2: 'Hat ein Gas bei null Grad Celsius noch Druck?'}),
        wahl('Frage 4', 'Welche Angabe ist unmöglich?',
             ['−20 °C', '20 K', '−20 K'], 2,
             {0: 'Negative Celsius-Temperaturen gibt es jeden Winter.', 1: 'Zwanzig Kelvin liegen über dem absoluten Nullpunkt.'},
             sprich='Welche Angabe ist unmöglich?'),
        wahl('Frage 5', 'Ein Gas wird von 100 K auf 200 K erwärmt. Was geschieht mit der mittleren Bewegungsenergie seiner Teilchen?',
             ['Sie wächst um 100 K', 'Sie verdoppelt sich', 'Sie bleibt gleich'], 1,
             {0: 'Kelvin ist eine Einheit der Temperatur, nicht der Energie. Was gilt für das Verhältnis?', 2: 'Wärmer heisst …?'},
             sprich='Ein Gas wird von hundert auf zweihundert Kelvin erwärmt. Was geschieht mit der mittleren Bewegungsenergie seiner Teilchen?'),
    ]))

# ================================================================== Kapitel 4: Umrechnen
DS = dict(x0=-320, x1=640, c=[-200, 0, 200, 400, 600], k=[0, 200, 400, 600, 800])


def strahl(ein=0.05, a=None, extra=None):
    return doppelstrahl(DS['x0'], DS['x1'], DS['c'], DS['k'], ein=ein, a=a, extra=extra)


def marke(c, ein=None, a=None, txt_c=None, txt_k=None, farbe=CEL):
    """senkrechte Marke bei c °C durch beide Strahlen mit Beschriftung oben (°C) und unten (K)."""
    g = graf([DS['x0'], DS['x1']], [0, 10], achsen=False, a=a, ein=ein if ein is not None else 0.05,
             strecken=[S((c, 2.2), (c, 7.3), TIN, 3, gestrichelt=True)],
             punkte=[{'x': c, 'y': 6.5, 'farbe': CEL}, {'x': c, 'y': 3.0, 'farbe': KEL}],
             texte=([T(c, 8.0, txt_c, CEL, 28)] if txt_c else []) + ([T(c, 1.3, txt_k, KEL, 28)] if txt_k else []))
    return g


DREH.append(dict(KOPF, titel='Temperatur sehen: von Celsius zu Kelvin und zurück', dateiname='p5-1-lp-umrechnen',
    kurzbeschrieb='Umrechnen zwischen Grad Celsius und Kelvin, Vorsicht beim Minus, warum eine Temperaturdifferenz in beiden Skalen gleich ist und wann man umrechnen muss — mit einem vorgerechneten Problem aus der Kühlkette.',
    schlagworte=['Celsius', 'Kelvin', 'umrechnen', 'Temperaturdifferenz', '273.15'], _probe=EIN % 4,
    szenen=[
        sz('Zwei Skalen', 'Celsius und Kelvin haben gleich grosse Schritte. Nur ihr Nullpunkt liegt verschieden: Die Kelvin-Skala ist um zweihundertdreiundsiebzig Komma eins fünf verschoben.',
           notiz('gleiche Schritte,|anderer Nullpunkt', y=300, ein=1.0),
           formel(r'0\,^\circ\text{C} = 273.15\;\text{K}', y=480, g=44, a='Die Kelvin-Skala'),
           strahl(extra={'strecken': [S((0, 2.2), (0, 7.3), TIN, 3, gestrichelt=True, ein=0.05)]})),
        sz('Umrechnen', 'Darum zählt man zum Celsius-Wert zweihundertdreiundsiebzig Komma eins fünf dazu. Kaffee mit zweiundachtzig Grad Celsius hat dreihundertfünfundfünfzig Komma eins fünf Kelvin.',
           formel(r'T\,[\text{K}] = \vartheta\,[^\circ\text{C}] + 273.15', y=280, g=44, ein=0.6),
           formel(r'T\,[\text{K}] = 82 + 273.15 = 355.15', y=420, g=42, a='Kaffee'),
           strahl(), marke(82, a='Kaffee', txt_c='82 °C', txt_k='355.15 K')),
        sz('Zurück', 'Zurück zieht man ab: Ein Ofen mit fünfhundert Kelvin hat zweihundertsechsundzwanzig Komma acht fünf Grad Celsius.',
           formel(r'\vartheta\,[^\circ\text{C}] = T\,[\text{K}] - 273.15', y=280, g=44, ein=0.6),
           formel(r'\vartheta\,[^\circ\text{C}] = 500 - 273.15 = 226.85', y=420, g=40, a='Ein Ofen'),
           strahl(), marke(226.85, a='Ein Ofen', txt_c='226.85 °C', txt_k='500 K')),
        sz('Minus', 'Vorsicht mit dem Minus: Minus zwölf Grad Celsius sind minus zwölf plus zweihundertdreiundsiebzig Komma eins fünf, also zweihunderteinundsechzig Komma eins fünf Kelvin, nicht zweihundertfünfundachtzig Komma eins fünf.',
           formel(r'T\,[\text{K}] = -12 + 273.15 = 261.15', y=300, g=42, ein=0.6, a='also zweihunderteinundsechzig'),
           notiz('nicht 273.15 + 12 = 285.15', y=440, a='nicht zweihundertfünfundachtzig', farbe='rot'),
           strahl(), marke(-12, a='also zweihunderteinundsechzig', txt_c='−12 °C', txt_k='261.15 K')),
        sz('Differenz', 'Bei einer Temperaturdifferenz fällt die Verschiebung weg. Wasser wird von fünfzehn auf fünfundsechzig Grad Celsius erwärmt: Die Temperatur steigt um fünfzig Grad. In Kelvin: dreihundertachtunddreissig Komma eins fünf minus zweihundertachtundachtzig Komma eins fünf, ebenfalls fünfzig Kelvin.',
           formel(r'\Delta\vartheta = 65\,^\circ\text{C} - 15\,^\circ\text{C} = 50\,^\circ\text{C}', y=300, g=40, a='steigt um fünfzig'),
           formel(r'\Delta T = 338.15\;\text{K} - 288.15\;\text{K} = 50\;\text{K}', y=420, g=38, a='ebenfalls fünfzig'),
           notiz('gleiche Zahl in beiden Skalen', y=560, a='ebenfalls fünfzig', farbe='gold'),
           doppelstrahl(-20, 100, [0, 20, 40, 60, 80], [280, 300, 320, 340, 360]),
           graf([-20, 100], [0, 10], achsen=False, a='Wasser wird',
                strecken=[S((15, 5.6), (15, 7.4), TIN, 3), S((65, 5.6), (65, 7.4), TIN, 3)]),
           graf([-20, 100], [0, 10], achsen=False, a='steigt um fünfzig',
                strecken=[P((15, 8.2), (65, 8.2), ORA, 5)],
                texte=[T(40, 8.8, 'Δϑ = 50 °C', ORA, 28)]),
           graf([-20, 100], [0, 10], achsen=False, a='In Kelvin',
                strecken=[S((15, 2.1), (15, 3.9), TIN, 3), S((65, 2.1), (65, 3.9), TIN, 3)]),
           graf([-20, 100], [0, 10], achsen=False, a='ebenfalls fünfzig',
                strecken=[P((15, 1.2), (65, 1.2), ORA, 5)],
                texte=[T(40, 0.2, 'ΔT = 50 K', ORA, 28)])),
        sz('Wann', 'Umrechnen muss man, wo eine Temperatur selbst als Faktor oder in einem Verhältnis steht, etwa bei der mittleren Bewegungsenergie. Bei einer Differenz muss man nicht umrechnen.',
           notiz('Faktor oder Verhältnis:|in Kelvin rechnen', y=300, ein=1.0, farbe='gruen'),
           notiz('Differenz: egal, gleiche Zahl', y=500, a='Bei einer Differenz')),
        sz('Problem Impfstoff', 'Jetzt ein ganzes Problem. Ein Impfstoff muss zwischen zwei und acht Grad Celsius lagern. Der Datenlogger im Kühlwagen zeigt zweihundertneunundsiebzig Komma sechs Kelvin. Ist der Impfstoff im erlaubten Bereich? Und wie viel Spielraum bleibt nach oben?',
           notiz('erlaubt: 2 °C bis 8 °C|Logger: 279.6 K', y=300, ein=2.0, a='Ein Impfstoff'),
           notiz('gesucht: im Bereich?|Spielraum bis 8 °C', y=480, a='Ist der Impfstoff', farbe='gold'),
           doppelstrahl(-1, 11, [0, 2, 4, 6, 8, 10], [274, 276, 278, 280, 282, 284],
                        extra={'flaechen': [F(rechteck(2, 6.0, 8, 7.1), CEL, 0.22)], 'texte': [T(5, 8.1, 'erlaubt', CEL, 26)]}),
           graf([-1, 11], [0, 10], achsen=False, a='Der Datenlogger',
                punkte=[{'x': round(279.6 - 273.15, 2), 'y': 3.0, 'farbe': KEL}], texte=[T(279.6 - 273.15, 1.3, '279.6 K', KEL, 28)])),
        sz('Vorgehen Impfstoff', 'Celsius-Zahlen sind um zweihundertdreiundsiebzig Komma eins fünf kleiner. Man zieht also ab und vergleicht dann mit dem erlaubten Bereich.',
           notiz('Celsius-Zahl = Kelvin-Zahl − 273.15', y=300, ein=1.0, a='Celsius-Zahlen'),
           doppelstrahl(-1, 11, [0, 2, 4, 6, 8, 10], [274, 276, 278, 280, 282, 284],
                        extra={'flaechen': [F(rechteck(2, 6.0, 8, 7.1), CEL, 0.22)], 'texte': [T(5, 8.1, 'erlaubt', CEL, 26)]}),
           graf([-1, 11], [0, 10], achsen=False,
                punkte=[{'x': round(279.6 - 273.15, 2), 'y': 3.0, 'farbe': KEL}], texte=[T(279.6 - 273.15, 1.3, '279.6 K', KEL, 28)])),
        sz('Lösung Impfstoff', 'Zweihundertneunundsiebzig Komma sechs minus zweihundertdreiundsiebzig Komma eins fünf ergibt sechs Komma vier fünf Grad Celsius: im Bereich von zwei bis acht Grad. Bis acht Grad bleiben eins Komma fünf fünf Grad, also eins Komma fünf fünf Kelvin, denn eine Differenz ist in beiden Skalen gleich. Probe: Acht Grad Celsius sind zweihunderteinundachtzig Komma eins fünf Kelvin, eins Komma fünf fünf Kelvin mehr als die Anzeige.',
           formel(r'\vartheta\,[^\circ\text{C}] = 279.6 - 273.15 = 6.45', y=280, g=40, ein=0.4, a='ergibt sechs Komma vier fünf'),
           formel(r'\Delta\vartheta = 8\,^\circ\text{C} - 6.45\,^\circ\text{C} = 1.55\,^\circ\text{C}', y=390, g=38, a='bleiben eins Komma fünf fünf Grad'),
           formel(r'\Delta T = 1.55\;\text{K}', y=490, g=40, a='also eins Komma fünf fünf Kelvin'),
           notiz('Probe: 281.15 K − 279.6 K = 1.55 K', y=600, a='Probe', farbe='gold', g=40),
           doppelstrahl(-1, 11, [0, 2, 4, 6, 8, 10], [274, 276, 278, 280, 282, 284],
                        extra={'flaechen': [F(rechteck(2, 6.0, 8, 7.1), CEL, 0.22)], 'texte': [T(5, 8.1, 'erlaubt', CEL, 26)]}),
           graf([-1, 11], [0, 10], achsen=False,
                punkte=[{'x': round(279.6 - 273.15, 2), 'y': 3.0, 'farbe': KEL}], texte=[T(279.6 - 273.15, 1.3, '279.6 K', KEL, 28)]),
           graf([-1, 11], [0, 10], achsen=False, a='ergibt sechs Komma vier fünf',
                strecken=[S((6.45, 2.4), (6.45, 7.2), TIN, 3, gestrichelt=True)], punkte=[{'x': 6.45, 'y': 6.5, 'farbe': CEL}],
                texte=[T(6.45, 9.2, '6.45 °C', CEL, 28)]),
           graf([-1, 11], [0, 10], achsen=False, a='bleiben eins Komma fünf fünf Grad',
                strecken=[P((6.45, 4.6), (8, 4.6), ORA, 5)], texte=[T(7.2, 4.0, '1.55 K', ORA, 26)])),
        sz('Merke', 'Zum Mitnehmen: Kelvin gleich Celsius plus zweihundertdreiundsiebzig Komma eins fünf, Celsius gleich Kelvin minus zweihundertdreiundsiebzig Komma eins fünf. Eine Differenz ist in beiden Skalen gleich.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'T\,[\text{K}] = \vartheta\,[^\circ\text{C}] + 273.15', y=420, g=44, ein=0.6),
           formel(r'\Delta T = \Delta\vartheta', y=560, g=46, a='Eine Differenz')),
        JETZT,
    ],
    fragen=[wahl('Vorgehen Impfstoff', 'Wie rechnest du die Anzeige in Grad Celsius um?',
                 ['ϑ = 279.6 + 273.15', 'ϑ = 279.6 − 273.15', 'ϑ = 273.15 − 279.6'], 1,
                 {0: 'Ist die Celsius-Zahl einer Temperatur grösser oder kleiner als ihre Kelvin-Zahl?', 2: 'Liegt die Anzeige über oder unter 273.15 K? Welches Vorzeichen erwartest du dann?'},
                 sprich='Wie rechnest du die Anzeige in Grad Celsius um?', kopf='Dein Vorgehen',
                 rueck_sprich={2: 'Liegt die Anzeige über oder unter zweihundertdreiundsiebzig Komma eins fünf Kelvin? Welches Vorzeichen erwartest du dann?'})]))

DREH.append(dict(KOPF, titel='Temperatur sehen: Kontrollfragen zum Umrechnen', dateiname='p5-1-lp-kontrolle-umrechnen',
    kurzbeschrieb='Fünf Fragen zum Umrechnen: eine Winternacht, ein Supraleiter, eine abkühlende Suppe, wann man umrechnen muss, und ein Faktor in Kelvin.',
    schlagworte=['Celsius', 'Kelvin', 'umrechnen', 'Temperaturdifferenz', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Minus fünfundzwanzig plus zweihundertdreiundsiebzig Komma eins fünf: zweihundertachtundvierzig Komma eins fünf Kelvin.',
           formel(r'T\,[\text{K}] = -25 + 273.15 = 248.15', y=320, g=42, ein=1.0)),
        sz('Frage 2', 'Dreiundneunzig minus zweihundertdreiundsiebzig Komma eins fünf: minus hundertachtzig Komma eins fünf Grad Celsius.',
           formel(r'\vartheta\,[^\circ\text{C}] = 93 - 273.15 = -180.15', y=320, g=40, ein=1.0)),
        sz('Frage 3', 'Ende minus Anfang: fünfundvierzig minus fünfundachtzig Grad, also minus vierzig Kelvin. Abkühlen gibt ein negatives Delta T; die zweihundertdreiundsiebzig Komma eins fünf fällt weg.',
           formel(r'\Delta\vartheta = 45\,^\circ\text{C} - 85\,^\circ\text{C} = -40\,^\circ\text{C}', y=300, g=40, ein=1.0),
           formel(r'\Delta T = -40\;\text{K}', y=420, g=40, ein=1.0)),
        sz('Frage 4', 'Beim Faktor muss man in Kelvin rechnen, weil der Nullpunkt der Celsius-Skala willkürlich ist. Bei der Temperaturänderung ist es egal: In beiden Skalen sind es zwanzig.',
           formel(r'\frac{313.15\;\text{K}}{293.15\;\text{K}} \approx 1.07', y=300, g=42, ein=1.0),
           notiz('nicht 40 / 20 = 2', y=440, ein=1.0, farbe='rot')),
        sz('Frage 5', 'In Kelvin: zweihundert Komma eins fünf und vierhundert Komma eins fünf. Vierhundert Komma eins fünf durch zweihundert Komma eins fünf ergibt rund zwei.',
           formel(r'\frac{400.15\;\text{K}}{200.15\;\text{K}} \approx 2.00', y=320, g=42, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'In einer Winternacht sind es −25 °C. Wie viel Kelvin sind das?',
             ['298.15 K', '248.15 K', '−298.15 K'], 1,
             {0: 'Liegt −25 °C über oder unter 0 °C? Wird die Kelvin-Zahl dann grösser oder kleiner als 273.15?', 2: 'Kann eine Kelvin-Temperatur negativ sein?'},
             rueck_sprich={0: 'Liegt minus fünfundzwanzig Grad über oder unter null Grad? Wird die Kelvin-Zahl dann grösser oder kleiner als zweihundertdreiundsiebzig Komma eins fünf?'},
             sprich='In einer Winternacht sind es minus fünfundzwanzig Grad Celsius. Wie viel Kelvin sind das?'),
        wahl('Frage 2', 'Ein Supraleiter leitet unter 93 K ohne Widerstand. Wie viel Grad Celsius sind 93 K?',
             ['−180.15 °C', '366.15 °C', '180.15 °C'], 0,
             {1: 'Celsius-Zahlen sind kleiner als Kelvin-Zahlen: abziehen, nicht dazuzählen.', 2: 'Dreiundneunzig Kelvin liegen unter 273.15 Kelvin. Welches Vorzeichen hat dann die Celsius-Temperatur?'},
             rueck_sprich={2: 'Dreiundneunzig Kelvin liegen unter zweihundertdreiundsiebzig Komma eins fünf Kelvin. Welches Vorzeichen hat dann die Celsius-Temperatur?'},
             sprich='Ein Supraleiter leitet unter dreiundneunzig Kelvin ohne Widerstand. Wie viel Grad Celsius sind dreiundneunzig Kelvin?'),
        wahl('Frage 3', 'Eine Suppe kühlt von 85 °C auf 45 °C ab. Wie gross ist die Temperaturänderung ΔT?',
             ['+40 K', '−313.15 K', '−40 K'], 2,
             {0: 'Ende minus Anfang: Wird die Suppe wärmer oder kälter?', 1: 'Bei einer Differenz fällt die Verschiebung um 273.15 weg.'},
             rueck_sprich={1: 'Bei einer Differenz fällt die Verschiebung um zweihundertdreiundsiebzig Komma eins fünf weg.'},
             sprich='Eine Suppe kühlt von fünfundachtzig auf fünfundvierzig Grad Celsius ab. Wie gross ist die Temperaturänderung?'),
        wahl('Frage 4', 'In welcher Rechnung musst du die Temperaturen in Kelvin umrechnen?',
             ['Temperaturänderung von 20 °C auf 40 °C', 'Faktor der mittleren Bewegungsenergie von 20 °C auf 40 °C', 'In beiden'], 1,
             {0: 'Bei einer Differenz fällt die Verschiebung weg. Wo spielt sie eine Rolle?', 2: 'Ist eine Differenz in Grad Celsius und Kelvin nicht dieselbe Zahl?'},
             sprich='In welcher Rechnung musst du die Temperaturen in Kelvin umrechnen?'),
        wahl('Frage 5', 'Ein Gas wird von −73 °C auf 127 °C erwärmt. Um welchen Faktor wächst die mittlere Bewegungsenergie seiner Teilchen?',
             ['−1.74', '0.50', '2.00'], 2,
             {0: 'Ein Verhältnis braucht die Temperaturen in Kelvin.', 1: 'Neu durch alt: Wird das Gas wärmer oder kälter?'},
             sprich='Ein Gas wird von minus dreiundsiebzig auf hundertsiebenundzwanzig Grad Celsius erwärmt. Um welchen Faktor wächst die mittlere Bewegungsenergie seiner Teilchen?'),
    ]))

# ------------------------------------------------------------------ schreiben
def schreiben():
    for d in DREH:
        pfad = os.path.join(CLIPS, d['dateiname'] + '.json')
        if NUR and d['dateiname'] not in NUR:
            continue
        if os.path.exists(pfad) and not NEU:
            print('vorhanden', d['dateiname'])
            continue
        with open(pfad, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print('geschrieben', d['dateiname'], len(d['szenen']), 'Szenen')


if __name__ == '__main__':     # antworten.py importiert die Bausteine, ohne zu schreiben
    schreiben()
