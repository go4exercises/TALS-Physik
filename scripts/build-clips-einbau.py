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
import clips_bibliothek   # Physik: REIHEN_VORN dort, nur fuer die Bibliothek


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
    6 andere Bereiche).

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


def suchtext(clip):
    """Alles, wonach in der Bibliothek gesucht werden koennen soll.

    Titel und Reihe stehen sichtbar in der Zeile, Schlagworte und
    Kurzbeschrieb nicht — sie liegen im Drehbuch und waeren sonst totes
    Kapital. Dazu die Lektionsnummer, damit «4.1» ebenso trifft wie
    «Kinematik». Kleingeschrieben, weil das Suchfeld ebenso vergleicht.
    """
    teile = [clip.get("titel", ""), clip.get("reihe", ""),
             clip.get("kurzbeschrieb", "")]
    teile += clip.get("schlagworte") or []
    teile += [lektionsnummer(c) for c in codes(clip)]
    return html.escape(" ".join(teile).lower(), quote=True)


def auch_in(clip, ids, seiten):
    """Wo derselbe Clip sonst noch steht — ohne die Lektionen dieser Gruppe.

    Fuenf Clips sind ueber Lerngebietsgrenzen hinweg zugeordnet und
    erscheinen darum zweimal in der Liste. Ohne diesen Hinweis sieht das
    nach zwei Clips aus; mit ihm sieht man, was das Projekt richtig macht:
    einmal gespeichert, mehrfach zugeordnet.
    """
    fremd = [c for c in codes(clip) if c not in ids]
    if not fremd:
        return ""
    # Eine fremde Lektion bekommt ihren Namen, mehrere nur die Nummern:
    # «auch in 0.3 Messen — Waagen, Dichte, Einheiten und 0.2 Groessen,
    # Einheiten und Messen» liest niemand mehr.
    if len(fremd) == 1:
        s = seiten.get(fremd[0])
        name = f"{lektionsnummer(fremd[0])} {s['titel']}" if s else lektionsnummer(fremd[0])
        return "auch in " + name
    nummern = sorted(lektionsnummer(c) for c in fremd)
    return "auch in " + " und ".join([", ".join(nummern[:-1]), nummern[-1]])


def zeile(clip, vor="", nuance=1, suche=None, auch="", anker=None, animlink=None):
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
    # `data-suche` traegt die Bibliothek, die Lektionsseite nicht: Dort
    # gibt es nichts zu filtern, und das Attribut waere nur Ballast.
    such = f' data-suche="{suche}"' if suche else ""
    # Sprungziel der Volltextsuche. Sie fuehrt zum einzelnen Clip, nicht
    # mehr zur Bibliotheksseite — dafuer braucht die Zeile eine Adresse.
    # Nur die Bibliothek vergibt sie, und dort nur beim ersten Vorkommen:
    # Ein Clip auf zwei Lerngebieten steht zweimal in der Liste, eine ID
    # darf es nur einmal geben.
    id_ = f' id="{anker}"' if anker else ""
    marke = ([f'    <span class="cl-auch">{html.escape(auch)}</span>'] if auch else [])
    # Clips zu einer einzelnen Animation sind farblich abgesetzt und tragen
    # vorn den Link «Anim» zu ihrer Animation — sie erklaeren ein Bild auf
    # der Seite, nicht ein Stoffgebiet. Der Link steht neben dem Knopf, nicht
    # darin: ein <a> in einem <button> ist kein gueltiges HTML.
    anim = clip.get("animation")
    kl = f"clip cl-r{nuance}" + (" cl-anim" if anim else "")
    alink = ([f'  <a class="cl-animlink" href="{animlink}"'
              f' aria-label="Zur Animation: {titel}">Anim</a>'] if anim and animlink else [])
    return [
        f'<div class="{kl}"{id_} data-clip="{vor}clips/{clip["datei"]}"'
        f' data-titel="{titel}" data-modus="gross"{such}>',
    ] + alink + [
        '  <button class="clip-start cl-clip" type="button" onclick="clipStart(this)"'
        f' aria-label="Clip abspielen: {titel}">',
        '    ' + nr,
        f'    <span class="cl-titel">{titel}</span>',
        f'    <span class="cl-zeit">{mmss(clip.get("dauer_s", 0))}</span>',
        '  </button>',
    ] + marke + ['</div>']



ANIM_AUF = '<!-- CLIP-ANIM — generiert von scripts/build-clips-einbau.py -->'
ANIM_ZU = '<!-- /CLIP-ANIM -->'
ANIM_ALT = re.compile(r'\n\s*' + re.escape(ANIM_AUF) + r'.*?' + re.escape(ANIM_ZU), re.DOTALL)


def anim_knoepfe(text, clips, tiefe):
    """Setzt in die Titelzeile jeder Animation, zu der es einen Clip gibt,
    den Eintrag «▶ Clip» neben «Worauf achten?» und «Erkenntnis».

    Gefunden wird die Animation ueber den Anker ihres <h3>,
    div.anim-titel oder <p> am Anfang der Titelzeile (Feld
    `animation` im Drehbuch); eingesetzt wird als letztes Kind der
    .widget-titelzeile, zwischen eigenen Markern — so bleibt der Knopf
    generiert und die Dauer stimmt nach jedem Neubau.
    """
    text = ANIM_ALT.sub("", text)
    vor = "../" * tiefe
    for c in clips:
        anker = c.get("animation")
        if not anker:
            continue
        # Mathe: Animationen in Aufgaben tragen statt <h3> ein div.anim-titel
        m = re.search(r'<(?:h3|div class="anim-titel"|p) id="%s"' % re.escape(anker), text)
        if not m:
            print(f"  [FEHLER] {c['datei']}: Animation #{anker} nicht gefunden")
            continue
        # Titelzeile auch mit weiteren Attributen (Mathe: style="margin:…")
        auf = [t.start() for t in re.finditer(r'<div class="widget-titelzeile"[^>]*>', text[:m.start()])]
        start = auf[-1] if auf else -1
        if start < 0 or m.start() - start > 200:
            # Mathe: <h3> im .widget-header, Titelzeile erst im .widget-body —
            # dann die naechste Titelzeile, sofern sie im selben Widget liegt
            nach = re.search(r'<div class="widget-titelzeile"[^>]*>', text[m.end():])
            if nach and '<div class="widget">' not in text[m.end():m.end() + nach.start()]:
                start = m.end() + nach.start()
        if start < 0 or (start < m.start() and m.start() - start > 200):
            print(f"  [FEHLER] {c['datei']}: #{anker} steht in keiner .widget-titelzeile")
            continue
        # Ende der Titelzeile: das passende </div> ab ihrem Anfang
        tiefe_, i = 0, start
        for t in re.finditer(r'<div\b|</div>', text[start:]):
            tiefe_ += 1 if t.group(0) != '</div>' else -1
            if tiefe_ == 0:
                i = start + t.start()
                break
        titel = html.escape(c["titel"])
        knopf = (f'\n  {ANIM_AUF}\n'
                 f'  <div class="clip" data-clip="{vor}clips/{c["datei"]}" data-titel="{titel}"'
                 f' data-modus="gross">\n'
                 f'    <button class="ah-clip-knopf" type="button" onclick="clipStart(this)"'
                 f' aria-label="Clip zu dieser Animation abspielen ({mmss(c.get("dauer_s", 0))}):'
                 f' {titel}">▶ Clip</button>\n'
                 f'  </div>\n  {ANIM_ZU}')
        rumpf = text[:i].rstrip()
        text = rumpf + knopf + "\n" + text[i:]
    return text


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
    # Zuerst die Clips zum Stoff, darunter abgesetzt die zu den Animationen
    stoff = [c for c in clips if not c.get("animation")]
    anim = [c for c in clips if c.get("animation")]
    aus = [MARKE_AUF, '<h2 id="clips">Clips</h2>']
    for gruppe, kopf in ((stoff, None),
                         (anim, 'Clips zu den Animationen — was jede Animation zeigt')):
        if not gruppe:
            continue
        if kopf:
            aus.append(f'<p class="cl-animkopf">{kopf}</p>')
        aus.append(f'<div class="cl-body clip-auswahl"'
                   f' style="grid-template-rows: repeat({-(-len(gruppe) // 2)}, auto)">')
        for c in gruppe:
            aus += ["  " + z for z in
                    zeile(c, vor, nuance[c.get("reihe") or c["titel"]],
                          animlink=("#" + c["animation"]) if c.get("animation") else None)]
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
    benannt = set()          # Clips, die ihre ID schon haben
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
            stamm = c["datei"].replace(".html", "")
            anker = None if stamm in benannt else "clip-" + stamm
            benannt.add(stamm)
            aus += ["      " + z for z in
                    zeile(c, "", nuance[c.get("reihe") or c["titel"]],
                          suche=suchtext(c), auch=auch_in(c, ids, seiten),
                          anker=anker,
                          animlink=(seiten[eigene[0]]["url"] + "#" + c["animation"])
                          if c.get("animation") and eigene else None)]
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
        neu = anim_knoepfe(neu, clips, tiefe)
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
            neu = BIB.sub(lambda _m: clips_bibliothek.block_bibliothek(alle, seiten, sys.modules[__name__]),
                          text, count=1)
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
