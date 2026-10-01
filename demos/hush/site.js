/* =====================================================================
   Hush Home Cleaning — one script shared by every page
   ===================================================================== */
(() => {
'use strict';

/* ---------------------------------------------------------------------
   CONFIG — the two things you change per client
   --------------------------------------------------------------------- */
const CONFIG = {
  // Free key from https://web3forms.com (no account needed). Paste it here and
  // booking requests arrive by email. Leave blank to fall back to the visitor's
  // own email app.
  FORM_ACCESS_KEY: '',
  FALLBACK_EMAIL: ''  /* portfolio copy: forms show success without sending */
};

/* Used only if content.json can't be reached (e.g. opening a file directly). */
const DEFAULT_CONTENT = {
  "business": {
    "name": "Hush Home Cleaning",
    "shortName": "hush",
    "suburb": "West End QLD",
    "established": "2016",
    "phone": "(07) 3844 7160",
    "phoneLink": "+61738447160",
    "email": "hello@hushhomecleaning.com.au",
    "addressLine1": "3/88 Boundary Street",
    "addressLine2": "West End QLD 4101",
    "abn": "38 611 520 947",
    "insurance": "$10 million public liability",
    "responseTime": "We confirm every booking by text within two hours, during office hours."
  },

  "hero": {
    "headline": "Come home to a house that's already done.",
    "lede": "Police-checked home cleaners across Brisbane's inner south. The same person every visit, a price you can see right now, and nothing to sign.",
    "stats": [
      { "value": "4.9", "label": "from 612 Google reviews" },
      { "value": "94%", "label": "of visits by your regular cleaner" },
      { "value": "48 hours", "label": "to ask for a free re-clean" },
      { "value": "No", "label": "contracts or lock-in" }
    ]
  },

  "worries": [
    { "q": "Will it be the same person each time?", "a": "Yes. You get one regular cleaner, plus a named backup who has already been to your home, for when they're on leave. Last year 94% of our visits were done by the customer's regular cleaner." },
    { "q": "Can I trust them in my house?", "a": "Every cleaner is a Hush employee, not a subcontractor. Each one has a current national police check, two references we've actually called, and two weeks of paid training before they work alone." },
    { "q": "Do I need to be home?", "a": "Most of our customers aren't. Leave a key in a lockbox, give us a door code, or keep a key with us. We text when we arrive and again when we've locked up." },
    { "q": "What if something gets missed?", "a": "Tell us within 48 hours and we'll come back and redo it, free. We don't argue about whether it counts." },
    { "q": "What if something gets broken?", "a": "It's rare, but it happens. We carry $10 million in public liability, and you'll hear about it from us before you find it yourself." },
    { "q": "Am I locked into anything?", "a": "No. Skip a visit, pause for a holiday or stop altogether with 48 hours' notice. We'd rather keep you because you're happy." }
  ],

  "steps": [
    { "title": "Get your price", "text": "Choose your home size and how often. The number you see here is the number on your invoice." },
    { "title": "Pick your days", "text": "Tell us which days suit and how we'll get in. We confirm by text, usually within two hours." },
    { "title": "Meet your cleaner", "text": "The first visit runs a little longer while we bring the house up to a proper baseline." },
    { "title": "Then it just happens", "text": "Same person, same day, same standard. Skip or pause any visit by replying to a text." }
  ],

  "guarantees": [
    { "title": "Free re-clean within 48 hours", "text": "If anything on the checklist isn't right, tell us within 48 hours and we'll come back and fix it at no cost." },
    { "title": "Bond back guarantee", "text": "End of lease cleans come with 72 hours of cover. If your agent flags something we were meant to clean, we return and sort it out, free." }
  ],

  "services": [
    {
      "key": "regular",
      "name": "Regular clean",
      "tagline": "Keeps a clean house clean.",
      "for": "Weekly, fortnightly or monthly visits for homes that are already in reasonable shape.",
      "time": "2 to 3 hours for most homes",
      "points": [
        "Kitchen benches, sink, stovetop and appliance fronts",
        "Bathrooms scrubbed and toilets sanitised",
        "Floors vacuumed and mopped throughout",
        "Every reachable surface dusted",
        "Beds made and bins emptied"
      ]
    },
    {
      "key": "deep",
      "name": "Deep clean",
      "tagline": "For first visits, spring cleans, or when life got busy.",
      "for": "A top-to-bottom reset. Most regular customers start with one of these.",
      "time": "4 to 6 hours, usually with two cleaners",
      "points": [
        "Everything in a regular clean",
        "Skirting boards, door frames and light switches",
        "Inside the microwave and range hood filters",
        "Shower screens de-scaled and grout scrubbed",
        "Under and behind furniture we can move"
      ]
    },
    {
      "key": "endOfLease",
      "name": "End of lease clean",
      "tagline": "Built around your agent's exit checklist.",
      "for": "Moving out of a rental and want your full bond back without a second trip.",
      "time": "5 to 8 hours with two cleaners",
      "points": [
        "Everything in a deep clean",
        "Inside the oven, cupboards and drawers",
        "Interior windows, tracks and sills",
        "Walls spot-cleaned and marks removed",
        "Bond back guarantee for 72 hours"
      ]
    }
  ],

  "pricing": {
    "services": {
      "regular":    { "label": "Regular clean",      "base": 69,  "perBedroom": 22, "perBathroom": 29, "baseHours": 1.25, "hoursPerBedroom": 0.35, "hoursPerBathroom": 0.5 },
      "deep":       { "label": "Deep clean",         "base": 119, "perBedroom": 42, "perBathroom": 48, "baseHours": 2.5,  "hoursPerBedroom": 0.6,  "hoursPerBathroom": 0.8 },
      "endOfLease": { "label": "End of lease clean", "base": 179, "perBedroom": 68, "perBathroom": 62, "baseHours": 3,    "hoursPerBedroom": 0.8,  "hoursPerBathroom": 1 }
    },
    "frequencies": [
      { "key": "weekly",      "label": "Weekly",      "discount": 15 },
      { "key": "fortnightly", "label": "Fortnightly", "discount": 10 },
      { "key": "monthly",     "label": "Monthly",     "discount": 5 },
      { "key": "once",        "label": "Just once",   "discount": 0 }
    ],
    "extras": [
      { "key": "oven",      "label": "Inside the oven",             "price": 65, "hours": 1,    "includedIn": ["endOfLease"] },
      { "key": "fridge",    "label": "Inside the fridge",           "price": 40, "hours": 0.5,  "includedIn": ["endOfLease"] },
      { "key": "windows",   "label": "Interior windows and tracks", "price": 55, "hours": 1,    "includedIn": ["endOfLease"] },
      { "key": "cupboards", "label": "Inside kitchen cupboards",    "price": 50, "hours": 0.75, "includedIn": ["endOfLease"] },
      { "key": "walls",     "label": "Wall spot-cleaning",          "price": 40, "hours": 0.75, "includedIn": ["endOfLease"] },
      { "key": "balcony",   "label": "Balcony or patio",            "price": 45, "hours": 0.5,  "includedIn": ["deep", "endOfLease"] },
      { "key": "blinds",    "label": "Blinds, slat by slat",        "price": 35, "hours": 0.75, "includedIn": [] },
      { "key": "linen",     "label": "Fresh linen on the beds",     "price": 15, "hours": 0.25, "includedIn": [] },
      { "key": "dishes",    "label": "Dishes done and put away",    "price": 20, "hours": 0.25, "includedIn": [] },
      { "key": "washing",   "label": "A load of washing hung out",  "price": 20, "hours": 0.25, "includedIn": [] }
    ],
    "minimum": 129,
    "promise": "The price here is the price on your invoice. The only exception is a home that's much bigger or messier than described, and we'll tell you before we start, never after."
  },

  "rooms": [
    {
      "key": "kitchen", "name": "Kitchen",
      "regular": ["Benchtops wiped and sanitised", "Sink and taps scrubbed and polished", "Stovetop degreased", "Appliance fronts wiped", "Splashback cleaned", "Floor vacuumed and mopped", "Bins emptied and relined"],
      "deep": ["Inside the microwave", "Range hood filters degreased", "Cupboard doors and handles wiped", "Kickboards and under the edges"],
      "endOfLease": ["Inside the oven and trays", "Inside every cupboard and drawer", "Inside the fridge, once it's emptied", "Dishwasher filter and seals"]
    },
    {
      "key": "living", "name": "Living areas",
      "regular": ["Shelves, tables and surfaces dusted", "Cushions straightened and throws folded", "Floors vacuumed, hard floors mopped", "Mirrors and glass polished", "Rubbish taken out"],
      "deep": ["Skirting boards wiped", "Doors and door frames spot-cleaned", "Under and behind movable furniture", "Blinds dusted", "Sofa vacuumed, under the cushions too"],
      "endOfLease": ["Walls spot-cleaned", "Interior windows, tracks and sills", "Light fittings dusted", "Air conditioner vents wiped"]
    },
    {
      "key": "bedrooms", "name": "Bedrooms",
      "regular": ["Beds made, linen changed if you leave it out", "Bedside tables and dressers dusted", "Mirrors polished", "Floors vacuumed and mopped"],
      "deep": ["Skirting boards and door frames", "Under the bed vacuumed", "Wardrobe doors and handles wiped", "Ceiling fan blades dusted"],
      "endOfLease": ["Inside wardrobes, shelves and drawers", "Walls spot-cleaned", "Windows, tracks and sills", "Light switches and fittings"]
    },
    {
      "key": "bathroom", "name": "Bathrooms",
      "regular": ["Shower, bath and screen cleaned", "Toilet scrubbed and sanitised inside and out", "Vanity and basin polished", "Mirrors left streak-free", "Floor mopped", "Towels folded or hung"],
      "deep": ["Shower screen de-scaled", "Grout scrubbed", "Exhaust fan cover cleaned", "Cabinet fronts and handles"],
      "endOfLease": ["Inside the vanity and cabinets", "Mould spot-treatment on grout and sealant", "Walls and tiles washed"]
    },
    {
      "key": "laundry", "name": "Laundry",
      "regular": ["Tub and taps cleaned", "Bench and machine tops wiped", "Floor mopped"],
      "deep": ["Washing machine seal and dispenser", "Dryer lint filter cleared", "Behind the machines where we can reach"],
      "endOfLease": ["Inside the cupboards", "Walls spot-cleaned", "Dryer vent cover"]
    },
    {
      "key": "outdoor", "name": "Balcony and entry",
      "regular": ["Front entry swept", "Front door and doormat"],
      "deep": ["Balcony or patio swept and mopped", "Outdoor furniture wiped", "Sliding door tracks"],
      "endOfLease": ["Ground-floor windows, outside", "Cobwebs cleared from the eaves", "Garage swept, if there is one"]
    }
  ],

  "dontDo": [
    "Biohazard, hoarding or post-party clean-ups. We'll point you to a specialist who does.",
    "Mould remediation beyond surface treatment.",
    "Anything above 2.5 metres, or outside work that needs a ladder.",
    "Moving heavy furniture or appliances.",
    "Carpet steam cleaning. We book a local carpet cleaner alongside your end of lease clean instead."
  ],

  "pillars": [
    { "title": "Employees, not subcontractors", "text": "Every cleaner is on our payroll with award wages, super and WorkCover. It's why they stay for years, and why you get the same person." },
    { "title": "Police-checked every two years", "text": "A national police check before anyone starts, renewed every two years, not just once on hiring." },
    { "title": "$10 million public liability", "text": "And one simple rule: if we break something, you hear it from us first." },
    { "title": "Two weeks of training", "text": "New cleaners shadow a senior cleaner for two weeks before they're ever sent out alone." },
    { "title": "Safe around kids and pets", "text": "Plant-based products by default. Tell us about allergies and we'll use whatever you prefer." },
    { "title": "We bring everything", "text": "Vacuum, mops, cloths and products. Nothing of yours gets used unless you ask." }
  ],

  "founder": {
    "name": "Leonie Park",
    "role": "Founder",
    "note": "I cleaned houses for six years before I started Hush, and the thing customers told me most wasn't that the last company did a bad job. It was that they never knew who was coming. So that's the whole idea: one person who knows your house, who you've actually met. Everything else — the checklists, the guarantee, the prices on the website — is just us making it easy to trust that person."
  },

  "team": [
    { "name": "Mai N.", "initials": "MN", "since": "2019", "languages": "English and Vietnamese", "loves": "A tap polished until you can see yourself in it." },
    { "name": "Tomás R.", "initials": "TR", "since": "2020", "languages": "English and Spanish", "loves": "End of lease cleans where the agent can't find a single note to make." },
    { "name": "Georgia W.", "initials": "GW", "since": "2021", "languages": "English", "loves": "Bathrooms. She's aware this is unusual." },
    { "name": "Aroha T.", "initials": "AT", "since": "2022", "languages": "English and te reo Māori", "loves": "Homes with dogs, who usually supervise." }
  ],

  "reviews": [
    { "stars": 5, "text": "I've had four cleaning companies in eight years and this is the first time I've had the same person twice in a row, let alone for a year. Mai knows where everything goes better than I do.", "name": "Sophie L.", "suburb": "Highgate Hill", "service": "Fortnightly clean" },
    { "stars": 5, "text": "Got our full bond back on a three bedroom rental that was, honestly, a disaster. The agent's report didn't have a single note on it.", "name": "Josh and Kiri", "suburb": "Annerley", "service": "End of lease clean" },
    { "stars": 5, "text": "The price on the website was the price on the invoice. That shouldn't be remarkable, but it is.", "name": "Daniel O.", "suburb": "West End", "service": "Deep clean" },
    { "stars": 5, "text": "We're never home and I was nervous about leaving a key. They text when they arrive and when they lock up. After the first month I stopped thinking about it at all.", "name": "Amara T.", "suburb": "Yeronga", "service": "Weekly clean" },
    { "stars": 5, "text": "Tomás noticed a slow leak under our kitchen sink and left a note about it. Saved us a much bigger problem.", "name": "Ben W.", "suburb": "Fairfield", "service": "Fortnightly clean" },
    { "stars": 5, "text": "Booked a deep clean before my parents visited from overseas. My mum, who is impossible to impress, asked for their number.", "name": "Lan N.", "suburb": "South Brisbane", "service": "Deep clean" }
  ],

  "faq": [
    { "q": "How do you work out the price?", "a": "By the number of bedrooms and bathrooms, the type of clean, and any extras. Regular visits get a discount for coming more often. The quote on our prices page is exactly what we charge." },
    { "q": "What do I need to provide?", "a": "Nothing. Your cleaner brings the vacuum, mops, cloths and all the products. If you'd like us to use something of yours, just leave it out with a note." },
    { "q": "How long does a clean take?", "a": "A regular clean on a three bedroom home is usually two and a half to three and a half hours. Longer jobs get two cleaners, so they're finished sooner." },
    { "q": "Can I skip or reschedule a visit?", "a": "Yes, with 48 hours' notice. Reply to your reminder text and it's done. There's no fee for skipping." },
    { "q": "What happens if my cleaner is sick?", "a": "Your named backup comes instead. They'll have been to your home before, so nobody new turns up unannounced." },
    { "q": "Do you clean homes with pets?", "a": "All the time. Let us know what pets you have so your cleaner knows who they're meeting, and whether anyone needs to stay inside." },
    { "q": "How do I pay?", "a": "We charge the card on file the day after each clean, so you've had a chance to check the work first. No deposits for regular or deep cleans." }
  ],

  "hours": [
    { "day": "Monday",    "open": "07:00", "close": "17:00", "closed": false },
    { "day": "Tuesday",   "open": "07:00", "close": "17:00", "closed": false },
    { "day": "Wednesday", "open": "07:00", "close": "17:00", "closed": false },
    { "day": "Thursday",  "open": "07:00", "close": "17:00", "closed": false },
    { "day": "Friday",    "open": "07:00", "close": "17:00", "closed": false },
    { "day": "Saturday",  "open": "08:00", "close": "13:00", "closed": false },
    { "day": "Sunday",    "open": "",      "close": "",      "closed": true  }
  ],

  "suburbs": ["West End", "South Brisbane", "Highgate Hill", "Dutton Park", "Woolloongabba", "Kangaroo Point", "East Brisbane", "Annerley", "Fairfield", "Yeronga", "Greenslopes", "Coorparoo"]
};
const DRAFT_KEY = 'hush-content';

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const params = new URLSearchParams(location.search);
const inFrame = (() => { try { return window.self !== window.top; } catch (e) { return true; } })();
const previewMode = inFrame || params.has('preview');
const page = document.body.dataset.page || 'home';

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const esc = t => { const d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; };
const dig = (o, p) => p.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const money = n => '$' + Math.round(n).toLocaleString('en-AU');
const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
const article = w => (/^[aeiou]/i.test(w) ? 'an' : 'a');
const listJoin = arr => arr.length < 2 ? (arr[0] || '') : arr.slice(0, -1).join(', ') + ' and ' + arr[arr.length - 1];

const CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
const TICK  = '<svg class="tick" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
const XMARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg>';
const SPARK = 'M12 1.5l2.4 7.1 7.1 2.4-7.1 2.4L12 20.5l-2.4-7.1L2.5 11l7.1-2.4z';
const MARK  = '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><path class="drop" d="M16 3.5c5 6 9 10.9 9 15.6a9 9 0 0 1-18 0C7 14.4 11 9.5 16 3.5z"/><path class="spk" d="M16 13.2l1.2 3.4 3.4 1.2-3.4 1.2L16 22.4l-1.2-3.4-3.4-1.2 3.4-1.2z"/></svg>';
const PAGES = [['index.html', 'Home'], ['services.html', 'What we clean'], ['pricing.html', 'Prices'], ['about.html', 'Our cleaners'], ['book.html', 'Book']];

let C = DEFAULT_CONTENT;
let usingDraft = false;

/* Links keep the ?preview flag when the owner is previewing unpublished edits. */
function href(path, qs) {
  const bits = [];
  if (qs) bits.push(qs);
  if (previewMode && !inFrame) bits.push('preview=1');
  return path + (bits.length ? '?' + bits.join('&') : '');
}

/* ---------------------------------------------------------------------
   Content: the owner's unpublished draft (only when previewing),
   otherwise the live content.json, otherwise the built-in copy.
   --------------------------------------------------------------------- */
function loadContent() {
  if (previewMode) {
    try {
      const d = JSON.parse(localStorage.getItem(DRAFT_KEY));
      if (d && d.business) { usingDraft = true; return Promise.resolve(d); }
    } catch (e) { /* storage blocked — fall through */ }
  }
  const req = fetch('content.json', { cache: 'no-store' }).then(r => (r.ok ? r.json() : null)).catch(() => null);
  const timeout = new Promise(res => setTimeout(() => res(null), 2500));
  return Promise.race([req, timeout]).then(j => (j && j.business ? j : DEFAULT_CONTENT));
}

/* ---------------------------------------------------------------------
   Pricing engine — the single source of truth for every price on the site
   --------------------------------------------------------------------- */
function quote(q) {
  const P = C.pricing;
  const s = P.services[q.type];
  const rooms = s.base + s.perBedroom * q.bed + s.perBathroom * q.bath;
  let hours = s.baseHours + s.hoursPerBedroom * q.bed + s.hoursPerBathroom * q.bath;
  const lines = [{ key: 'base', label: `${s.label}, ${plural(q.bed, 'bedroom')}, ${plural(q.bath, 'bathroom')}`, amount: rooms }];
  let sub = rooms;
  const included = [];
  P.extras.forEach(x => {
    if ((x.includedIn || []).includes(q.type)) { included.push(x.label); return; }
    if (q.extras.includes(x.key)) {
      sub += Number(x.price) || 0;
      hours += Number(x.hours) || 0;
      lines.push({ key: x.key, label: x.label, amount: Number(x.price) || 0 });
    }
  });
  let freq = null, discount = 0;
  if (q.type === 'regular') {
    freq = P.frequencies.find(f => f.key === q.freq) || P.frequencies[0];
    if (freq && freq.discount > 0) {
      discount = Math.round(sub * freq.discount / 100);
      lines.push({ key: 'disc', label: `${freq.label} visits, ${freq.discount}% off`, amount: -discount, disc: true });
    }
  }
  let total = sub - discount, minApplied = false;
  if (total < P.minimum) { total = P.minimum; minApplied = true; }
  const cleaners = hours > 5 ? 2 : 1;
  const onSite = Math.max(1, Math.round((hours / cleaners) * 2) / 2);
  return { lines, subtotal: sub, discount, total: Math.round(total), cleaners, onSite, freq, minApplied, included };
}
function hoursText(r) {
  const h = String(r.onSite).replace('.5', '½');
  return `About ${h} hour${r.onSite === 1 ? '' : 's'} with ${r.cleaners === 2 ? 'two cleaners' : 'one cleaner'}`;
}
function qsFrom(q) {
  const p = new URLSearchParams({ type: q.type, bed: q.bed, bath: q.bath });
  if (q.type === 'regular') p.set('freq', q.freq);
  if (q.extras.length) p.set('extras', q.extras.join(','));
  return p.toString();
}
function qFromParams() {
  const P = C.pricing;
  const t = params.get('type');
  const q = {
    type: P.services[t] ? t : 'regular',
    bed: clamp(parseInt(params.get('bed'), 10) || 3, 1, 6),
    bath: clamp(parseInt(params.get('bath'), 10) || 2, 1, 4),
    freq: 'fortnightly',
    extras: (params.get('extras') || '').split(',').filter(k => P.extras.some(x => x.key === k))
  };
  const f = params.get('freq');
  if (P.frequencies.some(x => x.key === f)) q.freq = f;
  if (!P.frequencies.some(x => x.key === q.freq)) q.freq = P.frequencies[0].key;
  return q;
}
function serviceName(key) { const s = C.services.find(x => x.key === key); return s ? s.name : key; }

/* ---------------------------------------------------------------------
   Small reusable controls
   --------------------------------------------------------------------- */
function tween(el, to) {
  const from = el.dataset.v != null ? Number(el.dataset.v) : to;
  el.dataset.v = to;
  cancelAnimationFrame(el._raf);
  if (reduced || from === to) { el.textContent = money(to); return; }
  const t0 = performance.now(), d = 480;
  const step = now => {
    const p = Math.min((now - t0) / d, 1), e = 1 - Math.pow(1 - p, 3);
    el.textContent = money(from + (to - from) * e);
    if (p < 1) el._raf = requestAnimationFrame(step);
  };
  el._raf = requestAnimationFrame(step);
}

function makeStepper(el, { min, max, value, label }, onChange) {
  el.innerHTML = `<button type="button" aria-label="Fewer ${esc(label)}">&minus;</button><output aria-live="polite"><span>${value}</span></output><button type="button" aria-label="More ${esc(label)}">+</button>`;
  const [dec, inc] = $$('button', el);
  const out = $('output', el);
  let v = value;
  const show = dir => {
    out.innerHTML = `<span>${v}</span>`;
    out.className = dir || '';
    dec.disabled = v <= min;
    inc.disabled = v >= max;
  };
  dec.addEventListener('click', () => { if (v > min) { v--; show('roll-down'); onChange(v); } });
  inc.addEventListener('click', () => { if (v < max) { v++; show('roll-up'); onChange(v); } });
  show();
}

function makeSeg(el, options, current, onChange) {
  el.innerHTML = '<span class="thumb" aria-hidden="true"></span>' + options.map(o =>
    `<button type="button" data-k="${esc(o.key)}" aria-pressed="${o.key === current}">${esc(o.label)}</button>`).join('');
  const thumb = $('.thumb', el);
  const place = () => {
    const b = $('[aria-pressed="true"]', el);
    if (!b || !b.offsetWidth) return;
    thumb.style.width = b.offsetWidth + 'px';
    thumb.style.height = b.offsetHeight + 'px';
    thumb.style.transform = `translate(${b.offsetLeft}px, ${b.offsetTop}px)`;
  };
  el.classList.add('still');
  place();
  requestAnimationFrame(() => requestAnimationFrame(() => el.classList.remove('still')));
  el.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b || !el.contains(b)) return;
    $$('button', el).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    place();
    onChange(b.dataset.k);
  });
  window.addEventListener('resize', place);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
}

function observeOnce(el, fn, threshold = 0.35) {
  if (!el) return;
  if (!('IntersectionObserver' in window) || reduced) { fn(el); return; }
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { fn(en.target); io.disconnect(); }
  }), { threshold });
  io.observe(el);
}

function revCard(r) {
  const n = Number(r.stars) || 5;
  return `<article class="rev"><div class="stars" aria-label="${n} out of 5 stars">${'★'.repeat(n)}</div>
    <blockquote>${esc(r.text)}</blockquote>
    <footer><b>${esc(r.name)}</b>${esc(r.suburb)}, ${esc(String(r.service || '').toLowerCase())}</footer></article>`;
}

/* Brisbane time — Queensland has no daylight saving */
function bneNow() {
  const parts = {};
  new Intl.DateTimeFormat('en-AU', { timeZone: 'Australia/Brisbane', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false })
    .formatToParts(new Date()).forEach(p => { parts[p.type] = p.value; });
  return {
    day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(String(parts.weekday).slice(0, 3)),
    mins: (parseInt(parts.hour, 10) % 24) * 60 + parseInt(parts.minute, 10)
  };
}
const toMins = t => { const [h, m] = String(t || '0:0').split(':').map(Number); return (h || 0) * 60 + (m || 0); };
const fmtT = m => { const h = Math.floor(m / 60), mm = m % 60; return (h % 12 || 12) + (mm ? ':' + String(mm).padStart(2, '0') : '') + (h >= 12 ? 'pm' : 'am'); };
function office() {
  const now = bneNow(), idx = (now.day + 6) % 7, row = C.hours[idx];
  if (row && !row.closed && now.mins >= toMins(row.open) && now.mins < toMins(row.close)) {
    return { open: true, idx, text: `Office open now, until ${fmtT(toMins(row.close))}` };
  }
  for (let k = 0; k < 8; k++) {
    const j = (idx + k) % 7, r = C.hours[j];
    if (!r || r.closed) continue;
    if (k === 0 && now.mins >= toMins(r.open)) continue;
    return { open: false, idx, text: `Office closed. Opens ${k === 0 ? 'today' : k === 1 ? 'tomorrow' : r.day} at ${fmtT(toMins(r.open))}` };
  }
  return { open: false, idx, text: 'Office closed' };
}

/* ---------------------------------------------------------------------
   Shared across every page
   --------------------------------------------------------------------- */
function bindAll() {
  $$('[data-bind]').forEach(el => { const v = dig(C, el.dataset.bind); if (v != null) el.textContent = v; });
}

function currentSlug() {
  const last = location.pathname.split('/').pop() || 'index.html';
  return last.replace(/\.html$/, '') || 'index';
}

function renderFooter() {
  const f = $('#foot');
  if (!f) return;
  const b = C.business;
  f.innerHTML = `<div class="wrap"><div class="foot-in">
    <div class="foot-grid">
      <div><a class="brand" href="${href('index.html')}">${MARK}<span>${esc(b.shortName)}</span></a>
        <p>Police-checked home cleaners across Brisbane's inner south since ${esc(b.established)}. The same cleaner, every visit.</p></div>
      <div><h4>Pages</h4><ul>${PAGES.map(([u, l]) => `<li><a href="${href(u)}">${esc(l)}</a></li>`).join('')}</ul></div>
      <div><h4>Where we clean</h4><ul>${C.suburbs.slice(0, 6).map(s => `<li>${esc(s)}</li>`).join('')}<li><a href="${href('book.html')}">and nearby</a></li></ul></div>
      <div><h4>Get in touch</h4><ul>
        <li><a href="tel:${esc(b.phoneLink)}">${esc(b.phone)}</a></li>
        <li><a href="mailto:${esc(b.email)}">${esc(b.email)}</a></li>
        <li>${esc(b.addressLine1)}<br>${esc(b.addressLine2)}</li></ul></div>
    </div>
    <div class="big" aria-hidden="true">${esc(b.shortName)}</div>
    <div class="legal"><span>${esc(b.name)}</span><span>ABN ${esc(b.abn)}</span><span>${esc(b.insurance)}</span><span>&copy; ${new Date().getFullYear()}</span></div>
  </div></div>`;
}

function wireNav() {
  const burger = $('.burger');
  if (!burger) return;
  const slug = currentSlug();
  const menu = document.createElement('div');
  menu.className = 'menu';
  menu.id = 'menu';
  menu.innerHTML = `<nav aria-label="Mobile">${PAGES.map(([u, l], i) => {
    const on = u.replace('.html', '') === slug;
    return `<a href="${href(u)}" style="transition-delay:${(0.12 + i * 0.05).toFixed(2)}s"${on ? ' aria-current="page"' : ''}>${esc(l)}</a>`;
  }).join('')}</nav>
    <div class="menu-foot"><a href="tel:${esc(C.business.phoneLink)}">${esc(C.business.phone)}</a><span>${esc(C.business.email)}</span></div>`;
  document.body.appendChild(menu);
  burger.setAttribute('aria-controls', 'menu');
  const set = open => {
    document.documentElement.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  burger.addEventListener('click', () => set(!document.documentElement.classList.contains('menu-open')));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
  $$('a', menu).forEach(a => a.addEventListener('click', () => set(false)));
}

/* Sub-page titles come into focus word by word */
function splitWords() {
  $$('.phero h1').forEach(h => {
    let i = 0;
    const walk = node => {
      Array.from(node.childNodes).forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const s = document.createElement('span');
            s.className = 'w';
            s.style.setProperty('--i', i++);
            s.textContent = part;
            frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(h);
    h.classList.add('words-ready');
  });
}

function propagatePreview() {
  if (!previewMode || inFrame) return;
  $$('a[href]').forEach(a => {
    const h = a.getAttribute('href');
    if (!/^[\w-]+\.html/.test(h) || /preview=/.test(h)) return;
    a.setAttribute('href', h + (h.includes('?') ? '&' : '?') + 'preview=1');
  });
}

/* Buttons fill from wherever the pointer enters */
document.addEventListener('pointerover', e => {
  const b = e.target.closest && e.target.closest('.btn');
  if (!b) return;
  const r = b.getBoundingClientRect();
  b.style.setProperty('--x', (e.clientX - r.left) + 'px');
  b.style.setProperty('--y', (e.clientY - r.top) + 'px');
});

/* ---------------------------------------------------------------------
   Home
   --------------------------------------------------------------------- */
function initHome() {
  const h = C.hero;
  $('#heroHeadline').textContent = h.headline;
  $('#heroLede').textContent = h.lede;
  $('#facts').innerHTML = h.stats.map(s => `<div><b>${esc(s.value)}</b> ${esc(s.label)}</div>`).join('');
  $('#worries').innerHTML = C.worries.map(w => `<div class="worry"><h3>${esc(w.q)}</h3><p>${esc(w.a)}</p></div>`).join('');
  $('#steps').innerHTML = C.steps.map((s, i) =>
    `<li class="step" style="--i:${i}"><span class="num">${i + 1}</span><h3>${esc(s.title)}</h3><p>${esc(s.text)}</p></li>`).join('');
  observeOnce($('#steps'), el => el.classList.add('in'));

  $('#svcRows').innerHTML = C.services.map(s => {
    const from = quote({ type: s.key, bed: 1, bath: 1, freq: 'once', extras: [] }).total;
    return `<a class="svc-row" href="${href('services.html')}"><h3>${esc(s.name)}</h3><p>${esc(s.tagline)} ${esc(s.for)}</p><span class="from">from<b>${money(from)}</b></span></a>`;
  }).join('');

  $('#guarantees').innerHTML = C.guarantees.map(g => `<div class="g"><h3>${esc(g.title)}</h3><p>${esc(g.text)}</p></div>`).join('');

  const track = $('#revTrack');
  track.innerHTML = C.reviews.map(revCard).join('');
  wireTrack(track, $('#revPrev'), $('#revNext'), $('#revBar'));

  initMiniQuote();

  const glass = $('#glass');
  if (glass && inFrame) $$('.fog, .blade, .glint, .spark', glass).forEach(n => n.remove());
  if (glass) {
    const setTilt = () => {
      const tilt = Math.atan((0.14 * glass.offsetWidth) / glass.offsetHeight) * 180 / Math.PI;
      glass.style.setProperty('--tilt', tilt.toFixed(2) + 'deg');
    };
    setTilt();
    window.addEventListener('resize', setTilt);
    glass.addEventListener('animationend', e => {
      if (e.animationName === 'wipe') $$('.fog, .blade', glass).forEach(n => n.remove());
      if (e.animationName === 'glint') e.target.remove();
    });
  }
}

function wireTrack(track, prev, next, bar) {
  const cardW = () => { const c = $('.rev', track); return c ? c.getBoundingClientRect().width + 16 : 320; };
  prev.addEventListener('click', () => track.scrollBy({ left: -cardW(), behavior: reduced ? 'auto' : 'smooth' }));
  next.addEventListener('click', () => track.scrollBy({ left: cardW(), behavior: reduced ? 'auto' : 'smooth' }));
  const update = () => {
    const max = track.scrollWidth - track.clientWidth;
    const frac = Math.min(1, track.clientWidth / track.scrollWidth);
    const p = max > 0 ? track.scrollLeft / max : 0;
    bar.style.width = (frac * 100) + '%';
    bar.style.transform = `translateX(${p * (1 / frac - 1) * 100}%)`;
    prev.disabled = track.scrollLeft < 4;
    next.disabled = track.scrollLeft > max - 4;
  };
  track.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
}

function initMiniQuote() {
  const P = C.pricing;
  const q = { type: 'regular', bed: 3, bath: 2, freq: P.frequencies.some(f => f.key === 'fortnightly') ? 'fortnightly' : P.frequencies[0].key, extras: [] };
  const total = $('#mqTotal'), was = $('#mqWas'), save = $('#mqSave'), hrs = $('#mqHours'), link = $('#mqLink');
  const update = () => {
    const r = quote(q);
    tween(total, r.total);
    was.textContent = r.discount && !r.minApplied ? money(r.subtotal) : '';
    const label = r.freq && r.freq.discount && !r.minApplied ? `Save ${r.freq.discount}%` : '';
    if (label !== save.textContent) {
      save.textContent = label;
      save.classList.remove('pop');
      void save.offsetWidth;
      if (label) save.classList.add('pop');
    }
    hrs.textContent = hoursText(r);
    link.href = href('pricing.html', qsFrom(q));
  };
  makeStepper($('#mqBed'), { min: 1, max: 6, value: q.bed, label: 'bedrooms' }, v => { q.bed = v; update(); });
  makeStepper($('#mqBath'), { min: 1, max: 4, value: q.bath, label: 'bathrooms' }, v => { q.bath = v; update(); });
  makeSeg($('#mqFreq'), P.frequencies.map(f => ({ key: f.key, label: f.label })), q.freq, k => { q.freq = k; update(); });
  update();
}

/* ---------------------------------------------------------------------
   What we clean
   --------------------------------------------------------------------- */
function initServices() {
  $('#tiers').innerHTML = C.services.map(s => {
    const from = quote({ type: s.key, bed: 1, bath: 1, freq: 'once', extras: [] }).total;
    return `<article class="tier">
      <h3>${esc(s.name)}</h3><p class="tag">${esc(s.tagline)}</p>
      <p class="for">${esc(s.for)}</p><p class="time">${esc(s.time)}</p>
      <p class="from">One bedroom, one bathroom, from<b>${money(from)}</b></p>
      <ul>${s.points.map(p => `<li>${TICK}<span>${esc(p)}</span></li>`).join('')}</ul>
      <a class="btn soft" href="${href('pricing.html', 'type=' + encodeURIComponent(s.key))}">Price this clean</a>
    </article>`;
  }).join('');

  C.rooms.forEach(r => { const t = $(`[data-rl="${r.key}"]`); if (t) t.textContent = r.name; });

  let room = 'kitchen', level = 'regular';
  const nameEl = $('#roomName'), countEl = $('#roomCount'), listEl = $('#roomList');
  const draw = animateTitle => {
    const R = C.rooms.find(r => r.key === room) || C.rooms[0];
    const items = [];
    (R.regular || []).forEach(t => items.push({ t }));
    if (level !== 'regular') (R.deep || []).forEach(t => items.push({ t, tag: 'Deep' }));
    if (level === 'endOfLease') (R.endOfLease || []).forEach(t => items.push({ t, tag: 'End of lease', eol: true }));
    const lv = serviceName(level).toLowerCase();
    nameEl.textContent = R.name;
    if (animateTitle) { nameEl.classList.remove('swap'); void nameEl.offsetWidth; nameEl.classList.add('swap'); }
    countEl.textContent = `${items.length} things on the list in ${article(lv)} ${lv}.`;
    listEl.innerHTML = items.map((it, i) =>
      `<li style="--i:${i}"><span class="tk">${CHECK}</span><span>${esc(it.t)}</span>${it.tag ? `<em class="${it.eol ? 'eol' : ''}">${esc(it.tag)}</em>` : ''}</li>`).join('');
    $$('.room').forEach(g => {
      const on = g.dataset.room === room;
      g.classList.toggle('on', on);
      g.setAttribute('aria-pressed', String(on));
    });
  };
  $$('.room').forEach(g => {
    const pick = () => { room = g.dataset.room; draw(true); };
    g.addEventListener('click', pick);
    g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
  });
  makeSeg($('#levelSeg'), C.services.map(s => ({ key: s.key, label: s.name.replace(/ clean$/i, '') })), level, k => { level = k; draw(false); });
  draw(false);

  $('#extras').innerHTML = C.pricing.extras.map(x => {
    const inc = (x.includedIn || []).map(k => serviceName(k).toLowerCase());
    return `<div class="xtra"><span>${esc(x.label)}${inc.length ? `<small>Included in ${esc(article(inc[0]))} ${esc(listJoin(inc))}</small>` : ''}</span><b>${money(x.price)}</b></div>`;
  }).join('');
  $('#nope').innerHTML = C.dontDo.map(t => `<li>${XMARK}<span>${esc(t)}</span></li>`).join('');
}

/* ---------------------------------------------------------------------
   Prices — the quote builder
   --------------------------------------------------------------------- */
function initPricing() {
  const P = C.pricing;
  const q = qFromParams();
  $$('[data-min]').forEach(el => { el.textContent = money(P.minimum); });

  const typesEl = $('#qTypes');
  typesEl.innerHTML = C.services.map(s =>
    `<button type="button" class="opt" data-k="${esc(s.key)}" aria-pressed="${s.key === q.type}"><b>${esc(s.name)}</b><span>${esc(s.tagline)}</span></button>`).join('');
  typesEl.addEventListener('click', e => {
    const b = e.target.closest('.opt');
    if (!b) return;
    q.type = b.dataset.k;
    $$('.opt', typesEl).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    update(true);
  });

  makeStepper($('#qBed'), { min: 1, max: 6, value: q.bed, label: 'bedrooms' }, v => { q.bed = v; update(false); });
  makeStepper($('#qBath'), { min: 1, max: 4, value: q.bath, label: 'bathrooms' }, v => { q.bath = v; update(false); });

  const freqEl = $('#qFreqs');
  freqEl.innerHTML = P.frequencies.map(f =>
    `<button type="button" class="opt" data-k="${esc(f.key)}" aria-pressed="${f.key === q.freq}"><b>${esc(f.label)}</b>${f.discount ? `<em>Save ${esc(f.discount)}%</em>` : '<span>Full price</span>'}</button>`).join('');
  freqEl.addEventListener('click', e => {
    const b = e.target.closest('.opt');
    if (!b) return;
    q.freq = b.dataset.k;
    $$('.opt', freqEl).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    update(false);
  });

  const exEl = $('#qExtras');
  const drawExtras = () => {
    exEl.innerHTML = P.extras.map(x => {
      const inc = (x.includedIn || []).includes(q.type);
      const on = inc || q.extras.includes(x.key);
      return `<label class="chip${inc ? ' included' : ''}"><input type="checkbox" value="${esc(x.key)}"${on ? ' checked' : ''}${inc ? ' disabled' : ''}><span class="box">${CHECK}</span><span class="lbl">${esc(x.label)}</span><span class="amt">${inc ? 'Included' : '+' + money(x.price)}</span></label>`;
    }).join('');
  };
  exEl.addEventListener('change', e => {
    const i = e.target;
    if (i.type !== 'checkbox') return;
    q.extras = i.checked ? Array.from(new Set(q.extras.concat(i.value))) : q.extras.filter(k => k !== i.value);
    update(false);
  });

  const mbar = $('#mbar'), summary = $('#summary');
  if (mbar && summary && 'IntersectionObserver' in window) {
    new IntersectionObserver(es => es.forEach(en => mbar.classList.toggle('hide', en.isIntersecting)), { threshold: 0.15 }).observe(summary);
  }

  let seen = null;
  function update(typeChanged) {
    const regular = q.type === 'regular';
    freqEl.hidden = !regular;
    const note = $('#qFreqNote');
    note.hidden = regular;
    if (!regular) {
      const n = serviceName(q.type).toLowerCase();
      note.textContent = `${article(n) === 'an' ? 'An' : 'A'} ${n} is a one-off visit, so there's nothing to choose here. Most people follow one with regular visits.`;
    }
    if (typeChanged) drawExtras();

    const r = quote(q);
    const keys = r.lines.map(l => l.key + ':' + l.amount);
    $('#qLines').innerHTML = r.lines.map((l, i) => {
      const fresh = seen && !seen.includes(keys[i]) ? ' fresh' : '';
      const amt = l.amount < 0 ? '&minus;' + money(-l.amount) : money(l.amount);
      return `<li class="${l.disc ? 'disc' : ''}${fresh}"><span>${esc(l.label)}</span><b>${amt}</b></li>`;
    }).join('') + (r.included.length ? `<li><span>${plural(r.included.length, 'extra')} already included</span><b>$0</b></li>` : '');
    seen = keys;

    const per = regular ? 'per clean' : 'one-off';
    tween($('#qTotal'), r.total);
    $('#qPer').textContent = per;
    $('#qHours').textContent = hoursText(r);
    $('#qMin').textContent = r.minApplied ? `Our minimum visit is ${money(P.minimum)}.` : '';
    const book = href('book.html', qsFrom(q));
    $('#qBook').href = book;
    if (mbar) { tween($('#mTotal'), r.total); $('#mPer').textContent = per; $('#mBook').href = book; }
    try { history.replaceState(null, '', location.pathname + '?' + qsFrom(q) + (previewMode && !inFrame ? '&preview=1' : '')); } catch (e) { /* ignore */ }
  }
  update(true);
}

/* ---------------------------------------------------------------------
   Our cleaners
   --------------------------------------------------------------------- */
function initAbout() {
  $('#team').innerHTML = C.team.map(m => `<article class="mate">
    <div class="blob"><span>${esc(m.initials)}</span></div>
    <h3>${esc(m.name)}</h3>
    <p class="since">With us since ${esc(m.since)}. Speaks ${esc(m.languages)}.</p>
    <p class="loves">${esc(m.loves)}</p>
    <span class="badge">${TICK}Police-checked</span></article>`).join('');
  $('#pillars').innerHTML = C.pillars.map(p => `<div class="pil"><h3>${esc(p.title)}</h3><p>${esc(p.text)}</p></div>`).join('');
  const f = C.founder;
  $('#letter').innerHTML = `<p>${esc(f.note)}</p><p class="sig">${esc(String(f.name).split(' ')[0])}<small>${esc(f.name)}, ${esc(String(f.role).toLowerCase())}</small></p>`;
  $('#wall').innerHTML = C.reviews.map(revCard).join('');
}

/* ---------------------------------------------------------------------
   Book
   --------------------------------------------------------------------- */
function chipGroup(el, name, options, type, checked) {
  el.innerHTML = options.map(o =>
    `<label class="chip${type === 'radio' ? ' radio' : ''}"><input type="${type}"${name ? ` name="${esc(name)}"` : ''} value="${esc(o)}"${o === checked ? ' checked' : ''}><span class="box">${CHECK}</span><span class="lbl">${esc(o)}</span></label>`).join('');
}

function initBook() {
  const P = C.pricing, b = C.business;
  const hasQuote = !!(params.get('type') && P.services[params.get('type')]);
  let chosenType = null;

  if (hasQuote) {
    const q = qFromParams(), r = quote(q), s = P.services[q.type];
    const bits = [`${plural(q.bed, 'bedroom')}, ${plural(q.bath, 'bathroom')}`];
    if (q.type === 'regular' && r.freq) bits.push(r.freq.label.toLowerCase());
    const ex = q.extras
      .map(k => P.extras.find(x => x.key === k))
      .filter(x => x && !(x.includedIn || []).includes(q.type))
      .map(x => x.label.toLowerCase());
    if (ex.length) bits.push('plus ' + listJoin(ex));
    const per = q.type === 'regular' ? 'per clean' : 'one-off';
    chosenType = serviceName(q.type);
    $('#qcard').innerHTML = `<p><strong>${esc(s.label)}</strong><br>${esc(bits.join(', '))}. <a href="${href('pricing.html', qsFrom(q))}">Change</a></p><div class="amt">${money(r.total)} <small>${per}</small></div>`;
    $('#fQuote').value = `${s.label}: ${bits.join(', ')}. ${money(r.total)} ${per}.`;
  } else {
    $('#qcard').innerHTML = `<p><strong>Haven't got a price yet?</strong><br>It takes under a minute, and it's the price we'll charge.</p><a class="btn sm" href="${href('pricing.html')}">Get your price</a>`;
  }

  chipGroup($('#gType'), 'Type of clean', C.services.map(s => s.name).concat('Not sure yet'), 'radio', chosenType);
  chipGroup($('#gDays'), '', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], 'checkbox');
  chipGroup($('#gTime'), 'Time of day', ['Morning, 8 to 12', 'Afternoon, 12 to 4', 'Either suits'], 'radio', 'Either suits');
  chipGroup($('#gAccess'), 'Getting in', ["I'll be home", 'Key in a lockbox', 'Door code', 'Collect a key from me'], 'radio');
  chipGroup($('#gPets'), 'Pets', ['No pets', 'A dog', 'A cat', 'More than one'], 'radio', 'No pets');
  $('#suburbList').innerHTML = C.suburbs.map(s => `<option value="${esc(s)}">`).join('');

  const st = office();
  $('#contact').innerHTML = `<p><a href="tel:${esc(b.phoneLink)}">${esc(b.phone)}</a><br><a href="mailto:${esc(b.email)}">${esc(b.email)}</a></p>
    <p class="office"><span class="pip${st.open ? ' on' : ''}"></span>${esc(st.text)}</p>`;
  $('#hours').innerHTML = C.hours.map((h, i) =>
    `<div${i === st.idx ? ' class="today"' : ''}><span>${esc(h.day)}</span><span>${h.closed ? 'Closed' : fmtT(toMins(h.open)) + ' to ' + fmtT(toMins(h.close))}</span></div>`).join('');
  $('#areas').innerHTML = C.suburbs.map(s => `<span>${esc(s)}</span>`).join('');
  $('#responseNote').textContent = b.responseTime;
  $('#faq').innerHTML = C.faq.map(f => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join('');

  const form = $('#bookForm'), btn = $('#submitBtn'), err = $('#ferr');
  const done = () => {
    form.hidden = true;
    $('#qcard').hidden = true;
    $('#done').classList.add('show');
    $('#doneNote').textContent = `${b.responseTime} If it can't wait, call ${b.phone}.`;
    $('#done').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
  };
  const fail = () => {
    btn.disabled = false;
    btn.textContent = 'Send booking request';
    err.textContent = `That didn't send. Call ${b.phone} and we'll book you in over the phone.`;
  };

  form.addEventListener('submit', e => {
    e.preventDefault();
    err.textContent = '';
    const checks = [
      ['#fName', v => v.trim().length > 1, 'your name'],
      ['#fMobile', v => v.replace(/\D/g, '').length >= 8, 'a mobile we can text'],
      ['#fSuburb', v => v.trim().length > 1, 'your suburb']
    ];
    $$('.bad', form).forEach(x => x.classList.remove('bad'));
    const missing = checks.filter(([sel, ok]) => !ok($(sel).value));
    if (missing.length) {
      missing.forEach(([sel]) => { const el = $(sel); void el.offsetWidth; el.classList.add('bad'); });
      $(missing[0][0]).focus();
      err.textContent = `Add ${listJoin(missing.map(m => m[2]))} so we can confirm your booking.`;
      return;
    }
    $('#fDays').value = $$('#gDays input:checked').map(i => i.value).join(', ') || 'Any day';
    btn.disabled = true;
    btn.innerHTML = '<span class="spin"></span>Sending';

    const fd = new FormData(form);
    const lines = [];
    fd.forEach((v, k) => { if (k !== 'botcheck' && v) lines.push(`${k}: ${v}`); });

    if (CONFIG.FORM_ACCESS_KEY) {
      fd.append('access_key', CONFIG.FORM_ACCESS_KEY);
      fd.append('subject', `New booking request from ${fd.get('Name')}`);
      fd.append('from_name', `${b.name} website`);
      fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd })
        .then(r => r.json())
        .then(j => (j.success ? done() : fail()))
        .catch(fail);
    } else {
      if (CONFIG.FALLBACK_EMAIL) window.location.href = 'mailto:' + CONFIG.FALLBACK_EMAIL +
        '?subject=' + encodeURIComponent('Booking request from ' + fd.get('Name')) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      setTimeout(done, 700);
    }
  });
}

/* ---------------------------------------------------------------------
   Start
   --------------------------------------------------------------------- */
splitWords();

loadContent().then(data => {
  C = data;
  bindAll();
  renderFooter();
  wireNav();
  const init = { home: initHome, services: initServices, pricing: initPricing, about: initAbout, book: initBook }[page];
  if (init) init();
  propagatePreview();
  if (usingDraft && !inFrame) {
    const d = document.createElement('div');
    d.className = 'draft';
    d.textContent = 'Previewing unpublished changes';
    document.body.appendChild(d);
  }
  const go = () => requestAnimationFrame(() => document.body.classList.add('ready'));
  if (document.fonts && document.fonts.ready) Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 1200))]).then(go);
  else setTimeout(go, 300);
});

})();
