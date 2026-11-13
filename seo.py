"""Search and sharing metadata for the four public, bilingual pages."""
from html import escape
from pathlib import Path
import base64
import hashlib
import json
import xml.etree.ElementTree as ET

BASE = 'https://harley-aguilar.github.io/Huderpg/'
LANGUAGES = {'en': 'en', 'pt': 'pt-BR'}
META = {
    'en': {
        'home': ('Hude — Custom RPG Character Sheets & Systems',
                 'Custom automated character sheets, original tabletop RPG systems and web sheets by Hude. Find ideas for your table and tell me about your game.'),
        'case': ('Web Character Sheets for Your RPG — Hude',
                 'A character sheet that feels like your RPG, right in your browser. Explore Hude’s web sheets and try the interactive UTOPIA implant map.'),
        'image_alt': 'Hude RPG: custom character sheets and original RPG systems, with examples from the portfolio.',
        'case_image_alt': 'Hude web character sheets, with an example implant sheet from UTOPIA.',
        'home_name': 'Home', 'case_name': 'Web character sheets',
    },
    'pt': {
        'home': ('Hude — Fichas Automáticas e Sistemas de RPG',
                 'Fichas automáticas personalizadas, sistemas autorais de RPG de mesa e fichas web. Conheça o trabalho do Hude e me conte sua ideia para a sua mesa.'),
        'case': ('Fichas Web Personalizadas para seu RPG — Hude',
                 'Uma ficha com a cara do seu RPG, direto no navegador. Conheça as fichas web do Hude e experimente o mapa de implantes interativo de UTOPIA.'),
        'image_alt': 'Hude RPG: fichas personalizadas e sistemas autorais de RPG, com exemplos do portfólio.',
        'case_image_alt': 'Fichas web do Hude, com um exemplo de ficha de implantes de UTOPIA.',
        'home_name': 'Início', 'case_name': 'Fichas web',
    },
}


def page_url(key, case=False):
    return BASE + ('pt/' if key == 'pt' else '') + ('projects/utopia.html' if case else '')


def sharing_image(key, case=False):
    return BASE + f'assets/social/{"web-sheets" if case else "portfolio"}-{key}.jpg'


def structured_data(key, case=False):
    title, description = META[key]['case' if case else 'home']
    url = page_url(key, case)
    person = {'@type': 'Person', '@id': BASE + '#hude', 'name': 'Hude',
              'alternateName': 'Harley Aguilar', 'url': BASE,
              'sameAs': ['https://www.youtube.com/@Hudezin',
                         'https://www.instagram.com/_huderpg_/',
                         'https://www.tiktok.com/@hudeplay']}
    website = {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE,
               'name': 'Hude RPG', 'inLanguage': list(LANGUAGES.values()),
               'publisher': {'@id': person['@id']}}
    page = {'@type': 'WebPage', '@id': url + '#webpage', 'url': url,
            'name': title, 'description': description, 'inLanguage': LANGUAGES[key],
            'isPartOf': {'@id': website['@id']}, 'about': {'@id': person['@id']},
            'primaryImageOfPage': {'@type': 'ImageObject', 'url': sharing_image(key, case),
                                   'width': 1200, 'height': 630},
            'mainEntity': {'@id': url + '#project' if case else person['@id']}}
    graph = [person, website, page]
    if case:
        graph.append({'@type': 'CreativeWork', '@id': url + '#project', 'url': url,
                      'name': META[key]['case_name'], 'description': description,
                      'inLanguage': LANGUAGES[key], 'author': {'@id': person['@id']},
                      'image': sharing_image(key, True)})
        graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumbs',
                      'itemListElement': [
                          {'@type': 'ListItem', 'position': 1,
                           'name': META[key]['home_name'], 'item': page_url(key)},
                          {'@type': 'ListItem', 'position': 2,
                           'name': META[key]['case_name'], 'item': url}]})
        page['breadcrumb'] = {'@id': url + '#breadcrumbs'}
    return {'@context': 'https://schema.org', '@graph': graph}


def metadata(key, case=False, not_found=False):
    """Return HTML metadata plus the exact JSON-LD hash allowed by the CSP."""
    e = escape
    data = META[key]
    title, description = data['case' if case else 'home']
    url = page_url(key, case)
    if not_found:
        return ('<title>Page not found — Hude RPG</title>'
                '<meta name="description" content="This page could not be found. Head back to Hude’s RPG portfolio.">'
                '<meta name="robots" content="noindex,follow">'
                f'<link rel="canonical" href="{BASE}404.html">'), ''
    locale = 'pt_BR' if key == 'pt' else 'en_US'
    alternate_locale = 'en_US' if key == 'pt' else 'pt_BR'
    image = sharing_image(key, case)
    image_alt = data['case_image_alt' if case else 'image_alt']
    schema = json.dumps(structured_data(key, case), ensure_ascii=False, separators=(',', ':'))
    schema_hash = base64.b64encode(hashlib.sha256(schema.encode()).digest()).decode()
    html = f'''<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{page_url('en', case)}">
<link rel="alternate" hreflang="pt-BR" href="{page_url('pt', case)}">
<link rel="alternate" hreflang="x-default" href="{page_url('en', case)}">
<link rel="sitemap" type="application/xml" href="{BASE}sitemap.xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Hude RPG">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{alternate_locale}">
<meta property="og:image" content="{image}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{e(image_alt)}">
<script type="application/ld+json">{schema}</script>'''
    return html, schema_hash


def write_discovery_files(root):
    sitemap_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml_ns = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('', sitemap_ns)
    ET.register_namespace('xhtml', xhtml_ns)
    sitemap = ET.Element(f'{{{sitemap_ns}}}urlset')
    for case in (False, True):
        for key in LANGUAGES:
            item = ET.SubElement(sitemap, f'{{{sitemap_ns}}}url')
            ET.SubElement(item, f'{{{sitemap_ns}}}loc').text = page_url(key, case)
            for lang, url in [('en', page_url('en', case)),
                              ('pt-BR', page_url('pt', case)),
                              ('x-default', page_url('en', case))]:
                ET.SubElement(item, f'{{{xhtml_ns}}}link', rel='alternate', hreflang=lang, href=url)
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(Path(root) / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (Path(root) / 'robots.txt').write_text(
        'User-agent: *\nAllow: /Huderpg/\nSitemap: ' + BASE + 'sitemap.xml\n', encoding='utf-8')
