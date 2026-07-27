/* ============================================================================
   code.js — self-contained syntax highlighter + copy button (no libraries)
   ----------------------------------------------------------------------------
   Wraps every <pre><code> in .gh-content with a Salesforce Developer
   Console-style window (navy header, white file tab, copy button) and tokenises
   the source with a tiny hand-written scanner.
   The scanner emits escaped text with <span class="tok-*"> wrappers; because it
   builds output left-to-right it never re-matches its own markup (the classic
   regex-highlighter bug). Languages: Apex/SOQL, JS/TS/LWC, HTML/XML, JSON,
   Bash, CSS — unknown languages fall back to a sensible default keyword set.
   ========================================================================== */
(function () {
  'use strict';

  var blocks = document.querySelectorAll('.gh-content pre');
  if (!blocks.length) return;

  // ── helpers ──
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function span(cls, text) { return '<span class="tok-' + cls + '">' + esc(text) + '</span>'; }
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
    if (pre.closest('.ns-syntax')) return;
    var codeEl = pre.querySelector('code') || pre;
    var raw = codeEl.textContent;
    var lang = ((codeEl.className + ' ' + pre.className).match(/language-([\w-]+)/) || [])[1] || '';
    lang = lang.toLowerCase();

    codeEl.innerHTML = isMarkup(lang) ? highlightMarkup(raw) : highlightCode(raw, lang);

    var wrap = document.createElement('div');
    wrap.className = 'ns-syntax';
    var bar = document.createElement('div');
    bar.className = 'ns-syntax__bar';
    bar.innerHTML =
      '<span class="ns-syntax__name">' +
        '<svg viewBox="0 0 24 24" fill="currentColor" class="h-3.5 w-3.5"><path d="M7 19a5 5 0 0 1-.8-9.9 6 6 0 0 1 11.5-1.2A4.5 4.5 0 0 1 17.5 19H7Z"/></svg>' +
        '<span>' + (lang || 'code') + '</span>' +
      '</span>';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ns-syntax__copy';
    btn.setAttribute('aria-label', 'Copy code');
    btn.innerHTML = ICON_COPY + '<span class="ns-syntax__copy-label">Copy</span>';
    bar.appendChild(btn);

    var body = document.createElement('div');
    body.className = 'ns-syntax__body';

    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(bar);
    wrap.appendChild(body);
    body.appendChild(pre);

    btn.addEventListener('click', function () { copyText(raw, btn); });
  });
})();
