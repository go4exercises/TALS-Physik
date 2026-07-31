#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  TALS Physik — Auffindbarkeit: Seiten-Metadaten, sitemap.xml, robots.txt
#
#  Schreibt in jede Seite einen generierten Kopfblock zwischen den Marken
#      <!-- SEO:ANFANG … -->  …  <!-- SEO:ENDE -->
#  (Beschreibung, canonical, Favicons, Open Graph, JSON-LD nach schema.org).
#  Der Block wird bei jedem Lauf ersetzt — von Hand aendert man ihn nie,
#  sondern die Tabelle SEITEN weiter unten.
#
#  Die JSON-LD-Daten folgen schema.org/LearningResource (LRMI). Die
#  RLP-Kompetenzen werden direkt aus der Seite gelesen (.rlp-kompetenzen li),
#  damit Metadaten und sichtbarer Inhalt nicht auseinanderlaufen.
#
#  Aufruf vom Repo-Root:
#      python3 scripts/build-seo.py            # schreiben
#      python3 scripts/build-seo.py --check    # nur pruefen (Exit 1 = veraltet)
# ─────────────────────────────────────────────────────────────

import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://go4exercises.github.io/TALS-Physik/'
AUTOR = 'Raphael Arnold Kohler'
LIZENZ = 'https://creativecommons.org/licenses/by-nc/4.0/deed.de'
STAND = '2026-08-01'

# ── Seiten-Tabelle: hier wird gepflegt ───────────────────────────────
# beschreibung: 140–165 Zeichen, eigenstaendig lesbar, mit den Suchbegriffen,
#               die jemand tatsaechlich eingibt.
# themen:       Stichworte fuer schema.org/about
SEITEN = {
 'index.html': dict(
   typ='website',
   titel='TALS Physik — interaktives Lehrmittel für die Berufsmaturität',
   beschreibung='Kostenloses interaktives Physik-Lehrmittel für die Berufsmaturität TALS nach RLP-BM 2030: Mechanik, Thermodynamik, Wellen und Elektrizität mit Animationen.',
   themen=['Physik', 'Berufsmaturität', 'RLP-BM 2030', 'Lehrmittel', 'Mechanik', 'Thermodynamik']),
 'glossar.html': dict(
   typ='article', lrt='Glossar',
   titel='Glossar — physikalische Begriffe von A bis Z',
   beschreibung='Physik-Glossar der Berufsmaturität: die zentralen Begriffe von Absolutem Nullpunkt bis Zentripetalbeschleunigung, kurz erklärt und mit Formel.',
   themen=['Physik', 'Glossar', 'Fachbegriffe']),
 'formelsammlung.html': dict(
   typ='article', lrt='Formelsammlung',
   titel='Formelsammlung Physik — alle Formeln nach Lerngebieten',
   beschreibung='Alle Physik-Formeln der Berufsmaturität auf einer Seite: Mechanik, Thermodynamik, Wellen und Elektrizität, geordnet nach den Lerngebieten des RLP-BM 2030.',
   themen=['Physik', 'Formelsammlung', 'Formeln', 'Berufsmaturität']),
 'rechtliches.html': dict(
   typ='website', noindex=False,
   titel='Rechtliches & Datenschutz',
   beschreibung='Verantwortlichkeit, Haftung, Lizenz und Datenschutz von TALS Physik — ohne Cookies, ohne Tracking.',
   themen=['Impressum', 'Datenschutz']),
 'feedback.html': dict(
   typ='website',
   titel='Kontakt & Feedback',
   beschreibung='Fehler melden, Verbesserungen vorschlagen oder Rückmeldung geben zu TALS Physik — ohne Anmeldung, Name und E-Mail freiwillig.',
   themen=['Kontakt', 'Feedback']),

 'themen/p0-0-vorwissen-kompakt.html': dict(
   beschreibung='Vorwissen Physik im Alltag: sieben Situationen vom Rucksack bis zum Wasserkocher zeigen, welche Werkzeuge aus der Sek I in der Berufsmaturität gebraucht werden.',
   themen=['Vorwissen', 'Alltagsphysik', 'Grössen', 'Einheiten']),
 'themen/p0-1-vorwissen-mathematik.html': dict(
   beschreibung='Rechnen und Schliessen für die Physik: Proportionalität, Formeln umstellen, Zehnerpotenzen, Runden und signifikante Stellen — mit interaktiven Übungen.',
   themen=['Proportionalität', 'Formel umstellen', 'Zehnerpotenzen', 'Signifikante Stellen', 'Dreisatz']),
 'themen/p0-2-vorwissen-physik.html': dict(
   beschreibung='Grössen, Einheiten und Messen: von der Grundgrösse zur SI-Einheit, Dichte, Kraft und Energie, Präfixe, Umrechnen und Abschätzen — mit Animationen.',
   themen=['SI-Einheiten', 'Grössen', 'Dichte', 'Einheitenpräfixe', 'Messen']),
 'themen/p4-1-kinematik.html': dict(
   beschreibung='Kinematik: Weg, Geschwindigkeit und Beschleunigung im v-t-Diagramm, gleichförmige und beschleunigte Bewegung, freier Fall, Wurf und Kreisbewegung.',
   themen=['Kinematik', 'Geschwindigkeit', 'Beschleunigung', 'v-t-Diagramm', 'Freier Fall', 'Kreisbewegung'],
   lg='Lerngebiet 4 Mechanik', tg='4.1 Kinematik des Schwerpunkts'),
 'themen/p4-2-dynamik.html': dict(
   beschreibung='Dynamik: die drei Newtonschen Gesetze, Kraft und Masse, Federkraft nach Hooke, Haft- und Gleitreibung sowie Kräfte an der schiefen Ebene.',
   themen=['Newtonsche Gesetze', 'Kraft', 'Reibung', 'Hookesches Gesetz', 'Schiefe Ebene'],
   lg='Lerngebiet 4 Mechanik', tg='4.2 Dynamik'),
 'themen/p4-3-energie.html': dict(
   beschreibung='Energie, Arbeit und Leistung: Energieformen, Energieerhaltung, Wirkungsgrad und der Zusammenhang W = F·s — mit interaktiven Diagrammen.',
   themen=['Energie', 'Arbeit', 'Leistung', 'Energieerhaltung', 'Wirkungsgrad'],
   lg='Lerngebiet 4 Mechanik', tg='4.3 Energie'),
 'themen/p4-4-statik.html': dict(
   beschreibung='Statik: Kräfteaddition und -zerlegung, Drehmoment und Hebelgesetz, Schwerpunkt und Auflagerkräfte — von der Wippe bis zum Kran.',
   themen=['Statik', 'Drehmoment', 'Hebelgesetz', 'Kräftezerlegung', 'Schwerpunkt'],
   lg='Lerngebiet 4 Mechanik', tg='4.4 Statik von Festkörpern'),
 'themen/p4-5-hydrostatik.html': dict(
   beschreibung='Hydrostatik: Schweredruck, Pascalsches Prinzip, hydraulische Presse und Auftrieb nach Archimedes — von der Tauchbrille bis zum Frachtschiff.',
   themen=['Hydrostatik', 'Druck', 'Auftrieb', 'Archimedisches Prinzip', 'Hydraulik'],
   lg='Lerngebiet 4 Mechanik', tg='4.5 Hydrostatik'),
 'themen/p5-1-temperatur.html': dict(
   beschreibung='Temperatur: was sie auf Teilchenebene misst, Celsius- und Kelvin-Skala, absoluter Nullpunkt, Aggregatzustände und das Gasgesetz.',
   themen=['Temperatur', 'Kelvin', 'Absoluter Nullpunkt', 'Teilchenmodell', 'Gasgesetz'],
   lg='Lerngebiet 5 Thermodynamik', tg='5.1 Temperatur'),
 'themen/p5-2-waerme.html': dict(
   beschreibung='Wärme als übertragene Energie: Wärmemenge Q = m·c·ΔT, spezifische Wärmekapazität, Mischungen, Phasenübergänge, Wärmetransport und Wirkungsgrad.',
   themen=['Wärme', 'Wärmemenge', 'Wärmekapazität', 'Phasenübergang', 'Wärmetransport'],
   lg='Lerngebiet 5 Thermodynamik', tg='5.2 Wärme'),
 'themen/p5-3-waermeausdehnung.html': dict(
   beschreibung='Wärmeausdehnung von Festkörpern, Flüssigkeiten und Gasen: Längen- und Volumenausdehnung, Anomalie des Wassers und die Dehnungsfuge im Bauwesen.',
   themen=['Wärmeausdehnung', 'Längenausdehnung', 'Volumenausdehnung', 'Anomalie des Wassers'],
   lg='Lerngebiet 5 Thermodynamik', tg='5.3 Wärmeausdehnung'),
 'themen/p6-1-wellen.html': dict(
   beschreibung='Wellen: von der Schwingung zur Welle, Wellenlänge, Frequenz und c = λ·f, Schall, stehende Wellen und das elektromagnetische Spektrum.',
   themen=['Wellen', 'Schwingung', 'Wellenlänge', 'Frequenz', 'Schall', 'Elektromagnetisches Spektrum'],
   lg='Lerngebiet 6 Einführung in andere Bereiche der Physik', tg='6.1 Wellen'),
 'themen/p6-1a-wellenexperimente.html': dict(
   beschreibung='Sieben Wellenexperimente am Seil und an der Feder: Transversal- und Longitudinalwellen, Reflexion, Überlagerung und stehende Wellen zum Selbstprobieren.',
   themen=['Wellenexperimente', 'Transversalwelle', 'Longitudinalwelle', 'Reflexion', 'Stehende Welle'],
   lg='Lerngebiet 6 Einführung in andere Bereiche der Physik', tg='6.1a Wellenexperimente'),
 'themen/p6-2-elektrizitaet.html': dict(
   beschreibung='Elektrizität: Ladung, Strom, Spannung und Widerstand, Ohmsches Gesetz, Reihen- und Parallelschaltung, elektrische Leistung und Stromgefahren.',
   themen=['Elektrizität', 'Ohmsches Gesetz', 'Stromstärke', 'Spannung', 'Widerstand', 'Reihenschaltung', 'Parallelschaltung'],
   lg='Lerngebiet 6 Einführung in andere Bereiche der Physik', tg='6.2 Elektrizität'),
}

MARKE_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
MARKE_ZU = '<!-- SEO:ENDE -->'


MAKROS = {'cdot': '·', 'Delta': 'Δ', 'delta': 'δ', 'lambda': 'λ', 'alpha': 'α',
          'beta': 'β', 'gamma': 'γ', 'rho': 'ρ', 'omega': 'ω', 'pi': 'π', 'mu': 'µ',
          'circ': '°', 'approx': '≈', 'cdots': '…', 'times': '×', 'frac': '/',
          'vec': '', 'text': '', 'mathrm': '', 'left': '', 'right': '', 'quad': ' '}


def tex_weg(t):
    """LaTeX aus Fliesstext in lesbaren Klartext ueberfuehren."""
    def innen(m):
        x = m.group(1)
        x = re.sub(r'\\([a-zA-Z]+)', lambda k: MAKROS.get(k.group(1), ' '), x)
        return re.sub(r'[\\{}$^_]', '', x)
    t = re.sub(r'\\\((.*?)\\\)', innen, t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


def kompetenzen(seite_html):
    # bis zum Ende der Liste lesen — das erste </div> schliesst nur .rlp-titel
    m = re.search(r'<div class="rlp-kompetenzen">(.*?)</ul>', seite_html, re.S)
    if not m:
        return []
    return [tex_weg(li) for li in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)]


def titel_von(seite_html):
    m = re.search(r'<title>(.*?)</title>', seite_html, re.S)
    return html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip() if m else ''


def git_datum(pfad):
    try:
        d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', pfad],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return d or STAND
    except Exception:
        return STAND


def jsonld(url, cfg, titel, komp, ist_thema):
    person = {'@type': 'Person', 'name': AUTOR}
    knoten = {
        '@type': ['LearningResource', 'WebPage'] if ist_thema else 'WebPage',
        '@id': url + '#inhalt',
        'url': url,
        'name': titel,
        'description': cfg['beschreibung'],
        'inLanguage': 'de-CH',
        'isAccessibleForFree': True,
        'license': LIZENZ,
        'creator': person,
        'publisher': person,
        'dateModified': cfg['datum'],
        'isPartOf': {'@id': BASIS + '#website'},
    }
    if cfg.get('themen'):
        knoten['about'] = [{'@type': 'DefinedTerm', 'name': t} for t in cfg['themen']]
        knoten['keywords'] = ', '.join(cfg['themen'])
    if ist_thema or cfg.get('lrt'):
        knoten['learningResourceType'] = cfg.get('lrt', ['Lerneinheit', 'interaktive Simulation', 'Aufgabensammlung'])
        knoten['educationalLevel'] = 'Sekundarstufe II — Berufsmaturität (Schweiz)'
        knoten['typicalAgeRange'] = '16-20'
        knoten['audience'] = {'@type': 'EducationalAudience',
                              'educationalRole': ['student', 'teacher']}
        knoten['interactivityType'] = 'active'
    if komp:
        knoten['teaches'] = komp
    if cfg.get('tg'):
        knoten['educationalAlignment'] = [{
            '@type': 'AlignmentObject',
            'alignmentType': 'teaches',
            'educationalFramework': 'Rahmenlehrplan für die Berufsmaturität RLP-BM 2030, Gruppe Technik, Architektur, Life Sciences',
            'targetName': f"{cfg['lg']} · {cfg['tg']}",
        }]
    graph = [knoten]

    if cfg['datei'] == 'index.html':
        graph.append({
            '@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS,
            'name': 'TALS Physik', 'inLanguage': 'de-CH', 'license': LIZENZ,
            'publisher': person,
            'potentialAction': {
                '@type': 'SearchAction',
                'target': {'@type': 'EntryPoint', 'urlTemplate': BASIS + '?q={search_term_string}'},
                'query-input': 'required name=search_term_string',
            },
        })
    else:
        graph.append({'@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS, 'name': 'TALS Physik'})

    if ist_thema:
        graph.append({
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'TALS Physik', 'item': BASIS},
                {'@type': 'ListItem', 'position': 2, 'name': cfg['lg'] if cfg.get('lg') else 'Vorwissen'},
                {'@type': 'ListItem', 'position': 3, 'name': cfg.get('tg', titel), 'item': url},
            ],
        })
    return {'@context': 'https://schema.org', '@graph': graph}


def block(datei, cfg, seite_html):
    tief = datei.count('/')
    auf = '../' * tief
    url = BASIS + datei
    titel = cfg.get('titel') or titel_von(seite_html)
    ist_thema = datei.startswith('themen/')
    komp = kompetenzen(seite_html) if ist_thema else []
    cfg = dict(cfg, datei=datei, datum=git_datum(datei))
    b = cfg['beschreibung']
    z = [MARKE_AUF,
         f'<meta name="description" content="{html.escape(b, quote=True)}">',
         f'<meta name="author" content="{AUTOR}">',
         f'<link rel="canonical" href="{url}">',
         f'<link rel="icon" href="{auf}favicon.svg" type="image/svg+xml">',
         f'<link rel="icon" href="{auf}favicon-32.png" sizes="32x32" type="image/png">',
         f'<link rel="apple-touch-icon" href="{auf}apple-touch-icon.png">',
         f'<meta property="og:type" content="{cfg.get("typ", "article")}">',
         '<meta property="og:site_name" content="TALS Physik">',
         '<meta property="og:locale" content="de_CH">',
         f'<meta property="og:title" content="{html.escape(titel, quote=True)}">',
         f'<meta property="og:description" content="{html.escape(b, quote=True)}">',
         f'<meta property="og:url" content="{url}">',
         f'<meta property="og:image" content="{BASIS}og-bild.png">',
         '<meta name="twitter:card" content="summary_large_image">',
         '<script type="application/ld+json">',
         json.dumps(jsonld(url, cfg, titel, komp, ist_thema), ensure_ascii=False, indent=1),
         '</script>',
         MARKE_ZU]
    return '\n'.join(z)


def einsetzen(datei, cfg):
    pfad = os.path.join(ROOT, datei)
    s = open(pfad, encoding='utf-8').read()
    neu = block(datei, cfg, s)
    if MARKE_AUF in s:
        s2 = re.sub(re.escape(MARKE_AUF) + r'.*?' + re.escape(MARKE_ZU), lambda _: neu, s, flags=re.S)
    else:
        m = re.search(r'</title>\n?', s)
        assert m, f'{datei}: kein <title>'
        s2 = s[:m.end()] + neu + '\n' + s[m.end():]
    geaendert = s2 != s
    return s2, geaendert


def sitemap():
    eintraege = []
    for datei in SEITEN:
        if SEITEN[datei].get('noindex'):
            continue
        eintraege.append((BASIS + datei, git_datum(datei),
                          '1.0' if datei == 'index.html' else
                          '0.8' if datei.startswith('themen/') else '0.5'))
    eintraege.append((BASIS + 'TALS-Physik-Formelsammlung.pdf', git_datum('TALS-Physik-Formelsammlung.pdf'), '0.6'))
    z = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, datum, prio in eintraege:
        z += ['  <url>', f'    <loc>{url}</loc>', f'    <lastmod>{datum}</lastmod>',
              f'    <priority>{prio}</priority>', '  </url>']
    z.append('</urlset>')
    return '\n'.join(z) + '\n'


ROBOTS = f"""# TALS Physik — alles darf indexiert werden.
User-agent: *
Allow: /

Sitemap: {BASIS}sitemap.xml
"""


def main(argv):
    pruefen = '--check' in argv
    offen = []
    for datei, cfg in SEITEN.items():
        s2, geaendert = einsetzen(datei, cfg)
        if geaendert:
            offen.append(datei)
            if not pruefen:
                open(os.path.join(ROOT, datei), 'w', encoding='utf-8').write(s2)
    for name, inhalt in (('sitemap.xml', sitemap()), ('robots.txt', ROBOTS)):
        p = os.path.join(ROOT, name)
        alt = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        if alt != inhalt:
            offen.append(name)
            if not pruefen:
                open(p, 'w', encoding='utf-8').write(inhalt)
    if pruefen:
        if offen:
            print('SEO-Metadaten VERALTET:', ', '.join(offen))
            return 1
        print(f'SEO-Metadaten aktuell ({len(SEITEN)} Seiten).')
        return 0
    print(f'{len(SEITEN)} Seiten mit Metadaten versehen, sitemap.xml und robots.txt geschrieben.')
    if offen:
        print('  geändert:', ', '.join(offen))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
