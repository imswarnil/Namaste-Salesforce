(function () {
  'use strict';
  var noMo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Audio context factory ────────────────────────────────────────────────
  function ac() { try { return new (window.AudioContext || window.webkitAudioContext)(); } catch(e){ return null; } }
  function rel(ctx, ms) { setTimeout(function(){ try { ctx.close(); } catch(e){} }, ms||200); }

  // Light: 3-note ascending chime (quiet triangle)
  function chimeUp() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    [523,659,784].forEach(function(f,i){
      var o=ctx.createOscillator(),g=ctx.createGain(),t=ctx.currentTime+i*0.16;
      o.type='triangle';
      o.frequency.setValueAtTime(f,t);
      g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(0.07,t+0.05); g.gain.exponentialRampToValueAtTime(0.001,t+0.35);
      o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t+0.4);
    }); rel(ctx,1000);
  }

  // Dark: 2-note descending (quiet triangle)
  function chimeDown() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    [440,329].forEach(function(f,i){
      var o=ctx.createOscillator(),g=ctx.createGain(),t=ctx.currentTime+i*0.22;
      o.type='triangle'; o.frequency.setValueAtTime(f,t); o.frequency.linearRampToValueAtTime(f*0.92,t+0.25);
      g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(0.06,t+0.06); g.gain.exponentialRampToValueAtTime(0.001,t+0.38);
      o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t+0.42);
    }); rel(ctx,900);
  }

  // Burger click: soft bandpass click
  function softClick() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    var len=Math.floor(ctx.sampleRate*0.04), buf=ctx.createBuffer(1,len,ctx.sampleRate), d=buf.getChannelData(0);
    for(var i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.exp(-i/(len*0.12));
    var s=ctx.createBufferSource(),g=ctx.createGain(),f=ctx.createBiquadFilter();
    f.type='bandpass'; f.frequency.value=900; f.Q.value=2; s.buffer=buf; g.gain.value=0.2;
    s.connect(f); f.connect(g); g.connect(ctx.destination); s.start(); s.stop(ctx.currentTime+0.05);
    rel(ctx,150);
  }

  // Dropdown: gentle pop
  function softPop() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    var o=ctx.createOscillator(),g=ctx.createGain();
    o.type='sine'; o.frequency.setValueAtTime(700,ctx.currentTime); o.frequency.exponentialRampToValueAtTime(480,ctx.currentTime+0.04);
    g.gain.setValueAtTime(0.06,ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.06);
    o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime+0.07); rel(ctx,150);
  }

  // Search: soft whoosh
  function softSwoosh() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    var len=Math.floor(ctx.sampleRate*0.18), buf=ctx.createBuffer(1,len,ctx.sampleRate), d=buf.getChannelData(0);
    for(var i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.exp(-i/(len*0.4));
    var s=ctx.createBufferSource(),g=ctx.createGain(),f=ctx.createBiquadFilter();
    f.type='highpass'; f.frequency.setValueAtTime(300,ctx.currentTime); f.frequency.exponentialRampToValueAtTime(3500,ctx.currentTime+0.15);
    s.buffer=buf; g.gain.setValueAtTime(0.12,ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.18);
    s.connect(f); f.connect(g); g.connect(ctx.destination); s.start(); s.stop(ctx.currentTime+0.2); rel(ctx,300);
  }

  // Nav click: subtle tick
  function softTick() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    var o=ctx.createOscillator(),g=ctx.createGain();
    o.type='sine'; o.frequency.setValueAtTime(1100,ctx.currentTime); o.frequency.exponentialRampToValueAtTime(800,ctx.currentTime+0.02);
    g.gain.setValueAtTime(0.04,ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.025);
    o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime+0.03); rel(ctx,100);
  }

  // $ hover: coin pings
  function coinPing() {
    if (noMo) return; var ctx=ac(); if (!ctx) return;
    [1600,2000,2400,1800].forEach(function(f,i){
      var o=ctx.createOscillator(),g=ctx.createGain(),t=ctx.currentTime+i*0.055;
      o.type='sine'; o.frequency.setValueAtTime(f+Math.random()*200,t);
      g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(0.05,t+0.012); g.gain.exponentialRampToValueAtTime(0.001,t+0.14);
      o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t+0.15);
    }); rel(ctx,500);
  }

  // Route data-sound clicks
  document.addEventListener('click', function(e) {
    var el=e.target.closest('[data-sound]'); if (!el) return;
    var s=el.getAttribute('data-sound');
    if (s==='click') softClick();
    else if (s==='pop')    softPop();
    else if (s==='swoosh') softSwoosh();
    else if (s==='tick')   softTick();
  });

  // Nav item tick
  document.addEventListener('click', function(e) {
    if (e.target.closest('.default-header__nav-item')) softTick();
  });

  // $ coin ping on hover
  document.querySelectorAll('[data-donate]').forEach(function(el) {
    el.addEventListener('mouseenter', coinPing);
  });

  // ── Theme ─────────────────────────────────────────────────────────────────
  var SK='site-color-scheme', doc=document.documentElement;
  function getTheme(){ return doc.getAttribute('data-color-scheme')==='dark'?'dark':'light'; }
  function applyTheme(t){ doc.setAttribute('data-color-scheme',t); localStorage.setItem(SK,t); syncUI(t); }
  function syncUI(t) {
    var dk=t==='dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(function(b){
      var ic=b.querySelector('i'); if(ic) ic.className=dk?'ph ph-sun-dim':'ph ph-moon';
      b.setAttribute('aria-label',dk?'Switch to light mode':'Switch to dark mode');
    });
  }
  var sv=localStorage.getItem(SK);
  syncUI((sv==='light'||sv==='dark')?sv:getTheme());
  document.addEventListener('click',function(e){
    if(!e.target.closest('[data-theme-toggle]')) return;
    var next=getTheme()==='dark'?'light':'dark';
    applyTheme(next);
    if(next==='light') chimeUp(); else chimeDown();
  });

  // ── Default / Blog burger ─────────────────────────────────────────────────
  function initBurger(bid, mid) {
    var b=document.getElementById(bid), m=document.getElementById(mid), h=document.getElementById('siteHeader');
    if(!b||!m) return;
    function tog(force){
      var open=force!==undefined?force:!b.classList.contains('is-open');
      b.classList.toggle('is-open',open); b.setAttribute('aria-expanded',String(open));
      m.classList.toggle('is-open',open); m.setAttribute('aria-hidden',String(!open));
      if(h) h.classList.toggle('menu-is-open',open);
      document.body.style.overflow=open?'hidden':'';
    }
    b.addEventListener('click',function(){tog();});
    document.addEventListener('click',function(e){
      if(m.classList.contains('is-open')&&!m.contains(e.target)&&!b.contains(e.target)) tog(false);
    });
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&m.classList.contains('is-open')){tog(false);b.focus();}
    });
  }
  initBurger('defaultNavBurger','defaultNavMenu');
  initBurger('blogNavBurger','blogNavMenu');

  // ── Dropdown factory ──────────────────────────────────────────────────────
  function mkDD(btnId, panelId, wrapId) {
    var btn=document.getElementById(btnId), panel=document.getElementById(panelId), wrap=document.getElementById(wrapId);
    if(!btn||!panel) return;
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      var open=panel.hidden; panel.hidden=!open;
      btn.setAttribute('aria-expanded',String(open)); btn.classList.toggle('is-open',open);
    });
    document.addEventListener('click',function(e){
      if(wrap&&!wrap.contains(e.target)){panel.hidden=true;btn.setAttribute('aria-expanded','false');btn.classList.remove('is-open');}
    });
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&!panel.hidden){panel.hidden=true;btn.setAttribute('aria-expanded','false');btn.classList.remove('is-open');btn.focus();}
    });
  }
  mkDD('moreBtn','morePanel','moreWrap');
  mkDD('accountBtn','accountDropdown','accountWrap');

  // ── Nav dropdown builder ("- " prefix → child items) ─────────────────────
  document.addEventListener('DOMContentLoaded',function(){
    ['defaultNavLinks','blogNavLinks'].forEach(function(id){
      var nav=document.getElementById(id); if(!nav) return;
      var items=Array.from(nav.querySelectorAll('.default-header__nav-item')), cur=null;
      items.forEach(function(el){
        if(el.getAttribute('data-child')==='true'&&cur){
          var lbl=el.querySelector('.default-header__nav-label');
          if(lbl) lbl.textContent=lbl.textContent.replace(/^[-–]\s*/,'').trim();
          var li=document.createElement('li'); li.appendChild(el); cur.list.appendChild(li);
        } else {
          var wrap=document.createElement('div'); wrap.className='default-header__dropdown-wrap';
          el.parentNode.insertBefore(wrap,el); wrap.appendChild(el);
          var list=document.createElement('ul'); list.className='default-header__dropdown-menu'; list.setAttribute('role','menu');
          wrap.appendChild(list); cur={wrap:wrap,trigger:el,list:list};
        }
      });
      nav.querySelectorAll('.default-header__dropdown-wrap').forEach(function(wrap){
        var list=wrap.querySelector('.default-header__dropdown-menu');
        var item=wrap.querySelector('.default-header__nav-item');
        if(!list||!list.children.length){if(item) wrap.parentNode.insertBefore(item,wrap); wrap.remove(); return;}
        wrap.classList.add('has-dropdown');
        if(item){
          item.classList.add('has-dropdown-trigger'); item.setAttribute('aria-haspopup','true'); item.setAttribute('aria-expanded','false');
          var chev=document.createElement('i'); chev.className='ph ph-caret-down default-header__dropdown-chevron'; chev.setAttribute('aria-hidden','true');
          item.appendChild(chev);
        }
      });
      nav.addEventListener('click',function(e){
        var t=e.target.closest('.has-dropdown-trigger'); if(!t||window.innerWidth>=1024) return;
        e.preventDefault();
        var w=t.closest('.has-dropdown'), isOpen=w.classList.contains('is-open');
        nav.querySelectorAll('.has-dropdown.is-open').forEach(function(d){
          d.classList.remove('is-open'); var dt=d.querySelector('.has-dropdown-trigger'); if(dt) dt.setAttribute('aria-expanded','false');
        });
        if(!isOpen){w.classList.add('is-open');t.setAttribute('aria-expanded','true');}
      });
      document.addEventListener('click',function(e){
        if(!nav.contains(e.target)) nav.querySelectorAll('.has-dropdown.is-open').forEach(function(d){d.classList.remove('is-open');});
      });
    });
  });

  // ── Course header: right-side lesson drawer ───────────────────────────────
  (function(){
    var burger  = document.getElementById('courseBurgerBtn');
    var panel   = document.getElementById('courseLessonPanel');
    var overlay = document.getElementById('courseLessonOverlay');
    var closeBtn= document.getElementById('coursePanelClose');
    if(!panel) return;

    function openPanel(){
      panel.classList.add('is-open'); panel.setAttribute('aria-hidden','false');
      if(burger){burger.classList.add('is-open');burger.setAttribute('aria-expanded','true');}
      document.body.classList.add('course-panel-open');
      softPop();
    }
    function closePanel(){
      panel.classList.remove('is-open'); panel.setAttribute('aria-hidden','true');
      if(burger){burger.classList.remove('is-open');burger.setAttribute('aria-expanded','false');}
      document.body.classList.remove('course-panel-open');
      if(burger) burger.focus();
    }

    if(burger) burger.addEventListener('click',function(){panel.classList.contains('is-open')?closePanel():openPanel();});
    if(closeBtn) closeBtn.addEventListener('click',closePanel);
    if(overlay) overlay.addEventListener('click',closePanel);
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&panel.classList.contains('is-open')) closePanel();
    });
    document.addEventListener('DOMContentLoaded',function(){
      var a=panel.querySelector('.course-header__lesson-link.is-active');
      if(a) setTimeout(function(){a.scrollIntoView({block:'nearest',behavior:'smooth'});},50);
    });
  })();

  // ── Blog reading progress ─────────────────────────────────────────────────
  (function(){
    var fill=document.getElementById('blogReadingFill'), strip=document.getElementById('blogReadingStrip');
    if(!fill) return;
    function upd(){
      var c=document.querySelector('.gh-content,.js-post-content'), pct;
      if(c){var s=c.getBoundingClientRect().top+window.scrollY,e=s+c.offsetHeight-window.innerHeight;pct=Math.min(100,Math.max(0,Math.round(((window.scrollY-s)/Math.max(1,e-s))*100)));}
      else pct=Math.min(100,Math.round(window.scrollY/Math.max(1,document.documentElement.scrollHeight-window.innerHeight)*100));
      fill.style.width=pct+'%'; if(strip) strip.setAttribute('aria-valuenow',pct);
    }
    window.addEventListener('scroll',upd,{passive:true});
    window.addEventListener('resize',upd,{passive:true});
    upd();
  })();

})();