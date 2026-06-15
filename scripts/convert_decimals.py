r"""
Convert Dezimalkomma → Dezimalpunkt in alle HTML-Dateien von TALS-Physik.

Konvention (gemäss STYLEGUIDE §2.5): Dezimal**punkt**, nicht Dezimalkomma.
Übernommen 1:1 aus tals-mathe/scripts/convert_decimals.py, nur ROOT und
Glob-Patterns für die Physik-Repo-Struktur angepasst (themen/, downloads/themen/).

Strategie (in dieser Reihenfolge):
1. Alle <style>, <svg>, Google-Fonts-URLs, SVG-Attribute (d/points/viewBox/transform)
   werden ausmaskiert — diese werden NICHT verändert.
2. Alle <script>-Blöcke werden separat ausmaskiert. In ihnen wird NACHHER
   gezielt nur das Pattern `[0-9]{,}[0-9]` → `[0-9].[0-9]` ersetzt (eindeutig
   MathJax-Dezimal). Normale JS-Kommas (z.B. f(1, 2)) bleiben unangetastet.
3. Im verbliebenen HTML/MathJax wird:
   - `[0-9]{,}[0-9]` → `[0-9].[0-9]` (MathJax-Dezimalkomma überall, ob in
     \(...\) oder als versehentlich übernommene Notation im Klartext)
   - `[0-9],[0-9]` → `[0-9].[0-9]` (Klartext-Dezimalkomma)
4. Alle Maskierungen zurücksetzen.
"""

import os
import re
import glob
import sys

ROOT = "/home/claude/work/tals-physik"


def process_text(text, allow_coord_replace=False):
    """Konvertiert Dezimalkommas in einem Text-String.

    Wenn allow_coord_replace=True, werden auch nackte 2-Tupel `(a, b)` aus
    Ganzzahlen zu `(a | b)` umgestellt. Sonst bleiben sie unangetastet.

    Gibt `(new_text, n_dec, n_coord)` zurück.
    """

    # ---- Phase 1: Geschützte Regionen rausnehmen ----
    protected = []
    script_indices = []

    def stash(match):
        protected.append(match.group(0))
        return f"\x00P{len(protected)-1}\x00"

    def stash_script(match):
        protected.append(match.group(0))
        idx = len(protected) - 1
        script_indices.append(idx)
        return f"\x00P{idx}\x00"

    text = re.sub(r'<script\b[^>]*>.*?</script>',
                  stash_script, text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style\b[^>]*>.*?</style>',
                  stash, text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<svg\b[^>]*>.*?</svg>',
                  stash, text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\sd="[^"]*"', stash, text)
    text = re.sub(r"\sd='[^']*'", stash, text)
    text = re.sub(r'\spoints="[^"]*"', stash, text)
    text = re.sub(r'\sviewBox="[^"]*"', stash, text)
    text = re.sub(r'\stransform="[^"]*"', stash, text)
    # Inline-Event-Handler
    text = re.sub(r'\son\w+="[^"]*"', stash, text)
    text = re.sub(r"\son\w+='[^']*'", stash, text)
    text = re.sub(r'fonts\.googleapis\.com[^"\s]*', stash, text)
    text = re.sub(r'fonts\.gstatic\.com[^"\s]*', stash, text)

    # LaTeX-Subscripts mit Index-Liste schützen: x_{1,2}, a_{i,j} etc.
    text = re.sub(r'_\{[0-9]+,\s*-?[0-9]+\}', stash, text)
    text = re.sub(r'_\{[0-9]+(?:,\s*-?[0-9]+){2,}\}', stash, text)

    # Punkt-Koordinaten / Vektor-Tupel etc. schützen
    text = re.sub(
        r'\(\s*-?[0-9]+(?:\s*,\s*-?[0-9]+){1,3}\s*\)',
        stash, text)

    n_coords = [0]

    def replace_coord(match):
        a, b = match.group(1), match.group(2)
        n_coords[0] += 1
        return f"({a} | {b})"

    if allow_coord_replace:
        text = re.sub(
            r'\(\s*(-?[0-9]+)\s*,\s*(-?[0-9]+)\s*\)',
            replace_coord, text)

    # ---- Phase 2: HTML/MathJax-Klartext bearbeiten ----
    text, n1 = re.subn(r'([0-9])\{,\}([0-9])', r'\1.\2', text)
    text, n2 = re.subn(r'([0-9]),([0-9])', r'\1.\2', text)
    n_total = n1 + n2

    # ---- Phase 3: <script>-Blöcke separat behandeln ----
    for idx in script_indices:
        block = protected[idx]
        new_block, n = re.subn(r'([0-9])\{,\}([0-9])', r'\1.\2', block)
        protected[idx] = new_block
        n_total += n

    # ---- Phase 4: Geschützte Regionen zurücksetzen ----
    def restore(match):
        return protected[int(match.group(1))]

    text = re.sub(r'\x00P(\d+)\x00', restore, text)

    return text, n_total, n_coords[0]


def process_file(filepath, dry_run=False):
    # Für Physik aktuell keine Coord-Whitelist nötig — Pilot-Themenseite hat keine
    # (a | b)-Punkt-Notation; falls später Themenseiten mit Vektor-Komponenten
    # 2D-Tupel als Punkt-Koordinaten verwenden, hier eintragen.
    COORD_WHITELIST = set()
    rel = os.path.relpath(filepath).replace(os.sep, '/')
    allow_coord = rel in COORD_WHITELIST

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    new_text, n_dec, n_coord = process_text(original, allow_coord_replace=allow_coord)
    changed = new_text != original
    if changed and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
    return n_dec, n_coord, changed


def verify_no_residuals(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    masked = text
    masked = re.sub(r'<style\b[^>]*>.*?</style>', '<S>', masked,
                    flags=re.DOTALL | re.IGNORECASE)
    masked = re.sub(r'<svg\b[^>]*>.*?</svg>', '<S>', masked,
                    flags=re.DOTALL | re.IGNORECASE)
    masked = re.sub(r'\sd="[^"]*"', '<S>', masked)
    masked = re.sub(r"\sd='[^']*'", '<S>', masked)
    masked = re.sub(r'\spoints="[^"]*"', '<S>', masked)
    masked = re.sub(r'\sviewBox="[^"]*"', '<S>', masked)
    masked = re.sub(r'\stransform="[^"]*"', '<S>', masked)
    masked = re.sub(r'\son\w+="[^"]*"', '<S>', masked)
    masked = re.sub(r"\son\w+='[^']*'", '<S>', masked)
    masked = re.sub(r'fonts\.googleapis\.com[^"\s]*', '<S>', masked)
    masked = re.sub(r'fonts\.gstatic\.com[^"\s]*', '<S>', masked)
    masked = re.sub(r'_\{[0-9]+(?:,\s*-?[0-9]+)+\}', '<S>', masked)
    masked = re.sub(r'\(\s*-?[0-9]+(?:\s*,\s*-?[0-9]+){1,3}\s*\)', '<S>', masked)
    masked = re.sub(r'\(\s*-?[0-9]+\s*,\s*-?[0-9]+\s*\)', '<S>', masked)

    script_braces = 0
    for m in re.finditer(r'<script\b[^>]*>.*?</script>', masked,
                         flags=re.DOTALL | re.IGNORECASE):
        script_braces += len(re.findall(r'[0-9]\{,\}[0-9]', m.group(0)))

    non_script = re.sub(r'<script\b[^>]*>.*?</script>', '<S>', masked,
                        flags=re.DOTALL | re.IGNORECASE)
    klartext_brace = len(re.findall(r'[0-9]\{,\}[0-9]', non_script))
    klartext_comma = len(re.findall(r'[0-9],[0-9]', non_script))

    stray = '\x00' in text or '\x01' in text

    return {
        'script_brace': script_braces,
        'klartext_brace': klartext_brace,
        'klartext_comma': klartext_comma,
        'stray_placeholder': stray,
    }


def main():
    dry_run = '--dry-run' in sys.argv
    os.chdir(ROOT)

    # Physik-Glob-Pattern: themen/ statt grundlagen/+schwerpunkt/,
    # downloads/themen/ statt downloads/grundlagen/+downloads/schwerpunkt/
    files = sorted(
        glob.glob('themen/*.html') +
        glob.glob('downloads/themen/**/*.html', recursive=True) +
        ['index.html', 'TEMPLATE.html']
    )

    print(f"{'Datei':<70} {'Dezimal':>8} {'Koord':>6}")
    print("-" * 88)

    total_dec = 0
    total_coord = 0
    n_changed = 0
    for fp in files:
        if not os.path.exists(fp):
            continue
        n_dec, n_coord, changed = process_file(fp, dry_run=dry_run)
        if n_dec or n_coord:
            short = fp if len(fp) <= 69 else "..." + fp[-66:]
            print(f"{short:<70} {n_dec:>8} {n_coord:>6}")
            total_dec += n_dec
            total_coord += n_coord
            if changed:
                n_changed += 1

    print("-" * 88)
    print(f"{'TOTAL':<70} {total_dec:>8} {total_coord:>6}")
    print()
    print(f"Dateien verändert: {n_changed}{'  (DRY RUN)' if dry_run else ''}")
    print(f"Dezimal-Umstellungen: {total_dec}")
    print(f"Koordinaten-Umstellungen ((a,b) → (a | b)): {total_coord}")

    if not dry_run:
        print()
        print("=== Verifikation: Residuen nach Konvertierung ===")
        all_clean = True
        for fp in files:
            if not os.path.exists(fp):
                continue
            res = verify_no_residuals(fp)
            problems = [k for k, v in res.items() if v]
            if problems:
                all_clean = False
                print(f"  RESIDUEN in {fp}: {res}")
        if all_clean:
            print("  Alle Dateien sauber — keine restlichen {,}, Kommas oder Stray-Placeholder.")


if __name__ == '__main__':
    main()
