#!/usr/bin/env python3
# Generiert die reduzierten Stub-Themenseiten (analog Mathe-Schwerpunktfach).
# Nur fehlende Seiten werden geschrieben; p4-1 und p4-5 (fertig) bleiben unangetastet.

import os

THEMEN_DIR = os.path.join(os.path.dirname(__file__), '..', 'themen')

# Vollständige Kette in RLP-Reihenfolge (für prev/next-Verkettung)
KETTE = [
    ('p4-1', '4.1', 'Kinematik des Schwerpunkts', 'p4-1-kinematik.html'),
    ('p4-2', '4.2', 'Dynamik',                     'p4-2-dynamik.html'),
    ('p4-3', '4.3', 'Energie',                      'p4-3-energie.html'),
    ('p4-4', '4.4', 'Statik von Festkörpern',       'p4-4-statik.html'),
    ('p4-5', '4.5', 'Hydrostatik',                  'p4-5-hydrostatik.html'),
    ('p5-1', '5.1', 'Temperatur',                   'p5-1-temperatur.html'),
    ('p5-2', '5.2', 'Wärme',                        'p5-2-waerme.html'),
    ('p5-3', '5.3', 'Wärmeausdehnung',              'p5-3-waermeausdehnung.html'),
    ('p6-1', '6.1', 'Wellen',                       'p6-1-wellen.html'),
    ('p6-2', '6.2', 'Elektrizität',                 'p6-2-elektrizitaet.html'),
]

# Lerngebiet-Zuordnung für den pt-bereich-Header
LERNGEBIET = {
    '4': 'Lerngebiet 4 Mechanik',
    '5': 'Lerngebiet 5 Thermodynamik',
    '6': 'Lerngebiet 6 Einführung in andere Bereiche der Physik',
}
LEKTIONEN = {'4': 100, '5': 30, '6': 30}

# Themen-spezifische Daten: Untertitel, lead, RLP-Kompetenzen (aus BM-Skript / master-todoliste)
DATEN = {
    'p4-2': {
        'untertitel': 'Kräfte als Ursache von Bewegungsänderungen — die Newtonschen Gesetze.',
        'lead': 'Die Dynamik erklärt, warum sich Bewegungszustände ändern: Kräfte. Von der Trägheit über das Grundgesetz \\(F = m \\cdot a\\) bis zu Reibung und schiefer Ebene werden hier die Werkzeuge gelegt, mit denen sich Alltagsbewegungen quantitativ beschreiben lassen.',
        'rlp': [
            'die drei Newtonschen Gesetze (Trägheit, Grundgesetz, Wechselwirkung) formulieren und anwenden',
            'das Grundgesetz \\(F = m \\cdot a\\) auf konkrete Bewegungen anwenden',
            'die Federkraft mit dem Hookeschen Gesetz \\(F = D \\cdot s\\) berechnen',
            'Haft- und Gleitreibung unterscheiden und Reibungskräfte berechnen',
            'Kräfte an der schiefen Ebene zerlegen und Bewegungsgleichungen aufstellen',
        ],
    },
    'p4-3': {
        'untertitel': 'Arbeit, Leistung und der Erhaltungssatz der Energie.',
        'lead': 'Energie ist die zentrale Erhaltungsgrösse der Physik. Dieses Lerngebiet verbindet mechanische Arbeit, Leistung und die verschiedenen Energieformen zu einem mächtigen Werkzeug: dem Energieerhaltungssatz, mit dem sich viele Bewegungsprobleme ohne Kräftezerlegung lösen lassen.',
        'rlp': [
            'die mechanische Arbeit \\(W = F \\cdot s \\cdot \\cos\\alpha\\) berechnen',
            'die Leistung \\(P = W / t\\) bestimmen und in Watt angeben',
            'kinetische Energie \\(E_{\\text{kin}} = \\tfrac{1}{2} m v^2\\) und potentielle Energie \\(E_{\\text{pot}} = m g h\\) berechnen',
            'den Energieerhaltungssatz auf mechanische Vorgänge anwenden',
            'den Wirkungsgrad als Verhältnis von Nutz- zu Gesamtenergie bestimmen',
        ],
    },
    'p4-4': {
        'untertitel': 'Gleichgewicht von Kräften und Drehmomenten an starren Körpern.',
        'lead': 'Die Statik untersucht, unter welchen Bedingungen ein Körper in Ruhe bleibt. Kräftegleichgewicht, Drehmoment und Schwerpunkt sind die Grundbegriffe, mit denen Brücken, Kräne und Hebel berechnet werden.',
        'rlp': [
            'Kräfte grafisch und rechnerisch zur Resultierenden zusammensetzen',
            'die Gleichgewichtsbedingung für Kräfte am Punkt anwenden (Drei-Kräfte-Schluss)',
            'das Drehmoment \\(M = F \\cdot r\\) berechnen und das Hebelgesetz anwenden',
            'die Gleichgewichtsbedingung für Drehmomente aufstellen',
            'den Schwerpunkt einfacher Körper bestimmen und Standfestigkeit beurteilen',
        ],
    },
    'p5-1': {
        'untertitel': 'Temperatur, Temperaturskalen und ihre Messung.',
        'lead': 'Die Temperatur ist ein Mass für die mittlere Bewegungsenergie der Teilchen. Dieses Lerngebiet führt die Temperaturskalen (Celsius, Kelvin, Fahrenheit) ein und zeigt, wie Temperatur gemessen wird.',
        'rlp': [
            'die Temperatur als Zustandsgrösse beschreiben und ihre Bedeutung erläutern',
            'zwischen den Skalen Celsius, Kelvin und Fahrenheit umrechnen',
            'den absoluten Nullpunkt erläutern und die Kelvin-Skala begründen',
            'gängige Temperaturmessverfahren beschreiben',
        ],
    },
    'p5-2': {
        'untertitel': 'Wärme als Energieform — Wärmekapazität und Wärmeübertragung.',
        'lead': 'Wärme ist Energie, die aufgrund eines Temperaturunterschieds übertragen wird. Von der spezifischen Wärmekapazität über die drei Übertragungsmechanismen bis zu den Aggregatzustandsänderungen wird hier die kalorische Wärmelehre entwickelt.',
        'rlp': [
            'die Wärmemenge \\(Q = c \\cdot m \\cdot \\Delta T\\) berechnen',
            'die spezifische Wärmekapazität als Stoffeigenschaft erläutern',
            'die drei Arten der Wärmeübertragung (Leitung, Konvektion, Strahlung) unterscheiden',
            'Schmelz- und Verdampfungswärme bei Aggregatzustandsänderungen berücksichtigen',
            'die Mischungsregel (kalorimetrische Grundgleichung) anwenden',
        ],
    },
    'p5-3': {
        'untertitel': 'Längen- und Volumenausdehnung bei Erwärmung — und die Anomalie des Wassers.',
        'lead': 'Die meisten Stoffe dehnen sich bei Erwärmung aus. Dieses Lerngebiet behandelt die Längenausdehnung fester Körper, die Volumenausdehnung von Flüssigkeiten und Gasen sowie die für das Leben wichtige Anomalie des Wassers.',
        'rlp': [
            'die Längenausdehnung \\(\\Delta l = \\alpha \\cdot l_0 \\cdot \\Delta T\\) fester Körper berechnen',
            'die Volumenausdehnung von Flüssigkeiten und Gasen beschreiben',
            'die Anomalie des Wassers erläutern und ihre Bedeutung für Gewässer einordnen',
            'technische Konsequenzen der Wärmeausdehnung (Dehnungsfugen, Bimetall) beschreiben',
        ],
    },
    'p6-1': {
        'untertitel': 'Schwingungen und Wellen — von der Wellenlänge bis zum Schall.',
        'lead': 'Wellen transportieren Energie ohne Materietransport. Dieses Lerngebiet führt die Grundbegriffe periodischer Vorgänge ein (Frequenz, Wellenlänge, Amplitude), unterscheidet Transversal- und Longitudinalwellen und wendet sie auf den Schall an.',
        'rlp': [
            'die Grundgrössen einer Welle (Wellenlänge, Frequenz, Amplitude, Periode) definieren',
            'die Wellengleichung \\(c = \\lambda \\cdot f\\) anwenden',
            'Transversal- und Longitudinalwellen unterscheiden',
            'Schall als Longitudinalwelle beschreiben und Eigenschaften (Tonhöhe, Lautstärke) zuordnen',
        ],
    },
    'p6-2': {
        'untertitel': 'Elektrischer Strom, Spannung, Widerstand und die Grundschaltungen.',
        'lead': 'Die Elektrizitätslehre führt die Grundgrössen des elektrischen Stromkreises ein. Vom Ohmschen Gesetz über Reihen- und Parallelschaltung bis zur elektrischen Leistung werden die Werkzeuge gelegt, mit denen sich einfache Schaltungen berechnen lassen.',
        'rlp': [
            'Stromstärke, Spannung und Widerstand definieren und ihre SI-Einheiten einsetzen',
            'das Ohmsche Gesetz \\(U = R \\cdot I\\) anwenden',
            'Gesamtwiderstände in Reihen- und Parallelschaltung berechnen',
            'die elektrische Leistung \\(P = U \\cdot I\\) und Energie \\(E = P \\cdot t\\) bestimmen',
        ],
    },
}

STUB_IDS = ['p4-2', 'p4-3', 'p4-4', 'p5-1', 'p5-2', 'p5-3', 'p6-1', 'p6-2']

def nav_entry(idx):
    if idx < 0 or idx >= len(KETTE):
        return 'null'
    _id, nr, titel, url = KETTE[idx]
    return "{nr:'%s',titel:'%s',url:'%s'}" % (nr, titel.replace("'", "\\'"), url)

def build_stub(theme_id):
    pos = next(i for i, t in enumerate(KETTE) if t[0] == theme_id)
    _id, nr, titel, url = KETTE[pos]
    lg = nr.split('.')[0]
    bereich = LERNGEBIET[lg]
    lek = LEKTIONEN[lg]
    d = DATEN[theme_id]
    rlp_items = '\n'.join('    <li>%s</li>' % k for k in d['rlp'])
    prev = nav_entry(pos - 1)
    nxt = nav_entry(pos + 1)
    title_full = f'{nr} {titel}'

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_full} — TALS Physik</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">

<script>
MathJax = {{
  tex: {{ inlineMath:[['\\\\(','\\\\)']], displayMath:[['\\\\[','\\\\]']], packages:{{'[+]':['boldsymbol']}} }},
  svg: {{ fontCache:'global', scale:1.05 }},
  loader: {{ load:['[tex]/boldsymbol'] }},
  options: {{ skipHtmlTags:['script','noscript','style','textarea'] }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

<style>
/* Themen-spezifische Styles werden hier ergänzt, sobald das Kapitel ausgearbeitet ist. */
</style>
</head>
<body>
<div id="nav-root"></div>
<div class="page-wrap">
<main class="content">

<!-- ══ 1. TITEL + RLP-HEADER ══ -->
<div class="page-titel">
  <div class="pt-bereich">Physik · {bereich}</div>
  <h1 class="pt-h1">{title_full}</h1>
  <p class="pt-untertitel">{d['untertitel']}</p>
</div>

<!-- Stub-Banner: Seite ist noch in Vorbereitung -->
<div class="stub-banner">
  <strong>In Vorbereitung</strong>
  Diese Seite ist noch in Vorbereitung — Themenstruktur und RLP-Kompetenzen stehen, der ausgearbeitete Inhalt mit interaktiven Animationen, Aufgaben und Druckseiten folgt. Stand: Mai 2026.
</div>

<p class="lead">{d['lead']}</p>

<div class="rlp-kompetenzen">
  <div class="rlp-titel">📋 Kompetenzen nach RLP-BM 2030 · Lerngebiet {nr} · {lek} Lektionen (Lerngebiet {lg})</div>
  <ul>
{rlp_items}
  </ul>
</div>


<!-- ══ 2. EINSTIEG ══ -->
<h2 id="einstieg">Einstieg</h2>
<p><em>Wird mit einem konkreten Alltagsphänomen ausgearbeitet.</em></p>


<!-- ══ 3. GRUNDBEGRIFFE ══ -->
<h2 id="definition">Grundbegriffe</h2>
<p><em>Wird ausgearbeitet — pro zentralem Begriff ein Definitionsblock.</em></p>


<!-- ══ 4. ANIMATIONEN ══ -->
<h2 id="animationen">Interaktive Darstellung</h2>
<p><em>Wird ausgearbeitet — 5 bis 10 Canvas-Animationen zum Hauptphänomen und seinen Spezialfällen.</em></p>


<!-- ══ 5. THEORIE ══ -->
<h2 id="theorie">Theorie und Herleitung</h2>
<p><em>Wird ausgearbeitet.</em></p>


<!-- ══ 6. AUFGABEN ══ -->
<h2 id="aufgaben">Aufgaben</h2>
<p><em>Wird ausgearbeitet — A1 bis A6 mit zunehmender Selbstständigkeit (siehe Styleguide §5.5).</em></p>


<!-- ══ 7. ZUSAMMENFASSUNG ══ -->
<h2 id="zusammenfassung">Zusammenfassung</h2>
<p><em>Wird ausgearbeitet — kompakte Formeltabelle und Merksatz.</em></p>


<!-- ══ 8. ZUSATZMATERIAL ══ -->
<h2 id="downloads">Zusatzmaterial</h2>
<p><em>Wird ergänzt — Handout, Formelauszug, Teste-dich-selbst, Aufgabenserie und Anki-Deck.</em></p>


<!-- ══ 9. RESSOURCEN ══ -->
<h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>
<p><em>Wird ergänzt — dreispaltig: 🎬 Videos · 🧪 Simulationen · 📝 Aufgaben.</em></p>


</main>
<aside class="toc-wrap"><div id="toc"></div></aside>
</div>

<footer class="site-footer">
  <p><strong>TALS Physik</strong> — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences</p>
  <p>Physik · {title_full}</p>
</footer>

<script src="../nav.js"></script>
<script src="../physiklib.js"></script>
<script>
buildNav({{
  id:'{_id}',
  kapitelNr:'{nr}', kapitelTitel:'{titel.replace("'", "\\'")}',
  prev:{prev},
  next:{nxt}
}});
</script>
</body>
</html>
'''

written = []
for tid in STUB_IDS:
    path = os.path.join(THEMEN_DIR, dict((t[0], t[3]) for t in KETTE)[tid])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(build_stub(tid))
    written.append(os.path.basename(path))

print("Geschrieben:")
for w in written:
    print("  ", w)
