"""Editorial HTML composition for the bilingual portfolio."""
from pathlib import Path
from html import escape as e
import json
from content import D
from editorial import COPY
from seo import metadata, write_discovery_files

ROOT=Path(__file__).parent
BASE='https://harley-aguilar.github.io/Huderpg/'
IG='https://www.instagram.com/_huderpg_/'
VERSION='official-1'

def arrow(direction='up'):
    path='M5 19 19 5M5 5h14v14' if direction=='up' else 'M5 12h14m-6-6 6 6-6 6'
    return f'<svg class="icon-arrow" aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="{path}" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def die(cls=''):
    return f'<svg class="die {cls}" aria-hidden="true" width="240" height="260" viewBox="0 0 240 260" fill="none"><path d="M120 9 222 68v121l-102 62L18 189V68L120 9Z"/><path d="m120 9 54 86 48-27M18 68l48 27 54-86M18 189l48-94h108l48 94M18 189l102-20 102 20M66 95l54 74 54-74M120 169v82"/><circle cx="120" cy="169" r="3" fill="currentColor" stroke="none"/></svg>'

def social_icon(name):
    icons = {
        'Email': '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 6 9 7 9-7"/>',
        'YouTube': '<rect x="2" y="5" width="20" height="14" rx="4"/><path d="m10 9 5 3-5 3Z" fill="currentColor" stroke="none"/>',
        'Instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
        'Discord': '<path d="M8 4.5 5.5 5.3C3.5 8.3 2.5 12 3 16.5L7 19l1.3-2M16 4.5l2.5.8c2 3 3 6.7 2.5 11.2L17 19l-1.3-2M8 6.5a16 16 0 0 1 8 0M7 15.5a12 12 0 0 0 10 0"/><circle cx="8.5" cy="11.5" r="1.3"/><circle cx="15.5" cy="11.5" r="1.3"/>',
        'TikTok': '<path d="M14 3h3c.3 2.4 1.7 4 4 4.5v3a9.7 9.7 0 0 1-4-1.6V16a6 6 0 1 1-7-5.9v3.1a3 3 0 1 0 4 2.8Z"/>'
    }
    return '<svg class="social-icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+icons[name]+'</svg>'

def logo(home='./',key='en',prefix=''):
    return f'<div class="brand-lockup"><button class="brand-character" type="button" data-character-toggle aria-label="{'Pausar animação' if key=='pt' else 'Pause animation'}" data-play-label="{'Reproduzir animação' if key=='pt' else 'Play animation'}" data-pause-label="{'Pausar animação' if key=='pt' else 'Pause animation'}"><span class="character-cutout"><video data-character-video muted playsinline loop preload="metadata" poster="{prefix}assets/character/poster.jpg" width="320" height="310" aria-hidden="true"><source src="{prefix}assets/character/paper.mp4" type="video/mp4"></video></span><svg class="character-status" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6v12m6-12v12"/></svg></button><a class="wordmark" href="{home}" aria-label="{'Hude — Início' if key=='pt' else 'Hude — Home'}">hude<span class="logo-dot">.</span></a></div>'

def btn(text,url,outline=False):
    ext=' target="_blank" rel="noopener noreferrer"' if url.startswith('https://') else ''
    return f'<a class="button{" outline" if outline else ""}" href="{url}"{ext}><span>{e(text)}</span>{arrow()}</a>'

def languages(key,case=False):
    urls=(['../../projects/utopia.html','utopia.html'] if key=='pt' else ['utopia.html','../pt/projects/utopia.html']) if case else (['../','./'] if key=='pt' else ['./','pt/'])
    return '<nav class="languages" aria-label="'+('Idioma' if key=='pt' else 'Language')+'">'+''.join(f'<a href="{u}" lang="{D[k]["lang"]}" hreflang="{D[k]["lang"]}"'+(' aria-current="page"' if k==key else '')+f'>{k.upper()}</a>' for k,u in zip(['en','pt'],urls))+'</nav>'

def header(key,case=False):
    d=D[key];c=COPY[key];home='../' if case else './'
    return f'''<header class="site-header" id="top"><div class="nav wrap">{logo(home,key,'../../' if case and key=='pt' else '../' if case or key=='pt' else '')}{languages(key,case)}<a class="nav-contact" href="mailto:huderpg@gmail.com" data-open-contact aria-haspopup="dialog" aria-controls="contact-dialog"><span>{c['start']}</span>{arrow()}</a></div></header>'''

def head(key,prefix='',case=False,not_found=False):
    d=D[key]
    seo_html,schema_hash=metadata(key,case,not_found)
    script_policy="'self'"+(" 'sha256-"+schema_hash+"'" if schema_hash else '')
    policy="default-src 'none'; script-src "+script_policy+"; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'self'; media-src 'self'"
    return f'''<!doctype html><html lang="{d['lang']}" prefix="og: https://ogp.me/ns#"><head>
<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{policy}"><meta name="referrer" content="no-referrer"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#141116"><meta name="color-scheme" content="dark">
{seo_html}
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
<link rel="preload" href="{prefix}assets/fonts/squartiqa-4f.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="{prefix}assets/fonts/chakra-petch-500.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{prefix}assets/style.css?v={VERSION}"><script src="{prefix}assets/app.js?v={VERSION}" defer></script></head><body><a class="skip" href="#main">{d['skip']}</a>'''

def project_art(key,prefix=''):
    d=D[key];c=COPY[key]
    attrs=''.join(f'<div><span>{x}</span><b>0{v}</b></div>' for x,v in zip(d['attrs'],[2,3,2]))
    bars=''.join(f'<div class="art-resource"><div><span>{x}</span><b>{v} / {m}</b></div><i></i></div>' for x,v,m in zip(d['resources'],[18,12,8],[24,16,12]))
    return f'''<div class="art-background" aria-hidden="true"><div class="art-grid"></div><span class="art-word">{'FICHAS WEB' if key=='pt' else 'WEB SHEETS'}</span>{die('art-die')}<div class="art-orbit orbit-one"></div><div class="art-orbit orbit-two"></div></div>
<div class="art-composition" aria-hidden="true"><div class="implant-card"><div class="implant-header mono"><span>{d['tabs'][2]}</span><span>12 SLOTS</span></div><img class="implant-body" src="{prefix}assets/body.svg" width="192" height="300" alt="" loading="lazy"><span class="map-point point-a"></span><span class="map-point point-b"></span><span class="map-point point-c"></span><div class="map-scale"><span>NEURAL</span><i></i><span>35%</span></div><div class="implant-bottom mono">BODY MAPPING / U.03</div></div>
<div class="dossier"><div class="dossier-top"><strong>{'FICHAS WEB' if key=='pt' else 'WEB SHEETS'}</strong><span class="mono">{d['hub']}<br>INTERFACE / V.03</span></div><div class="dossier-rule"></div><div class="dossier-identity"><span class="mono">{d['char']}</span><h3>{d['identity']}</h3><span class="identity-cross">+</span></div><div class="dossier-content"><div class="dossier-main"><div class="art-attributes mono">{attrs}</div><div class="art-resources mono">{bars}</div><div class="art-tabs mono"><span>{d['tabs'][0]}</span><span>{d['tabs'][1]}</span><span>{d['tabs'][2]}</span></div><div class="art-skill"><span class="mono">{d['skills']}</span><div><span>{d['skillList'][0]}</span><b>02</b></div><div><span>{d['skillList'][1]}</span><b>03</b></div></div></div><div class="dossier-side"><span class="mono">NEURAL LINK</span><div class="side-crosshair"></div><img src="{prefix}assets/body.svg" width="140" height="240" alt="" loading="lazy"><span class="mono">HUMAN / 001</span></div></div><div class="dossier-bottom mono"><span>{'FICHAS WEB' if key=='pt' else 'WEB SHEETS'} — {d['country']}</span><span>CHARACTER / SYSTEM</span></div></div></div>
<div class="stage-bottom mono"><span class="stage-open">{c['viewCase']}{arrow()}</span></div>'''

def footer(key,home='index.html'):
    d=D[key];c=COPY[key]
    return f'<div class="footer-bottom wrap"><span class="mono">© 2026 HUDE · {d["country"]}</span><a class="privacy-link" href="#privacy-notice" data-open-privacy>{"Privacidade" if key=="pt" else "Privacy"}</a><a href="#top">{c["backTop"]}{arrow()}</a></div></footer>'+privacy_notice(key)+contact_dialog(key)+image_dialog(key)+'</body></html>'

def privacy_notice(key):
    pt=key=='pt'
    title='Sua privacidade' if pt else 'Your privacy'
    summary='Este portfólio não usa cookies de rastreamento, anúncios ou ferramentas de análise. As fontes são carregadas pelo próprio site.' if pt else 'This portfolio uses no tracking cookies, ads or analytics. Fonts are served by this website.'
    details='O que você precisa saber' if pt else 'What you should know'
    text='A hospedagem no GitHub Pages registra endereços IP para segurança. Os dados digitados na demonstração ficam apenas na página e são apagados ao recarregar. Ao fechar este aviso, uma preferência é salva somente nesta sessão da aba, sem identificador de visitante. Links para redes sociais abrem serviços com políticas próprias. Evite inserir dados pessoais na demonstração.' if pt else 'GitHub Pages logs IP addresses for security. Data entered in the demonstration stays in the page and resets on reload. Dismissing this notice stores only a preference for this tab session, without a visitor identifier. Social links open services with their own policies. Avoid entering personal data in the demonstration.'
    return f'''<section class="privacy-notice" id="privacy-notice" data-nosnippet role="region" aria-labelledby="privacy-title"><h2 id="privacy-title" tabindex="-1">{title}</h2><p>{summary}</p><details><summary>{details}</summary><p>{text}</p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">{'Privacidade do GitHub' if pt else 'GitHub privacy statement'}{arrow()}</a></details><button type="button" data-close-privacy hidden>{'Entendi' if pt else 'Got it'}</button></section>'''

def contact_dialog(key):
    pt=key=='pt'
    title='Como prefere conversar?' if pt else 'How would you like to connect?'
    body='Escolha onde prefere conversar e me conta sua ideia.' if pt else 'Pick your favorite place to chat and tell me your idea.'
    options=''.join(f'<a class="contact-option" href="{url}"'+(' target="_blank" rel="noopener noreferrer"' if url.startswith('https:') else '')+f'>{social_icon(icon)}<span><strong>{label}</strong><small>{detail}</small></span>{arrow()}</a>' for icon,label,detail,url in [('Email','E-mail' if pt else 'Email','huderpg@gmail.com','mailto:huderpg@gmail.com'),('Instagram','Instagram','@_huderpg_',IG),('TikTok','TikTok','@hudeplay','https://www.tiktok.com/@hudeplay'),('Discord','Discord','Abrir perfil' if pt else 'Open profile','https://discord.com/users/430844973584482304')])
    return f'''<dialog class="contact-dialog" id="contact-dialog" aria-labelledby="contact-dialog-title" aria-describedby="contact-dialog-description"><button class="dialog-close" type="button" data-close-contact aria-label="{'Fechar contato' if pt else 'Close contact'}">×</button><p class="eyebrow">{'PODE ME CHAMAR' if pt else 'GET IN TOUCH'}</p><h2 id="contact-dialog-title">{title}</h2><p id="contact-dialog-description">{body}</p><div class="contact-options">{options}</div><button class="contact-mode" type="button" data-toggle-contact-focus aria-pressed="false" data-focus-label="{'Colocar em foco' if pt else 'Focus view'}" data-dock-label="{'Deixar na lateral' if pt else 'Move to the side'}">{'Colocar em foco' if pt else 'Focus view'}</button></dialog>'''

def contact(key,case=False):
    c=COPY[key]
    return f'<footer class="site-footer" id="contact"><div class="contact wrap"><div><p class="eyebrow">{c["contactLabel"]}</p><h2>{c["contactTitle"]}</h2></div><div class="contact-action"><p>{c["contactBody"]}</p><a class="nav-contact footer-contact" href="mailto:huderpg@gmail.com" data-open-contact aria-haspopup="dialog" aria-controls="contact-dialog"><span>{c["start"]}</span>{arrow()}</a></div></div>'

def image_gallery(key,group,prefix):
    items=json.loads((ROOT/'gallery.json').read_text())
    hint='Clique para ampliar' if key=='pt' else 'Click to enlarge'
    cards=[]
    for item in items:
        if item['group']!=group: continue
        label=e(item[key]);slug=item['slug']
        cards.append(f'<figure class="gallery-card"><a href="{prefix}assets/gallery/{slug}.webp" data-gallery="{group}" data-caption="{label}" aria-label="{label} — {hint}" aria-haspopup="dialog" aria-controls="image-dialog"><span class="gallery-preview"><img src="{prefix}assets/gallery/{slug}-thumb.webp" width="{item["width"]}" height="{item["height"]}" alt="{label}" loading="lazy" decoding="async"><span class="gallery-expand" aria-hidden="true">{arrow()}</span></span><span class="gallery-caption">{label}</span></a></figure>')
    return f'<div class="portfolio-gallery gallery-{group}"><div class="gallery-grid">'+''.join(cards)+'</div></div>'

def image_dialog(key):
    pt=key=='pt'
    return f'''<dialog class="image-dialog" id="image-dialog" aria-label="{'Visualização da imagem' if pt else 'Image viewer'}"><div class="image-toolbar"><p id="image-caption" aria-live="polite"></p><button class="image-zoom" type="button" data-image-zoom aria-pressed="false">{'Zoom' if pt else 'Zoom'}</button><button type="button" data-close-image aria-label="{'Fechar imagem' if pt else 'Close image'}">×</button></div><div class="image-canvas"><img id="image-full" alt=""></div><div class="image-navigation"><button type="button" data-image-prev aria-label="{'Imagem anterior' if pt else 'Previous image'}">←</button><span id="image-count" aria-live="polite"></span><button type="button" data-image-next aria-label="{'Próxima imagem' if pt else 'Next image'}">→</button></div></dialog>'''

def home(key):
    d=D[key];c=COPY[key];pre='../' if key=='pt' else ''
    tags=''.join(f'<span>{t}</span>' for t in c['tags'])
    rows=''.join(f'<details class="service-row" id="{"sheets" if i==1 else "systems"}" open><summary aria-labelledby="{'sheets' if i==1 else 'systems'}-title" aria-describedby="{'sheets' if i==1 else 'systems'}-tag"><h2 class="service-summary"><span class="service-name"><span class="service-title" id="{'sheets' if i==1 else 'systems'}-title">{title}</span> <small class="mono" id="{'sheets' if i==1 else 'systems'}-tag">{tag}</small></span><span class="service-plus" aria-hidden="true"></span></h2></summary><div class="service-body"><div class="service-intro"><p>{desc}</p><a class="text-link" href="mailto:huderpg@gmail.com" data-open-contact aria-haspopup="dialog" aria-controls="contact-dialog"><span>{c["start"]}</span>{arrow()}</a></div>{image_gallery(key,"sheets" if i==1 else "systems",pre)}</div></details>' for i,(title,tag,desc) in enumerate(c['serviceRows'],1))
    socials=''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer"><span class="profile-label">{social_icon(name)}<span>{name}<small>{handle}</small></span></span>{arrow()}</a>' for name,handle,url in [('YouTube','@Hudezin','https://www.youtube.com/@Hudezin'),('Instagram','@_huderpg_',IG),('TikTok','@hudeplay','https://www.tiktok.com/@hudeplay')])
    return head(key,pre)+header(key)+f'''<main id="main">
<section class="hero wrap"><div class="hero-top mono"><span class="availability"><i></i>{c['availability']}</span></div><div class="hero-grid"><h1>{c['hero']}</h1><div class="hero-intro"><p>{c['intro']}</p><a class="text-link" href="#work"><span>{c['work']}</span>{arrow('right')}</a></div></div></section>
<section class="selected-work wrap" id="work" aria-label="{d['nav'][0]}"><a class="project-stage" href="projects/utopia.html" aria-label="{c['stage']}">{project_art(key,pre)}</a><article class="project-caption"><h2>{c['caseTitle']}</h2><p class="project-description">{c['caseDescription']}</p><div class="project-meta"><div class="project-tags mono">{tags}</div><a class="text-link" href="projects/utopia.html"><span>{c['viewCase']}</span>{arrow()}</a></div><span class="project-disclosure mono">{c['designStudy']}</span></article></section>
<section class="services wrap" id="services"><div class="service-list">{rows}</div></section>
<section class="profiles wrap" id="profiles"><nav class="profile-links" aria-label="{'Perfis sociais' if key=='pt' else 'Social profiles'}">{socials}</nav></section>
</main>'''+contact(key)+footer(key)

def case(key):
    d=D[key];c=COPY[key];pre='../../' if key=='pt' else '../'
    return head(key,pre,True)+header(key,True)+f'''<main id="main"><section class="case-hero wrap"><a class="case-back text-link" href="../#work">{arrow('right')}{d['back']}</a><div class="case-hero-top"><h1>{'Fichas web' if key=='pt' else 'Web sheets'}</h1></div><div class="case-heading"><h2>{c['caseHero']}</h2><p>{c['caseHeroBody']}</p></div></section><section class="case-showcase wrap" aria-label="{'Fichas web' if key=='pt' else 'Web character sheets'}"><div class="project-stage case-stage">{project_art(key,pre)}</div><p class="case-image-caption mono">{c['designStudy']}</p></section><section class="case-overview wrap"><div><h2>{c['caseHeading']}</h2><p>{c['caseOverviewBody']}</p></div></section><section class="interactive-section" id="demo"><div class="wrap"><div class="interactive-heading"><div><p class="eyebrow">{c['demoLabel']}</p><h2>{c['demoTitle']}</h2></div><p>{'Escolha um espaço no mapa para adicionar um implante. Dê um nome, anote o que ele faz e ajuste a cibernética para ver como fica.' if key=='pt' else 'Pick a slot on the map to add an implant. Give it a name, note what it does and adjust its cybernetics to see how it fits.'}</p></div><div class="demo implants-only"><iframe class="official-implants" src="{pre}assets/utopia-implants/{'index.html' if key=='pt' else 'en.html'}?v=official-1" title="{'Implantes — ficha oficial UTOPIA' if key=='pt' else 'Implants — official UTOPIA sheet'}" loading="lazy"></iframe></div></div></section></main>'''+contact(key,True)+footer(key,'../index.html')

def build():
    for key in D:
        folder=ROOT/('pt' if key=='pt' else '')
        (folder/'projects').mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(home(key),encoding='utf-8')
        (folder/'projects/utopia.html').write_text(case(key),encoding='utf-8')
    (ROOT/'404.html').write_text(head('en','/Huderpg/',not_found=True)+'<header id="top" class="site-header"><div class="nav wrap">'+logo('/Huderpg/',prefix='/Huderpg/')+'</div></header><main id="main" class="not-found wrap"><p class="eyebrow">404 / WRONG TURN</p><h1>A different<br><em>kind of adventure.</em></h1><p>This page could not be found. Let’s get you back to the portfolio.</p>'+btn('Back to the portfolio','/Huderpg/')+'</main>'+contact('en')+footer('en','/Huderpg/'),encoding='utf-8')
    write_discovery_files(ROOT)
    print('Built 5 static pages: editorial home and UTOPIA case in English and Portuguese, plus 404.')
