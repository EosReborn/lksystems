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

  /* ---------- Hamburger menü ---------- */
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.burger');
  function setMenu(open) {
    if (!nav || !burger) return;
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Menü bezárása' : 'Menü megnyitása');
  }
  if (burger) {
    burger.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); burger.focus(); } });
    document.addEventListener('click', function (e) { if (!e.target.closest('.nav')) setMenu(false); });
    nav.querySelectorAll('.links a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    window.matchMedia('(min-width: 1081px)').addEventListener('change', function () { setMenu(false); });
  }

  /* ---------- Fejléc árnyék görgetéskor ---------- */
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- IT animáció: hálózati topológia adatcsomagokkal ---------- */
  document.querySelectorAll('.hero, .page-hero').forEach(function (host) {
    var cv = document.createElement('canvas');
    cv.className = 'netfx'; cv.setAttribute('aria-hidden', 'true');
    host.insertBefore(cv, host.firstChild);
    var ctx = cv.getContext('2d');
    var W, H, dpr, nodes = [], packets = [], running = false, raf = 0, LINK;

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = host.clientWidth; H = host.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      LINK = W < 640 ? 110 : 150;
      var n = Math.max(14, Math.min(54, Math.round(W * H / 15000)));
      nodes = [];
      for (var i = 0; i < n; i++) {
        nodes.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25,
          r: Math.random() < .18 ? 3.6 : 2.2,   // ritkán "szerver" (nagyobb) csomópont
          hub: Math.random() < .18
        });
      }
      packets = [];
    }

    function frame(move) {
      ctx.clearRect(0, 0, W, H);
      var i, j, a, b, d, links = [];
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        if (move) {
          a.x += a.vx; a.y += a.vy;
          if (a.x < 0 || a.x > W) a.vx *= -1;
          if (a.y < 0 || a.y > H) a.vy *= -1;
        }
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j];
          d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < LINK) {
            links.push([a, b]);
            ctx.strokeStyle = 'rgba(108,192,245,' + (0.6 * (1 - d / LINK)).toFixed(3) + ')';
            ctx.lineWidth = 1.2;
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        ctx.fillStyle = a.hub ? 'rgba(143,208,251,.95)' : 'rgba(160,214,252,.9)';
        if (a.hub) {           // szerver: kis négyzet halo-val
          ctx.shadowColor = 'rgba(108,192,245,.9)'; ctx.shadowBlur = 10;
          ctx.fillRect(a.x - a.r, a.y - a.r, a.r * 2, a.r * 2); ctx.shadowBlur = 0;
        } else { ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill(); }
      }
      if (!move) return;
      // adatcsomagok a kapcsolatokon
      if (links.length && packets.length < 14 && Math.random() < .07) {
        var l = links[(Math.random() * links.length) | 0];
        packets.push({ a: l[0], b: l[1], t: 0, s: .012 + Math.random() * .014, c: Math.random() < .25 ? '#ffffff' : '#8fd0fb' });
      }
      for (i = packets.length - 1; i >= 0; i--) {
        var p = packets[i]; p.t += p.s;
        if (p.t >= 1 || Math.hypot(p.a.x - p.b.x, p.a.y - p.b.y) > LINK) { packets.splice(i, 1); continue; }
        var x = p.a.x + (p.b.x - p.a.x) * p.t, y = p.a.y + (p.b.y - p.a.y) * p.t;
        ctx.shadowColor = p.c; ctx.shadowBlur = 12; ctx.fillStyle = p.c;
        ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 6.283); ctx.fill(); ctx.shadowBlur = 0;
      }
    }

    function loop() { if (!running) return; frame(true); raf = requestAnimationFrame(loop); }
    function start() { if (reduce || running) return; running = true; loop(); }
    function stop() { running = false; cancelAnimationFrame(raf); }

    size(); frame(false);
    var rt; window.addEventListener('resize', function () {
      clearTimeout(rt); rt = setTimeout(function () { size(); frame(false); }, 150);
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { en[0].isIntersecting ? start() : stop(); }).observe(host);
    } else start();
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
  });

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
