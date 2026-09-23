import json
FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%230C110E'/%3E"
       "%3Crect x='8' y='8' width='16' height='16' fill='none' stroke='%23ECEFE7' stroke-width='2'/%3E%3Ccircle cx='8' cy='8' r='3.2' fill='%23FF6533'/%3E"
       "%3Ccircle cx='24' cy='8' r='3.2' fill='%23ECEFE7'/%3E%3Ccircle cx='24' cy='24' r='3.2' fill='%23ECEFE7'/%3E%3Ccircle cx='8' cy='24' r='3.2' fill='%23ECEFE7'/%3E%3C/svg%3E")
MARK = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect class="bx" x="4" y="4" width="16" height="16"/>'
        '<circle class="pk hot" cx="4" cy="4" r="2.4"/><circle class="pk" cx="20" cy="4" r="2.4"/>'
        '<circle class="pk" cx="20" cy="20" r="2.4"/><circle class="pk" cx="4" cy="20" r="2.4"/></svg>')
EXT = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'
PHONE, PHONE_LINK, EMAIL = '0444 554 898', '+61444554898', 'Connor.ransome@gmail.com'

def letters(word, cls=''):
    return ''.join(f'<span style="--i:{i}">{c}</span>' for i, c in enumerate(word))

def head(title, desc, extra=''):
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0C110E">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="/assets/og.jpg">
<link rel="icon" href="{FAV}">
<link rel="preload" href="assets/fonts/anybody.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/hanken.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script>(function(){{var d=document.documentElement;d.classList.add('js');try{{if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&!sessionStorage.getItem('fh-intro')){{d.classList.add('intro');sessionStorage.setItem('fh-intro','1');}}}}catch(e){{}}}})();</script>
{extra}</head>'''

def nav(active):
    items = [('work', 'work.html', 'Work'), ('pricing', 'pricing.html', 'Pricing'), ('about', 'index.html#about', 'About')]
    links = ''.join(f'<a href="{u}"{" aria-current=\"page\"" if k == active else ""}>{l}</a>' for k, u, l in items)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="gridlines" aria-hidden="true"><i></i></div>
<div class="veil" id="veil" aria-hidden="true"><div class="intro-box"><span class="ln t"></span><span class="ln r"></span><span class="ln b"></span><span class="ln l"></span><i class="pg"></i><i class="pg"></i><i class="pg"></i><i class="pg"></i><div class="intro-word">{letters("FREEHOLD")}</div><p class="intro-cap">Bokarina, Sunshine Coast</p></div></div>
<header class="nav" id="nav">
  <a class="brand" href="index.html" aria-label="Freehold, home">{MARK}<b>FREEHOLD</b></a>
  <nav class="links" aria-label="Main">{links}</nav>
  <a class="btn sm navcta" href="pricing.html#quote">Get a quote</a>
  <button class="burger" type="button" aria-label="Open menu" aria-expanded="false"><span></span></button>
</header>'''

FOOT = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><a class="brand" href="index.html" aria-label="Freehold, home">{MARK}<b>FREEHOLD</b></a>
        <p style="margin-top:1.2rem">Custom websites for trades and local businesses, built by hand in Bokarina on the Sunshine Coast.</p></div>
      <div><h4>Contact</h4><ul><li><a href="tel:{PHONE_LINK}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Bokarina QLD 4575</li></ul></div>
      <div><h4>Pages</h4><ul><li><a href="index.html">Home</a></li><li><a href="work.html">Work</a></li><li><a href="pricing.html">Pricing</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
      <div><h4>In Bokarina it's</h4><div class="clock" id="clock">&nbsp;</div><p id="clockNote" style="margin-top:.6rem"></p></div>
    </div>
    <div class="legal"><span>&copy; <span id="year">2026</span> Freehold</span><span id="abnLine" hidden></span><a href="privacy.html">Privacy policy</a><span>This site was built the same way yours would be.</span></div>
  </div>
</footer>'''

def page(name, title, desc, active, body, extra_head=''):
    return f'''{head(title, desc, extra_head)}
<body data-page="{name}">
{nav(active)}
<main id="main">
{body.strip()}
</main>
{FOOT}
<script src="main.js"></script>
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
  ("Set up in person.",
   "I come to your business, set everything up on your own devices and show you how it all works. No emailed instructions, no screen-sharing, no guessing.", V_ROUTE),
]
feat_items = ''.join(f'<article class="feat"><h3>{h}</h3><p>{p}</p><div class="fv-inline">{v}</div></article>' for h, p, v in FEATS)
feat_stage = ''.join(f'<div class="fv">{v}</div>' for _, _, v in FEATS)

STEPS = [
  ("A chat", "Twenty minutes at your place or on the phone. You tell me about the business, and I'll tell you honestly whether a new website would help. It's free."),
  ("A plan and a price", "A fixed price in writing and a clear list of what's included. When you're ready to go ahead, a deposit books you in."),
  ("The build", "Usually two to three weeks. You get a private link to watch it come together and ask for changes along the way."),
  ("Handover", "I set it up at your business, walk you through the editor, and fix anything that comes up in the first month."),
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
      "telephone": PHONE_LINK, "email": EMAIL, "founder": "Connor Ransome",
      "address": {"@type": "PostalAddress", "addressLocality": "Bokarina", "addressRegion": "QLD", "postalCode": "4575", "addressCountry": "AU"},
      "areaServed": ["Sunshine Coast", "Brisbane"]}

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
  ("What does owning it outright actually mean?", "With the Freehold plan your website lives on accounts in your name, set up at handover. You can keep it forever, move it, or have someone else work on it. Nothing stops working if you never speak to me again."),
  ("I already have a website. Can you replace it?", "Yes. Your domain and your email stay exactly as they are, and the new site switches over on a day that suits you."),
  ("How long does it take?", "Usually two to three weeks from the deposit to handover, depending on how quickly we can pull together your details, photos and prices."),
  ("Do you work outside the Sunshine Coast?", "In person, anywhere between Noosa and Brisbane. Further away, I can build it and set everything up remotely."),
  ("Can you write the words for my site?", "Yes, it's included. I'll ask you about the business, write it in plain English, and you approve every word before it goes live."),
]
faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

def chips(name, options, kind='radio', checked=None, group_id=None):
    gid = f' id="{group_id}"' if group_id else ''
    inner = ''.join(f'<label class="chip"><input type="{kind}"{f" name={json.dumps(name)}" if name else ""} value="{o}"{" checked" if o == checked else ""}><span>{o}</span></label>' for o in options)
    return f'<div class="chips"{gid}>{inner}</div>'

pricing = f'''
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">Straight prices.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">Two ways to get a website from me. Both are built by hand, both come with an editor, and both prices are here in writing, not hidden behind a phone call.</p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="plans rise">
      <article class="plan primary">
        <h2>Freehold</h2>
        <p class="tag">Own it outright</p>
        <div class="price"><b data-price="freehold.base">$1,800</b><span>once, starting from</span></div>
        <p class="desc">Your website, set up on accounts in your name and yours to keep. Nothing to pay me each month.</p>
        {pegs(['Custom design and build, up to <span data-price="pages">5</span> pages', 'Owner editor with one-click publishing', 'Enquiry or booking form straight to your inbox', 'Set up in person, on your own accounts', 'Your domain connected, which you keep paying for yourself', 'A month of fixes after handover'])}
        <p class="terms"><span data-price="freehold.deposit">40%</span> deposit to book, the rest at handover. After the first month, changes are <span data-price="hourly">$60</span> an hour if you'd rather not do them yourself.</p>
        <a class="btn" data-mag data-plan-pick="Freehold" href="#quote">Get a quote for Freehold</a>
      </article>
      <article class="plan">
        <h2>Looked after</h2>
        <p class="tag">I look after it for you</p>
        <div class="price"><b data-price="managed.base">$499</b><span>to start, then <span data-price="managed.monthly">$69</span> a month</span></div>
        <p class="desc">Hosting, your domain and small changes are all handled. Use the editor for everyday updates, or just send me a text.</p>
        {pegs(['Custom design and build, up to <span data-price="pages">5</span> pages', 'A simple editor for the things you change often', 'Hosting and domain included', 'Up to an hour of changes from me every month', 'Enquiry or booking form straight to your inbox', 'Optional AI assistant on your site for <span data-price="ai">$29</span> a month'])}
        <p class="terms"><span data-price="managed.min">3</span> month minimum, then month to month. Cancel with 30 days' notice.</p>
        <a class="btn ghost" data-mag data-plan-pick="Looked after" href="#quote">Get a quote for Looked after</a>
      </article>
    </div>

    <div class="compare rise">
      <div class="crow"><span></span><span>Freehold</span><span>Looked after</span></div>
      <div class="crow"><span>Who owns it</span><span>You, on your own accounts</span><span>Hosted by me, for you</span></div>
      <div class="crow"><span>Each month</span><span>Nothing</span><span><span data-price="managed.monthly">$69</span></span></div>
      <div class="crow"><span>Changes</span><span>You, with the editor</span><span>You, plus an hour from me</span></div>
      <div class="crow"><span>Over two years</span><span>From <span data-price="freehold.base">$1,800</span></span><span>From <span data-price="managed.twoYears">$2,155</span></span></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0" id="estimate">
  <div class="wrap">
    <h2 class="split">Work out your price.</h2>
    <div class="estimator">
      <div class="ectl rise">
        <div class="erow"><div class="lbl"><b>Plan</b><span>Own it, or have it looked after</span></div>
          <div class="seg" id="planSeg" role="group" aria-label="Plan"><span class="thumb" aria-hidden="true"></span><button type="button" data-plan="freehold" aria-pressed="true">Freehold</button><button type="button" data-plan="managed" aria-pressed="false">Looked after</button></div></div>
        <div class="erow"><div class="lbl"><b>Pages</b><span id="pagesNote"></span></div>
          <div class="stepper"><button type="button" id="pagesDec" aria-label="Fewer pages">&minus;</button><output id="pagesOut" aria-live="polite">5</output><button type="button" id="pagesInc" aria-label="More pages">+</button></div></div>
        <div class="erow"><div class="lbl"><b>A price or quote calculator</b><span>Like the ones in the demos, <span data-price="tool">$350</span></span></div>
          <button class="switch" id="toolSw" type="button" role="switch" aria-checked="false" aria-label="Add a price or quote calculator"></button></div>
        <div class="erow"><div class="lbl"><b>AI assistant</b><span id="aiNote"></span></div>
          <button class="switch" id="aiSw" type="button" role="switch" aria-checked="false" aria-label="Add the AI assistant"></button></div>
      </div>
      <aside class="eout rise" style="--d:150ms" aria-live="polite">
        <h3>Your estimate</h3>
        <div class="eline big"><span>Upfront</span><b id="eUp">$0</b></div>
        <div class="eline"><span>Each month</span><b id="eMonth">Nothing</b></div>
        <div class="eline"><span id="eThirdLabel">Deposit to book</span><b id="eThird">$0</b></div>
        <div class="eline"><span>Over two years</span><b id="eTwo">$0</b></div>
        <p class="enote" id="eNote"></p>
        <button class="btn" type="button" id="useEstimate" data-mag>Add this to my quote request</button>
      </aside>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0" id="quote">
  <div class="wrap">
    <h2 class="split">Get a quote.</h2>
    <p class="lede rise" style="margin-top:1.2rem">Tell me about your business. I'll come back with a fixed price, usually within a day.</p>
    <div class="sheet rise">
      <form id="quoteForm" novalidate>
        <div class="estimate-tag" id="estimateTag"><span id="estimateText"></span><button type="button" id="clearEstimate">Remove</button></div>
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
          <div class="fld"><span class="label">What would help</span>{chips('', ['A new website', 'Replace my current site', 'Online bookings', 'A price or quote calculator', 'An AI assistant'], kind='checkbox', group_id='needs')}</div>
          <div class="fld"><span class="label">When</span>{chips('When', ['As soon as possible', 'In the next month or two', 'Just looking for now'], checked='In the next month or two')}</div>
        </fieldset>
        <fieldset class="fset">
          <legend>Anything else</legend>
          <div class="fld"><label for="fMsg">Tell me about the business</label><textarea id="fMsg" name="Message" placeholder="Two vans, mostly Buderim and Mooloolaba. The current site is ten years old and I can't change anything on it."></textarea></div>
        </fieldset>
        <input type="hidden" name="Estimate" id="fEstimate" value="">
        <input type="hidden" name="Needs" id="fNeeds" value="">
        <input type="text" name="botcheck" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
        <button class="btn" type="submit" id="sendBtn" data-mag>Send it through</button>
        <p class="ferr" id="ferr" role="alert"></p>
        <p class="fnote">By sending this you agree to how your details are handled in the <a href="privacy.html">privacy policy</a>. I'll only use them to reply to you.</p>
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
'''

# ---------- PRIVACY ----------
privacy = f'''
<section class="phero">
  <div class="wrap">
    <h1 class="split hero-split">Privacy.</h1>
    <p class="lede rise hero-rise" style="--d:300ms">What happens to your details when you contact Freehold, in plain English.</p>
  </div>
</section>
<section class="sec" style="padding-top:0">
  <div class="wrap">
    <article class="doc rise">
      <p class="updated">Last updated 23 September 2026</p>
      <p>Freehold is a web design business run by Connor Ransome from Bokarina, Queensland. This policy explains what personal information I collect through this website, why, and what I do with it. I aim to handle it in line with the Australian Privacy Principles.</p>

      <h2>What I collect</h2>
      <p>I only collect what you choose to send me. If you use the quote form, email me or call, that can include:</p>
      <ul>
        <li>your name, and the name of your business</li>
        <li>your phone number and email address</li>
        <li>your suburb and your current website address</li>
        <li>anything you write in your message, and any price estimate you attach</li>
      </ul>
      <p>You don't need an account to use this site, and I don't ask for payment details through it.</p>

      <h2>Why I collect it</h2>
      <p>To reply to you, prepare a quote, and if you go ahead, to build your website, invoice you and support you afterwards. I won't add you to a mailing list or use your details for marketing unless you ask me to.</p>

      <h2>Who else sees it</h2>
      <p>I don't sell or rent your information. A small number of services are involved in running this site and handling enquiries:</p>
      <ul>
        <li><strong>Website hosting.</strong> This site is hosted by Netlify, which keeps standard server logs such as IP addresses and browser types for security and performance.</li>
        <li><strong>Form delivery.</strong> Quote requests may be delivered to my inbox through a form-delivery service, or through your own email app.</li>
        <li><strong>Email.</strong> My email is provided by Google.</li>
      </ul>
      <p>Some of these providers store data outside Australia, including in the United States. I only use established providers with their own security and privacy commitments.</p>

      <h2>Cookies and tracking</h2>
      <p>This site doesn't use advertising cookies, tracking pixels or analytics. The demo editors on the work page save your practice edits in your own browser's local storage. That information stays on your device and is never sent to me.</p>

      <h2>How long I keep it</h2>
      <p>Enquiries that don't go ahead are deleted within 12 months. For clients, I keep records for as long as needed to provide the service and meet tax and legal obligations.</p>

      <h2>Seeing or correcting your information</h2>
      <p>You can ask what information I hold about you, ask me to correct it, or ask me to delete it. Get in touch using the details below and I'll respond within 30 days.</p>

      <h2>Concerns or complaints</h2>
      <p>If you're unhappy with how I've handled your information, please contact me first so I can put it right. If you're still not satisfied, you can contact the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener">oaic.gov.au</a>.</p>

      <h2>Contact</h2>
      <p>Connor Ransome, Freehold<br>Bokarina QLD 4575<br><a href="tel:{PHONE_LINK}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>

      <h2>Changes to this policy</h2>
      <p>If this policy changes, the updated version will be posted on this page with a new date at the top.</p>
    </article>
  </div>
</section>
'''

PAGES = {
  'index.html': page('home', 'Freehold — Custom websites for Sunshine Coast businesses',
                     'Custom websites for trades and local businesses on the Sunshine Coast and in Brisbane. Built by hand, with an editor you can use from your phone, and yours to own outright.',
                     None, home, f'<script type="application/ld+json">{json.dumps(LD)}</script>\n'),
  'work.html': page('work', 'The work — Freehold', 'Three working demo websites for a mechanic, an electrician and a home cleaner, each built from scratch with an owner editor.', 'work', work),
  'pricing.html': page('pricing', 'Pricing — Freehold', 'Straight prices for a custom website: own it outright from $1,800, or have it looked after from $499 plus $69 a month.', 'pricing', pricing),
  'privacy.html': page('privacy', 'Privacy — Freehold', 'How Freehold handles your personal information.', None, privacy),
}
for fn, html in PAGES.items():
    open(fn, 'w').write(html)
    print(fn, len(html), 'bytes')
