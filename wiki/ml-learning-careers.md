# ML Learning and Career Development

Becoming an ML engineer is less about following a credential pipeline and more about building tight loops between intuition, implementation, feedback, and real problems. The notes here converge on the same thesis from different angles: use AI to accelerate understanding, not to bypass it, and create direct evidence of skill through demos and shipped work.

## Source

- `raw/00-clippings/The Complete Guide How to Become an ML Engineer.md`
- `raw/00-clippings/high-school-dropout-self-taught-via-chatgpt-becomes-openai-research-scientist.md`
- `raw/00-clippings/Thread by @gabriel1.md`

## What an ML Engineer Actually Does

The raw guide makes an important distinction:
- **Researchers** push the frontier
- **Data scientists** analyze data and answer business questions
- **ML engineers** make models work in production

That means the job is a blend of:
- model training and fine-tuning
- data pipelines
- deployment and monitoring
- inference optimization
- integration into real applications

This is why the required skill stack spans both [[neural-networks]] and [[mlops]].

## The Learning Loop That Actually Works

The strongest recurring pattern is not passive content consumption. It is an iterative loop:

1. Pick a concrete thing to understand or build
2. Implement it
3. Debug it until it works
4. Ask for conceptual explanation
5. Ask for the intuition
6. Ask for the math intuition
7. Re-explain it in simpler terms until it truly clicks

That is exactly the workflow described in the short `@gabriel1` thread, and it matches Gabriel Petersson's much more detailed "recursive gap filling" method.

### Top-Down Learning

The anti-pattern is spending years on prerequisites before touching the thing you actually care about.

The proposed alternative:
- start from the real target (for example diffusion models)
- ask what sub-concepts block understanding
- drill down recursively only where needed
- use AI to explain the missing pieces in progressively simpler language

The key distinction is sharp:
- **bad shortcut**: skip understanding
- **good shortcut**: reach understanding faster

Gabriel Petersson states this explicitly: the goal is to take shortcuts **to the fundamentals**, not around them.

## How to Study Technical Material

The guide's two-pass rule is pragmatic:

### First Pass

- watch straight through
- do not pause constantly
- build the mental scaffold first

### Second Pass

- pause often
- rewrite notes in your own words
- type all code manually
- break the code on purpose
- vary parameters and observe behavior

This is slower than passive watching, but it creates the internal model you need for real engineering.

## Suggested Learning Path

The source proposes a staged curriculum.

### 1. Intuition First

Use 3Blue1Brown to build visual intuition for:
- neural networks
- gradient descent
- backpropagation
- transformers
- attention
- diffusion

### 2. Implementation Second

Use Andrej Karpathy's material to build systems from scratch:
- `micrograd`
- `makemore`
- GPT
- a tokenizer

This stage matters because writing the components yourself removes the "black box" feeling around modern ML.

### 3. Broader Context Third

After intuition and implementation, add broader context:
- how LLM training stacks fit together
- where supervised fine-tuning and RL enter
- how model behavior, failure modes, and tooling fit into the bigger system

## Real Problems Beat Abstract Study

Another strong claim from Gabriel Petersson's story: learning gets easier when the problem is real.

Why:
- the task decomposes naturally into smaller sub-problems
- feedback is immediate
- pressure forces focus
- the knowledge has an obvious purpose

This is why startup work, integrations, demos, and customer-facing problems can compress learning faster than abstract exercises alone.

## Career Strategy: Direct Evidence Beats Proxies

Degrees, internships, and school prestige are all proxies for capability. They become less important when you can show direct proof.

The recommended strategy is brutally simple:
- build something understandable in seconds
- show it to decision-makers, not process gatekeepers
- use the demo to prove you can create value

The argument is not that credentials never matter. It is that a working demo and strong code can bypass weaker proxies when the buyer actually understands the work.

## High-Leverage Career Habits

- Seek environments with strong code review culture
- Ask why feedback is correct, not just what to change
- Prefer real output over resume decoration
- Stay close to people and teams with high standards

The story here is not anti-learning or anti-mentorship. It is anti-passivity.

## The Core Thesis

AI changes the learning economics of ML:
- foundational knowledge is easier to access
- debugging and explanation loops are faster
- implementation barriers are lower

But the bottleneck does not disappear. It just moves to judgment:
- noticing what you still do not understand
- verifying that your explanation is actually correct
- reading code carefully instead of "vibe learning"

## Related Topics

- [[ai-coding]] — AI as a collaborator for implementation and review
- [[attention-transformers]] — the core architecture modern ML engineers must understand
- [[neural-networks]] — the mechanical foundations behind model training
- [[mlops]] — the production side of ML engineering work
