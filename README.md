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

The portfolio demonstration uses sample data and does not persist personal information, contain analytics, or include the complete UTOPIA application. External profile links open in a separate tab. Manrope and IBM Plex Mono are self-hosted with their OFL licenses; no Google Fonts connections are made.

## GitHub Pages

Published from `main`, folder `/ (root)`, through GitHub Pages. A `.nojekyll` file is included.

- English: https://harley-aguilar.github.io/Huderpg/
- Português: https://harley-aguilar.github.io/Huderpg/pt/index.html

## Validation

`python3 check_site.py` checks language metadata, local links, canonical URLs and required interactive controls. `node --check assets/app.js` checks JavaScript syntax. Live browser checks passed for English/Portuguese navigation, case pages, editable name and attributes, resource sliders, inventory/implant tabs, keyboard tab navigation and dice rolls.

## Editorial art direction

The portfolio uses a permanent dark palette, nonbinary purple, bold Manrope headings, a gently glowing header rule, large project imagery and an original polyhedral mark. Project visuals are editable HTML/SVG interface studies, clearly labeled as sample data. The body silhouette is retained from the owner’s UTOPIA source.

References studied (inspiration, no third-party artwork reused):

- [Locomotive](https://locomotive.ca/en): clear project-led portfolio structure.
- [Aparelho Studio](https://aparelho.studio/): editorial sequencing, typographic contrast and restrained accent color.
- [Mothership Companion](https://www.tuesdayknightgames.com/pages/mothership-companion-app): practical character-tool presentation.
- [WCAG contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): readable foreground/background combinations and focus states.

No invented commercial results, client testimonials or additional project credits were introduced. The visual language of UTOPIA remains distinct from the portfolio’s editorial identity. Motion respects reduced-motion preferences; content and service disclosures remain available without JavaScript.

## Privacy and security

All five HTML pages declare a restrictive Content Security Policy through a meta element: local scripts, styles, images and fonts only; no outbound fetches, forms, frames, plugins or base URL changes. JSON-LD is allowed by its generated SHA-256 hash. Inline executable scripts and inline styles are not allowed. External links use noopener/noreferrer; a no-referrer policy applies to the pages. GitHub Pages serves the site over HTTPS. Header-only protections such as frame-ancestors are not claimed by this static meta policy.

A bilingual privacy notice appears on first entry in each tab session. Only its dismissal preference is stored in sessionStorage; no visitor ID is generated. If storage is unavailable, the notice remains dismissible on the current page. It can be reopened from the footer. It explains the absence of site tracking, session storage, the temporary demo values, external profiles and GitHub Pages IP security logs. Acknowledgement is not presented as tracking consent.

## Current typography and header interaction

Squartiqa (owner supplied) is used for display headings. Self-hosted Chakra Petch Medium/Bold is the reading face, with its OFL license alongside the fonts. The header d20 is a separate keyboard-accessible button rather than part of the home link. Clicking animates a tumble and announces a uniform crypto-random d20 result; reduced-motion users receive the result without the tumble.
