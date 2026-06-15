/* anim-hinweise.js — gemeinsame Logik für die Animations-Hinweise
   (Rollover "Worauf achten?" / "Erkenntnis" mit optionaler Vorlese-Funktion).
   Markup pro Animation (in style.css gestaltet):
     <div class="widget-titelzeile">
       <h3>…Titel…</h3>
       <div class="anim-hinweis links">  …Auslöser + .ah-pop…  </div>
       <div class="anim-hinweis rechts"> …Auslöser + .ah-pop…  </div>
     </div>
   Vorlese-Text steht als Klartext im Attribut data-vorlesen der Schaltfläche
   (.ah-speak), damit Formeln verständlich klingen statt als roher LaTeX-Code. */
(function(){
  function init(){
    var supported = ('speechSynthesis' in window);
    function pickVoice(){
      var vs = window.speechSynthesis.getVoices() || [];
      return vs.find(function(v){return /^de([-_]|$)/i.test(v.lang);}) || null;
    }
    function stopSpeech(){
      if(supported) window.speechSynthesis.cancel();
      document.querySelectorAll('.ah-speak[aria-pressed="true"]').forEach(function(b){
        b.setAttribute('aria-pressed','false'); b.textContent='🔊 vorlesen';
      });
    }
    function entfixieren(ausser){
      document.querySelectorAll('.anim-hinweis.fixiert').forEach(function(x){
        if(x!==ausser) x.classList.remove('fixiert');
      });
    }

    // Vorlesen — läuft auch weiter, wenn das Rollover wieder schliesst
    document.querySelectorAll('.ah-speak').forEach(function(btn){
      if(!supported){ btn.disabled=true; btn.title='Vorlesen wird von diesem Browser nicht unterstützt'; return; }
      btn.addEventListener('click', function(e){
        e.stopPropagation();
        var speaking = btn.getAttribute('aria-pressed')==='true';
        stopSpeech();
        if(speaking) return;                 // erneuter Klick = Stopp
        var txt = (btn.getAttribute('data-vorlesen') || '').trim();
        if(!txt){ var el = btn.closest('.anim-hinweis').querySelector('.ah-text'); txt = el ? el.textContent.replace(/\s+/g,' ').trim() : ''; }
        if(!txt) return;
        var u = new SpeechSynthesisUtterance(txt);
        u.lang='de-DE'; u.rate=0.97;
        var v = pickVoice(); if(v) u.voice=v;
        u.onend = u.onerror = function(){ btn.setAttribute('aria-pressed','false'); btn.textContent='🔊 vorlesen'; };
        btn.setAttribute('aria-pressed','true'); btn.textContent='⏹ Stopp';
        window.speechSynthesis.speak(u);
      });
    });

    // Klick/Tap auf den Auslöser fixiert das Rollover, damit der Vorleseknopf sicher erreichbar ist
    document.querySelectorAll('.anim-hinweis .ah-trigger').forEach(function(tr){
      tr.addEventListener('click', function(e){
        e.stopPropagation();
        var h = tr.closest('.anim-hinweis');
        var war = h.classList.contains('fixiert');
        entfixieren(h);
        h.classList.toggle('fixiert', !war);
      });
    });

    // Klick ausserhalb schliesst fixierte Hinweise (Sprachausgabe läuft weiter)
    document.addEventListener('click', function(e){
      if(!e.target.closest('.anim-hinweis')) entfixieren(null);
    });
    // Escape schliesst und stoppt das Vorlesen
    document.addEventListener('keydown', function(e){
      if(e.key==='Escape'){ entfixieren(null); stopSpeech(); }
    });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
