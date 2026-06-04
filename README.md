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

### raw/ topics

| Directory | Content |
|-----------|---------|
| `00-clippings` | Web clippings and reference snippets |
| `01-open-source-models-hugging-face` | Hugging Face course material |
| `02-cs109-probability-for-computer-scientists` | Stanford CS109 probability course |
| `03-stanford-cs231n` | Stanford CS231n computer vision course |
| `04-machine-learning-engineering-for-production-mlops` | MLOps course material |
| `05-omniverse` | NVIDIA Omniverse and OpenUSD notes |
| `06-system-design` | System design references |
| `07-hailo-setup` | Hailo-8 edge AI accelerator setup notes |
| `08-llm-from-scratch-with-python-freecodecamp` | LLM from scratch course |
| `09-tmux` | Tmux reference and cheat sheets |

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
