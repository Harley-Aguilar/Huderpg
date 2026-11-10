# Huderpg

Bilingual portfolio for Hude / Harley Aguilar’s custom RPG character sheets, systems and digital experiences.

## Pages

- English: `index.html`
- Português: `pt/index.html`
- UTOPIA case and interactive demonstration: `projects/utopia.html` and `pt/projects/utopia.html`

Based on the [editable Figma design](https://www.figma.com/design/CNhWtPQ25SxiYpAIVhKrRA).

## Run locally

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. No Node dependencies or compilation are required.

## Edit

Update bilingual copy in `content.py` and `editorial.py`, and page templates in `layout.py`, then run `python3 build.py`. The interactive sheet preview is rendered by `demo.py`. Styling is in `assets/style.css`; interactions are in `assets/app.js`.

The portfolio demonstration uses sample data and does not persist personal information, contain analytics, or include the complete UTOPIA application. External profile links open in a separate tab. Google Fonts supplies Space Grotesk and IBM Plex Mono, with local system fallbacks.

## GitHub Pages

Published from `main`, folder `/ (root)`, through GitHub Pages. A `.nojekyll` file is included.

- English: https://harley-aguilar.github.io/Huderpg/
- Português: https://harley-aguilar.github.io/Huderpg/pt/index.html

## Validation

`python3 check_site.py` checks language metadata, local links, canonical URLs and required interactive controls. `node --check assets/app.js` checks JavaScript syntax. Live browser checks passed for English/Portuguese navigation, case pages, editable name and attributes, resource sliders, inventory/implant tabs, keyboard tab navigation and dice rolls.

## Editorial art direction

The redesign combines a warm paper palette, terracotta accents, Manrope with Instrument Serif, fine rules, large project imagery and an original polyhedral mark. Project visuals are editable HTML/SVG interface studies, clearly labeled as sample data. The body silhouette is retained from the owner’s UTOPIA source.

References studied (inspiration, no third-party artwork reused):

- [Locomotive](https://locomotive.ca/en): clear project-led portfolio structure.
- [Aparelho Studio](https://aparelho.studio/): editorial sequencing, typographic contrast and restrained accent color.
- [Mothership Companion](https://www.tuesdayknightgames.com/pages/mothership-companion-app): practical character-tool presentation.
- [WCAG contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): readable foreground/background combinations and focus states.

No invented commercial results, client testimonials or additional project credits were introduced. The visual language of UTOPIA remains distinct from the portfolio’s editorial identity. Motion respects reduced-motion preferences; content and service disclosures remain available without JavaScript.
