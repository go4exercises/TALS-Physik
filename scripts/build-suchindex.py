#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  TALS Physik — Suchindex-Generator
#
#  Liest die Themenseiten, das Glossar und die Formelsammlung, schneidet
#  den *Fliesstext* an den <h2 id="…">-Ankern in Abschnitte und schreibt
#  daraus  suchindex.js  (window.SUCHINDEX = {…}).
#
#  Ausgabe bewusst als .js und nicht als .json: so funktioniert die Suche
#  auch, wenn eine Seite lokal per file:// geoeffnet wird (fetch() auf JSON
#  scheitert dort an CORS).
#
#  Aufruf (immer vom Repo-Root):
#      python3 scripts/build-suchindex.py            # neu bauen
#      python3 scripts/build-suchindex.py --check    # nur pruefen, ob aktuell
#                                                    # Exit 1 = veraltet
#
#  Was NICHT in den Index kommt (Entscheid: nur Fliesstext):
#    - Mini-Checks (.minicheck) und Verstaendnisfragen (.frage)
#    - Aufgaben (Sektion #aufgaben, .block-aufg, .aufg-liste)
#    - Zusatzmaterial (#downloads) und externe Ressourcen (#ressourcen)
#    - Animationen: Bedienelemente und Live-Werte (.widget-body, <canvas>)
#      — Titel und Hinweis der Animation bleiben drin
#    - Navigation, Footer, Scripts, Styles
# ─────────────────────────────────────────────────────────────

import hashlib
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'suchindex.js')

# ── Was uebersprungen wird ────────────────────────────────────
SKIP_TAGS = {'script', 'style', 'canvas', 'svg', 'noscript', 'template', 'head'}
VOID_TAGS = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'col',
             'area', 'base', 'embed', 'param', 'track', 'wbr'}

SKIP_CLASSES = {
    'minicheck', 'mc-item', 'mc-kopf',      # Mini-Checks
    'frage',                                 # Verstaendnisfragen ❓
    'block-aufg', 'aufg-liste', 'aufg',      # Aufgaben
    'widget-body',                           # Animations-Bedienung + Live-Werte
    'dl-grid', 'links-grid',                 # Kachel-/Linklisten
    'toc-wrap', 'site-footer', 'mobile-nav', 'site-hdr',
}
SKIP_IDS = {'nav-root', 'toc'}

# Ganze Abschnitte, die uebersprungen werden (h2-Anker)
SKIP_SECTIONS = {'aufgaben', 'downloads', 'ressourcen'}

# ── LaTeX-Bereinigung ─────────────────────────────────────────
# Griechische Buchstaben und ein paar Begriffe behalten ihren Namen als Wort,
# alle uebrigen Makros fliegen raus (sonst findet man „frac" statt „Bruch").
KEEP_MACROS = {
    'alpha', 'beta', 'gamma', 'Gamma', 'delta', 'Delta', 'epsilon', 'zeta',
    'eta', 'theta', 'Theta', 'lambda', 'Lambda', 'mu', 'nu', 'xi', 'pi', 'Pi',
    'rho', 'sigma', 'Sigma', 'tau', 'phi', 'Phi', 'chi', 'psi', 'Psi',
    'omega', 'Omega', 'sin', 'cos', 'tan', 'log', 'ln', 'sqrt',
}

# Makros, die als Zeichen erhalten bleiben (damit „°C" oder „≈" suchbar sind)
MACRO_ZEICHEN = [
    (r'\\circ', '°'), (r'\\cdot', '·'), (r'\\approx', '≈'), (r'\\times', '×'),
    (r'\\pm', '±'), (r'\\leq', '≤'), (r'\\geq', '≥'), (r'\\neq', '≠'),
    (r'\\Rightarrow', '⇒'), (r'\\rightarrow', '→'), (r'\\to', '→'),
]


def clean_math(t):
    t = t.replace('\\(', ' ').replace('\\)', ' ')
    t = t.replace('\\[', ' ').replace('\\]', ' ')
    # Abstands-Makros (\; \, \! \: \ ) restlos weg — sonst bleiben ; und , stehen
    t = re.sub(r'\\[;,!:\s]', ' ', t)
    for pat, zeichen in MACRO_ZEICHEN:
        t = re.sub(pat + r'(?![a-zA-Z])', zeichen, t)
    # \text{kg} → kg   (zweimal, wegen einfacher Verschachtelung)
    for _ in range(2):
        t = re.sub(r'\\(?:text|mathrm|mathbf|mathit|operatorname|mathsf)\s*\{([^{}]*)\}',
                   r' \1 ', t)
    t = re.sub(r'\\([a-zA-Z]+)',
               lambda m: ' ' + m.group(1) + ' ' if m.group(1) in KEEP_MACROS else ' ', t)
    t = re.sub(r'[\\{}$^_&~|]', ' ', t)
    return t


def normalize(t):
    t = clean_math(t)
    t = t.replace('\u00ad', '').replace('\u200b', '')
    t = t.replace('\u00a0', ' ')
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


# ── Parser ────────────────────────────────────────────────────
class Extractor(HTMLParser):
    """Zerlegt eine Seite in Abschnitte {anker, titel, text}."""

    def __init__(self, mode='thema'):
        super().__init__(convert_charrefs=True)
        self.mode = mode            # 'thema' | 'glossar' | 'formeln'
        self.eintraege = []
        self.skipdepth = 0
        self.depth = 0
        self.stack = []             # (tag, war_skip_start)
        self.cur = None             # aktueller Eintrag
        self.cur_anchor = ''        # letzter h2-Anker (fuer Untereintraege)
        self.grab = None            # sammelt Titeltext (h2/h3/ge-begriff)
        self.grab_end = None        # Tag, bei dessen Schluss der Titel fertig ist
        self.section_skipped = False

    # -- Hilfen -------------------------------------------------
    def _flush(self):
        if self.cur:
            txt = normalize(' '.join(self.cur['buf']))
            if txt or self.cur['titel']:
                self.eintraege.append({
                    'anker': self.cur['anker'],
                    'titel': normalize(self.cur['titel']),
                    'text': txt,
                })
        self.cur = None

    def _start(self, anker, titel=''):
        self._flush()
        self.cur = {'anker': anker, 'titel': titel, 'buf': []}

    def _grab_start(self, tag):
        self.grab = []
        self.grab_end = tag

    # -- HTMLParser --------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get('class') or '').split())
        eid = a.get('id', '')

        if tag not in VOID_TAGS:
            self.stack.append(tag)

        if self.skipdepth:
            if tag not in VOID_TAGS:
                self.skipdepth += 1
            return

        # Abschnittswechsel an h2[id]
        if tag == 'h2' and eid:
            self._flush()
            self.section_skipped = eid in SKIP_SECTIONS
            self.cur_anchor = eid
            if not self.section_skipped:
                self._start(eid)
                self._grab_start('h2')
            return

        if self.section_skipped:
            return

        # Untereintraege
        if self.mode == 'glossar' and 'glossar-eintrag' in cls:
            self._start(self.cur_anchor)
            return
        if self.mode == 'glossar' and 'ge-begriff' in cls and self.cur is not None:
            self._grab_start('span')
            return
        if self.mode == 'glossar' and 'ge-quer' in cls:
            self.skipdepth = 1
            return
        if self.mode == 'formeln' and tag == 'h3':
            self._start(self.cur_anchor)
            self._grab_start('h3')
            return
        if self.mode == 'formeln' and 'fs-link' in cls:
            self.skipdepth = 1
            return

        if (tag in SKIP_TAGS or eid in SKIP_IDS or (cls & SKIP_CLASSES)):
            self.skipdepth = 1
            return

        # Seitentitel = erster Eintrag (Intro, Anker = Seitenanfang)
        if tag == 'h1' and self.cur is None:
            self._start('')
            self._grab_start('h1')

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:                 # unsauber geschachtelt: aufraeumen
            while self.stack and self.stack.pop() != tag:
                pass

        if self.skipdepth:
            self.skipdepth -= 1
            return

        if self.grab is not None and tag == self.grab_end:
            titel = normalize(' '.join(self.grab))
            if self.cur is not None:
                self.cur['titel'] = titel
            self.grab = None
            self.grab_end = None

    def handle_data(self, data):
        if self.skipdepth or self.section_skipped:
            return
        if self.grab is not None:
            self.grab.append(data)
        if self.cur is not None:
            self.cur['buf'].append(data)

    def close(self):
        super().close()
        self._flush()


# ── Seitenliste aus nav.js (einzige Quelle der Wahrheit) ──────
def seiten_aus_navjs():
    src = open(os.path.join(ROOT, 'nav.js'), encoding='utf-8').read()
    block = src.split('themen: [', 1)[1].split(']', 1)[0]
    seiten = []
    for m in re.finditer(r"nr:\s*'([^']+)'\s*,\s*titel:\s*'([^']+)'\s*,\s*url:\s*'([^']+)'", block):
        seiten.append({'nr': m.group(1), 'titel': m.group(2), 'url': m.group(3), 'mode': 'thema'})
    seiten.append({'nr': 'A–Z', 'titel': 'Glossar', 'url': 'glossar.html', 'mode': 'glossar'})
    seiten.append({'nr': '∑', 'titel': 'Formelsammlung', 'url': 'formelsammlung.html', 'mode': 'formeln'})
    return seiten


def js_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def build():
    seiten = seiten_aus_navjs()
    eintraege = []

    for pi, s in enumerate(seiten):
        pfad = os.path.join(ROOT, s['url'])
        if not os.path.exists(pfad):
            print(f"[WARN] fehlt: {s['url']}", file=sys.stderr)
            continue
        roh = open(pfad, encoding='utf-8').read()
        ex = Extractor(mode=s['mode'])
        ex.feed(roh)
        ex.close()
        n = 0
        for e in ex.eintraege:
            if len(e['text']) < 40:      # blosse Zwischenueberschrift ohne Inhalt
                continue
            eintraege.append({'p': pi, 'a': e['anker'], 't': e['titel'], 'x': e['text']})
            n += 1
        print(f"  {s['url']:44s} {n:3d} Abschnitte")

    # Fingerabdruck ueber den *indexierten Inhalt*, nicht ueber die Rohdateien:
    # so meldet --check nur dann „veraltet", wenn sich am Fliesstext etwas
    # geaendert hat — nicht bei jeder Aenderung an Skripten oder Aufgaben.
    fingerprint = hashlib.sha1(
        repr([(s['url'], s['nr'], s['titel']) for s in seiten]).encode('utf-8') +
        repr([(e['p'], e['a'], e['t'], e['x']) for e in eintraege]).encode('utf-8')
    ).hexdigest()[:16]

    zeilen = []
    zeilen.append('// ─────────────────────────────────────────────────────────────')
    zeilen.append('//  TALS Physik — Suchindex  (GENERIERT, nicht von Hand aendern)')
    zeilen.append('//  Neu bauen:  python3 scripts/build-suchindex.py')
    zeilen.append('// ─────────────────────────────────────────────────────────────')
    zeilen.append('window.SUCHINDEX = {')
    zeilen.append(f'  fp: "{fingerprint}",')
    zeilen.append('  seiten: [')
    for s in seiten:
        zeilen.append('    {u:%s, nr:%s, t:%s},' % (js_string(s['url']), js_string(s['nr']), js_string(s['titel'])))
    zeilen.append('  ],')
    zeilen.append('  eintraege: [')
    for e in eintraege:
        zeilen.append('    {p:%d, a:%s, t:%s, x:%s},' % (e['p'], js_string(e['a']), js_string(e['t']), js_string(e['x'])))
    zeilen.append('  ]')
    zeilen.append('};')
    return '\n'.join(zeilen) + '\n', fingerprint, len(eintraege)


def aktuelle_fp():
    if not os.path.exists(OUT):
        return None
    m = re.search(r'fp:\s*"([0-9a-f]+)"', open(OUT, encoding='utf-8').read())
    return m.group(1) if m else None


def main(argv):
    check = '--check' in argv
    inhalt, fp, n = build()
    if check:
        alt = aktuelle_fp()
        if alt == fp:
            print(f"Suchindex aktuell ({n} Abschnitte).")
            return 0
        print("Suchindex VERALTET — neu bauen mit: python3 scripts/build-suchindex.py")
        return 1
    open(OUT, 'w', encoding='utf-8').write(inhalt)
    kb = len(inhalt.encode('utf-8')) / 1024
    print(f"\nsuchindex.js geschrieben: {n} Abschnitte, {kb:.0f} KB (fp {fp})")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
