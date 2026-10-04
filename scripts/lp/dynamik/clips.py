"""Erzeugt die zehn Drehbücher des Leitprogramms Dynamik (clips/p4-2-lp-*.json).

  python3 scripts/lp/dynamik/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/dynamik/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/dynamik/clips.py --neu p4-2-lp-kontrolle-faden …   # nur diese

Archiv-Werkzeug wie scripts/lp/kinematik/clips.py: Nach der Vertonung sind die JSONs in clips/
die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf mit
--neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).

Farben wie in den Simulationen, soweit das Clip-Theme sie kennt: \\fc v (Grün), \\fa F_G
(Bernstein), \\fd F_W und F_z (Rot). Blau (Antrieb, Faden-, Normalkraft) und Violett (a) kennt
das Theme nicht — diese Grössen bleiben ungefärbt. Bilder: Aufnahmen der Simulationen
(clips/bilder/p4-2-lp-*.jpg). Zahlen im Sprechertext ausgeschrieben (CLAUDE.md). Kontrollclips:
neue Beispiele, richtige Antwort an wechselnden Stellen, Lösung erst nach der Antwort.
"""
import json
import os
import sys

SP = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(os.path.join(SP, '..', '..', '..', 'clips'))
NEU = '--neu' in sys.argv

KOPF = {
    'themenbereich': 'Mechanik · BM', 'lerngebiet': '4 · Mechanik',
    'lektion': ['p4-2'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-04', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Kraft sehen', 'nachlauf': 2.6, 'probe': True,
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
EIN = 'Einführungsclip des Leitprogramms Dynamik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Dynamik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'

# ================================================================== Kapitel 1
DREH.append(dict(KOPF, titel='Kraft sehen: doppelte Kraft, doppelte Beschleunigung', dateiname='p4-2-lp-grundgesetz',
    kurzbeschrieb='Kraft als Ursache einer Bewegungsänderung; ein Wagen mit doppelter Kraft und mit doppelter Masse, und daraus das Grundgesetz F = m · a.',
    schlagworte=['Kraft', 'Masse', 'Beschleunigung', 'Grundgesetz', 'Newton', 'Trägheit'], _probe=EIN % 1,
    szenen=[
        sz('Kraft', 'Eine Kraft sieht man nicht, man erkennt sie an ihrer Wirkung: Sie verformt einen Körper, oder sie ändert seine Bewegung. Er wird schneller, langsamer, oder er ändert die Richtung. Gemessen wird die Kraft in Newton.',
           titel('Was ist eine Kraft?', g=76),
           notiz('Wirkung:|verformen oder|Bewegung ändern', y=440, ein=3.0)),
        sz('Versuch', 'Auf einer reibungsfreien Bahn zieht eine Kraft von vier Newton einen Wagen von zwei Kilogramm. Im v-t-Diagramm entsteht eine Gerade: Der Wagen wird jede Sekunde um zwei Meter pro Sekunde schneller. Seine Beschleunigung ist zwei Meter pro Sekunde im Quadrat.',
           formel(r'a = \dfrac{F}{m} = \dfrac{4\;\text{N}}{2\;\text{kg}} = 2\;\text{m/s}^2', g=50, ein=9.0),
           notiz('jede Sekunde|2 m/s schneller', ein=6.0),
           bild('p4-2-lp-grundgesetz-1.jpg')),
        sz('Doppelte Kraft', 'Jetzt zieht die doppelte Kraft, acht Newton, am selben Wagen. Die Gerade wird doppelt so steil wie beim vorigen Lauf, grau gestrichelt: vier Meter pro Sekunde im Quadrat. Doppelte Kraft, doppelte Beschleunigung.',
           formel(r'a = \dfrac{8\;\text{N}}{2\;\text{kg}} = 4\;\text{m/s}^2', g=54, ein=4.0),
           notiz('doppelte Kraft:|doppelte Beschleunigung', ein=9.0),
           bild('p4-2-lp-grundgesetz-2.jpg')),
        sz('Doppelte Masse', 'Und mit vier Newton an einem Wagen von vier Kilogramm? Die Gerade ist nur halb so steil wie mit zwei Kilogramm: ein Meter pro Sekunde im Quadrat. Die grössere Masse ist träger, sie lässt sich schwerer beschleunigen.',
           formel(r'a = \dfrac{4\;\text{N}}{4\;\text{kg}} = 1\;\text{m/s}^2', g=54, ein=4.0),
           notiz('doppelte Masse:|halbe Beschleunigung', ein=8.0),
           bild('p4-2-lp-grundgesetz-3.jpg')),
        sz('Grundgesetz', 'Beides zusammen ergibt das Grundgesetz der Mechanik: Kraft gleich Masse mal Beschleunigung. Kraft und Beschleunigung zeigen in dieselbe Richtung. Ein Newton ist die Kraft, die ein Kilogramm mit einem Meter pro Sekunde im Quadrat beschleunigt.',
           titel('Das Grundgesetz', y=260, g=76),
           formel(r'F = m \cdot a', y=420, g=64, ein=2.0),
           formel(r'1\;\text{N} = 1\;\text{kg} \cdot \text{m/s}^2', y=560, g=50, ein=10.0)),
        sz('Merke', 'Zum Mitnehmen: Eine Kraft ändert die Geschwindigkeit, sie bestimmt nicht die Geschwindigkeit selbst. Die Beschleunigung ist Kraft durch Masse. Im v-t-Diagramm ist sie die Steigung.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'a = \dfrac{F}{m}', y=420, ein=0.4),
           notiz('doppelte Kraft: doppeltes a|doppelte Masse: halbes a|Steigung im v-t-Diagramm: a', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 2
DREH.append(dict(KOPF, titel='Kraft sehen: Antrieb gegen Widerstand', dateiname='p4-2-lp-gesamtkraft',
    kurzbeschrieb='Antrieb und Widerstand an einem Velo: die Gesamtkraft als Summe mit Vorzeichen, konstantes Tempo ohne Gesamtkraft (Trägheitsgesetz) und Ausrollen.',
    schlagworte=['Gesamtkraft', 'Trägheitsgesetz', 'Widerstand', 'Antriebskraft', 'Grundgesetz'], _probe=EIN % 2,
    szenen=[
        sz('Zwei Kräfte', 'Auf ein Velo mit Fahrerin, zusammen achtzig Kilogramm, wirken zwei Kräfte: der Antrieb von sechzig Newton nach vorn und der Widerstand von zwanzig Newton nach hinten. Für die Bewegung zählt nur ihre Summe mit Vorzeichen, die Gesamtkraft: vierzig Newton.',
           formel(r'F_\text{ges} = F_A - \fd{F_W} = 60\;\text{N} - \fd{20\;\text{N}} = 40\;\text{N}', g=44, ein=12.0),
           notiz('nach vorn: +|nach hinten: −', ein=6.0),
           bild('p4-2-lp-gesamtkraft-1.jpg')),
        sz('Beschleunigung', 'Die Gesamtkraft beschleunigt die achtzig Kilogramm: vierzig Newton durch achtzig Kilogramm, null Komma fünf Meter pro Sekunde im Quadrat. Nach acht Sekunden fährt das Velo vier Meter pro Sekunde.',
           formel(r'a = \dfrac{F_\text{ges}}{m} = \dfrac{40\;\text{N}}{80\;\text{kg}} = 0.5\;\text{m/s}^2', g=46, ein=1.0),
           bild('p4-2-lp-gesamtkraft-2.jpg')),
        sz('Gleich gross', 'Sind Antrieb und Widerstand gleich gross, hier je dreissig Newton, ist die Gesamtkraft null. Das Velo fuhr schon mit fünf Metern pro Sekunde, und dabei bleibt es: Die v-t-Linie ist waagrecht.',
           formel(r'F_\text{ges} = 30\;\text{N} - \fd{30\;\text{N}} = 0', g=50, ein=4.0),
           notiz('keine Gesamtkraft:|Tempo bleibt', ein=8.0),
           bild('p4-2-lp-gesamtkraft-3.jpg')),
        sz('Trägheitsgesetz', 'Das ist das Trägheitsgesetz: Wirkt keine Gesamtkraft, behält ein Körper seinen Bewegungszustand. Er bleibt in Ruhe, oder er fährt geradeaus mit gleichem Tempo weiter. Eine Kraft braucht es nur, um die Bewegung zu ändern.',
           titel('Das Trägheitsgesetz', y=260, g=76),
           notiz('keine Gesamtkraft:|in Ruhe bleiben oder|gleichförmig weiterfahren', y=440, ein=4.0)),
        sz('Ausrollen', 'Hört die Fahrerin auf zu treten, bleibt nur der Widerstand, hier vierzig Newton nach hinten. Die Gesamtkraft ist negativ, minus vierzig Newton, die Beschleunigung minus null Komma fünf Meter pro Sekunde im Quadrat. Das Velo wird langsamer.',
           formel(r'a = \dfrac{-\fd{40\;\text{N}}}{80\;\text{kg}} = -0.5\;\text{m/s}^2', g=50, ein=8.0),
           notiz('Gesamtkraft gegen|die Fahrtrichtung:|langsamer', ein=12.0),
           bild('p4-2-lp-gesamtkraft-4.jpg')),
        sz('Merke', 'Zum Mitnehmen: Kräfte auf einer Geraden werden mit Vorzeichen addiert. Die Gesamtkraft bestimmt die Beschleunigung. Ist sie null, bleibt das Tempo gleich.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_\text{ges} = F_A - \fd{F_W} = m \cdot a', y=420, g=50, ein=0.4),
           notiz('Gesamtkraft null: Tempo bleibt|Gesamtkraft nach hinten: langsamer', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 3
DREH.append(dict(KOPF, titel='Kraft sehen: was die Waage im Aufzug zeigt', dateiname='p4-2-lp-aufzug',
    kurzbeschrieb='Gewichtskraft und freier Fall mit dem Grundgesetz, dann die Normalkraft auf einer Waage im Aufzug: in Ruhe, beim Anfahren, beim Bremsen und im freien Fall.',
    schlagworte=['Gewichtskraft', 'Normalkraft', 'Aufzug', 'freier Fall', 'Waage', 'Grundgesetz'], _probe=EIN % 3,
    szenen=[
        sz('Gewichtskraft', 'Die Erde zieht jeden Körper an, mit der Gewichtskraft: Masse mal g, neun Komma acht eins Meter pro Sekunde im Quadrat. Ein Körper von zwei Kilogramm erfährt neunzehn Komma sechs Newton.',
           titel('Die Gewichtskraft', y=260, g=76),
           formel(r'\fa{F_G} = m \cdot g = 2\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx \fa{19.6\;\text{N}}', y=440, g=46, ein=4.0)),
        sz('Fall', 'Fällt ein Körper frei, wirkt nur die Gewichtskraft. Bei doppelter Masse ist sie doppelt so gross, muss aber auch die doppelte Masse beschleunigen. Die Masse kürzt sich: Alle Körper fallen mit g.',
           formel(r'a = \dfrac{\fa{F_G}}{m} = \dfrac{m \cdot g}{m} = g', g=56, ein=6.0),
           notiz('gilt für alle Körper|(ohne Luftwiderstand)', ein=9.0)),
        sz('Waage', 'Eine Person von sechzig Kilogramm steht im ruhenden Aufzug auf einer Waage. Die Waage drückt mit der Normalkraft zurück. In Ruhe ist sie gleich gross wie die Gewichtskraft, rund fünfhundertneunundachtzig Newton. Die Waage rechnet das in sechzig Kilogramm um.',
           formel(r'F_N = \fa{F_G} = 60\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx 589\;\text{N}', g=44, ein=7.0),
           notiz('Die Waage misst|die Normalkraft', ein=13.0),
           bild('p4-2-lp-aufzug-1.jpg', breite=700)),
        sz('Anfahren', 'Fährt der Aufzug mit zwei Metern pro Sekunde im Quadrat nach oben an, muss die Person mitbeschleunigt werden. Normalkraft minus Gewichtskraft ist Masse mal Beschleunigung. Die Normalkraft wird rund siebenhundertneun Newton, die Waage zeigt zweiundsiebzig Kilogramm.',
           formel(r'F_N - \fa{F_G} = m \cdot a', g=50, ein=5.0),
           formel(r'F_N = m \cdot (g + a) = 60\;\text{kg} \cdot 11.81\;\text{m/s}^2 \approx 709\;\text{N}', y=420, g=40, ein=10.0),
           bild('p4-2-lp-aufzug-2.jpg', breite=700)),
        sz('Bremsen', 'Bremst der Aufzug die Fahrt nach oben mit zwei Metern pro Sekunde im Quadrat, zeigt die Beschleunigung nach unten, a ist negativ. Die Normalkraft ist kleiner als die Gewichtskraft, rund vierhundertneunundsechzig Newton. Die Waage zeigt siebenundvierzig Komma acht Kilogramm.',
           formel(r'F_N = 60\;\text{kg} \cdot (9.81 - 2)\;\text{m/s}^2 \approx 469\;\text{N}', g=44, ein=8.0),
           notiz('a nach unten:|Waage zeigt weniger', ein=4.0),
           bild('p4-2-lp-aufzug-3.jpg', breite=700)),
        sz('Seil reisst', 'Und wenn das Seil reisst? Kabine und Person fallen beide mit g. Die Waage muss nicht mehr drücken, die Normalkraft ist null. Die Waage zeigt null, obwohl die Gewichtskraft weiter wirkt.',
           formel(r'F_N = m \cdot (g - g) = 0', g=54, ein=5.0),
           notiz('freier Fall:|schwerelos', ein=8.0),
           bild('p4-2-lp-aufzug-4.jpg', breite=700)),
        sz('Merke', 'Zum Mitnehmen: Die Gewichtskraft ist m mal g. Eine Waage misst die Normalkraft. Beschleunigt der Aufzug nach oben, zeigt sie mehr, nach unten weniger, im freien Fall null.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_N - \fa{F_G} = m \cdot a \qquad \fa{F_G} = m \cdot g', y=420, g=46, ein=0.4),
           notiz('a nach oben: mehr|a nach unten: weniger|freier Fall: null', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 4
DREH.append(dict(KOPF, titel='Kraft sehen: wer zieht wen am Faden', dateiname='p4-2-lp-faden',
    kurzbeschrieb='Ein Wagen auf dem Tisch, über eine Rolle von einem hängenden Körper gezogen: Beschleunigung des Systems und Fadenkraft am Wagen allein.',
    schlagworte=['Fadenkraft', 'System', 'Rolle', 'Gewichtskraft', 'Grundgesetz'], _probe=EIN % 4,
    szenen=[
        sz('Aufbau', 'Ein Wagen von drei Kilogramm steht auf einem reibungsfreien Tisch. Über eine Rolle zieht ihn ein Körper von einem Kilogramm, der am Faden hängt. Faden und Rolle denken wir uns masselos.',
           notiz('m₁ = 3 kg auf dem Tisch|m₂ = 1 kg am Faden', y=320, ein=1.0, g=50),
           bild('p4-2-lp-faden-1.jpg', y=180)),
        sz('System', 'Was treibt an? Nur die Gewichtskraft des hängenden Körpers, neun Komma acht eins Newton. Sie muss aber beide Körper beschleunigen, zusammen vier Kilogramm. Die Beschleunigung ist zwei Komma vier fünf Meter pro Sekunde im Quadrat.',
           formel(r'a = \dfrac{m_2 \cdot g}{m_1 + m_2} = \dfrac{1\;\text{kg} \cdot 9.81\;\text{m/s}^2}{4\;\text{kg}} \approx 2.45\;\text{m/s}^2', g=40, ein=9.0),
           notiz('Antrieb: m₂ · g|beschleunigt wird: m₁ + m₂', y=480, ein=3.0),
           bild('p4-2-lp-faden-2.jpg', y=180)),
        sz('Fadenkraft', 'Die Fadenkraft findet man am Wagen allein: Nur der Faden zieht ihn. Drei Kilogramm mal zwei Komma vier fünf, rund sieben Komma drei sechs Newton. Das ist weniger als die Gewichtskraft des hängenden Körpers, sonst würde er gar nicht fallen.',
           formel(r'F_S = m_1 \cdot a = 3\;\text{kg} \cdot 2.45\;\text{m/s}^2 \approx 7.36\;\text{N}', g=44, ein=4.0),
           formel(r'F_S \lt m_2 \cdot g = 9.81\;\text{N}', y=440, g=46, ein=10.0),
           bild('p4-2-lp-faden-2.jpg', y=180)),
        sz('Schwerer', 'Jetzt hängen drei Kilogramm am Faden. Die antreibende Kraft wird dreimal so gross, aber die Gesamtmasse wächst auf sechs Kilogramm. Die Beschleunigung ist die Hälfte von g, rund vier Komma neun Meter pro Sekunde im Quadrat, nur doppelt so viel wie vorher.',
           formel(r'a = \dfrac{3\;\text{kg} \cdot 9.81\;\text{m/s}^2}{6\;\text{kg}} \approx 4.91\;\text{m/s}^2', g=44, ein=6.0),
           notiz('dreifacher Antrieb,|aber auch mehr Masse', ein=10.0),
           bild('p4-2-lp-faden-3.jpg', y=180)),
        sz('Merke', 'Zum Mitnehmen: Für das ganze System beschleunigt die antreibende Kraft die Gesamtmasse. Die Fadenkraft bestimmt man an einem Körper allein.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'm_2 \cdot g = (m_1 + m_2) \cdot a \qquad F_S = m_1 \cdot a', y=420, g=44, ein=0.4),
           notiz('System: Gesamtmasse|Faden: ein Körper allein', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 5
DREH.append(dict(KOPF, titel='Kraft sehen: die Kraft, die im Kreis hält', dateiname='p4-2-lp-kurve',
    kurzbeschrieb='Zentripetalkraft als Gesamtkraft zur Mitte: Kugel an der Schnur, doppeltes Tempo und doppelter Radius, das Auto in der Kurve und die gekappte Schnur.',
    schlagworte=['Zentripetalkraft', 'Kreisbewegung', 'Trägheitsgesetz', 'Haftreibung', 'Grundgesetz'], _probe=EIN % 5,
    szenen=[
        sz('Kreis', 'Eine Kugel von zwei Kilogramm kreist an einer Schnur, mit drei Metern pro Sekunde auf einem Meter Radius. Ihr Tempo bleibt gleich, aber ihre Richtung ändert sich dauernd. Aus der Kinematik kennen wir dafür die Zentripetalbeschleunigung: v Quadrat durch r, neun Meter pro Sekunde im Quadrat.',
           formel(r'\fd{a_z} = \dfrac{\fc{v}^2}{r} = \dfrac{(\fc{3\;\text{m/s}})^2}{1\;\text{m}} = \fd{9\;\text{m/s}^2}', g=46, ein=13.0),
           bild('p4-2-lp-kurve-1.jpg', breite=680)),
        sz('Kraft', 'Nach dem Grundgesetz braucht diese Beschleunigung eine Kraft, die zur Mitte zeigt: die Zentripetalkraft. Masse mal Zentripetalbeschleunigung, zwei mal neun, achtzehn Newton. Hier liefert sie die Schnur.',
           formel(r'\fd{F_z} = m \cdot \fd{a_z} = \dfrac{m \cdot \fc{v}^2}{r}', g=50, ein=3.0),
           formel(r'= 2\;\text{kg} \cdot 9\;\text{m/s}^2 = \fd{18\;\text{N}}', y=430, g=46, ein=7.0),
           bild('p4-2-lp-kurve-1.jpg', breite=680)),
        sz('Doppelt', 'Doppeltes Tempo, sechs Meter pro Sekunde: Die Kraft wird viermal so gross, zweiundsiebzig Newton, denn das Tempo steht im Quadrat. Doppelter Radius bei drei Metern pro Sekunde: halbe Kraft, neun Newton.',
           formel(r'\fc{v} \cdot 2 \;\Rightarrow\; \fd{F_z} \cdot 4', y=280, g=50, ein=1.0),
           formel(r'r \cdot 2 \;\Rightarrow\; \fd{F_z} : 2', y=420, g=50, ein=9.0),
           graf([], [-0.8, 7], [-8, 80], [1, 2, 3, 4, 5, 6], [20, 40, 60, 80], 'v [m/s]', 'F [N]',
                punkte=[{'x': 3, 'y': 18, 'farbe': 4, 'beschriftung': '18 N', 'beschriftung_bei': [3.15, 24]},
                        {'x': 6, 'y': 72, 'farbe': 4, 'beschriftung': '72 N', 'beschriftung_bei': [5.85, 76], 'anker': 'end'},
                        {'x': 3, 'y': 9, 'farbe': 5, 'beschriftung': '9 N bei r = 2 m', 'beschriftung_bei': [3.3, 4]}],
                kurven=[{'formel': '2*x**2', 'farbe': 4, 'von': 0, 'bis': 6.15},
                        {'formel': 'x**2', 'farbe': 5, 'von': 0, 'bis': 6.5}])),
        sz('Kurve', 'Im Auto übernimmt die Haftreibung zwischen Reifen und Strasse diese Rolle. Ein Auto von tausend Kilogramm braucht bei fünfzehn Metern pro Sekunde in einer Kurve mit fünfzig Metern Radius viertausendfünfhundert Newton zur Kurvenmitte.',
           titel('Keine neue Kraft', y=260, g=76),
           formel(r'\fd{F_z} = \dfrac{1000\;\text{kg} \cdot (\fc{15\;\text{m/s}})^2}{50\;\text{m}} = \fd{4500\;\text{N}}', y=430, g=44, ein=8.0),
           notiz('Schnur, Haftreibung, Gravitation:|eine vorhandene Kraft|übernimmt die Rolle', y=600, ein=3.0, g=42)),
        sz('Schnur reisst', 'Reisst die Schnur, fehlt die Kraft zur Mitte. Die Kugel fliegt nicht nach aussen, sondern geradeaus in die Richtung, in die sie sich gerade bewegt hat: tangential. Das ist wieder das Trägheitsgesetz.',
           notiz('ohne Kraft zur Mitte:|geradeaus weiter,|tangential', y=320, ein=7.0, g=50),
           bild('p4-2-lp-kurve-2.jpg', breite=680)),
        sz('Merke', 'Zum Mitnehmen: Auf der Kreisbahn braucht es eine Gesamtkraft zur Mitte, die Zentripetalkraft. Doppeltes Tempo braucht die vierfache Kraft. Fehlt sie, fliegt der Körper tangential weiter.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\fd{F_z} = \dfrac{m \cdot \fc{v}^2}{r}', y=420, ein=0.4),
           notiz('zeigt zur Mitte|doppeltes v: vierfache Kraft|ohne Kraft zur Mitte: tangential', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kontrollclips
DREH.append(dict(KOPF, titel='Kraft sehen: Kontrollfragen zu Kraft, Masse und Beschleunigung', dateiname='p4-2-lp-kontrolle-grundgesetz',
    kurzbeschrieb='Fünf Fragen zu a = F/m, doppelter Kraft, Steigung im v-t-Diagramm, Geschwindigkeit nach einer Zeit und beladenem Lieferwagen.',
    schlagworte=['Grundgesetz', 'Kraft', 'Masse', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Kraft durch Masse: fünfzehn Newton durch fünf Kilogramm, drei Meter pro Sekunde im Quadrat.',
           formel(r'a = \dfrac{F}{m} = \dfrac{15\;\text{N}}{5\;\text{kg}} = 3\;\text{m/s}^2', ein=1.0)),
        sz('Frage 2', 'Die Beschleunigung ist proportional zur Kraft: dreifache Kraft, dreifache Beschleunigung.',
           formel(r'a = \dfrac{3 \cdot F}{m} = 3 \cdot \dfrac{F}{m}', ein=1.0)),
        sz('Frage 3', 'Die Steigung ist die Beschleunigung, Kraft durch Masse. B hat ein Fünftel der Masse, also die fünffache Steigung.',
           formel(r'a_A = \dfrac{F}{5\;\text{kg}} \qquad a_B = \dfrac{F}{1\;\text{kg}}', ein=1.0)),
        sz('Frage 4', 'Zuerst die Beschleunigung: sechs Newton durch drei Kilogramm, zwei Meter pro Sekunde im Quadrat. Nach vier Sekunden: acht Meter pro Sekunde.',
           formel(r'\fc{v} = \dfrac{F}{m} \cdot t = \dfrac{6\;\text{N}}{3\;\text{kg}} \cdot 4\;\text{s} = \fc{8\;\text{m/s}}', g=44, ein=1.0),
           graf([{'bewegung': [[1.0, 0, 0], [3.2, 2, 0]], 'farbe': 3}],
                [-0.7, 6.6], [-3, 27], [1, 2, 3, 4, 5, 6], [5, 10, 15, 20, 25], 't [s]', 'v [m/s]')),
        sz('Frage 5', 'Anderthalbfache Masse bei gleicher Kraft: Die Beschleunigung wird durch eins Komma fünf geteilt, rund eins Komma drei drei Meter pro Sekunde im Quadrat.',
           formel(r'a = \dfrac{F}{1.5 \cdot m} = \dfrac{2\;\text{m/s}^2}{1.5} \approx 1.33\;\text{m/s}^2', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Auf einen Wagen von 5 kg wirkt eine Gesamtkraft von 15 N. Wie gross ist seine Beschleunigung?',
             ['75 m/s²', '3 m/s²', '0.33 m/s²'], 1,
             {0: 'Mal gerechnet? Aus F = m · a folgt: Kraft durch Masse.', 2: 'Umgekehrt geteilt: Kraft durch Masse.'},
             sprich='Auf einen Wagen von fünf Kilogramm wirkt eine Gesamtkraft von fünfzehn Newton. Wie gross ist seine Beschleunigung?',
             rueck_sprich={0: 'Mal gerechnet? Aus F gleich m mal a folgt: Kraft durch Masse.'}),
        wahl('Frage 2', 'Die Kraft auf einen Körper wird verdreifacht, die Masse bleibt. Was geschieht mit der Beschleunigung?',
             ['sie bleibt gleich', 'sie wird dreimal so gross', 'sie wird ein Drittel so gross'], 1,
             {0: 'Dann hätte die Kraft keine Wirkung. Wie hängt a von F ab?', 2: 'Das gilt für dreifache Masse. Hier wächst die Kraft.'}),
        wahl('Frage 3', 'Dieselbe Kraft zieht Wagen A (5 kg) und Wagen B (1 kg). Welcher hat im v-t-Diagramm die steilere Gerade?',
             ['A', 'B', 'beide gleich steil'], 1,
             {0: 'Mehr Masse, mehr Beschleunigung? Die Masse steht im Nenner.', 2: 'Gleiche Kraft heisst nicht gleiche Beschleunigung. Die Masse zählt mit.'},
             sprich='Dieselbe Kraft zieht Wagen A mit fünf Kilogramm und Wagen B mit einem Kilogramm. Welcher hat im v-t-Diagramm die steilere Gerade?'),
        {'szene': 'Frage 4', 'bei': 0.3, 'typ': 'klick',
         'text': 'Eine Gesamtkraft von 6 N beschleunigt einen Körper von 3 kg aus dem Stand. Wie schnell ist er nach 4 s? Tipp den Punkt ins Bild oder gib ihn ein.',
         'sprich': 'Eine Gesamtkraft von sechs Newton beschleunigt einen Körper von drei Kilogramm aus dem Stand. Wie schnell ist er nach vier Sekunden? Tipp den Punkt ins Bild oder gib ihn ein.',
         'ziel': [4, 8], 'toleranz': [0.3, 1.2], 'eingabe': ['t in s', 'v in m/s'], 'richtig_text': 'Getroffen.',
         'fallen': [{'bei': [4, 24], 'text': 'Kraft mal Zeit? Zuerst die Beschleunigung: Kraft durch Masse.'},
                    {'bei': [4, 2], 'text': 'Das ist die Beschleunigung. Wie schnell ist er nach vier Sekunden?'}],
         'falsch_text': 'Nicht ganz. Rechne zuerst a = F / m, dann v = a · t, und such den Wert bei t = 4 s.',
         'falsch_sprich': 'Nicht ganz. Rechne zuerst die Beschleunigung, Kraft durch Masse, dann Beschleunigung mal Zeit, und such den Wert bei vier Sekunden.'},
        wahl('Frage 5', 'Ein leerer Lieferwagen fährt mit 2 m/s² an. Beladen hat er das Anderthalbfache der Masse, die Antriebskraft ist gleich. Wie stark beschleunigt er jetzt?',
             ['3 m/s²', '1.33 m/s²', '0.5 m/s²'], 1,
             {0: 'Mehr Masse macht den Wagen träger, nicht flinker.', 2: 'Abgezogen? Die Masse steht im Nenner: durch den Faktor teilen.'},
             sprich='Ein leerer Lieferwagen fährt mit zwei Metern pro Sekunde im Quadrat an. Beladen hat er das Anderthalbfache der Masse, die Antriebskraft ist gleich. Wie stark beschleunigt er jetzt?'),
    ]))

DREH.append(dict(KOPF, titel='Kraft sehen: Kontrollfragen zu Gesamtkraft und Trägheit', dateiname='p4-2-lp-kontrolle-gesamtkraft',
    kurzbeschrieb='Fünf Fragen zu Gesamtkraft, konstantem Tempo, Trägheitsgesetz, Geschwindigkeit mit Antrieb und Widerstand und zum Ausrollen.',
    schlagworte=['Gesamtkraft', 'Trägheitsgesetz', 'Widerstand', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Die Reibung zeigt gegen den Zug: fünfzig minus zwanzig, dreissig Newton.',
           formel(r'F_\text{ges} = 50\;\text{N} - \fd{20\;\text{N}} = 30\;\text{N}', ein=1.0)),
        sz('Frage 2', 'Konstantes Tempo geradeaus heisst: keine Beschleunigung. Also ist die Gesamtkraft null. Der Antrieb gleicht nur den Widerstand aus.',
           formel(r'a = 0 \;\Rightarrow\; F_\text{ges} = 0', ein=1.0)),
        sz('Frage 3', 'Der Bus wird langsamer, der Körper aber behält nach dem Trägheitsgesetz sein Tempo. Er bewegt sich gegenüber dem Bus nach vorn, bis Gurt oder Haltestange ihn bremsen.',
           notiz('Trägheit:|der Körper behält|sein Tempo', y=320, ein=1.0, g=50)),
        sz('Frage 4', 'Gesamtkraft siebzig minus dreissig, vierzig Newton, durch achtzig Kilogramm: null Komma fünf Meter pro Sekunde im Quadrat. Nach vier Sekunden: drei plus zwei, fünf Meter pro Sekunde.',
           formel(r'a = \dfrac{F_A - \fd{F_W}}{m} = \dfrac{40\;\text{N}}{80\;\text{kg}} = 0.5\;\text{m/s}^2', y=280, g=40, ein=1.0),
           formel(r'\fc{v} = \fc{3\;\text{m/s}} + 0.5\;\text{m/s}^2 \cdot 4\;\text{s} = \fc{5\;\text{m/s}}', y=420, g=40, ein=5.0),
           graf([{'bewegung': [[1.0, 0, 3], [3.2, 0.5, 3]], 'farbe': 3}],
                [-0.9, 8.8], [-1.3, 12.5], [2, 4, 6, 8], [2, 4, 6, 8, 10, 12], 't [s]', 'v [m/s]')),
        sz('Frage 5', 'Beim Ausrollen wirkt nur noch der Widerstand, und der zeigt nach hinten. Darum wird das Velo langsamer.',
           notiz('Gesamtkraft:|gegen die Fahrtrichtung', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Schlitten wird mit 50 N gezogen, die Reibung bremst mit 20 N. Wie gross ist die Gesamtkraft?',
             ['70 N', '30 N', '50 N'], 1,
             {0: 'Die Reibung zieht nicht mit, sie bremst. Welche Richtung hat sie?', 2: 'Das ist nur der Zug. Die Reibung zählt mit.'},
             sprich='Ein Schlitten wird mit fünfzig Newton gezogen, die Reibung bremst mit zwanzig Newton. Wie gross ist die Gesamtkraft?'),
        wahl('Frage 2', 'Ein Auto fährt mit konstant 80 km/h geradeaus. Wie gross ist die Gesamtkraft auf das Auto?',
             ['null', 'so gross wie die Antriebskraft', 'grösser als null, sonst hielte es an'], 0,
             {1: 'Der Fahrwiderstand wirkt auch. Was gibt die Summe beider Kräfte?', 2: 'Wird das Auto schneller? Ohne Beschleunigung …'},
             sprich='Ein Auto fährt mit konstant achtzig Kilometern pro Stunde geradeaus. Wie gross ist die Gesamtkraft auf das Auto?'),
        wahl('Frage 3', 'Ein Bus bremst plötzlich, und die Fahrgäste kippen nach vorn. Warum?',
             ['Eine Kraft stösst sie nach vorn.', 'Die Bremse zieht sie mit nach vorn.', 'Sie behalten ihr Tempo, der Bus wird langsamer.'], 2,
             {0: 'Welcher Körper sollte diese Kraft ausüben? Denk an das Trägheitsgesetz.', 1: 'Die Bremse wirkt auf den Bus, nicht auf die Fahrgäste. Was tun sie ohne Kraft?'}),
        {'szene': 'Frage 4', 'bei': 0.3, 'typ': 'klick',
         'text': 'Ein Velo (80 kg) fährt mit 3 m/s. Antrieb 70 N, Widerstand 30 N. Wie schnell ist es nach 4 s? Tipp den Punkt ins Bild oder gib ihn ein.',
         'sprich': 'Ein Velo mit achtzig Kilogramm fährt mit drei Metern pro Sekunde. Der Antrieb ist siebzig Newton, der Widerstand dreissig Newton. Wie schnell ist es nach vier Sekunden? Tipp den Punkt ins Bild oder gib ihn ein.',
         'ziel': [4, 5], 'toleranz': [0.4, 0.5], 'eingabe': ['t in s', 'v in m/s'], 'richtig_text': 'Getroffen.',
         'fallen': [{'bei': [4, 6.5], 'text': 'Der Widerstand zählt mit: Gesamtkraft = Antrieb − Widerstand.', 'sprich': 'Der Widerstand zählt mit: Gesamtkraft gleich Antrieb minus Widerstand.'},
                    {'bei': [4, 2], 'text': 'Das Velo fuhr schon mit 3 m/s. Die Anfangsgeschwindigkeit kommt dazu.', 'sprich': 'Das Velo fuhr schon mit drei Metern pro Sekunde. Die Anfangsgeschwindigkeit kommt dazu.'}],
         'falsch_text': 'Nicht ganz. Gesamtkraft durch Masse gibt a; dann v = v₀ + a · t bei t = 4 s.',
         'falsch_sprich': 'Nicht ganz. Gesamtkraft durch Masse gibt die Beschleunigung; dann Anfangsgeschwindigkeit plus Beschleunigung mal Zeit, bei vier Sekunden.'},
        wahl('Frage 5', 'Ein Velo rollt ohne Antrieb aus. Wohin zeigt die Gesamtkraft?',
             ['nach vorn, in Fahrtrichtung', 'nach hinten, gegen die Fahrtrichtung', 'sie ist null'], 1,
             {0: 'Dann würde es schneller. Was bremst es?', 2: 'Dann behielte es sein Tempo. Wird es langsamer?'}),
    ]))

DREH.append(dict(KOPF, titel='Kraft sehen: Kontrollfragen zu Gewichtskraft und Aufzug', dateiname='p4-2-lp-kontrolle-aufzug',
    kurzbeschrieb='Fünf Fragen zu Gewichtskraft, Waage beim Anfahren und bei konstanter Fahrt, Bremsen der Abwärtsfahrt und Fall schwerer und leichter Körper.',
    schlagworte=['Gewichtskraft', 'Normalkraft', 'Aufzug', 'freier Fall', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'Masse mal g: drei mal neun Komma acht eins, rund neunundzwanzig Komma vier Newton.',
           formel(r'\fa{F_G} = m \cdot g = 3\;\text{kg} \cdot 9.81\;\text{m/s}^2 \approx \fa{29.4\;\text{N}}', g=46, ein=1.0)),
        sz('Frage 2', 'Beim Anfahren nach oben zeigt die Beschleunigung nach oben. Die Normalkraft muss grösser sein als die Gewichtskraft: Die Waage zeigt mehr.',
           formel(r'F_N = m \cdot (g + a) \gt m \cdot g', ein=1.0)),
        sz('Frage 3', 'Konstantes Tempo heisst a gleich null, auch nach unten. Die Waage zeigt dasselbe wie in Ruhe.',
           formel(r'a = 0 \;\Rightarrow\; F_N = \fa{F_G}', ein=1.0)),
        sz('Frage 4', 'Wer eine Abwärtsfahrt bremst, beschleunigt nach oben. Siebzig mal neun Komma acht eins plus eins Komma fünf, rund siebenhundertzweiundneunzig Newton.',
           formel(r'F_N = m \cdot (g + a) = 70\;\text{kg} \cdot 11.31\;\text{m/s}^2 \approx 792\;\text{N}', g=44, ein=1.0)),
        sz('Frage 5', 'Kabine, Waage und Person fallen alle mit g. Die Waage muss nicht mehr drücken: Sie zeigt null, obwohl die Gewichtskraft weiter wirkt.',
           formel(r'F_N = m \cdot (g + a) = m \cdot (g - g) = 0', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Welche Gewichtskraft erfährt ein Körper von 3 kg auf der Erde?',
             ['3 N', '29.4 N', '0.31 N'], 1,
             {0: 'Das ist die Zahl der Masse. Gefragt ist die Kraft in Newton: m · g.', 2: 'Geteilt? Die Gewichtskraft ist Masse mal g.'},
             sprich='Welche Gewichtskraft erfährt ein Körper von drei Kilogramm auf der Erde?',
             rueck_sprich={0: 'Das ist die Zahl der Masse. Gefragt ist die Kraft in Newton: m mal g.'}),
        wahl('Frage 2', 'Ein Aufzug fährt nach oben an. Was zeigt die Personenwaage darin?',
             ['mehr als in Ruhe', 'weniger als in Ruhe', 'gleich viel wie in Ruhe'], 0,
             {1: 'Wohin zeigt die Beschleunigung beim Anfahren nach oben?', 2: 'Die Person wird mitbeschleunigt. Dafür braucht es eine zusätzliche Kraft.'}),
        wahl('Frage 3', 'Ein Aufzug fährt mit konstantem Tempo nach unten. Was zeigt die Waage?',
             ['weniger als in Ruhe', 'mehr als in Ruhe', 'gleich viel wie in Ruhe'], 2,
             {0: 'Wie gross ist die Beschleunigung bei konstantem Tempo?', 1: 'Wie gross ist die Beschleunigung bei konstantem Tempo?'}),
        wahl('Frage 4', 'Eine Person (70 kg) fährt im Aufzug nach unten. Der Aufzug bremst mit 1.5 m/s². Welche Normalkraft misst die Waage?',
             ['582 N', '792 N', '105 N'], 1,
             {0: 'Richtung prüfen: Wer eine Abwärtsfahrt bremst, beschleunigt nach oben.', 2: 'Das ist nur m · a. Die Waage trägt auch die Gewichtskraft.'},
             sprich='Eine Person mit siebzig Kilogramm fährt im Aufzug nach unten. Der Aufzug bremst mit eins Komma fünf Metern pro Sekunde im Quadrat. Welche Normalkraft misst die Waage?',
             rueck_sprich={2: 'Das ist nur m mal a. Die Waage trägt auch die Gewichtskraft.'}),
        wahl('Frage 5', 'Das Seil des Aufzugs reisst, die Kabine fällt frei. Was zeigt die Waage unter der Person?',
             ['ihre Masse, wie in Ruhe', 'doppelt so viel', 'null'], 2,
             {0: 'In Ruhe drückt die Waage gegen die Gewichtskraft. Muss sie das im freien Fall auch?', 1: 'Die Beschleunigung zeigt nach unten. Zeigt die Waage dann mehr oder weniger?'}),
    ]))

DREH.append(dict(KOPF, titel='Kraft sehen: Kontrollfragen zu Faden und Kupplung', dateiname='p4-2-lp-kontrolle-faden',
    kurzbeschrieb='Fünf Fragen zur Beschleunigung von Wagen und hängendem Körper, zur Fadenkraft, zur Kupplungskraft und zur verdoppelten hängenden Masse.',
    schlagworte=['Fadenkraft', 'System', 'Kupplung', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Die Gewichtskraft von einem halben Kilogramm beschleunigt beide Körper, zusammen drei Komma fünf Kilogramm: rund eins Komma vier null Meter pro Sekunde im Quadrat.',
           formel(r'a = \dfrac{m_2 \cdot g}{m_1 + m_2} = \dfrac{0.5\;\text{kg} \cdot 9.81\;\text{m/s}^2}{3.5\;\text{kg}} \approx 1.40\;\text{m/s}^2', g=40, ein=1.0)),
        sz('Frage 2', 'Der hängende Körper beschleunigt nach unten. Also ist die Kraft nach unten grösser: Die Fadenkraft ist kleiner als seine Gewichtskraft.',
           formel(r'm_2 \cdot g - F_S = m_2 \cdot a \gt 0', ein=1.0)),
        sz('Frage 3', 'Zuerst das System: dreitausend Newton durch tausendfünfhundert Kilogramm, zwei Meter pro Sekunde im Quadrat. Den Anhänger zieht nur die Kupplung: fünfhundert mal zwei, tausend Newton.',
           formel(r'a = \dfrac{3000\;\text{N}}{1500\;\text{kg}} = 2\;\text{m/s}^2', g=48, ein=1.0),
           formel(r'F_K = 500\;\text{kg} \cdot 2\;\text{m/s}^2 = 1000\;\text{N}', y=440, g=48, ein=6.0)),
        sz('Frage 4', 'Festgehalten ruht alles. Die Gesamtkraft am hängenden Körper ist null: Die Fadenkraft trägt seine ganze Gewichtskraft, neun Komma acht eins Newton.',
           formel(r'a = 0 \;\Rightarrow\; F_S = m_2 \cdot g = 9.81\;\text{N}', ein=1.0)),
        sz('Frage 5', 'Der Zähler verdoppelt sich, aber der Nenner wächst auch. Darum wird die Beschleunigung weniger als doppelt so gross.',
           formel(r'a = \dfrac{m_2 \cdot g}{m_1 + m_2}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Wagen (3 kg) auf dem reibungsfreien Tisch wird von einem hängenden Körper (0.5 kg) gezogen. Wie gross ist die Beschleunigung?',
             ['9.81 m/s²', '1.64 m/s²', '1.40 m/s²'], 2,
             {0: 'So fiele der Körper allein. Er muss den Wagen mitziehen.', 1: 'Nur durch die Wagenmasse geteilt. Beschleunigt werden beide Körper.'},
             sprich='Ein Wagen mit drei Kilogramm auf dem reibungsfreien Tisch wird von einem hängenden Körper mit einem halben Kilogramm gezogen. Wie gross ist die Beschleunigung?'),
        wahl('Frage 2', 'Solange alles beschleunigt: Ist die Fadenkraft grösser, gleich oder kleiner als die Gewichtskraft des hängenden Körpers?',
             ['grösser', 'gleich', 'kleiner'], 2,
             {0: 'Dann würde der Körper nach oben beschleunigen.', 1: 'Dann wäre die Gesamtkraft auf ihn null, und er würde nicht schneller.'}),
        wahl('Frage 3', 'Ein Auto (1000 kg) zieht einen Anhänger (500 kg) mit 3000 N Antriebskraft, ohne Widerstand. Welche Kraft überträgt die Kupplung?',
             ['1000 N', '3000 N', '2000 N'], 0,
             {1: 'Die Antriebskraft beschleunigt Auto und Anhänger. Der Anhänger allein braucht weniger.', 2: 'Das ist die Kraft, die das Auto allein beschleunigt.'},
             sprich='Ein Auto mit tausend Kilogramm zieht einen Anhänger mit fünfhundert Kilogramm, mit dreitausend Newton Antriebskraft, ohne Widerstand. Welche Kraft überträgt die Kupplung?'),
        wahl('Frage 4', 'Man hält den Wagen fest. Wie gross ist jetzt die Fadenkraft, wenn 1 kg am Faden hängt?',
             ['0 N', '9.81 N', '4.9 N'], 1,
             {0: 'Der Körper fällt nicht. Was hält ihn?', 2: 'Halb so viel? Der Körper ruht. Wie gross muss die Kraft nach oben sein?'},
             sprich='Man hält den Wagen fest. Wie gross ist jetzt die Fadenkraft, wenn ein Kilogramm am Faden hängt?'),
        wahl('Frage 5', 'Die hängende Masse wird verdoppelt, der Wagen bleibt gleich. Wird die Beschleunigung doppelt so gross?',
             ['ja, genau doppelt', 'nein, weniger als doppelt', 'nein, mehr als doppelt'], 1,
             {0: 'Die antreibende Kraft verdoppelt sich. Und die Masse, die beschleunigt wird?', 2: 'Die antreibende Kraft verdoppelt sich, die beschleunigte Masse wächst auch.'}),
    ]))

DREH.append(dict(KOPF, titel='Kraft sehen: Kontrollfragen zur Zentripetalkraft', dateiname='p4-2-lp-kontrolle-kurve',
    kurzbeschrieb='Fünf Fragen zur Zentripetalkraft, zum verdreifachten Tempo, zum Mond auf seiner Bahn, zur gerissenen Schnur und zum Auto in der Kurve.',
    schlagworte=['Zentripetalkraft', 'Kreisbewegung', 'Trägheitsgesetz', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Masse mal v Quadrat durch r: null Komma fünf mal sechzehn durch vier, zwei Newton.',
           formel(r'\fd{F_z} = \dfrac{m \cdot \fc{v}^2}{r} = \dfrac{0.5\;\text{kg} \cdot (\fc{4\;\text{m/s}})^2}{4\;\text{m}} = \fd{2\;\text{N}}', g=42, ein=1.0)),
        sz('Frage 2', 'Das Tempo steht im Quadrat: drei mal drei, neunmal so viel Kraft.',
           formel(r'(3 \cdot \fc{v})^2 = 9 \cdot \fc{v}^2', ein=1.0)),
        sz('Frage 3', 'Die Gravitation der Erde zieht den Mond zur Mitte seiner Bahn. Sie übernimmt die Rolle der Zentripetalkraft.',
           notiz('Gravitation:|Kraft zur Mitte', y=320, ein=1.0, g=50)),
        sz('Frage 4', 'Ohne Kraft zur Mitte gilt das Trägheitsgesetz: Die Kugel fliegt geradeaus weiter, tangential zur Bahn.',
           notiz('ohne Kraft zur Mitte:|geradeaus weiter,|tangential', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Die Haftreibung zwischen Reifen und Strasse zeigt zur Kurvenmitte. Eine Zentrifugalkraft gibt es nur im mitdrehenden Bezugssystem.',
           notiz('Haftreibung:|Kraft zur Kurvenmitte', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Kugel (0.5 kg) kreist mit 4 m/s auf r = 4 m. Wie gross ist die Zentripetalkraft?',
             ['0.5 N', '2 N', '4 N'], 1,
             {0: 'Hier fehlt ein Quadrat.', 2: 'Das ist die Zentripetalbeschleunigung in m/s². Die Masse fehlt.'},
             sprich='Eine Kugel mit null Komma fünf Kilogramm kreist mit vier Metern pro Sekunde auf einem Radius von vier Metern. Wie gross ist die Zentripetalkraft?',
             rueck_sprich={2: 'Das ist die Zentripetalbeschleunigung in Metern pro Sekunde im Quadrat. Die Masse fehlt.'}),
        wahl('Frage 2', 'Das Tempo auf der Kreisbahn verdreifacht sich, der Radius bleibt. Die nötige Kraft …',
             ['verdreifacht sich', 'verneunfacht sich', 'bleibt gleich'], 1,
             {0: 'Wie steht v in der Formel? Einfach oder im Quadrat?', 2: 'Schnellere Kreisbewegung, gleiche Kraft? Schau, wie v in der Formel steht.'},
             sprich='Das Tempo auf der Kreisbahn verdreifacht sich, der Radius bleibt. Wie ändert sich die nötige Kraft?'),
        wahl('Frage 3', 'Welche Kraft hält den Mond auf seiner Bahn um die Erde?',
             ['die Gravitation der Erde', 'eine Kraft nach aussen', 'keine, er fliegt von selbst im Kreis'], 0,
             {1: 'Eine Kraft nach aussen würde ihn von der Bahn wegziehen. Wohin muss die Kraft zeigen?', 2: 'Ohne Kraft flöge er geradeaus weiter.'}),
        wahl('Frage 4', 'Eine Kugel kreist an einer Schnur. Die Schnur reisst. In welche Richtung fliegt die Kugel weg?',
             ['nach aussen, von der Mitte weg', 'zur Mitte hin', 'geradeaus, tangential zur Bahn'], 2,
             {0: 'Es gibt keine Kraft, die sie nach aussen zieht. Was sagt das Trägheitsgesetz?', 1: 'Zur Mitte zog sie die Schnur, und die ist weg.'}),
        wahl('Frage 5', 'Ein Auto fährt durch eine Kurve. Welche Kraft liefert die Zentripetalkraft?',
             ['die Haftreibung zwischen Reifen und Strasse', 'der Motor', 'die Zentrifugalkraft'], 0,
             {1: 'Der Motor treibt in Fahrtrichtung an. Gesucht ist eine Kraft zur Kurvenmitte.', 2: 'Die Zentrifugalkraft zeigt nach aussen und ist eine Scheinkraft. Gesucht ist eine Kraft zur Mitte.'}),
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
