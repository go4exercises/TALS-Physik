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


# ─── Cards für p4-2 Dynamik ────────────────────────────────────────────────
p42_cards = [
    # Kraft & Masse
    ("Was ist eine <i>Kraft</i> und welche Einheit hat sie?",
     "Eine Kraft ist die <b>Ursache jeder Bewegungs- oder Formänderung</b>. Sie ist ein <b>Vektor</b> (Betrag + Richtung).<br>Einheit: <b>N</b> (Newton) = kg·m/s²."),
    ("Unterschied zwischen <i>Masse</i> und <i>Gewichtskraft</i>?",
     "<b>Masse</b> m (in kg): Mass für die Trägheit, überall gleich.<br><b>Gewichtskraft</b> F_G = m·g (in N): ortsabhängig (auf dem Mond kleiner). Die Masse bleibt dort dieselbe."),
    ("Formel für die Gewichtskraft",
     "<b>F_G = m · g</b>, mit g = <b>9.81 m/s²</b>.<br>Beispiel: 1 kg wiegt ≈ 9.81 N."),
    # Newtonsche Gesetze
    ("1. Newtonsches Gesetz (Trägheitsgesetz)",
     "Wirkt <b>keine Gesamtkraft</b> (F_ges = 0), so bleibt der Körper in <b>Ruhe</b> oder in <b>gleichförmiger, geradliniger Bewegung</b> (v = konstant)."),
    ("2. Newtonsches Gesetz (Grundgesetz)",
     "<b>F_ges = m · a</b><br>Die Gesamtkraft erzeugt eine gleichgerichtete Beschleunigung. Doppelte Kraft → doppelte Beschleunigung; doppelte Masse → halbe Beschleunigung."),
    ("3. Newtonsches Gesetz (Wechselwirkung)",
     "<b>actio = reactio</b>: F<sub>A→B</sub> = −F<sub>B→A</sub>.<br>Beide Kräfte sind gleich gross, entgegengesetzt — greifen aber an <b>verschiedenen Körpern</b> an und heben sich daher <b>nicht</b> auf."),
    ("Warum heben sich actio und reactio nicht auf?",
     "Weil sie an <b>zwei verschiedenen Körpern</b> angreifen. Nur Kräfte am <i>selben</i> Körper können sich zur Gesamtkraft null addieren."),
    ("Beispiel für das Trägheitsgesetz im Alltag",
     "Beim Bremsen wird man nach vorne „gedrückt“: der Körper <b>behält</b> seine Geschwindigkeit bei (Trägheit), während das Auto verzögert. Erst der Gurt liefert die bremsende Kraft."),
    # Federkraft
    ("Hookesches Gesetz (Federkraft)",
     "<b>F = D · s</b><br>D = Federkonstante (Federhärte) in <b>N/m</b>, s = Auslenkung. Gilt nur im elastischen Bereich."),
    ("Was bedeutet eine grosse Federkonstante D?",
     "Eine <b>harte</b> Feder — man braucht viel Kraft für wenig Dehnung. Kleines D = weiche Feder."),
    ("Dehnung einer Feder unter angehängter Masse",
     "Im Gleichgewicht trägt die Federkraft die Gewichtskraft:<br><b>D · s = m · g</b> → s = m·g / D."),
    # Reibung
    ("Formel für die Reibungskraft",
     "<b>F_R = μ · F_N</b><br>μ = Reibungszahl (dimensionslos), F_N = Normalkraft. Die Reibung wirkt <b>entgegen</b> der Bewegung."),
    ("Unterschied Haft- und Gleitreibung?",
     "<b>Haftreibung</b>: solange der Körper ruht, bis maximal μ_H·F_N.<br><b>Gleitreibung</b>: während der Bewegung, fester Wert μ_G·F_N.<br>Meist μ_H ≥ μ_G → Anfahren braucht mehr Kraft als Weiterschieben."),
    ("Wovon hängt die Reibungskraft <i>nicht</i> ab?",
     "Nicht von der <b>Grösse der Auflagefläche</b> und (in guter Näherung) nicht von der Geschwindigkeit — nur von Materialpaar (μ) und Normalkraft F_N."),
    ("Normalkraft auf waagrechtem Boden",
     "<b>F_N = m · g</b>. Auf der schiefen Ebene dagegen F_N = m·g·cosα (kleiner als das volle Gewicht)."),
    # Schiefe Ebene
    ("Hangabtriebskraft auf der schiefen Ebene",
     "<b>F_H = m · g · sinα</b> — parallel zur Ebene, treibt den Körper hangabwärts."),
    ("Normalkraft auf der schiefen Ebene",
     "<b>F_N = m · g · cosα</b> — senkrecht zur Ebene, drückt den Körper auf die Unterlage."),
    ("Beschleunigung auf der schiefen Ebene (mit Reibung)",
     "<b>a = g · (sinα − μ·cosα)</b><br>Massenunabhängig! Ohne Reibung: a = g·sinα."),
    ("Wann bleibt ein Körper auf der schiefen Ebene liegen?",
     "Solange die Haftreibung den Hangabtrieb hält: <b>tanα ≤ μ_H</b>. Der Grenzwinkel verrät direkt die Haftreibungszahl."),
    # Atwood & Anwendungen
    ("Beschleunigung der Atwoodschen Fallmaschine",
     "<b>a = (m₁ − m₂)·g / (m₁ + m₂)</b><br>Die Gewichtsdifferenz treibt an, beschleunigt werden beide Massen zusammen."),
    ("Fadenkraft bei der Atwood-Maschine",
     "Über die aufsteigende Masse: <b>F = m₂·(g + a)</b>.<br>Kontrolle über die absteigende: F = m₁·(g − a). Beide ergeben denselben Wert."),
    ("Scheinbares Gewicht im beschleunigten Aufzug",
     "<b>F_N = m·(g + a)</b> (a positiv = nach oben).<br>Nach oben → schwerer; nach unten → leichter; freier Fall (a = −g) → F_N = 0 (Schwerelosigkeit)."),
    ("Bremsbeschleunigung beim blockierten Rad",
     "Aus m·a = μ·m·g fällt die Masse heraus: <b>a = μ · g</b>. Der Bremsweg ist daher massenunabhängig (s = v² / (2a))."),
    ("Warum wird die kleinere Masse beim Abstossen stärker beschleunigt?",
     "Wegen actio = reactio wirkt auf beide dieselbe Kraft F. Mit a = F/m bekommt die <b>kleinere Masse die grössere Beschleunigung</b>."),
    # Verständnis / Methodik
    ("Vorgehen bei Dynamik-Aufgaben (Rezept)",
     "1. <b>Kräfteskizze</b> zeichnen (alle Kräfte am Körper). 2. <b>Gesamtkraft</b> in Bewegungsrichtung bilden. 3. <b>F_ges = m·a</b> ansetzen und nach der gesuchten Grösse auflösen."),
    ("Was bedeutet „die Gesamtkraft zählt“?",
     "Nur die <b>Resultierende</b> aller Kräfte bestimmt die Beschleunigung. Einzelne Kräfte können sich aufheben (F_ges = 0 → keine Beschleunigung trotz wirkender Kräfte)."),
    ("Einheit Newton in Basiseinheiten",
     "<b>1 N = 1 kg·m/s²</b> — folgt direkt aus F = m·a."),
    ("Typische Haftreibungszahl Gummi auf trockenem Asphalt",
     "μ_H ≈ <b>0.9</b> (Gleitreibung ≈ 0.7). Deshalb ist eine Vollbremsung mit rollenden Rädern (ABS) effektiver als mit blockierten."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p4-2-dynamik', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::Mechanik::p4-2 Dynamik',
                   'TALS Physik · Dynamik: Kraft, die drei Newtonschen Gesetze, Federkraft (Hooke), Haft- und Gleitreibung, schiefe Ebene, Atwoodsche Fallmaschine, scheinbares Gewicht.',
                   p42_cards)
    print(f"p4-2-dynamik: {n} Karten erzeugt -> {out_path}")

    # Test
    import tempfile
    sz = os.path.getsize(out_path)
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(out_path) as z:
            z.extractall(td)
        con = sqlite3.connect(os.path.join(td, 'collection.anki2'))
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM notes")
        n_notes = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM cards")
        n_cards = cur.fetchone()[0]
        con.close()
    print(f"  {sz} bytes, {n_notes} notes, {n_cards} cards")
