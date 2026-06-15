#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Physik · p4-5 Hydrostatik.

Basiert auf build_apkg_p4-1.py — gleiche Schema, gleiche CSS, andere Karten."""
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


# ─── Cards für p4-5 Hydrostatik ────────────────────────────────────────────
p45_cards = [
    # Grundbegriffe
    ("Was ist <i>Druck</i> und welche Einheit hat er?",
     "Druck ist <b>Kraft pro Fläche</b>:<br>p = <b>F / A</b><br>Einheit: <b>Pa</b> (Pascal) = N/m². Praxis: 1 bar = 10⁵ Pa = 1000 hPa."),
    ("Ist der Druck ein Skalar oder ein Vektor?",
     "<b>Skalar</b>. In einer ruhenden Flüssigkeit wirkt er an einem Punkt nach <b>allen Seiten gleich</b> — er hat also keinen Richtungspfeil."),
    ("Was ist <i>Dichte</i> und welche Einheit hat sie?",
     "Masse pro Volumen:<br>ρ = <b>m / V</b><br>Einheit: <b>kg/m³</b>. Wasser bei 4 °C: 1000 kg/m³ — die SI-Bezugsgrösse."),
    ("Dichte von Wasser, Eis, Quecksilber, Aluminium, Eisen (kg/m³)?",
     "<b>Wasser</b>: 1000<br><b>Eis</b>: 917<br><b>Meerwasser</b>: 1025<br><b>Quecksilber</b>: 13 600<br><b>Aluminium</b>: 2700<br><b>Eisen</b>: 7870"),
    ("Wie hoch ist der Luftdruck auf Meereshöhe?",
     "<b>p₀ ≈ 1013 hPa ≈ 1.013 bar ≈ 101 325 Pa</b><br>(Standardwert; nimmt mit der Höhe ab — pro 100 m Höhe etwa 12 hPa.)"),
    # Schweredruck
    ("Formel für den Schweredruck in einer Flüssigkeit",
     "<b>p_S = ρ · g · h</b><br>Zusätzlich zum Luftdruck. Hängt nicht von der Form des Gefässes ab."),
    ("Gesamtdruck in einer Flüssigkeit",
     "Luftdruck + Schweredruck:<br><b>p = p₀ + ρ · g · h</b><br>Für Anwendungen, wo der Luftdruck mitberücksichtigt wird (z.B. Druck auf Trommelfell beim Tauchen)."),
    ("Faustregel für den Schweredruck in Wasser",
     "Pro <b>10 m Wassertiefe</b> kommt etwa <b>1 bar</b> Druck dazu.<br>(genau: 0.981 bar — denn ρ·g·10 = 1000·9.81·10 = 98 100 Pa.)"),
    ("Was ist das <i>hydrostatische Paradoxon</i>?",
     "Der Bodendruck einer Flüssigkeit hängt <b>nur von der Füllhöhe</b> ab, <b>nicht von der Gefässform</b>. Schmale Röhre und weiter Becher bei gleicher Höhe → gleicher Bodendruck — auch wenn die Wassermengen sehr verschieden sind."),
    ("Unterschied Bodendruck vs. Bodenkraft beim Paradoxon",
     "<b>Druck</b> p = ρ·g·h hängt nur von Höhe ab — gleich in allen Gefässen.<br><b>Kraft</b> F = p·A hängt von der Bodenfläche ab — verschieden bei verschiedenen Gefässformen."),
    # Pascal-Prinzip / Hydraulik
    ("Prinzip von Pascal",
     "In einer geschlossenen Flüssigkeit pflanzt sich ein Druck <b>nach allen Seiten gleichmässig</b> fort. Ein zusätzlicher Druck auf eine Stelle wirkt unverändert an jeder anderen Stelle."),
    ("Hauptgleichung der hydraulischen Presse",
     "<b>F₁/A₁ = F₂/A₂</b> (Druck überall gleich) <br>→ <b>F₂ = F₁ · A₂/A₁</b><br>Kleine Kraft × grosses Flächenverhältnis = grosse Kraft."),
    ("Hubverhältnis bei der hydraulischen Presse (Volumenerhaltung)",
     "<b>A₁ · s₁ = A₂ · s₂</b><br>→ <b>s₂ = s₁ · A₁/A₂</b><br>Was an Kraft gewonnen wird, wird an Weg bezahlt — die Arbeit W = F·s ist auf beiden Seiten gleich (Energieerhaltung)."),
    ("Beispiel-Anwendungen des Pascal-Prinzips",
     "<b>Hydraulische Hebebühne, Wagenheber, Autobremse, Bagger-Hydraulik, Gabelstapler.</b><br>Überall, wo eine kleine Kraft auf einen kleinen Kolben in eine grosse Kraft auf einen grossen Kolben umgewandelt wird."),
    # Auftrieb
    ("Archimedisches Prinzip (in Worten)",
     "Ein in eine Flüssigkeit eingetauchter Körper erfährt eine <b>nach oben gerichtete Auftriebskraft</b>, die gleich dem <b>Gewicht der verdrängten Flüssigkeit</b> ist."),
    ("Formel für die Auftriebskraft",
     "<b>F_A = ρ_Fl · V_eingetaucht · g</b><br>ρ_Fl: Dichte der Flüssigkeit (kg/m³)<br>V_eingetaucht: Volumen des eingetauchten Körperteils (m³)"),
    ("Wovon hängt die Auftriebskraft <i>nicht</i> ab?",
     "<b>Nicht</b> vom Material des Körpers, nicht von der Form und nicht von der Eintauchtiefe (sofern der Körper voll eingetaucht ist). Nur Flüssigkeit-Dichte und eingetauchtes Volumen zählen."),
    # Schwimmen-Schweben-Sinken
    ("Wann schwimmt, schwebt oder sinkt ein Körper?",
     "<b>Schwimmen</b>: ρ_K &lt; ρ_Fl<br><b>Schweben</b>: ρ_K = ρ_Fl<br><b>Sinken</b>: ρ_K &gt; ρ_Fl<br>Es zählt allein der Dichtevergleich Körper ↔ Flüssigkeit."),
    ("Wie tief taucht ein schwimmender Körper ein?",
     "Bei einem schwimmenden Körper stellt sich das Gleichgewicht F_A = F_G ein. Daraus folgt:<br><b>V_eingetaucht / V_Körper = ρ_K / ρ_Fl</b>"),
    ("Warum ragt nur etwa 10 % eines Eisbergs aus dem Meer?",
     "Eis: ρ = 917 kg/m³, Meerwasser: ρ = 1025 kg/m³.<br>V_unter/V = 917/1025 ≈ <b>89.5 %</b><br>→ über Wasser: <b>10.5 %</b> — etwa 1/10. Daher der Spruch: „Das ist nur die Spitze des Eisbergs.“"),
    ("Warum schwimmt ein Stahlschiff, obwohl Stahl viel dichter ist als Wasser?",
     "Weil das Schiff als <b>Ganzes</b> (inkl. der vielen luftgefüllten Hohlräume) eine mittlere Dichte hat, die <b>kleiner als Wasser</b> ist. Das eingetauchte Volumen verdrängt mehr Wasser, als das Schiff wiegt."),
    # Kommunizierende Röhren / U-Rohr
    ("Was beobachtet man bei kommunizierenden Röhren (gleiche Flüssigkeit)?",
     "Der Flüssigkeitsspiegel stellt sich in allen verbundenen Gefässen <b>gleich hoch</b> ein — unabhängig von der Form. Anwendung: <b>Schlauchwaage</b> auf Baustellen."),
    ("Druckgleichheit am Grenzpunkt in einem U-Rohr mit zwei Flüssigkeiten",
     "Auf der Höhe der Flüssigkeitsgrenze gilt:<br><b>ρ₁ · h₁ = ρ₂ · h₂</b><br>Die schwerere Flüssigkeit drückt weiter nach unten, die leichtere steht höher."),
    # Konzepte
    ("Was misst ein <i>Quecksilberbarometer</i>?",
     "Den <b>Luftdruck</b>. Eine Quecksilbersäule der Höhe ca. <b>76 cm</b> (genau: 760 mm) entspricht dem Normaldruck von 1013 hPa. Daher die alte Einheit „Torr“ mit 1 Torr = 1 mm Hg."),
    ("Wie funktioniert ein U-Boot beim Tauchen und Auftauchen?",
     "<b>Tauchen</b>: Wasser wird in Tarier-Tanks gepumpt → Gesamtmasse steigt → F_G &gt; F_A → sinkt.<br><b>Auftauchen</b>: Druckluft drückt das Wasser aus den Tanks → Masse sinkt → F_A &gt; F_G → steigt.<br>Im Schweben: F_A = F_G."),
    ("Warum „verliert“ ein Körper im Wasser an Gewicht?",
     "Auf einer Federwaage zeigt der Körper nicht sein wahres Gewicht F_G, sondern das <b>scheinbare Gewicht</b> F_G − F_A. Die Auftriebskraft hebt einen Teil des Gewichts kompensiert auf."),
    ("Wie kann man die Dichte einer Flüssigkeit mit einem Aräometer messen?",
     "Ein Aräometer ist ein kalibrierter Schwimmkörper. Je tiefer es einsinkt, desto kleiner ist die Flüssigkeits­dichte. Aus F_A = F_G folgt: <b>ρ_Fl = m / V_eingetaucht</b>. Die Skala zeigt direkt ρ an."),
    ("Wie haben die alten Schweizer Baumeister Höhenunterschiede gemessen?",
     "Mit einem <b>Schlauch voll Wasser</b> — den Enden hochgehalten zeigen den Flüssigkeitsspiegel auf gleicher Höhe an (kommunizierende Röhren). Die einfachste und präziseste Wasserwaage über grosse Distanzen."),
    # Numerische Wissensanker
    ("Schweredruck in 1 m Wassertiefe",
     "p_S = 1000 · 9.81 · 1 ≈ <b>9810 Pa ≈ 98 hPa ≈ 0.1 bar</b><br>(Daher die Faustregel: pro Meter ~0.1 bar, pro 10 m ~1 bar.)"),
    ("Druck am Boden eines 5-m-Schwimmbeckens (Schweredruck)",
     "p_S = 1000 · 9.81 · 5 ≈ <b>49 050 Pa ≈ 0.49 bar</b><br>Mit Luftdruck dazu: Gesamtdruck ca. <b>1.5 bar</b> — etwa 50 % mehr als an der Oberfläche."),
    ("Auftriebskraft auf 1 Liter Wasser",
     "Volumen 1 L = 10⁻³ m³ → F_A = 1000 · 10⁻³ · 9.81 ≈ <b>9.81 N</b><br>(Gewicht von 1 kg Wasser — Auftrieb = verdrängtes Wassergewicht.)"),
    ("Welche Wassersäule entspricht einem Atmosphären-Druck?",
     "p = ρ·g·h → h = p/(ρ·g) = 101 325 / (1000·9.81) ≈ <b>10.3 m</b> Wasser.<br>Das ist auch die maximale „Saughöhe“ einer einfachen Pumpe — über 10 m saugt sie kein Wasser hoch."),
    ("Was leistet Pascal-Prinzip in einer 1:50-Hydraulik?",
     "Eine Eingangskraft von 50 N erzeugt eine Ausgangskraft von <b>2500 N</b> (≈ 255 kg Hub-Last). Der Eingangs-Kolben muss aber <b>50-mal so weit</b> bewegt werden wie der Ausgangs-Kolben (Volumenerhaltung)."),
]


if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen', 'p4-5-hydrostatik')
    out_dir = os.path.normpath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'ankideck.apkg')

    n = build_apkg(out_path,
                   'TALS Physik::Mechanik::p4-5 Hydrostatik',
                   'TALS Physik · Hydrostatik: Druck, Schweredruck, Pascal-Prinzip, Auftrieb, Schwimmen/Schweben/Sinken, kommunizierende Röhren.',
                   p45_cards)
    print(f"p4-5-hydrostatik: {n} Karten erzeugt → {out_path}")

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
