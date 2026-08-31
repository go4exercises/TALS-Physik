#!/usr/bin/env python3
"""
Schreibt die Clips dorthin, wo sie erscheinen sollen: in die Lektionsseiten
und in die Bibliotheksseite clips.html.

Verfahren wie bei scripts/build-seo.py — der Inhalt zwischen zwei
Kommentarzeilen ist generiert, alles andere bleibt von Hand gepflegt.

    Lektionsseite:  <!-- CLIPS:ANFANG … -->  …  <!-- CLIPS:ENDE -->
    clips.html:     <!-- CLIPS-BIBLIOTHEK:ANFANG … -->  …  <!-- CLIPS-BIBLIOTHEK:ENDE -->

Welche Clips auf welche Seite gehoeren, steht ausschliesslich im Drehbuch
unter `lektion` (Liste von Codes aus nav.js) — nicht in der Seite. Ein Clip
kann so auf mehreren Seiten stehen, ohne dass er dupliziert wird.

Der Block enthaelt eine Startkarte je Clip und darunter das Transkript aus
clips/sprechertext-*.txt. Das Transkript ist nicht Beiwerk: Von einem
animierten Clip sieht eine Suchmaschine sonst gar nichts, und die
Volltextsuche der Site ebenfalls nicht.

Der Clip selbst wird erst beim Klick geladen (clipStart in mathlib.js).

    python3 scripts/build-clips-einbau.py            # Probelauf
    python3 scripts/build-clips-einbau.py --schreiben

Vorher `python3 scripts/build-clips.py` laufen lassen — dieses Skript liest
clips/clips.json und baut selbst keine Clips.
"""

import argparse
import html
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")

MARKE_AUF = ('<!-- CLIPS:ANFANG — generiert von scripts/build-clips-einbau.py, '
             'nicht von Hand ändern -->')
MARKE_ZU = '<!-- CLIPS:ENDE -->'
BLOCK = re.compile(re.escape(MARKE_AUF) + r'.*?' + re.escape(MARKE_ZU), re.DOTALL)

BIB_AUF = ('<!-- CLIPS-BIBLIOTHEK:ANFANG — generiert von scripts/build-clips-einbau.py, '
           'nicht von Hand ändern -->')
BIB_ZU = '<!-- CLIPS-BIBLIOTHEK:ENDE -->'
BIB = re.compile(re.escape(BIB_AUF) + r'.*?' + re.escape(BIB_ZU), re.DOTALL)

BIBLIOTHEK = "clips.html"

# Reihenfolge der Zweige innerhalb eines Lerngebiets. Im Lerngebiet 1
# stehen die Clips zur Arithmetik vor denen zur Algebra — man rechnet mit
# Zahlen, bevor man mit Buchstaben rechnet. Was hier nicht steht, kommt
# alphabetisch dahinter.
ZWEIGE = ["Arithmetik", "Grössen", "Algebra", "Funktionen", "Datenanalyse", "Geometrie"]

# So viele Farbnuancen stehen fuer die Nummernplaketten bereit. Jede Reihe
# bekommt eine, bei der naechsten Reihe wird weitergeschaltet — dadurch
# gruppiert die Farbe, was zusammengehoert.
NUANCEN = 8


def zweig(clip):
    return (clip.get("themenbereich") or "").split(" ·")[0].strip()


# Reihen, deren Ordnung didaktisch ist und nicht alphabetisch. Was hier
# nicht steht, kommt danach in alphabetischer Folge.
REIHEN = ["Lineare Gleichungen", "Ungleichungen", "Parametergleichung",
          "Quadratische Gleichungen", "Quadratische Ungleichungen",
          "Quadratische Parametergleichungen", "Quadratische Gleichungssysteme",
          "Bruchgleichungen", "Gleichungssysteme"]


def lektionsnummer(code):
    """g2-2a -> 2.2a — die Nummer, unter der die Seite im Lehrplan steht."""
    return code[1:].replace("-", ".", 1)


def ordnung(clip):
    """Sortierschluessel: Zweig, dann Lektion, dann Reihe, dann Platz darin.

    Die Lektion steht bewusst *nach* dem Zweig: In Lerngebiet 1 sollen die
    Arithmetik-Clips vor den Algebra-Clips stehen, auch wenn sie aus zwei
    verschiedenen Lektionen kommen. Innerhalb eines Zweiges ordnet dann die
    Lektionsnummer — so stehen 2.2a, 2.2b und 2.3 beieinander.
    """
    z = zweig(clip)
    r = clip.get("reihe") or clip["titel"]
    return (ZWEIGE.index(z) if z in ZWEIGE else len(ZWEIGE),
            z,
            (codes(clip) or [""])[0],
            REIHEN.index(r) if r in REIHEN else len(REIHEN),
            r,
            clip.get("folge") if clip.get("folge") else 99,
            clip["titel"])


def nuancen_zuteilen(clips):
    """Je Reihe eine Nuance, in der Reihenfolge ihres Auftretens."""
    zu, naechste = {}, 0
    for c in clips:
        r = c.get("reihe") or c["titel"]
        if r not in zu:
            zu[r] = naechste % NUANCEN + 1
            naechste += 1
    return zu


def lektionsseiten():
    """Code -> {nr, titel, url}, gelesen aus nav.js. Das ist die einzige
    Liste, die weiss, welche Lektion auf welcher Datei liegt."""
    quelle = open(os.path.join(WURZEL, "nav.js"), encoding="utf-8").read()
    treffer = re.findall(
        r"id:\s*'([^']+)'\s*,\s*nr:\s*'([^']*)'\s*,\s*titel:\s*'([^']*)'\s*,\s*url:\s*'([^']+)'",
        quelle)
    return {i: dict(nr=nr, titel=ti, url=u) for i, nr, ti, u in treffer}


def lerngebiete():
    """Die Lerngebiets-Gruppen aus dem Block GROUPS in nav.js.

    Warum von dort: Das ist die Struktur, nach der Startseite und Menues
    gebaut sind. Wuerde die Bibliothek nach dem Freitextfeld `lerngebiet`
    im Drehbuch gruppieren, liefe sie frueher oder spaeter auseinander —
    ein Tippfehler dort ergaebe eine neue Gruppe.

    Physik hat, anders als Mathe, keine zwei Faecher: GROUPS ist eine flache
    Liste von Lerngebieten (0 Vorwissen, 4 Mechanik, 5 Thermodynamik,
    6 andere Bereiche, 99 Extras).

    Rueckgabe: Liste von (nr, titel, [lektions-ids]) in der Reihenfolge,
    in der sie auch auf der Startseite stehen.
    """
    quelle = open(os.path.join(WURZEL, "nav.js"), encoding="utf-8").read()
    m = re.search(r"const GROUPS = \[(.*?)\n\];", quelle, re.S)
    if not m:
        return []
    aus = []
    for g in re.finditer(
            r"\{\s*nr:\s*'([^']*)'\s*,\s*titel:\s*'([^']*)'\s*,"
            r"(?:[^}]*?)ids:\s*\[([^\]]*)\]", m.group(1)):
        aus.append((g.group(1), g.group(2), re.findall(r"'([^']+)'", g.group(3))))
    return aus



def mmss(sekunden):
    return f"{int(sekunden) // 60}:{int(sekunden) % 60:02d}"


def codes(clip):
    v = clip.get("lektion") or []
    return [v] if isinstance(v, str) else list(v)


def transkript(datei):
    """clips/sprechertext-<name>.txt -> Liste (Zeit, Text). Fehlt die Datei,
    gibt es kein Transkript — das meldet das Skript, es ist kein Abbruch."""
    pfad = os.path.join(CLIPS, "sprechertext-" + datei.replace(".html", "") + ".txt")
    if not os.path.exists(pfad):
        return None
    zeilen = []
    for z in open(pfad, encoding="utf-8"):
        if "\t" not in z:
            continue
        t, txt = z.split("\t", 1)
        try:
            zeilen.append((mmss(float(t)), txt.strip()))
        except ValueError:
            continue
    return zeilen or None


def zeile(clip, vor="", nuance=1):
    """Eine Clip-Zeile: Nummer, Titel, Laufzeit. Sonst nichts.

    Dieselbe Zeile in der Bibliothek und auf der Lektionsseite — es ist
    dieselbe Aufgabe, also dieselbe Form. Die Nummer ist der Platz des
    Clips in seiner Reihe (Feld `folge`), nicht eine laufende Nummer der
    Seite. Clips ohne `folge` sind Ergaenzungen und stehen dahinter.

    `data-modus="gross"` heisst: der Clip laeuft ueber dem Fenster, nicht
    in der Zeile. Die Klasse `clip-start` bleibt am Knopf, damit
    clipStart/clipStop aus mathlib.js unveraendert greifen.
    """
    titel = html.escape(clip["titel"])
    folge = clip.get("folge")
    nr = (f'<span class="cl-folge">{folge}</span>' if folge
          else '<span class="cl-folge cl-ohne" aria-hidden="true">·</span>')
    return [
        f'<div class="clip cl-r{nuance}" data-clip="{vor}clips/{clip["datei"]}"'
        f' data-titel="{titel}" data-modus="gross">',
        '  <button class="clip-start cl-clip" type="button" onclick="clipStart(this)"'
        f' aria-label="Clip abspielen: {titel}">',
        '    ' + nr,
        f'    <span class="cl-titel">{titel}</span>',
        f'    <span class="cl-zeit">{mmss(clip.get("dauer_s", 0))}</span>',
        '  </button>',
        '</div>',
    ]



def block_lektion(clips, tiefe, code=None):
    """Der Block auf einer Lektionsseite — dieselbe Darstellung wie in der
    Bibliothek: eine zweispaltige Auswahl aus Nummer, Titel und Laufzeit,
    und der Clip laeuft gross ueber dem Fenster.

    Die Transkripte stehen gesammelt darunter in einem Aufklapper. Sie
    muessen im HTML bleiben: Von einem animierten Clip sieht die Suche
    sonst nichts, und die Ueberschrift `h3.clip-h[id]` je Clip ist das,
    woran build-suchindex.py seine Abschnitte schneidet.

    tiefe = Ebenen unter der Wurzel, daraus wird der ../-Praefix.
    """
    vor = "../" * tiefe
    # Dieselbe didaktische Ordnung wie in der Bibliothek — mit einem Zusatz:
    # Ein Clip kann zu mehreren Lektionen gehoeren. Auf einer Seite stehen
    # zuerst die Clips, deren *erste* Lektion diese Seite ist, danach die
    # Gaeste aus anderen Lektionen. Sonst koennte ein Gast die eigene Reihe
    # der Seite anfuehren, nur weil sein Zweig alphabetisch frueher kommt.
    def platz(c):
        gast = 0 if (code is None or (codes(c) or [""])[0] == code) else 1
        return (gast,) + ordnung(c)

    clips = sorted(clips, key=platz)
    nuance = nuancen_zuteilen(clips)
    aus = [MARKE_AUF, '<h2 id="clips">Clips</h2>',
           f'<div class="cl-body clip-auswahl"'
           f' style="grid-template-rows: repeat({-(-len(clips) // 2)}, auto)">']
    for c in clips:
        aus += ["  " + z for z in
                zeile(c, vor, nuance[c.get("reihe") or c["titel"]])]
    aus.append('</div>')

    tk = [(c, transkript(c["datei"])) for c in clips]
    if any(t for _, t in tk):
        aus.append('<details class="clip-transkripte">')
        aus.append('<summary>Transkripte — der gesprochene Text zum Mitlesen</summary>')
        for c, zeilen in tk:
            if not zeilen:
                continue
            stamm = c["datei"].replace(".html", "")
            aus.append(f'<h3 id="clip-{stamm}" class="clip-h">{html.escape(c["titel"])}</h3>')
            aus.append('<ol>')
            for zeit, txt in zeilen:
                aus.append(f'<li><span class="tk-zeit">{zeit}</span>'
                           f'<span>{html.escape(txt)}</span></li>')
            aus.append('</ol>')
        aus.append('</details>')
    aus.append(MARKE_ZU)
    return "\n".join(aus)



def block_bibliothek(alle, seiten):
    """clips.html — nach Fach, darin nach Lerngebiet, jede Gruppe aufklappbar.

    Auf ~100 Clips ausgelegt: Die Gruppen sind zu, ihre Kopfzeile nennt
    Anzahl und Gesamtlaufzeit. So bleibt die Seite eine Uebersicht und
    keine Liste, durch die man scrollt. Dasselbe Verfahren wie die
    Kapitelbloecke der Startseite.

    Kein Transkript und kein Kurzbeschrieb: Die stehen auf der
    Lektionsseite, wo der Clip im Zusammenhang steht. Hier wuerden 100
    Transkripte die Seite unbrauchbar machen — und fuer die Suche zaehlen
    sie ohnehin schon dort.
    """
    gruppen = lerngebiete()
    nach_lektion = {}
    for c in alle:
        for code in codes(c):
            nach_lektion.setdefault(code, []).append(c)

    aus = [BIB_AUF]
    offen = False
    gesamt = 0
    for nr, titel, ids in gruppen:
        drin, gesehen = [], set()
        for code in ids:
            for c in nach_lektion.get(code, []):
                if c["datei"] not in gesehen:      # ein Clip auf zwei Lektionen
                    gesehen.add(c["datei"])        # derselben Gruppe nur einmal
                    drin.append(c)
        if not drin:
            continue                               # leere Lerngebiete weglassen
        if not offen:
            # Physik hat keine zwei Faecher: eine Liste, darin die
            # Lerngebiete. Die Zwischenueberschrift je Fach entfaellt.
            aus.append('<div class="cl-liste">')
            offen = True
        # Didaktische Ordnung: Reihen alphabetisch, darin nach `folge`.
        # Clips ohne `folge` sind Ergaenzungen und kommen ans Ende ihrer Reihe.
        drin.sort(key=ordnung)
        nuance = nuancen_zuteilen(drin)
        dauer = sum(c.get("dauer_s", 0) for c in drin)
        gesamt += len(drin)
        kid = f"p{nr}"
        aus += [
            '<div class="cl-kap">',
            f'  <button class="cl-hdr" type="button" aria-expanded="false"'
            f' aria-controls="cl-{kid}" onclick="togClips(\'{kid}\')">',
            f'    <span class="cl-nr">{nr}</span>',
            f'    <span class="cl-name">{html.escape(titel)}</span>',
            f'    <span class="cl-anz">{len(drin)} '
            f'{"Clip" if len(drin) == 1 else "Clips"} · {mmss(dauer)}</span>',
            '    <span class="cl-tog" aria-hidden="true">▼</span>',
            '  </button>',
            f'  <div class="cl-body" id="cl-{kid}" hidden>',
        ]
        # Untertitel je Lektion und Reihe. Ein Lerngebiet hat schnell
        # zwanzig Clips; ohne Zwischenueberschrift ist das eine Liste, durch
        # die man liest, statt einer, in der man etwas findet.
        letzte = None
        for c in drin:
            eigene = [x for x in codes(c) if x in ids]
            schlue = (eigene[0] if eigene else "", c.get("reihe") or c["titel"])
            if schlue != letzte:
                if letzte is not None:
                    aus.append('    </div>')
                aus.append('    <div class="cl-gruppe">')
                marke = lektionsnummer(schlue[0]) if schlue[0] else ""
                aus.append('      <h3 class="cl-gt">'
                           + (f'<span class="cl-gnr">{marke}</span>' if marke else "")
                           + html.escape(schlue[1]) + '</h3>')
                letzte = schlue
            aus += ["      " + z for z in
                    zeile(c, "", nuance[c.get("reihe") or c["titel"]])]
        if letzte is not None:
            aus.append('    </div>')
        aus += ['  </div>', '</div>']
    if offen:
        aus.append("</div>")
    if not gesamt:
        aus.append('<p class="cl-leer">Noch keine Clips.</p>')
    aus.append(BIB_ZU)
    return "\n".join(aus)



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schreiben", action="store_true", help="Änderungen speichern")
    a = ap.parse_args()

    index = os.path.join(CLIPS, "clips.json")
    if not os.path.exists(index):
        sys.exit("clips/clips.json fehlt — erst `python3 scripts/build-clips.py` laufen lassen.")
    alle = json.load(open(index, encoding="utf-8"))["clips"]
    seiten = lektionsseiten()

    nach_lektion = {}
    for c in alle:
        for code in codes(c):
            if code not in seiten:
                print(f"  [FEHLER] {c['datei']}: Lektion '{code}' steht nicht in nav.js")
                continue
            nach_lektion.setdefault(code, []).append(c)

    aufgaben = []          # (pfad, neuer Text)
    gleich, ohne_marker = 0, []

    for code, clips in sorted(nach_lektion.items()):
        pfad = os.path.join(WURZEL, seiten[code]["url"])
        if not os.path.exists(pfad):
            print(f"  [FEHLER] {code}: {seiten[code]['url']} existiert nicht")
            continue
        text = open(pfad, encoding="utf-8").read()
        if not BLOCK.search(text):
            ohne_marker.append((code, seiten[code]["url"], len(clips)))
            continue
        tiefe = seiten[code]["url"].count("/")
        neu = BLOCK.sub(lambda _m: block_lektion(clips, tiefe, code), text, count=1)
        if neu == text:
            gleich += 1
        else:
            aufgaben.append((pfad, neu))

    bib = os.path.join(WURZEL, BIBLIOTHEK)
    if not os.path.exists(bib):
        print(f"  [WARN] {BIBLIOTHEK} fehlt — Bibliothek wird nicht geschrieben")
    else:
        text = open(bib, encoding="utf-8").read()
        if not BIB.search(text):
            print(f"  [WARN] {BIBLIOTHEK} hat keine CLIPS-BIBLIOTHEK-Marker")
        else:
            neu = BIB.sub(lambda _m: block_bibliothek(alle, seiten), text, count=1)
            if neu == text:
                gleich += 1
            else:
                aufgaben.append((bib, neu))

    print(f"{len(aufgaben)} Seiten zu aktualisieren, {gleich} bereits aktuell")
    for code, url, n in ohne_marker:
        print(f"  [WARN] {code} hat {n} Clip(s), aber keine CLIPS-Marker in {url}")
    for pfad, _ in aufgaben:
        print("   ", os.path.relpath(pfad, WURZEL))

    if not aufgaben:
        return
    if not a.schreiben:
        print("\nProbelauf. Mit --schreiben werden die Änderungen gespeichert.")
        return
    for pfad, neu in aufgaben:
        open(pfad, "w", encoding="utf-8").write(neu)
    print(f"\n{len(aufgaben)} Seiten geschrieben.")


if __name__ == "__main__":
    main()
