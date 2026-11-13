# Huderpg — official portfolio

Hude’s bilingual portfolio for custom automated RPG character sheets, original
tabletop RPG systems and web character sheets. Published by GitHub Pages from
`main`, repository root; `.nojekyll` preserves the buildless static output.

## Public pages

| Page | English | Português |
| --- | --- | --- |
| Portfolio | https://harley-aguilar.github.io/Huderpg/ | https://harley-aguilar.github.io/Huderpg/pt/ |
| Web sheets | https://harley-aguilar.github.io/Huderpg/projects/utopia.html | https://harley-aguilar.github.io/Huderpg/pt/projects/utopia.html |

Both sheet and system galleries start **open** on each new page load. Visitors
can independently collapse/reopen either section, including using the keyboard.
The sheet gallery has three artworks; the system gallery has seven, with combat
specializations last. Artwork links support a full-size viewer, zoom and keyboard
navigation. The animated profile character appears before the Hude wordmark,
inside a violet frame, with moving paper clipped to its silhouette. Clicking it
pauses/resumes the animation; reduced-motion preferences start it paused.

## Edit and build

- `layout.py`: shared page templates and the two native `<details>` sections.
- `editorial.py` / `content.py`: bilingual visible copy and interface labels.
- `gallery.json`: image labels, dimensions and ordering.
- `seo.py`: unique titles/descriptions, canonical URLs, reciprocal language
  alternates, Open Graph/Twitter cards, JSON-LD and sitemap generation.
- `assets/style.css`: dark-only design, nonbinary purple, Squartiqa display
  type and self-hosted Chakra Petch Medium/Bold. The OFL license for Chakra
  Petch is included; Squartiqa was supplied by the owner.
- `assets/app.js`: privacy notice, dockable/focused contact dialog, image viewer,
  embedded-demo resizing and character-animation controls.

Run `python3 build.py` after template, copy or SEO edits. This generates the four
public pages, `404.html`, `sitemap.xml` and `robots.txt`, using only the Python
standard library. Serve the repository using a static web server for local use.
Managed workspace QA uses `sites-preview` and the ignored `dist/` mirror.

The four committed 1200 × 630 JPEG sharing images match each language and page.
To regenerate these optional artwork assets, run `python3 build_social.py` in an
environment with fontTools and FFmpeg/librsvg. Normal HTML builds use the committed
JPEGs and do not require those optional dependencies.

## SEO

Each public page has a self-canonical URL, `en` / `pt-BR` / `x-default` alternates,
localized search and sharing descriptions, locale-specific sharing images and
structured data describing the creator, website and page. Project pages also
describe the web-sheet example and include breadcrumb data. There are no invented
reviews, customers, results or commercial claims in the structured data.

The sitemap contains only the four canonical public pages, with reciprocal
language references. Both embedded implant pages and the error page carry
`noindex,follow` and are excluded from the sitemap. The privacy notice is excluded
from search snippets, while remaining available to visitors.

GitHub Pages hosts this repository below `/Huderpg/`. Crawlers read `robots.txt`
from the **host root**, not a project subdirectory. The repository’s file is a
portable deployment artifact; it does not override host-root rules. For explicit
submission, use `https://harley-aguilar.github.io/Huderpg/sitemap.xml` in an already
verified Search Console property, or reference it from the host owner’s root
robots file. No Search Console submission or verification is implied by this
release. Search engines determine discovery, indexing and result presentation.

## Demonstration, privacy and security

`assets/utopia-implants/` embeds only the official UTOPIA implant module. Names,
effects, installation slots and percentages can be edited; the total is recalculated.
Records exist only in memory and reset on reload. This portfolio does not contain
the full character application, cloud accounts, analytics or tracking cookies.

Contact buttons offer email, Instagram, TikTok and the owner-provided Discord
profile. The contact panel can stay at the side or become a focused modal.
External links use `noopener noreferrer`, and pages declare `no-referrer`.

The bilingual privacy notice stores only its dismissal flag in this tab’s
`sessionStorage`. It explains GitHub Pages security IP logs and external-service
policies and can be reopened from the footer. Demo input is escaped before being
rendered as HTML. Parent pages restrict sources to the site through a meta CSP;
their JSON-LD is allowed using the exact generated SHA-256 hash. The local iframe
has a separate CSP permitting the inline styles required by the supplied module.
Static meta policies do not claim header-only protections such as `frame-ancestors`.

## Validation

```sh
python3 build.py
python3 check_site.py
python3 check_seo.py
node --check assets/app.js
node --check assets/utopia-implants/implants.js
node --check assets/utopia-implants/implants-en.js
```

`check_site.py` checks all seven HTML files, local assets/links, anchors, heading
counts, language metadata and the implant-only demonstration. `check_seo.py`
checks distinct metadata, reciprocal language pairs, actual JPEG dimensions,
JSON-LD/CSP compatibility, canonical sitemap contents, noindex exclusions and
the default-open state of both galleries. Browser QA covers the gallery toggles,
image viewer, contacts, privacy controls, language navigation, implant editing,
percentage totals, removal and escaping, plus narrow-screen layout.
