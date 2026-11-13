"""Rebuild the four sharing cards from the portfolio's own fonts and artwork.

Optional asset task: requires fontTools and FFmpeg with librsvg. Normal HTML
builds reuse the committed JPEG files and have no third-party dependencies.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET
import base64
import subprocess

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).parent
INK, PURPLE, LIGHT = '#f1edf5', '#9c59d1', '#c59cec'
FONTS = {
    'display': TTFont(ROOT / 'assets/fonts/squartiqa-4f.woff'),
    'body': TTFont(ROOT / 'assets/fonts/chakra-petch-500.woff'),
    'bold': TTFont(ROOT / 'assets/fonts/chakra-petch-700.woff'),
}


def text(value, x, y, size, color=INK, face='body', max_width=780):
    font = FONTS[face]
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    units = font['head'].unitsPerEm
    width = sum(glyphs[cmap.get(ord(c), '.notdef')].width for c in value)
    scale = min(size / units, max_width / width) if width else size / units
    paths = []
    for char in value:
        glyph = glyphs[cmap.get(ord(char), '.notdef')]
        pen = SVGPathPen(glyphs)
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
        paths.append(f'<path d="{pen.getCommands()}" fill="{color}"/>')
        x += glyph.width * scale
    return ''.join(paths)


def image_uri(path):
    return 'data:image/jpeg;base64,' + base64.b64encode(path.read_bytes()).decode()


def card(key, case, artwork, poster):
    mask = ET.parse(ROOT / 'assets/character/mask.svg').getroot()[0].get('d')
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">',
           '<defs><clipPath id="character"><path transform="translate(-95 -85)" d="' + mask + '"/></clipPath>',
           '<filter id="glow"><feGaussianBlur stdDeviation="4"/></filter></defs>',
           '<rect width="1200" height="630" fill="#141116"/>',
           '<circle cx="1120" cy="375" r="280" fill="#21172c"/>',
           '<rect x="54" y="43" width="72" height="72" rx="8" fill="#211929" stroke="#44334e"/>',
           '<svg x="60" y="49" width="60" height="60" viewBox="0 0 320 310">',
           f'<image href="{poster}" width="320" height="310" clip-path="url(#character)"/></svg>',
           text('hude.', 143, 101, 64, face='bold', max_width=180),
           text('RPG', 1060, 91, 25, LIGHT, 'bold', 90),
           f'<rect y="146" width="1200" height="4" fill="{LIGHT}" filter="url(#glow)"/>',
           f'<rect y="147" width="1200" height="2" fill="{LIGHT}"/>']
    if case:
        out += [text('FICHAS WEB.' if key == 'pt' else 'WEB SHEETS.', 54, 271, 58, INK, 'display', 780),
                text('Com a cara do seu RPG.' if key == 'pt' else 'Made to feel like your RPG.',
                     54, 344, 37, LIGHT, 'bold', 770),
                text('Experimente o mapa de implantes de UTOPIA.' if key == 'pt' else 'Try the UTOPIA implant map.',
                     54, 415, 24, INK, 'body', 770)]
    else:
        out += [text('SEU UNIVERSO.' if key == 'pt' else 'YOUR WORLD.', 54, 257, 48, INK, 'display', 775),
                text('PRONTO PRA JOGAR.' if key == 'pt' else 'READY TO PLAY.', 54, 330, 48, PURPLE, 'display', 775),
                text('Fichas personalizadas e sistemas de RPG.' if key == 'pt' else 'Custom character sheets and RPG systems.',
                     54, 415, 26, INK, 'body', 770)]
    selected = [artwork['mapa-implantes']] if case else [artwork['ficha-personagem'], artwork['ficha-yin-yang']]
    for i, data in enumerate(selected):
        x, y = 900 + i * 30, 208 + i * 25
        angle = (-5 if len(selected) == 2 and i == 0 else 5)
        out += [f'<g transform="rotate({angle} {x+105} {y+148})">',
                f'<rect x="{x-8}" y="{y-8}" width="226" height="314" rx="7" fill="#211929" stroke="#6b4d7f"/>',
                f'<image href="{data}" x="{x}" y="{y}" width="210" height="298"/></g>']
    out += ['<path d="M54 539H1146" stroke="#44334e"/>',
            text('FICHAS · SISTEMAS · RPG' if key == 'pt' else 'SHEETS · SYSTEMS · RPG',
                 54, 585, 18, LIGHT, 'bold', 480),
            text('harley-aguilar.github.io/Huderpg', 745, 585, 18, INK, 'body', 405), '</svg>']
    return ''.join(out)


def build():
    output = ROOT / 'assets/social'
    output.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix='huderpg-sharing-') as tmp:
        temp = Path(tmp)
        artwork = {}
        for slug in ['ficha-personagem', 'mapa-implantes', 'ficha-yin-yang']:
            jpeg = temp / f'{slug}.jpg'
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i',
                            str(ROOT / f'assets/gallery/{slug}-thumb.webp'),
                            '-frames:v', '1', '-q:v', '2', str(jpeg)], check=True)
            artwork[slug] = image_uri(jpeg)
        poster = image_uri(ROOT / 'assets/character/poster.jpg')
        for key in ['en', 'pt']:
            for case in [False, True]:
                slug = ('web-sheets' if case else 'portfolio') + '-' + key
                svg = temp / f'{slug}.svg'
                svg.write_text(card(key, case, artwork, poster))
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(svg),
                                '-frames:v', '1', '-q:v', '2', str(output / f'{slug}.jpg')], check=True)
    print('Built 4 localized 1200 × 630 sharing images.')


if __name__ == '__main__':
    build()
