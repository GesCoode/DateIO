# Visagely — Homepage Redesign Concepts

Three full redesigns of the `visagely.com` landing page. All keep the existing positioning and
core content (from `src/routes/(marketing)/+page.svelte` and `src/lib/data/faq.ts`) but rethink
hierarchy, spacing, typography, composition and presentation. Shared goals: modern, elegant,
minimal, trustworthy, high-tech; product and generated photography as the visual focus; clear CTAs;
strong trust/privacy story; no neon, glassmorphism or heavy gradients.

The generated portraits in `assets/` are all the **same person across scenes**, created from one
reference to demonstrate the product's core promise (identity preserved, scenes varied).

## Concepts

### 1 · Editorial Light — `concept-1-editorial-light.html`
A modern photography-brand feel. Warm paper background, Playfair Display serif headlines, generous
whitespace, an asymmetric photo gallery, and a dark privacy band for contrast. Elegant and
premium; photography-forward.

![Concept 1](renders/concept-1-editorial-light.png)

### 2 · Technical Minimal — `concept-2-technical-minimal.html`
A high-end consumer-tech / product page. Near-white, Swiss grid, Inter + IBM Plex Mono technical
labels, a "generic AI vs. your private model" comparison, and a privacy spec-sheet. Communicates
capability, precision and trust; restrained and structured.

![Concept 2](renders/concept-2-technical-minimal.png)

### 3 · Cinematic Dark — `concept-3-cinematic-dark.html`
A premium launch-page feel. Dark palette, full-bleed cinematic hero, gold accents, large imagery
and a feature split. Confident and dramatic while staying tasteful (no neon/glow).

![Concept 3](renders/concept-3-cinematic-dark.png)

## Shared section structure

Nav · Hero (headline + CTA + hero photography) · Trust strip · How it works (3 steps) · Why it's
different (vs. generic AI) · Gallery (one person, many scenes) · Privacy & data · FAQ · Final CTA ·
Footer.

## Rendering

Self-contained HTML; fonts via Google Fonts. Rendered full-page at 2× with headless Chrome:

```sh
# from /tmp/shot with puppeteer-core installed
node shot2.js   # writes PNGs used in renders/
```
