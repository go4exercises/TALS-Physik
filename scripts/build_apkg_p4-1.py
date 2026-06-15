#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Physik · p4-1 Kinematik."""
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

# Card-CSS: Bernstein-Akzent statt Mathe-Blau für i
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


# ─── Cards für p4-1 Kinematik ────────────────────────────────────────────
p41_cards = [
    # Grundbegriffe
    ("Was beschreibt die <i>Kinematik</i>?",
     "Sie beschreibt <b>Bewegungen</b> (Lage, Geschwindigkeit, Beschleunigung) — aber <b>ohne</b> nach deren <b>Ursachen</b> (Kräften) zu fragen. Die Ursachen sind Sache der Dynamik."),
    ("Was bedeutet <i>Massenpunkt</i>?",
     "Idealisierung eines ausgedehnten Körpers als <b>Punkt</b> mit der gesamten Masse — typischerweise am <b>Schwerpunkt</b>. Vereinfacht die Beschreibung der Translationsbewegung."),
    ("Definition der Geschwindigkeit",
     "Zeitliche Änderung des Weges:<br>v = <b>ds/dt</b> = ṡ<br>Einheit: <b>m/s</b>"),
    ("Definition der Beschleunigung",
     "Zeitliche Änderung der Geschwindigkeit:<br>a = <b>dv/dt</b> = v̇ = s̈<br>Einheit: <b>m/s²</b>"),
    ("Welche Grössen der Kinematik sind <i>Skalare</i>, welche sind <i>Vektoren</i>?",
     "<b>Skalare</b>: Zeit t, Weg s (nur Länge)<br><b>Vektoren</b>: Ort r⃗, Geschwindigkeit v⃗, Beschleunigung a⃗ (mit Richtung)"),
    # Einheiten
    ("Umrechnung 1 m/s → km/h",
     "<b>1 m/s = 3.6 km/h</b><br>(weil 1 m/s · 3600 s/h / 1000 m/km = 3.6)"),
    ("Umrechnung 1 km/h → m/s",
     "<b>1 km/h ≈ 0.278 m/s</b><br>(weil 1/3.6 ≈ 0.278) — also: km/h-Wert durch 3.6 teilen"),
    ("Wert der Erdbeschleunigung g",
     "<b>g = 9.81 m/s²</b><br>(auf Meereshöhe, mittlere Breiten)"),
    # Gleichförmige Bewegung
    ("Weg-Zeit-Gesetz der geradlinig gleichförmigen Bewegung",
     "<b>s(t) = s₀ + v · t</b><br>mit konstanter Geschwindigkeit v und Startweg s₀"),
    ("Wie sehen die s-t-, v-t- und a-t-Diagramme einer gleichförmigen Bewegung aus?",
     "<b>s-t</b>: Gerade mit Steigung v<br><b>v-t</b>: waagrechte Linie auf Höhe v<br><b>a-t</b>: Null-Linie (a = 0)"),
    # Gleichmässig beschleunigt
    ("Drei Bewegungsgleichungen der gleichmässig beschleunigten Bewegung",
     "<b>a(t) = a</b> (konstant)<br><b>v(t) = v₀ + a · t</b><br><b>s(t) = s₀ + v₀ · t + ½ · a · t²</b>"),
    ("Zeitfreie Gleichung der gleichmässig beschleunigten Bewegung",
     "<b>v² = v₀² + 2 · a · (s − s₀)</b><br>Nützlich, wenn t weder gegeben noch gesucht ist."),
    ("Wie sehen die s-t-, v-t- und a-t-Diagramme einer gleichmässig beschleunigten Bewegung aus?",
     "<b>s-t</b>: Parabel (Krümmung ∝ a)<br><b>v-t</b>: Gerade mit Steigung a<br><b>a-t</b>: waagrechte Linie auf Höhe a"),
    ("Was bedeutet die <i>Fläche unter dem v-t-Graphen</i>?",
     "Der zurückgelegte <b>Weg Δs</b>. Bei konstantem v: Rechteck-Fläche v · t. Bei linearem v: Dreiecks- oder Trapez-Fläche."),
    ("Was bedeutet die <i>Steigung im v-t-Graphen</i>?",
     "Die <b>Beschleunigung a</b>. Bei einer geraden Linie: konstantes a. Bei einer Kurve: momentanes a als Tangentensteigung."),
    # Freier Fall
    ("Bewegungsgleichungen des freien Falls aus der Ruhe",
     "Mit a = g, v₀ = 0, s₀ = 0:<br><b>v(t) = g · t</b><br><b>s(t) = ½ · g · t²</b>"),
    ("Aufprallgeschwindigkeit nach einer Fallhöhe h (zeitfrei)",
     "Aus v² = 2 · g · h folgt:<br><b>v = √(2 · g · h)</b>"),
    ("Aus welcher Höhe muss ein Körper fallen, um beim Aufprall 50 km/h zu erreichen?",
     "v = 50 km/h ≈ 13.89 m/s. Aus h = v² / (2g):<br><b>h ≈ 9.8 m</b> — also etwa 3. Stock. Das ist die klassische Verkehrssicherheits-Vergleichshöhe."),
    # Schiefer Wurf
    ("Bewegungsgleichungen des schiefen Wurfs (Ursprung am Abwurfort, y nach oben)",
     "<b>x(t) = v₀ · cos(α) · t</b><br><b>y(t) = v₀ · sin(α) · t − ½ · g · t²</b>"),
    ("Formel für die <i>Wurfweite</i> beim schiefen Wurf (gleiche Abwurf- und Auftreffhöhe)",
     "<b>x_W = v₀² · sin(2α) / g</b><br>Maximum bei α = <b>45°</b>"),
    ("Formel für die <i>maximale Wurfhöhe</i> beim schiefen Wurf",
     "<b>h_max = v₀² · sin²(α) / (2g)</b>"),
    ("Formel für die <i>Flugzeit</i> beim schiefen Wurf (gleiche Abwurf- und Auftreffhöhe)",
     "<b>T_F = 2 · v₀ · sin(α) / g</b>"),
    ("Warum ist 45° der optimale Abwurfwinkel für die <i>Wurfweite</i> (bei gleicher Abwurf- und Auftreffhöhe)?",
     "Wegen sin(2α). Das ist maximal, wenn 2α = 90°, also <b>α = 45°</b>. Bei höherem oder tieferem Winkel: kürzere Weite."),
    # Kreisbewegung
    ("Beziehung zwischen <i>Periode T</i> und <i>Frequenz f</i>",
     "<b>f = 1 / T</b><br>Periode in Sekunden, Frequenz in Hz (= 1/s)"),
    ("Definition der Winkelgeschwindigkeit ω",
     "<b>ω = 2π / T = 2π · f</b><br>Einheit: rad/s. Gibt an, wie viel Winkel pro Sekunde überstrichen wird."),
    ("Beziehung Bahngeschwindigkeit v und Winkelgeschwindigkeit ω",
     "<b>v = ω · r</b><br>Je grösser der Radius, desto grösser die Bahngeschwindigkeit bei gleichem ω."),
    ("Formel für die Zentripetalbeschleunigung",
     "<b>a_z = v² / r = ω² · r</b><br>Richtung: <b>zum Kreismittelpunkt</b>, immer senkrecht zu v⃗."),
    ("Warum braucht es bei der gleichförmigen Kreisbewegung eine Beschleunigung, obwohl |v⃗| konstant ist?",
     "Weil sich die <b>Richtung</b> von v⃗ ständig ändert. a⃗ steht senkrecht zu v⃗ und zeigt zum Kreismittelpunkt — sie ändert die <b>Richtung</b>, nicht den <b>Betrag</b> der Geschwindigkeit."),
    # Relativbewegung
    ("Galilei-Addition für Geschwindigkeiten",
     "Körper K bewegt sich in Bezugssystem B, das sich seinerseits in System E bewegt:<br><b>v⃗_K/E = v⃗_K/B + v⃗_B/E</b>"),
    ("Wie addiert man zwei senkrecht zueinander stehende Geschwindigkeiten?",
     "Mit dem Satz des Pythagoras:<br><b>|v⃗_res| = √(v₁² + v₂²)</b><br>Beispiel: Schwimmer 1.2 m/s senkrecht zur Strömung 0.9 m/s → resultierend 1.5 m/s."),
    ("Schwimmer in einem Fluss: Was bestimmt die Überquerungszeit?",
     "Nur die <b>Geschwindigkeitskomponente senkrecht</b> zur Strömung — meist v_Schwimmer selbst. Die Strömung sorgt nur für die Abdrift, nicht für eine längere/kürzere Überquerung."),
    # Bremsen / Anhalten
    ("Bremsweg aus v₀ bei konstanter Bremsverzögerung |a|",
     "Aus v² = v₀² − 2|a|s mit v=0:<br><b>s_Brems = v₀² / (2|a|)</b><br>→ <i>proportional zu v₀²</i>: Geschwindigkeit verdoppeln = Bremsweg vervierfachen."),
    ("Was ist der Unterschied zwischen <i>Reaktionsweg</i> und <i>Bremsweg</i>?",
     "<b>Reaktionsweg</b>: Strecke während der Reaktionszeit, bei konstantem v (kein Bremsen) — linear in v.<br><b>Bremsweg</b>: ab dem Bremsbeginn bis zum Stillstand — quadratisch in v.<br><b>Anhalteweg</b> = Reaktionsweg + Bremsweg."),
    # Konzepte
    ("Was bedeutet eine negative Beschleunigung?",
     "Eine Beschleunigung entgegen der gewählten positiven Richtung. Bei einer Bewegung in positive Richtung heisst das <b>Verzögerung</b> (Verlangsamen). Bei einer Bewegung in negative Richtung beschleunigt sie den Körper."),
    ("Wie unterscheidet sich <i>Durchschnitts-</i> von <i>Momentangeschwindigkeit</i>?",
     "<b>Durchschnitt</b>: v̄ = Δs / Δt über ein ganzes Intervall.<br><b>Moment</b>: v(t) = ds/dt zu einem Zeitpunkt — Tangentensteigung im s-t-Diagramm.<br>Bei konstantem v sind beide gleich."),
]


if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen', 'p4-1-kinematik')
    out_dir = os.path.normpath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'ankideck.apkg')

    n = build_apkg(out_path,
                   'TALS Physik::Mechanik::p4-1 Kinematik',
                   'TALS Physik · Kinematik des Schwerpunkts: Geschwindigkeit, Beschleunigung, Bewegungsarten, Wurf, Kreis, Relativbewegung.',
                   p41_cards)
    print(f"p4-1-kinematik: {n} Karten erzeugt → {out_path}")

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
