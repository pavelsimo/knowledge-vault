AI skills are reusable folders of instructions, examples, evals, and optional memory that let an assistant reliably perform a recurring task without reloading every detail into the conversation. The Claude Skills tutorial frames a good skill as a small harness: explicit trigger description, progressively disclosed context, manual tests, pass/fail evals, clean-context review, and human taste at the end.

## Source

- [[raw/00-clippings/The Only Claude Skills Tutorial You Need (Add Evals and Memory).md|raw/00-clippings/The Only Claude Skills Tutorial You Need (Add Evals and Memory).md]]

## What a Skill Contains

A skill is a directory that the AI can trigger for a task. The source's example is an editing skill for long-form posts, but the structure generalizes:

| File or layer | Purpose |
|---|---|
| `SKILL.md` | Concise workflow and rules the assistant reads when the skill triggers |
| Description | Routing signal that tells the assistant when to load the full skill |
| Examples | Personal or task-specific reference outputs loaded only when relevant |
| `evals.md` | Pass/fail checks that let the assistant grade its own output |
| `memory.md` | Short reverse-chronological lessons from previous uses |
| Skill editor | A meta-skill for keeping other skills concise and readable |

The key design rule is progressive disclosure: keep the main instructions short, and put bulky examples or personal context in separate files so the model loads only what the task needs.

## Build Workflow

The tutorial's five-step process:

1. Give the AI best examples and personal context, then ask it to draft the skill.
2. Audit the description so the skill triggers reliably.
3. Test the skill manually on real input.
4. Add pass/fail evals and make the skill loop until checks pass.
5. Add concise memory for lessons that improve the skill over time.

This is [[agent-harness]] thinking at skill scale. The skill is not just prose instructions; it is a repeatable loop with state, examples, evaluation, and revision.

## Evals Beat Vibes

The most useful evals are concrete pass/fail checks, not vague scores. The source is skeptical of "4 out of 5" style grading because LLMs often cannot consistently distinguish adjacent numeric scores.

Better checks look like:

- Does the intro contain a clear hook?
- Does the tutorial include the required link or call to action?
- Are banned phrases absent?
- Is the output practical enough for the target reader?
- Does the final section ask the reader to take a concrete next step?

For higher-quality grading, the tutorial recommends using a separate agent or clean context window to run evals. That reduces bias from the editing agent's own previous work.

## Memory Without Bloat

Skill memory should capture lessons that are hard to encode as pass/fail rules. It should not duplicate the eval file.

Good memory entries are short:

- what was learned
- what changed in the user's preference
- what the skill should do differently next time

Memory is useful for taste, tone, and fuzzy quality judgments. Evals are better for crisp constraints.

## Human Taste Remains

The tutorial's final point is practical: even a strong skill may get an output 80-90 percent of the way there. Human judgment still matters for the last pass, especially where taste, context, or reputational risk is involved.

This connects to [[recursive-self-improvement]]: reusable skills, eval loops, and memory can make AI-assisted work compound, but the bottleneck shifts toward judgment, review, and verification.

## Related Topics

- [[agent-harness]] - the broader infrastructure pattern behind skill loops
- [[codex-workflows]] - skills as reusable routines inside durable AI work streams
- [[ai-coding]] - applying skills to coding and writing workflows
- [[ai-agents]] - evaluators, optimizers, and tool-using agents
- [[recursive-self-improvement]] - compounding AI-assisted improvement through tools and evals
