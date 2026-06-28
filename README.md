# Knowledge Vault

A personal knowledge base covering AI, math, robotics, system design, computer graphics, and related interests. Raw source material is ingested and compiled by AI into a structured wiki, rendered in both Markdown and self-contained HTML.

## Structure

```
raw/          # Unprocessed source material — never edit these files
wiki/         # Compiled Markdown wiki — AI-maintained
wiki_html/    # HTML-rendered wiki — AI-maintained, never edit manually
outputs/      # Generated reports, slides, and analyses
images/       # Shared image assets
```

### raw/ layout

| Directory | Content |
|-----------|---------|
| `raw/clippings/` | Web clippings, video notes, social posts, and reference snippets; existing contents stay unchanged internally |
| `raw/course-material/` | Course and tutorial source capsules such as CS109, CS231N, Hugging Face, MLOps, and LLM-from-scratch |
| `raw/reference-packs/` | Coherent reference/source packs such as Omniverse, system design, Hailo setup, tmux, and local models |
| `raw/inbox/` | Temporary landing area for newly added unsorted raw material before it is promoted into a source capsule |

## Wiki

`wiki/INDEX.md` lists every topic with a one-line description. Each topic file starts with a summary paragraph and links to related topics using `[[topic-name]]` syntax. Research papers are cited as clickable markdown links.

The HTML wiki at `wiki_html/index.html` mirrors the Markdown wiki with self-contained, dependency-free HTML pages styled according to `DESIGN.md`.

## Key Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Schema and rules for AI agents maintaining this vault |
| `DESIGN.md` | Design system tokens for all HTML wiki pages |
| `COMPILE.md` | Prompt used to compile raw sources into the wiki |
| `HEALTHCHECK.md` | Health check queries for the vault |
| `QUERIES.md` | Example queries for exploring the knowledge base |
| `wiki/LOG.md` | Change log for all raw source additions and updates |

## Slides

Wiki articles can be compiled into Marp slide decks:

```bash
npm run slides          # compile a specific topic
npm run slides:all      # compile all topics
npm run slides:clean    # remove generated slides
```

Output lands in `outputs/slides/`.

## Interests

AI · Math · Omniverse · Robotics · Investing · XR · LeRobot · Game Programming · Computer Graphics · System Design
