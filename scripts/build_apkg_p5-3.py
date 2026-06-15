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


# ─── Cards für p5-3 Wärmeausdehnung ─────────────────────────
p53_cards = [
    # Grundidee
    ("Warum dehnen sich Stoffe bei Erwärmung aus?",
     "Bei höherer Temperatur <b>schwingen die Atome heftiger</b> und stossen ihre Nachbarn im Mittel weiter weg \u2014 der mittlere Teilchenabstand wächst, der Körper wird in alle Richtungen grösser."),
    ("Warum haben Schienen, Brücken und Rohre Dehnungsfugen?",
     "Damit sich die Längenänderung bei Temperaturwechsel <b>spannungsfrei</b> ausdehnen kann. Sonst entstünden enorme Druckspannungen, die das Material verformen oder zerstören."),
    # Längenausdehnung
    ("Formel der Längenausdehnung fester Körper?",
     "<b>\u0394l = \u03b1 \u00b7 l\u2080 \u00b7 \u0394T</b> (\u03b1 = Längenausdehnungskoeffizient, l\u2080 = Anfangslänge, \u0394T = Temperaturänderung)."),
    ("Was ist der Längenausdehnungskoeffizient \u03b1?",
     "Eine <b>stoffabhängige</b> Konstante, die angibt, wie stark sich ein Material pro Kelvin relativ verlängert. Angabe meist in <b>10\u207b\u2076 K\u207b\u00b9</b>."),
    ("Wie berechnet man die relative Längenänderung?",
     "<b>\u0394l / l\u2080 = \u03b1 \u00b7 \u0394T</b> \u2014 einheitenlos und meist sehr klein."),
    ("Gilt die Längenausdehnungsformel auch beim Abkühlen?",
     "Ja. Bei Abkühlung ist <b>\u0394T &lt; 0</b>, also \u0394l &lt; 0 \u2014 der Körper wird kürzer."),
    ("Ungefährer \u03b1-Wert von Stahl/Eisen?",
     "<b>\u2248 12 \u00b7 10\u207b\u2076 K\u207b\u00b9</b>."),
    ("Ungefährer \u03b1-Wert von Aluminium?",
     "<b>23.8 \u00b7 10\u207b\u2076 K\u207b\u00b9</b> \u2014 fast doppelt so gross wie Stahl."),
    # Volumenausdehnung
    ("Formel der Volumenausdehnung?",
     "<b>\u0394V = \u03b3 \u00b7 V\u2080 \u00b7 \u0394T</b> (\u03b3 = Volumenausdehnungskoeffizient)."),
    ("Zusammenhang zwischen \u03b3 und \u03b1 für Festkörper?",
     "<b>\u03b3 \u2248 3\u03b1</b>, weil sich der Körper in alle drei Raumrichtungen ausdehnt."),
    ("Dehnen sich Flüssigkeiten stärker oder schwächer aus als Festkörper?",
     "<b>Deutlich stärker.</b> Ihr \u03b3 liegt typisch bei 10\u207b\u00b3 K\u207b\u00b9, das von Festkörpern (3\u03b1) bei rund 10\u207b\u2075 K\u207b\u00b9."),
    ("\u03b3-Wert von Ethanol?",
     "<b>1.10 \u00b7 10\u207b\u00b3 K\u207b\u00b9</b>."),
    # Dichte
    ("Wie ändert sich die Dichte bei Erwärmung und warum?",
     "Sie <b>sinkt</b>: Das Volumen wächst, die Masse bleibt gleich. Formel: <b>\u03c1 = \u03c1\u2080 / (1 + \u03b3 \u00b7 \u0394T)</b>."),
    ("Warum steigt warme Luft (oder warmes Wasser) auf?",
     "Weil erwärmtes Material eine <b>geringere Dichte</b> hat als die kältere Umgebung \u2014 das ist die Grundlage der Konvektion."),
    # Anomalie
    ("Was ist die Anomalie des Wassers?",
     "Wasser hat sein kleinstes Volumen \u2014 und damit die <b>grösste Dichte</b> \u2014 nicht am Gefrierpunkt, sondern bei <b>4 \u00b0C</b>. Unter 4 \u00b0C dehnt es sich wieder aus."),
    ("Warum frieren Seen von oben zu?",
     "Das dichteste Wasser (4 \u00b0C) sinkt nach unten; kälteres Wasser (0\u20134 \u00b0C) ist leichter und bleibt oben, wo es zu Eis gefriert. Am Grund bleibt flüssiges Wasser von \u2248 4 \u00b0C."),
    ("Welche Bedeutung hat die Wasseranomalie für Lebewesen?",
     "Am Seegrund herrschen 4 \u00b0C und flüssiges Wasser \u2014 <b>Fische und Wassertiere überleben den Winter</b>."),
    ("Warum platzen Wasserleitungen bei Frost?",
     "Wasser dehnt sich beim Gefrieren zu Eis aus (Folge der Anomalie). In einer geschlossenen Leitung erzeugt diese Volumenzunahme enorme Drücke, die das Rohr sprengen."),
    # Meeresspiegel
    ("Wodurch steigt der Meeresspiegel ausser durch schmelzendes Eis?",
     "Durch die <b>thermische Ausdehnung</b> des erwärmten Meerwassers. Modell: <b>\u0394h = \u03b3 \u00b7 h\u2080 \u00b7 \u0394T</b> für eine erwärmte Wassersäule der Tiefe h\u2080."),
    ("Warum ist die Meeresspiegel-Rechnung \u0394h = \u03b3\u00b7h\u2080\u00b7\u0394T nur eine Abschätzung?",
     "\u03b3 ist selbst temperaturabhängig, nicht alle Tiefen erwärmen sich gleich, und schmelzendes Eis ist nicht enthalten. Sie liefert nur die <b>Grössenordnung</b> des thermischen Anteils."),
    # Gasgesetz
    ("Wie lautet das ideale Gasgesetz?",
     "<b>p \u00b7 V / T = const</b>, also p\u2081V\u2081/T\u2081 = p\u2082V\u2082/T\u2082 (für gleichbleibende Gasmenge)."),
    ("Welche Einheit muss die Temperatur im Gasgesetz haben?",
     "Immer die <b>absolute Temperatur in Kelvin</b> (T/K = \u03d1/\u00b0C + 273.15)."),
    ("Welchen Druck setzt man im Gasgesetz ein?",
     "Den <b>absoluten Druck</b>. Zum Manometerdruck (relativ) muss der Luftdruck (\u2248 1 bar) addiert werden."),
    ("Gesetz von Boyle-Mariotte?",
     "Bei <b>konstanter Temperatur</b>: <b>p \u00b7 V = const</b> \u2014 verdoppelt man den Druck, halbiert sich das Volumen."),
    ("Gesetz von Amontons (Gay-Lussac, V konstant)?",
     "Bei <b>konstantem Volumen</b>: <b>p / T = const</b> \u2014 der Druck steigt proportional zur absoluten Temperatur."),
    ("Warum steigt der Druck in einem Gas bei Erwärmung (festes Volumen)?",
     "Die Teilchen bewegen sich schneller und stossen <b>häufiger und heftiger</b> gegen die Wände \u2014 der Druck nimmt zu (Amontons)."),
    ("Eine Druckgasflasche liegt in der Sonne. Welche Gefahr besteht?",
     "Bei konstantem Volumen steigt mit der Temperatur der <b>Druck</b> (Amontons). Er kann so hoch werden, dass das Sicherheitsventil anspricht \u2014 nie in der prallen Sonne lagern."),
    # Umrechnung / Merkpunkte
    ("Wie rechnet man Celsius in Kelvin um?",
     "<b>T/K = \u03d1/\u00b0C + 273.15</b>."),
    ("Sind \u0394T (in K) und \u0394\u03d1 (in \u00b0C) gleich gross?",
     "Ja. Eine Temperatur<b>differenz</b> ist in Kelvin und in Grad Celsius identisch \u2014 nur der Nullpunkt unterscheidet sich."),
    ("Warum darf man einen Flüssigkeitstank nie ganz randvoll füllen?",
     "Weil sich die Flüssigkeit bei Erwärmung ausdehnt (\u0394V = \u03b3\u00b7V\u2080\u00b7\u0394T). Ohne Ausdehnungsraum läuft sie über oder es entsteht gefährlicher Überdruck."),
    ("Welche drei Zustandsgrössen verknüpft das ideale Gasgesetz?",
     "<b>Druck p, Volumen V und (absolute) Temperatur T.</b>"),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p5-3-waermeausdehnung', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::Thermodynamik::p5-3 Wärmeausdehnung',
                   'TALS Physik \u00b7 Wärmeausdehnung: Längenausdehnung \u0394l = \u03b1\u00b7l\u2080\u00b7\u0394T, Volumenausdehnung \u0394V = \u03b3\u00b7V\u2080\u00b7\u0394T mit \u03b3 \u2248 3\u03b1, Dichteänderung, die Anomalie des Wassers (Dichtemaximum bei 4 \u00b0C), thermische Ausdehnung des Meeres und das ideale Gasgesetz p\u00b7V/T = const mit den Spezialfällen Boyle-Mariotte und Amontons.',
                   p53_cards)
    print(f"p5-3-waermeausdehnung: {n} Karten erzeugt -> {out_path}")

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
