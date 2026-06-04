# Knowledge Base Schema

## What This Is
A personal knowledge base about Pavel personal interests. 

## How It's Organized
- raw/ contains unprocessed source material. Never modify these files.
- wiki/ contains the organized wiki. AI maintains this entirely.
- wiki_html/ contains the HTML-rendered version of the wiki. AI maintains this entirely; never edit manually.
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
- A parallel HTML version of the wiki lives in `wiki_html/`; never edit it manually
- Every `wiki/<topic>.md` gets a matching `wiki_html/<topic>.html`
- `wiki_html/INDEX.html` is the main hub page, mirroring `wiki/INDEX.md`
- Internal `[[topic-name]]` links become `<a href="topic-name.html">` relative links
- Every HTML file must follow only the design tokens in `DESIGN.md` at the repo root — read it before generating any HTML
- Each HTML file is self-contained: inline all CSS, no external stylesheets or JS frameworks
- Before building a page, read `wiki_html/components/CATALOG.md` and pick components whose patterns fit the content; adapt their structure and styles using DESIGN.md tokens — do not copy whole files
- Page structure: visible top "Back to index" link to `INDEX.html` → masthead (eyebrow + serif h1 with italic `<em>` on a key word + intro paragraph + toc pills) → one `<section>` per H2 → footer with link back to INDEX.html
- Every topic HTML page must include an immediately visible back button/link near the top of the page pointing to `INDEX.html`, so readers do not need to scroll to the footer to return to the hub
- When the matching `wiki/<topic>.md` references raw-source images or figures, carry over a selected set of the most explanatory figures into the HTML page near the relevant section, with meaningful `alt` text and captions; avoid dumping every screenshot, but do not omit diagrams that materially clarify the concept
- Always end with a "Related Topics" section linking to other wiki pages
- For style and markup reference, read existing pages in `wiki_html/` — they are the canonical examples of correct output

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
