// ─────────────────────────────────────────────────────────────
//  TALS Physik — Shared Navigation (nav.js)
//  Version 1.0 · RLP-2030-Struktur 1:1 (10 Teilgebiete, 3 Lerngebiete)
//
//  Einbindung: <script src="../nav.js"></script>   (von Themenseiten)
//              <script src="nav.js"></script>      (von index.html)
//  Aufruf:     buildNav({ id, kapitelNr, kapitelTitel, prev, next, homepage })
//
//  Lerngebiet-Mapping (nach RLP-BM 7.5.4.1 Gruppe 1, Phys-Anteil):
//    Lerngebiet 4: Mechanik         (100 L) — p4-1 … p4-5
//    Lerngebiet 5: Thermodynamik    (30 L)  — p5-1 … p5-3
//    Lerngebiet 6: Einführung andere Bereiche (30 L) — p6-1 + p6-2
// ─────────────────────────────────────────────────────────────

const SITE = {
  themen: [
    { id:'p0-0', nr:'0.0', titel:'Vorwissen — die Alltagstour',    url:'themen/p0-0-vorwissen-kompakt.html' },
    { id:'p0-1', nr:'0.1', titel:'Mathematisches Vorwissen',       url:'themen/p0-1-vorwissen-mathematik.html' },
    { id:'p0-2', nr:'0.2', titel:'Physikalisches Alltagsverständnis', url:'themen/p0-2-vorwissen-physik.html' },
    { id:'p0-3', nr:'0.3', titel:'Technisches Vorwissen',          url:'themen/p0-3-vorwissen-technik.html' },
    { id:'p0-4', nr:'0.4', titel:'Logisches Denken',               url:'themen/p0-4-vorwissen-logik.html' },
    { id:'p4-1', nr:'4.1', titel:'Kinematik des Schwerpunkts',     url:'themen/p4-1-kinematik.html' },
    { id:'p4-2', nr:'4.2', titel:'Dynamik',                        url:'themen/p4-2-dynamik.html' },
    { id:'p4-3', nr:'4.3', titel:'Energie',                        url:'themen/p4-3-energie.html' },
    { id:'p4-4', nr:'4.4', titel:'Statik von Festkörpern',         url:'themen/p4-4-statik.html' },
    { id:'p4-5', nr:'4.5', titel:'Hydrostatik',                    url:'themen/p4-5-hydrostatik.html' },
    { id:'p5-1', nr:'5.1', titel:'Temperatur',                     url:'themen/p5-1-temperatur.html' },
    { id:'p5-2', nr:'5.2', titel:'Wärme',                          url:'themen/p5-2-waerme.html' },
    { id:'p5-3', nr:'5.3', titel:'Wärmeausdehnung',                url:'themen/p5-3-waermeausdehnung.html' },
    { id:'p6-1', nr:'6.1', titel:'Wellen',                         url:'themen/p6-1-wellen.html' },
    { id:'p6-1a', nr:'6.1a', titel:'Wellenexperimente',            url:'themen/p6-1a-wellenexperimente.html' },
    { id:'p6-2', nr:'6.2', titel:'Elektrizität',                   url:'themen/p6-2-elektrizitaet.html' },
  ]
};

// Lerngebiet-Gruppen für die Dropdown-Anzeige
const GROUPS = [
  { nr:'0', titel:'Vorwissen (kein RLP-Lerngebiet)',     ids:['p0-0','p0-1','p0-2','p0-3','p0-4'] },
  { nr:'4', titel:'Mechanik',                            lek:100, ids:['p4-1','p4-2','p4-3','p4-4','p4-5'] },
  { nr:'5', titel:'Thermodynamik',                       lek:30,  ids:['p5-1','p5-2','p5-3'] },
  { nr:'6', titel:'Einführung in andere Bereiche der Physik', lek:30, ids:['p6-1','p6-1a','p6-2'] }
];

function buildNav(cfg) {
  // cfg = { id, kapitelNr, kapitelTitel, prev, next, homepage }
  window.__navCfg = cfg;
  const prefix    = cfg.homepage ? '' : '../';
  const indexHref = cfg.homepage ? 'index.html' : '../index.html';

  const pageById = {};
  SITE.themen.forEach(p => pageById[p.id] = p);

  function renderDropdown() {
    return GROUPS.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'dd-aktiv':''}">
          <span class="dd-nr">${p.nr}</span>
          <span class="dd-tit">${p.titel}</span>
        </a>`;
      }).join('');
      return `<div class="dd-gruppe">
        <div class="dd-gruppe-titel">${g.nr} · ${g.titel}</div>
        ${items}
      </div>`;
    }).join('');
  }

  function renderMobileGroup() {
    return GROUPS.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'mn-aktiv':''}">${p.nr} · ${p.titel}</a>`;
      }).join('');
      return `<div class="mn-untergruppe">${g.nr} · ${g.titel}</div>${items}`;
    }).join('');
  }

  // Nachschlagewerke (Glossar + Formelsammlung) — neben „Themen"
  const refItems = [
    { href:`${prefix}glossar.html`,         nr:'A–Z', tit:'Glossar',                     cur:(cfg.id==='glossar') },
    { href:`${prefix}formelsammlung.html`,  nr:'∑',   tit:'Formelsammlung',               cur:(cfg.id==='formeln') },
  ];
  function renderRefDropdown() {
    const intern = refItems.map(r =>
      `<a href="${r.href}" class="${r.cur?'dd-aktiv':''}">
        <span class="dd-nr">${r.nr}</span>
        <span class="dd-tit">${r.tit}</span>
      </a>`).join('');
    return `<div class="dd-gruppe">
        <div class="dd-gruppe-titel">Lehrmittel-intern</div>
        ${intern}
      </div>
      <div class="dd-gruppe">
        <div class="dd-gruppe-titel">Offiziell</div>
        <a href="https://www.sbfi.admin.ch/dam/de/sd-web/xCh9wCCwVgrh/formulaire_final_d.pdf" target="_blank" rel="noopener">
          <span class="dd-nr">↗</span>
          <span class="dd-tit">BM-Formelsammlung (SBFI)</span>
        </a>
      </div>`;
  }
  function renderMobileRef() {
    const intern = refItems.map(r =>
      `<a href="${r.href}" class="${r.cur?'mn-aktiv':''}">${r.nr} · ${r.tit}</a>`).join('');
    return `<div class="mn-untergruppe">Nachschlagen</div>${intern}
      <a href="https://www.sbfi.admin.ch/dam/de/sd-web/xCh9wCCwVgrh/formulaire_final_d.pdf" target="_blank" rel="noopener">↗ BM-Formelsammlung (SBFI)</a>`;
  }

  // ── META-DROPDOWN-INHALTE ──
  const metaAutorHTML = `
    <div class="meta-titel">Autor &amp; Intention</div>
    <p>Erstellt von einem Elektroingenieur mit über 30 Jahren Unterrichtserfahrung,
       der gerne Mathematik und Physik erklärt — seinen Schülerinnen und Schülern
       genauso wie seinen fünf Kindern. Begeistert von dem, was sich mit KI im
       Bildungsbereich machen lässt.</p>
    <p>Dieses Lehrmittel <strong>ersetzt weder Lehrperson noch klassisches Lehrbuch</strong>.
       Es will eine niederschwellige, animierte und animierende Ergänzung sein, die der
       Lehrperson didaktischen Freiraum schafft — zum Beispiel für Methoden wie
       <em>Flipped Classroom</em>.</p>`;

  const metaAusblickHTML = `
    <div class="meta-titel">Ausblick</div>
    <div class="meta-sub">Erstellt</div>
    <ul>
      <li>Alle 10 Teilgebiete vollständig (Lerngebiete 4 Mechanik, 5 Thermodynamik, 6 Wellen und Elektrizität)</li>
      <li>Kapitel 0 Vorwissen (5 Seiten zur Sek-I-Auffrischung: kompakte Alltagstour plus Mathematik, Physik, Technik, Logik — kein RLP-Lerngebiet)</li>
      <li>6.1a Wellenexperimente — dynamische Vertiefungsseite zu 6.1 (Transversal-/Longitudinalwellen, Superposition, stehende Wellen)</li>
      <li>Je Themenseite: interaktive Animationen, Aufgaben, Zusammenfassung, 5 Druckseiten/Materialien und externe Ressourcen</li>
    </ul>
    <div class="meta-sub">Geplant</div>
    <ul>
      <li>Optionale Erweiterungen über die RLP-Grundlagen hinaus (z.B. Magnetismus / Elektromagnetismus, Schwingungen)</li>
    </ul>
    <div class="meta-sub">Schwesterprojekt</div>
    <ul>
      <li><a href="https://github.com/go4exercises/TALS-Mathe" target="_blank" rel="noopener" class="meta-link">TALS Mathematik</a> — gleicher Aufbau für das Fach Mathematik</li>
    </ul>`;

  const metaFeedbackHTML = `
    <div class="meta-titel">Feedback</div>
    <p>Fehler gefunden? Verbesserungsvorschlag? Fehlendes Thema?
       Bitte über den GitHub-Issue-Tracker melden — so geht keine Rückmeldung verloren
       und alle anderen profitieren von der Diskussion.</p>
    <p><a href="https://github.com/go4exercises/TALS-Physik/issues/new" target="_blank" rel="noopener" class="meta-link">
       → Issue auf GitHub erstellen</a></p>`;

  const metaLizenzHTML = `
    <div class="meta-titel">Lizenz</div>
    <p>Inhalte erstellt mit Unterstützung von <strong>Claude</strong> (Anthropic).</p>
    <p>Veröffentlicht unter <strong>Creative Commons BY-NC 4.0</strong>:
       Inhalte sind frei nutzbar für nicht-kommerzielle Zwecke, dürfen verändert
       und weitergegeben werden — bei Kopien und Weiterverarbeitung bitte auf die
       Herkunft verweisen. Die Inhalte sind frei und sollen frei bleiben.</p>
    <p><a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener" class="meta-link">
       → Lizenztext (CC BY-NC 4.0)</a></p>`;

  // ── HEADER ──
  const headerHTML = `
<header class="site-hdr">
  <a href="${indexHref}" class="logo">
    Physik
  </a>
  <nav class="site-nav">
    <div class="dropdown">
      <button class="nav-btn${(cfg.id && pageById[cfg.id]) ? ' aktiv':''}" onclick="toggleDD('dd-themen')">
        Themen ▾
      </button>
      <div class="dd-menu dd-menu-gross" id="dd-themen">
        ${renderDropdown()}
      </div>
    </div>
    <div class="dropdown">
      <button class="nav-btn${(cfg.id==='glossar'||cfg.id==='formeln') ? ' aktiv':''}" onclick="toggleDD('dd-ref')">
        Nachschlagen ▾
      </button>
      <div class="dd-menu" id="dd-ref">
        ${renderRefDropdown()}
      </div>
    </div>
    <a href="https://go4exercises.github.io/TALS-Mathe/" target="_blank" rel="noopener">Mathematik ↗</a>

    <span class="nav-sep" aria-hidden="true"></span>

    <div class="dropdown">
      <button class="nav-btn nav-meta" onclick="toggleDD('dd-ueber')">
        <span class="ueber-icon" aria-hidden="true">ⓘ</span> Über ▾
      </button>
      <div class="dd-menu dd-menu-ueber" id="dd-ueber">
        <div class="ueber-tabs" role="tablist">
          <button class="ueber-tab aktiv" role="tab" data-target="ueber-autor">Autor &amp; Intention</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-ausblick">Ausblick</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-feedback">Feedback</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-lizenz">Lizenz</button>
        </div>
        <div class="ueber-panels">
          <div class="ueber-panel aktiv" id="ueber-autor"   role="tabpanel">${metaAutorHTML}</div>
          <div class="ueber-panel"        id="ueber-ausblick" role="tabpanel">${metaAusblickHTML}</div>
          <div class="ueber-panel"        id="ueber-feedback" role="tabpanel">${metaFeedbackHTML}</div>
          <div class="ueber-panel"        id="ueber-lizenz"   role="tabpanel">${metaLizenzHTML}</div>
        </div>
      </div>
    </div>
  </nav>
  <button class="burger" onclick="toggleMobileNav()" aria-label="Navigation">☰</button>
</header>
<div class="mobile-nav" id="mobile-nav">
  <a href="${indexHref}">← Übersicht</a>
  ${renderMobileGroup()}
  ${renderMobileRef()}
  <div class="mn-gruppe">Über dieses Lehrmittel</div>
  <details class="mn-meta"><summary>Autor &amp; Intention</summary><div class="mn-meta-body">${metaAutorHTML}</div></details>
  <details class="mn-meta"><summary>Ausblick</summary><div class="mn-meta-body">${metaAusblickHTML}</div></details>
  <details class="mn-meta"><summary>Feedback</summary><div class="mn-meta-body">${metaFeedbackHTML}</div></details>
  <details class="mn-meta"><summary>Lizenz</summary><div class="mn-meta-body">${metaLizenzHTML}</div></details>
</div>`;

  document.getElementById('nav-root').innerHTML = headerHTML;

  document.addEventListener('click', e => {
    if (!e.target.closest('.dropdown') && !e.target.closest('.nav-btn')) {
      document.querySelectorAll('.dd-menu').forEach(m => m.classList.remove('open'));
    }
  });
}

function toggleDD(id) {
  const el = document.getElementById(id);
  const wasOpen = el.classList.contains('open');
  document.querySelectorAll('.dd-menu').forEach(m => m.classList.remove('open'));
  if (!wasOpen) el.classList.add('open');
}

document.addEventListener('click', e => {
  const tab = e.target.closest('.ueber-tab');
  if (!tab) return;
  const wrap = tab.closest('.dd-menu-ueber');
  if (!wrap) return;
  wrap.querySelectorAll('.ueber-tab').forEach(t => t.classList.remove('aktiv'));
  wrap.querySelectorAll('.ueber-panel').forEach(p => p.classList.remove('aktiv'));
  tab.classList.add('aktiv');
  const target = wrap.querySelector('#' + tab.dataset.target);
  if (target) target.classList.add('aktiv');
});

function toggleMobileNav() {
  document.getElementById('mobile-nav').classList.toggle('open');
}

// ── Sticky ToC ──
const TOC_KURZ = {
  einstieg:       'Einstieg',
  definition:     'Definition',
  darstellungen:  'Darstellungen',
  typen:          'Typen',
  theorie:        'Theorie',
  aufgaben:       'Aufgaben',
  zusammenfassung:'Zusammenfassung',
  downloads:      'Zusatzmaterial',
  ressourcen:     'Externe V&S&A'
};

function buildToC() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const headings = document.querySelectorAll('.content h2[id]');
  if (headings.length < 2) { toc.closest('.toc-wrap')?.remove(); return; }

  const cfg = window.__navCfg || {};
  const kapitel = cfg.kapitelNr
    ? `Kapitel <span class="toc-kapnr">${cfg.kapitelNr}</span>`
    : 'Auf dieser Seite';
  const prevLink = cfg.prev
    ? `<a href="${cfg.prev.url}" class="toc-prev" title="${cfg.prev.titel}">← ${cfg.prev.nr}</a>`
    : '';
  const nextLink = cfg.next
    ? `<a href="${cfg.next.url}" class="toc-next" title="${cfg.next.titel}">${cfg.next.nr} →</a>`
    : '';

  toc.innerHTML =
    (prevLink ? `<div class="toc-nav toc-nav-oben">${prevLink}</div>` : '') +
    `<button type="button" class="toc-title" title="Zum Seitenanfang">${kapitel}<span class="toc-title-pfeil" aria-hidden="true">↑</span></button>` +
    [...headings].map(h => {
      const label = TOC_KURZ[h.id] || h.textContent;
      return `
      <a href="#${h.id}" class="toc-link toc-${h.tagName.toLowerCase()}" title="${h.textContent.trim()}">
        ${label}
      </a>`;
    }).join('') +
    (nextLink ? `<div class="toc-nav toc-nav-unten">${nextLink}</div>` : '');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
        const link = toc.querySelector(`[href="#${e.target.id}"]`);
        if (link) link.classList.add('toc-aktiv');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });

  headings.forEach(h => observer.observe(h));

  // Sofortige, konsistente Markierung beim Klick (ohne auf den Observer zu warten);
  // Sprünge sind instant (kein Smooth-Scroll), wie bei der Titelwahl.
  toc.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', () => {
      document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
      link.classList.add('toc-aktiv');
    });
  });
  // Kapiteltitel = Sprung an den Seitenanfang (instant), Markierung zurücksetzen.
  const titelEl = toc.querySelector('.toc-title');
  if (titelEl) titelEl.addEventListener('click', () => {
    window.scrollTo(0, 0);
    history.replaceState(null, '', location.pathname + location.search);
    document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
  });
}

document.addEventListener('DOMContentLoaded', buildToC);
