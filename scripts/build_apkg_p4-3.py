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


# ─── Cards für p4-3 Energie ────────────────────────────────────────────────
p43_cards = [
    # Arbeit
    ("Definition der <i>Arbeit</i> und ihre Einheit",
     "Arbeit wird verrichtet, wenn eine <b>Kraft längs eines Weges</b> wirkt.<br><b>W = F · s · cosα</b><br>Einheit: <b>J</b> (Joule) = N·m = kg·m²/s². α ist der Winkel zwischen Kraft und Weg."),
    ("Was bedeutet das <i>cosα</i> in W = F·s·cosα?",
     "Nur die <b>Kraftkomponente in Wegrichtung</b> verrichtet Arbeit. Steht die Kraft senkrecht zum Weg (α = 90°, cos = 0), wird <b>keine</b> Arbeit verrichtet — z.B. beim Tragen einer Last waagrecht."),
    ("Formel für die <i>Hubarbeit</i>",
     "<b>W_Hub = m · g · h</b><br>Arbeit, um einen Körper der Masse m um die Höhe h anzuheben (Kraft = Gewichtskraft, Weg = Höhe, α = 0)."),
    ("Wann ist die verrichtete Arbeit negativ?",
     "Wenn die Kraft dem Weg <b>entgegengerichtet</b> ist (α > 90°, cosα < 0) — z.B. die <b>Reibungskraft</b> entzieht dem Körper Energie."),
    # Energieformen
    ("Definition <i>Energie</i>",
     "Energie ist die <b>Fähigkeit, Arbeit zu verrichten</b>. Sie wird durch Arbeit übertragen und in J (Joule) gemessen."),
    ("Formel für die <i>potentielle Energie</i> (Lageenergie)",
     "<b>E_pot = m · g · h</b><br>Energie aufgrund der Höhe h über einem Bezugsniveau. Entspricht der Hubarbeit."),
    ("Formel für die <i>kinetische Energie</i> (Bewegungsenergie)",
     "<b>E_kin = ½ · m · v²</b><br>Achtung: geht <b>quadratisch</b> mit v — doppelte Geschwindigkeit = vierfache Bewegungsenergie."),
    ("Formel für die <i>Spannenergie</i> (elastische Energie)",
     "<b>E_spann = ½ · D · s²</b><br>In einer gespannten Feder gespeicherte Energie. D = Federkonstante (N/m), s = Auslenkung."),
    ("Warum vervierfacht sich die Bewegungsenergie bei doppelter Geschwindigkeit?",
     "Weil E_kin = ½mv² <b>quadratisch</b> von v abhängt: (2v)² = 4v². Deshalb wächst auch der Bremsweg quadratisch mit der Geschwindigkeit."),
    # Energieerhaltung
    ("Energieerhaltungssatz der Mechanik",
     "Ohne Reibung bleibt die <b>Summe der mechanischen Energien konstant</b>:<br><b>E_kin + E_pot + E_spann = konstant</b><br>Energie wechselt nur die Form, sie verschwindet nicht."),
    ("Endgeschwindigkeit beim freien Fall aus Höhe h (Energieansatz)",
     "Aus m·g·h = ½·m·v² (Masse fällt heraus):<br><b>v = √(2·g·h)</b><br>Massenunabhängig — gilt auch für reibungsfreies Hinabgleiten."),
    ("Wie wendet man den Energieerhaltungssatz auf eine Achterbahn an?",
     "Höchster Punkt: viel E_pot, wenig E_kin. Tiefster Punkt: E_pot in E_kin umgewandelt → maximale Geschwindigkeit. <b>E_pot,oben = E_kin,unten</b> (reibungsfrei)."),
    ("Wohin geht die Energie bei Reibung?",
     "Sie wird in <b>Wärme</b> (thermische Energie) umgewandelt. Die mechanische Energie nimmt ab, die <b>Gesamtenergie</b> bleibt aber erhalten."),
    ("Energieumwandlung beim Fadenpendel",
     "Im Umkehrpunkt: maximale <b>E_pot</b>, v = 0. Im tiefsten Punkt: maximale <b>E_kin</b>, h = 0. Dazwischen ständiger Wechsel — Summe konstant (ohne Reibung)."),
    # Leistung
    ("Definition der <i>Leistung</i> und ihre Einheit",
     "Leistung = <b>Arbeit pro Zeit</b>:<br><b>P = W / t</b><br>Einheit: <b>W</b> (Watt) = J/s. Sie misst, wie <i>schnell</i> Energie umgesetzt wird."),
    ("Leistung über Kraft und Geschwindigkeit",
     "<b>P = F · v</b><br>Folgt aus P = W/t = F·s/t = F·v. Praktisch z.B. für Motoren bei konstanter Geschwindigkeit."),
    ("Umrechnung Pferdestärke in Watt",
     "<b>1 PS ≈ 735 W</b> ≈ 0.735 kW. Umgekehrt: 1 kW ≈ 1.36 PS."),
    # Wirkungsgrad
    ("Definition des <i>Wirkungsgrades</i>",
     "<b>η = E_nutz / E_zu</b> (auch P_nutz / P_zu).<br>Verhältnis von nutzbarer zu zugeführter Energie, dimensionslos (oft in %). Immer η < 1, da stets Verluste (meist Wärme) auftreten."),
    ("Kann der Wirkungsgrad grösser als 100 % sein?",
     "<b>Nein.</b> Es gibt immer Verluste (Reibung, Wärme). η = 1 (100 %) wäre der verlustfreie Idealfall, der real nie erreicht wird."),
    ("Beispiel-Wirkungsgrade: Glühlampe vs. LED",
     "Glühlampe ≈ <b>5–10 %</b> (Rest wird Wärme), LED ≈ <b>40–90 %</b>. Deshalb sind LEDs viel energieeffizienter."),
    ("Nutzenergie aus zugeführter Energie berechnen",
     "<b>E_nutz = η · E_zu</b>. Beispiel: η = 0.85, E_zu = 2000 J → E_nutz = 1700 J; 300 J gehen als Verlust verloren."),
    # Anwendung / Verständnis
    ("Funktionsweise eines Pumpspeicherkraftwerks (energetisch)",
     "Überschussstrom pumpt Wasser nach oben → speichert <b>E_pot</b>. Bei Bedarf fliesst es zurück, treibt Turbinen → <b>E_kin</b> → elektrische Energie. Energiespeicher mit Wirkungsgrad ≈ 75–80 %."),
    ("Warum ist der Bremsweg bei Tempo 100 viermal so lang wie bei Tempo 50?",
     "Die zu „vernichtende“ Bewegungsenergie E_kin = ½mv² ist <b>viermal</b> grösser (v doppelt → v² vierfach). Bei gleicher Bremskraft wird der Weg viermal so lang."),
    ("Vorgehen bei Energie-Aufgaben (Rezept)",
     "1. <b>Bezugsniveau</b> (h = 0) festlegen. 2. Energieformen <b>vorher</b> und <b>nachher</b> aufschreiben. 3. <b>Energieerhaltung</b> ansetzen (ohne Reibung) bzw. Verluste/Reibungsarbeit berücksichtigen. 4. Nach der gesuchten Grösse auflösen."),
    ("Zusammenhang Arbeit und Energieänderung",
     "Verrichtete Arbeit <b>ändert die Energie</b> des Körpers: Hubarbeit erhöht E_pot, Beschleunigungsarbeit erhöht E_kin, Reibungsarbeit verringert die mechanische Energie."),
    ("Einheit Joule in Basiseinheiten und als Wattsekunde",
     "<b>1 J = 1 N·m = 1 kg·m²/s² = 1 W·s</b>. Daraus folgt auch 1 kWh = 3.6 · 10⁶ J = 3.6 MJ."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p4-3-energie', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::Mechanik::p4-3 Energie',
                   'TALS Physik · Energie: Arbeit (W=F·s·cosα), Hubarbeit, Lage-, Bewegungs- und Spannenergie, Energieerhaltungssatz, Leistung (P=W/t=F·v) und Wirkungsgrad.',
                   p43_cards)
    print(f"p4-3-energie: {n} Karten erzeugt -> {out_path}")

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
