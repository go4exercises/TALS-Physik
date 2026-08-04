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
    { id:'p0-1', nr:'0.1', titel:'Rechnen und Schliessen',         url:'themen/p0-1-vorwissen-mathematik.html' },
    { id:'p0-2', nr:'0.2', titel:'Grössen, Einheiten und Messen', url:'themen/p0-2-vorwissen-physik.html' },
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
  { nr:'0', titel:'Vorwissen (kein RLP-Lerngebiet)',     ids:['p0-0','p0-1','p0-2'] },
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

  // Lerngebiet der aktuellen Seite — nur dessen Klappe startet offen, damit das
  // Mobilmenü nicht wieder als 22-zeilige Liste aufgeht.
  const aktGruppe = (GROUPS.find(g => g.ids.indexOf(cfg.id) !== -1) || {}).nr;

  function renderMobileGroup() {
    return GROUPS.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'mn-aktiv':''}">${p.nr} · ${p.titel}</a>`;
      }).join('');
      return `<details class="mn-lg"${g.nr===aktGruppe?' open':''}>
        <summary>${g.nr} · ${g.titel}</summary>
        <div class="mn-lg-body">${items}</div>
      </details>`;
    }).join('');
  }

  // Nachschlagewerke (Glossar + Formelsammlung) — neben „Themen"
  const refItems = [
    { href:`${prefix}glossar.html`,         nr:'A–Z', tit:'Glossar',                     cur:(cfg.id==='glossar') },
    { href:`${prefix}formelsammlung.html`,  nr:'∑',   tit:'Formelsammlung',               cur:(cfg.id==='formeln') },
    { href:`${prefix}TALS-Physik-Formelsammlung.pdf`, nr:'PDF',
      tit:'Formelsammlung illustriert — zum Herunterladen und Drucken', extern:true },
  ];
  // Auf Glossar/Formelsammlung startet im Mobilmenü «Nachschlagen» offen statt «Themen».
  const refAktiv = (cfg.id === 'glossar' || cfg.id === 'formeln');
  function renderRefDropdown() {
    const intern = refItems.map(r =>
      `<a href="${r.href}" class="${r.cur?'dd-aktiv':''}"${r.extern?' target="_blank" rel="noopener"':''}>
        <span class="dd-nr">${r.nr}</span>
        <span class="dd-tit">${r.tit}</span>
      </a>`).join('');
    return `<div class="dd-gruppe">
        <div class="dd-gruppe-titel">Lehrmittel-intern</div>
        ${intern}
      </div>`;
  }
  function renderMobileRef() {
    return refItems.map(r =>
      `<a href="${r.href}" class="${r.cur?'mn-aktiv':''}"${r.extern?' target="_blank" rel="noopener"':''}>${r.nr} · ${r.tit}</a>`).join('');
  }

  // ── META-DROPDOWN-INHALTE ──
  const metaAutorHTML = `
    <div class="meta-titel">Autor</div>
    <img class="meta-portrait" src="${prefix}autor.jpg" width="112" height="112" loading="lazy"
         alt="Porträt von Raphael Arnold Kohler (Aquarell)">
    <p><strong>Autor:</strong> Raphael Arnold Kohler, Elektroingenieur und BM-Fachlehrperson
       für Mathematik und Physik mit über 30 Jahren Unterrichtserfahrung.</p>
    <p>TALS Physik ist ein unabhängiges, kostenlos zugängliches Lernangebot für die Sek II,
       ausgerichtet auf den Rahmenlehrplan der Berufsmaturität Gruppe Technik, Architektur,
       Life Sciences (RLP-BM 2030, TALS). Es ergänzt Unterricht und Lehrmittel, ersetzt sie
       aber nicht. Das Angebot ist <strong>keine offizielle Publikation</strong> des SBFI,
       eines Kantons, einer Schule oder einer Prüfungsorganisation.</p>
    <p>Bei der Erstellung und technischen Umsetzung wurden KI-Werkzeuge eingesetzt.
       Alle veröffentlichten Inhalte werden redaktionell geprüft; die Verantwortung
       für die Veröffentlichung liegt bei Raphael Arnold Kohler.</p>`;

  const metaAusblickHTML = `
    <div class="meta-titel">Ausblick</div>
    <div class="meta-sub">Erstellt</div>
    <ul>
      <li>Alle 10 Teilgebiete vollständig (Lerngebiete 4 Mechanik, 5 Thermodynamik, 6 Wellen und Elektrizität)</li>
      <li>Kapitel 0 Vorwissen (3 Seiten zur Sek-I-Auffrischung)</li>
      <li>Je Themenseite: interaktive Animationen, Aufgaben, Zusammenfassung, Druckseiten/Materialien und externe Ressourcen</li>
      <li>Schwesterprojekt: <a href="https://go4exercises.github.io/TALS-Mathe/" target="_blank" rel="noopener" class="meta-link">TALS Mathematik</a> — gleicher Aufbau für das Fach Mathematik</li>
    </ul>
    <div class="meta-sub">Ideen für den Ausbau</div>
    <ul>
      <li>Erweiterungen über die RLP-Grundlagen hinaus (z.B. Magnetismus / Elektromagnetismus, Schwingungen)</li>
      <li>Animationen, die Lehrerdemos und Schülerexperimente visualisieren</li>
      <li>Übersetzung in Englisch</li>
      <li>Kapitelweise Moodle-Fragesammlungen</li>
      <li>Animierte Lösungen zu alten BM-Abschlussprüfungen</li>
      <li>Erweiterung für die Vorbereitung auf die Passerelle und die eidgenössische Maturitätsprüfung</li>
      <li>Mathematik erweitern mit Kombinatorik für die Gruppe GS</li>
    </ul>`;

  const metaLizenzHTML = `
    <div class="meta-titel">Lizenz</div>
    <p><strong>Autor:</strong> Raphael Arnold Kohler. Soweit nicht anders angegeben, stehen
       die von ihm erstellten Lerninhalte unter der Lizenz <strong>Creative Commons
       Namensnennung – Nicht kommerziell 4.0 International (CC BY-NC 4.0)</strong>.</p>
    <p>Die Inhalte dürfen für nicht-kommerzielle Zwecke geteilt und bearbeitet werden.
       Dabei sind Raphael Arnold Kohler als Urheber zu nennen, die Lizenz zu verlinken
       und Änderungen kenntlich zu machen. Inhalte Dritter und verlinkte externe
       Angebote unterliegen ihren eigenen Rechten und Nutzungsbedingungen.</p>
    <p><em>Empfohlene Namensnennung:</em> Raphael Arnold Kohler, TALS Physik,
       https://go4exercises.github.io/TALS-Physik/, CC BY-NC 4.0.</p>
    <p><a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener" class="meta-link">
       → Lizenztext (CC BY-NC 4.0)</a></p>
    <p><a href="https://github.com/go4exercises/TALS-Physik" target="_blank" rel="noopener" class="meta-link">
       → Quelltext und Inhalte des Lehrmittels (GitHub)</a></p>`;

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
        Über ▾
      </button>
      <div class="dd-menu dd-menu-ueber" id="dd-ueber">
        <div class="ueber-tabs" role="tablist">
          <button class="ueber-tab aktiv" role="tab" data-target="ueber-autor">Autor</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-ausblick">Ausblick</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-lizenz">Lizenz</button>
        </div>
        <div class="ueber-panels">
          <div class="ueber-panel aktiv" id="ueber-autor"   role="tabpanel">${metaAutorHTML}</div>
          <div class="ueber-panel"        id="ueber-ausblick" role="tabpanel">${metaAusblickHTML}</div>
          <div class="ueber-panel"        id="ueber-lizenz"   role="tabpanel">${metaLizenzHTML}</div>
        </div>
      </div>
    </div>
    <a href="${prefix}feedback.html" class="nav-meta">Kontakt &amp; Feedback</a>
  </nav>
  <div class="suche" id="suche">
    <button class="such-lupe" id="such-lupe" aria-label="Suche öffnen">🔍</button>
    <input type="search" class="such-feld" id="such-feld" autocomplete="off" spellcheck="false"
           placeholder="Suchen …  /" aria-label="Lehrmittel durchsuchen">
    <div class="such-panel" id="such-panel" role="listbox"></div>
  </div>
  <button class="burger" onclick="toggleMobileNav()" aria-label="Navigation">☰</button>
</header>
<div class="mobile-nav" id="mobile-nav">
  <a href="${indexHref}" class="mn-direkt">← Übersicht</a>
  <details class="mn-sektion"${refAktiv?'':' open'}>
    <summary>Themen</summary>
    <div class="mn-sektion-body">${renderMobileGroup()}</div>
  </details>
  <details class="mn-sektion"${refAktiv?' open':''}>
    <summary>Nachschlagen</summary>
    <div class="mn-sektion-body">${renderMobileRef()}</div>
  </details>
  <a href="https://go4exercises.github.io/TALS-Mathe/" target="_blank" rel="noopener" class="mn-direkt">Mathematik ↗</a>
  <details class="mn-sektion">
    <summary>Über dieses Lehrmittel</summary>
    <div class="mn-sektion-body">
      <details class="mn-meta"><summary>Autor</summary><div class="mn-meta-body">${metaAutorHTML}</div></details>
      <details class="mn-meta"><summary>Ausblick</summary><div class="mn-meta-body">${metaAusblickHTML}</div></details>
      <details class="mn-meta"><summary>Lizenz</summary><div class="mn-meta-body">${metaLizenzHTML}</div></details>
    </div>
  </details>
  <a href="${prefix}feedback.html" class="mn-direkt">Kontakt &amp; Feedback</a>
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
  ressourcen:     'Externe V&S&A',
  // rechtliches.html
  'datenschutz-aufruf':   'DS Seitenaufruf',
  'datenschutz-feedback': 'DS Feedback',
  // formelsammlung.html — sonst schneidet das ToC „Lerngebiet 4 · Mec…" ab
  konstanten:     'Konstanten',
  lg4:            '4 Mechanik',
  lg5:            '5 Thermodynamik',
  lg6:            '6 Andere Bereiche'
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
