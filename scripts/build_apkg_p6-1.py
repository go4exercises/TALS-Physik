#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Physik · p5-3 Wärmeausdehnung.

Basiert auf build_apkg_p5-2.py — gleiches Schema, gleiche CSS, andere Karten."""
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


# ─── Cards für p6-1 Wellen ──────────────────────────────────
p61_cards = [
    # Schwingung & Grundbegriffe
    ("Was ist eine Schwingung?",
     "Eine <b>periodische Bewegung um eine Ruhelage</b>. Die Periode \\u0054 ist die Dauer einer vollen Schwingung."),
    ("Zusammenhang von Frequenz f und Periode T?",
     "<b>f = 1 / T</b>. Einheit der Frequenz: <b>Hz = 1/s</b> (Anzahl Schwingungen pro Sekunde)."),
    ("Wie entsteht aus einer Schwingung eine Welle?",
     "Koppelt man viele schwingfähige Teilchen, überträgt sich die Schwingung von einem zum nächsten \\u2014 es entsteht eine <b>Welle</b>."),
    ("Was transportiert eine Welle \\u2014 und was nicht?",
     "Eine Welle transportiert <b>Energie</b>, aber <b>keine Materie</b>. Jeder Punkt schwingt nur um seine Ruhelage (z.\\u00a0B. Korken auf Wasser)."),
    ("Was ist die Amplitude einer Welle?",
     "Die <b>maximale Auslenkung</b> aus der Ruhelage."),
    ("Was ist die Wellenlänge \\u03bb?",
     "Der <b>Abstand zwischen zwei benachbarten Wellenbergen</b>. In einer Periode T rückt die Welle genau um \\u03bb weiter."),
    # Wellengleichung
    ("Wie lautet die Wellengleichung?",
     "<b>c = \\u03bb \\u00b7 f = \\u03bb / T</b>. c ist die Phasen- bzw. Ausbreitungsgeschwindigkeit."),
    ("Wovon hängt die Geschwindigkeit c einer mechanischen Welle ab?",
     "Nur vom <b>Medium</b>, <b>nicht</b> von der Frequenz. Höhere Frequenz bedeutet bei gleichem Medium eine <b>kürzere</b> Wellenlänge."),
    # Wellentypen
    ("Transversalwelle \\u2014 Schwingungsrichtung und Beispiele?",
     "Die Teilchen schwingen <b>quer (senkrecht)</b> zur Ausbreitung. Beispiele: Seilwelle, Wasserwelle, Licht."),
    ("Longitudinalwelle \\u2014 Schwingungsrichtung und Beispiele?",
     "Die Teilchen schwingen <b>längs (in Ausbreitungsrichtung)</b>; es entstehen Verdichtungen und Verdünnungen. Beispiele: Schall, Druckwellen."),
    ("Ist Schall transversal oder longitudinal?",
     "<b>Longitudinal</b> \\u2014 eine Welle aus Druckschwankungen längs der Ausbreitungsrichtung."),
    ("Ist Licht transversal oder longitudinal?",
     "<b>Transversal</b> \\u2014 elektrisches und magnetisches Feld schwingen quer zur Ausbreitung."),
    # Mechanische Wellen & Schall
    ("Was brauchen mechanische Wellen zur Ausbreitung?",
     "Ein <b>Medium</b> (fest, flüssig oder gasförmig) mit gekoppelten Teilchen. Beispiele: Wasser-, Erdbeben- und Schallwellen."),
    ("Schallgeschwindigkeit in Luft (15 \\u00b0C)?",
     "Etwa <b>340 m/s</b> (bei 25 \\u00b0C ca. 346 m/s)."),
    ("Wo ist der Schall schneller \\u2014 Luft, Wasser oder Stahl?",
     "Im <b>festen Stoff</b> am schnellsten: Stahl \\u2248 5170 m/s, Wasser \\u2248 1500 m/s, Luft \\u2248 340 m/s."),
    ("Hörbereich des menschlichen Ohrs?",
     "Etwa <b>20 Hz bis 20 kHz</b>; unter 50 Hz wird es schwierig."),
    # Elektromagnetische Wellen
    ("Was unterscheidet elektromagnetische von mechanischen Wellen?",
     "EM-Wellen brauchen <b>kein Medium</b> und breiten sich auch im <b>Vakuum</b> aus. Sie bestehen aus schwingenden E- und B-Feldern (transversal)."),
    ("Lichtgeschwindigkeit im Vakuum?",
     "<b>c \\u2248 3 \\u00b7 10\\u2078 m/s</b> (genauer 2.998 \\u00b7 10\\u2078 m/s). Gilt für <b>alle</b> EM-Wellen im Vakuum."),
    ("Welcher Bereich des EM-Spektrums ist sichtbares Licht?",
     "Nur ein <b>winziger Ausschnitt</b>: etwa <b>380 nm (violett) bis 780 nm (rot)</b>."),
    ("Ordne nach zunehmender Wellenlänge: Gamma, Radio, sichtbar, Mikrowellen.",
     "<b>Gammastrahlung &lt; sichtbares Licht &lt; Mikrowellen &lt; Radiowellen</b> (Gamma am kürzesten, Radio am längsten)."),
    # Lichterzeugung
    ("Drei Arten der Lichterzeugung?",
     "(1) <b>Wärmestrahlung</b> (Glühlampe, Sonne), (2) <b>atomare Emission</b> (Leuchtstoffröhre), (3) <b>Laser</b> (stimulierte Emission)."),
    ("Was ist ein Photon?",
     "Ein <b>Energiequant des Lichts</b> \\u2014 das kleinste Energiepaket einer EM-Welle."),
    ("Wie entsteht Licht bei der atomaren Emission?",
     "Ein <b>angeregtes Atom</b> springt auf ein tieferes Energieniveau zurück und gibt dabei ein <b>Photon</b> ab \\u2014 in zufälliger Richtung."),
    ("Was bedeutet die Abkürzung LASER?",
     "<b>Light Amplification by Stimulated Emission of Radiation</b> \\u2014 Lichtverstärkung durch stimulierte Emission."),
    ("Was zeichnet Laserlicht aus?",
     "Es ist <b>kohärent</b>, <b>einfarbig</b> (eine Wellenlänge) und <b>stark gebündelt</b> \\u2014 anders als das breite, ungerichtete Glühlampenlicht."),
    # Absorption & Treibhauseffekt
    ("Wovon hängt ab, wie stark ein Stoff Strahlung absorbiert?",
     "Von der <b>Wellenlänge</b> der Strahlung (wellenlängenabhängige Absorption)."),
    ("Warum ist die Atmosphäre für Sonnenlicht durchlässig, für Wärmestrahlung aber nicht?",
     "Das <b>kurzwellige</b>, sichtbare Sonnenlicht wird durchgelassen; die vom Boden abgegebene <b>langwellige</b> Infrarot-Wärmestrahlung wird von Treibhausgasen absorbiert."),
    ("Erkläre den Treibhauseffekt.",
     "Sonnenlicht erwärmt den Boden; dessen langwellige Wärmestrahlung wird von <b>Treibhausgasen (CO\\u2082, Wasserdampf)</b> absorbiert und teilweise zurückgestrahlt \\u2014 Energie bleibt in Bodennähe, es wird wärmer."),
    ("Welche Rolle spielen Treibhausgase?",
     "Sie <b>absorbieren die langwellige Wärmestrahlung</b> des Bodens. Mehr Treibhausgas verstärkt den Treibhauseffekt."),
    # Rechnen
    ("Wellenlänge des Kammertons a (440 Hz) in Luft (340 m/s)?",
     "\\u03bb = c/f = 340/440 \\u2248 <b>0.77 m</b>."),
    ("Frequenz eines roten Lasers mit \\u03bb = 632.8 nm (c = 3\\u00b710\\u2078 m/s)?",
     "f = c/\\u03bb = 3\\u00b710\\u2078 / 632.8\\u00b710\\u207b\\u2079 \\u2248 <b>4.7 \\u00b7 10\\u00b9\\u2074 Hz</b>."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p6-1-wellen', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::6.1 Wellen',
                   'TALS Physik \u00b7 Wellen: von der Schwingung zur Welle, Wellengleichung c = \u03bb\u00b7f, Transversal- und Longitudinalwellen, Schall in verschiedenen Medien, das elektromagnetische Spektrum, Lichterzeugung (Wärmestrahlung, atomare Emission, Laser) und die wellenlängenabhängige Absorption mit dem Treibhauseffekt.',
                   p61_cards)
    print(f"p6-1-wellen: {n} Karten erzeugt -> {out_path}")

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
