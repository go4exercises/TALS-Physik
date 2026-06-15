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
# ─── Cards für p6-2 Elektrizität ────────────────────────────
p62_cards = [
    # Ladung & Coulomb
    ("Was ist die Elementarladung e?",
     "Die kleinste frei vorkommende Ladung: <b>e = 1.602 · 10⁻¹⁹ C</b>. Alle Ladungen sind ganzzahlige Vielfache von e."),
    ("In welcher Einheit wird die elektrische Ladung gemessen?",
     "In <b>Coulomb (C)</b>. 1 C entspricht etwa 6.24 · 10¹⁸ Elementarladungen — eine sehr grosse Ladung."),
    ("Wie verhalten sich gleichnamige und ungleichnamige Ladungen?",
     "<b>Gleichnamige</b> Ladungen stossen sich ab, <b>ungleichnamige</b> ziehen sich an."),
    ("Wie lautet das Coulomb-Gesetz?",
     "<b>F = k · Q₁·Q₂ / r²</b> mit k = 8.99 · 10⁹ N·m²/C². Die Kraft nimmt mit dem <b>Quadrat</b> des Abstands ab."),
    # Strom & Spannung
    ("Wie ist die Stromstärke I definiert?",
     "Als bewegte Ladung pro Zeit: <b>I = Q / t</b>. Einheit: <b>Ampere (A) = C/s</b>."),
    ("Welche Ladung transportiert ein Strom I in der Zeit t?",
     "<b>Q = I · t</b>. Beispiel: 2 A während 60 s transportieren 120 C."),
    ("Was ist die elektrische Spannung U?",
     "Die pro Ladung verrichtete <b>Arbeit</b> — sie «treibt» die Elektronen an. Einheit: <b>Volt (V)</b>."),
    ("In welche Richtung fliessen die Elektronen im Stromkreis?",
     "Vom <b>Minus- zum Pluspol</b> (natürliche Stromrichtung). Die <i>technische</i> Stromrichtung zeigt umgekehrt (Plus → Minus)."),
    ("Unterschied zwischen Gleichstrom (DC) und Wechselstrom (AC)?",
     "Bei <b>DC</b> (Batterie) bleibt die Richtung gleich. Bei <b>AC</b> (Netz, 230 V) wechselt die Richtung periodisch."),
    # Ohmsches Gesetz
    ("Wie lautet das Ohmsche Gesetz?",
     "<b>U = R · I</b>. Umgestellt: R = U/I und I = U/R. Es gilt nur für Ohm'sche Widerstände."),
    ("Was bedeutet die Steigung im U-I-Diagramm?",
     "Sie ist gerade der <b>Widerstand R</b>: ein grösserer Widerstand macht die Gerade steiler."),
    ("Ist eine Glühlampe ein Ohm'scher Widerstand?",
     "<b>Nein.</b> Ihr Widerstand steigt mit der Temperatur — die Kennlinie ist keine Ursprungsgerade."),
    ("Welche Einheit hat der Widerstand?",
     "<b>Ohm (Ω) = V/A</b>."),
    # Leiterwiderstand
    ("Wie berechnet man den Widerstand eines Leiters?",
     "<b>R = ρ · l / A</b> — abhängig vom spezifischen Widerstand ρ (Material), der Länge l und dem Querschnitt A."),
    ("Wie ändert sich R mit Länge und Querschnitt?",
     "Mehr <b>Länge</b> vergrössert R, ein grösserer <b>Querschnitt</b> verkleinert R."),
    ("Was ist beim Widerstand eines Kabels zu beachten?",
     "Es zählt die <b>doppelte Länge</b> — Hin- und Rückleiter."),
    ("Welches Metall hat den kleinsten spezifischen Widerstand?",
     "<b>Silber</b> (ρ ≈ 0.016 Ω·mm²/m), dicht gefolgt von Kupfer (0.017). Deshalb nimmt man meist Kupfer."),
    # Schaltungen
    ("Reihenschaltung: was gilt für Strom, Spannung und Widerstand?",
     "<b>Strom überall gleich</b> (I = I₁ = I₂), <b>Spannung teilt sich auf</b> (U = U₁ + U₂), <b>R = R₁ + R₂</b>."),
    ("Parallelschaltung: was gilt für Strom, Spannung und Widerstand?",
     "<b>Spannung überall gleich</b> (U = U₁ = U₂), <b>Strom teilt sich auf</b> (I = I₁ + I₂), <b>1/R = 1/R₁ + 1/R₂</b>."),
    ("Ist der Gesamtwiderstand in Reihe grösser oder kleiner als die Einzelwiderstände?",
     "<b>Grösser</b> als jeder Einzelwiderstand. (Parallel: kleiner als der kleinste.)"),
    ("Formel für zwei parallele Widerstände?",
     "<b>R = (R₁ · R₂) / (R₁ + R₂)</b>."),
    ("Wie sind die Geräte im Haushalt geschaltet?",
     "<b>Parallel</b> — so liegt an jedem Gerät die volle Netzspannung (230 V)."),
    # Leistung & Energie
    ("Wie berechnet man die elektrische Leistung?",
     "<b>P = U · I</b>. Mit dem Ohmschen Gesetz auch P = R·I² = U²/R. Einheit: <b>Watt (W)</b>."),
    ("Wie berechnet man die elektrische Energie?",
     "<b>E = P · t = U · I · t</b>. Im Alltag in <b>Kilowattstunden (kWh)</b>."),
    ("Was ist eine Kilowattstunde?",
     "<b>1 kWh = 1000 W · 1 h = 3.6 · 10⁶ J</b>. Die Stromrechnung wird nach kWh abgerechnet."),
    # Rechnen
    ("Strom durch R = 220 Ω bei U = 12 V?",
     "I = U/R = 12/220 ≈ <b>0.055 A = 55 mA</b>."),
    ("Widerstand eines 50 m langen Kupferdrahts mit A = 1.5 mm²?",
     "R = ρ·l/A = 0.017 · 50 / 1.5 ≈ <b>0.57 Ω</b>."),
    ("Strom eines 2300-W-Heizlüfters am 230-V-Netz?",
     "I = P/U = 2300/230 = <b>10 A</b>."),
    # Gefahren
    ("Warum ist Strom über das Herz besonders gefährlich?",
     "Das Herz arbeitet mit elektrischen Impulsen; ein äusserer Strom kann <b>Herzkammerflimmern</b> auslösen. Schon ab ca. 50 mA gefährlich."),
    ("Wie schützt ein Fehlerstromschutzschalter (FI/RCD)?",
     "Er vergleicht hin- und zurückfliessenden Strom; bei einer Differenz (Fehlerstrom, z. B. durch den Körper) trennt er bei ca. <b>30 mA</b> in Millisekunden vom Netz."),
    ("Nenne vier Schutzmassnahmen gegen Stromunfälle.",
     "<b>Isolierung</b>, <b>Schutzleiter</b> (Erdung), <b>Sicherung</b> (begrenzt den Strom) und <b>FI/RCD</b> (Fehlerstromschutzschalter)."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p6-2-elektrizitaet', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::6.2 Elektrizität',
                   'TALS Physik \u00b7 Elektrizit\u00e4t: Ladung und Elementarladung, Coulomb-Gesetz, Stromst\u00e4rke I = Q/t und Spannung, Ohmsches Gesetz U = R\u00b7I, Widerstand eines Leiters R = \u03c1\u00b7l/A, Reihen- und Parallelschaltung, Leistung P = U\u00b7I und Energie E = U\u00b7I\u00b7t sowie die Gefahren des elektrischen Stroms.',
                   p62_cards)
    print(f"p6-2-elektrizitaet: {n} Karten erzeugt -> {out_path}")

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
