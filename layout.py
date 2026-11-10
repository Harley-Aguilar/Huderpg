"""Editorial HTML composition for the bilingual portfolio."""
from pathlib import Path
from html import escape as e
import json
from content import D
from editorial import COPY
from demo import sheet

ROOT=Path(__file__).parent
BASE='https://harley-aguilar.github.io/Huderpg/'
IG='https://www.instagram.com/_huderpg_/'
VERSION='dark-purple-1'

def arrow(direction='up'):
    path='M5 19 19 5M5 5h14v14' if direction=='up' else 'M5 12h14m-6-6 6 6-6 6'
    return f'<svg class="icon-arrow" aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="{path}" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def die(cls=''):
    return f'<svg class="die {cls}" aria-hidden="true" width="240" height="260" viewBox="0 0 240 260" fill="none"><path d="M120 9 222 68v121l-102 62L18 189V68L120 9Z"/><path d="m120 9 54 86 48-27M18 68l48 27 54-86M18 189l48-94h108l48 94M18 189l102-20 102 20M66 95l54 74 54-74M120 169v82"/><circle cx="120" cy="169" r="3" fill="currentColor" stroke="none"/></svg>'

def logo(home='index.html'):
    return f'<a class="wordmark" href="{home}" aria-label="Hude — Home">hude<span class="logo-dot">.</span>{die()}</a>'

def btn(text,url,outline=False):
    ext=' target="_blank" rel="noopener noreferrer"' if url.startswith('https://') else ''
    return f'<a class="button{" outline" if outline else ""}" href="{url}"{ext}><span>{e(text)}</span>{arrow()}</a>'

def languages(key,case=False):
    urls=(['../../projects/utopia.html','../../pt/projects/utopia.html'] if key=='pt' else ['utopia.html','../pt/projects/utopia.html']) if case else (['../index.html','index.html'] if key=='pt' else ['index.html','pt/index.html'])
    return '<nav class="languages" aria-label="Language / Idioma">'+''.join(f'<a href="{u}" lang="{k}" hreflang="{k}"'+(' aria-current="page"' if k==key else '')+f'>{k.upper()}</a>' for k,u in zip(['en','pt'],urls))+'</nav>'

def header(key,case=False):
    d=D[key];c=COPY[key];home='../index.html' if case else 'index.html'
    nav=''.join(f'<a href="{home if case else ""}#{s}"><span class="nav-index">0{i}</span>{t}</a>' for i,(s,t) in enumerate(zip(['work','services'],d['nav'][:2]),1))
    return f'''<header class="site-header" id="top"><div class="nav wrap">{logo(home)}<div class="brand-descriptor mono">RPG DESIGN<br>& CREATIVE TOOLS</div><nav class="nav-links" id="nav-links" aria-label="{'Navegação principal' if key=='pt' else 'Main navigation'}">{nav}</nav>{languages(key,case)}<a class="nav-contact" href="{IG}" target="_blank" rel="noopener noreferrer">{c['start']}{arrow()}</a><button class="menu-toggle" type="button" aria-label="{d['menu']}" aria-controls="nav-links" aria-expanded="false"><span></span><span></span></button></div></header>'''

def head(key,prefix='',case=False):
    d=D[key]
    route=('pt/' if key=='pt' else '')+('projects/utopia.html' if case else '')
    alt=BASE+('projects/utopia.html' if case else '')
    altpt=BASE+'pt/'+('projects/utopia.html' if case else '')
    title=('UTOPIA — '+d['title']) if case else d['title']
    schema={'@context':'https://schema.org','@type':'Person','name':'Harley Aguilar','alternateName':'Hude','url':BASE+('pt/' if key=='pt' else ''),'sameAs':['https://www.youtube.com/@Hudezin',IG,'https://www.tiktok.com/@hudeplay']}
    return f'''<!doctype html><html lang="{d['lang']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#141116"><meta name="color-scheme" content="dark"><title>{e(title)}</title><meta name="description" content="{e(d['description'])}">
<link rel="canonical" href="{BASE+route}"><link rel="alternate" hreflang="en" href="{alt}"><link rel="alternate" hreflang="pt-BR" href="{altpt}"><link rel="alternate" hreflang="x-default" href="{alt}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(d['description'])}"><meta property="og:url" content="{BASE+route}">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/style.css?v={VERSION}"><script src="{prefix}assets/app.js?v={VERSION}" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">{d['skip']}</a>'''

def project_art(key,prefix=''):
    d=D[key];c=COPY[key]
    attrs=''.join(f'<div><span>{x}</span><b>0{v}</b></div>' for x,v in zip(d['attrs'],[2,3,2]))
    bars=''.join(f'<div class="art-resource"><div><span>{x}</span><b>{v} / {m}</b></div><i style="--fill:{v/m*100:.1f}%"></i></div>' for x,v,m in zip(d['resources'],[18,12,8],[24,16,12]))
    return f'''<div class="art-background" aria-hidden="true"><div class="art-grid"></div><span class="art-word">UTOPIA</span>{die('art-die')}<div class="art-orbit orbit-one"></div><div class="art-orbit orbit-two"></div></div>
<div class="stage-top mono"><span>UTOPIA — 01</span><span>{c['personal'].upper()} / 2026</span></div>
<div class="art-composition" aria-hidden="true"><div class="implant-card"><div class="implant-header mono"><span>{d['tabs'][2]}</span><span>12 SLOTS</span></div><img class="implant-body" src="{prefix}assets/body.svg" width="192" height="300" alt="" loading="lazy"><span class="map-point point-a"></span><span class="map-point point-b"></span><span class="map-point point-c"></span><div class="map-scale"><span>NEURAL</span><i></i><span>35%</span></div><div class="implant-bottom mono">BODY MAPPING / U.03</div></div>
<div class="dossier"><div class="dossier-top"><strong>UTOPIA</strong><span class="mono">{d['hub']}<br>INTERFACE / V.03</span></div><div class="dossier-rule"></div><div class="dossier-identity"><span class="mono">{d['char']}</span><h3>{d['identity']}</h3><span class="identity-cross">+</span></div><div class="dossier-content"><div class="dossier-main"><div class="art-attributes mono">{attrs}</div><div class="art-resources mono">{bars}</div><div class="art-tabs mono"><span>{d['tabs'][0]}</span><span>{d['tabs'][1]}</span><span>{d['tabs'][2]}</span></div><div class="art-skill"><span class="mono">{d['skills']}</span><div><span>{d['skillList'][0]}</span><b>02</b></div><div><span>{d['skillList'][1]}</span><b>03</b></div></div></div><div class="dossier-side"><span class="mono">NEURAL LINK</span><div class="side-crosshair"></div><img src="{prefix}assets/body.svg" width="140" height="240" alt="" loading="lazy"><span class="mono">HUMAN / 001</span></div></div><div class="dossier-bottom mono"><span>UTOPIA — {d['country']}</span><span>CHARACTER / SYSTEM</span></div></div></div>
<div class="stage-bottom mono"><span>{c['projectType']}</span><span class="stage-open">{c['viewCase']}{arrow()}</span></div>'''

def footer(key,home='index.html'):
    d=D[key];c=COPY[key]
    return f'<div class="footer-bottom wrap"><span class="mono">© 2026 HUDE · {d["country"]}</span><span>{c["footer"]}</span><a href="#top">{c["backTop"]}{arrow()}</a></div><div class="footer-word wrap" aria-hidden="true">hude<span>.</span></div></footer></body></html>'

def contact(key,case=False):
    c=COPY[key]
    return f'<footer class="site-footer" id="contact"><div class="contact wrap"><div><p class="eyebrow">{c["contactLabel"]}</p><h2>{c["caseEnd" if case else "contactTitle"]}</h2></div><div class="contact-action"><p>{c["contactBody"]}</p><a class="contact-circle" href="{IG}" target="_blank" rel="noopener noreferrer"><span>{c["start"]}</span>{arrow()}</a></div></div>'

def home(key):
    d=D[key];c=COPY[key];pre='../' if key=='pt' else ''
    tags=''.join(f'<span>{t}</span>' for t in c['tags'])
    rows=''.join(f'<details class="service-row"'+(' open' if i==1 else '')+f'><summary><span class="service-num mono">0{i}</span><span class="service-name">{title}<small class="mono">{tag}</small></span><span class="service-plus" aria-hidden="true"></span></summary><div class="service-body"><p>{desc}</p><a href="{IG}" target="_blank" rel="noopener noreferrer">{c["start"]}{arrow()}</a></div></details>' for i,(title,tag,desc) in enumerate(c['serviceRows'],1))
    socials=''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer"><span>{name}<small>{handle}</small></span>{arrow()}</a>' for name,handle,url in [('YouTube','@Hudezin','https://www.youtube.com/@Hudezin'),('Instagram','@_huderpg_',IG),('TikTok','@hudeplay','https://www.tiktok.com/@hudeplay')])
    return head(key,pre)+header(key)+f'''<main id="main">
<section class="hero wrap"><div class="hero-top mono"><span>{c['role']}</span><span class="availability"><i></i>{c['availability']}</span></div><div class="hero-grid"><h1>{c['hero']}</h1><div class="hero-intro"><p>{c['intro']}</p><a class="text-link" href="#work">{c['work']}{arrow('right')}</a><span class="hero-location mono">HARLEY AGUILAR / {d['country']}</span></div></div></section>
<section class="selected-work wrap" id="work" aria-label="{d['nav'][0]}"><div class="work-heading mono"><span>{c['portfolio']}</span><span>{"ROLE PARA EXPLORAR" if key=="pt" else "SCROLL TO EXPLORE"}</span></div><a class="project-stage" href="projects/utopia.html" aria-label="{c['stage']}">{project_art(key,pre)}</a><article class="project-caption"><div><p class="eyebrow">01 / UTOPIA</p><h2>{c['caseTitle']}</h2></div><div class="project-copy"><p>{c['caseDescription']}</p><div class="project-tags mono">{tags}</div><a class="text-link" href="projects/utopia.html">{c['viewCase']}{arrow()}</a><span class="project-disclosure mono">{c['designStudy']}</span></div></article></section>
<div class="manifesto wrap"><span class="manifesto-mark" aria-hidden="true">{die()}</span><p>{c['studioLine']}</p><span class="mono">{c['studioNote'].replace(chr(10),'<br>')}</span></div>
<section class="services wrap" id="services"><div class="section-intro"><p class="eyebrow">{c['servicesLabel']}</p><h2>{c['services']}</h2><p>{d['intro']}</p></div><div class="service-list">{rows}</div></section>
<section class="about wrap" id="about"><div class="creator-art" aria-hidden="true"><span class="mono">INDEPENDENT BY DESIGN.</span>{die('creator-die')}<div class="creator-signature">hude.</div><span class="creator-index mono">RPG / DESIGN / PLAY</span></div><div class="about-content"><p class="eyebrow">{c['aboutLabel']}</p><h2>{c['aboutTitle']}</h2><p>{c['bio']}</p><p class="about-secondary">{c['bio2']}</p><nav class="socials" aria-label="Social"><span class="eyebrow">{c['follow']}</span>{socials}</nav></div></section>
</main>'''+contact(key)+footer(key)

def case(key):
    d=D[key];c=COPY[key];pre='../../' if key=='pt' else '../'
    meta=''.join(f'<div><dt class="mono">{label}</dt><dd>{value}</dd></div>' for label,value in c['caseMeta'])
    choices=''.join(f'<article><span class="mono">0{i}</span><h3>{title}</h3><p>{desc}</p></article>' for i,(title,desc) in enumerate(c['caseChoices'],1))
    return head(key,pre,True)+header(key,True)+f'''<main id="main"><section class="case-hero wrap"><a class="case-back text-link" href="../index.html#work">{arrow('right')}{d['back']}</a><div class="case-hero-top"><h1>UTOPIA<span> / 01</span></h1><span class="mono">{c['projectType']}<br>2026 / {c['personal'].upper()}</span></div><div class="case-heading"><h2>{c['caseHero']}</h2><p>{c['caseHeroBody']}</p></div><dl class="case-meta">{meta}</dl></section><section class="case-showcase wrap" aria-label="UTOPIA"><div class="project-stage case-stage">{project_art(key,pre)}</div><p class="case-image-caption mono">{c['designStudy']}</p></section><section class="case-overview wrap"><p class="eyebrow">{c['caseOverview']}</p><div><h2>{c['caseHeading']}</h2><p>{c['caseOverviewBody']}</p></div></section><section class="case-choices wrap"><p class="eyebrow">{c['detailsLabel']}</p><div class="choice-grid">{choices}</div></section><section class="interactive-section" id="demo"><div class="wrap"><div class="interactive-heading"><div><p class="eyebrow">{c['demoLabel']}</p><h2>{c['demoTitle']}</h2></div><p>{d['demoHelp']}</p></div><div class="demo" data-demo>{sheet(d,True,True)}</div><details class="scope"><summary>{c['scopeTitle']}<span class="service-plus" aria-hidden="true"></span></summary><p>{c['scope']}</p></details></div></section></main>'''+contact(key,True)+footer(key,'../index.html')

def build():
    for key in D:
        folder=ROOT/('pt' if key=='pt' else '')
        (folder/'projects').mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(home(key),encoding='utf-8')
        (folder/'projects/utopia.html').write_text(case(key),encoding='utf-8')
    (ROOT/'404.html').write_text(head('en','/Huderpg/')+'<header id="top" class="site-header"><div class="nav wrap">'+logo('/Huderpg/')+'</div></header><main id="main" class="not-found wrap"><p class="eyebrow">404 / WRONG TURN</p><h1>A different<br><em>kind of adventure.</em></h1><p>This page could not be found. Let’s get you back to the portfolio.</p>'+btn('Back to the portfolio','/Huderpg/')+'</main>'+contact('en')+footer('en','/Huderpg/'),encoding='utf-8')
    urls=['','pt/','projects/utopia.html','pt/projects/utopia.html']
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in urls)+'</urlset>',encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /Huderpg/\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    print('Built 5 static pages: editorial home and UTOPIA case in English and Portuguese, plus 404.')
