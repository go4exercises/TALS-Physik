# Physik begreifbar – Formelsammlung: Build-Paket

Stand: 14. September 2026 · Version 1.0 · 17 Seiten · 0 Fehler, 0 Overfull-Boxen

## Inhalt

| Datei | Rolle |
| --- | --- |
| `formelsammlung.tex` | Quelle — die einzige Datei, die von Hand bearbeitet wird |
| `formelsammlung.aux` | **wichtig**, siehe unten — Hilfsmarken, Inhaltsverzeichnis, hyperref-Ziele |
| `formelsammlung.toc` | Inhaltsverzeichnis |
| `formelsammlung.out` | PDF-Lesezeichen (hyperref) |
| `formelsammlung.log` | vollständiges Protokoll des letzten Laufs |
| `formelsammlung.fls` | Liste aller gelesenen und geschriebenen Dateien |
| `formelsammlung.fdb_latexmk` | latexmk-Datenbank (Abhängigkeiten, Prüfsummen) |
| `pruefdateien/` | Hilfsdokumente aus der Verifikation, siehe unten |

## Bauen

```bash
latexmk -pdf formelsammlung.tex
```

Gebaut mit pdfTeX 1.40.28 / TeX Live 2025 (Ubuntu 26.04); vorher TeX Live 2023.
Benötigte Pakete ausserhalb der Standardinstallation: `qrcode`, `needspace`, `fancyhdr`,
`tikz` (mit `arrows.meta`, `decorations.pathmorphing`, `patterns`, `calc`, `angles`, `quotes`).

Auf Ubuntu genügt:

```bash
sudo apt-get install --no-install-recommends latexmk texlive-latex-recommended \
  texlive-latex-extra texlive-pictures texlive-fonts-recommended texlive-lang-german
```

### babel: `german`, nicht `ngerman`

Die Zeile heisst `\usepackage[provide=*,german]{babel}`. Mit `provide=*` läuft babel über
den **ini-Mechanismus**, und der kennt nur `german` — `ngerman` bricht dort mit
«'ngerman' not valid with the 'ini' mechanism» ab. Das ist keine Rückkehr zur alten
Rechtschreibung: `babel-de.ini` setzt `hyphenrules = ngerman`, die Trennmuster sind
also die neuen. Bis TeX Live 2023 wurde `ngerman` noch geschluckt; seit 2025 nicht mehr.

### Achtung: zwei Durchläufe sind zwingend

Das Dokument braucht **mindestens zwei pdfLaTeX-Läufe** — nicht nur wegen Inhaltsverzeichnis
und Querverweisen, sondern wegen der laufenden Kopfzeile.

Hintergrund: `\LG` schreibt beim Kapitelanfang eine Marke `\talsfresh{<Seite>}` in die `.aux`,
wenn das Kapitel ganz oben auf einer Seite beginnt. Die Kopfzeile liest diese Marken beim
*nächsten* Lauf und zeigt auf solchen Seiten nur das neue Kapitel statt beider Kapitel.
Aktuell betroffen: Seite 5 und Seite 14.

Nach einem einzigen Lauf ohne vorhandene `.aux` steht auf Seite 14 fälschlich
«5 Thermodynamik | 6 Einführung in andere Bereiche der Physik» statt «6 Einführung in andere
Bereiche der Physik». `latexmk` erledigt die Wiederholung automatisch; ein einzelner Aufruf
von `pdflatex` reicht nicht.

Wer `.aux` löscht, muss also zweimal übersetzen. Deshalb liegt die `.aux` hier bei.

## Verzeichnis `pruefdateien/`

Keine Bestandteile des Dokuments, sondern die Hilfsdokumente, mit denen die Abbildungen
geprüft wurden. Sie laden dieselbe Präambel und rendern jeweils entweder nur die Linien
(`*_ink.tex`) oder nur die Beschriftungen (`*_txt.tex`) derselben Abbildungen. Beide Fassungen
werden bei 300 dpi gerastert und pixelweise verglichen; überlappende Tinte bedeutet eine
Kollision zwischen Schrift und Grafik.

| Datei | geprüft |
| --- | --- |
| `t_curve.tex` / `t_label.tex` | Gasgesetz-Diagramme (S. 13) |
| `w_ink.tex` / `w_txt.tex` | Wellendiagramme (S. 14) |
| `c_ink.tex` / `c_txt.tex` | Schaltbilder (S. 15/16) |
| `f_ink.tex` / `f_txt.tex` | Wellen- und Schaltbilder zusammen, inklusive Achsenbeschriftungen |
| `measure.tex`, `m2.tex` | Ausmessen von Textbreiten und -höhen für die Platzierung von Labels |

Die Auswertung selbst lief in Python (Pillow, NumPy, SciPy, OpenCV für die QR-Codes) und ist
nicht Teil dieses Pakets.

## Wo das fertige PDF liegt

Das ausgelieferte Dokument steht im Repo-Root als `TALS-Physik-Formelsammlung.pdf`
(darauf zeigt das Menü «Nachschlagen»). In diesem Ordner liegt es bewusst **nicht**,
damit es nur eine gültige Fassung gibt. Nach einem Neubau die erzeugte
`formelsammlung.pdf` dorthin kopieren und umbenennen.

**Stand 14.09.2026:** Sauber aus der Quelle gebaut — das umdatierte Dokument vom
1. August ist damit ersetzt. Inhaltlich unverändert (Version 1.0); neu sind allein der
Name «Physik begreifbar» und die Adresse `physik.begreifbar.ch`, Letztere auch in allen
18 Verweisen und in den drei QR-Codes. Der **Dateiname bleibt**
`TALS-Physik-Formelsammlung.pdf`: Menü, Sitemap und die Einheitentrainer-Seite zeigen
darauf.
