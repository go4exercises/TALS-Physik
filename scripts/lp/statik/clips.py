"""Erzeugt die zwölf Drehbücher des Leitprogramms Statik (clips/p4-4-lp-*.json).

  python3 scripts/lp/statik/clips.py          # nur fehlende Drehbücher schreiben
  python3 scripts/lp/statik/clips.py --neu    # alle neu schreiben (überschreibt «dauer»!)
  python3 scripts/lp/statik/clips.py --neu p4-4-lp-kontrolle-hebel …   # nur diese

Archiv-Werkzeug wie scripts/lp/energie/clips.py: Nach der Vertonung sind die JSONs in clips/
die Quelle — build-clip-ton.py schreibt die gemessene Dauer hinein, und ein erneuter Lauf mit
--neu würde sie überschreiben. Späte Korrekturen direkt im JSON (HOWTO-leitprogramme §7).

Farben: Die Formeln bleiben ungefärbt; die Farben der Kräfte (Gewicht Bernstein, Normal- und
Auflagerkraft Grün, Reibung Türkis, Komponenten Violett, Resultierende Rot) zeigen die Bilder.
Bilder: Aufnahmen der Simulationen (clips/bilder/p4-4-lp-*.jpg). Zahlen im Sprechertext ausgeschrieben
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
    'lektion': ['p4-4'], 'stufe': ['BM1', 'BM2'], 'datum': '2026-10-05', 'theme': 'begreifbar-schlicht',
    'latex': True, 'reihe': 'Statik sehen', 'nachlauf': 2.6, 'probe': True,
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
EIN = 'Einführungsclip des Leitprogramms Statik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'
KTRL = 'Kontrollclip des Leitprogramms Statik, Kapitel %d; gehört dorthin, nicht in die Clip-Bibliothek.'

# ================================================================== Kapitel 1
DREH.append(dict(KOPF, titel='Statik sehen: die Kraft als Pfeil', dateiname='p4-4-lp-vektor',
    kurzbeschrieb='Was eine Kraft bewirkt, Betrag, Richtung und Angriffspunkt, die Zerlegung in Komponenten mit Kosinus und Sinus, ihre Vorzeichen und der Betrag aus den Komponenten.',
    schlagworte=['Kraft', 'Vektor', 'Komponenten', 'Wirkungslinie', 'Newton'], _probe=EIN % 1,
    szenen=[
        sz('Kraft', 'Eine Kraft verformt einen Körper, oder sie ändert seine Bewegung: schneller, langsamer, in eine andere Richtung. Gemessen wird sie in Newton, zum Beispiel mit einem Federkraftmesser.',
           titel('Was ist eine Kraft?', g=76),
           notiz('verformt|oder ändert die Bewegung|Einheit: Newton', y=440, ein=2.0)),
        sz('Pfeil', 'Eine Kraft ist ein Vektor. Man zeichnet sie als Pfeil: Die Länge zeigt den Betrag, die Spitze die Richtung, der Anfang den Angriffspunkt. Die Gerade durch den Pfeil heisst Wirkungslinie. Längs der Wirkungslinie darf man die Kraft verschieben, quer dazu nicht.',
           titel('Kraft als Pfeil', y=260, g=76),
           notiz('Betrag, Richtung,|Angriffspunkt|Wirkungslinie', y=440, ein=3.0)),
        sz('Komponenten', 'Eine Kraft von sechzig Newton zeigt unter vierzig Grad zur x-Achse. Man zerlegt sie in zwei Teile längs der Achsen. Der Teil am Winkel gehört zum Kosinus: F x gleich F mal Kosinus Phi, rund sechsundvierzig Newton. Der Teil gegenüber gehört zum Sinus: F y, rund achtunddreissig Komma sechs Newton.',
           formel(r'F_x = F \cdot \cos\varphi \approx 46.0\;\text{N}', y=300, g=50, ein=8.0),
           formel(r'F_y = F \cdot \sin\varphi \approx 38.6\;\text{N}', y=420, g=50, ein=13.0),
           bild('p4-4-lp-vektor-1.jpg', breite=620, y=180)),
        sz('Vorzeichen', 'Zeigt dieselbe Kraft unter hundertfünfzig Grad nach links oben, wird F x negativ: minus zweiundfünfzig Newton. Die Vorzeichen ergeben sich von selbst, wenn man den Winkel immer von der positiven x-Achse aus gegen den Uhrzeigersinn misst.',
           formel(r'F_x = 60\;\text{N} \cdot \cos 150^\circ \approx -52.0\;\text{N}', y=300, g=46, ein=4.0),
           formel(r'\text{links: } F_x < 0 \qquad \text{unten: } F_y < 0', y=440, ein=9.0, g=44),
           bild('p4-4-lp-vektor-2.jpg', breite=620, y=180)),
        sz('Rückwärts', 'Rückwärts geht es mit Pythagoras. Achtzig Newton nach rechts und sechzig Newton nach oben geben zusammen hundert Newton, nicht hundertvierzig. Den Winkel liefert der Tangens: rund sechsunddreissig Komma neun Grad.',
           formel(r'F = \sqrt{F_x^2 + F_y^2} = \sqrt{(80\;\text{N})^2 + (60\;\text{N})^2} = 100\;\text{N}', y=300, g=42, ein=2.0),
           formel(r'\tan\varphi = \frac{F_y}{F_x} = \frac{60}{80} \quad \varphi \approx 36.9^\circ', y=440, g=46, ein=10.0)),
        sz('Merke', 'Zum Mitnehmen: Eine Kraft hat Betrag, Richtung und Angriffspunkt. Ihre Komponenten sind F mal Kosinus Phi und F mal Sinus Phi, den Betrag gibt Pythagoras.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_x = F \cdot \cos\varphi \qquad F_y = F \cdot \sin\varphi', y=420, g=46, ein=0.4),
           formel(r'F = \sqrt{F_x^2 + F_y^2}', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 2
DREH.append(dict(KOPF, titel='Statik sehen: Kräfte aneinanderhängen', dateiname='p4-4-lp-resultierende',
    kurzbeschrieb='Die resultierende Kraft grafisch (Spitze an Fuss, Parallelogramm) und über die Komponenten, Sonderfälle gleich- und entgegengesetzter Kräfte und das Kräftegleichgewicht als geschlossenes Krafteck.',
    schlagworte=['Resultierende', 'Vektoraddition', 'Kräfteparallelogramm', 'Kräftegleichgewicht', 'Krafteck'], _probe=EIN % 2,
    szenen=[
        sz('Spitze an Fuss', 'Zwei Kräfte von je siebzig Newton greifen an einem Ring an, die eine nach rechts, die andere unter sechzig Grad. Man hängt den zweiten Pfeil an die Spitze des ersten: Spitze an Fuss.',
           titel('Spitze an Fuss', y=260, g=76),
           notiz('70 N bei 0°|70 N bei 60°', y=440, ein=3.0),
           bild('p4-4-lp-resultierende-1.jpg')),
        sz('Resultierende', 'Der Pfeil vom ersten Fuss zur letzten Spitze ist die Resultierende. Sie ersetzt beide Kräfte. Hier sind es rund hunderteinundzwanzig Newton, nicht hundertvierzig: Verschieden gerichtete Kräfte darf man nicht einfach addieren.',
           formel(r'F_\text{res} \approx 121\;\text{N}', y=300, g=54, ein=6.0),
           notiz('nicht 70 N + 70 N', y=440, ein=11.0),
           bild('p4-4-lp-resultierende-2.jpg')),
        sz('Komponenten', 'Rechnen geht über die Komponenten. In x-Richtung: siebzig plus siebzig mal Kosinus sechzig, hundertfünf Newton. In y-Richtung: siebzig mal Sinus sechzig, rund sechzig Komma sechs Newton. Pythagoras gibt wieder rund hunderteinundzwanzig Newton.',
           formel(r'F_{\text{res},x} = 70\;\text{N} + 70\;\text{N} \cdot \cos 60^\circ = 105\;\text{N}', y=280, g=42, ein=2.0),
           formel(r'F_{\text{res},y} = 70\;\text{N} \cdot \sin 60^\circ \approx 60.6\;\text{N}', y=390, g=42, ein=7.5),
           formel(r'F_\text{res} = \sqrt{F_{\text{res},x}^2 + F_{\text{res},y}^2} \approx 121\;\text{N}', y=500, g=42, ein=12.5)),
        sz('Sonderfälle', 'Nur in zwei Fällen ist es einfacher. Gleich gerichtet addieren sich die Beträge, entgegengesetzt subtrahieren sie sich. Darum liegt die Resultierende zweier Kräfte immer zwischen ihrer Differenz und ihrer Summe.',
           notiz('gleich gerichtet: F₁ + F₂|entgegengesetzt: F₁ − F₂', y=320, ein=2.0, g=48),
           notiz('dazwischen: alle anderen Winkel', y=500, ein=7.0, g=44)),
        sz('Gleichgewicht', 'Drei Kräfte von je achtzig Newton zeigen nach oben und schräg nach links und rechts unten. Aneinandergehängt schliessen sie sich zu einem Dreieck: Die Resultierende ist null. Das ist das Kräftegleichgewicht, und der Ring bleibt in Ruhe.',
           formel(r'\vec{F}_1 + \vec{F}_2 + \vec{F}_3 = \vec{0}', y=300, g=50, ein=5.0),
           notiz('geschlossenes Krafteck:|Gleichgewicht', y=440, ein=8.0),
           bild('p4-4-lp-resultierende-3.jpg')),
        sz('Merke', 'Zum Mitnehmen: Kräfte addiert man als Pfeile oder über die Komponenten. Schliessen sich die Pfeile, herrscht Gleichgewicht.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_{\text{res},x} = \sum F_x \qquad F_{\text{res},y} = \sum F_y', y=420, g=46, ein=0.4),
           formel(r'F_\text{res} = 0:\ \text{Gleichgewicht}', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 3
DREH.append(dict(KOPF, titel='Statik sehen: Gewicht, Normalkraft und Haftreibung', dateiname='p4-4-lp-ruhe',
    kurzbeschrieb='Die Kräfte an einem ruhenden Körper: Gewichtskraft, Normalkraft und Haftreibung, die sich anpasst; die Zerlegung auf der schiefen Ebene und die Haftbedingung tan α ≤ μ_H.',
    schlagworte=['Gewichtskraft', 'Normalkraft', 'Auflagerkraft', 'Haftreibung', 'schiefe Ebene'], _probe=EIN % 3,
    szenen=[
        sz('Waagrecht', 'Eine Kiste mit zwölf Kilogramm liegt auf einem waagrechten Brett. Die Gewichtskraft zieht sie senkrecht nach unten, sie greift im Schwerpunkt an. Das Brett drückt mit der Normalkraft senkrecht zur Fläche zurück, genau so stark. Die Summe ist null, die Kiste ruht.',
           formel(r'F_G = m \cdot g \approx 118\;\text{N}', y=300, g=50, ein=5.0),
           formel(r'F_N = F_G:\ \text{Kiste ruht}', y=440, ein=11.0),
           bild('p4-4-lp-ruhe-1.jpg')),
        sz('Haftreibung', 'Zieht man seitlich, hält die Haftreibung dagegen. Sie ist nur so gross wie nötig und passt sich der Zugkraft an, aber höchstens bis My H mal F N. Die Haftreibungszahl My H hängt von den Materialien ab und hat keine Einheit.',
           titel('Haftreibung', y=260, g=76),
           formel(r'F_R \le \mu_H \cdot F_N', y=430, g=54, ein=8.0)),
        sz('Schiefe Ebene', 'Jetzt steht das Brett unter dreissig Grad. Man zerlegt die Gewichtskraft längs und senkrecht zum Brett. Längs zieht die Hangabtriebskraft, F G mal Sinus Alpha, rund achtundfünfzig Komma neun Newton. Senkrecht drückt F G mal Kosinus Alpha, rund hundertzwei Newton; so gross ist auch die Normalkraft.',
           formel(r'F_H = F_G \cdot \sin\alpha \approx 58.9\;\text{N}', y=300, g=48, ein=8.0),
           formel(r'F_N = F_G \cdot \cos\alpha \approx 102\;\text{N}', y=420, g=48, ein=14.0),
           bild('p4-4-lp-ruhe-2.jpg')),
        sz('Haften', 'Bei My H gleich null Komma sechs fünf kann die Haftreibung höchstens rund sechsundsechzig Newton aufbringen. Das reicht für achtundfünfzig Komma neun Newton Hangabtrieb: Die Kiste haftet, und die Reibung ist genau so gross wie der Hangabtrieb.',
           formel(r'\mu_H \cdot F_N \approx 66.3\;\text{N} > F_H', y=300, g=48, ein=5.0),
           formel(r'\text{haftet: } F_R = F_H', y=440, ein=11.0)),
        sz('Grenzwinkel', 'Neigt man weiter, wächst der Hangabtrieb, und die Normalkraft nimmt ab. Gleich gross werden sie, wenn der Tangens des Winkels gleich My H ist. Die Masse kürzt sich heraus. Hier rutscht die Kiste ab rund dreiunddreissig Grad.',
           formel(r'\tan\alpha \le \mu_H', y=300, g=54, ein=6.0),
           formel(r'\alpha_\text{max} = \arctan 0.65 \approx 33.0^\circ', y=420, g=46, ein=12.0),
           bild('p4-4-lp-ruhe-3.jpg')),
        sz('Merke', 'Zum Mitnehmen: Am ruhenden Körper wirken Gewichtskraft, Normalkraft und Haftreibung, und ihre Summe ist null. Auf der schiefen Ebene haftet er, solange der Tangens des Neigungswinkels höchstens My H ist.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_H = F_G \cdot \sin\alpha \qquad F_N = F_G \cdot \cos\alpha', y=420, g=44, ein=0.4),
           formel(r'\text{haftet, solange } \tan\alpha \le \mu_H', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 4
DREH.append(dict(KOPF, titel='Statik sehen: Kraft mal Hebelarm', dateiname='p4-4-lp-drehmoment',
    kurzbeschrieb='Das Drehmoment als Kraft mal wirksamer Hebelarm, die schräge Kraft mit M = F · l · sin α, die Kraft durch die Achse, Einheit und Vorzeichen, Anwendungen vom Schraubenschlüssel bis zum Kran.',
    schlagworte=['Drehmoment', 'Hebelarm', 'Newtonmeter', 'Schraubenschlüssel', 'Wirkungslinie'], _probe=EIN % 4,
    szenen=[
        sz('Drehwirkung', 'Eine festsitzende Schraube löst man nicht mit Kraft allein. Es zählt, wie weit aussen und in welche Richtung man zieht. Diese Drehwirkung heisst Drehmoment.',
           titel('Was dreht?', g=76),
           notiz('Kraft und Abstand|zur Drehachse', y=440, ein=3.0)),
        sz('Senkrecht', 'Hundertzwanzig Newton greifen senkrecht am Schlüssel an, null Komma zwei fünf Meter von der Drehachse D. Das Drehmoment ist Kraft mal Hebelarm: dreissig Newtonmeter. Doppelt so langer Schlüssel, halbe Kraft für dasselbe Moment.',
           formel(r'M = F \cdot r = 120\;\text{N} \cdot 0.25\;\text{m} = 30\;\text{Nm}', y=300, g=44, ein=6.0),
           notiz('M = F · r|aufgelöst: F = M / r', y=440, ein=12.0),
           bild('p4-4-lp-drehmoment-1.jpg')),
        sz('Schräg', 'Zieht man schräg, unter sechzig Grad zum Schlüssel, zählt nur der wirksame Hebelarm: der senkrechte Abstand der Wirkungslinie von D, l mal Sinus Alpha. Das Drehmoment sinkt auf rund sechsundzwanzig Newtonmeter.',
           formel(r'M = F \cdot l \cdot \sin\alpha', y=300, g=54, ein=6.0),
           formel(r'= 120\;\text{N} \cdot 0.25\;\text{m} \cdot \sin 60^\circ \approx 26.0\;\text{Nm}', y=420, g=42, ein=11.0),
           bild('p4-4-lp-drehmoment-2.jpg')),
        sz('Durch die Achse', 'Zieht man genau längs des Schlüssels, geht die Wirkungslinie durch die Drehachse. Der Hebelarm ist null, und es dreht sich nichts, egal wie stark man zieht.',
           formel(r'\alpha = 0^\circ:\quad r = 0,\; M = 0', y=300, g=50, ein=3.0),
           bild('p4-4-lp-drehmoment-3.jpg')),
        sz('Einheit', 'Die Einheit ist das Newtonmeter. Dreht die Kraft gegen den Uhrzeigersinn, zählt das Moment positiv, im Uhrzeigersinn negativ. Drehmomente nutzt man überall: am Schraubenschlüssel und am Radkreuz, an Türgriff und Lenkrad, an der Velokurbel, an Wippe, Kran und Motor.',
           titel('Newtonmeter', y=240, g=70),
           notiz('gegen den Uhrzeigersinn: +|im Uhrzeigersinn: −', y=380, ein=3.0, g=44),
           notiz('Schlüssel, Radkreuz, Türgriff,|Lenkrad, Velokurbel, Wippe, Kran', y=540, ein=10.0, g=42)),
        sz('Merke', 'Zum Mitnehmen: Das Drehmoment ist Kraft mal wirksamer Hebelarm. Am grössten ist es, wenn die Kraft senkrecht zum Hebel steht.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'M = F \cdot r = F \cdot l \cdot \sin\alpha', y=420, g=48, ein=0.4),
           notiz('Einheit: Nm', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 5
DREH.append(dict(KOPF, titel='Statik sehen: das Hebelgesetz', dateiname='p4-4-lp-hebel',
    kurzbeschrieb='Gleichgewicht der Drehmomente an der Wippe, das Hebelgesetz F₁ · r₁ = F₂ · r₂, zwei- und einarmige Hebel, mehrere Kräfte auf einer Seite und das Gewicht des Bretts im Drehpunkt.',
    schlagworte=['Hebelgesetz', 'Wippe', 'Drehmoment', 'Brechstange', 'Gleichgewicht'], _probe=EIN % 5,
    szenen=[
        sz('Wippe', 'Links sitzt ein Kind mit dreissig Kilogramm, eins Komma sechs Meter von der Achse. Rechts sitzt eins mit vierzig Kilogramm. Wo muss es sitzen, damit die Wippe waagrecht bleibt?',
           titel('Die Wippe', y=260, g=76),
           notiz('30 kg bei 1.6 m|40 kg bei ?', y=440, ein=4.0)),
        sz('Gleichgewicht', 'Die Wippe bleibt, wenn die Drehmomente links und rechts gleich gross sind. G kürzt sich, es bleibt Masse mal Abstand. Dreissig mal eins Komma sechs geteilt durch vierzig: eins Komma zwei Meter. Das schwerere Kind sitzt näher an der Achse.',
           formel(r'm_1 \cdot g \cdot r_1 = m_2 \cdot g \cdot r_2', y=280, g=48, ein=3.0),
           formel(r'r_2 = \frac{30\;\text{kg} \cdot 1.6\;\text{m}}{40\;\text{kg}} = 1.2\;\text{m}', y=420, g=44, ein=9.0),
           bild('p4-4-lp-hebel-1.jpg')),
        sz('Kippen', 'Setzt sich das schwerere Kind auch auf eins Komma sechs Meter, ist sein Moment grösser, und die Wippe kippt zu ihm. Es entscheidet nicht die Kraft allein, sondern Kraft mal Hebelarm.',
           notiz('rechts: grösseres Moment|kippt nach rechts', y=320, ein=3.0),
           bild('p4-4-lp-hebel-2.jpg')),
        sz('Hebelgesetz', 'Allgemein heisst das Hebelgesetz: F eins mal r eins gleich F zwei mal r zwei. Bei Wippe und Balkenwaage liegen die Kräfte auf beiden Seiten der Achse, bei Schubkarre und Brechstange auf derselben. Immer gilt: Kraft mal Kraftarm gleich Last mal Lastarm. Ein langer Kraftarm spart Kraft.',
           formel(r'F_1 \cdot r_1 = F_2 \cdot r_2', y=280, g=56, ein=2.0),
           notiz('Kraft · Kraftarm|= Last · Lastarm', y=440, ein=14.0)),
        sz('Mehrere', 'Sitzen links zwei Kinder, drehen beide in dieselbe Richtung: Ihre Momente addieren sich, jedes mit seinem eigenen Hebelarm. Das Brett der Wippe dagegen zählt nicht: Sein Gewicht greift in der Mitte an, im Drehpunkt, und hat keinen Hebelarm.',
           formel(r'\sum M = 0', y=300, g=56, ein=1.0),
           notiz('jede Last mit ihrem|eigenen Hebelarm', y=440, ein=6.0)),
        sz('Merke', 'Zum Mitnehmen: Ein Hebel ist im Gleichgewicht, wenn die Drehmomente links herum und rechts herum gleich gross sind.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'F_1 \cdot r_1 = F_2 \cdot r_2', y=420, g=50, ein=0.4),
           notiz('langer Arm: kleine Kraft', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kapitel 6
DREH.append(dict(KOPF, titel='Statik sehen: zwei Stützen teilen sich die Last', dateiname='p4-4-lp-auflager',
    kurzbeschrieb='Statisches Gleichgewicht mit Kräfte- und Momentenbedingung, die Drehachse am Auflager, die Auflagerkräfte eines Balkens auf zwei Stützen, das Eigengewicht in der Mitte und der Wagen auf der Brücke.',
    schlagworte=['statisches Gleichgewicht', 'Auflagerkraft', 'Momentengleichgewicht', 'Balken', 'Brücke'], _probe=EIN % 6,
    szenen=[
        sz('Bedingungen', 'Ein Körper ist im statischen Gleichgewicht, wenn er sich weder verschiebt noch zu drehen beginnt. Dafür muss die Summe aller Kräfte null sein und die Summe aller Drehmomente auch.',
           titel('Statisches Gleichgewicht', y=260, g=66),
           formel(r'\sum \vec{F} = \vec{0} \qquad \sum M = 0', y=430, g=52, ein=6.0)),
        sz('Brücke', 'Ein Wagen mit fünfzig Kilonewton steht auf einer Brücke, zwei Meter von der Stütze A, zehn Meter von A bis B. Wie verteilen die Stützen die Last?',
           titel('Zwei Stützen', y=260, g=76),
           bild('p4-4-lp-auflager-1.jpg')),
        sz('Momente um A', 'Man legt die Drehachse in die Stütze A. Dann fällt F A heraus, denn ihr Hebelarm ist null. F B mal zehn Meter gleich fünfzig Kilonewton mal zwei Meter: F B ist zehn Kilonewton.',
           formel(r'F_B \cdot L = F \cdot x', y=280, g=52, ein=5.0),
           formel(r'F_B = \frac{50\;\text{kN} \cdot 2\;\text{m}}{10\;\text{m}} = 10\;\text{kN}', y=420, g=44, ein=9.5),
           bild('p4-4-lp-auflager-1.jpg', ein=0.05)),
        sz('Kräfte', 'Die Kräftebedingung gibt den Rest: Zusammen tragen die Stützen die ganze Last. F A ist fünfzig minus zehn, vierzig Kilonewton. Die nähere Stütze trägt mehr.',
           formel(r'F_A = F - F_B = 40\;\text{kN}', y=300, g=50, ein=4.0),
           notiz('nähere Stütze|trägt mehr', y=440, ein=9.0)),
        sz('Fahrt', 'Fährt der Wagen von A nach B, nimmt F A gleichmässig ab und F B gleichmässig zu. Ihre Summe bleibt die ganze Last. Hat die Brücke ein Eigengewicht, greift es in ihrer Mitte an, und jede Stütze trägt die Hälfte davon dazu.',
           formel(r'F_A + F_B = \text{ganze Last}', y=300, ein=4.0),
           notiz('Eigengewicht: in der Mitte', y=440, ein=11.0),
           bild('p4-4-lp-auflager-2.jpg')),
        sz('Merke', 'Zum Mitnehmen: Im statischen Gleichgewicht sind Kräftesumme und Momentensumme null. Die Drehachse legt man dorthin, wo eine unbekannte Kraft angreift.',
           titel('Zum Mitnehmen', y=260, g=76),
           formel(r'\sum \vec{F} = \vec{0} \qquad \sum M = 0', y=420, g=48, ein=0.4),
           formel(r'F_B = \frac{F \cdot x}{L}', y=570, ein=1.2, g=44)),
        JETZT,
    ]))

# ================================================================== Kontrollclips
DREH.append(dict(KOPF, titel='Statik sehen: Kontrollfragen zur Kraft als Vektor', dateiname='p4-4-lp-kontrolle-vektor',
    kurzbeschrieb='Fünf Fragen zu den Angaben einer Kraft, zu Komponenten, Vorzeichen und zum Betrag aus den Komponenten.',
    schlagworte=['Kraft', 'Vektor', 'Komponenten', 'Kontrollfragen'], _probe=KTRL % 1,
    szenen=[
        sz('Frage 1', 'Eine Kraft ist erst mit Betrag, Richtung und Angriffspunkt festgelegt.',
           notiz('Betrag, Richtung,|Angriffspunkt', y=320, ein=1.0, g=50)),
        sz('Frage 2', 'Senkrecht nach oben hat die Kraft keinen Anteil in x-Richtung: Kosinus neunzig Grad ist null.',
           formel(r'F_x = 200\;\text{N} \cdot \cos 90^\circ = 0\;\text{N}', ein=1.0)),
        sz('Frage 3', 'Die senkrechte Komponente gehört zum Sinus: vierzig Newton mal Sinus dreissig Grad, zwanzig Newton.',
           formel(r'F_y = 40\;\text{N} \cdot \sin 30^\circ = 20\;\text{N}', ein=1.0)),
        sz('Frage 4', 'Nach links unten sind beide Komponenten negativ.',
           formel(r'F_x < 0 \text{ und } F_y < 0', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Pythagoras: Wurzel aus neun im Quadrat plus zwölf im Quadrat, fünfzehn Newton.',
           formel(r'F = \sqrt{(9\;\text{N})^2 + (12\;\text{N})^2} = 15\;\text{N}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Welche Angaben legen eine Kraft vollständig fest?',
             ['nur der Betrag in Newton', 'Betrag, Richtung und Angriffspunkt', 'Masse und Beschleunigung'], 1,
             {0: 'Drückst du gleich stark, aber in eine andere Richtung — passiert dasselbe?', 2: 'Damit berechnet man die Gesamtkraft. Was zeigt der Pfeil?'}),
        wahl('Frage 2', 'Eine Kraft von 200 N zeigt senkrecht nach oben (φ = 90°). Wie gross ist F_x?',
             ['200 N', '0 N', '100 N'], 1,
             {0: 'Das ist der ganze Betrag. Wie viel davon zeigt in x-Richtung?', 2: 'Halbieren hat hier keinen Grund. Was ist cos 90°?'},
             sprich='Eine Kraft von zweihundert Newton zeigt senkrecht nach oben, Phi gleich neunzig Grad. Wie gross ist F x?'),
        wahl('Frage 3', 'Seil: 40 N unter φ = 30° zur Waagrechten. Wie gross ist die senkrechte Komponente F_y?',
             ['34.6 N', '40 N', '20 N'], 2,
             {0: 'Das ist die waagrechte Komponente, mit dem Kosinus.', 1: 'Das ist die ganze Kraft. Gesucht ist nur ihr senkrechter Anteil.'},
             sprich='Ein Seil zieht mit vierzig Newton unter Phi gleich dreissig Grad zur Waagrechten. Wie gross ist die senkrechte Komponente F y?',
             rueck_sprich={0: 'Das ist die waagrechte Komponente, mit dem Kosinus.'}),
        wahl('Frage 4', 'Ein Pfeil zeigt nach links unten. Welche Vorzeichen haben seine Komponenten?',
             ['F_x > 0 und F_y < 0', 'beide positiv', 'F_x < 0 und F_y < 0'], 2,
             {0: 'Zeigt der Pfeil nach rechts?', 1: 'Nach links und nach unten heisst …?'},
             sprich='Ein Pfeil zeigt nach links unten. Welche Vorzeichen haben seine Komponenten?',
             rueck_sprich={0: 'Zeigt der Pfeil nach rechts?', 1: 'Nach links und nach unten heisst …?'}),
        wahl('Frage 5', 'Komponenten F_x = 9 N und F_y = 12 N. Wie gross ist der Betrag der Kraft?',
             ['15 N', '21 N', '225 N'], 0,
             {1: 'Komponenten stehen senkrecht aufeinander: nicht addieren.', 2: 'Noch die Wurzel ziehen.'},
             sprich='Eine Kraft hat die Komponenten F x gleich neun Newton und F y gleich zwölf Newton. Wie gross ist ihr Betrag?'),
    ]))

DREH.append(dict(KOPF, titel='Statik sehen: Kontrollfragen zur resultierenden Kraft', dateiname='p4-4-lp-kontrolle-resultierende',
    kurzbeschrieb='Fünf Fragen zu gleich gerichteten und rechtwinkligen Kräften, zum geschlossenen Krafteck, zur kleinsten Resultierenden und zur Richtung.',
    schlagworte=['Resultierende', 'Kräftegleichgewicht', 'Kontrollfragen'], _probe=KTRL % 2,
    szenen=[
        sz('Frage 1', 'Gleich gerichtet addieren sich die Beträge: dreissig plus vierzig, siebzig Newton.',
           formel(r'F_\text{res} = 30\;\text{N} + 40\;\text{N} = 70\;\text{N}', ein=1.0)),
        sz('Frage 2', 'Im rechten Winkel gilt Pythagoras: Wurzel aus fünfunddreissig im Quadrat plus hundertzwanzig im Quadrat, hundertfünfundzwanzig Newton.',
           formel(r'F_\text{res} = \sqrt{(35\;\text{N})^2 + (120\;\text{N})^2} = 125\;\text{N}', g=46, ein=1.0)),
        sz('Frage 3', 'Schliessen sich die Pfeile, endet der letzte am Fuss des ersten: Die Resultierende ist null.',
           formel(r'\vec{F}_\text{res} = \vec{0}', ein=1.0)),
        sz('Frage 4', 'Entgegengesetzte Kräfte heben sich teilweise auf: Die Resultierende kann kleiner sein als jede einzelne Kraft.',
           notiz('50 N und 40 N entgegengesetzt:|nur 10 N', y=320, ein=1.0, g=48)),
        sz('Frage 5', 'Gleich grosse Komponenten nach rechts und nach oben: Die Resultierende zeigt unter fünfundvierzig Grad nach rechts oben.',
           notiz('rechts oben, 45°', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', 'Zwei Kräfte von 30 N und 40 N ziehen in dieselbe Richtung. Wie gross ist die Resultierende?',
             ['50 N', '70 N', '10 N'], 1,
             {0: 'Pythagoras gilt nur im rechten Winkel.', 2: 'Subtrahieren nur bei entgegengesetzter Richtung.'},
             sprich='Zwei Kräfte von dreissig Newton und vierzig Newton ziehen in dieselbe Richtung. Wie gross ist die Resultierende?'),
        wahl('Frage 2', 'Rechtwinklig zueinander: 35 N und 120 N. Wie gross ist die Resultierende?',
             ['155 N', '85 N', '125 N'], 2,
             {0: 'Addieren nur bei gleicher Richtung.', 1: 'Subtrahieren nur bei entgegengesetzter Richtung.'},
             sprich='Zwei Kräfte stehen rechtwinklig zueinander: fünfunddreissig Newton und hundertzwanzig Newton. Wie gross ist die Resultierende?'),
        wahl('Frage 3', 'Drei Kraftpfeile, Spitze an Fuss gehängt, bilden ein geschlossenes Dreieck. Wie gross ist die Resultierende?',
             ['null', 'so gross wie die grösste Kraft', 'die Summe der drei Beträge'], 0,
             {1: 'Wo endet der letzte Pfeil, wenn sich das Dreieck schliesst?', 2: 'Wo endet der letzte Pfeil, wenn sich das Dreieck schliesst?'}),
        wahl('Frage 4', 'Kann die Resultierende zweier Kräfte kleiner sein als jede der beiden?',
             ['nein, nie', 'ja, wenn sie fast entgegengesetzt ziehen', 'nur bei drei Kräften'], 1,
             {0: 'Was geschieht, wenn zwei Kräfte gegeneinander ziehen?', 2: 'Schon zwei Kräfte genügen. Welche Richtung?'}),
        wahl('Frage 5', 'Am Ring: 50 N nach rechts und 50 N nach oben. Wohin zeigt die Resultierende?',
             ['unter 45° nach rechts oben', 'senkrecht nach oben', 'waagrecht nach rechts'], 0,
             {1: 'Die Kraft nach rechts zählt auch mit.', 2: 'Die Kraft nach oben zählt auch mit.'},
             sprich='Am Ring ziehen fünfzig Newton nach rechts und fünfzig Newton nach oben. Wohin zeigt die Resultierende?'),
    ]))

DREH.append(dict(KOPF, titel='Statik sehen: Kontrollfragen zu den Kräften am ruhenden Körper', dateiname='p4-4-lp-kontrolle-ruhe',
    kurzbeschrieb='Fünf Fragen zur Normalkraft, zur Hangabtriebskraft, zur Haftreibung, die sich anpasst, zum Grenzwinkel und zur Rolle der Masse.',
    schlagworte=['Normalkraft', 'Haftreibung', 'schiefe Ebene', 'Kontrollfragen'], _probe=KTRL % 3,
    szenen=[
        sz('Frage 1', 'Die Unterlage drückt mit der Normalkraft zurück, senkrecht zur Fläche. Waagrecht ist sie so gross wie die Gewichtskraft.',
           formel(r'\text{Normalkraft } F_N = F_G', y=320, ein=1.0, g=50)),
        sz('Frage 2', 'Hangabtrieb ist Gewichtskraft mal Sinus Alpha: fünfzig mal neun Komma acht eins mal Sinus zehn Grad, rund fünfundachtzig Newton.',
           formel(r'F_H = 50\;\text{kg} \cdot 9.81\;\text{m/s}^2 \cdot \sin 10^\circ \approx 85.2\;\text{N}', g=40, ein=1.0)),
        sz('Frage 3', 'Die Kiste ruht. Die Haftreibung ist so gross wie nötig, also so gross wie der Hangabtrieb: vierzig Newton. Siebzig Newton wären nur der Höchstwert.',
           formel(r'F_R = F_H = 40\;\text{N}', ein=1.0)),
        sz('Frage 4', 'An der Grenze ist der Tangens des Winkels gleich My H: Arcustangens null Komma zwei fünf, rund vierzehn Grad.',
           formel(r'\alpha = \arctan 0.25 \approx 14.0^\circ', ein=1.0)),
        sz('Frage 5', 'Die Masse kürzt sich heraus. Der Grenzwinkel bleibt gleich.',
           formel(r'\tan\alpha = \mu_H', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Eine Kiste liegt auf waagrechtem Boden. Welche Kraft hält sie gegen die Gewichtskraft?',
             ['die Haftreibung', 'die Normalkraft des Bodens', 'keine, sie liegt einfach'], 1,
             {0: 'Die Haftreibung wirkt längs der Fläche, nicht senkrecht.', 2: 'Ohne Gegenkraft würde die Gewichtskraft sie beschleunigen.'}),
        wahl('Frage 2', 'Kiste, 50 kg, auf einer Rampe mit α = 10°. Wie gross ist die Hangabtriebskraft?',
             ['85.2 N', '483 N', '490.5 N'], 0,
             {1: 'Das ist die Komponente senkrecht zur Rampe, mit dem Kosinus.', 2: 'Das ist die ganze Gewichtskraft.'},
             sprich='Eine Kiste mit fünfzig Kilogramm steht auf einer Rampe mit Alpha gleich zehn Grad. Wie gross ist die Hangabtriebskraft?'),
        wahl('Frage 3', 'Eine Kiste ruht auf einer Rampe: F_H = 40 N, höchstens möglich wären μ_H · F_N = 70 N. Wie gross ist die Haftreibung?',
             ['70 N', '40 N', '110 N'], 1,
             {0: 'Das ist nur ihr Höchstwert. Wie viel braucht es, damit die Kiste ruht?', 2: 'Die Reibung hält gegen den Hangabtrieb. Wie viel braucht es?'},
             sprich='Eine Kiste ruht auf einer Rampe. Der Hangabtrieb ist vierzig Newton, höchstens möglich wären siebzig Newton Haftreibung. Wie gross ist die Haftreibung?',
             rueck_sprich={0: 'Das ist nur ihr Höchstwert. Wie viel braucht es, damit die Kiste ruht?'}),
        wahl('Frage 4', 'Haftreibungszahl μ_H = 0.25. Bis zu welchem Neigungswinkel haftet ein Körper?',
             ['14.5°', '75.5°', '14.0°'], 2,
             {0: 'Das ist mit dem Arcussinus. An der Grenze gilt tan α = μ_H.', 1: 'Das ist mit dem Arcuskosinus. An der Grenze gilt tan α = μ_H.'},
             sprich='Die Haftreibungszahl ist My H gleich null Komma zwei fünf. Bis zu welchem Neigungswinkel haftet ein Körper?',
             rueck_sprich={0: 'Das ist mit dem Arcussinus. An der Grenze gilt Tangens Alpha gleich My H.', 1: 'Das ist mit dem Arcuskosinus. An der Grenze gilt Tangens Alpha gleich My H.'}),
        wahl('Frage 5', 'Man legt eine doppelt so schwere Kiste aus demselben Material auf die Rampe. Was geschieht mit dem Grenzwinkel?',
             ['er bleibt gleich', 'er halbiert sich', 'er verdoppelt sich'], 0,
             {1: 'Mit der Masse wächst auch die Normalkraft — und damit die Haftreibung.', 2: 'Mit der Masse wächst auch der Hangabtrieb.'}),
    ]))

DREH.append(dict(KOPF, titel='Statik sehen: Kontrollfragen zum Drehmoment', dateiname='p4-4-lp-kontrolle-drehmoment',
    kurzbeschrieb='Fünf Fragen zum Drehmoment einer senkrechten Kraft, zur Kraft durch die Achse, zur Einheit, zur Kraft aus Moment und Hebelarm und zu einer Anwendung.',
    schlagworte=['Drehmoment', 'Hebelarm', 'Kontrollfragen'], _probe=KTRL % 4,
    szenen=[
        sz('Frage 1', 'Kraft mal Hebelarm: fünfzig Newton mal null Komma drei Meter, fünfzehn Newtonmeter.',
           formel(r'M = 50\;\text{N} \cdot 0.3\;\text{m} = 15\;\text{Nm}', ein=1.0)),
        sz('Frage 2', 'Geht die Wirkungslinie durch die Achse, ist der Hebelarm null. Es gibt kein Drehmoment.',
           formel(r'r = 0 \;\Rightarrow\; M = 0', ein=1.0)),
        sz('Frage 3', 'Kraft in Newton mal Hebelarm in Meter: Newtonmeter.',
           notiz('N · m = Nm', y=320, ein=1.0, g=56)),
        sz('Frage 4', 'Umgestellt: Kraft gleich Moment durch Hebelarm. Vierundzwanzig Newtonmeter durch null Komma vier Meter, sechzig Newton.',
           formel(r'F = \frac{M}{r} = \frac{24\;\text{Nm}}{0.4\;\text{m}} = 60\;\text{N}', ein=1.0)),
        sz('Frage 5', 'Das Radkreuz hat lange Arme: grosser Hebelarm, kleine Kraft für das nötige Drehmoment.',
           notiz('langer Arm:|kleine Kraft', y=320, ein=1.0, g=50)),
    ],
    fragen=[
        wahl('Frage 1', '50 N greifen senkrecht an einem Hebel an, 0.3 m von der Drehachse. Wie gross ist das Drehmoment?',
             ['15 Nm', '167 Nm', '50 Nm'], 0,
             {1: 'Geteilt? Drehmoment ist Kraft mal Hebelarm.', 2: 'Das ist nur die Kraft. Der Abstand zählt mit.'},
             sprich='Fünfzig Newton greifen senkrecht an einem Hebel an, null Komma drei Meter von der Drehachse. Wie gross ist das Drehmoment?'),
        wahl('Frage 2', 'Eine Kraft zeigt genau auf die Drehachse. Wie gross ist ihr Drehmoment?',
             ['so gross wie F · l', 'null', 'halb so gross wie F · l'], 1,
             {0: 'Wie gross ist der senkrechte Abstand der Wirkungslinie von der Achse?', 2: 'Wie gross ist der senkrechte Abstand der Wirkungslinie von der Achse?'}),
        wahl('Frage 3', 'Welche Einheit hat das Drehmoment?',
             ['N/m', 'kg · m', 'Nm'], 2,
             {0: 'Kraft und Hebelarm werden multipliziert, nicht geteilt.', 1: 'Es ist eine Kraft im Spiel, keine Masse.'},
             sprich='Welche Einheit hat das Drehmoment?',
             rueck_sprich={0: 'Kraft und Hebelarm werden multipliziert, nicht geteilt.', 1: 'Es ist eine Kraft im Spiel, keine Masse.'}),
        wahl('Frage 4', 'Eine Schraube braucht 24 Nm. Du ziehst senkrecht, 0.4 m von der Achse. Welche Kraft braucht es?',
             ['9.6 N', '60 N', '24 N'], 1,
             {0: 'Mal gerechnet? Umstellen: F = M / r.', 2: 'Das ist das Moment, nicht die Kraft.'},
             sprich='Eine Schraube braucht vierundzwanzig Newtonmeter. Du ziehst senkrecht, null Komma vier Meter von der Achse. Welche Kraft braucht es?'),
        wahl('Frage 5', 'Wo nutzt man einen langen Hebelarm, um mit kleiner Kraft ein grosses Drehmoment zu erzeugen?',
             ['beim Radkreuz für den Radwechsel', 'bei der Pinzette', 'beim Kugelschreiber'], 0,
             {1: 'Die Pinzette dreht nichts fest. Wo muss man eine Mutter lösen?', 2: 'Beim Kugelschreiber dreht nichts gegen einen Widerstand.'}),
    ]))

DREH.append(dict(KOPF, titel='Statik sehen: Kontrollfragen zum Hebelgesetz', dateiname='p4-4-lp-kontrolle-hebel',
    kurzbeschrieb='Fünf Fragen zur Wippe im Gleichgewicht, zum Kippen bei gleichen Massen, zur Brechstange, zum Gewicht des Bretts und zu zwei Kindern auf einer Seite.',
    schlagworte=['Hebelgesetz', 'Wippe', 'Kontrollfragen'], _probe=KTRL % 5,
    szenen=[
        sz('Frage 1', 'Hebelgesetz: zwanzig mal zwei gleich fünfzig mal r. Null Komma acht Meter, näher an der Achse.',
           formel(r'r = \frac{20\;\text{kg} \cdot 2\;\text{m}}{50\;\text{kg}} = 0.8\;\text{m}', ein=1.0)),
        sz('Frage 2', 'Gleiche Kraft, grösserer Hebelarm: grösseres Drehmoment. Die Wippe kippt zum Kind weiter aussen.',
           notiz('weiter aussen:|grösseres Moment', y=320, ein=1.0, g=50)),
        sz('Frage 3', 'Fünfmal so langer Kraftarm, ein Fünftel der Kraft.',
           formel(r'F = \frac{F_L \cdot r_L}{r_K} = \frac{F_L}{5}', ein=1.0)),
        sz('Frage 4', 'Das Gewicht des Bretts greift im Drehpunkt an. Ohne Hebelarm hat es kein Drehmoment.',
           notiz('Hebelarm null:|kein Moment', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Links zwei Momente: zwanzig mal eins plus zehn mal zwei, vierzig Kilogramm mal Meter. Rechts vierzig Kilogramm: ein Meter.',
           formel(r'20 \cdot 1 + 10 \cdot 2 = 40 \cdot r \;\Rightarrow\; r = 1\;\text{m}', g=46, ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Kind (20 kg) sitzt 2 m von der Achse. Wo muss eine Person mit 50 kg sitzen?',
             ['5 m', '0.8 m', '1.25 m'], 1,
             {0: 'Umgekehrt: Die schwerere Person sitzt näher an der Achse.', 2: 'Masse mal Abstand muss auf beiden Seiten gleich sein. Nachrechnen.'},
             sprich='Ein Kind mit zwanzig Kilogramm sitzt zwei Meter von der Achse. Wo muss eine Person mit fünfzig Kilogramm sitzen?'),
        wahl('Frage 2', 'Zwei gleich schwere Kinder sitzen auf einer Wippe, eines weiter aussen. Was geschieht?',
             ['Die Wippe bleibt waagrecht.', 'Sie kippt zum Kind weiter innen.', 'Sie kippt zum Kind weiter aussen.'], 2,
             {0: 'Gleiche Kraft — aber gleicher Hebelarm?', 1: 'Welches Kind hat den grösseren Hebelarm?'}),
        wahl('Frage 3', 'An einer Brechstange ist der Kraftarm fünfmal so lang wie der Lastarm. Welche Kraft braucht es?',
             ['ein Fünftel der Last', 'die Last', 'fünfmal die Last'], 0,
             {1: 'Wozu dann die Stange? Kraft mal Kraftarm gleich Last mal Lastarm.', 2: 'Umgekehrt: Der lange Arm spart Kraft.'}),
        wahl('Frage 4', 'Das Brett einer symmetrischen Wippe wiegt 200 N. Wie viel trägt es zum Gleichgewicht der Momente bei?',
             ['nichts', '100 N auf jeder Seite', '200 N auf der schwereren Seite'], 0,
             {1: 'Wo greift das Gewicht des Bretts an — und wie gross ist dort der Hebelarm?', 2: 'Wo greift das Gewicht des Bretts an — und wie gross ist dort der Hebelarm?'},
             sprich='Das Brett einer symmetrischen Wippe wiegt zweihundert Newton. Wie viel trägt es zum Gleichgewicht der Momente bei?',
             rueck_sprich={1: 'Wo greift das Gewicht des Bretts an, und wie gross ist dort der Hebelarm?', 2: 'Wo greift das Gewicht des Bretts an, und wie gross ist dort der Hebelarm?'}),
        wahl('Frage 5', 'Links sitzen 20 kg bei 1 m und 10 kg bei 2 m. Wo muss rechts eine Person mit 40 kg sitzen?',
             ['0.5 m', '1 m', '1.125 m'], 1,
             {0: 'Das zweite Kind links dreht auch mit.', 2: 'Jedes Kind mit seinem eigenen Abstand: 20 · 1 + 10 · 2.'},
             sprich='Links sitzen zwanzig Kilogramm bei einem Meter und zehn Kilogramm bei zwei Metern. Wo muss rechts eine Person mit vierzig Kilogramm sitzen?',
             rueck_sprich={0: 'Das zweite Kind links dreht auch mit.', 2: 'Jedes Kind mit seinem eigenen Abstand: zwanzig mal eins plus zehn mal zwei.'}),
    ]))

DREH.append(dict(KOPF, titel='Statik sehen: Kontrollfragen zum statischen Gleichgewicht', dateiname='p4-4-lp-kontrolle-auflager',
    kurzbeschrieb='Fünf Fragen zu Auflagerkräften, zum Wagen auf der Brücke, zur Last über einer Stütze, zur Wahl der Drehachse und zum Eigengewicht.',
    schlagworte=['Auflagerkraft', 'statisches Gleichgewicht', 'Kontrollfragen'], _probe=KTRL % 6,
    szenen=[
        sz('Frage 1', 'Momente um A: F B mal acht Meter gleich vierhundert Newton mal zwei Meter, F B hundert Newton. Dann F A gleich vierhundert minus hundert, dreihundert Newton.',
           formel(r'F_B = \frac{400\;\text{N} \cdot 2\;\text{m}}{8\;\text{m}} = 100\;\text{N}', ein=1.0),
           formel(r'F_A = 300\;\text{N}', y=420, ein=6.0)),
        sz('Frage 2', 'Fährt der Wagen zu B, wandert die Last zu B: F A nimmt ab, F B nimmt zu, die Summe bleibt.',
           formel(r'F_A \downarrow \quad F_B \uparrow \quad \text{Summe bleibt}', y=320, ein=1.0, g=50)),
        sz('Frage 3', 'Steht die Last genau über B, hat sie um B keinen Hebelarm. A trägt nichts.',
           formel(r'F_A = 0', ein=1.0)),
        sz('Frage 4', 'Legt man die Drehachse in A, hat F A den Hebelarm null und fällt aus der Momentengleichung heraus.',
           formel(r'\text{Achse in A: } F_A \text{ fällt heraus}', y=320, ein=1.0, g=50)),
        sz('Frage 5', 'Das Eigengewicht greift in der Mitte an: Jede Stütze trägt die Hälfte, zehn Kilonewton.',
           formel(r'F_A = F_B = \frac{20\;\text{kN}}{2} = 10\;\text{kN}', ein=1.0)),
    ],
    fragen=[
        wahl('Frage 1', 'Ein Balken (8 m, ohne Eigengewicht) liegt auf A und B. Eine Last von 400 N steht 2 m von A. Wie gross ist F_A?',
             ['100 N', '200 N', '300 N'], 2,
             {0: 'Das ist F_B. Die nähere Stütze trägt mehr.', 1: 'Halb und halb gilt nur in der Mitte.'},
             sprich='Ein Balken von acht Metern ohne Eigengewicht liegt auf A und B. Eine Last von vierhundert Newton steht zwei Meter von A. Wie gross ist F A?',
             rueck_sprich={0: 'Das ist F B. Die nähere Stütze trägt mehr.'}),
        wahl('Frage 2', 'Ein Wagen fährt über eine Brücke von A nach B. Was geschieht mit den Auflagerkräften?',
             ['beide bleiben gleich', 'F_A nimmt ab, F_B nimmt zu', 'beide nehmen zu'], 1,
             {0: 'Welche Stütze ist dem Wagen jeweils näher?', 2: 'Zusammen tragen sie immer die ganze Last.'},
             rueck_sprich={0: 'Welche Stütze ist dem Wagen jeweils näher?'}),
        wahl('Frage 3', 'Eine Last steht genau über der Stütze B. Wie gross ist F_A?',
             ['null', 'die halbe Last', 'die ganze Last'], 0,
             {1: 'Halb und halb gilt in der Mitte. Wo steht die Last?', 2: 'Über welcher Stütze steht die Last?'}),
        wahl('Frage 4', 'Warum legt man die Drehachse für die Momente in die Stütze A?',
             ['weil A immer mehr trägt', 'weil F_A dort keinen Hebelarm hat und herausfällt', 'weil man sie dort legen muss'], 1,
             {0: 'Das hängt davon ab, wo die Last steht.', 2: 'Die Drehachse darf man frei wählen. Warum gerade dort?'}),
        wahl('Frage 5', 'Eine leere Brücke mit 20 kN Eigengewicht liegt auf zwei Stützen. Wie viel trägt jede?',
             ['10 kN', '20 kN', '5 kN'], 0,
             {1: 'Dann trügen beide zusammen 40 kN.', 2: 'Zusammen tragen sie die ganze Last.'},
             sprich='Eine leere Brücke mit zwanzig Kilonewton Eigengewicht liegt auf zwei Stützen. Wie viel trägt jede?',
             rueck_sprich={1: 'Dann trügen beide zusammen vierzig Kilonewton.'}),
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
