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
  email: 'connor@freeholdweb.com.au',
  pricing: {
    freehold: { price: 1500, depositPct: 40 },                       // one-off build: deposit to book, balance before go-live
    managed:  { start: 450, depositPct: 30, monthly: 99, changesPerMonth: 3 },   // subscription: balance is paid with the first monthly fee
    includedPages: 5,
    extraPage: 100,
    hourly: 75
  }
};

/* ---------------------------------------------------------------------
   Helpers
   --------------------------------------------------------------------- */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
const lerp = (a, b, t) => a + (b - a) * t;
const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const money = n => '$' + Math.round(n).toLocaleString('en-AU');
const esc = t => { const d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; };
const reduced = document.documentElement.classList.contains('calm');
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

function tween(el, to, fmt = money, d = 600) {
  const from = el.dataset.v != null ? Number(el.dataset.v) : to;
  el.dataset.v = to;
  cancelAnimationFrame(el._raf);
  if (reduced || from === to) { el.textContent = fmt(to); return; }
  const t0 = performance.now();
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
  }), { threshold: 0, rootMargin: '0px 0px -12% 0px' });
  targets.forEach(t => io.observe(t));
}

/* ---------------------------------------------------------------------
   First-visit intro, then the page's own entrance
   --------------------------------------------------------------------- */
const entered = [];
function go() {
  document.body.classList.add('go', 'ready');
  $$('.hero-split, .hero-rise').forEach(el => el.classList.add('in'));
  entered.forEach(f => f());
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

/* The page-change reveal spreads from where you clicked */
document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('a[href]');
  if (!a || a.target === '_blank' || e.defaultPrevented) return;
  let u; try { u = new URL(a.href, location.href); } catch (x) { return; }
  if (u.origin !== location.origin || u.pathname === location.pathname) return;
  try { sessionStorage.setItem('fh-from', JSON.stringify([(e.clientX / innerWidth || 0.5).toFixed(3), (e.clientY / innerHeight || 0.5).toFixed(3)])); } catch (x) {}
}, true);

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

/* Footer — the wordmark stretches toward your cursor, and the letters
   near it light up. Letters near the cursor widen while the rest give up
   the same width, so the word always fits. */
function footword() {
  const word = $('#footword');
  if (!word) return;
  const letters = $$('span', word), foot = word.closest('footer');
  let centres = [], wdth = letters.map(() => 100), k = letters.map(() => 0);
  const fit = () => {
    letters.forEach(l => { l.style.fontVariationSettings = "'wdth' 100,'wght' 800"; });
    word.style.fontSize = '100px';
    const natural = letters.reduce((s, l) => s + l.offsetWidth, 0);
    word.style.fontSize = (100 * word.clientWidth / natural * 0.96).toFixed(2) + 'px';
    centres = letters.map(l => l.offsetLeft + l.offsetWidth / 2);
    wdth = letters.map(() => 100);
  };
  fit();
  addEventListener('resize', fit);
  if (document.fonts) document.fonts.ready.then(fit);
  if (reduced) return;
  const ptr = { x: -1, on: false, last: -1e9 };
  foot.addEventListener('pointermove', e => { const r = word.getBoundingClientRect(); ptr.x = e.clientX - r.left; ptr.on = true; ptr.last = performance.now(); });
  foot.addEventListener('pointerleave', () => { ptr.on = false; });
  let visible = false, raf = 0, sx = 0;
  const loop = t => {
    raf = 0;
    if (!visible) return;
    const idle = !ptr.on || t - ptr.last > 2600;
    const w = word.clientWidth;
    const tx = idle ? w * (0.5 + 0.42 * Math.sin(t * 0.0005)) : ptr.x;
    sx += (tx - sx) * 0.08;
    const spread = Math.max(70, w * 0.12);
    const ws = letters.map((_, i) => Math.exp(-Math.pow(centres[i] - sx, 2) / (2 * spread * spread)));
    const raw = ws.map(v => 72 + 78 * v);
    const budget = letters.length * 97, spare = raw.reduce((s, v) => s + (v - 55), 0);
    const kk = Math.min(1, (budget - letters.length * 55) / spare);
    letters.forEach((l, i) => {
      const target = 55 + (raw[i] - 55) * kk;
      wdth[i] += (target - wdth[i]) * 0.14;
      k[i] += ((idle ? 0.35 : 1) * ws[i] - k[i]) * 0.12;
      l.style.fontVariationSettings = `'wdth' ${wdth[i].toFixed(1)},'wght' ${(640 + 260 * ws[i]).toFixed(0)}`;
      l.style.setProperty('--k', k[i].toFixed(3));
    });
    raf = requestAnimationFrame(loop);
  };
  new IntersectionObserver(es => {
    visible = es[0].isIntersecting;
    if (visible && !raf) raf = requestAnimationFrame(loop);
  }).observe(word);
}

/* ---------------------------------------------------------------------
   Home — topographic terrain that rises under the cursor
   --------------------------------------------------------------------- */
function terrain() {
  const canvas = $('#topo'), area = $('#stage');
  if (!canvas || !area) return;
  const ctx = canvas.getContext('2d');
  let W = 0, H = 0, dpr = 1, cell = 15, cols = 0, rows = 0, field = null;

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

  const resize = () => {
    dpr = Math.min(2, devicePixelRatio || 1);
    const r = canvas.getBoundingClientRect();
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    cell = W < 700 ? 19 : 15;
    cols = Math.ceil(W / cell) + 1; rows = Math.ceil(H / cell) + 1;
    field = new Float32Array(cols * rows);
  };

  const ptr = { x: 0, y: 0, last: -1e9 };
  const hill = { x: 0, y: 0, amp: 0 };
  area.addEventListener('pointermove', e => {
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
  };

  resize();
  addEventListener('resize', resize);
  if (reduced) { hill.x = W * 0.3; hill.y = H * 0.45; hill.amp = 0.55; draw(0); addEventListener('resize', () => draw(0)); return; }

  let visible = true, frame = 0;
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(canvas);
  const loop = t => {
    if (visible && !document.hidden && (frame++ & 1) === 0) draw(t);
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
}

/* ---------------------------------------------------------------------
   Home — the stage: a website built like a house on its own block.
   It builds itself as the page opens, comes apart into its layers as you
   scroll past the cards, and goes back together before you leave it.
   --------------------------------------------------------------------- */
const TRADES = {
  kingpin: { item: 'Logbook service', a: '$289', b: '$299', who: 'Leah, Buderim', want: 'Wants a logbook service on Friday', g: 'Mechanic in Kunda Park' },
  tessera: { item: 'Splashback, from', a: '$890', b: '$940', who: 'Sam, Sippy Downs', want: 'Wants a bathroom retiled', g: 'Tiler in Brendale' },
  hush: { item: 'Regular clean, from', a: '$149', b: '$159', who: 'Priya, Mooloolaba', want: 'Wants a fortnightly clean', g: 'Home cleaner in Annerley' }
};
function stage() {
  const st = $('#stage'), build = $('#build');
  if (!st || !build) return;
  const pin = $('.stage-pin', st), leader = $('#leader');
  const cards = $$('.lcard', st), layers = $$('.bl', build), anchors = layers.map(l => $('.b-anchor', l));
  const lpath = leader ? $('path', leader) : null, ldots = leader ? $$('circle', leader) : [];
  const narrow = matchMedia('(max-width: 980px)');
  const edit = $('.b-edit', build), mail = $('.b-mail', build);
  const shots = $$('.b-shot', build), wipe = $('.b-wipe', build), chips = $$('.tchip', st);
  const order = shots.map(s => s.dataset.k);

  /* camera and explode state (eased toward targets every frame) */
  const cam = { e: 0, rx: 57, rz: -36, tx: 0, ty: 0 };
  const want = { e: 0, rx: 57, rz: -36, tx: 0, ty: 0 };
  let box = { w: 1, h: 1 }, focus = -1, visible = true, raf = 0;

  const measure = () => { box = { w: build.clientWidth, h: build.clientHeight }; };
  measure();
  addEventListener('resize', () => { measure(); kick(); });

  /* how far apart the layers are, from the scroll position */
  const fromScroll = () => {
    const r = st.getBoundingClientRect(), vh = innerHeight;
    const top = narrow.matches ? pin.offsetHeight : 0;
    /* apart once the hero scrolls away, back together as the last card leaves */
    const last = cards[cards.length - 1].getBoundingClientRect();
    const down = clamp((last.bottom - top) / (vh * 0.4), 0, 1);
    let up;
    if (narrow.matches) {
      const hr = $('.hero', st).getBoundingClientRect();
      up = clamp((top + 40 - hr.top) / (hr.height * 0.9), 0, 1);
    } else up = clamp(-r.top / (vh * 0.85), 0, 1);
    want.e = reduced ? (up > 0.5 && down > 0.5 ? 1 : 0) : ease(up) * ease(down);
    /* the card nearest the middle of what's visible picks the layer in focus */
    const mid = narrow.matches ? (pin.offsetHeight + vh) / 2 : vh * 0.5;
    let best = -1, bestD = vh * 0.32;
    if (want.e > 0.6) cards.forEach((c, i) => {
      const cr = c.getBoundingClientRect(), d = Math.abs(cr.top + cr.height / 2 - mid);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best !== focus) {
      focus = best;
      cards.forEach((c, i) => c.classList.toggle('on', i === focus));
      layers.forEach((l, i) => l.classList.toggle('is-f', i === focus));
      build.classList.toggle('has-f', focus >= 0);
    }
    kick();
  };

  /* a gentle tilt toward the pointer */
  if (finePointer && !reduced) {
    st.addEventListener('pointermove', e => {
      want.tx = e.clientX / innerWidth - 0.5; want.ty = e.clientY / innerHeight - 0.5; kick();
    });
    st.addEventListener('pointerleave', () => { want.tx = 0; want.ty = 0; kick(); });
  }

  const apply = () => {
    const e = cam.e;
    const rx = lerp(50, 62, e) - cam.ty * 4, rz = lerp(-36, -31, e) + cam.tx * 7;
    const sm = narrow.matches;
    const natW = lerp(sm ? 800 : 820, sm ? 840 : 920, e), natH = lerp(sm ? 520 : 560, sm ? 800 : 860, e);
    const sc = Math.min(box.w / natW, box.h / natH) * (sm ? 0.98 : 1);
    const wy = lerp(sm ? 26 : 30, sm ? 175 : 195, e) * sc;
    build.style.setProperty('--e', e.toFixed(4));
    build.style.setProperty('--rx', rx.toFixed(2) + 'deg');
    build.style.setProperty('--rz', rz.toFixed(2) + 'deg');
    build.style.setProperty('--sc', sc.toFixed(4));
    build.style.setProperty('--wy', wy.toFixed(1) + 'px');
    build.classList.toggle('apart', e > 0.2);
    leaderLine();
  };

  const leaderLine = () => {
    if (!leader || !lpath) return;
    const on = focus >= 0 && !narrow.matches;
    leader.classList.toggle('on', on);
    if (!on) return;
    const c = cards[focus].getBoundingClientRect(), a = anchors[focus].getBoundingClientRect(), p = pin.getBoundingClientRect();
    const x1 = c.right - p.left, y1 = c.top + Math.min(c.height / 2, 60) - p.top;
    const x2 = a.left - p.left, y2 = a.top - p.top;
    const xm = Math.min(x2 - 20, x1 + Math.max(24, (x2 - x1) * 0.35));
    lpath.setAttribute('d', `M${x1.toFixed(1)} ${y1.toFixed(1)}H${xm.toFixed(1)}L${x2.toFixed(1)} ${y2.toFixed(1)}`);
    ldots.forEach(d => { d.setAttribute('cx', x2.toFixed(1)); d.setAttribute('cy', y2.toFixed(1)); });
  };

  const loop = () => {
    raf = 0;
    const k = reduced ? 1 : 0.11;
    let moving = false;
    for (const key of ['e', 'tx', 'ty']) {
      const d = want[key] - cam[key];
      if (Math.abs(d) > 0.0005) { cam[key] += d * k; moving = true; } else cam[key] = want[key];
    }
    apply();
    if (moving && visible) raf = requestAnimationFrame(loop);
  };
  function kick() { if (!raf) raf = requestAnimationFrame(loop); }
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) kick(); }).observe(pin);
  onScroll(fromScroll);
  apply();

  /* the finish: switch trades, with the editor and the inbox following along */
  let cur = 0, auto = !reduced, timers = [];
  const later = (fn, ms) => { const id = setTimeout(() => { timers = timers.filter(t => t !== id); fn(); }, ms); timers.push(id); };
  const fill = k => {
    const t = TRADES[k];
    $$('[data-f]', build).forEach(el => { if (t[el.dataset.f] != null) el.textContent = t[el.dataset.f]; });
  };
  const setTrade = (i, animate) => {
    const k = order[i];
    shots.forEach((s, j) => {
      s.classList.toggle('was', j === cur && j !== i && animate);
      s.classList.toggle('on', j === i);
      if (!animate) s.classList.remove('was');
    });
    if (animate && wipe) { wipe.classList.remove('go'); void wipe.offsetWidth; wipe.classList.add('go'); }
    chips.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.k === k)));
    cur = i;
    edit.classList.remove('typing', 'changed', 'pressed', 'published');
    fill(k);
  };
  /* one round of "change a price, publish, a new enquiry lands" */
  const round = () => {
    later(() => edit.classList.add('typing'), 900);
    later(() => edit.classList.add('changed'), 1700);
    later(() => { edit.classList.remove('typing'); edit.classList.add('pressed'); }, 2400);
    later(() => { edit.classList.remove('pressed'); edit.classList.add('published'); }, 2650);
    later(() => { mail.classList.remove('ping'); void mail.offsetWidth; mail.classList.add('ping'); }, 3200);
    later(() => { if (auto && visible && !document.hidden) { setTrade((cur + 1) % order.length, true); round(); } else idleWait(); }, 6200);
  };
  const idleWait = () => later(() => { if (auto && visible && !document.hidden) { setTrade((cur + 1) % order.length, true); round(); } else idleWait(); }, 1500);
  chips.forEach(c => c.addEventListener('click', () => {
    auto = false;
    timers.forEach(clearTimeout); timers = [];
    const i = order.indexOf(c.dataset.k);
    if (i !== cur) setTrade(i, !reduced); else edit.classList.remove('typing', 'changed', 'pressed', 'published');
    if (!reduced) round();
    else edit.classList.add('changed', 'published');
  }));
  fill(order[0]);

  /* the build itself, as the page opens */
  if (reduced) { build.classList.remove('wait'); edit.classList.add('changed', 'published'); return; }
  let quick = false;
  try { quick = sessionStorage.getItem('fh-built') === '1'; sessionStorage.setItem('fh-built', '1'); } catch (e) {}
  const bt = quick ? 0.55 : 1;
  build.style.setProperty('--bt', bt);
  entered.push(() => {
    build.classList.add('play');
    build.classList.remove('wait');
    setTimeout(() => { build.classList.remove('play'); if (auto) round(); }, 3900 * bt);
  });
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

  $$('.stage-dev').forEach(stage => {
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
   Pricing — plan prices and the quote form
   --------------------------------------------------------------------- */
/* Every price on the site comes from SITE.pricing */
function prices() {
  const P = SITE.pricing, own = P.freehold, sub = P.managed;
  const part = (amt, pct) => Math.round(amt * pct / 100);
  const num = {
    'freehold.price': own.price,
    'freehold.deposit': part(own.price, own.depositPct),
    'freehold.balance': own.price - part(own.price, own.depositPct),
    'managed.start': sub.start,
    'managed.deposit': part(sub.start, sub.depositPct),
    'managed.balance': sub.start - part(sub.start, sub.depositPct),
    'managed.monthly': sub.monthly,
    'managed.firstYear': sub.start + sub.monthly * 12,
    'extraPage': P.extraPage,
    'hourly': P.hourly
  };
  const text = {
    'freehold.depositPct': own.depositPct + '%',
    'managed.depositPct': sub.depositPct + '%',
    'changes': String(sub.changesPerMonth),
    'pages': String(P.includedPages)
  };
  $$('[data-price]').forEach(el => {
    const k = el.dataset.price;
    if (num[k] != null) { el.textContent = money(num[k]); el.dataset.n = num[k]; }
    else if (text[k] != null) el.textContent = text[k];
  });
}

function pricing() {
  $$('[data-plan-pick]').forEach(a => a.addEventListener('click', () => {
    const radio = $(`#quoteForm input[name="Plan"][value="${a.dataset.planPick}"]`);
    if (radio) radio.checked = true;
  }));
  try {
    const picked = sessionStorage.getItem('fh-plan');
    if (picked) {
      const radio = $(`#quoteForm input[name="Plan"][value="${picked}"]`);
      if (radio) radio.checked = true;
      sessionStorage.removeItem('fh-plan');
    }
  } catch (e) {}

  /* quote form: sent to Netlify Forms without leaving the page */
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
    $('#fNeeds').value = $$('#needs input:checked').map(i => i.value).join(', ');
    btn.disabled = true; btn.innerHTML = '<span class="spin"></span>Sending';
    const fd = new FormData(form);
    const val = k => String(fd.get(k) || '').trim();
    const need = val('What would help'), plan = val('Plan'), when = val('When');
    const where = [val('Trade'), val('Suburb')].filter(Boolean).join(', ');
    const wants = [plan && plan !== 'Not sure yet' ? plan + ' plan' : '', need.toLowerCase()].filter(Boolean).join(', ');
    const contact = [val('Name'), val('Phone') || val('email')].filter(Boolean).join(', ');
    fd.set('Summary', `${val('Business')}${where ? ' (' + where + ')' : ''}. ${wants ? 'Wants: ' + wants + '. ' : ''}${when ? 'Timing: ' + when.toLowerCase() + '. ' : ''}Contact: ${contact}.`);
    fd.set('subject', `Quote request: ${val('Business')}${plan && plan !== 'Not sure yet' ? ' (' + plan + ')' : ''}`);
    const body = new URLSearchParams();
    body.set('form-name', 'quote');
    fd.forEach((v, k) => { if (k === 'botcheck' || String(v).trim() !== '') body.set(k, v); });   // blank answers are left out of the email
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString()
    }).then(r => (r.ok ? done() : fail())).catch(fail);
  });
}

/* ---------------------------------------------------------------------
   Animations: calm by default where the device asks for it, with a
   visible switch so anyone can choose for themselves
   --------------------------------------------------------------------- */
function motion() {
  const calm = root.classList.contains('calm'), pref = root.classList.contains('prefers-calm');
  const choose = v => { try { localStorage.setItem('fh-motion', v); } catch (e) {} location.reload(); };
  const btn = $('#motionToggle');
  if (btn) {
    btn.hidden = false;
    btn.textContent = calm ? 'Turn animations on' : 'Reduce animations';
    btn.addEventListener('click', () => choose(calm ? 'full' : 'calm'));
  }
  let stored = null, dismissed = false;
  try { stored = localStorage.getItem('fh-motion'); dismissed = sessionStorage.getItem('fh-pill') === '1'; } catch (e) {}
  if (!(calm && pref && stored !== 'calm' && !dismissed)) return;
  const pill = document.createElement('div');
  pill.className = 'motion-pill';
  pill.setAttribute('role', 'region');
  pill.setAttribute('aria-label', 'Animation setting');
  pill.innerHTML = '<span>Animations are reduced on this device.</span><button type="button" class="mp-on">Show them</button><button type="button" class="mp-x" aria-label="Dismiss">&times;</button>';
  document.body.appendChild(pill);
  requestAnimationFrame(() => requestAnimationFrame(() => pill.classList.add('show')));
  $('.mp-on', pill).addEventListener('click', () => choose('full'));
  $('.mp-x', pill).addEventListener('click', () => { try { sessionStorage.setItem('fh-pill', '1'); } catch (e) {} pill.remove(); });
}

/* ---------------------------------------------------------------------
   Start
   --------------------------------------------------------------------- */
nav();
magnetic();
footer();
footword();
reveal();
prices();
motion();
$$('a[data-plan-pick][href*="pricing.html"]').forEach(a => a.addEventListener('click', () => { try { sessionStorage.setItem('fh-plan', a.dataset.planPick); } catch (e) {} }));
if (page === 'home') { terrain(); stage(); wall(); marquee(); feats(); process(); }
if (page === 'work') work();
if (page === 'pricing') pricing();

})();
