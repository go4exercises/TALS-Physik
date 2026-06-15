import sys
sys.path.insert(0, 'scripts')
from minicheck_lib import mc, lueck, rech, block, L, apply_page

p62 = [
 ('definition', block([
   mc(r"Was bewegt sich in einem metallischen Leiter beim Stromfluss?",
      [("A", r"Protonen"), ("B", r"freie Elektronen"), ("C", r"ganze Atome")],
      r"<strong>B.</strong> Im Metall tragen die frei beweglichen Elektronen den Strom."),
   lueck(r"Die elektrische Stromstärke gibt die " + L + r" pro Zeit an.",
      r"Ladung — \(I = Q/t\)."),
   rech(r"Durch einen Querschnitt fliesst die Ladung \(Q = 6\;\text{C}\) in \(t = 2\;\text{s}\). Stromstärke?",
      r"\(I = \dfrac{Q}{t} = \dfrac{6}{2} = 3\;\text{A}\)."),
 ],
  r"Warum leuchtet eine Lampe praktisch sofort, obwohl sich die einzelnen Elektronen nur langsam bewegen?",
  r"Das elektrische Feld breitet sich fast mit Lichtgeschwindigkeit aus und setzt alle Elektronen im Draht nahezu gleichzeitig in Bewegung. Es muss nicht erst ein Elektron zur Lampe wandern.")),
 ('ohm', block([
   mc(r"Die Einheit der elektrischen Spannung ist …",
      [("A", r"Ampere"), ("B", r"Volt"), ("C", r"Ohm")],
      r"<strong>B.</strong> Die Spannung wird in Volt (V) gemessen."),
   lueck(r"Die Stromstärke wird in " + L + r" gemessen.",
      r"Ampere (A)."),
   rech(r"Welche elektrische Grösse misst man in Ohm?",
      r"Den elektrischen Widerstand \(R\)."),
 ],
  r"Im Vergleich mit einem Wasserkreislauf: Was entspricht der elektrischen Spannung, was der Stromstärke?",
  r"Die Spannung entspricht dem Druckunterschied der Pumpe, die Stromstärke der pro Zeit durchfliessenden Wassermenge.")),
 ('leiter', block([
   mc(r"Verdoppelt man bei festem Widerstand die Spannung, so …",
      [("A", r"bleibt der Strom gleich"), ("B", r"verdoppelt sich der Strom"), ("C", r"halbiert sich der Strom")],
      r"<strong>B.</strong> \(I = U/R\) — bei festem \(R\) ist der Strom proportional zur Spannung."),
   lueck(r"Das Ohmsche Gesetz lautet \(U = R \cdot\) " + L + r".",
      r"\(I\)."),
   rech(r"An \(R = 200\;\Omega\) liegt \(U = 12\;\text{V}\). Stromstärke?",
      r"\(I = \dfrac{U}{R} = \dfrac{12}{200} = 0.06\;\text{A} = 60\;\text{mA}\)."),
 ],
  r"Eine Lampe (\(R = 240\;\Omega\)) hängt am \(230\;\text{V}\)-Netz. Welcher Strom fliesst (ohmsch gerechnet)?",
  r"\(I = \dfrac{U}{R} = \dfrac{230}{240} \approx 0.96\;\text{A}\).")),
 ('reihe', block([
   mc(r"Ein längerer Draht (gleiches Material, gleicher Querschnitt) hat …",
      [("A", r"einen kleineren Widerstand"), ("B", r"einen grösseren Widerstand"), ("C", r"den gleichen Widerstand")],
      r"<strong>B.</strong> \(R = \rho\,l/A\) — mit der Länge wächst der Widerstand."),
   lueck(r"Der Widerstand eines Leiters ist \(R = \rho \cdot l / \) " + L + r".",
      r"\(A\) (Querschnittsfläche)."),
   rech(r"Verdoppelt man den Querschnitt eines Drahtes, wie ändert sich \(R\)?",
      r"\(R\) halbiert sich: \(R \sim 1/A\)."),
 ],
  r"Warum verwendet man für lange Überlandleitungen dicke Kabel und sehr hohe Spannung?",
  r"Dicker Querschnitt senkt \(R = \rho\,l/A\). Hohe Spannung senkt bei gleicher Leistung (\(P = U I\)) den Strom; da die Verlustleistung \(P_V = R\,I^2\) mit kleinerem \(I\) stark sinkt, gibt es weniger Übertragungsverluste.")),
 ('parallel', block([
   mc(r"In einer Reihenschaltung ist … überall gleich.",
      [("A", r"die Spannung"), ("B", r"die Stromstärke"), ("C", r"der Widerstand")],
      r"<strong>B.</strong> In Reihe fliesst überall derselbe Strom; die Spannungen teilen sich auf."),
   lueck(r"In Reihe addieren sich die " + L + r".",
      r"Widerstände — \(R_{\text{ges}} = R_1 + R_2\)."),
   rech(r"Zwei Widerstände \(R_1 = 100\;\Omega\) und \(R_2 = 200\;\Omega\) in Reihe. Gesamtwiderstand?",
      r"\(R_{\text{ges}} = R_1 + R_2 = 300\;\Omega\)."),
 ],
  r"Bei einer alten Lichterkette in Reihe brennt eine Lampe durch — die ganze Kette bleibt dunkel. Warum?",
  r"In Reihe fliesst überall derselbe Strom. Eine durchgebrannte Lampe unterbricht den Stromkreis vollständig, sodass nirgends mehr Strom fliesst.")),
 ('leistung', block([
   mc(r"In einer Parallelschaltung ist … an allen Zweigen gleich.",
      [("A", r"die Stromstärke"), ("B", r"die Spannung"), ("C", r"der Widerstand")],
      r"<strong>B.</strong> Parallel liegt an jedem Zweig dieselbe Spannung an; die Ströme teilen sich auf."),
   lueck(r"Bei Parallelschaltung gilt \(\dfrac{1}{R_{\text{ges}}} = \dfrac{1}{R_1} + \) " + L + r".",
      r"\(\dfrac{1}{R_2}\)."),
   rech(r"Zwei gleiche Widerstände \(R = 100\;\Omega\) parallel. Gesamtwiderstand?",
      r"\(\dfrac{1}{R_{\text{ges}}} = \dfrac{1}{100} + \dfrac{1}{100} \Rightarrow R_{\text{ges}} = 50\;\Omega\)."),
 ],
  r"Warum sind die Steckdosen einer Wohnung parallel geschaltet und nicht in Reihe?",
  r"So liegt an jedem Gerät dieselbe Netzspannung (\(230\;\text{V}\)), und die Geräte arbeiten unabhängig. Ein ausgeschaltetes oder defektes Gerät unterbricht die anderen nicht.")),
 ('gefahren', block([
   mc(r"Die elektrische Leistung berechnet man als …",
      [("A", r"\(P = U/I\)"), ("B", r"\(P = U \cdot I\)"), ("C", r"\(P = U + I\)")],
      r"<strong>B.</strong> \(P = U \cdot I\) — Spannung mal Stromstärke."),
   lueck(r"Die elektrische Energie ist \(E = P \cdot\) " + L + r".",
      r"\(t\) (Zeit)."),
   rech(r"Ein Gerät zieht bei \(U = 230\;\text{V}\) einen Strom \(I = 2\;\text{A}\). Leistung?",
      r"\(P = U \cdot I = 230 \cdot 2 = 460\;\text{W}\)."),
 ],
  r"Ein \(2000\;\text{W}\)-Wasserkocher läuft \(5\;\text{min}\). Wie viel Energie in Kilowattstunden? (\(5\;\text{min} = \tfrac{1}{12}\;\text{h}\))",
  r"\(E = P \cdot t = 2\;\text{kW} \cdot \tfrac{1}{12}\;\text{h} \approx 0.17\;\text{kWh}\).")),
 ('aufgaben', block([
   mc(r"Für die Gefährlichkeit eines Stromschlags ist vor allem entscheidend …",
      [("A", r"die Spannung allein"), ("B", r"die Stromstärke durch den Körper und die Einwirkdauer"), ("C", r"die Farbe des Kabels")],
      r"<strong>B.</strong> Massgeblich sind die Stromstärke durch den Körper und wie lange sie einwirkt."),
   lueck(r"Gefährlich ist nicht die Spannung allein, sondern die " + L + r" durch den Körper.",
      r"Stromstärke."),
   rech(r"Bei \(230\;\text{V}\) und einem Körperwiderstand von \(1000\;\Omega\): welcher Strom fliesst etwa?",
      r"\(I = \dfrac{U}{R} = \dfrac{230}{1000} = 0.23\;\text{A} = 230\;\text{mA}\) — bereits lebensgefährlich."),
 ],
  r"Warum ist nasse Haut beim Stromschlag besonders gefährlich?",
  r"Feuchtigkeit senkt den Körperwiderstand stark. Nach \(I = U/R\) fliesst bei kleinerem \(R\) ein viel grösserer und damit gefährlicherer Strom durch den Körper.")),
]

assert 6/2 == 3 and 12/200 == 0.06 and round(230/240,2) == 0.96 and 100+200 == 300
assert 230*2 == 460 and round(2*(1/12),2) == 0.17 and 230/1000 == 0.23
# Parallel 100||100 = 50
assert 1/(1/100 + 1/100) == 50
print("Zahlen p6-2: OK")

n, do_, dc, oo, oc = apply_page("themen/p6-2-elektrizitaet.html", p62)
print(f"themen/p6-2-elektrizitaet.html: {n} Mini-Checks | div {do_}/{dc} {'OK' if do_==dc else 'DIFF'} | open( {oo}/{oc} {'OK' if oo==oc else 'DIFF'}")
