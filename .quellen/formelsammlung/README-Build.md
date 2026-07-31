# TALS Physik – Formelsammlung: Build-Paket

Stand: 1. August 2026 · Version 1.0 · 17 Seiten · 0 Fehler, 0 Overfull-Boxen

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

Getestet mit pdfTeX 1.40.25 / LaTeX2e 2023-11-01, TeX Live 2023.
Benötigte Pakete ausserhalb der Standardinstallation: `qrcode`, `needspace`, `fancyhdr`,
`tikz` (mit `arrows.meta`, `decorations.pathmorphing`, `patterns`, `calc`, `angles`, `quotes`).

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

**Stand 01.08.2026:** Das ausgelieferte PDF wurde nicht neu gebaut, sondern nur im
fertigen Dokument auf den 1. August umdatiert (die Quelle lag damals nicht vor).
Quelle und PDF stimmen inhaltlich überein; der nächste `latexmk`-Lauf ersetzt das
umdatierte durch ein sauber gebautes.
