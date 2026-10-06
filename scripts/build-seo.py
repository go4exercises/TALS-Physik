#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  Physik begreifbar — Auffindbarkeit: Seiten-Metadaten, sitemap.xml, robots.txt
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
#      python3 scripts/build-seo.py             # schreiben
#      python3 scripts/build-seo.py --check     # Gatter: Exit 1, wenn veraltet
#      python3 scripts/build-seo.py --dry-run   # Trockenlauf: zeigt, was sich
#                                               # aendern wuerde; Exit immer 0
#      python3 scripts/build-seo.py --dry-run --diff   # dazu die Zeilen selbst
#
#  --check und --dry-run unterscheiden sich in der Absicht: --check ist das
#  Gatter fuer den Pre-Flight und interessiert sich nur fuer den Exit-Code,
#  --dry-run ist zum Hinschauen, bevor man 32 Dateien anfasst.
#
#  Unbekannte Schalter brechen ab, statt durchzufallen. Frueher schrieb ein
#  `--help` die Metadaten, weil nur auf '--check' in argv geprueft wurde.
#
#  Achtung, zwei Laeufe: dateModified und lastmod kommen aus dem Git-Datum der
#  jeweiligen Datei. Ein Commit, der eine Seite anfasst, macht damit deren
#  eigenen Block um eine Generation veraltet. Nach dem Commit also noch einmal
#  laufen lassen und die Datumsaenderung mitcommitten — danach ist es stabil.
# ─────────────────────────────────────────────────────────────

import argparse
import difflib
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://physik.begreifbar.ch/'
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
   titel='Physik begreifbar — interaktives Lehrmittel für die Berufsmaturität',
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
 'leitprogramme.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramme — Physik im eigenen Tempo erarbeiten',
   beschreibung='Selbstlerneinheiten der Physik-Berufsmaturität: Vortest, Erklärung, '
                'Beispiel und Selbstkontrolle nach jedem Schritt, am Schluss ein Kapiteltest. '
                'Zum Vertiefen, Nachholen und für den Fernunterricht.',
   themen=['Physik', 'Leitprogramm', 'Selbststudium', 'Berufsmaturität']),
 'leitprogramme/leitprogramm-rechnen.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Rechnen und Schliessen — Dreisatz, Umstellen, Zehnerpotenzen',
   beschreibung='Leitprogramm zum Rechnen in der Physik: Variablen und '
                'Konstanten, direkte und indirekte Proportionalität, der '
                'Dreisatz, Gleichungen umstellen, Zehnerpotenzen und die '
                'EE-Taste, Bedingungen und Fallunterscheidungen, Kreis und '
                'Bogenmass sowie die drei Plausibilitätsproben — in acht '
                'Schritten mit Erklärclip, Simulation, Vortest und Gesamttest '
                'zur Selbstkontrolle.',
   themen=['Proportionalität', 'Dreisatz', 'Gleichungen umstellen',
           'Zehnerpotenzen', 'Bogenmass', 'Kreiszahl', 'Plausibilität',
           'Grössenordnung', 'Einheitenprobe']),
 'leitprogramme/leitprogramm-heizen.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Heizen, Dämmen, Umwandeln — Wirkungsgrad, Heizwert, Wärmetransport',
   beschreibung='Leitprogramm zur Energienutzung: Energieerhaltung und '
                'Entwertung, Wirkungsgrad und Wirkungsgrade in Serie, '
                'Heizwert und Brennstoffmenge, Wärmepumpe und Leistungszahl, '
                'Energiequellen im Vergleich sowie Leitung, Konvektion und '
                'Strahlung samt Dämmung und Treibhauseffekt — in acht '
                'Schritten mit Erklärclip, Simulation, Vortest und Gesamttest '
                'zur Selbstkontrolle.',
   themen=['Wirkungsgrad', 'Heizwert', 'Wärmepumpe', 'Leistungszahl',
           'Energiequellen', 'Wärmeleitung', 'Konvektion', 'Wärmestrahlung',
           'Treibhauseffekt', 'Dämmung']),
 'leitprogramme/leitprogramm-experimente-waerme.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Wärme im Experiment — Einstieg und Wärmekapazität',
   beschreibung='Sieben einfache Schulversuche zur Wärmelehre, gerechnet und '
                'simuliert: warum sich Metall kälter anfühlt als Holz, warum '
                'der Eiswürfel auf Aluminium schneller schmilzt, wie die '
                'Büroklammer ohne Flamme warm wird, der Wasserkocher als '
                'Messgerät für den Wirkungsgrad, Wasser gegen Speiseöl bei '
                'gleicher Heizleistung, vier Metallzylinder gleicher Masse und '
                'der Wasserballon über der Kerze — mit Vortest, Erklärclips, '
                'Simulationen und Gesamttest.',
   themen=['Wärme', 'Temperatur', 'Innere Energie', 'Wärmestrom',
           'Spezifische Wärmekapazität', 'Wärmebilanz', 'Mischtemperatur',
           'Wirkungsgrad', 'Experiment', 'Wärmeeindringzahl']),
 'leitprogramme/leitprogramm-waermemenge.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Wärmemenge und Wärmebilanz — Temperatur, Wärme, Heizkurve',
   beschreibung='Leitprogramm zur Wärmelehre: Temperatur als Teilchenbewegung, '
                'Celsius und Kelvin, Wärme als übertragene Energie, die '
                'Wärmemenge Q = m · c · ΔT, Wärmebilanz und Mischtemperatur, '
                'latente Wärme beim Schmelzen und Verdampfen, die Heizkurve '
                'sowie Leistung, Wirkungsgrad und Heizwert — in acht Schritten '
                'mit Erklärclip, Simulation, Vortest und Gesamttest zur '
                'Selbstkontrolle.',
   themen=['Wärmemenge', 'Spezifische Wärmekapazität', 'Wärmebilanz',
           'Mischtemperatur', 'Latente Wärme', 'Heizkurve', 'Wirkungsgrad',
           'Heizwert', 'Temperatur', 'Kelvin']),
 'leitprogramme/leitprogramm-waermeausdehnung.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Wärmeausdehnung — Feststoffe und Flüssigkeiten',
   beschreibung='Leitprogramm zur Wärmeausdehnung: Längen-, Flächen- und '
                'Volumenausdehnung fester Körper, warum der Volumenkoeffizient '
                'rund dreimal so gross ist wie der Längenkoeffizient, die '
                'Volumenausdehnung von Flüssigkeiten, die scheinbare Ausdehnung '
                'im Gefäss, Dichte und Temperatur sowie die Anomalie des Wassers '
                '— in acht Schritten mit Erklärclip, Simulation, Vortest und '
                'Gesamttest zur Selbstkontrolle.',
   themen=['Wärmeausdehnung', 'Längenausdehnung', 'Volumenausdehnung',
           'Ausdehnungskoeffizient', 'Scheinbare Ausdehnung', 'Dichte',
           'Anomalie des Wassers', 'Bimetall']),
 'leitprogramme/leitprogramm-ideale-gase.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Ideale Gase — Gasgesetze selbst erarbeiten',
   beschreibung='Leitprogramm zu den idealen Gasen: Boyle-Mariotte, Amontons und Gay-Lussac '
                'in acht Schritten zur allgemeinen Gasgleichung, mit Normbedingungen, den '
                'Grenzen des Modells, Vortest und Kapiteltest zur Selbstkontrolle.',
   themen=['Ideale Gase', 'Gasgesetze', 'Allgemeine Gasgleichung', 'Boyle-Mariotte',
           'Gay-Lussac', 'Amontons', 'Thermodynamik']),
 'leitprogramme/leitprogramm-schaltungen.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Schaltungen berechnen — Reihe, parallel, gemischt',
   beschreibung='Leitprogramm zur Elektrizität: Knoten- und Maschenregel, Reihenschaltung, '
                'Spannungsteiler, Parallelschaltung mit der Kehrwertformel, gemischte '
                'Schaltungen von innen nach aussen und die Leistung einzelner Bauteile — '
                'in sechs Schritten mit Erklärclip, Simulation, Vortest und Kapiteltest.',
   themen=['Physik', 'Elektrizität', 'Reihenschaltung', 'Parallelschaltung',
           'Spannungsteiler', 'Leitprogramm']),
 'leitprogramme/leitprogramm-elektrizitaet.html': dict(
   # Freigeschaltet am 03.10.2026 (nach /lp-pruefung).
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Elektrizität — Ladung, Spannung, Widerstand, Schaltungen, Gefahren',
   beschreibung='Leitprogramm zur Elektrizität in fünf Kapiteln — Ladung und Stromstärke; '
                'Spannung, Leistung und Energie; Widerstand eines Leiters; Reihen- und '
                'Parallelschaltung; Gefahren und Schutzmassnahmen — mit Erklärclips, '
                'Simulationen mit Aufgaben, Kontrollfragen im Clip, Übungen mit Rückmeldung '
                'und Gesamttest als PDF.',
   themen=['Physik', 'Elektrizität', 'Ladung', 'Stromstärke', 'Widerstand',
           'Reihenschaltung', 'Parallelschaltung', 'FI-Schutzschalter', 'Leitprogramm']),
 'leitprogramme/leitprogramm-kinematik.html': dict(
   # Freigeschaltet am 04.10.2026 (nach /lp-pruefung).
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Kinematik — Geschwindigkeit, Beschleunigung, Vektoren, Fall und Wurf, Kreisbewegung',
   beschreibung='Leitprogramm zur Kinematik in fünf Kapiteln — Ort, Bahn und Geschwindigkeit; '
                'Beschleunigung und Bremsweg; Geschwindigkeit als Vektor; freier Fall und Wurf; '
                'gleichförmige Kreisbewegung — mit Erklärclips, Simulationen mit Aufgaben, '
                'Kontrollfragen im Clip, Übungen mit Rückmeldung und Gesamttest als PDF.',
   themen=['Physik', 'Kinematik', 'Geschwindigkeit', 'Beschleunigung', 'freier Fall',
           'Wurf', 'Relativbewegung', 'Kreisbewegung', 'Leitprogramm']),
 'leitprogramme/leitprogramm-dynamik.html': dict(
   # Freigeschaltet am 06.10.2026 (nach /lp-pruefung).
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Dynamik — Kraft, Masse, Beschleunigung, Aufzug, Faden, Kreisbahn',
   beschreibung='Leitprogramm zur Dynamik in fünf Kapiteln — Kraft, Masse und Beschleunigung; '
                'Gesamtkraft und Trägheitsgesetz; Gewichtskraft und Aufzug; zwei Körper an einem '
                'Faden; Zentripetalkraft — mit Erklärclips, laufenden Simulationen mit Aufgaben, '
                'Kontrollfragen im Clip, Übungen mit Rückmeldung und Gesamttest als PDF.',
   themen=['Physik', 'Dynamik', 'Kraft', 'Grundgesetz', 'Trägheitsgesetz', 'Gewichtskraft',
           'Normalkraft', 'Zentripetalkraft', 'Leitprogramm']),
 'leitprogramme/leitprogramm-energie.html': dict(
   # Freigeschaltet am 06.10.2026 (nach /lp-pruefung).
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Energie — Arbeit, Energieerhaltung, Reibung und Motor, Leistung, Energiebilanz der Erde',
   beschreibung='Leitprogramm zur Energie in sechs Kapiteln — Energie und Arbeit; Lage- und '
                'Bewegungsenergie; Energieerhaltung; Reibung und Motor; Leistung und Wirkungsgrad; '
                'die Energiebilanz der Erde — mit Erklärclips, laufenden Simulationen mit Aufgaben, '
                'Kontrollfragen im Clip, Übungen mit Rückmeldung und Gesamttest als PDF.',
   themen=['Physik', 'Energie', 'Arbeit', 'Energieerhaltung', 'Leistung', 'Wirkungsgrad',
           'Energiebilanz der Erde', 'Treibhauseffekt', 'Leitprogramm']),
 'leitprogramme/leitprogramm-statik.html': dict(
   # Freigeschaltet am 06.10.2026 (nach /lp-pruefung).
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Statik — Kraft als Vektor, Resultierende, Haftreibung, Drehmoment, Hebelgesetz, Auflagerkräfte',
   beschreibung='Leitprogramm zur Statik in sechs Kapiteln — Kraft als Vektor; die resultierende '
                'Kraft; Kräfte am ruhenden Körper und schiefe Ebene; Drehmoment; Hebelgesetz; '
                'Auflagerkräfte — mit Erklärclips, laufenden Simulationen mit Aufgaben, '
                'Kontrollfragen im Clip, Übungen mit Rückmeldung und Gesamttest als PDF.',
   themen=['Physik', 'Statik', 'Kraft', 'Vektor', 'Resultierende', 'Drehmoment', 'Hebelgesetz',
           'Auflagerkraft', 'schiefe Ebene', 'Leitprogramm']),
 'leitprogramme/leitprogramm-hydrostatik.html': dict(
   # Freigeschaltet am 06.10.2026 (nach /lp-pruefung).
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Hydrostatik — Druck, Schweredruck, Luftdruck, Pascal, Auftrieb, Schwimmen',
   beschreibung='Leitprogramm zur Hydrostatik in sechs Kapiteln — Druck und Druckeinheiten; '
                'Schweredruck; Luftdruck; Pascal’sches Gesetz und hydraulische Presse; Auftrieb nach '
                'Archimedes; Schwimmen, Schweben, Sinken — mit Erklärclips, laufenden Simulationen mit '
                'Aufgaben, Kontrollfragen im Clip, Übungen mit Rückmeldung und Gesamttest als PDF.',
   themen=['Physik', 'Hydrostatik', 'Druck', 'Schweredruck', 'Luftdruck', 'Pascal', 'Hydraulik',
           'Auftrieb', 'Archimedes', 'Schwimmen', 'Leitprogramm']),
 'leitprogramme/leitprogramm-widerstand-leistung.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Widerstand, Leistung, Energie — ohmsches Gesetz bis Hochspannung',
   beschreibung='Leitprogramm zur Elektrizität: ohmsches Gesetz und Kennlinien, richtig messen '
                'mit Ampere- und Voltmeter, Widerstand eines Leiters, elektrische Leistung, '
                'Energie und Kosten, Verlustleistung und Hochspannung — in sieben Schritten '
                'mit Erklärclips, Simulationen, Vortest und Gesamttest.',
   themen=['Physik', 'Elektrizität', 'Ohmsches Gesetz', 'Widerstand', 'Leistung',
           'Energie', 'Leitprogramm']),
 'leitprogramme/leitprogramm-gefahren.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Gefahren und Schutzmassnahmen — FI, Schutzleiter, Sicherung',
   beschreibung='Leitprogramm zur Elektrizität: warum die Erde zum Rückleiter wird '
                '(der Neutralleiter ist am Transformator geerdet), '
                'Wirkung auf den Menschen, FI-Schutzschalter als zusätzlicher Schutz, '
                'Schutzleiter und Leitungsschutzschalter — in sechs Schritten mit '
                'Erklärclips, Simulationen, Vortest und Gesamttest.',
   themen=['Physik', 'Elektrizität', 'Elektrische Sicherheit', 'FI-Schutzschalter',
           'Schutzleiter', 'Leitungsschutzschalter', 'Leitprogramm']),
 'leitprogramme/uebungstest-waermelehre.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit', 'Übungsaufgaben'],
   titel='Leitprogramm Übungstest Wärmelehre — fünfzehn Aufgaben mit Erklärclip',
   beschreibung='Ein vollständiger Übungsbogen zur Wärmelehre, Aufgabe für Aufgabe '
                'aufgelöst: Einheiten und Dichte, Längen-, Flächen- und '
                'Volumenausdehnung, das ideale Gasgesetz mit Prozenten und '
                'Normbedingungen, Wärmebilanz mit Phasenwechsel und die Heizkurve — '
                'fünfzehn Aufgaben mit je einem vertonten Erklärclip, Musterlösung '
                'und Hinweis auf den typischen Fehler.',
   themen=['Wärmelehre', 'Wärmeausdehnung', 'Ideales Gas', 'Wärmebilanz',
           'Heizkurve', 'Dichte', 'Übungsaufgaben', 'Leitprogramm']),
 'leitprogramme/leitprogramm-vorwissen.html': dict(
   typ='article', lrt=['Leitprogramm', 'Selbstlerneinheit'],
   titel='Leitprogramm Grössen, Messen, Druck — das Vorwissen selbst erarbeiten',
   beschreibung='Leitprogramm zum physikalischen Vorwissen: Zahlenwert und Einheit, '
                'Vorsilben als Zehnerpotenzen, Flächen und Volumen, Runden auf drei '
                'signifikante Stellen, Masse und Gewichtskraft, Dichte, Druck und '
                'Überdruck — in acht Schritten mit Erklärclip, Simulation, Vortest '
                'und Gesamttest zur Selbstkontrolle.',
   themen=['Vorwissen', 'Grössen und Einheiten', 'Vorsilben', 'Signifikante Stellen',
           'Dichte', 'Druck', 'Überdruck', 'Gewichtskraft']),
 'clips.html': dict(
   typ='article', lrt=['Lernvideo', 'Animation'],
   titel='Clips — kurze Animationen zu den Rechenwegen',
   beschreibung='Kurze Animationen der Physik-Berufsmaturität: Ein Clip baut einen '
                'Gedankengang Schritt für Schritt auf, mit Farbführung und Text zum '
                'Mitlesen. Nach Lerngebieten geordnet.',
   themen=['Physik', 'Erklärclips', 'Animationen']),
 # Unverlinkt und nicht indexiert (HOWTO-uebungspruefung.md, Schritt 6b):
 # keine Karte, kein Eintrag im Suchindex, kein Sitemap-Eintrag — aber ein
 # Eintrag hier, damit Beschreibung, canonical und die Robots-Marke gesetzt
 # sind und die Seite beim naechsten Abgleich nicht vergessen wird.
 'loesungen/gravitation-und-elektronen-im-feld.html': dict(
   typ='article', lrt=['Lösungsblatt', 'Übungsaufgaben'], noindex=True,
   titel='Lösungen: Gravitation und Elektronen im Feld',
   beschreibung='Zwei Aufgabenblätter Schritt für Schritt gelöst: Gravitationsfeldstärke '
                'mit der Höhe, halbe Fluchtgeschwindigkeit, der Asteroid Pulcova mit seinem '
                'Möndchen — und Aufgabe 262 zu Elektronen im Plattenkondensator, '
                'Geschwindigkeitsfilter und Kreisbahn. Mit Erklärclips und Simulationen.',
   themen=['Physik', 'Gravitation', 'Plattenkondensator', 'Lorentzkraft', 'Lösungen']),
 'rechtliches.html': dict(
   typ='website', noindex=False,
   titel='Rechtliches & Datenschutz',
   beschreibung='Verantwortlichkeit, Haftung, Lizenz und Datenschutz von Physik begreifbar — ohne Cookies, ohne Tracking.',
   themen=['Impressum', 'Datenschutz']),
 'feedback.html': dict(
   typ='website',
   titel='Kontakt & Feedback',
   beschreibung='Fehler melden, Verbesserungen vorschlagen oder Rückmeldung geben zu Physik begreifbar — ohne Anmeldung, Name und E-Mail freiwillig.',
   themen=['Kontakt', 'Feedback']),
 'sonnenfinsternis-12-08-2026.html': dict(
   typ='article', lrt='Extras',
   titel='Sonnenfinsternis vom 12. August 2026 über Thun',
   beschreibung='Partielle Sonnenfinsternis am 12. August 2026 über Thun: Sicherheitsregeln zum Filter, Simulation der Netzhautschädigung und der Verlauf des Abends zum Selberbewegen.',
   themen=['Sonnenfinsternis', 'Astronomie', 'Optik', 'Thun']),

 'themen/p0-0-vorwissen-kompakt.html': dict(
   beschreibung='Vorwissen Physik im Alltag: sieben Situationen vom Rucksack bis zum Wasserkocher zeigen, welche Werkzeuge aus der Sek I in der Berufsmaturität gebraucht werden.',
   themen=['Vorwissen', 'Alltagsphysik', 'Grössen', 'Einheiten']),
 'themen/p0-1-vorwissen-mathematik.html': dict(
   beschreibung='Rechnen und Schliessen für die Physik: Proportionalität, Formeln umstellen, Zehnerpotenzen, Runden und signifikante Stellen — mit interaktiven Übungen.',
   themen=['Proportionalität', 'Formel umstellen', 'Zehnerpotenzen', 'Signifikante Stellen', 'Dreisatz']),
 'themen/p0-2-vorwissen-physik.html': dict(
   beschreibung='Grössen, Einheiten und Messen: von der Grösse zur SI-Einheit, Dichte, Kraft und Energie, Präfixe, Umrechnen und Abschätzen — mit Animationen.',
   themen=['SI-Einheiten', 'Grössen', 'Dichte', 'Einheitenpräfixe', 'Messen']),
 'themen/p0-3-messen-waagen-dichte.html': dict(
   beschreibung='Messen in der Physik: Masse und Gewichtskraft, Balkenwaage gegen Küchen- und Federwaage, direktes und indirektes Messen, Dichte bestimmen und Einheiten umrechnen.',
   themen=['Masse', 'Gewichtskraft', 'Waage', 'Dichte', 'Verdrängungsmethode', 'Dichte-Einheiten']),
 'themen/p0-4-einheitentrainer.html': dict(
   beschreibung='Einheiten umrechnen üben: Übungsgenerator für Länge, Fläche, Volumen, Masse, Zeit, Tempo, Kraft, Druck, Energie, Leistung, Dichte und Temperatur.',
   themen=['Einheiten umrechnen', 'Übungsgenerator', 'Einheitenpräfixe', 'Zehnerpotenzen', 'SI-Einheiten']),
 'themen/p0-5-si-einheiten.html': dict(
   beschreibung='Die sieben SI-Basiseinheiten: Herkunft und heutige Definition von Sekunde, Meter, Kilogramm, Ampere, Kelvin, Mol und Candela — mit Simulationen.',
   themen=['SI-Basiseinheiten', 'Naturkonstanten', 'Meter', 'Kilogramm', 'Sekunde', 'Einheitenvorsilben']),
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
          'circ': '°', 'approx': '≈', 'cdots': '…', 'times': '×',
          'vartheta': 'ϑ', 'Omega': 'Ω', 'eta': 'η', 'nu': 'ν', 'varphi': 'φ',
          'leftrightarrow': '↔', 'longrightarrow': '→', 'Rightarrow': '⇒',
          'leq': '≤', 'geq': '≥', 'neq': '≠', 'sqrt': '√',
          'sin': 'sin', 'cos': 'cos', 'tan': 'tan', 'log': 'log', 'ln': 'ln',
          'frac': '/', 'tfrac': '/', 'dfrac': '/',   # Rueckfall, s. bruch_auf()
          'vec': '', 'text': '', 'mathrm': '', 'left': '', 'right': '', 'quad': ' '}


def bruch_auf(x):
    """\\frac{a}{b} zu a/b aufloesen, von innen nach aussen.

    Ohne das wird aus \\tfrac{1}{2} erst «/{1}{2}» und dann «12» — in
    Metadaten ist das eine falsche Zahl, kein Bruch.
    """
    muster = re.compile(r'\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}')
    for _ in range(4):
        x, n = muster.subn(r'\1/\2', x)
        if not n:
            break
    return x


def tex_weg(t):
    """LaTeX aus Fliesstext in lesbaren Klartext ueberfuehren."""
    def innen(m):
        x = bruch_auf(m.group(1))
        x = re.sub(r'\\[ ,;:!]', ' ', x)            # LaTeX-Abstaende
        x = re.sub(r'\^\s*\\circ', '°', x)         # ^\circ C -> °C, nicht ^°C
        x = re.sub(r'\\([a-zA-Z]+)', lambda k: MAKROS.get(k.group(1), ' '), x)
        # ^ und _ bleiben stehen: ohne sie wird aus v^2 ein «v2» und aus
        # F_G ein «FG» — in Metadaten waere das schlicht falsch.
        return re.sub(r'[{}$]', '', x).replace('\\', '')
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
            'name': 'Physik begreifbar', 'inLanguage': 'de-CH', 'license': LIZENZ,
            'publisher': person,
            'potentialAction': {
                '@type': 'SearchAction',
                'target': {'@type': 'EntryPoint', 'urlTemplate': BASIS + '?q={search_term_string}'},
                'query-input': 'required name=search_term_string',
            },
        })
    else:
        graph.append({'@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS, 'name': 'Physik begreifbar'})

    if ist_thema:
        graph.append({
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Physik begreifbar', 'item': BASIS},
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
         f'<meta name="author" content="{AUTOR}">']
    # noindex muss beides tun: aus der Sitemap nehmen UND die Robots-Marke
    # setzen. Die Sitemap allein haelt keine Suchmaschine ab, die die Adresse
    # anderswoher kennt — aus einem geteilten Link, einem Referrer, der
    # Browserleiste. Das nofollow haelt von der Seite aus auch die verlinkten
    # Dateien aus dem Index.
    if cfg.get('noindex'):
        z.append('<meta name="robots" content="noindex, nofollow">')
    z += [
         f'<link rel="canonical" href="{url}">',
         f'<link rel="icon" href="{auf}favicon.svg" type="image/svg+xml">',
         f'<link rel="icon" href="{auf}favicon-32.png" sizes="32x32" type="image/png">',
         f'<link rel="apple-touch-icon" href="{auf}apple-touch-icon.png">',
         f'<meta property="og:type" content="{cfg.get("typ", "article")}">',
         '<meta property="og:site_name" content="Physik begreifbar">',
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
    """Gibt (alter Stand, neuer Stand) zurueck. Beide, weil der Trockenlauf
    sie vergleichen will — und ein zweites Lesen der Datei sich so spart."""
    pfad = os.path.join(ROOT, datei)
    s = open(pfad, encoding='utf-8').read()
    neu = block(datei, cfg, s)
    if MARKE_AUF in s:
        s2 = re.sub(re.escape(MARKE_AUF) + r'.*?' + re.escape(MARKE_ZU), lambda _: neu, s, flags=re.S)
    else:
        m = re.search(r'</title>\n?', s)
        assert m, f'{datei}: kein <title>'
        s2 = s[:m.end()] + neu + '\n' + s[m.end():]
    return s, s2


def zeilenbilanz(alt, neu):
    """Wie viele Zeilen kaemen dazu, wie viele fielen weg."""
    plus = minus = 0
    for z in difflib.unified_diff(alt.splitlines(), neu.splitlines(), lineterm='', n=0):
        if z.startswith('+') and not z.startswith('+++'):
            plus += 1
        elif z.startswith('-') and not z.startswith('---'):
            minus += 1
    return plus, minus


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


ROBOTS = f"""# Physik begreifbar — alles darf indexiert werden.
User-agent: *
Allow: /

Sitemap: {BASIS}sitemap.xml
"""


def main(argv):
    ap = argparse.ArgumentParser(
        prog='build-seo.py',
        description='Setzt die generierten Kopfbloecke in die Seiten und schreibt '
                    'sitemap.xml und robots.txt. Gepflegt wird die Tabelle SEITEN '
                    'im Skript, nie der Block in der Seite.',
        epilog='Ohne Schalter wird geschrieben.')
    modus = ap.add_mutually_exclusive_group()
    modus.add_argument('--check', action='store_true',
                       help='nur pruefen, nichts schreiben; Exit 1, wenn etwas veraltet ist '
                            '(so ruft der Pre-Flight das Skript auf)')
    modus.add_argument('--dry-run', action='store_true',
                       help='Trockenlauf: zeigt, was sich aendern wuerde, und schreibt nichts')
    ap.add_argument('--diff', action='store_true',
                    help='nur mit --dry-run: zusaetzlich die betroffenen Zeilen zeigen')
    a = ap.parse_args(argv)
    if a.diff and not a.dry_run:
        ap.error('--diff gibt es nur zusammen mit --dry-run')

    schreiben = not (a.check or a.dry_run)
    aenderungen = []                         # (Name, alter Stand, neuer Stand)

    for datei, cfg in SEITEN.items():
        alt, neu = einsetzen(datei, cfg)
        if alt != neu:
            aenderungen.append((datei, alt, neu))
            if schreiben:
                open(os.path.join(ROOT, datei), 'w', encoding='utf-8').write(neu)

    for name, inhalt in (('sitemap.xml', sitemap()), ('robots.txt', ROBOTS)):
        pfad = os.path.join(ROOT, name)
        alt = open(pfad, encoding='utf-8').read() if os.path.exists(pfad) else ''
        if alt != inhalt:
            aenderungen.append((name, alt, inhalt))
            if schreiben:
                open(pfad, 'w', encoding='utf-8').write(inhalt)

    namen = [n for n, _, _ in aenderungen]

    if a.check:
        if aenderungen:
            print('SEO-Metadaten VERALTET:', ', '.join(namen))
            return 1
        print(f'SEO-Metadaten aktuell ({len(SEITEN)} Seiten).')
        return 0

    if a.dry_run:
        if not aenderungen:
            print(f'[Trockenlauf] nichts zu tun — {len(SEITEN)} Seiten, sitemap.xml '
                  f'und robots.txt sind aktuell.')
            return 0
        print(f'[Trockenlauf] nichts geschrieben. {len(aenderungen)} Datei(en) '
              f'wuerden sich aendern:')
        for name, alt, neu in aenderungen:
            plus, minus = zeilenbilanz(alt, neu)
            print(f'  {name:<52s} +{plus} / -{minus} Zeilen')
            if a.diff:
                for z in difflib.unified_diff(
                        alt.splitlines(), neu.splitlines(),
                        fromfile=name + '  (jetzt)', tofile=name + '  (neu)',
                        lineterm='', n=1):
                    print('    ' + z)
        return 0

    print(f'{len(SEITEN)} Seiten mit Metadaten versehen, sitemap.xml und robots.txt geschrieben.')
    if aenderungen:
        print('  geändert:', ', '.join(namen))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
