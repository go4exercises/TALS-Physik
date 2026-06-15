#!/usr/bin/env python3
"""Erzeugt eine Anki-.apkg-Datei für TALS Physik · p5-2 Wärme.

Basiert auf build_apkg_p5-1.py — gleiches Schema, gleiche CSS, andere Karten."""
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


# ─── Cards für p5-2 Wärme ───────────────────────────────────
p52_cards = [
    # Wärme & innere Energie
    ("Was ist <i>Wärme</i> physikalisch?",
     "Energie, die wegen eines <b>Temperaturunterschieds</b> übertragen wird. Sie fliesst stets von selbst vom <b>wärmeren zum kälteren</b> Körper."),
    ("Was ist die <i>innere Energie</i> eines Körpers?",
     "Die gesamte ungeordnete <b>Bewegungsenergie</b> seiner Teilchen."),
    ("Auf welche zwei Arten kann man die innere Energie ändern?",
     "Durch <b>Arbeit</b> (z.&nbsp;B. Reiben, Hämmern) oder durch Zufuhr/Abgabe von <b>Wärme</b>. Beide sind Energieübertragungen."),
    ("In welcher Einheit misst man Wärme?",
     "In <b>Joule</b> (J)."),
    ("Was bedeutet das Vorzeichen von Q?",
     "<b>Q &gt; 0</b>: der Körper nimmt Wärme auf (wird wärmer). <b>Q &lt; 0</b>: er gibt Wärme ab."),
    ("Was ist das <i>thermische Gleichgewicht</i>?",
     "Alle beteiligten Körper haben <b>dieselbe Temperatur</b>; es fliesst keine Wärme mehr (Q = 0)."),
    ("Warum ist „Kälte fliesst zu\u201c falsch?",
     "In der Physik gibt es nur die <b>Wärme</b>, die vom Warmen zum Kalten fliesst. Es gibt keine „Kälte\u201c, die zuflösse \u2014 ein Körper wird kalt, weil ihm Wärme entzogen wird."),
    # Spezifische Wärmekapazität
    ("Was gibt die <i>spezifische Wärmekapazität</i> c an?",
     "Die Wärme, die <b>1 kg</b> eines Stoffes pro <b>1 K</b> Temperaturänderung aufnimmt oder abgibt."),
    ("Grundgleichung der Wärmelehre (Erwärmen ohne Phasenübergang)?",
     "<b>Q = m \u00b7 c \u00b7 \u0394T</b> (m in kg, c in J/(kg\u00b7K), \u0394T in K)."),
    ("Einheit der spezifischen Wärmekapazität?",
     "<b>J/(kg\u00b7K)</b>."),
    ("Spezifische Wärmekapazität von Wasser?",
     "<b>c = 4182 J/(kg\u00b7K)</b> \u2014 aussergewöhnlich hoch."),
    ("Warum ist Wasser ein so guter Wärmespeicher?",
     "Wegen seiner <b>hohen spezifischen Wärmekapazität</b>: Es nimmt pro Kilogramm und Kelvin sehr viel Energie auf bzw. gibt sie ab."),
    # Wärmebilanz & Mischung
    ("Wie lautet die Wärmebilanz im abgeschlossenen System?",
     "<b>\u03a3 Q\u1d62 = 0</b> \u2014 der wärmere Körper gibt genau so viel Wärme ab, wie der kältere aufnimmt."),
    ("Formel für die Mischtemperatur zweier Stoffe (ohne Phasenübergang)?",
     "<b>\u03d1\u2098 = (m\u2081c\u2081\u03d1\u2081 + m\u2082c\u2082\u03d1\u2082) / (m\u2081c\u2081 + m\u2082c\u2082)</b>."),
    ("Was vereinfacht sich, wenn beide Stoffe gleich sind (z.&nbsp;B. zweimal Wasser)?",
     "Die spezifische Wärmekapazität <b>c kürzt sich heraus</b>; \u03d1\u2098 ist dann das massengewichtete Mittel der Temperaturen."),
    ("Wo liegt die Mischtemperatur?",
     "Stets <b>zwischen</b> den Ausgangstemperaturen, <b>näher</b> bei der Temperatur der grösseren Masse."),
    # Latente Wärme
    ("Was passiert bei einem Phasenübergang (Schmelzen, Verdampfen) mit der Temperatur?",
     "Sie bleibt <b>konstant</b>, obwohl Wärme zugeführt wird: Die Energie (latente Wärme) löst die Teilchen aus ihrem Verband, statt sie schneller zu machen."),
    ("Formel für die Schmelzwärme?",
     "<b>Q = m \u00b7 L_f</b> (L_f = spezifische Schmelzwärme, Einheit J/kg)."),
    ("Formel für die Verdampfungswärme?",
     "<b>Q = m \u00b7 L_v</b> (L_v = spezifische Verdampfungswärme, Einheit J/kg)."),
    ("Spezifische Schmelzwärme von Wasser?",
     "<b>L_f = 334 kJ/kg</b>."),
    ("Spezifische Verdampfungswärme von Wasser?",
     "<b>L_v = 2256 kJ/kg</b> \u2014 deutlich grösser als die Schmelzwärme."),
    ("Warum hat die Heizkurve (Eis\u2192Wasser\u2192Dampf) zwei waagrechte Plateaus?",
     "Beim Schmelzen (0\u00a0\u00b0C) und Verdampfen (100\u00a0\u00b0C) geht die zugeführte Energie als <b>latente Wärme</b> in den Phasenübergang \u2014 die Temperatur steigt erst weiter, wenn die Umwandlung abgeschlossen ist."),
    # Leistung, Wirkungsgrad, Heizwert
    ("Definition und Einheit der Leistung?",
     "<b>P = E / t</b>; Einheit <b>Watt</b> (1 W = 1 J/s)."),
    ("Wie ist der Wirkungsgrad \u03b7 definiert?",
     "<b>\u03b7 = E_nutz / E_zu</b>, das Verhältnis von Nutzenergie zu zugeführter Energie. Stets <b>\u03b7 \u2264 1</b>."),
    ("Wohin geht die Verlustenergie bei einer Energieumwandlung?",
     "Meist als <b>Wärme</b> an die Umgebung."),
    ("Was gibt der <i>Heizwert</i> eines Brennstoffs an?",
     "Wie viel Energie beim Verbrennen <b>pro Kilogramm</b> frei wird (z.&nbsp;B. Propan \u2248 13 kWh/kg)."),
    ("Umrechnung: 1 kWh in MJ?",
     "<b>1 kWh = 3.6 MJ</b>."),
    # Wärmetransport
    ("Welche drei Arten des Wärmetransports gibt es?",
     "<b>Wärmeleitung</b>, <b>Konvektion (Strömung)</b> und <b>Wärmestrahlung</b>."),
    ("Wie funktioniert die <i>Wärmeleitung</i>?",
     "Teilchen geben Bewegungsenergie an Nachbarteilchen weiter, <b>ohne selbst zu wandern</b> (v.&nbsp;a. in Festkörpern; Metalle leiten gut). Beispiel: heisser Pfannengriff."),
    ("Wie funktioniert die <i>Konvektion</i>?",
     "Erwärmtes Material (Flüssigkeit/Gas) <b>strömt selbst</b> und transportiert die Energie mit. Beispiel: Heizkörper, Wind."),
    ("Wie funktioniert die <i>Wärmestrahlung</i>?",
     "Übertragung durch elektromagnetische (<b>Infrarot-</b>)Strahlung, <b>ganz ohne Materie</b>. Beispiel: Sonne, Lagerfeuer."),
    # Wärmepumpe
    ("Was tut eine <i>Wärmepumpe</i>?",
     "Sie befördert Wärme vom <b>kalten zum warmen</b> Ort \u2014 entgegen der natürlichen Richtung \u2014 und braucht dafür Antriebsenergie (meist Strom)."),
    ("Wie ist die Leistungszahl (COP) definiert?",
     "<b>COP = Q_warm / E_elektrisch</b>; maximal <b>COP_max = T_warm / (T_warm \u2212 T_kalt)</b> (Temperaturen in Kelvin)."),
    ("Warum ist die Leistungszahl einer Wärmepumpe grösser als 1?",
     "Weil ein grosser Teil der abgegebenen Wärme <b>kostenlos aus der Umgebung</b> stammt; die Antriebsenergie verschiebt sie nur. Kleinere Temperaturdifferenz \u2192 grösserer COP."),
    # Treibhauseffekt
    ("Erkläre den <i>Treibhauseffekt</i> in einem Satz.",
     "Die Atmosphäre ist für sichtbares Sonnenlicht <b>durchlässig</b> (Boden wird erwärmt), für die abgestrahlte <b>Infrarot-Wärmestrahlung</b> aber nur teilweise \u2014 ein Teil wird zurückgehalten, sodass es an der Oberfläche wärmer bleibt."),
]

if __name__ == '__main__':
    out_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'themen',
                            'p5-2-waerme', 'ankideck.apkg')
    out_path = os.path.normpath(out_path)
    n = build_apkg(out_path,
                   'TALS Physik::Thermodynamik::p5-2 Wärme',
                   'TALS Physik \u00b7 Wärme: Wärme als übertragene Energie, spezifische Wärmekapazität und Q = m\u00b7c\u00b7\u0394T, Wärmebilanz und Mischtemperatur, latente Wärme bei Phasenübergängen, Leistung, Wirkungsgrad und Heizwert, die drei Arten des Wärmetransports, Wärmepumpe (COP) und der Treibhauseffekt.',
                   p52_cards)
    print(f"p5-2-waerme: {n} Karten erzeugt -> {out_path}")

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
