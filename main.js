/* =====================================================================
   Freehold — site script
   ===================================================================== */
(() => {
'use strict';

/* ---------------------------------------------------------------------
   CONFIG — everything you're likely to change lives here
   --------------------------------------------------------------------- */
const SITE = {
  phone: '0444 554 898',
  phoneLink: '+61444554898',
  email: 'Connor.ransome@gmail.com',
  abn: '',        // add your ABN (e.g. '12 345 678 901') and it appears in the footer
  formKey: '',    // free key from web3forms.com; blank opens the visitor's email app instead
  pricing: {
    freehold: { base: 1800, depositPct: 40 },
    managed:  { base: 499, monthly: 69, minMonths: 3 },
    includedPages: 5,
    extraPage: 150,
    tool: 350,
    ai: 29,
    hourly: 60
  }
};

/* ---------------------------------------------------------------------
   Helpers
   --------------------------------------------------------------------- */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
const money = n => '$' + Math.round(n).toLocaleString('en-AU');
const esc = t => { const d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
const page = document.body.dataset.page;
const root = document.documentElement;

/* One scroll listener, shared by everything that reacts to scroll */
const onScrollFns = [];
let ticking = false;
function onScroll(fn) { onScrollFns.push(fn); fn(); }
function runScroll() { ticking = false; onScrollFns.forEach(f => f()); }
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(runScroll); } }, { passive: true });
addEventListener('resize', () => requestAnimationFrame(runScroll));

function tween(el, to, fmt = money) {
  const from = el.dataset.v != null ? Number(el.dataset.v) : to;
  el.dataset.v = to;
  cancelAnimationFrame(el._raf);
  if (reduced || from === to) { el.textContent = fmt(to); return; }
  const t0 = performance.now(), d = 600;
  const step = now => {
    const p = Math.min((now - t0) / d, 1), e = 1 - Math.pow(1 - p, 4);
    el.textContent = fmt(from + (to - from) * e);
    if (p < 1) el._raf = requestAnimationFrame(step);
  };
  el._raf = requestAnimationFrame(step);
}

/* ---------------------------------------------------------------------
   Headings reveal word by word
   --------------------------------------------------------------------- */
function splitWords(el) {
  let i = 0;
  const walk = node => {
    Array.from(node.childNodes).forEach(c => {
      if (c.nodeType === 3) {
        const frag = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
          const wd = document.createElement('span'); wd.className = 'wd';
          const wi = document.createElement('span'); wi.className = 'wi';
          wi.style.setProperty('--i', i++);
          wi.textContent = part;
          wd.appendChild(wi); frag.appendChild(wd);
        });
        c.replaceWith(frag);
      } else if (c.nodeType === 1 && c.tagName !== 'BR') walk(c);
    });
  };
  walk(el);
  el.classList.add('split-ready');
}
$$('.split').forEach(splitWords);

function reveal() {
  const targets = $$('.split:not(.hero-split), .rise:not(.hero-rise), .figure, .cta-box');
  if (reduced || !('IntersectionObserver' in window)) { targets.forEach(t => t.classList.add('in')); return; }
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
  }), { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
  targets.forEach(t => io.observe(t));
}

/* ---------------------------------------------------------------------
   First-visit intro, then the page's own entrance
   --------------------------------------------------------------------- */
function go() {
  document.body.classList.add('go', 'ready');
  $$('.hero-split, .hero-rise').forEach(el => el.classList.add('in'));
}
(function intro() {
  const el = $('#veil');
  if (root.classList.contains('intro') && el) {
    setTimeout(go, 1900);
    setTimeout(() => { root.classList.remove('intro'); el.remove(); }, 2650);
  } else {
    if (el) el.remove();
    requestAnimationFrame(() => requestAnimationFrame(go));
  }
})();

/* ---------------------------------------------------------------------
   Nav, mobile menu, magnetic buttons, footer
   --------------------------------------------------------------------- */
function nav() {
  const bar = $('#nav');
  onScroll(() => bar.classList.toggle('solid', scrollY > 30));
  const burger = $('.burger');
  const menu = document.createElement('div');
  menu.className = 'menu'; menu.id = 'menu';
  const here = (location.pathname.split('/').pop() || 'index.html').replace('.html', '') || 'index';
  const items = [['index.html', 'Home'], ['work.html', 'Work'], ['pricing.html', 'Pricing'], ['pricing.html#quote', 'Get a quote']];
  menu.innerHTML = items.map(([u, l], i) => {
    const on = u.replace('.html', '') === here;
    return `<a href="${u}" style="transition-delay:${(0.15 + i * 0.06).toFixed(2)}s"${on ? ' aria-current="page"' : ''}>${l}</a>`;
  }).join('') + `<div class="menu-foot"><a href="tel:${SITE.phoneLink}">${esc(SITE.phone)}</a><a href="mailto:${esc(SITE.email)}">${esc(SITE.email)}</a><span>Bokarina, Sunshine Coast</span></div>`;
  document.body.appendChild(menu);
  burger.setAttribute('aria-controls', 'menu');
  const set = open => {
    root.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  burger.addEventListener('click', () => set(!root.classList.contains('menu-open')));
  addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
  $$('a', menu).forEach(a => a.addEventListener('click', () => set(false)));
}

function magnetic() {
  if (!finePointer || reduced) return;
  $$('[data-mag]').forEach(b => {
    b.addEventListener('pointermove', e => {
      const r = b.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width / 2) * 0.22, y = (e.clientY - r.top - r.height / 2) * 0.32;
      b.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
    });
    b.addEventListener('pointerleave', () => { b.style.transform = ''; });
  });
}

function footer() {
  const y = $('#year'); if (y) y.textContent = new Date().getFullYear();
  const abn = $('#abnLine'); if (abn && SITE.abn) { abn.textContent = 'ABN ' + SITE.abn; abn.hidden = false; }
  const clock = $('#clock'), note = $('#clockNote');
  if (!clock) return;
  const tick = () => {
    const parts = {};
    new Intl.DateTimeFormat('en-AU', { timeZone: 'Australia/Brisbane', weekday: 'short', hour: 'numeric', minute: '2-digit', hour12: true })
      .formatToParts(new Date()).forEach(p => { parts[p.type] = p.value; });
    clock.textContent = `${parts.hour}:${parts.minute}${String(parts.dayPeriod || '').toLowerCase()}`;
    const h = Number(new Intl.DateTimeFormat('en-AU', { timeZone: 'Australia/Brisbane', hour: 'numeric', hour12: false }).format(new Date())) % 24;
    const weekend = /Sat|Sun/.test(parts.weekday);
    note.textContent = !weekend && h >= 8 && h < 18 ? 'Probably building something. Call or text any time.' : 'Off the clock. Texts get answered first thing.';
  };
  tick(); setInterval(tick, 30000);
}

/* ---------------------------------------------------------------------
   Home — topographic terrain that rises under the cursor
   --------------------------------------------------------------------- */
function terrain() {
  const canvas = $('#topo'), hero = $('.hero');
  if (!canvas || !hero) return;
  const ctx = canvas.getContext('2d');
  const word = $('#bigword');
  const letters = word ? $$('span', word) : [];
  let W = 0, H = 0, dpr = 1, cell = 15, cols = 0, rows = 0, field = null;
  let centres = [], wdth = letters.map(() => 100);

  const hash = (x, y) => {
    let h = (Math.imul(x | 0, 374761393) + Math.imul(y | 0, 668265263)) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177); h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  };
  const fade = t => t * t * t * (t * (t * 6 - 15) + 10);
  const grad = (ix, iy, x, y) => { const a = hash(ix, iy) * 6.283185307; return Math.cos(a) * (x - ix) + Math.sin(a) * (y - iy); };
  const perlin = (x, y) => {
    const x0 = Math.floor(x), y0 = Math.floor(y), sx = fade(x - x0), sy = fade(y - y0);
    const a = grad(x0, y0, x, y), b = grad(x0 + 1, y0, x, y), c = grad(x0, y0 + 1, x, y), d = grad(x0 + 1, y0 + 1, x, y);
    const ab = a + (b - a) * sx, cd = c + (d - c) * sx;
    return ab + (cd - ab) * sy;
  };

  const fitWord = () => {
    if (!word) return;
    letters.forEach(l => { l.style.fontVariationSettings = "'wdth' 100,'wght' 800"; });
    word.style.fontSize = '100px';
    const avail = word.parentElement.clientWidth;
    const natural = letters.reduce((s, l) => s + l.offsetWidth, 0);
    word.style.fontSize = (100 * avail / natural * 0.97).toFixed(2) + 'px';
    centres = letters.map(l => l.offsetLeft + l.offsetWidth / 2);
    wdth = letters.map(() => 100);
  };

  const resize = () => {
    dpr = Math.min(2, devicePixelRatio || 1);
    const r = canvas.getBoundingClientRect();
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    cell = W < 700 ? 19 : 15;
    cols = Math.ceil(W / cell) + 1; rows = Math.ceil(H / cell) + 1;
    field = new Float32Array(cols * rows);
    fitWord();
  };

  const ptr = { x: 0, y: 0, active: 0, last: -1e9 };
  const hill = { x: 0, y: 0, amp: 0 };
  hero.addEventListener('pointermove', e => {
    const r = canvas.getBoundingClientRect();
    ptr.x = e.clientX - r.left; ptr.y = e.clientY - r.top; ptr.last = performance.now();
  });

  const lines = (L, a, b, c, d, x, y) => {
    let idx = (a > L ? 8 : 0) | (b > L ? 4 : 0) | (c > L ? 2 : 0) | (d > L ? 1 : 0);
    if (idx === 0 || idx === 15) return;
    const T = () => [x + cell * ((L - a) / (b - a)), y];
    const R = () => [x + cell, y + cell * ((L - b) / (c - b))];
    const B = () => [x + cell * ((L - d) / (c - d)), y + cell];
    const Lf = () => [x, y + cell * ((L - a) / (d - a))];
    const seg = (p, q) => { ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); };
    switch (idx) {
      case 1: case 14: seg(Lf(), B()); break;
      case 2: case 13: seg(B(), R()); break;
      case 3: case 12: seg(Lf(), R()); break;
      case 4: case 11: seg(T(), R()); break;
      case 5: seg(T(), R()); seg(Lf(), B()); break;
      case 6: case 9: seg(T(), B()); break;
      case 7: case 8: seg(Lf(), T()); break;
      case 10: seg(Lf(), T()); seg(B(), R()); break;
    }
  };

  const draw = t => {
    const idle = t - ptr.last > 2600;
    const tx = idle ? W * (0.5 + 0.34 * Math.sin(t * 0.00019)) : ptr.x;
    const ty = idle ? H * (0.46 + 0.2 * Math.sin(t * 0.00029 + 1.3)) : ptr.y;
    const tamp = idle ? 0.55 : 0.85;
    hill.x += (tx - hill.x) * 0.07; hill.y += (ty - hill.y) * 0.07; hill.amp += (tamp - hill.amp) * 0.04;
    const sig = Math.max(90, Math.min(W, H) * 0.16), s2 = 2 * sig * sig, sc = cell / 330, tt = t * 0.001;

    for (let j = 0; j < rows; j++) {
      for (let i = 0; i < cols; i++) {
        const x = i * sc, y = j * sc;
        let v = perlin(x + tt * 0.05, y + tt * 0.022) * 0.95 + perlin(x * 2.3 - tt * 0.035 + 31, y * 2.3 + tt * 0.04) * 0.35;
        const dx = i * cell - hill.x, dy = j * cell - hill.y;
        v += hill.amp * Math.exp(-(dx * dx + dy * dy) / s2);
        field[j * cols + i] = v;
      }
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = 'round';
    const glow = (a, mid) => {
      const g = ctx.createRadialGradient(hill.x, hill.y, 0, hill.x, hill.y, sig * 2.4);
      g.addColorStop(0, 'rgba(255,101,51,0.95)');
      g.addColorStop(0.32, 'rgba(255,101,51,0.7)');
      g.addColorStop(0.62, `rgba(236,239,231,${mid})`);
      g.addColorStop(1, `rgba(236,239,231,${a})`);
      return g;
    };
    const plain = glow(0.085, 0.14), index = glow(0.2, 0.26);
    for (let L = -0.6, k = 0; L < 1.5; L += 0.075, k++) {
      ctx.beginPath();
      for (let j = 0; j < rows - 1; j++) {
        const r0 = j * cols, r1 = r0 + cols;
        for (let i = 0; i < cols - 1; i++) {
          lines(L, field[r0 + i], field[r0 + i + 1], field[r1 + i + 1], field[r1 + i], i * cell, j * cell);
        }
      }
      const isIndex = k % 4 === 0;
      ctx.strokeStyle = isIndex ? index : plain;
      ctx.lineWidth = isIndex ? 1.3 : 1;
      ctx.stroke();
    }

    /* the wordmark stretches toward the high ground */
    if (word && centres.length && document.body.classList.contains('go')) {
      const wr = word.getBoundingClientRect(), cr = canvas.getBoundingClientRect();
      const hx = hill.x + cr.left - wr.left;
      const spread = Math.max(80, wr.width * 0.13);
      /* letters near the hill widen, the rest give up the same width, so the word always fits */
      const ws = letters.map((_, i) => Math.exp(-Math.pow(centres[i] - hx, 2) / (2 * spread * spread)));
      const raw = ws.map(w => 72 + 78 * w);
      const budget = letters.length * 97, spare = raw.reduce((s, t) => s + (t - 55), 0);
      const k = Math.min(1, (budget - letters.length * 55) / spare);
      letters.forEach((l, i) => {
        const target = 55 + (raw[i] - 55) * k;
        wdth[i] += (target - wdth[i]) * 0.14;
        l.style.fontVariationSettings = `'wdth' ${wdth[i].toFixed(1)},'wght' ${(640 + 260 * ws[i]).toFixed(0)}`;
      });
    }
  };

  resize();
  addEventListener('resize', resize);
  if (document.fonts) document.fonts.ready.then(fitWord);
  if (reduced) { hill.x = W * 0.62; hill.y = H * 0.45; hill.amp = 0.55; draw(0); return; }

  let visible = true, frame = 0;
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(hero);
  const loop = t => {
    if (visible && !document.hidden && (frame++ & 1) === 0) draw(t);
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
}

/* Home — the wall of work flattens as it scrolls in */
function wall() {
  const sec = $('.wall');
  if (!sec) return;
  const plane = $('.wall-plane'), rows = $$('.wall-row');
  onScroll(() => {
    const r = sec.getBoundingClientRect(), vh = innerHeight;
    const p = clamp((vh - r.top) / (vh * 1.05), 0, 1);
    const e = 1 - Math.pow(1 - p, 3);
    plane.style.setProperty('--p', reduced ? 1 : e.toFixed(4));
    const drift = reduced ? 0 : (vh - r.top) * 0.13;
    rows.forEach((row, i) => {
      const base = -(row.scrollWidth - sec.clientWidth) / 2;
      row.style.transform = `translate3d(${(base + (i % 2 ? 1 : -1) * drift).toFixed(1)}px,0,0)`;
    });
  });
}

/* Home — trades marquee; scrolling pushes it faster */
function marquee() {
  const track = $('.marq-track');
  if (!track || reduced) return;
  let x = 0, last = performance.now(), v = 0, lastY = scrollY, visible = true;
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(track.parentElement);
  const loop = now => {
    const dt = Math.min(50, now - last); last = now;
    const dy = Math.abs(scrollY - lastY); lastY = scrollY;
    v += (dy - v) * 0.08;
    if (visible) {
      x -= (0.05 + v * 0.018) * dt;
      const half = track.scrollWidth / 2;
      if (x <= -half) x += half;
      track.style.transform = `translate3d(${x.toFixed(1)}px,0,0)`;
    }
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
}

/* Home — sticky visuals that swap as each point scrolls past */
function feats() {
  const items = $$('.feat'), vis = $$('.feat-stage .fv');
  if (!items.length) return;
  const set = k => {
    items.forEach((it, i) => it.classList.toggle('on', i === k));
    vis.forEach((v, i) => { v.classList.toggle('on', i <= k); v.style.zIndex = String(i + 1); });
  };
  set(0);
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) set(items.indexOf(en.target));
  }), { rootMargin: '-45% 0px -45% 0px' });
  items.forEach(i => io.observe(i));
}

/* Home — the process pins, and scrolling moves it sideways */
function process() {
  const sec = $('.proc');
  if (!sec) return;
  const track = $('.proc-track'), steps = $$('.pstep'), fill = $('.proc-line');
  const narrow = matchMedia('(max-width: 980px)');
  onScroll(() => {
    if (narrow.matches || reduced) {
      track.style.transform = '';
      steps.forEach(s => s.classList.add('on'));
      return;
    }
    const r = sec.getBoundingClientRect(), vh = innerHeight;
    const p = clamp(-r.top / (sec.offsetHeight - vh), 0, 1);
    const maxX = Math.max(0, track.scrollWidth - innerWidth);
    const x = -p * maxX;
    track.style.transform = `translate3d(${x.toFixed(1)}px,0,0)`;
    fill.style.setProperty('--pp', p.toFixed(4));
    steps.forEach(s => s.classList.toggle('on', s.offsetLeft + x < innerWidth * 0.62));
  });
}

/* ---------------------------------------------------------------------
   Work — lot map, demo videos, tilting device stage
   --------------------------------------------------------------------- */
function work() {
  $$('.parcel').forEach(g => {
    const goTo = () => { const t = document.getElementById(g.dataset.go); if (t) t.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' }); };
    g.addEventListener('click', goTo);
    g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); goTo(); } });
  });

  $$('.laptop video').forEach(v => {
    const btn = v.parentElement.querySelector('.vtoggle');
    let userPaused = false;
    const sync = () => btn.classList.toggle('paused', v.paused);
    btn.addEventListener('click', () => {
      if (v.paused) { userPaused = false; v.play().catch(() => {}); } else { userPaused = true; v.pause(); }
    });
    v.addEventListener('play', sync); v.addEventListener('pause', sync);
    sync();
    if (reduced) return;
    new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting && !userPaused) v.play().catch(() => {});
      else if (!en.isIntersecting) v.pause();
    }), { threshold: 0.35 }).observe(v);
  });

  $$('.stage').forEach(stage => {
    const inner = $('.stage-in', stage), phone = $('.phone', stage);
    if (finePointer && !reduced) {
      stage.addEventListener('pointermove', e => {
        const r = stage.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        inner.style.transform = `rotateY(${(x * 7).toFixed(2)}deg) rotateX(${(-y * 5).toFixed(2)}deg)`;
      });
      stage.addEventListener('pointerleave', () => { inner.style.transform = ''; });
    }
    if (phone && !reduced) {
      onScroll(() => {
        const r = stage.getBoundingClientRect();
        const p = clamp((innerHeight - r.top) / (innerHeight + r.height), 0, 1);
        phone.style.setProperty('--py', ((0.5 - p) * 140).toFixed(1) + 'px');
      });
    }
  });
}

/* ---------------------------------------------------------------------
   Pricing — plan prices, estimator, quote form
   --------------------------------------------------------------------- */
function pricing() {
  const P = SITE.pricing;
  const values = {
    'freehold.base': money(P.freehold.base),
    'freehold.deposit': P.freehold.depositPct + '%',
    'managed.base': money(P.managed.base),
    'managed.monthly': money(P.managed.monthly),
    'managed.min': String(P.managed.minMonths),
    'managed.twoYears': money(P.managed.base + P.managed.monthly * 24),
    'extraPage': money(P.extraPage),
    'tool': money(P.tool),
    'ai': money(P.ai),
    'hourly': money(P.hourly),
    'pages': String(P.includedPages)
  };
  $$('[data-price]').forEach(el => { if (values[el.dataset.price]) el.textContent = values[el.dataset.price]; });

  /* estimator */
  const st = { plan: 'freehold', pages: P.includedPages, tool: false, ai: false };
  const seg = $('#planSeg'), thumb = $('.thumb', seg);
  const placeThumb = () => {
    const b = $('[aria-pressed="true"]', seg);
    if (!b) return;
    thumb.style.width = b.offsetWidth + 'px';
    thumb.style.height = b.offsetHeight + 'px';
    thumb.style.transform = `translate(${b.offsetLeft}px, 0)`;
  };
  seg.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    $$('button', seg).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    st.plan = b.dataset.plan; placeThumb(); render();
  });
  addEventListener('resize', placeThumb);
  if (document.fonts) document.fonts.ready.then(placeThumb);
  placeThumb();

  const out = $('#pagesOut'), dec = $('#pagesDec'), inc = $('#pagesInc');
  const setPages = n => { st.pages = clamp(n, 1, 15); out.textContent = st.pages; dec.disabled = st.pages <= 1; inc.disabled = st.pages >= 15; render(); };
  dec.addEventListener('click', () => setPages(st.pages - 1));
  inc.addEventListener('click', () => setPages(st.pages + 1));

  const toolSw = $('#toolSw'), aiSw = $('#aiSw');
  toolSw.addEventListener('click', () => { st.tool = !st.tool; render(); });
  aiSw.addEventListener('click', () => { if (st.plan === 'managed') { st.ai = !st.ai; render(); } });

  let summary = '';
  function render() {
    if (st.plan !== 'managed') st.ai = false;
    toolSw.setAttribute('aria-checked', String(st.tool));
    aiSw.setAttribute('aria-checked', String(st.ai));
    aiSw.disabled = st.plan !== 'managed';
    $('#aiNote').textContent = st.plan === 'managed' ? `${money(P.ai)} a month, answers questions using your prices and details` : 'Available on the Looked after plan';
    const extraPages = Math.max(0, st.pages - P.includedPages);
    const extras = extraPages * P.extraPage + (st.tool ? P.tool : 0);
    let upfront, monthly, third, thirdLabel, two, note;
    if (st.plan === 'freehold') {
      upfront = P.freehold.base + extras; monthly = 0;
      third = Math.round(upfront * P.freehold.depositPct / 100); thirdLabel = 'Deposit to book';
      two = upfront;
      note = 'Plus your domain name, usually $20 to $30 a year, paid directly to whoever you register it with.';
    } else {
      upfront = P.managed.base + extras; monthly = P.managed.monthly + (st.ai ? P.ai : 0);
      third = P.managed.minMonths; thirdLabel = 'Minimum term';
      two = upfront + monthly * 24;
      note = `Hosting and your domain are included. ${P.managed.minMonths} month minimum, then month to month.`;
    }
    tween($('#eUp'), upfront);
    tween($('#eMonth'), monthly, n => (Math.round(n) === 0 ? 'Nothing' : money(n)));
    $('#eThirdLabel').textContent = thirdLabel;
    if (st.plan === 'freehold') tween($('#eThird'), third);
    else { $('#eThird').dataset.v = ''; $('#eThird').textContent = `${third} months`; }
    tween($('#eTwo'), two);
    $('#eNote').textContent = note;
    $('#pagesNote').textContent = extraPages ? `${P.includedPages} included, then ${money(P.extraPage)} each` : `Up to ${P.includedPages} included`;
    summary = `${st.plan === 'freehold' ? 'Freehold (own it)' : 'Looked after (managed)'}, ${st.pages} page${st.pages === 1 ? '' : 's'}` +
      `${st.tool ? ', with a price or quote calculator' : ''}${st.ai ? ', with the AI assistant' : ''}. ` +
      `Estimate: ${money(upfront)} upfront${monthly ? `, then ${money(monthly)} a month` : ''}.`;
  }
  setPages(st.pages);

  $('#useEstimate').addEventListener('click', () => {
    $('#fEstimate').value = summary;
    const tag = $('#estimateTag');
    $('#estimateText').textContent = summary;
    tag.classList.remove('show'); void tag.offsetWidth; tag.classList.add('show');
    const radio = $(`#quoteForm input[name="Plan"][value="${st.plan === 'freehold' ? 'Freehold' : 'Looked after'}"]`);
    if (radio) radio.checked = true;
    $('#quote').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
  });
  $('#clearEstimate').addEventListener('click', () => { $('#fEstimate').value = ''; $('#estimateTag').classList.remove('show'); });

  $$('[data-plan-pick]').forEach(a => a.addEventListener('click', () => {
    const radio = $(`#quoteForm input[name="Plan"][value="${a.dataset.planPick}"]`);
    if (radio) radio.checked = true;
  }));

  /* quote form */
  const form = $('#quoteForm'), btn = $('#sendBtn'), err = $('#ferr');
  const done = () => {
    form.hidden = true;
    const l = $('#lodged'); l.classList.add('show');
    l.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
  };
  const fail = () => {
    btn.disabled = false; btn.textContent = 'Send it through';
    err.textContent = `That didn't send. Call or text ${SITE.phone}, or email ${SITE.email}.`;
  };
  form.addEventListener('submit', e => {
    e.preventDefault();
    err.textContent = '';
    $$('.bad', form).forEach(x => x.classList.remove('bad'));
    const name = $('#fName'), biz = $('#fBiz'), phone = $('#fPhone'), email = $('#fEmail');
    const missing = [];
    if (name.value.trim().length < 2) missing.push([name, 'your name']);
    if (biz.value.trim().length < 2) missing.push([biz, 'your business name']);
    const phoneOk = phone.value.replace(/\D/g, '').length >= 8;
    const emailOk = /\S+@\S+\.\S+/.test(email.value);
    if (!phoneOk && !emailOk) missing.push([phone, 'a phone number or email']);
    if (missing.length) {
      missing.forEach(([el]) => { void el.offsetWidth; el.classList.add('bad'); });
      missing[0][0].focus();
      const words = missing.map(m => m[1]);
      err.textContent = `Add ${words.length > 1 ? words.slice(0, -1).join(', ') + ' and ' + words[words.length - 1] : words[0]} so I can get back to you.`;
      return;
    }
    $('#fNeeds').value = $$('#needs input:checked').map(i => i.value).join(', ') || 'Not specified';
    btn.disabled = true; btn.innerHTML = '<span class="spin"></span>Sending';
    const fd = new FormData(form);
    const lines = [];
    fd.forEach((v, k) => { if (k !== 'botcheck' && v) lines.push(`${k}: ${v}`); });
    if (SITE.formKey) {
      fd.append('access_key', SITE.formKey);
      fd.append('subject', `Quote request: ${fd.get('Business')}`);
      fd.append('from_name', 'Freehold website');
      fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd })
        .then(r => r.json()).then(j => (j.success ? done() : fail())).catch(fail);
    } else {
      location.href = `mailto:${SITE.email}?subject=${encodeURIComponent('Quote request: ' + fd.get('Business'))}&body=${encodeURIComponent(lines.join('\n'))}`;
      setTimeout(done, 800);
    }
  });
}

/* ---------------------------------------------------------------------
   Start
   --------------------------------------------------------------------- */
nav();
magnetic();
footer();
reveal();
if (page === 'home') { terrain(); wall(); marquee(); feats(); process(); }
if (page === 'work') work();
if (page === 'pricing') pricing();

})();
