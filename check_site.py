"""Check static output and relative navigation without external dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

ROOT=Path(__file__).parent.resolve()
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=[];self.lang=None;self.canonical=None;self.h1=0;self.controls=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.append(a['id'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
        for key in ('src','href'):
            if key in a:self.links.append(a[key])
        if tag in ('input','select','button'):self.controls.append(a)

pages={}
for file in ROOT.rglob('*.html'):
    p=Page();p.feed(file.read_text());pages[file]=p
    assert p.h1==1,(file,'one main heading required')
    assert len(p.ids)==len(set(p.ids)),(file,'duplicate IDs')
    assert p.lang==('pt-BR' if 'pt' in file.relative_to(ROOT).parts else 'en'),(file,'language')
    assert p.canonical and p.canonical.startswith('https://harley-aguilar.github.io/Huderpg/'),(file,'canonical')
for file,p in pages.items():
    for link in p.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc:continue
        target=(ROOT/parts.path.removeprefix('/Huderpg/')) if parts.path.startswith('/Huderpg/') else file.parent/unquote(parts.path)
        if not parts.path:target=file
        if target.is_dir():target=target/'index.html'
        target=target.resolve()
        assert target.exists(),(file,link,'broken local link')
        if parts.fragment and target in pages:assert parts.fragment in pages[target].ids,(file,link,'missing anchor')
    if file.name=='utopia.html':
        assert len([c for c in p.controls if 'data-resource' in c])==3
        assert len([c for c in p.controls if c.get('role')=='tab'])==3
        assert any('data-roll' in c for c in p.controls)
print(f'PASS: {len(pages)} pages; local links, anchors, language metadata, headings and demo controls.')
