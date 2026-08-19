/* ============================================================================
   code.js — self-contained syntax highlighter + copy button (no libraries)
   ----------------------------------------------------------------------------
   Upgrades every <pre><code> in .gh-content into the DESIGN SYSTEM's
   `.ns-code` figure — bar, line-number gutter, tokenised body — and nothing
   more. Ghost's Koenig emits a bare <pre><code class="language-x">; the system
   styles a richer structure; this is the bridge between the two.

   It does NOT handle copy or tabs. That is assets/js/ds/code.js, which wires
   [data-code="copy"] on the markup this produces.
   The scanner emits escaped text with <span class="tok-*"> wrappers; because it
   builds output left-to-right it never re-matches its own markup (the classic
   regex-highlighter bug). Languages: Apex/SOQL, JS/TS/LWC, HTML/XML, JSON,
   Bash, CSS — unknown languages fall back to a sensible default keyword set.
   ========================================================================== */
(function () {
  'use strict';

  var ICON_FILE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" class="ns-icon"><path d="M13.5 3.5H7A1.5 1.5 0 0 0 5.5 5v14A1.5 1.5 0 0 0 7 20.5h10a1.5 1.5 0 0 0 1.5-1.5V8.5Z"/><path d="M13.5 3.5v5h5"/></svg>';

  var blocks = document.querySelectorAll('.gh-content pre');
  if (!blocks.length) return;

  // ── helpers ──
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  /* The design system's token vocabulary (ds/components/css/code.css) is
     ns-tok-{kw,str,com,num,fn,type,punct}. This scanner grew its own names;
     they are mapped here rather than renamed throughout, so the scanner stays
     readable and there is exactly ONE place that knows the system's names. */
  var TOK = {
    keyword: 'kw', string: 'str', comment: 'com', number: 'num',
    function: 'fn', punct: 'punct',
    tag: 'type',   /* markup: the element name reads as a type */
    attr: 'fn'     /* markup: the attribute reads as a callable-ish name */
  };
  function span(cls, text) {
    return '<span class="ns-tok-' + (TOK[cls] || 'punct') + '">' + esc(text) + '</span>';
  }
  function toSet(str) {
    var s = {};
    str.split(/\s+/).forEach(function (w) { if (w) s[w.toLowerCase()] = true; });
    return s;
  }
  function readString(src, i) {
    var q = src[i], j = i + 1;
    while (j < src.length) {
      if (src[j] === '\\') { j += 2; continue; }
      if (src[j] === q) { j++; break; }
      j++;
    }
    return j;
  }

  // ── keyword sets ──
  var KW = {
    apex: toSet('public private protected global static final void return if else for while do try catch finally throw new this super class interface extends implements enum trigger on before after insert update delete undelete upsert merge with without sharing virtual abstract override transient testmethod system database integer string boolean decimal double long date datetime time id blob list set map sobject object instanceof select from where limit offset order by group having and or not like in asc desc count sum avg min max true false null'),
    soql: toSet('select from where and or not like in order by group having limit offset asc desc null true false count sum avg min max'),
    javascript: toSet('const let var function return if else for while do switch case break continue new this class extends super import export from default async await try catch finally throw typeof instanceof delete void yield static get set of in true false null undefined'),
    json: toSet('true false null'),
    bash: toSet('echo cd ls sudo apt npm yarn git node export source if then else fi for do done in while case esac function return'),
    css: toSet('important')
  };
  KW.js = KW.ts = KW.typescript = KW.lwc = KW.javascript;
  KW.sql = KW.soql;
  KW.sh = KW.shell = KW.console = KW.bash;
  KW.cls = KW.trigger = KW.apex;
  KW._default = toSet('public private protected static final void return if else for while do try catch finally throw new this super class interface extends implements import export from default async await const let var function switch case break continue select from where true false null');

  function isMarkup(l) { return /^(html|xml|markup|svg|hbs|handlebars|vue)$/.test(l); }

  // ── generic code scanner ──
  function highlightCode(code, lang) {
    var kw = KW[lang] || KW._default;
    var line = (lang === 'sql' || lang === 'soql') ? '--'
      : /^(bash|sh|shell|console|yaml|yml|python|py|ruby|rb)$/.test(lang) ? '#' : '//';
    var out = '', i = 0, n = code.length;
    while (i < n) {
      var ch = code[i], two = code.substr(i, 2);
      if (two === '/*') { var j = code.indexOf('*/', i); j = j < 0 ? n : j + 2; out += span('comment', code.slice(i, j)); i = j; continue; }
      if (line === '//' && two === '//') { var j = code.indexOf('\n', i); if (j < 0) j = n; out += span('comment', code.slice(i, j)); i = j; continue; }
      if (line === '--' && two === '--') { var j = code.indexOf('\n', i); if (j < 0) j = n; out += span('comment', code.slice(i, j)); i = j; continue; }
      if (line === '#' && ch === '#') { var j = code.indexOf('\n', i); if (j < 0) j = n; out += span('comment', code.slice(i, j)); i = j; continue; }
      if (ch === '"' || ch === "'" || ch === '`') { var j = readString(code, i); out += span('string', code.slice(i, j)); i = j; continue; }
      if (ch >= '0' && ch <= '9') { var m = /^[0-9][0-9a-fA-FxX._]*/.exec(code.slice(i)); out += span('number', m[0]); i += m[0].length; continue; }
      if (/[A-Za-z_$@]/.test(ch)) {
        var m = /^[A-Za-z_$@][\w$]*/.exec(code.slice(i)); var w = m[0]; i += w.length;
        var k = i; while (code[k] === ' ' || code[k] === '\t') k++;
        if (kw[w.toLowerCase()]) out += span('keyword', w);
        else if (code[k] === '(') out += span('function', w);
        else out += esc(w);
        continue;
      }
      out += esc(ch); i++;
    }
    return out;
  }

  // ── markup scanner (HTML/XML) ──
  function highlightTag(t) {
    var out = '', i = 0, n = t.length;
    out += span('punct', t[i]); i++;            // '<'
    if (t[i] === '/') { out += span('punct', '/'); i++; }
    var m = /^[\w:.-]+/.exec(t.slice(i));
    if (m) { out += span('tag', m[0]); i += m[0].length; }
    while (i < n) {
      var ch = t[i];
      if (ch === '>' || ch === '/') { out += span('punct', ch); i++; continue; }
      if (ch === '"' || ch === "'") { var j = readString(t, i); out += span('string', t.slice(i, j)); i = j; continue; }
      if (/\s/.test(ch)) { out += ch; i++; continue; }
      if (ch === '=') { out += esc('='); i++; continue; }
      var am = /^[\w:.-]+/.exec(t.slice(i));
      if (am) { out += span('attr', am[0]); i += am[0].length; continue; }
      out += esc(ch); i++;
    }
    return out;
  }
  function highlightMarkup(code) {
    var out = '', i = 0, n = code.length;
    while (i < n) {
      if (code.substr(i, 4) === '<!--') { var j = code.indexOf('-->', i); j = j < 0 ? n : j + 3; out += span('comment', code.slice(i, j)); i = j; continue; }
      if (code[i] === '<') { var j = code.indexOf('>', i); j = j < 0 ? n : j + 1; out += highlightTag(code.slice(i, j)); i = j; continue; }
      var j = code.indexOf('<', i); if (j < 0) j = n; out += esc(code.slice(i, j)); i = j;
    }
    return out;
  }

  // ── copy-to-clipboard ──
  var ICON_COPY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';

  function copyText(text, btn) {
    var label = btn.querySelector('.ns-syntax__copy-label');
    function done() {
      btn.classList.add('is-copied');
      if (label) label.textContent = 'Copied!';
      setTimeout(function () { btn.classList.remove('is-copied'); if (label) label.textContent = 'Copy'; }, 1500);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(function () { fallback(text, done); });
    } else { fallback(text, done); }
  }
  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta); done();
  }

  // ── process each block ──
  blocks.forEach(function (pre) {
    if (pre.closest('.ns-code')) return;
    var codeEl = pre.querySelector('code') || pre;
    var raw = codeEl.textContent;
    var lang = ((codeEl.className + ' ' + pre.className).match(/language-([\w-]+)/) || [])[1] || '';
    lang = lang.toLowerCase();

    codeEl.innerHTML = isMarkup(lang) ? highlightMarkup(raw) : highlightCode(raw, lang);

    /* The system's .ns-code is a <figure> with a <figcaption> bar, a line-number
       gutter and the <pre> beside it. Ghost's Koenig emits a bare
       <pre><code class="language-x">, so this upgrades one into the other —
       which is the only reason this file still exists. The BEHAVIOUR (copy,
       tabs) is the system's assets/js/ds/code.js; nothing here duplicates it. */
    var fig = document.createElement('figure');
    fig.className = 'ns-code';
    if (lang) fig.setAttribute('data-lang', lang);

    var bar = document.createElement('figcaption');
    bar.className = 'ns-code__bar';
    bar.innerHTML =
      '<span class="ns-code__file">' + ICON_FILE + '<span>' + esc(lang || 'code') + '</span></span>' +
      '<span class="ns-code__actions">' +
        (lang ? '<span class="ns-code__lang">' + esc(lang) + '</span>' : '') +
        '<button type="button" class="ns-code__btn" data-code="copy" aria-label="Copy code">' +
          ICON_COPY + '<span class="ns-code__btn-label"><span>Copy</span></span>' +
        '</button>' +
      '</span>';

    var body = document.createElement('div');
    body.className = 'ns-code__body';

    /* The gutter is aria-hidden and a separate <pre> so selecting the code
       never picks up the line numbers — the reason the system splits them. */
    var lines = raw.replace(/\n$/, '').split('\n').length;
    var gutter = document.createElement('pre');
    gutter.className = 'ns-code__gutter';
    gutter.setAttribute('aria-hidden', 'true');
    gutter.textContent = Array.from({ length: lines }, function (_, i) { return i + 1; }).join('\n');

    pre.className = 'ns-code__pre';

    pre.parentNode.insertBefore(fig, pre);
    fig.appendChild(bar);
    fig.appendChild(body);
    body.appendChild(gutter);
    body.appendChild(pre);

    /* copy is wired by the system's code.js via [data-code="copy"] */
  });
})();
