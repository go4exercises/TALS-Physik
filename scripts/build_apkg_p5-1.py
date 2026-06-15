#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Physik · p5-1 Temperatur.

Basiert auf build_apkg_p4-4.py — gleiches Schema, gleiche CSS, andere Karten."""
import sqlite3, zipfile, json, hashlib, random, string, os, sys

SCHEMA = """
CREATE TABLE col (id integer PRIMARY KEY, crt integer NOT NULL, mod integer NOT NULL, scm integer NOT NULL, ver integer NOT NULL, dty integer NOT NULL, usn integer NOT NULL, ls integer NOT NULL, conf text NOT NULL, models text NOT NULL, decks text NOT NULL, dconf text NOT NULL, tags text NOT NULL);
CREATE TABLE notes (id integer PRIMARY KEY, guid text NOT NULL, mid integer NOT NULL, mod integer NOT NULL, usn integer NOT NULL, tags text NOT NULL, flds text NOT NULL, sfld text NOT NULL, csum integer NOT NULL, flags integer NOT NULL, data text NOT NULL);
CREATE TABLE cards (id integer PRIMARY KEY, nid integer NOT NULL, did integer NOT NULL, ord integer NOT NULL, mod integer NOT NULL, usn integer NOT NULL, type integer NOT NULL, queue integer NOT NULL, due integer NOT NULL, ivl integer NOT NULL, factor integer NOT NULL, reps integer NOT NULL, lapses integer NOT NULL, left integer NOT NULL, odue integer NOT NULL, odid integer NOT NULL, flags integer NOT NULL, data text NOT NULL);
CREATE TABLE revlog (id integer PRIMARY KEY, cid integer NOT NULL, usn integer NOT NULL, ease integer NOT NULL, ivl integer NOT NULL, lastIvl integer NOT NULL, factor integer NOT NULL, time integer NOT NULL, type integer NOT NULL);
CREATE TABLE graves (usn integer NOT NULL, oid integer NOT NULL, type integer NOT NULL);
CREATE INDEX ix_notes_usn ON notes (usn);
CREATE INDEX ix_cards_usn ON cards (usn);
CREATE INDEX ix_revlog_usn ON revlog (usn);
CREATE INDEX ix_cards_nid ON cards (nid);
CREATE INDEX ix_cards_sched ON cards (did, queue, due);
CREATE INDEX ix_revlog_cid ON revlog (cid);
CREATE INDEX ix_notes_csum ON notes (csum);
"""

CSS = ".card { font-family: 'Source Sans 3','Helvetica Neue',sans-serif; font-size: 18px; color: #1a1a1a; background: #f8f5ee; padding: 18px; line-height: 1.5; }i { color: #8a4a0e; font-style: italic; }b { color: #1a1a1a; }hr#answer { border: 0; border-top: 1px solid #c8c2b0; margin: 14px 0; }"


def guid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def fnv32(s):
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b
        h = (h * 0x01000193) & 0xffffffff
    return h


def build_apkg(out_path, deck_name, deck_desc, cards):
    random.seed(hash(deck_name))
    base = abs(hash(deck_name))
    deck_id = (base & 0xffffffffffff) | 0x100000000000
    model_id = ((base >> 16) & 0xffffffffffff) | 0x100000000000
    crt = 1778025600
    mod = 1778050418

    conf = {"nextPos": 1, "estTimes": True, "activeDecks": [deck_id], "sortType": "noteFld",
            "timeLim": 0, "sortBackwards": False, "addToCur": True, "curDeck": deck_id,
            "newBury": True, "newSpread": 0, "dueCounts": True, "curModel": str(model_id),
            "collapseTime": 1200}

    models = {str(model_id): {
        "id": model_id, "name": "TALS Basic", "type": 0, "mod": mod, "usn": -1,
        "sortf": 0, "did": deck_id,
        "tmpls": [{"name": "Karte 1", "ord": 0, "qfmt": "{{Front}}",
                   "afmt": "{{Front}}<hr id=\"answer\">{{Back}}",
                   "did": None, "bqfmt": "", "bafmt": ""}],
        "flds": [{"name": "Front", "ord": 0, "sticky": False, "rtl": False,
                  "font": "Source Sans 3", "size": 16, "media": []},
                 {"name": "Back", "ord": 1, "sticky": False, "rtl": False,
                  "font": "Source Sans 3", "size": 16, "media": []}],
        "css": CSS,
        "latexPre": "\\documentclass[12pt]{article}\\usepackage{amssymb,amsmath}\\begin{document}",
        "latexPost": "\\end{document}",
        "req": [[0, "any", [0]]], "tags": [], "vers": []
    }}

    decks = {str(deck_id): {
        "id": deck_id, "name": deck_name, "extendRev": 50, "usn": -1, "collapsed": False,
        "newToday": [0, 0], "revToday": [0, 0], "lrnToday": [0, 0], "timeToday": [0, 0],
        "dyn": 0, "extendNew": 10, "conf": 1, "desc": deck_desc, "mod": mod,
        "browserCollapsed": False
    }}

    dconf = {"1": {"id": 1, "name": "Default", "replayq": True,
                   "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0},
                   "rev": {"perDay": 200, "ivlFct": 1.0, "maxIvl": 36500, "minSpace": 1, "ease4": 1.3,
                           "bury": False, "fuzz": 0.05, "hardFactor": 1.2},
                   "timer": 0, "maxTaken": 60, "usn": -1,
                   "new": {"perDay": 20, "delays": [1, 10], "separate": True, "ints": [1, 4, 7],
                           "initialFactor": 2500, "bury": False, "order": 1},
                   "mod": 0, "autoplay": True, "dyn": False}}

    tmp_db = out_path + '.tmp.sqlite'
    if os.path.exists(tmp_db):
        os.remove(tmp_db)
    con = sqlite3.connect(tmp_db)
    cur = con.cursor()
    cur.executescript(SCHEMA)
    cur.execute("INSERT INTO col VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (1, crt, mod, mod * 1000, 11, 0, 0, 0,
                 json.dumps(conf), json.dumps(models), json.dumps(decks), json.dumps(dconf), "{}"))

    note_base = mod * 1000
    for i, (front, back) in enumerate(cards):
        nid = note_base + i
        cid = nid + 1000000
        flds = front + "\x1f" + back
        sfld = front
        csum = fnv32(sfld) >> 0
        cur.execute("INSERT INTO notes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (nid, guid(), model_id, mod, -1, "", flds, sfld, csum, 0, ""))
        cur.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (cid, nid, deck_id, 0, mod, -1, 0, 0, i + 1, 0, 0, 0, 0, 0, 0, 0, 0, ""))
    con.commit()
    con.close()

    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(tmp_db, 'collection.anki2')
        z.writestr('media', '{}')
    os.remove(tmp_db)
    return len(cards)


# ─── Cards für p5-1 Temperatur ──────────────────────────────────
p51_cards = [
    # Temperatur als Teilchengrösse
    ("Was misst die <i>Temperatur</i> auf der Ebene der Teilchen?",
     "Die <b>mittlere Bewegungsenergie</b> der Teilchen (thermische Bewegung). Je höher die Temperatur, desto schneller bewegen sie sich im Mittel. Die Temperatur ist eine <b>Zustandsgrösse</b>."),
    ("Warum ist \u201edoppelte Temperatur = doppeltes Teilchentempo\u201c falsch?",
     "Das mittlere Tempo w\u00e4chst nur mit der <b>Wurzel</b> der absoluten Temperatur. Doppeltes T \u2192 Tempo nur \u00b7\u221a2 \u2248 1.41. Ausserdem z\u00e4hlt die <b>absolute</b> Temperatur, nicht die Celsius-Zahl."),
    ("Misst die Temperatur die Geschwindigkeit <i>eines</i> Teilchens?",
     "Nein \u2014 nur den <b>Mittelwert</b> \u00fcber sehr viele Teilchen. Einzelne Teilchen sind schneller oder langsamer."),
    ("Was ist die <i>Brown'sche Bewegung</i>?",
     "Der unregelm\u00e4ssige Zufallsweg eines sichtbaren Teilchens in einer Fl\u00fcssigkeit, verursacht durch zuf\u00e4llige St\u00f6sse unz\u00e4hliger bewegter Fl\u00fcssigkeitsteilchen. Belegt: Materie besteht aus bewegten Teilchen."),
    ("Was passiert mit der Brown'schen Bewegung beim Erw\u00e4rmen?",
     "Sie wird <b>heftiger und schneller</b> \u2014 die St\u00f6sse werden kr\u00e4ftiger und h\u00e4ufiger, weil die Teilchenbewegung mit der Temperatur zunimmt."),
    # Aggregatzustände
    ("Teilchenmodell: <i>fester</i> Zustand",
     "Teilchen sitzen an <b>festen Pl\u00e4tzen</b> und schwingen nur um ihre Ruhelage (oft kristallin). Eigenschaft: formstabil, starr."),
    ("Teilchenmodell: <i>fl\u00fcssiger</i> Zustand",
     "Teilchen ber\u00fchren sich noch, sind aber <b>gegeneinander verschiebbar</b>. Eigenschaft: nimmt Gef\u00e4ssform an, kaum pressbar, freie Oberfl\u00e4che."),
    ("Teilchenmodell: <i>gasf\u00f6rmiger</i> Zustand",
     "Grosse Abst\u00e4nde, Teilchen <b>fliegen frei</b> und stossen nur gelegentlich. Eigenschaft: f\u00fcllt jeden Raum aus, leicht komprimierbar."),
    ("Wie heissen die \u00dcberg\u00e4nge fest\u2194fl\u00fcssig?",
     "fest \u2192 fl\u00fcssig: <b>schmelzen</b>; fl\u00fcssig \u2192 fest: <b>erstarren</b>."),
    ("Wie heissen die \u00dcberg\u00e4nge fl\u00fcssig\u2194gasf\u00f6rmig?",
     "fl\u00fcssig \u2192 gasf\u00f6rmig: <b>verdampfen</b>; gasf\u00f6rmig \u2192 fl\u00fcssig: <b>kondensieren</b>."),
    ("Bei welchen Temperaturen schmilzt/siedet Wasser (Normaldruck)?",
     "Schmelzen bei <b>0 \u00b0C</b>, verdampfen (sieden) bei <b>100 \u00b0C</b>."),
    # Celsius-Skala
    ("Welche Fixpunkte definieren die <i>Celsius-Skala</i>?",
     "Schmelzpunkt des Eises = <b>0 \u00b0C</b>, Siedepunkt des Wassers = <b>100 \u00b0C</b> (Normaldruck). Der Abstand wird in 100 gleiche Schritte geteilt."),
    ("Warum ist die Celsius-Skala \u201ewillk\u00fcrlich\u201c?",
     "Ihre Fixpunkte sind an einen bestimmten Stoff \u2014 Wasser \u2014 gebunden. Praktisch (Wasser \u00fcberall verf\u00fcgbar), aber nicht physikalisch zwingend."),
    ("Welches Symbol nutzt man f\u00fcr die Celsius-Temperatur?",
     "<b>\u03d1</b> (Theta), Einheit <b>\u00b0C</b>."),
    # Kelvin / absoluter Nullpunkt
    ("Was ist der <i>absolute Nullpunkt</i>?",
     "Die <b>tiefstm\u00f6gliche Temperatur</b> (minimale Teilchenbewegung). Liegt bei <b>\u2212273.15 \u00b0C = 0 K</b> und kann prinzipiell nie ganz erreicht werden."),
    ("Was zeichnet die <i>Kelvin-Skala</i> aus?",
     "Nullpunkt am absoluten Nullpunkt, <b>keine negativen Werte</b>, gleiche Schrittweite wie Celsius. Symbol <b>T</b>, Einheit <b>K</b>. Physikalisch begr\u00fcndet."),
    ("Warum gibt es keine negativen Kelvin-Temperaturen?",
     "Weil der absolute Nullpunkt (0 K) die tiefstm\u00f6gliche Temperatur ist \u2014 es gibt nichts K\u00e4lteres, also nichts unter 0 K."),
    ("0 K entspricht wie viel Grad Celsius?",
     "<b>0 K = \u2212273.15 \u00b0C</b>."),
    ("Warum sagt man nie \u201eGrad Kelvin\u201c?",
     "Kelvin ist eine eigene SI-Basiseinheit; man sagt nur <b>\u201eKelvin\u201c</b> bzw. \u201e20 K\u201c \u2014 ohne \u201eGrad\u201c."),
    # Umrechnung
    ("Umrechnung Celsius \u2192 Kelvin",
     "<b>T = \u03d1 + 273.15</b> (T in K, \u03d1 in \u00b0C)."),
    ("Umrechnung Kelvin \u2192 Celsius",
     "<b>\u03d1 = T \u2212 273.15</b>."),
    ("Was gilt f\u00fcr eine <i>Temperaturdifferenz</i>?",
     "<b>\u0394T = \u0394\u03d1</b> \u2014 eine Erw\u00e4rmung um 1 \u00b0C ist genau 1 K. Der verschobene Nullpunkt f\u00e4llt bei der Differenz heraus."),
    ("Einzelwert vs. Differenz \u2014 wo unterscheiden sich die Skalen?",
     "Einzelne Werte unterscheiden sich um <b>273.15</b> (T = \u03d1 + 273.15). Eine <b>Differenz</b> ist in beiden Skalen <b>zahlengleich</b> (\u0394T = \u0394\u03d1)."),
    ("37 \u00b0C in Kelvin?",
     "T = 37 + 273.15 = <b>310.15 K</b>."),
    ("300 K in Grad Celsius?",
     "\u03d1 = 300 \u2212 273.15 = <b>26.85 \u00b0C</b>."),
    ("Flüssiger Stickstoff siedet bei 77 K \u2014 wie viel \u00b0C?",
     "\u03d1 = 77 \u2212 273.15 = <b>\u2212196.15 \u00b0C</b>."),
    # Absoluter Nullpunkt über Extrapolation
    ("Woher kennt man den absoluten Nullpunkt, wenn man ihn nicht erreichen kann?",
     "Durch <b>Extrapolation</b>: Bei konstantem Volumen ist der Gasdruck proportional zur absoluten Temperatur (p \u221d T). Verl\u00e4ngert man die p-\u03d1-Gerade bis p = 0, trifft sie die Achse bei \u2212273.15 \u00b0C \u2014 f\u00fcr jedes Gas gleich."),
    ("Welcher Zusammenhang gilt f\u00fcr Gasdruck und Temperatur bei konstantem Volumen?",
     "<b>p \u221d T</b> (Druck proportional zur <b>absoluten</b> Temperatur). Druck null \u21d4 T = 0 K = \u2212273.15 \u00b0C."),
    ("Warum treffen sich die p-\u03d1-Geraden verschiedener Gase im selben Punkt?",
     "Weil f\u00fcr jedes (ideale) Gas p \u221d T gilt: Bei p = 0 ist T = 0 K, also \u03d1 = \u2212273.15 \u00b0C \u2014 unabh\u00e4ngig vom Gas."),
    # Methodik / Merksätze
    ("Merksatz: Was ist Temperatur, kurz?",
     "Ein Mass daf\u00fcr, wie <b>heftig sich die Teilchen bewegen</b> (mittlere Bewegungsenergie)."),
    ("Celsius vs. Kelvin \u2014 der Kernunterschied",
     "Celsius: an Wasser-Fixpunkte gebunden, praktisch, <b>willk\u00fcrlich</b>. Kelvin: beginnt am absoluten Nullpunkt, <b>physikalisch begr\u00fcndet</b>. Gleiche Schrittweite \u2192 T = \u03d1 + 273.15."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p5-1-temperatur', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::Thermodynamik::p5-1 Temperatur',
                   'TALS Physik \u00b7 Temperatur: Temperatur als Mass der mittleren Teilchenbewegung, Brown\u2019sche Bewegung, Aggregatzust\u00e4nde und ihre \u00dcberg\u00e4nge, Celsius- und Kelvin-Skala, absoluter Nullpunkt, Umrechnung T = \u03d1 + 273.15 und Temperaturdifferenz \u0394T = \u0394\u03d1.',
                   p51_cards)
    print(f"p5-1-temperatur: {n} Karten erzeugt -> {out_path}")

    import tempfile
    sz = os.path.getsize(out_path)
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(out_path) as z:
            z.extractall(td)
        con = sqlite3.connect(os.path.join(td, 'collection.anki2'))
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM notes"); n_notes = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM cards"); n_cards = cur.fetchone()[0]
        con.close()
    print(f"  {sz} bytes, {n_notes} notes, {n_cards} cards")
