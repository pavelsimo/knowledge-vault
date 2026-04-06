# AI Agents: Sub-Agents and Agent Teams

Multi-agent systems in Claude let you decompose complex tasks across specialized Claude instances. Two distinct paradigms exist: sub-agents for parallel isolated work, and agent teams for ongoing coordinated collaboration. Choosing the wrong paradigm creates more overhead than the work itself.

## Source

- `raw/00-clippings/Claude Subagents vs. Agent Teams, explained.md`
- `raw/00-clippings/OpenClaw + CodexClaudeCode Agent Swarm The One-Person Dev Team Full Setup.md`

## The Core Distinction

The right question is never "should I use multiple agents?" but "what kind of coordination does this task actually need?"

| Property | Sub-Agents | Agent Teams |
|---|---|---|
| **Lifecycle** | Short-lived, fire-and-forget | Long-running, persistent |
| **Communication** | Parent → sub-agent → result only | Peer-to-peer between teammates |
| **Shared state** | None | Shared task list with dependencies |
| **Result** | Compressed output back to parent | Continuous coordination |
| **Best for** | Embarrassingly parallel work | Ongoing negotiation between tasks |

The architectural difference is fundamental: sub-agents are workers who go off, complete a task, and return a distilled result. Agent teams are a persistent crew working in the same room, talking directly to each other as they go.

## Sub-Agents: Parallelism Through Isolation

A sub-agent is a specialized Claude instance running in its own **isolated context window**. Think of it like a research lead delegating focused questions to specialized researchers — each researcher works independently, comes back with distilled findings, and the lead synthesizes everything.

Each sub-agent receives:
- Its own system prompt defining its specialty
- A specific set of tools it can access
- A clean, isolated context window
- One job to do

When it finishes, only the final result returns to the parent — not the full reasoning chain, not intermediate steps. Just the compressed output. This is the key point: sub-agents provide **context compression**, not just parallelism. You distill a vast amount of exploration into a clean signal without polluting the parent's context with noise.

**One hard constraint:** sub-agents cannot spawn other sub-agents, and they cannot talk to each other. Every result flows back to the parent. The parent is the sole coordinator. This is a feature — it keeps the system predictable. You always know where information flows and where decisions get made.

### SDK Example

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review the authentication module for security vulnerabilities",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                "security-reviewer": AgentDefinition(
                    description="Security specialist. Use for vulnerability checks and security audits.",
                    prompt="You are a security specialist with expertise in identifying vulnerabilities.",
                    tools=["Read", "Grep", "Glob"],
                    model="sonnet",
                ),
                "performance-optimizer": AgentDefinition(
                    description="Performance specialist. Use for latency issues and optimization reviews.",
                    prompt="You are a performance engineer with expertise in identifying bottlenecks.",
                    tools=["Read", "Grep", "Glob"],
                    model="sonnet",
                ),
            },
        ),
    ):
        print(message)
```

The `description` field is the routing signal. When the prompt mentions "security vulnerabilities," the parent routes to `security-reviewer` not `performance-optimizer`. Keep descriptions specific and unambiguous.

## Agent Teams: Coordination Through Communication

Agent teams are fundamentally different. Where sub-agents are short-lived workers that complete a task and disappear, agent teams are long-running instances that persist, communicate directly with each other, and coordinate through shared state.

An agent team has three moving parts:

1. **A team lead** — coordinates work, assigns tasks, synthesizes results
2. **Teammates** — independent agent instances, each with their own context window, working in parallel
3. **A shared task list** — tracks what's pending, in-progress, and done, along with dependencies between tasks

### Lifecycle Example

```
Claude (Team Lead):
└── spawnTeam("auth-feature")
    Phase 1 - Planning:
    └── spawn("architect", prompt="Design OAuth flow", plan_mode_required=true)
    Phase 2 - Implementation (parallel):
    └── spawn("backend-dev", prompt="Implement OAuth controller")
    └── spawn("frontend-dev", prompt="Build login UI components")
    └── spawn("test-writer", prompt="Write integration tests", blockedBy=["backend-dev"])
```

The `blockedBy` field on the test writer is the shared task list doing real coordination — the test writer won't start until the backend agent finishes, without the lead having to manually manage that sequencing.

**Key capability:** teammates send messages directly to each other. A frontend agent can tell a backend agent "the API response structure needs to change" and the backend agent adjusts — without routing everything through the lead. You can also interact with individual teammates directly without going through the lead.

## Context-Centric Decomposition

Most multi-agent designs fail because people split work by **role** instead of by **context**.

**Wrong approach — role-based splitting:**
```
Planner → Implementer → Tester
```
This creates a telephone game where information degrades at every handoff:
- The implementer doesn't have what the planner knew
- The tester doesn't have what the implementer decided
- Quality drops at every boundary

**Right approach — context-centric splitting:**

Ask: what context does this subtask actually need? If two subtasks need deeply overlapping information, they belong to the same agent. If they can operate with truly isolated information and clean interfaces between them, that's where you split.

**Practical example:** an agent implementing a feature should also write the tests for that feature. It already has the full context. Splitting those into separate agents creates a handoff problem that costs more than any parallelism benefit.

Only separate when context can be genuinely isolated.

## The Five Orchestration Patterns

These five patterns cover most real-world multi-agent needs:

| Pattern | Description | When to Use |
|---|---|---|
| **Prompt chaining** | Sequential steps; each call processes previous output | Order matters, steps are dependent |
| **Routing** | Classifier decides which specialized handler gets the task | Easy tasks → cheap/fast model; hard tasks → capable model |
| **Parallelization** | Independent subtasks run simultaneously | Same task multiple times for voting, or different subtasks sectioned out |
| **Orchestrator-worker** | Central agent breaks down task, delegates to workers, synthesizes | Most production systems; dominant architecture for both sub-agents and agent teams |
| **Evaluator-optimizer** | One agent generates, another evaluates and provides feedback in a loop | Quality matters more than speed; single pass is unreliable |

The orchestrator-worker pattern is the architecture that most real production systems use.

## When NOT to Use Multi-Agent Systems

This is what most guides skip. Teams have spent months building elaborate multi-agent pipelines only to discover that better prompting on a single agent achieved equivalent results.

**Multi-agent systems earn their cost in three situations:**

1. **Context protection** — a subtask generates information irrelevant to the main task; keeping it in a sub-agent prevents context bloat
2. **True parallelization** — independent research or search tasks that genuinely benefit from simultaneous coverage
3. **Specialization** — the task requires conflicting system prompts, or one agent is juggling so many tools that performance degrades

**They are the wrong call when:**
- Agents constantly need to share context with each other
- Inter-agent dependencies create more overhead than execution value
- The task is simple enough that one well-prompted agent handles it

**Special warning for coding:** parallel agents writing code make incompatible assumptions. When you merge their work, those implicit decisions conflict in ways that are hard to debug. Sub-agents for coding should **answer questions and explore, not write code simultaneously** with the main agent.

## Common Failure Modes

**1. Vague task descriptions → agents duplicate each other's work**

Every agent needs: clear objective, expected output format, guidance on tools/sources to use, explicit boundaries on what it should NOT cover. Without this, two agents research the same thing and neither notices.

**2. Verification agents declare victory without verifying**

Use explicit, concrete instructions: run the full test suite, cover these specific cases, do not mark as complete until each one passes. Vague approval criteria produce false positives.

**3. Token costs compound faster than expected**

Tier your models intelligently:
- Most capable model → where it genuinely matters
- Faster, cheaper models → routine work
- Build in budget controls so costs can't run away

## The One Design Principle

**Design around context boundaries, not around roles or org charts.**

Start with a single agent. Push it until you find where it breaks. That failure point tells you exactly what to add next. Add complexity only where it solves a real, measured problem.

## Orchestration Layer in Practice: The Two-Tier System

Context windows are zero-sum. You have to choose what goes in. Fill it with business context and you have no room for the codebase. Fill it with code and the agent knows nothing about why it matters. This constraint drives the two-tier production architecture.

### Context Comparison: Orchestrator vs. Coding Agent

| | Orchestrator | Coding Agent |
|---|---|---|
| **Business context** | Customer CRM, meeting notes, competitor intel, who's paying | None |
| **Technical context** | Minimal code | Repo conventions, design docs, API schemas, src/ codebase |
| **Memory** | MEMORY.md, daily notes, past decisions | Just the task prompt |
| **Good at** | Understanding why, customer priorities, writing prompts, research | Following conventions, writing correct code, running tests |
| **Bad at** | Writing actual code, file structures, code conventions | Knowing why it matters, prioritizing features, long-term memory |

Each tier is loaded with exactly what it needs. Specialization through context, not through different models.

### Production System Architecture

The orchestrator receives inputs from multiple sources — error logs (Sentry), support tickets, direct instruction, and meeting notes — and holds connections to business resources: Obsidian vault, memory system, skills, emails, and read-only production database. It translates all this into precise prompts for downstream coding agents.

The coding agents (Codex, Claude Code, Gemini) each operate in isolated git worktrees — separate branch checkouts where they can make changes without affecting each other. Each agent runs in its own tmux session for mid-task redirection:

```bash
# Redirect without killing the agent
tmux send-keys -t codex-templates "Stop. Focus on the API layer first, not the UI." Enter
```

All agent activity flows through a task registry that tracks state. Agents don't report directly to the human — a monitoring cron job checks registry state every 10 minutes, polls CI status via `gh cli`, auto-respawns failed agents (up to 3 attempts), and only notifies the human when something requires attention.

### Automated PR Pipeline

Every PR goes through a fixed definition of done before human review is requested:
1. PR created with branch synced to main (no merge conflicts)
2. CI passing: lint → typecheck → unit tests → E2E against preview environment
3. Three AI reviewers post comments:
   - **Codex reviewer** — deep edge case analysis; catches logic errors and race conditions; low false positive rate
   - **Gemini Code Assist** — security issues and scalability; suggests specific fixes; free
   - **Claude Code reviewer** — cautious, validates what others flag; mostly overengineering suggestions
4. Human reviews for 5–10 minutes: by this point CI has passed, three reviewers approved, and screenshots show UI changes

The human merge is the reward signal. When a PR ships, the prompt structure that produced it gets logged — "this works for billing features," "Codex needs type definitions upfront," "always include test file paths." The orchestrator writes better prompts over time because it remembers what shipped.

### Hardware Reality

Each parallel agent needs its own worktree, its own `node_modules`, and runs its own builds, type checks, and tests. Five simultaneous agents means five TypeScript compilers, five test runners, and five sets of dependencies in RAM. On 16 GB, the practical limit is 4–5 agents before swapping degrades performance. This is the actual bottleneck for scaling agent parallelism — not model costs, but RAM.

## Source

- `raw/00-clippings/OpenClaw + CodexClaudeCode Agent Swarm The One-Person Dev Team Full Setup.md`

## Related Topics

- [[attention-transformers]] — the transformer architecture powering each agent instance
- [[rag]] — agentic RAG combines retrieval with multi-agent orchestration
- [[ai-coding]] — sub-agents for codebase exploration; teams for full feature implementation
- [[mlops]] — deploying and monitoring multi-agent production systems
