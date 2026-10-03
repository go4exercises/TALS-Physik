#!/usr/bin/env python3
"""Vertont die Fragen eines Clips («fragen» im Drehbuch, HOWTO-clips.md).

Jede Frage und jede Rückmeldung bekommt eine eigene kurze Tondatei mit
derselben Stimme wie der Clip: clips/ton/<clip>-f<i>-<schluessel>.mp3.
Der Abspieler spielt sie, wenn die Frage erscheint bzw. geantwortet wird —
und nur, wenn der Ton des Clips an ist. Die Haupttonspur bleibt unberührt.

Aus TALS-Mathe übernommen (03.10.2026), dort entstanden; steht nicht in
abgleich.py. Benutzt sprich() und aussprache() aus build-clip-ton.py
(geteiltes Werkzeug, darum nicht dort eingebaut) und fragen_texte() aus
build-clips.py, damit Dateinamen und Abspieler immer zusammenpassen.

  export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
  python3 scripts/build-clip-fragen-ton.py <clipname>
  python3 scripts/build-clips.py <clipname>              # danach, damit der Clip die Dateien kennt
"""
import argparse
import importlib.util
import json
import os
import sys
import tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TON = os.path.join(WURZEL, "clips", "ton")


def lade(datei, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(WURZEL, "scripts", datei))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", help="Drehbuch ohne .json")
    ap.add_argument("--modell", default=os.environ.get("PIPER_MODELL", ""))
    ap.add_argument("--piper", default=os.environ.get("PIPER_CMD", "piper"))
    ap.add_argument("--qualitaet", type=float, default=0.5)
    a = ap.parse_args()
    if not a.modell or not os.path.exists(a.modell):
        sys.exit("Stimmmodell fehlt — --modell setzen oder PIPER_MODELL exportieren.")
    import numpy as np
    import soundfile as sf

    ton = lade("build-clip-ton.py", "clipton")
    bc = lade("build-clips.py", "buildclips")
    dreh = json.load(open(os.path.join(WURZEL, "clips", a.clip.removesuffix(".json") + ".json"), encoding="utf-8"))
    if not dreh.get("fragen"):
        sys.exit("Das Drehbuch hat keine «fragen».")
    os.makedirs(TON, exist_ok=True)
    piper = a.piper.split()

    # Alte Fragetoene dieses Clips entfernen: sonst bleiben Dateien gestrichener
    # Rueckmeldungen liegen, und der Abspieler wuerde sie noch finden.
    for alt in os.listdir(TON):
        if alt.startswith(dreh["dateiname"] + "-f") and alt.endswith(".mp3"):
            os.remove(os.path.join(TON, alt))

    with tempfile.TemporaryDirectory() as tmp:
        for i, F in enumerate(dreh["fragen"]):
            for schl, _, gesprochen in bc.fragen_texte(F):
                w = os.path.join(tmp, "s.wav")
                ton.sprich(piper, a.modell, ton.aussprache(gesprochen), w)
                daten, rate = sf.read(w, dtype="float32")
                spitze = float(np.abs(daten).max()) if len(daten) else 0
                if spitze > 0.95:
                    daten *= 0.95 / spitze
                ziel = os.path.join(TON, bc.fragen_tondatei(dreh["dateiname"], i, schl))
                sf.write(ziel, daten, rate, format="MP3", compression_level=a.qualitaet)
                print(f"  Frage {i + 1} {schl:<7} {len(daten) / rate:5.1f} s  {gesprochen[:60]}")
    print(f"\n  Jetzt: python3 scripts/build-clips.py {dreh['dateiname']}")


if __name__ == "__main__":
    main()
