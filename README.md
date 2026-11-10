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

Update the bilingual copy and page templates in `build.py`, then run `python3 build.py`. Styling is in `assets/style.css`; interactions are in `assets/app.js`.

The portfolio demonstration uses sample data and does not persist personal information, contain analytics, or include the complete UTOPIA application. External profile links open in a separate tab. Google Fonts supplies Space Grotesk and IBM Plex Mono, with local system fallbacks.

## GitHub Pages

The repository is ready to publish from `main`, folder `/ (root)`, in Settings → Pages. A `.nojekyll` file is included. Publication is subject to the owner’s visibility approval and the GitHub plan’s Pages availability.

## Validation

`python3 check_site.py` checks language metadata, local links, canonical URLs and required interactive controls. `node --check assets/app.js` checks JavaScript syntax. Browser verification of layout and interactions is pending publication approval.
