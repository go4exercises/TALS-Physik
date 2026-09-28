#!/usr/bin/env python3
"""
Erzeugt die Tonspur zu einem Clip — lokal, offline, aus dem Sprechertext
des Drehbuchs.

Warum ueberhaupt: Die Szenendauer wird sonst aus der Wortzahl geschaetzt
(`Woerter / sprechtempo`). Mit echtem Ton ist das falsch. Dieses Skript
misst die tatsaechliche Laenge jeder Szene und schreibt sie als Feld
`dauer` ins Drehbuch zurueck — danach stimmt Bild zu Sprache exakt.

Ergebnis: **eine** MP3 je Clip, nicht eine je Szene. Der Clip synchronisiert
sie gegen seine eigene Uhr; mit einer einzigen Spur gibt es nichts zu
verketten und kein Stolpern an den Szenengrenzen. Die Sprache jeder Szene
sitzt an `Szenenstart + vorlauf`, dazwischen ist Stille.

    export PIPER_MODELL=/pfad/de_DE-thorsten-high.onnx
    python3 scripts/build-clip-ton.py g2-2a-parametergleichung-drei-faelle
    python3 scripts/build-clips.py    g2-2a-parametergleichung-drei-faelle

Der zweite Aufruf ist noetig: Dieses Skript aendert nur das Drehbuch und
legt die Tonspur ab, gebaut wird der Clip weiterhin von build-clips.py.

Voraussetzungen (nicht im Repo, bewusst):
  pip install piper-tts soundfile
  Stimme: rhasspy/piper-voices, de/de_DE/thorsten/high  (Datensatz CC0)
Lizenzlage in HOWTO-clips.md, Abschnitt «Ton».
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import OrderedDict

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")
TON = os.path.join(CLIPS, "ton")

sys.path.insert(0, os.path.join(WURZEL, "scripts"))


def lade_generator():
    """szenen_planen aus build-clips.py wiederverwenden statt nachbauen —
    sonst laufen die beiden Zeitrechnungen frueher oder spaeter auseinander."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "buildclips", os.path.join(WURZEL, "scripts", "build-clips.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- Aussprache
# Fremdwoerter, die die Stimme falsch liest, bekommen eine feste Lautschrift
# (Piper nimmt IPA zwischen [[ und ]]). Getauscht wird nur im Text, der an
# Piper geht — Drehbuch, Transkript und Suchindex behalten die Schreibweise.
# Gilt auch in Zusammensetzungen (Milliampere, Amperemeter).
# Alles nach Hoerproben entschieden (Auftraggeber, 27.09.2026).
#
# 1. Wortstaemme -> Lautschrift. Gross/klein egal, nur am Wortanfang oder
#    nach einer Einheiten-Vorsilbe (sonst traefe «ampere» auch
#    «Schlamperei»); Zusammensetzungen greifen mit (Amperemeter).
AUSSPRACHE = [
    ("ampere", "ampˈɛːɾ"),              # bisher «AM-pe-re»
    ("coulomb", "kulˈoː"),              # bisher «KUH-lomp»; Nasal kennt die Stimme kaum
    ("joule", "dʒˈuːl"),                # bisher «Juh-le»
    ("pascal", "paskˈal"),              # bisher «PAS-kal»
    ("hertz", "hˈɛɾts"),                # «Kilohertz» verlor sonst das h
    ("boyle", "bˈɔɪl"),                 # bisher «Böh-le»
    ("mariotte", "maɾjˈɔt"),            # bisher «MAri-o-te»
    ("gay-lussac", "ɡeːlyːsˈak"),       # «Gee-lüü-SACK», langes ee und üü
    ("hooke", "hˈʊk"),                  # bisher «Hoo-ke»
    ("pythagoras", "pytˈɑːɡoːras"),     # bisher «PÜ-tagoras»
    ("laserpointer", "lˈeːzɐpɔɪntɐ"),   # bisher «Laaser-po-inter»
    ("spraydose", "ʃprˈeːdoːzə"),       # bisher «Schprei-dose»
    ("isotherm", "iːzoːtˈɛɾm"),         # bisher «I-sotterm»
    ("isobar", "iːzoːbˈɑːɾ"),           # bisher «I-sobar»
    ("photonen", "foːtˈoːnən"),         # sonst ohne Hauptbetonung
    ("zentripetal", "tsɛntɾipeːtˈɑːl"),  # sonst englisch «Sentraipt-oh…»
    # Nach Hoerproben 28.09.2026, in Saetzen aus beiden Repos (bisher meist
    # falsche Hauptbetonung)
    ("hypotenuse", "hypoːteːnˈuːzə"),
    ("logarithmus", "loːɡarˈɪtmʊs"),
    ("logarithmen", "loːɡarˈɪtmən"),
    ("definitions", "deːfiːniːtsjˈoːns"),
    ("funktions", "fʊŋktsjˈoːns"),
    ("äquivalenz", "ɛkviːvaːlˈɛnts"),
    ("sechstel", "zˈɛkstəl"),               # bisher «Sechs-TEEL»
    ("achsenabschnitt", "ˈaksənapʃnɪt"),
    ("komponentenweise", "kɔmpoːnˈɛntənvaɪzə"),
    ("mantisse", "mantˈɪsə"),
    ("exponentielles", "ɛkspoːnɛntsjˈɛləs"),
    ("exponential", "ɛkspoːnɛntsjˈɑːl"),
    ("exakte", "ɛksˈaktə"),                 # vor «exakt», sonst [[…]]e
    ("exakt", "ɛksˈakt"),
    ("hyperbel", "hypˈɛɾbəl"),
    ("gegenkathete", "ɡˈeːɡənkateːtə"),    # bisher «KA-te-te», kurz und verschluckt
    ("ankathete", "ˈankateːtə"),
    ("kathete", "katˈeːtə"),
    ("arkustangens", "ˈaɾkʊstˌaŋɡɛns"),    # vor «tangens»; bisher «TANG-ens» ohne g
    ("tangens", "tˈaŋɡɛns"),
    ("vertippt", "fɛɾtˈɪpt"),
    ("varianz", "vaɾiˈants"),
    ("variablenmenü", "vaɾiˈɑːblənmeːnˌyː"),
    ("untermenüs", "ˈʊntɐmeːnˌyːs"),       # «Menü» immer hinten betont (me-NÜ);
    ("untermenü", "ˈʊntɐmeːnˌyː"),         # bisher «Menüs» vorne, «Menü» hinten
    ("menüs", "meːnˈyːs"),                 # vor «menü», sonst [[…]]s
    ("menü", "meːnˈyː"),
    ("variablentaste", "vaɾiˈɑːbləntastə"),
    ("extremwerten", "ɛkstrˈeːmveːɾtən"),
    ("clear", "klˈiːɐ"),                    # Taste des TI-30X
    ("round", "rˈaʊnt"),
    ("domain", "doːmˈeːn"),
]
# Nicht geaendert, weil die bisherige Lesart besser klang: Archimedes,
# Perihel, Parabel, MathPrint, Asymptote, Mikrometer, Mikro; Volumen, linear
# und Erdbeschleunigung (28.09.2026 in Saetzen aus beiden Repos angehoert).
#
# 2. Abkuerzungen, die buchstabiert werden: nur in exakt dieser Schreibung
#    als ganzes Wort (sonst traefe «SI» auch «si» in anderen Woertern).
ABKUERZUNGEN = [
    ("FI", "ɛfˈiː"),                    # bisher «Fie»
    ("LED", "ɛleːdˈeː"),                # bisher «Leet»
    ("COP", "tseːoːpˈeː"),              # bisher «Kop»
    ("SI", "ɛsˈiː"),                    # bisher «Sie»
    ("EE", "eːˈeː"),                    # Tasten des TI-30X (Mathe, 28.09.2026)
    ("HY", "haːˈʏpsɪlɔn"),
    ("NAMES", "nˈeːms"),
    ("UNITS", "jˈuːnɪts"),
    ("Pfactor", "pˈeːfɛktɐ"),
    ("My", "mˈyː"),                     # Reibungszahl μ; bisher englisch «Mai»
]
# 3. Einfache Worttausche, wo keine Lautschrift noetig ist.
TAUSCH = [
    ("achthundert", "acht hundert"),    # sonst «acht-undert», auch in tausendachthundert…
    ("Newtonmeter", "Newton-Meter"),    # sonst englisch «Njuten-mieter»
    ("Lageenergie", "Lage-Energie"),    # sonst «Lag-energie»
    ("TI-30X", "T-I 30X"),              # Lautschrift vor «-30X» hiesse «minus dreissig»
]
VORSILBEN = r"(?:milli|mikro|nano|zenti|dezi|hekto|kilo|mega|giga)?"


def aussprache(text):
    """Setzt Lautschrift und Worttausche ein. Falle: Folgt ein Satzzeichen
    direkt auf ]], verschluckt Piper es und klebt das naechste Wort an
    («ampˈɛːɾdan», ohne Satzpause). Darum wandert ein Satzzeichen mit in die
    Klammer."""
    import re

    def klammer(ipa, nach, zeichen):
        if nach:                           # Amperemeter: Satzzeichen hinter dem Rest
            return "[[" + ipa + "]]" + nach + zeichen
        return "[[" + ipa + zeichen + "]]"

    for alt, neu_ in TAUSCH:
        text = re.sub(alt, neu_, text, flags=re.I) if alt.islower() else text.replace(alt, neu_)
    for wort, ipa in AUSSPRACHE:
        muster = re.compile(r"\b(%s)(%s)([^\W\d_]*)([.,;:!?]*)" % (VORSILBEN, re.escape(wort)), re.I)
        text = muster.sub(lambda m: m.group(1) + klammer(ipa, m.group(3), m.group(4)), text)
    for abk, ipa in ABKUERZUNGEN:
        muster = re.compile(r"\b%s\b([.,;:!?]*)" % re.escape(abk))
        text = muster.sub(lambda m: klammer(ipa, "", m.group(1)), text)
    return text


def sprich(piper, modell, text, ziel):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        f.write(text)
        quelle = f.name
    try:
        r = subprocess.run(piper + ["-m", modell, "-i", quelle, "-f", ziel],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"piper ist gescheitert:\n{r.stderr[-800:]}")
    finally:
        os.unlink(quelle)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", help="Drehbuch ohne .json")
    ap.add_argument("--modell", default=os.environ.get("PIPER_MODELL", ""),
                    help="Pfad zur .onnx-Stimme (oder Umgebung PIPER_MODELL)")
    ap.add_argument("--piper", default=os.environ.get("PIPER_CMD", "piper"),
                    help="Aufruf von piper (oder Umgebung PIPER_CMD)")
    ap.add_argument("--qualitaet", type=float, default=0.5,
                    help="MP3-Kompression 0.0 (gross) bis 1.0 (klein)")
    a = ap.parse_args()

    if not a.modell or not os.path.exists(a.modell):
        sys.exit("Stimmmodell fehlt — --modell setzen oder PIPER_MODELL exportieren.")
    try:
        import numpy as np
        import soundfile as sf
    except ImportError as e:
        sys.exit(f"{e} — `pip install soundfile` fehlt.")

    pfad = os.path.join(CLIPS, a.clip.removesuffix(".json") + ".json")
    if not os.path.exists(pfad):
        sys.exit(f"Drehbuch nicht gefunden: {pfad}")
    dreh = json.load(open(pfad, encoding="utf-8"), object_pairs_hook=OrderedDict)
    bc = lade_generator()
    piper = a.piper.split()

    # ---- Schritt 1: sprechen und messen ------------------------------
    stuecke = {}
    with tempfile.TemporaryDirectory() as tmp:
        for i, sz in enumerate(dreh["szenen"]):
            text = (sz.get("sprecher") or "").strip()
            if not text:
                continue
            w = os.path.join(tmp, f"{i}.wav")
            sprich(piper, a.modell, aussprache(text), w)
            daten, sr = sf.read(w, dtype="float32")
            stuecke[i] = (daten, sr)
            print(f"  Szene {i+1}: {len(daten)/sr:6.2f} s   {text[:52]}")

        if not stuecke:
            sys.exit("Keine sprecher-Texte im Drehbuch.")
        rate = stuecke[next(iter(stuecke))][1]

        # ---- Schritt 2: gemessene Dauer ins Drehbuch ------------------
        vorlauf = bc.STD["vorlauf"]
        takt = dreh.get("takt", bc.STD["takt"])
        nachlauf = dreh.get("nachlauf", bc.STD["nachlauf"])
        for i, sz in enumerate(dreh["szenen"]):
            letzte = max([el.get("ein", vorlauf + k * takt)
                          for k, el in enumerate(sz.get("elemente", []))] or [0.0])
            noetig = letzte + nachlauf
            if i in stuecke:
                daten, sr = stuecke[i]
                noetig = max(noetig, vorlauf + len(daten) / sr + 0.8)
            sz["dauer"] = round(max(noetig, 3.0), 2)
        json.dump(dreh, open(pfad, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

        # ---- Schritt 3: eine Spur, Sprache an die Szenenstarts --------
        plan, gesamt = bc.szenen_planen(dreh)
        spur = np.zeros(int(round(gesamt * rate)) + rate, dtype="float32")
        for i, p in enumerate(plan):
            if i not in stuecke:
                continue
            daten, _ = stuecke[i]
            ab = int(round((p["start"] + vorlauf) * rate))
            spur[ab:ab + len(daten)] += daten

        # Kopfraum: Piper steuert einzelne Saetze bis an die Grenze aus,
        # und der MP3-Encoder ueberschwingt leicht. Ohne das zerrt es.
        spitze = float(np.abs(spur).max())
        if spitze > 0.95:
            spur *= 0.95 / spitze

        os.makedirs(TON, exist_ok=True)
        ziel = os.path.join(TON, dreh["dateiname"] + ".mp3")
        sf.write(ziel, spur[:int(round(gesamt * rate))], rate,
                 format="MP3", compression_level=a.qualitaet)

    kb = os.path.getsize(ziel) / 1024
    print(f"\n  {os.path.relpath(ziel, WURZEL)}  —  {gesamt:.1f} s, {kb:.0f} kB")
    print(f"  Dauern im Drehbuch aktualisiert. Jetzt: "
          f"python3 scripts/build-clips.py {dreh['dateiname']}")


if __name__ == "__main__":
    main()
