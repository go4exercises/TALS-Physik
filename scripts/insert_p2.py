#!/usr/bin/env python3
# Phase-2-Politur: Lernziele (#18), Kernpunkte (#19), Verstaendnisfragen (#16)
# Einfuegung an stabilen Ankern. Idempotent: ueberspringt bereits eingefuegte Bloecke.
import pathlib, sys

BASE = pathlib.Path(__file__).resolve().parent.parent / "themen"

def lernziele(items):
    lis = "\n".join(f"      <li>{x}</li>" for x in items)
    return ('<details class="lernziele">\n'
            '  <summary>\U0001F3AF Lernziele — das kann ich nach dieser Seite</summary>\n'
            '  <div class="lz-body">\n'
            '    <ul>\n' + lis + '\n'
            '    </ul>\n'
            '  </div>\n'
            '</details>')

def kernpunkte(items):
    lis = "\n".join(f"  <li>{x}</li>" for x in items)
    return ('<h3>Kernpunkte</h3>\n'
            '<ul class="kernpunkte">\n' + lis + '\n</ul>')

def frage(q, a):
    return ('<details class="frage">\n'
            f'  <summary>\u2753 {q}</summary>\n'
            '  <div class="frage-antwort">\n'
            f'    <p>{a}</p>\n'
            '  </div>\n'
            '</details>')

# ---- Inhalte pro Seite ----
PAGES = {
"p4-1-kinematik.html": {
  "lz": ["Ich kann Schwerpunkt, Bahnkurve, Geschwindigkeit und Beschleunigung in eigenen Worten erklaeren und unterscheiden.",
         "Ich kann die Geschwindigkeit als Vektor darstellen und damit Relativbewegungen berechnen.",
         "Ich kann Aufgaben zur gleichfoermigen und zur gleichmaessig beschleunigten Bewegung loesen.",
         "Ich kann den freien Fall und den Wurf mit den Bewegungsgleichungen beschreiben.",
         "Ich kann bei der Kreisbewegung Rotationsfrequenz, Winkelgeschwindigkeit und Zentripetalbeschleunigung bestimmen."],
  "kp": ["Geschwindigkeit ist Weg pro Zeit, Beschleunigung ist Geschwindigkeitsaenderung pro Zeit — beide sind Vektoren.",
         "Gleichfoermig: \\(v=\\text{const.}\\), \\(s=s_0+v\\cdot t\\). Gleichmaessig beschleunigt: \\(v=v_0+a\\cdot t\\), \\(s=s_0+v_0 t+\\tfrac12 a t^2\\).",
         "Der freie Fall ist eine gleichmaessig beschleunigte Bewegung mit \\(g\\approx 9.81\\;\\text{m/s}^2\\) — unabhaengig von der Masse.",
         "Der waagrechte Wurf setzt sich aus gleichfoermiger Horizontal- und beschleunigter Vertikalbewegung zusammen.",
         "Bei der gleichfoermigen Kreisbewegung bleibt der Betrag von \\(v\\) konstant, die Richtung aendert sich staendig.",
         "Die Zentripetalbeschleunigung \\(a_z=v^2/r\\) zeigt immer zur Kreismitte.",
         "Relativbewegungen werden durch vektorielle Addition der Geschwindigkeiten beschrieben."],
  "fragen": [("theorie", "Was passiert mit dem Bremsweg, wenn du die Geschwindigkeit verdoppelst?",
              "Der Bremsweg waechst <strong>quadratisch</strong> mit der Geschwindigkeit (\\(s\\propto v^2\\)). Doppelte Geschwindigkeit bedeutet bei gleicher Bremsverzoegerung den <strong>vierfachen</strong> Bremsweg — der Hauptgrund fuer Tempolimits."),
             ("aufgaben", "Was passiert beim freien Fall, wenn du die Masse des Koerpers verdoppelst?",
              "Nichts an der Bewegung: im freien Fall (ohne Luftwiderstand) fallen alle Koerper gleich schnell, weil \\(g\\) massenunabhaengig ist. Eine Feder und eine Bleikugel landen im Vakuum gleichzeitig.")],
},
"p4-2-dynamik.html": {
  "lz": ["Ich kann die drei Newtonschen Gesetze formulieren und an Beispielen erklaeren.",
         "Ich kann das Grundgesetz \\(F=m\\cdot a\\) auf konkrete Bewegungen anwenden.",
         "Ich kann die Federkraft mit dem Hookeschen Gesetz \\(F=D\\cdot s\\) berechnen.",
         "Ich kann Haft- und Gleitreibung unterscheiden und Reibungskraefte berechnen.",
         "Ich kann die Kraefte an der schiefen Ebene zerlegen und die Beschleunigung bestimmen."],
  "kp": ["1. Newton (Traegheit): ohne resultierende Kraft bleibt der Bewegungszustand erhalten.",
         "2. Newton (Grundgesetz): \\(\\vec{F}_{\\text{ges}}=m\\cdot\\vec{a}\\) — Kraft und Beschleunigung sind gleichgerichtet.",
         "3. Newton (Wechselwirkung): Kraft und Gegenkraft sind gleich gross, entgegengesetzt und greifen an <em>verschiedenen</em> Koerpern an.",
         "Federkraft: \\(F=D\\cdot s\\), proportional zur Auslenkung.",
         "Reibung: \\(F_R=\\mu\\cdot F_N\\); die Haftreibung ist meist groesser als die Gleitreibung.",
         "Schiefe Ebene: Hangabtrieb \\(F_H=mg\\sin\\alpha\\), Normalkraft \\(F_N=mg\\cos\\alpha\\).",
         "Die Beschleunigung am reibungsbehafteten Hang \\(a=g(\\sin\\alpha-\\mu\\cos\\alpha)\\) ist massenunabhaengig."],
  "fragen": [("reibung", "Was passiert, wenn ein Auto auf der Strasse von Haft- in Gleitreibung wechselt?",
              "Sobald die Reifen durchdrehen oder blockieren, wirkt nur noch die <strong>kleinere</strong> Gleitreibung. Der Wagen wird schlechter gebremst und schwerer lenkbar — deshalb verhindert das ABS das Blockieren der Raeder."),
             ("aufgaben", "Was passiert mit der Beschleunigung am Hang, wenn du die Masse verdoppelst?",
              "Sie bleibt gleich. In \\(a=g(\\sin\\alpha-\\mu\\cos\\alpha)\\) kuerzt sich die Masse heraus — eine schwere und eine leichte Kiste rutschen bei gleichem Winkel und Reibwert gleich schnell.")],
},
"p4-3-energie.html": {
  "lz": ["Ich kann die mechanische Arbeit \\(W=F\\cdot s\\cdot\\cos\\alpha\\) berechnen.",
         "Ich kann die Leistung \\(P=W/t\\) bestimmen und in Watt angeben.",
         "Ich kann kinetische und potentielle Energie berechnen.",
         "Ich kann den Energieerhaltungssatz auf mechanische Vorgaenge anwenden.",
         "Ich kann den Wirkungsgrad als Verhaeltnis von Nutz- zu zugefuehrter Energie bestimmen."],
  "kp": ["Arbeit ist uebertragene Energie: \\(W=F\\cdot s\\cdot\\cos\\alpha\\) — nur der Kraftanteil laengs des Weges zaehlt.",
         "Potentielle Energie: \\(E_{\\text{pot}}=mgh\\); kinetische Energie: \\(E_{\\text{kin}}=\\tfrac12 m v^2\\).",
         "Energieerhaltung: ohne Reibung bleibt \\(E_{\\text{kin}}+E_{\\text{pot}}\\) konstant.",
         "Aus der Hoehe folgt die Endgeschwindigkeit \\(v=\\sqrt{2gh}\\) — massenunabhaengig.",
         "Leistung ist Energie pro Zeit: \\(P=W/t=F\\cdot v\\), Einheit Watt.",
         "Reibung wandelt mechanische Energie in Waerme um — sie geht nicht verloren, ist aber nicht mehr nutzbar.",
         "Der Wirkungsgrad \\(\\eta=E_{\\text{nutz}}/E_{\\text{zu}}\\) ist immer kleiner als 1; bei mehreren Stufen multiplizieren sich die Wirkungsgrade."],
  "fragen": [("erhaltung", "Was passiert mit der Energie, wenn ein Pendel durch Reibung langsamer wird?",
              "Sie verschwindet nicht — die mechanische Energie wird nach und nach in <strong>Waerme</strong> (und etwas Schall) umgewandelt. Die Gesamtenergie bleibt erhalten, nur ist sie am Ende nicht mehr als Bewegung nutzbar."),
             ("aufgaben", "Was passiert mit der kinetischen Energie, wenn du die Geschwindigkeit verdreifachst?",
              "Sie wird <strong>neunmal</strong> so gross, denn \\(E_{\\text{kin}}\\propto v^2\\). Das erklaert, warum Aufprallenergien bei hohem Tempo so dramatisch steigen.")],
},
"p4-4-statik.html": {
  "lz": ["Ich kann den Begriff Kraft definieren und Kraefte als Vektoren darstellen.",
         "Ich kann das Drehmoment \\(M=F\\cdot r\\) berechnen und Anwendungen nennen.",
         "Ich kann die wesentlichen Kraefte am Festkoerper aufzaehlen und charakterisieren.",
         "Ich kann mehrere Kraefte grafisch und rechnerisch zur Resultierenden zusammensetzen.",
         "Ich kann das Kraefte- und das Momentengleichgewicht auf waagrechter und schiefer Ebene anwenden."],
  "kp": ["Eine Kraft hat Betrag, Richtung und Angriffspunkt — sie ist ein Vektor.",
         "Kraefte werden in Komponenten zerlegt: \\(F_x=F\\cos\\varphi\\), \\(F_y=F\\sin\\varphi\\).",
         "Mehrere Kraefte fasst man zur Resultierenden \\(\\vec{F}_R=\\sum\\vec{F}_i\\) zusammen.",
         "Drehmoment: \\(M=F\\cdot r\\) — Drehwirkung aus Kraft und senkrechtem Hebelarm.",
         "Hebelgesetz: \\(F_1 r_1=F_2 r_2\\).",
         "Statisches Gleichgewicht: \\(\\sum F_x=0\\), \\(\\sum F_y=0\\) <em>und</em> \\(\\sum M=0\\).",
         "Auf der schiefen Ebene haelt ein Koerper, solange \\(\\tan\\alpha\\le\\mu_H\\)."],
  "fragen": [("drehmoment", "Was passiert mit der noetigen Kraft, wenn du beim Schraubenschluessel den Hebelarm verdoppelst?",
              "Sie halbiert sich. Da \\(M=F\\cdot r\\) und das benoetigte Drehmoment gleich bleibt, kommst du mit einem laengeren Schluessel mit der halben Kraft aus — das Prinzip jeder Hebelverlaengerung."),
             ("aufgaben", "Was passiert mit einem Koerper, wenn die Summe aller Kraefte null ist, die Summe der Momente aber nicht?",
              "Er beschleunigt nicht in seinem Schwerpunkt, beginnt aber zu <strong>drehen</strong>. Fuer vollstaendiges Gleichgewicht muessen sowohl die Kraftsumme als auch die Momentensumme verschwinden.")],
},
"p4-5-hydrostatik.html": {
  "lz": ["Ich kann den Begriff Druck definieren und die Einheit Pascal einsetzen.",
         "Ich kann den Schweredruck \\(p_S=\\rho g h\\) berechnen und das hydrostatische Paradoxon erklaeren.",
         "Ich kann das Prinzip von Pascal auf hydraulische Anlagen anwenden.",
         "Ich kann das archimedische Prinzip formulieren und Auftriebskraefte berechnen.",
         "Ich kann aus dem Dichtevergleich entscheiden, ob ein Koerper schwimmt, schwebt oder sinkt."],
  "kp": ["Druck ist Kraft pro Flaeche: \\(p=F/A\\), Einheit Pascal (Pa = N/m\\(^2\\)).",
         "Der Schweredruck \\(p_S=\\rho g h\\) waechst linear mit der Tiefe.",
         "Hydrostatisches Paradoxon: der Bodendruck haengt nur von der Fuellhoehe ab, nicht von der Gefaessform.",
         "Pascal-Prinzip: ein Druck breitet sich allseitig aus — Grundlage der hydraulischen Presse \\(F_2=F_1 A_2/A_1\\).",
         "Auftrieb \\(F_A=\\rho_{\\text{Fl}}V_e g\\) entspricht dem Gewicht der verdraengten Fluessigkeit.",
         "Schwimmen, Schweben oder Sinken entscheidet allein der Dichtevergleich Koerper/Fluessigkeit.",
         "Ein schwimmender Koerper taucht zum Anteil \\(\\rho_K/\\rho_{\\text{Fl}}\\) ein."],
  "fragen": [("auftrieb", "Was passiert mit dem Wasserstand im Glas, wenn ein schwimmender Eiswuerfel schmilzt?",
              "Der Pegel bleibt praktisch gleich. Der Eiswuerfel verdraengt schwimmend genau das Wasservolumen, das seinem Gewicht entspricht — und liefert beim Schmelzen genau diese Wassermenge nach."),
             ("aufgaben", "Was passiert mit dem Schweredruck am Beckenboden, wenn das Becken doppelt so breit ist, aber gleich tief?",
              "Er bleibt unveraendert. \\(p_S=\\rho g h\\) haengt nur von der <strong>Tiefe</strong> ab, nicht von der Flaeche oder Wassermenge — das ist der Kern des hydrostatischen Paradoxons.")],
},
"p5-1-temperatur.html": {
  "lz": ["Ich kann Temperatur ueber die Teilchenbewegung definieren.",
         "Ich kann den Zusammenhang zwischen Temperatur und Aggregatzustand beschreiben.",
         "Ich kann Ursprung und Anwendung der Celsius- und der Kelvin-Skala erklaeren.",
         "Ich kann Grad Celsius in Kelvin umrechnen und umgekehrt.",
         "Ich kann erklaeren, warum es einen absoluten Nullpunkt gibt."],
  "kp": ["Temperatur ist ein Mass fuer die mittlere Bewegungsenergie der Teilchen.",
         "Mit steigender Temperatur bewegen sich die Teilchen heftiger — das fuehrt zu den Aggregatzustaenden fest, fluessig, gasfoermig.",
         "Die Celsius-Skala nutzt die Fixpunkte des Wassers (\\(0\\,^\\circ\\text{C}\\) / \\(100\\,^\\circ\\text{C}\\)).",
         "Der absolute Nullpunkt liegt bei \\(-273.15\\,^\\circ\\text{C}\\) und ist nie ganz erreichbar.",
         "Die Kelvin-Skala beginnt am absoluten Nullpunkt; die Schrittweite ist gleich wie bei Celsius.",
         "Umrechnung: \\(T=\\vartheta+273.15\\); Temperaturdifferenzen sind in K und \\(^\\circ\\)C identisch."],
  "fragen": [("skalen", "Was passiert mit einem Temperaturunterschied von 10 °C, wenn du ihn in Kelvin angibst?",
              "Er bleibt 10 K. Celsius und Kelvin haben dieselbe Schrittweite, daher gilt \\(\\Delta T=\\Delta\\vartheta\\). Nur bei <em>absoluten</em> Temperaturen muss man \\(+273.15\\) addieren, bei Differenzen nicht."),
             ("aufgaben", "Was passiert mit der Teilchenbewegung, wenn man sich dem absoluten Nullpunkt naehert?",
              "Sie wird immer geringer und erreicht am absoluten Nullpunkt ein Minimum. Tiefer geht es nicht, weil es keine negative Bewegungsenergie gibt — deshalb ist \\(0\\;\\text{K}\\) die untere Grenze.")],
},
"p5-2-waerme.html": {
  "lz": ["Ich kann Waerme als Energieuebertragung wegen eines Temperaturunterschieds definieren.",
         "Ich kann die Waermemenge \\(Q=m c\\Delta T\\) und Waermebilanzen berechnen.",
         "Ich kann mit spezifischer Waermekapazitaet, latenter Waerme und Wirkungsgrad rechnen.",
         "Ich kann den Temperaturverlauf einer Heizkurve grafisch darstellen.",
         "Ich kann die drei Formen des Waermetransports unterscheiden und den Treibhaus-Effekt beschreiben."],
  "kp": ["Waerme \\(Q\\) ist eine Prozessgroesse: Energie, die wegen eines Temperaturunterschieds uebertragen wird.",
         "Ein Koerper speichert innere Energie, nicht Waerme.",
         "Waermemenge: \\(Q=m c\\Delta T\\), mit der spezifischen Waermekapazitaet \\(c\\).",
         "In einem abgeschlossenen System gilt die Waermebilanz \\(\\sum Q_i=0\\) (Mischtemperatur).",
         "Beim Schmelzen und Verdampfen bleibt die Temperatur konstant — die latente Waerme \\(Q=mL\\) wird verbraucht.",
         "Waerme wird durch Leitung, Konvektion und Strahlung uebertragen.",
         "Der Treibhaus-Effekt beruht auf der wellenlaengenabhaengigen Absorption der Atmosphaere."],
  "fragen": [("mischung", "Was passiert mit der Mischtemperatur, wenn du wenig heisses Wasser mit viel kaltem mischst?",
              "Die Mischtemperatur liegt naeher beim kalten Wasser. In der Bilanz \\(\\sum Q_i=0\\) zieht die groessere Masse die gemeinsame Temperatur staerker zu sich — Masse und \\(\\Delta T\\) gleichen sich aus."),
             ("aufgaben", "Was passiert mit der Temperatur, waehrend Eis bei 0 °C schmilzt?",
              "Sie bleibt bei \\(0\\,^\\circ\\text{C}\\) konstant. Die zugefuehrte Energie wird als <strong>latente Waerme</strong> zum Aufbrechen der Bindungen gebraucht; erst wenn alles geschmolzen ist, steigt die Temperatur weiter.")],
},
"p5-3-waermeausdehnung.html": {
  "lz": ["Ich kann die lineare Waermeausdehnung \\(\\Delta l=\\alpha l_0\\Delta T\\) berechnen.",
         "Ich kann die Volumenausdehnung von Festkoerpern, Fluessigkeiten und Gasen quantifizieren.",
         "Ich kann die Anomalie des Wassers erklaeren und ihre Folgen nennen.",
         "Ich kann mit dem Modell des idealen Gases Druck-, Volumen- und Temperaturaenderungen berechnen.",
         "Ich kann Anwendungen wie Dehnungsfugen und den Meeresspiegelanstieg einordnen."],
  "kp": ["Festkoerper dehnen sich beim Erwaermen aus: \\(\\Delta l=\\alpha l_0\\Delta T\\).",
         "Die Volumenausdehnung folgt \\(\\Delta V=\\gamma V_0\\Delta T\\); bei Festkoerpern gilt \\(\\gamma\\approx 3\\alpha\\).",
         "Fluessigkeiten und Gase dehnen sich staerker aus als Festkoerper.",
         "Bei Erwaermung sinkt die Dichte: \\(\\rho=\\rho_0/(1+\\gamma\\Delta T)\\).",
         "Wasseranomalie: groesste Dichte bei \\(4\\,^\\circ\\text{C}\\) — Seen frieren von oben zu.",
         "Ideales Gasgesetz: \\(pV/T=\\text{const}\\) (mit \\(T\\) in Kelvin und absolutem Druck).",
         "Dehnungsfugen in Schienen und Bruecken fangen die Laengenausdehnung auf."],
  "fragen": [("anomalie", "Was passiert in einem See im Winter, weil Wasser bei 4 °C am dichtesten ist?",
              "Das dichteste Wasser (\\(4\\,^\\circ\\text{C}\\)) sammelt sich am Grund, kaelteres und schliesslich Eis bleiben oben. So friert ein See von oben zu und Fische ueberleben am Grund — eine direkte Folge der Wasseranomalie."),
             ("aufgaben", "Was passiert mit dem Druck in einem geschlossenen Gasbehaelter, wenn du die absolute Temperatur verdoppelst?",
              "Der Druck verdoppelt sich (bei konstantem Volumen), denn \\(p/T=\\text{const}\\). Wichtig: \\(T\\) muss in <strong>Kelvin</strong> stehen — eine Verdopplung von \\(20\\,^\\circ\\text{C}\\) ist nicht \\(40\\,^\\circ\\text{C}\\), sondern von \\(293\\;\\text{K}\\) auf \\(586\\;\\text{K}\\).")],
},
"p6-1-wellen.html": {
  "lz": ["Ich kann Wellen mit Frequenz, Periode, Wellenlaenge und Phasengeschwindigkeit charakterisieren.",
         "Ich kann mechanische, Schall- und elektromagnetische Wellen unterscheiden.",
         "Ich kann die Wellenerzeugung am Beispiel mechanischer Wellen beschreiben.",
         "Ich kann die Besonderheiten elektromagnetischer Wellen (Spektrum, Geschwindigkeit, Emission, Absorption) erklaeren.",
         "Ich kann den Treibhaus-Effekt ueber die wellenlaengenabhaengige Absorption beschreiben."],
  "kp": ["Eine Welle transportiert Energie, aber keine Materie.",
         "Grundgroessen: Frequenz \\(f=1/T\\), Wellenlaenge \\(\\lambda\\), Geschwindigkeit \\(c=\\lambda f\\).",
         "Transversalwellen schwingen quer, Longitudinalwellen laengs zur Ausbreitungsrichtung.",
         "Mechanische Wellen (Schall, Wasser, Erdbeben) brauchen ein Medium.",
         "Elektromagnetische Wellen brauchen kein Medium und sind im Vakuum gleich schnell: \\(c\\approx 3\\cdot10^{8}\\;\\text{m/s}\\).",
         "Sichtbares Licht ist nur ein kleiner Ausschnitt (\\(380\\!-\\!780\\;\\text{nm}\\)) des Spektrums.",
         "Die Ausbreitungsgeschwindigkeit haengt vom Wellentyp und den Eigenschaften des Mediums ab."],
  "fragen": [("typen", "Was passiert mit dem Schall, wenn man die Luft aus einem Glas mit klingelndem Wecker abpumpt?",
              "Der Ton wird immer leiser und verstummt schliesslich. Schall ist eine <strong>mechanische</strong> Welle und braucht ein Medium — im Vakuum kann er sich nicht ausbreiten. Licht aus dem Glas sieht man dagegen weiter."),
             ("aufgaben", "Was passiert mit der Wellenlaenge, wenn bei gleicher Geschwindigkeit die Frequenz steigt?",
              "Die Wellenlaenge wird kleiner. Aus \\(c=\\lambda f\\) folgt bei konstantem \\(c\\): \\(\\lambda=c/f\\) — hoehere Frequenz, kuerzere Wellenlaenge. Hohe Toene haben kuerzere Wellenlaengen als tiefe.")],
},
"p6-2-elektrizitaet.html": {
  "lz": ["Ich kann die Beschaffenheit elektrischer Ladung beschreiben (Ursprung, Einheit, Elementarladung).",
         "Ich kann Ladung, Spannung, Stromstaerke, Energie und Leistung definieren.",
         "Ich kann den Widerstand eines Leiters mit \\(R=\\rho l/A\\) berechnen.",
         "Ich kann Berechnungen in einfachen Reihen- und Parallelschaltungen durchfuehren.",
         "Ich kann die Gefahren des elektrischen Stroms und passende Schutzmassnahmen nennen."],
  "kp": ["Ladung tritt nur als Vielfaches der Elementarladung \\(e=1.602\\cdot10^{-19}\\;\\text{C}\\) auf; \\(Q=I\\cdot t\\).",
         "Stromstaerke ist Ladung pro Zeit (\\(I=Q/t\\)), Spannung ist Energie pro Ladung.",
         "Ohmsches Gesetz: \\(U=R\\cdot I\\).",
         "Leiterwiderstand: \\(R=\\rho l/A\\) — abhaengig von Material und Geometrie.",
         "Reihenschaltung: gleicher Strom, Widerstaende addieren sich, Spannung teilt sich.",
         "Parallelschaltung: gleiche Spannung, Stroeme teilen sich, Gesamtwiderstand sinkt.",
         "Leistung \\(P=U\\cdot I\\); elektrische Energie wird in kWh abgerechnet.",
         "Gefaehrlich ist der <em>Strom durch den Koerper</em> — Schutz durch Isolation, Erdung und FI-Schalter."],
  "fragen": [("reihe", "Was passiert mit den restlichen Lampen einer Reihenschaltung, wenn eine Lampe durchbrennt?",
              "Alle gehen aus. In der Reihenschaltung fliesst <strong>derselbe Strom</strong> durch alle Bauteile; eine Unterbrechung trennt den ganzen Stromkreis — wie bei alten Lichterketten."),
             ("aufgaben", "Was passiert mit dem Gesamtwiderstand, wenn du einen zweiten gleichen Widerstand parallel schaltest?",
              "Er halbiert sich. Bei zwei gleichen Parallelwiderstaenden gilt \\(R_{\\text{ges}}=R/2\\); der Gesamtwiderstand ist immer kleiner als der kleinste Einzelwiderstand, weil dem Strom mehr Wege offenstehen.")],
},
}

def apply(fname, data):
    path = BASE / fname
    txt = path.read_text(encoding="utf-8")
    n = 0
    # Lernziele vor Einstieg-h2
    anchor = '<h2 id="einstieg">'
    if 'class="lernziele"' not in txt and anchor in txt:
        txt = txt.replace(anchor, lernziele(data["lz"]) + "\n\n" + anchor, 1)
        n += 1
    # Kernpunkte vor merksatz
    manchor = '<div class="merksatz">'
    if 'class="kernpunkte"' not in txt and manchor in txt:
        txt = txt.replace(manchor, kernpunkte(data["kp"]) + "\n\n" + manchor, 1)
        n += 1
    # Verstaendnisfragen vor gewaehlten Sektionen
    for secid, q, a in data["fragen"]:
        secanchor = f'<h2 id="{secid}">'
        block = frage(q, a)
        if block not in txt and secanchor in txt:
            txt = txt.replace(secanchor, block + "\n\n" + secanchor, 1)
            n += 1
    path.write_text(txt, encoding="utf-8")
    return n

if __name__ == "__main__":
    total = 0
    for fname, data in PAGES.items():
        c = apply(fname, data)
        total += c
        print(f"{fname}: {c} Einfuegungen")
    print(f"Total: {total}")
