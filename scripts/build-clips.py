#!/usr/bin/env python3
"""
Clip-Generator für physik.begreifbar.ch
======================================

Macht aus jedem Drehbuch in clips/ einen animierten Erklärclip als HTML.

    python3 scripts/build-clips.py                 # alle Clips bauen
    python3 scripts/build-clips.py bruchgleichungen
    python3 scripts/build-clips.py --eigenstaendig  # Schriften einbetten

Standardfall ist die Web-Fassung: sie verweist auf ../schriften.css und wiegt
rund 10 kB. Sie ist dafür gebaut, in einer Lektionsseite in einem <iframe> zu
stecken oder direkt geöffnet zu werden.

Mit --eigenstaendig entsteht stattdessen eine Datei, die alles enthält —
für Moodle, zum Verschicken, fürs Archiv.

Nebenbei entstehen clips/clips.json (Verzeichnis aller Clips für die
Bibliotheksseite) und je ein sprechertext-<name>.txt für die Vertonung.

Drehbuch-Aufbau: siehe clips/vorlage.json und todo.md.
"""

import argparse
import glob
import json
import math
import os
import re
import subprocess
import sys
from datetime import date

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")

# ---------------------------------------------------------------- Standardwerte
STD = {
    "takt": 1.7,          # Abstand zwischen Einblendungen, wenn nichts angegeben
    "nachlauf": 2.6,      # Standzeit nach der letzten Einblendung
    "vorlauf": 0.4,       # Verzögerung am Szenenanfang
    "sprechtempo": 1.45,  # Wörter pro Sekunde — für die Szenenlänge ohne Tonspur
    "theme": "heft",
}


# ---------------------------------------------------------------- Formelsatz
# Formelsatz. Seit dem 31.08.2026 setzt MathJax alle Clips: eine Formel
# lässt sich damit unverändert von einer Lektionsseite ins Drehbuch
# kopieren, statt in eine zweite Schreibweise übersetzt zu werden. Die
# eigene Schreibweise unten bleibt erreichbar über "latex": false — die
# 28 umgestellten Drehbücher brauchen sie nicht mehr.
LATEX = True


def tex(text):
    """Rohes LaTeX fuer MathJax verpacken — nur HTML-Zeichen entschaerfen."""
    t = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return "\\(" + t + "\\)"


def formel(text):
    """Kompakte Formelschreibweise in HTML.

        [a|b]   Bruch a über b
        x^2     Hochstellung
        -       echtes Minus
        *       Malpunkt
        !=      Ungleichheitszeichen,  <=  >=  ->  =>  in  notin  R  D
        _1      Tiefstellung
        "36"    Überstrich — die Periode einer Dezimalzahl

    Einzelne lateinische Buchstaben werden kursiv gesetzt (Variablen).
    """
    if LATEX:
        return tex(text)
    t = text

    def zeichen(s):
        # <=> muss vor <= stehen, sonst wird daraus ein «≤>».
        for a, b in [("<=>", "⟺"), ("!=", "≠"), ("<=", "≤"), (">=", "≥"),
                     ("=>", "⟹"), ("->", "⟶"), ("\\R", "ℝ"),
                     ("*", "·"), ("+-", "±")]:
            s = s.replace(a, b)
        # Was jetzt noch an < und > dasteht, ist gemeint — «2 < 3». Hier
        # maskieren, solange noch keine Tags im Text sind; sonst hält der
        # Browser ein «a <b» für den Anfang eines Elements und verschluckt es.
        s = s.replace("<", "&lt;").replace(">", "&gt;")
        # Wortzeichen nur als eigenständiges Wort ersetzen, sonst wird
        # aus «Scheinlösung» ein «Sche∈lösung».
        for a, b in [("notin", "∉"), ("in", "∈"), ("sqrt", "√"), ("inf", "∞")]:
            s = re.sub(r"(?<![A-Za-zÄÖÜäöü])" + a + r"(?![A-Za-zÄÖÜäöü])", b, s)
        # - sind die Platzhalter für Farb- und Kursivgruppen.
        # Sie müssen hier wie Zeichen zählen, sonst bleibt ein «-» davor
        # oder dahinter ein Bindestrich statt eines Minuszeichens.
        s = re.sub(r"(?<=[\w\)\]\s-])-(?=[\w\(\[\s-])", "−", s)
        s = re.sub(r"^-", "−", s)
        s = re.sub(r"(?<=[\s\(\{\[=,;])-(?=[\d-]|[a-zA-Z])", "−", s)
        s = re.sub(r"  +", lambda m: "\u00a0" * len(m.group()), s)
        return s

    def hoch_tief(s):
        # Was hochgestellt werden darf: {…} · ein Vorzeichen mit Ziffern ·
        # ein Platzhalter (dort steckt eine Farbgruppe) · ein einzelnes
        # Zeichen. Ohne die mittleren beiden blieb «10^-6» und «10^{3:4}»
        # als roher Text mit Dach stehen.
        stelle = r"(\{[^}]*\}|[-\u2212]?\d+|[\uE000-\uE1FF]|\w)"

        def setzen(tag):
            def f(m):
                inhalt = m.group(1).strip("{}").replace("-", "\u2212")
                return "<%s>%s</%s>" % (tag, inhalt, tag)
            return f

        s = re.sub(r"\^" + stelle, setzen("sup"), s)
        s = re.sub(r"_" + stelle, setzen("sub"), s)
        return s

    def variablen(s):
        # einzelne lateinische Buchstaben kursiv, ausserhalb von Tags
        teile = re.split(r"(<[^>]*>)", s)
        for i, p in enumerate(teile):
            if p.startswith("<"):
                continue
            teile[i] = re.sub(r"(?<![A-Za-zÄÖÜäöü])([a-z])(?![A-Za-zÄÖÜäöü])",
                              r"<i>\1</i>", p)
        return "".join(teile)

    def stueck(s):
        return variablen(hoch_tief(zeichen(s)))

    # `ax` — zusammengeschriebenes Variablenprodukt kursiv setzen. Die
    # Automatik unten erwischt nur einzelne Buchstaben, sonst würde aus
    # «kgV» ein «kgV» in Kursiv und aus «wahre Aussage» ein Buchstabensalat.
    kursiv = []

    def merken_kursiv(m):
        kursiv.append(m.group(1))
        return chr(0xE080 + len(kursiv) - 1)

    t = re.sub(r"`([^`]*)`", merken_kursiv, t)

    # #m# — aufrecht stehen lassen. Einheiten sind keine Variablen: «1 m»
    # und «20 a» gehören aufrecht, das a einer Seitenlänge kursiv.
    aufrecht = []

    def merken_aufrecht(m):
        aufrecht.append(m.group(1))
        return chr(0xE0C0 + len(aufrecht) - 1)

    t = re.sub(r"#([^#]*)#", merken_aufrecht, t)

    # "36" — Überstrich über der Periode: 0."36" ist 0.363636…  Bewusst
    # nicht ~…~: das Zeichen heisst im Fliesstext schon «gedämpft», und
    # zwei Bedeutungen für dasselbe Zeichen sind eine Falle.
    strich = []

    def merken_strich(m):
        strich.append(m.group(1))
        return chr(0xE140 + len(strich) - 1)

    t = re.sub(r'"([^"]*)"', merken_strich, t)

    # Didaktische Einfärbung {1:...} zuerst herausnehmen, damit die
    # Zeichenersetzung sie nicht zerlegt. Platzhalter aus der privaten
    # Unicode-Zone werden von keiner der folgenden Regeln angefasst.
    farbig = []

    def merken(m):
        farbig.append((m.group(1), m.group(2)))
        return chr(0xE000 + len(farbig) - 1)

    while True:
        neu_t = re.sub(r"\{([1-4]):([^{}]*)\}", merken, t, count=1)
        if neu_t == t:
            break
        t = neu_t

    # Brüche zuerst, sie enthalten eigene Teilausdrücke
    aus = []
    rest = t
    while True:
        m = re.search(r"\[([^\[\]|]*)\|([^\[\]|]*)\]", rest)
        if not m:
            aus.append(stueck(rest))
            break
        aus.append(stueck(rest[:m.start()]))
        aus.append('<span class="fr"><span>' + stueck(m.group(1))
                   + '</span><span>' + stueck(m.group(2)) + '</span></span>')
        rest = rest[m.end():]
    ergebnis = "".join(aus)
    for i, (nr, inhalt) in enumerate(farbig):
        ergebnis = ergebnis.replace(
            chr(0xE000 + i), '<span class="f%s">%s</span>' % (nr, formel(inhalt)))
    for i, inhalt in enumerate(kursiv):
        ergebnis = ergebnis.replace(chr(0xE080 + i), "<i>" + formel(inhalt) + "</i>")
    for i, inhalt in enumerate(strich):
        ergebnis = ergebnis.replace(
            chr(0xE140 + i), '<span class="ov">' + formel(inhalt) + "</span>")
    for i, inhalt in enumerate(aufrecht):
        # bewusst ohne variablen(): genau darum geht es hier
        ergebnis = ergebnis.replace(chr(0xE0C0 + i), hoch_tief(zeichen(inhalt)))
    return ergebnis


def entschaerfen(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text_html(s):
    """Fliesstext: Zeilenumbruch mit |, Formelteile in @...@ .

    Die Formelteile werden zuerst herausgenommen. Täte man es später, hätte
    die HTML-Maskierung aus «<=» längst ein «&lt;=» gemacht, und der
    Formelsatz erkennt das Zeichen nicht mehr. Nebenbei darf so auch ein
    senkrechter Strich in einer eingebetteten Formel stehen, ohne dass er
    zum Zeilenumbruch wird.
    """
    formeln = []

    def merken(m):
        formeln.append(m.group(1))
        return chr(0xE100 + len(formeln) - 1)

    s = re.sub(r"@([^@]*)@", merken, s)
    s = entschaerfen(s).replace("|", "<br>")
    s = re.sub(r"~([^~]*)~", r'<span class="dim">\1</span>', s)
    s = re.sub(r"\{([1-4]):([^{}]*)\}",
               lambda m: '<span class="f%s">%s</span>' % (m.group(1), m.group(2)), s)
    for i, f in enumerate(formeln):
        s = s.replace(chr(0xE100 + i), formel(f))
    return s


# ---------------------------------------------------------------- Koordinatenbild
def graf_svg(el, theme):
    """Kleines Koordinatensystem mit Geraden und Punkten, als SVG.

    Nur so viel, wie ein Clip braucht: Achsen mit Teilung, Geraden ueber
    Steigung und Achsenabschnitt (oder zwei Punkte) und markierte Punkte
    mit Beschriftung. Kein Diagrammwerkzeug — wer mehr will, zeichnet die
    Figur wie auf den Themenseiten in physiklib.js.

    Die Geraden werden am Fenster abgeschnitten, nicht an ihren Endpunkten:
    eine Gerade, die aus dem Bild laeuft, soll am Rand aufhoeren und nicht
    an einer willkuerlichen Stelle davor.
    """
    b = el.get("breite", 760)
    h = el.get("hoehe", 560)
    x0, x1 = el.get("xbereich", [-1, 6])
    y0, y1 = el.get("ybereich", [-1, 8])
    fv = theme.get("farben", ["#1F6FB2", "#C2621C", "#2C7A58", "#8A4BA0"])
    tinte, papier = theme["tinte"], theme["papier"]
    rand = 8

    def px(x):
        return rand + (x - x0) / (x1 - x0) * (b - 2 * rand)

    def py(y):
        return h - rand - (y - y0) / (y1 - y0) * (h - 2 * rand)

    teile = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (b, h, b, h)]

    # Karo
    if el.get("raster", True):
        for x in range(int(math.ceil(x0)), int(math.floor(x1)) + 1):
            teile.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d" stroke="%s" '
                         'stroke-opacity=".13" stroke-width="1.5"/>' % (px(x), px(x), h, tinte))
        for y in range(int(math.ceil(y0)), int(math.floor(y1)) + 1):
            teile.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                         'stroke-opacity=".13" stroke-width="1.5"/>' % (py(y), b, py(y), tinte))

    # Achsen mit Pfeil und Beschriftung
    teile.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="3"/>'
                 % (py(0), b, py(0), tinte))
    teile.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="0" stroke="%s" stroke-width="3"/>'
                 % (px(0), h, px(0), tinte))
    teile.append('<text x="%.1f" y="%.1f" font-size="26" font-style="italic" fill="%s">x</text>'
                 % (b - 26, py(0) - 14, tinte))
    teile.append('<text x="%.1f" y="26" font-size="26" font-style="italic" fill="%s">y</text>'
                 % (px(0) + 14, tinte))
    for x in range(int(math.ceil(x0)), int(math.floor(x1)) + 1):
        if x == 0:
            continue
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                     % (px(x), py(0) - 7, px(x), py(0) + 7, tinte))
        teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="middle" fill="%s" '
                     'fill-opacity=".75">%s</text>'
                     % (px(x), py(0) + 32, tinte, str(x).replace("-", "\u2212")))
    for y in range(int(math.ceil(y0)), int(math.floor(y1)) + 1):
        if y == 0:
            continue
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                     % (px(0) - 7, py(y), px(0) + 7, py(y), tinte))
        teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="end" fill="%s" '
                     'fill-opacity=".75">%s</text>'
                     % (px(0) - 13, py(y) + 8, tinte, str(y).replace("-", "\u2212")))

    # Geraden y = m x + q, am Fenster abgeschnitten
    for g in el.get("geraden", []):
        m, q = g["m"], g["q"]
        punkte = []
        for x in (x0, x1):
            y = m * x + q
            if y0 - 1e-9 <= y <= y1 + 1e-9:
                punkte.append((x, y))
        if abs(m) > 1e-9:
            for y in (y0, y1):
                x = (y - q) / m
                if x0 - 1e-9 <= x <= x1 + 1e-9:
                    punkte.append((x, y))
        if len(punkte) < 2:
            continue
        punkte.sort()
        (ax, ay), (bx, by) = punkte[0], punkte[-1]
        farbe = fv[g.get("farbe", 1) - 1]
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="%s" stroke-linecap="round" %s/>'
                     % (px(ax), py(ay), px(bx), py(by), farbe, g.get("dicke", 5),
                        'stroke-dasharray="14 10"' if g.get("gestrichelt") else ""))
        if g.get("beschriftung"):
            bx_, by_ = g.get("beschriftung_bei", [bx, by])
            teile.append('<text x="%.1f" y="%.1f" font-size="27" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (px(bx_), py(by_), farbe, g.get("anker", "start"),
                            entschaerfen(g["beschriftung"])))

    # Parabeln y = a x^2 + b x + c, als Streckenzug im Fenster
    for pa in el.get("parabeln", []):
        a_, b_, c_ = pa["a"], pa.get("b", 0), pa.get("c", 0)
        stuecke, lauf = [], []
        n = 240
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            y = a_ * x * x + b_ * x + c_
            if y0 <= y <= y1:
                lauf.append("%.1f,%.1f" % (px(x), py(y)))
            elif lauf:
                stuecke.append(lauf); lauf = []
        if lauf:
            stuecke.append(lauf)
        farbe = fv[pa.get("farbe", 1) - 1]
        for st in stuecke:
            if len(st) > 1:
                teile.append('<polyline points="%s" fill="none" stroke="%s" '
                             'stroke-width="%s" stroke-linecap="round" '
                             'stroke-linejoin="round" %s/>'
                             % (" ".join(st), farbe, pa.get("dicke", 5),
                                'stroke-dasharray="14 10"' if pa.get("gestrichelt") else ""))
        if pa.get("beschriftung"):
            bx_, by_ = pa["beschriftung_bei"]
            teile.append('<text x="%.1f" y="%.1f" font-size="27" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (px(bx_), py(by_), farbe, pa.get("anker", "start"),
                            entschaerfen(pa["beschriftung"])))

    # Punkte
    for pt in el.get("punkte", []):
        farbe = fv[pt.get("farbe", 3) - 1]
        teile.append('<circle cx="%.1f" cy="%.1f" r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                     % (px(pt["x"]), py(pt["y"]), papier, farbe))
        teile.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>'
                     % (px(pt["x"]), py(pt["y"]), farbe))
        if pt.get("beschriftung"):
            teile.append('<text x="%.1f" y="%.1f" font-size="29" font-weight="600" fill="%s">%s</text>'
                         % (px(pt["x"]) + 18, py(pt["y"]) - 16, farbe,
                            entschaerfen(pt["beschriftung"])))
    teile.append("</svg>")
    return "".join(teile)


# ---------------------------------------------------------------- Elemente
def element_html(el, theme):
    typ = el.get("typ", "text")
    stil = []
    klassen = ["l"]

    if typ == "titel":
        klassen += ["hand", "mitte"]
        stil.append("font-size:%dpx;font-weight:600;color:var(--tinte)" % el.get("groesse", 132))
        inhalt = text_html(el["text"])
    elif typ == "untertitel":
        klassen += ["sans", "mitte"]
        stil.append("font-size:%dpx;color:var(--blau)" % el.get("groesse", 48))
        inhalt = text_html(el["text"])
    elif typ == "aussage":
        klassen += ["m", "mitte"]
        stil.append("font-size:%dpx;font-weight:600" % el.get("groesse", 116))
        inhalt = text_html(el["text"])
    elif typ == "formel":
        klassen += ["m", "row"]
        stil.append("font-size:%dpx" % el.get("groesse", 56))
        if el.get("fett"):
            stil.append("font-weight:600")
        inhalt = "<span>" + formel(el["text"]) + "</span>"
    elif typ == "text":
        klassen += ["m"]
        stil.append("font-size:%dpx" % el.get("groesse", 50))
        inhalt = text_html(el["text"])
    elif typ == "notiz":
        klassen += ["hand"]
        farbe = {"rot": "var(--rot)", "blau": "var(--blau)",
                 "tinte": "var(--tinte)", "gruen": "var(--gruen)"}.get(el.get("farbe", "blau"))
        stil.append("font-size:%dpx;color:%s" % (el.get("groesse", 50), farbe))
        inhalt = text_html(el["text"])
    elif typ == "karte":
        klassen += ["m", "huelle"]
        stil.append("font-size:%dpx" % el.get("groesse", 42))
        inhalt = '<span class="karte row"><span>' + formel(el["text"]) + "</span></span>"
    elif typ == "box":
        klassen += ["m", "huelle"]
        kl = "box row" + (" boxg" if el.get("farbe") == "gruen" else "")
        stil.append("font-size:%dpx;font-weight:600" % el.get("groesse", 58))
        inhalt = '<span class="%s"><span>%s</span></span>' % (kl, formel(el["text"]))
    elif typ == "liste":
        klassen += ["sans"]
        stil.append("font-size:%dpx" % el.get("groesse", 50))
        zeilen = []
        for i, z in enumerate(el["punkte"], 1):
            zeilen.append('<div class="lz"><span class="ln">%d</span>%s</div>'
                          % (i, text_html(z)))
        inhalt = "".join(zeilen)
    elif typ == "graf":
        klassen += ["graf"]
        inhalt = graf_svg(el, theme)
    elif typ == "strich":
        klassen += ["strich"]
        stil.append("width:%dpx" % el.get("breite", 760))
        inhalt = ""
    else:
        raise SystemExit("Unbekannter Elementtyp: %s" % typ)

    return klassen, stil, inhalt


# ---------------------------------------------------------------- Zeitplanung
def szenen_planen(dreh):
    takt = dreh.get("takt", STD["takt"])
    nachlauf = dreh.get("nachlauf", STD["nachlauf"])
    tempo = dreh.get("sprechtempo", STD["sprechtempo"])
    t = 0.0
    plan = []
    for si, sz in enumerate(dreh["szenen"]):
        start = t
        letzte = 0.0
        eintritte = []
        for i, el in enumerate(sz.get("elemente", [])):
            ein = el.get("ein", STD["vorlauf"] + i * takt)
            eintritte.append(ein)
            letzte = max(letzte, ein)
        dauer = sz.get("dauer")
        if dauer is None:
            dauer = letzte + nachlauf
            sprech = sz.get("sprecher")
            if sprech:
                noetig = len(sprech.split()) / tempo + 1.4
                dauer = max(dauer, noetig)
            dauer = max(dauer, 3.0)
        plan.append({"start": start, "dauer": dauer, "eintritte": eintritte, "sz": sz})
        t += dauer
    return plan, t


# ---------------------------------------------------------------- HTML
def schriften_einbetten():
    """Alle woff2 aus schriften/ als data:-URL in @font-face-Regeln giessen."""
    import base64
    css = open(os.path.join(WURZEL, "schriften.css"), encoding="utf-8").read()
    # Nur latin und nur die drei Familien, die ein Clip benutzt — sonst
    # schleppt die Datei Kyrillisch und JetBrains Mono mit.
    regeln = [r for r in re.findall(r"@font-face\{[^}]*\}", css)
              if "-latin-" in r and "latin-ext" not in r
              and ("Source Serif 4" in r or "Source Sans 3" in r or "Caveat" in r)
              and not ("Source Sans 3" in r and "italic" in r)]
    css = "\n".join(regeln)
    def ersetzen(m):
        pfad = os.path.join(WURZEL, m.group(1))
        roh = base64.b64encode(open(pfad, "rb").read()).decode()
        return "url(data:font/woff2;base64,%s)" % roh
    return re.sub(r"url\((schriften/[^)]+\.woff2)\)", ersetzen, css)


def bauen(quelle, eigenstaendig=False):
    dreh = json.load(open(quelle, encoding="utf-8"))
    global LATEX
    LATEX = bool(dreh.get("latex", True))
    theme_name = dreh.get("theme", STD["theme"])
    theme = json.load(open(os.path.join(CLIPS, "themes", theme_name + ".json"), encoding="utf-8"))
    if eigenstaendig:
        fonts_css = schriften_einbetten()
    else:
        fonts_css = '@import url("../schriften.css");' 

    plan, gesamt = szenen_planen(dreh)
    schiene = dreh.get("schiene", [])

    # Tonspur, falls scripts/build-clip-ton.py eine erzeugt hat. Der Clip
    # laeuft ohne genauso; der Ton ist eine Zutat, keine Voraussetzung.
    tonname = (dreh.get("dateiname") or
               os.path.splitext(os.path.basename(quelle))[0]) + ".mp3"
    tonpfad = os.path.join(CLIPS, "ton", tonname)
    if not os.path.exists(tonpfad):
        ton_html = ""
    elif eigenstaendig:
        import base64
        roh = base64.b64encode(open(tonpfad, "rb").read()).decode("ascii")
        ton_html = ('<audio id="ton" preload="auto" '
                    'src="data:audio/mpeg;base64,%s"></audio>' % roh)
    else:
        ton_html = ('<audio id="ton" preload="auto" src="ton/%s"></audio>'
                    % tonname)

    teile = []          # HTML-Schnipsel
    sprecher = []       # Sprechertexte mit Zeitpunkt

    # --- Kopf- und Fusszeile: immer sichtbar
    marke = dreh.get("marke", "begreifbar.ch")
    bereich = dreh.get("themenbereich", "")
    autor = dreh.get("autor", "Raphael Arnold Kohler")
    datum = dreh.get("datum") or date.today().strftime("%d.%m.%Y")
    if re.match(r"^\d{4}-\d{2}-\d{2}$", datum):
        j, m_, t_ = datum.split("-")
        datum = f"{t_}.{m_}.{j}"

    teile.append(
        f'<div id="kopf"><span class="marke">{entschaerfen(marke)}</span>'
        f'<span class="bereich">{entschaerfen(bereich)}</span></div>')
    teile.append(
        f'<div id="fuss"><span>{entschaerfen(autor)}</span>'
        f'<span>{entschaerfen(datum)}</span></div>')

    # --- Schiene (Merkweg) wird einmal gebaut, Sichtbarkeit über die Szenen
    schienen_szenen = [p for p in plan if p["sz"].get("schritt")]
    if schiene and schienen_szenen:
        von = schienen_szenen[0]["start"]
        bis = schienen_szenen[-1]["start"] + schienen_szenen[-1]["dauer"]
        eintraege = []
        for i, s in enumerate(schiene, 1):
            # Zeitpunkt, ab dem dieser Schritt sichtbar ist
            erste = next((p for p in schienen_szenen if p["sz"]["schritt"] >= i), None)
            ein = erste["start"] + 0.3 if erste else von
            aktiv = [p for p in schienen_szenen if p["sz"].get("schritt") == i]
            dim = ""
            if aktiv:
                a0 = aktiv[0]["start"]
                a1 = aktiv[-1]["start"] + aktiv[-1]["dauer"]
                dim = f' data-dim="{a0:.2f},{a1:.2f}"'
            eintraege.append(
                f'<div class="step l flow" data-at="{ein:.2f}" data-anim="rise"{dim}>'
                f'<div class="num">{i}</div><div class="stxt">{text_html(s)}</div></div>')
        teile.append(
            f'<div class="l" data-at="{von:.2f}" data-out="{bis:.2f}" data-anim="fade" '
            f'style="left:130px;top:296px;width:470px">' + "".join(eintraege) + '</div>')

    # --- Szenen
    for p in plan:
        sz, start, dauer = p["sz"], p["start"], p["dauer"]
        layout = sz.get("layout", "zentriert")
        ende = start + dauer
        if sz.get("sprecher"):
            sprecher.append({"bei": round(start + sz.get("sprecher_bei", 0.4), 2),
                             "text": sz["sprecher"]})

        # Grundraster
        if layout == "schiene":
            links, breite, oben, abstand = 680, 1140, 168, 112
            mitte = False
        else:
            links, breite, oben, abstand = 130, 1660, 230, 118
            mitte = True

        y = sz.get("oben", oben)
        for i, el in enumerate(sz.get("elemente", [])):
            klassen, stil, inhalt = element_html(el, theme)
            ein = start + p["eintritte"][i]
            h = el.get("halten")
            if h is True:
                aus = None
            elif isinstance(h, str):
                ziel_sz = next((q for q in plan if q["sz"].get("name") == h), None)
                if ziel_sz is None:
                    raise SystemExit("halten verweist auf unbekannte Szene: %s" % h)
                aus = ziel_sz["start"] + ziel_sz["dauer"]
            else:
                aus = ende
            anim = el.get("anim", "pop" if el.get("typ") in ("box", "aussage") else "rise")

            if mitte and "x" not in el:
                klassen.append("mitte")
                stil.insert(0, "left:0;right:0;text-align:center")
            else:
                stil.insert(0, "left:%dpx" % el.get("x", links))
            stil.insert(1, "top:%dpx" % el.get("y", y))

            hoehe = el.get("hoehe", int(el.get("groesse", 50) * 1.5) + 40)
            y = el.get("y", y) + el.get("abstand", max(abstand, hoehe))

            attr = f' data-at="{ein:.2f}"'
            if aus is not None:
                attr += f' data-out="{aus:.2f}"'
            attr += f' data-anim="{anim}"'
            teile.append(f'<div class="{" ".join(klassen)}"{attr} '
                         f'style="{";".join(stil)}">{inhalt}</div>')

    karo = ""
    if theme.get("karo"):
        k = theme.get("karo_farbe", "rgba(43,95,140,.12)")
        karo = ("background-image:repeating-linear-gradient(to right,%s 0 1.5px,transparent 1.5px 60px),"
                "repeating-linear-gradient(to bottom,%s 0 1.5px,transparent 1.5px 60px);" % (k, k))
    rand = ""
    if theme.get("rand"):
        rand = ('<div id="rand" style="background:%s"></div>'
                % theme.get("rand_farbe", "rgba(191,59,43,.26)"))

    fv = theme.get("farben", ["#1F6FB2", "#C2621C", "#2C7A58", "#8A4BA0"])
    fl = theme.get("flaechen", ["rgba(31,111,178,.12)", "rgba(194,98,28,.13)",
                                "rgba(44,122,88,.12)", "rgba(138,75,160,.12)"])
    didaktik = ";".join("--f%d:%s;--f%dw:%s" % (i + 1, fv[i], i + 1, fl[i])
                        for i in range(4))

    # Im LaTeX-Versuch setzt MathJax. Die vier Farbmakros bilden die
    # Farbgruppen der eigenen Schreibweise nach — gleiche Werte, damit der
    # Vergleich der beiden Fassungen einer ueber die Gestaltung ist und
    # nicht einer ueber die Palette.
    mathjax = ""
    if LATEX:
        # Das Doppelkreuz einer Farbe muss verdoppelt werden: In einer
        # Makrodefinition ist #1 der Parameter, und «#1a4f8a» liest TeX
        # als «Parameter 1, dann a4f8a» — Fehlermeldung statt Formel.
        makros = ",".join(
            "%s:['\\\\bbox[%s,3px]{\\\\textcolor{%s}{#1}}',1]"
            % (n, fl[i].replace("#", "##"), fv[i].replace("#", "##"))
            for i, n in enumerate(["fa", "fb", "fc", "fd"]))
        mathjax = (
            "<script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],"
            "displayMath:[],macros:{%s}},svg:{fontCache:'global'},"
            "options:{enableMenu:false}};</script>"
            "<script src=\"../vendor/mathjax/tex-svg.js\"></script>" % makros)

    html = VORLAGE.format(
        mathjax=mathjax,
        didaktik=didaktik,
        titel=entschaerfen(dreh.get("titel", "Clip")),
        fonts=fonts_css,
        papier=theme["papier"], tinte=theme["tinte"], blau=theme["blau"],
        rot=theme["rot"], gruen=theme["gruen"], gold=theme.get("gold", "#E0A32E"),
        karte_bg=theme.get("karte", "rgba(255,255,255,.66)"),
        box_bg=theme.get("box", "rgba(255,255,255,.6)"),
        vignette=theme.get("vignette", "rgba(90,70,40,.10)"),
        karo=karo, rand=rand, ton=ton_html,
        dauer=round(gesamt, 2),
        inhalt="\n".join(teile),
        sprecher=json.dumps(sprecher, ensure_ascii=False),
    )

    name = dreh.get("dateiname") or os.path.splitext(os.path.basename(quelle))[0]
    if eigenstaendig:
        name += "-eigenstaendig"
    ziel = os.path.join(CLIPS, name + ".html")
    open(ziel, "w", encoding="utf-8").write(html)

    print(f"{ziel}")
    print(f"  {len(plan)} Szenen, {gesamt:.1f} s, {len(sprecher)} Sprechertexte")
    for i, p in enumerate(plan, 1):
        print(f"  {i:2d}  {p['start']:6.1f}–{p['start']+p['dauer']:6.1f}s  "
              f"{p['sz'].get('name','')}")

    # Sprechertexte als Skript herausschreiben — Grundlage für die Vertonung
    if sprecher:
        with open(os.path.join(CLIPS, "sprechertext-" + name + ".txt"), "w",
                  encoding="utf-8") as f:
            for s in sprecher:
                f.write(f"{s['bei']:.2f}\t{s['text']}\n")

    return ziel, dreh, gesamt




VORLAGE = r"""<!DOCTYPE html>
<html lang="de-CH"><head><meta charset="utf-8"><title>{titel}</title><style>
{fonts}
:root{{--papier:{papier};--tinte:{tinte};--blau:{blau};--rot:{rot};--gruen:{gruen};--gold:{gold};{didaktik}}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;background:#0d1418;overflow:hidden}}
#wrap{{position:absolute;left:0;right:0;top:0;bottom:60px;overflow:hidden}}
:fullscreen #wrap{{bottom:0}} :fullscreen #ui{{display:none}}
#stage{{width:1920px;height:1080px;position:absolute;left:50%;top:50%;overflow:hidden;
 background:var(--papier);color:var(--tinte);font-family:'Source Serif 4',Georgia,serif;transform-origin:center center}}
body.render #wrap{{bottom:0}} body.render #stage{{left:0;top:0;transform:none!important}}
#stage::before{{content:"";position:absolute;inset:0;pointer-events:none;{karo}}}
#stage::after{{content:"";position:absolute;inset:0;pointer-events:none;
 background:radial-gradient(120% 100% at 50% 40%,rgba(255,255,255,0) 55%,{vignette} 100%)}}
#rand{{position:absolute;left:76px;top:0;bottom:0;width:3px}}

#kopf,#fuss{{position:absolute;left:130px;right:100px;display:flex;justify-content:space-between;
 align-items:baseline;font-family:'Source Sans 3',sans-serif;z-index:5}}
#kopf{{top:46px;font-size:27px}}
#kopf .marke{{font-weight:600;letter-spacing:.01em;color:var(--blau)}}
#kopf .bereich{{color:var(--tinte);opacity:.55;letter-spacing:.07em;text-transform:uppercase;font-size:22px}}
#fuss{{bottom:44px;font-size:21px;color:var(--tinte);opacity:.42}}

.l{{position:absolute;will-change:opacity,transform}}
.l.flow{{position:relative}}
.m{{font-family:'Source Serif 4',Georgia,serif}} .m i,i{{font-style:italic}}
.hand{{font-family:'Caveat',cursive;line-height:1.24}}
.sans{{font-family:'Source Sans 3',system-ui,sans-serif}}
.huelle{{display:flex;justify-content:flex-start}}
.mitte.huelle{{justify-content:center}}
.huelle>span{{white-space:nowrap}}
.f1,.f2,.f3,.f4{{border-radius:7px;padding:0 .14em;margin:0 .02em}}
.f1{{color:var(--f1);background:var(--f1w)}}
.f2{{color:var(--f2);background:var(--f2w)}}
.f3{{color:var(--f3);background:var(--f3w)}}
.f4{{color:var(--f4);background:var(--f4w)}}
.dim{{opacity:.62}}
.graf{{line-height:0}}
.graf svg{{display:inline-block;vertical-align:top}}
.ov{{display:inline-block;line-height:1;padding-top:.07em;margin-top:.12em;border-top:3.5px solid currentColor}}
.row{{display:flex;align-items:center;line-height:1.06;white-space:nowrap;gap:.26em}}
.mitte.row{{justify-content:center}}
.fr{{position:relative;z-index:1;display:inline-flex;flex-direction:column;align-items:center;
 line-height:1.08;margin:0 .12em;vertical-align:middle}}
.fr>span:first-child{{padding:0 .32em .07em}}
.fr>span:last-child{{padding:.20em .32em 0;border-top:3.5px solid currentColor}}
.box{{border:3.5px solid var(--tinte);border-radius:14px;padding:12px 30px;background:{box_bg}}}
.boxg{{border-color:var(--gruen);color:var(--gruen)}}
.karte{{background:{karte_bg};border:2.5px solid rgba(128,128,128,.28);border-radius:16px;padding:14px 26px}}
.strich{{height:5px;background:var(--rot);border-radius:3px;transform-origin:left center}}
.lz{{display:flex;align-items:baseline;gap:22px;margin-bottom:26px}}
.ln{{color:var(--blau);font-weight:600;min-width:34px}}
.step{{display:flex;align-items:flex-start;gap:18px;margin-bottom:34px}}
.num{{flex:0 0 auto;width:56px;height:56px;border-radius:50%;background:var(--blau);color:var(--papier);
 font-family:'Source Sans 3',sans-serif;font-weight:600;font-size:31px;display:grid;place-items:center}}
.stxt{{font-family:'Source Sans 3',sans-serif;font-size:31px;line-height:1.24;padding-top:7px}}

#ui{{position:absolute;left:0;right:0;bottom:0;height:60px;display:flex;align-items:center;gap:18px;
 padding:0 26px;background:rgba(13,20,24,.85);color:#e8eef2;font-family:system-ui,sans-serif;font-size:14px;z-index:99}}
body.render #ui{{display:none}}
#bar{{flex:1;height:8px;background:rgba(255,255,255,.18);border-radius:4px;overflow:hidden;cursor:pointer}}
#barf{{height:100%;width:0;background:var(--gold)}}
#ui button{{background:rgba(255,255,255,.12);color:#e8eef2;border:0;border-radius:7px;padding:7px 14px;
 font-size:14px;cursor:pointer;white-space:nowrap}}
#tt{{white-space:nowrap;font-variant-numeric:tabular-nums}}
#tip{{opacity:.6;white-space:nowrap}}
/* Auf dem Telefon gibt es weder Leertaste noch Pfeiltasten — der Hinweis
   waere dort nur Text, der die 60px hohe Leiste sprengt. */
@media (max-width:700px){{#ui{{gap:11px;padding:0 12px}} #tip{{display:none}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>{mathjax}</head><body>
<div id="wrap"><div id="stage">
{rand}
{inhalt}
</div></div>
{ton}
<div id="ui">
  <button id="pp">Pause</button>
  <button id="ts" hidden>🔇 Ton an</button>
  <div id="bar"><div id="barf"></div></div>
  <span id="tt">0.0 s</span>
  <span id="tip">Leertaste = Pause &middot; &larr; &rarr; = 5 s &middot; R = Neustart &middot; F = Vollbild</span>
</div>
<script>
const DUR = {dauer};
const SPRECHER = {sprecher};
const stage = document.getElementById('stage');
const layers = [...document.querySelectorAll('.l')].map(el => ({{
  el, at: parseFloat(el.dataset.at || '0'),
  out: el.dataset.out ? parseFloat(el.dataset.out) : Infinity,
  anim: el.dataset.anim || 'fade',
  dim: el.dataset.dim ? el.dataset.dim.split(',').map(Number) : null
}}));
const IN = 0.5, OUT = 0.4;
const ease = p => 1 - Math.pow(1 - p, 3);
const cl = p => p < 0 ? 0 : p > 1 ? 1 : p;
function seek(t)  {{
  for (const L of layers) {{
    const pi = ease(cl((t - L.at) / IN));
    const po = L.out === Infinity ? 0 : ease(cl((t - L.out) / OUT));
    let o = pi * (1 - po), tr = '';
    if (L.anim === 'rise') tr = 'translateY(' + ((1 - pi) * 26) + 'px)';
    else if (L.anim === 'pop') tr = 'scale(' + (0.90 + 0.10 * pi) + ')';
    else if (L.anim === 'wipe') {{ tr = 'scaleX(' + pi + ')'; o = (t >= L.at ? 1 : 0) * (1 - po); }}
    if (L.dim && !(t >= L.dim[0] && t < L.dim[1])) o *= 0.34;
    L.el.style.transform = tr; L.el.style.opacity = o;
  }}
}}
window.__seek = seek;
window.__dauer = DUR;
if (!location.search.includes('render')) {{
  let t0 = performance.now(), playing = true, t = 0;
  const barf = document.getElementById('barf'), tt = document.getElementById('tt'),
        pp = document.getElementById('pp'), wrap = document.getElementById('wrap');
  const fit = () => {{ stage.style.transform = 'translate(-50%,-50%) scale('
      + Math.min(wrap.clientWidth / 1920, wrap.clientHeight / 1080) + ')'; }};
  window.addEventListener('resize', fit);
  document.addEventListener('fullscreenchange', () => setTimeout(fit, 60));
  fit();
  // Der Ton startet stumm mit — stummes Abspielen erlauben die Browser
  // ohne Nutzergeste. Der Klick auf «Ton an» ist die Geste, die ihn
  // hoerbar macht; ab dann fuehrt die Tonspur die Uhr, weil Tondrift
  // auffaellt und Bilddrift nicht.
  const ton = document.getElementById('ton'), ts = document.getElementById('ts');
  if (ton) {{
    ts.hidden = false;
    ton.muted = true;
    ton.play().catch(() => {{}});
    ts.onclick = () => {{
      ton.muted = !ton.muted;
      ts.textContent = ton.muted ? '🔇 Ton an' : '🔊 Ton aus';
      if (!ton.muted) {{ ton.currentTime = t; if (playing) ton.play().catch(() => {{}}); }}
    }};
  }}
  const tonLaeuft = () => ton && !ton.paused && !ton.ended;
  function loop(now) {{
    if (playing) {{
      if (tonLaeuft()) t = ton.currentTime;
      else {{ t += (now - t0) / 1000; if (t > DUR) t = DUR; }}
    }}
    t0 = now; seek(t);
    barf.style.width = (t / DUR * 100) + '%'; tt.textContent = t.toFixed(1) + ' s';
    requestAnimationFrame(loop);
  }}
  requestAnimationFrame(loop);
  const tonAn = () => {{ if (ton) {{ ton.currentTime = t; if (playing) ton.play().catch(() => {{}}); }} }};
  const toggle = () => {{
    playing = !playing;
    pp.textContent = playing ? 'Pause' : 'Play';
    if (ton) {{ if (playing) ton.play().catch(() => {{}}); else ton.pause(); }}
  }};
  pp.onclick = toggle;
  document.addEventListener('keydown', e => {{
    if (e.code === 'Space') {{ e.preventDefault(); toggle(); }}
    if (e.code === 'ArrowRight') {{ t = Math.min(DUR, t + 5); tonAn(); }}
    if (e.code === 'ArrowLeft') {{ t = Math.max(0, t - 5); tonAn(); }}
    const k = e.key.toLowerCase();
    if (k === 'r') {{ t = 0; playing = true; pp.textContent = 'Pause'; tonAn(); }}
    if (k === 'f') document.documentElement.requestFullscreen?.();
  }});
  document.getElementById('bar').onclick = e => {{
    const r = e.currentTarget.getBoundingClientRect();
    t = (e.clientX - r.left) / r.width * DUR; tonAn();
  }};
}} else {{ document.body.classList.add('render'); seek(0); }}
</script></body></html>
"""


def lektionen(dreh):
    """`lektion` darf ein Code oder eine Liste sein — hier immer eine Liste.

    Ein Clip gehoert oft auf mehrere Seiten. Die Bruchgleichung etwa passt
    ins Grundlagenfach unter g2-2b und ins Schwerpunktfach unter s2-2a; ohne
    Liste muesste man ihn duplizieren."""
    v = dreh.get("lektion", [])
    if isinstance(v, str):
        v = [v] if v else []
    return [str(x) for x in v]


def verzeichnis(neue):
    """clips.json fortschreiben — Grundlage fuer die Bibliotheksseite.

    Wichtig: Ein Lauf fuer einen einzelnen Clip darf die uebrigen Eintraege
    nicht wegwerfen. Darum wird der bestehende Index gelesen, die neu
    gebauten Eintraege ersetzen ihre Namensvettern, alles andere bleibt —
    ausser Eintraegen, deren HTML-Datei nicht mehr existiert."""
    ziel = os.path.join(CLIPS, "clips.json")
    bestand = []
    if os.path.exists(ziel):
        try:
            bestand = json.load(open(ziel, encoding="utf-8")).get("clips", [])
        except (ValueError, OSError) as e:
            print(f"  clips.json nicht lesbar ({e}) — wird neu angelegt.")

    frisch = {e["datei"] for e in neue}
    eintraege = list(neue)
    verwaist = 0
    for e in bestand:
        if e.get("datei") in frisch:
            continue
        if not os.path.exists(os.path.join(CLIPS, e.get("datei", ""))):
            verwaist += 1
            continue
        eintraege.append(e)

    eintraege.sort(key=lambda e: (e.get("fach", ""),
                                  (e.get("lektion") or [""])[0],
                                  e["titel"]))
    json.dump({"stand": date.today().isoformat(), "clips": eintraege},
              open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hinweis = f", {verwaist} verwaiste entfernt" if verwaist else ""
    print(f"\n{ziel}  —  {len(eintraege)} Clips "
          f"({len(neue)} neu gebaut{hinweis})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Clip-Generator für physik.begreifbar.ch")
    ap.add_argument("clip", nargs="?", help="einzelnes Drehbuch (ohne .json); ohne Angabe alle")
    ap.add_argument("--eigenstaendig", action="store_true",
                    help="Schriften einbetten — Datei läuft ohne die Site")
    a = ap.parse_args()

    if a.clip:
        quellen = [os.path.join(CLIPS, a.clip.removesuffix(".json") + ".json")]
    else:
        quellen = sorted(g for g in glob.glob(os.path.join(CLIPS, "*.json"))
                         if os.path.basename(g) not in ("clips.json", "vorlage.json"))
    if not quellen:
        sys.exit("Keine Drehbücher in clips/ gefunden.")

    eintraege = []
    for q in quellen:
        ziel, dreh, dauer = bauen(q, a.eigenstaendig)
        # "probe": true — ein Versuchsclip. Er wird gebaut, aber nicht in
        # clips.json aufgenommen und erscheint darum weder in der Bibliothek
        # noch auf einer Lektionsseite.
        if not a.eigenstaendig and not dreh.get("probe"):
            eintraege.append({
                "datei": os.path.basename(ziel),
                "titel": dreh.get("titel", ""),
                "kurzbeschrieb": dreh.get("kurzbeschrieb", ""),
                "fach": dreh.get("fach", ""),
                "lerngebiet": dreh.get("lerngebiet", ""),
                "lektion": lektionen(dreh),
                "themenbereich": dreh.get("themenbereich", ""),
                "reihe": dreh.get("reihe", ""),
                "folge": dreh.get("folge"),
                "stufe": dreh.get("stufe", []),
                "schlagworte": dreh.get("schlagworte", []),
                "dauer_s": round(dauer),
                "datum": dreh.get("datum", ""),
            })
    if eintraege:
        verzeichnis(eintraege)
