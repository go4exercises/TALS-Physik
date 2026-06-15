#!/usr/bin/env python3
# minicheck_lib.py — baut einklappbare Mini-Checks (MC, Lückentext, kurze
# Rechnung, Transfer) und fügt sie je Abschnitt vor dem nächsten <h2> ein.
import pathlib

L = '<span class="mc-luecke"></span>'

def loesung(inner, label="Lösung anzeigen"):
    return '<details class="mc-loesung"><summary>'+label+'</summary><div class="mc-antwort">'+inner+'</div></details>'

def mc(frage, opts, sol):
    lis = "".join('<li data-opt="'+o[0]+'">'+o[1]+'</li>' for o in opts)
    return '<div class="mc-item"><span class="mc-typ">Multiple Choice</span><p class="mc-frage">'+frage+'</p><ul class="mc-optionen">'+lis+'</ul>'+loesung(sol)+'</div>'

def lueck(frage, sol):
    return '<div class="mc-item"><span class="mc-typ">Lückentext</span><p class="mc-frage">'+frage+'</p>'+loesung(sol)+'</div>'

def rech(frage, sol):
    return '<div class="mc-item"><span class="mc-typ">Kurze Rechnung</span><p class="mc-frage">'+frage+'</p>'+loesung(sol)+'</div>'

def block(items, tf_frage, tf_sol):
    transfer = '<div class="mc-item"><span class="mc-typ">Transfer</span><p class="mc-frage">'+tf_frage+'</p>'+loesung(tf_sol, "Lösungsweg anzeigen")+'</div>'
    inner = "\n".join(items)+"\n"+transfer
    return '<details class="minicheck">\n<summary class="mc-kopf">✏️ Mini-Check</summary>\n'+inner+'\n</details>\n\n'

def _add_include(t):
    inc = '<script src="../anim-hinweise.js"></script>'
    add = '\n<script src="../minicheck.js"></script>'
    if '../minicheck.js' in t:
        return t
    assert inc in t, "anim-hinweise-Include fehlt"
    return t.replace(inc, inc+add, 1)

def apply_page(path, pairs):
    """pairs = ordered list of (anchor_id, block_html); block wird vor <h2 id=anchor> eingefügt."""
    p = pathlib.Path(path); t = p.read_text(encoding='utf-8')
    if 'class="minicheck"' in t:
        raise SystemExit(path+": Mini-Checks bereits vorhanden (Abbruch).")
    for anchor, blk in pairs:
        pat = '<h2 id="'+anchor+'">'
        idx = t.find(pat)
        if idx == -1:
            raise SystemExit(path+": Anker fehlt: "+anchor)
        t = t[:idx]+blk+t[idx:]
    t = _add_include(t)
    p.write_text(t, encoding='utf-8')
    do_, dc = t.count('<div'), t.count('</div>')
    oo, oc = t.count('\\('), t.count('\\)')
    return len(pairs), do_, dc, oo, oc
