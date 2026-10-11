# Simulationen — Details

Aus der Wurzel-`CLAUDE.md` ausgelagert (11.10.2026, /doctor): Claude Code lädt diese Datei, sobald in diesem
Ordner gearbeitet wird. Die Regeln der Wurzel-`CLAUDE.md` gelten weiter; bei Widerspruch gilt STYLEGUIDE.md.

- `simulationen/bungee-sprung.html` — Simulation Bungee-Jumping (4.2/4.3, seit 11.10.2026): **Fassung des
  Auftraggebers**, freigegeben — Texte, Aufbau (kompakte Vollbildansicht), Phasen, Momentanwerte \(s(t)=s(\ldots\;\text{s})=\ldots\)
  in den Farben der Pfeile und die 14 Fragen bleiben **wörtlich**. Angepasst nur, was Hausregeln verlangen: Schriften und
  MathJax lokal, Menü/Suche/Fusszeile/SEO-Marken (eigene Stile per `:where(.wrap)` gegen style.css geschützt), Dezimalpunkt,
  Bernstein und Vektorfarben nach STYLEGUIDE, \(D\) statt \(k\), \(F_G\), \(F_{\mathrm{res}}\), «Zeitregler», Strichpunkte;
  dazu \(E_\text{diss}\)-Kurve, \(T\) als kleine Schwingungen, Latexwerte als Annahme (Kockelman/Hubbard nur Vorbild),
  «Worauf achten?»/«Erkenntnis» im Kopf. **Bekannt und vom Auftraggeber so gewollt:** Bei 360 px läuft die Seite über
  (render-check meldet es). Dämpfung voreingestellt 15 kg/s. Selbsttest von aussen über `scripts/verify_bungee.js` im
  Pre-Flight (exportiert `simulate`, `elasticForce`, `fnum`; s_max, v_max gegen die Energiebilanz, E_tot erhalten,
  Gent-Eichung, E_diss monoton, Seil drückt nie). Verweise: 4.2 `#grundgesetz`, 4.3 `#elastisch`; kein Leitprogramm.
