"""Regression checks for published metadata, language pairs and discovery files."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import base64
import hashlib
import json
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
BASE = 'https://harley-aguilar.github.io/Huderpg/'
PUBLIC = {
    'index.html': ('en', BASE),
    'pt/index.html': ('pt-BR', BASE + 'pt/'),
    'projects/utopia.html': ('en', BASE + 'projects/utopia.html'),
    'pt/projects/utopia.html': ('pt-BR', BASE + 'pt/projects/utopia.html'),
}


class Head(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.meta, self.links, self.title, self.schema, self.details = {}, [], '', '', []
        self.lang, self.in_title, self.in_schema = '', False, False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'meta':
            key = a.get('name') or a.get('property') or a.get('http-equiv')
            if key:
                assert key not in self.meta, ('duplicate metadata', key)
                self.meta[key] = a.get('content', '')
        if tag == 'link':
            self.links.append(a)
        if tag == 'title':
            self.in_title = True
        if tag == 'script':
            self.in_schema = a.get('type') == 'application/ld+json'
        if tag == 'details' and a.get('class') == 'service-row':
            self.details.append(a)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script':
            self.in_schema = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_schema:
            self.schema += data

    def canonical(self):
        return self.link_map('canonical')['']

    def link_map(self, rel):
        return {a.get('hreflang', ''): a['href'] for a in self.links if a.get('rel') == rel}


def jpeg_dimensions(path):
    """Read the JPEG frame header without decoding images or adding dependencies."""
    data = path.read_bytes()
    assert data[:2] == b'\xff\xd8', (path, 'not a JPEG')
    offset = 2
    while offset < len(data):
        assert data[offset] == 0xff
        while data[offset] == 0xff:
            offset += 1
        marker = data[offset]
        offset += 1
        if marker in (0xd8, 0xd9) or 0xd0 <= marker <= 0xd7:
            continue
        size = struct.unpack('>H', data[offset:offset+2])[0]
        if marker in (0xc0, 0xc1, 0xc2):
            height, width = struct.unpack('>HH', data[offset+3:offset+7])
            return width, height
        offset += size
    raise AssertionError((path, 'missing JPEG frame header'))


pages = {path: Head((ROOT / path).read_text()) for path in PUBLIC}
assert len({p.title for p in pages.values()}) == 4, 'Each page needs its own title'
assert len({p.meta['description'] for p in pages.values()}) == 4, 'Descriptions must be page-specific'
assert len({p.meta['og:image'] for p in pages.values()}) == 4, 'Each language/page has its own sharing card'
by_url = {page.canonical(): page for page in pages.values()}
for path, page in pages.items():
    lang, url = PUBLIC[path]
    assert page.lang == lang and page.canonical() == url, (path, 'canonical/language')
    assert 'noindex' not in page.meta['robots']
    assert page.meta['og:url'] == url and page.meta['og:title'] == page.title
    assert page.meta['og:description'] == page.meta['description']
    assert page.meta['twitter:title'] == page.title
    assert page.meta['twitter:card'] == 'summary_large_image'
    assert page.meta['twitter:image'] == page.meta['og:image']
    assert page.meta['og:locale'] == ('pt_BR' if lang == 'pt-BR' else 'en_US')
    assert page.meta['og:locale:alternate'] != page.meta['og:locale']
    assert page.meta['og:image:alt'] and page.meta['twitter:image:alt']
    assert page.meta['og:image:width'] == '1200' and page.meta['og:image:height'] == '630'
    image_path = ROOT / page.meta['og:image'].removeprefix(BASE)
    assert page.meta['og:image'].startswith(BASE) and image_path.is_file()
    assert jpeg_dimensions(image_path) == (1200, 630)
    alternates = page.link_map('alternate')
    assert set(alternates) == {'en', 'pt-BR', 'x-default'}
    assert alternates[lang] == url and alternates['x-default'] == alternates['en']
    for alt_lang in ('en', 'pt-BR'):
        other = by_url[alternates[alt_lang]]
        assert other.lang == alt_lang and other.link_map('alternate') == alternates
    schema = json.loads(page.schema)
    assert schema['@context'] == 'https://schema.org'
    webpage = next(item for item in schema['@graph'] if item['@type'] == 'WebPage')
    assert webpage['url'] == url and webpage['inLanguage'] == lang
    assert any(item['@type'] == 'Person' for item in schema['@graph'])
    digest = base64.b64encode(hashlib.sha256(page.schema.encode()).digest()).decode()
    assert f"'sha256-{digest}'" in page.meta['Content-Security-Policy'], (path, 'JSON-LD is blocked by CSP')
    if path in ('index.html', 'pt/index.html'):
        assert len(page.details) == 2
        assert {d['id'] for d in page.details} == {'sheets', 'systems'}
        assert all('open' in d for d in page.details), (path, 'Galleries must start open')

for path in ['404.html', 'assets/utopia-implants/index.html', 'assets/utopia-implants/en.html']:
    page = Head((ROOT / path).read_text())
    assert 'noindex' in page.meta['robots'], (path, 'Not a search landing page')
    assert page.canonical() == BASE + path
    if path == '404.html':
        assert not page.link_map('alternate') and not page.schema

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
sitemap = ET.parse(ROOT / 'sitemap.xml')
entries = sitemap.findall('s:url', ns)
assert len(entries) == 4 and {item.find('s:loc', ns).text for item in entries} == set(by_url)
for item in entries:
    url = item.find('s:loc', ns).text
    assert not urlsplit(url).query and not urlsplit(url).fragment
    assert {a.get('hreflang'): a.get('href') for a in item.findall('x:link', ns)} == by_url[url].link_map('alternate')
assert f'Sitemap: {BASE}sitemap.xml' in (ROOT / 'robots.txt').read_text()
print('PASS: localized SEO, reciprocal language links, sharing cards, structured data/CSP, sitemap, noindex and open galleries.')
