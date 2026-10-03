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


# ---------------------------------------------------------------- Boxplot
def boxplot_svg(el, theme):
    """Ein Boxplot aus den fuenf Kennzahlen.

    Die Konvention ist die der Themenseite 4.3: Box von Q1 bis Q3, Strich
    beim Median, Antennen bis zum kleinsten und groessten Wert. Keine
    Ausreisserregel — die Seite kennt keine, und ein Clip soll keine
    einfuehren, die dort nicht steht.
    """
    b = el.get("breite", 1180)
    h = el.get("hoehe", 300)
    fv = theme.get("farben", ["#1F6FB2", "#C2621C", "#2C7A58", "#8A4BA0"])
    tinte = theme.get("tinte", "#20303a")
    papier = theme.get("papier", "#f7f5ef")
    kf = fv[el.get("farbe", 1) - 1]
    fl = theme.get("flaechen", ["rgba(31,111,178,.12)"] * 4)[el.get("farbe", 1) - 1]

    lo, hi = el["min"], el["max"]
    x0 = el.get("von", lo - (hi - lo) * 0.12)
    x1 = el.get("bis", hi + (hi - lo) * 0.12)
    rl, rr = 70, b - 70
    def px(v):
        return rl + (rr - rl) * (v - x0) / (x1 - x0)

    achse_y = h - 62
    box_o, box_u = 44, achse_y - 58
    mitte = (box_o + box_u) / 2

    t = ['<svg width="%d" height="%d" viewBox="0 0 %d %d" '
         'xmlns="http://www.w3.org/2000/svg" font-family="Source Sans 3,sans-serif">'
         % (b, h, b, h)]
    # Achse mit Teilung
    t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>'
             % (rl - 20, achse_y, rr + 20, achse_y, tinte))
    for v in el.get("teilung", []):
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                 % (px(v), achse_y - 9, px(v), achse_y + 9, tinte))
        t.append('<text x="%.1f" y="%.1f" font-size="26" fill="%s" text-anchor="middle" '
                 'opacity=".72">%s</text>' % (px(v), achse_y + 42, tinte, formel_zahl(v)))
    # Antennen
    for a_, e_ in ((lo, el["q1"]), (el["q3"], hi)):
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="4"/>'
                 % (px(a_), mitte, px(e_), mitte, kf))
    for v in (lo, hi):
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5" '
                 'stroke-linecap="round"/>' % (px(v), box_o + 12, px(v), box_u - 12, kf))
    # Box und Median
    t.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" '
             'stroke-width="5" rx="4"/>'
             % (px(el["q1"]), box_o, px(el["q3"]) - px(el["q1"]), box_u - box_o, fl, kf))
    t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="7"/>'
             % (px(el["med"]), box_o, px(el["med"]), box_u, tinte))
    # Beschriftung der fuenf Zahlen
    if el.get("marken", True):
        namen = [(lo, "min"), (el["q1"], "Q1"), (el["med"], "Median"),
                 (el["q3"], "Q3"), (hi, "max")]
        for v, nm in namen:
            t.append('<text x="%.1f" y="%.1f" font-size="25" font-weight="600" fill="%s" '
                     'text-anchor="middle">%s</text>' % (px(v), box_o - 14, kf, nm))
    t.append("</svg>")
    return "".join(t)


def formel_zahl(v):
    """Zahl fuer eine Achsenbeschriftung — Punkt als Trennzeichen, ohne .0."""
    return ("%g" % v)


# ---------------------------------------------------------------- Koordinatenbild
# Was in der Formel eines "kurven"-Eintrags stehen darf. Bewusst knapp:
# Ein Drehbuch beschreibt eine Kurve, es rechnet nicht.
_KURVE_NS = {"sin": math.sin, "cos": math.cos, "tan": math.tan,
             "asin": math.asin, "acos": math.acos, "atan": math.atan,
             "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
             "abs": abs, "pi": math.pi, "e": math.e}


def kurve_wert(formel, x):
    """Wert einer Drehbuch-Formel an der Stelle x, oder None.

    None heisst: hier gibt es keinen Punkt. Der Streckenzug bricht dann ab
    und faengt danach neu an — genau das braucht die Tangenskurve an ihren
    Polstellen, ohne dass im Drehbuch etwas ueber Pole stehen muss.
    """
    try:
        return float(eval(formel, {"__builtins__": {}}, dict(_KURVE_NS, x=x)))
    except Exception:
        return None


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

    # Wo die Achse geteilt wird. Ganze Zahlen sind der Normalfall; wo die
    # x-Achse ein Winkel ist, taugen sie nicht — eine Sinuskurve gehoert bei
    # pi/2 geteilt und nicht bei 1, 2, 3. Darum "xteilung"/"yteilung":
    # Paare [Stelle, Beschriftung], die die ganzen Zahlen ersetzen.
    def teilung(schluessel, a, e):
        eigen = el.get(schluessel)
        if eigen:
            return [(float(w), str(t)) for w, t in eigen]
        return [(float(k), str(k).replace("-", "\u2212"))
                for k in range(int(math.ceil(a)), int(math.floor(e)) + 1)]

    xt = teilung("xteilung", x0, x1)
    yt = teilung("yteilung", y0, y1)

    # Karo
    if el.get("raster", True):
        for x, _ in xt:
            teile.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d" stroke="%s" '
                         'stroke-opacity=".13" stroke-width="1.5"/>' % (px(x), px(x), h, tinte))
        for y, _ in yt:
            teile.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                         'stroke-opacity=".13" stroke-width="1.5"/>' % (py(y), b, py(y), tinte))

    # Achsen mit Pfeil und Beschriftung
    teile.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="3"/>'
                 % (py(0), b, py(0), tinte))
    teile.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="0" stroke="%s" stroke-width="3"/>'
                 % (px(0), h, px(0), tinte))
    # "pfeile": Pfeilspitzen in positiver Richtung; "xname"/"yname": Achsenbeschriftung,
    # bei Anwendungen mit Grösse und Einheit ("x [m]", "A [m²]"). Ohne Angabe bleibt das
    # Bild wie bisher — bestehende Clips bauen Byte für Byte gleich.
    xname, yname = el.get("xname", "x"), el.get("yname", "y")
    achsnamen = []      # benannte Achsen kommen zuletzt, mit Hof — sonst liegt die Kurve darüber
    if el.get("pfeile"):
        teile.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                     % (b, py(0), b - 18, py(0) - 9, b - 18, py(0) + 9, tinte))
        teile.append('<polygon points="%.1f,0 %.1f,18 %.1f,18" fill="%s"/>'
                     % (px(0), px(0) - 9, px(0) + 9, tinte))
    if xname == "x":
        teile.append('<text x="%.1f" y="%.1f" font-size="26" font-style="italic" fill="%s">x</text>'
                     % (b - 26, py(0) - 14, tinte))
    else:
        achsnamen.append('<text x="%.1f" y="%.1f" font-size="26" font-style="italic" fill="%s" '
                         'stroke="%s" stroke-width="10" paint-order="stroke" text-anchor="end">%s</text>'
                         % (b - 8, py(0) - 16, tinte, papier, entschaerfen(xname)))
    if yname == "y":
        teile.append('<text x="%.1f" y="26" font-size="26" font-style="italic" fill="%s">y</text>'
                     % (px(0) + 14, tinte))
    else:
        achsnamen.append('<text x="%.1f" y="26" font-size="26" font-style="italic" fill="%s" '
                         'stroke="%s" stroke-width="10" paint-order="stroke">%s</text>'
                         % (px(0) + 14, tinte, papier, entschaerfen(yname)))
    for x, mark in xt:
        if abs(x) < 1e-9:
            continue
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                     % (px(x), py(0) - 7, px(x), py(0) + 7, tinte))
        teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="middle" fill="%s" '
                     'fill-opacity=".75">%s</text>'
                     % (px(x), py(0) + 32, tinte, entschaerfen(mark)))
    for y, mark in yt:
        if abs(y) < 1e-9:
            continue
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                     % (px(0) - 7, py(y), px(0) + 7, py(y), tinte))
        teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="end" fill="%s" '
                     'fill-opacity=".75">%s</text>'
                     % (px(0) - 13, py(y) + 8, tinte, entschaerfen(mark)))

    # Geraden y = m x + q, am Fenster abgeschnitten
    for nr, g in enumerate(el.get("geraden", [])):
        # "bewegung": [[t, m, q], ...] — eine Gerade, die sich waehrend der Szene
        # bewegt (t ab Szenenbeginn, seit 03.10.2026). Wie bei den Parabeln wird
        # sie erst im Abspieler gezeichnet, aus der Zeit allein; siehe BEWEGUNG_JS.
        if g.get("bewegung"):
            farbe = fv[g.get("farbe", 1) - 1]
            gid = "bewg%d" % nr
            teile.append('<path data-bewg="%s" data-paar="%s" data-fenster="%g,%g,%g,%g,%d,%d,%d" '
                         'fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" %s%s/>'
                         % (entschaerfen(json.dumps(g["bewegung"])), gid, x0, x1, y0, y1, b, h, rand,
                            farbe, g.get("dicke", 5),
                            'stroke-dasharray="14 10"' if g.get("gestrichelt") else "",
                            # "ab": die Gerade beginnt erst bei diesem x (Physik 03.10.2026:
                            # eine Q-t-Gerade hat keinen Teil bei negativer Zeit)
                            ' data-ab="%g"' % g["ab"] if g.get("ab") is not None else ""))

            # Begleiter der bewegten Geraden, alle aus derselben Zeit gerechnet:
            # yachse ((0 | q)), nullstelle ((x_0 | 0)), marken (Punkt an festem x
            # mit Live-Wert), laeufer (Punkt, der auf der Geraden faehrt) und
            # dreieck (Steigungsdreieck ab Stelle x mit Breite dx, mit Delta-Zahlen).
            def g_punkt(klasse, farbe_, attr="", text=True):
                f_ = fv[farbe_ - 1]
                t_ = '<g class="%s" data-zu="%s"%s>' % (klasse, gid, attr)
                t_ += ('<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                       '<circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                if text:
                    t_ += '<text font-size="29" font-weight="600" fill="%s"></text>' % f_
                return t_ + '</g>'
            if g.get("yachse"):
                teile.append(g_punkt("bew-gy", g["yachse"].get("farbe", 2),
                                     text=g["yachse"].get("beschriftung", True) is not False))
            if g.get("nullstelle"):
                teile.append(g_punkt("bew-gn", g["nullstelle"].get("farbe", 3),
                                     text=g["nullstelle"].get("beschriftung", True) is not False))
            for mk in g.get("marken", []):
                teile.append(g_punkt("bew-gm", mk.get("farbe", 5),
                                     ' data-x="%g" data-text="%s"' % (mk["x"], entschaerfen(mk.get("text", "")))))
            lf = g.get("laeufer")
            if lf:
                teile.append(g_punkt("bew-gl", lf.get("farbe", 5),
                                     ' data-bahn="%s" data-text="%s"'
                                     % (entschaerfen(json.dumps(lf["bahn"])), entschaerfen(lf.get("text", "")))))
            dr = g.get("dreieck")
            if dr:
                f_ = fv[dr.get("farbe", 5) - 1]
                # Feste Stelle und Breite — oder "bahn": [[t, x, dx], ...], dann wandert
                # und waechst das Dreieck waehrend der Szene mit.
                if dr.get("bahn"):
                    teile.append('<g class="bew-gd" data-zu="%s" data-bahn="%s">'
                                 '<path class="bew-gd-w" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                                 '<path class="bew-gd-s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                                 '<text class="bew-gd-tx" font-size="27" font-weight="600" fill="%s" text-anchor="middle"></text>'
                                 '<text class="bew-gd-ty" font-size="27" font-weight="600" fill="%s"></text>'
                                 '</g>' % (gid, entschaerfen(json.dumps(dr["bahn"])), f_, f_, f_, f_))
                    continue
                teile.append('<g class="bew-gd" data-zu="%s" data-x="%g" data-dx="%g">'
                             '<path class="bew-gd-w" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                             '<path class="bew-gd-s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                             '<text class="bew-gd-tx" font-size="27" font-weight="600" fill="%s" text-anchor="middle"></text>'
                             '<text class="bew-gd-ty" font-size="27" font-weight="600" fill="%s"></text>'
                             '</g>' % (gid, dr["x"], dr["dx"], f_, f_, f_, f_))
            continue
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
    for nr, pa in enumerate(el.get("parabeln", [])):
        # "bewegung": [[t, a, u, v], ...] — eine Parabel in Scheitelform, die
        # sich waehrend der Szene bewegt (t ab Szenenbeginn). Gezeichnet wird
        # sie erst im Abspieler, aus der Zeit allein: Pause, Spulen und die
        # Pruefbilder bleiben so richtig. Siehe BEWEGUNG_JS.
        if pa.get("bewegung"):
            farbe = fv[pa.get("farbe", 1) - 1]
            bid = "bew%d" % nr
            teile.append('<path data-bew="%s" data-paar="%s" data-fenster="%g,%g,%g,%g,%d,%d,%d" '
                         'fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
                         'stroke-linejoin="round" %s/>'
                         % (entschaerfen(json.dumps(pa["bewegung"])), bid, x0, x1, y0, y1, b, h, rand,
                            farbe, pa.get("dicke", 5),
                            'stroke-dasharray="14 10"' if pa.get("gestrichelt") else ""))
            # Begleiter der bewegten Parabel, alle aus derselben Zeit gerechnet:
            # scheitel (mit "S(u | v)"), nullstellen, yachse, marken (Punkt an
            # festem x mit Live-Wert) und laeufer (Punkt, der auf der Kurve
            # faehrt; "spiegel" zeigt den Partner bei 2u - x).
            def punkt_g(klasse, farbe, attr="", geist=False, text=True):
                f_ = fv[farbe - 1]
                g = '<g class="%s" data-zu="%s"%s>' % (klasse, bid, attr)
                if geist:
                    g += ('<g class="bew-geist" opacity=".35"><circle r="11" fill="%s" stroke="%s" '
                          'stroke-width="3.5"/><circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                g += ('<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                      '<circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                if text:
                    g += '<text font-size="29" font-weight="600" fill="%s"></text>' % f_
                return g + '</g>'
            if pa.get("scheitel"):
                teile.append(punkt_g("bew-s", pa["scheitel"].get("farbe", 3)))
            if pa.get("nullstellen"):
                f_ = pa["nullstellen"].get("farbe", 2)
                mit = bool(pa["nullstellen"].get("beschriftung"))   # «(x | 0)» an den Nullstellen
                teile.append(punkt_g("bew-n bew-n1", f_, text=mit))
                teile.append(punkt_g("bew-n bew-n2", f_, text=mit))
            if pa.get("yachse"):
                teile.append(punkt_g("bew-y", pa["yachse"].get("farbe", 1)))
            for m in pa.get("marken", []):
                teile.append(punkt_g("bew-m", m.get("farbe", 4),
                                     ' data-x="%g" data-text="%s"' % (m["x"], entschaerfen(m.get("text", "")))))
            lf = pa.get("laeufer")
            if lf:
                teile.append(punkt_g("bew-l", lf.get("farbe", 2),
                                     ' data-bahn="%s" data-text="%s"' % (entschaerfen(json.dumps(lf["bahn"])),
                                                                         entschaerfen(lf.get("text", ""))),
                                     geist=bool(lf.get("spiegel"))))
            continue
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

    # Kurven y = f(x), als Streckenzug im Fenster. Wie die Parabeln, nur
    # mit freier Formel — und mit dem Zusatz, dass ein Stueck auch dann
    # abbricht, wenn f an einer Stelle gar nicht definiert ist. Genau daran
    # entstehen die Luecken der Tangenskurve an ihren Polstellen.
    for kv in el.get("kurven", []):
        n = kv.get("n", 480)
        # Eine Kurve darf auch nur ein Stueck des Fensters belegen. Gebraucht
        # wird das fuer Hilfslinien wie die Mittellinie einer Schwingung: Ohne
        # Grenze laeuft sie ueber die Achsenbeschriftung am linken Rand.
        a_ = kv.get("von", x0)
        e_ = kv.get("bis", x1)
        stuecke, lauf = [], []
        for i in range(n + 1):
            x = a_ + (e_ - a_) * i / n
            y = kurve_wert(kv["formel"], x)
            if y is not None and y0 <= y <= y1:
                lauf.append("%.1f,%.1f" % (px(x), py(y)))
            elif lauf:
                stuecke.append(lauf)
                lauf = []
        if lauf:
            stuecke.append(lauf)
        farbe = fv[kv.get("farbe", 1) - 1]
        for st in stuecke:
            if len(st) > 1:
                teile.append('<polyline points="%s" fill="none" stroke="%s" '
                             'stroke-width="%s" stroke-linecap="round" '
                             'stroke-linejoin="round" %s/>'
                             % (" ".join(st), farbe, kv.get("dicke", 5),
                                'stroke-dasharray="14 10"' if kv.get("gestrichelt") else ""))
        if kv.get("beschriftung"):
            bx_, by_ = kv["beschriftung_bei"]
            teile.append('<text x="%.1f" y="%.1f" font-size="27" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (px(bx_), py(by_), farbe, kv.get("anker", "start"),
                            entschaerfen(kv["beschriftung"])))

    # Punkte
    for pt in el.get("punkte", []):
        farbe = fv[pt.get("farbe", 3) - 1]
        teile.append('<circle cx="%.1f" cy="%.1f" r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                     % (px(pt["x"]), py(pt["y"]), papier, farbe))
        teile.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>'
                     % (px(pt["x"]), py(pt["y"]), farbe))
        if pt.get("beschriftung"):
            # Ohne Angabe steht die Beschriftung rechts ueber dem Punkt. Das
            # trifft am Scheitel einer Parabel die Achsenbeschriftung — darum
            # kann man sie wie bei Geraden und Parabeln frei setzen.
            if pt.get("beschriftung_bei"):
                bx_, by_ = pt["beschriftung_bei"]
                tx, ty = px(bx_), py(by_)
            else:
                tx, ty = px(pt["x"]) + 18, py(pt["y"]) - 16
            teile.append('<text x="%.1f" y="%.1f" font-size="29" font-weight="600" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (tx, ty, farbe, pt.get("anker", "start"),
                            entschaerfen(pt["beschriftung"])))
    teile.extend(achsnamen)
    teile.append("</svg>")
    return "".join(teile)


# ---------------------------------------------------------------- Rechneranzeige
def rechner_svg(el, theme):
    """Die Anzeige des TI-30X Pro MathPrint, so weit sie nachpruefbar ist.

    Belegt sind: vier Zeilen zu 16 Zeichen, Eingabe oben, Ergebnis
    rechtsbuendig, getrennte Tasten fuer Subtraktion (−) und negatives
    Vorzeichen ((−)), Berechnen mit =, Brueche ueber n/d. Quelle ist das
    Handbuch von Texas Instruments.

    **Nachgebaut wird die Anzeige, nicht das Tastenfeld.** Wo die Tasten
    auf dem Geraet liegen, steht hier nicht — es wird nur gezeigt, welche
    gedrueckt wird. Eine erfundene Tastenanordnung waere schlimmer als
    keine: Wer sie lernt, greift am Geraet daneben.

    Bruchdarstellung im Text: [a|b] wird zweistoeckig gesetzt, wie es
    MathPrint tut.
    """
    b = el.get("breite", 700)
    zeilen = el.get("zeilen", [])
    # Die Hoehe ergibt sich aus der Breite: 16 Zeichen, vier Zeilen. Sie
    # wird ins Element geschrieben, damit der senkrechte Fluss sie kennt
    # und die naechste Zeile nicht in die Anzeige laeuft.
    # Das Geraet hat vier Zeilen. Gezeigt werden nur die benutzten plus
    # die Ergebniszeile — ein zu drei Vierteln leeres Feld sieht nach
    # Fehler aus, nicht nach Anzeige.
    benutzt = min(4, max(2, len(el.get("zeilen", []))
                         + (1 if el.get("ergebnis") is not None else 0)))
    el["_zeilen"] = benutzt
    # Ein Bruch ist zweistoeckig und braucht rund die anderthalbfache
    # Zeilenhoehe — sonst schneidet der Rand Zaehler und Nenner ab.
    bruch = any("[" in z for z in list(el.get("zeilen", []))
                + ([el["ergebnis"]] if el.get("ergebnis") else []))
    el["_hoch"] = 1.55 if bruch else 1.0
    el.setdefault("hoehe", int(benutzt * ((b - 60) / 16 * 1.85 * el["_hoch"]) + 46
                               + (82 if (el.get("taste") or el.get("tasten")) else 0)))
    ergebnis = el.get("ergebnis")
    # Eine Taste oder eine Reihe: gedrueckte Tasten bleiben stehen, die
    # zuletzt gedrueckte ist gefuellt. So sieht man die ganze Folge, nicht
    # nur den letzten Anschlag.
    reihe = el.get("tasten") or ([el["taste"]] if el.get("taste") else [])
    taste = reihe[-1] if reihe else None
    tinte = theme["tinte"]
    lcd = el.get("lcd", "#c9d4c4")          # gruenlich, wie ein LCD
    rahmen = el.get("rahmen", "#2b2b2b")

    zeichen = 16
    zb = (b - 60) / zeichen                  # Zeichenbreite
    zh = zb * 1.85 * el.get("_hoch", 1.0)    # Zeilenhoehe
    reihen = el.get("_zeilen", 4)
    h_disp = reihen * zh + 46
    h = h_disp + (74 if taste else 0)
    t = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (b, h, b, h)]
    # Deckende Flaeche ueber das ganze Element. Eine Tastenfolge wird als
    # Stapel gebaut: Jede neue Anzeige muss die vorige vollstaendig
    # verdecken, auch im Tastenband — sonst schauen aeltere Kappen zwischen
    # den neuen hervor.
    t.append('<rect x="0" y="0" width="%d" height="%d" fill="%s"/>'
             % (b, h, theme["papier"]))
    t.append('<rect x="0" y="0" width="%d" height="%.0f" rx="14" fill="%s"/>'
             % (b, h_disp, rahmen))
    t.append('<rect x="18" y="16" width="%d" height="%.0f" rx="5" fill="%s"/>'
             % (b - 36, h_disp - 32, lcd))

    def setzen(text, y, rechts=False):
        """Eine Displayzeile. [a|b] wird zum Bruch."""
        teile = re.split(r"(\[[^\[\]|]*\|[^\[\]|]*\])", text)
        breite = 0
        for st in teile:
            breite += (len(st) - 3) * zb if st.startswith("[") else len(st) * zb
        x = (b - 30 - breite) if rechts else 30
        for st in teile:
            if st.startswith("["):
                oben, unten = st[1:-1].split("|")
                w = max(len(oben), len(unten)) * zb
                mitte = y - zb * 0.55            # Strich etwa auf halber Zeichenhoehe
                t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" '
                         'text-anchor="middle" fill="%s">%s</text>'
                         % (x + w / 2, mitte - zb * 0.22, "monospace", zb * 1.25, tinte,
                            entschaerfen(oben)))
                t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                         'stroke-width="2.5"/>' % (x, mitte, x + w, mitte, tinte))
                t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" '
                         'text-anchor="middle" fill="%s">%s</text>'
                         % (x + w / 2, mitte + zb * 1.15, "monospace", zb * 1.25, tinte,
                            entschaerfen(unten)))
                x += w
            elif st:
                t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" '
                         'fill="%s" xml:space="preserve">%s</text>'
                         % (x, y, "monospace", zb * 1.7, tinte, entschaerfen(st)))
                x += len(st) * zb

    # Grundlinie der ersten Zeile: so weit unter der Oberkante, dass die
    # Oberlaengen im Feld bleiben.
    y0 = 22 + zh * 0.78
    for i, z in enumerate(zeilen[:reihen]):
        setzen(z, y0 + i * zh)
    if ergebnis is not None:
        setzen(ergebnis, y0 + min(len(zeilen), reihen - 1) * zh, rechts=True)

    if taste:
        kappen = [(k, max(60, 26 + len(k) * 19)) for k in reihe]
        luecke = 9
        platz = b - 16

        def gesamtbreite(ks, f=1.0):
            return sum(w * f for _, w in ks) + luecke * (len(ks) - 1)

        # Passt die Reihe nicht, wird sie erst schmaler gesetzt und, wenn das
        # nicht reicht, vorn gekuerzt: Die letzten Anschlaege sind die, auf
        # die es ankommt.
        skala = 1.0
        if gesamtbreite(kappen) > platz:
            skala = max(0.62, platz / gesamtbreite(kappen))
        while len(kappen) > 1 and gesamtbreite(kappen, skala) > platz:
            kappen = kappen[1:]
            if kappen and kappen[0][0] != "…":
                kappen = [("…", 40 / skala)] + kappen
        kappen = [(k, w * skala) for k, w in kappen]
        gesamt = sum(w for _, w in kappen) + luecke * (len(kappen) - 1)
        x = max(8, (b - gesamt) / 2)
        y = h_disp + 12
        for i, (k, w) in enumerate(kappen):
            jetzt = (i == len(kappen) - 1)
            t.append('<rect x="%.1f" y="%.1f" width="%.1f" height="54" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="%s" %s/>'
                     % (x, y, w, tinte if jetzt else theme.get("karte", "#fff"),
                        tinte, "2.5" if jetzt else "2",
                        "" if jetzt else 'stroke-opacity=".45"'))
            t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" '
                     'text-anchor="middle" font-weight="600" fill="%s" %s>%s</text>'
                     % (x + w / 2, y + 36, "monospace",
                        max(14, int((26 if len(k) < 4 else 20) * skala)),
                        theme["papier"] if jetzt else tinte,
                        "" if jetzt else 'fill-opacity=".5"', entschaerfen(k)))
            x += w + luecke
    t.append("</svg>")
    return "".join(t)


# ---------------------------------------------------------------- Elemente
# Abspieler-Zusatz fuer "bewegung" (Prototyp 02.10.2026). seek(t) wird
# umgehaengt: erst die Ebenen wie immer, dann jede bewegte Parabel aus der
# Zeit neu gerechnet. Zwischen zwei Stuetzpunkten weich (smoothstep); wer
# "Bewegung reduzieren" eingestellt hat, sieht die Stuetzpunkte als Spruenge.
BEWEGUNG_JS = r'''
const RUHIG = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
const BEW = [...document.querySelectorAll('[data-t0]')].map(L => ({
  t0: parseFloat(L.dataset.t0),
  teile: [...L.querySelectorAll('[data-bew]')].map(p => ({
    art: 'p', p, L, k: JSON.parse(p.dataset.bew), f: p.dataset.fenster.split(',').map(Number) }))
    .concat([...L.querySelectorAll('[data-bewg]')].map(p => ({
      art: 'g', p, L, k: JSON.parse(p.dataset.bewg), f: p.dataset.fenster.split(',').map(Number) })))
}));
// Zwischen zwei Stuetzpunkten weich. Wie viele Zahlen ein Stuetzpunkt traegt, sagt er
// selbst: [t, a, u, v] bei einer Parabel, [t, m, q] bei einer Geraden, [t, x] bei einer Bahn.
function bewZustand(k, t) {
  const n = k[0].length - 1;
  if (t <= k[0][0]) return k[0].slice(1);
  for (let i = 0; i < k.length - 1; i++) {
    if (t < k[i + 1][0]) {
      let q = (t - k[i][0]) / (k[i + 1][0] - k[i][0]);
      q = RUHIG ? 0 : q * q * (3 - 2 * q);
      const aus = [];
      for (let j = 1; j <= n; j++) aus.push(k[i][j] + (k[i + 1][j] - k[i][j]) * q);
      return aus;
    }
  }
  return k[k.length - 1].slice(1);
}
const bewZahl = x => { const r = Math.round(x * 10) / 10; return (r < 0 ? '−' : '') + Math.abs(r); };
// Eine bewegte Gerade y = m x + q: am Fenster abgeschnitten, dazu ihre Begleiter.
function bewegeGerade(T, t, px, py, x0, x1, y0, y1) {
  const [m, q] = bewZustand(T.k, t - T.t0);
  if (T.p.dataset.ab !== undefined) x0 = Math.max(x0, parseFloat(T.p.dataset.ab));
  const f = x => m * x + q, innen = (x, y) => x >= x0 - 1e-9 && x <= x1 + 1e-9 && y >= y0 - 1e-9 && y <= y1 + 1e-9;
  const pt = [];
  for (const x of [x0, x1]) { const y = f(x); if (y >= y0 - 1e-9 && y <= y1 + 1e-9) pt.push([x, y]); }
  if (Math.abs(m) > 1e-9) for (const y of [y0, y1]) { const x = (y - q) / m; if (x >= x0 - 1e-9 && x <= x1 + 1e-9) pt.push([x, y]); }
  pt.sort((u, v) => u[0] - v[0]);
  T.p.setAttribute('d', pt.length > 1
    ? 'M' + px(pt[0][0]).toFixed(1) + ',' + py(pt[0][1]).toFixed(1) +
      'L' + px(pt[pt.length - 1][0]).toFixed(1) + ',' + py(pt[pt.length - 1][1]).toFixed(1)
    : '');
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); }); };
  const beschrifte = (g, x, y, text) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    tx.setAttribute('y', py(y) + (m > 0 ? 44 : -18));          // auf die Seite, wo die Gerade nicht laeuft
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  const fuell = (v, x, y) => v.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y))
                              .replace('{m}', bewZahl(m)).replace('{q}', bewZahl(q));
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-gy')) {
      setze(g, 0, q); beschrifte(g, 0, q, '(0 | ' + bewZahl(q) + ')');
    } else if (g.classList.contains('bew-gn')) {
      if (Math.abs(m) < 1e-9) { g.style.display = 'none'; continue; }
      const xn = -q / m; setze(g, xn, 0); beschrifte(g, xn, 0, '(' + bewZahl(xn) + ' | 0)');
    } else if (g.classList.contains('bew-gm')) {
      const x = parseFloat(g.dataset.x);
      setze(g, x, f(x)); beschrifte(g, x, f(x), fuell(g.dataset.text, x, f(x)));
    } else if (g.classList.contains('bew-gl')) {
      const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn));
      const x = bewZustand(bahn, t - T.t0)[0];
      setze(g, x, f(x)); beschrifte(g, x, f(x), fuell(g.dataset.text, x, f(x)));
    } else if (g.classList.contains('bew-gd')) {
      // Steigungsdreieck: von (x | f(x)) nach rechts, dann senkrecht auf die Gerade.
      let xa, dx;
      if (g.dataset.bahn) {
        const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn));
        [xa, dx] = bewZustand(bahn, t - T.t0);
      } else { xa = parseFloat(g.dataset.x); dx = parseFloat(g.dataset.dx); }
      const xb = xa + dx;
      const ya = f(xa), yb = f(xb), sichtbar = innen(xa, ya) && innen(xb, yb);
      g.style.display = sichtbar ? '' : 'none';
      if (!sichtbar) continue;
      g.querySelector('.bew-gd-w').setAttribute('d', 'M' + px(xa) + ',' + py(ya) + 'L' + px(xb) + ',' + py(ya));
      g.querySelector('.bew-gd-s').setAttribute('d', 'M' + px(xb) + ',' + py(ya) + 'L' + px(xb) + ',' + py(yb));
      const tx = g.querySelector('.bew-gd-tx'), ty = g.querySelector('.bew-gd-ty');
      tx.setAttribute('x', px((xa + xb) / 2)); tx.setAttribute('y', py(ya) + (m > 0 ? 36 : -14));
      tx.textContent = 'Δx = ' + bewZahl(dx);
      ty.setAttribute('x', px(xb) + 12); ty.setAttribute('y', py((ya + yb) / 2) + 10);
      ty.textContent = 'Δy = ' + bewZahl(yb - ya);
    }
  }
}
function bewegen(t) {
  for (const L of BEW) for (const T of L.teile) {
    const [x0, x1, y0, y1, b, h, rd] = T.f;
    const px = x => rd + (x - x0) / (x1 - x0) * (b - 2 * rd);
    const py = y => h - rd - (y - y0) / (y1 - y0) * (h - 2 * rd);
    // T.L ist das Element, die Startzeit der Szene steht an L (der Liste) — vorher
    // las bewegeGerade T.L.t0, bekam undefined, und jede Gerade stand im Endzustand.
    if (T.art === 'g') { T.t0 = L.t0; bewegeGerade(T, t, px, py, x0, x1, y0, y1); continue; }
    const [a, u, v] = bewZustand(T.k, t - L.t0);
    let d = '', zug = false;
    for (let i = 0; i <= 240; i++) {
      const x = x0 + (x1 - x0) * i / 240, y = a * (x - u) * (x - u) + v;
      if (y >= y0 && y <= y1) { d += (zug ? 'L' : 'M') + px(x).toFixed(1) + ',' + py(y).toFixed(1); zug = true; }
      else zug = false;
    }
    T.p.setAttribute('d', d);
    const f = x => a * (x - u) * (x - u) + v;
    const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
    const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
      g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); }); };
    const beschrifte = (g, x, y, text, unten) => {
      const tx = g.querySelector(':scope > text'); if (!tx) return;
      const rechts = x > x1 - (x1 - x0) * 0.3;
      tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
      tx.setAttribute('y', py(y) + (unten ? 44 : -18));
      tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
      tx.textContent = text;
    };
    const fuell = (vorlage, x, y) => vorlage.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y));
    for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
      if (g.classList.contains('bew-s')) {
        setze(g, u, v); beschrifte(g, u, v, 'S(' + bewZahl(u) + ' | ' + bewZahl(v) + ')', a > 0);
      } else if (g.classList.contains('bew-n')) {
        const q = a !== 0 ? -v / a : -1, w = q >= 0 ? Math.sqrt(q) : NaN;
        if (isNaN(w)) { g.style.display = 'none'; continue; }
        const xn = g.classList.contains('bew-n1') ? u - w : u + w;
        setze(g, xn, 0);
        if (g.querySelector(':scope > text')) {
          const tx = g.querySelector(':scope > text'), links = g.classList.contains('bew-n1') && w > 1e-9;
          tx.setAttribute('x', px(xn) + (links ? -16 : 16)); tx.setAttribute('y', py(0) + (a > 0 ? -18 : 44));
          tx.setAttribute('text-anchor', links ? 'end' : 'start'); tx.textContent = '(' + bewZahl(xn) + ' | 0)';
        }
      } else if (g.classList.contains('bew-y')) {
        setze(g, 0, f(0)); beschrifte(g, 0, f(0), '(0 | ' + bewZahl(f(0)) + ')', false);
      } else if (g.classList.contains('bew-m')) {
        const x = parseFloat(g.dataset.x);
        setze(g, x, f(x)); beschrifte(g, x, f(x), fuell(g.dataset.text, x, f(x)), false);
      } else if (g.classList.contains('bew-l')) {
        const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn).map(b => [b[0], b[1], 0, 0]));
        const x = bewZustand(bahn, t - L.t0)[0], y = f(x);
        setze(g.querySelector('.bew-pt'), x, y);
        g.style.display = innen(x, y) ? '' : 'none';
        const gs = g.querySelector('.bew-geist');
        if (gs) { const xs = 2 * u - x; gs.style.display = Math.abs(xs - x) > 0.05 && innen(xs, f(xs)) ? '' : 'none';
          gs.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(xs)); c.setAttribute('cy', py(f(xs))); }); }
        beschrifte(g, x, y, fuell(g.dataset.text, x, y), a > 0 && Math.abs(x - u) < (x1 - x0) * 0.15);
      }
    }
  }
}
const seekOhneBewegung = seek;
seek = function (t) { seekOhneBewegung(t); bewegen(t); };
'''


# Abspieler-Zusatz fuer "fragen" (Prototyp 02.10.2026): Der Clip haelt an,
# stellt eine Frage (Knoepfe oder Tippen ins Bild), gibt Rueckmeldung und
# laeuft auf «Weiter» weiter. Nur in Clips mit "fragen", nie im Pruefmodus
# (?render). Gespult wird an Fragen vorbei, ohne anzuhalten.
FRAGEN_JS = r'''
(() => {
  if (location.search.includes('render')) return;
  const pp = document.getElementById('pp');
  const css = document.createElement('style');
  css.textContent = `
    #frage{position:absolute;left:110px;top:560px;width:820px;z-index:50;display:none;
      background:rgba(255,255,255,.97);border:3px solid var(--f2);border-radius:22px;
      padding:28px 34px;box-shadow:0 10px 40px rgba(0,0,0,.18);font-family:inherit;color:inherit}
    #frage .fr-kopf{font-size:26px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--f2);margin-bottom:10px}
    #frage .fr-text{font-size:38px;line-height:1.3;margin-bottom:22px}
    #frage .fr-knoepfe{display:flex;flex-wrap:wrap;gap:14px}
    #frage button{font:inherit;font-size:32px;padding:10px 26px;border-radius:999px;cursor:pointer;
      border:2.5px solid var(--f2);background:var(--f2w);color:inherit}
    #frage button.ok{border-color:var(--f3);background:var(--f3w)}
    #frage button.nein{border-color:var(--f4);background:var(--f4w)}
    #frage .fr-rueck{font-size:32px;line-height:1.35;margin-top:20px}
    #frage .fr-weiter{margin-top:20px}
    .fr-tippbar, .fr-tippbar svg{pointer-events:auto !important;cursor:crosshair}`;
  document.head.appendChild(css);
  const box = document.createElement('div'); box.id = 'frage'; stage.appendChild(box);
  let letzt = 0, offen = null, tippen = null, stimme = null, sprung = false;
  // Vorlesen mit derselben Stimme wie der Clip — nur wenn dessen Ton an ist.
  const hauptton = document.getElementById('ton');
  const vorlesen = src => {
    if (stimme) { stimme.pause(); stimme = null; }
    if (!src || !hauptton || hauptton.muted) return;
    stimme = new Audio(src); stimme.play().catch(() => {});
  };
  const erledigt = new Set();     // beantwortete Fragen
  const pause = () => { if (pp.textContent === 'Pause') pp.click(); };
  const weiter = () => { if (pp.textContent === 'Play') pp.click(); };
  function schliessen() {
    vorlesen(null);
    box.style.display = 'none'; box.innerHTML = '';
    document.querySelectorAll('.fr-marke').forEach(m => m.remove());
    document.querySelectorAll('.fr-tippbar').forEach(l => l.classList.remove('fr-tippbar'));
    if (tippen) { stage.removeEventListener('click', tippen); tippen = null; }
    offen = null;
  }
  function antwort(F, ok, text, schl) {
    const o = offen; erledigt.add(o.i);
    box.dataset.fertig = '1';
    vorlesen((F.ton || {})[schl]);
    if (F.typ === 'klick') box.querySelector('.fr-knoepfe').innerHTML = '';
    const r = box.querySelector('.fr-rueck');
    r.innerHTML = (ok ? '✓ ' : '') + text;
    r.style.color = ok ? 'var(--f3)' : '';
    if (ok) {                      // richtig: kurz bestaetigen, dann von selbst weiter
      setTimeout(() => { if (offen === o) { schliessen(); weiter(); } }, 1300);
      return;
    }
    const w = document.createElement('button'); w.className = 'fr-weiter'; w.textContent = 'Weiter ▶';
    w.onclick = () => { schliessen(); weiter(); };
    box.appendChild(w); w.focus();
  }
  function zeigen(i, F) {
    offen = { i, t: F.t }; pause(); delete box.dataset.fertig;
    box.innerHTML = '<div class="fr-kopf">Deine Vorhersage</div><div class="fr-text"></div>'
      + '<div class="fr-knoepfe"></div><div class="fr-rueck"></div>';
    box.querySelector('.fr-text').textContent = F.text;
    const kn = box.querySelector('.fr-knoepfe');
    if (F.typ === 'wahl') {
      F.optionen.forEach((o, j) => {
        const b = document.createElement('button'); b.textContent = o;
        b.onclick = () => {
          kn.querySelectorAll('button').forEach(x => x.disabled = true);
          b.classList.add(j === F.richtig ? 'ok' : 'nein');
          antwort(F, j === F.richtig, (F.rueck || {})[j] || (j === F.richtig ? 'Richtig.' : 'Schau, was der Clip zeigt.'), 'r' + j);
        };
        kn.appendChild(b);
      });
    } else if (F.typ === 'klick') {
      const L = [...document.querySelectorAll('.l')].find(l => +l.style.opacity > 0.5 && l.querySelector('[data-fenster]'));
      if (!L) { schliessen(); weiter(); return; }
      const svg = L.querySelector('svg'), fe = L.querySelector('[data-fenster]').dataset.fenster.split(',').map(Number);
      const [x0, x1, y0, y1, b, h, rd] = fe;
      L.classList.add('fr-tippbar');
      // Am Stage horchen, nicht am Layer: unsichtbare spaetere Layer (Deckkraft 0)
      // liegen obenauf und wuerden den Tipp abfangen.
      tippen = ev => {
        if (!offen || box.dataset.fertig || box.contains(ev.target)) return;
        const r = svg.getBoundingClientRect();
        if (ev.clientX < r.left || ev.clientX > r.right || ev.clientY < r.top || ev.clientY > r.bottom) return;
        const sx = (ev.clientX - r.left) / r.width * b, sy = (ev.clientY - r.top) / r.height * h;
        const x = x0 + (sx - rd) / (b - 2 * rd) * (x1 - x0), y = y0 + (h - rd - sy) / (h - 2 * rd) * (y1 - y0);
        const mk = (cx, cy, farbe) => { const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', 16); c.setAttribute('class', 'fr-marke');
          c.setAttribute('fill', 'none'); c.setAttribute('stroke', farbe); c.setAttribute('stroke-width', 6); svg.appendChild(c); };
        mk(sx, sy, 'var(--f2)');
        const d = Math.hypot(x - F.ziel[0], y - F.ziel[1]);
        if (d <= (F.toleranz || 0.5)) return antwort(F, true, F.richtig_text || 'Getroffen.', 'ok');
        const zx = rd + (F.ziel[0] - x0) / (x1 - x0) * (b - 2 * rd), zy = h - rd - (F.ziel[1] - y0) / (y1 - y0) * (h - 2 * rd);
        mk(zx, zy, 'var(--f3)');
        const fk = (F.fallen || []).findIndex(f => Math.hypot(x - f.bei[0], y - f.bei[1]) <= (F.toleranz || 0.5));
        antwort(F, false, fk >= 0 ? F.fallen[fk].text : (F.falsch_text || 'Nicht ganz — der grüne Kreis zeigt die Stelle.'),
                fk >= 0 ? 'fall' + fk : 'falsch');
      };
      stage.addEventListener('click', tippen);
      kn.innerHTML = '<span style="font-size:30px;color:var(--f2)">👉 Tipp ins Bild rechts.</span>';
    }
    box.style.display = 'block';
    vorlesen((F.ton || {}).frage);
  }
  // Spulen wird ausdruecklich erkannt: Pfeiltasten und ein Klick auf die
  // Zeitleiste setzen ein Zeichen, das das naechste Bild auswertet. Ein
  // spaetes Bild (langsames Laden, Hintergrund-Tab) ist kein Spulen.
  // Neustart (R) und ein Sprung vor die erste Frage stellen alle Fragen neu;
  // nach R laeuft der Clip ab 0 wie beim ersten Abspielen.
  document.addEventListener('keydown', e => {
    if ((e.key || '').toLowerCase() === 'r') { schliessen(); erledigt.clear(); letzt = 0; }
    if (e.code === 'ArrowLeft' || e.code === 'ArrowRight') sprung = true;
  });
  const bar = document.getElementById('bar');
  bar.addEventListener('click', () => { sprung = true; });
  // Die Abspielzeit ist im Abspieler lokal; zurueckgestellt wird sie ueber
  // dessen Zeitleiste.
  const zurueck = s => {
    const r = bar.getBoundingClientRect();
    if (r.width > 0 && bar.onclick) bar.onclick({ currentTarget: bar, clientX: r.left + s / DUR * r.width });
  };
  const vorFragen = seek;
  seek = function (t) {
    vorFragen(t);
    if (sprung) {
      // gespult: eine uebersprungene Frage wird nicht gestellt, eine
      // beantwortete kommt nicht wieder — ausser zurueck an den Anfang
      sprung = false;
      if (FRAGEN.length && t < Math.min(...FRAGEN.map(F => F.t))) { schliessen(); erledigt.clear(); }
    } else if (!offen && pp.textContent === 'Pause') {
      // gewoehnliches Abspielen, auch wenn ein Bild weit springt: die erste
      // ueberschrittene Frage wird gestellt, der Clip geht an ihre Stelle zurueck
      let i = -1;
      FRAGEN.forEach((F, j) => {
        if (!erledigt.has(j) && letzt < F.t && t >= F.t && (i < 0 || F.t < FRAGEN[i].t)) i = j;
      });
      if (i >= 0) {
        zeigen(i, FRAGEN[i]);
        if (offen && t - offen.t > 0.1) { t = offen.t; zurueck(t); vorFragen(t); }
      }
    }
    if (offen && Math.abs(t - offen.t) > 1.0) schliessen();
    letzt = t;
  };
})();
'''


def fragen_texte(F):
    """Alle Texte einer Frage, die vorgelesen werden: Liste (schluessel,
    angezeigt, gesprochen). Der gesprochene Wortlaut steht in den *_sprich-
    Feldern (wie «x minus zwei» statt «x − 2»); fehlt er, wird der angezeigte
    Text gelesen. Dieselbe Liste benutzt build-clip-fragen-ton.py — so passen
    Tondateien und Abspieler immer zusammen."""
    t = [("frage", F["text"], F.get("sprich", F["text"]))]
    # Richtige Antworten werden nicht vorgelesen: Der Clip zeigt kurz ✓ und
    # rollt weiter (Entscheid 02.10.2026) — eine Ansage liefe in den Sprecher.
    if F.get("typ") == "wahl":
        rs = F.get("rueck_sprich", {})
        for j in range(len(F.get("optionen", []))):
            if j == F.get("richtig"):
                continue
            if str(j) in F.get("rueck", {}):
                t.append(("r%d" % j, F["rueck"][str(j)], rs.get(str(j), F["rueck"][str(j)])))
    else:
        for k, f in enumerate(F.get("fallen", [])):
            t.append(("fall%d" % k, f["text"], f.get("sprich", f["text"])))
        if F.get("falsch_text"):
            t.append(("falsch", F["falsch_text"], F.get("falsch_sprich", F["falsch_text"])))
    return t


def fragen_tondatei(dateiname, i, schluessel):
    return "%s-f%d-%s.mp3" % (dateiname, i, schluessel)


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
    elif typ == "boxplot":
        klassen += ["graf"]
        inhalt = boxplot_svg(el, theme)
    elif typ == "rechner":
        klassen += ["graf"]
        inhalt = rechner_svg(el, theme)
    elif typ == "bild":
        # Eine fertige SVG-Zeichnung aus clips/bilder/, eingegossen statt
        # verlinkt: Der Clip bleibt eine Datei. Gedacht fuer Skizzen, die eine
        # Animation der Lektionsseite wiederholen — der Clip zeigt dann
        # dasselbe Bild, das die Lernenden eben selbst bedient haben.
        klassen += ["graf"]
        pfad = os.path.join(CLIPS, el["datei"])
        endung = os.path.splitext(pfad)[1].lower()
        if endung == ".svg":
            with open(pfad, encoding="utf-8") as f:
                inhalt = f.read().strip()
            if not inhalt.startswith("<svg"):
                raise SystemExit("bild: keine SVG-Datei: %s" % el["datei"])
        elif endung in (".jpg", ".jpeg", ".png"):
            # Aufnahme einer Animation (Canvas), als data:-URL eingegossen.
            # `breite` in Buehnenpixeln; die Hoehe folgt dem Seitenverhaeltnis.
            import base64
            typ_ = "image/png" if endung == ".png" else "image/jpeg"
            with open(pfad, "rb") as f:
                daten = base64.b64encode(f.read()).decode("ascii")
            inhalt = ('<img src="data:%s;base64,%s" alt="" style="width:%dpx;'
                      'display:block;border:2px solid rgba(0,0,0,.12);border-radius:10px">'
                      % (typ_, daten, el.get("breite", 1140)))
        else:
            raise SystemExit("bild: SVG, JPG oder PNG erwartet: %s" % el["datei"])
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

    # --- Bedingungsleiste ------------------------------------------------
    # Was eine Rechnung voraussetzt, verschwindet sonst mit der Szene, in der
    # es genannt wurde — und drei Szenen spaeter rechnet der Clip auf einer
    # Bedingung weiter, die niemand mehr sieht. `halten` loest das nur halb:
    # ein gehaltenes Element behaelt die Position seiner Szene und blockiert
    # damit den Fluss aller folgenden. Die Leiste steht ausserhalb des
    # Flusses und kostet darum keine Zeile.
    #
    #   "voraussetzung": "a \\neq 0"
    #   "voraussetzung": {"text": "...", "ab": "Szenenname", "bis": "Szenenname"}
    #   "voraussetzung": [ {...}, {...} ]      mehrere nacheinander
    #
    vor = dreh.get("voraussetzung")
    if vor:
        if not isinstance(vor, list):
            vor = [vor]
        leiste = []
        for v in vor:
            if isinstance(v, str):
                v = {"text": v}
            def szene_zeit(name, feld):
                if name is None:
                    return None
                q = next((q for q in plan if q["sz"].get("name") == name), None)
                if q is None:
                    raise SystemExit("voraussetzung verweist auf unbekannte Szene: %s" % name)
                return q["start"] if feld == "start" else q["start"] + q["dauer"]
            ab = szene_zeit(v.get("ab"), "start")
            bis = szene_zeit(v.get("bis"), "ende")
            ein = (ab if ab is not None else 0.0) + v.get("verzug", 0.6)
            attr = f' data-at="{ein:.2f}"'
            if bis is not None:
                attr += f' data-out="{bis:.2f}"'
            attr += ' data-anim="fade"'
            tag = entschaerfen(v.get("tag", "Voraussetzung"))
            leiste.append(f'<div class="l vorzeile"{attr} style="position:relative">'
                          f'<span class="vor"><span class="vor-tag">{tag}</span>'
                          f'<span class="vor-txt">{formel(v["text"])}</span></span></div>')
        teile.append('<div id="vorleiste">' + "".join(leiste) + '</div>')

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
    for pi, p in enumerate(plan):
        naechste = plan[pi + 1] if pi + 1 < len(plan) else None
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

            # Die Textbreite begrenzen. Ohne das laeuft eine lange Zeile bis an
            # den Buehnenrand und bricht dort unausgeglichen um — im
            # Schienen-Layout bis 1920 statt bis 1820, in der Mitte ueber die
            # volle Breite ohne Rand. `breite` war bisher totes Kapital.
            if mitte and "x" not in el:
                klassen.append("mitte")
                rand = (1920 - breite) // 2
                stil.insert(0, "left:%dpx;right:%dpx;text-align:center" % (rand, rand))
            else:
                stil.insert(0, "left:%dpx" % el.get("x", links))
                if "breite" not in el and el.get("typ") not in ("graf", "bild", "strich"):
                    stil.append("width:%dpx" % breite)
            stil.insert(1, "top:%dpx" % el.get("y", y))

            hoehe = el.get("hoehe", int(el.get("groesse", 50) * 1.5) + 40)
            y = el.get("y", y) + el.get("abstand", max(abstand, hoehe))

            attr = f' data-at="{ein:.2f}"'
            if el.get("typ") == "graf" and (any(pa.get("bewegung") for pa in el.get("parabeln", []))
                                            or any(ge.get("bewegung") for ge in el.get("geraden", []))):
                attr += f' data-t0="{start:.2f}"'
            if aus is not None:
                attr += f' data-out="{aus:.2f}"'
            attr += f' data-anim="{anim}"'
            teile.append(f'<div class="{" ".join(klassen)}"{attr} '
                         f'style="{";".join(stil)}">{inhalt}</div>')

            # --- Anschluss an den vorherigen Schritt ------------------------
            # `mitnehmen: true` zeigt dieses Element in der naechsten
            # Schritt-Szene noch einmal, oben im Band, das das Schienen-Layout
            # dafuer frei laesst (168 bis 430 px). Das ist nicht dasselbe wie
            # `halten`: Gehalten bleibt ein Element an seinem Platz stehen —
            # was nur beim ersten Schritt oben passt. Mitgenommen wird es an
            # den Kopf der naechsten Szene gesetzt, gleich wo es vorher stand.
            #
            # Wozu: Ohne das faellt beim Szenenwechsel die Formel weg, die der
            # naechste Schritt gerade einsetzt. Auf der Merkschiene links steht
            # dann zwar noch, *dass* es einen Schritt davor gab, aber nicht
            # mehr, *was* er ergeben hat — und das Ansatz-Prinzip (erst die
            # Formel, dann die Werte) ist im Bild nicht mehr zu sehen.
            if el.get("mitnehmen"):
                if naechste is None or naechste["sz"].get("layout") != "schiene":
                    print("  [WARN] mitnehmen ohne folgende Schritt-Szene: %s"
                          % sz.get("name"))
                else:
                    a_kl, a_stil, a_inhalt = element_html(el, theme)
                    a_kl.append("anschluss")
                    a_stil.insert(0, "left:680px;top:168px")
                    if "breite" not in el and el.get("typ") not in ("graf", "bild", "strich"):
                        a_stil.append("width:1140px")
                    a_ein = naechste["start"] + 0.25
                    a_aus = naechste["start"] + naechste["dauer"]
                    teile.append(
                        f'<div class="{" ".join(a_kl)}" data-at="{a_ein:.2f}" '
                        f'data-out="{a_aus:.2f}" data-anim="fade" '
                        f'style="{";".join(a_stil)}">{a_inhalt}</div>')

        # Die Bedingungsleiste sitzt bei top:96px und ist rund 54px hoch, sie
        # endet also bei y = 150. Wer sie benutzt, laesst die Szenen darunter
        # beginnen. Lieber hier abbrechen als es spaeter im Bild suchen.
        if dreh.get("voraussetzung") and sz.get("oben", oben) < 170:
            raise SystemExit(
                "Szene %r beginnt bei oben=%d und liefe in die Bedingungsleiste "
                "(sie endet bei y=150). Mit einer Voraussetzung beginnen die Szenen "
                "bei oben >= 170." % (sz.get("name", "?"), sz.get("oben", oben)))

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

    # Nur Clips mit bewegten Bildern bekommen den Zusatz — alle anderen
    # bleiben Byte fuer Byte, wie sie waren.
    if "data-bew=" in html or "data-bewg=" in html:
        html = html.replace("window.__seek = seek;", BEWEGUNG_JS + "window.__seek = seek;", 1)
    if dreh.get("fragen"):
        fr = []
        for F in dreh["fragen"]:
            sz = next((q for q in plan if q["sz"].get("name") == F["szene"]), None)
            if sz is None:
                raise SystemExit("Frage verweist auf unbekannte Szene: %s" % F["szene"])
            G = {k: v for k, v in F.items() if not k.startswith("_") and k not in ("szene", "bei")
                 and not k.endswith("sprich")}
            for f_ in G.get("fallen", []):
                f_.pop("sprich", None)
            G["t"] = round(sz["start"] + F.get("bei", 0.3), 2)
            G["ton"] = {}
            for schl, _, _ in fragen_texte(F):
                datei = fragen_tondatei(dreh["dateiname"], len(fr), schl)
                if os.path.exists(os.path.join(CLIPS, "ton", datei)):
                    G["ton"][schl] = "ton/" + datei
            fr.append(G)
        html = html.replace("window.__seek = seek;", "const FRAGEN = " + json.dumps(fr, ensure_ascii=False)
                            + ";" + FRAGEN_JS + "window.__seek = seek;", 1)

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

/* Bedingungsleiste: die Voraussetzung, auf der die Rechnung steht.
   Sie liegt ausserhalb des Szenenflusses — darum kostet sie keine Zeile
   und kann trotzdem stehen bleiben, solange sie gilt. Unterhalb des
   Inhalts, oberhalb der Fusszeile. */
#vorleiste{{position:absolute;left:130px;right:100px;top:96px;
 display:flex;justify-content:center;gap:14px;z-index:5;pointer-events:none}}
.vor{{display:inline-flex;align-items:center;gap:.58em;
 background:var(--f1w);border:1.5px solid var(--f1);border-radius:10px;
 padding:7px 19px 8px;color:var(--tinte);font-size:30px;line-height:1.14;
 box-shadow:0 1px 0 rgba(0,0,0,.03)}}
.vor .vor-tag{{font-family:'Source Sans 3',sans-serif;font-size:18px;font-weight:700;
 letter-spacing:.13em;text-transform:uppercase;color:var(--f1);opacity:.95;
 white-space:nowrap;align-self:center}}
.vor .vor-txt{{white-space:nowrap}}

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
  // Der Ton laeuft von selbst und hoerbar los. Erlaubt ist das, weil der
  // Klick auf die Clipkarte die noetige Nutzergeste war und das <iframe>
  // sie ueber `allow="autoplay"` weitergereicht bekommt (clipRahmen in
  // physiklib.js). Verweigert der Browser trotzdem — etwa wenn jemand die
  // Clipdatei direkt aufruft, ohne vorher zu klicken —, faellt der Clip auf
  // stumm zurueck und der Knopf «Ton an» holt ihn hervor. Sobald der Ton
  // laeuft, fuehrt er die Uhr: Tondrift faellt auf, Bilddrift nicht.
  const ton = document.getElementById('ton'), ts = document.getElementById('ts');
  const tonBeschriften = () => {{
    if (ts) ts.textContent = (!ton || ton.muted) ? '🔇 Ton an' : '🔊 Ton aus';
  }};
  if (ton) {{
    ts.hidden = false;
    ton.muted = false;
    ton.play().then(tonBeschriften).catch(() => {{
      ton.muted = true;
      tonBeschriften();
      ton.play().catch(() => {{}});
    }});
    tonBeschriften();
    ts.onclick = () => {{
      ton.muted = !ton.muted;
      tonBeschriften();
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
            # Clip zu einer einzelnen Animation: Anker ihres <h3>. Daran
            # haengt build-clips-einbau.py den Knopf «▶ Clip» in die
            # Titelzeile und hebt die Zeile in den Listen farbig ab.
            if dreh.get("animation"):
                eintraege[-1]["animation"] = dreh["animation"]
    if eintraege:
        verzeichnis(eintraege)
