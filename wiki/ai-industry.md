# AI Industry and Organizations

This page covers insights into how leading AI companies are structured, how they operate, and what organizational patterns are emerging in the AI-native era. Primary case study: Moonshot AI (Kimi), a Chinese AI startup that reached a $16B valuation in three years with ~300 employees.

## Source

- `raw/00-clippings/100 Hours Inside Kimi.md`

## Moonshot AI (Kimi) — Key Observations

### Profile

- **Founded:** ~2023, Tsinghua University alumni (5 co-founders)
- **Valuation:** RMB 120 billion (~$16B USD) as of early 2026
- **Headcount:** ~300 employees, average age under 30
- **Focus:** Model capability above all else; shifted from consumer chatbot → open-source models → agent products (Kimi Agent, Kimi Code, Kimi CLI)

### The DeepSeek Moment

When DeepSeek launched in early 2025, it reshuffled the Chinese AI landscape:
- Growth team experienced an existential crisis: candidates asked "why Kimi over DeepSeek?"
- Algorithm team reaction was **excitement**, not fear — DeepSeek proved a lower-cost, open-source path could earn global respect
- The company responded by narrowing focus to model quality above all else
- Internal attitude: "DeepSeek saved us" — it clarified strategy and built internal cohesion

### Hiring Philosophy: "Taste"

Kimi's highest hiring standard is **taste** — an aesthetic and intellectual sense that is impossible to quantify but pervasive in the product, the naming conventions, the code.

- ~80% of staff from China's elite 985/211 universities, but credentials are not the filter
- Preferred candidates: early-stage startup founders, people who can "see through time"
- 50+ employees previously founded or joined startups
- 100+ hires in the past year came from peer referrals ("human-to-human transmission")
- Kimi "likes hiring CEOs" — founder-like DNA is an operating assumption

### Generalization Ability

A key selection criterion: can this person adapt to a completely new domain?

- Traditional big-tech employees are like **specialized models** — overfit to a particular KPI system; fail to adapt when environment changes
- Kimi wants **base models** — people who first learn basic rules (supervised fine-tuning), then acquire transfer ability through repeated self-play across domains (reinforcement learning analogy)
- 80%+ of interviewed employees were doing something completely different from their previous job

### Organizational Structure

- **No formal departments, no hierarchy, no titles, no OKRs, no KPIs**
- Co-founders interface directly with ~40–50 employees each
- Yang Zhilin's status message: **"Communicate directly"**
- Decision-making: anyone can be persuaded if the facts are clear enough — respect for objective reality over ego

**Tradeoff:** Without top-down OKRs, some employees experience "weightlessness" — uncertainty about direction and performance. The structure works for self-motivated geniuses; ordinary people may feel lost.

**Scaling concern:** Extreme flatness historically hits decision bottlenecks at ~500 people (c.f. holacracy failures). The company acknowledges this risk.

### AI-Native Operations

- Employees increasingly prefer interacting with AI over humans (simpler, more reliable)
- Product managers run **agent swarms**: strategy agent, translation agent, competitor monitoring agent — compress multi-day multi-person work into hours
- The model is both the **goal** (what they're building) and the **tool** (how they work)

### "Two-Dimensional Foil" Metaphor

The article uses a reference from *The Three-Body Problem*: a weapon that collapses 3D space into 2D, eliminating depth.

Moonshot AI has deliberately "flattened" itself:
- No vertical hierarchy, no horizontal departmental walls, no political tangles
- Only "model" and "intelligence" facing each other directly
- The endpoint: if model intelligence crosses a critical threshold, the organizational pain is justified

### Long-Context Research: MoBA

Kimi's engineers developed **MoBA (Mixture of Block Attention)** to enable 128K+ context (vs the 4K industry standard in 2023):
- MoBA v0.5: required rewriting the training framework mid-run — too costly, shelved
- MoBA v1: worked on small models, failed on large ones (loss spikes)
- MoBA v2: required a "saturation rescue" with experts from across the company; changed attention in final layers to fix long-summary tasks
- Three retreats over ~18 months; the project was never killed

## Patterns in AI-Native Companies

| Pattern | Description |
|---------|-------------|
| Flat hierarchy | Few or no management layers; direct communication |
| Agent-augmented work | Individual contributors manage fleets of AI agents |
| Generalization over specialization | Cross-functional contributors over narrow specialists |
| Model-as-product AND model-as-tool | The same model being built is used internally |
| Trust through dense peer networks | Referral-heavy hiring builds implicit trust without process |
| Anti-OKR | Outcome ownership is personal, not managed via metric systems |

## Related Topics

- [[attention-transformers]] — long-context attention research (MoBA); RL as core training paradigm
- [[distributed-training]] — the infrastructure behind training frontier models
- [[robot-learning]] — reinforcement learning as "the future" (Kimi co-founder Yang Zhilin's thesis)
- [[ai-coding]] — AI-native workflows and agent swarms
- [[mlops]] — productionizing models at scale
