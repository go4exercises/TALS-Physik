"""Prüft, dass die Zufallsübungen des Leitprogramms Wärme keine feste Aufgabe nachbauen.

  python3 scripts/lp/waerme/pruef_fest.py [N [MIND]]   (N Aufgaben je Übung, Standard 1500; MIND Standard 2)

Erzeugt je Übung N Aufgaben im echten Browser (Testhaken box.__aufgabe, wie .claude/tools/
pruef-uebungen.mjs) und vergleicht die Zahlen jeder Aufgabe mit den festen Beispielen:
Clip-Szenen und Clip-Fragen (clips/p5-2-lp-*.json), Aufgaben und Leisten des Leitprogramms
(leitprogramme/leitprogramm-waerme.html, Abschnitte ab «a-frage» bzw. Leistenzeilen in seite.js),
Gesamttest (downloads/leitprogramme/waerme/gesamttest.tex) und Blöcke der Themenseite 5.2.
Dazu ein Selbsttest der Fallunterscheidungen (FAELLE): Jede genannte Übung muss jeden ihrer Fälle
erzeugen (eiswuerfel: «alles Eis schmilzt» und «Eis bleibt übrig»), sonst Exit 1. Ebenso ein Rundungstest:
In «eiswuerfel» und «abstrahlung» (rückwärts) müssen gerundete Eingaben (0.1 °C, ganze Kelvin, dreistellige
Zwischenwerte) angenommen und die Fehlerwerte aus fehler() weiter abgewiesen werden.
Treffer: alle Zahlen einer Aufgabe (mindestens MIND = 2 verschiedene, ohne Stoffkonstanten und Exponenten)
stehen in einem einzigen Satz eines festen Beispiels, und dieser Satz hat höchstens eine Zahl mehr. Exit 1 bei Treffern. Liest nur.
"""
import glob
import json
import os
import re
import subprocess
import sys

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
MIND = int(sys.argv[2]) if len(sys.argv) > 2 else 2   # Zahlen je Aufgabe, ab denen verglichen wird
# Stoffwerte und Umrechnungen, die in fast jeder Aufgabe stehen: zählen nicht als Merkmal
KONST = {4182, 2100, 334, 2256, 334000, 2256000, 896, 450, 2430, 2000, 835, 3.6, 5.67, 42.6, 46.4, 0.84, 1000, 0}
# Von Hand gesichtete Zufallstreffer (gleiche Zahlen, andere Sache) — werden gemeldet, aber nicht gezählt
GESICHTET = {
    ('abschnitte', 'seite.js Zeile 395 (Leiste)'),      # sim1 A2: 0.80 kg Wasser bekommen 25 kJ — kein Eis, keine −25 °C
    ('leitfaehigkeit', 'seite.js Zeile 501 (Leiste)'),  # sim2: 80 °C heisses Wasser, 0.60 kg — keine Wärmeleitfähigkeit
}
# Übung → Feld der Aufgabe, dessen Werte alle vorkommen müssen
FAELLE = {'eiswuerfel': 'ganz'}
ZAHL = re.compile(r'(?<![\w.])-?\d+(?:[  ]\d{3})*(?:\.\d+)?')


def zahlen(t):
    t = re.sub(r'<svg.*?</svg>', ' ', t, flags=re.S)
    t = re.sub(r'<svg.*', ' ', t, flags=re.S)
    t = re.sub(r'10\^\{-?\d+\}|\^\{?-?\d+\}?', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t).replace('\\;', ' ').replace('\\,', ' ').replace('−', '-')
    out = set()
    for z in ZAHL.findall(t):
        z = z.replace(' ', '').replace(' ', '')
        try:
            out.add(round(abs(float(z)), 6))
        except ValueError:
            pass
    return out


def texte(x):
    """alle Textfelder eines Drehbuch-Elements (ohne Koordinaten)"""
    if isinstance(x, dict):
        return [v for k, v in x.items() if k in ('text', 'beschriftung') and isinstance(v, str)] + [t for k, v in x.items() if k not in ('text', 'beschriftung') for t in texte(v)]
    if isinstance(x, list):
        return [t for v in x for t in texte(v)]
    return []


def feste():
    stuecke = []
    for p in sorted(glob.glob(os.path.join(R, 'clips', 'p5-2-lp-*.json'))):
        d = json.load(open(p))
        for s in d['szenen']:
            stuecke.append((os.path.basename(p) + ' · ' + s['name'], ' '.join(texte(s['elemente']))))
        for f in d.get('fragen', []):
            stuecke.append((os.path.basename(p) + ' · Frage', f['text'] + ' ' + ' '.join(f['optionen'])))
    html = open(os.path.join(R, 'leitprogramme', 'leitprogramm-waerme.html'), encoding='utf-8').read()
    for i, t in enumerate(html.split('class="a-frage')[1:]):
        stuecke.append(('Leitprogramm · Aufgabe %d' % (i + 1), t[:3000]))
    for i, z in enumerate(open(os.path.join(R, 'scripts', 'lp', 'waerme', 'seite.js'), encoding='utf-8')):
        if 'auftrag' in z or 'vergleich' in z or "{ text: '" in z:
            stuecke.append(('seite.js Zeile %d (Leiste)' % (i + 1), z))
    gt = os.path.join(R, 'downloads', 'leitprogramme', 'waerme', 'gesamttest.tex')
    if os.path.exists(gt):
        for i, t in enumerate(open(gt, encoding='utf-8').read().split('begin{lpaufgabe}')[1:]):
            stuecke.append(('Gesamttest · Aufgabe %d' % (i + 1), t))
    ts = open(os.path.join(R, 'themen', 'p5-2-waerme.html'), encoding='utf-8').read()
    for i, t in enumerate(re.split(r'class="(?:block|aufg-liste)', ts)[1:]):
        stuecke.append(('Themenseite · Block %d' % (i + 1), t[:4000]))
    # in Sätze bzw. Zeilen zerlegen: Eine Aufgabe ist nachgebaut, wenn ihre Zahlen in *einem* Satz stehen
    saetze = []
    for n, t in stuecke:
        t = re.sub(r'</(?:p|li|div|td|tr)>|<br\s*/?>|\\\\|\|', '\n', t)
        for satz in re.split(r'\n|(?<=[a-zäöü)])\.\s|[?!]\s', t):
            z = zahlen(satz) - KONST
            if len(z) >= 2:
                saetze.append((n, z))
    return saetze


JS = r'''
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { chromium } from 'playwright';
const W = process.argv[2];
const server = http.createServer((req, res) => {
  const p = path.join(W, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(W) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.css') ? 'text/css' : 'text/html' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const b = await chromium.launch(); const p = await b.newPage();
await p.route('**/vendor/mathjax/**', r => r.abort());
await p.goto(`http://localhost:${server.address().port}/leitprogramme/leitprogramm-waerme.html`);
await p.waitForTimeout(500);
const r = await p.evaluate((n) => {
  const aus = {};
  document.querySelectorAll('.uebung[data-typ]').forEach((box) => {
    const k = box.querySelector('.ue-neu'); const typ = box.dataset.typ; aus[typ] = []; aus['fall:' + typ] = {};
    for (let i = 0; i < n; i++) { k.click(); const A = box.__aufgabe; if (A) { aus[typ].push(A.text || '');
      for (const f of ['ganz']) if (f in A) aus['fall:' + typ][f + '=' + A[f]] = (aus['fall:' + typ][f + '=' + A[f]] || 0) + 1; } }
  });
  // Rundungstest: gerundete Eingaben angenommen, Fehlerwerte (fehler()) weiter abgewiesen
  const rund = {};
  const s3 = (x) => +(+x).toPrecision(3);
  for (const typ of ['eiswuerfel', 'abstrahlung']) {
    const box = document.querySelector('.uebung[data-typ="' + typ + '"]'); const k = box.querySelector('.ue-neu');
    const z = { faelle: 0, gerundet_abgewiesen: 0, fehler_angenommen: 0, beispiele: [] };
    for (let i = 0; i < n; i++) {
      k.click(); const A = box.__aufgabe, T = box.__typ; const feld = T.felder[0];
      const eingaben = [];
      if (typ === 'eiswuerfel') {
        eingaben.push(+A.t.toFixed(1));
        if (A.ganz) eingaben.push((s3(A.qmax) - s3(A.qs)) / s3((A.mg + A.me) * 4182));
      } else if (A.art === 'r') {
        eingaben.push(+A.x.toFixed(1), Math.round(A.T) - 273.15, Math.round(A.T) - 273);
      } else continue;
      for (const w of eingaben) {
        z.faelle++;
        const m = T.pruefen(A, { [feld]: w });
        if (m !== null) { z.gerundet_abgewiesen++; if (z.beispiele.length < 5) z.beispiele.push([A[feld], w, m.slice(0, 60)]); }
      }
      for (const [f] of T.fehler(A)) { if (T.pruefen(A, Object.fromEntries(Object.entries(f).map(([a, b]) => [a, +b]))) === null) z.fehler_angenommen++; }
    }
    rund[typ] = z;
  }
  aus['rund:'] = rund;
  return aus;
}, +process.argv[3]);
console.log(JSON.stringify(r)); await b.close(); server.close();
'''


def main():
    # Playwright aus dem Repo laden: das Hilfsskript liegt kurz neben diesem, nicht in /tmp
    pfad = os.path.join(R, 'scripts', 'lp', 'waerme', '_pruef_fest_tmp.mjs')
    with open(pfad, 'w') as f:
        f.write(JS)
    try:
        out = subprocess.run(['node', pfad, R, str(N)],
                             capture_output=True, text=True, cwd=R)
    finally:
        os.remove(pfad)
    if out.returncode:
        print(out.stderr)
        sys.exit(2)
    gen = json.loads(out.stdout)
    fest = feste()
    treffer = 0
    for typ, feld in FAELLE.items():
        zaehl = gen.get('fall:' + typ, {})
        for wert in ('true', 'false'):
            k = '%s=%s' % (feld, wert)
            print('Fall %-12s %-11s %5d' % (typ, k, zaehl.get(k, 0)))
            if not zaehl.get(k):
                treffer += 1
                print('FALL FEHLT  %s: %s kommt nie vor' % (typ, k))
    for typ, z in gen.pop('rund:', {}).items():
        print('Rundung %-12s %5d gerundete Eingaben, abgewiesen %d; Fehlerwerte angenommen %d' % (typ, z['faelle'], z['gerundet_abgewiesen'], z['fehler_angenommen']))
        for b in z['beispiele']:
            print('   abgewiesen:', b)
        if z['gerundet_abgewiesen'] or z['fehler_angenommen']:
            treffer += 1
    gen = {k: v for k, v in gen.items() if not k.startswith('fall:')}
    for typ, texte in gen.items():
        gesehen = set()
        for t in texte:
            z = frozenset(zahlen(t) - KONST)
            if len(z) < MIND or z in gesehen:
                continue
            gesehen.add(z)
            for name, f in fest:
                if z <= f and len(f - z) <= 1:
                    if (typ, name) in GESICHTET:
                        print('gesichtet %-12s %s  in  %s' % (typ, sorted(z), name))
                        break
                    treffer += 1
                    print('TREFFER %-14s %s  in  %s\n        %s' % (typ, sorted(z), name, re.sub(r'<[^>]+>', '', t)[:160]))
                    break
        print('%-14s %5d Aufgaben, %5d verschiedene Zahlensätze geprüft' % (typ, len(texte), len(gesehen)))
    print('%d feste Beispiele;' % len(fest), 'KEINE TREFFER' if not treffer else '%d TREFFER' % treffer)
    sys.exit(1 if treffer else 0)


main()
