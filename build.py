import json
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
# Runs before anything paints: decides calm mode (OS reduce-motion, unless the visitor chose full
# animations) and whether the first-visit intro plays. Calm pages also skip the page transition.
CALM_JS = ("(function(){var d=document.documentElement;d.classList.add('js');try{"
  "var pref=matchMedia('(prefers-reduced-motion: reduce)').matches,s=localStorage.getItem('fh-motion');"
  "if(pref)d.classList.add('prefers-calm');"
  "if(s==='calm'||(pref&&s!=='full'))d.classList.add('calm');"
  "else if(!sessionStorage.getItem('fh-intro')){d.classList.add('intro');sessionStorage.setItem('fh-intro','1');}"
  "}catch(e){}"
  "addEventListener('pagereveal',function(e){if(e.viewTransition&&d.classList.contains('calm'))e.viewTransition.skipTransition();});})();")

def letters(word, cls=''):
    return ''.join(f'<span style="--i:{i}">{c}</span>' for i, c in enumerate(word))

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
<script>{CALM_JS}</script>
{extra}</head>'''

def nav(active, P=''):
    items = [('work', 'work.html', 'Work'), ('pricing', 'pricing.html', 'Pricing'), ('about', 'index.html#about', 'About')]
    CUR = ' aria-current="page"'
    links = ''.join(f'<a href="{P}{u}"{CUR if k == active else ""}>{l}</a>' for k, u, l in items)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="gridlines" aria-hidden="true"><i></i></div>
<div class="veil" id="veil" aria-hidden="true"><div class="intro-box"><span class="ln t"></span><span class="ln r"></span><span class="ln b"></span><span class="ln l"></span><i class="pg"></i><i class="pg"></i><i class="pg"></i><i class="pg"></i><div class="intro-word">{letters("FREEHOLD")}</div><p class="intro-cap">Bokarina, Sunshine Coast</p></div></div>
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
</footer>'''

def page(name, title, desc, active, body, extra_head='', P=''):
    return f'''{head(title, desc, extra_head, P)}
<body data-page="{name}">
{nav(active, P)}
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

# ---------- visuals for the "what's different" section ----------
V_COLLAGE = ('<div class="collage">'
  '<figure class="frame c1"><img src="assets/ironbark-desktop.webp" alt="" width="1440" height="900" loading="lazy" decoding="async"></figure>'
  '<figure class="frame c2"><img src="assets/copperline-feature.webp" alt="" width="1440" height="900" loading="lazy" decoding="async"></figure>'
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
   "Every site starts from a blank page and is designed around your trade. That means things templates can't do, like a live workshop board, a price calculator or a room-by-room checklist, and pages that load fast because there's nothing in them you don't need.", V_COLLAGE),
  ("An editor you'll actually use.",
   "Change your prices, your hours, your reviews or what's on today from your phone, then press publish. No logins to other platforms and no code. It's live in about a minute.", V_EDITOR),
  ("Yours to own outright.",
   "That's what freehold means. Buy a site outright and it's set up on accounts in your name, so it belongs to you. Not to me, and not to a platform charging you rent every month.", V_DEED),
  ("Set up in person, or remotely.",
   "I come to your business, set everything up and show you how it all works. Further afield, we do the same thing over a remote session, with you watching every step.", V_ROUTE),
]
feat_items = ''.join(f'<article class="feat"><h3>{h}</h3><p>{p}</p><div class="fv-inline">{v}</div></article>' for h, p, v in FEATS)
feat_stage = ''.join(f'<div class="fv">{v}</div>' for _, _, v in FEATS)

STEPS = [
  ("A chat", "Twenty minutes at your place or on the phone. You tell me about the business, and I'll tell you honestly whether a new website would help. It's free."),
  ("A plan and a price", "A fixed price in writing and a clear list of what's included. A deposit books you in, and the balance is due before your site goes live."),
  ("The build", "Usually two to three weeks. You see it come together, check every detail, and ask for changes along the way."),
  ("Handover", "I set it up at your business or over a remote session, walk you through the editor, and make sure everything works as agreed."),
]
steps_html = ''.join(f'<article class="pstep"><span class="n">0{i+1}</span><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(STEPS))

TRADES = ['Mechanics', 'Electricians', 'Home cleaners', 'Plumbers', 'Landscapers', 'Builders', 'Painters', 'Pool care']
marq = ''.join(f'<span>{t}<i></i></span>' for t in TRADES)

row1 = ''.join([shot('ironbark-desktop.webp', 'Ironbark Motor Works demo', *D), shot('hush-phone.webp', 'Hush Home Cleaning demo on a phone', *PH, tall=True),
                shot('copperline-feature.webp', 'Copperline Electrical safety check', *D), shot('hush-desktop.webp', 'Hush Home Cleaning demo', *D),
                shot('ironbark-phone.webp', 'Ironbark demo on a phone', *PH, tall=True), shot('editor.webp', 'The owner editor', *D)])
row2 = ''.join([shot('copperline-desktop.webp', 'Copperline Electrical demo', *D), shot('hush-feature.webp', 'Hush room-by-room checklist', *D),
                shot('copperline-phone.webp', 'Copperline demo on a phone', *PH, tall=True), shot('ironbark-feature.webp', 'Ironbark symptom checker', *D),
                shot('hush-desktop.webp', 'Hush Home Cleaning demo', *D)])

LD = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Freehold",
      "description": "Custom websites for trades and local businesses on the Sunshine Coast and in Brisbane.",
      "telephone": PHONE_LINK, "email": EMAIL, "founder": "Connor Ransome", "url": SITE_URL,
      "address": {"@type": "PostalAddress", "addressLocality": "Bokarina", "addressRegion": "QLD", "postalCode": "4575", "addressCountry": "AU"},
      "areaServed": ["Sunshine Coast", "Brisbane"]}


ICONS = {
  'phone': '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>',
  'search': '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5.5 5.5"/>',
  'fast': '<path d="M13 2.5 4.5 13.5H11l-1 8 8.5-11H12z"/>',
  'inbox': '<path d="M3 13.5 6 5h12l3 8.5V19H3z"/><path d="M3 13.5h5l1.2 2.2h5.6l1.2-2.2h5"/>',
  'lock': '<rect x="5" y="10.5" width="14" height="10.5" rx="1.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
  'share': '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="5.5" r="2.5"/><circle cx="18" cy="18.5" r="2.5"/><path d="m8.2 10.8 7.6-4.1M8.2 13.2l7.6 4.1"/>',
}
INCLUDED = [
  ('phone', 'Made for phones first', "Most customers will find you on their phone, so that's where every page is designed first, then scaled up."),
  ('search', 'Readable by Google', 'Proper titles, headings and descriptions that name your trade and the suburbs you cover. The foundations, done right.'),
  ('fast', 'Quick to load', 'No page builders and no plugins. Pages stay small and fast, even on one bar of signal.'),
  ('inbox', 'Enquiries to your inbox', 'Contact, booking or quote forms that land straight in your email, ready to reply to.'),
  ('lock', 'Secure as standard', 'The padlock on every page, with a free security certificate that renews itself.'),
  ('share', 'Linked up properly', 'Your Google profile and socials connected, and a tidy preview whenever someone shares your link.'),
]
inc_cards = ''.join(f'<article class="inc rise" style="--d:{i * 70}ms"><span class="inc-ic"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg></span><h3>{t}</h3><p>{d}</p></article>' for i, (k, t, d) in enumerate(INCLUDED))
INCLUDED_HTML = f"""
<section class="sec" id="included">
  <div class="wrap">
    <div class="inc-head"><h2 class="split">In every site, as standard.</h2><p class="lede rise">Whichever plan you choose, these come built in. No upsells for the basics.</p></div>
    <div class="inc-grid">{inc_cards}</div>
  </div>
</section>
"""

def founding_band(P=''):
    return f"""
<section class="sec founding-only" style="padding-top:0">
  <div class="wrap">
    <div class="fband rise">
      <div class="fband-copy">
        <h2>Founding clients get founding prices.</h2>
        <p>My first five clients get a Freehold site for <b data-price="freehold.founding">$900</b> instead of <span data-price="freehold.standard">$1,200</span>. In return, I'll ask for a short review once you're happy, and to show your site as part of my work.</p>
        <a class="btn" data-mag data-plan-pick="Freehold" href="{P}pricing.html#quote">Claim a founding spot</a>
      </div>
      <div class="fband-spots">
        <div class="fpegs" id="fpegs" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
        <p><b id="spotsLeft">5</b> of <span id="spotsOf">5</span> founding spots left</p>
      </div>
    </div>
  </div>
</section>
"""

home = f'''
<section class="hero">
  <canvas class="topo" id="topo" aria-hidden="true"></canvas>
  <div class="coords" aria-hidden="true"><span>Bokarina, Sunshine Coast</span><span>26&deg;44&prime;S 153&deg;08&prime;E</span></div>
  <div class="wrap">
    <div class="bigword" id="bigword" aria-hidden="true">{letters("FREEHOLD")}</div>
    <div class="hero-row">
      <h1 class="split hero-split">Websites for local businesses, built by hand and yours to own.</h1>
      <div class="hero-side rise hero-rise" style="--d:450ms">
        <p class="lede">I'm Connor. I design and build custom websites for trades and service businesses across the Sunshine Coast and Brisbane, with an editor simple enough to use from your phone.</p>
        <div class="actions"><a class="btn" data-mag href="work.html">See the work</a><a class="btn ghost" data-mag href="pricing.html">Get a price</a></div>
      </div>
    </div>
  </div>
  <div class="scrollcue" aria-hidden="true"></div>
</section>

<section class="wall">
  <div class="wrap wall-head">
    <h2 class="split">Three trades. Three websites. No templates.</h2>
    <div class="rise">
      <p class="lede">A mechanic, an electrician and a home cleaner. Each one designed from a blank page around what that trade's customers need to know, and each one live for you to click through.</p>
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
{INCLUDED_HTML}
<section class="sec" id="about">
  <div class="wrap about">
    <h2 class="split">Hi, I'm Connor.</h2>
    <div class="rise">
      <p>I'm based in Bokarina and I build websites for the kind of businesses people actually rely on: <strong>the mechanic, the sparky, the cleaner.</strong> Most of them are stuck with an old site they can't change, or paying every month for a template that looks like everyone else's.</p>
      <p>Freehold is the alternative. A website made for your business, that you can update yourself, and that you can own outright if you'd rather not pay rent on it.</p>
      <ul class="contact-list">
        <li><span>Phone</span><a href="tel:{PHONE_LINK}">{PHONE}</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Based in</span>Bokarina, Sunshine Coast</li>
      </ul>
    </div>
  </div>
</section>

{founding_band()}
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

# ---------- WORK ----------
CASES = [
  dict(id='lot-1', lot='Lot 1', acc='amber', slug='ironbark', name='Ironbark Motor Works', trade='Mechanic<br>One page', pass_='4060',
       idea="A workshop website that feels like the workshop. It opens on a roller door that lifts to show a live board of what's on the hoist, a price for every common job, and a \u201cwhat's that noise?\u201d tool that tells customers what's probably wrong before they ring.",
       feats=['Roller door opening', 'Live workshop board the owner updates from their phone', 'Symptom checker with typical prices', 'Open or closed light, from the real local time', 'Owner editor with one-click publishing'],
       fig="The symptom checker. Pick what the car's doing and it explains the likely cause, how urgent it is, and roughly what it costs."),
  dict(id='lot-2', lot='Lot 2', acc='copper', slug='copperline', name='Copperline Electrical', trade='Electrician<br>One page', pass_='4171',
       idea="An electrician's website that reads like a well-run job. A circuit diagram draws itself on arrival, rates are published instead of hidden, and a countdown to Queensland's 2027 smoke alarm deadline gives people a real reason to book now.",
       feats=['Self-drawing circuit diagram with flowing current', 'Six-question home safety check', 'Smoke alarm deadline countdown', 'Published rate card and fixed-price jobs', 'Owner editor with one-click publishing'],
       fig="The home safety check. Six questions anyone can answer, a straight verdict, and the specific things worth fixing."),
  dict(id='lot-3', lot='Lot 3', acc='violet', slug='hush', name='Hush Home Cleaning', trade='Home cleaning<br>Five pages', pass_='5829',
       idea="A cleaning company built around the worries people have about letting someone into their home. It opens on a fogged window being squeegeed clean, prices every clean instantly, and shows exactly what gets done in each room.",
       feats=['Fogged-window squeegee opening', 'Instant quote that carries through to booking', 'Tap-a-room cleaning checklist', 'Wipe transitions between pages', 'Owner editor that controls every price'],
       fig="The room-by-room checklist. Choose a room and a kind of clean to see exactly what's included."),
]
PAUSE = '<svg class="pause" viewBox="0 0 14 14"><rect x="2" y="1" width="3.5" height="12"/><rect x="8.5" y="1" width="3.5" height="12"/></svg><svg class="play" viewBox="0 0 14 14"><path d="M3 1l10 6-10 6z"/></svg>'
def case(c):
    feats = ''.join(f'<li><span>{f}</span></li>' for f in c['feats'])
    return f'''
<section class="case" id="{c['id']}" data-acc="{c['acc']}">
  <div class="wrap">
    <div class="case-head"><span class="lot">{c['lot']}</span><h2 class="split">{c['name']}</h2><span class="trade">{c['trade']}</span></div>
    <div class="stage"><div class="stage-in">
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
          <a class="btn" data-mag href="demos/{c['slug']}/index.html" target="_blank" rel="noopener">Open the demo {EXT}</a>
          <a class="btn ghost" data-mag href="demos/{c['slug']}/admin.html" target="_blank" rel="noopener">Try the editor {EXT}</a>
          <span class="passcode">Passcode<b>{c['pass_']}</b></span>
        </div>
      </div>
      <ul class="pegs rise" style="--d:150ms">{feats}</ul>
    </div>
    <figure class="figure"><div class="frame"><img src="assets/{c['slug']}-feature.webp" alt="{c['fig'].split('.')[0]} in the {c['name']} demo" width="1440" height="900" loading="lazy" decoding="async"></div><figcaption>{c['fig']}</figcaption></figure>
  </div>
</section>'''

def parcel(c, d, lx, accent):
    return (f'<g class="parcel" tabindex="0" role="link" data-go="{c["id"]}" style="--acc:{accent}" aria-label="{c["lot"]}, {c["name"]}">'
            f'<path pathLength="1" d="{d}"/>'
            f'<text class="lt" x="{lx}" y="92">{c["lot"].upper()}</text>'
            f'<text class="nm" x="{lx}" y="130">{c["name"]}</text>'
            f'<text class="tr" x="{lx}" y="156">{c["trade"].split("<br>")[0]}</text></g>')
lotmap = ('<div class="lotmap rise"><svg viewBox="0 0 1200 380" role="group" aria-label="Survey plan of the three demos. Choose one to jump to it.">'
  '<path class="ct" d="M0 70c200-40 380 30 600 0s420-50 600-10"/><path class="ct" d="M0 170c220-30 400 40 620 10s380-40 580-5"/>'
  '<path class="ct" d="M0 270c180-35 420 35 610 5s400-45 590-10"/><path class="ct" d="M0 350c240-30 380 25 600 0s420-30 600-5"/>'
  + parcel(CASES[0], 'M40 40 L420 30 L445 330 L60 350 Z', 80, '#FFB223')
  + parcel(CASES[1], 'M420 30 L790 50 L770 340 L445 330 Z', 470, '#E09A6C')
  + parcel(CASES[2], 'M790 50 L1160 36 L1150 350 L770 340 Z', 820, '#A38BEB')
  + '</svg></div>')
lotlist = '<ul class="lotlist">' + ''.join(f'<li><a href="#{c["id"]}"><b>{c["name"]}</b><span>{c["lot"]}</span></a></li>' for c in CASES) + '</ul>'

work = f'''
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">The work.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">Three demo websites for three trades, each built from a blank page. Every one is live: open it, click around, and try the editor the owner would use.</p>
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
      <p class="lede">Every site starts from a blank page. Tell me about your business and I'll show you what yours could look like.</p>
      <div class="actions"><a class="btn" data-mag href="pricing.html#quote">Get a quote</a><a class="btn ghost" data-mag href="pricing.html">See pricing</a></div>
    </div>
  </div>
</section>
'''

# ---------- PRICING ----------
def pegs(items): return '<ul class="pegs">' + ''.join(f'<li><span>{i}</span></li>' for i in items) + '</ul>'
FAQ = [
  ("Do I need to know anything technical?", "No. I set everything up, and the editor is plain boxes and a publish button. If you can fill in a form, you can update your website."),
  ("What's the real difference between the two plans?", "Who holds the keys, and how you pay. Freehold costs more upfront and then it's entirely yours. Looked after costs less to start, and I host it and handle the technical side for a monthly fee."),
  ("What does owning it outright actually mean?", "Once a Freehold site is paid for, it lives on accounts in your name and the site is yours. You can keep it forever, move it, or have someone else work on it. Nothing stops working if you never speak to me again."),
  ("What happens if I leave the subscription?", "Your content and your domain are yours. I'll send you an export of your content within 30 days of asking, and transfer your domain to you. The site itself stays with me unless you take the buy-out, which moves everything into your own accounts."),
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
  ("Extra pages", 'Both plans include up to <span data-price="pages">5</span> pages. More are <span data-price="extraPage">$100</span> each.'),
  ("Bigger changes", '<span data-price="hourly">$75</span> an hour, in 30-minute blocks, and always quoted before I start.'),
  ("Paying", "A deposit books you in and the balance is due before your site goes live. Invoices are due within 7 days, and subscriptions are billed monthly in advance."),
  ("Your domain", "It belongs to your business. On the subscription I can register and renew it for you, and I'll transfer it into your name whenever you ask."),
  ("Leaving the subscription early", '<span data-price="earlyExit">$40</span> for each month left in the <span data-price="managed.min">12</span>-month minimum. That repays the startup discount, nothing more.'),
  ("Taking a subscription site with you", 'Your content export is free. To keep the site itself, the buy-out is <span data-price="buyOut">$150</span> plus any early-exit amount, and I move everything into your own accounts.'),
  ("Google rankings", "Every site is built so Google can read it properly. Nobody can honestly guarantee a top spot, so I don't."),
  ("Not included", "Online shops, professional copywriting and photography, ongoing SEO campaigns and paid advertising. I'm happy to point you to someone good."),
]
fine = ''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in FINE)

pricing = f"""
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">Straight prices.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">Two ways to get a website from me. Both are built by hand, both come with an editor you can use from your phone, and both prices are here in writing, not hidden behind a phone call.</p>
  </div>
</section>
{founding_band()}
<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="plans rise">
      <article class="plan primary">
        <h2>Freehold</h2>
        <p class="tag">Own it outright</p>
        <div class="price"><b data-price="freehold.now">$900</b><span><span class="founding-only">founding price, then <span data-price="freehold.standard">$1,200</span></span><span class="standard-only" hidden>once</span></span></div>
        <p class="desc">Your website, set up on accounts in your name and fully yours once it's paid for. Nothing to pay me each month.</p>
        {pegs(['Custom design and build, up to <span data-price="pages">5</span> pages', 'Owner editor with one-click publishing', 'Enquiry or booking form straight to your inbox', 'Built so Google can read every page', 'Set up on your own accounts, in person or remotely', 'Full ownership of the site once it is paid for'])}
        <p class="terms"><span data-price="freehold.depositLine">40% ($360)</span> deposit to book, the balance before your site goes live. After that, changes are free with your editor, or <span data-price="hourly">$75</span> an hour if you'd rather I do them.</p>
        <a class="btn" data-mag data-plan-pick="Freehold" href="#quote">Get a quote for Freehold</a>
      </article>
      <article class="plan">
        <h2>Looked after</h2>
        <p class="tag">I look after it for you</p>
        <div class="price"><b data-price="managed.start">$400</b><span>to start, then <span data-price="managed.monthly">$50</span> a month</span></div>
        <p class="desc">Hosting, your domain, security and small changes are all handled. Use the editor for everyday updates, or just send me a text.</p>
        {pegs(['Custom design and build, up to <span data-price="pages">5</span> pages', 'A simple editor for everyday updates', 'Hosting, security certificate and your domain handled', 'Up to 2 change requests a month, done within 2 business days', 'Enquiry or booking form straight to your inbox', 'Set up remotely, with no accounts for you to create'])}
        <p class="terms"><span data-price="managed.depositLine">30% ($120)</span> deposit to book, the balance before go-live. Billed monthly in advance, with a <span data-price="managed.min">12</span>-month minimum, then month to month with 30 days' notice.</p>
        <a class="btn ghost" data-mag data-plan-pick="Looked after" href="#quote">Get a quote for Looked after</a>
      </article>
    </div>

    <div class="compare rise">
      <div class="crow"><span></span><span>Freehold</span><span>Looked after</span></div>
      <div class="crow"><span>Who holds the accounts</span><span>You, in your own name</span><span>Me, so you never have to</span></div>
      <div class="crow"><span>Upfront</span><span><span data-price="freehold.now">$900</span></span><span><span data-price="managed.start">$400</span></span></div>
      <div class="crow"><span>Each month</span><span>Nothing</span><span><span data-price="managed.monthly">$50</span></span></div>
      <div class="crow"><span>Changes after launch</span><span>You, with the editor</span><span>You, plus 2 requests a month from me</span></div>
      <div class="crow"><span>First-year total</span><span><span data-price="freehold.now">$900</span>, plus your domain</span><span><span data-price="managed.firstYear">$1,000</span>, domain included</span></div>
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
      <form id="quoteForm" novalidate>
        <fieldset class="fset">
          <legend>About you</legend>
          <div class="row">
            <div class="fld"><label for="fName">Your name</label><input id="fName" name="Name" type="text" autocomplete="name" placeholder="Jess Carter"></div>
            <div class="fld"><label for="fBiz">Business name</label><input id="fBiz" name="Business" type="text" autocomplete="organization" placeholder="Carter Plumbing"></div>
          </div>
          <div class="row">
            <div class="fld"><label for="fPhone">Phone</label><input id="fPhone" name="Phone" type="tel" autocomplete="tel" placeholder="0412 345 678"></div>
            <div class="fld"><label for="fEmail">Email</label><input id="fEmail" name="Email" type="email" autocomplete="email" placeholder="jess@carterplumbing.com.au"></div>
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
        <input type="hidden" name="Needs" id="fNeeds" value="">
        <input type="text" name="botcheck" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
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

# ---------- PRIVACY ----------
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
      <p class="updated">Last updated 1 October 2026</p>
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
      <p>Founding clients agree to let me show their finished website as an example of my work. I'll only ever show the public website itself, never your private details.</p>

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
        <li><strong>Website hosting.</strong> This site and subscription sites are hosted by Netlify, which keeps standard server logs such as IP addresses and browser types for security and performance. Website code and content are stored with GitHub.</li>
        <li><strong>Email.</strong> Messages to {EMAIL} are stored with my business email provider.</li>
        <li><strong>Domains.</strong> When a domain is registered, the registrant's details go to the domain registrar and the .au registry, as their rules require.</li>
        <li><strong>Payments.</strong> If you pay by card, your card details are handled by the payment provider. I never see or store full card numbers.</li>
      </ul>
      <p>I may also disclose information if the law requires it.</p>
      <p>Some of these providers store data outside Australia, including in the United States. I only use established providers with their own security and privacy commitments.</p>

      <h2>Cookies and your browser</h2>
      <p>This site doesn't use advertising cookies, tracking pixels or analytics. It saves two small things in your own browser: your choice if you turn the site's animations on or off, and any practice edits you make in the demo editors on the work page. Both stay on your device and are never sent to me.</p>

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
                     None, home, f'<script type="application/ld+json">{json.dumps(LD)}</script>\n'),
  'work.html': page('work', 'The work — Freehold', 'Three working demo websites for a mechanic, an electrician and a home cleaner, each built from scratch with an owner editor.', 'work', work),
  'pricing.html': page('pricing', 'Pricing — Freehold', 'Straight prices for a custom website: own it outright for $900 at the founding price, or have it looked after for $400 to start and $50 a month.', 'pricing', pricing),
  'privacy.html': page('privacy', 'Privacy — Freehold', 'How Freehold collects, uses and protects your personal information.', None, privacy),
  '404.html': page('notfound', 'Page not found — Freehold', 'This page could not be found.', None, notfound, '<meta name="robots" content="noindex">\n', P='/'),
}
for fn, html in PAGES.items():
    open(fn, 'w').write(html)
    print(fn, len(html), 'bytes')
