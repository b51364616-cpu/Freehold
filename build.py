import json, math, random
FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%230C110E'/%3E"
       "%3Crect x='8' y='8' width='16' height='16' fill='none' stroke='%23ECEFE7' stroke-width='2'/%3E%3Ccircle cx='8' cy='8' r='3.2' fill='%23FF6533'/%3E"
       "%3Ccircle cx='24' cy='8' r='3.2' fill='%23ECEFE7'/%3E%3Ccircle cx='24' cy='24' r='3.2' fill='%23ECEFE7'/%3E%3Ccircle cx='8' cy='24' r='3.2' fill='%23ECEFE7'/%3E%3C/svg%3E")
MARK = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect class="bx" x="4" y="4" width="16" height="16"/>'
        '<circle class="pk hot" cx="4" cy="4" r="2.4"/><circle class="pk" cx="20" cy="4" r="2.4"/>'
        '<circle class="pk" cx="20" cy="20" r="2.4"/><circle class="pk" cx="4" cy="20" r="2.4"/></svg>')
EXT = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'
PHONE, PHONE_LINK, EMAIL = '0444 554 898', '+61444554898', 'connor@freeholdweb.com.au'
ABN = '26 751 513 822'
SITE_URL = 'https://freeholdweb.com.au'

# Prices shown in the pages before main.js runs. Keep these the same as SITE.pricing in main.js.
PRICE = dict(oneoff=1500, oneoff_pct=40, start=450, start_pct=30, monthly=99, pages=5, extra_page=100, hourly=75, changes=3)
def money(n): return '${:,.0f}'.format(n)
ONEOFF_DEP = PRICE['oneoff'] * PRICE['oneoff_pct'] / 100
START_DEP = PRICE['start'] * PRICE['start_pct'] / 100

# Runs before anything paints: decides calm mode (OS reduce-motion, unless the visitor chose full
# animations), whether the first-visit intro plays, and where the page-change reveal starts from.
CALM_JS = ("(function(){var d=document.documentElement;d.classList.add('js');try{"
  "var pref=matchMedia('(prefers-reduced-motion: reduce)').matches,s=localStorage.getItem('fh-motion');"
  "if(pref)d.classList.add('prefers-calm');"
  "if(s==='calm'||(pref&&s!=='full'))d.classList.add('calm');"
  "else if(!sessionStorage.getItem('fh-intro')){d.classList.add('intro');sessionStorage.setItem('fh-intro','1');}"
  "}catch(e){}"
  "d.style.setProperty('--ar',(innerHeight/Math.max(1,innerWidth)).toFixed(3));"
  "addEventListener('pagereveal',function(e){if(!e.viewTransition)return;"
  "if(d.classList.contains('calm')){e.viewTransition.skipTransition();return;}"
  "try{var o=JSON.parse(sessionStorage.getItem('fh-from')||'null');sessionStorage.removeItem('fh-from');"
  "if(o){d.style.setProperty('--ox',o[0]);d.style.setProperty('--oy',o[1]);}}catch(x){}"
  "d.classList.add('vt-in');var f=function(){d.classList.remove('vt-in')};e.viewTransition.finished.then(f,f);});})();")

def letters(word, cls=''):
    return ''.join(f'<span style="--i:{i}">{c}</span>' for i, c in enumerate(word))

# ---------- page change: the new page is pegged out as a subdivision of lots ----------
def vt_mask():
    def grid(mid, cols, rows, seed):
        rnd = random.Random(seed)
        V = [[None] * (rows + 1) for _ in range(cols + 1)]
        for i in range(cols + 1):
            for j in range(rows + 1):
                x, y = i / cols, j / rows
                jx = 0 if i in (0, cols) else rnd.uniform(-.3, .3) / cols
                jy = 0 if j in (0, rows) else rnd.uniform(-.3, .3) / rows
                V[i][j] = (x + jx, y + jy)
        polys = ''
        for i in range(cols):
            for j in range(rows):
                pts = [V[i][j], V[i + 1][j], V[i + 1][j + 1], V[i][j + 1]]
                cx = sum(p[0] for p in pts) / 4; cy = sum(p[1] for p in pts) / 4
                ps = ' '.join(f'{x:.4f},{y:.4f}' for x, y in pts)
                polys += f'<polygon points="{ps}" style="--cx:{cx:.3f};--cy:{cy:.3f};--r:{rnd.uniform(-9, 9):.1f}deg"/>'
        return f'<mask id="{mid}" class="vtm" maskUnits="objectBoundingBox" maskContentUnits="objectBoundingBox" x="0" y="0" width="1" height="1">{polys}</mask>'
    return f'<svg class="vt-svg" width="0" height="0" aria-hidden="true" focusable="false"><defs>{grid("vtm-l", 9, 5, 3)}{grid("vtm-p", 4, 8, 5)}</defs></svg>'
VT_MASK = vt_mask()

def head(title, desc, extra='', P=''):
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0C110E">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Freehold">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAV}">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="{P}assets/fonts/anybody.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{P}assets/fonts/hanken.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}styles.css">
<link rel="expect" href="#vtm-p" blocking="render">
<script>{CALM_JS}</script>
{extra}</head>'''

VEIL = f'<div class="veil" id="veil" aria-hidden="true"><div class="intro-box"><span class="ln t"></span><span class="ln r"></span><span class="ln b"></span><span class="ln l"></span><i class="pg"></i><i class="pg"></i><i class="pg"></i><i class="pg"></i><div class="intro-word">{letters("FREEHOLD")}</div><p class="intro-cap">Bokarina, Sunshine Coast</p></div></div>'

def nav(active, P='', veil=True):
    items = [('work', 'work.html', 'Work'), ('pricing', 'pricing.html', 'Pricing'), ('about', 'index.html#about', 'About')]
    CUR = ' aria-current="page"'
    links = ''.join(f'<a href="{P}{u}"{CUR if k == active else ""}>{l}</a>' for k, u, l in items)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="gridlines" aria-hidden="true"><i></i></div>
{VEIL if veil else ''}
<header class="nav" id="nav">
  <a class="brand" href="{P}index.html" aria-label="Freehold, home">{MARK}<b>FREEHOLD</b></a>
  <nav class="links" aria-label="Main">{links}</nav>
  <a class="btn sm navcta" href="{P}pricing.html#quote">Get a quote</a>
  <button class="burger" type="button" aria-label="Open menu" aria-expanded="false"><span></span></button>
</header>'''

def foot(P=''):
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><a class="brand" href="{P}index.html" aria-label="Freehold, home">{MARK}<b>FREEHOLD</b></a>
        <p style="margin-top:1.2rem">Custom websites for trades and local businesses, built by hand in Bokarina on the Sunshine Coast.</p></div>
      <div><h4>Contact</h4><ul><li><a href="tel:{PHONE_LINK}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Bokarina QLD 4575</li></ul></div>
      <div><h4>Pages</h4><ul><li><a href="{P}index.html">Home</a></li><li><a href="{P}work.html">Work</a></li><li><a href="{P}pricing.html">Pricing</a></li><li><a href="{P}privacy.html">Privacy</a></li></ul></div>
      <div><h4>In Bokarina it's</h4><div class="clock" id="clock">&nbsp;</div><p id="clockNote" style="margin-top:.6rem"></p></div>
    </div>
    <div class="legal"><span>&copy; <span id="year">2026</span> Freehold</span><span>ABN {ABN}</span><a href="{P}privacy.html">Privacy policy</a><button class="motion-toggle" id="motionToggle" type="button" hidden></button><span>This site was built the same way yours would be.</span></div>
  </div>
  <div class="footword" id="footword" aria-hidden="true">{letters("FREEHOLD")}</div>
</footer>'''

def page(name, title, desc, active, body, extra_head='', P='', veil=True):
    return f'''{head(title, desc, extra_head, P)}
<body data-page="{name}">
{VT_MASK}
{nav(active, P, veil)}
<main id="main">
{body.strip()}
</main>
{foot(P)}
<script src="{P}main.js"></script>
</body>
</html>
'''

def shot(src, alt, w, h, tall=False):
    return f'<figure class="shot{" tall" if tall else ""}"><img src="assets/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></figure>'
D, PH = (1440, 900), (640, 1385)

# =====================================================================
# HOME — the hero: a website built like a house, on its own block of land
# =====================================================================
def smooth_closed(pts):
    n = len(pts); d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + 'Z'

def land_contours():
    rnd = random.Random(11); out = ''
    for cx, cy, n, r0, step in ((470, 150, 7, 26, 34), (120, 360, 4, 30, 38)):
        for k in range(n):
            r = r0 + k * step; a1, a2 = rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)
            pts = []
            for i in range(56):
                a = i / 56 * 2 * math.pi
                rr = r * (1 + .14 * math.sin(3 * a + a1) + .07 * math.sin(5 * a + a2))
                pts.append((cx + rr * math.cos(a) * 1.3, cy + rr * math.sin(a)))
            out += f'<path class="{"ct ix" if k == 3 and n > 4 else "ct"}" d="{smooth_closed(pts)}"/>'
    return out

LW, LH, SW, SH = 640, 460, 512, 320
LAND_SVG = (f'<svg class="b-svg" viewBox="0 0 {LW} {LH}" width="{LW}" height="{LH}">{land_contours()}'
  '<path class="tape" pathLength="1" d="M34 34H606V426H34Z"/>'
  '<g class="north"><path d="M50 62 56 44 62 62 56 58Z"/><text x="56" y="76" text-anchor="middle">N</text></g>'
  '<g class="scalebar"><path d="M440 409H580M440 404V414M510 406V412M580 404V414"/><text x="440" y="400">0</text><text x="580" y="400" text-anchor="end">10 m</text></g>'
  '<text class="etch" x="36" y="448">LOT 1 &#183; DP 2026 &#183; FREEHOLD</text>'
  '<text class="etch" x="604" y="448" text-anchor="end">YOURBUSINESS.COM.AU</text></svg>')
SLAB_SVG = (f'<svg class="b-svg" viewBox="0 0 {SW} {SH}" width="{SW}" height="{SH}">'
  '<g class="sg">' + ''.join(f'<path d="M{x} 0V{SH}"/>' for x in range(32, SW, 32)) + ''.join(f'<path d="M0 {y}H{SW}"/>' for y in range(32, SH, 32)) + '</g>'
  '<g class="sst" transform="translate(96 160)"><rect x="-58" y="-36" width="116" height="72" rx="4"/><path class="ico" d="M-9 -8v-5a9 9 0 0 1 18 0v5M-13 -8h26v18h-26z"/><text y="26">SECURE</text></g>'
  '<g class="sst" transform="translate(256 160)"><rect x="-58" y="-36" width="116" height="72" rx="4"/><path class="ico" d="M3 -20-11 2h11l-3 16 14-22H0z"/><text y="26">FAST</text></g>'
  '<g class="sst" transform="translate(416 160)"><rect x="-58" y="-36" width="116" height="72" rx="4"/><path class="ico" d="M-14 -14h28v9h-28zM-14 -1h28v9h-28zM-8 -9.5h.1M-8 3.5h.1"/><text y="26">HOSTED</text></g></svg>')
FRAME_SVG = (f'<svg class="b-svg" viewBox="0 0 {SW} {SH}" width="{SW}" height="{SH}">'
  '<g class="wf">'
  f'<rect pathLength="1" x="1" y="1" width="{SW-2}" height="{SH-2}" rx="7"/><path pathLength="1" d="M1 24H{SW-1}"/>'
  '<circle pathLength="1" cx="15" cy="12.5" r="4"/><circle pathLength="1" cx="28" cy="12.5" r="4"/><circle pathLength="1" cx="41" cy="12.5" r="4"/>'
  '<rect pathLength="1" x="160" y="6" width="192" height="13" rx="6.5"/>'
  '<rect pathLength="1" x="22" y="38" width="54" height="10" rx="2"/><path pathLength="1" d="M300 43h30M342 43h30M384 43h26"/><rect pathLength="1" x="430" y="34" width="60" height="18" rx="2"/>'
  '<rect pathLength="1" x="22" y="74" width="208" height="16" rx="2"/><rect pathLength="1" x="22" y="96" width="176" height="16" rx="2"/><rect pathLength="1" x="22" y="118" width="124" height="16" rx="2"/>'
  '<path pathLength="1" d="M22 146h190M22 155h168M22 164h182"/>'
  '<rect pathLength="1" x="22" y="180" width="66" height="20" rx="2"/><rect pathLength="1" x="96" y="180" width="66" height="20" rx="2"/>'
  '<rect pathLength="1" x="258" y="68" width="232" height="140" rx="3"/><path pathLength="1" d="M258 68 490 208M490 68 258 208"/>'
  '<rect pathLength="1" x="22" y="226" width="146" height="76" rx="3"/><rect pathLength="1" x="183" y="226" width="146" height="76" rx="3"/><rect pathLength="1" x="344" y="226" width="146" height="76" rx="3"/>'
  '</g><g class="dim"><path pathLength="1" d="M258 60H490M258 55V65M490 55V65"/><text x="374" y="54" text-anchor="middle">PLANNED FROM A BLANK PAGE</text></g>'
  '<g class="ph"><rect pathLength="1" x="404" y="150" width="78" height="150" rx="12"/><path pathLength="1" d="M432 158h22"/><text x="443" y="314" text-anchor="middle">PHONE FIRST</text></g></svg>')

def faces(w, h, t, cls):
    return f'<i class="fc fc-front {cls}" style="width:{w}px;height:{t}px;top:{h}px"></i><i class="fc fc-left {cls}" style="width:{t}px;height:{h}px"></i>'

TRADES3 = [
  dict(k='kingpin', name='Mechanic', shot='kingpin-desktop.webp', item='Logbook service', a='$289', b='$299', who='Leah, Buderim', want='Wants a logbook service on Friday', g='Mechanic in Kunda Park'),
  dict(k='tessera', name='Tiler', shot='tessera-desktop.webp', item='Splashback, from', a='$890', b='$940', who='Sam, Sippy Downs', want='Wants a bathroom retiled', g='Tiler in Brendale'),
  dict(k='hush', name='Cleaner', shot='hush-desktop.webp', item='Regular clean, from', a='$149', b='$159', who='Priya, Mooloolaba', want='Wants a fortnightly clean', g='Home cleaner in Annerley'),
]
shots = ''.join(f'<img class="b-shot{" on" if i == 0 else ""}" data-k="{t["k"]}" src="assets/{t["shot"]}" alt="" width="1440" height="900" decoding="async"{" fetchpriority=\"high\"" if i == 0 else ""}>' for i, t in enumerate(TRADES3))
T0 = TRADES3[0]
BUILD = f'''<div class="build wait" id="build" aria-hidden="true">
  <div class="b-cam"><div class="b-world" id="bWorld">
    <div class="bl bl-land" data-l="0"><div class="bi">
      <div class="b-top">{LAND_SVG}<i class="b-shadow"></i></div>
      {faces(LW, LH, 30, 'earth')}
      <span class="b-peg" style="--x:34px;--y:34px;--d:0"></span><span class="b-peg" style="--x:606px;--y:34px;--d:1"></span><span class="b-peg" style="--x:606px;--y:426px;--d:2"></span><span class="b-peg" style="--x:34px;--y:426px;--d:3"></span>
      <span class="b-bill b-owner" style="--x:606px;--y:34px"><span>Registered owner<b>You</b></span></span>
      <i class="b-anchor"></i>
    </div></div>
    <div class="bl bl-slab" data-l="1"><div class="bi">
      <div class="b-top">{SLAB_SVG}</div>{faces(SW, SH, 14, 'conc')}<i class="b-anchor"></i>
    </div></div>
    <div class="bl bl-frame" data-l="2"><div class="bi"><div class="b-top">{FRAME_SVG}</div><i class="b-anchor"></i></div></div>
    <div class="bl bl-finish" data-l="3"><div class="bi">
      <div class="b-top"><div class="b-chrome"><i></i><i></i><i></i><span>yourbusiness.com.au</span></div><div class="b-shots">{shots}</div><i class="b-wipe"></i></div>
      {faces(SW, SH, 5, 'glass')}<i class="b-anchor"></i>
    </div></div>
    <div class="bl bl-fit" data-l="4"><div class="bi">
      <span class="b-bill b-card b-edit" style="--x:96px;--y:296px;--d:0"><span>
        <em class="bc-h"><i class="dot"></i>Website editor</em>
        <span class="bc-row"><span class="bc-item" data-f="item">{T0["item"]}</span><span class="bc-field"><s data-f="a">{T0["a"]}</s><b data-f="b">{T0["b"]}</b><i class="caret"></i></span></span>
        <span class="bc-btn"><span class="pub">Publish</span><span class="done">Published &#10003;</span></span>
      </span></span>
      <span class="b-bill b-card b-mail" style="--x:150px;--y:62px;--d:1"><span>
        <em class="bc-h"><svg viewBox="0 0 16 16"><path d="M1.5 3.5h13v9h-13zM1.5 3.5 8 9l6.5-5.5"/></svg>New quote request</em>
        <b class="bc-who" data-f="who">{T0["who"]}</b><span class="bc-sub" data-f="want">{T0["want"]}</span>
      </span></span>
      <span class="b-bill b-card b-goog" style="--x:500px;--y:214px;--d:2"><span>
        <em class="bc-url">yourbusiness.com.au</em><b class="bc-t">Your Business</b><span class="bc-sub" data-f="g">{T0["g"]}</span>
        <span class="bc-acts"><i>Website</i><i>Call</i><i>Directions</i></span>
      </span></span>
      <i class="b-anchor" style="left:96px;top:296px"></i>
    </div></div>
  </div></div>
</div>'''

swap_chips = ''.join(f'<button type="button" class="tchip" data-k="{t["k"]}" aria-pressed="{"true" if i == 0 else "false"}">{t["name"]}</button>' for i, t in enumerate(TRADES3))

LAYERS = [
  ("Your land.", "Your domain is registered to your business on either plan. Choose the one-off build and every account sits in your name too, so the whole site is yours outright.", ["Your domain", "Yours outright"]),
  ("Solid foundations.", "Fast, reliable hosting with the padlock on every page and a security certificate that renews itself. No page builders and no plugins, so pages load quickly even on one bar of signal.", ["Secure as standard", "Quick to load"]),
  ("A frame planned for phones.", "Every page is planned from a blank page around what your customers need to know, phone first, with proper titles and headings that name your trade and the suburbs you cover.", ["Made for phones first", "Readable by Google"]),
  ("A finish that fits your trade.", "Designed around your business, whatever you do: your colours, your photos, your prices, and tools made for your customers. The demos have a warning-light guide for a mechanic and a problem finder for a tiler. A landscaper might get a quote calculator, and a plumber an after-hours call button.", ["Designed by hand", "No templates"]),
  ("The fit-out.", "An editor you can use from your phone, enquiries that land straight in your inbox, and your Google profile and socials linked up properly.", ["Owner editor", "Enquiries to your inbox", "Linked up properly"]),
]
lcards = ''.join(f'<li class="lcard rise" data-l="{i}"><span class="lno">0{i + 1}</span><h3>{t}</h3><p>{d}</p><ul class="tags">{"".join(f"<li>{g}</li>" for g in tags)}</ul></li>' for i, (t, d, tags) in enumerate(LAYERS))

STAGE = f'''
<div class="stage" id="stage">
  <div class="stage-pin">
    <canvas class="topo" id="topo" aria-hidden="true"></canvas>
    <div class="coords" aria-hidden="true"><span>Bokarina, Sunshine Coast</span><span>26&deg;44&prime;S 153&deg;08&prime;E</span></div>
    {BUILD}
    <svg class="leader" id="leader" aria-hidden="true"><path d=""/><circle r="5"/><circle class="halo" r="5"/></svg>
    <div class="tswap" role="group" aria-label="Show the finish from a different demo"><span>Try a demo finish</span>{swap_chips}</div>
  </div>
  <div class="stage-flow">
    <section class="hero">
      <div class="wrap">
        <div class="hero-copy">
          <h1 class="split hero-split">Websites for local businesses, built by hand and yours to own.</h1>
          <p class="lede rise hero-rise" style="--d:450ms">I'm Connor. I design and build custom websites for every kind of trade and service business across the Sunshine Coast and Brisbane, with an editor simple enough to use from your phone.</p>
          <div class="actions rise hero-rise" style="--d:600ms"><a class="btn" data-mag href="work.html">See the work</a><a class="btn ghost" data-mag href="pricing.html">Get a price</a></div>
        </div>
      </div>
      <div class="scrollcue" aria-hidden="true"></div>
    </section>
    <section class="layers" id="built" aria-labelledby="builtTitle">
      <div class="wrap">
        <div class="layers-col">
          <p class="eyebrow rise">From the ground up</p>
          <h2 class="split" id="builtTitle">What you're actually getting.</h2>
          <p class="lede rise">A website goes together a lot like a house on its own block. Here's every layer of a Freehold site, and what each one does for your business.</p>
          <ol class="lcards">{lcards}</ol>
        </div>
      </div>
    </section>
  </div>
</div>
'''

# ---------- visuals for the "what's different" section ----------
V_COLLAGE = ('<div class="collage">'
  '<figure class="frame c1"><img src="assets/kingpin-desktop.webp" alt="" width="1440" height="900" loading="lazy" decoding="async"></figure>'
  '<figure class="frame c2"><img src="assets/tessera-feature.webp" alt="" width="1440" height="900" loading="lazy" decoding="async"></figure>'
  '<figure class="frame c3"><img src="assets/hush-phone.webp" alt="" width="640" height="1385" loading="lazy" decoding="async"></figure></div>')
V_EDITOR = ('<div class="editor-wrap"><figure class="frame"><img src="assets/editor.webp" alt="" width="1440" height="900" loading="lazy" decoding="async"></figure>'
  '<div class="toast">Published. Live in about a minute.</div></div>')
V_DEED = ('<div class="deed"><h4>Certificate of title</h4><dl>'
  '<div><dt>Property</dt><dd>yourbusiness.com.au</dd></div><div><dt>Registered owner</dt><dd>You</dd></div>'
  '<div><dt>Estate</dt><dd>Freehold, owned outright</dd></div><div><dt>Monthly rent</dt><dd>None</dd></div>'
  '</dl><div class="seal">OWNED<br>OUTRIGHT</div></div>')
V_ROUTE = ('<div class="route"><svg viewBox="0 0 320 420" aria-hidden="true">'
  '<path class="ct" d="M20 60c60-30 110 10 150-10s80-40 120-20"/><path class="ct" d="M10 130c70-20 100 30 160 5s90-25 130-5"/>'
  '<path class="ct" d="M15 220c50-30 120 20 170-5s70-35 120-10"/><path class="ct" d="M25 300c60-20 100 25 150 0s80-30 125-5"/>'
  '<path class="ct" d="M20 380c70-25 110 15 160-5s60-20 120-5"/>'
  '<path class="coast" d="M262 8C250 90 272 150 252 214S246 334 222 414"/>'
  '<path class="road" pathLength="1" d="M222 52C236 92 224 122 230 150S214 300 192 378"/>'
  '<circle class="stop" cx="222" cy="52" r="6"/><circle class="stop" cx="192" cy="378" r="6"/>'
  '<circle class="pulse" cx="230" cy="150" r="7"/><circle class="home" cx="230" cy="150" r="7"/>'
  '<text x="120" y="57">Noosa</text><text x="96" y="146">Bokarina</text><text class="sub" x="96" y="162">Home base</text><text x="92" y="383">Brisbane</text>'
  '</svg><p>Set up at your place, anywhere between Noosa and Brisbane.</p></div>')

FEATS = [
  ("Built by hand, not dragged from a template.",
   "Every site starts from a blank page and is designed around your trade, whatever it is. That means things templates can't do, like the warning-light guide, tile problem finder and room-by-room checklist in my demos, and pages that load fast because there's nothing in them you don't need.", V_COLLAGE),
  ("An editor you'll actually use.",
   "Change your prices, your hours, your photos or your reviews from your phone, then press publish. No logins to other platforms and no code. It's live in about a minute.", V_EDITOR),
  ("Yours to own outright.",
   "That's what freehold means. Buy a site outright and it's set up on accounts in your name, so it belongs to you. Not to me, and not to a platform charging you rent every month.", V_DEED),
  ("Set up in person, or remotely.",
   "I come to your business, set everything up and show you how it all works. Further afield, we do the same thing over a remote session, with you watching every step.", V_ROUTE),
]
feat_items = ''.join(f'<article class="feat"><h3>{h}</h3><p>{p}</p><div class="fv-inline">{v}</div></article>' for h, p, v in FEATS)
feat_stage = ''.join(f'<div class="fv">{v}</div>' for _, _, v in FEATS)

STEPS = [
  ("A chat", "Twenty minutes at your place or on the phone. You tell me about the business, and I'll tell you honestly whether a new website would help. It's free."),
  ("A plan and a price", "A fixed price in writing and a clear list of what's included. A deposit books you in, then the work starts."),
  ("The build", "Usually two to three weeks. You see it come together, check every detail, and ask for changes along the way."),
  ("Handover", "I set it up at your business or over a remote session, walk you through the editor, and make sure everything works as agreed."),
]
steps_html = ''.join(f'<article class="pstep"><span class="n">0{i+1}</span><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(STEPS))

TRADES = ['Plumbers', 'Electricians', 'Builders', 'Landscapers', 'Painters', 'Roofers', 'Concreters', 'Mechanics', 'Tilers', 'Cleaners', 'Pool care', 'Pest control', 'Carpenters', 'Fencers']
marq = ''.join(f'<span>{t}<i></i></span>' for t in TRADES)

row1 = ''.join([shot('kingpin-desktop.webp', 'Kingpin Automotive demo', *D), shot('hush-phone.webp', 'Hush Home Cleaning demo on a phone', *PH, tall=True),
                shot('tessera-feature.webp', 'Tessera Tiling pattern studio', *D), shot('hush-desktop.webp', 'Hush Home Cleaning demo', *D),
                shot('kingpin-phone.webp', 'Kingpin demo on a phone', *PH, tall=True), shot('editor.webp', 'The owner editor', *D)])
row2 = ''.join([shot('tessera-desktop.webp', 'Tessera Tiling Co. demo', *D), shot('hush-feature.webp', 'Hush room-by-room checklist', *D),
                shot('tessera-phone.webp', 'Tessera demo on a phone', *PH, tall=True), shot('kingpin-feature.webp', 'Kingpin warning-light guide', *D),
                shot('hush-desktop.webp', 'Hush Home Cleaning demo', *D)])

LD = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Freehold",
      "description": "Custom websites for trades and local businesses on the Sunshine Coast and in Brisbane.",
      "telephone": PHONE_LINK, "email": EMAIL, "founder": "Connor Ransome", "url": SITE_URL,
      "address": {"@type": "PostalAddress", "addressLocality": "Bokarina", "addressRegion": "QLD", "postalCode": "4575", "addressCountry": "AU"},
      "areaServed": ["Sunshine Coast", "Brisbane"]}

home = f'''
{STAGE}
<section class="wall">
  <div class="wrap wall-head">
    <h2 class="split">Three demos. Any trade. No templates.</h2>
    <div class="rise">
      <p class="lede">A mechanic, a tiler and a home cleaner, built to show what's possible. Whatever your trade, your site starts from a blank page too, designed around what your customers need to know. All three demos are live for you to click through.</p>
      <a class="btn" data-mag href="work.html">Explore the demos</a>
    </div>
  </div>
  <div class="wall-stage" aria-hidden="true"><div class="wall-plane"><div class="wall-row">{row1}</div><div class="wall-row">{row2}</div></div></div>
</section>

<div class="marq" aria-hidden="true"><div class="marq-track">{marq}{marq}</div></div>

<section class="sec" id="different">
  <div class="wrap">
    <h2 class="split" style="max-width:16ch">What's different about a Freehold site.</h2>
    <div class="feats">
      <div class="feat-list">{feat_items}</div>
      <div class="feat-stage" aria-hidden="true">{feat_stage}</div>
    </div>
  </div>
</section>

<section class="proc" id="how">
  <div class="proc-pin">
    <div class="wrap proc-head">
      <h2 class="split">How it works.</h2>
      <p class="lede" style="margin:0">From the first chat to handover, usually in under a month.</p>
    </div>
    <div class="proc-rail">
      <div class="proc-line"><i></i></div>
      <div class="proc-track">
        {steps_html}
        <div class="proc-end"><p class="lede">It starts with a free chat. No obligation, and no jargon.</p><a class="btn" data-mag href="pricing.html#quote">Book a chat</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="about">
  <div class="wrap about">
    <h2 class="split">Hi, I'm Connor.</h2>
    <div class="rise">
      <p>I'm based in Bokarina and I build websites for the kind of businesses people actually rely on: <strong>the plumber, the sparky, the landscaper, the mechanic, and every trade in between.</strong> Most of them are stuck with an old site they can't change, or paying every month for a template that looks like everyone else's.</p>
      <p>Freehold is the alternative. A website made for your business, that you can update yourself, and that you can own outright if you'd rather not pay rent on it.</p>
      <ul class="contact-list">
        <li><span>Phone</span><a href="tel:{PHONE_LINK}">{PHONE}</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Based in</span>Bokarina, Sunshine Coast</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta-box">
      <span class="ln t"></span><span class="ln r"></span><span class="ln b"></span><span class="ln l"></span>
      <i class="pg"></i><i class="pg"></i><i class="pg"></i><i class="pg"></i>
      <h2 class="split">Let's build yours.</h2>
      <p class="lede">Tell me about your business and I'll come back with a fixed price, usually within a day.</p>
      <div class="actions"><a class="btn" data-mag href="pricing.html#quote">Get a quote</a><a class="btn ghost" data-mag href="tel:{PHONE_LINK}">Call {PHONE}</a></div>
    </div>
  </div>
</section>
'''

# =====================================================================
# WORK
# =====================================================================
CASES = [
  dict(id='lot-1', lot='Lot 1', acc='red', accent='#F05A4F', slug='kingpin', name='Kingpin Automotive', trade='Mechanic demo<br>Five pages',
       url='https://kingpinauto.netlify.app/',
       idea="A workshop website built around the questions people actually ring a mechanic about. The car on the home page puts itself together part by part, every part leads to a real price, and a dashboard of warning lights tells drivers how urgent theirs is before they book.",
       feats=['A car that assembles itself, with a price behind every part', 'Warning-light guide: how urgent it is and what to do', 'Every service priced, sorted by category', 'Online booking straight to the workshop inbox', 'Owner editor, locked to the owner’s own passphrase'],
       fig="The warning-light guide. Tap the light on your dash to see how urgent it is, what to do right now, and book it in."),
  dict(id='lot-2', lot='Lot 2', acc='glaze', accent='#7DB9A3', slug='tessera', name='Tessera Tiling Co.', trade='Tiler demo<br>Seven pages',
       url='https://tesseratiling.netlify.app/',
       idea="A tiler's website you can almost run your hand across. The home page lays a real 3D floor, from waterproofing to grout, then takes it apart as you scroll to show the five layers nobody sees. A problem finder, a showroom and a quote planner do the selling.",
       feats=['Live 3D floor, laid and taken apart as you scroll', 'Problem finder for cracked, drummy or leaking tiles', 'Showroom with a pattern and grout studio', 'Five-step quote planner with photo uploads', 'Owner editor for prices, photos, projects and more'],
       fig="The pattern studio. Pick a tile, a layout and a grout colour, and see the floor change before anyone lays a thing."),
  dict(id='lot-3', lot='Lot 3', acc='violet', accent='#A38BEB', slug='hush', name='Hush Home Cleaning', trade='Cleaner demo<br>Five pages', pass_='5829',
       url='demos/hush/index.html', editor='demos/hush/admin.html',
       idea="A cleaning company built around the worries people have about letting someone into their home. It opens on a fogged window being squeegeed clean, prices every clean instantly, and shows exactly what gets done in each room.",
       feats=['Fogged-window squeegee opening', 'Instant quote that carries through to booking', 'Tap-a-room cleaning checklist', 'Wipe transitions between pages', 'Owner editor that controls every price'],
       fig="The room-by-room checklist. Choose a room and a kind of clean to see exactly what's included."),
]
PAUSE = '<svg class="pause" viewBox="0 0 14 14"><rect x="2" y="1" width="3.5" height="12"/><rect x="8.5" y="1" width="3.5" height="12"/></svg><svg class="play" viewBox="0 0 14 14"><path d="M3 1l10 6-10 6z"/></svg>'
def case(c):
    feats = ''.join(f'<li><span>{f}</span></li>' for f in c['feats'])
    if c.get('editor'):
        ed = (f'<a class="btn ghost" data-mag href="{c["editor"]}" target="_blank" rel="noopener">Try the editor {EXT}</a>'
              f'<span class="passcode">Passcode<b>{c["pass_"]}</b></span>')
    else:
        ed = '<span class="passcode">Its editor is locked to the owner’s passphrase, so ask me and I’ll walk you through it.</span>'
    return f'''
<section class="case" id="{c['id']}" data-acc="{c['acc']}">
  <div class="wrap">
    <div class="case-head"><span class="lot">{c['lot']}</span><h2 class="split">{c['name']}</h2><span class="trade">{c['trade']}</span></div>
    <div class="stage-dev"><div class="stage-in">
      <div class="laptop"><div class="scr">
        <video muted loop playsinline preload="none" poster="assets/{c['slug']}-poster.webp" aria-label="Screen recording of the {c['name']} demo"><source src="assets/{c['slug']}.webm" type="video/webm"><source src="assets/{c['slug']}.mp4" type="video/mp4"></video>
        <button class="vtoggle paused" type="button" aria-label="Play or pause the recording">{PAUSE}</button>
      </div><div class="base"></div></div>
      <figure class="phone"><img src="assets/{c['slug']}-phone.webp" alt="The {c['name']} demo on a phone" width="640" height="1385" loading="lazy" decoding="async"></figure>
    </div></div>
    <div class="case-body">
      <div class="rise">
        <p class="idea">{c['idea']}</p>
        <div class="case-actions">
          <a class="btn" data-mag href="{c['url']}" target="_blank" rel="noopener">Open the demo {EXT}</a>
          {ed}
        </div>
      </div>
      <ul class="pegs rise" style="--d:150ms">{feats}</ul>
    </div>
    <figure class="figure"><div class="frame"><img src="assets/{c['slug']}-feature.webp" alt="{c['fig'].split('.')[0]} in the {c['name']} demo" width="1440" height="900" loading="lazy" decoding="async"></div><figcaption>{c['fig']}</figcaption></figure>
  </div>
</section>'''

def parcel(c, d, lx):
    return (f'<g class="parcel" tabindex="0" role="link" data-go="{c["id"]}" style="--acc:{c["accent"]}" aria-label="{c["lot"]}, {c["name"]}">'
            f'<path pathLength="1" d="{d}"/>'
            f'<text class="lt" x="{lx}" y="92">{c["lot"].upper()}</text>'
            f'<text class="nm" x="{lx}" y="130">{c["name"]}</text>'
            f'<text class="tr" x="{lx}" y="156">{c["trade"].split("<br>")[0]}</text></g>')
lotmap = ('<div class="lotmap rise"><svg viewBox="0 0 1200 380" role="group" aria-label="Survey plan of the three demos. Choose one to jump to it.">'
  '<path class="ct" d="M0 70c200-40 380 30 600 0s420-50 600-10"/><path class="ct" d="M0 170c220-30 400 40 620 10s380-40 580-5"/>'
  '<path class="ct" d="M0 270c180-35 420 35 610 5s400-45 590-10"/><path class="ct" d="M0 350c240-30 380 25 600 0s420-30 600-5"/>'
  + parcel(CASES[0], 'M40 40 L420 30 L445 330 L60 350 Z', 80)
  + parcel(CASES[1], 'M420 30 L790 50 L770 340 L445 330 Z', 470)
  + parcel(CASES[2], 'M790 50 L1160 36 L1150 350 L770 340 Z', 820)
  + '</svg></div>')
lotlist = '<ul class="lotlist">' + ''.join(f'<li><a href="#{c["id"]}"><b>{c["name"]}</b><span>{c["lot"]}</span></a></li>' for c in CASES) + '</ul>'

work = f'''
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">The work.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">Three demo websites, each built from a blank page to show what's possible. They're examples, not templates: whatever your trade, your site is designed around your business and your customers. Every demo is live, so open one and click around like a customer would.</p>
    {lotmap}
    {lotlist}
  </div>
</section>
{''.join(case(c) for c in CASES)}
<section class="sec">
  <div class="wrap">
    <div class="cta-box">
      <span class="ln t"></span><span class="ln r"></span><span class="ln b"></span><span class="ln l"></span>
      <i class="pg"></i><i class="pg"></i><i class="pg"></i><i class="pg"></i>
      <h2 class="split">Your trade next.</h2>
      <p class="lede">Plumber, painter, landscaper or anything else, every site starts from a blank page. Tell me about your business and I'll show you what yours could look like.</p>
      <div class="actions"><a class="btn" data-mag href="pricing.html#quote">Get a quote</a><a class="btn ghost" data-mag href="pricing.html">See pricing</a></div>
    </div>
  </div>
</section>
'''

# =====================================================================
# PRICING
# =====================================================================
def pegs(items): return '<ul class="pegs">' + ''.join(f'<li><span>{i}</span></li>' for i in items) + '</ul>'
FAQ = [
  ("Do I need to know anything technical?", "No. I set everything up, and the editor is plain boxes and a publish button. If you can fill in a form, you can update your website."),
  ("What's the real difference between the two plans?", "Who holds the keys, and how you pay. Freehold costs more upfront and then it's entirely yours. Looked after costs less to start, and I host it and handle the technical side for a monthly fee."),
  ("What does owning it outright actually mean?", "Once a Freehold site is paid for, it lives on accounts in your name and the site is yours. You can keep it forever, move it, or have someone else work on it. Nothing stops working if you never speak to me again."),
  ("Is there a lock-in on the subscription?", "No. There's no minimum term and no exit fee. Give me 30 days' notice whenever you like, and your monthly price stays the same for your first 12 months."),
  ("What happens if I leave the subscription?", "Your content and your domain are yours. I'll send you an export of your content within 30 days of asking and transfer your domain to you. The website itself runs on my accounts, so it stays with me."),
  ("Will I be number one on Google?", "Nobody can honestly promise that, and Google says so itself. I build every site so Google can read it properly. Your Google Business Profile and your reviews do most of the rest, and that usually takes months."),
  ("I already have a website. Can you replace it?", "Yes. Your domain and your email stay exactly as they are, and the new site switches over on a day that suits you."),
  ("How long does it take?", "Usually two to three weeks from the deposit to going live. Most of that depends on how quickly we can pull together your details, photos and approvals."),
  ("Do you work outside the Sunshine Coast?", "In person, anywhere between Noosa and Brisbane. Further away, we do everything over a remote session, with you watching each step on your own screen."),
  ("Who writes the words on the site?", "You know your business, so you supply the details: services, prices, photos and what makes you different. I shape them into clear, plain-English pages, and you approve every word before it goes live. Professional copywriting isn't included."),
]
faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

def chips(name, options, kind='radio', checked=None, group_id=None):
    gid = f' id="{group_id}"' if group_id else ''
    inner = ''.join(f'<label class="chip"><input type="{kind}"{f" name={json.dumps(name)}" if name else ""} value="{o}"{" checked" if o == checked else ""}><span>{o}</span></label>' for o in options)
    return f'<div class="chips"{gid}>{inner}</div>'

FINE = [
  ("Extra pages", f'Both plans include up to <span data-price="pages">{PRICE["pages"]}</span> pages. More are <span data-price="extraPage">{money(PRICE["extra_page"])}</span> each.'),
  ("Bigger changes", f'<span data-price="hourly">{money(PRICE["hourly"])}</span> an hour, in 30-minute blocks, and always quoted before I start.'),
  ("Paying", "A deposit books you in. On Freehold, the balance is due before your site goes live. On Looked after, the balance is paid with your first monthly fee, and months are billed in advance. Invoices are due within 7 days."),
  ("Your domain", "It belongs to your business. On the subscription I can register and renew it for you, and I'll transfer it into your name whenever you ask."),
  ("No lock-in", "The subscription has no minimum term and no exit fee. Cancel with 30 days' notice, and your monthly price is fixed for your first 12 months."),
  ("Leaving the subscription", "Your content export is free, and your domain moves to you. The website itself runs on my accounts, so it stays with me."),
  ("Google rankings", "Every site is built so Google can read it properly. Nobody can honestly guarantee a top spot, so I don't."),
  ("Not included", "Online shops, professional copywriting and photography, ongoing SEO campaigns and paid advertising. I'm happy to point you to someone good."),
]
fine = ''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in FINE)

def payline(items):
    """A survey line with three pegs: how the money is paid, step by step."""
    li = ''.join(f'<li style="--i:{i}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(items))
    return f'<ol class="payline">{li}</ol>'

PAY_OWN = payline([(f'<span data-price="freehold.deposit">{money(ONEOFF_DEP)}</span>', f'<span data-price="freehold.depositPct">{PRICE["oneoff_pct"]}%</span> deposit to book'),
                   (f'<span data-price="freehold.balance">{money(PRICE["oneoff"] - ONEOFF_DEP)}</span>', 'balance before go-live'),
                   ('$0', 'a month, ever. It’s yours')])
PAY_SUB = payline([(f'<span data-price="managed.deposit">{money(START_DEP)}</span>', f'<span data-price="managed.depositPct">{PRICE["start_pct"]}%</span> deposit to book'),
                   (f'<span data-price="managed.balance">{money(PRICE["start"] - START_DEP)}</span>', 'balance, with your first month'),
                   (f'<span data-price="managed.monthly">{money(PRICE["monthly"])}</span>', 'a month after that')])

pricing = f"""
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">Straight prices.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">Two ways to get a website from me. Both are built by hand, both come with an editor you can use from your phone, and both prices are here in writing, not hidden behind a phone call.</p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="plans rise">
      <article class="plan primary">
        <h2>Freehold</h2>
        <p class="tag">Own it outright</p>
        <div class="price"><b data-price="freehold.price">{money(PRICE["oneoff"])}</b><span>once</span></div>
        <p class="desc">Your website, set up on accounts in your name and fully yours once it's paid for. Nothing to pay me each month.</p>
        {PAY_OWN}
        {pegs([f'Custom design and build, up to <span data-price="pages">{PRICE["pages"]}</span> pages', 'Owner editor with one-click publishing', 'Enquiry or booking form straight to your inbox', 'Built so Google can read every page', 'Set up on your own accounts, in person or remotely', 'Full ownership of the site once it is paid for'])}
        <p class="terms">After launch, changes are free with your editor, or <span data-price="hourly">{money(PRICE["hourly"])}</span> an hour if you'd rather I do them.</p>
        <a class="btn" data-mag data-plan-pick="Freehold" href="#quote">Get a quote for Freehold</a>
      </article>
      <article class="plan">
        <h2>Looked after</h2>
        <p class="tag">I look after it for you</p>
        <div class="price"><b data-price="managed.start">{money(PRICE["start"])}</b><span>to start, then <span data-price="managed.monthly">{money(PRICE["monthly"])}</span> a month</span></div>
        <p class="desc">Hosting, your domain, security and small changes are all handled. Use the editor for everyday updates, or just send me a text.</p>
        {PAY_SUB}
        {pegs([f'Custom design and build, up to <span data-price="pages">{PRICE["pages"]}</span> pages', 'A simple editor for everyday updates', 'Hosting, security certificate and your domain handled', f'Up to <span data-price="changes">{PRICE["changes"]}</span> small changes a month, done within 2 business days', 'Enquiry or booking form straight to your inbox', 'Set up remotely, with no accounts for you to create'])}
        <p class="terms">Billed monthly in advance. No minimum term and no exit fee: cancel with 30 days' notice. Your monthly price is fixed for the first 12 months.</p>
        <a class="btn ghost" data-mag data-plan-pick="Looked after" href="#quote">Get a quote for Looked after</a>
      </article>
    </div>

    <div class="compare rise">
      <div class="crow"><span></span><span>Freehold</span><span>Looked after</span></div>
      <div class="crow"><span>Who holds the accounts</span><span>You, in your own name</span><span>Me, so you never have to</span></div>
      <div class="crow"><span>Upfront</span><span><span data-price="freehold.price">{money(PRICE["oneoff"])}</span></span><span><span data-price="managed.start">{money(PRICE["start"])}</span></span></div>
      <div class="crow"><span>Each month</span><span>Nothing</span><span><span data-price="managed.monthly">{money(PRICE["monthly"])}</span></span></div>
      <div class="crow"><span>Changes after launch</span><span>You, with the editor</span><span>You, plus <span data-price="changes">{PRICE["changes"]}</span> small changes a month from me</span></div>
      <div class="crow"><span>Lock-in</span><span>None. It's yours</span><span>None. 30 days' notice</span></div>
      <div class="crow"><span>First-year total</span><span><span data-price="freehold.price">{money(PRICE["oneoff"])}</span>, plus your domain</span><span><span data-price="managed.firstYear">{money(PRICE["start"] + PRICE["monthly"] * 12)}</span>, domain included</span></div>
      <div class="crow"><span>If you ever leave</span><span>Nothing to move. It's all yours</span><span>Your content and domain go with you</span></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0" id="fine-print">
  <div class="wrap">
    <h2 class="split">The fine print, in plain English.</h2>
    <dl class="fine rise">{fine}</dl>
    <p class="fine-note">All prices are in Australian dollars. Every job is covered by a written agreement before any work starts.</p>
  </div>
</section>

<section class="sec" style="padding-top:0" id="quote">
  <div class="wrap">
    <h2 class="split">Get a quote.</h2>
    <p class="lede rise" style="margin-top:1.2rem">Tell me about your business. I'll come back with a fixed price, usually within a day.</p>
    <div class="sheet rise">
      <form id="quoteForm" name="quote" method="POST" data-netlify="true" netlify-honeypot="botcheck" novalidate>
        <input type="hidden" name="Summary" value="">
        <fieldset class="fset">
          <legend>About you</legend>
          <div class="row">
            <div class="fld"><label for="fName">Your name</label><input id="fName" name="Name" type="text" autocomplete="name" placeholder="Jess Carter"></div>
            <div class="fld"><label for="fBiz">Business name</label><input id="fBiz" name="Business" type="text" autocomplete="organization" placeholder="Carter Plumbing"></div>
          </div>
          <div class="row">
            <div class="fld"><label for="fPhone">Phone</label><input id="fPhone" name="Phone" type="tel" autocomplete="tel" placeholder="0412 345 678"></div>
            <div class="fld"><label for="fEmail">Email</label><input id="fEmail" name="email" type="email" autocomplete="email" placeholder="jess@carterplumbing.com.au"></div>
          </div>
          <div class="row">
            <div class="fld"><label for="fTrade">What you do</label><input id="fTrade" name="Trade" type="text" placeholder="Plumbing, mostly residential"></div>
            <div class="fld"><label for="fSuburb">Suburb</label><input id="fSuburb" name="Suburb" type="text" autocomplete="address-level2" placeholder="Buderim"></div>
          </div>
          <div class="fld"><label for="fSite">Current website, if you have one</label><input id="fSite" name="Current website" type="text" placeholder="carterplumbing.com.au"></div>
        </fieldset>
        <fieldset class="fset">
          <legend>What you're after</legend>
          <div class="fld"><span class="label">Plan</span>{chips('Plan', ['Freehold', 'Looked after', 'Not sure yet'], checked='Not sure yet')}</div>
          <div class="fld"><span class="label">What would help</span>{chips('', ['A new website', 'Replace my current site', 'Online bookings', 'A price or quote calculator'], kind='checkbox', group_id='needs')}</div>
          <div class="fld"><span class="label">When</span>{chips('When', ['As soon as possible', 'In the next month or two', 'Just looking for now'], checked='In the next month or two')}</div>
        </fieldset>
        <fieldset class="fset">
          <legend>Anything else</legend>
          <div class="fld"><label for="fMsg">Tell me about the business</label><textarea id="fMsg" name="Message" placeholder="Two vans, mostly Buderim and Mooloolaba. The current site is ten years old and I can't change anything on it."></textarea></div>
        </fieldset>
        <input type="hidden" name="What would help" id="fNeeds" value="">
        <p class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="botcheck" tabindex="-1" autocomplete="off"></label></p>
        <input type="hidden" name="subject" value="Quote request from freeholdweb.com.au">
        <button class="btn" type="submit" id="sendBtn" data-mag>Send it through</button>
        <p class="ferr" id="ferr" role="alert"></p>
        <p class="fnote">I'll only use your details to reply to you. See the <a href="privacy.html">privacy policy</a> for how they're handled.</p>
      </form>
      <div class="lodged" id="lodged" role="status">
        <div class="stamp"><span>LODGED<small>Freehold, Bokarina</small></span></div>
        <h3>Got it. Thanks.</h3>
        <p>I'll be in touch with a fixed price, usually within a day. If it's urgent, call or text {PHONE}.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap" style="max-width:980px">
    <h2 class="split">Questions.</h2>
    <div class="faq rise">{faq}</div>
  </div>
</section>
"""

# =====================================================================
# PRIVACY
# =====================================================================
privacy = f"""
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">Privacy.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">What happens to your details when you contact or work with Freehold, in plain English.</p>
  </div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap">
    <article class="doc rise">
      <p class="updated">Last updated 22 October 2026</p>
      <p>Freehold is a web design business run by Connor Ransome from Bokarina, Queensland, under the registered business name Freehold Web (ABN {ABN}). This policy explains what personal information I collect, why I collect it, how I look after it, and what you can ask me to do with it. I aim to handle personal information in line with the Australian Privacy Principles.</p>

      <h2>What I collect</h2>
      <p><strong>If you get in touch.</strong> When you use the quote form, email, call or text me, I collect what you choose to send, which can include:</p>
      <ul>
        <li>your name and the name of your business</li>
        <li>your phone number and email address</li>
        <li>your suburb and your current website address</li>
        <li>what you're looking for, and anything you write in your message</li>
      </ul>
      <p><strong>If you become a client.</strong> To prepare your agreement, build your website and invoice you, I also collect your business's legal name, ABN and address, and the content you give me for your site, such as text, photos and logos. During setup you may also give me access to accounts like your domain registrar or hosting.</p>
      <p><strong>If you just browse this site.</strong> You don't need an account, and I don't run analytics or advertising trackers. The company that hosts the site keeps standard technical logs, explained below.</p>

      <h2>Why I collect it</h2>
      <p>To reply to you, prepare a quote, deliver the work we agree on, invoice you, support your website afterwards, and keep the records the law requires. I won't add you to a mailing list or use your details for marketing unless you ask me to.</p>
      <p>If you agree to it, I may show your finished website as an example of my work. I'll only ever show the public website itself, never your private details.</p>

      <h2>Logins and account access</h2>
      <p>I only ask for the minimum access needed to do the job. Logins are kept in an encrypted password manager, never in emails or messages, and I use two-step verification wherever it's available.</p>
      <ul>
        <li><strong>Freehold (one-off) sites</strong> are set up on accounts in your name. Once the handover is finished, I don't keep access to them.</li>
        <li><strong>Looked after (subscription) sites</strong> are hosted on my own accounts, so you never need to give me your logins to keep them running.</li>
      </ul>
      <p>When you no longer need me to have access to something, you can remove it at any time, and I'll remind you to.</p>

      <h2>Who else sees it</h2>
      <p>I don't sell, rent or trade your information. A small number of trusted services help me run Freehold, and they only receive what's needed for their part:</p>
      <ul>
        <li><strong>Website hosting.</strong> This site and subscription sites are hosted by Netlify, which keeps standard server logs such as IP addresses and browser types for security and performance. Quote requests sent through this site's form are received and stored by Netlify and emailed on to me. Website code and content are stored with GitHub.</li>
        <li><strong>Email.</strong> Messages to {EMAIL} are stored with my business email provider.</li>
        <li><strong>Domains.</strong> When a domain is registered, the registrant's details go to the domain registrar and the .au registry, as their rules require.</li>
        <li><strong>Payments.</strong> If you pay by card, your card details are handled by the payment provider. I never see or store full card numbers.</li>
      </ul>
      <p>I may also disclose information if the law requires it.</p>
      <p>Some of these providers store data outside Australia, including in the United States. I only use established providers with their own security and privacy commitments.</p>

      <h2>Cookies and your browser</h2>
      <p>This site doesn't use advertising cookies, tracking pixels or analytics. It saves a few small things in your own browser: your choice if you turn the site's animations on or off, whether you've already seen the opening animation, and any practice edits you make in the demo editor on the work page. They stay on your device and are never sent to me.</p>

      <h2>Websites I build for clients</h2>
      <p>If you've visited a website I built for another business, that business decides what its website collects and is responsible for its own privacy policy. Contact them about how they handle your information. Where I host the site, I'll help them answer any request.</p>

      <h2>Keeping it secure</h2>
      <p>I take reasonable steps to protect the information I hold, including strong passwords, two-step verification and limiting who and what can access it. No system is completely immune to attack, so if a breach happens that's likely to cause you serious harm, I'll tell you promptly and explain what I'm doing about it.</p>

      <h2>How long I keep it</h2>
      <p>If an enquiry doesn't go ahead, I delete it within 12 months. For clients, I keep agreements, invoices and related records for five years after our last transaction, as Australian tax law requires, and other project details only for as long as they're useful for supporting your site.</p>

      <h2>Seeing, correcting or deleting your information</h2>
      <p>You can ask what information I hold about you, ask me to correct it, or ask me to delete anything I'm not required to keep. I may need to confirm who you are first, and I'll respond within 30 days.</p>

      <h2>Concerns or complaints</h2>
      <p>If you're unhappy with how I've handled your information, please contact me first so I can put it right. I'll respond within 30 days. If you're still not satisfied, you can contact the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener">oaic.gov.au</a>.</p>

      <h2>Contact</h2>
      <p>Connor Ransome, Freehold<br>Bokarina QLD 4575<br><a href="tel:{PHONE_LINK}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>

      <h2>Changes to this policy</h2>
      <p>If this policy changes, the new version will be posted here with a new date at the top.</p>
    </article>
  </div>
</section>
"""

notfound = """
<section class="nf">
  <div class="wrap">
    <p class="nf-code" aria-hidden="true">404</p>
    <h1 class="split hero-split">This lot hasn't been surveyed.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">The page you're after has moved or never existed. Let's get you back on solid ground.</p>
    <div class="actions rise hero-rise" style="--d:450ms"><a class="btn" data-mag href="/">Back to the home page</a><a class="btn ghost" data-mag href="/work.html">See the work</a></div>
  </div>
</section>
"""

PAGES = {
  'index.html': page('home', 'Freehold — Custom websites for Sunshine Coast businesses',
                     'Custom websites for trades and local businesses on the Sunshine Coast and in Brisbane. Built by hand, with an editor you can use from your phone, and yours to own outright.',
                     None, home, f'<link rel="preload" href="assets/kingpin-desktop.webp" as="image">\n<script type="application/ld+json">{json.dumps(LD)}</script>\n', veil=False),
  'work.html': page('work', 'The work — Freehold', 'Three working demo websites, for a mechanic, a tiler and a home cleaner, showing what a custom website can do for any trade.', 'work', work),
  'pricing.html': page('pricing', 'Pricing — Freehold', f'Straight prices for a custom website: own it outright for {money(PRICE["oneoff"])}, or have it looked after for {money(PRICE["start"])} to start and {money(PRICE["monthly"])} a month.', 'pricing', pricing),
  'privacy.html': page('privacy', 'Privacy — Freehold', 'How Freehold collects, uses and protects your personal information.', None, privacy),
  '404.html': page('notfound', 'Page not found — Freehold', 'This page could not be found.', None, notfound, '<meta name="robots" content="noindex">\n', P='/'),
}
for fn, html in PAGES.items():
    open(fn, 'w').write(html)
    print(fn, len(html), 'bytes')
