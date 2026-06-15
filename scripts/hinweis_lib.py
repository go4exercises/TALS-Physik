#!/usr/bin/env python3
# hinweis_lib.py — baut die Titelzeile-Hinweise und ersetzt damit
# je Animation den Header (<h3> + bisherige Bedienungs-<p>).
import re, pathlib

def _esc(s): return s.replace('&','&amp;').replace('"','&quot;')

def _hint(side, label, titel, bullets, spoken):
    lis = "".join("<li>"+b+"</li>" for b in bullets)
    return ('  <div class="anim-hinweis '+side+'">\n'
            '    <span class="ah-trigger" tabindex="0" role="button" aria-haspopup="true" aria-label="'+titel+' zu dieser Animation">'+label+'</span>\n'
            '    <div class="ah-pop" role="tooltip">\n'
            '      <span class="ah-titel">'+titel+'</span>\n'
            '      <div class="ah-text"><ul>'+lis+'</ul></div>\n'
            '      <button type="button" class="ah-speak" data-vorlesen="'+_esc(spoken)+'" aria-pressed="false">🔊 vorlesen</button>\n'
            '    </div>\n  </div>')

def _titelzeile(h3, it):
    return ('<div class="widget-titelzeile">\n  <h3>'+h3+'</h3>\n'
            + _hint("links","💡 Worauf achten?","Worauf achten?", it['w'], it['ws']) + '\n'
            + _hint("rechts","✓ Erkenntnis","Erkenntnis", it['e'], it['es']) + '\n'
            + '</div>')

def build_and_apply(path, items):
    p = pathlib.Path(path); t = p.read_text(encoding='utf-8')
    pat = re.compile(r'<div class="widget-header">\s*<h3>(.*?)</h3>(\s*<p>.*?</p>)?', re.S)
    matches = list(pat.finditer(t))
    if len(matches) != len(items):
        raise SystemExit(f"{path}: {len(matches)} Header gefunden, aber {len(items)} Inhalte geliefert")
    for m, it in sorted(zip(matches, items), key=lambda mi: mi[0].start(), reverse=True):
        h3 = m.group(1).strip()
        repl = '<div class="widget-header">\n' + _titelzeile(h3, it)
        t = t[:m.start()] + repl + t[m.end():]
    p.write_text(t, encoding='utf-8')
    # einfache Balance-/Zaehlkontrolle
    do_ = t.count('<div'); dc = t.count('</div>')
    return len(items), do_, dc
