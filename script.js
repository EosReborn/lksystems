(function () {
  'use strict';
  var KEY = 'lk_cookie_consent';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Cookie consent ---------- */
  var banner = document.getElementById('cookie');

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      if (v && Date.now() - v.t < 365 * 864e5) return v.c;
    } catch (e) {}
    return null;
  }
  function save(choice) {
    try { localStorage.setItem(KEY, JSON.stringify({ c: choice, t: Date.now() })); } catch (e) {}
    apply(choice);
  }
  // Ide kerülhet a statisztikai szkript (pl. Google Analytics) betöltése,
  // KIZÁRÓLAG akkor, ha choice === 'all'.
  function apply(choice) {
    document.documentElement.setAttribute('data-consent', choice);
    if (choice === 'all') { /* loadAnalytics(); */ }
  }
  function show() {
    if (!banner) return;
    banner.hidden = false;
    requestAnimationFrame(function () { banner.classList.add('show'); });
  }
  function hide() {
    if (!banner) return;
    banner.classList.remove('show');
    setTimeout(function () { banner.hidden = true; }, reduce ? 0 : 300);
  }

  if (banner) {
    var saved = read();
    if (saved) apply(saved); else setTimeout(show, 600);

    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cookie]');
      if (!b) return;
      save(b.getAttribute('data-cookie'));
      hide();
    });
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-cookie-settings]')) show();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !banner.hidden && read()) hide();
    });
  }

  /* ---------- Menü bezárása navigáláskor / kattintáskor ---------- */
  var toggle = document.getElementById('menu-toggle');
  if (toggle) {
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') toggle.checked = false;
    });
    document.addEventListener('click', function (e) {
      if (toggle.checked && !e.target.closest('.nav')) toggle.checked = false;
    });
  }

  /* ---------- Fejléc árnyék görgetéskor ---------- */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Animációk ---------- */
  if (reduce || !('IntersectionObserver' in window)) return;

  // megjelenés görgetéskor
  var groups = '.grid, .stats, .chips, .logos, .why, .ticks, .facts, .split, .cta-in';
  var singles = '.section > .wrap > h2, .section > .wrap > .eyebrow, .panel, .panel-dark, .sz, .more, .note';
  var els = [];
  document.querySelectorAll(groups).forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (c, i) {
      c.classList.add('reveal');
      c.style.setProperty('--d', Math.min(i, 8) * 70 + 'ms');
      els.push(c);
    });
  });
  document.querySelectorAll(singles).forEach(function (c) {
    if (c.classList.contains('reveal') || c.closest('.reveal')) return;
    c.classList.add('reveal'); els.push(c);
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      io.unobserve(en.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  els.forEach(function (el) { io.observe(el); });

  // számláló animáció (géppark)
  var counters = document.querySelectorAll('.stats:not(.one) b');
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      cio.unobserve(en.target);
      var el = en.target, end = parseInt(el.textContent, 10);
      if (!end) return;
      var t0 = null, dur = 1200;
      (function step(t) {
        if (t0 === null) t0 = t;
        var p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      })(performance.now());
    });
  }, { threshold: 0.6 });
  counters.forEach(function (c) { cio.observe(c); });
})();
