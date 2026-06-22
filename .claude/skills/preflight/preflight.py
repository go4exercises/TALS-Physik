#!/usr/bin/env python3
"""
Pre-Flight-Check für TALS-Physik-Themenseiten.
Bündelt die grep-basierten Checks aus COLLABORATION.md §3.6–3.8 plus die generellen
Audit-Checks (MathJax-Parität, doppelte IDs, kein ß, Dezimalkomma in Math, node --check)
in einem deterministischen Lauf.

Aufruf:  python3 preflight.py themen/p4-1-kinematik.html
         python3 preflight.py themen/*.html

Exit 0  -> alle Checks bestanden.
Exit 1  -> mindestens ein [FEHLER]. Nicht committen.
"""
import re
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

PHANTOM_CLASSES = [
    "inhalt", "brot", "seiten-kopf", "rlp", "rlp-list", "rlp-label", "seiten-fuss",
    "dl-box", "ressourcen-grid", "ress", "ress-titel", "ress-beschr", "ress-quelle",
]

# Marker, die in der Ressourcen-Sektion genau einmal vorkommen müssen.
UNIQUE_MARKERS = [
    r'<h2 id="ressourcen"',
    r'ressourcen-subtitel">🎬',
    r'ressourcen-subtitel">🧪',
    r'ressourcen-subtitel">📝',
    r'<aside class="toc-wrap"',
    r'<footer class="site-footer"',
]


class Report:
    def __init__(self):
        self.errors = 0
        self.warns = 0

    def err(self, fname, msg):
        print(f"[FEHLER] {fname}: {msg}")
        self.errors += 1

    def warn(self, fname, msg):
        print(f"[WARN]   {fname}: {msg}")
        self.warns += 1


def check_tag_balance(text, fname, rep):
    for tag in ("div", "details"):
        opens = len(re.findall(rf"<{tag}\b", text))
        closes = len(re.findall(rf"</{tag}>", text))
        if opens != closes:
            rep.err(fname, f"<{tag}>-Bilanz: {opens} offen, {closes} geschlossen")


def check_mathjax_parity(text, fname, rep):
    # \( ... \)  und  \[ ... \]  jeweils paarweise.
    o_par = len(re.findall(r"\\\(", text))
    c_par = len(re.findall(r"\\\)", text))
    o_brk = len(re.findall(r"\\\[", text))
    c_brk = len(re.findall(r"\\\]", text))
    if o_par != c_par:
        rep.err(fname, rf"MathJax inline: {o_par}× \( vs {c_par}× \)")
    if o_brk != c_brk:
        rep.err(fname, rf"MathJax abgesetzt: {o_brk}× \[ vs {c_brk}× \]")


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
        # erste Fundstelle für Kontext
        idx = text.index("ß")
        ctx = text[max(0, idx - 20): idx + 20].replace("\n", " ")
        rep.err(fname, f"{n}× ß gefunden, erstes: …{ctx}…")


def _math_spans(text):
    """Liefert alle Textstücke innerhalb von \\(...\\) und \\[...\\]."""
    spans = []
    for m in re.finditer(r"\\\((.*?)\\\)", text, re.DOTALL):
        spans.append(m.group(1))
    for m in re.finditer(r"\\\[(.*?)\\\]", text, re.DOTALL):
        spans.append(m.group(1))
    return spans


def check_decimal_comma_in_math(text, fname, rep):
    # Nur INNERHALB von Math-Delimitern. Ausserhalb (URLs mit ital,opsz,wght@,
    # SVG-Pfade, JS-Arrays) wird bewusst nicht geprüft -> keine False Positives.
    hits = []
    for span in _math_spans(text):
        for m in re.finditer(r"\d,\d", span):
            frag = span[max(0, m.start() - 8): m.end() + 8].replace("\n", " ")
            hits.append(frag.strip())
    if hits:
        rep.err(fname, "Dezimalkomma in Math: " + "; ".join(hits[:5]))


def check_inline_js(text, fname, rep, node_path):
    # Alle <script> ohne src extrahieren und durch node --check schicken.
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>",
                        text, re.DOTALL | re.IGNORECASE)
    if not blocks:
        return
    if node_path is None:
        rep.warn(fname, "node nicht gefunden -> JS-Syntax-Check übersprungen")
        return
    for i, code in enumerate(blocks, 1):
        if not code.strip():
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
            tf.write(code)
            tmp = tf.name
        try:
            r = subprocess.run([node_path, "--check", tmp],
                               capture_output=True, text=True)
            if r.returncode != 0:
                first = (r.stderr.strip().splitlines() or ["(keine Meldung)"])[0]
                rep.err(fname, f"JS-Syntaxfehler in <script> #{i}: {first}")
        finally:
            Path(tmp).unlink(missing_ok=True)


def check_skeleton(text, fname, rep):
    pw = len(re.findall(r"page-wrap", text))
    mc = len(re.findall(r'main class="content"', text))
    nav_ok = len(re.findall(r'src="\.\./nav\.js">', text))
    nav_defer = len(re.findall(r'src="\.\./nav\.js" defer', text))
    if pw != 1:
        rep.err(fname, f'Skelett: page-wrap {pw}× (erwartet 1)')
    if mc != 1:
        rep.err(fname, f'Skelett: main class="content" {mc}× (erwartet 1)')
    if nav_defer:
        rep.err(fname, "Skelett: nav.js mit defer (erwartet ohne defer)")
    if nav_ok == 0 and nav_defer == 0:
        rep.warn(fname, "Skelett: keine nav.js-Einbindung gefunden")
    for cls in PHANTOM_CLASSES:
        if re.search(rf'class="{re.escape(cls)}"', text):
            rep.err(fname, f'Phantom-Klasse class="{cls}" — existiert im CSS nicht')


def check_physiklib_dep(text, fname, rep):
    toggles = len(re.findall(r'class="loesung-toggle"', text))
    has_lib = len(re.findall(r'src="\.\./physiklib\.js"', text))
    if toggles and not has_lib:
        rep.err(fname, f"{toggles} Lösungs-Toggle, aber physiklib.js nicht eingebunden")


def check_resources_section(text, fname, rep):
    # Duplicate-Marker
    for marker in UNIQUE_MARKERS:
        n = len(re.findall(marker, text))
        if n > 1:
            rep.err(fname, f"Duplicate-Marker '{marker}' {n}× (erwartet ≤1)")
    # Tag-Bilanz <a class="lk"> innerhalb der Ressourcen-Sektion
    m = re.search(r'<h2 id="ressourcen".*?</main>', text, re.DOTALL)
    if not m:
        return
    block = m.group(0)
    a_open = len(re.findall(r'<a [^>]*class="lk', block))
    a_close = len(re.findall(r"</a>", block))
    if a_open and a_open != a_close:
        rep.err(fname, f'Ressourcen: {a_open} <a class="lk">, {a_close} </a>')
    # Slot-Limits: zwischen 🎬→🧪, 🧪→📝, 📝→Ende je max. 4 <a href=
    for emoji_a, emoji_b, label in (("🎬", "🧪", "Videos"),
                                    ("🧪", "📝", "Simulationen"),
                                    ("📝", None, "Aufgaben")):
        start = block.find(emoji_a)
        if start < 0:
            continue
        end = block.find(emoji_b, start) if emoji_b else len(block)
        if end < 0:
            end = len(block)
        seg = block[start:end]
        n = len(re.findall(r"<a href=", seg))
        if n > 4:
            rep.err(fname, f"Slot-Limit {label}: {n} Links (erwartet ≤4)")


def run_file(path, rep, node_path):
    fname = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        rep.err(fname, f"nicht lesbar: {e}")
        return
    check_tag_balance(text, fname, rep)
    check_mathjax_parity(text, fname, rep)
    check_duplicate_ids(text, fname, rep)
    check_no_eszett(text, fname, rep)
    check_decimal_comma_in_math(text, fname, rep)
    check_inline_js(text, fname, rep, node_path)
    check_skeleton(text, fname, rep)
    check_physiklib_dep(text, fname, rep)
    check_resources_section(text, fname, rep)


def main(argv):
    args = argv[1:]
    if not args:
        print("Aufruf: python3 preflight.py themen/<datei>.html [...]")
        return 2
    paths = [Path(a) for a in args]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        print("[FEHLER] Datei(en) nicht gefunden: " + ", ".join(missing))
        return 2
    node_path = shutil.which("node")
    rep = Report()
    for p in paths:
        run_file(p, rep, node_path)
    print("-" * 60)
    if rep.errors == 0:
        suffix = f" ({rep.warns} Warnung[en])" if rep.warns else ""
        print(f"ALLE CHECKS BESTANDEN{suffix}")
        return 0
    print(f"NICHT BESTANDEN: {rep.errors} Fehler, {rep.warns} Warnung(en) — nicht committen")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
