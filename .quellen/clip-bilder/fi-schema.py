#!/usr/bin/env python3
"""Skizzen fuer den Clip p6-2-fi-stromvergleich (Element `bild`).

Dieselbe Anordnung wie Animation 12 auf p6-2 (Canvas `fi-cv`): Netz links,
Leitungsschutzschalter auf L, FI mit Ringkern um L und N, Wasserkocher mit
Metallgehaeuse, Schutzleiter PE, Mensch rechts. Die Werte stammen aus
fiRechne() der Animation (230 V, 2000 W, R_K = 1000 Ohm, Leitung und
Schutzleiter je 1 Ohm, Kurzschluss 0.5 Ohm) und werden hier nachgerechnet.

Aufruf vom Repo-Root:  python3 .quellen/clip-bilder/fi-schema.py
Schreibt clips/bilder/fi-<fall>.svg.
"""
import os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ZIEL = os.path.join(WURZEL, "clips", "bilder")

U, P, RK = 230.0, 2000.0, 1000.0
ILAST = P / U
TINTE, ROT, GRUEN = "#1c1a17", "#9b1c1c", "#1f6b3a"
LFARBE, NFARBE, PEFARBE = "#7a4a1e", "#1f4e8a", "#3f8f3a"
B, H = 1140, 400
YL, YN, YPE, YE = 70, 150, 230, 350
GX0, GX1, GY0, GY1 = 800, 960, 40, 270          # Metallgehaeuse
HX = 880                                          # Heizwiderstand


def fmt(x, n):
    return ("%%.%df" % n) % x


def werte(fall):
    iL = iN = ILAST
    w = {"iK": None, "iPE": None}
    if fall == "koerper":
        iK = U / RK
        iL, w["iK"] = ILAST + iK, iK
    elif fall == "pemensch":
        rp = 1 / (1 / 1.0 + 1 / RK)
        iF = U / (1.0 + rp)
        uB = iF * rp
        iL, w["iK"], w["iPE"] = ILAST + iF, uB / RK, uB
    elif fall == "kurz":
        iL = iN = ILAST + U / 0.5
    w["iL"], w["iN"] = iL, iN
    return w


def text(x, y, s, farbe=TINTE, gr=28, anker="start", fett=False):
    return ('<text x="%d" y="%d" fill="%s" font-size="%d" text-anchor="%s"%s '
            'font-family="\'Source Sans 3\',sans-serif">%s</text>'
            % (x, y, farbe, gr, anker, ' font-weight="600"' if fett else "", s))


def idx(gross, klein):
    return '%s<tspan dy="7" font-size="20">%s</tspan><tspan dy="-7"> </tspan>' % (gross, klein)


def pfeil(x0, y0, x1, y1, farbe):
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    k = 16
    p1 = (x1 - k * math.cos(a - 0.45), y1 - k * math.sin(a - 0.45))
    p2 = (x1 - k * math.cos(a + 0.45), y1 - k * math.sin(a + 0.45))
    return ('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="4"/>'
            '<polygon points="%d,%d %.1f,%.1f %.1f,%.1f" fill="%s"/>'
            % (x0, y0, x1 - 8 * math.cos(a), y1 - 8 * math.sin(a), farbe,
               x1, y1, p1[0], p1[1], p2[0], p2[1], farbe))


def schema(fall):
    w = werte(fall)
    t = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
         % (B, H, B, H)]
    # Erde
    t.append('<line x1="20" y1="%d" x2="1120" y2="%d" stroke="#9a8f7e" stroke-width="2" '
             'stroke-dasharray="10 8"/>' % (YE, YE))
    t.append(text(84, YE - 10, "Erde", "#7a6f5e", 22))
    # Gehaeuse und Heizwiderstand
    t.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#eef0f3" stroke="#6b7280" stroke-width="3" rx="6"/>'
             % (GX0, GY0, GX1 - GX0, GY1 - GY0))
    t.append(text((GX0 + GX1) // 2, GY1 - 14, "Metallgehäuse", "#4b5563", 20, "middle"))
    t.append(text((GX0 + GX1) // 2, GY0 - 12, "Wasserkocher 2000 W", "#4b5563", 22, "middle"))
    # Leiter
    t.append(text(24, YL + 10, "L", LFARBE, 30, fett=True))
    t.append(text(24, YN + 10, "N", NFARBE, 30, fett=True))
    t.append(text(14, YPE + 10, "PE", GRUEN, 30, fett=True))
    t.append('<line x1="60" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>' % (YL, HX, YL, LFARBE))
    t.append('<line x1="60" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>' % (YN, HX, YN, NFARBE))
    t.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (HX, YL, HX, YL + 18, LFARBE))
    t.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (HX, YN - 18, HX, YN, NFARBE))
    # N und PE an der Erde (Netz)
    t.append('<line x1="60" y1="%d" x2="60" y2="%d" stroke="%s" stroke-width="4"/>' % (YN, YE - 30, NFARBE))
    t.append('<circle cx="60" cy="%d" r="6" fill="%s"/>' % (YN, NFARBE))
    t.append('<circle cx="60" cy="%d" r="6" fill="%s"/>' % (YPE, GRUEN))
    for i, bb in enumerate((34, 22, 10)):
        t.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>'
                 % (60 - bb / 2, YE - 30 + i * 8, 60 + bb / 2, YE - 30 + i * 8, TINTE))
    # PE
    pe_ende = GX0 if fall != "koerper" else 640
    t.append('<line x1="60" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="6"/>' % (YPE, pe_ende, YPE, PEFARBE))
    t.append('<line x1="60" y1="%d" x2="%d" y2="%d" stroke="#e8c21a" stroke-width="6" '
             'stroke-dasharray="14 14"/>' % (YPE, pe_ende, YPE))
    if fall != "koerper":
        t.append('<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (GX0, YPE, GRUEN))
    if fall == "koerper":
        t.append(text(655, YPE + 9, "fehlt", ROT, 26, fett=True))
    # LS
    t.append('<rect x="120" y="%d" width="70" height="30" fill="#fff" stroke="%s" stroke-width="3"/>' % (YL - 15, TINTE))
    t.append(text(155, YL - 26, "LS 16 A", TINTE, 22, "middle"))
    # FI
    t.append('<rect x="250" y="25" width="150" height="160" fill="none" stroke="%s" stroke-width="3"/>' % TINTE)
    t.append('<ellipse cx="325" cy="%d" rx="22" ry="62" fill="none" stroke="#7a6f5e" stroke-width="7"/>' % ((YL + YN) // 2))
    t.append(text(325, 18, "FI 30 mA", TINTE, 24, "middle", True))
    t.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>' % (HX, YL, HX, YL + 18, LFARBE))
    t.append('<rect x="%d" y="%d" width="24" height="%d" fill="#e8a33c" stroke="%s" stroke-width="3"/>'
             % (HX - 12, YL + 18, YN - YL - 36, TINTE))
    # Stromangaben auf L und N
    t.append(text(560, YL - 14, "hin: %s A" % fmt(w["iL"], 1 if w["iL"] >= 100 else 2), LFARBE, 28, "middle", True))
    t.append(text(560, YN + 38, "zurück: %s A" % fmt(w["iN"], 1 if w["iN"] >= 100 else 2), NFARBE, 28, "middle", True))
    # Mensch
    mensch = fall in ("koerper", "pemensch")
    if mensch:
        mx = 1060
        t.append('<g stroke="%s" stroke-width="4" fill="none">' % TINTE)
        t.append('<circle cx="%d" cy="70" r="20" fill="#fff"/>' % mx)
        t.append('<line x1="%d" y1="90" x2="%d" y2="250"/>' % (mx, mx))
        t.append('<line x1="%d" y1="250" x2="%d" y2="%d"/>' % (mx, mx - 22, YE))
        t.append('<line x1="%d" y1="250" x2="%d" y2="%d"/>' % (mx, mx + 22, YE))
        t.append('<line x1="%d" y1="120" x2="%d" y2="170"/>' % (mx, mx + 26))
        t.append('<line x1="%d" y1="120" x2="%d" y2="130"/>' % (mx, GX1))
        t.append('</g>')
        # Fehler: L beruehrt das Gehaeuse
        t.append('<polyline points="%d,%d %d,%d %d,%d %d,%d" fill="none" stroke="%s" stroke-width="4"/>'
                 % (HX + 12, YL + 30, HX + 30, YL + 20, HX + 38, YL + 42, GX1, YL + 34, ROT))
        t.append(pfeil(mx - 44, 250, mx - 44, 335, ROT))
        t.append(text(mx - 56, 318, idx("I", "K") + "= %d mA" % round(w["iK"] * 1000), ROT, 26, "end", True))
    if fall == "pemensch":
        t.append(pfeil(760, YPE + 36, 600, YPE + 36, ROT))
        t.append(text(585, YPE + 46, "Fehlerstrom " + idx("I", "PE") + "= %d A" % round(w["iPE"]), ROT, 28, "end", True))
    if fall == "kurz":
        t.append('<line x1="760" y1="%d" x2="760" y2="%d" stroke="%s" stroke-width="7"/>' % (YL, YN, ROT))
        t.append(text(730, (YL + YN) // 2 + 12, "⚡", ROT, 36, "end"))
    t.append("</svg>")
    return "".join(t)


if __name__ == "__main__":
    os.makedirs(ZIEL, exist_ok=True)
    for fall in ("normal", "koerper", "pemensch", "kurz"):
        with open(os.path.join(ZIEL, "fi-%s.svg" % fall), "w", encoding="utf-8") as f:
            f.write(schema(fall) + "\n")
        w = werte(fall)
        print(fall, {k: (round(v, 4) if v else v) for k, v in w.items()})
