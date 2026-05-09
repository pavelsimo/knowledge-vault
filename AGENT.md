# Knowledge Base Schema

## What This Is
A personal knowledge base about Pavel personal interests. 

## How It's Organized
- raw/ contains unprocessed source material. Never modify these files.
- wiki/ contains the organized wiki. AI maintains this entirely.
- outputs/ contains generated reports, answers, and analyses.

## Wiki Rules
- Every topic gets its own .md file in wiki/
- Every wiki file starts with a one-paragraph summary
- Link related topics to each other using [[topic-name]] format
- Maintain an INDEX.md in wiki/ that lists every topic with a one-line description
- When new raw sources are added, update the relevant wiki articles
- Give a lot of importance to research papers when the topic has a meaningful paper trail
- References to papers must be clickable markdown links
- When a paper is referenced, try your best to include a suitable supporting image or figure

## HTML Wiki Rules
- A parallel HTML version of the wiki lives in wiki_html/; never edit it manually
- Every wiki/<topic>.md gets a matching wiki_html/<topic>.html
- wiki_html/INDEX.html is the main entry point, mirroring wiki/INDEX.md
- Internal [[topic-name]] links become relative `<a href="topic-name.html">` links
- Every HTML file MUST follow ONLY the design system defined in DESIGN.md at the repo root
- Read DESIGN.md before generating any HTML — all colors, fonts, spacing, and component styles come exclusively from its YAML tokens
- Before building each page, read wiki_html/components/CATALOG.md and pick any components whose patterns fit the topic; adapt their structure and scripts — do NOT copy whole files, only the relevant patterns, restyled with DESIGN.md tokens
- The 20 component source files live in wiki_html/components/ and are the ONLY approved source of interactive patterns
- Each HTML file is self-contained: inline all CSS, no external stylesheets or JS frameworks
- Page structure per topic file:
  1. `<header class="masthead">` — eyebrow "Knowledge Vault", serif h1 with italic `<em>` on a key word, intro paragraph from the wiki summary, `<nav class="toc">` pills linking to each H2 section
  2. One `<section>` per H2 in the wiki source, with `.sec-head` (`.idx` number + h2 text)
  3. `<footer>` with a link back to INDEX.html
- INDEX.html: masthead title "Knowledge *Vault*", topic cards grouped by Pavel's interests, each topic as `a.card` linking to `<topic>.html`

## Change Log Rules
- wiki/LOG.md tracks every change made to the raw/ directory; never edit it manually
- Add an entry whenever a raw source is added, updated, or removed
- Entries are sorted newest-first — always prepend new rows, never append
- Format: markdown table with columns `| Date | Action | Source Path | Type | Summary |`
- Valid Action values: `added`, `updated`, `removed`
- Valid Type values: `clipping`, `course-material`, `paper`, `video-notes`, `code`, `image`, `dataset`, `other`
- Summary: one sentence describing the content added or changed

## My Interests
- AI
- Math
- Omniverse
- Robotics
- Investing
- XR
- LeRobot
- Game Programming
- Computer Graphics
- System Design
