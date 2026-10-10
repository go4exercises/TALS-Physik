#!/usr/bin/env python3
"""
Pre-Flight-Check für die Themenseiten von «Physik begreifbar» (themen/).

Zwei Stufen:
1. Schnelle, abhängigkeitsfreie Eigen-Checks (Tag-Bilanz, ß, Dezimalkomma in Math,
   HTML innerhalb eines LaTeX-Ausdrucks, doppelte IDs, Skelett, Phantom-Klassen,
   physiklib-Abhängigkeit, Ressourcen-Marker inkl. Slot-Limits).
2. Orchestrierung der vorhandenen, autoritativen Repo-Skripte in scripts/:
   - verify_mathjax.js     (echte MathJax-Render-Prüfung; braucht node_modules/mathjax-full)
   - verify_js_runtime.js  (JS-Laufzeit in jsdom; braucht node_modules/jsdom)
   - verify_einheitentrainer.js (Selbsttest des Einheitentrainers; braucht jsdom)
   - check_identifier_collisions.py (falls vorhanden; ohne npm)
   - check_clips (Clip-Ablage gegen clips/clips.json und nav.js)
   - check_sim_wz (simulationen/ und werkzeuge/: Uebersicht, Verweise, Ruecklink-Anker)
   - check_todo_schwester (offene Eintraege in TODO-schwesterprojekt.md des
     Schwesterrepos; nur gelesen, WARN)
   Fehlt ein npm-Modul, wird der Tiefen-Check sauber als WARN übersprungen.

MUSS vom Repo-Wurzelverzeichnis aufgerufen werden (wegen scripts/ und node_modules/).

Aufruf:  python3 .claude/skills/preflight/preflight.py themen/*.html

Exit 0  -> alle Checks bestanden.   Exit 1 -> mindestens ein [FEHLER]. Nicht committen.
"""
import os
import re
import sys
import subprocess
from pathlib import Path

# Klassennamen, die im Physik-CSS NICHT existieren ('rlp' ist legitim und NICHT hier).
PHANTOM_CLASSES = [
    "inhalt", "brot", "seiten-kopf", "dl-box", "ressourcen-grid",
    "ress", "ress-titel", "ress-beschr", "ress-quelle",
]
UNIQUE_MARKERS = [
    r'<h2 id="ressourcen"',
    r'ressourcen-subtitel">🎬',
    r'ressourcen-subtitel">🧪',
    r'ressourcen-subtitel">📝',
    r'<aside class="toc-wrap"',
    r'<footer class="site-footer"',
]
LIB = "physiklib.js"


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0

    def err(self, who, msg):
        print(f"[FEHLER] {who}: {msg}")
        self.errors += 1

    def warn(self, who, msg):
        print(f"[WARN]   {who}: {msg}")
        self.warns += 1


# ---------- Stufe 1: schnelle Eigen-Checks ----------

def _strip_scripts(text):
    return re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)


def check_tag_balance(text, fname, rep):
    for tag in ("div", "details"):
        o = len(re.findall(rf"<{tag}\b", text))
        c = len(re.findall(rf"</{tag}>", text))
        if o != c:
            rep.err(fname, f"<{tag}>-Bilanz: {o} offen, {c} geschlossen")


def check_duplicate_ids(text, fname, rep):
    ids = re.findall(r'\bid="([^"]+)"', text)
    seen = {}
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
    dups = [f"{k} ({v}×)" for k, v in seen.items() if v > 1]
    if dups:
        rep.err(fname, "doppelte IDs: " + ", ".join(dups))


def check_no_eszett(text, fname, rep):
    n = text.count("ß")
    if n:
        idx = text.index("ß")
        ctx = text[max(0, idx - 20): idx + 20].replace("\n", " ")
        rep.err(fname, f"{n}× ß gefunden, erstes: …{ctx}…")


def check_decimal_comma_in_math(text, fname, rep):
    body = _strip_scripts(text)
    spans = re.findall(r"\\\((.*?)\\\)", body, re.DOTALL) + \
            re.findall(r"\\\[(.*?)\\\]", body, re.DOTALL)
    hits = []
    for span in spans:
        span = re.sub(r"[_^]\s*\{[^{}]*\}", "", span)   # Index-/Hochzahl-Gruppen raus
        for m in re.finditer(r"\d,\d", span):
            frag = span[max(0, m.start() - 8): m.end() + 8].replace("\n", " ")
            hits.append(frag.strip())
    if hits:
        rep.err(fname, "Dezimalkomma in Math: " + "; ".join(hits[:5]))


def check_html_in_math(text, fname, rep):
    r"""HTML-Element innerhalb eines LaTeX-Ausdrucks.

    MathJax bricht daran ab und zeigt die Formel als Rohtext — sichtbar oft
    erst, wenn ein Akkordeon geöffnet wird. Typischer Fall: eine Lücke
    <span class="mc-luecke"> im Index einer Formel.
    Das Kleiner-Zeichen in \(a < b\) ist erlaubt: gesucht wird ein echtes Tag.
    """
    body = _strip_scripts(text)
    spans = re.findall(r"\\\((.*?)\\\)", body, re.DOTALL) + \
            re.findall(r"\\\[(.*?)\\\]", body, re.DOTALL)
    tag = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*[^<>]*>")
    hits = [s.strip()[:70] for s in spans if tag.search(s)]
    if hits:
        rep.err(fname, "HTML im LaTeX-Ausdruck (MathJax rendert nicht): " + "; ".join(hits[:3]))


def check_skeleton(text, fname, rep):
    pw = len(re.findall(r"page-wrap", text))
    mc = len(re.findall(r'main class="content"', text))
    # Themenseiten binden ../nav.js ein, Wurzelseiten nav.js — beides gilt.
    nav_defer = len(re.findall(r'src="(?:\.\./)?nav\.js" defer', text))
    nav_any = len(re.findall(r'src="(?:\.\./)?nav\.js"', text))
    if pw != 1:
        rep.err(fname, f'Skelett: page-wrap {pw}× (erwartet 1)')
    if mc != 1:
        rep.err(fname, f'Skelett: main class="content" {mc}× (erwartet 1)')
    if nav_defer:
        rep.err(fname, "Skelett: nav.js mit defer (erwartet ohne defer)")
    if nav_any == 0:
        rep.warn(fname, "Skelett: keine nav.js-Einbindung gefunden")
    for cls in PHANTOM_CLASSES:
        if re.search(rf'class="{re.escape(cls)}"', text):
            rep.err(fname, f'Phantom-Klasse class="{cls}" — existiert im CSS nicht')


def check_lib_dep(text, fname, rep):
    toggles = len(re.findall(r'class="loesung-toggle"', text))
    has_lib = len(re.findall(rf'src="\.\./{re.escape(LIB)}"', text))
    if toggles and not has_lib:
        rep.err(fname, f"{toggles} Lösungs-Toggle, aber {LIB} nicht eingebunden")


def check_resources_section(text, fname, rep):
    for marker in UNIQUE_MARKERS:
        if len(re.findall(marker, text)) > 1:
            rep.err(fname, f"Duplicate-Marker '{marker}' (erwartet ≤1)")
    m = re.search(r'<h2 id="ressourcen".*?</main>', text, re.DOTALL)
    if not m:
        return
    block = m.group(0)
    # Der generierte Clip-Block folgt auf die Ressourcen und hat eigene Links
    # («zur Animation») — er gehoert nicht zur Zaehlung
    block = block.split('<!-- CLIPS:ANFANG', 1)[0]
    a_open = len(re.findall(r'<a [^>]*class="lk', block))
    a_close = len(re.findall(r"</a>", block))
    if a_open and a_open != a_close:
        rep.err(fname, f'Ressourcen: {a_open} <a class="lk">, {a_close} </a>')
    # Slot-Limits: je Sektion höchstens 4 <a href=
    for emoji_a, emoji_b, label in (("🎬", "🧪", "Videos"),
                                    ("🧪", "📝", "Simulationen"),
                                    ("📝", None, "Aufgaben")):
        start = block.find(emoji_a)
        if start < 0:
            continue
        end = block.find(emoji_b, start) if emoji_b else len(block)
        if end < 0:
            end = len(block)
        n = len(re.findall(r"<a href=", block[start:end]))
        if n > 4:
            rep.err(fname, f"Slot-Limit {label}: {n} Links (erwartet ≤4)")


FREMDHOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")


def check_keine_fremdhosts(text, fname, rep):
    """Schriften und MathJax werden lokal ausgeliefert (schriften.css,
    vendor/mathjax/). Ein Aufruf an einen Fremdhost uebertraegt die IP-Adresse
    der Besucherin an einen Dritten — der Fussbereich sagt aber «Keine Cookies ·
    Kein Tracking». Ohne diesen Check kommt der CDN-Aufruf beim naechsten
    Kopieren einer alten Vorlage zurueck."""
    for host in FREMDHOSTS:
        n = text.count(host)
        if n:
            rep.err(fname, f"{n}x {host} — lokal einbinden "
                           f"(schriften.css bzw. vendor/mathjax/tex-svg.js)")


def run_light(path, rep):
    fname = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        rep.err(fname, f"nicht lesbar: {e}")
        return
    check_tag_balance(text, fname, rep)
    check_duplicate_ids(text, fname, rep)
    check_no_eszett(text, fname, rep)
    check_decimal_comma_in_math(text, fname, rep)
    check_html_in_math(text, fname, rep)
    # Skelett, Bibliotheks-Einbindung und Ressourcen-Sektion beschreiben den
    # Aufbau einer THEMENSEITE. Die Startseite, die Nachschlagen-Seiten und die
    # Leitprogramme haben bewusst ein eigenes Geruest — dort meldete der Check
    # `page-wrap 0x` und `main class="content" 0x` als Fehler, die keine sind.
    if "themen" in path.parts:
        check_skeleton(text, fname, rep)
        check_lib_dep(text, fname, rep)
        check_resources_section(text, fname, rep)
    # Fremdhosts gelten ueberall — die Datenschutzaussage im Fussbereich auch.
    check_keine_fremdhosts(text, fname, rep)


# ---------- Stufe 2: vorhandene Repo-Skripte orchestrieren ----------

def _dep_present(name):
    return Path("node_modules", name).is_dir()


def _run_node(script, file_args, env):
    return subprocess.run(["node", script, *file_args],
                          capture_output=True, text=True, env=env)


def check_clips(wurzel, rep):
    """Konsistenz der Clip-Ablage. Faellt sonst nirgends auf: ein Clip ohne
    Eintrag fehlt lautlos in der Bibliothek, ein Eintrag ohne Datei liefert
    dort einen toten Knopf, und ein `lektion`-Code, den nav.js nicht kennt,
    landet auf keiner Seite."""
    import json as _json
    clips = wurzel / "clips"
    index = clips / "clips.json"
    if not clips.is_dir() or not index.is_file():
        return

    try:
        eintraege = _json.loads(index.read_text(encoding="utf-8")).get("clips", [])
    except ValueError as e:
        rep.err("clips.json", f"nicht lesbar: {e}")
        return

    # Drehbuecher mit "probe": true sind Versuche. Sie werden gebaut, aber
    # bewusst nicht ins Verzeichnis aufgenommen — sonst stuenden sie in der
    # Bibliothek und auf den Lektionsseiten.
    proben = set()
    for d in clips.glob("*.json"):
        if d.name == "clips.json":
            continue
        try:
            dreh = _json.loads(d.read_text(encoding="utf-8"))
            if dreh.get("probe"):
                proben.add((dreh.get("dateiname") or d.stem) + ".html")
        except ValueError:
            pass

    dateien = {f.name for f in clips.glob("*.html")} - proben
    gelistet = {e.get("datei", "") for e in eintraege}
    for fehlt in sorted(gelistet - dateien):
        rep.err("clips.json", f"Eintrag '{fehlt}' hat keine Datei")
    for fehlt in sorted(dateien - gelistet):
        rep.err("clips/", f"{fehlt} steht nicht in clips.json — "
                          "`python3 scripts/build-clips.py`")

    nav = wurzel / "nav.js"
    bekannt = set(re.findall(r"id:\s*'([^']+)'", nav.read_text(encoding="utf-8"))) \
        if nav.is_file() else set()
    for e in eintraege:
        codes = e.get("lektion") or []
        if isinstance(codes, str):
            codes = [codes]
        if not codes:
            rep.err("clips.json", f"{e.get('datei')}: Feld 'lektion' ist leer")
        for c in codes:
            if bekannt and c not in bekannt:
                rep.err("clips.json", f"{e.get('datei')}: Lektion '{c}' "
                                      "steht nicht in nav.js")
        stamm = e.get("datei", "").replace(".html", "")
        if stamm and not (clips / f"sprechertext-{stamm}.txt").is_file():
            rep.warn("clips/", f"kein Sprechertext zu {e.get('datei')} — "
                               "die Seite bekommt kein Transkript")


def run_deep(file_args, rep):
    scripts = Path("scripts")
    if not scripts.is_dir():
        rep.warn("deep", "scripts/ nicht gefunden — Pre-Flight vom Repo-Root aufrufen")
        return
    env = dict(os.environ)
    env["NODE_PATH"] = "node_modules"

    mj = scripts / "verify_mathjax.js"
    if mj.is_file():
        if not _dep_present("mathjax-full"):
            rep.warn("verify_mathjax.js", "node_modules/mathjax-full fehlt — `npm install mathjax-full`")
        else:
            r = _run_node(str(mj), file_args, env)
            out = (r.stdout or "") + (r.stderr or "")
            print("---- verify_mathjax.js ----")
            print(out.rstrip())
            m = re.search(r"SUMME:.*?(\d+)\s+Fehler", out)
            if r.returncode != 0:
                rep.err("verify_mathjax.js", f"Skript-Abbruch (exit {r.returncode})")
            elif m and int(m.group(1)) > 0:
                rep.err("verify_mathjax.js", f"{m.group(1)} MathJax-Fehler")
            elif not m:
                rep.warn("verify_mathjax.js", "Summenzeile nicht erkannt")

    js = scripts / "verify_js_runtime.js"
    # Das Skript ersetzt Bibliotheks-Einbindungen der Form src="../nav.js" —
    # es rechnet also mit Seiten genau eine Ebene tief. Wurzelseiten
    # (index, glossar, formelsammlung, rechtliches, feedback) wuerden dort
    # einen falschen [FEHLER] erzeugen, darum bekommt es nur Themenseiten
    # zu sehen — und die Simulationen und Werkzeuge, die ebenso eine Ebene
    # tief liegen, sofern sie die Bibliothek einbinden. Ohne sie hat eine Seite
    # einen eigenen Aufbau (die Sonnenfinsternis), und das Skript meldete
    # «libs=FEHLEN», ohne dass etwas fehlt.
    themenseiten = [f for f in file_args
                    if f.replace("\\", "/").split("/")[0] == "themen"
                    or (f.replace("\\", "/").split("/")[0] in ("simulationen", "werkzeuge")
                        and f'src="../{LIB}"' in Path(f).read_text(encoding="utf-8"))]
    if js.is_file() and not themenseiten:
        print("---- verify_js_runtime.js ----")
        print("keine Themenseiten uebergeben — uebersprungen")
    elif js.is_file():
        if not _dep_present("jsdom"):
            rep.warn("verify_js_runtime.js", "node_modules/jsdom fehlt — `npm install jsdom`")
        else:
            r = _run_node(str(js), themenseiten, env)
            out = (r.stdout or "") + (r.stderr or "")
            print("---- verify_js_runtime.js ----")
            print(out.rstrip())
            m = re.search(r"Problematische Seiten:\s*(\d+)", out)
            if r.returncode != 0:
                rep.err("verify_js_runtime.js", f"Skript-Abbruch (exit {r.returncode})")
            elif m and int(m.group(1)) > 0:
                rep.err("verify_js_runtime.js", f"{m.group(1)} Seite(n) mit JS-Problemen")
            elif not m:
                rep.warn("verify_js_runtime.js", "Summenzeile nicht erkannt")

    et = scripts / "verify_einheitentrainer.js"
    if et.is_file():
        if not _dep_present("jsdom"):
            rep.warn("verify_einheitentrainer.js", "node_modules/jsdom fehlt — `npm install jsdom`")
        else:
            r = _run_node(str(et), [], env)
            out = (r.stdout or "") + (r.stderr or "")
            print("---- verify_einheitentrainer.js ----")
            print(out.rstrip())
            if r.returncode != 0:
                rep.err("verify_einheitentrainer.js", "Einheitentrainer-Tests fehlgeschlagen (siehe oben)")

    si = scripts / "build-suchindex.py"
    if si.is_file():
        r = subprocess.run(["python3", str(si), "--check"], capture_output=True, text=True)
        if r.returncode != 0:
            rep.warn("suchindex", "Suchindex veraltet — `python3 scripts/build-suchindex.py`")

    seo = scripts / "build-seo.py"
    if seo.is_file():
        r = subprocess.run(["python3", str(seo), "--check"], capture_output=True, text=True)
        if r.returncode != 0:
            rep.warn("seo", "Metadaten/sitemap veraltet — `python3 scripts/build-seo.py`")

    ba = scripts / "build-animationen.py"
    if ba.is_file():
        r = subprocess.run(["python3", str(ba), "--check"], capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        print("---- build-animationen.py ----")
        print(out.rstrip())
        if r.returncode != 0:
            rep.err("animationen", "Animationsnummern/-verweise stimmen nicht "
                                   "(siehe oben)")


    check_clips(scripts.parent, rep)
    check_sim_wz(scripts.parent, rep)

    ab = scripts / "abgleich.py"
    if ab.is_file():
        r = subprocess.run(["python3", str(ab), "--check"], capture_output=True, text=True)
        if r.returncode != 0:
            rep.warn("abgleich", "neue Drift gegen das Schwesterrepo — "
                                 "`python3 scripts/abgleich.py`")

    check_todo_schwester(scripts.parent, rep)

    ic = scripts / "check_identifier_collisions.py"
    if ic.is_file():
        r = subprocess.run(["python3", str(ic)], capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        print("---- check_identifier_collisions.py ----")
        print(out.rstrip())
        if r.returncode != 0:
            rep.err("check_identifier_collisions.py", "blockierende Symbol-Kollision (siehe oben)")


def check_sim_wz(wurzel, rep):
    """Simulationen und Werkzeuge: eigene Seiten in simulationen/ und werkzeuge/.

    Sie haengen an drei Stellen zusammen, und keine faellt von selbst auf, wenn
    sie fehlt: die Kachel in der Uebersicht (simulationen.html / werkzeuge.html),
    der Verweis aus dem Abschnitt einer Themenseite und der Ruecklink der Seite
    auf diesen Abschnitt. Geprueft wird nur der href, nicht der Baustein darum.
      [FEHLER] Seite fehlt in ihrer Uebersicht
      [FEHLER] Ruecklink-Anker (../<themenordner>/x.html#a) zeigt ins Leere
      [FEHLER] Themenseite verlinkt eine Simulation/ein Werkzeug, das es nicht gibt
      [WARN]   keine Themenseite verlinkt die Seite — ausser die Uebersicht fuehrt
               sie unter <h2 id="ausserhalb">
    HOWTO-simulationen.md, HOWTO-werkzeuge.md.
    """
    wurzel = Path(wurzel)
    themenordner = [d for d in ("themen", "grundlagen", "schwerpunkt") if (wurzel / d).is_dir()]
    themen = {f"{d}/{f.name}": f.read_text(encoding="utf-8")
              for d in themenordner for f in sorted((wurzel / d).glob("*.html"))}
    ids_cache = {}

    def hat_id(rel, anker):
        if rel not in ids_cache:
            pfad = wurzel / rel
            ids_cache[rel] = (set(re.findall(r'\bid="([^"]+)"', pfad.read_text(encoding="utf-8")))
                              if pfad.is_file() else None)
        return ids_cache[rel] is not None and anker in ids_cache[rel]

    for art in ("simulationen", "werkzeuge"):
        ordner = wurzel / art
        uebersicht = wurzel / f"{art}.html"
        seiten = sorted(ordner.glob("*.html")) if ordner.is_dir() else []
        for rel_t, text in themen.items():
            for ziel in re.findall(rf'href="\.\./{art}/([^"#]+)', text):
                if not (ordner / ziel).is_file():
                    rep.err(rel_t, f"verlinkt {art}/{ziel}, die Datei gibt es nicht")
        if not seiten:
            continue
        ue = uebersicht.read_text(encoding="utf-8") if uebersicht.is_file() else ""
        if not ue:
            rep.err(f"{art}.html", f"Uebersicht fehlt, aber {art}/ enthaelt {len(seiten)} Seite(n)")
        m = re.search(r'<h2 id="ausserhalb".*?(?=<h2 |<!-- [A-Z]+:ENDE|\Z)', ue, re.S)
        ausserhalb = m.group(0) if m else ""
        for f in seiten:
            rel = f"{art}/{f.name}"
            if f'href="{rel}"' not in ue:
                rep.err(rel, f"nicht in {art}.html verlinkt (Kachel fehlt)")
            verlinkt = any(re.search(rf'href="\.\./{re.escape(rel)}["#]', t) for t in themen.values())
            if not verlinkt and f'href="{rel}"' not in ausserhalb:
                rep.warn(rel, "keine Themenseite verlinkt darauf — Baustein im passenden "
                              "Abschnitt setzen oder in der Uebersicht unter «Ausserhalb der Lerngebiete» fuehren")
            text = f.read_text(encoding="utf-8")
            for d, datei, anker in re.findall(r'href="\.\./([a-z]+)/([^"#]+\.html)#([^"]+)"', text):
                if d in themenordner and not hat_id(f"{d}/{datei}", anker):
                    rep.err(rel, f"Ruecklink {d}/{datei}#{anker}: Anker gibt es nicht")


def check_todo_schwester(wurzel, rep):
    """Offene Eintraege in der TODO-Datei des Schwesterrepos.

    Die Warteschlange OFFEN in scripts/abgleich.py meldet sich ueber die
    Drift von selbst. Mathes TODO-schwesterprojekt.md (Inhaltsauftraege an
    Physik) dagegen sah der Pre-Flight nicht — sie wurde nur gelesen, wenn
    jemand daran dachte. Gelesen wird die Datei im Nachbarordner, nie
    geschrieben. Physik fuehrt keine solche Datei (das Repo ist die Website);
    in Mathe findet der Check darum nichts und schweigt.
    """
    wurzel = Path(wurzel).resolve()
    physik = (wurzel / "physiklib.js").is_file()
    todo = wurzel.parent / ("tals-mathe" if physik else "tals-physik") / "TODO-schwesterprojekt.md"
    if not todo.is_file():
        return
    text = todo.read_text(encoding="utf-8")
    m = re.search(r"^## Offen\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return
    titel = []
    for e in re.finditer(r"^- \*\*(.+?)(?:\*\*|$)", m.group(1), re.M):
        teile = [t.strip() for t in e.group(1).split(" · ") if t.strip(" ·")]
        titel.append(" · ".join(teile[:2]).rstrip(" ·"))
    if not titel:
        return
    print("---- " + todo.parent.name + "/TODO-schwesterprojekt.md ----")
    for t in titel:
        print("  · " + t)
    n = len(titel)
    rep.warn("todo-schwester", "%d %s fuer dieses Repo in `../%s/TODO-schwesterprojekt.md`"
             % (n, "offener Eintrag" if n == 1 else "offene Eintraege", todo.parent.name))


def main(argv):
    args = argv[1:]
    if not args:
        print("Aufruf: python3 .claude/skills/preflight/preflight.py themen/*.html")
        return 2
    paths = [Path(a) for a in args]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        print("[FEHLER] Datei(en) nicht gefunden: " + ", ".join(missing))
        return 2

    rep = Report()
    for p in paths:
        run_light(p, rep)
    run_deep(args, rep)

    print("-" * 60)
    if rep.errors == 0:
        suffix = f" ({rep.warns} Warnung[en])" if rep.warns else ""
        print(f"ALLE CHECKS BESTANDEN{suffix}")
        return 0
    print(f"NICHT BESTANDEN: {rep.errors} Fehler, {rep.warns} Warnung(en) — nicht committen")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
