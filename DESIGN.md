# Design

## Theme

The website uses a light, calm product-marketing theme. The scene is a user sitting at a Mac or Windows computer, trying to safely upscale local images without uploading files. The interface should feel trustworthy, maintained, and practical.

## Palette

- Background: cool off-white with a faint blue-green cast.
- Surface: clean white panels with subtle borders.
- Ink: deep blue-charcoal for high readability.
- Muted text: blue-gray, dark enough for body contrast.
- Accent: restrained teal for primary actions and focus states.

Do not use purple AI gradients, beige craft neutrals, neon glow, or repeated glass cards.

## Typography

- Primary family: Geist first, then system sans and Chinese system fonts.
- Hero: large, balanced, maximum two lines on desktop.
- Section headings: strong, compact, no repeated uppercase eyebrow labels.
- Body: 65-75ch maximum where possible, readable contrast, no buzzword-heavy copy.

## Layout

- Static HTML and CSS remain the preferred architecture.
- The page follows a simple AIDA structure: navigation, hero, download/update, privacy, device guide, preview, FAQ, feedback, footer.
- Use varied section layouts instead of repeating identical card grids.
- Bento-like areas must collapse cleanly to one column on mobile.

## Components

- Buttons are full-pill, with clear contrast and tactile active states.
- Panels use 12-16px radii and borders. Avoid pairing heavy shadows with borders.
- Forms use labels above inputs, visible focus rings, and placeholder text with enough contrast.
- Language switching uses `data-lang` attributes and the body `en` class.

## Motion

- Motion is native CSS plus IntersectionObserver, not a framework dependency.
- Reveal motion is subtle and disabled under `prefers-reduced-motion: reduce`.
- Hover motion uses transform and filter only.

## Maintenance Notes

- Website entry: `docs/index.html`.
- Feedback success page: `docs/thanks.html`.
- Local app entry: `main.py`.
- Image processing core: `upscaler.py`.
- Version rule: each website or code update increments the final version by `0.0.1`, for example `v0.1.2` to `v0.1.3`.
