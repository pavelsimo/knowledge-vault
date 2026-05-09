---
name: Knowledge Vault Design System
colors:
  ivory: "#FAF9F5"
  paper: "#FFFFFF"
  slate: "#141413"
  clay: "#D97757"
  clay-d: "#B85C3E"
  oat: "#E3DACC"
  olive: "#788C5D"
  g100: "#F0EEE6"
  g200: "#E6E3DA"
  g300: "#D1CFC5"
  g500: "#87867F"
  g700: "#3D3D3A"
typography:
  heading-xl:
    fontFamily: 'ui-serif, Georgia, "Times New Roman", Times, serif'
    fontSize: clamp(38px, 5.4vw, 62px)
    fontWeight: "500"
    lineHeight: 1.06
    letterSpacing: -0.018em
  heading-md:
    fontFamily: 'ui-serif, Georgia, "Times New Roman", Times, serif'
    fontSize: 27px
    fontWeight: "500"
    lineHeight: 1.3
    letterSpacing: -0.012em
  heading-sm:
    fontFamily: 'ui-serif, Georgia, "Times New Roman", Times, serif'
    fontSize: 19px
    fontWeight: "500"
    lineHeight: 1.22
    letterSpacing: -0.008em
  body:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 16px
    fontWeight: "400"
    lineHeight: 1.55
    letterSpacing: 0em
  body-sm:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 13.5px
    fontWeight: "400"
    lineHeight: 1.5
    letterSpacing: 0em
  label:
    fontFamily: 'ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace'
    fontSize: 12px
    fontWeight: "400"
    lineHeight: 1.4
    letterSpacing: 0.12em
  label-sm:
    fontFamily: 'ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace'
    fontSize: 11px
    fontWeight: "400"
    lineHeight: 1.4
    letterSpacing: 0em
rounded:
  sm: 6px
  md: 10px
  lg: 14px
  full: 9999px
spacing:
  unit: 8px
  container-max: 1120px
  gutter: 32px
  section-gap: 72px
  card-gap: 20px
  card-min: 316px
components:
  card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate}"
    rounded: "{rounded.lg}"
    borderColor: "{colors.g300}"
    borderWidth: 1.5px
  card-hover:
    borderColor: "{colors.slate}"
    boxShadow: "0 10px 30px rgba(20, 20, 19, 0.10)"
  card-thumb:
    backgroundColor: "{colors.g100}"
    height: 132px
  card-title:
    textColor: "{colors.slate}"
    typography: "{typography.heading-sm}"
  card-desc:
    textColor: "{colors.g700}"
    typography: "{typography.body-sm}"
  card-file:
    textColor: "{colors.g500}"
    typography: "{typography.label-sm}"
  toc-pill:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.g700}"
    rounded: "{rounded.full}"
    borderColor: "{colors.g300}"
    borderWidth: 1.5px
    padding: 7px 14px
    typography: "{typography.label}"
  toc-pill-hover:
    borderColor: "{colors.slate}"
    textColor: "{colors.slate}"
  section-index:
    textColor: "{colors.clay}"
    typography: "{typography.label}"
    fontWeight: "600"
  eyebrow:
    textColor: "{colors.g500}"
    typography: "{typography.label}"
  code-block:
    backgroundColor: "{colors.g100}"
    borderColor: "{colors.g200}"
    borderWidth: 1px
    rounded: "{rounded.sm}"
    typography: "{typography.label-sm}"
    padding: 12px 16px
  table-header:
    backgroundColor: "{colors.g100}"
    typography: "{typography.label}"
  table-cell:
    borderColor: "{colors.g200}"
---

## Overview

The Knowledge Vault design system is derived from the thariqs "unreasonable effectiveness of HTML" visual language. It prizes legibility and warmth: warm ivory backgrounds, a clay accent for interactive emphasis, Georgia-family serifs for display text, and system-ui sans for body copy. Every wiki HTML file is self-contained — CSS is inlined, no external dependencies.

## Colors

`clay` (#D97757) is the sole accent color — use it for highlights, hover states, links, and active borders. `clay-d` (#B85C3E) is the darker variant for pressed states.

`slate` (#141413) is near-black used for primary text and active/hover borders.

`ivory` (#FAF9F5) is the page background. `paper` (#FFFFFF) is for elevated card surfaces.

The gray ramp handles structure without drawing attention:
- `g100` (#F0EEE6) — subtle fills, table headers, code blocks, thumb backgrounds
- `g200` (#E6E3DA) — inner borders (table rows, code block borders)
- `g300` (#D1CFC5) — card and pill borders at rest, section dividers
- `g500` (#87867F) — muted text, eyebrow labels, file names
- `g700` (#3D3D3A) — secondary body text, descriptions

`oat` (#E3DACC) and `olive` (#788C5D) are warm accents reserved for SVG illustrations and secondary visual highlights inside card thumbs.

## Typography

Three font stacks map to three semantic roles — never mix them across roles:

- **Serif** (`ui-serif, Georgia, "Times New Roman", Times, serif`) — display headings only
- **Sans** (`system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`) — all body and paragraph text
- **Mono** (`ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace`) — metadata, file names, index numbers, code, labels

Never substitute external web fonts. Rely only on these system font stacks so files remain self-contained.

Heading hierarchy: `heading-xl` for the page h1, `heading-md` for section h2s, `heading-sm` for card titles. Body text uses `body` (16px/1.55) and `body-sm` (13.5px/1.5) for descriptions. Labels and metadata use `label` (12px, 0.12em tracking, uppercase) and `label-sm` (11px) for file paths and index numbers.

## Layout

Container max-width is 1120px with 32px horizontal gutter (`padding: 0 32px 140px`). The large bottom padding (140px) ensures content never feels cramped above the footer.

Card grids use `repeat(auto-fill, minmax(316px, 1fr))` with 20px gap, left-indented 50px to align with section body (reset to 0 on narrow viewports).

Section vertical spacing is 72px `margin-top`. Masthead uses 80px top / 56px bottom padding with a 1.5px `g300` border-bottom.

## Elevation & Depth

Cards are flat at rest — no shadow. On hover: `transform: translateY(-3px)` plus `box-shadow: 0 10px 30px rgba(20,20,19,.10)`. Border transitions from `g300` to `slate` on hover to signal interactivity without color distraction.

Transitions use `150ms ease` for transform and box-shadow, `120ms` for color/border-color.

## Shapes

- Cards: 14px border-radius
- TOC pills: 9999px (fully pill-shaped)
- Tags and badges: 6px border-radius
- Code blocks: 6px border-radius
- Card thumbs: no border-radius on the thumb itself (clipped by the parent card's `overflow: hidden`)

## Components

All component tokens are in the YAML front matter. Key behavioral details:

**Cards** (`a.card`): flex column, paper background, 1.5px g300 border, 14px radius, `overflow: hidden`. Hover lifts the card and sharpens the border to slate. The thumb area transitions from g100 to oat on hover. The file/arrow row transitions to clay on hover with the arrow nudging right 3px.

**TOC pills** (`nav.toc a`): inline-flex, paper background, 1.5px g300 border, 999px radius, 7px 14px padding, 12.5px sans text. The index number inside uses `label-sm` mono in g500. Hover shifts border and text to slate; the index number shifts to clay.

**Section headers** (`.sec-head`): flex row with baseline alignment. The index (`.idx`) is `label` mono in clay at 13px/600 weight, fixed 34px width. The h2 is `heading-md` serif.

**Eyebrow** (`.eyebrow`): `label` mono, uppercase, g500, with a `::before` pseudo-element — 24×1.5px block in clay color — creating a decorative lead-in line.

**Code blocks**: g100 background, 1px g200 border, 6px radius, `label-sm` mono, 12px 16px padding.

**Tables**: `border-collapse: collapse`. `th` cells use g100 background, `label` mono, left-aligned. `td` cells have a 1px g200 border-bottom.

**Footer**: 1.5px g300 border-top, 36px padding-top, flex row space-between. Brand text is serif italic in g700. Links are clay with oat underline decoration, transitioning to clay on hover.

## Do's and Don'ts

- **DO** embed all CSS inline in every HTML file — no `<link>` tags, no CDN references.
- **DO** declare all color tokens as CSS custom properties in `:root` using the exact names from the YAML (e.g. `--clay`, `--ivory`, `--g300`).
- **DO** convert `[[wiki-link]]` syntax to relative `<a href="topic-name.html">` links.
- **DO** add `scroll-behavior: smooth` on `html` — the only JavaScript-adjacent behavior allowed.
- **DON'T** introduce any color, font family, font size, or spacing value not present in the YAML tokens above.
- **DON'T** use CSS frameworks (Bootstrap, Tailwind, etc.) or JavaScript libraries.
- **DON'T** add `<script>` tags beyond a minimal smooth-scroll inline if needed.
- **DON'T** use external images or icon fonts — SVG geometry inline only, using design system colors.
