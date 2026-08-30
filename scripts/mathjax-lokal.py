#!/usr/bin/env python3
"""
Ersetzt den Aufruf an cdn.jsdelivr.net durch das lokal ausgelieferte MathJax.

Warum: Wie bei den Schriften ging bei jedem Seitenaufruf die IP-Adresse der
Besucherin an einen Dritten — auf 50 Seiten, also praktisch ueberall. Mit
vendor/mathjax/ stimmt «Keine Cookies · Kein Tracking» vollstaendig, und die
Seite laeuft ohne Netz.

Wichtig: Die Seiten setzen `loader: { load:['[tex]/boldsymbol'] }`. MathJax
laedt Erweiterungen relativ zum Pfad der Startdatei nach, darum muss
vendor/mathjax/input/tex/extensions/boldsymbol.js daneben liegen — sonst
bricht der Formelsatz ueberall dort, wo \\boldsymbol vorkommt.

Voraussetzung: vendor/mathjax/tex-svg.js liegt im Repo (aus
node_modules/mathjax-full/es5, Version 3.2.2 — genau das, was
`mathjax@3` vom CDN geliefert hat).

    python3 scripts/mathjax-lokal.py            # zeigt nur, was geaendert wuerde
    python3 scripts/mathjax-lokal.py --schreiben

Das Skript ist wiederholbar: bereits umgestellte Dateien bleiben unberuehrt.
"""

import argparse
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
CDN = re.compile(
    r'<script[^>]*src=["\'][^"\']*cdn\.jsdelivr\.net/npm/mathjax[^"\']*["\'][^>]*>\s*</script>',
    re.I)
SCHON_LOKAL = re.compile(r'src=["\'][^"\']*vendor/mathjax/tex-svg\.js["\']', re.I)


def relativer_pfad(htmldatei):
    """Wie viele Ebenen tief liegt die Datei? Daraus wird ../ je Ebene."""
    tiefe = os.path.relpath(htmldatei, WURZEL).count(os.sep)
    return "../" * tiefe + "vendor/mathjax/tex-svg.js"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schreiben", action="store_true",
                    help="Aenderungen wirklich speichern")
    a = ap.parse_args()

    if not os.path.exists(os.path.join(WURZEL, "vendor", "mathjax", "tex-svg.js")):
        sys.exit("vendor/mathjax/tex-svg.js fehlt — erst aus node_modules kopieren.")

    geaendert, schon, ohne = [], [], 0
    for ordner, unter, dateien in os.walk(WURZEL):
        unter[:] = [u for u in unter
                    if u not in (".git", "node_modules", "vendor")]
        for d in sorted(dateien):
            if not d.endswith(".html"):
                continue
            pfad = os.path.join(ordner, d)
            text = open(pfad, encoding="utf-8").read()

            if not CDN.search(text):
                if SCHON_LOKAL.search(text):
                    schon.append(pfad)
                else:
                    ohne += 1
                continue

            ersatz = '<script src="%s"></script>' % relativer_pfad(pfad)
            geaendert.append((pfad, CDN.sub(ersatz, text)))

    print(f"{len(geaendert)} Dateien mit MathJax-CDN-Aufruf")
    print(f"{len(schon)} bereits lokal")
    print(f"{ohne} ohne MathJax")

    if not geaendert:
        print("Nichts zu tun.")
        return

    for pfad, _ in geaendert[:12]:
        print("   ", os.path.relpath(pfad, WURZEL))
    if len(geaendert) > 12:
        print(f"    … und {len(geaendert) - 12} weitere")

    if not a.schreiben:
        print("\nProbelauf. Mit --schreiben werden die Aenderungen gespeichert.")
        return

    for pfad, neu in geaendert:
        open(pfad, "w", encoding="utf-8").write(neu)
    print(f"\n{len(geaendert)} Dateien umgestellt.")
    print("Jetzt im Browser pruefen: Netzwerk-Tab, neu laden — es darf keine")
    print("Anfrage mehr an cdn.jsdelivr.net geben, und die Formeln muessen stehen.")


if __name__ == "__main__":
    main()
