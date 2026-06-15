#!/usr/bin/env python3
# Korrigiert ASCII-Transliterationen (ae/oe/ue) in den Phase-2-Bloecken
# (lernziele, kernpunkte, frage) zu echten Umlauten. Arbeitet NUR innerhalb
# dieser Bloecke, damit legitime Vorkommen (z.B. "aktuell") unberuehrt bleiben.
# Schweizer "ss" wird nie angetastet.
import pathlib, re

BASE = pathlib.Path(__file__).resolve().parent.parent / "themen"

REPL = {
 "erklaeren":"erklären","Geschwindigkeitsaenderung":"Geschwindigkeitsänderung",
 "Gleichfoermig":"Gleichförmig","gleichfoermigen":"gleichförmigen","gleichfoermiger":"gleichförmiger",
 "Gleichmaessig":"Gleichmässig","gleichmaessig":"gleichmässig","loesen":"lösen",
 "unabhaengig":"unabhängig","aendert":"ändert","staendig":"ständig","waechst":"wächst",
 "Bremsverzoegerung":"Bremsverzögerung","fuer":"für","Koerpers":"Körpers","Koerpern":"Körpern",
 "Koerper":"Körper","massenunabhaengig":"massenunabhängig","Traegheit":"Trägheit",
 "Reibungskraefte":"Reibungskräfte","Kraefte":"Kräfte","Raeder":"Räder","kuerzt":"kürzt",
 "uebertragene":"übertragene","laengs":"längs","zaehlt":"zählt","Vorgaenge":"Vorgänge",
 "Verhaeltnis":"Verhältnis","zugefuehrter":"zugeführter","Hoehe":"Höhe",
 "Waermemenge":"Wärmemenge","Waermebilanzen":"Wärmebilanzen","Waermekapazitaet":"Wärmekapazität",
 "Waermetransports":"Wärmetransports","Waerme":"Wärme","erklaert":"erklärt",
 "Festkoerpern":"Festkörpern","Festkoerper":"Festkörper","aufzaehlen":"aufzählen",
 "noetigen":"nötigen","noetige":"nötige","benoetigte":"benötigte","laengeren":"längeren",
 "Schraubenschluessel":"Schraubenschlüssel","Schluessel":"Schlüssel",
 "Hebelverlaengerung":"Hebelverlängerung","haelt":"hält","vollstaendiges":"vollständiges",
 "muessen":"müssen","Flaeche":"Fläche","haengt":"hängt","Fuellhoehe":"Füllhöhe",
 "Gefaessform":"Gefässform","verdraengten":"verdrängten","Fluessigkeiten":"Flüssigkeiten",
 "Fluessigkeit":"Flüssigkeit","Eiswuerfel":"Eiswürfel","unveraendert":"unverändert",
 "Aggregatzustaenden":"Aggregatzuständen","gasfoermig":"gasförmig","naehert":"nähert",
 "naeher":"näher","Energieuebertragung":"Energieübertragung","Prozessgroesse":"Prozessgrösse",
 "uebertragen":"übertragen","groessere":"grössere","groesste":"grösste","groesser":"grösser",
 "staerker":"stärker","waehrend":"während","Erwaermen":"Erwärmen","Erwaermung":"Erwärmung",
 "kaelteres":"kälteres","ueberleben":"überleben","Gasbehaelter":"Gasbehälter",
 "Temperaturaenderungen":"Temperaturänderungen","Bruecken":"Brücken",
 "Laengenausdehnung":"Längenausdehnung","wellenlaengenabhaengigen":"wellenlängenabhängigen",
 "wellenlaengenabhaengige":"wellenlängenabhängige","Wellenlaengen":"Wellenlängen",
 "Wellenlaenge":"Wellenlänge","Grundgroessen":"Grundgrössen","hoehere":"höhere",
 "kuerzere":"kürzere","Toene":"Töne","Stromstaerke":"Stromstärke","durchfuehren":"durchführen",
 "Parallelwiderstaenden":"Parallelwiderständen","Widerstaende":"Widerstände","Stroeme":"Ströme",
 "abhaengig":"abhängig","Gefaehrlich":"Gefährlich","ueber":"über",
 "Fuer":"Für","Auftriebskraefte":"Auftriebskräfte","verdraengt":"verdrängt",
 "fluessig":"flüssig","fuehrt":"führt","Atmosphaere":"Atmosphäre","zugefuehrte":"zugeführte",
}
# laengste Schluessel zuerst, damit Teilstrings nicht vorzeitig ersetzt werden
KEYS = sorted(REPL, key=len, reverse=True)

def fix_text(t):
    for k in KEYS:
        t = t.replace(k, REPL[k])
    return t

# Bloecke, die korrigiert werden (nur deren Innentext)
BLOCK_PATTERNS = [
    re.compile(r'<details class="lernziele">.*?</details>', re.S),
    re.compile(r'<h3>Kernpunkte</h3>\s*<ul class="kernpunkte">.*?</ul>', re.S),
    re.compile(r'<details class="frage">.*?</details>', re.S),
]

if __name__ == "__main__":
    total = 0
    for path in sorted(BASE.glob("*.html")):
        txt = path.read_text(encoding="utf-8")
        orig = txt
        for pat in BLOCK_PATTERNS:
            txt = pat.sub(lambda m: fix_text(m.group(0)), txt)
        if txt != orig:
            path.write_text(txt, encoding="utf-8")
            total += 1
        print(f"{path.name}: {'korrigiert' if txt != orig else 'unveraendert'}")
    print(f"Dateien geaendert: {total}")
