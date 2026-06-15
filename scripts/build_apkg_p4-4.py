#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Physik · p4-2 Dynamik.

Basiert auf build_apkg_p4-5.py — gleiche Schema, gleiche CSS, andere Karten."""
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


# ─── Cards für p4-4 Statik von Festkörpern ──────────────────────────────────
p44_cards = [
    # Kraft als Vektor
    ("Was beschreibt eine <i>Kraft</i> vollständig — und was kommt in der Statik dazu?",
     "Eine Kraft ist ein <b>Vektor</b>: Betrag + Richtung. Einheit <b>N</b> = kg·m/s².<br>In der Statik kommt der <b>Angriffspunkt</b> hinzu — und damit die <b>Wirkungslinie</b> (Gerade durch den Kraftvektor)."),
    ("Was ist die <i>Wirkungslinie</i> einer Kraft?",
     "Die Gerade in Richtung der Kraft durch ihren Angriffspunkt. Am starren Körper darf eine Kraft <b>entlang</b> ihrer Wirkungslinie verschoben werden, ohne dass sich die Wirkung ändert — <b>quer</b> dazu nicht."),
    ("Komponenten einer Kraft (Winkel \u03c6 zur x-Achse)",
     "<b>F_x = F\u00b7cos\u03c6</b> &nbsp; und &nbsp; <b>F_y = F\u00b7sin\u03c6</b>.<br>Rückwärts: F = \u221a(F_x\u00b2 + F_y\u00b2)."),
    ("Formel für die Gewichtskraft",
     "<b>F_G = m \u00b7 g</b>, mit g = <b>9.81 m/s\u00b2</b>. Greift senkrecht nach unten am <b>Schwerpunkt</b> an."),
    # Wesentliche Kräfte
    ("Richtung der <i>Normalkraft</i> F_N",
     "<b>Senkrecht zur Auflagefläche</b>, von der Unterlage weg. Auf der schiefen Ebene: F_N = m\u00b7g\u00b7cos\u03b1 (kleiner als das volle Gewicht)."),
    ("Richtung der <i>Seilkraft</i> F_S",
     "Immer <b>entlang des Seils</b>, vom Körper weg (Seile können nur ziehen, nicht drücken)."),
    ("Richtung und Grenze der <i>Haftreibungskraft</i>",
     "Entlang der Fläche, <b>der drohenden Bewegung entgegen</b>. Maximalwert: <b>F_R \u2264 \u03bc_H \u00b7 F_N</b>."),
    # Resultierende
    ("Was ist die <i>resultierende Kraft</i>?",
     "Die <b>Vektorsumme</b> aller angreifenden Kräfte: \u20d7F_R = \u03a3 \u20d7F_i.<br>Komponentenweise: F_R,x = \u03a3F_i,x und F_R,y = \u03a3F_i,y."),
    ("Wie addiert man Kräfte grafisch?",
     "Pfeile <b>aneinanderhängen</b> (Spitze an Schaft) oder das <b>Kräfteparallelogramm</b> aufspannen. Der Schlusspfeil ist die Resultierende."),
    # Drehmoment
    ("Formel für das <i>Drehmoment</i>",
     "<b>M = F \u00b7 r = F \u00b7 l \u00b7 sin\u03b1</b><br>r = l\u00b7sin\u03b1 = wirksamer Hebelarm (senkrechter Abstand Achse\u2013Wirkungslinie). Einheit <b>Nm</b>."),
    ("Was ist der <i>wirksame Hebelarm</i> r?",
     "Der <b>senkrechte Abstand</b> zwischen Drehachse und Wirkungslinie der Kraft: r = l\u00b7sin\u03b1. Nur er zählt für die Drehwirkung."),
    ("Bei welchem Winkel ist das Drehmoment maximal? Wann null?",
     "<b>Maximal</b> bei \u03b1 = 90\u00b0 (Kraft senkrecht zum Hebel, sin\u03b1 = 1).<br><b>Null</b>, wenn die Kraft auf die Drehachse zeigt (\u03b1 = 0\u00b0)."),
    ("Vorzeichen-Konvention beim Drehmoment",
     "Drehung im <b>Gegenuhrzeigersinn positiv</b>, im <b>Uhrzeigersinn negativ</b>."),
    ("Warum setzt man einen Schraubenschlüssel möglichst rechtwinklig an?",
     "Weil M = F\u00b7l\u00b7sin\u03b1 bei \u03b1 = 90\u00b0 maximal ist. Schräges Ziehen verschenkt Drehwirkung (der Faktor sin\u03b1 wird kleiner als 1)."),
    # Hebelgesetz
    ("Das <i>Hebelgesetz</i>",
     "<b>F_1 \u00b7 r_1 = F_2 \u00b7 r_2</b> (Gleichgewicht der Momente).<br>Das <b>leichtere</b> Gewicht muss <b>weiter aussen</b> sitzen."),
    ("Auf einer Wippe: warum gleicht ein leichtes Kind weit aussen ein schweres nahe der Achse aus?",
     "Weil das <b>Drehmoment</b> zählt (M = m\u00b7g\u00b7r), nicht die Masse allein. Grosser Hebelarm gleicht kleine Masse aus. Das g kürzt sich heraus."),
    # Gleichgewicht
    ("Die zwei Bedingungen für statisches Gleichgewicht",
     "<b>\u03a3 \u20d7F = \u20d70</b> (keine Beschleunigung) <b>und</b> <b>\u03a3 M = 0</b> (keine Rotation). Beide gleichzeitig!"),
    ("Worin zerfällt die Kräftebedingung \u03a3\u20d7F = 0?",
     "In zwei skalare Gleichungen: <b>\u03a3F_x = 0</b> und <b>\u03a3F_y = 0</b>."),
    ("Wie wählt man die Drehachse für die Momentengleichung?",
     "Sie ist <b>frei wählbar</b>. Geschickt legt man sie dorthin, wo eine <b>unbekannte Kraft angreift</b> — dann fällt diese (Hebelarm = 0) aus der Momentengleichung heraus."),
    # Seilkräfte
    ("Last an zwei Seilen (Winkel \u03b1 links, \u03b2 rechts zur Horizontalen)",
     "S\u2081 = F_G \u00b7 cos\u03b2 / sin(\u03b1+\u03b2) &nbsp; und &nbsp; S\u2082 = F_G \u00b7 cos\u03b1 / sin(\u03b1+\u03b2).<br>Folgt aus \u03a3F_x = 0 und \u03a3F_y = 0 am Knoten."),
    ("Welches von zwei Seilen ist stärker belastet?",
     "Das <b>steilere</b> Seil — es hat den grösseren vertikalen Kraftanteil und trägt daher mehr vom Gewicht."),
    ("Warum stehen straff gespannte Seile unter enormer Zugkraft?",
     "Bei kleinen Winkeln zur Horizontalen wird sin(\u03b1+\u03b2) klein, also die Seilkraft gross. Flache Seile können das Gewicht <b>um ein Vielfaches</b> übersteigen (durchhängende Wäscheleine)."),
    # Auflagerkräfte
    ("Auflagerkräfte am Balken (Last F_G im Abstand x von A, Stützweite L)",
     "F_B = F_G \u00b7 x/L &nbsp; und &nbsp; F_A = F_G \u00b7 (1 \u2212 x/L).<br>Drehachse bei A, dann \u03a3M_A = 0 und \u03a3F_y = 0."),
    ("Wie kontrolliert man die Auflagerkräfte?",
     "Über die Kräftebedingung: <b>F_A + F_B = F_ges</b> (Summe aller Lasten). Stimmt das, ist die Rechnung konsistent."),
    ("Welche Stütze eines Balkens trägt mehr?",
     "Die Stütze, die <b>näher an der Last</b> liegt. Bei mehreren Lasten summiert man die einzelnen Momente."),
    # Schiefe Ebene
    ("Zerlegung der Gewichtskraft auf der schiefen Ebene",
     "<b>F_H = F_G\u00b7sin\u03b1</b> (hangabwärts) &nbsp; und &nbsp; <b>F_N = F_G\u00b7cos\u03b1</b> (senkrecht zur Ebene)."),
    ("Haftbedingung auf der schiefen Ebene",
     "Der Körper bleibt liegen, solange <b>F_H \u2264 \u03bc_H\u00b7F_N</b>, also <b>tan\u03b1 \u2264 \u03bc_H</b>. F_G kürzt sich heraus."),
    ("Grenzwinkel auf der schiefen Ebene",
     "<b>\u03b1_max = arctan(\u03bc_H)</b>. Hängt <b>nur</b> vom Reibungskoeffizienten ab \u2014 nicht von der Masse."),
    ("Warum verrät der Kipp-/Grenzwinkel direkt die Haftreibungszahl?",
     "Weil im Grenzfall tan\u03b1 = \u03bc_H gilt. Misst man den Winkel, bei dem ein Körper gerade zu rutschen beginnt, ist \u03bc_H = tan\u03b1."),
    # Methodik
    ("Rezept für Statik-Aufgaben",
     "1. <b>Freikörperbild</b> zeichnen (alle Kräfte am Körper). 2. Bei Drehproblemen mit der <b>Momentengleichung</b> beginnen, Drehachse bei einer Unbekannten. 3. Dann \u03a3F_x = 0 und \u03a3F_y = 0. 4. Auflösen."),
    ("Einheit Newtonmeter",
     "<b>1 Nm = 1 N \u00b7 m</b> \u2014 die Einheit des Drehmoments. Nicht zu verwechseln mit dem Joule (auch N\u00b7m, aber Energie/Arbeit)."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p4-4-statik', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::Mechanik::p4-4 Statik',
                   'TALS Physik \u00b7 Statik von Festkörpern: Kraft als Vektor und Wirkungslinie, Komponentenzerlegung, Resultierende, Drehmoment und Hebelgesetz, statisches Gleichgewicht, Seilkräfte am Knoten, Auflagerkräfte am Balken, schiefe Ebene und Haftbedingung.',
                   p44_cards)
    print(f"p4-4-statik: {n} Karten erzeugt -> {out_path}")

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
