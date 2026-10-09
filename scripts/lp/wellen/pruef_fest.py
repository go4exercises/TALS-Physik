"""Prüft, dass die Zufallsübungen des Leitprogramms Wellen keine feste Aufgabe nachbauen.

  python3 scripts/lp/wellen/pruef_fest.py [N [MIND]]   (N Aufgaben je Übung, Standard 1500; MIND Standard 2)

Erzeugt je Übung N Aufgaben im echten Browser (Testhaken box.__aufgabe, wie .claude/tools/
pruef-uebungen.mjs) und vergleicht die Zahlen jeder Aufgabe mit den festen Beispielen:
Clip-Szenen und Clip-Fragen (clips/p6-1-lp-*.json), Aufgaben und Leisten des Leitprogramms
(leitprogramme/leitprogramm-wellen.html, Abschnitte ab «a-frage» bzw. Leistenzeilen in seite.js),
Gesamttest (downloads/leitprogramme/wellen/gesamttest.tex) und Blöcke der Themenseite 6.1 und der Vertiefung 6.1a.
Die Fall- und Rundungstests der Fassung Wärme entfallen: Die Übungen hier haben keine Fallunterscheidung
im Generator, und das Annehmen gerundeter Eingaben prüft .claude/tools/pruef-uebungen.mjs.
Dazu (R4-P2): jede Teilaufgabe des Gesamttests gegen alle übrigen festen Stücke, Wert mit Einheit.
Treffer: alle Zahlen einer Aufgabe (mindestens MIND = 2 verschiedene, ohne Konstanten und Exponenten)
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
KONST = {340, 1500, 980, 5170, 6300, 343, 346, 2.998, 380, 780, 0}   # Schall, Lichtgeschwindigkeit (2.998), sichtbar
# (vor der zweiten Prüfung standen hier auch 3, 20, 100 und 1000 — damit fielen Paare wie «2 m/s; 3 s» durch)   # Schall, c, sichtbar, Hörgrenzen, Umrechnungen
# Von Hand gesichtete Zufallstreffer (gleiche Zahlen, andere Sache) — werden gemeldet, aber nicht gezählt
GESICHTET = set()
# Übung → Feld der Aufgabe, dessen Werte alle vorkommen müssen
# Übung → (Feld der Aufgabe, Werte, die alle vorkommen müssen): Befund 4 der Prüfung — «wellengleichung» würfelte nie Luft
FAELLE = {'wellengleichung': ('med', ['Luft', 'Helium', 'Wasser', 'Eisen'])}
ZAHL = re.compile(r'(?<![\w.])-?\d+(?:[  ]\d{3})*(?:\.\d+)?')


def zahlen(t):
    t = re.sub(r'<svg.*?</svg>', ' ', t, flags=re.S)
    t = re.sub(r'<svg.*', ' ', t, flags=re.S)
    t = re.sub(r'3\.00?\s*(?:\\cdot|·)\s*10\^\{?8\}?', ' ', t)      # Lichtgeschwindigkeit
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


EINHEIT = re.compile(r'(\d+(?:\.\d+)?)\s*(?:\\[;,]|\s|\\text\{|\\mu\\text\{|\{)*\s*(km|m/s|mm|cm|nm|pm|µm|mu|kHz|MHz|GHz|Hz|ms|min|m|s)\b')


def werte_einheit(t):
    """Zahl mit Einheit (2.0 Hz, 450 nm): ein Einzelwert gilt nur als nachgebaut, wenn auch die Einheit stimmt"""
    t = re.sub(r'<[^>]+>', ' ', t).replace('\\mu\\text{m}', 'µm').replace('\\mu', 'µ')
    return {(round(float(a), 6), b) for a, b in EINHEIT.findall(t) if round(float(a), 6) not in KONST}


def texte(x):
    """alle Textfelder eines Drehbuch-Elements (ohne Koordinaten)"""
    if isinstance(x, dict):
        return [v for k, v in x.items() if k in ('text', 'beschriftung') and isinstance(v, str)] + [t for k, v in x.items() if k not in ('text', 'beschriftung') for t in texte(v)]
    if isinstance(x, list):
        return [t for v in x for t in texte(v)]
    return []


# Befund R4-P2 (vierte Prüfung): Der Gesamttest selbst darf keine Kapitelaufgabe, Vertiefung, Leistenaufgabe,
# Clip-Szene/-Frage oder Themenseiten-Aufgabe nachbauen. Verglichen wird je Teilaufgabe (Stamm, a, b, …) jeder Wert
# mit Einheit; schon ein gemeinsamer Wert wird gemeldet (Aufgabe 3d «Fledermaus 40 kHz» = alte G4 a).
# Von Hand gesichtet (gleiche Zahl, andere Sache): (Teilaufgabe, Wert)
TEST_GESICHTET = {
    ('G1 c', (20.0, 'm')),    # Rasterbreite 20 m; Aufgabe 4d: Kurzwelle 20 m
    ('G3 d', (2.0, 'Hz')),    # Feder 2.0 Hz mit 1.4 m; Kontrollfrage 2 und 6.1a: andere Wellen, andere Längen
}


def test_gegen_fest(stuecke):
    gt = os.path.join(R, 'downloads', 'leitprogramme', 'wellen', 'gesamttest.tex')
    if not os.path.exists(gt):
        return 0
    treffer = 0
    andere = [(n, werte_einheit(t)) for n, t in stuecke if not n.startswith('Gesamttest')]
    for i, t in enumerate(open(gt, encoding='utf-8').read().split('begin{lpaufgabe}')[1:]):
        for j, teil in enumerate(re.split(r'\\item', t.split('end{lpaufgabe}')[0])):
            name = 'G%d %s' % (i + 1, 'Stamm' if j == 0 else 'abcdefgh'[j - 1])
            w = werte_einheit(teil)
            for n, f in andere:
                for g in sorted(w & f):
                    if (name, g) in TEST_GESICHTET:
                        print('gesichtet TEST %-8s %s  in  %s' % (name, g, n))
                    else:
                        treffer += 1
                        print('TEST    %-8s %s  in  %s' % (name, g, n))
    return treffer


def feste():
    stuecke = []
    for p in sorted(glob.glob(os.path.join(R, 'clips', 'p6-1-lp-*.json'))):
        d = json.load(open(p))
        for s in d['szenen']:
            stuecke.append((os.path.basename(p) + ' · ' + s['name'], ' '.join(texte(s['elemente']))))
        for f in d.get('fragen', []):
            stuecke.append((os.path.basename(p) + ' · Frage', f['text'] + ' ' + ' '.join(f.get('optionen', []))))
    html = open(os.path.join(R, 'leitprogramme', 'leitprogramm-wellen.html'), encoding='utf-8').read()
    for i, t in enumerate(html.split('class="a-frage')[1:]):
        stuecke.append(('Leitprogramm · Aufgabe %d' % (i + 1), t[:3000]))
    for i, z in enumerate(open(os.path.join(R, 'scripts', 'lp', 'wellen', 'seite.js'), encoding='utf-8')):
        if 'auftrag' in z or 'vergleich' in z or "{ text: '" in z:
            stuecke.append(('seite.js Zeile %d (Leiste)' % (i + 1), z))
    gt = os.path.join(R, 'downloads', 'leitprogramme', 'wellen', 'gesamttest.tex')
    if os.path.exists(gt):
        for i, t in enumerate(open(gt, encoding='utf-8').read().split('begin{lpaufgabe}')[1:]):
            stuecke.append(('Gesamttest · Aufgabe %d' % (i + 1), t))
    for datei, name in (('p6-1-wellen.html', 'Themenseite 6.1'), ('p6-1a-wellenexperimente.html', 'Vertiefung 6.1a')):
        ts = open(os.path.join(R, 'themen', datei), encoding='utf-8').read()
        for i, t in enumerate(re.split(r'class="(?:block|aufg-liste)', ts)[1:]):
            stuecke.append(('%s · Block %d' % (name, i + 1), t[:4000]))
    FEST_STUECKE.extend(stuecke)
    # in Sätze bzw. Zeilen zerlegen: Eine Aufgabe ist nachgebaut, wenn ihre Zahlen in *einem* Satz stehen
    saetze = []
    for n, t in stuecke:
        t = re.sub(r'</(?:p|li|div|td|tr)>|<br\s*/?>|\\\\|\|', '\n', t)
        for satz in re.split(r'\n|(?<=[a-zäöü)])\.\s|[?!]\s', t):
            z = zahlen(satz) - KONST
            if len(z) >= 2:
                saetze.append((n, z))
            if 1 <= len(z) <= 2 and re.search(r'Gesamttest|Frage|Aufgabe', n):
                EINZEL.append((n, werte_einheit(satz)))
    return saetze


# Befund R2-10 (zweite Prüfung): Übungen mit nur einer Zahl je Aufgabe wurden nie verglichen. Diese Werte werden
# gegen kurze Sätze (höchstens zwei Zahlen) aus Gesamttest, Kontrollfragen und Kapitelaufgaben geprüft.
EINZEL = []
FEST_STUECKE = []   # alle festen Stücke, für den Vergleich des Gesamttests (R4-P2)
# Von Hand gesichtete Einzeltreffer (gleiche Zahl, andere Sache): (Übung, Zahl)
EINZEL_GESICHTET = {('wellengleichung', (2.5, 'm'))}   # Kontrollfrage 2/1: ein Wellenberg bei 2.5 m, keine Wellenlänge


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
await p.goto(`http://localhost:${server.address().port}/leitprogramme/leitprogramm-wellen.html`);
await p.waitForTimeout(500);
const r = await p.evaluate((n) => {
  const aus = {};
  document.querySelectorAll('.uebung[data-typ]').forEach((box) => {
    const k = box.querySelector('.ue-neu'); const typ = box.dataset.typ; aus[typ] = []; aus['fall:' + typ] = {};
    for (let i = 0; i < n; i++) { k.click(); const A = box.__aufgabe; if (A) { aus[typ].push(A.text || '');
      for (const f of ['med']) if (f in A) aus['fall:' + typ][f + '=' + A[f]] = (aus['fall:' + typ][f + '=' + A[f]] || 0) + 1; } }
  });
  return aus;
}, +process.argv[3]);
console.log(JSON.stringify(r)); await b.close(); server.close();
'''


def main():
    # Playwright aus dem Repo laden: das Hilfsskript liegt kurz neben diesem, nicht in /tmp
    pfad = os.path.join(R, 'scripts', 'lp', 'wellen', '_pruef_fest_tmp.mjs')
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
    for typ, (feld, werte) in FAELLE.items():
        zaehl = gen.get('fall:' + typ, {})
        for wert in werte:
            k = '%s=%s' % (feld, wert)
            print('Fall %-16s %-14s %5d' % (typ, k, zaehl.get(k, 0)))
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
    for typ, texte in gen.items():
        gesehen = set()
        for t in texte:
            z = frozenset(zahlen(t) - KONST)
            if len(z) != 1:
                continue
            we = frozenset(werte_einheit(t))
            if len(we) != 1 or we in gesehen:
                continue
            gesehen.add(we)
            for name, f in EINZEL:
                if we <= f:
                    w = next(iter(we))
                    if (typ, w) in EINZEL_GESICHTET:
                        break
                    treffer += 1
                    print('EINZEL  %-14s %s  in  %s\n        %s' % (typ, w, name, re.sub(r'<[^>]+>', '', t)[:160]))
                    break
        if gesehen:
            print('%-14s %5d Einzelwerte geprüft' % (typ, len(gesehen)))
    treffer += test_gegen_fest(FEST_STUECKE)
    print('%d feste Beispiele, %d kurze Sätze;' % (len(fest), len(EINZEL)), 'KEINE TREFFER' if not treffer else '%d TREFFER' % treffer)
    sys.exit(1 if treffer else 0)


main()
