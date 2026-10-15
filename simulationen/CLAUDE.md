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
- `simulationen/schiefe-ebene.html` — Simulation Schiefe Ebene (4.2/4.3, seit 15.10.2026): **Fassung des Auftraggebers**,
  **ohne inhaltliche Anpassung** eingebunden — Texte, Aufbau, Modell (Haften bis \(\tan\alpha>\mu_H\), Rampe, Horizontale mit
  Gleitreibung, idealer Übergang), Phasen und die 15 Fragen bleiben **wörtlich**. Angepasst nur Konventionen: Schriften und
  MathJax lokal, Menü/Suche/Fusszeile/SEO-Marken (globale Stile per `:where(.wrap)` gegen style.css geschützt), Dezimalpunkt,
  Bernstein als Akzent, Vektorfarben wie Animation 5 in 4.2 (\(F_G\) Bernstein, \(F_N\) Blau, \(F_R\) Rot, Komponenten Violett,
  \(v\) Grün, \(a\) Violett, \(F_\text{res}\) Orange), \(F_G\) statt \(F_g\), `fmt` → `fnum` (kollidierte mit `const fmt` aus
  `physiklib.js`), Zeile «Themenseiten» im Kopf. Keine 👁/💡-Hinweise (wären neuer Inhalt). Selbsttest von aussen über
  `scripts/verify_schiefe_ebene.js` im Pre-Flight (exportiert `model`, `fnum`; Losrutschen, Beschleunigungen, Bremsweg,
  \(E_\text{mech}+E_\text{diss}=E_0\), Reibungsarbeit). Verweise: 4.2 `#schiefe-ebene`, 4.3 `#erhaltung`; kein Leitprogramm.
  **Bekannt, nicht geändert:** Das Symbol \(F_\mathrm{H}\) steht hier für die Haftreibung (Phase «Haften»), in 4.2 für die
  Hangabtriebskraft; die Höhenmarke «h = … m» wird abgeschnitten, sobald die Kamera der Bewegung folgt.
