# Component Catalog

All 20 files in this directory are self-contained HTML examples from the thariqs "unreasonable effectiveness of HTML" collection. Before building any wiki_html page, scan this catalog, pick the components whose patterns fit the content, and adapt their code (do NOT copy entire files — extract only the relevant structure and scripts, then restyle using DESIGN.md tokens).

---

## Exploration & Comparison

### `01-exploration-code-approaches.html`
**Pattern:** Three-column side-by-side card layout. Each column has a header badge, pros/cons list, and a highlighted code snippet area.
**Use when:** Comparing multiple algorithms, architectures, or frameworks (e.g., attention mechanisms, optimizers, model families).
**Key elements:** Column grid, approach cards, trade-off badges, no JavaScript.

### `02-exploration-visual-designs.html`
**Pattern:** 2×2 grid of visual direction tiles, each with a thumbnail preview area and descriptive label.
**Use when:** Showing visual variations — e.g., different model output formats, dataset visualizations, UI paradigms.
**Key elements:** Thumbnail grid, labeled tiles, hover highlight, no JavaScript.

---

## Planning & Roadmaps

### `16-implementation-plan.html`
**Pattern:** Vertical milestone timeline + data-flow diagram (SVG) + risk table with severity rows.
**Use when:** Research roadmaps, training pipeline overviews, project breakdowns.
**Key elements:** Timeline with status dots, annotated SVG diagram, risk/severity table, 1 script tag.

---

## Code Review & Walkthroughs

### `03-code-review-pr.html`
**Pattern:** Annotated diff view with inline margin notes, severity tags (error/warning/info), and jump links.
**Use when:** Explaining code patterns, showing before/after implementations, annotating training scripts.
**Key elements:** Diff lines with color-coded additions/deletions, sidebar annotation callouts.

### `17-pr-writeup.html`
**Pattern:** Structured document with motivation, before/after panels, file-by-file tour, and reviewer focus list.
**Use when:** Explaining what changed in a paper/model update, annotated paper walkthroughs.
**Key elements:** Before/after split panels, section anchor nav, bullet checklists.

### `04-code-understanding.html`
**Pattern:** Module dependency graph rendered as connected boxes with directed arrows (SVG).
**Use when:** Architecture diagrams — encoder/decoder flows, agent orchestration graphs, system component maps.
**Key elements:** SVG node graph, labeled edges, color-coded node types, 1 script.

---

## Design System Reference

### `05-design-system.html`
**Pattern:** Color swatch grid, typography scale specimens, spacing ruler, interactive token table.
**Use when:** Documenting a model's visual output format, showing dataset label taxonomy, rendering a full token vocabulary.
**Key elements:** Swatch grid, type scale demo, token table with search, 1 script.

### `06-component-variants.html`
**Pattern:** Matrix table where rows = components, columns = states (default/hover/active/disabled). Each cell is a live rendered component.
**Use when:** Comparing model variants across tasks, showing hyperparameter sweep results in a structured grid.
**Key elements:** State matrix table, variant rows, live HTML component cells, 1 script.

---

## Interactive Prototypes

### `07-prototype-animation.html`
**Pattern:** CSS keyframe animation demo with a stage area, play/pause control, and a timeline bar. Includes confetti burst effect.
**Use when:** Demonstrating dynamic processes — training curves, token generation, attention flow over time.
**Key elements:** Animated stage, timeline scrubber, ease controls, CSS-only animation fallbacks.

### `08-prototype-interaction.html`
**Pattern:** Drag-to-reorder list with JS drag events, live count indicator, and sidebar annotations.
**Use when:** Ranking interfaces, priority queues, interactive concept ordering (e.g., importance of features).
**Key elements:** Draggable list items, drag handle grips, JS dragstart/dragover/drop, sidebar notes.

---

## Diagrams & Illustrations

### `10-svg-illustrations.html`
**Pattern:** Three themed SVG header illustrations with consistent icon style (stroked paths, filled shapes in design-system colors). Includes a palette key.
**Use when:** Generating visual headers for wiki topic pages. Adapt the SVG geometry to represent the topic (e.g., a neural network graph, a robot arm).
**Key elements:** Inline SVG, stroked/filled path styles in design tokens, 1 script for color theme toggle.

### `13-flowchart-diagram.html`
**Pattern:** Annotated process flowchart with decision gates (yes/no branches), step nodes, and a legend panel.
**Use when:** Training pipelines, inference flows, data preprocessing steps, algorithm decision trees.
**Key elements:** SVG flowchart, gate nodes (diamond shapes), yes/no edge labels, annotation chips, legend.

---

## Presentations & Decks

### `09-slide-deck.html`
**Pattern:** Paginated slide layout with prev/next controls, slide number indicator, and structured content per slide.
**Use when:** Summary views of a paper, multi-concept overviews where scrolling doesn't suit the content.
**Key elements:** Slide container, JS page navigation, progress dot indicators.

---

## Research Explainers

### `14-research-feature-explainer.html`
**Pattern:** Step-by-step tabbed walkthrough. Tab bar at the top, each tab reveals one stage of how something works. Includes `callout` highlight boxes, a TLDR summary, and a FAQ section.
**Use when:** Explaining how an algorithm works step-by-step (backprop, attention, RAG pipeline, RLHF). The most versatile component for technical wiki pages.
**Key elements:** `.tabbar` / `.tabs` with JS tab switching, `.callout` boxes, `.tldr` summary, `.faq` accordion-style section, file/code highlights.

### `15-research-concept-explainer.html`
**Pattern:** Interactive ring/circle diagram (SVG) where nodes are clickable, updating a detail panel. Includes a controls bar and a key legend.
**Use when:** Circular or graph-structured concepts — attention heads, transformer layers, hash rings, neural network architectures.
**Key elements:** SVG ring with labeled arc segments, JS click-to-highlight, detail readout panel, `.controls` bar.

---

## Status & Reports

### `11-status-report.html`
**Pattern:** Weekly status report with metric cards (number + trend arrow), progress bars, team/work item tables, and a "blockers" callout.
**Use when:** Summarizing benchmark results, model leaderboard comparisons, training run status.
**Key elements:** Metric KPI cards, progress bars with percentage labels, status badge chips (green/yellow/red), blockers section.

### `12-incident-report.html`
**Pattern:** Incident timeline (vertical, time-stamped), impact summary table, root cause section, and action items checklist.
**Use when:** Documenting known failure modes, paper retraction notes, model safety incidents, ablation study findings.
**Key elements:** Vertical timeline with timestamps, impact severity table, action item checkboxes.

---

## Custom Editors & Tools

### `18-editor-triage-board.html`
**Pattern:** Kanban-style board with three columns (To Triage / In Review / Done), draggable cards, and filter chips.
**Use when:** Research topic roadmap, paper reading queue, concept prioritization boards on index-like pages.
**Key elements:** Three-column flex layout, draggable cards with JS, filter chip bar, card count badges.

### `19-editor-feature-flags.html`
**Pattern:** Toggle-switch interface for boolean settings, with live JSON preview panel and search/filter.
**Use when:** Model hyperparameter reference, configuration options overview, feature comparison matrices with on/off states.
**Key elements:** Toggle switches (CSS + JS), live JSON output panel, search input with JS filter.

### `20-editor-prompt-tuner.html`
**Pattern:** Split-pane editor — left side is a prompt textarea with variable slots highlighted, right side shows a live rendered preview that updates on input.
**Use when:** LLM, RAG, or agent wiki pages where showing prompt templates interactively adds value.
**Key elements:** Textarea with highlighted `{{variable}}` spans, live preview pane, JS input event binding, copy-to-clipboard button.

---

## Component Selection Guide

| Wiki topic type | Recommended components |
|----------------|----------------------|
| Algorithm explanation (backprop, attention, etc.) | `14` (tabs + callouts), `15` (ring diagram), `13` (flowchart) |
| Architecture / system diagram | `04` (node graph), `13` (flowchart), `16` (timeline) |
| Model / framework comparison | `01` (side-by-side), `06` (variant matrix), `11` (metrics) |
| Training / pipeline overview | `13` (flowchart), `16` (plan + timeline), `07` (animation) |
| LLM / agent / prompt topics | `20` (prompt tuner), `14` (tabs), `04` (graph) |
| Paper walkthrough | `14` (tabs), `17` (PR writeup style), `15` (concept ring) |
| Benchmark / leaderboard | `11` (status report), `06` (variant matrix) |
| Interactive concept demo | `15` (ring), `08` (drag), `07` (animation) |
| SVG header illustration | `10` (svg illustrations) |
| Index / hub page | `18` (triage board style), design-system card grid |
