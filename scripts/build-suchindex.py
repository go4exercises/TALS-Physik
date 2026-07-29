#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  TALS — Suchindex-Generator (Physik und Mathe, eine Implementierung)
#
#  Liest die Themen-/Kapitelseiten, das Glossar und die Formelsammlung,
#  schneidet den *Fliesstext* an den <h2 id="…">-Ankern in Abschnitte und
#  schreibt daraus  suchindex.js  (window.SUCHINDEX = {…}).
#
#  Die Seitenliste kommt aus `nav.js` (Block `const SITE = {…}`) — egal ob
#  das Projekt eine Liste fuehrt (Physik: `themen`) oder mehrere
#  (Mathe: `grundlagen` + `schwerpunkt`). Das Projekt wird an der
#  Canvas-Bibliothek erkannt (physiklib.js / mathlib.js); daran haengen nur
#  die projekteigenen Skip-Klassen, alles Uebrige ist gemeinsam.
#
#  Ausgabe bewusst als .js und nicht als .json: so funktioniert die Suche
#  auch, wenn eine Seite lokal per file:// geoeffnet wird (fetch() auf JSON
#  scheitert dort an CORS).
#
#  Aufruf (immer vom Repo-Root):
#      python3 scripts/build-suchindex.py              # neu bauen
#      python3 scripts/build-suchindex.py --check      # nur pruefen, ob aktuell
#                                                      # Exit 1 = veraltet
#      python3 scripts/build-suchindex.py --dry-run    # bauen, nur berichten
#      python3 scripts/build-suchindex.py --root PFAD  # anderes Repo (schreibt
#                                                      # dorthin — mit --dry-run
#                                                      # gefahrlos pruefbar)
#
#  Was NICHT in den Index kommt (Entscheid: nur Fliesstext):
#    - Mini-Checks (.minicheck) und Verstaendnisfragen (.frage)
#    - Aufgaben (Sektion #aufgaben, .block-aufg, .aufg-liste)
#    - Zusatzmaterial (#downloads) und externe Ressourcen (#ressourcen)
#    - Animationen: Bedienelemente und Live-Werte — in Physik .widget-body,
#      in Mathe .regler/.legende/.formel; Titel, Hinweis und (in Mathe) die
#      .erklaerung bleiben drin
#    - Bedienelemente aller Art (<button>, <select>, <input>), <canvas>
#    - Navigation, Footer, Scripts, Styles
# ─────────────────────────────────────────────────────────────

import hashlib
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Was uebersprungen wird ────────────────────────────────────
SKIP_TAGS = {'script', 'style', 'canvas', 'svg', 'noscript', 'template', 'head',
             'button', 'select'}
VOID_TAGS = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'col',
             'area', 'base', 'embed', 'param', 'track', 'wbr'}

# In beiden Projekten gleich
SKIP_CLASSES = {
    'minicheck', 'mc-item', 'mc-kopf',       # Mini-Checks
    'frage',                                 # Verstaendnisfragen ❓
    'block-aufg', 'aufg-liste', 'aufg',      # Aufgaben
    'loesung-toggle', 'loesung-body',        # Loesungen zu Aufgaben
    'dl-grid', 'links-grid',                 # Kachel-/Linklisten
    'toc-wrap', 'site-footer', 'mobile-nav', 'site-hdr',
}
SKIP_IDS = {'nav-root', 'toc'}

# Ganze Abschnitte, die uebersprungen werden (h2-Anker) — in beiden Projekten
# heissen sie gleich.
SKIP_SECTIONS = {'aufgaben', 'downloads', 'ressourcen'}

# ── Projekte ──────────────────────────────────────────────────
# Erkannt wird an der Canvas-Bibliothek im Repo-Root. Nur die Klassen der
# Animations-Bedienung unterscheiden sich; wer ein Projekt umbaut, ergaenzt
# hier — nicht im Parser.
PROJEKTE = [
    {'name': 'TALS Physik', 'kennung': 'physiklib.js',
     # .widget-body umfasst Regler, Live-Boxen und Canvas; Titel und
     # „Worauf achten?"-Hinweis stehen im .widget-header und bleiben drin.
     'skip_classes': {'widget-body'}},
    {'name': 'TALS Mathe', 'kennung': 'mathlib.js',
     # Mathe hat kein .widget-body: die Bedienung liegt in .bedien, wo neben
     # Reglern und Legenden auch die .erklaerung steht — darum die Kinder
     # einzeln ausschliessen und .bedien selbst behalten.
     'skip_classes': {'regler', 'regler-label', 'legende', 'legende-zeile',
                      'legende-titel', 'formel', 'wert', 'val', 'lab',
                      'eingabe-row', 'btn-pruef', 'cr'}},
]


def projekt_erkennen(root):
    for p in PROJEKTE:
        if os.path.exists(os.path.join(root, p['kennung'])):
            return p
    raise SystemExit('[FEHLER] Kein bekanntes TALS-Repo: weder ' +
                     ' noch '.join(p['kennung'] for p in PROJEKTE) +
                     f' in {root} gefunden.')

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

    def __init__(self, mode='thema', skip_classes=SKIP_CLASSES):
        super().__init__(convert_charrefs=True)
        self.mode = mode            # 'thema' | 'glossar' | 'formeln'
        self.skip_classes = skip_classes
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

        if (tag in SKIP_TAGS or eid in SKIP_IDS or (cls & self.skip_classes)):
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
def _site_block(src):
    """Der `const SITE = { … }`-Block, ueber die Klammerbilanz abgegrenzt."""
    i = src.index('const SITE')
    j = src.index('{', i)
    tiefe = 0
    for k in range(j, len(src)):
        if src[k] == '{':
            tiefe += 1
        elif src[k] == '}':
            tiefe -= 1
            if tiefe == 0:
                return src[j:k + 1]
    raise SystemExit('[FEHLER] nav.js: const SITE ist nicht sauber geklammert.')


def seiten_aus_navjs(root):
    """Alle Seiteneintraege in Quelltext-Reihenfolge.

    Physik fuehrt eine Liste (`themen`), Mathe zwei (`grundlagen`,
    `schwerpunkt`). Beides faellt hier zusammen — entscheidend ist nur die
    Reihenfolge, in der die Eintraege in nav.js stehen.
    """
    src = open(os.path.join(root, 'nav.js'), encoding='utf-8').read()
    block = _site_block(src)
    seiten, gesehen = [], set()
    for m in re.finditer(r"nr:\s*'([^']+)'\s*,\s*titel:\s*'([^']+)'\s*,\s*url:\s*'([^']+)'", block):
        url = m.group(3)
        if url in gesehen:
            continue
        gesehen.add(url)
        seiten.append({'nr': m.group(1), 'titel': m.group(2), 'url': url, 'mode': 'thema'})
    if not seiten:
        raise SystemExit('[FEHLER] nav.js: keine Seiteneintraege im SITE-Block gefunden.')

    # Nachschlagewerke, sofern vorhanden (beide Projekte haben sie im Root)
    for url, nr, titel, mode in [('glossar.html', 'A–Z', 'Glossar', 'glossar'),
                                 ('formelsammlung.html', '∑', 'Formelsammlung', 'formeln')]:
        if os.path.exists(os.path.join(root, url)):
            seiten.append({'nr': nr, 'titel': titel, 'url': url, 'mode': mode})
    return seiten


def js_string(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def build(root, projekt):
    seiten = seiten_aus_navjs(root)
    skip_classes = SKIP_CLASSES | projekt['skip_classes']
    eintraege = []

    for pi, s in enumerate(seiten):
        pfad = os.path.join(root, s['url'])
        if not os.path.exists(pfad):
            print(f"[WARN] fehlt: {s['url']}", file=sys.stderr)
            continue
        roh = open(pfad, encoding='utf-8').read()
        ex = Extractor(mode=s['mode'], skip_classes=skip_classes)
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
    zeilen.append(f"//  {projekt['name']} — Suchindex  (GENERIERT, nicht von Hand aendern)")
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


def aktuelle_fp(out):
    if not os.path.exists(out):
        return None
    m = re.search(r'fp:\s*"([0-9a-f]+)"', open(out, encoding='utf-8').read())
    return m.group(1) if m else None


def main(argv):
    check = '--check' in argv
    dry = '--dry-run' in argv
    root = ROOT
    if '--root' in argv:
        root = os.path.abspath(argv[argv.index('--root') + 1])

    projekt = projekt_erkennen(root)
    out = os.path.join(root, 'suchindex.js')
    print(f"Projekt: {projekt['name']}  ({root})")

    inhalt, fp, n = build(root, projekt)
    kb = len(inhalt.encode('utf-8')) / 1024

    if check:
        if aktuelle_fp(out) == fp:
            print(f"Suchindex aktuell ({n} Abschnitte).")
            return 0
        print("Suchindex VERALTET — neu bauen mit: python3 scripts/build-suchindex.py")
        return 1
    if dry:
        print(f"\n[Trockenlauf] nichts geschrieben: {n} Abschnitte, {kb:.0f} KB (fp {fp})")
        return 0
    open(out, 'w', encoding='utf-8').write(inhalt)
    print(f"\nsuchindex.js geschrieben: {n} Abschnitte, {kb:.0f} KB (fp {fp})")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
